from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-12-melodic-minor"
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
    img = Image.new("RGB", (1540, 960), "#f6f0e7")
    draw = ImageDraw.Draw(img)
    draw.text((58, 38), "钢琴图：A 旋律小调上行与下行", fill="#2b241d", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "上行时把 6、7 级升高为 F#、G#，下行时恢复成 F、G。这样既保留小调色彩，又避免增二度太突兀。",
        fill="#695c4e",
        font=font(28),
    )

    white_w = 150
    white_h = 324
    x0 = 72
    y0 = 224
    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#26313e", width=3)
        draw.text((x + 22, y0 + 270), name, fill="#596472", font=font(30, bold=True))

    black_w = 88
    black_h = 198
    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#", "D#", "F#", "G#", "A#"]
    black_centers = {}
    for pos, name in zip(black_positions, black_names):
        x = x0 + white_w * (pos + 1) - black_w / 2
        black_centers[name] = x + black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 144, x + black_w, y0 + black_h), name, "#f8fafc", font(22, bold=True))

    f_x = x0 + 3 * white_w + white_w / 2
    g_x = x0 + 4 * white_w + white_w / 2
    a_x = x0 + 5 * white_w + white_w / 2
    f_sharp_x = black_centers["F#"]
    g_sharp_x = black_centers["G#"]

    for cx, note, label in [(f_x, "F", "下行 6"), (g_x, "G", "下行 7")]:
        draw.ellipse((cx - 34, y0 + 232, cx + 34, y0 + 300), fill="#5f7fb8", outline="#ffffff", width=3)
        center_text(draw, (cx - 30, y0 + 242, cx + 30, y0 + 288), note, "#ffffff", font(26, bold=True))
        draw.text((cx - 52, y0 + 306), label, fill="#5f7fb8", font=font(22, bold=True))

    for cx, note, label in [(f_sharp_x, "F#", "上行 升6"), (g_sharp_x, "G#", "上行 升7")]:
        draw.ellipse((cx - 34, y0 + 98, cx + 34, y0 + 166), fill="#bd7a2f", outline="#ffffff", width=3)
        center_text(draw, (cx - 30, y0 + 108, cx + 30, y0 + 154), note, "#ffffff", font(24, bold=True))
        draw.text((cx - 78, y0 + 172), label, fill="#bd7a2f", font=font(22, bold=True))

    draw.ellipse((a_x - 38, y0 + 244, a_x + 38, y0 + 320), fill="#2f8b61", outline="#ffffff", width=3)
    center_text(draw, (a_x - 34, y0 + 256, a_x + 34, y0 + 310), "A", "#ffffff", font(28, bold=True))

    draw.line((f_sharp_x + 38, y0 + 134, g_sharp_x - 42, y0 + 134), fill="#bd7a2f", width=6)
    draw.polygon([(g_sharp_x - 42, y0 + 134), (g_sharp_x - 60, y0 + 124), (g_sharp_x - 60, y0 + 144)], fill="#bd7a2f")
    draw.text((f_sharp_x + 44, y0 + 94), "上行走向更平滑", fill="#bd7a2f", font=font(24, bold=True))

    draw.line((g_sharp_x + 40, y0 + 134, a_x - 44, y0 + 282), fill="#bd7a2f", width=6)
    draw.polygon([(a_x - 44, y0 + 282), (a_x - 62, y0 + 272), (a_x - 58, y0 + 292)], fill="#bd7a2f")
    draw.text((g_sharp_x + 44, y0 + 150), "半音到主音", fill="#bd7a2f", font=font(24, bold=True))

    draw.rounded_rectangle((82, 592, 1452, 868), 28, fill="#fff9ef", outline="#d4c5b2", width=3)
    draw.text((112, 626), "A 旋律小调上行：A B C D E F# G# A", fill="#7a542d", font=font(34, bold=True))
    draw.text((112, 692), "A 旋律小调下行：A G F E D C B A", fill="#50606d", font=font(34, bold=True))
    draw.text((112, 760), "实用意义：上行时更适合旋律线条，下行时恢复自然小调色彩，不会一直保持“太亮”的 6、7 级。", fill="#5f5447", font=font(30))

    img.save(ASSET_DIR / "piano-melodic-minor.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks):
    grid_left = x + 64
    grid_top = y + 112
    fret_gap = 58
    string_gap = 44

    draw.rounded_rectangle((x, y, x + 396, y + 466), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#1d3136", font=font(34, bold=True))
    draw.text((x + 28, y + 70), subtitle, fill="#60717a", font=font(21))

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
    img = Image.new("RGB", (1520, 980), "#edf4f6")
    draw = ImageDraw.Draw(img)
    draw.text((62, 38), "吉他图：旋律小调在指板上的实际用法", fill="#16303a", font=font(54, bold=True))
    draw.text(
        (62, 106),
        "旋律小调常出现在小调句子的上行旋律、爵士 minor-major 色彩，或 V7 前的线条连接；下行时可以自然回到 A 自然小调。",
        fill="#4b636c",
        font=font(27),
    )

    draw.rounded_rectangle((86, 186, 1434, 314), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 222), "练耳思路：先唱 A-B-C-D-E-F#-G#-A，再唱 A-G-F-E-D-C-B-A。重点感受上行更“亮”、下行更“暗”。", fill="#223842", font=font(30, bold=True))

    draw_chord_grid(
        draw,
        88,
        370,
        "Am(maj7)",
        "旋律小调主和弦色彩",
        [(2, 1, "2", "#7f5aa8"), (2, 2, "3", "#7f5aa8"), (1, 3, "1", "#7f5aa8"), (1, 4, "4", "#7f5aa8")],
        {0: "X", 4: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        562,
        370,
        "D7",
        "上行中常见连接色彩",
        [(2, 0, "2", "#bd7a2f"), (1, 1, "1", "#bd7a2f"), (2, 2, "3", "#bd7a2f")],
        {3: "O", 4: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        1036,
        370,
        "E7",
        "回到 Am 前的属和弦",
        [(2, 0, "2", "#2f8b61"), (2, 1, "3", "#2f8b61"), (1, 3, "1", "#2f8b61")],
        {2: "O", 4: "O", 5: "O"},
    )

    draw.line((484, 604, 562, 604), fill="#94a0a6", width=7)
    draw.polygon([(562, 604), (540, 590), (540, 618)], fill="#94a0a6")
    draw.line((958, 604, 1036, 604), fill="#94a0a6", width=7)
    draw.polygon([(1036, 604), (1014, 590), (1014, 618)], fill="#94a0a6")

    draw.rounded_rectangle((86, 858, 1434, 936), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((112, 884), "练法：| Am(maj7) | D7 | E7 | Am |。上行旋律用 F#、G#，回落时改回 G、F，会更像真正的旋律小调句子。", fill="#4d5f68", font=font(27, bold=True))

    img.save(ASSET_DIR / "guitar-melodic-minor.png")


def save_structure_chart():
    img = Image.new("RGB", (1440, 900), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "结构图：旋律小调为何“上行升 6、7，下行还原”", fill="#2d261d", font=font(52, bold=True))
    draw.text((58, 106), "和声小调里 F 到 G# 是增二度，旋律里常显得跳。旋律小调把 F 升成 F#，让 E-F#-G#-A 更顺口。", fill="#655a4e", font=font(27))

    draw.rounded_rectangle((84, 196, 656, 724), 26, fill="#eef4ff", outline="#5f7fb8", width=4)
    draw.text((120, 234), "自然小调 / 下行", fill="#5f7fb8", font=font(40, bold=True))
    draw.text((120, 308), "A G F E D C B A", fill="#4d5d70", font=font(34, bold=True))
    draw.text((120, 380), "保留小调原本颜色", fill="#4d5d70", font=font(32))
    draw.text((120, 442), "下行回落更自然", fill="#4d5d70", font=font(32))
    draw.text((120, 526), "适合句尾、回声、收束", fill="#4d5d70", font=font(30))

    draw.rounded_rectangle((744, 196, 1316, 724), 26, fill="#fff3e8", outline="#bd7a2f", width=4)
    draw.text((780, 234), "旋律小调 / 上行", fill="#bd7a2f", font=font(40, bold=True))
    draw.text((780, 308), "A B C D E F# G# A", fill="#6e5437", font=font(34, bold=True))
    draw.text((780, 380), "E-F#-G#-A 更连贯", fill="#6e5437", font=font(32))
    draw.text((780, 442), "避免 F 到 G# 的增二度", fill="#6e5437", font=font(32))
    draw.text((780, 526), "适合上行旋律、爵士色彩", fill="#6e5437", font=font(30))

    draw.line((656, 448, 744, 448), fill="#9f907e", width=8)
    draw.polygon([(744, 448), (720, 434), (720, 462)], fill="#9f907e")

    draw.rounded_rectangle((126, 774, 1274, 844), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((154, 796), "一句话：旋律小调不是“永远升 6、7”，而是为了让上行旋律更顺畅、下行仍保留小调原味。", fill="#5f5547", font=font(30, bold=True))

    img.save(ASSET_DIR / "melodic-minor-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
