from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame")
OUT_DIR = ROOT / "assets/sprites/mvp"
CANVAS = (1600, 2000)
TARGET_MAX = (1450, 1880)
BOTTOM_MARGIN = 45

PORTRAITS = {
    "gui_han_calm_transparent.png": ROOT / "assets/generated_portraits/workbuddy-generated-eRNYZ3bk8s88MqYfPsW-EpOl7Gu9qSdjKYWxB_OpYIw.png",
    "li_keying_calm_transparent.png": ROOT / "assets/generated_portraits/workbuddy-generated-HRlVaCuaypgoMDIrkpDNrAYon9Nq_ID0B-PKqkpuDSA.png",
    "liu_lushu_calm_transparent.png": ROOT / "assets/generated_portraits/workbuddy-generated-ZSIIwtV3s9sdbW1R7uZj4BaYj1Bgich6WssCzMSNAO8.png",
}


def is_baked_checker(pixel: tuple[int, int, int]) -> bool:
    r, g, b = pixel
    return min(r, g, b) >= 230 and max(r, g, b) - min(r, g, b) <= 14


def connected_background_mask(rgb: Image.Image) -> Image.Image:
    width, height = rgb.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def add(x: int, y: int) -> None:
        index = y * width + x
        if visited[index] == 0 and is_baked_checker(pixels[x, y]):
            visited[index] = 1
            queue.append((x, y))

    for x in range(width):
        add(x, 0)
        add(x, height - 1)
    for y in range(height):
        add(0, y)
        add(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x > 0:
            add(x - 1, y)
        if x + 1 < width:
            add(x + 1, y)
        if y > 0:
            add(x, y - 1)
        if y + 1 < height:
            add(x, y + 1)

    alpha = Image.new("L", (width, height), 255)
    alpha_pixels = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if visited[row + x]:
                alpha_pixels[x, y] = 0

    # Slight inward feather removes checker fringe without erasing pale clothing interiors.
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.45))
    return alpha


def export_portrait(source_path: Path, output_path: Path) -> None:
    source = Image.open(source_path).convert("RGB")
    alpha = connected_background_mask(source)
    rgba = source.convert("RGBA")
    rgba.putalpha(alpha)

    bounds = alpha.getbbox()
    if bounds is None:
        raise RuntimeError(f"No foreground detected: {source_path}")

    left, top, right, bottom = bounds
    visible_w = right - left
    visible_h = bottom - top
    pad_x = max(20, round(visible_w * 0.035))
    pad_y = max(20, round(visible_h * 0.025))
    crop_box = (
        max(0, left - pad_x),
        max(0, top - pad_y),
        min(rgba.width, right + pad_x),
        min(rgba.height, bottom + pad_y),
    )
    cutout = rgba.crop(crop_box)

    scale = min(TARGET_MAX[0] / cutout.width, TARGET_MAX[1] / cutout.height)
    resized_size = (
        max(1, round(cutout.width * scale)),
        max(1, round(cutout.height * scale)),
    )
    resized = cutout.resize(resized_size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    x = (CANVAS[0] - resized.width) // 2
    y = CANVAS[1] - BOTTOM_MARGIN - resized.height
    canvas.alpha_composite(resized, (x, y))
    canvas.save(output_path, "PNG", optimize=True)

    result_alpha = canvas.getchannel("A")
    print(
        f"{output_path.name}: size={canvas.size}, mode={canvas.mode}, "
        f"alpha={result_alpha.getextrema()}, bounds={result_alpha.getbbox()}, bytes={output_path.stat().st_size}"
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for output_name, source_path in PORTRAITS.items():
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        export_portrait(source_path, OUT_DIR / output_name)


if __name__ == "__main__":
    main()
