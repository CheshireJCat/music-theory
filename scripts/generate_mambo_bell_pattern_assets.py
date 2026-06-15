from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-11-mambo-bell-pattern"
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


def draw_hit(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str, *, size: int = 26):
    draw.rounded_rectangle((x - 44, y - 30, x + 44, y + 30), 18, fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 38, y - 22, x + 38, y + 22), label, "#ffffff", font(size, bold=True))


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
    img = Image.new("RGB", (1560, 1000), "#f5efe6")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Mambo Bell Pattern 的高频时间线", fill="#30261B", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Mambo bell 可以理解为把前一天的 cascara 再提亮到高音区。钢琴上常用左手守低音 ostinato，右手在高音区重复 bell 的落点。",
        fill="#68584A",
        font=font(28),
    )

    panels = [
        ((74, 184, 486, 900), "#fff3e7", "#dfc7a7", "时间功能", "高频时间线", "它比 cascara 更亮，常负责让整支乐队都抓到持续前冲的脉搏。", "#ba7a37"),
        ((574, 184, 986, 900), "#eef4ff", "#b2c5df", "和 cascara 关系", "同源但更尖锐", "cascara 像外壳，mambo bell 像在外壳上画出更明确的亮点。", "#476f9d"),
        ((1074, 184, 1486, 900), "#eef8f0", "#afccb5", "钢琴应用", "右手高音重复", "右手可固定单音或八度，左手再用 Am6 - Dm9 - E7 带和声方向。", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 222), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 286), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 372), desc, fill="#5f6870", font=font(27))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    hit_colors = ["#c68445", "#c68445", "#e6ecf4", "#c68445", "#4f8265", "#e6ecf4", "#4f8265", "#4f8265"]
    hit_text = ["bell", "bell", "", "bell", "bell", "", "bell", "bell"]
    start_x = 144
    for idx, label in enumerate(labels):
        x = start_x + idx * 166
        draw_hit(draw, x, 746, label, hit_colors[idx], size=24 if label == "&" else 26)
        if hit_text[idx]:
            draw.text((x - 28, 800), hit_text[idx], fill="#5c554b", font=font(20, bold=True))

    draw_hit(draw, 1218, 672, "A", "#5a87ba", size=24)
    draw_hit(draw, 1360, 672, "E", "#5a87ba", size=24)
    draw_hit(draw, 1218, 828, "Dm9", "#4f8a66", size=20)
    draw_hit(draw, 1360, 828, "E7", "#4f8a66", size=20)

    draw.text((112, 876), "右手 bell 口令：打 - 提 - 空 - 提 - 打 - 空 - 打 - 提", fill="#ba7a37", font=font(25, bold=True))
    draw.text((824, 876), "左手：A pedal 或 Am6 - Dm9 - E7", fill="#4f8265", font=font(26, bold=True))

    draw.rounded_rectangle((92, 932, 1464, 978), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (112, 943),
        "钢琴练法：先让右手在高音区把 bell pattern 弹稳，再把左手低音和和弦轻轻铺进去。重点不是和弦多复杂，而是高频时间线不能漂。",
        fill="#5f564b",
        font=font(21, bold=True),
    )

    img.save(ASSET_DIR / "piano-mambo-bell-pattern.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：把 Mambo Bell Pattern 转成闷音加高把位切分", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他没有真的铃，但可以用高把位三和弦、闷音与短促重音，模拟 bell 的明亮落点。关键是右手动作持续，开和弦只落在指定格子。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am6 x A5 x | D9 x E7 E7 |。先把每个 8 分格子的手腕动作做出来，再让开和弦只点亮 bell 落点。", fill="#223943", font=font(26, bold=True))
    draw.text((114, 260), "如果每个格子都扫实，bell 会消失；如果只在出声时才动手，律动会塌。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am6", "x 0 2 2 1 2", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1"), (2, 5, "4")], {0: "X", 1: "O"}, "第一拍与后半拍先做出双落点。", "#2f8b61"),
        ("A5", "5 7 7 x x x", [(1, 0, "1"), (3, 1, "3"), (3, 2, "4")], {}, "高把位 power chord 模拟 bell 的亮点。", "#c97b3f"),
        ("D9", "x 5 4 5 5 x", [(1, 1, "1"), (1, 2, "2"), (1, 3, "3"), (1, 4, "4")], {0: "X", 5: "X"}, "第二小节先换色，再保留空位。", "#5c7db8"),
        ("E7", "0 2 0 1 0 0", [(2, 1, "2"), (1, 3, "1")], {0: "O", 2: "O", 4: "O", 5: "O"}, "末尾双击给出下一轮的拉力。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：点 - 提 - 空 - 提 - 点 - 空 - 点 - 提。想象自己在弹一条高频 bell 时间线，而不是普通扫弦。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-mambo-bell-pattern.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Mambo Bell Pattern", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Mambo bell 常被理解成 Afro-Cuban 编制里的高频时间线。它延续了 cascara 的连续性，但用更明亮、更明确的落点把脉搏抬到高处。",
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
        ("bell 落点", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 1, 3, 4, 6, 7], [], "bell 的特点是双落点更多，高频推进感更强。"),
        ("和 cascara 对照", ["壳", "壳", "空", "壳", "亮", "空", "亮", "亮"], [4, 6, 7], [0, 1, 3], "前半仍像壳线，后半更像被 bell 提亮。"),
        ("演奏理解", ["点", "提", "空", "提", "点", "空", "点", "提"], [0, 4, 6], [1, 3, 7], "先练身体动作连续，再决定哪些格子真正出声。"),
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
            state = "accent" if i in accents else ("support" if i in supports else "rest")
            center_text(draw, (x0, y + 70, x1, y + 118), state, txt if i in accents or i in supports else "#667485", font(19, bold=i in accents or i in supports))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((122, 840), "听感重点：Cascara 让时间线持续存在，Mambo Bell Pattern 则把其中几个落点提得更亮，让整支乐队更容易抓住前冲方向。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "mambo-bell-pattern-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
