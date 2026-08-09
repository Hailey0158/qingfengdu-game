# P2 结算页 · 走水夜 · 结局路由 实现评审

> 日期：2026-08-09
> 依据：P2_SETTLEMENT_ENDING_DESIGN.md、P2_T6_INNKEEPER_REVIEW.md、P2_T8_FIRE_NIGHT_REVIEW.md、《清风渡-MVP文案总汇》、endings-full.json、numerical-design.json
> 评审流程：产品设计总监 → 技术总监 → 美术总监 → 制作人终审

---

## 一、交付物

| 文件 | 内容 |
| --- | --- |
| `scenes/settlement_panel.tscn` + `scripts/settlement_panel.gd` | 独立结算面板：卷轴风（米色 StyleBoxFlat 与 DialogueBox 一致），展示 洞察/线索·碎片/柳黎归好感 + 5 项 flag 关键发现差分 + 收尾文案 + 「熄灯睡下」按钮（continue_pressed 信号） |
| `scenes/main.tscn` | 挂载 SettlementPanel 实例（DialogueBox 之后，渲染上层，鼠标可穿透） |
| `data/branch-tree-mvp.json` | 33→59 节点：day3_close 去 terminal 接结算；新增 summary/transition/fire_night/outcome/post_fire_night/route_split/solo_gate/ending_gate + 18 个 ending_* 节点（含既有 ending_front_no_road） |
| `data/final-dialogue/mvp/liu_lushu_day1.json` | 新增 6 段旁白（结算/过渡/走水夜/结果/分歧/独行）；结局叙事取自 endings-full 零改写 |
| `scripts/mvp_ui_controller.gd` | 新节点背景/颜色映射（26 项）；结算页显示面板、隐藏 ChoicePanel；`_on_settlement_continue` 驱动 |
| `tools/build_settlement_ending_nodes.py` / `verify_settlement.py` / `simulate_ending_gate.py` | 生成 / 校验 / 路由模拟脚本 |

## 二、流程链路

```
scene_day3_close → scene_day3_summary(结算面板) → fire_night_transition(过渡几句话)
→ scene_fire_night(走水夜四选项, P2_T8) → outcome(死亡分支:替人挡了刀)
→ post_fire_night(得闲饮茶入口) → route_split(合作/独行)
→ solo_gate(信错了人陷阱) → ending_gate(16 结局路由) → 18 个 ending_* 节点
```

## 三、校验结果

- 4 JSON 可解析；59 节点无断链；从入口 ch1_title 全图可达（仅 P1 遗留 scene_021_liu_day1_close 排除）
- 结算→走水夜→结局 链路完整；18 个新增结局节点 terminal=true、叙事取自已写文案
- 条件格式全部合规（bool/int/gte/lte/eq/neq）
- 结局路由模拟 12 场景全通过（真相/CP/CB/死亡×4/独行/清风过客/陌生人等）
- GDScript 括号平衡通过；控制器背景映射覆盖全部 59 节点

## 四、总监核查发现并修复的其他问题

1. **既有 bug——归汉双段条件失效**：9 个时段节点用 `{"op":"lt","value":1}`，但 runner 仅支持 gte/lte/eq/neq，lt 被静默忽略 → 双段选项同时显示。语义等价修正为 `{"op":"lte","value":0}`（9 处）。
2. **结局可达性缺陷——陌生人不可达**：清风过客兜底条件 `fragments>=4` 无好感约束，优先于陌生人（priority neutral>distant）→ 陌生人永远被拦截。修正：pass 限定 `fragments<=7`（f>=4 由前序 death 拦截保证），stranger 捕获 f>=8 低好感场景。

## 五、总监评审

### 产品设计总监
- 结论：**通过**。
- 意见：结算页「三日一瞬」文案与关键发现差分符合文案总汇设定；过渡文案（雨停又下→夜半走水）数句衔接自然，与 P2_T8 走水夜正文无缝；走水夜四选项与 fire_night_warned 差分复用 P2_T8 已评审内容；20 结局全覆盖（前方无路/淹死/信错了人/替人挡了刀在前置，16 结局路由 + 隐藏线/陷阱入口）；结局叙事零改写。

### 技术总监
- 结论：**通过**。
- 意见：分支树 59 节点结构正确、无断链、条件格式全合规；修复 lt 条件既有 bug 与陌生人可达性缺陷；结局路由模拟 12 场景通过；结算面板通过 continue_pressed 信号驱动（runner.choose("day3_to_fire_night")），与现有响应式选项流程不冲突；背景映射全覆盖。

### 美术总监
- 结论：**通过**。
- 意见：结算面板卷轴风（米色底、墨色边框圆角）与对话框/状态栏视觉语言一致；面板居中（240-1040 × 90-660）不遮对话框与状态栏；走水夜背景采用深红棕色调（3a2a24）区分紧张氛围；结局页深色留白符合「短句留白」收束气质。

### 制作人
- 结论：**终审通过**。
- 意见：设计→实现全链路落地，交付物完整（面板/分支树/文案/控制器/脚本），校验与模拟全部通过；依赖 P2-T3/T4/T6/T8 已完成；登记台账 P2-T11 completed。遗留：结算面板与走水夜/结局链路需 Godot 图形化编辑器联调验收（受 P1-T6 headless 挂起影响，静态校验已覆盖）。

## 六、验收结论

- **评审结论：通过（产品设计 / 技术 / 美术三总监 + 制作人终审）**。
- 台账：P2-T11 → completed（2026-08-09）；summary 20/48（41.7%）。
- 遗留：Godot 图形化编辑器人工验收（结算面板显示、走水夜四选项、结局路由与叙事展示）。
