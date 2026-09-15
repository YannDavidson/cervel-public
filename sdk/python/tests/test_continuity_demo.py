from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
DEMO = ROOT / "examples" / "python" / "model_replacement_continuity.py"

spec = importlib.util.spec_from_file_location("model_replacement_continuity", DEMO)
assert spec is not None and spec.loader is not None
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class ContinuityDemoTests(unittest.TestCase):
    def test_snapshot_is_stable_for_same_public_lookup_items(self) -> None:
        items = (
            SimpleNamespace(
                reference=SimpleNamespace(id="local-000001", source="continuity-demo"),
                text="Project Atlas knowledge",
            ),
        )
        before = demo.snapshot(items)
        after = demo.snapshot(items)
        self.assertEqual(before, after)
        self.assertEqual(
            (("local-000001", "continuity-demo", "Project Atlas knowledge"),),
            before,
        )

    def test_demo_source_states_same_process_boundary(self) -> None:
        source = DEMO.read_text(encoding="utf-8")
        self.assertIn("same sandbox process remains running", source)
        self.assertIn("does not claim persistence across restarts", source)
        self.assertIn("--send-context-to-cloud", source)


if __name__ == "__main__":
    unittest.main()
