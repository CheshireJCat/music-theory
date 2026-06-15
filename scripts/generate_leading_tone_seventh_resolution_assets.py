from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-15-leading-tone-seventh-resolution"
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
    img = Image.new("RGB", (1560, 980), "#f6f1e8")
    draw = ImageDraw.Draw(img)
    draw.text((56, 42), "钢琴图：vii°7 -> i 的四声部解决", fill="#2f261d", font=font(54, bold=True))
    draw.text(
        (56, 108),
        "以 A 小调为例：G#dim7 不是终点，而是把四个声部同时推回 Am。最重要的是听见每个音怎样找到自己的落点。",
        fill="#65594c",
        font=font(28),
    )

    white_w = 116
    white_h = 320
    x0 = 76
    y0 = 226
    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    centers = {}
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#2d3946", width=3)
        draw.text((x + 18, y0 + 268), name, fill="#5d6774", font=font(28, bold=True))
        centers[f"{name}{i}"] = x + white_w / 2

    black_w = 68
    black_h = 192
    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#", "D#", "F#", "G#", "A#"]
    black_centers = {}
    for pos, name in zip(black_positions, black_names):
        x = x0 + white_w * (pos + 1) - black_w / 2
        black_centers[name] = x + black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#131a22")
        center_text(draw, (x, y0 + 136, x + black_w, y0 + black_h), name, "#f8fafc", font(20, bold=True))

    source_notes = [
        ("G#", black_centers["G#"], y0 + 98, "#bd7a2f", "导音"),
        ("B", centers["B6"], y0 + 246, "#2f8b61", "上行"),
        ("D", centers["D1"], y0 + 246, "#5f7fb8", "下行"),
        ("F", centers["F3"], y0 + 246, "#c65b4b", "下行"),
    ]
    target_notes = [
        ("A", centers["A5"], y0 + 246, "#8a5cf6", "主音"),
        ("C", centers["C7"], y0 + 246, "#8a5cf6", "三音"),
        ("C", centers["C0"], y0 + 246, "#8a5cf6", "三音"),
        ("E", centers["E2"], y0 + 246, "#8a5cf6", "五音"),
    ]

    for note, cx, cy, color, label in source_notes:
        draw.ellipse((cx - 32, cy - 32, cx + 32, cy + 32), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 28, cy - 24, cx + 28, cy + 16), note, "#ffffff", font(22, bold=True))
        draw.text((cx - 28, cy + 40), label, fill=color, font=font(20, bold=True))

    for note, cx, cy, color, label in target_notes:
        draw.ellipse((cx - 32, cy - 32, cx + 32, cy + 32), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 28, cy - 24, cx + 28, cy + 16), note, "#ffffff", font(22, bold=True))

    arrows = [
        (black_centers["G#"] + 38, y0 + 126, centers["A5"] - 40, y0 + 246, "#8a5cf6", "G# -> A"),
        (centers["B6"] - 34, y0 + 224, centers["C7"] - 38, y0 + 224, "#2f8b61", "B -> C"),
        (centers["D1"] + 34, y0 + 214, centers["C0"] + 38, y0 + 214, "#5f7fb8", "D -> C"),
        (centers["F3"] + 34, y0 + 224, centers["E2"] + 38, y0 + 224, "#c65b4b", "F -> E"),
    ]
    for x1, y1, x2, y2, color, label in arrows:
        draw.line((x1, y1, x2, y2), fill=color, width=5)
        draw.polygon([(x2, y2), (x2 - 18, y2 - 10), (x2 - 18, y2 + 10)], fill=color)
        draw.text(((x1 + x2) / 2 - 26, y1 - 42), label, fill=color, font=font(20, bold=True))

    draw.rounded_rectangle((88, 608, 1464, 886), 28, fill="#fff9ef", outline="#d7c8b5", width=3)
    draw.text((120, 642), "标准听法：G#dim7 = G# B D F 先制造张力，再解决到 Am = A C E。", fill="#7a542d", font=font(34, bold=True))
    draw.text((120, 708), "关键不是只记“dim7 很紧张”，而是记住每个音的去向：导音 G# 上行，F 下行，B 与 D 往最近的稳定音移动。", fill="#5d5447", font=font(28))
    draw.text((120, 774), "钢琴练法：左手弹 A 作为低音，右手先按 G#dim7，再分声部慢慢移动到 A-C-E，耳朵会很清楚地听见“解决”发生。", fill="#5d5447", font=font(28))

    img.save(ASSET_DIR / "piano-leading-tone-seventh-resolution.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote):
    grid_left = x + 74
    grid_top = y + 114
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 420, y + 450), 26, fill="#fffdfa", outline="#d0d8dc", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#1c3138", font=font(34, bold=True))
    draw.text((x + 28, y + 70), subtitle, fill="#5c6d75", font=font(19))

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
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#51606b", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 240, sx + 12, grid_top + 272), name, "#51606b", font(16, bold=True))

    draw.text((x + 28, y + 382), footnote, fill="#52656e", font=font(19))


def save_guitar_chart():
    img = Image.new("RGB", (1500, 980), "#edf4f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 42), "吉他图：把 dim7 作为通向主和弦的经过和弦", fill="#17313b", font=font(52, bold=True))
    draw.text(
        (58, 108),
        "吉他上练 vii°7 -> i，重点不是刷很久，而是让紧张和放松紧挨着出现。这里继续用 A 小调：G#dim7 立刻解决到 Am。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 184, 1414, 308), 24, fill="#fffdfa", outline="#c7d3d7", width=3)
    draw.text((114, 218), "一个够用的练习循环：| Am | G#dim7 | E7 | Am |。先弹稳 Am，再把 G#dim7 当作只停一拍的导向和弦。", fill="#223942", font=font(30, bold=True))
    draw.text((114, 262), "如果只背形状，很容易把 dim7 弹成“奇怪的小和弦”；如果连着解决一起练，耳朵才会真正记住它的功能。", fill="#536770", font=font(24))

    draw_chord_grid(
        draw,
        92,
        376,
        "Am",
        "x 0 2 2 1 0",
        [(2, 1, "2", "#2f8b61"), (2, 2, "3", "#2f8b61"), (1, 3, "1", "#2f8b61")],
        {0: "X", 4: "O", 5: "O"},
        "起点：先把 Am 的稳定感听牢。",
    )
    draw_chord_grid(
        draw,
        540,
        376,
        "G#dim7",
        "x x 6 7 6 7",
        [(2, 2, "1", "#bd7a2f"), (3, 3, "3", "#bd7a2f"), (2, 4, "2", "#bd7a2f"), (3, 5, "4", "#bd7a2f")],
        {0: "X", 1: "X"},
        "中间：只停一拍，制造明显悬念。",
    )
    draw_chord_grid(
        draw,
        988,
        376,
        "Am (回到主和弦)",
        "x 0 2 2 1 0",
        [(2, 1, "2", "#8a5cf6"), (2, 2, "3", "#8a5cf6"), (1, 3, "1", "#8a5cf6")],
        {0: "X", 4: "O", 5: "O"},
        "终点：dim7 后立刻落回稳定中心。",
    )

    draw.line((512, 602, 540, 602), fill="#9aa8ad", width=7)
    draw.polygon([(540, 602), (520, 590), (520, 614)], fill="#9aa8ad")
    draw.line((960, 602, 988, 602), fill="#9aa8ad", width=7)
    draw.polygon([(988, 602), (968, 590), (968, 614)], fill="#9aa8ad")

    draw.rounded_rectangle((86, 844, 1414, 936), 24, fill="#fffaf4", outline="#cfd7db", width=3)
    draw.text((114, 876), "吉他练法：先分解 Am，再弹 G#dim7，再立刻回 Am；如果想更明显，可以在 dim7 之后先过一下 E7，再回到 Am。", fill="#4e6069", font=font(26, bold=True))

    img.save(ASSET_DIR / "guitar-leading-tone-seventh-resolution.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：vii°7 为什么会强烈解决到 i", fill="#2d261d", font=font(52, bold=True))
    draw.text((56, 106), "今天只记一件事：vii°7 的价值不在名字，而在每个音都有清楚的去向，所以它会强迫音乐向前。", fill="#655a4e", font=font(27))

    draw.rounded_rectangle((86, 194, 660, 760), 26, fill="#eef4ff", outline="#5f7fb8", width=4)
    draw.text((118, 230), "A 小调示例", fill="#5f7fb8", font=font(42, bold=True))
    draw.text((118, 306), "G#dim7 -> Am", fill="#4f6073", font=font(36, bold=True))
    draw.text((118, 380), "G# B D F -> A C E", fill="#4f6073", font=font(32))
    draw.text((118, 456), "导音上行：G# -> A", fill="#4f6073", font=font(30))
    draw.text((118, 516), "其余声部走最近距离：", fill="#4f6073", font=font(30))
    draw.text((148, 570), "B -> C", fill="#4f6073", font=font(28))
    draw.text((148, 620), "D -> C 或 E", fill="#4f6073", font=font(28))
    draw.text((148, 670), "F -> E", fill="#4f6073", font=font(28))

    draw.rounded_rectangle((784, 194, 1360, 760), 26, fill="#fff2e7", outline="#bd7a2f", width=4)
    draw.text((816, 230), "练习时该听什么", fill="#bd7a2f", font=font(40, bold=True))
    draw.text((816, 314), "1. 先听 dim7 的不稳定", fill="#6d5336", font=font(30))
    draw.text((816, 384), "2. 再听每个音怎么回家", fill="#6d5336", font=font(30))
    draw.text((816, 454), "3. 最后听整体从“悬着”到“落地”", fill="#6d5336", font=font(30))
    draw.text((816, 544), "如果你只会按形状，但听不出解决方向，说明还没有真正掌握它的功能。", fill="#6d5336", font=font(28))
    draw.text((816, 634), "一句人话：vii°7 不是为了独立站住，而是为了把你送回 i。", fill="#6d5336", font=font(30, bold=True))

    draw.line((660, 478, 784, 478), fill="#a2907d", width=8)
    draw.polygon([(784, 478), (760, 464), (760, 492)], fill="#a2907d")
    draw.text((688, 434), "解决", fill="#7a664f", font=font(24, bold=True))

    draw.rounded_rectangle((120, 802, 1288, 868), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((148, 822), "口诀：dim7 的“任务”比它的“颜色”更重要。练到耳朵能预测每个音往哪里走，才算真正会用。", fill="#5f5547", font=font(29, bold=True))

    img.save(ASSET_DIR / "leading-tone-seventh-resolution-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
