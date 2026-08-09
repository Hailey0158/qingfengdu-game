extends VBoxContainer
## P0 验证：动态选项创建、JSON 条件过滤、效果写入。

signal prototype_choice_selected(choice_id: String)

func _ready() -> void:
    BranchEngine.load_tree()
    render_choices(BranchEngine.get_available_choices("prototype"))

func render_choices(choices: Array[Dictionary]) -> void:
    for child in get_children():
        child.queue_free()
    for choice in choices:
        var button := Button.new()
        button.text = str(choice.get("text", "未命名选项"))
        button.custom_minimum_size.y = 44.0
        button.pressed.connect(_select.bind(choice))
        add_child(button)

func _select(choice: Dictionary) -> void:
    BranchEngine.apply_effects(choice.get("effects", {}))
    prototype_choice_selected.emit(str(choice.get("id", "prototype")))
    render_choices(BranchEngine.get_available_choices("prototype"))
