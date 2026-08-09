# -*- coding: utf-8 -*-
"""P2-T6 校验：场景脚本与 numerical-design / endings-full / PDD 对齐"""
import json, os, re

nd = json.load(open('data/numerical-design.json', encoding='utf-8'))
ef = json.load(open('data/endings-full.json', encoding='utf-8'))

print('== 1. flags 对齐（场景脚本引用的标志须在 numerical-design 中定义）==')
needed_flags = ['watched', 'innkeeper_alert', 'exposed', 'recognized_scar',
                'bait_marked', 'hidden_line_unlocked', 'observed_account_book',
                'fire_night_warned', 'solo_night_explore', 'sacrifice_choice']
defined = set(nd['flags'].keys())
missing = [f for f in needed_flags if f not in defined]
print('缺失 flag:', missing or '无')
assert not missing

print('== 2. 结局条件对齐 ==')
ec = nd['ending_conditions']
for name, conds in [('得闲饮茶', None), ('淹死在自己的好奇心里', None), ('信错了人', None)]:
    assert name in ec, '缺少结局条件: ' + name
    print('  [%s] 条件: %s' % (name, ec[name].get('conditions', ec[name])))

print('== 3. 结局文案存在（endings-full.json）==')
for name in ['得闲饮茶', '淹死在自己的好奇心里', '信错了人', '替人挡了刀']:
    assert name in ef['endings'], '缺少结局文案: ' + name
    assert ef['endings'][name].get('narration'), '结局文案为空: ' + name
    print('  [%s] 文案 OK (%d 字)' % (name, len(ef['endings'][name]['narration'])))

print('== 4. 场景脚本格式与关键字段 ==')
for f, expect_id in [
    ('scenes/innkeeper_secret.scene.md', 'innkeeper_secret'),
    ('scenes/innkeeper_third_explore.scene.md', 'innkeeper_third_explore'),
    ('scenes/tea_ending.scene.md', 'tea_ending'),
]:
    src = open(f, encoding='utf-8').read()
    assert src.startswith('scene_id: %s' % expect_id), f + ' scene_id 不匹配'
    for field in ['location:', 'characters:', 'mood_tag:', 'plot_tags:',
                  'narration:', 'choices:', 'audio:', 'branch_notes:']:
        assert field in src, f + ' 缺少字段 ' + field
    print('  %s OK (%d 行, scene_id=%s)' % (f, len(src.splitlines()), expect_id))

print('== 5. 已写文案零改动抽查（得闲饮茶结尾）==')
tea = ef['endings']['得闲饮茶']['narration']
tea_md = open('scenes/tea_ending.scene.md', encoding='utf-8').read()
assert '两息够一个活人喝完一盏茶吗' in tea and '两息够一个活人喝完一盏茶吗' in tea_md
print('  得闲饮茶关键句在结局数据与场景脚本中均存在')

print('P2-T6 校验全部通过')
