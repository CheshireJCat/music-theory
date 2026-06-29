from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-29-timba-mambo-horn-hits"
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
    img = Image.new("RGB", (1560, 1040), "#F6EBDD")
    draw = ImageDraw.Draw(img)
    draw.text((54, 38), "钢琴图：Timba Mambo Horn Hits", fill="#2E2419", font=font(52, bold=True))
    draw.text(
        (54, 102),
        "Horn hits 是高能段里像口号一样整齐砸出的铜管/高位齐奏短句。钢琴要做的不是把它弹成长线旋律，而是把这些短句落点弹得像一整排招牌灯同时亮起。",
        fill="#66584B",
        font=font(28),
    )

    draw.rounded_rectangle((74, 176, 1486, 354), 26, fill="#FFF8EE", outline="#DCC8A8", width=3)
    draw.text((102, 212), "示例调性：Gm。前一小节先由 marcha / moña 把兴奋顶住，下一小节用 Bb-D-F / A-C-Eb 的齐奏短句做 horn hits。", fill="#8B5A2A", font=font(28, bold=True))
    draw.text((102, 262), "理解方式：moña 负责不断回勾，horn hits 负责把那句口号扩大成整队都会喊的高位标语。", fill="#58616B", font=font(24))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    marcha = [1, 3, 5, 6, 7]
    hits = [0, 3, 5, 7]
    start_x = 146
    y_top = 484
    y_bottom = 650
    draw.text((96, 436), "前一小节推进", fill="#4A78AE", font=font(30, bold=True))
    draw.text((96, 602), "horn hits 落点", fill="#A4562B", font=font(30, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 160
        fill_top = "#5D88C5" if idx in marcha else "#E7EDF3"
        fill_bottom = "#C97847" if idx in hits else "#E8E3D9"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)

    cards = [
        (92, 790, "#EEF3FF", "#AFC2E2", "先铺口号感", "前一小节必须先把 marcha 或 moña 的持续推进立住，齐奏口号才会显得像被举到前景。"),
        (560, 790, "#FFF2DD", "#D9B57F", "句子要短而齐", "每次 horn hit 都要像一块整齐切下来的和声砖块，不可拖成长线。"),
        (1028, 790, "#EEF8F0", "#B8D5C0", "打完立刻留空", "真正有冲击力的 hits 不是一直堆音，而是砸一下、闪开、再回来。"),
    ]
    for x, y, fill, outline, title, body in cards:
        draw.rounded_rectangle((x, y, x + 376, y + 186), 26, fill=fill, outline=outline, width=3)
        draw.text((x + 26, y + 22), title, fill="#33414C", font=font(32, bold=True))
        draw.text((x + 26, y + 82), body, fill="#5E6871", font=font(23))

    img.save(ASSET_DIR / "piano-timba-mambo-horn-hits.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF4F2")
    draw = ImageDraw.Draw(img)
    draw.text((56, 38), "吉他图：跟出 Horn Hits 的高位和弦", fill="#17313A", font=font(52, bold=True))
    draw.text(
        (56, 102),
        "吉他在这个主题里更像高位铜管补光层。不要把和弦扫成长条，而要把每次出声做成统一、短促、齐整的和声切片。",
        fill="#4C636C",
        font=font(26),
    )

    draw.rounded_rectangle((88, 164, 1470, 332), 26, fill="#FFFDF9", outline="#C7D1D5", width=3)
    draw.text((116, 202), "练习循环：先用 Gm9 - C13 轻推，再在 Bb6/9 与 D7alt 上做短促齐奏，最后用 Ebmaj9 收回到下一轮。", fill="#223943", font=font(24, bold=True))
    draw.text((116, 258), "判断标准：每次 hits 出来时，你听到的应该是“整队一起喊一句”，而不是普通切分伴奏。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "前段轻推。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "把句子抬高。", "#C97B3F"),
        ("Bb6/9", "6 x 5 7 6 6", [(1, 0, "1"), (1, 2, "3"), (2, 3, "6"), (1, 4, "9"), (1, 5, "5")], {1: "X"}, "第一下齐奏口号。", "#5C7DB8"),
        ("D7alt", "x 5 4 5 6 x", [(1, 1, "1"), (1, 2, "3"), (1, 3, "b7"), (2, 4, "b9")], {0: "X", 5: "X"}, "第二下负责刺穿张力。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 414, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((88, 930, 1470, 1026), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (112, 958),
        "右手口令：推 - 留 - 推 - 留 | 喊 - 停 - 喊 - 回。Horn hits 的关键是齐和短，不是密和长。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-mambo-horn-hits.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1040), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Mambo Horn Hits", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Horn hits 是高能段里的高位齐奏口号。它通常接在 moña 或 marcha 之后，把已存在的兴奋感集中成更大面积、更像乐队宣言的短句。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 232
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("推进层", ["1", "&", "2", "&", "3", "&", "4", "&"], [1, 3, 5, 6, 7], "先由 marcha / moña 把高能段一直顶住。"),
        ("horn hits", ["Bb", "-", "D", "F", "A", "C", "Eb", "-"], [0, 3, 5, 6], "短句必须像高位齐奏口号一样整齐、明亮、短促。"),
        ("身体口令", ["喊", "留", "抬", "喊", "冲", "喊", "落", "回"], [0, 3, 4, 5, 6], "打完后立刻回到 groove，给下一轮继续抬升留空间。"),
    ]

    for row_idx, (label, cells, active, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 48), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            active_fill = "#5E88C6" if row_idx == 0 else "#C8823F"
            outline = "#5E759E" if row_idx == 0 else "#B76E31"
            txt = "#FFFFFF" if i in active else "#4A5766"
            fill = active_fill if i in active else "#E6ECF4"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(24, bold=True))
            state = "hit" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 874, 1404, 980), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 908), "判断标准：听感应该像“前面先把兴奋吊住，然后整队一起把一句高位口号举起来”，而不是随手多弹几下高音。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "timba-mambo-horn-hits-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
