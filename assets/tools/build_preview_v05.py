"""preview-sheet-v05.png: every death strip (normal + golden), FX, transitions, icons."""
import os, io, cairosvg
from PIL import Image, ImageDraw, ImageFont
A = os.path.join(os.path.dirname(__file__), ".."); BG = (46, 38, 74)
try: F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16); FS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except Exception: F = FS = ImageFont.load_default()
def im(n, s=1): return Image.open(io.BytesIO(cairosvg.svg2png(url=os.path.join(A, n + ".svg"), scale=s))).convert("RGBA")
def frames(p):
    out = []; i = 0
    while os.path.exists(os.path.join(A, f"{p}-{i}.svg")): out.append(f"{p}-{i}"); i += 1
    return out
rows = []
for t in ("bat", "pumpkin", "meteor", "tombstone", "skull", "floor", "generic"):
    rows.append((f"death-{t}  ({len(frames('death-'+t))}f @12fps)", [im(n) for n in frames("death-" + t)]))
    rows.append((f"death-{t}-golden", [im(n) for n in frames(f"death-{t}-golden")]))
rows.append(("fx-stars-ring / smoke-puff / sparkle-poof / bonk", [im(n, 1.5) for p in ("fx-stars-ring", "fx-smoke-puff") for n in frames(p)] + [im(n) for p in ("fx-sparkle-poof", "fx-bonk") for n in frames(p)]))
rows.append(("ui-banner-blank + stage banners", [im("ui-banner-blank")] + [im(f"ui-banner-{s}") for s in ("graveyard", "church", "countryside")]))
rows.append(("", [im(f"ui-banner-{s}") for s in ("schools", "city", "space")] + [im("ui-banner-space-blank")]))
rows.append(("fx-swoosh-0..5", [im(n) for n in frames("fx-swoosh")]))
for s in ("graveyard", "church", "countryside", "schools", "city", "space"):
    rows.append((f"fx-burst-{s}-0..5", [im(n) for n in frames(f"fx-burst-{s}")]))
rows.append(("ui-stage-badge-blank, -1..6", [im("ui-stage-badge-blank")] + [im(f"ui-stage-badge-{n}") for n in range(1, 7)]))
rows.append(("ui-icon-* 48 / 32 (shown 2x)", [im(f"ui-icon-{n}-{z}", 2) for z in (48, 32) for n in ("add-player", "trophy", "player-chip-pink", "player-chip-mint", "player-chip-butter", "player-chip-lilac")]))
W = 40 + max(sum(i.width + 10 for i in r) for _, r in rows)
H = 60 + sum(max(i.height for i in r) + 34 for _, r in rows)
sheet = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(sheet)
d.text((20, 18), "Halloween Ghost v0.5 - deaths, FX, transitions, profile icons (1x; 128x128 death canvas, + = game anchor 64,64)", font=F, fill=(255, 230, 240))
y = 56
for title, r in rows:
    d.text((20, y), title, font=FS, fill=(220, 205, 245)); y += 18; x = 20
    for i in r:
        d.rectangle([x, y, x + i.width - 1, y + i.height - 1], fill=(58, 48, 92))
        sheet.alpha_composite(i, (x, y))
        if i.size == (128, 128): d.line([x + 60, y + 64, x + 68, y + 64], fill=(255, 120, 160)); d.line([x + 64, y + 60, x + 64, y + 68], fill=(255, 120, 160))
        x += i.width + 10
    y += max(i.height for i in r) + 16
sheet.convert("RGB").save(os.path.join(A, "preview-sheet-v05.png")); print(sheet.size)
