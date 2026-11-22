"""v0.5 shareable score card frame (600x800) + per-stage tints + share icon.
Code draws ghost/text into the safe areas listed in scorecard-layout.json (also ASSETS.md §12).
Writes SVGs into assets/, exports png/1x + png/2x, writes scorecard-layout.json."""
import os, sys, json, random, cairosvg
sys.path.insert(0, os.path.dirname(__file__))
from build_v05 import svg, inner, star5
from build_extras import bat_svg, pumpkin_svg, sweet_wrapped, sweet_lollipop, sweet_macaron, sparkle
OUT = os.path.join(os.path.dirname(__file__), "..")
SKY = json.load(open(os.path.join(OUT, "sky-palettes.json")))
STAGES = ["graveyard", "church", "countryside", "schools", "city", "space", "void"]
W, H = 600, 800
PANEL = (36, 36, 528, 688)          # cream card, constant across tints -> text colours constant
INK, INK2, ACC = "#4A3358", "#7A5A9E", "#C9798F"
# safe areas: [x, y, w, h], align, baseline, max font px, colour
SAFE = {
  "ghost":  dict(rect=[200, 66, 200, 200], note="draw ghost sprite centred, e.g. 64px art at 3x = 192px"),
  "stage":  dict(rect=[110, 282, 380, 40], align="center", baseline="middle", maxFont=28, color=INK2, weight="bold"),
  "score":  dict(rect=[80, 330, 440, 140], align="center", baseline="middle", maxFont=120, color=INK, weight="900",
                 note="optional 4px stroke #FFFFFF behind fill for extra pop"),
  "best":   dict(rect=[130, 480, 340, 40], align="center", baseline="middle", maxFont=28, color=ACC, weight="bold"),
  "player": dict(rect=[120, 546, 360, 56], align="center", baseline="middle", maxFont=34, color=INK, weight="bold",
                 note="sits on a lilac pill; shrink-to-fit"),
  "url":    dict(rect=[90, 742, 420, 36], align="center", baseline="middle", maxFont=22, color=INK, weight="bold",
                 note="cream ribbon at the bottom, outside the card"),
}
def mix(a, b, t):
    a = [int(a[i:i+2], 16) for i in (1, 3, 5)]; b = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * t) for x, y in zip(a, b))
def put(s, x, y, sc=1.0, rot=0):
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">{inner(s)}</g>'

def frame(stage=None):
    if stage: top, bot = SKY[stage]["top"], SKY[stage]["bottom"]
    else: top, bot = "#282142", "#4E3E6E"
    bord = mix(bot, "#FFFFFF", 0.55); bord2 = mix(bot, "#FFFFFF", 0.3)
    g = [f'<defs><linearGradient id="sc_bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient>'
         f'<radialGradient id="sc_glow" cx="0.5" cy="0.3" r="0.6"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sc_bg)"/>']
    rnd = random.Random(7)
    for _ in range(40):  # tiny background stars
        x, y = rnd.uniform(4, W-4), rnd.uniform(4, H-4)
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(0.8, 2):.1f}" fill="#FFF4D6" opacity="{rnd.uniform(0.4, 0.9):.2f}"/>')
    x, y, w, h = PANEL
    # scalloped border: bumps around the card
    for i in range(14):
        for yy in (y, y + h):
            g.append(f'<circle cx="{x + 18 + i*(w-36)/13:.1f}" cy="{yy}" r="14" fill="{bord}" stroke="#6B4E7A" stroke-width="2.4"/>')
    for i in range(18):
        for xx in (x, x + w):
            g.append(f'<circle cx="{xx}" cy="{y + 18 + i*(h-36)/17:.1f}" r="14" fill="{bord}" stroke="#6B4E7A" stroke-width="2.4"/>')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="{bord}"/>')
    g.append(f'<rect x="{x+12}" y="{y+12}" width="{w-24}" height="{h-24}" rx="26" fill="#FFF8F0" stroke="#6B4E7A" stroke-width="2.6"/>')
    g.append(f'<rect x="{x+20}" y="{y+20}" width="{w-40}" height="{h-40}" rx="20" fill="none" stroke="{bord2}" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>')
    # ghost halo
    g.append('<circle cx="300" cy="166" r="118" fill="url(#sc_glow)"/><ellipse cx="300" cy="166" rx="104" ry="104" fill="#F3ECFB" opacity="0.7"/>')
    g.append('<ellipse cx="300" cy="258" rx="70" ry="8" fill="#E6DDF7" opacity="0.8"/>')
    # divider hearts/dots under score
    for i, dx in enumerate((-60, -30, 0, 30, 60)):
        c = ("#FFB3CB", "#AEE3C6", "#FFE08A", "#AEE3C6", "#FFB3CB")[i]
        g.append(f'<circle cx="{300+dx}" cy="532" r="{5 if dx else 7}" fill="{c}" stroke="#6B4E7A" stroke-width="1.4"/>')
    # player pill
    g.append(f'<rect x="110" y="544" width="380" height="60" rx="30" fill="#EDE4FA" stroke="#6B4E7A" stroke-width="2.4"/>')
    # bottom URL ribbon (outside the card)
    g.append(f'<path d="M70,738 L52,760 L70,782 H530 L548,760 L530,738 Z" fill="#FFF8F0" stroke="#6B4E7A" stroke-width="2.6" stroke-linejoin="round"/>')
    g.append(f'<path d="M82,744 H518" stroke="{bord}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>')
    # decorations: corners + edges, away from safe areas
    g.append(put(pumpkin_svg(), 46, 640, 1.9))           # bottom-left
    g.append(put(pumpkin_svg(), 478, 652, 1.6, 6))       # bottom-right
    g.append(put(bat_svg("0"), 40, 52, 1.6, -12))        # top-left
    g.append(put(bat_svg("1"), 480, 70, 1.3, 14))        # top-right
    g.append(put(sweet_lollipop(), 70, 330, 1.3, -18))   # left edge
    g.append(put(sweet_wrapped(), 488, 400, 1.3, 20))    # right edge
    g.append(put(sweet_macaron(), 470, 230, 1.2))
    g.append(put(sweet_wrapped(), 74, 206, 1.1, -30))
    for (sx, sy, r, rot) in ((150, 92, 10, 10), (452, 160, 8, -8), (150, 248, 7, 0), (462, 300, 9, 15), (80, 460, 8, 0), (514, 520, 7, 0), (300, 22, 9, 0)):
        g.append(star5(sx, sy, r, rot=rot))
    for (sx, sy, r) in ((172, 130, 5), (430, 112, 6), (110, 590, 5), (494, 600, 5), (250, 652, 4), (360, 662, 5), (300, 690, 4)):
        g.append(sparkle(sx, sy, r))
    return svg(W, H, "".join(g))

def share_icon(size):
    s = size / 48
    g = [f'<g transform="scale({s})">',
         '<path d="M15,24 L33,13 M15,24 L33,35" stroke="#6B4E7A" stroke-width="3.2" stroke-linecap="round"/>']
    for (x, y, c) in ((14, 24, "#FFB3CB"), (34, 12, "#AEE3C6"), (34, 36, "#FFE08A")):
        g.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{c}" stroke="#6B4E7A" stroke-width="2.4"/>'
                 f'<circle cx="{x-2.6}" cy="{y-2.6}" r="2" fill="#FFF" opacity="0.85"/>')
    g.append('<path d="M11.5,25 Q14,27.4 16.5,25" fill="none" stroke="#4A3358" stroke-width="1.4" stroke-linecap="round"/>')
    g.append(sparkle(43, 5, 3.4))
    g.append('</g>')
    return svg(size, size, "".join(g))

def build():
    F = {"ui-scorecard-frame": frame()}
    for st in STAGES: F[f"ui-scorecard-frame-{st}"] = frame(st)
    for sz in (32, 48): F[f"ui-icon-share-{sz}"] = share_icon(sz)
    return F

if __name__ == "__main__":
    F = build()
    for d in ("png/1x", "png/2x"): os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for k, v in F.items():
        p = os.path.join(OUT, k + ".svg"); open(p, "w").write(v)
        for sc, d in ((1, "png/1x"), (2, "png/2x")):
            cairosvg.svg2png(url=p, write_to=os.path.join(OUT, d, k + ".png"), scale=sc)
    # convenience copies at assets/ root, as Code asked: ui-scorecard-frame*.png (+@2x)
    import shutil
    for k in F:
        if k.startswith("ui-scorecard"):
            shutil.copy(os.path.join(OUT, "png/1x", k + ".png"), os.path.join(OUT, k + ".png"))
            shutil.copy(os.path.join(OUT, "png/2x", k + ".png"), os.path.join(OUT, k + "@2x.png"))
    layout = {"_note": "600x800 canvas coords (multiply by 2 for @2x). rect=[x,y,w,h]. Text colours sit on the constant cream card/ribbon so they read on every stage tint.",
              "canvas": [W, H], "font": "rounded bold (e.g. 'Baloo 2', 'M PLUS Rounded 1c', fallback sans-serif bold)",
              "areas": SAFE}
    json.dump(layout, open(os.path.join(OUT, "scorecard-layout.json"), "w"), indent=2)
    print(len(F), "files")
