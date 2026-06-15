from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-04-cinquillo-rhythm"
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
    draw.ellipse((x - 32, y - 32, x + 32, y + 32), fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 24, y - 18, x + 24, y + 18), label, "#ffffff", font(18, bold=True))


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 116
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


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f4efe7")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Cinquillo Rhythm 的五击型重心", fill="#30261b", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Cinquillo 比 Habanera 更密集，常被概括为 3+1+2+2 的五击型。钢琴练习时要把每一次短促推动弹清楚，尤其别把中间的单独一下吞掉。",
        fill="#68584a",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 872), "#eef4ff", "#b2c5df", "左手低音", "A - A - E - A - E", "五次落点比 Habanera 更密", "#476f9d"),
        ((574, 186, 986, 872), "#fff3e7", "#dfc7a7", "节奏口令", "长 - 短 - 中 - 中", "抓住 3+1+2+2 的推力变化", "#ba7a37"),
        ((1074, 186, 1486, 872), "#eef8f0", "#afccb5", "听感结果", "更碎、更前冲", "适合制造连续扭动的律动", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 288), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 374), desc, fill="#5f6870", font=font(28))

    note_positions = [
        ("A", 152, 754, "#476f9d"),
        ("A", 258, 754, "#476f9d"),
        ("E", 364, 698, "#476f9d"),
        ("A", 470, 754, "#476f9d"),
        ("E", 576, 754, "#476f9d"),
        ("3", 652, 754, "#c68445"),
        ("1", 758, 698, "#c68445"),
        ("2", 864, 754, "#c68445"),
        ("2", 970, 754, "#c68445"),
        ("Am", 1156, 754, "#4f8a66"),
        ("G", 1242, 698, "#4f8a66"),
        ("E7", 1328, 754, "#4f8a66"),
        ("Am", 1414, 754, "#4f8a66"),
    ]
    for label, x, y, color in note_positions:
        draw_note(draw, x, y, label, color)

    draw.line((486, 738, 574, 738), fill="#9cadbf", width=7)
    draw.polygon([(574, 738), (552, 724), (552, 752)], fill="#9cadbf")
    draw.line((986, 738, 1074, 738), fill="#d1ab7a", width=7)
    draw.polygon([(1074, 738), (1052, 724), (1052, 752)], fill="#d1ab7a")

    draw.rounded_rectangle((92, 896, 1464, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (118, 907),
        "钢琴练法：右手保持 Am - G - E7 - Am，左手先只练 A - A - E - A - E，确保第三击比前后两组更像“插进来的一脚”。",
        fill="#5f564b",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "piano-cinquillo-rhythm.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：Cinquillo Rhythm 的低音与和弦循环", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上可把 Cinquillo 理解成更密集的低音加和弦模板。先守住 3+1+2+2 的五次击弦，再让和弦补在较长的位置上，律动会立刻更灵活。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am | G | E7 | Am |。拇指先做 A - A - E - A - E 的五击型低音，再用手指把和弦补在较长的落点上。", fill="#223943", font=font(27, bold=True))
    draw.text((114, 260), "和 Habanera 相比，这里中间多了一次单独推进。若这一击不够清楚，整条节奏就会又塌回普通切分伴奏。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "第一组 3 个八分音符的起点。", "#2f8b61"),
        ("G", "3 2 0 0 0 3", [(3, 0, "2"), (2, 1, "1"), (3, 5, "3")], {2: "O", 3: "O", 4: "O"}, "单独一下后换和声色彩。", "#c97b3f"),
        ("E7", "0 2 0 1 0 0", [(2, 1, "2"), (1, 3, "1")], {0: "O", 2: "O", 4: "O", 5: "O"}, "2+2 结尾把张力推起来。", "#5c7db8"),
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "回到主和弦，准备下一轮。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    for start, end, color in [(392, 418, "#95a1a7"), (706, 716, "#b9986f"), (1020, 1030, "#95a1a7")]:
        draw.line((start, 652, end, 652), fill=color, width=7)
        draw.polygon([(end, 652), (end - 18, 640), (end - 18, 664)], fill=color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：3 + 1 + 2 + 2。先数清五次击弦，再决定哪些位置留长；不要把所有音都扫成一样重。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-cinquillo-rhythm.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "节奏结构图：Cinquillo Rhythm", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Cinquillo 是从 Tresillo / Habanera 再往前一步的五击型模板。重点不是死记数字，而是听出它比 Habanera 多出来的那一下如何让律动更密、更前冲。",
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
        ("Habanera 参考", ["起", "拖", "空", "推", "拖", "空", "落", "留"], [0, 3, 6], "四击感，舞步更宽。"),
        ("Cinquillo 核心", ["1", "2", "3", "4", "5", "6", "7", "8"], [0, 3, 4, 6, 7], "五击感，常概括为 3+1+2+2。"),
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
    draw.text((126, 766), "1. 先念 3+1+2+2  2. 再用单音弹五次击打  3. 最后把和弦放进较长的落点", fill="#5f5547", font=font(26))
    draw.text((126, 812), "常见误区：只听到切分，却没把中间那一下单独凸出来。没有那次“额外推动”，Cinquillo 的辨识度就会明显下降。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "cinquillo-rhythm-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
