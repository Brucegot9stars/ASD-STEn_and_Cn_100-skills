# CHANGELOG

## 1.0.2 — 2026-11-19

前四轮评审整改与本轮一致性修复。

**规则与来源**
- 英文规则分节数更正为 14 / 2 / 7 / 5 / 5 / 6 / 3 / 7 / 4。
- `references/sources.md` 补 Issue 10 状态。尚无官方时间表。
- 修订 description 触发词、流程模式、句长口径与 before/after 语义。

**工具**
- `scripts/install.py` 修正 codex 目标路径。
- `scripts/check_en.py` 的 M9 拉丁缩写检查改用 `re.I`。
- 检查器空输入返回码改为 2。
- 新增 `tests/test_install.py`。单元测试由 8 例增至 14 例。

**打包与文档**
- `scripts/package.py` 修正 tag 中的斜杠。文件名替换为连字符。
- 修复源码包把 `--out` 输出目录打进包内的缺陷。输出目录首段动态排除。
- 更新 MANIFEST 文件数为 22，并按实际刷新全部行数。
- 删除 CHANGELOG 中已不存在的校验工具引用。

## 1.0.1 — 2026-11-19

CI 上移到工作区顶层。删除本目录的 `.github/workflows/ci.yml`。改由顶层配置分别执行两个 skill 的检查。本目录可独立分发，不依赖 CI 文件。

## 1.0.0 — 2026-11-19

首个独立发布版本。与 `ste-zh-technical-writing` 并列交付，规则集不合并。

**规则**
- 基于 ASD-STE100 Issue 9（2025-01）的执行摘要：53 条写作规则、9 节结构（14/2/7/5/5/6/3/7/4）。
- 硬约束：程序句 ≤ 20 词、描述句 ≤ 25 词、段落 ≤ 6 句、名词簇 ≤ 3 词、受控词典一词一义一词性。
- 明确边界：不含完整词典，非官方，不构成合规认证，AI 生成文本必须人工复核。

**工具**
- `scripts/check_en.py`：零依赖检查脚本，对应 M1–M14 与 S 系列，`--strict` / `--json` / `--kind` / `--no-vocab` / `--no-lang-skip`。
- `scripts/install.py`：安装到 Claude Code、WorkBuddy、Codex 或任意目录。
- 反例 12 条（7 条【必须】），正例 0 条。

**集成**
- `SKILL.md`：Agent Skills 入口（Claude Code、WorkBuddy）。
- `AGENTS.md`：通用入口（Codex、opencode）。
- `adapters/`：Codex 片段、opencode 自定义命令。
- `dist/ste-en.prompt.md`：单文件压缩版，供无 skill 机制的 agent 使用。
- `docs/mixed-language.md`：两个 skill 的分工与中英混合文本分诊规范。

**验证**
- 单元测试 14/14 通过。
