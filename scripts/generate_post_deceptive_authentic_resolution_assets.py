from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-19-post-deceptive-authentic-resolution"
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


def draw_note(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str):
    draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 24, y - 18, x + 24, y + 14), label, "#ffffff", font(21, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f5f2eb")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：延缓后再真正终止", fill="#2e261c", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "今天只看一种句法：先用 E7 -> F 把终止延后，再用 E7 -> Am 真正落地。重点不是新和弦，而是两次解决的时间差。",
        fill="#665a4b",
        font=font(28),
    )

    draw.rounded_rectangle((70, 184, 486, 870), 28, fill="#ecf5ff", outline="#b6cbe3", width=3)
    draw.rounded_rectangle((572, 184, 988, 870), 28, fill="#fff4e7", outline="#e5c39b", width=3)
    draw.rounded_rectangle((1074, 184, 1490, 870), 28, fill="#edf8ef", outline="#abc7af", width=3)

    draw.text((100, 220), "第一步", fill="#3b6598", font=font(40, bold=True))
    draw.text((100, 278), "E7", fill="#3b6598", font=font(34, bold=True))
    draw.text((100, 348), "属功能把耳朵", fill="#526277", font=font(29))
    draw.text((100, 396), "拉向 Am。", fill="#526277", font=font(29))
    draw.text((100, 478), "音：E G# B D", fill="#526277", font=font(29, bold=True))

    draw.text((602, 220), "第二步", fill="#a8662d", font=font(40, bold=True))
    draw.text((602, 278), "F", fill="#a8662d", font=font(34, bold=True))
    draw.text((602, 348), "先不回家，", fill="#6b5b46", font=font(29))
    draw.text((602, 396), "把句子偏转一下。", fill="#6b5b46", font=font(29))
    draw.text((602, 478), "音：F A C", fill="#6b5b46", font=font(29, bold=True))

    draw.text((1104, 220), "第三步", fill="#357254", font=font(40, bold=True))
    draw.text((1104, 278), "E7 -> Am", fill="#357254", font=font(34, bold=True))
    draw.text((1104, 348), "重新拉起张力，", fill="#506658", font=font(29))
    draw.text((1104, 396), "再真正落地。", fill="#506658", font=font(29))
    draw.text((1104, 478), "音：A C E", fill="#506658", font=font(29, bold=True))

    for note, x, y, color in [
        ("E", 138, 682, "#3b6598"),
        ("G#", 222, 682, "#3b6598"),
        ("B", 306, 682, "#3b6598"),
        ("D", 390, 682, "#3b6598"),
        ("F", 640, 682, "#d18242"),
        ("A", 724, 682, "#d18242"),
        ("C", 808, 616, "#d18242"),
        ("E", 1140, 682, "#357254"),
        ("G#", 1216, 682, "#357254"),
        ("B", 1292, 682, "#357254"),
        ("D", 1368, 682, "#357254"),
        ("A", 1200, 792, "#5a9b76"),
        ("C", 1276, 726, "#5a9b76"),
        ("E", 1352, 792, "#5a9b76"),
    ]:
        draw_note(draw, x, y, note, color)

    draw.line((430, 682, 572, 682), fill="#95a9c6", width=7)
    draw.polygon([(572, 682), (550, 668), (550, 696)], fill="#95a9c6")
    draw.line((918, 682, 1074, 682), fill="#cfa06d", width=7)
    draw.polygon([(1074, 682), (1052, 668), (1052, 696)], fill="#cfa06d")

    draw.rounded_rectangle((98, 896, 1462, 944), 18, fill="#fffdf9", outline="#d6cabd", width=2)
    draw.text(
        (122, 908),
        "练耳重点：不是单独听 F，而是听“E7 先骗开一次，再用第二个 E7 把真正终止补回来”的完整时间线。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-post-deceptive-authentic-resolution.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 118
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 424, y + 470), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#21323a", font=font(34, bold=True))
    draw.text((x + 28, y + 72), subtitle, fill="#66757d", font=font(20))

    for i in range(6):
        sx = grid_left + i * string_gap
        draw.line((sx, grid_top, sx, grid_top + 4 * fret_gap), fill="#2d3748", width=4)
    for i in range(5):
        sy = grid_top + i * fret_gap
        draw.line((grid_left, sy, grid_left + 5 * string_gap, sy), fill="#2d3748", width=8 if i == 0 else 4)

    for fret, string_idx, label in dots:
        cx = grid_left + string_idx * string_gap
        cy = grid_top + (fret - 0.5) * fret_gap
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#ffffff", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#56656f", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 246, sx + 12, grid_top + 278), name, "#56656f", font(16, bold=True))

    draw.text((x + 28, y + 404), footnote, fill="#52656e", font=font(19))


def save_guitar_chart():
    img = Image.new("RGB", (1520, 1000), "#eef4f5")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：偏转后再回归的五和弦路线", fill="#173039", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "吉他上最好把今天的知识点练成一句完整进行，而不是分开背概念。核心循环：| Am | E7 | F | E7 | Am |。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 178, 1432, 332), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 218), "前 3 个和弦说明“先被骗开”，后 2 个和弦说明“再真正回家”。这就是 Post-Deceptive Authentic Resolution。", fill="#223943", font=font(31, bold=True))
    draw.text((114, 270), "如果只弹到 F 就停住，你只练到了延缓解决；把 E7 -> Am 补上，才是今天这一课的完整句法。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        404,
        "Am",
        "x 0 2 2 1 0",
        [(2, 1, "2"), (2, 2, "3"), (1, 3, "1")],
        {0: "X", 4: "O", 5: "O"},
        "起点与终点都是主和弦。",
        "#2f8b61",
    )
    draw_chord_grid(
        draw,
        548,
        404,
        "E7",
        "0 2 0 1 0 0",
        [(2, 1, "2"), (1, 3, "1")],
        {0: "O", 2: "O", 4: "O", 5: "O"},
        "第一次出现：制造预期；第二次出现：把句子拉回终止线。",
        "#5f7fb8",
    )
    draw_chord_grid(
        draw,
        1008,
        404,
        "F",
        "1 3 3 2 1 1",
        [(1, 0, "1"), (3, 1, "3"), (3, 2, "4"), (2, 3, "2"), (1, 4, "1"), (1, 5, "1")],
        {},
        "中途偏转：让真正的终止晚一点发生。",
        "#cf7e3e",
    )

    draw.line((512, 638, 548, 638), fill="#95a1a7", width=7)
    draw.polygon([(548, 638), (528, 626), (528, 650)], fill="#95a1a7")
    draw.line((972, 638, 1008, 638), fill="#c1a075", width=7)
    draw.polygon([(1008, 638), (988, 626), (988, 650)], fill="#c1a075")

    draw.rounded_rectangle((86, 874, 1432, 956), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 900),
        "节奏练法：每个和弦 4 下，先全下拨 5 轮，再改成 低-高-低高 的分解。重点听 F 后面第二次 E7 为什么会让 Am 的落地更明显。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-post-deceptive-authentic-resolution.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Post-Deceptive Authentic Resolution", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 106),
        "一句话：先用 deceptive resolution 把终止延后，再补一个 authentic cadence，让真正回家比平常更有分量。",
        fill="#655a4e",
        font=font(27),
    )

    steps = [
        ("1. 预期建立", "V7", "耳朵以为会直接回 i。", "#eef4ff", "#5f7fb8"),
        ("2. 预期偏转", "VI", "先不回家，句子继续往前。", "#fff3e7", "#bd7a2f"),
        ("3. 张力重建", "V7", "重新把听感拉回终止线。", "#eef4ff", "#5f7fb8"),
        ("4. 真正落地", "i", "现在才完成 authentic cadence。", "#edf8ef", "#4d8a64"),
    ]

    left = 84
    top = 248
    width = 292
    height = 430
    gap = 44
    for idx, (title, chord, desc, fill, outline) in enumerate(steps):
        x0 = left + idx * (width + gap)
        x1 = x0 + width
        draw.rounded_rectangle((x0, top, x1, top + height), 26, fill=fill, outline=outline, width=4)
        draw.text((x0 + 24, top + 28), title, fill=outline, font=font(31, bold=True))
        draw.text((x0 + 24, top + 112), chord, fill="#51483d", font=font(52, bold=True))
        draw.text((x0 + 24, top + 214), desc, fill="#5f564b", font=font(25))
        if idx < len(steps) - 1:
            ax = x1
            bx = x1 + gap
            y = top + 210
            draw.line((ax, y, bx, y), fill="#9f907e", width=8)
            draw.polygon([(bx, y), (bx - 24, y - 14), (bx - 24, y + 14)], fill="#9f907e")

    draw.rounded_rectangle((120, 764, 1310, 852), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text(
        (146, 790),
        "听感逻辑：第一次 V7 负责“骗开”，第二次 V7 负责“补回”。两次张力的功能不同，但都围绕同一个主和弦展开。",
        fill="#5f5547",
        font=font(28, bold=True),
    )

    img.save(ASSET_DIR / "post-deceptive-authentic-resolution-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
