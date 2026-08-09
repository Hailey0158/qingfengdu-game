# P1-T6 资源扫描与 Web 验收报告

日期：2026-08-07
工程：`gotbotgame/`
引擎：Godot 4.7.1 stable

## 已完成

- 清理 `assets/placeholder_sprites/` 中指向不存在源文件的 `.import` 残留。
- 新增三张可追踪的 1280×720 PNG 背景占位：
  - `bg_rain_night.png`：雨夜山道/清风渡灯笼的青黑冷调。
  - `bg_inn_hall.png`：客栈大堂的青黑白与暖灯色调。
  - `bg_inn_window.png`：窗边饮茶的青黑白水墨色调。
- 将 `scenes/character_sprite.tscn` 从 `ColorRect` 占位改为 `TextureRect`，安全加载：
  - `assets/placeholder_sprites/liu_lushu_reference_placeholder.jpg`
- 将 `scenes/main.tscn` 的背景层改为 `TextureRect`，并在 `mvp_ui_controller.gd` 中按 MVP 节点切换三组背景资源。
- 静态检查通过：主场景所有 `res://` 引用存在；分支 JSON 与柳陆书 MVP 文案 JSON 可解析；四项占位图片均存在且有非零文件大小。

## 无头扫描结果

执行：

```text
Godot_v4.7.1-stable_win64_console.exe --headless --path gotbotgame --editor --quit
```

结果：未再出现此前的 signal 11；但进程在 `first_scan_filesystem` 的 16%（加载全局类名）阶段持续挂起。90 秒硬超时返回 `124`，并出现 Godot 退出清理阶段的线程/RID 泄漏警告。

## Web 构建结果

尝试使用 Web 预设导出到 `build/web-t6/index.html`。导出进程同样停在资源扫描 16% 阶段，因未生成完整产物而中止。`build/web-t6/` 当前为空。

## 当前结论

资源链已完成安全接入，静态资源与场景引用无断链；但 Godot 4.7.1 的无头资源扫描/编辑器退出挂起仍未解决，不能将 P1-T6 或 Web 构建标记为通过。建议后续在同一版本的 GUI 编辑器中执行一次全量导入并保存项目缓存，或使用经验证的 Godot 4.x 修订版本/干净用户数据目录后再重跑 Web 导出。
