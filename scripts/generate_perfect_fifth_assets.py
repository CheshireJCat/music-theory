from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-21-perfect-fifth"
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
    img = Image.new("RGB", (1200, 820), "#eef6f0")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    label = font(34, bold=True)
    body = font(28)

    draw.rounded_rectangle((60, 50, 1140, 760), radius=32, fill="#fbfff8", outline="#9bbf9f", width=4)
    draw.text((100, 92), "纯五度 Perfect Fifth", fill="#173b2f", font=title)
    draw.text((100, 165), "结构：根音向上 7 个半音，例：C 到 G", fill="#3f6b52", font=body)

    start = 125
    y = 365
    step_w = 76
    semitones = ["C", "C#", "D", "D#", "E", "F", "F#", "G"]
    for i, name in enumerate(semitones):
        x = start + i * step_w
        fill = "#f7f7ec"
        outline = "#365945"
        text_fill = "#365945"
        if name == "C":
            fill = "#2f6f4e"
            text_fill = "#ffffff"
        if name == "G":
            fill = "#d97941"
            text_fill = "#ffffff"
        draw.rounded_rectangle((x, y, x + 58, y + 58), 14, fill=fill, outline=outline, width=3)
        draw_center(draw, (x, y, x + 58, y + 58), name, text_fill, font(23, bold=True))
        if i < 7:
            draw.text((x + 64, y + 12), "+1", fill="#6b7f70", font=font(20, bold=True))

    draw.line((155, 525, 690, 525), fill="#173b2f", width=8)
    draw.polygon([(700, 525), (670, 507), (670, 543)], fill="#173b2f")
    draw.text((285, 545), "7 个半音 = 纯五度", fill="#173b2f", font=label)

    circles = [
        ((780, 310, 960, 490), "#2f6f4e", "C", "根音 Root"),
        ((910, 430, 1090, 610), "#d97941", "G", "五度 Fifth"),
    ]
    for box, color, note, desc in circles:
        draw.ellipse(box, fill=color, outline="#ffffff", width=8)
        draw_center(draw, box, note, "#ffffff", font(76, bold=True))
        draw.text((box[0] + 18, box[3] + 20), desc, fill="#173b2f", font=font(26, bold=True))

    draw.text((105, 685), "听感关键词：稳定、宽阔、空旷；没有三度，所以暂时不分大调或小调色彩。", fill="#365945", font=body)
    img.save(ASSET_DIR / "interval-perfect-fifth.png")


def save_piano_chart():
    img = Image.new("RGB", (1400, 650), "#f4f1e8")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(30)
    note_font = font(34, bold=True)

    draw.text((80, 50), "钢琴示意：C 到 G 的纯五度", fill="#27251f", font=title)
    draw.text((80, 125), "同时按 C 和 G，得到开放、稳定的五度骨架", fill="#5f5a4d", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    selected = {"C": "#2f6f4e", "G": "#d97941"}
    white_w = 150
    white_h = 340
    x0 = 80
    y0 = 220

    c_center = None
    g_center = None
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        fill = "#fffdf8" if i != 7 else "#f0eee6"
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill=fill, outline="#111827", width=3)
        if name in selected and not (i == 7 and name == "C"):
            draw.rounded_rectangle((x + 20, y0 + 205, x + white_w - 20, y0 + white_h - 25), 18, fill=selected[name])
            draw_center(draw, (x + 20, y0 + 205, x + white_w - 20, y0 + white_h - 25), name, "#ffffff", note_font)
            if name == "C":
                c_center = (x + white_w / 2, y0 + 195)
            if name == "G":
                g_center = (x + white_w / 2, y0 + 195)
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

    if c_center and g_center:
        draw.arc((c_center[0], 175, g_center[0], 355), start=185, end=355, fill="#7c4a28", width=7)
        draw.text((365, 178), "跨 5 个字母名 C-D-E-F-G", fill="#7c4a28", font=font(26, bold=True))

    legend_y = 592
    legend = [("C 根音", "#2f6f4e"), ("G 纯五度", "#d97941")]
    lx = 155
    for text, color in legend:
        draw.rounded_rectangle((lx, legend_y - 16, lx + 36, legend_y + 20), 8, fill=color)
        draw.text((lx + 55, legend_y - 22), text, fill="#27251f", font=body)
        lx += 330

    img.save(ASSET_DIR / "piano-c-g-perfect-fifth.png")


def save_guitar_chart():
    img = Image.new("RGB", (1000, 1300), "#f3f7fb")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)
    note_font = font(32, bold=True)

    draw.text((80, 55), "吉他示意：C5 Power Chord", fill="#183247", font=title)
    draw.text((80, 125), "C5 = C + G；只保留根音和纯五度", fill="#39576e", font=body)

    left = 180
    top = 260
    string_gap = 100
    fret_gap = 145
    strings = ["E", "A", "D", "G", "B", "e"]

    for i, s in enumerate(strings):
        x = left + i * string_gap
        width = 6 if i < 3 else 4
        draw.line((x, top, x, top + fret_gap * 5), fill="#4b5563", width=width)
        draw.text((x - 12, top - 70), s, fill="#183247", font=note_font)

    for i in range(6):
        y = top + i * fret_gap
        draw.line((left, y, left + string_gap * 5, y), fill="#1f2937", width=5)

    for i, fl in enumerate(["3", "4", "5", "6", "7"], start=1):
        y = top + fret_gap * i - fret_gap / 2
        draw.text((82, y - 22), fl, fill="#39576e", font=note_font)

    markers = [
        (1, 3, "#2f6f4e", "1", "C 根音"),
        (2, 5, "#d97941", "3", "G 五度"),
    ]
    for string_idx, fret, color, finger, note in markers:
        x = left + string_gap * string_idx
        y = top + fret_gap * (fret - 2.5)
        draw.ellipse((x - 44, y - 44, x + 44, y + 44), fill=color, outline="#ffffff", width=6)
        draw_center(draw, (x - 44, y - 44, x + 44, y + 44), finger, "#ffffff", note_font)
        draw.text((x - 54, y + 62), note, fill="#183247", font=font(24, bold=True))

    muted_strings = [0, 3, 4, 5]
    for string_idx in muted_strings:
        x = left + string_gap * string_idx
        draw.line((x - 22, top - 140, x + 22, top - 96), fill="#dc2626", width=7)
        draw.line((x + 22, top - 140, x - 22, top - 96), fill="#dc2626", width=7)

    draw.rounded_rectangle((80, 1040, 920, 1210), 24, fill="#e7eef6", outline="#9eb7cf", width=3)
    draw.text((120, 1076), "推荐拨弦：只弹 A 弦 3 品 + D 弦 5 品", fill="#183247", font=font(34, bold=True))
    draw.text((120, 1142), "常见场景：摇滚节奏、强拍重音、低音根音支撑", fill="#39576e", font=body)

    img.save(ASSET_DIR / "guitar-c5-power-chord.png")


if __name__ == "__main__":
    save_interval_chart()
    save_piano_chart()
    save_guitar_chart()
