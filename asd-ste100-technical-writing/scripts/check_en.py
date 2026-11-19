#!/usr/bin/env python3
"""check_en.py — ASD-STE100 风格英文技术文档机械检查（零依赖，Python 3.9+）

用法:
    python check_en.py 文档.md [更多文件]
        --strict               存在【必须】级发现时退出码为 1
        --json                 输出 JSON
        --kind procedure|description   强制按一种句型检查句长
        --max-proc 20          程序句词数上限
        --max-desc 25          描述句词数上限
        --no-vocab             跳过词表与语法形式检查
        --no-lang-skip        不跳过中文主导行（默认跳过，便于双语文档分诊）

对应 references/checklist.md 的 M1–M14 与 S 系列。
只查句法层面：查不出词典批准状态、词性、词义、名词簇关系、技术含义。
所有发现都要人工确认，脚本会有误报。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# (规则号, 级别, 正则, 说明, 是否属于词表/语法类)
PATTERNS = [
    ("M3", "必须", r";", "不用分号：拆成两句或改列表", False),
    ("M4", "必须", r"[—–]", "不用 em/en dash 连接独立意思：拆句（复合词连字符 - 不算）", False),
    ("M6", "必须",
     r"\b(?:has|have|had)\s+(?:\w+ed|been|done|made|set|put|given|taken|shown|found|got|gotten|written|built|sent|kept|left|held|brought|thought|known|grown|drawn|driven|broken|chosen|spoken|stolen|worn|torn|born)\b",
     "完成时：改成一般时态或祈使句", True),
    ("M7", "必须", r"\b(?:is|are|was|were|be|been|being)\s+\w+ing\b", "进行时：改成一般现在时", True),
    ("M8", "必须",
     r"\b(?:don't|doesn't|didn't|can't|won't|isn't|aren't|wasn't|weren't|it's|that's|we'll|you'll|they're|you're|shouldn't|couldn't|wouldn't)\b",
     "缩写形式：写完整形式（do not, cannot, it is）", True),
    ("M9", "必须", r"\b(?:e\.g\.|i\.e\.|etc\.)", "拉丁缩写：改成 for example / that is / and so on，或直接列举", True),
    ("M14", "建议", r"\b(?:he|she|his|her)\b", "性别代词：改用 the operator / the technician 或复数", True),
    ("J8", "建议", r"\b(?:may|might|could|should)\b", "模糊情态：用 must / can，或写成可检查的条件", True),
    ("J8", "建议", r"\b(?:approximately|roughly|essentially|most likely|it looks like|basically|probably)\b",
     "软化语：删除，或改成可检查的事实", True),
    ("S7", "建议", r"\b(?:EXTREME|CRITICAL|IMPERATIVE|dangerous|very|extremely)\b",
     "不可验证的强调词：删除，写具体后果", True),
]

# -ing 白名单：批准词、技术名词、常见非动词形式
ING_ALLOW = {
    "during", "warning", "opening", "remaining", "setting", "binding",
    "landing", "following", "existing", "according", "concerning",
    "including", "engineering", "training", "reading", "spring",
    "string", "thing", "ceiling", "building", "fitting", "meeting",
    "bearing", "clamping", "coupling", "housing", "piping", "wiring",
    "shielding", "marking", "packing", "shipping", "timing", "cooling",
    "heating", "lighting", "coating", "sealing", "mounting", "spacing",
}

# 程序句里额外检查
STEP_CHECKS = [
    ("M12", "建议", r"^(?:The|This|These|Those|You|It|We|They|All|A|An|If|When|Before|After|Users?|The operator|The technician|System)\b",
     "程序指令应以祈使动词开头"),
    ("J7", "必须", r"\b(?:must|should)\s+be\s+\w+ed\b", "程序不用被动情态：改成祈使句"),
    ("J6", "必须", r",?\s+(?:if|when|unless)\b[^.]*\.$", "条件在句尾：把条件写到动作前面"),
]

# NOTE 中不应出现指令
NOTE_IMPERATIVE = re.compile(r"\b(?:make sure|do|remove|install|disconnect|connect|check|set|open|close|press|ensure|use)\b", re.I)

SENT_END = re.compile(r"[.!?]")
STEP_RE = re.compile(r"^(\s*)(?:(\d+(?:\.\d+)*)[.)）]|\[[ xX]\]\s)")
HEADING_RE = re.compile(r"^\s*#{1,6}\s")
TABLE_RE = re.compile(r"^\s*\|")
QUOTE_RE = re.compile(r"^\s*>")
SKIP_PREFIX = ("✗", "❌", "Before", "**Before**", "不批准", "反例", "改写前", "Bad", "Wrong")

UNIT_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:°C|°F|in\.|ft|mm|cm|m|kg|g|lb|psi|kPa|MPa|Pa|N·m|Nm|V|A|W|kW|Hz|%|s|ms|min|h|hours?|minutes?|seconds?|degrees?\s+Celsius)\b",
    re.I,
)


def word_count(sentence: str) -> int:
    """数字 + 单位算一个词；行内代码按一个词计。"""
    text = re.sub(r"`[^`]*`", " CODE ", sentence)
    text = UNIT_RE.sub(" NUMUNIT ", text)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'./:_-]*", text))


def clean_line(line: str) -> str:
    line = re.sub(r"<!--.*?-->", "", line)
    line = re.sub(r"`[^`]*`", " CODE ", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    return line


def is_other_language(line: str, target: str) -> bool:
    """默认跳过非目标语言主导的行，便于双语文档分别跑两个脚本。"""
    cjk = len(re.findall(r"[\u4e00-\u9fff]", line))
    words = len(re.findall(r"[A-Za-z]{2,}", line))
    if target == "en":
        return cjk >= 3 and cjk >= words
    return cjk == 0 and words > 0


class Finding:
    __slots__ = ("line", "rule", "level", "msg")

    def __init__(self, line: int, rule: str, level: str, msg: str):
        self.line, self.rule, self.level, self.msg = line, rule, level, msg

    def as_dict(self):
        return {"line": self.line, "rule": self.rule, "level": self.level, "message": self.msg}


def check_file(path: Path, args) -> list:
    findings: list = []
    in_code = in_front = in_comment = False
    para_lines: list = []
    para_sent = 0

    def flush_para():
        nonlocal para_lines, para_sent
        if para_sent > 6 and para_lines:
            findings.append(Finding(para_lines[0], "M11", "建议",
                                    f"段落 {para_sent} 句，不超过 6 句"))
        para_lines, para_sent = [], 0

    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            in_code = not in_code
            flush_para()
            continue
        if in_code:
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if line.lstrip().startswith("<!--") and "-->" not in line:
            in_comment = True
            flush_para()
            continue
        if lineno == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
            continue
        if (not line.strip() or HEADING_RE.match(line) or TABLE_RE.match(line)
                or QUOTE_RE.match(line)):
            flush_para()
            continue
        stripped = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)）]\s*|>\s*)?", "", line)
        if stripped.startswith(SKIP_PREFIX) or "✗" in line or "❌" in line:
            flush_para()
            continue
        if not args.no_lang_skip and is_other_language(line, "en"):
            flush_para()
            continue

        text = clean_line(line)
        step = STEP_RE.match(text)

        # M5：-ing 动词（排除白名单）
        if not args.no_vocab:
            for m in re.finditer(r"\b([A-Za-z]+ing)\b", text):
                if m.group(1).lower() not in ING_ALLOW:
                    findings.append(Finding(lineno, "M5", "建议",
                                            f"-ing 形式 `{m.group(1)}`：确认是技术名词，不是动词"))
                    break
        for rule, level, pattern, msg, is_vocab in PATTERNS:
            if args.no_vocab and is_vocab:
                continue
            flags = re.I if rule in ("M8", "M9", "M14", "J8", "S7") else 0
            if re.search(pattern, text, flags):
                findings.append(Finding(lineno, rule, level, msg))

        # NOTE 不得含指令
        if re.match(r"^\s*NOTE\s*:", text, re.I) and NOTE_IMPERATIVE.search(text.split(":", 1)[-1]):
            findings.append(Finding(lineno, "S5", "必须", "NOTE 含操作指令：把指令移到步骤里"))

        if step:
            body = text[step.end():]
            for rule, level, pattern, msg in STEP_CHECKS:
                if re.search(pattern, body, re.I if rule == "M12" else 0):
                    findings.append(Finding(lineno, rule, level, msg))
            if args.kind in (None, "procedure"):
                n = word_count(body)
                if n > args.max_proc:
                    findings.append(Finding(lineno, "M1", "必须",
                                            f"程序句 {n} 词，不超过 {args.max_proc} 词"))
            flush_para()
            continue

        sents = [s for s in SENT_END.split(text) if word_count(s) > 0]
        if args.kind in (None, "description"):
            for s in sents:
                n = word_count(s)
                if n > args.max_desc:
                    findings.append(Finding(lineno, "M2", "必须",
                                            f"描述句 {n} 词，不超过 {args.max_desc} 词"))
        if args.kind in (None, "description"):
            if re.match(r"^\s*[-*+]\s", line):
                flush_para()
            else:
                if not para_lines:
                    para_lines = [lineno]
                para_sent += max(len(sents), 1)

    flush_para()
    return dedupe(findings)


def dedupe(findings: list) -> list:
    best = {}
    for f in findings:
        key = (f.line, f.rule)
        cur = best.get(key)
        if cur is None or (cur.level == "建议" and f.level == "必须"):
            best[key] = f
    return sorted(best.values(), key=lambda x: (x.line, x.rule))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="ASD-STE100 风格英文技术文档机械检查")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--kind", choices=["procedure", "description"], default=None)
    ap.add_argument("--max-proc", type=int, default=20)
    ap.add_argument("--max-desc", type=int, default=25)
    ap.add_argument("--no-vocab", action="store_true")
    ap.add_argument("--no-lang-skip", action="store_true")
    args = ap.parse_args(argv)

    total, must, report = 0, 0, {}
    valid = 0
    for f in args.files:
        if not f.is_file():
            print(f"跳过（不是文件）：{f}", file=sys.stderr)
            continue
        valid += 1
        fs = check_file(f, args)
        fs.sort(key=lambda x: (x.line, x.rule))
        report[str(f)] = [x.as_dict() for x in fs]
        total += len(fs)
        must += sum(1 for x in fs if x.level == "必须")
        if not args.json:
            for x in fs:
                print(f"{f}:{x.line}: [{x.rule}][{x.level}] {x.msg}")

    if valid == 0:
        print("错误：没有可检查的有效文件。", file=sys.stderr)
        if args.json:
            print(json.dumps({"error": "no_valid_files", "total": 0,
                              "must": 0, "files": {}}, ensure_ascii=False, indent=2))
        return 2

    if args.json:
        print(json.dumps({"total": total, "must": must, "files": report},
                         ensure_ascii=False, indent=2))
    else:
        print(f"\n合计 {total} 条，其中【必须】{must} 条；还有 {total - must} 条【建议】需人工判断。")
        print("脚本只查句法，词典批准状态与术语必须人工复核。")

    return 1 if args.strict and must else 0


if __name__ == "__main__":
    raise SystemExit(main())
