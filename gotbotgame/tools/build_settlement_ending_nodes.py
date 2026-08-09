# -*- coding: utf-8 -*-
"""P2 结算页+走水夜+结局路由：扩展 branch-tree-mvp.json
day3_close 去 terminal → scene_day3_summary → fire_night_transition → fire_night
→ outcome → post_fire_night → route_split → solo_gate → ending_gate → 18 个 ending_* 节点。
结局叙事取��� endings-full.json（零改写）。
"""
import json, shutil, os

BT = 'data/branch-tree-mvp.json'
EF = 'data/endings-full.json'
shutil.copyfile(BT, BT + '.bak_settlement')

bt = json.load(open(BT, encoding='utf-8'))
ef = json.load(open(EF, encoding='utf-8'))['endings']

nodes = bt['nodes']

# 1) day3_close 去 terminal，接入结算页
dc = nodes['scene_day3_close']
dc['terminal'] = False
dc['choices'] = [{
    'choice_id': 'day3_to_summary', 'text': '熄灯睡下',
    'target_node': 'scene_day3_summary', 'effects': {}
}]

# 2) 流程节点
flow = {
    'scene_day3_summary': {
        'node_id': 'scene_day3_summary', 'scene_ref': 'mvp-inline:scene_day3_summary',
        'location': '清风渡客栈·客房', 'speaker': '旁白', 'mood_tag': '结算·余韵',
        'plot_tags': ['settlement', 'summary', 'p2'], 'save_point': True,
        'character_appearances': [],
        'note': '三日结算页：数值统计由 SettlementPanel 展示，此处仅旁白标题。选项由面板按钮触发（choice_id=day3_to_fire_night）。',
        'choices': [{'choice_id': 'day3_to_fire_night', 'text': '（结算面板继续）',
                     'target_node': 'scene_fire_night_transition', 'effects': {}}],
        'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_night', 'sfx': []}
    },
    'scene_fire_night_transition': {
        'node_id': 'scene_fire_night_transition', 'scene_ref': 'mvp-inline:scene_fire_night_transition',
        'location': '清风渡客栈·客房', 'speaker': '旁白', 'mood_tag': '过渡·骤变',
        'plot_tags': ['fire_night', 'transition', 'p2'], 'save_point': True,
        'character_appearances': [],
        'choices': [{'choice_id': 'fn_t_go', 'text': '循声出去看看', 'target_node': 'scene_fire_night', 'effects': {}}],
        'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_night', 'sfx': ['sfx_footstep_wet']}
    },
    'scene_fire_night': {
        'node_id': 'scene_fire_night', 'scene_ref': 'scenes/fire_night.scene.md',
        'location': '清风渡客栈·二楼走廊 / 楼下院中', 'speaker': '旁白', 'mood_tag': '火·危急',
        'plot_tags': ['fire_night', 'event', 'p2'], 'save_point': True,
        'character_appearances': [],
        'choices': [
            {'choice_id': 'fire_help_liu_upstairs', 'text': '冲上楼，跟着柳陆书一起把人扶出来。',
             'target_node': 'scene_fire_night_outcome', 'effects': {'gui_affection': 5, 'liu_affection': 5, 'insight': 1}},
            {'choice_id': 'fire_help_li_below', 'text': '留在楼下帮黎客颍——搬水、递湿毛巾，接住跳下来的人。',
             'target_node': 'scene_fire_night_outcome', 'effects': {'li_affection': 10, 'fragments': 1}},
            {'choice_id': 'fire_warn_alerted', 'text': '先看了一眼火势：这不是普通的走水。提醒黎客颍看火是从哪儿起来的。',
             'target_node': 'scene_fire_night_outcome', 'effects': {'insight': 1, 'li_affection': 5},
             'conditions': {'fire_night_warned': True}},
            {'choice_id': 'fire_find_innkeeper', 'text': '跑去找伙计要水桶和灭火的沙土。',
             'target_node': 'scene_fire_night_outcome', 'effects': {'action_count': 1}}
        ],
        'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_night', 'sfx': ['sfx_door_open', 'sfx_candle_crackle']}
    },
    'scene_fire_night_outcome': {
        'node_id': 'scene_fire_night_outcome', 'scene_ref': 'mvp-inline:scene_fire_night_outcome',
        'location': '清风渡客栈·楼下院中', 'speaker': '旁白', 'mood_tag': '火后·余烬',
        'plot_tags': ['fire_night', 'outcome', 'p2'], 'save_point': True,
        'character_appearances': [],
        'note': '走水夜结果：若已暴露且三好感均低（无人接应）→ 死亡·替人挡了刀；否则进入后续。',
        'choices': [
            {'choice_id': 'fn_o_sacrifice', 'text': '（火中意外，替人挡了刀）',
             'target_node': 'ending_sacrifice', 'effects': {},
             'conditions': {'exposed': True, 'liu_affection': {'op': 'lte', 'value': -1},
                            'li_affection': {'op': 'lte', 'value': -1}, 'gui_affection': {'op': 'lte', 'value': -1}}},
            {'choice_id': 'fn_o_after', 'text': '回房歇下', 'target_node': 'scene_post_fire_night', 'effects': {}}
        ],
        'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_night', 'sfx': []}
    },
    'scene_post_fire_night': {
        'node_id': 'scene_post_fire_night', 'scene_ref': 'mvp-inline:scene_post_fire_night',
        'location': '清风渡客栈·大堂', 'speaker': '旁白', 'mood_tag': '暗涌·余韵',
        'plot_tags': ['fire_night', 'hidden_line', 'p2'], 'save_point': True,
        'character_appearances': [],
        'note': '走水夜后：已解锁隐藏线可探查第三张桌（得闲饮茶）；否则直接进入路线分歧。',
        'choices': [
            {'choice_id': 'pfn_tea', 'text': '再去看看靠门第三张桌。',
             'target_node': 'ending_tea', 'effects': {'observed_account_book': True},
             'conditions': {'hidden_line_unlocked': True}},
            {'choice_id': 'pfn_route', 'text': '回房休息', 'target_node': 'scene_route_split', 'effects': {}}
        ],
        'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_night', 'sfx': []}
    },
    'scene_route_split': {
        'node_id': 'scene_route_split', 'scene_ref': 'mvp-inline:scene_route_split',
        'location': '清风渡客栈·大堂', 'speaker': '旁白', 'mood_tag': '抉择',
        'plot_tags': ['route_split', 'p2'], 'save_point': True,
        'character_appearances': [],
        'choices': [
            {'choice_id': 'route_coop', 'text': '与三人同行，一起去观澜阁。',
             'target_node': 'scene_ending_gate', 'effects': {'route_coop': True}},
            {'choice_id': 'route_solo', 'text': '独自先行，先到观澜阁一步。',
             'target_node': 'scene_solo_gate', 'effects': {'route_solo': True}}
        ],
        'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_day', 'sfx': []}
    },
    'scene_solo_gate': {
        'node_id': 'scene_solo_gate', 'scene_ref': 'mvp-inline:scene_solo_gate',
        'location': '清风渡·后山路口', 'speaker': '旁白', 'mood_tag': '独行·警觉',
        'plot_tags': ['solo', 'p2'], 'save_point': True,
        'character_appearances': [],
        'note': '独行线：被标记诱饵(bait_marked)时可走伙计说的密道（→信错了人）；否则绕大路或独自摸黑。',
        'choices': [
            {'choice_id': 'solo_trap', 'text': '按伙计说的密道走——北走三里，歪脖子老槐树底下。',
             'target_node': 'ending_betrayed', 'effects': {'solo_night_explore': True},
             'conditions': {'bait_marked': True}},
            {'choice_id': 'solo_road', 'text': '绕大路，天亮后再走。', 'target_node': 'scene_ending_gate', 'effects': {}},
            {'choice_id': 'solo_direct', 'text': '独自摸黑进观澜阁。', 'target_node': 'scene_ending_gate', 'effects': {}}
        ],
        'audio': {'bgm': 'bgm_rain_intro', 'ambient': 'sfx_rain_continuous', 'sfx': ['sfx_footstep_wet']}
    },
}

# 3) 结局路由节点（按数值设计优先级顺序，条件用顺序裁剪表达）
gate_choices = [
    {'choice_id': 'to_fight', 'text': '（三人反目）', 'target_node': 'ending_fight',
     'conditions': {'liu_affection': {'op': 'lte', 'value': -11}, 'li_affection': {'op': 'lte', 'value': -11},
                    'gui_affection': {'op': 'lte', 'value': -11}}},
    {'choice_id': 'to_missed', 'text': '（错过真相）', 'target_node': 'ending_missed',
     'conditions': {'fragments': {'op': 'lte', 'value': 2}}},
    {'choice_id': 'to_crushed', 'text': '（被真相压垮）', 'target_node': 'ending_crushed',
     'conditions': {'fragments': {'op': 'gte', 'value': 6}, 'insight': {'op': 'lte', 'value': 1}}},
    {'choice_id': 'to_half', 'text': '（一知半解）', 'target_node': 'ending_half',
     'conditions': {'fragments': {'op': 'gte', 'value': 3}, 'insight': {'op': 'lte', 'value': 3}}},
    {'choice_id': 'to_seal_break', 'text': '（封印破碎）', 'target_node': 'ending_seal_break',
     'conditions': {'fragments': {'op': 'lte', 'value': 3}}},
    {'choice_id': 'to_truth', 'text': '（真相达成）', 'target_node': 'ending_truth',
     'conditions': {'fragments': {'op': 'gte', 'value': 8}, 'insight': {'op': 'gte', 'value': 6}}},
    {'choice_id': 'to_liu_cp', 'text': '（扇底风）', 'target_node': 'ending_liu_cp',
     'conditions': {'liu_affection': {'op': 'gte', 'value': 70}}},
    {'choice_id': 'to_li_cp', 'text': '（归刀入鞘）', 'target_node': 'ending_li_cp',
     'conditions': {'li_affection': {'op': 'gte', 'value': 70}}},
    {'choice_id': 'to_gui_cp', 'text': '（长剑有穗）', 'target_node': 'ending_gui_cp',
     'conditions': {'gui_affection': {'op': 'gte', 'value': 70}}},
    {'choice_id': 'to_liu_cb', 'text': '（旧友新茶）', 'target_node': 'ending_liu_cb',
     'conditions': {'liu_affection': {'op': 'gte', 'value': 30}}},
    {'choice_id': 'to_li_cb', 'text': '（同路之人）', 'target_node': 'ending_li_cb',
     'conditions': {'li_affection': {'op': 'gte', 'value': 30}}},
    {'choice_id': 'to_gui_cb', 'text': '（不冻泉）', 'target_node': 'ending_gui_cb',
     'conditions': {'gui_affection': {'op': 'gte', 'value': 30}}},
    {'choice_id': 'to_solo', 'text': '（独行者）', 'target_node': 'ending_solo',
     'conditions': {'route_solo': True, 'insight': {'op': 'gte', 'value': 6}}},
    {'choice_id': 'to_pass', 'text': '（清风过客）', 'target_node': 'ending_pass',
     'conditions': {'fragments': {'op': 'gte', 'value': 4}}},
    {'choice_id': 'to_stranger', 'text': '（陌生人）', 'target_node': 'ending_stranger',
     'conditions': {'liu_affection': {'op': 'lte', 'value': 29}, 'li_affection': {'op': 'lte', 'value': 29},
                    'gui_affection': {'op': 'lte', 'value': 29}}},
]
flow['scene_ending_gate'] = {
    'node_id': 'scene_ending_gate', 'scene_ref': 'mvp-inline:scene_ending_gate',
    'location': '观澜阁', 'speaker': '旁白', 'mood_tag': '终局·判定',
    'plot_tags': ['ending_gate', 'p2'], 'save_point': True,
    'character_appearances': [],
    'note': '结局路由：按数值设计优先级（death→hidden→truth→cp→cb→solo→neutral→distant）顺序判定，条件互斥。',
    'choices': gate_choices,
    'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_night', 'sfx': []}
}

# 4) 结局节点（叙事取自 endings-full.json，零改写）
ENDING_MAP = {
    'ending_sacrifice': '替人挡了刀',
    'ending_betrayed': '信错了人',
    'ending_tea': '得闲饮茶',
    'ending_fight': '三人反目',
    'ending_seal_break': '封印破碎',
    'ending_missed': '错过真相',
    'ending_half': '一知半解',
    'ending_crushed': '被真相压垮',
    'ending_truth': '真相达成',
    'ending_liu_cp': '扇底风_liu_cp',
    'ending_li_cp': '归刀入鞘_li_cp',
    'ending_gui_cp': '长剑有穗_gui_cp',
    'ending_liu_cb': '旧友新茶_liu_cb',
    'ending_li_cb': '同路之人_li_cb',
    'ending_gui_cb': '不冻泉_gui_cb',
    'ending_solo': '独行者',
    'ending_pass': '清风过客',
    'ending_stranger': '陌生人',
}
for nid, ekey in ENDING_MAP.items():
    entry = ef[ekey]
    nodes[nid] = {
        'node_id': nid, 'scene_ref': 'mvp-inline:' + nid,
        'location': '观澜阁·结局', 'speaker': '旁白', 'mood_tag': '结局·余韵',
        'plot_tags': ['ending', ekey, 'p2'], 'save_point': False,
        'character_appearances': [], 'terminal': True,
        'text': str(entry['narration']),
        'choices': [],
        'audio': {'bgm': 'bgm_inn_daily', 'ambient': 'amb_inn_night', 'sfx': []}
    }

# 5) 合并写回
nodes.update(flow)
bt['nodes'] = nodes
json.dump(bt, open(BT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print('OK: 节点数 %d -> %d' % (33, len(nodes)))
print('新增流程节点:', list(flow.keys()))
print('新增结局节点:', list(ENDING_MAP.keys()))
