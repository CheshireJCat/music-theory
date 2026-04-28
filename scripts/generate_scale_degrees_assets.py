from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-27-scale-degrees"
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


def save_piano_chart():
    img = Image.new("RGB", (1520, 900), "#f6f1e6")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(29)
    note_font = font(28, bold=True)
    small = font(24)

    draw.text((70, 50), "钢琴示意：C 大调里的音阶级数与功能", fill="#2b231c", font=title)
    draw.text((70, 120), "同一条大调音阶里，不同级数的听感不同。今天先抓住 1 级、5 级、7 级。", fill="#645649", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    degree_names = ["1", "2", "3", "4", "5", "6", "7", "8"]
    function_names = ["主音", "上主音", "中音", "下属音", "属音", "下中音", "导音", "八度主音"]
    white_w = 160
    white_h = 360
    x0 = 70
    y0 = 255
    centers = {}
    highlight = {"C0": "#d96c3f", "G4": "#2f67b1", "B6": "#c84d6c", "C7": "#d96c3f"}

    for i, (name, degree, fn_name) in enumerate(zip(white_names, degree_names, function_names)):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 16, y0 + 300), name, fill="#475569", font=font(30, bold=True))
        draw.text((x + 16, y0 + 336), f"{degree}级", fill="#6b7280", font=small)
        centers[f"{name}{i}"] = (x + white_w / 2, y0 + 145)
        if fn_name:
            center_text(draw, (x + 6, y0 + 14, x + white_w - 6, y0 + 64), fn_name, "#786858", font(20, bold=True))

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 96
    black_h = 220
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 146, x + black_w, y0 + black_h), name, "#f8fafc", font(20, bold=True))

    for key, color in highlight.items():
        cx, _ = centers[key]
        draw.rounded_rectangle((cx - 48, y0 + 212, cx + 48, y0 + 302), 16, fill=color)
        box_text = "1" if key.startswith("C") else "5" if key.startswith("G") else "7"
        center_text(draw, (cx - 48, y0 + 212, cx + 48, y0 + 302), box_text, "#ffffff", note_font)

    boxes = [
        ((85, 670, 470, 815), "#fff7ee", "#d96c3f", "1级 主音", "像“家”，最稳定，乐句停在这里最安心。"),
        ((560, 670, 945, 815), "#eef5fc", "#2f67b1", "5级 属音", "常推动音乐往前，和 1 级构成最常见支点。"),
        ((1035, 670, 1420, 815), "#fdf0f3", "#c84d6c", "7级 导音", "离上方主音只差半音，天然有回到 1 级的倾向。"),
    ]
    for box, bg, color, heading, desc in boxes:
        draw.rounded_rectangle(box, 24, fill=bg, outline=color, width=3)
        draw.text((box[0] + 28, box[1] + 22), heading, fill=color, font=font(34, bold=True))
        draw.text((box[0] + 28, box[1] + 78), desc, fill="#594f44", font=body)

    img.save(ASSET_DIR / "piano-scale-degrees.png")


def save_guitar_chart():
    img = Image.new("RGB", (1460, 940), "#edf5f6")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)
    note_font = font(24, bold=True)

    draw.text((70, 50), "吉他示意：开放把位中的 1 级、5 级、7 级", fill="#173039", font=title)
    draw.text((70, 122), "在 C 大调里，把音名和级数同时看，会更容易把旋律与和弦连接起来。", fill="#47616a", font=body)

    left = 135
    right = 1285
    top = 270
    string_gap = 92
    fret_gap = 210
    strings = ["E", "A", "D", "G", "B", "e"]

    for i, s in enumerate(strings):
        y = top + i * string_gap
        draw.line((left, y, right, y), fill="#4b5563", width=5 if i < 3 else 4)
        draw.text((85, y - 18), s, fill="#173039", font=note_font)

    for i in range(5):
        x = left + i * fret_gap
        draw.line((x, top - 38, x, top + string_gap * 5 + 38), fill="#1f2937", width=7 if i == 0 else 4)
        if i < 4:
            draw.text((x + fret_gap / 2 - 8, top - 95), str(i), fill="#47616a", font=note_font)

    note_map = [
        (3, 1, "C", "1", "#d96c3f"),
        (1, 4, "C", "1", "#d96c3f"),
        (3, 5, "G", "5", "#2f67b1"),
        (0, 3, "G", "5", "#2f67b1"),
        (2, 1, "B", "7", "#c84d6c"),
        (0, 4, "B", "7", "#c84d6c"),
    ]

    for fret, string_idx, name, degree, color in note_map:
        x = left + (fret_gap * 0.5 if fret == 0 else fret_gap * (fret + 0.5))
        y = top + string_idx * string_gap
        draw.ellipse((x - 40, y - 40, x + 40, y + 40), fill=color, outline="#ffffff", width=5)
        center_text(draw, (x - 40, y - 48, x + 40, y - 6), name, "#ffffff", font(22, bold=True))
        center_text(draw, (x - 40, y - 2, x + 40, y + 36), f"{degree}级", "#ffffff", font(18, bold=True))

    legend = [
        ("#d96c3f", "1级 C：落点最稳，适合结束句子"),
        ("#2f67b1", "5级 G：常用来支撑属功能或过门"),
        ("#c84d6c", "7级 B：回到 C 前最有“想解决”的感觉"),
    ]
    for idx, (color, text) in enumerate(legend):
        y = 700 + idx * 56
        draw.rounded_rectangle((85, y, 115, y + 30), 8, fill=color)
        draw.text((135, y - 2), text, fill="#173039", font=body)

    draw.rounded_rectangle((925, 660, 1325, 840), 26, fill="#ffffff", outline="#9ab3bd", width=3)
    draw.text((955, 692), "快速练法", fill="#173039", font=font(34, bold=True))
    draw.text((955, 748), "5弦 2-3 = B-C", fill="#47616a", font=body)
    draw.text((955, 790), "3弦 0 后接 2弦 0-1", fill="#47616a", font=body)
    draw.text((955, 830), "G  B  C，听 7->1 的解决感", fill="#47616a", font=body)

    img.save(ASSET_DIR / "guitar-scale-degrees.png")


def save_function_chart():
    img = Image.new("RGB", (1360, 860), "#f7f7f0")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)
    small = font(23)

    draw.text((70, 55), "音阶级数功能图", fill="#29251f", font=title)
    draw.text((70, 125), "先理解每一级的大致听感，再把它放到旋律和伴奏中使用。", fill="#665d52", font=body)

    degrees = [
        ("1", "主音", "#d96c3f", "最稳定，像回家"),
        ("2", "上主音", "#93a3b8", "可通向 1 或 3"),
        ("3", "中音", "#7b9b84", "决定大小调色彩"),
        ("4", "下属音", "#c29a4a", "容易把音乐推向 5"),
        ("5", "属音", "#2f67b1", "强支点，常等着回 1"),
        ("6", "下中音", "#9a78b8", "常带柔和或抒情感"),
        ("7", "导音", "#c84d6c", "离 1 半音，最想解决"),
    ]

    x0 = 90
    y0 = 250
    col_w = 170
    gap = 16
    for i, (degree, label, color, desc) in enumerate(degrees):
        x = x0 + i * (col_w + gap)
        draw.rounded_rectangle((x, y0, x + col_w, y0 + 290), 24, fill="#fffdf8", outline=color, width=4)
        draw.rounded_rectangle((x + 20, y0 + 22, x + col_w - 20, y0 + 92), 18, fill=color)
        center_text(draw, (x + 20, y0 + 22, x + col_w - 20, y0 + 92), f"{degree}级", "#ffffff", font(28, bold=True))
        center_text(draw, (x + 15, y0 + 114, x + col_w - 15, y0 + 158), label, color, font(26, bold=True))
        center_text(draw, (x + 12, y0 + 176, x + col_w - 12, y0 + 262), desc, "#5b5349", small)

    draw.rounded_rectangle((100, 610, 1260, 760), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((130, 640), "入门时先重点记 1 级、5 级、7 级：", fill="#6a4a21", font=font(34, bold=True))
    draw.text((130, 692), "1 最稳，5 最能支撑推进，7 最强烈地想回到 1。", fill="#665d52", font=body)

    img.save(ASSET_DIR / "scale-degree-functions.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_function_chart()
