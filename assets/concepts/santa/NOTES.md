# Santa's Rocket Run (December skin): first-step concepts

This is concept art only and is not wired into the game. Everything is script-generated SVG, rendered with cairosvg by `tools/build_santa_concepts.py` (run `python3 tools/build_santa_concepts.py`). It uses the ghost's kawaii language from `assets/tools/build_ghosts.py`: the #6B4E7A outline, gradient eyes with double highlights, blush with tick marks, and 'w'/'o' mouths, plus the golden-ghost golds and the game's lilac night sky. This job didn't touch game files, `hitboxes.json` or the main `ASSETS.md`.

## santa-hero-options.png
Each option is shown at 64px gameplay size and at 3x, in idle and boost frames. Boost tilts up about 9°, uses the 'o' mouth and has a 1.5x flame puff.

| option | pitch |
|---|---|
| A) Round mini Santa, twin-rocket pack | A pocket-sized jingle ball puffing along on two little rockets, his sack bouncing behind. |
| B) Santa on a candy-cane rocket | Santa straddles a peppermint candy-cane rocket, with the sack hooked on its crook. Reads instantly as "Christmas". |
| C) Hooded chibi Santa, gift-box jetpack | A hoodie-onesie Santa with a gift-box jetpack. It's the closest to the ghost's dome silhouette, so the hitbox swap is easiest. |

Hitbox notes for later:
- **A and C** fit the ghost's roughly round body and could reuse its hitbox, with the flame and sack left out of it.
- **B** is wide and low: the rocket runs about x 4–62 and y 42–56. It would need a capsule hitbox, or a slightly smaller rocket.

## santa-mock-london.png (360x640, stage 2 "London")
- **Background:** a snowy night with Big Ben and Tower Bridge silhouettes over the Thames, a row of snowy roofs with lit windows, and a kawaii red double-decker bus on the snowy street.
- **Obstacle pair:**
  - Top: a frosted ice column with an icicle fringe (sleepy face).
  - Bottom: a snowy brick chimney stack with pots and smoke puffs.
  - Both use the 72px footprint, with a gap of about 200px.
- **Floater:** a chibi pigeon in a Santa hat with a mint scarf.
- **Pickup:** a gold magic bauble with a glow and sparkles.
- **Hero:** Santa A in boost.
- **HUD:** the score "24", a "Stage 2 · London" chip, and a bauble counter showing ×3.

## If a direction is picked
- Next steps would be full idle and flap frame sets matching `ghost-normal-*`, and a golden variant.
- Flame-puff FX strips would come next.
- London obstacles and backgrounds would follow the v0.4 top and bottom rules, with a continuity check.

---

# Santa C sprite set (David's pick: hooded chibi + gift-box jetpack)
This is still in the concept folder and not wired into the game; no game files were touched. It's built by `tools/build_santa_c.py`, which reuses the helpers in `tools/build_santa_concepts.py` (run `python3 tools/build_santa_c.py`).
- Output is in `santa-c/`: `*.svg`, `png/1x/*.png` and `png/2x/*.png`, plus `png/{1x,2x}/<set>-strip.png` with frames left to right.
- Previews: `santa-c-sprites.png` (the sheet), `santa-c-boost-preview.mp4` (720x1280, H.264 yuv420p, 24 fps, 4.0 s, 96 frames, seamless loop) and `santa-c-boost-preview.gif` (360x640, 12 fps, loops).

## Conventions (matching the ghost)
- **Hero frames:** drawn at the ghost's 64px gameplay scale on a **96x128 canvas**. The extra 32px below is for the full jet flame. Every frame was alpha-scanned with nothing touching any edge, and the lowest flame pixel is at row 97 of 128.
  - **Anchor (48,48)** is the ghost's (32,32) + 16. Draw at `(x - 48k, y - 48k)` with `k = CONFIG.ghost.size / 64`, and rotate about the anchor.
  - **Hitbox:** circle **(48,49) r18**, the same as the ghost's (32,33) r18. Flame, sack, pompom, aura and sparkles never collide.
  - If you rotate on an offscreen canvas, pad it to at least 200x200 (1x) around the anchor so the flame can't be clipped. The preview pads to a square centred on the anchor before rotating.
- **Deaths:** 128x128, **anchor (64,64)**, 12 fps, play once and hold the last frame, the same pattern as `death-<type>-*`. Every frame stays inside the canvas: things leaving the frame fade out instead of being cut off.
- **Trail FX:** `fx-santa-boost-trail`, 160x128, **emitter point (144,64)**, 10 frames at 16 fps (0.63 s).
  - On each tap, spawn one at the jet nozzle: hero canvas point (25,61), or the anchor offset (-23, +13.5) rotated by the current tilt.
  - Leave it in world space so it scrolls back at world speed. Draw it **before** (behind) Santa.

| set (files `<set>-<n>`) | frames | fps | canvas | anchor | play | notes |
|---|---|---|---|---|---|---|
| `santa-c-idle` | 4 | 8 | 96x128 | 48,48 | loop | Gentle bob (0, -1, -2, -1 px) with a steady, clearly visible twin jet flame that flickers in length. Frame 2 blinks. |
| `santa-c-boost` | 4 | 16 | 96x128 | 48,48 | once per tap (0.25 s), then back to idle | Frame 0 squash (1.14 x 0.86), with the flame igniting. Frame 1 stretch (0.88 x 1.14) and **full burst, about 2.2x the idle flame, with flickering tongues**. Frames 2-3 settle while the flame flickers down. |
| `fx-santa-boost-trail` | 10 | 16 | 160x128 | emitter 144,64 | once per tap | 14 snow puffs, 12 sparkles and 6 snowflakes. Full opacity for the first half, then a fade. |
| `santa-c-rush-idle` / `-boost` | 4 / 4 | 8 / 16 | 96x128 | 48,48 | as above | Gold bauble (Rush): gold aura, gold trim and ribbon, honey flame, twinkles. |
| `santa-c-life-idle` / `-boost` | 4 / 4 | 8 / 16 | 96x128 | 48,48 | as above | Red bauble (Extra Life): rose aura, pink trim, pink flame. |
| `santa-c-chill-idle` / `-boost` | 4 / 4 | 8 / 16 | 96x128 | 48,48 | as above | Blue bauble (Chill): icy-blue aura, frost trim, blue flame. |
| `death-santa-generic` | 10 | 12 | 128 | 64,64 | once, hold last | Bonk, dizzy spin and shrink, then a sparkle poof. The last frame is nearly empty, so fade it. |
| `death-santa-floor` | 8 | 12 | 128 | 64,64 | once, hold last | Splat with dust, bounce, flop, then lies on his side with x_x eyes while the jetpack sputters. Floor line y=95. |
| `death-santa-icicle` | 12 (1.0 s) | 12 | 128 | 64,64 | once, hold last | Frost flash (0). An ice block freezes up around him (1-3). Frozen and shivering (4-7). Cracks (8-9). It shatters into shards and he's left frosty and dazed (10-11). |
| `death-santa-chimney` | 12 (1.0 s) | 12 | 128 | 64,64 | once, hold last | Bonk from below (0) and squash (1). A soot cloud bursts (2-3). Soot-covered Santa blinks and coughs a puff (4-11). |
| `death-santa-pigeon` | 14 (1.17 s) | 12 | 128 | 64,64 | once, hold last | A pigeon fades in and swoops (0-2) and snatches the hood tip (3). It flaps off up-right carrying the hat while Santa tumbles down and both fade out (4-13). The last frame is empty. |
| `death-santa-plane` | 12 (1.0 s) | 12 | 128 | 64,64 | once, hold last | A little plane and its contrail whoosh across (0-1). Hit (2). He spins off up-left in a contrail swirl, shrinking and fading (3-11). |

The ghost-world `death-santa-tombstone` is **removed**, replaced by the Santa-world deaths above.

## Suggested death-type mapping (Santa skin; ids are the ones `game.js` passes to `die()`)
| what killed him | death |
|---|---|
| London top columns with icicles or frozen ice (e.g. the mock's ice column), and any icy hazard | `icicle` |
| bottom chimney stacks, brick and roof columns | `chimney` |
| `hazard:pigeon` floater, or any bird | `pigeon` |
| a plane event, `event:plane-*` or a fast flyover hazard | `plane` |
| `ground` | `floor` |
| `ceiling` and anything unmapped | `generic` |

If the Santa skin needs it, add a `death-map-santa.json` (or a `santa` block) next to the main map later. Nothing was written to the game's `death-map.json`.

## Not made yet (cheap to add)
Bauble-variant deaths. Until then, the normal deaths cover every type.

## Stage set: top/bottom pairs and what each top hangs from

David's rule: every top must make physical sense. Each one has a drawn anchor (girder, ledge, bough fork, wire, lintel,
balloon envelope, crane cable) or is a real sky object (aurora, cloud). Nothing floats from nowhere and no top is a flipped
ground object. The full specs are in `SANTA-ASSETS.md`, and the build is in `tools/build_santa_stages.py`.

| stage | top | anchor | bottom it pairs with |
|---|---|---|---|
| 1 Lapland | `aurora` | the northern lights themselves: a curtain of aurora hanging out of the sky (no hard anchor needed, it IS the sky) | `pine` |
|  | `sprucebough` | a giant snowy spruce bough reaching down from the top edge: the brown trunk with needle tufts comes down, forks into a wide snow-laden branch, and icicles hang beneath it | `workshop` |
|  | `pinebough` | an elf lantern hangs on a cord from the fork of a giant pine's drooping snowy bough | `gifts` |
| 2 London | `girder` | icicles hang under a Tower Bridge walkway girder; the lattice hanger runs up to the walkway off-screen | `chimney` |
|  | `snowcloud` | a low snow cloud - genuinely in the sky, snowing | `phonebox` |
|  | `lights` | Regent St-style fairy lights: each tile is a wire strung between the buildings (ends fade off-column); a giant bauble hangs from the lowest wire | `bus` |
| 3 New York | `cranehook` | a tower crane's hook block on two cable falls from the jib above, lifting a present | `skyscraper` |
|  | `trafficlight` | a traffic light hung from a span wire, with snowflake decorations on the span wires above it | `xmastree` |
|  | `elgirder` | icicles under an elevated-railway girder; lattice bents run up to the track deck | `taxi` |
| 4 Rio | `cablecar` | the Sugarloaf cable car: the hanger arm runs up to the haul rope above the screen | `sugarloaf` |
|  | `bunting` | festa bunting on wires strung across a street between buildings, a pennant drop hanging from the lowest one | `palm` |
|  | `rockledge` | an overhanging granite ledge of the Morro da Urca with vines and a bromeliad hanging under it | `drums` |
| 5 Egypt | `balloon` | a Luxor hot-air balloon: the body IS the lower envelope (it fills the sky above); burner and basket hang from its mouth | `pyramid` |
|  | `fanous` | fanous lanterns strung on wires across a souk lane, a big one on the lowest wire | `obelisk` |
|  | `templeledge` | a brass oil lamp hanging on a chain under a temple's overhanging sandstone lintel | `camel` |
| 6 Tokyo | `chochin` | red chochin lanterns on wires strung across a shopping street (the steering example), a big one at the bottom | `pagoda` |
|  | `neongantry` | a neon panel chained under a steel sign gantry; the gantry legs go up off-screen | `vending` |
|  | `matsubough` | a glass furin wind bell hanging from the fork of a snowy Japanese pine bough | `manekineko` |
| 7 Sydney | `bridgehanger` | a festive star hung under the Harbour Bridge deck; the hanger runs up to the arch | `opera` |
|  | `gumbranch` | a koala in a Santa hat hugging the fork of a gum tree's overhanging branch | `surfboards` |
|  | `summercloud` | a fluffy summer cloud with the sun peeking out - in the sky | `sandcastle` |
| 8 Antarctica | `serac` | an ice-cliff face coming down from above: snow-crusted overhanging lip at the screen top (obs-antarctica-serac-lip, wider than the column), blue strata down the face, drip edge and icicles at the cap | `iceberg` |
|  | `blizzard` | a low blizzard cloud blowing snow - in the sky | `penguins` |
|  | `aurora` | the aurora australis: a pink-teal curtain hanging out of the sky | `snowman` |

Pairs are suggestions only. Any top can meet any bottom of its stage, since both edges come from the hitbox JSON.

**London mock fix (santa-mock-london.png):** the icicle column used to be an ice block hanging from nothing. Now the icicles
hang under a Tower Bridge walkway girder, with the blue lattice hanger running up off-screen (`ice_top` in
`tools/build_santa_concepts.py`). The Santa C boost preview MP4/GIF uses this mock as its backdrop, so I re-rendered it too.

**QA fix (Oct 19):** the Lapland fell-ledge top read as a grey stone pillar, so it's replaced by `obs-lapland-sprucebough` (a snowy spruce bough with icicles under its fork). The Antarctica serac is redrawn as an ice-cliff face with strata, a drip edge with icicles, and a decorative snow-crusted lip piece `obs-antarctica-serac-lip` (112x36) pinned to the screen top. The aurora zone reuses it.
