"""Recompute every number in app/content/courses/ito/problems-4.json twice (docs/briefs/chained.md check 1).

Level 4 only; levels 1 to 3 are in problems-ito-numbers.py. Method 1 is exact or closed form (fractions, sympy,
the formula the lesson teaches). Method 2 takes another route: sympy's own differentiation for the drift tests,
the discrete gambler's-ruin chain solved as a linear system for the exit chances and times, Monte Carlo of the
two-date product under Q, and root finding for the forward price.

For each numeric part: both methods agree; the key lies within its tol of them; every `wrong` value matches its
named slip, lies outside the key band, does not overlap another slip and is no wider than its value; byKey covers
the wrongs exactly; a non-whole key's question states its form. Every decimal printed in a part's feedback and
explain is either in the item's stem or the part's question, or listed in that part's `shown` check and equal to the
recomputed value at the printed places. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-ito-4-numbers.py
"""
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp
from scipy import optimize

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'ito')
fails, checks = [], 0
FORM = re.compile(r'decimal|places?\b|significant|nearest|percentage|per cent|fraction', re.I)
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
    parse = lambda t: parse_expr(t.replace('^', '**'), local_dict=sym, transformations=tr)
    ok(sp.simplify(parse(w['answer']) - answer) == 0, f'{tag}: answer {w["answer"]}')
    for a in w.get('accept', []):
        ok(sp.simplify(parse(a) - answer) == 0, f'{tag}: accept {a}')
    got = {x['id']: x['tex'] for x in w['wrong']}
    ok(set(got) == set(wrong) == set(p['feedback'].get('byKey', {})), f'{tag}: wrong ids')
    for wid, ex in wrong.items():
        ok(sp.simplify(parse(got[wid]) - ex) == 0, f'{tag}: wrong {wid}')
        ok(sp.simplify(ex - answer) != 0, f'{tag}: wrong {wid} equals key')


def drift(f, t, x, s2):
    """Itô drift of f(t, X_t) for X = sigma W: f_t + sigma^2/2 f_xx, by sympy differentiation."""
    return sp.expand(sp.diff(f, t) + sp.Rational(1, 2) * s2 * sp.diff(f, x, 2))


def ruin_chain(N, k, step_time):
    """Symmetric walk on 0..N from k (method 2 for the exit): P(hit N), E[tau], E[tau; hit N] by linear solves."""
    n = N - 1
    M = np.zeros((n, n))
    for i in range(n):
        M[i, i] = 1
        if i > 0:
            M[i, i - 1] = -0.5
        if i < n - 1:
            M[i, i + 1] = -0.5
    e_top = np.zeros(n)
    e_top[-1] = 0.5
    h = np.linalg.solve(M, e_top)                       # h_i = P(hit N from i + 1)
    T = np.linalg.solve(M, np.full(n, step_time))       # E[tau]
    J = np.linalg.solve(M, step_time * h)               # E[tau 1{hit N}]: each step weighted by h at its start
    return h[k - 1], T[k - 1], J[k - 1]


# ===================================================================== level 4
def level4():
    items = load(4)

    # ---------------------------------------------------------------- p-band-wait (l13, l14)
    # Re-authored in session AF (review-problems-ito-4 finding 1): X = 30 + 2W in pips, exit at 0 or 50.
    it = items['p-band-wait']
    t, x, c = sp.symbols('t x c')
    s2, x0, L = Fr(4), Fr(30), Fr(50)
    # the chain on a 1-pip grid, levels 0..50 from 30, each step lasting 1/sigma^2 = 0.25 min (exact for these moments)
    Pc, Tc, Jc = ruin_chain(int(L), int(x0), 1 / float(s2))
    P = x0 / L
    ok(close(Pc, float(P), 1e-12), 'p-band-wait: P = 3/5 by the chain')
    ok(Fr(3, 5) == P, 'p-band-wait: stated P = 3/5')
    # part 1: E[X^3] = 50^3 P (method 1) and 2500 E[X] = 2500 x0 (method 2)
    EX3 = L ** 3 * P
    numeric(it, 1, float(EX3), float(L ** 2 * x0),
            {'start-cube': float(x0 ** 3), 'swapped': float(L ** 3 * (1 - P)), 'sure-top': float(L ** 3)},
            shown={'0.6': 0.6, '0.4': 0.4})
    ok(EX3 == 75000, 'p-band-wait part 1: 75,000')
    ok(sp.expand(drift(x ** 3, t, x, sp.Integer(4))) == 12 * x, 'p-band-wait part 1: drift of X^3 is 12X')
    # part 2: c from the drift (by hand 3 sigma^2, by sympy solve), then E[tau X] = (E[X^3] - x0^3)/c
    c1 = 3 * s2
    c2 = sp.solve(sp.Poly(drift(x ** 3 - c * t * x, t, x, sp.Integer(4)), x).coeffs()[0], c)[0]
    ok(c1 == 12 and c2 == 12, 'p-band-wait part 2: c = 12')
    EtX = (EX3 - x0 ** 3) / c1
    EtX_c = L * Jc                                       # tau X_tau = 50 tau on the top edge only
    numeric(it, 2, float(EtX), EtX_c,
            {'no-half': float((EX3 - x0 ** 3) / 24), 'sigma-unsquared': float((EX3 - x0 ** 3) / 6),
             'no-start': float(EX3 / 12), 'unit-c': float((EX3 - x0 ** 3) / 3)}, agree=1e-7)
    ok(EtX == 4000, 'p-band-wait part 2: 4,000')
    # part 3: A = E[tau X]/50
    A = EtX / L
    numeric(it, 3, float(A), Jc, {'squared-level': float(EtX / L ** 2), 'no-divide': float(EtX)}, agree=1e-7)
    # part 4: A / P; closed form (L^2 - x0^2)/(3 sigma^2) as method 2
    up = A / P
    ok(up == (L ** 2 - x0 ** 2) / (3 * s2), 'p-band-wait part 4: closed form (50^2 - 30^2)/12')
    numeric(it, 4, float(up), Jc / Pc, {'times-p': float(A * P), 'joint': float(A), 'swapped': float(A / (1 - P))},
            agree=1e-7, shown={'133.33': float(up), '0.6': 0.6, '0.4': 0.4})
    # part 5: E[tau] = x0 (L - x0)/sigma^2 = 150 as stated; floor wait (E[tau] - A)/(1 - P); closed form by reflection
    Et = x0 * (L - x0) / s2
    ok(Et == 150 and close(Tc, 150, 1e-7), 'p-band-wait part 5: stated E[tau] = 150 (formula and chain)')
    ok(drift(x ** 2 - 4 * t, t, x, sp.Integer(4)) == 0, 'p-band-wait part 5: X^2 - 4t driftless')
    down = (Et - A) / (1 - P)
    down2 = (L ** 2 - (L - x0) ** 2) / (3 * s2)
    numeric(it, 5, float(down), float(down2),
            {'wrong-weight': float((Et - up) / (1 - P)), 'no-condition': float(Et - A), 'top-chance': float((Et - A) / P)},
            agree=1e-9, shown={'0.4': 0.4, '133.33': float(up), '0.6': 0.6})
    ok(close((Tc - Jc) / (1 - Pc), float(down), 1e-6), 'p-band-wait part 5: chain agrees')
    ok(up < Et < down, 'p-band-wait: near edge quicker, far edge slower')
    ok(close(80 / 0.6, it['parts'][3]['widget']['answer'], it['parts'][3]['widget']['tol']['abs']),
       'p-band-wait part 4: printed working 80/0.6 in the band')

    # ---------------------------------------------------------------- p-two-date-product (l15, l16)
    it = items['p-two-date-product']
    S0, r, s = 50.0, 0.03, 0.30
    cov = s * s * min(1, 2)
    # method 2: sample covariance of sigma W_1, sigma W_2 from simulated paths
    n = 2_000_000
    Z1, Z2 = rng.standard_normal(n), rng.standard_normal(n)
    W1, W2 = Z1, Z1 + Z2
    cov_mc = float(np.cov(s * W1, s * W2)[0, 1])
    numeric(it, 1, cov, cov_mc, {'later-time': s * s * 2, 'independent': 0, 'unsquared': s}, agree=2e-3,
            shown={'0.09': cov, '0.3': s})
    var = s * s * (1 + 2) + 2 * cov
    var_mc = float(np.var(s * W1 + s * W2))
    numeric(it, 2, var, var_mc, {'no-cov': s * s * 3, 'cov-once': s * s * 3 + cov, 'later-time': s * s * 3 + 2 * 0.18},
            agree=3e-3, shown={'0.09': cov, '0.18': 0.18, '0.45': var, '0.27': s * s * 3})
    ok(close(s * s * 5, var, 1e-12), 'p-two-date-product part 2: 5 sigma^2')
    m = 2 * math.log(S0) + 3 * (r - s * s / 2)
    ok(close(m - 2 * math.log(S0), -0.045, 1e-12), 'p-two-date-product part 3: log mean offset')
    mean = math.exp(m + var / 2) / 100
    S1 = S0 * np.exp((r - s * s / 2) * 1 + s * W1)
    S2 = S0 * np.exp((r - s * s / 2) * 2 + s * W2)
    mean_mc = float(np.mean(S1 * S2)) / 100
    # method 3 (exact, other route): E[S_1^2] e^{r} from the power formula and the independent second year
    mean_split = S0 ** 2 * math.exp((2 * r + s * s) * 1) * math.exp(r * 1) / 100
    ok(close(mean, mean_split, 1e-9), 'p-two-date-product part 3: split at t = 1 agrees')
    numeric(it, 3, mean, mean_mc,
            {'no-half': math.exp(m + var) / 100, 'no-cov': math.exp(m + 0.27 / 2) / 100,
             'r-drift': math.exp(2 * math.log(S0) + 3 * r + var / 2) / 100}, agree=0.1,
            shown={'0.045': 0.045, '0.225': var / 2, '0.18': 0.18, '29.93': mean, '0.09': 0.09, '0.27': 0.27, '0.45': 0.45})
    ok(close(25 * math.exp(0.18), mean, 1e-9), 'p-two-date-product part 3: 25 e^0.18')
    ok(close(mean / (S0 * math.exp(r) * S0 * math.exp(2 * r) / 100), math.exp(0.09), 1e-12), 'p-two-date-product part 3: e^0.09 over forwards')
    price = math.exp(-2 * r) * mean
    price_mc = math.exp(-2 * r) * mean_mc
    naive = math.exp(-2 * r) * S0 * math.exp(r) * S0 * math.exp(2 * r) / 100
    numeric(it, 4, price, price_mc,
            {'forwards': naive, 'one-year': math.exp(-r) * mean, 'undiscounted': mean}, agree=0.1,
            shown={'0.06': 0.06, '0.18': 0.18, '0.12': 0.12, '28.19': price, '0.03': 0.03, '25.76': naive, '2.43': price - naive})
    ok(close(naive, 25 * math.exp(0.03), 1e-9), 'p-two-date-product part 4: naive is 25 e^0.03')

    # ---------------------------------------------------------------- p-dividend-hedge (l16, l17)
    it = items['p-dividend-hedge']
    choice(it, 1, 'with-yield')
    tt, S, T, K = sp.symbols('t S T K', positive=True)
    rr, qq, ss, mu = sp.symbols('r q sigma mu')
    Vf = sp.Function('V')(tt, S)
    Vt, VS, VSS = sp.diff(Vf, tt), sp.diff(Vf, S), sp.diff(Vf, S, 2)
    # part 1: dt coefficient of -dV + V_S dS + q V_S S dt
    coef = -(Vt + mu * S * VS + ss ** 2 * S ** 2 * VSS / 2) + VS * mu * S + qq * S * VS
    ok(sp.simplify(coef - (-Vt - ss ** 2 * S ** 2 * VSS / 2 + qq * S * VS)) == 0, 'p-dividend-hedge part 1: coefficient')
    # part 2: coef = r(-V + S V_S) rearranged; read off the S V_S coefficient
    pde = sp.expand(-(coef - rr * (-Vf + S * VS)))
    bracket = sp.simplify(pde.coeff(VS) / S)
    expression(it, 2, rr - qq, {'plus': rr + qq, 'no-yield': rr, 'sign': qq - rr}, {'r': rr, 'q': qq})
    ok(sp.simplify(bracket - (rr - qq)) == 0, 'p-dividend-hedge part 2: sympy coefficient r - q')
    # part 3
    Sv, r4, q4, tau = 120.0, 0.045, 0.02, 0.75
    Vp = Sv * math.exp(-q4 * tau)
    Vt_pde = r4 * Vp - (r4 - q4) * Sv * math.exp(-q4 * tau)
    Vexpr = S * sp.exp(-qq * (T - tt))
    Vt_direct = float(sp.diff(Vexpr, tt).subs({S: Sv, qq: q4, T: tau, tt: 0}))
    ok(sp.simplify(sp.diff(Vexpr, tt) + (rr - qq) * S * sp.diff(Vexpr, S) + ss ** 2 * S ** 2 * sp.diff(Vexpr, S, 2) / 2 - rr * Vexpr) == 0,
       'p-dividend-hedge part 3: prepaid share solves the dividend equation')
    numeric(it, 3, Vt_pde, Vt_direct,
            {'plus': r4 * Vp - (r4 + q4) * Vp, 'no-yield': r4 * Vp - r4 * Vp, 'no-discount': q4 * Sv}, agree=1e-9,
            shown={'0.015': q4 * tau, '118.2134': Vp, '0.02': q4, '2.3643': Vt_pde})
    # part 4
    Kf = Sv * math.exp((r4 - q4) * tau)
    Kroot = optimize.brentq(lambda k: Vp - k * math.exp(-r4 * tau), 50, 200, xtol=1e-12)
    numeric(it, 4, Kf, Kroot,
            {'prepaid': Vp, 'no-yield': Sv * math.exp(r4 * tau), 'plus': Sv * math.exp((r4 + q4) * tau)}, agree=1e-8,
            shown={'118.2134': Vp, '0.03375': r4 * tau, '0.01875': (r4 - q4) * tau, '122.27': Kf, '0.025': r4 - q4})
    ok(close(118.2134 * math.exp(0.03375), it['parts'][3]['widget']['answer'], it['parts'][3]['widget']['tol']['abs']),
       'p-dividend-hedge part 4: rounded route from 118.2134')


level4()
print(f'{checks - len(fails)} of {checks} checks passed')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
