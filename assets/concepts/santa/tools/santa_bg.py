"""Lite backgrounds for Santa's Rocket Run (same approach as the Void v0.6 set, ASSETS.md 14.2):
each layer = a few transparent content bands drawn at world-y offsets inside a 720-wide, horizontally seamless tile slot,
over a 2-stop sky gradient (santa-sky-palettes.json). No full-height opaque tiles."""
import math, random
from santa_lib import *
W = 720
SKY = {  # top, bottom (y 0 -> 640)
 "lapland": ("#1B2348", "#3E5E8A"), "london": ("#1F1D44", "#5B5596"), "newyork": ("#1C2044", "#4C3E7A"), "rio": ("#241A4A", "#7A4E8E"),
 "egypt": ("#2A2350", "#C98A7A"), "tokyo": ("#1A1840", "#5A3E86"), "sydney": ("#6EC3F0", "#FFE3B8"), "antarctica": ("#16264A", "#4E7AA8"), "aurora": ("#0E1430", "#2E2A66")}
STARS = {"lapland", "london", "newyork", "rio", "egypt", "tokyo", "antarctica", "aurora"}
def wrap(inner): return inner + f'<g transform="translate(-{W},0)">{inner}</g><g transform="translate({W},0)">{inner}</g>'
def band(h, inner): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">{DEFS}{wrap(inner)}</svg>'
def hills(yb, amp, col, k=(2, 5), ph=0.0, h=None, line=None):
    pts = [f"{x},{yb - amp*(0.6*math.sin(2*math.pi*k[0]*x/W + ph) + 0.4*math.sin(2*math.pi*k[1]*x/W + ph*2)):.1f}" for x in range(0, W + 1, 8)]
    return f'<path d="M0,{h or yb+400} L{" L".join(pts)} L{W},{h or yb+400} Z" fill="{col}"' + (f' stroke="{line}" stroke-width="2"' if line else "") + "/>"
def peaks(ps, base, col, snow="#FFFFFF"):
    g = ""
    for x, w, hh in ps:
        g += f'<path d="M{x-w},{base} L{x},{base-hh} L{x+w},{base} Z" fill="{col}"/>'
        g += f'<path d="M{x-w*0.3:.0f},{base-hh*0.7:.0f} L{x},{base-hh} L{x+w*0.3:.0f},{base-hh*0.7:.0f} L{x+w*0.12:.0f},{base-hh*0.64:.0f} L{x},{base-hh*0.72:.0f} L{x-w*0.14:.0f},{base-hh*0.64:.0f} Z" fill="{snow}" opacity="0.9"/>'
    return g
def skyline(base, col, lit, seed, hmin=40, hmax=140, wmin=26, wmax=52, op=0.55, spire=0.15):
    r = random.Random(seed); g = ""; x = 0
    while x < W:
        w = r.randint(wmin, wmax); h = r.randint(hmin, hmax); w = min(w, W - x) if W - x < wmin else w
        g += f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{col}"/>'
        if r.random() < spire: g += f'<rect x="{x+w/2-2}" y="{base-h-18}" width="4" height="18" fill="{col}"/>'
        for wx in range(x + 5, x + w - 6, 9):
            for wy in range(base - h + 8, base - 8, 14):
                if r.random() < 0.45: g += f'<rect x="{wx}" y="{wy}" width="4" height="6" fill="{lit}" opacity="{op}"/>'
        x += w + r.randint(0, 6)
    return g
def pine_sil(x, b, s, col, snow=True):
    g = ""
    for k in range(3):
        y = b - 18 * s - k * 16 * s; w = (20 - k * 5) * s
        g += f'<path d="M{x-w:.1f},{y+14*s:.1f} L{x},{y-10*s:.1f} L{x+w:.1f},{y+14*s:.1f} Z" fill="{col}"/>'
        if snow: g += f'<path d="M{x-w*0.5:.1f},{y+2*s:.1f} L{x},{y-10*s:.1f} L{x+w*0.5:.1f},{y+2*s:.1f} Z" fill="#FFFFFF" opacity="0.75"/>'
    return g + f'<rect x="{x-2*s:.1f}" y="{b-8*s:.1f}" width="{4*s:.1f}" height="{8*s:.1f}" fill="{col}"/>'
def aurora_band(h, cols, seed):
    r = random.Random(seed); g = []
    for i, c in enumerate(cols):
        ph = r.uniform(0, 6); y0 = 30 + i * 26; amp = 30
        top = [f"{x},{y0 + amp*math.sin(2*math.pi*2*x/W + ph) + 10*math.sin(2*math.pi*5*x/W):.1f}" for x in range(0, W + 1, 12)]
        bot = [f"{x},{y0 + 90 + amp*math.sin(2*math.pi*2*x/W + ph + 0.4) + 14*math.sin(2*math.pi*3*x/W + ph):.1f}" for x in range(W, -1, -12)]
        gid = f"au{i}"
        g.append(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c}" stop-opacity="0"/><stop offset="0.6" stop-color="{c}" stop-opacity="0.55"/><stop offset="1" stop-color="{c}" stop-opacity="0.05"/></linearGradient></defs>'
                 f'<path d="M{" L".join(top)} L{" L".join(bot)} Z" fill="url(#{gid})"/>')
        for x in range(10, W, 18): g.append(f'<path d="M{x},{y0 + amp*math.sin(2*math.pi*2*x/W + ph) + 20:.0f} v60" stroke="{c}" stroke-width="3" opacity="0.18"/>')
    # v0.8.4 top-bleed fix: alpha fade over the band's top TOP_FADE px (the engine's edge bleed stretches the canvas top rows)
    m = (f'<defs><linearGradient id="tfg{seed}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{TOP_FADE}"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#FFF"/></linearGradient>'
         f'<mask id="tfm{seed}" maskUnits="userSpaceOnUse" x="{-W}" y="0" width="{3*W}" height="{h}"><rect x="{-W}" y="0" width="{3*W}" height="{h}" fill="url(#tfg{seed})"/></mask></defs>')
    return m + f'<g mask="url(#tfm{seed})">' + "".join(g) + "</g>"
TOP_FADE = 24

def stars_tile():
    r = random.Random(77); g = []
    for _ in range(70):
        x, y = r.uniform(0, 360), r.uniform(0, 320); rr = r.choice((0.8, 1, 1.2, 1.5))
        for dx in (-360, 0, 360):
            for dy in (-320, 0, 320):
                if y + dy - rr * 3 < TOP_FADE: continue  # v0.8.4: keep the tile's top rows dark (tile y=0 = canvas top -> edge bleed)
                if 0 <= x + dx + rr * 3 and x + dx - rr * 3 <= 360 and 0 <= y + dy + rr * 3 and y + dy - rr * 3 <= 320:
                    g.append(f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="{rr}" fill="#FDF6FF" opacity="{r.uniform(0.35, 0.9):.2f}"/>')
    for x, y in ((60, 50), (250, 120), (150, 260)):  # all below TOP_FADE
        g.append(sparkle(x, y, 3.2, "#FFFFFF", "#9EB8EE", 0.8))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="360" height="320" viewBox="0 0 360 320">{"".join(g)}</svg>'

# -------------- per-stage bands: list of (layer, part, y, h, svg-inner) --------------
def bg_parts(s):
    P_ = []
    add = lambda layer, part, y, h, inner, note="": P_.append((layer, part, y, h, inner, note))
    if s == "lapland":
        add("far", "aurora", 20, 220, aurora_band(220, ("#7FF0C0", "#B9A3F5", "#7FD8F0"), 3), "northern lights")
        add("far", "fells", 360, 160, hills(80, 34, "#4E6A9A", (2, 5), 0.3) + hills(110, 20, "#5E7EAE", (3, 7), 1.2), "snowy fells")
        add("mid", "forest", 380, 200, "".join(pine_sil(x, 190, 1.4 + (x % 3) * 0.2, "#2E4A6E") for x in range(10, W, 46))
            + f'<g transform="translate(420,98)"><rect x="0" y="40" width="110" height="52" fill="#3E3A6E"/><path d="M-10,42 L55,0 L120,42 Z" fill="#3E3A6E"/><path d="M-12,42 L55,-2 L122,42 L110,44 L55,8 L0,44 Z" fill="#FFFFFF" opacity="0.85"/>'
              + "".join(f'<rect x="{12+k*30}" y="54" width="18" height="16" rx="3" fill="#FFE08A" opacity="0.9"/>' for k in range(3)) + '<rect x="80" y="8" width="14" height="26" fill="#3E3A6E"/>'
              + '<circle cx="88" cy="-4" r="7" fill="#C9C2E8" opacity="0.5"/><circle cx="96" cy="-16" r="5" fill="#C9C2E8" opacity="0.35"/></g>'
            + "".join(f'<g transform="translate({x},{168}) scale({sc})"><ellipse cx="0" cy="0" rx="16" ry="8" fill="#2E3A5E"/><path d="M12,-4 L18,-16 L24,-14 L20,-4 Z M-10,6 v12 M-4,6 v12 M6,6 v12 M12,6 v12" fill="#2E3A5E" stroke="#2E3A5E" stroke-width="3"/>'
                      f'<path d="M20,-16 l-4,-8 M20,-16 l2,-9 M22,-15 l6,-6" stroke="#2E3A5E" stroke-width="2"/></g>' for x, sc in ((150, 1.1), (210, 0.9), (620, 1.0))), "pines, reindeer, elf workshop")
        add("near", "snow", 560, 80, hills(26, 8, "#F4F8FF", (3, 8), 0.5, 120) + "".join(pine_sil(x, 34, 0.9, "#4F7A8A") for x in (40, 230, 480, 650)), "snow ground")
    elif s == "london":
        add("far", "skyline", 360, 140, skyline(140, "#3A3670", "#FFE7A8", 5, 30, 90, op=0.4), "far roofs")
        add("mid", "landmarks", 220, 320, f'<rect x="0" y="250" width="{W}" height="70" fill="#3A3670" opacity="0.8"/><path d="M0,250 H{W}" stroke="#FFFFFF" stroke-width="2" opacity="0.25"/>'
            + K.big_ben(90, 254, 1.0, "#47427F", "#FFE7A8") + K.tower_bridge(300, 254, "#47427F", "#FFE7A8") + K.big_ben(610, 254, 0.7, "#423C78", "#FFE7A8").replace("scale(0.7)", "scale(0.7)"), "Big Ben, Tower Bridge, Thames")
        rows = K.house_row(80, ("#6E5E9C", "#7C6BB0", "#5E5090"), random.Random(12))
        rows2 = K.house_row(80, ("#6E5E9C", "#7C6BB0", "#5E5090"), random.Random(13))
        clip = '<clipPath id="hr"><rect x="0" y="0" width="360" height="140"/></clipPath>'
        add("near", "roofs", 500, 140, clip + f'<g clip-path="url(#hr)">{rows}</g><g transform="translate(360,0)"><g clip-path="url(#hr)">{rows2}</g></g>'
            + f'<path d="M0,94 Q180,86 360,94 T{W},92 V140 H0 Z" fill="#FFFFFF"/>' + f'<g transform="translate(470,40) scale(0.8)">{K.bus(0, 0)}</g>', "snowy roofs + red bus")
    elif s == "newyork":
        add("far", "skyline", 300, 220, skyline(220, "#2E2E66", "#FFE7A8", 9, 60, 190, 22, 44, 0.35, 0.3), "far skyline")
        tree = (f'<g transform="translate(520,0)">' + "".join(f'<path d="M{-40+k*8},{200-k*42} L0,{140-k*42} L{40-k*8},{200-k*42} Z" fill="#3E7A5E"/>' for k in range(3))
                + "".join(f'<circle cx="{(i*37)%60-30}" cy="{80+(i*53)%120}" r="2.6" fill="{("#FF8FB1","#FFE08A","#9EF0E0")[i%3]}"/>' for i in range(18)) + star5(0, 52, 12, GOLD, "#B07A3A") + '<rect x="-8" y="200" width="16" height="20" fill="#5E4A3E"/></g>')
        add("mid", "towers", 260, 280, skyline(280, "#3E3A78", "#FFE08A", 21, 80, 220, 34, 60, 0.6, 0.0)
            + '<g transform="translate(240,0)"><rect x="-26" y="90" width="52" height="190" fill="#4A4588"/><rect x="-18" y="60" width="36" height="30" fill="#4A4588"/><rect x="-10" y="36" width="20" height="24" fill="#4A4588"/><rect x="-3" y="0" width="6" height="36" fill="#4A4588"/><circle cx="0" cy="0" r="4" fill="#FF8FB1"/></g>'
            + tree, "skyscrapers, Empire-ish spire, Rockefeller tree")
        taxi = lambda x: f'<g transform="translate({x},40)"><rect x="0" y="10" width="64" height="20" rx="6" fill="#FFD45C"/><path d="M12,10 L20,0 H44 L52,10 Z" fill="#FFD45C"/><path d="M18,9 L23,3 H41 L46,9 Z" fill="#BFE6FF"/><circle cx="14" cy="30" r="6" fill="#4A3358"/><circle cx="50" cy="30" r="6" fill="#4A3358"/><rect x="26" y="-5" width="12" height="5" fill="#FFF4C9"/></g>'
        add("near", "street", 540, 100, f'<rect x="0" y="62" width="{W}" height="38" fill="#F4F8FF"/><path d="M0,62 Q180,56 360,62 T{W},62" fill="#FFFFFF"/>' + taxi(90) + taxi(400) + taxi(610), "snowy street + taxis")
    elif s == "rio":
        cristo = '<g transform="translate(200,40)"><rect x="-3" y="0" width="6" height="34" fill="#4A3A7A"/><rect x="-24" y="8" width="48" height="5" rx="2" fill="#4A3A7A"/><circle cx="0" cy="-4" r="4" fill="#4A3A7A"/></g>'
        fw = "".join(f'<g transform="translate({x},{y})">' + "".join(f'<path d="M0,0 L{math.cos(a)*r:.1f},{math.sin(a)*r:.1f}" stroke="{c}" stroke-width="2" stroke-linecap="round" opacity="0.85"/>' for a in [i*math.pi/6 for i in range(12)]) + f'<circle r="3" fill="#FFFFFF"/></g>'
                     for x, y, r, c in ((90, 40, 22, "#FF8FB1"), (360, 20, 26, "#FFE08A"), (560, 50, 20, "#9EF0E0")))
        add("far", "corcovado", 160, 260, fw + hills(200, 40, "#3E2E6E", (2, 3), 1.0, 300).replace('d="M0,300', 'd="M0,300')
            + '<path d="M150,80 Q200,60 250,80 L300,260 H100 Z" fill="#3E2E6E"/>' + cristo, "Corcovado + Christ the Redeemer silhouette, fireworks")
        add("mid", "sugarloaf", 300, 260, '<path d="M380,260 Q390,40 470,30 Q540,40 560,260 Z" fill="#5A4488"/><path d="M200,260 Q220,140 290,130 Q340,140 350,260 Z" fill="#54407E"/>'
            + '<path d="M290,132 L470,32" stroke="#C9C2E8" stroke-width="1.6" opacity="0.7"/><rect x="372" y="78" width="16" height="12" rx="3" fill="#FFD45C"/>' + hills(240, 10, "#4A3878", (3, 6), 0, 260), "Sugarloaf + cable-car line")
        add("near", "promenade", 480, 160, f'<g transform="translate(0,60)"><rect x="0" y="40" width="{W}" height="60" fill="#FFF4E6"/>' + "".join(f'<path d="M{x},60 q15,-14 30,0 t30,0" stroke="#4A3A5E" stroke-width="5" fill="none"/>' for x in range(0, W, 60))
            + "".join(f'<g transform="translate({x},40)"><path d="M0,0 Q4,-30 2,-56" stroke="#5E4A3E" stroke-width="6" fill="none"/>' + "".join(f'<path d="M2,-56 q{dx},{-8} {dx*1.6},{12}" stroke="#3E7A5E" stroke-width="6" fill="none" stroke-linecap="round"/>' for dx in (-14, -7, 7, 14)) + '</g>' for x in (120, 420, 640)) + "</g>", "Copacabana wave promenade + palms")
    elif s == "egypt":
        add("far", "dunes", 380, 160, hills(70, 24, "#B9787E", (2, 5), 0.2) + hills(100, 16, "#C98A84", (3, 4), 1.6), "far dunes")
        sphinx = '<g transform="translate(560,150)"><path d="M-60,40 V20 Q-40,10 0,12 L10,-10 Q14,-30 30,-30 Q44,-28 44,-10 L46,40 Z" fill="#7A4E6E"/><path d="M18,-28 L14,-6 M42,-28 L46,-6" stroke="#7A4E6E" stroke-width="6"/></g>'
        add("mid", "pyramids", 340, 200, '<path d="M60,190 L190,40 L320,190 Z" fill="#8A5A74"/><path d="M190,40 L320,190 H240 Z" fill="#7A4E6E"/><path d="M300,190 L390,90 L480,190 Z" fill="#8A5A74"/><path d="M390,90 L480,190 H430 Z" fill="#7A4E6E"/>'
            + '<path d="M180,52 L190,40 L200,52 Z" fill="#FFD873"/>' + sphinx, "pyramids + Sphinx")
        camel = lambda x: f'<g transform="translate({x},20)"><ellipse cx="0" cy="30" rx="22" ry="10" fill="#6E4A5E"/><circle cx="-6" cy="20" r="8" fill="#6E4A5E"/><path d="M18,28 Q26,16 24,6" stroke="#6E4A5E" stroke-width="6" fill="none"/><ellipse cx="28" cy="4" rx="7" ry="5" fill="#6E4A5E"/><path d="M-14,36 v20 M-6,36 v20 M8,36 v20 M14,36 v20" stroke="#6E4A5E" stroke-width="4"/></g>'
        add("near", "sand", 540, 100, hills(70, 8, "#F6D7A0", (3, 7), 0.8, 120) + camel(150) + camel(220) + camel(520), "sand + camel train")
    elif s == "tokyo":
        add("far", "fuji", 200, 300, f'<path d="M140,300 L300,60 Q340,46 380,60 L560,300 Z" fill="#4E4A8E"/><path d="M266,110 L300,60 Q340,46 380,60 L414,110 Q392,100 376,114 Q356,96 340,112 Q322,96 304,114 Q288,100 266,110 Z" fill="#FFFFFF" opacity="0.9"/>', "Mt Fuji")
        tower = '<g transform="translate(560,0)"><path d="M-30,260 L0,0 L30,260 Z" fill="none" stroke="#F26D7D" stroke-width="5"/><path d="M-22,190 H22 M-14,120 H14 M-8,70 H8" stroke="#F26D7D" stroke-width="5"/><path d="M-24,180 L18,120 M24,180 L-18,120" stroke="#F26D7D" stroke-width="2"/></g>'
        neon = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="none" stroke="{c}" stroke-width="3" opacity="0.9"/>' for x, y, w, h, c in ((40, 120, 18, 50, "#FF8FC8"), (190, 90, 40, 16, "#9EF0E0"), (330, 140, 16, 44, "#FFE08A"), (440, 110, 36, 14, "#FF8FC8")))
        add("mid", "city", 280, 260, skyline(260, "#3A2E6E", "#FFE08A", 33, 60, 170, 30, 56, 0.5) + tower + neon, "city, Tokyo Tower, neon")
        lant = "".join(f'<path d="M{x},10 Q{x+60},30 {x+120},10" stroke="#3A2E5E" stroke-width="2" fill="none"/>' + "".join(f'<ellipse cx="{x+20+k*20}" cy="{22+ (8 if k in (2,3) else 4)}" rx="6" ry="8" fill="#FF6F7F"/>' for k in range(5)) for x in range(0, W, 120))
        add("near", "street", 520, 120, lant + f'<rect x="0" y="90" width="{W}" height="30" fill="#F4F8FF"/><path d="M0,90 Q180,84 360,90 T{W},90" fill="#FFFFFF"/>', "lantern strings + snowy street")
    elif s == "sydney":
        add("far", "sea", 380, 160, f'<circle cx="560" cy="40" r="34" fill="#FFF4C9"/><circle cx="560" cy="40" r="50" fill="#FFF4C9" opacity="0.35"/><rect x="0" y="90" width="{W}" height="70" fill="#5EB0E0"/>'
            + "".join(f'<path d="M{x},{y} q10,-4 20,0" stroke="#FFFFFF" stroke-width="2" fill="none" opacity="0.6"/>' for x, y in ((40, 110), (200, 130), (330, 104), (480, 140), (640, 118))), "sea horizon + sun")
        opera = '<g transform="translate(150,190)"><rect x="-80" y="0" width="200" height="30" fill="#E3B98A"/>' + "".join(f'<path d="M{x},0 Q{x+4},{-h} {x+w},{-h} Q{x+w*0.7},{-h*0.5} {x+w},0 Z" fill="#FFFFFF" stroke="#C9C2E8" stroke-width="2"/>' for x, w, h in ((-70, 40, 50), (-40, 56, 84), (10, 46, 66), (50, 50, 90), (90, 30, 40))) + '</g>'
        bridge = '<g transform="translate(400,0)"><path d="M0,200 Q140,40 280,200" fill="none" stroke="#8E86B8" stroke-width="10"/><path d="M0,200 Q140,70 280,200" fill="none" stroke="#8E86B8" stroke-width="4"/>' + "".join(f'<path d="M{x},{200 - (1-((x-140)/140)**2)*130:.0f} V170" stroke="#8E86B8" stroke-width="2"/>' for x in range(30, 260, 22)) + '<rect x="-20" y="168" width="320" height="8" fill="#8E86B8"/><rect x="-24" y="120" width="22" height="80" fill="#C9AF9E"/><rect x="282" y="120" width="22" height="80" fill="#C9AF9E"/></g>'
        add("mid", "harbour", 330, 230, f'<rect x="0" y="200" width="{W}" height="30" fill="#4E9ED0"/>' + opera + bridge, "Opera House + Harbour Bridge")
        boards = "".join(f'<rect x="{x}" y="10" width="14" height="56" rx="7" fill="{c}" stroke="#6B4E7A" stroke-width="2"/>' for x, c in ((80, "#FF8FB1"), (98, "#9EF0E0"), (520, "#FFE08A")))
        add("near", "beach", 540, 100, f'<rect x="0" y="50" width="{W}" height="50" fill="#FFE3B8"/><path d="M0,50 Q90,40 180,50 T360,50 T540,50 T{W},50" fill="#FFFFFF" opacity="0.8"/>' + boards
            + f'<g transform="translate(300,30)"><path d="M0,30 L0,-10" stroke="#6B4E7A" stroke-width="3"/><path d="M-34,-6 Q0,-34 34,-6 Z" fill="#FF8FB1" stroke="#6B4E7A" stroke-width="2"/></g>', "beach, surfboards, umbrella")
    elif s in ("antarctica", "aurora"):
        cols = ("#FF9ED8", "#7FF0D0", "#9EB8FF") if s == "antarctica" else ("#7FF0C0", "#FF9ED8", "#9EB8FF", "#B9A3F5")
        add("far", "aurora", 10, 260 if s == "aurora" else 220, aurora_band(220, cols, 8 if s == "antarctica" else 15), "aurora australis" if s == "antarctica" else "big aurora")
        if s == "antarctica":
            add("far", "mountains", 360, 160, peaks([(80, 90, 120), (230, 70, 90), (380, 110, 140), (560, 80, 100), (700, 70, 90)], 160, "#4E6A9E", "#E6F2FF"), "far ice mountains")
            berg = lambda x, w, h: f'<path d="M{x-w},{200} L{x-w*0.6},{200-h*0.7} L{x-w*0.2},{200-h} L{x+w*0.3},{200-h*0.8} L{x+w},{200} Z" fill="#9EC8EE"/><path d="M{x-w*0.2},{200-h} L{x+w*0.3},{200-h*0.8} L{x+w*0.1},{200} L{x-w*0.3},{200} Z" fill="#BFE0F8"/>'
            add("mid", "icebergs", 360, 210, f'<rect x="0" y="196" width="{W}" height="14" fill="#3E6A9A"/>' + berg(120, 70, 110) + berg(360, 50, 80) + berg(600, 80, 130), "icebergs")
            peng = lambda x: f'<g transform="translate({x},30)"><ellipse cx="0" cy="14" rx="8" ry="13" fill="#2E2E58"/><ellipse cx="0" cy="17" rx="5" ry="9" fill="#FFFFFF"/><circle cx="0" cy="0" r="6" fill="#2E2E58"/><path d="M4,0 l5,1 -5,2 Z" fill="#FFB36B"/></g>'
            add("near", "shelf", 540, 100, f'<path d="M0,58 Q180,48 360,58 T{W},56 V100 H0 Z" fill="#F4F8FF"/>' + "".join(peng(x) for x in (60, 80, 300, 520, 540, 560)), "ice shelf + penguins")
        else:
            add("mid", "ribbons", 200, 200, aurora_band(200, ("#7FF0C0", "#B9A3F5"), 29).replace('opacity="0.18"', 'opacity="0.08"'), "faint second aurora")
            add("near", "horizon", 560, 80, hills(40, 6, "#2E3A6E", (3, 7), 0.2, 80) + "".join(sparkle(x, 30, 3, "#FFFFFF", "#9EB8EE", 0.8) for x in (90, 300, 520)), "dark ice horizon")
    return P_
