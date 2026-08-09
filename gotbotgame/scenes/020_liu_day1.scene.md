scene_id: scene_020_liu_day1
location: 清风渡客栈大堂·窗边
characters: [玩家, 柳陆书]
mood_tag: 散漫·试探
plot_tags: [liu_route, day_1, mvp]
save_point: true

narration: |
  柳陆书把扇子半合，往旁边让了让。
  他眉眼带笑，却没有把笑意交出来。

  柳陆书：哟，新面孔。如此不小心，我赌你活不过三天。

character_appearances:
  - character: liu_lushu
    visual_anchor: "黑发高髻、青衫、墨竹折扇"
    pose: "扇子半开半合"
    expression: "含笑试探"

choices:
  - id: liu_answer_directly
    label: "直说：我来查观澜阁"
    target: scene_021_liu_day1_close
    effects:
      insight: +1
      liu_affection: +1
  - id: liu_play_along
    label: "顺着他的话笑：那便赌一局"
    target: scene_021_liu_day1_close
    effects:
      liu_affection: +2
  - id: liu_ask_truth
    label: "问他是否知道古玉的事"
    target: scene_021_liu_day1_close
    conditions:
      insight: ">= 1（已获得至少一点洞察）"
    effects:
      insight: +2
      liu_guarded: true
      clue_liu_observation: true

ending_gate:
  note: "进入 scene_021_liu_day1_close，完成 P1 MVP 柳陆书第一天闭环；三天九时段与全量结局判定在 P2 接入。"

audio:
  bgm: bgm_liu_theme
  ambient: amb_inn_night
  sfx: [sfx_fan_open, sfx_fan_close]
