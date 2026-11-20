#!/usr/bin/env python3
"""Diagnostic for a "Rules conformance" failure: is it the model's rules, or the view it hands the strategy?
Plays one fixed probe game (all five turret types, upgrades, a sell; the probe never reads the view, so the game itself
cannot depend on it) in the reference engine and in each deliverable's rampart-sim, records every plan(state) and
target(turret, candidates) call, and lists each field that differs, after applying the view reading score.py detected
for that sim. A field listed here is one the prompt may leave open: check the prompt before counting the failure, and
if the text allows the sim's reading, add it to VIEW_READINGS in score.py and re-grade (see PROTOCOL.md).
Usage: audit_views.py path/to/index.html [more.html ...]
"""
import html, json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as sc  # noqa: E402

PROBE = ('function createStrategy(){const T=["bolt","cannon","frost","lance","flak"];return{plan(s){const a=[];let g=s.gold,k=s.wave;'
         'for(const sl of s.slots){if(sl.turret&&sl.turret.tier<3&&g>=200){a.push({op:"upgrade",slot:sl.slot});g-=200;}'
         'if(!sl.turret&&g>=120){a.push({op:"build",slot:sl.slot,type:T[(sl.slot+k)%5]});g-=120;}}'
         'if(s.wave===9)a.push({op:"sell",slot:0});return a;},target(t,c){return undefined;}};}')

PAGE = r"""<!DOCTYPE html><html><body><script>
const __E=(function(){ __ENGINE__; const e=globalThis.RampartEngine; delete globalThis.RampartEngine; return e;})();
const L=(src,n)=>new Function("window","document","globalThis","self","Date","performance","THREE","RampartEngine",src+"\n;return "+n+";")();
const cp=v=>JSON.parse(JSON.stringify(v));
function wrap(cs,rec){return function(){const s=cs();return{plan(st){rec.push(["plan",cp(st)]);return s.plan(st);},
  target(t,c){rec.push(["target",cp(t),cp(c)]);return s.target(t,c);}};};}
let out;try{const j=__JOB__;const cs=L(j.S,"createStrategy");const ra=[],rb=[];
const A=__E.simulate(wrap(cs,ra)(),42,12020);const B=L(j.M,"rampartSimulate")(wrap(cs,rb),42,12020);
const P=new Map();
const walk=(a,b,p)=>{ if(typeof a!==typeof b||Array.isArray(a)!==Array.isArray(b)||(a===null)!==(b===null)){if(!P.has(p))P.set(p,JSON.stringify(a)+" vs "+JSON.stringify(b));return;}
  if(a&&typeof a==="object"){ for(const k of new Set([...Object.keys(a),...Object.keys(b)])){const q=Array.isArray(a)?p+"[]":p+"."+k;
      if(!(k in a)||!(k in b)){if(!P.has(q))P.set(q,"missing on one side");continue;} walk(a[k],b[k],q);} return;}
  if(a!==b&&!P.has(p))P.set(p,JSON.stringify(a)+" vs "+JSON.stringify(b)); };
for(let k=0;k<Math.min(ra.length,rb.length);k++)walk(ra[k],rb[k],ra[k][0]);
out={calls:[ra.length,rb.length],hash:[A.hash,B.hash],diffs:[...P.entries()]};}catch(e){out={error:String(e)}}
document.body.textContent="@@"+JSON.stringify(out)+"@@";</script></body></html>"""

def audit(path, tmp):
    p = sc.Scripts(); p.feed(open(path, encoding="utf-8").read())
    sims = p.found.get("rampart-sim", [])
    if len(sims) != 1: return {"error": "expected one rampart-sim script, found %d" % len(sims)}
    view = sc.detect_view(sims[0], tmp)
    engine = sc.ENGINE
    for f, r in view.items(): engine = engine.replace(sc.VIEW_ANCHORS[f], sc.VIEW_READINGS[f][r])
    page = os.path.join(tmp, "audit.html")
    open(page, "w").write(PAGE.replace("__ENGINE__", engine).replace("__JOB__", json.dumps({"S": PROBE, "M": sims[0]})))
    try:
        out = subprocess.run([sc.chrome(), "--dump-dom", "file://" + page], capture_output=True, text=True, timeout=120).stdout
    except subprocess.TimeoutExpired:
        return {"view": view, "error": "timeout"}
    m = re.search(r"@@(.*)@@", html.unescape(out))
    r = json.loads(m.group(1)) if m else {"error": "no result from page"}
    r["view"] = view
    return r

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmp:
        for path in sys.argv[1:]:
            r = audit(path, tmp)
            print(path, json.dumps(r.get("view")), r.get("error") or "calls %s, hash %s" % (r["calls"], "same" if r["hash"][0] == r["hash"][1] else "DIFFERS"))
            for k, v in r.get("diffs", []): print("    %s: %s" % (k, v[:160]))
            if not r.get("error") and not r.get("diffs"): print("    every field matches the reference")
