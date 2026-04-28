from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-20-major-triad"
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
    img = Image.new("RGB", (1200, 800), "#f7f1e3")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    label = font(36, bold=True)
    body = font(28)

    draw.rounded_rectangle((60, 50, 1140, 740), radius=30, fill="#fffaf0", outline="#d9c7a1", width=4)
    draw.text((100, 95), "C 大三和弦的构成", fill="#3d2c1e", font=title)
    draw.text((100, 165), "Major Triad = 根音 + 大三度 + 纯五度", fill="#8a5a24", font=body)

    circles = [
        ((185, 350, 385, 550), "#d1495b", "C", "根音"),
        ((500, 350, 700, 550), "#edae49", "E", "大三度"),
        ((815, 350, 1015, 550), "#00798c", "G", "纯五度"),
    ]
    for box, color, note, desc in circles:
        draw.ellipse(box, fill=color, outline="#ffffff", width=8)
        draw_center(draw, box, note, "#ffffff", font(88, bold=True))
        draw.text((box[0] + 55, box[3] + 28), desc, fill="#3d2c1e", font=label)

    draw.line((385, 450, 500, 450), fill="#5c4d3d", width=8)
    draw.polygon([(500, 450), (474, 434), (474, 466)], fill="#5c4d3d")
    draw.text((410, 385), "4 个半音", fill="#5c4d3d", font=label)

    draw.line((700, 450, 815, 450), fill="#5c4d3d", width=8)
    draw.polygon([(815, 450), (789, 434), (789, 466)], fill="#5c4d3d")
    draw.text((725, 385), "3 个半音", fill="#5c4d3d", font=label)

    draw.text((110, 655), "听感关键词：明亮、稳定、开放", fill="#3d2c1e", font=body)
    img.save(ASSET_DIR / "interval-structure.png")


def save_piano_chart():
    img = Image.new("RGB", (1400, 650), "#f3f6fb")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(30)
    note_font = font(34, bold=True)

    draw.text((80, 50), "钢琴示意：C 大三和弦", fill="#1f2937", font=title)
    draw.text((80, 125), "高亮根音 C、大三度 E、纯五度 G", fill="#4b5563", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    selected = {"C": "#d1495b", "E": "#edae49", "G": "#00798c"}
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
        if name in selected and not (i == 7 and name == "C"):
            draw.rounded_rectangle((x + 20, y0 + 205, x + white_w - 20, y0 + white_h - 25), 18, fill=selected[name])
            draw_center(draw, (x + 20, y0 + 205, x + white_w - 20, y0 + white_h - 25), name, "#ffffff", note_font)
        else:
            draw_center(draw, (x, y0 + 255, x + white_w, y0 + white_h), name, "#374151", note_font)

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#", "D#", "F#", "G#", "A#"]
    black_w = 90
    black_h = 210
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 12, fill="#111827")
        draw_center(draw, (x, y0 + 135, x + black_w, y0 + black_h), name, "#f9fafb", font(21, bold=True))

    legend_y = 590
    legend = [("C 根音", "#d1495b"), ("E 大三度", "#edae49"), ("G 纯五度", "#00798c")]
    lx = 140
    for text, color in legend:
        draw.rounded_rectangle((lx, legend_y - 16, lx + 36, legend_y + 20), 8, fill=color)
        draw.text((lx + 55, legend_y - 22), text, fill="#1f2937", font=body)
        lx += 300

    img.save(ASSET_DIR / "piano-c-major.png")


def save_guitar_chart():
    img = Image.new("RGB", (1000, 1300), "#fff7ed")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)
    note_font = font(32, bold=True)

    draw.text((80, 55), "吉他 C 大三和弦开放按法", fill="#7c2d12", font=title)
    draw.text((80, 125), "从 A 弦到 e 弦拨弦，最低 E 弦不弹", fill="#9a3412", font=body)

    left = 180
    top = 260
    string_gap = 100
    fret_gap = 150
    strings = ["E", "A", "D", "G", "B", "e"]

    for i, s in enumerate(strings):
        x = left + i * string_gap
        draw.line((x, top, x, top + fret_gap * 4), fill="#4b5563", width=4)
        draw.text((x - 10, top - 70), s, fill="#7c2d12", font=note_font)

    for i in range(5):
        y = top + i * fret_gap
        width = 14 if i == 0 else 5
        draw.line((left, y, left + string_gap * 5, y), fill="#1f2937", width=width)

    fret_labels = ["1", "2", "3"]
    for i, fl in enumerate(fret_labels, start=1):
        y = top + fret_gap * i - fret_gap / 2
        draw.text((80, y - 20), fl, fill="#9a3412", font=note_font)

    markers = [
        (1, 3, "#d1495b", "3", "C"),
        (2, 2, "#edae49", "2", "E"),
        (4, 1, "#00798c", "1", "C"),
    ]
    for string_idx, fret, color, finger, note in markers:
        x = left + string_gap * string_idx
        y = top + fret_gap * (fret - 0.5)
        draw.ellipse((x - 42, y - 42, x + 42, y + 42), fill=color, outline="#ffffff", width=6)
        draw_center(draw, (x - 42, y - 42, x + 42, y + 42), finger, "#ffffff", note_font)
        draw.text((x - 22, y + 65), note, fill="#7c2d12", font=body)

    open_strings = [(5, "E"), (3, "G")]
    for string_idx, note in open_strings:
        x = left + string_gap * string_idx
        draw.ellipse((x - 25, top - 135, x + 25, top - 85), outline="#16a34a", width=6)
        draw.text((x - 14, top - 195), note, fill="#166534", font=body)

    mute_x = left
    draw.line((mute_x - 22, top - 140, mute_x + 22, top - 96), fill="#dc2626", width=7)
    draw.line((mute_x + 22, top - 140, mute_x - 22, top - 96), fill="#dc2626", width=7)

    draw.rounded_rectangle((80, 980, 920, 1200), 24, fill="#ffedd5", outline="#fdba74", width=3)
    draw.text((120, 1020), "实际响弦音：C - E - G - C - E", fill="#7c2d12", font=font(36, bold=True))
    draw.text((120, 1090), "手指：无名指按 A3，中指按 D2，食指按 B1", fill="#9a3412", font=body)
    draw.text((120, 1145), "用途：民谣伴奏、流行和弦进行、基础扫弦训练", fill="#9a3412", font=body)

    img.save(ASSET_DIR / "guitar-c-major.png")


if __name__ == "__main__":
    save_interval_chart()
    save_piano_chart()
    save_guitar_chart()
