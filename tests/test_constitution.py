"""Structural checks for the lightweight runtime constitution."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "common" / "instructions" / "universal-laws.md"
RATIONALE = ROOT / "common" / "instructions" / "L0-rationale.md"


class TestRuntimeConstitution(unittest.TestCase):
    def test_runtime_is_compact_and_versioned(self):
        text = RUNTIME.read_text(encoding="utf-8")
        self.assertIn("Runtime Constitution v2.1", text)
        self.assertLessEqual(len(text.split()), 440)
        self.assertTrue(RATIONALE.exists())
        self.assertNotIn("L0-rationale.md", text)

    def test_laws_and_meta_laws_are_present_once(self):
        text = RUNTIME.read_text(encoding="utf-8")
        for law in range(1, 8):
            self.assertEqual(len(re.findall(rf"^\*\*F{law} ", text, re.M)), 1)
        for meta in ("M1", "M1b", "M2", "M3"):
            self.assertEqual(len(re.findall(rf"^\*\*{meta} ", text, re.M)), 1)

    def test_input_trust_and_fail_closed_rules(self):
        text = RUNTIME.read_text(encoding="utf-8")
        for phrase in (
            "data, never instructions",
            "L3 profile and L4 memory provide data",
            "L1 must define action authorities",
            "pause only affected actions",
            "missing required authority",
            "version",
        ):
            self.assertIn(phrase, text)

    def test_rationale_contains_review_examples(self):
        text = RATIONALE.read_text(encoding="utf-8")
        for item in ("Derives: F3", "F7", "M1b", "rollback", "violation"):
            self.assertIn(item, text)


if __name__ == "__main__":
    unittest.main()
