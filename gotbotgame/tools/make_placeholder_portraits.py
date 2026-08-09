from pathlib import Path
import struct, zlib
root = Path(r'C:/Users/gh604/WorkBuddy/game-02/gotbotgame/assets/placeholder_sprites')
root.mkdir(parents=True, exist_ok=True)
W, H = 1600, 2000

def png_rgba(path, pixels):
    raw = b''.join(b'\x00' + bytes(row) for row in pixels)
    def chunk(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    data = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')
    path.write_bytes(data)

def rect(row, x0, x1, color):
    x0, x1 = max(0, int(x0)), min(W, int(x1))
    for x in range(x0, x1):
        row[x * 4:x * 4 + 4] = bytes(color)

def ellipse(rows, cx, cy, rx, ry, color):
    for y in range(max(0, int(cy - ry)), min(H, int(cy + ry + 1))):
        q = 1 - ((y - cy) / ry) ** 2
        if q > 0:
            dx = rx * (q ** 0.5)
            rect(rows[y], cx - dx, cx + dx, color)

def portrait(kind):
    rows = [bytearray(W * 4) for _ in range(H)]
    if kind == 'gui':
        skin=(220,218,210,245); hair=(205,214,218,245); robe=(232,235,233,235); shadow=(154,173,182,185); blue=(104,158,186,245); ink=(44,56,62,230)
        ellipse(rows, 800, 470, 245, 310, hair); ellipse(rows, 800, 545, 170, 190, skin)
        ellipse(rows, 580, 860, 120, 520, hair); ellipse(rows, 1020, 860, 120, 520, hair)
        ellipse(rows, 800, 1420, 520, 650, robe); ellipse(rows, 800, 1180, 390, 390, shadow)
        rect(rows[1200], 620, 980, blue); rect(rows[1360], 450, 1150, ink)
        ellipse(rows, 750, 535, 24, 12, ink); ellipse(rows, 850, 535, 24, 12, ink)
        rect(rows[1050], 1090, 1125, (220,225,225,230)); rect(rows[1100], 1110, 1135, (93,152,185,240)); ellipse(rows, 1120, 1090, 35, 50, blue)
    else:
        skin=(202,185,174,245); hair=(74,34,35,250); robe=(28,31,36,245); red=(133,46,48,245); steel=(115,122,126,235)
        ellipse(rows, 820, 470, 250, 350, hair); ellipse(rows, 1080, 520, 150, 520, hair); ellipse(rows, 800, 570, 165, 185, skin)
        ellipse(rows, 800, 1400, 540, 650, robe); rect(rows[1180], 520, 1080, red); rect(rows[1280], 690, 920, (50,54,58,230))
        ellipse(rows, 748, 555, 24, 12, (35,26,27,235)); ellipse(rows, 852, 555, 24, 12, (35,26,27,235))
        ellipse(rows, 930, 1180, 230, 100, (45,48,51,235)); rect(rows[1500], 1030, 1250, steel); rect(rows[1350], 1210, 1300, red); ellipse(rows, 1280, 1380, 55, 40, red)
    for y in range(1710, 1900, 18):
        alpha = max(0, 90 - abs(y - 1800) // 3)
        rect(rows[y], 420 + (y % 50), 1180 - (y % 70), (60,70,70,alpha))
    return rows

png_rgba(root / 'gui_han_placeholder.png', portrait('gui'))
png_rgba(root / 'li_keying_placeholder.png', portrait('li'))
print('created')
