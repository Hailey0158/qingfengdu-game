scene_id: scene_100_confrontation
location: 观澜阁秘境深处
characters: [玩家, 归汉, 柳陆书, 黎客颍, 谢师叔]
mood_tag: 对峙·宿命
plot_tags: [confrontation, climax, truth, p2]
save_point: true

narration: |
  秘境深处，封印已裂了大半。古玉嵌在石壁正中，透出幽绿的光。光不强，却把每个人的影子都拉得很长。
  
  石壁前的椅子上坐着一个人。面容清瘦，头发已半白，但脊骨笔直。他手里攥着半截旧刀柄，闭着眼。
  
  归汉停下了脚步。她的手握在剑柄上，指节一节一节收紧。剑穗晃了晃，淡蓝色的丝线在幽光里显得格外亮。
  
  "……师叔。"
  
  她只说了两个字，声音很轻。但整个洞窟都听见了。
  
  谢师叔睁开眼睛。他看了归汉很久，目光从她的脸移到她手里的剑，又移到那根剑穗。然后他笑了。
  
  "小丫头，你长这么大了。"
  
  归汉握着剑的手开始抖。柳陆书往前迈了一步，扇子握得死紧。黎客颍站在最外侧，刀已出鞘三指宽，他的目光在古玉和谢师叔之间掠了一个来回。
  
  谢师叔的声音很平和："怎么来了？是那老头让你来的？"
  
  归汉没有回答。她的嘴唇动了动，一个字都没吐出来。
  
  你看见她的剑尖在发抖。你看见柳陆书的扇子骨缝里还留着一道黑痕。你看见黎客颍的手指已经按在了刀背上。
  
  在归汉的沉默里，柳陆书的沉默里，黎客颍的沉默里——该你开口了。

choices:
  - id: confront_a_persuade_gui
    label: "劝归汉出手：'你拦的不是他，是古玉。'"
    target: scene_101_confront_outcome
    effects:
      gui_affection: +10
      insight: +2
    conditions: {}

  - id: confront_b_let_gui_decide
    label: "让归汉自己做决定"
    target: scene_101_confront_outcome
    effects:
      gui_affection: +5
      insight: +1
    conditions: {}

  - id: confront_c_save_xie
    label: "趁其他人缠斗时，自己去救谢前辈"
    target: scene_101_confront_outcome
    effects:
      li_affection: +15
      sacrifice_choice: true
    conditions:
      li_met: true

  - id: confront_d_point_jade
    label: "大声喊：'别打他了——打碎古玉！执念散了，他就会醒！'"
    target: scene_101_confront_outcome
    effects:
      truth_route_ready: true
      insight: +3
    conditions:
      insight: {"op": "gte", "value": 6}
      fragments: {"op": "gte", "value": 8}

  - id: confront_e_observe
    label: "在一旁看着"
    target: scene_101_confront_outcome
    effects:
      liu_affection: -5
      li_affection: -5
      gui_affection: -5
      insight: +1
    conditions: {}

audio:
  bgm: bgm_confrontation
  ambient: amb_cave
  sfx: [sfx_sword_draw, sfx_jade_hum]
