extends Control
## P3 结局结算面板：达成结局后展示专属结算页面。
## 按 ending_id（分支树 terminal 节点 ID）读取 endings-full.json 的 ending_page 配置，
## 渲染差异化背景色/题记/数值回顾/结局叙事/再玩一次按钮。

signal replay_pressed

const ENDINGS_PATH: String = "res://data/endings-full.json"
const CHINESE_FONT_PATH: String = "res://fonts/NotoSansCJKsc-Regular.otf"

var endings_data: Dictionary = {}
var node_to_ending: Dictionary = {}
var chinese_font: Font

@onready var bg_panel: PanelContainer = %BgPanel
@onready var title_label: Label = %TitleLabel
@onready var type_label: Label = %TypeLabel
@onready var epigraph_label: Label = %EpigraphLabel
@onready var stats_label: Label = %StatsLabel
@onready var affection_label: Label = %AffectionLabel
@onready var path_label: Label = %PathLabel
@onready var progress_label: Label = %ProgressLabel
@onready var narration_label: RichTextLabel = %NarrationLabel
@onready var replay_button: Button = %ReplayButton

func _ready() -> void:
	chinese_font = load(CHINESE_FONT_PATH) as Font
	_load_endings()
	replay_button.pressed.connect(_on_replay_pressed)
	visible = false

func _load_endings() -> void:
	var file: FileAccess = FileAccess.open(ENDINGS_PATH, FileAccess.READ)
	if file == null:
		push_error("无法读取结局数据: %s" % ENDINGS_PATH)
		return
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		endings_data = parsed
		node_to_ending = parsed.get("node_to_ending", {})
	else:
		push_error("endings-full.json 格式错误")

## 由 mvp_ui_controller 在 terminal ending 节点调用。
func refresh(ending_node_id: String) -> void:
	var ending_key: String = str(node_to_ending.get(ending_node_id, ""))
	if ending_key.is_empty():
		push_warning("结局节点未映射: %s" % ending_node_id)
		visible = false
		return
	var entry: Dictionary = endings_data.get("endings", {}).get(ending_key, {})
	if entry.is_empty():
		push_warning("结局数据缺失: %s" % ending_key)
		visible = false
		return
	var page: Dictionary = entry.get("ending_page", {})
	# ① 标题 + 类型标签
	title_label.text = str(entry.get("name", ending_key))
	type_label.text = str(page.get("label", ""))
	# ② 题记
	epigraph_label.text = "“%s”" % str(page.get("epigraph", ""))
	# ③ 数值回顾
	var state: QingfengduGameStateManager = _state_manager()
	if state != null:
		var liu: int = int(state.affection.get("liu", 0))
		var li: int = int(state.affection.get("li", 0))
		var gui: int = int(state.affection.get("gui", 0))
		stats_label.text = "洞察  %d    碎片  %d" % [state.insight, state.fragments]
		affection_label.text = "柳陆书  %d    黎客颍  %d    归汉  %d" % [liu, li, gui]
		# 路径摘要
		var path_taken: Array = state.path_taken
		var key_flags: Array = []
		for flag_key in ["recognized_scar","hidden_line_unlocked","route_solo","fire_night_warned","exposed"]:
			if bool(state.flags.get(flag_key, false)):
				key_flags.append(flag_key)
		path_label.text = "关键抉择：" + (", ".join(key_flags) if not key_flags.is_empty() else "无")
		# 解锁进度
		if not ending_key in state.ending_unlocked:
			state.ending_unlocked.append(ending_key)
		progress_label.text = "结局达成  %d / 20" % state.ending_unlocked.size()
	# ④ 结局叙事
	narration_label.text = str(entry.get("narration", ""))
	# 差异化背景色
	var bg_color_str: String = str(page.get("bg_color", "#1a1a1a"))
	var accent_str: String = str(page.get("accent", "#888780"))
	_apply_theme(bg_color_str, accent_str)
	# 中文字体
	if chinese_font != null:
		for child in _collect_labels():
			child.add_theme_font_override("font", chinese_font)
	visible = true

## 应用差异化背景色与 accent 装饰条。
func _apply_theme(bg_hex: String, accent_hex: String) -> void:
	var bg: Color = Color.from_string(bg_hex, Color(0.1, 0.1, 0.1, 0.97))
	var accent: Color = Color.from_string(accent_hex, Color(0.5, 0.5, 0.5))
	var style: StyleBoxFlat = bg_panel.get_theme_stylebox("panel").duplicate() as StyleBoxFlat
	if style == null:
		style = StyleBoxFlat.new()
	style.bg_color = bg
	style.border_color = accent
	style.border_width_left = 3
	style.border_width_top = 3
	style.border_width_right = 3
	style.border_width_bottom = 3
	bg_panel.add_theme_stylebox_override("panel", style)
	# 标题色用 accent 亮化
	title_label.add_theme_color_override("font_color", accent.lightened(0.4))
	type_label.add_theme_color_override("font_color", accent)
	epigraph_label.add_theme_color_override("font_color", accent.lightened(0.2))
	var text_col: Color = accent.lightened(0.6)
	stats_label.add_theme_color_override("font_color", text_col)
	affection_label.add_theme_color_override("font_color", text_col)
	path_label.add_theme_color_override("font_color", text_col.darkened(0.2))
	progress_label.add_theme_color_override("font_color", accent)
	narration_label.add_theme_color_override("default_color", Color(0.92, 0.90, 0.85))
	replay_button.add_theme_color_override("font_color", accent.lightened(0.3))
	replay_button.add_theme_color_override("font_hover_color", accent.lightened(0.5))

func _collect_labels() -> Array:
	return [title_label, type_label, epigraph_label, stats_label, affection_label, path_label, progress_label]

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func _on_replay_pressed() -> void:
	replay_pressed.emit()
