from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-29-dominant-seventh"
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
    img = Image.new("RGB", (1540, 980), "#f7f2ea")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)
    small = font(22)

    draw.text((70, 42), "钢琴示意：G7 属七和弦如何解决到 C", fill="#2f2418", font=title)
    draw.text((70, 110), "在 C 大调里，V7 就是 G-B-D-F。它比单纯的 G 大三和弦更紧张，因为多了 7 音 F。", fill="#65564a", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 155
    white_h = 330
    x0 = 85
    y0 = 240
    centers = {}
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 18, y0 + 276), name, fill="#55616f", font=font(30, bold=True))
        centers[f"{name}{i}"] = (x + white_w / 2, y0 + 135)

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 94
    black_h = 210
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 145, x + black_w, y0 + black_h), name, "#f9fafb", font(19, bold=True))

    g7_keys = [("G4", "#2f67b1"), ("B6", "#2f67b1"), ("D1", "#2f67b1"), ("F3", "#d96c3f")]
    c_keys = [("C0", "#2f8f5b"), ("E2", "#2f8f5b"), ("G4", "#2f8f5b")]
    for key, color in g7_keys:
        cx, cy = centers[key]
        circle_y = y0 + 175
        draw.ellipse((cx - 36, circle_y - 36, cx + 36, circle_y + 36), fill=color, outline="#ffffff", width=4)
        center_text(draw, (cx - 36, circle_y - 26, cx + 36, circle_y + 18), key[0], "#ffffff", font(22, bold=True))

    for key, color in c_keys:
        cx, cy = centers[key]
        circle_y = y0 + 258
        draw.ellipse((cx - 34, circle_y - 34, cx + 34, circle_y + 34), fill=color, outline="#ffffff", width=4)
        center_text(draw, (cx - 34, circle_y - 24, cx + 34, circle_y + 18), key[0], "#ffffff", font(22, bold=True))

    draw.rounded_rectangle((80, 610, 1460, 720), 22, fill="#fffaf3", outline="#2f67b1", width=3)
    draw.text((110, 640), "上排蓝色是 G7：G-B-D-F    下排绿色是解决后的 C：C-E-G", fill="#2f67b1", font=font(33, bold=True))

    draw.rounded_rectangle((1040, 160, 1445, 540), 26, fill="#fff8ee", outline="#ccb8a0", width=3)
    draw.text((1070, 188), "关键听感", fill="#2f2418", font=font(36, bold=True))
    draw.text((1070, 250), "B 很想上行到 C", fill="#65564a", font=body)
    draw.text((1070, 310), "F 很想下行到 E", fill="#65564a", font=body)
    draw.text((1070, 370), "这两个音同时动，", fill="#65564a", font=body)
    draw.text((1070, 412), "就会出现很清楚的", fill="#65564a", font=body)
    draw.text((1070, 454), "“回到主和弦”感觉", fill="#8b5a28", font=font(31, bold=True))

    draw.rounded_rectangle((100, 772, 1410, 910), 28, fill="#fffdf8", outline="#d7c5ae", width=3)
    draw.text((132, 800), "钢琴练法：左手弹 G -> C，右手先弹 G7 再弹 C，专门听 B->C、F->E 的移动。", fill="#5b4f43", font=body)
    draw.text((132, 850), "如果把 D 省略，只保留 B 和 F，再接到 C 和 E，你会更容易听到“张力 -> 解决”。", fill="#5b4f43", font=small)

    img.save(ASSET_DIR / "piano-g7-resolution.png")


def draw_chord_diagram(draw, x, y, title, subtitle, dots, labels):
    grid_left = x + 62
    grid_top = y + 102
    fret_gap = 60
    string_gap = 44

    draw.rounded_rectangle((x, y, x + 380, y + 455), 28, fill="#fffdfa", outline="#d5d8de", width=3)
    draw.text((x + 28, y + 24), title, fill="#1d3136", font=font(34, bold=True))
    draw.text((x + 28, y + 66), subtitle, fill="#60717a", font=font(21))

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

    for i, mark in labels.items():
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 16, grid_top - 42, sx + 16, grid_top - 10), mark, "#51606b", font(16, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 255, sx + 12, grid_top + 288), name, "#51606b", font(16, bold=True))


def save_guitar_chart():
    img = Image.new("RGB", (1480, 980), "#eef4f0")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((70, 44), "吉他示意：开放 G7 如何制造回到 C 的感觉", fill="#163038", font=title)
    draw.text((70, 112), "在流行、民谣和布鲁斯伴奏里，G7 比 G 更像“快要回家了”。这是最常见的属功能声音之一。", fill="#49626b", font=body)

    draw_chord_diagram(
        draw,
        100,
        220,
        "V7 = G7",
        "开放和弦，张力更强",
        [(2, 0, "2", "#2f67b1"), (3, 1, "1", "#2f67b1"), (1, 0, "F", "#d96c3f"), (3, 5, "3", "#2f67b1")],
        {4: "O", 2: "O", 3: "O"},
    )
    draw_chord_diagram(
        draw,
        560,
        220,
        "I = C",
        "回到主和弦",
        [(3, 1, "3", "#2f8f5b"), (2, 3, "2", "#2f8f5b"), (1, 4, "1", "#2f8f5b")],
        {0: "X", 2: "O", 5: "O"},
    )

    draw.rounded_rectangle((1030, 220, 1380, 675), 28, fill="#fffdfa", outline="#c4d1cb", width=3)
    draw.text((1060, 252), "练耳重点", fill="#163038", font=font(36, bold=True))
    draw.text((1060, 320), "先扫 G", fill="#49626b", font=body)
    draw.text((1060, 370), "再扫 G7", fill="#49626b", font=body)
    draw.text((1060, 420), "最后回到 C", fill="#49626b", font=body)
    draw.text((1060, 500), "你会听到：", fill="#7a5530", font=font(31, bold=True))
    draw.text((1060, 546), "G 稳一点，", fill="#49626b", font=body)
    draw.text((1060, 590), "G7 更急着回 C", fill="#49626b", font=body)

    draw.rounded_rectangle((100, 735, 1335, 900), 28, fill="#ffffff", outline="#b8c8c2", width=3)
    draw.text((130, 770), "实用进行：| C | F | G7 | C |", fill="#163038", font=font(36, bold=True))
    draw.text((130, 824), "扫弦可先保持四拍稳定，再把第三小节从 G 改成 G7，比较“回家感”是否更明显。", fill="#49626b", font=body)

    img.save(ASSET_DIR / "guitar-g7-chord.png")


def save_structure_chart():
    img = Image.new("RGB", (1400, 860), "#f8f7f2")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)
    small = font(23)

    draw.text((70, 48), "结构图：为什么 V7 比 V 更想回到 I", fill="#2c261f", font=title)
    draw.text((70, 118), "关键不只是“多了一个音”，而是这个音让解决方向更明确。", fill="#665d52", font=body)

    draw.rounded_rectangle((95, 220, 600, 610), 30, fill="#fffdf8", outline="#2f67b1", width=4)
    draw.text((132, 256), "G7 的构成音", fill="#2f67b1", font=font(38, bold=True))
    for idx, line in enumerate(["G = 根音", "B = 3 音", "D = 5 音", "F = 小 7 音"]):
        draw.text((140, 336 + idx * 58), line, fill="#5a5146", font=body)
    draw.text((140, 575), "公式：1 - 3 - 5 - b7", fill="#8b5a28", font=font(30, bold=True))

    draw.rounded_rectangle((685, 220, 1220, 610), 30, fill="#fffdf8", outline="#d96c3f", width=4)
    draw.text((720, 256), "最关键的解决", fill="#d96c3f", font=font(38, bold=True))
    draw.text((735, 344), "B  ->  C", fill="#2f67b1", font=font(34, bold=True))
    draw.text((735, 402), "F  ->  E", fill="#2f67b1", font=font(34, bold=True))
    draw.text((735, 488), "一个上行半音", fill="#5a5146", font=body)
    draw.text((735, 540), "一个下行半音", fill="#5a5146", font=body)
    draw.text((735, 592), "这就是最容易听见的解决感来源", fill="#8b5a28", font=small)

    draw.line((600, 415, 685, 415), fill="#9b8a74", width=8)
    draw.polygon([(685, 415), (655, 397), (655, 433)], fill="#9b8a74")

    draw.rounded_rectangle((120, 690, 1260, 790), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((150, 720), "结论：V7 不是更复杂而已，而是把“我要回到 I”的方向说得更清楚。", fill="#6a5644", font=font(34, bold=True))

    img.save(ASSET_DIR / "v7-resolution-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
