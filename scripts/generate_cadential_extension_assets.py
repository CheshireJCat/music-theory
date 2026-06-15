from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-20-cadential-extension"
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
    img = Image.new("RGB", (1560, 980), "#f6f3ed")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：终止扩展 Cadential Extension", fill="#2d261d", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "在已经出现终止感之后，不立刻收住，而是插入一个短扩展，让最后的回家更像完整句点。示例：| Am | E7 | Am | Dm | E7 | Am |。",
        fill="#675a4d",
        font=font(28),
    )

    panels = [
        ((70, 184, 486, 872), "#edf5ff", "#b5c7e1", "第一层", "Am", "先得到一次落地", "音：A C E", "#3e6699"),
        ((572, 184, 988, 872), "#fff4e9", "#e5c49d", "扩展层", "Dm -> E7", "再拉一个小尾巴", "音：D F A / E G# B D", "#b36d32"),
        ((1074, 184, 1490, 872), "#edf8ef", "#abc6b0", "终点层", "Am", "这次才真正收句", "音：A C E", "#377153"),
    ]

    for box, fill, outline, title, chord, desc1, desc2, title_color in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 30
        draw.text((x0, 220), title, fill=title_color, font=font(40, bold=True))
        draw.text((x0, 278), chord, fill=title_color, font=font(34, bold=True))
        draw.text((x0, 356), desc1, fill="#56616a", font=font(29))
        draw.text((x0, 408), desc2, fill="#56616a", font=font(29, bold=True))

    for note, x, y, color in [
        ("A", 160, 700, "#3e6699"),
        ("C", 244, 634, "#3e6699"),
        ("E", 328, 700, "#3e6699"),
        ("D", 648, 700, "#c98445"),
        ("F", 732, 634, "#c98445"),
        ("A", 816, 700, "#c98445"),
        ("E", 708, 806, "#b36d32"),
        ("G#", 792, 806, "#b36d32"),
        ("B", 876, 806, "#b36d32"),
        ("D", 960, 740, "#b36d32"),
        ("A", 1162, 700, "#377153"),
        ("C", 1246, 634, "#377153"),
        ("E", 1330, 700, "#377153"),
    ]:
        draw_note(draw, x, y, note, color)

    draw.line((432, 690, 572, 690), fill="#97a8c3", width=7)
    draw.polygon([(572, 690), (550, 676), (550, 704)], fill="#97a8c3")
    draw.line((918, 740, 1074, 740), fill="#cfa26f", width=7)
    draw.polygon([(1074, 740), (1052, 726), (1052, 754)], fill="#cfa26f")

    draw.rounded_rectangle((96, 896, 1464, 944), 18, fill="#fffdfa", outline="#d6cbbd", width=2)
    draw.text(
        (120, 908),
        "钢琴练习时把第一次 Am 弹得像“已经结束”，再刻意补上 Dm -> E7 -> Am，你就能听出 cadential extension 的真正作用：延长结尾。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-cadential-extension.png")


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
    img = Image.new("RGB", (1520, 1020), "#eef4f5")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：把结尾再拉长两拍", fill="#173039", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "最常见的体验是：你已经听到 Am 落地了，但伴奏不马上停，而是再补一个 Dm -> E7 -> Am，把句尾做得更完整。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 178, 1432, 336), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 218), "Cadential Extension 不是换一个更复杂的终止，而是在终止已经成立后，继续扩写一个小尾声。", fill="#223943", font=font(31, bold=True))
    draw.text((114, 272), "吉他上可以直接练成：| Am | E7 | Am | Dm | E7 | Am |。前 3 个和弦像结尾，后 3 个和弦像再说一句“这次真的结束”。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        420,
        "Am",
        "x 0 2 2 1 0",
        [(2, 1, "2"), (2, 2, "3"), (1, 3, "1")],
        {0: "X", 4: "O", 5: "O"},
        "第一次和最后一次都弹这个主和弦，但角色不同。",
        "#2f8b61",
    )
    draw_chord_grid(
        draw,
        548,
        420,
        "Dm",
        "x x 0 2 3 1",
        [(2, 2, "1"), (3, 3, "3"), (1, 4, "2")],
        {0: "X", 1: "X", 2: "O"},
        "扩展段常用的前属支点，把结尾继续往前推。",
        "#cf7e3e",
    )
    draw_chord_grid(
        draw,
        1008,
        420,
        "E7",
        "0 2 0 1 0 0",
        [(2, 1, "2"), (1, 3, "1")],
        {0: "O", 2: "O", 4: "O", 5: "O"},
        "最后一次把张力重新聚焦，再回到 Am。",
        "#5f7fb8",
    )

    draw.line((512, 654, 548, 654), fill="#95a1a7", width=7)
    draw.polygon([(548, 654), (528, 642), (528, 666)], fill="#95a1a7")
    draw.line((972, 654, 1008, 654), fill="#c1a075", width=7)
    draw.polygon([(1008, 654), (988, 642), (988, 666)], fill="#c1a075")

    draw.rounded_rectangle((86, 900, 1432, 980), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 926),
        "节奏练法：前半句每和弦 2 拍，后半句 Dm - E7 - Am 每和弦 2 拍。重点听“已经结束”与“再补一句结束”之间的差别。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-cadential-extension.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Cadential Extension", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 106),
        "一句话：Authentic cadence 已经出现后，再补一个短的前属-属-主尾声，让结尾更稳、更完整、更像句点。",
        fill="#655a4e",
        font=font(27),
    )

    steps = [
        ("1. 已有终止", "V7 -> i", "耳朵已经觉得句子收住了。", "#eef4ff", "#5f7fb8"),
        ("2. 追加尾声", "iv / ii", "再补一个前属和弦，把句尾拉长。", "#fff3e7", "#bd7a2f"),
        ("3. 重建张力", "V7", "重新把听感拉回终止线。", "#eef4ff", "#5f7fb8"),
        ("4. 最终句点", "i", "这次才是完整、稳固的结尾。", "#edf8ef", "#4d8a64"),
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
        draw.text((x0 + 24, top + 112), chord, fill="#51483d", font=font(50, bold=True))
        draw.text((x0 + 24, top + 214), desc, fill="#5f564b", font=font(25))
        if idx < len(steps) - 1:
            ax = x1
            bx = x1 + gap
            y = top + 210
            draw.line((ax, y, bx, y), fill="#9f907e", width=8)
            draw.polygon([(bx, y), (bx - 24, y - 14), (bx - 24, y + 14)], fill="#9f907e")

    draw.rounded_rectangle((112, 760, 1320, 852), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text(
        (138, 786),
        "最容易混淆的点：Cadential Extension 不是“还没终止”，而是“终止已经到了，但作者故意把句尾再写长一点”。",
        fill="#5f5547",
        font=font(28, bold=True),
    )

    img.save(ASSET_DIR / "cadential-extension-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
