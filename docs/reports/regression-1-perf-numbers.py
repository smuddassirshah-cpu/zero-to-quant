"""regression level 1 performance task (h-derive-normal-eqs): every number, two routes.

Route A: exact Fractions and the closed forms of the model answer.
Route B: statsmodels OLS (and NumPy) on the same data; sympy for the algebraic identities.
Also lists every passing tick set of the rubric and checks none skips a named part.
Run with the venv Python from the repository root: exits 0 when every check holds.
"""
import itertools, json, pathlib, re, sys
from fractions import Fraction as F

import numpy as np
import statsmodels.api as sm
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[2]
HW = ROOT / "app/content/courses/regression/homework-1.json"
item = next(i for i in json.loads(HW.read_text())["items"] if i["id"] == "h-derive-normal-eqs")

fails = 0
checks = 0


def check(name, ok):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("FAIL", name)


x = [F(v) for v in (1, 3, 6, 10, 15)]
y = [F(v) for v in ("1.3", "1.8", "3.8", "5.4", "8.2")]
n = len(x)

# Route A: exact closed form
xbar, ybar = sum(x) / n, sum(y) / n
dx = [v - xbar for v in x]
dy = [v - ybar for v in y]
sxx = sum(d * d for d in dx)
sxy = sum(a * b for a, b in zip(dx, dy))
b_hat = sxy / sxx
a_hat = ybar - b_hat * xbar
fit = [a_hat + b_hat * v for v in x]
e = [yy - ff for yy, ff in zip(y, fit)]
sse = sum(v * v for v in e)
check("xbar 7", xbar == 7 and sum(x) == 35)
check("ybar 4.1", ybar == F("4.1") and sum(y) == F("20.5"))
check("x deviations", dx == [-6, -4, -1, 3, 8])
check("y deviations", dy == [F(s) for s in ("-2.8", "-2.3", "-0.3", "1.3", "4.1")])
check("Sxx 126", sxx == 126 and [d * d for d in dx] == [36, 16, 1, 9, 64])
check("Sxy 63", sxy == 63 and [a * b for a, b in zip(dx, dy)] == [F(s) for s in ("16.8", "9.2", "0.3", "3.9", "32.8")])
check("b 0.5", b_hat == F(1, 2))
check("a 0.6", a_hat == F(3, 5))
check("fitted", fit == [F(s) for s in ("1.1", "2.1", "3.6", "5.6", "8.1")])
check("residuals", e == [F(s) for s in ("0.2", "-0.3", "0.2", "-0.2", "0.1")])
check("sum e 0", sum(e) == 0)
check("sum x e 0", sum(a * b for a, b in zip(x, e)) == 0 and [a * b for a, b in zip(x, e)] == [F(s) for s in ("0.2", "-0.9", "1.2", "-2.0", "1.5")])
check("SSE 0.22", sse == F("0.22") and [v * v for v in e] == [F(s) for s in ("0.04", "0.09", "0.04", "0.04", "0.01")])
# raw-sum forms used in (a)
check("Sxx raw form", sum(v * v for v in x) - n * xbar ** 2 == sxx)
check("Sxy raw form", sum(a * b for a, b in zip(x, y)) - n * xbar * ybar == sxy)

# colleague's line
ac, bc = F(1), F("0.45")
miss = [yy - ac - bc * xx for xx, yy in zip(x, y)]
s_direct = sum(v * v for v in miss)
check("colleague misses", miss == [F(s) for s in ("-0.15", "-0.55", "0.1", "-0.1", "0.45")])
check("colleague squares", [v * v for v in miss] == [F(s) for s in ("0.0225", "0.3025", "0.01", "0.01", "0.2025")])
check("colleague S direct 0.5475", s_direct == F("0.5475"))
c = (a_hat - ac) + (b_hat - bc) * xbar
check("c -0.05", c == F("-0.05") and b_hat - bc == F("0.05"))
s_identity = sse + n * c ** 2 + (b_hat - bc) ** 2 * sxx
check("identity pieces", n * c ** 2 == F("0.0125") and (b_hat - bc) ** 2 * sxx == F("0.315") and (b_hat - bc) ** 2 == F("0.0025"))
check("colleague S identity 0.5475", s_identity == s_direct)
check("extra 0.3275", s_direct - sse == F("0.3275"))

# Route B: statsmodels and NumPy
xf = np.array([float(v) for v in x])
yf = np.array([float(v) for v in y])
res = sm.OLS(yf, sm.add_constant(xf)).fit()
check("sm intercept", abs(res.params[0] - 0.6) < 1e-12)
check("sm slope", abs(res.params[1] - 0.5) < 1e-12)
check("sm SSE", abs(res.ssr - 0.22) < 1e-12)
check("sm residuals", np.allclose(res.resid, [0.2, -0.3, 0.2, -0.2, 0.1], atol=1e-12))
check("sm centred TSS", abs(res.centered_tss - float(sum(d * d for d in dy))) < 1e-12)
X = np.column_stack([np.ones(n), xf])
check("normal equations solve", np.allclose(np.linalg.solve(X.T @ X, X.T @ yf), [0.6, 0.5], atol=1e-12))
check("numpy polyfit", np.allclose(np.polyfit(xf, yf, 1), [0.5, 0.6], atol=1e-12))
s_np = float(np.sum((yf - 1 - 0.45 * xf) ** 2))
check("colleague S numpy", abs(s_np - 0.5475) < 1e-12)
# brute force: no grid line beats the fit, and the fit beats every nearby line
grid = [(a, b) for a in np.linspace(0, 1.2, 121) for b in np.linspace(0.4, 0.6, 81)]
smin = min(float(np.sum((yf - a - b * xf) ** 2)) for a, b in grid)
check("grid minimum at fit", abs(smin - 0.22) < 1e-9)

# sympy: the identities of (a), (b), (c) for general n = 5 symbols
xs = sp.symbols("x1:6")
ys = sp.symbols("y1:6")
a, b = sp.symbols("a b")
N = 5
S = sum((yy - a - b * xx) ** 2 for xx, yy in zip(xs, ys))
dSa, dSb = sp.diff(S, a), sp.diff(S, b)
check("dS/da", sp.expand(dSa - (-2 * sum(yy - a - b * xx for xx, yy in zip(xs, ys)))) == 0)
check("dS/db", sp.expand(dSb - (-2 * sum(xx * (yy - a - b * xx) for xx, yy in zip(xs, ys)))) == 0)
sol = sp.solve([dSa, dSb], [a, b], dict=True)[0]
mx, my = sum(xs) / N, sum(ys) / N
Sxx = sum((xx - mx) ** 2 for xx in xs)
Sxy = sum((xx - mx) * (yy - my) for xx, yy in zip(xs, ys))
check("b = Sxy/Sxx", sp.simplify(sol[b] - Sxy / Sxx) == 0)
check("a = ybar - b xbar", sp.simplify(sol[a] - (my - Sxy / Sxx * mx)) == 0)
check("Sxx raw (sympy)", sp.expand(Sxx - (sum(xx ** 2 for xx in xs) - N * mx ** 2)) == 0)
check("Sxy raw (sympy)", sp.expand(Sxy - (sum(xx * yy for xx, yy in zip(xs, ys)) - N * mx * my)) == 0)
check("determinant n Sxx", sp.expand(sp.Matrix([[N, sum(xs)], [sum(xs), sum(v ** 2 for v in xs)]]).det() - N * Sxx) == 0)
ah, bh = sol[a], sol[b]
Smin = S.subs({a: ah, b: bh})
cc = (ah - a) + (bh - b) * mx
ident = sp.simplify(S - (Smin + N * cc ** 2 + (bh - b) ** 2 * Sxx))
check("(b) identity S = Smin + n c^2 + (bh - b)^2 Sxx", ident == 0)
k = sp.symbols("k")
Sk = S.subs({xx: k for xx in xs})
check("(c) identity for constant x", sp.expand(Sk - (sum((yy - my) ** 2 for yy in ys) + N * (my - a - b * k) ** 2)) == 0)
eqs_k = [sp.expand(dSa.subs({xx: k for xx in xs})), sp.expand(dSb.subs({xx: k for xx in xs}))]
check("(c) second equation is k times the first", sp.expand(eqs_k[1] - k * eqs_k[0]) == 0)
# constant x numerically: many lines tie
yk = yf
for slope in (-3.0, 0.0, 0.5, 7.0):
    aa = yk.mean() - slope * 5
    check(f"constant x ties at slope {slope}", abs(np.sum((yk - aa - slope * 5) ** 2) - np.sum((yk - yk.mean()) ** 2)) < 1e-9)

# the numbers stated in the model and rubric appear there
txt = item["model"] + " ".join(r["text"] for r in item["rubric"])
for s in ("35/5 = 7", "20.5/5 = 4.1", "-6, -4, -1, 3, 8", "36 + 16 + 1 + 9 + 64 = 126", "-2.8, -2.3, -0.3, 1.3, 4.1",
          "16.8 + 9.2 + 0.3 + 3.9 + 32.8 = 63", "63/126 = 0.5", "4.1 - 0.5 \\times 7 = 0.6", "1.1, 2.1, 3.6, 5.6, 8.1",
          "0.2, -0.3, 0.2, -0.2, 0.1", "0.2 - 0.9 + 1.2 - 2.0 + 1.5 = 0", "0.04 + 0.09 + 0.04 \\\\ &\\quad + 0.04 + 0.01 = 0.22",
          "-0.15, -0.55, 0.1, -0.1, 0.45", "0.0225 + 0.3025 + 0.01 \\\\ &\\quad + 0.01 + 0.2025 = 0.5475", "(0.6 - 1) + 0.05 \\times 7 = -0.05",
          "0.22 + 5 \\times 0.0025 \\\\ &\\quad + 0.0025 \\times 126", "0.22 + 0.0125 + 0.315 \\\\ &= 0.5475", "0.3275", "0.315",
          "\\textstyle\\sum x_i^2 - 2\\bar x \\cdot n\\bar x + n\\bar x^2"):
    check("stated: " + s, s in txt)
check("prompt data", "$x = 1, 3, 6, 10, 15$" in item["prompt"] and "$y = 1.3, 1.8, 3.8, 5.4, 8.2$" in item["prompt"] and "1 + 0.45x" in item["prompt"])

# rubric: shape and every passing tick set
rub = item["rubric"]
pts = [r["points"] for r in rub]
req = [bool(r.get("required")) for r in rub]
check("rubric sums to 10", sum(pts) == 10 and 3 <= len(rub) <= 5)
check("not every row required", not all(req))
passes = [s for m in range(len(rub) + 1) for s in itertools.combinations(range(len(rub)), m)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows 1-based):", [[i + 1 for i in s] for s in passes])
named = {"(a) normal equations and solution": 0, "(b) minimum and uniqueness": 1, "(a) assumption and (c) constant x": 2, "(d) numbers": 3}
for part, row in named.items():
    check("no pass skips " + part, all(row in s for s in passes))
check("only the optional row can be left out", [i for i in range(len(rub)) if any(i not in s for s in passes)] == [4])
check("optional part marked in prompt", "Optional, one more point" in item["prompt"])
check("kind and shape", item["performance"] == "derivation" and item["kind"] == "longform"
      and not any(k in item for k in ("starter", "steps", "order", "derive", "hints", "parts")))

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
