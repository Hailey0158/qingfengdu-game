class_name QingfengduGameStateManager
extends Node
## P1 MVP：全局剧情状态，负责生成可持久化的完整存档快照。

signal state_changed

const DEFAULT_AFFECTION: Dictionary = {"liu": 0, "li": 0, "gui": 0}

var current_scene_id: String = "scene_001_rain_night"
var current_node_id: String = "scene_001_rain_night"
var path_taken: Array[String] = []
var weather: String = "rainy_night"
var day: int = 1
var current_slot: String = "morning"
var slot: int = 1
var action_count: int = 0
var playtime_seconds: int = 0
var insight: int = 0
var fragments: int = 0
var affection: Dictionary = DEFAULT_AFFECTION.duplicate(true)
var flags: Dictionary = {}
var collected_clues: Array[Dictionary] = []
var obtained_items: Array[Dictionary] = []
var ending_unlocked: Array[String] = []

func reset() -> void:
	current_scene_id = "scene_001_rain_night"
	current_node_id = "scene_001_rain_night"
	path_taken.clear()
	weather = "rainy_night"
	day = 1
	current_slot = "morning"
	slot = 1
	action_count = 0
	playtime_seconds = 0
	insight = 0
	fragments = 0
	affection = DEFAULT_AFFECTION.duplicate(true)
	flags.clear()
	collected_clues.clear()
	obtained_items.clear()
	ending_unlocked.clear()
	state_changed.emit()

func set_current_node(scene_id: String, node_id: String = "") -> void:
	current_scene_id = scene_id
	current_node_id = node_id if not node_id.is_empty() else scene_id
	if path_taken.is_empty() or path_taken.back() != current_node_id:
		path_taken.append(current_node_id)
	state_changed.emit()

func set_flag(key: String, value: Variant = true) -> void:
	flags[key] = value
	state_changed.emit()

func snapshot() -> Dictionary:
	return {
		"schema_version": "qingfengdu.save.mvp.1",
		"current_scene": current_scene_id,
		"save_timestamp": Time.get_datetime_string_from_system(true),
		"playtime_seconds": playtime_seconds,
		"branch_state": {
			"current_node": current_node_id,
			"path_taken": path_taken.duplicate()
		},
		"global_vars": {
			"weather": weather,
			"day": day,
			"current_slot": current_slot,
			"slot": slot,
			"action_count": action_count,
			"insight": insight,
			"fragments": fragments
		},
		"relationship_vars": {
			"liu_affection": int(affection.get("liu", 0)),
			"li_affection": int(affection.get("li", 0)),
			"gui_affection": int(affection.get("gui", 0))
		},
		"player_flags": flags.duplicate(true),
		"collected_clues": collected_clues.duplicate(true),
		"obtained_items": obtained_items.duplicate(true),
		"ending_unlocked": ending_unlocked.duplicate()
	}

func restore(data: Dictionary) -> void:
	current_scene_id = str(data.get("current_scene", data.get("current_scene_id", current_scene_id)))
	var branch_state: Variant = data.get("branch_state", {})
	if branch_state is Dictionary:
		current_node_id = str(branch_state.get("current_node", current_scene_id))
		var saved_path: Variant = branch_state.get("path_taken", [])
		path_taken = _string_array(saved_path)
	var global_vars: Variant = data.get("global_vars", {})
	if global_vars is Dictionary:
		weather = str(global_vars.get("weather", weather))
		day = int(global_vars.get("day", day))
		current_slot = str(global_vars.get("current_slot", current_slot))
		slot = int(global_vars.get("slot", slot))
		action_count = int(global_vars.get("action_count", action_count))
		insight = int(global_vars.get("insight", insight))
		fragments = int(global_vars.get("fragments", fragments))
	playtime_seconds = int(data.get("playtime_seconds", playtime_seconds))
	var relationships: Variant = data.get("relationship_vars", {})
	if relationships is Dictionary:
		affection = {
			"liu": int(relationships.get("liu_affection", 0)),
			"li": int(relationships.get("li_affection", 0)),
			"gui": int(relationships.get("gui_affection", 0))
		}
	var saved_flags: Variant = data.get("player_flags", data.get("flags", {}))
	flags = saved_flags.duplicate(true) if saved_flags is Dictionary else {}
	collected_clues = _dictionary_array(data.get("collected_clues", []))
	obtained_items = _dictionary_array(data.get("obtained_items", []))
	ending_unlocked = _string_array(data.get("ending_unlocked", []))
	state_changed.emit()

func _string_array(value: Variant) -> Array[String]:
	var result: Array[String] = []
	if value is Array:
		for item: Variant in value:
			result.append(str(item))
	return result

func _dictionary_array(value: Variant) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	if value is Array:
		for item: Variant in value:
			if item is Dictionary:
				result.append(item.duplicate(true))
	return result
