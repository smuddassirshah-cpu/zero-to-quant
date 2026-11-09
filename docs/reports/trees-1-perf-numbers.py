"""trees level 1 performance task h-derive-one-step: every number twice.

Run from the repository root: venv/bin/python -I docs/reports/trees-1-perf-numbers.py
Route A is symbolic (sympy); route B is exact arithmetic with Fractions and a
direct 2 by 2 solve, or a second floating-point formula. Exits 1 on any failure.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HW = os.path.join(ROOT, "app", "content", "courses", "trees", "homework-1.json")

fails = 0
checks = 0


def check(name, ok):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("FAIL", name)


def near(a, b, tol):
    return abs(a - b) <= tol


# ---------- symbolic route A (sympy) ----------
try:
    import sympy as sp
    S, u, d, r, dt, fu, fd, Dl, B, w, a = sp.symbols("S u d r dt f_u f_d Delta B w a", real=True)
    g = sp.exp(r * dt)
    sol = sp.solve([Dl * u * S + B * g - fu, Dl * d * S + B * g - fd], [Dl, B], dict=True)
    check("A: one copy", len(sol) == 1)
    s0 = sol[0]
    check("A: Delta", sp.simplify(s0[Dl] - (fu - fd) / (S * (u - d))) == 0)
    check("A: B", sp.simplify(s0[B] - sp.exp(-r * dt) * (u * fd - d * fu) / (u - d)) == 0)
    det = sp.Matrix([[u * S, g], [d * S, g]]).det()
    check("A: determinant", sp.simplify(det - S * g * (u - d)) == 0)
    V0 = s0[Dl] * S + s0[B]
    q = (g - d) / (u - d)
    check("A: q form", sp.simplify(V0 - sp.exp(-r * dt) * (q * fu + (1 - q) * fd)) == 0)
    check("A: 1 - q", sp.simplify((1 - q) - (u - g) / (u - d)) == 0)
    # the middle line of the aligned display
    mid = sp.exp(-r * dt) * ((g - d) * fu + (u - g) * fd) / (u - d)
    first = (fu - fd) / (u - d) + sp.exp(-r * dt) * (u * fd - d * fu) / (u - d)
    check("A: display line 1 = line 2", sp.simplify(first - mid) == 0)
    # Be^{r dt} from the down equation
    check("A: B e^{r dt}", sp.simplify(fd - d * (fu - fd) / (u - d) - (u * fd - d * fu) / (u - d)) == 0)
    # unique martingale weight
    ws = sp.solve(sp.Eq(w * u * S + (1 - w) * d * S, S * g), w)
    check("A: one weight", len(ws) == 1 and sp.simplify(ws[0] - q) == 0)
    # arbitrage payoffs: short and bank, borrow and buy, zero-cost a shares
    check("A: short-bank up", sp.simplify((S * g - u * S) - S * (g - u)) == 0)
    check("A: zero-cost trade", sp.simplify((a * u * S - a * S * g) - a * S * (u - g)) == 0)
    print("symbolic route: sympy", sp.__version__)
except ImportError:
    print("sympy missing: symbolic route skipped")

# ---------- exact route B on many trees: copy by direct solve against formulas ----------
import random
rng = random.Random(7)
for _ in range(300):
    Sv = F(rng.randint(1, 500))
    dv = F(rng.randint(10, 99), 100)
    uv = dv + F(rng.randint(1, 120), 100)
    gv = F(rng.randint(50, 250), 100)  # stands for e^{r dt}, any positive number
    fuv, fdv = F(rng.randint(-50, 50)), F(rng.randint(-50, 50))
    # Cramer on [[uS, g], [dS, g]]
    detv = uv * Sv * gv - gv * dv * Sv
    Dv = (fuv * gv - gv * fdv) / detv
    Bv = (uv * Sv * fdv - dv * Sv * fuv) / detv
    check("B: Delta formula", Dv == (fuv - fdv) / (Sv * (uv - dv)))
    check("B: B formula", Bv == (uv * fdv - dv * fuv) / (uv - dv) / gv)
    qv = (gv - dv) / (uv - dv)
    check("B: q form", Dv * Sv + Bv == (qv * fuv + (1 - qv) * fdv) / gv)
    check("B: 0<q<1 iff d<g<u", (0 < qv < 1) == (dv < gv < uv))
    if 0 < qv < 1:
        V = Dv * Sv + Bv
        check("B: bounds", min(fuv, fdv) / gv <= V <= max(fuv, fdv) / gv)
        for av in (F(-2), F(-1, 3), F(1, 2), F(3)):
            up, dn = av * Sv * (uv - gv), av * Sv * (dv - gv)
            check("B: no zero-cost arbitrage", up * dn < 0)
    if gv >= uv:
        check("B: short-bank never loses", Sv * (gv - uv) >= 0 and Sv * (gv - dv) > 0)
    if gv <= dv:
        check("B: borrow-buy never loses", Sv * (uv - gv) > 0 and Sv * (dv - gv) >= 0)

# ---------- part (d): the straddle, by the copy and by q ----------
S0, uu, dd, rr, h, K = 64.0, 1.25, 0.8, 0.06, 0.25, 64.0
Su, Sd = uu * S0, dd * S0
check("d: Su 80", Su == 80.0)
check("d: Sd 51.2", near(Sd, 51.2, 1e-12))
fU, fD = abs(Su - K), abs(Sd - K)
check("d: payoffs 16, 12.8", near(fU, 16, 1e-12) and near(fD, 12.8, 1e-12))
grow = math.exp(rr * h)
grow2 = sum((rr * h) ** k / math.factorial(k) for k in range(20))
check("d: e^0.015 two ways", near(grow, grow2, 1e-15) and f"{grow:.6f}" == "1.015113")
check("d: condition holds", dd < grow < uu)
# copy route
Delta = (fU - fD) / (Su - Sd)
check("d: Delta 1/9", near(Delta, 1 / 9, 1e-15) and f"{Delta:.4f}" == "0.1111")
check("d: 3.2/28.8", near(3.2 / 28.8, 1 / 9, 1e-15))
Bg = (uu * fD - dd * fU) / (uu - dd)
check("d: B e^{r dt} = 3.2/0.45 = 64/9", near(Bg, 3.2 / 0.45, 1e-12) and near(Bg, 64 / 9, 1e-12) and f"{Bg:.4f}" == "7.1111")
Bv = Bg / grow
check("d: B 7.0052", f"{Bv:.4f}" == "7.0052" and f"{Bv:.2f}" == "7.01")
check("d: B shown product 7.1111 x 0.985112", f"{7.1111 * 0.985112:.4f}" == "7.0052")
V_copy = Delta * S0 + Bv
# second route for the copy: solve the 2 by 2 system numerically with numpy if present
try:
    import numpy as np
    xs = np.linalg.solve(np.array([[Su, grow], [Sd, grow]]), np.array([fU, fD]))
    check("d: numpy solve", near(xs[0], Delta, 1e-12) and near(xs[1], Bv, 1e-12))
except ImportError:
    pass
check("d: copy pays 16 and 12.8", near(Delta * Su + Bv * grow, 16, 1e-12) and near(Delta * Sd + Bv * grow, 12.8, 1e-12))
check("d: shown checks", near(80 / 9 + 7.1111, 16, 1e-3) and near(51.2 / 9 + 7.1111, 12.8, 1e-3))
check("d: copy price 14.12", f"{V_copy:.2f}" == "14.12" and f"{64 / 9 + 7.0052:.2f}" == "14.12")
# q route
qq = (grow - dd) / (uu - dd)
check("d: q 0.478029", f"{qq:.6f}" == "0.478029" and f"{1 - qq:.6f}" == "0.521971" and f"{qq:.4f}" == "0.4780")
mix = qq * fU + (1 - qq) * fD
check("d: q mix 14.329693", f"{mix:.6f}" == "14.329693")
check("d: discount 0.985112", f"{1 / grow:.6f}" == "0.985112" and f"{math.exp(-0.015):.6f}" == "0.985112")
V_q = mix / grow
check("d: q price 14.12", f"{V_q:.2f}" == "14.12" and f"{0.985112 * 14.329693:.2f}" == "14.12")
check("d: routes agree", near(V_q, V_copy, 1e-12))
check("d: lends", Bv > 0)
# (e) bounds
lo, hi = fD / grow, fU / grow
check("e: bounds 12.61 and 15.76", f"{lo:.2f}" == "12.61" and f"{hi:.2f}" == "15.76" and lo < V_q < hi)

# ---------- the item and its rubric ----------
hw = json.load(open(HW, encoding="utf-8"))
items = hw["items"]
idx = [i for i, it in enumerate(items) if it["id"] == "h-derive-one-step"]
check("item present once", len(idx) == 1)
it = items[idx[0]]
check("item last", idx[0] == len(items) - 1)
check("kind", it.get("performance") == "derivation" and it.get("kind") == "longform")
for bad in ("starter", "steps", "order", "derive", "hints", "parts"):
    check("no " + bad, bad not in it)
rub = it["rubric"]
pts = [row["points"] for row in rub]
check("rubric 3 to 5 rows", 3 <= len(rub) <= 5)
check("rubric sums to 10", sum(pts) == 10)
req = [bool(row.get("required")) for row in rub]
check("not every row required", not all(req))
# every passing tick set holds every required row (named parts a to d), row 5 is (e), optional
passing = []
for ticks in itertools.product([0, 1], repeat=len(rub)):
    total = sum(p for p, t in zip(pts, ticks) if t)
    if total >= 7 and all(t for t, rq in zip(ticks, req) if rq):
        passing.append(ticks)
print("passing tick sets:", passing)
check("two passing sets", passing == [(1, 1, 1, 1, 0), (1, 1, 1, 1, 1)])
for part, row in (("a", 0), ("b", 1), ("c", 2), ("d", 3)):
    check("part %s in every pass" % part, all(t[row] for t in passing) and rub[row]["text"].startswith("(" + part + ")"))
check("optional part marked in prompt", "(e) Optional, one more point" in it["prompt"])
# stated numbers in model and rubric
for s in ("1.015113", "0.1111", "7.1111", "7.0052", "£7.01", "14.12", "0.478029", "0.521971", "14.329693", "0.985112", "12.61", "15.76", "51.2", "12.8"):
    check("model states " + s, s in it["model"])
for s in ("7.0052", "£7.01", "14.12", "0.4780"):
    check("rubric states " + s, any(s in row["text"] for row in rub))
# homework limits
check("6 to 12 items", 6 <= len(items) <= 12)
check("a difficulty 5", any(x.get("difficulty") == 5 for x in items))
check("difficulties 3 to 5", all(3 <= x.get("difficulty", 0) <= 5 for x in items))
check("one performance task", sum(1 for x in items if "performance" in x) == 1)

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
