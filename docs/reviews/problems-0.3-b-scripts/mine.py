"""Second read, problems 0.3 (b): the reader's own answers and slips for exp-log problem sets 1 to 3.

Every part was solved from its text before its key was read. Here each answer is computed two ways (sympy exact or
mpmath, then a second route: stepping the story month by month, bisection, counting halvings, a loop), compared with
the content key inside the part's own tolerance, and every wrong[] value is rebuilt from the slip its feedback names
and compared inside that entry's own band. Further checks per numeric part:
  - the band takes every value in ACCEPT (the value the feedback prints, sensible roundings in the stated form,
    the value carried from the rounded earlier part) and refuses every value in REFUSE;
  - no wrong band overlaps the answer band or another wrong band.
Rows in NOTE are the reader's findings: they print, and do not fail the run.

Run from the repo root:  <venv>/bin/python docs/reviews/problems-0.3-b-scripts/mine.py
"""
import json
import math
import sys

import mpmath as mp
import sympy as sp

mp.mp.dps = 30
checks = fails = 0
notes = []


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def close(a, b, t=1e-9):
    return abs(float(a) - float(b)) <= t


SETS = {n: json.load(open(f'app/content/courses/exp-log/problems-{n}.json')) for n in (1, 2, 3)}


def part(n, item, i):
    it = next(x for x in SETS[n]['items'] if x['id'] == item)
    return it['parts'][i - 1]


def bisect(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(lo) > 0) == (f(mid) > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


ln, log10, e = math.log, math.log10, math.exp

# ---------------------------------------------------------------------------------------------------------------
# MINE[(set, item, part)] = (answer route 1, answer route 2, {wrong id: rebuilt slip}, [accept], [refuse])
# percentage parts hold fractions, as the content does; accept and refuse lists are in the stored unit too.
# ---------------------------------------------------------------------------------------------------------------
M = {}

# ---- set 1 -----------------------------------------------------------------------------------------------------
M[1, 'p-yeast-culture', 2] = (sp.Integer(3000) * sp.Rational(1, 4), 3000 / 2 / 2,
                              {'negative': 3000 * -2 * 2, 'one-hour': 3000 / 2, 'forwards': 3000 * 2 * 2}, [750], [751, 749])
M[1, 'p-yeast-culture', 3] = (3000 * sp.sqrt(2), bisect(lambda g: g * g - 2, 1, 2) * 3000,
                              {'halfway': (3000 + 6000) / 2, 'times-half': 3000 * (2 * 0.5), 'halved': 3000 * 0.5,
                               'base-times': math.sqrt(6000)}, [4243, 4242, 4242.64, 4242.6, 3000 * 1.414, 3000 * 1.4142],
                              [4241, 4245, 4200, 3000 * 1.41, 3000 * 1.4])
M[1, 'p-yeast-culture', 4] = (sp.Rational(1, 2) - (-2), math.log2(3000 * math.sqrt(2) / 750),
                              {'added-powers': 0.5 + -2, 'divided-powers': 0.5 / -2, 'ratio': 2 ** 2.5}, [2.5], [2, 3, 2.4])
M[1, 'p-laptop-value', 1] = (1 - sp.Rational(25, 100), (1200 - 300) / 1200, {'loss': 0.25, 'rise': 1.25}, [0.75], [0.7, 0.8])
v = 1200
for _ in range(2):
    v -= v / 4
M[1, 'p-laptop-value', 2] = (1200 * sp.Rational(3, 4) ** 2, v,
                             {'steady': 1200 - 2 * 300, 'one-year': 900, 'loss-factor': 1200 * 0.25 ** 2,
                              'rise-factor': 1200 * 1.25 ** 2}, [675], [674, 676])
for _ in range(2):
    v -= v / 4
M[1, 'p-laptop-value', 3] = (675 * sp.Rational(5625, 10000), v,
                             {'steady': 675 - (1200 - 675), 'one-year': 675 * 0.75, 'halved': 675 / 2},
                             [379.69, 379.6875], [379.7, 379.68, 380])
M[1, 'p-laptop-value', 4] = ((1200 - sp.Rational(37969, 100)) / 1200, 1 - 0.75 ** 4,
                             {'added': 4 * 0.25, 'kept': 0.75 ** 4, 'one-short': 1 - 0.75 ** 3, 'decimal': 0.6836 / 100},
                             [0.6836], [0.684, 0.68, 0.6835, 0.6837])
M[1, 'p-rare-coin', 1] = (sp.Rational(1000, 640), 1000 / 640, {'inverted': 640 / 1000, 'rise': (1000 - 640) / 640},
                          [1.5625], [1.56, 1.563, 1.6])
M[1, 'p-rare-coin', 2] = (sp.sqrt(sp.Rational(15625, 10000)), bisect(lambda g: g * g - 1.5625, 1, 2),
                          {'halved-factor': 1.5625 / 2, 'halved-rise': 1 + 0.5625 / 2, 'squared': 1.5625 ** 2}, [1.25], [1.2, 1.3])
M[1, 'p-rare-coin', 3] = (sp.Rational(5, 4) - 1, (800 - 640) / 640,
                          {'factor': 1.25, 'halved-rise': 0.5625 / 2, 'decimal': 0.25 / 100}, [0.25], [0.2, 0.3])
M[1, 'p-rare-coin', 4] = (1000 * sp.Rational(5, 4) ** sp.Rational(3, 2), 1250 * bisect(lambda g: g * g - 1.25, 1, 2),
                          {'halfway': (1250 + 1562.5) / 2, 'simple': 1000 * (1 + 1.5 * 0.25), 'one-year': 1250,
                           'two-years': 1562.5, 'carried': 1000 * 1.28125 ** 1.5},
                          [1398, 1397.54, 1397, 1250 * 1.118, 1000 * 1.3975], [1400, 1395, 1390])
M[1, 'p-curve-point', 1] = (sp.root(64, 3), bisect(lambda a: a ** 3 - 64, 1, 64),
                            {'divided': 64 / 3, 'square-root': math.sqrt(64)}, [4], [3, 5])
M[1, 'p-curve-point', 2] = (sp.log(2) / sp.log(4), bisect(lambda h: 4 ** h - 2, 0, 1),
                            {'factor': 2, 'quarter': 0.25, 'one': 1}, [0.5], [0.4, 0.6])
M[1, 'p-curve-point', 3] = (sp.log(2048) / sp.log(4), 3 + 0.5 * math.log2(2048 / 64),
                            {'step-one': 3 + 5 * 1, 'counted-ratio': 3 + 32 * 0.5, 'distance-only': 2.5, 'step-two': 3 + 5 * 2},
                            [5.5], [5, 6])
M[1, 'p-curve-point', 4] = (sp.log(2048) / sp.log(sp.Rational(1, 4)), bisect(lambda x: 0.25 ** x - 2048, -10, 0),
                            {'no-flip': 5.5, 'reciprocal': 1 / 5.5}, [-5.5], [-5, -6])

# ---- set 2 -----------------------------------------------------------------------------------------------------


def checks_needed(n):
    k = 0
    while 2 ** k < n:
        k += 1
    return k


def halvings(n):
    k = 0
    while n > 1:
        n = math.ceil(n / 2)
        k += 1
    return k


M[2, 'p-fault-search', 1] = (sp.log(2048, 2), halvings(2048), {'halved': 2048 / 2, 'off-by-one': 10}, [11], [12])
ok(checks_needed(2048) == 11, 'fault 1 by the prose rule')
M[2, 'p-fault-search', 2] = (sp.log(32 * 2048, 2), halvings(32 * 2048),
                             {'multiplied-logs': 5 * 11, 'times-batches': 32 * 11, 'added-count': 32 + 11, 'carried': 5 + 10},
                             [16], [17])
M[2, 'p-fault-search', 3] = (sp.ceiling(sp.log(327680, 2)), halvings(327680),
                             {'rounded-down': 18, 'added-five': 16 + 5, 'times-five': 16 * 5}, [19], [20])
ok(checks_needed(327680) == 19 and 5 * 65536 == 327680 and 2 ** 18 == 262144 and 2 ** 19 == 524288, 'fault 3 facts')
L2 = 0.30103
M[2, 'p-forty-doublings', 1] = (40 * sp.Rational(30103, 100000), float(mp.log10(mp.mpf(2) ** 40)),
                                {'swapped': log10(40 ** 2), 'added': 40 + L2}, [12.0412, 12.04120], [12.041, 12.04, 12.0411])
M[2, 'p-forty-doublings', 2] = (sp.floor(sp.log(2 ** 40, 10)), len(str(2 ** 40)) - 1,
                                {'rounded-up': 13, 'power': 40, 'carried': math.floor(log10(1600))}, [12], [])
M[2, 'p-forty-doublings', 3] = (sp.Float(10) ** sp.Rational(412, 10000), 2 ** 40 / 10 ** 12,
                                {'fraction-part': 0.0412, 'one-plus': 1.0412}, [1.10, 1.0995, 1.1], [1.09, 1.11, 1.0])
ok(2 ** 40 == 1099511627776, '2^40 printed')
M[2, 'p-forty-doublings', 4] = (sp.ceiling((15 - sp.Rational(120412, 10000)) / sp.Rational(30103, 100000)),
                                next(j for j in range(100) if 2 ** (40 + j) > 10 ** 15),
                                {'rounded-down': 9, 'tenfold-steps': round(15 - 12.0412), 'total': 50}, [10], [])
ok(close(12.0412 + 9 * L2, 14.75, 0.005) and close((15 - 12.0412) / L2, 9.83, 0.005) and close(15 - 12.0412, 2.9588), 'forty 4 prose')
v = 50000
for _ in range(2):
    v *= 0.8
M[2, 'p-drawdown-recovery', 1] = (50000 * sp.Rational(4, 5) ** 2, v, {'added-falls': 50000 * 0.6, 'one-fall': 40000},
                                  [32000], [32001])
M[2, 'p-drawdown-recovery', 2] = (sp.Rational(50000, 32000) - 1, 18000 / 32000,
                                  {'two-twenties': 0.4, 'the-loss': 18000 / 50000, 'factor': 50000 / 32000,
                                   'carried': 50000 / 30000 - 1, 'decimal': 0.5625 / 100}, [0.5625], [0.56, 0.563, 0.5626])
n_true = bisect(lambda n: 1.08 ** n - 1.5625, 0, 20)
M[2, 'p-drawdown-recovery', 3] = (2 * sp.log(sp.Rational(5, 4)) / sp.log(sp.Rational(108, 100)), n_true,
                                  {'no-power': 0.09691 / 0.03342, 'inverted': 0.03342 / (2 * 0.09691), 'simple': 56.25 / 8,
                                   'carried': ln(1.4) / ln(1.08), 'divided-numbers': 1.5625 / 1.08},
                                  [5.80, 5.8, 2 * 0.09691 / 0.03342, 5.7989], [5.79, 5.81, 6])
ok(close(log10(1.25), 0.09691, 5e-6) and close(log10(1.08), 0.03342, 5e-6) and 1.25 ** 2 == 1.5625, 'drawdown 3 given logs')
m, v = 0, 32000
while v <= 50000:
    v *= 1.08
    m += 1
M[2, 'p-drawdown-recovery', 4] = (sp.ceiling(sp.Rational(580, 100)), m, {'rounded-down': 5, 'with-falls': 6 + 2}, [6], [])
ok(round(32000 * 1.08 ** 5) == 47018 and round(32000 * 1.08 ** 6) == 50780, 'drawdown 4 printed balances')
n_true = bisect(lambda n: 1.3 ** n - 25, 0, 40)
M[2, 'p-app-users', 3] = (sp.log(25) / sp.log(sp.Rational(13, 10)), n_true,
                          {'joined': ln(50000) / ln(2600), 'divided': 25 / 1.3, 'rate-only': log10(25) / log10(0.3),
                           'simple': 25 / 0.3}, [12.27, 1.3979 / 0.1139, 1.39794 / 0.11394], [12.26, 12.28, 12.3])
ok(close(log10(25), 1.39794, 5e-6) and close(log10(1.3), 0.11394, 5e-6), 'app 3 printed logs')
m, v = 0, 2000
while v <= 50000:
    v *= 1.3
    m += 1
M[2, 'p-app-users', 4] = (sp.ceiling(sp.Rational(1227, 100)), m, {'rounded-down': 12, 'joined': math.ceil(1.38)}, [13], [])
ok(round(2000 * 1.3 ** 12) == 46596 and round(2000 * 1.3 ** 13) == 60575, 'app 4 printed counts')

# ---- set 3 -----------------------------------------------------------------------------------------------------
T2 = ln(2) / 0.055
M[3, 'p-savings-doubling', 2] = (sp.log(2) / sp.Rational(55, 1000), bisect(lambda t: 2400 * e(0.055 * t) - 4800, 0, 50),
                                 {'rule-72': 72 / 5.5, 'yearly': ln(2) / ln(1.055), 'percent': ln(2) / 5.5, 'factor': 2 / 0.055},
                                 [12.60, 12.6, 0.6931 / 0.055, 0.693 / 0.055], [12.59, 12.61, 12.7, 13])
M[3, 'p-savings-doubling', 3] = (3 * sp.Float('12.60'), bisect(lambda t: 2400 * e(0.055 * t) - 19200, 0, 100),
                                 {'eight-times': 8 * 12.60, 'four': 4 * 12.60, 'two': 2 * 12.60},
                                 [37.80, 37.8, 37.81], [37.79, 37.83, 38])
M[3, 'p-savings-doubling', 4] = (2400 * sp.Integer(2) ** sp.Rational(3, 2), 2400 * e(0.055 * 18.90),
                                 {'halfway-pounds': (2400 + 19200) / 2, 'midpoint': (4800 + 9600) / 2,
                                  'years': 2400 * e(0.055 * 1.5)},
                                 [6788, 6787, 2400 * 2.8284, 2400 * e(0.055 * 18.9), 2400 * 2 ** 1.5], [6785, 6790, 6800])
M[3, 'p-weekly-target', 1] = (sum(sp.Rational(x, 1000) for x in (30, -12, 45, -20)), 0.030 - 0.012 + 0.045 - 0.020,
                              {'signs': 0.030 + 0.012 + 0.045 + 0.020, 'averaged': 0.043 / 4}, [0.043], [0.04, 0.044])
p = 40.0
for r in (0.030, -0.012, 0.045, -0.020):
    p *= e(r)
M[3, 'p-weekly-target', 2] = (40 * sp.exp(sp.Rational(43, 1000)), p,
                              {'one-plus': 40 * 1.043, 'added': 40 + 0.043, 'carried': 40 * e(0.107)},
                              [41.76, 40 * 1.04394, 41.7575], [41.75, 41.77, 41.8])
M[3, 'p-weekly-target', 3] = (sp.log(sp.Rational(45, 40)) - sp.Rational(43, 1000), ln(45 / 41.76),
                              {'simple': (45 - 41.76) / 41.76, 'from-monday': ln(45 / 40), 'inverted': ln(41.76 / 45),
                               'difference': 45 - 41.76}, [0.0748, 0.0747, round(ln(45 / 41.76), 6)], [0.075, 0.0746, 0.0749])
M[3, 'p-weekly-target', 4] = (sp.Rational(748, 10000) / 3, 0.0748 / 3,
                              {'cube-root': 0.0748 ** (1 / 3), 'times-three': 0.0748 * 3, 'carried': 0.0776 / 3},
                              [0.0249, 0.0747 / 3], [0.0248, 0.0251])
M[3, 'p-weekly-target', 5] = (sp.exp(sp.Rational(249, 10000)) - 1, e(0.0249) - 1,
                              {'log-as-simple': 0.0249, 'simple-split': 0.0776 / 3, 'decimal': 0.0252 / 100, 'e-power': e(0.0249)},
                              [0.0252, round(e(0.0249) - 1, 6)], [0.0251, 0.0253, 0.025])
k = ln(135 / 15) / 8
M[3, 'p-log-chart-line', 1] = (sp.log(9) / 8, bisect(lambda k: 15 * e(8 * k) - 135, 0, 1),
                               {'simple-total': (135 - 15) / 15 / 8, 'ratio-over-years': 9 / 8, 'yearly-factor': 9 ** (1 / 8) - 1,
                                'log10': log10(9) / 8, 'decimal': 0.2747 / 100}, [0.2747, 2.1972 / 8], [0.275, 0.27, 0.2746, 0.2748])
M[3, 'p-log-chart-line', 2] = (sp.log(2) / sp.Rational(2747, 10000), bisect(lambda t: e(0.2747 * t) - 2, 0, 10),
                               {'rule-72': 72 / 27.47, 'inverse': 1 / 0.2747, 'percent': ln(2) / 27.47, 'tripling': ln(3) / k},
                               [2.52, 0.6931 / 0.2747, ln(2) / k], [2.51, 2.53, 2.5])
M[3, 'p-log-chart-line', 3] = (sp.sqrt(15 * 135), 15 * 2 ** (4 / 2.52),
                               {'pounds-midpoint': (15 + 135) / 2, 'whole-doublings': 15 * 2, 'rounded-up': 15 * 4},
                               [45, 15 * 2 ** 1.59, 15 * 2 ** 1.587, 15 * 2 ** (4 / 2.52), 15 * e(0.2747 * 4)], [44, 46])
M[3, 'p-log-chart-line', 4] = (12 * sp.log(3) / sp.log(9), 12 * ln(45 / 15) / ln(135 / 15),
                               {'pounds': 12 * (45 - 15) / (135 - 15), 'ratio': 12 * 45 / 135}, [6], [5, 7])
v = 1.0
for _ in range(12):
    v *= 1.004
M[3, 'p-monthly-deposit', 1] = (sp.Rational(1004, 1000) ** 12, v,
                                {'once': 1.048, 'continuous': e(0.048), 'whole-rate': 1.048 ** 12}, [1.0491, 1.04907],
                                [1.049, 1.0490, 1.0492, 1.05])
M[3, 'p-monthly-deposit', 2] = (12 * sp.log(sp.Rational(1004, 1000)), ln(1.0491),
                                {'quoted': 0.048, 'factor-rate': 1.0491 - 1, 'decimal': 0.0479 / 100, 'log10': log10(1.0491)},
                                [0.0479, round(ln(1.0491), 6)], [0.048, 0.0478, 0.047])
M[3, 'p-monthly-deposit', 3] = (5 * sp.Rational(479, 10000), 5 * 0.0479,
                                {'quoted': 5 * 0.048, 'simple': 1.0491 ** 5 - 1, 'one-year': 0.0479}, [0.2395], [0.24, 0.239, 0.2397])
v = 6000.0
for _ in range(60):
    v *= 1.004
M[3, 'p-monthly-deposit', 4] = (6000 * sp.exp(sp.Rational(2395, 10000)), v,
                                {'one-plus': 6000 * 1.2395, 'quoted': 6000 * e(0.24), 'simple-interest': 6000 * (1 + 5 * 0.048)},
                                [7624, 6000 * e(0.2395), 6000 * 1.2706, 7623.84], [7623, 7625, 7620, 7627])

# two routes may differ where one starts from a rounded carried value: the allowed gap, by part
GAP = {(3, 'p-savings-doubling', 3): 0.01, (3, 'p-savings-doubling', 4): 1.5, (3, 'p-weekly-target', 3): 1e-4,
       (3, 'p-weekly-target', 5): 1e-4, (3, 'p-log-chart-line', 2): 1e-3, (3, 'p-log-chart-line', 3): 0.1,
       (3, 'p-monthly-deposit', 2): 5e-5, (3, 'p-monthly-deposit', 3): 1e-4, (3, 'p-monthly-deposit', 4): 0.2,
       (2, 'p-forty-doublings', 1): 1e-5, (2, 'p-forty-doublings', 3): 1e-4, (1, 'p-yeast-culture', 3): 1e-6,
       (1, 'p-laptop-value', 4): 1e-5, (2, 'p-drawdown-recovery', 3): 1e-6, (2, 'p-app-users', 3): 1e-6}

seen = 0
for n, d in SETS.items():
    for it in d['items']:
        for i, p in enumerate(it['parts'], 1):
            w = p['widget']
            if w['kind'] != 'numeric':
                continue
            key = (n, it['id'], i)
            ok(key in M, f'{key}: no reader answer')
            if key not in M:
                continue
            seen += 1
            a1, a2, slips, acc, ref = M[key]
            a1 = float(sp.N(a1, 20))
            tol = w['tol']['abs']
            ok(close(a1, a2, GAP.get(key, 1e-9)), f'{key}: my two routes differ {a1} {a2}')
            inband = lambda x: abs(x - w['answer']) <= tol + 1e-12
            ok(inband(a1) and inband(float(a2)), f'{key}: key {w["answer"]} ±{tol} against mine {a1}, {a2}')
            for x in acc:
                ok(inband(x), f'{key}: sensible entry {x} refused (key {w["answer"]} ±{tol})')
            for x in ref:
                ok(not inband(x), f'{key}: entry {x} accepted (key {w["answer"]} ±{tol})')
            ids = [x['id'] for x in w.get('wrong', [])]
            ok(sorted(ids) == sorted(slips), f'{key}: wrong ids {ids} against mine {sorted(slips)}')
            bands = [(w['answer'] - tol, w['answer'] + tol, 'answer')]
            for x in w.get('wrong', []):
                t = x.get('tol', w['tol'])['abs']
                if x['id'] in slips:
                    ok(abs(float(slips[x['id']]) - x['value']) <= t + 1e-12,
                       f'{key}: wrong {x["id"]}={x["value"]} ±{t}, the slip gives {float(slips[x["id"]]):.6g}')
                bands.append((x['value'] - t, x['value'] + t, x['id']))
            for a in range(len(bands)):
                for b in range(a + 1, len(bands)):
                    ok(bands[a][1] < bands[b][0] or bands[b][1] < bands[a][0], f'{key}: bands {bands[a][2]} and {bands[b][2]} overlap')

ok(seen == len(M), f'{len(M)} reader rows, {seen} numeric parts')

# ---- claims and printed numbers beyond the keys ------------------------------------------------------------------
ok(close(2 ** 2.5, 5.66, 0.005) and close(4243 / 750, 5.66, 0.005), 'yeast 4 check line')
ok(close(0.75 ** 4, 0.3164, 5e-5) and close(1 - 0.75 ** 3, 0.5781, 5e-5) and close(1200 - 379.69, 820.31), 'laptop 4 prose')
ok(640 * 1.25 == 800 and 800 * 1.25 == 1000, 'coin 2 check line')
ok(close(1.25 ** 0.5, 1.118, 5e-4) and close(1.25 ** 1.5, 1.39754, 5e-6), 'coin 4 prose')
ok(4 ** 5.5 == 2048 == 2 ** 11 and close(4 ** 0.25, 1.414, 5e-4) and close(4 ** -5.5, 1 / 2048), 'curve prose')
ok(close(32000 * 1.2 ** 2, 46080), 'drawdown 2 two twenties')
ok(close(ln(2), 0.6931, 5e-5) and close(e(0.043), 1.04394, 5e-6) and close(ln(1.125), 0.1178, 5e-5), 'set 3 printed logs')
ok(close(ln(9), 2.1972, 5e-5) and close(4 / 2.52, 1.587, 5e-4) and close(2 ** 1.587, 3.00, 0.005), 'chart prose')
ok(close(e(0.048), 1.0492, 5e-5) and close(e(0.2395), 1.2706, 5e-5) and close(6000 * e(0.2395), 7623.68, 0.005), 'deposit prose')
ok(close(6000 * 1.004 ** 60, 7623.84, 0.005) and close(1.0491 ** 5 - 1, 0.2708, 5e-5), 'deposit check lines')
ok(close(2400 * 16, 38400) and close(2400 * 4, 9600), 'savings 3 feedback')
ok(close(9 ** (1 / 8) - 1, 0.3161, 5e-5), 'chart 1 yearly rate')
# is the weekly target met? three weeks at 2.52% from 41.76
ok(close(41.76 * 1.0252 ** 3, 45, 0.01), 'weekly: three weeks at 2.52% reach 45')

# ---- reader's notes (findings; printed, not failures) ------------------------------------------------------------
notes.append(f"weekly 3: ln(45/41.76) = {ln(45 / 41.76):.6f} -> 0.0747 from the value the question names; key headline 0.0748")
notes.append(f"weekly 5: e^0.0249 - 1 = {e(0.0249) - 1:.6f}; key 0.025241 is e^(0.0748/3) - 1; 2.52 typed is {abs(0.0252 - 0.025241):.2e} from the key, tol 5e-05")
notes.append(f"savings 4: 2400e^(0.055 x 18.9) = {2400 * e(0.055 * 18.9):.2f}; 2400 x 2^1.5 = {2400 * 2 ** 1.5:.2f}")
notes.append(f"savings 4 wrong 'years': 2400e^(0.055 x 1.5) = {2400 * e(0.0825):.2f}, 2400 x 2^(1.5/12.6) = {2400 * 2 ** (1.5 / 12.6):.2f}; keyed 2606.2")
notes.append(f"coin 4: band 1397.54 ± 1.5 takes 1399: {abs(1399 - 1397.54) <= 1.5}")
notes.append(f"chart 3: 15 x 2^1.59 = {15 * 2 ** 1.59:.2f}, 15 x 2^1.6 = {15 * 2 ** 1.6:.2f}, 15 x 2^1.5 = {15 * 2 ** 1.5:.2f}")
notes.append(f"deposit 3 wrong 'simple': 1.0491^5 - 1 = {1.0491 ** 5 - 1:.5f}, 1.004^60 - 1 = {1.004 ** 60 - 1:.5f}; keyed 0.2707 ± 0.0002")
notes.append('savings 3: band 37.808 ± 0.015 also takes 37.82; deposit 3: band 0.239521 ± 0.0001 also takes 0.2396 (loose, harmless)')
for s in notes:
    print('NOTE', s)
print(f'parts with a reader answer: {len(M)}; checks: {checks}; failures: {fails}')
sys.exit(1 if fails else 0)
