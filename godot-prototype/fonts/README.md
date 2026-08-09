# 中文字体接入说明（P0）

本原型已按 1280×720 与 RichTextLabel 中文文本验证路径搭建，但仓库不内置未获授权的字体文件。

在执行 Godot 编辑器与 Web 实机验收前，必须放入一份可再分发的中文 OTF/TTF，例如 `SourceHanSerifSC-Regular.otf`，并在 Project Settings → GUI → Theme 中设为默认字体或为各 UI 节点设置 Theme Override。Web 导出必须打包该字体，不能依赖开发机的系统字体。

推荐：思源宋体 / Noto Serif CJK SC。