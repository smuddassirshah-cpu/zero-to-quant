"""integrals L2 performance task h-derive-window: every stated number and step, computed twice.

Run from the repository root with the venv that has sympy and scipy:
    <venv>/bin/python -I docs/reports/integrals-2-perf-numbers.py
Route 1 is symbolic (sympy); route 2 is numeric (scipy quad and the normal cdf, finite differences, grids).
"""
import itertools
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

import sympy as sp  # noqa: E402
from scipy.integrate import quad  # noqa: E402
from scipy.optimize import minimize_scalar  # noqa: E402
from scipy.stats import norm  # noqa: E402

lv = Level("integrals", 2)
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'integrals', 'homework-2.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-derive-window']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"

phi = lambda t: math.exp(-t * t / 2) / math.sqrt(2 * math.pi)

# (a) the squeeze bounds m_h <= (A(x+h) - A(x))/h <= M_h, for both signs of h, on several continuous f
random.seed(7)
fs = {'phi': phi, 'cos': math.cos, 'abs': lambda t: abs(t - 0.3), 'cubic': lambda t: t ** 3 - 2 * t}
ok = True
for name, f in fs.items():
    A = lambda x, f=f: quad(f, 0, x, epsabs=1e-13, epsrel=1e-13)[0]
    for _ in range(40):
        x = random.uniform(-2, 2)
        h = random.choice([-1, 1]) * random.uniform(1e-3, 0.5)
        lo, hi = min(x, x + h), max(x, x + h)
        grid = [f(lo + (hi - lo) * j / 2000) for j in range(2001)]
        ratio = (A(x + h) - A(x)) / h
        ok = ok and min(grid) - 1e-9 <= ratio <= max(grid) + 1e-9
    for x in (-1.2, 0.0, 0.7, 1.9):                                     # A'(x) = f(x) by a central difference
        d = (A(x + 1e-5) - A(x - 1e-5)) / 2e-5
        ok = ok and abs(d - f(x)) < 1e-6
lv.claim(ok, "m_h <= ratio <= M_h for both signs of h, and A'(x) = f(x) numerically, on four continuous f")

# sympy: A'(x) = f(x) for phi, and G' = 2 f(2x) - f(x)
t, x = sp.symbols('t x', real=True)
xp = sp.Symbol('x', positive=True)
ph = sp.exp(-t ** 2 / 2) / sp.sqrt(2 * sp.pi)
A_s = sp.integrate(ph, (t, 0, x))                        # an erf expression
lv.claim(sp.simplify(sp.diff(A_s, x) - ph.subs(t, x)) == 0, "sympy: d/dx int_0^x phi = phi(x)")
G_s = sp.integrate(ph, (t, xp, 2 * xp))
Gp_s = sp.diff(G_s, xp)
lv.claim(sp.simplify(Gp_s - (2 * ph.subs(t, 2 * xp) - ph.subs(t, xp))) == 0, "sympy: G'(x) = 2 phi(2x) - phi(x)")
lv.claim(sp.simplify(G_s - (A_s.subs(x, 2 * xp) - A_s.subs(x, xp))) == 0, "sympy: G(x) = A(2x) - A(x)")
fx = sp.Function('f')
lv.claim(sp.simplify(sp.diff(sp.Integral(fx(t), (t, xp, 2 * xp)), xp) - (2 * fx(2 * xp) - fx(xp))) == 0, "sympy: Leibniz rule for a general f")
# the factorisation and phi(2x)
lv.claim(sp.simplify(ph.subs(t, 2 * xp) - sp.exp(-2 * xp ** 2) / sp.sqrt(2 * sp.pi)) == 0, "phi(2x) = e^{-2x^2}/sqrt(2 pi)")
lv.claim(sp.simplify(sp.exp(-2 * xp ** 2) - sp.exp(-xp ** 2 / 2) * sp.exp(-3 * xp ** 2 / 2)) == 0, "e^{-2x^2} = e^{-x^2/2} e^{-3x^2/2}")
fact = sp.exp(-xp ** 2 / 2) / sp.sqrt(2 * sp.pi) * (2 * sp.exp(-3 * xp ** 2 / 2) - 1)
lv.claim(sp.simplify(Gp_s - fact) == 0, "G' = (1/sqrt(2pi)) e^{-x^2/2} (2 e^{-3x^2/2} - 1)")
# the critical point, two routes
sol = sp.solve(sp.Eq(2 * sp.exp(-3 * xp ** 2 / 2), 1), xp)
xs_sym = sp.sqrt(2 * sp.log(2) / 3)
lv.claim(len(sol) == 1 and sp.simplify(sol[0] - xs_sym) == 0, "sympy: the only x > 0 is sqrt(2 ln 2 / 3)")
xs = float(xs_sym)
Gnum = lambda x: norm.cdf(2 * x) - norm.cdf(x)
opt = minimize_scalar(lambda x: -Gnum(x), bounds=(0.01, 3), method='bounded', options={'xatol': 1e-10})
lv.claim(abs(opt.x - xs) < 1e-6, f"scipy: maximiser of Phi(2x) - Phi(x) is {opt.x:.6f}")
gq = lambda x: quad(phi, x, 2 * x, epsabs=1e-14)[0]
grid = [j / 10000 for j in range(1, 30001)]
best = max(grid, key=Gnum)
lv.claim(abs(best - xs) < 1e-4 and abs(gq(xs) - Gnum(xs)) < 1e-12, "grid argmax agrees, and quad equals the cdf difference")
lv.claim(round(xs, 3) == 0.680 and round(xs, 4) == 0.6798, f"x* = {xs:.6f}: 0.680 to 3 dp, 0.6798 to 4")
lv.claim(round(math.log(2), 4) == 0.6931 and abs(2 * 0.6931 / 3 - 0.4621) < 5e-5 and round(math.sqrt(0.4621), 4) == 0.6798,
         "ln 2 = 0.6931, 2(0.6931)/3 = 0.4621, sqrt = 0.6798")
lv.claim(abs(math.exp(-1.5 * xs * xs) - 0.5) < 1e-14, "e^{-3x*^2/2} = 1/2 at x*")
# sign of G' either side, and G' by finite differences of quad
Gp = lambda x: 2 * phi(2 * x) - phi(x)
lv.claim(all(Gp(x) > 0 for x in [xs * j / 100 for j in range(1, 100)]) and all(Gp(x) < 0 for x in [xs + j / 50 for j in range(1, 300)]),
         "G' > 0 on (0, x*) and G' < 0 on (x*, x* + 6)")
lv.claim(all(abs((gq(x + 1e-5) - gq(x - 1e-5)) / 2e-5 - Gp(x)) < 1e-7 for x in (0.2, 0.5, xs, 1.0, 2.0)), "G' = 2phi(2x) - phi(x) by finite differences")
# second derivative
Gpp_s = sp.diff(Gp_s, xp)
lv.claim(sp.simplify(Gpp_s - (-8 * xp * ph.subs(t, 2 * xp) + xp * ph.subs(t, xp))) == 0, "G'' = -8x phi(2x) + x phi(x)")
lv.claim(sp.simplify(ph.subs(t, xs_sym) - 2 * ph.subs(t, 2 * xs_sym)) == 0, "phi(x*) = 2 phi(2x*)")
lv.claim(sp.simplify(Gpp_s.subs(xp, xs_sym) - (-6 * xs_sym * ph.subs(t, 2 * xs_sym))) == 0 and float(Gpp_s.subs(xp, xs_sym)) < 0, "G''(x*) = -6x* phi(2x*) < 0")
lv.claim(abs((Gp(xs + 1e-5) - Gp(xs - 1e-5)) / 2e-5 - (-6 * xs * phi(2 * xs))) < 1e-8, "G''(x*) numerically")
print(f"G(x*) = {Gnum(xs):.6f} (not stated)")

for v in [r"x^* = \sqrt{\tfrac{2\ln 2}{3}} \approx 0.680", r"\ln 2 \approx 0.6931", r"\tfrac{2 \times 0.6931}{3} \approx 0.4621", "0.6798",
          r"G'(x) = 2f(2x) - f(x)", r"A(2x) - A(x)", r"G''(x^*) = -6x^*\varphi(2x^*) < 0", r"2e^{-3x^2/2} - 1"]:
    lv.expect("homework", M, v)

# rubric
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [False, True, True, True, True], "rows 2 to 5 required, row 1 optional")
named = {1: 'a', 2: 'b', 3: 'c-point', 4: 'c-max'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(1, 2, 3, 4), (0, 1, 2, 3, 4)], "the only passes are rows 2-5 and all five")
lv.claim(all(set(named.values()) <= {named[i] for i in s if i in named} for s in passes), "every pass covers (a), (b), the point and the maximum")
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(key in it for key in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for y in items if y.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(y['difficulty'] == 5 for y in items), "homework limits")
blob = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in blob and '—' not in blob and '–' not in blob, "no ! or dashes")

lv.check_wrongs()
lv.report()
