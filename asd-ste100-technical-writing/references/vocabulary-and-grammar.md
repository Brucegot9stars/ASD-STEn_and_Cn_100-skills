# 词汇与语法限制

## 1. 词典的工作方式

ASD-STE100 的词典不是普通词典，而是**写作许可清单**。

| 列 | 内容 |
|---|---|
| Word (part of speech) | 词 + 批准词性；大写表示批准词，小写表示不批准词 |
| Approved meaning / replacement | 批准含义，或不批准词对应的替换建议 |
| STE example | 合规例句 |
| Non-STE example | 不合规例句 |

核心数据（Issue 9）：

- 官方公开概述：约 **900** 个批准词、约 **1,200** 个不批准词。
- Issue 9 的精确计数常被引为 **875** 个批准词、**1,274** 个不批准词；引用精确数字时应以官方 PDF 为准。
- 每个批准词通常只有一个批准含义、一个批准词性。
- 拼写采用**美式英语**。
- 词典不收部件名、材料名、工具名、工序名、公司专有术语——这些走"技术名词/技术动词"通道。

## 2. 一词一义一词性

这是 STE 的地基。同一个词不能今天当名词、明天当动词；不能今天表"关闭"、明天表"靠近"。

| 词 | 批准情况 | 错误用法 | 正确用法 |
|---|---|---|---|
| `start` | 动词，开始 | `commence / begin / initiate` | `Start the procedure.` |
| `close` | 动词，关闭 | `close to the landing gear`（表靠近） | `Do not go near the landing gear.` |
| `fall` | 动词，受重力下落 | `The pressure falls.`（表减少） | `The pressure is lower.` |
| `follow` | 动词，come after | `Follow the safety rules.`（表 obey） | `Do the safety rules.` |
| `test` | 名词，测试 | `Test the system.` | `Do a test of the system.` 或 `Do the leak test.` |
| `check` | 名词，检查 | `Check the valve.` | `Do a check of the valve.` |
| `dim` | 形容词，暗的 | `Dim the lights.` | `Set the lights to the dim position.` |

> 上表中的"错误/正确"用于说明机制，不构成完整词典条目。实际写作必须查 Issue 9 词典确认。

## 3. 常见替换表

> 以下是公开资料中反复出现的替换做法，用于快速起步。**最终以 Issue 9 词典为准**；不同 Issue 的批准状态可能变化。

| 不推荐 / 未批准 | 优先使用 | 说明 |
|---|---|---|
| begin, commence, initiate, originate | start | 只保留一个"开始" |
| ensure, verify, confirm | make sure | `make sure that ...` |
| prior to | before | 介词简化 |
| utilize, leverage | use | 删除商业腔 |
| approximately | about | 口语化简短词 |
| sufficient | enough | |
| additional | more | |
| obtain | get | |
| assist, facilitate | help | |
| perform, carry out, accomplish | do | |
| terminate, cease | stop | |
| implement | do | `do the procedure` |
| may（表可能/许可） | can | 避免模糊情态 |
| should, shall（表要求） | must | 要求用 must，建议需明确条件 |
| however | but | 拆句或转折 |
| therefore | thus | 或拆成因果两句 |
| e.g. | for example | 不用拉丁缩写 |
| i.e. | that is | |
| etc. | and so on | 或直接列完 |
| hook up | connect | 不用短语动词 |
| check (v.) | do a check of | check 常只批准作名词 |
| test (v.) | do a test of | test 常只批准作名词 |

## 4. 词性陷阱清单

以下词在公开资料中反复被指出"只批准某一种词性"：

- `check`：名词 → `do a check of`
- `test`：名词 → `do a test of` / `do the leak test`
- `damage`：名词 → `cause damage to`
- `cover`：名词 → `install the cover`
- `oil`：名词 → `apply oil to`
- `dim`：形容词 → `set to the dim position`
- `close`：动词 → `close the valve`
- `fall`：动词，仅"下落" → 不表"减少"

写作时的自检问题：**这个词在句子里是什么词性？词典批准这个词性吗？**

## 5. 语法限制

| 维度 | 允许 | 禁止 / 限制 | 示例 |
|---|---|---|---|
| 动词形式 | 不定式、祈使式、一般现在、一般过去、一般将来（will） | 完成时、进行时、复杂助动词结构 | ✗ `has been adjusted` → ✓ `adjust` |
| 过去分词 | 只作形容词 | 作谓语构成完成时/被动复杂结构 | ✓ `the installed filter` |
| 语态 | 程序：主动 + 祈使；描述：优先主动 | 程序中的被动；描述中施动者已知时的被动 | ✗ `The bolts must be removed.` → ✓ `Remove the bolts.` |
| 情态动词 | `can`（能力/可能）、`must`（要求） | `may / might / could / should` 表模糊可能或建议 | ✗ `The valve may open.` → ✓ `The valve can open.` |
| `-ing` 形式 | 技术名词或其修饰语 | 作动词、作从句谓语 | ✗ `Before installing the unit, ...` → ✓ `Before you install the unit, ...` |
| 冠词 | 保留 `a / an / the` | 为缩短而省略 | ✗ `Remove cover.` → ✓ `Remove the cover.` |
| 连接词 `that` | 保留 | 为缩短而省略 | ✓ `Make sure that the valve is closed.` |
| 缩写形式 | `do not`、`cannot`、`it is` | `don't`、`can't`、`it's` | |
| 拉丁缩写 | `for example`、`that is` | `e.g.`、`i.e.`、`etc.` | |
| 代词 | `the operator`、`the technician`、复数 | `he / she` 作通用指代 | |
| 标点 | 标准英文标点 | 分号；em/en dash 连接独立句 | |
| 句长 | 程序 ≤ 20 词；描述 ≤ 25 词 | 超长句 | |
| 段落 | ≤ 6 句，一段一主题 | 多主题长段 | |
| 名词簇 | ≤ 3 词 | 4 个以上名词连用 | |

## 6. 技术名词与技术动词

### 6.1 定义

- **技术名词（technical noun）**：项目、行业、公司特有的部件、系统、材料、工具、软件、角色、法规等名称。
- **技术动词（technical verb）**：项目或行业特有的操作，如 `deploy`、`merge`、`rebase`、`torque`、`calibrate`。

Issue 9 用这两个术语替代旧称 "technical names / technical verbs"，并与 ISO 1087-1:2019 对齐。

### 6.2 使用条件

1. 来自**项目术语表、工程图、官方文件、术语数据库**，不能临时发明。
2. 必须作**名词**或**动词**使用，不能当形容词或副词滥用。
3. 技术名词**不能当动词**用（Rule 1.7）：写 `apply oil to the valve`，不写 `oil the valve`。
4. 技术动词**不能当名词**用（Rule 1.13）。
5. 全文**写法一致**；同一对象不能有多个技术名词（Rule 1.11）。
6. 首次出现时，读者能通过上下文或术语表确定其含义。
7. 尽量限制数量；技术名词不是规避词典的"后门"。

### 6.3 分类

- 技术名词按主题领域分为 **22 类**（Issue 9）。类别覆盖官方零件信息、车辆/机器及其位置、工具与保障设备、材料、设施、系统与部件、数学与科学、导航、数字与单位、引用文本、角色与组织、人体部位、医疗、文档、环境条件、颜色、损伤、计算机与 ICT、民事/军事操作、法律法规、动植物等；Issue 9 新增 "Law and regulations" 和 "Animals, plants, and other life forms" 两类。完整清单见 **Rule 1.5**。
- 技术动词分为 **4 类**：制造工艺（`drill`、`weld`、`anneal`）、计算机操作（`click`、`boot`、`download`）、特定领域操作说明（`taxi`、`hover`）、法律法规（`comply with`、`waive`）；完整清单见 **Rule 1.12**。

### 6.4 术语表示例

| 技术名词 | 批准写法 | 禁止写法 |
|---|---|---|
| 液压泵 | `hydraulic pump` | `hyd. pump`、`HP`（未定义缩写） |
| 前起落架 | `nose landing gear` | `front gear`、`NLG`（首次未给全称） |
| 连接器 | `connector J1` | `plug`、`jack` 混用 |

## 7. 安全说明的语言

```text
WARNING: DO NOT TOUCH THE EXHAUST DUCT. THE SURFACE IS HOT AND CAN CAUSE BURNS.
CAUTION: DO NOT USE WATER ON THE ELECTRICAL PANEL. WATER CAN DAMAGE THE CONNECTORS.
NOTE: The test takes about 5 minutes.
```

规则：

- `WARNING` = 人身伤害/死亡；`CAUTION` = 设备损坏；`NOTE` = 仅信息。
- 标签大写；正文大小写按公司样式指南，STE 示例通常全大写。
- 安全说明放在受影响步骤**之前**。
- 先命令/条件，再原因/后果。
- `NOTE` 中不得写指令。

## 8. 常见错误 Top 12

1. `ensure` / `verify` / `confirm` 混用 → `make sure`。
2. `check` / `test` 当动词 → `do a check/test of`。
3. 名词簇 4 词以上 → 用介词拆。
4. 程序句超过 20 词 → 拆步。
5. 描述句超过 25 词 → 拆句。
6. 一句两个指令 → 拆成两步。
7. 条件放在指令后面 → 前置。
8. 警告放在步骤后面 → 前置。
9. 用分号连接两个句子 → 拆句。
10. 为缩短删冠词/主语 → 补回。
11. 同义词轮换 → 固定一个词。
12. 把 `CAUTION` 用于人身风险 → 改 `WARNING`。

## 9. 自检问句

写完每句，问自己：

1. 这个词是批准词、技术名词、技术动词，还是不可改字面量？
2. 词性和词义都对吗？
3. 这句话有几个指令？是否超过句长？
4. 条件和风险在动作之前吗？
5. 施动者明确吗？
6. 同一对象和前文叫法一致吗？
7. 删掉一个词，技术信息会丢吗？会，就别删。
