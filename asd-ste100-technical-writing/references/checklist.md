# 质量检查清单

## 0. 使用方式

交付前做三遍检查，不要合并：

1. **机械检查**：句长、禁用字符、禁用形式。可以用脚本或 grep。
2. **语言检查**：词性、词义、语态、时态、名词簇、冠词。
3. **技术检查**：含义是否改变、条件/警告是否丢失、术语是否一致。

每项标记 `PASS / FAIL / N/A`。`FAIL` 必须修复，或在"待确认清单"中说明原因和责任人。

## 1. 机械检查

| # | 检查项 | 方法 | 通过标准 |
|---|---|---|---|
| M1 | 程序句 ≤ 20 词 | 分词计数 | 每条指令 ≤ 20 |
| M2 | 描述句 ≤ 25 词 | 分词计数 | 每句 ≤ 25 |
| M3 | 无分号 | 搜索 `;` | 0 处 |
| M4 | 无 em/en dash 连接独立句 | 搜索 `—`、`–` | 0 处（复合词连字符 `-` 不算） |
| M5 | 无 `-ing` 动词 | 搜索 `\b\w+ing\b` + 人工排除 | 0 处违规 |
| M6 | 无完成时 | 搜索 `has/have/had + 过去分词` | 0 处 |
| M7 | 无进行时 | 搜索 `is/are/was/were + -ing` | 0 处 |
| M8 | 无缩写形式 | 搜索 `don't/can't/won't/isn't/it's` 等 | 0 处 |
| M9 | 无拉丁缩写 | 搜索 `e.g. / i.e. / etc.` | 0 处 |
| M10 | 名词簇 ≤ 3 词 | 人工或词性标注脚本 | 0 处超长 |
| M11 | 段落 ≤ 6 句 | 计数 | 0 段超长 |
| M12 | 程序句以祈使动词开头 | 逐条检查 | 100% |
| M13 | 条件在动作之前 | 逐条检查 | 100% |
| M14 | 无 `he/she` 通用指代 | 搜索 | 0 处 |

### 1.1 快速搜索

```bash
# 分号
grep -nE ";" file.md

# em/en dash
grep -nE "—|–" file.md

# 缩写形式
grep -niE "\b(don't|doesn't|didn't|can't|won't|isn't|aren't|wasn't|weren't|it's|that's|we'll|you'll)\b" file.md

# 拉丁缩写
grep -niE "\b(e\.g\.|i\.e\.|etc\.)" file.md

# 完成时（含常见不规则过去分词）
grep -niE "\b(has|have|had)\s+([a-z]+ed|been|done|made|set|put|given|taken|shown|found|got|gotten|written|built|sent|kept|left|held|brought|thought|known|grown|drawn|driven|broken|chosen|spoken|stolen|worn|torn|born)\b" file.md

# 进行时
grep -niE "\b(is|are|was|were)\s+[a-z]+ing\b" file.md

# 模糊情态
grep -niE "\b(may|might|could|should)\b" file.md
```

### 1.2 句长计数

按句号、问号、感叹号、列表项切句；标题、标牌、引用文本按一个词计；代码块和行内代码不计数。

```python
import re

def word_count(sentence: str) -> int:
    # 行内代码按 1 个词计
    text = re.sub(r"`[^`]*`", " CODE ", sentence)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'./:_-]*", text))
```

判定：

- 程序文本：`word_count <= 20`
- 描述文本：`word_count <= 25`
- 超限：拆句、拆步、改列表。

## 2. 逐句判断检查

| # | 检查项 | 自检问题 | 不合格示例 | 修正 |
|---|---|---|---|---|
| J1 | 词性 | 这个词在句中是名词、动词还是形容词？词典批准这个词性吗？ | `Test the valve.` | `Do a test of the valve.` |
| J2 | 词义 | 用的是批准含义吗？ | `Follow the rules.`（表 obey） | `Do the rules.` |
| J3 | 一词一义 | 同一概念前文叫什么？这里换词了吗？ | `panel` / `console` 混用 | 统一为一个词 |
| J4 | 名词簇 | 连续名词超过 3 个了吗？ | `forward turbine overheat thermocouple terminal tags` | `the terminal tags on the forward overheat thermocouple` |
| J5 | 一句一指令 | 这句话让人做几件事？ | `Set the switch and release the button.` | 拆成两步 |
| J6 | 条件位置 | 读者动手前知道条件吗？ | `Do the test if the light is off.` | `If the light is off, do the test.` |
| J7 | 语态 | 谁做这个动作？ | `The bolts must be removed.` | `Remove the bolts.` |
| J8 | 时态 | 用了完成时/进行时吗？ | `The system has been tested.` | `The system is correct after the test.` 或 `Do the test.` |
| J9 | `-ing` | 是技术名词还是动词？ | `Before installing the unit, ...` | `Before you install the unit, ...` |
| J10 | 冠词 | 为缩短删了 `a/an/the` 吗？ | `Remove cover.` | `Remove the cover.` |
| J11 | 缩写 | 首次出现给全称了吗？ | `NLG` | `nose landing gear (NLG)` 首次，后文 `NLG` |
| J12 | 术语一致 | 同一部件全文同名吗？ | `hydraulic pump` / `hyd. pump` | 统一 |
| J13 | 可翻译性 | 去掉上下文后，这句还能只有一种译法吗？ | 多义词、代词指代不明 | 换成具体名词 |
| J14 | 读者视角 | 非母语读者需要回读吗？ | 长从句、嵌套条件 | 拆句 |

## 3. 安全说明专项

| # | 检查项 | 通过标准 |
|---|---|---|
| S1 | 级别正确 | 人身伤害/死亡 = `WARNING`；设备损坏 = `CAUTION`；信息 = `NOTE` |
| S2 | 位置正确 | 在受影响步骤之前 |
| S3 | 命令先行 | 第一句是明确的动作或禁止动作 |
| S4 | 后果具体 | 说清"会发生什么"，不用 `dangerous` 等空泛词 |
| S5 | `NOTE` 无指令 | `NOTE` 中不出现 `do / remove / install / make sure` 等指令 |
| S6 | 不弱化 | 不把人身风险写成 `CAUTION`，不把 `must` 改成 `should` |
| S7 | 不夸大 | 不加 `EXTREME`、`CRITICAL` 等无法验证的强调词 |

## 4. 不可改清单

改写前先列出来，交付前逐项核对：

- [ ] 代码块、行内代码
- [ ] 命令、参数、flag
- [ ] 文件路径、URL
- [ ] 变量名、函数名、类名、API 名
- [ ] 错误串、日志片段
- [ ] 数字、单位、公差、扭矩值
- [ ] 日期、版本号
- [ ] UI 标签、按钮文字
- [ ] 法规、合同、认证原文
- [ ] 直接引用（保持原话）

核对标准：**逐字一致**，包括大小写、空格、标点。

## 5. 交付模板

```markdown
## 改写稿

<改写后的英文文本>

## 变更说明

| # | Before | After | 触发的规则 | 理由 |
|---|---|---|---|---|
| 1 | Prior to carrying out ... | Disconnect ... | 1.1 / 3.4 / 5.2 | 去同义词、去被动完成时、一句一指令 |

## 待确认

- [ ] 术语 `XXX` 是否为企业批准技术名词？
- [ ] `30 seconds` 是否为该型号的默认超时？
- [ ] 法规段落是否允许改写？

## 合规声明

本稿按 ASD-STE100 Issue 9 的写作规则改写，未经 ASD/STEMG 认证。
```

## 6. 交付判定

| 结论 | 条件 |
|---|---|
| **可以交付** | 机械项全部 PASS；判断项无高危未解决项；不可改清单零改动 |
| **有条件交付** | 存在低风险待确认项，已逐条标注并说明影响 |
| **不可交付** | 技术含义改变；警告/限制丢失；伪造"官方合规"声明；不可改内容被改写 |

高危项（任一出现即不可交付）：

- 安全说明级别错误或位置错误。
- 条件、例外、失败处理被删除。
- 数字、单位、扭矩值、版本号被改动。
- 把"可能"改成"必须"或反之。
- 声称"通过 ASD-STE100 认证/完全合规"。

## 7. 常见误报

- `during`、`opening`、`remaining`、`setting`、`binding` 等可能是批准词或技术名词，不应被 `-ing` 规则误杀。
- 代码块、命令、引用原文不参与检查。
- 被动语态在描述文本中、施动者未知时是允许的。
- 两个动作确实同时发生时，可以同句。
- 标题、标牌、引用文本按一个词计，不按普通句长判断。
- 技术名词可能很长，但作为一个整体名称使用时不按名词簇规则拆。
