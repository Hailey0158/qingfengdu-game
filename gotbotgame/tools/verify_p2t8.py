# -*- coding: utf-8 -*-
"""P2-T8 校验：fire_night.scene.md 字段完整 + PDD 走水夜细节对齐 + 结局衔接"""
import json

src = open('scenes/fire_night.scene.md', encoding='utf-8').read()
assert src.startswith('scene_id: fire_night')
for field in ['location:', 'characters:', 'mood_tag:', 'plot_tags:', 'save_point:',
              'trigger:', 'narration:', 'dialogue:', 'choices:', 'narration_after:',
              'ending_gate:', 'branch_notes:', 'audio:']:
    assert field in src, '缺少字段 ' + field
print('OK: fire_night.scene.md 字段完整 (%d 行)' % len(src.splitlines()))

# PDD 走水夜细节关键词对齐
details = ['第一个冲进去', '被烟呛得说不出话', '扇骨燎黑了', '扇骨燎黑', '湿毛巾', '刀背',
           '剑尖点地', '拆剑穗', '丝线', '补扇', 'fire_night_warned', '灯油痕迹']
for kw in details:
    assert kw in src, '缺少 PDD 细节: ' + kw
print('OK: PDD 走水夜细节全部覆盖')

# 选项与数值体系对齐
ef = json.load(open('data/endings-full.json', encoding='utf-8'))
assert '替人挡了刀' in ef['endings'], '缺少死亡结局文案'
assert '得闲饮茶' in ef['endings'], '缺少隐藏结局文案'
print('OK: 死亡结局【替人挡了刀】/隐藏结局【得闲饮茶】文案存在')

for cid in ['fire_help_liu_upstairs', 'fire_help_li_below', 'fire_warn_alerted', 'fire_find_innkeeper']:
    assert ('id: %s' % cid) in src, '缺少选项 ' + cid
print('OK: 4 个玩家参与选项齐全')

nd = json.load(open('data/numerical-design.json', encoding='utf-8'))
assert 'fire_night_warned' in nd['flags'], 'fire_night_warned 未定义'
print('OK: fire_night_warned flag 已在数值设计定义')
print('P2-T8 校验全部通过')
