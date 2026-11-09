"""analysis L3 performance task h-prove-integral-test: every stated number, computed twice.

Run from the repository root with the venv that has sympy and mpmath:
    <venv>/bin/python -I docs/reports/analysis-3-perf-numbers.py
Routes: sympy (symbolic) against mpmath and math (numeric); the true tails by Euler-Maclaurin (mpmath.sumem)
and by a direct sum plus the integral with its first correction terms.
"""
import itertools
import json
import math
import os
import sys

import mpmath
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("analysis", 3)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'analysis', 'homework-3.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-integral-test']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"
mpmath.mp.dps = 40

x, X, K = sp.symbols('x X K', positive=True)
f = 1 / (x * sp.log(x) ** 2)
# (b) the antiderivative and the integral, symbolic and numeric
lv.claim(sp.simplify(sp.diff(-1 / sp.log(x), x) - f) == 0, "d/dx(-1/ln x) = 1/(x (ln x)^2)")
FX = sp.integrate(f, (x, 2, X))
lv.claim(sp.simplify(FX - (1 / sp.log(2) - 1 / sp.log(X))) == 0, "int_2^X f = 1/ln 2 - 1/ln X (sympy)")
lv.claim(sp.limit(1 / sp.log(2) - 1 / sp.log(X), X, sp.oo) == 1 / sp.log(2), "limit is 1/ln 2")
fm = lambda t: 1 / (t * mpmath.log(t) ** 2)
q = mpmath.quad(lambda u: fm(mpmath.e ** u) * mpmath.e ** u, [mpmath.log(2), 10, 100, mpmath.inf])
lv.claim(abs(q - 1 / mpmath.log(2)) < 1e-12, "int_2^inf f = 1/ln 2 (mpmath quadrature after x = e^u)")
lv.claim(round(1 / math.log(2), 4) == 1.4427 and mpmath.nstr(1 / mpmath.log(2), 5) == '1.4427', "1/ln 2 = 1.4427")
for k0 in (2, 5, 50, 22026):
    lv.claim(abs(mpmath.quad(fm, [k0, k0 + 1]) - (1 / mpmath.log(k0) - 1 / mpmath.log(k0 + 1))) < 1e-25, f"int_{k0}^{k0+1} f by quadrature and by the antiderivative")
# hypotheses: positive and decreasing on [2, inf), sampled on a fine grid and by the derivative's sign
lv.claim(all(fm(2 + j / 50) > fm(2 + (j + 1) / 50) > 0 for j in range(5000)), "f positive and decreasing on [2, 102] (grid)")
fp = sp.simplify(sp.diff(f, x))
lv.claim(all(fp.subs(x, v) < 0 for v in (2, 3, 10, 1000, 10 ** 9)), "f' < 0 at sample points")
lv.claim(sp.simplify(fp + (sp.log(x) + 2) / (x ** 2 * sp.log(x) ** 3)) == 0, "f' = -(ln x + 2)/(x^2 (ln x)^3), negative for x >= 2")

# (a) the term bounds a_{k+1} <= int_k^{k+1} f <= a_k on many k
lv.claim(all(fm(k + 1) <= 1 / mpmath.log(k) - 1 / mpmath.log(k + 1) <= fm(k) for k in range(2, 3000)), "a_{k+1} <= int_k^{k+1} f <= a_k for k < 3000")

# the ratio test: ratios tend to 1, and the squeeze for ln n / ln(n+1)
ratio = lambda n: (n / (n + 1)) * (math.log(n) / math.log(n + 1)) ** 2
lv.claim(all(ratio(n) < 1 for n in range(2, 10 ** 5)), "every ratio is below 1")
lv.claim(abs(ratio(10 ** 7) - 1) < 1e-6 and sp.limit((X / (X + 1)) * (sp.log(X) / sp.log(X + 1)) ** 2, X, sp.oo) == 1, "ratios tend to 1 (float and sympy)")
lv.claim(all(1 - 1 / (n * math.log(n)) <= math.log(n) / math.log(n + 1) < 1 for n in range(2, 10 ** 5)), "1 - 1/(n ln n) <= ln n/ln(n+1) < 1")
lv.claim(all(0 < math.log1p(1 / n) <= 1 / n for n in range(1, 10 ** 5)), "0 < ln(1 + 1/n) <= 1/n")
lv.claim(all(mpmath.log(1 + t) <= t for t in [mpmath.mpf(j) / 97 for j in range(1, 2000)]), "ln(1 + t) <= t on a grid")
lv.claim(all(mpmath.quad(lambda u: 1 / u, [1, 1 + t]) - mpmath.log(1 + t) < 1e-30 for t in (0.5, 1, 3)), "ln(1 + t) = int_1^{1+t} dx/x")

# (c) K = 22027, two routes, and the stated logarithms
e10 = mpmath.e ** 10
lv.claim(mpmath.nstr(e10, 7) == '22026.47' and round(math.exp(10), 2) == 22026.47, "e^10 = 22026.47")
K1 = next(k for k in range(22000, 22100) if 1 / math.log(k) < 0.1)
K2 = int(mpmath.floor(e10)) + 1
lv.claim(K1 == K2 == 22027, "smallest K with 1/ln K < 0.1 is 22027, by search and by e^10")
lv.claim(mpmath.nstr(mpmath.log(22027), 8) == '10.000024' and round(math.log(22027), 6) == 10.000024, "ln 22027 = 10.000024")
lv.claim(mpmath.nstr(mpmath.log(22026), 7) == '9.999979' and round(math.log(22026), 6) == 9.999979, "ln 22026 = 9.999979")
lv.claim(1 / mpmath.log(22026) > mpmath.mpf('0.1') > 1 / mpmath.log(22027), "1/ln 22026 > 0.1 > 1/ln 22027")
lv.claim(all(1 / mpmath.log(k + 1) > mpmath.mpf('0.1') for k in range(21900, 22026)), "for K <= 22025 the lower bound exceeds 0.1")
lv.claim(22026 < e10 < 22027, "22026 < e^10 < 22027")


def em_from(a):
    """sum_{n >= a} f(n) by Euler-Maclaurin: the exact integral 1/ln a plus the end corrections."""
    a = mpmath.mpf(a)
    return 1 / mpmath.log(a) + fm(a) / 2 - mpmath.diff(fm, a) / 12 + mpmath.diff(fm, a, 3) / 720


def tail_em(k):
    return em_from(k + 1)


def tail_direct(k, terms=200000):
    """Second route: add the next `terms` terms one by one, then Euler-Maclaurin far out."""
    s = mpmath.fsum(fm(n) for n in range(k + 1, k + 1 + terms))
    return s + em_from(k + 1 + terms)


for k0 in (2, 10, 100, 1000, 22025, 22026, 22027):
    t = tail_em(k0)
    lv.claim(1 / mpmath.log(k0 + 1) <= t <= 1 / mpmath.log(k0), f"1/ln(K+1) <= tail <= 1/ln K at K = {k0}")
for k0 in (1000, 22026):
    lv.claim(abs(tail_em(k0) - tail_direct(k0)) < 1e-12, f"tail at K = {k0}: Euler-Maclaurin and direct sum agree")
S = mpmath.fsum(fm(n) for n in range(2, 1001)) + tail_em(1000)
lv.claim(abs(S - (mpmath.fsum(fm(n) for n in range(2, 1001)) + tail_direct(1000))) < 1e-12, "the sum S, two routes")
print("sum S =", mpmath.nstr(S, 10), "; tail at 22026 =", mpmath.nstr(tail_em(22026), 12))
true_K = next(k for k in (22025, 22026, 22027) if tail_em(k) < mpmath.mpf('0.1'))
lv.claim(true_K in (22026, 22027), f"the true smallest K ({true_K}) is 22,026 or 22,027, as the model says")
lv.claim(S <= fm(2) + 1 / mpmath.log(2), "S <= a_2 + I, the bound of (a)")

for v in ["1.4427", "22026.47", "10.000024", "9.999979", "0.1"]:
    lv.expect("homework", M, float(v))
for v in [22027, 22026, 22025]:
    lv.expect("homework", M, v)
lv.expect("homework", f"items[{I}].rubric[3].text", 22027)
lv.expect("homework", f"items[{I}].rubric[3].text", 22026.47)
lv.expect("homework", f"items[{I}].rubric[4].text", 22025)

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 optional")
parts = {0: 'a', 1: 'a', 2: 'b', 3: 'c', 4: 'c'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({parts[i] for i in s} == {'a', 'b', 'c'} for s in passes) and all(1 in s for s in passes), "every pass covers (a) with its tail bound, (b) and (c)")
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x_ in items if x_.get('performance')) == 1, "one performance task in the homework")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")

lv.report()
