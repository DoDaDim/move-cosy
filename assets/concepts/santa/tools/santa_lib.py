"""Shared helpers for the Santa's Rocket Run stage set (concept folder, NOT wired into the game).
Column conventions are the ghost game's v0.4/v0.5/Void ones (ASSETS.md 11-14):
  80px canvas, 72px footprint (x 4..76); -body 80x64 tiles vertically, hitbox = exactly ONE rect;
  caps 80x80; TOP columns = body + cap-bottom (cap attaches at y=0, gap edge = ceilEdge);
  BOTTOM columns = cap-top + body (cap attaches at y=80, gap edge = floorEdge)."""
import os, io, sys, math, random, cairosvg
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import build_santa_concepts as K
from build_santa_concepts import L, EYE, EYE2, BLUSH, MOUTH, RED, RED2, RED_D, FUR, FUR2, SKIN, GOLD, GOLD2, MINT, MINT2, SACK, SACK2, BOOT, DEFS, FONT
SANTA = os.path.dirname(HERE); OUT = os.path.join(SANTA, "stages")
FILES, HIT, EDGES, STRIPS = {}, {}, {}, {}   # name -> svg ; name -> hitbox ; column id -> record ; strip name -> [frame names]

def svg(w, h, inner): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{inner}</svg>'
def st(w=2.0, c=L): return f'stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def _s(sw, extra): return "" if (not sw or "stroke=" in extra) else st(sw)
def R(x, y, w, h, fill, sw=2, rx=0, extra=""): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {_s(sw, extra)} {extra}/>'
def P(d, fill, sw=2, extra=""): return f'<path d="{d}" fill="{fill}" {_s(sw, extra)} {extra}/>'
def C(x, y, r, fill, sw=2, extra=""): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {_s(sw, extra)} {extra}/>'
def E(x, y, rx, ry, fill, sw=2, extra=""): return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" {_s(sw, extra)} {extra}/>'
def hl(x1, y1, x2, y2, w=1.6, op=0.75): return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="#FFF" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
def face(cx, cy, k=0.45, eyes="open", mouth="w"): return K.face(cx, cy, k, eyes, mouth)
def tile3(inner): return inner + f'<g transform="translate(0,-64)">{inner}</g><g transform="translate(0,64)">{inner}</g>'
def sparkle(x, y, r, fill="#FFF4B8", line="#D9953A", op=1.0):
    return (f'<path d="M{x},{y-r} Q{x+r*0.22},{y-r*0.22} {x+r},{y} Q{x+r*0.22},{y+r*0.22} {x},{y+r} Q{x-r*0.22},{y+r*0.22} {x-r},{y} Q{x-r*0.22},{y-r*0.22} {x},{y-r} Z" '
            f'fill="{fill}" stroke="{line}" stroke-width="{max(0.6, r*0.16):.2f}" opacity="{op}"/>')
def flake(x, y, r, col="#FFFFFF", line="#7FA8D8", rot=0, w=None):
    d = ""
    for i in range(6):
        a = math.radians(rot + i * 60); ex, ey = x + math.cos(a) * r, y + math.sin(a) * r
        mx, my = x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55
        d += f"M{x:.1f},{y:.1f} L{ex:.1f},{ey:.1f} "
        for dd in (-50, 50):
            b = a + math.radians(dd); d += f"M{mx:.1f},{my:.1f} L{mx+math.cos(b)*r*0.32:.1f},{my+math.sin(b)*r*0.32:.1f} "
    w = w or max(1.0, r * 0.22)
    return (f'<path d="{d}" stroke="{line}" stroke-width="{w+1.4:.1f}" stroke-linecap="round" fill="none"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w:.1f}" stroke-linecap="round" fill="none"/>')
def star5(x, y, r, fill=GOLD, line="#B07A3A", sw=1.6, rot=-90):
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36); rr = r if i % 2 == 0 else r * 0.48
        pts.append(f"{x+math.cos(a)*rr:.1f},{y+math.sin(a)*rr:.1f}")
    return f'<path d="M{" L".join(pts)} Z" fill="{fill}" stroke="{line}" stroke-width="{sw}" stroke-linejoin="round"/>'
def snowcap(x0, x1, y, depth=6, sw=1.6):
    """soft snow pile sitting on a horizontal edge at y, from x0 to x1"""
    n = max(2, int((x1 - x0) / 14)); w = (x1 - x0) / n; d = f"M{x0-2},{y+2} "
    for i in range(n): d += f"Q{x0+w*(i+0.5):.1f},{y-depth-(i%2)*2} {x0+w*(i+1):.1f},{y} "
    d += f"L{x1+2},{y+3} Q{(x0+x1)/2},{y+5} {x0-2},{y+2} Z"
    return P(d, "#FFFFFF", sw) + f'<path d="M{x0+4},{y-depth*0.5} Q{(x0+x1)/2},{y-depth} {x1-6},{y-depth*0.4}" stroke="#E6F2FF" stroke-width="1.6" fill="none"/>'
def icicles(x0, x1, y, lens, col="#CFEAFF", sw=1.6):
    n = len(lens); w = (x1 - x0) / n; s = ""
    for i, l in enumerate(lens):
        cx = x0 + w * (i + 0.5); hw = w * 0.42
        s += P(f"M{cx-hw:.1f},{y-1} L{cx:.1f},{y+l} L{cx+hw:.1f},{y-1} Z", col, sw) + hl(cx - hw * 0.4, y + 2, cx - 0.5, y + l * 0.6, 1.2, 0.8)
    return s

# ---------- edge maths + registration (same rules as tools/v04_common.py) ----------
def edge_top(h): return min([y for (x, y, w, hh) in h.get("rects", [])] + [cy - r for (cx, cy, r) in h.get("circles", [])])
def edge_bot(h): return max([y + hh for (x, y, w, hh) in h.get("rects", [])] + [cy + r for (cx, cy, r) in h.get("circles", [])])
def check(name, h, body=False):
    for (x, y, w, hh) in h.get("rects", []):
        assert 4 <= x and x + w <= 76, (name, "rect outside column footprint", x, w)
        assert 0 <= y and y + hh <= (64 if body else 80), (name, "rect outside canvas", y, hh)
    for (cx, cy, r) in h.get("circles", []):
        assert 4 <= cx - r and cx + r <= 76, (name, "circle outside column footprint", cx, r)
        assert 0 <= cy - r and cy + r <= 80, (name, "circle outside canvas", cy, r)
    if body: assert len(h["rects"]) == 1 and not h.get("circles"), (name, "body must be ONE rect")
def hb(rects, circles=()):
    d = {"rects": [list(r) for r in rects]}
    if circles: d["circles"] = [list(c) for c in circles]
    return d
def reg_top(name, stage, body, cap, hb_body, hb_cap, anchor, death, note=None):
    check(name + "-body", hb_body, True); check(name + "-cap-bottom", hb_cap)
    FILES[name + "-body"], FILES[name + "-cap-bottom"] = svg(80, 64, body), svg(80, 80, cap)
    HIT[name + "-body"], HIT[name + "-cap-bottom"] = hb_body, hb_cap
    e = {"files": name + "-{body,cap-bottom}", "side": "top", "stage": stage, "ceilEdge": edge_bot(hb_cap), "anchor": anchor, "death": death}
    if note: e["note"] = note
    EDGES[name] = e
def reg_bot(name, stage, body, cap, hb_body, hb_cap, seat, death, note=None):
    check(name + "-body", hb_body, True); check(name + "-cap-top", hb_cap)
    FILES[name + "-body"], FILES[name + "-cap-top"] = svg(80, 64, body), svg(80, 80, cap)
    HIT[name + "-body"], HIT[name + "-cap-top"] = hb_body, hb_cap
    e = {"files": name + "-{body,cap-top}", "side": "bottom", "stage": stage, "floorEdge": edge_top(hb_cap), "pumpkinSeat": seat, "death": death}
    if note: e["note"] = note
    EDGES[name] = e

# ---------- render / export ----------
def png(s, w=None, h=None): return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=w, output_height=h))).convert("RGBA")
def size_of(s):
    import re; m = re.search(r'width="(\d+)" height="(\d+)"', s); return int(m.group(1)), int(m.group(2))
def export_all():
    for d in ("svg", "png/1x", "png/2x"): os.makedirs(os.path.join(OUT, d), exist_ok=True)
    cache = {}
    for name, s in FILES.items():
        open(os.path.join(OUT, "svg", name + ".svg"), "w").write(s)
        w, h = size_of(s)
        for k, d in ((1, "png/1x"), (2, "png/2x")):
            im = png(s, w * k, h * k); im.save(os.path.join(OUT, d, name + ".png"), optimize=True); cache[(name, k)] = im
    for sname, frames in STRIPS.items():
        for k, d in ((1, "png/1x"), (2, "png/2x")):
            ims = [cache[(f, k)] for f in frames]; W, H = ims[0].size
            strip = Image.new("RGBA", (W * len(ims), H))
            for i, im in enumerate(ims): strip.paste(im, (i * W, 0))
            strip.save(os.path.join(OUT, d, sname + ".png"), optimize=True)
    return cache
