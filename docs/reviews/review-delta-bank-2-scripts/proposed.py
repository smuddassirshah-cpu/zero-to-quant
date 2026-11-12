#!/usr/bin/env python3
"""Numbers of every fix proposed in review-delta-bank-2.md for a typed or choice item, each by two routes.
(The proposed hidden tests are in proposed_code.py.)  Usage: python docs/reviews/review-delta-bank-2-scripts/proposed.py"""
import math, sys
from fractions import Fraction as F
Phi = lambda z: 0.5 * math.erfc(-z / math.sqrt(2))
n = bad = 0
def ok(cond, label):
    global n, bad
    n += 1
    print(('ok   ' if cond else 'FAIL ') + label)
    bad += 0 if cond else 1
r2 = lambda v, p: float(f'{v:.{p}f}')

# finding 1: collinear-features-inflation-factor with correlation 0.5
vif = 1 / (1 - F(1, 2) ** 2)
# second route: variance of a slope with two standardised predictors is sigma^2 / (n (1 - r^2)); ratio to r = 0
ok(vif == F(4, 3) and abs(float(vif) - (1 / (1 - 0.25))) < 1e-12 and r2(float(vif), 2) == 1.33, 'VIF at r = 0.5 is 4/3 = 1.3333, 1.33 to 2 places')
ok(1 / (1 - 0.5) == 2 and r2(math.sqrt(4 / 3), 2) == 1.15 and abs(math.sqrt(4 / 3) - 1.1547) < 5e-5, 'slips: 2 (no square) and 1.15 (root, 1.1547)')
ok(abs(1.3333 - 1.33) <= 0.005 and abs(2 - 4 / 3) > 0.01 and abs(1.15 - 4 / 3) > 0.01, 'bands of 0.005 hold 1.33 and 1.3333 and stay apart')

# finding 2: weak-signal-daily-edge with 0.07% a day, sd 1.4%, 1,225 days
se = F(14, 10) / 35
t = F(7, 100) / se
ok(math.isqrt(1225) == 35 and se == F(4, 100) and t == F(7, 4), 'se 0.04%, t = 1.75')
ok(abs(0.07 * math.sqrt(1225) / 1.4 - 1.75) < 1e-12, 't by mean times root n over sd')
ok(r2(0.07 / 1.4, 2) == 0.05 and r2(0.07 / 1.4 * math.sqrt(252), 2) == 0.79 and abs(0.05 * math.sqrt(252) - 0.7937) < 5e-5, 'slips 0.05 (no root) and 0.79 (annual Sharpe, 0.7937)')
ok((F(35, 10) * F(14, 10) / F(7, 100)) ** 2 == 4900 == 4 * 1225, 't = 3.5 needs four times the data, 4,900 days')

# finding 3: ht-pvalue-z-two-and-a-half with z = 2.05
one = 1 - Phi(2.05)
ok(abs(one - 0.0202) < 5e-5 and abs(2 * one - 0.0404) < 5e-5 and f'{2 * one:.3f}' == '0.040' and f'{one:.3f}' == '0.020', f'z = 2.05: one tail {one:.4f}, two-sided {2 * one:.4f}')
ok(0.01 < 2 * one < 0.05, 'significant at 5% but not at 1%')
# second route: numerical integral of the density
h = 1e-4; integ = sum(math.exp(-((2.05 + (k + 0.5) * h) ** 2) / 2) for k in range(int(8 / h))) * h / math.sqrt(2 * math.pi)
ok(abs(integ - one) < 1e-7, 'tail beyond 2.05 by a midpoint integral')

# finding 4: sample-size-for-signal-sharpe-years with Sharpe 1.1
T = (F(3) / F(11, 10)) ** 2
ok(T == F(900, 121) and abs(float(T) - 7.438) < 5e-4 and r2(float(T), 1) == 7.4, f'years (3/1.1)^2 = {float(T):.4f}, 7.4 to 1 place')
ok(abs(1.1 * math.sqrt(float(T)) - 3) < 1e-12, 'check: 1.1 times root T is 3')
ok(r2(3 / 1.1, 1) == 2.7 and r2((2 / 1.1) ** 2, 1) == 3.3, 'slips 2.7 (no square, 2.727) and 3.3 (t of 2, 3.306)')
ok(abs(7.44 - float(T)) <= 0.05 and abs(7.4 - float(T)) <= 0.05, 'band 0.05 holds 7.4 and 7.44')

# finding 12: pf-types-round-half-even with two halves of different parity
expr = 'int(-1.5) + round(-1.5) + round(-4.5) + (-9 // 2)'
terms = (int(-1.5), round(-1.5), round(-4.5), -9 // 2)
ok(eval(expr) == -12 and terms == (-1, -2, -4, -5), f'{expr} is -12: {terms}')
trunc = lambda x: int(x)
half_up = lambda x: math.floor(x + 0.5)
half_away = lambda x: int(math.copysign(math.floor(abs(x) + 0.5), x))
ok(trunc(-1.5) + trunc(-1.5) + trunc(-4.5) + trunc(-9 / 2) == -10, 'all cut towards zero: -10')
ok(int(-1.5) + half_up(-1.5) + half_up(-4.5) + (-9 // 2) == -11, 'half rounded up: -11')
ok(int(-1.5) + half_away(-1.5) + half_away(-4.5) + (-9 // 2) == -13, 'half rounded away from zero (the school rule): -13')
ok(int(-3.5) + half_away(-3.5) + (-9 // 2) == -12, 'as the item stands, the school rule gives the key, -12')

# finding 11: strangle, the size without the sign
ok(abs(3.20 + 2.80 - (90 - 81)) == 3, 'short strangle: the unsigned slip is 3')

# finding 14: the dropout story with the baseline scored on the held-out cohort
se83 = math.sqrt(0.83 * 0.17 / 400)
ok(abs(se83 - 0.0188) < 5e-5 and abs(3 / 2 - 1.5) < 1e-12, 'standard error 1.88 points ("about 2"); 3 points over 2 is one and a half')

print(f'{n} checks, {bad} failures')
sys.exit(1 if bad else 0)
