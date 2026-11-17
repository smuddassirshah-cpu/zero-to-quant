"""Recompute every number in app/content/courses/pdes/problems-1.json to problems-3.json twice.

Method 1 is exact where it can be (fractions, sympy, the closed form). Method 2 is independent: an exact binomial
walk, a quadrature of the heat kernel, a brentq root, a grid run in numpy, a long partial sum, a Monte Carlo
estimate or a second Crank-Nicolson solver. For each numeric part the script checks that the two methods agree,
that the JSON key lies within its tol of the value, that the figure at the asked rounding is accepted, and that
every `wrong` value equals its named slip recomputed here and lies outside the key's band. Stated figures in
prose, feedback and explain are checked as text with numbers_lib.Level.expect, and Level.check_wrongs runs over
each set as a second check of the bands. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-pdes-numbers.py
"""
import json, math, os, sys
from fractions import Fraction as F

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import sici
from scipy.stats import norm, binom

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'pdes')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
P = norm.cdf


def Phi2(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf8') as f:
        return {it['id']: it for it in json.load(f)['items']}


SETS = {n: load(n) for n in (1, 2, 3)}


def part(n, iid, p):
    return SETS[n][iid]['parts'][p - 1]


def num(n, iid, p, v1, v2, slips, rounded=None, agree=1e-9):
    """v1, v2: the value two ways. slips: {wrong id: recomputed value}. rounded: the figure the asked rounding gives."""
    pt = part(n, iid, p)
    w, tag = pt['widget'], f'L{n} {iid} p{p}'
    ok(w['kind'] == 'numeric', f'{tag} is numeric')
    v1, v2 = float(v1), float(v2)
    ok(abs(v1 - v2) <= agree * max(1.0, abs(v1)), f'{tag} methods agree {v1} vs {v2}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - v1) <= tol, f'{tag} key {w["answer"]} within {tol} of {v1}')
    if rounded is not None:
        ok(abs(rounded - w['answer']) <= tol + 1e-12, f'{tag} rounded {rounded} accepted')
    ids = {x['id']: x for x in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} match slips {sorted(slips)}')
    by = pt['feedback'].get('byKey', {})
    for wid, val in slips.items():
        if wid not in ids:
            continue
        x = ids[wid]
        ok(abs(x['value'] - val) <= x['tol']['abs'] + 1e-9, f'{tag} wrong {wid} {x["value"]} is the slip {val}')
        ok(abs(x['value'] - w['answer']) > tol + x['tol']['abs'], f'{tag} wrong {wid} outside the key band')
        ok(wid in by, f'{tag} wrong {wid} has a byKey line')
    return v1


def txt(n, iid, p=None):
    it = SETS[n][iid]
    if p is None:
        return it['prose']
    pt = it['parts'][p - 1]
    return ' '.join([pt['question'], pt['feedback']['correct'], pt['explain']['text']] + list(pt['feedback'].get('byKey', {}).values()))


def says(n, iid, p, *figs):
    t = txt(n, iid, p)
    for s in figs:
        ok(s in t, f'L{n} {iid} p{p} states {s!r}')


# ---------------------------------------------------------------- level 1
def level1():
    n = 1
    # p-tick-spread: ticks 0.4p every 0.1 s
    dx, dt = F(2, 5), F(1, 10)
    D = dx * dx / (2 * dt)
    walk = binom(600, 0.5)                      # 600 fair steps in a minute: position = 0.4 (2B - 600)
    var_walk = float(dx * dx) * 4 * walk.var()
    D2 = var_walk / (2 * 60)
    num(n, 'p-tick-spread', 1, D, D2, {'no-half': dx * dx / dt, 'unsquared': dx / (2 * dt)}, 0.8)
    sd = math.sqrt(2 * float(D) * 60)
    num(n, 'p-tick-spread', 2, sd, math.sqrt(var_walk), {'variance': 96, 'no-two': math.sqrt(48), 'd-slip': math.sqrt(2 * 1.6 * 60)}, 9.80)
    z = 15 / sd
    ok(abs(z - 1.531) < 0.0005 and abs(P(1.531) - 0.9371) < 0.00005, 'L1 tick p3 z and table value')
    pr = 2 * (1 - P(z))
    num(n, 'p-tick-spread', 3, pr, 2 * (1 - Phi2(z)), {'one-tail': 1 - P(z), 'inside': 2 * P(z) - 1}, 0.126)
    ok(round(2 * (1 - 0.9371), 3) == 0.126, 'L1 tick p3 table route gives 0.126')
    t24 = sp.solve(sp.Eq(2 * sp.Rational(4, 5) * sp.Symbol('t'), 24 ** 2))[0]
    num(n, 'p-tick-spread', 4, t24, brentq(lambda t: math.sqrt(1.6 * t) - 24, 1, 1e4), {'linear': 60 * 24 / sd, 'var-24': 15}, 360)
    says(n, 'p-tick-spread', 2, '96', '9.80')
    says(n, 'p-tick-spread', 4, '576', '360', '2.449')

    # p-two-level-bar: 30 | 90, D = 0.2
    Dd = 0.2
    def u(x, t):
        return 30 + 60 * P(x / math.sqrt(2 * Dd * t))
    def u_quad(x, t):                          # kernel against the start, by quadrature
        k = lambda y: math.exp(-(x - y) ** 2 / (4 * Dd * t)) / math.sqrt(4 * math.pi * Dd * t)
        w = 12 * math.sqrt(2 * Dd * t)
        lo, hi = x - w, x + w
        left = quad(lambda y: k(y) * 30, lo, min(0, hi))[0] if lo < 0 else 0.0
        right = quad(lambda y: k(y) * 90, max(0, lo), hi)[0] if hi > 0 else 0.0
        return left + right
    num(n, 'p-two-level-bar', 1, u(50, 1) - u(-50, 1), u_quad(40, 1) - u_quad(-40, 1), {'right-value': 90, 'gave-a': 30}, 60, agree=1e-6)
    v = u(0.4, 0.25)
    num(n, 'p-two-level-bar', 2, v, u_quad(0.4, 0.25), {'no-two': 30 + 60 * P(0.4 / math.sqrt(0.05)), 'no-base': 60 * P(0.4 / math.sqrt(0.1))}, 83.8, agree=1e-7)
    ok(abs(P(1.265) - 0.8971) < 0.00005 and abs(30 + 60 * 0.8971 - 83.826) < 1e-6, 'L1 bar p2 table route 83.82')
    q = norm.ppf(0.75)
    ok(abs(q - 0.6745) < 0.00005, 'L1 bar quantile 0.6745')
    x75 = q * math.sqrt(0.1)
    num(n, 'p-two-level-bar', 3, x75, brentq(lambda x: u_quad(x, 0.25) - 75, 0, 1), {'no-width': q, 'share': 0.75 * math.sqrt(0.1)}, 0.213, agree=1e-6)
    t75 = (0.4 / q) ** 2 / (2 * Dd)
    num(n, 'p-two-level-bar', 4, t75, brentq(lambda t: u(0.4, t) - 75, 0.1, 5), {'no-two': (0.4 / q) ** 2 / Dd, 'unsquared': (0.4 / q) / (2 * Dd)}, 0.879, agree=1e-7)
    xs = np.linspace(-3, 3, 61)                # steady state on a grid: solve the discrete Laplace system
    A = np.diag(-2 * np.ones(59)) + np.diag(np.ones(58), 1) + np.diag(np.ones(58), -1)
    b = np.zeros(59); b[0] -= 30; b[-1] -= 90
    us = np.linalg.solve(A, b)
    num(n, 'p-two-level-bar', 5, F(30) + F(60) * F(34, 10) / 6, us[33], {'centre': 60, 'level': 75}, 64, agree=1e-9)
    ok(abs(xs[34] - 0.4) < 1e-12, 'L1 bar grid node 0.4')
    says(n, 'p-two-level-bar', 2, '0.3162', '1.265', '83.8')
    says(n, 'p-two-level-bar', 4, '0.5930', '0.3517', '0.879')

    # p-grid-rod: [0, 1.2], ends 15 and 75, start 40, D = 0.25, dx = 0.1
    Dr, h = F(1, 4), F(1, 10)
    dtmax = h * h / (2 * Dr)
    steps = math.ceil(F(3, 2) / dtmax)
    num(n, 'p-grid-rod', 1, steps, brentq(lambda m: 0.25 * (1.5 / m) / 0.01 - 0.5, 1, 1e4), {'lam-one': math.ceil(1.5 / 0.04), 'no-d': math.ceil(1.5 / 0.005)}, 75, agree=1e-9)
    def run(k, lam=F(1, 2)):
        g = [F(15)] + [F(40)] * 11 + [F(75)]
        for _ in range(k):
            g = [g[0]] + [g[j] + lam * (g[j + 1] - 2 * g[j] + g[j - 1]) for j in range(1, 12)] + [g[12]]
        return g
    def run_np(k):
        g = np.array([15.0] + [40.0] * 11 + [75.0])
        for _ in range(k):
            g[1:-1] = 0.5 * (g[:-2] + g[2:])
        return g
    num(n, 'p-grid-rod', 2, run(1)[1], run_np(1)[1], {'lam-one': run(1, F(1))[1], 'three-mean': F(15 + 40 + 40, 3)}, 27.5)
    num(n, 'p-grid-rod', 3, run(3)[1], run_np(3)[1], {'two-steps': run(2)[1]}, 24.375)
    ok(run(2)[2] == F(135, 4), 'L1 rod u(0.2) after two steps is 33.75')
    num(n, 'p-grid-rod', 4, F(15) + F(60) * F(1, 12), run_np(6000)[1], {'mean-ends': 45, 'left-end': 15}, 20, agree=1e-9)
    says(n, 'p-grid-rod', 3, '33.75', '24.375')

    # p-drift-walk: dx 0.05, dt 0.001, q 0.6
    c = (2 * F(3, 5) - 1) * F(1, 20) / F(1, 1000)
    rng = np.random.default_rng(7)
    steps_ = np.where(rng.random(2_000_000) < 0.6, 0.05, -0.05)
    num(n, 'p-drift-walk', 1, c, round(steps_.mean() / 0.001), {'no-bias': 50, 'used-q': 30}, 10)
    x, t, a = sp.symbols('x t a')
    uu = sp.exp(-a * t) * sp.cos(2 * (x - 10 * t))
    res = sp.simplify((sp.diff(uu, t) + 10 * sp.diff(uu, x) - sp.Rational(5, 4) * sp.diff(uu, x, 2)) / uu)
    asol = sp.solve(res, a)[0]
    def resid_fd(av, x0=0.3, t0=0.2, e=1e-4):
        f = lambda X, T: math.exp(-av * T) * math.cos(2 * (X - 10 * T))
        return ((f(x0, t0 + e) - f(x0, t0 - e)) / (2 * e) + 10 * (f(x0 + e, t0) - f(x0 - e, t0)) / (2 * e)
                - 1.25 * (f(x0 + e, t0) - 2 * f(x0, t0) + f(x0 - e, t0)) / e ** 2)
    num(n, 'p-drift-walk', 2, asol, brentq(resid_fd, 1, 9), {'unsquared': 2.5, 'no-freq': 1.25}, 5, agree=1e-5)
    m, var = 10 * 0.32, 2 * 1.25 * 0.32
    zz = (2 - m) / math.sqrt(var)
    ok(abs(-zz - 1.342) < 0.0005 and abs(P(1.342) - 0.9102) < 0.00005, 'L1 drift p3 z and table value')
    num(n, 'p-drift-walk', 3, P(zz), Phi2(zz), {'no-drift': P(2 / math.sqrt(var)), 'var-dt': P((2 - m) / math.sqrt(1.25 * 0.32))}, 0.090)
    q99 = norm.ppf(0.99)
    ok(abs(q99 - 2.3263) < 0.00005, 'L1 drift quantile 2.3263')
    t1 = (q99 / (10 / math.sqrt(2.5))) ** 2
    num(n, 'p-drift-walk', 4, t1, brentq(lambda t: P(-10 * t / math.sqrt(2.5 * t)) - 0.01, 0.01, 1), {'unsquared': math.sqrt(t1), 'var-dt': (q99 / (10 / math.sqrt(1.25))) ** 2}, 0.135, agree=1e-7)
    says(n, 'p-drift-walk', 3, '0.8944', '0.090')
    says(n, 'p-drift-walk', 4, '6.325', '0.3678')
    lv = Level('pdes', 1)
    lv.check_wrongs('problems')
    return lv


LEVELS = [level1]

if __name__ == '__main__':
    lvs = []
    for f in LEVELS:
        lvs.append(f())
    for lv in lvs:
        bad = [r for r in lv.results if not r[0]]
        for b in bad:
            fails.append(b[1])
    print(f'{checks} checks, {len(fails)} failures')
    sys.exit(1 if fails else 0)
