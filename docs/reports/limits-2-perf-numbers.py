"""limits L2 performance task h-prove-negative-powers: every stated number, computed twice.

Run from the repository root with the venv that has sympy and numpy:
    <venv>/bin/python -I docs/reports/limits-2-perf-numbers.py
Routes: sympy limits of the difference quotient and exact algebra (route 1) against exact rationals (Fraction)
and a numerical table of quotients as h shrinks (route 2). The rubric's passing tick sets are listed and checked.
"""
import itertools
import json
import os
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("limits", 2)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'limits', 'homework-2.json')
hw = json.load(open(HW, encoding='utf-8'))
items = hw['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-negative-powers']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"
x, h = sp.symbols('x h')

# (a) route 1: sympy limit of the quotient of x^n, n = 1..15
lv.claim(all(sp.simplify(sp.limit(((x + h) ** n - x ** n) / h, h, 0) - n * x ** (n - 1)) == 0 for n in range(1, 16)),
         "sympy: lim ((x+h)^n - x^n)/h = n x^(n-1), n = 1..15")
# (a) route 2: the expansion x^n + n x^(n-1) h + h^2 R with R a polynomial (R = 0 for n = 1), by counting brackets
ok = True
for n in range(1, 16):
    e = sp.expand((x + h) ** n)
    R = sp.expand((e - x ** n - n * x ** (n - 1) * h) / h ** 2)
    ok &= R.is_polynomial(x, h) and (n > 1 or R == 0)
    ok &= sp.Poly(e, h).coeff_monomial(h) == n * x ** (n - 1)   # one bracket gives h: n ways
    ok &= sp.expand((e - x ** n) / h - (n * x ** (n - 1) + h * R)) == 0
lv.claim(ok, "(x+h)^n = x^n + n x^(n-1) h + h^2 R, R polynomial, quotient = n x^(n-1) + hR")
# other routes the rubric accepts: factorisation (n terms each -> x^(n-1)) and induction
ok = True
for n in range(1, 16):
    S = sum((x + h) ** (n - 1 - k) * x ** k for k in range(n))
    ok &= sp.expand(h * S - ((x + h) ** n - x ** n)) == 0 and sp.expand(S.subs(h, 0) - n * x ** (n - 1)) == 0
    Q = sp.expand(((x + h) ** n - x ** n) / h)
    ok &= sp.expand(((x + h) ** (n + 1) - x ** (n + 1)) / h - ((x + h) * Q + x ** n)) == 0
lv.claim(ok, "factorisation: h * sum of n terms, each -> x^(n-1); induction step (x+h)Q_n + x^n")

# (b) route 1: sympy limit of the quotient of x^(-n), n = 1..12
lv.claim(all(sp.simplify(sp.limit((1 / (x + h) ** n - 1 / x ** n) / h, h, 0) + n / x ** (n + 1)) == 0 for n in range(1, 13)),
         "sympy: lim (1/(x+h)^n - 1/x^n)/h = -n/x^(n+1), n = 1..12")
# (b) route 2: the model's algebra, line by line, and the value at h = 0
ok = True
for n in range(1, 13):
    q = (1 / (x + h) ** n - 1 / x ** n) / h
    l2 = (x ** n - (x + h) ** n) / (h * x ** n * (x + h) ** n)
    l3 = -((x + h) ** n - x ** n) / h * 1 / (x ** n * (x + h) ** n)
    R = sp.expand((sp.expand((x + h) ** n) - x ** n - n * x ** (n - 1) * h) / h ** 2)
    l4 = -(n * x ** (n - 1) + h * R) / (x ** n * (x + h) ** n)
    ok &= all(sp.simplify(a - q) == 0 for a in (l2, l3, l4))
    ok &= sp.simplify(l4.subs(h, 0) + n * x ** (n - 1) / x ** (2 * n)) == 0
    ok &= sp.simplify(n * x ** (n - 1) / x ** (2 * n) - n / x ** (n + 1)) == 0
lv.claim(ok, "(b) each line equals the quotient; at h = 0 it is -n x^(n-1)/x^(2n) = -n/x^(n+1)")
# x + h has the sign of x when 0 < |h| < |x|
ok = all((xx + hh) * xx > 0 for xx in (F(-3), F(-1, 2), F(1, 3), F(2)) for hh in (xx * F(k, 7) for k in range(-6, 7) if k))
lv.claim(ok, "0 < |h| < |x| gives x + h with the sign of x (exact grid)")
lv.claim(all((1 / x ** n).subs(x, 0) == sp.zoo for n in range(1, 6)), "x = 0 is excluded: g(0) = 1/0^n is undefined")

# (c) the stated numbers, exact rationals and floats
g = lambda t: t ** -4
gp = lambda t: -4 * t ** -5
lv.claim(gp(F(2)) == F(-1, 8) and F(-4, 32) == F(-1, 8) and float(sp.diff(x ** -4, x).subs(x, 2)) == -0.125, "g'(2) = -4/32 = -0.125, exact and sympy")
lv.claim(g(F(2)) == F(1, 16) and 1 / 16 == 0.0625, "g(2) = 1/16 = 0.0625")
lv.claim(round(2.01 ** -4, 6) == 0.061265 and round(float(1 / F(201, 100) ** 4), 6) == 0.061265, "2.01^-4 = 0.061265")
lv.claim(round(1.99 ** -4, 6) == 0.063766 and round(float(1 / F(199, 100) ** 4), 6) == 0.063766, "1.99^-4 = 0.063766")
quot = {}
for hh in (F(1, 100), F(-1, 100), F(1, 1000), F(-1, 1000)):
    exact = (g(2 + hh) - g(F(2))) / hh
    flt = ((2 + float(hh)) ** -4 - 2.0 ** -4) / float(hh)
    lv.claim(abs(float(exact) - flt) < 1e-9, f"quotient at h = {hh}: rational {float(exact):.6f} = float {flt:.6f}")
    quot[hh] = float(exact)
lv.claim(round(quot[F(1, 100)], 4) == -0.1235 and round(quot[F(-1, 100)], 4) == -0.1266, "quotients -0.1235 and -0.1266")
lv.claim(round((0.061265 - 0.0625) / 0.01, 4) == -0.1235 and round((0.063766 - 0.0625) / -0.01, 4) == -0.1266,
         "the printed fractions give the printed quotients")
lv.claim(quot[F(-1, 100)] < -0.125 < quot[F(1, 100)], "-0.125 lies between the two secant slopes")
lv.claim(max(abs(quot[F(1, 100)] + 0.125), abs(quot[F(-1, 100)] + 0.125)) < 0.002, "each within 0.002 of -0.125")
lv.claim(round(quot[F(1, 1000)], 4) == -0.1248 and round(quot[F(-1, 1000)], 4) == -0.1252, "h = +-0.001 give -0.1248 and -0.1252")
lv.claim(abs(quot[F(1, 1000)] + 0.125) < abs(quot[F(1, 100)] + 0.125) and abs(quot[F(-1, 1000)] + 0.125) < abs(quot[F(-1, 100)] + 0.125),
         "closer still at h = +-0.001")
# numerical table: the quotient closes in on -0.125 as h shrinks, from both sides
hs = np.array([10.0 ** -k for k in range(1, 7)])
right = ((2 + hs) ** -4 - 2.0 ** -4) / hs
left = ((2 - hs) ** -4 - 2.0 ** -4) / (-hs)
print("h      right quotient    left quotient")
for a, b, c in zip(hs, right, left):
    print(f"{a:.0e}  {b:.8f}  {c:.8f}")
lv.claim(np.all(np.diff(np.abs(right + 0.125)) < 0) and np.all(np.diff(np.abs(left + 0.125)) < 0) and abs(right[-1] + 0.125) < 1e-5,
         "numerical table: both sides close in on -0.125")
lv.claim(np.all(left < -0.125) and np.all(right > -0.125), "table: left quotients below, right above")
# optional part
lv.claim(gp(F(-2)) == F(1, 8) and (-2) ** 5 == -32 and float(sp.diff(x ** -4, x).subs(x, -2)) == 0.125, "g'(-2) = -4/(-32) = 0.125")
lv.claim(all(g(F(t)) == g(F(-t)) for t in range(1, 20)) and all(gp(F(t)) == -gp(F(-t)) for t in range(1, 20)), "g even, g' odd")

for v in [-0.125, 0.0625, 0.061265, 0.063766, -0.1235, -0.1266, 0.002, -0.1248, -0.1252, 0.125, 4, 32, -32, 2.01, 1.99, 0.01, -0.01]:
    lv.expect("homework", M, v)
for v in [-0.125, -0.1235, -0.1266, 0.01, -0.01]:
    lv.expect("homework", f"items[{I}].rubric[3].text", v)
lv.expect("homework", f"items[{I}].rubric[4].text", 0.125)
for v in [4, 2, 0.01, -0.01, -2]:
    lv.expect("homework", f"items[{I}].prompt", v)

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 (the optional part) not")
parts = {0: 'a', 1: 'a-limit', 2: 'b', 3: 'c', 4: 'c-optional'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({'a', 'a-limit', 'b', 'c'} <= {parts[i] for i in s} for s in passes), "every pass covers (a), its limit, (b) and (c)")
lv.claim('Optional, one more point:' in it['prompt'], "the one optional row's part is marked optional in the prompt")

# shape and homework limits
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for y in items if y.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(y.get('difficulty') == 5 for y in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")
lv.check_wrongs("homework")
lv.report()
