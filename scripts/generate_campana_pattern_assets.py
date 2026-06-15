from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-15-campana-pattern"
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


def draw_hit(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str, *, size: int = 24):
    draw.rounded_rectangle((x - 48, y - 32, x + 48, y + 32), 18, fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 42, y - 22, x + 42, y + 22), label, "#ffffff", font(size, bold=True))


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 116
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 304, y + 470), 28, fill="#fffdfa", outline="#d2d6db", width=3)
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
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#ffffff", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#56656F", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 246, sx + 12, grid_top + 278), name, "#56656F", font(16, bold=True))

    draw.text((x + 28, y + 404), footnote, fill="#52656E", font=font(17))


def save_piano_chart():
    img = Image.new("RGB", (1560, 1000), "#f3efe7")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Campana Pattern 的外层提示感", fill="#2f251d", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Campana 可以看成比 bongo bell 更外层、更开阔的 cowbell 时间线。钢琴上适合把它放在右手高音区，让左手和中声部继续做 montuno 或低音循环。",
        fill="#68584A",
        font=font(28),
    )

    panels = [
        ((74, 184, 486, 900), "#fff5ea", "#dfc7a7", "时间功能", "外层框架提示", "它不只是推进，还会让整条 groove 的大轮廓更清楚，像把编制的轮廓线画出来。", "#ba7a37"),
        ((574, 184, 986, 900), "#eef4ff", "#b2c5df", "和 bongo bell 对比", "更开、更亮、更像带队", "bongo bell 像小齿轮持续滚，campana 则像把乐队往前提一层。", "#476f9d"),
        ((1074, 184, 1486, 900), "#eef8f0", "#afccb5", "钢琴应用", "右手高音区分层", "右手可用单音 E 或双音 E-B 点出 campana，左手继续 A-C-E-G 或 tumbao 型低音。", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 222), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 286), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 372), desc, fill="#5f6870", font=font(27))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    hit_colors = ["#c68445", "#e6ecf4", "#5a87ba", "#c68445", "#5a87ba", "#e6ecf4", "#c68445", "#5a87ba"]
    hit_text = ["call", "", "lift", "call", "lift", "", "call", "lift"]
    start_x = 144
    for idx, label in enumerate(labels):
        x = start_x + idx * 166
        draw_hit(draw, x, 746, label, hit_colors[idx], size=24 if label == "&" else 26)
        if hit_text[idx]:
            draw.text((x - 26, 800), hit_text[idx], fill="#5c554b", font=font(20, bold=True))

    draw_hit(draw, 1218, 672, "A", "#5a87ba", size=24)
    draw_hit(draw, 1360, 672, "E-B", "#5a87ba", size=18)
    draw_hit(draw, 1218, 828, "Am7", "#4f8a66", size=20)
    draw_hit(draw, 1360, 828, "G13", "#4f8a66", size=20)

    draw.text((112, 876), "右手口令：打 - 空 - 提 - 打 - 提 - 空 - 打 - 提", fill="#ba7a37", font=font(25, bold=True))
    draw.text((760, 876), "左手：A-C-E-G 循环或简化 tumbao，右手保持外层 bell 提示感", fill="#4f8265", font=font(25, bold=True))

    draw.rounded_rectangle((92, 932, 1464, 978), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (110, 943),
        "钢琴练法：先把 campana 的落点练成比 bongo bell 更开阔的提示层，再和左手低音叠起来。听感应像“把 groove 的外框点亮”。",
        fill="#5f564b",
        font=font(21, bold=True),
    )

    img.save(ASSET_DIR / "piano-campana-pattern.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：用高位切分模拟 Campana 的 cowbell 轮廓", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他可以把 campana 理解成比普通 comping 更短、更亮的高位切分层。用闷音维持 8 分脉搏，再用高把位和弦把 cowbell 的外层框架点出来。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am9 x C6/9 x | D9 x G13 x |。把开和弦都弹得短一点，保留 campana 的“点亮外框”感觉。", fill="#223943", font=font(26, bold=True))
    draw.text((114, 260), "如果扫得太满，它会变成普通伴奏；如果高位不够亮，cowbell 的提示感就不明显。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am9", "5 7 5 5 5 7", [(1, 0, "1"), (3, 1, "3"), (1, 2, "1"), (1, 3, "1"), (1, 4, "1"), (3, 5, "4")], {}, "第一拍做清晰起点，但不要拖长。", "#2f8b61"),
        ("C6/9", "x 3 2 2 3 3", [(3, 1, "2"), (2, 2, "1"), (2, 3, "1"), (3, 4, "3"), (3, 5, "4")], {0: "X"}, "中段色彩轻一点，保持上方亮度。", "#c97b3f"),
        ("D9", "x 5 4 5 5 x", [(1, 1, "1"), (1, 2, "2"), (1, 3, "3"), (1, 4, "4")], {0: "X", 5: "X"}, "后半拍的“提”可以用更薄的和弦表达。", "#5c7db8"),
        ("G13", "3 x 3 4 5 5", [(1, 0, "1"), (1, 2, "2"), (2, 3, "3"), (3, 4, "4"), (3, 5, "4")], {1: "X"}, "最后一个亮点像带着整句往下一轮走。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：下 - 空 - 上 - 下 - 上 - 空 - 下 - 上。先维持连续动作，再让 campana 的关键落点发亮。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-campana-pattern.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Campana Pattern", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Campana 常被当作 cowbell 的外层时间线。和 bongo bell 比起来，它更像一条把句法外框和乐队提示感一起抬高的亮线。",
        fill="#655a4e",
        font=font(27),
    )

    lane_top = 220
    lane_left = 96
    cell_w = 150
    lane_h = 132
    row_gap = 54
    accent_fill = "#d9803d"
    support_fill = "#7a90b8"
    base_fill = "#e6ecf4"

    rows = [
        ("campana 落点", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 6], [2, 4, 7], "主拍像在立柱子，附加落点像把句子向前拎起来，因此听起来比 bongo bell 更开阔。"),
        ("身体动作", ["下", "留", "上", "下", "上", "留", "下", "上"], [0, 3, 6], [2, 4, 7], "动作必须连续，否则它会变成几次分散重拍，而不是完整的 campana 时间线。"),
        ("和 bongo bell 对比", ["框", "留", "滚", "框", "提", "留", "框", "提"], [0, 3, 6], [2, 4, 7], "bongo bell 更像持续滚动的小齿轮，campana 更像把外层轮廓与带队感一起点亮。"),
    ]

    for row_idx, (label, cells, accents, supports, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 52), label, fill="#3f3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            if i in accents:
                fill = accent_fill
                outline = "#b86930"
                txt = "#ffffff"
            elif i in supports:
                fill = support_fill
                outline = "#5e759e"
                txt = "#ffffff"
            else:
                fill = base_fill
                outline = "#b7c2d0"
                txt = "#4a5766"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline, width=3)
            center_text(draw, (x0, y + 16, x1, y + 68), cell, txt, font(24, bold=True))
            state = "frame" if i in accents else ("lift" if i in supports else "space")
            center_text(draw, (x0, y + 70, x1, y + 118), state, txt if i in accents or i in supports else "#667485", font(19, bold=i in accents or i in supports))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((122, 840), "听感重点：Campana Pattern 的核心，是用更开阔、更亮的 cowbell 落点把 groove 的外层框架和带队感一起抬起来。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "campana-pattern-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
