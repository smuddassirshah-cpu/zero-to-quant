#!/usr/bin/env python3
"""Second read of pdes problems-1 to -3 (topic 3.2): the reader's own recomputation.

Imports nothing from problems-pdes-numbers.py. Every key is rebuilt from the prose by one route
(closed form with the exact inputs) and again by another (quadrature, a grid run, a matrix, a series
sum, a dense Crank-Nicolson solve), then by the part's own printed working with its rounded inputs.
Each band must take all of these at the asked rounding; each wrong[] value is rebuilt from the slip
its line names, must sit in its own band at the asked rounding and outside the key band.
Uses math and numpy only (no SciPy solver), so it cannot fail to converge on another build.

Always exits 0. A failing check prints a line starting FINDING (docs/reviews/review-problems-pdes-1-3.md).
"""
import json
import math
import os
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'pdes')
SETS = {n: json.load(open(os.path.join(BASE, f'problems-{n}.json'), encoding='utf-8')) for n in (1, 2, 3)}
N = {'checks': 0, 'findings': 0}


def ok(cond, msg):
    N['checks'] += 1
    if not cond:
        N['findings'] += 1
        print('FINDING', msg)


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def Phinv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if Phi(mid) < p else (lo, mid)
    return (lo + hi) / 2


def trap(f, a, b, n=200000):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return float((y[0] / 2 + y[1:-1].sum() + y[-1] / 2) * (b - a) / n)


def item(n, iid):
    return next(i for i in SETS[n]['items'] if i['id'] == iid)


def text(part):
    fb = part['feedback']
    return ' '.join([part['question'], fb['correct'], fb.get('generic', ''), part['explain']['text']] + list(fb.get('byKey', {}).values()))


def part(n, iid, p, routes, dp=None, wrong=None, pct=False, agree=1e-6):
    """routes: values the key band must take (exact, second method, printed working).
    dp: decimal places asked (of what the learner types). wrong: {id: [values the slip gives]}."""
    w = item(n, iid)['parts'][p - 1]['widget']
    tag = f'L{n} {iid} p{p}'
    key, tol = w['answer'], w['tol']['abs']
    scale = 100 if pct else 1
    ok((w.get('unit') == '%') == pct, f'{tag}: unit "%" {"missing" if pct else "unexpected"}')
    for v in routes:
        ok(abs(v - key) <= tol + 1e-9, f'{tag}: route value {v:.8g} outside key band {key} +- {tol}')
        if dp is not None:
            r = round(v * scale, dp) / scale
            ok(abs(r - key) <= tol + 1e-9, f'{tag}: {v:.8g} rounded to {dp} dp ({r:.8g}) outside key band {key} +- {tol}')
    ok(abs(routes[0] - routes[1]) <= max(agree * abs(routes[0]), 1e-9), f'{tag}: the two routes disagree {routes[0]!r} {routes[1]!r}')
    have = {x['id']: x for x in w.get('wrong', [])}
    wrong = wrong or {}
    ok(set(have) == set(wrong), f'{tag}: wrong ids {sorted(have)} against the reader\'s {sorted(wrong)}')
    by = item(n, iid)['parts'][p - 1]['feedback'].get('byKey', {})
    for wid, vals in wrong.items():
        if wid not in have:
            continue
        x = have[wid]
        ok(wid in by, f'{tag}: wrong {wid} has no byKey line')
        ok(abs(x['value'] - key) > tol + x['tol']['abs'], f'{tag}: wrong {wid} band reaches the key band')
        for v in vals:
            ok(abs(v - x['value']) <= x['tol']['abs'] + 1e-9, f'{tag}: slip {wid} gives {v:.8g}, outside its band {x["value"]} +- {x["tol"]["abs"]}')
            if dp is not None:
                r = round(v * scale, dp) / scale
                ok(abs(r - x['value']) <= x['tol']['abs'] + 1e-9, f'{tag}: slip {wid} rounded to {dp} dp ({r:.8g}) misses its band')
            ok(abs(v - key) > tol, f'{tag}: slip {wid} value {v:.8g} is taken by the key')
    ids = list(have)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = have[ids[i]], have[ids[j]]
            ok(abs(a['value'] - b['value']) > a['tol']['abs'] + b['tol']['abs'], f'{tag}: wrong bands {ids[i]} and {ids[j]} overlap')


def says(n, iid, p, *figs):
    t = text(item(n, iid)['parts'][p - 1])
    for s in figs:
        ok(s in t, f'L{n} {iid} p{p}: the text should print {s}')


def not_says(n, iid, p, s, why):
    t = text(item(n, iid)['parts'][p - 1])
    ok(s not in t, f'L{n} {iid} p{p}: prints {s}; {why}')


# ------------------------------------------------------------------ level 1
def level1():
    # p-tick-spread: tick 0.4p every 0.1 s
    D = 0.4 ** 2 / (2 * 0.1)
    var_per_sec = 0.4 ** 2 / 0.1                       # second route: variance of independent steps
    part(1, 'p-tick-spread', 1, [D, var_per_sec / 2], wrong={'no-half': [0.16 / 0.1], 'unsquared': [0.4 / 0.2]})
    sd = math.sqrt(2 * D * 60)
    part(1, 'p-tick-spread', 2, [sd, math.sqrt(600 * 0.16)], dp=2,
         wrong={'variance': [96], 'no-two': [math.sqrt(48)], 'd-slip': [math.sqrt(2 * 1.6 * 60)]})
    # exact binomial walk as a cross-check of the normal tail (600 steps of 0.4: |move| > 15 means |net steps| >= 38)
    pm = [math.comb(600, k) / 2 ** 600 for k in range(601)]
    binom = sum(q for k, q in enumerate(pm) if abs(2 * k - 600) * 0.4 > 15)
    p_exact = 2 * (1 - Phi(15 / sd))
    ok(abs(binom - p_exact) < 0.012, f'L1 p-tick-spread p3: exact walk tail {binom:.4f} against the kernel {p_exact:.4f}')
    part(1, 'p-tick-spread', 3, [p_exact, 2 * (1 - Phi(15 / math.sqrt(96.0))), 2 * (1 - 0.9371)], dp=3,
         wrong={'one-tail': [1 - 0.9371, 1 - Phi(15 / sd)], 'inside': [1 - 2 * (1 - 0.9371)]})
    ok(abs(Phi(1.531) - 0.9371) < 5e-5 and abs(15 / 9.798 - 1.531) < 5e-4, 'L1 p-tick-spread p3: table value')
    t = 24 ** 2 / (2 * D)
    part(1, 'p-tick-spread', 4, [t, 60 * (24 / sd) ** 2], dp=0, wrong={'linear': [60 * 24 / 9.798, 60 * 24 / sd], 'var-24': [24 / (2 * D)]})
    says(1, 'p-tick-spread', 4, '2.449', '576')
    ok(abs(24 / sd - 2.449) < 5e-4, 'L1 p-tick-spread p4: 2.449')

    # p-two-level-bar: D = 0.2, 30 left, 90 right
    def u(x, tt, w2=0.4):
        return 30 + 60 * Phi(x / math.sqrt(w2 * tt))
    # second route: the kernel integral of the start by quadrature
    def u_quad(x, tt):
        ker = lambda y: np.exp(-(x - y) ** 2 / (4 * 0.2 * tt)) / math.sqrt(4 * math.pi * 0.2 * tt)
        return 30 * trap(ker, -8.0, 0.0) + 90 * trap(ker, 0.0, 8.0)
    part(1, 'p-two-level-bar', 1, [60, u(50, 1) - u(-50, 1)], dp=0, wrong={'right-value': [90], 'gave-a': [30]})
    part(1, 'p-two-level-bar', 2, [u(0.4, 0.25), u_quad(0.4, 0.25), 30 + 60 * 0.8971], dp=1,
         wrong={'no-two': [u(0.4, 0.25, 0.2)], 'no-base': [60 * 0.8971, 60 * Phi(0.4 / math.sqrt(0.1))]})
    ok(abs(Phi(1.265) - 0.8971) < 5e-5 and abs(Phinv(0.75) - 0.6745) < 5e-5, 'L1 p-two-level-bar: table values')
    z = Phinv(0.75)
    x75 = z * math.sqrt(0.1)
    ok(abs(u(x75, 0.25) - 75) < 1e-9, 'L1 p-two-level-bar p3: u at the answer is 75')
    part(1, 'p-two-level-bar', 3, [x75, x75, 0.6745 * 0.3162], dp=3, wrong={'no-width': [0.6745], 'share': [0.75 * 0.3162]})
    t75 = (0.4 / z) ** 2 / 0.4
    ok(abs(u(0.4, t75) - 75) < 1e-9, 'L1 p-two-level-bar p4: u(0.4, t) at the answer is 75')
    part(1, 'p-two-level-bar', 4, [t75, t75, (0.4 / 0.6745) ** 2 / 0.4, 0.3517 / 0.4], dp=3,
         wrong={'no-two': [(0.4 / 0.6745) ** 2 / 0.2], 'unsquared': [0.593 / 0.4, (0.4 / 0.6745) / 0.4]})
    ok(u(0.4, 0.01) > 89 and u(0.4, 0.5) > 75 > u(0.4, 1.5) and abs(u(0.4, 1e9) - 60) < 0.01, 'L1 p-two-level-bar p5: u(0.4, t) falls through 75 towards 60')
    # steady state on [-3, 3] by relaxation as the second route
    g = np.linspace(-3, 3, 61)
    v = np.where(g > 0, 90.0, 30.0); v[0], v[-1] = 30, 90
    for _ in range(20000):
        v[1:-1] = 0.5 * (v[:-2] + v[2:])
    part(1, 'p-two-level-bar', 5, [30 + 10 * 3.4, float(v[34])], dp=0, wrong={'centre': [60], 'level': [75]})

    # p-grid-rod: [0, 1.2], D = 0.25, dx = 0.1, ends 15 and 75, start 40
    dtmax = Fraction(1, 100) / (2 * Fraction(1, 4))
    steps = math.ceil(Fraction(3, 2) / dtmax)
    part(1, 'p-grid-rod', 1, [steps, 1.5 / 0.02], dp=0,
         wrong={'lam-one': [math.ceil(Fraction(3, 2) / (2 * dtmax))], 'no-d': [math.ceil(Fraction(3, 2) / (Fraction(1, 100) / 2))]})

    def run(lam, n):
        w = np.full(13, 40.0); w[0], w[-1] = 15, 75
        for _ in range(n):
            w[1:-1] = w[1:-1] + lam * (w[2:] - 2 * w[1:-1] + w[:-2])
        return w
    part(1, 'p-grid-rod', 2, [0.5 * (15 + 40), float(run(0.5, 1)[1])], wrong={'lam-one': [float(run(1.0, 1)[1])], 'three-mean': [95 / 3]})
    r3 = run(0.5, 3)
    ok(abs(run(0.5, 2)[2] - 33.75) < 1e-12 and abs(run(0.5, 2)[1] - 27.5) < 1e-12, 'L1 p-grid-rod p3: 33.75 and 27.5 after two steps')
    part(1, 'p-grid-rod', 3, [0.5 * (15 + 33.75), float(r3[1])], dp=3, wrong={'two-steps': [float(run(0.5, 2)[1])]})
    far = run(0.5, 5000)
    ok(np.abs(far - (15 + 50 * np.linspace(0, 1.2, 13))).max() < 1e-9, 'L1 p-grid-rod p4: the lambda = 1/2 grid does settle on the line')
    part(1, 'p-grid-rod', 4, [15 + 50 * 0.1, float(far[1])], dp=0, wrong={'mean-ends': [45], 'left-end': [15]})

    # p-drift-walk: dx = 0.05, dt = 0.001, q = 0.6
    ok(abs(0.05 ** 2 / 0.002 - 1.25) < 1e-12, 'L1 p-drift-walk: D = 1.25')
    c = (2 * 0.6 - 1) * 0.05 / 0.001
    part(1, 'p-drift-walk', 1, [c, (0.6 * 0.05 - 0.4 * 0.05) / 0.001], dp=0, wrong={'no-bias': [0.05 / 0.001], 'used-q': [0.6 * 50]})

    def resid(a, x=0.37, tt=0.21, h=1e-4):
        f = lambda xx, t_: math.exp(-a * t_) * math.cos(2 * (xx - 10 * t_))
        ut = (f(x, tt + h) - f(x, tt - h)) / (2 * h)
        ux = (f(x + h, tt) - f(x - h, tt)) / (2 * h)
        uxx = (f(x + h, tt) - 2 * f(x, tt) + f(x - h, tt)) / h ** 2
        return ut + 10 * ux - 1.25 * uxx
    ok(abs(resid(5)) < 1e-5 and abs(resid(2.5)) > 0.1 and abs(resid(1.25)) > 0.1, 'L1 p-drift-walk p2: residual zero only at a = 5')
    part(1, 'p-drift-walk', 2, [1.25 * 4, 5.0], wrong={'unsquared': [1.25 * 2], 'no-freq': [1.25]})
    m, sdv = c * 0.32, math.sqrt(2 * 1.25 * 0.32)
    part(1, 'p-drift-walk', 3, [Phi((2 - m) / sdv), 1 - Phi(1.2 / sdv), 1 - 0.9102], dp=3,
         wrong={'no-drift': [Phi(2 / sdv)], 'var-dt': [Phi((2 - m) / math.sqrt(0.4))]})
    ok(abs(Phi(1.342) - 0.9102) < 5e-5 and abs(Phinv(0.99) - 2.3263) < 5e-5, 'L1 p-drift-walk: table values')
    z99 = Phinv(0.99)
    t1 = (z99 / (10 / math.sqrt(2.5))) ** 2
    ok(abs(Phi(-10 * t1 / math.sqrt(2.5 * t1)) - 0.01) < 1e-9, 'L1 p-drift-walk p4: the chance at the answer is 1%')
    part(1, 'p-drift-walk', 4, [t1, t1, (2.3263 / 6.325) ** 2, 0.3678 ** 2], dp=3,
         wrong={'unsquared': [2.3263 / 6.325], 'var-dt': [(z99 / (10 / math.sqrt(1.25))) ** 2]})
    # claim: "its density obeys u_t + c u_x = D u_xx": the walk's own variance rate
    walk_var_rate = 4 * 0.6 * 0.4 * 0.05 ** 2 / 0.001
    ok(abs(walk_var_rate - 2 * 1.25) < 1e-9,
       f'L1 p-drift-walk prose: the walk\'s own variance is {walk_var_rate:.2f}t, not 2Dt = 2.50t (homework-1 item 7 names the gap c^2 dt t); '
       f'the walk itself is below 2 at t = 0.32 with chance {Phi((2 - m) / math.sqrt(walk_var_rate * 0.32)):.4f}, the model says 0.0899')


# ------------------------------------------------------------------ level 2
def level2():
    pi = math.pi
    rate = 0.1 * (pi / 2) ** 2
    part(2, 'p-tent-rod', 1, [rate, 0.1 * pi ** 2 / 4], dp=4, wrong={'unsquared': [0.1 * pi / 2], 'length-one': [0.1 * pi ** 2]})
    tent = lambda x: np.where(x < 1, 6 * x, 6 * (2 - x))
    bk = lambda k: trap(lambda x: tent(x) * np.sin(k * pi * x / 2), 0, 2)          # (2/L) = 1
    part(2, 'p-tent-rod', 2, [48 / pi ** 2, bk(1)], dp=4, wrong={'one-over-l': [bk(1) / 2], 'peak': [6]})
    ok(abs(bk(3) + 0.5404) < 5e-5 and abs(bk(2)) < 1e-9, 'L2 p-tent-rod p3: b_3 = -0.5404 and b_2 = 0')
    two = bk(1) * math.exp(-rate * 1.5) - bk(3) * math.exp(-9 * rate * 1.5)
    work = 4.8634 * math.exp(-0.2467 * 1.5) + 0.5404 * math.exp(-9 * 0.2467 * 1.5)
    full = sum(bk(k) * math.exp(-k * k * rate * 1.5) * math.sin(k * pi / 2) for k in range(1, 12))
    ok(abs(full - two) < 1e-4, 'L2 p-tent-rod p3: later terms are below 1e-4 at t = 1.5')
    part(2, 'p-tent-rod', 3, [two, full, work, 3.359 + 0.019], dp=2, agree=1e-4,
         wrong={'one-term': [4.8634 * math.exp(-0.2467 * 1.5)], 'sign': [4.8634 * math.exp(-0.2467 * 1.5) - 0.5404 * math.exp(-9 * 0.2467 * 1.5)]})
    says(2, 'p-tent-rod', 3, 'e^{-0.370}', 'e^{-3.331}', '3.359', '0.019')
    ok(abs(0.2467 * 1.5 - 0.370) < 5e-4 and abs(9 * 0.2467 * 1.5 - 3.331) < 6e-4, 'L2 p-tent-rod p3: exponents')
    t1 = math.log(bk(1)) / rate
    part(2, 'p-tent-rod', 4, [t1, math.log(48 / pi ** 2) / (0.1 * pi ** 2 / 4), math.log(4.8634) / 0.2467], dp=2,
         wrong={'peak': [math.log(6) / rate], 'sign': [-t1]})
    ok(abs(bk(3)) * math.exp(-9 * rate * t1) < 1e-6, 'L2 p-tent-rod p4: the k = 3 term is below 1e-6 by then')

    # p-exp-series
    b = lambda k: trap(lambda x: np.exp(x) * np.sin(k * x), -pi, pi) / pi
    a = lambda k: trap(lambda x: np.exp(x) * np.cos(k * x), -pi, pi) / pi
    b1 = math.sinh(pi) / pi
    part(2, 'p-exp-series', 1, [b1, b(1)], dp=4, wrong={'no-pi': [math.sinh(pi)], 'sign': [-b1]})
    says(2, 'p-exp-series', 1, '11.5487')
    for k in (2, 3, 7):
        ok(abs(b(k) - (-1) ** (k + 1) * 2 * k / (1 + k * k) * b1) < 1e-7, f'L2 p-exp-series: b_{k} formula')
        ok(abs(a(k) * math.cos(k * pi) - 2 * b1 / (1 + k * k)) < 1e-7, f'L2 p-exp-series p5: a_{k} cos k pi = 2 sinh(pi)/(pi(1 + k^2))')
    ok(abs(a(0) / 2 - b1) < 1e-7, 'L2 p-exp-series p5: a_0/2 = sinh(pi)/pi')
    part(2, 'p-exp-series', 2, [0.6 * b1, b(3), 0.6 * 3.6761], dp=4, wrong={'sign': [-0.6 * b1], 'no-k': [0.2 * b1, 0.2 * 3.6761]})
    w4 = round(0.6 * 3.6761, 4)
    not_says(2, 'p-exp-series', 2, r'0.6 \times 3.6761 \approx 2.2056', f'0.6 x 3.6761 = {0.6 * 3.6761:.5f}, which is {w4} to 4 places')
    slope = (math.log(2 * 4000 / (1 + 4000 ** 2)) - math.log(2 * 2000 / (1 + 2000 ** 2))) / math.log(2)
    part(2, 'p-exp-series', 3, [-1, round(slope, 4)], dp=0, wrong={'minus-two': [-2], 'plus-one': [1]})
    part(2, 'p-exp-series', 4, [math.cosh(pi), (math.exp(pi) + math.exp(-pi)) / 2], dp=4,
         wrong={'left': [math.exp(pi)], 'right': [math.exp(-pi)], 'half-gap': [math.sinh(pi)]})
    says(2, 'p-exp-series', 4, '23.1407', '0.0432')
    Nn = 2_000_000
    ks = np.arange(1, Nn + 1, dtype=float)
    ssum = float((1 / (1 + ks * ks)).sum()) + (math.pi / 2 - math.atan(Nn + 0.5))      # tail by the midpoint integral
    coth = math.cosh(pi) / math.sinh(pi)
    part(2, 'p-exp-series', 5, [(pi * coth - 1) / 2, ssum, (pi * 11.5920 / 11.5487 - 1) / 2, (3.15335 - 1) / 2], dp=4,
         wrong={'no-half': [pi * coth - 1], 'keep-one': [pi * coth / 2], 'used-left': [(pi * math.exp(pi) / math.sinh(pi) - 1) / 2]})
    ok(abs(pi * coth - 3.15335) < 5e-6, 'L2 p-exp-series p5: pi coth pi = 3.15335')

    # p-grid-modes: length pi, 12 intervals, D = 0.5, dt = 0.06
    dx = pi / 12
    lam = 0.5 * 0.06 / dx ** 2
    part(2, 'p-grid-modes', 1, [lam, 0.5 * 0.06 * 144 / pi ** 2, 0.03 / 0.068539], dp=4, wrong={'no-d': [0.06 / dx ** 2], 'unsquared': [0.03 / dx]})
    ok(abs(dx ** 2 - 0.068539) < 5e-7 and lam < 0.5, 'L2 p-grid-modes p1: dx^2 and lambda below 1/2')
    A = np.diag(np.full(11, 1 - 2 * lam)) + np.diag(np.full(10, lam), 1) + np.diag(np.full(10, lam), -1)
    eig = np.sort(np.linalg.eigvalsh(A))
    g = 1 - 4 * lam * math.sin(dx / 2) ** 2
    ok(np.abs(eig).max() < 1, 'L2 p-grid-modes p1: every grid mode stays bounded')
    part(2, 'p-grid-modes', 2, [g, float(eig[-1]), 1 - 4 * 0.4377 * 0.01704], dp=4,
         wrong={'exact': [math.exp(-0.03)], 'no-half': [1 - 4 * lam * math.sin(dx) ** 2, 1 - 4 * 0.4377 * math.sin(dx) ** 2]})
    mode = np.sin(np.arange(1, 12) * dx)
    after = float((np.linalg.matrix_power(A, 50) @ mode)[5] / mode[5])
    part(2, 'p-grid-modes', 3, [g ** 50, after, 0.9702 ** 50], dp=3, wrong={'exact': [math.exp(-1.5)], 'power-t': [0.9702 ** 3]})
    ex = math.exp(-1.5)
    part(2, 'p-grid-modes', 4, [(ex - g ** 50) / ex, (ex - after) / ex, (0.2231 - 0.2200) / 0.2231], dp=1, pct=True,
         wrong={'absolute': [0.2231 - 0.2200], 'ratio': [0.2200 / 0.2231]})
    w = item(2, 'p-grid-modes')['parts'][3]['widget']
    own4 = round(0.9702 ** 50, 4)
    ok(abs(own4 - 0.2200) < 5e-5, f'L2 p-grid-modes p4: part 3\'s own working, 0.9702^50, is {own4} to 4 places, but part 4 restates 0.2200')
    carried = (0.2231 - own4) / 0.2231
    ok(abs(carried - w['answer']) <= w['tol']['abs'],
       f'L2 p-grid-modes p4: a learner who carries {own4} gets {100 * carried:.2f}% ({round(100 * carried, 1)} to 1 place) and is refused')


# ------------------------------------------------------------------ level 3
def bs(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    return S * Phi(d1) - K * math.exp(-r * T) * Phi(d2), d1, d2


def cn_dense(S, K, r, s, T, nx, L=1.0):
    """Crank-Nicolson on u_tau = u_xx over [-L, L], n_t = n_x/5, zero left edge, exact right edge (lesson 12),
    with a dense solve of (I - lam/2 A) u_new = (I + lam/2 A) u_old + edge terms."""
    k = 2 * r / s ** 2
    a1, a2 = (k + 1) / 2, (k - 1) / 2
    tau_end = 0.5 * s * s * T
    nt = nx // 5
    x = np.linspace(-L, L, nx + 1)
    h, dt = x[1] - x[0], tau_end / nt
    lam = dt / h ** 2
    u = np.maximum(np.exp(a1 * x) - np.exp(a2 * x), 0.0)
    n = nx - 1
    A = np.diag(np.full(n, -2.0)) + np.diag(np.ones(n - 1), 1) + np.diag(np.ones(n - 1), -1)
    Minv = np.linalg.inv(np.eye(n) - 0.5 * lam * A)
    P = np.eye(n) + 0.5 * lam * A
    edge = lambda tau: math.exp(a1 * L + a1 * a1 * tau) - math.exp(a2 * L + a2 * a2 * tau)
    tau = 0.0
    for _ in range(nt):
        rhs = P @ u[1:-1]
        rhs[-1] += 0.5 * lam * (u[-1] + edge(tau + dt))
        tau += dt
        u[1:-1] = Minv @ rhs
        u[0], u[-1] = 0.0, edge(tau)
    x0 = math.log(S / K)
    alpha, beta = -(k - 1) / 2, -(k + 1) ** 2 / 4
    return K * math.exp(alpha * x0 + beta * tau_end) * float(np.interp(x0, x, u))


def level3():
    # p-call-heat: S 80, K 75, r 4%, sigma 25%, T 0.8
    S, K, r, s, T = 80, 75, 0.04, 0.25, 0.8
    tau = 0.5 * s * s * T
    part(3, 'p-call-heat', 1, [tau, 0.03125 * 0.8], dp=3, wrong={'no-half': [s * s * T], 'unsquared': [0.5 * s * T]})
    k = 2 * r / s ** 2
    part(3, 'p-call-heat', 2, [k, 0.08 / 0.0625], dp=2, wrong={'no-two': [r / s ** 2], 'upside-down': [s ** 2 / (2 * r)]})
    V, d1, d2 = bs(S, K, r, s, T)
    x = math.log(S / K)
    a1, a2 = (k + 1) / 2, (k - 1) / 2
    arg = (x + 2 * a1 * tau) / math.sqrt(2 * tau)
    part(3, 'p-call-heat', 3, [arg, d1, 0.12154 / math.sqrt(0.05)], dp=4,
         wrong={'no-x': [2 * a1 * tau / math.sqrt(2 * tau)], 'used-a2': [(x + 2 * a2 * tau) / math.sqrt(2 * tau), d2]})
    w = item(3, 'p-call-heat')['parts'][2]['widget']
    ex_work = round(0.12154 / 0.2236, 4)
    ok(ex_work == round(arg, 4),
       f'L3 p-call-heat p3: the explanation\'s own division, 0.12154 / 0.2236, is {0.12154 / 0.2236:.5f}, {ex_work} to 4 places, not 0.5435 '
       f'(it sits {abs(ex_work - w["answer"]):.6f} from the key, band {w["tol"]["abs"]})')
    ok(abs(Phi(d1) - 0.70662) < 5e-6 and abs(Phi(d2) - 0.62549) < 5e-6 and abs(d2 - 0.3199) < 5e-5, 'L3 p-call-heat p4: given Phi values')
    # second route: the kernel integral of the heat start (lesson 10's route), then undo the variables
    ker = lambda y: np.maximum(np.exp(a1 * y) - np.exp(a2 * y), 0) * np.exp(-(x - y) ** 2 / (4 * tau)) / math.sqrt(4 * math.pi * tau)
    Vq = K * math.exp(-(k - 1) / 2 * x - (k + 1) ** 2 / 4 * tau) * trap(ker, 0.0, 6.0, 600000)
    disc = K * math.exp(-r * T)
    part(3, 'p-call-heat', 4, [V, Vq, S * 0.70662 - disc * 0.62549, 56.530 - 45.434], dp=2,
         wrong={'no-disc': [S * 0.70662 - K * 0.62549], 'swapped': [S * 0.62549 - disc * 0.70662]})
    says(3, 'p-call-heat', 4, '72.638', '56.530', '45.434')
    ok(abs(disc - 72.638) < 5e-4 and abs(80 * 0.70662 - 56.530) < 5e-4 and abs(72.638 * 0.62549 - 45.434) < 6e-4, 'L3 p-call-heat p4: printed products')

    # p-fk-claim: V_t - 0.1 V_x + 0.18 V_xx - 0.05 V = 0, V(T, x) = e^x, x = 0, two years
    part(3, 'p-fk-claim', 1, [0.18 * 2, 0.5 * 0.36 * 2], dp=2, wrong={'no-c': [2], 'double': [0.36 * 2]})
    part(3, 'p-fk-claim', 2, [2 * 0.36, 0.36 * 2.0], dp=2, wrong={'tau': [0.36], 'sd': [math.sqrt(0.72)]})
    dens = lambda y: np.exp(y) * np.exp(-(y + 0.2) ** 2 / (2 * 0.72)) / math.sqrt(2 * math.pi * 0.72)
    part(3, 'p-fk-claim', 3, [math.exp(0.16), trap(dens, -12, 12)], dp=4, wrong={'no-half': [math.exp(-0.2 + 0.72)], 'no-var': [math.exp(-0.2)]})
    # second route for V: V = e^{x + b(T - t)} in the equation gives -b - 0.1 + 0.18 - 0.05 = 0
    bb = -0.1 + 0.18 - 0.05
    part(3, 'p-fk-claim', 4, [math.exp(0.06), math.exp(bb * 2), math.exp(-0.1) * 1.1735], dp=4,
         wrong={'no-disc': [math.exp(0.16), 1.1735], 'one-year': [math.exp(-0.05) * math.exp(0.16), math.exp(-0.05) * 1.1735]})
    se = 1.0904 / math.sqrt(40000)
    part(3, 'p-fk-claim', 5, [(1.0731 - math.exp(0.06)) / se, (1.0731 - math.exp(bb * 2)) * 200 / 1.0904, (1.0731 - 1.06184) / se, (1.0731 - 1.0618) / 0.005452], dp=2,
         wrong={'sd-not-se': [(1.0731 - 1.0618) / 1.0904], 'over-n': [(1.0731 - 1.0618) / (1.0904 / 40000), (1.0731 - math.exp(0.06)) / (1.0904 / 40000)]})
    sd_true = math.exp(0.06) * math.sqrt(math.exp(0.72) - 1)
    ok(abs(sd_true - 1.0904) < 0.02, f'L3 p-fk-claim p5: the payoff\'s true sd is {sd_true:.4f}, so a sample sd of 1.0904 is plausible')

    # p-grid-no-formula: S = K = 50, r 3%, sigma 24%, T 0.5
    stated = {100: 3.7357101, 200: 3.7398157, 400: 3.7408399}
    for nx, v in stated.items():
        mine = cn_dense(50, 50, 0.03, 0.24, 0.5, nx)
        ok(abs(mine - v) < 5e-7, f'L3 p-grid-no-formula: dense Crank-Nicolson on {nx} intervals gives {mine:.7f}, the prose {v}')
    ok(abs(cn_dense(100, 100, 0.05, 0.2, 1.0, 200) - 10.4486123) < 5e-7, 'L3 the reader\'s solver reproduces lesson 12\'s 10.4486123')
    V1, V2, V4 = stated[100], stated[200], stated[400]
    da, db = V2 - V1, V4 - V2
    part(3, 'p-grid-no-formula', 1, [math.log2(da / db), math.log(da / db) / math.log(2), math.log(4.009) / math.log(2)], wrong={'ratio': [da / db, 4.009]})
    ok(abs(round(math.log2(da / db), 1) - 2.0) < 1e-9 and abs(da - 0.0041056) < 5e-8 and abs(db - 0.0010242) < 5e-8 and abs(da / db - 4.009) < 5e-4, 'L3 p-grid-no-formula p1: differences, ratio, order')
    part(3, 'p-grid-no-formula', 2, [db / 3 * 1e6, 1024.2 / 3], dp=1, wrong={'difference': [db * 1e6]})
    R = V4 + db / 3
    part(3, 'p-grid-no-formula', 3, [R, (4 * V4 - V2) / 3, 3.7408399 + 0.0003414], dp=6, wrong={'subtracted': [V4 - db / 3], 'quarter': [V4 + db / 4]})
    Vbs = bs(50, 50, 0.03, 0.24, 0.5)[0]
    ok(abs(R - Vbs) < 2e-6, f'L3 p-grid-no-formula p3: Richardson {R:.7f} against the formula {Vbs:.7f}')
    disc = 50 * math.exp(-0.015)
    _, d1, d2 = bs(50, 50, 0.03, 0.24, 0.5)
    put_bs = disc * Phi(-d2) - 50 * Phi(-d1)
    part(3, 'p-grid-no-formula', 4, [3.741181 - 50 + disc, R - 50 + disc], dp=4,
         wrong={'no-disc': [3.741181], 'v400': [V4 - 50 + disc], 'sign': [3.741181 + 50 - disc]})
    ok(abs(put_bs - (R - 50 + disc)) < 2e-6, 'L3 p-grid-no-formula p4: put against the formula')
    not_says(3, 'p-grid-no-formula', 4, '49.255582', f'50 e^(-0.015) is {disc:.6f}')
    w = item(3, 'p-grid-no-formula')['parts'][3]['widget']
    v400 = next(x for x in w['wrong'] if x['id'] == 'v400')['value']
    ok(abs(v400 - (V4 - 50 + disc)) < 5e-7, f'L3 p-grid-no-formula p4: wrong v400 is stored as {v400}; the slip gives {V4 - 50 + disc:.6f}')


def shape():
    for n, s in SETS.items():
        ok(3 <= len(s['items']) <= 5, f'L{n}: 3 to 5 problems')
        ok(any(i['difficulty'] == 5 for i in s['items']), f'L{n}: one difficulty 5')
        for i in s['items']:
            ok(3 <= len(i['parts']) <= 5 and 3 <= i['difficulty'] <= 5, f'L{n} {i["id"]}: part count and difficulty')
            for j, p in enumerate(i['parts'], 1):
                q = p['question']
                ok(any(t in q for t in ('decimal', 'whole number', 'fraction')), f'L{n} {i["id"]} p{j}: states its form')
    course = json.load(open(os.path.join(BASE, 'course.json'), encoding='utf-8'))
    for lv in course['levels']:
        sk = set()
        for l in lv['lessons']:
            sk |= set(json.load(open(os.path.join(BASE, l + '.json'), encoding='utf-8'))['skills'])
        for i in SETS[lv['n']]['items']:
            ok(set(i['skills']) <= sk, f'L{lv["n"]} {i["id"]}: skills {i["skills"]} not all carried by the level\'s lessons {sorted(sk)}')


if __name__ == '__main__':
    level1(); level2(); level3(); shape()
    print(f'{N["checks"]} checks, {N["findings"]} FINDING line(s)')
