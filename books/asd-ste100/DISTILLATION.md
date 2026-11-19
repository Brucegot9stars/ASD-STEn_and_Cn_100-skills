# ASD-STE100 蒸馏记录（cangjie-skill / single 模式）

> 来源类型：网络权威资料集（官方标准说明、ASD/STEMG FAQ、AI 白皮书、行业媒体、学术论文、培训材料）。
> 蒸馏日期：2026-11-19。
> 输出模式：single（1 个入口 + 1 张能力卡 + 4 个参考文件）。

## 阶段 0 — 整体理解（Adler 四步）

### 0.1 结构

ASD-STE100 不是一本"写作技巧书"，而是一套**受控自然语言标准**，由两个互相咬合的部分组成：

1. **53 条写作规则 / 9 节**：管词、名词簇、动词、句子、程序、描述、安全说明、标点、写作实践。
2. **受控词典**：约 900 个批准词（一词一义一词性）+ 约 1200 个不批准词及替换建议。

规则负责"怎么组织"，词典负责"能用什么"。缺任何一半都不成立。

### 0.2 解释

STE 的核心不是"把英语写简单"，而是**消除解释空间**：

- 一个词只有一个批准含义、一个批准词性 → 读者不用猜。
- 一句只下一个指令 → 执行者不会漏步。
- 条件和警告放在动作之前 → 读者动手前已经知道风险。
- 同一事物全文同名 → 翻译、检索、培训都不产生歧义。

它服务的是**高风险、跨语言、多人协作的技术文档**，尤其是非英语母语的维修、操作、装配人员。

### 0.3 批判

- 规则和词典只保证"语言受控"，**不保证技术内容正确**。清晰但错误的指令仍然是错误指令。
- STE 文本读起来重复、生硬，这是设计代价，不是缺陷。
- 标准本身不认证文本、不认证工具；第三方"完全合规"声明不可信。
- 完整词典和 53 条原文不公开在网页上，只存在于官方 PDF；本 skill 只能做执行摘要，不能替代逐词查典。
- 行业收益数据多来自标准方/培训商，缺少独立第三方研究，引用时需标注来源性质。

### 0.4 应用

最适合：维修手册、工卡、安装/拆卸/调试步骤、SOP、运行手册、安全警告、翻译前源文本、LLM 输出约束。
不适合：营销、法律原文、文学、对话式文档、纯中文写作。

## 阶段 1 — 五类候选提取

### 1.1 框架提取

| 候选 | 内容 | 来源 |
|---|---|---|
| F1 双层结构 | 写作规则 + 受控词典 | 官方 About |
| F2 文本二分 | 程序性 vs 描述性，句长/语态规则不同 | 官方/培训材料 |
| F3 分层改写 | 词 → 名词簇 → 动词 → 句子 → 段落 → 安全 → 标点 | 规则节顺序 |
| F4 安全说明结构 | 级别 + 位置 + 命令先行 + 后果 | Rule 7 系列 |
| F5 术语治理 | 企业术语表 + 技术名词/动词 + 一致性 | 官方/实施资料 |

### 1.2 原则提取

| 候选 | 内容 |
|---|---|
| P1 | 一词一义一词性 |
| P2 | 一句一指令 |
| P3 | 程序句 ≤ 20 词；描述句 ≤ 25 词 |
| P4 | 名词簇 ≤ 3 词 |
| P5 | 段落 ≤ 6 句，一段一主题 |
| P6 | 程序用主动 + 祈使；描述被动受限 |
| P7 | 只用简单时态；过去分词只作形容词 |
| P8 | 条件、警告、风险前置 |
| P9 | 术语一致，禁止同义轮换 |
| P10 | 不删冠词、主语、限定词；不改变技术含义 |
| P11 | 不用分号；不用破折号连接独立句 |
| P12 | WARNING/CAUTION/NOTE 级别与位置 |
| P13 | 技术名词/动词只能用项目既有术语，不能临时发明 |

### 1.3 案例提取

| 候选 | 内容 | 类型 |
|---|---|---|
| C1 | `Prior to ... ensure ... has been isolated` → `Disconnect ... before you ...` | 公开示例 |
| C2 | `Set the switch and release the button` → 两步 | 公开示例（Rule 5.2） |
| C3 | `forward turbine overheat thermocouple terminal tags` → 介词拆分 | 公开示例（Rule 2.1） |
| C4 | `CAUTION: EXTREME CLEANLINESS ...` → `WARNING: ... CAN CAUSE INJURY OR DEATH` | 公开示例（Rule 7.1） |
| C5 | `Users cannot replace the battery; ...` → 拆两句 | 公开示例（Rule 8.1） |
| C6 | `Test the system for leaks.` → `Do the leak test of the system.` | 公开示例（Rule 1.2） |

### 1.4 反例提取

| 候选 | 失败模式 |
|---|---|
| N1 | 把 STE 当"baby English"或可读性评分 |
| N2 | 只换简单词，不查批准词性/词义 |
| N3 | 把建议（recommend/should）改成命令（must），升级确定性 |
| N4 | 为缩短删冠词、主语、条件、例外 |
| N5 | 把警告放在步骤之后，或级别降级 |
| N6 | 用技术名词当"后门"，临时发明术语 |
| N7 | 依赖检查工具，认为工具通过 = 合规 |
| N8 | 相信 AI 生成文本"看起来像 STE" |
| N9 | 把 STE 用在营销、法律、文学文本 |
| N10 | 把 STE 文本"润色"回普通英语，破坏受控性 |

### 1.5 术语提取

| 术语 | 含义 |
|---|---|
| Controlled natural language | 受控自然语言：限制词汇和语法，降低歧义 |
| Approved word | 词典批准词，通常一词一义一词性 |
| Technical noun | 项目/行业特有名词，来自术语表/图纸/官方文件 |
| Technical verb | 项目/行业特有动词，如 deploy、torque |
| Procedure | 程序性文本：步骤、指令 |
| Description | 描述性文本：功能、结构、原理 |
| Noun cluster | 连续名词组合，上限 3 词 |
| WARNING / CAUTION / NOTE | 人身风险 / 设备风险 / 纯信息 |
| Issue | 标准版本，当前 Issue 9（2025-01） |

## 阶段 1.5 — 三重验证

| 单元 | V1 来源充分 | V2 可执行 | V3 任务增益 | 判定 | 去向 |
|---|---|---|---|---|---|
| 双层结构 | ✓ 官方 | ✓ | ✓ 决定工作流 | verified | SKILL §1、§5 |
| 一词一义一词性 | ✓ 官方 | ✓ | ✓ 核心 | verified | SKILL §4.1；vocab §2 |
| 名词簇 ≤ 3 | ✓ 官方+培训 | ✓ | ✓ | verified | SKILL §4.2；rules §3.2 |
| 动词形式限制 | ✓ 官方 | ✓ | ✓ | verified | SKILL §4.3；vocab §5 |
| 句长 20/25 | ✓ 多方一致 | ✓ | ✓ | verified | SKILL §4.4；checklist M1/M2 |
| 一句一指令 | ✓ 官方+论文 | ✓ | ✓ | verified | SKILL §4.5 |
| 段落 ≤ 6 句 | ✓ 多方一致 | ✓ | ✓ | verified | SKILL §4.4 |
| 安全说明三级别 | ✓ 官方+论文 | ✓ | ✓ | verified | SKILL §4.7；checklist §3 |
| 标点（禁分号） | ✓ 论文+培训 | ✓ | ✓ | verified | SKILL §4.8 |
| 术语一致性 | ✓ 官方 | ✓ | ✓ | verified | SKILL §4.9 |
| 技术名词/动词 | ✓ 官方 | ✓ 需术语表 | ✓ | verified | SKILL §4.1；vocab §6 |
| 工具/AI 边界 | ✓ 官方白皮书 | ✓ | ✓ 防误用 | verified | SKILL §8；sources §5 |
| 历史与版本 | ✓ 官方 | — | 参考 | reference | sources §1 |
| 行业采用数据 | ✓ 官方分发日志 | — | 参考 | reference | sources §3 |
| 22 类技术名词 / 4 类技术动词 | ✓ 公开蒸馏+交叉 | ✓ | ✓ | verified（回炉后） | vocab §6.3 列类别与示例 |
| 53 条逐条原文 | 未获取完整正文 | 部分 | 高 | needs_review | rules §0 声明以官方 PDF 为准 |

**缺口处理**：分类清单在回炉后补齐并交叉验证；53 条逐条原文仍未获取，skill 明确"完整内容查官方 PDF"，只把可核实的高频规则做成执行摘要，不伪造条文。

## 阶段 1.6 — 晋级门

单一能力 `asd-ste100-technical-writing`：

| 判据 | 结果 | 理由 |
|---|---|---|
| 独立意图 | ✓ | 用户明确要求 STE 改写/写作/审计 |
| 独立契约 | ✓ | 输入文本类型、输出改写稿+变更说明+待确认 |
| 独立运行 | ✓ | 不依赖其他 skill，按 7 步流程执行 |
| 独立复用 | ✓ | 航空、汽车、医疗、IT 运维等多场景 |
| 独立评测 | ✓ | 可用句长、禁用形式、安全说明位置等客观检查 |

结论：**promoted**，输出 single 入口。

## 阶段 2 — RIA++ 能力卡

### R — 原文（Reading）

> The STE standard consists of a set of writing rules and a controlled dictionary. The writing rules focus on grammar and style. The dictionary contains the approved words that a writer can use and a list of words that are not approved with related alternative suggestions.
>
> — ASD/STEMG, *About ASD-STE100*, asd-ste100.org

### I — 方法论骨架（Interpretation）

STE 用两层约束把"技术英语"变成可预测的受控语言。第一层是词典：每个批准词只有一个含义、一个词性，同义表达被收敛到一个词。第二层是规则：短句、一句一指令、名词簇不超过三词、程序用祈使句、条件和警告前置、术语全文一致。写作时按"词 → 名词簇 → 动词 → 句子 → 段落 → 安全说明 → 标点"逐层收敛；每层只解决一类歧义。最终目标不是优美，而是让不同语言背景的读者对同一句话只有一种理解。技术名词和动词是唯一的合法扩展口，但必须来自项目术语表并全文一致。

### A1 — 应用示例

**示例 1（公开示例，Rule 5.2）**

- 输入：`Set the TEST switch to the middle position and release the SHORT-CIRCUIT TEST switch.`
- 方法：识别两个顺序动作 → 拆成两步 → 每步祈使句。
- 输出：
  ```
  1. Set the TEST switch to the middle position.
  2. Release the SHORT-CIRCUIT TEST switch.
  ```

**示例 2（合成演练，非官方样本）**

- 输入：`We recommend that you should verify that the hydraulic system has been properly bled before attempting to commence the removal of the pump, as failure to do so may potentially result in damage to the equipment.`
- 方法：识别"建议"而非命令 → 不升级为 must；去 `should/verify/commence/may potentially`；拆句；条件前置。
- 输出：
  ```
  Before you remove the pump, make sure that the hydraulic system is fully bled.
  If the hydraulic system is not fully bled, the pump can be damaged.
  ```
- 说明：原文是建议，改写保留建议强度；`fully bled` 的可验证标准需主题专家确认。

### A2 — 触发场景

1. 用户要改写维修/安装/调试步骤，要求"非母语读者一次读懂"。
2. 用户写 WARNING/CAUTION，要求级别正确、位置正确。
3. 用户要统一多份手册的术语。
4. 用户要在翻译前降低源文本歧义。
5. 用户要求"用 STE / 简化技术英语 / controlled English 写"。

语言信号：`ASD-STE100`、`STE`、`Simplified Technical English`、`简化技术英语`、`受控英语`、`controlled English`、`维修手册`、`工卡`、`安全警告`、`non-native readers`、`unambiguous instructions`。

### E — 可执行步骤

见 `.workbuddy/skills/asd-ste100-technical-writing/SKILL.md` 第 5 节：分类 → 锁定不可改 → 建术语表 → 分层改写 → 机械自检 → 语义复核 → 交付。

必需输入：待改文本、文本类型（程序/描述/安全）、目标读者、项目术语表（可选）、目标 Issue（默认 9）。
交付物：改写稿 + 变更说明表 + 待确认清单 + 非官方合规声明。

### B — 边界

- 不用于营销、法律原文、文学、对话式文档、纯中文。
- 不修正技术错误；不替代工程评审。
- 不认证、不声称"完全合规"。
- 不虚构词典批准状态；不伪造 53 条条文。
- 不改变确定性、不删条件/警告/例外。

## 阶段 3 — 链接

- `SKILL.md` ↔ `references/writing-rules.md`：规则总览与分节执行。
- `SKILL.md` ↔ `references/vocabulary-and-grammar.md`：词典机制与语法限制。
- `SKILL.md` ↔ `references/checklist.md`：交付前检查。
- `references/sources.md`：版本、来源、引用边界。
- 相邻方法论区分：Plain English（一般清晰，规则更松）、S1000D（管结构与数据模块，不管语言）、EARS（管需求句式，不管词汇）。

## 阶段 4 — 压力测试

### 4.1 触发测试

| 输入 | 期望 | 结果 |
|---|---|---|
| "帮我把这段维修步骤改成 STE" | 触发 | ✓ |
| "用简化技术英语写这个安装流程" | 触发 | ✓ |
| "写一段产品营销文案" | 不触发 | ✓ |
| "把这份合同改成简化英语" | 不触发（法律原文） | ✓ |
| "解释一下 Kubernetes" | 不触发（无 STE 信号） | ✓ |
| "用 STE 风格解释这个报错" | 触发（输出约束场景） | ✓ |

### 4.2 输出测试

用例：把一段含建议、被动完成时、模糊情态、长句的文本改写为 STE。

- 第一版错误：把 `We recommend` 改成命令 `Bleed the hydraulic system.`，**升级了确定性**。
- 按 B 段"不改变确定性"回炉：保留建议语气，改为 `Before you remove the pump, make sure that ...`，并在待确认中标注"原文为建议，是否升级为强制步骤需确认"。
- 机械检查：最长句 19 词；无分号；无完成时；无 `-ing` 动词；名词簇 ≤ 3。
- 判断检查：`make sure`、`before`、`remove`、`pump`、`hydraulic system` 均为批准词/技术名词；`fully bled` 标为待确认技术条件。
- 结论：通过，但保留 1 项技术待确认。

### 4.3 安全检查测试

输入：`CAUTION: High voltage. Can cause injury.`
输出：`WARNING: HIGH VOLTAGE. CONTACT CAN CAUSE INJURY OR DEATH.`
判定：人身风险从 `CAUTION` 升为 `WARNING`，正确；后果具体化；命令/条件在前。

## 阶段 5 — 覆盖审计

| 原资料关键任务 | 是否覆盖 | 去向 |
|---|---|---|
| 定义与性质 | ✓ | SKILL §1；sources §1 |
| 历史与治理 | ✓ | sources §1、§2 |
| 适用范围 | ✓ | SKILL §2、§3 |
| 53 条规则结构 | ✓（摘要） | writing-rules §1–§3 |
| 词汇限制 | ✓ | vocabulary §1–§4 |
| 语法限制 | ✓ | vocabulary §5 |
| 安全说明 | ✓ | SKILL §4.7；checklist §3 |
| 应用场景 | ✓ | SKILL §3；sources §4 |
| 常见注意事项 | ✓ | SKILL §8；DIGEST |
| 工具与 AI 边界 | ✓ | SKILL §8；sources §5、§6 |
| 版本与引用 | ✓ | sources §1、§5 |
| 53 条逐条原文 | 部分 | needs_review；指向官方 PDF |
| 22/4 类完整清单 | ✓ | vocab §6.3 |

## 质量红线自检

| 红线 | 结果 |
|---|---|
| 能力通过三重验证 | ✓（1 项标 needs_review，未伪装为完整） |
| 能力卡 R/I/A1/A2/E/B 完整 | ✓（本文档阶段 2） |
| 原文引用 ≤100 词 | ✓（R 段约 47 词） |
| 单一去向 | ✓ promoted |
| description 含触发与不触发 | ✓ SKILL frontmatter |
| 不伪造原文/编号 | ✓ 标 † 与"以官方 PDF 为准" |
| 覆盖有可追溯去向 | ✓ 阶段 5 |
| 明确非官方、不认证 | ✓ SKILL §6、sources §5 |
