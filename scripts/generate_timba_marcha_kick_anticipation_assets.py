from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-07-06-timba-marcha-kick-anticipation"
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
    img = Image.new("RGB", (1560, 1040), "#F4E9DA")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Marcha Kick Anticipation", fill="#2E2419", font=font(50, bold=True))
    draw.text(
        (54, 102),
        "上一课已经把 groove 锁稳，这一课只推进一步：在 marcha 已经稳住以后，用提前半拍的 kick 把下一轮推进往前拽。",
        fill="#66584B",
        font=font(27),
    )

    draw.rounded_rectangle((74, 176, 1486, 356), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 214), "示例调性：Gm。核心动作不是多加重音，而是在第 4 拍后半拍提前给出 Gm9 / C13 的 kick，制造“下一轮已经要到了”的前冲感。", fill="#8B5A2A", font=font(24, bold=True))
    draw.text((102, 268), "判断标准：如果身体会被提前一下往前拽，而 groove 仍然稳，说明 anticipation 成立；如果只是抢拍，就不对。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    left_hits = [0, 3, 6, 7]
    right_hits = [1, 3, 5, 7]
    kick_zone = [7]
    start_x = 146
    y_top = 484
    y_mid = 650
    y_bottom = 816
    draw.text((96, 436), "左手入口", fill="#486FA8", font=font(30, bold=True))
    draw.text((96, 602), "右手 marcha", fill="#2E7D59", font=font(30, bold=True))
    draw.text((96, 768), "提前 kick", fill="#B4622F", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#5D88C5" if idx in left_hits else "#E7EDF3"
        fill_mid = "#3E9A72" if idx in right_hits else "#E6F2EB"
        fill_bottom = "#C97847" if idx in kick_zone else "#EEE8DF"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_mid, x + 108, y_mid + 56), label, fill_mid, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    cards = [
        (92, 900, "#EEF3FF", "#AFC2E2", "锁稳以后才提前", "如果 groove 还没锁住就抢拍，只会听起来乱；anticipation 必须建立在稳定 marcha 之后。"),
        (560, 900, "#EEF8F0", "#B8D5C0", "kick 要短", "提前 kick 像拉门把手，点到就收，目的是把下一轮拉近，不是把整拍占满。"),
        (1028, 900, "#FFF2DD", "#D9B57F", "提前不等于快", "速度不变，真正变的是心理重心被提前半步往前送。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 110), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 22, y + 14), title, fill="#33414C", font=font(27, bold=True))
        draw.text((x + 22, y + 54), body, fill="#5E6871", font=font(19))

    img.save(ASSET_DIR / "piano-timba-marcha-kick-anticipation.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF4F2")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：Timba Marcha Kick Anticipation", fill="#17313A", font=font(50, bold=True))
    draw.text(
        (56, 102),
        "吉他这里的任务，是在高位短促 comping 已经锁住 groove 后，用一次提前半拍的和弦 kick 把下一轮入口往前拽。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：| Gm9 . . C13 . . Gm9 kick |。最后一个 Gm9 放在 `4 &`，像提前吸一口气，把下一小节拽进来。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "手感标准：前面是稳定 marcha，最后一下是短促 anticipatory kick，不是额外扫满。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "主和弦切片。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "属味推动。", "#C97B3F"),
        ("Gm9 kick", "x 10 12 10 11 x", [(1, 1, "1"), (3, 2, "5"), (1, 3, "b7"), (2, 4, "9")], {0: "X", 5: "X"}, "放在 `4 &` 的提前 kick。", "#5C7DB8"),
        ("右手口令", "点 留 点 留 拉", [(2, 1, "1"), (2, 2, "2"), (2, 3, "3"), (2, 4, "4")], {0: "X", 5: "X"}, "最后一拉要短，像把下一轮拽近。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：点 - 留 - 点 - 留 - 拉。最后那个“拉”在 `4 &`，目的是把下一小节的重拍提前预告出来。",
        fill="#4D5F68",
        font=font(23, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-marcha-kick-anticipation.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Marcha Kick Anticipation", fill="#2D261D", font=font(48, bold=True))
    draw.text(
        (56, 104),
        "这一步承接 re-entry marcha lock：先把 groove 咬稳，再在最后半拍提前给一个 kick，让下一轮推进像被提前点火。",
        fill="#655A4E",
        font=font(26),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("基础 marcha", ["Gm9", "-", "-", "C13", "-", "-", "Gm9", "-"], [0, 3, 6], "先把稳定推进咬住。"),
        ("anticipation kick", ["-", "-", "-", "-", "-", "-", "-", "kick"], [7], "在 `4 &` 提前半步把下一轮拉近。"),
        ("听感结果", ["稳", "推", "稳", "推", "稳", "推", "悬", "拽"], [6, 7], "最后两格从稳定推进转成“已经要进下一轮”的前冲。"),
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
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(24, bold=True))
            state = "go" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：提前 kick 应该让你感觉“下一拍已经在路上”，而不是让乐队真的把速度越弹越快。", fill="#5F5547", font=font(23, bold=True))

    img.save(ASSET_DIR / "timba-marcha-kick-anticipation-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
