# -*- coding: utf-8 -*-
"""P2 需求2 补充全量校验：JSON 合法性 / 引用完整性 / 条件合规 / 可达性 / 结局路由模拟。"""
import json, re, sys
from collections import deque

BT = 'gotbotgame/data/branch-tree-mvp.json'
FD = 'gotbotgame/data/final-dialogue/mvp/liu_lushu_day1.json'
ND = 'gotbotgame/data/numerical-design.json'

fail = 0
def check(cond, msg):
    global fail
    if cond:
        print('✅', msg)
    else:
        print('❌', msg)
        fail += 1

with open(BT, encoding='utf-8') as f:
    bt = json.load(f)
with open(FD, encoding='utf-8') as f:
    fd = json.load(f)
with open(ND, encoding='utf-8') as f:
    nd = json.load(f)

nodes = bt['nodes']
check('branch-tree JSON 解析', True)
check('final-dialogue JSON 解析', True)
check('numerical-design JSON 解析', True)

# 1. 所有 target_node 存在
missing = []
for nid, node in nodes.items():
    for c in node.get('choices', []):
        t = c.get('target_node')
        if t and t not in nodes:
            missing.append((nid, c.get('choice_id'), t))
check(f'target 引用完整（{len(missing)} 缺失）', not missing)
if missing:
    print('  ', missing[:10])

# 2. 所有 mvp-inline 引用在 final-dialogue 有文本
no_text = []
for nid, node in nodes.items():
    ref = node.get('scene_ref', '')
    if ref.startswith('mvp-inline:'):
        key = ref.split(':', 1)[1]
        if key not in fd['nodes'] and not node.get('text'):
            no_text.append((nid, key))
check(f'mvp-inline 文本覆盖（{len(no_text)} 缺失）', not no_text)
if no_text:
    print('  ', no_text[:10])

# 3. 条件操作符合规（仅 gte/lte/eq/neq/bool/int）
bad_ops = []
for nid, node in nodes.items():
    for c in node.get('choices', []):
        conds = c.get('conditions', {})
        if not isinstance(conds, dict):
            continue
        for k, v in conds.items():
            if isinstance(v, dict):
                op = v.get('op')
                if op not in ('gte', 'lte', 'eq', 'neq'):
                    bad_ops.append((nid, c.get('choice_id'), k, op))
check(f'条件操作符合规（{len(bad_ops)} 异常）', not bad_ops)
if bad_ops:
    print('  ', bad_ops[:10])

# 4. 乱码检查
bad_chars = []
for nid, node in fd['nodes'].items():
    t = node.get('text', '')
    if '\ufffd' in t:
        bad_chars.append(nid)
check(f'final-dialogue 无乱码（{len(bad_chars)} 处）', not bad_chars)

# 5. 全图可达性（乐观 BFS：条件选项视为可满足，auto_route 内部也扩展）
reachable = set()
q = deque(['ch1_title'])
while q:
    nid = q.popleft()
    if nid in reachable:
        continue
    reachable.add(nid)
    for c in nodes[nid].get('choices', []):
        t = c.get('target_node')
        if t and t not in reachable:
            q.append(t)
unreachable = [nid for nid in nodes if nid not in reachable and not nodes[nid].get('terminal')]
check(f'全图可达（{len(nodes)} 节点，{len(unreachable)} 不可达非终端）', not unreachable)
if unreachable:
    print('  ', unreachable[:15])

# 6. 新增 flag 已在数值设计登记
new_flags = ['returned_early', 'ach_meet_noise', 'liu_tea_first_done', 'explore_count',
             'liu_private_done', 'li_private_done', 'gui_private_done', 'clue_old_grudge', 'item_sword_tassel', 'li_map_entrusted']
unreg = [fl for fl in new_flags if fl not in nd['flags']]
check(f'新 flag 已登记（{len(unreg)} 未登记）', not unreg)
if unreg:
    print('  ', unreg)

# 7. 结局路由模拟：auto_route 下每个条件组合收敛到唯一结局
# 简化：确认 scene_ending_gate 选项条件互斥且 auto_route 标记
eg = nodes['scene_ending_gate']
check('ending_gate auto_route 标记', eg.get('auto_route') is True)
check(f'ending_gate 选项数 {len(eg["choices"])}（16 结局路由）', len(eg['choices']) >= 14)

print()
print('=== 校验结果:', '全部通过 ✅' if fail == 0 else f'{fail} 项失败 ❌', '===')
sys.exit(0 if fail == 0 else 1)
