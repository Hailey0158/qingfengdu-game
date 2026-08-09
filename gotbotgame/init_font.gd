extends Node

const CHINESE_FONT_PATH: String = "res://fonts/NotoSansCJKsc-Regular.otf"

var chinese_font: Font

func _ready() -> void:
	chinese_font = load(CHINESE_FONT_PATH) as Font
	if chinese_font == null:
		push_error("中文字体加载失败：%s" % CHINESE_FONT_PATH)
		return
	_apply_font_overrides(get_tree().root)
	get_tree().node_added.connect(_on_node_added)
	print("中文字体加载成功：NotoSansCJKsc-Regular.otf（包含动态控件）")

func _on_node_added(node: Node) -> void:
	if chinese_font == null:
		return
	_apply_font_overrides(node)

func _apply_font_overrides(node: Node) -> void:
	if node is Control:
		var control := node as Control
		control.add_theme_font_override("font", chinese_font)
		control.add_theme_font_override("normal_font", chinese_font)
		control.add_theme_font_override("bold_font", chinese_font)
	for child: Node in node.get_children():
		_apply_font_overrides(child)
