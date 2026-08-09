# -*- coding: utf-8 -*-
"""GDScript 括号平衡粗检（忽略字符串与注释）"""
files = ['scripts/mvp_ui_controller.gd', 'scripts/mvp_scene_runner.gd',
         'scripts/status_bar.gd', 'scripts/choice_panel.gd']
ok = True
for f in files:
    src = open(f, encoding='utf-8').read()
    for ch, close_ch in [('(', ')'), ('[', ']')]:
        depth = 0
        in_str = None
        i = 0
        while i < len(src):
            c = src[i]
            if in_str is not None:
                if c == in_str and (i == 0 or src[i - 1] != '\\'):
                    in_str = None
                i += 1
                continue
            if c in ('"', "'"):
                in_str = c
            elif c == '#':
                while i < len(src) and src[i] != '\n':
                    i += 1
            elif c == ch:
                depth += 1
            elif c == close_ch:
                depth -= 1
            i += 1
        status = 'OK' if depth == 0 else 'UNBALANCED depth=%d' % depth
        if depth != 0:
            ok = False
        print('%s: %s%s %s' % (f, ch, close_ch, status))
print('OVERALL:', 'PASS' if ok else 'FAIL')
