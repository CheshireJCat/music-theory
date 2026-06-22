from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-17-songo-bell-pattern"
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


def draw_hit(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str, state: str = "", *, size: int = 24):
    draw.rounded_rectangle((x - 48, y - 32, x + 48, y + 32), 18, fill=color, outline="#FFFFFF", width=3)
    center_text(draw, (x - 42, y - 22, x + 42, y + 22), label, "#FFFFFF", font(size, bold=True))
    if state:
        draw.text((x - 28, y + 44), state, fill="#5B5D61", font=font(18, bold=True))


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
    img = Image.new("RGB", (1560, 1000), "#EFF3EE")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Songo Bell Pattern 的线性推动感", fill="#1F2A22", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Songo bell 把前几天的 cowbell 组织感再往现代化推进一步。它比 Mozambique 更线性，和鼓组、ghost note、切分 bass 的咬合通常更紧。",
        fill="#56645A",
        font=font(28),
    )

    panels = [
        ((74, 184, 486, 900), "#FFF7EC", "#E1CCAB", "时间功能", "线性推动", "它不是只强调大拍，而是在主拍之间不断留下推动标记，让 groove 像一条持续滚动的线。", "#B98238"),
        ((574, 184, 986, 900), "#EDF3FF", "#B8C8E1", "和 Mozambique 对比", "更现代、更贴鼓组", "Mozambique 像前冲口令，Songo 更像把口令拆进整条节奏织体里。", "#4B76A7"),
        ((1074, 184, 1486, 900), "#EEF8F3", "#B2D0BE", "钢琴应用", "右手 bell + 左手空隙低音", "右手可固定 G 或 G-D 的短音，左手用 D-A-C 的切分低音，让线条一直向前滑。", "#4C8463"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 222), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 286), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 372), desc, fill="#5F6870", font=font(27))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    colors = ["#C68645", "#5E8BBB", "#E5EBF2", "#C68645", "#5E8BBB", "#C68645", "#E5EBF2", "#5E8BBB"]
    states = ["anchor", "flow", "", "anchor", "flow", "lift", "", "flow"]
    start_x = 144
    for idx, label in enumerate(labels):
        x = start_x + idx * 166
        draw_hit(draw, x, 746, label, colors[idx], states[idx], size=24 if label == "&" else 26)

    draw_hit(draw, 1218, 672, "G", "#5E8BBB", "RH", size=24)
    draw_hit(draw, 1360, 672, "G-D", "#5E8BBB", "RH", size=18)
    draw_hit(draw, 1218, 828, "Dm9", "#4C8463", "LH", size=20)
    draw_hit(draw, 1360, 828, "C13", "#4C8463", "LH", size=20)

    draw.text((110, 890), "右手口令：稳 - 推 - 空 - 稳 - 推 - 提 - 空 - 推", fill="#B98238", font=font(25, bold=True))
    draw.text((756, 890), "左手：D-A-C 空隙低音，故意给 bell 留缝，让线性感更明显", fill="#4C8463", font=font(25, bold=True))

    draw.rounded_rectangle((92, 940, 1464, 984), 18, fill="#FFFDF9", outline="#D5CBBE", width=2)
    draw.text(
        (112, 950),
        "钢琴练法：先把右手 Songo bell 练成连续线条，再让左手低音只在空隙处补位。听感应比 Mozambique 更像整条 groove 在滑行。",
        fill="#5F564B",
        font=font(20, bold=True),
    )

    img.save(ASSET_DIR / "piano-songo-bell-pattern.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EEF3F7")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：高把位切分里的 Songo Bell", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上弹 Songo bell，重点是让右手像鼓组 hi-hat 一样连续，而高把位和弦只在关键位置发亮。这样会比 Mozambique 更有现代、流动的编配感。",
        fill="#4D636C",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#FFFDF9", outline="#C4D0D6", width=3)
    draw.text((114, 204), "入门循环：| Dm9 x G13 x | C13 x A7sus x |。先让闷音把八分脉搏铺满，再让和弦像 bell 一样短促地冒出来。", fill="#223943", font=font(26, bold=True))
    draw.text((114, 260), "如果右手停顿太多，Songo 会失去线性感；如果每个点都扫满，又会退回普通 Latin comping。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Dm9", "x 5 3 5 5 5", [(1, 1, "1"), (1, 2, "b3"), (1, 3, "5"), (1, 4, "b7"), (1, 5, "9")], {0: "X"}, "主拍要准，但别压重到失去弹性。", "#2F8B61"),
        ("G13", "3 x 3 4 5 5", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "这个点像线条里的前冲弯钩。", "#C97B3F"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "后半段不要太满，留出滑行空间。", "#5C7DB8"),
        ("A7sus", "5 x 5 5 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "4"), (3, 4, "9"), (1, 5, "5")], {1: "X"}, "最后一击像把下一轮推出去。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((86, 932, 1474, 1028), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (108, 960),
        "右手口令：下 - 上 - 空 - 下 - 上 - 下 - 空 - 上。先连贯，再把亮点做成短、弹、滑的高位切分。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-songo-bell-pattern.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#F8F6F1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Songo Bell Pattern", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Songo bell 可以看成 bell 时间线继续现代化的一步。重点不是更密，而是把推进拆成更流动、更贴近鼓组语言的线性组织。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 220
    lane_left = 96
    cell_w = 150
    lane_h = 132
    row_gap = 54
    accent_fill = "#D9803D"
    support_fill = "#7A90B8"
    base_fill = "#E6ECF4"

    rows = [
        ("bell 落点", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 5], [1, 4, 7], "主拍仍是骨架，但真正的现代感来自主拍之间那些持续牵引的连接点。"),
        ("身体动作", ["下", "上", "留", "下", "上", "下", "留", "上"], [0, 3, 5], [1, 4, 7], "手感不能只剩重音，必须保持像滚动一样的连续动作。"),
        ("听感对比", ["锚", "流", "空", "锚", "流", "提", "空", "流"], [0, 3, 5], [1, 4, 7], "Mozambique 更像口令式前冲，Songo 更像口令已经化进整条编配的流动线。"),
    ]

    for row_idx, (label, cells, accents, supports, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 52), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            if i in accents:
                fill = accent_fill
                outline = "#B86930"
                txt = "#FFFFFF"
            elif i in supports:
                fill = support_fill
                outline = "#5E759E"
                txt = "#FFFFFF"
            else:
                fill = base_fill
                outline = "#B7C2D0"
                txt = "#4A5766"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline, width=3)
            center_text(draw, (x0, y + 16, x1, y + 68), cell, txt, font(24, bold=True))
            state = "anchor" if i in accents else ("flow" if i in supports else "space")
            center_text(draw, (x0, y + 70, x1, y + 118), state, txt if i in accents or i in supports else "#667485", font(19, bold=i in accents or i in supports))
        draw.text((lane_left, y + 150), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 840), "听感重点：Songo Bell Pattern 的核心，是把 bell 变成一条持续滑行的线，而不只是几个显眼的冲击点。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "songo-bell-pattern-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
