from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-05-predominant-ii"
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
    draw.polygon([(x2, y2), (x2 - 28, y2 - 16), (x2 - 28, y2 + 16)], fill=color)


def save_piano_chart():
    img = Image.new("RGB", (1520, 980), "#f5efe5")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)

    draw.text((64, 40), "钢琴示意：二级和弦 ii 如何把音乐推向 V", fill="#2c241b", font=title)
    draw.text(
        (64, 108),
        "以 C 大调为例，ii 就是 Dm。它通常不会直接承担“结束”的职责，而是先制造向前的动力，再交给 G 或 G7 完成终止。",
        fill="#6d5f51",
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
        draw.text((x + 22, y0 + 278), name, fill="#5d6671", font=font(30, bold=True))

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 92
    black_h = 208
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 146, x + black_w, y0 + black_h), name, "#f9fafb", font(19, bold=True))

    def mark_white(note_idx: int, note: str, color: str, cy: int, label: str):
        cx = x0 + note_idx * white_w + white_w / 2
        draw.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=color, outline="#ffffff", width=4)
        center_text(draw, (cx - 36, cy - 40, cx + 36, cy - 6), note, "#ffffff", font(21, bold=True))
        center_text(draw, (cx - 36, cy - 2, cx + 36, cy + 24), label, "#ffffff", font(16, bold=True))

    for idx, note in [(1, "D"), (3, "F"), (5, "A")]:
        mark_white(idx, note, "#3d78c2", y0 + 132, "ii")
    for idx, note in [(1, "D"), (4, "G"), (6, "B")]:
        mark_white(idx, note, "#c48327", y0 + 216, "V")
    for idx, note in [(0, "C"), (2, "E"), (4, "G")]:
        mark_white(idx, note, "#2f8f5b", y0 + 292, "I")

    draw.rounded_rectangle((80, 596, 1450, 716), 24, fill="#fff9ef", outline="#d6c2a5", width=3)
    draw.text((112, 628), "蓝：ii = D-F-A    金：V = G-B-D    绿：I = C-E-G", fill="#4b5563", font=font(33, bold=True))

    draw.rounded_rectangle((1008, 166, 1446, 552), 26, fill="#fffaf4", outline="#d8cbbb", width=3)
    draw.text((1036, 198), "听感重点", fill="#2b241c", font=font(38, bold=True))
    draw.text((1036, 270), "1. ii 不稳定，但不急着回家", fill="#675a4b", font=body)
    draw.text((1036, 332), "2. 它先把重心抬向属区", fill="#675a4b", font=body)
    draw.text((1036, 394), "3. 再由 V 把张力交给 I", fill="#675a4b", font=body)
    draw.text((1036, 474), "它像“终止前的准备区”", fill="#8a5a2c", font=font(30, bold=True))

    draw.rounded_rectangle((84, 774, 1424, 902), 28, fill="#fffdf8", outline="#d9c8b2", width=3)
    draw.text(
        (116, 800),
        "钢琴练法：左手弹 D -> G -> C，右手弹 F-A-D -> G-B-D -> G-C-E。把 ii 听成“出发去终止”的一步，而不是停留点。",
        fill="#5a5045",
        font=body,
    )

    img.save(ASSET_DIR / "piano-predominant-ii.png")


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
        center_text(draw, (sx - 16, grid_top - 42, sx + 16, grid_top - 10), mark, "#51606b", font(16, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 255, sx + 12, grid_top + 288), name, "#51606b", font(16, bold=True))


def save_guitar_chart():
    img = Image.new("RGB", (1500, 980), "#edf3f6")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 42), "吉他示意：ii-V-I 是非常常见的推进骨架", fill="#17303a", font=title)
    draw.text(
        (68, 112),
        "在 C 大调里最基础的练法就是 Dm -> G -> C。对吉他来说，这个进行既适合扫弦，也适合分解和弦与指弹编配。",
        fill="#49626b",
        font=body,
    )

    draw.rounded_rectangle((94, 194, 1410, 320), 28, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((124, 230), "实用理解：ii 不是终点，它负责把耳朵先带离稳定区，再顺势推向 V，最后交给 I 落地。", fill="#17303a", font=font(31, bold=True))

    draw_chord_grid(
        draw,
        92,
        384,
        "Dm",
        "ii：前属准备",
        [(2, 2, "2", "#3d78c2"), (3, 1, "3", "#3d78c2"), (1, 5, "1", "#3d78c2")],
        {0: "X", 3: "O", 4: "O"},
    )
    draw_chord_grid(
        draw,
        548,
        384,
        "G",
        "V：属功能推进",
        [(2, 0, "2", "#c48327"), (3, 1, "3", "#c48327"), (3, 5, "4", "#c48327")],
        {2: "O", 3: "O", 4: "O"},
    )
    draw_chord_grid(
        draw,
        1004,
        384,
        "C",
        "I：稳定解决",
        [(3, 1, "3", "#2f8f5b"), (2, 3, "2", "#2f8f5b"), (1, 4, "1", "#2f8f5b")],
        {0: "X", 2: "O", 5: "O"},
    )

    draw.rounded_rectangle((92, 872, 1410, 936), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((118, 892), "吉他练法：循环 | Dm | G | C |，先均匀下扫，再改成 4 拍分解和弦，听 ii 如何把 V 的到来变得更自然。", fill="#4d5f68", font=font(28, bold=True))

    img.save(ASSET_DIR / "guitar-predominant-ii.png")


def save_structure_chart():
    img = Image.new("RGB", (1440, 900), "#f8f7f2")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 44), "结构图：ii 为什么叫前属功能", fill="#2c261f", font=title)
    draw.text((68, 114), "Predominant 的意思不是“比属更重要”，而是“在属之前出现、负责把音乐送往属和弦的区域”。", fill="#665d52", font=body)

    boxes = [
        (96, 214, 392, 642, "#edf4ff", "#3d78c2", "ii", ["D-F-A", "听感：离开稳定区", "任务：准备 V"]),
        (572, 214, 868, 642, "#fff7eb", "#c48327", "V", ["G-B-D", "听感：张力聚焦", "任务：推动解决"]),
        (1048, 214, 1344, 642, "#f1fbf4", "#2f8f5b", "I", ["C-E-G", "听感：回到稳定", "任务：完成解决"]),
    ]

    for left, top, right, bottom, fill, outline, head, lines in boxes:
        draw.rounded_rectangle((left, top, right, bottom), 30, fill=fill, outline=outline, width=4)
        draw.text((left + 112, top + 40), head, fill=outline, font=font(42, bold=True))
        draw.text((left + 44, top + 136), lines[0], fill="#5a5146", font=body)
        draw.text((left + 44, top + 228), lines[1], fill="#5a5146", font=font(26, bold=True))
        draw.text((left + 44, top + 320), lines[2], fill="#8b5a28", font=font(25, bold=True))

    draw_arrow(draw, 392, 428, 572, 428, "#9b8a74")
    draw_arrow(draw, 868, 428, 1048, 428, "#9b8a74")

    draw.rounded_rectangle((122, 716, 1318, 816), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((146, 746), "一句话：ii 的作用是先把音乐推出主和弦的稳定区，再把方向交给 V，最后让 I 真正落地。", fill="#6a5644", font=font(31, bold=True))

    img.save(ASSET_DIR / "predominant-ii-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
