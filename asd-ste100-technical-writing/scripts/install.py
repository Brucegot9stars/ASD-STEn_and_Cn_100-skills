#!/usr/bin/env python3
"""install.py — 把本 skill 安装到各 agent 的技能目录，或生成 AGENTS.md 片段。

用法:
    python scripts/install.py --target claude
    python scripts/install.py --target claude --project
    python scripts/install.py --target workbuddy
    python scripts/install.py --target workbuddy --project
    python scripts/install.py --target codex          # 当前目录写 AGENTS.md 片段
    python scripts/install.py --target dir --dest D:/skills

参数:
    --target claude|workbuddy|codex|dir
    --project    项目级安装（写入当前目录），默认用户级
    --dest PATH  目标目录（--target dir 必填，其他用于覆盖默认位置）
    --dry-run    只打印计划，不写文件
    --force      覆盖已存在的目标目录

--target codex 固定写当前目录的 AGENTS.md 片段，不需要 --dest 或 --project。

只安装运行所需文件：SKILL.md、references/、examples/、scripts/check_en.py。
tests/、adapters/、dist/、docs/ 不进入技能目录。
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "asd-ste100-technical-writing"
COPY_ITEMS = ("SKILL.md", "references", "examples", "scripts/check_en.py")
AGENTS_BEGIN = "<!-- ste-en:begin -->"
AGENTS_END = "<!-- ste-en:end -->"

USER_DIRS = {
    "claude": Path.home() / ".claude" / "skills",
    "workbuddy": Path.home() / ".workbuddy" / "skills",
}
PROJECT_DIRS = {
    "claude": Path.cwd() / ".claude" / "skills",
    "workbuddy": Path.cwd() / ".workbuddy" / "skills",
}


def plan_target(args) -> Path:
    if args.target == "codex":
        return Path.cwd()
    if args.target == "dir":
        if not args.dest:
            sys.exit("--target dir 需要 --dest")
        return Path(args.dest).expanduser().resolve()
    if args.dest:
        return Path(args.dest).expanduser().resolve()
    table = PROJECT_DIRS if args.project else USER_DIRS
    if args.target not in table:
        sys.exit(f"--target {args.target} 不支持目录安装，请用 --dest")
    return table[args.target].resolve()


def install_skill(dest_root: Path, dry: bool, force: bool) -> None:
    dest = dest_root / SKILL_NAME
    print(f"安装到：{dest}")
    if dest.exists() and not force:
        sys.exit(f"目标已存在：{dest}\n加 --force 覆盖，或先删除。")
    if dry:
        for item in COPY_ITEMS:
            print(f"  将写入 {item}")
        return
    dest.mkdir(parents=True, exist_ok=True)
    for item in COPY_ITEMS:
        src = ROOT / item
        target = dest / item
        if src.is_dir():
            shutil.copytree(src, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
        print(f"  + {item}")
    print(f"完成。验证：python {dest / 'scripts' / 'check_en.py'} --strict {dest / 'examples' / 'after.md'}")


def install_codex(dest_root: Path, dry: bool, force: bool) -> None:
    snippet = (ROOT / "adapters" / "codex-AGENTS.md").read_text(encoding="utf-8").strip()
    target = dest_root / "AGENTS.md"
    print(f"写入 AGENTS.md：{target}")
    old = target.read_text(encoding="utf-8") if target.exists() else ""
    if AGENTS_BEGIN in old and AGENTS_END in old:
        head, rest = old.split(AGENTS_BEGIN, 1)
        _, tail = rest.split(AGENTS_END, 1)
        new = head + snippet + tail
        action = "替换已有片段"
    else:
        new = (old.rstrip() + "\n\n" + snippet + "\n") if old.strip() else snippet + "\n"
        action = "追加片段"
    if dry:
        print(f"  将{action}（{len(snippet)} 字节）")
        return
    if target.exists() and not force and AGENTS_BEGIN not in old:
        print("  注意：AGENTS.md 已存在且无标记，将追加在末尾（原文保留）。")
    target.write_text(new, encoding="utf-8")
    print(f"  {action}完成。片段以 {AGENTS_BEGIN} / {AGENTS_END} 包裹，可重复执行。")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="安装 ASD-STE100 英文技术写作 skill")
    ap.add_argument("--target", required=True, choices=["claude", "workbuddy", "codex", "dir"])
    ap.add_argument("--project", action="store_true", help="项目级安装（写入当前目录）")
    ap.add_argument("--dest", help="自定义目标目录")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)

    dest = plan_target(args)
    if args.target == "codex":
        install_codex(dest, args.dry_run, args.force)
    else:
        install_skill(dest, args.dry_run, args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
