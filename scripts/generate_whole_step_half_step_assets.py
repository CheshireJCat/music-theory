from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-23-whole-step-half-step"
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


def draw_center(draw: ImageDraw.ImageDraw, box, text, fill, text_font):
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=text_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = left + (right - left - tw) / 2
    y = top + (bottom - top - th) / 2 - 2
    draw.text((x, y), text, fill=fill, font=text_font)


def arrow(draw, start, end, color, width=8):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    draw.polygon([(x2, y2), (x2 - 24, y2 - 16), (x2 - 24, y2 + 16)], fill=color)


def save_piano_chart():
    img = Image.new("RGB", (1500, 780), "#f5efe2")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(30)
    small = font(24)
    note_font = font(32, bold=True)

    draw.text((70, 50), "钢琴示意：半音与全音", fill="#2b261f", font=title)
    draw.text((70, 125), "半音 = 相邻琴键；全音 = 隔过一个半音后到达下一个音", fill="#675847", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 165
    white_h = 360
    x0 = 75
    y0 = 250
    key_centers = {}

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdf7", outline="#111827", width=3)
        draw_center(draw, (x, y0 + 260, x + white_w, y0 + white_h), name, "#334155", note_font)
        key_centers[f"{name}{i}"] = (x + white_w / 2, y0 + 140)

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 100
    black_h = 225
    black_centers = {}
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        draw_center(draw, (x, y0 + 138, x + black_w, y0 + black_h), name, "#f8fafc", font(20, bold=True))
        black_centers[name] = (x + black_w / 2, y0 + 70)

    c = key_centers["C0"]
    c_sharp = black_centers["C#/Db"]
    d = key_centers["D1"]
    e = key_centers["E2"]
    f = key_centers["F3"]

    draw.rounded_rectangle((c[0] - 42, y0 + 235, c[0] + 42, y0 + 320), 16, fill="#1f7a5a")
    draw_center(draw, (c[0] - 42, y0 + 235, c[0] + 42, y0 + 320), "C", "#ffffff", note_font)
    draw.rounded_rectangle((c_sharp[0] - 42, y0 + 30, c_sharp[0] + 42, y0 + 115), 16, fill="#d96c3f")
    draw_center(draw, (c_sharp[0] - 42, y0 + 30, c_sharp[0] + 42, y0 + 115), "C#", "#ffffff", note_font)
    draw.rounded_rectangle((d[0] - 42, y0 + 235, d[0] + 42, y0 + 320), 16, fill="#2f67b1")
    draw_center(draw, (d[0] - 42, y0 + 235, d[0] + 42, y0 + 320), "D", "#ffffff", note_font)
    draw.rounded_rectangle((e[0] - 42, y0 + 235, e[0] + 42, y0 + 320), 16, fill="#8d5bb8")
    draw_center(draw, (e[0] - 42, y0 + 235, e[0] + 42, y0 + 320), "E", "#ffffff", note_font)
    draw.rounded_rectangle((f[0] - 42, y0 + 235, f[0] + 42, y0 + 320), 16, fill="#d6a432")
    draw_center(draw, (f[0] - 42, y0 + 235, f[0] + 42, y0 + 320), "F", "#ffffff", note_font)

    arrow(draw, (c[0] + 30, y0 + 180), (c_sharp[0] - 25, y0 + 90), "#d96c3f")
    draw.text((115, 205), "C -> C#：半音", fill="#9f3d20", font=font(28, bold=True))
    arrow(draw, (c[0] + 28, y0 + 380), (d[0] - 28, y0 + 380), "#2f67b1")
    draw.text((170, 650), "C -> D：全音 = 两个半音", fill="#224f8d", font=font(28, bold=True))
    arrow(draw, (e[0] + 25, y0 + 190), (f[0] - 25, y0 + 190), "#d6a432")
    draw.text((455, 205), "E -> F：白键相邻，也是半音", fill="#896614", font=font(28, bold=True))

    draw.rounded_rectangle((970, 650, 1420, 720), 18, fill="#fff7ed", outline="#d6a432", width=3)
    draw.text((1000, 666), "记忆点：相邻琴键才是半音，不一定是黑键。", fill="#5b4630", font=small)

    img.save(ASSET_DIR / "piano-whole-half-step.png")


def save_guitar_chart():
    img = Image.new("RGB", (1200, 850), "#edf5f7")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(30)
    note_font = font(32, bold=True)

    draw.text((70, 50), "吉他示意：一个品格 = 一个半音", fill="#16313d", font=title)
    draw.text((70, 122), "同一根弦上移动 1 品是半音，移动 2 品是全音", fill="#45616d", font=body)

    left = 135
    right = 1080
    top = 255
    string_gap = 78
    fret_gap = 135
    strings = ["E", "A", "D", "G", "B", "e"]

    for i, s in enumerate(strings):
        y = top + i * string_gap
        draw.line((left, y, right, y), fill="#475569", width=5 if i < 3 else 4)
        draw.text((70, y - 20), s, fill="#16313d", font=note_font)

    for i in range(8):
        x = left + i * fret_gap
        draw.line((x, top - 35, x, top + string_gap * 5 + 35), fill="#1e293b", width=6 if i == 0 else 4)
        if i > 0:
            draw.text((x - fret_gap / 2 - 8, top - 95), str(i), fill="#45616d", font=note_font)

    string_y = top + string_gap * 1
    notes = [
        (3, "C", "#1f7a5a"),
        (4, "C#", "#d96c3f"),
        (5, "D", "#2f67b1"),
    ]
    for fret, label, color in notes:
        x = left + fret_gap * (fret - 0.5)
        draw.ellipse((x - 43, string_y - 43, x + 43, string_y + 43), fill=color, outline="#ffffff", width=6)
        draw_center(draw, (x - 43, string_y - 43, x + 43, string_y + 43), label, "#ffffff", note_font)

    x3 = left + fret_gap * 2.5
    x4 = left + fret_gap * 3.5
    x5 = left + fret_gap * 4.5
    arrow(draw, (x3 + 56, string_y - 86), (x4 - 56, string_y - 86), "#d96c3f")
    draw.text((x3 + 20, string_y - 155), "3品 C -> 4品 C#：半音", fill="#9f3d20", font=font(28, bold=True))
    arrow(draw, (x3 + 56, string_y + 100), (x5 - 56, string_y + 100), "#2f67b1")
    draw.text((x3 + 45, string_y + 126), "3品 C -> 5品 D：全音", fill="#224f8d", font=font(28, bold=True))

    draw.rounded_rectangle((95, 655, 1105, 775), 24, fill="#ffffff", outline="#9ab3bd", width=3)
    draw.text((135, 682), "使用场景：推弦、滑音、旋律连接都在用半音/全音距离。", fill="#16313d", font=font(31, bold=True))
    draw.text((135, 728), "例：A弦 3-5 品是 C 到 D，适合练大调音阶的前两个音。", fill="#45616d", font=body)

    img.save(ASSET_DIR / "guitar-whole-half-step.png")


def save_structure_chart():
    img = Image.new("RGB", (1200, 760), "#f7f7ef")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(30)
    label = font(28, bold=True)

    draw.text((70, 55), "结构对比：半音 vs 全音", fill="#26231e", font=title)
    draw.text((70, 128), "半音是最小常用音高距离；全音由两个半音组成。", fill="#62594c", font=body)

    y1 = 285
    x0 = 135
    box = 90
    gap = 45
    draw.text((85, y1 - 65), "半音", fill="#9f3d20", font=font(36, bold=True))
    for i, (name, color) in enumerate([("C", "#1f7a5a"), ("C#", "#d96c3f")]):
        x = x0 + i * (box + gap)
        draw.rounded_rectangle((x, y1, x + box, y1 + box), 18, fill=color)
        draw_center(draw, (x, y1, x + box, y1 + box), name, "#ffffff", label)
    arrow(draw, (x0 + box + 12, y1 + box / 2), (x0 + box + gap - 12, y1 + box / 2), "#9f3d20", width=6)
    draw.text((390, y1 + 22), "1 个半音：紧张、靠近、很容易产生解决感", fill="#6f3b2a", font=body)

    y2 = 485
    draw.text((85, y2 - 65), "全音", fill="#224f8d", font=font(36, bold=True))
    for i, (name, color) in enumerate([("C", "#1f7a5a"), ("C#", "#d96c3f"), ("D", "#2f67b1")]):
        x = x0 + i * (box + gap)
        draw.rounded_rectangle((x, y2, x + box, y2 + box), 18, fill=color)
        draw_center(draw, (x, y2, x + box, y2 + box), name, "#ffffff", label)
        if i < 2:
            arrow(draw, (x + box + 12, y2 + box / 2), (x + box + gap - 12, y2 + box / 2), "#224f8d", width=6)
    draw.text((525, y2 + 22), "2 个半音：更开阔，是音阶向前走的常见步伐", fill="#2e4c79", font=body)

    draw.rounded_rectangle((700, 240, 1105, 585), 26, fill="#fffaf1", outline="#d0ae66", width=3)
    draw.text((735, 280), "快速判断", fill="#5c4425", font=font(38, bold=True))
    draw.text((735, 350), "钢琴：数相邻琴键", fill="#5c4425", font=body)
    draw.text((735, 405), "吉他：数移动品格", fill="#5c4425", font=body)
    draw.text((735, 460), "半音：1 格 / 1 键", fill="#9f3d20", font=body)
    draw.text((735, 515), "全音：2 格 / 2 键", fill="#224f8d", font=body)

    img.save(ASSET_DIR / "structure-whole-half-step.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
