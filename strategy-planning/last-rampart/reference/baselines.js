/* Baseline strategies used to tune difficulty and to calibrate the score scale (not shown to models). */
(function (root) {
  const E = root.RampartEngine;
  // path coverage of each slot: centi-tiles of ground / air route within a given range
  function coverage(range) {
    const out = [];
    const walk = pts => { const P = pts.map(([x, y]) => [x * 100 + 50, y * 100 + 50]); const s = [];
      for (let i = 0; i + 1 < P.length; i++) { const [ax, ay] = P[i], [bx, by] = P[i + 1];
        const L = Math.abs(bx - ax) + Math.abs(by - ay);
        for (let d = 0; d < L; d += 10) s.push([ax + Math.sign(bx - ax) * d, ay + Math.sign(by - ay) * d]); }
      return s; };
    const G = walk(E.PATH), A = walk(E.AIR);
    for (const [sx, sy] of E.SLOTS) { const cx = sx * 100 + 50, cy = sy * 100 + 50;
      const n = pts => pts.filter(([x, y]) => (x - cx) ** 2 + (y - cy) ** 2 <= range * range).length * 10;
      out.push({ g: n(G), a: n(A) }); }
    return out;
  }
  const naive = { plan(s) { const acts = []; let g = s.gold;
    for (const sl of s.slots) if (!sl.turret && g >= 50) { acts.push({ op: "build", slot: sl.slot, type: "bolt" }); g -= 50; }
    return acts; } };

  // "decent": coverage-ranked slots, a fixed type mix, upgrades once every slot is built
  function decent() {
    const cov = coverage(300);
    const order = cov.map((c, i) => [c.g + c.a, i]).sort((a, b) => b[0] - a[0]).map(x => x[1]);
    const airSlots = cov.map((c, i) => [c.a, i]).sort((a, b) => b[0] - a[0]).slice(0, 3).map(x => x[1]);
    const mix = ["bolt", "cannon", "bolt", "lance", "frost", "cannon", "lance", "bolt", "cannon", "lance", "cannon", "lance", "bolt"];
    return { plan(s) { const acts = []; let g = s.gold; let mi = s.slots.filter(x => x.turret && !airSlots.includes(x.slot)).length;
      for (const i of airSlots) if (!s.slots[i].turret && g >= 80 && s.wave >= 2) { acts.push({ op: "build", slot: i, type: s.wave < 4 ? "bolt" : "flak" }); g -= s.wave < 4 ? 50 : 80; }
      for (const i of order) { if (airSlots.includes(i) || s.slots[i].turret) continue;
        const t = mix[mi % mix.length], c = E.TURRETS[t].cost; if (g < c) break; acts.push({ op: "build", slot: i, type: t }); g -= c; mi++; }
      const built = s.slots.filter(x => x.turret);
      if (built.length >= 14) for (const tier of [1, 2]) for (const i of order) { const t = s.slots[i].turret;
        if (!t || t.tier !== tier) continue; const c = E.upgradeCost(t.type, t.tier); if (g >= c) { acts.push({ op: "upgrade", slot: i }); g -= c; } }
      return acts; } };
  }
  // "strong": same as decent but saves for interest, upgrades top slots early, kills menders first
  function strong() {
    const d = decent();
    return { plan(s) { return d.plan(s); },
      target(t, c) { const m = c.find(e => e.type === "mender"); if (m) return m.id;
        if (t.type === "lance") { let b = c[0]; for (const e of c) if (e.hp > b.hp) b = e; return b.id; }
        let b = c[0]; for (const e of c) if (e.remaining < b.remaining) b = e; return b.id; } };
  }
  root.RampartBaselines = { naive, decent: decent(), strong: strong(), coverage };
})(typeof window !== "undefined" ? window : globalThis);
