# P1-T6 MVP 三角色立绘集成复核

日期：2026-08-07

## 1. 集成范围

本轮只修改 P1 MVP 的角色视觉资源与节点布局，不扩展剧情、分支、结局、战斗、卡牌或多时段系统。

运行时场景保持：

- 雨夜开场：不显示角色立绘；
- 客栈大堂 `scene_010_meet`：归汉（左）、黎客颍（中）、柳陆书（右）；
- 窗边柳陆书第一日 `scene_020_liu_day1` / `scene_021_liu_day1_close`：仅显示柳陆书。

## 2. 用户确认的来源图

- 归汉：`assets/generated_portraits/workbuddy-generated-eRNYZ3bk8s88MqYfPsW-EpOl7Gu9qSdjKYWxB_OpYIw.png`
- 黎客颍：`assets/generated_portraits/workbuddy-generated-HRlVaCuaypgoMDIrkpDNrAYon9Nq_ID0B-PKqkpuDSA.png`
- 柳陆书：`assets/generated_portraits/workbuddy-generated-ZSIIwtV3s9sdbW1R7uZj4BaYj1Bgich6WssCzMSNAO8.png`

三张来源均为 1122×1402 RGB PNG，棋盘格已烘焙，不具备真实 Alpha；原图保持不变。

## 3. Godot 运行时资源

通过 `tools/prepare_mvp_portraits.py` 进行边缘连通背景分离、裁边、等比例缩放与透明安全区补齐，生成：

- `assets/sprites/mvp/gui_han_calm_transparent.png`
- `assets/sprites/mvp/li_keying_calm_transparent.png`
- `assets/sprites/mvp/liu_lushu_calm_transparent.png`

统一规格：

- 1600×2000 px；
- RGBA PNG；
- Alpha 范围 0–255；
- PNG 色彩类型为 6（RGBA），四角与整圈画布边缘 Alpha 均为 0；
- 全透明像素比例：归汉 72.14%、黎客颍 73.72%、柳陆书 66.70%；
- 完整保留头顶、衣摆、武器与宽袖；
- 保持纵横比，不进行非等比拉伸；
- 底部基线统一，适配 `TextureRect` / `Sprite2D`。

## 4. Godot 接入

- `scenes/character_sprite.tscn` 改为引用柳陆书 MVP 运行时资源；
- `scenes/main.tscn` 改为引用归汉、黎客颍 MVP 运行时资源；
- 三个角色框调整为 370×462 px，顶部 38、底部 500，对应 1280×720 画面约 64% 屏高；
- 横向位置：归汉 50–420、黎客颍 455–825、柳陆书 860–1230；
- `mvp_ui_controller.gd` 的可见性规则保持不变。

## 5. 静态验收

通过：

- 三张运行时 PNG 尺寸、RGBA、PNG 色彩类型与 Alpha 像素级检查；
- 四角及整圈外缘完全透明，不再把烘焙棋盘格当作透明背景；
- `main.tscn`、`character_sprite.tscn`、`mvp_ui_controller.gd` 的 `res://` 引用检查；
- `LiuPortrait`、`LiPortrait`、`GuiPortrait` 节点存在；
- 6 个 JSON 文件全部可解析；
- 未发现孤立 `.import`。

## 6. 规范同步

用户确认归汉黑发版本进入当前 MVP，因此 PRD/PDD 的归汉视觉锚点由“银白长发”同步调整为“墨黑长发”；白袍、长剑、淡蓝剑穗、冷淡内敛与无相宗身份保持不变。

## 7. 评审结论

### 美术总监

通过本轮 MVP 运行时资源规格与三人并列比例方案：三张立绘风格、色调和人物辨识度满足当前 MVP 门槛。棋盘背景通过保守 Alpha 分离处理，未把 RGB 原图直接冒充透明资源。

### 技术总监

静态接入通过：资源存在、路径完整、节点接口与业务可见性规则一致，未新增 Autoload 或全局类，未产生孤立 `.import`。

### 制作人

条件通过“立绘资源接入”子项；P1-T6 总任务仍保持 `blocked`，原因是本轮未执行 Godot 图形化编辑器人工验收，且既有 Godot 4.7.1 无头扫描阻塞尚未闭环。不得将本报告解释为 Web 构建或 P1-T6 总体验收通过。

## 8. 图形化编辑器人工检查清单

1. 打开 `scenes/main.tscn`，确认没有缺失资源提示；
2. 运行后在雨夜节点确认三人均隐藏；
3. 进入客栈大堂，确认三人从左至右为归汉、黎客颍、柳陆书；
4. 检查三人头顶、衣摆和武器没有被裁断；
5. 检查三人脚底基线接近一致，身高比例自然；
6. 检查对话框遮挡不超过角色下半身可接受范围；
7. 进入柳陆书窗边节点，确认只显示柳陆书；
8. 检查透明边缘无明显棋盘格、白边或白色方框；
9. 检查 Debugger 无资源加载、节点路径或类型错误；
10. 完成人工截图后，再决定是否解除 P1-T6 阻塞并进入 P1-T8。
