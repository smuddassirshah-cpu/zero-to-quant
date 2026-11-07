"""Recompute every number in game-theory homework-1 `hw1-street-carts` (performance task, code).

Route A: the item's own solution, run through a copy of the engine's grading (code.js: setup, then
eval of the call, `equal` as == after tolist, `isclose` element by element at rel 1e-9, abs 1e-12).
Route B: independent re-derivations: street cells by the midpoint between the carts with exact
Fractions, best replies with NumPy, and a few cells worked by hand. Then the starter and thirteen
planted wrong solutions are run against every test. Exits 0 only if every check holds.
"""
import json
import math
import pathlib
import sys
from fractions import Fraction

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
HW = ROOT / "app/content/courses/game-theory/homework-1.json"
doc = json.loads(HW.read_text())
item = next(i for i in doc["items"] if i["id"] == "hw1-street-carts")
w = item["widget"]
fails = 0
checks = 0


def check(ok, msg):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("FAIL:", msg)


# ---------- engine-like grading ----------
def flat(v):
    return v.tolist() if hasattr(v, "tolist") and not isinstance(v, (int, float, complex, str)) else v


def close(x, y):
    x, y = flat(x), flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def run(src, case):
    ns = {}
    try:
        exec(src, ns)
        if case.get("setup"):
            exec(case["setup"], ns)
        got = eval(case["call"], ns)
        exp = eval(case["expect"], ns)
    except Exception:
        return False
    if case["compare"] == "isclose":
        return close(got, exp)
    try:
        return bool(flat(got) == flat(exp))
    except Exception:
        return False


tests, examples = w["tests"], w["examples"]

# ---------- shape ----------
check(item["performance"] == "code", "kind is code")
check(len(tests) >= 3 and len(tests) > len(examples), "more tests than examples")
check(f"runs {len(tests)} hidden tests" in w["how"], "how names the test count")
check(len(doc["items"]) <= 12, "homework at most 12 items")
check(any(i["difficulty"] == 5 for i in doc["items"]), "a difficulty 5 present")
check(sum(1 for i in doc["items"] if i.get("performance")) == 1, "one performance task")

# ---------- route A: solution passes everything ----------
for k, c in enumerate(examples + tests):
    check(run(w["solution"], c), f"solution fails case {k}")

# ---------- route B: independent recomputation of every expect ----------
def table_mid(homes, xs, ys, a, b):
    out = []
    for x in xs:
        row = []
        for y in ys:
            if x == y:
                sa = sb = Fraction(len(homes), 2)
            else:
                mid = Fraction(x + y, 2)
                side = lambda p: (p > mid) - (p < mid)
                sa = sum(Fraction(1) if side(h) == side(x) else Fraction(1, 2) if side(h) == 0 else 0 for h in homes)
                sb = len(homes) - sa
            row.append((a * sa, b * sb))
        out.append(row)
    return out


def replies_np(t):
    A = np.array([[c[0] for c in r] for r in t], dtype=object)
    B = np.array([[c[1] for c in r] for r in t], dtype=object)
    ana = [[int(i) for i in np.flatnonzero(A[:, j] == max(A[:, j]))] for j in range(A.shape[1])]
    ben = [[int(j) for j in np.flatnonzero(B[i, :] == max(B[i, :]))] for i in range(B.shape[0])]
    return [ana, ben]


envB = {"street_table": table_mid, "best_replies": lambda t: replies_np(t)}
for k, c in enumerate(examples + tests):
    ns = dict(envB)
    if c.get("setup"):
        exec(c["setup"], ns)
    got = eval(c["call"], ns)
    exp = eval(c["expect"])
    ok = close(got, exp) if c["compare"] == "isclose" else [[list(r) for r in s] for s in got] == exp
    check(ok, f"route B disagrees on case {k}: {got} vs {exp}")

# ---------- cells by hand ----------
# Example: homes 0..4, Ana at 1, Ben at 3: homes 0, 1 Ana's; 2 halfway; 3, 4 Ben's. 2.5 coffees each.
check(table_mid([0, 1, 2, 3, 4], [1], [3], 2, 3)[0][0] == (5, Fraction(15, 2)), "hand cell (1, 3) = (5, 7.5)")
# Ana at 2 and Ben at 3: homes 0, 1, 2 Ana's (3 coffees, £6); 3, 4 Ben's (2 coffees, £6).
check(table_mid([0, 1, 2, 3, 4], [2], [3], 2, 3)[0][0] == (6, 6), "hand cell (2, 3) = (6, 6)")
# Test 2: Ana at 1 and Ben at 1 share a spot: 7 homes, 3.5 coffees each: £7 and £10.50.
check(table_mid([0, 1, 1, 4, 6, 6, 6], [1], [1], 2, 3)[0][0] == (7, Fraction(21, 2)), "hand cell shared spot = (7, 10.5)")
# Test 2: Ana at 4, Ben at 5, midpoint 4.5: homes 0, 1, 1, 4 Ana's (4 x £2 = 8); 6, 6, 6 Ben's (3 x £3 = 9).
check(table_mid([0, 1, 1, 4, 6, 6, 6], [4], [5], 2, 3)[0][0] == (8, 9), "hand cell (4, 5) = (8, 9)")
# Coffees always add up to the number of homes, in every cell of every street the tests use.
for spec in [([0, 1, 2, 3, 4], [1, 2], [2, 3], 2, 3), ([0, 1, 1, 4, 6, 6, 6], [4, 1, 6], [1, 5], 2, 3),
             ([3, 0, 7, 2, 2, 9], [5, 2], [2, 8, 5], 1, 4), (list(range(11)), [0, 2, 4, 6, 8, 10], [0, 2, 4, 6, 8, 10], 2, 3),
             ([0, 0, 0, 1, 5, 9, 10], [8, 0, 5, 3], [9, 1, 5], 3, 2)]:
    homes, xs, ys, a, b = spec
    for r in table_mid(*spec):
        for pa, pb in r:
            check(pa / a + pb / b == len(homes), f"coffees add to homes in {spec}")

# ---------- starter fails every test ----------
for k, c in enumerate(tests):
    check(not run(w["starter"], c), f"starter passes test {k + 1}")

# ---------- planted wrong solutions ----------
SOL = w["solution"]
def swap(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)

BR_HEAD = SOL[SOL.index("def best_replies"):]
ST_HEAD = SOL[:SOL.index("def best_replies")]
bugs = {
    "Ana reads Ben's number": swap("table[i][j][0] for i in range(m))\n        ana.append([i for i in range(m) if table[i][j][0] == top])",
                                   "table[i][j][1] for i in range(m))\n        ana.append([i for i in range(m) if table[i][j][1] == top])"),
    "Ben reads Ana's number": swap("table[i][j][1] for j in range(n))\n        ben.append([j for j in range(n) if table[i][j][1] == top])",
                                   "table[i][j][0] for j in range(n))\n        ben.append([j for j in range(n) if table[i][j][0] == top])"),
    "ties dropped": ST_HEAD + '''def best_replies(table):
    m, n = len(table), len(table[0])
    ana = [[max(range(m), key=lambda i: table[i][j][0])] for j in range(n)]
    ben = [[max(range(n), key=lambda j: table[i][j][1])] for i in range(m)]
    return ana, ben
''',
    "Ana read along a row": ST_HEAD + '''def best_replies(table):
    m, n = len(table), len(table[0])
    ana = []
    for i in range(m):
        top = max(table[i][j][0] for j in range(n))
        ana.append([j for j in range(n) if table[i][j][0] == top])
    ben = []
    for i in range(m):
        top = max(table[i][j][1] for j in range(n))
        ben.append([j for j in range(n) if table[i][j][1] == top])
    return ana, ben
''',
    "best starts at 0": ST_HEAD + '''def best_replies(table):
    m, n = len(table), len(table[0])
    ana = []
    for j in range(n):
        best, rows = 0, []
        for i in range(m):
            v = table[i][j][0]
            if v > best:
                best, rows = v, [i]
            elif v == best:
                rows.append(i)
        ana.append(rows)
    ben = []
    for i in range(m):
        best, cols = 0, []
        for j in range(n):
            v = table[i][j][1]
            if v > best:
                best, cols = v, [j]
            elif v == best:
                cols.append(j)
        ben.append(cols)
    return ana, ben
''',
    "best cell of the whole table": ST_HEAD + '''def best_replies(table):
    m, n = len(table), len(table[0])
    ta = max(c[0] for r in table for c in r)
    tb = max(c[1] for r in table for c in r)
    ana = [[i for i in range(m) if table[i][j][0] == ta] for j in range(n)]
    ben = [[j for j in range(n) if table[i][j][1] == tb] for i in range(m)]
    return ana, ben
''',
    "halfway home to Ana": swap("if abs(h - x) < abs(h - y):", "if abs(h - x) <= abs(h - y):"),
    "halfway home to nobody": swap("ana += 0.5\n                    ben += 0.5", "pass"),
    "one price for both": swap("row.append((a * ana, b * ben))", "row.append((a * ana, a * ben))"),
    "repeated homes counted once": swap("for h in homes:", "for h in set(homes):"),
    "table transposed": swap("for x in ana_spots:\n        row = []\n        for y in ben_spots:",
                             "for y in ben_spots:\n        row = []\n        for x in ana_spots:"),
    "Ana assumed on the left": ST_HEAD.replace(ST_HEAD, '''def street_table(homes, ana_spots, ben_spots, a, b):
    table = []
    for x in ana_spots:
        row = []
        for y in ben_spots:
            mid = (x + y) / 2
            ana = sum(1 if h < mid else 0.5 if h == mid else 0 for h in homes)
            ben = len(homes) - ana
            row.append((a * ana, b * ben))
        table.append(row)
    return table


''') + BR_HEAD,
    "spots sorted first": swap("for x in ana_spots:", "for x in sorted(ana_spots):"),
}
for name, src in bugs.items():
    res = [run(src, c) for c in tests]
    first = next((k + 1 for k, r in enumerate(res) if not r), None)
    check(first is not None, f"planted bug passes every test: {name}")
    print(f"planted: {name:30s} fails tests {[k + 1 for k, r in enumerate(res) if not r]}")

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
