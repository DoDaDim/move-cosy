// =============================================================================
// Move Cosy — pack #1: Ghost (Sept–Nov). Pack format 1 (docs/ARCHITECTURE.md).
// Pure data: the engine (game.js) composes it over the global CONFIG at boot.
// The tap-to-float feel (CONFIG.ghost) and the speed-up (CONFIG.speed) are global and are NOT set here;
// a stage may only override them through the fields the engine allows (physics / speed / gap / spacing).
// All values are the v0.6.3 values, moved here unchanged (TUNING.md v2.0).
// =============================================================================
PackRegistry.register({
  id: 'ghost',
  format: 1,
  name: 'Ghost',                 // version name (picker, top-10, share card)
  title: 'Ghost Flap',           // start-screen title (canvas)
  months: [9, 10, 11],           // informational; the season window lives in packs/manifest.js
  storage: { legacyKeys: true }, // v0.7.0: Ghost owns the pre-pack keys (`${bestKey}`, `${bestKey}.<id>`, `${bestKey}.top`) — no migration needed

  // ---- hero sprite set (normal / golden strips; rush / life / chill art lives in heroSpecials; deaths in deathAnims) ----
  hero: {
    strips: { normal: 'ghost-normal-strip.png', golden: 'ghost-golden-strip.png' },
    frameOrder: ['idle-0', 'idle-1', 'flap-0', 'flap-1', 'flap-2'],
    frameSize: 64,
    anchor: [32, 32],
    hitbox: { cx: 32, cy: 33, r: 18 },
    idleFrames: ['idle-0', 'idle-1'],
    idleFps: 2,
    flapFrames: ['flap-0', 'flap-1', 'flap-2', 'flap-1'],
    flapFps: 12,
    deadFrame: 'idle-1',
  },
  // Art (ASSETS.md §13). Offsets relative to the 64px hero's top-left; sizes in game px.
  heroSpecials: {
    pickup: { rush: 'pickup-rush-strip.png', extraLife: 'pickup-life-strip.png', slowMo: 'pickup-chill-strip.png', size: 56, frames: 4, fps: 8 },
    ghostRush: { file: 'ghost-rush-strip.png', w: 112, h: 64, frames: 4, fps: 12, dx: -48, dy: 0 },
    rushAura: { file: 'fx-rush-aura-strip.png', w: 96, h: 96, frames: 4, fps: 8, dx: -16, dy: -16 },
    candyBurst: { file: 'fx-candy-burst-strip.png', w: 128, h: 128, frames: 6, fps: 12 },
    heart: { file: 'ghost-heart-overlay-strip.png', w: 20, h: 20, frames: 2, fps: 4, dx: 40, dy: 2 },
    heartPop: { file: 'fx-heart-pop-strip.png', w: 96, h: 96, frames: 6, fps: 12, dx: -16, dy: -16 },
    heartBreak: { file: 'fx-heart-break-strip.png', w: 96, h: 96, frames: 6, fps: 12, dx: -16, dy: -16 },
    frostBurst: { file: 'fx-frost-burst-strip.png', w: 96, h: 96, frames: 6, fps: 12, dx: -16, dy: -16 },
    frostVignette: { file: 'ui-frost-vignette.png' },
    flakes: ['fx-frost-flake-a.png', 'fx-frost-flake-b.png', 'fx-frost-flake-c.png'], flakeSize: 16,
    hud: { rush: 'ui-hud-rush-48.png', extraLife: 'ui-hud-life-48.png', slowMo: 'ui-hud-chill-48.png', size: 26 },
    fxSeconds: 0.5, // = 6 frames @ 12 fps
    placeholder: { rush: '#FFD966', extraLife: '#FF6F8E', slowMo: '#8FD3FF' },
  },

  // ---- ordered stages ----
  // startAt: PAIRS passed (TUNING v1.7). enter.cutscene: reached ONLY through that cutscene (see cutscenes).
  // top/bottom: weighted obstacle sets (ids in objects). Per-stage overrides the engine accepts: physics (keys of
  // CONFIG.ghost, or 'normal'), breatherPairs, speed { stepEveryPairs, stepAmount, max } (ramps on from the global
  // speed-up, counted from stage entry), gap, spacing, specials { <type>: rate overrides }.
  // look.style picks the engine's placeholder painters (used until/if the art is missing).
  stages: [
    { id: 'graveyard', name: 'The Graveyard', startAt: 0,
      top:    { 'lantern-branch': 2, 'spider': 2 },
      bottom: { 'tomb-a': 1, 'tomb-b': 1, 'tomb-c': 1, 'coffin': 1, 'cross': 1 },
      palette: ['#241D40', '#5E4A86'],
      look: { sky: ['#1e1433', '#4a3270'], celestial: 'moon', ground: '#3b2a55', groundTop: '#6b5394', layers: ['#3a2a5c', '#30224d', '#271b40'],
              style: { silhouettes: 'graves', backdrop: 'twinkle', ground: 'spikes' } },
      floaters: { chance: 0.15, mix: { skull: 2, pumpkin: 1 } },
      event: { id: 'hearse', type: 'groundSweep', firesAt: 3, seconds: 3.0, bonus: 3,
               floorRise: 60, length: 150, // placeholder size; the sprite uses hitboxes.json (top 52 px)
               sheet: 'hearse', warning: { label: 'Hearse!', groundOffset: -32 }, bonusText: 'Hearse dodged!',
               desc: 'Hearse rolls along the ground; floor rises 60 px while it passes.' },
      ambient: { fog: { enabled: true, count: 6, alpha: 0.16, drift: 12 } } },
    { id: 'church', name: 'The Old Church', startAt: 5,
      top:    { 'chandelier': 2, 'bats': 1, 'bell': 1 },
      bottom: { 'ivystone': 2, 'font': 1, 'lychgate': 1 },
      palette: ['#222350', '#5A5490'],
      look: { sky: ['#1d1838', '#51407a'], celestial: 'moon', ground: '#3d2f52', groundTop: '#7a6a9c', layers: ['#3b3163', '#322853', '#291f45'],
              style: { silhouettes: 'church', backdrop: 'twinkle', ground: 'spikes' } },
      floaters: { chance: 0.20, mix: { bat: 2, skull: 1 } },
      event: { id: 'batSwarm', type: null, firesAt: 10, seconds: 3.5, bonus: 4,   // stub (no handler yet: logged only)
               desc: '6 bats burst from the spire in a loose line across the upper half; fly low.' },
      ambient: { birds: { enabled: true, count: 6, roofY: 430, scatterDist: 120, flyVx: -80, flyVy: -120 } } },
    { id: 'countryside', name: 'Countryside', startAt: 15,
      top:    { 'beehive': 2, 'branch': 2, 'swing': 1 },
      bottom: { 'haybales': 2, 'pumpkinstack': 1, 'churn': 1 },
      palette: ['#1E2C4A', '#4E6E8A'],
      look: { sky: ['#18213d', '#3f4d7a'], celestial: 'moon', ground: '#2f3d4a', groundTop: '#5f8a7a', layers: ['#2c3a5e', '#25314f', '#1e2842'],
              style: { silhouettes: 'farm', backdrop: 'twinkle', ground: 'spikes' } },
      floaters: { chance: 0.25, mix: { pumpkin: 2, bat: 1 } },
      event: { id: 'pumpkinRoll', type: null, firesAt: 22, seconds: 4.0, bonus: 5,   // stub
               desc: '3 pumpkins bounce across the lower half at different heights; thread between.' },
      ambient: { fireflies: { enabled: true, count: 14 } } },
    { id: 'school', name: 'School Town', startAt: 30,
      top:    { 'handbell': 2, 'kite': 2, 'lamp': 1 },
      bottom: { 'books': 2, 'lockers': 2, 'globe': 1 },
      palette: ['#26245A', '#6E5694'],
      look: { sky: ['#22183a', '#5a3f72'], celestial: 'moon', ground: '#3c2f4f', groundTop: '#8a6f9c', layers: ['#3d2f5e', '#33264f', '#2a1f42'],
              style: { silhouettes: 'school', backdrop: 'twinkle', ground: 'spikes' } },
      floaters: { chance: 0.30, mix: { bat: 1, pumpkin: 1, skull: 1 } },
      event: { id: 'sweetShower', type: null, firesAt: 38, seconds: 4.0, bonus: 0, perSweet: 1, maxSweets: 6, // stub
               desc: 'Trick-or-treat sweets fall from the top; catch them for +1 each. No hazards.' },
      ambient: { bikes: { enabled: true, spacing: 170, speedFactor: 1.05 } } },
    { id: 'city', name: 'Big City', startAt: 50,
      top:    { 'cradle': 2, 'trafficlight': 2, 'neonsign': 1, 'cranehook': 1 },
      bottom: { 'postbox': 2, 'phonebox': 1, 'hydrant': 1 },
      palette: ['#1C2044', '#4C3E7A'],
      look: { sky: ['#141428', '#3c2f5e'], celestial: 'moon', ground: '#2c2a3e', groundTop: '#5c5a7a', layers: ['#2a2848', '#22203d', '#1b1a33'],
              style: { silhouettes: 'skyline', backdrop: 'twinkle', ground: 'spikes', extra: { layer: 1, kind: 'litWindows' } } },
      floaters: { chance: 0.35, mix: { bat: 2, skull: 2, pumpkin: 1 } },
      event: { id: 'nightBus', type: null, firesAt: 58, repeatEvery: 25, seconds: 3.5, bonus: 6, // stub
               desc: 'Night bus along the ground (floor rises 70 px) with a pigeon flock above; ride the middle.' },
      ambient: { rain: { enabled: true, count: 60, speed: 500, slant: 125, color: 'rgba(212, 230, 255, 0.5)', width: 1.2 } } }, // one batched path, capped count; Art's (-125, +500) px/s
    { id: 'space', name: 'Outer Space', startAt: 100, enter: { cutscene: 'rocket' },
      top:    { 'satellite': 2, 'arm': 1, 'astronaut': 1, 'ufo': 1 },
      bottom: { 'moonrock': 2, 'crystals': 1, 'alienplant': 1 },
      // applied only while in space; same key names as CONFIG.ghost
      physics: { gravity: 1400, flapImpulse: -415, maxFallSpeed: 560, maxRiseSpeed: -520 },
      specials: { rush: { chancePerPair: 0.04, minPairsBetween: 20, pityAfterPairs: 40 } },
      palette: ['#120F2C', '#2B2050'],
      look: { sky: ['#05040f', '#1c1238'], celestial: 'planet', ground: '#4a4560', groundTop: '#7d7896', layers: ['#ffffff', '#c9b3f0', '#6c6488'],
              style: { silhouettes: 'starfield', backdrop: 'starfieldSheet', ground: 'craters', layerAlpha: [0.7, 0.35, 0.6], extra: { layer: 1, kind: 'planetRing' }, floatGlow: 'tomb-a' } },
      parallax: { far: 0.05, mid: 0.15, near: 0.5 },
      floaters: { chance: 0.35, mix: { miniAsteroid: 2, alien: 1 } },
      event: { id: 'meteorShower', type: 'diagonalShower', firesAt: 120, firesAfterLaunchPairs: 15, repeatEvery: 30, seconds: 4.0, bonus: 8,
               // 2 diagonal waves, each a curtain of meteors with one clear lane
               waves: 2, waveCrossAt: [1.0, 2.6], laneHeight: 170, spacing: 50,
               vx: -320, vy: 160, laneShiftMin: 60, laneShiftMax: 120, laneMinY: 140, laneMaxY: 420,
               r: 12, sheet: 'meteor', warning: { label: 'Meteors!', y: 90 }, laneTint: [184, 240, 210],
               desc: 'Meteors streak diagonally from top-right in 2 waves with a clear lane between; hold the lane.' },
      ambient: { stars: { enabled: true, count: 30 }, shootingStars: { enabled: true, intervalMin: 2, intervalMax: 4.5 } } },
    // TUNING v2.0: reached ONLY by the warp at a displayed score (no startAt in pairs). Art §14 column ids.
    { id: 'void', name: 'The Void', startAtScore: 200, enter: { cutscene: 'warp' }, // displayed score (= cutscenes.warp.atScore)
      top:    { 'obs-void-crt-top': 2, 'obs-void-phone-top': 2, 'obs-void-alarm-top': 2, 'obs-void-typewriter-top': 1, 'obs-void-cassette-top': 1, 'obs-void-gramophone-top': 1 },
      bottom: { 'obs-void-typewriter-bottom': 2, 'obs-void-crt-bottom': 2, 'obs-void-phone-bottom': 1, 'obs-void-cassette-bottom': 1, 'obs-void-gramophone-bottom': 1, 'obs-void-alarm-bottom': 1 },
      physics: 'normal',                 // back to standard flap and gravity
      breatherPairs: 1,                  // 1 random breather between patterns (was 2)
      speed: { stepEveryPairs: 10, stepAmount: 4, max: 270 }, // ramps on from 240, counted from Void entry
      gap: 145, spacing: 190,            // held at the floors, never tighter
      specials: { rush: { chancePerPair: 0.04, minPairsBetween: 20, pityAfterPairs: 40 } }, // the Void uses the space rates
      palette: ['#2C2356', '#7A64AE'], // sky-palettes.json (Art §14.2)
      // Nebula Drift (Art concept A palette #2A2150 #7A64AE #F3EAFF #D9C6F5 #6B4E7A #FFB6CC #AEE3C6 #BFE6FF)
      look: { sky: ['#2C2356', '#7A64AE'], celestial: 'none', ground: '#6B4E7A', groundTop: '#D9C6F5', layers: ['#D9C6F5', '#FFB6CC', '#BFE6FF'],
              mist: ['#FFB6CC', '#D9C6F5', '#AEE3C6', '#BFE6FF'], nebula: 0.28, ribbon: '#FFB6CC', ribbonShade: '#E58FAE', cloud: '#F3EAFF', cloudShade: '#D9C6F5',
              style: { silhouettes: 'nebula', backdrop: 'twinkle', ground: 'mistFloor', layerAlpha: [0.28, 0.8, 0.9] } },
      parallax: { far: 0.05, mid: 0.15, near: 0.5 }, // Art §14.2
      layerMeta: {},
      floaters: { chance: 0.40, mix: { 'void-float-a': 1, 'void-float-b': 1, 'void-float-c': 1, 'void-float-d': 1 } }, // retro floaters (d = floppy)
      // counted from Void entry (pairs at the warp); meteors are space-only, so they stop in the Void
      event: { id: 'invaderWave', type: 'laneWave', firesAfterEntryPairs: 10, repeatEvery: 30, seconds: 4.0, bonus: 10,
               // 2 rows (formations) sweep right -> left, each a full-height curtain with ONE clear lane
               waves: 2, waveCrossAt: [1.2, 2.8], laneHeight: 176, spacing: 44, r: 14, vx: -260, wiggle: 3,
               rowSheets: ['invader', 'invaderB', 'invaderC'], // one colour per row (wave), picked without repeats
               rowColors: ['#AEE3C6', '#FFB6CC', '#D9C6F5'],   // placeholder colours for the same three types
               popSeconds: 0.5, warningSheet: 'warningVoid', popSheet: 'invaderPop',
               laneShiftMin: 60, laneShiftMax: 110, laneMinY: 150, laneMaxY: 410,
               warning: { label: 'Invaders!', y: 90 }, laneTint: [174, 227, 198],
               desc: 'Two rows of retro pixel invaders sweep across with one clear lane at least 176 px tall; hold the lane.' },
      ambient: { mist: { enabled: true, count: 7, alpha: 0.22, drift: 10 }, sparkles: { enabled: true, count: 22 } } },
  ],
  stageRules: {
    loopFrom: 'void', // v2.0: The Void is the final, endless stage (space is no longer endless)
    // v0.6.1 (QA F3, David's rule: top and bottom must not look alike): never pair the same object top and bottom.
    // objectOf: regex whose group 1 names the object behind a column id (obs-void-crt-top / -bottom -> crt).
    pairRule: { distinctObjects: true, objectOf: '^obs-void-(.+)-(?:top|bottom)$' },
    aliases: { schools: 'school' }, // old stage ids still accepted by ?stage= / setStage
    bottom: { 'tomb-a': 1, 'tomb-b': 1, 'tomb-c': 1 }, // default if a stage has no bottom map
  },

  // ---- floaters (small hazards between pairs; TUNING radius / motion). shape = engine placeholder painter ----
  floaters: {
    bat:          { radius: 12, motion: 'bobY', amplitude: 30, period: 1.2, shape: 'bat' },
    pumpkin:      { radius: 14, motion: 'sitOnColumn', shape: 'pumpkin' }, // rests on the ground between pairs
    skull:        { radius: 13, motion: 'driftY', amplitude: 45, period: 2.4, shape: 'skull' },
    miniAsteroid: { radius: 13, motion: 'driftY', amplitude: 40, period: 3.0, spin: true, spinSpeed: 1.8, shape: 'rock' }, // ~103 deg/s (Art: 90-120)
    alien:        { radius: 13, motion: 'bobY', amplitude: 30, period: 1.4, shape: 'alien' },
    // v2.0 retro floaters (r 12 to 14 per Tuning)
    'void-float-a': { radius: 13, motion: 'driftY', amplitude: 35, period: 2.8, art: 'cassette', shape: 'cassette' },
    'void-float-b': { radius: 14, motion: 'bobY', amplitude: 28, period: 1.6, art: 'clock', shape: 'clock' },
    'void-float-c': { radius: 12, motion: 'driftY', amplitude: 40, period: 3.2, art: 'phone', shape: 'phone' },
    'void-float-d': { radius: 13, motion: 'bobY', amplitude: 30, period: 2.0, art: 'floppy', shape: 'floppy' }, // Art §15 optional floppy
  },

  // ---- obstacle registry. side: 'top' = hangs (body + cap-bottom), 'bottom' = stands (cap-top + body). Only that cap is loaded.
  // art = file prefix in assets/. shape = placeholder used until (or if) the sprites load. tomb = tombstone sprite variant.
  objects: {
    // --- tops ---
    'lantern-branch': { side: 'top', art: 'obs-graveyard-lantern-branch' },
    'spider':         { side: 'top', art: 'obs-graveyard-spider' },
    'chandelier':     { side: 'top', art: 'obs-church-chandelier' },
    'bats':           { side: 'top', art: 'obs-church-bats' },
    'bell':           { side: 'top', art: 'obs-church-bell' },
    'beehive':        { side: 'top', art: 'obs-countryside-beehive' },
    'branch':         { side: 'top', art: 'obs-countryside-branch' },
    'swing':          { side: 'top', art: 'obs-countryside-swing' },
    'handbell':       { side: 'top', art: 'obs-school-handbell' },
    'kite':           { side: 'top', art: 'obs-school-kite' },
    'lamp':           { side: 'top', art: 'obs-school-lamp' },
    'cradle':         { side: 'top', art: 'obs-city-cradle' },
    'trafficlight':   { side: 'top', art: 'obs-city-trafficlight' },
    'neonsign':       { side: 'top', art: 'obs-city-neonsign' },
    'cranehook':      { side: 'top', art: 'obs-city-cranehook' },
    'satellite':      { side: 'top', art: 'obs-space-satellite', shape: 'satellite' },
    'arm':            { side: 'top', art: 'obs-space-arm' },
    'astronaut':      { side: 'top', art: 'obs-space-astronaut' },
    'ufo':            { side: 'top', art: 'obs-space-ufo', shape: 'ufo' },
    // --- bottoms ---
    'tomb':           { side: 'bottom', tomb: 'random' },
    'tomb-a':         { side: 'bottom', tomb: 'a' },
    'tomb-b':         { side: 'bottom', tomb: 'b' },
    'tomb-c':         { side: 'bottom', tomb: 'c' },
    'coffin':         { side: 'bottom', art: 'obs-common-coffin', shape: 'coffin' },
    'cross':          { side: 'bottom', art: 'obs-common-cross', shape: 'cross' },
    'ivystone':       { side: 'bottom', art: 'obs-church-ivystone' },
    'font':           { side: 'bottom', art: 'obs-church-font' },
    'lychgate':       { side: 'bottom', art: 'obs-church-lychgate' },
    'haybales':       { side: 'bottom', art: 'obs-countryside-haybales' },
    'pumpkinstack':   { side: 'bottom', art: 'obs-countryside-pumpkinstack' },
    'churn':          { side: 'bottom', art: 'obs-countryside-churn' },
    'books':          { side: 'bottom', art: 'obs-school-books' },
    'lockers':        { side: 'bottom', art: 'obs-school-lockers' },
    'globe':          { side: 'bottom', art: 'obs-school-globe' },
    'postbox':        { side: 'bottom', art: 'obs-city-postbox' },
    'phonebox':       { side: 'bottom', art: 'obs-city-phonebox' },
    'hydrant':        { side: 'bottom', art: 'obs-city-hydrant' },
    'moonrock':       { side: 'bottom', art: 'obs-space-moonrock', shape: 'asteroid' },
    'crystals':       { side: 'bottom', art: 'obs-space-crystals' },
    'alienplant':     { side: 'bottom', art: 'obs-space-alienplant' },
    // --- v0.6 The Void (ASSETS.md §14). Loaded only when hitboxes.json lists <id>-cap-bottom (tops) / <id>-cap-top (bottoms).
    'obs-void-typewriter-top':    { side: 'top', art: 'obs-void-typewriter-top' },
    'obs-void-crt-top':           { side: 'top', art: 'obs-void-crt-top' },
    'obs-void-phone-top':         { side: 'top', art: 'obs-void-phone-top' },
    'obs-void-cassette-top':      { side: 'top', art: 'obs-void-cassette-top' },
    'obs-void-gramophone-top':    { side: 'top', art: 'obs-void-gramophone-top' },
    'obs-void-alarm-top':         { side: 'top', art: 'obs-void-alarm-top' },
    'obs-void-typewriter-bottom': { side: 'bottom', art: 'obs-void-typewriter-bottom' },
    'obs-void-crt-bottom':        { side: 'bottom', art: 'obs-void-crt-bottom' },
    'obs-void-phone-bottom':      { side: 'bottom', art: 'obs-void-phone-bottom' },
    'obs-void-cassette-bottom':   { side: 'bottom', art: 'obs-void-cassette-bottom' },
    'obs-void-gramophone-bottom': { side: 'bottom', art: 'obs-void-gramophone-bottom' },
    'obs-void-alarm-bottom':      { side: 'bottom', art: 'obs-void-alarm-bottom' },
  },
  objectAliases: { asteroid: 'moonrock', 'tree-branch': 'branch', 'crane-hook': 'cranehook', // old ids (TUNING <= v1.7)
    // TUNING v2.0 placeholder ids -> Art §14 columns
    'void-top-a': 'obs-void-phone-top', 'void-top-b': 'obs-void-alarm-top', 'void-top-c': 'obs-void-cassette-top',
    'void-bot-a': 'obs-void-typewriter-bottom', 'void-bot-b': 'obs-void-crt-bottom', 'void-bot-c': 'obs-void-gramophone-bottom' },

  // ---- cutscenes (engine types 'rocket' and 'warp'; at most one of each). Both fire on the DISPLAYED score, once per run.
  cutscenes: {
    rocket: {
      type: 'rocket',
      target: 'space',         // the stage the rocket flies to
      trigger: 'score',        // v0.4.2 hotfix (David): launch when the DISPLAYED score reaches atScore
      atScore: 100,            // displayed score (bonuses included); pairs >= stages[target].startAt also launches (QA hooks)
      eventFinishMaxSeconds: 6, // an ACTIVE event at that moment finishes first (max this long), else it's cleared
      cutsceneSeconds: 2.5,    // no collisions, no scoring, pairs on screen cleared, taps ignored
      speedRamps: true,        // speedFor(score) keeps applying
      then: 'transition',      // normal stage breather afterwards
      achievement: 'Lift-off!',
      // Art timeline (ASSETS.md §8), in seconds of a 2.5 s cutscene (scaled if cutsceneSeconds changes)
      timeline: { padIn: 0.5, board: 0.3, ignite: 0.5, liftOff: 0.8, climb: 1.0, arrive: 2.2 },
      padWorld: [80, 420],     // launch pad top-left (bottom on the ground line)
      rocketOnPad: [22, -28],  // rocket offset from pad: x = padX + 70 - 48, y = padY + 112 - 140
      porthole: [48, 66],      // hero tweens into this point of the rocket sprite
      liftOffRise: 60, climbHoldY: 250, climbDrift: 40, zoomSpeed: 600,
      skyPan: [1280, 0],       // bg-launch-sky window top: bottom -> top during the climb
      clouds: { count: 4, speedMin: 500, speedMax: 700, kinds: ['cloudA', 'cloudB', 'cloudC'] },
      smoke: { life: 0.7, spread: 60, rate: 22 },
      shakePx: 2,
      crossfadeAt: 0.88,       // = arrive / 2.5: stage switches to the target and its layers fade in
    },
    // v2.0 (TUNING.md): space -> The Void. Same rule as the launch: DISPLAYED score, once per run, a bonus jumping past
    // atScore still triggers, an active event finishes first.
    warp: {
      type: 'warp',
      atScore: 200,
      cutsceneSeconds: 2.0,     // no collisions, no scoring, pairs cleared, taps ignored
      then: 'transition',
      achievement: 'Into the Void',
      from: 'space', target: 'void',
      eventFinishMaxSeconds: 6, // same as the launch
      // 'stars blur into pastel mist', seconds of a 2.0 s cutscene (scaled if cutsceneSeconds changes)
      timeline: { streak: [0.0, 1.2], mistStart: 1.0, ghostSettle: 1.0 },
      mist: { file: 'bg-trans-space-void-mist-strip.png', folder: '1x', frames: 8, fps: 8, w: 360, h: 640, switchFrame: 3, // 1x strip upscaled
        crossfade: true, normalise: true, swapFadeSeconds: 0,
        veil: { peak: 0.5, halfWidth: 0.2 } },
      warmOnIdle: true,         // decode the target's images one per idle callback once the warp is near
      streakLength: 110, streakCount: 36, mistBlobs: 10, ribbons: 3, // placeholder mist (if Art's strip is missing)
      prewarmScoreAhead: 5,     // queue the target tiles only this close to atScore (or once the warp starts)
      useTransitionTiles: false,
      unloadFromAfterSwap: true,
      deferLayers: ['near'],    // target layers built only after the swap (2x peak 23.5 MB, not 31.7)
      qaStartPairs: 200,        // ?stage=void starts here (QA only; the real entry is the warp)
    },
  },

  // ---- death map (Art: ASSETS.md §11.1, death-map.json). Types are engine death painters (bat, pumpkin, meteor,
  // tombstone, skull, floor, generic); strips replace the placeholder painter when they load.
  deathAnims: {
    file: 'death-{type}-strip.png', goldenFile: 'death-{type}-golden-strip.png',
    frameSize: 128, anchor: [64, 64], fps: 12,
    types: {
      bat:       { frames: 10, seconds: 1.1 },
      pumpkin:   { frames: 8,  seconds: 1.0 },
      meteor:    { frames: 10, seconds: 1.1 },
      tombstone: { frames: 10, seconds: 1.3, loop: [2, 9] },
      skull:     { frames: 10, seconds: 1.0 },
      floor:     { frames: 8,  seconds: 1.0 },
      generic:   { frames: 10, seconds: 1.0, fadeLast: true },
    },
    aliases: { stars: 'tombstone', stone: 'tombstone', poof: 'generic' }, // extra ?death= names
    fallback: 'generic',
    map: {
      'tomb-a': 'tombstone', 'tomb-b': 'tombstone', 'tomb-c': 'tombstone', coffin: 'tombstone', cross: 'tombstone', moonrock: 'tombstone',
      'obs-church-spire': 'tombstone', bell: 'generic', branch: 'generic', 'obs-countryside-scarecrow': 'generic', 'obs-school-chimney': 'tombstone', 'obs-school-clocktower': 'tombstone',
      'obs-city-skyscraper': 'tombstone', cranehook: 'generic', satellite: 'generic', ufo: 'generic', asteroid: 'meteor', 'lantern-branch': 'generic',
      spider: 'generic', chandelier: 'generic', bats: 'bat', beehive: 'generic', swing: 'generic', handbell: 'generic',
      kite: 'generic', lamp: 'generic', cradle: 'generic', trafficlight: 'generic', neonsign: 'generic', arm: 'generic',
      astronaut: 'generic', ivystone: 'tombstone', font: 'tombstone', lychgate: 'tombstone', haybales: 'generic', pumpkinstack: 'pumpkin',
      churn: 'generic', books: 'generic', lockers: 'generic', globe: 'generic', postbox: 'generic', phonebox: 'generic',
      hydrant: 'generic', crystals: 'tombstone', alienplant: 'generic', bat: 'bat', pumpkin: 'pumpkin', skull: 'skull',
      miniAsteroid: 'meteor', alien: 'generic', hearse: 'floor', batSwarm: 'generic', pumpkinRoll: 'generic', sweetShower: 'generic',
      nightBus: 'floor', 'city-pigeon': 'bat', meteorShower: 'meteor', ground: 'floor', ceiling: 'generic', tomb: 'tombstone',
      // v0.6 The Void — death-map.json §14: hanging tops -> generic, hard retro bottoms -> tombstone (see-stars)
      'obs-void-typewriter-top': 'generic', 'obs-void-crt-top': 'generic', 'obs-void-phone-top': 'generic', 'obs-void-cassette-top': 'generic', 'obs-void-gramophone-top': 'generic', 'obs-void-alarm-top': 'generic',
      'obs-void-typewriter-bottom': 'tombstone', 'obs-void-crt-bottom': 'tombstone', 'obs-void-phone-bottom': 'tombstone', 'obs-void-cassette-bottom': 'tombstone', 'obs-void-gramophone-bottom': 'tombstone', 'obs-void-alarm-bottom': 'tombstone',
      'void-float-a': 'generic', 'void-float-b': 'generic', 'void-float-c': 'generic', 'void-float-d': 'generic', invaderWave: 'generic', 'void-invader': 'generic',
    },
    fx: { // ASSETS.md §11.2 (12 fps)
      starsRing: { file: 'fx-stars-ring-strip.png', frames: 6, w: 64, h: 32 },
      smokePuff: { file: 'fx-smoke-puff-strip.png', frames: 4, w: 48, h: 48 },
      sparklePoof: { file: 'fx-sparkle-poof-strip.png', frames: 5, w: 96, h: 96 },
      bonk: { file: 'fx-bonk-strip.png', frames: 3, w: 64, h: 64 },
    },
    colors: { soot: '#2b2230', smoke: 'rgba(80, 70, 90, 0.55)', star: '#ffe08a', bat: '#5a4a78', spook: '#c9b3f0' },
  },

  // ---- stage-transition art (ASSETS.md §11.3). {stage} = Art's stage id, {n} = frame / stage number. Missing -> placeholder.
  transitionArt: {
    banner: 'ui-banner-{stage}.png',          // pre-lettered (Capriola), preferred
    bannerStageBlank: 'ui-banner-{stage}-blank.png', bannerBlank: 'ui-banner-blank.png', // + the stage name drawn on top
    burst: { file: 'fx-burst-{stage}-strip.png', frames: 6, w: 160, h: 160 },
    swoosh: { file: 'fx-swoosh-strip.png', frames: 6, w: 240, h: 64 }, // frame 0 is empty on purpose
    badge: 'ui-stage-badge-{n}.png', badgeBlank: 'ui-stage-badge-blank.png',
  },

  // ---- score card (ASSETS.md §12): frame per stage (stage id 'school' -> file 'schools'); no-stage file = generic night sky
  share: {
    title: 'Ghost Game',
    template: '{name} scored {score} in Ghost Game, reaching {stage}! Can you beat it?',
    fileName: 'ghost-game-score.png',
    frameFile: 'assets/ui-scorecard-frame{stage}@2x.png', frameStageFile: { school: 'schools' },
    frameGeneric: [],       // list stages here to force the generic frame
    layout: 'assets/scorecard-layout.json',
  },

  // ---- art files + sheets (assets/ASSETS.md). Sizes are 1x sprite px. Loaded only when hitboxes.json lists them (no 404s).
  assets: {
    pngDir: 'assets/png',
    hitboxes: 'assets/hitboxes.json',
    columns: {
      // file templates per object id (tombs: tomb-a-body.png, ...)
      files: { body: '{art}-body.png', capTop: '{art}-cap-top.png', capBottom: '{art}-cap-bottom.png' }, // {art} = objects[id].art || id
      alwaysLoad: ['tomb-a', 'tomb-b', 'tomb-c'], // others load only if hitboxes.json lists the cap their side needs
      spriteWidth: 80,
      bodyHeight: 64,
      capHeight: 80,
      drawScale: 1,
      hitboxX: 8,
      // fallback gap edges if hitboxes.json is missing (otherwise computed from it)
      floorEdge: { 'tomb-a': 10, 'tomb-b': 5, 'tomb-c': 31 },
      ceilEdge:  { 'tomb-a': 70, 'tomb-b': 75, 'tomb-c': 49 },
    },
    // Sprite sheets (horizontal strips). Loaded only when the hitboxes.json path in `json` exists. frames = strip indices in play order.
    // Names used by engine features: launchpad/rocketIdle/rocketThrust/flame/smoke/launchSky/cloud* (rocket cutscene),
    // warning (event warning icon), fogBack/fogFront, birdPerch/birdFly, bikeMint/bikePink, star, starfield (ambient kinds).
    sheets: {
      bat:          { file: 'obs-common-bat-flap-strip.png', w: 48, h: 48, frames: [0, 1, 2, 1], fps: 12, json: ['hazards', 'bat'] },
      pumpkin:      { file: 'obs-common-pumpkin.png', w: 40, h: 40, frames: [0], fps: 0, json: ['hazards', 'pumpkin'] },
      skull:        { file: 'obs-common-skull-strip.png', w: 40, h: 40, frames: [0, 1], fps: 3, json: ['hazards', 'skull'] },
      miniAsteroid: { file: 'obs-space-miniasteroid.png', w: 40, h: 40, frames: [0], fps: 0, json: ['hazards', 'miniAsteroid'] },
      alien:        { file: 'obs-space-alien-strip.png', w: 40, h: 40, frames: [0, 1], fps: 3, json: ['hazards', 'alien'] },
      goldenPickup: { file: 'pickup-golden-ghost-strip.png', w: 56, h: 56, frames: [0, 1, 2, 1], fps: 6, json: ['pickups', 'golden-ghost'] },
      goldenPickupSpace: { file: 'pickup-golden-ghost-space-strip.png', w: 56, h: 56, frames: [0, 1, 2, 1], fps: 6, json: ['pickups', 'golden-ghost-space'] },
      hearse:       { file: 'event-graveyard-hearse-strip.png', w: 160, h: 64, frames: [0, 1], fps: 10, json: ['events', 'graveyard-hearse'] },
      meteor:       { file: 'event-space-meteor-strip.png', w: 72, h: 48, frames: [0, 1], fps: 10, json: ['events', 'space-meteor'] },
      launchpad:    { file: 'prop-city-launchpad.png', w: 200, h: 140, frames: [0], fps: 0, json: ['cutscene'] },
      rocketIdle:   { file: 'cut-rocket-idle-strip.png', w: 96, h: 148, frames: [0, 1], fps: 4, json: ['cutscene'] },
      rocketThrust: { file: 'cut-rocket-thrust-strip.png', w: 96, h: 148, frames: [0, 1], fps: 12, json: ['cutscene'] },
      flame:        { file: 'cut-rocket-flame-strip.png', w: 48, h: 80, frames: [0, 1, 2, 1], fps: 15, json: ['cutscene'] },
      smoke:        { file: 'cut-smoke-puff-strip.png', w: 64, h: 64, frames: [0, 1, 2], fps: 0, json: ['cutscene'] },
      cloudA:       { file: 'cut-cloud-a.png', w: 160, h: 64, frames: [0], fps: 0, json: ['cutscene'] },
      cloudB:       { file: 'cut-cloud-b.png', w: 160, h: 64, frames: [0], fps: 0, json: ['cutscene'] },
      cloudC:       { file: 'cut-cloud-c.png', w: 160, h: 64, frames: [0], fps: 0, json: ['cutscene'] },
      launchSky:    { file: 'bg-launch-sky.png', w: 360, h: 1920, frames: [0], fps: 0, json: ['cutscene'] },
      warning:      { file: 'ui-event-warning-strip.png', w: 40, h: 40, frames: [0, 1], fps: 4, json: ['events', 'warning'] },
      fogBack:      { file: 'amb-graveyard-fog-back.png', w: 360, h: 120, frames: [0], fps: 0, json: ['ambient'], parallax: 0.3 },
      fogFront:     { file: 'amb-graveyard-fog-front.png', w: 360, h: 80, frames: [0], fps: 0, json: ['ambient'], parallax: 0.6 },
      birdPerch:    { file: 'amb-church-bird-perch.png', w: 24, h: 24, frames: [0], fps: 0, json: ['ambient'] },
      birdFly:      { file: 'amb-church-bird-fly-strip.png', w: 24, h: 24, frames: [0, 1, 2, 1], fps: 12, json: ['ambient'] },
      bikeMint:     { file: 'amb-school-bike-mint.png', w: 72, h: 48, frames: [0], fps: 0, json: ['ambient'] },
      bikePink:     { file: 'amb-school-bike-pink.png', w: 72, h: 48, frames: [0], fps: 0, json: ['ambient'] },
      rain:         { file: 'amb-city-rain-0.png', w: 128, h: 128, frames: [0], fps: 0, json: ['ambient'] },
      star:         { file: 'amb-space-star-strip.png', w: 16, h: 16, frames: [0, 1, 2, 1], fps: 4, json: ['ambient'] },
      starfield:    { file: 'amb-space-starfield.png', w: 180, h: 180, frames: [0], fps: 0, json: ['ambient'], parallax: 0.1 },
      // v0.6 Void floaters / invaders (Art §15.1: 4-frame wobble strips, hit circle fixed at (20,20))
      'void-float-a': { file: 'obs-void-float-cassette-strip.png', w: 40, h: 40, frames: [0, 1, 2, 3], fps: 6, json: ['hazards', 'void-float-a'] },
      'void-float-b': { file: 'obs-void-float-clock-strip.png',    w: 40, h: 40, frames: [0, 1, 2, 3], fps: 6, json: ['hazards', 'void-float-b'] },
      'void-float-c': { file: 'obs-void-float-phone-strip.png',    w: 40, h: 40, frames: [0, 1, 2, 3], fps: 6, json: ['hazards', 'void-float-c'] },
      'void-float-d': { file: 'obs-void-float-floppy-strip.png',   w: 40, h: 40, frames: [0, 1, 2, 3], fps: 6, json: ['hazards', 'void-float-d'] },
      // Art §15.2: invader types a (mint), b (pink), c (lilac) share size + hitbox; pop + Void warning icon are decorative
      invader:      { file: 'event-void-invader-strip.png',   w: 40, h: 40, frames: [0, 1], fps: 4, json: ['events', 'void-invader'] },
      invaderB:     { file: 'event-void-invader-b-strip.png', w: 40, h: 40, frames: [0, 1], fps: 4, json: ['events', 'void-invader'] },
      invaderC:     { file: 'event-void-invader-c-strip.png', w: 40, h: 40, frames: [0, 1], fps: 4, json: ['events', 'void-invader'] },
      invaderPop:   { file: 'event-void-invader-pop-strip.png', w: 64, h: 64, frames: [0, 1, 2, 3, 4, 5], fps: 12, json: ['events', 'void-invader-pop'] },
      warningVoid:  { file: 'ui-event-warning-void-strip.png', w: 40, h: 40, frames: [0, 1], fps: 4, json: ['events', 'warning-void'] },
    },
    // Void-only v0.5-style art (banner, burst, badge 7, score-card frame) is requested only once Art's Void set exists
    // (a hitboxes.json key starting with detectPrefix, or 'void' in backgrounds.stages): no 404s.
    voidArt: { stage: 'void', detectPrefix: 'obs-void-', transitions: ['space-void'] },
    backgrounds: {
      load: true,            // only stages listed in hitboxes.json backgrounds.stages are fetched (no 404s)
      file: 'bg-{stage}-{layer}.png', // Art: 720x640 world px tiles in png/{1x,2x}/, scroll horizontally
      tileWidth: 720,
      layers: ['far', 'mid', 'near'],
      parallax: { far: 0.1, mid: 0.3, near: 0.6 },              // Art's scroll factors (per-stage: stages[].parallax)
      transFile: 'bg-trans-{from}-{to}-{layer}.png', // used at each layer's next tile edge (ASSETS.md §7a)
      transMaxSeconds: 3,    // mid/far: use the transition tile only if the next edge is this close...
      fadeSeconds: 1.5,      // ...otherwise crossfade outgoing -> incoming tiles over this long
      alwaysTransLayers: ['near'],
      // Art §14.2 memory-lite Void, drawn from hitboxes.json backgrounds.void (stacks of parts per 720 slot, no layer cache).
      // lite1xOnHiDpi: these parts load from png/1x on 2x screens (soft art; 2x decoded set 8.5 -> ~3.7 MiB).
      voidParts: { enabled: true, stage: 'void', glints: true, smoothing: true,
        lite1xOnHiDpi: ['bg-void-mid-upper.png', 'bg-void-mid-lower.png', 'bg-void-far-stars.png'] },
      artStageIds: { school: 'schools' }, // Art's bg files and hitboxes.json backgrounds still say 'schools'
    },
  },

  // ---- UI accents + placeholder colours (merged over the global CONFIG.colors) ----
  colors: {
    accent: '#ffb3c9', sparkle: '#fff3b0', warning: '#ffcf5a', bannerEdge: 'rgba(255, 201, 218, 0.85)',
    ghostBody: '#fbf7ff', ghostShade: '#d9c9f5', ghostGolden: '#ffe08a', ghostGoldenShade: '#f5b942',
  },
  ui: { goldenText: 'Golden ghost! x2 points', medalNames: { pumpkin: 'Pumpkin medal', gold: 'Gold medal', silver: 'Silver medal', bronze: 'Bronze medal' } },

  // ---- audio slots (reserved: the engine has no audio yet; null = silent) ----
  audio: { music: null, flap: null, score: null, hit: null, cutscene: null, special: null },
});
