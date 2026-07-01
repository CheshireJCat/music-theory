from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-07-01-timba-pedal-breakdown"
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
    img = Image.new("RGB", (1560, 1040), "#F4ECDD")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Pedal Breakdown", fill="#2E2419", font=font(52, bold=True))
    draw.text(
        (54, 102),
        "Pedal Breakdown 是在 breakdown 已经抽空的基础上，再固定一个低音支点，让空间没有塌掉，反而更集中地积蓄回弹张力。",
        fill="#66584B",
        font=font(28),
    )

    draw.rounded_rectangle((74, 176, 1486, 354), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 212), "示例调性：Gm。左手持续握住 D 这个属音支点，右手把上一课的稀疏落点继续缩成更像信号灯的短句。", fill="#8B5A2A", font=font(27, bold=True))
    draw.text((102, 262), "理解方式：不是随便留空，而是在留空的同时给听众一个始终没消失的低音焦点。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    pedal_hits = [0, 4, 6]
    right_hits = [1, 5]
    start_x = 146
    y_top = 484
    y_bottom = 650
    draw.text((96, 436), "左手持续 D pedal", fill="#A4562B", font=font(30, bold=True))
    draw.text((96, 602), "右手稀疏提示短句", fill="#4A78AE", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#C97847" if idx in pedal_hits else "#EEE8DF"
        fill_bottom = "#5D88C5" if idx in right_hits else "#E7EDF3"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    cards = [
        (92, 790, "#EEF3FF", "#AFC2E2", "低音别乱换", "pedal breakdown 的根本是支点持续存在。左手宁可少，也不要不停改根音。"),
        (560, 790, "#FFF2DD", "#D9B57F", "右手像发信号", "右手只保留两三个关键短句，像提醒整队“还没结束，下一轮要回来了”。"),
        (1028, 790, "#EEF8F0", "#B8D5C0", "张力更集中", "普通 breakdown 是抽空；pedal breakdown 是抽空但不失焦，让等待感更黏。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 186), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 26, y + 22), title, fill="#33414C", font=font(32, bold=True))
        draw.text((x + 26, y + 82), body, fill="#5E6871", font=font(23))

    img.save(ASSET_DIR / "piano-timba-pedal-breakdown.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF4F2")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Pedal Breakdown 的高位切片", fill="#17313A", font=font(52, bold=True))
    draw.text(
        (56, 102),
        "吉他在 pedal breakdown 里既不能把空间填满，也不能完全失去方向。高位和弦像闪灯一样出现，低音支点则由整队共同暗示。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：低音想象持续 D，和声切片用 | Gm9/D . . . | Ebmaj9/D . D7alt/D . |。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "判断标准：高位出声更少，但耳朵始终觉得“属音还挂着，段落还在蓄力”。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9/D", "x 5 3 3 3 5", [(1, 1, "5"), (1, 2, "1"), (1, 3, "b7"), (1, 4, "9"), (3, 5, "b3")], {0: "X"}, "保留 Gm 色彩，但心里听 D。", "#2F8B61"),
        ("D pedal", "10 12 12 x x x", [(1, 0, "1"), (3, 1, "5"), (3, 2, "1")], {3: "X", 4: "X", 5: "X"}, "把属音支点听稳。", "#C97B3F"),
        ("Ebmaj9/D", "x 5 5 7 6 6", [(1, 1, "7"), (1, 2, "3"), (3, 3, "6"), (2, 4, "1"), (2, 5, "5")], {0: "X"}, "上方和声变了，低音焦点不变。", "#5C7DB8"),
        ("D7alt/D", "x 5 4 5 6 x", [(1, 1, "1"), (1, 2, "3"), (1, 3, "b7"), (2, 4, "b9")], {0: "X", 5: "X"}, "给回弹前的最终拉力。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：留 - 点 - 留 - 等 | 点 - 留 - 勾 - 停。少弹不等于没方向，pedal 要让每一下都围着同一个重心。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-pedal-breakdown.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Pedal Breakdown", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "和普通 breakdown 相比，Pedal Breakdown 会在下方固定一个持续支点。上层虽然抽空，但身体仍然会被同一个低音焦点牵住。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("低音 pedal", ["D", "-", "-", "D", "-", "-", "D", "-"], [0, 3, 6], "低音支点一直把耳朵拴在属音上。"),
        ("上层短句", ["-", "Gm", "-", "-", "-", "Eb", "-", "D7"], [1, 5, 7], "上层只偶尔发声，但每次都像围着 pedal 转。"),
        ("身体口令", ["挂", "点", "等", "挂", "留", "勾", "挂", "回"], [0, 1, 3, 5, 6, 7], "听感像一直憋着重心，等下一轮真正冲回主句。"),
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
            state = "hold" if row_idx == 0 and i in active else ("play" if i in active else "rest")
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：如果段落已经变瘦，但你仍然清楚感觉到“同一个属音重心一直吊着不放”，那就是 pedal breakdown。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "timba-pedal-breakdown-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
