extends PanelContainer
## P0 验证：中文 RichTextLabel 打字机、单击跳过。

@onready var speaker_name: Label = %SpeakerName
@onready var dialogue_text: RichTextLabel = %DialogueText

func _ready() -> void:
    DialogueSystem.typing_finished.connect(func() -> void: queue_redraw())
    show_prototype_text()

func show_prototype_text() -> void:
    speaker_name.text = "技术验证"
    DialogueSystem.type_text(dialogue_text, "清风渡 · Godot 4 技术原型：验证中文打字机显示与跳过交互。")

func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        DialogueSystem.skip(dialogue_text)
