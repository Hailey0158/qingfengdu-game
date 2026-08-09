# P2-T6 伙计暗线+隐藏线 · 评审与验收

> 日期：2026-08-09
> 负责人：story-designer + branch-logic-engineer
> 依据：PDD「客栈伙计完整身份」(4.1–4.6)、PDD scene_300_ending_tea、numerical-design.json、endings-full.json、《清风渡-MVP文案总汇》
> 评审流程：产品设计总监 → 技术总监 → 制作人终审

---

## 一、交付物

| 文件 | 内容 |
| --- | --- |
| `scenes/innkeeper_secret.scene.md` | 伙计暗线·掌柜秘密：虎口剑疤（练武痕迹）、耳后青黑纹路（古玉侵蚀）、靠门第三张桌每日续茶、账本「等他回来。等他回来。」；三出口（正面质问→警觉 / 假作不知→保留账本标记 / 追问密道→诱饵标记） |
| `scenes/innkeeper_third_explore.scene.md` | 第三次闲逛·风险判定：安全路线（洞察≥4 或识破虎口疤）解锁隐藏线【得闲饮茶】；暴露路线（exposed && !recognized_scar）→ 死亡结局【淹死在自己的好奇心里】；其余→被进一步盯上 |
| `scenes/tea_ending.scene.md` | 隐藏结局【得闲饮茶】：走水夜后探查第三张桌 + 账本 → 伙计现身四句台词 → 结尾旁白（严格取自已写文案，零改写） |
| `data/numerical-design.json` | **补齐 flags 定义缺口**：observed_account_book / solo_night_explore / sacrifice_choice / survived（原在 ending_conditions 中被引用但未登记定义） |
| `tools/verify_p2t6.py` | 一致性校验脚本：flags 对齐 / 结局条件对齐 / 结局文案存在 / 场景脚本字段完整 / 已写文案零改动抽查 |

## 二、一致性校验结果（verify_p2t6.py）

- flags：场景脚本引用的 10 个标志全部在 numerical-design 中定义 ✅（补 4 个缺口后）
- 结局条件：得闲饮茶 / 淹死在自己的好奇心里 / 信错了人 / 替人挡了刀 均在 ending_conditions 中且条件键名一致 ✅
- 结局文案：4 篇死亡/隐藏结局叙事存在于 endings-full.json 且非空 ✅
- 场景脚本：3 文件 scene_id 正确、关键字段齐全 ✅
- 零改动：得闲饮茶关键句在结局数据与场景脚本中一致 ✅

## 三、总监评审

### 产品设计总监
- 结论：**通过**。
- 意见：伙计暗线严格遵循 PDD 4.1–4.6（表面伙计实为老板、虎口剑疤练武痕迹、古玉侵蚀致记忆混乱、以「保护重要的人」为杀人动机、第三张桌续茶执念）；隐藏线触发链（第三次安全闲逛→茶壶→账本→结局）与 PDD 4.6 一致；三份脚本的旁白与台词取自《目前8.8.docx》已写内容零改写；未越界引入新设定、未提前泄露古玉真相。

### 技术总监
- 结论：**通过**。
- 意见：发现并修复 numerical-design.json 数据完备性缺口（3 个被引用未定义的 flag + survived 补充登记），保证场景脚本与结局判定键名一致；场景脚本的 choice_id / conditions / effects 与数值设计对齐；死亡结局与隐藏结局触发条件正确映射；校验脚本通过。

### 制作人
- 结论：**终审通过**。
- 意见：交付物完整（3 场景脚本 + 数值设计补全 + 校验脚本），与 P2-T6 任务范围匹配；依赖 P2-T3/P2-T4 均已完成；可标记 completed。建议：走水夜（P2-T8）完成后，将 innkeeper_secret 与 tea_ending 的衔接在图形化编辑器联调验收。

## 四、验收结论

- **评审结论：通过（产品设计总监 / 技术总监 / 制作人终审）**。
- 台账：P2-T6 → completed（2026-08-09）；summary 18/47（38.3%）。
- 遗留：Godot 图形化编辑器联调（P2-T8 走水夜后衔接验证）待后续集成阶段。
