# P2-T8 走水夜事件脚本 · 评审与验收

> 日期：2026-08-09
> 负责人：story-designer
> 依据：PDD 角色档案（liu_lushu / li_keying / gui_han 的 arc_stages 与 relationships 走水夜细节）、PDD 分支流程【走水夜事件】scene_040、numerical-design.json（fire_night_warned / 死亡结局）、endings-full.json
> 评审流程：产品设计总监 → 技术总监 → 制作人终审

---

## 一、交付物

| 文件 | 内容 |
| --- | --- |
| `scenes/fire_night.scene.md` | 走水夜事件完整场景：夜半起火 → 柳陆书第一个冲进归汉房间救人（扇骨燎黑了也没松手）→ 黎客颍楼下搬水/湿毛巾/刀背接应 → 归汉剑尖点地落地 → 事后归汉半夜拆剑穗丝线塞柳门缝补扇。玩家 4 选项参与（上楼接应/楼下帮黎/灯油警觉差分/找伙计），衔接隐藏线与死亡结局 |
| `tools/verify_p2t8.py` | 一致性校验脚本 |

## 二、叙事要点（严格取自 PDD，零改写设定）

- 柳陆书：归汉房间着火时第一个冲进去，被烟呛得说不出话，**扇骨燎黑了也没松手**（PDD liu_lushu arc_stages 走水夜）
- 黎客颍：柳去救人时在下面接应——瞄了高度搬水过来准备湿毛巾，柳跳时用刀帮他踩刀上跳下来（PDD li_keying relationships）
- 归汉：房间着火被柳救出，剑尖点地轻巧落地；事后**半夜拆剑穗丝线塞进柳门缝**让他补扇子（PDD gui_han arc_stages）
- fire_night_warned 差分：走水夜前发现灯油痕迹 → 提前警觉火源（洞察 +1）
- 衔接：走水夜后可探查第三张桌（隐藏线【得闲饮茶】）；走水夜站位不当且无人接应 → 死亡结局【替人挡了刀】

## 三、校验结果（verify_p2t8.py）

- 场景字段完整（scene_id/location/characters/mood_tag/plot_tags/save_point/trigger/narration/dialogue/choices/narration_after/ending_gate/branch_notes/audio）✅
- PDD 走水夜细节 12 项关键词全覆盖 ✅（含忠实补回「扇骨燎黑了也没松手」原句）
- 死亡结局【替人挡了刀】、隐藏结局【得闲饮茶】文案存在于 endings-full.json ✅
- 4 个玩家参与选项齐全；fire_night_warned flag 已在数值设计定义 ✅

## 四、总监评审

### 产品设计总监
- 结论：**通过**。
- 意见：走水夜是三人关系暗线的高光事件，叙事忠实 PDD 角色档案（柳的义气、黎的默契、归汉不善言谢的回应），玩家的参与选项不影响既定三人行为主线，仅产生数值与差分；隐藏线/死亡结局衔接正确；未越界改写任何已写设定。

### 技术总监
- 结论：**通过**。
- 意见：fire_night_warned 条件选项、效果数值（liu/li/gui_affection、insight、fragments、action_count）均对齐既有数值体系；「替人挡了刀」触发条件说明与 numerical-design 一致；校验脚本通过。效果建议值已标注待接入分支树时固化。

### 制作人
- 结论：**终审通过**。
- 意见：交付物与 P2-T8 范围匹配，依赖 P2-T3 已完成；可标记 completed。P2 剩余 P2-T10（全剧本文案润色）可作为下一收口任务。

## 五、验收结论

- **评审结论：通过（产品设计总监 / 技术总监 / 制作人终审）**。
- 台账：P2-T8 → completed（2026-08-09）；summary 19/47（40.4%）。
- 遗留：fire_night 事件接入分支树与数值固化（联同 P2-T6 隐藏线）留待集成阶段（P4-T1/P4-T2）统一验证。
