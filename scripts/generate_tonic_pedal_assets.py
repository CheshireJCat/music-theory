from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-25-tonic-pedal"
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
    img = Image.new("RGB", (1560, 980), "#f4f1ea")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Tonic Pedal 主持续音", fill="#2b241d", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "在 D 大调里把主音 D 持续放在低音区，上方和弦做 D -> G/D -> A/D -> D。低音像地板一样稳定，和声在其上展开。",
        fill="#67594d",
        font=font(28),
    )

    panels = [
        ((72, 186, 488, 870), "#eef6ff", "#b6c7de", "固定主音", "D pedal", "左手持续保留 D", "#45688d"),
        ((572, 186, 988, 870), "#f9f2e7", "#dfc29d", "上层移动", "G/D -> A/D", "稳定底座上出现展开", "#b67733"),
        ((1072, 186, 1488, 870), "#eef7ef", "#acc6af", "落回中心", "D", "一切再次收拢到主和弦", "#42765b"),
    ]

    for box, fill, outline, title, chord, desc, title_color in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=title_color, font=font(40, bold=True))
        draw.text((x0, 286), chord, fill=title_color, font=font(36, bold=True))
        draw.text((x0, 368), desc, fill="#5d6770", font=font(29))

    for note, x, y, color in [
        ("D", 180, 716, "#45688d"),
        ("D", 180, 804, "#45688d"),
        ("D", 670, 716, "#c98643"),
        ("G", 754, 650, "#c98643"),
        ("B", 838, 716, "#c98643"),
        ("D", 922, 650, "#c98643"),
        ("A", 670, 804, "#b67733"),
        ("C#", 754, 804, "#b67733"),
        ("E", 838, 716, "#b67733"),
        ("D", 922, 804, "#b67733"),
        ("D", 1170, 716, "#4e8b67"),
        ("F#", 1254, 650, "#4e8b67"),
        ("A", 1338, 716, "#4e8b67"),
        ("D", 1212, 804, "#42765b"),
        ("F#", 1296, 804, "#42765b"),
        ("A", 1380, 804, "#42765b"),
    ]:
        draw_note(draw, x, y, note, color)

    draw.line((488, 728, 572, 728), fill="#9aacbe", width=7)
    draw.polygon([(572, 728), (552, 716), (552, 740)], fill="#9aacbe")
    draw.line((988, 728, 1072, 728), fill="#d0aa7c", width=7)
    draw.polygon([(1072, 728), (1052, 716), (1052, 740)], fill="#d0aa7c")

    draw.rounded_rectangle((104, 896, 1458, 944), 18, fill="#fffdfa", outline="#d6cbbd", width=2)
    draw.text(
        (126, 908),
        "钢琴练法：左手持续按 D 或反复弹 D 八度，右手依次弹 D、G/D、A/D、D。重点听“下面已稳定，上面在展开”的感觉。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-tonic-pedal.png")


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
    draw.text((58, 40), "吉他图：在 D 音上建立稳定底座", fill="#173039", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "吉他上练 tonic pedal 最直接的做法，是让四弦开放 D 尽量持续响着，同时从 D 推到 G/D、A/D，再回到 D。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 178, 1432, 336), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 218), "Tonic Pedal 的关键是：固定的是主音，所以它不像 dominant pedal 那样一直催你解决，而是给你一个稳定的中心，让上方和声像围着家转。", fill="#223943", font=font(30, bold=True))
    draw.text((114, 272), "今天用 D 大调练，是因为开放四弦 D 很好保持。弹奏时尽量让四弦延音不断，感受每个和弦都仍然踩在主音地板上。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        420,
        "D",
        "x x 0 2 3 2",
        [(2, 3, "1"), (3, 4, "3"), (2, 5, "2")],
        {0: "X", 1: "X", 2: "O"},
        "先建立主和弦与开放四弦 D 的稳定中心。",
        "#2f8b61",
    )
    draw_chord_grid(
        draw,
        548,
        420,
        "G/D",
        "x x 0 0 3 3",
        [(3, 4, "1"), (3, 5, "2")],
        {0: "X", 1: "X", 2: "O", 3: "O"},
        "上层转向 IV，但 D 仍然持续在低音区。",
        "#cf7e3e",
    )
    draw_chord_grid(
        draw,
        1008,
        420,
        "A/D",
        "x x 0 2 2 0",
        [(2, 3, "1"), (2, 4, "2")],
        {0: "X", 1: "X", 2: "O", 5: "O"},
        "上层走到属功能，但地板仍然是 D。",
        "#5f7fb8",
    )

    draw.line((512, 654, 548, 654), fill="#95a1a7", width=7)
    draw.polygon([(548, 654), (528, 642), (528, 666)], fill="#95a1a7")
    draw.line((972, 654, 1008, 654), fill="#c1a075", width=7)
    draw.polygon([(1008, 654), (988, 642), (988, 666)], fill="#c1a075")

    draw.rounded_rectangle((86, 900, 1432, 980), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 926),
        "节奏练法：每个和弦扫 4 下，刻意让四弦开放 D 多留一点。对比普通 D - G - A - D，更容易听出 tonic pedal 的“稳定扩展感”。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-tonic-pedal.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Tonic Pedal", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 106),
        "一句话：让主音 D 持续存在，上方和弦继续移动，但整段音乐始终围绕主中心展开。常见于前奏、尾声、中段铺垫。",
        fill="#655a4e",
        font=font(27),
    )

    steps = [
        ("1. 固定主音", "D pedal", "先把主音变成不动地板。", "#eef4ff", "#5f7fb8"),
        ("2. 上层展开", "G/D", "和声离开主和弦，但中心没丢。", "#fff3e7", "#bd7a2f"),
        ("3. 短暂对比", "A/D", "出现一点推动感，却仍站在主音上。", "#eef4ff", "#5f7fb8"),
        ("4. 回到收拢", "D", "再次把稳定感说完整。", "#edf8ef", "#4d8a64"),
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
        "最容易混淆的点：Tonic Pedal 不是“完全不变化”，而是“变化都发生在一个稳定主中心之上”。它通常比 Dominant Pedal 更稳、更像扩展而不是催促。",
        fill="#5f5547",
        font=font(25, bold=True),
    )

    img.save(ASSET_DIR / "tonic-pedal-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
