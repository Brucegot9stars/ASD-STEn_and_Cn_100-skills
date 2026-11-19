#!/usr/bin/env python3
"""check_zh.py — 受控中文技术文档机械检查（零依赖，Python 3.9+）

用法:
    python check_zh.py 文档.md [更多文件]
        --strict            存在【必须】级发现时退出码为 1
        --json              输出 JSON
        --kind 操作|描述     强制按一种句型检查句长（默认自动判断）
        --max-op 30         操作句字数上限
        --max-desc 40       描述句字数上限
        --no-vocab          跳过词表检查

只查句法层面：句长、禁用词、名词化、并联词、被动、句末条件、分号、
端点歧义、相对日期、双重否定。查不出事实错误、术语是否选对、顺序是否合理、
定语是否清楚、指代是否明确——这些必须人工判断。
所有发现都要人工确认，脚本会有误报。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- 词表（内置）

BANNED = [
    # (规则号, 级别, 正则, 说明)
    ("1.1", "必须", r"登陆", "「登陆」是错别字，写「登录」"),
    ("1.1", "必须", r"帐号|帐户", "写「账号」「账户」"),
    ("1.1", "必须", r"其它", "写「其他」"),
    ("1.1", "必须", r"按装", "写「安装」"),
    ("1.1", "必须", r"布署", "写「部署」"),
    ("1.1", "必须", r"做为", "写「作为」"),
    ("1.1", "必须", r"既使", "写「即使」"),
    ("1.1", "必须", r"以经", "写「已经」"),
    ("1.1", "必须", r"重起", "写「重启」"),
    ("1.3", "必须",
     r"(进行|加以|予以|作出|给予|实施|开展)[^，。；：]{0,4}"
     r"(处理|检查|修改|调整|分析|优化|操作|维护|管理|升级|配置|确认|验证|统计|评估|测试|响应|部署)",
     "名词化：「进行/加以/予以 + 动词」改为直接用动词"),
    ("1.4", "必须",
     r"值得注意的是|综上所述|众所周知|不难看出|显而易见|总的来说|总体而言|"
     r"在一定程度上|在某种意义上",
     "空转词：删除，直接给事实"),
    ("1.5", "必须", r"尽快|必要时|酌情|视情况|适当地|适当|尽量", "模糊词：改成可执行的条件、时限或数值"),
    ("1.5", "建议", r"及时", "「及时」无判据：写「在 N 秒内」"),
    ("1.5", "建议", r"大概|大约|左右|若干|等等", "估计词：给出数值或范围"),
    ("7.4", "建议", r"请注意|务必注意|小心操作", "空提示：写具体防护动作"),
    ("1.6", "建议", r"赋能|抓手|闭环|打通|拉齐|丝滑|兜底|全链路", "黑话：改写成具体动作和对象"),
    ("2.3", "建议", r"相关的|有关的|相应的", "虚指修饰：写出具体对象"),
    ("4.4", "建议", r"然后|接着|随后|之后", "串联词：拆成编号步骤"),
    ("4.4", "建议", r"与此同时", "串联词：拆成编号步骤或明确「同时」"),
    ("4.5", "必须", r"并且", "并列堆叠：拆句或改列表"),
    ("4.5", "建议", r"以及", "并列堆叠：拆句或改列表"),
    ("1.7", "建议", r"应当|务必|(?<!必)须", "情态不统一：统一用「必须 / 可以 / 建议」"),
    ("4.6", "必须", r"不得不|不能不|未必不|不得(?:不|没)|没有一个不", "双重否定：改成肯定句"),
    ("4.6", "建议", r"[！!]", "技术文本不用感叹号"),
    ("4.6", "建议", r"[？?]", "技术文本不用问句"),
    ("8.1", "必须",
     r"\d+\s*(?:%|°C|℃|[A-Za-z]+|个|字|位|天|小时|分钟|秒|次|年|月|米|毫米|厘米|千克|公斤|克)?\s*(?:以上|以下)",
     "「以上/以下」端点歧义：写「不小于 / 大于 / 不超过 / 小于」"),
    ("8.2", "建议", r"\d+\s*[~～]\s*\d+", "范围写「A 至 B」，不用 ~"),
    ("8.4", "建议", r"昨天|今天|明天|上周|下周|上个月|下个月|前几天|近日|最近", "相对时间：写绝对日期"),
    ("9.1", "必须", r"；", "不用分号：拆句或改列表"),
]

# 操作句里额外检查（只对编号步骤生效）
STEP_CHECKS = [
    ("3.1", "建议", r"请(?:您)?|用户需要|用户应|我们需要", "步骤不用「请/您/用户需要」，动词开头"),
    ("3.2", "必须", r"被", "步骤不用「被」字句，改主动句"),
    ("3.5", "建议", r"(?:处理|检查|优化|操作|确认|调整)(?:一下|好|完)", "动作写全：动词 + 对象 + 结果"),
]

SENT_END = re.compile(r"[。！？!?]")
STEP_RE = re.compile(r"^(\s*)(?:(\d+(?:\.\d+)*)[.、)）]|\[[ xX]\]\s)")
HEADING_RE = re.compile(r"^\s*#{1,6}\s")
TABLE_RE = re.compile(r"^\s*\|")
SKIP_PREFIX = ("不批准", "反例", "改写前", "✗", "❌")
PUNCT_RE = re.compile(r"[\s，。；：、！？,.;:!?（）()\[\]「」『』“”‘’\"'《》〈〉—…·/\\|]")


def char_count(text: str) -> int:
    """汉字按字计，连续的英文/数字/标识符按 1 个词计（与「10 °C 算一个词」一致）。"""
    body = PUNCT_RE.sub("", text)
    cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
    latin = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9._\-/%]*", body))
    return cjk + latin


def clean_line(line: str) -> str:
    """去掉 HTML 注释、行内代码、引号内界面文字，避免误报。"""
    line = re.sub(r"<!--.*?-->", "", line)
    line = re.sub(r"`[^`]*`", "CODE", line)
    line = re.sub(r"「[^」]*」", "UI", line)
    return line


def is_other_language(line: str, target: str) -> bool:
    """默认跳过非目标语言主导的行，便于中英混合文档分别跑两个检查脚本。"""
    cjk = len(re.findall(r"[\u4e00-\u9fff]", line))
    words = len(re.findall(r"[A-Za-z]{2,}", line))
    if target == "zh":
        return cjk == 0 and words > 0
    return cjk >= 3 and cjk >= words


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
        if para_sent > 5 and para_lines:
            findings.append(Finding(para_lines[0], "6.1", "建议",
                                    f"段落 {para_sent} 句，不超过 5 句"))
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

        if not line.strip() or HEADING_RE.match(line) or TABLE_RE.match(line):
            flush_para()
            continue
        stripped = re.sub(r"^\s*(?:[-*+]\s+|\d+[.、)）]\s*|>\s*)?", "", line)
        if stripped.startswith(SKIP_PREFIX) or "✗" in line or "❌" in line:
            flush_para()
            continue
        if not args.no_lang_skip and is_other_language(line, "zh"):
            flush_para()
            continue

        text = clean_line(line)
        step = STEP_RE.match(text)

        # --- 词表类检查
        if not args.no_vocab:
            for rule, level, pattern, msg in BANNED:
                if re.search(pattern, text):
                    findings.append(Finding(lineno, rule, level, msg))
        if step:
            body = text[step.end():]
            for rule, level, pattern, msg in STEP_CHECKS:
                if re.search(pattern, body):
                    findings.append(Finding(lineno, rule, level, msg))
            # 条件在句尾
            if re.search(r"[，,]\s*(?:如果|若|当|在)[^。]{0,25}(?:时|的话)?\s*。?$", body):
                findings.append(Finding(lineno, "4.3", "必须", "条件在句尾：把条件写到动作前面"))
            # 开放列举
            if re.search(r"等\s*[。；，]?\s*$", body):
                findings.append(Finding(lineno, "8.3", "建议", "开放列举「等」：列全或写「包括 A、B、C」"))
            if args.kind in (None, "操作"):
                n = char_count(body)
                if n > args.max_op:
                    findings.append(Finding(lineno, "4.1", "必须",
                                            f"操作句 {n} 字，不超过 {args.max_op} 字"))
            para_lines, para_sent = [], 0
            continue

        # --- 描述句句长
        sents = [s for s in SENT_END.split(text) if char_count(s) > 0]
        if args.kind in (None, "描述"):
            for s in sents:
                n = char_count(s)
                if n > args.max_desc:
                    findings.append(Finding(lineno, "4.1", "必须",
                                            f"描述句 {n} 字，不超过 {args.max_desc} 字"))
        if args.kind in (None, "描述"):
            if re.search(r"等\s*[。；]?\s*$", text):
                findings.append(Finding(lineno, "8.3", "建议", "开放列举「等」：列全或写「包括 A、B、C」"))
            # 无序列表项各自成段，不合并计句数
            if re.match(r"^\s*[-*+]\s", line):
                flush_para()
            else:
                if not para_lines:
                    para_lines = [lineno]
                para_sent += max(len(sents), 1)

    flush_para()
    return dedupe(findings)


def dedupe(findings: list) -> list:
    """同一行同一规则只留一条，保留更高级别。"""
    best = {}
    for f in findings:
        key = (f.line, f.rule)
        cur = best.get(key)
        if cur is None or (cur.level == "建议" and f.level == "必须"):
            best[key] = f
    return sorted(best.values(), key=lambda x: (x.line, x.rule))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="受控中文技术文档机械检查")
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--strict", action="store_true", help="存在【必须】级发现时退出码为 1")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--kind", choices=["操作", "描述"], default=None)
    ap.add_argument("--max-op", type=int, default=30)
    ap.add_argument("--max-desc", type=int, default=40)
    ap.add_argument("--no-vocab", action="store_true")
    ap.add_argument("--no-lang-skip", action="store_true",
                    help="不跳过纯英文行（默认跳过，便于双语文档分诊）")
    args = ap.parse_args(argv)

    total, must, report = 0, 0, {}
    for f in args.files:
        if not f.is_file():
            print(f"跳过（不是文件）：{f}", file=sys.stderr)
            continue
        fs = check_file(f, args)
        fs.sort(key=lambda x: (x.line, x.rule))
        report[str(f)] = [x.as_dict() for x in fs]
        total += len(fs)
        must += sum(1 for x in fs if x.level == "必须")
        if not args.json:
            for x in fs:
                print(f"{f}:{x.line}: [{x.rule}][{x.level}] {x.msg}")

    if args.json:
        print(json.dumps({"total": total, "must": must, "files": report},
                         ensure_ascii=False, indent=2))
    else:
        print(f"\n合计 {total} 条，其中【必须】{must} 条；还有 {total - must} 条【建议】需人工判断。")
        print("脚本只查句法，事实与术语必须人工复核。")

    if args.strict and must:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
