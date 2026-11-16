#!/usr/bin/env python3
"""Second reader's recompute of app/content/courses/convex/problems-4.json.

Imports nothing from the author's script. Every key, every `wrong` value and
every number printed in a question, feedback or explain line is rebuilt here,
by exact fractions or sympy first and then by a simulated run in floats.
Exit 0 always; a check that fails on the content prints a FINDING line
(docs/reviews/review-problems-convex-4.md). Pass another content file as
argv[1] to check a copy.
"""
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    HERE, '..', '..', 'app', 'content', 'courses', 'convex', 'problems-4.json')
SET = json.load(open(PATH, encoding='utf-8'))
ITEMS = {it['id']: it for it in SET['items']}

n_checks = 0
n_fail = 0
findings = []


def check(name, ok):
    global n_checks, n_fail
    n_checks += 1
    if not ok:
        n_fail += 1
        print('FAIL', name)


def finding(num, text):
    findings.append((num, text))


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def band(w):
    t = w.get('tol', {}).get('abs', 0)
    return (w['value'] if 'value' in w else w['answer']) - t, (w['value'] if 'value' in w else w['answer']) + t


def part(item, k):
    return ITEMS[item]['parts'][k]


def key(item, k):
    return part(item, k)['widget']['answer']


def wrong(item, k, wid):
    for w in part(item, k)['widget']['wrong']:
        if w['id'] == wid:
            return w
    raise KeyError(wid)


def takes(item, k, value):
    w = part(item, k)['widget']
    return abs(value - w['answer']) <= w['tol']['abs'] + 1e-12


def text_of(item, k):
    p = part(item, k)
    out = [p['question'], p['explain']['text']]
    fb = p['feedback']
    out += [fb['correct'], fb['generic']] + list(fb.get('byKey', {}).values())
    for o in p['widget'].get('options', []):
        out += [o['text'], o.get('why', '')]
    return ' '.join(out)


def has(item, k, s):
    return s in text_of(item, k)


def bands_disjoint(item, k):
    w = part(item, k)['widget']
    if w['kind'] != 'numeric':
        return True
    lo, hi = w['answer'] - w['tol']['abs'], w['answer'] + w['tol']['abs']
    spans = [(lo, hi)] + [band(x) for x in w.get('wrong', [])]
    spans.sort()
    return all(spans[i][1] < spans[i + 1][0] for i in range(len(spans) - 1))


# ---------------------------------------------------------------- structure
check('three to five items', 3 <= len(SET['items']) <= 5)
check('a difficulty 5', any(it['difficulty'] == 5 for it in SET['items']))
n_parts = sum(len(it['parts']) for it in SET['items'])
n_typed = sum(p['widget']['kind'] in ('numeric', 'expression') for it in SET['items'] for p in it['parts'])
check('typed share at least two thirds', 3 * n_typed >= 2 * n_parts)
for it in SET['items']:
    check(it['id'] + ' parts 3 to 5', 3 <= len(it['parts']) <= 5)
    check(it['id'] + ' skills of the level', set(it['skills']) <= {'cv-descent', 'cv-duality'})
    for k, p in enumerate(it['parts']):
        check('%s part %d bands disjoint' % (it['id'], k + 1), bands_disjoint(it['id'], k))
        if p['widget']['kind'] == 'numeric':
            check('%s part %d states a form' % (it['id'], k + 1),
                  any(s in p['question'] for s in ('decimal', 'whole number', 'nearest pound')))
            ids = [w['id'] for w in p['widget'].get('wrong', [])]
            check('%s part %d each slip has a line' % (it['id'], k + 1),
                  set(ids) == set(p['feedback'].get('byKey', {}).keys()))

# ------------------------------------------------------------ A. curve fit
A = 'p-curve-fit-backtrack'   # parts 1 and 2 kept from p-curve-fit-log
s0 = F(1, 20)
lam = sp.symbols('lam')
lam_d = sp.solve(sp.Eq(1 - sp.Rational(1, 20) * lam, sp.Rational(96, 100)), lam)[0]
lam_l = sp.solve(sp.Eq(1 - sp.Rational(1, 20) * lam, sp.Rational(-1, 2)), lam)[0]
check('A1 key 0.8', sp.Rational(4, 5) == lam_d and close(key(A, 0), 0.8))
check('A2 key 30', lam_l == 30 and key(A, 1) == 30)
# second route: run descent on the bowl with those curvatures and read the factors off the run
x = np.array([1.0, 1.0])
H = np.array([0.8, 30.0])
x1 = x - 0.05 * H * x
check('A stem factors from a run', close(x1[0], 0.96) and close(x1[1], -0.5))
check('A1 wrong factor-over-s', close(wrong(A, 0, 'factor-over-s')['value'], 0.96 / 0.05))
check('A1 wrong no-divide', close(wrong(A, 0, 'no-divide')['value'], 1 - 0.96))
check('A2 wrong sign', wrong(A, 1, 'sign')['value'] == (1 - F(1, 2)) / s0)
check('A2 wrong times-s', close(wrong(A, 1, 'times-s')['value'], 1.5 * 0.05))
check('A1 printed 0.04', has(A, 0, '0.05\\lambda = 0.04') and has(A, 0, '0.04/0.05 = 0.8'))
check('A2 printed 1.5', has(A, 1, '0.05\\lambda = 1.5') and has(A, 1, '1.5/0.05 = 30'))
lo, hi = band(wrong(A, 1, 'times-s'))
if lo <= 0.5 <= hi or lo <= 0.04 <= hi:
    finding(2, 'p-curve-fit-log part 2: slip band times-s is %.3f to %.3f, so 0.5 and 0.04 are told "You multiplied 1.5 by the step"' % (lo, hi))

# Parts 3 to 5 of p-curve-fit-log (best step, its factor, the steps saved) were removed when the main session
# ruled the problem a re-author; their checks (A3 to A5, findings 3 to 5) are removed with them. The new parts 3 to 5
# of p-curve-fit-backtrack are checked in problems-convex-numbers.py; a delta reader adds its own route here.
check('A2 times-s band tightened to 0.0005 (finding 2)', wrong(A, 1, 'times-s')['tol']['abs'] == 0.0005)

# --------------------------------------------------------- B. sale horizon
B = 'p-sale-horizon'
T = sp.symbols('T', positive=True)
f = 8 / T + 2 * T
f1 = sp.diff(f, T)
f2 = sp.diff(f, T, 2)
check('B stem derivatives', sp.simplify(f1 - (2 - 8 / T**2)) == 0 and sp.simplify(f2 - 16 / T**3) == 0)
check('B curvature falls on T >= 1', sp.diff(f2, T).subs(T, 1) < 0 and all(sp.diff(f2, T).subs(T, v) < 0 for v in (1, 2, 5, 50)))
L = f2.subs(T, 1)
check('B1 key', L == 16 and close(key(B, 0), 2 / 16))
check('B1 wrong one-over-l', close(wrong(B, 0, 'one-over-l')['value'], 1 / 16))
check('B1 wrong curvature-at-min', close(wrong(B, 0, 'curvature-at-min')['value'], 2 / f2.subs(T, 2)))
check('B best horizon', sp.solve(f1, T) == [2] and f2.subs(T, 2) == 2)


def fd(t):
    return 2 - 8 / t**2


def fdd(t):
    return 16 / t**3


def fv(t):
    return 8 / t + 2 * t


# claim "any step below 2/16 settles": runs from both sides, just under the bound
for s in (0.01, 0.0625, 0.1249):
    for t0 in (1.0, 3.0, 60.0):
        t = t0
        ok = True
        for _ in range(60000):
            t = t - s * fd(t)
            if t < 1 - 1e-12:
                ok = False
        check('B1 claim: s=%.4f from %.0f stays in the region and settles' % (s, t0), ok and abs(t - 2) < 1e-6)

t1 = F(1) - F(1, 16) * (2 - 8)
check('B2 key', t1 == F(11, 8) and close(key(B, 1), 1.375))
check('B2 wrong sign', close(wrong(B, 1, 'sign')['value'], 1 + (1 / 16) * (-6)))
check('B2 wrong limit-step', close(wrong(B, 1, 'limit-step')['value'], 1 - (2 / 16) * (-6)))
check('B2 Newton lands on the same point', 1 - fd(1.0) / fdd(1.0) == 1.375)

t1f = F(11, 8)
g = 2 - 8 / t1f**2
h = 16 / t1f**3
t2 = t1f - g / h
check('B3 printed slope and curvature', round(float(g), 4) == -2.2314 and round(float(h), 4) == 6.1548 and round(float(-g / h), 4) == 0.3625)
check('B3 key', round(float(t2), 4) == key(B, 2) and takes(B, 2, float(t2)))
check('B3 key from the printed 4-place values', takes(B, 2, 1.375 + 2.2314 / 6.1548))
t2_desc = t1f - F(1, 16) * g
check('B3 wrong descent', round(float(t2_desc), 4) == wrong(B, 2, 'descent')['value'])
check('B3 wrong sign', round(float(t1f + g / h), 4) == wrong(B, 2, 'sign')['value'])
check('B3 Newton step longer than descent step', -g / h > -g / 16)
# second route: Newton by a float loop from 1
t = 1.0
seq = []
for _ in range(2):
    t = t - fd(t) / fdd(t)
    seq.append(t)
check('B3 float loop', close(seq[0], 1.375) and abs(seq[1] - float(t2)) < 1e-12)

extra_told = (fv(1.7375) - fv(2.0)) * 1000
extra_exact = (fv(float(t2)) - 8) * 1000
check('B4 key', takes(B, 3, extra_told) and takes(B, 3, extra_exact) and round(extra_told) == key(B, 3) == 79)
check('B4 printed 8.0793', round(fv(1.7375), 4) == 8.0793 and round(fv(float(t2)), 4) == 8.0793)
check('B4 wrong descent', abs((fv(1.5145) - 8) * 1000 - wrong(B, 3, 'descent')['value']) < 0.5)
check('B4 wrong total', round(fv(1.7375) * 1000) == wrong(B, 3, 'total')['value'])
check('B4 wrong start', round((fv(1.375) - 8) * 1000) == wrong(B, 3, 'start')['value'])
check('B4 wrong thousands', round(fv(1.7375) - 8, 4) == wrong(B, 3, 'thousands')['value'] and wrong(B, 3, 'thousands')['tol']['abs'] == 0.005)
check('B4 excess at T=1 is 2000', (fv(1.0) - 8) * 1000 == 2000)
if has(B, 3, '4.6042 + 3.4751') and (round(8 / 1.7375, 4), round(2 * 1.7375, 4)) != (4.6042, 3.4751):
    finding(9, 'p-sale-horizon part 4: feedback prints 4.6042 + 3.4751, the terms at the unrounded T2; at the 1.7375 the part restates they are %.4f + %.4f (the explain line has 3.475)' % (8 / 1.7375, 2 * 1.7375))
lo, hi = band(wrong(B, 3, 'thousands'))
if lo <= 0.3113 <= hi or lo <= 0.5682 <= hi:
    finding(10, 'p-sale-horizon part 4: slip band thousands is %.3f to %.3f, so 0.311 and 0.568 (the descent and start slips in £k) are told "0.0793 is the extra cost in £k"' % (lo, hi))

# --------------------------------------------------------- C. variance log
C = 'p-variance-log'
V = [F(2004096, 10000), F(2003136, 10000), F(2002401, 10000)]
for v in ('200.4096', '200.3136', '200.2401'):
    check('C stem value ' + v, v in ITEMS[C]['prose'])
d1, d2 = V[0] - V[1], V[1] - V[2]
check('C1 drops', d1 == F(96, 1000) and d2 == F(735, 10000))
r2 = d2 / d1
check('C1 rho squared', r2 == F(49, 64) and float(r2) == 0.765625)
check('C1 key', F(7, 8) ** 2 == r2 and close(key(C, 0), 0.875))
check('C1 wrong ratio', abs(float(r2) - wrong(C, 0, 'ratio')['value']) <= 0.00005 + 1e-12)
check('C1 wrong one-minus', abs(float(1 - r2) - wrong(C, 0, 'one-minus')['value']) <= 0.00005)
check('C1 slips typed to 3 places reach their lines',
      band(wrong(C, 0, 'ratio'))[0] <= 0.766 <= band(wrong(C, 0, 'ratio'))[1]
      and band(wrong(C, 0, 'one-minus'))[0] <= 0.234 <= band(wrong(C, 0, 'one-minus'))[1])
check('C1 kappa 15', (1 + F(7, 8)) / (1 - F(7, 8)) == 15 and has(C, 0, '1.875/0.125 = 15'))

e22 = d2 * r2 / (1 - r2)
vstar = V[2] - e22
check('C2 key', e22 == F(2401, 10000) and vstar == 200 and close(key(C, 1), 200))
# second route: Aitken's delta-squared on the three logged values
aitken = V[2] - (V[2] - V[1]) ** 2 / (V[2] - 2 * V[1] + V[0])
check('C2 Aitken', aitken == 200)
check('C2 the three excesses are squares', [v - 200 for v in V] == [F(64, 100) ** 2, F(56, 100) ** 2, F(49, 100) ** 2])
check('C2 wrong no-extrapolation', close(wrong(C, 1, 'no-extrapolation')['value'], float(V[2])))
e_rho = d2 * F(7, 8) / (1 - F(7, 8))
check('C2 wrong used-rho', e_rho == F(5145, 10000) and close(wrong(C, 1, 'used-rho')['value'], float(V[2] - e_rho)))
check('C2 wrong one-step-back', close(wrong(C, 1, 'one-step-back')['value'], float(V[2] - (V[1] - 200))))
check('C2 printed 0.234375', 1 - r2 == F(234375, 1000000))

# third route: a real run. Three funds, budget removed by substitution, best fixed step, kappa 15.
rng = np.random.default_rng(20261116)
Q, _ = np.linalg.qr(rng.normal(size=(2, 2)))
Hred = Q @ np.diag([2.0, 30.0]) @ Q.T          # reduced Hessian, eigenvalues 2 and 30
step = 2 / 32
z = np.array([3.0, -1.5])
exc = []
for _ in range(30):
    exc.append(0.5 * z @ Hred @ z)
    z = z - step * (Hred @ z)
ratios = [exc[i + 1] / exc[i] for i in range(len(exc) - 1)]
check('C stem claim: excess falls by exactly rho^2 at the best step', max(abs(r - 0.765625) for r in ratios) < 1e-9)
drops = [exc[i] - exc[i + 1] for i in range(len(exc) - 1)]
check('C1 claim: drops shrink by rho^2 too', max(abs(drops[i + 1] / drops[i] - 0.765625) for i in range(len(drops) - 1)) < 1e-8)

n_more = 0
e = F(2401, 10000)
while e > F(1, 10000):
    e *= r2
    n_more += 1
check('C3 key by loop', n_more == key(C, 2) == 30)
q3 = math.log(2401) / math.log(1 / 0.765625)
check('C3 printed 29.15, 1.306', round(q3, 2) == 29.15 and round(1 / 0.765625, 3) == 1.306)
check('C3 wrong floor', wrong(C, 2, 'floor')['value'] == 29 and round(0.2401 * 0.765625**29 * 1e4, 2) == 1.04)
check('C3 wrong used-rho', math.ceil(math.log(2401) / math.log(1 / 0.875)) == wrong(C, 2, 'used-rho')['value'] == 59)
check('C3 ends at step 52', 22 + 30 == 52 and has(C, 2, 'step 52'))
check('C3 excess after 30 steps', round(0.2401 * 0.765625**30 * 1e5, 2) == 7.96)

gap = V[2] - F(19995, 100)
check('C4 gap', gap == F(2901, 10000) and has(C, 3, '0.2901'))
opts = part(C, 3)['widget']['options']
check('C4 one keyed option', [o['id'] for o in opts if o.get('correct')] == ['bracket'])
check('C4 dual value under V*', F(19995, 100) <= 200 <= V[2])
check('C4 drop per step below 0.1', d2 < F(1, 10) and d1 < F(1, 10))
why_extra = next(o for o in opts if o['id'] == 'extrapolated').get('why', '')
if 'exactly' in ITEMS[C]['prose'] and 'holding exactly' in why_extra:
    finding(15, 'p-variance-log part 4: the stem says the excess "falls by exactly rho^2 a step", and the distractor is refused because 200.00 "rests on the ratio holding exactly"')

# ------------------------------------------------- reuse lines (by reading)
REUSE = [
    (1, A, 1, 'the step overshoots the floor'),
    (6, B, 0, 'is a safe choice of step, not the limit'),
    (6, B, 0, 'must hold over the whole region'),
    (7, B, 1, 'You moved with the gradient'),
    (8, B, 2, "You added $f'/f''$."),
    (8, B, 2, 'Newton divides by the curvature'),
    (11, C, 0, 'the share of the excess removed each step'),
    (12, C, 2, 'for the smallest whole $n$'),
    (12, C, 2, 'still above the tolerance'),
    (13, C, 3, 'a floor under $V^*$'),
    (13, C, 3, 'lies between 199.95 and 200.2401'),
    (13, C, 3, 'The run is slow, not wrong'),
    (13, C, 3, 'is a ceiling on $V^*$'),
]
for num, item, k, s in REUSE:
    if has(item, k, s):
        finding(num, '%s part %d still carries the course line "%s"' % (item, k + 1, s))

print('problems-convex-4-numbers-read: %d checks, %d failed' % (n_checks, n_fail))
for num, text in sorted(findings):
    print('FINDING %d: %s' % (num, text))
sys.exit(0)
