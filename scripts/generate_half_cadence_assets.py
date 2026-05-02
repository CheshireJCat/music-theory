from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-02-half-cadence"
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
    img = Image.new("RGB", (1540, 980), "#f4efe7")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)

    draw.text((68, 40), "钢琴示意：半终止停在 V，像逗号不是句号", fill="#2d261d", font=title)
    draw.text((68, 108), "以 C 大调为例，半终止常把乐句停在 G 或 G7 上。它制造“先停一下，但还没结束”的感觉。", fill="#65584c", font=body)

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

    def mark_white_key(note_idx: int, note: str, circle_y: int, color: str):
        cx = x0 + note_idx * white_w + white_w / 2
        cy = circle_y
        radius = 36
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color, outline="#ffffff", width=4)
        center_text(draw, (cx - radius, cy - 22, cx + radius, cy + 18), note, "#ffffff", font(22, bold=True))

    for idx, note in [(0, "C"), (2, "E"), (4, "G")]:
        mark_white_key(idx, note, y0 + 260, "#2f8f5b")
    for idx, note in [(4, "G"), (6, "B"), (1, "D")]:
        mark_white_key(idx, note, y0 + 170, "#2f67b1")

    draw.line((1040, 330, 1420, 330), fill="#b7a38c", width=8)
    draw.polygon([(1420, 330), (1386, 310), (1386, 350)], fill="#b7a38c")
    draw.text((1068, 258), "乐句走向", fill="#2d261d", font=font(34, bold=True))
    draw.text((1068, 372), "I 或 ii 或 IV", fill="#2f8f5b", font=font(30, bold=True))
    draw.text((1068, 430), "最后停在 V", fill="#2f67b1", font=font(30, bold=True))
    draw.text((1068, 506), "听感：悬着、等下一句", fill="#8b5a28", font=body)

    draw.rounded_rectangle((80, 612, 1460, 722), 24, fill="#fff8ef", outline="#2f67b1", width=3)
    draw.text((112, 646), "绿色先表示稳定起点，蓝色表示最后停住的 G 大三和弦。重点是它没有再回到 C。", fill="#2f67b1", font=font(31, bold=True))

    draw.rounded_rectangle((96, 774, 1412, 912), 28, fill="#fffdf8", outline="#d7c5ae", width=3)
    draw.text((128, 804), "钢琴练法：左手弹 C -> G，右手先弹 C-E-G，再弹 G-B-D。停在 G 上，先别回 C。", fill="#5b4f43", font=body)
    draw.text((128, 856), "这样你会很清楚地听到：句子像在逗号处停顿，而不是已经收尾。", fill="#5b4f43", font=font(23))

    img.save(ASSET_DIR / "piano-half-cadence.png")


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
    img = Image.new("RGB", (1480, 980), "#edf3f4")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((70, 44), "吉他示意：半终止常停在 V，推动下一句进入", fill="#163038", font=title)
    draw.text((70, 112), "在 C 大调弹唱里，很多主歌前半句会先停在 G，再进入下一句。这个“没说完”的效果，就是 Half Cadence。", fill="#49626b", font=body)

    draw.rounded_rectangle((92, 194, 530, 322), 28, fill="#fffdfa", outline="#c7d1d4", width=3)
    draw.text((124, 228), "常见进行：| C | F | G |", fill="#163038", font=font(36, bold=True))
    draw.text((124, 278), "最后停在 G，不马上回 C", fill="#60717a", font=font(24))

    draw_chord_diagram(
        draw,
        108,
        390,
        "I = C",
        "先建立稳定起点",
        [(3, 1, "3", "#2f8f5b"), (2, 3, "2", "#2f8f5b"), (1, 4, "1", "#2f8f5b")],
        {0: "X", 2: "O", 5: "O"},
    )
    draw_chord_diagram(
        draw,
        568,
        390,
        "V = G",
        "停在这里，等下一句",
        [(2, 0, "2", "#2f67b1"), (3, 1, "1", "#2f67b1"), (3, 5, "3", "#2f67b1")],
        {2: "O", 3: "O", 4: "O"},
    )

    draw.rounded_rectangle((1032, 222, 1386, 852), 28, fill="#fffdfa", outline="#c4d1cb", width=3)
    draw.text((1060, 256), "实际用法", fill="#163038", font=font(36, bold=True))
    draw.text((1060, 328), "1. 主歌前半句结尾", fill="#49626b", font=body)
    draw.text((1060, 388), "2. 过门前的停顿", fill="#49626b", font=body)
    draw.text((1060, 448), "3. 副歌前的蓄力", fill="#49626b", font=body)
    draw.text((1060, 540), "练法", fill="#7a5530", font=font(31, bold=True))
    draw.text((1060, 590), "先弹 | C | F | G |", fill="#49626b", font=body)
    draw.text((1060, 644), "再接 | C | F | G | C |", fill="#49626b", font=body)
    draw.text((1060, 698), "对比哪一个更像句号", fill="#49626b", font=body)

    img.save(ASSET_DIR / "guitar-half-cadence.png")


def save_structure_chart():
    img = Image.new("RGB", (1420, 860), "#f7f6f2")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 48), "结构图：半终止为什么像“逗号”", fill="#2c261f", font=title)
    draw.text((68, 118), "关键不是用了哪个和弦，而是乐句最后停在属功能上，没有解决回主和弦。", fill="#665d52", font=body)

    draw.rounded_rectangle((96, 236, 398, 624), 30, fill="#f8fdf9", outline="#2f8f5b", width=4)
    draw.text((134, 274), "前半句", fill="#2f8f5b", font=font(40, bold=True))
    draw.text((134, 356), "可以从 I、ii、IV 开始", fill="#5a5146", font=font(27))
    draw.text((134, 426), "建立调性感", fill="#5a5146", font=body)
    draw.text((134, 496), "例：C -> F", fill="#2f8f5b", font=font(31, bold=True))

    draw.rounded_rectangle((560, 236, 860, 624), 30, fill="#fff8ee", outline="#d2b071", width=4)
    draw.text((600, 274), "句尾动作", fill="#8b5a28", font=font(40, bold=True))
    draw.text((600, 356), "最后落到 V", fill="#5a5146", font=font(35, bold=True))
    draw.text((600, 426), "不回 I", fill="#5a5146", font=font(35, bold=True))
    draw.text((600, 496), "听感保持悬念", fill="#5a5146", font=font(30))

    draw.rounded_rectangle((1022, 236, 1324, 624), 30, fill="#eef4ff", outline="#2f67b1", width=4)
    draw.text((1060, 274), "结果", fill="#2f67b1", font=font(40, bold=True))
    draw.text((1060, 356), "像逗号", fill="#5a5146", font=font(36, bold=True))
    draw.text((1060, 426), "不是句号", fill="#5a5146", font=font(36, bold=True))
    draw.text((1060, 496), "等下一句继续", fill="#2f67b1", font=font(31, bold=True))

    draw.line((398, 430, 560, 430), fill="#9b8a74", width=8)
    draw.polygon([(560, 430), (526, 410), (526, 450)], fill="#9b8a74")
    draw.line((860, 430, 1022, 430), fill="#9b8a74", width=8)
    draw.polygon([(1022, 430), (988, 410), (988, 450)], fill="#9b8a74")

    draw.rounded_rectangle((122, 690, 1296, 790), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((154, 720), "一句话理解：半终止就是把句子停在属和弦上，让音乐明显还想继续。", fill="#6a5644", font=font(33, bold=True))

    img.save(ASSET_DIR / "half-cadence-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
