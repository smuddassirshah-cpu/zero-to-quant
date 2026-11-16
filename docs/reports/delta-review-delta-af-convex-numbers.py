#!/usr/bin/env python3
"""Delta read AF, convex problem sets 1 to 4: independent recompute.

Scope: the three new problems (p-account-target, p-style-fit, p-curve-fit-backtrack)
and every part the two fix passes changed. Imports nothing from the author's or the
readers' scripts. Second routes: SLSQP and a grid in the original variables, exact
fractions, 12 months of data built from the square root of the Gram matrix, a real
backtracking loop, a fixed-step loop, linprog on the level 2 programmes.

Exit 0 always. A failing number prints FAIL and counts; a finding of the review
prints a FINDING line while the content still carries it and `resolved` once fixed.
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog, minimize, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
SETS = os.environ.get('ZQ_CONVEX_DIR') or os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'convex')
COURSE = SETS
n_checks = 0
n_fail = 0
n_find = 0


def load(n):
    with open(os.path.join(SETS, 'problems-%d.json' % n), encoding='utf-8') as fh:
        return json.load(fh)


def item(n, pid):
    for it in load(n)['items']:
        if it['id'] == pid:
            return it
    raise KeyError(pid)


def check(name, cond):
    global n_checks, n_fail
    n_checks += 1
    if not cond:
        n_fail += 1
        print('FAIL', name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def finding(num, present, text):
    global n_checks, n_find
    n_checks += 1
    if present:
        n_find += 1
        print('FINDING %s: %s' % (num, text))
    else:
        print('finding %s resolved' % num)


def strings(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def text_of(it):
    return '\n'.join(strings(it))


def has(it, s):
    return s in text_of(it)


# ---- the engine's numeric rule (app/js/engine/grade.js numGrade): a bare number is
# divided by 100 when unit is "%", and every absolute band has 1e-9 of slack.
def typed(w, s):
    v = float(s.rstrip('%').strip())
    if w.get('unit') == '%':
        v = v / 100.0
    if abs(v - w['answer']) <= w['tol']['abs'] + 1e-9:
        return 'correct'
    for x in w.get('wrong', []):
        if abs(v - x['value']) <= x.get('tol', {'abs': 0})['abs'] + 1e-9:
            return x['id']
    return 'generic'


def bands(tag, w):
    """key band takes the key, refuses every slip; slip bands are disjoint."""
    k, t = w['answer'], w['tol']['abs']
    ws = w.get('wrong', [])
    for x in ws:
        xt = x.get('tol', {'abs': 0})['abs']
        check('%s slip %s clear of the key band' % (tag, x['id']), abs(x['value'] - k) > t + xt + 1e-9)
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            a, b = ws[i], ws[j]
            check('%s slips %s and %s disjoint' % (tag, a['id'], b['id']),
                  abs(a['value'] - b['value']) > a.get('tol', {'abs': 0})['abs'] + b.get('tol', {'abs': 0})['abs'] + 1e-9)


def wrongs(w):
    return {x['id']: x['value'] for x in w.get('wrong', [])}


# =====================================================================
# A. problems-1 p-account-target
# =====================================================================
A = item(1, 'p-account-target')
pa = A['parts']

# part 1: second derivative of 6 sqrt(x), by a central second difference and exactly
for x in (0.5, 1.0, 4.0, 16.0, 30.0):
    h = 1e-4 * x
    d2 = (6 * math.sqrt(x + h) - 12 * math.sqrt(x) + 6 * math.sqrt(x - h)) / h ** 2
    check('A1 second derivative at %g' % x, close(d2, -1.5 * x ** -1.5, 1e-5 * x ** -1.5 + 1e-7))
check('A1 key text', pa[0]['widget']['answer'] == r'-\frac{3}{2}x^{-3/2}')
w1 = {x['id']: x['tex'] for x in pa[0]['widget']['wrong']}
check('A1 slips', w1 == {'sign': r'\frac{3}{2}x^{-3/2}', 'first': r'3x^{-1/2}', 'power': r'-\frac{3}{2}x^{-1/2}'})

# part 2: the feasible set is convex (midpoints of 20,000 random pairs), N is concave,
# and the two counterexamples in the distractors do what the lines say
rng = np.random.default_rng(20261116)
N = lambda x, y: 6 * np.sqrt(x) + 3 * np.sqrt(y)
P = rng.uniform(0, 120, size=(200000, 2))
P = P[N(P[:, 0], P[:, 1]) >= 30][:40000]
a, b = P[:20000], P[20000:40000]
th = rng.uniform(0, 1, size=(20000, 1))
m = th * a + (1 - th) * b
check('A2 mixes stay in the set', bool(np.all(N(m[:, 0], m[:, 1]) >= 30 - 1e-9)))
check('A2 N concave on random chords', bool(np.all(N(m[:, 0], m[:, 1]) >= (th[:, 0] * N(a[:, 0], a[:, 1]) + (1 - th[:, 0]) * N(b[:, 0], b[:, 1])) - 1e-9)))
check('A2 rising counterexample', max(1, 0) >= 1 and max(0, 1) >= 1 and max(0.5, 0.5) < 1)
check('A2 any-ge counterexample', (-1) ** 2 >= 1 and 1 ** 2 >= 1 and 0 ** 2 < 1)
keyopt = [o['id'] for o in pa[1]['widget']['options'] if o.get('correct')]
check('A2 key option', keyopt == ['rewrite'])


def least_spend(T):
    """SLSQP in the original variables x, y, from four starts; and a boundary grid."""
    best = None
    for x0 in ((1.0, 1.0), (T, T), (T * T / 36, 0.01), (0.01, T * T / 9)):
        r = minimize(lambda z: z[0] + z[1], x0, method='SLSQP', bounds=[(1e-12, None)] * 2,
                     constraints=[{'type': 'ineq', 'fun': lambda z: 6 * math.sqrt(max(z[0], 0)) + 3 * math.sqrt(max(z[1], 0)) - T}],
                     options={'ftol': 1e-14, 'maxiter': 500})
        if r.success and 6 * math.sqrt(r.x[0]) + 3 * math.sqrt(r.x[1]) >= T - 1e-7:
            if best is None or r.fun < best[0]:
                best = (r.fun, r.x[0], r.x[1])
    u = np.linspace(0, T / 6, 600001)
    v = (T - 6 * u) / 3
    s = u ** 2 + v ** 2
    i = int(np.argmin(s))
    return best, (s[i], u[i] ** 2, v[i] ** 2)


best, grid = least_spend(30)
check('A3 SLSQP x = 16', close(best[1], 16, 1e-3) and close(best[2], 4, 1e-3))
check('A3 grid x = 16', close(grid[1], 16, 1e-3) and close(grid[2], 4, 1e-3))
check('A3 key 16', pa[2]['widget']['answer'] == 16 and pa[2]['widget']['tol']['abs'] == 0)
check('A4 SLSQP spend 20', close(best[0], 20, 1e-5) and close(grid[0], 20, 1e-8))
check('A4 key 20', pa[3]['widget']['answer'] == 20)
check('A3 on the limit', close(6 * 4 + 3 * 2, 30))
# slope printed in the feedback: d/du [u^2 + (10 - 2u)^2] = 10u - 40
for u in (0.0, 1.0, 4.0, 5.0):
    h = 1e-6
    g = ((u + h) ** 2 + (10 - 2 * (u + h)) ** 2 - (u - h) ** 2 - (10 - 2 * (u - h)) ** 2) / (2 * h)
    check('A3 slope 10u - 40 at %g' % u, close(g, 10 * u - 40, 1e-5))
# slips: gave-u 4; corner (all on search) 25; no-chain 2u + 2(10 - 2u) = 0 at u = 10
check('A3 slips', wrongs(pa[2]['widget']) == {'gave-u': 4, 'corner': 25, 'no-chain': 100})
check('A3 corner', close((30 / 6) ** 2, 25) and close((F(20, 2)) ** 2, 100))
check('A4 slips', wrongs(pa[3]['widget']) == {'search-only': 16, 'roots': 6, 'corner': 25})
bands('A3', pa[2]['widget'])
bands('A4', pa[3]['widget'])
# part 5: T^2/45 exactly, and against SLSQP at four targets
for T in (F(12), F(30), F(45), F(60)):
    u = 2 * T / 15
    v = T / 3 - 2 * u
    check('A5 exact T=%s' % T, v == T / 15 and u * u + v * v == T * T / 45 and 10 * u - 4 * T / 3 == 0)
    bs, gr = least_spend(float(T))
    check('A5 SLSQP T=%s' % T, close(bs[0], float(T * T / 45), 2e-5 * float(T * T)) and close(gr[0], float(T * T / 45), 1e-7 * float(T * T)))
check('A5 key', pa[4]['widget']['answer'] == r'\frac{T^2}{45}')
check('A5 printed values', F(30) ** 2 / 45 == 20 and F(60) ** 2 / 45 == 80 and F(2 * 30, 3) == 20
      and F(30) ** 2 / 36 == 25 and F(1, 45) < F(1, 36) < F(1, 9))
check('A5 slips', {x['id']: x['tex'] for x in pa[4]['widget']['wrong']} ==
      {'linear': r'\frac{2T}{3}', 'search-only': r'\frac{T^2}{36}', 'podcast-only': r'\frac{T^2}{9}'})

# =====================================================================
# B. problems-3 p-style-fit
# =====================================================================
B = item(3, 'p-style-fit')
pb = B['parts']
svv, svg, sgg, srv, srg, srr = F(60), F(20), F(80), F(30), F(60), F(60)
# Q and q from the expansion, exactly
Q = [[2 * svv, 2 * svg], [2 * svg, 2 * sgg]]
q = [-2 * srv, -2 * srg]
check('B1 Q12 = 40', Q[0][1] == 40 == pb[0]['widget']['answer'])
check('B1 Q, q printed', Q == [[120, 40], [40, 160]] and q == [-60, -120])
check('B1 slips', wrongs(pb[0]['widget']) == {'no-two': 20, 'double': 80})
check('B1 Q positive definite', Q[0][0] > 0 and Q[0][0] * Q[1][1] - Q[0][1] ** 2 > 0)
# the stated sums are possible: the Gram matrix of (r, v, g) is positive definite
G = np.array([[60.0, 30, 60], [30, 60, 20], [60, 20, 80]])
check('B stem Gram positive definite', bool(np.all(np.linalg.eigvalsh(G) > 0)))
# 12 months of data with exactly these sums, from the symmetric square root of G
ev, V = np.linalg.eigh(G)
R3 = (V * np.sqrt(ev)) @ V.T
X = np.zeros((12, 3))
X[:3] = R3
rot = np.linalg.qr(np.random.default_rng(7).standard_normal((12, 12)))[0]
X = rot @ X
check('B stem data reproduce the sums', bool(np.allclose(X.T @ X, G, atol=1e-9)))
r_, v_, g_ = X[:, 0], X[:, 1], X[:, 2]
Sdata = lambda bv, bg: float(np.sum((r_ - bv * v_ - bg * g_) ** 2))
Sform = lambda bv, bg: 60 - 60 * bv - 120 * bg + 60 * bv * bv + 40 * bv * bg + 80 * bg * bg
for bv, bg in ((0.3, 0.7), (0.0, 1.0), (1.0, 0.0), (0.27, 0.68), (0.5, 0.5)):
    check('B1 expanded S at (%g, %g)' % (bv, bg), close(Sdata(bv, bg), Sform(bv, bg), 1e-8))
# part 2: along the budget S = 100 b^2 - 140 b + 60
for bgv in (F(0), F(1, 2), F(7, 10), F(1)):
    bvv = 1 - bgv
    Sx = srr - 2 * (srv * bvv + srg * bgv) + svv * bvv ** 2 + 2 * svg * bvv * bgv + sgg * bgv ** 2
    check('B2 budget quadratic at %s' % bgv, Sx == 100 * bgv ** 2 - 140 * bgv + 60)
check('B2 key 0.7', F(140, 200) == F(7, 10) and pb[1]['widget']['answer'] == 0.7)
grid = np.linspace(0, 1, 1000001)
check('B2 grid on the budget', close(grid[int(np.argmin(100 * grid ** 2 - 140 * grid + 60))], 0.7, 1e-6))
# slips: no budget (Q beta = -q), no cross term, gave beta_V
det = Q[0][0] * Q[1][1] - Q[0][1] ** 2
ub_v = (-q[0] * Q[1][1] + q[1] * Q[0][1]) / det
ub_g = (-q[1] * Q[0][0] + q[0] * Q[1][0]) / det
check('B2 no-budget weights', ub_g == F(15, 22) and ub_v == F(3, 11) and ub_v + ub_g == F(21, 22))
check('B2 "sum to 0.95"', round(float(ub_v + ub_g), 2) == 0.95 and round(float(ub_g), 2) == 0.68)
check('B2 no-cross', F(60 * 2 - 60 + 120, 2 * (60 + 80)) == F(9, 14))
wb2 = wrongs(pb[1]['widget'])
check('B2 slip values', close(wb2['no-budget'], 15 / 22, 1e-6) and close(wb2['no-cross'], 9 / 14, 1e-6) and wb2['gave-v'] == 0.3)
bands('B2', pb[1]['widget'])
check('B2 typed', typed(pb[1]['widget'], '0.70') == 'correct' and typed(pb[1]['widget'], '0.7') == 'correct'
      and typed(pb[1]['widget'], '0.68') == 'no-budget' and typed(pb[1]['widget'], '0.64') == 'no-cross'
      and typed(pb[1]['widget'], '0.30') == 'gave-v' and typed(pb[1]['widget'], '0.69') == 'generic')
# part 3: the long-only solve, by SLSQP on the data and on the quadratic form, and by active sets
for name, fun in (('data', lambda z: Sdata(z[0], z[1])), ('form', lambda z: Sform(z[0], z[1]))):
    for x0 in ((0.5, 0.5), (1.0, 0.0), (0.0, 1.0)):
        r = minimize(fun, x0, method='SLSQP', bounds=[(0, 1), (0, 1)],
                     constraints=[{'type': 'eq', 'fun': lambda z: z[0] + z[1] - 1}], options={'ftol': 1e-15, 'maxiter': 500})
        check('B3 SLSQP (%s) from %s' % (name, x0), r.success and close(r.x[0], 0.3, 5e-7) and close(r.x[1], 0.7, 5e-7))
cands = {(0.3, 0.7): Sform(0.3, 0.7), (0.0, 1.0): Sform(0, 1), (1.0, 0.0): Sform(1, 0)}
check('B3 active sets: the interior point wins', min(cands, key=cands.get) == (0.3, 0.7))
# KKT at (0.3, 0.7) with both bound multipliers 0: Q beta + q = lam * (1, 1)
gv = 120 * F(3, 10) + 40 * F(7, 10) - 60
gg = 40 * F(3, 10) + 160 * F(7, 10) - 120
check('B3 stationarity with the budget alone', gv == gg)
check('B3 key option', [o['id'] for o in pb[2]['widget']['options'] if o.get('correct')] == ['slack'])
check('B3 "at least 0.3 from 0 and from 1"', min(0.3, 0.7, 1 - 0.3, 1 - 0.7) == 0.3 or close(min(0.3, 0.7, 0.7, 0.3), 0.3))
# part 4
S11 = 100 * F(7, 10) ** 2 - 140 * F(7, 10) + 60
check('B4 S = 11', S11 == 11 == pb[3]['widget']['answer'] and close(Sdata(0.3, 0.7), 11, 1e-8))
check('B4 working', 30 * F(3, 10) + 60 * F(7, 10) == 51 and 60 * F(9, 100) + 40 * F(21, 100) + 80 * F(49, 100) == 53 and 60 - 102 + 53 == 11)
Sub = srr - 2 * (srv * ub_v + srg * ub_g) + svv * ub_v ** 2 + 2 * svg * ub_v * ub_g + sgg * ub_g ** 2
wb4 = wrongs(pb[3]['widget'])
check('B4 no-budget', Sub == F(120, 11) and close(wb4['no-budget'], 120 / 11, 1e-6))
check('B4 half-cross', close(60 - 102 + 5.4 + 4.2 + 39.2, 6.8) and wb4['half-cross'] == 6.8)
check('B4 linear-half', 60 - 51 + 53 == 62 == wb4['linear-half'])
check('B4 49/60', 1 - F(11, 60) == F(49, 60))
bands('B4', pb[3]['widget'])
check('B4 typed', typed(pb[3]['widget'], '11.00') == 'correct' and typed(pb[3]['widget'], '10.91') == 'no-budget'
      and typed(pb[3]['widget'], '6.80') == 'half-cross' and typed(pb[3]['widget'], '62') == 'linear-half')
# part 5: a percentage part
w5 = pb[4]['widget']
rms = math.sqrt(11 / 12)
check('B5 key', close(w5['answer'], rms / 100, 5e-8) and w5.get('unit') == '%' and w5['tol']['abs'] == 5e-6)
check('B5 no rounding tie', abs(rms * 1000 - round(rms * 1000)) < 0.45)
wb5 = wrongs(w5)
check('B5 slips', close(wb5['no-twelve'], math.sqrt(11) / 100, 5e-8) and close(wb5['no-root'], 11 / 12 / 100, 5e-8)
      and close(wb5['no-fit'], math.sqrt(5) / 100, 5e-8))
bands('B5', w5)
for s, want in (('0.957', 'correct'), ('0.957%', 'correct'), ('0.9574', 'correct'), ('0.958', 'generic'), ('0.956', 'generic'),
                ('0.96', 'generic'), ('3.317', 'no-twelve'), ('0.917', 'no-root'), ('2.236', 'no-fit'), ('0.00957', 'generic')):
    check('B5 typed %s' % s, typed(w5, s) == want)
check('B5 printed', round(11 / 12, 4) == 0.9167 and round(rms, 3) == 0.957 and round(math.sqrt(11), 3) == 3.317 and round(math.sqrt(5), 3) == 2.236)

# =====================================================================
# C. problems-4 p-curve-fit-backtrack
# =====================================================================
C = item(4, 'p-curve-fit-backtrack')
pc = C['parts']
s0 = 0.05
l1 = (1 - 0.96) / s0
l2 = (1 + 0.5) / s0
check('C1 curvature 0.8', close(l1, 0.8) and pc[0]['widget']['answer'] == 0.8)
check('C2 curvature 30', close(l2, 30) and pc[1]['widget']['answer'] == 30)
check('C1 slips', close(0.96 / 0.05, 19.2) and wrongs(pc[0]['widget']) == {'factor-over-s': 19.2, 'no-divide': 0.04})
check('C2 slips', close((1 - 0.5) / 0.05, 10) and close(1.5 * 0.05, 0.075) and wrongs(pc[1]['widget']) == {'sign': 10, 'times-s': 0.075})
bands('C1', pc[0]['widget'])
bands('C2', pc[1]['widget'])
# the narrowed band of review finding 2
check('C2 times-s band is 0.0005', pc[1]['widget']['wrong'][1]['tol']['abs'] == 0.0005)
for s, want in (('0.075', 'times-s'), ('0.5', 'generic'), ('0.04', 'generic'), ('0.3', 'generic'), ('0', 'generic'), ('0.08', 'generic'), ('30', 'correct'), ('10', 'sign')):
    check('C2 typed %s' % s, typed(pc[1]['widget'], s) == want)

H = np.diag([l1, l2])
f = lambda e: 0.5 * float(e @ H @ e)          # the excess


def backtrack(e):
    g = H @ e
    s = 1.0
    tried = []
    while True:
        new = e - s * g
        ok = f(new) <= f(e) - 0.5 * s * float(g @ g) + 1e-15
        tried.append((s, f(new), ok))
        if ok:
            return s, new, tried, g
        s /= 2


e40 = np.array([0.4 / l1, 0.06 / l2])
check('C3 errors 0.5 and 0.002', close(e40[0], 0.5) and close(e40[1], 0.002))
check('C3 excess 0.10006', close(f(e40), 0.10006, 1e-12))
s1, e41, tr1, g40 = backtrack(e40)
check('C3 accepted step 0.5', s1 == 0.5 == pc[2]['widget']['answer'] and [t[0] for t in tr1] == [1.0, 0.5])
check('C3 at s = 1: 0.05446, wanted 0.0818', round(tr1[0][1], 5) == 0.05446 and round(0.5 * float(g40 @ g40), 4) == 0.0818 and not tr1[0][2])
check('C3 at s = 0.5: 0.04776 under 0.05916', round(tr1[1][1], 5) == 0.04776 and round(0.10006 - 0.0409, 5) == 0.05916
      and round(0.25 * float(g40 @ g40), 4) == 0.0409 and close(e41[0], 0.3) and close(e41[1], -0.028))
gg40, gHg40 = float(g40 @ g40), float(g40 @ H @ g40)
check('C3 0.1636, 0.236, 0.693', close(gg40, 0.1636) and close(gHg40, 0.236) and round(gg40 / gHg40, 3) == 0.693)
# the closed form of the explain: the fall is s|g|^2 - s^2 gHg / 2
for s in (1.0, 0.5, 0.25, 0.05):
    check('C3 fall formula at %g' % s, close(f(e40) - f(e40 - s * g40), s * gg40 - 0.5 * s * s * gHg40, 1e-12))
check('C3 ten times, 7.5 times', close(0.5 / 0.05, 10) and close(0.5 / (2 / 30), 7.5))
wc3 = wrongs(pc[2]['widget'])
check('C3 slips', wc3 == {'any-fall': 1, 'below-limit': 0.0625, 'below-inverse': 0.03125, 'one-over-l': 0.0333})
halv = [2.0 ** -k for k in range(0, 12)]
check('C3 below-limit, below-inverse', max(h for h in halv if h < 2 / 30) == 0.0625 and max(h for h in halv if h < 1 / 30) == 0.03125)
bands('C3', pc[2]['widget'])
for s, want in (('0.5', 'correct'), ('1', 'any-fall'), ('0.0625', 'below-limit'), ('0.03125', 'below-inverse'), ('0.0333', 'one-over-l'),
                ('0.03333', 'one-over-l'), ('0.25', 'generic')):
    check('C3 typed %s' % s, typed(pc[2]['widget'], s) == want)
# part 4
s2, e42, tr2, g41 = backtrack(e41)
gg41, gHg41 = float(g41 @ g41), float(g41 @ H @ g41)
check('C4 gradient (0.24, -0.84)', close(g41[0], 0.24) and close(g41[1], -0.84))
check('C4 accepted step 0.03125', s2 == 0.03125 == pc[3]['widget']['answer'] and [t[0] for t in tr2] == [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125])
check('C4 0.7632, 21.2141, 0.036', close(gg41, 0.7632) and round(gHg41, 4) == 21.2141 and round(gg41 / gHg41, 3) == 0.036)
check('C4 keep: excess about 2.32', round(tr2[1][1], 2) == 2.32)
check('C4 untested: grows by about 9.8', round(tr2[0][1] - f(e41), 1) == 9.8 and close(1 - 30, -29))
check('C4 any-fall: 0.0063 against 0.02385', round(f(e41) - tr2[4][1], 4) == 0.0063 and round(0.5 * 0.0625 * gg41, 5) == 0.02385 and not tr2[4][2])
check('C4 sixteenfold, -14', close(0.5 / 0.03125, 16) and close(1 - 0.5 * 30, -14) and close(1 - 0.5 * 0.8, 0.6))
check('C4 slips', wrongs(pc[3]['widget']) == {'keep': 0.5, 'any-fall': 0.0625, 'untested': 1, 'one-over-l': 0.0333})
bands('C4', pc[3]['widget'])
for s, want in (('0.03125', 'correct'), ('0.0313', 'correct'), ('0.0312', 'correct'), ('0.031', 'generic'), ('0.0333', 'one-over-l'), ('0.5', 'keep'),
                ('0.0625', 'any-fall'), ('1', 'untested'), ('0.036', 'generic')):
    check('C4 typed %s' % s, typed(pc[3]['widget'], s) == want)
# part 5: the fixed-step run, by a loop on both errors
target = f(e42)
check('C5 excess after the two steps about 0.0343', round(target, 4) == 0.0343)
for tgt in (target, 0.0343):
    e = e40.copy()
    k = 0
    trace = []
    while f(e) > tgt:
        e = e * np.array([1 - s0 * l1, 1 - s0 * l2])
        k += 1
        trace.append(f(e))
    check('C5 fixed steps = 14 (target %.6f)' % tgt, k == 14 == pc[4]['widget']['answer'])
    check('C5 thirteen leave 0.0346', round(trace[12], 4) == 0.0346)
check('C5 13.1', round(math.log(0.10006 / 0.0343) / math.log(1 / 0.9216), 1) == 13.1 and close(0.96 ** 2, 0.9216))
check('C5 generic line: first k with 0.10006 x 0.9216^k <= 0.0343 is 14',
      0.10006 * 0.9216 ** 13 > 0.0343 >= 0.10006 * 0.9216 ** 14)
check('C5 slips', wrongs(pc[4]['widget']) == {'floor': 13, 'unsquared': 27, 'saved': 12}
      and math.ceil(math.log(0.10006 / 0.0343) / math.log(1 / 0.96)) == 27 and 14 - 2 == 12)
bands('C5', pc[4]['widget'])
# finding 1: the stem's step number against its own factor
steps = [int(x) for x in re.findall(r'At step (\d+) the gradient', C['prose'])]
back = 0.002 * 2.0 ** steps[0] if steps else 0.0
check('C stem names a step', bool(steps))
finding(1, bool(steps) and back > 10,
        'p-curve-fit-backtrack stem: a level error of 0.002 at step %d under a factor of -0.5 a step needs a start error of %.3g (the decay-rate error starts at %.3g)'
        % (steps[0] if steps else -1, back, 0.5 / 0.96 ** (steps[0] if steps else 0)))

# =====================================================================
# D. kept problems: every changed line recomputed
# =====================================================================
# --- set 1, p-shortfall-and-fee
Cc = lambda x: 2 * (x - 3) ** 2 + 5 * abs(x)
check('D1 chord gap 13', F(1, 2) * Cc(F(-1)) + F(1, 2) * Cc(F(3)) - Cc(F(1)) == 13)
check('D1 C(-1) = 37', Cc(-1) == 37 and 2 * 16 - 5 == 27)
check('D1 minimiser 1.75', close(brentq(lambda x: 4 * (x - 3) + 5, 0, 3), 1.75))
check('D1 C(1.75) = 11.875 = 3.125 + 8.75', Cc(1.75) == 11.875 and 2 * 1.5625 == 3.125 and 5 * 1.75 == 8.75)
check('D1 C(0) = 18, C(3) = 15', Cc(0) == 18 and Cc(3) == 15)
check("D1 C'(1.2) = -2.2, C(1.2) = 12.48", close(4 * (1.2 - 3) + 5, -2.2) and close(Cc(1.2), 12.48) and close(2 * 1.8 ** 2, 6.48)
      and close(12.48 - 11.875, 0.605))
xs = np.linspace(-5, 1.2, 620001)
check('D1 grid under the cap', close(float(np.min(2 * (xs - 3) ** 2 + 5 * np.abs(xs))), 12.48, 1e-9))
xs = np.linspace(-5, 8, 1300001)
check('D1 grid free', close(float(np.min(2 * (xs - 3) ** 2 + 5 * np.abs(xs))), 11.875, 1e-9))
SF = item(1, 'p-shortfall-and-fee')
for i in (2, 3, 4):
    bands('D1 part %d' % (i + 1), SF['parts'][i]['widget'])
check('D1 story swapped', has(SF, 'can maker') and not has(SF, 'shares'))
# --- set 1, p-two-futures-hedge: Var(P - a F1 - b F2)
Sg = np.array([[6.0, 1, 1], [1, 1, 3], [1, 3, 10]])           # order P, F1, F2
Vv = lambda a_, b_: float(np.array([1, -a_, -b_]) @ Sg @ np.array([1, -a_, -b_]))
for a_, b_ in ((0, 0), (7, -2), (1, 0), (3, 4), (-2, 5)):
    check('D2 V formula at (%g, %g)' % (a_, b_), close(Vv(a_, b_), a_ * a_ + 6 * a_ * b_ + 10 * b_ * b_ - 2 * a_ - 2 * b_ + 6))
sol = np.linalg.solve(np.array([[2.0, 6], [6, 20]]), np.array([2.0, 2]))
check('D2 minimiser (7, -2), V = 1', close(sol[0], 7) and close(sol[1], -2) and close(Vv(7, -2), 1))
check('D2 working 49 - 84 + 40 - 14 + 4 + 6', 49 - 84 + 40 - 14 + 4 + 6 == 1)
check('D2 Hessian det 4; with 7ab it is -9; 1*10 - 9 = 1', 2 * 20 - 36 == 4 and 40 - 49 == -9 and 1 * 10 - 3 ** 2 == 1)
check('D2 covariance positive definite', bool(np.all(np.linalg.eigvalsh(Sg) > 0)))
r = minimize(lambda z: Vv(z[0], z[1]), (0.0, 1.0), method='SLSQP', bounds=[(None, None), (0, None)], options={'ftol': 1e-14})
check('D2 with b >= 0: V = 5 at (1, 0)', close(r.fun, 5, 1e-7) and close(r.x[0], 1, 1e-4) and close(r.x[1], 0, 1e-6))
check('D2 five sixths', 1 - F(1, 6) == F(5, 6))
HF = item(1, 'p-two-futures-hedge')
check('D2 the ban is on buying', has(HF, 'may not buy carbon forwards') and has(HF, 'a negative amount is a purchase'))
# --- set 2, p-parking-cash
r = linprog(c=[-6, -10], A_ub=[[1, 1], [0.5, 1]], b_ub=[14, 8])
check('D3 linprog (12, 2), -92', close(r.fun, -92, 1e-7) and close(r.x[0], 12, 1e-6) and close(r.x[1], 2, 1e-6))
check('D3 all-bills line', 6 * 14 == 84 and 8 - 0.5 * 14 == 1 and 1 / 0.5 == 2 and 2 * (10 - 6) == 8 and 10 * 8 == 80)
r = linprog(c=[-6, -10], A_ub=[[1, 1], [0.5, 1]], b_ub=[14, 8], bounds=[(0, None), (5, None)])
check('D3 floor 5: 886 at (6, 5)', close(800 - r.fun, 886, 1e-6) and close(r.x[0], 6, 1e-6) and 800 + 50 == 850 and 800 + 80 == 880)
st = [linprog(c=[-6, -10], A_ub=[[1, 1], [0.5, 1]], b_ub=[14, 8], bounds=[(0, None), (fl, None)]).status for fl in (8, 8.01, 9)]
check('D3 largest floor 8', st == [0, 2, 2])
# --- set 2, p-whole-blocks
r = linprog(c=[-6, -5], A_ub=[[4, 3], [1, 3]], b_ub=[19, 8])
check('D4 fractional 263/9 at (11/3, 13/9)', close(-r.fun, 263 / 9, 1e-7) and close(r.x[0], 11 / 3, 1e-6) and close(r.x[1], 13 / 9, 1e-6))
check('D4 axis points', 6 * 4.75 == 28.5 and close(5 * 8 / 3, 13.3333333, 1e-6) and 8 - 4.75 == 3.25)
check('D4 swap three A for four B', 3 * 4 == 4 * 3 and 4 * 5 - 3 * 6 == 2)
whole = [(x, y, 6 * x + 5 * y) for x in range(6) for y in range(4) if 4 * x + 3 * y <= 19 and x + 3 * y <= 8]
check('D4 whole plans: best 29 at (4, 1) only', max(w[2] for w in whole) == 29 and [w[:2] for w in whole if w[2] == 29] == [(4, 1)])
# --- set 2, p-three-strategies
r = linprog(c=[10, 10], A_ub=[[-3, -2], [-1, -3], [-2, -1]], b_ub=[-6, -7, -4])
check('D5 dual 30 at (1, 2)', close(r.fun, 30, 1e-7) and close(r.x[0], 1, 1e-6) and close(r.x[1], 2, 1e-6))
r = linprog(c=[-6, -7, -4], A_ub=[[3, 1, 2], [2, 3, 1]], b_ub=[10, 10])
check('D5 primal 30 at (0, 2, 4)', close(-r.fun, 30, 1e-7) and close(r.x[1], 2, 1e-6) and close(r.x[2], 4, 1e-6))
feas = lambda u, v: 3 * u + 2 * v >= 6 and u + 3 * v >= 7 and 2 * u + v >= 4
check('D5 corners 40, 30, 70', feas(0, 4) and feas(1, 2) and feas(7, 0) and 10 * 4 == 40 and 10 * 7 == 70)
check('D5 "raising u by 1 lets v fall by 2, saves 10"', 2 * 1 + (4 - 2) == 4 and 10 * 1 - 10 * 2 == -10)
check('D5 columns', (3, 2) == (3, 2) and 1 * 1 + 3 * 2 == 7 and 3 * 1 + 2 * 2 == 7 and 2 * 1 + 1 * 2 == 4)
# --- set 3, p-capital-price
P1 = lambda x: 10 * x - x * x
P2 = lambda x: 8 * x - x * x / 2
gd = lambda lam: P1(5 - lam / 2) + P2(8 - lam) - lam * (5 - lam / 2 + 8 - lam - 6)
check('D6 g(3) = 42.75', close(gd(3), 42.75))
lam = brentq(lambda t: 6 - (5 - t / 2) - (8 - t), 0, 8)
check('D6 price 14/3, profit 122/3', close(lam, 14 / 3) and close(P1(8 / 3) + P2(10 / 3), 122 / 3))
check('D6 estimate 42.07', close(122 / 3 + 0.3 * 14 / 3, 42.0666667, 1e-6))
r = minimize(lambda z: -(P1(z[0]) + P2(z[1])), (3.0, 3.0), method='SLSQP', constraints=[{'type': 'ineq', 'fun': lambda z: 6.3 - z[0] - z[1]}], options={'ftol': 1e-14})
check('D6 re-solve 42.04 at a price of 4.47', round(-r.fun, 2) == 42.04 and round(10 - 2 * r.x[0], 2) == 4.47)
CP = item(3, 'p-capital-price')
check('D6 key band takes the estimate and the re-solve', typed(CP['parts'][4]['widget'], '42.07') == 'correct' and typed(CP['parts'][4]['widget'], '42.04') == 'correct')
check('D6 dual function named', has(CP, 'The dual function $g(\\lambda)$ is the Lagrangian') and 'in £k' in CP['parts'][4]['question'])
# --- set 3, p-variance-limit
Vw = lambda w: 0.0625 * w * w + 2 * 0.005 * w * (1 - w) + 0.01 * (1 - w) ** 2
for w in (0.0, 0.4, 1.0, 0.25):
    check('D7 V(w) at %g' % w, close(Vw(w), 0.01 - 0.01 * w + 0.0625 * w * w))
check('D7 w = 0.4, mu = 1.5', close(brentq(lambda w: Vw(w) - 0.016, 0.08, 1), 0.4) and close(0.06 / (0.125 * 0.4 - 0.01), 1.5))
w2 = brentq(lambda w: Vw(w) - 0.0162, 0.08, 1)
check('D7 3 basis points; re-solve 2.98 at w = 0.405', close(1.5 * 0.0002 * 1e4, 3) and round(w2, 3) == 0.405 and round(0.06 * (w2 - 0.4) * 1e4, 2) == 2.98)
VL = item(3, 'p-variance-limit')
check('D7 story swapped', has(VL, 'An endowment') and has(VL, 'corporate bonds') and not has(VL, 'gilts'))
# --- set 4, p-sale-horizon
fT = lambda T: 8 / T + 2 * T
d1 = lambda T: 2 - 8 / T ** 2
d2 = lambda T: 16 / T ** 3
T1 = 1 - d1(1) / 16
T2 = T1 - d1(T1) / d2(T1)
check('D8 2/L = 0.125, 1/16, 2/f"(2) = 1, eight times', close(2 / d2(1), 0.125) and close(2 / d2(2), 1) and close(d2(1) / d2(2), 8))
check('D8 T1 = 1.375', close(T1, 1.375) and close(1 + d1(1) / 16, 0.625) and close(fT(0.625), 14.05) and fT(1) == 10)
check('D8 T2 = 1.7375', round(T2, 4) == 1.7375 and round(-d1(1.375), 4) == 2.2314 and round(d2(1.375), 2) == 6.15)
check('D8 slips 1.5145, 1.0125', round(1.375 + 2.2314 / 16, 4) == 1.5145 and round(2.2314 / 16, 4) == 0.1395 and round(1.375 - 0.3625, 4) == 1.0125
      and round(-d1(1.375) / d2(1.375), 4) == 0.3625)
check('D8 4.6043 + 3.4750 = 8.0793, 79 pounds', round(8 / 1.7375, 4) == 4.6043 and round(fT(1.7375), 4) == 8.0793 and round((fT(1.7375) - 8) * 1000) == 79)
SH = item(4, 'p-sale-horizon')
w4 = SH['parts'][3]['widget']
check('D8 thousands band is 0.005', [x for x in w4['wrong'] if x['id'] == 'thousands'][0]['tol']['abs'] == 0.005)
for s, want in (('79', 'correct'), ('79.3', 'correct'), ('0.0793', 'thousands'), ('0.08', 'thousands'), ('0.079', 'thousands'), ('0.311', 'generic'),
                ('0.568', 'generic'), ('0', 'generic'), ('311', 'descent'), ('568', 'start'), ('8079', 'total')):
    check('D8 typed %s' % s, typed(w4, s) == want)
for i in range(4):
    bands('D8 part %d' % (i + 1), SH['parts'][i]['widget'])
# --- set 4, p-variance-log
lv = [F(2004096, 10000), F(2003136, 10000), F(2002401, 10000)]
ratio = (lv[1] - lv[2]) / (lv[0] - lv[1])
check('D9 ratio 0.765625, rho 0.875', ratio == F(49, 64) and F(7, 8) ** 2 == ratio and 1 - ratio == F(15, 64) and float(1 - ratio) == 0.234375)
Vstar = lv[2] - (lv[1] - lv[2]) * ratio / (1 - ratio)
check('D9 V* = 200, excess 0.2401', Vstar == 200 and lv[2] - 200 == F(2401, 10000))
k = 0
ex = F(2401, 10000)
while ex > F(1, 10000):
    ex *= ratio
    k += 1
check('D9 30 more steps', k == 30)
check('D9 29 leave 1.04e-4, 30 give 7.96e-5', round(0.2401 * 0.765625 ** 29 * 1e4, 2) == 1.04 and round(0.2401 * 0.765625 ** 30 * 1e5, 2) == 7.96)
check('D9 0.2901, 0.0735', close(200.2401 - 199.95, 0.2901) and close(200.3136 - 200.2401, 0.0735))
VG = item(4, 'p-variance-log')
check('D9 key option', [o['id'] for o in VG['parts'][3]['widget']['options'] if o.get('correct')] == ['bracket'])
for i in range(3):
    bands('D9 part %d' % (i + 1), VG['parts'][i]['widget'])

# =====================================================================
# E. findings of the review that a string decides
# =====================================================================
SFp2 = item(3, 'p-style-fit')['parts']
finding(2, pa[2]['feedback']['correct'].startswith('Along the line the spend is') and SFp2[1]['feedback']['correct'].startswith('Along the budget $S ='),
        'p-account-target part 3 and p-style-fit part 2: the two `correct` lines are one sentence frame ("Along the ... with slope ... It is 0 at ..., so ...")')
# ruling b: the two last parts of set 3 are different quantities; one explain line follows l13 screen 3
check('E ruling b: the two estimates', close(0.3 * 14 / 3, 1.4) and close(1.5 * 0.0002, 0.0003))
check('E replacement line of finding 3: within 0.03, mu falls to 1.48',
      3 - 0.06 * (w2 - 0.4) * 1e4 < 0.03 and round(0.06 / (0.125 * w2 - 0.01), 2) == 1.48)
finding(3, 'adds about 0.0003. Re-solving gives' in VL['parts'][4]['explain']['text'],
        'p-variance-limit part 5 explain keeps the frame of l13 screen 3 explain ("..., so a step of 0.002 adds about 0.002571. Re-solving gives ...")')

print('delta-review-delta-af-convex-numbers: %d checks, %d failed, %d FINDING line(s)' % (n_checks, n_fail, n_find))
sys.exit(0)
