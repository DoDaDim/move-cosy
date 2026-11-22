"""Stage 7 'void' (The Void, concept A Nebula Drift): endless zone after space.
Obstacles obs-void-<obj>-top-{body,cap-bottom} (satin ribbon tile + hanging object) and
obs-void-<obj>-bottom-{body,cap-top} (cotton-candy cloud tile + object sitting on a cloud), 72px footprint.
Also bg-void-{far,mid,near}, bg-trans-space-void-{far,mid,near}, bg-trans-space-void-mist-0..7 overlay,
ui-banner-void(-blank), ui-stage-badge-7, fx-burst-void-0..5. Writes SVG + png/1x,2x + strips and merges
hitboxes.json / sky-palettes.json / death-map.json. Run: python3 tools/build_void.py && python3 tools/check_hitbox_continuity.py"""
import os, sys, math, json, random, cairosvg
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from build_tombs import svg, LW
from build_extras import sparkle
import v04_common as C
import build_v05 as V
import build_backgrounds as B
OUT = os.path.join(os.path.dirname(__file__), "..")
FILES, HIT, EDGES, STRIPS = {}, {}, {}, {}
LINE = "#6B4E7A"
SKY = ("#2C2356", "#7A64AE")
COL = {  # per-object pastel sets: fill, fill2, acc, acc2
  "typewriter": ("#E8F7EF", "#BFE6D2", "#FFB6CC", "#FFE08A"),
  "crt":        ("#F3EAFF", "#D9C6F5", "#FFB6CC", "#AEE3C6"),
  "phone":      ("#FFE3EC", "#FFC2D6", "#FF9EB8", "#FFE08A"),
  "cassette":   ("#E6F2FF", "#BFD8F5", "#FFB6CC", "#FFE08A"),
  "gramophone": ("#FFF1DC", "#F5D9B4", "#C9B6FF", "#AEE3C6"),
  "alarm":      ("#FFF6D6", "#F5E3A8", "#FFB6CC", "#AEE3C6"),
}
def st(w=2.6): return f'stroke="{LINE}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def face(x, y, s=1.0, sleepy=True):
    e = (f'<path d="M-7,-1 Q-5,1.5 -3,-1 M3,-1 Q5,1.5 7,-1" fill="none" stroke="#4A3358" stroke-width="1.7" stroke-linecap="round"/>' if sleepy else
         f'<circle cx="-5" cy="-1" r="2.2" fill="#4A3358"/><circle cx="-5.7" cy="-1.8" r="0.8" fill="#FFF"/><circle cx="5" cy="-1" r="2.2" fill="#4A3358"/><circle cx="4.3" cy="-1.8" r="0.8" fill="#FFF"/>')
    return (f'<g transform="translate({x},{y}) scale({s})">{e}<path d="M-1.8,2.6 Q0,4.2 1.8,2.6" fill="none" stroke="#4A3358" stroke-width="1.4" stroke-linecap="round"/>'
            f'<ellipse cx="-9" cy="2.6" rx="2.6" ry="1.5" fill="#FFB3CB" opacity="0.85"/><ellipse cx="9" cy="2.6" rx="2.6" ry="1.5" fill="#FFB3CB" opacity="0.85"/></g>')

# ---- objects drawn in a 100x100 box; ART = (top, bottom) art extents; HB = hit shapes in box coords
def o_typewriter(c):
    f, f2, a, a2 = c
    return (f'<path d="M22,30 L78,30 L84,46 L16,46 Z" fill="{f2}" {st()}/><rect x="30" y="16" width="40" height="16" rx="2" fill="#FFFFFF" {st(2)}/>'
            f'<path d="M36,22 H64 M36,27 H56" stroke="{LINE}" stroke-width="1.4" opacity="0.5"/>'
            f'<rect x="12" y="44" width="76" height="34" rx="9" fill="{f}" {st()}/><rect x="8" y="36" width="10" height="8" rx="3" fill="{a}" {st(2)}/>'
            + "".join(f'<circle cx="{22 + i*8 + r*4}" cy="{70 if r else 62}" r="2.8" fill="{a2 if (i+r) % 3 else a}" {st(1.4)}/>' for r in (0, 1) for i in range(8 - r))
            + face(50, 52, 0.9) + '<path d="M18,50 Q20,47 24,47" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.8"/>')
def o_crt(c):
    f, f2, a, a2 = c
    return (f'<path d="M42,16 L34,8 M54,16 L62,7" {st(2.2)}/><circle cx="34" cy="8" r="2.6" fill="{a}" {st(1.2)}/><circle cx="62" cy="7" r="2.6" fill="{a}" {st(1.2)}/>'
            f'<path d="M28,74 L25,82 M72,74 L75,82" {st(3.2)}/>'
            f'<rect x="12" y="16" width="76" height="58" rx="13" fill="{f}" {st()}/><rect x="20" y="24" width="50" height="42" rx="11" fill="#BFE6FF" {st(2.2)}/>'
            f'<path d="M26,31 Q30,27 36,28" stroke="#FFF" stroke-width="2.2" fill="none" opacity="0.85" stroke-linecap="round"/>'
            f'<circle cx="80" cy="33" r="3.6" fill="{a}" {st(1.4)}/><circle cx="80" cy="45" r="3.6" fill="{a2}" {st(1.4)}/><path d="M76,58 H84 M76,62 H84" {st(1.4)}/>'
            + face(45, 46, 1.05, False))
def o_phone(c):
    f, f2, a, a2 = c
    dial = "".join(f'<circle cx="{50 + math.cos(math.radians(t))*13:.1f}" cy="{60 + math.sin(math.radians(t))*13:.1f}" r="3" fill="#FFFFFF" {st(1.2)}/>' for t in range(-60, 241, 30))
    return (f'<path d="M82,62 q8,3 5,9 q-5,4 -1,9" fill="none" {st(2)}/>'
            f'<path d="M24,40 Q50,30 76,40 L84,82 Q50,90 16,82 Z" fill="{f}" {st()}/>'
            f'<path d="M14,32 Q14,18 30,20 L70,20 Q86,18 86,32 L80,38 L66,34 L34,34 L20,38 Z" fill="{a}" {st()}/>'
            f'<circle cx="50" cy="60" r="19" fill="{f2}" {st(2)}/>{dial}<circle cx="50" cy="60" r="7" fill="#FFF" {st(1.4)}/>'
            + face(50, 61, 0.55) + '<path d="M22,26 Q24,23 28,23" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.8"/>')
def o_cassette(c):
    f, f2, a, a2 = c
    return (f'<rect x="10" y="26" width="80" height="50" rx="7" fill="{f}" {st()}/><rect x="20" y="34" width="60" height="22" rx="5" fill="#FFFFFF" {st(2)}/>'
            f'<circle cx="35" cy="45" r="7" fill="{f2}" {st(2)}/><circle cx="65" cy="45" r="7" fill="{f2}" {st(2)}/>'
            + "".join(f'<path d="M{cx-3},{45} H{cx+3} M{cx},{42} V{48}" {st(1.2)}/>' for cx in (35, 65))
            + f'<path d="M42,45 H58" stroke="{a}" stroke-width="3"/><path d="M28,76 L32,64 H68 L72,76" fill="{a2}" {st(2)}/>'
            f'<path d="M22,30 H78" stroke="{a}" stroke-width="2.4"/>' + face(50, 46, 0.62)
            + f'<circle cx="16" cy="70" r="1.8" fill="{LINE}"/><circle cx="84" cy="70" r="1.8" fill="{LINE}"/>')
def o_gramophone(c):
    f, f2, a, a2 = c
    return (f'<path d="M22,62 L22,84 Q22,88 26,88 H74 Q78,88 78,84 L78,62 Z" fill="{f}" {st()}/>'
            f'<ellipse cx="50" cy="61" rx="30" ry="5" fill="{f2}" {st(2)}/>'
            f'<path d="M44,60 Q40,40 20,18 Q34,8 52,10 Q70,8 86,14 Q66,34 56,60 Z" fill="{a}" {st()}/>'
            f'<path d="M32,16 Q48,28 50,58 M62,12 Q56,30 52,58" fill="none" stroke="{LINE}" stroke-width="1.4" opacity="0.45"/>'
            f'<path d="M28,18 Q34,14 42,14" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.8"/>'
            + face(50, 75, 0.85))
def o_alarm(c):
    f, f2, a, a2 = c
    return (f'<path d="M32,84 L27,90 M68,84 L73,90" {st(3.2)}/>'
            f'<circle cx="30" cy="21" r="10" fill="{a}" {st()}/><circle cx="70" cy="21" r="10" fill="{a}" {st()}/>'
            f'<rect x="45" y="12" width="10" height="9" rx="2.5" fill="{a2}" {st(1.8)}/>'
            f'<circle cx="50" cy="55" r="33" fill="{f}" {st()}/><circle cx="50" cy="55" r="26" fill="#FFFFFF" {st(2)}/>'
            + "".join(f'<circle cx="{50+math.cos(math.radians(t))*21:.1f}" cy="{55+math.sin(math.radians(t))*21:.1f}" r="1.8" fill="{LINE}"/>' for t in range(0, 360, 30))
            + f'<path d="M50,55 L50,40 M50,55 L60,59" {st(2.6)}/><circle cx="50" cy="55" r="2.4" fill="{a}"/>' + face(50, 66, 0.65)
            + '<path d="M28,40 Q32,32 40,29" stroke="#FFF" stroke-width="2.2" fill="none" stroke-linecap="round" opacity="0.7"/>')
OBJ = {
  "typewriter": (o_typewriter, (16, 78), {"rects": [[30, 16, 40, 16], [16, 30, 68, 16], [12, 44, 76, 34], [8, 36, 10, 8]]}),
  "crt":        (o_crt,        (4, 82),  {"rects": [[12, 16, 76, 58], [24, 72, 52, 8], [31, 5, 7, 11], [58, 4, 7, 12]]}),
  "phone":      (o_phone,      (18, 88), {"rects": [[14, 19, 72, 19], [22, 36, 56, 10], [17, 44, 68, 42]]}),
  "cassette":   (o_cassette,   (26, 76), {"rects": [[10, 26, 80, 50]]}),
  "gramophone": (o_gramophone, (9, 88),  {"rects": [[21, 10, 65, 10], [27, 20, 50, 12], [36, 32, 30, 26], [22, 56, 56, 32]]}),
  "alarm":      (o_alarm,      (11, 90), {"rects": [[45, 12, 10, 10]], "circles": [[50, 55, 33], [30, 21, 9], [70, 21, 9]]}),
}
NOTE = {"typewriter": "paper sheet is solid", "crt": "rabbit-ear antenna tips are solid (2 small rects)", "phone": "curly cord stub on the right is decorative",
        "cassette": "", "gramophone": "horn is stepped in 3 rects", "alarm": "bells + knob solid; little feet decorative"}

def xf(hb, s, ox, oy):
    r = [[round(ox + x*s), round(oy + y*s), round(w*s), round(h*s)] for x, y, w, h in hb.get("rects", [])]
    c = [[round(ox + x*s, 1), round(oy + y*s, 1), round(rr*s, 1)] for x, y, rr in hb.get("circles", [])]
    return r, c
def place(name, s, ox, oy):
    fn = OBJ[name][0]
    return f'<g transform="translate({ox:.2f},{oy:.2f}) scale({s:.4f})">{fn(COL[name])}</g>'

# ---- satin ribbon (tops) ----
RIB, RIB2, RIBL = "#FFC2D6", "#FF9EB8", "#8A5068"
def ribbon_strip(y0, y1):
    s = (f'<rect x="30" y="{y0}" width="20" height="{y1-y0}" fill="{RIB}"/><rect x="43" y="{y0}" width="7" height="{y1-y0}" fill="{RIB2}" opacity="0.8"/>'
         f'<rect x="33" y="{y0}" width="3" height="{y1-y0}" fill="#FFF" opacity="0.65"/>'
         f'<path d="M30,{y0} V{y1} M50,{y0} V{y1}" stroke="{RIBL}" stroke-width="2.2"/>')
    return s
def ribbon_body():
    d = ribbon_strip(-1, 65) + C.tile3('<path d="M31,12 Q40,18 49,12 M31,44 Q40,50 49,44" stroke="#FF9EB8" stroke-width="1.4" fill="none" opacity="0.8"/>'
                                      + sparkle(40, 30, 2, "#FFFFFF", "#D2507A", 0.85))
    return svg(80, 64, d)
def bow(x, y):
    return (f'<path d="M{x},{y} C{x-6},{y-10} {x-20},{y-10} {x-18},{y} C{x-20},{y+10} {x-6},{y+8} {x},{y} Z" fill="{RIB}" stroke="{RIBL}" stroke-width="2"/>'
            f'<path d="M{x},{y} C{x+6},{y-10} {x+20},{y-10} {x+18},{y} C{x+20},{y+10} {x+6},{y+8} {x},{y} Z" fill="{RIB}" stroke="{RIBL}" stroke-width="2"/>'
            f'<rect x="{x-4}" y="{y-4}" width="8" height="8" rx="3" fill="{RIB2}" stroke="{RIBL}" stroke-width="1.8"/>')

# ---- cotton-candy cloud (bottoms) ----
CL = ("#FFFFFF", "#FFE3F0", "#E9DDFB")
def puffs(cy_list, x0=10, x1=70):
    s = []
    for i, cy in enumerate(cy_list):
        for j, (cx, r) in enumerate(((x0 + 8, 14), (40, 18), (x1 - 8, 14))):
            s.append(f'<circle cx="{cx}" cy="{cy + (j % 2) * -3}" r="{r}" fill="{CL[(i + j) % 3]}" stroke="#C9B6E8" stroke-width="2.2"/>')
    return "".join(s)
def cloud_body():
    core = f'<rect x="10" y="-2" width="60" height="68" fill="#FFF2F8"/>'
    d = core + C.tile3(puffs([8, 40]) + sparkle(24, 24, 2.2, "#FFFFFF", "#C9B6E8") + sparkle(56, 54, 1.8, "#FFF4B8", "#D9953A"))
    return svg(80, 64, f'<clipPath id="cbc"><rect x="0" y="0" width="80" height="64"/></clipPath><g clip-path="url(#cbc)">{d}</g>')

# ---- build obstacles ----
def seat_y(h):
    ys = [y for x, y, w, hh in h.get("rects", []) if x <= 40 < x + w] + [cy - r for cx, cy, r in h.get("circles", []) if abs(cx - 40) < r]
    return round(min(ys))
def build_obstacles():
    for n, (fn, (at, ab), hb) in OBJ.items():
        hts = [y for x, y, w, h in hb.get("rects", [])] + [y - r for x, y, r in hb.get("circles", [])]
        hbs = [y + h for x, y, w, h in hb.get("rects", [])] + [y + r for x, y, r in hb.get("circles", [])]
        Ht, Hb = min(hts), max(hbs)
        s = min(0.72, 54 / (ab - at)); ox = 40 - 50 * s
        # TOP: ribbon + bow + object; object art bottom at y=77
        oy = 77 - ab * s; rib_end = round(oy + Ht * s + 6)
        cap = (ribbon_strip(-1, rib_end) + place(n, s, ox, oy) + bow(40, round(oy + Ht * s + 1))
               + sparkle(12, 30, 2.4, "#FFF4B8", "#D9953A") + sparkle(68, 22, 2, "#FFFFFF", "#9E94B8"))
        r, c = xf(hb, s, ox, oy)
        hcap = {"rects": [[28, 0, 24, rib_end]] + r}
        if c: hcap["circles"] = c
        C.reg_top(f"obs-void-{n}-top", ribbon_body(), svg(80, 80, cap), {"rects": [[28, 0, 24, 64]]}, hcap,
                  note=f"satin ribbon (24px solid) from the cloud-bank ceiling; bow and sparkles decorative; {NOTE[n]}".rstrip("; "))
        # BOTTOM: object sitting on a cloud; hit top ~ y 6
        oy = 6 - Ht * s; yc = round(oy + Hb * s - 7)
        cap = (f'<rect x="10" y="{yc+8}" width="60" height="{82-yc-8}" fill="#FFF2F8"/>' + puffs([yc + 12, yc + 40, yc + 66]) + place(n, s, ox, oy)
               + sparkle(14, yc - 2, 2.4, "#FFF4B8", "#D9953A") + sparkle(68, yc + 2, 2, "#FFFFFF", "#9E94B8"))
        # front lip of cloud over the object's base
        cap += "".join(f'<circle cx="{cx}" cy="{yc+10}" r="{rr}" fill="#FFFFFF" stroke="#C9B6E8" stroke-width="2.2"/>' for cx, rr in ((20, 9), (60, 9)))
        r, c = xf(hb, s, ox, oy)
        hcap = {"rects": r + [[10, yc, 60, 80 - yc]], "circles": c + [[20, yc + 6, 10], [60, yc + 6, 10]]}
        C.reg_bot(f"obs-void-{n}-bottom", cloud_body(), svg(80, 80, cap), {"rects": [[10, 0, 60, 64]]}, hcap, [40, seat_y(hcap)],
                  note=f"cotton-candy cloud stack (60px solid); cloud side bumps and sparkles decorative; {NOTE[n]}".rstrip("; "))

# ---- backgrounds ----
TW, H = 720, 640
def cloud_edge(y0, top=True, cols=("#FFFFFF", "#FFE3F0", "#E9DDFB"), op=0.9, seed=0):
    """periodic cotton-candy bank along the top (hanging) or bottom of the tile, seamless over 720"""
    s = []
    for row in range(2):
        for i in range(-1, 19):
            x = i * 40 + row * 20
            r = 26 + 8 * math.sin(2 * math.pi * (x % TW) / TW * 3 + seed) + 5 * math.sin(2 * math.pi * (x % TW) / TW * 5 + row)
            y = (y0 - row * 14 + 6 * math.sin(2 * math.pi * (x % TW) / TW * 2)) if top else (y0 + row * 14 - 6 * math.sin(2 * math.pi * (x % TW) / TW * 2))
            s.append(f'<circle cx="{x}" cy="{y:.1f}" r="{r:.1f}" fill="{cols[(i + row) % 3]}" opacity="{op}"/>')
    band = f'<rect x="0" y="{0 if top else y0}" width="{TW}" height="{y0 if top else H - y0}" fill="{cols[0]}" opacity="{op}"/>'
    return band + "".join(s)
def mini_obj(name, x, y, sc, rot, op):
    fn = OBJ[name][0]
    return f'<g opacity="{op}" transform="translate({x},{y}) rotate({rot}) scale({sc}) translate(-50,-50)">{fn(COL[name])}</g>'
def bg_void():
    S, E = B.S, B.E
    far = dict(sky=SKY, band=None,
               els=B.stars(71, 150, 630, ("#FFF6D6", "#E3D4FF", "#FFD6E4", "#BFE6FF"), 12) +
                   [S(0, 720, lambda x, b: (B.nebula(x + 120, 160, 240, 120, "#FFB6D9", 0.32) + B.nebula(x + 470, 380, 260, 150, "#C9B6FF", 0.34)
                                           + B.nebula(x + 640, 120, 160, 90, "#A9E4FF", 0.25) + B.nebula(x + 280, 520, 200, 90, "#FFC9A0", 0.18)))])
    mid_items = [("alarm", 90, 210, 0.36, -14), ("cassette", 260, 430, 0.34, 18), ("crt", 420, 150, 0.38, 8), ("gramophone", 600, 360, 0.36, -10), ("phone", 700, 520, 0.3, 12)]
    mid = dict(band=None, els=[S(x - 40, 80, (lambda X, b, n=n, y=y, sc=sc, r=r, x0=x: mini_obj(n, X + 40, y, sc, r, 0.42))) for n, x, y, sc, r in mid_items]
               + [S(x - 60, 120, (lambda X, b, y=y, w=w: f'<ellipse cx="{X+60}" cy="{y}" rx="{w}" ry="{w*0.32:.0f}" fill="#FFFFFF" opacity="0.13"/>')) for x, y, w in ((160, 300, 110), (520, 240, 130), (380, 560, 120))])
    near_items = [S(x, 10, (lambda X, b, y=y, r=r: sparkle(round(X, 1), y, r, "#FFF8DC", "#F2D48A", 0.9, 0.5))) for x, y, r in ((40, 140, 3), (200, 470, 3.6), (330, 90, 2.6), (480, 330, 3.2), (640, 500, 2.8), (560, 180, 2.4))]
    near_items += [S(x, 20, (lambda X, b, y=y, k=k: f'<g transform="translate({X:.0f},{y}) scale(1.1)" opacity="0.65"><path d="M0,0 V-12 L8,-14 V-2" fill="none" stroke="#FFE3F0" stroke-width="1.8"/><ellipse cx="-2" cy="0" rx="3" ry="2.2" fill="#FFE3F0"/>{"" if k else ""}<ellipse cx="6" cy="-2" rx="3" ry="2.2" fill="#FFE3F0"/></g>')) for x, y, k in ((120, 260, 0), (420, 420, 1), (690, 230, 0))]
    near = dict(band=None, els=near_items)
    B.STAGES["void"] = {"far": far, "mid": mid, "near": near}
    for layer in ("far", "mid", "near"):
        t = B.render_tile("void", layer)
        if layer == "near":  # cloud banks: ceiling (y 0..34) and floor (y 590..640), periodic
            t = t.replace("</svg>", cloud_edge(26, True, seed=0.5) + cloud_edge(604, False, seed=1.7) + "</svg>")
        FILES[f"bg-void-{layer}"] = t
def nested(svgtxt, mask=None):
    inner = svgtxt[svgtxt.index(">") + 1: svgtxt.rindex("</svg>")]
    return f'<g{(" mask=" + chr(34) + "url(#" + mask + ")" + chr(34)) if mask else ""}>{inner}</g>'
def uniq(svgtxt, p):  # prefix ids to avoid clashes when nesting two tiles
    import re
    return re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', svgtxt))
def trans_tiles():
    for layer in ("far", "mid", "near"):
        a = uniq(open(os.path.join(OUT, f"bg-space-{layer}.svg")).read(), "sa_"); b = uniq(FILES[f"bg-void-{layer}"], "vb_")
        stops = "".join(f'<stop offset="{t:.2f}" stop-color="#FFFFFF" stop-opacity="{B.wfun(t*TW):.3f}"/>' for t in [i / 20 for i in range(21)])
        stops_inv = "".join(f'<stop offset="{t:.2f}" stop-color="#FFFFFF" stop-opacity="{1-B.wfun(t*TW):.3f}"/>' for t in [i / 20 for i in range(21)])
        g = (f'<defs><linearGradient id="tm" x1="0" y1="0" x2="{TW}" y2="0" gradientUnits="userSpaceOnUse">{stops}</linearGradient>'
             f'<linearGradient id="tmi" x1="0" y1="0" x2="{TW}" y2="0" gradientUnits="userSpaceOnUse">{stops_inv}</linearGradient>'
             f'<mask id="mb" maskUnits="userSpaceOnUse" x="0" y="0" width="{TW}" height="{H}"><rect width="{TW}" height="{H}" fill="url(#tm)"/></mask>'
             f'<mask id="ma" maskUnits="userSpaceOnUse" x="0" y="0" width="{TW}" height="{H}"><rect width="{TW}" height="{H}" fill="url(#tmi)"/></mask></defs>')
        g += (nested(a, None if layer == "far" else "ma") + nested(b, "mb"))
        if layer != "far":  # pastel mist puffs in the middle (kept away from both edges)
            random.seed(3 if layer == "mid" else 4)
            for _ in range(14 if layer == "mid" else 9):
                x, y, r = random.uniform(240, 480), random.uniform(40, 600), random.uniform(30, 70)
                g += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{random.choice(["#FFE3F0", "#E9DDFB", "#DFF3FF"])}" opacity="{0.22 if layer=="mid" else 0.3}"/>'
        FILES[f"bg-trans-space-void-{layer}"] = f'<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{H}" viewBox="0 0 {TW} {H}">{g}</svg>'
def mist_overlay(i, n=8):
    """360x640 full-screen overlay; t 0..1. 0-0.5 mist blooms (stars blur), 0.5-1 ribbons drift in and the mist thins."""
    t = i / (n - 1); random.seed(21); g = []
    a = math.sin(math.pi * min(1, t / 0.75)) if t < 0.75 else (1 - t) / 0.25 * 1.0
    a = max(0.0, min(1.0, a))
    g.append(f'<rect width="360" height="640" fill="#E9DDFB" opacity="{0.35*a:.2f}"/>')
    for k in range(22):
        x, y, r = random.uniform(-40, 400), random.uniform(-40, 680), random.uniform(50, 120)
        c = random.choice(["#FFE3F0", "#E9DDFB", "#DFF3FF", "#FFFFFF"])
        g.append(f'<circle cx="{x + (t - 0.5) * 30 * (1 if k % 2 else -1):.0f}" cy="{y:.0f}" r="{r * (0.7 + 0.5 * t):.0f}" fill="{c}" opacity="{0.42*a:.2f}"/>')
    if t >= 0.4:  # ribbons with little bows drift down from the top
        k = (t - 0.4) / 0.6
        for x, L in ((70, 200), (190, 140), (300, 240)):
            y1 = -20 + L * k * 1.1
            g.append(ribbon_strip(-2, y1).replace('x="30"', f'x="{x-10}"').replace('x="43"', f'x="{x+3}"').replace('x="33"', f'x="{x-7}"').replace("M30,", f"M{x-10},").replace("M50,", f"M{x+10},")
                     + bow(x, y1))
        for j in range(6):
            g.append(sparkle(40 + j * 55, 80 + (j % 3) * 120 + 40 * k, 3 + (j % 2), "#FFF4B8", "#D9953A", min(1, k * 1.5)))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="640" viewBox="0 0 360 640">{"".join(g)}</svg>'

# ---- UI: banner, badge, burst ----
def ui():
    V.STAGE_NAMES["void"] = "The Void"
    V.BANNER_COL["void"] = ("#E9DDFB", "#FFC2D6", "#5E4A8A")
    om, ob = V.motif, V.burst_item
    def motif(stage):
        if stage != "void": return om(stage)
        return (f'<g transform="translate(4,2) scale(0.36)">{o_alarm(COL["alarm"])}</g><g transform="translate(260,6) scale(0.34)">{o_cassette(COL["cassette"])}</g>'
                + sparkle(46, 12, 3.4, "#FFF4B8", "#D9953A") + sparkle(254, 14, 3, "#FFFFFF", "#9E94B8"))
    def burst_item(stage, k, x, y, a, sc):
        if stage != "void": return ob(stage, k, x, y, a, sc)
        t = f'transform="translate({x:.1f},{y:.1f}) rotate({a:.0f}) scale({sc:.2f})"'
        m = k % 4
        if m == 0: return f'<g {t}><path d="M0,4 V-8 L8,-10 V2" fill="none" stroke="#6B4E7A" stroke-width="1.6"/><ellipse cx="-2" cy="4" rx="3" ry="2.3" fill="#FFB6CC" stroke="#6B4E7A" stroke-width="1.2"/><ellipse cx="6" cy="2" rx="3" ry="2.3" fill="#C9B6FF" stroke="#6B4E7A" stroke-width="1.2"/></g>'
        if m == 1: return f'<g {t}><g transform="scale(0.2) translate(-50,-50)">{o_cassette(COL["cassette"])}</g></g>'
        if m == 2: return f'<g {t}><path d="M-9,0 Q-4,-6 0,0 Q4,6 9,0" fill="none" stroke="#FF9EB8" stroke-width="4" stroke-linecap="round"/></g>'
        return f'<g {t}>{V.star5(0, 0, 6, ["#FFE9A8", "#E3D4FF", "#BFE6FF"][k % 3], "#7A5A9E")}</g>'
    V.motif, V.burst_item = motif, burst_item
    FILES["ui-banner-void"] = V.banner("void", "The Void"); FILES["ui-banner-void-blank"] = V.banner("void")
    FILES["ui-stage-badge-7"] = V.badge(7)
    STRIPS["fx-burst-void"] = []
    for i in range(6): FILES[f"fx-burst-void-{i}"] = V.burst("void", i); STRIPS["fx-burst-void"].append(f"fx-burst-void-{i}")

# ---- v0.6 memory-lite Void backgrounds (Code: 49.6MB peak @2x in the warp vs a 30MB budget) ----
# Full-height 720x640 tiles are kept as bg-void-{far,mid,near}-full backups. Lite set (all seamless over 720 px):
#   far  = sky gradient (Code: sky-palettes.json void, or the 8x64 bg-void-far-sky tile stretched)
#          + bg-void-far-nebula (pre-squashed 360x80, drawn STRETCHED to 720x640: soft radial blobs survive)
#          + bg-void-far-stars (240x240, repeat in x AND y)
#   mid  = bg-void-mid-upper (y 128, h 320) + bg-void-mid-lower (y 504, h 96): crops of the same tile
#   near = bg-void-near-ceil (y 0, h 72) + bg-void-near-floor (y 556, h 84) + 9 tiny glint sprites (placements in hitboxes.json)
LITE = {}
VOID_NEB = lambda x, b: (B.nebula(x + 120, 160, 240, 120, "#FFB6D9", 0.32) + B.nebula(x + 470, 380, 260, 150, "#C9B6FF", 0.34)
                         + B.nebula(x + 640, 120, 160, 90, "#A9E4FF", 0.25) + B.nebula(x + 280, 520, 200, 90, "#FFC9A0", 0.18))
SPARKLES = [(40, 140, 3), (200, 470, 3.6), (330, 90, 2.6), (480, 330, 3.2), (640, 500, 2.8), (560, 180, 2.4)]
NOTES = [(120, 260), (420, 420), (690, 230)]
def _inner(t): return t[t.index(">") + 1: t.rindex("</svg>")]
def band(full, y0, h): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{h}" viewBox="0 {y0} {TW} {h}">{_inner(full)}</svg>'
def note_svg(x, y): return (f'<g transform="translate({x},{y}) scale(1.1)" opacity="0.65"><path d="M0,0 V-12 L8,-14 V-2" fill="none" stroke="#FFE3F0" stroke-width="1.8"/>'
                            f'<ellipse cx="-2" cy="0" rx="3" ry="2.2" fill="#FFE3F0"/><ellipse cx="6" cy="-2" rx="3" ry="2.2" fill="#FFE3F0"/></g>')
def bg_void_lite():
    S = B.S
    # far: nebula only (no sky, no stars), squashed 2x horizontally / 8x vertically
    B.STAGES["void_neb"] = {"far": dict(band=None, els=[S(0, 720, VOID_NEB)])}
    neb = B.render_tile("void_neb", "far"); del B.STAGES["void_neb"]
    LITE["bg-void-far-nebula"] = dict(svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="80" viewBox="0 0 {TW} {H}" preserveAspectRatio="none">{_inner(neb)}</svg>',
                                      y=0, drawW=TW, drawH=H, note="draw stretched to 720x640 world px with image smoothing ON")
    LITE["bg-void-far-sky"] = dict(svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="8" height="64" viewBox="0 0 8 64" preserveAspectRatio="none"><linearGradient id="vs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY[0]}"/><stop offset="1" stop-color="{SKY[1]}"/></linearGradient><rect width="8" height="64" fill="url(#vs)"/></svg>',
                                   y=0, drawW=TW, drawH=H, note="optional: same as a canvas linear gradient sky-palettes.json void top->bottom over y 0..640")
    # far stars: 360x320 tile, repeats exactly 2 x 2 per 720x640 tile slot (density matches the old 150 stars + 12 sparkles)
    r = random.Random(77); TX, TY = 360, 320; g = []
    cols = ("#FFF6D6", "#E3D4FF", "#FFD6E4", "#BFE6FF")
    def far_enough(x, y, pts, dmin):  # toroidal distance, keeps sparkles from clumping into a visible repeat
        return all(min(abs(x - a), TX - abs(x - a)) ** 2 + min(abs(y - b), TY - abs(y - b)) ** 2 > dmin ** 2 for _, a, b, *_ in pts)
    pts = []
    while len(pts) < 3:
        x, y = r.uniform(0, TX), r.uniform(0, TY)
        if far_enough(x, y, pts, 150): pts.append(("spk", x, y, r.choice([2.2, 2.8, 3.4]), None, None))
    while len(pts) < 3 + 39:
        x, y = r.uniform(0, TX), r.uniform(0, TY)
        if far_enough(x, y, pts, 14): pts.append(("dot", x, y, r.choice([0.7, 0.9, 1.1, 1.4]), r.choice(cols), r.uniform(0.45, 0.95)))
    for kind, x, y, rr, c, op in pts:
        for dx in (-TX, 0, TX):
            for dy in (-TY, 0, TY):
                X, Y = x + dx, y + dy
                if -6 < X < TX + 6 and -6 < Y < TY + 6:
                    g.append(B.star_dot(X, Y, rr, c, op) if kind == "dot" else sparkle(round(X, 1), round(Y, 1), rr, "#FFF8DC", "#F2D48A", 0.9, 0.4))
    LITE["bg-void-far-stars"] = dict(svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{TX}" height="{TY}" viewBox="0 0 {TX} {TY}">{"".join(g)}</svg>',
                                     y=0, repeat="xy", note="repeat 2 x 2 to fill the 720x640 tile slot (x 0/360, y 0/320), scroll with the far layer")
    # mid: two bands cut from the unchanged mid tile
    mid = FILES["bg-void-mid"]
    LITE["bg-void-mid-upper"] = dict(svg=band(mid, 128, 320), y=128, note="clock, CRT, cassette, gramophone silhouettes + 2 mist ovals")
    LITE["bg-void-mid-lower"] = dict(svg=band(mid, 504, 96), y=504, note="phone silhouette + low mist oval")
    # near: cloud banks only (glints become sprites)
    B.STAGES["void_near"] = {"near": dict(band=None, els=[])}
    near = B.render_tile("void_near", "near"); del B.STAGES["void_near"]
    near = near.replace("</svg>", cloud_edge(26, True, seed=0.5) + cloud_edge(604, False, seed=1.7) + "</svg>")
    LITE["bg-void-near-ceil"] = dict(svg=band(near, 0, 72), y=0, note="cotton-candy ceiling bank")
    LITE["bg-void-near-floor"] = dict(svg=band(near, 556, 84), y=556, note="cotton-candy floor bank")
    LITE["bg-void-near-glint-sparkle"] = dict(svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12">{sparkle(6, 6, 4, "#FFF8DC", "#F2D48A", 0.9, 0.5)}</svg>',
                                              anchor=[6, 6], note="sparkle r=4 at scale 1; scale = r/4")
    LITE["bg-void-near-glint-note"] = dict(svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">{note_svg(6, 17)}</svg>',
                                           anchor=[6, 17], note="music note, 65% alpha baked in")
    for k, v in LITE.items(): FILES[k] = v["svg"]
def lite_json():
    sz = lambda k, sc: Image.open(os.path.join(OUT, f"png/{sc}x", k + ".png")).size
    ent = lambda k: {kk: vv for kk, vv in dict(file=k + ".png", size1x=list(sz(k, 1)), size2x=list(sz(k, 2)), **{a: b for a, b in LITE[k].items() if a != "svg"}).items()}
    glints = ([dict(sprite="bg-void-near-glint-sparkle", x=x, y=y, scale=round(rr / 4, 2)) for x, y, rr in SPARKLES]
              + [dict(sprite="bg-void-near-glint-note", x=x, y=y, scale=1.0) for x, y in NOTES])
    hp = os.path.join(OUT, "hitboxes.json"); Hj = json.load(open(hp)); bgj = Hj["backgrounds"]
    if "void" not in bgj["stages"]: bgj["stages"].append("void")
    bgj["scroll"]["void"] = {"far": 0.05, "mid": 0.15, "near": 0.5}
    bgj["void"] = {
      "_note": "v0.6 memory-lite set (ASSETS.md 14.2). NOT the plain bg-void-{layer}.png 720x640 tiles: each layer is a stack of parts drawn at "
               "world y offsets inside the 720-wide tile slot (tileWidth 720, seamless in x). The full-height originals stay as "
               "bg-void-{far,mid,near}-full.* backups (and the old bg-void-{layer}.* names are left in place until Code switches).",
      "far": [dict(kind="gradient", top=SKY[0], bottom=SKY[1], y=0, h=640, alt="bg-void-far-sky.png"),
              ent("bg-void-far-nebula"), ent("bg-void-far-stars")],
      "mid": [ent("bg-void-mid-upper"), ent("bg-void-mid-lower")],
      "near": [ent("bg-void-near-ceil"), ent("bg-void-near-floor"),
               dict(kind="sprites", sprites={k: ent(k) for k in ("bg-void-near-glint-sparkle", "bg-void-near-glint-note")},
                    placements=glints, note="x,y = sprite anchor in world px within the 720 tile period")],
      "transitions": "none: bg-trans-space-void-* are deprecated/optional. Swap space -> void layers under bg-trans-space-void-mist frame 3.",
    }
    json.dump(Hj, open(hp, "w"), indent=2)

STAGE_TOPS = {f"obs-void-{n}-top": w for n, w in (("typewriter", 1), ("crt", 2), ("phone", 2), ("cassette", 1), ("gramophone", 1), ("alarm", 2))}
STAGE_BOTS = {f"obs-void-{n}-bottom": w for n, w in (("typewriter", 2), ("crt", 2), ("phone", 1), ("cassette", 1), ("gramophone", 1), ("alarm", 1))}
def merge_json():
    hp = os.path.join(OUT, "hitboxes.json"); Hj = json.load(open(hp))
    Hj.update(HIT); Hj["columns"].update(EDGES)
    Hj["columns"]["_stageTopsVoid"] = dict(STAGE_TOPS, note="stage 7 'void' TOP (ceiling) set: column id -> suggested weight (Tuning owns weights). Tops use -body + -cap-bottom only (satin ribbon + hanging object).")
    Hj["columns"]["_stageBottomsVoid"] = dict(STAGE_BOTS, note="stage 7 'void' BOTTOM (floor) set: column id -> suggested weight. Bottoms use -body + -cap-top only (cotton-candy cloud + object).")
    json.dump(Hj, open(hp, "w"), indent=2)
    sp = os.path.join(OUT, "sky-palettes.json"); S = json.load(open(sp)); S["void"] = {"top": SKY[0], "bottom": SKY[1]}; json.dump(S, open(sp, "w"), indent=2)
    dp = os.path.join(OUT, "death-map.json"); Dm = json.load(open(dp))
    for n in OBJ:
        Dm[f"obs-void-{n}-top"] = "generic"
        Dm[f"obs-void-{n}-bottom"] = "tombstone"
    Dm["_voidNote"] = "void: hanging tops (soft ribbon + swinging object) -> generic bonk/poof, like the other v0.4 hanging tops; bottoms are hard retro objects bumped head-on -> tombstone (see-stars)"
    json.dump(Dm, open(dp, "w"), indent=2)

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
            sh.save(os.path.join(OUT, d, name + "-strip.png"))

def build():
    C.FILES.clear(); C.HIT.clear(); C.EDGES.clear()
    build_obstacles(); FILES.update(C.FILES); HIT.update(C.HIT); EDGES.update(C.EDGES)
    bg_void(); trans_tiles()
    STRIPS["bg-trans-space-void-mist"] = []
    for i in range(8): FILES[f"bg-trans-space-void-mist-{i}"] = mist_overlay(i); STRIPS["bg-trans-space-void-mist"].append(f"bg-trans-space-void-mist-{i}")
    ui()

if __name__ == "__main__":
    if "--bg-lite" in sys.argv:  # only the v0.6 lite Void backgrounds + hitboxes.json backgrounds.void
        bg_void(); keep = {k: FILES[k] for k in ("bg-void-mid",)}; bg_void_lite()
        for k in list(FILES):
            if k not in LITE: del FILES[k]
        STRIPS.clear(); export(); lite_json(); print(len(FILES), "lite files"); sys.exit()
    build(); bg_void_lite(); export(); merge_json(); lite_json()
    print(len(FILES), "svgs"); [print(k, v.get("ceilEdge", v.get("floorEdge")), v.get("pumpkinSeat", "")) for k, v in EDGES.items()]
