from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-09-rumba-clave"
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


def draw_hit(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str):
    draw.ellipse((x - 30, y - 30, x + 30, y + 30), fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 26, y - 16, x + 26, y + 16), label, "#ffffff", font(17, bold=True))


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 116
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 304, y + 470), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#21323A", font=font(34, bold=True))
    draw.text((x + 28, y + 72), subtitle, fill="#66757D", font=font(20))

    for i in range(6):
        sx = grid_left + i * string_gap
        draw.line((sx, grid_top, sx, grid_top + 4 * fret_gap), fill="#2D3748", width=4)
    for i in range(5):
        sy = grid_top + i * fret_gap
        draw.line((grid_left, sy, grid_left + 5 * string_gap, sy), fill="#2D3748", width=8 if i == 0 else 4)

    for fret, string_idx, label in dots:
        cx = grid_left + string_idx * string_gap
        cy = grid_top + (fret - 0.5) * fret_gap
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#ffffff", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#56656F", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 246, sx + 12, grid_top + 278), name, "#56656F", font(16, bold=True))

    draw.text((x + 28, y + 404), footnote, fill="#52656E", font=font(17))


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f4efe7")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Rumba Clave 的后拍牵引", fill="#30261B", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Rumba Clave 在 son clave 的五击骨架上，把其中一个落点轻微后移，形成更明显的拖曳感。钢琴上要感受的是“不是更快，而是更会挂住后拍”。",
        fill="#68584A",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 872), "#fff3e7", "#dfc7a7", "骨架来源", "3-2 变体", "五击仍在，但其中一击故意拖后", "#ba7a37"),
        ((574, 186, 986, 872), "#eef4ff", "#b2c5df", "律动感觉", "后拍牵引", "第二小节更像被拽着往前滑", "#476f9d"),
        ((1074, 186, 1486, 872), "#eef8f0", "#afccb5", "钢琴应用", "低音 + 分层和弦", "左手固定骨架，右手在后拍补色彩", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 288), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 374), desc, fill="#5f6870", font=font(28))

    first_bar = [170, 308, 492]
    second_bar = [690, 882, 968]
    for idx, x in enumerate(first_bar, start=1):
        draw_hit(draw, x, 738, str(idx), "#c68445")
    for idx, x in enumerate(second_bar, start=4):
        draw_hit(draw, x, 738, str(idx), "#476f9d")

    chord_hits = [("Am9", 1156, 720), ("Dm9", 1284, 662), ("E7", 1412, 738)]
    for label, x, y in chord_hits:
        draw_hit(draw, x, y, label, "#4f8a66")

    draw.text((102, 800), "左手：A . . E . A | A . . E . .", fill="#ba7a37", font=font(27, bold=True))
    draw.text((604, 800), "口令：推 - 空 - 拉 | 等 - 拖 - 收", fill="#476f9d", font=font(27, bold=True))
    draw.text((1112, 800), "右手：Am9 - Dm9 - E7", fill="#4f8265", font=font(28, bold=True))

    draw.rounded_rectangle((92, 896, 1464, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (108, 907),
        "钢琴练法：先只拍出 3-2，再把第五击故意往后拖一点；稳定后用左手低音守骨架，右手在 Dm9 和 E7 里体会后拍吸力。",
        fill="#5f564b",
        font=font(22, bold=True),
    )

    img.save(ASSET_DIR / "piano-rumba-clave.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：Rumba Clave 的切分挂靠", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上练 Rumba Clave，不是把手打得更碎，而是把原来 son clave 的落点里某一个故意拖到后面，让律动像在脚边拽着你走。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am9  .  x  Am9 | Dm9  .  E7  .  Am9 |。先闷音守住 clave，再在拖后的落点补和弦，才会有 rumba 的摆动。", fill="#223943", font=font(25, bold=True))
    draw.text((114, 260), "如果每个空位都扫满，Rumba Clave 会立刻退化成普通八分音符伴奏。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am9", "x 0 2 0 1 0", [(2, 2, "2"), (1, 4, "1")], {0: "X", 1: "O", 3: "O", 5: "O"}, "先用短促第一击稳住重心。", "#2f8b61"),
        ("Am9", "x 0 2 0 1 0", [(2, 2, "2"), (1, 4, "1")], {0: "X", 1: "O", 3: "O", 5: "O"}, "第三击前保留空白，不要抢拍。", "#c97b3f"),
        ("Dm9", "x 5 3 5 5 5", [(3, 1, "1"), (2, 2, "2"), (3, 3, "3"), (3, 4, "4"), (3, 5, "4")], {0: "X"}, "第二小节先给一击，再留出拖后的入口。", "#5c7db8"),
        ("E7", "0 2 0 1 0 0", [(2, 1, "2"), (1, 3, "1")], {0: "O", 2: "O", 4: "O", 5: "O"}, "最后一击稍后进入，制造 rumba 挂感。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：拍稳骨架，再把后拍拖住。先全闷音练 3-2 轮廓，再把拖后的那一击换成和弦重音。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-rumba-clave.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Rumba Clave", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Rumba Clave 常被视为 son clave 的近亲。核心不是多打一拍，而是把其中一个落点拖向后拍，形成更明显的摆动和拉扯。",
        fill="#655a4e",
        font=font(27),
    )

    lane_top = 220
    lane_left = 96
    cell_w = 150
    lane_h = 132
    row_gap = 54
    accent_fill = "#d9803d"
    delayed_fill = "#8b6fb3"
    base_fill = "#e6ecf4"

    rows = [
        ("参考：3-2 Son Clave", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 6], [0, 3, 6], "先看原始 3-2 第一小节的三击。"),
        ("Rumba 拖后处理", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 7], [0, 3], "把第三击拖到更靠后的位置，形成悬挂感。"),
        ("第二小节回应", ["1", "&", "2", "&", "3", "&", "4", "&"], [2, 6], [2, 6], "第二小节保持两击，让拖后的张力被听见。"),
    ]

    for row_idx, (label, cells, accents, normal_accents, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 52), label, fill="#3f3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            if i in accents and i not in normal_accents:
                fill = delayed_fill
                outline = "#71559a"
            elif i in accents:
                fill = accent_fill
                outline = "#b86930"
            else:
                fill = base_fill
                outline = "#b7c2d0"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline, width=3)
            center_text(draw, (x0, y + 16, x1, y + 68), cell, "#ffffff" if i in accents else "#4a5766", font(26, bold=True))
            state = "delay" if i in accents and i not in normal_accents else ("hit" if i in accents else "rest")
            center_text(draw, (x0, y + 70, x1, y + 118), state, "#ffffff" if i in accents else "#667485", font(21, bold=i in accents))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((126, 840), "听感重点：先认出 son clave 的五击，再专门听那个被拖后的落点。Rumba Clave 的关键不是数量，而是悬挂出来的后拍。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "rumba-clave-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
