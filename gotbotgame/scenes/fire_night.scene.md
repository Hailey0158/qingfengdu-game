scene_id: fire_night
location: 清风渡客栈·二楼走廊 / 归汉房门口 / 楼下院中
characters: [玩家, 归汉, 柳陆书, 黎客颍]
mood_tag: 火·危急
plot_tags: [fire_night, event, p2]
save_point: true

trigger:
  conditions:
    - "入夜后触发（对齐 PDD 分支流程【走水夜事件】scene_040）"
  note: "走水夜前若已发现灯油痕迹（fire_night_warned）则进入提前警觉叙事分支。"

narration: |
  夜半，你被一阵急促的脚步声吵醒。

  推开房门，走廊尽头——那是归汉房间的方向——门缝里透出火光，浓烟正从门框上方往外涌。

  楼下有人喊了一声：「走水了——」

  你还没完全反应过来，一道青影已经从你身边掠过去了。

  柳陆书。他什么都没拿，连扇子都扔在了楼下桌上，三步并作两步冲上楼梯，一头扎进那扇冒烟的门里。

  「柳陆书——！」

  dialogue:
  - speaker: 旁白
    text: "楼下院子里，黎客颍不知什么时候已经搬来了水桶，湿毛巾搭在肩头，正抬头瞄着二楼的高度——他在等柳把人带出来。"
  - speaker: 旁白
    text: "火舌舔着门框。你听见里面传来咳嗽声，然后是柳陆书被烟呛得说不出话的闷咳，混着归汉一声极轻的闷哼。"
  - speaker: 旁白
    text: "你该做点什么。"

choices:
  - id: fire_help_liu_upstairs
    label: "冲上楼，跟着柳陆书一起把人扶出来。"
    target: fire_night_rescue
    effects:
      gui_affection: +5
      liu_affection: +5
      insight: +1
    note: "冒险进入烟火中接应；归汉与柳好感提升。若此时已暴露(exposed)且无人接应，存在站错位风险。"
  - id: fire_help_li_below
    label: "留在楼下帮黎客颍——搬水、递湿毛巾，在他刀背上接住跳下来的人。"
    target: fire_night_rescue
    effects:
      li_affection: +10
      fragments: +1
    note: "黎客颍的接应位最稳妥，直接参与营救关键一环。"
  - id: fire_warn_alerted
    label: "（已发现灯油痕迹）先看了一眼火势——这不是普通的走水。你提醒黎客颍：'水别急着泼，先看火是从哪儿起来的。'"
    target: fire_night_rescue
    conditions:
      fire_night_warned: true
    effects:
      insight: +1
      li_affection: +5
    note: "fire_night_warned 差分：提前警觉火源，事后回想更清晰，洞察+1。"
  - id: fire_find_innkeeper
    label: "跑去找伙计要水桶和灭火的沙土。"
    target: fire_night_rescue
    effects:
      action_count: +1
    note: "无功无过：水桶和沙土送到时，柳已经把人带出来了。"

narration_after: |
  门被撞开的时候，柳陆书用肩膀顶着门框，一手扶着归汉，一手还护着那扇燎黑了的扇骨——扇骨燎黑了也没松手。

  归汉用剑尖点地，借着楼下黎客颍的刀背稳稳落了地。她呛了几口烟，白袍上落了一层灰，剑穗被火燎焦了一截，人没有大碍。

  柳陆书被烟呛得说不出话，蹲在院子里咳了好一阵。他手里那把扇子，扇面卷了边，扇骨烧黑了一根——他低头看了一眼，居然笑了，哑着嗓子说：「……还能补。」

  dialogue:
  - speaker: 旁白
    text: "这一夜谁都没有睡好。"
  - speaker: 旁白
    text: "第二天一早，你路过柳陆书门边，看见门缝底下塞着什么东西——一截淡蓝色的丝线，是剑穗上拆下来的。门缝里还塞着一张小纸条，上面只有两个字：'补扇。'"
  - speaker: 旁白
    text: "柳陆书捏着那截丝线，看了半天，什么也没说。窗边那把破扇子，后来被他仔仔细细地补好了。"

ending_gate:
  note: "走水夜后：1) 可继续探查靠门第三张桌（衔接隐藏线【得闲饮茶】→ tea_ending）；2) 进入秘境前路线分歧（合作线/独行线）；3) 若走水夜站位不当且好感不足无人接应，触发死亡结局【替人挡了刀】。"

branch_notes:
  fire_night_rescue: "三条主要参与路线均导向营救成功（归汉获救、柳扇骨燎黑、黎刀背接应），仅数值与差分不同。"
  "替人挡了刀触发": "走水夜事件中若玩家选择深入火场（fire_help_liu_upstairs）且已暴露(exposed)、三好感均低无人接应，火中意外接刀→死亡结局【替人挡了刀】（endings-full 对应文案：'刀光闪过的时候，你推开了身旁的人……你只知道有人活着出去了。'）。"
  "fire_night_warned": "走水夜前在闲逛中发现的灯油痕迹（flag 由探索/伙计线设置）在本事件提供差分叙事与洞察+1。"
  "效果建议": "上述 effects 为建议数值（对齐既有 liu/li/gui_affection、insight、fragments、action_count 体系），接入分支树(P2-T4/branch-tree)时与 numerical-design.json 固化同步。"
  "文本来源": "柳/黎/归三人在走水夜中的行为细节（柳第一个冲进去、扇骨燎黑不松手、黎搬水湿毛巾刀背接应、归汉剑尖点地落地、事后拆剑穗丝线塞柳门缝补扇）严格取自 PDD 角色档案（liu_lushu/li_keying/gui_han arc_stages 与 relationships）。"

audio:
  bgm: bgm_inn_daily
  ambient: amb_inn_night
  sfx: [sfx_door_open, sfx_candle_crackle]
