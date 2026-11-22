"""v0.5 art: obstacle-specific death animations (normal + golden), reusable FX, stage-transition art,
profile UI icons and sky palettes. All decorative (no hitboxes). Writes SVGs into assets/."""
import os, math, json, random
from build_ghosts import PAL, body_path, sparkle
from build_extras import bat_svg, pumpkin_svg, mini_ghost, blush, happy_eyes
OUT = os.path.join(os.path.dirname(__file__), "..")
FILES = {}
def svg(w, h, inner): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{inner}\n</svg>\n'
def inner(s): return s[s.index(">") + 1: s.rindex("</svg>")]
_uid = [0]
def uid(p): _uid[0] += 1; return f"{p}{_uid[0]}"

# ------------------------------------------------------------------ ghost puppet
TINT = {
  "soot": dict(body_hi="#E2DCE8", body_lo="#A99FB8", shade="#8E84A0", line="#4E4258", eye="#3A2E44", eye2="#5E5070", blush="#E8A9B8", mouth="#C9798F", arm="#CFC7DA"),
  "pale": dict(body_hi="#F2FAFF", body_lo="#BFE0F7", shade="#9CCBEF", line="#4E6A9A", eye="#34486E", eye2="#5A78A8", blush="#C9D8F5", mouth="#9AB8E6", arm="#DDEEFF"),
}
def pal(kind, tint=None):
    p = dict(PAL[kind])
    if tint == "soot" and kind == "golden":
        p.update(body_hi="#F2E6C4", body_lo="#C9A86A", shade="#A88A58", line="#5E4030", arm="#E6D2A4", blush="#E8A08F")
    elif tint: p.update(TINT[tint])
    return p
def eyes_svg(mode, p):
    g = []
    for i, cx in enumerate((24.2, 39.8)):
        if mode == "open" or mode == "wide":
            ry = 5.3 if mode == "open" else 6.2
            g.append(f'<ellipse cx="{cx}" cy="28.6" rx="{4.3 if mode=="open" else 4.8}" ry="{ry}" fill="{p["eye"]}"/>'
                     f'<ellipse cx="{cx-1.3}" cy="26.6" rx="1.8" ry="2.1" fill="#FFF"/><circle cx="{cx+1.6}" cy="31" r="0.95" fill="#FFF"/>')
            if mode == "wide": g.append(f'<circle cx="{cx}" cy="28.6" r="7.4" fill="none" stroke="{p["line"]}" stroke-width="0.9" opacity="0.5"/>')
        elif mode == "closed":
            g.append(f'<path d="M{cx-4},29.2 Q{cx},32.6 {cx+4},29.2" fill="none" stroke="{p["eye"]}" stroke-width="2" stroke-linecap="round"/>')
        elif mode == "swirl":
            d = f"M{cx},{28.6}"
            for k in range(1, 22):
                a = k * 0.62 * (1 if i == 0 else -1); r = k * 0.24
                d += f" L{cx + math.cos(a) * r:.2f},{28.6 + math.sin(a) * r:.2f}"
            g.append(f'<path d="{d}" fill="none" stroke="{p["eye"]}" stroke-width="1.5" stroke-linecap="round"/>')
        elif mode == "x":
            g.append(f'<path d="M{cx-3.4},25.4 L{cx+3.4},31.8 M{cx+3.4},25.4 L{cx-3.4},31.8" stroke="{p["eye"]}" stroke-width="2.2" stroke-linecap="round"/>')
        elif mode == "squeeze":  # > <
            s = 1 if i == 0 else -1
            g.append(f'<path d="M{cx-3*s},25.8 L{cx+3*s},28.8 L{cx-3*s},31.8" fill="none" stroke="{p["eye"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        elif mode == "dot":
            g.append(f'<circle cx="{cx}" cy="28.8" r="2" fill="{p["eye"]}"/>')
    return "".join(g)
def mouth_svg(mode, p):
    L = p["line"]
    if mode == "w": return f'<path d="M29.4,34.4 Q30.7,36.4 32,34.6 Q33.3,36.4 34.6,34.4" fill="none" stroke="{L}" stroke-width="1.4" stroke-linecap="round"/>'
    if mode == "o": return f'<ellipse cx="32" cy="35.6" rx="2.2" ry="2.6" fill="{p["mouth"]}" stroke="{L}" stroke-width="1.2"/>'
    if mode == "O": return f'<ellipse cx="32" cy="36" rx="3" ry="3.8" fill="{p["mouth"]}" stroke="{L}" stroke-width="1.3"/>'
    if mode == "wavy": return f'<path d="M27.5,35.4 q1.5,-1.6 3,0 q1.5,1.6 3,0 q1.5,-1.6 3,0" fill="none" stroke="{L}" stroke-width="1.3" stroke-linecap="round"/>'
    if mode == "flat": return f'<path d="M29.5,35.2 H34.5" stroke="{L}" stroke-width="1.4" stroke-linecap="round"/>'
    if mode == "tongue": return (f'<path d="M29,34.4 Q32,36.6 35,34.4" fill="none" stroke="{L}" stroke-width="1.3" stroke-linecap="round"/>'
                                 f'<path d="M32.4,35.4 q0.6,3 2.2,2.4 q0.8,-1 -0.2,-2.6" fill="#FF9EB8" stroke="{L}" stroke-width="0.9"/>')
    return ""
def ghost(kind, eyes="open", mouth="w", tint=None, arms=0, soot=False, sway=0.0, glow=True):
    """inner SVG of the 64x64 ghost (game sprite coordinates, anchor (32,32))"""
    p = pal(kind, tint); L = p["line"]; gid = uid("g")
    g = [f'<defs><radialGradient id="{gid}b" cx="0.38" cy="0.3" r="0.8"><stop offset="0" stop-color="{p["body_hi"]}"/><stop offset="0.55" stop-color="{p["body_hi"]}"/><stop offset="1" stop-color="{p["body_lo"]}"/></radialGradient>'
         f'<clipPath id="{gid}c"><path d="{body_path(sway)}"/></clipPath></defs>']
    if kind == "golden" and glow and tint is None:
        g.append(f'<defs><radialGradient id="{gid}w"><stop offset="0.45" stop-color="#FFE7A0" stop-opacity="0.55"/><stop offset="1" stop-color="#FFE7A0" stop-opacity="0"/></radialGradient></defs><circle cx="32" cy="33" r="31" fill="url(#{gid}w)"/>')
    for side, x in ((-1, 13.5), (1, 50.5)):
        g.append(f'<ellipse cx="{x + side*4.2}" cy="37" rx="6.2" ry="4" fill="{p["arm"]}" stroke="{L}" stroke-width="2" transform="rotate({arms*side} {x} 37)"/>')
    g.append(f'<path d="{body_path(sway)}" fill="url(#{gid}b)"/>')
    g.append(f'<g clip-path="url(#{gid}c)"><ellipse cx="47" cy="47" rx="17" ry="16" fill="{p["shade"]}" opacity="0.35"/>')
    if soot:
        for x, y, r in ((18, 20, 5), (44, 46, 6), (26, 50, 4), (48, 22, 3.5), (36, 14, 3)):
            g.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#6E6480" opacity="0.35"/>')
    g.append('</g>')
    g.append(f'<path d="{body_path(sway)}" fill="none" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>')
    if soot:  # frazzled tufts on top
        g.append(f'<path d="M24,10 l-2,-6 l3,3 l1,-6 l2,6 l3,-5 l0,7 l4,-4 l-1,6 l5,-2 l-4,5" fill="none" stroke="{L}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>')
    else:
        g.append(f'<ellipse cx="22" cy="15.5" rx="4.2" ry="2.4" fill="#FFF" opacity="0.9" transform="rotate(-28 22 15.5)"/>')
    for cx in (18.8, 45.2):
        g.append(f'<ellipse cx="{cx}" cy="35.2" rx="3.6" ry="2.1" fill="{p["blush"]}" opacity="0.85"/>')
    g.append(eyes_svg(eyes, p) + mouth_svg(mouth, p))
    if kind == "golden" and tint is None: g.append(sparkle(40.5, 14.5, 2.4, "#FFFFFF", "#F2B84B"))
    return "".join(g)
def place(inner_svg, dx=0, dy=0, sx=1, sy=1, rot=0, op=1, pivot=(32, 58)):
    """put a 64-space ghost into the 128 canvas: anchor (32,32) -> (64,64), then offset; scale/rotate about pivot (64-space)"""
    px, py = pivot
    return (f'<g opacity="{op}" transform="translate({32+dx},{32+dy}) translate({px},{py}) rotate({rot}) scale({sx},{sy}) translate({-px},{-py})">{inner_svg}</g>')

# ------------------------------------------------------------------ FX pieces
def star5(x, y, r, fill="#FFE9A8", line="#D9953A", rot=0, sw=1.2):
    pts = []
    for i in range(10):
        a = math.radians(rot - 90 + i * 36); rr = r if i % 2 == 0 else r * 0.48
        pts.append(f"{x + math.cos(a)*rr:.2f},{y + math.sin(a)*rr:.2f}")
    return f'<path d="M{" L".join(pts)} Z" fill="{fill}" stroke="{line}" stroke-width="{sw}" stroke-linejoin="round"/>'
def birdie(x, y, s=1.0, flap=0):
    w = -3 if flap else 2
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M-5,{w} Q-2.5,-3 0,0 Q2.5,-3 5,{w}" fill="none" stroke="#7A5A9E" stroke-width="1.4" stroke-linecap="round"/>'
            f'<ellipse cx="0" cy="1" rx="3" ry="2.4" fill="#BDEBD6" stroke="#4F7A62" stroke-width="1"/><circle cx="1.2" cy="0.6" r="0.6" fill="#2E2450"/><path d="M3,1 l1.6,0.5 l-1.6,0.5" fill="#FFC9A0"/></g>')
def stars_ring(cx, cy, rx, ry, phase, n=4, birds=True):
    """items orbit on an ellipse; back half drawn smaller. phase 0..1"""
    s = [f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#FFF4B8" stroke-width="1" stroke-dasharray="2 3" opacity="0.55"/>']
    cols = ["#FFE9A8", "#FFC9DA", "#BDEBD6", "#E3D4FF"]
    for i in range(n):
        a = 2 * math.pi * (phase + i / n)
        x, y = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        k = 0.8 + 0.25 * math.sin(a)
        if birds and i % 2 == 1: s.append(birdie(x, y, 1.1 * k, int(phase * 12 + i) % 2))
        else: s.append(star5(x, y, 4.6 * k, cols[i % 4], "#B07A3A", phase * 360))
    return "".join(s)
def puff(x, y, r, op=1.0, col="#EEE8F6", line="#9E94B8"):
    b = [(0, 0, 1), (-0.7, 0.25, 0.7), (0.7, 0.25, 0.72), (-0.35, -0.5, 0.65), (0.4, -0.45, 0.6)]
    s = "".join(f'<circle cx="{x+dx*r:.1f}" cy="{y+dy*r:.1f}" r="{rr*r*0.62:.1f}" fill="{line}"/>' for dx, dy, rr in b)
    s += "".join(f'<circle cx="{x+dx*r:.1f}" cy="{y+dy*r:.1f}" r="{rr*r*0.62-1.2:.1f}" fill="{col}"/>' for dx, dy, rr in b)
    s += f'<circle cx="{x-r*0.3:.1f}" cy="{y-r*0.35:.1f}" r="{r*0.14:.1f}" fill="#FFF" opacity="0.9"/>'
    return f'<g opacity="{op:.2f}">{s}</g>'
def bonk(x, y, r, phase=0, word=True):
    pts = []
    for i in range(16):
        a = math.radians(i * 22.5 + phase * 11); rr = r if i % 2 == 0 else r * 0.62
        pts.append(f"{x+math.cos(a)*rr:.1f},{y+math.sin(a)*rr:.1f}")
    s = f'<path d="M{" L".join(pts)} Z" fill="#FFF4B8" stroke="#E8A050" stroke-width="2" stroke-linejoin="round"/>'
    s += f'<circle cx="{x}" cy="{y}" r="{r*0.42:.1f}" fill="#FFFFFF" opacity="0.9"/>'
    for i in range(8):
        a = math.radians(i * 45 + 22); s += f'<path d="M{x+math.cos(a)*r*1.1:.1f},{y+math.sin(a)*r*1.1:.1f} L{x+math.cos(a)*r*1.35:.1f},{y+math.sin(a)*r*1.35:.1f}" stroke="#FFB6CC" stroke-width="2.2" stroke-linecap="round"/>'
    return s
def sparkle_poof(cx, cy, t):
    """t 0..1: ring of sparkles expanding and fading"""
    s = []; random.seed(5)
    cols = [("#FFF4B8", "#D9953A"), ("#FFC9DA", "#C86A8A"), ("#BDEBD6", "#4F8A6C"), ("#E3D4FF", "#7A5A9E")]
    if t < 0.5: s.append(puff(cx, cy, 14 + 26 * t, 1 - t, "#FFFFFF", "#E3D4FF"))
    for i in range(10):
        a = 2 * math.pi * i / 10 + 0.3; d = 10 + 34 * t + (i % 3) * 3
        r = (5 - 2.5 * t) * (1 if i % 2 else 0.7)
        f, l = cols[i % 4]
        s.append(f'<g opacity="{max(0, 1 - t*0.9):.2f}">' + sparkle(cx + math.cos(a) * d, cy + math.sin(a) * d, r, f, l) + '</g>')
    return "".join(s)

def fx_files():
    for i in range(6):  # stars ring loop: 64x32, orbit centre (32,16)
        FILES[f"fx-stars-ring-{i}"] = svg(64, 32, stars_ring(32, 16, 24, 8, i / 6))
    for i, (r, op, dy) in enumerate(((8, 1, 0), (12, 0.95, -4), (16, 0.75, -9), (19, 0.4, -14))):
        FILES[f"fx-smoke-puff-{i}"] = svg(48, 48, puff(24, 28 + dy, r, op))
    for i in range(5):
        FILES[f"fx-sparkle-poof-{i}"] = svg(96, 96, sparkle_poof(48, 48, i / 4))
    for i, r in enumerate((14, 24, 20)):
        FILES[f"fx-bonk-{i}"] = svg(64, 64, f'<g opacity="{1 if i < 2 else 0.6}">{bonk(32, 32, r, i)}</g>')

# ------------------------------------------------------------------ deaths (128x128, anchor (64,64) = game anchor)
def bat_inner(frame, sc=1.0): return inner(bat_svg(frame, sc))
def death_bat(kind):
    out = []
    # bat path: swoops in from top-right, grabs (frame 3), carries the ghost up-left
    for i in range(10):
        s = []
        if i < 3:
            bx, by = 108 - i * 18, 8 + i * 9
            g = ghost(kind, "open" if i < 2 else "wide", "w" if i < 2 else "O")
            s.append(place(g))
            s.append(f'<g transform="translate({bx-24},{by-25})">{bat_inner(str(i % 3))}</g>')
        else:
            k = i - 3; up = k * 9; lx = -k * 3
            sway = math.sin(k * 1.4) * 8
            g = ghost(kind, "wide" if k < 2 else "swirl", "O" if k < 3 else "wavy", arms=-35)
            s.append(place(g, lx, 4 - up, rot=sway, pivot=(32, 6)))
            # little feet grip lines + bat above the head
            s.append(f'<path d="M{60+lx},{40-up} l-2,-6 M{68+lx},{40-up} l2,-6" stroke="#54427A" stroke-width="2" stroke-linecap="round"/>')
            s.append(f'<g transform="translate({64+lx-24},{8-up})">{bat_inner(["0","1","2","1"][k % 4])}</g>')
            if k < 3: s.append(f'<path d="M{86+lx},{60-up} q4,-3 8,0 M{88+lx},{66-up} q4,-2 7,1" stroke="#FFF4B8" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
        out.append(svg(128, 128, "".join(s)))
    return out
def pumpkin_inner(): return inner(pumpkin_svg())
def death_pumpkin(kind):
    out = []
    seq = [(-60, 1, 1, "open", "o"), (-30, 1, 1, "wide", "O"), (0, 1.25, 0.72, "squeeze", "O"),
           (0, 1.5, 0.42, "swirl", "wavy"), (0, 1.55, 0.38, "swirl", "wavy"), (0, 1.5, 0.4, "swirl", "wavy"), (0, 1.52, 0.4, "swirl", "tongue"), (0, 1.5, 0.4, "swirl", "tongue")]
    for i, (py, sx, sy, e, m) in enumerate(seq):
        s = []
        flat_top = 90 - (58 - 8) * sy  # ghost top y in canvas when squashed about its base (y 90)
        s.append(f'<ellipse cx="64" cy="92" rx="{30*sx:.1f}" ry="4" fill="#2A2040" opacity="0.18"/>')
        s.append(place(ghost(kind, e, m), sx=sx, sy=sy, pivot=(32, 58)))
        if py < 0: top = -34 + i * 30
        else: top = flat_top - 50 + (2 if i == 3 else 0) - (3 if i == 2 else 0)
        s.append(f'<g transform="translate(36,{top:.1f}) scale(1.4)">{pumpkin_inner()}</g>')
        if i >= 3:
            s.append(stars_ring(64, top + 8, 22, 6, (i - 3) / 5, 3, False))
        if i == 2: s.append(f'<g opacity="0.8">{bonk(64, 74, 26, 0)}</g>'.replace('fill="#FFF4B8"', 'fill="#FFF4B8" fill-opacity="0.0"'))
        out.append(svg(128, 128, "".join(s)))
    return out
def death_meteor(kind):
    out = []
    for i in range(10):
        s = []
        if i == 0:
            s.append(bonk(64, 60, 40, 0)); s.append(place(ghost(kind, "squeeze", "O"), sx=1.08, sy=0.92))
        else:
            e, m = ("wide", "o") if i < 3 else (("squeeze", "O") if i in (4, 5) else ("dot", "wavy"))
            jit = (1 if i in (4, 5) else 0) * (2 if i % 2 else -2)
            s.append(place(ghost(kind, e, m, tint="soot", soot=True), dx=jit))
            for k in range(3):  # rising smoke from the head
                t = ((i - 1) / 9 + k / 3) % 1
                s.append(puff(46 + k * 18 + math.sin(t * 6 + k) * 4, 30 - t * 30, 6 + 8 * t, 1 - t * 0.9))
            if i in (4, 5, 6):  # cough puff from the mouth
                s.append(puff(64 + 6 + (i - 4) * 8, 74 - (i - 4) * 3, 5 + (i - 4) * 3, 1 - (i - 4) * 0.3, "#F4F0FA", "#B8AECB"))
                s.append(f'<text x="{86+(i-4)*4}" y="{62}" font-family="sans-serif" font-weight="bold" font-size="9" fill="#FFF4B8" stroke="#6B4E7A" stroke-width="0.6">*cough*</text>' if i == 5 else "")
            if i < 4:
                for k in range(3): s.append(sparkle(36 + k * 28, 96 - k * 4, 3 - k * 0.5, "#FFD27A", "#E8A050"))
        out.append(svg(128, 128, "".join(s)))
    return out
def death_tombstone(kind):
    out = []
    for i in range(10):
        s = []
        if i == 0:
            s.append(place(ghost(kind, "squeeze", "O"), dx=-3, sx=0.84, sy=1.08)); s.append(bonk(98, 56, 18, 0))
        elif i == 1:
            s.append(place(ghost(kind, "wide", "O"), dx=-6, rot=-8)); s.append(f'<g opacity="0.6">{bonk(100, 56, 14, 1)}</g>')
        else:
            k = i - 2
            s.append(place(ghost(kind, "swirl", "wavy" if k % 4 < 2 else "tongue"), dx=math.sin(k * 0.8) * 2, rot=math.sin(k * 0.8) * 6))
            s.append(stars_ring(64, 36, 26, 8, k / 8))
        out.append(svg(128, 128, "".join(s)))
    return out
def death_skull(kind):
    out = []
    for i in range(10):
        s = []; tint = None if i == 0 else "pale"
        e, m = ("wide", "O") if i < 3 else ("wide", "wavy")
        dx = (2.5 if i % 2 else -2.5) if i >= 3 else 0
        if i >= 5: dx += (i - 4) * 6
        dy = -2 * max(0, i - 4) - (4 if i == 1 else 0)
        op = 1 if i < 6 else 1 - (i - 5) * 0.2
        g = ghost(kind, e, m, tint=tint, arms=-40 if i in (1, 2) else 25, glow=False)
        s.append(place(g, dx, dy, op=op))
        if i in (1, 2): s.append(f'<path d="M30,26 l-6,-6 M28,40 h-8 M98,26 l6,-6 M100,40 h8" stroke="#BFE6FF" stroke-width="2" stroke-linecap="round"/>')
        if i >= 3:  # shiver lines + sweat drop
            s.append(f'<g opacity="{op:.2f}"><path d="M{26+dx},{52+dy} q-3,3 0,6 q3,3 0,6 M{102+dx},{52+dy} q3,3 0,6 q-3,3 0,6" stroke="#9CCBEF" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
                     f'<path d="M{84+dx},{36+dy} q3,5 0,7 q-3,-2 0,-7 z" fill="#DFF4FF" stroke="#4E6A9A" stroke-width="1"/></g>')
        if i == 0: s.append(f'<text x="84" y="22" font-family="sans-serif" font-weight="bold" font-size="16" fill="#BFE6FF" stroke="#4E6A9A" stroke-width="0.8">!!</text>')
        out.append(svg(128, 128, "".join(s)))
    return out
def death_floor(kind):
    out = []
    seq = [(1.12, 0.84, 0, "squeeze", "O"), (0.94, 1.08, -8, "wide", "o"), (1.0, 1.0, 40, "swirl", "wavy"),
           (1.0, 1.0, 82, "x", "tongue"), (1.0, 0.92, 90, "x", "tongue"), (1.0, 0.9, 90, "x", "tongue"), (1.0, 0.9, 90, "x", "flat"), (1.0, 0.9, 90, "x", "tongue")]
    for i, (sx, sy, rot, e, m) in enumerate(seq):
        s = [f'<path d="M8,{95} H120" stroke="#C9B6E8" stroke-width="2" stroke-linecap="round" opacity="0.5"/>']
        dy = -10 if i == 1 else 0
        lie = min(1, rot / 90)
        s.append(f'<ellipse cx="64" cy="95" rx="{26+8*lie:.1f}" ry="3.5" fill="#2A2040" opacity="0.2"/>')
        # rotate about the base, then drop so the side rests on the floor
        s.append(place(ghost(kind, e, m), dx=-26 * lie, dy=dy - 16 * lie, sx=sx, sy=sy, rot=rot, pivot=(32, 58)))
        if i in (0, 1):
            s.append(puff(30, 90, 7, 0.9)); s.append(puff(98, 90, 7, 0.9))
        if i >= 4: s.append(f'<g opacity="0.8">' + sparkle(40, 70, 2.6, "#FFF4B8", "#D9953A") + '</g>')
        out.append(svg(128, 128, "".join(s)))
    return out
def death_generic(kind):
    out = []
    for i in range(10):
        s = []
        if i == 0:
            s.append(place(ghost(kind, "squeeze", "O"), sx=1.06, sy=0.94)); s.append(f'<g opacity="0.8">{bonk(64, 26, 12, 0)}</g>')
        elif i <= 6:
            k = i; sc = 1 - (k - 1) * 0.1
            s.append(place(ghost(kind, "swirl", "wavy"), rot=k * 60, sx=sc, sy=sc, pivot=(32, 33)))
            s.append(f'<path d="M24,78 Q64,96 104,78" stroke="#E3D4FF" stroke-width="2" fill="none" stroke-dasharray="3 4" opacity="0.7"/>')
        else:
            s.append(sparkle_poof(64, 64, (i - 7) / 2.5 + 0.1))
            if i == 7: s.append(place(ghost(kind, "closed", "w"), sx=0.3, sy=0.3, op=0.7, pivot=(32, 33)))
        out.append(svg(128, 128, "".join(s)))
    return out
DEATHS = {"bat": death_bat, "pumpkin": death_pumpkin, "meteor": death_meteor, "tombstone": death_tombstone,
          "skull": death_skull, "floor": death_floor, "generic": death_generic}

# ------------------------------------------------------------------ transitions
STAGE_NAMES = {"graveyard": "The Graveyard", "church": "The Old Church", "countryside": "Countryside", "schools": "School Town", "city": "Big City", "space": "Outer Space"}
BANNER_COL = {"graveyard": ("#D9CCF5", "#B9A3E6", "#5E4A7E"), "church": ("#E6DCFA", "#C9B6F0", "#5E5486"), "countryside": ("#C9F0DA", "#9ED8B8", "#3F6A5E"),
              "schools": ("#FFE3A0", "#F2C46E", "#7A5A3E"), "city": ("#FFC9DA", "#F29EC4", "#6E2E58"), "space": ("#C9DAF8", "#9EB8EE", "#3E4A8A"), None: ("#FFE3EC", "#FFC2D6", "#7A4E66")}
def ribbon(stage):
    a, b, L = BANNER_COL[stage]
    s = []
    for sx in (1, -1):  # tails
        x0 = 150 - sx * 118
        s.append(f'<path d="M{x0},30 L{x0 - sx*34},30 L{x0 - sx*24},48 L{x0 - sx*34},66 L{x0},66 Z" fill="{b}" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/>'
                 f'<path d="M{x0},66 L{x0 + sx*14},76 L{x0 + sx*14},62 Z" fill="{L}" opacity="0.55"/>')
    s.append(f'<path d="M32,18 Q150,6 268,18 L268,62 Q150,50 32,62 Z" fill="{a}" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>')
    s.append(f'<path d="M40,24 Q150,13 260,24" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.75" stroke-linecap="round"/>')
    s.append(f'<path d="M40,56 Q150,45 260,56" stroke="{b}" stroke-width="2" fill="none" stroke-dasharray="4 4"/>')
    return "".join(s)
def motif(stage):
    if stage == "graveyard": return (f'<g transform="translate(8,4) scale(0.7)">{bat_inner("0")}</g><g transform="translate(258,4) scale(0.7)">{bat_inner("2")}</g>')
    if stage == "church":
        bell = lambda x: (f'<path d="M{x-9},26 C{x-9},14 {x+9},14 {x+9},26 L{x+12},32 H{x-12} Z" fill="#FFE6A6" stroke="#8E5A3C" stroke-width="1.8" stroke-linejoin="round"/>'
                          f'<circle cx="{x}" cy="34" r="2.6" fill="#F2C46E" stroke="#8E5A3C" stroke-width="1"/>')
        return bell(22) + bell(278)
    if stage == "countryside":
        lf = lambda x, y, a, c: f'<path d="M0,0 Q7,-7 15,0 Q7,7 0,0 Z" fill="{c}" stroke="#4F7A62" stroke-width="1.3" transform="translate({x},{y}) rotate({a})"/>'
        return lf(10, 20, -30, "#A9DDBF") + lf(16, 30, 20, "#FFC9A0") + lf(275, 16, 200, "#A9DDBF") + lf(272, 30, 150, "#FFB6CC")
    if stage == "schools":
        return (f'<g transform="translate(8,12) rotate(-20)"><path d="M0,0 H22 L28,4 L22,8 H0 Z" fill="#FFE08A" stroke="#7A5A3E" stroke-width="1.4"/><rect x="-4" y="0" width="5" height="8" fill="#FFB6CC" stroke="#7A5A3E" stroke-width="1.2"/></g>'
                + star5(282, 20, 8, "#FFE9A8", "#B07A3A") + star5(270, 8, 4, "#FFC9DA", "#C86A8A"))
    if stage == "city":
        return (f'<path d="M14,10 l6,10 h-5 l5,12" stroke="#FF9EC8" stroke-width="5" fill="none" opacity="0.3" stroke-linecap="round"/><path d="M14,10 l6,10 h-5 l5,12" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round"/>'
                f'<path d="M280,10 l-6,10 h5 l-5,12" stroke="#9EF0E0" stroke-width="5" fill="none" opacity="0.3" stroke-linecap="round"/><path d="M280,10 l-6,10 h5 l-5,12" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round"/>')
    if stage == "space":
        return (f'<circle cx="20" cy="20" r="10" fill="#FFC2DD" stroke="#5A4A8A" stroke-width="1.8"/><ellipse cx="20" cy="21" rx="17" ry="4.5" fill="none" stroke="#9EF0E0" stroke-width="2.2" transform="rotate(-15 20 21)"/>'
                + star5(280, 18, 8, "#FFE9A8", "#B07A3A") + sparkle(268, 34, 3, "#FFF", "#9EB8EE"))
    return sparkle(26, 22, 6, "#FFF4B8", "#D9953A") + sparkle(274, 22, 6, "#FFF4B8", "#D9953A")
def banner(stage=None, title=None):
    a, b, L = BANNER_COL[stage]
    s = ribbon(stage) + motif(stage)
    if title:
        fs = 25 if len(title) <= 12 else 22
        s += (f'<text x="150" y="{47}" text-anchor="middle" font-family="Capriola, sans-serif" font-size="{fs}" fill="#FFFFFF" stroke="{L}" stroke-width="5" stroke-linejoin="round" paint-order="stroke">{title}</text>')
    return svg(300, 90, s)
def swoosh(i):
    t = i / 5
    x1 = -40 + t * 320; x0 = x1 - 140
    gid = f"sw{i}"
    s = (f'<defs><linearGradient id="{gid}" x1="{x0}" y1="0" x2="{x1}" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
         f'<stop offset="0.7" stop-color="#FFE3EC" stop-opacity="0.75"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="1"/></linearGradient></defs>'
         f'<path d="M{x0},40 Q{(x0+x1)/2},18 {x1},28 Q{(x0+x1)/2},34 {x0},46 Z" fill="url(#{gid})"/>'
         f'<path d="M{x0+30},48 Q{(x0+x1)/2+10},34 {x1-10},38" stroke="#E3D4FF" stroke-width="2" fill="none" opacity="0.7" stroke-linecap="round"/>')
    for k in range(4):
        s += sparkle(x1 - k * 34 + 6, 28 + (k % 2) * 12 - 6, 5 - k, "#FFF4B8", "#D9953A", 1 - k * 0.2)
    return svg(240, 64, f'<g opacity="{1 if i < 5 else 0.5}">{s}</g>')
def burst_item(stage, k, x, y, a, sc):
    t = f'transform="translate({x:.1f},{y:.1f}) rotate({a:.0f}) scale({sc:.2f})"'
    if stage == "graveyard": return f'<g {t}><g transform="scale(0.45) translate(-24,-25)">{bat_inner(str(k % 3))}</g></g>'
    if stage == "church":
        if k % 2: return f'<g {t}><path d="M-7,6 C-7,-4 7,-4 7,6 L9,9 H-9 Z" fill="#FFE6A6" stroke="#8E5A3C" stroke-width="1.4"/><circle cy="10" r="1.8" fill="#F2C46E"/></g>'
        return f'<g {t}><path d="M-8,0 Q-2,-7 2,-2 Q6,-8 10,-6 Q6,0 2,2 Q-2,6 -8,0 Z" fill="#FFFFFF" stroke="#7A7AB0" stroke-width="1.3"/><circle cx="-4" cy="-1" r="0.8" fill="#3E3A6E"/></g>'
    if stage == "countryside":
        c = ["#A9DDBF", "#FFC9A0", "#FFB6CC", "#FFE08A"][k % 4]
        return f'<g {t}><path d="M-8,0 Q0,-7 8,0 Q0,7 -8,0 Z" fill="{c}" stroke="#4F7A62" stroke-width="1.2"/><path d="M-8,0 H8" stroke="#4F7A62" stroke-width="0.8"/></g>'
    if stage == "schools":
        if k % 2: return f'<g {t}>{star5(0, 0, 6, ["#FFE9A8", "#FFC9DA", "#BDEBD6"][k % 3], "#B07A3A")}</g>'
        return f'<g {t}><rect x="-6" y="-7" width="12" height="14" rx="1" fill="#FFFFFF" stroke="#7A7AB0" stroke-width="1.2"/><path d="M-3,-3 H3 M-3,0 H3 M-3,3 H1" stroke="#A9C8F0" stroke-width="1"/></g>'
    if stage == "city":
        c = ["#FF9EC8", "#9EF0E0", "#FFE9A8"][k % 3]
        return f'<g {t}><path d="M-6,0 H6 M0,-6 V6" stroke="{c}" stroke-width="5" opacity="0.35" stroke-linecap="round"/><path d="M-6,0 H6 M0,-6 V6" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/></g>'
    c = ["#FFE9A8", "#FFFFFF", "#C9DAF8", "#FFC9DA"][k % 4]
    return f'<g {t}>{star5(0, 0, 6, c, "#7A7AB0")}</g>'
def burst(stage, i):
    t = (i + 1) / 6; random.seed(11 + len(stage)); s = []
    for k in range(14):
        a = 2 * math.pi * k / 14 + random.uniform(-0.2, 0.2); sp = random.uniform(0.7, 1.0)
        d = 12 + 62 * sp * (1 - (1 - t) ** 2)
        x, y = 80 + math.cos(a) * d, 80 + math.sin(a) * d + 18 * t * t
        op = 1 if t < 0.7 else 1 - (t - 0.7) / 0.35
        s.append(f'<g opacity="{max(0, op):.2f}">' + burst_item(stage, k, x, y, random.uniform(-40, 40) + 120 * t, 1.0 + 0.2 * math.sin(k)) + '</g>')
    if i == 0: s.append(f'<circle cx="80" cy="80" r="14" fill="#FFF4B8" opacity="0.5"/>' + sparkle(80, 80, 9, "#FFFFFF", "#E8A050"))
    return svg(160, 160, "".join(s))
def badge(n=None):
    s = (f'<path d="M12,8 H84 Q92,8 92,16 V32 Q92,40 84,40 H12 Q4,40 4,32 V16 Q4,8 12,8 Z" fill="#FFE3EC" stroke="#7A4E66" stroke-width="2.4"/>'
         f'<path d="M10,13 H60" stroke="#FFF" stroke-width="2" stroke-linecap="round" opacity="0.8"/>'
         f'<circle cx="74" cy="24" r="13" fill="#FFE08A" stroke="#8E5A3C" stroke-width="2"/>' + sparkle(91, 6, 4, "#FFF4B8", "#D9953A"))
    s += '<text x="36" y="30" text-anchor="middle" font-family="Capriola, sans-serif" font-size="15" fill="#7A4E66">Stage</text>'
    if n is not None:
        s += f'<text x="74" y="30" text-anchor="middle" font-family="Capriola, sans-serif" font-size="17" fill="#5A3828">{n}</text>'
    return svg(96, 48, s)

# ------------------------------------------------------------------ profile icons
def icon(name, size, col=None):
    k = size / 48
    if name == "add-player":
        s = (f'<circle cx="22" cy="25" r="17" fill="#E3D4FF" stroke="#5E4A7E" stroke-width="2.4"/>'
             f'<g transform="translate(22,26) scale(1.35)">{inner(svg(1,1,mini_ghost(0, 0, 1)))}</g>'
             f'<circle cx="37" cy="35" r="9" fill="#BDEBD6" stroke="#3F6A5E" stroke-width="2.2"/><path d="M37,30.5 V39.5 M32.5,35 H41.5" stroke="#3F6A5E" stroke-width="2.6" stroke-linecap="round"/>')
    elif name == "player-chip":
        a, b = col
        s = (f'<circle cx="24" cy="24" r="20" fill="{a}" stroke="#5E4A7E" stroke-width="2.4"/><circle cx="24" cy="24" r="16" fill="none" stroke="{b}" stroke-width="2"/>'
             f'<path d="M12,14 Q16,9 22,8" stroke="#FFF" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.8"/>'
             f'<g transform="translate(24,26) scale(1.55)">{mini_ghost(0, 0, 1)}</g>')
    else:  # trophy
        s = (f'<path d="M14,8 H34 V18 C34,26 30,30 24,30 C18,30 14,26 14,18 Z" fill="#FFE08A" stroke="#8E5A3C" stroke-width="2.4" stroke-linejoin="round"/>'
             f'<path d="M14,11 H8 Q8,21 15,22 M34,11 H40 Q40,21 33,22" fill="none" stroke="#8E5A3C" stroke-width="2.4" stroke-linecap="round"/>'
             f'<path d="M21,30 H27 V36 H21 Z" fill="#F2C46E" stroke="#8E5A3C" stroke-width="2"/><rect x="14" y="36" width="20" height="6" rx="2" fill="#FFC9DA" stroke="#8E5A3C" stroke-width="2"/>'
             f'<path d="M18,11 V19" stroke="#FFF6D6" stroke-width="2.4" stroke-linecap="round"/>' + happy_eyes(20.5, 27.5, 18, 2, "#5A3828", 1.4) + blush(18, 30, 22, 1.8, 1.1)
             + sparkle(41, 6, 3.4, "#FFF4B8", "#D9953A"))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 48 48">\n{s}\n</svg>\n'
CHIP_COLS = {"pink": ("#FFC9DA", "#FFFFFF"), "mint": ("#BDEBD6", "#FFFFFF"), "butter": ("#FFE9A8", "#FFFFFF"), "lilac": ("#E3D4FF", "#FFFFFF")}

def build():
    fx_files()
    for t, fn in DEATHS.items():
        for kind in ("normal", "golden"):
            for i, s in enumerate(fn(kind)):
                FILES[f"death-{t}-{i}" if kind == "normal" else f"death-{t}-golden-{i}"] = s
    FILES["ui-banner-blank"] = banner(None)
    for st, nm in STAGE_NAMES.items():
        FILES[f"ui-banner-{st}"] = banner(st, nm)
        FILES[f"ui-banner-{st}-blank"] = banner(st)
        for i in range(6): FILES[f"fx-burst-{st}-{i}"] = burst(st, i)
    for i in range(6): FILES[f"fx-swoosh-{i}"] = swoosh(i)
    FILES["ui-stage-badge-blank"] = badge()
    for n in range(1, 7): FILES[f"ui-stage-badge-{n}"] = badge(n)
    for size in (32, 48):
        FILES[f"ui-icon-add-player-{size}"] = icon("add-player", size)
        FILES[f"ui-icon-trophy-{size}"] = icon("trophy", size)
        for c, col in CHIP_COLS.items(): FILES[f"ui-icon-player-chip-{c}-{size}"] = icon("player-chip", size, col)
    return FILES

if __name__ == "__main__":
    build()
    for k, v in FILES.items(): open(os.path.join(OUT, k + ".svg"), "w").write(v)
    print(len(FILES), "files")
