scene_id: tea_ending
location: 清风渡客栈·大堂·深夜 / 后门
characters: [玩家, 客栈伙计]
mood_tag: 怅然·余韵
plot_tags: [hidden_line, tea_ending, ending, p2]
save_point: true

trigger:
  conditions:
    - "已解锁隐藏线（hidden_line_unlocked）"
    - "走水夜后探查第三张桌（observed_account_book）"
    - "存活（survived）"
  note: "对齐 PDD scene_300_ending_tea 触发条件与 numerical-design ending_conditions['得闲饮茶']。"

narration: |
  走水夜过后，客栈里安静得像什么都没有发生过。

  你在夜里又走到靠门第三张桌旁边。茶壶还在，水是温的——续茶的人，从来没有断过。

  你蹲下去，借着一点油灯光，看见柜台账本下压着的那几页纸。流水账下面是另一行字，写得极慢，每一笔都像是刻的：

  「等他回来。等他回来。」

  你合上账本的时候，回头，伙计正站在柜台外。他手里拎着一个空茶盘，看着你，没有笑。

  dialogue:
  - speaker: 伙计
    text: "你看完了。"
    emotion: "声音很平，没有情绪"
  - speaker: 伙计
    text: "我有的时候能想起来他是谁，有时候想不起来，但是我一直记得要续茶。"
    emotion: "茫然"
  - speaker: 伙计
    text: "你走吧，趁我还能认出你是一个活人。"
    emotion: "平静"
  - speaker: 伙计
    text: "我不想再添一个了。"
    emotion: "低沉"

narration_after: |
  你连夜从客栈后门走了出去。风很大，吹得灯笼来回晃。

  你回头的时候，看见大厅里亮着一盏灯，那盏灯就放在靠门第三张桌上，灯光透过旧茶壶映出一个很模糊的影子，像是一个人坐在桌边，端着一杯茶慢慢喝。

  那盏灯亮了两息就灭了，但你站着看了很久。

  两息够一个活人喝完一盏茶吗？够一个死人回来坐上一会儿吗？

  你不知道，你只是站到天快亮就走了。

ending:
  id: tea_ending
  name: "得闲饮茶"
  type: hidden
  description: "你没有探查清楚全部真相，但你发现了客栈真正的秘密。"

choices: []

branch_notes:
  "文本来源": "本场景叙事与台词严格取自《目前8.8.docx》已写内容（endings-full.json『得闲饮茶』条目与 PDD scene_300_ending_tea），零改写。"
  "结局路由": "对齐 numerical-design.json：得闲饮茶 = hidden_line_unlocked && observed_account_book && survived；结局判定优先级 death > easter_egg > hidden > truth > cp > cb > neutral > distant。"

audio:
  bgm: bgm_ending_secret
  ambient: amb_inn_night
  sfx: [sfx_wind_strong, sfx_lantern_sway]
