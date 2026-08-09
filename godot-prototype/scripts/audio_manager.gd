extends Node
## P0 验证：BGM/SFX/Ambient 三总线和 BGM 淡入；音频资源由编辑器临时拖入。

var bgm_player := AudioStreamPlayer.new()
var sfx_player := AudioStreamPlayer.new()
var ambient_player := AudioStreamPlayer.new()

func _ready() -> void:
    _attach_player(bgm_player, "BGM")
    _attach_player(sfx_player, "SFX")
    _attach_player(ambient_player, "Ambient")

func _attach_player(player: AudioStreamPlayer, bus: StringName) -> void:
    player.bus = bus
    add_child(player)

func play_bgm_fade_in(stream: AudioStream, seconds := 1.0) -> void:
    if stream == null:
        push_warning("P0 原型未分配 BGM，跳过淡入播放。")
        return
    var bus_index := AudioServer.get_bus_index("BGM")
    if bus_index < 0:
        push_error("未找到 BGM AudioBus")
        return
    bgm_player.stream = stream
    AudioServer.set_bus_volume_db(bus_index, -40.0)
    bgm_player.play()
    var tween := create_tween()
    tween.tween_method(func(value: float) -> void: AudioServer.set_bus_volume_db(bus_index, value), -40.0, -6.0, seconds)

func set_bus_muted(bus_name: StringName, muted: bool) -> void:
    var bus_index := AudioServer.get_bus_index(bus_name)
    if bus_index >= 0:
        AudioServer.set_bus_mute(bus_index, muted)
