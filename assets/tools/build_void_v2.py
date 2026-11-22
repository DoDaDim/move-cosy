"""Stage 7 'void' v2.0 (TUNING v2.0): retro floater hazards + Invader Wave event sprites (Nebula Drift palette).
Names follow game.js CONFIG.assets.sheets: obs-void-float-{cassette,clock,phone}(.png = frame 0) for void-float-a/b/c,
plus an optional 4th obs-void-float-floppy (void-float-d); event-void-invader-strip.png (40x40, 2f @4fps) = events['void-invader'],
extra types event-void-invader-b/-c, event-void-invader-pop-0..5, ui-event-warning-void-0/1.
Writes SVG + png/1x,2x + strips; merges hitboxes.json (hazards/events) and death-map.json."""
import os, sys, math, json, cairosvg
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from build_tombs import svg
from build_extras import sparkle
import build_void as BV
OUT = os.path.join(os.path.dirname(__file__), "..")
FILES, STRIPS = {}, {}
LINE = "#6B4E7A"
def st(w=2.0): return f'stroke="{LINE}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def mini_face(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-4.5,-0.5 Q-3,1.2 -1.5,-0.5 M1.5,-0.5 Q3,1.2 4.5,-0.5" fill="none" stroke="#4A3358" stroke-width="1.3" stroke-linecap="round"/>'
            f'<path d="M-1,1.8 Q0,2.8 1,1.8" fill="none" stroke="#4A3358" stroke-width="1" stroke-linecap="round"/>'
            f'<ellipse cx="-6" cy="1.8" rx="1.8" ry="1" fill="#FFB3CB"/><ellipse cx="6" cy="1.8" rx="1.8" ry="1" fill="#FFB3CB"/></g>')
# ---------------- floaters (40x40, hit circle centre (20,20)) ----------------
def pocket_watch():
    return (f'<path d="M20,4 C14,-2 26,-2 20,4" fill="none" stroke="#D9953A" stroke-width="2"/>'
            f'<rect x="17" y="3.5" width="6" height="4" rx="1.5" fill="#FFE08A" {st(1.4)}/>'
            f'<circle cx="20" cy="21" r="13" fill="#FFE08A" {st(2.2)}/><circle cx="20" cy="21" r="10" fill="#FFF8EC" {st(1.4)}/>'
            + "".join(f'<circle cx="{20+math.cos(math.radians(a))*8:.1f}" cy="{21+math.sin(math.radians(a))*8:.1f}" r="0.9" fill="{LINE}"/>' for a in range(0, 360, 90))
            + f'<path d="M20,21 V15 M20,21 L24,22.5" {st(1.5)}/>' + mini_face(20, 25, 0.75)
            + '<path d="M11,15 Q13,11 17,10" stroke="#FFF" stroke-width="1.6" fill="none" stroke-linecap="round" opacity="0.8"/>')
def floppy():
    return (f'<rect x="7" y="7" width="26" height="26" rx="3" fill="#BFD8F5" {st(2.2)}/>'
            f'<path d="M7,10 V30 Q7,33 10,33 H30 Q33,33 33,30 V11 L29,7 H10 Q7,7 7,10 Z" fill="#BFD8F5" {st(2.2)}/>'
            f'<rect x="12" y="7" width="15" height="9" fill="#E9DDFB" {st(1.4)}/><rect x="22" y="8.5" width="3" height="6" fill="#9E94B8"/>'
            f'<rect x="10.5" y="19" width="19" height="12" rx="1.5" fill="#FFF8EC" {st(1.3)}/><path d="M12.5,21.5 H27.5" stroke="#FFB6CC" stroke-width="1.4"/>'
            + mini_face(20, 25.5, 0.7))
def cassette_mini(): return f'<g transform="translate(20,20) scale(0.34) translate(-50,-51)">{BV.o_cassette(BV.COL["cassette"])}</g>'
def phone_mini():   return f'<g transform="translate(20,20) scale(0.36) translate(-50,-53)">{BV.o_phone(BV.COL["phone"])}</g>'
FLOAT = {  # Code id -> (art name, drawer, radius per Tuning, motion note)
  "void-float-a": ("cassette", cassette_mini, 13),
  "void-float-b": ("clock", pocket_watch, 14),
  "void-float-c": ("phone", phone_mini, 12),
  "void-float-d": ("floppy", floppy, 13),
}
def floater_frame(fn, i):
    a = (0, 6, 0, -6)[i]                     # gentle wobble about the hit centre
    tw = (1.0, 0.55, 0.25, 0.6)[i]
    return svg(40, 40, f'<g transform="rotate({a} 20 20)">{fn()}</g>' + sparkle(35, 6, 2.4, "#FFF4B8", "#D9953A", tw) + sparkle(5, 33, 1.8, "#FFFFFF", "#9E94B8", 1.2 - tw))

# ---------------- invaders (40x40, hit circle (20,20) r14) ----------------
INV = {
  "a": dict(fill="#AEE3C6", hi="#D8F5E6", line="#3F6A5E", px=[
      ["...XXXX...", "..XXXXXX..", ".XXXXXXXX.", "XXXXXXXXXX", "XXXXXXXXXX", "XXXXXXXXXX", ".XX.XX.XX.", "X..X..X..X"],
      ["...XXXX...", "..XXXXXX..", ".XXXXXXXX.", "XXXXXXXXXX", "XXXXXXXXXX", "XXXXXXXXXX", ".XX.XX.XX.", ".X..XX..X."]]),
  "b": dict(fill="#FFB6CC", hi="#FFE0EA", line="#8A3A52", px=[
      ["X........X", ".X......X.", "..XXXXXX..", ".XXXXXXXX.", "XXXXXXXXXX", "XXXXXXXXXX", "X.XXXXXX.X", "X.X....X.X"],
      [".X......X.", ".X......X.", "..XXXXXX..", ".XXXXXXXX.", "XXXXXXXXXX", "XXXXXXXXXX", ".XXXXXXXX.", "XX......XX"]]),
  "c": dict(fill="#C9B6FF", hi="#EDE4FF", line="#5E4A8A", px=[
      ["..X....X..", "..X....X..", ".XXXXXXXX.", "XXXXXXXXXX", "XXXXXXXXXX", ".XXXXXXXX.", "..X.XX.X..", ".X......X."],
      [".X......X.", "..X....X..", ".XXXXXXXX.", "XXXXXXXXXX", "XXXXXXXXXX", ".XXXXXXXX.", ".X..XX..X.", "X........X"]]),
}
P = 3.2; OX = 20 - 5 * P; OY = 20 - 4 * P + 1   # 10x8 grid -> 32 x 25.6 px, centred on (20,20)
def invader(t, f):
    c = INV[t]; rows = c["px"][f]; out, fill, hi = [], [], []
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != "X": continue
            X, Y = OX + x * P, OY + y * P
            out.append(f'<rect x="{X-1.1:.2f}" y="{Y-1.1:.2f}" width="{P+2.2:.2f}" height="{P+2.2:.2f}" rx="1.4" fill="{c["line"]}"/>')
            fill.append(f'<rect x="{X-0.35:.2f}" y="{Y-0.35:.2f}" width="{P+0.7:.2f}" height="{P+0.7:.2f}" fill="{c["fill"]}"/>')
            if y in (1, 2) and 2 <= x <= 4: hi.append(f'<rect x="{X:.2f}" y="{Y:.2f}" width="{P:.2f}" height="{P:.2f}" fill="{c["hi"]}"/>')
    ey = OY + 3.6 * P
    face = (f'<ellipse cx="{20-5.2}" cy="{ey}" rx="2.3" ry="2.8" fill="#2A2150"/><circle cx="{20-5.9}" cy="{ey-1}" r="0.9" fill="#FFF"/>'
            f'<ellipse cx="{20+5.2}" cy="{ey}" rx="2.3" ry="2.8" fill="#2A2150"/><circle cx="{20+4.5}" cy="{ey-1}" r="0.9" fill="#FFF"/>'
            f'<path d="M18.2,{ey+3.2} Q19.1,{ey+4.6} 20,{ey+3.4} Q20.9,{ey+4.6} 21.8,{ey+3.2}" fill="none" stroke="#2A2150" stroke-width="1.1" stroke-linecap="round"/>'
            f'<rect x="{20-10.2}" y="{ey+2}" width="3.2" height="1.8" rx="0.9" fill="#FF8FAE" opacity="0.8"/><rect x="{20+7}" y="{ey+2}" width="3.2" height="1.8" rx="0.9" fill="#FF8FAE" opacity="0.8"/>')
    return svg(40, 40, "".join(out + fill + hi) + face)
def pop(i):  # 64x64, centre (32,32), 6f @12fps
    t = i / 5; s = []
    if i < 3: s.append(f'<circle cx="32" cy="32" r="{8 + 16*t:.1f}" fill="#FFF4B8" opacity="{0.8 - t:.2f}"/>' + sparkle(32, 32, 10 - 6 * t, "#FFFFFF", "#E8A050"))
    cols = ["#AEE3C6", "#FFB6CC", "#C9B6FF", "#BFE6FF", "#FFE08A"]
    for k in range(10):
        a = 2 * math.pi * k / 10 + 0.3; d = 6 + 24 * (1 - (1 - t) ** 2)
        x, y = 32 + math.cos(a) * d, 32 + math.sin(a) * d + 6 * t * t; sz = 4.6 - 2.4 * t
        s.append(f'<rect x="{x-sz/2:.1f}" y="{y-sz/2:.1f}" width="{sz:.1f}" height="{sz:.1f}" rx="0.8" fill="{cols[k % 5]}" stroke="{LINE}" stroke-width="0.9" opacity="{max(0, 1 - t*0.9):.2f}" transform="rotate({k*30 + i*25} {x:.1f} {y:.1f})"/>')
    if 1 <= i <= 4:
        s.append(f'<text x="32" y="{14 - i}" text-anchor="middle" font-family="Capriola, sans-serif" font-size="11" fill="#FFFFFF" stroke="{LINE}" stroke-width="3" paint-order="stroke" opacity="{1 if i < 4 else 0.5}">pop!</text>')
    return svg(64, 64, "".join(s))
def warning(f):  # 40x40 like ui-event-warning, invader peeking + "!"
    b = (0, -1.5)[f]
    s = (f'<path d="M6,{8+b} Q6,{4+b} 10,{4+b} H30 Q34,{4+b} 34,{8+b} V{26+b} Q34,{30+b} 30,{30+b} H24 L20,{36+b} L16,{30+b} H10 Q6,{30+b} 6,{26+b} Z" fill="{"#FFE08A" if f else "#FFF1B8"}" stroke="#8E5A3C" stroke-width="2.2" stroke-linejoin="round"/>'
         f'<g transform="translate(-3,{b-1}) scale(0.55) translate(14,10)">{invader("a", f)[invader("a", f).index(">")+1:invader("a", f).rindex("</svg>")]}</g>'
         f'<rect x="26.5" y="{8+b}" width="4" height="12" rx="2" fill="#E2557A"/><circle cx="28.5" cy="{24.5+b}" r="2.2" fill="#E2557A"/>'
         + sparkle(36, 4, 2.4, "#FFFFFF", "#D9953A", 1 if f else 0.5))
    return svg(40, 40, s)

def build():
    for cid, (n, fn, r) in FLOAT.items():
        STRIPS[f"obs-void-float-{n}"] = []
        for i in range(4):
            FILES[f"obs-void-float-{n}-{i}"] = floater_frame(fn, i); STRIPS[f"obs-void-float-{n}"].append(f"obs-void-float-{n}-{i}")
        FILES[f"obs-void-float-{n}"] = floater_frame(fn, 0)
    for t in INV:
        base = "event-void-invader" if t == "a" else f"event-void-invader-{t}"
        STRIPS[base] = []
        for f in (0, 1): FILES[f"{base}-{f}"] = invader(t, f); STRIPS[base].append(f"{base}-{f}")
    STRIPS["event-void-invader-pop"] = []
    for i in range(6): FILES[f"event-void-invader-pop-{i}"] = pop(i); STRIPS["event-void-invader-pop"].append(f"event-void-invader-pop-{i}")
    STRIPS["ui-event-warning-void"] = []
    for f in (0, 1): FILES[f"ui-event-warning-void-{f}"] = warning(f); STRIPS["ui-event-warning-void"].append(f"ui-event-warning-void-{f}")

def merge_json():
    hp = os.path.join(OUT, "hitboxes.json"); H = json.load(open(hp))
    for cid, (n, fn, r) in FLOAT.items():
        H["hazards"][cid] = {"files": f"obs-void-float-{n}-{{0,1,2,3}}", "single": f"obs-void-float-{n}", "strip": f"obs-void-float-{n}-strip",
                             "size": [40, 40], "type": "circle", "cx": 20, "cy": 20, "r": r, "frames": 4, "fps": 6, "art": n,
                             "note": "4-frame wobble loop (+-6 deg about (20,20)) with twinkle; hit circle fixed at (20,20). Motion (drift/bob) is Code's"
                                     + ("; optional 4th floater, not in CONFIG yet" if cid == "void-float-d" else "")}
    H["events"]["void-invader"] = {"files": "event-void-invader-{0,1}", "strip": "event-void-invader-strip", "size": [40, 40], "type": "circle", "cx": 20, "cy": 20, "r": 14,
                                   "frames": 2, "fps": 4, "variants": ["event-void-invader-strip", "event-void-invader-b-strip", "event-void-invader-c-strip"],
                                   "note": "march: alternate frames 0/1. Types a (mint), b (pink), c (lilac) share size + hitbox; e.g. one type per wave/row"}
    H["events"]["void-invader-pop"] = {"files": "event-void-invader-pop-{0..5}", "strip": "event-void-invader-pop-strip", "size": [64, 64], "anchor": [32, 32], "frames": 6, "fps": 12, "hitbox": None,
                                       "note": "play once at an invader's centre (e.g. when it leaves / on wave cleared / on hit); decorative"}
    H["events"]["warning-void"] = {"files": "ui-event-warning-void-{0,1}", "strip": "ui-event-warning-void-strip", "size": [40, 40], "frames": 2, "fps": 4, "hitbox": None,
                                   "note": "Void version of ui-event-warning for the 'Invaders!' warning"}
    json.dump(H, open(hp, "w"), indent=2)
    dp = os.path.join(OUT, "death-map.json"); D = json.load(open(dp))
    for cid in FLOAT: D[cid] = "generic"
    D["void-invader"] = "generic"; D["invaderWave"] = "generic"
    D["_voidV2Note"] = "void floaters are small, light keepsakes -> generic bonk (as game.js already maps them); invaders -> generic"
    json.dump(D, open(dp, "w"), indent=2)

if __name__ == "__main__":
    build(); BV.FILES.clear(); BV.STRIPS.clear(); BV.FILES.update(FILES); BV.STRIPS.update(STRIPS); BV.export(); merge_json()
    print(len(FILES), "svgs,", len(STRIPS), "strips")
