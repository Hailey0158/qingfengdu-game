extends Node
## P0 验证：RichTextLabel 中文打字机和 200ms 立绘/占位节点淡入。

signal typing_finished

var _tween: Tween

func type_text(target: RichTextLabel, text: String, seconds_per_char := 0.035) -> void:
    if is_instance_valid(_tween):
        _tween.kill()
    target.text = text
    target.visible_ratio = 0.0
    var duration := maxf(0.25, float(text.length()) * seconds_per_char)
    _tween = create_tween()
    _tween.tween_property(target, "visible_ratio", 1.0, duration)
    _tween.tween_callback(func() -> void: typing_finished.emit())

func skip(target: RichTextLabel) -> void:
    if is_instance_valid(_tween):
        _tween.kill()
    target.visible_ratio = 1.0
    typing_finished.emit()

func fade_in(target: CanvasItem, duration := 0.2) -> void:
    target.modulate.a = 0.0
    var tween := create_tween()
    tween.tween_property(target, "modulate:a", 1.0, duration)
