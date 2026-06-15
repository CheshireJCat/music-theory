from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-28-upper-pedal"
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
    img = Image.new("RGB", (1560, 980), "#f4f0e8")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Upper Pedal 上持续音", fill="#2b251d", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "在 D 大调里把高音 A 持续保留在右手顶声部，左手与中声部做 D -> G -> A -> D。固定支点从低音转到高音，听感会更悬浮、更像上方持续发光。",
        fill="#675b4f",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 868), "#eef5ff", "#b3c4dd", "高音固定", "A pedal", "顶声部一直留住 A", "#4d6f98"),
        ((574, 186, 986, 868), "#f9f2e7", "#ddc29e", "下方和声变化", "D -> G -> A", "支点不在低音，而在上面发亮", "#b97b3a"),
        ((1074, 186, 1486, 868), "#eef7ef", "#abc6af", "听感结果", "悬浮张力", "不像厚底座，更像上空持续悬着", "#46785e"),
    ]

    for box, fill, outline, title, chord, desc, title_color in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=title_color, font=font(40, bold=True))
        draw.text((x0, 286), chord, fill=title_color, font=font(36, bold=True))
        draw.text((x0, 370), desc, fill="#5f6870", font=font(29))

    for x, y in [(186, 650), (686, 650), (1186, 650)]:
        draw_note(draw, x, y, "A", "#466c95")

    for note, x, y, color in [
        ("D", 160, 804, "#466c95"),
        ("F#", 246, 734, "#466c95"),
        ("A", 332, 804, "#466c95"),
        ("G", 660, 804, "#c98846"),
        ("B", 746, 734, "#c98846"),
        ("D", 832, 804, "#c98846"),
        ("A", 1186, 650, "#4f8a66"),
        ("C#", 1272, 734, "#4f8a66"),
        ("E", 1358, 804, "#4f8a66"),
    ]:
        draw_note(draw, x, y, note, color)

    draw.line((486, 734, 574, 734), fill="#9cadbf", width=7)
    draw.polygon([(574, 734), (552, 720), (552, 748)], fill="#9cadbf")
    draw.line((986, 734, 1074, 734), fill="#d0ab7e", width=7)
    draw.polygon([(1074, 734), (1052, 720), (1052, 748)], fill="#d0ab7e")

    draw.rounded_rectangle((96, 896, 1460, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (120, 908),
        "钢琴练法：右手小指持续按住 A，左手与中声部依次弹 D、G、A、D。重点听“亮点一直悬在上面”，而不是“地板一直在下面”。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-upper-pedal.png")


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
    draw.text((58, 40), "吉他图：用开放一弦做 Upper Pedal", fill="#163039", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "吉他上最容易做 upper pedal 的方式，是让开放一弦 e 持续共鸣，再在下方更换和弦。它不是低音铺底，而是高音线一直悬在上面。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 178, 1432, 340), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 218), "Upper Pedal 的关键不是“固定最高音就行”，而是这条高音要在和弦变化中持续被听见。吉他上最顺手的就是保留开放一弦，让和弦围着它换色。", fill="#223943", font=font(28, bold=True))
    draw.text((114, 272), "今天用 E 小调练习，因为开放一弦 e 很容易保留。你会听到和声在下方走 Em -> Cmaj7 -> Dsus2 -> Em，而高音 e 像一条持续悬浮的线。", fill="#516771", font=font(24))

    draw_chord_grid(
        draw,
        88,
        428,
        "Em",
        "0 2 2 0 0 0",
        [(2, 1, "2"), (2, 2, "3")],
        {0: "O", 3: "O", 4: "O", 5: "O"},
        "先建立 E 小调，并让高音 e 明显地持续响着。",
        "#2f8b61",
    )
    draw_chord_grid(
        draw,
        548,
        428,
        "Cmaj7",
        "x 3 2 0 0 0",
        [(3, 1, "3"), (2, 2, "2")],
        {0: "X", 3: "O", 4: "O", 5: "O"},
        "下方变成 Cmaj7，但高音 e 仍然不动，形成温和悬浮感。",
        "#cf7e3e",
    )
    draw_chord_grid(
        draw,
        1008,
        428,
        "Dsus2",
        "x x 0 2 3 0",
        [(2, 3, "1"), (3, 4, "3")],
        {0: "X", 1: "X", 2: "O", 5: "O"},
        "属前推动里继续保留高音 e，让张力挂在上方。",
        "#5f7fb8",
    )

    draw.line((512, 662, 548, 662), fill="#95a1a7", width=7)
    draw.polygon([(548, 662), (528, 650), (528, 674)], fill="#95a1a7")
    draw.line((972, 662, 1008, 662), fill="#c1a075", width=7)
    draw.polygon([(1008, 662), (988, 650), (988, 674)], fill="#c1a075")

    draw.rounded_rectangle((86, 900, 1432, 982), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 926),
        "练法：每个和弦扫 4 下或分解 6 音，尽量别碰掉一弦开放 e。重点听“高音不动、下方在换景色”的感觉。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-upper-pedal.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Upper Pedal", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 106),
        "一句话：把固定支点放在高音声部，而不是低音。这样不会形成厚底座，而会形成上方持续悬挂的亮线，常见于抒情前奏、配乐和琶音织体。",
        fill="#655a4e",
        font=font(27),
    )

    steps = [
        ("1. 固定高音", "A / e", "先让顶声部变成不动支点。", "#eef4ff", "#5f7fb8"),
        ("2. 下方先稳定", "D 或 Em", "先交代当前调性感。", "#fff3e7", "#bd7a2f"),
        ("3. 下方改色", "G / Cmaj7 / Dsus2", "和弦推进，但高音线还悬着。", "#eef4ff", "#5f7fb8"),
        ("4. 回到中心", "D 或 Em", "固定高音帮助整句收回，但仍留一点空中余韵。", "#edf8ef", "#4d8a64"),
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
        draw.text((x0 + 24, top + 112), chord, fill="#51483d", font=font(39, bold=True))
        draw.text((x0 + 24, top + 214), desc, fill="#5f564b", font=font(25))
        if idx < len(steps) - 1:
            ax = x1
            bx = x1 + gap
            y = top + 210
            draw.line((ax, y, bx, y), fill="#9f907e", width=8)
            draw.polygon([(bx, y), (bx - 24, y - 14), (bx - 24, y + 14)], fill="#9f907e")

    draw.rounded_rectangle((118, 760, 1314, 852), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text(
        (142, 786),
        "最容易混淆的点：Upper Pedal 不是简单的旋律重复。只有当那条高音在多个和弦上持续承担共同支点作用时，它才是真正的 upper pedal。",
        fill="#5f5547",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "upper-pedal-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
