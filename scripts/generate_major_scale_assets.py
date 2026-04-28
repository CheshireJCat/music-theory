from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-24-major-scale"
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


def arrow(draw, start, end, color, width=7):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    draw.polygon([(x2, y2), (x2 - 20, y2 - 12), (x2 - 20, y2 + 12)], fill=color)


def save_piano_chart():
    img = Image.new("RGB", (1500, 860), "#f5efe3")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(29)
    note_font = font(30, bold=True)
    small = font(24)

    draw.text((70, 50), "钢琴示意：C 大调音阶", fill="#2c241d", font=title)
    draw.text((70, 120), "大调公式：全 全 半 全 全 全 半。C 大调正好全部用白键完成。", fill="#675849", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 160
    white_h = 360
    x0 = 70
    y0 = 255
    centers = {}
    colors = {
        "C0": "#d96c3f",
        "D1": "#2f67b1",
        "E2": "#2f8f6b",
        "F3": "#bf8b2c",
        "G4": "#7d59b5",
        "A5": "#cc5f7a",
        "B6": "#3f7a8c",
        "C7": "#d96c3f",
    }

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdf8", outline="#1f2937", width=3)
        draw.text((x + 18, y0 + 312), name, fill="#475569", font=note_font)
        centers[f"{name}{i}"] = (x + white_w / 2, y0 + 150)

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 96
    black_h = 220
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 145, x + black_w, y0 + black_h), name, "#f8fafc", font(20, bold=True))

    for key, color in colors.items():
        cx, cy = centers[key]
        draw.rounded_rectangle((cx - 46, y0 + 218, cx + 46, y0 + 304), 16, fill=color)
        center_text(draw, (cx - 46, y0 + 218, cx + 46, y0 + 304), key[0], "#ffffff", note_font)

    formula_y = 675
    formula = ["全", "全", "半", "全", "全", "全", "半"]
    formula_colors = ["#2f67b1", "#2f67b1", "#d96c3f", "#2f67b1", "#2f67b1", "#2f67b1", "#d96c3f"]
    draw.text((75, formula_y - 60), "相邻音之间的距离", fill="#4b5563", font=font(33, bold=True))
    for i, step in enumerate(formula):
        left = x0 + i * white_w + 95
        right = left + 70
        draw.rounded_rectangle((left, formula_y, right, formula_y + 54), 14, fill=formula_colors[i])
        center_text(draw, (left, formula_y, right, formula_y + 54), step, "#ffffff", font(26, bold=True))
        if i < len(formula) - 1:
            arrow(draw, (right + 8, formula_y + 27), (right + 35, formula_y + 27), "#8b7355", width=4)

    draw.rounded_rectangle((1085, 255, 1415, 545), 24, fill="#fff8ef", outline="#d1b483", width=3)
    draw.text((1115, 290), "延伸到 G 大调", fill="#6a4a21", font=font(34, bold=True))
    draw.text((1115, 355), "G A B C D E F# G", fill="#2c241d", font=body)
    draw.text((1115, 405), "仍然是：全全半全全全半", fill="#2c241d", font=body)
    draw.text((1115, 455), "区别只是第七级变成 F#", fill="#9f3d20", font=body)
    draw.text((1115, 505), "说明公式固定，起点可变。", fill="#5f5243", font=small)

    img.save(ASSET_DIR / "piano-major-scale.png")


def save_guitar_chart():
    img = Image.new("RGB", (1400, 920), "#edf5f7")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)
    note_font = font(26, bold=True)

    draw.text((70, 50), "吉他示意：C 大调音阶的一把位自然音", fill="#17313c", font=title)
    draw.text((70, 122), "先看开放把位，理解大调音阶并不等于只背一个指型。", fill="#48626c", font=body)

    left = 135
    right = 1260
    top = 265
    string_gap = 88
    fret_gap = 210
    strings = ["E", "A", "D", "G", "B", "e"]

    for i, s in enumerate(strings):
        y = top + i * string_gap
        draw.line((left, y, right, y), fill="#4b5563", width=5 if i < 3 else 4)
        draw.text((85, y - 18), s, fill="#17313c", font=note_font)

    for i in range(5):
        x = left + i * fret_gap
        draw.line((x, top - 38, x, top + string_gap * 5 + 38), fill="#1f2937", width=7 if i == 0 else 4)
        if i < 4:
            draw.text((x + fret_gap / 2 - 8, top - 95), str(i), fill="#48626c", font=note_font)

    note_map = [
        (0, 0, "E"), (1, 0, "F"), (3, 0, "G"),
        (0, 1, "A"), (2, 1, "B"), (3, 1, "C"),
        (0, 2, "D"), (2, 2, "E"), (3, 2, "F"),
        (0, 3, "G"), (2, 3, "A"),
        (0, 4, "B"), (1, 4, "C"), (3, 4, "D"),
        (0, 5, "E"), (1, 5, "F"), (3, 5, "G"),
    ]

    root_color = "#d96c3f"
    note_color = "#2f67b1"
    for fret, string_idx, name in note_map:
        x = left + (fret_gap * 0.5 if fret == 0 else fret_gap * (fret + 0.5))
        y = top + string_idx * string_gap
        color = root_color if name == "C" else note_color
        draw.ellipse((x - 34, y - 34, x + 34, y + 34), fill=color, outline="#ffffff", width=5)
        center_text(draw, (x - 34, y - 34, x + 34, y + 34), name, "#ffffff", note_font)

    draw.rounded_rectangle((920, 625, 1280, 815), 24, fill="#ffffff", outline="#9ab3bd", width=3)
    draw.text((950, 660), "观察重点", fill="#17313c", font=font(34, bold=True))
    draw.text((950, 718), "1 品会出现 F", fill="#48626c", font=body)
    draw.text((950, 758), "2 品会出现 A / B / E", fill="#48626c", font=body)
    draw.text((950, 798), "3 品会出现 C / D / F / G", fill="#48626c", font=body)

    draw.rounded_rectangle((105, 690, 800, 825), 24, fill="#f8fcfd", outline="#9ab3bd", width=3)
    draw.text((140, 722), "可直接练：5弦 3-0-2-3 = C-A-B-C，", fill="#17313c", font=font(30, bold=True))
    draw.text((140, 770), "再接 4弦 0-2-3 = D-E-F，组成顺阶上行片段。", fill="#48626c", font=body)

    img.save(ASSET_DIR / "guitar-major-scale.png")


def save_formula_chart():
    img = Image.new("RGB", (1300, 820), "#f7f6ee")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(29)
    label = font(26, bold=True)

    draw.text((70, 55), "大调音阶结构图", fill="#29251f", font=title)
    draw.text((70, 125), "用级数来看，大调是 1 2 3 4 5 6 7 1，每一级之间距离固定。", fill="#655c50", font=body)

    degrees = ["1", "2", "3", "4", "5", "6", "7", "1"]
    note_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    steps = ["全", "全", "半", "全", "全", "全", "半"]
    x0 = 105
    y0 = 320
    box = 110
    gap = 34

    for i, (degree, note) in enumerate(zip(degrees, note_names)):
        x = x0 + i * (box + gap)
        fill = "#d96c3f" if note == "C" else "#2f67b1"
        draw.rounded_rectangle((x, y0, x + box, y0 + box), 22, fill=fill)
        center_text(draw, (x, y0 + 8, x + box, y0 + 58), degree, "#ffffff", font(28, bold=True))
        center_text(draw, (x, y0 + 48, x + box, y0 + 104), note, "#ffffff", font(34, bold=True))
        if i < len(steps):
            sx = x + box
            draw.line((sx + 8, y0 + box / 2, sx + gap - 8, y0 + box / 2), fill="#8b7355", width=5)
            draw.text((sx + 6, y0 + 115), steps[i], fill="#9f3d20" if steps[i] == "半" else "#224f8d", font=label)

    draw.rounded_rectangle((85, 555, 1215, 720), 24, fill="#fffaf1", outline="#d2b071", width=3)
    draw.text((118, 585), "核心理解：你记住的不是一串固定字母，而是一套“距离模板”。", fill="#5c4527", font=font(33, bold=True))
    draw.text((118, 635), "所以从 G 开始套同一模板，就会得到 G A B C D E F# G。", fill="#655c50", font=body)

    img.save(ASSET_DIR / "major-scale-formula.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_formula_chart()
