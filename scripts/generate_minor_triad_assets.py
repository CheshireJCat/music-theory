from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-20-minor-triad"
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


def save_interval_chart():
    img = Image.new("RGB", (1200, 800), "#eef2f7")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    label = font(36, bold=True)
    body = font(28)

    draw.rounded_rectangle((60, 50, 1140, 740), radius=30, fill="#f8fafc", outline="#b8c4d4", width=4)
    draw.text((100, 95), "A 小三和弦的构成", fill="#1f2937", font=title)
    draw.text((100, 165), "Minor Triad = 根音 + 小三度 + 纯五度", fill="#475569", font=body)

    circles = [
        ((185, 350, 385, 550), "#5b6c8f", "A", "根音"),
        ((500, 350, 700, 550), "#9a6fb0", "C", "小三度"),
        ((815, 350, 1015, 550), "#2a9d8f", "E", "纯五度"),
    ]
    for box, color, note, desc in circles:
        draw.ellipse(box, fill=color, outline="#ffffff", width=8)
        draw_center(draw, box, note, "#ffffff", font(88, bold=True))
        draw.text((box[0] + 48, box[3] + 28), desc, fill="#334155", font=label)

    draw.line((385, 450, 500, 450), fill="#475569", width=8)
    draw.polygon([(500, 450), (474, 434), (474, 466)], fill="#475569")
    draw.text((410, 385), "3 个半音", fill="#475569", font=label)

    draw.line((700, 450, 815, 450), fill="#475569", width=8)
    draw.polygon([(815, 450), (789, 434), (789, 466)], fill="#475569")
    draw.text((725, 385), "4 个半音", fill="#475569", font=label)

    draw.text((110, 655), "听感关键词：柔和、内省、略带忧郁", fill="#334155", font=body)
    img.save(ASSET_DIR / "interval-structure.png")


def save_piano_chart():
    img = Image.new("RGB", (1400, 650), "#f6f7fb")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(30)
    note_font = font(34, bold=True)

    draw.text((80, 50), "钢琴示意：A 小三和弦", fill="#1f2937", font=title)
    draw.text((80, 125), "高亮根音 A、小三度 C、纯五度 E", fill="#4b5563", font=body)

    white_names = ["A", "B", "C", "D", "E", "F", "G", "A"]
    selected = {"A": "#5b6c8f", "C": "#9a6fb0", "E": "#2a9d8f"}
    white_w = 150
    white_h = 340
    x0 = 80
    y0 = 220

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        fill = "#fffdf8"
        if i == 7:
            fill = "#f5f5f4"
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill=fill, outline="#111827", width=3)
        is_highlight = name in selected and not (i == 7 and name == "A")
        if is_highlight:
            draw.rounded_rectangle((x + 20, y0 + 205, x + white_w - 20, y0 + white_h - 25), 18, fill=selected[name])
            draw_center(draw, (x + 20, y0 + 205, x + white_w - 20, y0 + white_h - 25), name, "#ffffff", note_font)
        else:
            draw_center(draw, (x, y0 + 255, x + white_w, y0 + white_h), name, "#374151", note_font)

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["A#", "C#", "D#", "F#", "G#"]
    black_w = 90
    black_h = 210
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 12, fill="#111827")
        draw_center(draw, (x, y0 + 135, x + black_w, y0 + black_h), name, "#f9fafb", font(21, bold=True))

    legend_y = 590
    legend = [("A 根音", "#5b6c8f"), ("C 小三度", "#9a6fb0"), ("E 纯五度", "#2a9d8f")]
    lx = 130
    for text, color in legend:
        draw.rounded_rectangle((lx, legend_y - 16, lx + 36, legend_y + 20), 8, fill=color)
        draw.text((lx + 55, legend_y - 22), text, fill="#1f2937", font=body)
        lx += 320

    img.save(ASSET_DIR / "piano-a-minor.png")


def save_guitar_chart():
    img = Image.new("RGB", (1000, 1300), "#f7f4fb")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)
    note_font = font(32, bold=True)

    draw.text((80, 55), "吉他 A 小三和弦开放按法", fill="#4c1d95", font=title)
    draw.text((80, 125), "从 A 弦到 e 弦拨弦，最低 E 弦不弹", fill="#6d28d9", font=body)

    left = 180
    top = 260
    string_gap = 100
    fret_gap = 150
    strings = ["E", "A", "D", "G", "B", "e"]

    for i, s in enumerate(strings):
        x = left + i * string_gap
        draw.line((x, top, x, top + fret_gap * 4), fill="#4b5563", width=4)
        draw.text((x - 10, top - 70), s, fill="#4c1d95", font=note_font)

    for i in range(5):
        y = top + i * fret_gap
        width = 14 if i == 0 else 5
        draw.line((left, y, left + string_gap * 5, y), fill="#1f2937", width=width)

    fret_labels = ["1", "2", "3"]
    for i, fl in enumerate(fret_labels, start=1):
        y = top + fret_gap * i - fret_gap / 2
        draw.text((80, y - 20), fl, fill="#6d28d9", font=note_font)

    markers = [
        (2, 2, "#5b6c8f", "2", "E"),
        (3, 2, "#9a6fb0", "3", "A"),
        (4, 1, "#2a9d8f", "1", "C"),
    ]
    for string_idx, fret, color, finger, note in markers:
        x = left + string_gap * string_idx
        y = top + fret_gap * (fret - 0.5)
        draw.ellipse((x - 42, y - 42, x + 42, y + 42), fill=color, outline="#ffffff", width=6)
        draw_center(draw, (x - 42, y - 42, x + 42, y + 42), finger, "#ffffff", note_font)
        draw.text((x - 34, y + 65), note, fill="#4c1d95", font=body)

    open_strings = [(1, "A"), (5, "E")]
    for string_idx, note in open_strings:
        x = left + string_gap * string_idx
        draw.ellipse((x - 25, top - 135, x + 25, top - 85), outline="#16a34a", width=6)
        draw.text((x - 13, top - 195), note, fill="#166534", font=body)

    mute_x = left
    draw.line((mute_x - 22, top - 140, mute_x + 22, top - 96), fill="#dc2626", width=7)
    draw.line((mute_x + 22, top - 140, mute_x - 22, top - 96), fill="#dc2626", width=7)

    draw.rounded_rectangle((80, 980, 920, 1200), 24, fill="#ede9fe", outline="#c4b5fd", width=3)
    draw.text((120, 1020), "常见形状：x02210", fill="#4c1d95", font=font(36, bold=True))
    draw.text((120, 1090), "用途：抒情伴奏、流行编配、Am-F-C-G 进行", fill="#5b21b6", font=body)
    draw.text((120, 1145), "注意：1 指按 B1，2 指按 D2，3 指按 G2", fill="#5b21b6", font=body)

    img.save(ASSET_DIR / "guitar-a-minor.png")


if __name__ == "__main__":
    save_interval_chart()
    save_piano_chart()
    save_guitar_chart()
