#!/usr/bin/env python3
"""check_zh.py 的单元测试。运行：python -m unittest discover -s tests"""

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
CHECK = ROOT / "scripts" / "check_zh.py"

spec = importlib.util.spec_from_file_location("check_zh", CHECK)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def run(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run(
        [sys.executable, str(CHECK), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )


class CheckZhTest(unittest.TestCase):
    def test_after_passes_strict(self):
        """正例必须 0 条【必须】级发现，且退出码为 0。"""
        p = run("--strict", ROOT / "examples" / "after.md")
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("【必须】0 条", p.stdout)

    def test_before_flags_known_problems(self):
        """反例必须命中已埋的三类问题。"""
        out = run(ROOT / "examples" / "before.md").stdout
        self.assertIn("[1.1][必须]", out, "未检出「登陆」")
        self.assertIn("[4.1][必须]", out, "未检出超长句")
        self.assertIn("[9.1][必须]", out, "未检出分号")

    def test_strict_exit_code_is_one(self):
        p = run("--strict", ROOT / "examples" / "before.md")
        self.assertEqual(p.returncode, 1)

    def test_json_shape(self):
        p = run("--json", ROOT / "examples" / "before.md")
        data = json.loads(p.stdout)
        self.assertGreaterEqual(data["must"], 1)
        self.assertEqual(data["total"], sum(len(v) for v in data["files"].values()))

    def test_skill_docs_have_no_must(self):
        """规则文档自身必须通过【必须】级检查。"""
        files = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
        p = run("--json", *files)
        data = json.loads(p.stdout)
        self.assertEqual(data["must"], 0, p.stdout)

    def test_language_detection(self):
        """中文脚本跳过纯英文行，英文脚本跳过中文主导行。"""
        self.assertTrue(mod.is_other_language("Remove the cover.", "zh"))
        self.assertFalse(mod.is_other_language("拆下盖板并检查密封圈。", "zh"))
        self.assertTrue(mod.is_other_language("拆下盖板并检查密封圈。", "en"))
        self.assertFalse(mod.is_other_language("Remove the cover.", "en"))

    def test_mixed_file_has_no_false_positives(self):
        """双语文档里，纯英文行默认跳过，不产生误报。"""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "mixed.md"
            p.write_text("Remove the cover.\n拆下盖板并检查密封圈。\n", encoding="utf-8")
            data = json.loads(run("--json", p).stdout)
            self.assertEqual(data["total"], 0)

    def test_skip_code_and_quotes(self):
        """代码块与「」内的界面文字不应触发词表。"""
        p = run("--json", ROOT / "examples" / "after.md")
        data = json.loads(p.stdout)
        self.assertEqual(data["total"], 0)


if __name__ == "__main__":
    unittest.main()
