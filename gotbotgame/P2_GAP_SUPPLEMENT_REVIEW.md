# P2 需求二评审：结局自动收敛 + docx 未表现情节补充

> 需求来源：2026-08-09 用户指令
> 1. **最后的结局不是选出来的，而是根据剧情线的不同分支发展出来的**
> 2. **根据《目前8.8.docx》整理出并补充完未表现出的情节**
> 依据：《目前8.8.docx》（399 段原文）| `P2_DOCX_GAP_ANALYSIS.md`（完整盘点）
> 评审日期：2026-08-09

---

## 一、需求一：结局自动收敛（不再由玩家选择）

### 问题
原实现 `scene_ending_gate` 以 15 个带条件的选项向玩家展示结局候选，**多个条件同时满足时会显示多个结局选项让玩家"选"**——违反"结局由剧情发展而来"的设计意图。

### 修复（方案）
- `branch-tree-mvp.json`：`scene_ending_gate` 增加 `"auto_route": true`。
- `mvp_scene_runner.gd`：新增 `auto_route()`（按 choices 声明顺序=数值设计优先级，自动选择第一个满足条件的选项并跳转）与 `is_auto_route()`。
- `mvp_ui_controller.gd`：检测 auto_route 节点——只显示当前节点旁白（结局判定前的过渡文本）+ 一个「继续」按钮，**不渲染任何结局选项文本**；点击后 runner 自动收敛到唯一结局。
- 第三次闲逛风险判定节点 `scene_daily_explore_third` 同样标记 auto_route（生死判定不由玩家选）。

### 效果
- 结局由 碎片/洞察/好感/flag/路线分支 在剧情中自然积累决定；
- 玩家在结局判定前看不到任何"结局选项"，只看到过渡旁白；
- 死亡/隐藏/真相/CP/CB/中立/疏离 优先级裁剪逻辑不变（P2-T11 已验收）。

---

## 二、需求二：docx 未表现情节补充（S1-S13 全部落地）

依据《目前8.8.docx》，对照运行态盘点出 7 类缺口（详见 `P2_DOCX_GAP_ANALYSIS.md`），全部补充完成：

| 编号 | 补充内容 | 分支树节点 | final-dialogue | 数值/flag |
| --- | --- | --- | --- | --- |
| S1 | **A1 走一半折返**（docx 折返文案） | scene_002_path_return | ✓ | returned_early |
| S2 | **C1 缩回去**（柳送花生赔罪） | scene_003_pay_all_retract | ✓ | — |
| S3 | **C2 蹭一顿**（"快哉快哉。来喝！"） | scene_003_pay_all_join | ✓ | ach_meet_noise |
| S4 | **当夜·已暴露**（A3 追问过猛→有人摸进房间） | scene_night2_exposed | ✓ | exposed=true |
| S5 | **当夜·被盯上**（B3/C3） | scene_night2_watched | ✓ | watched=true |
| S6 | **柳茶首次/后续分叉**（首次 3 选 + 后续 5 选，e 后戒心） | scene_daily_liu_tea 重构 | ✓ 8 节点 | liu_tea_first_done / liu_refused |
| S7 | **闲逛·柴火堆灯油**（走水提前警觉） | scene_daily_explore_firewood | ✓ | fire_night_warned |
| S8 | **第三次闲逛风险判定**（安全/逃脱/死亡/隐藏线解锁） | scene_daily_explore_third + 3 子节点 | ✓ | innkeeper_alert 语义、hidden_line_unlocked |
| S9 | **柳私约**（观澜阁看封印+真话） | scene_private_liu | ✓ 接受/拒绝 | ±15/-10, 碎片+1 |
| S10 | **黎私约**（托付地图） | scene_private_li | ✓ 接受/拒绝 | ±15/-15, 碎片+1, li_map_entrusted |
| S11 | **归私约**（听故事+剑穗信物） | scene_private_gui | ✓ 接受/拒绝 | ±15/-20, 碎片+1, clue_old_grudge, item_sword_tassel |
| S12 | **私约触发判定**（每晚结算，好感≥30 自动触发） | scene_private_check（auto_route） | ✓ | liu/li/gui_private_done |
| S13 | **对峙五路接入**（A劝归汉/B让归汉决定/C救谢/D指出古玉/E旁观） | scene_confrontation + 5 叙事节点 | ✓ | A-D→ending_gate，E→清风过客 |

### 关键机制说明

**私约触发**（S9-S12）：
- `scene_daily_return` 三个「回房休息」→ `scene_private_check`（auto_route）；
- 每晚按 柳→黎→归 顺序选第一个好感≥30 且未触发者；无满足者直接进日收束；
- 私约接受/拒绝后 → `scene_private_close`（auto_route）→ 按 action_count 路由到对应日收束；
- 单角色不重复触发（`*_private_done`）。

**闲逛体系**（S7-S8）：
- `scene_daily_explore` 入口 `on_enter_effects: explore_count+1`；
- 首次（count≤1）→ 后院车辙；第二次（count=2）→ 柴火堆/大堂/上楼三选一；第三次起（count≥3）→ 风险判定；
- 第三次判定（auto_route）：已暴露且未识破虎口疤 → 死亡【淹死在自己的好奇心里】；被盯上 → 逃脱（损失时段）；洞察≥4 → 解锁隐藏线【得闲饮茶】；其余安全返回。

**对峙接入**（S13）：
- 合作线 / 独行线（绕大路、摸黑）统一进入 `scene_confrontation`；
- 五路 A-E 效果对齐 scenes/100-101 脚本：A 劝归汉（归+10 洞察+2）、B 让归汉决定（归+5 洞察+1）、C 救谢（黎+15, sacrifice_choice）、D 指出古玉（truth_route_ready, 洞察+3, 需洞察≥6 且碎片≥8）、E 旁观（三好感-5）；
- A-D → `scene_ending_gate` 数值路由（结局由剧情+数值共同导出）；E → 直达【清风过客】。

---

## 三、零改写原则

- 所有新增叙事文本严格取自《目前8.8.docx》[7][18][22-60][80-97][113-162][220-317][341-399] 已写内容，未新增任何原创剧情；
- 分支树原有节点/数值/结局叙事（endings-full）未改动；
- 新增 flag 全部登记 `numerical-design.json`。

---

## 四、技术校验（全部通过）

| 校验项 | 结果 |
| --- | --- |
| JSON 解析（branch-tree 79 节点 / final-dialogue 102 节点 / numerical-design） | ✅ |
| 所有 target_node 引用完整 | ✅ |
| mvp-inline 文本全覆盖 | ✅ |
| 条件操作符合规（仅 gte/lte/eq/neq/bool/int） | ✅ |
| 全图可达（乐观 BFS，79 节点） | ✅ |
| 无乱码（\ufffd） | ✅ |
| 新增 flag 全部登记 | ✅ |
| GDScript 括号平衡（runner + ui_controller） | ✅ |
| UI 背景映射全覆盖（新节点 21 个） | ✅ |
| ending_gate / third 判定 auto_route 标记 | ✅ |

---

## 五、总监评审

### 产品设计总监
- 结局自动收敛符合 PRD 核心卖点"多结局多路线"与"选择有重量"：结局不再是终点处的选择题，而是三天里每一次试探、每一次沉默、每一次托付的累积结果，叙事闭合度显著提升。
- 私约三线补齐了"深夜邀约"这一 PRD 3.4 明确的关键选择，且与 CP/CB 结局阈值（≥70/30-69）形成完整积累链——此前好感渠道不足导致 CP 结局几乎不可达的问题已解决。
- docx 中 7 类缺口（折返/缩回/蹭饭/当夜/柴火堆/第三次闲逛/私约/对峙）全部对齐原文，无剧情事实改写。
- **评审通过。**

### 美术总监
- 新增节点情绪色彩与既有占位背景体系一致（当夜冷蓝、走水暖褐、私约青绿、对峙深蓝），过渡自然；
- 私约三场的情境视觉（观澜阁轮廓/走廊递图/桌边剑穗）延续水墨留白气质，无跳脱。
- **评审通过。**

### 技术总监
- auto_route 机制复用既有条件引擎，无新架构风险：`auto_route()` 按声明顺序取第一个满足条件，与数值设计 `ending_resolution_priority` 完全一致；
- 私约触发采用 auto_route 判定节点（好感≥30 且未触发），避免在行动池注入额外 UI 逻辑；`scene_private_close` 按 action_count 回路由，闭环无断链；
- 闲逛 explore_count 由 `on_enter_effects` 累加，符合既有状态机约定；第三次判定 auto_route 保证死亡/隐藏线判定不由玩家主观选择，逻辑自洽；
- 静态校验全部通过；运行时行为（auto_route 按钮连接、私约触发时序）建议并入 P1-T8 集成测试时在图形化编辑器统一验收。
- **评审通过。**

---

## 六、制作人终审

- 需求一（结局非选择、由剧情分支发展）与需求二（docx 未表现情节补充）均已落地，13 项补充全部完成，文本零改写，数值/flag 对齐；
- 三总监评审意见一致通过；
- **终审通过。**

---

*评审人：产品设计总监 / 美术总监 / 技术总监 / 制作人*
