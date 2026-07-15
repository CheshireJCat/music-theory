from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-07-15-timba-entry-accent-release"
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
    img = Image.new("RGB", (1560, 1040), "#F5F0E7")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Entry Accent Release", fill="#2E2419", font=font(48, bold=True))
    draw.text(
        (54, 102),
        "今天讲 entry accent release：入口已经用两层重音叠厚以后，怎样在下一拍顺势放回 marcha，让能量继续流动而不是僵在重拍上。",
        fill="#66584B",
        font=font(27),
    )

    draw.rounded_rectangle((74, 176, 1486, 356), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 214), "示例调性：Gm。第 1 拍先 lock，第 1 个 `&` 做 stack，第 2 拍立刻缩回正常 marcha。重点不是把重音越堆越久，而是让入口厚一下以后自然放开。", fill="#8B5A2A", font=font(24, bold=True))
    draw.text((102, 268), "判断标准：如果第 2 拍还能听见 groove 重新流起来，就是 release 成功；如果还像抱着一大块和弦不放，就说明 release 失败。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&", "1", "&", "2", "&"]
    left_hits = [0, 3, 6, 8]
    right_marcha = [1, 3, 5, 10]
    cue_zone = [7]
    lock_zone = [8]
    stack_zone = [9]
    release_zone = [10]
    start_x = 70
    y_top = 484
    y_mid = 650
    y_bottom = 816
    draw.text((24, 436), "左手支点", fill="#486FA8", font=font(30, bold=True))
    draw.text((24, 602), "右手 marcha", fill="#2E7D59", font=font(30, bold=True))
    draw.text((24, 768), "入口层次", fill="#B4622F", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 102
        fill_top = "#5D88C5" if idx in left_hits else "#E7EDF3"
        fill_mid = "#3E9A72" if idx in right_marcha else "#E6F2EB"
        if idx in cue_zone:
            fill_bottom = "#8A8F98"
        elif idx in lock_zone:
            fill_bottom = "#C97847"
        elif idx in stack_zone:
            fill_bottom = "#D79A3D"
        elif idx in release_zone:
            fill_bottom = "#5F9C7A"
        else:
            fill_bottom = "#EEE8DF"
        draw_pill(draw, (x, y_top, x + 78, y_top + 56), label, fill_top, "#FFFFFF", size=20)
        draw_pill(draw, (x, y_mid, x + 78, y_mid + 56), label, fill_mid, "#FFFFFF", size=20)
        draw_pill(draw, (x, y_bottom, x + 78, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=20)

    center_text(draw, (784, y_bottom + 8, 862, y_bottom + 48), "cue", "#FFFFFF", font(18, bold=True))
    center_text(draw, (886, y_bottom + 8, 964, y_bottom + 48), "lock", "#FFFFFF", font(18, bold=True))
    center_text(draw, (988, y_bottom + 8, 1066, y_bottom + 48), "stack", "#FFFFFF", font(18, bold=True))
    center_text(draw, (1090, y_bottom + 8, 1168, y_bottom + 48), "release", "#FFFFFF", font(16, bold=True))

    cards = [
        (92, 900, "#EEF3FF", "#AFC2E2", "先叠厚", "entry accent stack 先把入口做成双层重音，但这只是瞬间加厚，不是长期占住脉冲。"),
        (560, 900, "#FFF6E8", "#D8B37E", "立刻放回", "第 2 拍就回到 marcha，让重音的能量释放成滚动，而不是继续僵在前面两格。"),
        (1028, 900, "#EEF8F0", "#B8D5C0", "听见呼吸", "release 成功时，你会听见入口厚一下以后马上重新呼吸，像乐队吸完气继续跑。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 110), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 22, y + 14), title, fill="#33414C", font=font(27, bold=True))
        draw.text((x + 22, y + 54), body, fill="#5E6871", font=font(19))

    img.save(ASSET_DIR / "piano-timba-entry-accent-release.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EDF3EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Timba Entry Accent Release", fill="#17313A", font=font(48, bold=True))
    draw.text(
        (56, 102),
        "吉他上的重点是入口厚一下就收回，不把右手卡死在连续大重拍里。release 负责把 stack 的推进感重新导回正常 comping。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| Gm9 . C13 . Gm9 [cue] | -> | Gm9 [lock] [stack] C13 [release] ... |。今天比昨天多的，不是第三个重音，而是“怎么把第二层重音接回滚动”。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "手感标准：lock 像第一脚，stack 像第二脚，release 像脚落地后马上恢复走路；如果还停在原地跺脚，就没有 release。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Lock", "下一轮 1", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "先站稳入口。", "#C97B3F"),
        ("Stack", "1& 跟随重音", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "补第二层厚度。", "#D2A13D"),
        ("Release", "2 拍回 marcha", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "立刻放回滚动。", "#5F9C7A"),
        ("C13", "后续 comping", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "保持 groove 连续。", "#5C7DB8"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：点 - 落 - 补 - 放 - 走。第 4 步的“放”最关键：它把入口的厚度重新导回 marcha，而不是继续加码。",
        fill="#4D5F68",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-entry-accent-release.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Entry Accent Release", fill="#2D261D", font=font(46, bold=True))
    draw.text(
        (56, 104),
        "这一步承接 Timba Entry Accent Stack：上一课解决“怎样把入口叠厚”，今天解决“叠厚以后怎样顺势放回 marcha，让入口不是一坨硬重拍，而是继续流动的 groove”。",
        fill="#655A4E",
        font=font(25),
    )

    lane_top = 232
    lane_left = 72
    cell_w = 104
    lane_h = 118
    row_gap = 48

    rows = [
        ("时间格", ["1", "&", "2", "&", "3", "&", "4", "&", "1", "&", "2", "&"], [7, 8, 9, 10], "第 8 格发 cue，下一轮 `1` lock，`1&` stack，`2` release。"),
        ("动作层", ["稳", "-", "推", "-", "稳", "-", "收", "cue", "lock", "stack", "release", "flow"], [7, 8, 9, 10, 11], "release 把双层入口重音重新接回流动，不让队形卡在门口。"),
        ("听感层", ["滚", "留", "推", "留", "滚", "留", "含", "进", "齐", "厚", "松", "走"], [7, 8, 9, 10, 11], "听感从“进来”到“站稳”再到“厚一下后放开”，最后必须回到能继续走的状态。"),
    ]

    for row_idx, (label, cells, active, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 48), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 10
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
            if row_idx == 1 and i == 9:
                fill = "#D2A13D"
            if row_idx == 1 and i == 10:
                fill = "#5F9C7A"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(21, bold=True))
            state = "active" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(17, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：entry accent stack 解决“厚”，entry accent release 解决“松开并继续走”；如果没有第 2 拍的回流动作，入口会显得硬而笨。", fill="#5F5547", font=font(22, bold=True))

    img.save(ASSET_DIR / "timba-entry-accent-release-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
