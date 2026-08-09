extends Node
## 兼容控制器：旧场景若引用此脚本时，仅提供通用立绘淡入与转场能力。

@onready var portrait: CanvasItem = get_node_or_null("../CharacterLayer/LiuPortrait")
@onready var transition: ColorRect = %Transition

func _dialogue_system() -> QingfengduDialogueSystem:
	return get_node_or_null("/root/DialogueSystem") as QingfengduDialogueSystem

func _ready() -> void:
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system != null and is_instance_valid(portrait):
		dialogue_system.fade_in(portrait)

func play_portrait_fade() -> void:
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system != null and is_instance_valid(portrait):
		dialogue_system.fade_in(portrait)

func play_transition() -> void:
	if is_instance_valid(transition):
		transition.play_transition()
