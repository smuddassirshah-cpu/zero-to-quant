"""analysis L4 performance task h-prove-uniform-diagonal: every stated number, computed twice.

Run from the repository root with the venv that has sympy:
    <venv>/bin/python -I docs/reports/analysis-4-perf-numbers.py
Routes: exact Fractions and integer search against sympy (symbolic solving, derivatives, limits) and floats on grids.
The rubric's passing tick sets are enumerated here and, when node is on the path, compared with tools/rubric-passes.mjs.
"""
import itertools
import json
import math
import os
import shutil
import subprocess
import sys
from fractions import Fraction as F

import sympy as sp

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("analysis", 4)
HW = os.path.join(ROOT, 'app', 'content', 'courses', 'analysis', 'homework-4.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-uniform-diagonal']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M, P = f"items[{I}].model", f"items[{I}].prompt"

n, x = sp.symbols('n x', positive=True)
xr = sp.symbols('xr', real=True)
h = 1 / (1 + n * xr ** 2)
hf = lambda k, t: 1 / (1 + k * t * t)
hF = lambda k, t: 1 / (1 + k * t * t)        # works on Fractions too

# (b) the pointwise limit, two routes
lv.claim(sp.limit(h.subs(xr, 0), n, sp.oo) == 1, "h_n(0) = 1 for every n, limit 1 (sympy)")
lv.claim(all(sp.limit(h.subs(xr, v), n, sp.oo) == 0 for v in (sp.Rational(1, 10), -3, sp.Rational(7, 2))), "h_n(x) -> 0 for x != 0 (sympy)")
lv.claim(all(0 < hf(k, t) < 1 / (k * t * t) for k in range(1, 400) for t in (-2.0, -0.3, 0.01, 0.5, 7.0)), "0 < h_n(x) < 1/(n x^2) for x != 0 (floats)")
# the Archimedean N > 1/(eps x^2) works, checked exactly
for eps, t in ((F(1, 100), F(1, 3)), (F(1, 1000), F(-2)), (F(1, 20), F(1, 50))):
    N = math.floor(1 / (eps * t * t)) + 1
    lv.claim(all(hF(k, t) < eps for k in range(N, N + 500)), f"N = {N} > 1/(eps x^2) works at eps = {eps}, x = {t}")
lv.claim(all(1 + k * t * t >= 1 for k in range(1, 50) for t in (-5.0, 0.0, 0.2)), "1 + n x^2 >= 1, the denominator never 0")

# (b) not uniform: h_n(1/sqrt n) = 1/2, symbolic and float
lv.claim(sp.simplify(h.subs(xr, 1 / sp.sqrt(n)) - sp.Rational(1, 2)) == 0, "h_n(1/sqrt n) = 1/2 (sympy)")
lv.claim(all(abs(hf(k, 1 / math.sqrt(k)) - 0.5) < 1e-12 for k in range(1, 5000)), "h_n(1/sqrt n) = 1/2 (floats, n < 5000)")
lv.claim(all(hF(F(1), F(1, k)) == 1 / (1 + F(1, k * k)) and 1 + F(1, k * k) > 1 for k in range(1, 50)), "h(1/k) = 0 while h_1(1/k) < 1: 1/k is never 0")
# (a) the moving-point claim fails without uniformity: h_n(x_n) -> 1/2, not h(0) = 1
lv.claim(all(abs(hf(k, 1 / math.sqrt(k)) - 1) > 0.49 for k in (10, 10 ** 4, 10 ** 8)), "pointwise only: h_n(1/sqrt n) stays 1/2 away from h(0) = 1")
# (a) the moving-point claim holds for a uniform example: g_n(x) = sqrt(x^2 + 1/n^2) -> |x| uniformly (gap <= 1/n)
g = lambda k, t: math.sqrt(t * t + 1 / (k * k))
lv.claim(all(abs(g(k, t) - abs(t)) <= 1 / k + 1e-15 for k in range(1, 300) for t in (-3.0, -0.01, 0.0, 0.4, 9.0)), "sqrt(x^2 + 1/n^2) is within 1/n of |x|")
lv.claim(abs(g(10 ** 6, 0.3 + 1e-6) - 0.3) < 1e-5 and abs(g(10 ** 6, 1 / 10 ** 6) - 0.0) < 1e-5, "g_n(x_n) -> |a| for x_n = a + 1/n at a = 0.3 and at a = 0")

# (c) sup over E of h_n is 4/(n+4): by the derivative's sign and evenness (sympy), and on a grid (floats)
dh = sp.diff(1 / (1 + n * x ** 2), x)
lv.claim(sp.simplify(dh + 2 * n * x / (1 + n * x ** 2) ** 2) == 0, "h_n' = -2nx/(1 + nx^2)^2 < 0 for x > 0")
lv.claim(sp.simplify(h.subs(xr, -xr) - h) == 0, "h_n is even, so |x| >= 1/2 reduces to x >= 1/2")
lv.claim(sp.simplify(h.subs(xr, sp.Rational(1, 2)) - 4 / (n + 4)) == 0, "h_n(1/2) = 4/(n + 4) (sympy)")
grid = [0.5 + j / 200 for j in range(20000)] + [-0.5 - j / 200 for j in range(20000)]
for k in (1, 7, 1329, 1330):
    lv.claim(abs(max(hf(k, t) for t in grid) - 4 / (k + 4)) < 1e-15, f"grid sup over E of h_{k} is 4/({k} + 4)")
lv.claim(all(F(4, k + 4) > F(4, k + 5) for k in range(1, 3000)), "4/(n + 4) falls as n grows")

# the uniform N > 4/eps works: 4/(n + 4) < 4/n <= 4/N < eps
for eps in (F(1, 10), F(3, 1000), F(1, 7)):
    N = math.floor(4 / eps) + 1
    lv.claim(all(F(4, k + 4) < F(4, k) <= F(4, N) < eps for k in range(N, N + 300)), f"N = {N} > 4/eps gives a uniform bound below {eps}")

# the smallest N for 0.003: search in Fractions, and sympy's inequality solving
eps = F(3, 1000)
N_search = next(k for k in range(1, 10 ** 5) if all(F(4, j + 4) < eps for j in range(k, k + 5000)))
m_ = sp.Symbol('m', real=True)
s = sp.solve_univariate_inequality(4 / (m_ + 4) < sp.Rational(3, 1000), m_, relational=False).intersect(sp.Interval.open(0, sp.oo))
lv.claim(s.left == sp.Rational(3988, 3) and s.left_open, "sympy: 4/(m + 4) < 0.003 exactly when m > 3988/3")
N_sym = math.floor(sp.Rational(3988, 3)) + 1
lv.claim(N_search == N_sym == 1330, f"smallest N = 1330 by search ({N_search}) and by solving ({N_sym})")
lv.claim(F(4, 1334) < eps and not F(4, 1333) < eps, "4/1334 < 0.003 and 4/1333 is not")
lv.claim(hF(1329, F(1, 2)) == F(4, 1333) and hF(1330, F(1, 2)) == F(4, 1334), "h_1329(1/2) = 4/1333 and h_1330(1/2) = 4/1334")
lv.claim(F(4000, 3) == 4 / eps and round(4000 / 3, 2) == 1333.33 and round(4000 / 3 - 4, 2) == 1329.33, "4/0.003 = 4000/3 = 1333.33, minus 4 is 1329.33")
lv.claim(f"{4 / 1334:.7f}" == "0.0029985" and round(float(F(4, 1334)), 7) == 0.0029985, "4/1334 = 0.0029985")
lv.claim(f"{4 / 1333:.7f}" == "0.0030008" and round(float(F(4, 1333)), 7) == 0.0030008, "4/1333 = 0.0030008")
crude_search = next(k for k in range(1, 10 ** 5) if F(4, k) < eps)
crude_formula = math.floor(F(4) / eps) + 1
lv.claim(crude_search == crude_formula == 1334, "the cruder bound 4/n gives 1334, by search and by formula")
lv.claim(all(F(4, k + 4) < eps for k in range(1334, 1400)), "N = 1334 works, but is not the smallest")

for v in (1330, 1329, 1334, 1333.33, 1329.33, 0.0029985, 0.0030008, 0.003):
    lv.expect("homework", M, v)
lv.expect("homework", M, "\\tfrac{4000}{3}")
lv.expect("homework", M, "\\tfrac{4}{1334}")
lv.expect("homework", M, "\\tfrac{4}{1333}")
lv.expect("homework", P, 0.003)
for v in (1330, 1334, 1333, 0.003):
    lv.expect("homework", f"items[{I}].rubric[3].text", v)

# rubric: sums to 10, rows 1 to 4 required, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 optional")
lv.claim('Optional, one more point:' in it['prompt'] and rub[4]['text'].startswith('(c) Optional'), "row 5's part is marked optional in the prompt")
named = {0: 'a: f continuous', 1: 'a: moving point', 2: 'b: limit and not uniform', 3: 'c: uniform and N'}
passes = [st for r in range(1, len(rub) + 1) for st in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in st) >= 7 and all(i in st for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in st) for st in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all(all(i in st for i in named) for st in passes), "every pass covers each named part: (a) twice, (b), (c)")
node = shutil.which('node')
if node:
    out = subprocess.run([node, 'tools/rubric-passes.mjs', '--item', f'content/courses/analysis/homework-4.json#{it["id"]}', '--json'],
                         cwd=os.path.join(ROOT, 'app'), capture_output=True, text=True).stdout
    rp = json.loads(out)[0]
    lv.claim(rp['passingSets'] == len(passes) and [r['canBeLeftOut'] for r in rp['rows']] == [False] * 4 + [True],
             "rubric-passes.mjs agrees: 2 passing sets, only row 5 can be left out")
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for y in items if y.get('performance')) == 1, "one performance task in the homework")
lv.claim(len(items) <= 12, "homework at most 12 items")
txt = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in txt and '—' not in txt and '–' not in txt, "no ! or dashes")
lv.claim(txt.count('$$') == 4 and txt.count('\\\\begin{aligned}') == 2, "the two displays are split with aligned, three lines and two lines")

lv.report()
