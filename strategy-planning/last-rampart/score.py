#!/usr/bin/env python3
"""Last Rampart strategy grader (runs alongside the shell evaluator).
  1. Extracts <script id="rampart-strategy"> and <script id="rampart-sim"> from the deliverable.
  2. Conformance (pass/fail): the model's own rampart-sim + its strategy must give the same log hash, score and fall tick
     as the reference engine + its strategy, on seed 42 and on one undisclosed seed.
     Self-check vectors A and B (published in the prompt) are reported for information.
  3. Strategy score: the strategy runs in the reference engine on five undisclosed seeds, each up to 300 waves
     (maxTicks 12020); score = mean waves held. A seed whose page throws or runs past TIMEOUT_S scores 0.
Each check runs in its own headless Chrome page (chrome-headless-shell --dump-dom), so a hung strategy cannot stall the rest.
The strategy runs inside a Function scope with window/document/Date/performance shadowed and Math.random poisoned.
Usage: score.py path/to/index.html [--seeds baseline/secret_seeds.json]   -> JSON on stdout
"""
import argparse, glob, html, json, os, re, subprocess, sys, tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = open(os.path.join(HERE, "reference", "engine.js")).read()
MAX_TICKS = 12020
TIMEOUT_S = 30          # wall clock per page; the prompt promises 10 s of CPU per game
VEC_A = 'function createStrategy(){return{plan(s){const a=[];let g=s.gold;for(const sl of s.slots)if(!sl.turret&&g>=50){a.push({op:"build",slot:sl.slot,type:"bolt"});g-=50;}return a;}};}'
VEC_B = ('function createStrategy(){return{plan(s){return s.wave===1?[{op:"build",slot:3,type:"cannon"},{op:"build",slot:6,type:"frost"}]'
         ':s.wave===3?[{op:"upgrade",slot:3},{op:"build",slot:12,type:"flak"}]:s.wave===6?[{op:"build",slot:8,type:"lance"},{op:"sell",slot:6}]:[];}};}')
EXPECT = {"A": [25.38, 1035, 166, "82a5353d"], "B": [10.93, 457, 48, "2e8858d7"]}

# Two state fields are named in the prompt without a type or unit, and the reference's choice is only one of the valid
# readings: EnemyView.slowed (true/false in the reference; the prompt also says "All quantities are integers", so 1/0 or
# the remaining slow ticks are as valid) and state.slots[].x/y (centi-tiles in the reference; tile numbers are also a
# reading of the text). The reading the model's own rampart-sim uses is detected with PROBE, and the reference engine
# hands the strategy that same view for the conformance check and the strategy score, so a strategy is always graded
# with the view its author wrote it for. Every other field matched the reference in all 19 runs of the first two rounds
# (fix 2026-11-20; see PROTOCOL.md, "Grader changes").
VIEW_ANCHORS = {"slowed": "slowed: e.slow > 0", "slotxy": "x: SLOT_XY[i][0], y: SLOT_XY[i][1],"}
for _a in VIEW_ANCHORS.values(): assert ENGINE.count(_a) == 1, _a
VIEW_READINGS = {
    "slowed": {"bool": "slowed: e.slow > 0", "int01": "slowed: e.slow > 0 ? 1 : 0", "ticks": "slowed: e.slow"},
    "slotxy": {"centi": "x: SLOT_XY[i][0], y: SLOT_XY[i][1],", "tile": "x: SLOTS[i][0], y: SLOTS[i][1],"},
}
REFERENCE_VIEW = {"slowed": "bool", "slotxy": "centi"}
PROBE = ('function createStrategy(){return{plan(s){const a=[];let g=s.gold,k=0;for(const sl of s.slots){if(sl.turret)continue;'
         'const t=k%2?"bolt":"frost",c=k%2?50:70;if(g<c)break;a.push({op:"build",slot:sl.slot,type:t});g-=c;k++;}return a;},'
         'target(t,c){return undefined;}};}')

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False); self.found = {}; self.cur = None; self.buf = []
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            i = dict(attrs).get("id")
            if i in ("rampart-strategy", "rampart-sim"): self.cur = i; self.buf = []
    def handle_data(self, d):
        if self.cur: self.buf.append(d)
    def handle_endtag(self, tag):
        if tag == "script" and self.cur:
            self.found.setdefault(self.cur, []).append("".join(self.buf)); self.cur = None

def chrome():
    c = sorted(glob.glob(os.path.expanduser("~/Library/Caches/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell")))
    if not c: raise SystemExit("chrome-headless-shell not found")
    return c[-1]

# The page: the engine is captured in a closure and its global removed before any submitted code runs.
PAGE = """<!DOCTYPE html><html><body><script>
const __E = (function(){ %(engine)s; const e = globalThis.RampartEngine; delete globalThis.RampartEngine; return e; })();
const __now = performance.now.bind(performance);
const __load = (src, name) => new Function("window","document","globalThis","self","Date","performance","THREE","RampartEngine",
    src + "\\n;return typeof " + name + " === 'function' ? " + name + " : null;")();
let __out;
try {
  Math.random = () => { throw new Error("Math.random is not allowed"); };
  const job = %(job)s; const t0 = __now(); let r;
  const strat = __load(job.strategy, "createStrategy"); if (!strat) throw new Error("createStrategy() not defined");
  const __seen = new Set();
  if (job.kind === "reference") r = __E.simulate(strat(), job.seed, job.maxTicks);
  else { const sim = __load(job.sim, "rampartSimulate"); if (!sim) throw new Error("rampartSimulate() not defined");
         const mk = job.kind !== "probe" ? strat : () => { const s = strat(); return {
           plan: (st) => { __seen.add("slot0x:" + JSON.stringify(st.slots && st.slots[0] && st.slots[0].x)); return s.plan(st); }, target: (t, c) => {
           for (const e of c) { const v = e.slowed; __seen.add(typeof v === "number" ? (v > 1 ? "gt1" : String(v)) : typeof v + ":" + String(v)); }
           return undefined; } }; };
         r = sim(mk, job.seed, job.maxTicks); }
  __out = { ok: true, score: r.score, fallTick: r.fallTick, n: Array.isArray(r.log) ? r.log.length : null, hash: r.hash,
            refHash: __E.fnv(JSON.stringify(r.log || [])), ms: Math.round(__now() - t0), seen: [...__seen].sort() };
} catch (e) { __out = { ok: false, error: String(e && e.message || e).slice(0, 300) }; }
document.body.textContent = "@@" + JSON.stringify(__out) + "@@";
</script></body></html>"""

def detect_view(sim, tmp):
    """The view the model's rampart-sim hands its strategy, as {field: reading}; the reference's reading when unclear."""
    seen = set(run({"kind": "probe", "strategy": PROBE, "sim": sim, "seed": 42, "maxTicks": MAX_TICKS}, tmp).get("seen") or [])
    sl = {v for v in seen if not v.startswith("slot0x:")}
    if sl & {"boolean:true", "boolean:false"} or not sl <= {"0", "1", "gt1"}: slowed = "bool"
    else: slowed = "ticks" if "gt1" in sl else "int01" if "1" in sl else "bool"
    xs = {v for v in seen if v.startswith("slot0x:")}
    slotxy = "tile" if xs == {"slot0x:3"} else "centi"
    return {"slowed": slowed, "slotxy": slotxy}

def run(job, tmp, view=None):
    p = os.path.join(tmp, "job.html")
    engine = ENGINE
    for f, r in (view or REFERENCE_VIEW).items(): engine = engine.replace(VIEW_ANCHORS[f], VIEW_READINGS[f][r])
    open(p, "w").write(PAGE.replace("%(engine)s", engine).replace("%(job)s", json.dumps(job)))
    try:
        out = subprocess.run([chrome(), "--dump-dom", "file://" + p], capture_output=True, text=True, timeout=TIMEOUT_S).stdout
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout > %ds" % TIMEOUT_S}
    m = re.search(r"@@(.*)@@", html.unescape(out))
    return json.loads(m.group(1)) if m else {"ok": False, "error": "no result from page"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("html")
    ap.add_argument("--seeds", default=os.path.join(HERE, "..", "..", "baseline", "secret_seeds.json"))
    a = ap.parse_args()
    seeds = json.load(open(a.seeds))           # {"score": [5 seeds], "conformance": seed}
    sp = Scripts(); sp.feed(open(a.html, encoding="utf-8").read())
    res = {"file": os.path.abspath(a.html), "checks": []}
    def check(name, ok, detail=""): res["checks"].append({"name": name, "passed": bool(ok), "detail": detail})
    strat, sim = sp.found.get("rampart-strategy", []), sp.found.get("rampart-sim", [])
    check("Exactly one rampart-strategy and one rampart-sim script", len(strat) == 1 and len(sim) == 1,
          "strategy=%d sim=%d" % (len(strat), len(sim)))
    with tempfile.TemporaryDirectory() as tmp:
        if len(strat) == 1 and len(sim) == 1:
            S, M = strat[0], sim[0]
            rd = res["view"] = detect_view(M, tmp)
            for seed in (42, seeds["conformance"]):
                ref = run({"kind": "reference", "strategy": S, "seed": seed, "maxTicks": MAX_TICKS}, tmp, rd)
                own = run({"kind": "model", "strategy": S, "sim": M, "seed": seed, "maxTicks": MAX_TICKS}, tmp)
                # fallTick and hash must match exactly. The prompt says "rounded to 2 decimals" without naming a
                # method, and Math.round(x*100)/100 and Number(x.toFixed(2)) differ by 0.01 when x ends in 5 at the
                # third decimal (45.925 -> 45.93 or 45.92), so the score may differ by at most 0.01 (fix 2026-11-20).
                same = (ref.get("ok") and own.get("ok") and [own["fallTick"], own["hash"]] == [ref["fallTick"], ref["hash"]]
                        and isinstance(own["score"], (int, float)) and abs(own["score"] - ref["score"]) <= 0.0100001)
                check("Rules conformance, seed %s" % ("42" if seed == 42 else "undisclosed"), same,
                      "reference=%s model=%s" % ({k: ref.get(k) for k in ("score", "fallTick", "hash", "error") if k in ref},
                                                 {k: own.get(k) for k in ("score", "fallTick", "hash", "error") if k in own}))
            res["self_check"] = {}
            for v, src in (("A", VEC_A), ("B", VEC_B)):
                own = run({"kind": "model", "strategy": src, "sim": M, "seed": 42 if v == "A" else 7, "maxTicks": MAX_TICKS}, tmp)
                res["self_check"][v] = own.get("ok") and [own["score"], own["fallTick"], own["n"], own["hash"]] == EXPECT[v]
            per = []
            for seed in seeds["score"]:
                r = run({"kind": "reference", "strategy": S, "seed": seed, "maxTicks": MAX_TICKS}, tmp, rd)
                per.append({"score": r["score"] if r.get("ok") else 0.0, "ms": r.get("ms"), "error": r.get("error")})
            res["strategy"] = {"per_seed": per, "mean_waves": round(sum(p["score"] for p in per) / len(per), 2)}
    res["passed_checks"] = sum(c["passed"] for c in res["checks"]); res["total_checks"] = len(res["checks"])
    res["verdict"] = "PASS" if res["passed_checks"] == res["total_checks"] else "FAIL"
    print(json.dumps(res, indent=2)); sys.exit(0 if res["verdict"] == "PASS" else 1)

if __name__ == "__main__":
    main()
