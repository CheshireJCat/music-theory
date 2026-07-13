from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-07-13-timba-section-entry-lock"
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
    img = Image.new("RGB", (1560, 1040), "#F5EFE6")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Section Entry Lock", fill="#2E2419", font=font(48, bold=True))
    draw.text(
        (54, 102),
        "今天推进到 section entry lock：句尾 cue 已经会发出后，下一步是让钢琴和吉他在下一轮第 1 拍一起落地，把新段落锁成整队齐进的着陆点。",
        fill="#66584B",
        font=font(27),
    )

    draw.rounded_rectangle((74, 176, 1486, 356), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 214), "示例调性：Gm。左手持续锁住 marcha，右手在第 8 格做短 cue，下一轮第 1 格与左手一起把入口钉稳。", fill="#8B5A2A", font=font(24, bold=True))
    draw.text((102, 268), "判断标准：cue 是“说进来”，entry lock 是“大家真的一起进并且站稳”；重点从提示转为着陆。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&", "1"]
    left_hits = [0, 3, 6, 8]
    right_marcha = [1, 3, 5]
    cue_zone = [7]
    lock_zone = [8]
    start_x = 118
    y_top = 484
    y_mid = 650
    y_bottom = 816
    draw.text((70, 436), "左手支点", fill="#486FA8", font=font(30, bold=True))
    draw.text((70, 602), "右手 marcha", fill="#2E7D59", font=font(30, bold=True))
    draw.text((70, 768), "入口动作", fill="#B4622F", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 136
        fill_top = "#5D88C5" if idx in left_hits else "#E7EDF3"
        fill_mid = "#3E9A72" if idx in right_marcha else "#E6F2EB"
        if idx in cue_zone:
            fill_bottom = "#8A8F98"
        elif idx in lock_zone:
            fill_bottom = "#C97847"
        else:
            fill_bottom = "#EEE8DF"
        draw_pill(draw, (x, y_top, x + 102, y_top + 56), label, fill_top, "#FFFFFF", size=23)
        draw_pill(draw, (x, y_mid, x + 102, y_mid + 56), label, fill_mid, "#FFFFFF", size=23)
        draw_pill(draw, (x, y_bottom, x + 102, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=23)

    center_text(draw, (1068, y_bottom + 8, 1160, y_bottom + 48), "cue", "#FFFFFF", font(20, bold=True))
    center_text(draw, (1204, y_bottom + 8, 1310, y_bottom + 48), "一起落", "#FFFFFF", font(20, bold=True))

    cards = [
        (92, 900, "#EEF3FF", "#AFC2E2", "先提示", "第 8 格 cue 要短而清楚，让下一拍的合奏落点有统一目标。"),
        (560, 900, "#EEF8F0", "#B8D5C0", "再着陆", "下一轮第 1 拍必须和低音、和弦一起站稳，不能只打一记热闹重音。"),
        (1028, 900, "#FFF2DD", "#D9B57F", "锁成一队", "section entry lock 的重点是多人同步着陆，听感像编配重新列队。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 110), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 22, y + 14), title, fill="#33414C", font=font(27, bold=True))
        draw.text((x + 22, y + 54), body, fill="#5E6871", font=font(19))

    img.save(ASSET_DIR / "piano-timba-section-entry-lock.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF4F0")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Timba Section Entry Lock", fill="#17313A", font=font(48, bold=True))
    draw.text(
        (56, 102),
        "吉他上的重点是先用一句短 cue 对齐入口，再在下一轮第 1 拍和钢琴一起把和弦切实落下，让新段落不飘不散。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| Gm9 . C13 . Gm9 [cue] | -> | Gm9 [lock] ... |。上一课先讲“说进来”，今天讲“说完以后怎样一起站稳”。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "手感标准：cue 像口令，lock 像全队同时落地；第 1 拍要短、齐、稳，而不是拖成长扫。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "常态 marcha 位。", "#2F8B61"),
        ("Cue", "短促口令", [(2, 1, "cue"), (2, 3, "!"), (2, 4, "in")], {0: "X", 5: "X"}, "先把入口说清楚。", "#A15B6B"),
        ("Lock", "下一轮 1", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "第 1 拍齐落。", "#C97B3F"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "再继续推进。", "#5C7DB8"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：推 - 推 - 点 - 落。最后一步不是更长，而是和全队一起更稳地站到下一轮第 1 拍上。",
        fill="#4D5F68",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-section-entry-lock.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Section Entry Lock", fill="#2D261D", font=font(46, bold=True))
    draw.text(
        (56, 104),
        "这一步承接 Timba Cross-Stick Cue：上一课解决“如何发出入口提示”，今天解决“提示之后，怎样让钢琴和吉他在下一轮真正锁成统一着陆点”。",
        fill="#655A4E",
        font=font(25),
    )

    lane_top = 232
    lane_left = 80
    cell_w = 128
    lane_h = 118
    row_gap = 48

    rows = [
        ("时间格", ["1", "&", "2", "&", "3", "&", "4", "&", "1"], [0, 2, 4, 6, 8], "第 8 格发出 cue，下一轮第 1 格完成全队着陆。"),
        ("动作层", ["稳", "-", "推", "-", "稳", "-", "收", "cue", "lock"], [7, 8], "从口令过渡到合奏落点，真正核心是第 1 拍的同步站稳。"),
        ("听感层", ["滚", "留", "推", "留", "滚", "留", "含", "进", "齐"], [7, 8], "如果最后只听见提示却没有齐整着陆，就还没形成 section entry lock。"),
    ]

    for row_idx, (label, cells, active, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 48), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 12
            if row_idx == 0:
                active_fill = "#5E88C6"
                outline = "#5E759E"
            elif row_idx == 1:
                active_fill = "#C8823F"
                outline = "#B76E31"
            else:
                active_fill = "#3E9A72"
                outline = "#2E7D59"
            txt = "#FFFFFF" if i in active else "#4A5766"
            fill = active_fill if i in active else "#E6ECF4"
            if row_idx == 1 and i == 7:
                fill = "#8A8F98"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(23, bold=True))
            state = "active" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：cue 负责指向入口，lock 负责让所有人一起站上入口；如果只有“进”的感觉没有“齐”的感觉，就还在上一课。", fill="#5F5547", font=font(22, bold=True))

    img.save(ASSET_DIR / "timba-section-entry-lock-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
