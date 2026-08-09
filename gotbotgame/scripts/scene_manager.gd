class_name QingfengduSceneManager
extends Node
## P1 MVP：统一管理 scene_id 到 PackedScene 的加载和切换。

signal scene_change_started(scene_id: String)
signal scene_changed(scene_id: String)
signal scene_change_failed(scene_id: String)

var scene_paths: Dictionary = {
	"prototype": "res://scenes/main.tscn",
	"scene_001_rain_night": "res://scenes/001_rain.tscn",
	"scene_010_meet": "res://scenes/010_meet.tscn",
	"scene_020_liu_day1": "res://scenes/020_liu_day1.tscn"
}

var current_scene_id: String = "prototype"

func get_scene_path(scene_id: String) -> String:
	return str(scene_paths.get(scene_id, ""))

func has_scene(scene_id: String) -> bool:
	return not get_scene_path(scene_id).is_empty()

func change_scene(scene_id: String) -> bool:
	var scene_path: String = get_scene_path(scene_id)
	if scene_path.is_empty():
		push_error("未注册的清风渡场景 ID: %s" % scene_id)
		scene_change_failed.emit(scene_id)
		return false
	if not ResourceLoader.exists(scene_path, "PackedScene"):
		push_warning("场景尚未产出，暂不能切换: %s -> %s" % [scene_id, scene_path])
		scene_change_failed.emit(scene_id)
		return false
	current_scene_id = scene_id
	scene_change_started.emit(scene_id)
	get_tree().change_scene_to_file(scene_path)
	var state: QingfengduGameStateManager = get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager
	if state != null:
		state.current_scene_id = scene_id
	scene_changed.emit(scene_id)
	return true

func register_scene(scene_id: String, scene_path: String) -> void:
	if scene_id.is_empty() or scene_path.is_empty():
		push_error("场景注册需要非空 scene_id 和 scene_path")
		return
	scene_paths[scene_id] = scene_path
