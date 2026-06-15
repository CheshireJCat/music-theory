from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-14-diminished-seventh"
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


def save_piano_chart():
    img = Image.new("RGB", (1500, 960), "#f5f1e8")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "钢琴图：G#dim7 如何强烈推向 Am", fill="#2d241c", font=font(54, bold=True))
    draw.text(
        (56, 106),
        "G#-B-D-F 是 A 小调里的导七减七和弦。它由连续小三度叠成，张力很满，最常见的任务就是把耳朵推回 Am。",
        fill="#6a5a4d",
        font=font(28),
    )

    white_w = 122
    white_h = 316
    x0 = 76
    y0 = 224
    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    centers = {}
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#273341", width=3)
        draw.text((x + 18, y0 + 264), name, fill="#596472", font=font(28, bold=True))
        centers[f"{name}{i}"] = x + white_w / 2

    black_w = 72
    black_h = 190
    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#", "D#", "F#", "G#", "A#"]
    black_centers = {}
    for pos, name in zip(black_positions, black_names):
        x = x0 + white_w * (pos + 1) - black_w / 2
        black_centers[name] = x + black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#131a22")
        center_text(draw, (x, y0 + 136, x + black_w, y0 + black_h), name, "#f8fafc", font(20, bold=True))

    note_positions = [
        (black_centers["G#"], y0 + 104, "#bd7a2f", "G#", "导音"),
        (centers["B6"], y0 + 246, "#2f8b61", "B", "小三度"),
        (centers["D1"], y0 + 246, "#5f7fb8", "D", "减五度"),
        (centers["F3"], y0 + 246, "#c65b4b", "F", "减七度"),
    ]
    for cx, cy, color, note, label in note_positions:
        draw.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 30, cy - 26, cx + 30, cy + 18), note, "#ffffff", font(24, bold=True))
        draw.text((cx - 42, cy + 42), label, fill=color, font=font(21, bold=True))

    a_cx = centers["A5"]
    a_cy = y0 + 246
    draw.ellipse((a_cx - 34, a_cy - 34, a_cx + 34, a_cy + 34), fill="#8a5cf6", outline="#ffffff", width=3)
    center_text(draw, (a_cx - 30, a_cy - 26, a_cx + 30, a_cy + 18), "A", "#ffffff", font(24, bold=True))
    draw.text((a_cx - 34, a_cy + 42), "解决", fill="#8a5cf6", font=font(21, bold=True))

    draw.line((black_centers["G#"] + 40, y0 + 132, a_cx - 40, y0 + 258), fill="#8a5cf6", width=6)
    draw.polygon([(a_cx - 40, y0 + 258), (a_cx - 58, y0 + 246), (a_cx - 54, y0 + 270)], fill="#8a5cf6")
    draw.text((black_centers["G#"] + 54, y0 + 138), "G# 想往 A 解决", fill="#8a5cf6", font=font(24, bold=True))

    draw.rounded_rectangle((84, 606, 1416, 862), 28, fill="#fff9ef", outline="#d4c5b2", width=3)
    draw.text((116, 640), "和弦结构：G# - B - D - F = 1 - b3 - b5 - bb7", fill="#7a542d", font=font(35, bold=True))
    draw.text((116, 704), "连续小三度：G#→B、B→D、D→F 都是小三度，所以它听起来均匀、紧绷、没有明显稳定重心。", fill="#5f5447", font=font(29))
    draw.text((116, 768), "钢琴练法：先同时按 G#-B-D-F，再把 G#→A、B→C、D→C 或 E、F→E，直接听见“紧张回家”的过程。", fill="#5f5447", font=font(28))

    img.save(ASSET_DIR / "piano-diminished-seventh.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote):
    grid_left = x + 74
    grid_top = y + 116
    fret_gap = 54
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 430, y + 470), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 30, y + 24), title_text, fill="#1d3136", font=font(34, bold=True))
    draw.text((x + 30, y + 70), subtitle, fill="#60717a", font=font(20))

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
        center_text(draw, (sx - 12, grid_top + 250, sx + 12, grid_top + 282), name, "#51606b", font(16, bold=True))

    draw.text((x + 30, y + 404), footnote, fill="#52656e", font=font(20))


def save_guitar_chart():
    img = Image.new("RGB", (1520, 980), "#edf4f6")
    draw = ImageDraw.Draw(img)
    draw.text((60, 40), "吉他图：减七和弦的对称指型", fill="#17313b", font=font(54, bold=True))
    draw.text(
        (60, 106),
        "减七和弦最适合在吉他上体会“每隔 3 品重复一次”的对称性。把同一个形状整体平移 3 品，音名会轮换，但和弦功能仍然属于同一个 dim7 集合。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 182, 1432, 316), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 220), "示例指型：G#dim7 = x x 6 7 6 7。四个音是 G#-B-D-F，正好全是小三度叠置。", fill="#233943", font=font(31, bold=True))
    draw.text((114, 266), "把这个形状移到 9-10 品或 12-13 品，声音紧张度几乎不变，这就是减七和弦“可循环”的实用价值。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        378,
        "G#dim7",
        "x x 6 7 6 7",
        [(2, 2, "1", "#bd7a2f"), (3, 3, "3", "#bd7a2f"), (2, 4, "2", "#bd7a2f"), (3, 5, "4", "#bd7a2f")],
        {0: "X", 1: "X"},
        "原位：把 4-1 弦看作一个紧凑的悬疑色彩块。",
    )
    draw_chord_grid(
        draw,
        544,
        378,
        "同形上移 3 品",
        "x x 9 10 9 10",
        [(2, 2, "1", "#5f7fb8"), (3, 3, "3", "#5f7fb8"), (2, 4, "2", "#5f7fb8"), (3, 5, "4", "#5f7fb8")],
        {0: "X", 1: "X"},
        "上移 3 品后，音名重排，但仍是同一组 dim7 音。",
    )
    draw_chord_grid(
        draw,
        1000,
        378,
        "解决到 Am",
        "x 0 2 2 1 0",
        [(2, 1, "2", "#2f8b61"), (2, 2, "3", "#2f8b61"), (1, 3, "1", "#2f8b61")],
        {0: "X", 4: "O", 5: "O"},
        "最常见用法：dim7 后立刻落到小调主和弦。",
    )

    draw.line((470, 608, 544, 608), fill="#94a0a6", width=7)
    draw.polygon([(544, 608), (522, 594), (522, 622)], fill="#94a0a6")
    draw.line((926, 608, 1000, 608), fill="#94a0a6", width=7)
    draw.polygon([(1000, 608), (978, 594), (978, 622)], fill="#94a0a6")

    draw.rounded_rectangle((86, 854, 1432, 940), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((114, 884), "伴奏练法：| Am | G#dim7 | Am/E | E7 | Am |。dim7 不适合久停，更适合当“往前推一下”的经过或导向和弦。", fill="#4d5f68", font=font(27, bold=True))

    img.save(ASSET_DIR / "guitar-diminished-seventh.png")


def save_structure_chart():
    img = Image.new("RGB", (1440, 900), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：减七和弦的对称性与解决感", fill="#2d261d", font=font(52, bold=True))
    draw.text((56, 106), "完整减七和弦由连续小三度叠成，所以四个音彼此间距均匀；这也是它既对称又不稳定的原因。", fill="#655a4e", font=font(27))

    draw.rounded_rectangle((86, 194, 650, 732), 26, fill="#eef4ff", outline="#5f7fb8", width=4)
    draw.text((120, 232), "G#dim7 结构", fill="#5f7fb8", font=font(42, bold=True))
    draw.text((120, 310), "G# - B - D - F", fill="#4d5d70", font=font(35, bold=True))
    draw.text((120, 386), "1 - b3 - b5 - bb7", fill="#4d5d70", font=font(32))
    draw.text((120, 462), "每相邻两音都是小三度", fill="#4d5d70", font=font(31))
    draw.text((120, 534), "对称、密集、悬念强", fill="#4d5d70", font=font(31))
    draw.text((120, 600), "常见角色：导向 Am 的 vii°7", fill="#4d5d70", font=font(28))

    draw.rounded_rectangle((790, 194, 1352, 732), 26, fill="#fff3e8", outline="#bd7a2f", width=4)
    draw.text((824, 232), "为什么它特别想解决", fill="#bd7a2f", font=font(40, bold=True))
    draw.text((824, 310), "G# -> A", fill="#6e5437", font=font(34, bold=True))
    draw.text((824, 378), "B -> C", fill="#6e5437", font=font(34, bold=True))
    draw.text((824, 446), "D -> C 或 E", fill="#6e5437", font=font(34, bold=True))
    draw.text((824, 514), "F -> E", fill="#6e5437", font=font(34, bold=True))
    draw.text((824, 594), "多个音都带着半音倾向，所以它比普通三和弦更难“原地站稳”。", fill="#6e5437", font=font(28))

    draw.line((650, 458, 790, 458), fill="#9f907e", width=8)
    draw.polygon([(790, 458), (766, 444), (766, 472)], fill="#9f907e")
    draw.text((672, 412), "半音解决", fill="#7a664f", font=font(24, bold=True))

    draw.rounded_rectangle((126, 782, 1278, 846), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((154, 802), "一句话：减七和弦最值得记住的，不是“它有多怪”，而是“它由连续小三度构成，因此天然适合制造强烈导向”。", fill="#5f5547", font=font(29, bold=True))

    img.save(ASSET_DIR / "diminished-seventh-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
