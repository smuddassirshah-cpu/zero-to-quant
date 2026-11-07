"""Second read of the five fixer-written exam items (topic-0.2, 0.3, 1.1, 1.2).

Run from the repository root:  python3 docs/reviews/exam-fixer-items-scripts/numbers.py
Optional: PYTEST_PY=<python with pytest 8.1.1> for the real fixture count.
Exit 0 only when every check passes. Checks named FIX-n are content findings
(review-exam-fixer-items.md finding n): they fail until the fix is applied.
"""
import os, sys
# this file is named numbers.py, which shadows the stdlib module fractions needs
_here = os.path.dirname(os.path.abspath(__file__))
sys.path = [q for q in sys.path if os.path.abspath(q or ".") != _here]
import ast, contextlib, io, json, math, re, subprocess, tempfile
from fractions import Fraction as F

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
EX = os.path.join(ROOT, "app", "content", "exams")
CO = os.path.join(ROOT, "app", "content", "courses")
results = []

def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))

def item(exam, iid):
    d = json.load(open(os.path.join(EX, exam + ".json")))
    for i, it in enumerate(d["items"]):
        if it.get("id") == iid:
            return i, it
    raise SystemExit("missing " + iid)

def strings(o):
    if isinstance(o, dict):
        for v in o.values(): yield from strings(v)
    elif isinstance(o, list):
        for v in o: yield from strings(v)
    elif isinstance(o, str):
        yield o

def code_block(prose):
    m = re.search(r"```python\n(.*?)```", prose, re.S)
    return m.group(1)

def run(src, env=None):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(src, env if env is not None else {})
    return buf.getvalue().strip()

# ---------------------------------------------------------------- voice, all five
ITEMS = {
    "e-gen-once": item("topic-1.1", "e-gen-once"),
    "e-assert-catch": item("topic-1.1", "e-assert-catch"),
    "e-fixture-calls": item("topic-1.2", "e-fixture-calls"),
    "e-gap-table": item("topic-0.2", "e-gap-table"),
    "e-truss-angle": item("topic-0.3", "e-truss-angle"),
}
def prose_words(s):
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = re.sub(r"\$\$.*?\$\$|\$[^$]*\$|`[^`]*`", " X ", s)
    return s
for iid, (idx, it) in ITEMS.items():
    allt = " ".join(strings(it))
    check(f"voice {iid}: no em/en dash", "—" not in allt and "–" not in allt)
    check(f"voice {iid}: no exclamation", "!" not in prose_words(allt))
    longest = 0
    for s in strings({k: v for k, v in it.items() if k not in ("id",)}):
        for sent in re.split(r"(?<=[.?])\s+", prose_words(s)):
            longest = max(longest, len(sent.split()))
    check(f"voice {iid}: sentences under 35 words", longest < 35, f"longest {longest}")
    ex = prose_words(it["explain"]["text"])
    n = len([x for x in re.split(r"(?<=[.?])\s+", ex.strip()) if x])
    check(f"voice {iid}: explanation at most three sentences", n <= 3, f"{n}")
    for w in ("color", "center", "analyze", "behavior", "favorite", "$ "):
        pass
    check(f"voice {iid}: no US spellings", not re.search(r"\b(color|center|analyz|behavior|favor)", allt))

# ---------------------------------------------------------------- e-gen-once
i, it = ITEMS["e-gen-once"]
src = code_block(it["prose"])
out = run(src)
key = [o for o in it["widget"]["options"] if o.get("correct")][0]["text"].strip("`")
check("e-gen-once: shown code prints the key", out == key, out)
closes = [100.0, 110.0, 99.0]
check("e-gen-once: pairs = closes - 1 = 2 (route 2)", len(closes) - 1 == 2 == len(list(zip(closes, closes[1:]))))
r = [b / a - 1 for a, b in zip(closes, closes[1:])]
check("e-gen-once: returns 0.1 and -0.1 as stated", math.isclose(r[0], 0.1) and math.isclose(r[1], -0.1))
check("e-gen-once: distractor 3 0 = closes counted", len(closes) == 3)
# freshness evidence: py-found l13 screens[6] is the same trap
l13 = json.load(open(os.path.join(CO, "py-found", "l13-one-at-a-time.json")))
s6 = l13["screens"][6]
check("e-gen-once evidence: l13 screens[6] uses up a generator then lists it",
      "print(max(dd))" in s6["prose"] and "print(list(dd))" in s6["prose"])
hw4 = json.load(open(os.path.join(CO, "py-found", "homework-4.json")))
check("e-gen-once evidence: homework-4 items[2] is the same trap", "max(c)" in hw4["items"][2]["prose"])
# proposed fix (finding 1)
FIX1 = '''def gains(closes):
    for a, b in zip(closes, closes[1:]):
        yield b / a - 1

g = gains([80.0, 84.0, 82.0, 86.0, 85.0])
for r in g:
    if r < 0:
        break
print(len(list(g)))
'''
check("fix 1 proposal: prints 2", run(FIX1) == "2")
cl = [80.0, 84.0, 82.0, 86.0, 85.0]
gs = [b / a - 1 for a, b in zip(cl, cl[1:])]
first_neg = next(k for k, x in enumerate(gs) if x < 0)
check("fix 1 proposal: 4 returns, first negative is the 2nd, 2 left (route 2)",
      len(gs) == 4 and first_neg == 1 and len(gs) - (first_neg + 1) == 2)
check("fix 1 proposal: slips 4 (replay), 0 (used up), 3 (value handed back) differ from 2",
      len({2, 4, 0, 3}) == 4)
check("FIX-1 applied: e-gen-once stops the generator part-way", "break" in it["prose"])

# ---------------------------------------------------------------- e-assert-catch
i, it = ITEMS["e-assert-catch"]
src = code_block(it["prose"])
def true_mdd(cs):
    peak, w = cs[0], 0.0
    for c in cs:
        peak = max(peak, c); w = max(w, 1 - c / peak)
    return w
def fails(assert_src, fn):
    env = {"math": math, "max_drawdown": fn}
    try:
        exec(assert_src, env); return False
    except AssertionError:
        return True
benv = {}; exec(src, benv); buggy = benv["max_drawdown"]
fail_ids, correct_ids = [], []
for o in it["widget"]["options"]:
    a = o["text"].strip("`")
    if fails(a, buggy): fail_ids.append(o["id"])
    check(f"e-assert-catch: option {o['id']} passes on a correct max_drawdown", not fails(a, true_mdd))
    if o.get("correct"): correct_ids.append(o["id"])
check("e-assert-catch: keyed options are exactly the failing asserts", fail_ids == correct_ids == ["b", "d"], f"{fail_ids}")
# route 2: from-first-close closed form max(0, 1 - min/first)
ff = lambda cs: max(0.0, 1 - min(cs) / cs[0])
check("e-assert-catch: buggy values 0.2, 0.1, 0.0, 0.0 (two routes)",
      [round(buggy(p), 10) for p in ([100.0, 80.0], [100.0, 120.0, 90.0], [100.0, 110.0, 121.0], [50.0, 100.0, 75.0])]
      == [round(ff(p), 10) for p in ([100.0, 80.0], [100.0, 120.0, 90.0], [100.0, 110.0, 121.0], [50.0, 100.0, 75.0])]
      == [0.2, 0.1, 0.0, 0.0])
check("e-assert-catch: explain 'true 0.25' for both rising paths",
      math.isclose(true_mdd([100.0, 120.0, 90.0]), 0.25) and math.isclose(true_mdd([50.0, 100.0, 75.0]), 0.25)
      and math.isclose((120 - 90) / 120, 0.25) and math.isclose((100 - 75) / 100, 0.25))
pl6 = json.load(open(os.path.join(CO, "pytest", "l6-many-inputs.json")))
check("e-assert-catch evidence: pytest l6 screens[1] tests the same from-first-price bug",
      "prices[0]" in pl6["screens"][1]["prose"] and "first price" in pl6["screens"][1]["prose"])
# proposed fix (finding 2): worst resets at each new high
FIX2 = '''def max_drawdown(closes):
    peak, worst = closes[0], 0.0
    for c in closes:
        if c > peak:
            peak, worst = c, 0.0
        worst = max(worst, 1 - c / peak)
    return worst
'''
e2 = {}; exec(FIX2, e2); bug2 = e2["max_drawdown"]
opts2 = {"a": ("[100.0, 80.0]", 0.2, False), "b": ("[100.0, 60.0, 120.0, 108.0]", 0.4, True),
         "c": ("[100.0, 90.0, 110.0, 77.0]", 0.3, False), "d": ("[200.0, 150.0, 220.0, 187.0]", 0.25, True)}
for k, (path, exp, keyed) in opts2.items():
    a = f"assert math.isclose(max_drawdown({path}), {exp})"
    check(f"fix 2 proposal: option {k} passes on a correct max_drawdown", not fails(a, true_mdd))
    check(f"fix 2 proposal: option {k} fails on the bug iff keyed", fails(a, bug2) == keyed)
check("fix 2 proposal: bug gives 0.1 and 0.15 on the keyed paths (two routes)",
      math.isclose(bug2([100.0, 60.0, 120.0, 108.0]), 0.1) and math.isclose(1 - 108 / 120, 0.1)
      and math.isclose(bug2([200.0, 150.0, 220.0, 187.0]), 0.15) and math.isclose((220 - 187) / 220, 0.15))
check("fix 2 proposal: true 0.4 and 0.25, and path c's earlier fall is 0.1",
      math.isclose(1 - 60 / 100, 0.4) and math.isclose(1 - 150 / 200, 0.25) and math.isclose(1 - 90 / 100, 0.1)
      and math.isclose(true_mdd([100.0, 90.0, 110.0, 77.0]), 0.3) and math.isclose(bug2([100.0, 90.0, 110.0, 77.0]), 0.3))
check("FIX-2 applied: e-assert-catch uses a bug the courses have not tested", "peak, worst = c, 0.0" in it["prose"])

# ---------------------------------------------------------------- e-fixture-calls
i, it = ITEMS["e-fixture-calls"]
src = code_block(it["prose"])
tree = ast.parse(src)
n_calls = n_tests = n_funcs = 0
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
        rows = 1
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call) and getattr(dec.func, "attr", "") == "parametrize":
                rows *= len(dec.args[1].elts)
        n_tests += rows
        if any(a.arg == "closes" for a in node.args.args):
            n_calls += rows; n_funcs += 1
w = {x["id"]: x["value"] for x in it["widget"]["wrong"]}
check("e-fixture-calls: key 4 by counting (route 1)", it["widget"]["answer"] == n_calls == 4)
check("e-fixture-calls: per-function slip 2 = test functions naming closes", w["per-function"] == n_funcs == 2)
check("e-fixture-calls: every-test slip 5 = tests pytest reports", w["every-test"] == n_tests == 5)
check("e-fixture-calls: once slip is 1", w["once"] == 1)
py = os.environ.get("PYTEST_PY", sys.executable)
probe = subprocess.run([py, "-c", "import pytest"], capture_output=True)
if probe.returncode == 0:
    with tempfile.TemporaryDirectory() as td:
        counted = src.replace("def closes():\n", "def closes():\n    CALLS.append(1)\n", 1)
        body = "import pytest\nCALLS = []\n" + counted + "\ndef test_zz_report():\n    print('CALLS', len(CALLS))\n"
        open(os.path.join(td, "test_shown.py"), "w").write(body)
        p = subprocess.run([py, "-m", "pytest", "-q", "-s", "-p", "no:cacheprovider", "test_shown.py"],
                           cwd=td, capture_output=True, text=True)
        m = re.search(r"CALLS (\d+)", p.stdout)
        check("e-fixture-calls: real pytest builds closes() 4 times (route 2)", m and int(m.group(1)) == 4, p.stdout[-200:])
        check("e-fixture-calls evidence: the shown file raises NameError in test_no_prices",
              "NameError" in p.stdout and "1 failed, 5 passed" in p.stdout)
else:
    check("e-fixture-calls: real pytest available (set PYTEST_PY)", False)
check("FIX-3 applied: e-fixture-calls imports pytest and daily_returns",
      "import pytest" in it["prose"] and "import daily_returns" in it["prose"])

# ---------------------------------------------------------------- e-gap-table
i, it = ITEMS["e-gap-table"]
xs, ys = [1, 3, 4, 7], [-4, 2, 5, 14]
check("e-gap-table: prose lists inputs 1, 3, 4, 7 and outputs -4, 2, 5, 14",
      "Inputs 1, 3, 4 and 7 give outputs −4, 2, 5 and 14" in it["prose"])
check("e-gap-table: 3x - 7 fits every row", all(3 * x - 7 == y for x, y in zip(xs, ys)))
slopes = {F(ys[k + 1] - ys[k], xs[k + 1] - xs[k]) for k in range(3)}
check("e-gap-table: every step climbs 3 per unit (route 2)", slopes == {3})
check("e-gap-table: input steps 2, 1, 3 (not equal)", [xs[k + 1] - xs[k] for k in range(3)] == [2, 1, 3])
check("e-gap-table: c from f(1) = 3 + c = -4", -4 - 3 == -7)
check("e-gap-table: first-climb 6x - 10 is the 6 as m, through (1, -4); fits only row 1",
      6 * 1 - 10 == -4 and [6 * x - 10 == y for x, y in zip(xs, ys)] == [True, False, False, False])
check("e-gap-table: 6 / 2 = 3 in byKey", 6 / 2 == 3 and ys[1] - ys[0] == 6)
fl2 = json.load(open(os.path.join(CO, "functions", "l2-table-to-rule.json")))
check("e-gap-table evidence: l2 screens[3] has a table with inputs not in ones and the same climb-m slip",
      "do not go up in ones" in fl2["screens"][3]["prose"]
      and any(o.get("id") == "climb-m" for o in fl2["screens"][3]["widget"]["options"]))
check("e-gap-table evidence: l2 screens[9] has unequal input steps (1.00 then 1.50)",
      [r[0] for r in fl2["screens"][9]["canvas"]["params"]["rows"]] == ["£15.00", "£16.00", "£17.50"])
# proposed fix (finding 5): one output miscopied
fx, fy = [1, 3, 4, 7], [-4, 3, 5, 14]
fits = [3 * x - 7 == y for x, y in zip(fx, fy)]
check("fix 5 proposal: 3x - 7 fits rows 1, 3, 4 and breaks row 2 (it should be 2)", fits == [True, False, True, True] and 3 * 3 - 7 == 2)
m12 = F(fy[1] - fy[0], fx[1] - fx[0]); c12 = fy[0] - m12 * fx[0]
check("fix 5 proposal: first two rows give 7/2 x - 15/2, which gives 6.5 at 4", m12 == F(7, 2) and c12 == F(-15, 2) and m12 * 4 + c12 == F(13, 2))
check("fix 5 proposal: first-climb 7x - 11 through (1, -4)", fy[1] - fy[0] == 7 and -4 - 7 == -11)
check("fix 5 proposal: (1,-4)-(4,5) and (4,5)-(7,14) both climb 3 per unit (route 2)",
      F(5 - (-4), 4 - 1) == 3 and F(14 - 5, 7 - 4) == 3)
check("FIX-5 applied: e-gap-table has a miscopied row", "copied wrongly" in it["prose"] + it["question"])

# ---------------------------------------------------------------- e-truss-angle
i, it = ITEMS["e-truss-angle"]
th = math.degrees(math.acos(5 / 7))
th2 = math.degrees(math.acos((10 ** 2 + 7 ** 2 - 7 ** 2) / (2 * 10 * 7)))   # cosine rule at a base corner
apex = math.degrees(math.acos((7 ** 2 + 7 ** 2 - 10 ** 2) / (2 * 7 * 7)))   # cosine rule at the apex
wr = {x["id"]: x for x in it["widget"]["wrong"]}
check("e-truss-angle: key acos(5/7) = 44.4153 (two routes)", abs(th - 44.4153) < 5e-5 and abs(th2 - th) < 1e-9 and abs(it["widget"]["answer"] - th) < 5e-5)
check("e-truss-angle: angles add to 180", abs(2 * th + apex - 180) < 1e-9)
check("e-truss-angle: apex slip 91.17", abs(wr["apex"]["value"] - apex) < 0.005 and abs(180 - 2 * th - 91.17) < 0.005)
check("e-truss-angle: vertical slip asin(5/7) = 45.58 = half the apex",
      abs(wr["vertical"]["value"] - math.degrees(math.asin(5 / 7))) < 0.005 and abs(apex / 2 - 45.58) < 0.005)
check("e-truss-angle: radians slip acos(5/7) = 0.7752 rad", abs(wr["radians"]["value"] - math.acos(5 / 7)) < 5e-5)
check("e-truss-angle: 44.4 accepted, 44.3 and 44.5 not", abs(44.4 - th) <= 0.05 and abs(44.3 - th) > 0.05 and abs(44.5 - th) > 0.05)
tol = it["widget"]["tol"]["abs"]
check("e-truss-angle: no wrong window overlaps the key window",
      all(abs(x["value"] - th) > tol + x["tol"]["abs"] for x in it["widget"]["wrong"]))
check("e-truss-angle: half base 5, hypotenuse 7 in feedback and explain",
      "tfrac57" in it["feedback"]["correct"] and "hypotenuse 7 and adjacent side 5" in it["explain"]["text"])

# ---------------------------------------------------------------- report
bad = [r for r in results if not r[1]]
for name, ok, d in results:
    print(("PASS " if ok else "FAIL ") + name + (f"  [{d}]" if d and not ok else ""))
print(f"{len(results) - len(bad)} of {len(results)} checks pass")
sys.exit(1 if bad else 0)
