scene_id: innkeeper_secret
location: 清风渡客栈·柜台 / 大堂·靠门第三张桌
characters: [玩家, 客栈伙计]
mood_tag: 暗涌·悬疑
plot_tags: [innkeeper, secret, dark_line, p2]
save_point: true

trigger:
  conditions:
    - "已识破虎口剑疤（recognized_scar）或 洞察 ≥ 2"
    - "至少一次与伙计搭话（innkeeper 行动池）"
  note: "三天任意时段触发的暗线揭示场景，可在闲逛/搭话路径后接入。"

narration: |
  线索在你自己心里慢慢拼起来了。

  伙计右手虎口那道疤——那不是干粗活留下的。那是练武留下的，而且练的时间不短。可一个客栈伙计，为什么会有这样的疤？

  你想起他每一次都站在柜台后，笑容妥帖，动作麻利，续茶倒水从不含糊。你也想起他耳后偶尔露出的那道青黑色纹路——你起初以为是脏，后来看分明了，那是从皮肤底下透出来的颜色，像藤蔓一样爬进衣领。

  你忽然想到一件事。这三天里，你从来没有见那张靠门第三张桌坐过人。可那张桌上，永远有一壶茶。茶是温的，续得很勤，勤得像是有人每天都会来坐。

dialogue:
  - speaker: 旁白
    text: "你趁伙计去后院的空当，走到柜台后面。账本摊开在灯下，最近几页写的都是每日流水——直到你翻到最下面一行。那行字跟前头的都不一样，写得极慢，每一笔都像是刻的：\n\n'等他回来。等他回来。'"
  - speaker: 旁白
    text: "你抬起头。外头雨声未歇，大堂里油灯晃了一下。你听见后院传来脚步声——伙计回来了。"

choices:
  - id: secret_ask_directly
    label: "等他回来——等谁回来？"
    target: innkeeper_secret_confront
    effects:
      insight: +1
      flag_watched: true
    warning: "正面质问会让他警觉，触发【被盯上了】"
  - id: secret_pretend
    label: "装作没看见，把账本放回原处。"
    target: innkeeper_secret_leave
    effects:
      insight: +1
      flag_observed_account_book: true
    note: "发现账本记录，为隐藏线【得闲饮茶】埋下伏笔"
  - id: secret_trap_ask
    label: "想起他提过的后山密道——追问那棵歪脖子老槐树的位置。"
    target: innkeeper_secret_trap
    effects:
      flag_bait_marked: true
    warning: "⚠️ 陷阱线：被标记为可诱饵，后续独自夜探秘境将触发死亡结局【信错了人】"

branch_notes:
  innkeeper_secret_confront: "直接质问：伙计笑容僵住，答非所问。触发 innkeeper_alert（伙计已警觉），后续闲逛风险升高。"
  innkeeper_secret_leave: "离开柜台装作无事。保留 observed_account_book 标记，走水夜后可继续探查第三张桌，衔接隐藏线。"
  innkeeper_secret_trap: "伙计凑近压低声音：'北走三里，歪脖子老槐树底下有个洞……'——他记得每一个字，像早就在等有人问。bait_marked=true。"
  "与数值设计对应": "flags 对齐 numerical-design.json：watched / innkeeper_alert / recognized_scar / bait_marked / observed_account_book；死亡结局【信错了人】条件 = bait_marked && solo_night_explore。"

audio:
  bgm: bgm_inn_daily
  ambient: amb_inn_night
  sfx: [sfx_tea_pour, sfx_door_open]
