"""taylor L2 performance task h2-prove-perpetuity-series: every stated number, computed twice.

Run from the repository root with the venv that has sympy, numpy and mpmath:
    <venv>/bin/python -I docs/reports/taylor-2-perf-numbers.py
Route 1: sympy (diff, series, exact rationals). Route 2: exact Fraction repricing and float finite differences and sums.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("taylor", 2)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'taylor', 'homework-2.json')
hw = json.load(open(HW, encoding='utf-8'))
items = hw['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h2-prove-perpetuity-series']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"
R = f"items[{I}].rubric"

y, h, k = sp.symbols('y h k', positive=True)
P = 5 / y
y0 = sp.Rational(1, 20)

# ---------- (a) the derivative pattern and the series ----------
ok = all(sp.simplify(sp.diff(P, y, n) - (-1) ** n * sp.factorial(n) * 5 * y ** (-(n + 1))) == 0 for n in range(0, 13))
lv.claim(ok, "sympy diff: P^(k)(y) = (-1)^k k! 5 y^-(k+1) for k = 0..12")
kk = sp.Symbol('kk', integer=True, nonnegative=True)
claim_k = (-1) ** kk * sp.factorial(kk) * 5 * y ** (-(kk + 1))
step = sp.simplify(sp.diff(claim_k, y) - (-1) ** (kk + 1) * sp.factorial(kk + 1) * 5 * y ** (-(kk + 2)))
lv.claim(step == 0, "sympy: differentiating the k-th formula gives the (k+1)-th (the induction step)")
f = 5 / (y0 + h)
ser = sp.series(f, h, 0, 8).removeO()
coef = [ser.coeff(h, n) for n in range(8)]
lv.claim(coef == [100 * (-20) ** n for n in range(8)], "sympy series: c_k = 100 (-20)^k for k = 0..7")
lv.claim(all(sp.Rational((-1) ** n * 5) / y0 ** (n + 1) == 100 * (-20) ** n for n in range(12)), "(-1)^k 5 / y0^(k+1) = 100 (-20)^k")
lv.claim(coef[:3] == [100, -2000, 40000], "100 - 2000h + 40,000h^2")
lv.claim(sp.simplify(f - 100 / (1 + 20 * h)) == 0, "5/(0.05 + h) = 100/(1 + 20h)")
# route 2: Maclaurin coefficients by float finite differences of P at 0.05
hh = 1e-4
P_ = lambda t: 5 / t
d1 = (P_(0.05 + hh) - P_(0.05 - hh)) / (2 * hh)
d2 = (P_(0.05 + hh) - 2 * P_(0.05) + P_(0.05 - hh)) / hh ** 2
lv.claim(abs(d1 + 2000) < 1e-2 and abs(d2 - 80000) < 1, f"finite differences: P' = {d1:.3f}, P'' = {d2:.1f}")

# ---------- (b) duration and convexity ----------
D = -sp.diff(P, y).subs(y, y0) / P.subs(y, y0)
C = sp.diff(P, y, 2).subs(y, y0) / P.subs(y, y0)
lv.claim(D == 20 and C == 800, "sympy: D = 20, C = 800")
lv.claim(-F(coef[1]) / coef[0] == 20 and 2 * F(coef[2]) / coef[0] == 800 and 2 * coef[2] == 80000, "from the coefficients: D = -c1/c0 = 20, C = 2c2/c0 = 800, P'' = 80,000")
lv.claim(abs(-d1 / 100 - 20) < 1e-4 and abs(d2 / 100 - 800) < 1e-2, "finite differences give D and C too")
lv.claim(D == 1 / y0 and C == 2 / y0 ** 2, "D = 1/y0, C = 2/y0^2")

# ---------- (c) the exact error of the second-order rule ----------
Q = 100 - D * 100 * h + sp.Rational(1, 2) * C * 100 * h ** 2
lv.claim(sp.expand(Q - (coef[0] + coef[1] * h + coef[2] * h ** 2)) == 0, "the rule is the series cut after h^2 (-DP = c1, CP/2 = c2)")
u = sp.Symbol('u')
lv.claim(sp.expand((1 - u + u ** 2) * (1 + u)) == 1 + u ** 3, "(1 - u + u^2)(1 + u) = 1 + u^3")
err = sp.simplify(f - Q)
lv.claim(sp.simplify(err - (-800000 * h ** 3 / (1 + 20 * h))) == 0, "sympy: error = -800,000 h^3 / (1 + 20h)")
lv.claim(sp.simplify((-100 * u ** 3 / (1 + u)).subs(u, 20 * h) - err) == 0, "= -100u^3/(1 + u) with u = 20h")
lv.claim(sp.limit(err / h ** 3, h, 0) == -800000, "error / h^3 tends to -800,000: it shrinks like h^3")
lv.claim(sp.series(f, h, 0, 4).removeO().coeff(h, 3) == -800000, "the first dropped term is -800,000 h^3")
e_small = [float(err.subs(h, sp.Rational(1, 100) / 2 ** j)) for j in range(6)]
e_neg = [float(err.subs(h, -sp.Rational(1, 100) / 2 ** j)) for j in range(6)]
lv.claim(all(7.5 < e[j] / e[j + 1] < 8.5 for e in (e_small, e_neg) for j in range(1, 5)), "for small moves (0.5% and below) halving the move cuts the error about eightfold")

# ---------- (d) a 1% move, two routes ----------
for hv, rule, true, e in [(F(1, 100), 84, F(250, 3), F(-2, 3)), (F(-1, 100), 124, 125, F(1))]:
    uq = 20 * hv
    lv.claim(100 * (1 - uq + uq ** 2) == rule and F(5) / (F(1, 20) + hv) == true, f"h = {hv}: rule {rule}, true {float(true):.2f} (Fraction)")
    lv.claim(abs(float(Q.subs(h, sp.Rational(hv.numerator, hv.denominator))) - rule) < 1e-12 and abs(5 / (0.05 + float(hv)) - float(true)) < 1e-12, f"h = {hv}: sympy rule and float repricing agree")
    lv.claim(true - rule == e and -100 * uq ** 3 / (1 + uq) == e, f"h = {hv}: error {float(e):.4f} by repricing and by the closed form")
    lv.claim(round(abs(float(-100 * uq ** 3)), 2) == 0.80, "dropped cubic term 80p in size")
    lv.claim((e > 0) == (hv < 0), "error has the opposite sign to h")
lv.claim(round(5 / 0.06, 2) == 83.33 and round(-0.8 / 1.2, 2) == -0.67 and 0.8 / 0.8 == 1, "printed 83.33, -0.67, 1")
lv.claim(100 * 0.84 == 84 and round(100 * 1.24, 9) == 124 and 5 / 0.04 == 125, "printed 84, 124, 125")
lv.claim(1 - 0.2 + 0.04 == 0.84 or abs((1 - 0.2 + 0.04) - 0.84) < 1e-12, "1 - u + u^2 = 0.84 at u = 0.2")
lv.claim(abs((1 + 0.2 + 0.04) - 1.24) < 1e-12, "1 - u + u^2 = 1.24 at u = -0.2")

# ---------- optional: where the series works ----------
partial = lambda hv, n: sum(100 * (-20 * hv) ** j for j in range(n))
lv.claim(abs(partial(0.049, 4000) - 5 / 0.099) < 1e-6 and abs(partial(-0.049, 4000) - 5 / 0.001) < 1e-3, "series sums to the price at h = +-0.049")
lv.claim(abs(partial(0.06, 200)) > 1e10, "at h = 0.06 (yield 11%) the partial sums blow up")
lv.claim(round(5 / 0.11, 2) == 45.45, "5/0.11 = 45.45")
lv.claim(sp.limit(sp.Abs(coef[1] / coef[0]) ** -1, h, 0) == sp.Rational(1, 20), "radius 1/20 = 0.05 from the ratio of coefficients")

# ---------- printed numbers appear in the text ----------
for v in [100, 2000, 40000, 80000, 20, 800, -800000, 0.84, 84, 83.33, -0.67, 67, 1.24, 124, 125, 0.05, 10, 11, 45.45, 0.2, -0.2]:
    lv.expect("homework", M, v)
for v in [84.00, 83.33, 67, 124.00, 125.00, 1.00]:
    lv.expect("homework", f"{R}[3].text", v)
lv.expect("homework", f"{R}[1].text", 20)
lv.expect("homework", f"{R}[1].text", 800)
lv.expect("homework", f"{R}[4].text", 0.05)
lv.expect("homework", f"items[{I}].prompt", 0.05)
lv.expect("homework", f"items[{I}].prompt", 100)

# ---------- rubric ----------
rub = it['rubric']
pts = [q['points'] for q in rub]
req = [bool(q.get('required')) for q in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 (the optional part) not")
parts = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'opt'}
passes = [s for n in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), n)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({'a', 'b', 'c', 'd'} <= {parts[i] for i in s} for s in passes), "every pass covers (a), (b), (c) and (d)")
lv.claim('Optional, one more point:' in it['prompt'], "the optional part is marked in the prompt")

# ---------- shape and homework limits ----------
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(q in it for q in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for q in items if q.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(q.get('difficulty') == 5 for q in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
import re
s = re.sub(r'\$\$.*?\$\$|\$[^$]*\$', '', s, flags=re.S)
lv.claim('!' not in s and '—' not in s and '–' not in s and '$' not in it['title'], "no ! or dashes; no $ in the title")
lv.claim(math.isclose(sum(pts), 10), "points total 10")

lv.check_wrongs("homework")
lv.report()
