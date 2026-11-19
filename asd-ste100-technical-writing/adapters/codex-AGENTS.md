<!-- ste-en:begin -->
## ASD-STE100 英文技术写作

写、改、审**英文**技术文档（维修手册、工卡、步骤、SOP、runbook、安全警告）时，按本节执行。营销文案、法规原文、文学创作不适用。中文文档请用 `ste-zh-technical-writing`。

规则细节按需读取：

- `references` 目录下的 writing-rules.md：53 条规则按 9 节的结构与示例。
- `references` 目录下的 vocabulary-and-grammar.md：词典机制、常见替换、词性陷阱。
- `references` 目录下的 checklist.md：机械检查、判断检查、交付模板。

硬约束：

- 只用词典批准词，按批准词性与批准含义使用。技术名词与技术动词只能用项目既有术语。
- 程序句 ≤ 20 词，描述句 ≤ 25 词。一句一指令，条件在动作之前。
- 名词簇 ≤ 3 词。不省略冠词、主语、`that`。
- 禁完成时、进行时、`-ing` 动词、缩写形式、拉丁缩写。程序用祈使句 + 主动语态。
- `WARNING` 管人身伤害，`CAUTION` 管设备损坏，`NOTE` 不含指令，且都在步骤之前。
- 不用分号。代码、命令、路径、数字、单位原样保留。

交付：改写稿 + 变更说明（`Before | After | 规则 | 理由`）+ 待确认清单。
检查：`python scripts/check_en.py <文件> --strict`。

不新增事实，不删警告。不虚构词典批准状态。可以写"按 ASD-STE100 Issue 9 写作规则改写"，不能写"通过认证"或"完全合规"。
<!-- ste-en:end -->
