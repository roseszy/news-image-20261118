#!/usr/bin/env python3
"""Draw entry.png for news-image-20261118: the world's news of Wednesday
18 November 2026 in one 1024x1024 image.

Layout: a navy masthead naming the date, then six panels (2 x 3), each with
a flat illustration, a kicker, a short title and a one- or two-line caption.
Everything is drawn programmatically with PIL + DejaVu so every letter is
crisp. Deterministic: fixed seed, no time, no network.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
GOLD = (252, 163, 17)
INK = (24, 24, 24)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (216, 210, 196)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def starburst(d, cx, cy, r1, r2, points, color):
    import math
    pts = []
    for i in range(points * 2):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)


def stars(d, box, n, seed=7):
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rng.randint(x0, x1)
        y = rng.randint(y0, y1)
        r = rng.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))


# ---------------------------------------------------------------- panels
def panel_summit(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 233, 235))  # pale sky
    d.ellipse([x1 - 70, y0 + 12, x1 - 26, y0 + 56], fill=(252, 200, 90))
    # skyline
    for bx, bw, bh in [(0, 62, 78), (66, 44, 104), (114, 70, 66), (188, 40, 92)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(38, 62, 92))
        for wy in range(y1 - bh + 10, y1 - 8, 14):
            for wx in range(x0 + bx + 8, x0 + bx + bw - 8, 14):
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(252, 200, 90))
    # three flags on poles
    flags = [(255, 222, 89), (255, 255, 255), (200, 60, 60)]
    # China (red), Russia (white/blue/red), USA (stripes) — simplified
    for i, fx in enumerate([x0 + 250, x0 + 310, x0 + 370]):
        d.line([fx, y0 + 18, fx, y1 - 30], fill=(60, 60, 60), width=3)
    d.rectangle([x0 + 250, y0 + 18, x0 + 292, y0 + 46], fill=(222, 41, 16))
    for sx, sy in [(x0 + 256, y0 + 24), (x0 + 266, y0 + 22), (x0 + 274, y0 + 28),
                   (x0 + 260, y0 + 34), (x0 + 270, y0 + 36)]:
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 222, 89))
    d.rectangle([x0 + 310, y0 + 18, x0 + 352, y0 + 27], fill=(255, 255, 255))
    d.rectangle([x0 + 310, y0 + 27, x0 + 352, y0 + 36], fill=(0, 57, 166))
    d.rectangle([x0 + 310, y0 + 36, x0 + 352, y0 + 46], fill=(213, 0, 50))
    for k in range(4):
        d.rectangle([x0 + 370, y0 + 18 + k * 7, x0 + 412, y0 + 24 + k * 7],
                    fill=(178, 34, 52) if k % 2 == 0 else (255, 255, 255))
    d.rectangle([x0 + 370, y0 + 18, x0 + 388, y0 + 32], fill=(60, 59, 110))


def panel_gulf(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 222, 196))  # desert sky
    d.rectangle([x0, y0 + 96, x1, y1], fill=(28, 96, 140))  # sea
    for wx in range(x0 + 8, x1 - 8, 46):
        d.arc([wx, y0 + 108, wx + 34, y0 + 124], 0, 180, fill=(255, 255, 255), width=3)
    # island with launch site
    d.polygon([(x0 + 120, y1), (x0 + 150, y0 + 84), (x0 + 300, y0 + 84),
               (x0 + 330, y1)], fill=(94, 74, 52))
    d.rectangle([x0 + 205, y0 + 52, x0 + 245, y0 + 84], fill=(60, 60, 60))
    d.line([x0 + 225, y0 + 52, x0 + 225, y0 + 30], fill=(60, 60, 60), width=4)
    # explosion
    starburst(d, x0 + 225, y0 + 26, 30, 13, 8, (255, 140, 0))
    starburst(d, x0 + 225, y0 + 26, 18, 8, 8, (255, 220, 60))
    # smoke puffs
    for sx, sy, sr in [(x0 + 190, y0 + 44, 10), (x0 + 255, y0 + 38, 12),
                       (x0 + 222, y0 + 58, 9)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))
    # drones
    for dx, dy in [(x0 + 40, y0 + 30), (x0 + 80, y0 + 52), (x0 + 360, y0 + 26)]:
        d.polygon([(dx, dy - 6), (dx + 12, dy), (dx, dy + 6), (dx - 12, dy)],
                  fill=(40, 40, 40))
        d.line([dx - 26, dy, dx - 14, dy], fill=(40, 40, 40), width=2)
    # small ship
    d.polygon([(x0 + 380, y1 - 26), (x0 + 420, y1 - 26), (x0 + 412, y1 - 12),
               (x0 + 388, y1 - 12)], fill=(30, 30, 30))
    d.rectangle([x0 + 394, y1 - 40, x0 + 406, y1 - 26], fill=(30, 30, 30))


def panel_kerch(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(205, 225, 235))  # sky
    d.rectangle([x0, y0 + 100, x1, y1], fill=(32, 110, 160))  # strait
    for wx in range(x0 + 6, x1 - 6, 52):
        d.arc([wx, y0 + 116, wx + 38, y0 + 132], 0, 180, fill=(255, 255, 255), width=3)
    # bridge deck, two standing ends, gap in the middle
    d.rectangle([x0, y0 + 66, x0 + 170, y0 + 82], fill=(70, 70, 78))
    d.rectangle([x0 + 300, y0 + 66, x1, y0 + 82], fill=(70, 70, 78))
    for px in [x0 + 40, x0 + 120, x0 + 340, x0 + 420]:
        d.rectangle([px, y0 + 30, px + 10, y0 + 66], fill=(70, 70, 78))
    d.arc([x0 + 20, y0 + 8, x0 + 160, y0 + 80], 180, 360, fill=(70, 70, 78), width=6)
    d.arc([x0 + 310, y0 + 8, x0 + 450, y0 + 80], 180, 360, fill=(70, 70, 78), width=6)
    # fallen deck segment in the water, tilted, with splash
    d.polygon([(x0 + 185, y0 + 118), (x0 + 280, y0 + 104),
               (x0 + 288, y0 + 122), (x0 + 193, y0 + 136)], fill=(50, 50, 58))
    d.polygon([(x0 + 210, y0 + 128), (x0 + 258, y0 + 120),
               (x0 + 262, y0 + 134), (x0 + 214, y0 + 142)], fill=(70, 70, 78))
    # splash
    for sx, sy in [(x0 + 200, y0 + 128), (x0 + 235, y0 + 138), (x0 + 268, y0 + 126)]:
        d.line([sx - 8, sy, sx + 8, sy], fill=(255, 255, 255), width=3)
        d.line([sx, sy - 8, sx, sy + 2], fill=(255, 255, 255), width=3)


def panel_senate(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(235, 228, 210))  # parchment
    # Capitol dome
    d.rectangle([x0 + 30, y0 + 96, x0 + 190, y1], fill=(250, 250, 248))
    d.pieslice([x0 + 70, y0 + 40, x0 + 150, y0 + 110], 180, 360, fill=(250, 250, 248))
    d.rectangle([x0 + 106, y0 + 22, x0 + 114, y0 + 44], fill=(250, 250, 248))
    d.line([x0 + 110, y0 + 10, x0 + 110, y0 + 24], fill=(120, 120, 120), width=2)
    d.polygon([(x0 + 110, y0 + 10), (x0 + 126, y0 + 15), (x0 + 110, y0 + 20)],
              fill=(178, 34, 52))
    for cx in range(x0 + 44, x0 + 180, 22):
        d.rectangle([cx, y0 + 110, cx + 8, y1 - 6], fill=(200, 196, 186))
    # ballot box with check
    d.rectangle([x0 + 250, y0 + 84, x0 + 400, y1 - 6], fill=(38, 62, 92))
    d.rectangle([x0 + 290, y0 + 72, x0 + 360, y0 + 86], fill=(24, 44, 70))
    d.line([x0 + 292, y0 + 118, x0 + 318, y0 + 142, x0 + 366, y0 + 92],
           fill=(120, 200, 90), width=10, joint="curve")
    # stars
    for sx, sy in [(x0 + 220, y0 + 30), (x0 + 420, y0 + 40), (x0 + 250, y0 + 150)]:
        starburst(d, sx, sy, 9, 4, 5, (252, 163, 17))


def panel_ebola(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(250, 232, 222))  # pale red
    # virus: spiky circle
    cx, cy, r = x0 + 130, y0 + 78, 48
    for k in range(12):
        import math
        a = math.pi * 2 * k / 12
        x2, y2 = cx + (r + 20) * math.cos(a), cy + (r + 20) * math.sin(a)
        d.line([cx + r * math.cos(a), cy + r * math.sin(a), x2, y2],
               fill=(150, 40, 40), width=5)
        d.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(150, 40, 40))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(185, 55, 55))
    for ex, ey in [(cx - 20, cy - 14), (cx + 18, cy - 20), (cx + 8, cy + 18),
                   (cx - 8, cy + 26)]:
        d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(140, 30, 30))
    # medical cross badge
    bx, by = x0 + 320, y0 + 40
    d.ellipse([bx - 46, by - 46, bx + 46, by + 46], fill=(255, 255, 255))
    d.rectangle([bx - 10, by - 30, bx + 10, by + 30], fill=(185, 55, 55))
    d.rectangle([bx - 30, by - 10, bx + 30, by + 10], fill=(185, 55, 55))
    # small dots (cases) — confined to the illustration area
    rng = random.Random(11)
    for _ in range(14):
        dx = rng.randint(x0 + 250, x1 - 20)
        dy = rng.randint(y0 + 108, y0 + 146)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(185, 55, 55))


def panel_voyager(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(10, 14, 34))  # space
    stars(d, box, 70, seed=21)
    # Earth, bottom left
    d.ellipse([x0 + 18, y1 - 66, x0 + 86, y1 + 2], fill=(46, 130, 200))
    d.ellipse([x0 + 30, y1 - 52, x0 + 56, y1 - 30], fill=(80, 180, 100))
    d.ellipse([x0 + 52, y1 - 34, x0 + 74, y1 - 14], fill=(80, 180, 100))
    # dashed trajectory
    for t in range(0, 21):
        fx = x0 + 86 + t * 14
        fy = (y1 - 34) - t * 5
        d.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=(252, 200, 90))
    # Voyager craft: gold dish + body + boom
    cx, cy = x0 + 380, y0 + 52
    d.line([cx - 70, cy + 44, cx + 10, cy + 10], fill=(200, 200, 200), width=4)
    d.ellipse([cx - 34, cy - 30, cx + 34, cy + 30], fill=(230, 200, 120))
    d.ellipse([cx - 22, cy - 18, cx + 22, cy + 18], fill=(200, 170, 90))
    d.rectangle([cx - 58, cy - 8, cx - 30, cy + 8], fill=(180, 180, 180))
    d.line([cx - 58, cy, cx - 96, cy - 22], fill=(180, 180, 180), width=3)
    d.ellipse([cx - 104, cy - 30, cx - 88, cy - 14], fill=(240, 240, 240))


PANELS = [
    ("DIPLOMACY · CHINA", "SHENZHEN SUMMIT", "Xi meets Putin in Shenzhen; a first trilateral with Trump follows on Thursday.", (15, 118, 110), panel_summit),
    ("WAR · THE GULF", "GULF STRIKES", "Iran fires drones at Kuwait and Bahrain after the US strikes Qeshm Island.", (185, 28, 28), panel_gulf),
    ("WAR · UKRAINE", "KERCH BRIDGE FALLS", "Its road arch falls into the strait after two nights of Ukrainian strikes.", (29, 78, 216), panel_kerch),
    ("POLITICS · USA", "ALASKA FLIPS SENATE", "Peltola beats Sullivan; Democrats take a 56–44 Senate majority.", (124, 58, 237), panel_senate),
    ("HEALTH · CONGO", "EBOLA SURGES", "The outbreak passes 11,000 cases, with 5,400 dead, the UN says.", (180, 83, 9), panel_ebola),
    ("SPACE · NASA", "VOYAGER 1, ONE LIGHT-DAY", "The first human-made object a full day's light from Earth.", (15, 23, 42), panel_voyager),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 124], fill=NAVY)
    d.rectangle([0, 124, W, 128], fill=GOLD)
    f_small = font(BOLD, 20)
    f_date = font(BOLD, 58)
    f_sub = font(REG, 18)
    d.text((W // 2, 12), "WEDNESDAY", font=f_small, fill=GOLD, anchor="ma")
    d.text((W // 2, 34), "18 NOVEMBER 2026", font=f_date, fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 102), "THE WORLD IN ONE DAY", font=f_sub, fill=(200, 210, 225), anchor="ma")

    # ---- panels, 2 x 3
    pw, ph, gap, mx = 494, 272, 12, 12
    top = 138
    f_kick = font(BOLD, 15)
    f_title = font(BOLD, 27)
    f_cap = font(REG, 19)
    for i, (kicker, title, caption, accent, draw_fn) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = mx + col * (pw + gap)
        y0 = top + row * (ph + 8)
        x1, y1 = x0 + pw, y0 + ph
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=CARD, outline=LINE, width=2)
        d.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=accent)
        d.rectangle([x0, y0 + 4, x1, y0 + 8], fill=accent)
        draw_fn(d, (x0 + 14, y0 + 14, x1 - 14, y0 + 152))
        d.text((x0 + 16, y0 + 160), kicker, font=f_kick, fill=accent)
        d.text((x0 + 16, y0 + 180), title, font=f_title, fill=INK)
        lines = wrap(d, caption, f_cap, pw - 32)
        for j, ln in enumerate(lines[:2]):
            d.text((x0 + 16, y0 + 214 + j * 24), ln, font=f_cap, fill=MUTED)

    # ---- footer
    f_foot = font(REG, 16)
    d.text((W // 2, 982), "Sources: Reuters · AP · AFP · BBC · NASA/JPL · UN · PAHO",
           font=f_foot, fill=MUTED, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
