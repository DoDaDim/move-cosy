"""Santa pack v0.8.0 art fill-in: event sheets, golden Santa C, scorecard, sleigh hop, hero fx, 2x HUD, badge 9, confetti.
Writes ../v080/{svg,png/1x,png/2x} and COPIES the PNGs into packs/santa/assets/png/{1x,2x}; merges JSON sections
(events, cutscene, fx, confetti) into packs/santa/assets/santa-hitboxes.json + ../stages/santa-hitboxes.json.
Scorecard frame -> packs/santa/assets/ui-santa-scorecard-frame.png (600x800) + @2x + santa-scorecard-layout.json.
Run AFTER build_santa_stages.py (which rewrites stages/santa-hitboxes.json). Script SVG only, no AI imagery."""
import os, sys, json, math, random, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from santa_lib import *
import santa_lib as SL
import build_santa_c as BC
from build_santa_stages import bird, reindeer, badge, heart, text2
TOOLS = os.path.dirname(os.path.abspath(__file__)); SANTA = os.path.dirname(TOOLS)
ROOT = os.path.abspath(os.path.join(SANTA, "../../.."))
PACK = os.path.join(ROOT, "packs/santa/assets"); OUTD = os.path.join(SANTA, "v080")
SL.OUT = OUTD; SL.FILES.clear(); SL.STRIPS.clear()
F, S, J = SL.FILES, SL.STRIPS, {"events": {}, "cutscene": {}, "fx": {}, "confetti": {}}
def strip(base, frames_svg):
    S[base] = []
    for i, s in enumerate(frames_svg): F[f"{base[:-6]}-{i}"] = s; S[base].append(f"{base[:-6]}-{i}")
def flip(w, inner): return f'<g transform="translate({w},0) scale(-1,1)">{inner}</g>'
def glow(x, y, r, col, op=0.5, uid="g"):
    return (f'<defs><radialGradient id="{uid}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#{uid})"/>')

# ======================= 1. EVENTS =======================
# Reindeer stampede (Lapland, laneWave, flies right->left in the sky: a real flying-reindeer formation, no anchor needed)
def rein_ev(f):
    trail = "".join(sparkle(37 + i * 2.5, 30 - i * 3 + (f % 2), 2.2 - i * 0.5, "#FFF4B8", "#D9953A", 0.9 - i * 0.25) for i in range(3))
    return glow(20, 20, 19, "#FFF4B8", 0.35, f"rg{f}") + flip(40, reindeer(f)) + trail
strip("event-santa-reindeer-strip", [svg(40, 40, rein_ev(f)) for f in range(4)])
J["events"]["santa-reindeer"] = {"strip": "event-santa-reindeer-strip", "size": [40, 40], "frames": 4, "fps": 8, "type": "circle", "cx": 20, "cy": 20, "r": 14,
    "faces": "left", "event": "reindeerStampede", "art": "flying reindeer, red nose + bell collar, sparkle hoof-trail behind (right). Sky object: no anchor."}
strip("event-santa-pigeon-strip", [svg(40, 40, flip(40, bird(f, "#C9C2E8", "#A9A3C9", "#E6E2EE", GOLD2))) for f in range(4)])
J["events"]["santa-pigeon"] = {"strip": "event-santa-pigeon-strip", "size": [40, 40], "frames": 4, "fps": 8, "type": "circle", "cx": 20, "cy": 20, "r": 14, "faces": "left", "event": "bigBenPigeons", "art": "Santa-hat pigeon flock (flying)"}
# aurora wisps: little glowing aurora spirits (genuine sky objects)
AUR = {"a": ("#9EF0C8", "#4FBF95"), "b": ("#FFB3E1", "#D96FA8"), "c": ("#C9B8FF", "#8A74D6")}
def wisp(f, a, b, uid):
    wv = (0, 2, 0, -2)[f]; bob = (0, -1, 0, 1)[f]
    tail = f'<path d="M24,{14+bob} Q32,{10+wv} 39,{16-wv} Q33,{20+bob} 38,{27+wv} Q30,{26+bob} 24,{27+bob} Z" fill="{a}" stroke="{b}" stroke-width="1.4" stroke-linejoin="round" opacity="0.85"/>'
    return (glow(18, 20 + bob, 19, a, 0.55, uid) + tail + C(17, 20 + bob, 10, "#FFFFFF", 1.6, f'stroke="{b}"') + C(17, 20 + bob, 7, a, 0, 'opacity="0.55"')
            + face(16, 21 + bob, 0.3, "blink" if f == 2 else "open") + sparkle(8, 9 + bob, 3, "#FFFFFF", b) + sparkle(30 + wv / 2, 33, 2.2, "#FFFFFF", b, 0.8))
for k, (a, b) in AUR.items():
    strip(f"event-santa-aurora-wisp-{k}-strip", [svg(40, 40, wisp(f, a, b, f"w{k}{f}")) for f in range(4)])
    J["events"][f"santa-aurora-{k}"] = {"strip": f"event-santa-aurora-wisp-{k}-strip", "size": [40, 40], "frames": 4, "fps": 8, "type": "circle", "cx": 18, "cy": 20, "r": 14, "faces": "left", "event": "auroraStorm", "art": f"aurora wisp ({a}); comet tail streams right (behind)"}
# shared pop (Rush smash) 64x64 6f, and warning 40x40 2f
def pop(f):
    t = f / 5; g = C(32, 32, 6 + 22 * t, "none", 0, f'stroke="#FFF4B8" stroke-width="{4*(1-t)+0.5:.1f}" opacity="{1-t:.2f}"')
    for i in range(8):
        a = i * math.pi / 4 + 0.3; d = 6 + 22 * t
        g += (flake if i % 2 else (lambda x, y, r, *a_: star5(x, y, r)))(32 + math.cos(a) * d, 32 + math.sin(a) * d, 6 * (1 - t * 0.6), *(("#FFFFFF", "#7FA8D8") if i % 2 else ()))
    if f < 2: g += C(32, 32, 10 - f * 3, "#FFFFFF", 0, 'opacity="0.9"')
    return f'<g opacity="{1 - max(0, t - 0.6) * 2:.2f}">{g}</g>'
strip("event-santa-pop-strip", [svg(64, 64, pop(f)) for f in range(6)])
J["events"]["santa-pop"] = {"strip": "event-santa-pop-strip", "size": [64, 64], "frames": 6, "fps": 12, "anchor": [32, 32], "art": "snow-sparkle smash burst (Rush), play once"}
def warn(f):
    s = 1 + 0.08 * f
    return (f'<g transform="translate(20,21) scale({s}) translate(-20,-21)">' + P("M20,4 Q22,4 23,6 L37,32 Q38,35 35,35 H5 Q2,35 3,32 L17,6 Q18,4 20,4 Z", "url(#red)", 2.2)
            + snowcap(12, 28, 10, 3) + R(18, 13, 4, 12, "#FFFFFF", 0, 2) + C(20, 30, 2.4, "#FFFFFF", 0) + "</g>" + (sparkle(35, 6, 3.4) if f else sparkle(5, 8, 2.6)))
strip("ui-santa-event-warning-strip", [svg(40, 40, warn(f)) for f in range(2)])
J["events"]["santa-warning"] = {"strip": "ui-santa-event-warning-strip", "size": [40, 40], "frames": 2, "fps": 4, "anchor": [20, 20], "art": "candy-red warning triangle with snowcap"}

# diagonal showers 72x48, circle (cx,cy) r12; trail points opposite to travel
def balloon(f):  # rises up-left (vy<0): body top-left, string hangs DOWN-right (physically trails behind+below)
    sw = (0, 2)[f]
    return (f'<path d="M22,30 Q{30+sw},38 {38},{42-sw} T{58},46" fill="none" {st(1.4)}/>' + P("M20,28 L24,28 L22,32 Z", "#FF6F7F", 1.2)
            + E(22, 17, 13, 14, "#FF8FA3", 2) + E(17, 11, 4, 2.6, "#FFFFFF", 0, 'opacity="0.8" transform="rotate(-30 17 11)"') + face(22, 19, 0.35)
            + star5(32, 6, 4) + P("M10,6 Q22,-2 34,6", "none", 0, ""))
strip("event-santa-parade-balloon-strip", [svg(72, 48, balloon(f)) for f in range(2)])
J["events"]["santa-balloon"] = {"strip": "event-santa-parade-balloon-strip", "size": [72, 48], "frames": 2, "fps": 4, "type": "circle", "cx": 22, "cy": 18, "r": 12, "travel": "up-left", "event": "paradeBalloons",
    "art": "loose parade balloon drifting up; its string trails down-right. NOTE cx/cy differ from the ghost meteor default (18,32): set from json."}
def firework(f):  # falls down-left: trail up-right
    tr = "".join(sparkle(30 + i * 9, 26 - i * 5 + (f * 2 if i % 2 else 0), 4 - i * 0.6, ("#FFE08A", "#FFB3E1", "#9EF0E0")[i % 3], "#B07A3A", 1 - i * 0.18) for i in range(5))
    return (tr + f'<path d="M20,30 L66,4" stroke="#FFE08A" stroke-width="3" stroke-linecap="round" opacity="0.45"/>' + glow(18, 32, 16, "#FFE08A", 0.6, f"fw{f}")
            + star5(18, 32, 11, "#FFD873", "#B07A3A", 2, -90 + f * 18) + face(18, 33, 0.25, "happy"))
strip("event-santa-firework-strip", [svg(72, 48, firework(f)) for f in range(2)])
J["events"]["santa-firework"] = {"strip": "event-santa-firework-strip", "size": [72, 48], "frames": 2, "fps": 10, "type": "circle", "cx": 18, "cy": 32, "r": 12, "travel": "down-left", "event": "harbourFireworks", "art": "spent firework star falling (sky object) with spark trail up-right"}
def icefall(f):  # falls down-left; a chunk broken off the ice cliffs, frost trail up-right
    tr = "".join(flake(34 + i * 10, 24 - i * 6, 4 - i * 0.7, "#FFFFFF", "#7FA8D8", f * 20) for i in range(4))
    return (tr + f'<path d="M22,28 L68,4" stroke="#DDF1FF" stroke-width="5" stroke-linecap="round" opacity="0.6"/>'
            + f'<g transform="rotate({-35 + f*6} 18 32)">' + P("M8,26 L18,18 L30,24 L28,38 L16,44 L6,36 Z", "#CFEAFF", 2) + P("M10,27 L18,21 L27,25 L18,29 Z", "#FFFFFF", 0, 'opacity="0.8"') + snowcap(9, 29, 22, 3) + "</g>" + face(18, 34, 0.25, "squeeze" if f else "open"))
strip("event-santa-icefall-strip", [svg(72, 48, icefall(f)) for f in range(2)])
J["events"]["santa-icefall"] = {"strip": "event-santa-icefall-strip", "size": [72, 48], "frames": 2, "fps": 10, "type": "circle", "cx": 18, "cy": 32, "r": 12, "travel": "down-left", "event": "icefall", "art": "ice chunk calved off the Antarctic cliffs, frost trail up-right"}

# ground sweeps, bottom on the ground line, move right->left (face left)
def camel(x, f, hat):
    leg = (2, -2)[f]
    g = P(f"M{x+8},50 l{leg},20 M{x+14},52 l{-leg},18 M{x+30},52 l{leg},18 M{x+36},50 l{-leg},20", "none", 0, f'stroke="{L}" stroke-width="3.4" stroke-linecap="round"')
    g += P(f"M{x+2},40 Q{x+4},26 {x+16},32 Q{x+22},20 {x+30},30 Q{x+40},28 {x+42},42 Q{x+40},54 {x+24},54 Q{x+6},54 {x+2},40 Z", "#E8BC84", 2)
    g += R(x + 12, 36, 22, 10, "#FF8FA3", 1.4, 4) + "".join(C(x + 15 + i * 8, 46, 1.8, GOLD, 0.8) for i in range(3))
    g += P(f"M{x+4},40 Q{x-6},28 {x-4},16", "none", 0, f'stroke="{L}" stroke-width="9" stroke-linecap="round"') + P(f"M{x+4},40 Q{x-6},28 {x-4},16", "none", 0, 'stroke="#E8BC84" stroke-width="6" stroke-linecap="round"')
    g += E(x - 8, 14, 8, 6, "#E8BC84", 2) + C(x - 11, 12, 1.3, EYE, 0) + E(x - 9, 16.5, 1.6, 1, BLUSH, 0) + C(x - 4, 22, 2.4, GOLD, 1)
    if hat: g += P(f"M{x-14},9 Q{x-8},1 {x-1},8 Z", "url(#red)", 1.2) + R(x - 15, 7.5, 15, 3, FUR, 0.9, 1.5) + C(x - 13.5, 3, 1.8, FUR, 0.8)
    return g
CAMX = (16, 80, 144)  # v0.8.4: third camel used to overhang the 192px box (x up to 196)
def caravan(f):
    return (P("M56,32 Q66,34 74,22 M120,32 Q130,34 138,22", "none", 0, f'stroke="{L}" stroke-width="1.4" stroke-dasharray="2 3"')
            + camel(CAMX[0], f, True) + camel(CAMX[1], 1 - f, True) + camel(CAMX[2], f, False) + "".join(sparkle(68 + i * 64, 8 + (f * 3 if i else 0), 2.6) for i in range(2)))
strip("event-santa-camel-caravan-strip", [svg(192, 72, caravan(f)) for f in range(2)])
J["events"]["santa-camels"] = {"strip": "event-santa-camel-caravan-strip", "size": [192, 72], "frames": 2, "fps": 10, "rects": [r for x in CAMX for r in ([x - 14, 8, 22, 34], [x, 22, 44, 50])], "bottom": "ground", "floor": 72, "solidTop": 8, "solidHeight": 64,
    "heightNote": "72 = art box only. Feet touch y=72 = GROUND_Y. Solid = per camel head/neck [x-14,8,22,34] + body/legs [x,22,44,50]; Santa hats (y<8) and the rope are not solid.", "faces": "left", "event": "camelCaravan",
    "art": "three camels on lead ropes, bells + Santa hats; feet on the ground line"}
def train(f):
    g = R(0, 64, 288, 5, "#C9C2E8", 1.4, 2)  # rail it runs on: top y64 (wheels r5 @ y60 sit on it)
    for i in range(6): g += R(10 + i * 48 + f * 6, 68, 10, 4, "#A9A3C9", 0, 1)  # sleepers, bottom = y72 = ground
    g += P("M60,20 Q8,22 4,50 Q4,60 14,60 H284 V22 Q284,18 278,18 H70 Q64,18 60,20 Z", "#F7FAFF", 2.2)
    g += P("M8,46 Q12,32 40,26 L44,40 Q24,42 8,46 Z", "#7FB8F0", 1.6) + P("M6,52 H284", "none", 0, 'stroke="#7FA8F0" stroke-width="4"') + P("M6,55 H284", "none", 0, f'stroke="{RED2}" stroke-width="2"')
    for i in range(5): g += R(76 + i * 42, 28, 26, 12, "#BFE6FF", 1.4, 4)
    g += P("M120,18 V22 M200,18 V22", "none", 0, f'stroke="{L}" stroke-width="1.4"') + face(28, 48, 0.4) + C(8, 50, 2.2, "#FFF4B8", 1)
    g += "".join(C(40 + i * 56, 60, 5, "#6B4E7A", 0) + C(40 + i * 56, 60, 2, "#C9C2E8", 0) for i in range(5))
    g += P("M70,18 Q90,8 110,18 Z", "none", 0, "") + "".join(P(f"M{270-i*10},{24+f*2} h12", "none", 0, f'stroke="#FFFFFF" stroke-width="2" opacity="{0.7-i*0.2}" stroke-linecap="round"') for i in range(3))
    g += snowcap(70, 280, 19, 3) + R(150, 22, 16, 8, "#FFE3EC", 1, 2) + sparkle(158, 14, 3)
    return g
strip("event-santa-bullet-train-strip", [svg(288, 72, train(f)) for f in range(2)])
J["events"]["santa-train"] = {"strip": "event-santa-bullet-train-strip", "size": [288, 72], "frames": 2, "fps": 10, "rects": [[6, 30, 40, 42], [30, 18, 258, 54]], "bottom": "ground (train sits on its own rail, rail bottom = sprite bottom)", "floor": 72, "railTop": 64, "solidTop": 18, "solidHeight": 54,
    "heightNote": "72 = art box. Body y18-60, wheels to y65 on the rail (top y64), sleepers end at y72 = GROUND_Y. Solid all the way down (the 12px under the body is the moving rail; no fly-under gap).", "faces": "left", "event": "bulletTrain",
    "art": "kawaii shinkansen with a festive stripe, on its rail"}

# confetti (Rio confettiShower, catchables) 32x32, 6 frames = 6 shapes; engine picks frame + spins
CONF = ["#FF8FB1", "#9EF0E0", "#FFE08A", "#C9B8FF", "#FF9F6B", "#7FD8A6"]
def conf(i):
    c = CONF[i]
    shp = [P("M8,12 Q14,4 18,12 T28,12", "none", 0, f'stroke="{L}" stroke-width="7" stroke-linecap="round"') + P("M8,12 Q14,4 18,12 T28,12", "none", 0, f'stroke="{c}" stroke-width="4.4" stroke-linecap="round"'),
           star5(16, 17, 11, c, L, 1.8), C(16, 16, 10, c, 1.8), R(7, 7, 18, 18, c, 1.8, 4, 'transform="rotate(20 16 16)"'), heart(16, 17, 1.6, c, L),
           P("M6,24 Q12,4 20,16 Q26,24 28,6", "none", 0, f'stroke="{L}" stroke-width="6" stroke-linecap="round"') + P("M6,24 Q12,4 20,16 Q26,24 28,6", "none", 0, f'stroke="{c}" stroke-width="3.6" stroke-linecap="round"')][i]
    return glow(16, 16, 16, "#FFFFFF", 0.5, f"cf{i}") + shp + hl(11, 11, 14, 9, 1.4, 0.8)
strip("event-santa-confetti-strip", [svg(32, 32, conf(i)) for i in range(6)])
J["confetti"]["santa-confetti"] = {"strip": "event-santa-confetti-strip", "size": [32, 32], "frames": 6, "frameMode": "pick one frame per piece (6 shapes), rotate in code", "type": "circle", "cx": 16, "cy": 16, "r": 12, "hazard": False, "event": "confettiShower", "art": "carnival confetti pieces (curl, star, dot, square, heart, streamer)"}
def cburst(f):
    t = f / 5; rnd = random.Random(3); g = ""
    for i in range(14):
        a = i / 14 * 2 * math.pi + rnd.uniform(-.2, .2); d = 10 + 60 * t * rnd.uniform(.7, 1)
        x, y = 80 + math.cos(a) * d, 80 + math.sin(a) * d + 18 * t * t
        g += f'<g transform="translate({x:.1f},{y:.1f}) rotate({i*40+f*50}) scale({0.9-0.4*t:.2f}) translate(-16,-16)">{conf(i % 6).split("</defs>",1)[1]}</g>'
    return f'<g opacity="{1 - max(0, t - 0.5) * 1.6:.2f}">' + g + (text2(80, 86, "+1", 26, "#FFFFFF", "#8A3A52", 5) if f < 4 else "") + "</g>"
strip("fx-santa-confetti-burst-strip", [svg(160, 160, cburst(f)) for f in range(6)])
J["confetti"]["santa-confetti-burst"] = {"strip": "fx-santa-confetti-burst-strip", "size": [160, 160], "frames": 6, "fps": 12, "anchor": [80, 80], "art": "catch burst with +1, play once"}

# ======================= 2. GOLDEN SANTA C =======================
BC.VAR["golden"] = dict(trim="#FFF4C9", aura="#FFD45C", flame=("#FFC24B", "#FFF0A0", "#FFFFFF"), spk="#FFFBE0")
GSWAP = {RED: "#FFE7A0", RED2: "#F6C453", RED_D: "#C98A2E"}
def golden(svgs):
    for a, b in GSWAP.items(): svgs = svgs.replace(a, b)
    return svgs
for name, seq in (("idle", BC.IDLE), ("boost", BC.BOOST)):
    for i, kw in enumerate(seq):
        kw = dict(kw); kw.setdefault("seed", i + (10 if name == "boost" else 0)); kw["sparkles"] = BC.VSPARK[i]; kw["aura_r"] = 36 if name == "idle" else 40
        F[f"santa-c-golden-{name}-{i}"] = golden(BC.hero("golden", **kw))
S["santa-c-golden-strip"] = [f"santa-c-golden-idle-{i}" for i in range(4)] + [f"santa-c-golden-boost-{i}" for i in range(4)]

# ======================= 3. HERO FX =======================
def aura(f):
    r = 40 + (0, 2, 4, 2)[f]; g = glow(48, 48, r + 6, "#FFD45C", 0.6, f"au{f}") + C(48, 48, r - 4, "none", 0, f'stroke="#FFF4B8" stroke-width="2.4" stroke-dasharray="3 7" opacity="0.8" transform="rotate({f*22} 48 48)"')
    for i in range(4):
        a = f * 0.4 + i * math.pi / 2; g += star5(48 + math.cos(a) * (r - 2), 48 + math.sin(a) * (r - 2), 4.4, "#FFE08A", "#B07A3A", 1.2)
    return g
strip("fx-santa-rush-aura-strip", [svg(96, 96, aura(f)) for f in range(4)])
strip("santa-heart-overlay-strip", [svg(20, 20, heart(10, 11, 1.2 + 0.1 * f, "#FF8FA8", L) + E(7, 8, 1.6, 1, "#FFFFFF", 0, 'opacity="0.8"')) for f in range(2)])
def frostb(f):
    t = f / 5; g = C(48, 48, 8 + 36 * t, "none", 0, f'stroke="#CDEBFF" stroke-width="{5*(1-t)+0.6:.1f}" opacity="{1-t:.2f}"')
    for i in range(6):
        a = i * math.pi / 3 + t; d = 8 + 34 * t; g += flake(48 + math.cos(a) * d, 48 + math.sin(a) * d, 8 - 4 * t, "#FFFFFF", "#6FA8D6", t * 60)
    return f'<g opacity="{1 - max(0, t - 0.6) * 2:.2f}">{g}</g>'
strip("fx-santa-frost-burst-strip", [svg(96, 96, frostb(f)) for f in range(6)])
def bburst(f):
    t = f / 5; g = C(64, 64, 10 + 46 * t, "none", 0, f'stroke="#FFE08A" stroke-width="{6*(1-t)+0.6:.1f}" opacity="{1-t:.2f}"')
    for i in range(8):
        a = i * math.pi / 4; d = 10 + 44 * t
        g += (P("M-6,-4 L6,-4 L4,6 L-4,6 Z", ("#FFD873", "#FF8FA8", "#9ED8FF")[i % 3], 1.4, f'transform="translate({64+math.cos(a)*d:.1f},{64+math.sin(a)*d:.1f}) rotate({i*45+f*30})"') if i % 2 else sparkle(64 + math.cos(a) * d, 64 + math.sin(a) * d, 6))
    return f'<g opacity="{1 - max(0, t - 0.6) * 2:.2f}">{g}</g>'
strip("fx-santa-bauble-burst-strip", [svg(128, 128, bburst(f)) for f in range(6)])
def heartfx(f, broken):
    t = f / 5; s = 1.6 + t * 1.4 if not broken else 2.2
    if broken:
        dx = t * 16
        g = (f'<g transform="translate({-dx},{t*20}) rotate({-t*25} 48 48)"><clipPath id="hl{f}"><rect x="0" y="0" width="48" height="96"/></clipPath><g clip-path="url(#hl{f})">{heart(48, 50, 3, "#FF8FA8", L)}</g></g>'
             f'<g transform="translate({dx},{t*20}) rotate({t*25} 48 48)"><clipPath id="hr{f}"><rect x="48" y="0" width="48" height="96"/></clipPath><g clip-path="url(#hr{f})">{heart(48, 50, 3, "#FF8FA8", L)}</g></g>')
    else:
        g = heart(48, 50, s, "#FF8FA8", L) + "".join(sparkle(48 + math.cos(i * 1.57 + .7) * (12 + 26 * t), 48 + math.sin(i * 1.57 + .7) * (12 + 26 * t), 4) for i in range(4))
    return f'<g opacity="{1 - max(0, t - 0.6) * 2:.2f}">{g}</g>'
strip("fx-santa-heart-pop-strip", [svg(96, 96, heartfx(f, False)) for f in range(6)])
strip("fx-santa-heart-break-strip", [svg(96, 96, heartfx(f, True)) for f in range(6)])
def vignette():
    g = ('<defs><radialGradient id="vg" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#CDEBFF" stop-opacity="0"/><stop offset="0.9" stop-color="#CDEBFF" stop-opacity="0.55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0.85"/></radialGradient></defs>'
         '<rect width="360" height="640" fill="url(#vg)"/>')
    rnd = random.Random(11)
    for i in range(34):
        side = i % 4; u = rnd.uniform(0, 1)
        x, y = [(u * 360, rnd.uniform(2, 26)), (u * 360, 640 - rnd.uniform(2, 26)), (rnd.uniform(2, 22), u * 640), (360 - rnd.uniform(2, 22), u * 640)][side]
        g += flake(round(x, 1), round(y, 1), rnd.uniform(4, 9), "#FFFFFF", "#8FBEE6", rnd.uniform(0, 60))
    return svg(360, 640, g + icicles(0, 360, 0, [10, 18, 8, 22, 12, 16, 9, 20, 14, 11, 19, 8, 15, 21, 10, 17]))
F["ui-santa-frost-vignette"] = vignette()
for k, (r, rot) in zip("abc", ((7, 0), (6, 15), (5.5, 30))): F[f"fx-santa-frost-flake-{k}"] = svg(16, 16, flake(8, 8, r, "#FFFFFF", "#7FA8D8", rot))
J["fx"] = {"rushAura": {"file": "fx-santa-rush-aura-strip.png", "w": 96, "h": 96, "frames": 4, "fps": 8, "dx": -16, "dy": -16, "note": "centre (48,48) = hero anchor"},
           "heart": {"file": "santa-heart-overlay-strip.png", "w": 20, "h": 20, "frames": 2, "fps": 4, "dx": 46, "dy": 2, "note": "sits right of the hood bobble, clear of the face"},
           "heartPop": {"file": "fx-santa-heart-pop-strip.png", "w": 96, "h": 96, "frames": 6, "fps": 12}, "heartBreak": {"file": "fx-santa-heart-break-strip.png", "w": 96, "h": 96, "frames": 6, "fps": 12},
           "frostBurst": {"file": "fx-santa-frost-burst-strip.png", "w": 96, "h": 96, "frames": 6, "fps": 12}, "candyBurst": {"file": "fx-santa-bauble-burst-strip.png", "w": 128, "h": 128, "frames": 6, "fps": 12},
           "frostVignette": {"file": "ui-santa-frost-vignette.png", "w": 360, "h": 640}, "flakes": ["fx-santa-frost-flake-a.png", "fx-santa-frost-flake-b.png", "fx-santa-frost-flake-c.png"]}

# ======================= 4. SLEIGH HOP CUTSCENE =======================
def sleigh(f):
    gal = (0, 3, 0, -3)[f]; g = ""
    for i in range(6): g += sparkle(212 - i * 0, 0, 0) if False else ""
    for i in range(5): g += sparkle(206 + i * 4, 70 + (i * 7 + f * 5) % 20 - 6, 3.2 - i * 0.4, ("#FFF4B8", "#FFB3E1", "#9EF0E0")[i % 3], "#B07A3A", 0.9 - i * 0.12)
    g += P("M100,64 Q70,56 52,40 M100,64 Q72,62 18,40", "none", 0, f'stroke="{RED2}" stroke-width="2" stroke-linecap="round"')  # reins: sleigh -> reindeer harness
    g += f'<g transform="translate(8,{18+gal})">{flip(40, reindeer(f))}</g>' + f'<g transform="translate(44,{20-gal})">{flip(40, reindeer((f+2)%4))}</g>'
    g += P("M96,70 Q92,86 108,88 H196 Q206,88 204,80", "none", 0, f'stroke="{GOLD2}" stroke-width="4" stroke-linecap="round"') + P("M96,70 Q92,86 108,88 H196 Q206,88 204,80", "none", 0, f'stroke="{L}" stroke-width="1.4" stroke-linecap="round" opacity="0.6"')
    g += P("M100,46 Q98,72 116,78 H184 Q200,78 202,60 L204,34 Q190,40 176,46 Z", "url(#red)", 2.4) + snowcap(104, 176, 47, 4) + P("M108,62 Q150,70 196,58", "none", 0, f'stroke="{GOLD}" stroke-width="3"')
    g += R(184, 18, 18, 16, "#9ED8FF", 1.6, 2) + R(191, 18, 4, 16, "#FFFFFF", 0) + R(170, 26, 16, 18, "#FFD873", 1.6, 2) + R(176, 26, 4, 18, "#FF8FA8", 0)
    g += C(140, 46, 3, "#FFFFFF", 0, 'opacity="0"')  # seat marker (invisible)
    return g
strip("cut-santa-sleigh-strip", [svg(224, 96, sleigh(f)) for f in range(4)])
def hopstar(f):
    t = f / 5
    return (glow(32, 32, 30, "#FFF4B8", 0.7 * (1 - t), f"hs{f}") + "".join(sparkle(32 + math.cos(i * 1.05 + t) * 26 * t, 32 + math.sin(i * 1.05 + t) * 26 * t, 5 - 3 * t, "#FFFFFF", "#D9953A") for i in range(6)) + star5(32, 32, 10 * (1 - t) + 2, "#FFE08A", "#B07A3A", 1.6))
strip("cut-santa-hop-sparkle-strip", [svg(64, 64, hopstar(f)) for f in range(6)])
def swoosh(f):
    t = f / 5; x0 = -60 + 300 * t
    return "".join(P(f"M{x0+i*10:.0f},{22+i*10} Q{x0+90+i*10:.0f},{14+i*10} {x0+170+i*10:.0f},{24+i*10}", "none", 0, f'stroke="{c}" stroke-width="{6-i}" stroke-linecap="round" opacity="{0.9-i*0.2}"') for i, c in enumerate(("#FFF4B8", "#FFB3E1", "#9EF0E0"))) + sparkle(min(x0 + 175, 232), 26, 6)
strip("ui-santa-swoosh-strip", [svg(240, 64, swoosh(f)) for f in range(6)])
# v0.8.4: numeric cutscene timeline. Mirrors pack.js sleigh {seat:[140,46], seatS:0.6, leaveS:0.6, goneS:1.6, enterDy:40, riseDy:-180, exitX:-240, heroScale:0.75, sparkleSize:64}
# Authored over 2000 ms; the engine scales by cutsceneSeconds (t_engine = t_ms * cutsceneSeconds / 2.0). Positions: "seat" = sleigh seat point in screen px,
# sleigh sprite drawn at seat - seat[]; hero = hero anchor (hx,hy) at warp start; W = view width.
TIMELINE = {"authoredMs": 2000, "scaleTo": "cutsceneSeconds", "units": {"t": "ms", "pos": "screen px", "seatPx": "sleigh sprite px"},
 "events": [
  {"t_ms": 0, "action": "sleighEnter", "params": {"sheet": "santa-sleigh", "fps": 10, "frames": 4, "loop": True, "from": {"seatX": "W+140", "seatY": "hy+40"}, "to": {"seatX": "hx", "seatY": "hy"},
      "durMs": 600, "easeX": "outQuad", "easeY": "linear", "dxFromW": 140, "dy": 40}},
  {"t_ms": 600, "action": "santaHop", "params": {"from": "hero anchor (hx,hy)", "to": {"seat": [140, 46]}, "durMs": 0, "heroFrame": 0, "heroScale": 0.75, "drawOrder": ["hero", "sleigh"], "note": "snap: the sleigh arrives under the hero, so no arc"}},
  {"t_ms": 600, "action": "sparkle", "params": {"sheet": "santa-hop-sparkle", "frames": 6, "fps": 12, "durMs": 500, "loop": False, "at": "seat", "anchor": [32, 32], "size": 64}},
  {"t_ms": 600, "action": "sleighExit", "params": {"durMs": 1000, "dx": -240, "dy": -180, "ease": "inQuad", "carriesHero": True}},
  {"t_ms": 1600, "action": "sleighGone", "params": {"hide": ["sleigh", "hero"]}},
  {"t_ms": 2000, "action": "end", "params": {"stageSwap": "engine warp timeline (streak/mist) unchanged"}}]}
J["cutscene"] = {"santa-sleigh": {"strip": "cut-santa-sleigh-strip", "size": [224, 96], "frames": 4, "fps": 10, "faces": "left (flies right->left, the same way as the world scrolls)",
                 "seat": [140, 46], "note": "draw Santa C idle (k=0.75) with his anchor at seat, behind the sleigh front: draw sleigh, then hero, then re-draw nothing (sleigh rim covers his legs since hero is drawn first is NOT required; simplest order = hero then sleigh)."},
                 "santa-hop-sparkle": {"strip": "cut-santa-hop-sparkle-strip", "size": [64, 64], "frames": 6, "fps": 12, "anchor": [32, 32], "note": "play once where Santa lands in the seat"},
                 "santa-swoosh": {"strip": "ui-santa-swoosh-strip", "size": [240, 64], "frames": 6, "fps": 12, "note": "transitionArt.swoosh drop-in (240x64 6f)"},
                 "timeline": TIMELINE}

# ======================= 5. HUD 2x, BADGE 9 =======================
HUD2X = {}
for k in ("rush", "life", "chill"): HUD2X[k] = SL.png(open(os.path.join(SANTA, "stages/svg", f"ui-hud-santa-{k}.svg")).read(), 96, 96)
b9 = badge(9).replace("#FFE3EC", "#DDF7EC").replace("url(#red)", "url(#aur9)").replace("#7A4E66", "#4A3E7A").replace("#8A3A52", "#4A3E7A")
b9 = b9.replace("<g", '<defs><linearGradient id="aur9" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9EF0C8"/><stop offset="0.5" stop-color="#C9B8FF"/><stop offset="1" stop-color="#FFB3E1"/></linearGradient></defs><g', 1) if "<g" in b9 else b9.replace("</svg>", "", 0)
if "aur9" not in b9.split("url(#aur9)")[0]: b9 = b9.replace(">", '><defs><linearGradient id="aur9" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9EF0C8"/><stop offset="0.5" stop-color="#C9B8FF"/><stop offset="1" stop-color="#FFB3E1"/></linearGradient></defs>', 1)
F["ui-santa-badge-9"] = b9

# helpers reused by build_santa_scorecard.py
from build_santa_stages import bauble
def BAUB_SVG(kind): return bauble(kind, 0)
F_REIN = flip(40, reindeer(1))
def GIFT(c, rib): return R(4, 14, 40, 32, c, 2, 4) + R(20, 14, 8, 32, rib, 1.4) + R(2, 8, 44, 10, c, 2, 3) + R(20, 8, 8, 10, rib, 1.4) + P("M24,8 Q14,-2 12,6 Q18,8 24,8 Q34,-2 36,6 Q30,8 24,8 Z", rib, 1.4) + snowcap(4, 44, 9, 3)
if __name__ == "__main__":
    cache = SL.export_all()
    # HUD 2x (same filenames the pack already uses; png/2x currently holds 48px copies)
    for k, im in HUD2X.items():
        im.save(os.path.join(OUTD, "png/2x", f"ui-hud-santa-{k}-48.png"), optimize=True)
        im.resize((64, 64), 1).save(os.path.join(OUTD, "png/2x", f"ui-hud-santa-{k}-32.png"), optimize=True)
    n = 0
    for d in ("png/1x", "png/2x"):
        for fn in os.listdir(os.path.join(OUTD, d)):
            if fn[:-4] in F and not fn[:-4].split("-")[-1].isdigit() or fn.endswith("-strip.png") or fn.startswith("ui-hud-santa") or fn == "ui-santa-badge-9.png" or fn.startswith("ui-santa-frost") or fn.startswith("fx-santa-frost-flake"):
                shutil.copy(os.path.join(OUTD, d, fn), os.path.join(PACK, d, fn)); n += 1
    for jp in (os.path.join(PACK, "santa-hitboxes.json"), os.path.join(SANTA, "stages/santa-hitboxes.json")):
        j = json.load(open(jp))
        for k, v in J.items(): j.setdefault(k, {}).update(v) if isinstance(v, dict) else None
        json.dump(j, open(jp, "w"), indent=1)
    print(len(F), "svgs", len(S), "strips; copied", n)
