# -*- coding: utf-8 -*-
"""P2 结局自动收敛 + 补情节：静态校验脚本"""
import json, re, sys

def check_gd_balance(path: str) -> None:
    s = open(path, encoding="utf-8").read()
    # strip triple-quoted strings
    s = re.sub(r'""".*?"""', '', s, flags=re.S)
    s = re.sub(r"'''", '', s)
    # strip line comments (careful: keep strings)
    out_lines = []
    in_str = None
    for line in s.split('\n'):
        res = []
        i = 0
        while i < len(line):
            ch = line[i]
            if in_str:
                res.append(ch)
                if ch == '\\' and i + 1 < len(line):
                    res.append(line[i+1])
                    i += 2
                    continue
                if ch == in_str:
                    in_str = None
                i += 1
                continue
            if ch in ('"', "'"):
                # only treat as string if not preceded by # context
                in_str = ch
                res.append(ch)
            elif ch == '#':
                break
            else:
                res.append(ch)
            i += 1
        out_lines.append(''.join(res))
    s = ''.join(out_lines)
    bal = 0
    for ch in s:
        if ch in '({[':
            bal += 1
        elif ch in ')}]':
            bal -= 1
        if bal < 0:
            break
    print(f'{path}: bracket balance = {bal} (0=OK)')
    if bal != 0:
        sys.exit(1)

def main():
    for p in ['gotbotgame/data/branch-tree-mvp.json',
              'gotbotgame/data/final-dialogue/mvp/liu_lushu_day1.json']:
        with open(p, encoding='utf-8') as f:
            json.load(f)
        print('JSON OK:', p)

    for p in ['gotbotgame/scripts/mvp_scene_runner.gd',
              'gotbotgame/scripts/mvp_ui_controller.gd']:
        check_gd_balance(p)

    # verify auto_route node exists and runner references are consistent
    with open('gotbotgame/data/branch-tree-mvp.json', encoding='utf-8') as f:
        bt = json.load(f)
    eg = bt['nodes'].get('scene_ending_gate', {})
    print('scene_ending_gate auto_route =', eg.get('auto_route', False))
    assert eg.get('auto_route') is True, 'auto_route 标记缺失'

    runner_src = open('gotbotgame/scripts/mvp_scene_runner.gd', encoding='utf-8').read()
    assert 'func auto_route' in runner_src, 'runner auto_route 缺失'
    assert 'func is_auto_route' in runner_src, 'runner is_auto_route 缺失'
    ui_src = open('gotbotgame/scripts/mvp_ui_controller.gd', encoding='utf-8').read()
    assert 'func _on_auto_route_continue' in ui_src, 'UI auto_route 继续处理缺失'
    print('=== 需求1 结局自动收敛 静态校验通过 ===')

if __name__ == '__main__':
    main()
