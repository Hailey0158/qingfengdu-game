# P1 MVP 占位资产

本目录资产仅服务 P1 MVP 的雨夜开场、清风渡大堂与柳陆书第一天阅读链路，采用 PNG 以确保 Godot 4.7.1 Web 导出可直接加载并保留后续替换空间。

- `liu_lushu_reference_placeholder.jpg`：用户提供的柳陆书立绘参考图，作为 P1 MVP 的实际立绘占位；采用黑发高髻、青灰长衫、墨竹折扇、含笑试探的视觉锚点。
- `li_keying_placeholder.png`：黎客颍占位立绘，红发高马尾、黑衣、暗红束带与长刀，保留透明背景接口。
- `gui_han_placeholder.png`：归汉占位立绘，银白长发、白袍、淡蓝剑穗与长剑，保留透明背景接口。
- `bg_rain_night.png`：雨夜山道与清风渡灯笼。
- `bg_inn_hall.png`：客栈大堂。
- `bg_inn_window.png`：窗边饮茶场景。

这些不是 P3 正式美术。P3 替换时需保持 TextureRect 路径接口、透明背景立绘、16:9 背景比例，以及 PRD/PDD 的半厚涂、水墨晕染、青黑白主色方向。

## 2026-08-07 拆分参考立绘

以下 Godot 可用的拆分立绘存放在 `res://assets/sprites/`，原始双人参考图保留在 `res://assets/generated_portraits/`：

- `gui_han_calm.png`：归汉平静单表情，1600×2000 RGBA PNG，已验证透明通道。
- `li_keying_calm.png`：黎客颖平静单表情，1600×2000 RGBA PNG，已验证透明通道。

两张资源由双人参考图以保守的近白背景 Alpha 蒙版拆分生成，保留低饱和冷调、水墨半厚涂方向。它们当前是美术参考资产，尚未绑定 P1 运行时节点；P1-T6 仍须通过独立的 Godot 扫描/图形化编辑器验证后才能解除阻塞。
