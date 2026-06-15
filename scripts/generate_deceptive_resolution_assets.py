from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-05-19-deceptive-resolution"
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


def draw_note(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str):
    draw.ellipse((x - 28, y - 28, x + 28, y + 28), fill=color, outline="#ffffff", width=3)
    center_text(draw, (x - 24, y - 18, x + 24, y + 14), label, "#ffffff", font(21, bold=True))


def save_piano_chart():
    img = Image.new("RGB", (1560, 980), "#f6f2ea")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：延缓解决 Deceptive Resolution", fill="#2f261d", font=font(56, bold=True))
    draw.text(
        (52, 106),
        "在 A 小调里，耳朵本来以为 E7 会回到 Am，但如果它先转去 F，就会产生“本该落地却被拐走”的效果。",
        fill="#66594b",
        font=font(28),
    )

    draw.rounded_rectangle((70, 182, 746, 882), 28, fill="#eef6ff", outline="#b9cbe8", width=3)
    draw.rounded_rectangle((814, 182, 1490, 882), 28, fill="#fff4e8", outline="#e0c29c", width=3)

    draw.text((102, 218), "预期解决", fill="#3d639c", font=font(40, bold=True))
    draw.text((102, 276), "E7 -> Am", fill="#3d639c", font=font(32, bold=True))
    draw.text((102, 340), "G# -> A", fill="#4e6179", font=font(29, bold=True))
    draw.text((102, 390), "D -> C", fill="#4e6179", font=font(29))
    draw.text((102, 440), "低音 E -> A", fill="#4e6179", font=font(29))
    draw.text((102, 520), "听感：稳定、完整、", fill="#4e6179", font=font(30))
    draw.text((102, 568), "像标准终止真正落地。", fill="#4e6179", font=font(30))

    draw.text((846, 218), "延缓解决", fill="#a9642b", font=font(40, bold=True))
    draw.text((846, 276), "E7 -> F", fill="#a9642b", font=font(32, bold=True))
    draw.text((846, 340), "G# -> A（内声部可先保留张力）", fill="#6c5a45", font=font(29, bold=True))
    draw.text((846, 390), "D -> C", fill="#6c5a45", font=font(29))
    draw.text((846, 440), "低音 E -> F", fill="#6c5a45", font=font(29))
    draw.text((846, 520), "听感：像要回家，", fill="#6c5a45", font=font(30))
    draw.text((846, 568), "却先被带去别处。", fill="#6c5a45", font=font(30))

    expected_notes = [("E", 156, 706, "#3d639c"), ("G#", 260, 706, "#bd7a2f"), ("B", 364, 706, "#2f8b61"), ("D", 468, 706, "#5f7fb8")]
    am_notes = [("A", 610, 706, "#7d4fe0"), ("C", 676, 640, "#7d4fe0"), ("E", 706, 706, "#7d4fe0")]
    deceptive_notes = [("F", 1364, 706, "#cf7e3e"), ("A", 1260, 706, "#cf7e3e"), ("C", 1328, 640, "#cf7e3e")]

    for note, x, y, color in expected_notes + am_notes + deceptive_notes:
        draw_note(draw, x, y, note, color)

    draw.line((500, 706, 572, 706), fill="#88a7d0", width=7)
    draw.polygon([(572, 706), (550, 692), (550, 720)], fill="#88a7d0")
    draw.text((520, 656), "应有的落地", fill="#6e87a7", font=font(22, bold=True))

    draw.line((500, 748, 1220, 748), fill="#c9a071", width=7)
    draw.polygon([(1220, 748), (1198, 734), (1198, 762)], fill="#c9a071")
    draw.text((772, 778), "先延缓，再决定是否回到 i", fill="#8d6b43", font=font(22, bold=True))

    draw.rounded_rectangle((98, 804, 1464, 918), 24, fill="#fffdf8", outline="#d8ccbd", width=3)
    draw.text(
        (126, 836),
        "钢琴练法：左手固定低音，右手先弹 E7 -> Am，再弹 E7 -> F。对比“终止真正完成”和“终止被暂时偏转”这两种感觉。",
        fill="#5e5448",
        font=font(27, bold=True),
    )

    img.save(ASSET_DIR / "piano-deceptive-resolution.png")


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 118
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 424, y + 470), 28, fill="#fffdfa", outline="#d2d6db", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#21323a", font=font(34, bold=True))
    draw.text((x + 28, y + 72), subtitle, fill="#66757d", font=font(20))

    for i in range(6):
        sx = grid_left + i * string_gap
        draw.line((sx, grid_top, sx, grid_top + 4 * fret_gap), fill="#2d3748", width=4)
    for i in range(5):
        sy = grid_top + i * fret_gap
        draw.line((grid_left, sy, grid_left + 5 * string_gap, sy), fill="#2d3748", width=8 if i == 0 else 4)

    for fret, string_idx, label in dots:
        cx = grid_left + string_idx * string_gap
        cy = grid_top + (fret - 0.5) * fret_gap
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#ffffff", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#ffffff", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#56656f", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 246, sx + 12, grid_top + 278), name, "#56656f", font(16, bold=True))

    draw.text((x + 28, y + 404), footnote, fill="#52656e", font=font(19))


def save_guitar_chart():
    img = Image.new("RGB", (1520, 1000), "#edf4f6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：用和弦循环听见“被骗开的终止”", fill="#17313b", font=font(54, bold=True))
    draw.text(
        (58, 106),
        "吉他上最常见的 deceptive resolution 不是复杂的理论推导，而是你以为属和弦要回主和弦，结果它先转到 VI 或相关和弦。",
        fill="#4d636c",
        font=font(26),
    )

    draw.rounded_rectangle((86, 178, 1432, 320), 26, fill="#fffdfa", outline="#c4d0d6", width=3)
    draw.text((114, 218), "推荐比较：| Am | E7 | Am | 和 | Am | E7 | F |。第一种是正常落地，第二种是故意延缓回家。", fill="#223943", font=font(31, bold=True))
    draw.text((114, 266), "如果想把戏剧感再放大，可继续弹 | Am | E7 | F | E7 | Am |，让“偏转后再回归”的路线更清楚。", fill="#516771", font=font(25))

    draw_chord_grid(
        draw,
        88,
        392,
        "Am",
        "x 0 2 2 1 0",
        [(2, 1, "2"), (2, 2, "3"), (1, 3, "1")],
        {0: "X", 4: "O", 5: "O"},
        "主和弦：稳定中心。",
        "#2f8b61",
    )
    draw_chord_grid(
        draw,
        548,
        392,
        "E7",
        "0 2 0 1 0 0",
        [(2, 1, "2"), (1, 3, "1")],
        {0: "O", 2: "O", 4: "O", 5: "O"},
        "属七：制造“马上要解决”的预期。",
        "#5f7fb8",
    )
    draw_chord_grid(
        draw,
        1008,
        392,
        "F",
        "1 3 3 2 1 1",
        [(1, 0, "1"), (3, 1, "3"), (3, 2, "4"), (2, 3, "2"), (1, 4, "1"), (1, 5, "1")],
        {},
        "VI 色彩：把终止先拐开，制造继续进行的空间。",
        "#cf7e3e",
    )

    draw.line((512, 626, 548, 626), fill="#95a1a7", width=7)
    draw.polygon([(548, 626), (528, 614), (528, 638)], fill="#95a1a7")
    draw.line((972, 626, 1008, 626), fill="#c1a075", width=7)
    draw.polygon([(1008, 626), (988, 614), (988, 638)], fill="#c1a075")

    draw.rounded_rectangle((86, 868, 1432, 956), 24, fill="#fffaf4", outline="#c9d3d8", width=3)
    draw.text(
        (114, 898),
        "吉他练法：先下拨比较两种三和弦循环，再把 F 后面补回 E7 -> Am。你会听到 deceptive resolution 的重点不是“不解决”，而是“先不让你立刻解决”。",
        fill="#4d5f68",
        font=font(27, bold=True),
    )

    img.save(ASSET_DIR / "guitar-deceptive-resolution.png")


def save_structure_chart():
    img = Image.new("RGB", (1460, 920), "#f8f6f1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Deceptive Resolution 是怎么工作的", fill="#2d261d", font=font(52, bold=True))
    draw.text(
        (56, 106),
        "核心不是“不解决”，而是先让你以为会回到 i，再把这个预期拐到别的和弦上，从而延缓真正的稳定。",
        fill="#655a4e",
        font=font(27),
    )

    draw.rounded_rectangle((86, 194, 650, 764), 26, fill="#eef4ff", outline="#5f7fb8", width=4)
    draw.text((118, 232), "标准终止", fill="#5f7fb8", font=font(42, bold=True))
    draw.text((118, 308), "V7 -> i", fill="#4d5d70", font=font(34, bold=True))
    draw.text((118, 384), "预期：属功能出现后", fill="#4d5d70", font=font(30))
    draw.text((118, 430), "耳朵准备好听主和弦落地", fill="#4d5d70", font=font(30))
    draw.text((118, 506), "结果：稳定完成", fill="#4d5d70", font=font(30))
    draw.text((118, 552), "句子可以就此收住", fill="#4d5d70", font=font(30))
    draw.text((118, 628), "听感关键词：完整、明确、", fill="#4d5d70", font=font(30))
    draw.text((118, 674), "标准回家", fill="#4d5d70", font=font(30))

    draw.rounded_rectangle((808, 194, 1372, 764), 26, fill="#fff2e7", outline="#bd7a2f", width=4)
    draw.text((840, 232), "延缓解决", fill="#bd7a2f", font=font(42, bold=True))
    draw.text((840, 308), "V7 -> VI 或相关和弦", fill="#6e5437", font=font(34, bold=True))
    draw.text((840, 384), "预期：本来该回 i", fill="#6e5437", font=font(30))
    draw.text((840, 430), "结果：先被带向别处", fill="#6e5437", font=font(30))
    draw.text((840, 506), "作用：延长句子、制造戏剧感、", fill="#6e5437", font=font(30))
    draw.text((840, 552), "让后面的真正终止更有分量", fill="#6e5437", font=font(30))
    draw.text((840, 628), "听感关键词：意外、偏转、", fill="#6e5437", font=font(30))
    draw.text((840, 674), "先不让你落地", fill="#6e5437", font=font(30))

    draw.line((650, 476, 808, 476), fill="#9f907e", width=8)
    draw.polygon([(808, 476), (784, 462), (784, 490)], fill="#9f907e")
    draw.text((682, 432), "预期被改写", fill="#7a664f", font=font(24, bold=True))

    draw.rounded_rectangle((120, 804, 1302, 872), 24, fill="#fffaf0", outline="#d0b892", width=3)
    draw.text(
        (148, 824),
        "一句人话：Deceptive Resolution 不是把终止取消，而是把“应该现在回家”的感觉先骗开，等后面再真正落地。",
        fill="#5f5547",
        font=font(29, bold=True),
    )

    img.save(ASSET_DIR / "deceptive-resolution-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
