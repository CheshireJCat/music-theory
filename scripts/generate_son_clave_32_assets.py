from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-05-son-clave-32"
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
    center_text(draw, (x - 22, y - 16, x + 22, y + 16), label, "#ffffff", font(18, bold=True))


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
    draw.text((52, 38), "钢琴图：3-2 Son Clave 的两小节骨架", fill="#30261B", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "3-2 Son Clave 不是把音弹得更密，而是把两小节里的 3 击和 2 击重心分成前后两组。钢琴上先把落点数稳，再把低音和和弦放进去。",
        fill="#68584A",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 872), "#eef4ff", "#b2c5df", "第一小节", "3 击", "先建立方向感和舞步重心", "#476f9d"),
        ((574, 186, 986, 872), "#fff3e7", "#dfc7a7", "第二小节", "2 击", "留出空间，形成回答感", "#ba7a37"),
        ((1074, 186, 1486, 872), "#eef8f0", "#afccb5", "钢琴应用", "低音 + 和弦", "左手守 clave，右手补和声", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 288), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 374), desc, fill="#5f6870", font=font(28))

    bar1_hits = [152, 290, 428]
    bar2_hits = [652, 876]
    for idx, x in enumerate(bar1_hits, start=1):
        draw_hit(draw, x, 738, str(idx), "#476f9d")
    for idx, x in enumerate(bar2_hits, start=4):
        draw_hit(draw, x, 738, str(idx), "#c68445")

    chord_hits = [("Am", 1156, 738), ("G", 1284, 682), ("E7", 1412, 738)]
    for label, x, y in chord_hits:
        draw_hit(draw, x, y, label, "#4f8a66")

    draw.text((118, 800), "示例低音：A ... A ... E | A ... E", fill="#476f9d", font=font(28, bold=True))
    draw.text((620, 800), "口令：强 - 回答 - 推 | 回 - 收", fill="#ba7a37", font=font(28, bold=True))
    draw.text((1112, 800), "右手：Am - G - E7", fill="#4f8265", font=font(28, bold=True))

    draw.rounded_rectangle((92, 896, 1464, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (118, 907),
        "钢琴练法：先单手拍出 3-2，两小节里只弹 A；稳定后再变成左手 A-E 低音、右手 Am-G-E7 和弦。",
        fill="#5f564b",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "piano-son-clave-32.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：3-2 Son Clave 的和弦入口", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上常把 3-2 Son Clave 放进分解或闷音伴奏里。关键是前一小节三次落点更主动，后一小节两次落点像回答，不能全扫平均八分音符。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am | G E7 |。前一小节弹 3 次，后一小节弹 2 次；拇指可以先守低音，手指只在落点补和弦。", fill="#223943", font=font(27, bold=True))
    draw.text((114, 260), "如果第二小节还继续挤成三次，听感就会失去 clave 的前后呼应，只剩普通拉丁切分。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "第一小节的起点和主和弦中心。", "#2f8b61"),
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "第三击仍在主和弦里，先把舞步站稳。", "#c97b3f"),
        ("G", "3 2 0 0 0 3", [(3, 0, "2"), (2, 1, "1"), (3, 5, "3")], {2: "O", 3: "O", 4: "O"}, "第二小节第一击，像回答。", "#5c7db8"),
        ("E7", "0 2 0 1 0 0", [(2, 1, "2"), (1, 3, "1")], {0: "O", 2: "O", 4: "O", 5: "O"}, "最后一击给出回到 Am 的张力。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：3 击在前一小节，2 击在后一小节。先闷音拍清楚，再换成分解或扫弦，别把两小节弹成平均五次。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-son-clave-32.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：3-2 Son Clave", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Son Clave 是很多拉丁伴奏的核心骨架。3-2 表示前一小节有 3 次落点，后一小节有 2 次落点，重点在两小节之间的呼应关系。",
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
        ("第一小节 3 击", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 6], "先抛出三次主动落点。"),
        ("第二小节 2 击", ["1", "&", "2", "&", "3", "&", "4", "&"], [2, 6], "再用两次回答收束。"),
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
    draw.text((126, 714), "应用顺序", fill="#8b5a24", font=font(30, bold=True))
    draw.text((126, 766), "1. 先拍 3-2  2. 再只弹根音  3. 最后把和弦放进 3 击和 2 击的落点", fill="#5f5547", font=font(26))
    draw.text((126, 812), "和 Cinquillo 的区别：Cinquillo 更像单小节里的五击型，Son Clave 则强调两小节的前后问答结构。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "son-clave-32-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
