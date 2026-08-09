from collections import deque
from pathlib import Path
from PIL import Image, ImageFilter

src_path = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame/assets/generated_portraits/Character_portrait__single_per_2026-08-07T17-15-45.png")
dst_path = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame/assets/sprites/mvp/innkeeper_calm_v2.png")
CAN = (1600, 2000)
TARGET_MAX = (1450, 1880)
BOTTOM_MARGIN = 45

def is_bg(pixel):
    r, g, b = pixel
    return min(r, g, b) >= 190 and max(r, g, b) - min(r, g, b) <= 18

def connected_bg_mask(rgb):
    width, height = rgb.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    queue = deque()
    def add(x, y):
        idx = y * width + x
        if visited[idx] == 0 and is_bg(pixels[x, y]):
            visited[idx] = 1
            queue.append((x, y))
    for x in range(width):
        add(x, 0)
        add(x, height - 1)
    for y in range(height):
        add(0, y)
        add(width - 1, y)
    while queue:
        x, y = queue.popleft()
        if x > 0: add(x - 1, y)
        if x + 1 < width: add(x + 1, y)
        if y > 0: add(x, y - 1)
        if y + 1 < height: add(x, y + 1)
    alpha = Image.new("L", (width, height), 255)
    ap = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if visited[row + x]:
                ap[x, y] = 0
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.6))
    return alpha

src = Image.open(src_path).convert("RGB")
alpha = connected_bg_mask(src)
rgba = src.convert("RGBA")
rgba.putalpha(alpha)
bbox = alpha.getbbox()
if bbox is None:
    raise RuntimeError("No foreground detected")
left, top, right, bottom = bbox
vw = right - left
vh = bottom - top
pad_x = max(20, round(vw * 0.035))
pad_y = max(20, round(vh * 0.025))
crop_box = (max(0, left - pad_x), max(0, top - pad_y), min(rgba.width, right + pad_x), min(rgba.height, bottom + pad_y))
cutout = rgba.crop(crop_box)
scale = min(TARGET_MAX[0] / cutout.width, TARGET_MAX[1] / cutout.height)
resized_size = (max(1, round(cutout.width * scale)), max(1, round(cutout.height * scale)))
resized = cutout.resize(resized_size, Image.Resampling.LANCZOS)
canvas = Image.new("RGBA", CAN, (0, 0, 0, 0))
x = (CAN[0] - resized.width) // 2
y = CAN[1] - BOTTOM_MARGIN - resized.height
canvas.alpha_composite(resized, (x, y))
dst_path.parent.mkdir(parents=True, exist_ok=True)
canvas.save(dst_path, "PNG", optimize=True)
ra = canvas.getchannel("A")
hist = ra.histogram()
total = CAN[0] * CAN[1]
transp = hist[0]
print("saved", dst_path.name, "size=", canvas.size, "mode=", canvas.mode, "alpha=", ra.getextrema(), "bounds=", ra.getbbox(), "bytes=", dst_path.stat().st_size)
print("transparent_pct=", round(transp / total * 100, 2), "opaque_pct=", round(hist[255] / total * 100, 2))
print("corners=", [ra.getpixel(xy) for xy in [(0, 0), (1599, 0), (0, 1999), (1599, 1999)]])
