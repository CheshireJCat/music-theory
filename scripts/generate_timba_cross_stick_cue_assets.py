from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-07-10-timba-cross-stick-cue"
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
    img = Image.new("RGB", (1560, 1040), "#F3EEE4")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Cross-Stick Cue", fill="#2E2419", font=font(48, bold=True))
    draw.text(
        (54, 102),
        "今天推进到 cross-stick cue：在句尾已经会做 release accent 之后，再加入更短、更干脆的提示音，专门给下一轮入口或编配转折打信号。",
        fill="#66584B",
        font=font(27),
    )

    draw.rounded_rectangle((74, 176, 1486, 356), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 214), "示例调性：Gm。左手持续锁住 marcha，右手在第 8 格给出短促 cue，像鼓手 cross-stick 一样告诉乐队“入口在这”。", fill="#8B5A2A", font=font(24, bold=True))
    draw.text((102, 268), "判断标准：cue 要比 release accent 更短、更清楚；重点不在延长，而在一记明白的提示。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    left_hits = [0, 3, 6]
    marcha_hits = [1, 3, 5]
    prep_zone = [6]
    cue_zone = [7]
    start_x = 146
    y_top = 484
    y_mid = 650
    y_bottom = 816
    draw.text((96, 436), "左手支点", fill="#486FA8", font=font(30, bold=True))
    draw.text((96, 602), "右手 marcha", fill="#2E7D59", font=font(30, bold=True))
    draw.text((96, 768), "cue 动作", fill="#B4622F", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#5D88C5" if idx in left_hits else "#E7EDF3"
        fill_mid = "#3E9A72" if idx in marcha_hits else "#E6F2EB"
        if idx in prep_zone:
            fill_bottom = "#8A8F98"
        elif idx in cue_zone:
            fill_bottom = "#C97847"
        else:
            fill_bottom = "#EEE8DF"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_mid, x + 108, y_mid + 56), label, fill_mid, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    center_text(draw, (1120, y_bottom + 8, 1210, y_bottom + 48), "收", "#FFFFFF", font(22, bold=True))
    center_text(draw, (1280, y_bottom + 8, 1390, y_bottom + 48), "短提示", "#FFFFFF", font(20, bold=True))

    cards = [
        (92, 900, "#EEF3FF", "#AFC2E2", "更短", "cue 不是再拉长一个 accent，而是用短促音头给大家一个明确入口。"),
        (560, 900, "#EEF8F0", "#B8D5C0", "更准", "要准落在句尾提示位，否则乐队只会听见重拍，不会听见指令。"),
        (1028, 900, "#FFF2DD", "#D9B57F", "更像信号", "它的任务是说“这里要进了”，不是说“这里要更大声”。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 110), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 22, y + 14), title, fill="#33414C", font=font(27, bold=True))
        draw.text((x + 22, y + 54), body, fill="#5E6871", font=font(19))

    img.save(ASSET_DIR / "piano-timba-cross-stick-cue.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EDF4F1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Timba Cross-Stick Cue", fill="#17313A", font=font(48, bold=True))
    draw.text(
        (56, 102),
        "吉他上的重点是让最后一下像一个干脆的口令：前面 comping 继续锁紧，句尾用一记短促和弦或闷击把下一轮入口说清楚。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| Gm9 . C13 . Gm9 [prep] [cue] |。cue 要比昨天的 release accent 更短，像鼓里的 cross-stick 点头。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "手感标准：不是扫出更长的尾巴，而是让最后一下更像“啪”的提示，带着下一轮一起进。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "稳定 comping 起点。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "句尾准备提示。", "#C97B3F"),
        ("Prep", "轻压收紧", [(2, 1, "PM"), (2, 2, "PM"), (2, 3, "PM")], {0: "X", 5: "X"}, "先把能量含住。", "#5C7DB8"),
        ("Cue", "短促提示", [(2, 1, "cue"), (2, 3, "!"), (2, 4, "in")], {0: "X", 5: "X"}, "清楚说出入口。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：推 - 推 - 吸 - 点。最后一步像一句极短的 cue，落下后整段 groove 立刻知道下一轮怎么进。",
        fill="#4D5F68",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-cross-stick-cue.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Cross-Stick Cue", fill="#2D261D", font=font(46, bold=True))
    draw.text(
        (56, 104),
        "这一步承接 gear release accent：昨天解决“如何把放开做成明确重音”，今天解决“如何再压缩成更短的入口提示”。",
        fill="#655A4E",
        font=font(25),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("基础 marcha", ["Gm9", "-", "C13", "-", "Gm9", "-", "C13", "-"], [0, 2, 4, 6], "前面的滚动继续稳定，cue 必须站在已有 groove 上。"),
        ("句尾动作", ["-", "-", "-", "-", "-", "-", "prep", "cue"], [6, 7], "先短收，再给一记极短提示；和 release accent 相比，长度更短，指令感更强。"),
        ("听感结果", ["稳", "推", "弹", "留", "稳", "推", "含", "进"], [6, 7], "最后两格的“含 -> 进”不是夸张重音，而是把下一轮入口说清楚。"),
    ]

    for row_idx, (label, cells, active, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 48), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            active_fill = "#5E88C6" if row_idx == 0 else "#C8823F"
            if row_idx == 2:
                active_fill = "#3E9A72"
            outline = "#5E759E" if row_idx == 0 else "#B76E31"
            if row_idx == 2:
                outline = "#2E7D59"
            txt = "#FFFFFF" if i in active else "#4A5766"
            fill = active_fill if i in active else "#E6ECF4"
            if row_idx == 1 and i == 6:
                fill = "#8A8F98"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(24, bold=True))
            state = "active" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：如果最后一下听起来只是更大声，说明还是 accent 思路；如果它像一句短促的“现在进”，才是 cue 的状态。", fill="#5F5547", font=font(22, bold=True))

    img.save(ASSET_DIR / "timba-cross-stick-cue-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
