"""Concept-only (not wired): 'The Void' endless zone after space. 3 directions A/B/C.
Script-generated SVG -> PNG; assembles void-concept-{A,B,C}.png. Does not touch game assets/hitboxes."""
import os, sys, math, random, io, cairosvg
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(OUT, "..", "..", "tools"))
from build_v05 import ghost, star5
from build_ghosts import sparkle
FONT = "/usr/share/fonts/truetype/sand-box/google/Fredoka/Fredoka-VariableFont_wdth,wght.ttf"
def font(sz):
    f = ImageFont.truetype(FONT, sz)
    try: f.set_variation_by_name("Bold")
    except Exception: pass
    return f
def svg(w, h, s): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{s}</svg>'
def render(w, h, s, scale=1):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(w, h, s).encode(), scale=scale))).convert("RGBA")

D = {
 "A": dict(name="A · Nebula Drift", pitch="Dreamy lilac nebula where lost keepsakes float on pastel ribbons, sleepy and sweet.",
   mood="Soft, floaty, lullaby. Objects bob slowly on satin ribbons hanging from cloud-banks; bottoms rest on drifting cotton-candy cloud islands. Cute sleepy faces, sparkles, no hard edges.",
   bg=("#2A2150", "#7A64AE"), blobs=["#FFB6D9", "#C9B6FF", "#A9E4FF"], fill="#F3EAFF", fill2="#D9C6F5", line="#6B4E7A", acc="#FFB6CC", acc2="#AEE3C6",
   screen="#BFE6FF", face=True, tether="ribbon", base="cloud",
   swatch=["#2A2150", "#7A64AE", "#F3EAFF", "#D9C6F5", "#6B4E7A", "#FFB6CC", "#AEE3C6", "#BFE6FF"]),
 "B": dict(name="B · Static Signal", pitch="A lost-channel VHS void: CRT towers, teal/magenta chroma glitch and scanlines, cute pixel faces on the screens.",
   mood="Playful retro-tech. Navy static with scanlines; objects have chunky teal outlines and a magenta chromatic offset. Tops hang from tangled coiled cables (phone cords / AV leads); bottoms are wobbly stacks of CRTs and cassettes. Faces are pixel emotes shown on screens.",
   bg=("#0E1630", "#1F2F55"), blobs=["#4FE3D6", "#FF6FB5"], fill="#25385E", fill2="#1A2848", line="#4FE3D6", acc="#FF6FB5", acc2="#FFE08A",
   screen="#7FF2E6", face=True, tether="coil", base="stack",
   swatch=["#0E1630", "#1F2F55", "#25385E", "#4FE3D6", "#7FF2E6", "#FF6FB5", "#FFE08A", "#F4F0FF"]),
 "C": dict(name="C · Memory Glow", pitch="A deep ink void where warm sepia memories glow like lanterns, hung on golden light-threads.",
   mood="Quiet and nostalgic, slightly mysterious but never scary. Near-black indigo ink; each object glows warm sepia/amber like an old photo. Tops hang on thin golden threads; bottoms float on glowing memory-dust pools. Closed, content eyes.",
   bg=("#0B0A14", "#1E1830"), blobs=["#F2C98A", "#E89A6A"], fill="#F2DDB4", fill2="#D9B88A", line="#5A3A24", acc="#E89A6A", acc2="#FFE7B0",
   screen="#FFE7B0", face=True, tether="thread", base="dust",
   swatch=["#0B0A14", "#1E1830", "#F2DDB4", "#D9B88A", "#5A3A24", "#E89A6A", "#FFE7B0", "#8A6A9E"]),
}

def face(P, x, y, s=1.0, mode=None):
    L = "#2E2450" if P is D["B"] else P["line"]
    if P is D["B"]:  # pixel emote
        c = "#0E1630"
        return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-7" y="-4" width="3" height="3" fill="{c}"/><rect x="4" y="-4" width="3" height="3" fill="{c}"/>'
                f'<rect x="-3" y="2" width="2" height="2" fill="{c}"/><rect x="-1" y="3" width="2" height="2" fill="{c}"/><rect x="1" y="2" width="2" height="2" fill="{c}"/>'
                f'<rect x="-10" y="0" width="3" height="2" fill="{P["acc"]}"/><rect x="7" y="0" width="3" height="2" fill="{P["acc"]}"/></g>')
    closed = P is D["C"] or P is D["A"]
    eyes = (f'<path d="M-7,-1 Q-5,1.5 -3,-1 M3,-1 Q5,1.5 7,-1" fill="none" stroke="{L}" stroke-width="1.6" stroke-linecap="round"/>' if closed else
            f'<circle cx="-5" cy="-1" r="2" fill="{L}"/><circle cx="5" cy="-1" r="2" fill="{L}"/>')
    return (f'<g transform="translate({x},{y}) scale({s})">{eyes}<path d="M-1.6,2.6 Q0,4 1.6,2.6" fill="none" stroke="{L}" stroke-width="1.3" stroke-linecap="round"/>'
            f'<ellipse cx="-9" cy="2.5" rx="2.4" ry="1.4" fill="#FFB3CB" opacity="0.8"/><ellipse cx="9" cy="2.5" rx="2.4" ry="1.4" fill="#FFB3CB" opacity="0.8"/></g>')

def S(P, w=2.6): return f'stroke="{P["line"]}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
# ---- objects in a 100x100 box ----
def typewriter(P):
    return (f'<path d="M22,30 L78,30 L84,46 L16,46 Z" fill="{P["fill2"]}" {S(P)}/><rect x="30" y="16" width="40" height="16" rx="2" fill="#FFFFFF" {S(P,2)}/>'
            f'<path d="M36,22 H64 M36,27 H56" stroke="{P["line"]}" stroke-width="1.4" opacity="0.5"/>'
            f'<rect x="12" y="44" width="76" height="34" rx="9" fill="{P["fill"]}" {S(P)}/><rect x="8" y="36" width="10" height="8" rx="3" fill="{P["acc"]}" {S(P,2)}/>'
            + "".join(f'<circle cx="{22 + i*8}" cy="{70 if r else 62}" r="2.8" fill="{P["acc2"]}" {S(P,1.4)}/>' for r in (0, 1) for i in range(8 - r))
            + face(P, 50, 52, 0.9))
def crt(P):
    scr = (f'<rect x="20" y="24" width="50" height="40" rx="10" fill="{P["screen"]}" {S(P,2.2)}/>'
           + (''.join(f'<path d="M22,{28+i*4} H68" stroke="#0E1630" stroke-width="1" opacity="0.18"/>' for i in range(9)) if P is D["B"] else '')
           + f'<path d="M26,30 Q30,26 36,27" stroke="#FFF" stroke-width="2" fill="none" opacity="0.8"/>')
    return (f'<path d="M40,16 L30,4 M52,16 L64,2" {S(P,2.2)}/><circle cx="30" cy="4" r="2.5" fill="{P["acc"]}"/><circle cx="64" cy="2" r="2.5" fill="{P["acc"]}"/>'
            f'<rect x="12" y="16" width="76" height="58" rx="12" fill="{P["fill"]}" {S(P)}/>{scr}'
            f'<circle cx="80" cy="32" r="3.5" fill="{P["acc"]}" {S(P,1.4)}/><circle cx="80" cy="44" r="3.5" fill="{P["acc2"]}" {S(P,1.4)}/>'
            f'<path d="M26,74 L22,84 M74,74 L78,84" {S(P,3)}/>' + face(P, 45, 45, 1.0))
def phone(P):
    dial = "".join(f'<circle cx="{50 + math.cos(math.radians(a))*13:.1f}" cy="{58 + math.sin(math.radians(a))*13:.1f}" r="3" fill="{P["fill"]}" {S(P,1.2)}/>' for a in range(-60, 241, 30))
    return (f'<path d="M14,32 Q14,18 30,20 L70,20 Q86,18 86,32 L80,38 L66,34 L34,34 L20,38 Z" fill="{P["acc"]}" {S(P)}/>'
            f'<path d="M24,40 Q50,30 76,40 L84,80 Q50,88 16,80 Z" fill="{P["fill"]}" {S(P)}/>'
            f'<circle cx="50" cy="58" r="19" fill="{P["fill2"]}" {S(P,2)}/>{dial}<circle cx="50" cy="58" r="7" fill="#FFF" {S(P,1.4)}/>'
            f'<path d="M84,72 q8,4 4,10 q-6,4 -2,10 q6,4 2,8" fill="none" {S(P,2)}/>' + face(P, 50, 59, 0.55))
def cassette(P):
    return (f'<rect x="10" y="26" width="80" height="50" rx="7" fill="{P["fill"]}" {S(P)}/><rect x="20" y="34" width="60" height="22" rx="5" fill="#FFFFFF" {S(P,2)}/>'
            f'<circle cx="35" cy="45" r="7" fill="{P["fill2"]}" {S(P,2)}/><circle cx="65" cy="45" r="7" fill="{P["fill2"]}" {S(P,2)}/>'
            f'<path d="M42,45 H58" stroke="{P["acc"]}" stroke-width="3"/><path d="M28,76 L32,64 H68 L72,76" fill="{P["acc2"]}" {S(P,2)}/>'
            f'<path d="M22,30 H78" stroke="{P["acc"]}" stroke-width="2.4"/>' + face(P, 50, 46, 0.6)
            + f'<path d="M86,68 q8,6 2,14 q-8,6 0,14" fill="none" stroke="{P["acc"]}" stroke-width="2.4" stroke-linecap="round"/>')
def gramophone(P):
    return (f'<path d="M44,62 Q40,40 20,18 Q34,8 52,10 Q70,8 86,14 Q66,34 56,60 Z" fill="{P["acc"]}" {S(P)}/>'
            f'<path d="M32,16 Q48,28 50,58 M62,12 Q56,30 52,58" fill="none" stroke="{P["line"]}" stroke-width="1.4" opacity="0.5"/>'
            f'<rect x="22" y="62" width="56" height="24" rx="5" fill="{P["fill"]}" {S(P)}/><ellipse cx="50" cy="62" rx="30" ry="5" fill="{P["fill2"]}" {S(P,2)}/>'
            f'<path d="M58,86 V92 M42,86 V92" {S(P,3)}/>' + face(P, 50, 75, 0.8))
def clock(P):
    return (f'<circle cx="30" cy="20" r="10" fill="{P["acc"]}" {S(P)}/><circle cx="70" cy="20" r="10" fill="{P["acc"]}" {S(P)}/>'
            f'<path d="M30,84 L24,92 M70,84 L76,92" {S(P,3)}/><circle cx="50" cy="54" r="34" fill="{P["fill"]}" {S(P)}/>'
            f'<circle cx="50" cy="54" r="27" fill="#FFFFFF" {S(P,2)}/>'
            + "".join(f'<circle cx="{50+math.cos(math.radians(a))*22:.1f}" cy="{54+math.sin(math.radians(a))*22:.1f}" r="1.8" fill="{P["line"]}"/>' for a in range(0, 360, 30))
            + f'<path d="M50,54 L50,38 M50,54 L60,58" {S(P,2.6)}/>' + face(P, 50, 64, 0.65) + f'<rect x="46" y="14" width="8" height="8" rx="2" fill="{P["acc2"]}" {S(P,1.6)}/>')
OBJ = {"typewriter": typewriter, "crt-tv": crt, "rotary-phone": phone, "cassette": cassette, "gramophone": gramophone, "alarm-clock": clock}

def obj(P, name, x, y, s=1.0, rot=0):
    g = OBJ[name](P)
    if P is D["B"]:  # chroma offset glitch
        ghostcopy = g.replace(P["line"], P["acc"])
        g = f'<g opacity="0.55" transform="translate(-3,1)">{ghostcopy}</g>{g}'
    if P is D["C"]:
        g = (f'<defs><radialGradient id="mg"><stop offset="0" stop-color="#F2C98A" stop-opacity="0.55"/><stop offset="1" stop-color="#F2C98A" stop-opacity="0"/></radialGradient></defs>'
             f'<circle cx="50" cy="52" r="58" fill="url(#mg)"/>{g}')
    if P is D["A"]:
        g += sparkle(90, 12, 4, "#FFF4B8", "#D9953A") + sparkle(8, 82, 3, "#FFFFFF", "#9E94B8")
    return f'<g transform="translate({x},{y}) rotate({rot} {50*s} {50*s}) scale({s})">{g}</g>'

def background(P, w, h, seed=3):
    a, b = P["bg"]; r = random.Random(seed)
    g = [f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>']
    for i, c in enumerate(P["blobs"]): g.append(f'<radialGradient id="bl{i}"><stop offset="0" stop-color="{c}" stop-opacity="0.45"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
    g.append(f'</defs><rect width="{w}" height="{h}" fill="url(#bg)"/>')
    for k in range(6):
        i = k % len(P["blobs"]); g.append(f'<ellipse cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" rx="{r.uniform(80, 200):.0f}" ry="{r.uniform(60, 140):.0f}" fill="url(#bl{i})"/>')
    for _ in range(int(w * h / 3000)):
        g.append(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.uniform(0.6, 1.8):.1f}" fill="#FFF4D6" opacity="{r.uniform(0.3, 0.9):.2f}"/>')
    if P is D["B"]:
        g += [f'<rect x="0" y="{y}" width="{w}" height="1.5" fill="#000" opacity="0.25"/>' for y in range(0, h, 4)]
        for _ in range(5):
            y = r.uniform(0, h); g.append(f'<rect x="0" y="{y:.0f}" width="{w}" height="{r.uniform(2, 6):.0f}" fill="{r.choice(P["blobs"])}" opacity="0.18"/>')
    if P is D["C"]:
        for _ in range(30): g.append(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.uniform(1, 2.5):.1f}" fill="#F2C98A" opacity="{r.uniform(0.2, 0.6):.2f}"/>')
    return "".join(g)

def tether(P, x, y0, y1):
    if P["tether"] == "ribbon":
        d = f"M{x},{y0} " + " ".join(f"Q{x + (8 if i % 2 else -8)},{y0 + (i + 0.5) * (y1 - y0) / 6:.0f} {x},{y0 + (i + 1) * (y1 - y0) / 6:.0f}" for i in range(6))
        return f'<path d="{d}" fill="none" stroke="#6B4E7A" stroke-width="9" stroke-linecap="round"/><path d="{d}" fill="none" stroke="{P["acc"]}" stroke-width="6" stroke-linecap="round"/>'
    if P["tether"] == "coil":
        n = max(3, int(abs(y1 - y0) / 7)); d = f"M{x},{y0} " + " ".join(f"L{x + (7 if i % 2 else -7)},{y0 + i * (y1 - y0) / n:.0f}" for i in range(1, n)) + f" L{x},{y1}"
        return f'<path d="{d}" fill="none" stroke="{P["acc"]}" stroke-width="4" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{P["line"]}" stroke-width="1.5" transform="translate(2,0)" opacity="0.7"/>'
    return (f'<path d="M{x},{y0} V{y1}" stroke="#FFE7B0" stroke-width="7" opacity="0.18"/><path d="M{x},{y0} V{y1}" stroke="#F2C98A" stroke-width="2.4"/>'
            + "".join(f'<circle cx="{x}" cy="{y0 + (y1 - y0) * k / 4:.0f}" r="2.6" fill="#FFE7B0"/>' for k in range(1, 4)))
def base(P, cx, y, w):
    if P["base"] == "cloud":
        return "".join(f'<circle cx="{cx + dx}" cy="{y + dy}" r="{r}" fill="#FFFFFF" stroke="#C9B6E8" stroke-width="2.5"/>' for dx, dy, r in ((-w*0.35, 10, 22), (w*0.35, 10, 22), (-w*0.12, 0, 28), (w*0.15, 2, 26), (0, 22, 30)))
    if P["base"] == "dust":
        return (f'<ellipse cx="{cx}" cy="{y + 14}" rx="{w*0.75}" ry="20" fill="#F2C98A" opacity="0.25"/><ellipse cx="{cx}" cy="{y + 14}" rx="{w*0.5}" ry="10" fill="#FFE7B0" opacity="0.4"/>'
                + "".join(f'<circle cx="{cx + (k - 3) * 12}" cy="{y + 6 + (k % 2) * 8}" r="2" fill="#FFE7B0"/>' for k in range(7)))
    return ""

def column(P, cx, top, gap_y, h, objs):
    """returns svg: top column for top=True hangs from y=0 down to gap_y; bottom stands from gap_y to h"""
    g = []; s = 0.9; ow = 100 * s
    if top:
        y = gap_y - ow * len(objs)
        g.append(tether(P, cx, 0, y + 8))
        for i, n in enumerate(objs):
            if i: g.append(tether(P, cx, y + ow * i - 6, y + ow * i + 8))
            g.append(obj(P, n, cx - ow / 2, y + ow * i, s, (-1) ** i * 4))
    else:
        y = gap_y
        if P["base"] == "stack": g.append(f'<path d="M{cx},{y + ow*len(objs) - 6} V{h}" stroke="{P["acc"]}" stroke-width="5"/>')
        else: g.append(tether(P, cx, y + ow * len(objs) - 8, h))
        for i, n in enumerate(objs):
            g.append(obj(P, n, cx - ow / 2, y + ow * i, s, (-1) ** i * -4))
        if P["base"] != "stack": g.insert(1, base(P, cx, y + ow * len(objs) - 18, ow))
    return "".join(g)

COLS = {"A": (["alarm-clock", "rotary-phone"], ["gramophone", "cassette"]),
        "B": (["rotary-phone", "cassette"], ["crt-tv", "crt-tv", "typewriter"]),
        "C": (["gramophone", "alarm-clock"], ["typewriter", "rotary-phone"])}
def gameplay(k, P):
    W, H = 360, 640; tops, bots = COLS[k]
    g = [background(P, W, H, 5)]
    g.append(column(P, 250, True, 250, H, tops)); g.append(column(P, 250, False, 420, H, bots))
    g.append(f'<g opacity="0.5">{obj(P, "cassette", 30, 520, 0.45, 20)}{obj(P, "alarm-clock", 300, 40, 0.35, -15)}</g>')
    g.append(f'<rect x="200" y="250" width="100" height="170" fill="none" stroke="#FFFFFF" stroke-width="1.2" stroke-dasharray="4 5" opacity="0.5"/>')
    g.append(f'<g transform="translate(80,300) scale(1)">{ghost("normal")}</g>')
    return render(W, H, "".join(g))

def transition(k, P):
    pw, ph = 170, 300; panels = []
    sp = ("#120F2C", "#2B2050")
    for i in range(4):
        r = random.Random(9); g = []
        if i == 0:
            g.append(f'<rect width="{pw}" height="{ph}" fill="{sp[0]}"/>' + "".join(f'<circle cx="{r.uniform(0,pw):.0f}" cy="{r.uniform(0,ph):.0f}" r="1.3" fill="#FFF"/>' for _ in range(40)))
            g.append(f'<circle cx="130" cy="60" r="22" fill="#E3D4FF" stroke="#6B5A84" stroke-width="2"/>')
        elif i == 3:
            g.append(background(P, pw, ph, 2) + obj(P, "crt-tv" if k == "B" else "alarm-clock", 80, 40, 0.7, 6))
        else:
            if k == "A":  # stars melt into nebula clouds
                t = i / 3; g.append(f'<rect width="{pw}" height="{ph}" fill="{sp[0]}"/><rect width="{pw}" height="{ph}" fill="{P["bg"][1]}" opacity="{t*0.8:.2f}"/>')
                g += [f'<ellipse cx="{r.uniform(0,pw):.0f}" cy="{r.uniform(0,ph):.0f}" rx="{20+40*t:.0f}" ry="{12+30*t:.0f}" fill="{r.choice(P["blobs"])}" opacity="{0.25+0.3*t:.2f}"/>' for _ in range(5 + 4 * i)]
                if i == 2: g.append(tether(P, 50, 0, 120) + tether(P, 125, 0, 70) + obj(P, "rotary-phone", 20, 110, 0.6, -6))
            elif k == "B":  # signal lost: static + rolling bars
                g.append(f'<rect width="{pw}" height="{ph}" fill="{sp[0]}"/>')
                for y in range(0, ph, 3):
                    if r.random() < 0.6 * i / 2: g.append(f'<rect x="0" y="{y}" width="{pw}" height="2" fill="{r.choice(["#4FE3D6","#FF6FB5","#F4F0FF","#1F2F55"])}" opacity="{r.uniform(.2,.7):.2f}"/>')
                if i == 2: g.append(f'<rect x="30" y="120" width="110" height="40" rx="6" fill="#0E1630" stroke="#4FE3D6" stroke-width="2"/><text x="85" y="147" font-family="monospace" font-size="18" font-weight="bold" fill="#FF6FB5" text-anchor="middle">NO SIGNAL</text>')
                else: g.append(f'<rect x="0" y="0" width="{pw}" height="{ph}" fill="#FFF" opacity="0.06"/>')
            else:  # stars dim, one warm light grows like a memory
                t = i / 3; g.append(f'<rect width="{pw}" height="{ph}" fill="{P["bg"][0]}"/>' + "".join(f'<circle cx="{r.uniform(0,pw):.0f}" cy="{r.uniform(0,ph):.0f}" r="1.2" fill="#FFF" opacity="{1-t:.2f}"/>' for _ in range(40)))
                g.append(f'<defs><radialGradient id="tg{i}"><stop offset="0" stop-color="#FFE7B0" stop-opacity="0.9"/><stop offset="1" stop-color="#F2C98A" stop-opacity="0"/></radialGradient></defs><circle cx="85" cy="150" r="{30 + 50*i}" fill="url(#tg{i})"/>')
        g.append(f'<g transform="translate({pw/2-26},{ph-80}) scale(0.8)">{ghost("normal", "wide" if i in (1, 2) else "open", "o" if i in (1, 2) else "w")}</g>')
        panels.append(render(pw, ph, "".join(g)))
    return panels
TRANS = {"A": ["Space", "Stars blur into pastel mist", "Ribbons drift in from above", "The Void: Nebula Drift"],
         "B": ["Space", "Signal crackles, scanlines roll", "NO SIGNAL… then it tunes in", "The Void: Static Signal"],
         "C": ["Space", "Stars go out one by one", "A warm memory-light blooms", "The Void: Memory Glow"]}

def wrap(d, text, xy, f, width, fill):
    x, y = xy; line = ""
    for w in text.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=f) > width: d.text((x, y), line, font=f, fill=fill); y += f.size + 4; line = w
        else: line = t
    d.text((x, y), line, font=f, fill=fill); return y + f.size + 4

def sheet(k):
    P = D[k]; W, H = 1240, 900
    im = render(W, H, background(P, W, H, 1)); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for box in ((16, 16, W - 16, 120), (16, 132, 392, 830), (404, 132, W - 16, 470), (404, 482, W - 16, 884)):
        od.rounded_rectangle(box, 16, fill=(10, 8, 24, 120))
    im.alpha_composite(ov); d = ImageDraw.Draw(im)
    tc = "#FFF4E8"
    d.text((32, 24), f"The Void: concept {P['name']}", font=font(34), fill=tc)
    wrap(d, P["mood"], (32, 68), font(15), 800, "#E8E0F4")
    for i, c in enumerate(P["swatch"]):  # palette
        x = 852 + (i % 4) * 95; y = 28 + (i // 4) * 44
        d.rounded_rectangle((x, y, x + 24, y + 24), 7, fill=c, outline="#FFFFFF", width=2); d.text((x + 28, y + 5), c, font=font(12), fill=tc)
    d.text((32, 140), "Sample gameplay (360x640)", font=font(17), fill=tc)
    im.alpha_composite(gameplay(k, P), (24, 166))
    d.text((32, 810), "dashed box = gap · ghost 64px", font=font(13), fill="#CFC6E6")
    d.text((420, 140), "Obstacle sketches", font=font(17), fill=tc)
    for i, n in enumerate(OBJ):
        x, y = 420 + i * 134, 170
        im.alpha_composite(render(130, 130, obj(P, n, 10, 8, 1.1)), (x, y)); d.text((x + 10, y + 132), n, font=font(13), fill=tc)
    # top/bottom logic
    d.text((420, 330), "Top / bottom logic", font=font(17), fill=tc)
    logic = {"A": "TOPS hang from cloud-banks on satin ribbons (1-2 objects). BOTTOMS sit on cotton-candy cloud islands, ribbon down to the edge.",
             "B": "TOPS dangle from coiled phone/AV cords. BOTTOMS are wobbly CRT + cassette stacks on a cable to the floor.",
             "C": "TOPS hang on golden light-threads. BOTTOMS float on memory-dust pools with a thread down to the edge."}[k]
    y = wrap(d, logic, (420, 356), font(14), 790, "#E8E0F4")
    wrap(d, "Hitbox continuity (later): treat each tether/cord/stack link as a solid rect at least 24px wide from the screen edge to the gap edge, so there is no fly-through between objects. Objects bob ±4px visually only.", (420, y + 2), font(13), 790, "#CFC6E6")
    d.text((420, 490), "Transition: Space to The Void", font=font(17), fill=tc)
    for i, p in enumerate(transition(k, P)):
        x = 420 + i * 200; im.alpha_composite(p, (x, 518))
        d.rounded_rectangle((x, 518, x + 170, 818), 8, outline="#FFFFFF", width=2)
        wrap(d, f"{i+1}. {TRANS[k][i]}", (x, 826), font(13), 175, tc)
    out = os.path.join(OUT, f"void-concept-{k}.png")
    im.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(out, optimize=True)
    return out

if __name__ == "__main__":
    for k in D: p = sheet(k); print(p, os.path.getsize(p))
