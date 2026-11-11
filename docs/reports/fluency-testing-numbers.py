"""Recompute the Fluency sets of testing from the drawn variables alone (docs/briefs/fluency.md check 1).

Run: <scratchpad>/venv/bin/python docs/reports/fluency-testing-numbers.py [--n 200]
Each statistic is (estimate - null) / standard error, with the standard error from sympy's sqrt of n (the tuple root
is asserted equal). The Sharpe family rebuilds a mean and sd with that Sharpe ratio (mean = SR, sd = 1) and forms
t = mean / (sd / sqrt(T)) from them. Checks are in fluency_check.py beside this script.
"""
import os
import sys

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fluency_check import Checker  # noqa: E402


def z_zero(V):
    xb, sig, n = V['xh'] / 100, V['sig'], V['n']
    rt = sp.sqrt(n)
    assert rt == V['rt']
    key = (xb - 0) / (sig / rt)
    return key, {'divided-by-sigma': xb / sig, 'divided-by-n': xb / (sig / n)}


def z_nonzero(V):
    m0, sig, n = V['m0'], V['sig'], V['n']
    xb = m0 + V['dh'] / 10
    rt = sp.sqrt(n)
    assert rt == V['rt']
    key = (xb - m0) / (sig / rt)
    return key, {'centred-on-zero': xb / (sig / rt), 'divided-by-sigma': (xb - m0) / sig}


def t_stat(V):
    n, xb, s = V['n'], V['xh'] / 10, V['sh'] / 10
    key = xb / (s / sp.sqrt(n))
    return key, {'no-root-n': xb / s, 'root-of-df': xb / (s / sp.sqrt(n - 1))}


def sharpe(V):
    sr, T = V['sr'], V['y']
    assert V['lo'] <= T <= V['hi']
    mean, sd = sr, sp.Integer(1)
    key = mean / (sd / sp.sqrt(T))
    return key, {'times-t': sr * T, 'over-root': sr / sp.sqrt(T)}


# ---- Level 4 (lessons l13, l15, l17, l18). Each key is rebuilt from the vars by a route of its own:
# moment equations solved by sympy, information as minus the expected second derivative of a sympy log-density,
# likelihoods as products of densities, and Pearson's statistic summed cell by cell from expected counts.
p_, lam_, sig_, x_, a_, l_ = sp.symbols('p lam sig x a l', positive=True)


def mom_exponential(V):
    gaps = [V['g%d' % i] for i in range(1, 6)]
    xbar = sum(gaps) / sp.Integer(5)
    key = sp.solve(sp.Eq(1 / l_, xbar), l_)[0]
    return key, {'gave-mean': xbar, 'total': 1 / sum(gaps)}


def gamma_moments(V):
    sol = sp.solve([sp.Eq(a_ / l_, V['m']), sp.Eq(a_ / l_ ** 2, V['v'])], [a_, l_], dict=True)[0]
    return sol[a_], sol[l_]


def mom_gamma_shape(V):
    a, lam = gamma_moments(V)
    return a, {'gave-rate': lam, 'inverted': 1 / a}


def mom_gamma_rate(V):
    a, lam = gamma_moments(V)
    return lam, {'inverted': 1 / lam, 'gave-shape': a}


def mom_uniform(V):
    xs = [V['x1'], V['x1'] + V['g2'], V['x1'] + V['g2'] + V['g3'], V['x1'] + V['g2'] + V['g3'] + V['g4']]
    th = sp.symbols('th', positive=True)
    xbar = sum(xs) / sp.Integer(4)
    key = sp.solve(sp.Eq(sp.integrate(x_ / th, (x_, 0, th)), xbar), th)[0]
    return key, {'gave-mean': xbar, 'largest': max(xs)}


def info(logf, par, dist):
    """Fisher information as -E[d2 logf / d par2], the expectation over the named distribution's x values."""
    d2 = sp.diff(logf, par, 2)
    return sp.simplify(-dist(d2))


def bern_info(V):
    p, n = V['p'], V['n']
    logf = x_ * sp.log(p_) + (1 - x_) * sp.log(1 - p_)
    one = info(logf, p_, lambda e: e.subs(x_, 1) * p_ + e.subs(x_, 0) * (1 - p_)).subs(p_, p)
    return n * one, {'one-trade': one, 'variance': n * p * (1 - p)}


def pois_se(V):
    lam, n = V['lam'], V['n']
    logf = x_ * sp.log(lam_) - lam_
    one = info(logf, lam_, lambda e: e.subs(x_, lam_)).subs(lam_, lam)   # E[X] = lam, and d2 is linear in x
    se = 1 / sp.sqrt(n * one)
    return se, {'no-root': se ** 2, 'information-flipped': 1 / sp.sqrt(n * lam)}


def exp_se(V):
    lam, n = V['lam'], V['n']
    logf = sp.log(lam_) - lam_ * x_
    one = info(logf, lam_, lambda e: e.subs(x_, 1 / lam_)).subs(lam_, lam)
    se = 1 / sp.sqrt(n * one)
    return se, {'no-root': se ** 2, 'information-flipped': 1 / sp.sqrt(n * lam ** 2)}


def vol_se(V):
    s, n = V['sig'], V['n']
    logf = -sp.log(sig_) - x_ ** 2 / (2 * sig_ ** 2)
    one = info(logf, sig_, lambda e: e.subs(x_ ** 2, sig_ ** 2)).subs(sig_, s)   # E[X^2] = sigma^2
    se = 1 / sp.sqrt(n * one)
    # SE of sigma^2 by the chain rule: I(sigma^2) = I(sigma) / (2 sigma)^2
    se_var = 1 / sp.sqrt(n * one / (2 * s) ** 2)
    return se, {'no-two': s / sp.sqrt(n), 'variance-se': se_var, 'percent-sign': se / 100}   # a typed % is read as a hundredth


def binom_lr(V):
    n, k, p1 = V['n'], V['k'], V['p1']
    L = lambda p: sp.binomial(n, k) * p ** k * (1 - p) ** (n - k)
    key = L(p1) / L(sp.Rational(1, 2))
    return key, {'inverted': 1 / key, 'wins-only': (p1 / sp.Rational(1, 2)) ** k}


def two_ll(V):
    l0 = -V['l0h'] / sp.Integer(10)
    l1 = l0 + V['g'] / sp.Integer(10)
    return 2 * (l1 - l0), {'not-doubled': l1 - l0, 'sign': 2 * (l0 - l1)}


def wilks_df(V):
    p, r = V['p'], V['r']
    free_full, free_null = p, p - r
    w = {'all-parameters': p}
    if free_null != free_full - free_null:
        w['free-under-null'] = free_null
    return free_full - free_null, w


def pois_lrt(V):
    n, lam0, dv = V['n'], V['lam0'], V['dv']
    s = n * lam0 + dv
    lhat = sp.Rational(s, n)
    ll = lambda lam: s * sp.log(lam) - n * lam          # Poisson log-likelihood, constants dropped
    key = 2 * (ll(lhat) - ll(lam0))
    return key, {'not-doubled': key / 2, 'no-mean-term': 2 * s * sp.log(lhat / lam0), 'score-form': (s - n * lam0) ** 2 / sp.Integer(n * lam0)}


def expected_cell(V):
    tot, rt, ct = V['tot'], V['rt'], V['ct']
    key = tot * (sp.Rational(rt, tot) * sp.Rational(ct, tot))
    return key, {'averaged': sp.Rational(rt + ct, 2), 'no-divide': rt * ct}


def gof(V):
    e = V['ee']
    d = [V['d1'], V['d2'], V['d3']]
    d.append(-sum(d))
    obs = [e + di for di in d]
    exp_ = [sp.Rational(sum(obs), 4)] * 4
    key = sum((o - ex) ** 2 / ex for o, ex in zip(obs, exp_))
    return key, {'no-divide': sum((o - ex) ** 2 for o, ex in zip(obs, exp_)),
                 'over-observed': sum((o - ex) ** 2 / o for o, ex in zip(obs, exp_))}


def two_by_two(V):
    t = [[V['a'], V['b']], [V['c'], V['d']]]
    N = sum(map(sum, t))
    R = [sum(r) for r in t]
    C = [t[0][j] + t[1][j] for j in range(2)]
    E = [[sp.Rational(R[i] * C[j], N) for j in range(2)] for i in range(2)]
    terms = [(t[i][j] - E[i][j]) ** 2 / E[i][j] for i in range(2) for j in range(2)]
    obs = sum((t[i][j] - E[i][j]) ** 2 / t[i][j] for i in range(2) for j in range(2))                # divided by the observed counts
    g = 2 * sum(t[i][j] * sp.log(t[i][j] / E[i][j]) for i in range(2) for j in range(2))                # the likelihood-ratio G
    return sum(terms), {'one-cell': terms[0], 'no-divide': sum((t[i][j] - E[i][j]) ** 2 for i in range(2) for j in range(2)),
                        'over-observed': obs, 'likelihood-ratio': g}


def indep_df(V):
    r, c = V['r'], V['c']
    key = (r * c - 1) - ((r - 1) + (c - 1))     # cells minus 1, minus the estimated margins
    w = {'cells-minus-one': r * c - 1}
    if key != r + c - 2:
        w['margins'] = r + c - 2
    return key, w


ck = Checker('testing')
ck.add('fluency-l13-matching-moments', 'exponential-rate', mom_exponential)
ck.add('fluency-l13-matching-moments', 'gamma-shape', mom_gamma_shape)
ck.add('fluency-l13-matching-moments', 'gamma-rate', mom_gamma_rate)
ck.add('fluency-l13-matching-moments', 'uniform-moment', mom_uniform)
ck.add('fluency-l15-sharpness-of-the-peak', 'bernoulli-information', bern_info)
ck.add('fluency-l15-sharpness-of-the-peak', 'poisson-se', pois_se)
ck.add('fluency-l15-sharpness-of-the-peak', 'exponential-se', exp_se)
ck.add('fluency-l15-sharpness-of-the-peak', 'volatility-se', vol_se)
ck.add('fluency-l17-ratio-of-likelihoods', 'binomial-ratio', binom_lr)
ck.add('fluency-l17-ratio-of-likelihoods', 'two-log-likelihoods', two_ll)
ck.add('fluency-l17-ratio-of-likelihoods', 'wilks-df', wilks_df)
ck.add('fluency-l17-ratio-of-likelihoods', 'poisson-ratio-test', pois_lrt)
ck.add('fluency-l18-counts-against-expectations', 'expected-cell', expected_cell)
ck.add('fluency-l18-counts-against-expectations', 'goodness-of-fit', gof)
ck.add('fluency-l18-counts-against-expectations', 'two-by-two', two_by_two)
ck.add('fluency-l18-counts-against-expectations', 'independence-df', indep_df)
ck.add('fluency-l2-measuring-surprise', 'z-null-zero', z_zero)
ck.add('fluency-l2-measuring-surprise', 'z-null-nonzero', z_nonzero)
ck.add('fluency-l4-t-test', 't-statistic', t_stat)
ck.add('fluency-l4-t-test', 'sharpe-t', sharpe)

# ---- review-holes-1.6-2.1 fixes: the bands take what a rounded working prints (findings 16, 17), the % entry (18), the df prompt (21)
import math  # noqa: E402


def extra():
    bad = []
    n_ = 0
    for it in ck.sample('fluency-l18-counts-against-expectations', 'two-by-two'):
        V = {k: float(it['vars'][k]) for k in 'abcd'}
        t = [[V['a'], V['b']], [V['c'], V['d']]]
        N = sum(map(sum, t))
        R = [sum(r) for r in t]
        C = [t[0][0] + t[1][0], t[0][1] + t[1][1]]
        tol = it['tol']['abs']
        for places in (2, 3):         # the prompt says to keep at least 2 places in each expected count, then the four terms summed
            E = [[round(R[i] * C[j] / N, places) for j in range(2)] for i in range(2)]
            x2 = sum((t[i][j] - E[i][j]) ** 2 / E[i][j] for i in range(2) for j in range(2))
            n_ += 1
            if abs(x2 - it['answer']) > tol:
                bad.append(('two-by-two', it['seed'], places, x2, it['answer']))
        gap = round(abs(t[0][0] * t[1][1] - t[0][1] * t[1][0]) / N, 3)   # the solution's printed gap, with expected counts to 2 places
        x2p = gap ** 2 * sum(1 / round(R[i] * C[j] / N, 2) for i in range(2) for j in range(2))
        n_ += 2
        if abs(x2p - it['answer']) > tol:
            bad.append(('two-by-two printed', it['seed'], x2p, it['answer']))
        if tol != 0.05 or any(abs(w['value'] - it['answer']) <= 2 * tol for w in it['wrong']):
            bad.append(('two-by-two band', it['seed']))
    for it in ck.sample('fluency-l17-ratio-of-likelihoods', 'poisson-ratio-test'):
        V = {k: float(it['vars'][k]) for k in ('n', 'lam0', 'dv')}
        s_, n, l0 = V['n'] * V['lam0'] + V['dv'], V['n'], V['lam0']
        tol = it['tol']['abs']
        for places in (4, 5):         # the prompt says to keep the ratio as a fraction and at least 4 places in a logarithm
            lg = round(math.log(s_ / (n * l0)), places)
            x2 = 2 * (s_ * lg - V['dv'])
            n_ += 1
            if abs(x2 - it['answer']) > tol:
                bad.append(('poisson-ratio log', it['seed'], places, x2, it['answer']))
        n_ += 1
        if tol != 0.05 or any(abs(w['value'] - it['answer']) <= 2 * tol for w in it['wrong']):
            bad.append(('poisson-ratio band', it['seed']))
    for it in ck.sample('fluency-l15-sharpness-of-the-peak', 'volatility-se'):
        w = [x for x in it['wrong'] if x['id'] == 'percent-sign']
        n_ += 1
        if len(w) != 1 or abs(w[0]['value'] - it['answer'] / 100) > 1e-12 or any(abs(x['value'] - w[0]['value']) <= 1e-4 for x in it['wrong'] if x is not w[0]) or abs(w[0]['value'] - it['answer']) <= 1e-4:
            bad.append(('volatility-se percent-sign', it['seed']))
    for it in ck.sample('fluency-l17-ratio-of-likelihoods', 'wilks-df'):
        p, r = int(it['vars']['p']), int(it['vars']['r'])
        n_ += 1
        if f"leaves {p - r} free" not in it['prompt'] or 'stay free' in it['prompt'] or it['answer'] != r:   # review-delta-holes finding 10: no 'Under the null hypothesis 1 of them stay free'
            bad.append(('wilks-df prompt', it['seed'], it['prompt']))
    # ---- review-delta-holes findings 2 and 3: 200 draws each. The right working is accepted in every draw; every wrong method
    # (its own formula, written here from the definition, not read from the family's lets) is refused in every draw. The engine's
    # grader accepts a typed value v when |v - answer| <= tol, so "refused" means that distance exceeds the band.
    for it in ck.sample('fluency-l18-counts-against-expectations', 'two-by-two'):
        V = {k: float(it['vars'][k]) for k in 'abcd'}
        O = [V['a'], V['b'], V['c'], V['d']]
        N = sum(O)
        r1, r2, c1, c2 = O[0] + O[1], O[2] + O[3], O[0] + O[2], O[1] + O[3]
        Ex = [r1 * c1 / N, r1 * c2 / N, r2 * c1 / N, r2 * c2 / N]
        x2 = sum((o - e) ** 2 / e for o, e in zip(O, Ex))
        tol = it['tol']['abs']
        right = [x2, sum((o - round(e, 2)) ** 2 / round(e, 2) for o, e in zip(O, Ex)),
                 sum((o - round(e, 3)) ** 2 / round(e, 3) for o, e in zip(O, Ex))]
        wrongs = {'over-observed': sum((o - e) ** 2 / o for o, e in zip(O, Ex)),
                  'likelihood-ratio': 2 * sum(o * math.log(o / e) for o, e in zip(O, Ex)),
                  'no-divide': sum((o - e) ** 2 for o, e in zip(O, Ex)),
                  'one-cell': (O[0] - Ex[0]) ** 2 / Ex[0]}
        n_ += len(right) + len(wrongs)
        for v in right:
            if abs(v - it['answer']) > tol:
                bad.append(('two-by-two right working refused', it['seed'], v, it['answer']))
        for k, v in wrongs.items():
            if abs(v - it['answer']) <= tol:
                bad.append(('two-by-two wrong method accepted', it['seed'], k, v, it['answer']))
        n_ += 1
        if abs(x2 - wrongs['over-observed']) <= 0.11 or abs(x2 - wrongs['likelihood-ratio']) <= 0.11 or abs(wrongs['likelihood-ratio'] - wrongs['over-observed']) <= 0.11:
            bad.append(('two-by-two where clause: a slip is within 0.11 of the key', it['seed']))
    for it in ck.sample('fluency-l17-ratio-of-likelihoods', 'poisson-ratio-test'):
        n, l0, dv = float(it['vars']['n']), float(it['vars']['lam0']), float(it['vars']['dv'])
        s_ = n * l0 + dv
        tol = it['tol']['abs']
        lr = 2 * (s_ * math.log(s_ / (n * l0)) - dv)
        right = [lr] + [2 * (s_ * round(math.log(s_ / (n * l0)), p) - dv) for p in (4, 5)]
        wrongs = {'score': dv ** 2 / (n * l0),
                  'wald': dv ** 2 / s_,   # the Wald form, also refused by the same clause
                  
                  'not-doubled': lr / 2,
                  'no-mean-term': 2 * s_ * math.log(s_ / (n * l0))}
        n_ += len(right) + len(wrongs)
        for v in right:
            if abs(v - it['answer']) > tol:
                bad.append(('poisson-ratio right working refused', it['seed'], v, it['answer']))
        for k, v in wrongs.items():
            if abs(v - it['answer']) <= tol:
                bad.append(('poisson-ratio wrong method accepted', it['seed'], k, v, it['answer']))
    # each new slip has its own wrong entry, so a learner who makes it gets its line, not the generic one
    for fam_set, fam in (('fluency-l18-counts-against-expectations', 'two-by-two'), ('fluency-l17-ratio-of-likelihoods', 'poisson-ratio-test')):
        for it in ck.sample(fam_set, fam)[:20]:
            ids = {w['id'] for w in it['wrong']}
            n_ += 1
            if fam == 'two-by-two' and not {'over-observed', 'likelihood-ratio'} <= ids:
                bad.append((fam, 'wrong entries missing', it['seed'], sorted(ids)))
            if fam == 'poisson-ratio-test' and 'score-form' not in ids:
                bad.append((fam, 'wrong entry missing', it['seed'], sorted(ids)))
    print('review-holes extra: %d checks, %d failures' % (n_, len(bad)))
    for b in bad[:20]:
        print('FAIL', b)
    return bad


if extra():
    sys.exit(1)
ck.run()
