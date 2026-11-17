"""Recompute every number in app/content/courses/ito/problems-<n>.json twice (docs/briefs/chained.md check 1).

Levels 1 to 3, one block per set. Method 1 is exact or closed form (fractions, sympy, the formula the lesson
teaches). Method 2 takes another route: the binomial law of the trades, Monte Carlo with a fixed seed, numerical
integration of the normal density, sympy's own differentiation for Itô's lemma, root finding for the touch note,
enumeration of the coarse path, two-dimensional Itô by sympy and a Q simulation for the twin shares, and
simulated Brownian bridges between the closes of the barrier path (re-author and fix pass, session AF).

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

    # p-maker-tally: 625 trades of +-40, win chance 0.507 (review finding 1)
    it = L1['p-maker-tally']
    n, a, p = 625, 40, Fr(507, 1000)
    m_trade = a * p - a * (1 - p)
    e_day = n * m_trade
    ok(m_trade == Fr(14, 25) and e_day == 350, 'p-maker-tally: mean per trade 0.56, day 350')
    k = np.arange(n + 1)
    pmf = stats.binom.pmf(k, n, 0.507)
    e_day_binom = float(np.sum(pmf * (40 * (2 * k - n))))
    numeric(it, 1, float(e_day), e_day_binom,
            {'wins-only': n * a * 0.507, 'half-edge': float(e_day) / 2, 'per-trade-count': n * 0.014}, agree=1e-6,
            shown={'0.56': float(m_trade), '0.014': 0.014, '0.493': 0.493, '49.3': 49.3})
    qv = n * a * a
    paths = rng.choice([-40, 40], size=(200, n), p=[0.493, 0.507])
    qv_sim = float(np.unique((paths ** 2).sum(axis=1))[0])
    ok(len(np.unique((paths ** 2).sum(axis=1))) == 1, 'p-maker-tally: squared sum varies by path')
    var_day = float(n * (a * a - m_trade ** 2))
    ok(var_day == 999804, f'p-maker-tally: day variance {var_day}')
    numeric(it, 2, qv, qv_sim, {'variance': var_day, 'abs-sum': n * a}, shown={'0.56': float(m_trade)})
    sigma = math.sqrt(qv)
    sd5 = sigma * math.sqrt(5)
    sd5_mc = float(np.std(sigma * rng.standard_normal((200000, 5)).sum(axis=1)))
    numeric(it, 3, sd5, sd5_mc, {'sd-times-t': 5 * sigma, 'one-day': sigma}, agree=15)
    mean5 = 5 * float(e_day)
    z = -mean5 / sd5
    numeric(it, 4, Phi(z), nquad_normal_tail(z),
            {'sd-times-t': Phi(-mean5 / (5 * sigma)), 'no-drift': 0.5, 'ends-up': 1 - Phi(z), 'one-day': Phi(-mean5 / sigma)},
            agree=1e-8, shown={'0.7826': -z, '2236.07': sd5, '0.2169': Phi(z)})
    ok(close(Phi(-1750 / 2236.07), it['parts'][3]['widget']['answer'], it['parts'][3]['widget']['tol']['abs']), 'p-maker-tally part 4: rounded route')
    ok(close(float(np.mean(mean5 + sd5 * rng.standard_normal(400000) < 0)), Phi(z), 0.003), 'p-maker-tally part 4: simulation')

    # p-quarter-rally: GBM S0 45, mu 13%, sigma 35%, S_0.25 = 52
    it = L1['p-quarter-rally']
    mu, s, tl, s25 = 0.13, 0.35, 0.75, 52.0
    nu = mu - s * s / 2
    sd_inc = s * math.sqrt(tl)
    w_inc = math.sqrt(tl) * rng.standard_normal(400000)
    numeric(it, 1, sd_inc, float(np.std(s * w_inc)), {'full-year': s, 'variance': s * s * tl, 'past-quarter': s * math.sqrt(0.25)},
            agree=2e-3, shown={'0.3031': sd_inc, '0.75': tl, '0.0919': s * s * tl})
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
    r, s, Bn = 0.04, 0.25, 75.0  # barrier 75 (review finding 10)
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
    ok('75' in it['prose'] and '80' not in json.dumps(it), 'p-touch-note: barrier 75 throughout')
    aa = roots[0]
    xr = 100 / Bn
    V = xr ** aa
    # second route: discounted Q-expectation of the hitting time, from the Laplace transform of a first passage
    nu_q = r - s * s / 2
    dist = math.log(xr) / s
    lam = (math.sqrt(nu_q ** 2 / s ** 2 + 2 * r) + nu_q / s)
    V2 = math.exp(-lam * dist)
    numeric(it, 3, V, V2, {'sign': xr ** 1.28, 'no-half': xr ** (-r / (s * s)), 'root-one': xr}, agree=1e-9,
            shown={'0.6920': V, '1.28': 1.28, '0.64': r / (s * s)})
    h = 1e-4
    dV = ((100 + h) / Bn) ** aa - ((100 - h) / Bn) ** aa
    numeric(it, 4, 10000 * aa * V / 100, 10000 * dV / (2 * h), {'sign': -10000 * aa * V / 100, 'no-power': -10000 * V / 100}, agree=1e-4,
            shown={'0.00886': -aa * V / 100, '88.6': -10000 * aa * V / 100, '0.6920': V, '1.28': 1.28})
    ok(close(-1.28 * 0.6920 * 100, it['parts'][3]['widget']['answer'], it['parts'][3]['widget']['tol']['abs']), 'p-touch-note part 4: rounded route')

    # p-twin-shares (re-authored, replaces p-digital-measures): two shares on one W, a note on S_B/S_A
    it = L3['p-twin-shares']
    A0, B0, muA, sA, sB, r, T = 60, 45, Fr(95, 1000), Fr(18, 100), Fr(30, 100), Fr(5, 100), 2
    xs = sp.Symbol('x')
    hedge = 1000 * sA / sB
    hedge2 = float(sp.solve(sp.Eq(1000 * sp.Rational(18, 100) - xs * sp.Rational(30, 100), 0), xs)[0])
    numeric(it, 1, float(hedge), hedge2, {'inverted': float(1000 * sB / sA), 'equal': 1000.0, 'variance-ratio': float(1000 * (sA / sB) ** 2)},
            shown={'0.18': 0.18, '0.30': 0.30})
    mB = sp.Symbol('m')
    muB = sp.solve(sp.Eq(1000 * sp.Rational(95, 1000) - 600 * mB, sp.Rational(5, 100) * 400), mB)[0]
    theta = (muA - r) / sA
    muB2 = r + theta * sB
    ok(muB == sp.Rational(1, 8) and muB2 == Fr(1, 8) and theta == Fr(1, 4), 'p-twin-shares: mu_B 12.5% by the book and by one price of risk')
    numeric(it, 2, float(muB), float(muB2),
            {'whole-book': float((1000 * muA - r * 1000) / 600), 'no-r': float(1000 * muA / 600), 'same-drift': float(muA)},
            shown={'0.095': 0.095, '0.05': 0.05, '0.125': 0.125, '0.25': 0.25, '0.30': 0.30, '0.18': 0.18})
    ok(it['parts'][1]['widget'].get('unit') == '%', 'p-twin-shares part 2: % unit')
    # Ito on f(x, y) = y / x with dx = muA x dt + sA x dW, dy = muB y dt + sB y dW (one W)
    X, Y, mA_, mB_, sA_, sB_ = sp.symbols('X Y muA muB sA sB', positive=True)
    f = Y / X
    dr = (sp.diff(f, X) * mA_ * X + sp.diff(f, Y) * mB_ * Y + sp.Rational(1, 2) * sp.diff(f, X, 2) * sA_ ** 2 * X ** 2
          + sp.Rational(1, 2) * sp.diff(f, Y, 2) * sB_ ** 2 * Y ** 2 + sp.diff(f, X, Y) * sA_ * sB_ * X * Y) / f
    dr = sp.simplify(dr)
    ok(sp.simplify(dr - (mB_ - mA_ + sA_ ** 2 - sA_ * sB_)) == 0, f'p-twin-shares: Ito drift of the ratio {dr}')
    subs = {mA_: sp.Rational(95, 1000), mB_: sp.Rational(1, 8), sA_: sp.Rational(18, 100), sB_: sp.Rational(3, 10)}
    dP = float(dr.subs(subs))
    logd = float((Fr(1, 8) - sB ** 2 / 2) - (muA - sA ** 2 / 2))
    dP2 = logd + float((sB - sA) ** 2) / 2
    numeric(it, 3, dP, dP2,
            {'no-ito': 0.03, 'no-cross': float(Fr(1, 8) - muA + sA ** 2), 'no-convexity': float(Fr(1, 8) - muA - sA * sB), 'log-drift': logd},
            shown={'0.125': 0.125, '0.045': float(sB ** 2 / 2), '0.095': 0.095, '0.0162': float(sA ** 2 / 2), '0.0012': logd,
                   '0.30': 0.30, '0.18': 0.18, '0.12': 0.12, '0.0084': dP, '0.08': 0.08, '0.0788': float(muA - sA ** 2 / 2),
                   '0.0072': 0.0072, '0.054': 0.054, '0.0324': 0.0324, '0.84': 0.84})
    ok(it['parts'][2]['widget'].get('unit') == '%', 'p-twin-shares part 3: % unit')
    dQ = float(dr.subs({**subs, mA_: sp.Rational(5, 100), mB_: sp.Rational(5, 100)}))
    ok(close(dQ, -0.0216, 1e-15), 'p-twin-shares: Q drift of the ratio -2.16%')
    R0 = B0 / A0
    price = math.exp(-float(r) * T) * 100 * R0 * math.exp(dQ * T)
    # second route: simulate both shares under Q on the same normal draws
    z = rng.standard_normal(2000000)
    SA = A0 * np.exp((0.05 - 0.0162) * T + 0.18 * math.sqrt(T) * z)
    SB = B0 * np.exp((0.05 - 0.045) * T + 0.30 * math.sqrt(T) * z)
    price_mc = math.exp(-0.05 * T) * 100 * float(np.mean(SB / SA))
    numeric(it, 4, price, price_mc,
            {'real-drift': math.exp(-0.1) * 75 * math.exp(dP * T), 'martingale': math.exp(-0.1) * 75, 'undiscounted': 75 * math.exp(dQ * T),
             'log-drift': math.exp(-0.1) * 75 * math.exp(float(sA ** 2 - sB ** 2) / 2 * T)},
            agree=0.03, shown={'0.0324': 0.0324, '0.054': 0.054, '0.0216': -dQ, '0.75': 0.75, '0.0432': -2 * dQ, '0.1': 0.1, '64.99': price,
                               '0.84': 0.84, '2.16': 2.16, '2.88': 2.88, '0.12': 0.12, '0.1432': 0.1 - 2 * dQ})

    # p-bridge-closes (re-authored, replaces p-one-touch): bridge touch chances between daily closes
    it = L3['p-bridge-closes']
    s, r, K, Bb = 0.28, 0.045, 100.0, 112.0
    closes = [105.00, 107.60, 111.20, 110.30, 109.40]
    dt = 1 / 252
    s2 = s * s * dt
    sd = math.sqrt(s2)
    b = math.log(Bb)
    choice(it, 1, 'end-values')
    check_shown(it, 1, {'0.0058': r - s * s / 2, '0.045': r, '0.0392': s * s / 2})
    # the claim: a drift cancels from the bridge. X_t = x + nu t + sd W_t, bridge X_t - (t/D)(X_D - y): nu drops out exactly
    tgrid = np.linspace(0, 1, 501)
    Wg = np.concatenate([[0], np.cumsum(rng.standard_normal(500) * math.sqrt(1 / 500))])
    br = lambda nu: (nu * tgrid + Wg) - tgrid * (nu + Wg[-1])
    ok(float(np.max(np.abs(br(5.0) - br(0.0)))) < 1e-12, 'p-bridge-closes part 1: drift cancels from the bridge')
    ps, ps_pdf = [], []
    for x_, y_ in zip(closes, closes[1:]):
        u, v = b - math.log(x_), b - math.log(y_)
        ps.append(math.exp(-2 * u * v / s2))
        lx, ly = math.log(x_), math.log(y_)
        ps_pdf.append(stats.norm.pdf(2 * b - ly, lx, sd) / stats.norm.pdf(ly, lx, sd))
    u, v = b - math.log(111.2), b - math.log(110.3)
    numeric(it, 2, ps[2], ps_pdf[2],
            {'no-two': math.exp(-u * v / s2), 'whole-year': math.exp(-2 * u * v / (s * s)), 'survival': 1 - round(ps[2], 4)},
            agree=1e-12, shown={'0.007168': u, '0.015295': v, '0.0003111': s2, '0.7048': 2 * u * v / s2, '0.4942': ps[2], '0.01764': sd,
                                '0.0784': s * s, '0.28': s})
    # simulated bridges for the gap, fine grid with per-step exact correction
    def sim_touch(x_, y_, npth=20000, nst=400, seed=0):
        gg = np.random.default_rng(seed)
        lx, ly = math.log(x_), math.log(y_)
        inc = gg.standard_normal((npth, nst)) * sd * math.sqrt(1 / nst)
        Wp = np.hstack([np.zeros((npth, 1)), np.cumsum(inc, axis=1)])
        tt = np.linspace(0, 1, nst + 1)
        path = lx + Wp - tt * (Wp[:, -1:]) + tt * (ly - lx)
        a0, a1 = b - path[:, :-1], b - path[:, 1:]
        pc = np.where((a0 <= 0) | (a1 <= 0), 1.0, np.exp(-2 * np.clip(a0, 0, None) * np.clip(a1, 0, None) / (s2 / nst)))
        return 1 - np.prod(1 - pc, axis=1)
    sims = [sim_touch(x_, y_, seed=40 + i) for i, (x_, y_) in enumerate(zip(closes, closes[1:]))]
    ok(close(float(np.mean(sims[2])), ps[2], 0.01), f'p-bridge-closes part 2: simulated bridges {float(np.mean(sims[2]))}')
    surv = (1 - ps[0]) * (1 - ps[1]) * (1 - round(ps[2], 4)) * (1 - ps[3])
    surv_exact = math.exp(sum(math.log1p(-p_) for p_ in ps))
    surv_mc = float(np.mean(np.prod(1 - np.array(sims), axis=0)))
    ok(close(surv_mc, surv_exact, 0.01), f'p-bridge-closes part 3: simulated survival {surv_mc}')
    numeric(it, 3, surv, surv_exact,
            {'sum-rule': 1 - (ps[0] + ps[1] + 0.4942 + ps[3]), 'one-gap': 1 - 0.4942, 'touch': 1 - surv}, agree=1e-4,
            shown={'0.1577': ps[1], '0.4942': ps[2], '0.0993': ps[3], '0.3837': surv, '0.8423': 1 - ps[1], '0.5058': 1 - ps[2],
                   '0.9007': 1 - ps[3], '0.0645': b - math.log(105), '16.6': 2 * (b - math.log(105)) * (b - math.log(107.6)) / s2})
    ok(close(ps[0], 6e-8, 0.5e-8), f'p-bridge-closes part 3: first gap {ps[0]}')
    df = math.exp(-r * 4 / 252)
    pay = closes[-1] - K
    val = df * pay * 0.3837
    numeric(it, 4, val, df * pay * surv_exact,
            {'plain': round(df * pay, 2), 'knock-in': round(df * pay * (1 - surv_exact), 2), 'one-gap': round(df * pay * (1 - 0.4942), 2),
             'sum-rule': round(df * pay * (1 - (ps[0] + ps[1] + 0.4942 + ps[3])), 2)},
            agree=1e-3, shown={'0.999286': df, '3.60': val, '9.3933': df * pay, '0.3837': surv, '0.6163': 1 - surv, '0.4942': ps[2],
                               '9.40': 9.40})
    ok(close(round(val, 2), df * pay * surv_exact, it['parts'][3]['widget']['tol']['abs']), 'p-bridge-closes part 4: both routes in band')


for _n, _f in ((1, level1), (2, level2), (3, level3)):
    if os.path.exists(os.path.join(COURSE, f'problems-{_n}.json')):
        _f()

print(f'{checks - len(fails)} of {checks} checks passed')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
