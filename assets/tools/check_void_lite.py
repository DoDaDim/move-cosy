"""Rebuild the Void layers from the v0.6 lite parts (as Code would draw them) and compare with the -full backups.
Also checks horizontal seams (self-wrap) of every lite tile and prints decoded RGBA memory (w*h*4)."""
import os, json, numpy as np
from PIL import Image
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
bg = json.load(open("hitboxes.json"))["backgrounds"]["void"]
def im(n, sc): return Image.open(f"png/{sc}x/{n}.png").convert("RGBA")
def build(layer, sc):
    W, H = 720 * sc, 640 * sc; out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for p in bg[layer]:
        if p.get("kind") == "gradient":
            t = np.linspace(0, 1, H)[:, None]; a = np.array([int(p["top"][i:i+2], 16) for i in (1, 3, 5)]); b = np.array([int(p["bottom"][i:i+2], 16) for i in (1, 3, 5)])
            g = (a + (b - a) * t).round().astype(np.uint8); g = np.repeat(g[:, None, :], W, 1)
            out.alpha_composite(Image.fromarray(np.dstack([g, np.full((H, W), 255, np.uint8)]), "RGBA"))
        elif p.get("kind") == "sprites":
            for q in p["placements"]:
                s = p["sprites"][q["sprite"]]; spr = im(q["sprite"], sc); k = q["scale"]
                spr = spr.resize((max(1, round(spr.width * k)), max(1, round(spr.height * k))), Image.LANCZOS)
                ax, ay = s["anchor"]; out.alpha_composite(spr, (round((q["x"] - ax * k) * sc), round((q["y"] - ay * k) * sc)))
        elif p.get("repeat") == "xy":
            t = im(p["file"][:-4], sc)
            for x in range(0, W, t.width):
                for y in range(0, H, t.height): out.alpha_composite(t, (x, y))
        elif "drawH" in p:
            out.alpha_composite(im(p["file"][:-4], sc).resize((W, H), Image.BILINEAR))
        else:
            out.alpha_composite(im(p["file"][:-4], sc), (0, p["y"] * sc))
    return out
mem = lambda w, h: w * h * 4
tot_old = {1: 0, 2: 0}; tot_new = {1: 0, 2: 0}
for layer in ("far", "mid", "near"):
    for sc in (1, 2):
        old = im(f"bg-void-{layer}-full", sc); tot_old[sc] += mem(*old.size)
        new = build(layer, sc)
        bgc = Image.new("RGBA", old.size, (44, 35, 86, 255))  # compare over the void sky colour
        A = np.asarray(Image.alpha_composite(bgc, old)).astype(float)[:, :, :3]; Bn = np.asarray(Image.alpha_composite(bgc, new)).astype(float)[:, :, :3]
        d = np.abs(A - Bn)
        if sc == 2: new.save(f"/tmp/void-lite-{layer}.png")
        print(f"{layer} @{sc}x  mean diff {d.mean():5.2f}  p99 {np.percentile(d, 99):5.1f}  max {d.max():5.0f}")
files = sorted({p["file"][:-4] for L in ("far", "mid", "near") for p in bg[L] if "file" in p} | set(bg["near"][2]["sprites"]))
for n in files:
    for sc in (1, 2):
        a = np.asarray(im(n, sc)).astype(float); tot_new[sc] += mem(a.shape[1], a.shape[0])
        if n.startswith(("bg-void-mid", "bg-void-near-ceil", "bg-void-near-floor", "bg-void-far-nebula")) and sc == 1:
            inner = np.percentile(np.abs(np.diff(a, axis=1)).mean(axis=(0, 2)), 99); seam = np.abs(a[:, -1] - a[:, 0]).mean()
            print(f"  seam {n:32s} {seam:5.2f} (p99 inner {inner:5.2f}) {'OK' if seam <= max(1.0, inner) else 'CHECK'}")
    if n == "bg-void-far-stars":
        a = np.asarray(im(n, 1)).astype(float); print(f"  seam {n:32s} x {np.abs(a[:, -1] - a[:, 0]).mean():5.2f} y {np.abs(a[-1] - a[0]).mean():5.2f}")
for sc in (1, 2): print(f"RGBA decode @{sc}x: old {tot_old[sc]/2**20:6.2f} MiB -> new {tot_new[sc]/2**20:6.2f} MiB  ({100*(1-tot_new[sc]/tot_old[sc]):.0f}% less)")
