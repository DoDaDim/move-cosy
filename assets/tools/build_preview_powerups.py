"""preview-sheet-v05-powerups.png (<=1.5MB): all power-up strips at 2x on night sky."""
import os
from PIL import Image, ImageDraw
A = os.path.join(os.path.dirname(__file__), ".."); P = lambda n: os.path.join(A, "png/2x", n + ".png")
rows = [["pickup-rush-strip", "pickup-life-strip", "pickup-chill-strip"], ["ghost-rush-strip"], ["fx-rush-aura-strip", "fx-rush-trail-strip"],
        ["fx-candy-burst-strip"], ["ghost-heart-overlay-strip", "fx-heart-pop-strip"], ["fx-heart-break-strip"], ["fx-frost-burst-strip", "fx-frost-flake-a", "fx-frost-flake-b", "fx-frost-flake-c"],
        ["ui-hud-rush-48", "ui-hud-life-48", "ui-hud-chill-48", "ui-hud-rush-32", "ui-hud-life-32", "ui-hud-chill-32"]]
W = 1700; y = 20; placed = []
for r in rows:
    x = 20; h = 0
    for n in r:
        im = Image.open(P(n)).convert("RGBA"); placed.append((n, im, x, y + 16)); x += im.width + 30; h = max(h, im.height)
    y += h + 40
# demo: ghost with heart overlay and aura, vignette thumbnail
gh = Image.open(P("ghost-normal-idle-0")).convert("RGBA"); ht = Image.open(P("ghost-heart-overlay-0")).convert("RGBA")
au = Image.open(P("fx-rush-aura-0")).convert("RGBA"); gg = Image.open(P("ghost-golden-idle-0")).convert("RGBA")
vg = Image.open(P("ui-frost-vignette")).convert("RGBA").resize((360, 640))
Ht = max(y, 700); sheet = Image.new("RGBA", (W + 420, Ht), "#282142"); d = ImageDraw.Draw(sheet)
for n, im, x, yy in placed: sheet.alpha_composite(im, (x, yy)); d.text((x, yy - 14), n, fill="#FFF4D6")
bx = W + 30; tint = Image.new("RGBA", (360, 640), (191, 230, 255, 46)); bg = Image.new("RGBA", (360, 640), "#4E3E6E")
bg.alpha_composite(tint); bg.alpha_composite(vg); sheet.alpha_composite(bg, (bx, 40)); d.text((bx, 22), "ui-frost-vignette + tint #BFE6FF a=0.18 (1x)", fill="#FFF4D6")
demo_y = 40 + 640 + 30 if Ht > 760 else None
if demo_y:
    sheet.alpha_composite(au, (bx, demo_y)); sheet.alpha_composite(gg, (bx + 32, demo_y + 32))
    sheet.alpha_composite(gh, (bx + 220, demo_y + 32)); sheet.alpha_composite(ht, (bx + 220 + 80, demo_y + 32 + 4))
    d.text((bx, demo_y - 14), "demo: aura on golden ghost / heart overlay at (+40,+2)", fill="#FFF4D6")
sheet.convert("RGB").save(os.path.join(A, "preview-sheet-v05-powerups.png"), optimize=True)
