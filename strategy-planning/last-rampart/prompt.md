# Benchmark Specification: Last Rampart: Wave Defense Strategist

Generate a complete, single-file `index.html` application containing a self-playing wave-defense game: a fortified base at the end of a winding road is attacked by endless, ever-stronger waves of six enemy types, and **your own strategy code** decides where to build five kinds of turrets, when to upgrade or sell them, and which enemy each turret shoots. The game rules are fixed exactly below and the outcome is decided by your strategy alone: the better it plays, the more waves the base survives. The page plays a fixed 100-second replay of your strategy on seed `42`. Write the completed deliverable directly to `./index.html` in the current working directory, and do not leave auxiliary files in the working directory.

**How this run is scored.** Two separate results:
1. **Pass / fail:** the page must meet the shell contract (sections 3 to 5) and its simulation must reproduce the rules exactly (section 2, checked by event-log hash).
2. **Strategy score:** your strategy is re-run by the grader in its own reference engine on **five undisclosed seeds**, each until the base falls (at most 300 waves). Your score is the mean number of waves held. Seed `42` is not one of the five. A strategy tuned only to seed `42` will score poorly; make it play well on any seed.

### Mandatory Architecture & Constraints (Universal Standard)
- **Format & Target File:** Exactly one single `.html` file written to `./index.html` containing all HTML, CSS inside `<style>`, and JavaScript inside `<script>`.
- **Permitted External Resource (Single Exception Only):**
  Exactly one external network resource is permitted—the pinned Three.js `r128` global UMD script:
  `<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>`
  Do NOT load any other external scripts, `<script type="importmap">`, `esm.sh`, 3D models (`.gltf`, `.glb`, `.obj`), textures/images, HDR/EXR environment maps, web fonts (`@import` or `<link>`), audio files, or CSS files. Do NOT make any `fetch()`, `XMLHttpRequest`, `WebSocket`, or external `THREE.TextureLoader` requests at runtime.
  All procedural textures, sprites, materials, and geometry must be generated dynamically in memory (keep any 2D helper canvases detached in memory; never append helper canvases to the DOM). Because this is the `r128` global UMD build, configure color output with `renderer.outputEncoding = THREE.sRGBEncoding;` (do NOT reference `THREE.SRGBColorSpace`).
- **Three separate inline scripts (graded separately):**
  1. `<script id="rampart-strategy">` defines exactly one global function `createStrategy()` that returns a fresh strategy object `{ plan(state), target(turret, candidates) }` (section 2.6). It must be self-contained: no access to `window`, `document`, `THREE`, other scripts, `Math.random`, `Date` or `performance`, and no state shared between two objects it returns. The grader copies this script's text into a clean page and calls `createStrategy()` once per simulated game.
  2. `<script id="rampart-sim">` defines exactly one global function `rampartSimulate(createStrategy, seed, maxTicks)` that plays the rules of section 2 and returns `{ score, fallTick, log, hash }` (section 2.8). It must not touch the DOM, `THREE` or audio. The grader copies this script's text into a clean page and runs it with your strategy.
  3. A main `<script>` (rendering, playback, audio) that builds the replay from `rampartSimulate(createStrategy, 42, 2020)` plus whatever per-tick state it records, and never re-implements the rules differently from `rampart-sim`.
- **Deterministic Replay & Frame-Exact Scrubbing (Seed `42`):** The game runs on integer ticks at 20 ticks per second. Precompute the whole replay (ticks `0` to `2019`) at load. The displayed state at any `simTime` in `[0, 100]` is tick `k = floor(simTime * 20)` interpolated toward tick `k + 1` by the fractional remainder for smooth motion, so forward playback, backward scrubbing, repeated resets, and 60Hz vs. 120Hz displays produce identical visual states at any given `simTime`. Use a separate seeded generator (seed `42`, never `Math.random()`) for any purely visual randomness (debris, sparks, ground detail). Drive all visual/shader animations from `simTime`, never from frame counters or `Date.now()`.
- **Local Execution:** Opening `./index.html` directly via `file://` in a desktop browser (with internet access for the single pinned Three.js CDN tag) must run cleanly with zero CORS or module errors.

---

### 1. Scene Composition & Camera
- **Backdrop & Stage Canvas:** Mount WebGL strictly onto the canonical `<canvas id="stage"></canvas>` element using `new THREE.WebGLRenderer({ canvas: document.getElementById('stage'), antialias: true, alpha: true })` over the CSS studio radial gradient (`#161922` center fading to `#090a0f` at edges).
- **Renderer DPR & Resize:** Set `renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));` and `renderer.setSize(window.innerWidth, window.innerHeight, false);`. Update camera projection and renderer size cleanly on `window` `resize`.
- **Board & camera:** The board is the 24 × 14 tile grid of section 2.1, one world unit per tile, lying on the `XZ` plane with tile `(x, y)` centred at world `(x + 0.5, 0, y + 0.5)`. Use one fixed `THREE.PerspectiveCamera` (near `0.1`, far `500`), looking down at the board's centre from about 55° above the horizon, with no camera motion except a short trauma shake (below). Frame it so the **whole board, with a margin of at least half a tile, stays inside the view at `16:9` and at `1280×650`** (the size of one panel in a four-way split screen), and so nothing important sits in the bottom 90 px (the dock). Recompute the framing on resize.
- **Readable at quarter size (must be followed):** This replay is shown in a 2 × 2 split screen at `1280×650` per panel. Every enemy type and turret type must be told apart by **silhouette and colour** at that size; avoid fine detail that only reads full-screen. Use these colour families: grunt grey-green, brute dark iron with orange plates, runner yellow, wisp cyan and glowing (floats 0.8 tiles above the ground with a shadow), splitter purple, splitling small purple, mender white with a soft green halo; turrets bolt steel-blue, cannon bronze, frost ice-white, lance crimson, flak teal. Show turret tier with 1 to 3 bright pips or rings on the turret.
- **World:** An original fortified setting with no names, logos or characters from any existing game: a dark stone road along the ground path, a faint glowing air lane along the flyer route, 16 build pads (low stone platforms) at the slots, rough terrain elsewhere, and the base (a walled keep about 1.5 tiles across) at the road's end, tile `(23, 11)`. Lighting is dusk with a warm key light and shadows; `renderer.toneMapping = THREE.ACESFilmicToneMapping`.
- **Combat visuals (all functions of the recorded tick state and `simTime`):**
  - Enemies move smoothly along their routes, face their direction of travel, and show a small health bar above them. Slowed enemies are tinted frost-blue.
  - Each shot is a visible effect from the turret to its target that lasts at most `0.15` s: bolts are thin tracers, cannon shells arc and burst in a ring the size of the splash radius, frost is a pale beam, lance is a thick crimson beam with a flash, flak bursts in a teal ring in the air. Kills pop into small debris (seeded, ballistic, closed-form in time since the kill). A mender's heal is a green pulse ring of the heal radius. A splitter's death bursts into its three splitlings.
  - Builds, upgrades and sells at each wave start get a short rising sparkle, a ring pulse, or a collapse into rubble.
  - **Leaks:** each enemy that reaches the base flashes the keep red and knocks one visible chunk off its walls; the keep visibly crumbles as base HP falls.
  - **Fall:** at the fall tick the keep collapses in a burst of debris and a large shockwave ring (trauma `1.0`), everything freezes, and over the next `1.0` s the scene desaturates to near-greyscale. Hold that state until `simTime = 100`.
  - **Trauma shake:** leaks add `0.3` trauma and the fall adds `1.0`; trauma decays linearly at `1.0` per second and is clamped to `[0, 1]`; the shake offset is `trauma²` times smooth seeded noise of `simTime` (up to `0.25` tiles), closed-form, so scrubbing gives the identical frame.

---

### 2. Game Rules (Must Be Followed Exactly)
All quantities are **integers**. Positions are in centi-tiles (100 per tile), measured from the board's top-left corner, so the centre of tile `(x, y)` is `(100x + 50, 100y + 50)`. Time is in ticks (20 per second). Every division below is integer division rounded down (`Math.floor`). Distances are compared squared (`dx*dx + dy*dy <= r*r`), never with square roots.

#### 2.1 Board
- **Ground path** (axis-aligned polyline through tile centres): `(0,2) → (6,2) → (6,10) → (12,10) → (12,3) → (18,3) → (18,11) → (23,11)`. Its length is `4600` centi-tiles.
- **Air lane** (flyers only): `(0,6) → (21,6) → (21,11) → (23,11)`, length `2600`.
- An enemy's position is the point at distance `progress` along its route from the first point (`progress` starts at `0`); its `remaining` distance is route length minus `progress`.
- **Slots** (index: tile): `0:(3,3) 1:(5,5) 2:(7,4) 3:(7,8) 4:(9,9) 5:(10,5) 6:(11,8) 7:(13,8) 8:(14,5) 9:(15,2) 10:(16,7) 11:(17,4) 12:(19,8) 13:(20,10) 14:(22,9) 15:(3,7)`. A turret sits at its slot's tile centre.

#### 2.2 Turrets
| Type | Cost | Damage | Period (ticks) | Range | Splash radius | Slow (ticks) | Pierce | Hits ground | Hits air |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: | :---: |
| `bolt` | 50 | 26 | 8 | 300 | 0 | 0 | no | yes | yes |
| `cannon` | 90 | 60 | 24 | 260 | 90 | 0 | no | yes | no |
| `frost` | 70 | 10 | 12 | 240 | 0 | 30 | no | yes | yes |
| `lance` | 120 | 180 | 36 | 360 | 0 | 0 | yes | yes | no |
| `flak` | 80 | 40 | 10 | 320 | 70 | 0 | no | no | yes |

- **Tiers 1 to 3.** Upgrading from tier 1 to 2 costs the base cost; from 2 to 3 costs twice the base cost. Each tier above 1 multiplies damage by `16/10` (rounded down at each step: tier-2 damage `floor(d*16/10)`, tier-3 `floor(tier2*16/10)`) and adds `30` range. Period, splash and slow do not change.
- **Selling** refunds `floor(70% of everything spent on that turret)` and frees the slot at once.
- **Damage:** a hit deals `damage − armour` (at least `1`); a pierce turret ignores armour. A turret with slow sets each enemy it hits to `slow` ticks of slow (resetting, not adding). A slowed enemy moves `floor(speed * 60 / 100)` per tick.
- **Splash:** a splash turret damages every enemy it can hit (right domain, alive) within the splash radius of the target's position, including the target.

#### 2.3 Enemies
| Type | Base HP | Speed (centi-tiles/tick) | Armour | Bounty | Leak damage | Route | First wave | Weight |
| :--- | ---: | ---: | :--- | ---: | ---: | :--- | ---: | ---: |
| `grunt` | 60 | 10 | `floor(wave/4)` | 4 | 1 | ground | 1 | 10 |
| `runner` | 40 | 20 | 0 | 4 | 1 | ground | 2 | 4 |
| `wisp` | 50 | 12 | 0 | 6 | 2 | air | 3 | 3 |
| `brute` | 150 | 6 | `6 + wave` | 9 | 3 | ground | 4 | 3 |
| `splitter` | 90 | 8 | 0 | 6 | 2 | ground | 6 | 2 |
| `mender` | 70 | 8 | 0 | 7 | 2 | ground | 8 | 1 |
| `splitling` | see below | 12 | 0 | 1 | 1 | ground | (from splitters) | – |

- **HP scaling:** an enemy of wave `w` has `maxHp = floor(baseHp * m(w) / 1000)`, where `m(1) = 1000` and `m(w) = floor(m(w−1) * 108 / 100)`. `wave` in the armour column is the enemy's own wave.
- **Splitter:** when killed, spawns 3 `splitling`s at its `progress`, each with `maxHp = max(1, floor(splitter maxHp / 4))`, the splitter's wave, and new ids.
- **Mender:** every enemy has an `age` that counts ticks since it spawned. When a mender's `age` reaches a multiple of `20`, every enemy within `150` of it (itself included) is healed by `floor(maxHp * 8 / 100)`, up to its `maxHp`.

#### 2.4 Waves & economy
- The base starts with `10` HP; the player starts with `250` gold.
- Wave `w` starts at tick `20 + 40 * (w − 1)` and contains `4 + floor(3w / 5)` enemies, which spawn at the wave's start tick plus `4 * i` for the `i`-th enemy (`i` from `0`). Waves overlap once a wave holds more than 10 enemies.
- **Composition:** one generator per game, Mulberry32 seeded with the game seed, returning **unsigned 32-bit integers** (exactly this code):
  ```js
  function mulberry32(a) { return function () {
    a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return (t ^ (t >>> 14)) >>> 0; }; }
  ```
  Waves are generated in order `1, 2, 3, …`, each enemy by one draw: take the types whose first wave is `<= w` in the table order above (grunt, runner, wisp, brute, splitter, mender), let `r = draw % (sum of their weights)`, and walk the list subtracting weights until `r` falls inside one. Wave `w + 1` is generated at the start of wave `w` (so the strategy can preview it).
- At each wave start, before anything else that tick: `gold += min(50, floor(gold * 5 / 100)) + 10 + 2 * w` (interest on the gold held before this payment, plus the wave bonus). Each kill adds the enemy's bounty.

#### 2.5 Tick order (each tick, in this order)
1. **Wave start** (if this tick starts wave `w`): pay interest and bonus; generate the next wave; call `plan(state)` once and apply its actions in order (2.6); queue wave `w`'s spawns. Keep the spawn queue ordered by tick, then wave, then index within the wave.
2. **Spawn** every queued enemy due this tick, assigning ids `1, 2, 3, …` in spawn order.
3. **Move** every enemy in ascending id order. An enemy whose `progress` reaches its route length leaks: the base loses its leak damage, the enemy is removed, and if base HP is now `<= 0` the base **falls**: the game ends immediately at this tick (no further steps or enemies are processed).
4. **Age & heal:** in ascending id order, increase each enemy's `age` by `1`; each mender whose `age` is now a multiple of `20` heals (2.3).
5. **Turrets fire** in ascending slot order. A turret's cooldown starts at `0` when built. Each tick: if cooldown `> 0`, subtract `1`; if it is still `> 0`, skip. Otherwise its **candidates** are the living enemies it can hit within range, in ascending id order; with none, it waits (cooldown stays `0`). With candidates it picks a target (`target()` if provided and it returns a candidate's id; otherwise the candidate with the smallest `remaining`, the lowest id on ties), deals damage (and splash), sets cooldown to its period, then removes every enemy with HP `<= 0` in ascending id order, paying bounty and spawning splitlings (which take part in the rest of this tick).
6. **Slow timers:** every enemy with slow `> 0` loses `1`.

The game also ends without a fall at `maxTicks`.

#### 2.6 Strategy API
`createStrategy()` returns an object with:
- `plan(state)` (required), called at every wave start. Returns an array of actions, applied in order; only the first `32` count; invalid or unaffordable actions are skipped silently:
  - `{ op: "build", slot, type }`: empty slot and enough gold.
  - `{ op: "upgrade", slot }`: a turret below tier 3 and enough gold.
  - `{ op: "sell", slot }`: a turret on that slot.
- `target(turret, candidates)` (optional), called each time a turret fires. Return the `id` of one of the candidates; anything else uses the default target.

`state` (a fresh copy each call; changing it has no effect) is:
```js
{ tick, wave, gold, baseHp,
  slots: [ { slot, x, y, turret: null | { type, tier, spent } } ],   // all 16, by index
  enemies: [ EnemyView ],                                              // living enemies, ascending id
  nextWave: [ "grunt", "brute", ... ] }                                // composition of wave + 1
```
`EnemyView` is `{ id, type, hp, maxHp, x, y, air, armor, speed, slowed, remaining }` (`air` is `1` or `0`). `turret` passed to `target()` is `{ slot, type, tier, x, y, range }`; `candidates` is an array of `EnemyView` in ascending id order.

The grader stops a seed and scores it `0` if your strategy throws, or if the whole game (up to 300 waves) takes more than 10 s of CPU in desktop Chrome.

#### 2.7 Score
`score = (endTick − 20) / 40`, rounded to 2 decimals, where `endTick` is the fall tick, or `maxTicks` if the base never fell (waves held, counted from the first wave).

#### 2.8 Event log & hash
`rampartSimulate` records, in the order they happen, `[tick, code, a, b]` entries:
| Code | When | `a` | `b` |
| :--- | :--- | :--- | :--- |
| `"B"` | turret built | slot | type index (`bolt 0, cannon 1, frost 2, lance 3, flak 4`) |
| `"U"` | turret upgraded | slot | new tier |
| `"S"` | turret sold | slot | `0` |
| `"L"` | enemy leaked | enemy id | base HP after the leak |
| `"K"` | enemy killed | enemy id | slot of the turret that fired |
| `"F"` | base fell (last entry) | current wave | `0` |

`hash` is the 32-bit FNV-1a of `JSON.stringify(log)` over its UTF-16 code units (offset `0x811c9dc5`, prime `0x01000193`, via `Math.imul`), as 8 lowercase hex digits. It returns `{ score, fallTick, log, hash }`, with `fallTick = −1` if the base never fell.

**Self-check vectors (your `rampart-sim` must reproduce these exactly):**
- *A.* `createStrategy = () => ({ plan(s) { const a = []; let g = s.gold; for (const sl of s.slots) if (!sl.turret && g >= 50) { a.push({ op: "build", slot: sl.slot, type: "bolt" }); g -= 50; } return a; } })`, seed `42`, `maxTicks = 12020`: `score 25.38`, `fallTick 1035`, `166` log entries, `hash "82a5353d"`. The first entries are `[20,"B",0,0]`, `[20,"B",1,0]`, … `[20,"B",4,0]`, `[37,"K",1,0]`.
- *B.* a strategy whose `plan` returns `[{op:"build",slot:3,type:"cannon"},{op:"build",slot:6,type:"frost"}]` at wave 1, `[{op:"upgrade",slot:3},{op:"build",slot:12,type:"flak"}]` at wave 3, `[{op:"build",slot:8,type:"lance"},{op:"sell",slot:6}]` at wave 6 and `[]` otherwise, seed `7`, `maxTicks = 12020`: `score 10.93`, `fallTick 457`, `48` entries, `hash "2e8858d7"`.

**Pass check:** the grader runs your `rampart-sim` with your strategy on seed `42` and on one undisclosed seed, and compares the hashes with its reference engine. Any mismatch fails the run.

---

### 3. Timeline, State Machine & Playback Controls
Define total active duration `const DURATION = 100;` (in seconds) and implement the following exact 5-state playback state machine (`COUNTDOWN`, `PLAYING`, `PAUSED`, `REFIRE_HOLD`, `ENDED`):

1. **Initial Launch (`COUNTDOWN` State — Exactly 3.000s Wall-Clock):**
   - Start `COUNTDOWN` on the first `requestAnimationFrame` callback after the initial resting scene (`simTime = 0.000`) has rendered (`countdownElapsed = 0`), advancing `countdownElapsed` by clamped wall `dt = Math.min(rawDt, 0.1)` each frame so cold-start shader compilation never skips `"3"`.
   - While `0.000 <= countdownElapsed < 3.000` (measured in real wall-clock seconds, **unaffected** by the speed selector):
     - `0.000 <= countdownElapsed < 1.000`: `#countdown` is visible (`display: block`) with text `"3"`.
     - `1.000 <= countdownElapsed < 2.000`: `#countdown` is visible with text `"2"`.
     - `2.000 <= countdownElapsed < 3.000`: `#countdown` is visible with text `"1"`.
     - `simTime` remains `0.000` and `#scrubber.value` remains `"0"`.
   - At `countdownElapsed >= 3.000`: immediately hide `#countdown` (`display: none` and text `""`), transition to `PLAYING`, and advance `simTime` from `0.000` at rate `dt * playbackSpeed`.
2. **Active Playback (`PLAYING` State) & Endpoint Hold (`ENDED` State):**
   - During `PLAYING`, advance `simTime = Math.min(DURATION, simTime + dt * playbackSpeed)` each frame (clamping per-frame wall `dt` to `<= 0.1` s so background tab switches do not jump the simulation), update `#scrubber.value = simTime.toFixed(3)`, and render `simTime`.
   - When `simTime >= DURATION`, clamp `simTime = DURATION`, set `#scrubber.value = DURATION.toFixed(3)`, render the final state, and transition to `ENDED` (holding the final frame cleanly; `#icon-pause` hides, `#icon-play` shows, and `#btn-toggle` sets `aria-label="Play"`).
3. **Play / Pause Toggle (`#btn-toggle`):**
   - If clicked during `PLAYING`: transition to `PAUSED` (freeze `simTime`, show `#icon-play`, hide `#icon-pause`, set `aria-label="Play"`).
   - If clicked during `COUNTDOWN` or `REFIRE_HOLD`: cancel the countdown/hold immediately, hide `#countdown` (`display: none`), keep `simTime = 0.000`, and transition to `PAUSED`.
   - If clicked during `PAUSED`: transition to `PLAYING` from current `simTime` (show `#icon-pause`, hide `#icon-play`, set `aria-label="Pause"`).
   - If clicked during `ENDED`: reset `simTime = 0.000` and transition immediately to `PLAYING` (with `#countdown` hidden).
4. **Speed Selector Pills (`.speed-pill`):**
   - Clicking a pill sets `playbackSpeed` (`0.25`, `0.5`, `1.0`, or `2.0`), moves `.is-active` and `aria-checked="true"` exclusively to that pill (setting `aria-checked="false"` on the other three), and persists `playbackSpeed` across `Re-fire` and scrubbing.
5. **Scrubbing Slider (`#scrubber`):**
   - Any `input` event on `#scrubber` immediately cancels `COUNTDOWN` or `REFIRE_HOLD` (hiding `#countdown` via `display: none`), sets `simTime = parseFloat(scrubber.value)`, renders `simTime` deterministically, and transitions to `PAUSED` while the user scrubs (or remains `PAUSED` until `#btn-toggle` or `#btn-refire` is pressed).
6. **Silent Re-Fire (`#btn-refire` -> `REFIRE_HOLD` State):**
   - Clicking `#btn-refire` from ANY state cancels any active timers, hides `#countdown` (`display: none`, text `""`), resets `simTime = 0.000` and `#scrubber.value = "0"`, renders the exact initial resting state immediately, shows `#icon-pause` (`aria-label="Pause"`), and enters `REFIRE_HOLD` (`holdElapsed = 0`).
   - `#countdown` MUST remain completely hidden throughout `REFIRE_HOLD`. After **1.000 second** of wall-clock hold (`holdElapsed >= 1.000`, unaffected by `playbackSpeed`), transition automatically to `PLAYING`.

---

### 4. Canonical Minimalist Bottom Dock (UI) & Clean Viewport Contract
To guarantee pixel-accurate alignment in side-by-side multi-model video compositing at `1920x1080`, use the **exact** DOM structure, IDs, attributes, and CSS rules below without adding extra elements, labels, readouts, or wrappers:

#### Canonical `<body>` Markup:
```html
<canvas id="stage"></canvas>
<div id="countdown" aria-hidden="true">3</div>

<div id="dock" role="toolbar" aria-label="Simulation Controls">
  <button id="btn-refire" type="button" aria-label="Re-fire" title="Re-fire">
    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.19"/>
    </svg>
    <span>Re-fire</span>
  </button>
  <span class="dock-sep" aria-hidden="true"></span>
  <button id="btn-toggle" type="button" aria-label="Pause" title="Play / Pause">
    <svg id="icon-pause" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true">
      <rect x="6" y="4" width="4" height="16" rx="1"/>
      <rect x="14" y="4" width="4" height="16" rx="1"/>
    </svg>
    <svg id="icon-play" viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true" style="display:none;">
      <path d="M8 5v14l11-7z"/>
    </svg>
  </button>
  <span class="dock-sep" aria-hidden="true"></span>
  <div id="speed-group" role="radiogroup" aria-label="Playback Speed">
    <button class="speed-pill" type="button" role="radio" aria-checked="false" data-speed="0.25">0.25×</button>
    <button class="speed-pill" type="button" role="radio" aria-checked="false" data-speed="0.5">0.5×</button>
    <button class="speed-pill is-active" type="button" role="radio" aria-checked="true" data-speed="1.0">1.0×</button>
    <button class="speed-pill" type="button" role="radio" aria-checked="false" data-speed="2.0">2.0×</button>
  </div>
  <span class="dock-sep" aria-hidden="true"></span>
  <input id="scrubber" type="range" min="0" max="100" step="0.001" value="0" aria-label="Timeline Scrubber">
</div>
```

#### Mandatory CSS Rules (include verbatim inside `<style>`; do not override these geometry properties):
```css
*, *::before, *::after {
  box-sizing: border-box;
}
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: radial-gradient(circle at center, #161922 0%, #090a0f 100%);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -webkit-user-select: none;
  user-select: none;
}
#stage {
  display: block;
  width: 100vw;
  height: 100vh;
}

#countdown {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 50;
  pointer-events: none;
  font-size: 96px;
  font-weight: 700;
  line-height: 1;
  color: rgba(255, 255, 255, 0.35);
  font-variant-numeric: tabular-nums;
}

#dock {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 100;
  width: 536px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 0 14px;
  background: rgba(15, 17, 23, 0.78);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9999px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
}

#dock button {
  font-family: inherit;
  line-height: 1;
  margin: 0;
  flex-shrink: 0;
  white-space: nowrap;
  appearance: none;
  -webkit-appearance: none;
}

.dock-sep {
  width: 1px;
  height: 18px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.12);
}

#btn-refire {
  width: 78px;
  height: 28px;
  padding: 0 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9999px;
  color: #ffffff;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
}
#btn-refire:hover {
  background: rgba(255, 255, 255, 0.16);
}

#btn-toggle {
  width: 28px;
  height: 28px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 9999px;
  color: #ffffff;
  cursor: pointer;
}
#btn-toggle:hover {
  background: rgba(255, 255, 255, 0.16);
}

#speed-group {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}
.speed-pill {
  width: 42px;
  height: 24px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 9999px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 11px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
}
.speed-pill:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
}
.speed-pill.is-active {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.2);
}

#scrubber {
  width: 157px;
  height: 4px;
  margin: 0;
  padding: 0;
  flex-shrink: 0;
  appearance: none;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.22);
  border-radius: 9999px;
  outline: none;
  cursor: pointer;
}
#scrubber::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ffffff;
  border: none;
  cursor: pointer;
}
#scrubber::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ffffff;
  border: none;
  cursor: pointer;
}
```

- **Unobstructed Viewport (Strict):** Do NOT render any other DOM elements, visible text, titles, headings, watermarks, phase labels, FPS counters, or 2D canvas text overlays anywhere on screen outside of `#countdown` and `#dock`. The only exception is the wordless HUD defined in section 5, which is drawn inside `#stage` by the WebGL renderer and adds nothing to the DOM. Note that `#dock` and `#countdown` use translucent studio styling so their geometry, positions, and control widths are pixel-locked across models while subtly blending over each model's rendered scene.

---

### 5. World-Anchored HUD (Drawn Inside the WebGL Canvas)
This benchmark has a HUD, and it is the one exception to the clean viewport contract in section 4: draw it **inside `#stage`** as a final orthographic pass of the same `THREE.WebGLRenderer` (sprites, lines and quads). Add no DOM elements, no second canvas in the page and no DOM text for it. Digits come from a glyph atlas drawn once on a detached in-memory canvas. The HUD contains **no words, labels, titles, logos or FPS readouts**. Every HUD element is a pure function of the replay at `simTime`. Keep the HUD clear of the bottom 90 px of the viewport (the dock) and of the centre of the screen during the countdown. Size it to stay readable at `1280×650`.
- **Wave number:** large digits in the top-left corner (at least 7% of the viewport height), with a small wave-glyph icon (crossed blades or a banner, drawn from shapes). It counts up at each wave start.
- **Base HP:** 10 pips in a row in the top-right corner; each leak extinguishes pips with a short flash.
- **Gold:** digits with a coin icon under the wave number.
- **Next-wave preview:** a small row of coloured enemy-type icons (counts as digits) under the gold.

---

### 6. Synthesized Sound Effects (No Music)
All sound is synthesized at runtime with the Web Audio API. Use no audio files, no `<audio>` elements, no other audio libraries and no music.
- **Start-up without extra UI:** Create one `AudioContext` at load and call `resume()` on it immediately, and again on the first `pointerdown` or `keydown` anywhere on the page. Add no start screen, mute button, volume control or any other element.
- **Sound follows the playback state:** Sound is audible only in the `PLAYING` state. In `COUNTDOWN`, `PAUSED`, `REFIRE_HOLD` and `ENDED`, and while the scrubber is being dragged, the master gain fades to silence within 50 ms and every one-shot sound still ringing is stopped. Audio only reads the replay and never changes it.
- **Driven by `simTime`:** Trigger a one-shot sound when forward playback carries `simTime` across its event's tick; scrubbing or Re-fire never triggers one-shots. At playback speeds other than `1x`, sounds are not pitch-shifted by the speed selector. Use a separate seeded generator (seed `4242`) for noise and variation.
- **Sounds:** a distinct short shot for each turret type (rate-limited so a full board never turns into noise: at most 12 shot sounds per second in total, the loudest types first), a soft pop for kills, a rising horn at each wave start, a stone crack and alarm tone for each leak, and a deep collapse with rumble at the fall, then only a low wind until the end. Pan each sound by its board position (left to right).
- **Output:** Route everything through one master gain and a `DynamicsCompressorNode`, with levels set so the mix never clips.

---

### 7. Performance & Self-Report
- **Frame-rate target:** 60 fps at `1920×1080` in current desktop Chrome on a mid-range discrete GPU, with up to 150 enemies on screen. Use instancing for enemies, effects and debris.
- **Machine-readable report:** Define this global in your main script, with truthful values:
  ```js
  window.BENCH_REPORT = {
    selfCheck: { vectorA: false, vectorB: false },  // true only if you ran rampart-sim and the hash matched
    strategy: { summary: "", seedsTested: 0, meanScoreOnTestedSeeds: null },  // your own evaluation, seeds other than 42 count
    seed42: { score: null, fallTick: null },        // from rampartSimulate(createStrategy, 42, 2020)
    systems: { board: "", enemiesAndTurrets: "", combatVisuals: "", fall: "", hud: "", audio: "" },  // "full", "simplified" or "missing"
    simplifications: [],
    testedInBrowser: false,                         // true only if you loaded the finished file in a browser this session
    measuredFps: null                               // a number only if you measured it; otherwise null
  };
  ```
- **Final message:** End your session with a short summary: whether the self-check vectors matched, how you designed and tested your strategy and its measured score on your own seeds, what is fully implemented and what was simplified, and whether you ran the file in a browser. Keep what you verified separate from what you assume.
