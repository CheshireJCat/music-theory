from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-23-timba-gear-change"
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


def draw_pill(draw, box, text, fill, outline, text_fill="#FFFFFF", size=26):
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
    img = Image.new("RGB", (1560, 1020), "#F4F0E8")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Timba Gear Change 的换挡手感", fill="#2C231A", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Gear change 不是单纯把 bell 打得更满，而是在固定 groove 里突然切换重心、层次和爆发方向，让整队在同样拍速里像瞬间进入下一档。",
        fill="#65584A",
        font=font(28),
    )

    panels = [
        ((74, 184, 486, 904), "#FFF6EA", "#E1CCAB", "段落前", "稳住时间线", "先用 bell 或 montuno 维持循环，让耳朵建立当前 groove。", "#B76F2A"),
        ((574, 184, 986, 904), "#EEF2FF", "#B8C8E1", "换挡瞬间", "提前切入 + 重音搬家", "左手和声提早半拍，右手亮点忽然改落点，听感像从巡航直接进入加速。", "#4F6DA8"),
        ((1074, 184, 1486, 904), "#EEF8F0", "#B8D5C0", "段落后", "更密更冲", "换挡后的重复型通常更密、更亮，也更像在催促全队往前冲。", "#48795B"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 222), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 286), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 372), desc, fill="#5F6870", font=font(27))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    before = [0, 3, 5]
    after = [1, 3, 4, 6, 7]
    start_x = 128
    y_top = 710
    y_bottom = 830
    draw.text((112, 650), "换挡前", fill="#A86A32", font=font(28, bold=True))
    draw.text((112, 770), "换挡后", fill="#4E73AA", font=font(28, bold=True))
    for idx, label in enumerate(labels):
        x = start_x + idx * 168
        fill_top = "#C97B3F" if idx in before else "#E8ECEF"
        fill_bottom = "#5E88C6" if idx in after else "#E8ECEF"
        draw_pill(draw, (x, y_top, x + 108, y_top + 56), label, fill_top, "#FFFFFF", size=24)
        draw_pill(draw, (x, y_bottom, x + 108, y_bottom + 56), label, fill_bottom, "#FFFFFF", size=24)
    draw.text((114, 900), "钢琴练法：右手先把前后两种落点分开练，左手再把 Gm9-C13 与 Ebmaj9-D7alt 的切换做成提前半拍的推力。", fill="#5E5448", font=font(23, bold=True))
    draw.text((114, 944), "关键：换挡必须让人听见“同样的速度，但能量层级突然变了”。", fill="#48795B", font=font(22, bold=True))

    img.save(ASSET_DIR / "piano-timba-gear-change.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EDF3F5")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：Timba Gear Change 的高位切换", fill="#18313A", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上做 gear change，重点是同一段 comping 先稳住，再突然把和弦亮点换到更前、更密、更高的位置。右手的连续动作不能断，换挡感来自落点和重音的重新分配。",
        fill="#4D636C",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#FFFDF9", outline="#C4D0D6", width=3)
    draw.text((114, 204), "入门循环：前半段 | Gm9 x C13 x |，换挡后改成 | Ebmaj9 D7alt | 并把出声点提前，像突然把编配推到更亮的一层。", fill="#223943", font=font(24, bold=True))
    draw.text((114, 260), "如果只是换了和弦没换重心，就不是 gear change；真正的感觉是整队忽然抬头、加压、往前扑。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "稳住第一档的 groove。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "准备把能量往前甩。", "#C97B3F"),
        ("Ebmaj9", "x 6 5 7 6 x", [(1, 1, "1"), (1, 2, "3"), (2, 3, "7"), (1, 4, "9")], {0: "X", 5: "X"}, "换挡后更亮、更开阔。", "#5C7DB8"),
        ("D7alt", "x 5 4 5 6 x", [(1, 1, "1"), (1, 2, "3"), (1, 3, "b7"), (2, 4, "b9")], {0: "X", 5: "X"}, "最后负责把下一轮继续顶起来。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((86, 932, 1474, 1028), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (108, 960),
        "右手口令：下 - 上 - 空 - 上 - 下 - 上 - 下 - 上。前半段像巡航，后半段像突然踩下去。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-gear-change.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 1020), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Gear Change", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Timba 里的 gear change，本质是保持大拍不变，但把重音、落点、层次和和声入口突然改写，于是听感像整段 groove 被瞬间推入下一档。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 228
    lane_left = 96
    cell_w = 150
    lane_h = 118
    row_gap = 48

    rows = [
        ("换挡前", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 5], "稳住基础 bell/comping，让听众先习惯当前档位。"),
        ("换挡后", ["1", "&", "2", "&", "3", "&", "4", "&"], [1, 3, 4, 6, 7], "把亮点往前挤、往后拖，立刻形成更密更冲的第二档。"),
        ("身体口令", ["稳", "提", "留", "推", "咬", "顶", "追", "爆"], [0, 3, 4, 6, 7], "动作和重音一起换挡，整队听起来像忽然抬起车头。"),
    ]

    for row_idx, (label, cells, active, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 48), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            active_fill = "#D9803D" if row_idx == 0 else "#5E88C6"
            outline = "#B86930" if row_idx == 0 else "#5E759E"
            txt = "#FFFFFF" if i in active else "#4A5766"
            fill = active_fill if i in active else "#E6ECF4"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline if i in active else "#B7C2D0", width=3)
            center_text(draw, (x0, y + 16, x1, y + 62), cell, txt, font(24, bold=True))
            state = "hit" if i in active else "rest"
            center_text(draw, (x0, y + 66, x1, y + 106), state, txt if i in active else "#667485", font(18, bold=i in active))
        draw.text((lane_left, y + 136), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 858, 1404, 964), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 892), "判断标准：听感不是“更忙”，而是“同样 BPM 下，整段 groove 突然切到更高压的一档”。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "timba-gear-change-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
