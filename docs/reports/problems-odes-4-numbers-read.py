#!/usr/bin/env python3
"""Second read of app/content/courses/odes/problems-4.json (Transforms and numerical solution).

Imports nothing from the author's script. Every equation is typed here from the prose.
Laplace: each transform by sympy laplace_transform and by the defining integral; each inverse by
inverse_laplace_transform, by sympy residue(), and by putting the answer back into the equation and its
starting values. Euler and Runge-Kutta: the reader's own steppers, once in exact fractions and once in
50-digit mpmath; error figures against the closed form at 50 digits. Stability: the RK4 edge as the real
root of R(z) = 1, and the two-equation system stepped as a matrix (spectral radius of the step matrix).
Keys and wrong[] values are read from the JSON and compared with the reader's own values.
Exit 0 when every check holds.

Run from the repo root: <scratchpad>/venv/bin/python docs/reports/problems-odes-4-numbers-read.py
"""
import json
import math
import sys
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 50
DOC = json.load(open("app/content/courses/odes/problems-4.json"))
ITEMS = {it["id"]: it for it in DOC["items"]}
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", msg)


def W(item, k):
    return ITEMS[item]["parts"][k - 1]["widget"]


def text_of(item, k=None):
    o = ITEMS[item] if k is None else ITEMS[item]["parts"][k - 1]
    return json.dumps(o, ensure_ascii=False).replace("\\\\", "\\")


s, t = sp.symbols("s t", positive=True)
S = sp.Symbol("s")
LOCAL = {"s": S, "t": t, "e": sp.E}


def tex(expr_text):
    """The small LaTeX the keys use -> sympy."""
    import re
    x = expr_text
    while "\\frac" in x:
        x = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", x)
    x = re.sub(r"e\^\{([^{}]*)\}", r"exp(\1)", x)
    x = re.sub(r"e\^\(([^()]*)\)", r"exp(\1)", x)
    x = x.replace("^", "**")
    x = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", x)
    x = re.sub(r"\)\(", ")*(", x)
    x = re.sub(r"([st])\(", r"\1*(", x)
    x = re.sub(r"\)(exp|[st\d])", r")*\1", x)
    return sp.sympify(x, locals={"s": S, "t": t, "exp": sp.exp}, rational=True)


def eq(a, b):
    return sp.simplify(a - b) == 0


def L(f):
    return sp.laplace_transform(f, t, S, noconds=True)


def band_clear(w):
    """each wrong band is clear of the key band and holds no accepted value"""
    for x in w.get("wrong", []):
        if isinstance(x.get("value"), (int, float)):
            ok(abs(x["value"] - w["answer"]) > w["tol"]["abs"] + x["tol"]["abs"], f"wrong {x['id']} band clear of the key band")


# ---------------------------------------------------------------- set shape
LEVEL = ["l14-laplace-transform", "l15-solving-with-laplace", "l16-euler-method", "l17-runge-kutta", "l18-four-decimal-places"]
SK = set()
for l in LEVEL:
    SK |= set(json.load(open(f"app/content/courses/odes/{l}.json"))["skills"])
ok(DOC["level"] == 4 and DOC["course"] == "odes" and 3 <= len(DOC["items"]) <= 5, "set shape")
typed = total = 0
for it in DOC["items"]:
    ok(3 <= len(it["parts"]) <= 5 and 3 <= it["difficulty"] <= 5 and set(it["skills"]) <= SK, f"{it['id']}: parts, difficulty, skills of the level")
    for p in it["parts"]:
        total += 1
        typed += p["widget"]["kind"] in ("numeric", "expression")
        for x in p["widget"].get("wrong", []):
            ok(x["id"] in p["feedback"]["byKey"], f"{it['id']}: wrong {x['id']} has a line")
ok(any(it["difficulty"] == 5 for it in DOC["items"]) and Fr(typed, total) >= Fr(2, 3), "a 5 in the set; two thirds typed")

# ---------------------------------------------------------------- p-test-rig (y'' + 6y' + 8y = 24e^(-8t))
P = "p-test-rig"
force = 24 * sp.exp(-8 * t)
F1 = L(force)
ok(eq(F1, 24 / (S + 8)), "L{24e^(-8t)} = 24/(s+8) by laplace_transform")
ok(abs(mp.quad(lambda u: mp.exp(-mp.mpf(7) / 5 * u) * 24 * mp.exp(-8 * u), [0, mp.inf]) - mp.mpf(24) / (mp.mpf(7) / 5 + 8)) < 1e-20, "the same by the defining integral at s = 1.4")
ok(eq(tex(W(P, 1)["answer"]), F1), "part 1 key")
w = {x["id"]: tex(x["tex"]) for x in W(P, 1)["wrong"]}
ok(eq(w["sign"], L(24 * sp.exp(8 * t))) and eq(w["no-factor"], L(sp.exp(-8 * t))), "part 1 slips: transform of 24e^(8t); the 24 dropped")
ok(all(not eq(v, F1) for v in w.values()), "part 1 wrong differ from key")
# part 2
Ysym = sp.Symbol("Y")
Y = sp.solve(sp.Eq(S**2 * Ysym + 6 * S * Ysym + 8 * Ysym, F1), Ysym)[0]
ok(eq(Y, 24 / ((S + 2) * (S + 4) * (S + 8))), "Y = 24/((s+2)(s+4)(s+8))")
ok(eq(tex(W(P, 2)["answer"]), Y) and all(eq(tex(a), Y) for a in W(P, 2)["accept"]), "part 2 key and accept forms")
ok(sp.factor(S**2 + 6 * S + 8) == (S + 2) * (S + 4) and sorted(sp.roots(S**2 + 6 * S + 8)) == [-4, -2], "s^2 + 6s + 8 = (s+2)(s+4)")
w = {x["id"]: tex(x["tex"]) for x in W(P, 2)["wrong"]}
ok(eq(w["carried-sign"], (24 / (S - 8)) / (S**2 + 6 * S + 8)), "part 2 carried-sign: 24/(s-8) carried")
ok(eq(w["root-signs"], 24 / ((S + 8) * (S - 2) * (S - 4))), "part 2 root-signs")
ok(all(not eq(v, Y) for v in w.values()), "part 2 wrong differ from key")
# part 3
res = {p: sp.residue(Y, S, p) for p in (-2, -4, -8)}
ok(res == {-2: 2, -4: -3, -8: 1}, "residues 2, -3, 1 by sympy residue")
ok(sp.apart(Y, S) == 2 / (S + 2) - 3 / (S + 4) + 1 / (S + 8), "the same by apart")
ok(W(P, 3)["answer"] == -3 and {x["id"]: x["value"] for x in W(P, 3)["wrong"]} == {"sign": 3, "other-pole": 2}, "part 3 key and slips")
ok(sum(res.values()) == 0, "explain: the residues add to 0 = y(0)")
# part 4
y = 2 * sp.exp(-2 * t) - 3 * sp.exp(-4 * t) + sp.exp(-8 * t)
yinv = sp.inverse_laplace_transform(Y, S, t)
ok(eq(yinv.subs(sp.Heaviside(t), 1), y), "y by inverse_laplace_transform")
ok(eq(sp.diff(y, t, 2) + 6 * sp.diff(y, t) + 8 * y, force) and y.subs(t, 0) == 0 and sp.diff(y, t).subs(t, 0) == 0, "y satisfies the equation and both starting values")
ok(eq(tex(W(P, 4)["answer"]), y) and all(eq(tex(a), y) for a in W(P, 4)["accept"]), "part 4 key and accept forms")
w = {x["id"]: tex(x["tex"]) for x in W(P, 4)["wrong"]}
ok(eq(w["exp-sign"], y.subs(t, -t)) and eq(w["carried-sign"], 2 * sp.exp(-2 * t) + 3 * sp.exp(-4 * t) + sp.exp(-8 * t)), "part 4 slips")
ok(w["carried-sign"].subs(t, 0) == 6, "carried-sign line: y(0) = 6")
ok((2 - 3 + 1, -4 + 12 - 8) == (0, 0), "feedback sums y(0) and y'(0)")
# part 5: peak by calculus (u = e^(-2t)) and by a fine grid
u = sp.Symbol("u", positive=True)
yu = 2 * u - 3 * u**2 + u**4
ok(sp.expand(sp.diff(yu, u) - 2 * (u - 1) * (2 * u**2 + 2 * u - 1)) == 0, "printed dy/du = 2(u-1)(2u^2+2u-1)")
ok(sp.expand(yu - u * (1 - u) ** 2 * (u + 2)) == 0, "y = u(1-u)^2(u+2) >= 0: no overshoot")
ur = [r for r in sp.solve(2 * u**2 + 2 * u - 1, u) if 0 < r < 1]
ok(ur == [(sp.sqrt(3) - 1) / 2], "root in (0, 1): (sqrt 3 - 1)/2")
peak = sp.simplify(yu.subs(u, ur[0]))
ok(sp.simplify(peak - (6 * sp.sqrt(3) - 9) / 4) == 0, "peak (6 sqrt 3 - 9)/4")
tp = sp.log(1 + sp.sqrt(3)) / 2
ok(sp.simplify(y.subs(t, tp) - peak) == 0, "y at t = ln(1 + sqrt 3)/2 is the peak")
grid = np.linspace(0, 12, 1200001)
yg = 2 * np.exp(-2 * grid) - 3 * np.exp(-4 * grid) + np.exp(-8 * grid)
ok(abs(yg.max() - float(peak)) < 1e-9 and abs(grid[yg.argmax()] - float(tp)) < 1e-4 and yg.min() >= -1e-15, "peak by grid; y never negative")
ok(abs(W(P, 5)["answer"] - float(peak)) <= W(P, 5)["tol"]["abs"] and round(float(peak), 3) == 0.348, "part 5 key 0.3481, prints 0.348")
slips = {"u-value": float(ur[0]), "time": float(tp), "at-one": float(y.subs(t, 1))}
for x in W(P, 5)["wrong"]:
    ok(abs(slips[x["id"]] - x["value"]) <= x["tol"]["abs"], f"part 5 wrong {x['id']} holds its slip value")
band_clear(W(P, 5))
# reuse guard (finding 1): not lesson 15's Y shifted and scaled; fails if the old item returns
Y15 = 2 / (S * (S + 1) * (S + 2))
ok(not any(eq(Y, c * Y15.subs(S, S + k)) for c in (1, 2, 4, 8, 12, 24) for k in range(0, 9)), "Y is no shift and scale of l15 screens[3]")
ok(len({-2 - -4, -4 - -8}) == 2, "pole gaps unequal")
# finding 2: the RK4 limit is stated for real negative lambda
ok("real negative" in text_of("p-dose-simulator"), "RK4 limit stated for real negative lambda")

# ---------------------------------------------------------------- p-skydiver-check
P = "p-skydiver-check"
Vs = sp.Symbol("V")
V = sp.solve(sp.Eq(S * Vs - 0, sp.Rational(49, 5) / S - sp.Rational(1, 5) * Vs), Vs)[0]
ok(eq(V, sp.Rational(49, 5) / (S * (S + sp.Rational(1, 5)))), "V = 9.8/(s(s+0.2))")
ok(eq(tex(W(P, 1)["answer"]), V) and all(eq(tex(a), V) for a in W(P, 1)["accept"]), "part 1 key and accept forms")
w = {x["id"]: tex(x["tex"]) for x in W(P, 1)["wrong"]}
ok(eq(w["constant"], sp.Rational(49, 5) / (S + sp.Rational(1, 5))) and eq(w["sign"], sp.Rational(49, 5) / (S * (S - sp.Rational(1, 5)))), "part 1 slips")
ok(all(not eq(v_, V) for v_ in w.values()), "part 1 wrong differ from key")
ok(sp.residue(V, S, 0) == 49 and sp.residue(V, S, -sp.Rational(1, 5)) == -49, "residues 49 and -49")
v = 49 * (1 - sp.exp(-t / 5))
ok(eq(sp.inverse_laplace_transform(V, S, t).subs(sp.Heaviside(t), 1), v), "v = 49(1 - e^(-0.2t)) by inverse transform")
ok(eq(sp.diff(v, t), sp.Rational(49, 5) - v / 5) and v.subs(t, 0) == 0, "v satisfies the equation and v(0) = 0")
ok(eq(L(v), V), "L{v} = V")
ok(sp.limit(v, t, sp.oo) == 49, "terminal speed 49")
v2 = mp.mpf(49) * (1 - mp.exp(mp.mpf(-2) / 5))
ok(abs(v2 - mp.mpf("16.154317")) < 1e-6, "v(2) = 16.154317...")
ok(abs(W(P, 2)["answer"] - float(v2)) <= 5e-5 and round(float(v2), 4) == 16.1543, "part 2 key is v(2) to 4 places")
slips = {"no-divide": 9.8 * (1 - math.exp(-0.4)), "carried-constant": 9.8 * math.exp(-0.4), "carried-sign": 49 * (math.exp(0.4) - 1)}
for x in W(P, 2)["wrong"]:
    ok(abs(slips[x["id"]] - x["value"]) <= 5e-5, f"part 2 wrong {x['id']} = {slips[x['id']]:.6f}")
band_clear(W(P, 2))
ok(eq(sp.inverse_laplace_transform(sp.Rational(49, 5) / (S + sp.Rational(1, 5)), S, t).subs(sp.Heaviside(t), 1), sp.Rational(49, 5) * sp.exp(-t / 5)), "carried-constant line: 9.8/(s+0.2) inverts to 9.8e^(-0.2t)")
ok(eq(sp.inverse_laplace_transform(sp.Rational(49, 5) / (S * (S - sp.Rational(1, 5))), S, t).subs(sp.Heaviside(t), 1), 49 * (sp.exp(t / 5) - 1)), "carried-sign line: 49(e^(0.2t) - 1)")
ok(mp.nstr(mp.exp(mp.mpf(-2) / 5), 6) == "0.67032" and abs(49 * 0.329680 - 16.1543) < 5e-5, "explain: e^(-0.4) = 0.670320, 49 x 0.329680 = 16.1543")

f_ex = lambda u: Fr(49, 5) - Fr(1, 5) * u


def euler(f, y0, T, n):
    h, yv = T / n, y0
    for _ in range(n):
        yv = yv + h * f(yv)
    return yv


def rk4(f, y0, T, n, trace=None):
    h, yv = T / n, y0
    for _ in range(n):
        k1 = f(yv)
        k2 = f(yv + h / 2 * k1)
        k3 = f(yv + h / 2 * k2)
        k4 = f(yv + h * k3)
        if trace is not None:
            trace.append((k1, k2, k3, k4))
        yv = yv + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return yv


e2 = euler(f_ex, Fr(0), Fr(2), 2)
ok(e2 == Fr(1764, 100) and W(P, 3)["answer"] == 17.64, "Euler h = 1: 17.64 exactly")
ok(euler(f_ex, Fr(0), Fr(1), 1) == Fr(98, 10) and f_ex(Fr(98, 10)) == Fr(784, 100), "v1 = 9.8, second slope 7.84")
ok(W(P, 3)["wrong"][0]["value"] == 19.6 and euler(f_ex, Fr(0), Fr(2), 1) == Fr(196, 10), "same-slope slip 19.6 is one step of h = 2")
band_clear(W(P, 3))
ok(mp.nstr(mp.mpf(1764) / 100 - v2, 5) == "1.4857", "Euler error 1.4857")
ok(float(e2) > float(v2), "Euler overshoots")
tr = []
r1 = rk4(f_ex, Fr(0), Fr(2), 1, tr)
ok(tr[0] == (Fr(98, 10), Fr(784, 100), Fr(8232, 1000), Fr(65072, 10000)), "RK4 slopes 9.8, 7.84, 8.232, 6.5072")
ok(sum(c * k for c, k in zip((1, 2, 2, 1), tr[0])) == Fr(484512, 10000) and r1 == Fr(161504, 10000), "weighted sum 48.4512; one step gives 16.1504 exactly")
ok(W(P, 4)["answer"] == 16.1504, "part 4 key")
slips = {"plain-mean": float(2 * sum(tr[0]) / 4), "no-h": float(Fr(484512, 10000) / 6)}
for x in W(P, 4)["wrong"]:
    ok(abs(slips[x["id"]] - x["value"]) <= 5e-5, f"part 4 wrong {x['id']} = {slips[x['id']]:.6f}")
band_clear(W(P, 4))
f_mp = lambda u: mp.mpf(49) / 5 - u / 5
err = {n: v2 - rk4(f_mp, mp.mpf(0), mp.mpf(2), n) for n in (1, 2, 4, 8)}
ok(mp.nstr(err[1], 2) == "0.0039", "RK4 one-step error 0.0039 (0.003917)")
ok(mp.nstr(err[2], 3) == "0.000207" and mp.nstr(err[4], 3) == "1.19e-5", "true RK4 errors 0.000207 at n = 2 and 0.0000119 at n = 4")
# exact stability function check of the same numbers: v_n = 49(1 - R(-0.2h)^n)
R = lambda z: 1 + z + z**2 / 2 + z**3 / 6 + z**4 / 24
ok(all(abs((49 * (1 - R(mp.mpf(-2) / 5 / n) ** n)) - rk4(f_mp, mp.mpf(0), mp.mpf(2), n)) < mp.mpf(10) ** -40 for n in (1, 2, 4, 8)), "RK4 by its stability polynomial agrees")
pred = {1: 0.0039, 2: 0.0039 / 16, 4: 0.0039 / 256}
ok(round(pred[2], 5) == 0.00024 and round(pred[4], 6) == 0.000015, "predicted 0.00024 and 0.000015")
first = next(n for n in (1, 2, 4, 8, 16) if 0.0039 / 16 ** int(math.log2(n)) < 5e-5)
first_true = next(n for n in (1, 2, 4, 8, 16) if abs(err[n]) < 5e-5) if True else None
ok(first == 4 and first_true == 4 and W(P, 5)["answer"] == 4, "part 5: first n is 4, predicted and run")
ok(next(n for n in (2**k for k in range(12)) if 0.0039 / n < 5e-5) == 128, "first-order slip 128")
ok(pred[2] < 5e-4 and pred[2] > 5e-5, "half-unit slip 2: below 5e-4, not below 5e-5")
ok(round(float(rk4(f_mp, mp.mpf(0), mp.mpf(2), 4)), 4) == 16.1543, "n = 4 does print 16.1543")
ok({x["id"]: x["value"] for x in W(P, 5)["wrong"]} == {"half-unit": 2, "first-order": 128}, "part 5 wrong values")
ok(abs(err[1] / err[2] - 16) < 3.5 and abs(err[2] / err[4] - 16) < 2, "error ratios near 16 (18.9 and 17.4)")

# ---------------------------------------------------------------- p-dose-simulator
P = "p-dose-simulator"
A = sp.Matrix([[-6, 0], [6, -sp.Rational(1, 2)]])
ok(sorted(A.eigenvals(multiple=True)) == [-6, -sp.Rational(1, 2)] and sorted(W(P, 1)["answers"]) == [-6, -0.5], "eigenvalues -6 and -0.5")
ok(W(P, 1)["wrong"][0]["value"].replace(" ", "") == "6,0.5", "part 1 wrong value")
ok(1 + Fr(1, 2) * -6 == -2 and W(P, 2)["answer"] == -2, "Euler factor -2 at h = 0.5")
ok({x["id"]: x["value"] for x in W(P, 2)["wrong"]} == {"abs": 2, "slow-mode": float(1 + Fr(1, 2) * Fr(-1, 2))}, "part 2 slips 2 and 0.75")
E = lambda h: sp.eye(2) + h * A
ok(tuple(E(sp.Rational(1, 2)) * sp.Matrix([1, 0]))[0] == -2, "the system's own Euler step multiplies g by -2")
h_ = sp.Symbol("h", positive=True)
sol = sp.solve_univariate_inequality(sp.Abs(1 - 6 * h_) < 1, h_, relational=False)
ok(sol == sp.Interval.open(0, sp.Rational(1, 3)), "|1 - 6h| < 1 exactly for 0 < h < 1/3")
ok(abs(W(P, 3)["answer"] - 1 / 3) <= W(P, 3)["tol"]["abs"], "part 3 key band holds 1/3")
slips = {"slow-mode": 2 / 0.5, "no-two": 1 / 6}
for x in W(P, 3)["wrong"]:
    ok(abs(slips[x["id"]] - x["value"]) <= max(x["tol"]["abs"], 5e-5), f"part 3 wrong {x['id']}")
band_clear(W(P, 3))
z = sp.Symbol("z", real=True)
edge = [r for r in sp.nroots(sp.Poly(1 + z + z**2 / 2 + z**3 / 6 + z**4 / 24 - 1, z)) if abs(sp.im(r)) < 1e-12 and sp.re(r) < -1e-9]
ok(len(edge) == 1 and round(float(-sp.re(edge[0])), 4) == 2.7853, "RK4 real stability edge 2.7853 (2.785294)")
zz = np.linspace(-2.7852, -1e-6, 200001)
ok(np.all(np.abs(1 + zz + zz**2 / 2 + zz**3 / 6 + zz**4 / 24) < 1), "|R(z)| < 1 on the whole of (-2.7852, 0)")
ok(abs(W(P, 4)["answer"] - 2.7853 / 6) <= 5e-5 and round(2.7853 / 6, 4) == 0.4642, "part 4: 2.7853/6 = 0.4642")
slips = {"slow-mode": 2.7853 / 0.5, "euler": 2 / 6}
for x in W(P, 4)["wrong"]:
    ok(abs(slips[x["id"]] - x["value"]) <= 5e-5, f"part 4 wrong {x['id']}")
band_clear(W(P, 4))
ok(0.39 < 0.4642 / (1 / 3) - 1 < 0.40, "explain: the gain is under 40% (39.3%)")
ok(round(0.4642 * 60) == 28 and Fr(1, 3) * 60 == 20, "28 minutes and 20 minutes")
# part 5: by search over n, on the system itself
An = np.array(A.tolist(), dtype=float)


def rho_euler(n):
    h = 24 / n
    return max(abs(np.linalg.eigvals(np.eye(2) + h * An)))


def rho_rk4(n):
    h = 24 / n
    M = h * An
    St = np.eye(2) + M + M @ M / 2 + M @ M @ M / 6 + M @ M @ M @ M / 24
    return max(abs(np.linalg.eigvals(St)))


ne = next(n for n in range(1, 400) if rho_euler(n) < 1 - 1e-12)
nr = next(n for n in range(1, 400) if rho_rk4(n) < 1 - 1e-12)
ok((ne, nr) == (73, 52), "fewest stable steps: Euler 73, RK4 52 (spectral radius of the step matrix)")
ok(all(rho_euler(n) < 1 for n in range(73, 400)) and all(rho_rk4(n) < 1 for n in range(52, 400)), "every finer run is stable too")
ok(abs(rho_euler(72) - 1) < 1e-12 and rho_rk4(51) > 1, "n = 72 sits on the edge; RK4 at 51 grows")
ok(math.floor(24 / (1 / 3)) + 1 == 73 and math.ceil(24 / 0.4642) == 52 and round(24 / 0.4642, 1) == 51.7, "n > 72 and n > 51.7")
ok(min(ne, 4 * nr) == 73 and 4 * nr == 208 and W(P, 5)["answer"] == 73, "part 5: 73 readings against 208")
ok({x["id"]: x["value"] for x in W(P, 5)["wrong"]} == {"rk4": 208, "edge": 72, "rk4-steps": 52}, "part 5 wrong values")
# direct runs: the gut amount after 24 h stays bounded at 73 and 52 steps
g73 = (1 - 6 * 24 / 73) ** 73
ok(abs(g73) < 1 and abs((1 - 6 * 24 / 71) ** 71) > 1, "Euler: gut mode decays at n = 73, grows at n = 71")
ok(math.exp(-6) < 0.003 and math.exp(-0.5 * 6) < 0.05, "explain: fast mode gone within an hour, slow over several hours")

# ---------------------------------------------------------------- printed numbers present in the text
for item, bits in {
    "p-test-rig": ["\\dfrac{24}{(-2)(4)} = -3", "\\dfrac{24}{(2)(6)} = 2", "\\dfrac{24}{(-6)(-4)} = 1", "\\tfrac{6\\sqrt3 - 9}{4} \\approx 0.348"],
    "p-skydiver-check": ["17.64 - 16.1543 = 1.4857", "\\tfrac13 \\times 48.4512 = 16.1504", "0.000207", "0.0000119", "f(16.464) = 6.5072"],
    "p-dose-simulator": ["n > 51.7", "4 \\times 52", "\\dfrac{2.7853}{6} \\approx 0.4642"],
}.items():
    for b in bits:
        ok(b in text_of(item), f"{item} text holds {b}")

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
