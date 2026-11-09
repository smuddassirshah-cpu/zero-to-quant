"""limits-thm L1 performance task h-prove-capped-wait: every stated number, computed twice.

Run from the repository root with the venv that has numpy and sympy:
    <venv>/bin/python -I docs/reports/limits-thm-1-perf-numbers.py
Routes: exact rationals (Fraction) and sympy symbolic sums against a seeded Monte Carlo of the capped order.
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("limits-thm", 1)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'limits-thm', 'homework-1.json')
hw = json.load(open(HW, encoding='utf-8'))
items = hw['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-capped-wait']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"


def pmf(p, m):
    q = 1 - p
    return {k: (q ** (k - 1) * p if k < m else q ** (m - 1)) for k in range(1, m + 1)}


def mean_series(p, m):
    return sum(k * pr for k, pr in pmf(p, m).items())


def mean_recurrence(p, m):
    e = 0
    for _ in range(m):
        e = 1 + (1 - p) * e
    return e


def mean_closed(p, m):
    return (1 - (1 - p) ** m) / p


# (a), (b), (c) exactly in rationals for many p and m: pmf sums to 1, series = recurrence = closed form
ok_sum = ok_eq = True
for p in (F(1, 20), F(3, 20), F(1, 2), F(9, 10)):
    for m in range(1, 41):
        ok_sum &= sum(pmf(p, m).values()) == 1
        ok_eq &= mean_series(p, m) == mean_recurrence(p, m) == mean_closed(p, m)
        q = 1 - p
        G = sum(q ** j for j in range(m - 1))
        ok_sum &= G == (1 - q ** (m - 1)) / p and p * G + q ** (m - 1) == 1
        S = sum(k * q ** (k - 1) for k in range(1, m))
        ok_eq &= (1 - q) * S == G - (m - 1) * q ** (m - 1)
        ok_eq &= p * S + m * q ** (m - 1) == (1 - q ** (m - 1)) / p + q ** (m - 1)
lv.claim(ok_sum, "pmf adds to 1 and G = (1 - q^(m-1))/p, exact, m = 1..40")
lv.claim(ok_eq, "series, recurrence and (1 - q^m)/p agree exactly; (1 - q)S = G - (m-1)q^(m-1)")

# symbolic route with m left general
p_, k_, m_ = sp.symbols('p k m', positive=True)
q_ = 1 - p_
ser = sp.summation(k_ * q_ ** (k_ - 1) * p_, (k_, 1, m_ - 1)) + m_ * q_ ** (m_ - 1)
lv.claim(all(sp.nsimplify(sp.simplify(ser - (1 - q_ ** m_) / p_).subs({p_: sp.Rational(3, 20), m_: mm})) == 0 for mm in (1, 2, 5, 10, 17)),
         "sympy: the general series equals (1 - q^m)/p at sample m")
qs = sp.symbols('q', positive=True)
lhs = ((1 - qs ** (m_ - 1)) / (1 - qs) + qs ** (m_ - 1)) - (1 - qs ** m_) / (1 - qs)
lv.claim(sp.simplify(sp.expand_power_exp(sp.expand(lhs * (1 - qs)))) == 0, "sympy: (1-q^(m-1))/p + q^(m-1) = (1-q^m)/p")
lv.claim(sp.limit((1 - sp.Rational(17, 20) ** m_) / sp.Rational(3, 20), m_, sp.oo) == sp.Rational(20, 3), "limit as m -> oo is 1/p = 20/3")

# (d) the stated figures, exact and in floats
p, m = 0.15, 10
cancel = 0.85 ** 10
lv.claim(abs(cancel - float(F(17, 20) ** 10)) < 1e-15 and round(cancel, 4) == 0.1969, "cancel chance 0.85^10 = 0.1969")
lv.claim(round(0.85 ** 9, 4) == 0.2316 and abs(float(pmf(F(3, 20), 10)[10]) - 0.85 ** 9) < 1e-15, "P(T = 10) = 0.85^9 = 0.2316")
ET = mean_closed(p, m)
lv.claim(round(ET, 3) == 5.354 and abs(float(mean_series(F(3, 20), 10)) - ET) < 1e-12, "E[T] = 5.354, closed form and series")
lv.claim(round(1 - cancel, 4) == 0.8031 and round(0.8031 / 0.15, 3) == 5.354, "0.8031 / 0.15 = 5.354 as printed")
lv.claim(round(1 / p, 3) == 6.667, "1/p = 6.667")
lv.claim(round(1 / p - ET, 2) == 1.31, "the cap takes about 1.31 minutes off")
lv.claim(abs(cancel - 0.2) < 0.01, "cancelled about one time in five")

# seeded simulation of the order, minute by minute
rng = np.random.default_rng(20261109)
N = 1_000_000
X = rng.geometric(p, size=N)          # minute of first fill, support 1, 2, ...
T = np.minimum(X, m)
se = T.std() / math.sqrt(N)
lv.claim(abs(T.mean() - ET) < 4 * se, f"simulated E[T] {T.mean():.4f} within 4 se of 5.354")
fc = (X > m).mean()
lv.claim(abs(fc - cancel) < 4 * math.sqrt(cancel * (1 - cancel) / N), f"simulated cancel share {fc:.4f} near 0.1969")
f10 = (T == m).mean()
lv.claim(abs(f10 - 0.85 ** 9) < 4 * math.sqrt(0.2316 * 0.7684 / N), f"simulated P(T = 10) {f10:.4f} near 0.2316")
# a second, independent simulation: Bernoulli minutes drawn one by one (no geometric sampler)
U = rng.random((200_000, m)) < p
first = np.where(U.any(axis=1), U.argmax(axis=1) + 1, m)
lv.claim(abs(first.mean() - ET) < 4 * first.std() / math.sqrt(len(first)), f"minute-by-minute simulation E[T] {first.mean():.4f}")
X2 = rng.geometric(p, size=N)
lv.claim(abs(X2.mean() - 1 / p) < 4 * X2.std() / math.sqrt(N), "uncapped mean near 1/p = 6.667")

for v in ["0.1969", "0.2316", "0.8031", "5.354", "6.667", "1.31", "0.15", "0.85"]:
    lv.expect("homework", M, float(v))
lv.expect("homework", f"items[{I}].rubric[3].text", 0.1969)
lv.expect("homework", f"items[{I}].rubric[3].text", 5.354)
lv.expect("homework", f"items[{I}].rubric[4].text", 6.667)
lv.expect("homework", f"items[{I}].prompt", 0.15)
lv.expect("homework", f"items[{I}].prompt", 10)

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
lv.claim(all({parts[i] for i in s} == {'a', 'b', 'c', 'd'} for s in passes), "every pass covers (a), (b), (c) and (d)")
lv.claim(all(1 in s and 2 in s for s in passes), "every pass has both routes to the mean (conditioning and series)")

# shape and homework limits
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x_ in items if x_.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(x_.get('difficulty') == 5 for x_ in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")

lv.report()
