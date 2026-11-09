"""taylor L1 performance task h-prove-newton-error: every stated number, computed twice.

Run from the repository root with the venv that has sympy, numpy and mpmath:
    <venv>/bin/python -I docs/reports/taylor-1-perf-numbers.py
Route 1: sympy (exact symbols, series and limits). Route 2: mpmath at 40 digits and plain floats, plus grid checks.
"""
import itertools
import json
import math
import os
import sys

import mpmath as mp
import numpy as np
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("taylor", 1)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'taylor', 'homework-1.json')
hw = json.load(open(HW, encoding='utf-8'))
items = hw['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-newton-error']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"
R = f"items[{I}].rubric"

# ---------- (a) and (b): the update and the exact error identity, symbolically ----------
x, xn, r, h, c = sp.symbols('x x_n r h c', real=True)
f = sp.Function('f')
tangent = sp.series(sp.exp(x), x, xn, 2).removeO()                     # order-1 Taylor polynomial of e^x about x_n
lv.claim(sp.simplify(tangent - (sp.exp(xn) + sp.exp(xn) * (x - xn))) == 0, "sympy series: the tangent of e^x at x_n is f(x_n) + f'(x_n)(x - x_n)")
F_, dF = sp.symbols('F dF', nonzero=True)                                # f(x_n) and f'(x_n)
zero = sp.solve(sp.Eq(F_ + dF * (x - xn), 0), x)
lv.claim(len(zero) == 1 and sp.simplify(zero[0] - (xn - F_ / dF)) == 0, "the tangent meets the axis at x_n - f(x_n)/f'(x_n)")
# identity: with f(r) = 0 and R := f(r) - f(x_n) - f'(x_n)(r - x_n), e_{n+1} = R / f'(x_n)
Rem = sp.Symbol('Rem')
Fr = F_ + dF * (r - xn) + Rem                                            # exact form: f(r) = f(x_n) + f'(x_n)(r - x_n) + Rem
F_solved = sp.solve(sp.Eq(Fr, 0), F_)[0]                                 # use f(r) = 0
e_next = (xn - F_solved / dF) - r
lv.claim(sp.simplify(e_next - Rem / dF) == 0, "with f(r) = 0, e_{n+1} = Rem / f'(x_n); Rem = f''(c) e_n^2 / 2 gives the claim")

# numerical check of (b) for e^x - 3: solve for c in the exact tangent error and compare
mp.mp.dps = 40
rt = mp.log(3)
fx = lambda t: mp.e ** t - 3
step = lambda t: t - 1 + 3 * mp.e ** (-t)
ok_b = True
for x0 in [mp.mpf(v) for v in ('0.5', '1', '1.05', '1.15', '1.2', '2')]:
    en = x0 - rt
    rem = fx(rt) - fx(x0) - mp.e ** x0 * (rt - x0)                     # = f''(c)/2 * e_n^2
    cc = mp.log(2 * rem / en ** 2)                                       # f''(c) = e^c
    ok_b &= min(x0, rt) < cc < max(x0, rt)
    ok_b &= abs((step(x0) - rt) - mp.e ** cc / (2 * mp.e ** x0) * en ** 2) < mp.mpf(10) ** -35
lv.claim(ok_b, "e^x - 3: c from the exact tangent error lies between x_n and r, and e_{n+1} = f''(c) e_n^2 / (2 f'(x_n)), six starts")

# ---------- (c) the bound on [1, 1.2] and the sign ----------
K_sym = sp.exp(sp.Rational(6, 5)) / (2 * sp.E)
lv.claim(sp.simplify(K_sym - sp.exp(sp.Rational(1, 5)) / 2) == 0, "e^1.2 / (2e) = e^0.2 / 2 exactly")
K = float(mp.e ** mp.mpf('0.2') / 2)
lv.claim(abs(K - math.exp(0.2) / 2) < 1e-15 and round(K, 3) == 0.611, "K = 0.611 (mpmath and math)")
lv.claim(1 <= float(rt) <= 1.2 and round(float(rt), 4) == 1.0986, "ln 3 = 1.0986 lies in [1, 1.2]")
grid = np.linspace(1, 1.2, 2001)
en_g = grid - math.log(3)
en1_g = grid - 1 + 3 * np.exp(-grid) - math.log(3)
lv.claim(np.all(np.abs(en1_g) <= K * en_g ** 2 + 1e-15), "grid on [1, 1.2]: |e_{n+1}| <= 0.611 e_n^2")
lv.claim(np.all(en1_g >= -1e-15), "grid on [1, 1.2]: e_{n+1} >= 0")
wide = np.linspace(-3, 5, 4001)
lv.claim(np.all(wide - 1 + 3 * np.exp(-wide) - math.log(3) >= -1e-12), "from any start in [-3, 5] the next guess is at or above ln 3")

# ---------- (d) the check from x0 = 1, both routes ----------
xs = [mp.mpf(1)]
for _ in range(4):
    xs.append(step(xs[-1]))
es = [v - rt for v in xs]
x1_sym = sp.Integer(1) - (sp.E - 3) / sp.E
lv.claim(sp.simplify(x1_sym - 3 / sp.E) == 0, "sympy: x_1 = 3/e exactly")
xf = [1.0]
for _ in range(2):
    xf.append(xf[-1] - (math.exp(xf[-1]) - 3) / math.exp(xf[-1]))
lv.claim(abs(xf[1] - float(xs[1])) < 1e-15 and abs(xf[2] - float(xs[2])) < 1e-14, "float Newton agrees with mpmath for x_1, x_2")
lv.claim(round(float(xs[1]), 6) == 1.103638 and round(float(xs[1]), 4) == 1.1036, "x_1 = 1.103638")
lv.claim(round(float(es[1]), 6) == 0.005026 and round(float(es[1]), 4) == 0.0050, "e_1 = 0.005026")
lv.claim(round(float(es[0]), 6) == -0.098612, "e_0 = -0.098612")
lv.claim(round(float(es[0] ** 2), 6) == 0.009724, "e_0^2 = 0.009724")
lv.claim(round(0.611 * 0.009724, 5) == 0.00594 and round(K * float(es[0] ** 2), 5) == 0.00594, "bound 0.611 x 0.009724 = 0.00594 (printed and unrounded)")
lv.claim(0 < es[1] < K * es[0] ** 2, "0 < e_1 < bound")
lv.claim(round(float(xs[2]), 7) == 1.0986249 and round(float(xs[2]), 5) == 1.09862, "x_2 = 1.0986249")
lv.claim(round(float(es[2]) * 1e5, 2) == 1.26 and round(float(es[2]) * 1e5, 1) == 1.3, "e_2 = 1.26e-5")
lv.claim(round(0.611 * 0.005026 ** 2 * 1e5, 2) == 1.54 and round(K * float(es[1]) ** 2 * 1e5, 2) == 1.54, "bound 0.611 e_1^2 = 1.54e-5")
lv.claim(round(K * float(es[1]) ** 2 * 1e5, 1) == 1.5 and round(K * float(es[0]) ** 2, 4) == 0.0059, "rubric rounding 1.5e-5 and 0.0059")
lv.claim(0 < es[2] < K * es[1] ** 2, "0 < e_2 < bound")
lv.claim(round(abs(float(es[0])), 3) == 0.099 and round(float(es[1]), 3) == 0.005 and round(float(es[2]), 6) == 0.000013, "errors 0.099, 0.005, 0.000013")
ratios = [es[k + 1] / es[k] ** 2 for k in range(3)]
lv.claim(abs(ratios[-1] - mp.mpf("0.5")) < 1e-5 and abs(ratios[-1] - 0.5) < abs(ratios[0] - 0.5), f"e_{{n+1}}/e_n^2 tends to 1/2 numerically ({mp.nstr(ratios[-1], 12)})")
lim = sp.limit((x - 1 + 3 * sp.exp(-x) - sp.log(3)) / (x - sp.log(3)) ** 2, x, sp.log(3))
lv.claim(lim == sp.Rational(1, 2), "sympy limit: f''(r)/(2f'(r)) = 1/2")
ser = sp.series((sp.log(3) + h) - 1 + 3 * sp.exp(-(sp.log(3) + h)) - sp.log(3), h, 0, 3).removeO()
lv.claim(sp.simplify(ser - h ** 2 / 2) == 0, "sympy series: the step error map is h^2/2 + O(h^3) about ln 3")

# optional part: [ln 3, 1.2] is kept
top = 1.2 - float(rt)
lv.claim(round(top, 3) == 0.101 and round(0.611 * 0.101, 3) == 0.062 and round(K * top, 3) == 0.062, "1.2 - ln 3 = 0.101, 0.611 x 0.101 = 0.062")
g2 = np.linspace(math.log(3), 1.2, 2001)
nx = g2 - 1 + 3 * np.exp(-g2)
lv.claim(np.all(nx >= math.log(3) - 1e-15) and np.all(nx <= g2 + 1e-15), "grid: x_n in [ln 3, 1.2] gives ln 3 <= x_{n+1} <= x_n")
lv.claim(all(rt <= v <= 1.2 for v in xs[1:]), "x_1 .. x_4 all in [ln 3, 1.2]")

# ---------- printed numbers appear in the text ----------
for v in [1.0986, 0.611, 1.103638, 0.005026, -0.098612, 0.009724, 0.00594, 1.0986249, 1.26, 1.54, 0.099, 0.005, 0.000013, 0.101, 0.062, 1.1036]:
    lv.expect("homework", M, v)
lv.expect("homework", f"{R}[2].text", 0.611)
for v in [1.1036, 1.09862, 0.0050, 1.3, 0.0059, 1.5]:
    lv.expect("homework", f"{R}[3].text", v)
lv.expect("homework", f"{R}[4].text", 0.611)
lv.expect("homework", f"items[{I}].prompt", 1.2)

# ---------- rubric: sums to 10, required rows as designed, no pass skips a named part ----------
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
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for q in items if q.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(q.get('difficulty') == 5 for q in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s and '$' not in it['title'], "no ! or dashes; no $ in the title")

lv.check_wrongs("homework")
lv.report()
