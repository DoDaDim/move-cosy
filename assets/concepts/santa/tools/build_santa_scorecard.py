"""Santa scorecard frame 600x800 (+@2x), same safe areas as assets/scorecard-layout.json. Writes packs/santa/assets/."""
import os, sys, json, random, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from santa_lib import *
import santa_lib as SL
from build_santa_stages import heart
import build_santa_v080 as V  # reuse drawers (does not export on import)
T = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(T, "../../../.."))
PACK = os.path.join(ROOT, "packs/santa/assets")
def put(inner, x, y, sc=1, rot=0): return f'<g transform="translate({x},{y}) rotate({rot}) scale({sc})">{inner}</g>'
def frame():
    x, y, w, h = 36, 36, 528, 688; bord = "#F7B9C6"; Ln = "#7A4E66"
    g = ['<defs><linearGradient id="sc_bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2348"/><stop offset="1" stop-color="#3E5E8A"/></linearGradient>'
         '<radialGradient id="sc_glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.95"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>',
         '<rect width="600" height="800" fill="url(#sc_bg)"/>']
    rnd = random.Random(5)
    for _ in range(36): g.append(flake(round(rnd.uniform(6, 594), 1), round(rnd.uniform(6, 794), 1), round(rnd.uniform(2, 4.5), 1), "#FFFFFF", "#9FB6D6", rnd.uniform(0, 60)))
    for i in range(14):
        for yy in (y, y + h): g.append(C(round(x + 18 + i * (w - 36) / 13, 1), yy, 14, bord if i % 2 else "#FFFFFF", 2.4, f'stroke="{Ln}"'))
    for i in range(18):
        for xx in (x, x + w): g.append(C(xx, round(y + 18 + i * (h - 36) / 17, 1), 14, bord if i % 2 else "#FFFFFF", 2.4, f'stroke="{Ln}"'))
    g.append(R(x, y, w, h, bord, 0, 34)); g.append(R(x + 12, y + 12, w - 24, h - 24, "#FFF8F0", 2.6, 26, f'stroke="{Ln}"'))
    g.append(f'<rect x="{x+20}" y="{y+20}" width="{w-40}" height="{h-40}" rx="20" fill="none" stroke="#F26D7D" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>')
    g.append(snowcap(70, 530, 49, 6))
    g.append('<circle cx="300" cy="166" r="118" fill="url(#sc_glow)"/><circle cx="300" cy="166" r="104" fill="#E6F2FF" opacity="0.75"/><ellipse cx="300" cy="258" rx="70" ry="8" fill="#D6E6F7" opacity="0.9"/>')
    for i, dx in enumerate((-60, -30, 0, 30, 60)):
        g.append(star5(300 + dx, 532, 7, GOLD) if dx == 0 else C(300 + dx, 532, 5, ("#F26D7D", "#AEE3C6", "", "#AEE3C6", "#F26D7D")[i], 1.4, f'stroke="{Ln}"'))
    g.append(R(110, 544, 380, 60, "#FFE3EC", 2.4, 30, f'stroke="{Ln}"'))
    g.append(f'<path d="M70,738 L52,760 L70,782 H530 L548,760 L530,738 Z" fill="#FFF8F0" stroke="{Ln}" stroke-width="2.6" stroke-linejoin="round"/><path d="M82,744 H518" stroke="{bord}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>')
    # corner deco (kept off the safe areas): baubles hanging from the card's top rim on ribbons, gifts on the bottom rim, flying reindeer
    for bx, by, kind in ((92, 120, "rush"), (508, 104, "life")):
        g.append(f'<path d="M{bx},50 V{by-22}" stroke="#F26D7D" stroke-width="2.4"/>' + put(V.BAUB_SVG(kind), bx - 28, by - 30, 1.0))
    g.append(put(V.F_REIN, 448, 200, 1.6)); g.append(put(V.F_REIN, 64, 380, 1.3))
    g.append(put(V.GIFT("#9ED8FF", "#FFFFFF"), 52, 664, 1.0) + put(V.GIFT("#FF8FA8", "#FFD873"), 100, 678, 0.7) + put(V.GIFT("#AEE3C6", "#F26D7D"), 470, 666, 0.95))
    for (sx, sy, r) in ((150, 92, 9), (452, 300, 8), (80, 470, 7), (514, 520, 7), (300, 22, 10)): g.append(star5(sx, sy, r))
    for (sx, sy, r) in ((172, 130, 5), (430, 112, 6), (494, 600, 5), (250, 652, 4), (360, 662, 5), (300, 690, 4)): g.append(sparkle(sx, sy, r))
    return svg(600, 800, "".join(g))
if __name__ == "__main__":
    s = frame(); open(os.path.join(T, "../v080/svg/ui-santa-scorecard-frame.svg"), "w").write(s)
    SL.png(s, 600, 800).save(os.path.join(PACK, "ui-santa-scorecard-frame.png"), optimize=True)
    SL.png(s, 1200, 1600).save(os.path.join(PACK, "ui-santa-scorecard-frame@2x.png"), optimize=True)
    lay = json.load(open(os.path.join(ROOT, "assets/scorecard-layout.json")))
    lay["_note"] = "Santa copy of assets/scorecard-layout.json: identical safe areas (600x800, x2 for @2x). Draw Santa C idle frame 0 in the 'ghost' rect (96x128 art: centre its anchor (48,48) on the rect centre)."
    json.dump(lay, open(os.path.join(PACK, "santa-scorecard-layout.json"), "w"), indent=1); print("ok")
