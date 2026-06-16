from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/nekos/daily/music-theory")
ASSET_DIR = ROOT / "assets" / "2026-06-16-mozambique-bell-pattern"
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


def draw_hit(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, color: str, state: str = "", *, size: int = 24):
    draw.rounded_rectangle((x - 48, y - 32, x + 48, y + 32), 18, fill=color, outline="#FFFFFF", width=3)
    center_text(draw, (x - 42, y - 22, x + 42, y + 22), label, "#FFFFFF", font(size, bold=True))
    if state:
        draw.text((x - 28, y + 44), state, fill="#5B5D61", font=font(18, bold=True))


def draw_chord_grid(draw, x, y, title_text, subtitle, dots, top_marks, footnote, color):
    grid_left = x + 74
    grid_top = y + 116
    fret_gap = 52
    string_gap = 38

    draw.rounded_rectangle((x, y, x + 304, y + 470), 28, fill="#FFFDF9", outline="#D2D6DB", width=3)
    draw.text((x + 28, y + 24), title_text, fill="#21323A", font=font(34, bold=True))
    draw.text((x + 28, y + 72), subtitle, fill="#66757D", font=font(20))

    for i in range(6):
        sx = grid_left + i * string_gap
        draw.line((sx, grid_top, sx, grid_top + 4 * fret_gap), fill="#2D3748", width=4)
    for i in range(5):
        sy = grid_top + i * fret_gap
        draw.line((grid_left, sy, grid_left + 5 * string_gap, sy), fill="#2D3748", width=8 if i == 0 else 4)

    for fret, string_idx, label in dots:
        cx = grid_left + string_idx * string_gap
        cy = grid_top + (fret - 0.5) * fret_gap
        draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=color, outline="#FFFFFF", width=3)
        center_text(draw, (cx - 18, cy - 16, cx + 18, cy + 14), label, "#FFFFFF", font(15, bold=True))

    for idx, mark in top_marks.items():
        sx = grid_left + idx * string_gap
        center_text(draw, (sx - 18, grid_top - 40, sx + 18, grid_top - 10), mark, "#56656F", font(15, bold=True))

    for i, name in enumerate(["E", "A", "D", "G", "B", "e"]):
        sx = grid_left + i * string_gap
        center_text(draw, (sx - 12, grid_top + 246, sx + 12, grid_top + 278), name, "#56656F", font(16, bold=True))

    draw.text((x + 28, y + 404), footnote, fill="#52656E", font=font(17))


def save_piano_chart():
    img = Image.new("RGB", (1560, 1000), "#F4EFE8")
    draw = ImageDraw.Draw(img)
    draw.text((52, 38), "钢琴图：Mozambique Bell Pattern 的前冲组织感", fill="#2E241C", font=font(52, bold=True))
    draw.text(
        (52, 102),
        "Mozambique bell 比 campana 更像主动往前推的时间线。钢琴上适合把它放在右手高音区，左手保持 tumbao 或 pedal，让整个 groove 更像在向前卷。",
        fill="#67584C",
        font=font(28),
    )

    panels = [
        ((74, 184, 486, 900), "#FFF5E9", "#DFC7A7", "时间功能", "更强的前冲组织", "它不只是点亮外框，而是把 clave 感、推进感和句法方向一起收束到同一条 bell 线上。", "#BA7A37"),
        ((574, 184, 986, 900), "#EEF4FF", "#B2C5DF", "和 campana 对比", "更紧、更推、更像带节奏", "campana 更像外层提示；Mozambique 更像把提示变成带着编制向前冲的组织力。", "#476F9D"),
        ((1074, 184, 1486, 900), "#EEF8F0", "#AFCCB5", "钢琴应用", "右手 bell + 左手 tumbao", "右手可固定 E 或 E-B 的短音，左手用 A-C-E-G 的分解低音，让 bell 持续往前拉。", "#4F8265"),
    ]
    for box, fill, outline, title, accent, desc, tone in panels:
        draw.rounded_rectangle(box, 28, fill=fill, outline=outline, width=3)
        x0 = box[0] + 28
        draw.text((x0, 222), title, fill=tone, font=font(40, bold=True))
        draw.text((x0, 286), accent, fill=tone, font=font(35, bold=True))
        draw.text((x0, 372), desc, fill="#5F6870", font=font(27))

    labels = ["1", "&", "2", "&", "3", "&", "4", "&"]
    colors = ["#C68445", "#E6ECF4", "#5A87BA", "#C68445", "#5A87BA", "#E6ECF4", "#C68445", "#5A87BA"]
    states = ["lead", "", "push", "lead", "push", "", "lead", "push"]
    start_x = 144
    for idx, label in enumerate(labels):
        x = start_x + idx * 166
        draw_hit(draw, x, 746, label, colors[idx], states[idx], size=24 if label == "&" else 26)

    draw_hit(draw, 1218, 672, "E", "#5A87BA", "RH", size=24)
    draw_hit(draw, 1360, 672, "E-B", "#5A87BA", "RH", size=18)
    draw_hit(draw, 1218, 828, "Am9", "#4F8A66", "LH", size=20)
    draw_hit(draw, 1360, 828, "G13", "#4F8A66", "LH", size=20)

    draw.text((112, 890), "右手口令：打 - 空 - 推 - 打 - 推 - 空 - 打 - 推", fill="#BA7A37", font=font(25, bold=True))
    draw.text((760, 890), "左手：A-C-E-G 低音循环，始终稳，别和右手抢前冲感", fill="#4F8265", font=font(25, bold=True))

    draw.rounded_rectangle((92, 940, 1464, 984), 18, fill="#FFFDF9", outline="#D5CBBE", width=2)
    draw.text(
        (108, 950),
        "钢琴练法：先让右手的 Mozambique bell 自己形成前冲感，再加入左手 tumbao。听起来应比 campana 更有“往下一拍扑过去”的力量。",
        fill="#5F564B",
        font=font(20, bold=True),
    )

    img.save(ASSET_DIR / "piano-mozambique-bell-pattern.png")


def save_guitar_chart():
    img = Image.new("RGB", (1560, 1080), "#EDF3F6")
    draw = ImageDraw.Draw(img)
    draw.text((58, 40), "吉他图：用高位切分把 Mozambique Bell 弹出推动力", fill="#173039", font=font(52, bold=True))
    draw.text(
        (58, 104),
        "吉他上可以把 Mozambique bell 理解成更主动、更连续的高位切分层。闷音维持八分脉搏，亮和弦专门负责把 bell 的推力打出来。",
        fill="#4D636C",
        font=font(26),
    )

    draw.rounded_rectangle((86, 166, 1474, 334), 26, fill="#FFFDF9", outline="#C4D0D6", width=3)
    draw.text((114, 204), "入门循环：| Am9 x C6/9 x | D9 x G13 x |。重点不在扫满，而在让每次亮点都像把乐队往前推半步。", fill="#223943", font=font(26, bold=True))
    draw.text((114, 260), "如果每个亮点都拖长，Mozambique 的组织感会立刻变成普通 comping。", fill="#516771", font=font(23))

    positions = [88, 402, 716, 1030]
    grids = [
        ("Am9", "5 7 5 5 5 7", [(1, 0, "1"), (3, 1, "3"), (1, 2, "1"), (1, 3, "1"), (1, 4, "1"), (3, 5, "4")], {}, "第一拍像起跑点，亮但必须短。", "#2F8B61"),
        ("C6/9", "x 3 2 2 3 3", [(3, 1, "3"), (2, 2, "1"), (2, 3, "1"), (3, 4, "3"), (3, 5, "4")], {0: "X"}, "第二个亮点是“推”，不是休息。", "#C97B3F"),
        ("D9", "x 5 4 5 5 x", [(1, 1, "1"), (1, 2, "2"), (1, 3, "3"), (1, 4, "4")], {0: "X", 5: "X"}, "后半段再提一次，句子会更像滚动前冲。", "#5C7DB8"),
        ("G13", "3 x 3 4 5 5", [(1, 0, "1"), (1, 2, "2"), (2, 3, "3"), (3, 4, "4"), (3, 5, "4")], {1: "X"}, "尾部亮点负责把下一轮门打开。", "#A15B6B"),
    ]
    for x, (title, subtitle, dots, top, footnote, color) in zip(positions, grids):
        draw_chord_grid(draw, x, 418, title, subtitle, dots, top, footnote, color)

    draw.rounded_rectangle((86, 932, 1474, 1028), 24, fill="#FFFAF4", outline="#C9D3D8", width=3)
    draw.text(
        (110, 960),
        "右手口令：下 - 空 - 上 - 下 - 上 - 空 - 下 - 上。先保证手一直走，再把 Mozambique 的亮点做成短、亮、推的高位切分。",
        fill="#4D5F68",
        font=font(24, bold=True),
    )

    img.save(ASSET_DIR / "guitar-mozambique-bell-pattern.png")


def save_structure_chart():
    img = Image.new("RGB", (1500, 980), "#F8F6F1")
    draw = ImageDraw.Draw(img)
    draw.text((56, 40), "结构图：Mozambique Bell Pattern", fill="#2D261D", font=font(50, bold=True))
    draw.text(
        (56, 104),
        "Mozambique bell 可以看成 bell 线继续向前推进的一步：不只点外框，还把更强的句法推动和组织感挂在高频层上。",
        fill="#655A4E",
        font=font(27),
    )

    lane_top = 220
    lane_left = 96
    cell_w = 150
    lane_h = 132
    row_gap = 54
    accent_fill = "#D9803D"
    support_fill = "#7A90B8"
    base_fill = "#E6ECF4"

    rows = [
        ("bell 落点", ["1", "&", "2", "&", "3", "&", "4", "&"], [0, 3, 6], [2, 4, 7], "主拍像立柱，附加落点连续往前推，所以它比 campana 更像主动组织 groove。"),
        ("身体动作", ["下", "留", "上", "下", "上", "留", "下", "上"], [0, 3, 6], [2, 4, 7], "动作不能断，尤其在附加落点上要感觉像把身体往前提一下。"),
        ("听感对比", ["框", "留", "推", "框", "推", "留", "框", "推"], [0, 3, 6], [2, 4, 7], "campana 更像提示外框，Mozambique 更像外框里每次都带一点推进命令。"),
    ]

    for row_idx, (label, cells, accents, supports, desc) in enumerate(rows):
        y = lane_top + row_idx * (lane_h + row_gap)
        draw.text((lane_left, y - 52), label, fill="#3F3428", font=font(31, bold=True))
        for i, cell in enumerate(cells):
            x0 = lane_left + i * cell_w
            x1 = x0 + cell_w - 14
            if i in accents:
                fill = accent_fill
                outline = "#B86930"
                txt = "#FFFFFF"
            elif i in supports:
                fill = support_fill
                outline = "#5E759E"
                txt = "#FFFFFF"
            else:
                fill = base_fill
                outline = "#B7C2D0"
                txt = "#4A5766"
            draw.rounded_rectangle((x0, y, x1, y + lane_h), 22, fill=fill, outline=outline, width=3)
            center_text(draw, (x0, y + 16, x1, y + 68), cell, txt, font(24, bold=True))
            state = "lead" if i in accents else ("push" if i in supports else "space")
            center_text(draw, (x0, y + 70, x1, y + 118), state, txt if i in accents or i in supports else "#667485", font(19, bold=i in accents or i in supports))
        draw.text((lane_left, y + 150), desc, fill="#5F564B", font=font(22))

    draw.rounded_rectangle((96, 806, 1404, 922), 24, fill="#FFFAF0", outline="#D0B892", width=3)
    draw.text((120, 840), "听感重点：Mozambique Bell Pattern 的核心，是把 bell 从“提示层”推进到“组织前冲”的时间线。", fill="#5F5547", font=font(24, bold=True))

    img.save(ASSET_DIR / "mozambique-bell-pattern-structure.png")


if __name__ == "__main__":
    save_piano_chart()
    save_guitar_chart()
    save_structure_chart()
