from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-13-minor-major-seventh"
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
    img = Image.new("RGB", (1500, 940), "#f6f1e8")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "钢琴图：A-C-E-G# 小小大七和弦", fill="#2b241d", font=font(54, bold=True))
    draw.text(
        (56, 106),
        "小小大七和弦 = 小三和弦 + 大七度。在 A 小调里写作 Am(maj7)，它是旋律小调最有辨识度的主和弦色彩。",
        fill="#6d5d4f",
        font=font(28),
    )

    white_w = 126
    white_h = 318
    x0 = 76
    y0 = 228
    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    centers = {}
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#26313e", width=3)
        draw.text((x + 18, y0 + 266), name, fill="#596472", font=font(28, bold=True))
        centers[f"{name}{i}"] = x + white_w / 2

    black_w = 76
    black_h = 194
    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#", "D#", "F#", "G#", "A#"]
    black_centers = {}
    for pos, name in zip(black_positions, black_names):
        x = x0 + white_w * (pos + 1) - black_w / 2
        black_centers[name] = x + black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 140, x + black_w, y0 + black_h), name, "#f8fafc", font(20, bold=True))

    note_positions = [
        (centers["A5"], y0 + 246, "#2f8b61", "A", "根音"),
        (centers["C0"], y0 + 246, "#c65b4b", "C", "小三度"),
        (centers["E2"], y0 + 246, "#5f7fb8", "E", "纯五度"),
        (black_centers["G#"], y0 + 100, "#bd7a2f", "G#", "大七度"),
    ]
    for cx, cy, color, note, label in note_positions:
        draw.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 30, cy - 26, cx + 30, cy + 18), note, "#ffffff", font(24, bold=True))
        draw.text((cx - 44, cy + 42), label, fill=color, font=font(21, bold=True))

    draw.line((black_centers["G#"] + 40, y0 + 132, centers["A5"] - 40, y0 + 262), fill="#bd7a2f", width=6)
    draw.polygon(
        [(centers["A5"] - 40, y0 + 262), (centers["A5"] - 58, y0 + 250), (centers["A5"] - 54, y0 + 274)],
        fill="#bd7a2f",
    )
    draw.text((black_centers["G#"] + 54, y0 + 136), "大七度紧贴主音，张力非常明显", fill="#bd7a2f", font=font(24, bold=True))

    draw.rounded_rectangle((84, 608, 1416, 854), 28, fill="#fff9ef", outline="#d4c5b2", width=3)
    draw.text((116, 642), "和弦结构：A - C - E - G# = 1 - b3 - 5 - 7", fill="#7a542d", font=font(35, bold=True))
    draw.text((116, 706), "听感关键词：忧郁、悬着、不完全落地，比普通 Am 更精致，也比 Amaj7 更暗。", fill="#5f5447", font=font(30))
    draw.text((116, 768), "钢琴练法：左手弹 A，右手同时按 C-E-G#；再把 G# 解决到 A，体会“快要回家但还没落稳”的感觉。", fill="#5f5447", font=font(28))

    img.save(ASSET_DIR / "piano-minor-major-seventh.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks):
    grid_left = x + 64
    grid_top = y + 112
    fret_gap = 56
    string_gap = 42

    draw.rounded_rectangle((x, y, x + 396, y + 454), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#1d3136", font=font(34, bold=True))
    draw.text((x + 28, y + 70), subtitle, fill="#60717a", font=font(20))

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


def save_guitar_chart():
    img = Image.new("RGB", (1520, 980), "#edf4f6")
    draw = ImageDraw.Draw(img)
    draw.text((60, 40), "吉他图：Am、Am(maj7)、Am7 的对比", fill="#17313b", font=font(54, bold=True))
    draw.text(
        (60, 106),
        "吉他上最容易学会这类色彩的方式，不是单独背一个复杂名称，而是对比同一个 A 小调主和弦的三个版本。",
        fill="#4d636c",
        font=font(27),
    )

    draw.rounded_rectangle((86, 182, 1432, 316), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 220), "核心差别：Am = G 不参与；Am7 = 小七度 G；Am(maj7) = 大七度 G#。", fill="#233943", font=font(31, bold=True))
    draw.text((114, 266), "把 5 弦空弦 A 当根音，单独听 G 与 G# 的变化，就能很快分辨“小七”和“大七”的紧张度。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        378,
        "Am",
        "基础小三和弦",
        [(2, 1, "2", "#5f7fb8"), (2, 2, "3", "#5f7fb8"), (1, 3, "1", "#5f7fb8")],
        {0: "X", 4: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        562,
        378,
        "Am(maj7)",
        "把 G 升到 G#",
        [(2, 1, "2", "#bd7a2f"), (2, 2, "3", "#bd7a2f"), (1, 3, "1", "#bd7a2f"), (1, 4, "4", "#bd7a2f")],
        {0: "X", 5: "O"},
    )
    draw_chord_grid(
        draw,
        1036,
        378,
        "Am7",
        "把 G 保留下来",
        [(2, 1, "2", "#2f8b61"), (2, 2, "3", "#2f8b61"), (1, 3, "1", "#2f8b61")],
        {0: "X", 4: "O", 5: "O"},
    )

    draw.line((484, 606, 562, 606), fill="#94a0a6", width=7)
    draw.polygon([(562, 606), (540, 592), (540, 620)], fill="#94a0a6")
    draw.line((958, 606, 1036, 606), fill="#94a0a6", width=7)
    draw.polygon([(1036, 606), (1014, 592), (1014, 620)], fill="#94a0a6")

    draw.rounded_rectangle((86, 854, 1432, 940), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((114, 884), "伴奏练法：| Am | Am(maj7) | Am7 | Dm6 |。这是一条经典下行线 A-G#-G-F#，电影配乐和 bossa 常见。", fill="#4d5f68", font=font(27, bold=True))

    img.save(ASSET_DIR / "guitar-minor-major-seventh.png")


def save_structure_chart():
    img = Image.new("RGB", (1440, 900), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：小小大七和弦如何从旋律小调长出来", fill="#2d261d", font=font(52, bold=True))
    draw.text((56, 106), "在 A 旋律小调 A-B-C-D-E-F#-G# 中，以 A 为根音叠三度：A-C-E-G#，得到 Am(maj7)。", fill="#655a4e", font=font(27))

    draw.rounded_rectangle((86, 200, 648, 730), 26, fill="#eef4ff", outline="#5f7fb8", width=4)
    draw.text((120, 238), "普通小七和弦 Am7", fill="#5f7fb8", font=font(40, bold=True))
    draw.text((120, 312), "A - C - E - G", fill="#4d5d70", font=font(34, bold=True))
    draw.text((120, 384), "1 - b3 - 5 - b7", fill="#4d5d70", font=font(32))
    draw.text((120, 452), "更松弛、更蓝调", fill="#4d5d70", font=font(31))
    draw.text((120, 520), "常见于流行、R&B、爵士 ii-V-I", fill="#4d5d70", font=font(28))

    draw.rounded_rectangle((790, 200, 1352, 730), 26, fill="#fff3e8", outline="#bd7a2f", width=4)
    draw.text((824, 238), "小小大七和弦 Am(maj7)", fill="#bd7a2f", font=font(40, bold=True))
    draw.text((824, 312), "A - C - E - G#", fill="#6e5437", font=font(34, bold=True))
    draw.text((824, 384), "1 - b3 - 5 - 7", fill="#6e5437", font=font(32))
    draw.text((824, 452), "更悬、更精致、更像旋律小调", fill="#6e5437", font=font(31))
    draw.text((824, 520), "常见于电影配乐、拉丁爵士、悬疑感开头", fill="#6e5437", font=font(28))

    draw.line((648, 454, 790, 454), fill="#9f907e", width=8)
    draw.polygon([(790, 454), (766, 440), (766, 468)], fill="#9f907e")
    draw.text((666, 410), "把 G 升成 G#", fill="#7a664f", font=font(24, bold=True))

    draw.rounded_rectangle((126, 780, 1278, 846), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((154, 800), "一句话：Am(maj7) 不是“Am 多加一个音”而已，它是旋律小调升 7 级后自然产生的标志性主和弦色彩。", fill="#5f5547", font=font(29, bold=True))

    img.save(ASSET_DIR / "minor-major-seventh-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
