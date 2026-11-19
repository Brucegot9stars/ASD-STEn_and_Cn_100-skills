#!/usr/bin/env python3
"""install.py 的单元测试。运行：python -m unittest discover -s tests"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.py"

spec = importlib.util.spec_from_file_location("install_en", INSTALL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BEGIN = "<!-- ste-en:begin -->"
END = "<!-- ste-en:end -->"


class InstallEnTest(unittest.TestCase):
    def snippet(self):
        return (ROOT / "adapters" / "codex-AGENTS.md").read_text(encoding="utf-8").strip()

    def test_codex_append_fragment(self):
        """codex 目录无 AGENTS.md 时，追加带标记的片段。"""
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)
            with contextlib.redirect_stdout(io.StringIO()):
                mod.install_codex(dest, dry=False, force=False)
            agents = dest / "AGENTS.md"
            self.assertTrue(agents.is_file())
            text = agents.read_text(encoding="utf-8")
            self.assertIn(BEGIN, text)
            self.assertIn(END, text)
            self.assertIn(self.snippet(), text)

    def test_codex_idempotent(self):
        """重复执行不产生第二份标记片段。"""
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)
            with contextlib.redirect_stdout(io.StringIO()):
                mod.install_codex(dest, False, False)
                mod.install_codex(dest, False, False)
            text = (dest / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(text.count(BEGIN), 1)
            self.assertEqual(text.count(END), 1)

    def test_codex_dry_run_writes_nothing(self):
        """--dry-run 只打印计划。不创建文件。"""
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mod.install_codex(dest, dry=True, force=False)
            self.assertFalse((dest / "AGENTS.md").exists())
            self.assertIn("将", buf.getvalue())

    def test_codex_force_and_notice(self):
        """无标记文件存在时。--force 抑制追加提示。"""
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            for d in (d1, d2):
                (Path(d) / "AGENTS.md").write_text("原文保留。\n", encoding="utf-8")
            out1 = io.StringIO()
            with contextlib.redirect_stdout(out1):
                mod.install_codex(Path(d1), False, False)
            self.assertIn("注意", out1.getvalue())
            text1 = (Path(d1) / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("原文保留", text1)
            self.assertIn(BEGIN, text1)
            out2 = io.StringIO()
            with contextlib.redirect_stdout(out2):
                mod.install_codex(Path(d2), False, True)
            self.assertNotIn("注意", out2.getvalue())

    def test_dir_install_uses_dest(self):
        """--target dir --dest 把技能装到指定目录。"""
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)
            with contextlib.redirect_stdout(io.StringIO()):
                mod.install_skill(dest, dry=False, force=False)
            installed = dest / mod.SKILL_NAME
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertTrue((installed / "scripts" / "check_en.py").is_file())

    def test_dir_install_dry_run_and_force(self):
        """目录安装支持 --dry-run 与 --force。"""
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d)
            with contextlib.redirect_stdout(io.StringIO()):
                mod.install_skill(dest, dry=True, force=False)
            self.assertFalse((dest / mod.SKILL_NAME).exists())
            with contextlib.redirect_stdout(io.StringIO()):
                mod.install_skill(dest, False, False)
                mod.install_skill(dest, False, True)
            self.assertTrue((dest / mod.SKILL_NAME / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
