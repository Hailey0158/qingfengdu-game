scene_id: scene_001_rain_night
location: 雨夜山道 → 清风渡客栈门口
characters: [玩家, 客栈伙计]
mood_tag: 孤独·悬疑
plot_tags: [opening, rain_night, choice_branch_A, choice_branch_B, choice_branch_C, mvp]
save_point: true

narration: |
  雨下得密，山道被水光切成一段一段。
  你在风里看见一盏灯笼。灯下的木牌写着：清风渡。
  客栈门半掩着，里面有人影走动，像是一直在等谁。

choices:
  - id: open_enter_inn
    label: "终于有个能休息的地方了，进去坐会！"
    target: scene_010_meet
    effects:
      insight: +1
      action_count: +1
  - id: open_keep_walking
    label: "荒郊野岭，还是走到前面的镇子上再说吧。"
    target: scene_002_path
    effects:
      watched: true
      action_count: +1
  - id: open_pay_all
    label: "他怎么知道我是侠客？全场消费由我买单！"
    target: scene_003_pay_all
    effects:
      liu_invited: true
      action_count: +1

audio:
  bgm: bgm_rain_intro
  ambient: sfx_rain_continuous
  sfx: [sfx_footstep_wet, sfx_door_open]

branch_notes:
  scene_002_path: "回头可进入初识；坚持走到底进入 PDD 定义的彩蛋结局‘前方无路’。"
  scene_003_pay_all: "豪客选择进入伙计的试探，再决定收回玩笑或直接与柳陆书同坐。"
