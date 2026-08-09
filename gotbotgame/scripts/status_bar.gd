extends VBoxContainer
## P1 MVP 状态栏：按剧情节点显示 天/时段（第一、二章不显示时间标记）；
## 常驻显示 洞察/碎片/三角色好感 计数，并保留存档入口。

@onready var day_label: Label = %DayLabel
@onready var insight_label: Label = %InsightLabel
@onready var fragment_label: Label = %FragmentLabel
@onready var affection_label: Label = %AffectionLabel
@onready var save_hint: Label = %SaveHint

const SLOT_NAMES: Array[String] = ["上午", "下午", "夜"]

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func _save_manager() -> QingfengduSaveManager:
	return get_node_or_null("/root/SaveManager") as QingfengduSaveManager

func _ready() -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		push_error("未找到 AutoLoad: GameStateManager")
		return
	state.state_changed.connect(refresh)
	refresh()

func refresh() -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return
	_update_day_label(state)
	insight_label.text = "洞察  %d" % state.insight
	fragment_label.text = "碎片  %d" % state.fragments
	var liu: int = int(state.affection.get("liu", 0))
	var li: int = int(state.affection.get("li", 0))
	var gui: int = int(state.affection.get("gui", 0))
	affection_label.text = "柳 %d   黎 %d   归 %d" % [liu, li, gui]

## 第一章/第二章/章节卡/结局不显示"第 X 天 · 时段"；第三章日常起随剧情节点推进显示。
func _update_day_label(state: QingfengduGameStateManager) -> void:
	if _is_chapter_three_node(state.current_node_id):
		day_label.text = "第 %d 天 · %s" % [state.day, SLOT_NAMES[clampi(state.slot - 1, 0, 2)]]
		day_label.visible = true
	else:
		day_label.text = ""
		day_label.visible = false

func _is_chapter_three_node(node_id: String) -> bool:
	if node_id.begins_with("scene_daily_"):
		return true
	return node_id in ["scene_day1_close", "scene_day2_close", "scene_day3_close"]

func _on_save_pressed() -> void:
	var save_manager: QingfengduSaveManager = _save_manager()
	var ok: bool = save_manager != null and save_manager.save_slot(1)
	save_hint.text = "进度已记下" if ok else "暂无法保存"

func _on_load_pressed() -> void:
	var save_manager: QingfengduSaveManager = _save_manager()
	var ok: bool = save_manager != null and save_manager.load_slot(1)
	save_hint.text = "进度已恢复" if ok else "暂无可用进度"
