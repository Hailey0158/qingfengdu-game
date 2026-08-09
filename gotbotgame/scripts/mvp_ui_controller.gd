extends Control
## P1 MVP：主场景 UI 控制器，驱动柳陆书线场景文本和选项。

@onready var dialogue_box: PanelContainer = $DialogueBox
@onready var speaker_name: Label = $DialogueBox/Margin/Content/SpeakerName
@onready var dialogue_text: RichTextLabel = $DialogueBox/Margin/Content/DialogueText
@onready var choice_panel: VBoxContainer = $ChoicePanel
@onready var runner: QingfengduMvpSceneRunner = $MvpSceneRunner
@onready var background_layer: TextureRect = %BackgroundLayer
@onready var liu_portrait: TextureRect = %LiuPortrait
@onready var li_portrait: TextureRect = $CharacterLayer/LiPortrait
@onready var gui_portrait: TextureRect = $CharacterLayer/GuiPortrait
@onready var innkeeper_portrait: TextureRect = $CharacterLayer/InnkeeperPortrait

const FINAL_DIALOGUE_PATH: String = "res://data/final-dialogue/mvp/liu_lushu_day1.json"
## 选项分支回应的"继续"占位选项 ID：选择后先展示分支内容，点击继续再进入目标节点。
const RESPONSE_CONTINUE_ID: String = "_continue_response"
const BACKGROUND_TEXTURES: Dictionary = {
	"ch1_title": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_001a_rain_lantern": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_001b_innkeeper": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_001c_choices": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_002_path": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"ending_front_no_road": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_003_pay_all": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"ch2_title": "res://assets/placeholder_sprites/bg_three_characters_scene.png",
	"scene_010_meet": "res://assets/placeholder_sprites/bg_three_characters_scene.png",
	"scene_020_liu_day1": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_030_li_day1": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_040_gui_day1": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day1_01": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day1_02": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day1_03": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"ch3_title": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_liu_tea": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_li_clues": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_gui_sit": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_gui_sit_first": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_explore": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_innkeeper": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_return": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day2_01": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day2_02": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day2_03": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day3_01": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day3_02": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_daily_day3_03": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_day1_close": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_day2_close": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_day3_close": "res://assets/placeholder_sprites/bg_inn_hall_clean.png",
	"scene_021_liu_day1_close": "res://assets/placeholder_sprites/bg_inn_hall_clean.png"
}
const BACKGROUND_COLORS: Dictionary = {
	"ch1_title": Color("0d1b25"),
	"scene_001a_rain_lantern": Color("122a33"),
	"scene_001b_innkeeper": Color("1a2a30"),
	"scene_001c_choices": Color("122a33"),
	"scene_002_path": Color("10212c"),
	"ending_front_no_road": Color("0d1b25"),
	"scene_003_pay_all": Color("30413b"),
	"ch2_title": Color("2b3b37"),
	"scene_010_meet": Color("2b3b37"),
	"scene_020_liu_day1": Color("284342"),
	"scene_030_li_day1": Color("2b3b37"),
	"scene_040_gui_day1": Color("2b3b37"),
	"ch3_title": Color("2b3b37"),
	"scene_daily_day1_01": Color("2b3b37"),
	"scene_daily_day1_02": Color("2b3b37"),
	"scene_daily_day1_03": Color("1f3436"),
	"scene_daily_liu_tea": Color("284342"),
	"scene_daily_li_clues": Color("2b3b37"),
	"scene_daily_gui_sit": Color("2b3b37"),
	"scene_daily_gui_sit_first": Color("2b3b37"),
	"scene_daily_explore": Color("1a2a30"),
	"scene_daily_innkeeper": Color("2b3b37"),
	"scene_daily_return": Color("2b3b37"),
	"scene_daily_day2_01": Color("2b3b37"),
	"scene_daily_day2_02": Color("2b3b37"),
	"scene_daily_day2_03": Color("1f3436"),
	"scene_daily_day3_01": Color("2b3b37"),
	"scene_daily_day3_02": Color("2b3b37"),
	"scene_daily_day3_03": Color("1f3436"),
	"scene_day1_close": Color("1f3436"),
	"scene_day2_close": Color("1f3436"),
	"scene_day3_close": Color("1f3436"),
	"scene_021_liu_day1_close": Color("1f3436")
}

var final_dialogue: Dictionary = {}
## 展示选项分支回应时暂存的目标节点，点击"继续"后进入。
var _pending_target: String = ""

func _ready() -> void:
	choice_panel.use_mvp_runner = true
	runner.load_branch_tree()
	_load_final_dialogue()
	_render_current_scene()

func _render_current_scene() -> void:
	var scene_data: Dictionary = runner.get_scene_data()
	var node_id: String = str(scene_data.get("node_id", runner.current_scene_id))
	var dialogue_data: Dictionary = _dialogue_for(node_id)
	speaker_name.text = str(dialogue_data.get("speaker", scene_data.get("speaker", "旁白")))
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system != null:
		dialogue_system.type_text(dialogue_text, str(dialogue_data.get("text", scene_data.get("text", ""))))
	_apply_visuals(node_id)
	var choices: Array[Dictionary] = runner.get_choices()
	choice_panel.render_choices(choices)
	choice_panel.visible = not runner.is_terminal()
	for child: Node in choice_panel.get_children():
		if child is Button:
			var button: Button = child as Button
			var callable: Callable = _on_choice_pressed.bind(str(button.get_meta("choice_id", "")))
			if not button.pressed.is_connected(callable):
				button.pressed.connect(callable)

func _on_choice_pressed(choice_id: String) -> void:
	var audio_manager: QingfengduAudioManager = _audio_manager()
	if audio_manager != null:
		audio_manager.start_prototype_mix()
	if choice_id == RESPONSE_CONTINUE_ID:
		_continue_from_response()
		return
	var response_id: String = _response_node_for(choice_id)
	if runner.choose(choice_id):
		if not response_id.is_empty() and _show_choice_response(response_id):
			return
		_render_current_scene()

## 点击分支回应的"继续"：进入被暂存的目标节点并正常渲染。
func _continue_from_response() -> void:
	if _pending_target.is_empty():
		return
	var target: String = _pending_target
	_pending_target = ""
	runner.show_scene(target)
	_render_current_scene()

func _load_final_dialogue() -> void:
	var file: FileAccess = FileAccess.open(FINAL_DIALOGUE_PATH, FileAccess.READ)
	if file == null:
		push_error("无法读取 MVP 最终文案: %s" % FINAL_DIALOGUE_PATH)
		return
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		final_dialogue = parsed
	else:
		push_error("MVP 最终文案 JSON 格式错误")

func _dialogue_for(node_id: String) -> Dictionary:
	var nodes: Variant = final_dialogue.get("nodes", {})
	if nodes is Dictionary:
		var entry: Variant = nodes.get(node_id, {})
		if entry is Dictionary:
			return entry
	return {}

func _response_node_for(choice_id: String) -> String:
	## 每个选项对应的对白分支节点（节点文本定义于 final-dialogue JSON）。
	## 选完后在旁白处展示对应分支内容（标题=说话人，正文=分支文案），再"继续"进入目标节点。
	var mapping: Dictionary = {
		# 第二章 · 柳陆书初识
		"liu_a1_joke": "scene_020_liu_response_a1",
		"liu_a2_challenge": "scene_020_liu_response_a2",
		"liu_a3_ask_secret": "scene_020_liu_response_a3",
		"liu_a4_silence": "scene_020_liu_response_a4",
		# 第二章 · 黎客颍初识
		"li_b1_name": "scene_030_li_response_b1",
		"li_b2_weapon": "scene_030_li_response_b2",
		"li_b3_ask": "scene_030_li_response_b3",
		"li_b4_silence": "scene_030_li_response_b4",
		# 第二章 · 归汉初识
		"gui_c1_found": "scene_040_gui_response_c1",
		"gui_c2_sword": "scene_040_gui_response_c2",
		"gui_c3_scenery": "scene_040_gui_response_c3",
		"gui_c4_sit": "scene_040_gui_response_c4",
		# 第三章 · 柳陆书喝茶
		"liu_tea_a": "scene_daily_liu_tea_a",
		"liu_tea_b": "scene_daily_liu_tea_b",
		"liu_tea_c": "scene_daily_liu_tea_c",
		"liu_tea_d": "scene_daily_liu_tea_d",
		"liu_tea_e": "scene_daily_liu_tea_e",
		# 第三章 · 黎客颍线索
		"li_clue_a": "scene_daily_li_clue_a",
		"li_clue_b": "scene_daily_li_clue_b",
		"li_clue_c": "scene_daily_li_clue_c",
		"li_clue_d": "scene_daily_li_clue_d",
		# 第三章 · 归汉对坐
		"gui_sit_a": "scene_daily_gui_sit_a",
		"gui_sit_b": "scene_daily_gui_sit_b",
		"gui_sit_c": "scene_daily_gui_sit_c",
		"gui_sit_d": "scene_daily_gui_sit_d",
		# 第三章 · 独自闲逛
		"explore_backyard": "scene_daily_explore_backyard",
		"explore_hall": "scene_daily_explore_hall",
		"explore_upstairs": "scene_daily_explore_upstairs",
		# 第三章 · 与伙计搭话
		"inn_a": "scene_daily_innkeeper_a",
		"inn_b": "scene_daily_innkeeper_b",
		"inn_c": "scene_daily_innkeeper_c",
		"inn_d": "scene_daily_innkeeper_d"
	}
	return str(mapping.get(choice_id, ""))

func _show_choice_response(response_id: String) -> bool:
	var response: Dictionary = _dialogue_for(response_id)
	if response.is_empty():
		return false
	speaker_name.text = str(response.get("speaker", "旁白"))
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system != null:
		dialogue_system.type_text(dialogue_text, str(response.get("text", "")))
	# 暂存目标节点，仅渲染一个"继续"选项，点击后进入目标节点。
	# 注意：render_choices 参数为强类型 Array[Dictionary]，须用同类型变量传入，
	# 直接传无类型数组字面量会触发 GDScript 强类型校验错误。
	_pending_target = runner.current_scene_id
	var continue_choices: Array[Dictionary] = [
		{"choice_id": RESPONSE_CONTINUE_ID, "text": "继续"}
	]
	choice_panel.render_choices(continue_choices)
	choice_panel.visible = true
	# 只连接本次新增的"继续"按钮，避免误连 queue_free 延迟删除的旧按钮。
	for child: Node in choice_panel.get_children():
		if child is Button and str(child.get_meta("choice_id", "")) == RESPONSE_CONTINUE_ID:
			var button: Button = child as Button
			var callable: Callable = _on_choice_pressed.bind(RESPONSE_CONTINUE_ID)
			if not button.pressed.is_connected(callable):
				button.pressed.connect(callable)
	return true

func _apply_visuals(node_id: String) -> void:
	var background_path: String = str(BACKGROUND_TEXTURES.get(node_id, BACKGROUND_TEXTURES["scene_001a_rain_lantern"]))
	var background_texture: Texture2D = load(background_path) as Texture2D
	if background_texture != null:
		background_layer.texture = background_texture
	else:
		push_warning("占位背景加载失败，回退为纯色: %s" % background_path)
		background_layer.texture = null
		background_layer.modulate = BACKGROUND_COLORS.get(node_id, BACKGROUND_COLORS["scene_001a_rain_lantern"]) as Color
	# 角色可见性：三线初识各显其角，日常场景显对应角色，首日收束全隐。
	var show_innkeeper: bool = node_id == "scene_001b_innkeeper" or node_id == "scene_daily_innkeeper"
	var show_liu: bool = node_id in ["scene_020_liu_day1", "scene_021_liu_day1_close", "scene_daily_liu_tea"]
	var show_li: bool = node_id in ["scene_030_li_day1", "scene_daily_li_clues"]
	var show_gui: bool = node_id in ["scene_040_gui_day1", "scene_daily_gui_sit", "scene_daily_gui_sit_first"]
	innkeeper_portrait.visible = show_innkeeper
	liu_portrait.visible = show_liu
	li_portrait.visible = show_li
	gui_portrait.visible = show_gui
	innkeeper_portrait.modulate.a = 1.0 if show_innkeeper else 0.0
	liu_portrait.modulate.a = 1.0 if show_liu else 0.0
	li_portrait.modulate.a = 1.0 if show_li else 0.0
	gui_portrait.modulate.a = 1.0 if show_gui else 0.0

func _dialogue_system() -> QingfengduDialogueSystem:
	return get_node_or_null("/root/DialogueSystem") as QingfengduDialogueSystem

func _audio_manager() -> QingfengduAudioManager:
	return get_node_or_null("/root/AudioManager") as QingfengduAudioManager
