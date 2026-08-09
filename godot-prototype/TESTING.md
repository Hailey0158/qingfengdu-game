# 清风渡 P0-T2 · Godot 4 技术原型测试流程

## 前置条件

1. 使用 Godot 4.3 或兼容的 Godot 4.x 版本导入 `godot-prototype/project.godot`。
2. 向 `fonts/` 加入可再分发中文字体，并为项目 UI 主题或节点设置该字体。
3. 为音频淡入测试准备一段短 `.ogg` 文件；将其在运行时通过调试器调用 `AudioManager.play_bgm_fade_in(preload("res://assets/audio/bgm/prototype.ogg"))`，或临时加一个验证按钮调用该方法。
4. 本阶段不得加入正式剧情文本、角色立绘或成品 BGM。

## A. 中文打字机与跳过

1. 运行主场景 `scenes/main.tscn`。
2. 确认底部对话框显示中文“清风渡 · Godot 4 技术原型……”且没有方块字、问号或乱码。
3. 观察文字逐步显示；目标是 `RichTextLabel.visible_ratio` 驱动而非逐字符 append。
4. 对话框内点击鼠标，确认文字立即补全。
5. 判定：中文可读、无截断、点击跳过有效即通过。

## B. JSON 存档读写

1. 点击“验证选项：洞察 +1”，确认状态栏洞察变为 1，并出现洞察门槛选项。
2. 点击“验证存档”；确认提示“存档成功”。
3. 再次点击洞察 +1，使数值变化。
4. 点击“验证读档”；确认洞察恢复为保存时的数值，门槛选项显示状态同步恢复。
5. 桌面版检查 `user://saves/prototype_slot_00.json` 是否存在。不得把绝对桌面路径写入代码。
6. 判定：JSON 形成、读档恢复完整、失败时有提示即通过。

## C. AudioBus 三轨与 BGM 淡入

1. 打开 Project → Project Settings → Audio，确认默认总线布局为 `default_bus_layout.tres`。
2. 在 Audio 面板确认 `Master` 下存在 `BGM`、`SFX`、`Ambient` 三条总线，均发送至 Master。
3. 通过调试调用 `AudioManager.play_bgm_fade_in()` 播放短 OGG。
4. 观察 BGM 总线在约 1 秒内从 -40 dB 平滑到 -6 dB；确认 SFX、Ambient 的静音开关不影响 BGM。
5. 判定：三总线独立、BGM 无爆音或中断、淡入曲线连续即通过。

## D. 立绘占位淡入与黑屏转场

1. 在 Remote 场景树选中 `PrototypePortrait`，从调试器调用 `DialogueSystem.fade_in($CanvasLayer/PrototypePortrait)`。
2. 观察占位节点在 200ms 内从透明到完全显示；确认没有闪白、跳帧或错误。
3. 调用 `$CanvasLayer/Transition.play_transition()`；确认黑屏淡入 → 短暂停留 → 淡出，总时长约 1.4 秒。
4. 判定：200ms 立绘淡入与 1.5 秒以内黑屏过渡可稳定复现即通过。

## E. Web 导出专项检查

1. 安装与 Godot 版本一致的 Web export templates，导出 Web，关闭 Threads，开启 Size optimization。
2. 使用本地 HTTP 服务器而非直接双击 HTML 打开导出结果。
3. Chrome 与微信内置浏览器各测一次：中文字体、点击、打字机、存/读档、AudioBus 与首次音频播放。
4. 注意浏览器通常要求用户手势后才能播放音频；在用户点击“开始/继续”后再调用 BGM 播放。
5. 判定：首屏目标 ≤5 秒、场景/黑屏转场 ≤1 秒（不含刻意停留）、存档跨刷新行为符合目标浏览器策略。
