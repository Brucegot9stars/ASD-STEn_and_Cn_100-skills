#!/usr/bin/env python3
"""check_en.py 的单元测试。运行：python -m unittest discover -s tests"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK = ROOT / "scripts" / "check_en.py"

spec = importlib.util.spec_from_file_location("check_en", CHECK)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def run(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(CHECK), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )


class CheckEnTest(unittest.TestCase):
    def test_after_passes_strict(self):
        p = run("--strict", ROOT / "examples" / "after.md")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("【必须】0 条", p.stdout)

    def test_before_flags_known_problems(self):
        out = run(ROOT / "examples" / "before.md").stdout
        for rule in ("M3", "M6", "M8", "M9", "S5"):
            self.assertIn(f"[{rule}][必须]", out, f"未检出 {rule}")

    def test_strict_exit_code_is_one(self):
        self.assertEqual(run("--strict", ROOT / "examples" / "before.md").returncode, 1)

    def test_json_shape(self):
        data = json.loads(run("--json", ROOT / "examples" / "before.md").stdout)
        self.assertGreaterEqual(data["must"], 1)
        self.assertEqual(data["total"], sum(len(v) for v in data["files"].values()))

    def test_number_plus_unit_is_one_word(self):
        """Issue 9：10 °C 算一个词。"""
        self.assertLessEqual(mod.word_count("Set the temperature to 10 °C."), 6)

    def test_ing_allowlist(self):
        self.assertIn("bearing", mod.ING_ALLOW)
        self.assertIn("during", mod.ING_ALLOW)
        self.assertNotIn("carrying", mod.ING_ALLOW)

    def test_language_detection(self):
        self.assertTrue(mod.is_other_language("拆下盖板并检查密封圈。", "en"))
        self.assertFalse(mod.is_other_language("Remove the cover.", "en"))
        self.assertTrue(mod.is_other_language("Remove the cover.", "zh"))
        self.assertFalse(mod.is_other_language("拆下盖板。", "zh"))

    def test_mixed_file_has_no_false_positives(self):
        """双语文档里，中文行默认跳过，不产生误报。"""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "mixed.md"
            p.write_text("拆下盖板并检查密封圈。\nRemove the cover.\n", encoding="utf-8")
            data = json.loads(run("--json", p).stdout)
            self.assertEqual(data["total"], 0)


if __name__ == "__main__":
    unittest.main()
