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
    # fix pass: part 4 now asks how far 24.375 sits above the steady value (finding 10)
    part(1, 'p-grid-rod', 4, [24.375 - (15 + 50 * 0.1), float(r3[1] - far[1])], dp=3,
         wrong={'steady': [15 + 50 * 0.1], 'mean-ends': [24.375 - 45], 'left-end': [24.375 - 15]})

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
    # fix pass: the prose now calls the equation a model of the walk (finding 5), so the check reads the wording
    pr = item(1, 'p-drift-walk')['prose'] + ' ' + item(1, 'p-drift-walk')['parts'][2]['question']
    ok(abs(walk_var_rate - 2 * 1.25) > 1e-3 and 'obeys' not in pr and 'We model its density' in pr and 'the walker has' not in pr,
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

    # p-grid-modes: length pi, 12 intervals, D = 0.75, dt = 0.04 (fix pass, finding 9)
    dx = pi / 12
    lam = 0.75 * 0.04 / dx ** 2
    part(2, 'p-grid-modes', 1, [lam, 0.75 * 0.04 * 144 / pi ** 2, 0.03 / 0.068539], dp=4, wrong={'no-d': [0.04 / dx ** 2], 'unsquared': [0.03 / dx]})
    ok(abs(dx ** 2 - 0.068539) < 5e-7 and lam < 0.5, 'L2 p-grid-modes p1: dx^2 and lambda below 1/2')
    A = np.diag(np.full(11, 1 - 2 * lam)) + np.diag(np.full(10, lam), 1) + np.diag(np.full(10, lam), -1)
    eig = np.sort(np.linalg.eigvalsh(A))
    g = 1 - 4 * lam * math.sin(dx / 2) ** 2
    ok(np.abs(eig).max() < 1, 'L2 p-grid-modes p1: every grid mode stays bounded')
    part(2, 'p-grid-modes', 2, [g, float(eig[-1]), 1 - 4 * 0.4377 * 0.01704], dp=4,
         wrong={'exact': [math.exp(-0.03)], 'no-half': [1 - 4 * lam * math.sin(dx) ** 2, 1 - 4 * 0.4377 * math.sin(dx) ** 2]})
    mode = np.sin(np.arange(1, 12) * dx)
    after = float((np.linalg.matrix_power(A, 40) @ mode)[5] / mode[5])
    part(2, 'p-grid-modes', 3, [g ** 40, after, 0.9702 ** 40], dp=3, wrong={'exact': [math.exp(-1.2)], 'power-t': [0.9702 ** 1.6]})
    ex = math.exp(-1.2)
    part(2, 'p-grid-modes', 4, [(ex - g ** 40) / ex, (ex - after) / ex, (0.3012 - 0.298) / 0.3012], dp=1, pct=True,
         wrong={'absolute': [0.3012 - 0.298], 'ratio': [0.298 / 0.3012]})
    w = item(2, 'p-grid-modes')['parts'][3]['widget']
    own4 = round(0.9702 ** 40, 4)
    ok(round(0.9702 ** 40, 3) == 0.298 and '0.298 from part 3' in item(2, 'p-grid-modes')['parts'][3]['question'],
       f'L2 p-grid-modes p4: part 3\'s own working, 0.9702^40, is {round(0.9702 ** 40, 3)} to 3 places, as part 4 restates')
    carried = (0.3012 - own4) / 0.3012
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
    # Fix pass (session AF): p-call-heat, p-fk-claim and p-grid-no-formula were re-authored as p-straddle-vol,
    # p-log-contract and p-grid-budget (findings 6 to 8), so the reader's checks of the old problems are removed,
    # findings 1 and 4 with them. The solver check is kept and retargeted to the new grid prices; the delta reader
    # adds its own checks of the new parts.
    ok(abs(cn_dense(100, 100, 0.05, 0.2, 1.0, 200) - 10.4486123) < 5e-7, 'L3 the reader\'s solver reproduces lesson 12\'s 10.4486123')
    pr = item(3, 'p-grid-budget')['prose']
    for nx, v in {100: 12.9896396, 200: 12.9963192, 400: 12.9979920}.items():
        mine = cn_dense(120, 120, 0.045, 0.18, 1.25, nx)
        ok(abs(mine - v) < 5e-7 and f'{v:.7f}' in pr, f'L3 p-grid-budget: dense Crank-Nicolson on {nx} intervals gives {mine:.7f}, the prose {v}')


def shape():
    for n, s in SETS.items():
        ok(3 <= len(s['items']) <= 5, f'L{n}: 3 to 5 problems')
        ok(any(i['difficulty'] == 5 for i in s['items']), f'L{n}: one difficulty 5')
        for i in s['items']:
            ok(3 <= len(i['parts']) <= 5 and 3 <= i['difficulty'] <= 5, f'L{n} {i["id"]}: part count and difficulty')
            for j, p in enumerate(i['parts'], 1):
                q = p['question']
                form = ('expression', 'in terms of') if p['widget']['kind'] == 'expression' else ('decimal', 'whole number', 'fraction')
                ok(any(t in q for t in form), f'L{n} {i["id"]} p{j}: states its form')
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
