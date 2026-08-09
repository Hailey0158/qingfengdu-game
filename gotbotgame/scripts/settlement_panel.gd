extends Control
## P2 结算面板：三日结算时展示 洞察/线索碎片/三角色好感 与关键发现（flag 差分）。
## 由 mvp_ui_controller 在 scene_day3_summary 节点显示并连接 continue_pressed。

signal continue_pressed

@onready var stats_label: Label = %StatsLabel
@onready var affection_label: Label = %AffectionLabel
@onready var findings_label: Label = %FindingsLabel
@onready var continue_button: Button = %ContinueButton

## flag → 关键发现文案（与 P2_SETTLEMENT_ENDING_DESIGN.md 一致）
const FINDING_TEXTS: Dictionary = {
	"recognized_scar": "你一直记得伙计右手虎口那道旧疤——那不是干粗活留下的。",
	"hidden_line_unlocked": "你总想起靠门第三张桌那壶没人喝的茶，茶还是温的。",
	"watched": "你隐约觉得，有双眼睛一直在暗处看着你。",
	"fire_night_warned": "你想起那夜闻到的灯油味——那味道不对。",
	"bait_marked": "你记下了伙计说的那棵歪脖子老槐树。"
}

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func _ready() -> void:
	refresh()

func refresh() -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return
	stats_label.text = "洞察  %d    线索·碎片  %d" % [state.insight, state.fragments]
	var liu: int = int(state.affection.get("liu", 0))
	var li: int = int(state.affection.get("li", 0))
	var gui: int = int(state.affection.get("gui", 0))
	affection_label.text = "柳陆书  %d    黎客颍  %d    归汉  %d" % [liu, li, gui]
	var lines: Array[String] = []
	for flag: String in FINDING_TEXTS:
		if bool(state.flags.get(flag, false)):
			lines.append("· " + str(FINDING_TEXTS[flag]))
	if lines.is_empty():
		findings_label.text = "这一夜，你什么特别的事都没记下。"
	else:
		findings_label.text = "\n".join(lines)

func _on_continue_pressed() -> void:
	continue_pressed.emit()
