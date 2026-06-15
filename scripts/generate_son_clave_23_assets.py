from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-08-son-clave-23"
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
    center_text(draw, (x - 24, y - 16, x + 24, y + 16), label, "#ffffff", font(18, bold=True))


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
    img = Image.new("RGB", (1560, 980), "#f5f0e8")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：2-3 Son Clave 的句法翻转", fill="#30261B", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "2-3 Son Clave 和 3-2 用的是同一组五个落点，但顺序翻转后，第一小节先收住、第二小节再展开。钢琴上要练的是起拍重心的改变。",
        fill="#68584A",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 872), "#fff3e7", "#dfc7a7", "第一小节", "2 击", "先留空间，像先回答或先铺垫", "#ba7a37"),
        ((574, 186, 986, 872), "#eef4ff", "#b2c5df", "第二小节", "3 击", "再把推进感和张力展开", "#476f9d"),
        ((1074, 186, 1486, 872), "#eef8f0", "#afccb5", "钢琴应用", "低音 + 和弦", "左手先稳住两击，再带出三击", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 288), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 374), desc, fill="#5f6870", font=font(28))

    bar1_hits = [212, 436]
    bar2_hits = [652, 790, 928]
    for idx, x in enumerate(bar1_hits, start=1):
        draw_hit(draw, x, 738, str(idx), "#c68445")
    for idx, x in enumerate(bar2_hits, start=3):
        draw_hit(draw, x, 738, str(idx), "#476f9d")

    chord_hits = [("Am", 1156, 738), ("Dm9", 1284, 682), ("E7", 1412, 738)]
    for label, x, y in chord_hits:
        draw_hit(draw, x, y, label, "#4f8a66")

    draw.text((118, 800), "示例低音：A ... E | A ... A ... E", fill="#ba7a37", font=font(28, bold=True))
    draw.text((620, 800), "口令：收 - 答 | 推 - 展 - 收", fill="#476f9d", font=font(28, bold=True))
    draw.text((1112, 800), "右手：Am - Dm9 - E7", fill="#4f8265", font=font(28, bold=True))

    draw.rounded_rectangle((92, 896, 1464, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (118, 907),
        "钢琴练法：先单手拍出 2-3，再只弹 A；稳定后改成左手 A-E | A-A-E，右手用 Am-Dm9-E7 体会第二小节更主动。",
        fill="#5f564b",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "piano-son-clave-23.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：2-3 Son Clave 的伴奏入口", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "2-3 Son Clave 常见于句子从第二小节开始加速展开的伴奏。吉他上要把第一小节的两击弹得克制，第二小节三击再逐步推开。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am | Dm9 E7 Am |。第一小节只放 2 次落点，第二小节再分成 3 次，让句子从后半段真正走起来。", fill="#223943", font=font(27, bold=True))
    draw.text((114, 260), "练习时先闷音做 2-3，再补和弦；如果第一小节就扫得太满，翻转后的呼吸感会直接消失。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "第一小节第一击，先把重心放稳。", "#2f8b61"),
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "第一小节第二击，仍然保持克制。", "#c97b3f"),
        ("Dm9", "x 5 3 5 5 5", [(3, 1, "1"), (2, 2, "2"), (3, 3, "3"), (3, 4, "4"), (3, 5, "4")], {0: "X"}, "第二小节第一击，开始把和声推开。", "#5c7db8"),
        ("E7", "0 2 0 1 0 0", [(2, 1, "2"), (1, 3, "1")], {0: "O", 2: "O", 4: "O", 5: "O"}, "最后一击给出回到 Am 的张力。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：先 2 后 3。先闷音拍稳，再换成低音加和弦；第二小节第三击要明显比第一小节更有前冲感。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-son-clave-23.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：2-3 Son Clave", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "2-3 Son Clave 仍然是五个固定落点，但顺序变成前一小节 2 击、后一小节 3 击。它不是新节奏，而是把句法重心翻到后半段。",
        fill="#655a4e",
        font=font(27),
    )

    lane_top = 220
    lane_left = 96
    cell_w = 150
    lane_h = 132
    row_gap = 54
    accent_fill = "#d9803d"
    base_fill = "#e6ecf4"

    rows = [
        ("第一小节 2 击", ["1", "&", "2", "&", "3", "&", "4", "&"], [2, 6], "先给出较克制的铺垫和回答感。"),
        ("第二小节 3 击", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 6], "再把三次主动落点放到后半段。"),
    ]

    for row_idx, (label, cells, accents, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 52), label, fill="#3f3428", font=font(32, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            fill = accent_fill if i in accents else base_fill
            outline = "#b86930" if i in accents else "#b7c2d0"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline, width=3)
            center_text(draw, (x0, y + 16, x1, y + 68), cell, "#ffffff" if i in accents else "#4a5766", font(26, bold=True))
            center_text(draw, (x0, y + 70, x1, y + 118), "hit" if i in accents else "rest", "#ffffff" if i in accents else "#667485", font(21, bold=i in accents))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(24))

    draw.rounded_rectangle((96, 676, 1404, 862), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((126, 714), "和 3-2 的区别", fill="#8b5a24", font=font(30, bold=True))
    draw.text((126, 766), "3-2 是先展开再回答；2-3 是先克制、后推进。五个落点相同，但起拍感觉和句子重心完全不同。", fill="#5f5547", font=font(26))
    draw.text((126, 812), "练习顺序：拍手 2-3 -> 单音根音 -> 加和弦。不要一上来就扫满八分音符。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "son-clave-23-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
