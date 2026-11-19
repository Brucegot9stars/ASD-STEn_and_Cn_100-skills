# 受控技术写作 Skill 集

两套给 AI agent 用的技术写作规范：英文版依据 **ASD-STE100 Simplified Technical English（Issue 9）**，中文版是**受控中文**。目标相同，让读者**一遍读对，只有一种理解**。

## 效果示例

英文版：

```text
Before: Prior to carrying out the lubrication procedure, ensure that the power supply has been isolated.
After:  1. Disconnect the power supply.
        2. Lubricate the bearing.
```

中文版：

```text
原文：用户首先需要登陆到目标服务器，然后切换到 /opt 目录并且创建一个用于存放采集器配置文件以及运行时产生的临时数据的工作目录。
改写：1. 登录目标服务器。2. 切换到 /opt 目录。3. 创建工作目录 /opt/collector。工作目录存放配置文件和临时数据。
```

## 两个 skill

| | `asd-ste100-technical-writing` | `ste-zh-technical-writing` |
|---|---|---|
| 用途 | 英文技术文档的写、改、审 | 中文技术文档的写、改、审 |
| 依据 | ASD-STE100 Issue 9，53 条规则 / 9 节 | 方法迁移，9 节 44 条规则 |
| 句长 | 程序句 ≤ 20 词，描述句 ≤ 25 词 | 操作句 ≤ 30 字，描述句 ≤ 40 字 |
| 词表 | 约 900 批准词、约 1200 不批准词 | 约 110 条中文词表 |
| 检查器 | `scripts/check_en.py` | `scripts/check_zh.py` |
| 合规声明 | 可写「按 Issue 9 改写」 | 不能声称符合 ASD-STE100 |

**两者不合并。** 句长单位、词典、语法限制、安全提示写法都不同。最关键的是合规边界：合并后模型容易拿英文规则改中文，并误标合规。

**中英混合文本**用分诊解决，不需要第三个 skill。按段落标 `EN / ZH / MIXED / CODE`。英文段用英文版，中文段用中文版，代码原样保留。两个脚本各跑一次。规范见 [`docs/mixed-language.md`](asd-ste100-technical-writing/docs/mixed-language.md)。

## 适用场景

适用：航空维修手册与工卡、安装配置指南、API 与运维文档。也用于 SOP、设备说明书、故障处理流程、安全警告。还用于翻译前简化与约束 LLM 输出。

不适用：营销文案、法律与法规原文、文学创作、需要个人风格的内容、代码与日志本身。

## 目录结构

```text
.
├── README.md                          # 本文件
├── LICENSE                            # 脚本：MIT
├── LICENSE-docs                       # 文档：CC BY 4.0
├── .github/workflows/
│   ├── ci.yml                         # 分支与 PR 检查
│   └── release.yml                    # v* 标签打包并发布 Release
├── scripts/package.py                 # 打包脚本，本地可复现
├── asd-ste100-technical-writing/      # 英文版 skill（21 个文件）
├── ste-zh-technical-writing/          # 中文版 skill（21 个文件）
└── books/asd-ste100/                  # 蒸馏审计与精华文档
```

每个 skill 仓库内部同构。

- 入口与说明：`SKILL.md`、`AGENTS.md`、`README.md`、`MANIFEST.md`。
- `references/`：规则与词表。
- `scripts/`：检查器与安装器。
- `examples/`：反例与正例。
- `dist/`、`adapters/`：各 agent 的适配文件。
- `tests/`：单元测试。

逐文件说明见各自的 `MANIFEST.md`。

## 快速开始

以中文版为例，在工作区根目录执行：

```bash
python ste-zh-technical-writing/scripts/install.py --target workbuddy --project --force
python asd-ste100-technical-writing/scripts/install.py --target workbuddy --project --force
```

`--target` 支持 `claude`、`workbuddy`、`codex`、`dir`。可选 `--project`、`--dest`、`--dry-run`、`--force`。

装好后直接对 agent 说：

- 「用 STE 改写这段维修步骤」
- 「用受控中文检查这份手册」
- 「把这几个术语统一一下」

也可直接跑检查器：

```bash
cd ste-zh-technical-writing
python scripts/check_zh.py 文档.md --strict
```

## Agent 适配

| Agent | 读取入口 | 安装方式 |
|---|---|---|
| Claude Code | `SKILL.md` | `install.py --target claude` |
| WorkBuddy | `SKILL.md` | `install.py --target workbuddy` |
| Codex | `AGENTS.md` | `install.py --target codex` |
| opencode | `AGENTS.md` + 自定义命令 | 复制 `adapters/opencode-command.md` |
| Hermes 等 | `dist/*.prompt.md` | 将单文件版粘进系统提示 |

各家的 frontmatter 键与命令目录可能随版本变化。适配文件给的是最小可用写法，若某个键不被识别，删掉即可，不影响规则本体。详细用法见各 skill 的 `README.md`。

## 验证

顶层 CI 用 `working-directory` 分别进入两个仓库，各跑单元测试、正例 `--strict`、反例命中检查。中文版额外检查规则文档不得有【必须】级发现。

本地复核：

```bash
(cd ste-zh-technical-writing && python -m unittest discover -s tests)
(cd asd-ste100-technical-writing && python -m unittest discover -s tests)
```

当前状态：两版单元测试各 8/8 通过。反例英文命中 12 条（7 条【必须】），中文命中 11 条（8 条【必须】）。正例均为 0 条。

## 发布

推送 `v*` 标签，例如 `v1.1.0`，会触发 `release.yml`。流程先跑两版检查，再打包，最后创建 GitHub Release 并上传附件。

产物有三个：

- `asd-ste100-technical-writing-<tag>.zip`
- `ste-zh-technical-writing-<tag>.zip`
- `ste-writing-skills-<tag>-source.zip`

本地可复现：`python scripts/package.py --tag v1.1.0`。产物写到 `dist/`，该目录已被忽略。

## 许可

本项目采用双许可，与两个 skill 仓库保持一致：

- **脚本**（`scripts/`、`tests/`）：MIT，见 [`LICENSE`](LICENSE)。
- **文档、规则、词表、示例**：CC BY 4.0，见 [`LICENSE-docs`](LICENSE-docs)。

可复制、修改、商用，需保留署名与许可说明。

## 边界

- 本项目是**非官方**写作辅助，不隶属 ASD 或 STEMG，不构成合规认证。
- 英文版不含完整标准正文与受控词典，关键用词以官方 Issue 9 PDF 为准。
- 中文版是方法迁移，不是 ASD-STE100 的官方译本。
- 检查脚本只查句法。事实错误、步骤顺序、术语选择仍需人工判断。
