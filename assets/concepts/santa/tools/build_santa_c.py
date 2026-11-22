"""Santa C (hooded chibi + gift-box jetpack) sprite set, picked by David. Concept-folder build, NOT wired into the game.
Writes ../santa-c/{*.svg, png/1x, png/2x (+ -strip.png)}, ../santa-c-sprites.png, ../santa-c-boost-preview.{mp4,gif}.
Conventions (as the ghost, ASSETS.md 1 / 11.1):
  hero frames: 64px gameplay scale on a 96x128 canvas (32px extra below for the full jet flame); anchor (48,48) == ghost anchor (32,32) + 16;
               hitbox circle (48,49) r18 == ghost (32,33) r18. Draw at (x - 48k, y - 48k), k = size/64. Rotate about the anchor.
  deaths:      128x128, anchor (64,64), 12 fps, play once, hold last frame (same as death-<type>-*).
  fx trail:    160x128, emitter point (144,64), 10f @ 16 fps; spawn at the jet nozzle each tap and let it scroll with the world.
Run: python3 build_santa_c.py"""
import os, io, sys, math, random, subprocess, shutil, cairosvg
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_santa_concepts as K
from build_santa_concepts import L, EYE, EYE2, BLUSH, MOUTH, RED, RED2, RED_D, FUR, SKIN, GOLD, GOLD2, MINT, BOOT, st, pompom, sack
SANTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(SANTA, "santa-c")
FILES, STRIPS = {}, {}
VAR = {  # bauble variants: trim, aura, flame (outer, mid, core), extra sparkle colour
  "normal": dict(trim=FUR,       aura=None,      flame=("#FFB36B", "#FFE08A", "#FFFFFF"), spk="#FFF4B8"),
  "rush":   dict(trim="#FFE08A", aura="#FFD45C", flame=("#FFC24B", "#FFF0A0", "#FFFFFF"), spk="#FFF4B8"),
  "life":   dict(trim="#FFC4D4", aura="#FF7FA8", flame=("#FF8FB1", "#FFD0DE", "#FFFFFF"), spk="#FFD0DE"),
  "chill":  dict(trim="#D6F0FF", aura="#8FD3FF", flame=("#7CC8FF", "#CDEBFF", "#FFFFFF"), spk="#E6F6FF"),
}
def defs(v, uid):
    a = VAR[v]["aura"] or "#FFFFFF"
    return (f'<defs><linearGradient id="e" x1="0" y1="0" x2="0" y2="1"><stop offset="0.35" stop-color="{EYE}"/><stop offset="1" stop-color="{EYE2}"/></linearGradient>'
            f'<radialGradient id="red" cx="0.35" cy="0.3" r="0.85"><stop offset="0" stop-color="{RED}"/><stop offset="0.6" stop-color="{RED2}"/><stop offset="1" stop-color="{RED_D}"/></radialGradient>'
            f'<radialGradient id="skin" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#FFF3EA"/><stop offset="1" stop-color="{SKIN}"/></radialGradient>'
            f'<radialGradient id="aura{uid}"><stop offset="0.35" stop-color="{a}" stop-opacity="0.55"/><stop offset="0.75" stop-color="{a}" stop-opacity="0.22"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient></defs>')
def svg(w, h, inner): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{inner}</svg>'

def face(cx, cy, k, eyes="open", mouth="w"):
    g = [f'<g transform="translate({cx},{cy}) scale({k})">']
    for x in (-13.2, 13.2): g.append(f'<ellipse cx="{x}" cy="4.2" rx="3.6" ry="2.1" fill="{BLUSH}" opacity="0.85"/>')
    g.append('<g stroke="#FFFFFF" stroke-width="0.7" stroke-linecap="round" opacity="0.8"><path d="M-15.2,3.6 l0.9,-1.2 M-13.4,3.8 l0.9,-1.2"/><path d="M11.2,3.6 l0.9,-1.2 M13,3.8 l0.9,-1.2"/></g>')
    for x in (-7.8, 7.8):
        if eyes == "open":
            g.append(f'<ellipse cx="{x}" cy="-2.4" rx="4.3" ry="5.3" fill="url(#e)"/><ellipse cx="{x-1.3}" cy="-4.4" rx="1.8" ry="2.1" fill="#FFF"/>'
                     f'<circle cx="{x+1.6}" cy="0" r="0.95" fill="#FFF"/><circle cx="{x+2.2}" cy="-3.8" r="0.5" fill="#FFF" opacity="0.8"/>')
        elif eyes == "happy":
            g.append(f'<path d="M{x-4},-1.8 Q{x},-6 {x+4},-1.8" fill="none" stroke="{EYE}" stroke-width="2" stroke-linecap="round"/>')
        elif eyes == "blink":
            g.append(f'<path d="M{x-4},-2.2 Q{x},1.2 {x+4},-2.2" fill="none" stroke="{EYE}" stroke-width="2" stroke-linecap="round"/>')
        elif eyes == "squeeze":  # > <
            d = 1 if x < 0 else -1
            g.append(f'<path d="M{x-3*d},-6 L{x+3*d},-2.4 L{x-3*d},1.2" fill="none" stroke="{EYE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        elif eyes == "swirl":
            g.append(f'<path d="M{x},-2.4 m-0.8,0 a0.8,0.8 0 1 1 1.6,0 a1.8,1.8 0 1 1 -3.6,0 a2.8,2.8 0 1 1 5.6,0 a3.8,3.8 0 1 1 -7.6,0" fill="none" stroke="{EYE}" stroke-width="1.5" stroke-linecap="round"/>')
        elif eyes == "x":
            g.append(f'<path d="M{x-3},-5.4 L{x+3},0.6 M{x+3},-5.4 L{x-3},0.6" stroke="{EYE}" stroke-width="2" stroke-linecap="round"/>')
    if mouth == "w":
        g.append(f'<path d="M-2.6,3.4 Q-1.3,5.4 0,3.6 Q1.3,5.4 2.6,3.4" fill="none" stroke="{L}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')
    elif mouth == "o":
        g.append(f'<ellipse cx="0" cy="4.4" rx="1.9" ry="2.2" fill="{MOUTH}" stroke="{L}" stroke-width="1.2"/><ellipse cx="0" cy="5.4" rx="1" ry="0.7" fill="#FFC4D4"/>')
    elif mouth == "grin":
        g.append(f'<path d="M-3.4,3 Q0,8 3.4,3 Z" fill="{MOUTH}" stroke="{L}" stroke-width="1.2" stroke-linejoin="round"/>')
    elif mouth == "wobble":
        g.append(f'<path d="M-3,4.4 q1,-1.4 2,0 q1,1.4 2,0 q1,-1.4 2,0" fill="none" stroke="{L}" stroke-width="1.3" stroke-linecap="round"/>')
    return "".join(g) + "</g>"
def mitten(x, y, rot, trim):
    return f'<g transform="translate({x},{y}) rotate({rot})"><ellipse cx="0" cy="0" rx="4.4" ry="3.6" fill="url(#red)" {st(1.6)}/><ellipse cx="-3.6" cy="0" rx="1.6" ry="2.6" fill="{trim}" {st(1.2)}/></g>'
def jet(x, y, ang, Ln, w, cols, seed=0, spikes=0):
    """flame from nozzle (x,y) along ang; spikes > 0 adds flickering outer tongues (boost)"""
    o, m, c = cols; r = random.Random(seed)
    def tear(l, ww, col, op=1.0, ex=""):
        return (f'<path d="M0,{-ww/2:.1f} C{l*0.45:.1f},{-ww/2:.1f} {l*0.8:.1f},{-ww*0.2:.1f} {l:.1f},0 C{l*0.8:.1f},{ww*0.2:.1f} {l*0.45:.1f},{ww/2:.1f} 0,{ww/2:.1f} '
                f'C{-ww*0.35:.1f},{ww/2:.1f} {-ww*0.35:.1f},{-ww/2:.1f} 0,{-ww/2:.1f} Z" fill="{col}" opacity="{op}" {ex}/>')
    g = f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang})">'
    for i in range(spikes):  # outer tongues, randomised per frame = flicker
        a = r.uniform(-28, 28); l = Ln * r.uniform(0.55, 0.9)
        g += f'<g transform="rotate({a:.0f})">' + tear(l, w * 0.45, o, 0.85) + '</g>'
    g += tear(Ln, w, o, 1, f'stroke="#E8875A" stroke-width="1"') + tear(Ln * 0.7, w * 0.68, m) + tear(Ln * 0.4, w * 0.4, c, 0.95)
    return g + "</g>"
NOZ = [(12, 48), (19, 48)]   # nozzle points in the 64-unit body space (bottom of the gift box)
def body(v="normal", eyes="open", mouth="w", tip=(16, 13), sack_dy=0, mit=(48, 43, -20), cuff=True, soot=0.0, frost=False):
    """Santa C in the 64-unit space of the concept (body centre ~ (35, 35.5))"""
    t = VAR[v]["trim"]; g = []
    rib = GOLD if v != "rush" else "#FFF0A0"
    g.append(f'<rect x="7" y="26" width="17" height="19" rx="3" fill="{MINT}" {st(1.8)}/><rect x="13.5" y="26" width="4" height="19" fill="{rib}" {st(1)}/>'
             f'<rect x="7" y="33.5" width="17" height="4" fill="{rib}" {st(1)}/>'
             f'<path d="M15.5,26 Q10,19 12,24 Q11,27 15.5,26 Q21,19 19,24 Q20,27 15.5,26 Z" fill="{rib}" {st(1.3)}/>'
             f'<rect x="9.5" y="45" width="5" height="3" rx="1" fill="{GOLD2}" {st(1.1)}/><rect x="16.5" y="45" width="5" height="3" rx="1" fill="{GOLD2}" {st(1.1)}/>')
    g.append(f'<path d="M20,30 C20,20 26,14 35,14 C44,14 50,20 50,30 L50,46 C50,53 46,57 41,57 L29,57 C24,57 20,53 20,46 Z" fill="url(#red)" {st(2.2)}/>')
    g.append(f'<path d="M21,46 Q35,51 49,46" fill="none" stroke="{t}" stroke-width="4" stroke-linecap="round"/><path d="M21,46 Q35,51 49,46" fill="none" stroke="{L}" stroke-width="1" opacity="0.4"/>')
    g.append(f'<ellipse cx="30" cy="58" rx="3.4" ry="2.2" fill="{BOOT}"/><ellipse cx="40" cy="58" rx="3.4" ry="2.2" fill="{BOOT}"/>')
    g.append(f'<ellipse cx="35.5" cy="30" rx="13" ry="11.6" fill="{t}" {st(1.8)}/><ellipse cx="35.5" cy="30.6" rx="10.4" ry="9.2" fill="url(#skin)" {st(1.2)}/>')
    g.append(f'<path d="M30,37.6 Q35.5,41.5 41,37.6 Q39,40.6 35.5,40.8 Q32,40.6 30,37.6 Z" fill="#FFFFFF" {st(1.1)}/>')
    g.append(face(35.5, 29.4, 0.62, eyes, mouth))
    if tip: g.append(f'<path d="M27,17 Q22,10 {tip[0]+2},{tip[1]}" fill="none" stroke="{L}" stroke-width="7" stroke-linecap="round"/><path d="M27,17 Q22,10 {tip[0]+2},{tip[1]}" fill="none" stroke="{RED2}" stroke-width="4.2" stroke-linecap="round"/>'
             + pompom(tip[0], tip[1], 3.3).replace(f'fill="{FUR}"', f'fill="{t}"'))
    else: g.append(f'<path d="M25,19 Q28,15 32,15" fill="none" stroke="{L}" stroke-width="1.4" stroke-linecap="round"/>')  # hood top, tip gone
    if soot:  # soot smudges over suit, fur and face
        for (x, y, rx, ry) in ((27, 24, 6, 4), (44, 22, 5, 3.5), (30, 46, 7, 3), (43, 50, 6, 4), (31, 34, 2.6, 1.8), (41, 26, 2.4, 1.6), (24, 38, 3.5, 5), (47, 34, 3, 4), (36, 18, 6, 2.6), (14, 32, 4, 5)):
            g.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#3E3650" opacity="{0.78*soot:.2f}"/>')
    if frost:
        g.append(f'<path d="M22,18 q3,3 6,0 q3,3 6,0" fill="none" stroke="#E6F6FF" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="13" r="2.2" fill="#E6F6FF"/>')
    g.append(sack(50, 50 + sack_dy, 0.7, 10) + mitten(mit[0], mit[1], mit[2], t))
    return "".join(g)
BC = (35, 36)  # body centre for squash/stretch
def hero(v, dy=0, sx=1, sy=1, tilt=0, flameL=11, flameW=6, spikes=0, seed=0, eyes="open", mouth="w", tip=(16, 13), sack_dy=0, mit=(48, 43, -20), aura_r=34, sparkles=()):
    """96x96 frame; body shifted so its hitbox centre lands on (48,49)"""
    uid = f"{v}{seed}{int(dy*10)}{int(sx*100)}"
    cols = VAR[v]["flame"]; g = [defs(v, uid)]
    if VAR[v]["aura"]: g.append(f'<circle cx="48" cy="{49+dy}" r="{aura_r}" fill="url(#aura{uid})"/>')
    inner = "".join(jet(x, y, 112 + i * 6, flameL * (1 if i else 0.92), flameW, cols, seed * 7 + i, spikes) for i, (x, y) in enumerate(NOZ))
    inner += body(v, eyes, mouth, tip, sack_dy, mit)
    sq = f"translate({BC[0]},{BC[1]}) scale({sx},{sy}) translate({-BC[0]},{-BC[1]})"
    g.append(f'<g transform="translate(13,{13.5+dy}) rotate({tilt} {BC[0]} {BC[1]}) {sq}">{inner}</g>')
    for (x, y, r, op) in sparkles: g.append(K.sparkle(x, y, r, VAR[v]["spk"], "#D9953A" if v != "chill" else "#6FA8D6", op) if hasattr(K, "sparkle") else spark(x, y, r, VAR[v]["spk"], op, v))
    return svg(96, 128, "".join(g))
def spark(x, y, r, fill, op, v="normal"):
    k = r * 0.28; line = {"chill": "#6FA8D6", "life": "#D9708F"}.get(v, "#D9953A")
    return (f'<path d="M{x},{y-r} Q{x+k},{y-k} {x+r},{y} Q{x+k},{y+k} {x},{y+r} Q{x-k},{y+k} {x-r},{y} Q{x-k},{y-k} {x},{y-r} Z" '
            f'fill="{fill}" stroke="{line}" stroke-width="0.9" stroke-linejoin="round" opacity="{op}"/>')
VSPARK = {  # twinkles that move per frame for the variants (like the golden ghost)
  0: [(14, 22, 3.4, 1), (80, 18, 2.4, .85), (82, 66, 2.6, .8)], 1: [(16, 24, 2.4, .8), (79, 20, 3.4, 1), (12, 62, 2.2, .85)],
  2: [(13, 26, 3, 1), (81, 64, 3, .95), (78, 16, 2, .8)], 3: [(18, 20, 2.6, .9), (82, 22, 3, 1), (14, 66, 2.6, .9)]}

IDLE = [dict(dy=0, flameL=14, flameW=7.4), dict(dy=-1, flameL=15.5, flameW=7.8, tip=(16, 12)),
        dict(dy=-2, flameL=14.5, flameW=7.4, tip=(16, 11.5), eyes="blink"), dict(dy=-1, flameL=16, flameW=8, tip=(16, 12))]
BOOST = [dict(sx=1.14, sy=0.86, dy=2, tilt=-4, flameL=17, flameW=9, spikes=3, eyes="squeeze", mouth="o", tip=(17, 15), sack_dy=2, mit=(48, 44, -10)),   # squash + ignition
         dict(sx=0.88, sy=1.14, dy=-3, tilt=-12, flameL=31, flameW=13.5, spikes=5, eyes="open", mouth="o", tip=(13, 9), sack_dy=3, mit=(48, 38, -40)),    # stretch, full burst
         dict(sx=0.94, sy=1.07, dy=-2, tilt=-10, flameL=27, flameW=12, spikes=5, eyes="happy", mouth="grin", tip=(14, 10), sack_dy=2, mit=(48, 39, -36)),
         dict(sx=1.0, sy=1.0, dy=-1, tilt=-7, flameL=19, flameW=9, spikes=3, eyes="happy", mouth="grin", tip=(15, 11.5), sack_dy=1, mit=(48, 41, -26))]
def build_hero():
    for v in VAR:
        pre = "santa-c" if v == "normal" else f"santa-c-{v}"
        for name, seq in (("idle", IDLE), ("boost", BOOST)):
            STRIPS[f"{pre}-{name}"] = []
            for i, f in enumerate(seq):
                kw = dict(f); kw.setdefault("seed", i + (10 if name == "boost" else 0))
                if v != "normal": kw["sparkles"] = VSPARK[i]; kw["aura_r"] = 36 if name == "idle" else 40
                FILES[f"{pre}-{name}-{i}"] = hero(v, **kw); STRIPS[f"{pre}-{name}"].append(f"{pre}-{name}-{i}")

# ---- fx: boost trail (sparkles + snow puffs drifting back from the nozzle) ----
def trail(i, n=10):
    t = i / (n - 1); ex, ey = 144, 64; g = []; r = random.Random(5)
    fade = lambda base: max(0.0, min(1.0, base * (1.0 - max(0.0, t - 0.45) / 0.55)))
    for k in range(14):  # snow puffs (grow, drift back + sink a little)
        a = math.radians(r.uniform(160, 200)); sp = r.uniform(45, 110); d = sp * (0.15 + 0.85 * t) + 6
        size = r.uniform(6, 10) * (0.8 + 0.7 * t)
        x, y = ex + math.cos(a) * d, ey + math.sin(a) * d + 10 * t
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size:.1f}" fill="#FFFFFF" stroke="#B9B0E0" stroke-width="1.6" opacity="{fade(1.0):.2f}"/>')
    for k in range(12):  # sparkles
        a = math.radians(r.uniform(150, 210)); d = r.uniform(20, 120) * (0.15 + 0.85 * t) + 4; x, y = ex + math.cos(a) * d, ey + math.sin(a) * d
        rr = r.uniform(4, 6.5) * (1 - 0.35 * t) * (1.2 if (i + k) % 2 else 0.85)
        g.append(spark(round(x, 1), round(y, 1), round(rr, 1), "#FFF4B8", fade(1.0)))
    for k in range(6):  # snowflakes
        a = math.radians(r.uniform(150, 210)); d = r.uniform(30, 110) * (0.2 + 0.8 * t); x, y = ex + math.cos(a) * d, ey + math.sin(a) * d
        g.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({30*i + k*20})" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="{fade(0.95):.2f}"><path d="M-5,0 H5 M-2.5,-4.3 L2.5,4.3 M2.5,-4.3 L-2.5,4.3"/></g>')
    return svg(160, 128, "".join(g))
def build_fx():
    STRIPS["fx-santa-boost-trail"] = []
    for i in range(10): FILES[f"fx-santa-boost-trail-{i}"] = trail(i); STRIPS["fx-santa-boost-trail"].append(f"fx-santa-boost-trail-{i}")

# ---- deaths: 128x128, anchor (64,64) = hero anchor (48,48) + 16 ----
def dhero(v="normal", rot=0, s=1.0, dx=0, dy=0, sx=1, sy=1, op=1, **kw):
    inner = body(v, **kw)
    sq = f"translate({BC[0]},{BC[1]}) scale({sx},{sy}) translate({-BC[0]},{-BC[1]})"
    return f'<g opacity="{op}" transform="translate({29+dx},{29.5+dy}) translate({BC[0]},{BC[1]}) rotate({rot}) scale({s}) translate({-BC[0]},{-BC[1]}) {sq}">{inner}</g>'
def bonk(x, y, r):
    pts = " ".join(f"{x + (r if k % 2 == 0 else r*0.45)*math.cos(math.radians(k*36-90)):.1f},{y + (r if k % 2 == 0 else r*0.45)*math.sin(math.radians(k*36-90)):.1f}" for k in range(10))
    return f'<polygon points="{pts}" fill="#FFF4B8" {st(1.8)}/>'
def star_ring(cx, cy, ph, n=3):
    return "".join(spark(round(cx + 20 * math.cos(ph + k * 2 * math.pi / n), 1), round(cy + 6 * math.sin(ph + k * 2 * math.pi / n), 1), 4.2, "#FFE08A", 1) for k in range(n))
def puff(x, y, r, op): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F3EEFC" stroke="#C9C2E8" stroke-width="1.2" opacity="{op}"/>'
def build_deaths():
    D = defs("normal", "d")
    # generic: bonk (0), dizzy spin + shrink (1-6), sparkle poof (7-9)
    seq = []
    for i in range(10):
        g = [D]
        if i == 0: g += [dhero(eyes="squeeze", mouth="o", sx=1.08, sy=0.92), bonk(92, 40, 12)]
        elif i <= 6:
            k = i / 6; g.append(dhero(eyes="swirl", mouth="wobble", rot=60 * i, s=1 - 0.5 * k, dy=-6 * k))
            if i < 4: g.append(star_ring(64, 40 - 6 * k, i * 1.2))
        else:
            k = (i - 6) / 3
            if i == 7: g.append(dhero(eyes="swirl", mouth="wobble", rot=420, s=0.42, dy=-7, op=0.6))
            for j in range(8):
                a = j * math.pi / 4 + 0.3; d = 10 + 28 * k
                g.append(spark(round(64 + d * math.cos(a), 1), round(58 + d * math.sin(a), 1), round(5.5 * (1.1 - k * 0.7), 1), "#FFF4B8", max(0.05, 1 - k * 0.85)))
            g.append(puff(64, 58, 8 + 10 * k, max(0, 0.7 - k * 0.7)))
        seq.append(svg(128, 128, "".join(g)))
    STRIPS["death-santa-generic"] = []
    for i, s in enumerate(seq): FILES[f"death-santa-generic-{i}"] = s; STRIPS["death-santa-generic"].append(f"death-santa-generic-{i}")
    # floor: splat + dust (0), bounce (1), flop (2-3), lying on its side x_x (4-7); floor line y=95
    floor = '<path d="M8,95 H120" stroke="#C9C2E8" stroke-width="2" stroke-dasharray="4 6" stroke-linecap="round" opacity="0.6"/>'
    FL = [dict(sx=1.3, sy=0.72, dy=14, eyes="squeeze", mouth="o"), dict(sx=0.92, sy=1.1, dy=-2, rot=-10, eyes="swirl", mouth="o"),
          dict(rot=45, dy=8, eyes="swirl", mouth="wobble"), dict(rot=80, dy=12, sx=1.04, sy=0.96, eyes="x", mouth="wobble")]
    FL += [dict(rot=90, dy=13, eyes="x", mouth="wobble")] * 4
    STRIPS["death-santa-floor"] = []
    for i, f in enumerate(FL):
        g = [D, floor, dhero(**f)]
        if i == 0: g += [puff(34, 92, 7, 0.9), puff(94, 92, 7, 0.9), puff(24, 88, 4, 0.7), puff(104, 88, 4, 0.7)]
        if i == 1: g += [puff(26, 90, 5, 0.6), puff(102, 90, 5, 0.6)]
        if i >= 4:  # jetpack sputters: tiny smoke rising
            k = (i - 4) / 3; g += [puff(round(44 - 2 * k, 1), round(56 - 14 * k, 1), round(3 + 3 * k, 1), round(0.8 - 0.5 * k, 2)), puff(round(50 + 2 * k, 1), round(46 - 12 * k, 1), 2.5, round(0.6 - 0.4 * k, 2))]
        FILES[f"death-santa-floor-{i}"] = svg(128, 128, "".join(g)); STRIPS["death-santa-floor"].append(f"death-santa-floor-{i}")
    # ---- Santa-world deaths (replace the ghost-world tombstone) ----
    def put(name, frames):
        STRIPS[name] = []
        for i, g in enumerate(frames): FILES[f"{name}-{i}"] = svg(128, 128, D + "".join(g)); STRIPS[name].append(f"{name}-{i}")
    # icicle (12f, 1.0 s): ice flash (0), block freezes up around him (1-3), frozen + shiver (4-7), cracks (8-9), shatters, shivering (10-11)
    fr = []
    def block(h, op=0.55):  # translucent ice block, grows from the bottom (y 98) up
        top = 98 - h
        return (f'<rect x="30" y="{top:.1f}" width="68" height="{h:.1f}" rx="8" fill="#BFE6FF" opacity="{op}" {st(2)}/>'
                f'<path d="M38,{top+6:.1f} V{min(96, top + h*0.6):.1f} M46,{top+4:.1f} V{min(96, top+h*0.35):.1f}" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.7"/>')
    def shards(k):
        out = ""
        for j in range(9):
            a = math.radians(-160 + j * 40); d = 26 + 34 * k
            x, y = 64 + d * 0.85 * math.cos(a), 62 + d * 0.8 * math.sin(a) + 6 * k * k
            out += f'<path d="M{x:.1f},{y-5:.1f} L{x+4:.1f},{y+3:.1f} L{x-4:.1f},{y+4:.1f} Z" fill="#DDF1FF" {st(1.2)} opacity="{max(0, 1-k*0.6):.2f}" transform="rotate({j*37+k*90:.0f} {x:.1f} {y:.1f})"/>'
        return out
    fr.append([dhero(eyes="squeeze", mouth="o", sx=1.06, sy=0.94), bonk(70, 26, 12).replace("#FFF4B8", "#DDF1FF")])
    for i, h in enumerate((24, 50, 74)): fr.append([dhero(eyes="squeeze", mouth="o", dx=0.6 * (-1) ** i), block(h)])
    for i in range(4): fr.append([dhero(eyes="blink", mouth="wobble", frost=True, dx=(1 if i % 2 else -1)), block(74, 0.6), spark(34, 26, 4, "#FFFFFF", 0.9 if i % 2 else 0.4), spark(96, 60, 3.4, "#FFFFFF", 0.4 if i % 2 else 0.9)])
    crack1 = f'<path d="M64,24 L58,40 L66,50 L60,64" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M64,24 L58,40 L66,50 L60,64" fill="none" stroke="{L}" stroke-width="1" opacity="0.6"/>'
    crack2 = crack1 + f'<path d="M58,40 L42,46 M66,50 L86,44 L92,58 M60,64 L70,82" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"/>'
    fr.append([dhero(eyes="squeeze", mouth="wobble", frost=True), block(74, 0.6), crack1])
    fr.append([dhero(eyes="squeeze", mouth="wobble", frost=True, dx=1), block(74, 0.6), crack2])
    fr.append([dhero(eyes="swirl", mouth="o", frost=True, rot=-6), shards(0.2)])
    fr.append([dhero(eyes="swirl", mouth="wobble", frost=True, rot=6, dy=2), shards(0.75), spark(40, 30, 4, "#E6F6FF", 0.9), spark(90, 36, 3.4, "#E6F6FF", 0.9)])
    put("death-santa-icicle", fr)
    # chimney (12f, 1.0 s): bonk (0), squash (1), soot cloud bursts (2-3), sooty Santa blinks + coughs a puff (4-11)
    fr = []
    soot = lambda x, y, r, op: f'<circle cx="{x}" cy="{y}" r="{r}" fill="#5B536B" stroke="#3B3448" stroke-width="1.2" opacity="{op}"/>'
    fr.append([dhero(eyes="squeeze", mouth="o", sx=1.1, sy=0.9, dy=2), bonk(64, 98, 13)])
    fr.append([dhero(eyes="squeeze", mouth="o", sx=1.18, sy=0.82, dy=6), bonk(64, 100, 9)])
    fr.append([dhero(eyes="swirl", mouth="o", soot=0.6, dy=2)] + [soot(64 + 22 * math.cos(j), 62 + 20 * math.sin(j), 10, 0.85) for j in range(0, 7)])
    fr.append([dhero(eyes="swirl", mouth="o", soot=1.0)] + [soot(round(64 + 34 * math.cos(j + 0.4), 1), round(60 + 30 * math.sin(j + 0.4), 1), 12, 0.5) for j in range(0, 7)])
    for i in range(8):
        eyes = "blink" if i in (2, 6) else "open"; mouth = "o" if i in (3, 4) else "wobble"
        g = [dhero(eyes=eyes, mouth=mouth, soot=1.0, rot=3 * math.sin(i))]
        if i in (3, 4, 5):  # cough puff from the mouth, drifting up-right
            k = (i - 3) / 2; g.append(soot(round(84 + 10 * k, 1), round(58 - 12 * k, 1), round(5 + 4 * k, 1), round(0.9 - 0.5 * k, 2)))
        if i < 3: g.append(soot(40 - 3 * i, 30 - 6 * i, 6 + i, 0.4 - 0.1 * i))
        fr.append(g)
    put("death-santa-chimney", fr)
    # pigeon (14f, 1.17 s): pigeon swoops in (0-2), snatches the hood tip (3), flaps off up-right with it (4-13) while Santa tumbles down and out
    fr = []
    def bird(x, y, up, hat=False, rot=0, op=1.0, sc=0.9):
        wing = (f'<path d="M-6,-2 Q-16,-20 -2,-14 Q3,-8 -6,-2 Z" fill="#A9A3C9" {st(1.5)}/>' if up else f'<path d="M-6,0 Q-18,10 -4,8 Q2,5 -6,0 Z" fill="#A9A3C9" {st(1.5)}/>')
        h = (f'<path d="M-1,16 L1,23 M5,16 L5,23" stroke="{GOLD2}" stroke-width="1.8" stroke-linecap="round"/><g transform="translate(3,28) rotate(-15)"><path d="M-9,-4 Q-6,-9 0,-8 Q8,-7 14,2 Q6,0 2,4 Q-4,6 -9,-4 Z" fill="url(#red)" {st(1.5)}/><rect x="-10" y="-6" width="12" height="5" rx="2.5" fill="{FUR}" {st(1.2)} transform="rotate(20)"/>{pompom(15, 3, 3.2)}</g>' if hat else "")
        base = K.pigeon(0, 0).replace(f'<path d="M-5,-2 Q-12,-14 -2,-10 Q2,-6 -5,-2 Z" fill="#A9A3C9" {st(1.5)}/>', "")
        return f'<g opacity="{op:.2f}" transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sc})">{base}{wing}{h}</g>'
    path_in = [(104, 34, 0.35), (92, 32, 0.75), (78, 32, 1.0)]  # fades in inside the canvas (no hard edge cut)
    for i, (x, y, o) in enumerate(path_in): fr.append([dhero(eyes="open" if i < 2 else "squeeze", mouth="w" if i < 2 else "o"), bird(x, y, i % 2 == 0, op=o)])
    fr.append([dhero(eyes="squeeze", mouth="o", tip=None, rot=-8), bird(58, 30, False, True), spark(40, 18, 4, "#FFF4B8", 1)])
    for i in range(10):
        k = (i + 1) / 10
        bx, by = 58 + 42 * k, 30 - 2 * k
        sy = 6 + 34 * k * k; fo = 1.0 if k < 0.6 else max(0.0, 1 - (k - 0.6) / 0.4)
        fr.append([dhero(eyes="swirl", mouth="wobble", tip=None, rot=-30 * (i + 1), dy=sy, s=1 - 0.35 * k, op=fo),
                   bird(bx, by, i % 2 == 0, True, -10, op=fo, sc=0.9 - 0.35 * k)])
    put("death-santa-pigeon", fr)
    # plane (12f, 1.0 s): a little plane + contrail whoosh streaks across (0-1), hit (2), Santa spins off up-left inside swirling contrail, shrinking (3-11)
    fr = []
    def plane(x, y, op=1.0):
        return (f'<g opacity="{op}" transform="translate({x},{y})"><path d="M-14,0 Q-14,-6 -4,-6 H12 Q20,-4 20,0 Q20,4 12,6 H-4 Q-14,6 -14,0 Z" fill="#FFFFFF" {st(1.6)}/>'
                f'<path d="M0,-5 L-8,-16 L-3,-16 L8,-5 Z M0,5 L-6,13 L-2,13 L8,5 Z M-12,-4 L-17,-12 L-13,-12 L-8,-5 Z" fill="#BFE6FF" {st(1.4)}/>'
                + "".join(f'<circle cx="{cx}" cy="-1" r="1.6" fill="#7FB6E0"/>' for cx in (2, 7, 12)) + '</g>')
    CT = ('<linearGradient id="ct" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="128" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
          '<stop offset="0.2" stop-color="#FFFFFF" stop-opacity="1"/><stop offset="0.8" stop-color="#FFFFFF" stop-opacity="1"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
    def contrail(x0, x1, y, op, w=9):  # fades out towards both canvas edges (no hard cut)
        x0, x1 = max(x0, 12), min(x1, 116)
        return (CT + f'<path d="M{x0},{y} H{x1}" stroke="url(#ct)" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
                f'<path d="M{x0},{y} H{x1}" stroke="#E6DDF7" stroke-width="{w*0.35:.1f}" stroke-linecap="round" opacity="{op*0.5:.2f}"/>')
    fr.append([dhero(), contrail(4, 14, 44, 0.9), plane(28, 44, 0.6)])
    fr.append([dhero(eyes="squeeze", mouth="o"), contrail(-20, 60, 46, 0.9), plane(76, 46)])
    fr.append([dhero(eyes="swirl", mouth="o", rot=-40, sx=0.9, sy=1.1), contrail(-20, 128, 48, 0.85), plane(104, 48, 0.35), bonk(70, 44, 10)])
    for i in range(9):
        k = (i + 1) / 9
        swirl = f'<path d="M{64-40*k:.1f},{60-36*k:.1f} m-14,0 a14,10 0 1 1 28,0" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="{0.8 - 0.6*k:.2f}" transform="rotate({-60*i} {64-40*k:.1f} {60-36*k:.1f})"/>'
        fr.append([contrail(-20, 128, 48, max(0, 0.75 - k * 0.7), 9 + 8 * k), swirl,
                   dhero(eyes="swirl", mouth="wobble", rot=-80 * (i + 1) - 40, dx=-40 * k, dy=-36 * k, s=1 - 0.55 * k, op=1 if i < 7 else 0.5)])
    put("death-santa-plane", fr)

def export():
    for d in ("png/1x", "png/2x"): os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for k, v in FILES.items():
        p = os.path.join(OUT, k + ".svg"); open(p, "w").write(v)
        for sc, d in ((1, "png/1x"), (2, "png/2x")): cairosvg.svg2png(url=p, write_to=os.path.join(OUT, d, k + ".png"), scale=sc)
    for name, frames in STRIPS.items():
        for d in ("png/1x", "png/2x"):
            ims = [Image.open(os.path.join(OUT, d, f + ".png")).convert("RGBA") for f in frames]
            sh = Image.new("RGBA", (ims[0].width * len(ims), ims[0].height), (0, 0, 0, 0))
            for i, im in enumerate(ims): sh.alpha_composite(im, (i * im.width, 0))
            sh.save(os.path.join(OUT, d, name + "-strip.png"), optimize=True)

FPS = {"idle": 8, "boost": 16, "fx-santa-boost-trail": 16, "death": 12}
def sheet():
    F = ImageFont.truetype(K.FONT, 24); FS = ImageFont.truetype(K.FONT, 14); FT = ImageFont.truetype(K.FONT, 34)
    rows = [("santa-c-idle", "Idle loop: 4f @ 8 fps (96x128, anchor 48,48)", 2), ("santa-c-boost", "Boost on tap: 4f @ 16 fps, play once (squash -> stretch -> burst)", 2),
            ("fx-santa-boost-trail", "fx-santa-boost-trail: 10f @ 16 fps (0.63 s), 160x128, emitter (144,64)", 2)]
    for v in ("rush", "life", "chill"):
        rows += [(f"santa-c-{v}-idle", f"{v.capitalize()} bauble ({ {'rush': 'gold', 'life': 'red', 'chill': 'blue'}[v] }): idle 4f @ 8 fps", 1), (f"santa-c-{v}-boost", f"{v.capitalize()}: boost 4f @ 16 fps", 1)]
    rows += [("death-santa-generic", "death generic: 10f @ 12 fps (128x128, anchor 64,64)", 1), ("death-santa-floor", "death floor: 8f @ 12 fps (floor line y=95)", 1),
             ("death-santa-icicle", "death icicle: 12f @ 12 fps (freeze in an ice block -> cracks -> shatters)", 1),
             ("death-santa-chimney", "death chimney: 12f @ 12 fps (bonk -> soot burst -> sooty, coughs a puff)", 1),
             ("death-santa-pigeon", "death pigeon: 14f @ 12 fps (pigeon snatches the hood tip, Santa tumbles out)", 1),
             ("death-santa-plane", "death plane: 12f @ 12 fps (contrail whoosh spins him off)", 1)]
    W = 1600; y = 80; layout = []
    for name, label, sc in rows:
        strip = Image.open(os.path.join(OUT, f"png/{sc}x", name + "-strip.png")).convert("RGBA")
        if strip.width > W - 60: strip = strip.resize((W - 60, round(strip.height * (W - 60) / strip.width)), Image.LANCZOS)
        layout.append((label, strip, y)); y += 34 + strip.height + 24
    im = Image.new("RGBA", (W, y + 10), "#2B2347"); d = ImageDraw.Draw(im)
    d.text((30, 22), "Santa C: hooded chibi + gift-box jetpack (sprite set, concept folder)", font=FT, fill="#FFE08A")
    for label, strip, yy in layout:
        d.text((30, yy), label, font=F, fill="#FFFFFF")
        n = len([1 for _ in range(1)])
        plate = Image.new("RGBA", strip.size, "#4B4682"); plate.alpha_composite(strip); im.alpha_composite(plate, (30, yy + 34))
    p = os.path.join(SANTA, "santa-c-sprites.png")
    im.convert("RGB").quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(p, optimize=True); return p

# ---- boost preview: 4 s @ 24 fps over the London mock (Santa A removed); loops seamlessly ----
def preview():
    S = 2; W, H = 360 * S, 640 * S; fps = 24; T = 4.0; N = int(T * fps)
    bg = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=K.mock(hero=False, path=True).encode(), output_width=W, output_height=H))).convert("RGBA")
    load = lambda n: Image.open(os.path.join(OUT, "png/2x", n + ".png")).convert("RGBA")
    PAD = 400  # pad each 192x256 (2x) hero frame onto a 400x400 square centred on the anchor, so rotation never clips the flame
    def padded(im):
        sq = Image.new("RGBA", (PAD, PAD), (0, 0, 0, 0)); sq.alpha_composite(im, (PAD // 2 - 96, PAD // 2 - 96)); return sq
    idle = [padded(load(f"santa-c-idle-{i}")) for i in range(4)]; boost = [padded(load(f"santa-c-boost-{i}")) for i in range(4)]
    tr = [load(f"fx-santa-boost-trail-{i}") for i in range(10)]
    taps = [1.0, 1.55, 2.15, 2.85]; X = 120; y0 = 330.0; g_, imp = 900.0, -260.0
    ys, vs = [], []; y, v = y0, 0.0
    for f in range(N):
        t = f / fps
        if t < taps[0]: y = y0 + 3 * math.sin(t * 2 * math.pi); v = 0.0
        else:
            for tp in taps:
                if abs(t - tp) < 0.5 / fps: v = imp
            v += g_ / fps; y += v / fps
        ys.append(y); vs.append(v)
    tilts = []
    for f in range(N):
        t = f / fps
        tl = 0.0 if t < taps[0] else max(-20.0, min(25.0, vs[f] / 14))
        if any(0 <= t - tp < 4 / 16 for tp in taps): tl = min(tl, -6.0)
        tilts.append(tl)
    E0 = T - 0.75  # ease y AND tilt back to the hover pose over the last 0.75 s -> frame N-1 flows into frame 0
    for f in range(N):
        t = f / fps
        if t > E0:
            k = (t - E0) / (T - E0); k = k * k * (3 - 2 * k)
            ys[f] = ys[f] * (1 - k) + (y0 + 3 * math.sin(t * 2 * math.pi)) * k; tilts[f] *= (1 - k)
    tmp = "/tmp/santa_frames"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    scroll = 120.0; emits = []
    for f in range(N):
        t = f / fps; fr = bg.copy(); bf = None
        for i, tp in enumerate(taps):
            if 0 <= t - tp < 4 / 16: bf = int((t - tp) * 16)
            if 0 <= t - tp < 1.0 / fps and not any(e[0] == i for e in emits):
                a = math.radians(tilts[f]); ox, oy = -23, 13.5  # nozzle offset from the anchor (1x), rotated with the tilt
                emits.append((i, tp, X + ox * math.cos(a) - oy * math.sin(a), ys[f] + ox * math.sin(a) + oy * math.cos(a)))
        for i, tp, ex, ey in emits:  # trail first = behind Santa; it scrolls back with the world
            k = int((t - tp) * 16)
            if 0 <= k < len(tr):
                px = ex - (t - tp) * scroll; fr.alpha_composite(tr[k], (round((px - 144) * S), round((ey - 64) * S)))
        spr = boost[bf] if bf is not None else idle[int(t * 8) % 4]
        spr = spr.rotate(-tilts[f], resample=Image.BICUBIC, center=(PAD // 2, PAD // 2))
        fr.alpha_composite(spr, (round(X * S) - PAD // 2, round(ys[f] * S) - PAD // 2))
        fr.convert("RGB").save(os.path.join(tmp, f"f{f:03d}.png"))
    mp4 = os.path.join(SANTA, "santa-c-boost-preview.mp4"); gif = os.path.join(SANTA, "santa-c-boost-preview.gif")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%03d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-profile:v", "high", "-crf", "20", "-movflags", "+faststart", mp4], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(tmp, "f%03d.png"), "-vf",
                    "fps=12,scale=360:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                    "-loop", "0", gif], check=True)
    return mp4, gif

if __name__ == "__main__":
    build_hero(); build_fx(); build_deaths(); export()
    p = sheet(); m, g = preview()
    for f in (p, m, g): print(f, os.path.getsize(f))
    print(len(FILES), "svgs;", len(STRIPS), "strips")
