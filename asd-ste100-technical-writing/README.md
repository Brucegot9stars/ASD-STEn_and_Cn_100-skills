# asd-ste100-technical-writing

用 **ASD-STE100 Simplified Technical English（Issue 9）** 写、改、审英文技术文档的 skill。目标是让读者**一次读对、只有一种理解**。

```text
Before: Prior to carrying out the lubrication procedure, ensure that the power supply has been isolated.
After:  1. Disconnect the power supply.
        2. Lubricate the bearing.
```

本仓库是**非官方**写作辅助，不隶属 ASD 或 STEMG，不构成合规认证。标准正文与词典以官方 Issue 9 PDF 为准。

## 1. 为什么是两个 skill

配套项目：`ste-zh-technical-writing`（受控中文版，同级目录，各自独立交付）。

**不合并**，因为规则集有硬冲突：英文按 20/25 **词**、中文按 30/40 **字**；英文有约 900 批准词的受控词典，中文是约 110 条词表；英文管 `-ing`、完成时、冠词，中文管名词化、`以上/以下`、定语层数。最关键的是合规边界——英文部分可写"按 Issue 9 改写"，中文部分**不能**声称符合 ASD-STE100。合并会让模型把中文按英文规则改，并误标合规。

两个 skill 共享目录约定、安装器、顶层 CI 和许可。两者独立安装、独立触发、独立检查。

**中英混合文本**靠分诊解决，不需要第三个 skill。完整规范见 [`docs/mixed-language.md`](docs/mixed-language.md)：按段落标 `EN / ZH / MIXED / CODE`，英文段用本 skill，中文段用中文版，代码与界面文字原样保留，一句只用一套句长上限，最后两个检查脚本各跑一次。

## 2. 适用场景

| 适用 | 不适用 |
|---|---|
| 航空维修手册、工卡、AMM | 营销文案、品牌文案、发布公告 |
| 安装/拆卸/调试步骤、SOP | 法律合同、法规原文、认证文本 |
| 运行手册（runbook）、API 运维文档 | 文学、博客、对话式内容 |
| 安全警告（WARNING / CAUTION / NOTE） | 纯中文写作（用中文版 skill） |
| 设备说明书、故障处理流程 | 代码、日志、命令本身 |
| 翻译前简化、术语统一、约束 LLM 输出 | 需要作者个人风格的内容 |

行业：航空、国防、汽车、铁路、医疗器械、制药、能源、机械、IT 运维。标准强制或推荐场景：ATA iSpec 2200（原 ATA 100）、ATA 104、S1000D、EASA/FAA/CAAC 持续适航指令。

## 3. 目录结构

```text
asd-ste100-technical-writing/
├── SKILL.md                    # 入口①：Agent Skills（Claude Code / WorkBuddy）
├── AGENTS.md                   # 入口②：常驻指令（Codex / opencode）
├── README.md                   # 本文件
├── MANIFEST.md                 # 逐文件说明与依赖关系
├── CHANGELOG.md                # 版本记录
├── LICENSE / LICENSE-docs      # MIT（脚本）/ CC BY 4.0（文档）
├── docs/
│   └── mixed-language.md       # 两 skill 分工与中英混合文本分诊规范
├── references/
│   ├── writing-rules.md        # 53 条规则按 9 节的执行摘要与示例
│   ├── vocabulary-and-grammar.md  # 词典机制、替换表、词性陷阱、语法限制
│   ├── checklist.md            # M1–M14 机械检查、J1–J14 判断检查、交付模板
│   └── sources.md              # 权威来源、版本信息、免责边界
├── scripts/
│   ├── check_en.py             # 零依赖检查脚本
│   └── install.py              # 安装器
├── examples/
│   ├── before.md               # 反例：12 条发现，7 条【必须】
│   └── after.md                # 正例：0 条
├── dist/ste-en.prompt.md       # 入口③：单文件版（Hermes 等无 skill 机制）
├── adapters/
│   ├── codex-AGENTS.md         # 追加到 AGENTS.md 的片段
│   └── opencode-command.md     # opencode 自定义命令
└── tests/
    ├── test_check_en.py        # 检查器单元测试
    └── test_install.py         # 安装器单元测试
```

CI 配置在工作区顶层的 `.github/workflows/ci.yml`。本目录可单独分发，不带 CI 文件。

**命名约定**：目录名 = skill 名 = `name` 字段，全小写连字符。入口恒为 `SKILL.md` / `AGENTS.md`。参考材料放 `references/`，可执行放 `scripts/`，示例放 `examples/`。

## 4. 安装

### 4.1 依赖

- Python **3.9+**（只用标准库，无需 `pip install`）
- 无网络依赖，无 API key，无外部词表文件
- 若要判定某个词是否"批准"，需要 ASD-STE100 Issue 9 官方 PDF（本仓库不含词典）

### 4.2 获取与自检

```bash
git clone <this-repo> asd-ste100-technical-writing
cd asd-ste100-technical-writing
python scripts/check_en.py --strict examples/after.md    # 应当 0 条
python -m unittest discover -s tests                    # 14 个用例
```

### 4.3 一键安装

```bash
python scripts/install.py --target claude               # ~/.claude/skills/asd-ste100-technical-writing/
python scripts/install.py --target workbuddy            # ~/.workbuddy/skills/asd-ste100-technical-writing/
python scripts/install.py --target workbuddy --project # ./.workbuddy/skills/...
python scripts/install.py --target claude --project    # ./.claude/skills/...
python scripts/install.py --target codex               # 当前目录写入 AGENTS.md 片段（幂等）
python scripts/install.py --target dir --dest D:/skills
```

可选参数：`--dry-run`、`--force`、`--dest`。`--project` 写入**执行命令时的当前目录**，请先 `cd` 到目标项目根目录。

`--target codex` 不需要 `--dest` 或 `--project`，直接在当前目录写 AGENTS.md 片段。

安装只复制运行所需文件：`SKILL.md`、`references/`、`examples/`、`scripts/check_en.py`。`tests/`、`adapters/`、`dist/`、`docs/` 不进入 skill 目录。

### 4.4 各 agent 的适配方式

| Agent | 安装位置 | 触发方式 | 备注 |
|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` 或项目 `.claude/skills/` | 按 `description` 自动触发，也可在对话中点名 | 标准 Agent Skills 结构，`SKILL.md` 开箱可用 |
| **WorkBuddy** | `~/.workbuddy/skills/` 或项目 `.workbuddy/skills/` | 按 `description` 触发，或说"用 STE 改写" | 与本项目结构一致 |
| **Codex** | 仓库根 `AGENTS.md`，或全局 `~/.codex/AGENTS.md` | 读取 `AGENTS.md` 作为常驻指令 | 用 `adapters/codex-AGENTS.md` |
| **opencode** | 项目 `AGENTS.md` + `.opencode/command/ste-en.md` | `AGENTS.md` 常驻，命令按需触发 | 用 `adapters/opencode-command.md` |
| **Hermes / 其他** | 系统提示或项目说明文件 | 由宿主决定 | 用 `dist/ste-en.prompt.md` 单文件版，无外部依赖 |

各家前端字段（命令名、frontmatter 键）可能随版本变化。上面是最小可用写法，删掉不认识的键不影响规则本体。

**中英混合任务**：两个 skill 都装，触发时让 agent 先按 `docs/mixed-language.md` 分诊，不要只加载其中一个。

## 5. 基本用法

```bash
python scripts/check_en.py 文档.md
python scripts/check_en.py --strict docs/*.md            # CI：有【必须】级发现即退出码 1
python scripts/check_en.py --json 文档.md                # 给流水线消费
python scripts/check_en.py --kind description answer.md # 聊天回答
python scripts/check_en.py --no-lang-skip 双语手册.md    # 强制检查全部行
```

| 参数 | 作用 | 默认 |
|---|---|---|
| `--strict` | 存在【必须】级发现时退出码 1 | 关 |
| `--json` | 输出 JSON（`total` / `must` / `files`） | 关 |
| `--kind procedure\|description` | 强制一种句型判句长 | 自动 |
| `--max-proc N` | 程序句词数上限 | 20 |
| `--max-desc N` | 描述句词数上限 | 25 |
| `--no-vocab` | 跳过词表与语法形式检查 | 关 |
| `--no-lang-skip` | 不跳过中文主导行 | 关 |

检查项对应 `references/checklist.md` 的 M1–M14 与 S 系列：分号、破折号、完成时、进行时、缩写、拉丁缩写、`-ing`、模糊情态、软化语、`NOTE` 含指令、句长、段落句数、祈使句开头、条件在句尾。

**脚本查不出**：词典批准状态、词性、词义、名词簇关系、冠词是否该补、技术含义是否改变。这些必须人工判断。

## 6. 示例调用

### 6.1 脚本实际输出

```bash
$ python scripts/check_en.py examples/before.md
examples/before.md:3: [M3][必须] 不用分号：拆成两句或改列表
examples/before.md:3: [M6][必须] 完成时：改成一般时态或祈使句
examples/before.md:5: [M8][必须] 缩写形式：写完整形式
examples/before.md:5: [M9][必须] 拉丁缩写：改成 for example / that is
examples/before.md:9: [S5][必须] NOTE 含操作指令：把指令移到步骤里
...
合计 12 条，其中【必须】7 条。
```

```bash
$ python scripts/check_en.py --strict examples/after.md
合计 0 条，其中【必须】0 条。
$ echo $?
0
```

### 6.2 Claude Code / WorkBuddy

```text
> 用 STE 改写这段维修步骤，保留所有数值和单位。

（skill 触发）读 references/writing-rules.md 与 vocabulary-and-grammar.md，
跑 scripts/check_en.py，输出改写稿 + 变更说明 + 待确认清单。
```

### 6.3 Codex

把 `adapters/codex-AGENTS.md` 追加到仓库 `AGENTS.md`，之后：

```text
按 AGENTS.md 里的 STE 规则检查 docs/amm.md。
```

### 6.4 opencode

复制 `adapters/opencode-command.md` 到 `.opencode/command/ste-en.md`，之后：

```text
/ste-en docs/amm.md --check
```

### 6.5 Hermes 或无 skill 机制的 agent

把 `dist/ste-en.prompt.md` 全文粘进系统提示。它含核心规则、常见替换、输出格式与自检清单，不依赖外部文件。

### 6.6 中英混合文档

```text
这是中英混合文档。先按 docs/mixed-language.md 分诊：英文段用 asd-ste100-technical-writing，
中文段用 ste-zh-technical-writing，代码与界面文字原样保留。
最后分别跑 check_en.py 与 check_zh.py，并核对双语术语表与安全提示级别。
```

## 7. 规则速查

| 规则 | 要求 | 反例 → 正例 |
|---|---|---|
| 1.1 | 只用批准词 | `Commence the procedure.` → `Start the procedure.` |
| 2.1 | 名词簇 ≤ 3 词 | `forward turbine overheat thermocouple terminal tags` → 用介词拆开 |
| 3.4 | 去被动情态 | `The temperature must be adjusted.` → `Adjust the temperature.` |
| 4.1 | 程序句 ≤ 20 词 | 长句 → 拆步骤 |
| 5.2 | 一句一指令 | `Set ... and release ...` → 两步 |
| 6.3 | 描述句 ≤ 25 词 | 多条件长句 → 2–3 短句 |
| 7.1 | 级别正确 | 人身风险用 `CAUTION` → 改 `WARNING` |
| 8.1 | 不用分号 | `...battery; only...` → 拆两句 |
| 9.4 | 术语一致 | `panel` / `console` 混用 → 统一 |

完整 9 节结构见 [`references/writing-rules.md`](references/writing-rules.md)。

## 8. 边界

- **不是"baby English"**，用受控方式描述复杂系统。
- **不修正错误的技术内容**。清晰但错误的指令仍是错误指令。
- **不消除翻译需求**，降低的是翻译难度和成本。
- **不含完整词典**。关键用词查官方 Issue 9 PDF。
- **ASD/STEMG 不认证任何工具**。脚本会漏报误报。
- **AI 生成文本可能"看起来合规"**，必须人工复核。
- **版本**：Issue 9（2025-01）已替代 Issue 8（2021-04），合同若写 Issue 8 需确认是否迁移。
- **不要"润色"回普通英语**，为可读性换词会破坏受控性。

## 9. 维护

```bash
python -m unittest discover -s tests
python scripts/check_en.py --strict examples/after.md
python scripts/check_en.py --strict examples/before.md   # 预期退出码 1
```

改规则时按 `references/writing-rules.md` → `SKILL.md` 第 4 节 → `AGENTS.md` → `dist/ste-en.prompt.md` 顺序同步。`docs/mixed-language.md` 与中文版仓库同名文件保持一致。

## 10. 发布与版本

两套 skill 各自独立版本。版本记录见各自的 CHANGELOG.md。发布 tag 只标识发布批次。tag 不代表各 skill 的内部版本号。同一 tag 下两个包的版本号可以不同。

## 11. 许可

- 规则、词表、README、示例文本：**CC BY 4.0**
- 脚本：**MIT**

ASD-STE100 是 ASD 的商标与版权作品。本仓库未复制标准正文或词典，只做执行摘要，并明确标注以官方 PDF 为准。
