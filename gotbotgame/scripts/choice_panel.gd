extends VBoxContainer
## P1 MVP 选项面板：动态生成叙事选择，并提供可见的悬停与选中反馈。

const CHINESE_FONT_PATH: String = "res://fonts/NotoSansCJKsc-Regular.otf"
const CHOICE_PREFIX: String = ">"

@export var use_mvp_runner: bool = false

var chinese_font: Font

func _branch_engine() -> QingfengduBranchEngine:
	return get_node_or_null("/root/BranchEngine") as QingfengduBranchEngine

func _ready() -> void:
	chinese_font = load(CHINESE_FONT_PATH) as Font
	if chinese_font == null:
		push_error("选项中文字体加载失败：%s" % CHINESE_FONT_PATH)
	if use_mvp_runner:
		return
	var branch_engine: QingfengduBranchEngine = _branch_engine()
	if branch_engine == null:
		push_error("未找到 AutoLoad: BranchEngine")
		return
	branch_engine.load_tree()
	render_choices(branch_engine.get_available_choices("prototype"))

func render_choices(choices: Array[Dictionary]) -> void:
	for child: Node in get_children():
		child.queue_free()
	for index: int in choices.size():
		var choice: Dictionary = choices[index]
		var button: Button = Button.new()
		button.text = "%s  %s" % [CHOICE_PREFIX, str(choice.get("text", "未命名选项"))]
		if chinese_font != null:
			button.add_theme_font_override("font", chinese_font)
		button.set_meta("choice_id", str(choice.get("choice_id", choice.get("id", ""))))
		button.custom_minimum_size = Vector2(0, 40)
		button.alignment = HORIZONTAL_ALIGNMENT_LEFT
		button.focus_mode = Control.FOCUS_ALL
		button.add_theme_font_size_override("font_size", 20)
		button.add_theme_color_override("font_color", Color("#5F5E5A"))
		button.add_theme_color_override("font_hover_color", Color("#A32D2D"))
		button.add_theme_color_override("font_pressed_color", Color("#A32D2D"))
		button.add_theme_stylebox_override("normal", _button_style(Color(0.957, 0.949, 0.922, 0.78), Color(0.45, 0.45, 0.40, 0.35)))
		button.add_theme_stylebox_override("hover", _button_style(Color(0.99, 0.96, 0.90, 0.96), Color(0.64, 0.18, 0.16, 0.72)))
		button.add_theme_stylebox_override("pressed", _button_style(Color(0.90, 0.87, 0.80, 0.96), Color(0.64, 0.18, 0.16, 0.9)))
		if not use_mvp_runner:
			button.pressed.connect(_select.bind(choice))
		add_child(button)

func _button_style(background: Color, border: Color) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = background
	style.border_color = border
	style.set_border_width_all(1)
	style.corner_radius_top_left = 8
	style.corner_radius_top_right = 8
	style.corner_radius_bottom_left = 8
	style.corner_radius_bottom_right = 8
	style.content_margin_left = 16.0
	style.content_margin_right = 16.0
	return style

func _select(choice: Dictionary) -> void:
	var branch_engine: QingfengduBranchEngine = _branch_engine()
	if branch_engine == null:
		push_error("未找到 AutoLoad: BranchEngine")
		return
	var effects: Variant = choice.get("effects", {})
	branch_engine.apply_effects(effects if effects is Dictionary else {})
	render_choices(branch_engine.get_available_choices("prototype"))
