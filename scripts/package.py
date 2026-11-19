#!/usr/bin/env python3
"""把两个 skill 与整个源码树打成 zip，供 GitHub Release 上传。零依赖。"""
from __future__ import annotations

import argparse
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("asd-ste100-technical-writing", "ste-zh-technical-writing")
SKIP_DIRS = {"__pycache__", ".idea", ".vscode"}
SKIP_SUFFIXES = (".pyc", ".pyo", ".pyd")


def collect(base: Path, root_exclude: set[str]):
    """产出 (磁盘路径, 归档内相对路径)。root_exclude 只作用于顶层。"""
    for path in sorted(base.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(base)
        if rel.parts[0] in root_exclude:
            continue
        if any(part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        if path.suffix in SKIP_SUFFIXES:
            continue
        yield path, rel


def make_zip(out: Path, base: Path, arcroot: str, root_exclude: set[str]) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, rel in collect(base, root_exclude):
            archive.write(path, f"{arcroot}/{rel.as_posix()}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", default=os.environ.get("GITHUB_REF_NAME", "dev"),
                        help="版本标签，默认取 GITHUB_REF_NAME，否则 dev")
    parser.add_argument("--out", default="dist", help="输出目录，默认 dist")
    args = parser.parse_args()

    tag = args.tag.strip() or "dev"
    out = ROOT / args.out
    products = []

    for name in SKILLS:
        target = out / f"{name}-{tag}.zip"
        products.append(make_zip(target, ROOT / name, name, set()))

    source_name = f"ste-writing-skills-{tag}"
    source = out / f"{source_name}-source.zip"
    products.append(make_zip(source, ROOT, source_name, {".git", ".workbuddy", "dist"}))

    for product in products:
        size = product.stat().st_size
        print(f"{product.relative_to(ROOT)}  ({size} bytes)")


if __name__ == "__main__":
    main()
