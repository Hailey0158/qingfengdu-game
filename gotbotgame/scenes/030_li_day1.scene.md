scene_id: scene_030_li_day1
location: 清风渡客栈大堂·右边桌
characters: [玩家, 黎客颍]
mood_tag: 温和·试探
plot_tags: [li_route, day_1, p2]
save_point: true

narration: |
  你走向右边桌子。黎客颍抬头冲你笑了一下。

  他说："别理他，他就是闲得慌。坐吧，喝点茶水，温的。"

  他推了一杯茶过来。

choices:
  - id: li_b1_name
    label: "道谢坐下，问他叫什么"
    target: scene_030_li_response
    effects:
      li_affection: +15
  - id: li_b2_weapon
    label: "注意到他的刀：'你是刀客？'"
    target: scene_030_li_response
    effects:
      li_affection: 0
      insight: +1
  - id: li_b3_ask_purpose
    label: "直接问他：'你来这里做什么？'"
    target: scene_030_li_response
    effects:
      li_affection: -10
      watched: true
  - id: li_b4_silent_tea
    label: "不说话，安静喝他的茶"
    target: scene_030_li_response
    effects:
      li_affection: 0

audio:
  bgm: bgm_inn_daily
  ambient: amb_inn_day
  sfx: [sfx_tea_pour]
