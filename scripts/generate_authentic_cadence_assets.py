from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-04-30-authentic-cadence"
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
    img = Image.new("RGB", (1540, 980), "#f6f1e8")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)

    draw.text((68, 40), "钢琴示意：正格终止 V-I 的“回家”感", fill="#2d261d", font=title)
    draw.text((68, 108), "以 C 大调为例，G7 -> C 是最典型的正格终止。V 或 V7 走向 I，会让乐句显得真正结束。", fill="#65584c", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 155
    white_h = 330
    x0 = 82
    y0 = 240
    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 20, y0 + 278), name, fill="#586474", font=font(30, bold=True))

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 94
    black_h = 210
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 145, x + black_w, y0 + black_h), name, "#f9fafb", font(19, bold=True))

    def mark_white_key(note_idx: int, note: str, circle_y: int, color: str, radius: int):
        cx = x0 + note_idx * white_w + white_w / 2
        cy = circle_y
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color, outline="#ffffff", width=4)
        center_text(draw, (cx - radius, cy - 22, cx + radius, cy + 18), note, "#ffffff", font(22, bold=True))

    for idx, note, color in [(4, "G", "#2f67b1"), (6, "B", "#2f67b1"), (1, "D", "#2f67b1"), (3, "F", "#d96c3f")]:
        mark_white_key(idx, note, y0 + 172, color, 36)
    for idx, note in [(0, "C"), (2, "E"), (4, "G")]:
        mark_white_key(idx, note, y0 + 258, "#2f8f5b", 34)

    draw.rounded_rectangle((80, 612, 1460, 720), 24, fill="#fff8ef", outline="#2f67b1", width=3)
    draw.text((112, 642), "上排蓝色：V7 = G-B-D-F     下排绿色：I = C-E-G", fill="#2f67b1", font=font(33, bold=True))

    draw.rounded_rectangle((1035, 162, 1450, 560), 26, fill="#fffaf2", outline="#d2c3ad", width=3)
    draw.text((1066, 190), "为什么像结束", fill="#2d261d", font=font(36, bold=True))
    draw.text((1066, 256), "1. 先有属功能张力", fill="#65584c", font=body)
    draw.text((1066, 318), "2. B 上行到 C", fill="#65584c", font=body)
    draw.text((1066, 380), "3. F 下行到 E", fill="#65584c", font=body)
    draw.text((1066, 462), "于是听感会稳定落到 I", fill="#8b5a28", font=font(31, bold=True))

    draw.rounded_rectangle((96, 774, 1412, 912), 28, fill="#fffdf8", outline="#d7c5ae", width=3)
    draw.text((128, 804), "钢琴练法：左手弹 G -> C，右手先弹 G7 再弹 C。先感受整和弦，再单独听 B->C、F->E。", fill="#5b4f43", font=body)
    draw.text((128, 856), "如果句子还没结束，通常不会这么稳定地落到 I；这正是终止式和普通和弦连接的区别。", fill="#5b4f43", font=font(23))

    img.save(ASSET_DIR / "piano-authentic-cadence.png")


def draw_chord_box(draw, x, y, title_text, chord_line, fill_color, border_color):
    draw.rounded_rectangle((x, y, x + 350, y + 170), 28, fill=fill_color, outline=border_color, width=4)
    draw.text((x + 28, y + 28), title_text, fill="#183038", font=font(34, bold=True))
    draw.text((x + 28, y + 92), chord_line, fill="#50656c", font=font(28))


def draw_chord_diagram(draw, x, y, title_text, subtitle, dots, top_marks):
    grid_left = x + 62
    grid_top = y + 102
    fret_gap = 60
    string_gap = 44

    draw.rounded_rectangle((x, y, x + 380, y + 455), 28, fill="#fffdfa", outline="#d5d8de", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#1d3136", font=font(34, bold=True))
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

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 16, grid_top - 42, sx + 16, grid_top - 10), mark, "#51606b", font(16, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 255, sx + 12, grid_top + 288), name, "#51606b", font(16, bold=True))


def save_guitar_chart():
    img = Image.new("RGB", (1480, 980), "#edf4ef")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((70, 44), "吉他示意：正格终止常见于结尾和副歌收束", fill="#163038", font=title)
    draw.text((70, 112), "在吉他伴奏里，Authentic Cadence 通常表现为 V 或 V7 回到 I。C 大调最常见的就是 G7 -> C。", fill="#49626b", font=body)

    draw_chord_box(draw, 96, 196, "终止式名称", "Authentic Cadence = V-I 或 V7-I", "#fffdfa", "#bfcfc8")

    draw_chord_diagram(
        draw,
        110,
        400,
        "V7 = G7",
        "把乐句推向结束",
        [(2, 0, "2", "#2f67b1"), (3, 1, "1", "#2f67b1"), (1, 0, "F", "#d96c3f"), (3, 5, "3", "#2f67b1")],
        {2: "O", 3: "O", 4: "O"},
    )
    draw_chord_diagram(
        draw,
        570,
        400,
        "I = C",
        "稳定落点",
        [(3, 1, "3", "#2f8f5b"), (2, 3, "2", "#2f8f5b"), (1, 4, "1", "#2f8f5b")],
        {0: "X", 2: "O", 5: "O"},
    )

    draw.rounded_rectangle((1032, 222, 1386, 852), 28, fill="#fffdfa", outline="#c4d1cb", width=3)
    draw.text((1060, 256), "常见场景", fill="#163038", font=font(36, bold=True))
    draw.text((1060, 328), "1. 一段尾句最后两拍", fill="#49626b", font=body)
    draw.text((1060, 388), "2. 副歌收尾回主和弦", fill="#49626b", font=body)
    draw.text((1060, 448), "3. 民谣段落结尾", fill="#49626b", font=body)
    draw.text((1060, 540), "实用练法", fill="#7a5530", font=font(31, bold=True))
    draw.text((1060, 590), "循环 | C | F | G7 | C |", fill="#49626b", font=body)
    draw.text((1060, 644), "第三小节先停一下，", fill="#49626b", font=body)
    draw.text((1060, 688), "再扫回 C，听结束感", fill="#49626b", font=body)

    img.save(ASSET_DIR / "guitar-authentic-cadence.png")


def save_flow_chart():
    img = Image.new("RGB", (1420, 860), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 48), "结构图：正格终止为什么能让乐句结束", fill="#2c261f", font=title)
    draw.text((68, 118), "它不是单纯的两个和弦连在一起，而是张力明确地解决到稳定。", fill="#665d52", font=body)

    draw.rounded_rectangle((100, 220, 390, 610), 30, fill="#fffdf8", outline="#2f67b1", width=4)
    draw.text((136, 258), "V 或 V7", fill="#2f67b1", font=font(40, bold=True))
    draw.text((136, 340), "功能：属", fill="#5a5146", font=body)
    draw.text((136, 396), "听感：紧张、想继续", fill="#5a5146", font=body)
    draw.text((136, 470), "例：G 或 G7", fill="#8b5a28", font=font(31, bold=True))

    draw.rounded_rectangle((560, 220, 860, 610), 30, fill="#fff8ee", outline="#d2b071", width=4)
    draw.text((600, 258), "解决动作", fill="#8b5a28", font=font(40, bold=True))
    draw.text((600, 340), "B -> C", fill="#5a5146", font=font(36, bold=True))
    draw.text((600, 400), "F -> E", fill="#5a5146", font=font(36, bold=True))
    draw.text((600, 492), "张力往主和弦核心音靠拢", fill="#5a5146", font=font(24))

    draw.rounded_rectangle((1030, 220, 1320, 610), 30, fill="#f8fdf9", outline="#2f8f5b", width=4)
    draw.text((1068, 258), "I", fill="#2f8f5b", font=font(40, bold=True))
    draw.text((1068, 340), "功能：主", fill="#5a5146", font=body)
    draw.text((1068, 396), "听感：稳定、结束", fill="#5a5146", font=body)
    draw.text((1068, 470), "例：C", fill="#2f8f5b", font=font(31, bold=True))

    draw.line((390, 416, 560, 416), fill="#9b8a74", width=8)
    draw.polygon([(560, 416), (526, 396), (526, 436)], fill="#9b8a74")
    draw.line((860, 416, 1030, 416), fill="#9b8a74", width=8)
    draw.polygon([(1030, 416), (996, 396), (996, 436)], fill="#9b8a74")

    draw.rounded_rectangle((122, 690, 1296, 790), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((154, 720), "一句话理解：正格终止就是属功能把句子推向主和弦，并在主和弦上落稳。", fill="#6a5644", font=font(33, bold=True))

    img.save(ASSET_DIR / "authentic-cadence-flow.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_flow_chart()
