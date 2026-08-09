# -*- coding: utf-8 -*-
"""全流程模拟：验证 章节->初识->三天九时段->收束 的节点路由、天/时段同步、状态栏可见性"""
import json

branch = json.load(open('data/branch-tree-mvp.json', encoding='utf-8'))
nodes = branch['nodes']

SLOT_NAMES = ["上午", "下午", "夜"]


def is_ch3(node_id):
    if node_id.startswith('scene_daily_'):
        return True
    return node_id in ['scene_day1_close', 'scene_day2_close', 'scene_day3_close']


def sync_day_slot(scene_id, state):
    if scene_id.startswith('scene_daily_day'):
        parts = scene_id.split('_')  # scene_daily_day1_01
        if len(parts) >= 4:
            state['day'] = int(parts[2].removeprefix('day'))
            state['slot'] = max(1, min(3, int(parts[3])))
    elif scene_id.endswith('_close'):
        parts = scene_id.split('_')
        if len(parts) >= 2:
            state['day'] = int(parts[1].removeprefix('day'))
            state['slot'] = 3


def status_label(state):
    if is_ch3(state['node']):
        return '第 %d 天 · %s' % (state['day'], SLOT_NAMES[state['slot'] - 1])
    return '(隐藏)'


state = {'node': 'ch1_title', 'day': 1, 'slot': 1, 'action_count': 0}
print('== 第一章/第二章：时间标记应隐藏 ==')
for nid in ['ch1_title', 'scene_001a_rain_lantern', 'scene_001b_innkeeper', 'scene_001c_choices',
            'scene_002_path', 'scene_003_pay_all', 'ch2_title', 'scene_010_meet',
            'scene_020_liu_day1', 'scene_030_li_day1', 'scene_040_gui_day1']:
    state['node'] = nid
    sync_day_slot(nid, state)
    lbl = status_label(state)
    assert lbl == '(隐藏)', (nid, lbl)
print('  PASS: 全部隐藏')

print('== 第三章：按节点推进 ==')
route = [
    ('scene_daily_day1_01', '第 1 天 · 上午'),
    ('scene_daily_day1_02', '第 1 天 · 下午'),
    ('scene_daily_day1_03', '第 1 天 · 夜'),
    ('scene_day1_close', '第 1 天 · 夜'),
    ('scene_daily_day2_01', '第 2 天 · 上午'),
    ('scene_daily_day2_02', '第 2 天 · 下午'),
    ('scene_daily_day2_03', '第 2 天 · 夜'),
    ('scene_day2_close', '第 2 天 · 夜'),
    ('scene_daily_day3_01', '第 3 天 · 上午'),
    ('scene_daily_day3_02', '第 3 天 · 下午'),
    ('scene_daily_day3_03', '第 3 天 · 夜'),
    ('scene_day3_close', '第 3 天 · 夜'),
]
for nid, expect in route:
    state['node'] = nid
    sync_day_slot(nid, state)
    lbl = status_label(state)
    assert lbl == expect, (nid, lbl, expect)
print('  PASS: 12 个节点时间推进全部正确')

print('== 行动类节点（动作/返回）：继承当前天时段 ==')
for nid in ['scene_daily_liu_tea', 'scene_daily_li_clues', 'scene_daily_gui_sit',
            'scene_daily_gui_sit_first', 'scene_daily_explore', 'scene_daily_innkeeper',
            'scene_daily_return']:
    state['node'] = nid
    sync_day_slot(nid, state)
    lbl = status_label(state)
    assert lbl == '第 %d 天 · %s' % (state['day'], SLOT_NAMES[state['slot'] - 1]), (nid, lbl)
print('  PASS: 行动/返回节点时间继承正确')

print('== 每个时段节点最多可见选项数（<=5，保证不溢出选项面板）==')
for nid, node in nodes.items():
    if nid.startswith('scene_daily_day'):
        visible = [c for c in node.get('choices', []) if not c.get('conditions')]
        cond = [c for c in node.get('choices', []) if c.get('conditions')]
        # 归汉双段为条件互斥对，最多同时显示其一
        max_visible = len(visible) + min(len(cond), 1)
        assert max_visible <= 5, (nid, max_visible, node['choices'])
        print('  %s: 无条件%d + 条件%d -> 最多%d个可见' % (nid, len(visible), len(cond), max_visible))
print('PASS: 全部时段最多5个选项（面板 286px 可容纳 5*40+4*8=232px）')
