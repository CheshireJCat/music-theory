from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-29-ostinato-bass"
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
    draw.ellipse((x - 30, y - 30, x + 30, y + 30), fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 22, y - 18, x + 22, y + 16), label, "#ffffff", font(18, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f5f1ea")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Ostinato Bass 持续低音", fill="#2b251d", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "在 A 小调里把左手低音型 A - G - F - E 持续循环，右手再叠加和弦或旋律。重点不是单个支点，而是整条重复低音轨道。",
        fill="#675b4f",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 868), "#edf4ff", "#b1c4df", "左手固定循环", "A - G - F - E", "四个音反复回来，形成低音轨道", "#456d9a"),
        ((574, 186, 986, 868), "#faf2e5", "#dec59a", "右手上层变化", "Am - G - F - E", "和弦或旋律可变，但低音型不变", "#bc7f38"),
        ((1074, 186, 1486, 868), "#edf7ef", "#acc8b0", "听感结果", "推进感", "不像静止支点，更像一直向前滚动", "#4b7d61"),
    ]

    for box, fill, outline, title, chord, desc, title_color in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=title_color, font=font(40, bold=True))
        draw.text((x0, 286), chord, fill=title_color, font=font(36, bold=True))
        draw.text((x0, 370), desc, fill="#5f6870", font=font(29))

    for note, x, y, color in [
        ("A", 152, 786, "#456d9a"),
        ("G", 238, 724, "#456d9a"),
        ("F", 324, 786, "#456d9a"),
        ("E", 410, 724, "#456d9a"),
        ("A", 652, 786, "#c98546"),
        ("C", 738, 724, "#c98546"),
        ("E", 824, 786, "#c98546"),
        ("G", 910, 724, "#c98546"),
        ("A", 1156, 786, "#4f8a66"),
        ("G", 1242, 724, "#4f8a66"),
        ("F", 1328, 786, "#4f8a66"),
        ("E", 1414, 724, "#4f8a66"),
    ]:
        draw_note(draw, x, y, note, color)

    draw.line((486, 734, 574, 734), fill="#9cadbf", width=7)
    draw.polygon([(574, 734), (552, 720), (552, 748)], fill="#9cadbf")
    draw.line((986, 734, 1074, 734), fill="#d0ab7e", width=7)
    draw.polygon([(1074, 734), (1052, 720), (1052, 748)], fill="#d0ab7e")

    draw.rounded_rectangle((96, 896, 1460, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (120, 908),
        "钢琴练法：左手先只练 A - G - F - E 的稳定循环，右手后加和弦。重点听“低音在滚动推进”，而不是“一个点固定不动”。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-ostinato-bass.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 118
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 304, y + 470), 28, fill="#fffdfa", outline="#d2d6db", width=3)
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

    draw.text((x + 28, y + 404), footnote, fill="#52656e", font=font(17))


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1060), "#edf4f5")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：Am - G - F - E 的 Ostinato Bass", fill="#163039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上最直接的做法，是让低音线 A -> G -> F -> E 清楚地下行。和弦会换，但听众首先会记住这条重复回来的 bass line。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 320), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "Ostinato Bass 和普通换和弦的差别，在于低音不只是“顺便变化”，而是主动成为段落的记忆点。今天先练最常见的 A 小调下行循环。", fill="#223943", font=font(27, bold=True))
    draw.text((114, 258), "建议先用慢速分解或轻扫，每小节把第 1 拍低音根音弹清楚。只要 A -> G -> F -> E 的轨迹稳定，整段就会自然形成推进感。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "低音 A 建立起点。", "#2f8b61"),
        ("G", "3 2 0 0 0 3", [(3, 0, "2"), (2, 1, "1"), (3, 5, "3")], {2: "O", 3: "O", 4: "O"}, "低音下降到 G。", "#c97b3f"),
        ("F", "1 3 3 2 1 1", [(1, 0, "1"), (3, 1, "3"), (3, 2, "4"), (2, 3, "2"), (1, 4, "1"), (1, 5, "1")], {}, "继续降到 F，张力变厚。", "#5c7db8"),
        ("E", "0 2 2 1 0 0", [(2, 1, "2"), (2, 2, "3"), (1, 3, "1")], {0: "O", 4: "O", 5: "O"}, "回到属功能低音 E。", "#a15b6b"),
    ]

    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 404, title, subtitle, dots, top, footnote, color)

    for start, end, color in [(392, 402, "#95a1a7"), (706, 716, "#b9986f"), (1020, 1030, "#95a1a7")]:
        draw.line((start, 638, end, 638), fill=color, width=7)
        draw.polygon([(end, 638), (end - 18, 626), (end - 18, 650)], fill=color)

    draw.rounded_rectangle((86, 930, 1474, 1016), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 956),
        "练法：拇指先把 A -> G -> F -> E 低音弹稳，再补完整和弦。要让人一听就能跟着记住这条下降 bass line。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-ostinato-bass.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Ostinato Bass", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 106),
        "一句话：把低音从“单个持续支点”发展成“会反复循环的短句”。这样听感不再只是稳定，而会形成持续推进、反复回归的段落骨架。",
        fill="#655a4e",
        font=font(27),
    )

    steps = [
        ("1. 写出低音型", "A - G - F - E", "先决定哪条低音线要重复出现。", "#eef4ff", "#5f7fb8"),
        ("2. 固定循环", "repeat", "让这条低音型稳定反复，不轻易改。", "#fff3e7", "#bd7a2f"),
        ("3. 上方改色", "Am / G / F / E", "和弦和旋律可以换，但低音轨道保留。", "#eef4ff", "#5f7fb8"),
        ("4. 形成记忆点", "推进感", "听众会先记住这条 bass line。", "#edf8ef", "#4d8a64"),
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
        "最容易混淆的点：只要低音重复，并不自动等于 ostinato。只有当这条低音型被反复当作段落骨架使用，它才是真正的 ostinato bass。",
        fill="#5f5547",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "ostinato-bass-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
