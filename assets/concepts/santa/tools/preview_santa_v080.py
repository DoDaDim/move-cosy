import os, glob
from PIL import Image, ImageDraw, ImageFont
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(T, "../../../.."))
P2 = os.path.join(R, "packs/santa/assets/png/2x"); FONT = "/usr/share/fonts/truetype/sand-box/google/Capriola/Capriola-Regular.ttf"
rows = [("1  Reindeer stampede (Lapland) - FIRST", ["event-santa-reindeer-strip", "ui-santa-event-warning-strip", "event-santa-pop-strip"]),
 ("Events: pigeons, balloons, fireworks, icefall", ["event-santa-pigeon-strip", "event-santa-parade-balloon-strip", "event-santa-firework-strip", "event-santa-icefall-strip"]),
 ("Events: aurora storm wisps", ["event-santa-aurora-wisp-a-strip", "event-santa-aurora-wisp-b-strip", "event-santa-aurora-wisp-c-strip"]),
 ("Ground sweeps: camel caravan, bullet train", ["event-santa-camel-caravan-strip", "event-santa-bullet-train-strip"]),
 ("2  Golden Santa C (idle 0-3 + boost 0-3)", ["santa-c-golden-strip"]),
 ("4  Sleigh hop + hop sparkle", ["cut-santa-sleigh-strip", "cut-santa-hop-sparkle-strip"]),
 ("Swoosh", ["ui-santa-swoosh-strip"]),
 ("5  Rush aura, heart overlay, frost/heart/bauble bursts", ["fx-santa-rush-aura-strip", "santa-heart-overlay-strip", "fx-santa-frost-burst-strip"]),
 ("", ["fx-santa-heart-pop-strip", "fx-santa-heart-break-strip"]),
 ("", ["fx-santa-bauble-burst-strip", "fx-santa-frost-flake-a", "fx-santa-frost-flake-b", "fx-santa-frost-flake-c"]),
 ("6/7/8  2x HUD, badge 9, confetti", ["ui-hud-santa-rush-48", "ui-hud-santa-life-48", "ui-hud-santa-chill-48", "ui-santa-badge-9", "event-santa-confetti-strip"]),
 ("", ["fx-santa-confetti-burst-strip"])]
W = 1500; f = ImageFont.truetype(FONT, 22); ims = []
for t, names in rows:
    items = [Image.open(os.path.join(P2, n + ".png")) for n in names]
    items = [i if i.width <= 1300 else Image.open(os.path.join(P2.replace("2x","1x"), n + ".png")) for i, n in zip(items, names)]
    h = max(i.height for i in items) + (36 if t else 10)
    ims.append((t, items, h))
sc = Image.open(os.path.join(R, "packs/santa/assets/ui-santa-scorecard-frame.png")).convert("RGBA")
vg = Image.open(os.path.join(P2, "ui-santa-frost-vignette.png")).resize((300, 533))
H = sum(h for *_, h in ims) + 40
out = Image.new("RGBA", (W + 640, max(H, 1400)), "#2B2645"); d = ImageDraw.Draw(out); y = 20
for t, items, h in ims:
    if t: d.text((20, y), t, font=f, fill="#FFF4D6"); yy = y + 32
    else: yy = y + 4
    x = 20
    for i in items:
        if x + i.width > W: i = i.resize((W - x - 10, int(i.height * (W - x - 10) / i.width)))
        d.rectangle([x - 2, yy - 2, x + i.width + 1, yy + i.height + 1], fill="#3B3560"); out.alpha_composite(i, (x, yy)); x += i.width + 24
    y += h + 8
d.text((W + 20, 20), "3  Scorecard frame 600x800 (+@2x)", font=f, fill="#FFF4D6"); out.alpha_composite(sc, (W + 20, 56))
d.text((W + 20, 870), "Frost vignette 360x640", font=f, fill="#FFF4D6"); bgv = Image.new("RGBA", vg.size, "#3E5E8A"); bgv.alpha_composite(vg); out.alpha_composite(bgv, (W + 20, 900))
p = os.path.join(T, "../previews/santa-v080-preview.png"); os.makedirs(os.path.dirname(p), exist_ok=True)
out.convert("RGB").quantize(256).save(p, optimize=True); print(p, os.path.getsize(p))
