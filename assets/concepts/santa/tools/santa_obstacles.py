"""Santa's Rocket Run column obstacles: 8 stages x (3 tops + 3 bottoms).
David's rule for TOPS: every top must make physical sense - an anchor is drawn in (girder, ledge, branch, wire,
envelope, cloud) or it is a genuine sky object. Nothing floats from nowhere and nothing is a flipped ground object."""
import math
from santa_lib import *

# ======================================================================= TOP FAMILIES
def wave_band(cx, w, y0, y1, ph, col, op=0.85, hem=None):
    pts_l, pts_r = [], []
    y = y0
    while y <= y1 + 0.01:
        dx = 3 * math.sin(2 * math.pi * y / 64 + ph)
        pts_l.append((cx - w / 2 + dx, y)); pts_r.append((cx + w / 2 + dx, y)); y += 4
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts_l)
    if hem: d += f" Q{cx:.1f},{y1 + hem} {pts_r[-1][0]:.1f},{pts_r[-1][1]:.1f}"
    d += " L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in reversed(pts_r)) + " Z"
    return f'<path d="{d}" fill="{col}" opacity="{op}" stroke="{L}" stroke-width="1.4" stroke-opacity="0.45"/>'

def curtain(c):
    """aurora curtain: the sky itself (Lapland / Antarctica)"""
    a, b, s = c["c1"], c["c2"], c["c3"]
    def bands(y1, hem=None, h2=None):
        g = wave_band(22, 18, -2, y1 - 4, 0.0, b, 0.8, hem) + wave_band(58, 18, -2, y1 - 2, 2.1, b, 0.8, hem)
        g += wave_band(40, 22, -2, y1, 1.0, a, 0.9, hem)
        for x in (24, 40, 56): g += f'<path d="M{x},-2 V{y1-8}" stroke="{s}" stroke-width="2.4" opacity="0.55" stroke-linecap="round"/>'
        return g
    body = bands(66) + tile3(sparkle(30, 18, 2.6, "#FFFFFF", "#7FA8D8", 0.9) + sparkle(52, 46, 2.2, "#FFFFFF", "#7FA8D8", 0.9))
    cap = bands(54, 10) + face(40, 34, 0.42, "closed") + sparkle(26, 66, 3, "#FFFFFF", "#7FA8D8") + sparkle(56, 70, 2.4, "#FFFFFF", "#7FA8D8") + sparkle(42, 74, 2, "#FFFFFF", "#7FA8D8", 0.8)
    return body, cap, hb([[14, 0, 52, 64]]), hb([[14, 0, 52, 52], [20, 52, 40, 8]])

def rock_face(c, y0, y1, ice=False):
    g = R(10, y0, 60, y1 - y0, c["rock"], 0)
    if ice: g += "".join(f'<path d="M{x},{y0} V{y1}" stroke="#FFFFFF" stroke-width="{w}" opacity="0.55"/>' for x, w in ((18, 4), (34, 2), (50, 5), (62, 2)))
    else: g += f'<rect x="58" y="{y0}" width="12" height="{y1-y0}" fill="{c["rock2"]}" opacity="0.8"/><rect x="13" y="{y0}" width="4" height="{y1-y0}" fill="#FFFFFF" opacity="0.3"/>'
    return g
def ledge(c, item):
    """overhanging rock/ice ledge: body = cliff face going up off-screen, cap = the overhang with things under it"""
    ice = c.get("ice", False)
    tex = (f'<path d="M24,6 l6,8 -4,10 M46,30 l-5,9 6,9 M30,48 l4,6" stroke="{c["rock2"]}" stroke-width="2" fill="none" stroke-linecap="round"/>'
           + E(52, 14, 4, 2.4, c["rock2"], 0, 'opacity="0.7"') + E(24, 38, 3.5, 2, c["rock2"], 0, 'opacity="0.7"'))
    body = rock_face(c, -1, 65, ice) + tile3(tex) + f'<path d="M10,-1 V65 M70,-1 V65" stroke="{L}" stroke-width="2.2"/>'
    cap = rock_face(c, -1, 30, ice) + tex.replace('M30,48 l4,6', '')
    lip = "M10,-1 V26 L4,34 Q3,42 8,46 Q40,50 72,46 Q77,42 76,34 L70,26 V-1"
    cap += P(lip, c["rock"], 2.2) + f'<path d="M8,44 Q40,48 72,44" stroke="{c["rock2"]}" stroke-width="4" fill="none" opacity="0.8"/>'
    cap += hl(10, 36, 30, 37, 2, 0.6) + face(40, 37, 0.36, "closed")
    hc = [[10, 0, 60, 30], [4, 30, 72, 16]]
    if item == "icicles":
        cap += icicles(8, 72, 46, [12, 20, 10, 26, 14, 18], c.get("ice_col", "#CFEAFF")); hc += [[14, 46, 52, 8], [24, 54, 32, 8]]
    elif item == "vines":
        for x, l in ((14, 22), (24, 30), (56, 26), (66, 18)):
            cap += f'<path d="M{x},45 Q{x+3},{45+l/2} {x},{45+l}" stroke="#4F8A5A" stroke-width="2.4" fill="none" stroke-linecap="round"/>'
            for k in range(1, 4): cap += E(x + (2 if k % 2 else -2), 45 + l * k / 4, 3, 1.8, "#7FCB8A", 1)
        cap += (P("M32,46 L36,60 L40,48 L44,60 L48,46 Z", "#7FCB8A", 1.6) + C(40, 62, 6, "#FF8FB1", 1.6) + C(40, 62, 2.4, GOLD, 0)
                + sparkle(30, 66, 2.4) + sparkle(52, 70, 2))
        hc += [[16, 46, 48, 10], [34, 56, 12, 12]]
    elif item == "lamp":
        cap += K.svg(0, 0, "")[0:0] + f'<path d="M40,46 V56" stroke="{c["metal"]}" stroke-width="3"/>' + C(40, 46, 2, c["metal"], 1)
        cap += (f'<circle cx="40" cy="64" r="16" fill="url(#glow)"/>' + P("M26,58 Q40,54 54,58 Q52,72 40,72 Q28,72 26,58 Z", GOLD, 2) + E(40, 58, 14, 3.4, GOLD2, 1.6)
                + P("M40,52 Q36,46 40,40 Q44,46 40,52 Z", "#FFB36B", 1.2) + hl(31, 61, 34, 68, 1.6, 0.8) + face(40, 64, 0.3))
        hc += [[38, 46, 4, 8], [26, 54, 28, 18]]
    return body, cap, hb([[10, 0, 60, 64]]), hb(hc)

def bough(c, item):
    """a big tree's drooping bough coming down from above; cap = the fork the thing hangs from"""
    def tufts(y0, y1):
        g = ""
        for y in range(y0, y1, 16):
            sx = 1 if (y // 16) % 2 == 0 else -1; x0 = 40 + sx * 6
            if c["kind"] == "gum":
                g += E(40 + sx * 16, y + 8, 10, 4, c["leaf"], 1.6, f'transform="rotate({sx*25} {40+sx*16} {y+8})"')
            else:
                g += P(f"M{x0},{y+2} Q{40+sx*22},{y+4} {40+sx*24},{y+12} Q{40+sx*14},{y+10} {x0},{y+12} Z", c["leaf"], 1.6)
                if c.get("snow"): g += P(f"M{x0+sx*4},{y+3} Q{40+sx*18},{y+2} {40+sx*23},{y+8} Q{40+sx*14},{y+6} {x0+sx*4},{y+6} Z", "#FFFFFF", 1)
        return g
    trunk = lambda y0, y1: (R(31, y0, 18, y1 - y0, c["bark"], 0) + f'<rect x="44" y="{y0}" width="5" height="{y1-y0}" fill="{c["bark2"]}"/>'
                            + f'<path d="M31,{y0} V{y1} M49,{y0} V{y1}" stroke="{L}" stroke-width="2"/>')
    body = trunk(-1, 65) + tile3(tufts(0, 64)) + tile3(f'<path d="M36,20 q3,6 0,12" stroke="{c["bark2"]}" stroke-width="1.6" fill="none"/>')
    fork = "M31,-1 V8 Q31,12 26,12 H10 Q4,12 4,17 Q4,22 10,22 H70 Q76,22 76,17 Q76,12 70,12 H54 Q49,12 49,8 V-1"
    cap = trunk(-1, 10) + tufts(0, 8) + P(fork, c["bark"], 2.2) + f'<path d="M10,20 H70" stroke="{c["bark2"]}" stroke-width="2.4" opacity="0.8"/>'
    for x in (12, 64):
        cap += (E(x, 10, 8, 4, c["leaf"], 1.6) if c["kind"] == "gum" else P(f"M{x-8},12 Q{x},2 {x+8},12 Z", c["leaf"], 1.6))
    if c.get("snow"): cap += snowcap(6, 30, 12, 5) + snowcap(50, 74, 12, 5)
    hc = [[31, 0, 18, 12], [4, 12, 72, 10]]
    if item == "lantern":   # elf lantern on a short cord
        cap += (f'<path d="M40,22 V30" stroke="{L}" stroke-width="2"/><circle cx="40" cy="46" r="20" fill="url(#glow)"/>'
                + R(30, 28, 20, 5, MINT2, 1.6, 2) + R(28, 33, 24, 26, "#FFE9A8", 2, 6) + R(28, 33, 24, 26, "none", 0)
                + f'<path d="M34,33 V59 M46,33 V59" stroke="{RED2}" stroke-width="2.4"/>' + R(30, 57, 20, 5, MINT2, 1.6, 2)
                + P("M36,62 L40,68 L44,62 Z", RED2, 1.4) + face(40, 45, 0.32))
        hc += [[38, 22, 4, 8], [28, 28, 24, 34]]
    elif item == "icicles":  # icicles under the heavy snowy fork (Lapland spruce)
        cap += icicles(8, 72, 21, [12, 20, 10, 24, 14, 22, 12, 18], "#CFEAFF") + face(40, 17, 0.26, "closed")
        hc += [[10, 22, 60, 8], [20, 30, 40, 8]]
    elif item == "furin":  # glass wind bell with a paper strip
        cap += (f'<path d="M40,22 V28" stroke="{L}" stroke-width="1.8"/>' + P("M30,46 Q30,28 40,28 Q50,28 50,46 Z", "#DDF4FF", 2, 'opacity="0.95"')
                + f'<path d="M32,40 Q40,36 48,40" stroke="{RED2}" stroke-width="2" fill="none"/>' + face(40, 37, 0.24, "closed")
                + f'<path d="M40,46 V52" stroke="{L}" stroke-width="1.4"/>' + P("M35,52 H45 L44,70 Q40,72 36,70 Z", "#FFF4D6", 1.6)
                + f'<path d="M37,58 H43 M37,63 H43" stroke="{RED2}" stroke-width="1.4"/>')
        hc += [[38, 22, 4, 6], [30, 28, 20, 18], [36, 46, 8, 16]]
    elif item == "koala":  # koala hugging the branch, in a Santa hat
        g = "#B9B3C9"
        cap += (E(40, 40, 15, 17, g, 2) + E(40, 45, 9, 11, "#E6E2EE", 0) + C(25, 22, 7, g, 2) + C(55, 22, 7, g, 2) + C(25, 22, 3.5, "#FFC4D4", 0) + C(55, 22, 3.5, "#FFC4D4", 0)
                + C(40, 28, 12, g, 2) + face(40, 28, 0.32) + E(40, 31, 3, 2.2, "#4A3358", 0)
                + E(29, 18, 4, 6, g, 1.8, 'transform="rotate(-20 29 18)"') + E(51, 18, 4, 6, g, 1.8, 'transform="rotate(20 51 18)"')
                + P("M30,18 Q36,4 48,10 L50,18 Z", "url(#red)", 1.4) + R(29, 15, 22, 4, FUR, 1, 2) + C(50, 8, 2.4, FUR, 1)
                + E(30, 56, 5, 3.4, g, 1.6) + E(50, 56, 5, 3.4, g, 1.6))
        hc += [[26, 22, 28, 34]]
    return body, cap, hb([[28, 0, 24, 64]]), hb(hc)

def girder(c, item):
    """bridge / gantry steel: body = lattice hanger going up to the deck/arch, cap = the cross girder with things under it"""
    s1, s2 = c["steel"], c["steel2"]
    lat = (R(26, -1, 6, 66, s1, 0) + R(48, -1, 6, 66, s1, 0)
           + f'<path d="M32,0 L48,32 L32,64 M48,0 L32,32 L48,64" stroke="{s2}" stroke-width="4" fill="none"/>'
           + f'<path d="M26,-1 V65 M32,-1 V65 M48,-1 V65 M54,-1 V65" stroke="{L}" stroke-width="1.6"/>'
           + "".join(C(29, y, 1.4, "#FFFFFF", 0, 'opacity="0.7"') + C(51, y, 1.4, "#FFFFFF", 0, 'opacity="0.7"') for y in (8, 24, 40, 56)))
    body = lat
    cap = (lat.replace('height="66"', 'height="17"').replace("V65", "V16").replace("M32,0 L48,32 L32,64 M48,0 L32,32 L48,64", "M32,0 L40,16 M48,0 L40,16")
           + R(4, 14, 72, 16, s1, 2.2, 2) + R(4, 14, 72, 4, s2, 0) + R(4, 26, 72, 4, s2, 0) + R(4, 14, 72, 16, "none", 2.2, 2)
           + "".join(C(x, 22, 1.6, "#FFFFFF", 0, 'opacity="0.75"') for x in (10, 18, 62, 70)))
    hc = [[26, 0, 28, 16], [4, 14, 72, 16]]
    if c.get("snow"): cap += snowcap(4, 26, 14, 5) + snowcap(54, 76, 14, 5)
    cap += face(40, 22, 0.3, "closed")
    if item == "icicles":
        cap += icicles(6, 74, 30, [12, 20, 10, 24, 14, 18, 10]); hc += [[10, 30, 60, 8], [20, 38, 40, 8]]
    elif item == "sign":   # neon panel hung on two short chains (Tokyo gantry)
        cap += (f'<path d="M22,30 V40 M58,30 V40" stroke="{L}" stroke-width="2.6"/>' + R(10, 38, 60, 30, "#3A2E5E", 2.2, 6)
                + f'<path d="M24,52 C24,44 34,44 34,50 C34,44 44,44 44,52 C44,58 34,62 34,64 C34,62 24,58 24,52 Z" fill="none" stroke="#FF8FC8" stroke-width="5" opacity="0.4"/>'
                + f'<path d="M24,52 C24,44 34,44 34,50 C34,44 44,44 44,52 C44,58 34,62 34,64 C34,62 24,58 24,52 Z" fill="none" stroke="#FFE3F2" stroke-width="2"/>'
                + f'<path d="M50,58 V46 L54,50 L58,46 V58 Q54,62 50,58 Z" fill="none" stroke="#9EF0E0" stroke-width="5" opacity="0.4"/>'
                + f'<path d="M50,58 V46 L54,50 L58,46 V58 Q54,62 50,58 Z" fill="none" stroke="#E8FFF9" stroke-width="2"/>')
        hc += [[20, 30, 4, 8], [56, 30, 4, 8], [10, 38, 60, 30]]
    elif item == "star":   # festive star hung under the Harbour Bridge deck
        cap += (f'<path d="M40,30 V42" stroke="{L}" stroke-width="2.6"/><circle cx="40" cy="56" r="20" fill="url(#glow)"/>' + star5(40, 56, 17, "url(#gold)", "#B07A3A", 2)
                + face(40, 57, 0.28) + sparkle(18, 46, 3) + sparkle(64, 64, 2.6))
        hc += [[38, 30, 4, 12], [28, 42, 24, 26]]
    return body, cap, hb([[26, 0, 28, 64]]), hb(hc)

def cloud(c, item):
    """low snow / summer cloud: a genuine sky object"""
    col, sh = c["col"], c["shade"]
    bumps = lambda ys: "".join(C(x, y, 16, col, 2.2) for x in (20, 60) for y in ys)
    body = (bumps((-32, 0, 32, 64, 96)) + R(20, -1, 40, 66, col, 0) + R(52, -1, 14, 66, sh, 0, 0, 'opacity="0.55"')
            + tile3(E(30, 30, 8, 4, "#FFFFFF", 0, 'opacity="0.7"')))
    lobes = [(24, 40, 14), (56, 40, 14), (40, 46, 16)]
    cap = (bumps((-32, 0, 22)) + "".join(C(x, y, r, col, 2.2) for x, y, r in lobes) + R(20, -1, 40, 36, col, 0) + R(16, 20, 48, 26, col, 0)
           + C(56, 40, 12, sh, 0, 'opacity="0.5"')
           + E(30, 38, 6, 3, "#FFFFFF", 0, 'opacity="0.8"') + face(40, 40, 0.4, "closed" if item != "sun" else "open"))
    if item == "snow":
        cap += flake(18, 66, 4.5, "#FFFFFF", "#9EB8EE", 10) + flake(62, 70, 4, "#FFFFFF", "#9EB8EE", 30) + flake(40, 75, 3.4, "#FFFFFF", "#9EB8EE")
    elif item == "blizzard":
        cap += "".join(f'<path d="M{x},{y} q8,-4 14,0 t14,0" stroke="#FFFFFF" stroke-width="2.4" fill="none" stroke-linecap="round" opacity="0.85"/>' for x, y in ((8, 66), (34, 72), (48, 64)))
        cap += flake(20, 74, 3.4, "#FFFFFF", "#9EB8EE")
    elif item == "sun":
        cap = (C(66, 10, 12, "#FFE08A", 2) + "".join(f'<path d="M{66+math.cos(math.radians(a))*15:.1f},{10+math.sin(math.radians(a))*15:.1f} L{66+math.cos(math.radians(a))*20:.1f},{10+math.sin(math.radians(a))*20:.1f}" stroke="#F6B54A" stroke-width="2.4" stroke-linecap="round"/>' for a in range(-30, 150, 30))
               + cap)
    return body, cap, hb([[12, 0, 56, 64]]), hb([[12, 0, 56, 40]], lobes)

def wires(c, bitem, citem):
    """decorations strung on cross-street wires between buildings: each tile is one wire (anchor drawn, ends fade
    into the buildings off-column) with a drop cord tying it to the wire below; the cap is the lowest wire"""
    gid = "wf"
    grad = (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="80" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{c["wire"]}" stop-opacity="0"/>'
            f'<stop offset="0.25" stop-color="{c["wire"]}"/><stop offset="0.75" stop-color="{c["wire"]}"/><stop offset="1" stop-color="{c["wire"]}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="wl" x1="0" y1="0" x2="80" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#E6DDF7" stop-opacity="0"/>'
            f'<stop offset="0.25" stop-color="#E6DDF7"/><stop offset="0.75" stop-color="#E6DDF7"/><stop offset="1" stop-color="#E6DDF7" stop-opacity="0"/></linearGradient></defs>')
    wire = lambda y: (f'<path d="M0,{y-4} Q40,{y+6} 80,{y-4}" stroke="url(#{gid})" stroke-width="4" fill="none"/>'
                      f'<path d="M0,{y-4} Q40,{y+6} 80,{y-4}" stroke="url(#wl)" stroke-width="1.6" fill="none"/>')
    def small(kind, y):
        if kind == "bulbs":
            g = f'<path d="M40,{y} V{y+56}" stroke="{c["wire"]}" stroke-width="2"/>'
            for k, (dx, col) in enumerate(((-6, "#FF8FB1"), (6, "#FFE08A"), (-6, "#9EF0E0"), (6, "#FF8FB1"))):
                yy = y + 10 + k * 13; g += f'<path d="M40,{yy} L{40+dx},{yy}" stroke="{c["wire"]}" stroke-width="1.6"/>' + E(40 + dx * 1.6, yy + 3, 4, 5.5, col, 1.6) + C(40 + dx * 1.6 - 1.2, yy + 1.5, 1.2, "#FFF", 0)
            for x, col in ((12, "#9EF0E0"), (24, "#FFE08A"), (56, "#FF8FB1"), (68, "#FFE08A")):
                g += E(x, y + 3 - abs(40 - x) * 0.12, 2.4, 3.4, col, 1.2)
            return g
        if kind == "flake":
            return f'<path d="M40,{y} V{y+56}" stroke="{c["wire"]}" stroke-width="2"/>' + flake(40, y + 26, 11, "#FFFFFF", "#7FA8D8", 0, 2.6) + C(40, y + 26, 3, GOLD, 1.2) + sparkle(40, y + 48, 3, "#FFFFFF", "#7FA8D8")
        if kind == "flags":
            g = f'<path d="M40,{y} V{y+56}" stroke="{c["wire"]}" stroke-width="2"/>'
            for k, x in enumerate((6, 18, 30, 50, 62, 74)):
                yy = y - 2 + 6 - abs(40 - x) * 0.12; col = c["flags"][k % len(c["flags"])]
                g += P(f"M{x-5},{yy:.1f} L{x+5},{yy:.1f} L{x},{yy+10:.1f} Z", col, 1.2, 'opacity="0.95"')
            for k in range(3):
                yy = y + 12 + k * 15; col = c["flags"][(k + 2) % len(c["flags"])]; sx = -1 if k % 2 else 1
                g += P(f"M40,{yy} L40,{yy+12} L{40+sx*12},{yy+6} Z", col, 1.4)
            return g
        if kind == "fanous":
            return (f'<path d="M40,{y} V{y+56}" stroke="{c["wire"]}" stroke-width="2"/><circle cx="40" cy="{y+28}" r="14" fill="url(#glow)"/>'
                    + P(f"M34,{y+14} L46,{y+14} L50,{y+22} L46,{y+40} L34,{y+40} L30,{y+22} Z", "#FFE9A8", 1.6) + P(f"M34,{y+14} L40,{y+8} L46,{y+14} Z", GOLD2, 1.4)
                    + f'<path d="M30,{y+22} H50 M40,{y+14} V{y+40}" stroke="#C99A4B" stroke-width="1.4"/>' + P(f"M36,{y+40} L40,{y+46} L44,{y+40} Z", GOLD2, 1.2))
        if kind == "chochin":
            return (f'<path d="M40,{y} V{y+56}" stroke="{c["wire"]}" stroke-width="2"/><circle cx="40" cy="{y+28}" r="14" fill="url(#glow)" opacity="0.8"/>'
                    + R(34, y + 10, 12, 4, "#3A2E5E", 1.2, 1) + E(40, y + 28, 11, 14, "#FF6F7F", 1.8) + "".join(f'<path d="M{29+k},{y+20+k*4} Q40,{y+18+k*4+2} {51-k},{y+20+k*4}" stroke="#C23B57" stroke-width="1" fill="none"/>' for k in range(4))
                    + R(34, y + 42, 12, 4, "#3A2E5E", 1.2, 1))
    body = grad + tile3(wire(6)) + small(bitem, 8) + small(bitem, -56)
    body = grad + wire(6) + f'<g transform="translate(0,-64)">{wire(6)}</g>' + small(bitem, 8) + f'<g transform="translate(0,-64)">{small(bitem, 8)}</g>'
    cap = grad + wire(6) + f'<path d="M40,0 V14" stroke="{c["wire"]}" stroke-width="2"/>'
    hc = [[38, 0, 4, 16]]
    if citem == "bauble":
        cap += (f'<circle cx="40" cy="46" r="26" fill="url(#glow)"/>' + R(35, 14, 10, 7, "#E6DDF7", 1.4, 2) + C(40, 44, 20, "url(#red)", 2.2)
                + f'<path d="M21,40 Q40,50 59,40" stroke="{GOLD}" stroke-width="3" fill="none"/>' + E(32, 34, 5, 3, "#FFF", 0, 'opacity="0.85" transform="rotate(-30 32 34)"')
                + face(40, 48, 0.36) + small("bulbs", 8).split("</path>")[0][:0])
        hc += [[35, 14, 10, 12]]; circ = [(40, 44, 20)]
        return grad + wire(6) + f'<g transform="translate(0,-64)">{wire(6)}</g>' + small(bitem, 8) + f'<g transform="translate(0,-64)">{small(bitem, 8)}</g>', cap, hb([[28, 0, 24, 64]]), hb(hc, circ)
    if citem == "traffic":
        cap += (R(29, 14, 22, 52, "#FFD45C", 2.2, 5) + R(26, 14, 28, 4, "#3A2E5E", 1.4, 1)
                + C(40, 26, 6.5, "#FF7F8F", 1.6) + C(40, 40, 6.5, "#FFE08A", 1.6) + C(40, 54, 6.5, "#8FE3A6", 1.6)
                + "".join(P(f"M33,{y-8} Q40,{y-11} 47,{y-8}", "#E2A23E", 1.2) for y in (26, 40, 54))
                + face(40, 40, 0.2) + snowcap(28, 52, 14, 4) + R(29, 64, 22, 3, "#E2A23E", 1, 1))
        hc += [[26, 14, 28, 4], [29, 18, 22, 48]]
    elif citem == "flags":
        cols = c["flags"]
        for k in range(3):
            yy = 16 + k * 16; col = cols[k % len(cols)]
            cap += P(f"M40,{yy} L{40-16},{yy+4} L40,{yy+14} Z", col, 1.6) + P(f"M40,{yy} L{40+16},{yy+4} L40,{yy+14} Z", cols[(k + 1) % len(cols)], 1.6)
        cap += C(40, 66, 7, GOLD, 1.8) + face(40, 66, 0.18) + small("flags", 8).split('<path d="M40,8 V64"')[0]
        for k, x in enumerate((6, 18, 30, 50, 62, 74)):
            yy = 6 - abs(40 - x) * 0.12; cap += P(f"M{x-5},{yy:.1f} L{x+5},{yy:.1f} L{x},{yy+10:.1f} Z", cols[k % len(cols)], 1.2)
        hc += [[24, 16, 32, 46], [33, 58, 14, 14]]
    elif citem == "fanous":
        cap += (f'<circle cx="40" cy="44" r="28" fill="url(#glow)"/>' + P("M40,10 L50,20 H30 Z", GOLD2, 1.6)
                + P("M30,20 H50 L56,32 L50,62 H30 L24,32 Z", "#FFE9A8", 2) + f'<path d="M24,32 H56 M30,20 L34,62 M50,20 L46,62 M40,20 V62" stroke="#C99A4B" stroke-width="1.6" fill="none"/>'
                + star5(40, 45, 5, "#FFF4C9", "#C99A4B", 1) + P("M32,62 H48 L44,68 H36 Z", GOLD2, 1.6) + P("M38,68 L40,74 L42,68 Z", GOLD2, 1.2) + face(40, 35, 0.24))
        hc += [[30, 14, 20, 6], [24, 20, 32, 42], [32, 62, 16, 6]]
    elif citem == "chochin":
        cap += (f'<circle cx="40" cy="42" r="30" fill="url(#glow)" opacity="0.8"/>' + R(30, 14, 20, 6, "#3A2E5E", 1.6, 2) + E(40, 42, 20, 24, "#FF6F7F", 2.2)
                + "".join(f'<path d="M{22+k*0.4},{26+k*6} Q40,{24+k*6+3} {58-k*0.4},{26+k*6}" stroke="#C23B57" stroke-width="1.2" fill="none"/>' for k in range(6))
                + R(30, 64, 20, 6, "#3A2E5E", 1.6, 2) + f'<path d="M36,70 V77 M40,70 V78 M44,70 V77" stroke="#FFD45C" stroke-width="1.6"/>' + face(40, 42, 0.42))
        hc += [[30, 14, 20, 6], [22, 20, 36, 44], [30, 64, 20, 6]]
    return body, cap, hb([[28, 0, 24, 64]]), hb(hc)

def cable(c, item):
    """hangs from a real machine above: crane jib (two cable falls) or the cable-car haul rope (hanger arm)"""
    if item == "hook":
        rope = lambda x: R(x - 2.5, -1, 5, 66, "#C9C2E8", 1.4) + "".join(f'<path d="M{x-2},{y} L{x+2},{y+3}" stroke="#8E86B8" stroke-width="1.2"/>' for y in range(0, 64, 6))
        body = rope(31) + rope(49)
        cap = (rope(31).replace('height="66"', 'height="12"') + rope(49).replace('height="66"', 'height="12"')
               + R(22, 8, 36, 22, "#FFD45C", 2.2, 6) + C(40, 16, 6, "#E2A23E", 1.6) + C(40, 16, 2, L, 0) + f'<path d="M26,26 H54" stroke="#3A2E5E" stroke-width="3" stroke-dasharray="4 3"/>'
               + R(36, 30, 8, 6, "#B9B3D9", 1.6) + P("M40,36 V42 Q40,50 33,50 Q27,50 27,44", "none", 0, f'stroke="{L}" stroke-width="7" stroke-linecap="round"')
               + P("M40,36 V42 Q40,50 33,50 Q27,50 27,44", "none", 0, 'stroke="#D6D2EC" stroke-width="3.6" stroke-linecap="round"')
               + f'<path d="M33,50 L40,56 L48,50" stroke="{RED2}" stroke-width="2.4" fill="none"/>'
               + R(24, 54, 32, 22, "#AEE3C6", 2.2, 3) + R(37, 54, 6, 22, RED2, 0) + R(24, 62, 32, 5, RED2, 0) + R(24, 54, 32, 22, "none", 2.2, 3)
               + P("M40,56 Q32,46 30,54 Z M40,56 Q48,46 50,54 Z", RED2, 1.4) + face(31, 71, 0.18) + snowcap(22, 58, 8, 4))
        return body, cap, hb([[28, 0, 24, 64]]), hb([[28, 0, 24, 10], [22, 8, 36, 22], [34, 30, 12, 16], [24, 46, 32, 30]])
    # cable car (Sugarloaf): hanger arm up to the haul rope
    arm = lambda y1: (R(32, -1, 5, y1 + 1, "#8E86B8", 1.4) + R(43, -1, 5, y1 + 1, "#8E86B8", 1.4))
    body = arm(65) + tile3(R(30, 28, 20, 5, "#B9B3D9", 1.4, 1))
    cap = (arm(20) + R(26, 16, 28, 6, "#B9B3D9", 1.6, 2) + R(14, 22, 52, 48, c["car"], 2.4, 10) + R(18, 28, 44, 22, "#CFEAFF", 1.8, 6)
           + f'<path d="M40,28 V50" stroke="{L}" stroke-width="1.6"/>' + hl(21, 32, 26, 44, 2, 0.8) + face(40, 60, 0.3) + R(14, 64, 52, 6, c["car2"], 0, 0)
           + R(14, 22, 52, 48, "none", 2.4, 10) + snowcap(16, 64, 22, 4) .replace("#FFFFFF", "#FFFFFF") + sparkle(70, 40, 2.6))
    return body, cap, hb([[28, 0, 24, 64]]), hb([[28, 0, 24, 18], [14, 18, 52, 52]])

def balloon(c):
    """hot-air balloon: body = the lower envelope (it's huge, it fills the sky above), cap = mouth + burner + basket"""
    cols = c["stripes"]
    gores = lambda clip: "".join(f'<rect x="{10 + i*10}" y="-1" width="10" height="82" fill="{cols[i % len(cols)]}"/>' for i in range(6))
    body = (f'<clipPath id="eb"><rect x="10" y="-1" width="60" height="66"/></clipPath><g clip-path="url(#eb)">{gores(0)}</g>'
            + "".join(f'<path d="M{10+i*10},-1 V65" stroke="{L}" stroke-width="1" opacity="0.5"/>' for i in range(1, 6))
            + f'<path d="M10,-1 V65 M70,-1 V65" stroke="{L}" stroke-width="2.2"/>' + f'<rect x="58" y="-1" width="12" height="66" fill="#3A2E5E" opacity="0.18"/>' + tile3(sparkle(22, 30, 2.4, "#FFFFFF", "#D9953A", 0.8)))
    env = "M10,-1 V8 Q12,22 28,34 H52 Q68,22 70,8 V-1 Z"
    cap = (f'<clipPath id="ec"><path d="{env}"/></clipPath><g clip-path="url(#ec)">{gores(0)}</g>' + P(env, "none", 2.2) + face(40, 14, 0.34, "closed")
           + R(26, 32, 28, 5, "#8E86B8", 1.6, 2) + P("M36,37 Q40,29 44,37", "#FFB36B", 1.2)
           + f'<path d="M28,37 L24,52 M36,37 L33,52 M44,37 L47,52 M52,37 L56,52" stroke="{L}" stroke-width="1.6"/>'
           + R(22, 50, 36, 24, "#E3B98A", 2.2, 4) + "".join(f'<path d="M22,{y} H58" stroke="#C99A6B" stroke-width="1.4"/>' for y in (56, 62, 68))
           + "".join(f'<path d="M{x},50 V74" stroke="#C99A6B" stroke-width="1.2"/>' for x in (30, 40, 50)) + R(20, 48, 40, 5, "#C99A6B", 1.8, 2)
           + E(20, 62, 4, 6, "#C9B6A0", 1.4) + E(60, 62, 4, 6, "#C9B6A0", 1.4) + K.pompom(40, 47, 0)[:0])
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 0, 60, 12], [16, 12, 48, 10], [24, 22, 32, 12], [26, 32, 28, 18], [20, 48, 40, 26]])

# ======================================================================= BOTTOM DRAWERS
def bricks(x0, x1, y0, y1, col, mort, rowh=16):
    g = R(x0, y0, x1 - x0, y1 - y0, col, 0)
    r = 0; y = y0 - (y0 % rowh)
    while y < y1:
        g += f'<path d="M{x0},{max(y,y0)} H{x1}" stroke="{mort}" stroke-width="1.6"/>'
        for o in ((x1 - x0) * 0.25, (x1 - x0) * 0.75) if r % 2 else ((x1 - x0) * 0.5,):
            g += f'<path d="M{x0+o:.0f},{max(y,y0)} V{min(y+rowh,y1)}" stroke="{mort}" stroke-width="1.6"/>'
        y += rowh; r += 1
    return g
def sides(x0, x1, y0=-1, y1=65, sw=2.2): return f'<path d="M{x0},{y0} V{y1} M{x1},{y0} V{y1}" stroke="{L}" stroke-width="{sw}"/>'

def pine_tier(xb0, xb1, xt0, xt1, yt, yb, col, snow=True, lights=False):
    g = P(f"M{xt0},{yt} L{xt1},{yt} L{xb1},{yb} Q{(xb0+xb1)/2},{yb+4} {xb0},{yb} Z", col, 2)
    if snow: g += P(f"M{xb0+2},{yb-1} Q{(xb0+xb1)/2},{yb+5} {xb1-2},{yb-1} Q{(xb0+xb1)/2},{yb-4} {xb0+2},{yb-1} Z", "#FFFFFF", 1.2)
    if lights:
        g += f'<path d="M{xb0+6},{yb-6} Q{(xb0+xb1)/2},{yb} {xb1-6},{yb-8}" stroke="{GOLD2}" stroke-width="1.4" fill="none"/>'
        for k, col2 in enumerate(("#FF8FB1", "#FFE08A", "#9EF0E0", "#FF8FB1")):
            t = (k + 0.5) / 4; g += C(xb0 + 6 + (xb1 - xb0 - 12) * t, yb - 6 + 4 * math.sin(math.pi * t) - 2 * t, 2.6, col2, 1)
    return g
def pine(c, lights=False):
    col = c["leaf"]
    tier = lambda y: pine_tier(8, 72, 22, 58, y, y + 32, col, True, lights)
    body = R(36, -1, 8, 66, "#C99A6B", 0) + tier(-32) + tier(0) + tier(32)
    cap = (R(36, 60, 8, 21, "#C99A6B", 0) + pine_tier(8, 72, 22, 58, 56, 81, col, False, lights) + pine_tier(12, 68, 26, 54, 38, 62, col, True, lights)
           + pine_tier(18, 62, 36, 44, 18, 44, col, True, lights) + face(40, 34, 0.3))
    cap += (f'<circle cx="40" cy="12" r="14" fill="url(#glow)"/>' + star5(40, 12, 10 if lights else 7, "url(#gold)", "#B07A3A", 1.8)) 
    return body, cap, hb([[12, 0, 56, 64]]), hb([[12, 60, 56, 20], [18, 40, 44, 20], [26, 26, 28, 14], [34, 16, 12, 10]]), [40, 16]

def workshop():
    stone = "#C9C2E8"; st2 = "#A9A3C9"
    cob = lambda y0: "".join(E(x + (8 if r % 2 else 0), y0 + r * 16 + 8, 9, 6.5, stone, 1.6) for r in range(4) for x in (18, 36, 54) if x + (8 if r % 2 else 0) < 66)
    base = R(12, -1, 56, 66, st2, 0)
    body = base + f'<clipPath id="cb"><rect x="12" y="-1" width="56" height="66"/></clipPath><g clip-path="url(#cb)">{cob(0)}</g>' + sides(12, 68)
    cap = (R(12, 30, 56, 51, st2, 0) + f'<clipPath id="cc"><rect x="12" y="30" width="56" height="51"/></clipPath><g clip-path="url(#cc)">{cob(32)}</g>' + sides(12, 68, 30, 81)
           + R(8, 20, 64, 12, "#FFFFFF", 2.2, 3) + "".join(R(8 + k * 16, 20, 8, 12, RED2, 0) for k in range(4)) + R(8, 20, 64, 12, "none", 2.2, 3)
           + snowcap(10, 70, 20, 5) + C(40, 52, 9, "none", 0, f'stroke="#7FCBA6" stroke-width="5"') + C(40, 44, 2.4, RED2, 0) + C(36, 46, 2, RED2, 0)
           + face(40, 66, 0.28) + C(30, 10, 5, "#F3EEFC", 1.2, 'opacity="0.85"') + C(24, 2, 3.6, "#F3EEFC", 1, 'opacity="0.6"'))
    return body, cap, hb([[12, 0, 56, 64]]), hb([[12, 30, 56, 50], [8, 20, 64, 12]]), [40, 20]

def gifts():
    box = lambda y, col, rib, x0=10, x1=70: (R(x0, y, x1 - x0, 32, col, 2) + R((x0 + x1) / 2 - 4, y, 8, 32, rib, 0) + R(x0, y + 12, x1 - x0, 7, rib, 0)
                                            + R(x0, y, x1 - x0, 32, "none", 2) + hl(x0 + 4, y + 4, x0 + 4, y + 10, 1.8, 0.7))
    body = box(0, "#AEE3C6", RED2) + box(32, "#FFC4D4", GOLD)
    cap = (box(48, "#AEE3C6", RED2) + box(16, "#FFE08A", "#7FA8D8", 18, 62).replace('height="32"', 'height="32"')
           + P("M40,16 Q26,2 26,10 Q26,16 40,16 Z M40,16 Q54,2 54,10 Q54,16 40,16 Z", "#7FA8D8", 1.8) + C(40, 16, 3, "#7FA8D8", 1.4) + face(28, 35, 0.22))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 48, 60, 32], [18, 16, 44, 32], [28, 6, 24, 10]]), [40, 8]

def chimney():
    body = bricks(12, 68, -1, 65, "#E7A08F", "#C47F76") + sides(12, 68)
    cap = (bricks(12, 68, 28, 81, "#E7A08F", "#C47F76") + sides(12, 68, 28, 81) + R(8, 22, 64, 8, "#D88A80", 2.2, 2)
           + R(18, 8, 14, 16, "#C9798F", 2, 3) + R(46, 4, 16, 20, "#C9798F", 2, 3) + snowcap(16, 34, 8, 4) + snowcap(44, 64, 4, 4) + snowcap(8, 72, 22, 4)
           + face(40, 50, 0.32) + C(54, -0, 0, "none", 0))
    return body, cap, hb([[12, 0, 56, 64]]), hb([[12, 28, 56, 52], [8, 22, 64, 8], [18, 8, 14, 14], [46, 4, 16, 18]]), [25, 6]

def phonebox():
    panes = lambda y0: "".join(R(20 + i * 14, y0 + 4 + j * 14, 12, 12, "#FFF4C9", 1.4, 1) for i in range(3) for j in range(4) if y0 + 4 + j * 14 < 64 + y0)
    body = R(14, -1, 52, 66, "url(#red)", 0) + f'<clipPath id="pb"><rect x="14" y="-1" width="52" height="66"/></clipPath><g clip-path="url(#pb)">' + "".join(R(20 + i * 14, 2 + j * 16, 12, 12, "#FFF4C9", 1.4, 1) for i in range(3) for j in range(4)) + "</g>" + sides(14, 66)
    cap = (R(14, 30, 52, 51, "url(#red)", 0) + "".join(R(20 + i * 14, 34 + j * 16, 12, 12, "#FFF4C9", 1.4, 1) for i in range(3) for j in range(3)) + sides(14, 66, 30, 81)
           + R(12, 20, 56, 10, "url(#red)", 2) + R(22, 22, 36, 6, "#FFFFFF", 1.2, 1) + P("M18,20 Q18,8 40,8 Q62,8 62,20 Z", "url(#red)", 2.2) + R(35, 3, 10, 6, "url(#red)", 1.6, 2)
           + snowcap(18, 62, 12, 4) + face(40, 42, 0.26))
    return body, cap, hb([[14, 0, 52, 64]]), hb([[14, 30, 52, 50], [12, 20, 56, 10], [18, 10, 44, 10], [35, 4, 10, 6]]), [40, 6]

def bus_stack():
    rows = lambda y: R(10, y, 60, 32, "url(#red)", 0) + "".join(R(14 + i * 14, y + 6, 11, 14, "#FFE08A", 1.4, 3) for i in range(4)) + R(10, y + 25, 60, 3, GOLD, 0)
    body = rows(0) + rows(32) + sides(10, 70)
    cap = (rows(48) + sides(10, 70, 48, 81) + P("M10,48 V26 Q10,12 26,12 H54 Q70,12 70,26 V48 Z", "url(#red)", 2.2)
           + R(15, 22, 22, 18, "#BFE6FF", 1.8, 4) + R(43, 22, 22, 18, "#BFE6FF", 1.8, 4) + R(28, 14, 24, 6, "#3A2E5E", 1.2, 2) + R(31, 16, 18, 2, "#FFE08A", 0)
           + "".join(C(x, 31, 2.2, EYE, 0) + C(x - 0.8, 30.2, 0.8, "#FFF", 0) for x in (26, 54)) + f'<path d="M37,44 Q40,47 43,44" stroke="{L}" stroke-width="1.4" fill="none"/>'
           + snowcap(14, 66, 13, 4) + hl(18, 25, 22, 34, 1.6, 0.8))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 26, 60, 54], [14, 12, 52, 14]]), [40, 12]

def skyscraper():
    win = lambda x0, x1, y0, y1: "".join(R(x, y, 6, 8, "#FFE08A" if (x * 7 + y * 3) % 5 else "#8E86B8", 0, 1) for x in range(x0 + 4, x1 - 6, 10) for y in range(y0 + 4, y1 - 6, 16))
    body = R(12, -1, 56, 66, "#9E95C9", 0) + win(12, 68, 0, 64) + R(56, -1, 12, 66, "#3A2E5E", 0, 0, 'opacity="0.18"') + sides(12, 68)
    cap = (R(12, 50, 56, 31, "#9E95C9", 2) + win(12, 68, 50, 82) + R(20, 34, 40, 18, "#ADA5D6", 2) + win(20, 60, 34, 52)
           + R(28, 20, 24, 16, "#BDB6E0", 2) + R(37, 4, 6, 18, "#C9C2E8", 1.6) + C(40, 4, 3, "#FF8FB1", 1.2) + f'<circle cx="40" cy="4" r="6" fill="#FF8FB1" opacity="0.35"/>'
           + snowcap(12, 68, 50, 3) + snowcap(20, 60, 34, 3) + snowcap(28, 52, 20, 3) + face(40, 28, 0.22))
    return body, cap, hb([[12, 0, 56, 64]]), hb([[12, 50, 56, 30], [20, 34, 40, 16], [28, 20, 24, 14], [37, 4, 6, 16]]), [40, 20]

def snowbank_tex(y0, y1):
    return (R(10, y0, 60, y1 - y0, "#F4F8FF", 0) + "".join(P(f"M10,{y} Q40,{y+8} 70,{y}", "none", 0, 'stroke="#D6E6F8" stroke-width="2"') for y in range(y0 + 10, y1, 16))
            + R(56, y0, 14, y1 - y0, "#DDE9F8", 0, 0, 'opacity="0.7"'))
def taxi():
    body = snowbank_tex(-1, 65) + tile3(sparkle(24, 20, 2.4, "#FFFFFF", "#7FA8D8") + sparkle(50, 50, 2, "#FFFFFF", "#7FA8D8")) + sides(10, 70)
    cap = (snowbank_tex(56, 81) + P("M10,81 V58 Q40,48 70,58 V81", "none", 2.2) + R(10, 30, 60, 26, "#FFD45C", 2.2, 8) + P("M16,32 L22,18 H58 L64,32 Z", "#FFD45C", 2.2)
           + P("M21,31 L25,21 H55 L59,31 Z", "#BFE6FF", 1.6) + R(30, 12, 20, 7, "#FFF4C9", 1.6, 2) + C(18, 42, 4, "#FFF4C9", 1.4) + C(62, 42, 4, "#FFF4C9", 1.4)
           + R(28, 44, 24, 6, "#3A2E5E", 1.2, 2) + "".join(R(12 + k * 8, 36, 4, 4, "#3A2E5E", 0) for k in range(0)) + face(40, 26, 0.18) + R(10, 34, 60, 3, "#3A2E5E", 0, 0, 'opacity="0.0"')
           + snowcap(26, 54, 18, 3) + P("M10,56 Q40,62 70,56 V60 Q40,66 10,60 Z", "#FFFFFF", 1.6))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 54, 60, 26], [10, 30, 60, 26], [16, 20, 48, 10], [30, 12, 20, 8]]), [40, 12]

def granite(y0, y1):
    return (R(10, y0, 60, y1 - y0, "#C9AFC0", 0) + R(56, y0, 14, y1 - y0, "#A98FA6", 0, 0, 'opacity="0.8"')
            + "".join(f'<path d="M{x},{y0} V{y1}" stroke="#B49AB0" stroke-width="2"/>' for x in (24, 40)))
def sugarloaf():
    moss = tile3(E(20, 14, 7, 5, "#7FCB8A", 1.4) + E(58, 44, 8, 5, "#7FCB8A", 1.4))
    body = granite(-1, 65) + moss + sides(10, 70)
    dome = "M10,81 V48 Q12,8 40,8 Q68,8 70,48 V81 Z"
    cap = (f'<clipPath id="sd"><path d="{dome}"/></clipPath><g clip-path="url(#sd)">{granite(0, 81)}</g>' + P(dome, "none", 2.2)
           + E(18, 46, 8, 5, "#7FCB8A", 1.4) + E(60, 60, 8, 5, "#7FCB8A", 1.4) + E(32, 12, 7, 4, "#7FCB8A", 1.4) + E(48, 11, 6, 3.6, "#7FCB8A", 1.4)
           + hl(22, 24, 30, 16, 2, 0.6) + face(40, 36, 0.4))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 46, 60, 34], [14, 26, 52, 20], [22, 14, 36, 12], [30, 9, 20, 6]]), [40, 9]

def palm():
    seg = lambda y0, y1: R(31, y0, 18, y1 - y0, "#C99A6B", 0) + "".join(P(f"M31,{y} Q40,{y+4} 49,{y}", "none", 0, f'stroke="#8E6A4E" stroke-width="1.6"') for y in range(y0 - (y0 % 8), y1, 8))
    lights = lambda y0: "".join(C(40 + (7 if k % 2 else -7), y0 + k * 8 + 4, 2.2, ("#FF8FB1", "#FFE08A", "#9EF0E0")[k % 3], 1) for k in range(8))
    body = seg(-1, 65) + lights(0) + sides(31, 49)
    cap = seg(36, 81) + lights(40) + sides(31, 49, 36, 81)
    for a, l in ((-160, 34), (-120, 30), (-60, 30), (-20, 34), (-90, 22)):
        ex, ey = 40 + math.cos(math.radians(a)) * l, 30 + math.sin(math.radians(a)) * l * 0.7 + (abs(math.cos(math.radians(a))) * 12)
        cap += P(f"M40,30 Q{(40+ex)/2},{min(30,ey)-10} {ex:.1f},{ey:.1f} Q{(40+ex)/2},{min(30,ey)-2} 40,34 Z", "#7FCB8A", 1.8)
    cap += C(34, 36, 6, "#A97A52", 1.6) + C(46, 36, 6, "#A97A52", 1.6) + C(40, 40, 6, "#A97A52", 1.6) + face(40, 40, 0.16)
    cap += P("M34,30 Q40,16 48,22 L48,30 Z", "url(#red)", 1.4) + K.pompom(48, 21, 2.4)
    return body, cap, hb([[31, 0, 18, 64]]), hb([[31, 40, 18, 40], [28, 30, 24, 12], [14, 22, 52, 8]]), [40, 22]

def drums():
    drum = lambda y, col: (R(10, y, 60, 32, col, 2) + R(10, y, 60, 5, "#FFFFFF", 1.6) + R(10, y + 27, 60, 5, "#FFFFFF", 1.6)
                           + "".join(f'<path d="M{x},{y+5} L{x+10},{y+27} M{x+10},{y+5} L{x},{y+27}" stroke="{GOLD2}" stroke-width="1.6"/>' for x in (16, 34, 52)))
    body = drum(0, "#7FCB8A") + drum(32, "#FFD45C")
    cap = (drum(48, "#7FCB8A") + R(10, 26, 60, 22, "#7FA8D8", 2) + R(10, 26, 60, 4, "#FFFFFF", 1.4) + E(40, 26, 30, 6, "#FFF4E6", 2) + face(40, 38, 0.26)
           + f'<path d="M20,10 L36,24 M60,10 L44,24" stroke="#C99A6B" stroke-width="3.4" stroke-linecap="round"/>' + C(20, 10, 3, "#FF8FB1", 1.2) + C(60, 10, 3, "#FF8FB1", 1.2))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 26, 60, 54], [12, 20, 56, 8]]), [40, 20]

def sandstone(x0, x1, y0, y1, col="#F2CF95", mort="#D6A866"): return bricks(x0, x1, y0, y1, col, mort, 16)
def pyramid():
    body = sandstone(10, 70, -1, 65) + sides(10, 70)
    cap = ""
    for k, (x0, x1) in enumerate(((10, 70), (16, 64), (22, 58), (28, 52))):
        y = 64 - k * 14; cap += sandstone(x0, x1, y, y + (17 if k == 0 else 14)) + R(x0, y, x1 - x0, (17 if k == 0 else 14), "none", 2)
    cap += P("M30,22 L40,6 L50,22 Z", "url(#gold)", 2) + f'<circle cx="40" cy="14" r="12" fill="url(#glow)"/>' + face(40, 44, 0.26)
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 64, 60, 16], [16, 50, 48, 14], [22, 36, 36, 14], [28, 22, 24, 14], [34, 10, 12, 12]]), [40, 10]

def obelisk():
    glyph = lambda y: (C(32, y + 8, 3, "none", 0, 'stroke="#A9708A" stroke-width="1.6"') + f'<path d="M44,{y+4} q2,4 0,8 M28,{y+22} h8 M42,{y+20} l4,6 l4,-6" stroke="#A9708A" stroke-width="1.6" fill="none"/>'
                       + f'<path d="M30,{y+40} q4,-4 8,0 q4,4 8,0" stroke="#A9708A" stroke-width="1.6" fill="none"/>' + E(46, y + 50, 3, 2, "#A9708A", 0))
    body = R(22, -1, 36, 66, "#E8B9C2", 0) + R(50, -1, 8, 66, "#D29EAA", 0) + glyph(0) + sides(22, 58)
    cap = (R(22, 30, 36, 51, "#E8B9C2", 0) + R(50, 30, 8, 51, "#D29EAA", 0) + glyph(30)[:0] + sides(22, 58, 30, 81) + P("M22,31 L40,6 L58,31 Z", "#E8B9C2", 2.2)
           + P("M33,16 L40,6 L47,16 Z", "url(#gold)", 1.6) + face(40, 44, 0.26) + glyph(56).split("<ellipse")[0][:0])
    return body, cap, hb([[22, 0, 36, 64]]), hb([[22, 30, 36, 50], [28, 20, 24, 10], [34, 10, 12, 10]]), [40, 10]

def dune(y0, y1): return R(10, y0, 60, y1 - y0, "#F6D7A0", 0) + "".join(P(f"M10,{y} Q25,{y-4} 40,{y} T70,{y}", "none", 0, 'stroke="#E2B878" stroke-width="1.8"') for y in range(y0 + 8, y1, 12))
def camel():
    body = dune(-1, 65) + sides(10, 70) + tile3(E(24, 30, 3, 1.6, "#E2B878", 0))
    cap = (dune(56, 81) + P("M10,81 V58 Q40,50 70,58 V81", "none", 2.2) + R(10, 58, 60, 23, "none", 0)
           + E(36, 48, 22, 10, "#E8C08A", 2) + C(30, 38, 9, "#E8C08A", 2) + C(44, 40, 8, "#E8C08A", 2) + E(36, 48, 20, 8, "#E8C08A", 0)
           + P("M54,46 Q60,40 58,30", "none", 0, f'stroke="{L}" stroke-width="9" stroke-linecap="round"') + P("M54,46 Q60,40 58,30", "none", 0, 'stroke="#E8C08A" stroke-width="5.4" stroke-linecap="round"')
           + E(61, 24, 9, 7, "#E8C08A", 2) + C(60, 22, 1.8, EYE, 0) + E(57, 27, 2.4, 1.4, BLUSH, 0) + P("M54,18 Q60,6 68,16 Z", "url(#red)", 1.4) + R(53, 16, 16, 3.6, FUR, 1, 1.5) + K.pompom(68, 10, 2.2)
           + R(26, 40, 16, 5, RED2, 1.2, 1) + P("M14,48 Q10,52 12,56", "none", 0, f'stroke="{L}" stroke-width="2"'))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 56, 60, 24], [14, 38, 46, 18], [24, 30, 26, 8]], [(61, 24, 9)]), [36, 30]

def pagoda():
    storey = lambda y: (R(16, y + 8, 48, 24, "#F26D7D", 2) + R(30, y + 14, 20, 14, "#FFE08A", 1.4, 2) + P(f"M4,{y+8} Q40,{y-2} 76,{y+8} L70,{y} Q40,{y-8} 10,{y} Z", "#5E5090", 2) + snowcap(10, 70, y, 3))
    body = storey(0) + storey(32) + storey(64)[:0]
    cap = (storey(56).replace('height="24"', 'height="26"') + P("M8,50 Q40,40 72,50 L64,40 Q40,32 16,40 Z", "#5E5090", 2) + snowcap(16, 64, 40, 3)
           + R(37, 8, 6, 34, GOLD, 1.6) + "".join(E(40, y, 6, 2, GOLD2, 1.2) for y in (16, 22, 28, 34)) + C(40, 6, 3, "url(#gold)", 1.4) + face(40, 70, 0.22))
    return body, cap, hb([[14, 0, 52, 64]]), hb([[14, 52, 52, 28], [10, 40, 60, 12], [36, 8, 8, 32]]), [40, 8]

def vending():
    cans = lambda y: "".join(R(18 + i * 11, y + 6, 8, 14, ("#FF8FB1", "#9EF0E0", "#FFE08A", "#AEC8FF")[i], 1.2, 2) for i in range(4)) + R(16, y + 22, 44, 3, "#C9C2E8", 0)
    body = R(12, -1, 56, 66, "#EAF4FF", 0) + R(14, -1, 48, 66, "#BFE0FF", 0) + cans(0) + cans(32) + R(62, -1, 6, 66, "#7FA8D8", 0) + sides(12, 68)
    cap = (R(12, 24, 56, 57, "#EAF4FF", 2.2, 6) + R(16, 30, 48, 20, "#FFF4E6", 1.6, 3) + cans(52) + R(62, 30, 4, 50, "#7FA8D8", 0)
           + f'<rect x="16" y="30" width="48" height="20" rx="3" fill="#9EF0E0" opacity="0.35"/>' + face(40, 40, 0.3) + snowcap(14, 66, 24, 4))
    return body, cap, hb([[12, 0, 56, 64]]), hb([[12, 24, 56, 56]]), [40, 22]

def crates():
    crate = lambda y: R(10, y, 60, 32, "#E3B98A", 2) + f'<path d="M10,{y} L70,{y+32} M10,{y+32} L70,{y}" stroke="#C99A6B" stroke-width="3"/>' + R(10, y, 60, 32, "none", 2)
    return crate(0) + crate(32), crate
def manekineko():
    body, crate = crates()
    cat = (E(40, 38, 16, 12, "#FFFFFF", 2) + C(40, 22, 14, "#FFFFFF", 2) + P("M28,14 L28,4 L36,10 Z M52,14 L52,4 L44,10 Z", "#FFFFFF", 1.8) + P("M29,12 L29,7 L33,10 Z", "#FFB3CB", 0)
           + face(40, 22, 0.3, "closed") + R(28, 32, 24, 4, RED2, 1.2, 2) + C(40, 38, 3, GOLD, 1.2) + E(56, 22, 4.4, 7, "#FFFFFF", 1.8) + C(28, 36, 3, "#FFB36B", 0, 'opacity="0.8"'))
    cap = crate(48) + cat + R(18, 46, 44, 2, "#E3B98A", 0) + sparkle(64, 8, 3)
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 48, 60, 32], [24, 26, 32, 22], [27, 10, 26, 16]]), [40, 10]

def opera():
    shell = lambda x, y, w, h: P(f"M{x},{y+h} Q{x+w*0.1},{y} {x+w},{y} Q{x+w*0.7},{y+h*0.6} {x+w},{y+h} Z", "#FFFFFF", 2) + f'<path d="M{x+w*0.3},{y+h} Q{x+w*0.4},{y+h*0.35} {x+w*0.85},{y+h*0.1}" stroke="#E6DDF7" stroke-width="1.4" fill="none"/>'
    tiles = "".join(P(f"M{x},{y} l6,4 l6,-4", "none", 0, 'stroke="#E6DDF7" stroke-width="1.2"') for x in range(12, 66, 12) for y in range(4, 64, 8))
    body = R(10, -1, 60, 66, "#FFF8F0", 0) + tiles + R(56, -1, 14, 66, "#E6DDF7", 0, 0, 'opacity="0.6"') + sides(10, 70)
    cap = (R(10, 62, 60, 19, "#E3B98A", 2) + "".join(R(14 + k * 12, 66, 8, 10, "#FFE08A", 1.2, 1) for k in range(5))
           + shell(42, 30, 28, 32) + shell(10, 22, 36, 40) + shell(26, 6, 30, 56) + face(36, 52, 0.22))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 50, 60, 30], [14, 34, 52, 16], [22, 20, 34, 14], [30, 8, 24, 12]]), [40, 8]

def surfboards():
    cols = (("#FF8FB1", "#FFFFFF"), ("#9EF0E0", "#FFE08A"), ("#FFE08A", "#FF8FB1"))
    xs = ((10, 30), (30, 50), (50, 70))
    board = lambda i, y0, y1: R(xs[i][0], y0, 20, y1 - y0, cols[i][0], 0) + R(xs[i][0] + 8, y0, 4, y1 - y0, cols[i][1], 0)
    body = "".join(board(i, -1, 65) for i in range(3)) + "".join(f'<path d="M{x},-1 V65" stroke="{L}" stroke-width="2"/>' for x in (10, 30, 50, 70)) + tile3(f'<path d="M10,28 Q40,40 70,26" stroke="#7FCB8A" stroke-width="4" fill="none"/>' + C(24, 32, 2.4, RED2, 1) + C(52, 32, 2.4, GOLD, 1))
    tips = (22, 8, 16)
    cap = ""
    for i in range(3):
        x0, x1 = xs[i]; t = tips[i]
        cap += P(f"M{x0},81 V{t+10} Q{x0},{t} {(x0+x1)/2},{t} Q{x1},{t} {x1},{t+10} V81 Z", cols[i][0], 2) + R(x0 + 8, t + 4, 4, 77 - t, cols[i][1], 0)
        cap += P(f"M{x0},81 V{t+10} Q{x0},{t} {(x0+x1)/2},{t} Q{x1},{t} {x1},{t+10} V81 Z", "none", 2)
    cap += P("M10,60 Q40,72 70,58", "none", 0, 'stroke="#7FCB8A" stroke-width="4"') + face(40, 34, 0.24) + K.pompom(40, 8, 0)[:0]
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 32, 60, 48], [12, 26, 16, 6], [32, 12, 16, 20], [52, 20, 16, 12]]), [40, 8]

def sandcastle():
    body = bricks(10, 70, -1, 65, "#F6D7A0", "#E2B878") + sides(10, 70) + tile3(P("M24,30 l3,-6 3,6 -6,-3 6,0 Z", "#FFB3CB", 1) + E(54, 48, 4, 3, "#FFF4E6", 1))
    cap = (bricks(10, 70, 40, 81, "#F6D7A0", "#E2B878") + sides(10, 70, 40, 81) + R(10, 40, 60, 2, L, 0)
           + "".join(R(x, 32, 10, 9, "#F6D7A0", 2) for x in (10, 60)) + R(26, 16, 28, 25, "#F6D7A0", 2, 2) + "".join(R(x, 10, 7, 7, "#F6D7A0", 1.8) for x in (26, 36.5, 47))
           + f'<path d="M40,10 V0" stroke="{L}" stroke-width="1.6"/>' + P("M40,0 L50,3 L40,6 Z", "#FF8FB1", 1.2) + face(40, 28, 0.24) + star5(18, 56, 5, "#FFB36B", "#C9794A", 1.2))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 40, 60, 40], [10, 32, 10, 8], [60, 32, 10, 8], [26, 16, 28, 24], [26, 10, 28, 6]]), [40, 10]

def ice_tex(x0, x1, y0, y1):
    return (R(x0, y0, x1 - x0, y1 - y0, "#DDF1FF", 0) + R(x1 - 14, y0, 14, y1 - y0, "#B9DDF5", 0)
            + "".join(f'<path d="M{x},{y0} V{y1}" stroke="#FFFFFF" stroke-width="{w}" opacity="0.7"/>' for x, w in ((18, 4), (30, 2), (44, 3))))
def iceberg():
    body = ice_tex(10, 70, -1, 65) + tile3(f'<path d="M20,10 l10,14 -6,12 M48,38 l6,10" stroke="#9EC8EE" stroke-width="1.6" fill="none"/>') + sides(10, 70)
    peak = "M10,81 V50 L18,34 L26,38 L34,14 L40,8 L48,22 L56,18 L64,40 L70,46 V81 Z"
    cap = (f'<clipPath id="ib"><path d="{peak}"/></clipPath><g clip-path="url(#ib)">{ice_tex(10, 70, 0, 81)}</g>' + P(peak, "none", 2.2)
           + P("M34,14 L40,8 L48,22 L44,20 L40,24 Z", "#FFFFFF", 1.2) + face(40, 50, 0.36))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 50, 60, 30], [16, 36, 50, 14], [26, 22, 34, 14], [34, 10, 12, 12]]), [40, 10]

def penguin(cx, top, h, hat=False):
    g = (E(cx, top + h / 2, 22, h / 2, "#4A4A78", 2) + E(cx, top + h / 2 + 3, 15, h / 2 - 5, "#FFFFFF", 0) + E(cx - 23, top + h / 2 + 2, 5, 9, "#4A4A78", 1.6, f'transform="rotate(20 {cx-23} {top+h/2+2})"')
         + E(cx + 23, top + h / 2 + 2, 5, 9, "#4A4A78", 1.6, f'transform="rotate(-20 {cx+23} {top+h/2+2})"') + face(cx, top + h * 0.34, 0.3) + P(f"M{cx-3},{top+h*0.42} L{cx},{top+h*0.48} L{cx+3},{top+h*0.42} Z", "#FFB36B", 1))
    if hat: g += P(f"M{cx-14},{top+2} Q{cx-2},{top-18} {cx+14},{top-8} L{cx+14},{top+2} Z", "url(#red)", 1.6) + R(cx - 16, top - 1, 32, 5, FUR, 1.2, 2) + K.pompom(cx + 15, top - 9, 3)
    return g
def penguins():
    body = f'<clipPath id="pg"><rect x="0" y="-1" width="80" height="66"/></clipPath><g clip-path="url(#pg)">' + penguin(40, -32, 32) + penguin(40, 0, 32) + penguin(40, 32, 32) + "</g>"
    cap = penguin(40, 48, 32) + penguin(40, 16, 34, True)
    return body, cap, hb([[14, 0, 52, 64]]), hb([[14, 48, 52, 32], [16, 18, 48, 32], [26, 8, 28, 10]]), [40, 8]

def snowman():
    ball = lambda y: C(40, y, 30, "#FFFFFF", 2) + C(50, y + 6, 18, "#E6F2FF", 0, 'opacity="0.7"') + C(40, y - 8, 2.4, "#4A3358", 0)
    body = f'<clipPath id="sm"><rect x="0" y="-1" width="80" height="66"/></clipPath><g clip-path="url(#sm)">' + ball(-16) + ball(16) + ball(48) + ball(80) + "</g>"
    cap = (f'<clipPath id="sc"><rect x="0" y="50" width="80" height="31"/></clipPath><g clip-path="url(#sc)">{ball(80)}</g>' + C(40, 34, 20, "#FFFFFF", 2.2) + face(40, 32, 0.34)
           + P("M40,36 L52,38 L40,40 Z", "#FFB36B", 1.2) + P("M22,48 Q40,56 58,48 L58,52 Q40,60 22,52 Z", RED2, 1.6) + R(52, 50, 6, 12, RED2, 1.4)
           + R(26, 12, 28, 4, "#4A3358", 1.6, 2) + R(30, 2, 20, 11, "#4A3358", 1.6, 2) + R(30, 9, 20, 3, RED2, 0))
    return body, cap, hb([[10, 0, 60, 64]]), hb([[10, 52, 60, 28], [26, 4, 28, 12]], [(40, 34, 20)]), [40, 4]


# ---------- Antarctica serac: ice cliff face with strata, snow-crusted lip piece at the screen top, drip edge at the cap
SER = dict(ice="#DDF1FF", ice2="#B9DDF5", band="#9EC8EE", deep="#7FB0E0")
def serac_face(y0, y1):
    c = SER
    g = P(f"M6,{y0} H74 V{y1} H6 Z", c["ice"], 0)
    for k in range((y0 // 16) * 16 - 16, y1 + 16, 16):        # strata every 16px -> 64 tiles seamlessly
        g += f'<path d="M6,{k} Q24,{k+3} 40,{k} T74,{k}" stroke="{c["band"]}" stroke-width="3" fill="none" opacity="0.85"/>'
        g += f'<path d="M6,{k+6} Q30,{k+8} 52,{k+6} T74,{k+7}" stroke="#FFFFFF" stroke-width="1.6" fill="none" opacity="0.7"/>'
    g += f'<rect x="58" y="{y0}" width="16" height="{y1-y0}" fill="{c["ice2"]}" opacity="0.75"/><rect x="10" y="{y0}" width="5" height="{y1-y0}" fill="#FFFFFF" opacity="0.55"/>'
    return g
def serac():
    c = SER
    cracks = f'<path d="M30,4 l5,10 -4,8 M50,36 l-4,9 5,8" stroke="{c["deep"]}" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
    body = (f'<clipPath id="sf"><rect x="6" y="-1" width="68" height="66"/></clipPath><g clip-path="url(#sf)">{serac_face(-1, 65)}{tile3(cracks)}</g>'
            f'<path d="M6,-1 V65 M74,-1 V65" stroke="{L}" stroke-width="2.2"/>')
    drip = "M6,-1 V40 Q4,48 9,52 Q22,56 40,54 Q58,56 71,52 Q76,48 74,40 V-1"
    cap = (f'<clipPath id="sc2"><path d="{drip}"/></clipPath><g clip-path="url(#sc2)">{serac_face(-1, 60)}{cracks}</g>' + P(drip, "none", 2.2)
           + f'<path d="M9,50 Q40,56 71,50" stroke="#FFFFFF" stroke-width="3" fill="none" opacity="0.9"/>'
           + icicles(8, 72, 52, [12, 22, 10, 26, 14, 20], "#BFE6FF")
           + "".join(f'<path d="M{x},{y} q-2,4 0,6 q2,-2 0,-6 Z" fill="#BFE6FF" {st(1)}/>' for x, y in ((22, 70), (52, 74)))
           + face(40, 40, 0.36, "closed"))
    lip = (P("M2,0 H110 V14 Q104,26 92,24 Q84,32 72,28 Q56,34 40,28 Q28,32 20,26 Q8,26 2,16 Z", c["ice"], 2.2)
           + "".join(f'<path d="M{a},{y} Q56,{y+3} {b},{y}" stroke="{c["band"]}" stroke-width="2.6" fill="none"/>' for a, b, y in ((6, 106, 8), (10, 100, 16)))
           + P("M0,-2 H112 V6 Q96,12 80,7 Q64,12 48,7 Q32,12 16,7 Q6,10 0,6 Z", "#FFFFFF", 1.8)
           + icicles(12, 100, 26, [6, 10, 5, 8, 4, 9, 6, 10], "#CFEAFF"))
    return body, cap, lip, hb([[10, 0, 60, 64]]), hb([[10, 0, 60, 46], [14, 46, 52, 8], [24, 54, 32, 8]])
