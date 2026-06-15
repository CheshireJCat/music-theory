from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-11-harmonic-minor-leading-tone"
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
    img = Image.new("RGB", (1500, 920), "#f4efe6")
    draw = ImageDraw.Draw(img)
    draw.text((60, 40), "钢琴图：A 自然小调 vs A 和声小调（升七级）", fill="#2f261d", font=font(50, bold=True))
    draw.text(
        (60, 104),
        "核心变化：自然小调第七级是 G，和声小调把它升为 G#，导向主音 A 的力量更强。",
        fill="#6f6254",
        font=font(27),
    )

    white_w = 150
    white_h = 320
    x0 = 78
    y0 = 220
    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#27313f", width=3)
        draw.text((x + 22, y0 + 268), name, fill="#5c6673", font=font(30, bold=True))

    black_w = 88
    black_h = 198
    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#", "D#", "F#", "G#", "A#"]
    black_centers = {}
    for pos, name in zip(black_positions, black_names):
        x = x0 + white_w * (pos + 1) - black_w / 2
        black_centers[name] = x + black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 142, x + black_w, y0 + black_h), name, "#f9fafb", font(22, bold=True))

    g_white_x = x0 + 4 * white_w + white_w / 2
    draw.ellipse((g_white_x - 34, y0 + 218, g_white_x + 34, y0 + 286), fill="#5f7fb8", outline="#ffffff", width=3)
    center_text(draw, (g_white_x - 30, y0 + 228, g_white_x + 30, y0 + 276), "G", "#ffffff", font(26, bold=True))
    draw.text((g_white_x - 72, y0 + 298), "自然小调 7", fill="#5f7fb8", font=font(23, bold=True))

    g_sharp_x = black_centers["G#"]
    draw.ellipse((g_sharp_x - 34, y0 + 102, g_sharp_x + 34, y0 + 170), fill="#bd7a2f", outline="#ffffff", width=3)
    center_text(draw, (g_sharp_x - 32, y0 + 112, g_sharp_x + 32, y0 + 158), "G#", "#ffffff", font(24, bold=True))
    draw.text((g_sharp_x - 108, y0 + 178), "和声小调 升7", fill="#bd7a2f", font=font(23, bold=True))

    a_x = x0 + 5 * white_w + white_w / 2
    draw.ellipse((a_x - 38, y0 + 246, a_x + 38, y0 + 322), fill="#2f8b61", outline="#ffffff", width=3)
    center_text(draw, (a_x - 34, y0 + 258, a_x + 34, y0 + 312), "A", "#ffffff", font(28, bold=True))

    draw.line((g_white_x + 40, y0 + 252, a_x - 44, y0 + 284), fill="#5f7fb8", width=6)
    draw.polygon([(a_x - 44, y0 + 284), (a_x - 62, y0 + 274), (a_x - 58, y0 + 294)], fill="#5f7fb8")
    draw.text((g_white_x + 44, y0 + 220), "全音", fill="#5f7fb8", font=font(24, bold=True))

    draw.line((g_sharp_x + 40, y0 + 132, a_x - 44, y0 + 284), fill="#bd7a2f", width=6)
    draw.polygon([(a_x - 44, y0 + 284), (a_x - 62, y0 + 274), (a_x - 58, y0 + 294)], fill="#bd7a2f")
    draw.text((g_sharp_x + 44, y0 + 146), "半音导向", fill="#bd7a2f", font=font(24, bold=True))

    draw.rounded_rectangle((86, 594, 1426, 860), 26, fill="#fff9ef", outline="#d4c5b2", width=3)
    draw.text((114, 622), "A 自然小调：A B C D E F G A", fill="#51606d", font=font(34, bold=True))
    draw.text((114, 682), "A 和声小调：A B C D E F G# A", fill="#7b552f", font=font(34, bold=True))
    draw.text((114, 748), "结论：把第七级从 G 升到 G# 后，回到 A 的解决感会明显增强。", fill="#5f5447", font=font(30))

    img.save(ASSET_DIR / "piano-harmonic-minor-leading-tone.png")


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
    img = Image.new("RGB", (1500, 980), "#edf4f6")
    draw = ImageDraw.Draw(img)
    draw.text((66, 40), "吉他图：导音升高后，V7 -> i 的收束更强", fill="#17303a", font=font(54, bold=True))
    draw.text(
        (66, 108),
        "在 A 小调中，对比 Em(自然小调 v) 与 E7(和声小调 V7)：E7 里的 G# 会更强烈地指向 Am。",
        fill="#49626b",
        font=font(27),
    )

    draw.rounded_rectangle((88, 186, 1412, 304), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 222), "关键听感：G 到 A（全音）较松；G# 到 A（半音）更紧，常用于句尾制造“必须回家”的感觉。", fill="#223842", font=font(30, bold=True))

    draw_chord_grid(
        draw,
        90,
        362,
        "Em",
        "自然小调常见 v",
        [(2, 0, "2", "#5f7fb8"), (2, 1, "3", "#5f7fb8")],
        {2: "O", 3: "O", 4: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        552,
        362,
        "E7",
        "和声小调常见 V7",
        [(2, 0, "2", "#bd7a2f"), (2, 1, "3", "#bd7a2f"), (1, 3, "1", "#bd7a2f")],
        {2: "O", 4: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        1014,
        362,
        "Am",
        "i：主和弦落点",
        [(2, 1, "2", "#2f8b61"), (2, 2, "3", "#2f8b61"), (1, 3, "1", "#2f8b61")],
        {0: "X", 4: "O", 5: "O"},
    )

    draw.line((486, 594, 552, 594), fill="#8f9ca3", width=7)
    draw.polygon([(552, 594), (530, 580), (530, 608)], fill="#8f9ca3")
    draw.line((948, 594, 1014, 594), fill="#8f9ca3", width=7)
    draw.polygon([(1014, 594), (992, 580), (992, 608)], fill="#8f9ca3")

    draw.rounded_rectangle((90, 868, 1412, 936), 22, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((112, 890), "练法：| Em | Am | 与 | E7 | Am | 轮流弹，比较哪一个更有“句子结束”感，再加入 | Bm7b5 | E7 | Am |。", fill="#4d5f68", font=font(26, bold=True))

    img.save(ASSET_DIR / "guitar-harmonic-minor-leading-tone.png")


def save_interval_chart():
    img = Image.new("RGB", (1400, 860), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "音程结构图：为什么升七级会增强导向", fill="#2d261d", font=font(52, bold=True))
    draw.text((58, 106), "把第七级升高后，7 到 1 从全音变成半音，听感会从“可能回去”变成“强烈想回去”。", fill="#655a4e", font=font(27))

    draw.rounded_rectangle((84, 196, 656, 704), 26, fill="#eef4ff", outline="#5f7fb8", width=4)
    draw.text((120, 234), "自然小调", fill="#5f7fb8", font=font(40, bold=True))
    draw.text((120, 306), "7 = G", fill="#4d5d70", font=font(34, bold=True))
    draw.text((120, 366), "G -> A = 全音", fill="#4d5d70", font=font(34, bold=True))
    draw.text((120, 446), "导向相对柔和", fill="#4d5d70", font=font(32))
    draw.text((120, 526), "常见：v -> i（Em -> Am）", fill="#4d5d70", font=font(30))

    draw.rounded_rectangle((744, 196, 1316, 704), 26, fill="#fff3e8", outline="#bd7a2f", width=4)
    draw.text((780, 234), "和声小调", fill="#bd7a2f", font=font(40, bold=True))
    draw.text((780, 306), "7 = G#", fill="#6e5437", font=font(34, bold=True))
    draw.text((780, 366), "G# -> A = 半音", fill="#6e5437", font=font(34, bold=True))
    draw.text((780, 446), "导向显著增强", fill="#6e5437", font=font(32))
    draw.text((780, 526), "常见：V7 -> i（E7 -> Am）", fill="#6e5437", font=font(30))

    draw.line((656, 450, 744, 450), fill="#9f907e", width=8)
    draw.polygon([(744, 450), (720, 436), (720, 464)], fill="#9f907e")

    draw.rounded_rectangle((126, 744, 1274, 822), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((154, 768), "一句话：升七级本质上是把“7 到 1”的距离收紧，从而让终止更像终止。", fill="#5f5547", font=font(30, bold=True))

    img.save(ASSET_DIR / "harmonic-minor-leading-tone-interval.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_interval_chart()
