from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-01-tresillo-ostinato"
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


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f7f1e8")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Tresillo Ostinato 的 3+3+2 切分模板", fill="#30261b", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Tresillo 是最常见的固定切分节奏之一。把 8 个八分音符分成 3 + 3 + 2，循环就会同时保留稳定骨架和明显的律动推力。",
        fill="#68584a",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 872), "#eef4ff", "#b2c5df", "左手低音", "A - A - A | G - G - G | F - F", "音高可简化，关键是节奏分组", "#476f9d"),
        ((574, 186, 986, 872), "#fff3e7", "#dfc7a7", "拍内分组", "3 + 3 + 2", "一小节 8 个八分音符，重音落在 1 / 4 / 7", "#ba7a37"),
        ((1074, 186, 1486, 872), "#eef8f0", "#afccb5", "听感结果", "滚动推进", "不像平均切分那样板正", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 288), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 374), desc, fill="#5f6870", font=font(28))

    note_positions = [
        ("1", 152, 726, "#476f9d"),
        ("4", 238, 788, "#476f9d"),
        ("7", 324, 726, "#476f9d"),
        ("8", 410, 788, "#476f9d"),
        ("3", 652, 726, "#c68445"),
        ("3", 738, 788, "#c68445"),
        ("2", 824, 726, "#c68445"),
        ("A", 1156, 726, "#4f8a66"),
        ("G", 1242, 788, "#4f8a66"),
        ("F", 1328, 726, "#4f8a66"),
        ("E", 1414, 788, "#4f8a66"),
    ]
    for note, x, y, color in note_positions:
        draw_note(draw, x, y, note, color)

    draw.line((486, 738, 574, 738), fill="#9cadbf", width=7)
    draw.polygon([(574, 738), (552, 724), (552, 752)], fill="#9cadbf")
    draw.line((986, 738, 1074, 738), fill="#d1ab7a", width=7)
    draw.polygon([(1074, 738), (1052, 724), (1052, 752)], fill="#d1ab7a")

    draw.rounded_rectangle((92, 896, 1464, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (118, 907),
        "钢琴练法：右手数 “1-2-3 1-2-3 1-2”，左手只在每组第一个八分音符上强调。先拍手，再把 A 小调和弦加到右手。",
        fill="#5f564b",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "piano-tresillo-ostinato.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：Tresillo Ostinato 的和弦循环", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上最容易上手的做法，是保留常见和弦进行，再把扫弦或拨弦重音固定成 3+3+2。节奏一稳定，整段就会立刻有拉丁或流行律动感。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "先保持右手不断数 8 个八分音符，再只强调第 1、4、7 个位置。不要急着加复杂分解，先把 3+3+2 的身体感练稳。", fill="#223943", font=font(27, bold=True))
    draw.text((114, 260), "建议入门循环：| Am | G | F | E |。拇指管低音，食指或扫弦动作在每组第一个八分音符上稍微加重，就能清楚听到 Tresillo。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "第 1 组的起点，用来建立重音。", "#2f8b61"),
        ("G", "3 2 0 0 0 3", [(3, 0, "2"), (2, 1, "1"), (3, 5, "3")], {2: "O", 3: "O", 4: "O"}, "第 2 组继续 3 个八分音符。", "#c97b3f"),
        ("F", "1 3 3 2 1 1", [(1, 0, "1"), (3, 1, "3"), (3, 2, "4"), (2, 3, "2"), (1, 4, "1"), (1, 5, "1")], {}, "最后 2 个八分音符更像收束。", "#5c7db8"),
        ("E", "0 2 2 1 0 0", [(2, 1, "2"), (2, 2, "3"), (1, 3, "1")], {0: "O", 4: "O", 5: "O"}, "E 把循环拉回下一轮。", "#a15b6b"),
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
        "右手口令：强-弱-弱，强-弱-弱，强-弱。数 “1-2-3 1-2-3 1-2”，把重音稳定放在每组第一个八分音符上。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-tresillo-ostinato.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "节奏结构图：Tresillo Ostinato", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Tresillo 的重点是把 8 个八分音符固定分成 3 + 3 + 2。它比普通反拍更具体，所以特别适合从“泛化切分”进一步落到可直接演奏的模板。",
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
        ("平均 8 个八分音符", ["1", "2", "3", "4", "5", "6", "7", "8"], [0, 2, 4, 6], "平均分布，听感比较直。"),
        ("Tresillo 3+3+2", ["1", "2", "3", "4", "5", "6", "7", "8"], [0, 3, 6], "重音落在第 1、4、7 个八分音符上。"),
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
            center_text(draw, (x0, y + 16, x1, y + 68), cell, "#ffffff" if i in accents else "#4a5766", font(28, bold=True))
            center_text(draw, (x0, y + 70, x1, y + 118), "accent" if i in accents else "flow", "#ffffff" if i in accents else "#667485", font(22, bold=i in accents))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(24))

    draw.rounded_rectangle((96, 676, 1404, 862), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((126, 714), "应用顺序", fill="#8b5a24", font=font(30, bold=True))
    draw.text((126, 766), "1. 先拍出 3+3+2  2. 再把低音或和弦套进去  3. 最后让旋律学会避开每次都落在重音上", fill="#5f5547", font=font(26))
    draw.text((126, 812), "常见误区：把 Tresillo 理解成越快越好。真正重要的是分组稳定，哪怕慢速也要听得出 3 + 3 + 2。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "tresillo-ostinato-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
