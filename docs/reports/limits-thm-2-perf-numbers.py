"""limits-thm L2 performance task h-prove-cycles-exponential: every stated number, computed twice.

Run from the repository root with the venv that has numpy, scipy and sympy:
    <venv>/bin/python -I docs/reports/limits-thm-2-perf-numbers.py
Routes: closed forms (sympy, exact rationals, scipy quadrature) against seeded simulations of the cycle model,
the exponential and the uniform audit error.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp
from scipy import integrate

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("limits-thm", 2)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'limits-thm', 'homework-2.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-cycles-exponential']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"
rng = np.random.default_rng(20261109)

# (a) P(T_n > t) = r^floor(nt): exact product of misses against a direct sum over the fill cycle
ok = True
for lam, n in ((F(1, 2), 10), (F(3, 2), 7), (F(2), 5)):
    r = 1 - lam / n
    for t in (F(0), F(1, 3), F(1), F(37, 10), F(4)):
        j = math.floor(n * t)
        direct = 1 - sum(r ** (k - 1) * (lam / n) for k in range(1, j + 1))   # 1 - P(K <= floor(nt))
        ok &= direct == r ** j
lv.claim(ok, "1 - P(K <= floor(nt)) = (1 - lam/n)^floor(nt), exact rationals")
K = rng.geometric(0.05, size=1_000_000)       # n = 10, lam = 0.5: chance 0.05 a cycle
for t in (0.25, 1.0, 2.55, 4.0):
    sim = (K / 10 > t).mean()
    ex = 0.95 ** math.floor(10 * t)
    lv.claim(abs(sim - ex) < 4 * math.sqrt(ex * (1 - ex) / len(K)), f"simulated P(T_10 > {t}) {sim:.4f} against 0.95^floor(10t) {ex:.4f}")

# (b) the squeeze holds and the limit is e^{-lam t}
ok = True
for lam in (0.5, 2.0):
    for n in (5, 50, 500):
        if n <= lam:
            continue
        r = 1 - lam / n
        for t in np.linspace(0, 6, 241):
            j = math.floor(n * t)
            ok &= r ** (n * t) <= r ** j + 1e-15 and r ** j < r ** (n * t - 1)
lv.claim(ok, "r^(nt) <= r^floor(nt) < r^(nt - 1) on a grid")
n_, t_, l_ = sp.symbols('n t lambda', positive=True)
lv.claim(sp.simplify(sp.limit((1 - l_ / n_) ** (n_ * t_), n_, sp.oo) - sp.exp(-l_ * t_)) == 0, "sympy: (1 - lam/n)^(nt) -> e^(-lam t)")
lv.claim(sp.limit((1 - l_ / n_) ** (-1), n_, sp.oo) == 1, "sympy: r^(-1) -> 1")
lv.claim(all(abs((1 - 0.5 / 10 ** 6) ** math.floor(10 ** 6 * t) - math.exp(-0.5 * t)) < 1e-5 for t in (0.3, 1.7, 4)), "n = 10^6 is within 1e-5 of the limit")
s_ = sp.symbols('s', positive=True)
lv.claim(sp.simplify(sp.integrate(l_ * sp.exp(-l_ * s_), (s_, t_, sp.oo)) - sp.exp(-l_ * t_)) == 0, "sympy: tail integral of the density is e^(-lam t)")
lv.claim(abs(integrate.quad(lambda s: 0.5 * math.exp(-0.5 * s), 4, np.inf)[0] - math.exp(-2)) < 1e-10, "quadrature: tail at 4 is e^-2")
E = rng.exponential(2.0, size=1_000_000)
lv.claim(abs((E > 4).mean() - math.exp(-2)) < 4 * math.sqrt(0.1353 * 0.8647 / len(E)), "simulated exponential P(T > 4) near e^-2")

# (c) the figures
lim = math.exp(-2)
p10, p100 = 0.95 ** 40, 0.995 ** 400
lv.claim(round(lim, 4) == 0.1353 and round(p10, 4) == 0.1285 and round(p100, 4) == 0.1347, "e^-2 = 0.1353, 0.95^40 = 0.1285, 0.995^400 = 0.1347")
lv.claim(abs(p10 - float(F(19, 20) ** 40)) < 1e-15 and abs(p100 - float(F(199, 200) ** 400)) < 1e-15, "powers checked in exact rationals")
lv.claim(p10 < p100 < lim, "both below the limit, the finer one closer")
lv.claim(round(lim - p10, 4) == 0.0068 and round(lim - p100, 4) == 0.0007, "gaps 0.0068 and 0.0007")
lv.claim(0.5 * 4 == 2 and 10 * 4 == 40 and 0.5 / 10 == 0.05 and 100 * 4 == 400 and 0.5 / 100 == 0.005, "lam t = 2, nt = 40, lam/n = 0.05; n = 100 gives 400 and 0.005")
lv.claim(all(math.log1p(-x) < -x for x in np.linspace(1e-6, 0.999, 2000)), "ln(1 - x) < -x on (0, 1)")
lv.claim(all(abs(integrate.quad(lambda u: 1 / u, 1 - x, 1)[0] + math.log(1 - x)) < 1e-10 for x in (0.05, 0.3, 0.9)), "ln(1 - x) = -int_{1-x}^1 du/u")
K100 = rng.geometric(0.005, size=1_000_000)
sim100 = (K100 / 100 > 4).mean()
lv.claim(abs(sim100 - p100) < 4 * math.sqrt(p100 * (1 - p100) / len(K100)), f"simulated P(T_100 > 4) {sim100:.4f} near 0.1347")

# (d) the uniform moments, symbolic and numeric
a_, b_, x_ = sp.symbols('a b x', real=True)
EX = sp.integrate(x_ / (b_ - a_), (x_, a_, b_))
EX2 = sp.integrate(x_ ** 2 / (b_ - a_), (x_, a_, b_))
lv.claim(sp.simplify(EX - (a_ + b_) / 2) == 0, "sympy: E[D] = (a + b)/2")
lv.claim(sp.simplify(EX2 - (a_ ** 2 + a_ * b_ + b_ ** 2) / 3) == 0, "sympy: E[D^2] = (a^2 + ab + b^2)/3")
lv.claim(sp.simplify(EX2 - EX ** 2 - (b_ - a_) ** 2 / 12) == 0, "sympy: Var = (b - a)^2/12")
lv.claim(sp.expand(4 * (a_ ** 2 + a_ * b_ + b_ ** 2) - 3 * (a_ + b_) ** 2 - (a_ - b_) ** 2) == 0, "the common-denominator algebra")
lv.claim(sp.expand((b_ - a_) * (a_ ** 2 + a_ * b_ + b_ ** 2) - (b_ ** 3 - a_ ** 3)) == 0, "difference of cubes")
a, b = -0.02, 0.08
mean, var = (a + b) / 2, (b - a) ** 2 / 12
lv.claim(abs(mean - 0.03) < 1e-15 and abs((a + b) - 0.06) < 1e-15, "E[D] = 0.06/2 = 0.03 s")
lv.claim(round(var, 6) == 0.000833 and abs(var - float(F(1, 10) ** 2 / 12)) < 1e-15, "Var = 0.1^2/12 = 0.000833")
lv.claim(round(math.sqrt(var), 4) == 0.0289 and round(0.1 / math.sqrt(12), 4) == 0.0289, "sd = 0.1/sqrt(12) = 0.0289 s, 28.9 ms")
U = rng.uniform(a, b, size=1_000_000)
lv.claim(abs(U.mean() - 0.03) < 4 * math.sqrt(var / len(U)) and abs(U.std() - 0.0289) < 2e-4, f"simulated D: mean {U.mean():.5f}, sd {U.std():.5f}")

for v in ["0.1353", "0.1285", "0.1347", "0.0068", "0.0007", "0.05", "0.03", "0.000833", "0.0289", "28.9", "-0.02", "0.08"]:
    lv.expect("homework", M, float(v))
for v in [40, 400, 10, 100, 30, 12]:
    lv.expect("homework", M, v)
lv.expect("homework", f"items[{I}].rubric[2].text", 0.1285)
lv.expect("homework", f"items[{I}].rubric[2].text", 0.1347)
lv.expect("homework", f"items[{I}].rubric[2].text", 0.1353)
lv.expect("homework", f"items[{I}].rubric[4].text", 0.0289)
lv.expect("homework", f"items[{I}].rubric[4].text", 0.03)
lv.expect("homework", f"items[{I}].prompt", 0.5)

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, False, True], "rows 1, 2, 3 and 5 required, row 4 optional")
parts = {0: 'a', 1: 'b', 2: 'c', 3: 'c', 4: 'd'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 4), (0, 1, 2, 3, 4)], "the only passes are rows 1, 2, 3, 5 and all five")
lv.claim(all({parts[i] for i in s} == {'a', 'b', 'c', 'd'} for s in passes), "every pass covers (a) to (d)")
lv.claim(all(1 in s and 4 in s for s in passes), "every pass has the exponential survival limit and the uniform variance")

lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x in items if x.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(x.get('difficulty') == 5 for x in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")

lv.report()
