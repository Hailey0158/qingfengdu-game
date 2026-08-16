# P3 结局结算面板设计 · 方案文档

> 任务：为 20 个结局设计专属结算页面（P2-T13 范畴延伸至 P3 UI 终化）
> 设计：产品设计总监 + 美术总监 + UI 交互设计师
> 日期：2026-08-16
> 依赖：P2-T7（20 结局叙事）、P2-T11（结算面板已有）、P2-T12（结局路由 auto_route）

---

## 一、设计目标

玩家达成结局后，不再只看到一段 terminal 旁白就结束，而是进入一个**专属结算面板**：
- 视觉氛围与结局情绪匹配（CP 暖色 / 死亡冷暗 / 真相金暖 / 隐藏暗调）
- 展示本局数值回顾 + 关键 flag 差分 + 达成路径摘要
- 给出结局专属"题记"（一句点睛引言，基于结局叙事提炼）
- 解锁进度（X / 20 结局达成），激励多周目
- 「再玩一次」按钮 → 重置 GameStateManager → ch1_title

## 二、通用面板结构（5 区）

| 区 | 内容 | 数据来源 |
| --- | --- | --- |
| ① 结局标题区 | 结局名称（书法体）+ 类型标签 | endings-full.name / type |
| ② 题记区 | 一句点睛引言（结局专属） | ending_page.epigraph（新增） |
| ③ 数值回顾区 | 柳/黎/归好感 + 洞察 + 碎片 + 关键 flag 差分 + 路径摘要 + 解锁进度 | GameStateManager |
| ④ 结局叙事区 | 结局正文（零改写） | endings-full.narration |
| ⑤ 操作区 | 「再玩一次」按钮 | 重置 → ch1_title |

## 三、20 结局视觉差异化配置

### CP 线 ×3（暖色·角色主题色）

| 结局 | bg_color | accent | decor | label | epigraph | stats_focus |
| --- | --- | --- | --- | --- | --- | --- |
| 扇底风 | #1a3a2a | #5DCAA5 | bamboo_fan | CP·柳陆书 | 扇面墨竹，山路很长。 | liu_affection, fragments |
| 归刀入鞘 | #2a1a1a | #D85A30 | sword_sheath | CP·黎客颍 | 这么多年，终于不是一个人。 | li_affection, fragments |
| 长剑有穗 | #1a2a3a | #85B7EB | sword_tassel | CP·归汉 | 你看着它的时候，它就不冷了。 | gui_affection, fragments |

### CB 线 ×3（中性偏暖·信物）

| 结局 | bg_color | accent | decor | label | epigraph | stats_focus |
| --- | --- | --- | --- | --- | --- | --- |
| 旧友新茶 | #2a3a2a | #9FE1CB | tea_bamboo | CB·柳陆书 | 茶凉就续，一续许多年。 | liu_affection |
| 同路之人 | #2a2a1a | #FAC775 | letter_tea | CB·黎客颍 | 他离得并不远。 | li_affection |
| 不冻泉 | #2a2a3a | #B5D4F4 | spring_silver | CB·归汉 | 她不冷，只是不愿让人看见。 | gui_affection |

### 正史 ×4（真相·冷峻）

| 结局 | bg_color | accent | decor | label | epigraph | stats_focus |
| --- | --- | --- | --- | --- | --- | --- |
| 真相达成 | #3a3a1a | #EF9F27 | jade_shatter | 真相 | 四十年了，这破玩意儿。 | fragments, insight |
| 清风过客 | #2a2a2a | #888780 | silhouette | 中立 | 有些人的故事，你不必知道结尾。 | fragments |
| 独行者 | #1a2a3a | #378ADD | lone_blade | 独行 | 目光已说了很多。 | insight, route_solo |
| 陌生人 | #1a1a1a | #B4B2A9 | empty_table | 疏离 | 你甚至不知道他们叫什么。 | liu/li/gui_affection |

### 隐藏 ×1（暗调·灯笼暖光）

| 结局 | bg_color | accent | decor | label | epigraph | stats_focus |
| --- | --- | --- | --- | --- | --- | --- |
| 得闲饮茶 | #1a1a0a | #FAC775 | lantern_tea | 隐藏 | 两息够一个活人喝完一盏茶吗。 | hidden_line_unlocked, observed_account_book |

### 彩蛋 ×1（山雾空寂）

| 结局 | bg_color | accent | decor | label | epigraph | stats_focus |
| --- | --- | --- | --- | --- | --- | --- |
| 前方无路 | #2a2a2a | #D3D1C7 | cliff_mist | 彩蛋 | 有些答案，你永远不会知道。 | chose_path_to_end |

### 死亡 ×8（冷暗·各异）

| 结局 | bg_color | accent | decor | label | epigraph | stats_focus |
| --- | --- | --- | --- | --- | --- | --- |
| 淹死在自己的好奇心里 | #0a1a0a | #5DCAA5 | fire_torch | 死亡 | 客官，您不该上二楼那间房的。 | exposed, recognized_scar |
| 信错了人 | #1a0a0a | #D85A30 | old_tree | 死亡 | 我提醒过你了。 | bait_marked, solo_night_explore |
| 替人挡了刀 | #2a1a1a | #F09595 | fire_flash | 死亡 | 有人活着出去了。 | sacrifice_choice |
| 三人反目 | #2a0a0a | #E24B4A | clash | 死亡 | 没有人走出那扇门。 | liu/li/gui_affection |
| 封印破碎 | #1a1a1a | #888780 | collapse | 死亡 | 知道了也拦不住。 | fragments |
| 错过真相 | #1a1a1a | #B4B2A9 | empty_cup | 死亡 | 只有认真的人配知道。 | fragments |
| 一知半解 | #0a1a1a | #85B7EB | fallen_sword | 死亡 | 你知道的还不够多。 | fragments, insight |
| 被真相压垮 | #0a0a1a | #378ADD | flood_info | 死亡 | 听了就是一辈子。 | fragments, insight |

## 四、数据结构扩展

`endings-full.json` 每个结局增加 `ending_page` 字段：
```json
"扇底风_liu_cp": {
  "name": "扇底风",
  "type": "liu_cp",
  "condition": "柳好感≥70",
  "narration": "...",  // 既有·零改写
  "ending_page": {
    "bg_color": "#1a3a2a",
    "accent": "#5DCAA5",
    "decor": "bamboo_fan",
    "label": "CP·柳陆书",
    "epigraph": "扇面墨竹，山路很长。",
    "stats_focus": ["liu_affection", "fragments"]
  }
}
```

## 五、实现方式

1. **`scenes/ending_panel.tscn`** + **`scripts/ending_panel.gd`**：通用面板，`refresh(ending_id)` 按 ID 读取 endings-full 的 ending_page 配置渲染差异化背景色/装饰/题记/数值回顾/叙事/再玩一次
2. **`mvp_ui_controller.gd`**：检测 terminal ending 节点 → 显示 ending_panel（隐藏常规对话框与选项面板）
3. **GameStateManager**：新增 `ending_unlocked` 数组记录已达成结局（存档持久化），「再玩一次」调用 `reset()` → `runner.show_scene("ch1_title")`
4. **decor 元素**：MVP 阶段用纯色背景+ accent 色装饰条/边框即可（P3 资产量产阶段替换为正式美术素材）

## 六、约束

- 题记（epigraph）基于结局叙事提炼，**不新增世界观设定**
- 结局叙事取自 endings-full.json，**零改写**
- 背景色取自既有 BACKGROUND_COLORS 体系，**与 PRD 美术方向一致**（青/黑/白主色，关键剧情暖红/冷蓝）
- 解锁进度依赖 GameStateManager.ending_unlocked（既有字段，P0 已定义）

---

*设计人：产品设计总监 / 美术总监 / UI 交互设计师*
