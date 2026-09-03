from __future__ import annotations

import re
import sys
from pathlib import Path

SIGNED_OFF_BY = re.compile(
    r"^Signed-off-by:\s+[^<>\n]+\s+<[^<>\s]+@[^<>\s]+>$",
    re.IGNORECASE | re.MULTILINE,
)


def has_valid_signoff(message: str) -> bool:
    """Return True when a commit message contains a syntactically valid DCO trailer."""
    return SIGNED_OFF_BY.search(message) is not None


def check_messages(messages: list[tuple[str, str]]) -> list[str]:
    """Return labels for commit messages that do not contain a valid sign-off trailer."""
    return [label for label, message in messages if not has_valid_signoff(message)]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python governance/check_dco.py <commit-message-file> [...]", file=sys.stderr)
        return 2

    messages: list[tuple[str, str]] = []
    for raw_path in argv[1:]:
        path = Path(raw_path)
        messages.append((str(path), path.read_text(encoding="utf-8")))

    failures = check_messages(messages)
    if failures:
        for label in failures:
            print(f"FAIL {label}: missing valid Signed-off-by trailer")
        return 1

    for label, _ in messages:
        print(f"PASS {label}: DCO sign-off present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
