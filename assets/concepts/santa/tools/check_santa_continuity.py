"""Run the game's own column audit (assets/tools/check_hitbox_continuity.py, unmodified logic) on stages/santa-hitboxes.json.
Also verifies: every top has an 'anchor', every column has a death type, bodies are one rect, every stage has 3 tops + 3 bottoms.
Usage: python3 check_santa_continuity.py   (exit 1 on any break)"""
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
GAME_TOOLS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "tools"))
spec = importlib.util.spec_from_file_location("chk", os.path.join(GAME_TOOLS, "check_hitbox_continuity.py"))
chk = importlib.util.module_from_spec(spec); spec.loader.exec_module(chk)   # loads hitboxes.json read-only; replaced below
chk.H = json.load(open(os.path.join(HERE, "..", "stages", "santa-hitboxes.json")))
bad = n = 0
for name, h, y0, y1 in chk.pieces():
    n += 1
    br, wr = chk.audit(name, h, y0, y1)
    for a, b in br: print(f"BREAK  {name:42s} no coverage y {a:g}..{b:g}"); bad += 1
    for y in wr: print(f"warn   {name:42s} rows {y-chk.STEP:g}/{y:g} only touch diagonally")
    base = name.rsplit("-cap-", 1)[0] if "-cap-" in name else None
    if base and base + "-body" in chk.H:
        y = 0.5 if name.endswith("-cap-bottom") else 79.5
        if not chk.seam(name, h, chk.H[base + "-body"], y): print(f"BREAK  {name:42s} does not overlap {base}-body at the joint row y {y}"); bad += 1
    if name.endswith("-body") and (len(h.get("rects", [])) != 1 or h.get("circles")): print(f"BREAK  {name} body is not exactly one rect"); bad += 1
cols = chk.H["columns"]; per = {}
for k, v in cols.items():
    if k.startswith("_") or not isinstance(v, dict): continue
    per.setdefault(v["stage"], [0, 0])[0 if v["side"] == "top" else 1] += 1
    if v["side"] == "top" and not v.get("anchor"): print("BREAK", k, "top without an anchor"); bad += 1
    if v.get("death") not in ("icicle", "chimney", "pigeon", "plane", "floor", "generic"): print("BREAK", k, "bad death", v.get("death")); bad += 1
for s, (t, b) in per.items():
    if (t, b) != (3, 3): print("BREAK stage", s, "has", t, "tops", b, "bottoms"); bad += 1
print(f"{n} column pieces checked across {len(per)} stages ({sum(t for t, b in per.values())} tops / {sum(b for t, b in per.values())} bottoms), {bad} break(s)")
sys.exit(1 if bad else 0)
