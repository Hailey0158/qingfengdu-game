class_name QingfengduSaveManager
extends Node
## P1 MVP：JSON user:// 存档，支持 10 个手动槽位、自动槽位和日终槽位。

signal save_completed(slot_id: String)
signal load_completed(slot_id: String)
signal save_failed(slot_id: String, reason: String)

const SAVE_DIR: String = "user://saves"
const SAVE_SCHEMA: String = "qingfengdu.save.mvp.1"
const AUTO_SLOT: String = "slot_auto"
const DAY_END_SLOT: String = "slot_day_end"
const MANUAL_SLOT_MIN: int = 1
const MANUAL_SLOT_MAX: int = 10

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func save_slot(slot_id: int = 1) -> bool:
	if not _is_manual_slot(slot_id):
		return _fail(str(slot_id), "手动槽位必须为 1 到 10")
	return save_named_slot(_manual_slot_name(slot_id))

func load_slot(slot_id: int = 1) -> bool:
	if not _is_manual_slot(slot_id):
		return false
	return load_named_slot(_manual_slot_name(slot_id))

func save_auto() -> bool:
	return save_named_slot(AUTO_SLOT)

func load_auto() -> bool:
	return load_named_slot(AUTO_SLOT)

func save_day_end() -> bool:
	return save_named_slot(DAY_END_SLOT)

func load_day_end() -> bool:
	return load_named_slot(DAY_END_SLOT)

func save_named_slot(slot_id: String) -> bool:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return _fail(slot_id, "未找到 AutoLoad: GameStateManager")
	if slot_id.is_empty():
		return _fail(slot_id, "槽位 ID 不能为空")
	var payload: Dictionary = state.snapshot()
	payload["save_slot_id"] = slot_id
	return _write_json_atomic(slot_id, payload)

func load_named_slot(slot_id: String) -> bool:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null or slot_id.is_empty():
		return false
	var path: String = _slot_path(slot_id)
	if not FileAccess.file_exists(path):
		return false
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not (parsed is Dictionary):
		return _fail(slot_id, "存档 JSON 损坏")
	if str(parsed.get("schema_version", "")) != SAVE_SCHEMA:
		return _fail(slot_id, "存档版本不兼容")
	state.restore(parsed)
	load_completed.emit(slot_id)
	return true

func list_slots() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	for slot_id: String in _all_slot_ids():
		var path: String = _slot_path(slot_id)
		var entry: Dictionary = {"slot_id": slot_id, "exists": FileAccess.file_exists(path)}
		if entry["exists"]:
			entry.merge(_read_summary(path))
		result.append(entry)
	return result

func has_slot(slot_id: String) -> bool:
	return FileAccess.file_exists(_slot_path(slot_id))

func delete_slot(slot_id: int = 1) -> bool:
	if not _is_manual_slot(slot_id):
		return false
	return delete_named_slot(_manual_slot_name(slot_id))

func delete_named_slot(slot_id: String) -> bool:
	var dir: DirAccess = DirAccess.open(SAVE_DIR)
	if dir == null:
		return false
	return dir.remove(_file_name(slot_id)) == OK

func _write_json_atomic(slot_id: String, payload: Dictionary) -> bool:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(SAVE_DIR))
	var final_path: String = _slot_path(slot_id)
	var temp_path: String = final_path + ".tmp"
	var file: FileAccess = FileAccess.open(temp_path, FileAccess.WRITE)
	if file == null:
		return _fail(slot_id, "无法创建临时存档")
	file.store_string(JSON.stringify(payload, "  "))
	file.flush()
	file.close()
	var absolute_temp_path: String = ProjectSettings.globalize_path(temp_path)
	var absolute_final_path: String = ProjectSettings.globalize_path(final_path)
	if DirAccess.rename_absolute(absolute_temp_path, absolute_final_path) != OK:
		return _fail(slot_id, "原子替换存档失败")
	save_completed.emit(slot_id)
	return true

func _read_summary(path: String) -> Dictionary:
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not (parsed is Dictionary):
		return {"valid": false}
	return {
		"valid": true,
		"save_timestamp": parsed.get("save_timestamp", ""),
		"current_scene": parsed.get("current_scene", ""),
		"day": int(parsed.get("global_vars", {}).get("day", 1)) if parsed.get("global_vars", {}) is Dictionary else 1,
		"liu_affection": int(parsed.get("relationship_vars", {}).get("liu_affection", 0)) if parsed.get("relationship_vars", {}) is Dictionary else 0
	}

func _state_path_id(slot_id: String) -> String:
	return slot_id.validate_filename()

func _slot_path(slot_id: String) -> String:
	return "%s/%s.json" % [SAVE_DIR, _file_name(slot_id)]

func _file_name(slot_id: String) -> String:
	return "qingfengdu_%s" % _state_path_id(slot_id)

func _manual_slot_name(slot_id: int) -> String:
	return "slot_%02d" % slot_id

func _all_slot_ids() -> Array[String]:
	var result: Array[String] = []
	for slot_id: int in range(MANUAL_SLOT_MIN, MANUAL_SLOT_MAX + 1):
		result.append(_manual_slot_name(slot_id))
	result.append(AUTO_SLOT)
	result.append(DAY_END_SLOT)
	return result

func _is_manual_slot(slot_id: int) -> bool:
	return slot_id >= MANUAL_SLOT_MIN and slot_id <= MANUAL_SLOT_MAX

func _fail(slot_id: String, reason: String) -> bool:
	save_failed.emit(slot_id, reason)
	push_error("存档失败 [%s]：%s" % [slot_id, reason])
	return false
