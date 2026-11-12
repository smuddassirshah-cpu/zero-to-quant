"""Recompute every number in app/content/courses/testing/problems-<n>.json twice (docs/briefs/chained.md check 1).

Levels 1 to 4. Method 1 is exact: sympy, with the likelihood, information or table written out and solved or
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


def stale(items, iid, old_values):
    """Re-authored item: none of the old setting's figures may remain in its text (review-problems-1.6-b finding 9)."""
    text = json.dumps(items[iid], ensure_ascii=False)
    for v in old_values:
        ok(v not in text, f'{iid}: stale value {v} still in the item')


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
    q5 = L4['p-disk-failures']['parts'][4]['question']
    ok('smallest number of gaps' in q5 and 'How many gaps make' not in q5, 'p-disk-failures p5: the question asks for the smallest number of gaps, so exactly one number answers it (review-delta-holes finding 6)')
    ok(min(k for k in range(3, 10000) if sp.Rational(k - 2, k) >= sp.Rational(99, 100)) == n_brute == 200, 'p-disk-failures p5: 200 is the smallest n with (n - 2) / n >= 0.99')

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

L1 = load(1)
if L1 is not None:
    Phi = stats.norm.cdf
    # ---------- p-cereal-boxes: 36 boxes, mean 743.1 g, sigma 18, label 750 ----------
    pick(L1, 'p-cereal-boxes', 1, 'label-lower')
    n, sig, xbar, mu0 = 36, 18, sp.Rational(7431, 10), 750
    se = sp.Integer(sig) / sp.sqrt(n)
    sims = rng.normal(mu0, sig, size=(200000, n)).mean(axis=1)                  # route 2: simulated sd of the mean
    ok(abs(sims.std() - 3) < 0.02, 'p-cereal-boxes: simulated se near 3')
    num(L1, 'p-cereal-boxes', 2, se, math.sqrt(sig ** 2 / n), {'over-n': sp.Rational(sig, n), 'variance': sp.Rational(sig ** 2, n)})
    z = (xbar - mu0) / se
    num(L1, 'p-cereal-boxes', 3, z, stats.norm.ppf(stats.norm(750, sig / math.sqrt(n)).cdf(743.1)),   # route 2: through the mean's own normal law
        {'sign': -z, 'over-sd': (xbar - mu0) / sig, 'carried': (xbar - mu0) / sp.Rational(1, 2)})
    p_rounded = 1 - sp.Rational(9893, 10000)                                     # the part gives Phi(2.3) = 0.9893
    ok(round(Phi(2.3), 4) == 0.9893, 'p-cereal-boxes: Phi(2.3) = 0.9893')
    num(L1, 'p-cereal-boxes', 4, p_rounded, stats.norm.sf(2.3), {'upper-tail': 1 - p_rounded, 'two-sided': 2 * p_rounded},
        agree=5e-5, round_tol=0.00006)
    ok(abs(stats.norm.cdf(-2.3) - 0.0107) < 0.00005 and round(1 / 0.0107) == 93, 'p-cereal-boxes: p = 0.0107, one in 93')
    pick(L1, 'p-cereal-boxes', 5, 'fail')
    ok(0.0107 > 0.01 and 0.0107 < 0.05, 'p-cereal-boxes: between the two levels')
    prints(L1, 'p-cereal-boxes', 4, ['0.0107', '0.9893'])

    # ---------- p-phone-battery: 8 lives, advert 19.5, one-sided t ----------
    xs = [15, 19, 20, 17, 18, 16, 21, 18]
    n = len(xs)
    xbar = sp.Rational(sum(xs), n)
    num(L1, 'p-phone-battery', 1, xbar, np.mean(xs), {'n-minus-one': sp.Rational(sum(xs), n - 1)}, round_tol=0.001)
    ss = sum((sp.Integer(x) - xbar) ** 2 for x in xs)
    ok(ss == 28 and sum(xs) == 144, 'p-phone-battery: total 144 and squares 28')
    s = sp.sqrt(ss / (n - 1))
    xbar_slip = sp.Rational(sum(xs), n - 1)
    num(L1, 'p-phone-battery', 2, s, np.std(xs, ddof=1),
        {'divide-by-n': sp.sqrt(ss / n), 'variance': s ** 2, 'carried': sp.sqrt(sum((x - xbar_slip) ** 2 for x in xs) / (n - 1))},
        round_tol=0.001)
    t = (xbar - sp.Rational(39, 2)) / (s / sp.sqrt(n))
    t_scipy = stats.ttest_1samp(xs, 19.5).statistic
    num(L1, 'p-phone-battery', 3, t, t_scipy,
        {'root-seven': (xbar - sp.Rational(39, 2)) / (s / sp.sqrt(n - 1)), 'over-s': (xbar - sp.Rational(39, 2)) / s, 'sign': -t,
         'carried': (xbar - sp.Rational(39, 2)) / (sp.sqrt(ss / n) / sp.sqrt(n))}, round_tol=0.0006)
    ok(abs(-1.5 / 0.707 - (-2.1213)) < 0.001, 'p-phone-battery p3: a 3-place standard error stays in the band')
    c7, c2, cn = stats.t(7).ppf(0.95), stats.t(7).ppf(0.975), stats.norm.ppf(0.95)
    ok(round(c7, 3) == 1.895 and round(c2, 3) == 2.365 and round(cn, 3) == 1.645, 'p-phone-battery: cut-offs')
    ok(float(t) < -c7 and abs(float(t)) < c2, 'p-phone-battery: one-sided rejects, two-sided would not')
    pick(L1, 'p-phone-battery', 4, 'one-sided-t7')
    se = s / sp.sqrt(n)
    mu_star = xbar + sp.Rational(1895, 1000) * se
    # route 2: bisection for the null value that puts the scipy t statistic at -1.895
    mu_root = optimize.brentq(lambda m: stats.ttest_1samp(xs, m).statistic + 1.895, 18, 25)
    num(L1, 'p-phone-battery', 5, mu_star, mu_root,
        {'normal': xbar + sp.Rational(1645, 1000) * se, 'two-sided': xbar + sp.Rational(2365, 1000) * se,
         'wrong-side': xbar - sp.Rational(1895, 1000) * se, 'sd-not-se': xbar + sp.Rational(1895, 1000) * s}, round_tol=0.005)
    ok(round(18 + 1.895 * 0.7071, 2) == 19.34 and abs(19.5 - 19.34 - 0.16) < 1e-9, 'p-phone-battery p5: printed 0.7071 gives 19.34; 0.16 inside')

    # ---------- p-wine-taster: 12 trials, guessing p = 1/2 ----------
    seqs = list(itertools.product([0, 1], repeat=12))                            # route 2: enumerate all 4096
    def tail(k):
        return sp.Rational(sum(math.comb(12, j) for j in range(k, 13)), 4096)
    def enum_tail(k):
        return sum(1 for q in seqs if sum(q) >= k) / len(seqs)
    num(L1, 'p-wine-taster', 1, tail(11), enum_tail(11), {'eleven-only': sp.Rational(12, 4096), 'twelve-only': sp.Rational(1, 4096)},
        round_tol=0.00005)
    num(L1, 'p-wine-taster', 2, tail(10), stats.binom(12, 0.5).sf(9), {'exactly-ten': sp.Rational(66, 4096), 'carried': sp.Rational(78, 4096)},
        round_tol=0.00005)
    ok(math.comb(12, 10) == 66 and math.comb(12, 9) == 220 and tail(10) == sp.Rational(79, 4096), 'p-wine-taster: binomial counts')
    num(L1, 'p-wine-taster', 3, tail(9), enum_tail(9), {'exactly-nine': sp.Rational(220, 4096), 'carried': sp.Rational(66 + 220, 4096)},
        round_tol=0.00005)
    ok(abs(0.0193 + 0.0537 - 0.0730) < 1e-9, 'p-wine-taster p3: the rounded sum is 0.0730')
    k_star = min(k for k in range(13) if tail(k) <= sp.Rational(1, 20))
    k_star2 = int(stats.binom(12, 0.5).isf(0.05)) + 1                             # smallest k with P(W >= k) <= 0.05
    num(L1, 'p-wine-taster', 4, k_star, k_star2, {'nine': k_star - 1, 'eleven': min(k for k in range(13) if tail(k) <= sp.Rational(1, 100))})

    # ---------- p-pizza-delivery: 16 deliveries, mean 33.5, sigma 8 then s = 9.6 ----------
    n, xbar, mu0 = 16, sp.Rational(67, 2), 30
    z = (xbar - mu0) / (sp.Integer(8) / sp.sqrt(n))
    num(L1, 'p-pizza-delivery', 1, z, (33.5 - 30) / (8 / math.sqrt(16)),
        {'over-sd': (xbar - mu0) / 8, 'over-n': (xbar - mu0) / sp.Rational(8, 16), 'no-null': xbar / 2}, round_tol=0.005)
    ok(round(Phi(1.75), 4) == 0.9599, 'p-pizza-delivery: Phi(1.75) = 0.9599')
    p_r = 1 - sp.Rational(9599, 10000)
    num(L1, 'p-pizza-delivery', 2, p_r, stats.norm.sf(1.75), {'two-sided': 2 * p_r, 'lower-tail': 1 - p_r}, agree=5e-5, round_tol=0.00006)
    t = z * sp.Rational(8, 1) / sp.Rational(96, 10)
    num(L1, 'p-pizza-delivery', 3, t, 3.5 / (9.6 / 4), {'flipped': z * sp.Rational(96, 80), 'over-s': (xbar - mu0) / sp.Rational(96, 10)})
    c15 = stats.t(15).ppf(0.95)
    ok(round(c15, 3) == 1.753 and float(t) < c15 and float(z) > 1.645, 'p-pizza-delivery: z rejects, t does not')
    pick(L1, 'p-pizza-delivery', 4, 't-fails')
    # fix pass (review-problems-1.6-b findings 5 and 7): the doubled tail from the calculator's Phi sits in the slip band; normality is stated
    two_s = next(x for x in L1['p-pizza-delivery']['parts'][1]['widget']['wrong'] if x['id'] == 'two-sided')
    ok(abs(round(2 * stats.norm.sf(1.75), 4) - two_s['value']) <= two_s['tol']['abs'] and abs(2 * stats.norm.sf(1.75) - 0.0801) < 0.0001 and two_s['tol']['abs'] < (0.0802 - 0.0401) / 2,
       'p-pizza-delivery p2: two-sided 0.0801 (calculator) and 0.0802 (table) both land on the slip, clear of the key 0.0401')
    ok('independent draws from a normal distribution' in L1['p-pizza-delivery']['prose'], 'p-pizza-delivery: normality stated')
    ok(all(L1['p-phone-battery']['parts'][k - 1]['widget'].get('unit') == 'h' for k in (1, 2, 5)), 'p-phone-battery: unit h on parts 1, 2 and 5')
    ok(all(w in L1['p-wine-taster']['parts'][3]['question'] for w in ('0.0193', '0.0730')), 'p-wine-taster p4: restates 0.0193 and 0.0730')
    ok(sp.Rational(78, 4096) == sp.Rational(39, 2048) and round(78 / 4096, 3) == 0.019 and round(79 / 4096, 4) == 0.0193 and 79 == 66 + 13,
       'p-wine-taster p2: 78/4096 is 0.019 to 3 places and 66 + 12; 79/4096 is 0.0193')
    ok('79}{4096} \\approx 0.0193' in L1['p-wine-taster']['parts'][1]['feedback']['byKey']['carried'], 'p-wine-taster p2: carried line prints 79/4096')

L2 = load(2)
if L2 is not None:
    Phi = stats.norm.cdf
    # ---------- p-fertiliser-trials: sd 1.2, 36 plots, effect 0.45, cut-off 1.645 ----------
    m = sp.Rational(45, 100) / (sp.Rational(12, 10) / 6)
    sims = rng.normal(0.45, 1.2, size=(100000, 36)).mean(axis=1) / 0.2       # route 2: simulated z under H1
    ok(abs(sims.mean() - 2.25) < 0.01 and abs(sims.std() - 1) < 0.01, 'p-fertiliser-trials: simulated centre 2.25, sd 1')
    num(L2, 'p-fertiliser-trials', 1, m, sims.mean(), {'over-sd': sp.Rational(45, 100) / sp.Rational(12, 10), 'over-n': sp.Rational(45, 100) / (sp.Rational(12, 10) / 36)},
        agree=0.01)
    ok(round(Phi(0.605), 4) == 0.7274 and abs(2.25 - 1.645 - 0.605) < 1e-12, 'p-fertiliser-trials: Phi(0.605) = 0.7274')
    pw = sp.Rational(7274, 10000)
    num(L2, 'p-fertiliser-trials', 2, pw, (sims > 1.645).mean(), {'beta': 1 - pw, 'alpha': sp.Rational(5, 100), 'centre-only': sp.Rational(9878, 10000)}, agree=0.005, round_tol=0.00006)
    either = 1 - (1 - pw) ** 2
    sims2 = rng.normal(0.45, 1.2, size=(100000, 36)).mean(axis=1) / 0.2       # a second, independent trial
    num(L2, 'p-fertiliser-trials', 3, either, 1 - stats.norm.cdf(1.645 - 2.25) ** 2, {'both': pw ** 2, 'added': 2 * pw, 'carried': 1 - pw ** 2},
        agree=5e-5, round_tol=0.00006)
    ok(abs(((sims > 1.645) | (sims2 > 1.645)).mean() - float(either)) < 0.005, 'p-fertiliser-trials: simulated either rule')
    c72 = 2.25 * math.sqrt(2) - 1.645
    ok(abs(c72 - 1.537) < 0.0005 and round(Phi(1.537), 4) == 0.9379, 'p-fertiliser-trials: 72-plot centre and Phi(1.537)')
    pw72 = sp.Rational(9379, 10000)
    num(L2, 'p-fertiliser-trials', 4, pw72, stats.norm.sf(1.645, loc=0.45 / (1.2 / math.sqrt(72))), {'beta': 1 - pw72, 'unchanged': pw, 'centre-only': sp.Rational(9993, 10000)},
        agree=5e-5, round_tol=0.00006)
    ok(round(1 - 0.95 ** 2, 4) == 0.0975 and pw72 > either, 'p-fertiliser-trials: either-rule alpha 0.0975, one trial wins on power')
    pick(L2, 'p-fertiliser-trials', 5, 'one-big')
    # fix pass (finding 2): a second Phi value is given, so the learner must pick the one past the cut-off
    ok(round(Phi(2.25), 4) == 0.9878 and round(Phi(3.182), 4) == 0.9993 and abs(2.25 * math.sqrt(2) - 3.182) < 0.0005, 'p-fertiliser-trials: Phi(2.25) = 0.9878, Phi(3.182) = 0.9993')
    for k_, cv in ((2, 0.9878), (4, 0.9993)):
        wc = next(x for x in L2['p-fertiliser-trials']['parts'][k_ - 1]['widget']['wrong'] if x['id'] == 'centre-only')
        ok(wc['value'] == cv and wc['tol']['abs'] == 5e-05 and 'centre-only' in L2['p-fertiliser-trials']['parts'][k_ - 1]['feedback']['byKey'], f'p-fertiliser-trials p{k_}: centre-only slip {cv}')
    ok('\\Phi(2.25) = 0.9878' in L2['p-fertiliser-trials']['parts'][1]['question'] and '\\Phi(3.182) = 0.9993' in L2['p-fertiliser-trials']['parts'][3]['question'], 'p-fertiliser-trials: the questions give both Phi values')
    prints(L2, 'p-fertiliser-trials', 3, ['0.0743', '0.9257'])

    # ---------- p-tyre-brands: Welch, 50 v 40 cars ----------
    va, vb = sp.Rational(81, 100) / 50, sp.Rational(36, 100) / 40
    se = sp.sqrt(va + vb)
    # route 2: scipy's Welch test from the summary statistics gives the same t, so se = gap / t
    wt = stats.ttest_ind_from_stats(3.2, 0.9, 50, 2.8, 0.6, 40, equal_var=False).statistic
    num(L2, 'p-tyre-brands', 1, se, 0.4 / wt,
        {'sum-se': sp.sqrt(sp.Rational(81, 100) / 50) + sp.sqrt(sp.Rational(36, 100) / 40), 'variance': va + vb,
         'same-n': sp.sqrt(sp.Rational(117, 100) / 50)}, round_tol=0.0001)
    t = sp.Rational(4, 10) / se
    num(L2, 'p-tyre-brands', 2, t, wt, {'carried': sp.Rational(4, 10) / sp.Rational(2221, 10000), 'over-variance': sp.Rational(4, 10) / (va + vb)})
    ok(abs(0.4 / 0.1587 - 2.5198) < 0.001, 'p-tyre-brands p2: printed 0.1587 stays in the band')
    ok(round(Phi(2.52), 4) == 0.9941, 'p-tyre-brands: Phi(2.52)')
    p2 = 2 * (1 - sp.Rational(9941, 10000))
    num(L2, 'p-tyre-brands', 3, p2, 2 * stats.norm.sf(float(t)), {'one-sided': p2 / 2, 'inside': 1 - p2}, agree=0.0001, round_tol=0.0001)
    pick(L2, 'p-tyre-brands', 4, 'right')

    # ---------- p-running-shoes: nine paired differences ----------
    d = [-7, -3, -9, -1, -4, -5, 1, -3, -5]
    n = len(d)
    db = sp.Rational(sum(d), n)
    num(L2, 'p-running-shoes', 1, db, np.mean(d), {'n-minus-one': sp.Rational(sum(d), n - 1), 'sign': -db})
    ss = sum((x - db) ** 2 for x in d)
    ok(ss == 72 and [x - db for x in d] == [-3, 1, -5, 3, 0, -1, 5, 1, -1], 'p-running-shoes: deviations and 72')
    sd = sp.sqrt(ss / (n - 1))
    db_slip = sp.Rational(sum(d), n - 1)
    num(L2, 'p-running-shoes', 2, sd, np.std(d, ddof=1),
        {'divide-by-n': sp.sqrt(ss / n), 'variance': sd ** 2, 'carried': sp.sqrt(sum((x - db_slip) ** 2 for x in d) / (n - 1))}, round_tol=0.001)
    t = db / (sd / sp.sqrt(n))
    old = np.array([1200, 1260, 1185, 1320, 1230, 1275, 1210, 1290, 1245])      # any old times: the paired t uses only the gaps
    num(L2, 'p-running-shoes', 3, t, stats.ttest_rel(old + np.array(d), old).statistic,
        {'over-sd': db / sd, 'root-eight': db / (sd / sp.sqrt(n - 1)), 'carried': db / (sp.sqrt(ss / n) / 3), 'sign': -t}, round_tol=0.001)
    c8 = stats.t(8).ppf(0.95)
    ok(round(c8, 3) == 1.860 and float(t) < -c8, 'p-running-shoes: t8 cut-off 1.860, reject')
    pick(L2, 'p-running-shoes', 4, 'paired')
    n_need = sp.ceiling(sp.Rational(618, 100) * (sd / sp.Rational(3, 2)) ** 2)
    # route 2: the smallest n with power at least 0.8 by the normal power formula, searched
    n_brute = next(k for k in range(2, 500) if Phi(1.5 * math.sqrt(k) / 3 - 1.645) >= 0.8)
    num(L2, 'p-running-shoes', 5, n_need, n_brute,
        {'not-rounded': sp.Rational(618, 100) * 4, 'rounded-down': n_need - 1, 'no-square': sp.ceiling(sp.Rational(618, 100) * 2),
         'carried': sp.ceiling(sp.Rational(618, 100) * 8 / sp.Rational(9, 4))}, round_tol=0.05)
    ok(abs(6.18 * 8 / 2.25 - 21.97) < 0.01 and Phi(1.5 * math.sqrt(24) / 3 - 1.645) < 0.8, 'p-running-shoes p5: carried 21.97; 24 runners fall short')

    # ---------- p-blood-screen: healthy N(50, 10), disease N(72, 10), cut-off 68, prevalence 2% ----------
    ok(round(Phi(1.8), 4) == 0.9641 and round(Phi(0.4), 4) == 0.6554, 'p-blood-screen: Phi values')
    a_ = 1 - sp.Rational(9641, 10000)
    num(L2, 'p-blood-screen', 1, a_, stats.norm(50, 10).sf(68), {'lower': 1 - a_, 'two-tail': 2 * a_, 'disease-curve': sp.Rational(6554, 10000)},
        agree=5e-5, round_tol=0.00006)
    b_ = 1 - sp.Rational(6554, 10000)
    num(L2, 'p-blood-screen', 2, b_, stats.norm(72, 10).cdf(68), {'power': 1 - b_, 'healthy-curve': 1 - a_}, agree=5e-5, round_tol=0.00006)
    flags = 9800 * a_ + 200 * (1 - b_)
    pop = np.r_[rng.normal(50, 10, 980000), rng.normal(72, 10, 20000)]            # route 2: a simulated million patients
    num(L2, 'p-blood-screen', 3, flags, (pop > 68).sum() / 100,
        {'true-only': 200 * (1 - b_), 'false-only': 9800 * a_, 'beta-not-power': 9800 * a_ + 200 * b_}, agree=1.5, round_tol=0.5)
    ok(round(float(flags)) == 483 and round(9800 * stats.norm(50, 10).sf(68) + 200 * stats.norm(72, 10).sf(68)) == 483, 'p-blood-screen: 483 from rounded and unrounded rates')
    share = 200 * (1 - b_) / flags
    sick = np.r_[np.zeros(980000, bool), np.ones(20000, bool)]
    num(L2, 'p-blood-screen', 4, share, sick[pop > 68].mean(),
        {'flipped': 1 - share, 'power': 1 - b_, 'carried': 200 * b_ / (9800 * a_ + 200 * b_)}, agree=0.01, round_tol=0.005)
    ok(abs(131.1 / 483 - 0.27) < 0.005 and round(float(9800 * a_), 1) == 351.8 and round(float(200 * (1 - b_)), 1) == 131.1, 'p-blood-screen: printed 351.8, 131.1, 0.27')
    pick(L2, 'p-blood-screen', 5, 'right')
    # fix pass (finding 5): the doubled tail from a calculator's Phi (0.0719) and from the table (0.0718) both land on the slip
    tw = next(x for x in L2['p-blood-screen']['parts'][0]['widget']['wrong'] if x['id'] == 'two-tail')
    ok(abs(2 * stats.norm.sf(1.8) - 0.0719) < 0.00005 and all(abs(v - tw['value']) <= tw['tol']['abs'] for v in (0.0718, 0.0719)) and abs(tw['value'] - 0.0359) > tw['tol']['abs'] + 5e-05,
       'p-blood-screen p1: two-tail 0.0718 and 0.0719 land on the slip, clear of 0.0359')
    # fix pass (findings 4, 7): shoes slip bands, hypothesis, and the t-test sample size behind the part 5 explanation
    sh_parts = L2['p-running-shoes']['parts']
    for k_, wid, v in ((2, 'divide-by-n', 2.83), (2, 'carried', 3.05), (3, 'over-sd', -1.33), (3, 'root-eight', -3.77), (3, 'carried', -4.24)):
        wx = next(x for x in sh_parts[k_ - 1]['widget']['wrong'] if x['id'] == wid)
        ok(wx['tol']['abs'] == 0.005 and abs(v - wx['value']) <= wx['tol']['abs'], f'p-running-shoes p{k_}: {wid} band 0.005 takes the 2-place slip {v}')
    ok('independent draws from a normal distribution' in L2['p-running-shoes']['prose'], 'p-running-shoes: normality of the differences stated')
    def t_power(nn):
        return stats.nct.sf(stats.t(nn - 1).ppf(0.95), nn - 1, 1.5 * math.sqrt(nn) / 3)
    n_t = next(nn for nn in range(3, 200) if t_power(nn) >= 0.8)
    ok(abs(t_power(25) - 0.783) < 0.002 and n_t == 27 and Phi(1.5 * math.sqrt(25) / 3 - 1.645) >= 0.8, 'p-running-shoes p5: paired t needs 27 runners (power 0.783 at 25); the normal formula gives 25')

def bh_count(pv, q):
    """Benjamini-Hochberg by the rule: the largest rank k with p_(k) <= kq/N."""
    s = sorted(pv)
    N = len(s)
    return max([k for k in range(1, N + 1) if s[k - 1] <= sp.Rational(k, 1) * q / N] or [0])


L3 = load(3)
if L3 is not None:
    from statsmodels.stats.multitest import multipletests
    Phi = stats.norm.cdf
    # ---------- p-gene-screen (re-authored, review-problems-1.6-b finding 9): 60 genes, Bonferroni and BH at 10% ----------
    q = sp.Rational(1, 10)
    bonf = q / 60
    small = [sp.Rational(x) for x in ('0.0004', '0.0021', '0.0038', '0.0071', '0.0079', '0.0125', '0.0190', '0.034')]
    rest = [sp.Rational(11, 100) + sp.Rational(i, 1000) for i in range(52)]        # stand-ins for the other 52, all above 0.1
    pv = small + rest
    fl = [float(x) for x in pv]
    ok(len(pv) == 60 and all(x > sp.Rational(1, 10) for x in rest), 'p-gene-screen: 60 p-values, the other 52 above 0.1')
    bar_root = optimize.brentq(lambda p: min(1.0, p * 60) - 0.10, 1e-6, 0.1)       # route 2: where the Bonferroni-adjusted p reaches 0.10
    num(L3, 'p-gene-screen', 1, bonf, bar_root, {'unadjusted': q, 'times-m': q * 60, 'five-percent': sp.Rational(5, 100) / 60}, round_tol=1e-6)
    ok(round(float(bonf), 6) == 0.001667 and abs(0.10 / 60 * 60 - 0.10) < 1e-12, 'p-gene-screen p1: 0.001667 to 6 places; the 60 bars add to 0.10')
    nb = sum(1 for x in pv if x <= bonf)
    num(L3, 'p-gene-screen', 2, nb, multipletests(fl, 0.10, 'bonferroni')[0].sum(), {'unadjusted': sum(1 for x in pv if x < q), 'bh': bh_count(pv, q)})
    first_fail = next(k for k in range(1, 61) if sorted(pv)[k - 1] > k * q / 60) - 1
    num(L3, 'p-gene-screen', 3, bh_count(pv, q), multipletests(fl, 0.10, 'fdr_bh')[0].sum(),
        {'first-fail': first_fail, 'bonferroni': nb, 'unadjusted': sum(1 for x in pv if x < q)})
    ok(first_fail == 3 and sp.Rational('0.0071') > 4 * bonf and sp.Rational('0.0079') <= 5 * bonf and 8 * bonf > sp.Rational('0.0133')
       and sp.Rational('0.0125') > 6 * bonf and sp.Rational('0.0190') > 7 * bonf and sp.Rational('0.034') > 8 * bonf,
       'p-gene-screen p3: ranks 1 to 3 pass, 4 fails, 5 passes, 6 to 8 fail')
    ok([round(float(k * bonf), 5) for k in (4, 5, 8)] == [0.00667, 0.00833, 0.01333], 'p-gene-screen p3: printed bars 0.00667, 0.00833, 0.01333')
    # part 4: the smallest q at which rank 5 stays in, algebra and then bisection on the BH rule itself
    q5 = sp.Rational('0.0079') * 60 / 5
    lo, hi = 0.0, 0.2
    for _ in range(60):
        mid = (lo + hi) / 2
        if multipletests(fl, mid, 'fdr_bh')[0].sum() >= 5:
            hi = mid
        else:
            lo = mid
    q4 = sp.Rational('0.0071') * 60 / 4
    num(L3, 'p-gene-screen', 4, q5, hi, {'no-divide': sp.Rational('0.0079') * 60, 'first-fail': q4, 'bar': 5 * q / 60}, agree=1e-6, round_tol=0.0006)
    ok(q5 == sp.Rational(948, 10000) and q4 == sp.Rational(1065, 10000), 'p-gene-screen p4: 0.0948 for rank 5, 0.1065 for rank 4')
    ok(multipletests(fl, 0.0949, 'fdr_bh')[0].sum() == 5 and multipletests(fl, 0.0947, 'fdr_bh')[0].sum() == 3,
       'p-gene-screen p4: at q = 0.0949 BH rejects 5, at 0.0947 only 3 (rank 5 is the step)')
    ok(multipletests(fl, 0.15, 'fdr_bh')[0].sum() == 6 and bh_count(pv, sp.Rational(15, 100)) == 6, 'p-gene-screen p5: at q = 0.15 BH rejects 6, so the list changes')
    pick(L3, 'p-gene-screen', 5, 'right')
    stale(L3, 'p-gene-screen', ['0.8715', '0.1285', '0.00125', '0.0488', '0.9512', '40 genes', '0.0011', '0.0052', '0.0060', '0.0081', '0.031', '0.05}{40'])

    # ---------- p-fund-managers: 8 managers, H has SR 0.9 over 9 years, BH at q = 0.10 ----------
    tH = sp.Rational(9, 10) * sp.sqrt(9)
    num(L3, 'p-fund-managers', 1, tH, 0.9 / (1 / math.sqrt(9)), {'over-root': sp.Rational(9, 10) / 3, 'times-t': sp.Rational(81, 10)})
    ok(round(Phi(2.7), 4) == 0.9965, 'p-fund-managers: Phi(2.7)')
    pH = 1 - sp.Rational(9965, 10000)
    num(L3, 'p-fund-managers', 2, pH, stats.norm.sf(2.7), {'two-sided': 2 * pH, 'lower': 1 - pH}, agree=5e-5, round_tol=0.00006)
    others = [sp.Rational(x) for x in ('0.0006', '0.014', '0.052', '0.058', '0.09', '0.31', '0.62')]
    q = sp.Rational(1, 10)
    allp = others + [pH]
    ff = next(k for k in range(1, 9) if sorted(allp)[k - 1] > k * q / 8) - 1
    num(L3, 'p-fund-managers', 3, bh_count(allp, q), multipletests([float(x) for x in allp], 0.10, 'fdr_bh')[0].sum(),
        {'first-fail': ff, 'bonferroni': sum(1 for x in allp if x <= q / 8), 'unadjusted': sum(1 for x in allp if x <= q)})
    ok(bh_count(others + [1 - pH], q) == 2 and bh_count(others + [2 * pH], q) == 5, 'p-fund-managers p3: a lower-tail p gives 2; a doubled p still 5')
    ok(1000 * 0.0035 < 4, 'p-fund-managers p2: fewer than 4 in 1,000')
    tws = next(x for x in L3['p-fund-managers']['parts'][1]['widget']['wrong'] if x['id'] == 'two-sided')
    ok(abs(2 * stats.norm.sf(2.7) - 0.0069) < 0.00005 and all(abs(v - tws['value']) <= tws['tol']['abs'] for v in (0.0069, 0.007)) and abs(tws['value'] - 0.0035) > tws['tol']['abs'] + 5e-05,
       'p-fund-managers p2: two-sided 0.0069 (calculator) and 0.007 (table) land on the slip, clear of 0.0035')
    ok('0.0035 from part 2' in L3['p-fund-managers']['parts'][2]['question'], 'p-fund-managers p3: restates the p-value 0.0035')

    # ---------- p-checkout-designs (re-authored, finding 9): 18 pages, five per cent, GBP 4,000 a launch ----------
    pg = sp.Rational(5, 100)
    sims18 = rng.random((400000, 18)) < 0.05                                       # route 2: simulated null months
    num(L3, 'p-checkout-designs', 1, 18 * pg, sims18.sum(axis=1).mean(), {'one-sided': 18 * pg / 2, 'all-pages': 18, 'complement': 18 * (1 - pg)},
        agree=0.01, round_tol=0.05)
    num(L3, 'p-checkout-designs', 2, 18 * pg * 4000, stats.binom(18, 0.05).mean() * 4000, {'all-pages': 18 * 4000, 'one-launch': 4000, 'thousands': 18 * pg * 4},
        round_tol=0.5)
    bar18 = pg / 18
    bar_root18 = optimize.brentq(lambda p: min(1.0, p * 18) - 0.05, 1e-6, 0.05)
    num(L3, 'p-checkout-designs', 3, bar18, bar_root18, {'unadjusted': pg, 'times-n': 18 * pg, 'sidak': 1 - (1 - pg) ** sp.Rational(1, 18)}, round_tol=1e-6)
    ok(round(float(bar18), 6) == 0.002778 and round(float(1 - (1 - pg) ** sp.Rational(1, 18)), 6) == 0.002846, 'p-checkout-designs p3: Bonferroni 0.002778, Sidak 0.002846')
    ch = 1 - (1 - sp.Rational(2778, 1000000)) ** 18                                # the rounded bar the part names
    ch_exact = 1 - (1 - bar18) ** 18
    fam18 = rng.random((1000000, 18)).min(axis=1)
    num(L3, 'p-checkout-designs', 4, ch_exact, (fam18 <= float(bar18)).mean(), {'bound': pg, 'no-complement': (1 - bar18) ** 18, 'carried': 1 - (1 - pg) ** 18},
        agree=0.001, round_tol=0.00006)
    ok(round(float(ch), 4) == round(float(ch_exact), 4) == 0.0488 and round(float((1 - bar18) ** 18), 4) == 0.9512 and round(float(1 - 0.95 ** 18), 4) == 0.6028,
       'p-checkout-designs p4: 0.0488, 0.9512 and 0.6028 from the rounded and the exact bar')
    waste = 18 * bar18 * 4000
    ok(waste == 200 and abs(18 * 0.002778 * 4000 - 200) < 0.1 and 18 * pg * 4000 == 3600, 'p-checkout-designs p5: expected waste 3600 falls to 200')
    pick(L3, 'p-checkout-designs', 5, 'power')
    stale(L3, 'p-checkout-designs', ['25 ', '0.004', '0.002050', '0.00205', '0.9047', '0.0953', '0.533', '0.97', '0.996', '0.03', 'holdout'])
    prints(L3, 'p-checkout-designs', 4, ['0.9512', '0.0488'])
    prints(L3, 'p-checkout-designs', 5, ['0.6028', '3,600', '200'])

    # ---------- p-biomarker-field (re-authored, finding 9): choose a bar for 380 nulls and 20 real biomarkers ----------
    tab = {2.5: (0.0124, 0.90), 2.8: (0.0051, 0.84), 3.1: (0.0019, 0.75), 3.5: (0.00047, 0.61)}
    m_real = 2.5 + stats.norm.ppf(0.9)                                             # a real centre that passes |z| > 2.5 with chance 0.9
    for c_, (pn, pr) in tab.items():
        null_tail = 2 * stats.norm.sf(c_)
        real_pow = stats.norm.sf(c_ - m_real) + stats.norm.cdf(-c_ - m_real)
        ok(abs(null_tail - pn) <= 0.5 * 10 ** (-5 if pn < 0.001 else -4) + 1e-12, f'p-biomarker-field: null tail at {c_} is {pn}')
        ok(abs(real_pow - pr) <= 0.005 + 1e-9, f'p-biomarker-field: a real centre of {m_real:.3f} passes {c_} with chance {pr}')
    num(L3, 'p-biomarker-field', 1, sp.Rational(1, 380), 1 / (400 - 20), {'over-400': sp.Rational(1, 400), 'times': 380, 'five-percent': sp.Rational(5, 100) / 380},
        round_tol=1e-6)
    ok(round(1 / 380, 6) == 0.002632, 'p-biomarker-field p1: 0.002632')
    lowest = min(c_ for c_, (pn, pr) in tab.items() if pn <= 1 / 380)
    ok(lowest == 3.1 and 380 * 0.0124 == 4.712 and round(380 * 0.0051, 3) == 1.938 and 380 * 0.0019 < 1 and 380 * 0.00047 < 1,
       'p-biomarker-field p2: 3.1 is the lowest bar with null tail at most 1/380; 4.712 and 1.938 false finds at 2.5 and 2.8')
    pick(L3, 'p-biomarker-field', 2, 'c31')
    real3 = rng.binomial(20, 0.75, size=200000)
    num(L3, 'p-biomarker-field', 3, 20 * sp.Rational(75, 100), real3.mean(), {'old-bar': 20 * sp.Rational(90, 100), 'all-real': 20, 'next-bar': 20 * sp.Rational(61, 100)},
        agree=0.02, round_tol=0.5)
    f31 = 380 * sp.Rational(19, 10000)
    sh = f31 / (f31 + 15)
    nul_s = rng.binomial(380, 0.0019, size=400000).mean()
    num(L3, 'p-biomarker-field', 4, sh, nul_s / (nul_s + real3.mean()), {'true-share': 1 - sh, 'over-400': f31 / 400, 'no-power': f31 / (f31 + 20)},
        agree=0.002, round_tol=0.0006)
    ok(f31 == sp.Rational(722, 1000) and round(float(sh), 4) == 0.0459 and round(1 / float(sh)) == 22, 'p-biomarker-field p4: 0.722 false finds, share 0.0459, about 1 in 22')
    any_false = 1 - (1 - 0.0019) ** 380
    ok(round(any_false, 2) == 0.51 and any_false > 0.5, 'p-biomarker-field p5: the chance of at least one false find is about 0.51, more than a half')
    pick(L3, 'p-biomarker-field', 5, 'share')
    stale(L3, 'p-biomarker-field', ['17.29', '0.0455', '0.0027', '1.026', '0.490', '0.079', '0.64', '300', '|z| > 2$', '18.2', '35.29'])
    prints(L3, 'p-biomarker-field', 5, ['0.51'])
    ok(all('independent' in L3[i]['prose'] for i in ('p-gene-screen', 'p-checkout-designs', 'p-biomarker-field')), 'problems-3: the three re-authored items state independence (the 0.51 and 0.9512 figures need it)')
    ok(any(it['difficulty'] == 5 for it in L3.values()) and all(3 <= it['difficulty'] <= 5 for it in L3.values()), 'problems-3: difficulties 3 to 5, one 5')
    parts3 = [p for it in L3.values() for p in it['parts']]
    ok(3 * sum(p['widget']['kind'] == 'numeric' for p in parts3) >= 2 * len(parts3), 'problems-3: at least two thirds of the parts are typed')

present = [n for n in (1, 2, 3, 4) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
