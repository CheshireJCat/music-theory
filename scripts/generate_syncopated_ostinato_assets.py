from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-30-syncopated-ostinato"
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


def draw_note(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str):
    draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 20, y - 16, x + 20, y + 14), label, "#ffffff", font(18, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f6f2eb")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Syncopated Ostinato 切分持续音型", fill="#2f261e", font=font(54, bold=True))
    draw.text(
        (52, 104),
        "重点变化不是换掉低音型，而是把重音故意放到弱拍或拍子的后半段。这样同一条循环会从“稳步推进”变成“被往前推着走”。",
        fill="#675a4d",
        font=font(28),
    )

    panels = [
        ((74, 186, 486, 872), "#edf4ff", "#b2c5df", "低音型", "A - G - F - E", "音高顺序保持稳定", "#456d9a"),
        ((574, 186, 986, 872), "#fff3e8", "#dec6a3", "切分节奏", "休止 + 反拍进入", "不要总落在强拍 1 和 3", "#b97a33"),
        ((1074, 186, 1486, 872), "#edf7ef", "#adcbb3", "听感结果", "前冲感", "循环像被持续往前推", "#4d7f63"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 224), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 288), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 374), desc, fill="#5f6870", font=font(29))

    note_positions = [
        ("A", 152, 788, "#456d9a"),
        ("G", 238, 726, "#456d9a"),
        ("F", 324, 788, "#456d9a"),
        ("E", 410, 726, "#456d9a"),
        ("&", 652, 726, "#c68243"),
        ("2", 738, 788, "#c68243"),
        ("&", 824, 726, "#c68243"),
        ("4", 910, 788, "#c68243"),
        ("A", 1156, 726, "#4f8a66"),
        ("G", 1242, 788, "#4f8a66"),
        ("F", 1328, 726, "#4f8a66"),
        ("E", 1414, 788, "#4f8a66"),
    ]
    for note, x, y, color in note_positions:
        draw_note(draw, x, y, note, color)

    draw.line((486, 738, 574, 738), fill="#9cadbf", width=7)
    draw.polygon([(574, 738), (552, 724), (552, 752)], fill="#9cadbf")
    draw.line((986, 738, 1074, 738), fill="#d1ab7a", width=7)
    draw.polygon([(1074, 738), (1052, 724), (1052, 752)], fill="#d1ab7a")

    draw.rounded_rectangle((92, 896, 1464, 944), 18, fill="#fffdfa", outline="#d5cbbe", width=2)
    draw.text(
        (118, 907),
        "钢琴练法：左手保持 A - G - F - E 不变，但把每次进入点放在反拍。先数 “1-and-2-and-3-and-4-and”，再在 and 上下键。",
        fill="#5f564b",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "piano-syncopated-ostinato.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 118
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 304, y + 470), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#21323a", font=font(34, bold=True))
    draw.text((x + 28, y + 72), subtitle, fill="#66757d", font=font(20))

    for i in range(6):
        sx = grid_left + i * string_gap
        draw.line((sx, grid_top, sx, grid_top + 4 * fret_gap), fill="#2d3748", width=4)
    for i in range(5):
        sy = grid_top + i * fret_gap
        draw.line((grid_left, sy, grid_left + 5 * string_gap, sy), fill="#2d3748", width=8 if i == 0 else 4)

    for fret, string_idx, label in dots:
        cx = grid_left + string_idx * string_gap
        cy = grid_top + (fret - 0.5) * fret_gap
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#ffffff", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#56656f", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 246, sx + 12, grid_top + 278), name, "#56656f", font(16, bold=True))

    draw.text((x + 28, y + 404), footnote, fill="#52656e", font=font(17))


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#edf4f5")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：Syncopated Ostinato 的切分循环", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上可以保持 Am - G - F - E 的熟悉低音路线，但把扫弦或分解的重心故意放在反拍。听感会立刻从“稳”变成“推”。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 204), "建议右手先做两步：第 1 拍轻落空，第 1 拍后半或第 2 拍前半补进来。这样不会破坏低音顺序，却能把节奏重心从强拍移开。", fill="#223943", font=font(27, bold=True))
    draw.text((114, 260), "最实用的起步法：拇指继续负责 A -> G -> F -> E，食指或扫弦动作专门去强调 “and” 的位置。先慢速数拍，再加流畅性。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am", "x 0 2 2 1 0", [(2, 2, "2"), (2, 3, "3"), (1, 4, "1")], {0: "X", 1: "O", 5: "O"}, "第 1 个循环先故意晚半拍进入。", "#2f8b61"),
        ("G", "3 2 0 0 0 3", [(3, 0, "2"), (2, 1, "1"), (3, 5, "3")], {2: "O", 3: "O", 4: "O"}, "低音到 G，但重音放在反拍。", "#c97b3f"),
        ("F", "1 3 3 2 1 1", [(1, 0, "1"), (3, 1, "3"), (3, 2, "4"), (2, 3, "2"), (1, 4, "1"), (1, 5, "1")], {}, "F 保持下行，同时延续切分感。", "#5c7db8"),
        ("E", "0 2 2 1 0 0", [(2, 1, "2"), (2, 2, "3"), (1, 3, "1")], {0: "O", 4: "O", 5: "O"}, "E 常带来属功能的回拉。", "#a15b6b"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    for start, end, color in [(392, 418, "#95a1a7"), (706, 716, "#b9986f"), (1020, 1030, "#95a1a7")]:
        draw.line((start, 652, end, 652), fill=color, width=7)
        draw.polygon([(end, 652), (end - 18, 640), (end - 18, 664)], fill=color)

    rhythm_box = (86, 932, 1474, 1028)
    draw.rounded_rectangle(rhythm_box, 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 960),
        "右手口令：空一下，再进来。数拍时说 “1-and-2-and-3-and-4-and”，把扫弦落在 and 上，比全落强拍更像切分持续音型。",
        fill="#4d5f68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-syncopated-ostinato.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "节奏结构图：Syncopated Ostinato", fill="#2d261d", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "核心不是换一条新低音，而是把同一条重复型的进入点、重音位置故意挪到弱拍或反拍。切分会让循环更有推动力。",
        fill="#655a4e",
        font=font(27),
    )

    lane_top = 240
    lane_left = 96
    beat_w = 160
    lane_h = 132
    row_gap = 56
    accent_fill = "#d9803d"
    base_fill = "#e6ecf4"

    rows = [
        ("普通 ostinato", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 2, 4, 6], "重音大多落在拍点上，稳定但较直。"),
        ("切分 ostinato", ["1", "&", "2", "&", "3", "&", "4", "&"], [1, 3, 5, 7], "重音移到反拍，听感更向前推。"),
    ]

    for row_idx, (label, cells, accents, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 52), label, fill="#3f3428", font=font(32, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * beat_w
            x1 = x0 + beat_w - 16
            fill = accent_fill if i in accents else base_fill
            outline = "#b86930" if i in accents else "#b7c2d0"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline, width=3)
            center_text(draw, (x0, y + 14, x1, y + 64), cell, "#ffffff" if i in accents else "#4a5766", font(28, bold=True))
            center_text(draw, (x0, y + 64, x1, y + 116), "hit" if i in accents else "rest", "#ffffff" if i in accents else "#667485", font(24, bold=i in accents))
        draw.text((lane_left, y + 150), desc, fill="#5f564b", font=font(24))

    draw.rounded_rectangle((96, 688, 1404, 858), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text((126, 726), "应用顺序", fill="#8b5a24", font=font(30, bold=True))
    draw.text((126, 776), "1. 先把低音顺序练稳  2. 再把重音移到反拍  3. 最后让上层和弦或旋律跟着切分呼吸", fill="#5f5547", font=font(26))
    draw.text((126, 818), "最容易错的点：一切分就把速度拉快。真正需要变化的是重音位置，不是节拍本身。", fill="#5f5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "syncopated-ostinato-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
