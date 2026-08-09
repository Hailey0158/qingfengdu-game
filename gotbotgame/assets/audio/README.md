# 清风渡音频小样

当前目录包含 P0-T4「雨夜引子」方向验证小样：

- `bgm/bgm_rain_intro_sample.wav`：箫 + 古琴程序化验证母带，120 秒，48 kHz / 24-bit / 立体声。
- `bgm/bgm_rain_intro_sample.ogg`：Godot 接入版 Vorbis，120 秒，48 kHz / 立体声，约 395 KB。
- `ambient/sfx_rain_continuous_sample.wav`：独立连续雨声母带，120 秒，48 kHz / 24-bit / 立体声。
- `ambient/sfx_rain_continuous_sample.ogg`：Godot 接入版 Vorbis，120 秒，48 kHz / 立体声，约 1.4 MB。
- `bgm/rain-night-intro-loop-notes.txt`：循环区间、淡入淡出和 Godot 总线接入标记。

这组文件是方向验证小样，不是最终作曲成品。P0 原型已在用户首次点击任一验证选项时，于同一用户手势中启动两条音轨：箫/古琴 OGG 接入 `BGM`，独立雨声 OGG 接入 `Ambient`。两条 OGG 均设置为循环播放，避免 Web 首次播放后静音或播放结束。

```text
res://assets/audio/bgm/bgm_rain_intro_sample.ogg
res://assets/audio/ambient/sfx_rain_continuous_sample.ogg
```

如果浏览器此前打开过旧构建，请使用强制刷新（`Ctrl + F5`）；Web 浏览器通常禁止页面在无用户操作时自动播放声音，因此必须先点击一个选项。
