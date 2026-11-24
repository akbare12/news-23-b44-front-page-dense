#!/usr/bin/env python3
"""news-23 b44 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PAPER = (255, 255, 255)
GOLD = (255, 191, 0)
RED = (192, 57, 43)
DARKRED = (160, 30, 20)
NAVY = (31, 56, 100)
TEAL = (0, 128, 128)
GREEN = (30, 132, 73)
PURPLE = (108, 52, 131)
BROWN = (125, 102, 8)
GREY = (90, 90, 90)
LGREY = (230, 230, 230)
CREAM = (250, 243, 224)
SKY = (214, 234, 248)
LEAF = (169, 209, 142)
DARKNAVY = (10, 25, 60)

def font(name, size):
    try:
        if name == "b":
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()

def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trunc(d, text, fnt, maxw, ell="..."):
    if d.textlength(text, font=fnt) <= maxw:
        return text
    while text and d.textlength(text + ell, font=fnt) > maxw:
        text = text[:-1]
    return text + ell

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 54], fill=BLACK)
d.text((10, 6), "THE WORLD TODAY", font=font("b", 42), fill=WHITE)
dt = "MONDAY 23 NOVEMBER 2026"
d.text((W - 10 - d.textlength(dt, font=font("b", 20)), 16), dt, font=font("b", 20), fill=GOLD)

# ---------- kicker ----------
kick = "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B"
d.text((10, 57), kick, font=font("b", 13), fill=RED)

# ---------- number strip ----------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", GREEN), ("10T won", "SEOUL STABILISATION FUND", BROWN),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES IN A WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", NAVY), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", BROWN),
    ("$107.3B", "ANTHROPIC IPO — LARGEST", PURPLE),
]
colw = (W - 20) // 5
for i, (num, lab, col) in enumerate(nums):
    cx = 10 + (i % 5) * colw
    cy = 74 + (i // 5) * 34
    d.text((cx, cy), num, font=font("b", 22), fill=col)
    d.text((cx, cy + 23), lab, font=font("b", 8), fill=BLACK)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", TEAL, 290), ("AMERICAS 8", NAVY, 290),
           ("MIDDLE EAST 6", BROWN, 190), ("EUROPE 5", PURPLE, 116),
           ("AFRICA 3", RED, 66), ("WORLD 2", GREY, 72)]
x = 0
for name, col, wdt in regions:
    d.rectangle([x, 142, x + wdt, 158], fill=col)
    tw = d.textlength(name, font=font("b", 9))
    d.text((x + (wdt - tw) / 2, 145), name, font=font("b", 9), fill=WHITE)
    x += wdt

# ---------- UTC strip ----------
d.rectangle([0, 158, W, 174], fill=NAVY)
d.text((10, 160), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 IPO $97.17",
       font=font("b", 10), fill=WHITE)
ap = "~ APPROX"
d.text((W - 10 - d.textlength(ap, font=font("b", 10)), 160), ap, font=font("b", 10), fill=(180, 200, 230))

# ---------- hero scenes ----------
hx = [0, 342, 684]
hw = [342, 342, 340]
# scene 1: Kospi chart
x0, y0, wdt = hx[0], 174, hw[0]
d.rectangle([x0, y0, x0 + wdt, 306], fill=DARKNAVY)
d.text((x0 + 8, y0 + 4), "-3.3%", font=font("b", 30), fill=(255, 90, 70))
pts = [(x0 + 12 + i * 32, y0 + 62 + v) for i, v in enumerate([0, 14, 8, 26, 18, 40, 30, 48, 38, 52])]
d.line(pts, fill=(255, 90, 70), width=2)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD)
import random
random.seed(44)
for bx in range(x0 + 8, x0 + wdt - 10, 26):
    bh = random.randint(18, 52)
    d.rectangle([bx, 306 - bh, bx + 18, 306], fill=(24, 48, 90))
    for wy in range(306 - bh + 4, 302, 10):
        for wx in (bx + 4, bx + 11):
            if random.random() < 0.6:
                d.rectangle([wx, wy, wx + 3, wy + 3], fill=GOLD)
# scene 2: Guterres
x0 = hx[1]
d.rectangle([x0, y0, x0 + hw[1], 306], fill=TEAL)
d.text((x0 + 10, y0 + 8), "150 DELEGATES", font=font("b", 30), fill=GOLD)
d.text((x0 + 10, y0 + 42), "BACK A RISK", font=font("b", 30), fill=WHITE)
d.text((x0 + 10, y0 + 76), "FRAMEWORK", font=font("b", 30), fill=WHITE)
# globe bottom-right
gx, gy, gr = x0 + hw[1] - 34, 306 - 34, 16
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(180, 220, 220), outline=WHITE, width=2)
d.ellipse([gx - 8, gy - gr, gx + 8, gy + gr], outline=(90, 140, 140), width=1)
d.line([gx - gr, gy, gx + gr, gy], fill=(90, 140, 140), width=1)
# scene 3: power bars
x0 = hx[2]
d.rectangle([x0, y0, x0 + hw[2], 306], fill=CREAM)
d.text((x0 + 10, y0 + 4), "NARROWEST SINCE 2018", font=font("b", 11), fill=BLACK)
g5 = "GAP 5.3"
d.text((x0 + hw[2] - 10 - d.textlength(g5, font=font("b", 11)), y0 + 4), g5, font=font("b", 11), fill=BROWN)
bars = [("78.9", "US", NAVY, 88), ("73.6", "CHINA", RED, 82), ("40.5", "INDIA", (200, 160, 0), 46)]
bx = x0 + 22
base = 306 - 24
for val, lab, col, bh in bars:
    d.rectangle([bx, base - bh, bx + 78, base], fill=col)
    d.text((bx + 20, base - bh + 8), val, font=font("b", 16), fill=WHITE)
    d.text((bx + 26, base - 20), lab, font=font("b", 11), fill=WHITE)
    bx += 96

# scene caption bars
caps = ["KOSPI 4,708.54   ·   -161 PTS", "UN  ·  BRIDGETOWN", "ASIA POWER INDEX 2026"]
for i, cap in enumerate(caps):
    d.rectangle([hx[i], 306, hx[i] + hw[i], 322], fill=BLACK)
    d.text((hx[i] + 8, 309), cap, font=font("b", 11), fill=WHITE)

# hero text
heroes = [
    ("1", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
     "KOREA EXCHANGE", "REPORTED"),
    ("2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS", "REPORTED"),
    ("3", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED"),
]
for i, (num, head, body, src, chip) in enumerate(heroes):
    x0 = hx[i] + 8
    wdt = hw[i] - 16
    d.ellipse([x0, 328, x0 + 18, 346], fill=RED)
    d.text((x0 + 6, 328), num, font=font("b", 12), fill=WHITE)
    hl = wrap(d, head, font("b", 14), wdt - 22)
    yy = 328
    for ln in hl[:2]:
        d.text((x0 + 24, yy), ln, font=font("b", 14), fill=BLACK)
        yy += 17
    by = 328 + 17 * len(hl[:2]) + 2
    bl = wrap(d, body, font("r", 10), wdt)
    for ln in bl[:2]:
        d.text((x0, by), ln, font=font("r", 10), fill=BLACK)
        by += 13
    # source + chip row (fixed row under text)
    d.text((x0, 394), src, font=font("r", 9), fill=GREY)
    chw = d.textlength(chip, font=font("b", 8)) + 8
    cx = hx[i] + hw[i] - 10 - chw
    d.rectangle([cx, 392, cx + chw, 404], fill=NAVY if chip == "REPORTED" else RED)
    d.text((cx + 4, 394), chip, font=font("b", 8), fill=WHITE)

# ---------- MORE bar ----------
d.rectangle([0, 412, W, 428], fill=BLACK)
d.text((10, 415), "MORE OF THE DAY  —  10 STORIES", font=font("b", 11), fill=WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED"),
    ("FBI", PURPLE, "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED"),
    ("WHITE HOUSE", BROWN, "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", GREEN, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED"),
    ("TECH", NAVY, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", BROWN, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", GREY, "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", "CLAIM"),
]
cw = (W - 20) // 5
for i, (cat, col, head, body, src, chip) in enumerate(cards):
    cx = 10 + (i % 5) * cw
    cy = 428 + (i // 5) * 74
    # tag bar
    d.rectangle([cx, cy + 4, cx + cw - 8, cy + 16], fill=col)
    d.text((cx + 3, cy + 5), cat, font=font("b", 8), fill=WHITE)
    n = str(i + 1)
    d.text((cx + cw - 8 - d.textlength(n, font=font("b", 9)) - 3, cy + 5), n, font=font("b", 9), fill=WHITE)
    hl = wrap(d, head, font("b", 10), cw - 10)
    yy = cy + 19
    for ln in hl[:2]:
        d.text((cx, yy), ln, font=font("b", 10), fill=BLACK)
        yy += 12
    # body on its own line, truncated clear of the chip zone
    d.text((cx, yy + 1), trunc(d, body, font("r", 9), cw - 10), font=font("r", 9), fill=BLACK)
    # source + chip row at bottom of card
    sy = cy + 60
    d.text((cx, sy), src, font=font("r", 8), fill=GREY)
    chw = d.textlength(chip, font=font("b", 8)) + 8
    chx = cx + cw - 8 - chw
    d.rectangle([chx, sy - 1, chx + chw, sy + 11], fill=NAVY if chip == "REPORTED" else RED)
    d.text((chx + 4, sy), chip, font=font("b", 8), fill=WHITE)

# ---------- map + ALSO header ----------
d.rectangle([0, 576, W, 592], fill=BLACK)
d.text((10, 579), "WHERE IT HAPPENED", font=font("b", 11), fill=WHITE)
d.text((352, 579), "ALSO ON MONDAY", font=font("b", 11), fill=WHITE)

# map
mx, my, mw, mh = 10, 592, 330, 208
d.rectangle([mx, my, mx + mw, my + mh], fill=SKY)
for gx in range(mx, mx + mw, 16):
    d.line([gx, my, gx, my + mh], fill=(190, 215, 235), width=1)
for gy in range(my, my + mh, 16):
    d.line([mx, gy, mx + mw, gy], fill=(190, 215, 235), width=1)
for (ex, ey, ew, eh) in [(20, 610, 120, 90), (150, 620, 90, 70), (250, 605, 70, 60),
                          (60, 720, 80, 50), (180, 730, 60, 40), (280, 740, 40, 30)]:
    d.ellipse([ex, ey, ex + ew, ey + eh], fill=LEAF)
pins = [(45, 640, 1), (95, 735, 2), (70, 665, 3), (60, 690, 4), (95, 660, 5),
        (185, 660, 6), (55, 625, 7), (45, 685, 8), (80, 695, 9), (105, 720, 10),
        (175, 635, 11), (195, 650, 12), (225, 625, 13)]
for px, py, pn in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    d.text((px - 3 if pn < 10 else px - 6, py - 6), str(pn), font=font("b", 9), fill=WHITE)
# map legend (3 short lines, inside map box)
leg = ["Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing",
       "4 Washington · 5 New York · 6 Tehran · 7 Chicago",
       "8 San Francisco · 9 Denver · 10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow"]
ly = my + mh - 34
for ln in leg:
    d.text((mx + 4, ly), ln, font=font("r", 8), fill=BLACK)
    ly += 11

# ALSO list
also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules", "31. Seoul readies 10T-won fund",
]
ax = 352
for i, item in enumerate(also):
    col = i % 2
    ay = 596 + (i // 2) * 21
    d.text((ax + col * 330, ay), item, font=font("r", 10), fill=BLACK)

# ---------- DATE CHECK ----------
d.rectangle([10, 800, W - 10, 888], outline=RED, width=2)
d.text((16, 804), "DATE CHECK", font=font("b", 12), fill=RED)
rt = "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY"
d.text((W - 16 - d.textlength(rt, font=font("b", 9)), 806), rt, font=font("b", 9), fill=RED)
left = "LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)"
for j, ln in enumerate(wrap(d, left, font("r", 10), W - 32)):
    d.text((16, 822 + j * 13), ln, font=font("r", 10), fill=BLACK)
ny = "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff"
d.text((16, 862), ny, font=font("b", 10), fill=BLACK)

# ---------- footer sources ----------
d.text((10, 894), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
       font=font("r", 9), fill=GREY)
d.text((10, 908), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing",
       font=font("r", 9), fill=GREY)
d.text((10, 922), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=font("r", 9), fill=GREY)

# ---------- bottom bar ----------
d.rectangle([0, 960, W, 1024], fill=BLACK)
bb = "THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions"
d.text(((W - d.textlength(bb, font=font("b", 15))) / 2, 984), bb, font=font("b", 15), fill=GOLD)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
