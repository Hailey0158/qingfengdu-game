# -*- coding: utf-8 -*-
"""P2 需求2 补充：S13 对峙五路接入分支树（docx [7] + scenes/100/101 脚本）。
A-D 路 → scene_ending_gate 数值路由；E 旁观 → ending_pass（清风过客）。"""
import json

BT = 'gotbotgame/data/branch-tree-mvp.json'
FD = 'gotbotgame/data/final-dialogue/mvp/liu_lushu_day1.json'

with open(BT, encoding='utf-8') as f:
    bt = json.load(f)
nodes = bt['nodes']

# route_split 合作线 → 对峙
nodes['scene_route_split']['choices'][0]['target_node'] = 'scene_confrontation'
# solo_gate 绕大路/摸黑 → 对峙
for c in nodes['scene_solo_gate']['choices']:
    if c['choice_id'] in ('solo_road', 'solo_direct'):
        c['target_node'] = 'scene_confrontation'

# ============ 对峙入口 ============
nodes['scene_confrontation'] = {
    "node_id": "scene_confrontation",
    "scene_ref": "scenes/100_confrontation.scene.md",
    "location": "观澜阁秘境深处",
    "speaker": "旁白",
    "mood_tag": "对峙·宿命",
    "plot_tags": ["confrontation", "climax", "p2"],
    "save_point": True,
    "character_appearances": [],
    "note": "最终对峙五路 A-E（docx [7]）：A 劝归汉出手 / B 让归汉决定 / C 救谢前辈 / D 指出古玉关键 / E 旁观。A-D→ending_gate 数值路由，E→清风过客。",
    "choices": [
        {
            "choice_id": "confront_a_persuade_gui",
            "text": "劝归汉出手：“你拦的不是他，是古玉。”",
            "target_node": "scene_confront_a",
            "effects": {"gui_affection": 10, "insight": 2}
        },
        {
            "choice_id": "confront_b_let_gui_decide",
            "text": "让归汉自己做决定",
            "target_node": "scene_confront_b",
            "effects": {"gui_affection": 5, "insight": 1}
        },
        {
            "choice_id": "confront_c_save_xie",
            "text": "趁其他人缠斗时，自己去救谢前辈",
            "target_node": "scene_confront_c",
            "effects": {"li_affection": 15, "sacrifice_choice": True},
            "conditions": {"li_met": True}
        },
        {
            "choice_id": "confront_d_point_jade",
            "text": "大声喊：“别打他了——打碎古玉！执念散了，他就会醒！”",
            "target_node": "scene_confront_d",
            "effects": {"truth_route_ready": True, "insight": 3},
            "conditions": {"insight": {"op": "gte", "value": 6}, "fragments": {"op": "gte", "value": 8}}
        },
        {
            "choice_id": "confront_e_observe",
            "text": "在一旁看着",
            "target_node": "scene_confront_e",
            "effects": {"liu_affection": -5, "li_affection": -5, "gui_affection": -5, "insight": 1}
        }
    ],
    "audio": {"bgm": "bgm_confrontation", "ambient": "amb_cave", "sfx": ["sfx_sword_draw", "sfx_jade_hum"]}
}

# ============ 五路叙事节点（对齐 scenes/101 脚本，A-D → ending_gate，E → pass） ============
nodes['scene_confront_a'] = {
    "node_id": "scene_confront_a",
    "scene_ref": "scenes/101_confront_outcome.scene.md",
    "location": "观澜阁秘境深处",
    "speaker": "旁白",
    "mood_tag": "抉择·余震",
    "plot_tags": ["confrontation", "resolution", "p2"],
    "save_point": True,
    "character_appearances": [],
    "note": "A 劝归汉出手：归汉提剑向谢师叔走去，古玉发出执念被切断的嘶鸣。",
    "choices": [{"choice_id": "confront_a_continue", "text": "继续", "target_node": "scene_ending_gate", "effects": {}}],
    "audio": {"bgm": "bgm_resolution", "ambient": "amb_cave", "sfx": ["sfx_jade_shatter"]}
}
nodes['scene_confront_b'] = {
    "node_id": "scene_confront_b",
    "scene_ref": "scenes/101_confront_outcome.scene.md",
    "location": "观澜阁秘境深处",
    "speaker": "旁白",
    "mood_tag": "抉择·余震",
    "plot_tags": ["confrontation", "resolution", "p2"],
    "save_point": True,
    "character_appearances": [],
    "note": "B 让归汉决定：归汉下不去手，黎客颍用刀背打晕谢师叔，替他做了决定。",
    "choices": [{"choice_id": "confront_b_continue", "text": "继续", "target_node": "scene_ending_gate", "effects": {}}],
    "audio": {"bgm": "bgm_resolution", "ambient": "amb_cave", "sfx": ["sfx_sword_draw"]}
}
nodes['scene_confront_c'] = {
    "node_id": "scene_confront_c",
    "scene_ref": "scenes/101_confront_outcome.scene.md",
    "location": "观澜阁秘境深处",
    "speaker": "旁白",
    "mood_tag": "抉择·余震",
    "plot_tags": ["confrontation", "resolution", "p2"],
    "save_point": True,
    "character_appearances": [],
    "note": "C 救谢前辈：撬开锁链，谢师叔喊小子，黎客颍在战局中回应嗯，来了。",
    "choices": [{"choice_id": "confront_c_continue", "text": "继续", "target_node": "scene_ending_gate", "effects": {}}],
    "audio": {"bgm": "bgm_resolution", "ambient": "amb_cave", "sfx": ["sfx_sword_draw"]}
}
nodes['scene_confront_d'] = {
    "node_id": "scene_confront_d",
    "scene_ref": "scenes/101_confront_outcome.scene.md",
    "location": "观澜阁秘境深处",
    "speaker": "旁白",
    "mood_tag": "抉择·余震",
    "plot_tags": ["confrontation", "resolution", "p2"],
    "save_point": True,
    "character_appearances": [],
    "note": "D 指出古玉关键：三人合力一击，古玉碎裂，谢师叔睁开眼睛——雨停了吗。",
    "choices": [{"choice_id": "confront_d_continue", "text": "继续", "target_node": "scene_ending_gate", "effects": {}}],
    "audio": {"bgm": "bgm_resolution", "ambient": "amb_cave", "sfx": ["sfx_jade_shatter", "sfx_stone_collapse"]}
}
nodes['scene_confront_e'] = {
    "node_id": "scene_confront_e",
    "scene_ref": "scenes/101_confront_outcome.scene.md",
    "location": "观澜阁秘境深处",
    "speaker": "旁白",
    "mood_tag": "抉择·余震",
    "plot_tags": ["confrontation", "resolution", "p2"],
    "save_point": True,
    "character_appearances": [],
    "note": "E 旁观：代价更大——归汉受轻伤、柳扇子报废、黎刀卷刃，三人对主控失望。→ 清风过客。",
    "choices": [{"choice_id": "confront_e_continue", "text": "继续", "target_node": "ending_pass", "effects": {}}],
    "audio": {"bgm": "bgm_resolution", "ambient": "amb_cave", "sfx": ["sfx_stone_collapse"]}
}

with open(BT, 'w', encoding='utf-8') as f:
    json.dump(bt, f, ensure_ascii=False, indent=2)
print('branch-tree 对峙节点完成，总节点数:', len(nodes))

# ============ final-dialogue 对峙文本 ============
with open(FD, encoding='utf-8') as f:
    fd = json.load(f)
fnd = fd['nodes']

fnd['scene_confrontation'] = {
    "speaker": "旁白",
    "text": "秘境深处，封印已裂了大半。古玉嵌在石壁正中，透出幽绿的光。光不强，却把每个人的影子都拉得很长。\n\n石壁前的椅子上坐着一个人。面容清瘦，头发已半白，但脊骨笔直。他手里攥着半截旧刀柄，闭着眼。\n\n归汉停下了脚步。她的手握在剑柄上，指节一节一节收紧。剑穗晃了晃，淡蓝色的丝线在幽光里显得格外亮。\n\n“……师叔。”\n\n她只说了两个字，声音很轻。但整个洞窟都听见了。\n\n谢师叔睁开眼睛。他看了归汉很久，目光从她的脸移到她手里的剑，又移到那根剑穗。然后他笑了。\n\n“小丫头，你长这么大了。”\n\n归汉握着剑的手开始抖。柳陆书往前迈了一步，扇子握得死紧。黎客颍站在最外侧，刀已出鞘三指宽，他的目光在古玉和谢师叔之间掠了一个来回。\n\n谢师叔的声音很平和：“怎么来了？是那老头让你来的？”\n\n归汉没有回答。她的嘴唇动了动，一个字都没吐出来。\n\n你看见她的剑尖在发抖。你看见柳陆书的扇子骨缝里还留着一道黑痕。你看见黎客颍的手指已经按在了刀背上。\n\n在归汉的沉默里，柳陆书的沉默里，黎客颍的沉默里——该你开口了。"
}
fnd['scene_confront_a'] = {
    "speaker": "旁白",
    "text": "你说：“归汉——你拦的不是他。是古玉。”\n\n归汉猛地转过头看你。她的眼睛里有一瞬的空，又很快填满了什么。\n\n她转回去。剑尖不再抖了。\n\n“师叔，对不住。”\n\n她提剑向谢师叔走去。每一步都踩得很重。谢师叔看着她走过来，没有躲。\n\n“……好。”他说，“好。”\n\n剑光落下时，古玉发出一声尖锐的嘶鸣——那是执念被切断的声音。"
}
fnd['scene_confront_b'] = {
    "speaker": "旁白",
    "text": "你没有开口。你听见归汉的呼吸声越来越慢。沉默了很久。\n\n她说：“师父让我来把你带回去。”\n\n谢师叔愣了一下，然后笑了，笑得眼睛都弯了：“那老头儿还记得我呢。”\n\n归汉握着剑的手又紧了。她可以出剑的——但她下不去手。\n\n然后一道刀风从侧面劈来。黎客颍用刀背，干脆利落地敲在谢师叔后颈。\n\n谢师叔身体一软。黎客颍接住了他，单手把人放倒在地，动作利落得像排练过无数遍。\n\n归汉站在原地，剑尖垂了下去。她没有道谢。黎客颍也没等她道谢。"
}
fnd['scene_confront_c'] = {
    "speaker": "旁白",
    "text": "你趁着三人与古玉缠斗的间隙，侧身绕到石壁后。\n\n谢师叔被锁在石壁的阴影里，锁链早已锈蚀，但连接处的封印仍死死扣着他的手腕。你蹲下来，用随身短刀撬开封口，一扣一扣地拆。\n\n黎客颍注意到了你的动作。他在战局中刀锋一转，为你挡开飞溅的石屑。\n\n最后一扣脱开。谢师叔抬起头，看了你一眼，然后又看向战局中那个红发的背影。\n\n“……小子。”\n\n黎客颍在刀光中抬起头，手上的动作没有停。\n\n“嗯。来了。”"
}
fnd['scene_confront_d'] = {
    "speaker": "旁白",
    "text": "你几乎是喊出来的：“别打他了——打碎古玉！执念散了，他就会醒！”\n\n三个人同时看向你。\n\n柳陆书沉默了一会儿，然后，他轻声说：“你连这个居然都查到了。”\n\n他没有再犹豫。扇子一收，第一个转剑向古玉。归汉紧随其后，剑锋直指石壁中央那团幽绿的光。黎客颍的刀封住了古玉的退路。\n\n三人合击。古玉发出一声长啸——像是一个持续了百年的叹息——然后碎了。\n\n光散了。洞窟里安静下来。谢师叔缓缓睁开了眼睛。这一次，他的眼睛里有光了。\n\n“……雨停了吗。”"
}
fnd['scene_confront_e'] = {
    "speaker": "旁白",
    "text": "你没有开口。你只是站着，看着。\n\n他们三个人依旧解决了这个局面。但代价更大。\n\n归汉被古玉的反震弹开，左肩撞在石壁上，鲜血顺着袖口往下淌。柳陆书的扇子在最后一击中被震散了骨，墨竹扇面裂成两半，碎纸落了一地。黎客颍的刀刃卷了半寸，他盯着那道豁口，没说话。\n\n一切结束之后，归汉靠着石壁慢慢坐下来。柳陆书看着那两片碎扇面发了一会儿呆，然后踹开脚边碎石，什么都没说。黎客颍把刀插回鞘里，没有看你的方向。\n\n你不怪他们。"
}

with open(FD, 'w', encoding='utf-8') as f:
    json.dump(fd, f, ensure_ascii=False, indent=2)
print('final-dialogue 对峙文本完成，总节点数:', len(fnd))
print('=== S13 完成 ===')
