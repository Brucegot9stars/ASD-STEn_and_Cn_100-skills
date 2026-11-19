# 文件清单

共 22 个文件。每个文件的作用、行数与依赖关系如下。配套项目 `asd-ste100-technical-writing` 有同规格结构，两者规则集不合并。

## 入口

| 文件 | 行数 | 作用 |
|---|---|---|
| `SKILL.md` | 285 | Agent Skills 入口。frontmatter（`name` / `description`）+ 用途、触发条件（含 2.3 中英混合文本）、任务表、9 节规则要点、执行流程、输出约束、检查清单、边界。Claude Code、WorkBuddy 直接读它。 |
| `AGENTS.md` | 103 | 通用 agent 入口。Codex、opencode 及自建 agent 读它。含启用条件、文件索引、硬约束摘要、流程、输出契约。 |
| `README.md` | 295 | 给人看的项目说明。用途、两个 skill 的分工、适用场景、目录结构、安装、各 agent 适配、用法、示例、阈值依据、维护、许可。 |
| `dist/ste-zh.prompt.md` | 121 | 单文件压缩版。36 条硬规则 + 选词表 + 输出格式 + 自检清单。供无 skill 机制的 agent（如 Hermes）直接粘进系统提示。 |
| `MANIFEST.md` | — | 本文件。 |
| `CHANGELOG.md` | 59 | 版本记录。 |

## 规则与词表

| 文件 | 行数 | 作用 |
|---|---|---|
| `references/writing-rules.md` | 381 | 核心。9 节 45 条规则，每条带【必须】/【建议】级别、✗ 反例、✓ 正例、理由。 |
| `references/word-list.md` | 169 | 约 110 条词表。9 类：异形词、名词化、空转词、模糊词、虚指、选词表、易混搭配、黑话、情态。标注哪些能被脚本自动检查。 |
| `references/checklist.md` | 137 | 19 项机械检查、判断检查、否定范围判断项、变更说明模板、交付模板、验收判定、脚本边界说明。 |
| `references/sources.md` | 73 | 方法来源、STE 与中文规则的对应表、阈值校准依据、与中文排版规范的关系、已知局限。 |
| `docs/mixed-language.md` | 79 | 两个 skill 的七项硬冲突、按段落分诊流程、双语术语表、安全提示级别映射、合规声明分开写。英文版仓库存有相同副本。 |

## 工具

| 文件 | 行数 | 作用 |
|---|---|---|
| `scripts/check_zh.py` | 283 | 零依赖检查脚本。19 类机械检查，输出 `文件:行号: [规则号][级别] 说明`。支持 `--strict` / `--json` / `--kind` / `--max-op` / `--max-desc` / `--no-vocab` / `--no-lang-skip`。默认跳过纯英文行。 |
| `scripts/install.py` | 125 | 安装器。`claude` / `workbuddy` / `codex` / `dir` 四种目标，用户级与项目级，`--dry-run` / `--force` / `--dest`。 |

## 示例

| 文件 | 行数 | 作用 |
|---|---|---|
| `examples/before.md` | 9 | 反例。脚本命中 11 条，其中 8 条【必须】。 |
| `examples/after.md` | 31 | 正例。脚本 0 条，`--strict` 退出码 0。 |

## 集成片段

| 文件 | 行数 | 作用 |
|---|---|---|
| `adapters/codex-AGENTS.md` | 25 | 追加到 `AGENTS.md` 的片段，用 `<!-- ste-zh:begin -->` / `<!-- ste-zh:end -->` 包裹，可重复执行不重复插入。 |
| `adapters/opencode-command.md` | 19 | opencode 自定义命令。带 frontmatter，用 `$ARGUMENTS` 接收目标文件。 |

## 测试与工程

| 文件 | 行数 | 作用 |
|---|---|---|
| `tests/test_check_zh.py` | 85 | 本文件 8 例。两文件共 14 个用例：正例通过、反例命中、退出码、JSON 结构、规则文档无【必须】、代码与引号跳过、语言检测、双语无误报。 |
| `tests/test_install.py` | 103 | 6 个用例：codex 片段追加、幂等、`--dry-run` 不写盘、`--force` 提示、`dir` 目标与 `--dest`、dry-run 与 force 组合。 |
| `LICENSE` | 21 | MIT，覆盖脚本。 |
| `LICENSE-docs` | 15 | CC BY 4.0，覆盖规则、词表、说明、示例。 |
| `.gitignore` | 8 | 忽略缓存与编辑器目录。 |

CI 不在本目录。配置位于工作区顶层的 `.github/workflows/ci.yml`。该配置分别执行两个 skill 的检查。

## 依赖关系

```text
SKILL.md ──引用──> references/ ──被检查──> scripts/check_zh.py
AGENTS.md ─引用──> references/
docs/mixed-language.md   ←→ asd-ste100-technical-writing/docs/mixed-language.md（内容一致）
dist/ste-zh.prompt.md   自包含，不依赖任何文件
scripts/install.py ─复制──> SKILL.md + references/ + examples/ + scripts/check_zh.py
tests/ ─调用──> scripts/check_zh.py 与 scripts/install.py
```

`SKILL.md`、`AGENTS.md`、`dist/ste-zh.prompt.md` 三份入口内容有重叠，属于**有意的冗余**：不同 agent 只读其中一份。改规则时按 `references/writing-rules.md` → `SKILL.md` 第 4 节 → `references/checklist.md` 判断项与否定范围 → `AGENTS.md` → `dist/ste-zh.prompt.md` 顺序同步。脚本规则号映射单独维护。改编号时同步 `scripts/check_zh.py` 与 `references/checklist.md`。改分诊规范时两个仓库的 `docs/mixed-language.md` 一起改。每次实质变更记入 `CHANGELOG.md`。
