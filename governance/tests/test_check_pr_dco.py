from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

GOVERNANCE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOVERNANCE_DIR))

CHECKER_PATH = GOVERNANCE_DIR / "check_pr_dco.py"
SPEC = importlib.util.spec_from_file_location("check_pr_dco", CHECKER_PATH)
assert SPEC and SPEC.loader
check_pr_dco = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_pr_dco)


class PullRequestDCOTests(unittest.TestCase):
    def test_accepts_every_signed_commit(self) -> None:
        records = [
            {
                "sha": "a" * 40,
                "commit": {"message": "First\n\nSigned-off-by: Ada Developer <ada@example.com>"},
            },
            {
                "sha": "b" * 40,
                "commit": {"message": "Second\n\nSigned-off-by: Ben Developer <ben@example.com>"},
            },
        ]
        self.assertEqual(check_pr_dco.unsigned_commits(records), [])

    def test_reports_each_unsigned_commit(self) -> None:
        records = [
            {"sha": "a" * 40, "commit": {"message": "Unsigned one"}},
            {
                "sha": "b" * 40,
                "commit": {"message": "Signed\n\nSigned-off-by: Ben Developer <ben@example.com>"},
            },
            {"sha": "c" * 40, "commit": {"message": "Unsigned two\n\nBody"}},
        ]
        self.assertEqual(
            check_pr_dco.unsigned_commits(records),
            [("a" * 40, "Unsigned one"), ("c" * 40, "Unsigned two")],
        )

    def test_rejects_empty_pull_request(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least one commit"):
            check_pr_dco.fetch_pr_commits("owner/repo", 1, "token", 0)

    def test_rejects_more_than_github_pr_commit_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "at most 250"):
            check_pr_dco.fetch_pr_commits("owner/repo", 1, "token", 251)

    def test_fails_closed_when_api_count_differs(self) -> None:
        with mock.patch.object(check_pr_dco, "_get_json", side_effect=[[], []]):
            with self.assertRaisesRegex(RuntimeError, "expected 2"):
                check_pr_dco.fetch_pr_commits("owner/repo", 1, "token", 2)

    def test_paginates_until_expected_count(self) -> None:
        first = [
            {"sha": f"{index:040d}", "commit": {"message": f"Commit {index}"}}
            for index in range(100)
        ]
        second = [
            {"sha": f"{index:040d}", "commit": {"message": f"Commit {index}"}}
            for index in range(100, 101)
        ]
        with mock.patch.object(check_pr_dco, "_get_json", side_effect=[first, second]) as get_json:
            records = check_pr_dco.fetch_pr_commits("owner/repo", 17, "token", 101)
        self.assertEqual(len(records), 101)
        self.assertEqual(get_json.call_count, 2)


if __name__ == "__main__":
    unittest.main()
