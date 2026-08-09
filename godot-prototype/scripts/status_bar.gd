extends HBoxContainer
## P0 验证：状态信号驱动的中文 UI 刷新与存档按钮。

@onready var day_label: Label = %DayLabel
@onready var insight_label: Label = %InsightLabel
@onready var save_hint: Label = %SaveHint

func _ready() -> void:
    GameStateManager.state_changed.connect(refresh)
    refresh()

func refresh() -> void:
    day_label.text = "第 %d 天 · 时段 %d" % [GameStateManager.day, GameStateManager.slot]
    insight_label.text = "洞察：%d" % GameStateManager.insight

func _on_save_pressed() -> void:
    var ok := SaveManager.save_slot(0)
    save_hint.text = "存档成功" if ok else "存档失败"

func _on_load_pressed() -> void:
    var ok := SaveManager.load_slot(0)
    save_hint.text = "读档成功" if ok else "无可用存档"
