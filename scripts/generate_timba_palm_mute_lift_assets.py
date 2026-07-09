from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-07-08-timba-palm-mute-lift"
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
    img = Image.new("RGB", (1560, 1040), "#F6EEDF")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Palm Mute Lift", fill="#2E2419", font=font(50, bold=True))
    draw.text(
        (54, 102),
        "今天推进到 palm mute lift：在反拍 punch 之后，不是继续加音，而是用短闷后瞬间放开的动作，把句尾抬起来。",
        fill="#66584B",
        font=font(27),
    )

    draw.rounded_rectangle((74, 176, 1486, 356), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 214), "示例调性：Gm。左手支点保持稳定，右手在 `4 &` 前后做一次短闷再放开，让下一轮像被托起来。", fill="#8B5A2A", font=font(24, bold=True))
    draw.text((102, 268), "判断标准：lift 应该来自“收紧再松开”的对比，而不是简单把最后一个反拍再打重。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    left_hits = [0, 3, 6]
    marcha_hits = [1, 3, 5]
    mute_zone = [6]
    lift_zone = [7]
    start_x = 146
    y_top = 484
    y_mid = 650
    y_bottom = 816
    draw.text((96, 436), "左手支点", fill="#486FA8", font=font(30, bold=True))
    draw.text((96, 602), "右手 marcha", fill="#2E7D59", font=font(30, bold=True))
    draw.text((96, 768), "mute -> lift", fill="#B4622F", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#5D88C5" if idx in left_hits else "#E7EDF3"
        fill_mid = "#3E9A72" if idx in marcha_hits else "#E6F2EB"
        if idx in mute_zone:
            fill_bottom = "#8A8F98"
        elif idx in lift_zone:
            fill_bottom = "#C97847"
        else:
            fill_bottom = "#EEE8DF"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_mid, x + 108, y_mid + 56), label, fill_mid, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    center_text(draw, (1120, y_bottom + 8, 1210, y_bottom + 48), "闷", "#FFFFFF", font(22, bold=True))
    center_text(draw, (1280, y_bottom + 8, 1370, y_bottom + 48), "抬", "#FFFFFF", font(22, bold=True))

    cards = [
        (92, 900, "#EEF3FF", "#AFC2E2", "先收再放", "先把句尾短暂收紧，下一下放开才会有真正 lift。"),
        (560, 900, "#EEF8F0", "#B8D5C0", "长度要短", "mute 只是一瞬间，不要把 groove 整体压扁。"),
        (1028, 900, "#FFF2DD", "#D9B57F", "lift 在下一轮", "听感重点不是停顿本身，而是停顿后下一轮更轻巧地弹起。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 110), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 22, y + 14), title, fill="#33414C", font=font(27, bold=True))
        draw.text((x + 22, y + 54), body, fill="#5E6871", font=font(19))

    img.save(ASSET_DIR / "piano-timba-palm-mute-lift.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF4F2")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Timba Palm Mute Lift", fill="#17313A", font=font(50, bold=True))
    draw.text(
        (56, 102),
        "吉他的任务是先用掌根轻闷把句尾收住，再在下一拍或下一轮立刻放开，让 comping 出现明显的上提感。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| Gm9 . C13 . Gm9 [mute] [lift] |。先把 `4` 收紧，再在 `4 &` 或下一轮 `1` 放开。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "手感标准：不是停住不动，而是让闷音像压缩弹簧，放开时整段 groove 更轻更弹。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "主和弦切片。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "句尾准备收紧。", "#C97B3F"),
        ("Palm mute", "掌根轻压", [(2, 1, "PM"), (2, 2, "PM"), (2, 3, "PM")], {0: "X", 5: "X"}, "让弦瞬间失去延音。", "#5C7DB8"),
        ("Lift", "松开再弹", [(2, 1, "up"), (2, 3, "go"), (2, 4, "!")], {0: "X", 5: "X"}, "放开时要更轻巧。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：推 - 推 - 收 - 抬。最后两步一定要形成对比，只有这样 palm mute lift 才会听起来像句尾起飞。",
        fill="#4D5F68",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-palm-mute-lift.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Palm Mute Lift", fill="#2D261D", font=font(48, bold=True))
    draw.text(
        (56, 104),
        "这一步承接 contratiempo punch：前一课解决“反拍顶起”，今天解决“句尾怎样通过短闷与放开做出 lift”。",
        fill="#655A4E",
        font=font(26),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("基础 marcha", ["Gm9", "-", "C13", "-", "Gm9", "-", "C13", "-"], [0, 2, 4, 6], "支点继续稳定，不能因为句尾要 lift 就提前散掉。"),
        ("句尾动作", ["-", "-", "-", "-", "-", "-", "mute", "lift"], [6, 7], "先在 `4` 附近收紧，再在 `4 &` 或下一轮放开。"),
        ("听感结果", ["稳", "推", "弹", "留", "稳", "推", "缩", "抬"], [6, 7], "最后两格的“缩 -> 抬”决定这一步是否成立。"),
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
    draw.text((118, 908), "判断标准：如果只听到“停了一下”，说明 mute 太重；如果只听到“又打一下”，说明 lift 不够来自收放对比。", fill="#5F5547", font=font(23, bold=True))

    img.save(ASSET_DIR / "timba-palm-mute-lift-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
