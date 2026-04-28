from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-22-44-meter"
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


def save_meter_structure():
    img = Image.new("RGB", (1300, 820), "#f5efe4")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(30)
    label = font(34, bold=True)
    small = font(24, bold=True)

    draw.rounded_rectangle((58, 48, 1242, 762), radius=34, fill="#fffaf0", outline="#b78a57", width=4)
    draw.text((100, 88), "四四拍 4/4 Meter：一小节 4 拍", fill="#312414", font=title)
    draw.text((100, 162), "分母 4 = 以四分音符为一拍；分子 4 = 每小节有 4 拍", fill="#6f4c28", font=body)

    start_x = 145
    beat_w = 245
    y = 330
    beats = [
        ("1", "强", "#9f2d20", 1.0),
        ("2", "弱", "#d8a63a", 0.72),
        ("3", "次强", "#c8692f", 0.86),
        ("4", "弱", "#d8a63a", 0.72),
    ]
    for i, (num, accent, color, height_scale) in enumerate(beats):
        x = start_x + i * beat_w
        draw.rounded_rectangle((x, y, x + 175, y + 260), 24, fill="#f7ead6", outline="#a77948", width=3)
        bar_h = int(150 * height_scale)
        draw.rounded_rectangle((x + 47, y + 202 - bar_h, x + 128, y + 202), 18, fill=color)
        draw_center(draw, (x, y + 208, x + 175, y + 260), f"第 {num} 拍", "#312414", label)
        draw_center(draw, (x + 32, y + 62, x + 143, y + 115), accent, "#ffffff", small)
        if i < 3:
            draw.text((x + 188, y + 112), "→", fill="#8b5a2b", font=font(44, bold=True))

    draw.line((132, 665, 1168, 665), fill="#312414", width=6)
    for i in range(5):
        x = start_x - 42 + i * beat_w
        draw.line((x, 638, x, 692), fill="#312414", width=6)
    draw.text((155, 704), "|  1        2        3        4  |", fill="#312414", font=font(38, bold=True))
    draw.text((100, 235), "常见口令：强 - 弱 - 次强 - 弱", fill="#312414", font=font(38, bold=True))

    img.save(ASSET_DIR / "meter-44-accent-pattern.png")


def save_piano_chart():
    img = Image.new("RGB", (1450, 760), "#edf3ef")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(29)
    note_font = font(32, bold=True)

    draw.text((74, 50), "钢琴用法：4/4 左手低音 + 和弦重音", fill="#19362b", font=title)
    draw.text((74, 123), "第 1 拍低音最稳，第 3 拍给次强支撑；第 2、4 拍可轻弹和弦", fill="#446454", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 150
    white_h = 330
    x0 = 80
    y0 = 250
    chord_notes = {"C": "#256c4f", "E": "#db7a31", "G": "#2f6e9e"}

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        fill = "#fffdf6" if i != 7 else "#eef1e8"
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill=fill, outline="#111827", width=3)
        if name in chord_notes and not (i == 7 and name == "C"):
            draw.rounded_rectangle((x + 18, y0 + 205, x + white_w - 18, y0 + white_h - 25), 18, fill=chord_notes[name])
            draw_center(draw, (x + 18, y0 + 205, x + white_w - 18, y0 + white_h - 25), name, "#ffffff", note_font)
        else:
            draw_center(draw, (x, y0 + 250, x + white_w, y0 + white_h), name, "#374151", note_font)

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#", "D#", "F#", "G#", "A#"]
    black_w = 88
    black_h = 202
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        draw_center(draw, (x, y0 + 130, x + black_w, y0 + black_h), name, "#f9fafb", font(20, bold=True))

    timeline_y = 635
    draw.rounded_rectangle((80, timeline_y - 34, 1370, timeline_y + 82), 22, fill="#dfe9e3", outline="#87a391", width=3)
    beats = [
        ("1", "C 低音", "强", "#9f2d20"),
        ("2", "C-E-G", "弱", "#7d946c"),
        ("3", "G 或 C", "次强", "#c8692f"),
        ("4", "C-E-G", "弱", "#7d946c"),
    ]
    for i, (num, action, accent, color) in enumerate(beats):
        x = 130 + i * 310
        draw.ellipse((x, timeline_y - 12, x + 48, timeline_y + 36), fill=color)
        draw_center(draw, (x, timeline_y - 12, x + 48, timeline_y + 36), num, "#ffffff", font(24, bold=True))
        draw.text((x + 62, timeline_y - 25), action, fill="#19362b", font=font(27, bold=True))
        draw.text((x + 62, timeline_y + 24), accent, fill="#446454", font=font(22, bold=True))

    img.save(ASSET_DIR / "piano-44-accompaniment.png")


def save_guitar_strum_chart():
    img = Image.new("RGB", (1300, 900), "#f0f4f7")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(29)
    label = font(32, bold=True)
    small = font(24, bold=True)

    draw.text((70, 55), "吉他用法：4/4 基础扫弦 Down-Up", fill="#173247", font=title)
    draw.text((70, 128), "第 1 拍扫得最明确，第 3 拍略加强；第 2、4 拍保持轻而稳", fill="#405c70", font=body)

    table_left = 90
    table_top = 235
    col_w = 290
    row_h = 132
    headers = ["1 强", "2 弱", "3 次强", "4 弱"]
    colors = ["#9f2d20", "#6f8fbd", "#c8692f", "#6f8fbd"]
    for i, header in enumerate(headers):
        x = table_left + i * col_w
        draw.rounded_rectangle((x, table_top, x + col_w - 22, table_top + 98), 20, fill=colors[i], outline="#ffffff", width=4)
        draw_center(draw, (x, table_top, x + col_w - 22, table_top + 98), header, "#ffffff", label)

    rows = [
        ("口令", ["1", "&", "2", "&"], ["3", "&", "4", "&"]),
        ("扫弦", ["↓", "↑", "↓", "↑"], ["↓", "↑", "↓", "↑"]),
    ]
    y = 390
    draw.text((70, y + 18), "八分音符细分：", fill="#173247", font=label)
    cells = [("1", "#9f2d20"), ("&", "#cdd7df"), ("2", "#6f8fbd"), ("&", "#cdd7df"),
             ("3", "#c8692f"), ("&", "#cdd7df"), ("4", "#6f8fbd"), ("&", "#cdd7df")]
    for i, (txt, color) in enumerate(cells):
        x = 310 + i * 112
        draw.rounded_rectangle((x, y, x + 82, y + 82), 16, fill=color, outline="#466274", width=2)
        fill = "#ffffff" if txt != "&" else "#173247"
        draw_center(draw, (x, y, x + 82, y + 82), txt, fill, font(30, bold=True))

    y2 = 545
    draw.text((70, y2 + 20), "右手动作：", fill="#173247", font=label)
    strokes = [("↓", "#9f2d20"), ("↑", "#aebdca"), ("↓", "#6f8fbd"), ("↑", "#aebdca"),
               ("↓", "#c8692f"), ("↑", "#aebdca"), ("↓", "#6f8fbd"), ("↑", "#aebdca")]
    for i, (txt, color) in enumerate(strokes):
        x = 310 + i * 112
        draw.ellipse((x, y2, x + 82, y2 + 82), fill=color, outline="#ffffff", width=4)
        draw_center(draw, (x, y2 - 3, x + 82, y2 + 79), txt, "#ffffff", font(42, bold=True))

    draw.rounded_rectangle((86, 715, 1214, 830), 24, fill="#ffffff", outline="#9cb3c4", width=3)
    draw.text((125, 742), "推荐和弦进行：C | G | Am | F，每个和弦一小节", fill="#173247", font=font(34, bold=True))
    draw.text((125, 790), "先只扫：↓  ↓  ↓  ↓；稳定后再加入：↓↑ ↓↑ ↓↑ ↓↑", fill="#405c70", font=small)

    img.save(ASSET_DIR / "guitar-44-strum-pattern.png")


if __name__ == "__main__":
    save_meter_structure()
    save_piano_chart()
    save_guitar_strum_chart()
