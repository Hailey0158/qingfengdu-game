extends ColorRect
## P0 验证：黑屏 1.5 秒过渡，符合 PRD/PDD 的阅读场景切换方向。

func play_transition(hold_seconds: float = 0.4) -> void:
	visible = true
	modulate.a = 0.0
	var transition_tween: Tween = create_tween()
	transition_tween.tween_property(self, "modulate:a", 1.0, 0.5)
	transition_tween.tween_interval(hold_seconds)
	transition_tween.tween_property(self, "modulate:a", 0.0, 0.5)
	transition_tween.tween_callback(func() -> void: visible = false)
