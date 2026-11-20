#!/usr/bin/env python3
"""Extra analysis, not the official score: replays every graded strategy on 200 public wave sequences
(seeds 1000-1199, 300 waves max each) in the reference engine, with the same view reading score.py uses for that build
(detect_view), and writes replay200.json {"<model-key>/run-N": [200 scores]} plus a summary table.
Answers "are five hidden maps enough to rank the strategies?". The board and routes are the same on every seed.
Usage: replay200.py [run-dir ...]   (default: every <model-key>/run-N with a deliverable)"""
import glob, html, json, os, re, statistics as st, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); BENCH = os.path.dirname(HERE)
sys.path.insert(0, BENCH); import score as sc  # noqa: E402
SEEDS = list(range(1000, 1200))
PAGE = r"""<!DOCTYPE html><html><body><script>
const __E=(function(){ __ENGINE__; const e=globalThis.RampartEngine; delete globalThis.RampartEngine; return e;})();
const L=(src,n)=>new Function("window","document","globalThis","self","Date","performance","THREE","RampartEngine",src+"\n;return "+n+";")();
let out=[];try{Math.random=()=>{throw new Error("Math.random is not allowed")};const cs=L(__S__,"createStrategy");
for(const s of __SEEDS__){try{out.push(__E.simulate(cs(),s,12020).score);}catch(e){out.push(0);}}}catch(e){out=String(e);}
document.body.textContent="@@"+JSON.stringify(out)+"@@";</script></body></html>"""
def main():
    runs = sys.argv[1:] or sorted(os.path.relpath(os.path.dirname(p), BENCH) for p in glob.glob(os.path.join(BENCH, "*", "run-*", "index.html")))
    out_p = os.path.join(HERE, "replay200.json"); res = json.load(open(out_p)) if os.path.exists(out_p) else {}
    with tempfile.TemporaryDirectory() as tmp:
        for name in runs:
            p = sc.Scripts(); p.feed(open(os.path.join(BENCH, name, "index.html"), encoding="utf-8").read())
            S, M = p.found["rampart-strategy"][0], p.found["rampart-sim"][0]; view = sc.detect_view(M, tmp); eng = sc.ENGINE
            for f, r in view.items(): eng = eng.replace(sc.VIEW_ANCHORS[f], sc.VIEW_READINGS[f][r])
            f = os.path.join(tmp, "p.html")
            open(f, "w").write(PAGE.replace("__ENGINE__", eng).replace("__S__", json.dumps(S)).replace("__SEEDS__", json.dumps(SEEDS)))
            o = subprocess.run([sc.chrome(), "--dump-dom", "file://" + f], capture_output=True, text=True, timeout=900).stdout
            r = json.loads(re.search(r"@@(.*)@@", html.unescape(o)).group(1)); assert isinstance(r, list) and len(r) == len(SEEDS), (name, r)
            res[name] = r; print("%-34s %s  mean %.2f" % (name, view, st.mean(r)), flush=True)
    json.dump(res, open(out_p, "w"), indent=0)
    tel = {r["model_key"] + "/" + r["run"]: r for r in json.load(open(os.path.join(BENCH, "telemetry.json")))}
    rows = sorted(res, key=lambda k: -st.mean(res[k]))
    md = ["# 200-map replay (extra analysis, not the official score)", "",
          "Each graded strategy replayed on seeds 1000-1199 in the reference engine, with its own view reading. "
          "Official score: mean of five hidden maps (round score 0 = the build did not ship).", "",
          "| Rank | Build | 200-map mean | Std. error | Official strategy score | Round score |", "|---|---|---|---|---|---|"]
    for i, k in enumerate(rows, 1):
        t = tel.get(k, {}); md.append("| %d | %s | %.2f | %.3f | %s | %s |" % (i, k, st.mean(res[k]), st.stdev(res[k]) / len(res[k]) ** 0.5,
                                                                              t.get("strategy_mean_waves"), t.get("round_score")))
    open(os.path.join(HERE, "REPLAY200.md"), "w").write("\n".join(md) + "\n"); print("wrote replay200.json and REPLAY200.md")
if __name__ == "__main__":
    main()
