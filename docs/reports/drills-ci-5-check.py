"""Check for drill pack ci, pack 5 (graphs): 15 drills.

For every drill it:
- runs the model solution on every example and hidden test and compares with `expect`;
- runs an independent method written here (brute force on small inputs: every permutation, a sweep
  until nothing changes, a search over states, every simple path, every wall removed in turn; on large
  inputs a different algorithm) and compares with `expect`;
- reads the arguments of every example and test as the function receives them and checks them against
  the drill's `constraints` objects (the same rules as tools/drill-constraints.mjs) and against the
  prose constraints (`VALID`, e.g. a grid is rectangular, racks are below `n`);
- checks the starter fails at least one test;
- runs every planted solution on all hidden tests in its own CPython process: a wrong one must fail a
  test inside 2.5 s; a planted solution marked too slow (`SLOW_PLANTED`, always last) must run past 5 s;
- runs each further slow method in SLOW one test at a time and asserts a hidden test takes it past 5 s;
- times the model over all tests (under 1.5 s in CPython);
- checks the pack mix: 3/5/5/2 by difficulty 2/3/4/5, two stdin drills, pace 900 to 2,700, 10 to 15
  hidden tests, 2 or 3 examples with a note, `pack-5` first in tags, two or more planted, and at
  difficulty 4 and 5 a `how` that names the obvious method and the step to the target.
With --pyodide <pkgs>, it also times, in Pyodide under node, the model and the obvious method of every
difficulty 4 and 5 drill over all hidden tests: the model must take at most 1 s (a fifth of the 5 s
limit) and the obvious method more than 5 s.
Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-5-check.py [--pyodide <pkgs>] [drill ids]
"""
import json, os, re, subprocess, sys, time, heapq, tempfile
from collections import Counter, defaultdict, deque
from itertools import permutations

sys.setrecursionlimit(20000)
HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
IDS = ["ci-flood-reach", "ci-loop-cables", "ci-line-from-pairs", "ci-checkpoint-route", "ci-stuck-jobs",
       "ci-two-shift-rota", "ci-cheapest-route", "ci-island-shapes", "ci-wall-break-route", "ci-nearest-depot",
       "ci-reclaimed-land", "ci-ferry-timetable", "ci-first-circular-rule", "ci-half-fare-route", "ci-safest-walk"]
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
SMALL = 40   # cells, stations or jobs up to which the brute-force method runs

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

def capture_args(d, call):
    """the arguments the function receives in this call, by parameter name"""
    names = re.match(r"def\s+\w+\s*\(([^)]*)\)", re.search(r"^def\s+" + d["fn"] + r"\s*\(.*$", d["starter"], re.M).group(0)).group(1)
    names = [s.strip().split("=")[0].strip() for s in names.split(",") if s.strip()]
    got = []
    def grab(*a, **kw):
        got.append(dict(zip(names, a), **kw))
        return CAPTURED
    try:
        eval(call, {d["fn"]: grab})
    except Exception:
        pass
    return got

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

# ======================= prose constraints, per drill =======================

def grid_ok(g, chars=None):
    return len(g) >= 1 and all(len(r) == len(g[0]) for r in g) and (chars is None or all(set(r) <= set(chars) for r in g))

def stdin_grid(text, chars, once):
    tok = text.split()
    r, c = int(tok[0]), int(tok[1])
    rows = tok[2:]
    assert len(rows) == r and 1 <= r <= 300 and 1 <= c <= 300, "row count"
    assert all(len(x) == c and set(x) <= set(chars) for x in rows), "row shape"
    flat = "".join(rows)
    for ch in once:
        assert flat.count(ch) == 1, f"{ch} once"
    lines = text.split("\n")
    return True

def v_flood(a):
    g = a["heights"]
    assert grid_ok(g) and 0 <= a["r"] < len(g) and 0 <= a["c"] < len(g[0])

def v_loop(a):
    assert all(x != y and 0 <= x < a["n"] and 0 <= y < a["n"] for x, y in a["cables"])

def v_line(a):
    p = a["pairs"]
    names = {s for q in p for s in q}
    assert len(names) == len(p) + 1, "one line: n stations, n - 1 pairs"
    deg = Counter(s for q in p for s in q)
    assert max(deg.values()) <= 2 and all(x != y for x, y in p)
    assert len({frozenset(q) for q in p}) == len(p), "each pair once"
    # connected: walk
    near = defaultdict(list)
    for x, y in p:
        near[x].append(y); near[y].append(x)
    start = next(iter(names)); seen = {start}; st = [start]
    while st:
        u = st.pop()
        for w in near[u]:
            if w not in seen:
                seen.add(w); st.append(w)
    assert seen == names

def v_checkpoint(a):
    stdin_grid(a["text"], "#.SCE", "SCE")

def v_jobs(a):
    assert all(0 <= x < a["n"] and 0 <= y < a["n"] for x, y in a["rules"])

VALID = {"ci-flood-reach": v_flood, "ci-loop-cables": v_loop, "ci-line-from-pairs": v_line,
         "ci-checkpoint-route": v_checkpoint, "ci-stuck-jobs": v_jobs}

# ======================= independent methods =======================

def wet_cells(heights, r, c):
    rows, cols = len(heights), len(heights[0])
    if rows * cols <= SMALL:
        # sweep until nothing changes: a cell is wet when a wet neighbour is at least as high
        wet = {(r, c)}
        changed = True
        while changed:
            changed = False
            for i in range(rows):
                for j in range(cols):
                    if (i, j) in wet:
                        continue
                    for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                        if (a, b) in wet and heights[a][b] >= heights[i][j]:
                            wet.add((i, j)); changed = True
                            break
        return len(wet)
    seen = {(r, c)}
    q = deque([(r, c)])
    while q:
        i, j = q.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < rows and 0 <= b < cols and (a, b) not in seen and heights[a][b] <= heights[i][j]:
                seen.add((a, b)); q.append((a, b))
    return len(seen)

def loop_cables(n, cables):
    if n <= SMALL:
        near = defaultdict(set); out = []
        for i, (a, b) in enumerate(cables):
            seen, st = {a}, [a]
            while st:
                u = st.pop()
                for w in near[u]:
                    if w not in seen:
                        seen.add(w); st.append(w)
            if b in seen:
                out.append(i)
            near[a].add(b); near[b].add(a)
        return out
    # union by size, with path halving
    par, size, out = list(range(n)), [1] * n, []
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for i, (a, b) in enumerate(cables):
        x, y = f(a), f(b)
        if x == y:
            out.append(i); continue
        if size[x] < size[y]: x, y = y, x
        par[y] = x; size[x] += size[y]
    return out

def rebuild_line(pairs):
    names = sorted({s for p in pairs for s in p})
    if len(names) <= 7:
        need = {frozenset(p) for p in pairs}
        lines = [list(o) for o in permutations(names) if {frozenset(o[i:i + 2]) for i in range(len(o) - 1)} == need]
        return min(l if l[0] < l[-1] else l[::-1] for l in lines)
    # grow outwards from the first pair, then orient
    near = defaultdict(list)
    for x, y in pairs:
        near[x].append(y); near[y].append(x)
    line = deque(pairs[0]); used = set(pairs[0])
    for side in (0, 1):
        while True:
            end = line[-1] if side else line[0]
            nxt = [w for w in near[end] if w not in used]
            if not nxt: break
            used.add(nxt[0])
            if side: line.append(nxt[0])
            else: line.appendleft(nxt[0])
    line = list(line)
    return line if line[0] < line[-1] else line[::-1]

def solve_checkpoint_route(text):
    tok = text.split()
    R, C = int(tok[0]), int(tok[1])
    g = tok[2:2 + R]
    s = next((i, j) for i in range(R) for j in range(C) if g[i][j] == "S")
    # one search over states (cell, checkpoint scanned yet)
    start = (s[0], s[1], g[s[0]][s[1]] == "C")
    dist = {start: 0}; q = deque([start])
    while q:
        i, j, k = q.popleft()
        if k and g[i][j] == "E":
            return str(dist[(i, j, k)])
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and g[a][b] != "#":
                st = (a, b, k or g[a][b] == "C")
                if st not in dist:
                    dist[st] = dist[(i, j, k)] + 1; q.append(st)
    return "-1"

def stuck_jobs(n, rules):
    adj = defaultdict(list)
    for a, b in rules:
        adj[a].append(b)
    if n <= SMALL:
        def reach(v):   # nodes reachable from v by one or more rules
            seen, st = set(), list(adj[v])
            while st:
                u = st.pop()
                if u not in seen:
                    seen.add(u); st.extend(adj[u])
            return seen
        R = {v: reach(v) for v in range(n)}
        on_cycle = [v for v in range(n) if v in R[v]]
        bad = set()
        for v in on_cycle:
            bad |= R[v] | {v}
        return sorted(bad)
    # Kosaraju, iterative: a job is stuck when it is reachable from a strongly connected part with a cycle
    order, seen = [], [False] * n
    for s in range(n):
        if seen[s]: continue
        seen[s] = True; st = [(s, 0)]
        while st:
            v, i = st.pop()
            if i < len(adj[v]):
                st.append((v, i + 1)); w = adj[v][i]
                if not seen[w]:
                    seen[w] = True; st.append((w, 0))
            else:
                order.append(v)
    radj = defaultdict(list)
    for a, b in rules:
        radj[b].append(a)
    comp = [-1] * n; c = 0
    for s in reversed(order):
        if comp[s] >= 0: continue
        comp[s] = c; st = [s]
        while st:
            v = st.pop()
            for w in radj[v]:
                if comp[w] < 0:
                    comp[w] = c; st.append(w)
        c += 1
    size = Counter(comp)
    cyc = {comp[a] for a, b in rules if a == b} | {k for k, s in size.items() if s > 1}
    bad = [False] * n; st = [v for v in range(n) if comp[v] in cyc]
    for v in st: bad[v] = True
    while st:
        v = st.pop()
        for w in adj[v]:
            if not bad[w]:
                bad[w] = True; st.append(w)
    return [v for v in range(n) if bad[v]]

INDEP = {"ci-flood-reach": wet_cells, "ci-loop-cables": loop_cables, "ci-line-from-pairs": rebuild_line,
         "ci-checkpoint-route": solve_checkpoint_route, "ci-stuck-jobs": stuck_jobs}

# ======================= slow methods kept out of `planted` =======================
SLOW = {}
# planted solutions that are right but too slow (always the last entry): (drill id, index)
SLOW_PLANTED = set()
# the obvious method timed in Pyodide for each difficulty 4 and 5 drill: (drill id, planted index) or SLOW key
OBVIOUS = {}

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
    if spec.get("stop") and first is not None:
        break
print(json.dumps({"failed": first, "s": round(time.time() - t0, 2)}))
"""

def run_isolated(code, cases, limit=10, stop=False):
    try:
        r = subprocess.run([sys.executable, "-c", RUNNER], input=json.dumps({"code": code, "cases": cases, "stop": stop}),
                           capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        return {"failed": "timeout", "s": limit}
    return json.loads(r.stdout.strip().splitlines()[-1])

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
    """seconds Pyodide takes over the cases (stops after `cap` seconds; a run cut off reports more than 5)"""
    with tempfile.TemporaryDirectory() as tmp:
        spec, script, js = (os.path.join(tmp, f) for f in ("spec.json", "t.py", "t.mjs"))
        json.dump({"code": code, "cases": cases, "cap": cap}, open(spec, "w"))
        open(script, "w").write("SPEC_PATH = '/spec.json'\n" + PYO_SCRIPT)
        open(js, "w").write(PYO_JS)
        pkg = os.path.join(PYODIDE, "pyodide-0.27.7", "package")
        try:
            r = subprocess.run(["node", js, pkg, spec, script], capture_output=True, text=True, timeout=cap + 60)
        except subprocess.TimeoutExpired:
            return {"s": cap, "ok": None}
        line = [l for l in r.stdout.splitlines() if l.startswith("PYO ")]
        if not line:
            return {"s": None, "ok": None, "err": r.stderr[-300:]}
        return json.loads(line[-1][4:])

diffs = Counter()
stdin = 0
timings = {}
for did in IDS:
    d = json.load(open(os.path.join(DRILLS, did + ".json")))
    cases = d["examples"] + d["tests"]
    fn = d["fn"]
    objs = [c for c in d["constraints"] if isinstance(c, dict)]
    if not objs:
        err(f"{did}: no constraint objects")
    for c in cases:
        for a in capture_args(d, c["call"]):
            for o in objs:
                if o["arg"] in a:
                    for m in violations(o, a[o["arg"]], o["arg"]):
                        err(f"{did}: {c['call'][:50]}: {m}")
            try:
                VALID[did](a)
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
    ins = {fn: INDEP[did]}
    for c in cases:
        if eval(c["call"], ins) != eval(c["expect"]):
            err(f"{did}: independent method disagrees on {c['call'][:60]}")
    sres = run_isolated(d["starter"], d["tests"])
    if sres["failed"] is None:
        err(f"{did}: starter passes every test")
    pl = d.get("planted", [])
    if len(pl) < 2:
        err(f"{did}: fewer than two planted")
    caught = []
    for k, p in enumerate(pl):
        if (did, k) in SLOW_PLANTED:
            if k != len(pl) - 1:
                err(f"{did}: slow planted[{k}] is not last")
            r = run_isolated(p["code"], d["tests"], limit=5)
            if r["failed"] != "timeout":
                err(f"{did}: planted[{k}] is meant to be too slow but finished ({r})")
            caught.append("timeout (slow plant)")
            continue
        r = run_isolated(p["code"], d["tests"], limit=2.5)
        if r["failed"] == "timeout":
            err(f"{did}: planted[{k}] runs past 2.5 s in CPython, so it could time out in the browser")
        elif r["failed"] is None:
            err(f"{did}: planted[{k}] passes every hidden test ({p['slip']})")
        caught.append(f"test {r['failed']} in {r['s']} s")
    slow_out = []
    for k, code in enumerate(SLOW.get(did, [])):
        hit = None
        for i, c in enumerate(d["tests"]):
            r = run_isolated(code, [c], limit=5)
            if r["failed"] == "timeout":
                hit = i
                break
        if hit is None:
            err(f"{did}: slow method {k} finishes every hidden test inside 5 s")
        slow_out.append(hit)
    if d["difficulty"] >= 4:
        if did not in OBVIOUS:
            err(f"{did}: difficulty {d['difficulty']} needs an obvious method in OBVIOUS")
        if "obvious method" not in d["how"] or "step to the target" not in d["how"]:
            err(f"{did}: how must name the obvious method and the step to the target")
        if PYODIDE and did in OBVIOUS:
            src = OBVIOUS[did]
            code = pl[src][ "code"] if isinstance(src, int) else SLOW[did][int(src[1:])]
            tm = pyodide_time(d["solution"], d["tests"])
            ts = pyodide_time(code, d["tests"])
            timings[did] = (tm["s"], ts["s"])
            if tm["s"] is None or tm["s"] > 1.0 or not tm["ok"]:
                err(f"{did}: model in Pyodide {tm}")
            if ts["s"] is None or ts["s"] <= 5.0:
                err(f"{did}: obvious method in Pyodide {ts}")
            print(f"  {did}: Pyodide model {tm['s']} s, obvious {ts['s']} s{' (cut off)' if ts['s'] and ts['s'] >= 12 else ''}")
    diffs[d["difficulty"]] += 1
    stdin += "stdin" in d["tags"]
    if d["tags"][0] != "pack-5": err(f"{did}: tags must start pack-5")
    if not 900 <= d["pace"] <= 2700: err(f"{did}: pace {d['pace']}")
    if not 10 <= len(d["tests"]) <= 15: err(f"{did}: {len(d['tests'])} tests")
    if not 2 <= len(d["examples"]) <= 3 or not all(e.get("note") for e in d["examples"]): err(f"{did}: examples")
    if len(d["notes"]) != 3: err(f"{did}: notes")
    if d["pack"] != "ci" or d["course"] != "coding-int": err(f"{did}: pack or course")
    if d["pattern"] != "graphs": err(f"{did}: pattern {d['pattern']}")
    if f"Submit runs {len(d['tests'])} hidden tests" not in d["how"]: err(f"{did}: how test count")
    print(f"{did}: d{d['difficulty']} {len(d['tests'])} tests ok, model {dt:.2f} s, starter fails at {sres['failed']}, planted fail at {caught}, slow methods time out at {slow_out}")
if FULL and dict(diffs) != {2: 3, 3: 5, 4: 5, 5: 2}: err(f"difficulty mix {dict(diffs)}")
if FULL and stdin != 2: err(f"{stdin} stdin drills")
print(f"{len(IDS)} drills, {len(errors)} errors")
sys.exit(1 if errors else 0)
