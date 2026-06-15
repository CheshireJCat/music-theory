from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-18-vii7-vs-v7-resolution"
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
    draw.text((56, 42), "钢琴图：比较 vii°7 -> i 和 V7 -> i 的解决", fill="#2f261d", font=font(54, bold=True))
    draw.text(
        (56, 108),
        "同样是在 A 小调里回到主和弦，G#dim7 更像“每个音都急着回家”，E7 则更像“属功能带着低音支点把你推回去”。",
        fill="#65594c",
        font=font(28),
    )

    draw.rounded_rectangle((70, 184, 748, 872), 28, fill="#fffaf1", outline="#d6c7b2", width=3)
    draw.rounded_rectangle((812, 184, 1490, 872), 28, fill="#f4f8ff", outline="#b7c7e6", width=3)

    draw.text((102, 218), "vii°7 -> i", fill="#7a542d", font=font(40, bold=True))
    draw.text((102, 278), "G#dim7 -> Am", fill="#7a542d", font=font(32, bold=True))
    draw.text((102, 340), "G# -> A", fill="#6c5a45", font=font(29, bold=True))
    draw.text((102, 390), "B -> C", fill="#6c5a45", font=font(29))
    draw.text((102, 440), "D -> C / E", fill="#6c5a45", font=font(29))
    draw.text((102, 490), "F -> E", fill="#6c5a45", font=font(29))
    draw.text((102, 566), "听感：更尖、更紧、", fill="#6c5a45", font=font(29))
    draw.text((102, 612), "像每条声部都在抢着解决。", fill="#6c5a45", font=font(29))

    draw.text((844, 218), "V7 -> i", fill="#385e9d", font=font(40, bold=True))
    draw.text((844, 278), "E7 -> Am", fill="#385e9d", font=font(32, bold=True))
    draw.text((844, 340), "G# -> A", fill="#506278", font=font(29, bold=True))
    draw.text((844, 390), "D -> C", fill="#506278", font=font(29))
    draw.text((844, 440), "B -> C 或留作经过", fill="#506278", font=font(29))
    draw.text((844, 490), "E 作为属音支点", fill="#506278", font=font(29))
    draw.text((844, 566), "听感：更完整、更传统、", fill="#506278", font=font(29))
    draw.text((844, 612), "像“先立住属，再回到主”。", fill="#506278", font=font(29))

    left_notes = [("G#", 146, 714, "#bd7a2f"), ("B", 250, 714, "#2f8b61"), ("D", 354, 714, "#5f7fb8"), ("F", 458, 714, "#c65b4b")]
    right_notes = [("E", 888, 714, "#385e9d"), ("G#", 992, 714, "#bd7a2f"), ("B", 1096, 714, "#2f8b61"), ("D", 1200, 714, "#5f7fb8")]
    target = [("A", 1300, 714, "#8a5cf6"), ("C", 1404, 714, "#8a5cf6"), ("E", 1452, 642, "#8a5cf6")]

    for note, x, y, color in left_notes + right_notes + target:
        draw.ellipse((x - 30, y - 30, x + 30, y + 30), fill=color, outline="#ffffff", width=3)
        center_text(draw, (x - 28, y - 22, x + 28, y + 16), note, "#ffffff", font(22, bold=True))

    draw.line((492, 714, 610, 714), fill="#9b8670", width=7)
    draw.polygon([(610, 714), (588, 700), (588, 728)], fill="#9b8670")
    draw.text((514, 670), "更密集的解决", fill="#8b7258", font=font(22, bold=True))

    draw.line((1234, 714, 1268, 714), fill="#8ca0c2", width=7)
    draw.polygon([(1268, 714), (1246, 700), (1246, 728)], fill="#8ca0c2")
    draw.text((1072, 770), "属功能支点更清楚", fill="#61789a", font=font(22, bold=True))

    draw.rounded_rectangle((96, 804, 1462, 916), 24, fill="#fffdf8", outline="#d8ccbd", width=3)
    draw.text((124, 836), "钢琴练法：先把两种解决都弹在同一个速度下。dim7 版本重点听四个音都想动；V7 版本重点听低音 E 和导音 G# 怎样共同制造回归。", fill="#5d5447", font=font(27, bold=True))

    img.save(ASSET_DIR / "piano-vii7-vs-v7-resolution.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote):
    grid_left = x + 74
    grid_top = y + 116
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 424, y + 462), 28, fill="#fffdfa", outline="#d2d6db", width=3)
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
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#51606b", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 244, sx + 12, grid_top + 276), name, "#51606b", font(16, bold=True))

    draw.text((x + 28, y + 398), footnote, fill="#52656e", font=font(19))


def save_guitar_chart():
    img = Image.new("RGB", (1520, 990), "#edf4f6")
    draw = ImageDraw.Draw(img)
    draw.text((60, 40), "吉他图：同样回到 Am，dim7 与 V7 的差别", fill="#17313b", font=font(54, bold=True))
    draw.text(
        (60, 106),
        "吉他上最直接的练法不是抽象比较，而是把两个连接都放到同一个小调循环里。这样你会很快听出谁更尖锐，谁更稳定。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 182, 1432, 320), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 220), "推荐比较：| Am | G#dim7 | Am | 和 | Am | E7 | Am |。前者像突然绷紧，后者像标准属和弦回家。", fill="#233943", font=font(31, bold=True))
    draw.text((114, 266), "如果想做更完整的伴奏，再弹 | Am | G#dim7 | E7 | Am |，dim7 会像属和弦前面再补一脚更尖的推动。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        388,
        "Am",
        "x 0 2 2 1 0",
        [(2, 1, "2", "#2f8b61"), (2, 2, "3", "#2f8b61"), (1, 3, "1", "#2f8b61")],
        {0: "X", 4: "O", 5: "O"},
        "稳定起点：先把主和弦中心听牢。",
    )
    draw_chord_grid(
        draw,
        548,
        388,
        "G#dim7",
        "x x 6 7 6 7",
        [(2, 2, "1", "#bd7a2f"), (3, 3, "3", "#bd7a2f"), (2, 4, "2", "#bd7a2f"), (3, 5, "4", "#bd7a2f")],
        {0: "X", 1: "X"},
        "更尖：像把音乐先吊起来，再松手。",
    )
    draw_chord_grid(
        draw,
        1008,
        388,
        "E7",
        "0 2 0 1 0 0",
        [(2, 1, "2", "#5f7fb8"), (1, 3, "1", "#5f7fb8")],
        {0: "O", 2: "O", 4: "O", 5: "O"},
        "更传统：属七的支点和方向都更明确。",
    )

    draw.line((512, 620, 548, 620), fill="#94a0a6", width=7)
    draw.polygon([(548, 620), (528, 608), (528, 632)], fill="#94a0a6")
    draw.line((972, 620, 1008, 620), fill="#94a0a6", width=7)
    draw.polygon([(1008, 620), (988, 608), (988, 632)], fill="#94a0a6")

    draw.rounded_rectangle((86, 860, 1432, 946), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((114, 890), "吉他练法：先只弹三小节比较两种回归，再把 dim7 和 E7 串起来。你会发现 dim7 更适合短促、悬疑、电影感；E7 更适合标准和声与歌伴奏。", fill="#4d5f68", font=font(27, bold=True))

    img.save(ASSET_DIR / "guitar-vii7-vs-v7-resolution.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：为什么 vii°7 和 V7 都能回到 i，但感觉不同", fill="#2d261d", font=font(52, bold=True))
    draw.text((56, 106), "今天只记一件事：两者都能解决到主和弦，但一个靠“多条声部同时急着动”，一个靠“属功能支点 + 导音”来推动。", fill="#655a4e", font=font(27))

    draw.rounded_rectangle((86, 194, 650, 764), 26, fill="#fff2e7", outline="#bd7a2f", width=4)
    draw.text((118, 232), "vii°7 -> i", fill="#bd7a2f", font=font(42, bold=True))
    draw.text((118, 310), "G# B D F -> A C E", fill="#6e5437", font=font(34, bold=True))
    draw.text((118, 386), "特点：四个音几乎都带有", fill="#6e5437", font=font(30))
    draw.text((118, 432), "半音或近距离解决倾向", fill="#6e5437", font=font(30))
    draw.text((118, 508), "听感：更尖、更密、", fill="#6e5437", font=font(30))
    draw.text((118, 554), "更像“马上落地”", fill="#6e5437", font=font(30))
    draw.text((118, 630), "适合：悬疑、短促导向、", fill="#6e5437", font=font(30))
    draw.text((118, 676), "dim7 经过和弦色彩", fill="#6e5437", font=font(30))

    draw.rounded_rectangle((808, 194, 1372, 764), 26, fill="#eef4ff", outline="#5f7fb8", width=4)
    draw.text((840, 232), "V7 -> i", fill="#5f7fb8", font=font(42, bold=True))
    draw.text((840, 310), "E G# B D -> A C E", fill="#4d5d70", font=font(34, bold=True))
    draw.text((840, 386), "特点：有明确属音 E 作为支点，", fill="#4d5d70", font=font(30))
    draw.text((840, 432), "再加导音 G# 指向主音 A", fill="#4d5d70", font=font(30))
    draw.text((840, 508), "听感：更完整、更传统、", fill="#4d5d70", font=font(30))
    draw.text((840, 554), "更像“标准终止”", fill="#4d5d70", font=font(30))
    draw.text((840, 630), "适合：古典终止、流行伴奏、", fill="#4d5d70", font=font(30))
    draw.text((840, 676), "常规属功能回归", fill="#4d5d70", font=font(30))

    draw.line((650, 476, 808, 476), fill="#9f907e", width=8)
    draw.polygon([(808, 476), (784, 462), (784, 490)], fill="#9f907e")
    draw.text((690, 432), "都回到 i", fill="#7a664f", font=font(24, bold=True))

    draw.rounded_rectangle((124, 804, 1298, 872), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((152, 824), "一句人话：vii°7 更像“纯张力解决器”，V7 更像“完整属功能终止器”。会比较，才算真正听懂它们。", fill="#5f5547", font=font(29, bold=True))

    img.save(ASSET_DIR / "vii7-vs-v7-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
