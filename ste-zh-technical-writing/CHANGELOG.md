# CHANGELOG

## 1.1.2 — 2026-11-19

前四轮评审整改与本轮一致性修复。

**规则与文档**
- 中文规则由 36 条增至 45 条。每条带级别、反例、正例与理由。
- 补严格档标注。安全关键文档用 20 / 30 字。
- 修订规则号口径、流程模式、description 触发词与句长口径。
- 修订 before/after 语义与「等」的规则号级别。
- 新增否定范围规则。SKILL、checklist、AGENTS 与 dist 口径一致。
- 删除「符合 ASTM F3349」的旧表述。更正为 ASD/STEMG 自有标准。

**工具**
- `scripts/install.py` 修正 codex 目标路径。
- 检查器空输入返回码改为 2。
- 新增 `tests/test_install.py`。单元测试由 8 例增至 14 例。

**打包与文档**
- 更新 MANIFEST 文件数为 22，并按实际刷新全部行数。
- 删除 CHANGELOG 中已不存在的校验工具引用。

## 1.1.1 — 2026-11-19

CI 上移到工作区顶层。删除本目录的 `.github/workflows/ci.yml`。改由顶层配置分别执行两个 skill 的检查。本目录可独立分发，不依赖 CI 文件。

## 1.1.0 — 2026-11-19

明确与英文版 skill 的分工，补齐中英混合文本处理能力。规则集**不合并**。

- 新增 `docs/mixed-language.md`。内容含不合并的七项硬冲突、按段落分诊流程、双语术语表与安全提示级别映射。该文档在英文版仓库存有一份相同副本。
- `scripts/check_zh.py` 增加语言感知跳过（默认跳过纯英文行）与 `--no-lang-skip`。英文版 `check_en.py` 对应跳过中文主导行。
- `SKILL.md` 新增 2.3 节「中英混合文本」。`AGENTS.md`、`dist/ste-zh.prompt.md`、`README.md` 同步补充分诊说明与交叉引用。
- 单元测试新增语言检测与双语无误报用例。

## 1.0.0 — 2026-11-19

首个独立发布版本。

**规则**
- 9 节 45 条受控中文写作规则，分【必须】与【建议】两级。
- 阈值：操作句 30 字、描述句 40 字（安全关键文档 20 / 30 字），依据约 350 万字语料 90 分位校准。
- 词表约 110 条，覆盖异形词、名词化、空转词、模糊词、虚指、选词表、易混搭配、黑话、情态。

**工具**
- `scripts/check_zh.py`：零依赖检查脚本，19 类机械检查，支持 `--strict` / `--json` / `--kind` / `--max-op` / `--max-desc`。
- `scripts/install.py`：安装到 Claude Code、WorkBuddy、Codex 或任意目录。

**集成**
- `SKILL.md`：Agent Skills 入口（Claude Code、WorkBuddy）。
- `AGENTS.md`：通用入口（Codex、opencode）。
- `adapters/`：Codex 片段、opencode 自定义命令。
- `dist/ste-zh.prompt.md`：单文件压缩版，供无 skill 机制的 agent 使用。

**验证**
- `examples/after.md` 通过 `--strict`（0 条【必须】）。
- `examples/before.md` 命中 11 条（8 条【必须】）。
- `SKILL.md` 与 `references/` 自身通过【必须】级检查。
