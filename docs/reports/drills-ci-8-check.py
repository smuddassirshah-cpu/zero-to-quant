"""Check for drill pack ci, pack 8 (intervals, greedy, bits, simulation): 15 drills.

For every drill it:
- runs the model solution on every example and hidden test and compares with `expect`;
- runs an independent method (drills-ci-8-indep.py: brute force on small inputs, a different algorithm on
  large ones) and compares with `expect`;
- reads the arguments of every example and test as the function receives them and checks them against the
  drill's `constraints` objects (the rules of tools/drill-constraints.mjs) and the prose constraints (VALID);
- checks the starter fails at least one test;
- runs every planted solution on all hidden tests in its own CPython process: a wrong one must fail a test
  inside 2.5 s; a slow one (SLOW_IDX, always the last entries) must run past 5 s;
- runs every further wrong solution of drills-ci-8-wrong.py (four or more a drill) and asserts each fails a
  hidden test, by value, by an exception or past 5 s;
- recomputes the worked numbers stated in each brief (STATED);
- checks the pack: mix 3/5/5/2 by difficulty 2/3/4/5, two stdin drills, pace 900 to 2,700, 10 to 15 hidden
  tests, 2 or 3 examples with a note, `pack-8` first in tags, two or more planted, the `how` test count, the
  index.json row, and at difficulty 4 and 5 a `how` naming the obvious method and the step to the target.
With --pyodide <pkgs>, it also times, in Pyodide under node, the model and each slow planted method of every
difficulty 4 and 5 drill over all hidden tests: the model must take at most 1 s and each slow method more than 5 s.
Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-8-check.py [--pyodide <pkgs>] [drill ids]
"""
import json, os, re, subprocess, sys, time, tempfile, importlib.util
from collections import Counter

sys.setrecursionlimit(20000)
HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")

def _load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

IND = _load("drills-ci-8-indep")
WRONG = _load("drills-ci-8-wrong").WRONG

IDS = ["ci-grace-sessions", "ci-rest-days", "ci-robot-floor",
       "ci-one-bit-apart", "ci-switch-panel", "ci-ring-turns", "ci-double-checks", "ci-first-fit-slot",
       "ci-room-numbers", "ci-loop-starts", "ci-stone-hops", "ci-k-bit-count", "ci-ring-bonuses",
       "ci-spiral-cells", "ci-stop-cascade"]
args = sys.argv[1:]
PYODIDE = None
if "--pyodide" in args:
    k = args.index("--pyodide")
    PYODIDE = args[k + 1]
    del args[k:k + 2]
FULL = not args
if not FULL:
    IDS = args
IDS = [i for i in IDS if os.path.exists(os.path.join(DRILLS, i + ".json"))]
PATTERNS = {"intervals", "greedy", "bits", "simulation"}

# planted solutions that are right but too slow (always the last entries of `planted`)
SLOW_IDX = getattr(IND, "SLOW_IDX", {})
SLOW_PLANTED = {(d, k) for d, ks in SLOW_IDX.items() for k in ks}

# ======================= constraint objects (mirror of tools/drill-constraints.mjs) =======================

def kind(v):
    if isinstance(v, bool): return "bool"
    if isinstance(v, int): return "int"
    if isinstance(v, float): return "float"
    if isinstance(v, str): return "str"
    if v is None: return "None"
    if isinstance(v, (list, tuple)): return "list"
    if isinstance(v, dict): return "dict"
    return "value"

def violations(c, v, where):
    m, k = [], kind(v)
    t = c.get("type")
    if t:
        ok = k == "int" if t == "int" else k in ("int", "float") if t in ("float", "number") else k == t
        if not ok:
            return [f"{where} is {k}, not {t}"]
    if c.get("range") and k in ("int", "float"):
        lo, hi = c["range"]
        if (lo is not None and v < lo) or (hi is not None and v > hi):
            m.append(f"{where} = {v} outside {c['range']}")
    if k in ("str", "list", "dict"):
        if c.get("len"):
            lo, hi = c["len"]
            if (lo is not None and len(v) < lo) or (hi is not None and len(v) > hi):
                m.append(f"{where} has length {len(v)}, outside {c['len']}")
        if c.get("nonEmpty") and not v:
            m.append(f"{where} is empty")
    if k == "str" and c.get("pattern") and not re.fullmatch(c["pattern"], v):
        m.append(f"{where} does not match {c['pattern']}")
    if k == "list":
        if c.get("sorted"):
            desc = c["sorted"] == "desc"
            if any((v[i - 1] < v[i]) if desc else (v[i - 1] > v[i]) for i in range(1, len(v))):
                m.append(f"{where} not sorted")
        if c.get("distinct"):
            keys = [json.dumps(x) for x in v]
            if len(set(keys)) != len(keys):
                m.append(f"{where} repeats a value")
        if "of" in c or c.get("range"):
            sub = {"range": c["range"]} if "of" not in c else ({"type": c["of"], "range": c.get("range")} if isinstance(c["of"], str) else c["of"])
            if sub.get("range") is None:
                sub = {k2: v2 for k2, v2 in sub.items() if k2 != "range"}
            for i, x in enumerate(v):
                r = violations(sub, x, f"{where}[{i}]")
                if r:
                    m += r
                    break
    return m

class _Captured:
    def __getattr__(self, _): return self
    def __getitem__(self, _): return self
    def __len__(self): return 0
    def __iter__(self): return iter(())
    def __call__(self, *a, **k): return self
    def __mod__(self, _): return 0
    def __eq__(self, _): return False
    def __hash__(self): return 0
CAPTURED = _Captured()

def capture_args(d, call):
    """the arguments the function receives in this call, by parameter name"""
    head = re.search(r"^def\s+" + d["fn"] + r"\s*\(([^)]*)\)", d["starter"], re.M).group(1)
    names = [s.strip().split("=")[0].strip() for s in head.split(",") if s.strip()]
    got = []
    def grab(*a, **kw):
        got.append(dict(zip(names, a), **kw))
        return CAPTURED
    try:
        eval(call, {d["fn"]: grab})
    except Exception:
        pass
    return got

# ======================= running =======================

RUNNER = r"""
import json, sys, time
sys.setrecursionlimit(1000)
spec = json.load(sys.stdin)
ns = {}
exec(spec["code"], ns)
first = None
t0 = time.time()
for i, c in enumerate(spec["cases"]):
    try:
        ok = eval(c["call"], ns) == eval(c["expect"])
    except Exception as e:
        ok = False
    if not ok and first is None:
        first = i
        break
print(json.dumps({"failed": first, "s": round(time.time() - t0, 2)}))
"""

def run_isolated(code, cases, limit=10):
    try:
        r = subprocess.run([sys.executable, "-c", RUNNER], input=json.dumps({"code": code, "cases": cases}),
                           capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        return {"failed": "timeout", "s": limit}
    lines = r.stdout.strip().splitlines()
    if not lines:
        return {"failed": "crash", "s": None}
    return json.loads(lines[-1])

errors = []
def err(m):
    errors.append(m)
    print("ERROR", m)

PYO_SCRIPT = r"""
import json, time, sys
spec = json.loads(open(SPEC_PATH).read())
ns = {}
exec(spec["code"], ns)
t0 = time.time()
ok = True
for c in spec["cases"]:
    ok = ok and eval(c["call"], ns) == eval(c["expect"])
    if time.time() - t0 > spec["cap"]:
        break
print("PYO", json.dumps({"s": round(time.time() - t0, 3), "ok": ok}))
"""

PYO_JS = r"""
import fs from 'node:fs'; import path from 'node:path';
const dir = path.resolve(process.argv[2]);
const { loadPyodide } = await import(path.join(dir, 'pyodide.mjs'));
const py = await loadPyodide({ indexURL: dir + '/' });
py.FS.writeFile('/spec.json', fs.readFileSync(process.argv[3], 'utf8'));
py.runPython(fs.readFileSync(process.argv[4], 'utf8'));
"""

def pyodide_time(code, cases, cap=12.0):
    """seconds Pyodide takes over the cases (stops after `cap` seconds; a run cut off reports the cap)"""
    with tempfile.TemporaryDirectory() as tmp:
        spec, script, js = (os.path.join(tmp, f) for f in ("spec.json", "t.py", "t.mjs"))
        json.dump({"code": code, "cases": cases, "cap": cap}, open(spec, "w"))
        open(script, "w").write("SPEC_PATH = '/spec.json'\n" + PYO_SCRIPT)
        open(js, "w").write(PYO_JS)
        pkg = os.path.join(PYODIDE, "pyodide-0.27.7", "package")
        try:
            r = subprocess.run(["node", js, pkg, spec, script], capture_output=True, text=True, timeout=cap + 8)
        except subprocess.TimeoutExpired:
            return {"s": cap, "ok": None}
        line = [l for l in r.stdout.splitlines() if l.startswith("PYO ")]
        if not line:
            return {"s": None, "ok": None, "err": r.stderr[-300:]}
        return json.loads(line[-1][4:])

diffs = Counter()
INDEX = json.load(open(os.path.join(DRILLS, "index.json")))
stdin = 0
for did in IDS:
    d = json.load(open(os.path.join(DRILLS, did + ".json")))
    cases = d["examples"] + d["tests"]
    fn = d["fn"]
    objs = [c for c in d["constraints"] if isinstance(c, dict)]
    if not objs:
        err(f"{did}: no constraint objects")
    for c in cases:
        got = capture_args(d, c["call"])
        if not got:
            err(f"{did}: could not read the arguments of {c['call'][:60]}")
        for a in got:
            for o in objs:
                if o["arg"] in a:
                    for m in violations(o, a[o["arg"]], o["arg"]):
                        err(f"{did}: {c['call'][:50]}: {m}")
            try:
                IND.VALID[did](a)
            except AssertionError as e:
                err(f"{did}: {c['call'][:60]} breaks the prose constraints ({e})")
    ns = {}
    exec(d["solution"], ns)
    t0 = time.time()
    for c in cases:
        if eval(c["call"], ns) != eval(c["expect"]):
            err(f"{did}: model fails {c['call'][:60]}")
    dt = time.time() - t0
    if dt > 1.5:
        err(f"{did}: model took {dt:.2f} s")
    ins = {fn: IND.INDEP[did]}
    for c in cases:
        if eval(c["call"], ins) != eval(c["expect"]):
            err(f"{did}: independent method disagrees on {c['call'][:60]}")
    for check, want in getattr(IND, "STATED", {}).get(did, []):
        if check() != want:
            err(f"{did}: a stated number does not recompute ({want})")
    sres = run_isolated(d["starter"], d["tests"])
    if sres["failed"] is None:
        err(f"{did}: starter passes every test")
    pl = d.get("planted", [])
    if len(pl) < 2:
        err(f"{did}: fewer than two planted")
    caught = []
    for k, p in enumerate(pl):
        if (did, k) in SLOW_PLANTED:
            if k < len(pl) - len(SLOW_IDX[did]):
                err(f"{did}: slow planted[{k}] is not in the last entries")
            r = run_isolated(p["code"], d["tests"], limit=5)
            if r["failed"] != "timeout":
                err(f"{did}: planted[{k}] is meant to be too slow but finished ({r})")
            caught.append("slow")
            continue
        r = run_isolated(p["code"], d["tests"], limit=2.5)
        if r["failed"] == "timeout":
            err(f"{did}: planted[{k}] runs past 2.5 s in CPython, so it could time out in the browser")
        elif r["failed"] is None:
            err(f"{did}: planted[{k}] passes every hidden test ({p['slip']})")
        caught.append(r["failed"])
    extra = []
    ws = WRONG.get(did, [])
    if len(ws) < 4:
        err(f"{did}: fewer than four further wrong solutions in drills-ci-8-wrong.py")
    for code, what in ws:
        r = run_isolated(code, d["tests"], limit=5)
        if r["failed"] is None:
            err(f"{did}: wrong solution passes every hidden test ({what})")
        extra.append(r["failed"])
    if d["difficulty"] >= 4:
        if not SLOW_IDX.get(did):
            err(f"{did}: difficulty {d['difficulty']} needs a slow planted method")
        if "obvious method" not in d["how"] or "step to the target" not in d["how"]:
            err(f"{did}: how must name the obvious method and the step to the target")
    if PYODIDE and SLOW_IDX.get(did):
        tm = pyodide_time(d["solution"], d["tests"])
        if tm["s"] is None or tm["s"] > 1.0 or not tm["ok"]:
            err(f"{did}: model in Pyodide {tm}")
        for src in SLOW_IDX[did]:
            ts = pyodide_time(pl[src]["code"], d["tests"])
            if ts["s"] is None or ts["s"] <= 5.0:
                err(f"{did}: slow planted[{src}] in Pyodide {ts}")
            print(f"  {did}: Pyodide model {tm['s']} s, slow planted[{src}] {ts['s']} s{' (cut off)' if ts['s'] and ts['s'] >= 12 else ''}")
    diffs[d["difficulty"]] += 1
    stdin += "stdin" in d["tags"]
    if d["tags"][0] != "pack-8": err(f"{did}: tags must start pack-8")
    if not 900 <= d["pace"] <= 2700: err(f"{did}: pace {d['pace']}")
    if not 10 <= len(d["tests"]) <= 15: err(f"{did}: {len(d['tests'])} tests")
    if not 2 <= len(d["examples"]) <= 3 or not all(e.get("note") for e in d["examples"]): err(f"{did}: examples")
    if len(d["notes"]) != 3: err(f"{did}: notes")
    if d["pack"] != "ci" or d["course"] != "coding-int": err(f"{did}: pack or course")
    if d["pattern"] not in PATTERNS: err(f"{did}: pattern {d['pattern']}")
    if f"Submit runs {len(d['tests'])} hidden tests" not in d["how"]: err(f"{did}: how test count")
    row = [r for r in INDEX if r["id"] == did]
    if len(row) != 1 or row[0]["difficulty"] != d["difficulty"] or row[0]["name"] != d["name"] or row[0]["course"] != "coding-int":
        err(f"{did}: index row out of step with the drill")
    print(f"{did}: d{d['difficulty']} {len(d['tests'])} tests ok, model {dt:.2f} s, starter fails at {sres['failed']}, planted fail at {caught}, further wrong fail at {extra}")
if FULL and dict(diffs) != {2: 3, 3: 5, 4: 5, 5: 2}: err(f"difficulty mix {dict(diffs)}")
if FULL and stdin != 2: err(f"{stdin} stdin drills")
print(f"{len(IDS)} drills, {len(errors)} errors")
sys.exit(1 if errors else 0)
