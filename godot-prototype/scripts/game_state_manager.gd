extends Node
## P0 验证：仅保存/恢复最小状态；不含任何正式剧情逻辑。

signal state_changed

var current_scene_id := "prototype"
var day := 1
var slot := 1
var insight := 0
var affection := {"liu": 0, "li": 0, "gui": 0}
var flags: Dictionary = {}

func reset() -> void:
    current_scene_id = "prototype"
    day = 1
    slot = 1
    insight = 0
    affection = {"liu": 0, "li": 0, "gui": 0}
    flags.clear()
    state_changed.emit()

func set_flag(key: String, value: Variant = true) -> void:
    flags[key] = value
    state_changed.emit()

func snapshot() -> Dictionary:
    return {
        "current_scene_id": current_scene_id,
        "day": day,
        "slot": slot,
        "insight": insight,
        "affection": affection.duplicate(true),
        "flags": flags.duplicate(true)
    }

func restore(data: Dictionary) -> void:
    current_scene_id = str(data.get("current_scene_id", "prototype"))
    day = int(data.get("day", 1))
    slot = int(data.get("slot", 1))
    insight = int(data.get("insight", 0))
    affection = data.get("affection", {"liu": 0, "li": 0, "gui": 0}).duplicate(true)
    flags = data.get("flags", {}).duplicate(true)
    state_changed.emit()
