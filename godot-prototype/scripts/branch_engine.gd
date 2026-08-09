extends Node
## P0 验证：读取 JSON、按最小条件过滤选项；不载入正式分支树。

var prototype_tree: Dictionary = {}

func load_tree(path := "res://data/branch-tree.json") -> bool:
    var file := FileAccess.open(path, FileAccess.READ)
    if file == null:
        push_error("无法读取原型分支 JSON: %s" % path)
        return false
    var parsed = JSON.parse_string(file.get_as_text())
    if not (parsed is Dictionary):
        push_error("原型分支 JSON 格式错误")
        return false
    prototype_tree = parsed
    return true

func get_available_choices(node_id: String) -> Array[Dictionary]:
    var node: Dictionary = prototype_tree.get(node_id, {})
    var result: Array[Dictionary] = []
    for choice in node.get("choices", []):
        if _conditions_met(choice.get("conditions", {})):
            result.append(choice)
    return result

func apply_effects(effects: Dictionary) -> void:
    for key in effects:
        if key == "insight":
            GameStateManager.insight += int(effects[key])
        else:
            GameStateManager.flags[key] = effects[key]
    GameStateManager.state_changed.emit()

func _conditions_met(conditions: Dictionary) -> bool:
    return GameStateManager.insight >= int(conditions.get("min_insight", 0))
