from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-28-i-iv-v-chords"
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


def draw_wrapped_text(draw, text, xy, max_width, text_font, fill, line_gap=10):
    x, y = xy
    current = ""
    for ch in text:
        trial = current + ch
        width = draw.textbbox((0, 0), trial, font=text_font)[2]
        if width > max_width and current:
            draw.text((x, y), current, font=text_font, fill=fill)
            y += text_font.size + line_gap
            current = ch
        else:
            current = trial
    if current:
        draw.text((x, y), current, font=text_font, fill=fill)


def save_piano_chart():
    img = Image.new("RGB", (1520, 940), "#f7f1e7")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)
    small = font(22)

    draw.text((70, 48), "钢琴示意：C 大调里的 I-IV-V 和弦", fill="#2e2419", font=title)
    draw.text((70, 118), "把级数功能真正落到和弦上：I 是主功能，IV 是下属功能，V 是属功能。", fill="#65584b", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 155
    white_h = 330
    x0 = 85
    y0 = 240
    centers = {}
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 16, y0 + 275), name, fill="#55616f", font=font(30, bold=True))
        centers[f"{name}{i}"] = (x + white_w / 2, y0 + 135)

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 94
    black_h = 210
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#101826")
        center_text(draw, (x, y0 + 145, x + black_w, y0 + black_h), name, "#f9fafb", font(19, bold=True))

    chords = [
        ("I = C 大三和弦", ["C0", "E2", "G4"], "#d96c3f"),
        ("IV = F 大三和弦", ["F3", "A5", "C7"], "#c08b2d"),
        ("V = G 大三和弦", ["G4", "B6", "D1"], "#2f67b1"),
    ]

    for idx, (label, keys, color) in enumerate(chords):
        top = 610 + idx * 95
        draw.rounded_rectangle((80, top, 1435, top + 74), 20, fill="#fffaf2", outline=color, width=3)
        draw.text((110, top + 18), label, fill=color, font=font(34, bold=True))
        for key in keys:
            cx, cy = centers[key]
            circle_y = y0 + 178 + idx * 46
            draw.ellipse((cx - 34, circle_y - 34, cx + 34, circle_y + 34), fill=color, outline="#ffffff", width=4)
            note_name = key[0]
            center_text(draw, (cx - 34, circle_y - 26, cx + 34, circle_y + 20), note_name, "#ffffff", font(23, bold=True))

    draw.rounded_rectangle((1010, 150, 1430, 540), 28, fill="#fff8ee", outline="#cdb9a1", width=3)
    draw.text((1040, 180), "听感口诀", fill="#2e2419", font=font(36, bold=True))
    draw.text((1040, 248), "I：最稳定，像落地", fill="#65584b", font=body)
    draw.text((1040, 308), "IV：像离开家，准备变化", fill="#65584b", font=body)
    draw.text((1040, 368), "V：最想回 I，推动结束", fill="#65584b", font=body)
    draw.text((1040, 452), "常见顺序：I - IV - V - I", fill="#8b5a28", font=font(31, bold=True))

    img.save(ASSET_DIR / "piano-i-iv-v.png")


def draw_chord_diagram(draw, x, y, title, subtitle, dots):
    grid_left = x + 55
    grid_top = y + 95
    fret_gap = 58
    string_gap = 42

    draw.rounded_rectangle((x, y, x + 360, y + 430), 26, fill="#fffdfa", outline="#d5d8de", width=3)
    draw.text((x + 28, y + 24), title, fill="#1f2f38", font=font(34, bold=True))
    draw.text((x + 28, y + 62), subtitle, fill="#60717a", font=font(21))

    for i in range(6):
        sx = grid_left + i * string_gap
        draw.line((sx, grid_top, sx, grid_top + 4 * fret_gap), fill="#2d3748", width=4)
    for i in range(5):
        sy = grid_top + i * fret_gap
        draw.line((grid_left, sy, grid_left + 5 * string_gap, sy), fill="#2d3748", width=8 if i == 0 else 4)

    for fret, string_idx, label, color in dots:
        cx = grid_left + string_idx * string_gap
        cy = grid_top + (fret - 0.5) * fret_gap
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#ffffff", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 252, sx + 12, grid_top + 286), name, "#51606b", font(16, bold=True))


def save_guitar_chart():
    img = Image.new("RGB", (1480, 980), "#edf4f1")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((70, 45), "吉他示意：开放和弦里的 I-IV-V", fill="#163038", font=title)
    draw.text((70, 114), "在 C 大调里，最基础的一组功能和弦就是 C、F、G。它们足够支撑大量流行歌伴奏。", fill="#49626b", font=body)

    draw_chord_diagram(
        draw,
        80,
        220,
        "I = C",
        "主功能，最稳",
        [(3, 1, "3", "#d96c3f"), (2, 3, "2", "#d96c3f"), (1, 4, "1", "#d96c3f")],
    )
    draw_chord_diagram(
        draw,
        500,
        220,
        "IV = F",
        "下属功能，准备推进",
        [(3, 2, "4", "#c08b2d"), (2, 3, "3", "#c08b2d"), (1, 4, "1", "#c08b2d"), (1, 5, "1", "#c08b2d")],
    )
    draw_chord_diagram(
        draw,
        920,
        220,
        "V = G",
        "属功能，最想回家",
        [(2, 0, "2", "#2f67b1"), (3, 1, "1", "#2f67b1"), (3, 5, "3", "#2f67b1")],
    )

    draw.rounded_rectangle((90, 700, 1310, 900), 28, fill="#ffffff", outline="#b8c8c2", width=3)
    draw.text((120, 736), "实用伴奏练法", fill="#163038", font=font(36, bold=True))
    draw.text((120, 794), "每个和弦各弹 4 拍：C | F | G | C", fill="#49626b", font=body)
    draw.text((120, 842), "右手扫弦可先用：下 下上 上下上", fill="#49626b", font=body)

    img.save(ASSET_DIR / "guitar-i-iv-v.png")


def save_flow_chart():
    img = Image.new("RGB", (1380, 860), "#f8f7f2")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)
    small = font(23)

    draw.text((70, 52), "功能流程图：I -> IV -> V -> I", fill="#2c261f", font=title)
    draw.text((70, 124), "把三个和弦按功能顺序理解，比死记三个形状更重要。", fill="#665d52", font=body)

    boxes = [
        (110, 280, 340, 500, "#d96c3f", "I", "主功能", "稳定、落地、像起点和终点"),
        (430, 280, 660, 500, "#c08b2d", "IV", "下属功能", "从稳定离开，制造展开感"),
        (750, 280, 980, 500, "#2f67b1", "V", "属功能", "张力最强，期待回到 I"),
        (1070, 280, 1300, 500, "#d96c3f", "I", "回归主功能", "解决张力，形成完整句子"),
    ]

    for left, top, right, bottom, color, degree, heading, desc in boxes:
        draw.rounded_rectangle((left, top, right, bottom), 28, fill="#fffdf8", outline=color, width=4)
        draw.rounded_rectangle((left + 52, top + 30, right - 52, top + 108), 18, fill=color)
        center_text(draw, (left + 52, top + 30, right - 52, top + 108), degree, "#ffffff", font(34, bold=True))
        center_text(draw, (left + 18, top + 132, right - 18, top + 176), heading, color, font(26, bold=True))
        draw_wrapped_text(draw, desc, (left + 26, top + 208), 178, small, "#5c5348", line_gap=8)

    arrow_color = "#9b8a74"
    for x1, x2 in [(340, 430), (660, 750), (980, 1070)]:
        y = 390
        draw.line((x1 + 18, y, x2 - 18, y), fill=arrow_color, width=7)
        draw.polygon([(x2 - 18, y), (x2 - 42, y - 14), (x2 - 42, y + 14)], fill=arrow_color)

    draw.rounded_rectangle((120, 620, 1260, 760), 28, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((150, 648), "真实音乐里的作用：", fill="#724919", font=font(34, bold=True))
    draw.text((150, 698), "前两拍稳住，第三拍开始推进，最后回到主和弦，很多儿歌、民谣和流行歌都在这样写。", fill="#665d52", font=body)

    img.save(ASSET_DIR / "i-iv-v-flow.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_flow_chart()
