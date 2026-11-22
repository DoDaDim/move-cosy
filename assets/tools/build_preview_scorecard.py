"""preview-sheet-v05-scorecard.png: all 7 frames with example text drawn into the safe areas (+ faint rect outlines)."""
import os, json
from PIL import Image, ImageDraw, ImageFont
A = os.path.join(os.path.dirname(__file__), "..")
L = json.load(open(os.path.join(A, "scorecard-layout.json")))["areas"]
FONT = next(p for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if os.path.exists(p))
names = ["", "graveyard", "church", "countryside", "schools", "city", "space"]
EX = {"stage": "{st}", "score": "128", "best": "BEST 214", "player": "David", "url": "ghostgame.example/play"}
S = 0.5; cw, ch = int(600*S), int(800*S); pad = 16
sheet = Image.new("RGBA", (pad + 4*(cw+pad), pad + 2*(ch+pad+20)), "#282142")
gh = Image.open(os.path.join(A, "png/2x/ghost-normal-idle-0.png")).convert("RGBA").resize((192, 192), Image.LANCZOS)
for i, st in enumerate(names):
    n = "ui-scorecard-frame" + (f"-{st}" if st else "")
    im = Image.open(os.path.join(A, "png/1x", n + ".png")).convert("RGBA")
    d = ImageDraw.Draw(im)
    x, y, w, h = L["ghost"]["rect"]; im.alpha_composite(gh, (x + 4, y + 4))
    for k, a in L.items():
        x, y, w, h = a["rect"]; d.rectangle([x, y, x+w, y+h], outline=(255, 0, 120, 110))
        if k == "ghost": continue
        t = EX[k].format(st=(st or "graveyard").upper()); f = a["maxFont"]
        while True:
            font = ImageFont.truetype(FONT, f)
            if d.textlength(t, font=font) <= w - 8 or f < 8: break
            f -= 2
        if k == "score": d.text((x + w/2, y + h/2), t, font=font, fill="white", anchor="mm", stroke_width=4, stroke_fill="white")
        d.text((x + w/2, y + h/2), t, font=font, fill=a["color"], anchor="mm")
    im = im.resize((cw, ch), Image.LANCZOS)
    cx, cy = pad + (i % 4)*(cw+pad), pad + (i // 4)*(ch+pad+20)
    sheet.alpha_composite(im, (cx, cy))
    ImageDraw.Draw(sheet).text((cx, cy + ch + 3), n, fill="#FFF4D6")
for j, sz in enumerate((32, 48)):
    ic = Image.open(os.path.join(A, "png/2x", f"ui-icon-share-{sz}.png")).convert("RGBA")
    sheet.alpha_composite(ic, (pad + 3*(cw+pad) + 20 + j*120, pad + ch + pad + 20 + 60))
ImageDraw.Draw(sheet).text((pad + 3*(cw+pad) + 20, pad + ch + pad + 20 + 30), "ui-icon-share-32 / -48 (@2x)", fill="#FFF4D6")
sheet.convert("RGB").save(os.path.join(A, "preview-sheet-v05-scorecard.png"))
