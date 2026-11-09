"""limits L4 performance task h-build-cable-route: every stated number, computed twice.

Run from the repository root with the venv that has sympy and numpy:
    <venv>/bin/python -I docs/reports/limits-4-perf-numbers.py
Routes: sympy (derivative, exact solve, limits and exact values; route 1) against a dense numerical table of the cost
and a brute-force search over landing points, including landings outside the range (route 2).
The rubric's passing tick sets are listed and checked.
"""
import itertools
import json
import math
import os
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("limits", 4)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'limits', 'homework-4.json')
hw = json.load(open(HW, encoding='utf-8'))
items = hw['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-build-cable-route']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"

x, d = sp.symbols('x d', real=True)
W, UW, LAND = 3, 500, 300                        # river width km, £ thousand per km under water and along the bank
C = UW * sp.sqrt(W ** 2 + x ** 2) + LAND * (d - x)
Cp = sp.diff(C, x)


def cost(t, dd):
    """Route 2: the cost of landing at t (any real), in £ thousand, from the geometry alone."""
    return UW * math.hypot(W, t) + LAND * abs(dd - t)


# (a) the build: the formula equals the geometric cost on the range, and landings outside cost more than the ends
xs = np.linspace(0, 8, 8001)
lv.claim(all(abs(float(C.subs({d: 8, x: float(t)})) - cost(float(t), 8)) < 1e-9 for t in xs[::400]), "C(x) matches the geometry on 0..8")
lv.claim(all(cost(t, 8) > cost(0, 8) for t in np.linspace(-20, -1e-3, 500)) and all(cost(t, 8) > cost(8, 8) for t in np.linspace(8.001, 30, 500)),
         "upstream of O costs more than O; past B costs more than B")
lv.claim(cost(8, 8) == 500 * math.sqrt(73), "water run to B is sqrt(73)")

# (b) route 1: derivative, exact solve, type
lv.claim(sp.simplify(Cp - (500 * x / sp.sqrt(9 + x ** 2) - 300)) == 0, "C'(x) = 500x/sqrt(9+x^2) - 300, independent of d")
lv.claim(sp.simplify(sp.diff(sp.sqrt(9 + x ** 2), x) - x / sp.sqrt(9 + x ** 2)) == 0, "chain rule: d/dx sqrt(9+x^2) = x/sqrt(9+x^2)")
sols = sp.solve(sp.Eq(Cp, 0), x)
lv.claim(sols == [sp.Rational(9, 4)], f"sympy: the only real zero of C' is 9/4 (got {sols})")
lv.claim(sp.solve(sp.Eq(25 * x ** 2, 81 + 9 * x ** 2), x) == [-sp.Rational(9, 4), sp.Rational(9, 4)] and
         sp.simplify((5 * x - 3 * sp.sqrt(9 + x ** 2)).subs(x, -sp.Rational(9, 4))) != 0,
         "squared equation 16x^2 = 81 has +-9/4; -9/4 fails the unsquared one")
lv.claim(sp.Rational(81, 16) == sp.Rational(9, 4) ** 2 and float(sp.Rational(9, 4)) == 2.25, "x = 9/4 = 2.25")
C2 = sp.diff(C, x, 2)
lv.claim(sp.simplify(C2 - 4500 / (9 + x ** 2) ** sp.Rational(3, 2)) == 0, "C''(x) = 4500/(9+x^2)^(3/2) > 0")
# sign of C' equals sign of 16x^2 - 81 for x >= 0: exact on a rational grid and in floats on a fine grid
grid = [sp.Rational(k, 40) for k in range(0, 321)]
lv.claim(all(sp.sign(Cp.subs(x, t)) == sp.sign(16 * t ** 2 - 81) for t in grid), "sign C' = sign(16x^2 - 81), exact grid 0..8")
cp_num = 500 * xs / np.sqrt(9 + xs ** 2) - 300
lv.claim(np.all(cp_num[xs < 2.25 - 1e-9] < 0) and np.all(cp_num[xs > 2.25 + 1e-9] > 0), "numerical table: C' < 0 before 2.25, > 0 after")
# route 2: brute force over landing points
cs = np.array([cost(t, 8) for t in xs])
lv.claim(abs(xs[cs.argmin()] - 2.25) < 1e-3 and abs(cs.min() - 3600) < 1e-6, f"brute force: min at {xs[cs.argmin()]:.3f}, cost {cs.min():.4f}")
lv.claim(sp.sqrt(9 + sp.Rational(81, 16)) == sp.Rational(15, 4) and 9 + 2.25 ** 2 == 14.0625 and math.sqrt(14.0625) == 3.75, "water run 3.75 km")
lv.claim(8 - 2.25 == 5.75 and 500 * 3.75 == 1875 and 300 * 5.75 == 1725 and 1875 + 1725 == 3600, "C(2.25) = 1,875 + 1,725 = 3,600")
lv.claim(sp.simplify(C.subs({d: 8, x: sp.Rational(9, 4)})) == 3600, "sympy C(9/4) = 3600 exactly")
lv.claim(C.subs({d: 8, x: 0}) == 3900 and 1500 + 2400 == 3900, "C(0) = 3,900")
lv.claim(round(float(C.subs({d: 8, x: 8})), 0) == 4272 and round(cost(8, 8)) == 4272, "C(8) = 500 sqrt 73 = 4,272")
lv.claim(sp.limit(Cp, x, sp.oo) == 200, "far out C' -> 500 - 300 = 200 > 0 (no other turn)")

# (c) d = 2: end point
lv.claim(9 / 4 > 2 and 16 * 2 ** 2 - 81 == -17 and 64 - 81 < 0, "2.25 outside 0..2; 16x^2 - 81 <= -17 there")
xs2 = np.linspace(0, 2, 2001)
cs2 = np.array([cost(t, 2) for t in xs2])
lv.claim(np.all(np.diff(cs2) < 0), "numerical table: C falls across 0..2")
lv.claim(abs(cs2.min() - 500 * math.sqrt(13)) < 1e-9 and xs2[cs2.argmin()] == 2.0, "brute force: best at x = 2")
lv.claim(round(500 * math.sqrt(13), 1) == 1802.8 and round(float(sp.N(500 * sp.sqrt(13))) * 1000, -3) == 1803000, "500 sqrt 13 = 1,802.8 thousand, £1,803,000")
lv.claim(cost(0, 2) == 2100 and 1500 + 600 == 2100, "other end £2,100,000")
tt = np.linspace(-10, 10, 20001)
lv.claim(min(cost(t, 2) for t in tt) >= 500 * math.sqrt(13) - 1e-9, "no landing anywhere beats straight to B'")

# optional: lands short exactly when d > 2.25
ok = True
for dd in np.linspace(0.25, 12, 48):
    g = np.linspace(0, dd, 4001)
    best = g[np.argmin([cost(t, dd) for t in g])]
    ok &= (abs(best - 2.25) < 3e-3) if dd > 2.25 else (abs(best - dd) < 1e-12)
lv.claim(ok, "for d in 0.25..12: best landing 2.25 if d > 2.25, else d (straight)")
lv.claim(sp.diff(Cp, d) == 0, "C' does not depend on d")

for v in [3, 8, 2.25, 3.75, 5.75, 1500, 2400, 3900, 4272, 1875, 1725, 3600, 3600000, 1802.8, 1803000, 2100, 2100000, 9, 81, 16, 25, 5.0625, 64, r'\sqrt{73}', r'\sqrt{13}', r'\sqrt{14.0625}']:
    lv.expect("homework", M, v)
for v, r in [(3900, 2), (4272, 2), (3600000, 2), (2.25, 1), (2.25, 3), (1803000, 3), (2100000, 3), (2.25, 4), (8, 0)]:
    lv.expect("homework", f"items[{I}].rubric[{r}].text", v)
for v in [3, 8, 500000, 300000, 2, 1000]:
    lv.expect("homework", f"items[{I}].prompt", v)

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 (the optional part) not")
parts = {0: 'a', 1: 'b-stationary', 2: 'b-type-ends', 3: 'c', 4: 'optional'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({'a', 'b-stationary', 'b-type-ends', 'c'} <= {parts[i] for i in s} for s in passes), "every pass covers (a), both halves of (b), and (c)")
lv.claim('Optional, one more point:' in it['prompt'], "the optional row's part is marked optional in the prompt")

# shape and homework limits
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for y in items if y.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(y.get('difficulty') == 5 for y in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")
lv.check_wrongs("homework")
lv.report()
