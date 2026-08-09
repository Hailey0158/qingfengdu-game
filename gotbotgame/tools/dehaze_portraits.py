from PIL import Image
from pathlib import Path
import numpy as np

mvp_dir = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame/assets/sprites/mvp")
output_dir = mvp_dir / "dehazed"
output_dir.mkdir(exist_ok=True)

targets = [
    "gui_han_calm_transparent.png",
    "li_keying_calm_transparent.png",
    "liu_lushu_calm_transparent.png",
    "innkeeper_calm_v2.png",
]

for name in targets:
    src = mvp_dir / name
    if not src.exists():
        print(f"SKIP {name}")
        continue
    im = Image.open(src).convert("RGBA")
    arr = np.array(im).astype(np.float32)

    alpha = arr[:, :, 3]
    red = arr[:, :, 0]
    green = arr[:, :, 1]
    blue = arr[:, :, 2]

    # Premultiply: for any pixel with alpha < 255, scale RGB by alpha/255
    # This eliminates the white fringe because semi-transparent white pixels
    # become dark semi-transparent pixels that blend naturally with the background
    alpha_norm = alpha / 255.0
    arr[:, :, 0] = red * alpha_norm
    arr[:, :, 1] = green * alpha_norm
    arr[:, :, 2] = blue * alpha_norm

    # Then threshold: any pixel with alpha < 30 becomes fully transparent
    arr[alpha < 30, 3] = 0
    arr[alpha < 30, 0] = 0
    arr[alpha < 30, 1] = 0
    arr[alpha < 30, 2] = 0

    result = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
    dst = output_dir / name
    result.save(dst, "PNG", optimize=True)

    # Verify - check if bright semi-transparent pixels are gone
    arr2 = np.array(result).astype(np.int32)
    a2 = arr2[:, :, 3]
    min_rgb2 = np.minimum(np.minimum(arr2[:,:,0], arr2[:,:,1]), arr2[:,:,2])
    semi = ((a2 > 10) & (a2 < 250)).sum()
    bright_halo = ((a2 > 10) & (a2 < 250) & (min_rgb2 > 180)).sum()
    print(f"DONE {name}: semi={int(semi)} bright_halo={int(bright_halo)} ({round(bright_halo/max(semi,1)*100,1)}%)")
