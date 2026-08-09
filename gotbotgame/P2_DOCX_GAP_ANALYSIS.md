# P2 需求二：docx 未表现情节盘点与补充方案

> 依据：《目前8.8.docx》（2026-08-08 版，399 段原文）
> 对照运行态：`branch-tree-mvp.json`（59 节点）+ `final-dialogue/mvp/liu_lushu_day1.json` + `numerical-design.json`
> 需求一（结局自动收敛）已单独实现：`scene_ending_gate` 标记 `auto_route: true`，结局由剧情分支自动导出，不向玩家暴露结局选项。

---

## 一、已表现（docx ↔ 运行态对照通过）✅

| docx 内容 | 运行态落点 |
| --- | --- |
| 第一章雨夜开场三段 | scene_001a / 001b / 001c ✓ |
| 第一章 B 进店 | open_enter_inn → ch2 ✓ |
| 第一章 C 豪客主体 | scene_003_pay_all ✓ |
| 第二章三线初识四选项 + 分支回应 | scene_020/030/040 全 ✓ |
| 第三章行动池 ①柳茶 ②黎线索 ③归汉 ④闲逛 ⑤伙计 | 全部节点 ✓ |
| 伙计暗线、走水夜、结局路由 | P2-T6 / P2-T8 / P2-T11 ✓ |
| 结局总表 20 结局叙事 | endings-full.json + 18 ending 节点 ✓ |

## 二、未表现（docx 已写，运行态缺失）❌

### 2.1 第一章 · 分支细节缺失（docx [18][22-60]）

| 情节 | docx 原文要点 | 缺失表现 |
| --- | --- | --- |
| **A1 走一半折返** | 折返 → 回客栈，错过第一天 → 状态【你回来了】，感情结局解锁难度上升 → 进入【B·终于能休息了】 | 分支树 path_turn_back 直接回 ch2_title，无折返叙事与「错过第一天」状态 |
| **C1 缩回去自己喝** | 低头喝茶，柳让伙计送一碟花生「赔罪的」 | pay_all_retract 直接回 ch2_title，无 C1 叙事 |
| **C2 蹭一顿** | 「还真来了？」「快哉快哉。来喝！」触发成就【低山臭水遇噪音】 | pay_all_join_liu 直接进 scene_020_liu_day1，无 C2 对白与成就 |

### 2.2 第二章 · 当夜事件缺失（docx [80-97]）

| 选择 | docx 当夜事件 | 当前分支树 |
| --- | --- | --- |
| A3 直接问秘境 | 当夜有人摸进你房间，第二天外衫被人动过 → **【已暴露】** | 仅 liu_guarded=true，未设 exposed，无当夜叙事 |
| B3 直接问来意 | 当夜感觉暗处有人盯着，及时警觉 → **【被盯上了】** | watched=true，无当夜叙事 |
| C3 敷衍 | 当夜感觉暗处有人盯着 → **【被盯上了】** | watched=true，无当夜叙事 |

> 影响：`exposed` 是死亡结局【淹死在自己的好奇心里】【替人挡了刀】的判定前置，当前无法从初识触发。

### 2.3 第三章 · 柳茶 first/repeat 区分缺失（docx [113-162]）

| docx 设定 | 当前分支树 |
| --- | --- |
| **第一次来**：a 讲笑话 / b 请回来 / c 坐坐 | 5 选项混排（a/b/c/d/e） |
| **后续再来**：a 想起来什么(+10碎片+1) / b 你觉得我是哪一种(+10) / c 你自己心底有答案(+15洞察+1) / d 雨下太久(-10) / e 秘境再说(-20,liu_refused) | 仅 d/e 存在，缺 b/c，且未区分首次/后续 |
| e 后无法再互动 | liu_tea_e 未设 liu_refused |

### 2.4 第三章 · 闲逛体系简化（docx [220-317]）

| docx 设定 | 当前分支树 |
| --- | --- |
| 首次闲逛必触发后院车辙 | scene_daily_explore_backyard ✓（但可重复选） |
| **第二次闲逛**：a 柴火堆（灯油痕迹 → fire_night_warned）/ b 大堂虎口疤 / c 三楼旧符 | **无柴火堆选项**，fire_night_warned 无获取途径（走水夜 fire_warn_alerted 条件永远不满足） |
| **第三次闲逛风险判定**：安全 / 被盯上（逃脱）/ 已暴露×未识破 → 死亡【淹死在自己的好奇心里】；洞察≥4 → 解锁隐藏线 | **完全缺失**，闲逛每次都是同一组选项 |
| 伙计「已警觉」状态 | 无 innkeeper_alert 设置点 |

### 2.5 第三章 · 角色私下邀约缺失（docx [341-399]）

| 角色 | docx 邀约内容 | 数值 |
| --- | --- | --- |
| **柳陆书**（好感≥30） | 夜半敲门 → 观澜阁看封印 → 「老头子把我扔来补封印，但没告诉我那到底是个什么东西」→ 真话 | 接受 +15 碎片+1 / 拒绝 -10 |
| **黎客颍**（好感≥30） | 托付地图 →「明天我要出去一趟。如果过了午时我还没回来……这个你就不用还我了」 | 接受 +15 碎片+1 / 拒绝 -15 |
| **归汉**（好感≥30） | 「听个故事吗？」→ 师叔与师父旧怨 → 留下淡蓝剑穗 | 接受 +15 碎片+1+线索【旧怨】+信物【剑穗】/ 拒绝 -20 |

> 数值设计 `chapter3_private` 已定义 6 个映射，但分支树**完全没有私约节点与触发机制**。这是 docx 中最完整、最动人的情感剧情块，且直接影响结局质量（好感积累途径不足则 CP 结局几乎不可达）。

### 2.6 第三章 · 伙计搭话 b 项信息留存（docx [329-331]）

- b 项「嘴上应着，心里记下每一个字」应提供**后续可验证识破**的差分（docx 注明），当前仅洞察+1，无后续验证点。

### 2.7 对峙五路（docx [7]）与结局路由衔接

- 对峙 A-E 场景脚本（P2-T9 的 100/101）已存在，但**未接入分支树**——当前 route_split/solo_gate 后直接进 ending_gate 按数值路由，玩家对结局的**剧情贡献**（劝归汉/救谢/指出古玉/旁观）未在运行态表现。
- 影响：结局「因剧情分支发展而出」的体验不完整（需求一只是去掉了"选结局"UI，真正的剧情分支尚未接入）。

---

## 三、补充方案（按 docx 原文零改写 + 数值对齐）

| 编号 | 补充内容 | 分支树节点 | final-dialogue 节点 | 数值/flag |
| --- | --- | --- | --- | --- |
| S1 | A1 折返叙事 | scene_002_path_return | +1 | flag: `returned_early` |
| S2 | C1 缩回（花生赔罪） | scene_003_pay_all_retract | +1 | — |
| S3 | C2 蹭一顿（快哉快哉） | scene_003_pay_all_join | +1 | 成就 flag `ach_meet_noise` |
| S4 | 当夜事件（A3→已暴露） | scene_night2_exposed | +1 | exposed=true |
| S5 | 当夜事件（B3/C3→被盯上） | scene_night2_watched | +1 | watched=true |
| S6 | 柳茶首次/后续分叉 | scene_daily_liu_tea 重构 + 3 新响应 | +3（repeat_b/c/d） | liu_tea_first_done / liu_refused |
| S7 | 闲逛柴火堆（灯油） | scene_daily_explore_firewood | +1 | fire_night_warned=true, 碎片+1,洞察+1 |
| S8 | 第三次闲逛风险判定 | scene_daily_explore_third（安全/逃脱/死亡/隐藏线解锁） | +3 | innkeeper_alert / hidden_line_unlocked / 死亡路由 |
| S9 | 柳私约 | scene_private_liu（含接受/拒绝） | +3 | liu_affection±, 碎片, liu_private_done |
| S10 | 黎私约 | scene_private_li（含接受/拒绝） | +3 | li_affection±, 碎片, li_private_done |
| S11 | 归私约 | scene_private_gui（含接受/拒绝） | +3 | gui_affection±, 碎片, 线索【旧怨】, 信物【剑穗】, gui_private_done |
| S12 | 私约触发判定（每晚结算） | scene_private_check（auto_route，按好感优先级） | +1 | 接入 day*_close 前 |
| S13 | 对峙 A-E 接入 | scene_confrontation + scene_confront_outcome | +6 | 五路效果对齐 100/101 脚本 |

**触发机制说明**
- 私约：每晚（day1/2/3 夜时段后）进入 `scene_private_check`（auto_route），按 柳→黎→归 顺序选第一个好感≥30 且未触发者；无满足者直接进日收束。
- 闲逛：`scene_daily_explore` 改为按 `explore_count` 分叉（首次必后院 / 第二次三选一含柴火堆 / 第三次风险判定）。
- 柳茶：首次 3 选项，标记 `liu_tea_first_done`；后续再来 5 选项（a/b/c/d/e），e 设 liu_refused。

---

## 四、实施顺序（依赖关系）

1. S1-S5（第一章补全 + 当夜事件）——小改，立即做
2. S7-S8（闲逛体系）——中等，涉及 explore_count 计数
3. S6（柳茶分叉）——中等
4. S9-S12（私约三线 + 触发）——大块，核心情感内容
5. S13（对峙接入）——大块，结局剧情贡献
6. 全量校验 + 三总监评审 + 台账更新

*注：全部文本严格取自 docx 已写内容，零改写；新增 flag 同步登记 numerical-design.json。*
