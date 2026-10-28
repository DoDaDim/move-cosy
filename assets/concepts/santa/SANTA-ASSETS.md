# Santa's Rocket Run - asset list (concept, NOT wired into the game)

Seasonal skin of **Move Cosy** (the umbrella title; the ghost is the Halloween version). Everything here lives under
`assets/concepts/santa/` and nothing in `assets/` proper, `hitboxes.json` or the game code was touched.
Style: the same kawaii chibi SVG look as Santa C and the ghost. All script-generated (`tools/`), no AI art, no tracing.

| | |
|---|---|
| Hero | Santa C (hooded chibi, gift-box jetpack) - see `NOTES.md` / `santa-c/` |
| Stages | 8, then an endless **aurora** zone after Antarctica |
| Columns | 48 (3 tops + 3 bottoms per stage), 96 pieces, **0 continuity breaks** |
| Column rules | exactly the game's v0.4/v0.5/Void rules (ASSETS.md §§11-14): 80px canvas, 72px footprint (x 4..76), `-body` 80x64 with exactly one rect, caps 80x80 |
| Tops | body + cap-bottom only. `ceilEdge` = the gap edge (bottom of the cap). Every top is anchored or genuinely in the sky (David's rule, table below) |
| Bottoms | cap-top + body. `floorEdge` = the gap edge (top of the cap). `pumpkinSeat` kept in the schema for compatibility |
| Backgrounds | lite bands + y offsets over a gradient sky, same approach as the Void v0.6 set (ASSETS.md §14.2) |
| Check | `python3 tools/check_santa_continuity.py` -> `96 column pieces checked across 8 stages (24 tops / 24 bottoms), 0 break(s)` |

## 1. Top obstacles and their anchors

David's rule: nothing hangs from nowhere and nothing is a flipped ground object. Each top either has a drawn anchor
(girder, ledge, branch, wire, lintel, envelope, crane cable) or is itself a sky object (aurora, cloud, balloon).

| stage | id | anchor | death | w |
|---|---|---|---|---|
| Lapland | `obs-lapland-aurora` | the northern lights themselves: the curtain IS the sky, no hard anchor needed | generic | 1 |
| | `obs-lapland-sprucebough` | a giant snowy spruce bough reaching down from the top edge: the brown trunk with needle tufts comes down, forks into a wide snow-laden branch, and icicles hang beneath it | icicle | 2 |
| | `obs-lapland-pinebough` | an elf lantern on a cord from the fork of a giant pine's drooping snowy bough | generic | 2 |
| London | `obs-london-girder` | icicles under a Tower Bridge walkway girder; lattice hanger up to the walkway | icicle | 2 |
| | `obs-london-snowcloud` | a low snow cloud, genuinely in the sky and snowing | icicle | 1 |
| | `obs-london-lights` | Regent St fairy lights: each tile is one wire strung between buildings (ends fade off-column into the buildings); a giant bauble hangs from the lowest wire | generic | 2 |
| New York | `obs-newyork-cranehook` | a tower crane's hook block on two cable falls from the jib above, lifting a present | generic | 2 |
| | `obs-newyork-trafficlight` | a traffic light hung from a span wire, with snowflake decorations on the wires above | generic | 2 |
| | `obs-newyork-elgirder` | icicles under an elevated-railway girder; lattice bents run up to the track deck | icicle | 1 |
| Rio | `obs-rio-cablecar` | the Sugarloaf cable car: the hanger arm runs up to the haul rope above the screen | plane | 2 |
| | `obs-rio-bunting` | festa bunting on wires strung across a street, a pennant drop on the lowest wire | generic | 2 |
| | `obs-rio-rockledge` | an overhanging granite ledge of the Morro da Urca with vines and a bromeliad under it | generic | 1 |
| Egypt | `obs-egypt-balloon` | a Luxor hot-air balloon: the body IS the lower envelope (it fills the sky above); the burner and basket hang from its mouth | plane | 1 |
| | `obs-egypt-fanous` | fanous lanterns strung on wires across a souk lane, a big one on the lowest wire | generic | 2 |
| | `obs-egypt-templeledge` | a brass oil lamp on a chain under a temple's overhanging sandstone lintel | generic | 2 |
| Tokyo | `obs-tokyo-chochin` | red chochin lanterns on wires strung across a shopping street, a big one at the bottom | generic | 2 |
| | `obs-tokyo-neongantry` | a neon panel chained under a steel sign gantry; the gantry legs go up off-screen | generic | 2 |
| | `obs-tokyo-matsubough` | a glass furin wind bell hanging from the fork of a snowy Japanese pine bough | generic | 1 |
| Sydney | `obs-sydney-bridgehanger` | a festive star hung under the Harbour Bridge deck; the hanger runs up to the arch | generic | 2 |
| | `obs-sydney-gumbranch` | a koala in a Santa hat hugging the fork of a gum tree's overhanging branch | generic | 1 |
| | `obs-sydney-summercloud` | a fluffy summer cloud with the sun peeking out, in the sky | generic | 2 |
| Antarctica | `obs-antarctica-serac` | an ice-cliff face coming down from above: snow-crusted overhanging lip at the screen top (obs-antarctica-serac-lip, wider than the column), blue strata down the face, drip edge and icicles at the cap. Lip: draw `obs-antarctica-serac-lip.png` (112x36, no hitbox) at (columnX-16, 0) over the body, see `columns.obs-antarctica-serac.topLip` | icicle | 2 |
| | `obs-antarctica-blizzard` | a low blizzard cloud blowing snow, in the sky | icicle | 1 |
| | `obs-antarctica-aurora` | the aurora australis: a pink-teal curtain hanging out of the sky | generic | 2 |

Wire columns (lights, trafficlight, bunting, fanous, chochin): the body is one wire plus its drop cord and tiles seamlessly
in 64px steps; the cap is the lowest wire with the big object. The wire ends fade out at the column edges on purpose,
so the string reads as continuing into the buildings off-column.

## 2. Bottom obstacles

| stage | id | what it is | death | w | floorEdge |
|---|---|---|---|---|---|
| Lapland | `obs-lapland-pine` | snowy pine tiers, star on top | generic | 2 | 16 |
| | `obs-lapland-workshop` | elf-workshop stone chimney, candy-stripe crown, wreath | chimney | 2 | 20 |
| | `obs-lapland-gifts` | stacked presents, bow on top | generic | 1 | 6 |
| London | `obs-london-chimney` | brick chimney stack with pots | chimney | 2 | 4 |
| | `obs-london-phonebox` | stacked red phone boxes, domed top | generic | 1 | 4 |
| | `obs-london-bus` | double-decker windows stacked, front top deck as the cap | generic | 2 | 12 |
| New York | `obs-newyork-skyscraper` | setback tower with a spire light | generic | 2 | 4 |
| | `obs-newyork-xmastree` | Rockefeller-style tree with lights | generic | 1 | 16 |
| | `obs-newyork-taxi` | yellow cab parked on a snowbank | generic | 2 | 12 |
| Rio | `obs-rio-sugarloaf` | granite dome with moss | generic | 2 | 9 |
| | `obs-rio-palm` | fairy-lit palm trunk (narrow 18px body); the outer fronds are decorative | generic | 2 | 22 |
| | `obs-rio-drums` | stacked samba surdo drums, sticks decorative | generic | 1 | 20 |
| Egypt | `obs-egypt-pyramid` | stepped pyramid, gold capstone | generic | 2 | 10 |
| | `obs-egypt-obelisk` | pink granite obelisk (36px body) | generic | 1 | 10 |
| | `obs-egypt-camel` | a camel in a Santa hat lying on a dune | generic | 2 | 15 |
| Tokyo | `obs-tokyo-pagoda` | pagoda storeys, eaves decorative | generic | 2 | 8 |
| | `obs-tokyo-vending` | stacked vending machines | generic | 2 | 24 |
| | `obs-tokyo-manekineko` | lucky cat on crates | generic | 1 | 10 |
| Sydney | `obs-sydney-opera` | Opera House sail shells on a podium | generic | 1 | 8 |
| | `obs-sydney-surfboards` | three upright surfboards with tinsel | generic | 2 | 12 |
| | `obs-sydney-sandcastle` | sandcastle wall and turret, flag decorative | generic | 2 | 10 |
| Antarctica | `obs-antarctica-iceberg` | faceted iceberg peak | icicle | 2 | 10 |
| | `obs-antarctica-penguins` | penguin tower, the top one in a Santa hat | generic | 2 | 8 |
| | `obs-antarctica-snowman` | snowballs stacked, snowman head on top | icicle | 1 | 4 |

`w` is the suggested weight (Tuning owns weights). Exact hitboxes, `ceilEdge`/`floorEdge` and `pumpkinSeat` are in
`stages/santa-hitboxes.json` under `columns`.

## 3. Floaters

40x40, 4 frames @ 6fps, circle (20,20) r13, one per stage. Motion (drift/bob) is Code's, as with the Void floaters.

| id | art | death |
|---|---|---|
| `santa-float-lapland` | `obs-lapland-float-reindeer` - flying reindeer, bell collar | generic |
| `santa-float-london` | `obs-london-float-pigeon` - pigeon in a Santa hat | pigeon |
| `santa-float-newyork` | `obs-newyork-float-plane` - little prop plane | plane |
| `santa-float-rio` | `obs-rio-float-macaw` - scarlet macaw | pigeon |
| `santa-float-egypt` | `obs-egypt-float-ibis` - sacred ibis | pigeon |
| `santa-float-tokyo` | `obs-tokyo-float-papercrane` - origami crane | pigeon |
| `santa-float-sydney` | `obs-sydney-float-gull` - seagull | pigeon |
| `santa-float-antarctica` | `obs-antarctica-float-penguinfloe` - penguin on a tiny ice floe | icicle |

## 4. Death mapping

`stages/santa-death-map.json`. Strips live in `santa-c/` (see `NOTES.md` for frames/fps/anchors: 128 canvas, anchor (64,64), 12fps).

| death | strip | used for |
|---|---|---|
| icicle | `death-santa-icicle` | spruce bough + girders with icicles, serac, snow/blizzard clouds, iceberg, snowman, penguin floe |
| chimney | `death-santa-chimney` | `obs-lapland-workshop`, `obs-london-chimney` |
| pigeon | `death-santa-pigeon` | bird floaters (pigeon, macaw, ibis, gull, paper crane) |
| plane | `death-santa-plane` | `obs-rio-cablecar`, `obs-egypt-balloon`, the plane floater |
| floor | `death-santa-floor` | hitting the ground |
| generic | `death-santa-generic` | everything else, and the default |

## 5. Magic baubles and HUD

Same powers as the special ghosts (ASSETS.md §13). 56x56, 4 frames @ 8fps, circle (28,30) r16, `gapCentre`.

| id | power | art | HUD icon |
|---|---|---|---|
| `santa-rush` | `power-rush` | gold bauble, star inside, twinkles | `ui-hud-santa-rush-{32,48}.png` |
| `santa-life` | `power-life` | red bauble, heart inside | `ui-hud-santa-life-{32,48}.png` |
| `santa-chill` | `power-chill` | blue bauble, snowflake inside | `ui-hud-santa-chill-{32,48}.png` |

## 6. Banners, badges, bursts

- `ui-santa-banner-<stage>` and `ui-santa-banner-<stage>-blank`: 300x90 ribbon, one per stage incl. aurora. Titles baked in: Lapland, London, New York, Rio, Egypt, Tokyo, Sydney, Antarctica, Aurora.
- `ui-santa-badge` (blank) and `ui-santa-badge-1..8`: 96x48, "Stage" + number.
- `fx-santa-burst-<stage>-0..5` (+ `-strip`): 160x160, centre (80,80), 6 frames @ 12fps, play once. Per-stage items: flakes, baubles, stars, fireworks, pyramids, lanterns, suns, penguins.

## 7. Backgrounds (lite) and sky palettes

`stages/santa-sky-palettes.json` gives the gradient top/bottom (y 0 -> 640). `backgrounds` in `santa-hitboxes.json`
lists every band with its file, size and world y. Draw order per layer: gradient first, then parts in list order.
Scroll: far 0.1, mid 0.3, near 0.6 (aurora 0.05 / 0.15 / 0.5). `bg-santa-far-stars.png` is one shared 360x320 tile,
repeated 2x2 over the 720x640 slot on every night stage.

| stage | sky top -> bottom | bands (1x) | decoded RGBA |
|---|---|---|---|
| lapland | #1B2348 -> #3E5E8A | far aurora 720x220 @y20, fells 720x160 @y360, mid forest 720x200 @y380 (pines, reindeer, workshop), near snow 720x80 @y560 | 2.36MB / 9.45MB @2x |
| london | #1F1D44 -> #5B5596 | far skyline 720x140 @y360, mid landmarks 720x320 @y220 (Big Ben, Tower Bridge, Thames), near roofs 720x140 @y500 (snowy roofs, red bus) | 2.19MB / 8.76MB |
| newyork | #1C2044 -> #4C3E7A | far skyline 720x220 @y300, mid towers 720x280 @y260 (skyscrapers, spire, Rockefeller tree), near street 720x100 @y540 (taxis) | 2.19MB / 8.76MB |
| rio | #241A4A -> #7A4E8E | far corcovado 720x260 @y160 (Christ the Redeemer, fireworks), mid sugarloaf 720x260 @y300 (cable-car line), near promenade 720x160 @y480 | 2.42MB / 9.68MB |
| egypt | #2A2350 -> #C98A7A | far dunes 720x160 @y380, mid pyramids 720x200 @y340 (pyramids, Sphinx), near sand 720x100 @y540 (camel train) | 1.79MB / 7.14MB |
| tokyo | #1A1840 -> #5A3E86 | far fuji 720x300 @y200, mid city 720x260 @y280 (Tokyo Tower, neon), near street 720x120 @y520 (lantern strings) | 2.42MB / 9.68MB |
| sydney | #6EC3F0 -> #FFE3B8 | far sea 720x160 @y380 (sun, no stars), mid harbour 720x230 @y330 (Opera House, Harbour Bridge), near beach 720x100 @y540 | 1.41MB / 5.64MB |
| antarctica | #16264A -> #4E7AA8 | far aurora 720x220 @y10 + mountains 720x160 @y360, mid icebergs 720x210 @y360, near shelf 720x100 @y540 (penguins) | 2.45MB / 9.79MB |
| aurora | #0E1430 -> #2E2A66 | far aurora 720x260 @y10, mid ribbons 720x200 @y200, near horizon 720x80 @y560 | 2.02MB / 8.06MB |

Memory is per stage including the shared stars tile once. A full-height 720x640 opaque layer is 1.84MB, so a stage's
three layers would have been ~5.5MB; the lite set is roughly 1.4-2.5MB.

**Endless zone:** `aurora`, after Antarctica. Its columns reuse the Antarctica set (`_stageTopsAurora` /
`_stageBottomsAurora`); a random mix of all stages' columns would also work.

## 8. Transitions

One shared white snow-mist overlay, `fx-santa-mist-0..7` (360x640, 8 frames @ 12fps, + `fx-santa-mist-strip`),
same shape as the Void mist: it blooms to frame ~5 then thins, so swap the stage layers under it at frame 3.
Per-stage colour comes from a multiply tint (`backgrounds.transition.tint` in the JSON). Pre-tinted 1x strips are also
provided as `fx-santa-mist-<stage>-strip.png` so no runtime tinting is needed.

## 9. Files

```
stages/svg/*.svg                     263 SVGs (columns, floaters, baubles, banners, badges, bursts, mist, bands)
stages/png/1x, png/2x                PNGs + strips; HUD icons only at 1x (32 and 48)
stages/santa-hitboxes.json           columns, hazards, pickups, backgrounds, ui, death per column
stages/santa-sky-palettes.json
stages/santa-death-map.json
stages/previews/santa-preview-<stage>.png   one sheet per stage incl. aurora, each under 1MB
stages/previews/santa-overview.png          all 9 stages, 133KB
tools/santa_lib.py            drawing helpers + column registration (the v0.4 rules)
tools/santa_obstacles.py      the 24 tops and 24 bottoms
tools/santa_columns.py        the stage table (ids, anchors, deaths, weights)
tools/santa_bg.py             background bands
tools/build_santa_stages.py   builds everything
tools/check_santa_continuity.py
```

## 10. Wiring it in later (for Code)

1. Copy `stages/svg`, `stages/png/1x`, `stages/png/2x` into `assets/` (names don't collide: everything is prefixed
   `obs-<stage>-`, `bg-santa-`, `ui-santa-`, `fx-santa-`, `pickup-santa-`).
2. Merge `santa-hitboxes.json`: column pieces into the top level, `columns.*` into `columns`, `hazards` into `hazards`,
   `pickups` into `pickups`, and add the stages to `backgrounds` exactly like `backgrounds.void` (parts with y offsets).
3. Merge `santa-sky-palettes.json` into `sky-palettes.json`.
4. Santa C hero: `santa-c/`, canvas 96x128, anchor (48,48), circle (48,49) r18, which is the ghost's (32,33) r18 shifted
   by +16. Idle 4f @ 8fps, boost 4f @ 16fps, trail `fx-santa-boost-trail` 10f @ 16fps on 160x128, emitter (144,64).
5. Deaths: look up the column/floater id in `santa-death-map.json`; ground hits use `floor`.
6. Stage order: lapland, london, newyork, rio, egypt, tokyo, sydney, antarctica, then loop the aurora zone.
7. Transitions: play `fx-santa-mist-<stage>-strip` (the destination tint) and swap layers at frame 3.
