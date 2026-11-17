"""Recompute every number in app/content/courses/ito/problems-<n>.json twice (docs/briefs/chained.md check 1).

Levels 1 to 3, one block per set. Method 1 is exact or closed form (fractions, sympy, the formula the lesson
teaches). Method 2 takes another route: the binomial law of the trades, Monte Carlo with a fixed seed, numerical
integration of the normal density, sympy's own differentiation for Itô's lemma, root finding for the touch note,
and enumeration of the coarse path.

For each numeric part: both methods agree; the key lies within its tol of them; every `wrong` value matches its
named slip, lies outside the key band, does not overlap another slip and is no wider than its value; byKey covers
the wrongs exactly; a non-whole key's question states its form. Every decimal printed in a part's feedback and
explain is either in the item's stem or the part's question, or listed in that part's `shown` check and equal to the
recomputed value at the printed places. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-ito-numbers.py
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp
from scipy import integrate, optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ito')
fails, checks = [], 0
FORM = re.compile(r'decimal|places?\b|significant|nearest|percentage|per cent|fraction', re.I)
Phi = stats.norm.cdf
rng = np.random.default_rng(20261117)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def close(a, b, t):
    return abs(a - b) <= t


def load(n):
    d = json.load(open(os.path.join(COURSE, f'problems-{n}.json'), encoding='utf-8'))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'ito', f'problems-{n}: header')
    ok(3 <= len(d['items']) <= 5, f'problems-{n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'problems-{n}: no difficulty 5')
    return {it['id']: it for it in d['items']}


def nquad_normal_tail(z):
    """Second route to Phi: integrate the standard normal density."""
    return integrate.quad(lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi), -np.inf, z)[0]


def mc(f, n=400000):
    return f(rng.standard_normal(n))


def numeric(item, k, m1, m2, slips, agree=1e-6, shown=None):
    """slips: {id: value recomputed from the slip}."""
    p = item['parts'][k - 1]
    tag = f"{item['id']} part {k}"
    w = p['widget']
    ok(w['kind'] == 'numeric', f'{tag}: kind')
    key, tol = w['answer'], w['tol']['abs']
    ok(close(m1, m2, agree), f'{tag}: methods disagree {m1} {m2}')
    ok(close(key, m1, tol), f'{tag}: key {key} vs {m1}')
    if abs(key - round(key)) > 1e-9:
        ok(bool(FORM.search(p['question'])), f'{tag}: form not stated')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs {sorted(slips)}')
    ok(set(p['feedback'].get('byKey', {})) == set(wrongs), f'{tag}: byKey ids')
    bands = []
    for wid, x in wrongs.items():
        v, t = x['value'], x['tol']['abs']
        ok(close(v, slips.get(wid, 1e99), max(t, 1e-9)), f'{tag}: wrong {wid} {v} vs slip {slips.get(wid)}')
        ok(abs(v - key) > t + tol, f'{tag}: wrong {wid} overlaps key')
        ok(v == 0 or t <= abs(v), f'{tag}: wrong {wid} band wider than value')
        bands.append((v - t, v + t, wid))
    bands.sort()
    for a, b in zip(bands, bands[1:]):
        ok(a[1] < b[0], f'{tag}: wrongs {a[2]} and {b[2]} overlap')
    check_shown(item, k, shown or {})


def check_shown(item, k, shown):
    p = item['parts'][k - 1]
    tag = f"{item['id']} part {k}"
    texts = [p['feedback']['correct'], p['feedback']['generic'], p['explain']['text']] + list(p['feedback'].get('byKey', {}).values())
    if p['widget']['kind'] == 'choice':
        texts += [o.get('why', '') for o in p['widget']['options']]
    printed = set()
    for t in texts:
        for s in re.findall(r'(?<![\w.])-?\d+\.\d+|(?<![\w.])-?\d{1,3}(?:,\d{3})+\.\d+', t):
            printed.add(s.replace(',', ''))
    stem = (item.get('prose', '') + ' ' + p['question']).replace('{,}', '').replace(',', '')
    stem += ' ' + ' '.join(str(float(x) / 100) for x in re.findall(r'(\d+(?:\.\d+)?)\\?%', stem))
    for s in printed:
        if s in stem or s.lstrip('-') in stem:
            continue
        ok(s in shown or s.lstrip('-') in shown, f'{tag}: printed {s} not checked')
    for s, v in shown.items():
        dp = len(s.split('.')[1]) if '.' in s else 0
        ok(close(float(s), v, 0.5 * 10 ** -dp + 1e-12), f'{tag}: shown {s} vs {v}')
        ok(any(s in t.replace('{,}', '').replace(',', '') for t in texts), f'{tag}: shown {s} not in text')


def choice(item, k, key_id):
    p = item['parts'][k - 1]
    w = p['widget']
    tag = f"{item['id']} part {k}"
    corr = [o['id'] for o in w['options'] if o.get('correct')]
    ok(corr == [key_id], f'{tag}: keyed option {corr}')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{tag}: why missing')


def expression(item, k, answer, wrong, sym):
    p = item['parts'][k - 1]
    w = p['widget']
    tag = f"{item['id']} part {k}"
    ok(w['kind'] == 'expression', f'{tag}: kind')
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    tr = standard_transformations + (implicit_multiplication_application,)
    parse = lambda t: parse_expr(t.replace('\\frac{1}{2}', '(1/2)*').replace('\\sigma', 'sigma').replace('\\mu', 'mu').replace('^', '**'),
                                 local_dict=sym, transformations=tr)
    ok(sp.simplify(parse(w['answer']) - answer) == 0, f'{tag}: answer {w["answer"]}')
    for a in w.get('accept', []):
        ok(sp.simplify(parse(a) - answer) == 0, f'{tag}: accept {a}')
    got = {x['id']: x['tex'] for x in w['wrong']}
    ok(set(got) == set(wrong) == set(p['feedback'].get('byKey', {})), f'{tag}: wrong ids')
    for wid, ex in wrong.items():
        ok(sp.simplify(parse(got[wid]) - ex) == 0, f'{tag}: wrong {wid}')
        ok(sp.simplify(ex - answer) != 0, f'{tag}: wrong {wid} equals key')


# ===================================================================== level 1
def level1():
    global rng
    L1 = load(1)

    # p-maker-tally: 625 trades of +-40, win chance 0.51
    it = L1['p-maker-tally']
    n, a, p = 625, 40, Fr(51, 100)
    m_trade = a * p - a * (1 - p)
    e_day = n * m_trade
    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k, n, 0.51)
    e_day_binom = float(np.sum(pmf * (40 * (2 * k - n))))
    numeric(it, 1, float(e_day), e_day_binom,
            {'wins-only': n * a * 0.51, 'half-edge': n * a * 0.01, 'per-trade-count': n * 0.02}, agree=1e-6,
            shown={'0.8': float(m_trade), '0.02': 0.02, '0.49': 0.49})
    qv = n * a * a
    paths = rng.choice([-40, 40], size=(200, n), p=[0.49, 0.51])
    qv_sim = float(np.unique((paths ** 2).sum(axis=1))[0])
    ok(len(np.unique((paths ** 2).sum(axis=1))) == 1, 'p-maker-tally: squared sum varies by path')
    var_day = float(n * (a * a - m_trade ** 2))
    numeric(it, 2, qv, qv_sim, {'variance': var_day, 'abs-sum': n * a}, shown={'0.8': float(m_trade)})
    sigma = math.sqrt(qv)
    sd5 = sigma * math.sqrt(5)
    sd5_mc = float(np.std(sigma * rng.standard_normal((200000, 5)).sum(axis=1)))
    numeric(it, 3, sd5, sd5_mc, {'sd-times-t': 5 * sigma, 'one-day': sigma}, agree=15)
    mean5 = 5 * float(e_day)
    z = -mean5 / sd5
    numeric(it, 4, Phi(z), nquad_normal_tail(z),
            {'sd-times-t': Phi(-mean5 / (5 * sigma)), 'no-drift': 0.5, 'ends-up': 1 - Phi(z), 'one-day': Phi(-mean5 / sigma)},
            agree=1e-8, shown={'1.1180': -z, '2236.07': sd5, '0.1318': Phi(z)})
    ok(close(float(np.mean(mean5 + sd5 * rng.standard_normal(400000) < 0)), Phi(z), 0.003), 'p-maker-tally part 4: simulation')

    # p-quarter-rally: GBM S0 45, mu 13%, sigma 35%, S_0.25 = 52
    it = L1['p-quarter-rally']
    mu, s, tl, s25 = 0.13, 0.35, 0.75, 52.0
    nu = mu - s * s / 2
    sd_inc = s * math.sqrt(tl)
    w_inc = math.sqrt(tl) * rng.standard_normal(400000)
    numeric(it, 1, sd_inc, float(np.std(s * w_inc)), {'full-year': s, 'variance': s * s * tl, 'past-quarter': s * math.sqrt(0.25)},
            agree=2e-3, shown={'0.3031': sd_inc, '0.75': tl})
    med = s25 * math.exp(nu * tl)
    S1 = s25 * np.exp(nu * tl + s * w_inc)
    numeric(it, 2, med, float(np.median(S1)), {'mean': s25 * math.exp(mu * tl), 'from-start': 45 * math.exp(nu), 'whole-year': s25 * math.exp(nu)},
            agree=0.2, shown={'0.0515625': nu * tl, '0.06125': s * s / 2, '0.06875': nu, '54.75': med, '0.75': tl})
    mean1 = med * math.exp(s * s * tl / 2)
    numeric(it, 3, mean1, float(np.mean(S1)), {'median': med, 'full-factor': med * math.exp(s * s * tl), 'full-year': s25 * math.exp(mu)},
            agree=0.15, shown={'0.0459375': s * s * tl / 2, '0.091875': s * s * tl, '0.0975': mu * tl, '57.33': mean1})
    z = (math.log(45 / 52) - nu * tl) / sd_inc
    numeric(it, 4, Phi(z), float(np.mean(S1 < 45)),
            {'full-year-sd': Phi((math.log(45 / 52) - nu * tl) / s), 'no-rally': Phi(-nu / s), 'upper': 1 - Phi(z)},
            agree=3e-3, shown={'0.6471': -z, '0.2588': Phi(z), '0.3031': sd_inc})

    # p-realised-then-risk: 84 days, sum r^2 = 0.0147, S0 64, mu 9%
    it = L1['p-realised-then-risk']
    T, m = Fr(1, 3), 84
    sig2 = Fr(147, 10000) / T
    sig = math.sqrt(sig2)
    sim_r = 0.21 * math.sqrt(1 / 252) * rng.standard_normal((20000, m))
    sig_hat = np.sqrt((sim_r ** 2).sum(axis=1) / float(T))
    numeric(it, 1, sig, float(np.mean(sig_hat)), {'not-annual': math.sqrt(0.0147), 'variance': float(sig2), 'times-days': math.sqrt(0.0147 * 252)},
            agree=1e-3, shown={'0.0441': float(sig2), '0.21': sig})
    sd_est = float(sig2) * math.sqrt(2 / m)
    sd_est_exact = math.sqrt(float(sig2 ** 2 * 2 * T * (T / m) / T ** 2))
    numeric(it, 2, sd_est, sd_est_exact, {'no-sigma': math.sqrt(2 / m), 'sum-not-rate': sd_est * float(T), 'variance': sd_est ** 2},
            agree=1e-12, shown={'0.006805': sd_est})
    ok(close(float(np.std((sim_r ** 2).sum(axis=1) / float(T))), sd_est, 2e-4), 'p-realised-then-risk part 2: simulation')
    nu1 = 0.09 - float(sig2) / 2
    z3 = (math.log(60 / 64) - nu1) / sig
    numeric(it, 3, Phi(z3), nquad_normal_tail(z3),
            {'no-drag': Phi((math.log(60 / 64) - 0.09) / sig), 'upper': 1 - Phi(z3), 'not-annual': Phi((math.log(60 / 64) - (0.09 - 0.0147 / 2)) / math.sqrt(0.0147))},
            agree=1e-8, shown={'0.6309': -z3, '0.02205': float(sig2) / 2, '0.06795': nu1, '0.2641': Phi(z3), '0.1212': math.sqrt(0.0147)})
    sig2h = float(sig2) + 2 * sd_est
    sgh = math.sqrt(sig2h)
    nuh = 0.09 - sig2h / 2
    z4 = (math.log(60 / 64) - nuh) / sgh
    sg_wrong = sig + 2 * sd_est
    numeric(it, 4, Phi(z4), float(np.mean(64 * np.exp(nuh + sgh * rng.standard_normal(400000)) < 60)),
            {'unchanged': Phi(z3), 'sd-on-sigma': Phi((math.log(60 / 64) - (0.09 - sg_wrong ** 2 / 2)) / sg_wrong), 'same-drift': Phi((math.log(60 / 64) - nu1) / sgh)},
            agree=3e-3, shown={'0.05771': sig2h, '0.2402': sgh, '0.02885': sig2h / 2, '0.06115': nuh, '0.5232': -z4, '0.3004': Phi(z4), '0.06795': nu1})
    # rounded route stays in the band
    sg_r = math.sqrt(0.0441 + 2 * 0.006805)
    ok(close(Phi((math.log(60 / 64) - (0.09 - sg_r ** 2 / 2)) / sg_r), it['parts'][3]['widget']['answer'], 0.0005), 'p-realised-then-risk part 4: rounded route')

# ===================================================================== level 2
def level2():
    global rng
    L2 = load(2)
    mu_s, sg_s, x_s, t_s = sp.symbols('mu sigma x t', positive=True)
    SYM = {'mu': mu_s, 'sigma': sg_s, 'w': sp.Symbol('w')}

    it = L2['p-cable-inverse']
    f = 1 / x_s
    drift = sp.simplify((mu_s * x_s * sp.diff(f, x_s) + sp.Rational(1, 2) * sg_s ** 2 * x_s ** 2 * sp.diff(f, x_s, 2)) / f)
    ok(sp.simplify(drift - (sg_s ** 2 - mu_s)) == 0, 'p-cable-inverse part 1: Ito drift')
    expression(it, 1, sg_s ** 2 - mu_s, {'chain-only': -mu_s, 'half': sg_s ** 2 / 2 - mu_s, 'signs': mu_s - sg_s ** 2}, SYM)
    mu, s, T = 0.02, 0.12, 3
    EY = 0.8 * math.exp((s * s - mu) * T)
    Xt = 1.25 * np.exp((mu - s * s / 2) * T + s * math.sqrt(T) * rng.standard_normal(1000000))
    numeric(it, 2, EY, float(np.mean(1 / Xt)), {'inverse-mean': 1 / (1.25 * math.exp(mu * T)), 'median': 0.8 * math.exp(-(mu - s * s / 2) * T)},
            agree=3e-4, shown={'0.0056': -(s * s - mu), '0.0168': -(s * s - mu) * T, '0.7867': EY, '0.0144': s * s, '0.02': mu, '0.8': 0.8})
    prod = 1.25 * math.exp(mu * T) * EY
    numeric(it, 3, prod, float(np.mean(Xt) * np.mean(1 / Xt)), {'one': 1.0, 'median-y': 1.25 * math.exp(mu * T) * 0.8 * math.exp(-(mu - s * s / 2) * T)},
            agree=1e-3, shown={'0.0432': s * s * T, '1.0441': prod, '0.0168': -(s * s - mu) * T})
    mu_root = float(sp.solve(sp.Eq(drift.subs(sg_s, sp.Rational(12, 100)), 0), mu_s)[0])
    numeric(it, 4, s * s, mu_root, {'log-flat': s * s / 2, 'zero': 0.0, 'sigma': s}, shown={'0.0144': s * s, '0.12': s})

    it = L2['p-cube-path']
    W = [Fr(0), Fr(3, 10), Fr(-2, 10), Fr(4, 10), Fr(6, 10)]
    d = [W[i + 1] - W[i] for i in range(4)]
    left = sum(W[i] ** 2 * d[i] for i in range(4))
    left2 = float(np.dot(np.array(W[:-1], dtype=float) ** 2, np.diff(np.array(W, dtype=float))))
    numeric(it, 1, float(left), left2,
            {'right-point': float(sum(W[i + 1] ** 2 * d[i] for i in range(4))), 'ordinary': float(W[-1] ** 3 / 3), 'no-square': float(sum(W[i] * d[i] for i in range(4)))},
            shown={'-0.045': float(W[1] ** 2 * d[1]), '0.09': 0.09, '0.16': 0.16, '0.04': 0.04, '0.024': float(W[2] ** 2 * d[2]), '0.032': float(W[3] ** 2 * d[3]), '0.011': float(left), '0.072': 0.072})
    cube = sum(x ** 3 for x in d)
    ok(cube == Fr(126, 1000), 'p-cube-path: cube sum 0.126')
    mid = sum(W[i] * d[i] ** 2 for i in range(4))
    mid_from_identity = (W[-1] ** 3 - 3 * left - cube) / 3
    numeric(it, 2, float(mid_from_identity), float(mid), {'no-third': float(W[-1] ** 3 - 3 * left - cube), 'no-cube': float((W[-1] ** 3 - 3 * left) / 3)},
            shown={'0.057': float(W[-1] ** 3 - 3 * left - cube), '0.019': float(mid)})
    choice(it, 3, 'time-integral')
    # limit check by simulation: sum W (dW)^2 against int W dt on fine grids
    nst = 20000
    dW = math.sqrt(1 / nst) * rng.standard_normal((50, nst))
    Wf = np.cumsum(dW, axis=1) - dW
    ok(float(np.max(np.abs((Wf * dW ** 2).sum(axis=1) - (Wf / nst).sum(axis=1)))) < 0.05, 'p-cube-path part 3: limit by simulation')
    w = sp.Symbol('w')
    coef = sp.Rational(1, 2) * sp.diff(w ** 3, w, 2)
    ok(sp.simplify(coef - 3 * w) == 0, 'p-cube-path part 4: Ito coefficient')
    expression(it, 4, 3 * SYM['w'], {'no-half': 6 * SYM['w'], 'ordinary': sp.Integer(0), 'first': 3 * SYM['w'] ** 2}, SYM)

    it = L2['p-results-vol']
    v = Fr(16, 100) * Fr(1, 4) + Fr(225, 10000) * Fr(3, 4)
    v2 = integrate.quad(lambda t: (0.4 if t < 0.25 else 0.15) ** 2, 0, 1, points=[0.25])[0]
    numeric(it, 1, float(v), v2, {'average-first': (0.4 * 0.25 + 0.15 * 0.75) ** 2, 'no-weights': 0.16 + 0.0225, 'not-squared': 0.4 * 0.25 + 0.15 * 0.75},
            shown={'0.056875': float(v), '0.16': 0.16, '0.0225': 0.0225, '0.2125': 0.4 * 0.25 + 0.15 * 0.75, '0.75': 0.75, '0.25': 0.25})
    sbar = math.sqrt(v)
    # second route: simulate the integral of sigma(t) dW on a grid and take its sd
    grid = 400
    dWs = math.sqrt(1 / grid) * rng.standard_normal((100000, grid))
    sig_t = np.where(np.arange(grid) / grid < 0.25, 0.4, 0.15)
    I = dWs @ sig_t
    numeric(it, 2, sbar, float(np.std(I)), {'time-average': 0.2125, 'plain-average': 0.275, 'variance': float(v)}, agree=2e-3,
            shown={'0.2385': sbar, '21.25': 100 * (0.4 * 0.25 + 0.15 * 0.75), '27.5': 100 * (0.4 + 0.15) / 2})
    med = 72 * math.exp(0.06 - float(v) / 2)
    lnS = math.log(72) + 0.06 - float(v) / 2 + I
    numeric(it, 3, med, float(np.exp(np.median(lnS))), {'mean': 72 * math.exp(0.06), 'average-vol': 72 * math.exp(0.06 - 0.2125 ** 2 / 2), 'full-variance': 72 * math.exp(0.06 - float(v))},
            agree=0.15, shown={'0.0284375': float(v) / 2, '0.0315625': 0.06 - float(v) / 2, '74.31': med, '21.25': 21.25})
    z = -(0.06 - float(v) / 2) / sbar
    numeric(it, 4, Phi(z), float(np.mean(lnS < math.log(72))),
            {'average-vol': Phi(-(0.06 - 0.2125 ** 2 / 2) / 0.2125), 'no-drag': Phi(-0.06 / sbar), 'upper': 1 - Phi(z)},
            agree=4e-3, shown={'0.0315625': 0.06 - float(v) / 2, '0.1323': -z, '0.4474': Phi(z), '0.2385': sbar, '23.85': 100 * sbar, '21.25': 21.25})

# ===================================================================== level 3
def level3():
    global rng
    L3 = load(3)

    it = L3['p-touch-note']
    r, s = 0.04, 0.25
    a_s = sp.Symbol('a')
    roots = sorted(float(x) for x in sp.solve(sp.Rational(1, 2) * sp.Rational(1, 16) * a_s * (a_s - 1) + sp.Rational(1, 25) * a_s - sp.Rational(1, 25), a_s))
    g = lambda a: 0.5 * s * s * a * (a - 1) + r * a - r
    roots2 = sorted([optimize.brentq(g, 0.5, 2), optimize.brentq(g, -3, 0)])
    p1 = it['parts'][0]['widget']
    ok(sorted(p1['answers']) == sorted(round(x, 2) for x in roots), f'p-touch-note part 1: roots {roots}')
    ok(all(close(x, y, 1e-9) for x, y in zip(roots, roots2)), 'p-touch-note part 1: brentq')
    wr = {x['id']: sorted(float(t) for t in x['value'].split(',')) for x in p1['wrong']}
    ok(wr == {'sign': [1.0, 1.28], 'no-half': sorted([1.0, -r / (s * s)])}, f'p-touch-note part 1: wrongs {wr}')
    check_shown(it, 1, {'0.03125': 0.5 * s * s, '1.28': -roots[0], '0.04': r})
    choice(it, 2, 'negative-power')
    check_shown(it, 2, {'1.28': -roots[0]})
    aa = roots[0]
    V = 1.25 ** aa
    # second route: discounted Q-expectation of the hitting time, from the Laplace transform of a first passage
    nu_q = r - s * s / 2
    dist = math.log(1.25) / s
    lam = (math.sqrt(nu_q ** 2 / s ** 2 + 2 * r) + nu_q / s)
    V2 = math.exp(-lam * dist)
    numeric(it, 3, V, V2, {'sign': 1.25 ** 1.28, 'no-half': 1.25 ** (-r / (s * s)), 'root-one': 1.25}, agree=1e-9,
            shown={'0.7515': V, '1.25': 1.25, '1.28': 1.28, '0.64': r / (s * s)})
    h = 1e-4
    dV = ((100 + h) / 80) ** aa - ((100 - h) / 80) ** aa
    numeric(it, 4, 10000 * aa * V / 100, 10000 * dV / (2 * h), {'sign': -10000 * aa * V / 100, 'no-power': -10000 * V / 100}, agree=1e-4,
            shown={'0.00962': -aa * V / 100, '96.2': -10000 * aa * V / 100, '0.7515': V, '1.28': 1.28})

    it = L3['p-digital-measures']
    S0, mu, r, s, T, K = 40, 0.11, 0.03, 0.32, 0.5, 36
    th = (mu - r) / s
    th2 = float(sp.solve(sp.Eq(sp.Rational(11, 100) - sp.Rational(32, 100) * sp.Symbol('th'), sp.Rational(3, 100)))[0])
    numeric(it, 1, th, th2, {'excess': mu - r, 'sum': (mu + r) / s, 'inverse': s / (mu - r)}, shown={'0.08': mu - r, '0.25': th, '0.32': s})
    zq = (math.log(K / S0) - (r - s * s / 2) * T) / (s * math.sqrt(T))
    zp = (math.log(K / S0) - (mu - s * s / 2) * T) / (s * math.sqrt(T))
    zz = rng.standard_normal(1000000)
    STq = S0 * np.exp((r - s * s / 2) * T + s * math.sqrt(T) * zz)
    numeric(it, 2, Phi(zq), float(np.mean(STq < K)),
            {'real-drift': Phi(zp), 'no-drag': Phi((math.log(K / S0) - r * T) / (s * math.sqrt(T))), 'upper': 1 - Phi(zq)},
            agree=2e-3, shown={'0.0512': s * s / 2, '0.4188': -zq, '0.3377': Phi(zq), '0.0106': -(r - s * s / 2) * T, '0.2263': s * math.sqrt(T), '0.03': r, '0.9': 0.9})
    df = math.exp(-r * T)
    price = df * Phi(zq)
    numeric(it, 3, price, float(df * np.mean(STq < K)), {'undiscounted': 0.3377, 'mu-discount': math.exp(-mu * T) * 0.3377, 'whole-year': math.exp(-r) * 0.3377},
            agree=2e-3, shown={'0.985112': df, '0.3327': price, '0.015': r * T, '0.03': r})
    ok(close(df * 0.3377, it['parts'][2]['widget']['answer'], it['parts'][2]['widget']['tol']['abs']), 'p-digital-measures part 3: rounded route')
    gap = 1e4 * df * (Phi(zq) - Phi(zp))
    STp = S0 * np.exp((mu - s * s / 2) * T + s * math.sqrt(T) * zz)
    gap2 = 1e4 * df * (float(np.mean(STq < K)) - float(np.mean(STp < K)))
    ok(close(zq - th * math.sqrt(T), zp, 1e-12), 'p-digital-measures: Girsanov shift of z')
    numeric(it, 4, gap, gap2,
            {'undiscounted': 1e4 * (Phi(zq) - Phi(zp)), 'theta-t': 1e4 * df * (Phi(zq) - Phi(zq - th * T)), 'mu-discount': 1e4 * (df * Phi(zq) - math.exp(-mu * T) * Phi(zp))},
            agree=15, shown={'0.5956': -zp, '0.275734': Phi(zp), '0.337686': Phi(zq), '0.985112': df, '0.061953': Phi(zq) - Phi(zp),
                             '0.1768': th * math.sqrt(T), '0.04': (mu - r) * T, '0.2757': Phi(zp), '0.4188': -zq, '0.015': r * T, '610': gap})
    ok(close(1e4 * df * (0.3377 - 0.2757), it['parts'][3]['widget']['answer'], it['parts'][3]['widget']['tol']['abs']), 'p-digital-measures part 4: rounded route')

    it = L3['p-one-touch']
    s, T = 0.24, 0.75
    r = s * s / 2
    numeric(it, 1, r, float(Fr(24, 100) ** 2 / 2), {'full-square': s * s, 'half-vol': s / 2}, shown={'0.0288': r, '0.0576': s * s, '0.24': s})
    b = math.log(1.2)
    x = b / (s * math.sqrt(T))
    touch = 2 * (1 - Phi(x))
    # second route: simulate driftless log paths on a fine grid with the Brownian-bridge crossing correction
    nst, npth = 200, 100000
    dt = T / nst
    inc = s * math.sqrt(dt) * rng.standard_normal((npth, nst))
    X = np.cumsum(inc, axis=1)
    Xprev = np.hstack([np.zeros((npth, 1)), X[:, :-1]])
    pcross = np.exp(-2 * np.clip(b - Xprev, 0, None) * np.clip(b - X, 0, None) / (s * s * dt))
    pcross[(X >= b) | (Xprev >= b)] = 1
    touch_mc = float(np.mean(1 - np.prod(1 - pcross, axis=1)))
    numeric(it, 2, touch, touch_mc, {'no-reflection': 1 - Phi(x), 'price-gap': 2 * (1 - Phi(0.2 / (s * math.sqrt(T)))), 'whole-year': 2 * (1 - Phi(b / s))},
            agree=4e-3, shown={'0.1823': b, '0.2078': s * math.sqrt(T), '0.8772': x, '0.3804': touch, '1.2': 1.2, '0.2': 0.2, '0.75': T})
    df = math.exp(-r * T)
    nt = df * (1 - touch)
    numeric(it, 3, nt, df * (1 - touch_mc), {'undiscounted': 1 - 0.3804, 'one-touch': df * 0.3804}, agree=5e-3,
            shown={'0.0216': r * T, '0.978632': df, '0.6196': 1 - 0.3804, '0.6064': nt, '0.0288': r, '0.3804': touch, '0.75': T})
    ok(close(df * (1 - 0.3804), it['parts'][2]['widget']['answer'], it['parts'][2]['widget']['tol']['abs']), 'p-one-touch part 3: rounded route')
    sh = 0.5826 * s * math.sqrt(1 / 252)
    x2 = (b + sh) / (s * math.sqrt(T))
    touch2 = 2 * (1 - Phi(x2))
    nt2 = df * (1 - touch2)
    # second route: daily-monitored simulation of the touch (189 closes in nine months)
    nd = 189
    Xd = np.cumsum(s * math.sqrt(1 / 252) * rng.standard_normal((200000, nd)), axis=1)
    nt2_mc = df * float(np.mean(Xd.max(axis=1) < b))
    numeric(it, 4, nt2, nt2_mc,
            {'shift-in': df * (1 - 2 * (1 - Phi((b - sh) / (s * math.sqrt(T))))), 'continuous': nt, 'one-touch': df * touch2},
            agree=4e-3, shown={'0.008808': sh, '0.0088': sh, '0.9196': x2, '0.3578': touch2, '0.6422': 1 - touch2, '0.6285': nt2,
                               '0.1823': b, '0.1911': b + sh, '0.2078': s * math.sqrt(T), '0.978632': df, '0.5826': 0.5826, '0.24': s, '1.2': 1.2})
    ok(close(0.978632 * 0.6422, it['parts'][3]['widget']['answer'], it['parts'][3]['widget']['tol']['abs']), 'p-one-touch part 4: rounded route')

for _n, _f in ((1, level1), (2, level2), (3, level3)):
    if os.path.exists(os.path.join(COURSE, f'problems-{_n}.json')):
        _f()

print(f'{checks - len(fails)} of {checks} checks passed')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
