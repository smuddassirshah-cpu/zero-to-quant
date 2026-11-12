"""Delta read AC-1: recompute every changed key, wrong value and printed number by two routes.

Route 1 is exact (sympy, fractions); route 2 is NumPy (solve, lstsq, polyfit, eigh, svd, a regression on simulated
data, enumeration, bisection). Each stored key and each wrong[] value is then read from the content and compared, and
each numeric band is checked: it takes the key, refuses every wrong value, and no two bands of a part meet.

Run from the repo root with the scratchpad venv:
    <venv>/bin/python docs/reviews/review-delta-problems-ac-1-scripts/recompute.py
Exit 0 when every check passes."""
import itertools
import math
import os
import re
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(__file__))
from dump import item  # noqa: E402

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", msg)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def vec(tex):
    """'(15, 18, 9)' or '(-1, -5/6)' -> tuple of Fractions."""
    body = tex.strip().strip("()[]")
    return tuple(F(x.strip()) for x in body.split(","))


def part(it, n):
    return it["parts"][n - 1]


def key_num(it, n, want, name="key"):
    w = part(it, n)["widget"]
    ok(close(w["answer"], want, w["tol"]["abs"] + 1e-12), f"{it['id']} {n} {name}: stored {w['answer']} against {float(want)}")


def key_vec(it, n, want):
    w = part(it, n)["widget"]
    ok(vec(w["answer"]) == tuple(F(x) for x in want), f"{it['id']} {n} key {w['answer']} against {want}")


def wrong(it, n, wid, want):
    w = part(it, n)["widget"]
    hit = [x for x in w.get("wrong", []) if x["id"] == wid]
    ok(len(hit) == 1, f"{it['id']} {n} wrong {wid} exists")
    if not hit:
        return
    x = hit[0]
    if "value" in x:
        ok(close(x["value"], want, x["tol"]["abs"] + 1e-12), f"{it['id']} {n} wrong {wid}: stored {x['value']} against {float(want)}")
    else:
        ok(vec(x["tex"]) == tuple(F(v) for v in want), f"{it['id']} {n} wrong {wid}: stored {x['tex']} against {want}")
    ok(wid in part(it, n)["feedback"]["byKey"], f"{it['id']} {n} wrong {wid} has a line")


def bands(it, n, extra_ok=(), extra_no=()):
    """The key band takes the key and extra_ok, refuses wrong values and extra_no; no two bands meet."""
    w = part(it, n)["widget"]
    if w["kind"] != "numeric":
        return
    lo, hi = w["answer"] - w["tol"]["abs"], w["answer"] + w["tol"]["abs"]
    spans = [("key", lo, hi)]
    for x in w.get("wrong", []):
        ok(not (lo - 1e-12 <= x["value"] <= hi + 1e-12), f"{it['id']} {n}: key band refuses wrong {x['id']}")
        spans.append((x["id"], x["value"] - x["tol"]["abs"], x["value"] + x["tol"]["abs"]))
    for (a, al, ah), (b, bl, bh) in itertools.combinations(spans, 2):
        ok(ah < bl or bh < al, f"{it['id']} {n}: bands {a} and {b} do not meet")
    for v in extra_ok:
        ok(lo - 1e-12 <= v <= hi + 1e-12, f"{it['id']} {n}: key band takes {v}")
    for v in extra_no:
        ok(not (lo - 1e-12 <= v <= hi + 1e-12), f"{it['id']} {n}: key band refuses {v}")


def says(it, n, field, *needles):
    p = part(it, n)
    text = {"question": p["question"], "correct": p["feedback"]["correct"], "explain": p["explain"]["text"]}.get(field)
    if text is None:
        text = p["feedback"]["byKey"][field]
    for s in needles:
        ok(s in text, f"{it['id']} {n} {field} prints {s!r}")


def all_text(it):
    out = [it["prose"]]
    for p in it["parts"]:
        out += [p["question"], p["feedback"]["correct"], p["feedback"]["generic"], p["explain"]["text"]]
        out += list(p["feedback"].get("byKey", {}).values())
        for o in p["widget"].get("options", []):
            out += [o.get("text", ""), o.get("why", "")]
    return out


def stale(it, patterns):
    text = " ".join(all_text(it))
    for pat in patterns:
        ok(not re.search(pat, text), f"{it['id']}: no stale {pat!r} left")


# ------------------------------------------------------------------ courier (elimination/problems-1)
it = item("p-courier-rounds")
A = sp.Matrix([[0, 3, 2], [4, 1, 1], [0, 6, 7]])
b = sp.Matrix([18, 15, 45])
ok("3 large and 2 signed-for" in it["prose"] and "4 small, 1 large and 1 signed-for" in it["prose"] and "6 large and 7 signed-for" in it["prose"], "courier prose rows match A")
ok(r"0&3&2\\4&1&1\\0&6&7" in it["prose"] and "(18, 15, 45)" in it["prose"], "courier prose prints A and b")
x_exact = A.LUsolve(b)
x_np = np.linalg.solve(np.array(A, float), np.array(b, float).ravel())
ok(list(x_exact) == [2, 4, 3] and np.allclose(x_np, [2, 4, 3]), "courier x = (2, 4, 3) both ways")
P = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
PA = P * A
ok(PA.tolist() == [[4, 1, 1], [0, 3, 2], [0, 6, 7]], "PA rows")
L = sp.Matrix([[1, 0, 0], [0, 1, 0], [0, 2, 1]])
U = sp.Matrix([[4, 1, 1], [0, 3, 2], [0, 0, 3]])
ok(L * U == PA, "PA = LU")
import scipy.linalg as sla  # noqa: E402

p_, l_, u_ = sla.lu(np.array(PA, float))  # second route: partial pivoting on PA picks no further swap? check product only
ok(np.allclose(p_ @ l_ @ u_, np.array(PA, float)), "scipy LU reproduces PA")
ok(r"4&1&1\\0&3&2\\0&0&3" in part(it, 4)["question"], "courier part 4 prints U")
Pb = P * b
c = L.LUsolve(Pb)
key_vec(it, 3, (15, 18, 9))
ok(list(c) == [15, 18, 9] and list(Pb) == [15, 18, 45], "c and Pb")
ok(np.allclose(np.linalg.solve(np.array(L, float), np.array(Pb, float).ravel()), [15, 18, 9]), "c by NumPy")
wrong(it, 3, "unswapped", tuple(L.LUsolve(b)))           # b unswapped
wrong(it, 3, "signs", (15, 18, 45 + 2 * 18))             # added 2 x 18
ok(tuple(L.LUsolve(b)) == (18, 15, 15), "unswapped is (18, 15, 15)")
key_vec(it, 4, (2, 4, 3))
ok(list(U.LUsolve(c)) == [2, 4, 3], "Ux = c")
z = 9; y = 18 - 2 * z; x = 15 - y - z                     # no division by any pivot
wrong(it, 4, "no-divide", (x, y, z))
wrong(it, 4, "reversed", (3, 4, 2))
key_num(it, 5, 5 * 2 + 2 * 4 + 4 * 3)
ok(np.dot([5, 2, 4], x_np).round(9) == 30, "new round by NumPy")
wrong(it, 5, "reversed", 5 * 3 + 2 * 4 + 4 * 2)
bands(it, 5)
says(it, 3, "correct", "(15, 18, 45)", "45 - 2 \\times 18 = 9")
says(it, 4, "correct", "(18 - 6)/3 = 4", "(15 - 4 - 3)/4 = 2")
stale(it, [r"\(14, 15", r"-10, 6, 9", r"15, 14, 11", r"14, 15, 69"])

# ------------------------------------------------------------------ gantry (elimination/problems-2)
it = item("p-tilted-gantry")
k, cc = sp.symbols("k c")
M = sp.Matrix([[1, 1, 0], [0, 1, 2], [2, 0, k]])            # columns m1, m2, m3
ok(sp.solve(M.det(), k) == [-4], "gantry dependent at k = -4 (det)")
ok(abs(np.linalg.det(np.array(M.subs(k, -4), float))) < 1e-12 and np.linalg.matrix_rank(np.array(M.subs(k, -4), float)) == 2, "gantry rank 2 at k = -4 (NumPy)")
key_num(it, 1, -4)
M4 = M.subs(k, -4)
aug = M4.row_join(sp.Matrix([6, 2, cc]))
aug[2, :] = aug[2, :] - 2 * aug[0, :]
half = sp.solve(aug[2, 3], cc)[0]                          # stops after column 1: c - 12 = 0
aug[2, :] = aug[2, :] + 2 * aug[1, :]
full = sp.solve(aug[2, 3], cc)[0]
ok(aug[2, :3] == sp.Matrix([[0, 0, 0]]), "gantry row 3 clears")
key_num(it, 3, full)
ok(full == 8 and half == 12, "gantry c = 8, half-step 12")
wrong(it, 3, "half-step", half)
wrong(it, 3, "sign", -4)
# second route: (6, 2, c) = x1 m1 + x2 m2
x2 = 2; x1 = 6 - x2
ok(2 * x1 == 8, "gantry c by combination")
# least squares residual is 0 only at c = 8
for cv in (4, 8, 12):
    r = np.linalg.lstsq(np.array(M4, float), np.array([6, 2, cv], float), rcond=None)
    res = np.array(M4, float) @ r[0] - np.array([6, 2, cv], float)
    ok((np.abs(res).max() < 1e-9) == (cv == 8), f"gantry (6, 2, {cv}) reachable only at 8")
key_vec(it, 4, (6, 0, 1))
ok(list(M4 * sp.Matrix([6, 0, 1])) == [6, 2, 8] and list(M4 * sp.Matrix([4, 2, 0])) == [6, 2, 8], "gantry turns reach the point")
ok(list(M4 * sp.Matrix([2, -2, 1])) == [0, 0, 0], "gantry nullspace (2, -2, 1)")
ns = M4.nullspace()[0]
ok(list(ns / ns[2]) == [2, -2, 1], "gantry nullspace by sympy")
wrong(it, 4, "no-motor-3", (4, 2, 0))
wrong(it, 4, "sign", (4 - 2, 2 + 2, 1))
ok(list(M4 * sp.Matrix([2, 4, 1])) != [6, 2, 8], "gantry sign slip misses the point")
ok(list(2 * sp.Matrix([1, 0, 2]) - 2 * sp.Matrix([1, 1, 0])) == [0, -2, 4], "gantry part 2 sign line")
bands(it, 1); bands(it, 3)
says(it, 3, "half-step", "c - 12 = 0", "c - 8 = 0")
stale(it, [r"\(4, 2, c\)", r"\(4, -1, 1\)", r"\(0, 3, 1\)", r"\(2, 1, 0\)"])

# ------------------------------------------------------------------ futures (elimination/problems-2)
it = item("p-futures-packages")
S = sp.Matrix([[1, 0, 1], [-1, 1, -2], [0, -1, 1]])
ok(S.rank() == 2 and np.linalg.matrix_rank(np.array(S, float)) == 2, "futures rank 2")
ns = S.nullspace()[0]
ok(list(ns / ns[2]) == [-1, 1, 1], "futures special solution")
aug = S.row_join(sp.Matrix([5, -2, cc]))
aug[1, :] = aug[1, :] + aug[0, :]
stale_rhs = sp.solve(cc + (-2), cc)[0]                     # adds the old -2 to row 3
aug[2, :] = aug[2, :] + aug[1, :]
ok(list(aug[:, 3]) == [5, 3, cc + 3], "futures target after the row steps")
key_num(it, 3, sp.solve(aug[2, 3], cc)[0])
ok(sp.solve(5 - 2 + cc, cc) == [-3], "futures c by the zero-sum route")
wrong(it, 3, "sign", 3)
wrong(it, 3, "stale-rhs", stale_rhs)
ok(stale_rhs == 2, "futures stale-rhs is 2")
key_vec(it, 4, (5, 3, 0))
ok(list(S * sp.Matrix([5, 3, 0])) == [5, -2, -3], "futures (5, 3, 0) builds the position")
ok(np.allclose(np.linalg.lstsq(np.array(S[:, :2], float), np.array([5, -2, -3], float), rcond=None)[0], [5, 3]), "futures (5, 3) by lstsq")
wrong(it, 4, "sign", (5, -3, 0))
ok((S * sp.Matrix([5, -3, 0]))[1] == -8, "futures sign slip: June -8")
key_vec(it, 5, (3, 5, 2))
ok(list(S * sp.Matrix([3, 5, 2])) == [5, -2, -3], "futures (3, 5, 2) builds the position")
wrong(it, 5, "sign", (5 + 2, 3 - 2, 2))
ok(list(S * sp.Matrix([7, 1, 2])) == [9, -10, 1], "futures sign slip gives (9, -10, 1)")
wrong(it, 5, "nullspace-only", (-2, 2, 2))
ok(list(sp.Matrix([1, -1, 0]) - sp.Matrix([0, 1, -1]) + sp.Matrix([1, -2, 1])) == [2, -4, 2], "futures part 2 sign line")
bands(it, 3)
stale(it, [r"\(4, 3, 0\)", r"\(2, 5, 2\)", r"\(6, 1, 2\)", r"\(4, -2"])

# ------------------------------------------------------------------ vinyl cutter (elimination/problems-3)
it = item("p-vinyl-cutter")
T = sp.Matrix([[3, k], [2, 4]])
ok(T.det() == 12 - 2 * k, "vinyl det 12 - 2k")
d2 = T.subs(k, 2).det()
key_num(it, 1, 5 * d2)
ok(close(5 * abs(np.linalg.det(np.array(T.subs(k, 2), float))), 40), "vinyl area by NumPy")
# third route: the unit square's image, by the shoelace formula
u, v = (3, 2), (2, 4)
ok(abs(u[0] * v[1] - u[1] * v[0]) * 5 == 40, "vinyl area by the parallelogram")
wrong(it, 1, "plus", 5 * (12 + 4))
wrong(it, 1, "diagonal", 5 * 12)
key_num(it, 2, sp.solve(T.det(), k)[0])
key_num(it, 3, 4)
ok(sp.Matrix([[3, 6], [2, 4]]) * sp.Matrix([2, -1]) == sp.Matrix([0, 0]), "vinyl kernel")
bands(it, 1); bands(it, 2); bands(it, 3)
says(it, 2, "question", "at $k = 2$, where it is 8")
stale(it, [r"= 50", r"\b70\b", r"k = 1\b"])

# ------------------------------------------------------------------ gas hubs (least-squares/problems-3)
it = item("p-gas-hubs")
t = np.array([0, 1, 2, 3, 4.0])
yN = np.array([3.5, 0, -0.5, -3, -5])
yS = np.array([2, 1, -2, -2, -4.0])
ok("(0, 1, 2, 3, 4)" in it["prose"] and "(3.5, 0, -0.5, -3, -5)" in it["prose"] and "(2, 1, -2, -2, -4)" in it["prose"], "gas prose data")
Am = np.column_stack([np.ones(5), t])
AtA = Am.T @ Am
ok(AtA.tolist() == [[5, 10], [10, 30]], "gas A^T A")
key_num(it, 1, AtA[1, 1])
ok(sum(F(i) ** 2 for i in range(5)) == 30, "gas sum of squares exact")
wrong(it, 1, "count", AtA[0, 0]); wrong(it, 1, "sum", AtA[0, 1]); wrong(it, 1, "sum-squared", t.sum() ** 2)
ok((Am.T @ yN).tolist() == [-5, -30] and (Am.T @ yS).tolist() == [-5, -25], "gas A^T y")
says(it, 2, "question", "[[5, 10], [10, 30]]", "[-5, -30]")
says(it, 3, "question", "[-5, -25]")
G = sp.Matrix([[5, 10], [10, 30]])
fN = G.LUsolve(sp.Matrix([-5, -30])); fS = G.LUsolve(sp.Matrix([-5, -25]))
ok(list(fN) == [3, -2] and list(fS) == [2, sp.Rational(-3, 2)], "gas fits exact")
ok(np.allclose(np.polyfit(t, yN, 1)[::-1], [3, -2]) and np.allclose(np.polyfit(t, yS, 1)[::-1], [2, -1.5]), "gas fits by polyfit")
ok(np.allclose(np.linalg.lstsq(Am, np.column_stack([yN, yS]), rcond=None)[0].T, [[3, -2], [2, -1.5]]), "gas fits by lstsq")
key_vec(it, 2, (3, -2)); key_vec(it, 3, (2, F(-3, 2))); key_vec(it, 4, (1, F(-1, 2)))
wrong(it, 2, "diagonal", (F(-5, 5), F(-30, 30))); wrong(it, 2, "swapped", (-2, 3)); wrong(it, 2, "no-sign", (3, 2))
wrong(it, 3, "diagonal", (F(-5, 5), F(-25, 30))); wrong(it, 3, "no-sign", (2, F(3, 2)))
wrong(it, 4, "added", (5, F(-7, 2))); wrong(it, 4, "reversed", (-1, F(1, 2)))
sp_ = yN - yS
ok(sp_.tolist() == [1.5, -1, 1.5, -1, -1] and sp_.sum() == 0, "gas spread and its mean")
says(it, 5, "question", "(1.5, -1, 1.5, -1, -1)")
ok(np.allclose(np.polyfit(t, sp_, 1)[::-1], [1, -0.5]), "gas spread fit by polyfit")
e = sp_ - (1 - 0.5 * t)
ok(e.tolist() == [0.5, -1.5, 1.5, -0.5, 0], "gas spread residuals")
sse, sst = (e ** 2).sum(), ((sp_ - sp_.mean()) ** 2).sum()
ok(sse == 5 and sst == 7.5, "gas spread SSE 5, SST 7.5")
key_num(it, 5, 1 - sse / sst)
ok(close(np.corrcoef(t, sp_)[0, 1] ** 2, 1 / 3), "gas R^2 as the squared correlation")
eN, eS = yN - (3 - 2 * t), yS - (2 - 1.5 * t)
ok(close((eN ** 2).sum(), 1.5) and close((eS ** 2).sum(), 1.5), "gas hub SSEs 1.5 each")
sstN = ((yN - yN.mean()) ** 2).sum()
ok(close(sstN, 41.5), "gas hub N SST 41.5")
wrong(it, 5, "ratio", sse / sst); wrong(it, 5, "added-sse", 1 - 3 / 7.5); wrong(it, 5, "hub-n", 1 - 1.5 / 41.5)
r2S = 1 - 1.5 / ((yS - yS.mean()) ** 2).sum()
ok(r2S > 0.9, "gas: temperature explains hub S well too (explain of part 5)")
bands(it, 1); bands(it, 5, extra_ok=(0.333, 0.3333), extra_no=(0.33, 0.334))
stale(it, [r"\(1, -2\)", r"0\.5, -1\.5\)", r"\(0\.5, -0\.5\)", r"= 15\b", r"-5/3", r"-4/3", r"1\.5, -3\.5"])

# ------------------------------------------------------------------ strain gauges (eigen/problems-2 p-river-gauges)
it = item("p-river-gauges")
c = sp.symbols("c")
K = sp.Matrix([[4, 2, 1], [2, 3, 1], [1, 1, c]])
ok(r"4 & 2 & 1 \\ 2 & 3 & 1 \\ 1 & 1 & c" in it["prose"] and "c = 0.5" in it["prose"], "gauges prose prints K and c")
E = K.copy()
E[1, :] = E[1, :] - sp.Rational(1, 2) * E[0, :]
piv2 = E[1, 1]
key_num(it, 1, piv2)
ok(K[:2, :2].det() / 4 == 2, "gauges second pivot by the corner determinant")
wrong(it, 1, "multiplier-one", 3 - 1 * 2); wrong(it, 1, "multiplier-two", 3 - 2 * 2)
ok(list(E[1, :]) == [0, 2, sp.Rational(1, 2)], "gauges row 2 after step 1")
E[2, :] = E[2, :] - sp.Rational(1, 4) * E[0, :]
ok(list(E[2, :]) == [0, sp.Rational(1, 2), c - sp.Rational(1, 4)], "gauges row 3 after step 1")
E[2, :] = E[2, :] - (E[2, 1] / E[1, 1]) * E[1, :]
d = sp.simplify(c - E[2, 2])
key_num(it, 2, d)
ok(sp.simplify(K.det() - (8 * c - 3)) == 0 and sp.simplify(K.det() / K[:2, :2].det() - (c - sp.Rational(3, 8))) == 0, "gauges det 8c - 3; third pivot c - 3/8")
for cv in (0.3, 0.375, 0.5):
    ev = np.linalg.eigvalsh(np.array(K.subs(c, cv), float)).min()
    ok((ev > 1e-12) == (cv > 0.375), f"gauges positive definite at c = {cv}: {cv > 0.375} (eigvalsh)")
wrong(it, 2, "one-step", sp.Rational(1, 4))
wrong(it, 2, "big-multiplier", sp.Rational(1, 4) + sp.Rational(1, 2) * sp.Rational(1, 2))
wrong(it, 2, "added", sp.Rational(1, 4) - sp.Rational(1, 8))
K0 = K.subs(c, sp.Rational(3, 8))
ns = K0.nullspace()[0]; ns = ns / ns[2]
key_vec(it, 3, tuple(F(int(x.p), int(x.q)) for x in ns))
ok(list(ns) == [sp.Rational(-1, 8), sp.Rational(-1, 4), 1], "gauges null vector exact")
vt = np.linalg.svd(np.array(K0, float))[2][-1]
ok(np.allclose(vt / vt[2], [-0.125, -0.25, 1]), "gauges null vector by SVD")
wrong(it, 3, "sign", (F(1, 8), F(1, 4), 1)); wrong(it, 3, "swapped", (F(-1, 4), F(-1, 8), 1))
wrong(it, 3, "no-b", (F(-1, 4), F(-1, 4), 1))           # 4a + 1 = 0 with 2b left out
w = sp.Matrix([sp.Rational(-1, 8), sp.Rational(-1, 4), 1])
K5 = K.subs(c, sp.Rational(1, 2))
ok(list(K5 * w) == [0, 0, sp.Rational(1, 8)], "gauges Kw at c = 0.5")
q = (w.T * K5 * w)[0]
key_num(it, 4, q)
Kn = np.array(K5, float); wn = np.array([-0.125, -0.25, 1])
ok(close(wn @ Kn @ wn, 0.125), "gauges w^T K w by NumPy")
ws = sp.Matrix([sp.Rational(1, 8), sp.Rational(1, 4), 1])
wrong(it, 4, "sign", (ws.T * K5 * ws)[0]); wrong(it, 4, "c-only", sp.Rational(1, 2)); wrong(it, 4, "boundary", sp.Rational(3, 8))
# "removes what A and B predict of C": the population regression of C on A and B
beta = np.linalg.solve(Kn[:2, :2], Kn[:2, 2])
ok(np.allclose(beta, [0.125, 0.25]), "gauges regression of C on A and B has slopes (0.125, 0.25)")
resid_var = Kn[2, 2] - Kn[:2, 2] @ beta
ok(close(resid_var, 0.125), "gauges residual variance 0.125")
key_num(it, 5, 1 - q / sp.Rational(1, 2))
ok(close(1 - resid_var / Kn[2, 2], 0.75), "gauges R^2 by the regression")
rng = np.random.default_rng(7)
Z = rng.multivariate_normal(np.zeros(3), Kn, size=400_000)
bh = np.linalg.lstsq(Z[:, :2], Z[:, 2], rcond=None)[0]
r2 = 1 - np.var(Z[:, 2] - Z[:, :2] @ bh) / np.var(Z[:, 2])
ok(abs(r2 - 0.75) < 0.01 and np.abs(bh - [0.125, 0.25]).max() < 0.01, f"gauges R^2 by simulation ({r2:.4f})")
wrong(it, 5, "unexplained", sp.Rational(1, 4)); wrong(it, 5, "not-scaled", 1 - sp.Rational(1, 8))
for n in (1, 2, 4, 5):
    bands(it, n)
says(it, 2, "explain", "8c - 3"); says(it, 5, "explain", "0.375/c")
stale(it, [r"river", r"correlation", r"standardis", r"0\.28", r"1\.28", r"0\.72"])

# ------------------------------------------------------------------ tank part 5 (eigen/problems-2)
it = item("p-tank-thermometers")
Sm = sp.Matrix([[3, 1, 1], [1, 3, 1], [1, 1, 3]])
w = sp.Matrix([sp.Rational(3, 5), sp.Rational(1, 4), sp.Rational(3, 20)])
ok("(0.6, 0.25, 0.15)" in part(it, 5)["question"], "tank part 5 prints w")
d = w - sp.Matrix([1, 1, 1]) / 3
ok(list(d) == [sp.Rational(4, 15), sp.Rational(-1, 12), sp.Rational(-11, 60)] and sum(d) == 0, "tank d")
ok(Sm * d == 2 * d, "tank S d = 2 d")
d2 = (d.T * d)[0]
ok(d2 == sp.Rational(67, 600), "tank |d|^2 = 67/600")
v1 = sp.Rational(5, 3) + 2 * d2
v2 = (w.T * Sm * w)[0]
ok(v1 == v2 == sp.Rational(189, 100), "tank variance 189/100 both ways")
wn = np.array([0.6, 0.25, 0.15]); Sn = np.array(Sm, float)
ok(close(wn @ Sn @ wn, 1.89), "tank by NumPy")
vals, vecs = np.linalg.eigh(Sn)
ok(close(sum(l * (vecs[:, i] @ wn) ** 2 for i, l in enumerate(vals)), 1.89), "tank by the eigen decomposition")
key_num(it, 5, v1)
wrong(it, 5, "no-eigenvalue", sp.Rational(5, 3) + d2); wrong(it, 5, "d-only", 2 * d2)
wrong(it, 5, "no-cov", 3 * (w.T * w)[0])
ok(3 * (w.T * w)[0] == sp.Rational(267, 200) and (w.T * w)[0] == sp.Rational(89, 200), "tank diagonal part 3(0.445) = 1.335")
cross = w[0] * w[1] + w[0] * w[2] + w[1] * w[2]
ok(cross == sp.Rational(111, 400) and 2 * cross == sp.Rational(111, 200), "tank off-diagonal part 2(0.2775) = 0.555")
says(it, 5, "correct", "\\tfrac{67}{600} = 0.1117", "1.89"); says(it, 5, "no-cov", "0.15 + 0.09 + 0.0375", "0.555")
says(it, 5, "explain", "3(0.445) + 2(0.2775) = 1.89")
ok(w[0] * w[1] == sp.Rational(15, 100) and w[0] * w[2] == sp.Rational(9, 100) and w[1] * w[2] == sp.Rational(375, 10000), "tank cross products")
bands(it, 5, extra_ok=(1.89,), extra_no=(1.88, 1.9))
# the claim "the plain average has the least error": minimise w^T S w over weights adding to 1
ones = np.ones(3); wopt = np.linalg.solve(Sn, ones); wopt /= wopt.sum()
ok(np.allclose(wopt, 1 / 3), "tank: the plain average minimises the variance")
stale({"id": "tank-5", "prose": "", "parts": [part(it, 5)]}, [r"0\.0467", r"0\.093", r"1\.76", r"1\.71", r"1\.14\b"])

# ------------------------------------------------------------------ crab part 5 (eigen/problems-3)
it = item("p-crab-sizes")
wd = np.array([68, 74, 60, 46, 52.0]); cl = np.array([59, 42, 40, 38, 21.0])
C = np.cov(wd, cl)
ok(np.allclose(C, [[130, 90], [90, 182.5]]), "crab covariance matrix")
vals, vecs = np.linalg.eigh(C)
ok(np.allclose(vals, [62.5, 250]), "crab eigenvalues")
lam = sp.Matrix([[130, 90], [90, sp.Rational(365, 2)]]).eigenvals()
ok(set(lam) == {250, sp.Rational(125, 2)}, "crab eigenvalues exact")
score = 0.6 * 8 + 0.8 * 19
ok(close(score, 20), "crab 1 score 20")
scores = np.column_stack([wd - 60, cl - 40]) @ np.array([0.6, 0.8])
ok(close(scores.var(ddof=1), 250) and close(scores[0], 20), "crab PC1 scores have variance 250")
key_num(it, 5, 20 / sp.sqrt(250))
ok(close(scores[0] / scores.std(ddof=1), 1.2649110640673518), "crab z by NumPy")
for route in (20 / 15.811, 20 / 15.81, 20 / math.sqrt(250)):
    ok(round(route, 3) == 1.265, f"crab {route:.6f} rounds to 1.265")
wrong(it, 5, "variance", 20 / 250); wrong(it, 5, "total", 20 / math.sqrt(312.5)); wrong(it, 5, "pc2-sd", 20 / math.sqrt(62.5))
ok(round(math.sqrt(250), 3) == 15.811, "sqrt 250 = 15.811")
says(it, 5, "correct", "15.811", "1.265")
bands(it, 5, extra_ok=(1.265, 1.2649), extra_no=(1.26, 1.27, 1.264, 1.266))
# part 3 as reworded: the printed columns are eigenvectors of the printed matrix
ok(np.allclose(C @ [0.8, -0.6], 62.5 * np.array([0.8, -0.6])) and np.allclose(C @ [-0.6, -0.8], 250 * np.array([-0.6, -0.8])), "crab part 3 columns are eigenvectors")
stale({"id": "crab-5", "prose": "", "parts": [part(it, 5)]}, [r"15\.81\b", r"1\.26\b", r"1\.13\b"])

# ------------------------------------------------------------------ gene screen (testing/problems-3)
it = item("p-gene-screen")
m = 60
shown = [F("0.0004"), F("0.0021"), F("0.0055"), F("0.0058"), F("0.0090"), F("0.0096"), F("0.0190"), F("0.034")]
for s in ("0.0004, 0.0021, 0.0055, 0.0058, 0.0090, 0.0096, 0.0190 and 0.034", "other 52 are all above 0.2"):
    ok(s in it["prose"], f"gene prose prints {s!r}")
ok(shown == sorted(shown), "gene p-values are sorted")


def bh_count(ps, q, m=60):
    ks = [i + 1 for i, p in enumerate(sorted(ps)) if p <= F(i + 1) * q / m]
    return max(ks) if ks else 0


key_num(it, 1, F(1, 600))
wrong(it, 1, "unadjusted", F(1, 10)); wrong(it, 1, "times-m", 6); wrong(it, 1, "five-percent", F(5, 100) / 60)
bonf = sum(p <= F(1, 600) for p in shown)
key_num(it, 2, bonf)
wrong(it, 2, "unadjusted", sum(p < F(1, 10) for p in shown)); wrong(it, 2, "bh", bh_count(shown, F(1, 10)))
passes = [i + 1 for i, p in enumerate(shown) if p <= F(i + 1, 600)]
ok(passes == [1, 2, 4, 6], "gene ranks passing their own bar: 1, 2, 4, 6")
key_num(it, 3, bh_count(shown, F(1, 10)))
wrong(it, 3, "first-fail", next(i for i, p in enumerate(shown) if p > F(i + 1, 600)))
wrong(it, 3, "bonferroni", bonf); wrong(it, 3, "unadjusted", 8); wrong(it, 3, "count-passes", len(passes))
# second route: statsmodels, with the other 52 anywhere above 0.2 (three fills)
from statsmodels.stats.multitest import multipletests  # noqa: E402

rng = np.random.default_rng(3)
for fill in (np.full(52, 0.2001), np.linspace(0.21, 0.99, 52), rng.uniform(0.2001, 1, 52)):
    ps = np.array([float(p) for p in shown] + list(fill))
    ok(multipletests(ps, alpha=0.10, method="fdr_bh")[0].sum() == 6, "gene BH count 6 by statsmodels")
    ok(multipletests(ps, alpha=0.10, method="bonferroni")[0].sum() == 1, "gene Bonferroni count 1 by statsmodels")
    ok(multipletests(ps, alpha=0.20, method="fdr_bh")[0].sum() == 7, "gene BH count 7 at q = 0.20")
    ok(multipletests(ps, alpha=0.0959, method="fdr_bh")[0].sum() == 4 and multipletests(ps, alpha=0.0961, method="fdr_bh")[0].sum() == 6, "gene list is 4 just under q = 0.096 and 6 just over")
qmin = F(60) * shown[5] / 6
key_num(it, 4, qmin)
ok(qmin == F(96, 1000), "gene smallest q = 0.096 exactly")
lo, hi = 0.0, 0.2                                           # bisection on q for rank 6 to be in the list
for _ in range(60):
    mid = (lo + hi) / 2
    if bh_count(shown, F(mid)) >= 6:
        hi = mid
    else:
        lo = mid
ok(abs(hi - 0.096) < 1e-9, "gene smallest q by bisection")
wrong(it, 4, "no-divide", 60 * shown[5]); wrong(it, 4, "rank-five", F(60) * shown[4] / 5); wrong(it, 4, "bar", F(6, 600))
ok(F(60) * shown[2] / 3 == F(11, 100) and F(60) * shown[4] / 5 == F(108, 1000), "gene ranks 3 and 5 alone need 0.11 and 0.108")
ok(round(float(F(7) * F(2, 10) / 60), 5) == 0.02333 and shown[6] < F(7) * F(2, 10) / 60, "gene rank 7 bar at q = 0.20 is 0.02333, above 0.0190")
ok(round(float(F(8, 600)), 5) == 0.01333 and round(float(F(4, 600)), 5) == 0.00667 and round(float(F(5, 600)), 5) == 0.00833, "gene bars printed in part 3")
for n in (1, 2, 3, 4):
    bands(it, n)
bands(it, 4, extra_ok=(0.096,), extra_no=(0.0959, 0.0961, 0.0948))
opts = part(it, 5)["widget"]["options"]
ok([o["id"] for o in opts if o.get("correct")] == ["right"], "gene part 5 has one keyed option")
longest = max(len(o["text"]) for o in opts if not o.get("correct"))
ok(len(opts[0]["text"]) <= 1.5 * longest, "gene part 5 key under 1.5 times the longest distractor")
stale(it, [r"0\.0948", r"0\.474", r"0\.1065", r"BH's 5", r"5 genes", r"rank 4, since"])

print(f"recompute: {checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
