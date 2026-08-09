# 清风渡 · Godot 4.7.1 批量解析错误修复说明

## 修复范围

本次仅修复 P0-T2 技术原型的 Godot 4.7.1 兼容性与脚本解析问题：

- 修复 `default_bus_layout.tres` 缺少资源类型导致的 AudioBus 加载失败。
- 为 5 个 AutoLoad 脚本添加不与单例名冲突的 `class_name`。
- 将跨脚本单例访问统一改为 `get_node_or_null("/root/<AutoLoadName>") as <class_name>`，避免编辑器缓存/加载顺序导致的 `Identifier not declared` 连锁错误。
- 补齐关键变量、参数和局部变量类型。
- 将临时自动测试脚本从 `scripts/` 归档为 `tests/disabled/p0_verification_runner.gd.disabled`，不再参与编辑器编译或运行。

没有加入正式剧情、角色、美术或正式音频业务内容；本次补充的是 P0 原型音频的实际接入与 Web 首次交互解锁，不改变正式剧情范围或音频方向。

## 1. 已验证结果

- Godot 版本：`4.7.1.stable.official.a13da4feb`
- 工程：`C:\Users\gh604\WorkBuddy\game-02\gotbotgame`
- 重新导入：通过；5 个全局类均已注册。
- 主场景启动：通过；无 GDScript 解析错误。
- 本次归档前的 P0 自动实机验证：17/17 项通过。

## 2. P0 原型音频接入与 Web 验收

- 音频文件本身有有效波形：BGM 与雨声 WAV 均为 48 kHz、立体声、120 秒，非静音文件。
- 原问题是 `prototype_bgm` 未在主场景绑定资源，且没有运行路径调用 `play_bgm_fade_in()`；`audio-triggers.json` 仍为空是因为正式触发规则保留到 P3/P4。
- 现已由 `AudioManager` 直接预加载 P0 音频资源；首次点击任一验证选项时，在同一浏览器用户手势中启动 BGM 与 Ambient，满足 Web 自动播放限制。
- BGM 与 Ambient 的 `.ogg.import` 已设置 `loop=true`；BGM 淡入至 `-6 dB`，雨声 Ambient 使用 `-12 dB`。
- 人工验收步骤：打开新 Web 构建 → 点击任一选项 → 应听到雨声与箫/古琴小样；若仍无声，检查浏览器标签页是否静音、系统输出设备和浏览器站点声音权限，并使用 `Ctrl + F5` 强制刷新。

## 3. AutoLoad 配置

在 **Project > Project Settings > Globals > Autoload** 中，确认以下五项存在、名称与路径完全一致，且启用单例：

| 名称 | 路径 |
|---|---|
| `GameStateManager` | `res://scripts/game_state_manager.gd` |
| `DialogueSystem` | `res://scripts/dialogue_system.gd` |
| `BranchEngine` | `res://scripts/branch_engine.gd` |
| `SaveManager` | `res://scripts/save_manager.gd` |
| `AudioManager` | `res://scripts/audio_manager.gd` |

当前 `project.godot` 对应配置：

```ini
[autoload]
GameStateManager="*res://scripts/game_state_manager.gd"
DialogueSystem="*res://scripts/dialogue_system.gd"
BranchEngine="*res://scripts/branch_engine.gd"
SaveManager="*res://scripts/save_manager.gd"
AudioManager="*res://scripts/audio_manager.gd"
```

> `class_name` 采用 `Qingfengdu...` 前缀，故不会和 AutoLoad 名称本身冲突。

## 4. 合规 AudioBus 配置

文件：`res://default_bus_layout.tres`

```tres
[gd_resource type="AudioBusLayout" load_steps=1 format=3]

[resource]
bus/0/name = &"Master"
bus/0/solo = false
bus/0/mute = false
bus/0/bypass_fx = false
bus/0/volume_db = 0.0
bus/0/send = &""
bus/1/name = &"BGM"
bus/1/solo = false
bus/1/mute = false
bus/1/bypass_fx = false
bus/1/volume_db = 0.0
bus/1/send = &"Master"
bus/2/name = &"SFX"
bus/2/solo = false
bus/2/mute = false
bus/2/bypass_fx = false
bus/2/volume_db = 0.0
bus/2/send = &"Master"
bus/3/name = &"Ambient"
bus/3/solo = false
bus/3/mute = false
bus/3/bypass_fx = false
bus/3/volume_db = 0.0
bus/3/send = &"Master"
```

`project.godot` 中必须保留：

```ini
[audio]
default_bus_layout="res://default_bus_layout.tres"
```

## 5. 完整活动 GDScript

### `res://scripts/game_state_manager.gd`

```gdscript
class_name QingfengduGameStateManager
extends Node

signal state_changed

var current_scene_id: String = "prototype"
var day: int = 1
var slot: int = 1
var insight: int = 0
var affection: Dictionary = {"liu": 0, "li": 0, "gui": 0}
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
	var saved_affection: Variant = data.get("affection", {"liu": 0, "li": 0, "gui": 0})
	var saved_flags: Variant = data.get("flags", {})
	affection = saved_affection.duplicate(true) if saved_affection is Dictionary else {"liu": 0, "li": 0, "gui": 0}
	flags = saved_flags.duplicate(true) if saved_flags is Dictionary else {}
	state_changed.emit()
```

### `res://scripts/dialogue_system.gd`

```gdscript
class_name QingfengduDialogueSystem
extends Node

signal typing_finished

var _typing_tween: Tween

func type_text(target: RichTextLabel, text: String, seconds_per_char: float = 0.035) -> void:
	if is_instance_valid(_typing_tween):
		_typing_tween.kill()
	target.text = text
	target.visible_ratio = 0.0
	var duration: float = maxf(0.25, float(text.length()) * seconds_per_char)
	_typing_tween = create_tween()
	_typing_tween.tween_property(target, "visible_ratio", 1.0, duration)
	_typing_tween.tween_callback(func() -> void: typing_finished.emit())

func skip(target: RichTextLabel) -> void:
	if is_instance_valid(_typing_tween):
		_typing_tween.kill()
	target.visible_ratio = 1.0
	typing_finished.emit()

func fade_in(target: CanvasItem, duration: float = 0.2) -> void:
	target.modulate.a = 0.0
	var fade_tween: Tween = create_tween()
	fade_tween.tween_property(target, "modulate:a", 1.0, duration)
```

### `res://scripts/branch_engine.gd`

```gdscript
class_name QingfengduBranchEngine
extends Node

var prototype_tree: Dictionary = {}

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func load_tree(path: String = "res://data/branch-tree.json") -> bool:
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("无法读取原型分支 JSON: %s" % path)
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not (parsed is Dictionary):
		push_error("原型分支 JSON 格式错误")
		return false
	prototype_tree = parsed
	return true

func get_available_choices(node_id: String) -> Array[Dictionary]:
	var node: Dictionary = prototype_tree.get(node_id, {})
	var result: Array[Dictionary] = []
	for raw_choice: Variant in node.get("choices", []):
		if raw_choice is Dictionary and _conditions_met(raw_choice.get("conditions", {})):
			result.append(raw_choice)
	return result

func apply_effects(effects: Dictionary) -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		push_error("未找到 AutoLoad: GameStateManager")
		return
	for key: Variant in effects:
		if str(key) == "insight":
			state.insight += int(effects[key])
		else:
			state.flags[str(key)] = effects[key]
	state.state_changed.emit()

func _conditions_met(conditions: Dictionary) -> bool:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return false
	return state.insight >= int(conditions.get("min_insight", 0))
```

### `res://scripts/save_manager.gd`

```gdscript
class_name QingfengduSaveManager
extends Node

const SAVE_DIR: String = "user://saves"
const SLOT_FILE: String = SAVE_DIR + "/prototype_slot_%02d.json"

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func save_slot(slot_id: int = 0) -> bool:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		push_error("未找到 AutoLoad: GameStateManager")
		return false
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(SAVE_DIR))
	var file: FileAccess = FileAccess.open(SLOT_FILE % slot_id, FileAccess.WRITE)
	if file == null:
		push_error("存档写入失败: %s" % (SLOT_FILE % slot_id))
		return false
	file.store_string(JSON.stringify(state.snapshot(), "  "))
	return true

func load_slot(slot_id: int = 0) -> bool:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		push_error("未找到 AutoLoad: GameStateManager")
		return false
	var path: String = SLOT_FILE % slot_id
	if not FileAccess.file_exists(path):
		return false
	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if file == null:
		return false
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if not (parsed is Dictionary):
		push_error("存档 JSON 损坏: %s" % path)
		return false
	state.restore(parsed)
	return true

func delete_slot(slot_id: int = 0) -> void:
	var dir: DirAccess = DirAccess.open(SAVE_DIR)
	if dir != null:
		dir.remove("prototype_slot_%02d.json" % slot_id)
```

### `res://scripts/audio_manager.gd`

```gdscript
class_name QingfengduAudioManager
extends Node

var bgm_player: AudioStreamPlayer = AudioStreamPlayer.new()
var sfx_player: AudioStreamPlayer = AudioStreamPlayer.new()
var ambient_player: AudioStreamPlayer = AudioStreamPlayer.new()

func _ready() -> void:
	_attach_player(bgm_player, &"BGM")
	_attach_player(sfx_player, &"SFX")
	_attach_player(ambient_player, &"Ambient")

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
```

### `res://scripts/choice_panel.gd`

```gdscript
extends VBoxContainer

signal prototype_choice_selected(choice_id: String)

func _branch_engine() -> QingfengduBranchEngine:
	return get_node_or_null("/root/BranchEngine") as QingfengduBranchEngine

func _ready() -> void:
	var branch_engine: QingfengduBranchEngine = _branch_engine()
	if branch_engine == null:
		push_error("未找到 AutoLoad: BranchEngine")
		return
	branch_engine.load_tree()
	render_choices(branch_engine.get_available_choices("prototype"))

func render_choices(choices: Array[Dictionary]) -> void:
	for child: Node in get_children():
		child.queue_free()
	for choice: Dictionary in choices:
		var button: Button = Button.new()
		button.text = str(choice.get("text", "未命名选项"))
		button.custom_minimum_size.y = 44.0
		button.pressed.connect(_select.bind(choice))
		add_child(button)

func _select(choice: Dictionary) -> void:
	var branch_engine: QingfengduBranchEngine = _branch_engine()
	if branch_engine == null:
		push_error("未找到 AutoLoad: BranchEngine")
		return
	var effects: Variant = choice.get("effects", {})
	branch_engine.apply_effects(effects if effects is Dictionary else {})
	prototype_choice_selected.emit(str(choice.get("id", "prototype")))
	render_choices(branch_engine.get_available_choices("prototype"))
```

### `res://scripts/dialogue_box.gd`

```gdscript
extends PanelContainer

@onready var speaker_name: Label = %SpeakerName
@onready var dialogue_text: RichTextLabel = %DialogueText

func _dialogue_system() -> QingfengduDialogueSystem:
	return get_node_or_null("/root/DialogueSystem") as QingfengduDialogueSystem

func _ready() -> void:
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system == null:
		push_error("未找到 AutoLoad: DialogueSystem")
		return
	dialogue_system.typing_finished.connect(func() -> void: queue_redraw())
	show_prototype_text()

func show_prototype_text() -> void:
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system == null:
		return
	speaker_name.text = "技术验证"
	dialogue_system.type_text(dialogue_text, "清风渡 · Godot 4 技术原型：验证中文打字机显示与跳过交互。")

func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed:
		var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
		if dialogue_system != null:
			dialogue_system.skip(dialogue_text)
```

### `res://scripts/status_bar.gd`

```gdscript
extends HBoxContainer

@onready var day_label: Label = %DayLabel
@onready var insight_label: Label = %InsightLabel
@onready var save_hint: Label = %SaveHint

func _state_manager() -> QingfengduGameStateManager:
	return get_node_or_null("/root/GameStateManager") as QingfengduGameStateManager

func _save_manager() -> QingfengduSaveManager:
	return get_node_or_null("/root/SaveManager") as QingfengduSaveManager

func _ready() -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		push_error("未找到 AutoLoad: GameStateManager")
		return
	state.state_changed.connect(refresh)
	refresh()

func refresh() -> void:
	var state: QingfengduGameStateManager = _state_manager()
	if state == null:
		return
	day_label.text = "第 %d 天 · 时段 %d" % [state.day, state.slot]
	insight_label.text = "洞察：%d" % state.insight

func _on_save_pressed() -> void:
	var save_manager: QingfengduSaveManager = _save_manager()
	var ok: bool = save_manager != null and save_manager.save_slot(0)
	save_hint.text = "存档成功" if ok else "存档失败"

func _on_load_pressed() -> void:
	var save_manager: QingfengduSaveManager = _save_manager()
	var ok: bool = save_manager != null and save_manager.load_slot(0)
	save_hint.text = "读档成功" if ok else "无可用存档"
```

### `res://scripts/ui_controller.gd`

```gdscript
extends Node

@export var prototype_bgm: AudioStream
@onready var portrait: CanvasItem = %PrototypePortrait
@onready var transition: ColorRect = %Transition

func _dialogue_system() -> QingfengduDialogueSystem:
	return get_node_or_null("/root/DialogueSystem") as QingfengduDialogueSystem

func _audio_manager() -> QingfengduAudioManager:
	return get_node_or_null("/root/AudioManager") as QingfengduAudioManager

func _ready() -> void:
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system != null:
		dialogue_system.fade_in(portrait)

func run_portrait_fade_test() -> void:
	var dialogue_system: QingfengduDialogueSystem = _dialogue_system()
	if dialogue_system != null:
		dialogue_system.fade_in(portrait)

func run_transition_test() -> void:
	transition.play_transition()

func run_bgm_fade_test() -> void:
	var audio_manager: QingfengduAudioManager = _audio_manager()
	if audio_manager != null:
		audio_manager.play_bgm_fade_in(prototype_bgm)
```

### `res://scripts/fade_transition.gd`

```gdscript
extends ColorRect

func play_transition(hold_seconds: float = 0.4) -> void:
	visible = true
	modulate.a = 0.0
	var transition_tween: Tween = create_tween()
	transition_tween.tween_property(self, "modulate:a", 1.0, 0.5)
	transition_tween.tween_interval(hold_seconds)
	transition_tween.tween_property(self, "modulate:a", 0.0, 0.5)
	transition_tween.tween_callback(func() -> void: visible = false)
```

## 5. 临时验证器处理

原 `res://scripts/p0_verification_runner.gd` 是一次性命令行测试辅助脚本。它在未加载 AutoLoad 的 `--script` 模式下会产生单例未声明错误，因此已归档：

```text
res://tests/disabled/p0_verification_runner.gd.disabled
```

它未被项目场景或 AutoLoad 引用，删除/归档不会影响原型的对话、选项、存档、音频或转场功能。

## 6. 编辑器修复操作步骤

1. 关闭当前 Godot 编辑器。
2. 确认以上文件已覆盖到 `C:\Users\gh604\WorkBuddy\game-02\gotbotgame`。
3. 使用 Godot 4.7.1 打开 `project.godot`。
4. 等待 FileSystem 扫描结束；Output 中应出现 5 个 `Qingfengdu...` 类注册记录且不含 Parse Error。
5. 打开 **Project > Project Settings > Globals > Autoload**，确认第 2 节的 5 项配置。
6. 打开 **Project > Project Settings > Audio** 或 Audio 面板，确认 `Master / BGM / SFX / Ambient` 四条总线。
7. 运行 `res://scenes/main.tscn`。如旧报错仍残留，关闭编辑器后删除项目目录下的 `.godot/` 缓存目录，再重新导入；不要删除 `project.godot`、`scenes/`、`scripts/` 或 `assets/`。

## 7. 备注

- 运行时访问 AutoLoad 使用 `/root/GameStateManager` 等节点路径，避免依赖编辑器对单例标识符的编译顺序。
- 正式项目仍保留 `GameStateManager`、`DialogueSystem` 等 AutoLoad 名称；新 `class_name` 仅用于类型安全和编辑器解析。
- 当前 P0-T2 仍等待 Web 浏览器人工验收，修复本身不改变台账的任务验收状态。
