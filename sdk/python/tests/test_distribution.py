from __future__ import annotations

import tarfile
import unittest
import zipfile
from pathlib import Path

SDK_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = SDK_ROOT / "dist"
EXPECTED_VERSION = "0.1.0a0"


class DistributionIntegrityTests(unittest.TestCase):
    def test_single_wheel_and_sdist_exist(self) -> None:
        self.assertEqual(1, len(list(DIST_DIR.glob("*.whl"))))
        self.assertEqual(1, len(list(DIST_DIR.glob("*.tar.gz"))))

    def test_wheel_contains_only_public_sdk_package_metadata_and_license(self) -> None:
        wheel = next(DIST_DIR.glob("*.whl"))
        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
            self.assertIn("cervel_public/__init__.py", names)
            self.assertIn("cervel_public/models.py", names)
            self.assertTrue(any(name.endswith(".dist-info/licenses/LICENSE") for name in names))
            self.assertFalse(any("/tests/" in name or name.startswith("tests/") for name in names))
            self.assertFalse(any(name.startswith("schemas/") for name in names))
            self.assertFalse(any(name.startswith("conformance/") for name in names))
            self.assertFalse(any(name.startswith(".github/") for name in names))

            metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
            metadata = archive.read(metadata_name).decode("utf-8")
            self.assertIn("Name: cervel-public", metadata)
            self.assertIn(f"Version: {EXPECTED_VERSION}", metadata)
            self.assertIn("Requires-Python: >=3.10", metadata)
            self.assertIn("License-Expression: Apache-2.0", metadata)
            self.assertIn("License-File: LICENSE", metadata)

    def test_sdist_contains_minimal_public_release_source(self) -> None:
        sdist = next(DIST_DIR.glob("*.tar.gz"))
        with tarfile.open(sdist, "r:gz") as archive:
            names = archive.getnames()
            self.assertTrue(any(name.endswith("/pyproject.toml") for name in names))
            self.assertTrue(any(name.endswith("/README.md") for name in names))
            self.assertTrue(any(name.endswith("/LICENSE") for name in names))
            self.assertTrue(any(name.endswith("/cervel_public/__init__.py") for name in names))
            self.assertTrue(any(name.endswith("/cervel_public/models.py") for name in names))
            self.assertFalse(any("/tests/" in name for name in names))
            self.assertFalse(any("/.github/" in name for name in names))
            self.assertFalse(any("/schemas/" in name for name in names))
            self.assertFalse(any("/conformance/" in name for name in names))


if __name__ == "__main__":
    unittest.main()
