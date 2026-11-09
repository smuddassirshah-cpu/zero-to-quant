"""limits-thm L3 performance task h-prove-desk-guarantee: every stated number, computed twice.

Run from the repository root with the venv that has numpy, scipy and sympy:
    <venv>/bin/python -I docs/reports/limits-thm-3-perf-numbers.py
Routes: exact rationals and integer binomial sums (math.comb) against scipy and seeded simulations of the book.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp
from scipy.stats import binom, norm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("limits-thm", 3)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'limits-thm', 'homework-3.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-desk-guarantee']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"
rng = np.random.default_rng(20261109)

# (a), (b): the indicator bound pointwise, then Markov and Chebyshev on random discrete laws, exactly
ok_pt = all(a * (1 if y >= a else 0) <= y for y in np.linspace(0, 10, 401) for a in (0.1, 1, 2.5, 7))
lv.claim(ok_pt, "a 1{Y >= a} <= Y for Y >= 0, pointwise grid")
ok_m = ok_c = True
for _ in range(300):
    k = int(rng.integers(2, 7))
    vals = [F(int(v)) for v in rng.integers(-20, 21, size=k)]
    w = [F(int(x)) for x in rng.integers(1, 10, size=k)]
    pr = [x / sum(w) for x in w]
    yv = [abs(v) for v in vals]
    EY = sum(p * y for p, y in zip(pr, yv))
    for a in (F(1, 2), F(3), F(11)):
        ok_m &= sum(p for p, y in zip(pr, yv) if y >= a) <= EY / a
    mu = sum(p * v for p, v in zip(pr, vals))
    var = sum(p * (v - mu) ** 2 for p, v in zip(pr, vals))
    for eps in (F(1), F(5, 2), F(9)):
        ok_c &= sum(p for p, v in zip(pr, vals) if abs(v - mu) >= eps) <= var / eps ** 2
lv.claim(ok_m, "Markov holds on 300 random laws (exact)")
lv.claim(ok_c, "Chebyshev holds on 300 random laws (exact)")
Z = rng.standard_t(5, size=500_000)
lv.claim(all((np.abs(Z) >= e).mean() <= (5 / 3) / e ** 2 for e in (1, 2, 3)), "Chebyshev holds for a simulated t(5), variance 5/3")

# (c): non-identical bets, the variance of the average and the bound
kinds = [((1, -1), (0.55, 0.45)), ((3, -1), (0.3, 0.7)), ((10, -2), (0.1, 0.9)), ((0.5, -0.5), (0.5, 0.5))]
def mv(k):
    (x, y), (p, q) = k
    m = p * x + q * y
    return m, p * x * x + q * y * y - m * m
vs = [mv(k)[1] for k in kinds]
v = max(vs)
n, eps = 400, 0.3
seq = [kinds[i % 4] for i in range(n)]
mubar = sum(mv(k)[0] for k in seq) / n
var_avg = sum(mv(k)[1] for k in seq) / n ** 2
lv.claim(var_avg <= v / n, "Var(average) <= v/n for a mixed book")
sims = np.zeros(20_000)
for k in range(4):
    (x, y), (p, q) = kinds[k]
    cnt = n // 4
    w = rng.binomial(cnt, p, size=sims.size)
    sims += w * x + (cnt - w) * y
avg = sims / n
lv.claim(abs(avg.var() - var_avg) < 0.05 * var_avg, f"simulated Var(average) {avg.var():.5f} against {var_avg:.5f}")
lv.claim((np.abs(avg - mubar) >= eps).mean() <= v / (n * eps ** 2), "simulated miss chance under v/(n eps^2)")
i_, n_ = sp.symbols('i n', positive=True, integer=True)
lv.claim(sp.simplify(sp.summation(i_, (i_, 1, n_)) / n_ ** 2 - (n_ + 1) / (2 * n_)) == 0 and sp.limit((n_ + 1) / (2 * n_), n_, sp.oo) == sp.Rational(1, 2),
         "sigma_i^2 = i: Var(average) = (n+1)/(2n) -> 1/2")

# (d): the two kinds, exactly
mA, mB = F(55, 100) - F(45, 100), F(3, 10) * 3 - F(7, 10)
EA2, EB2 = F(1), F(3, 10) * 9 + F(7, 10)
vA, vB = EA2 - mA ** 2, EB2 - mB ** 2
lv.claim((mA, mB, EB2, vA, vB) == (F(1, 10), F(1, 5), F(17, 5), F(99, 100), F(84, 25)), "means 0.1, 0.2; E[X^2] 1, 3.4; variances 0.99, 3.36")
lv.claim(abs(mv(kinds[0])[1] - 0.99) < 1e-12 and abs(mv(kinds[1])[1] - 3.36) < 1e-12, "the same variances in floats")
lv.claim(mA + mB == F(3, 10) and vA + vB == F(435, 100), "per pair: mean 0.3, variance 4.35")
bound = lambda m: F(435, 100) * m / (F(3, 10) * m) ** 2
lv.claim(bound(966) > F(1, 20) and bound(967) <= F(1, 20), "Chebyshev: 966 fails, 967 is the smallest n")
lv.claim(round(4.35 / (0.09 * 0.05), 1) == 966.7 and math.ceil(F(435, 100) / (F(9, 100) * F(1, 20))) == 967 and 2 * 967 == 1934, "n >= 966.7, so 967 of each, 1,934 in all")


def exact_loss_comb(m):
    """P(S <= 0) = P(W_A + 2 W_B <= m), by integer binomial sums."""
    tot = F(0)
    cA = [math.comb(m, k) * 55 ** k * 45 ** (m - k) for k in range(m + 1)]
    run, cum = 0, []
    for c in cA:
        run += c
        cum.append(run)
    for wb in range(m // 2 + 1):
        tot += F(math.comb(m, wb) * 3 ** wb * 7 ** (m - wb), 10 ** m) * F(cum[m - 2 * wb], 100 ** m)
    return tot


def exact_loss_scipy(m):
    wb = np.arange(m // 2 + 1)
    return float(np.sum(binom.pmf(wb, m, 0.3) * binom.cdf(m - 2 * wb, m, 0.55)))


for m in (131, 135, 136):
    a1, a2 = float(exact_loss_comb(m)), exact_loss_scipy(m)
    lv.claim(abs(a1 - a2) < 1e-12, f"exact P(S <= 0) at n = {m}: {a1:.5f}, two routes agree")
lv.claim(float(exact_loss_comb(135)) > 0.05 >= float(exact_loss_comb(136)), "exact smallest n is 136 (135 fails)")
lv.claim(next(m for m in range(100, 200) if exact_loss_scipy(m) <= 0.05) == 136, "scan: 136 is the first n with exact chance <= 0.05")
lv.claim(float(exact_loss_comb(967)) < 1e-4, "at n = 967 the true loss chance is tiny")
for m in (131, 136):
    A = rng.binomial(m, 0.55, size=2_000_000)
    B = rng.binomial(m, 0.3, size=2_000_000)
    S = (2 * A - m) + (4 * B - m)
    ph = (S <= 0).mean()
    ex = exact_loss_scipy(m)
    lv.claim(abs(ph - ex) < 4 * math.sqrt(ex * (1 - ex) / S.size), f"simulated P(S <= 0) at n = {m}: {ph:.5f} against {ex:.5f}")
    lv.claim(abs(S.mean() - 0.3 * m) < 0.1 and abs(S.var() / (4.35 * m) - 1) < 0.01, f"simulated S mean and variance at n = {m}")

# the normal model
r435 = math.sqrt(4.35)
lv.claim(round(r435, 4) == 2.0857, "sqrt(4.35) = 2.0857")
lv.claim(round(1.645 * 2.0857 / 0.3, 2) == 11.44 and round((1.645 * r435 / 0.3) ** 2, 1) == 130.8, "sqrt n >= 11.44, n >= 130.8")
phi = lambda m: norm.cdf(-0.3 * m / math.sqrt(4.35 * m))
lv.claim(phi(130) > 0.05 >= phi(131), "normal model: 131 is the smallest n (scipy Phi)")
lv.claim(next(m for m in range(100, 200) if 0.3 * math.sqrt(m) / r435 >= 1.645) == 131, "normal model with the 1.645 cut-off: 131")
lv.claim(phi(131) < exact_loss_scipy(131), "the uncorrected normal gives S <= 0 too little chance at 131")
lv.claim(round(967 / 136) == 7 and round(967 / 131) == 7, "Chebyshev asks for about seven times as many")

for val in ["0.55", "0.45", "0.1", "0.99", "0.2", "3.4", "3.36", "0.3", "4.35", "0.09", "0.05", "966.7", "2.0857", "1.645", "11.44", "130.8"]:
    lv.expect("homework", M, float(val))
for val in [967, 1934, 131, 136]:
    lv.expect("homework", M, val)
for val in ["0.1", "0.2", "0.99", "3.36", "4.35"]:
    lv.expect("homework", f"items[{I}].rubric[3].text", float(val))
lv.expect("homework", f"items[{I}].rubric[3].text", 967)
lv.expect("homework", f"items[{I}].rubric[4].text", 131)

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 optional")
parts = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'd'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({parts[i] for i in s} == {'a', 'b', 'c', 'd'} for s in passes), "every pass covers (a) to (d)")
lv.claim(all(0 in s and 1 in s for s in passes), "every pass derives Markov and Chebyshev from Markov")

lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x in items if x.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(x.get('difficulty') == 5 for x in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")

lv.report()
