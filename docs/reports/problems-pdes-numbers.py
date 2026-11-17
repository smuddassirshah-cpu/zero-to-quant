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
    steady = F(15) + F(60) * F(1, 12)
    num(n, 'p-grid-rod', 4, run(3)[1] - steady, run_np(3)[1] - run_np(6000)[1], {'steady': steady, 'mean-ends': run(3)[1] - 45, 'left-end': run(3)[1] - 15}, 4.375, agree=1e-9)
    says(n, 'p-grid-rod', 3, '33.75', '24.375')
    says(n, 'p-grid-rod', 4, '24.375', '4.375', '20')

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


# ---------------------------------------------------------------- level 2
def level2():
    n = 2
    X = sp.Symbol('x')
    pi = sp.pi
    # p-tent-rod: L = 2, D = 0.1, tent of height 6
    L, D = 2, sp.Rational(1, 10)
    rate = D * (pi / L) ** 2
    h = 1e-3                                       # second method: lowest eigenvalue of the discrete Laplacian on [0, 2]
    m = int(round(L / h)) - 1
    lam_grid = 4 / h ** 2 * math.sin(math.pi * h / (2 * L)) ** 2
    num(n, 'p-tent-rod', 1, rate, 0.1 * lam_grid, {'unsquared': 0.1 * math.pi / L, 'length-one': 0.1 * math.pi ** 2}, 0.2467, agree=1e-6)
    ok(m == 1999, 'L2 tent grid size')
    f = sp.Piecewise((6 * X, X <= 1), (6 * (2 - X), True))
    def bk(k):
        return sp.Rational(2, L) * (sp.integrate(6 * X * sp.sin(k * pi * X / L), (X, 0, 1)) + sp.integrate(6 * (2 - X) * sp.sin(k * pi * X / L), (X, 1, 2)))
    def bk_quad(k):
        g = lambda x: (6 * x if x <= 1 else 6 * (2 - x)) * math.sin(k * math.pi * x / L)
        return quad(g, 0, 1)[0] + quad(g, 1, 2)[0]
    b1, b3 = sp.nsimplify(bk(1)), sp.nsimplify(bk(3))
    ok(sp.simplify(b1 - 48 / pi ** 2) == 0 and sp.simplify(b3 + sp.Rational(48, 9) / pi ** 2) == 0, 'L2 tent b1 = 48/pi^2, b3 = -48/(9 pi^2)')
    num(n, 'p-tent-rod', 2, b1, bk_quad(1), {'one-over-l': float(b1) / 2, 'peak': 6}, 4.8634, agree=1e-8)
    r1 = float(rate)
    def centre(t, ks, coef=lambda k: float(bk(k))):
        return sum(coef(k) * math.exp(-r1 * k * k * t) * math.sin(k * math.pi / 2) for k in ks)
    c2 = centre(1.5, (1, 3))
    num(n, 'p-tent-rod', 3, c2, centre(1.5, (1, 3), bk_quad), {'one-term': centre(1.5, (1,)), 'sign': centre(1.5, (1,)) - abs(centre(1.5, (3,)))}, 3.38, agree=1e-8)
    ok(abs(4.8634 * math.exp(-0.2467 * 1.5) + 0.5404 * math.exp(-9 * 0.2467 * 1.5) - c2) < 0.001, 'L2 tent p3 rounded inputs land in the band')
    t1 = math.log(float(b1)) / r1
    full = lambda t: centre(t, range(1, 60, 2), bk_quad) - 1
    num(n, 'p-tent-rod', 4, t1, brentq(full, 1, 20), {'peak': math.log(6) / r1, 'sign': -t1}, 6.41, agree=1e-5)
    ok(abs(math.log(4.8634) / 0.2467 - 6.41) < 0.005, 'L2 tent p4 rounded inputs give 6.41')
    ok(abs(float(b3)) * math.exp(-9 * r1 * 6.41) < 1e-6, 'L2 tent k = 3 term below 1e-6 at t = 6.41')
    says(n, 'p-tent-rod', 1, '2.4674', '0.2467')
    says(n, 'p-tent-rod', 3, '0.370', '3.331', '3.359', '0.019')

    # p-exp-series: e^x on (-pi, pi)
    shp = math.sinh(math.pi)
    b1e = sp.integrate(sp.exp(X) * sp.sin(X), (X, -pi, pi)) / pi
    num(n, 'p-exp-series', 1, b1e, quad(lambda x: math.exp(x) * math.sin(x), -math.pi, math.pi)[0] / math.pi, {'no-pi': shp, 'sign': -shp / math.pi}, 3.6761, agree=1e-9)
    b3e = 3 * 2 / 10 * float(b1e)
    num(n, 'p-exp-series', 2, b3e, quad(lambda x: math.exp(x) * math.sin(3 * x), -math.pi, math.pi)[0] / math.pi, {'sign': -b3e, 'no-k': 2 / 10 * float(b1e)}, 2.2056, agree=1e-9)
    ok(round(0.6 * 3.6761, 4) == 2.2057 and abs(0.6 * 3.6761 - b3e) <= part(n, 'p-exp-series', 2)['widget']['tol']['abs'], 'L2 exp p2 rounded b1 gives 2.2057, in the band')
    says(n, 'p-exp-series', 2, '2.2057', '2.2056')
    says(n, 'p-exp-series', 5, '11.5487', '11.5920')
    kk = sp.Symbol('k', positive=True)
    slope = sp.limit(sp.log(2 * kk / (1 + kk ** 2)) / sp.log(kk), kk, sp.oo)
    big = 1e6
    num(n, 'p-exp-series', 3, slope, (math.log(2 * 2 * big / (1 + 4 * big ** 2)) - math.log(2 * big / (1 + big ** 2))) / math.log(2), {'minus-two': -2, 'plus-one': 1}, -1, agree=1e-5)
    a = lambda k: (-1) ** k * 2 * shp / (math.pi * (1 + k * k))
    ks = np.arange(1, 2_000_001)
    s_pi = shp / math.pi + np.sum(2 * shp / (math.pi * (1 + ks.astype(float) ** 2)))   # a_k cos(k pi) = 2 sinh(pi)/(pi(1+k^2)); b_k sin(k pi) = 0
    num(n, 'p-exp-series', 4, math.cosh(math.pi), s_pi, {'left': math.exp(math.pi), 'right': math.exp(-math.pi), 'half-gap': shp}, 11.5920, agree=1e-6)
    ok(abs(a(1) + shp / math.pi) < 1e-12, 'L2 exp a_1 sign')
    Sig = (math.pi / math.tanh(math.pi) - 1) / 2
    Sig_sum = float(np.sum(1 / (1 + np.arange(1, 4_000_001, dtype=float) ** 2))) + 1 / 4_000_000   # tail ~ 1/N
    num(n, 'p-exp-series', 5, Sig, Sig_sum, {'no-half': 2 * Sig, 'keep-one': (2 * Sig + 1) / 2, 'used-left': (math.pi * math.exp(math.pi) / shp - 1) / 2}, 1.0767, agree=1e-9)
    ok(abs((11.5920 * math.pi / 11.5487 - 1) / 2 - Sig) < 0.00006, 'L2 exp p5 rounded inputs give 1.0767')
    ok(abs(math.pi * math.cosh(math.pi) / shp - 3.15335) < 0.000005, 'L2 exp pi coth pi = 3.15335')
    says(n, 'p-exp-series', 1, '11.5487', '3.6761')
    says(n, 'p-exp-series', 4, '23.1407', '0.0432', '11.5920')
    says(n, 'p-exp-series', 5, '3.15335', '1.0767')

    # p-grid-modes: L = pi, N = 12, D = 0.75, dt = 0.04, 40 steps to t = 1.6
    dx = math.pi / 12
    dtm = sp.pi ** 2 / 144                                  # dx^2, quoted in the feedback
    ok(abs(float(dtm) - 0.068539) < 5e-7, 'L2 grid dx^2 = 0.068539')
    lam = 0.75 * 0.04 / dx ** 2
    num(n, 'p-grid-modes', 1, lam, 0.03 / float(dtm), {'no-d': 0.04 / dx ** 2, 'unsquared': 0.03 / dx}, 0.4377)
    ok(lam < 0.5, 'L2 grid lambda below one half')
    g = 1 - 4 * lam * math.sin(dx / 2) ** 2
    M = np.eye(11) * (1 - 2 * lam) + np.eye(11, k=1) * lam + np.eye(11, k=-1) * lam
    ev = sorted(np.linalg.eigvalsh(M))
    num(n, 'p-grid-modes', 2, g, ev[-1], {'exact': math.exp(-0.03), 'no-half': 1 - 4 * lam * math.sin(dx) ** 2}, 0.9702, agree=1e-9)
    ok(abs(ev[0] - (1 - 4 * lam * math.sin(11 * dx / 2) ** 2)) < 1e-9 and abs(ev[0]) < 1, 'L2 grid top mode bounded')
    xg = np.arange(1, 12) * dx
    v = np.sin(xg)
    for _ in range(40):
        v = M @ v
    num(n, 'p-grid-modes', 3, g ** 40, v[5] / math.sin(xg[5]), {'exact': math.exp(-1.2), 'power-t': 0.9702 ** 1.6}, 0.298, agree=1e-9)
    ok(abs(0.9702 ** 40 - 0.298) < 0.0005 and round(0.9702 ** 40, 3) == 0.298, 'L2 grid p3 rounded factor gives 0.298, in the band')
    ok(abs(math.exp(-1.2) - 0.3012) < 5e-5, 'L2 grid p4 e^-1.2 = 0.3012')
    short = (math.exp(-1.2) - g ** 40) / math.exp(-1.2)
    num(n, 'p-grid-modes', 4, short, 1 - math.exp(40 * math.log(g) + 1.2), {'absolute': 0.3012 - 0.298, 'ratio': 0.298 / 0.3012}, 0.011, agree=1e-9)
    w4 = part(2, 'p-grid-modes', 4)['widget']
    work4 = (0.3012 - 0.298) / 0.3012
    for typed in (1.0, 1.1, 1.06, 1.13, 100 * (0.3012 - 0.2982) / 0.3012):   # 1 dp roundings, the printed working, the exact value, a carried 0.2982
        ok(abs(typed / 100 - w4['answer']) <= w4['tol']['abs'] + 1e-12, f'L2 grid p4 takes {typed}%')
    for typed in (0.9, 1.2):
        ok(abs(typed / 100 - w4['answer']) > w4['tol']['abs'], f'L2 grid p4 refuses {typed}%')
    ok(abs(work4 - 0.010624) < 1e-6 and round(work4, 3) == 0.011, 'L2 grid p4 printed working 0.0106, about 0.011')
    rat = [x for x in w4['wrong'] if x['id'] == 'ratio'][0]
    ok(all(abs(t / 100 - rat['value']) <= rat['tol']['abs'] for t in (98.9, 99.0)) and abs(0.298 / 0.3012 - rat['value']) <= rat['tol']['abs'], 'L2 grid p4 ratio band takes 98.9 and 99.0')
    ok(rat['tol']['abs'] <= 0.0015, 'L2 grid p4 ratio band no wider than its roundings need')
    ok(w4.get('unit') == '%', 'L2 grid p4 carries unit %')
    says(n, 'p-grid-modes', 1, '0.068539', '0.4377', '0.75')
    says(n, 'p-grid-modes', 2, '0.01704', '0.9702')
    says(n, 'p-grid-modes', 3, '0.298', '1.6 \\div 0.04 = 40')
    says(n, 'p-grid-modes', 4, '0.3012', '0.298', '0.011', '1.1%', '0.9704')
    lv = Level('pdes', 2)
    lv.check_wrongs('problems')
    return lv


# ---------------------------------------------------------------- level 3
def bs_call(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    return S * P(d1) - K * math.exp(-r * T) * P(d2), d1, d2


def cn_price(S, K, r, s, T, nx, L=1.0):
    """Crank-Nicolson in heat variables on [-L, L], n_t = n_x/5, u = 0 on the left, exact u on the right (as lesson 12)."""
    k = 2 * r / s ** 2; a = -(k - 1) / 2; b = -(k + 1) ** 2 / 4; tau = 0.5 * s * s * T
    x = np.linspace(-L, L, nx + 1); dxx = x[1] - x[0]; nt = nx // 5; dt = tau / nt; lam = dt / dxx ** 2
    u = np.maximum(np.exp((k + 1) / 2 * x) - np.exp((k - 1) / 2 * x), 0)
    def right(t):
        Sx = K * math.exp(L)
        V = bs_call(Sx, K, r, s, 2 * t / s ** 2)[0]
        return V / K / math.exp(a * L + b * t)
    nn = nx - 1
    lo = np.full(nn, -lam / 2); di = np.full(nn, 1 + lam); up = np.full(nn, -lam / 2)
    t = 0.0
    for _ in range(nt):
        rhs = u[1:-1] + lam / 2 * (u[2:] - 2 * u[1:-1] + u[:-2])
        t += dt
        uR = right(t)
        rhs[-1] += lam / 2 * uR
        cp, dp = np.zeros(nn), np.zeros(nn)          # Thomas algorithm
        cp[0], dp[0] = up[0] / di[0], rhs[0] / di[0]
        for i in range(1, nn):
            mm = di[i] - lo[i] * cp[i - 1]
            cp[i] = up[i] / mm
            dp[i] = (rhs[i] - lo[i] * dp[i - 1]) / mm
        un = np.zeros(nn); un[-1] = dp[-1]
        for i in range(nn - 2, -1, -1):
            un[i] = dp[i] - cp[i] * un[i + 1]
        u = np.concatenate([[0.0], un, [uR]])
    return K * math.exp(a * x[nx // 2] + b * tau) * u[nx // 2]


def shown(value, printed, dp, label):
    """A printed figure is the value at full precision, rounded to dp places (not a string match)."""
    ok(round(value, dp) == round(printed, dp) and abs(value - printed) <= 0.5 * 10 ** -dp + 1e-12, f'{label}: {value:.8g} prints as {printed}')


def expr_part(n, iid, p, key, accepts, slips):
    """An expression part: the key equals the derived form, each accept form equals it, each slip differs."""
    pt = part(n, iid, p)
    w, tag = pt['widget'], f'L{n} {iid} p{p}'
    ok(w['kind'] == 'expression', f'{tag} is an expression')
    ids = {x['id']: x['tex'] for x in w.get('wrong', [])}
    ok(set(ids) == set(slips), f'{tag} wrong ids {sorted(ids)} match slips {sorted(slips)}')
    by = pt['feedback'].get('byKey', {})
    syms = sorted(key.free_symbols, key=str)
    pts = [dict(zip(syms, v)) for v in ((0.37,), (1.3,), (2.6,))] if len(syms) == 1 else [{}]
    def same(a, b):
        return all(abs(complex(a.subs(q)) - complex(b.subs(q))) < 1e-9 for q in pts)
    for f in accepts:
        ok(same(f, key), f'{tag} accept form {f} equals the key')
    for wid, f in slips.items():
        ok(not same(f, key), f'{tag} slip {wid} differs from the key')
        ok(wid in by, f'{tag} wrong {wid} has a byKey line')


def level3():
    n = 3
    tau_, kk = sp.symbols('tau k', positive=True)

    # p-straddle-vol: r = 0, S = K = 80, T = 0.75, straddle 9.60
    K, T, Q = 80, 0.75, 9.60
    a = sp.Rational(1, 2)
    arg = sp.simplify((0 + 2 * a * tau_) / sp.sqrt(2 * tau_))
    ok(sp.simplify(arg - sp.sqrt(tau_ / 2)) == 0, 'L3 straddle p1 argument is sqrt(tau/2)')
    expr_part(n, 'p-straddle-vol', 1, sp.sqrt(tau_ / 2),
              [sp.sqrt(tau_) / sp.sqrt(2), tau_ / sp.sqrt(2 * tau_), sp.sqrt(2 * tau_) / 2],
              {'no-half': sp.sqrt(2 * tau_), 'numerator': tau_, 'no-root': sp.Rational(1, 2)})
    # the call at r = 0 from the lemma equals Black-Scholes: K e^{-tau/4}(e^{tau/4}Phi(z) - e^{tau/4}Phi(-z)) = K(2 Phi(z) - 1)
    for t_ in (0.004, 0.0113, 0.03):
        z = math.sqrt(t_ / 2)
        ok(abs(K * (2 * P(z) - 1) - bs_call(K, K, 1e-12, math.sqrt(2 * t_ / T), T)[0]) < 1e-8, f'L3 straddle C = K(2 Phi - 1) at tau = {t_}')
    sig_iv = brentq(lambda s_: 2 * bs_call(K, K, 1e-12, s_, T)[0] - Q, 0.01, 1.0, xtol=1e-14)   # method 2: implied vol by root finding
    Ph = (1 + Q / 2 / K) / 2
    num(n, 'p-straddle-vol', 2, Ph, P(sig_iv * math.sqrt(T) / 2), {'whole': (1 + Q / K) / 2, 'c-over-k': Q / 2 / K}, 0.53)
    zq = norm.ppf(0.53)
    ok(abs(zq - 0.07527) < 5e-6, f'L3 straddle table value Phi^-1(0.53) = {zq:.6f}')
    tau1 = 2 * zq ** 2
    num(n, 'p-straddle-vol', 3, tau1, 0.5 * sig_iv ** 2 * T, {'unsquared': 2 * 0.07527, 'halved': 0.07527 ** 2 / 2, 'no-two': 0.07527 ** 2}, 0.01133, agree=1e-8)
    ok(abs(2 * 0.07527 ** 2 - tau1) <= part(n, 'p-straddle-vol', 3)['widget']['tol']['abs'], 'L3 straddle p3 printed working in the band')
    shown(0.07527 ** 2, 0.0056656, 7, 'L3 straddle p3 0.07527^2')
    shown(2 * 0.07527 ** 2, 0.01133, 5, 'L3 straddle p3 tau')
    sig = math.sqrt(2 * tau1 / T)
    num(n, 'p-straddle-vol', 4, sig, sig_iv, {'no-half': math.sqrt(0.01133 / T), 'calendar': math.sqrt(2 * 0.01133), 'no-root': 2 * 0.01133 / T}, 0.1738, agree=1e-8)
    w4 = part(n, 'p-straddle-vol', 4)['widget']
    ok(w4.get('unit') == '%', 'L3 straddle p4 carries unit %')
    ok(abs(math.sqrt(2 * 0.01133 / T) - w4['answer']) <= w4['tol']['abs'], 'L3 straddle p4 from the rounded tau lands in the band')
    shown(2 * 0.01133, 0.02266, 5, 'L3 straddle p4 2 tau')
    shown(0.02266 / 0.75, 0.030213, 6, 'L3 straddle p4 sigma^2')
    shown(math.sqrt(0.030213), 0.1738, 4, 'L3 straddle p4 sigma')
    ok(abs(2 * bs_call(K, K, 1e-12, 0.1738, T)[0] - Q) < 0.005, 'L3 straddle at 17.38% reprices to 9.60')
    says(n, 'p-straddle-vol', 2, '4.80', '0.06', '0.5300')
    says(n, 'p-straddle-vol', 4, '17.38%', '0.030213')

    # p-log-contract: pays 1000 ln(S_T/K), K = S_0 = 64, sigma 28%, r 2%, T 1.5
    r, s, T2, N = F(2, 100), F(28, 100), F(3, 2), 1000
    k = 2 * r / s ** 2
    tau2 = s * s * T2 / 2
    x, c = sp.symbols('x c')
    v = sp.exp(-kk * tau_) * (x + c * tau_)
    res = sp.simplify((sp.diff(v, tau_) - sp.diff(v, x, 2) - (kk - 1) * sp.diff(v, x) + kk * v) / sp.exp(-kk * tau_))
    csol = sp.solve(res, c)[0]
    ok(sp.simplify(csol - (kk - 1)) == 0, 'L3 log p1 c = k - 1 by substitution')
    expr_part(n, 'p-log-contract', 1, kk - 1, [-1 + kk], {'sign': 1 - kk, 'no-minus': kk, 'plus': kk + 1})
    # second method for the whole claim: put V(S, t) into the Black-Scholes equation in S and t
    S_, t_ = sp.symbols('S t', positive=True)
    rr, ss = sp.Rational(2, 100), sp.Rational(28, 100)
    Vst = N * sp.exp(-rr * (sp.Rational(3, 2) - t_)) * (sp.log(S_ / 64) + (rr - ss ** 2 / 2) * (sp.Rational(3, 2) - t_))
    pde = sp.simplify(sp.diff(Vst, t_) + ss ** 2 * S_ ** 2 / 2 * sp.diff(Vst, S_, 2) + rr * S_ * sp.diff(Vst, S_) - rr * Vst)
    ok(pde == 0, 'L3 log V(S, t) solves the Black-Scholes equation')
    mean = (k - 1) * tau2
    ok(mean == F(-288, 10000), 'L3 log mean is exactly -0.0288')
    ok(k * tau2 == r * T2, 'L3 log k tau = rT')
    shown(float(k), 0.5102, 4, 'L3 log k')
    shown(float(tau2), 0.0588, 4, 'L3 log tau')
    disc = math.exp(-float(k * tau2))
    V = N * disc * float(mean)
    rng = np.random.default_rng(23)                               # method 3: Feynman-Kac by simulation, exact log steps
    lnST = (0.02 - 0.0392) * 1.5 + 0.28 * math.sqrt(1.5) * rng.standard_normal(4_000_000)
    pay = N * math.exp(-0.03) * lnST
    Vmc, se = pay.mean(), pay.std() / math.sqrt(len(pay))
    ok(abs(Vmc - V) < 3 * se, f'L3 log Monte Carlo {Vmc:.3f} within 3 se ({se:.3f}) of {V:.4f}')
    num(n, 'p-log-contract', 2, V, float(Vst.subs({S_: 64, t_: 0})), {'no-disc': N * float(mean), 'used-k': N * disc * float(k * tau2), 'sign': -V}, -27.95, agree=1e-9)
    shown(disc, 0.97045, 5, 'L3 log discount')
    shown(1000 * 0.97045 * -0.0288, -27.95, 2, 'L3 log p2 printed product')
    shown(1000 * disc, 970.45, 2, 'L3 log p3 slope')
    xb = 27.95 / 970.45
    rise = math.exp(xb) - 1
    xroot = brentq(lambda S: float(Vst.subs({S_: S, t_: 0})), 60, 70, xtol=1e-12)
    num(n, 'p-log-contract', 3, rise, xroot / 64 - 1, {'log-return': 0.0288, 'no-disc': math.exp(27.95 / 1000) - 1}, 0.0292, agree=2e-6)
    ok(part(n, 'p-log-contract', 3)['widget'].get('unit') == '%', 'L3 log p3 carries unit %')
    shown(xb, 0.028801, 6, 'L3 log p3 x')
    shown(math.exp(0.028801), 1.02922, 5, 'L3 log p3 ratio')
    shown(64 * math.exp(0.0288), 65.87, 2, 'L3 log p3 break-even price')
    sdl = math.sqrt(float(2 * tau2))
    ok(2 * tau2 == s * s * T2 and float(2 * tau2) == 0.1176, 'L3 log variance 2 tau = sigma^2 T = 0.1176')
    zl = float(mean) / sdl
    shown(sdl, 0.34293, 5, 'L3 log p4 sd')
    shown(-zl, 0.0840, 4, 'L3 log p4 z')
    shown(P(0.0840), 0.5335, 4, 'L3 log p4 table value')
    _, d1l, d2l = bs_call(64, 64, 0.02, 0.28, 1.5)
    num(n, 'p-log-contract', 4, P(zl), P(d2l), {'wrong-side': 0.5335, 'no-drift': 0.5}, 0.4665, agree=1e-9)
    ok(abs((lnST > 0).mean() - P(zl)) < 0.001, f'L3 log p4 simulated chance {(lnST > 0).mean():.4f} near {P(zl):.5f}')
    ok(abs(1 - 0.5335 - part(n, 'p-log-contract', 4)['widget']['answer']) <= part(n, 'p-log-contract', 4)['widget']['tol']['abs'], 'L3 log p4 table route in the band')
    says(n, 'p-log-contract', 2, '0.97045', '27.95', '0.5102')
    says(n, 'p-log-contract', 3, '0.028801', '1.02922', '2.92%', '65.87')
    says(n, 'p-log-contract', 4, '0.34293', '0.0840', '0.4665')

    # p-grid-budget (parts 1 and 2 re-authored, session AH): S = K = 120, r 4.5%, sigma 18%, T 1.25.
    # Route 1: cn_price above (Thomas sweep, edge from the formula). Route 2: a banded solve with scipy and the
    # heat-variable edge e^{a1 L + a1^2 t} - e^{a2 L + a2^2 t}, written apart from route 1.
    from scipy.linalg import solve_banded
    def cn_banded(S, K, r, sg, T, nx, L=1.0):
        k = 2 * r / sg ** 2; a1, a2 = (k + 1) / 2, (k - 1) / 2; te = 0.5 * sg * sg * T
        h = 2 * L / nx; nt = nx // 5; dt = te / nt; lam = dt / h / h
        xg = -L + h * np.arange(nx + 1)
        u = np.maximum(np.exp(a1 * xg) - np.exp(a2 * xg), 0.0)
        edge = lambda t: math.exp(a1 * L + a1 * a1 * t) - math.exp(a2 * L + a2 * a2 * t)
        ab = np.zeros((3, nx - 1)); ab[0, 1:] = -lam / 2; ab[1, :] = 1 + lam; ab[2, :-1] = -lam / 2
        for j in range(nt):
            rhs = (1 - lam) * u[1:-1] + lam / 2 * (u[:-2] + u[2:])
            rhs[-1] += lam / 2 * edge((j + 1) * dt)
            u = np.concatenate([[0.0], solve_banded((1, 1), ab, rhs), [edge((j + 1) * dt)]])
        return K * math.exp(-a2 * math.log(S / K) - a1 * a1 * te) * u[nx // 2]
    opt = (120, 120, 0.045, 0.18, 1.25)
    Vs = {nx: cn_price(*opt, nx) for nx in (200, 300, 400, 1000)}
    Vb = {nx: cn_banded(*opt, nx) for nx in Vs}
    for nx in Vs:
        ok(abs(Vs[nx] - Vb[nx]) < 1e-9, f'L3 grid: both solvers agree on {nx} intervals ({Vs[nx]:.9f}, {Vb[nx]:.9f})')
    ok(abs(cn_banded(100, 100, 0.05, 0.2, 1, 100) - 10.4427214) < 5e-8 and abs(cn_banded(100, 100, 0.05, 0.2, 1, 200) - 10.4486123) < 5e-8,
       'L3 grid: route 2 gives lesson 12 prices on 100 and 200 intervals')
    stated = {200: 12.9963192, 300: 12.9975576}
    for nx, v in stated.items():
        shown(Vs[nx], v, 7, f'L3 grid price on {nx} intervals')
    says(3, 'p-grid-budget', None, '12.9963192', '12.9975576', 'n_x/5', '4.5', '18', '1.25')
    gap = stated[300] - stated[200]
    shown(gap, 0.0012384, 7, 'L3 grid gap of the two runs')
    h2, h3, h4 = 2 / 200, 2 / 300, 2 / 400
    ok(abs((h2 ** 2 - h3 ** 2) - 1 / 18000) < 1e-18 and abs(h3 - 1 / 150) < 1e-15 and abs(1e-4 - 1 / 22500 - 1 / 18000) < 1e-18,
       'L3 grid: h200^2 - h300^2 = 10^-4 - 1/22500 = 1/18000')
    C1 = gap / (h2 ** 2 - h3 ** 2)                                  # route 1: the gap over the change in h^2
    C2 = float(np.linalg.lstsq(np.array([[1, -h2 ** 2], [1, -h3 ** 2]]), np.array([stated[200], stated[300]]), rcond=None)[0][1])
    #                                                                 route 2: solve V_h = V - C h^2 for V and C together
    num(3, 'p-grid-budget', 1, C1, C2, {'n-not-h': gap / (1 / 200 ** 2 - 1 / 300 ** 2), 'no-square': gap / (h2 - h3),
        'one-run': gap / h2 ** 2}, rounded=22.29, agree=1e-7)
    ok(abs(18000 * 0.0012384 - C1) < 1e-9 and round(C1, 2) == 22.29, 'L3 grid p1 prints 18,000 x 0.0012384 = 22.29')
    Cfull = (Vs[300] - Vs[200]) / (h2 ** 2 - h3 ** 2)
    ok(round(Cfull, 2) == 22.29, f'L3 grid p1 the unrounded runs give C = {Cfull:.5f}, also 22.29')
    ok(abs(gap / (1 / 200 ** 2 - 1 / 300 ** 2) / 4 - C1) < 1e-9, 'L3 grid p1 slip n-not-h is four times the key')
    w1 = part(3, 'p-grid-budget', 1)['widget']
    for typed in (22.29,):
        ok(abs(typed - w1['answer']) < w1['tol']['abs'] - 0.003, f'L3 grid p1 takes {typed} away from the band edge')
    for typed in (22.28, 22.30):
        ok(abs(typed - w1['answer']) > w1['tol']['abs'] + 0.003, f'L3 grid p1 refuses {typed} away from the band edge')
    # part 2: C h^2 at 400 intervals
    e400 = C1 * h4 ** 2 * 1e6
    e400b = (stated[300] - stated[200]) * (h4 ** 2 / (h2 ** 2 - h3 ** 2)) * 1e6
    num(3, 'p-grid-budget', 2, e400, e400b, {'unit-length': 22.29 / 400 ** 2 * 1e6, 'wrong-run': 22.29 * h3 ** 2 * 1e6}, rounded=557, agree=1e-9)
    carried2 = 22.29 * 0.000025 * 1e6
    w2 = part(3, 'p-grid-budget', 2)['widget']
    ok(round(carried2) == 557 and round(e400) == 557 and abs(carried2 - w2['answer']) < w2['tol']['abs'], f'L3 grid p2 carried 22.29 gives {carried2:.2f}, also 557')
    ok(abs(22.29 * 0.000025 - 0.000557) < 1e-6, 'L3 grid p2 prints 22.29 x 0.000025 = 0.000557')
    ok(abs(round(e400, 2) - 557.28) < 1e-9, 'L3 grid p3 restates the unrounded 557.28')
    Vbs = bs_call(*opt)[0]
    true400 = (Vbs - Vs[400]) * 1e6
    ok(1.005 < true400 / e400 < 1.02, f'L3 grid "about 1% higher": the 400 run is {true400:.2f}e-6 below the formula, {true400 / e400:.4f} times the prediction')
    for wid, typed in (('unit-length', 139), ('wrong-run', 991)):
        x = [w for w in w2['wrong'] if w['id'] == wid][0]
        ok(abs(typed - x['value']) < x['tol']['abs'] - 0.1, f'L3 grid p2 slip {wid} takes {typed}')
    # part 3: 2.25 times the work is 1.5 times the intervals (work n_x^2/5), so divide by 2.25
    s3 = 557.28 / 1.5 ** 2
    n600 = next(m for m in range(400, 2000, 5) if abs(m * m / 5 - 2.25 * 400 * 400 / 5) < 1e-9)
    num(3, 'p-grid-budget', 3, s3, 557.28 * (400 / n600) ** 2, {'per-interval': 557.28 / 2.25 ** 2, 'first-order': 557.28 / 1.5}, rounded=247.68, agree=1e-9)
    ok(n600 == 600 and 600 // 5 == 120, 'L3 grid p3 600 intervals (n_t 120) carry 2.25 times the work')
    w3 = part(3, 'p-grid-budget', 3)['widget']
    for typed in (247.68,):           # 557.28 / 2.25 is 247.68 exactly: rounded and cut to 2 places alike
        ok(abs(typed - w3['answer']) < w3['tol']['abs'] - 0.005, f'L3 grid p3 takes {typed} clear of the band edge')
    for typed in (247.67, 247.69):
        ok(abs(typed - w3['answer']) > w3['tol']['abs'] + 0.002, f'L3 grid p3 refuses {typed} clear of the band edge')
    ok(abs(C1 * (2 / 600) ** 2 * 1e6 - w3['answer']) < 1e-6 and abs(Cfull * (2 / 600) ** 2 * 1e6 - w3['answer']) < w3['tol']['abs'],
       'L3 grid p3 key is C h^2 at 600 intervals too (rounded and unrounded C)')
    ok(abs(557.28 / 2.25 - 247.68) < 1e-9, 'L3 grid p3 prints 557.28 / 1.5^2 = 247.68')
    for wid, typed in (('per-interval', 110.08), ('first-order', 371.52)):
        x = [w for w in w3['wrong'] if w['id'] == wid][0]
        ok(abs(typed - x['value']) < 1e-9 and x['tol']['abs'] >= 0.005, f'L3 grid p3 slip {wid} is {typed} exactly')
    Vs[600] = cn_price(*opt, 600)
    ok(abs(Vs[600] - cn_banded(*opt, 600)) < 1e-9, 'L3 grid both solvers agree on 600 intervals')
    true600 = (Vbs - Vs[600]) * 1e6
    ok(round(true600) == 253, f'L3 grid the 600 run is {true600:.2f}e-6 below the formula, "about 253"')
    ok(true600 > s3 and (Vs[400] - Vs[200]) / (Vs[600] - Vs[400]) > 0, 'L3 grid the true gap exceeds the order-2 prediction')
    # the observed order slips under 2: the error constant C grows on finer grids
    Cs = [(Vbs - Vs[nx]) * nx ** 2 / 4 for nx in (200, 300, 400, 600, 1000)]
    ok(all(c2 > c1 for c1, c2 in zip(Cs, Cs[1:])), f'L3 grid the constant creeps up on finer grids {[round(c, 3) for c in Cs]}')
    # part 4: the paths grow by the square of the error factor
    num(3, 'p-grid-budget', 4, (557.28 / s3) ** 2, 2.25 ** 2, {'linear': 2.25, 'root': 1.5}, rounded=5.06, agree=1e-9)
    car4 = (557.28 / 247.68) ** 2
    w4 = part(3, 'p-grid-budget', 4)['widget']
    ok(abs(557.28 / 247.68 - 2.25) < 1e-12 and round(car4, 2) == 5.06, f'L3 grid p4 carried 557.28 / 247.68 = 2.25, squared {car4}')
    for typed in (5.06,):             # 5.0625 rounds and cuts to 5.06
        ok(abs(typed - w4['answer']) < w4['tol']['abs'] - 0.002, f'L3 grid p4 takes {typed} clear of the edge')
    for typed in (5.05, 5.07):
        ok(abs(typed - w4['answer']) > w4['tol']['abs'] + 0.002, f'L3 grid p4 refuses {typed} clear of the edge')
    ok(2.25 < 0.5 * 5.0625, 'L3 grid p4 explain: the work grows by under half the factor the paths need')
    says(3, 'p-grid-budget', 3, '557.28', '247.68', '600', '253', '1.5')
    says(3, 'p-grid-budget', 4, '557.28', '247.68', '2.25', '5.06')
    lv = Level('pdes', 3)
    lv.check_wrongs('problems')
    return lv


def shape():
    lessons = {1: ['l1', 'l2', 'l3', 'l4'], 2: ['l5', 'l6', 'l7', 'l8'], 3: ['l9', 'l10', 'l11', 'l12']}
    skills = {1: {'pe-heat'}, 2: {'pe-fourier', 'pe-heat'}, 3: {'pe-bs', 'pe-heat', 'pe-fk', 'pe-fd'}}
    for lvn, items in SETS.items():
        if items is None:
            continue
        diffs = [it['difficulty'] for it in items.values()]
        ok(3 <= len(items) <= 5 and all(3 <= d <= 5 for d in diffs) and 5 in diffs, f'L{lvn} set shape and a difficulty 5')
        parts = [p for it in items.values() for p in it['parts']]
        typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
        ok(typed * 3 >= 2 * len(parts), f'L{lvn} typed share {typed} of {len(parts)}')
        ok(all(set(it['skills']) <= skills[lvn] for it in items.values()), f'L{lvn} skills from the level')
        ok(all(3 <= len(it['parts']) <= 5 for it in items.values()), f'L{lvn} 3 to 5 parts each')


LEVELS = [level1, level2, level3]

if __name__ == '__main__':
    lvs = []
    for n_, f in enumerate(LEVELS, 1):
        if SETS[n_] is not None:
            lvs.append(f())
    shape()
    for lv in lvs:
        bad = [r for r in lv.results if not r[0]]
        for b in bad:
            fails.append(b[1])
    print(f'{checks} checks, {len(fails)} failures')
    sys.exit(1 if fails else 0)
