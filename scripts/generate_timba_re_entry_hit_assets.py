from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-07-02-timba-re-entry-hit"
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
    img = Image.new("RGB", (1560, 1040), "#F6ECDE")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Re-Entry Hit", fill="#2E2419", font=font(52, bold=True))
    draw.text(
        (54, 102),
        "Re-Entry Hit 发生在 pedal breakdown 已经把张力悬住之后。重点不是随便加一拍，而是整队用统一重击把能量重新掀回主循环。",
        fill="#66584B",
        font=font(28),
    )

    draw.rounded_rectangle((74, 176, 1486, 354), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 212), "示例调性：Gm。前半拍继续听 D pedal，重返点用 Gm9 与 C13 的统一重击，把前一课的“悬着”变成今天的“砸回主循环”。", fill="#8B5A2A", font=font(26, bold=True))
    draw.text((102, 262), "判断标准：听感必须像门突然被撞开，而不是只是多弹了一个和弦。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    pedal_zone = [0, 3]
    hit_zone = [4, 6]
    resolve_zone = [7]
    start_x = 146
    y_top = 484
    y_mid = 650
    y_bottom = 816
    draw.text((96, 436), "pedal 悬挂区", fill="#A4562B", font=font(30, bold=True))
    draw.text((96, 602), "统一 re-entry hit", fill="#4A78AE", font=font(30, bold=True))
    draw.text((96, 768), "回到 marcha 推进", fill="#2E7D59", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#C97847" if idx in pedal_zone else "#EEE8DF"
        fill_mid = "#5D88C5" if idx in hit_zone else "#E7EDF3"
        fill_bottom = "#3E9A72" if idx in resolve_zone else "#E6F2EB"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_mid, x + 108, y_mid + 56), label, fill_mid, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    cards = [
        (92, 900, "#EEF3FF", "#AFC2E2", "先悬再砸", "没有前面的 pedal 悬挂，re-entry hit 就只剩普通重音，缺少真正的回归冲击。"),
        (560, 900, "#FFF2DD", "#D9B57F", "左手别抢拍", "左手先守住 D，再在回击点与右手同时落下，形成整队统一入口。"),
        (1028, 900, "#EEF8F0", "#B8D5C0", "回击后要接推进", "重击不是终点，砸回去以后要立刻接回 marcha 或主 groove。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 110), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 22, y + 14), title, fill="#33414C", font=font(27, bold=True))
        draw.text((x + 22, y + 54), body, fill="#5E6871", font=font(19))

    img.save(ASSET_DIR / "piano-timba-re-entry-hit.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF4F2")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Re-Entry Hit 的回击和弦", fill="#17313A", font=font(52, bold=True))
    draw.text(
        (56, 102),
        "吉他在 re-entry hit 里要从 pedal breakdown 的稀疏闪灯，瞬间切到整齐、短促、同口气的集体重击，然后立刻接回推进型 comping。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| D pedal . . . | Gm9 hit . C13 hit . |。先吊住重心，再用两个短促和弦把段落砸回主循环。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "手感标准：每次 hit 都像全队一起喊“回来”，不是平常的碎切 comping。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("D pedal", "10 12 12 x x x", [(1, 0, "1"), (3, 1, "5"), (3, 2, "1")], {3: "X", 4: "X", 5: "X"}, "先把支点挂住。", "#C97B3F"),
        ("Gm9 hit", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "第一下像撞门。", "#2F8B61"),
        ("C13 hit", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "第二下把推进接稳。", "#5C7DB8"),
        ("Gm9 return", "x 10 12 10 11 x", [(1, 1, "1"), (3, 2, "5"), (1, 3, "b7"), (2, 4, "9")], {0: "X", 5: "X"}, "回到高位 marcha。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：挂 - 留 - 等 - 吊 | 砸 - 停 - 砸 - 回。关键不在大力，而在全队同时、短促、干净地回到同一个入口。",
        fill="#4D5F68",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-re-entry-hit.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Re-Entry Hit", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Re-Entry Hit 的任务，是把 pedal breakdown 累积出来的等待感，转换成一次统一回击，再把整队推进重新锁回主 groove。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("pedal 悬挂", ["D", "-", "-", "D", "-", "-", "-", "-"], [0, 3], "前半段先吊住属音重心。"),
        ("回击入口", ["-", "-", "-", "-", "Gm9", "-", "C13", "-"], [4, 6], "回击点必须整齐短促，像整队一起撞门。"),
        ("回归动作", ["-", "-", "-", "-", "砸", "停", "砸", "回"], [4, 6, 7], "最后一个“回”要立刻把身体送回 marcha。"),
    ]

    for row_idx, (label, cells, active, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 48), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            active_fill = "#C8823F" if row_idx == 0 else "#5E88C6"
            if row_idx == 2:
                active_fill = "#3E9A72"
            outline = "#B76E31" if row_idx == 0 else "#5E759E"
            if row_idx == 2:
                outline = "#2E7D59"
            txt = "#FFFFFF" if i in active else "#4A5766"
            fill = active_fill if i in active else "#E6ECF4"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(24, bold=True))
            state = "play" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：如果你能清楚听到“前面一直吊着，接着整队一起撞回来，并且马上接回推进”，那就是有效的 re-entry hit。", fill="#5F5547", font=font(23, bold=True))

    img.save(ASSET_DIR / "timba-re-entry-hit-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
