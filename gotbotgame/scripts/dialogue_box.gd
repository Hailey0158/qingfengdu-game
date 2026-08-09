extends PanelContainer
## P1 MVP 对话框：承载角色名、旁白和打字机文本；点击正文可跳过当前打字。

@onready var dialogue_text: RichTextLabel = %DialogueText

func _dialogue_system() -> QingfengduDialogueSystem:
	return get_node_or_null("/root/DialogueSystem") as QingfengduDialogueSystem

func _ready() -> void:
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system == null:
		push_error("未找到 AutoLoad: DialogueSystem")

func show_text(speaker: String, text: String) -> void:
	var speaker_name: Label = %SpeakerName
	speaker_name.text = speaker
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system != null:
		dialogue_system.type_text(dialogue_text, text)

func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
		if dialogue_system != null:
			dialogue_system.skip(dialogue_text)
