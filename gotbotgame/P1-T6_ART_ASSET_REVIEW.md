# 《清风渡》P1-T6 美术组占位资产与 Godot 接入评审

- 日期：2026-08-07
- 工程：`C:/Users/gh604/WorkBuddy/game-02/gotbotgame`
- 任务范围：雨夜开场、清风渡客栈大堂、窗边柳陆书第一天
- 交付性质：P1 占位资产；不替代 P3 正式美术量产

## 一、交付物

### 角色占位立绘

- `assets/placeholder_sprites/liu_lushu_reference_placeholder.jpg`
  - 用户提供参考图，继续作为柳陆书 MVP 基准。
  - 视觉锚点：黑发高髻、青灰/青衫、墨竹折扇、含笑试探。
- `assets/placeholder_sprites/li_keying_placeholder.png`
  - 1600×2000 RGBA PNG。
  - 视觉锚点：红发高马尾、黑衣、暗红束带、长刀、沉静冷峻。
- `assets/placeholder_sprites/gui_han_placeholder.png`
  - 1600×2000 RGBA PNG。
  - 视觉锚点：银白长发、白袍、淡蓝剑穗、长剑、清冷克制。

两张新增 PNG 是低细节、半厚涂/水墨方向的程序化占位稿，仅用于验证透明立绘接口、比例和可视层级；不宣称达到 P3 正式立绘质量。

### 场景背景

- `assets/placeholder_sprites/bg_rain_night.png`：1280×720，雨夜山道/清风渡灯笼。
- `assets/placeholder_sprites/bg_inn_hall.png`：1280×720，客栈大堂、烛火暖意。
- `assets/placeholder_sprites/bg_inn_window.png`：1280×720，窗边饮茶、冷青雨色。

## 二、Godot 接入

- `scenes/main.tscn`
  - 保留 `BackgroundLayer` 为 `TextureRect`。
  - 新增 `LiuPortrait`、`LiPortrait`、`GuiPortrait` 三个可视立绘节点。
  - 三个节点均使用完整 `res://` 路径；柳陆书继续复用 `character_sprite.tscn`。
- `scripts/mvp_ui_controller.gd`
  - `scene_010_meet`：显示三位角色。
  - `scene_020_liu_day1`、`scene_021_liu_day1_close`：仅显示柳陆书。
  - 雨夜与“前方无路”节点不显示角色立绘。
- `scripts/ui_controller.gd`
  - 将旧的 `PrototypePortrait` 引用改为当前 `LiuPortrait`，避免已删除节点名残留。
- `assets/placeholder_sprites/README.md`
  - 补充三位角色占位资产说明与 P3 替换边界。

## 三、静态验证结果

- 所有项目 JSON 可解析：通过。
- 主场景、立绘场景、业务脚本中的 `res://` 引用：15 条扫描，缺失 0 条。
- 角色节点 `LiuPortrait` / `LiPortrait` / `GuiPortrait`：存在。
- 新增角色 PNG：均为 1600×2000，PNG 头有效。
- 三张背景 PNG：均为 1280×720，PNG 头有效。
- `.import` 孤立文件：0 个。
- 主场景未引入战斗、卡牌、抽卡、P2 结局或全量三天九时段逻辑：通过。

## 四、人工验证清单（Godot 图形化编辑器）

1. 打开工程，等待 FileSystem 导入完成；确认新增两张 PNG 无红色导入错误。
2. 打开 `scenes/main.tscn`，确认 `BackgroundLayer`、三个人物节点均可选中。
3. 运行项目，确认雨夜开场背景显示且没有立绘。
4. 选择“进去坐会”，确认切换到客栈大堂背景，并同时看到柳陆书、黎客颍、归汉三张占位立绘。
5. 选择走向柳陆书，确认切换到窗边背景，仅显示柳陆书立绘。
6. 继续三项柳陆书 MVP 选择，确认旁白、选项和洞察门槛正常。
7. 使用 Debugger/Output 检查：无 `Node not found: PrototypePortrait`、无纹理加载失败、无脚本解析错误。
8. 在 FileSystem 中确认新增 PNG 的 Import 面板无源文件缺失提示。
9. 确认 P1 范围未出现 P2 结局、战斗、卡牌、抽卡或三天九时段扩展入口。

## 五、风险与边界

- `P1-T6` 的 Godot 4.7.1 无头扫描仍沿用已知阻塞：`first_scan_filesystem` 16% 挂起、`EXIT_CODE=124`。本轮没有重跑或修改导入配置，也没有把静态检查冒充无头构建通过。
- `scripts/scene_manager.gd` 既有的三个预留 `.tscn` 不存在路径仍是中风险；本轮没有擅自改动场景路由。
- 柳陆书当前使用用户 JPG 参考图，仍是 P1 占位；P3 应替换为透明 PNG，并统一三位角色的正式画风、三表情规格。
- 本轮不更新 P1-T6 为 completed；最终准入仍需要 Godot 图形化编辑器人工验证。P3-T1/T2 仍按台账管理，不因本轮占位资产直接宣称正式量产完成。

## 六、评审结论

### 美术总监评审：通过（占位资产门槛）

- 三位角色的身份、服色、武器和气质符合 PDD 视觉锚点。
- 三组背景符合青、黑、白主色与雨夜/客栈/窗边氛围映射。
- 资源规格满足 Godot 占位接入需要；正式质量留待 P3。

### 产品设计总监复核：通过（范围一致性）

- 仅在 `scene_010_meet` 展示三人；柳陆书第一日不越界展示其他角色剧情。
- 未改变文案、分支条件、角色关系或世界观；没有提前展开 P2 内容。

### 技术总监复核：静态通过，GUI 待验

- 资源路径、PNG/JPG 文件、节点名称与运行时显示条件静态一致。
- 旧 `PrototypePortrait` 业务引用已清理。
- 不对已知无头扫描挂起作自动化通过结论。

### 制作人终审：条件通过

- 通过本轮“美术占位资产与安全接入”交付。
- 不通过 P1-T6 最终验收；需完成上方 Godot GUI 人工验证后再决定是否解阻塞。
