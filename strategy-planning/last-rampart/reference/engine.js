/* Last Rampart reference engine (integer-only, deterministic).
   The rules here are the rules in prompt.md, section 2; if the two ever disagree, the prompt is wrong and both get fixed.
   Every quantity is an integer: positions in centi-tiles (100 per tile), time in ticks (20 per second).
   Usage: RampartEngine.simulate(strategy, seed, maxTicks) -> { score, fallTick, wave, log, hash } */
(function (root) {
  "use strict";
  const C = {
    TPS: 20, FIRST_WAVE: 20, WAVE_GAP: 40, SPAWN_GAP: 4, BASE_HP: 10, START_GOLD: 250,
    INTEREST_PCT: 5, INTEREST_CAP: 50, HP_GROWTH_PCT: 108, MAX_ACTIONS: 32,
    COLS: 24, ROWS: 14,
  };
  const PATH = [[0, 2], [6, 2], [6, 10], [12, 10], [12, 3], [18, 3], [18, 11], [23, 11]];
  const AIR = [[0, 6], [21, 6], [21, 11], [23, 11]];
  const SLOTS = [[3, 3], [5, 5], [7, 4], [7, 8], [9, 9], [10, 5], [11, 8], [13, 8],
                 [14, 5], [15, 2], [16, 7], [17, 4], [19, 8], [20, 10], [22, 9], [3, 7]];
  const TURRETS = {
    bolt:   { cost: 50,  dmg: 26, period: 8,  range: 300, splash: 0,  slow: 0,  pierce: 0, ground: 1, air: 1 },
    cannon: { cost: 90,  dmg: 60, period: 24, range: 260, splash: 90, slow: 0,  pierce: 0, ground: 1, air: 0 },
    frost:  { cost: 70,  dmg: 10, period: 12, range: 240, splash: 0,  slow: 30, pierce: 0, ground: 1, air: 1 },
    lance:  { cost: 120, dmg: 180, period: 36, range: 360, splash: 0,  slow: 0,  pierce: 1, ground: 1, air: 0 },
    flak:   { cost: 80,  dmg: 40, period: 10, range: 320, splash: 70, slow: 0,  pierce: 0, ground: 0, air: 1 },
  };
  const TURRET_ORDER = ["bolt", "cannon", "frost", "lance", "flak"];
  const ENEMIES = {
    grunt:     { hp: 60,  speed: 10, armor: 0, bounty: 4, leak: 1, air: 0 },
    brute:     { hp: 150, speed: 6,  armor: 6, bounty: 9, leak: 3, air: 0 },
    runner:    { hp: 40,  speed: 20, armor: 0, bounty: 4, leak: 1, air: 0 },
    wisp:      { hp: 50,  speed: 12, armor: 0, bounty: 6, leak: 2, air: 1 },
    splitter:  { hp: 90,  speed: 8,  armor: 0, bounty: 6, leak: 2, air: 0 },
    mender:    { hp: 70,  speed: 8,  armor: 0, bounty: 7, leak: 2, air: 0 },
    splitling: { hp: 0,   speed: 12, armor: 0, bounty: 1, leak: 1, air: 0 },   // hp = floor(parent maxHp / 4)
  };
  // [type, weight, first wave it can appear]
  const WEIGHTS = [["grunt", 10, 1], ["runner", 4, 2], ["wisp", 3, 3], ["brute", 3, 4], ["splitter", 2, 6], ["mender", 1, 8]];
  const SLOW_PCT = 60, MENDER_PERIOD = 20, MENDER_RADIUS = 150, MENDER_PCT = 8, SELL_PCT = 70;

  function mulberry32(a) {
    return function () {               // returns an unsigned 32-bit integer (not a float)
      a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return (t ^ (t >>> 14)) >>> 0;
    };
  }
  function polyline(pts) {
    const P = pts.map(([x, y]) => [x * 100 + 50, y * 100 + 50]);
    let len = 0; const segs = [];
    for (let i = 0; i + 1 < P.length; i++) {
      const [ax, ay] = P[i], [bx, by] = P[i + 1];
      const L = Math.abs(bx - ax) + Math.abs(by - ay);   // segments are axis-aligned
      segs.push({ ax, ay, dx: Math.sign(bx - ax), dy: Math.sign(by - ay), s0: len, L }); len += L;
    }
    return { len, at(p) {
      for (const s of segs) if (p < s.s0 + s.L) { const d = p - s.s0; return [s.ax + s.dx * d, s.ay + s.dy * d]; }
      const s = segs[segs.length - 1]; return [s.ax + s.dx * s.L, s.ay + s.dy * s.L];
    } };
  }
  const GROUND = polyline(PATH), SKY = polyline(AIR);
  const SLOT_XY = SLOTS.map(([x, y]) => [x * 100 + 50, y * 100 + 50]);

  function turretStats(type, tier) {
    const b = TURRETS[type];
    let dmg = b.dmg; for (let t = 1; t < tier; t++) dmg = Math.floor(dmg * 16 / 10);
    return { dmg, range: b.range + 30 * (tier - 1), period: b.period, splash: b.splash, slow: b.slow,
             pierce: b.pierce, ground: b.ground, air: b.air };
  }
  function upgradeCost(type, tier) { return TURRETS[type].cost * (tier === 1 ? 1 : 2); }   // tier 1->2, 2->3
  function waveStart(w) { return C.FIRST_WAVE + (w - 1) * C.WAVE_GAP; }
  function waveCount(w) { return 4 + Math.floor(3 * w / 5); }
  function hpMult(w) { let m = 1000; for (let i = 1; i < w; i++) m = Math.floor(m * C.HP_GROWTH_PCT / 100); return m; }

  function simulate(strategy, seed, maxTicks) {
    const rng = mulberry32(seed >>> 0);
    const waves = [];
    function genWave(w) {
      const pool = WEIGHTS.filter(e => w >= e[2]); const tot = pool.reduce((a, e) => a + e[1], 0);
      const out = [];
      for (let i = 0; i < waveCount(w); i++) {
        let r = rng() % tot, k = 0; while (r >= pool[k][1]) { r -= pool[k][1]; k++; }
        out.push(pool[k][0]);
      }
      return out;
    }
    let gold = C.START_GOLD, baseHp = C.BASE_HP, nextId = 1, wave = 0, fallTick = -1;
    const slots = SLOTS.map(() => null);        // {type, tier, spent, cd}
    const enemies = [];                         // kept in ascending id order
    const queue = [];                           // [tick, type, wave]
    const log = [];
    const mult = [0];
    function spawn(type, w, progress, hpOverride) {
      const d = ENEMIES[type]; const maxHp = hpOverride || Math.floor(d.hp * mult[w] / 1000);
      const armor = type === "brute" ? d.armor + w : type === "grunt" ? Math.floor(w / 4) : d.armor;   // armour grows with the wave
      enemies.push({ id: nextId++, type, wave: w, hp: maxHp, maxHp, progress, slow: 0, age: 0,
                     speed: d.speed, armor, air: d.air });
    }
    function pos(e) { return (e.air ? SKY : GROUND).at(e.progress); }
    function remaining(e) { return (e.air ? SKY.len : GROUND.len) - e.progress; }
    function view(e) { const [x, y] = pos(e);
      return { id: e.id, type: e.type, hp: e.hp, maxHp: e.maxHp, x, y, air: e.air, armor: e.armor,
               speed: e.speed, slowed: e.slow > 0, remaining: remaining(e) }; }
    function snapshot(tick) {
      return { tick, wave, gold, baseHp,
        slots: slots.map((s, i) => ({ slot: i, x: SLOT_XY[i][0], y: SLOT_XY[i][1],
                                       turret: s ? { type: s.type, tier: s.tier, spent: s.spent } : null })),
        enemies: enemies.map(view), nextWave: waves[wave + 1] ? waves[wave + 1].slice() : [] };
    }
    function act(tick, a) {
      if (!a || typeof a !== "object") return;
      const i = a.slot | 0; if (i < 0 || i >= SLOTS.length || a.slot !== i) return;
      if (a.op === "build" && !slots[i] && TURRETS[a.type] && gold >= TURRETS[a.type].cost) {
        gold -= TURRETS[a.type].cost; slots[i] = { type: a.type, tier: 1, spent: TURRETS[a.type].cost, cd: 0 };
        log.push([tick, "B", i, TURRET_ORDER.indexOf(a.type)]);
      } else if (a.op === "upgrade" && slots[i] && slots[i].tier < 3) {
        const c = upgradeCost(slots[i].type, slots[i].tier);
        if (gold >= c) { gold -= c; slots[i].tier++; slots[i].spent += c; log.push([tick, "U", i, slots[i].tier]); }
      } else if (a.op === "sell" && slots[i]) {
        gold += Math.floor(slots[i].spent * SELL_PCT / 100); slots[i] = null; log.push([tick, "S", i, 0]);
      }
    }
    function hit(e, dmg, st) {
      e.hp -= st.pierce ? dmg : Math.max(1, dmg - e.armor);
      if (st.slow) e.slow = st.slow;
    }
    for (let tick = 0; tick < maxTicks; tick++) {
      // 1. wave start: interest, wave bonus, generate, plan, queue spawns
      if (tick >= C.FIRST_WAVE && (tick - C.FIRST_WAVE) % C.WAVE_GAP === 0) {
        wave++; mult[wave] = hpMult(wave);
        if (!waves[wave]) waves[wave] = genWave(wave);
        waves[wave + 1] = genWave(wave + 1); mult[wave + 1] = hpMult(wave + 1);
        gold += Math.min(C.INTEREST_CAP, Math.floor(gold * C.INTEREST_PCT / 100)) + 10 + 2 * wave;
        let actions = [];
        if (strategy.plan) actions = strategy.plan(snapshot(tick)) || [];
        if (!Array.isArray(actions)) actions = [];
        for (const a of actions.slice(0, C.MAX_ACTIONS)) act(tick, a);
        waves[wave].forEach((t, k) => queue.push([waveStart(wave) + k * C.SPAWN_GAP, t, wave, k]));
        // waves overlap once a wave holds more than WAVE_GAP / SPAWN_GAP enemies: keep spawns ordered by (tick, wave, index)
        queue.sort((a, b) => a[0] - b[0] || a[2] - b[2] || a[3] - b[3]);
      }
      // 2. spawns due this tick, in queue order
      while (queue.length && queue[0][0] === tick) { const [, t, w] = queue.shift(); spawn(t, w, 0); }
      // 3. movement and leaks (ascending id)
      for (let k = 0; k < enemies.length; k++) {
        const e = enemies[k];
        e.progress += e.slow > 0 ? Math.floor(e.speed * SLOW_PCT / 100) : e.speed;
        if (e.progress >= (e.air ? SKY.len : GROUND.len)) {
          baseHp -= ENEMIES[e.type].leak; log.push([tick, "L", e.id, baseHp]); enemies.splice(k--, 1);
          if (baseHp <= 0) { fallTick = tick; break; }
        }
      }
      if (fallTick >= 0) { log.push([fallTick, "F", wave, 0]); break; }
      // 4. menders heal every 20 ticks of age (ascending id)
      for (const e of enemies) {
        e.age++;
        if (e.type === "mender" && e.age % MENDER_PERIOD === 0) {
          const [mx, my] = pos(e);
          for (const o of enemies) { const [ox, oy] = pos(o); const dx = ox - mx, dy = oy - my;
            if (dx * dx + dy * dy <= MENDER_RADIUS * MENDER_RADIUS)
              o.hp = Math.min(o.maxHp, o.hp + Math.floor(o.maxHp * MENDER_PCT / 100)); }
        }
      }
      // 5. turrets fire (ascending slot)
      for (let i = 0; i < slots.length; i++) {
        const s = slots[i]; if (!s) continue;
        if (s.cd > 0) s.cd--;
        if (s.cd > 0) continue;
        const st = turretStats(s.type, s.tier); const [tx, ty] = SLOT_XY[i];
        const inDomain = e => (e.air ? st.air : st.ground) && e.hp > 0;
        const cand = enemies.filter(e => { if (!inDomain(e)) return false; const [x, y] = pos(e);
          const dx = x - tx, dy = y - ty; return dx * dx + dy * dy <= st.range * st.range; });
        if (!cand.length) continue;
        let tgt = null;
        if (strategy.target) {
          const id = strategy.target({ slot: i, type: s.type, tier: s.tier, x: tx, y: ty, range: st.range }, cand.map(view));
          tgt = cand.find(e => e.id === id) || null;
        }
        if (!tgt) { tgt = cand[0]; for (const e of cand) if (remaining(e) < remaining(tgt)) tgt = e; }
        const victims = [];
        if (st.splash) { const [cx, cy] = pos(tgt);
          for (const e of enemies) { if (!inDomain(e)) continue; const [x, y] = pos(e); const dx = x - cx, dy = y - cy;
            if (dx * dx + dy * dy <= st.splash * st.splash) victims.push(e); }
        } else victims.push(tgt);
        for (const e of victims) hit(e, st.dmg, st);
        s.cd = st.period;
        // deaths in ascending id; splitters split into 3 splitlings at their progress
        for (let k = 0; k < enemies.length; k++) {
          const e = enemies[k]; if (e.hp > 0) continue;
          gold += ENEMIES[e.type].bounty; log.push([tick, "K", e.id, i]); enemies.splice(k--, 1);
          if (e.type === "splitter") for (let j = 0; j < 3; j++) {
            spawn("splitling", e.wave, e.progress, Math.max(1, Math.floor(e.maxHp / 4)));
          }
        }
      }
      // 6. slow timers
      for (const e of enemies) if (e.slow > 0) e.slow--;
    }
    const endTick = fallTick >= 0 ? fallTick : maxTicks;
    const score = Math.max(0, endTick - C.FIRST_WAVE) / C.WAVE_GAP;
    return { score: Math.round(score * 100) / 100, fallTick, wave, gold, baseHp, log, hash: fnv(JSON.stringify(log)) };
  }
  function fnv(s) { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); }
    return (h >>> 0).toString(16).padStart(8, "0"); }

  root.RampartEngine = { C, PATH, AIR, SLOTS, TURRETS, ENEMIES, WEIGHTS, simulate, turretStats, upgradeCost, hpMult, waveCount, fnv };
})(typeof window !== "undefined" ? window : globalThis);
