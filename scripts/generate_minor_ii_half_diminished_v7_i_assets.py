from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-08-minor-ii-half-diminished-v7-i"
ASSET_DIR.mkdir(parents=True, exist_ok=True)

FONT_CJK = "/System/Library/Fonts/PingFang.ttc"
FONT_UI = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Hiragino Sans GB.ttc" if bold else FONT_CJK,
        FONT_UI,
        "/System/Library/Fonts/STHeiti Medium.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def center_text(draw: ImageDraw.ImageDraw, box, text, fill, text_font):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=text_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = left + (right - left - tw) / 2
    y = top + (bottom - top - th) / 2 - 2
    draw.text((x, y), text, fill=fill, font=text_font)


def draw_arrow(draw, x1, y1, x2, y2, color):
    draw.line((x1, y1, x2, y2), fill=color, width=8)
    draw.polygon([(x2, y2), (x2 - 24, y2 - 14), (x2 - 24, y2 + 14)], fill=color)


def mark_white(draw, x0, y0, white_w, note_idx: int, note: str, color: str, cy: int, label: str):
    cx = x0 + note_idx * white_w + white_w / 2
    draw.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=color, outline="#ffffff", width=4)
    center_text(draw, (cx - 34, cy - 38, cx + 34, cy - 8), note, "#ffffff", font(20, bold=True))
    center_text(draw, (cx - 34, cy - 2, cx + 34, cy + 22), label, "#ffffff", font(13, bold=True))


def mark_black(draw, x, y, note: str, color: str, label: str):
    draw.ellipse((x - 30, y - 30, x + 30, y + 30), fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 30, y - 32, x + 30, y - 6), note, "#ffffff", font(16, bold=True))
    center_text(draw, (x - 32, y, x + 32, y + 20), label, "#ffffff", font(12, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1520, 980), "#f4f0e8")
    draw = ImageDraw.Draw(img)
    title = font(52, bold=True)
    body = font(28)

    draw.text((64, 42), "钢琴示意：小调里的 ii半减七 - V7 - i", fill="#2c241b", font=title)
    draw.text(
        (64, 108),
        "以 A 小调为例，Bm7b5 -> E7 -> Am。和昨天的大调 ii-V-I 相比，ii 变成半减七，V 常加入导音 G#，色彩更紧张。",
        fill="#6f6154",
        font=body,
    )

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 155
    white_h = 330
    x0 = 76
    y0 = 236

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 22, y0 + 278), name, fill="#59636d", font=font(30, bold=True))

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 92
    black_h = 208
    black_centers = {}
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        black_centers[name] = x + black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 146, x + black_w, y0 + black_h), name, "#f9fafb", font(19, bold=True))

    for idx, note in [(6, "B"), (1, "D"), (3, "F"), (5, "A")]:
        mark_white(draw, x0, y0, white_w, idx, note, "#4a79bf", y0 + 110, "iio7")
    mark_black(draw, black_centers["G#/Ab"], y0 + 112, "G#", "#c07a28", "V7")
    for idx, note in [(2, "E"), (4, "G"), (6, "B"), (1, "D")]:
        mark_white(draw, x0, y0, white_w, idx, note, "#c07a28", y0 + 202, "V7")
    for idx, note in [(5, "A"), (0, "C"), (2, "E")]:
        mark_white(draw, x0, y0, white_w, idx, note, "#2f8a5c", y0 + 292, "i")

    draw.rounded_rectangle((78, 594, 1450, 720), 24, fill="#fff9ef", outline="#d6c4ae", width=3)
    draw.text(
        (104, 626),
        "蓝：Bm7b5 = B-D-F-A    金：E7 = E-G#-B-D    绿：Am = A-C-E",
        fill="#4a5563",
        font=font(33, bold=True),
    )

    draw.rounded_rectangle((1000, 164, 1448, 556), 26, fill="#fffaf4", outline="#d8cbbb", width=3)
    draw.text((1028, 198), "钢琴听点", fill="#2b241c", font=font(38, bold=True))
    draw.text((1028, 268), "1. 低音 B -> E -> A", fill="#675a4b", font=body)
    draw.text((1028, 330), "2. D 可保留到 E7", fill="#675a4b", font=body)
    draw.text((1028, 392), "3. G# 强烈想去 A", fill="#675a4b", font=body)
    draw.text((1028, 472), "这就是小调里更尖锐的解决感", fill="#8a5a2c", font=font(28, bold=True))

    draw.rounded_rectangle((84, 778, 1434, 906), 28, fill="#fffdf8", outline="#d9c8b2", width=3)
    draw.text(
        (114, 804),
        "练法：左手弹 B -> E -> A，右手弹 A-B-D-F -> G#-B-D-E -> A-C-E，重点去听 G# 最后如何被 A 吸住。",
        fill="#5a5045",
        font=body,
    )

    img.save(ASSET_DIR / "piano-minor-ii-v-i.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, base_fret="1fr"):
    grid_left = x + 64
    grid_top = y + 112
    fret_gap = 58
    string_gap = 44

    draw.rounded_rectangle((x, y, x + 386, y + 466), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#1d3136", font=font(34, bold=True))
    draw.text((x + 28, y + 68), subtitle, fill="#60717a", font=font(21))
    draw.text((x + 290, y + 102), base_fret, fill="#60717a", font=font(18, bold=True))

    for i in range(6):
        sx = grid_left + i * string_gap
        draw.line((sx, grid_top, sx, grid_top + 4 * fret_gap), fill="#2d3748", width=4)
    for i in range(5):
        sy = grid_top + i * fret_gap
        draw.line((grid_left, sy, grid_left + 5 * string_gap, sy), fill="#2d3748", width=8 if i == 0 else 4)

    for fret, string_idx, label, color in dots:
        cx = grid_left + string_idx * string_gap
        cy = grid_top + (fret - 0.5) * fret_gap
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#ffffff", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 42, sx + 18, grid_top - 10), mark, "#51606b", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 255, sx + 12, grid_top + 288), name, "#51606b", font(16, bold=True))


def save_guitar_chart():
    img = Image.new("RGB", (1500, 980), "#eef3f5")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 42), "吉他示意：Bm7b5 - E7 - Am", fill="#17303a", font=title)
    draw.text(
        (68, 112),
        "在 A 小调里，这三个和弦是最常见的小调句尾之一。Bm7b5 先铺出阴影，E7 用 G# 强化导向，Am 负责真正落地。",
        fill="#49626b",
        font=body,
    )

    draw.rounded_rectangle((94, 194, 1410, 320), 28, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((120, 230), "核心听感：Bm7b5 不稳定但不终结，E7 把张力拉到最高，Am 把它收回到小调主和弦。", fill="#17303a", font=font(31, bold=True))

    draw_chord_grid(
        draw,
        92,
        384,
        "Bm7b5",
        "ii半减七：前属",
        [(2, 0, "2", "#4a79bf"), (1, 1, "1", "#4a79bf"), (2, 2, "3", "#4a79bf"), (2, 4, "4", "#4a79bf")],
        {3: "O", 5: "X"},
    )
    draw_chord_grid(
        draw,
        548,
        384,
        "E7",
        "V7：导向最强",
        [(2, 0, "2", "#c07a28"), (2, 1, "3", "#c07a28"), (1, 3, "1", "#c07a28")],
        {2: "O", 4: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        1004,
        384,
        "Am",
        "i：小调落点",
        [(2, 1, "2", "#2f8a5c"), (2, 2, "3", "#2f8a5c"), (1, 3, "1", "#2f8a5c")],
        {0: "X", 4: "O", 5: "O"},
    )

    draw.rounded_rectangle((92, 872, 1410, 936), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((112, 892), "练法：循环 | Bm7b5 | E7 | Am |，先每小节四拍扫弦，再改成分解和弦，盯住 E7 到 Am 的收束。", fill="#4d5f68", font=font(28, bold=True))

    img.save(ASSET_DIR / "guitar-minor-ii-v-i.png")


def save_flow_chart():
    img = Image.new("RGB", (1440, 900), "#f7f5ef")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)

    draw.text((68, 42), "结构图：小调 ii半减七 - V7 - i 的功能路线", fill="#2c261f", font=title)
    draw.text((68, 110), "它沿用 ii-V-I 的语法，但因为出现半减七和升高导音，整体颜色更暗，解决也更明显。", fill="#665d52", font=body)

    boxes = [
        (92, 224, 430, 660, "#edf4ff", "#4a79bf", "ii半减七", ["Bm7b5", "B-D-F-A", "前属：先制造不稳", "F 到 E，A 可保留到 Am"]),
        (550, 224, 888, 660, "#fff7eb", "#c07a28", "V7", ["E7", "E-G#-B-D", "属：G# 强烈想去 A", "是小调句尾的推进核心"]),
        (1008, 224, 1346, 660, "#f1fbf4", "#2f8a5c", "i", ["Am", "A-C-E", "主：把张力收回", "结束感来自导音解决"]),
    ]

    for left, top, right, bottom, fill, outline, head, lines in boxes:
        draw.rounded_rectangle((left, top, right, bottom), 30, fill=fill, outline=outline, width=4)
        draw.text((left + 76, top + 36), head, fill=outline, font=font(40, bold=True))
        draw.text((left + 40, top + 126), lines[0], fill="#5a5146", font=body)
        draw.text((left + 40, top + 194), lines[1], fill="#5a5146", font=font(24, bold=True))
        draw.text((left + 40, top + 286), lines[2], fill="#5a5146", font=font(25, bold=True))
        draw.text((left + 40, top + 380), lines[3], fill="#8b5a28", font=font(24, bold=True))

    draw_arrow(draw, 430, 442, 550, 442, "#9b8a74")
    draw_arrow(draw, 888, 442, 1008, 442, "#9b8a74")

    draw.rounded_rectangle((156, 716, 1286, 814), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((184, 746), "一句话：小调版本之所以更有戏剧性，是因为半减七的不稳加上导音 G# 的强烈吸引，让 V7 到 i 的回归更深。", fill="#6a5644", font=font(27, bold=True))

    img.save(ASSET_DIR / "minor-ii-v-i-flow.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_flow_chart()
