extends Node
## P0 验证：以 JSON 写入 user://，验证桌面与 Web 持久化路径。

const SAVE_DIR := "user://saves"
const SLOT_FILE := SAVE_DIR + "/prototype_slot_%02d.json"

func save_slot(slot_id := 0) -> bool:
    DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(SAVE_DIR))
    var file := FileAccess.open(SLOT_FILE % slot_id, FileAccess.WRITE)
    if file == null:
        push_error("存档写入失败: %s" % (SLOT_FILE % slot_id))
        return false
    file.store_string(JSON.stringify(GameStateManager.snapshot(), "  "))
    return true

func load_slot(slot_id := 0) -> bool:
    var path := SLOT_FILE % slot_id
    if not FileAccess.file_exists(path):
        return false
    var file := FileAccess.open(path, FileAccess.READ)
    var parsed = JSON.parse_string(file.get_as_text())
    if not (parsed is Dictionary):
        push_error("存档 JSON 损坏: %s" % path)
        return false
    GameStateManager.restore(parsed)
    return true

func delete_slot(slot_id := 0) -> void:
    var dir := DirAccess.open(SAVE_DIR)
    if dir != null:
        dir.remove("prototype_slot_%02d.json" % slot_id)
