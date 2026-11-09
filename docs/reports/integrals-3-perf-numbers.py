"""integrals L3 performance task h-derive-parts-tail: every stated number and step, computed twice.

Run from the repository root with the venv that has sympy and scipy:
    <venv>/bin/python -I docs/reports/integrals-3-perf-numbers.py
Route 1 is symbolic (sympy); route 2 is numeric (scipy quad, finite differences, grids).
"""
import itertools
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

import sympy as sp  # noqa: E402
from scipy.integrate import quad  # noqa: E402

lv = Level("integrals", 3)
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'integrals', 'homework-3.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-derive-parts-tail']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"

x, s, t = sp.symbols('x s t', positive=True)
b, B = sp.symbols('b B', positive=True)

# (a) the parts formula, symbolically for general u, v, and numerically on concrete pairs
u, v = sp.Function('u'), sp.Function('v')
lv.claim(sp.simplify(sp.diff(u(x) * v(x), x) - (sp.diff(u(x), x) * v(x) + u(x) * sp.diff(v(x), x))) == 0, "product rule")
pairs = [(sp.log(x), -1 / (2 * x ** 2)), (x ** 2, sp.sin(x)), (sp.exp(x), sp.cos(3 * x)), (sp.sqrt(x), sp.log(x + 1))]
ok = True
for uu, vv in pairs:
    lhs = quad(sp.lambdify(x, uu * sp.diff(vv, x)), 1, 4)[0]
    rhs = float((uu * vv).subs(x, 4) - (uu * vv).subs(x, 1)) - quad(sp.lambdify(x, sp.diff(uu, x) * vv), 1, 4)[0]
    ok = ok and abs(lhs - rhs) < 1e-9
lv.claim(ok, "parts formula holds numerically on [1, 4] for four pairs")

# (b) the split
U, V = sp.log(x), -1 / (2 * x ** 2)
lv.claim(sp.diff(U, x) == 1 / x and sp.simplify(sp.diff(V, x) - x ** -3) == 0, "u' = 1/x and v' = x^-3")
lv.claim(sp.simplify(-sp.diff(U, x) * V - 1 / (2 * x ** 3)) == 0, "-u'v = +1/(2x^3)")
F_b = sp.Rational(1, 4) - 1 / (4 * b ** 2) - sp.log(b) / (2 * b ** 2)
lv.claim(sp.simplify(sp.integrate(sp.log(x) / x ** 3, (x, 1, b)) - F_b) == 0, "sympy: int_1^b = 1/4 - 1/(4b^2) - ln b/(2b^2)")
bracket = (U * V).subs(x, b) - (U * V).subs(x, 1)
lv.claim(sp.simplify(bracket + sp.log(b) / (2 * b ** 2)) == 0 and (U * V).subs(x, 1) == 0, "bracket = -ln b/(2b^2), 0 at x = 1")
lv.claim(sp.simplify(sp.integrate(1 / (2 * x ** 3), (x, 1, b)) - (sp.Rational(1, 4) - 1 / (4 * b ** 2))) == 0, "int_1^b 1/(2x^3) = 1/4 - 1/(4b^2)")
lv.claim(sp.simplify(sp.diff(F_b, b) - sp.log(b) / b ** 3) == 0, "differentiating the closed form gives the integrand")
ok = all(abs(quad(lambda y: math.log(y) / y ** 3, 1, bb)[0] - float(F_b.subs(b, bb))) < 1e-11 for bb in (1.5, 2, 5, 10, 100, 1e4))
lv.claim(ok, "quad on [1, b] matches the closed form at six b")
# the limits
lv.claim(sp.limit(sp.log(b) / (2 * b ** 2), b, sp.oo) == 0 and sp.limit(F_b, b, sp.oo) == sp.Rational(1, 4), "sympy: ln b/(2b^2) -> 0 and the limit is 1/4")
lv.claim(sp.integrate(sp.log(x) / x ** 3, (x, 1, sp.oo)) == sp.Rational(1, 4), "sympy: the improper integral is 1/4")
val, err = quad(lambda y: math.log(y) / y ** 3, 1, math.inf)
lv.claim(abs(val - 0.25) < 1e-10, f"scipy quad on [1, inf) gives {val:.12f}")
grid = [1 + j * 0.01 for j in range(0, 100001)]
lv.claim(all(0 <= math.log(y) <= y - 1 < y for y in grid), "0 <= ln b <= b - 1 < b on [1, 1001]")
lv.claim(all(abs(quad(lambda q: 1 / q, 1, y)[0] - math.log(y)) < 1e-10 for y in (2, 7.5, 40)), "ln b = int_1^b dt/t")
lv.claim(all(0 <= math.log(y) / (2 * y * y) < 1 / (2 * y) for y in grid[1:]), "0 <= ln b/(2b^2) < 1/(2b)")
# the other route
sub = (sp.log(x) / x ** 3).subs(x, sp.exp(s)) * sp.diff(sp.exp(s), s)
lv.claim(sp.simplify(sub - s * sp.exp(-2 * s)) == 0, "x = e^s turns the integrand into s e^{-2s}")
G_B = sp.Rational(1, 4) - sp.exp(-2 * B) / 4 - B * sp.exp(-2 * B) / 2
lv.claim(sp.simplify(sp.integrate(s * sp.exp(-2 * s), (s, 0, B)) - G_B) == 0, "int_0^B s e^{-2s} = 1/4 - e^{-2B}/4 - B e^{-2B}/2")
lv.claim(sp.simplify(G_B.subs(B, sp.log(b)) - F_b) == 0, "same expression with B = ln b")
ok = all(abs(quad(lambda q: q * math.exp(-2 * q), 0, BB)[0] - float(G_B.subs(B, BB))) < 1e-11 for BB in (0.5, 1, 3, 9))
lv.claim(ok, "quad on [0, B] matches the substituted closed form")
lv.claim(all(math.exp(2 * y) > 2 * y * y and y * math.exp(-2 * y) < 1 / (2 * y) for y in [j * 0.01 for j in range(1, 5000)]), "e^{2B} > 2B^2 and B e^{-2B} < 1/(2B)")
# the check
lv.claim(all(math.log(y) < y for y in grid) and abs(quad(lambda y: y ** -2, 1, math.inf)[0] - 1) < 1e-10 and 0 < 0.25 < 1, "ln x < x, int 1/x^2 = 1, and 0 < 1/4 < 1")

for vv in [r"\frac14 - \frac{1}{4b^2} - \frac{\ln b}{2b^2}", r"\frac14 - \frac{e^{-2B}}{4} - \frac{B\,e^{-2B}}{2}", r"e^{2B} > 2B^2",
           r"B\,e^{-2B} < \tfrac{1}{2B}", r"0 \le \tfrac{\ln b}{2b^2} < \tfrac{1}{2b}", r"b - 1 < b", r"v = -\tfrac{1}{2x^2}"]:
    lv.expect("homework", M, vv)
lv.claim(r"= \frac14.$$" in it['model'], "the stated value 1/4")

# rubric
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, False, True, True, True], "rows 1, 3, 4, 5 required, row 2 optional")
named = {0: 'a', 2: 'b-finite', 3: 'b-limit', 4: 'b-value'}
passes = [c for r in range(1, len(rub) + 1) for c in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in c) >= 7 and all(i in c for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in c) for c in passes])
lv.claim(passes == [(0, 2, 3, 4), (0, 1, 2, 3, 4)], "the only passes are rows 1, 3, 4, 5 and all five")
lv.claim(all(set(named.values()) <= {named[i] for i in c if i in named} for c in passes), "every pass covers (a) and the finite range, limit and value of (b)")
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(key in it for key in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for y in items if y.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(y['difficulty'] == 5 for y in items), "homework limits")
blob = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in blob and '—' not in blob and '–' not in blob, "no ! or dashes")

lv.check_wrongs()
lv.report()
