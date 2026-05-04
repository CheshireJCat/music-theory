from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-04-cadential-64"
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
    img = Image.new("RGB", (1520, 980), "#f7f0e6")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)

    draw.text((68, 40), "钢琴示意：终止四六 I6/4 -> V -> I", fill="#2b241c", font=title)
    draw.text(
        (68, 108),
        "在 C 大调里常写成 C/G -> G(或 G7) -> C。虽然开头看起来像 I 和弦，但这里的 6/4 更像属功能前的加强装饰。",
        fill="#675a4b",
        font=body,
    )

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 155
    white_h = 330
    x0 = 78
    y0 = 236

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 22, y0 + 278), name, fill="#56606d", font=font(30, bold=True))

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 92
    black_h = 208
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 146, x + black_w, y0 + black_h), name, "#f9fafb", font(19, bold=True))

    def mark_white(note_idx: int, note: str, color: str, cy: int, label: str):
        cx = x0 + note_idx * white_w + white_w / 2
        draw.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=color, outline="#ffffff", width=4)
        center_text(draw, (cx - 36, cy - 40, cx + 36, cy - 6), note, "#ffffff", font(21, bold=True))
        center_text(draw, (cx - 36, cy - 2, cx + 36, cy + 24), label, "#ffffff", font(16, bold=True))

    for idx, note in [(0, "C"), (2, "E"), (4, "G")]:
        mark_white(idx, note, "#2f67b1", y0 + 132, "I6/4")
    for idx, note in [(1, "D"), (4, "G"), (6, "B")]:
        mark_white(idx, note, "#b7791f", y0 + 216, "V")
    for idx, note in [(0, "C"), (2, "E"), (4, "G")]:
        mark_white(idx, note, "#2f8f5b", y0 + 292, "I")

    draw.rounded_rectangle((82, 596, 1450, 716), 24, fill="#fff8ef", outline="#ceb89f", width=3)
    draw.text((112, 630), "蓝：I6/4 = G 低音上的 C-E-G    金：V = G-B-D    绿：I = C-E-G", fill="#4b5563", font=font(33, bold=True))

    draw.rounded_rectangle((1016, 166, 1446, 552), 26, fill="#fffaf4", outline="#d8cbbb", width=3)
    draw.text((1042, 198), "听感重点", fill="#2b241c", font=font(38, bold=True))
    draw.text((1042, 270), "1. 先把重心放在 G 低音", fill="#675a4b", font=body)
    draw.text((1042, 332), "2. 4 度与 6 度向内收紧", fill="#675a4b", font=body)
    draw.text((1042, 394), "3. 再解决到主和弦 I", fill="#675a4b", font=body)
    draw.text((1042, 474), "它不是单纯“再弹一次 I”", fill="#8a5a2c", font=font(30, bold=True))

    draw.rounded_rectangle((86, 774, 1420, 902), 28, fill="#fffdf8", outline="#d9c8b2", width=3)
    draw.text(
        (118, 800),
        "钢琴练法：左手保持 G -> G -> C，右手弹 C-E-G -> B-D-G -> C-E-G。听右手的 C 下行到 B、E 下行到 D，感受它如何把终止推向 V 再落地。",
        fill="#5a5045",
        font=body,
    )

    img.save(ASSET_DIR / "piano-cadential-64.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, base_fret="1fr"):
    grid_left = x + 64
    grid_top = y + 112
    fret_gap = 58
    string_gap = 44

    draw.rounded_rectangle((x, y, x + 386, y + 466), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#1d3136", font=font(34, bold=True))
    draw.text((x + 28, y + 68), subtitle, fill="#60717a", font=font(21))
    draw.text((x + 290, y + 102), base_fret, fill="#60717a", font=font(18, bold=True))

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
    img = Image.new("RGB", (1500, 980), "#edf3f6")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 42), "吉他示意：把终止四六当成 V 的前奏", fill="#17303a", font=title)
    draw.text(
        (68, 112),
        "吉他里不一定总写成完整古典记谱，但在收尾时常会听到“先把低音停在 G，再把上方音收向 G 或 G7，最后回 C”的效果。",
        fill="#49626b",
        font=body,
    )

    draw.rounded_rectangle((96, 196, 1410, 320), 28, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((126, 230), "实用理解：Cadential 6/4 不是另一个独立功能的 I，而是“站在 V 上、准备推向终止”的 I6/4。", fill="#17303a", font=font(32, bold=True))

    draw_chord_grid(
        draw,
        92,
        384,
        "C/G",
        "I6/4：保持 G 低音",
        [(3, 1, "3", "#2f67b1"), (2, 3, "2", "#2f67b1"), (1, 4, "1", "#2f67b1")],
        {0: "3", 2: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        548,
        384,
        "G7",
        "V：张力集中",
        [(2, 0, "2", "#b7791f"), (1, 1, "1", "#b7791f"), (2, 4, "3", "#b7791f"), (1, 5, "4", "#b7791f")],
        {2: "O", 3: "O"},
    )
    draw_chord_grid(
        draw,
        1004,
        384,
        "C",
        "I：稳定结束",
        [(3, 1, "3", "#2f8f5b"), (2, 3, "2", "#2f8f5b"), (1, 4, "1", "#2f8f5b")],
        {0: "X", 2: "O", 5: "O"},
    )

    draw.rounded_rectangle((92, 872, 1410, 936), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((120, 892), "吉他练法：循环 | C/G | G7 | C |，重点听高音 C -> B、E -> D 的收紧，再回到 C 的落地感。", fill="#4d5f68", font=font(29, bold=True))

    img.save(ASSET_DIR / "guitar-cadential-64.png")


def save_structure_chart():
    img = Image.new("RGB", (1440, 900), "#f8f7f2")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 44), "结构图：为什么 I6/4 会加强终止", fill="#2c261f", font=title)
    draw.text((68, 114), "把主和弦放在属音低音之上时，会形成需要向内解决的 6 度和 4 度，所以它更像 V 的扩展。", fill="#665d52", font=body)

    draw.rounded_rectangle((96, 214, 392, 642), 30, fill="#eef5ff", outline="#2f67b1", width=4)
    draw.text((136, 254), "I6/4", fill="#2f67b1", font=font(42, bold=True))
    draw.text((136, 338), "低音：G", fill="#5a5146", font=body)
    draw.text((136, 394), "上方音：C 与 E", fill="#5a5146", font=body)
    draw.text((136, 450), "它们分别形成 4 度与 6 度", fill="#5a5146", font=font(26, bold=True))
    draw.text((136, 534), "下一步倾向：C -> B，E -> D", fill="#8b5a28", font=font(25, bold=True))

    draw.rounded_rectangle((572, 214, 868, 642), 30, fill="#fff8ee", outline="#d2b071", width=4)
    draw.text((654, 254), "V", fill="#b7791f", font=font(42, bold=True))
    draw.text((618, 338), "低音仍是 G", fill="#5a5146", font=body)
    draw.text((618, 394), "上方音收成 B 与 D", fill="#5a5146", font=body)
    draw.text((618, 450), "属功能被明确强化", fill="#5a5146", font=font(26, bold=True))
    draw.text((618, 534), "张力准备落向主和弦", fill="#8b5a28", font=font(25, bold=True))

    draw.rounded_rectangle((1048, 214, 1344, 642), 30, fill="#f4fbf5", outline="#2f8f5b", width=4)
    draw.text((1162, 254), "I", fill="#2f8f5b", font=font(42, bold=True))
    draw.text((1088, 338), "低音回到 C", fill="#5a5146", font=body)
    draw.text((1088, 394), "张力完全解决", fill="#5a5146", font=body)
    draw.text((1088, 450), "终止感比直接 V-I 更铺垫", fill="#5a5146", font=font(26, bold=True))
    draw.text((1088, 534), "常见于正式收尾", fill="#8b5a28", font=font(25, bold=True))

    draw.line((392, 428, 572, 428), fill="#9b8a74", width=8)
    draw.polygon([(572, 428), (538, 408), (538, 448)], fill="#9b8a74")
    draw.line((868, 428, 1048, 428), fill="#9b8a74", width=8)
    draw.polygon([(1048, 428), (1014, 408), (1014, 448)], fill="#9b8a74")

    draw.rounded_rectangle((120, 716, 1318, 816), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((146, 746), "一句话：终止四六是“主和弦外形、属和弦功能”，它先把终止感拉紧，再让 V-I 的解决更有分量。", fill="#6a5644", font=font(31, bold=True))

    img.save(ASSET_DIR / "cadential-64-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
