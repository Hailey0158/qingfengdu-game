# 中文字体接入说明（P0/P1）

当前工程统一使用 `NotoSansCJKsc-Regular.otf`，用于 1280×720、RichTextLabel、Button 与动态生成的中文选项。该字体随 Web 导出打包，采用 SIL Open Font License 1.1；许可证来源记录在 `OFL-Noto-CJK.txt`。

`scenes/main.tscn` 的根节点启动脚本 `init_font.gd` 会在运行时加载该字体，并递归为所有 Control 节点设置 `font`、`normal_font` 与 `bold_font` 覆盖；同时监听 `node_added`，确保点击选项后动态创建的 Button 也不会回退到浏览器系统字体。

`choice_panel.gd` 在生成选项按钮时会再次显式绑定同一字体，作为 Web 端的第二层保障。选项引导符使用 ASCII `>`，避免把装饰符号当成必需字形。

已用 fontTools 按 Unicode 码位验证：当前 GDScript、TSCN 与 JSON 中 585 个非 ASCII 字符在字体中 0 缺字，包含“清风渡”、三位角色名、中文标点、箭头和原三角引导符。后续新增对白或 UI 文案时，仍需重新执行字形覆盖检查。
