from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-22-timba-bell-pattern"
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
        draw.text((x - 32, y + 44), state, fill="#5B5D61", font=font(18, bold=True))


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
    img = Image.new("RGB", (1560, 1000), "#F3EFE9")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Timba Bell Pattern 的高能切换感", fill="#2A221B", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Timba bell 是把 Songo 的线性滑行再推到更强编配切换、更高能量的舞曲组织里。重点不只是流动，而是带着全队突然抬升、甩开、再落回来的拉扯感。",
        fill="#64574B",
        font=font(28),
    )

    panels = [
        ((74, 184, 486, 900), "#FFF6EA", "#E1CCAB", "时间功能", "推进 + 抬升", "Timba 不只是把 groove 往前推，而是把每次切换都做得更像乐队整体换挡。", "#B76F2A"),
        ((574, 184, 986, 900), "#EEF2FF", "#B8C8E1", "和 Songo 对比", "更外放、更带能量", "Songo 像持续滑行，Timba 像滑行中不断加入更强的抛射点与提拉感。", "#4F6DA8"),
        ((1074, 184, 1486, 900), "#EEF8F0", "#B8D5C0", "钢琴应用", "右手 bell + 左手 anticipations", "右手可固定 A 或 A-E，左手用 Gm9-C13-F9-D7alt 的 anticipations 把编配往前甩。", "#48795B"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 222), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 286), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 372), desc, fill="#5F6870", font=font(27))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    colors = ["#B76F2A", "#5E88C6", "#E5EBF2", "#5E88C6", "#B76F2A", "#5E88C6", "#E5EBF2", "#B76F2A"]
    states = ["anchor", "lift", "", "push", "anchor", "lift", "", "gear"]
    start_x = 144
    for idx, label in enumerate(labels):
        x = start_x + idx * 166
        draw_hit(draw, x, 746, label, colors[idx], states[idx], size=24 if label == "&" else 26)

    draw_hit(draw, 1218, 672, "A", "#5E88C6", "RH", size=26)
    draw_hit(draw, 1360, 672, "A-E", "#5E88C6", "RH", size=18)
    draw_hit(draw, 1218, 828, "Gm9", "#48795B", "LH", size=18)
    draw_hit(draw, 1360, 828, "D7alt", "#48795B", "LH", size=18)

    draw.text((110, 890), "右手口令：稳 - 提 - 空 - 推 - 稳 - 提 - 空 - 换挡", fill="#B76F2A", font=font(25, bold=True))
    draw.text((692, 890), "左手：用 anticipations 提前半拍切进和声，制造 Timba 特有的编配爆发感", fill="#48795B", font=font(24, bold=True))

    draw.rounded_rectangle((92, 940, 1464, 984), 18, fill="#FFFDF9", outline="#D5CBBE", width=2)
    draw.text(
        (112, 950),
        "钢琴练法：右手先像 bell 一样稳定，左手再用提前切入的和声把拍点往前拉。听感应该比 Songo 更外放、更像整队突然提速。",
        fill="#5F564B",
        font=font(20, bold=True),
    )

    img.save(ASSET_DIR / "piano-timba-bell-pattern.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EDF2F5")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：高位切分里的 Timba Bell", fill="#18313A", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上弹 Timba bell，右手要保留 bell 的短促金属感，但比 Songo 更强调提早切入和突然冒头的能量。它像在 comping 里不断做小型 gear change。",
        fill="#4D636C",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#FFFDF9", outline="#C4D0D6", width=3)
    draw.text((114, 204), "入门循环：| Gm9 x C13 x | F9 x D7alt x |。先让闷音保持八分动作，再把出声点提早半拍抛出去。", fill="#223943", font=font(26, bold=True))
    draw.text((114, 260), "如果每个点都压在拍上，Timba 会退回普通 Latin comping；真正的味道来自 anticipations 和高位短促亮点。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Gm9", "3 x 3 3 3 5", [(1, 0, "1"), (1, 2, "b7"), (1, 3, "9"), (1, 4, "b3"), (3, 5, "5")], {1: "X"}, "起点要稳，但别弹成厚扫。", "#2F8B61"),
        ("C13", "8 x 8 9 10 10", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (3, 4, "13"), (3, 5, "5")], {1: "X"}, "这里像把编配往前甩出去。", "#C97B3F"),
        ("F9", "1 x 1 2 1 3", [(1, 0, "1"), (1, 2, "b7"), (2, 3, "3"), (1, 4, "5"), (3, 5, "9")], {1: "X"}, "落回主和声时也要保留弹性。", "#5C7DB8"),
        ("D7alt", "x 5 4 5 6 x", [(1, 1, "1"), (1, 2, "3"), (1, 3, "b7"), (2, 4, "b9")], {0: "X", 5: "X"}, "最后一击负责把下一轮能量抬起来。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((86, 932, 1474, 1028), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (108, 960),
        "右手口令：下 - 上 - 空 - 上 - 下 - 上 - 空 - 下。重点是提前切入的弹射感，而不是平均扫满八个格子。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-timba-bell-pattern.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#F8F5EF")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Timba Bell Pattern", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Timba bell 可以看成把 Songo 的线性组织再推进成更强的舞曲切换语言。重点不是更复杂，而是更明显的提前切入、提拉和换挡感。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 220
    lane_left = 96
    cell_w = 150
    lane_h = 132
    row_gap = 54
    accent_fill = "#D9803D"
    support_fill = "#6E88C3"
    base_fill = "#E6ECF4"

    rows = [
        ("bell 落点", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 4, 7], [1, 3, 5], "主拍仍然可见，但真正的 Timba 味道来自主拍之前与之后的提早抛点。"),
        ("身体动作", ["下", "提", "留", "推", "下", "提", "留", "换"], [0, 4, 7], [1, 3, 5], "动作上像在持续准备下一次切换，不能只是平推八分。"),
        ("听感对比", ["锚", "lift", "空", "push", "锚", "lift", "空", "gear"], [0, 4, 7], [1, 3, 5], "Songo 更像滑行，Timba 更像滑行中不断突然抬升、切换、甩开。"),
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
            state = "anchor" if i in accents else ("lift" if i in supports else "space")
            center_text(draw, (x0, y + 70, x1, y + 118), state, txt if i in accents or i in supports else "#667485", font(19, bold=i in accents or i in supports))
        draw.text((lane_left, y + 150), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((118, 840), "听感重点：Timba Bell Pattern 的核心，是把 bell 做成会提前抛、会突然换挡的高能时间线。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "timba-bell-pattern-structure.png")


def main():
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()


if __name__ == "__main__":
    main()
