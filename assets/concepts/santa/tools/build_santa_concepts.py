"""Santa's Rocket Run (December skin) - first-step concepts only, NOT wired into the game.
Writes ../santa-hero-options.png (3 hero options, idle + boost, 64px + 3x) and ../santa-mock-london.png (360x640 mock frame).
Same kawaii chibi language as the ghost (assets/tools/build_ghosts.py): #6B4E7A outline, gradient eyes with
double highlights, blush with tick marks, 'w' / 'o' mouth. Run: python3 build_santa_concepts.py"""
import os, io, math, random, cairosvg
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
L = "#6B4E7A"                                     # ghost line colour
EYE, EYE2, BLUSH, MOUTH = "#4A3358", "#7A5A9E", "#FFB3CB", "#E87FA3"
RED, RED2, RED_D = "#F26D7D", "#E04F66", "#C23B57"  # soft kawaii Santa red (hi / base / shade)
FUR, FUR2 = "#FFFFFF", "#E6DDF7"                  # ghost body whites
SKIN, SKIN2 = "#FFE6D8", "#F8CDBE"
GOLD, GOLD2 = "#FFD873", "#F6C766"                # golden-ghost gold
MINT, MINT2 = "#AEE3C6", "#7FCBA6"
SACK, SACK2 = "#E3B98A", "#C99A6B"
BOOT = "#4A3358"
FONT = "/usr/share/fonts/truetype/sand-box/google/Capriola/Capriola-Regular.ttf"

def svg(w, h, inner, vb=None):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb or f"0 0 {w} {h}"}">{inner}</svg>'
def png(s, w=None, h=None): return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(), output_width=w, output_height=h))).convert("RGBA")
def st(w=2.0): return f'stroke="{L}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
DEFS = (f'<defs><linearGradient id="e" x1="0" y1="0" x2="0" y2="1"><stop offset="0.35" stop-color="{EYE}"/><stop offset="1" stop-color="{EYE2}"/></linearGradient>'
        f'<radialGradient id="red" cx="0.35" cy="0.3" r="0.85"><stop offset="0" stop-color="{RED}"/><stop offset="0.6" stop-color="{RED2}"/><stop offset="1" stop-color="{RED_D}"/></radialGradient>'
        f'<radialGradient id="skin" cx="0.4" cy="0.35" r="0.8"><stop offset="0" stop-color="#FFF3EA"/><stop offset="1" stop-color="{SKIN}"/></radialGradient>'
        f'<radialGradient id="gold" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="#FFF4C9"/><stop offset="0.5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD2}"/></radialGradient>'
        f'<radialGradient id="glow"><stop offset="0.3" stop-color="#FFE7A0" stop-opacity="0.6"/><stop offset="1" stop-color="#FFE7A0" stop-opacity="0"/></radialGradient></defs>')

def face(cx, cy, k=1.0, eyes="open", mouth="w"):
    """the ghost's face, centred at (cx, cy) (ghost face centre = (32, 31) in its 64 box)"""
    g = [f'<g transform="translate({cx},{cy}) scale({k})">']
    for x in (-13.2, 13.2):
        g.append(f'<ellipse cx="{x}" cy="4.2" rx="3.6" ry="2.1" fill="{BLUSH}" opacity="0.85"/>')
    g.append(f'<g stroke="#FFFFFF" stroke-width="0.7" stroke-linecap="round" opacity="0.8"><path d="M-15.2,3.6 l0.9,-1.2 M-13.4,3.8 l0.9,-1.2"/><path d="M11.2,3.6 l0.9,-1.2 M13,3.8 l0.9,-1.2"/></g>')
    for x in (-7.8, 7.8):
        if eyes == "open":
            g.append(f'<ellipse cx="{x}" cy="-2.4" rx="4.3" ry="5.3" fill="url(#e)"/><ellipse cx="{x-1.3}" cy="-4.4" rx="1.8" ry="2.1" fill="#FFF"/>'
                     f'<circle cx="{x+1.6}" cy="0" r="0.95" fill="#FFF"/><circle cx="{x+2.2}" cy="-3.8" r="0.5" fill="#FFF" opacity="0.8"/>')
        else:  # happy closed
            g.append(f'<path d="M{x-4},-1.8 Q{x},-6 {x+4},-1.8" fill="none" stroke="{EYE}" stroke-width="2" stroke-linecap="round"/>')
    if mouth == "w":
        g.append(f'<path d="M-2.6,3.4 Q-1.3,5.4 0,3.6 Q1.3,5.4 2.6,3.4" fill="none" stroke="{L}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        g.append(f'<ellipse cx="0" cy="4.4" rx="1.9" ry="2.2" fill="{MOUTH}" stroke="{L}" stroke-width="1.2"/><ellipse cx="0" cy="5.4" rx="1" ry="0.7" fill="#FFC4D4"/>')
    return "".join(g) + "</g>"
def flame(x, y, ang, Ln=14, w=7, big=False):
    """flame puff from nozzle (x, y) pointing along ang (deg, 0 = +x, 90 = down) + two smoke puffs"""
    if big: Ln, w = Ln * 1.5, w * 1.25
    def tear(l, ww, col, op=1):
        return (f'<path d="M0,{-ww/2:.1f} C{l*0.45:.1f},{-ww/2:.1f} {l*0.8:.1f},{-ww*0.2:.1f} {l:.1f},0 C{l*0.8:.1f},{ww*0.2:.1f} {l*0.45:.1f},{ww/2:.1f} 0,{ww/2:.1f} '
                f'C{-ww*0.35:.1f},{ww/2:.1f} {-ww*0.35:.1f},{-ww/2:.1f} 0,{-ww/2:.1f} Z" fill="{col}" opacity="{op}"/>')
    g = f'<g transform="translate({x},{y}) rotate({ang})">'
    a = math.radians(0)
    g += (f'<circle cx="{Ln*1.15:.1f}" cy="{w*0.2:.1f}" r="{w*0.42:.1f}" fill="#F3EEFC" stroke="{L}" stroke-width="1" opacity="0.85"/>'
          f'<circle cx="{Ln*1.45:.1f}" cy="{-w*0.25:.1f}" r="{w*0.3:.1f}" fill="#F3EEFC" stroke="{L}" stroke-width="0.9" opacity="0.7"/>')
    g += tear(Ln, w, "#FFB36B") + tear(Ln * 0.7, w * 0.66, "#FFE08A") + tear(Ln * 0.38, w * 0.36, "#FFFFFF", 0.95)
    g += f'<path d="M0,{-w/2:.1f} C{Ln*0.45:.1f},{-w/2:.1f} {Ln*0.8:.1f},{-w*0.2:.1f} {Ln:.1f},0 C{Ln*0.8:.1f},{w*0.2:.1f} {Ln*0.45:.1f},{w/2:.1f} 0,{w/2:.1f}" fill="none" stroke="#E8875A" stroke-width="1" opacity="0.8"/>'
    return g + "</g>"
def pompom(x, y, r=3.6): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{FUR}" {st(1.6)}/><circle cx="{x-1}" cy="{y-1.2}" r="{r*0.35:.1f}" fill="#FFF" opacity="0.9"/>'
def sack(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})"><path d="M-7,-6 Q-11,6 -6,9 Q0,11 6,9 Q11,6 7,-6 Q0,-9 -7,-6 Z" fill="{SACK}" {st(1.6)}/>'
            f'<path d="M-4,-7 Q0,-4 4,-7" fill="none" stroke="#B5455C" stroke-width="1.8" stroke-linecap="round"/><path d="M-3,-8 Q0,-13 3,-8" fill="{SACK2}" {st(1.4)}/>'
            f'<path d="M-4,2 Q0,5 4,2" fill="none" stroke="{SACK2}" stroke-width="1" stroke-linecap="round"/>'
            f'<rect x="-1.5" y="-1" width="5" height="4" rx="0.8" fill="{MINT}" stroke="{L}" stroke-width="0.9" transform="rotate(-10)"/></g>')
def mitten(x, y, rot=0): return f'<g transform="translate({x},{y}) rotate({rot})"><ellipse cx="0" cy="0" rx="4.4" ry="3.6" fill="url(#red)" {st(1.6)}/><ellipse cx="-3.6" cy="0" rx="1.6" ry="2.6" fill="{FUR}" {st(1.2)}/></g>'
def beard(cx, cy, k=1.0):
    pts = [(-9, 0, 4.6), (-5, 3.6, 4.8), (0, 5.2, 5), (5, 3.6, 4.8), (9, 0, 4.6)]
    return "".join(f'<circle cx="{cx+dx*k:.1f}" cy="{cy+dy*k:.1f}" r="{r*k:.1f}" fill="{FUR}" {st(1.5)}/>' for dx, dy, r in pts) + \
           "".join(f'<circle cx="{cx+dx*k:.1f}" cy="{cy+dy*k:.1f}" r="{(r-1.2)*k:.1f}" fill="{FUR}"/>' for dx, dy, r in pts)

# ---------------- A: round mini Santa + twin-rocket pack ----------------
def rocket(x, y, rot, s=1.0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M-3,6 L-6,10 L-3,9 Z M3,6 L6,10 L3,9 Z" fill="{RED2}" {st(1.2)}/>'
            f'<path d="M-3.6,7 V-5 Q-3.6,-11 0,-13 Q3.6,-11 3.6,-5 V7 Z" fill="#F3EEFC" {st(1.5)}/>'
            f'<path d="M-3.4,-6 Q0,-8 3.4,-6 L3.6,-3 Q0,-5 -3.6,-3 Z" fill="{RED2}"/><circle cx="0" cy="0.5" r="1.6" fill="#BFE6FF" {st(1)}/>'
            f'<rect x="-2.6" y="7" width="5.2" height="2.4" rx="0.6" fill="{GOLD2}" {st(1.1)}/></g>')
def hero_a(boost=False):
    tilt = -10 if boost else 0; dy = -1 if boost else 0
    g = [f'<g transform="translate(0,{dy}) rotate({tilt} 32 36)">']
    # rocket pack: two rockets behind the back (thrust down-left)
    for (x, y) in ((15, 30), (20, 36)):
        g.append(flame(x - 4.6, y + 8.4, 120, 10, 5.6, boost))
    g.append(rocket(15, 30, 30, 0.95) + rocket(20, 36, 30, 0.95))
    g.append(sack(14, 50, 0.85, -14))
    g.append(f'<ellipse cx="34" cy="46" rx="14" ry="12.5" fill="url(#red)" {st(2.2)}/>')   # round body
    g.append(f'<path d="M21,48 Q34,53 47,48" fill="none" stroke="{BOOT}" stroke-width="3.4" stroke-linecap="round"/><rect x="31.5" y="47.6" width="5" height="4" rx="1" fill="{GOLD}" {st(1)}/>')
    g.append(f'<ellipse cx="29" cy="58" rx="3.6" ry="2.4" fill="{BOOT}"/><ellipse cx="39" cy="58" rx="3.6" ry="2.4" fill="{BOOT}"/>')
    g.append(f'<circle cx="34" cy="30" r="13.5" fill="url(#skin)" {st(2.2)}/>')            # head
    g.append(beard(34, 37, 1.0))
    g.append(face(34, 28, 0.82, "open", "o" if boost else "w"))
    # hat: floppy cone back-left, fur band, pompom
    g.append(f'<path d="M21,22 Q22,9 33,7 Q42,6 46,17 Q40,12 33,12 Q26,13 23,18 Q16,14 10,17 Q13,10 21,9 Q16,13 21,22 Z" fill="none"/>')
    g.append(f'<path d="M21.5,21 Q21,8 34,6.5 Q44,6.5 47,19 Z" fill="url(#red)" {st(2)}/>'
             f'<path d="M24,9 Q16,7 10,13" fill="none" stroke="{RED2}" stroke-width="5" stroke-linecap="round"/><path d="M24,9 Q16,7 10,13" fill="none" {st(1.6)} opacity="0"/>')
    g.append(f'<path d="M25,8.6 Q17,6 10.4,12.4" fill="none" stroke="{L}" stroke-width="7.6" stroke-linecap="round"/><path d="M25,8.6 Q17,6 10.4,12.4" fill="none" stroke="{RED2}" stroke-width="4.4" stroke-linecap="round"/>')
    g.append(pompom(9.6, 13.4, 3.6))
    g.append(f'<rect x="19.5" y="17" width="29" height="7" rx="3.5" fill="{FUR}" {st(1.8)}/>')
    g.append(mitten(48, 37 if boost else 46, -40 if boost else 10))
    g.append("</g>")
    return "".join(g)

# ---------------- B: Santa riding a candy-cane rocket ----------------
def hero_b(boost=False):
    tilt = -9 if boost else 0
    g = [f'<g transform="rotate({tilt} 32 40)">']
    g.append(flame(7, 48, 180, 10, 7, boost))
    # cane crook at the tail (handle + sack hook)
    g.append(f'<path d="M12,47 Q4,47 4,38 Q4,30 11,30 Q16,30 16,35" fill="none" stroke="{L}" stroke-width="7.4" stroke-linecap="round"/>'
             f'<path d="M12,47 Q4,47 4,38 Q4,30 11,30 Q16,30 16,35" fill="none" stroke="#FFFFFF" stroke-width="4.4" stroke-linecap="round"/>'
             f'<path d="M12,47 Q4,47 4,38 Q4,30 11,30 Q16,30 16,35" fill="none" stroke="{RED2}" stroke-width="4.4" stroke-dasharray="3 3"/>')
    g.append(f'<path d="M15.5,36 L15,40" stroke="{L}" stroke-width="1.2"/>' + sack(15, 45, 0.7, 8))
    # rocket body: striped tube with nose cone + fins
    body = "M10,42.5 H50 Q60,42.5 62,48 Q60,53.5 50,53.5 H10 Q8,48 10,42.5 Z"
    g.append(f'<clipPath id="cane"><path d="{body}"/></clipPath><path d="{body}" fill="#FFFFFF"/>'
             f'<g clip-path="url(#cane)">' + "".join(f'<path d="M{x},56 L{x+6},40 L{x+10},40 L{x+4},56 Z" fill="{RED2}"/>' for x in range(4, 64, 9)) + '</g>'
             f'<path d="{body}" fill="none" {st(2)}/><path d="M14,45 H46" stroke="#FFF" stroke-width="1.4" opacity="0.7" stroke-linecap="round"/>')
    g.append(f'<path d="M14,53 L9,59 L18,57 Z" fill="{MINT}" {st(1.4)}/><path d="M14,43 L10,38 L19,41 Z" fill="{MINT}" {st(1.4)}/>')
    g.append(f'<circle cx="52" cy="48" r="2.6" fill="#BFE6FF" {st(1.2)}/>')
    # Santa astride (small chibi)
    g.append(f'<path d="M26,44 Q26,32 34,31 Q42,32 42,44 Z" fill="url(#red)" {st(2)}/>')
    g.append(f'<ellipse cx="36" cy="55" rx="3.6" ry="2.3" fill="{BOOT}"/><path d="M33,52 Q34,55 36,55" stroke="{RED_D}" stroke-width="3" fill="none"/>')
    g.append(f'<path d="M26.5,43 Q34,46 41.5,43" fill="none" stroke="{BOOT}" stroke-width="2.8" stroke-linecap="round"/>')
    g.append(f'<circle cx="34" cy="22" r="11" fill="url(#skin)" {st(2)}/>' + beard(34, 28, 0.8))
    g.append(face(34, 20.5, 0.66, "open", "o" if boost else "w"))
    g.append(f'<path d="M23.4,15 Q24,4 34,3.5 Q43,4 45,15 Z" fill="url(#red)" {st(1.8)}/>'
             f'<path d="M26,6 Q19,3 15,{9 if boost else 11}" fill="none" stroke="{L}" stroke-width="6.6" stroke-linecap="round"/><path d="M26,6 Q19,3 15,{9 if boost else 11}" fill="none" stroke="{RED2}" stroke-width="3.8" stroke-linecap="round"/>'
             + pompom(14.4, 9.6 if boost else 11.6, 3) + f'<rect x="22" y="12.6" width="24" height="5.8" rx="2.9" fill="{FUR}" {st(1.6)}/>')
    g.append(mitten(45, 36 if boost else 41, -50 if boost else 0))
    g.append("</g>")
    return "".join(g)

# ---------------- C: hooded chibi Santa + gift-box jetpack ----------------
def hero_c(boost=False):
    dy = -1 if boost else 0; tilt = -8 if boost else 0
    g = [f'<g transform="translate(0,{dy}) rotate({tilt} 32 36)">']
    g.append(flame(12, 47, 115, 9, 5, boost) + flame(19, 49, 105, 9, 5, boost))
    # gift-box jetpack on the back
    g.append(f'<rect x="7" y="26" width="17" height="19" rx="3" fill="{MINT}" {st(1.8)}/><rect x="13.5" y="26" width="4" height="19" fill="{GOLD}" {st(1)}/>'
             f'<rect x="7" y="33.5" width="17" height="4" fill="{GOLD}" {st(1)}/>'
             f'<path d="M15.5,26 Q10,19 12,24 Q11,27 15.5,26 Q21,19 19,24 Q20,27 15.5,26 Z" fill="{GOLD}" {st(1.3)}/>'
             f'<rect x="9.5" y="45" width="5" height="3" rx="1" fill="{GOLD2}" {st(1.1)}/><rect x="16.5" y="45" width="5" height="3" rx="1" fill="{GOLD2}" {st(1.1)}/>')
    # onesie body: ghost-like dome with a soft hem
    g.append(f'<path d="M20,30 C20,20 26,14 35,14 C44,14 50,20 50,30 L50,46 C50,53 46,57 41,57 L29,57 C24,57 20,53 20,46 Z" fill="url(#red)" {st(2.2)}/>')
    g.append(f'<path d="M21,46 Q35,51 49,46" fill="none" stroke="{FUR}" stroke-width="4" stroke-linecap="round"/><path d="M21,46 Q35,51 49,46" fill="none" stroke="{L}" stroke-width="1" opacity="0.4"/>')
    g.append(f'<ellipse cx="30" cy="58" rx="3.4" ry="2.2" fill="{BOOT}"/><ellipse cx="40" cy="58" rx="3.4" ry="2.2" fill="{BOOT}"/>')
    # hood opening: fur rim framing the face
    g.append(f'<ellipse cx="35.5" cy="30" rx="13" ry="11.6" fill="{FUR}" {st(1.8)}/><ellipse cx="35.5" cy="30.6" rx="10.4" ry="9.2" fill="url(#skin)" {st(1.2)}/>')
    g.append(f'<path d="M30,37.6 Q35.5,41.5 41,37.6 Q39,40.6 35.5,40.8 Q32,40.6 30,37.6 Z" fill="{FUR}" {st(1.1)}/>')  # tiny beard fluff
    g.append(face(35.5, 29.4, 0.62, "open", "o" if boost else "w"))
    # hood tip flops back with pompom
    tip = (14, 10) if boost else (16, 13)
    g.append(f'<path d="M27,17 Q22,10 {tip[0]+2},{tip[1]}" fill="none" stroke="{L}" stroke-width="7" stroke-linecap="round"/><path d="M27,17 Q22,10 {tip[0]+2},{tip[1]}" fill="none" stroke="{RED2}" stroke-width="4.2" stroke-linecap="round"/>'
             + pompom(tip[0], tip[1], 3.3))
    # mitten holds the present sack in front
    g.append(sack(50, 50 if not boost else 46, 0.7, 10) + mitten(48, 43 if not boost else 39, -20))
    g.append("</g>")
    return "".join(g)

HEROES = {"A": ("Round mini Santa, twin-rocket pack", "A pocket-sized jingle ball: a round Santa puffing along on two little rockets, his sack bouncing behind.", hero_a),
          "B": ("Santa riding a candy-cane rocket", "Santa straddles a peppermint candy-cane rocket, with the sack hooked on its crook. Reads instantly as 'Christmas'.", hero_b),
          "C": ("Hooded chibi Santa, gift-box jetpack", "A hoodie-onesie Santa with a gift-box jetpack. It's closest to the ghost's dome silhouette, so the hitbox swap is easiest.", hero_c)}
def hero_svg(key, boost, size=64): return svg(size, size, DEFS + HEROES[key][2](boost), "0 0 64 64")

# ---------------- sheet ----------------
def sheet():
    F = ImageFont.truetype(FONT, 26); FS = ImageFont.truetype(FONT, 15); FT = ImageFont.truetype(FONT, 34)
    W, rowh = 1180, 300; Hh = 90 + rowh * 3 + 20
    im = Image.new("RGBA", (W, Hh), "#2B2347"); d = ImageDraw.Draw(im)
    for i in range(140):
        r = random.Random(i); x, y = r.uniform(0, W), r.uniform(0, Hh); d.ellipse((x - 1.4, y - 1.4, x + 1.4, y + 1.4), fill=(255, 255, 255, 140))
    d.text((30, 22), "Santa's Rocket Run: hero options (concept)", font=FT, fill="#FFE08A")
    d.text((W - 30, 34), "64px gameplay + 3x  |  idle / boost", font=FS, fill="#E6DDF7", anchor="ra")
    for i, k in enumerate("ABC"):
        y = 90 + i * rowh
        d.rounded_rectangle((20, y, W - 20, y + rowh - 16), 22, fill="#3B3166", outline="#6B4E7A", width=3)
        d.text((40, y + 14), f"{k})  {HEROES[k][0]}", font=F, fill="#FFFFFF")
        x = 40
        for boost in (False, True):  # 64px on a gameplay-size plate
            d.rounded_rectangle((x, y + 70, x + 84, y + 154), 12, fill="#4B4682")
            im.alpha_composite(png(hero_svg(k, boost)), (x + 10, y + 80)); d.text((x + 42, y + 160), "boost" if boost else "idle", font=FS, fill="#E6DDF7", anchor="ma")
            x += 100
        x += 10
        for boost in (False, True):
            d.rounded_rectangle((x, y + 52, x + 212, y + 264), 16, fill="#4B4682")
            im.alpha_composite(png(hero_svg(k, boost), 192, 192), (x + 10, y + 62)); x += 228
        d.text((x - 456 + 106, y + 268), "idle  (3x)", font=FS, fill="#E6DDF7", anchor="ma"); d.text((x - 228 + 106, y + 268), "boost  (3x)", font=FS, fill="#E6DDF7", anchor="ma")
        # pitch text
        tx = x + 16; words = HEROES[k][1].split(); line = ""; ly = y + 80
        for w in words:
            if d.textlength(line + " " + w, font=FS) > W - 40 - tx and line: d.text((tx, ly), line, font=FS, fill="#FFF8F0"); ly += 22; line = w
            else: line = (line + " " + w).strip()
        d.text((tx, ly), line, font=FS, fill="#FFF8F0")
    p = os.path.join(OUT, "santa-hero-options.png")
    im.convert("RGB").quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(p, optimize=True); return p

# ---------------- mock: stage 2 London, 360x640 ----------------
def big_ben(x, b, s, col, lit):
    return (f'<g transform="translate({x},{b}) scale({s})"><rect x="-14" y="-190" width="28" height="190" fill="{col}"/>'
            f'<path d="M-17,-190 H17 V-198 H-17 Z" fill="{col}"/><rect x="-16" y="-232" width="32" height="42" fill="{col}"/>'
            f'<circle cx="0" cy="-212" r="12" fill="{lit}"/><path d="M0,-212 V-220 M0,-212 L6,-209" stroke="{col}" stroke-width="2" stroke-linecap="round"/>'
            f'<path d="M-16,-232 L0,-268 L16,-232 Z" fill="{col}"/><path d="M0,-268 V-282" stroke="{col}" stroke-width="3"/>'
            + "".join(f'<rect x="{-8 + j*6}" y="{-170 + i*26}" width="3" height="12" rx="1.5" fill="{lit}" opacity="0.55"/>' for i in range(6) for j in range(3)) + '</g>')
def tower_bridge(x, b, col, lit):
    tw = lambda tx: (f'<rect x="{tx-12}" y="{b-120}" width="24" height="120" fill="{col}"/><path d="M{tx-14},{b-120} L{tx},{b-146} L{tx+14},{b-120} Z" fill="{col}"/>'
                     + "".join(f'<path d="M{tx+dx},{b-122} l-3,-10 h6 Z" fill="{col}"/>' for dx in (-12, 12))
                     + f'<rect x="{tx-4}" y="{b-100}" width="8" height="12" rx="4" fill="{lit}" opacity="0.6"/>')
    return (tw(x) + tw(x + 120) + f'<rect x="{x}" y="{b-112}" width="120" height="8" fill="{col}"/><rect x="{x}" y="{b-100}" width="120" height="3" fill="{col}"/>'
            f'<path d="M{x-70},{b-36} Q{x-30},{b-70} {x-6},{b-96} M{x+126},{b-96} Q{x+150},{b-70} {x+190},{b-36}" stroke="{col}" stroke-width="3" fill="none"/>'
            f'<rect x="{x-80}" y="{b-36}" width="290" height="8" fill="{col}"/>')
def house_row(y0, cols, rnd):
    g = []; x = -10
    while x < 370:
        w = rnd.choice((44, 52, 60)); h = rnd.choice((54, 66, 78)); c = rnd.choice(cols)
        g.append(f'<rect x="{x}" y="{y0-h}" width="{w}" height="{h+40}" fill="{c}" stroke="#2B2347" stroke-width="1.5"/>'
                 f'<path d="M{x-4},{y0-h} L{x+w/2},{y0-h-20} L{x+w+4},{y0-h} Z" fill="{c}" stroke="#2B2347" stroke-width="1.5"/>'
                 f'<path d="M{x-5},{y0-h+1} L{x+w/2},{y0-h-21} L{x+w+5},{y0-h+1} Q{x+w*0.75},{y0-h+6} {x+w/2},{y0-h+2} Q{x+w*0.25},{y0-h+7} {x-5},{y0-h+1} Z" fill="#FFFFFF" stroke="#C9C2E8" stroke-width="1"/>')
        for wx in (x + 9, x + w - 19):
            for wy in (y0 - h + 12, y0 - h + 36):
                if wy < y0 - 8: g.append(f'<rect x="{wx}" y="{wy}" width="10" height="13" rx="2" fill="#FFE08A" opacity="{rnd.choice((0.95, 0.7, 0.35))}"/>')
        x += w + 2
    return "".join(g)
def bus(x, y):
    return (f'<g transform="translate({x},{y})"><rect x="0" y="0" width="118" height="62" rx="12" fill="url(#red)" {st(2.2)}/>'
            f'<path d="M4,2 Q59,-6 114,2" fill="#FFFFFF" stroke="#C9C2E8" stroke-width="1"/><rect x="0" y="27" width="118" height="5" fill="{GOLD}"/>'
            + "".join(f'<rect x="{8 + i*21}" y="8" width="16" height="14" rx="3" fill="#FFE08A" {st(1.2)}/>' for i in range(5))
            + "".join(f'<rect x="{8 + i*21}" y="37" width="16" height="13" rx="3" fill="#FFE08A" {st(1.2)}/>' for i in range(4))
            + f'<rect x="94" y="36" width="18" height="24" rx="3" fill="#BFE6FF" {st(1.2)}/>'
            f'<circle cx="26" cy="62" r="8" fill="{BOOT}" {st(1.6)}/><circle cx="92" cy="62" r="8" fill="{BOOT}" {st(1.6)}/><circle cx="26" cy="62" r="3" fill="#C9C2E8"/><circle cx="92" cy="62" r="3" fill="#C9C2E8"/>'
            f'<circle cx="114" cy="50" r="2.6" fill="#FFF4C9"/>'
            f'<g transform="translate(0,-7)">' + face(103, 51, 0.32, "open", "w").replace('fill="url(#e)"', f'fill="{EYE}"') + '</g></g>')
def ice_top(x, bottom):
    """top column (anchored, per David's rule): Tower Bridge walkway lattice hanger from above, a cross girder,
    and the icicle fringe hanging UNDER the girder (gap edge = icicle tips at `bottom`)"""
    gy = bottom - 46                       # girder top
    g = (f'<rect x="{x+26}" y="-10" width="6" height="{gy+12}" fill="#8FC4F0"/><rect x="{x+48}" y="-10" width="6" height="{gy+12}" fill="#8FC4F0"/>'
         + "".join(f'<path d="M{x+32},{y} L{x+48},{y+32} M{x+48},{y} L{x+32},{y+32}" stroke="#6FA4D8" stroke-width="4"/>' for y in range(-10, gy, 32))
         + f'<path d="M{x+26},-10 V{gy} M{x+32},-10 V{gy} M{x+48},-10 V{gy} M{x+54},-10 V{gy}" stroke="{L}" stroke-width="1.6"/>')
    g += (f'<rect x="{x+4}" y="{gy}" width="72" height="16" rx="2" fill="#8FC4F0" {st(2.2)}/><rect x="{x+4}" y="{gy}" width="72" height="4" fill="#6FA4D8"/>'
          f'<rect x="{x+4}" y="{gy+12}" width="72" height="4" fill="#6FA4D8"/><rect x="{x+4}" y="{gy}" width="72" height="16" rx="2" fill="none" {st(2.2)}/>'
          + "".join(f'<circle cx="{x+cx}" cy="{gy+8}" r="1.6" fill="#FFFFFF" opacity="0.8"/>' for cx in (10, 18, 62, 70)))
    for x0, x1 in ((4, 26), (54, 76)):
        g += f'<path d="M{x+x0-2},{gy+2} Q{x+(x0+x1)/2},{gy-7} {x+x1+2},{gy+2} Z" fill="#FFFFFF" {st(1.4)}/>'
    for dx, l in ((10, 18), (20, 28), (30, 14), (40, 30), (50, 16), (60, 26), (70, 14)):
        g += f'<path d="M{x+dx-4},{gy+15} L{x+dx},{gy+16+l} L{x+dx+4},{gy+15} Z" fill="#CFEAFF" {st(1.4)}/>'
    g += f'<g transform="translate({x+40},{gy+8})">' + face(0, 0, 0.3, "closed", "w").replace('fill="url(#e)"', f'fill="{EYE}"') + '</g>'
    return g
def chimney_bottom(x, top, H=640):
    g = f'<rect x="{x+4}" y="{top+14}" width="72" height="{H-top}" fill="#E7A08F" {st(2.2)}/>'
    for r in range(int((H - top) / 14)):
        yy = top + 28 + r * 14; g += f'<path d="M{x+4},{yy} H{x+76}" stroke="#C47F76" stroke-width="1.4"/>'
        g += "".join(f'<path d="M{x + 4 + o},{yy} V{yy+14}" stroke="#C47F76" stroke-width="1.4"/>' for o in ((18, 54) if r % 2 else (36,)))
    g += (f'<rect x="{x+16}" y="{top-8}" width="16" height="24" rx="3" fill="#C9798F" {st(1.8)}/><rect x="{x+46}" y="{top-14}" width="18" height="30" rx="3" fill="#C9798F" {st(1.8)}/>'
          f'<path d="M{x},{top+16} Q{x+20},{top+2} {x+40},{top+12} Q{x+60},{top+2} {x+80},{top+16} L{x+80},{top+24} L{x},{top+24} Z" fill="#FFFFFF" {st(2)}/>'
          f'<path d="M{x+14},{top-6} Q{x+24},{top-14} {x+34},{top-6} Z M{x+44},{top-12} Q{x+55},{top-20} {x+66},{top-12} Z" fill="#FFFFFF" {st(1.6)}/>'
          f'<circle cx="{x+55}" cy="{top-28}" r="6" fill="#F3EEFC" opacity="0.8"/><circle cx="{x+60}" cy="{top-40}" r="4.5" fill="#F3EEFC" opacity="0.6"/>')
    return g
def pigeon(x, y):
    return (f'<g transform="translate({x},{y})"><path d="M-14,4 Q-22,0 -20,-6 Q-14,-2 -10,0 Z" fill="#A9A3C9" {st(1.5)}/>'
            f'<ellipse cx="0" cy="2" rx="15" ry="12" fill="#C9C2E8" {st(2)}/><circle cx="9" cy="-8" r="8.5" fill="#C9C2E8" {st(2)}/>'
            f'<path d="M2,-4 Q9,0 16,-4 L16,0 Q9,4 2,0 Z" fill="#AEE3C6" opacity="0.9"/>'
            f'<path d="M-5,-2 Q-12,-14 -2,-10 Q2,-6 -5,-2 Z" fill="#A9A3C9" {st(1.5)}/>'
            f'<path d="M17,-8 L22,-6.5 L17,-5 Z" fill="{GOLD2}" {st(1)}/><circle cx="12" cy="-9.5" r="1.8" fill="{EYE}"/><circle cx="11.4" cy="-10.2" r="0.6" fill="#FFF"/>'
            f'<ellipse cx="9" cy="-4.6" rx="2" ry="1.2" fill="{BLUSH}"/>'
            f'<path d="M3,-15 Q9,-26 17,-14 Z" fill="url(#red)" {st(1.4)}/><rect x="2" y="-16.5" width="16" height="3.6" rx="1.8" fill="{FUR}" {st(1)}/>' + pompom(17.5, -22, 2.2) +
            f'<path d="M-2,14 v4 M4,14 v4" stroke="{GOLD2}" stroke-width="1.8" stroke-linecap="round"/></g>')
def bauble(x, y, r=13):
    return (f'<circle cx="{x}" cy="{y}" r="{r*1.9}" fill="url(#glow)"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#gold)" {st(2)}/>'
            f'<path d="M{x-r+2},{y+2} Q{x},{y+7} {x+r-2},{y+2}" fill="none" stroke="#FFFFFF" stroke-width="1.6" opacity="0.8"/>'
            f'<rect x="{x-4}" y="{y-r-5}" width="8" height="6" rx="1.5" fill="#E6DDF7" {st(1.4)}/><path d="M{x-2},{y-r-5} Q{x},{y-r-11} {x+2},{y-r-5}" fill="none" {st(1.4)}/>'
            f'<ellipse cx="{x-4.5}" cy="{y-4.5}" rx="3.2" ry="2" fill="#FFF" opacity="0.9" transform="rotate(-30 {x-4.5} {y-4.5})"/>'
            f'<path d="M{x+r+6},{y-r} l1.2,3 3,1.2 -3,1.2 -1.2,3 -1.2,-3 -3,-1.2 3,-1.2 Z" fill="#FFF4B8" stroke="#D9953A" stroke-width="0.8"/>'
            f'<path d="M{x-r-7},{y+r-4} l0.9,2.2 2.2,0.9 -2.2,0.9 -0.9,2.2 -0.9,-2.2 -2.2,-0.9 2.2,-0.9 Z" fill="#FFF4B8" stroke="#D9953A" stroke-width="0.7"/>')
def hud_text(x, y, t, size, fill="#FFFFFF", anchor="middle"):
    a = f'x="{x}" y="{y}" font-family="Capriola" font-size="{size}" text-anchor="{anchor}"'
    return f'<text {a} fill="{L}" stroke="{L}" stroke-width="{size*0.22:.1f}" stroke-linejoin="round">{t}</text><text {a} fill="{fill}">{t}</text>'
def mock(hero=True, path=None):
    W, H = 360, 640; r = random.Random(12); g = [DEFS]
    g.append('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1F1D44"/><stop offset="0.7" stop-color="#3E3A78"/><stop offset="1" stop-color="#5B5596"/></linearGradient>'
             f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    g.append(f'<circle cx="300" cy="96" r="60" fill="url(#glow)" opacity="0.6"/><circle cx="300" cy="96" r="22" fill="#FFF4D6"/><circle cx="310" cy="90" r="19" fill="#2A2652" opacity="0.0"/>')
    g += [f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, 400):.0f}" r="{r.choice((0.8, 1, 1.3))}" fill="#FDF6FF" opacity="{r.uniform(0.4, 0.9):.2f}"/>' for _ in range(40)]
    # far: river + Big Ben + Tower Bridge silhouettes
    g.append(f'<rect x="0" y="470" width="{W}" height="60" fill="#3A3670"/>' + big_ben(70, 474, 1.0, "#47427F", "#FFE7A8") + tower_bridge(196, 474, "#47427F", "#FFE7A8"))
    g.append(f'<path d="M0,470 H{W}" stroke="#FFFFFF" stroke-width="2" opacity="0.25"/>')
    # mid: snowy roofs
    g.append(house_row(560, ("#6E5E9C", "#7C6BB0", "#5E5090"), r))
    # ground: snowy street + red bus
    g.append(f'<path d="M0,586 Q90,578 180,586 T360,584 V640 H0 Z" fill="#FFFFFF"/><path d="M0,604 H360" stroke="#E6DDF7" stroke-width="3"/>')
    g.append(bus(40, 540))
    g.append(f'<path d="M40,540 Q99,532 158,540" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')
    # obstacle pair (one column, gap 200px)
    g.append(ice_top(200, 200) + chimney_bottom(200, 410))
    g.append(pigeon(300, 300))
    g.append(bauble(150, 210))
    # Santa A in flight (64px), slight boost
    if hero: g.append(f'<g transform="translate(60,270)">{hero_a(True)}</g>')
    # falling snow on top
    g += [f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" r="{r.choice((1.4, 1.8, 2.4, 3))}" fill="#FFFFFF" opacity="{r.uniform(0.5, 0.95):.2f}"/>' for _ in range(70)]
    # HUD: score + stage chip + bauble count
    g.append(hud_text(180, 78, "24", 52))
    g.append(f'<rect x="12" y="14" width="118" height="28" rx="14" fill="#18102A" opacity="0.7"/>' + hud_text(71, 34, "Stage 2 · London", 13, "#FFE08A"))
    g.append(f'<rect x="276" y="14" width="72" height="28" rx="14" fill="#18102A" opacity="0.7"/>' + bauble(294, 28, 8).replace('r="15.2"', 'r="0"') + hud_text(326, 34, "×3", 14))
    if path: return svg(W, H, "".join(g))  # svg only (used by build_santa_c.py for the animation background)
    p = os.path.join(OUT, "santa-mock-london.png")
    png(svg(W, H, "".join(g))).convert("RGB").save(p, optimize=True); return p

if __name__ == "__main__":
    for p in (sheet(), mock()): print(p, os.path.getsize(p))
