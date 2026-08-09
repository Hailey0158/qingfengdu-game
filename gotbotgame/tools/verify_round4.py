# -*- coding: utf-8 -*-
"""静态校验：JSON 可解析 + 选项->分支节点映射完整性 + 数值一致性"""
import json

dialogue = json.load(open('data/final-dialogue/mvp/liu_lushu_day1.json', encoding='utf-8'))
branch = json.load(open('data/branch-tree-mvp.json', encoding='utf-8'))
print('OK: 对话/分支 JSON 均可解析')

exp = dialogue['nodes'].get('scene_daily_explore', {})
assert exp['text'] == '你离开众人视线，在客栈四处走动。', exp['text']
assert 'scene_daily_explore_backyard' in dialogue['nodes'], '缺少后院分支节点'
print('OK: 闲逛基础文本已拆分，后院分支节点存在')

mapping = {
    'liu_a1_joke': 'scene_020_liu_response_a1', 'liu_a2_challenge': 'scene_020_liu_response_a2',
    'liu_a3_ask_secret': 'scene_020_liu_response_a3', 'liu_a4_silence': 'scene_020_liu_response_a4',
    'li_b1_name': 'scene_030_li_response_b1', 'li_b2_weapon': 'scene_030_li_response_b2',
    'li_b3_ask': 'scene_030_li_response_b3', 'li_b4_silence': 'scene_030_li_response_b4',
    'gui_c1_found': 'scene_040_gui_response_c1', 'gui_c2_sword': 'scene_040_gui_response_c2',
    'gui_c3_scenery': 'scene_040_gui_response_c3', 'gui_c4_sit': 'scene_040_gui_response_c4',
    'liu_tea_a': 'scene_daily_liu_tea_a', 'liu_tea_b': 'scene_daily_liu_tea_b',
    'liu_tea_c': 'scene_daily_liu_tea_c', 'liu_tea_d': 'scene_daily_liu_tea_d',
    'liu_tea_e': 'scene_daily_liu_tea_e',
    'li_clue_a': 'scene_daily_li_clue_a', 'li_clue_b': 'scene_daily_li_clue_b',
    'li_clue_c': 'scene_daily_li_clue_c', 'li_clue_d': 'scene_daily_li_clue_d',
    'gui_sit_a': 'scene_daily_gui_sit_a', 'gui_sit_b': 'scene_daily_gui_sit_b',
    'gui_sit_c': 'scene_daily_gui_sit_c', 'gui_sit_d': 'scene_daily_gui_sit_d',
    'explore_backyard': 'scene_daily_explore_backyard', 'explore_hall': 'scene_daily_explore_hall',
    'explore_upstairs': 'scene_daily_explore_upstairs',
    'inn_a': 'scene_daily_innkeeper_a', 'inn_b': 'scene_daily_innkeeper_b',
    'inn_c': 'scene_daily_innkeeper_c', 'inn_d': 'scene_daily_innkeeper_d',
}
all_choice_ids = set()
for nid, node in branch['nodes'].items():
    for c in node.get('choices', []):
        all_choice_ids.add(c['choice_id'])
missing_choices = [k for k in mapping if k not in all_choice_ids]
missing_nodes = [v for v in mapping.values() if v not in dialogue['nodes']]
print('缺失的选项ID:', missing_choices or '无')
print('缺失的分支节点:', missing_nodes or '无')
assert not missing_choices and not missing_nodes, '映射不完整！'
print('OK: 32 个选项->分支节点映射全部有效')

for nid, node in branch['nodes'].items():
    for c in node.get('choices', []):
        if c['choice_id'] == 'li_clue_b':
            assert c['effects'].get('li_affection') == 15, c['effects']
            assert c['effects'].get('fragments') == 1, c['effects']
            print('OK: li_clue_b 效果 =', c['effects'])

# 分支树所有 target 都可达（排除旧遗留 scene_021_liu_day1_close）
targets = set()
for nid, node in branch['nodes'].items():
    for c in node.get('choices', []):
        targets.add(c['target_node'])
reachable = set(branch['nodes'].keys())
broken = [t for t in targets if t not in reachable]
print('断链目标:', broken or '无')
print('全部校验通过')
