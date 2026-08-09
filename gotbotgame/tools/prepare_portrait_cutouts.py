from pathlib import Path
import struct
import zlib
from collections import deque

OUT_W, OUT_H = 1600, 2000
ROOT = Path(r"C:/Users/gh604/WorkBuddy/game-02/gotbotgame")
SOURCES = {
    "gui_han_calm_godot.png": Path(r"C:/Users/gh604/Downloads/剑修立绘生成.png"),
    "li_keying_calm_godot.png": Path(r"C:/Users/gh604/Downloads/剑修立绘生成 (3).png"),
}
OUT_DIR = ROOT / "assets" / "generated_portraits"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def read_png(path: Path):
    blob = path.read_bytes()
    assert blob[:8] == b"\x89PNG\r\n\x1a\n", "Only PNG is supported"
    chunks = []
    pos = 8
    while pos < len(blob):
        length = struct.unpack(">I", blob[pos:pos + 4])[0]
        kind = blob[pos + 4:pos + 8]
        data = blob[pos + 8:pos + 8 + length]
        pos += 12 + length
        chunks.append((kind, data))
    hdr = next(data for kind, data in chunks if kind == b"IHDR")
    width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", hdr)
    assert bit_depth == 8 and color_type == 2 and compression == 0 and filtering == 0 and interlace == 0, "Expected RGB non-interlaced PNG"
    packed = zlib.decompress(b"".join(data for kind, data in chunks if kind == b"IDAT"))
    stride = width * 3
    rows = []
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        filter_type = packed[offset]
        scan = bytearray(packed[offset + 1:offset + 1 + stride])
        offset += stride + 1
        for i in range(stride):
            left = scan[i - 3] if i >= 3 else 0
            above = previous[i]
            upper_left = previous[i - 3] if i >= 3 else 0
            if filter_type == 1:
                scan[i] = (scan[i] + left) & 255
            elif filter_type == 2:
                scan[i] = (scan[i] + above) & 255
            elif filter_type == 3:
                scan[i] = (scan[i] + ((left + above) // 2)) & 255
            elif filter_type == 4:
                p = left + above - upper_left
                pa, pb, pc = abs(p - left), abs(p - above), abs(p - upper_left)
                scan[i] = (scan[i] + (left if pa <= pb and pa <= pc else above if pb <= pc else upper_left)) & 255
            elif filter_type != 0:
                raise ValueError("Unsupported PNG filter")
        rows.append(scan)
        previous = scan
    return width, height, rows


def is_white_background(row: bytearray, x: int) -> bool:
    r, g, b = row[x * 3:x * 3 + 3]
    return r >= 242 and g >= 242 and b >= 242 and max(r, g, b) - min(r, g, b) <= 14


def cutout(src: Path, dest: Path):
    width, height, rows = read_png(src)
    bg = bytearray(width * height)
    queue = deque()
    def add(x, y):
        idx = y * width + x
        if not bg[idx] and is_white_background(rows[y], x):
            bg[idx] = 1
            queue.append((x, y))
    for x in range(width):
        add(x, 0); add(x, height - 1)
    for y in range(height):
        add(0, y); add(width - 1, y)
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                add(nx, ny)
    # Preserve a 30px visual boundary, then scale source uniformly onto standard Godot canvas.
    scale = min((OUT_W - 100) / width, (OUT_H - 100) / height)
    draw_w, draw_h = max(1, round(width * scale)), max(1, round(height * scale))
    left, top = (OUT_W - draw_w) // 2, (OUT_H - draw_h) // 2
    target = [bytearray(OUT_W * 4) for _ in range(OUT_H)]
    for ty in range(draw_h):
        sy = min(height - 1, int(ty / scale))
        for tx in range(draw_w):
            sx = min(width - 1, int(tx / scale))
            sr, sg, sb = rows[sy][sx * 3:sx * 3 + 3]
            idx = sy * width + sx
            # Feather the border-connected near-white background only; preserve white garments inside the silhouette.
            alpha = 0 if bg[idx] else 255
            out = (left + tx) * 4
            target[top + ty][out:out + 4] = bytes((sr, sg, sb, alpha))
    raw = b"".join(b"\x00" + bytes(row) for row in target)
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", OUT_W, OUT_H, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    dest.write_bytes(png)
    return width, height, dest.stat().st_size


for name, source in SOURCES.items():
    print(name, cutout(source, OUT_DIR / name))
