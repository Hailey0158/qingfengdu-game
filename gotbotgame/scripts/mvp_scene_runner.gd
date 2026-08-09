class_name QingfengduMvpSceneRunner
extends Node
## P1 MVP：从 branch-tree-mvp.json 驱动柳陆书线三段场景。

const BRANCH_TREE_PATH: String = "res://data/branch-tree-mvp.json"

var branch_tree: Dictionary = {}
var current_scene_id: String = "ch1_title"

func _ready() -> void:
	if not load_branch_tree():
		return
	show_scene(current_scene_id)

func load_branch_tree(path: String = BRANCH_TREE_PATH) -> bool:
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("无法读取 MVP 分支树: %s" % path)
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not (parsed is Dictionary):
		push_error("MVP 分支树 JSON 格式错误: %s" % path)
		return false
	var raw_nodes: Variant = parsed.get("nodes", {})
	if not (raw_nodes is Dictionary):
		push_error("MVP 分支树缺少 nodes 字典")
		return false
	branch_tree = parsed
	return true

func show_scene(scene_id: String) -> void:
	if not _has_node(scene_id):
		push_error("MVP 场景节点不存在: %s" % scene_id)
		return
	current_scene_id = scene_id
	var state: QingfengduGameStateManager = _state_manager()
	if state != null:
		_sync_day_slot_from_node(scene_id)
		state.set_current_node(scene_id, scene_id)
		_apply_effects(get_scene_data(scene_id).get("on_enter_effects", {}))
		state.state_changed.emit()
		var save_manager: QingfengduSaveManager = get_node_or_null("/root/SaveManager") as QingfengduSaveManager
		if save_manager != null:
			save_manager.save_auto()

## 依据当前节点 ID 同步 天/时段 状态，供左上角时间推进与存档快照使用。
func _sync_day_slot_from_node(scene_id: String) -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return
	if scene_id.begins_with("scene_daily_day"):
		# 形如 scene_daily_day1_01 → day=1 slot=1
		var parts: PackedStringArray = scene_id.split("_")
		if parts.size() >= 4:
			state.day = int(parts[2].trim_prefix("day"))
			state.slot = clampi(int(parts[3]), 1, 3)
			state.current_slot = ["morning", "afternoon", "night"][state.slot - 1]
	elif scene_id.ends_with("_close"):
		# 形如 scene_day1_close → 该日夜间收束
		var parts: PackedStringArray = scene_id.split("_")
		if parts.size() >= 2:
			state.day = int(parts[1].trim_prefix("day"))
			state.slot = 3
			state.current_slot = "night"

func get_scene_data(scene_id: String = current_scene_id) -> Dictionary:
	var raw_nodes: Variant = branch_tree.get("nodes", {})
	if not (raw_nodes is Dictionary):
		return {}
	var raw_scene: Variant = raw_nodes.get(scene_id, {})
	return raw_scene if raw_scene is Dictionary else {}

func get_choices(scene_id: String = current_scene_id) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	var raw_choices: Variant = get_scene_data(scene_id).get("choices", [])
	if not (raw_choices is Array):
		return result
	for raw_choice: Variant in raw_choices:
		if raw_choice is Dictionary and _conditions_met(raw_choice.get("conditions", {})):
			result.append(raw_choice)
	return result

func choose(choice_id: String) -> bool:
	for choice: Dictionary in get_choices():
		if str(choice.get("choice_id", "")) != choice_id:
			continue
		_apply_effects(choice.get("effects", {}))
		var next_scene: String = str(choice.get("target_node", current_scene_id))
		show_scene(next_scene)
		return true
	return false

## 结局自动收敛：按分支树 choices 声明顺序（即数值设计优先级）自动选择第一个满足条件的选项。
## 用于 auto_route 节点——结局不是由玩家"选"出来的，而是由剧情分支自然导出。
func auto_route(scene_id: String = current_scene_id) -> bool:
	for choice: Dictionary in get_choices(scene_id):
		if _conditions_met(choice.get("conditions", {})):
			_apply_effects(choice.get("effects", {}))
			var next_scene: String = str(choice.get("target_node", scene_id))
			show_scene(next_scene)
			return true
	return false

## 节点是否为自动路由节点（结局判定等不应向玩家暴露选项的节点）。
func is_auto_route(scene_id: String = current_scene_id) -> bool:
	return bool(get_scene_data(scene_id).get("auto_route", false))

func is_terminal(scene_id: String = current_scene_id) -> bool:
	return bool(get_scene_data(scene_id).get("terminal", false))

func _has_node(scene_id: String) -> bool:
	var raw_nodes: Variant = branch_tree.get("nodes", {})
	return raw_nodes is Dictionary and raw_nodes.has(scene_id)

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func _conditions_met(raw_conditions: Variant) -> bool:
	if raw_conditions == null or not (raw_conditions is Dictionary):
		return true
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return false
	for key: Variant in raw_conditions:
		var condition_key: String = str(key)
		var condition: Variant = raw_conditions[key]
		# 简写格式：bool 值 → 检查标志是否匹配
		if condition is bool:
			if bool(state.flags.get(condition_key, false)) != condition:
				return false
			continue
		# 简写格式：int 或 float 值 → 检查数值是否 >= 该值
		# Godot 4 的 JSON.parse_string 将所有数字解析为 float
		if condition is int or condition is float:
			if _read_numeric_state(state, condition_key) < int(condition):
				return false
			continue
		# 完整格式：Dictionary with op/value
		if not (condition is Dictionary):
			continue
		var expected: int = int(condition.get("value", 0))
		var actual: int = _read_numeric_state(state, condition_key)
		var op: String = str(condition.get("op", "gte"))
		if op == "gte" and actual < expected:
			return false
		if op == "lte" and actual > expected:
			return false
		if op == "eq" and actual != expected:
			return false
		if op == "neq" and actual == expected:
			return false
	return true

func _apply_effects(raw_effects: Variant) -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null or not (raw_effects is Dictionary):
		return
	for key: Variant in raw_effects:
		var effect_key: String = str(key)
		var effect: Variant = raw_effects[key]
		# 简写格式：int 或 float 值 → 数值键 add，标志键 set
		# Godot 4 的 JSON.parse_string 将所有数字解析为 float
		if effect is int or effect is float:
			if _is_numeric_key(effect_key):
				_apply_numeric_effect(state, effect_key, "add", int(effect))
			else:
				state.flags[effect_key] = effect
			continue
		# 简写格式：bool 值 → set 标志
		if effect is bool:
			state.flags[effect_key] = effect
			continue
		# 完整格式：Dictionary with op/value
		if not (effect is Dictionary):
			continue
		var op: String = str(effect.get("op", "set"))
		var value: Variant = effect.get("value", true)
		if _is_numeric_key(effect_key):
			_apply_numeric_effect(state, effect_key, op, int(value))
		else:
			state.flags[effect_key] = value
	state.state_changed.emit()

func _is_numeric_key(key: String) -> bool:
	return key in ["insight", "liu_affection", "li_affection", "gui_affection", "fragments", "action_count"]

func _apply_numeric_effect(state: QingfengduGameStateManager, key: String, op: String, value: int) -> void:
	if key == "insight":
		state.insight = _apply_numeric(state.insight, op, value)
	elif key == "fragments":
		state.fragments = _apply_numeric(state.fragments, op, value)
	elif key == "action_count":
		var current: int = int(state.flags.get("action_count", 0))
		var new_val: int = _apply_numeric(current, op, value)
		state.flags["action_count"] = new_val
		state.action_count = new_val
	elif key == "liu_affection":
		var current_val: int = int(state.affection.get("liu", 0))
		state.affection["liu"] = _apply_numeric(current_val, op, value)
	elif key == "li_affection":
		var current_val: int = int(state.affection.get("li", 0))
		state.affection["li"] = _apply_numeric(current_val, op, value)
	elif key == "gui_affection":
		var current_val: int = int(state.affection.get("gui", 0))
		state.affection["gui"] = _apply_numeric(current_val, op, value)

func _apply_numeric(current: int, op: String, value: int) -> int:
	if op == "add":
		return current + value
	if op == "sub":
		return current - value
	return value

func _read_numeric_state(state: QingfengduGameStateManager, key: String) -> int:
	if key == "insight":
		return state.insight
	if key == "fragments":
		return state.fragments
	if key == "liu_affection":
		return int(state.affection.get("liu", 0))
	if key == "li_affection":
		return int(state.affection.get("li", 0))
	if key == "gui_affection":
		return int(state.affection.get("gui", 0))
	return int(state.flags.get(key, 0))
