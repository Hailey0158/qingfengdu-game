# 《清风渡》P1-T6 静态完整性审计报告

- 审计日期：2026-08-07
- 工程：`C:/Users/gh604/WorkBuddy/game-02/gotbotgame`
- 审计范围：P1-T6「占位立绘+背景」
- 范围锁定：雨夜开场、清风渡客栈大堂、窗边柳陆书第一天
- 审计方式：只读静态检查
- 明确未执行：无头构建、Web 导出、导入配置修改、全局类名重构、Autoload 增删

## 一、结论摘要

| 项目 | 结论 | 风险 |
|---|---|---|
| `scenes/main.tscn` 背景层 | `TextureRect`，初始绑定雨夜背景，运行时按 MVP 节点切换三组背景路径 | 低 |
| 柳陆书立绘 | `character_sprite.tscn` 使用 `TextureRect`，引用用户 JPG，源文件存在 | 低 |
| MVP 对话/分支 JSON | 6 个 JSON 均可解析为对象；P1 MVP 分支与柳陆书文案范围一致 | 低 |
| `res://` 资源引用 | 主场景、脚本、场景和 JSON 中的资源引用均存在，除 `scene_manager.gd` 的 3 个预留场景路径外 | 中 |
| `.import` 孤立文件 | 11 个 `.import` 均有对应源文件；未发现孤立 `.import` | 低 |
| Autoload / 全局类 | 6 个 Autoload、7 个 `class_name`；数量不大，未发现新增 Autoload 或明显数量异常 | 低-中 |
| 无头扫描 | 本次未执行；沿用已知阻塞：`first_scan_filesystem` 16% 挂起，`EXIT_CODE=124` | 阻塞项，不属于本次静态审计结论 |

**总体判断：** P1-T6 的资源引用链与静态文件完整性良好，可以进入图形化编辑器人工验证；不能据此宣称 Godot 无头扫描或 Web 构建已通过。当前唯一明确的工程业务风险是 `SceneManager` 中登记了 3 个尚未产出的场景文件。

## 二、`scenes/main.tscn` 审计

### 2.1 背景 TextureRect

`main.tscn`：

```text
BackgroundLayer: TextureRect
texture = res://assets/placeholder_sprites/bg_rain_night.png
expand_mode = 1
stretch_mode = 6
```

运行时控制：

```text
scripts/mvp_ui_controller.gd::_apply_visuals(node_id)
```

节点到背景的静态映射：

| MVP 节点 | 背景资源 | 结果 |
|---|---|---|
| `scene_001_rain_night` | `bg_rain_night.png` | 存在 |
| `scene_002_path` | `bg_rain_night.png` | 存在 |
| `ending_front_no_road` | `bg_rain_night.png` | 存在 |
| `scene_003_pay_all` | `bg_inn_hall.png` | 存在 |
| `scene_010_meet` | `bg_inn_hall.png` | 存在 |
| `scene_020_liu_day1` | `bg_inn_window.png` | 存在 |
| `scene_021_liu_day1_close` | `bg_inn_window.png` | 存在 |

静态结论：三组背景路径均使用完整 `res://` 路径，四张对应图片（含初始雨夜图）存在。

### 2.2 柳陆书立绘

`scenes/character_sprite.tscn`：

```text
CharacterSprite: TextureRect
texture = res://assets/placeholder_sprites/liu_lushu_reference_placeholder.jpg
stretch_mode = 5
```

`main.tscn` 中通过 `PrototypePortrait` 实例化；`mvp_ui_controller.gd` 仅在以下节点显示：

```text
scene_020_liu_day1
scene_021_liu_day1_close
```

静态结论：立绘源文件存在，路径有效，显示范围没有扩展到 P2 角色或其他剧情段。

## 三、JSON 与剧情配置审计

扫描文件共 6 个，均成功解析为顶层 `Dictionary/object`：

```text
data/audio-triggers.json
 data/branch-tree-mvp.json
 data/branch-tree.json
 data/character-profiles.json
 data/endings-map.json
 data/final-dialogue/mvp/liu_lushu_day1.json
```

### P1-T6 相关配置

- `branch-tree-mvp.json`：
  - `schema_version`、`task_id`、`route`、`scope`、`nodes` 存在；
  - MVP 节点覆盖雨夜开场、初识、柳陆书第一天、第一日收束和“前方无路”彩蛋；
  - 未发现 P2 终局、战斗、卡牌或全量三天九时段节点被接入运行时。
- `liu_lushu_day1.json`：
  - `schema_version`、`task_id`、`route`、`scope`、`style_notes`、`nodes` 存在；
  - 文案节点与 MVP 对话节点对应；
  - 柳陆书文本保持半文半白、玩笑试探和留白，没有提前揭示二十年前真相。

### 非阻塞观察

- `branch-tree.json`、`endings-map.json`、`character-profiles.json` 属于项目既有全局/原型配置；本次未修改，也未将其扩展到 P1-T6 运行链。
- MVP 分支中部分 `scene_ref` 使用 `mvp-inline:*`，这是当前配置中的显式内联节点标记，不是资源路径；不应误判为缺失 `.tscn`。

## 四、脚本与废弃节点引用审计

### 4.1 `res://` 路径检查

脚本、场景和 JSON 中共发现 3 条实际不存在的资源路径，全部位于：

```text
scripts/scene_manager.gd
```

具体为：

```text
res://scenes/001_rain.tscn
res://scenes/010_meet.tscn
res://scenes/020_liu_day1.tscn
```

这些文件当前不存在；对应的内容脚本实际是：

```text
scenes/001_rain.scene.md
scenes/010_meet.scene.md
scenes/020_liu_day1.scene.md
```

`SceneManager.change_scene()` 已有 `ResourceLoader.exists()` 失败保护，因此不会静默加载错误资源，但如果未来业务代码调用这 3 个 scene_id，会触发警告并切换失败。

**风险等级：中。**

本次不修复，原因：用户明确要求只做静态分析，且该问题属于场景路由业务设计，不应在审计阶段擅自重构或生成新场景。

### 4.2 废弃节点名称

当前 P1-T6 主链使用的节点与脚本引用一致：

```text
Root/DialogueBox
Root/ChoicePanel
Root/MvpSceneRunner
Root/BackgroundLayer
Root/CharacterLayer/PrototypePortrait
```

未发现主链脚本继续引用已删除的 `ColorRect` 类型或旧的 P0 对话节点名称。

### 4.3 业务范围检查

- 当前主场景只有一套 MVP 运行器和一套柳陆书立绘占位实例。
- 未发现新增 Autoload。
- 未发现通过本轮资源接入引入战斗、卡牌、抽卡、收集、多时段或 P2 结局业务逻辑。

## 五、`.import` 孤立文件审计

共发现 11 个 `.import` 文件，逐一检查对应源文件均存在：

- `icon.svg.import` → `icon.svg`
- `CMSFont-Bold.TTF.import` → `CMSFont-Bold.TTF`
- `assets/sprites/liu_lushu_calm_style_concept.png.import` → 对应 PNG
- `assets/sprites/style-concept.png.import` → 对应 PNG
- 4 个音频 `.ogg/.wav.import` → 对应音频源文件
- 3 个 `build/web` 图标 PNG `.import` → 对应图标源文件

**结论：未发现孤立 `.import` 文件。**

本审计没有执行删除操作。

## 六、Autoload 与全局类清单

### 6.1 Autoload：6 个

```text
GameStateManager → res://scripts/game_state_manager.gd
DialogueSystem   → res://scripts/dialogue_system.gd
BranchEngine     → res://scripts/branch_engine.gd
SaveManager      → res://scripts/save_manager.gd
AudioManager     → res://scripts/audio_manager.gd
SceneManager     → res://scripts/scene_manager.gd
```

### 6.2 `class_name`：7 个

```text
QingfengduAudioManager       scripts/audio_manager.gd
QingfengduBranchEngine       scripts/branch_engine.gd
QingfengduDialogueSystem     scripts/dialogue_system.gd
QingfengduGameStateManager   scripts/game_state_manager.gd
QingfengduMvpSceneRunner     scripts/mvp_scene_runner.gd
QingfengduSaveManager        scripts/save_manager.gd
QingfengduSceneManager       scripts/scene_manager.gd
```

### 6.3 对无头扫描挂起的评估

数量层面：6 个 Autoload + 7 个全局脚本类对于当前小型 Godot MVP 工程并不构成明显的规模诱因；本次没有证据表明数量本身导致 16% 阶段挂起。

更值得在后续图形化编辑器中观察的风险：

1. Autoload 脚本在项目初始化时会参与全局类解析，任何单个脚本解析异常都可能放大全局扫描阶段的问题。
2. `class_name` 与 Autoload 结合属于已有架构，不建议为了绕过挂起而批量删除或重命名。
3. 当前工程存在一个独立的 `SceneManager` 预留路径风险，但它不是全局类数量问题。
4. 本次静态检查没有能力证明 Godot 引擎自身在该环境下的扫描挂起原因；保持已知阻塞，不作因果断言。

## 七、风险清单

| 编号 | 风险 | 等级 | 影响 | 建议 |
|---|---|---:|---|---|
| R1 | `SceneManager` 登记 3 个不存在的 `.tscn` | 中 | 未来调用对应 scene_id 时切场失败 | 后续单独安排场景路由收口；不要在本审计中生成新场景 |
| R2 | Godot 4.7.1 无头扫描在 16% 挂起 | 阻塞 | 无法用无头模式完成导出验收 | 保持现状；改用图形化编辑器人工验证，不以无头结果替代人工验收 |
| R3 | `.import` 由 Godot GUI 重新导入后可能重新生成 | 低 | 需要再次确认源文件映射 | 每次导入后检查 `source_file` 与源文件存在性 |
| R4 | `character_sprite.tscn` 使用 JPG 参考图而非最终 PNG 透明立绘 | 低（符合 P1 占位范围） | 当前有背景矩形/参考图底色，不代表 P3 正式美术 | P3 再替换为符合规格的透明 PNG；P1 不扩大范围 |
| R5 | 当前静态审计未证明音频、存档、浏览器刷新恢复 | 低（非本任务目标） | 不能把静态通过理解为完整 MVP 验收 | 由图形化编辑器按人工清单逐项验证 |

## 八、本地编辑器可验证功能

以下项目应在 Godot 图形化编辑器中打开工程后验证：

1. 打开工程并确认 FileSystem 面板无导入错误或红色资源。
2. 双击 `scenes/main.tscn`，确认 `BackgroundLayer` 类型为 `TextureRect`，初始纹理为 `bg_rain_night.png`。
3. 打开 `scenes/character_sprite.tscn`，确认节点类型为 `TextureRect`，纹理为柳陆书参考 JPG。
4. 运行项目，确认雨夜开场背景显示，旁白和选项可见。
5. 选择“终于有个能休息的地方了，进去坐会！”，确认背景切换为客栈大堂占位图。
6. 在大堂选择“走向窗边的柳陆书”或先观察扇子，确认背景切换为窗边饮茶占位图。
7. 确认柳陆书立绘仅在 `scene_020_liu_day1` 与 `scene_021_liu_day1_close` 显示。
8. 依次测试柳陆书三项 MVP 选择；确认第三项洞察门槛行为符合配置。
9. 确认第一日收束节点隐藏选项，文案显示“第一日暂告一段落”。
10. 选择开场“走到底”路径，确认“前方无路”终止节点可达。
11. 打开 Output / Debugger，确认没有资源加载失败、节点路径错误或脚本解析错误。
12. 在 FileSystem 中逐个查看 `.import` 关联资源，确认没有“源文件不存在”的导入报错。

## 九、自动化无头构建阻塞

本报告没有重新运行无头命令，也没有尝试修复该阻塞。

已知事实仅沿用项目记录：

```text
Godot 4.7.1 headless
first_scan_filesystem → 16%
EXIT_CODE=124
```

因此本报告中的“静态完整性通过”不等于：

- 无头扫描通过；
- Web 导出通过；
- 浏览器人工验收通过；
- P1-T6 已完成；
- 可以将台账中的 P1-T6 改为 completed。

## 十、审计收口意见

- 产品设计总监：从静态范围看，资源接入没有越过 P1-T6 边界，未发现 P2 内容污染；可进入图形化编辑器内容与视觉验收。
- 美术总监：背景三组资源路径与色调用途匹配 PDD 的青黑白方向；柳陆书参考图符合 PDD 视觉锚点，但仍是 P1 占位，不是 P3 正式透明立绘。
- 技术总监：主场景资源引用、JSON、脚本路径和 `.import` 映射静态完整；`SceneManager` 三条不存在场景路径列为中风险；无头挂起保持阻塞，不作自动化通过结论。
- 制作人：本报告通过“静态审计”这一交付门槛，不通过 P1-T6 最终验收；下一步应执行图形化编辑器人工验证，并单独决定是否收口 `SceneManager` 预留路径问题。
