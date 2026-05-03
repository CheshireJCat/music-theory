from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-03-plagal-cadence"
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
    img = Image.new("RGB", (1500, 940), "#f5efe5")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)
    small = font(23)

    draw.text((68, 42), "钢琴示意：变格终止 IV-I 的柔和收束", fill="#2d261d", font=title)
    draw.text((68, 108), "以 C 大调为例，F -> C 是最常见的变格终止。它不像 V-I 那么强烈，而是更平稳地落回主和弦。", fill="#67594b", font=body)

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 155
    white_h = 330
    x0 = 80
    y0 = 232

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 20, y0 + 278), name, fill="#5b6471", font=font(30, bold=True))

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
        center_text(draw, (cx - 36, cy - 42, cx + 36, cy - 5), note, "#ffffff", font(21, bold=True))
        center_text(draw, (cx - 36, cy + 0, cx + 36, cy + 28), label, "#ffffff", font(16, bold=True))

    for idx, note in [(3, "F"), (5, "A"), (0, "C")]:
        mark_white(idx, note, "#2f67b1", y0 + 168, "IV")
    for idx, note in [(0, "C"), (2, "E"), (4, "G")]:
        mark_white(idx, note, "#2f8f5b", y0 + 258, "I")

    draw.rounded_rectangle((78, 596, 1450, 706), 24, fill="#fff8ef", outline="#c7b39c", width=3)
    draw.text((108, 628), "蓝色上排：IV = F-A-C     绿色下排：I = C-E-G", fill="#355c8d", font=font(34, bold=True))

    draw.rounded_rectangle((1000, 162, 1440, 534), 26, fill="#fffaf4", outline="#d8cbbb", width=3)
    draw.text((1032, 194), "听感重点", fill="#2d261d", font=font(38, bold=True))
    draw.text((1032, 270), "1. 没有导音强解决", fill="#67594b", font=body)
    draw.text((1032, 330), "2. 共享 C 这个共同音", fill="#67594b", font=body)
    draw.text((1032, 390), "3. 像安静收束，不像强句号", fill="#67594b", font=body)
    draw.text((1032, 466), "常见于圣歌、抒情尾句", fill="#8a5a2c", font=font(30, bold=True))

    draw.rounded_rectangle((84, 764, 1418, 892), 28, fill="#fffdf8", outline="#d9c8b2", width=3)
    draw.text((118, 792), "钢琴练法：左手弹 F -> C，右手先弹 F-A-C 再弹 C-E-G。感受它是“落稳”，但不像 G7 -> C 那样带明显张力释放。", fill="#5a5045", font=body)
    draw.text((118, 842), "如果把它放在歌曲结尾，常会有一种更温和、更像余韵的结束感。", fill="#5a5045", font=small)

    img.save(ASSET_DIR / "piano-plagal-cadence.png")


def draw_chord_diagram(draw, x, y, title_text, subtitle, dots, top_marks):
    grid_left = x + 64
    grid_top = y + 106
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

    draw.text((70, 44), "吉他示意：变格终止常见于柔和收尾", fill="#163038", font=title)
    draw.text((70, 112), "在吉他伴奏里，Plagal Cadence 常写成 IV-I。C 大调里最直接的例子是 F -> C，也常被叫作“阿门终止”。", fill="#49626b", font=body)

    draw.rounded_rectangle((96, 196, 450, 348), 28, fill="#fffdfa", outline="#bfcfc8", width=3)
    draw.text((124, 228), "终止式名称", fill="#163038", font=font(34, bold=True))
    draw.text((124, 290), "Plagal Cadence = IV-I", fill="#49626b", font=font(29))

    draw_chord_diagram(
        draw,
        110,
        400,
        "IV = F",
        "先铺开，再回主和弦",
        [(1, 0, "1", "#2f67b1"), (2, 2, "2", "#2f67b1"), (3, 3, "3", "#2f67b1")],
        {0: "X", 4: "O", 5: "O"},
    )
    draw_chord_diagram(
        draw,
        570,
        400,
        "I = C",
        "温和稳定的落点",
        [(3, 1, "3", "#2f8f5b"), (2, 3, "2", "#2f8f5b"), (1, 4, "1", "#2f8f5b")],
        {0: "X", 2: "O", 5: "O"},
    )

    draw.rounded_rectangle((1026, 222, 1392, 856), 28, fill="#fffdfa", outline="#c4d1cb", width=3)
    draw.text((1054, 256), "常见场景", fill="#163038", font=font(36, bold=True))
    draw.text((1054, 328), "1. 歌曲尾句最后两拍", fill="#49626b", font=body)
    draw.text((1054, 388), "2. 圣歌或合唱式收尾", fill="#49626b", font=body)
    draw.text((1054, 448), "3. 抒情段落淡出结尾", fill="#49626b", font=body)
    draw.text((1054, 540), "实用练法", fill="#7a5530", font=font(31, bold=True))
    draw.text((1054, 590), "循环 | C | G | F | C |", fill="#49626b", font=body)
    draw.text((1054, 644), "第三小节把扫弦压低，", fill="#49626b", font=body)
    draw.text((1054, 688), "最后回 C 时留一点余音", fill="#49626b", font=body)

    img.save(ASSET_DIR / "guitar-plagal-cadence.png")


def save_structure_chart():
    img = Image.new("RGB", (1420, 860), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 48), "结构图：变格终止为什么更柔和", fill="#2c261f", font=title)
    draw.text((68, 118), "它同样会回到主和弦，但没有 V-I 那种强烈的属功能推动，所以收束感更平静。", fill="#665d52", font=body)

    draw.rounded_rectangle((100, 220, 390, 610), 30, fill="#fffdf8", outline="#2f67b1", width=4)
    draw.text((150, 258), "IV", fill="#2f67b1", font=font(42, bold=True))
    draw.text((150, 340), "功能：下属", fill="#5a5146", font=body)
    draw.text((150, 396), "听感：展开、铺垫", fill="#5a5146", font=body)
    draw.text((150, 470), "例：F", fill="#8b5a28", font=font(31, bold=True))

    draw.rounded_rectangle((560, 220, 860, 610), 30, fill="#fff8ee", outline="#d2b071", width=4)
    draw.text((618, 258), "过渡特点", fill="#8b5a28", font=font(40, bold=True))
    draw.text((618, 338), "A -> G", fill="#5a5146", font=font(34, bold=True))
    draw.text((618, 392), "F -> E", fill="#5a5146", font=font(34, bold=True))
    draw.text((618, 446), "C 作为共同音保留", fill="#5a5146", font=font(28, bold=True))
    draw.text((618, 510), "因此更像平稳落下", fill="#5a5146", font=font(24))

    draw.rounded_rectangle((1030, 220, 1320, 610), 30, fill="#f8fdf9", outline="#2f8f5b", width=4)
    draw.text((1112, 258), "I", fill="#2f8f5b", font=font(42, bold=True))
    draw.text((1080, 340), "功能：主", fill="#5a5146", font=body)
    draw.text((1070, 396), "听感：稳定、安静结束", fill="#5a5146", font=body)
    draw.text((1108, 470), "例：C", fill="#2f8f5b", font=font(31, bold=True))

    draw.line((390, 416, 560, 416), fill="#9b8a74", width=8)
    draw.polygon([(560, 416), (526, 396), (526, 436)], fill="#9b8a74")
    draw.line((860, 416, 1030, 416), fill="#9b8a74", width=8)
    draw.polygon([(1030, 416), (996, 396), (996, 436)], fill="#9b8a74")

    draw.rounded_rectangle((118, 690, 1298, 790), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((148, 720), "一句话理解：变格终止是下属功能回到主和弦，像温柔落地，不像强烈句号。", fill="#6a5644", font=font(33, bold=True))

    img.save(ASSET_DIR / "plagal-cadence-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
