"""regression L1 h-derive-normal-eqs (numbers, two routes) and L2 h-slope-check (code: shipped, starter, reader
solution, statsmodels route, planted slips). Run with the venv Python: python -I reg_two.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fractions import Fraction as F
import numpy as np
from harness11 import item, summary, patched

bad = 0
def check(name, ok):
    global bad
    print(("ok   " if ok else "FAIL ") + name)
    bad += 0 if ok else 1

# ---------- L1: route 1 exact Fractions from raw sums, route 2 numpy lstsq and a brute grid near the optimum
x = [F(v) for v in (1, 3, 6, 10, 15)]
y = [F(v) for v in ("1.3", "1.8", "3.8", "5.4", "8.2")]
n = 5
Sx, Sy, Sxx_raw, Sxy_raw = sum(x), sum(y), sum(v * v for v in x), sum(a * b for a, b in zip(x, y))
b1 = (n * Sxy_raw - Sx * Sy) / (n * Sxx_raw - Sx ** 2)
a1 = (Sy - b1 * Sx) / n
xb, yb = Sx / n, Sy / n
Sxx = sum((v - xb) ** 2 for v in x); Sxy = sum((u - xb) * (w - yb) for u, w in zip(x, y))
check("x bar 7, y bar 4.1", xb == 7 and yb == F("4.1"))
check("Sxx 126 = raw sum - n xbar^2", Sxx == 126 and Sxx_raw - n * xb ** 2 == 126)
check("Sxy 63 = raw - n xbar ybar", Sxy == 63 and Sxy_raw - n * xb * yb == 63)
check("b 0.5 a 0.6 (two formulas)", b1 == F(1, 2) == Sxy / Sxx and a1 == F(3, 5) == yb - b1 * xb)
coef = np.linalg.lstsq(np.column_stack([np.ones(5), [float(v) for v in x]]), [float(v) for v in y], rcond=None)[0]
check("lstsq agrees", abs(coef[0] - 0.6) < 1e-12 and abs(coef[1] - 0.5) < 1e-12)
e = [w - a1 - b1 * u for u, w in zip(x, y)]
check("residuals 0.2 -0.3 0.2 -0.2 0.1", e == [F(s) for s in ("0.2", "-0.3", "0.2", "-0.2", "0.1")])
check("sum e = sum x e = 0", sum(e) == 0 and sum(u * v for u, v in zip(x, e)) == 0)
check("x e terms 0.2 -0.9 1.2 -2.0 1.5", [u * v for u, v in zip(x, e)] == [F(s) for s in ("0.2", "-0.9", "1.2", "-2.0", "1.5")])
S = lambda a, b: sum((w - a - b * u) ** 2 for u, w in zip(x, y))
check("S(0.6, 0.5) = 0.22", S(a1, b1) == F("0.22"))
check("colleague misses", [w - 1 - F("0.45") * u for u, w in zip(x, y)] == [F(s) for s in ("-0.15", "-0.55", "0.1", "-0.1", "0.45")])
check("S(1, 0.45) = 0.5475 directly", S(1, F("0.45")) == F("0.5475"))
c = (a1 - 1) + (b1 - F("0.45")) * xb
check("c = -0.05, identity 0.22 + 0.0125 + 0.315", c == F("-0.05") and S(a1, b1) + n * c ** 2 + (b1 - F("0.45")) ** 2 * Sxx == F("0.5475")
      and n * c ** 2 == F("0.0125") and (b1 - F("0.45")) ** 2 * Sxx == F("0.315"))
check("extra 0.3275", S(1, F("0.45")) - S(a1, b1) == F("0.3275"))
# identity on random lines and a grid (route 2 for uniqueness)
rng = np.random.default_rng(1)
ok = True
for _ in range(200):
    a, b = F(int(rng.integers(-300, 300)), 100), F(int(rng.integers(-300, 300)), 100)
    cc = (a1 - a) + (b1 - b) * xb
    ok &= S(a, b) == S(a1, b1) + n * cc ** 2 + (b1 - b) ** 2 * Sxx
    ok &= (S(a, b) > S(a1, b1)) or (a, b) == (a1, b1)
check("S(a,b) = S_min + n c^2 + (b^-b)^2 Sxx on 200 random lines, strict above", ok)
# (c) constant x: S = sum (y - ybar)^2 + n (ybar - a - b k)^2 for every line, ties through (k, ybar)
k = F(4); yy = y
Sk = lambda a, b: sum((w - a - b * k) ** 2 for w in yy)
ok = all(Sk(yb - bb * k, bb) == sum((w - yb) ** 2 for w in yy) for bb in (F(-3), F(0), F(7, 2)))
ok &= all(Sk(a, b) == sum((w - yb) ** 2 for w in yy) + n * (yb - a - b * k) ** 2 for a, b in ((F(1), F(2)), (F(-1), F(1, 3))))
check("constant x: every line through (k, ybar) ties, identity holds", ok)

# ---------- L2 code
it = item("regression", "homework-2.json", "h-slope-check")
w = it["widget"]
sol = w["solution"]
print("L2 h-slope-check")
f, _ = summary(w, sol, "shipped solution", "all"); check("shipped passes all", f == [])
f, _ = summary(w, w["starter"], "starter"); check("starter fails", len(f) > 0)
mine = r'''
import math
from scipy.stats import t as _t
def slope_check(x, y, beta0=0.0, level=0.95):
    x = [float(v) for v in x]; y = [float(v) for v in y]
    n = len(x)
    if n < 3:
        raise ValueError("fewer than three points")
    mx = sum(x) / n; my = sum(y) / n
    sxx = sum((v - mx) ** 2 for v in x)
    if sxx == 0:
        raise ValueError("every x the same")
    sxy = sum((u - mx) * (v - my) for u, v in zip(x, y))
    b = sxy / sxx; a = my - b * mx
    resid = [v - a - b * u for u, v in zip(x, y)]
    sse = sum(r * r for r in resid); sst = sum((v - my) ** 2 for v in y)
    se = math.sqrt(sse / (n - 2) / sxx)
    q = _t.ppf(0.5 + level / 2, n - 2)
    t = (b - beta0) / se
    return {"coef": [a, b], "resid": resid, "r2": 1 - sse / sst, "se": se, "ci": [b - q * se, b + q * se], "t": t, "reject": abs(t) > q}
'''
f, _ = summary(w, mine, "reader solution (centred sums, pure Python + scipy t)", "all"); check("reader solution passes", f == [])
sm = r'''
import numpy as np
import statsmodels.api as sm
def slope_check(x, y, beta0=0.0, level=0.95):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3 or np.ptp(x) == 0:
        raise ValueError("bad input")
    r = sm.OLS(y, sm.add_constant(x)).fit()
    lo, hi = r.conf_int(alpha=1 - level)[1]
    tt = r.t_test(np.array([[0.0, 1.0]]), use_t=True)
    tv = float((r.params[1] - beta0) / r.bse[1])
    p = float(r.t_test((np.array([[0.0, 1.0]]), np.array([beta0]))).pvalue)
    return {"coef": list(r.params), "resid": list(r.resid), "r2": r.rsquared, "se": r.bse[1], "ci": [lo, hi], "t": tv, "reject": p < 1 - level}
'''
f, _ = summary(w, sm, "statsmodels route (OLS, conf_int, t_test p-value)", "all"); check("statsmodels route passes", f == [])
poly = r'''
import numpy as np
from scipy import stats
def slope_check(x, y, beta0=0.0, level=0.95):
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    if n < 3 or len(set(x.tolist())) == 1:
        raise ValueError("bad")
    b, a = np.polyfit(x, y, 1)
    res = y - (a + b * x)
    s2 = res @ res / (n - 2)
    se = np.sqrt(s2 / ((x - x.mean()) ** 2).sum())
    q = stats.t.isf((1 - level) / 2, n - 2)
    t = (b - beta0) / se
    return dict(coef=[a, b], resid=res, r2=np.corrcoef(x, y)[0, 1] ** 2, se=se, ci=[b - q * se, b + q * se], t=t, reject=bool(abs(t) > q))
'''
f, _ = summary(w, poly, "polyfit route (R^2 as squared correlation)", "all"); check("polyfit route passes", f == [])

plants = [
    ("SSE over n, not n - 2", [("sse / (n - 2)", "sse / n")]),
    ("SSE over n - 1", [("sse / (n - 2)", "sse / (n - 1)")]),
    ("t critical with n - 1 df", [("(1 + level) / 2, n - 2)", "(1 + level) / 2, n - 1)")]),
    ("normal critical value", [("stats.t.ppf((1 + level) / 2, n - 2)", "stats.norm.ppf((1 + level) / 2)")]),
    ("one-sided quantile ppf(level)", [("stats.t.ppf((1 + level) / 2, n - 2)", "stats.t.ppf(level, n - 2)")]),
    ("R^2 about 0 (uncentred)", [("np.sum((y - y.mean()) ** 2)", "np.sum(y ** 2)")]),
    ("t against 0, beta0 ignored", [("t = (b - beta0) / se", "t = b / se")]),
    ("residuals fitted minus observed", [("resid = y - X @ coef", "resid = X @ coef - y")]),
    ("no column of ones", [("X = np.column_stack([np.ones(n), x])", "X = np.column_stack([np.zeros(n), x]) + np.column_stack([np.ones(n), np.zeros(n)]) * 0"),
                            ("coef = np.linalg.solve(X.T @ X, X.T @ y)", "coef = np.array([0.0, (x @ y) / (x @ x)])")]),
    ("Sxx uncentred", [("np.sum((x - x.mean()) ** 2)", "np.sum(x ** 2)")]),
    ("no n < 3 check", [("n < 3 or np.all(x == x[0])", "np.all(x == x[0])")]),
]
for name, pairs in plants:
    f, _ = summary(w, patched(sol, *pairs), "plant: " + name)
    check("plant caught: " + name, len(f) > 0)
# With every check removed, or only the constant-x check removed, np.linalg.solve meets the singular X'X of test 11.
# CPython NumPy raises LinAlgError (a ValueError subclass), so test 11 passes by accident there; Pyodide's NumPy 2.0.2
# returns NaN with no error, so test 11 fails in the engine. Test 12 (two points) fails either way.
emsc = sys.platform == "emscripten"
f, _ = summary(w, patched(sol, ("if n < 3 or np.all(x == x[0]):\n        raise ValueError('need three points and two different x values')", "pass")), "plant: no checks at all")
check("no checks at all: caught (test 12, and test 11 in Pyodide)", f == ([11, 12] if emsc else [12]))
f, _ = summary(w, patched(sol, ("n < 3 or np.all(x == x[0])", "n < 3")), "plant: no constant-x check")
check("no constant-x check: caught by test 11 in Pyodide (passes in CPython only)", f == ([11] if emsc else []))
for k in (2.0, 0.3):
    X = np.column_stack([np.ones(4), np.full(4, k)])
    try:
        print(f"  solve on constant x = {k}: {np.linalg.solve(X.T @ X, X.T @ np.array([1.0, 1.5, 0.5, 2.0]))} (no error)")
    except Exception as ex:
        print(f"  solve on constant x = {k}: {type(ex).__name__}")

# margins: |t| against t* at every test (a learner's rounding never flips reject)
from scipy import stats
for xs, ys, b0, lv in [([-1.2, 0.4, 0.9, -0.3, 1.5, -0.8, 0.2, 1.1], [-2.28, 0.72, 1.68, -0.73, 2.95, -1.46, 0.35, 2.13], 2.0, 0.95),
                       ([-1.2, 0.4, 0.9, -0.3, 1.5, -0.8, 0.2, 1.1], [-2.28, 0.72, 1.68, -0.73, 2.95, -1.46, 0.35, 2.13], 2.0, 0.90),
                       ([10, 12, 15, 18, 20, 25], [52.1, 55.0, 60.2, 63.9, 68.3, 75.8], 1.5, 0.95),
                       ([10, 12, 15, 18, 20, 25], [52.1, 55.0, 60.2, 63.9, 68.3, 75.8], 0.0, 0.95)]:
    X = [F(str(v)) for v in xs]; Y = [F(str(v)) for v in ys]; m = len(X)
    mx, my = sum(X) / m, sum(Y) / m
    sxx = sum((v - mx) ** 2 for v in X); bb = sum((u - mx) * (v - my) for u, v in zip(X, Y)) / sxx; aa = my - bb * mx
    sse = sum((v - aa - bb * u) ** 2 for u, v in zip(X, Y))
    tt = (float(bb) - b0) / (float(sse / (m - 2) / sxx) ** 0.5)
    q = stats.t.ppf((1 + lv) / 2, m - 2)
    print(f"  n={m} beta0={b0} level={lv}: t={tt:.6f} t*={q:.6f} margin {abs(abs(tt) - q):.4f}")
    check("reject margin over 0.1", abs(abs(tt) - q) > 0.1)
check("t* at n = 3 is 12.71 (byKey test-8)", round(stats.t.ppf(0.975, 1), 2) == 12.71 and round(stats.t.ppf(0.975, 4), 2) == 2.78)
print("failures:", bad)
sys.exit(1 if bad else 0)
