// =============================================================================
// Move Cosy — the version list (loaded by index.html BEFORE game.js, so the picker works offline).
// status: 'ready' = playable, 'soon' = shown as "coming soon" (never loaded), 'test' = debug builds only.
// months: the season window (local month, 1-12). file: the one data file loaded when that pack is chosen.
// =============================================================================
window.MOVE_COSY_PACKS = {
  fallback: 'ghost',
  packs: [
    { id: 'ghost',    name: 'Ghost',    title: 'Ghost Flap',          months: [9, 10, 11], status: 'ready', file: 'packs/ghost/pack.js' },
    { id: 'santa',    name: 'Santa',    title: "Santa's Rocket Run",  months: [12, 1, 2],  status: 'ready', file: 'packs/santa/pack.js' }, // v0.8.0
    { id: 'bunny',    name: 'Bunny',    title: 'Easter Bunny',        months: [3, 4, 5],   status: 'soon' },
    { id: 'seagull',  name: 'Seagull',  title: 'Seagull Beach Tour',  months: [6, 7, 8],   status: 'soon' },
    { id: 'test',     name: 'Test',     title: 'Test Pack',           months: [],          status: 'test', file: 'packs/test/pack.js' },
  ],
};
