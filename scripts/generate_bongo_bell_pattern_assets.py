from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-12-bongo-bell-pattern"
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
    draw.rounded_rectangle((x - 46, y - 30, x + 46, y + 30), 18, fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 40, y - 22, x + 40, y + 22), label, "#ffffff", font(size, bold=True))


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
    img = Image.new("RGB", (1560, 1000), "#f4efe7")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Bongo Bell Pattern 的持续驱动", fill="#2f251d", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Bongo bell 比 mambo bell 更像一条持续往前滚动的小齿轮。钢琴上常把它放在右手中高音区，左手则维持 bass tumbao 或 pedal。",
        fill="#68584A",
        font=font(28),
    )

    panels = [
        ((74, 184, 486, 900), "#fff5ea", "#dfc7a7", "时间功能", "小而密的驱动层", "它不像大铃那样强调编制中的“号召感”，而是更像稳定、持续的推力来源。", "#ba7a37"),
        ((574, 184, 986, 900), "#eef4ff", "#b2c5df", "和 mambo bell 关系", "少一点宣告，多一点滚动", "mambo bell 更亮更外放，bongo bell 更常连续挂在 groove 里当细密推进器。", "#476f9d"),
        ((1074, 184, 1486, 900), "#eef8f0", "#afccb5", "钢琴应用", "右手固定小动机", "右手可用单音或双音反复敲出 bell，左手维持 A-C-E-G 的低音层或简化 pedal。", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 222), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 286), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 372), desc, fill="#5f6870", font=font(27))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    hit_colors = ["#c68445", "#e6ecf4", "#5a87ba", "#c68445", "#e6ecf4", "#5a87ba", "#c68445", "#e6ecf4"]
    hit_text = ["hit", "", "push", "hit", "", "push", "hit", ""]
    start_x = 144
    for idx, label in enumerate(labels):
        x = start_x + idx * 166
        draw_hit(draw, x, 746, label, hit_colors[idx], size=24 if label == "&" else 26)
        if hit_text[idx]:
            draw.text((x - 26, 800), hit_text[idx], fill="#5c554b", font=font(20, bold=True))

    draw_hit(draw, 1218, 672, "A", "#5a87ba", size=24)
    draw_hit(draw, 1360, 672, "E", "#5a87ba", size=24)
    draw_hit(draw, 1218, 828, "Dm9", "#4f8a66", size=20)
    draw_hit(draw, 1360, 828, "E7", "#4f8a66", size=20)

    draw.text((112, 876), "右手口令：打 - 空 - 推 - 打 - 空 - 推 - 打 - 空", fill="#ba7a37", font=font(25, bold=True))
    draw.text((796, 876), "左手：A pedal 或 A - C - E - G 的低音分解", fill="#4f8265", font=font(26, bold=True))

    draw.rounded_rectangle((92, 932, 1464, 978), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (110, 943),
        "钢琴练法：先把右手的三次落点练成不抢拍的连续推动，再加左手低音。听感要像小齿轮一直转，不像大铃在上面发号施令。",
        fill="#5f564b",
        font=font(21, bold=True),
    )

    img.save(ASSET_DIR / "piano-bongo-bell-pattern.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：把 Bongo Bell Pattern 变成轻短切分与高位双音", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他可以用高把位双音、闷音和短促上拨来模拟 bongo bell。重点不是大扫弦，而是把短而密的推动维持在同一条线上。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am7 x C6 x | D9 x E7 x |。闷音保持 8 分脉搏，开和弦只在 bell 的三次落点上点亮。", fill="#223943", font=font(26, bold=True))
    draw.text((114, 260), "如果开和弦太长，它就会变普通拉丁扫弦；如果闷音太弱，持续驱动会消失。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am7", "5 7 5 5 5 5", [(1, 0, "1"), (3, 1, "3"), (1, 2, "1"), (1, 3, "1"), (1, 4, "1"), (1, 5, "1")], {}, "第一拍用高把位 barre 做短促亮点。", "#2f8b61"),
        ("C6", "x 3 2 2 1 0", [(3, 1, "3"), (2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 5: "O"}, "第二次落点换成更柔和的色彩。", "#c97b3f"),
        ("D9", "x 5 4 5 5 x", [(1, 1, "1"), (1, 2, "2"), (1, 3, "3"), (1, 4, "4")], {0: "X", 5: "X"}, "后半拍推力可以用更薄的和弦层。", "#5c7db8"),
        ("E7", "0 2 0 1 0 0", [(2, 1, "2"), (1, 3, "1")], {0: "O", 2: "O", 4: "O", 5: "O"}, "回到 E7 后别拖拍，保持短促。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：下 - 空 - 上 - 下 - 空 - 上 - 下 - 空。把它想成持续滚动的 bell，不是三次孤立重拍。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-bongo-bell-pattern.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Bongo Bell Pattern", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Bongo bell 可以看成小编制里持续存在的高频驱动层。它比 mambo bell 更像一条滚动时间线，常把 groove 维持得细密、轻巧、不断气。",
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
        ("bell 落点", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 6], [2, 5], "主落点落在 1、2 的后半和 4 前，形成不断往前推的细密感觉。"),
        ("身体动作", ["下", "留", "上", "下", "留", "上", "下", "留"], [0, 3, 6], [2, 5], "先保证手或身体的动作连续，再让指定格子真正发声。"),
        ("和 mambo bell 对比", ["更小", "更稳", "推", "更小", "更稳", "推", "更小", "留"], [2, 5], [0, 3, 6], "mambo bell 更亮更宣告，bongo bell 更像一直在转的推进器。"),
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
            state = "hit" if i in accents else ("push" if i in supports else "space")
            center_text(draw, (x0, y + 70, x1, y + 118), state, txt if i in accents or i in supports else "#667485", font(19, bold=i in accents or i in supports))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((122, 840), "听感重点：Bongo Bell Pattern 的核心不是“大铃式宣告”，而是用较小、较密的高频落点把整个 groove 持续往前推。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "bongo-bell-pattern-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
