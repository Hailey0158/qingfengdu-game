extends Node
## P0 验证入口：仅绑定标准原型组件，不加载正式场景、剧情或资产。

@export var prototype_bgm: AudioStream
@onready var portrait: CanvasItem = %PrototypePortrait
@onready var transition: ColorRect = %Transition

func _ready() -> void:
    DialogueSystem.fade_in(portrait)

func run_portrait_fade_test() -> void:
    DialogueSystem.fade_in(portrait)

func run_transition_test() -> void:
    transition.play_transition()

func run_bgm_fade_test() -> void:
    AudioManager.play_bgm_fade_in(prototype_bgm)
