# -*- coding: utf-8 -*-
"""模拟结局路由（scene_ending_gate）条件判定，验证典型数值路径"""
import json

bt = json.load(open('data/branch-tree-mvp.json', encoding='utf-8'))
gate = bt['nodes']['scene_ending_gate']['choices']


def cond_met(conds, s):
    for k, v in conds.items():
        actual = s.get(k, s.get('flags', {}).get(k, 0))
        if isinstance(v, bool):
            if bool(s.get('flags', {}).get(k, False)) != v:
                return False
        elif isinstance(v, (int, float)):
            if actual < int(v):
                return False
        elif isinstance(v, dict):
            val = int(v.get('value', 0))
            op = v.get('op')
            if op == 'gte' and actual < val:
                return False
            if op == 'lte' and actual > val:
                return False
            if op == 'eq' and actual != val:
                return False
            if op == 'neq' and actual == val:
                return False
    return True


def route(s):
    for c in gate:
        if cond_met(c.get('conditions', {}), s):
            return c['target_node']
    return 'NONE'


cases = [
    ('真相达成', {'insight': 7, 'fragments': 9, 'liu_affection': 75, 'li_affection': 20, 'gui_affection': 20}, 'ending_truth'),
    ('柳CP', {'insight': 5, 'fragments': 5, 'liu_affection': 75, 'li_affection': 20, 'gui_affection': 20}, 'ending_liu_cp'),
    ('黎CB', {'insight': 5, 'fragments': 5, 'liu_affection': 20, 'li_affection': 45, 'gui_affection': 20}, 'ending_li_cb'),
    ('错过真相', {'insight': 0, 'fragments': 1}, 'ending_missed'),
    ('被真相压垮', {'insight': 1, 'fragments': 9}, 'ending_crushed'),
    ('一知半解', {'insight': 2, 'fragments': 4}, 'ending_half'),
    ('封印破碎', {'insight': 5, 'fragments': 3}, 'ending_seal_break'),
    ('三人反目', {'insight': 5, 'fragments': 5, 'liu_affection': -20, 'li_affection': -20, 'gui_affection': -20}, 'ending_fight'),
    ('独行者', {'insight': 7, 'fragments': 5, 'flags': {'route_solo': True}}, 'ending_solo'),
    ('清风过客', {'insight': 4, 'fragments': 5, 'liu_affection': 10, 'li_affection': 10, 'gui_affection': 10}, 'ending_pass'),
    ('陌生人(f8低好感)', {'insight': 4, 'fragments': 8, 'liu_affection': 10, 'li_affection': 10, 'gui_affection': 10}, 'ending_stranger'),
    ('全低好感低碎片', {'insight': 0, 'fragments': 0, 'liu_affection': -5, 'li_affection': -5, 'gui_affection': -5}, 'ending_missed'),
]
ok = True
for name, s, expect in cases:
    got = route(s)
    status = 'OK' if got == expect else 'FAIL'
    if got != expect:
        ok = False
    print('[%s] %s -> %s (期望 %s)' % (status, name, got, expect))
print('结局路由模拟:', '全部通过' if ok else '存在失败')
assert ok
