from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from check_dco import has_valid_signoff

MAX_GITHUB_PR_COMMITS = 250


def unsigned_commits(records: list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Return (sha, subject) pairs for commits missing a valid DCO sign-off."""
    failures: list[tuple[str, str]] = []
    for record in records:
        sha = str(record.get("sha", ""))
        commit = record.get("commit") or {}
        message = str(commit.get("message", ""))
        subject = message.splitlines()[0] if message else ""
        if not has_valid_signoff(message):
            failures.append((sha, subject))
    return failures


def _get_json(url: str, token: str) -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "cervel-public-dco-check",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_pr_commits(repository: str, pr_number: int, token: str, expected_count: int) -> list[dict[str, Any]]:
    """Fetch all PR commits from GitHub, failing closed beyond GitHub's 250-commit PR limit."""
    if expected_count < 1:
        raise ValueError("pull request must contain at least one commit")
    if expected_count > MAX_GITHUB_PR_COMMITS:
        raise ValueError(
            f"pull request has {expected_count} commits; DCO enforcement supports at most "
            f"{MAX_GITHUB_PR_COMMITS}. Split the pull request into smaller changes."
        )

    records: list[dict[str, Any]] = []
    page = 1
    while len(records) < expected_count:
        query = urllib.parse.urlencode({"per_page": 100, "page": page})
        url = f"https://api.github.com/repos/{repository}/pulls/{pr_number}/commits?{query}"
        batch = _get_json(url, token)
        if not isinstance(batch, list):
            raise RuntimeError("GitHub returned an unexpected response while listing pull-request commits")
        if not batch:
            break
        records.extend(batch)
        page += 1

    if len(records) != expected_count:
        raise RuntimeError(
            f"expected {expected_count} pull-request commits but GitHub returned {len(records)}; failing closed"
        )
    return records


def main() -> int:
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    pr_number_raw = os.environ.get("PR_NUMBER", "")
    commit_count_raw = os.environ.get("PR_COMMIT_COUNT", "")

    if not repository or not token or not pr_number_raw or not commit_count_raw:
        print("FAIL DCO gate configuration: required environment is missing", file=sys.stderr)
        return 2

    try:
        pr_number = int(pr_number_raw)
        expected_count = int(commit_count_raw)
        records = fetch_pr_commits(repository, pr_number, token, expected_count)
    except (ValueError, RuntimeError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(f"FAIL DCO gate: {exc}", file=sys.stderr)
        return 2

    failures = unsigned_commits(records)
    if failures:
        for sha, subject in failures:
            short_sha = sha[:12] if sha else "unknown"
            print(f"FAIL {short_sha}: missing valid Signed-off-by trailer — {subject}")
        print(f"DCO sign-off required on every pull-request commit; unsigned commits: {len(failures)}")
        return 1

    for record in records:
        sha = str(record.get("sha", ""))
        print(f"PASS {sha[:12]}: DCO sign-off present")
    print(f"Checked {len(records)} pull-request commit(s); unsigned commits: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
