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

    # p-grid-modes: L = pi, N = 12, D = 0.5
    dx = math.pi / 12
    dtm = sp.pi ** 2 / 144 / (2 * sp.Rational(1, 2))       # the stability bound, quoted only in the feedback
    ok(abs(float(dtm) - 0.068539) < 5e-7, 'L2 grid dx^2 = 0.068539')
    lam = 0.5 * 0.06 / dx ** 2
    num(n, 'p-grid-modes', 1, lam, 0.03 / float(dtm), {'no-d': 0.06 / dx ** 2, 'unsquared': 0.03 / dx}, 0.4377)
    ok(lam < 0.5, 'L2 grid lambda below one half')
    g = 1 - 4 * lam * math.sin(dx / 2) ** 2
    M = np.eye(11) * (1 - 2 * lam) + np.eye(11, k=1) * lam + np.eye(11, k=-1) * lam
    ev = sorted(np.linalg.eigvalsh(M))
    num(n, 'p-grid-modes', 2, g, ev[-1], {'exact': math.exp(-0.03), 'no-half': 1 - 4 * lam * math.sin(dx) ** 2}, 0.9702, agree=1e-9)
    ok(abs(ev[0] - (1 - 4 * lam * math.sin(11 * dx / 2) ** 2)) < 1e-9 and abs(ev[0]) < 1, 'L2 grid top mode bounded')
    xg = np.arange(1, 12) * dx
    v = np.sin(xg)
    for _ in range(50):
        v = M @ v
    num(n, 'p-grid-modes', 3, g ** 50, v[5] / math.sin(xg[5]), {'exact': math.exp(-1.5), 'power-t': 0.9702 ** 3}, 0.220, agree=1e-9)
    ok(abs(0.9702 ** 50 - 0.2200) < 0.0005, 'L2 grid p3 rounded factor lands in the band')
    short = (math.exp(-1.5) - g ** 50) / math.exp(-1.5)
    num(n, 'p-grid-modes', 4, short, 1 - math.exp(50 * math.log(g) + 1.5), {'absolute': 0.2231 - 0.2200, 'ratio': 0.2200 / 0.2231}, 0.014, agree=1e-9)
    ok(abs((0.2231 - 0.2200) / 0.2231 - short) < 0.0005, 'L2 grid p4 rounded inputs land in the band')
    ok(part(2, 'p-grid-modes', 4)['widget'].get('unit') == '%', 'L2 grid p4 carries unit %')
    says(n, 'p-grid-modes', 1, '0.068539', '0.4377')
    says(n, 'p-grid-modes', 2, '0.01704', '0.9702')
    says(n, 'p-grid-modes', 4, '0.2231', '0.014', '1.4%')
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


def level3():
    n = 3
    # p-call-heat
    S, K, r, s, T = 80, 75, F(4, 100), F(1, 4), F(4, 5)
    tau = s * s * T / 2
    num(n, 'p-call-heat', 1, tau, 0.5 * 0.25 ** 2 * 0.8, {'no-half': s * s * T, 'unsquared': s * T / 2}, 0.025)
    k = 2 * r / (s * s)
    num(n, 'p-call-heat', 2, k, 0.08 / 0.0625, {'no-two': r / (s * s), 'upside-down': s * s / (2 * r)}, 1.28)
    V, d1, d2 = bs_call(80, 75, 0.04, 0.25, 0.8)
    x = math.log(80 / 75)
    arg = (x + (float(k) + 1) * float(tau)) / math.sqrt(2 * float(tau))
    num(n, 'p-call-heat', 3, arg, d1, {'no-x': (float(k) + 1) * float(tau) / math.sqrt(2 * float(tau)), 'used-a2': d2}, 0.5435)
    ok(abs(d2 - 0.3199) < 0.00005 and abs(P(d1) - 0.70662) < 0.000005 and abs(P(d2) - 0.62549) < 0.000005, 'L3 call d2 and the two Phi values')
    ST = lambda z: 80 * math.exp((0.04 - 0.03125) * 0.8 + 0.25 * math.sqrt(0.8) * z)
    Vq = math.exp(-0.032) * quad(lambda z: max(ST(z) - 75, 0) * norm.pdf(z), -12, 12, points=[-0.54], limit=200)[0]
    disc = 75 * math.exp(-0.032)
    num(n, 'p-call-heat', 4, V, Vq, {'no-disc': 80 * 0.70662 - 75 * 0.62549, 'swapped': 80 * 0.62549 - disc * 0.70662}, 11.10, agree=1e-7)
    ok(abs(80 * 0.70662 - disc * 0.62549 - V) < 0.0005, 'L3 call table route lands on 11.10')
    says(n, 'p-call-heat', 3, '0.06454', '0.057', '0.12154', '0.5435')
    says(n, 'p-call-heat', 4, '72.638', '56.530', '45.434', '11.10')

    # p-fk-claim: V_t - 0.1 V_x + 0.18 V_xx - 0.05 V = 0, V(T, x) = e^x, x = 0, T - t = 2
    c = F(18, 100)
    tau2 = c * 2
    num(n, 'p-fk-claim', 1, tau2, 0.36 / 2 * 2, {'no-c': 2, 'double': 2 * tau2}, 0.36)
    var = 2 * tau2
    num(n, 'p-fk-claim', 2, var, 2 * 0.18 * 2, {'tau': tau2, 'sd': math.sqrt(0.72)}, 0.72)
    E = math.exp(-0.2 + 0.36)
    Eq = quad(lambda y: math.exp(y) * norm.pdf(y, -0.2, math.sqrt(0.72)), -12, 12)[0]
    num(n, 'p-fk-claim', 3, E, Eq, {'no-half': math.exp(-0.2 + 0.72), 'no-var': math.exp(-0.2)}, 1.1735, agree=1e-9)
    Vf = math.exp(-0.1) * E
    rng = np.random.default_rng(11)               # Monte Carlo with exact steps of the drifted Brownian motion
    XT = -0.2 + math.sqrt(0.72) * rng.standard_normal(4_000_000)
    Vmc = math.exp(-0.1) * np.exp(XT).mean()
    num(n, 'p-fk-claim', 4, Vf, math.exp(0.06), {'no-disc': E, 'one-year': math.exp(-0.05) * E}, 1.0618)
    ok(abs(Vmc - Vf) < 0.003, f'L3 fk Monte Carlo {Vmc:.5f} near {Vf:.5f}')
    sd = math.exp(-0.1) * math.sqrt(math.exp(-0.4 + 2 * 0.72) - math.exp(-0.4 + 0.72))
    ok(abs(sd - 1.0904) < 0.00005, 'L3 fk stated sd 1.0904 is the true sd of the discounted payoff')
    se = 1.0904 / math.sqrt(40000)
    zz = (1.0731 - Vf) / se
    num(n, 'p-fk-claim', 5, zz, (1.0731 - math.exp(0.06)) * 200 / 1.0904, {'sd-not-se': (1.0731 - Vf) / 1.0904, 'over-n': (1.0731 - 1.0618) / (1.0904 / 40000)}, 2.07)
    ok(abs((1.0731 - 1.0618) / 0.005452 - 2.07) < 0.008, 'L3 fk rounded V gives 2.07 in band')
    says(n, 'p-fk-claim', 5, '0.005452', '2.07')

    # p-grid-no-formula: S = K = 50, r = 3%, sigma = 24%, T = 0.5
    Vs = {nx: cn_price(50, 50, 0.03, 0.24, 0.5, nx) for nx in (100, 200, 400)}
    stated = {100: 3.7357101, 200: 3.7398157, 400: 3.7408399}
    for nx in stated:
        ok(abs(Vs[nx] - stated[nx]) < 5e-8, f'L3 CN on {nx} intervals is {Vs[nx]:.7f}')
    V1, V2, V4 = stated[100], stated[200], stated[400]
    d_a, d_b = V2 - V1, V4 - V2
    pord = math.log2(d_a / d_b)
    num(n, 'p-grid-no-formula', 1, pord, math.log(d_a / d_b) / math.log(2), {'ratio': d_a / d_b}, 2.0)
    est = d_b / 3 * 1e6
    c_ = d_b / (3 * (2 / 400) ** 2)                 # second method: fit V = V_inf - c h^2 to the 200 and 400 grids
    vinf = V4 + c_ * (2 / 400) ** 2
    num(n, 'p-grid-no-formula', 2, est, (vinf - V4) * 1e6, {'difference': d_b * 1e6}, 341.4, agree=1e-6)
    R = V4 + d_b / 3
    num(n, 'p-grid-no-formula', 3, R, vinf, {'subtracted': V4 - d_b / 3, 'quarter': V4 + d_b / 4}, 3.741181)
    Vbs = bs_call(50, 50, 0.03, 0.24, 0.5)[0]
    ok(abs(R - Vbs) < 1e-6, f'L3 Richardson {R:.7f} matches the formula {Vbs:.7f}')
    put = R - 50 + 50 * math.exp(-0.015)
    d1b = (math.log(1) + (0.03 + 0.24 ** 2 / 2) * 0.5) / (0.24 * math.sqrt(0.5)); d2b = d1b - 0.24 * math.sqrt(0.5)
    put_bs = 50 * math.exp(-0.015) * P(-d2b) - 50 * P(-d1b)
    num(n, 'p-grid-no-formula', 4, put, put_bs, {'no-disc': R, 'v400': V4 - 50 + 50 * math.exp(-0.015), 'sign': R + 50 - 50 * math.exp(-0.015)}, 2.9968, agree=1e-6)
    says(n, 'p-grid-no-formula', 1, '0.0041056', '0.0010242', '4.009')
    says(n, 'p-grid-no-formula', 4, '49.255582', '2.9968')
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
