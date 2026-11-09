"""vectors level 3 performance task: every number recomputed twice, and the code graded.

Item: app/content/courses/vectors/homework-3.json#h-bond-curve (performance: code).
Run: <venv>/bin/python -I docs/reports/vectors-3-perf-numbers.py   (numpy and sympy; exits 0 when all checks pass)

Route 1: sympy exact arithmetic, C d = p solved by LU over the rationals (prices read as exact decimals).
Route 2: forward pricing with Fractions: the stated curves reprice every bond in the tests to the cent.
Route 3: numpy lstsq on the same matrix, built by a second, independent builder.
Refusals: exact sympy rank of C (and of [C | p]) for every refusal set.
Then a harness that mirrors code.js (source run once, setup and call in one namespace, isclose element by element with
the case tol, equal exact, raises by exception class or subclass, __learner_source__ defined) grades the shipped
solution, two other correct solutions, the starter and fourteen planted slips. Pyodide's NumPy returns nan for an
exactly singular solve or inverse (AUTHORING section 3); the harness patches np.linalg.solve and inv to do that,
and also runs CPython's own behaviour.
"""
import json, math, os, sys
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app", "content", "courses", "vectors", "homework-3.json")
doc = json.load(open(HW, encoding="utf-8"))
items = doc["items"]
idx = [i for i, it in enumerate(items) if it["id"] == "h-bond-curve"][0]
item = items[idx]
W = item["widget"]
fails = 0
checks = 0


def check(cond, msg):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", msg)


# ---------- structure ----------
check(idx == 9 and len(items) == 10, "appended as item 10 of 10 (index 9)")
check(item["performance"] == "code" and W["kind"] == "code" and W["language"] == "python", "kind")
check(len(W["tests"]) == 12 and len(W["examples"]) == 1 and len(W["tests"]) > len(W["examples"]), "12 tests, 1 example")
check(W["examples"][0] == W["tests"][0], "example is test 1")
check(6 <= len(items) <= 12, "homework size")
check(any(i.get("difficulty") == 5 for i in items), "a difficulty 5")
check(any(i.get("kind") == "longform" for i in items), "a longform")
check(sum(1 for i in items if i.get("performance")) == 1, "one performance item")
kinds = [t["compare"] for t in W["tests"]]
check(kinds.count("isclose") == 7 and kinds.count("raises") == 4 and kinds.count("equal") == 1, "7 isclose, 4 raises, 1 equal")
check("12 hidden tests on seven sets of bonds" in W["how"] and "seven compare arrays within 1e-9" in W["how"]
      and "four expect `ValueError`" in W["how"], "how counts")
bond_sets = []
for t in W["tests"]:
    if "setup" in t:
        g = {}
        exec(t["setup"], {}, g)
        if g["bonds"] not in bond_sets:
            bond_sets.append(g["bonds"])
check(len(bond_sets) == 7, "seven distinct sets of bonds")
check(all("tol" in t and t["tol"] == {"abs": 1e-9} for t in W["tests"] if t["compare"] == "isclose"), "tol 1e-9")


# ---------- the data, parsed back from the tests ----------
def parse(t):
    g = {}
    exec(t["setup"], {}, g)
    return g["bonds"], g["prices"], g["targets"]


def Q(v):
    return sp.Rational(str(v))


def rows_sym(bonds, m):
    out = []
    for c, T in bonds:
        r = [sp.Integer(0)] * m
        for t in range(T):
            r[t] = Q(c)
        r[T - 1] += 100
        out.append(r)
    return sp.Matrix(out)


def rows_np(bonds, m):
    # second builder: cash flow at year t is coupon for t <= T, plus 100 at t == T
    return np.array([[(c if t <= T else 0.0) + (100.0 if t == T else 0.0) for t in range(1, m + 1)] for c, T in bonds])


def route1(bonds, prices, targets):
    m = max(T for c, T in bonds)
    C = rows_sym(bonds, m)
    d = C.LUsolve(sp.Matrix([Q(p) for p in prices]))
    return d, rows_sym(targets, m) * d


def route3(bonds, prices, targets):
    m = max(T for c, T in bonds)
    d = np.linalg.lstsq(rows_np(bonds, m), np.array(prices, float), rcond=None)[0]
    return d, rows_np(targets, m) @ d


T = W["tests"]
for k in range(7):
    b, p, tg = parse(T[k])
    d1, v1 = route1(b, p, tg)
    d3, v3 = route3(b, p, tg)
    exp = eval(T[k]["expect"])
    got1 = [float(x) for x in (d1 if T[k]["call"].endswith("[0]") else v1)]
    got3 = (d3 if T[k]["call"].endswith("[0]") else v3).tolist()
    check(len(got1) == len(exp) and all(abs(a - e) < 1e-12 for a, e in zip(got1, exp)), f"test {k + 1} route 1 {got1}")
    check(len(got3) == len(exp) and all(abs(a - e) < 1e-9 for a, e in zip(got3, exp)), f"test {k + 1} route 3 {got3}")

# route 2: the stated round curves reprice every bond to the cent, by Fractions
def price_fr(bond, d):
    c, Tm = Fr(str(bond[0])), bond[1]
    return sum(c * d[t] for t in range(Tm)) + 100 * d[Tm - 1]

D1 = [Fr("0.96"), Fr("0.92"), Fr("0.88")]
D2 = [Fr("0.97"), Fr("0.93"), Fr("0.89")]
b, p, tg = parse(T[0])
check([price_fr(x, D1) for x in b] == [Fr(str(v)) for v in p], "set 1 prices from 0.96, 0.92, 0.88")
check([price_fr(x, D1) for x in tg] == [Fr("104.56"), Fr(92), Fr("101.4")], "set 1 targets 104.56, 92, 101.4")
check(Fr("5.76") + Fr("5.52") + Fr("93.28") == Fr("104.56"), "104.56 by hand: 6(0.96) + 6(0.92) + 106(0.88)")
b, p, tg = parse(T[2])
check([price_fr(x, D2) for x in b] == [Fr(str(v)) for v in p], "set 2 prices from 0.97, 0.93, 0.89")
check([price_fr(x, D2) for x in tg] == [Fr(97), Fr("98.7")], "set 2 targets 97, 98.7")
check(Fr("2.91") + Fr("95.79") == Fr("98.7"), "98.7 by hand: 3(0.97) + 103(0.93)")
# set 3 by peeling (it has one bond per year, so the classic bootstrap is a second exact route)
b, p, tg = parse(T[4])
byT = sorted(zip(b, p), key=lambda z: z[0][1])
d = []
for (c, Tm), pr in byT:
    c, pr = Fr(str(c)), Fr(str(pr))
    d.append((pr - c * sum(d)) / (100 + c))
exp5 = eval(T[4]["expect"])
check(all(abs(float(a) - e) < 1e-14 for a, e in zip(d, exp5)), "set 3 curve by peeling")
check(d[0] == Fr("0.965") and d[1] == Fr(38369, 41400), "d1 = 0.965, d2 = 38369/41400")
exp6 = eval(T[5]["expect"])
check(all(abs(float(price_fr(x, d)) - e) < 1e-12 for x, e in zip(tg, exp6)), "set 3 targets by peeling")
check(round(exp6[0], 3) == 104.807 and round(exp6[1], 3) == 83.165 and exp6[2] == 98.43, "feedback 104.807, 83.165, 98.43")
check(price_fr([2, 1], d) == Fr("98.43"), "98.43 = 102 x 0.965")
b, p, tg = parse(T[6])
check(Fr("99.5") / 103 == Fr(199, 206) and abs(float(Fr(9950, 103)) - eval(T[6]["expect"])[0]) < 1e-13, "99.5/103")

# ---------- refusals ----------
for k in (7, 8, 10):
    b, p, tg = parse(T[k])
    m = max(x[1] for x in b)
    C = rows_sym(b, m)
    rk = C.rank()
    rka = C.row_join(sp.Matrix([Q(v) for v in p])).rank()
    if k in (7, 8):
        check(C.shape == (3, 3) and rk == 2 and rka == 2, f"test {k + 1}: square, rank 2, prices consistent (infinitely many curves)")
    else:
        check(C.shape == (2, 3) and rk == 2, "test 11: two bonds, three years")
# two different curves both fit test 8 and test 9
for k, curves in ((7, ([Fr("0.97"), Fr("0.93"), Fr("0.89")], [Fr("0.97"), Fr("0.995"), Fr("0.8875")])),
                  (8, ([Fr("0.97"), Fr("0.93"), Fr("0.89")], [Fr("0.90"), Fr("1.00"), Fr("0.89")]))):
    b, p, tg = parse(T[k])
    for dd in curves:
        check([price_fr(x, dd) for x in b] == [Fr(str(v)) for v in p], f"test {k + 1}: curve {dd} fits")
# test 9: in floats the determinant is tiny but not 0, so `det == 0` and a bare solve do not refuse
b, p, tg = parse(T[8])
Cf = rows_np(b, 3)
check(np.linalg.det(Cf) != 0 and abs(np.linalg.det(Cf)) < 1e-10 and np.linalg.matrix_rank(Cf) == 2, "test 9 float det tiny, rank 2")
b, p, tg = parse(T[9])
check(max(x[1] for x in tg) == 4 and max(x[1] for x in b) == 3, "test 10 target past the curve")
check(T[11]["call"] == "'inv(' not in __learner_source__" and T[11]["expect"] == "True", "test 12 source check")


# ---------- grading harness ----------
def _tolist(v):
    if hasattr(v, "tolist"):
        return v.tolist()
    if isinstance(v, (tuple, list)):
        return [_tolist(x) for x in v]
    return v


def close(a, e, tol):
    a = _tolist(a)
    if isinstance(e, (list, tuple)):
        return isinstance(a, (list, tuple)) and len(a) == len(e) and all(close(x, y, tol) for x, y in zip(a, e))
    if isinstance(a, (list, tuple, dict)) or a is None or isinstance(a, str):
        return False
    try:
        a = float(a)
    except Exception:
        return False
    if math.isnan(a):
        return False
    return math.isclose(a, float(e), rel_tol=tol.get("rel", 0), abs_tol=tol.get("abs", 0))


PATCH = ("import numpy as _np\n_os, _oi = _np.linalg.solve, _np.linalg.inv\n"
         "def _sq(a):\n    a = _np.asarray(a, float)\n"
         "    if a.ndim != 2 or a.shape[0] != a.shape[1]:\n        raise _np.linalg.LinAlgError('Last 2 dimensions of the array must be square')\n"
         "    return a\n"
         "def _s(a, b):\n    a = _sq(a)\n"
         "    if _np.linalg.matrix_rank(a) < a.shape[0]:\n        return _np.full(_np.shape(b), _np.nan)\n    return _os(a, b)\n"
         "def _i(a):\n    a = _sq(a)\n"
         "    if _np.linalg.matrix_rank(a) < a.shape[0]:\n        return _np.full(a.shape, _np.nan)\n    return _oi(a)\n"
         "_np.linalg.solve, _np.linalg.inv = _s, _i\n")


def grade(src, pyodide=True):
    g = {"__learner_source__": src}
    if pyodide:
        exec(PATCH, g)
    try:
        exec(compile(src, "main.py", "exec"), g)
        res = []
        for c in W["tests"]:
            try:
                if "setup" in c:
                    exec(c["setup"], g)
                if c["compare"] == "raises":
                    try:
                        eval(c["call"], g)
                        res.append(False)
                    except Exception as ex:
                        res.append(isinstance(ex, ValueError) and c["expect"] == "ValueError")
                    continue
                a = eval(c["call"], g)
                e = eval(c["expect"])
                res.append(close(a, e, c.get("tol", {"rel": 1e-9, "abs": 1e-12})) if c["compare"] == "isclose" else _tolist(a) == e)
            except Exception:
                res.append(False)
        return res
    finally:
        if pyodide:
            exec("_np.linalg.solve, _np.linalg.inv = _os, _oi\n", g)


SOL = W["solution"]
for py in (True, False):
    r = grade(SOL, py)
    check(all(r), f"solution passes all ({'pyodide' if py else 'cpython'}): {r}")
r = grade(W["starter"])
check(sum(r[:11]) == 0, f"starter fails tests 1 to 11: {r}")
check(not all(r), "starter fails")
check(W["starter"].count("def ") == 1 and W["starter"].rstrip().endswith("..."), "starter is a stub")

ALT_FRACTIONS = '''
from fractions import Fraction
import numpy as np

def curve_from_bonds(bonds, prices, targets):
    n = max(m for c, m in bonds)
    def row(c, m):
        if m > n:
            raise ValueError("too long")
        r = [Fraction(c)] * m + [Fraction(0)] * (n - m)
        r[m - 1] += 100
        return r
    if len(bonds) != n:
        raise ValueError("count")
    A = [row(c, m) + [Fraction(p)] for (c, m), p in zip(bonds, prices)]
    for j in range(n):
        piv = next((i for i in range(j, n) if A[i][j] != 0), None)
        if piv is None:
            raise ValueError("not fixed")
        A[j], A[piv] = A[piv], A[j]
        for i in range(n):
            if i != j and A[i][j] != 0:
                f = A[i][j] / A[j][j]
                A[i] = [x - f * y for x, y in zip(A[i], A[j])]
    d = [A[i][n] / A[i][i] for i in range(n)]
    vals = [sum(x * y for x, y in zip(row(c, m), d)) for c, m in targets]
    return np.array([float(x) for x in d]), np.array([float(x) for x in vals])
'''
ALT_LSTSQ = '''
import numpy as np

def curve_from_bonds(bonds, prices, targets):
    n = max(m for c, m in bonds)
    def rows(bs):
        R = np.zeros((len(bs), n))
        for i, (c, m) in enumerate(bs):
            if m > n:
                raise ValueError("target too long")
            R[i, :m] += c
            R[i, m - 1] += 100
        return R
    C = rows(bonds)
    d, res, rank, sv = np.linalg.lstsq(C, np.asarray(prices, float), rcond=None)
    if C.shape != (n, n) or rank < n:
        raise ValueError("not fixed")
    return d, rows(targets) @ d
'''
for name, src in (("fractions elimination", ALT_FRACTIONS), ("lstsq with rank", ALT_LSTSQ)):
    for py in (True, False):
        r = grade(src, py)
        check(all(r), f"other correct solution ({name}, {'pyodide' if py else 'cpython'}) passes: {r}")


def sub(old, new, count=1):
    assert SOL.count(old) >= 1, old
    return SOL.replace(old, new, count)


PLANTS = {
    "no principal": sub("        C[i, maturity - 1] += 100\n", ""),
    "no coupon at maturity": sub("        C[i, :maturity] = coupon\n        C[i, maturity - 1] += 100\n",
                                 "        C[i, :maturity - 1] = coupon\n        C[i, maturity - 1] = 100\n"),
    "transposed C": sub("np.linalg.solve(C, ", "np.linalg.solve(C.T, "),
    "no rank check": sub("    if len(bonds) != years or np.linalg.matrix_rank(C) < years:\n", "    if len(bonds) != years:\n"),
    "lstsq, no checks": sub("    if len(bonds) != years or np.linalg.matrix_rank(C) < years:\n        raise ValueError(\"these prices do not fix every discount factor\")\n    d = np.linalg.solve(C, np.array(prices, dtype=float))\n",
                            "    d = np.linalg.lstsq(C, np.array(prices, dtype=float), rcond=None)[0]\n"),
    "det == 0": sub("np.linalg.matrix_rank(C) < years", "np.linalg.det(C) == 0"),
    "inverse with rank check": sub("np.linalg.solve(C, np.array(prices, dtype=float))", "np.linalg.inv(C) @ np.array(prices, dtype=float)"),
    "no target length check": sub("        if maturity > years:\n            raise ValueError(\"a bond matures after the curve ends\")\n", ""),
    "target rows on their own grid": sub("cash_flow_rows(targets, years) @ d", "cash_flow_rows(targets, max(m for c, m in targets)) @ d"),
    "one bond per year required": sub("    if len(bonds) != years or",
                                      "    if sorted(m for c, m in bonds) != list(range(1, years + 1)) or len(bonds) != years or"),
    "outputs swapped": sub("    return d, values\n", "    return values, d\n"),
    "classic bootstrap": '''import numpy as np

def curve_from_bonds(bonds, prices, targets):
    order = sorted(range(len(bonds)), key=lambda i: bonds[i][1])
    d = []
    for i in order:
        c, m = bonds[i]
        if m != len(d) + 1:
            raise ValueError("gap in maturities")
        d.append((prices[i] - c * sum(d)) / (100 + c))
    d = np.array(d)
    out = []
    for c, m in targets:
        if m > len(d):
            raise ValueError("too long")
        out.append(c * d[:m].sum() + 100 * d[m - 1])
    return d, np.array(out)
''',
    "grid of distinct maturities": '''import numpy as np

def curve_from_bonds(bonds, prices, targets):
    dates = sorted({m for c, m in bonds})
    def rows(bs):
        R = np.zeros((len(bs), len(dates)))
        for i, (c, m) in enumerate(bs):
            if m > dates[-1]:
                raise ValueError("too long")
            for j, t in enumerate(dates):
                if t <= m:
                    R[i, j] = c
            R[i, dates.index(m)] += 100
        return R
    C = rows(bonds)
    if C.shape[0] != C.shape[1] or np.linalg.matrix_rank(C) < len(dates):
        raise ValueError("not fixed")
    d = np.linalg.solve(C, np.array(prices, float))
    return d, rows(targets) @ d
''',
    "prices per row ignored order (sorted bonds, unsorted prices)": sub(
        "    C = cash_flow_rows(bonds, years)\n",
        "    C = cash_flow_rows(sorted(bonds, key=lambda b: b[1]), years)\n"),
}
caught = {}
for name, src in PLANTS.items():
    rp = grade(src, True)
    rc = grade(src, False)
    bad = [i + 1 for i, ok in enumerate(rp) if not ok]
    badc = [i + 1 for i, ok in enumerate(rc) if not ok]
    caught[name] = (bad, badc)
    check(bad, f"plant '{name}' passes every test in Pyodide mode")
    print(f"plant {name!r}: fails tests {bad} (Pyodide), {badc} (CPython)")
check(len(PLANTS) == 14, "fourteen plants")
check(caught["det == 0"][1] == [9], "det == 0 caught by test 9 in CPython")
check(9 in caught["no rank check"][0] and 8 in caught["no rank check"][0], "no rank check caught by tests 8 and 9 (Pyodide)")
check(9 in caught["no rank check"][1], "no rank check caught by test 9 in CPython too (tiny det, no raise)")
check(caught["inverse with rank check"][0] == [12], "inverse caught only by test 12")
check(4 in caught["target rows on their own grid"][0], "test 4 catches unpadded target rows")
check(3 in caught["classic bootstrap"][0] and 3 in caught["one bond per year required"][0], "test 3 catches the peel and the one-per-year rule")
check(5 in caught["prices per row ignored order (sorted bonds, unsorted prices)"][0], "test 5 catches a sorted matrix")

# ---------- feedback and explain figures ----------
fb = item["feedback"]["byKey"]
check("0.96, 0.92 and 0.88" in fb["test-1"] and "104.56, 92 and 101.4" in fb["test-2"], "feedback tests 1, 2")
check("97 and 98.7" in fb["test-4"] and "0.97, 0.93 and 0.89" in fb["test-4"], "feedback test 4")
check("104.807, 83.165 and 98.43" in fb["test-6"] and "99.5/103" in fb["test-7"], "feedback tests 6, 7")
check(set(fb) == {"error"} | {f"test-{k}" for k in range(1, 13)}, "byKey covers every test")

# ---------- voice spot checks on the item ----------
text = json.dumps(item, ensure_ascii=False)
check("!" not in text.replace("!=", ""), "no exclamation marks")
check("—" not in text and "–" not in text, "no em or en dashes")

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
