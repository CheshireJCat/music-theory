from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-24-timba-piano-marcha"
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


def draw_pill(draw, box, text, fill, outline, text_fill="#FFFFFF", size=24):
    draw.rounded_rectangle(box, 18, fill=fill, outline=outline, width=3)
    center_text(draw, box, text, text_fill, font(size, bold=True))


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 116
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 304, y + 470), 28, fill="#FFFDF9", outline="#D2D6DB", width=3)
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
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#FFFFFF", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#FFFFFF", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#56656F", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 246, sx + 12, grid_top + 278), name, "#56656F", font(16, bold=True))

    draw.text((x + 28, y + 404), footnote, fill="#52656E", font=font(17))


def save_piano_chart():
    img = Image.new("RGB", (1560, 1040), "#F7F0E6")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Piano Marcha 的固定推进", fill="#2F2418", font=font(52, bold=True))
    draw.text(
        (54, 102),
        "Piano marcha 是 Timba 里钢琴把 bell、anticipation 和和声入口组织成固定推进型的方式。它不是随手分解和弦，而是专门负责把段落持续往前拽。",
        fill="#66584B",
        font=font(28),
    )

    draw.rounded_rectangle((74, 176, 1486, 354), 26, fill="#FFF9F1", outline="#DCC8A8", width=3)
    draw.text((102, 212), "示例调性：Gm。两小节骨架：| Gm9 . C13 . | Ebmaj9 . D7alt . |", fill="#8B5A2A", font=font(28, bold=True))
    draw.text((102, 262), "思路：左手管和声入口，右手用短促双音和 anticipations 维持“咬住前方”的感觉。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    left_hand = [0, 3, 4, 7]
    right_hand = [1, 3, 5, 6, 7]
    start_x = 146
    y_top = 484
    y_bottom = 650
    draw.text((96, 436), "左手和声入口", fill="#8C5E2E", font=font(30, bold=True))
    draw.text((96, 602), "右手 marcha 亮点", fill="#436B9A", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#CD8544" if idx in left_hand else "#E8E3D9"
        fill_bottom = "#5D88C5" if idx in right_hand else "#E7EDF3"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    cards = [
        (92, 790, "#FFF2DD", "#D9B57F", "先稳住", "第一层先让左手把和声支点站稳，右手不要急着填满。"),
        (560, 790, "#EEF3FF", "#AFC2E2", "再前推", "右手重点落在 & 与后半拍，制造 anticipations。"),
        (1028, 790, "#EEF8F0", "#B8D5C0", "持续咬拍", "每轮都像往下一拍伸手，不是横着铺开。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 186), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 26, y + 22), title, fill="#33414C", font=font(32, bold=True))
        draw.text((x + 26, y + 82), body, fill="#5E6871", font=font(23))

    img.save(ASSET_DIR / "piano-timba-piano-marcha.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EDF3F4")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：围绕 Piano Marcha 的高位 comping", fill="#18313A", font=font(52, bold=True))
    draw.text(
        (56, 102),
        "吉他这里不是另起炉灶，而是配合钢琴 marcha 留出主推进位。做法是高位短促、少量补点，在钢琴 anticipations 之间帮它抬亮而不抢主线。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| Gm9 . C13 . | Ebmaj9 . D7alt . |。吉他把出声点压缩成短刺点，主要补在钢琴右手音尾之后。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "判断标准：钢琴像发动机主轴，吉他像高频火花。两者一起推，但主推进感必须仍来自 piano marcha。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "先留空间给钢琴起跑。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "在后半拍补亮点。", "#C97B3F"),
        ("Ebmaj9", "x 6 5 7 6 x", [(1, 1, "1"), (1, 2, "3"), (2, 3, "7"), (1, 4, "9")], {0: "X", 5: "X"}, "换段时抬亮颜色。", "#5C7DB8"),
        ("D7alt", "x 5 4 5 6 x", [(1, 1, "1"), (1, 2, "3"), (1, 3, "b7"), (2, 4, "b9")], {0: "X", 5: "X"}, "把下一轮继续点燃。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：闷 - 点 - 闷 - 点 | 闷 - 点 - 点 - 闷。目标不是铺满，而是让钢琴的 marcha 更清楚。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-piano-marcha.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Piano Marcha", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Piano marcha 的任务，是把和声、落点与 anticipations 固定成一个能持续推段落的钢琴型。它比单纯 bell 更像段落发动机。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("低层支点", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 4, 7], "左手负责和声支点与提早切入。"),
        ("高层亮点", ["1", "&", "2", "&", "3", "&", "4", "&"], [1, 3, 5, 6, 7], "右手主要落在反拍与后半拍，持续往前咬。"),
        ("身体口令", ["站", "提", "留", "推", "顶", "追", "咬", "冲"], [0, 1, 3, 5, 6, 7], "整条型必须像在把下一拍拉近。"),
    ]

    for row_idx, (label, cells, active, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 48), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            active_fill = "#C8823F" if row_idx == 0 else "#5E88C6"
            outline = "#B76E31" if row_idx == 0 else "#5E759E"
            txt = "#FFFFFF" if i in active else "#4A5766"
            fill = active_fill if i in active else "#E6ECF4"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(24, bold=True))
            state = "hit" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：这条型一循环起来，听感应该是“段落被持续往前拖着跑”，而不是静态分解和弦。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "timba-piano-marcha-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
