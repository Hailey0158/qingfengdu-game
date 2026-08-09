# -*- coding: utf-8 -*-
"""P2 需求2 补充：S7-S8 闲逛体系重构（首次/二次/三次分叉 + 柴火堆 + 风险判定死亡）+ S9-S12 私约三线 + S13 对峙接入骨架。
严格依据《目前8.8.docx》已写内容，新增 flag 同步登记数值设计。"""
import json, re

BT = 'gotbotgame/data/branch-tree-mvp.json'
FD = 'gotbotgame/data/final-dialogue/mvp/liu_lushu_day1.json'

with open(BT, encoding='utf-8') as f:
    bt = json.load(f)
nodes = bt['nodes']

# ============ S7-S8 闲逛体系 ============
# 1. 入口节点重构：按 explore_count 分叉
explore = nodes['scene_daily_explore']
explore['on_enter_effects'] = {"explore_count": {"op": "add", "value": 1}}
explore['choices'] = [
    {
        "choice_id": "explore_backyard",
        "text": "去后院看看",
        "target_node": "scene_daily_explore_backyard",
        "effects": {"fragments": 1, "insight": 1, "action_count": 1},
        "conditions": {"explore_count": {"op": "lte", "value": 1}}
    },
    {
        "choice_id": "explore_firewood",
        "text": "去柴火堆看看",
        "target_node": "scene_daily_explore_firewood",
        "effects": {"fragments": 1, "insight": 1, "fire_night_warned": True, "action_count": 1},
        "conditions": {"explore_count": {"op": "eq", "value": 2}}
    },
    {
        "choice_id": "explore_hall",
        "text": "去大堂看看伙计",
        "target_node": "scene_daily_explore_hall",
        "effects": {"fragments": 1, "insight": 1, "action_count": 1},
        "conditions": {"explore_count": {"op": "eq", "value": 2}}
    },
    {
        "choice_id": "explore_upstairs",
        "text": "上楼转转",
        "target_node": "scene_daily_explore_upstairs",
        "effects": {"insight": 1, "action_count": 1},
        "conditions": {"explore_count": {"op": "eq", "value": 2}}
    },
    {
        "choice_id": "explore_third",
        "text": "再去走走（第三次）",
        "target_node": "scene_daily_explore_third",
        "effects": {"action_count": 1},
        "conditions": {"explore_count": {"op": "gte", "value": 3}}
    }
]

# 2. 新增：柴火堆（灯油痕迹）
nodes['scene_daily_explore_firewood'] = {
    "node_id": "scene_daily_explore_firewood",
    "scene_ref": "mvp-inline:scene_daily_explore_firewood",
    "location": "清风渡客栈·后院柴火堆",
    "speaker": "旁白",
    "mood_tag": "警觉·线索",
    "plot_tags": ["daily", "explore", "fire_night_warned"],
    "save_point": False,
    "character_appearances": [],
    "note": "第二次闲逛·柴火堆：发现灯油痕迹 → fire_night_warned（走水夜可提前警觉）。",
    "choices": [
        {"choice_id": "explore_firewood_return", "text": "继续", "target_node": "scene_daily_return", "effects": {}}
    ],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_day", "sfx": ["sfx_footstep_wet"]}
}

# 3. 新增：第三次闲逛风险判定（安全/逃脱/已暴露×未识破→死亡【淹死在自己的好奇心里】/洞察≥4→隐藏线）
nodes['scene_daily_explore_third'] = {
    "node_id": "scene_daily_explore_third",
    "scene_ref": "mvp-inline:scene_daily_explore_third",
    "location": "清风渡客栈·后院",
    "speaker": "旁白",
    "mood_tag": "紧绷·生死一线",
    "plot_tags": ["daily", "explore", "third", "risk_check", "death_gate"],
    "save_point": True,
    "character_appearances": [],
    "note": "第三次闲逛风险判定：exposed&&!recognized_scar→死亡【淹死在自己的好奇心里】；watched→逃脱；其余安全；洞察≥4 解锁隐藏线【得闲饮茶】。",
    "choices": [
        {
            "choice_id": "third_drown",
            "text": "（死亡结局）",
            "target_node": "ending_drown_curiosity",
            "effects": {},
            "conditions": {"exposed": True, "recognized_scar": False}
        },
        {
            "choice_id": "third_escape",
            "text": "（被盯上，借花瓶反光逃脱）",
            "target_node": "scene_daily_explore_third_escape",
            "effects": {"watched": True},
            "conditions": {"watched": True, "exposed": False}
        },
        {
            "choice_id": "third_safe_unlock",
            "text": "（安全返回，解锁隐藏线）",
            "target_node": "scene_daily_explore_third_safe",
            "effects": {"hidden_line_unlocked": True, "fragments": 1, "insight": 1},
            "conditions": {"insight": {"op": "gte", "value": 4}}
        },
        {
            "choice_id": "third_safe",
            "text": "（安全返回）",
            "target_node": "scene_daily_explore_third_safe",
            "effects": {},
            "conditions": {}
        }
    ],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_night", "sfx": ["sfx_footstep_wet"]}
}

nodes['scene_daily_explore_third_escape'] = {
    "node_id": "scene_daily_explore_third_escape",
    "scene_ref": "mvp-inline:scene_daily_explore_third_escape",
    "location": "清风渡客栈·走廊",
    "speaker": "旁白",
    "mood_tag": "逃脱·惊险",
    "plot_tags": ["daily", "explore", "third_escape"],
    "save_point": False,
    "character_appearances": [],
    "note": "第三次闲逛·被盯上逃脱：损失一次行动时段（action_count 由选择时已 +1，此处不再补）。",
    "choices": [
        {"choice_id": "third_escape_return", "text": "继续", "target_node": "scene_daily_return", "effects": {}}
    ],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_night", "sfx": ["sfx_footstep_wet"]}
}

nodes['scene_daily_explore_third_safe'] = {
    "node_id": "scene_daily_explore_third_safe",
    "scene_ref": "mvp-inline:scene_daily_explore_third_safe",
    "location": "清风渡客栈·后院",
    "speaker": "旁白",
    "mood_tag": "安全·余悸",
    "plot_tags": ["daily", "explore", "third_safe", "hidden_line"],
    "save_point": False,
    "character_appearances": [],
    "note": "第三次闲逛·安全返回：洞察≥4 时已由上一节点解锁隐藏线【得闲饮茶】。",
    "choices": [
        {"choice_id": "third_safe_return", "text": "继续", "target_node": "scene_daily_return", "effects": {}}
    ],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_day", "sfx": ["sfx_footstep_wet"]}
}

# 4. 新增：死亡结局【淹死在自己的好奇心里】
nodes['ending_drown_curiosity'] = {
    "node_id": "ending_drown_curiosity",
    "scene_ref": "mvp-inline:ending_drown_curiosity",
    "location": "清风渡客栈·后院",
    "speaker": "旁白",
    "mood_tag": "结局·余韵",
    "plot_tags": ["ending", "淹死在自己的好奇心里", "p2"],
    "save_point": False,
    "terminal": True,
    "character_appearances": [],
    "text": "你走在后院，身后脚步声不紧不慢。你回头，看见伙计站在三步之外。他端着茶盘，笑容妥帖。\n\n“客官，您不该上二楼那间房的。”\n\n他手中的火折子亮了。",
    "choices": [],
    "audio": {"bgm": "bgm_inn_daily", "ambient": "amb_inn_night", "sfx": ["sfx_footstep_wet"]}
}

with open(BT, 'w', encoding='utf-8') as f:
    json.dump(bt, f, ensure_ascii=False, indent=2)
print('branch-tree 更新完成，节点数:', len(nodes))

# ============ final-dialogue 补充 ============
with open(FD, encoding='utf-8') as f:
    fd = json.load(f)
fnd = fd['nodes']

fnd['scene_daily_explore_firewood'] = {
    "speaker": "旁白",
    "text": "你绕到后院柴火堆旁。\n\n堆边有一滩没干透的油渍，颜色发深，凑近了能闻到一股灯油味。柴火垛码得整整齐齐，油却泼得像是急急忙忙倒的。\n\n你蹲下看了一眼，把这地方记在心里。"
}
fnd['scene_daily_explore_third_escape'] = {
    "speaker": "旁白",
    "text": "你走在走廊里，听见身后有脚步声靠近。\n\n你借着走廊上花瓶的反光，看见伙计站在三步之外。\n\n你当机侧身闪进空房，从后窗翻了出去。\n\n——逃过一劫。"
}
fnd['scene_daily_explore_third_safe'] = {
    "speaker": "旁白",
    "text": "你走在后院，感觉有人在看你。\n\n你回头，伙计站在远处，手里端着茶盘对你笑笑，没有靠近就去忙自己的事情了。\n\n你随便看了看，也回去了。"
}

with open(FD, 'w', encoding='utf-8') as f:
    json.dump(fd, f, ensure_ascii=False, indent=2)
print('final-dialogue 更新完成，节点数:', len(fnd))

# ============ 数值设计登记新 flag ============
ND = 'gotbotgame/data/numerical-design.json'
with open(ND, encoding='utf-8') as f:
    nd = json.load(f)
nd['flags']['returned_early'] = {"description": "A1 折返：错过第一天，感情结局解锁难度上升"}
nd['flags']['ach_meet_noise'] = {"description": "成就【低山臭水遇噪音】"}
nd['flags']['liu_tea_first_done'] = {"description": "柳茶首次互动已完成，后续再来展示重复选项"}
nd['flags']['explore_count'] = {"description": "闲逛次数累计（首次必后院/二次三选一/三次风险判定）"}
nd['flags']['liu_private_done'] = {"description": "柳陆书私下邀约已触发"}
nd['flags']['li_private_done'] = {"description": "黎客颍私下邀约已触发"}
nd['flags']['gui_private_done'] = {"description": "归汉私下邀约已触发"}
nd['choice_value_mapping']['chapter3_liu_tea'] = {
    "first_a_joke": {"liu_affection": 5, "liu_tea_first_done": True},
    "first_b_return_favor": {"liu_affection": 0, "liu_tea_first_done": True},
    "first_c_rude": {"liu_affection": -10, "liu_tea_first_done": True},
    "repeat_a_remember": {"liu_affection": 10, "fragments": 1},
    "repeat_b_mirror": {"liu_affection": 10},
    "repeat_c_listen": {"liu_affection": 15, "insight": 1},
    "repeat_d_weather": {"liu_affection": -10},
    "repeat_e_ask_secret": {"liu_affection": -20, "flag": "liu_refused"}
}
with open(ND, 'w', encoding='utf-8') as f:
    json.dump(nd, f, ensure_ascii=False, indent=2)
print('numerical-design 更新完成')
print('=== S7-S8 完成 ===')
