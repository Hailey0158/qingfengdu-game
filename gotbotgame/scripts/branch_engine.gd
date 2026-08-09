class_name QingfengduBranchEngine
extends Node
## P1 MVP：读取 JSON、按状态条件过滤选项；柳陆书线运行由 MvpSceneRunner 使用 branch-tree-mvp.json。

var prototype_tree: Dictionary = {}

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func load_tree(path: String = "res://data/branch-tree.json") -> bool:
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("无法读取原型分支 JSON: %s" % path)
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not (parsed is Dictionary):
		push_error("原型分支 JSON 格式错误")
		return false
	prototype_tree = parsed
	return true

func get_available_choices(node_id: String) -> Array[Dictionary]:
	var node: Dictionary = prototype_tree.get(node_id, {})
	var result: Array[Dictionary] = []
	for raw_choice: Variant in node.get("choices", []):
		if raw_choice is Dictionary and _conditions_met(raw_choice.get("conditions", {})):
			result.append(raw_choice)
	return result

func apply_effects(effects: Dictionary) -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		push_error("未找到 AutoLoad: GameStateManager")
		return
	for key: Variant in effects:
		if str(key) == "insight":
			state.insight += int(effects[key])
		else:
			state.flags[str(key)] = effects[key]
	state.state_changed.emit()

func _conditions_met(conditions: Dictionary) -> bool:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return false
	return state.insight >= int(conditions.get("min_insight", 0))
