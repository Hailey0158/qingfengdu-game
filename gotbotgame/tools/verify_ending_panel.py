# -*- coding: utf-8 -*-
"""P3 ending_panel 静态校验"""
import json, re, sys

fail = 0
def check(cond, msg):
    global fail
    print(('✅' if cond else '❌') + ' ' + msg)
    if not cond: fail += 1

# JSON
for p in ['gotbotgame/data/endings-full.json', 'gotbotgame/data/branch-tree-mvp.json']:
    with open(p, encoding='utf-8') as f:
        json.load(f)
    check(True, f'JSON: {p}')

# endings-full 含 ending_page
with open('gotbotgame/data/endings-full.json', encoding='utf-8') as f:
    e = json.load(f)
has_page = sum(1 for k, ed in e['endings'].items() if 'ending_page' in ed)
check(has_page == 20, f'20 结局含 ending_page（实际 {has_page}）')
check(len(e.get('node_to_ending', {})) == 20, f'node_to_ending 映射 20 项（实际 {len(e.get("node_to_ending", {}))}）')

# 分支树 ending 节点与 node_to_ending 对齐
with open('gotbotgame/data/branch-tree-mvp.json', encoding='utf-8') as f:
    bt = json.load(f)
bt_endings = [nid for nid in bt['nodes'] if nid.startswith('ending_')]
check(len(bt_endings) == 20, f'分支树 20 个 ending 节点（实际 {len(bt_endings)}）')
mapped = [nid for nid in bt_endings if nid in e.get('node_to_ending', {})]
check(len(mapped) == 20, f'全部 ending 节点已映射（{len(mapped)}/20）')

# GDScript 括号平衡（逐行剥离字符串与注释）
def gd_balance(path):
    s = open(path, encoding='utf-8').read()
    lines = s.split('\n')
    clean = []
    for line in lines:
        in_str = None
        res = []
        j = 0
        while j < len(line):
            ch = line[j]
            if in_str:
                if ch == '\\' and j + 1 < len(line):
                    j += 2
                    continue
                if ch == in_str:
                    in_str = None
                j += 1
                continue
            if ch in ('"', "'"):
                in_str = ch
                j += 1
                continue
            if ch == '#':
                break
            res.append(ch)
            j += 1
        clean.append(''.join(res))
    code = ''.join(clean)
    bal = code.count('{') - code.count('}') + code.count('(') - code.count(')') + code.count('[') - code.count(']')
    return bal

for p in ['gotbotgame/scripts/ending_panel.gd', 'gotbotgame/scripts/mvp_ui_controller.gd', 'gotbotgame/scripts/mvp_scene_runner.gd']:
    bal = gd_balance(p)
    check(bal == 0, f'{p}: bracket balance = {bal}')

# mvp_ui_controller 含 ending_panel 引用与 replay handler
ui = open('gotbotgame/scripts/mvp_ui_controller.gd', encoding='utf-8').read()
check('ending_panel' in ui, 'UI 引用 ending_panel')
check('_on_ending_replay' in ui, 'UI 含 _on_ending_replay')
check('runner.is_terminal(node_id)' in ui, 'UI 检测 terminal ending 节点')

# ending_panel.gd 含 refresh + replay_pressed signal
ep = open('gotbotgame/scripts/ending_panel.gd', encoding='utf-8').read()
check('func refresh' in ep, 'ending_panel 含 refresh()')
check('signal replay_pressed' in ep, 'ending_panel 含 replay_pressed signal')

# tscn 挂载
mt = open('gotbotgame/scenes/main.tscn', encoding='utf-8').read()
check('EndingPanel' in mt and 'ending_panel.tscn' in mt, 'main.tscn 挂载 EndingPanel')

print(f'\n=== 校验结果: {"全部通过 ✅" if fail == 0 else str(fail)+" 项失败 ❌"} ===')
sys.exit(0 if fail == 0 else 1)
