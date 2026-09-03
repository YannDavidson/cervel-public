from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

CHECKER_PATH = Path(__file__).resolve().parents[1] / "check_dco.py"
SPEC = importlib.util.spec_from_file_location("check_dco", CHECKER_PATH)
assert SPEC and SPEC.loader
check_dco = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_dco)


class DCOCheckerTests(unittest.TestCase):
    def test_accepts_standard_signoff(self) -> None:
        message = "Add example\n\nSigned-off-by: Ada Developer <ada@example.com>\n"
        self.assertTrue(check_dco.has_valid_signoff(message))

    def test_accepts_signoff_with_other_trailers(self) -> None:
        message = (
            "Improve docs\n\n"
            "Co-authored-by: Reviewer <reviewer@example.com>\n"
            "Signed-off-by: Ada Developer <ada@example.com>\n"
        )
        self.assertTrue(check_dco.has_valid_signoff(message))

    def test_rejects_missing_signoff(self) -> None:
        self.assertFalse(check_dco.has_valid_signoff("Add example\n"))

    def test_rejects_missing_email(self) -> None:
        self.assertFalse(check_dco.has_valid_signoff("Signed-off-by: Ada Developer\n"))

    def test_rejects_malformed_email_form(self) -> None:
        self.assertFalse(check_dco.has_valid_signoff("Signed-off-by: Ada Developer <ada example.com>\n"))

    def test_reports_only_unsigned_messages(self) -> None:
        failures = check_dco.check_messages(
            [
                ("signed", "Change\n\nSigned-off-by: Ada Developer <ada@example.com>\n"),
                ("unsigned", "Change without trailer\n"),
            ]
        )
        self.assertEqual(["unsigned"], failures)


if __name__ == "__main__":
    unittest.main()
