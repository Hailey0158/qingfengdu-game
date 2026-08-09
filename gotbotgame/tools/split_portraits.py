from pathlib import Path
from PIL import Image, ImageChops, ImageFilter

ROOT = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame")
SOURCE = ROOT / "assets/generated_portraits/workbuddy-generated-HRlVaCuaypgoMDIrkpDNrAYon9Nq_ID0B-PKqkpuDSA.png"
OUT_DIR = ROOT / "assets/sprites"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# The source sheet is two side-by-side character panels. Keep the original source intact.
source = Image.open(SOURCE).convert("RGBA")
w, h = source.size


def make_alpha(image: Image.Image) -> Image.Image:
    """Convert only near-white backing into transparency with a feathered edge."""
    rgb = image.convert("RGB")
    alpha = Image.new("L", image.size)
    src = rgb.load()
    out = alpha.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = src[x, y]
            # Squared distance to a pure white backing. A soft ramp preserves pale fabric.
            distance = ((255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2) ** 0.5
            if distance <= 14:
                out[x, y] = 0
            elif distance >= 60:
                out[x, y] = 255
            else:
                out[x, y] = int((distance - 14) * 255 / 46)
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=0.35))
    image.putalpha(alpha)
    return image


def export_panel(name: str, left: int, right: int) -> None:
    # Include a small seam overlap so no hair/weapon detail is clipped.
    panel = source.crop((left, 0, right, h))
    panel = make_alpha(panel)
    bbox = panel.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError(f"No visible pixels detected for {name}")
    # Preserve a 7% artistic breathing margin around the visible character.
    bx0, by0, bx1, by1 = bbox
    pad_x = max(16, int((bx1 - bx0) * 0.07))
    pad_y = max(16, int((by1 - by0) * 0.07))
    bx0 = max(0, bx0 - pad_x); by0 = max(0, by0 - pad_y)
    bx1 = min(panel.width, bx1 + pad_x); by1 = min(panel.height, by1 + pad_y)
    cutout = panel.crop((bx0, by0, bx1, by1))

    # Fit inside Godot's portrait canvas while retaining aspect ratio and alpha.
    canvas = Image.new("RGBA", (1600, 2000), (0, 0, 0, 0))
    scale = min(1360 / cutout.width, 1880 / cutout.height)
    resized = cutout.resize((max(1, round(cutout.width * scale)), max(1, round(cutout.height * scale))), Image.Resampling.LANCZOS)
    x = (1600 - resized.width) // 2
    y = 2000 - resized.height - 50
    canvas.alpha_composite(resized, (x, y))
    path = OUT_DIR / name
    canvas.save(path, "PNG", optimize=True)
    visible = canvas.getchannel("A").getbbox()
    print(f"{path.name}: {canvas.size}, RGBA, alpha_bbox={visible}")


# Generated sheet composition: Gui Han on left, Li Keying on right.
mid = w // 2
export_panel("gui_han_calm.png", 0, mid + 18)
export_panel("li_keying_calm.png", mid - 18, w)
