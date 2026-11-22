"""preview-sheet-void.png (<=1.5MB): void columns (art + hitboxes), backgrounds, space->void transition, UI."""
import os, json
from PIL import Image, ImageDraw, ImageFont
A = os.path.join(os.path.dirname(__file__), ".."); P = lambda n, d="1x": Image.open(os.path.join(A, "png", d, n + ".png")).convert("RGBA")
H = json.load(open(os.path.join(A, "hitboxes.json")))
F = ImageFont.truetype("/usr/share/fonts/truetype/sand-box/google/Capriola/Capriola-Regular.ttf", 14)
OBJ = ["typewriter", "crt", "phone", "cassette", "gramophone", "alarm"]
K = 2  # draw columns at 2x
def column(n, side, hb=False, tiles=3):
    base = f"obs-void-{n}-{side}"
    body = P(base + "-body", "2x"); cap = P(base + ("-cap-bottom" if side == "top" else "-cap-top"), "2x")
    h = body.height * tiles + cap.height; im = Image.new("RGBA", (160, h), (0, 0, 0, 0))
    if side == "top":
        for i in range(tiles): im.alpha_composite(body, (0, i * 128))
        im.alpha_composite(cap, (0, tiles * 128)); offs = [(base + "-body", i * 128) for i in range(tiles)] + [(base + "-cap-bottom", tiles * 128)]
    else:
        im.alpha_composite(cap, (0, 0))
        for i in range(tiles): im.alpha_composite(body, (0, 160 + i * 128))
        offs = [(base + "-cap-top", 0)] + [(base + "-body", 160 + i * 128) for i in range(tiles)]
    if hb:
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        for key, oy in offs:
            for x, y, w, hh in H[key].get("rects", []): d.rectangle([x*K, oy + y*K, (x+w)*K - 1, oy + (y+hh)*K - 1], fill=(255, 60, 120, 70), outline=(255, 60, 120, 200))
            for cx, cy, r in H[key].get("circles", []): d.ellipse([(cx-r)*K, oy + (cy-r)*K, (cx+r)*K, oy + (cy+r)*K], fill=(60, 200, 255, 70), outline=(60, 200, 255, 220))
        im.alpha_composite(ov)
    return im
W = 2000; sheet = Image.new("RGBA", (W, 3000), "#282142"); d = ImageDraw.Draw(sheet)
y = 20; d.text((20, y), "Stage 7 'void' (The Void, Nebula Drift): tops = ribbon body + cap-bottom; bottoms = cap-top + cloud body. Drawn at 2x; pink = rects, blue = circles", font=F, fill="#FFF4D6"); y += 30
x = 20
for n in OBJ:
    for hb in (False, True):
        t = column(n, "top", hb, 2); sheet.alpha_composite(t, (x, y)); 
        b = column(n, "bottom", hb, 2); sheet.alpha_composite(b, (x, y + t.height + 40))
        x += 165
    d.text((x - 330, y + t.height + 12), n, font=F, fill="#FFF4D6")
y += 2 * (160 + 256) + 60
# gameplay mock: void bg + a pair
bgw = Image.new("RGBA", (720, 640))
for L in ("far", "mid", "near"): bgw.alpha_composite(P(f"bg-void-{L}"))
d.text((20, y), "bg-void far+mid+near (720x640, two tiles side by side)", font=F, fill="#FFF4D6"); y += 22
sheet.alpha_composite(bgw, (20, y)); sheet.alpha_composite(bgw, (740, y))
# mock pair over first tile
g = P("ghost-normal-idle-0"); 
def col1x(n, side, top_y, h):
    base = f"obs-void-{n}-{side}"; body = P(base + "-body"); cap = P(base + ("-cap-bottom" if side == "top" else "-cap-top"))
    im = Image.new("RGBA", (80, h))
    if side == "top":
        yy = h - 80; im.alpha_composite(cap, (0, yy)); yy -= 64
        while yy > -64: im.alpha_composite(body, (0, yy)); yy -= 64
    else:
        im.alpha_composite(cap, (0, 0)); yy = 80
        while yy < h: im.alpha_composite(body, (0, yy)); yy += 64
    return im
for cx, nt, nb, gy in ((200, "alarm", "typewriter", 250), (480, "crt", "gramophone", 300)):
    sheet.alpha_composite(col1x(nt, "top", 0, gy), (20 + cx - 40, y)); sheet.alpha_composite(col1x(nb, "bottom", 0, 640 - gy - 160), (20 + cx - 40, y + gy + 160))
sheet.alpha_composite(g, (20 + 90, y + 300))
y += 660
d.text((20, y), "Space to Void: bg-space | bg-trans-space-void | bg-void (composited, 0.5x)", font=F, fill="#FFF4D6"); y += 22
for i, nm in enumerate(("space", "trans-space-void", "void")):
    t = Image.new("RGBA", (720, 640))
    for L in ("far", "mid", "near"): t.alpha_composite(P(f"bg-{nm}-{L}"))
    sheet.alpha_composite(t.resize((360, 320)), (20 + i * 360, y))
for i in range(3): d.line([(20 + i * 360, y), (20 + i * 360, y + 320)], fill="#FFFFFF", width=1)
# mist overlay frames over space+void
d.text((1120, y - 22), "bg-trans-space-void-mist-0..7 (360x640 overlay, 8f @8fps) over the scene, 0.4x", font=F, fill="#FFF4D6")
sp = Image.new("RGBA", (360, 640))
for L in ("far", "mid", "near"): sp.alpha_composite(P(f"bg-space-{L}").crop((0, 0, 360, 640)))
vd = Image.new("RGBA", (360, 640))
for L in ("far", "mid", "near"): vd.alpha_composite(P(f"bg-void-{L}").crop((0, 0, 360, 640)))
for i in range(8):
    base = (sp if i < 4 else vd).copy(); base.alpha_composite(P(f"bg-trans-space-void-mist-{i}"))
    sheet.alpha_composite(base.resize((144, 256)), (1120 + (i % 4) * 150, y + (i // 4) * 262))
y += 540
d.text((20, y), "ui-banner-void, ui-banner-void-blank, ui-stage-badge-7, fx-burst-void-0..5", font=F, fill="#FFF4D6"); y += 22
sheet.alpha_composite(P("ui-banner-void", "2x"), (20, y)); sheet.alpha_composite(P("ui-banner-void-blank", "2x"), (640, y)); sheet.alpha_composite(P("ui-stage-badge-7", "2x"), (1260, y))
y += 190; sheet.alpha_composite(P("fx-burst-void-strip"), (20, y)); y += 170
sheet = sheet.crop((0, 0, W, y + 10)).convert("RGB")
out = os.path.join(A, "preview-sheet-void.png")
sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(out, optimize=True)
print(out, os.path.getsize(out), sheet.size)
