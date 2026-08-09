class_name QingfengduAudioManager
extends Node
## P0 验证：BGM/SFX/Ambient 三总线和 Web 首次交互后的音频解锁。

const PROTOTYPE_BGM: AudioStream = preload("res://assets/audio/bgm/bgm_rain_intro_sample.ogg")
const PROTOTYPE_AMBIENT: AudioStream = preload("res://assets/audio/ambient/sfx_rain_continuous_sample.ogg")

var bgm_player: AudioStreamPlayer = AudioStreamPlayer.new()
var sfx_player: AudioStreamPlayer = AudioStreamPlayer.new()
var ambient_player: AudioStreamPlayer = AudioStreamPlayer.new()
var prototype_audio_started: bool = false

func _ready() -> void:
	_attach_player(bgm_player, &"BGM")
	_attach_player(sfx_player, &"SFX")
	_attach_player(ambient_player, &"Ambient")

func start_prototype_mix() -> void:
	if prototype_audio_started:
		return
	prototype_audio_started = true
	play_bgm_fade_in(PROTOTYPE_BGM)
	play_ambient(PROTOTYPE_AMBIENT)
	print("P0 原型音频已在用户交互中启动：BGM + Ambient")

func play_ambient(stream: AudioStream) -> void:
	if stream == null:
		push_warning("P0 原型未分配 Ambient，跳过环境音播放。")
		return
	var bus_index: int = AudioServer.get_bus_index(&"Ambient")
	if bus_index < 0:
		push_error("未找到 Ambient AudioBus")
		return
	ambient_player.stream = stream
	AudioServer.set_bus_volume_db(bus_index, -12.0)
	ambient_player.play()

func _attach_player(player: AudioStreamPlayer, bus: StringName) -> void:
	player.bus = bus
	add_child(player)

func play_bgm_fade_in(stream: AudioStream, seconds: float = 1.0) -> void:
	if stream == null:
		push_warning("P0 原型未分配 BGM，跳过淡入播放。")
		return
	var bus_index: int = AudioServer.get_bus_index(&"BGM")
	if bus_index < 0:
		push_error("未找到 BGM AudioBus")
		return
	bgm_player.stream = stream
	AudioServer.set_bus_volume_db(bus_index, -40.0)
	bgm_player.play()
	var fade_tween: Tween = create_tween()
	fade_tween.tween_method(
		func(value: float) -> void: AudioServer.set_bus_volume_db(bus_index, value),
		-40.0,
		-6.0,
		seconds
	)

func set_bus_muted(bus_name: StringName, muted: bool) -> void:
	var bus_index: int = AudioServer.get_bus_index(bus_name)
	if bus_index >= 0:
		AudioServer.set_bus_mute(bus_index, muted)
