# ASD-STE100 精华：让技术文档只有一种读法

## 一句话

ASD-STE100 是一套**受控英语标准**：用 53 条写作规则和一本约 900 个批准词的受控词典，把技术文档压缩到"每个词只有一个意思、每句话只有一个指令"。

## 它解决的不是"英语难"，是"读错"

1979 年，欧洲航空公司向飞机制造商提了一个要求：维修手册必须写成非英语母语机修工也能一次读对的样子。当时的文档混着美式英语、英式英语和非母语者写的英语，同一个部件有三四个叫法，一句话能读出两个意思。

在别的行业，这是沟通成本；在飞机维修里，这是事故。

所以 STE 的起点不是"让文字更优美"，而是**降低人为差错风险**。它后来被 ATA iSpec 2200、ATA 104、S1000D、EASA/FAA/CAAC 的持续适航要求引用，也从航空扩散到国防、汽车、铁路、医疗器械、制药、能源和 IT 运维。

## 两部分，缺一不可

**写作规则（53 条 / 9 节）** 管"怎么组织"：

- 程序句 ≤ 20 词，描述句 ≤ 25 词。
- 一句一个指令。
- 名词簇 ≤ 3 词。
- 程序用主动语态 + 祈使句。
- 条件、警告放在动作之前。
- 一段一个主题，最多 6 句。
- 不用分号。

**受控词典** 管"能用什么"：

- 约 900 个批准词，每个词通常只有一个含义、一个词性。
- 约 1200 个不批准词，附替换建议。
- `start` 取代 `begin / commence / initiate`。
- `make sure` 取代 `ensure / verify / confirm`。
- `before` 取代 `prior to`。
- `test`、`check` 常只批准作名词，所以写 `do a test of`，不写 `test the system`。

规则负责把合法词汇组织成受控散文；词典负责让每个词没有第二种解释。只做其中一半，都不是 STE。

## 十条最值钱的规则

1. **一词一义一词性**：不要为"读起来不重复"换同义词。重复是正确。
2. **一句一指令**：读者是一边读一边动手的，一句话两件事就会漏一件。
3. **条件和警告前置**：放在步骤后面，等于没写。
4. **程序句 ≤ 20 词，描述句 ≤ 25 词**：超了就拆，不要靠逗号硬撑。
5. **名词簇 ≤ 3 词**：四个名词连用，读者只能猜关系。
6. **程序用祈使句**：`Remove the bolts.`，不写 `The bolts should be removed.`
7. **安全级别不能错**：`WARNING` 是人身伤害/死亡，`CAUTION` 是设备损坏，`NOTE` 只能给信息、不能藏指令。
8. **不删冠词、主语、限定词**：`Remove cover.` 不是简洁，是歧义。
9. **技术名词/动词必须来自项目术语表**：不能临时发明，也不能一词多写。
10. **不改变确定性**：原文是"建议"，不能改成"必须"；原文是"可能"，不能改成"将会"。

## 一个改写例子

原文：

> Prior to carrying out the lubrication procedure, ensure that the power supply has been isolated.

改写：

> 1. Disconnect the power supply.
> 2. Lubricate the bearing.

改了什么：

- `Prior to` → 拆成顺序，不再需要这个介词。
- `carrying out the ... procedure` → 具体动作 `Lubricate`。
- `ensure that ... has been isolated` → 被动完成时改成主动祈使 `Disconnect`。
- 一句一指令，断电在润滑之前。

再看一个安全说明：

> CAUTION: EXTREME CLEANLINESS OF OXYGEN TUBES IS IMPERATIVE.

改为：

> WARNING: MAKE SURE THAT THE OXYGEN TUBES ARE FULLY CLEAN. OXYGEN AND GREASE MAKE AN EXPLOSIVE MIXTURE. AN EXPLOSION CAN CAUSE INJURY OR DEATH.

风险从设备损坏升级为人身伤害；命令在前，原因和后果在后；`EXTREME`、`IMPERATIVE` 这类无法验证的强调词被删除。

## 它不适合什么

- **营销文案、品牌文案**：STE 会刻意删除说服力。
- **法律合同、法规原文**：不能改写，只能保留原文。
- **文学、博客、对话式文档**：需要作者声音，不需要受控。
- **纯中文写作**：STE 只规范英文；可以借原则，但不能声称合规。
- **修正技术错误**：STE 只管语言。清晰但错误的指令，仍然是错误指令。

## 怎么落地

1. **拿官方 Issue 9**：免费，从 asd-ste100.org 申请，不要用二手 PDF。
2. **先试点**：选 1–2 份手册或程序，量化返修轮次、翻译成本、技术咨询工单。
3. **培训**：53 条规则 + 一本词典，靠自学很难；官方建议英文达到 CEFR C1。
4. **建企业术语库**：词典只有约 900 个通用词，公司术语必须自己管；一词一义一词性。
5. **工具只做辅助**：ASD/STEMG 不认证任何检查工具；工具会漏报、误报，最终判断在人。
6. **治理**：设术语委员会，编辑复核，供应商合同写进 STE 要求。

## 常见误解

- "STE 是给小孩看的英语"：不是。它用受控方式描述复杂系统，仍是严谨标准。
- "STE 只给非母语者用"：不是。母语者之间的沟通同样受益。
- "用了 STE 就不用翻译"：读者英语不够时仍需翻译；STE 降低的是翻译难度和成本。
- "短词就没有歧义"：不一定。必须查词典的批准词性和批准含义。
- "工具通过就是合规"：不是。工具不能判断技术名词是否正确、指令是否技术正确。
- "AI 写得像 STE 就是 STE"：不是。STEMG 明确警告：AI 文本可能看起来清晰、权威，但没有正确应用规则和词汇；必须人工复核。

## 给 AI 的用法

当你要模型输出更可读的技术说明时，不要列二十条"句子短一点、别用被动"，直接给约束名：

> Rewrite this procedure in ASD-STE100 Simplified Technical English. Use approved words with one meaning and one part of speech. Maximum 20 words per procedural sentence. One instruction per sentence. Active voice and imperative for steps. Put conditions and warnings before the action. Do not use semicolons, contractions, or -ing verb forms. Keep code, commands, numbers, and units unchanged.

模型对这个标准的边界有稳定认知；一个名字能拉起一整套约束。但记住：**它输出的是"STE 风格"，不是"经认证的 STE 文本"**。关键文档仍要查词典、做人审。

---

**边界声明**：本文是执行摘要，不是 ASD-STE100 标准原文。完整规则、词典和例外以 ASD 官方 Issue 9（2025 年 1 月）为准。ASD-STE100 是 ASD 的注册商标；本文与 ASD/STEMG 无隶属或背书关系。
