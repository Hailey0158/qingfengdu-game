class_name QingfengduDialogueSystem
extends Node
## P0 验证：RichTextLabel 中文打字机和 200ms 立绘/占位节点淡入。

signal typing_finished

var _typing_tween: Tween

func type_text(target: RichTextLabel, text: String, seconds_per_char: float = 0.035) -> void:
	if is_instance_valid(_typing_tween):
		_typing_tween.kill()
	target.text = text
	target.visible_ratio = 0.0
	var duration: float = maxf(0.25, float(text.length()) * seconds_per_char)
	_typing_tween = create_tween()
	_typing_tween.tween_property(target, "visible_ratio", 1.0, duration)
	_typing_tween.tween_callback(func() -> void: typing_finished.emit())

func skip(target: RichTextLabel) -> void:
	if is_instance_valid(_typing_tween):
		_typing_tween.kill()
	target.visible_ratio = 1.0
	typing_finished.emit()

func fade_in(target: CanvasItem, duration: float = 0.2) -> void:
	target.modulate.a = 0.0
	var fade_tween: Tween = create_tween()
	fade_tween.tween_property(target, "modulate:a", 1.0, duration)
