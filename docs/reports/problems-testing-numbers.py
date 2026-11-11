"""Recompute every number in app/content/courses/testing/problems-<n>.json twice (docs/briefs/chained.md check 1).

Level 4 only so far. Method 1 is exact: sympy, with the likelihood, information or table written out and solved or
summed symbolically. Method 2 takes another route: a score root found numerically, information as the variance of
the score by summing over the Poisson or exponential law, a Monte Carlo estimate (seeded) where a mean or variance is
claimed, a brute search over n for a sample size. For each numeric part the script checks: the two methods agree;
the JSON key is within its tol of them; every `wrong` value matches its named slip, lies outside the key's band and
does not overlap another wrong; the figures that feedback and explain print agree with the key. Choice parts check
the keyed option and the numbers the options and lines state. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-testing-numbers.py
"""
import itertools
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy import integrate, optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'testing')
fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'testing', f'problems-{n}: header')
    return {it['id']: it for it in d['items']}


def num(items, iid, k, exact, alt, slips, round_tol=0.0006, agree=1e-6):
    """Part k of item iid: two methods, the key in its band, each named slip."""
    w = items[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(math.isclose(e, a, rel_tol=agree, abs_tol=agree), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, round_tol), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
        ok(wt <= abs(x['value']) / 2 + 1e-12, f'{tag}: wrong {wid} band wider than half its value')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')
    fb = items[iid]['parts'][k - 1]['feedback']
    ok(set(fb.get('byKey', {})) == set(wrongs), f'{tag}: byKey keys {sorted(fb.get("byKey", {}))} vs wrongs')


def pick(items, iid, k, correct_id):
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')
    fb = items[iid]['parts'][k - 1]['feedback']
    ok(set(fb.get('byKey', {})) == {o['id'] for o in w['options'] if not o.get('correct')}, f'{iid} p{k}: byKey keys')


def prints(items, iid, k, figures):
    """Each figure must appear in the part's feedback.correct or explain text, as printed."""
    part = items[iid]['parts'][k - 1]
    text = part['feedback']['correct'] + ' ' + part.get('explain', {}).get('text', '')
    for f in figures:
        ok(f in text, f'{iid} p{k}: text does not print {f}')


rng = np.random.default_rng(20261111)
L4 = load(4)
if L4 is not None:
    # ---------- p-disk-failures: 40 exponential gaps totalling 100 days ----------
    n, T = 40, sp.Integer(100)
    lam = sp.symbols('lam', positive=True)
    loglik = n * sp.log(lam) - lam * T
    lam_mom = sp.solve(sp.Eq(1 / lam, T / n), lam)[0]                     # moments: 1/lam = mean gap
    lam_mle = optimize.brentq(lambda l: n / l - float(T), 0.01, 10)        # score root, numerically
    num(L4, 'p-disk-failures', 1, lam_mom, lam_mle, {'mean-gap': T / n, 'over-total': 1 / T})
    one_gap = -sp.diff(sp.log(lam) - lam * sp.Symbol('x'), lam, 2)          # 1/lam^2, free of x
    info = n * one_gap.subs(lam, lam_mom)
    # variance of one gap's score 1/lam - X by integration against the exponential density at lam = 0.4
    l_ = 0.4
    var_score = integrate.quad(lambda x: (1 / l_ - x) ** 2 * l_ * math.exp(-l_ * x), 0, np.inf)[0]
    num(L4, 'p-disk-failures', 2, info, n * var_score,
        {'one-gap': one_gap.subs(lam, lam_mom), 'no-square': n / lam_mom, 'carried': n / sp.Rational(5, 2) ** 2})
    se = 1 / sp.sqrt(info)
    num(L4, 'p-disk-failures', 3, se, lam_mom / sp.sqrt(n),
        {'variance': 1 / info, 'root-of-info': sp.sqrt(info), 'carried': 1 / sp.sqrt(n / sp.Rational(5, 2) ** 2)})
    crb = 1 / info
    num(L4, 'p-disk-failures', 4, crb, lam_mom ** 2 / n,
        {'standard-error': se, 'one-gap': 1 / one_gap.subs(lam, lam_mom), 'information': info})
    var_unb = lam_mom ** 2 / (n - 2)
    # Monte Carlo of (n - 1)/sum x at lam = 0.4: its variance should sit near lam^2/(n - 2)
    sims = (n - 1) / rng.exponential(1 / 0.4, size=(200000, n)).sum(axis=1)
    ok(abs(sims.mean() - 0.4) < 0.002 and abs(sims.var() / float(var_unb) - 1) < 0.02, 'p-disk-failures: simulation of the unbiased estimator')
    # part 5 (turned round, review-holes-1.6-2.1 finding 9): the smallest n with efficiency (n - 2)/n >= 0.99
    nn = sp.Symbol('nn', positive=True)
    n_alg = sp.solve(sp.Eq((nn - 2) / nn, sp.Rational(99, 100)), nn)[0]                       # route 1: algebra, 2 / 0.01
    n_brute = next(k for k in range(3, 10000) if (lam_mom ** 2 / k) / (lam_mom ** 2 / (k - 2)) >= sp.Rational(99, 100))   # route 2: search on the ratio
    num(L4, 'p-disk-failures', 5, n_alg, n_brute, {'numerator': n_alg - 2, 'efficiency-now': crb / var_unb}, round_tol=0.0006)
    sims200 = 199 / rng.exponential(1 / 0.4, size=(40000, 200)).sum(axis=1)
    ok(abs(0.4 ** 2 / 200 / sims200.var() - 0.99) < 0.02, 'p-disk-failures p5: simulated efficiency at n = 200 is near 0.99')
    ok(sp.Rational(198, 200) == sp.Rational(99, 100) and sp.Rational(38, 40) == sp.Rational(19, 20) and (n_brute - 1 - 2) / (n_brute - 1) < 0.99, 'p-disk-failures p5: 198/200 = 0.99, 38/40 = 0.95, and 199 gaps fall short')
    prints(L4, 'p-disk-failures', 5, ['n \\ge 200', 'n = 200', '0.95'])

    # ---------- p-website-signups: 12 Poisson hours totalling 54 ----------
    pick(L4, 'p-website-signups', 1, 'total')
    n, T = 12, 54
    x = sp.symbols('x0:12', nonnegative=True, integer=True)
    joint = sp.exp(-n * lam) * lam ** sum(x) / sp.prod([sp.factorial(xi) for xi in x])
    g = sp.exp(-n * lam) * lam ** sum(x)
    ok(sp.simplify(joint / g).has(lam) is False, 'p-website-signups: factorisation leaves no lam in h')
    # E[X1 | T] by the conditional law Binomial(T, 1/n), and by simulation
    rb_exact = sp.Rational(T, n)
    rb_binom = stats.binom(T, 1 / n).mean()
    num(L4, 'p-website-signups', 2, rb_exact, rb_binom, {'total': T, 'n-minus-one': sp.Rational(T, n - 1)})
    lam_v = sp.Rational(9, 2)
    var_rb = n * lam_v / n ** 2
    counts = rng.poisson(4.5, size=(400000, n))
    ok(abs(counts.mean(axis=1).var() - float(var_rb)) < 0.004, 'p-website-signups: simulated variance of T/12')
    num(L4, 'p-website-signups', 3, var_rb, stats.poisson(4.5 * n).var() / n ** 2,
        {'one-hour': lam_v, 'n-squared': lam_v / n ** 2, 'sd': sp.sqrt(var_rb)})
    crb = 1 / (n * (1 / lam_v))
    ok(crb == var_rb, 'p-website-signups: the bound equals the variance of T/12')
    num(L4, 'p-website-signups', 4, crb / lam_v, 1 / n, {'inverted': lam_v / crb, 'improved': crb / var_rb},
        round_tol=0.00005)
    need = sp.ceiling(lam_v / sp.Rational(3, 10) ** 2)
    brute = next(m for m in range(1, 1000) if math.sqrt(4.5 / m) <= 0.3 + 1e-12)
    num(L4, 'p-website-signups', 5, need, brute,
        {'no-square': lam_v / sp.Rational(3, 10), 'root-only': sp.sqrt(lam_v) / sp.Rational(3, 10),
         'carried': sp.ceiling(var_rb / sp.Rational(3, 10) ** 2)}, round_tol=0.01)

    # ---------- p-bakery-loaves: 2 x 3 table ----------
    O = sp.Matrix([[50, 40, 30], [20, 40, 20]])
    R = [sum(O.row(i)) for i in range(2)]
    C = [sum(O.col(j)) for j in range(3)]
    N = sum(R)
    E = sp.Matrix(2, 3, lambda i, j: sp.Rational(R[i] * C[j], N))
    on = np.array(O.tolist(), float)
    chi = stats.chi2_contingency(on, correction=False)
    num(L4, 'p-bakery-loaves', 1, E[1, 0], chi[3][1, 0],
        {'averaged': sp.Rational(R[1] + C[0], 2), 'weekday-cell': E[0, 0], 'chance': sp.Rational(R[1] * C[0], N ** 2)},
        round_tol=0.005)
    X2 = sum((O[i, j] - E[i, j]) ** 2 / E[i, j] for i in range(2) for j in range(3))
    ok(X2 == sp.Rational(50, 7), 'p-bakery-loaves: X2 is 50/7')
    num(L4, 'p-bakery-loaves', 2, X2, chi[0],
        {'no-divide': sum((O[i, j] - E[i, j]) ** 2 for i in range(2) for j in range(3)),
         'over-observed': sum((O[i, j] - E[i, j]) ** 2 / O[i, j] for i in range(2) for j in range(3)),
         'weekdays-only': sum((O[0, j] - E[0, j]) ** 2 / E[0, j] for j in range(3))})
    df = (2 - 1) * (3 - 1)
    num(L4, 'p-bakery-loaves', 3, df, chi[2], {'cells-minus-one': 6 - 1, 'margins': (2 - 1) + (3 - 1)})
    p_x2 = sp.exp(-sp.Rational(7143, 1000) / 2)            # the part says to use X^2 = 7.143
    num(L4, 'p-bakery-loaves', 4, p_x2, stats.chi2(2).sf(7.143),
        {'no-half': sp.exp(-sp.Rational(7143, 1000)), 'lower-tail': 1 - p_x2,
         'carried': sp.exp(-sp.Rational(2857, 1000) / 2)}, round_tol=0.00006)
    ok(abs(float(sp.exp(-X2 / 2)) - 0.0281) < 0.00005, 'p-bakery-loaves: unrounded X2 gives the same 4-place p')
    G = 2 * sum(O[i, j] * sp.log(O[i, j] / E[i, j]) for i in range(2) for j in range(3))
    G_scipy = stats.chi2_contingency(on, correction=False, lambda_='log-likelihood')[0]
    ok(math.isclose(float(G), G_scipy, rel_tol=1e-9) and round(float(G), 3) == 7.242, f'p-bakery-loaves: G {float(G)}')
    cut2 = stats.chi2(2).ppf(0.95)
    ok(round(cut2, 3) == 5.991 and float(G) > cut2 and float(X2) > cut2, 'p-bakery-loaves: both past the 5% cut-off')
    ok(round(stats.chi2(5).ppf(0.95), 2) == 11.07, 'p-bakery-loaves: chi2_5 cut-off 11.07')
    ok(5 - 3 == df, 'p-bakery-loaves: Wilks count 5 free shares minus 3')
    pick(L4, 'p-bakery-loaves', 5, 'both-reject')
    prints(L4, 'p-bakery-loaves', 2, ['7.143', '1.524', '1.333', '2.286'])
    ok(sp.Rational(40, 80) == sp.Rational(1, 2) and sp.Rational(40, 120) == sp.Rational(1, 3), 'p-bakery-loaves: brown shares')

    # ---------- p-night-admissions: 10 Poisson nights totalling 38, null 3 ----------
    n, S, l0 = 10, 38, 3
    ll = S * sp.log(lam) - n * lam
    lhat = sp.solve(sp.diff(ll, lam), lam)[0]
    lhat_num = optimize.minimize_scalar(lambda l: -(S * math.log(l) - n * l), bounds=(0.1, 20), method='bounded').x
    num(L4, 'p-night-admissions', 1, lhat, lhat_num, {'total': S, 'excess': lhat - l0}, agree=1e-5)
    stat = 2 * (ll.subs(lam, lhat) - ll.subs(lam, l0))
    # route 2: the summed Poisson log-pmfs, factorials and all, for a sample with this total
    xs = [4] * 8 + [3] * 2
    ok(sum(xs) == S, 'p-night-admissions: stand-in sample totals 38')
    stat2 = 2 * (stats.poisson(3.8).logpmf(xs).sum() - stats.poisson(3).logpmf(xs).sum())
    num(L4, 'p-night-admissions', 2, stat, stat2,
        {'not-doubled': stat / 2, 'no-mean-term': 2 * S * sp.log(lhat / l0),
         'no-n': 2 * (S * sp.log(lhat / l0) - (lhat - l0))})
    info = n / lhat
    var_score = sum(stats.poisson(3.8).pmf(k) * (k / 3.8 - 1) ** 2 for k in range(0, 80))   # Var(S) one night
    se = 1 / sp.sqrt(info)
    num(L4, 'p-night-admissions', 3, se, 1 / math.sqrt(n * var_score),
        {'variance': 1 / info, 'information-flipped': 1 / sp.sqrt(n * lhat), 'null-value': sp.sqrt(sp.Rational(l0, n))})
    se_r = sp.Rational(6164, 10000)                                    # the part says to use 0.6164
    z = (lhat - l0) / se_r
    num(L4, 'p-night-admissions', 4, z, (3.8 - 3) / math.sqrt(0.38), {'squared': z ** 2, 'null-se': (lhat - l0) / sp.sqrt(sp.Rational(3, 10)),
                                                                       'carried': (lhat - l0) / sp.Rational(38, 100)},
        agree=2e-4, round_tol=0.0006)
    cut1 = stats.chi2(1).ppf(0.95)
    ok(round(cut1, 3) == 3.841, 'p-night-admissions: chi2_1 cut-off')
    per = sp.Rational(1966, 10000)                                     # 1.966 over 10 nights
    need = sp.ceiling(sp.Rational(3841, 1000) / per)
    brute = next(m for m in range(1, 500) if float(stat) / n * m > 3.841)   # unrounded statistic per night
    num(L4, 'p-night-admissions', 5, need, brute,
        {'rounded-down': need - 1, 'wald': sp.ceiling(sp.Rational(3841, 1000) / (z ** 2 / n)),
         'carried': sp.ceiling(sp.Rational(3841, 1000) / (per / 2))})
    ok(abs(19 * 0.1966 - 3.735) < 0.0005, 'p-night-admissions: 19 nights give 3.735')
    prints(L4, 'p-night-admissions', 2, ['8.9828', '1.966'])
    ok(abs(S * math.log(3.8 / 3) - 8.9828) < 0.00005, 'p-night-admissions: 38 ln(3.8/3)')

present = [n for n in (1, 2, 3, 4) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
