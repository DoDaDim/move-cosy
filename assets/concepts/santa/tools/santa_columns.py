"""Stage table for the Santa columns: ids, families, anchors, death types. Imported by build_santa_stages.py."""
from santa_obstacles import *
O = __import__("santa_obstacles")
ORDER = ["lapland", "london", "newyork", "rio", "egypt", "tokyo", "sydney", "antarctica"]
AUR_N = dict(c1="#9EF0C8", c2="#B9A3F5", c3="#FFFFFF")
AUR_S = dict(c1="#FFB3E0", c2="#8FE3D0", c3="#FFFFFF")
TOPS = {  # id: (builder, anchor explanation, death, weight)
 "lapland": [("aurora",     lambda: curtain(AUR_N), "the northern lights themselves: a curtain of aurora hanging out of the sky (no hard anchor needed, it IS the sky)", "generic", 1),
             ("sprucebough", lambda: bough(dict(kind="pine", bark="#8E6A5E", bark2="#6E4E4A", leaf="#3F8A6A", snow=True), "icicles"), "a giant snowy spruce bough reaching down from the top edge: the brown trunk with needle tufts comes down, forks into a wide snow-laden branch, and icicles hang beneath it", "icicle", 2),
             ("pinebough",  lambda: bough(dict(kind="pine", bark="#A97A6E", bark2="#8E6A5E", leaf="#6FBF8E", snow=True), "lantern"), "an elf lantern hangs on a cord from the fork of a giant pine's drooping snowy bough", "generic", 2)],
 "london":  [("girder",     lambda: girder(dict(steel="#8FC4F0", steel2="#6FA4D8", snow=True), "icicles"), "icicles hang under a Tower Bridge walkway girder; the lattice hanger runs up to the walkway off-screen", "icicle", 2),
             ("snowcloud",  lambda: cloud(dict(col="#F3EEFC", shade="#DCD3F2"), "snow"), "a low snow cloud - genuinely in the sky, snowing", "icicle", 1),
             ("lights",     lambda: wires(dict(wire="#4A3358"), "bulbs", "bauble"), "Regent St-style fairy lights: each tile is a wire strung between the buildings (ends fade off-column); a giant bauble hangs from the lowest wire", "generic", 2)],
 "newyork": [("cranehook",  lambda: cable({}, "hook"), "a tower crane's hook block on two cable falls from the jib above, lifting a present", "generic", 2),
             ("trafficlight", lambda: wires(dict(wire="#3A2E5E"), "flake", "traffic"), "a traffic light hung from a span wire, with snowflake decorations on the span wires above it", "generic", 2),
             ("elgirder",   lambda: girder(dict(steel="#9ED8B8", steel2="#6FB896", snow=True), "icicles"), "icicles under an elevated-railway girder; lattice bents run up to the track deck", "icicle", 1)],
 "rio":     [("cablecar",   lambda: cable(dict(car="#FFD45C", car2="#E2A23E"), "car"), "the Sugarloaf cable car: the hanger arm runs up to the haul rope above the screen", "plane", 2),
             ("bunting",    lambda: wires(dict(wire="#3A2E5E", flags=("#FF8FB1", "#FFE08A", "#9EF0E0", "#AEE3C6", "#B9A3F5")), "flags", "flags"), "festa bunting on wires strung across a street between buildings, a pennant drop hanging from the lowest one", "generic", 2),
             ("rockledge",  lambda: ledge(dict(rock="#C9AFC0", rock2="#A98FA6"), "vines"), "an overhanging granite ledge of the Morro da Urca with vines and a bromeliad hanging under it", "generic", 1)],
 "egypt":   [("balloon",    lambda: balloon(dict(stripes=("#FF8FB1", "#FFE08A", "#9EF0E0", "#FFB36B", "#B9A3F5", "#FFE08A"))), "a Luxor hot-air balloon: the body IS the lower envelope (it fills the sky above); burner and basket hang from its mouth", "plane", 1),
             ("fanous",     lambda: wires(dict(wire="#5A3828"), "fanous", "fanous"), "fanous lanterns strung on wires across a souk lane, a big one on the lowest wire", "generic", 2),
             ("templeledge", lambda: ledge(dict(rock="#F2CF95", rock2="#D6A866", metal="#8E6A4E"), "lamp"), "a brass oil lamp hanging on a chain under a temple's overhanging sandstone lintel", "generic", 2)],
 "tokyo":   [("chochin",    lambda: wires(dict(wire="#3A2E5E"), "chochin", "chochin"), "red chochin lanterns on wires strung across a shopping street (the steering example), a big one at the bottom", "generic", 2),
             ("neongantry", lambda: girder(dict(steel="#B9B3D9", steel2="#8E86B8", snow=False), "sign"), "a neon panel chained under a steel sign gantry; the gantry legs go up off-screen", "generic", 2),
             ("matsubough", lambda: bough(dict(kind="pine", bark="#8E6A5E", bark2="#6E4E4A", leaf="#4FA67A", snow=True), "furin"), "a glass furin wind bell hanging from the fork of a snowy Japanese pine bough", "generic", 1)],
 "sydney":  [("bridgehanger", lambda: girder(dict(steel="#B9B3D9", steel2="#9E95C9", snow=False), "star"), "a festive star hung under the Harbour Bridge deck; the hanger runs up to the arch", "generic", 2),
             ("gumbranch",  lambda: bough(dict(kind="gum", bark="#E6DDF7", bark2="#C9C2E8", leaf="#9ED8B8", snow=False), "koala"), "a koala in a Santa hat hugging the fork of a gum tree's overhanging branch", "generic", 1),
             ("summercloud", lambda: cloud(dict(col="#FFFFFF", shade="#E6EEFA"), "sun"), "a fluffy summer cloud with the sun peeking out - in the sky", "generic", 2)],
 "antarctica": [("serac",   "SERAC", "an ice-cliff face coming down from above: snow-crusted overhanging lip at the screen top (obs-antarctica-serac-lip, wider than the column), blue strata down the face, drip edge and icicles at the cap", "icicle", 2),
             ("blizzard",   lambda: cloud(dict(col="#E6EEFA", shade="#C9D8F0"), "blizzard"), "a low blizzard cloud blowing snow - in the sky", "icicle", 1),
             ("aurora",     lambda: curtain(AUR_S), "the aurora australis: a pink-teal curtain hanging out of the sky", "generic", 2)],
}
BOTS = {  # id: (builder, death, weight)
 "lapland": [("pine", lambda: pine(dict(leaf="#6FBF8E")), "generic", 2), ("workshop", workshop, "chimney", 2), ("gifts", gifts, "generic", 1)],
 "london":  [("chimney", chimney, "chimney", 2), ("phonebox", phonebox, "generic", 1), ("bus", bus_stack, "generic", 2)],
 "newyork": [("skyscraper", skyscraper, "generic", 2), ("xmastree", lambda: pine(dict(leaf="#4FA67A"), True), "generic", 1), ("taxi", taxi, "generic", 2)],
 "rio":     [("sugarloaf", sugarloaf, "generic", 2), ("palm", palm, "generic", 2), ("drums", drums, "generic", 1)],
 "egypt":   [("pyramid", pyramid, "generic", 2), ("obelisk", obelisk, "generic", 1), ("camel", camel, "generic", 2)],
 "tokyo":   [("pagoda", pagoda, "generic", 2), ("vending", vending, "generic", 2), ("manekineko", manekineko, "generic", 1)],
 "sydney":  [("opera", opera, "generic", 1), ("surfboards", surfboards, "generic", 2), ("sandcastle", sandcastle, "generic", 2)],
 "antarctica": [("iceberg", iceberg, "icicle", 2), ("penguins", penguins, "generic", 2), ("snowman", snowman, "icicle", 1)],
}
BOT_NOTE = {
 "pine": "snowy pine tiers; star decorative", "workshop": "elf-workshop stone chimney, candy-stripe crown, wreath; smoke decorative", "gifts": "stacked presents; bow decorative",
 "chimney": "brick chimney stack + pots; smoke decorative", "phonebox": "stacked red phone boxes, domed top", "bus": "double-decker windows stacked, front top deck as cap",
 "skyscraper": "setback tower + spire light", "xmastree": "Rockefeller-style tree with lights; star decorative", "taxi": "yellow cab parked on a snowbank",
 "sugarloaf": "granite dome with moss", "palm": "fairy-lit palm trunk (narrow 18px body); outer fronds decorative", "drums": "stacked samba surdo drums; sticks decorative",
 "pyramid": "stepped pyramid with gold capstone", "obelisk": "pink granite obelisk (36px body)", "camel": "a camel in a Santa hat lying on a dune",
 "pagoda": "pagoda storeys; eaves overhang decorative", "vending": "stacked vending machines", "manekineko": "lucky cat on crates",
 "opera": "Opera House sail shells on a podium", "surfboards": "three upright surfboards with tinsel", "sandcastle": "sandcastle wall + turret; flag decorative",
 "iceberg": "faceted iceberg peak", "penguins": "penguin tower, top one in a Santa hat", "snowman": "snowballs stacked, snowman head on top",
}
def build_columns():
    for s in ORDER:
        for oid, fn, anchor, death, w in TOPS[s]:
            if fn == "SERAC":
                b, c, lip, hbb, hbc = serac(); n = f"obs-{s}-{oid}"
                reg_top(n, s, b, c, hbb, hbc, anchor, death)
                FILES[n + "-lip"] = svg(112, 36, lip)
                EDGES[n]["topLip"] = {"file": n + "-lip", "size": [112, 36], "draw": "decorative, no hitbox: draw at (columnX - 16, 0) i.e. pinned to the screen top, over the body"}
                continue
            b, c, hbb, hbc = fn(); reg_top(f"obs-{s}-{oid}", s, b, c, hbb, hbc, anchor, death)
        for oid, fn, death, w in BOTS[s]:
            b, c, hbb, hbc, seat = fn(); reg_bot(f"obs-{s}-{oid}", s, b, c, hbb, hbc, seat, death, BOT_NOTE[oid])
