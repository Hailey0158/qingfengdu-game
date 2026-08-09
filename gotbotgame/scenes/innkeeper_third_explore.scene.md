scene_id: innkeeper_third_explore
location: 清风渡客栈·大堂 / 后门
characters: [玩家, 客栈伙计]
mood_tag: 紧绷·生死一线
plot_tags: [innkeeper, third_explore, risk_check, hidden_line, death_gate, p2]
save_point: true

trigger:
  conditions:
    - "三天内第三次选择『独自闲逛』"
  note: "按初识/日常阶段累积状态分叉（对齐 numerical-design chapter3_explore.third_trigger）。"

narration: |
  这是你第三次在客栈里独自走动。

  大堂的油灯已经换过一盏，桌角的水渍还是那样。你走得很慢，一步一停，像是这间客栈忽然变得比前两天更大、更空。

  你走到靠门第三张桌旁边，停住了。

  桌上放着一壶茶。壶嘴还挂着水汽，茶是温的。桌边没有人，凳子摆得整整齐齐——像是一直有人在这里坐着，只是刚好起身。

  「这张桌每天都有人续茶，不知道是谁放的，但从来没断过。甚至有人说，是给死人留的。」

  你回头。伙计站在柜台后面，隔着七八步的距离，正看着你。他手里端着茶盘，笑容还是那样妥帖，可你忽然觉得，那双眼睛里什么都没有。

  「客官，那张桌不能坐。」

  dialogue:
  - speaker: 旁白
    text: "他走过来，步子不快不慢。你看见他右手虎口那道疤，在油灯下像一条没合拢的旧伤口。"

choices:
  - id: third_explore_safe
    label: "（洞察 ≥ 4 或已识破虎口疤）后退一步，借着倒茶的空当退到门口。"
    target: hidden_line_unlock
    conditions:
      insight: ">= 4"
    effects:
      flag_hidden_line_unlocked: true
      fragments: +1
      insight: +1
    note: "安全脱身，解锁隐藏线【得闲饮茶】入口。"
  - id: third_explore_safe_scar
    label: "（已识破虎口疤）盯着他的疤看，笑一笑：'讨生活的手，我也有一双。'"
    target: hidden_line_unlock
    conditions:
      recognized_scar: true
    effects:
      flag_hidden_line_unlocked: true
      insight: +1
    note: "识破练武痕迹，令对方忌惮，安全脱身，解锁隐藏线。"
  - id: third_explore_exposed
    label: "（已暴露且未识破虎口疤）一时语塞，退了两步，撞上身后的屏风。"
    target: ending_drown_curiosity
    conditions:
      exposed: true
      recognized_scar: false
    effects: {}
    warning: "⚠️ 死亡结局：淹死在自己的好奇心里（exposed=true && recognized_scar=false）"
  - id: third_explore_back
    label: "（其余情况）低头端茶，假装什么也没看见，退回自己的房间。"
    target: daily_return
    effects:
      flag_watched: true
    note: "安全但被进一步盯上。"

branch_notes:
  hidden_line_unlock: "解锁 hidden_line_unlocked，进入【得闲饮茶】隐藏线：走水夜后探查第三张桌 → 发现柜台账本记录 → tea_ending。"
  ending_drown_curiosity: "死亡结局【淹死在自己的好奇心里】——'你走在后院，身后脚步声不紧不慢。你回头，看见伙计站在三步之外。他端着茶盘，笑容妥帖。\"客官，您不该上二楼那间房的。\"他手中的火折子亮了。'"
  "与数值设计对应": "对齐 numerical-design.json：insight≥4 解锁隐藏线；death 结局『淹死在自己的好奇心里』= exposed && !recognized_scar；『得闲饮茶』= hidden_line_unlocked && observed_account_book && survived。"

audio:
  bgm: bgm_inn_daily
  ambient: amb_inn_night
  sfx: [sfx_footstep_wet, sfx_door_open]
