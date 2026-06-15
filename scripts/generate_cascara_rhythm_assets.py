from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-10-cascara-rhythm"
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


def draw_hit(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str):
    draw.rounded_rectangle((x - 40, y - 28, x + 40, y + 28), 18, fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 34, y - 20, x + 34, y + 20), label, "#ffffff", font(18, bold=True))


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
    img = Image.new("RGB", (1560, 980), "#f5efe6")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Cascara Rhythm 的稳定外壳", fill="#30261B", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Cascara 是鼓手敲 timbale 鼓壳时形成的稳定时间型。放到钢琴上，可以把左手当作时间线，右手只在关键落点补和弦。",
        fill="#68584A",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 872), "#fff3e7", "#dfc7a7", "时间功能", "稳住 8 分框架", "它不像 clave 那样只给骨架，而是持续告诉乐队“格子在哪”。", "#ba7a37"),
        ((574, 186, 986, 872), "#eef4ff", "#b2c5df", "和 clave 关系", "互相咬合", "clave 决定句法重心，cascara 负责把流动感铺满。", "#476f9d"),
        ((1074, 186, 1486, 872), "#eef8f0", "#afccb5", "钢琴应用", "低音 + 和弦点缀", "左手守时间线，右手在后拍插入色彩和回应。", "#4f8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 288), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 374), desc, fill="#5f6870", font=font(27))

    time_line = [
        ("1", 168, 742, "#c68445"),
        ("&", 304, 688, "#c68445"),
        ("2", 440, 742, "#c68445"),
        ("&", 576, 688, "#c68445"),
        ("3", 712, 742, "#476f9d"),
        ("&", 848, 688, "#476f9d"),
        ("4", 984, 742, "#476f9d"),
        ("&", 1120, 688, "#476f9d"),
    ]
    for label, x, y, tone in time_line:
        draw_hit(draw, x, y, label, tone)

    chord_hits = [("Am6", 1192, 756), ("Dm9", 1320, 692), ("E7", 1440, 756)]
    for label, x, y in chord_hits:
        draw_hit(draw, x, y, label, "#4f8a66")

    draw.text((104, 804), "左手口令：踏 - 提 - 踏 - 提", fill="#ba7a37", font=font(27, bold=True))
    draw.text((608, 804), "感觉：不是抢拍，而是连续给出时间外壳", fill="#476f9d", font=font(27, bold=True))
    draw.text((1124, 804), "右手：Am6 - Dm9 - E7", fill="#4f8265", font=font(28, bold=True))

    draw.rounded_rectangle((92, 896, 1464, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (112, 907),
        "钢琴练法：先用左手单音拍出 cascara 的连续时间线，再在右手只放少量和弦。你要先听见“壳”的连续感，再听见和弦颜色。",
        fill="#5f564b",
        font=font(22, bold=True),
    )

    img.save(ASSET_DIR / "piano-cascara-rhythm.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf3f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：Cascara Rhythm 的切分伴奏入口", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上练 cascara，不是一路扫八分，而是把时间线拆成稳定的闷音与少量开和弦。这样才能既稳，又有 Afro-Cuban 的弹性。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "入门循环：| Am6 x x Am6 | Dm9 x E7 x |。用闷音把外壳铺平，再把和弦放进指定落点。", fill="#223943", font=font(26, bold=True))
    draw.text((114, 260), "如果把每个 8 分都扫成同样力度，cascara 会塌成普通分解伴奏，失去“壳”的骨感。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am6", "x 0 2 2 1 2", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1"), (2, 5, "4")], {0: "X", 1: "O"}, "第一落点给温和重音，后面留呼吸。", "#2f8b61"),
        ("Am6", "x 0 2 2 1 2", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1"), (2, 5, "4")], {0: "X", 1: "O"}, "空位先用闷音，不要补满扫弦。", "#c97b3f"),
        ("Dm9", "x 5 3 5 5 5", [(3, 1, "1"), (2, 2, "2"), (3, 3, "3"), (3, 4, "4"), (3, 5, "4")], {0: "X"}, "第二小节先把律动重新抬起来。", "#5c7db8"),
        ("E7", "0 2 0 1 0 0", [(2, 1, "2"), (1, 3, "1")], {0: "O", 2: "O", 4: "O", 5: "O"}, "最后给属和弦回应，保留下一轮弹性。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：闷 - 提 - 点 - 提。先让闷音形成鼓壳感，再把 Am6、Dm9、E7 放进固定格子里。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-cascara-rhythm.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Cascara Rhythm", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Cascara 是一种持续的时间型。和只给五击骨架的 clave 相比，它更像把整条时间外壳铺在乐队上，让其他声部可以往里挂靠。",
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
        ("连续时间格", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 1, 3, 4, 6, 7], [], "壳线会持续告诉你每个八分格子在哪里。"),
        ("和 clave 咬合", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 6], [1, 4, 7], "橙色是主重音，蓝色是支撑性提点。"),
        ("伴奏理解", ["低", "提", "空", "点", "低", "提", "点", "提"], [0, 4], [1, 3, 5, 6, 7], "先有稳定低音，再用提点与和弦把壳补完整。"),
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
            state = "main" if i in accents else ("support" if i in supports else "rest")
            center_text(draw, (x0, y + 70, x1, y + 118), state, txt if i in accents or i in supports else "#667485", font(19, bold=i in accents or i in supports))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((122, 840), "听感重点：clave 像“句法骨架”，cascara 像“稳定外壳”。你要同时听见前者的重心和后者的持续流动。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "cascara-rhythm-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
