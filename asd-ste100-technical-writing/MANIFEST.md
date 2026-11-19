# 文件清单

共 21 个文件。每个文件的作用、行数与依赖关系如下。配套项目 `ste-zh-technical-writing` 有同规格结构，两者规则集不合并。

## 入口

| 文件 | 行数 | 作用 |
|---|---|---|
| `SKILL.md` | 266 | Agent Skills 入口。frontmatter（`name` / `description`）+ 用途、触发条件（含 2.3 中英混合文本）、适用任务、9 节规则要点、执行流程、输出约束、检查清单、边界。Claude Code、WorkBuddy 直接读它。 |
| `AGENTS.md` | 86 | 通用 agent 入口。Codex、opencode 及自建 agent 读它。含启用条件、文件索引、硬约束摘要、流程、输出契约。 |
| `README.md` | 241 | 给人看的项目说明。用途、两个 skill 的分工、适用场景、目录结构、安装、各 agent 适配、用法、示例、边界、维护、许可。 |
| `dist/ste-en.prompt.md` | 128 | 单文件压缩版。34 条硬规则 + 常见替换表 + 输出格式 + 自检清单。供无 skill 机制的 agent（如 Hermes）直接粘进系统提示。 |
| `MANIFEST.md` | — | 本文件。 |
| `CHANGELOG.md` | 30 | 版本记录。 |

## 规则与词表

| 文件 | 行数 | 作用 |
|---|---|---|
| `references/writing-rules.md` | 196 | 核心。53 条规则按 9 节的执行摘要，含高频规则示例、4 个完整改写示例、引用边界。不是标准原文。 |
| `references/vocabulary-and-grammar.md` | 174 | 词典机制、常见替换表、词性陷阱、语法限制、技术名词与技术动词规则。 |
| `references/checklist.md` | 171 | M1–M14 机械检查、J1–J14 判断检查、安全说明专项 S1–S7、不可改清单、交付模板、交付判定、常见误报。 |
| `references/sources.md` | 87 | 权威来源、Issue 9 版本信息、行业应用、引用与免责边界。 |
| `docs/mixed-language.md` | 79 | 两个 skill 的七项硬冲突、按段落分诊流程、双语术语表、安全提示级别映射、合规声明分开写。中文版仓库存有相同副本。 |

## 工具

| 文件 | 行数 | 作用 |
|---|---|---|
| `scripts/check_en.py` | 265 | 零依赖检查脚本。M1–M14 与 S 系列，输出 `文件:行号: [规则号][级别] 说明`。支持 `--strict` / `--json` / `--kind` / `--max-proc` / `--max-desc` / `--no-vocab` / `--no-lang-skip`。默认跳过中文主导行。 |
| `scripts/install.py` | 121 | 安装器。`claude` / `workbuddy` / `codex` / `dir` 四种目标，用户级与项目级，`--dry-run` / `--force` / `--dest`。 |

## 示例

| 文件 | 行数 | 作用 |
|---|---|---|
| `examples/before.md` | 13 | 反例。脚本命中 12 条，其中 7 条【必须】。 |
| `examples/after.md` | 14 | 正例。脚本 0 条，`--strict` 退出码 0。 |

## 集成片段

| 文件 | 行数 | 作用 |
|---|---|---|
| `adapters/codex-AGENTS.md` | 25 | 追加到 `AGENTS.md` 的片段，用 `<!-- ste-en:begin -->` / `<!-- ste-en:end -->` 包裹，可重复执行不重复插入。 |
| `adapters/opencode-command.md` | 19 | opencode 自定义命令。带 frontmatter，用 `$ARGUMENTS` 接收目标文件。 |

## 测试与工程

| 文件 | 行数 | 作用 |
|---|---|---|
| `tests/test_check_en.py` | 75 | 8 个用例：正例通过、反例命中、退出码、JSON 结构、数字加单位算一词、`-ing` 白名单、语言检测、双语无误报。 |
| `LICENSE` | 21 | MIT，覆盖脚本。 |
| `LICENSE-docs` | 16 | CC BY 4.0，覆盖规则、词表、说明、示例。 |
| `.gitignore` | 8 | 忽略缓存与编辑器目录。 |

CI 不在本目录。配置位于工作区顶层的 `.github/workflows/ci.yml`。该配置分别执行两个 skill 的检查。

## 依赖关系

```text
SKILL.md ──引用──> references/ ──被检查──> scripts/check_en.py
AGENTS.md ─引用──> references/
docs/mixed-language.md   ←→ ste-zh-technical-writing/docs/mixed-language.md（内容一致）
dist/ste-en.prompt.md   自包含，不依赖任何文件
scripts/install.py ─复制──> SKILL.md + references/ + examples/ + scripts/check_en.py
tests/ ─调用──> scripts/check_en.py
```

`SKILL.md`、`AGENTS.md`、`dist/ste-en.prompt.md` 三份入口内容有重叠，属于**有意的冗余**：不同 agent 只读其中一份。改规则时按 `references/writing-rules.md` → `SKILL.md` 第 4 节 → `AGENTS.md` → `dist/ste-en.prompt.md` 顺序同步。改分诊规范时两个仓库的 `docs/mixed-language.md` 一起改。
