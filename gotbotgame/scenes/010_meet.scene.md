scene_id: scene_010_meet
location: 清风渡客栈大堂
characters: [玩家, 柳陆书, 黎客颍, 归汉, 客栈伙计]
mood_tag: 试探·好奇
plot_tags: [first_meet, all_routes, mvp, p2]
save_point: true

narration: |
  窗边坐着一个年轻男子，青衫，歪在椅子上，半条腿架在另一张凳上，手里转着把扇面画着墨竹的折扇。他见你看去，目光在你身上停了停，嘴角似乎弯了弯，像看见了什么有趣的东西。
  右边桌坐着的是另一个年轻男子，看上去比青衫人要年少几分。黑衣，高马尾，用根褪了色的红绳束起，落了几根。他坐的长凳上摆着把刀，刀鞘朴素无纹。你望去时他看了你一眼，目光温和，只停了一下便收回去，继续低头看他手里那张泛黄的纸。
  最里侧靠墙则坐着一个白衣女子，气质出尘如山间新雪。面前一柄长剑藏锋敛锐，淡蓝色的剑穗随风轻晃。你清楚她知道你进了门，可她从始至终都没动过一下，仿佛你只是吹动她剑穗的一阵风。
  你想了想，决定去找人聊聊天。

choices:
  - id: meet_liu
    label: "走向窗边男子"
    target: scene_020_liu_day1
    effects:
      liu_met: true
      liu_affection: +2
  - id: meet_li
    label: "走向右边桌子"
    target: scene_030_li_day1
    effects:
      li_met: true
      li_affection: +2
  - id: meet_gui
    label: "走向里侧桌子"
    target: scene_040_gui_day1
    effects:
      gui_met: true
      gui_affection: +2
  - id: observe_liu
    label: "先观察他的扇子"
    target: scene_020_liu_day1
    effects:
      liu_met: true
      insight: +1
      liu_observed: true
  - id: ask_innkeeper
    label: "向伙计打听观澜阁"
    target: scene_020_liu_day1
    effects:
      innkeeper_alert: true
      insight: +1

audio:
  bgm: bgm_inn_daily
  ambient: amb_inn_day
  sfx: [sfx_tea_pour, sfx_candle_crackle]
