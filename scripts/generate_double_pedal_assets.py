from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-27-double-pedal"
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
    center_text(draw, (x - 24, y - 18, x + 24, y + 14), label, "#ffffff", font(18, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f3efe7")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Double Pedal 双持续音", fill="#2a251e", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "在 D 大调里同时把 D 和 A 固定在低音区，上方和弦做 D -> G -> A -> D。双持续音比单一 pedal 更厚，像长期存在的和声底座。",
        fill="#675b4f",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 868), "#eef5ff", "#b3c4dd", "两个固定支点", "D + A", "低音区一直保留 1 和 5", "#4d6f98"),
        ((574, 186, 986, 868), "#f9f2e7", "#ddc29e", "上层继续移动", "D -> G -> A", "和弦变，但底座不换", "#b97b3a"),
        ((1074, 186, 1486, 868), "#eef7ef", "#abc6af", "听感结果", "更宽、更稳", "不像悬挂，更像铺开的主中心", "#46785e"),
    ]

    for box, fill, outline, title, chord, desc, title_color in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=title_color, font=font(40, bold=True))
        draw.text((x0, 286), chord, fill=title_color, font=font(36, bold=True))
        draw.text((x0, 370), desc, fill="#5f6870", font=font(29))

    fixed_notes = [(160, 734), (250, 804), (660, 734), (750, 804), (1160, 734), (1250, 804)]
    for x, y in fixed_notes:
        draw_note(draw, x, y, "D" if y == 734 else "A", "#466c95")

    for note, x, y, color in [
        ("D", 832, 650, "#c98846"),
        ("F#", 916, 734, "#c98846"),
        ("A", 1000, 650, "#c98846"),
        ("G", 1338, 650, "#4f8a66"),
        ("B", 1422, 734, "#4f8a66"),
        ("D", 1338, 818, "#4f8a66"),
    ]:
        draw_note(draw, x, y, note, color)

    draw.line((486, 734, 574, 734), fill="#9cadbf", width=7)
    draw.polygon([(574, 734), (552, 720), (552, 748)], fill="#9cadbf")
    draw.line((986, 734, 1074, 734), fill="#d0ab7e", width=7)
    draw.polygon([(1074, 734), (1052, 720), (1052, 748)], fill="#d0ab7e")

    draw.rounded_rectangle((110, 896, 1450, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (130, 908),
        "钢琴练法：左手持续保留 D 和 A，可分八度或五度反复弹；右手依次弹 D、G、A、D。重点听“一个音变成两个音后，地板变厚了”。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-double-pedal.png")


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
    img = Image.new("RGB", (1520, 1020), "#edf4f5")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：开放弦里的 Double Pedal", fill="#163039", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "吉他上最容易做双持续音的方式，是让开放四弦 D 与开放一弦 e 形成持续共鸣，再在中间更换和弦形状；也可以理解成持续保留同一组开放支点。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 178, 1432, 340), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 218), "Double Pedal 比单一 pedal 多一个固定支点。对吉他来说，最常见的实现不是死守两个最低音，而是保留两个持续共鸣的开放弦，让上层和弦围着它们变化。", fill="#223943", font=font(28, bold=True))
    draw.text((114, 272), "今天用 D 大调练习：尽量让四弦 D 和一弦 e 的延音不断。这样会听到和声在动，但共鸣底座始终存在，特别适合前奏、指弹铺底和电影感尾声。", fill="#516771", font=font(24))

    draw_chord_grid(
        draw,
        88,
        428,
        "Dsus2",
        "x x 0 2 3 0",
        [(2, 3, "1"), (3, 4, "2")],
        {0: "X", 1: "X", 2: "O", 5: "O"},
        "先让 D 与 e 两条开放弦建立持续框架。",
        "#2f8b61",
    )
    draw_chord_grid(
        draw,
        548,
        428,
        "Gadd9/D",
        "x x 0 4 3 0",
        [(4, 3, "3"), (3, 4, "2")],
        {0: "X", 1: "X", 2: "O", 5: "O"},
        "中间换成 G 色彩，但双支点仍然保留。",
        "#cf7e3e",
    )
    draw_chord_grid(
        draw,
        1008,
        428,
        "A7sus4",
        "x 0 2 0 3 0",
        [(2, 2, "2"), (3, 4, "3")],
        {0: "X", 1: "O", 3: "O", 5: "O"},
        "转向属功能时，持续开放弦把声音拉得更宽。",
        "#5f7fb8",
    )

    draw.line((512, 662, 548, 662), fill="#95a1a7", width=7)
    draw.polygon([(548, 662), (528, 650), (528, 674)], fill="#95a1a7")
    draw.line((972, 662, 1008, 662), fill="#c1a075", width=7)
    draw.polygon([(1008, 662), (988, 650), (988, 674)], fill="#c1a075")

    draw.rounded_rectangle((86, 900, 1432, 982), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 926),
        "练法：每个和弦扫 4 下或做 6 连分解，刻意让开放四弦与一弦多留一点。重点不是复杂和弦名，而是听出“两个固定共鸣点”让声音更厚。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-double-pedal.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Double Pedal", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 106),
        "一句话：不是只固定一个音，而是同时保留两个支点。最常见的是 1 和 5，能让和声底座比 tonic pedal 更厚、更像长期铺开的背景。",
        fill="#655a4e",
        font=font(27),
    )

    steps = [
        ("1. 固定两音", "D + A", "把主音与五音都留住。", "#eef4ff", "#5f7fb8"),
        ("2. 叠上主和弦", "D", "先确认调性感与底座关系。", "#fff3e7", "#bd7a2f"),
        ("3. 上层改色", "G / A", "和声前进，但支点不离开。", "#eef4ff", "#5f7fb8"),
        ("4. 回到完整中心", "D", "厚底座让收束更宽阔。", "#edf8ef", "#4d8a64"),
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
        draw.text((x0 + 24, top + 112), chord, fill="#51483d", font=font(45, bold=True))
        draw.text((x0 + 24, top + 214), desc, fill="#5f564b", font=font(25))
        if idx < len(steps) - 1:
            ax = x1
            bx = x1 + gap
            y = top + 210
            draw.line((ax, y, bx, y), fill="#9f907e", width=8)
            draw.polygon([(bx, y), (bx - 24, y - 14), (bx - 24, y + 14)], fill="#9f907e")

    draw.rounded_rectangle((118, 760, 1314, 852), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text(
        (144, 786),
        "最容易混淆的点：Double Pedal 不是简单地“多弹几个低音”，而是这两个音要在和声变化时持续承担支点作用。它通常比单一 pedal 更厚、更像氛围底色。",
        fill="#5f5547",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "double-pedal-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
