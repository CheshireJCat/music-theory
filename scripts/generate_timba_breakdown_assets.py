from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-30-timba-breakdown"
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
    img = Image.new("RGB", (1560, 1040), "#F4EBDD")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Breakdown", fill="#2E2419", font=font(52, bold=True))
    draw.text(
        (54, 102),
        "Breakdown 不是简单把乐器变少，而是主动抽空密度，让前面刚喊完的高位口号突然留出空间，为下一轮能量重组制造落差。",
        fill="#66584B",
        font=font(28),
    )

    draw.rounded_rectangle((74, 176, 1486, 354), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 212), "示例调性：Gm。前一小节还保留 horn hits 的高位亮点，下一小节把左手减到支点、右手减到稀疏短句，让 groove 先“蹲”一下。", fill="#8B5A2A", font=font(27, bold=True))
    draw.text((102, 262), "理解方式：不是没劲，而是故意抽掉厚度，让听众感觉下一轮要重新炸开。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    before_hits = [0, 3, 5, 7]
    breakdown_hits = [0, 4, 6]
    start_x = 146
    y_top = 484
    y_bottom = 650
    draw.text((96, 436), "上一轮高位口号", fill="#A4562B", font=font(30, bold=True))
    draw.text((96, 602), "breakdown 留空后落点", fill="#4A78AE", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#C97847" if idx in before_hits else "#E8E3D9"
        fill_bottom = "#5D88C5" if idx in breakdown_hits else "#E7EDF3"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    cards = [
        (92, 790, "#EEF3FF", "#AFC2E2", "先抽空再重组", "breakdown 要先让段落瘦下来，下一轮重启时才会有更明显的抬升感。"),
        (560, 790, "#FFF2DD", "#D9B57F", "左手只留支点", "钢琴左手别继续铺满，让低音和鼓组有空间把重心重新站稳。"),
        (1028, 790, "#EEF8F0", "#B8D5C0", "右手改成稀疏短句", "右手不再像 horn hits 那样整排齐奏，而是像在暗示“下一轮马上回来”。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 186), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 26, y + 22), title, fill="#33414C", font=font(32, bold=True))
        draw.text((x + 26, y + 82), body, fill="#5E6871", font=font(23))

    img.save(ASSET_DIR / "piano-timba-breakdown.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF4F2")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Breakdown 里的高位留空 comping", fill="#17313A", font=font(52, bold=True))
    draw.text(
        (56, 102),
        "吉他在 breakdown 里要学会克制。重点不是继续堆满和弦，而是在更少的出声里保留舞感，让下一轮 horn hits 或 moña 回来时更炸。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| Gm9 . C13 . | Ebmaj9 . D7alt . |。第一小节还能轻推，第二小节把和弦切成更少、更短的几块。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "判断标准：听感应该像“空间突然被打开”，而不是“伴奏突然散掉”。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "先轻推一轮。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "保持高位亮度。", "#C97B3F"),
        ("Ebmaj9", "x 6 8 7 6 x", [(1, 1, "1"), (3, 2, "5"), (2, 3, "7"), (1, 4, "3")], {0: "X", 5: "X"}, "进入 breakdown 后只短点一下。", "#5C7DB8"),
        ("D7alt", "x 5 4 5 6 x", [(1, 1, "1"), (1, 2, "3"), (1, 3, "b7"), (2, 4, "b9")], {0: "X", 5: "X"}, "留出回弹张力。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：推 - 留 - 推 - 留 | 点 - 停 - 点 - 停。Breakdown 的价值在于空间管理，不在于多弹几下。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-breakdown.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Breakdown", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Breakdown 常接在高位口号或爆点之后。它通过减法编配让 groove 暂时变瘦，同时保留明确脉冲，给下一次重启制造更大的反差。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("上一轮 horn hits", ["Bb", "-", "D", "F", "A", "C", "Eb", "-"], [0, 3, 5, 6], "上一轮还是高位密集口号。"),
        ("breakdown 层", ["Gm", "-", "-", "C13", "Eb", "-", "D7", "-"], [0, 3, 4, 6], "进入 breakdown 后改成更稀疏的支点和短句。"),
        ("身体口令", ["蹲", "留", "等", "点", "抬", "留", "勾", "回"], [0, 3, 4, 6], "听感像先蹲一下，再把身体重新推向下一轮高潮。"),
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
            state = "play" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：如果你能明显听到“高位口号喊完以后，段落突然变瘦但脉冲没断”，那就是 breakdown 的核心效果。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "timba-breakdown-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
