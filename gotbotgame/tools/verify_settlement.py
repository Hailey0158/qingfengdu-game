# -*- coding: utf-8 -*-
"""P2 结算/走水夜/结局路由 静态校验"""
import json, re

print('== 1. JSON 解析 ==')
bt = json.load(open('data/branch-tree-mvp.json', encoding='utf-8'))
dl = json.load(open('data/final-dialogue/mvp/liu_lushu_day1.json', encoding='utf-8'))
ef = json.load(open('data/endings-full.json', encoding='utf-8'))['endings']
nd = json.load(open('data/numerical-design.json', encoding='utf-8'))
print('OK: 4 个 JSON 均可解析; 分支树节点数 =', len(bt['nodes']))

nodes = bt['nodes']
print('== 2. 断链检查（所有 target_node 存在）==')
broken = []
for nid, node in nodes.items():
    for c in node.get('choices', []):
        t = c.get('target_node')
        if t and t not in nodes:
            broken.append((nid, c.get('choice_id'), t))
print('断链:', broken or '无')
assert not broken

print('== 3. 关键流程链 ==')
chain = ['scene_day3_close', 'scene_day3_summary', 'scene_fire_night_transition',
         'scene_fire_night', 'scene_fire_night_outcome', 'scene_post_fire_night',
         'scene_route_split', 'scene_solo_gate', 'scene_ending_gate']
for i in range(len(chain) - 1):
    src, dst = chain[i], chain[i + 1]
    targets = {c.get('target_node') for c in nodes[src].get('choices', [])}
    assert dst in targets, '链路断: %s 未指向 %s' % (src, dst)
print('OK: 结算→过渡→走水夜→结果→隐藏线→分歧→独行→结局路由 链路完整')

print('== 4. 结局节点 ==')
ending_nodes = [n for n in nodes if n.startswith('ending_')]
print('结局节点数:', len(ending_nodes), ending_nodes)
# 本轮新增的 18 个结局节点（ending_front_no_road 为 P1 既有开场彩蛋，文本来自 final-dialogue 简版）
NEW_ENDINGS = [n for n in ending_nodes if n != 'ending_front_no_road']
for n in ending_nodes:
    node = nodes[n]
    assert node.get('terminal') is True, n + ' 非 terminal'
    assert node.get('text'), n + ' 叙事为空'
for n in NEW_ENDINGS:
    node = nodes[n]
    assert node.get('text') in [e['narration'] for e in ef.values()], n + ' 叙事未在 endings-full 中'
print('OK: %d 个新增结局节点 terminal=true、叙事非空且取自已写文案; 既有 ending_front_no_road 正常' % len(NEW_ENDINGS))

print('== 5. 结局可达性（从入口 ch1_title 全图遍历）==')
from collections import deque
q = deque(['ch1_title'])
seen = set()
while q:
    n = q.popleft()
    if n in seen:
        continue
    seen.add(n)
    for c in nodes.get(n, {}).get('choices', []):
        t = c.get('target_node')
        if t:
            q.append(t)
unreachable = [n for n in nodes if n not in seen]
print('不可达节点:', unreachable or '无')
# 允许的例外：scene_021_liu_day1_close 为 P1 遗留终端节点（P2 起由三日九时段收束替代）
allowed = ['scene_021_liu_day1_close']
real_unreachable = [n for n in unreachable if n not in allowed]
print('实际不可达（排除遗留）:', real_unreachable or '无')
assert not real_unreachable, '存在真实不可达节点'

print('== 6. 条件格式（runner 支持 bool/int/dict{op,value}）==')
bad = []
for nid, node in nodes.items():
    for c in node.get('choices', []):
        for k, v in c.get('conditions', {}).items():
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                continue
            if isinstance(v, dict) and v.get('op') in ('gte', 'lte', 'eq', 'neq') and 'value' in v:
                continue
            bad.append((nid, k, v))
print('非法条件:', bad or '无')
assert not bad

print('== 7. 控制器背景映射覆盖全部节点 ==')
ctrl = open('scripts/mvp_ui_controller.gd', encoding='utf-8').read()
tex_map = ctrl[ctrl.index('const BACKGROUND_TEXTURES'):ctrl.index('const BACKGROUND_COLORS')]
missing = [n for n in nodes if ('"%s":' % n) not in tex_map]
print('缺失背景映射节点:', missing or '无')
assert not missing

print('== 8. 结算/过渡/走水夜旁白存在于 final-dialogue ==')
for k in ['scene_day3_summary', 'scene_fire_night_transition', 'scene_fire_night',
          'scene_fire_night_outcome', 'scene_route_split', 'scene_solo_gate']:
    assert k in dl['nodes'] and dl['nodes'][k].get('text'), k + ' 文案缺失'
print('OK: 6 段新旁白文案齐全')

print('P2 结算/走水夜/结局路由 校验全部通过')
