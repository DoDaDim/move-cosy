"""Santa's Rocket Run - full stage set (seasonal skin of 'Move Cosy'). Concept folder, NOT wired into the game.
Writes ../stages/{svg,png/1x,png/2x}, ../stages/santa-hitboxes.json, santa-sky-palettes.json, santa-death-map.json,
../stages/previews/santa-preview-<stage>.png + santa-overview.png. Docs: ../SANTA-ASSETS.md.
Run: python3 build_santa_stages.py && python3 check_santa_continuity.py"""
import os, sys, json, math, random, glob
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from santa_lib import *
import santa_lib as SL
from santa_columns import ORDER, TOPS, BOTS, build_columns
from santa_bg import SKY, STARS, bg_parts, band, stars_tile
NAMES = {"lapland": "Lapland", "london": "London", "newyork": "New York", "rio": "Rio", "egypt": "Egypt", "tokyo": "Tokyo", "sydney": "Sydney", "antarctica": "Antarctica", "aurora": "Aurora"}
BAN = {"lapland": ("#C9F0DA", "#9ED8B8", "#3F6A5E"), "london": ("#FFC9D2", "#F29EB0", "#7A3A52"), "newyork": ("#FFE3A0", "#F2C46E", "#7A5A3E"), "rio": ("#C9F0E6", "#FFB6CC", "#5E3E7A"),
       "egypt": ("#FFE6B8", "#F2C88A", "#7A5A3E"), "tokyo": ("#FFD0DA", "#F29EB4", "#6E2E58"), "sydney": ("#C9EEFF", "#9ED8F5", "#2E5E8A"), "antarctica": ("#DDF1FF", "#B9DDF5", "#3E5E8A"), "aurora": ("#D9CCF5", "#9EF0C8", "#4A3E7A")}
MIST_TINT = {"lapland": "#CFF5E4", "london": "#E6DDF7", "newyork": "#FFF0D0", "rio": "#FFD6E6", "egypt": "#FFE3C4", "tokyo": "#FFD6E0", "sydney": "#D6F2FF", "antarctica": "#DDF1FF", "aurora": "#D9CCF5"}
FLOAT = {}
def text2(x, y, t, size, fill, line, sw):  # stroke layer then fill layer (cairosvg ignores paint-order)
    a = f'x="{x}" y="{y}" text-anchor="middle" font-family="Capriola" font-size="{size}"'
    return f'<text {a} fill="{line}" stroke="{line}" stroke-width="{sw}" stroke-linejoin="round">{t}</text><text {a} fill="{fill}">{t}</text>'

# ------------------------------------------------------------------ floaters (40x40, 4f @ 6fps, circle (20,20) r13)
def bird(f, body, wing, belly, beak, hat=True, crest=None, longbeak=False):
    a = (-30, -5, 25, -5)[f]; bob = (0, -1, 0, 1)[f]
    g = f'<g transform="translate(0,{bob})">'
    g += P("M8,22 Q2,20 3,15 Q8,18 11,19 Z", wing, 1.4)
    g += E(19, 22, 11, 9, body, 1.8) + E(21, 25, 6, 5, belly, 0) + C(27, 15, 7, body, 1.8)
    if crest: g += P("M25,9 Q24,2 30,4 Q28,7 29,9 Z", crest, 1.2)
    g += (P("M33,15 Q42,18 38,24", "none", 0, f'stroke="{L}" stroke-width="3.6" stroke-linecap="round"') + P("M33,15 Q42,18 38,24", "none", 0, f'stroke="{beak}" stroke-width="2" stroke-linecap="round"')) if longbeak else P("M33,14 L38,15.5 L33,17 Z", beak, 1)
    g += C(29, 14, 1.6, EYE, 0) + C(28.5, 13.4, 0.55, "#FFF", 0) + E(27, 18, 1.8, 1.1, BLUSH, 0)
    g += f'<g transform="rotate({a} 18 19)">' + P("M18,19 Q8,8 4,12 Q8,20 18,22 Z", wing, 1.5) + "</g>"
    if hat: g += P("M22,10 Q27,0 33,9 Z", "url(#red)", 1.2) + R(21, 8.6, 13, 3, FUR, 0.9, 1.5) + C(32.6, 2.6, 1.8, FUR, 0.9)
    return g + "</g>"
def reindeer(f):
    bob = (0, -1, 0, 1)[f]; leg = (0, 3, 0, -3)[f]
    return (f'<g transform="translate(0,{bob})">' + P(f"M10,26 l{-3+leg/2},8 M15,27 l{2-leg/2},8 M24,27 l{-2+leg/2},8 M29,26 l{3-leg/2},8", "none", 0, f'stroke="{L}" stroke-width="2.6" stroke-linecap="round"')
            + E(19, 22, 12, 7, "#C99A6B", 1.8) + E(19, 24, 7, 4, "#F0D6B8", 0) + C(30, 13, 6.5, "#C99A6B", 1.8)
            + P("M27,7 L24,1 M24,3 L21,2 M32,7 L35,1 M35,3 L38,2", "none", 0, f'stroke="#8E6A4E" stroke-width="2" stroke-linecap="round"')
            + C(36, 14, 2.6, "#FF6F7F", 1) + C(29, 12, 1.4, EYE, 0) + E(31, 16, 1.6, 1, BLUSH, 0) + R(25, 17, 9, 2.6, RED2, 0.8, 1) + C(29.5, 20.6, 1.6, GOLD, 0.8)
            + P("M7,20 Q4,18 6,15", "none", 0, f'stroke="{L}" stroke-width="1.6"') + "</g>")
def plane(f):
    bob = (0, -0.6, 0, 0.6)[f]; prop = ("M37,14 V26", "M37,17 V23", "M34,20 H40", "M37,17 V23")[f]
    return (f'<g transform="translate(0,{bob})">' + P("M14,20 L4,12 L8,12 L18,18 Z", "#FFC4D4", 1.4) + E(21, 20, 15, 6, "#FFFFFF", 1.8) + P("M16,20 L10,31 L16,31 L24,21 Z", "#FFC4D4", 1.4)
            + R(24, 16, 8, 4, "#BFE6FF", 1, 2) + C(13, 19, 1.4, "#BFE6FF", 0) + C(18, 19, 1.4, "#BFE6FF", 0) + R(35.5, 18.5, 2.5, 3, "#C9C2E8", 0.8, 1)
            + P(prop, "none", 0, f'stroke="{L}" stroke-width="1.6" stroke-linecap="round"') + face(28, 22, 0.13) + P("M6,12 L4,10", "none", 0, f'stroke="{RED2}" stroke-width="2"') + "</g>")
def paper_crane(f):
    a = (-14, 0, 14, 0)[f]
    return (f'<g transform="translate(0,{(0,-1,0,1)[f]})">' + P("M6,24 L20,20 L34,24 L20,30 Z", "#FFC4D4", 1.6) + f'<g transform="rotate({a} 20 22)">' + P("M20,22 L10,6 L24,20 Z", "#FFE3EC", 1.4) + P("M20,22 L30,8 L22,20 Z", "#FFD0DE", 1.4) + "</g>"
            + P("M6,24 L2,14 L9,22 Z", "#FFC4D4", 1.2) + P("M34,24 L39,13 L36,13 L31,22 Z", "#FFC4D4", 1.2) + C(37, 14, 0.9, EYE, 0) + "</g>")
def penguin_floe(f):
    bob = (0, -1, 0, 1)[f]; tilt = (-3, 0, 3, 0)[f]
    return (f'<g transform="translate(0,{bob}) rotate({tilt} 20 30)">' + P("M5,30 L10,26 H32 L36,30 L32,34 H9 Z", "#DDF1FF", 1.6) + P("M10,26 H32 L30,28 H12 Z", "#FFFFFF", 0)
            + E(20, 19, 7, 9, "#4A4A78", 1.6) + E(20, 21, 4.6, 6.4, "#FFFFFF", 0) + C(18.6, 15, 1, EYE, 0) + C(21.4, 15, 1, EYE, 0) + P("M19,17 L20,18.6 L21,17 Z", "#FFB36B", 0.6)
            + P("M14,11 Q19,3 26,9 L26,12 Z", "url(#red)", 1) + R(13.5, 10.4, 13, 2.6, FUR, 0.8, 1.3) + C(26, 8, 1.6, FUR, 0.7) + "</g>")
FLOATERS = {
 "lapland": ("reindeer", reindeer, "generic", "a flying reindeer (bell collar)"),
 "london": ("pigeon", lambda f: bird(f, "#C9C2E8", "#A9A3C9", "#E6E2EE", GOLD2), "pigeon", "pigeon in a Santa hat"),
 "newyork": ("plane", plane, "plane", "little prop plane"),
 "rio": ("macaw", lambda f: bird(f, "#FF7F8F", "#7FA8F0", "#FFE08A", "#4A3358", True, "#FFE08A"), "pigeon", "scarlet macaw"),
 "egypt": ("ibis", lambda f: bird(f, "#FFFFFF", "#E6DDF7", "#FFFFFF", "#4A3358", True, None, True), "pigeon", "sacred ibis"),
 "tokyo": ("papercrane", paper_crane, "pigeon", "origami paper crane"),
 "sydney": ("gull", lambda f: bird(f, "#FFFFFF", "#C9C2E8", "#FFFFFF", "#FFB36B"), "pigeon", "seagull"),
 "antarctica": ("penguinfloe", penguin_floe, "icicle", "penguin drifting on a tiny ice floe"),
}
def build_floaters():
    for s, (nm, fn, death, note) in FLOATERS.items():
        base = f"obs-{s}-float-{nm}"; fr = []
        for f in range(4): SL.FILES[f"{base}-{f}"] = svg(40, 40, fn(f)); fr.append(f"{base}-{f}")
        SL.STRIPS[base + "-strip"] = fr
        FLOAT[s] = {"files": base + "-{0,1,2,3}", "strip": base + "-strip", "size": [40, 40], "type": "circle", "cx": 20, "cy": 20, "r": 13, "frames": 4, "fps": 6, "stage": s, "death": death, "art": note}

# ------------------------------------------------------------------ magic baubles + HUD
BAUB = {"rush": ("#FFD873", "#F6B54A", "#FFF4C9", "#B07A3A", "Golden bauble = Rush (same power as the golden ghost)"),
        "life": ("#FF8FA8", "#E04F66", "#FFE0E8", "#8A3A52", "Red bauble = Extra Life (same as the red special ghost)"),
        "chill": ("#9ED8FF", "#5AA8E8", "#E6F6FF", "#3E5E8E", "Blue bauble = Chill / slow-mo (same as the blue special ghost)")}
def heart(x, y, s, fill, line): return f'<path transform="translate({x},{y}) scale({s})" d="M0,6 C-9,0 -9,-7 -4.5,-7 C-2,-7 0,-5 0,-3.5 C0,-5 2,-7 4.5,-7 C9,-7 9,0 0,6 Z" fill="{fill}" stroke="{line}" stroke-width="{1.4/s:.2f}"/>'
def bauble(kind, f=0, hud=False):
    a, b, hi, line, _ = BAUB[kind]; sw = (-6, 0, 6, 0)[f] if not hud else 0
    gid = f"bb{kind}"
    g = (f'<defs><radialGradient id="{gid}" cx="0.35" cy="0.3" r="0.85"><stop offset="0" stop-color="{hi}"/><stop offset="0.55" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></radialGradient>'
         f'<radialGradient id="{gid}g"><stop offset="0.3" stop-color="{a}" stop-opacity="0.6"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient></defs>')
    if not hud: g += f'<circle cx="28" cy="30" r="{26 + (0, 1.5, 0, -1.5)[f]}" fill="url(#{gid}g)"/>'
    g += f'<g transform="rotate({sw} 28 10)">'
    g += (f'<path d="M25,10 Q28,4 31,10" fill="none" {st(1.6)}/>' + R(23, 10, 10, 6, "#E6DDF7", 1.6, 1.5) + C(28, 30, 15, f"url(#{gid})", 2.2)
          + f'<path d="M14,27 Q28,34 42,27" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.75"/>')
    if kind == "rush": g += star5(28, 33, 6, "#FFFBE0", line, 1.2)
    elif kind == "life": g += heart(28, 33, 0.85, "#FFE0E8", line)
    else: g += flake(28, 33, 5.5, "#FFFFFF", line, 0, 1.4)
    g += E(22, 23, 4, 2.4, "#FFFFFF", 0, 'opacity="0.9" transform="rotate(-30 22 23)"') + "</g>"
    if not hud:
        k = [(47, 12), (8, 40), (46, 46), (10, 14)]
        for i in range(2): x, y = k[(f + i * 2) % 4]; g += sparkle(x, y, 3.4 - i, "#FFFFFF", line, 0.95)
    return g
def build_baubles():
    PK = {}
    for kind in BAUB:
        fr = []
        for f in range(4): n = f"pickup-santa-{kind}-{f}"; SL.FILES[n] = svg(56, 56, bauble(kind, f)); fr.append(n)
        SL.STRIPS[f"pickup-santa-{kind}-strip"] = fr
        hud = svg(56, 56, bauble(kind, 0, True)).replace('width="56" height="56" viewBox="0 0 56 56"', 'width="48" height="48" viewBox="4 6 48 48"')
        SL.FILES[f"ui-hud-santa-{kind}"] = hud
        PK[f"santa-{kind}"] = {"files": f"pickup-santa-{kind}-{{0..3}}", "strip": f"pickup-santa-{kind}-strip", "size": [56, 56], "type": "circle", "cx": 28, "cy": 30, "r": 16,
                               "placement": "gapCentre", "fps": 8, "power": {"rush": "power-rush", "life": "power-life", "chill": "power-chill"}[kind], "hud": f"ui-hud-santa-{kind}-{{32,48}}", "note": BAUB[kind][4]}
    return PK

# ------------------------------------------------------------------ banner / badge / burst / mist
def motif(s):
    m = {"lapland": lambda x: flake(x, 22, 9, "#FFFFFF", "#7FA8D8"), "london": lambda x: C(x, 24, 9, "url(#red)", 1.8) + R(x - 3, 12, 6, 4, "#E6DDF7", 1.2),
         "newyork": lambda x: star5(x, 22, 10), "rio": lambda x: "".join(f'<path d="M{x},22 L{x+math.cos(a)*11:.1f},{22+math.sin(a)*11:.1f}" stroke="#FF8FB1" stroke-width="2.4" stroke-linecap="round"/>' for a in [i*math.pi/4 for i in range(8)]),
         "egypt": lambda x: P(f"M{x-11},32 L{x},12 L{x+11},32 Z", "#F2CF95", 1.8), "tokyo": lambda x: E(x, 24, 8, 10, "#FF6F7F", 1.8),
         "sydney": lambda x: C(x, 22, 8, "#FFE08A", 1.8) + "".join(f'<path d="M{x+math.cos(a)*11:.1f},{22+math.sin(a)*11:.1f} L{x+math.cos(a)*14:.1f},{22+math.sin(a)*14:.1f}" stroke="#F6B54A" stroke-width="2" stroke-linecap="round"/>' for a in [i*math.pi/4 for i in range(8)]),
         "antarctica": lambda x: E(x, 24, 7, 10, "#4A4A78", 1.6) + E(x, 26, 4.5, 7, "#FFFFFF", 0), "aurora": lambda x: sparkle(x, 22, 9, "#9EF0C8", "#4A3E7A")}[s]
    return m(22) + m(278)
def banner(s, title):
    a, b, Lc = BAN[s]; g = []
    for sx in (1, -1):
        x0 = 150 - sx * 118
        g.append(f'<path d="M{x0},30 L{x0 - sx*34},30 L{x0 - sx*24},48 L{x0 - sx*34},66 L{x0},66 Z" fill="{b}" stroke="{Lc}" stroke-width="2.4" stroke-linejoin="round"/>'
                 f'<path d="M{x0},66 L{x0 + sx*14},76 L{x0 + sx*14},62 Z" fill="{Lc}" opacity="0.55"/>')
    g.append(f'<path d="M32,18 Q150,6 268,18 L268,62 Q150,50 32,62 Z" fill="{a}" stroke="{Lc}" stroke-width="2.6" stroke-linejoin="round"/>'
             f'<path d="M40,24 Q150,13 260,24" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.75" stroke-linecap="round"/>'
             f'<path d="M40,56 Q150,45 260,56" stroke="{b}" stroke-width="2" fill="none" stroke-dasharray="4 4"/>' + snowcap(60, 240, 14, 4).replace('stroke-width="1.6"', 'stroke-width="1.2"'))
    g.append(motif(s))
    if title: g.append(text2(150, 47, title, 25 if len(title) <= 9 else 22, "#FFFFFF", Lc, 5))
    return svg(300, 90, "".join(g))
def badge(n=None):
    g = (P("M12,8 H84 Q92,8 92,16 V32 Q92,40 84,40 H12 Q4,40 4,32 V16 Q4,8 12,8 Z", "#FFE3EC", 2.4, f'stroke="#7A4E66" stroke-width="2.4"') + hl(10, 13, 60, 13, 2, 0.8)
         + C(74, 24, 13, "url(#red)", 2) + R(70, 8, 8, 4, "#E6DDF7", 1.2, 1) + E(69, 19, 3, 2, "#FFFFFF", 0, 'opacity="0.8"') + sparkle(91, 6, 4) + snowcap(10, 60, 9, 3))
    g += text2(36, 30, "Stage", 15, "#7A4E66", "#FFE3EC", 0.1)
    if n is not None: g += text2(74, 30, str(n), 16, "#FFFFFF", "#8A3A52", 3.4)
    return svg(96, 48, g)
def burst_item(s, k, x, y, a, sc):
    t = f'transform="translate({x:.1f},{y:.1f}) rotate({a:.0f}) scale({sc:.2f})"'
    items = {"lapland": [flake(0, 0, 7, "#FFFFFF", "#7FA8D8"), star5(0, 0, 7)], "london": [C(0, 0, 6, "url(#red)", 1.4), flake(0, 0, 6, "#FFFFFF", "#7FA8D8")],
             "newyork": [star5(0, 0, 7), flake(0, 0, 6, "#FFFFFF", "#7FA8D8")], "rio": [sparkle(0, 0, 7, "#FF8FB1", "#8A3A52"), sparkle(0, 0, 7, "#9EF0E0", "#3E6A5E"), sparkle(0, 0, 6, "#FFE08A", "#B07A3A")],
             "egypt": [star5(0, 0, 6, "#FFD873"), P("M-6,4 L0,-6 L6,4 Z", "#F2CF95", 1.2)], "tokyo": [E(0, 0, 5, 6.5, "#FF6F7F", 1.2), sparkle(0, 0, 6, "#FFE3F2", "#C86A8A")],
             "sydney": [C(0, 0, 5, "#FFE08A", 1.2), P("M0,-6 L2,-2 6,-1 3,2 4,6 0,4 -4,6 -3,2 -6,-1 -2,-2 Z", "#FFB36B", 1)], "antarctica": [flake(0, 0, 7, "#FFFFFF", "#7FA8D8"), sparkle(0, 0, 6, "#DDF1FF", "#5A8EC8")],
             "aurora": [sparkle(0, 0, 7, "#9EF0C8", "#3E6A5E"), sparkle(0, 0, 7, "#FF9ED8", "#8A3A6E")]}[s]
    return f'<g {t}>{items[k % len(items)]}</g>'
def burst(s, i):
    t = (i + 1) / 6; r = random.Random(11 + ORDER.index(s) if s in ORDER else 99); g = []
    for k in range(14):
        ang = 2 * math.pi * k / 14 + r.uniform(-0.2, 0.2); sp = r.uniform(0.7, 1.0)
        d = 12 + 58 * sp * (1 - (1 - t) ** 2)
        x, y = 80 + math.cos(ang) * d, 80 + math.sin(ang) * d + 16 * t * t
        op = 1 if t < 0.7 else 1 - (t - 0.7) / 0.35
        g.append(f'<g opacity="{max(0, op):.2f}">' + burst_item(s, k, x, y, r.uniform(-40, 40) + 120 * t, 1.0 + 0.2 * math.sin(k)) + "</g>")
    if i == 0: g.append(C(80, 80, 14, "#FFF4B8", 0, 'opacity="0.5"') + sparkle(80, 80, 9, "#FFFFFF", "#E8A050"))
    return svg(160, 160, "".join(g))
def mist(i, n=8):
    t = i / (n - 1); r = random.Random(21); g = []
    a = math.sin(math.pi * min(1, t / 0.75)) if t < 0.75 else (1 - t) / 0.25
    a = max(0.0, min(1.0, a))
    g.append(f'<rect width="360" height="640" fill="#F2F4FF" opacity="{0.35*a:.2f}"/>')
    for k in range(22):
        x, y, rr = r.uniform(-40, 400), r.uniform(-40, 680), r.uniform(50, 120)
        g.append(f'<circle cx="{x + (t - 0.5) * 30 * (1 if k % 2 else -1):.0f}" cy="{y:.0f}" r="{rr * (0.7 + 0.5 * t):.0f}" fill="{r.choice(("#FFFFFF", "#F2F4FF", "#E9EEFB"))}" opacity="{0.42*a:.2f}"/>')
    for k in range(40):
        x, y0 = r.uniform(0, 360), r.uniform(-60, 640); y = (y0 + t * 160) % 700 - 30
        g.append(f'<g opacity="{min(1, 0.3 + a):.2f}">' + flake(x, y, r.choice((3, 4, 5.5)), "#FFFFFF", "#B9C8E8", r.uniform(0, 60), 1.2) + "</g>")
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="640" viewBox="0 0 360 640">{"".join(g)}</svg>'
def build_ui():
    for s in ORDER + ["aurora"]:
        SL.FILES[f"ui-santa-banner-{s}"] = banner(s, NAMES[s]); SL.FILES[f"ui-santa-banner-{s}-blank"] = banner(s, None)
        fr = []
        for i in range(6): n = f"fx-santa-burst-{s}-{i}"; SL.FILES[n] = burst(s, i); fr.append(n)
        SL.STRIPS[f"fx-santa-burst-{s}-strip"] = fr
    SL.FILES["ui-santa-badge"] = badge()
    for n in range(1, 9): SL.FILES[f"ui-santa-badge-{n}"] = badge(n)
    fr = []
    for i in range(8): n = f"fx-santa-mist-{i}"; SL.FILES[n] = mist(i); fr.append(n)
    SL.STRIPS["fx-santa-mist-strip"] = fr

# ------------------------------------------------------------------ backgrounds
BG = {}
def build_bg():
    SL.FILES["bg-santa-far-stars"] = stars_tile()
    for s in ORDER + ["aurora"]:
        t, b = SKY[s]; L_ = {"far": [{"kind": "gradient", "top": t, "bottom": b, "y": 0, "h": 640}], "mid": [], "near": []}
        if s in STARS: L_["far"].append({"file": "bg-santa-far-stars.png", "size1x": [360, 320], "size2x": [720, 640], "y": 0, "repeat": "xy", "note": "shared; repeat 2x2 over the 720x640 slot"})
        for layer, part, y, h, inner, note in bg_parts(s):
            n = f"bg-santa-{s}-{layer}-{part}"; SL.FILES[n] = band(h, inner)
            L_[layer].append({"file": n + ".png", "size1x": [720, h], "size2x": [1440, h * 2], "y": y, "note": note})
        BG[s] = L_

# ------------------------------------------------------------------ JSON
def write_json(PK):
    stage_list = ORDER + ["aurora"]
    cols = {"_note": "Santa column sets, same schema as hitboxes.json 'columns'. Tops = -body + -cap-bottom (ceilEdge = gap edge); bottoms = -cap-top + -body (floorEdge). "
                     "'anchor' explains what each top hangs from (David's rule: every top is anchored or genuinely in the sky). 'death' = Santa death type."}
    cols.update(SL.EDGES)
    for s in ORDER:
        cap = s[0].upper() + s[1:]
        cols[f"_stageTops{cap}"] = {f"obs-{s}-{oid}": w for oid, fn, an, d, w in TOPS[s]}
        cols[f"_stageBottoms{cap}"] = {f"obs-{s}-{oid}": w for oid, fn, d, w in BOTS[s]}
    cols["_stageTopsAurora"] = {**cols["_stageTopsAntarctica"], "note": "endless zone reuses the Antarctica columns (and optionally a random mix of all stages)"}
    cols["_stageBottomsAurora"] = dict(cols["_stageBottomsAntarctica"])
    H = dict(SL.HIT)
    H["_note"] = "Santa's Rocket Run (concept). Same schema as assets/hitboxes.json. Column pieces at top level; check with tools/check_santa_continuity.py"
    H["columns"] = cols
    H["hazards"] = {f"santa-float-{s}": v for s, v in FLOAT.items()}
    H["pickups"] = PK
    H["santa"] = {"files": "santa-c-{idle,boost}-*", "canvas": [96, 128], "anchor": [48, 48], "type": "circle", "cx": 48, "cy": 49, "r": 18,
                  "note": "from ../santa-c (NOTES.md): == ghost circle (32,33) r18 shifted by +16"}
    H["backgrounds"] = {"_note": "decorative only - NO hitboxes. Lite set: each layer is a list of parts drawn at world y inside the 720-wide slot (tileWidth 720, seamless in x), as backgrounds.void in hitboxes.json",
                        "stages": stage_list, "layers": ["far", "mid", "near"], "scroll": {"far": 0.1, "mid": 0.3, "near": 0.6, "aurora": {"far": 0.05, "mid": 0.15, "near": 0.5}},
                        "transition": {"overlay": "fx-santa-mist-{0..7}", "strip": "fx-santa-mist-strip", "size": [360, 640], "fps": 12, "swapAtFrame": 3,
                                       "tint": MIST_TINT, "tintedStrips1x": "fx-santa-mist-<stage>-strip (1x, pre-tinted)", "note": "white snow mist; tint with multiply or use the pre-tinted strips; swap stage layers under the mist at frame 3"},
                        **BG}
    H["ui"] = {"banner": "ui-santa-banner-<stage>[-blank] 300x90", "badge": "ui-santa-badge[-1..8] 96x48", "burst": {"files": "fx-santa-burst-<stage>-{0..5}", "size": [160, 160], "centre": [80, 80], "fps": 12, "loop": False}}
    json.dump(H, open(os.path.join(OUT, "santa-hitboxes.json"), "w"), indent=1)
    sky = {"_note": "top/bottom of each Santa stage's vertical sky gradient (y 0 -> 640); 'aurora' = endless zone"}
    sky.update({s: {"top": t, "bottom": b} for s, (t, b) in SKY.items()})
    json.dump(sky, open(os.path.join(OUT, "santa-sky-palettes.json"), "w"), indent=1)
    dm = {"_note": "obstacle / floater id -> Santa death strip death-santa-<type> (../santa-c). Anything not listed -> generic. Ground hit -> floor.",
          "floor": "floor", "default": "generic", "deaths": ["icicle", "chimney", "pigeon", "plane", "floor", "generic"]}
    dm["columns"] = {k: v["death"] for k, v in SL.EDGES.items()}
    dm["floaters"] = {f"santa-float-{s}": v["death"] for s, v in FLOAT.items()}
    json.dump(dm, open(os.path.join(OUT, "santa-death-map.json"), "w"), indent=1)

# ------------------------------------------------------------------ previews
def font(sz): return ImageFont.truetype(FONT, sz)
def grad(t, b, w=360, h=640):
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    tc = [int(t[i:i+2], 16) for i in (1, 3, 5)]; bc = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    for y in range(h): k = y / (h - 1); d.line([(0, y), (w, y)], fill=tuple(int(tc[i] + (bc[i] - tc[i]) * k) for i in range(3)) + (255,))
    return im
def I(name, k=1): return Image.open(os.path.join(OUT, f"png/{k}x", name + ".png")).convert("RGBA")
def column(im, x, top, bot, gapT, gapB):
    tc = I(top + "-cap-bottom"); tb = I(top + "-body"); ce = SL.EDGES[top]["ceilEdge"]
    cy = gapT - ce; im.alpha_composite(tc, (x, cy)); y = cy - 64
    while y > -64: im.alpha_composite(tb, (x, y)); y -= 64
    if "topLip" in SL.EDGES[top]: im.alpha_composite(I(SL.EDGES[top]["topLip"]["file"]), (x - 16, 0))
    bc = I(bot + "-cap-top"); bb = I(bot + "-body"); fe = SL.EDGES[bot]["floorEdge"]
    cy = gapB - fe; y = cy + 80
    while y < 640: im.alpha_composite(bb, (x, y)); y += 64
    im.alpha_composite(bc, (x, cy))
def mock(s, ti=0, bi=0, ti2=1, bi2=2, santa=True):
    t, b = SKY[s]; im = grad(t, b)
    if s in STARS:
        stt = I("bg-santa-far-stars")
        for y in (0, 320): im.alpha_composite(stt, (0, y))
    for layer in ("far", "mid", "near"):
        for p in BG[s][layer]:
            if "file" in p and not p["file"].startswith("bg-santa-far-stars"): im.alpha_composite(I(p["file"][:-4]).crop((0, 0, 360, p["size1x"][1])), (0, p["y"]))
    st_ = s if s in ORDER else "antarctica"
    tops = [f"obs-{st_}-{o[0]}" for o in TOPS[st_]]; bots = [f"obs-{st_}-{o[0]}" for o in BOTS[st_]]
    column(im, 196, tops[ti], bots[bi], 210, 420); column(im, 20, tops[ti2], bots[bi2], 300, 500) if santa else None
    if s in FLOATERS: im.alpha_composite(I(f"obs-{s}-float-{FLOATERS[s][0]}-0"), (300, 300))
    im.alpha_composite(I("pickup-santa-rush-0"), (210, 288))
    if santa:
        sp = os.path.join(SANTA, "santa-c", "png", "1x", "santa-c-idle-0.png")
        if os.path.exists(sp): im.alpha_composite(Image.open(sp).convert("RGBA"), (120 - 48, 380 - 48))
    d = ImageDraw.Draw(im)
    d.text((180, 60), "24", font=font(44), fill="white", anchor="mm", stroke_width=5, stroke_fill="#6B4E7A")
    return im
def preview(s):
    W_, H_ = 1240, 700
    sh = Image.new("RGBA", (W_, H_), (36, 30, 66, 255)); d = ImageDraw.Draw(sh)
    sh.alpha_composite(mock(s), (10, 50))
    i = ORDER.index(s) + 1 if s in ORDER else "∞"
    d.text((10, 12), f"Santa's Rocket Run · stage {i} · {NAMES[s]}  (concept, not wired)", font=font(22), fill="#FFE08A")
    x0 = 390
    if s in ORDER:
        tops = [f"obs-{s}-{o[0]}" for o in TOPS[s]]; bots = [f"obs-{s}-{o[0]}" for o in BOTS[s]]
        for k, n in enumerate(tops + bots):
            x = x0 + k * 100; y = 50
            col = Image.new("RGBA", (80, 208), (0, 0, 0, 0))
            if SL.EDGES[n]["side"] == "top":
                col.alpha_composite(I(n + "-body"), (0, 0)); col.alpha_composite(I(n + "-body"), (0, 64)); col.alpha_composite(I(n + "-cap-bottom"), (0, 128))
            else:
                col.alpha_composite(I(n + "-cap-top"), (0, 0)); col.alpha_composite(I(n + "-body"), (0, 80)); col.alpha_composite(I(n + "-body"), (0, 144))
            sh.alpha_composite(col, (x, y + 22))
            d.text((x + 40, y + 6), n.split("-", 2)[2], font=font(12), fill="white", anchor="mm")
            d.text((x + 40, y + 240), ("TOP" if k < 3 else "BOT") + " · " + SL.EDGES[n]["death"], font=font(11), fill="#C9C2E8", anchor="mm")
        y = 310
        nm = FLOATERS[s][0]
        d.text((x0, y), f"floater: {nm} (4f @6fps)", font=font(13), fill="white")
        for f in range(4): sh.alpha_composite(I(f"obs-{s}-float-{nm}-{f}", 2), (x0 + f * 86, y + 20))
    else:
        y = 310; d.text((x0, 60), "Endless zone after Antarctica: aurora starfield.\nColumns: reuse Antarctica (or a random mix of all stages).", font=font(15), fill="white")
    sh.alpha_composite(I(f"ui-santa-banner-{s}"), (x0 + 360, y + 10))
    if s in ORDER: sh.alpha_composite(I(f"ui-santa-badge-{i}"), (x0 + 680, y + 30))
    d.text((x0, y + 110), "burst fx (6f @12fps)", font=font(13), fill="white")
    for f in range(6): sh.alpha_composite(I(f"fx-santa-burst-{s}-{f}").resize((100, 100)), (x0 + f * 104, y + 128))
    d.text((x0, y + 240), "transition: snow mist, tinted", font=font(13), fill="white")
    ms = Image.open(os.path.join(OUT, "png/1x", f"fx-santa-mist-{s}-strip.png")).convert("RGBA")
    for f in (1, 3, 5):
        fr = ms.crop((f * 360, 0, f * 360 + 360, 640)).resize((54, 96)); bgm = mock(s, santa=False).resize((54, 96)); bgm.alpha_composite(fr)
        sh.alpha_composite(bgm, (x0 + (f // 2) * 62, y + 262))
    for k, kind in enumerate(BAUB): sh.alpha_composite(I(f"pickup-santa-{kind}-0"), (x0 + 220 + k * 64, y + 290))
    d.text((x0 + 420, y + 300), "sky " + " -> ".join(SKY[s]), font=font(13), fill="#C9C2E8")
    os.makedirs(os.path.join(OUT, "previews"), exist_ok=True)
    p = os.path.join(OUT, "previews", f"santa-preview-{s}.png")
    sh.convert("RGB").quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(p, optimize=True); return p
def overview():
    names = ORDER + ["aurora"]; tw, th = 240, 427
    sh = Image.new("RGB", (tw * 5 + 60, th * 2 + 110), (36, 30, 66)); d = ImageDraw.Draw(sh)
    d.text((20, 14), "Santa's Rocket Run - stage set overview (1-8 + endless aurora zone)", font=font(26), fill="#FFE08A")
    for k, s in enumerate(names):
        x = 10 + (k % 5) * (tw + 10); y = 60 + (k // 5) * (th + 24)
        sh.paste(mock(s, santa=(k == 1 or True)).resize((tw, th), Image.LANCZOS).convert("RGB"), (x, y))
        d.text((x + tw / 2, y + th + 10), f"{k+1 if k < 8 else '∞'} · {NAMES[s]}", font=font(16), fill="white", anchor="mm")
    x = 10 + 4 * (tw + 10); y = 60 + th + 24
    p = os.path.join(OUT, "previews", "santa-overview.png")
    sh.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(p, optimize=True); return p

def tint_mists():
    base = Image.open(os.path.join(OUT, "png/1x", "fx-santa-mist-strip.png")).convert("RGBA")
    for s, c in MIST_TINT.items():
        rgb = [int(c[i:i+2], 16) for i in (1, 3, 5)]
        r, g, b, a = base.split()
        r = r.point(lambda v, m=rgb[0]: v * m // 255); g = g.point(lambda v, m=rgb[1]: v * m // 255); b = b.point(lambda v, m=rgb[2]: v * m // 255)
        Image.merge("RGBA", (r, g, b, a)).save(os.path.join(OUT, "png/1x", f"fx-santa-mist-{s}-strip.png"), optimize=True)

if __name__ == "__main__":
    build_columns(); build_floaters(); PK = build_baubles(); build_ui(); build_bg()
    export_all()
    for kind in BAUB:   # HUD icons at 32/48
        s = SL.FILES[f"ui-hud-santa-{kind}"]
        for px in (32, 48): png(s, px, px).save(os.path.join(OUT, "png/1x", f"ui-hud-santa-{kind}-{px}.png"), optimize=True)
    tint_mists(); write_json(PK)
    ps = [preview(s) for s in ORDER + ["aurora"]] + [overview()]
    for p in ps: print(os.path.relpath(p, SANTA), os.path.getsize(p))
    print(len(SL.FILES), "svgs;", len(SL.EDGES), "columns")
