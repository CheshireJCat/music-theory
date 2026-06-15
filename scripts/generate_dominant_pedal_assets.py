from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-21-dominant-pedal"
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
    center_text(draw, (x - 24, y - 18, x + 24, y + 14), label, "#ffffff", font(20, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f6f2ea")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Dominant Pedal 属持续音", fill="#2b251c", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "低音持续停在属音 E，上方和弦继续移动。示例：| Am/E | Dm/E | E7 | Am |。耳朵会一直悬着，直到最后真正落回主和弦。",
        fill="#6a5b4c",
        font=font(28),
    )

    panels = [
        ((72, 186, 488, 870), "#eef4ff", "#b5c7e1", "持续低音", "E", "左手或低音区一直按住 E", "#446b9d"),
        ((572, 186, 988, 870), "#fff5ea", "#e3c39c", "上方变化", "Am/E -> Dm/E", "和声在动，地板不动", "#bc7837"),
        ((1072, 186, 1488, 870), "#eef8ef", "#abc6b0", "最终解决", "E7 -> Am", "最后才真正回家", "#3f7b59"),
    ]

    for box, fill, outline, title, chord, desc, title_color in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=title_color, font=font(40, bold=True))
        draw.text((x0, 286), chord, fill=title_color, font=font(36, bold=True))
        draw.text((x0, 368), desc, fill="#5d6770", font=font(29))

    for note, x, y, color in [
        ("E", 180, 716, "#446b9d"),
        ("E", 180, 804, "#446b9d"),
        ("A", 670, 716, "#cc8a49"),
        ("C", 754, 650, "#cc8a49"),
        ("E", 838, 716, "#cc8a49"),
        ("D", 670, 804, "#bc7837"),
        ("F", 754, 804, "#bc7837"),
        ("A", 838, 804, "#bc7837"),
        ("E", 922, 716, "#bc7837"),
        ("E", 1170, 716, "#4f916b"),
        ("G#", 1254, 650, "#4f916b"),
        ("B", 1338, 716, "#4f916b"),
        ("D", 1422, 650, "#4f916b"),
        ("A", 1212, 804, "#3f7b59"),
        ("C", 1296, 804, "#3f7b59"),
        ("E", 1380, 804, "#3f7b59"),
    ]:
        draw_note(draw, x, y, note, color)

    draw.line((488, 728, 572, 728), fill="#9bacbe", width=7)
    draw.polygon([(572, 728), (552, 716), (552, 740)], fill="#9bacbe")
    draw.line((988, 728, 1072, 728), fill="#d1aa7b", width=7)
    draw.polygon([(1072, 728), (1052, 716), (1052, 740)], fill="#d1aa7b")

    draw.rounded_rectangle((104, 896, 1458, 944), 18, fill="#fffdfa", outline="#d6cbbd", width=2)
    draw.text(
        (126, 908),
        "钢琴练法：左手持续按 E 或反复弹 E 八度，右手依次弹 Am、Dm、E7、Am。重点听“上面在换，下面不动”的悬停感。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-dominant-pedal.png")


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
    draw.text((58, 40), "吉他图：在高音 E 上制造尾声悬停", fill="#173039", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "吉他上最容易感受到 dominant pedal 的方法，是让第一弦开放 E 尽量持续响着，同时把和弦从 Am/E 推到 Dm/E，再到 E7、Am。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 178, 1432, 336), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 218), "Pedal Point 的关键不是和弦名字变复杂，而是某个音固定不走，让上面的和声移动时产生“悬着不落地”的张力。", fill="#223943", font=font(31, bold=True))
    draw.text((114, 272), "今天只练属持续音版本：保持 E 的存在感，听它怎样把结尾从“已经稳定”拖成“还在等待最后解决”。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        420,
        "Am/E",
        "0 0 2 2 1 0",
        [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")],
        {0: "O", 1: "O", 5: "O"},
        "低音和高音都能带出 E，适合开始建立 pedal 感。",
        "#2f8b61",
    )
    draw_chord_grid(
        draw,
        548,
        420,
        "Dm/E",
        "0 x 0 2 3 1",
        [(2, 2, "1"), (3, 3, "3"), (1, 4, "2")],
        {0: "O", 1: "X", 2: "O"},
        "和弦功能在变化，但 E 仍然留下来，张力更明显。",
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
        "最后把属功能说完整，再回到 Am 收尾。",
        "#5f7fb8",
    )

    draw.line((512, 654, 548, 654), fill="#95a1a7", width=7)
    draw.polygon([(548, 654), (528, 642), (528, 666)], fill="#95a1a7")
    draw.line((972, 654, 1008, 654), fill="#c1a075", width=7)
    draw.polygon([(1008, 654), (988, 642), (988, 666)], fill="#c1a075")

    draw.rounded_rectangle((86, 900, 1432, 980), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 926),
        "节奏练法：让第一弦尽量延音，扫弦顺序用低到高。对比普通 Am - Dm - E7 - Am，你会更容易听到 pedal 带来的悬停感。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-dominant-pedal.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Dominant Pedal", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 106),
        "一句话：让属音 E 持续存在，上方和弦继续移动，直到最后真正解决。这常用在结尾扩展、尾声、桥段回主前。",
        fill="#655a4e",
        font=font(27),
    )

    steps = [
        ("1. 固定低音", "E pedal", "把属音当成不动地板。", "#eef4ff", "#5f7fb8"),
        ("2. 上方变和声", "Am/E -> Dm/E", "和声在动，但稳定感被暂时悬住。", "#fff3e7", "#bd7a2f"),
        ("3. 属功能聚焦", "E7", "pedal 与属和弦合流，张力更集中。", "#eef4ff", "#5f7fb8"),
        ("4. 最终解决", "Am", "撤掉 pedal 的悬停，真正回家。", "#edf8ef", "#4d8a64"),
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
        "最容易混淆的点：Pedal Point 不是“低音不动所以很稳定”，恰恰相反，它经常因为低音不动而让上层和声显得更悬、更有等待感。",
        fill="#5f5547",
        font=font(27, bold=True),
    )

    img.save(ASSET_DIR / "dominant-pedal-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
