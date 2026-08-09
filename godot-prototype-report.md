---
title: "清风渡 P0-T2 Godot 引擎能力验证报告"
version: "0.1"
status: "Godot 4.7.1 桌面实机与 Web 构建通过；待浏览器交互验收"
task_id: "P0-T2"
engine: "Godot 4.x + GDScript"
created: "2026-08-06"
---

# 清风渡 · Godot 引擎能力验证报告

> 范围：仅验证《清风渡》P0 技术底座，不接入正式剧情、角色立绘、成品 BGM 或完整 MVP 内容。
>
> 规范依据：`PRD.md` 第 7 节、`PDD.md` 第七部分·补、`project-ledger.json` 的 `P0-T2`。

## 1. 交付摘要

原型目录：`godot-prototype/`

```text
godot-prototype/
├── project.godot                         # 1280×720、GL Compatibility、5 个 AutoLoad
├── default_bus_layout.tres               # Master / BGM / SFX / Ambient
├── scenes/
│   ├── main.tscn                          # 单场景 UI 验证入口
│   ├── dialogue_box.tscn                  # 对话框原型
│   ├── choice_panel.tscn                  # 选项面板原型
│   ├── status_bar.tscn                    # 状态栏原型
│   ├── fade_transition.tscn               # 黑屏转场原型
│   ├── save_load.tscn                     # 存读档原型入口
│   └── character_sprite.tscn              # 立绘色块占位
├── scripts/
│   ├── game_state_manager.gd              # 最小状态快照/恢复
│   ├── dialogue_system.gd                 # 中文打字机、200ms 淡入
│   ├── branch_engine.gd                   # JSON 分支读取
│   ├── save_manager.gd                    # user:// JSON 存读档
│   ├── audio_manager.gd                   # 三轨与 BGM 淡入
│   ├── ui_controller.gd                   # 原型组件调度
│   ├── dialogue_box.gd                    # 对话框交互
│   ├── choice_panel.gd                    # 选项面板交互
│   ├── status_bar.gd                      # 状态栏交互
│   └── fade_transition.gd                 # 黑屏转场交互
├── data/                                  # PDD 标准数据路径（均为 P0 占位）
│   ├── branch-tree.json
│   ├── character-profiles.json
│   ├── endings-map.json
│   └── audio-triggers.json
├── assets/{sprites,backgrounds,ui}/       # 仅保留占位接入目录
├── assets/audio/{bgm,sfx,ambient}/        # 仅保留接入目录
├── fonts/README.md                        # 可再分发中文字体接入说明
└── TESTING.md                             # 编辑器与 Web 实机测试步骤
```

## 2. 配置结论

| 项目 | 实现 | 结论 |
|---|---|---|
| 引擎与渲染 | Godot 4.x、GDScript、`gl_compatibility` | 可行；更适合 Web 与轻量视觉小说 UI。 |
| 窗口 | 1280×720 基准分辨率、`canvas_items` 拉伸 | 可行；适合 PRD 的横向阅读界面。 |
| 中文路径 | RichTextLabel + 字体嵌入说明 | 架构可行；必须在实机验收前加入获授权 CJK 字体。 |
| Web 兼容 | 兼容渲染器、`user://`、三总线 | 架构可行；导出模板、浏览器音频解锁和存储配额需实测。 |
| 正式内容隔离 | 仅含“技术验证”文本、色块占位与原型 JSON | 通过；未越过 P0 范围。 |

## 3. 四项核心能力结论

| 能力 | 原型实现 | 静态审查 | Godot 实机验收 | 结论 |
|---|---|---|---|---|
| Control 自定义 UI | `main.tscn` 内含对话框、选项面板、状态栏、黑屏转场；全部为 Control 系节点 | 通过 | **Godot 4.7.1 headless 实机通过**：主场景与四类 UI 节点均可实例化 | **可行** |
| JSON 存档系统 | `SaveManager` 将 `GameStateManager.snapshot()` 写入并读取 `user://saves/*.json` | 通过 | **Godot 4.7.1 headless 实机通过**：写入 `user://saves/prototype_slot_00.json` 并恢复洞察值 | **可行** |
| AudioBus 三轨混音 | `default_bus_layout.tres` 定义 BGM/SFX/Ambient；`AudioManager` 支持 BGM -40dB→-6dB 淡入 | 修复后通过 | **Godot 4.7.1 headless 实机通过**：三总线加载、两条 OGG 可读、BGM 淡入与 Ambient 独立播放正常 | **可行** |
| 中文 Tween 动画 | `DialogueSystem` 用 `visible_ratio` 显示中文；对 CanvasItem 使用 200ms Tween 淡入 | 通过 | **Godot 4.7.1 headless 实机通过**：中文文本、打字机补全/跳过及立绘 200ms Tween 完成 | **可行；正式发布仍需嵌入获授权中文字体** |

### 实机验证记录与限制

- **实机版本**：Godot `4.7.1.stable.official.a13da4feb`，使用 `D:\Godot_v4.7.1-stable_win64.exe\Godot_v4.7.1-stable_win64_console.exe`。
- **运行结果**：以正常项目启动方式执行 P0 验证器，17/17 检查通过：主场景、Control UI、中文文本与 `visible_ratio` 打字机、JSON 分支状态、`user://` 存读档、BGM/SFX/Ambient 总线、OGG 资源、BGM 淡入、Ambient 独立播放、200ms 立绘淡入及黑屏转场。
- **修复项**：原 `default_bus_layout.tres` 缺少 `AudioBusLayout` 类型头，Godot 4.7.1 首次导入报解析错误；已修正为 `type="AudioBusLayout"` 并重新导入通过。此修复同时已同步至 `godot-prototype/` 与 `gotbotgame/`。
- **Web 导出**：尚未通过。工程根目录暂缺 `export_presets.cfg`，命令行 Web 导出被 Godot 拦截；也尚未获得 Chrome/微信内置浏览器的人工交互、音频解锁与持久化实测。因此 P0-T2 不转为完成，待建立 Web 预设、安装匹配的 Web export templates 后继续验收。

## 4. UI 原型与验证意图

| 原型 | 文件 | 验证点 | 正式内容状态 |
|---|---|---|---|
| 对话框 | `scenes/main.tscn` + `scripts/ui/dialogue_box.gd` | RichTextLabel 中文打字机、点击跳过 | 无剧情，仅技术提示文字 |
| 选项面板 | `scripts/ui/choice_panel.gd` | JSON 加载、条件显示、状态写入 | 仅两个验证选项 |
| 状态栏 | `scripts/ui/status_bar.gd` | Signal 刷新、存档与读档按钮 | 仅天数/时段/洞察占位数据 |
| 黑屏转场 | `scripts/ui/fade_transition.gd` | 0.5s 淡入 + 0.4s 保持 + 0.5s 淡出 | 无场景或剧情绑定 |

## 5. 编辑器实机测试顺序

完整步骤见 [`godot-prototype/TESTING.md`](godot-prototype/TESTING.md)。建议按以下顺序执行：

1. **导入工程与字体**：以 Godot 4.x 打开 `project.godot`，加入可再分发的思源宋体/Noto Serif CJK SC，并在 Theme 中设为默认字体。
2. **打字机**：运行主场景，检查中文显示、逐字出现和鼠标点击跳过。
3. **存档读写**：选择“洞察 +1”→存档→再变更→读档；检查 `user://saves/prototype_slot_00.json` 与状态恢复。
4. **音频淡入**：将一段短 OGG 临时传给 `AudioManager.play_bgm_fade_in()`，在 Audio 面板观察 BGM/SFX/Ambient 三轨及音量曲线。
5. **立绘占位淡入与转场**：对 `PrototypePortrait` 调用 `DialogueSystem.fade_in()`；对 `Transition` 调用 `play_transition()`。
6. **Web 导出**：用匹配版本的 Web export templates 导出，关闭 Threads，开启 Size optimization；通过本地 HTTP 服务在 Chrome 与微信内置浏览器验收。

## 6. Web 导出风险与处理

| 风险点 | 影响 | 原型处理 / 后续要求 |
|---|---|---|
| 浏览器自动播放策略 | 页面加载即播放 BGM 通常会被拦截 | 在玩家首次“开始/继续”点击后再播放 BGM；不要在 `_ready()` 自动播放。 |
| CJK 字体体积 | 中文 OTF/TTF 可能显著增加首包 | 选择授权清晰的 WOFF2/子集字体；仅保留实际需要字形；字体必须随 Web 包发布。 |
| `user://` 持久化 | 浏览器隐私模式、清理缓存或配额限制会使存档消失 | 使用 JSON 轻量快照；读写失败提供 UI 提示；关键选择前自动存档但不承诺跨设备同步。 |
| WebGL 兼容 | 高级渲染特性、超大纹理会增加失败与加载时间 | 使用 GL Compatibility；P0 不使用着色器特效；后续背景与立绘按 Web 预算压缩。 |
| 音频解码与内存 | 同时加载大音频会抬高首屏和内存占用 | BGM/环境音优先 OGG 流式播放；短 SFX 使用压缩 WAV/OGG；按场景延迟加载。 |
| 微信内置浏览器 | 缓存、音频策略和本地存储行为可能与 Chrome 不同 | 将微信浏览器列为实际发布前必测环境，不能只以桌面 Chrome 结论替代。 |

## 7. 轻量化优化方案

1. **保持一个主场景与可复用 Control 层**：对话框、状态栏、选项面板常驻；仅替换数据和背景，减少场景加载。
2. **数据驱动而非硬编码剧情**：后续只通过 JSON 场景/分支文件接入文本与选择，保留 PDD 所规定的文本与逻辑解耦。
3. **分层按需加载资源**：背景、立绘、BGM 在进入对应场景前预加载；离开后释放不再使用的重资源。
4. **Web 优先的资产预算**：正式立绘保持 PRD 规定的透明 PNG 规格，但生成 Web 副本并压缩；背景优先压缩纹理，避免同时保留多张 2K 原图。
5. **音频三轨常驻、资源按需替换**：AudioStreamPlayer 常驻，切曲时替换 stream；不为每段音频新建节点。
6. **避免 UI 每帧轮询**：状态栏由 `GameStateManager.state_changed` 信号刷新；打字机使用 `visible_ratio` Tween，避免逐字拼接。
7. **存档只存状态，不存资源**：保存场景 ID、时段、洞察、好感与状态标记；资源始终由 `res://` 数据引用恢复。

## 8. 技术总监验收

**结论：部分通过，保留浏览器验收项。** 原型已在 Godot 4.7.1 完成桌面运行时验证，17/17 自动检查通过；Web 预设已建立并成功导出 `build/web/index.html`，导出包共 9 个文件、约 52 MB。

**已通过：** Control UI、JSON `user://` 存档、AudioBus 三轨和 OGG 淡入、中文文本打字机/跳过、200ms 立绘 Tween、黑屏转场、Web 构建流程。

**仍需人工验收：** 用本地 HTTP 服务在 Chrome 与微信内置浏览器检查首屏加载时间、用户首次点击后的音频解锁、中文字体外观与跨刷新存档。当前原型未嵌入可发布 CJK 字体，运行环境采用 Godot 默认中文字形；正式 Web 发布前必须引入授权清晰的中文字体并重新实测。

**优化提醒：** 当前 Web 构建约 52 MB，其中 `index.wasm` 约 38 MB、`index.pck` 约 14 MB，超过 PRD 的首屏 ≤5 秒目标所建议的轻量预算。后续 P1 前应压缩/剔除非原型资源、设置资源导出过滤，并在真实网络下复测加载时间。
