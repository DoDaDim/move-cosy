"""preview-sheet-void-v2.png (<=1.5MB): void floaters, invaders (with hit circles), pop, warning, wave mock-up."""
import os, json
from PIL import Image, ImageDraw, ImageFont
A = os.path.join(os.path.dirname(__file__), ".."); P = lambda n, d="2x": Image.open(os.path.join(A, "png", d, n + ".png")).convert("RGBA")
H = json.load(open(os.path.join(A, "hitboxes.json")))
F = ImageFont.truetype("/usr/share/fonts/truetype/sand-box/google/Capriola/Capriola-Regular.ttf", 15)
sheet = Image.new("RGBA", (1500, 1900), "#2C2356"); d = ImageDraw.Draw(sheet)
def big(im, k=2): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def circ(x, y, cx, cy, r, k):
    d.ellipse([x + (cx - r) * k, y + (cy - r) * k, x + (cx + r) * k, y + (cy + r) * k], outline=(60, 220, 255, 255), width=2)
y = 20; d.text((20, y), "Void floaters (40x40, 4-frame wobble @6fps) shown 4x; blue = hit circle", font=F, fill="#FFF4D6"); y += 28
for row, (cid, h) in enumerate([(k, v) for k, v in H["hazards"].items() if k.startswith("void-float")]):
    n = h["art"]; d.text((20, y + 70), f"{cid}\n{n}  r{h['r']}", font=F, fill="#FFF4D6")
    for i in range(4):
        x = 190 + i * 180; sheet.alpha_composite(big(P(f"obs-void-float-{n}-{i}")), (x, y)); circ(x, y, h["cx"], h["cy"], h["r"], 4)
    y += 175
d.text((20, y), "Invaders a / b / c (40x40, 2-frame march @4fps) 4x; r14", font=F, fill="#FFF4D6"); y += 28
for j, base in enumerate(["event-void-invader", "event-void-invader-b", "event-void-invader-c"]):
    for f in (0, 1):
        x = 20 + (j * 2 + f) * 175; sheet.alpha_composite(big(P(f"{base}-{f}")), (x, y)); circ(x, y, 20, 20, 14, 4)
y += 180
d.text((20, y), "event-void-invader-pop-0..5 (64x64 @12fps) 2x  |  ui-event-warning-void-0/1 (40x40 @4fps) 2x", font=F, fill="#FFF4D6"); y += 26
for i in range(6): sheet.alpha_composite(P(f"event-void-invader-pop-{i}"), (20 + i * 140, y))
for f in (0, 1): sheet.alpha_composite(big(P(f"ui-event-warning-void-{f}"), 1), (900 + f * 110, y + 20))
y += 150
d.text((20, y), "Wave mock-up on bg-void (1x, 360x640 window): 2 formations, each with one clear 176 px lane (Code's spacing 44)", font=F, fill="#FFF4D6"); y += 26
for k, lane in enumerate((260, 360)):
    scene = Image.new("RGBA", (360, 640))
    for L in ("far", "mid", "near"): scene.alpha_composite(P(f"bg-void-{L}", "1x").crop((k * 200, 0, k * 200 + 360, 640)))
    inv = [P(b, "1x") for b in ("event-void-invader-0", "event-void-invader-b-1", "event-void-invader-c-0")]
    yc = 14; i = 0
    while yc < 560 + 14:
        if abs(yc - lane) >= 176 / 2 + 14 + 3:
            scene.alpha_composite(inv[i % 3], (200 - 20, yc - 20)); scene.alpha_composite(inv[(i + 1) % 3], (250 - 20, yc - 20 + 6))
        yc += 44; i += 1
    scene.alpha_composite(P("ghost-normal-idle-0", "1x"), (70, lane - 32))
    sheet.alpha_composite(scene, (20 + k * 380, y))
sheet.alpha_composite(big(P("ui-event-warning-void-0", "1x"), 3), (820, y + 20)); d.text((820, y + 150), "warning icon 3x", font=F, fill="#FFF4D6")
y += 660
sheet = sheet.crop((0, 0, 1500, y)).convert("RGB")
out = os.path.join(A, "preview-sheet-void-v2.png")
sheet.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(out, optimize=True)
print(out, os.path.getsize(out), sheet.size)
