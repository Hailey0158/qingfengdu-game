# -*- coding: utf-8 -*-
"""P2 需求2 补充：S9-S12 角色私下邀约（柳/黎/归）+ 每晚触发判定。
文本严格基于《目前8.8.docx》[341-399] 已写内容，零改写。"""
import json

BT = 'gotbotgame/data/branch-tree-mvp.json'
FD = 'gotbotgame/data/final-dialogue/mvp/liu_lushu_day1.json'

with open(BT, encoding='utf-8') as f:
    bt = json.load(f)
nodes = bt['nodes']

# ============ 1. daily_return 三个"回房休息"改指向私约检查 ============
dr = nodes['scene_daily_return']
for c in dr['choices']:
    if c['choice_id'] in ('to_day1_close', 'to_day2_close', 'to_day3_close'):
        c['target_node'] = 'scene_private_check'

# ============ 2. 私约检查节点（auto_route，按好感优先级） ============
nodes['scene_private_check'] = {
    "node_id": "scene_private_check",
    "scene_ref": "mvp-inline:scene_private_check",
    "location": "清风渡客栈·客房",
    "speaker": "旁白",
    "mood_tag": "当夜·私约判定",
    "plot_tags": ["private", "night", "p2"],
    "save_point": True,
    "auto_route": True,
    "character_appearances": [],
    "note": "每晚结算：按 柳→黎→归 顺序选第一个好感≥30 且未触发私约者；无则直接日收束。",
    "choices": [
        {
            "choice_id": "private_check_liu",
            "text": "（柳私约）",
            "target_node": "scene_private_liu",
            "effects": {},
            "conditions": {"liu_affection": {"op": "gte", "value": 30}, "liu_private_done": False}
        },
        {
            "choice_id": "private_check_li",
            "text": "（黎私约）",
            "target_node": "scene_private_li",
            "effects": {},
            "conditions": {"li_affection": {"op": "gte", "value": 30}, "li_private_done": False}
        },
        {
            "choice_id": "private_check_gui",
            "text": "（归私约）",
            "target_node": "scene_private_gui",
            "effects": {},
            "conditions": {"gui_affection": {"op": "gte", "value": 30}, "gui_private_done": False}
        },
        {
            "choice_id": "private_check_none",
            "text": "（无私约）",
            "target_node": "scene_private_close",
            "effects": {}
        }
    ],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_night", "sfx": []}
}

# ============ 3. 柳私约 ============
nodes['scene_private_liu'] = {
    "node_id": "scene_private_liu",
    "scene_ref": "mvp-inline:scene_private_liu",
    "location": "清风渡客栈·柳陆书房门外",
    "speaker": "柳陆书",
    "mood_tag": "当夜·私约",
    "plot_tags": ["private", "liu", "p2"],
    "save_point": True,
    "character_appearances": [{"character": "liu_lushu", "pose": "倚门框", "expression": "含笑"}],
    "note": "柳私约：观澜阁看封印。接受+15碎片+1；拒绝-10。",
    "choices": [
        {
            "choice_id": "liu_private_accept",
            "text": "接受：跟上他，去看看。",
            "target_node": "scene_private_close",
            "effects": {"liu_affection": 15, "fragments": 1, "liu_private_done": True}
        },
        {
            "choice_id": "liu_private_refuse",
            "text": "拒绝：这大半夜的，我要睡觉。",
            "target_node": "scene_private_close",
            "effects": {"liu_affection": -10, "liu_private_done": True}
        }
    ],
    "audio": {"bgm": "bgm_liu_theme", "ambient": "amb_inn_night", "sfx": ["sfx_door_open"]}
}

# ============ 4. 黎私约 ============
nodes['scene_private_li'] = {
    "node_id": "scene_private_li",
    "scene_ref": "mvp-inline:scene_private_li",
    "location": "清风渡客栈·黎客颍房门外",
    "speaker": "黎客颍",
    "mood_tag": "当夜·私约",
    "plot_tags": ["private", "li", "p2"],
    "save_point": True,
    "character_appearances": [{"character": "li_keying", "pose": "持地图", "expression": "温和"}],
    "note": "黎私约：托付地图。接受+15碎片+1；拒绝-15。",
    "choices": [
        {
            "choice_id": "li_private_accept",
            "text": "接受：替他收着这张地图。",
            "target_node": "scene_private_close",
            "effects": {"li_affection": 15, "fragments": 1, "li_private_done": True, "li_map_entrusted": True}
        },
        {
            "choice_id": "li_private_refuse",
            "text": "拒绝：这个忙，我帮不上。",
            "target_node": "scene_private_close",
            "effects": {"li_affection": -15, "li_private_done": True}
        }
    ],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_night", "sfx": ["sfx_door_open"]}
}

# ============ 5. 归私约 ============
nodes['scene_private_gui'] = {
    "node_id": "scene_private_gui",
    "scene_ref": "mvp-inline:scene_private_gui",
    "location": "清风渡客栈·归汉房门外",
    "speaker": "归汉",
    "mood_tag": "当夜·私约",
    "plot_tags": ["private", "gui", "p2"],
    "save_point": True,
    "character_appearances": [{"character": "gui_han", "pose": "立于门外", "expression": "平静"}],
    "note": "归私约：听故事（旧怨）。接受+15碎片+1+线索【旧怨】+信物【剑穗】；拒绝-20。",
    "choices": [
        {
            "choice_id": "gui_private_accept",
            "text": "接受：进来说？我一向是个好听众。",
            "target_node": "scene_private_close",
            "effects": {"gui_affection": 15, "fragments": 1, "gui_private_done": True, "clue_old_grudge": True, "item_sword_tassel": True}
        },
        {
            "choice_id": "gui_private_refuse",
            "text": "拒绝：改天吧，我今晚有些累了。",
            "target_node": "scene_private_close",
            "effects": {"gui_affection": -20, "gui_private_done": True}
        }
    ],
    "audio": {"bgm": "bgm_gui_theme", "ambient": "amb_inn_night", "sfx": ["sfx_door_open"]}
}

# ============ 6. 私约后统一回日收束（auto_route 按 action_count） ============
nodes['scene_private_close'] = {
    "node_id": "scene_private_close",
    "scene_ref": "mvp-inline:scene_private_close",
    "location": "清风渡客栈·客房",
    "speaker": "旁白",
    "mood_tag": "当夜·收束",
    "plot_tags": ["private", "night_close", "p2"],
    "save_point": True,
    "auto_route": True,
    "character_appearances": [],
    "note": "私约后按 action_count 路由到对应日收束。",
    "choices": [
        {"choice_id": "pc_day1", "text": "（第一日收束）", "target_node": "scene_day1_close", "effects": {}, "conditions": {"action_count": {"op": "eq", "value": 3}}},
        {"choice_id": "pc_day2", "text": "（第二日收束）", "target_node": "scene_day2_close", "effects": {}, "conditions": {"action_count": {"op": "eq", "value": 6}}},
        {"choice_id": "pc_day3", "text": "（第三日收束）", "target_node": "scene_day3_close", "effects": {}, "conditions": {"action_count": {"op": "gte", "value": 9}}}
    ],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_night", "sfx": []}
}

with open(BT, 'w', encoding='utf-8') as f:
    json.dump(bt, f, ensure_ascii=False, indent=2)
print('branch-tree 私约节点完成，总节点数:', len(nodes))

# ============ final-dialogue 私约文本（docx 零改写） ============
with open(FD, encoding='utf-8') as f:
    fd = json.load(f)
fnd = fd['nodes']

fnd['scene_private_check'] = {
    "speaker": "旁白",
    "text": "当夜。\n\n你正要熄灯——"
}
fnd['scene_private_liu'] = {
    "speaker": "柳陆书",
    "text": "你正要熄灯，门被敲响了。三下，很轻，很散漫，像是没骨头一样随手叩的。\n\n你拉开门。柳陆书斜斜倚在门框上，换了身深色罩衫，手里那把扇子你没见过。他看见你，笑了一下：“睡不着？带你去个地方，去不去。”\n\n他手上的扇骨边缘隐约泛着银光。你问他去哪，他没答，只侧身让出走廊，催你快点跟上。"
}
fnd['scene_private_liu_accept'] = {
    "speaker": "柳陆书",
    "text": "你跟上他，走了许久。等到了地方你才发现，这里能看到观澜阁的轮廓。这座废弃的楼阁半隐在山雾中，只露出灰黑色的檐角，像是一截沉在水底的枯木。\n\n“我第一天来的时候，是师父带我站在这的。”他啪的一声撑开扇子，看了一眼山下，“我师父说，这封印二十年前就该修了。”\n\n夜风灌进衣领。他说话时语气还是懒懒散散的，但你注意到他扇子捏得很紧。“你知道最没意思的是什么吗？”他转过头来看你，“老头子把我扔来补封印，但没告诉我那到底是个什么东西。”\n\n你同他并肩看了半天，安静了好一会，再开口时，他声音低了几分：“……所以，你想问的那事，我是真的不知道。”\n\n他转身率先往回走。走了两步，没回头，声音从前面飘进你的耳朵：“至少你听见了一句真话，算你赚了，小家伙。”"
}
fnd['scene_private_liu_refuse'] = {
    "speaker": "旁白",
    "text": "你只觉得这人大半夜扰人清梦，你也是要睡觉的好吧！\n\n你啪的一声关上门，任由他的背影在风中凌乱。"
}
fnd['scene_private_li'] = {
    "speaker": "黎客颍",
    "text": "你听见两下不重不轻的敲门声。打开门，黎客颍正站在走廊里。他难得没束发，刀别在腰间，手中拿着那张旧地图。\n\n面前的游侠依旧温和地笑着，只是你能看清他眼中带着些隐隐约约的期待。\n\n“这个，拜托你帮我收着。”\n\n他把地图递过来。你接住了。\n\n“明天我要出去一趟。如果过了午时我还没回来……”他停了一下，“这个你就不用还我了。”"
}
fnd['scene_private_li_accept'] = {
    "speaker": "黎客颍",
    "text": "你握着那张地图，忽然觉得很沉重。“你找到人了？”\n\n他没有否认。安静了一会儿才开口：“我是去确认一件事。不是去送死。但这种事谁也说不好。”他抬头看了你一眼，“你今晚就当没见过我。明天过了午时，我若没来找你拿，你就随意处理了。”\n\n他说完转身要走。脚步很稳，像早就把这段话在心里说过很多遍了。"
}
fnd['scene_private_li_refuse'] = {
    "speaker": "黎客颍",
    "text": "你摇了摇头：“这个忙，我帮不上。”\n\n他愣了一下，随即把地图收回袖中，像是没听到你拒绝一样，声音还是那样温和平静：“是我冒昧了。打扰。”\n\n他转身离开，脚步依旧很稳。"
}
fnd['scene_private_gui'] = {
    "speaker": "归汉",
    "text": "当夜。你正要熄灯，门被敲响了。只有一下，很轻。\n\n你开门，归汉站在走廊里，没有拿剑。她仍旧穿着那身白袍，但剑穗却没有系在剑上，淡蓝色的一截自袖口露出，像是被她攥在手中的月光。\n\n“你还没睡，”她似乎有些意外，表情虽然没什么变化，但眼底有些淡淡的纠结和哀愁。她站在你门口，安静了一会儿，想了想还是开口：“听个故事吗？”\n\n她的语气很平静。但她的手指攥着那根剑穗，攥得指节发白。"
}
fnd['scene_private_gui_accept'] = {
    "speaker": "归汉",
    "text": "你侧身让开门。她犹豫了一下，走进来坐在桌边。你给她倒茶，她没接，只是看着自己手上的那根剑穗。\n\n“我师叔和师父是同一个师父带出来的。二十年前，他们一起封印了观澜阁。后来他们吵了一架。师叔想毁掉古玉，师父想带走它。师叔说那东西留着迟早出事。师父说那东西不该被毁。”\n\n她实在不是擅长讲故事的人，但你仍旧认真听着她用这样生硬的语气，尝试着讲完她的回忆。\n\n“他们吵完那一架，只有师父一个人回了��门。从此他们再也没见过面。”\n\n窗外的风吹动门板，她的声音有些低。“三个月前，师父派我来看，他说是因为封印需要加固了，但我知道，他是想让我来看看师叔。可那天我才知道……他不是守着，他是被关在里面了。”\n\n你们二人沉默了许久。她把那根剑穗轻轻放在了你的桌子上，推到你面前。“这根剑穗是我外出游历时，师叔给我的。那时我还不知道他和师父已经决裂。他对我很好。”\n\n她说完便起身走向门口，到门边却顿住了脚步，没有回头。\n\n她走了，剑穗留在了你的桌子上。"
}
fnd['scene_private_gui_refuse'] = {
    "speaker": "归汉",
    "text": "“改天吧，我今晚有些累了。”\n\n她点了点头，没再多说，转身走了。\n\n走廊尽头，她攥着那根剑穗的手，指节还是白的。"
}
fnd['scene_private_close'] = {
    "speaker": "旁白",
    "text": "这一夜，比想象中要长。\n\n你躺下，看着窗外雨停又落，想了很久。"
}

with open(FD, 'w', encoding='utf-8') as f:
    json.dump(fd, f, ensure_ascii=False, indent=2)
print('final-dialogue 私约文本完成，总节点数:', len(fnd))
print('=== S9-S12 完成 ===')
