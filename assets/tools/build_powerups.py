"""v0.5 power-ups: Golden Ghost Rush, Red Extra Life, Blue Slow-Mo Chill.
Pickups, ghost overlays, FX strips, frost vignette, HUD icons. Writes SVGs + png/1x,2x + strips,
and merges pickup hitboxes into hitboxes.json. Specs: ASSETS.md section 13."""
import os, sys, math, json, random, cairosvg
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import build_v05 as V
from build_v05 import svg, inner, star5, puff, ghost
from build_ghosts import sparkle
from build_extras import sweet_wrapped, sweet_lollipop, sweet_macaron
OUT = os.path.join(os.path.dirname(__file__), "..")
F = {}; STRIPS = {}
V.TINT["red"] = dict(body_hi="#FFF0F2", body_lo="#FF9EB0", shade="#F2839A", line="#8A3A52", eye="#5A2238", eye2="#9A4A64", blush="#FF7F9E", mouth="#E2557A", arm="#FFD6DE")
V.TINT["blue"] = dict(body_hi="#F2FAFF", body_lo="#A9D8F5", shade="#8CC4EE", line="#3E5E8E", eye="#2E4468", eye2="#5A78A8", blush="#C9D8F5", mouth="#8AB0E0", arm="#DDEEFF")
TOK = {"rush": ("golden", None, "#FFF1BF", "#FFE08A", "#FFE7A3", ("#FFFBE0", "#E2A23E")),
       "life": ("normal", "red", "#FFE0E6", "#FF9EB0", "#FFC2CE", ("#FFE6EC", "#D2507A")),
       "chill": ("normal", "blue", "#E6F6FF", "#A9D8F5", "#CFEAFF", ("#F4FBFF", "#5A8EC8"))}

def heart(x, y, s, fill="#FF8FAE", line="#8A3A52", face=True):
    g = (f'<g transform="translate({x},{y}) scale({s})"><path d="M0,6 C-9,0 -9,-7 -4.5,-7 C-2,-7 0,-5 0,-3.5 C0,-5 2,-7 4.5,-7 C9,-7 9,0 0,6 Z" '
         f'fill="{fill}" stroke="{line}" stroke-width="{1.6/s:.2f}" stroke-linejoin="round"/><ellipse cx="-4" cy="-4" rx="1.6" ry="1" fill="#FFF" opacity="0.85" transform="rotate(-30 -4 -4)"/>')
    if face: g += f'<circle cx="-2" cy="-1" r="0.7" fill="{line}"/><circle cx="2" cy="-1" r="0.7" fill="{line}"/><path d="M-1,0.8 Q0,1.8 1,0.8" fill="none" stroke="{line}" stroke-width="0.6"/>'
    return g + '</g>'
def flake(x, y, r, rot=0, col="#FFFFFF", line="#5A8EC8"):
    arms = ""
    for i in range(6):
        a = math.radians(rot + i * 60); ex, ey = x + math.cos(a)*r, y + math.sin(a)*r
        mx, my = x + math.cos(a)*r*0.55, y + math.sin(a)*r*0.55
        for d in (-50, 50):
            b = a + math.radians(d); arms += f"M{mx:.1f},{my:.1f} L{mx+math.cos(b)*r*0.3:.1f},{my+math.sin(b)*r*0.3:.1f} "
        arms += f"M{x},{y} L{ex:.1f},{ey:.1f} "
    return (f'<path d="{arms}" stroke="{line}" stroke-width="{max(1.2, r*0.32):.1f}" stroke-linecap="round"/>'
            f'<path d="{arms}" stroke="{col}" stroke-width="{max(0.6, r*0.16):.1f}" stroke-linecap="round"/><circle cx="{x}" cy="{y}" r="{r*0.22:.1f}" fill="{col}" stroke="{line}" stroke-width="0.6"/>')
def badge_mark(kind, x, y, s):
    if kind == "rush": return f'<g transform="translate({x},{y}) scale({s})"><path d="M2,-8 L-5,1 H0 L-2,8 L5,-1 H0 Z" fill="#FFF7C8" stroke="#B0702E" stroke-width="1.3" stroke-linejoin="round"/></g>'
    if kind == "life": return heart(x, y, s * 0.75, face=False)
    return flake(x, y, 6.5 * s)

def token(kind, f):
    k, tint, c1, c2, ring, sp = TOK[kind]
    dy = (0, -1.2, -1.8, -0.8)[f]; gid = f"tk{kind}{f}"
    g = [f'<defs><radialGradient id="{gid}"><stop offset="0.55" stop-color="{c1}" stop-opacity="0.75"/><stop offset="0.85" stop-color="{c2}" stop-opacity="0.35"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></radialGradient></defs>',
         f'<circle cx="28" cy="28" r="27" fill="url(#{gid})"/>',
         f'<circle cx="28" cy="28" r="22.5" fill="none" stroke="{ring}" stroke-width="1.6" stroke-dasharray="1.5 3.2" stroke-linecap="round" transform="rotate({f*12} 28 28)"/>',
         f'<g transform="translate(28,{28+dy}) scale(0.84) translate(-32,-33)">{ghost(k, "open", "w", tint, glow=False)}</g>',
         badge_mark(kind, 45, 44 + dy * 0.5, 0.85)]
    random.seed(f)
    for i, (x, y) in enumerate(((8, 12), (48, 12), (9, 45))):
        r = 2.2 + 1.6 * abs(math.sin(f * 1.3 + i * 2))
        g.append(sparkle(x, y, r, sp[0], sp[1]))
    return svg(56, 56, "".join(g))

def aura(f):  # 96x96, centre (48,49) = ghost (32,33)
    r = 38 + 2.5 * math.sin(f * math.pi / 2)
    g = [f'<defs><radialGradient id="au{f}"><stop offset="0.45" stop-color="#FFE7A0" stop-opacity="0.6"/><stop offset="0.8" stop-color="#FFD873" stop-opacity="0.25"/><stop offset="1" stop-color="#FFD873" stop-opacity="0"/></radialGradient></defs>',
         f'<circle cx="48" cy="49" r="{r:.1f}" fill="url(#au{f})"/>']
    for i in range(6):
        a = math.radians(i * 60 + f * 15); d = 36
        g.append(sparkle(48 + math.cos(a)*d, 49 + math.sin(a)*d, 2.5 + 1.5 * ((i + f) % 2), "#FFFBE0", "#E2A23E"))
    return svg(96, 96, "".join(g))
def streaks(f, x0, y0, n=4, col="#FFE08A", line="#E2A23E"):
    s = ""
    for i in range(n):
        y = y0 + i * 9; L = 26 + ((i * 7 + f * 9) % 18); x = x0 - ((f * 6 + i * 5) % 10)
        s += f'<path d="M{x},{y} H{x-L}" stroke="{line}" stroke-width="5" stroke-linecap="round" opacity="0.5"/><path d="M{x},{y} H{x-L}" stroke="{col}" stroke-width="3" stroke-linecap="round"/>'
    return s
def ghost_rush(f):  # 112x64; ghost in the 64x64 at x 48..112 -> offset (-48,0)
    g = [inner(aura(f)).replace(f'au{f}"', f'gr{f}"').replace(f'#au{f}', f'#gr{f}')]
    g = [f'<g transform="translate(32,-16)">{g[0]}</g>', streaks(f, 52, 22)]
    for k, op in ((2, 0.25), (1, 0.45)):
        g.append(f'<g opacity="{op}" transform="translate({48 - 18*k},0)">{ghost("golden", "closed", "w", None, glow=False, sway=-2)}</g>')
    g.append(f'<g transform="translate(48,{(0, -1, 0, 1)[f]})">{ghost("golden", "closed" if f == 2 else "open", "w", None, arms=-25, sway=-2.5)}</g>')
    return svg(112, 64, "".join(g))
def trail(f):  # 80x64 afterimages; right edge sits at ghost x+16
    g = []
    for k, op in ((3, 0.18), (2, 0.3), (1, 0.45)):
        g.append(f'<g opacity="{op}" transform="translate({80 - 32 - 16 - 16*k + (f % 2) * 2},0)">{ghost("golden", "closed", "w", None, glow=False, sway=-2)}</g>')
    g.append(streaks(f, 70, 20))
    return svg(80, 64, "".join(g))

def candy_burst(f):  # 128x128, centre (64,64), 6 frames @12fps = 0.5s
    t = f / 5; g = []
    if t < 0.6: g.append(V.bonk(64, 64, 18 + 30 * t, f, False).replace('<path', f'<path opacity="{1 - t*1.4:.2f}"', 1))
    sw = [sweet_wrapped(), sweet_lollipop(), sweet_macaron()]
    for i in range(8):
        a = 2 * math.pi * i / 8 + 0.2; d = 6 + 50 * (1 - (1 - t) ** 2); gy = 22 * t * t
        x, y = 64 + math.cos(a) * d, 64 + math.sin(a) * d + gy
        sc = 0.55 + 0.25 * (i % 2); op = 1 if t < 0.7 else (1 - t) / 0.3
        g.append(f'<g opacity="{op:.2f}" transform="translate({x:.1f},{y:.1f}) rotate({i*40 + f*50}) scale({sc}) translate(-16,-16)">{inner(sw[i % 3])}</g>')
    for i in range(6):
        a = 2 * math.pi * i / 6; d = 14 + 40 * t
        g.append(f'<g opacity="{max(0, 1 - t):.2f}">' + star5(64 + math.cos(a)*d, 64 + math.sin(a)*d, 4 - 2 * t, ("#FFE9A8", "#FFC9DA", "#BDEBD6")[i % 3], "#B07A3A", f * 30) + '</g>')
    return svg(128, 128, "".join(g))

def heart_overlay(f):  # 20x20, place top-left at ghost (+40,+2)
    s = (1.0, 1.15)[f]
    return svg(20, 20, heart(10, 11, s))
def heart_pop(kind, f):  # 96x96 centre (48,48), 6 frames @12fps
    t = f / 5; g = []
    if kind == "gain":
        s = (0.6, 1.4, 1.9, 1.7, 1.8, 1.8)[f]; y = 48 - 14 * t; op = 1 if t < 0.8 else 0.5
        g.append(f'<g opacity="{op}">{heart(48, y, s)}</g>')
        for i in range(8):
            a = 2 * math.pi * i / 8; d = 12 + 30 * t
            g.append(f'<g opacity="{max(0, 1 - t):.2f}">{heart(48 + math.cos(a)*d, 48 + math.sin(a)*d, 0.45, "#FFC2CE", face=False)}</g>' if i % 2 else
                     f'<g opacity="{max(0, 1 - t):.2f}">' + sparkle(48 + math.cos(a)*d, 48 + math.sin(a)*d, 3.5, "#FFE6EC", "#D2507A") + '</g>')
    else:  # lost: heart wobbles, splits, halves fall, puff
        if f < 2: g.append(heart(48 + (2 if f else -2), 44, 1.8))
        else:
            sp = (f - 1) * 7; dy = (f - 1) ** 2 * 1.4; op = max(0, 1 - (f - 2) / 4)
            for side in (-1, 1):
                g.append(f'<g opacity="{op:.2f}" transform="translate({48 + side*sp},{44 + dy}) rotate({side*15*(f-1)})"><clipPath id="hc{f}{side}"><rect x="{-20 if side < 0 else 0}" y="-20" width="20" height="40"/></clipPath>'
                         f'<g clip-path="url(#hc{f}{side})">{heart(0, 0, 1.8, face=False)}</g></g>')
            g.append(V.puff(48, 46, 8 + 3 * f, max(0, 0.9 - (f - 2) * 0.25), "#FFF0F2", "#F2A6B8"))
    return svg(96, 96, "".join(g))

def frost_vignette():  # 360x640 overlay
    g = ['<defs><radialGradient id="fv" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#DFF3FF" stop-opacity="0"/><stop offset="0.85" stop-color="#CFEAFF" stop-opacity="0.45"/><stop offset="1" stop-color="#F4FBFF" stop-opacity="0.85"/></radialGradient></defs>',
         '<rect width="360" height="640" fill="url(#fv)"/>']
    random.seed(11)
    for (cx, cy) in ((0, 0), (360, 0), (0, 640), (360, 640)):
        for i in range(14):
            r = random.uniform(30, 90); a = random.uniform(0, math.pi / 2)
            x = cx + (1 if cx == 0 else -1) * math.cos(a) * r * random.uniform(0.3, 1.1)
            y = cy + (1 if cy == 0 else -1) * math.sin(a) * r * random.uniform(0.3, 1.1)
            g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(14, 34):.0f}" fill="#F4FBFF" opacity="0.35"/>')
        for i in range(6):
            x = cx + (1 if cx == 0 else -1) * random.uniform(10, 80); y = cy + (1 if cy == 0 else -1) * random.uniform(10, 110)
            g.append(f'<g opacity="0.8">{flake(round(x), round(y), random.uniform(5, 11), random.uniform(0, 60), "#FFFFFF", "#8CC4EE")}</g>')
    for i in range(10):  # small edge flakes
        g.append(f'<g opacity="0.6">{flake(random.choice((10, 350)), random.uniform(160, 480), random.uniform(3, 6), 0, "#FFFFFF", "#8CC4EE")}</g>')
    return svg(360, 640, "".join(g))
def frost_burst(f):  # 96x96 centre (48,48), 6 frames @12fps
    t = f / 5; g = []
    g.append(f'<circle cx="48" cy="48" r="{10 + 34*t:.1f}" fill="none" stroke="#CFEAFF" stroke-width="{4 - 3*t:.1f}" opacity="{1 - t:.2f}"/>')
    for i in range(8):
        a = 2 * math.pi * i / 8 + 0.4; d = 8 + 34 * t
        g.append(f'<g opacity="{max(0, 1 - t*0.9):.2f}">{flake(round(48 + math.cos(a)*d, 1), round(48 + math.sin(a)*d, 1), 4 + 2*(i % 2) - 1.5*t, f*20)}</g>')
    return svg(96, 96, "".join(g))

def hud(kind, size):
    g = {"rush": '<circle cx="24" cy="24" r="20" fill="#FFE9A8" stroke="#8E5A3C" stroke-width="2.4"/>' + badge_mark("rush", 24, 24, 2.1),
         "life": '<circle cx="24" cy="24" r="20" fill="#FFD6DE" stroke="#8A3A52" stroke-width="2.4"/>' + heart(24, 25, 1.9),
         "chill": '<circle cx="24" cy="24" r="20" fill="#DDEEFF" stroke="#3E5E8E" stroke-width="2.4"/>' + flake(24, 24, 13, 0, "#FFFFFF", "#3E5E8E")}[kind]
    g += '<path d="M12,14 Q16,9 22,8" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.8"/>' + sparkle(41, 6, 3.4, "#FFF4B8", "#D9953A")
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 48 48">\n{g}\n</svg>\n'

def build():
    def strip(name, frames, maker):
        STRIPS[name] = []
        for i in range(frames): F[f"{name}-{i}"] = maker(i); STRIPS[name].append(f"{name}-{i}")
    for k in TOK: strip(f"pickup-{k}", 4, lambda i, k=k: token(k, i))
    strip("ghost-rush", 4, ghost_rush); strip("fx-rush-aura", 4, aura); strip("fx-rush-trail", 4, trail)
    strip("fx-candy-burst", 6, candy_burst)
    strip("ghost-heart-overlay", 2, heart_overlay)
    strip("fx-heart-pop", 6, lambda i: heart_pop("gain", i)); strip("fx-heart-break", 6, lambda i: heart_pop("lost", i))
    F["ui-frost-vignette"] = frost_vignette()
    for j, (n, r) in enumerate((("a", 7), ("b", 5), ("c", 3.5))):
        F[f"fx-frost-flake-{n}"] = svg(16, 16, flake(8, 8, r, j * 15))
    strip("fx-frost-burst", 6, frost_burst)
    for k in ("rush", "life", "chill"):
        for sz in (32, 48): F[f"ui-hud-{k}-{sz}"] = hud(k, sz)

HIT_PU = {
  "rush":  {"files": "pickup-rush-{0..3}", "strip": "pickup-rush-strip", "size": [56, 56], "type": "circle", "cx": 28, "cy": 28, "r": 16, "placement": "gapCentre", "fps": 8},
  "life":  {"files": "pickup-life-{0..3}", "strip": "pickup-life-strip", "size": [56, 56], "type": "circle", "cx": 28, "cy": 28, "r": 16, "placement": "gapCentre", "fps": 8},
  "chill": {"files": "pickup-chill-{0..3}", "strip": "pickup-chill-strip", "size": [56, 56], "type": "circle", "cx": 28, "cy": 28, "r": 16, "placement": "gapCentre", "fps": 8},
}
if __name__ == "__main__":
    build()
    for d in ("png/1x", "png/2x"): os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for k, v in F.items():
        p = os.path.join(OUT, k + ".svg"); open(p, "w").write(v)
        for sc, d in ((1, "png/1x"), (2, "png/2x")):
            cairosvg.svg2png(url=p, write_to=os.path.join(OUT, d, k + ".png"), scale=sc)
    for name, frames in STRIPS.items():
        for d in ("png/1x", "png/2x"):
            ims = [Image.open(os.path.join(OUT, d, f + ".png")).convert("RGBA") for f in frames]
            sh = Image.new("RGBA", (ims[0].width * len(ims), ims[0].height), (0, 0, 0, 0))
            for i, im in enumerate(ims): sh.alpha_composite(im, (i * im.width, 0))
            sh.save(os.path.join(OUT, d, name + "-strip.png"))
    hp = os.path.join(OUT, "hitboxes.json"); H = json.load(open(hp))
    H["pickups"].update({f"power-{k}": v for k, v in HIT_PU.items()})
    json.dump(H, open(hp, "w"), indent=2)
    print(len(F), "svgs,", len(STRIPS), "strips")
