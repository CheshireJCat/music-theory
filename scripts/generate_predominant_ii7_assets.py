from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-06-predominant-ii7"
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


def draw_arrow(draw, x1, y1, x2, y2, color):
    draw.line((x1, y1, x2, y2), fill=color, width=8)
    draw.polygon([(x2, y2), (x2 - 26, y2 - 14), (x2 - 26, y2 + 14)], fill=color)


def mark_white(draw, x0, y0, white_w, note_idx: int, note: str, color: str, cy: int, label: str):
    cx = x0 + note_idx * white_w + white_w / 2
    draw.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=color, outline="#ffffff", width=4)
    center_text(draw, (cx - 36, cy - 40, cx + 36, cy - 6), note, "#ffffff", font(21, bold=True))
    center_text(draw, (cx - 36, cy - 2, cx + 36, cy + 24), label, "#ffffff", font(16, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1520, 980), "#f4efe7")
    draw = ImageDraw.Draw(img)
    title = font(54, bold=True)
    body = font(28)

    draw.text((64, 40), "钢琴示意：ii7 让前属功能更顺地流向 V", fill="#2c241b", font=title)
    draw.text(
        (64, 108),
        "以 C 大调为例，ii7 = D-F-A-C。比起 Dm，加入七度音 C 以后，和 G 或 G7 的连接会更连贯，声部也更容易级进。",
        fill="#6d5f51",
        font=body,
    )

    white_names = ["C", "D", "E", "F", "G", "A", "B", "C"]
    white_w = 155
    white_h = 330
    x0 = 76
    y0 = 236

    for i, name in enumerate(white_names):
        x = x0 + i * white_w
        draw.rectangle((x, y0, x + white_w, y0 + white_h), fill="#fffdfa", outline="#1f2937", width=3)
        draw.text((x + 22, y0 + 278), name, fill="#5d6671", font=font(30, bold=True))

    black_positions = [0, 1, 3, 4, 5]
    black_names = ["C#/Db", "D#/Eb", "F#/Gb", "G#/Ab", "A#/Bb"]
    black_w = 92
    black_h = 208
    for idx, name in zip(black_positions, black_names):
        x = x0 + white_w * (idx + 1) - black_w / 2
        draw.rounded_rectangle((x, y0, x + black_w, y0 + black_h), 10, fill="#111827")
        center_text(draw, (x, y0 + 146, x + black_w, y0 + black_h), name, "#f9fafb", font(19, bold=True))

    for idx, note in [(1, "D"), (3, "F"), (5, "A"), (7, "C")]:
        mark_white(draw, x0, y0, white_w, idx, note, "#3d78c2", y0 + 118, "ii7")
    for idx, note in [(4, "G"), (6, "B"), (1, "D"), (3, "F")]:
        mark_white(draw, x0, y0, white_w, idx, note, "#c48327", y0 + 208, "V7")
    for idx, note in [(0, "C"), (2, "E"), (4, "G")]:
        mark_white(draw, x0, y0, white_w, idx, note, "#2f8f5b", y0 + 292, "I")

    draw.rounded_rectangle((80, 596, 1450, 716), 24, fill="#fff9ef", outline="#d6c2a5", width=3)
    draw.text((104, 626), "蓝：ii7 = D-F-A-C    金：V7 = G-B-D-F    绿：I = C-E-G", fill="#4b5563", font=font(33, bold=True))

    draw.rounded_rectangle((1000, 164, 1448, 556), 26, fill="#fffaf4", outline="#d8cbbb", width=3)
    draw.text((1028, 198), "连接重点", fill="#2b241c", font=font(38, bold=True))
    draw.text((1028, 270), "1. 新增的 C 是和弦七度", fill="#675a4b", font=body)
    draw.text((1028, 332), "2. C 往下到 B，张力更明确", fill="#675a4b", font=body)
    draw.text((1028, 394), "3. F 可保留到 V7，连接更平滑", fill="#675a4b", font=body)
    draw.text((1028, 474), "ii7 常比 ii 更有“推力”", fill="#8a5a2c", font=font(30, bold=True))

    draw.rounded_rectangle((84, 774, 1432, 904), 28, fill="#fffdf8", outline="#d9c8b2", width=3)
    draw.text(
        (114, 800),
        "钢琴练法：左手弹 D -> G -> C，右手弹 C-F-A-D -> B-F-G-D -> C-E-G。重点去听 C 下行到 B 的吸引力。",
        fill="#5a5045",
        font=body,
    )

    img.save(ASSET_DIR / "piano-predominant-ii7.png")


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

    draw.text((68, 42), "吉他示意：Dm7-G7-C 比 Dm-G-C 更有连续感", fill="#17303a", font=title)
    draw.text(
        (68, 112),
        "在吉他上，ii7-V7-I 往往比三和弦版更容易听出和声流动，因为共同音和半音下行会更明显。",
        fill="#49626b",
        font=body,
    )

    draw.rounded_rectangle((94, 194, 1410, 320), 28, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((120, 230), "核心听感：Dm7 里的 C 会自然向下到 G7 里的 B，这个半音运动就是 ii7 常见的推进来源。", fill="#17303a", font=font(31, bold=True))

    draw_chord_grid(
        draw,
        92,
        384,
        "Dm7",
        "ii7：前属更柔顺",
        [(2, 2, "2", "#3d78c2"), (1, 4, "1", "#3d78c2"), (1, 5, "1", "#3d78c2")],
        {0: "X", 3: "O"},
    )
    draw_chord_grid(
        draw,
        548,
        384,
        "G7",
        "V7：张力集中",
        [(2, 0, "2", "#c48327"), (3, 1, "3", "#c48327"), (1, 4, "1", "#c48327")],
        {2: "O", 3: "O", 5: "O"},
    )
    draw_chord_grid(
        draw,
        1004,
        384,
        "C",
        "I：稳定解决",
        [(3, 1, "3", "#2f8f5b"), (2, 3, "2", "#2f8f5b"), (1, 4, "1", "#2f8f5b")],
        {0: "X", 2: "O", 5: "O"},
    )

    draw.rounded_rectangle((92, 872, 1410, 936), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text((112, 892), "吉他练法：循环 | Dm7 | G7 | C |，先 4 拍下扫，再改成 6-4-3-2 分解，专门听 C -> B 的半音下行。", fill="#4d5f68", font=font(28, bold=True))

    img.save(ASSET_DIR / "guitar-predominant-ii7.png")


def save_voice_leading_chart():
    img = Image.new("RGB", (1440, 900), "#f8f7f2")
    draw = ImageDraw.Draw(img)
    title = font(56, bold=True)
    body = font(28)

    draw.text((68, 44), "声部连接图：ii7 为什么比 ii 更顺", fill="#2c261f", font=title)
    draw.text((68, 114), "这里看的是最关键的两个连接点：共同音保留，以及和弦七度向下解决。它们让 ii7 -> V7 -> I 更像连续的语句。", fill="#665d52", font=body)

    boxes = [
        (100, 232, 420, 636, "#edf4ff", "#3d78c2", "Dm7", ["D-F-A-C", "新增七度：C", "任务：把音乐推出去"]),
        (560, 232, 880, 636, "#fff7eb", "#c48327", "G7", ["G-B-D-F", "C -> B 下行", "F 可作为共同张力音"]),
        (1020, 232, 1340, 636, "#f1fbf4", "#2f8f5b", "C", ["C-E-G", "B -> C 解决", "E 吸收前面的张力"]),
    ]

    for left, top, right, bottom, fill, outline, head, lines in boxes:
        draw.rounded_rectangle((left, top, right, bottom), 30, fill=fill, outline=outline, width=4)
        draw.text((left + 100, top + 40), head, fill=outline, font=font(42, bold=True))
        draw.text((left + 42, top + 136), lines[0], fill="#5a5146", font=body)
        draw.text((left + 42, top + 228), lines[1], fill="#5a5146", font=font(26, bold=True))
        draw.text((left + 42, top + 320), lines[2], fill="#8b5a28", font=font(25, bold=True))

    draw_arrow(draw, 420, 434, 560, 434, "#9b8a74")
    draw_arrow(draw, 880, 434, 1020, 434, "#9b8a74")

    draw.rounded_rectangle((146, 696, 1296, 812), 26, fill="#fff8ee", outline="#d2b071", width=3)
    draw.text((174, 724), "一句话：ii7 多出来的七度音，往往给 V 提供更明确的下行目标，所以“前属”会更连、更像在推动句子。", fill="#6a5644", font=font(30, bold=True))

    img.save(ASSET_DIR / "voice-leading-ii7.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_voice_leading_chart()
