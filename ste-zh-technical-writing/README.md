# ste-zh-technical-writing

受控中文技术写作 skill。让中文技术文档**读一遍就不会读错**。

方法借自 [ASD-STE100](https://www.asd-ste100.org/)（航空维修手册用的受控英语）。规则按中文的歧义来源重写。

产物有三样：9 节 45 条规则、约 110 条受控词表、一个零依赖检查脚本。另有一套入口文件，可直接被 Claude Code、Codex、opencode、WorkBuddy、Hermes 调用。

```text
原文：用户首先需要登陆到目标服务器，然后切换到 /opt 目录并且创建一个用于存放采集器配置文件以及运行时产生的临时数据的工作目录。
改写：1. 登录目标服务器。2. 切换到 /opt 目录。3. 创建工作目录 /opt/collector。工作目录存放配置文件和临时数据。
```

## 1. 这个项目解决什么问题

中文技术文档的歧义不在语法，在几个固定位置反复出现：

| 歧义源 | 例子 | 规则 |
|---|---|---|
| 名词化 | `对日志进行压缩处理` | 1.3 直接用动词 |
| 长定语全部前置 | `前部涡轮过热热电偶接线柱固定螺栓` | 2.1 定语 ≤ 3 层 |
| 端点歧义 | `20 N·m 以上` 含不含 20 | 8.1 写"不小于" |
| `可以` 双重含义 | 是"允许"还是"能力" | 1.7 情态只留三档 |
| 一个动词覆盖多对象 | `打开` 文件 / 功能 / 程序 | 1.2 一词一职 |
| 连接词串步骤 | `然后`、`接着` | 4.4 改编号步骤 |

这些问题没法靠"写清楚一点"解决，只能靠**可检查的规则**。

### 两个 skill 不合并

配套项目 `asd-ste100-technical-writing` 管英文技术文档。两者**不合并**。句长单位（20/25 词 vs 30/40 字）、受控词典、语法限制与合规声明边界都是硬冲突。最关键的一条：英文部分可写"按 ASD-STE100 Issue 9 改写"，中文部分**不能**声称符合该标准。合并会让模型把中文按英文规则改，并误标合规。

**中英混合文本**靠分诊解决，不需要第三个 skill。按段落标 `ZH / EN / MIXED / CODE`。中文段用本 skill，英文段用英文版，代码与界面文字原样保留。一句只用一套句长上限，最后两个脚本各跑一次。完整规范见 `docs/mixed-language.md`。

### 不是 ASD-STE100 中文版

ASD-STE100 只规范英文，没有官方中文版，也不对中文文本作合规判定。本项目是**方法迁移**。借用受控词表、句长上限、一句一事、祈使句、条件前置、三级安全提示这些机制，规则文本按中文重写。

因此：**不得声称本项目的产出"符合 ASD-STE100"**。英文文档请用同作者的 `asd-ste100-technical-writing` skill（`SKILL.md` 结构兼容，可并列安装）。

## 2. 适用与不适用

| 适用 | 不适用 |
|---|---|
| 操作步骤、安装/部署/配置指南 | 营销文案、品牌文案、发布会稿 |
| 接口文档、API 说明、错误码表 | 法律合同、法规原文、认证文本 |
| 运维手册（runbook）、SOP、工卡 | 文学、随笔、需要作者声音的内容 |
| 设备说明书、故障处理流程 | 英文技术文档（用英文版 skill） |
| 安全警告、注意事项 | 代码、日志本身（原样保留） |
| 约束 AI 输出（"别端着说话"） | 需要保留个人风格的博客 |

## 3. 目录结构

```text
ste-zh-technical-writing/
├── SKILL.md                 # skill 入口（Claude Code / WorkBuddy 约定：frontmatter + 正文）
├── AGENTS.md                # 通用 agent 入口（Codex / opencode / 自建 agent）
├── README.md                # 本文件
├── MANIFEST.md              # 文件清单：每个文件的作用与规模
├── CHANGELOG.md             # 版本记录
├── LICENSE                  # 脚本：MIT
├── LICENSE-docs             # 规则、词表、README：CC BY 4.0
├── references/
│   ├── writing-rules.md     # 9 节 45 条规则，每条带 ✗/✓ 与理由
│   ├── word-list.md         # 约 110 条：异形词、名词化、空转词、模糊词、虚指、选词表、易混搭配、黑话、情态
│   ├── checklist.md         # 19 项机械检查 + 判断检查 + 变更说明/交付模板
│   └── sources.md           # 方法来源、阈值校准依据、与官方标准的关系
├── scripts/
│   ├── check_zh.py          # 零依赖检查脚本（Python 3.9+）
│   └── install.py           # 一键安装到各 agent 目录
├── examples/
│   ├── before.md            # 反例：11 条发现，8 条【必须】
│   └── after.md             # 正例：0 条，--strict 通过
├── docs/
│   └── mixed-language.md    # 两个 skill 的分工与中英混合文本分诊规范
├── dist/
│   └── ste-zh.prompt.md     # 单文件压缩版，供无 skill 机制的 agent 直接粘进系统提示
├── adapters/
│   ├── codex-AGENTS.md      # 追加到 AGENTS.md 的片段
│   └── opencode-command.md  # opencode 自定义命令
└── tests/
    ├── test_check_zh.py     # 检查器单元测试
    └── test_install.py      # 安装器单元测试
```

CI 配置在工作区顶层的 `.github/workflows/ci.yml`。本目录可单独分发，不带 CI 文件。

**命名约定**：目录名 = skill 名 = `name` 字段，全小写连字符。入口恒为 `SKILL.md`（agent 用）与 `AGENTS.md`（通用用）。参考材料一律放 `references/`，可执行文件一律放 `scripts/`，反例正例一律放 `examples/`。

## 4. 安装

### 4.1 依赖

- Python **3.9+**（只用标准库，无需 `pip install`）
- 无网络依赖，无 API key

### 4.2 获取

```bash
git clone <this-repo> ste-zh-technical-writing
cd ste-zh-technical-writing
python scripts/check_zh.py --strict examples/after.md   # 自检：应当 0 条
```

### 4.3 一键安装到各 agent

```bash
python scripts/install.py --target claude              # ~/.claude/skills/ste-zh-technical-writing/
python scripts/install.py --target workbuddy           # ~/.workbuddy/skills/ste-zh-technical-writing/
python scripts/install.py --target workbuddy --project # ./.workbuddy/skills/ste-zh-technical-writing/
python scripts/install.py --target claude --project    # ./.claude/skills/ste-zh-technical-writing/
python scripts/install.py --target codex               # 在当前目录写入 AGENTS.md 片段（幂等）
python scripts/install.py --target dir --dest D:/skills # 任意目录
```

可选参数：`--dry-run` 只打印将写入的路径，`--force` 覆盖已存在目录。

`--target codex` 不需要 `--dest` 或 `--project`，直接在当前目录写 AGENTS.md 片段。

`--project` 写入**执行命令时的当前目录**。要装到某个项目，先 `cd` 到该项目根目录，或用 `--dest` 给绝对路径。

安装只复制运行所需文件：`SKILL.md`、`references/`、`scripts/check_zh.py`、`examples/`。`tests/`、`adapters/`、`dist/` 不进入 skill 目录。

### 4.4 各 agent 的适配方式

| Agent | 安装位置 | 触发方式 | 备注 |
|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` 或项目 `.claude/skills/` | 按 `description` 自动触发，也可在对话中直接点名 | 标准 Agent Skills 结构，`SKILL.md` 开箱可用 |
| **WorkBuddy** | `~/.workbuddy/skills/` 或项目 `.workbuddy/skills/` | 按 `description` 触发，或直接说"用受控中文改写" | 与本项目结构一致，`--target workbuddy` 即可 |
| **Codex** | 仓库根 `AGENTS.md`，或全局 `~/.codex/AGENTS.md` | 读取 `AGENTS.md` 作为常驻指令 | 用 `adapters/codex-AGENTS.md`，指向 `references/` |
| **opencode** | 项目 `AGENTS.md` + `.opencode/command/ste-zh.md` | `AGENTS.md` 常驻，命令按需触发 | 用 `adapters/opencode-command.md` |
| **Hermes / 其他** | 系统提示或项目说明文件 | 由宿主决定 | 用 `dist/ste-zh.prompt.md` 单文件版，无外部依赖 |

各家的前端字段（命令名、frontmatter 键）可能随版本变化。上面给的是**最小可用**写法，若你的版本不认某个键，删掉它不影响规则本体。

## 5. 基本用法

### 5.1 改写一段文档

对 agent 说：

```text
用受控中文改写这段安装步骤，保留所有数值和路径。
```

agent 按 `SKILL.md` 的流程执行：分类 → 锁定不可改内容 → 建术语表 → 分层改写 → 跑脚本 → 复核 → 交付三件套。

### 5.2 检查已有文档

```bash
python scripts/check_zh.py 文档.md                 # 列出所有发现
python scripts/check_zh.py --strict docs/*.md     # CI：有【必须】级发现即退出码 1
python scripts/check_zh.py --kind 描述 answer.md  # 聊天回答：不按操作句算句长
python scripts/check_zh.py --max-op 20 --max-desc 30 手册.md   # 安全关键文档严格档
python scripts/check_zh.py --json 文档.md          # 给流水线消费
```

| 参数 | 作用 | 默认 |
|---|---|---|
| `--strict` | 存在【必须】级发现时退出码 1 | 关 |
| `--json` | 输出 JSON（`total` / `must` / `files`） | 关 |
| `--kind 操作\|描述` | 强制一种句型判句长 | 自动 |
| `--max-op N` | 操作句字数上限 | 30 |
| `--max-desc N` | 描述句字数上限 | 40 |
| `--no-vocab` | 跳过词表检查 | 关 |
| `--no-lang-skip` | 不跳过纯英文行（默认跳过，便于双语文档分诊） | 关 |

双语文档分诊示例：

```bash
python ../asd-ste100-technical-writing/scripts/check_en.py --strict 双语手册.md
python scripts/check_zh.py --strict 双语手册.md
```

任一脚本出现【必须】级发现，整份文档不交付。

输出格式：`文件:行号: [规则号][级别] 说明`。

### 5.3 统一术语

```text
把这四份文档里的"删除 / 移除 / 清除 / 去掉"统一成一个词，输出替换清单。
```

## 6. 示例调用

### 6.1 脚本实际输出

```bash
$ python scripts/check_zh.py examples/before.md
examples/before.md:3: [1.1][必须] 「登陆」是错别字，写「登录」
examples/before.md:3: [1.4][必须] 空转词：删除，直接给事实
examples/before.md:3: [4.1][必须] 描述句 73 字，不超过 40 字
examples/before.md:3: [4.4][建议] 串联词：拆成编号步骤
examples/before.md:3: [4.5][必须] 并列堆叠：拆句或改列表
examples/before.md:5: [2.3][建议] 虚指修饰：写出具体对象
examples/before.md:7: [1.5][必须] 模糊词：改成可执行的条件、时限或数值
examples/before.md:7: [4.1][必须] 描述句 46 字，不超过 40 字
examples/before.md:7: [9.1][必须] 不用分号：拆句或改列表
examples/before.md:9: [7.4][建议] 空提示：写具体防护动作

合计 11 条，其中【必须】8 条。
```

```bash
$ python scripts/check_zh.py --strict examples/after.md
合计 0 条，其中【必须】0 条。
$ echo $?
0
```

### 6.2 Claude Code / WorkBuddy

```text
> 帮我按受控中文检查 docs/deploy.md，先给必须项，再给建议项。

（skill 触发）会读 references/writing-rules.md 与 word-list.md，
跑 scripts/check_zh.py，逐条给规则号、原文、改写、理由。
```

### 6.3 Codex

把 `adapters/codex-AGENTS.md` 追加到仓库 `AGENTS.md`。装好后在仓库内直接说：

```text
按 AGENTS.md 里的受控中文规则改写 docs/runbook.md。
```

### 6.4 opencode

复制 `adapters/opencode-command.md` 到 `.opencode/command/ste-zh.md`。装好后：

```text
/ste-zh docs/deploy.md --check
```

### 6.5 Hermes 或无 skill 机制的 agent

把 `dist/ste-zh.prompt.md` 全文粘进系统提示，或写进项目说明文件。它是压缩版，含 36 条硬规则、核心替换表、输出格式与自检清单，不依赖外部文件。

## 7. 规则速查（最高频的 10 条）

| # | 规则 | 反例 → 正例 |
|---|---|---|
| 1.3 | 不用 `进行 / 加以 + 动词` | 对配置进行修改 → 修改配置 |
| 1.1 | 一个概念只用一个词 | 删除 / 移除 / 清除 混用 → 全用"删除" |
| 2.1 | 定语 ≤ 3 层 | 前部涡轮过热热电偶接线柱螺栓 → 分开写 |
| 3.1 | 操作句动词开头 | 请点击保存 → 点击「保存」 |
| 3.2 | 不用 `被` 字句（步骤里） | 温度必须被调整 → 将温度调整到 80 °C |
| 4.1 | 操作句 ≤ 30 字，描述句 ≤ 40 字 | 56 字长句 → 拆三步 |
| 4.2 | 一句一个动作 | 按下并保持 3 s 后松开 → 按住 3 s。松开。 |
| 4.3 | 条件在动作前 | 关闭阀门，如果超压 → 如果超压，关闭阀门 |
| 7.2 | 安全提示在步骤前、独立成段 | 步骤 5 括号里加"注意高温" → 警告段前置 |
| 8.1 | 不用"以上/以下" | 20 N·m 以上 → 不小于 20 N·m |

完整 45 条见 [`references/writing-rules.md`](references/writing-rules.md)。

## 8. 设计约束

- **只改散文**。代码、命令、路径、参数、错误串、界面文字、数字、单位原样保留。
- **不新增事实**。不加原文没有的数值、条件、能力、结论。
- **不删信息**。警告、限制、例外、默认值、失败处理必须保留。
- **不改变确定性**。`可能` 不得升级为 `必须`。
- **不声称合规**。可以说"按受控中文规则改写"，不能说"符合 ASD-STE100"。
- **脚本只查句法**。事实对不对、术语选得准不准、顺序合不合理，必须人工判断。
- **脚本级别不等于规则级别**。脚本只报可机械判定的项。以规则文档的级别为准。

## 9. 阈值从哪来

操作句 30 字、描述句 40 字，不是估的。做法参照公开项目 Simplified Technical Chinese。语料是约 350 万字中文技术文档，含 8 个开源项目、2856 个文件。统计句长分布后取 90 分位：操作句 33 字、描述句 41 字。本项目取整为 30 / 40，留余量。

严格档 20 / 30 字用于航空、医疗、高压、化工等场景，是工程判断，没有语料校准支撑。细节与免责见 [`references/sources.md`](references/sources.md)。

## 10. 维护

```bash
python -m unittest discover -s tests          # 单元测试
python scripts/check_zh.py --strict SKILL.md references/*.md   # 文档自检
```

- 改规则：先改 `references/writing-rules.md`，再同步 `SKILL.md` 第 4 节摘要与 `dist/ste-zh.prompt.md`。
- 改词表：改 `references/word-list.md` 后，同步 `scripts/check_zh.py` 的 `BANNED` 表，再跑 `examples/` 确认无误报。
- 加词条写清四项：词、意义、处理方式（禁用 / 选词 / 限定）、一个例句。
- 版本变更记入 `CHANGELOG.md`。

## 11. 发布与版本

两套 skill 各自独立版本。版本记录见各自的 CHANGELOG.md。发布 tag 只标识发布批次。tag 不代表各 skill 的内部版本号。同一 tag 下两个包的版本号可以不同。

## 12. 许可

- 规则、词表、README、示例文本：**CC BY 4.0**
- 脚本：**MIT**

本项目为**非官方**写作辅助，不隶属 ASD、STEMG 或任何相关标准组织，不构成合规认证。
