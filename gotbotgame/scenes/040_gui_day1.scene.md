scene_id: scene_040_gui_day1
location: 清风渡客栈大堂·里侧桌
characters: [玩家, 归汉]
mood_tag: 冷淡·试探
plot_tags: [gui_route, day_1, p2]
save_point: true

narration: |
  你走向里侧桌子。你还没走到她面前，她放下茶杯先开口了。

  "你看了我三次。"

choices:
  - id: gui_c1_found_out
    label: "……你发现了？"
    target: scene_040_gui_response
    effects:
      gui_affection: +5
  - id: gui_c2_sword
    label: "我在看你的剑。"
    target: scene_040_gui_response
    effects:
      gui_affection: +10
      insight: +1
  - id: gui_c3_scenery
    label: "我只是看看风景。"
    target: scene_040_gui_response
    effects:
      gui_affection: -10
      watched: true
  - id: gui_c4_sit_down
    label: "不说话，直接在她对面坐下"
    target: scene_040_gui_response
    effects:
      gui_affection: 0

audio:
  bgm: bgm_inn_daily
  ambient: amb_inn_day
  sfx: [sfx_tea_pour]
