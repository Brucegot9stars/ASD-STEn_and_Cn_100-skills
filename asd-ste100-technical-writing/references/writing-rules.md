# ASD-STE100 Issue 9 写作规则结构

## 0. 使用说明

- 官方计数：**53 条写作规则，分 9 节**。各节条数为 14 / 3 / 7 / 4 / 5 / 6 / 3 / 7 / 4。
- 本文件是**执行摘要**，不是标准原文。完整条文、定义和例外以 ASD-STE100 Issue 9 官方 PDF 为准。
- 标 † 的规则编号来自公开培训材料和研究论文中的示例，引用前请核对官方原文。
- 规则不能脱离词典单独使用：词汇合法性由词典判定，规则负责把合法词汇组织成受控散文。

## 1. 九节总览

| 节 | 名称 | 条数 | 管什么 | 关键硬约束 |
|---|---|---:|---|---|
| 1 | Words（词） | 14 | 词的选择、词性、词义、技术名词/动词、拼写 | 只用批准词；按批准词性和批准含义使用；一词一义 |
| 2 | Multi-word nouns（名词簇） | 3 | 多个名词连用 | 名词簇 ≤ 3 词；超长用介词拆开 |
| 3 | Verbs（动词） | 7 | 动词形式、助动词、语态、情态 | 只用简单时态；程序用主动+祈使；描述被动受限 |
| 4 | Sentences（句子） | 4 | 句长、句子信息量、列表、连接 | 短句；一句一意；复杂内容用竖列表 |
| 5 | Procedural writing（程序性写作） | 5 | 步骤、指令、顺序、条件 | 祈使句；一句一指令；条件前置 |
| 6 | Descriptive writing（描述性写作） | 6 | 说明、原理、功能、结构 | 描述句 ≤ 25 词；一段一主题；逻辑顺序 |
| 7 | Safety instructions（安全说明） | 3 | 警告、注意、提示 | 级别正确；位置在步骤前；先命令后原因 |
| 8 | Punctuation and word count（标点与字数） | 7 | 标点、列表、词数计算 | 不用分号；不用破折号连接独立句 |
| 9 | Writing practices（写作实践） | 4 | 一致性、完整性、技术准确 | 同一事物同一名称；不删必要信息 |

## 2. 高频规则与示例

| 规则 | 要求 | 违例 | 改法 |
|---|---|---|---|
| 1.1 | 只用词典批准词 | `Commence the procedure.` | `Start the procedure.` |
| 1.2 † | 按词典给的词性使用 | `Dim the lights.`（dim 只批准作形容词） | `Set the lights to the dim position.` |
| 1.3 † | 按词典给的批准含义使用 | `Follow the safety instructions.`（follow 的批准义是 come after，不表 obey） | `Do the safety instructions.` |
| 2.1 † | 名词簇 ≤ 3 词 | `Install the forward turbine overheat thermocouple terminal tags.` | `Install the terminal tags on the forward overheat thermocouple of the turbine.` |
| 3.4 † | 不用助动词构成复杂动词结构 | `The temperature must be adjusted.` | `Adjust the temperature.` |
| 4.3 † | 复杂内容用竖列表 | `The wheel assembly comprises the tire, the tube, the spokes, the spoke fittings, the valve, and the hub.` | `The wheel assembly has these parts:` + 竖排各项 |
| 5.2 † | 一句一指令，除非动作同时发生 | `Set the TEST switch to the middle position and release the SHORT-CIRCUIT TEST switch.` | 拆成两步：`1. Set ...` / `2. Release ...` |
| 6.3 † | 描述句 ≤ 25 词 | 一句塞入多个条件、原因、结果 | 拆成 2–3 个短句，按因果顺序排列 |
| 7.1 † | 用 warning / caution 标明风险级别 | 对人身伤害风险使用 `CAUTION` | 改为 `WARNING`，并说明后果 |
| 8.1 † | 可用标准标点，但不用分号 | `Users cannot replace the battery; only approved service stations can replace it.` | 拆成两句：`Users cannot replace the battery. Only approved service stations can replace it.` |
| 9.4 † | 术语和措辞保持一致 | 同一部件在 3 页叫 `panel`，在 300 页叫 `console` | 全文统一为一个名称，并在术语表登记 |

## 3. 分节执行要点

### 3.1 Words（14 条）

- 先查词典，再写作；不要凭语感判断"这个词应该可以"。
- 一个词只用一个批准含义、一个批准词性；词典里大写词是批准词，小写词是不批准词。
- 技术名词、技术动词是唯一合法的词典外词汇通道，但必须来自项目术语表/图纸/官方文件，并全文一致。
- Issue 9 把旧称 "technical names" 改为 **technical nouns**，并与 ISO 1087-1:2019 的术语分类对齐。
- 技术名词按主题领域分类（Issue 9 共 22 类，含新增的 "Law and regulations"、"Animals, plants, and other life forms"）；技术动词按 4 类划分。完整清单见 Rule 1.5 与 Rule 1.12。
- 拼写用美式英语。
- 不用缩写形式、拉丁缩写、性别代词、隐喻、习语、短语动词。
- `-ing` 形式只允许作技术名词或其修饰语。

### 3.2 Multi-word nouns（3 条）

- 名词簇上限 3 词；4 个以上名词连用会让读者猜关系。
- 拆分手段：介词（`of / on / in / for`）、所有格、关系从句、冠词。
- 优先保留"中心词 + 介词短语"的结构，而不是把所有限定词堆在中心词前。
- 超过 3 词的技术名词：第一次写全称，之后用短名或连字符组合（`pressure-relief valve`），不要每次重复全称；不要把长技术名词硬拆成语义不明的碎片。

### 3.3 Verbs（7 条）

- 允许的形式：不定式、祈使式、一般现在时、一般过去时、一般将来时（`will`）。
- 过去分词只作形容词：`the changed file`、`the installed filter`。
- 禁止完成时、进行时、复杂助动词结构。
- 程序：主动语态 + 祈使句，施动者明确。
- 描述：优先主动；只有施动者未知或不重要时才用被动。
- 情态动词按词典批准义使用；不要用情态动词堆叠表达不确定性。
- 不用 `-ing` 从句代替完整句子。

### 3.4 Sentences（4 条）

- 程序句 ≤ 20 词；描述句 ≤ 25 词。
- 一句一个主要意思；不要把条件、动作、结果、原因全塞进一句。
- 条件前置：`If the pressure is more than 3000 psi, the valve opens.`
- 三个以上同类项、连续步骤、复杂并列：用竖列表。
- 用 `then / because / but / so` 明确句子关系。

### 3.5 Procedural writing（5 条）

- 每条指令以祈使动词开头。
- 一句一指令；同时发生的动作可同句，但必须明确"同时"。
- 按执行顺序编号；不要跳步、并步。
- 一步一个主要动作；不要把"检查、拆卸、安装、测试"写进同一步。
- 条件、位置、风险放在动作之前，或单独列为前置条件。
- 不把关键限制放在步骤末尾的括号里。

### 3.6 Descriptive writing（6 条）

- 描述句 ≤ 25 词。
- 一段一个主题，最多 6 句；主题句先行。
- 按因果、时间或空间顺序组织信息。
- 先给结论/功能，再给细节、条件、例外。
- 不写修辞、比喻、拟人、营销形容词。
- 把模糊表述改成可检查的事实：`runs smoothly` → `all pods show the status Running`。

### 3.7 Safety instructions（3 条）

- `WARNING`：人身伤害或死亡风险。
- `CAUTION`：设备、工具或财产损坏风险。
- `NOTE`：仅信息，不含指令。
- 位置：放在受影响步骤之前。
- 结构：先命令/条件，再原因/后果。
- 级别要与后果匹配；不要把人身风险降级为 `CAUTION`。

### 3.8 Punctuation and word count（7 条）

- 标准英文标点可用，但**不用分号**。
- 不用 em dash / en dash 连接两个独立意思；拆句。
- 连字符用于复合词、标识符、单位。
- 列表用冒号引导；步骤编号。
- 统计句长时，标题、标牌、引用文本按一个词计；数字 + 单位算一个词（Issue 9：`10 °C`、`10 degrees Celsius`、`10 in.` 都算 1 个词）。
- 数字、单位、符号按公司样式指南和标准写法；不改写其值。
- 代码、命令、路径按字面量处理，不参与改写。

### 3.9 Writing practices（4 条）

- 同一部件、动作、状态全文同一名称。
- 不为了缩短而删除冠词、主语、限定词、条件、例外。
- 不改变技术含义；STE 不是技术评审的替代品。
- 不为了"读起来顺"而换词；重复是受控语言的特征。
- 另有 **8 条 general recommendations（GR-1–GR-8）**，性质是建议而非写作规则；不要把 GR 计入 53 条。

## 4. 完整改写示例

### 4.1 程序段

**Before**

> Prior to carrying out the lubrication procedure, ensure that the power supply has been isolated.

**After**

> 1. Disconnect the power supply.
> 2. Lubricate the bearing.

**改动**

- `Prior to` → `before` 结构，直接拆成顺序步骤。
- `carrying out` → `do` 的语义，改为具体动作 `Lubricate`。
- `ensure that ... has been isolated` → 被动完成时改为主动祈使 `Disconnect`。
- 一句一指令，条件（断电）在动作（润滑）之前。

### 4.2 描述段

**Before**

> It looks like the issue you are experiencing is most likely related to connection pool exhaustion. Essentially, when your application receives a sudden spike in traffic, the pool may become saturated, causing subsequent requests to wait for an available connection until they eventually time out.

**After**

> The pool has 10 connections. When traffic increases, all 10 connections are in use. New requests wait for a free connection. After 30 seconds, these requests fail. Slow queries make the problem worse. They keep a connection for a long time.

**改动**

- 删除 `It looks like`、`most likely`、`Essentially` 等软化语。
- 一句一个事实，按事件发生顺序排列。
- `eventually time out` 改为可检查的 `After 30 seconds, these requests fail`。
- 每句 ≤ 25 词。

### 4.3 安全说明

**Before**

> CAUTION: EXTREME CLEANLINESS OF OXYGEN TUBES IS IMPERATIVE.

**After**

> WARNING: MAKE SURE THAT THE OXYGEN TUBES ARE FULLY CLEAN. OXYGEN AND GREASE MAKE AN EXPLOSIVE MIXTURE. AN EXPLOSION CAN CAUSE INJURY OR DEATH.

**改动**

- 风险涉及人身伤害，级别从 `CAUTION` 升为 `WARNING`。
- 先命令（确保清洁），再原因（氧气+油脂爆炸），再后果（伤亡）。
- 删除 `EXTREME`、`IMPERATIVE` 等无法验证的强调词。

### 4.4 词性陷阱

**Before**

> Test the system for leaks.

**After**

> Do the leak test of the system.

**说明**

- `test` 在词典中批准为名词，不批准作动词；改为 `do the ... test`。
- 同类常见词：`check`、`damage`、`cover`、`oil`。使用前查词典确认词性。

## 5. 引用边界

- 不要写"符合 ASD-STE100"或"通过 STE 认证"，除非有正式合规评审。
- 可以写"按 ASD-STE100 Issue 9 的写作规则改写"。
- 规则编号引用必须核对官方原文；本文件的 † 标记项仅作公开示例。
- 标准版权归 ASD 所有；本文件是执行摘要，不复制标准正文。
