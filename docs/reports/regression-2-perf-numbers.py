"""regression level 2 performance task (h-slope-check): every number, two routes, and the code checks.

Route A: exact sums in Fractions with the closed forms (b = Sxy/Sxx, s^2 = SSE/(n - 2), SE = s/sqrt(Sxx),
         t* from scipy.stats.t.ppf) -- recomputed here, not read from the item.
Route B: statsmodels OLS (params, resid, rsquared, bse, conf_int, t_test) on the same data.
Then the item's own expects are checked against both, and the shipped solution, the starter and
planted wrong solutions are run through a harness that mirrors app/js/engine/widgets/code.js
(__zq_cmp: isclose element by element, dicts by key set, tol rel/abs; raises by exception class).
Run with the venv Python from the repository root (an optional argument names another homework file).
"""
import ast, json, math, pathlib, sys, time, warnings
from fractions import Fraction as F

import numpy as np
import statsmodels.api as sm
from scipy import stats

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[2]
HW = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "app/content/courses/regression/homework-2.json"
item = next(i for i in json.loads(HW.read_text())["items"] if i["id"] == "h-slope-check")
W = item["widget"]

fails = 0
checks = 0


def check(name, ok):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("FAIL", name)


def close(a, b, rel=1e-9, ab=1e-9):
    if isinstance(a, dict) or isinstance(b, dict):
        return isinstance(a, dict) and isinstance(b, dict) and set(a) == set(b) and all(close(a[k], b[k], rel, ab) for k in a)
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(p, q, rel, ab) for p, q in zip(a, b))
    return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)


# ---------- Route A: exact closed form ----------
def route_a(x, y, beta0=0.0, level=0.95):
    xs = [F(str(v)) for v in x]
    ys = [F(str(v)) for v in y]
    n = len(xs)
    xb, yb = sum(xs) / n, sum(ys) / n
    sxx = sum((v - xb) ** 2 for v in xs)
    sxy = sum((u - xb) * (v - yb) for u, v in zip(xs, ys))
    syy = sum((v - yb) ** 2 for v in ys)
    b = sxy / sxx
    a = yb - b * xb
    e = [v - a - b * u for u, v in zip(xs, ys)]
    sse = sum(v * v for v in e)
    assert sum(e) == 0 and sum(u * v for u, v in zip(xs, e)) == 0  # normal equations hold exactly
    assert sse == syy - b * b * sxx  # SST = SSR + SSE, exactly
    se = math.sqrt(sse / (n - 2) / sxx)
    tc = float(stats.t.ppf((1 + level) / 2, n - 2))
    t = (float(b) - beta0) / se
    return {"coef": [float(a), float(b)], "resid": [float(v) for v in e], "r2": float(1 - sse / syy), "se": se,
            "ci": [float(b) - tc * se, float(b) + tc * se], "t": t, "reject": abs(t) > tc}


# ---------- Route B: statsmodels ----------
def route_b(x, y, beta0=0.0, level=0.95):
    X = sm.add_constant(np.asarray(x, dtype=float))
    res = sm.OLS(np.asarray(y, dtype=float), X).fit()
    ci = res.conf_int(alpha=1 - level)[1]
    tt = res.t_test(([0.0, 1.0], beta0))
    t = float(np.squeeze(tt.tvalue))
    p = float(np.squeeze(tt.pvalue))
    return {"coef": res.params.tolist(), "resid": res.resid.tolist(), "r2": float(res.rsquared), "se": float(res.bse[1]),
            "ci": ci.tolist(), "t": t, "reject": p < 1 - level}


D1 = ([-1.2, 0.4, 0.9, -0.3, 1.5, -0.8, 0.2, 1.1], [-2.28, 0.72, 1.68, -0.73, 2.95, -1.46, 0.35, 2.13])
D2 = ([10, 12, 15, 18, 20, 25], [52.1, 55.0, 60.2, 63.9, 68.3, 75.8])
D3 = ([0, 1, 3], [0.5, 1.9, 2.6])
cases = {"D1 b0=2": (D1, 2.0, 0.95), "D1 b0=2 90%": (D1, 2.0, 0.90), "D2": (D2, 0.0, 0.95), "D2 b0=1.5": (D2, 1.5, 0.95), "D3": (D3, 0.0, 0.95)}
A, B = {}, {}
for k, (D, b0, lv) in cases.items():
    A[k], B[k] = route_a(*D, b0, lv), route_b(*D, b0, lv)
    check(f"route A = route B on {k}", close(A[k], B[k], 1e-10, 1e-11) and A[k]["reject"] == B[k]["reject"])

# critical values two ways (scipy quantile, and the quantile found by bisection on the t CDF)
def tq(p, df):
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if stats.t.cdf(mid, df) < p else (lo, mid)
    return lo
for p, df, v in [(0.975, 6, 2.447), (0.95, 6, 1.943), (0.975, 4, 2.776), (0.975, 1, 12.706)]:
    check(f"t*({p}, {df}) = {v}", abs(stats.t.ppf(p, df) - tq(p, df)) < 1e-9 and round(tq(p, df), 3) == v)
# the stated story: |t| = 2.29 between the 90% and 95% critical values with 6 df
t1 = A["D1 b0=2"]["t"]
check("t = -2.29", round(t1, 2) == -2.29 and round(A["D1 b0=2"]["coef"][1], 3) == 1.925 and round(A["D1 b0=2"]["se"], 4) == 0.0326)
check("inside 95%, outside 90%", stats.t.ppf(0.95, 6) < abs(t1) < stats.t.ppf(0.975, 6)
      and A["D1 b0=2"]["ci"][0] < 2 < A["D1 b0=2"]["ci"][1] and A["D1 b0=2 90%"]["ci"][1] < 2)
check("reject flags", A["D1 b0=2"]["reject"] is False and A["D1 b0=2 90%"]["reject"] is True and A["D2"]["reject"] is True
      and A["D2 b0=1.5"]["reject"] is False and A["D3"]["reject"] is False)
check("D3 three points: residuals and t* 12.71", close(A["D3"]["resid"], [-0.3, 0.45, -0.15]) and close(A["D3"]["coef"], [0.8, 0.65]))
txt = json.dumps(item, ensure_ascii=False)
for s in ("1.925", "0.0326", "-2.29", "2.29 standard errors", "12.71", "1.96", "4.30"):
    check("stated: " + s, s in txt)
check("4.30 is the 95% t* with 2 df (n - 1 slip)", round(stats.t.ppf(0.975, 2), 2) == 4.30)

# ---------- the item's expects against both routes ----------
def ev(s):
    return eval(s, {"True": True, "False": False})

tests = W["tests"]
exp_map = {
    0: A["D1 b0=2"],
    1: [A["D1 b0=2 90%"][k] for k in ("ci", "t", "reject")],
    2: A["D2"]["coef"], 3: A["D2"]["r2"], 4: A["D2"]["se"],
    5: [A["D2 b0=1.5"][k] for k in ("t", "reject")],
    6: [A["D2"][k] for k in ("t", "reject")],
    7: A["D3"]["ci"], 8: A["D3"]["resid"], 9: sorted(A["D3"]),
}
for i, want in exp_map.items():
    got = ev(tests[i]["expect"])
    check(f"test {i + 1} expect matches route A", got == want if isinstance(want, list) and want and isinstance(want[0], str) else close(got, want, 1e-9, 1e-9))  # the item's own tests use isclose at rel 1e-9, abs 1e-9; 1e-12 is tighter than the test and fails on Pyodide's SciPy 1.14.1 t quantile (12.706204736432 vs 12.706204736175 in 1.18.1)
check("example is test 1", W["examples"][0] == tests[0])
check("tests > examples, at most 15", len(tests) > len(W["examples"]) and 3 <= len(tests) <= 15)
check("raises cases", [t["compare"] for t in tests[10:]] == ["raises", "raises"] and all(t["expect"] == "ValueError" for t in tests[10:]))
check("how counts tests", f"{len(tests)} hidden tests" in W["how"])
check("seven keys in prose", all(f"`{k}`" in item["prose"] for k in ("coef", "resid", "r2", "se", "ci", "t", "reject")) and "seven keys" in item["prose"])


# ---------- harness mirroring code.js ----------
def _flat(v):
    if hasattr(v, "to_numpy") and getattr(v, "ndim", 0) == 2:
        return v.to_numpy().tolist()
    return v.tolist() if hasattr(v, "tolist") and not isinstance(v, (int, float, complex, str)) else v


def _nan(v):
    try:
        return bool(v != v)
    except Exception:
        return False


def _same(x, y):
    x, y = _flat(x), _flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    if _nan(x) and _nan(y):
        return True
    return bool(x == y)


def _close(x, y, tol):
    x, y = _flat(x), _flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_close(x[k], y[k], tol) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    if _nan(x) and _nan(y):
        return True
    try:
        if tol:
            return math.isclose(float(x), float(y), rel_tol=tol[0], abs_tol=tol[1])
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def _tol(c):
    t = c.get("tol")
    if isinstance(t, dict):
        return [max(0, float(t.get("rel", 0) or 0)), max(0, float(t.get("abs", 0) or 0))]
    return None


PYODIDE_SOLVE = True  # Pyodide's NumPy 2.0.2 returns nan for an exactly singular solve (AUTHORING section 3)


def run(src):
    g = {"__name__": "__main__", "__learner_source__": src}
    if PYODIDE_SOLVE:
        exec("import numpy as _np\n_orig = _np.linalg.solve\n"
             "def _solve(a, b):\n    a = _np.asarray(a, dtype=float)\n"
             "    if _np.linalg.matrix_rank(a) < a.shape[0]:\n        return _np.full(_np.shape(b), _np.nan)\n"
             "    return _orig(a, b)\n_np.linalg.solve = _solve\n", g)
    out = []
    try:
        exec(compile(src, "solution.py", "exec"), g)
    except Exception as e:
        return ["load-error"] * len(tests)
    for c in tests:
        t0 = time.time()
        try:
            if c.get("setup"):
                exec(c["setup"], g)
            if c["compare"] == "raises":
                try:
                    eval(c["call"], g)
                    ok = False
                except Exception as x:
                    ok = c["expect"] in [k.__name__ for k in type(x).__mro__]
            else:
                a = eval(c["call"], g)
                e = eval(c["expect"], g)
                ok = _close(a, e, _tol(c)) if c["compare"] == "isclose" else _same(a, e)
        except Exception:
            ok = False
        out.append(ok)
        check("case under 1 s", time.time() - t0 < 1.0)
    return out


ORIG_SOLVE = np.linalg.solve


def failing(src):
    try:
        r = run(src)
    finally:
        np.linalg.solve = ORIG_SOLVE
    return [i + 1 for i, ok in enumerate(r) if ok is not True]


sol = W["solution"]
check("solution passes every test", failing(sol) == [])
check("starter fails every test", failing(W["starter"]) == list(range(1, len(tests) + 1)))

# an independent pure-Python solution passes too
pure = '''
from statistics import NormalDist
from scipy import stats
def slope_check(x, y, beta0=0.0, level=0.95):
    n = len(x)
    if n < 3 or len(set(x)) == 1:
        raise ValueError("bad input")
    xb, yb = sum(x) / n, sum(y) / n
    sxx = sum((u - xb) ** 2 for u in x)
    sxy = sum((u - xb) * (v - yb) for u, v in zip(x, y))
    b = sxy / sxx
    a = yb - b * xb
    e = [v - a - b * u for u, v in zip(x, y)]
    sse = sum(r * r for r in e)
    sst = sum((v - yb) ** 2 for v in y)
    se = (sse / (n - 2) / sxx) ** 0.5
    q = stats.t.isf((1 - level) / 2, n - 2)
    t = (b - beta0) / se
    return {"coef": [a, b], "resid": e, "r2": 1 - sse / sst, "se": se, "ci": [b - q * se, b + q * se], "t": t, "reject": abs(t) > q}
'''
check("pure-Python route passes", failing(pure) == [])

# planted wrong solutions: each must fail at least one hidden test
def plant(old, new, src=sol):
    assert old in src, old
    return src.replace(old, new)

plants = {
    "no column of ones (through the origin)": plant("X = np.column_stack([np.ones(n), x])\n    coef = np.linalg.solve(X.T @ X, X.T @ y)\n    resid = y - X @ coef",
                                                    "X = x[:, None]\n    c1 = np.linalg.solve(X.T @ X, X.T @ y)\n    coef = np.array([0.0, c1[0]])\n    resid = y - X @ c1"),
    "R^2 against zero, not the mean": plant("np.sum((y - y.mean()) ** 2)", "np.sum(y ** 2)"),
    "s^2 = SSE / n": plant("sse / (n - 2) /", "sse / n /"),
    "s^2 = SSE / (n - 1)": plant("sse / (n - 2) /", "sse / (n - 1) /"),
    "S_xx not centred": plant("np.sum((x - x.mean()) ** 2))", "np.sum(x ** 2))"),
    "normal 1.96 for t*": plant("stats.t.ppf((1 + level) / 2, n - 2)", "1.959963984540054"),
    "normal quantile at level": plant("stats.t.ppf((1 + level) / 2, n - 2)", "stats.norm.ppf((1 + level) / 2)"),
    "t* with n - 1 df": plant("stats.t.ppf((1 + level) / 2, n - 2)", "stats.t.ppf((1 + level) / 2, n - 1)"),
    "t* with n df": plant("stats.t.ppf((1 + level) / 2, n - 2)", "stats.t.ppf((1 + level) / 2, n)"),
    "one-sided t* (ppf(level))": plant("stats.t.ppf((1 + level) / 2, n - 2)", "stats.t.ppf(level, n - 2)"),
    "level read as alpha": plant("stats.t.ppf((1 + level) / 2, n - 2)", "stats.t.ppf(1 - level / 2, n - 2)"),
    "t against 0, ignoring beta0": plant("t = (b - beta0) / se", "t = b / se"),
    "beta0 ignored in reject only": plant("'reject': bool(abs(t) > tcrit)", "'reject': bool(abs(b / se) > tcrit)"),
    "reject from p > alpha (reversed)": plant("'reject': bool(abs(t) > tcrit)", "'reject': bool(abs(t) < tcrit)"),
    "residuals fitted minus observed": plant("resid = y - X @ coef", "resid = X @ coef - y"),
    "no constant-x check": plant("if n < 3 or np.all(x == x[0]):", "if n < 3:"),
    "no n < 3 check": plant("if n < 3 or np.all(x == x[0]):", "if np.all(x == x[0]):"),
    "lstsq, no checks at all": plant("    if n < 3 or np.all(x == x[0]):\n        raise ValueError('need three points and two different x values')\n", ""
                                     ).replace("np.linalg.solve(X.T @ X, X.T @ y)", "np.linalg.lstsq(X, y, rcond=None)[0]"),
    "CI of half width t* s (no sqrt Sxx)": plant("'ci': [float(b - tcrit * se), float(b + tcrit * se)]",
                                                 "'ci': [float(b - tcrit * np.sqrt(sse / (n - 2))), float(b + tcrit * np.sqrt(sse / (n - 2)))]"),
    "CI b +- 2 SE": plant("'ci': [float(b - tcrit * se), float(b + tcrit * se)]", "'ci': [float(b - 2 * se), float(b + 2 * se)]"),
    "coef slope first": plant("'coef': [float(coef[0]), float(b)]", "'coef': [float(b), float(coef[0])]"),
    "extra key": plant("'reject': bool(abs(t) > tcrit)}", "'reject': bool(abs(t) > tcrit), 'n': n}"),
    "key named beta": plant("'coef': [float(coef[0]), float(b)]", "'beta': [float(coef[0]), float(b)]"),
    "R^2 as 1 - SSE/SSR": plant("r2 = 1 - sse / np.sum((y - y.mean()) ** 2)", "r2 = 1 - sse / np.sum((X @ coef - y.mean()) ** 2)"),
}
for name, src in plants.items():
    f = failing(src)
    print(f"  plant {name:<40} fails tests {f}")
    check("plant caught: " + name, len(f) > 0)
# the three slips the brief names are each caught by their own test
check("missing intercept caught by test 3", 3 in failing(plants["no column of ones (through the origin)"]))
check("R^2 against zero caught by test 4", 4 in failing(plants["R^2 against zero, not the mean"]))
check("n for n - 2 caught by test 5", 5 in failing(plants["s^2 = SSE / n"]))
check("t* df caught on three points (test 8)", 8 in failing(plants["t* with n - 1 df"]) and 8 in failing(plants["normal 1.96 for t*"]))
check("beta0 caught by test 6", 6 in failing(plants["t against 0, ignoring beta0"]))

# CPython note: real np.linalg.solve raises LinAlgError (a ValueError) on singular X'X; Pyodide returns nan.
PYODIDE_SOLVE = False
f_cpy = failing(plants["no constant-x check"])
print("  CPython only: 'no constant-x check' fails tests", f_cpy, "(LinAlgError is a ValueError subclass here)")
check("LinAlgError subclasses ValueError in CPython", issubclass(np.linalg.LinAlgError, ValueError))
PYODIDE_SOLVE = True
# pure-Python division slip: ZeroDivisionError is not a ValueError, so it fails test 11 everywhere
zd = pure.replace('if n < 3 or len(set(x)) == 1:\n        raise ValueError("bad input")\n', "")
check("pure route without checks fails 11 and 12", {11, 12} <= set(failing(zd)))

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
