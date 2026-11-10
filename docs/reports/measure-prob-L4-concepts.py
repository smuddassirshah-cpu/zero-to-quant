#!/usr/bin/env python3
"""Concept audit checks, measure-prob level 4 (l14 to l17, review-4, homework-4).

Run from anywhere: python3 docs/reports/measure-prob-L4-concepts.py
Exits 0 when every check passes. A check that fails because the content is wrong is
registered with expected_fail=True: it is listed as EXPECTED_FAIL, the corrected assert
sits next to it, and it does not change the exit code. If an EXPECTED_FAIL check starts
to pass (the content was fixed), it is listed as FIXED and the exit code is still 0.
"""
import json
import math
import os
import sys
from fractions import Fraction as F
from itertools import product

import numpy as np
from scipy import integrate, optimize, stats

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'measure-prob')
FILES = ['l14-radon-nikodym', 'l15-likelihood-ratios', 'l16-girsanov-on-a-tree',
         'l17-risk-neutral-rigorous', 'review-4', 'homework-4']
DOC = {f: json.load(open(os.path.join(CDIR, f + '.json'))) for f in FILES}

results = []  # (name, status)


def check(name, cond, expected_fail=False):
    cond = bool(cond)
    if expected_fail:
        status = 'FIXED' if cond else 'EXPECTED_FAIL'
    else:
        status = 'ok' if cond else 'FAIL'
    results.append((name, status))


def close(a, b, tol):
    return abs(a - b) <= tol


Phibar = lambda y: 0.5 * math.erfc(y / math.sqrt(2))

# ---------------------------------------------------------------------------
# 0. Code widgets: every solution passes its hidden tests, every starter fails
# ---------------------------------------------------------------------------


def run_widget(w, source):
    env = {}
    try:
        exec(w.get('prelude', ''), env)
        exec(source, env)
    except Exception:
        return 0, len(w['tests'])
    passed = 0
    for t in w['tests']:
        mode = t.get('compare', 'equal')
        try:
            if mode == 'raises':
                try:
                    eval(t['call'], env)
                    ok = False
                except Exception as e:  # noqa: BLE001
                    ok = isinstance(e, eval(str(t['expect']), env))
            else:
                got = eval(t['call'], env)
                exp = eval(str(t['expect']), env)
                if mode == 'isclose':
                    tol = t.get('tol', {})
                    ok = np.allclose(got, exp, rtol=tol.get('rel', 1e-9 if 'abs' in tol else 1e-6),
                                     atol=tol.get('abs', 0.0))
                else:
                    ok = got == exp
                    if ok is None or got is None or isinstance(got, type(Ellipsis)):
                        ok = False
        except Exception:  # noqa: BLE001
            ok = False
        passed += bool(ok)
    return passed, len(w['tests'])


def code_widgets():
    out = []
    for f in FILES:
        d = DOC[f]
        for key in ('screens', 'items', 'quiz'):
            for i, s in enumerate(d.get(key, [])):
                w = s.get('widget', {})
                if w.get('kind') == 'code':
                    out.append((f'{f} {key}[{i}]', w))
    return out


n_tests = 0
for label, w in code_widgets():
    p, n = run_widget(w, w['solution'])
    n_tests += n
    check(f'{label}: solution passes {n} hidden tests', p == n)
    p0, _ = run_widget(w, w['starter'])
    check(f'{label}: starter fails (passes {p0} of {n})', p0 < n)
    for e in w.get('examples', []):
        pe, ne = run_widget({'prelude': w.get('prelude', ''), 'tests': [e]}, w['solution'])
        check(f'{label}: example {e["call"][:40]}', pe == ne)

# ---------------------------------------------------------------------------
# l14 Radon-Nikodym
# ---------------------------------------------------------------------------
P6 = {k: F(1, 6) for k in range(1, 7)}
Q6 = {1: F(1, 10), 2: F(1, 10), 3: F(1, 10), 4: F(1, 5), 5: F(1, 5), 6: F(3, 10)}
Z6 = {k: Q6[k] / P6[k] for k in P6}
check('l14.s0 factors 0.6, 1.2, 1.8', [Z6[k] for k in (1, 4, 6)] == [F(3, 5), F(6, 5), F(9, 5)])
check('l14.s1 E_P[Z] = 1', sum(P6[k] * Z6[k] for k in P6) == 1)
check('l14.s2 option d: Q(A) <= P(A) for all A forces Q = P (search over 3-point measures)',
      all(q == p for p in [(F(1, 2), F(1, 4), F(1, 4))]
          for q in [(F(a, 8), F(b, 8), F(8 - a - b, 8)) for a in range(9) for b in range(9 - a)]
          if all(sum(q[i] for i in A) <= sum(p[i] for i in A)
                 for r in range(4) for A in __import__('itertools').combinations(range(3), r))))
check('l14.s3 Q(even) = 0.6, Q({5,6}) = 0.5',
      sum(P6[k] * Z6[k] for k in (2, 4, 6)) == F(3, 5) and sum(P6[k] * Z6[k] for k in (5, 6)) == F(1, 2))
EQface = sum(P6[k] * Z6[k] * k for k in P6)
check('l14.s7 E_Q[face] = 4.2, covariance 0.7', EQface == F(21, 5) and EQface - F(7, 2) == F(7, 10))
check('l14.s6 dP/dQ = 5/3, 5/6, 5/9', [1 / Z6[k] for k in (1, 4, 6)] == [F(5, 3), F(5, 6), F(5, 9)])
th = 0.5
Zn = lambda x, t=th: math.exp(t * x - t * t / 2)
phi = stats.norm.pdf
check('l14.s4 dQ/dP for N(theta,1) over N(0,1) is exp(theta x - theta^2/2)',
      all(close(phi(x, th, 1) / phi(x), Zn(x), 1e-12) for x in np.linspace(-4, 4, 33)))
check('l14.s4 E_P[Z] = 1 and without the correction it is exp(theta^2/2)',
      close(integrate.quad(lambda x: Zn(x) * phi(x), -12, 12)[0], 1, 1e-9)
      and close(integrate.quad(lambda x: math.exp(th * x) * phi(x), -12, 12)[0], math.exp(th * th / 2), 1e-9))
check('l14.q0 E_P[X Z(X)] = theta = 0.5',
      close(integrate.quad(lambda x: x * Zn(x) * phi(x), -12, 12)[0], 0.5, 1e-9))
# uniform pair: dP/dQ = 2 on [0,1]; Q-mean of dP/dQ is 1; Q << P fails
check('l14.s5 P([1,2]) = 0, Q([1,2]) = 1/2, E_Q[dP/dQ] = 1', close(2 * 0.5, 1, 0))
# l14.s5 option d why: "Q ignores only null sets of length 0". [3,4] has length 1 and Q([3,4]) = 0.
check('l14.s5 option d why: every Q-null set has length 0', not (stats.uniform(0, 2).cdf(4) - stats.uniform(0, 2).cdf(3) == 0),
      expected_fail=True)
# corrected: a Q-null interval meets [0,2] in length 0, hence meets [0,1] in length 0 (P-null)
check('l14.s5 corrected: Q-null sets meet [0,2] in length 0, so P << Q',
      stats.uniform(0, 1).cdf(4) - stats.uniform(0, 1).cdf(3) == 0)
# state prices
p, q, r = 0.7, 0.625, 0.05
check('l14.s9 Z_up 0.8929, Z_down 1.25, call 11.90, kernel 0.850 / 1.190, real-chance price 13.33',
      close(q / p, 0.8929, 5e-5) and close((1 - q) / (1 - p), 1.25, 1e-12)
      and close(p * (q / p) * 20 / 1.05, 11.90, 5e-3) and close(q / p / 1.05, 0.850, 5e-4)
      and close(1.25 / 1.05, 1.190, 5e-4) and close(p * 20 / 1.05, 13.33, 5e-3))
check('l14.q3 q = 0.6, Z_down = 0.8', close((1.02 - 0.9) / 0.2, 0.6, 1e-12) and close(0.4 / 0.5, 0.8, 1e-12))
# l14 summary.trap states E_Q[X] != E_P[Z] E_P[X] without condition. Counterexample: X uncorrelated with Z.
Xsym = {1: 1, 2: 0, 3: -1, 4: 1, 5: -1, 6: 0}   # cov_P(Z, X) = 0 on the die
lhs = sum(P6[k] * Z6[k] * Xsym[k] for k in P6)
rhs = sum(P6[k] * Z6[k] for k in P6) * sum(P6[k] * Xsym[k] for k in P6)
check('l14.summary.trap: E_Q[X] != E_P[Z]E_P[X] for every X', lhs != rhs, expected_fail=True)
# corrected: the two differ exactly by cov_P(Z, X)
check('l14.summary.trap corrected: E_Q[X] - E_P[Z]E_P[X] = cov_P(Z, X)',
      all(sum(P6[k] * Z6[k] * X[k] for k in P6) - sum(P6[k] * X[k] for k in P6)
          == sum(P6[k] * (Z6[k] - 1) * X[k] for k in P6) for X in (Xsym, {k: k for k in P6})))

# ---------------------------------------------------------------------------
# l15 likelihood ratios and importance sampling
# ---------------------------------------------------------------------------
tail4 = Phibar(4)
check('l15.s0 tail beyond 4 is 3.167e-5', close(tail4, 3.167e-5, 5e-9))


def relerr(theta, a=4.0):
    pa = Phibar(a)
    return math.sqrt(math.exp(theta ** 2) * Phibar(a + theta) - pa ** 2) / pa


check('l15.s1 relative error per draw: 177.7, 7.26, 2.12, 2.66, 5.63',
      close(relerr(0), 177.7, 0.05) and close(relerr(2), 7.26, 0.005) and close(relerr(4), 2.12, 0.005)
      and close(relerr(5), 2.66, 0.005) and close(relerr(6), 5.63, 0.005))
opt = optimize.minimize_scalar(relerr, bounds=(0, 8), method='bounded', options={'xatol': 1e-9})
check('l15.s1 minimum 2.115 near theta = 4.12', close(opt.x, 4.12, 0.005) and close(opt.fun, 2.115, 0.0005))
# second moment formula E_Q[(dP/dQ)^2 1{x>a}] = exp(theta^2) Phibar(a + theta), by quadrature
for t in (2.0, 4.0):
    m2 = integrate.quad(lambda x: math.exp(-2 * t * x + t * t) * phi(x, t, 1), 4, 14, epsabs=0, epsrel=1e-10)[0]
    check(f'l15.s1 second moment formula at theta = {t}', close(m2 / (math.exp(t * t) * Phibar(4 + t)), 1, 1e-6))
check('l15.s2 dP/dQ on HHT = 125/144', F(1, 8) / (F(3, 5) ** 2 * F(2, 5)) == F(125, 144))
rng = np.random.default_rng(21)
z21 = rng.standard_normal(10000)
check('l15.s0 seed 21: a plain run of 10,000 sees no loss above 4', int((z21 > 4).sum()) == 0)
x21 = z21 + 4
w21 = np.exp(-4 * x21 + 8) * (x21 > 4)
check('l15.s5/s6 seed 21: estimate 3.185e-5, s.e. 6.73e-7, 4,994 above 4, weights sum 0.3185',
      close(w21.mean(), 3.185e-5, 5e-9) and close(w21.std(ddof=1) / 100, 6.73e-7, 5e-10)
      and int((x21 > 4).sum()) == 4994 and close(w21.sum(), 0.3185, 5e-5))
inv = (np.exp(4 * x21 - 8) * (x21 > 4)).mean()
check('l15.s6/q3 inverted weight on seed 21 gives about 4e11 per 100,000 days', 3.5e11 < inv * 1e5 < 4.5e11)
# l15.q3 option d why: the undivided total "would give 0.3185", but the item reports per 100,000 days
check('l15.q3 option d: undivided total, in the item\'s unit per 100,000 days, is 0.3185',
      close(w21.sum() * 1e5, 0.3185, 5e-3), expected_fail=True)
check('l15.q3 option d corrected: undivided total is 31,850 per 100,000 days', close(w21.sum() * 1e5, 31850, 5))
# Monte Carlo: the estimator is unbiased and its per-draw relative error is as stated
rng = np.random.default_rng(2026)
xs = rng.standard_normal(2_000_000) + 4
ws = np.exp(-4 * xs + 8) * (xs > 4)
se = ws.std(ddof=1) / math.sqrt(ws.size)
check('l15 MC: weighted estimator within 4 s.e. of the exact tail', abs(ws.mean() - tail4) < 4 * se)
check('l15 MC: per-draw relative error at theta = 4 is 2.12 (2m draws)', close(ws.std(ddof=1) / tail4, 2.12, 0.03))
check('l15 MC: unweighted share estimates Q(X > 4) = 1/2, not the tail', close((xs > 4).mean(), 0.5, 0.002))
xs3 = rng.standard_normal(2_000_000) + 1.0
check('l15.s8 MC: the mean weight with no indicator is 1 (shown at theta = 1)', close(np.exp(-xs3 + 0.5).mean(), 1, 0.005))
check('l15.s8 plain error 27.2, IS error 1.826 at 3.15, n = 333 against 73,980, ratio 222',
      close(math.sqrt((1 - Phibar(3)) / Phibar(3)), 27.2, 0.05) and close(relerr(3.15, 3), 1.826, 0.0005)
      and close((1.826 / 0.1) ** 2, 333, 1) and close((27.2 / 0.1) ** 2, 73980, 10)
      and close(73984 / 333.4, 222, 0.5))
check('l15.q0-q2 weights: e^-4 = 0.0183, e^4 = 54.6, e^-6 = 0.00248, 13.5 days, 27%',
      close(math.exp(-4), 0.0183, 5e-5) and close(math.exp(4), 54.6, 0.05) and close(math.exp(-6), 0.00248, 5e-6)
      and close(1 / math.sqrt(13.5), 0.27, 0.005))

# ---------------------------------------------------------------------------
# l16 Girsanov on a tree
# ---------------------------------------------------------------------------


def paths(n):
    return [''.join(w) for w in product('HT', repeat=n)]


def chance(path, a):
    return a ** path.count('H') * (1 - a) ** path.count('T')


def Zw(path, pp, qq):
    return chance(path, qq) / chance(path, pp)


S = lambda w: w.count('H') - w.count('T')
pp, qq = F(3, 5), F(1, 2)
check('l16.s0/s1 E_P[Z_20 S_20] = 20(2q - 1) for q = 0.4, 0.5, 0.6, 0.7 (binomial sum)',
      all(sum(math.comb(20, k) * pp ** k * (1 - pp) ** (20 - k) * (qv / pp) ** k * ((1 - qv) / (1 - pp)) ** (20 - k)
              * (2 * k - 20) for k in range(21)) == 20 * (2 * qv - 1)
          for qv in (F(2, 5), F(1, 2), F(3, 5), F(7, 10))))
check('l16.s2 one-step weights 5/6 and 5/4, P-mean 1', qq / pp == F(5, 6) and (1 - qq) / (1 - pp) == F(5, 4)
      and pp * F(5, 6) + (1 - pp) * F(5, 4) == 1)
check('l16.s3 Z_3(HHT) = 125/144; slips 1.152 and 1.0417', Zw('HHT', pp, qq) == F(125, 144)
      and close(144 / 125, 1.152, 1e-9) and close(float(F(5, 6) * F(5, 4)), 1.0417, 5e-5))
# Z is a P-martingale, not a Q-martingale; E_Q of the one-step weight exceeds 1
ok = True
for n in range(0, 4):
    for pre in paths(n):
        nxt = pp * Zw(pre + 'H', pp, qq) + (1 - pp) * Zw(pre + 'T', pp, qq)
        ok &= nxt == Zw(pre, pp, qq)
check('l16.s4 E_P[Z_{n+1} | F_n] = Z_n at every node up to n = 3', ok)
check('l16.s4 d2: under Q the one-step weight has mean above 1 (25/24)',
      qq * F(5, 6) + (1 - qq) * F(5, 4) == F(25, 24))
# Bayes rule, exact, for a path-dependent X on a 4-step tree
runmax = lambda w: max([0] + [S(w[:i]) for i in range(1, len(w) + 1)])
ok = ok_b = ok_c = True
N = 4
for n in range(N + 1):
    for pre in paths(n):
        tl = paths(N - n)
        direct = sum(chance(t, qq) * runmax(pre + t) for t in tl)
        num = sum(chance(t, pp) * Zw(pre + t, pp, qq) * runmax(pre + t) for t in tl)
        ok &= direct == num / Zw(pre, pp, qq)
        if 0 < n < N and direct != 0:
            ok_b &= direct != num                      # option b is wrong at interior nodes
            ok_c &= direct != Zw(pre, pp, qq) * sum(chance(t, pp) * runmax(pre + t) for t in tl)
check('l16.s5 Bayes: E_Q[X|F_n] = E_P[Z_N X|F_n]/Z_n at every node', ok)
check('l16.s5 options b and c disagree with the Q-forecast at interior nodes', ok_b and ok_c)
check('l16.s5 tree labels 0.8333, 1.25, 0.6944, 1.0417, 1.5625',
      [round(float(Zw(w, pp, qq)), 4) for w in ('H', 'T', 'HH', 'HT', 'TT')] == [0.8333, 1.25, 0.6944, 1.0417, 1.5625])
# option c why says the future weight "is correlated with X": false for X = 1 (and any X independent of the future)
check('l16.s5 option c why: the future weight Z_N/Z_n is correlated with every X',
      all(sum(chance(t, pp) * Zw(t, pp, qq) * X(t) for t in paths(2))
          != sum(chance(t, pp) * X(t) for t in paths(2)) for X in (lambda w: 1, S)), expected_fail=True)
check('l16.s5 option c corrected: covariance is nonzero for X = S, zero for X = 1',
      sum(chance(t, pp) * Zw(t, pp, qq) * S(t) for t in paths(2)) != sum(chance(t, pp) * S(t) for t in paths(2))
      and sum(chance(t, pp) * Zw(t, pp, qq) for t in paths(2)) == 1)
# continuous limit table


def lnZ_moments(n, theta):
    e = theta / math.sqrt(n)
    pu = 0.5 * (1 + e)
    a, b = -math.log(1 + e), -math.log(1 - e)       # ln weight after up, after down (Q fair)
    m = pu * a + (1 - pu) * b
    v = pu * a * a + (1 - pu) * b * b - m * m
    return n * m, n * v


m100, v100 = lnZ_moments(100, 0.35)
m1e4, v1e4 = lnZ_moments(10000, 0.35)
check('l16.s6 table: n = 100 gives -0.06126, 0.12245; n = 10,000 gives -0.06125, 0.12250',
      close(m100, -0.06126, 5e-6) and close(v100, 0.12245, 5e-6) and close(m1e4, -0.06125, 5e-6)
      and close(v1e4, 0.12250, 5e-6))
# continuous Girsanov by Monte Carlo: Z = exp(-theta B_T - theta^2 T/2); under Q, B_T + theta T is N(0, T)
rng = np.random.default_rng(7)
theta, T = 0.35, 1.0
B = rng.standard_normal(2_000_000) * math.sqrt(T)
Zc = np.exp(-theta * B - theta ** 2 * T / 2)
Wt = B + theta * T
check('l16.s6 MC: E_P[Z] = 1', close(Zc.mean(), 1, 0.002))
check('l16.s6 MC: under Q, B_T + theta T has mean 0 and variance T',
      close((Zc * Wt).mean(), 0, 0.004) and close((Zc * Wt ** 2).mean(), T, 0.008))
Zplus = np.exp(theta * B - theta ** 2 * T / 2)
check('l16.s6 MC: the plus-sign weight gives mean 2 theta T instead (slip "plus" is wrong)',
      close((Zplus * Wt).mean(), 2 * theta * T, 0.006))
check('l16.s6 MC: without the correction the mean weight is exp(theta^2 T/2)',
      close(np.exp(-theta * B).mean(), math.exp(theta ** 2 * T / 2), 0.003))
# the table alone (mean and variance of ln Z) cannot fix the sign of theta B: both signs have the same law
check('l16.s6 explain: mean and variance of ln Z identify -theta B_1 - theta^2/2 as a function of B',
      not (close(np.log(Zplus).mean(), np.log(Zc).mean(), 0.002) and close(np.log(Zplus).var(), np.log(Zc).var(), 0.002)),
      expected_fail=True)
# corrected: the sign follows from the path: ln Z_n = -theta * (walk end) + theta^2/2 to first order
n = 10000
e = theta / math.sqrt(n)
U = rng.binomial(n, 0.5 * (1 + e), size=20000)
walk_end = (2 * U - n) / math.sqrt(n)
lnZ = -U * math.log(1 + e) - (n - U) * math.log(1 - e)
check('l16.s6 corrected: ln Z_n = -theta (walk) + theta^2/2 = -theta B_1 - theta^2/2 path by path',
      np.max(np.abs(lnZ - (-theta * (walk_end - theta) - theta ** 2 / 2))) < 5e-3)
# volatility claim: "the steps, the paths and the volatility stay"
varP = 1 - float(2 * pp - 1) ** 2
varQ = 1 - float(2 * qq - 1) ** 2
check('l16.s7/summary: the step has the same standard deviation under P and Q', close(varP, varQ, 1e-12),
      expected_fail=True)
check('l16.s7 corrected: squared steps add to n on every path (the pathwise volatility is unchanged)',
      all(sum((1 if c == 'H' else -1) ** 2 for c in w) == len(w) for w in paths(5)))
check('l16.s7 corrected: step variance 0.96 under P and 1.00 under Q; Var S_20 is 19.2 and 20',
      close(varP, 0.96, 1e-12) and close(varQ, 1.0, 1e-12))
check('l16.s7 corrected: with steps 1/sqrt(n) the gap in variance per unit time is theta^2/n, nil in the Brownian limit',
      all(close((1 - (0.35 / math.sqrt(m)) ** 2) - 1.0, -0.35 ** 2 / m, 1e-15) for m in (100, 10000)))
check('l16.s7 option b: mean step 0, variance 2/3 against 0.96; option c: weights average 0.9',
      close(0.6 * 2 / 3 - 0.4, 0, 1e-12) and close(0.6 * 4 / 9 + 0.4, 2 / 3, 1e-12)
      and pp * F(5, 6) + (1 - pp) == F(9, 10))
check('l16.s8 fair 4-step running maximum averages 19/16', sum(chance(w, qq) * runmax(w) for w in paths(4)) == F(19, 16))
check('l16.s9 weights 0.7972, 1.1161, 1.5625; call 15.59; unweighted 19.56',
      close((0.625 / 0.7) ** 2, 0.7972, 5e-5) and close(0.625 / 0.7 * 1.25, 1.1161, 5e-5)
      and close(0.49 * (0.625 / 0.7) ** 2 * 44 / 1.1025, 15.59, 5e-3) and close(0.49 * 44 / 1.1025, 19.56, 5e-3))
check('l16.q1 q = 1: Z = 0 on any path with a down move; q3 0.9453, 1.0579, 0.8403',
      Zw('HT', pp, F(1)) == 0 and close((0.55 / 0.6) ** 2 * 0.45 / 0.4, 0.9453, 5e-5)
      and close(1 / ((0.55 / 0.6) ** 2 * 0.45 / 0.4), 1.0579, 5e-5) and close((0.55 / 0.6) ** 2, 0.8403, 5e-5))

# ---------------------------------------------------------------------------
# l17 risk-neutral measure
# ---------------------------------------------------------------------------
u, d, r = 1.2, 0.8, 0.05
dS = lambda t, k: 100 * u ** k * d ** (t - k) / (1 + r) ** t
check('l17.s0 discounted prices 114.29, 76.19, 130.61, 87.07, 58.05',
      [round(dS(1, 1), 2), round(dS(1, 0), 2), round(dS(2, 2), 2), round(dS(2, 1), 2), round(dS(2, 0), 2)]
      == [114.29, 76.19, 130.61, 87.07, 58.05])
check('l17.s0 up node under q is 114.29; root under p is 102.86; slips 108.84 and 117.55',
      close(0.625 * dS(2, 2) + 0.375 * dS(2, 1), dS(1, 1), 1e-9) and close(0.7 * dS(1, 1) + 0.3 * dS(1, 0), 102.86, 5e-3)
      and close(0.5 * 130.61 + 0.5 * 87.07, 108.84, 5e-3) and close(0.7 * 130.61 + 0.3 * 87.07, 117.55, 5e-3))
# first fundamental theorem on the one-period binomial market: arbitrage exists iff not d < 1+r < u.
# An arbitrage is a share holding h (financed by cash) with h(S1 - S0(1+r)) >= 0 in both states, > 0 in one.


def has_arbitrage(uu, dd, rr):
    gu, gd = uu - (1 + rr), dd - (1 + rr)
    return any(h * gu >= 0 and h * gd >= 0 and (h * gu > 0 or h * gd > 0) for h in (1, -1))


grid = [(F(a, 20), F(b, 20), F(c, 20)) for a in range(18, 30) for b in range(10, 24) for c in range(0, 5) if b < a]
check('l17.s1/s2 FTAP, one period: no arbitrage exactly when q lies in (0,1), i.e. d < 1+r < u (grid of %d trees)' % len(grid),
      all(has_arbitrage(a, b, c) == (not 0 < (1 + c - b) / (a - b) < 1) for a, b, c in grid))
check('l17.s2 q = 25/24 = 1.0417; short share, hold 105, owe at most 104', F(105 - 80, 104 - 80) == F(25, 24)
      and close(25 / 24, 1.0417, 5e-5))
# easy direction: any self-financing strategy with V0 = 0 has E_Q[discounted V_2] = 0 (two-step tree)
rng = np.random.default_rng(11)
ok = True
for _ in range(200):
    D1, D2u, D2d = rng.normal(size=3)
    tot = 0.0
    for w, pr in (('UU', 0.625 ** 2), ('UD', 0.625 * 0.375), ('DU', 0.375 * 0.625), ('DD', 0.375 ** 2)):
        k1 = 1 if w[0] == 'U' else 0
        k2 = k1 + (1 if w[1] == 'U' else 0)
        D2 = D2u if w[0] == 'U' else D2d
        V = D1 * (dS(1, k1) - dS(0, 0)) + D2 * (dS(2, k2) - dS(1, k1))
        tot += pr * V
    ok &= abs(tot) < 1e-9
check('l17.s3 gains of 200 random predictable strategies have Q-mean 0', ok)
qu, qm, qd = 0.625 ** 2, 2 * 0.625 * 0.375, 0.375 ** 2
check('l17.s4 put 6.29; slips 6.61 and 4.46; parity 15.59 - 6.29 = 9.30',
      close((qm * 4 + qd * 36) / 1.1025, 6.29, 5e-3) and close((qm * 4 + qd * 36) / 1.05, 6.61, 5e-3)
      and close((0.42 * 4 + 0.09 * 36) / 1.1025, 4.46, 5e-3)
      and close(qu * 44 / 1.1025 - (qm * 4 + qd * 36) / 1.1025, 100 - 100 / 1.1025, 1e-9))


def bs_call(S0, K, rr, sig, TT, drift=None):
    mu = rr if drift is None else drift
    d1 = (math.log(S0 / K) + (mu + sig * sig / 2) * TT) / (sig * math.sqrt(TT))
    d2 = d1 - sig * math.sqrt(TT)
    return math.exp(-rr * TT) * (S0 * math.exp(mu * TT) * stats.norm.cdf(d1) - K * stats.norm.cdf(d2))


check('l17.s5/q2 Black-Scholes 10.4506; real-drift slip 15.53; undiscounted slip 10.99',
      close(bs_call(100, 100, 0.05, 0.2, 1), 10.4506, 5e-5) and close(bs_call(100, 100, 0.05, 0.2, 1, 0.12), 15.53, 5e-3)
      and close(bs_call(100, 100, 0.05, 0.2, 1) * math.exp(0.05), 10.99, 5e-3)
      and close(stats.norm.cdf(0.35), 0.636831, 5e-7) and close(stats.norm.cdf(0.15), 0.559618, 5e-7))
rng = np.random.default_rng(5)
G = rng.standard_normal(2_000_000)
ST_Q = 100 * np.exp((0.05 - 0.02) + 0.2 * G)
ST_P = 100 * np.exp((0.12 - 0.02) + 0.2 * G)
check('l17.s5 MC: E_Q[e^{-rT} S_T] = 100; under P it is 100 e^{0.07}',
      close(math.exp(-0.05) * ST_Q.mean(), 100, 0.06) and close(math.exp(-0.05) * ST_P.mean(), 100 * math.exp(0.07), 0.07))
check('l17.s5 MC: E_Q[e^{-rT}(S_T - K)^+] = 10.4506',
      close(math.exp(-0.05) * np.maximum(ST_Q - 100, 0).mean(), 10.4506, 0.04))
check('l17.s6 call 15.59, with p 19.56 (3.97 too high), one discount 16.37',
      close(qu * 44 / 1.1025, 15.59, 5e-3) and close(0.49 * 44 / 1.1025, 19.56, 5e-3)
      and close(0.49 * 44 / 1.1025 - qu * 44 / 1.1025, 3.97, 5e-3) and close(qu * 44 / 1.05, 16.37, 5e-3))
# trinomial: range of martingale prices by linear programming (closure of the open range)


def emm_range(S1, payoff, S0=100.0, extra=None):
    A = [list(S1), [1, 1, 1]]
    b = [S0, 1]
    if extra:
        A.append(extra[0]); b.append(extra[1])
    lo = optimize.linprog(payoff, A_eq=A, b_eq=b, bounds=[(0, 1)] * 3)
    hi = optimize.linprog([-x for x in payoff], A_eq=A, b_eq=b, bounds=[(0, 1)] * 3)
    return lo.fun, -hi.fun


lo, hi = emm_range([120, 100, 80], [20, 0, 0])
check('l17.s7 trinomial call: martingale prices fill (0, 10); 1/3 each gives 6.67', close(lo, 0, 1e-8)
      and close(hi, 10, 1e-8) and close(20 / 3, 6.67, 5e-3))
check('l17.s7/q3 incomplete: payoff matrix of cash and share has rank 2 on 3 states',
      np.linalg.matrix_rank(np.array([[1, 1, 1], [120, 100, 80]])) == 2)
check('l17.s9 drift of the share under P is 8% a step', close(0.7 * 1.2 + 0.3 * 0.8, 1.08, 1e-12))
check('l17.q0 q = 0.4667; q1 gain 1 to 25', close(0.07 / 0.15, 0.4667, 5e-5) and (105 - 104, 105 - 80) == (1, 25))

# ---------------------------------------------------------------------------
# review-4
# ---------------------------------------------------------------------------
Pr, Qr, Xr = (F(1, 2), F(1, 4), F(1, 4)), (F(1, 4), F(1, 4), F(1, 2)), (10, 20, 30)
check('r4[0] E_Q[X] = 22.5, E_P[X] = 17.5', sum(q_ * x for q_, x in zip(Qr, Xr)) == F(45, 2)
      and sum(p_ * (q_ / p_) * x for p_, q_, x in zip(Pr, Qr, Xr)) == F(45, 2)
      and sum(p_ * x for p_, x in zip(Pr, Xr)) == F(35, 2))
check('r4[1] e^-6 = 0.0025, e^6 = 403.4, e^-10.5 = 2.75e-5', close(math.exp(-6), 0.0025, 5e-5)
      and close(math.exp(6), 403.4, 0.05) and close(math.exp(-10.5), 2.75e-5, 5e-8))
check('r4[2] Z_3(THH) = 0.9183, slips 1.089 and 0.8264', close((0.5 / 0.55) ** 2 * 0.5 / 0.45, 0.9183, 5e-5)
      and close(1 / ((0.5 / 0.55) ** 2 * 0.5 / 0.45), 1.089, 5e-4) and close((0.5 / 0.55) ** 2, 0.8264, 5e-5))
check('r4[3] q = 0.52', close(0.13 / 0.25, 0.52, 1e-12))
check('r4[4] dP/dQ = (1/2, 3, 0); Q << P fails', [F(1, 4) / F(1, 2), F(3, 4) / F(1, 4), F(0) / F(1, 4)] == [F(1, 2), 3, 0])
check('r4[5] error per draw 6.554, n = 17,182; tail 0.02275; best shift near 2.2',
      close(Phibar(2), 0.02275, 5e-6) and close(math.sqrt(0.97725 / 0.02275), 6.554, 5e-4)
      and close(0.97725 / 0.02275 / 0.0025, 17182, 1)
      and close(optimize.minimize_scalar(lambda t: relerr(t, 2), bounds=(0, 6), method='bounded').x, 2.2, 0.05))
check('r4[6] q = 0.14/0.13 = 1.0769', close(0.14 / 0.13, 1.0769, 5e-5))
check('r4[7] q = 0.55, Z_UU = 1.89, call 19.67, slips 0.5289, 10.41, 20.26',
      close((1.03 - 0.7) / 0.6, 0.55, 1e-12) and close(1.375 ** 2, 1.8906, 5e-5) and close(0.3025 * 69 / 1.0609, 19.67, 5e-3)
      and close(1 / 1.375 ** 2, 0.5289, 5e-5) and close(0.16 * 69 / 1.0609, 10.41, 5e-3)
      and close(0.3025 * 69 / 1.03, 20.26, 5e-3) and 100 * 1.3 * 0.7 < 100)

# ---------------------------------------------------------------------------
# homework-4
# ---------------------------------------------------------------------------
Ph, Qh = (F(2, 5), F(3, 10), F(1, 5), F(1, 10)), (F(1, 10), F(1, 5), F(3, 10), F(2, 5))
check('h4[0] Z = (1/4, 2/3, 3/2, 4); E_Q X = 3, E_Q X^2 = 10, E_P X = 2, E_P X^2 = 5',
      [q_ / p_ for p_, q_ in zip(Ph, Qh)] == [F(1, 4), F(2, 3), F(3, 2), 4]
      and sum(q_ * x for q_, x in zip(Qh, range(1, 5))) == 3 and sum(q_ * x * x for q_, x in zip(Qh, range(1, 5))) == 10
      and sum(p_ * x for p_, x in zip(Ph, range(1, 5))) == 2 and sum(p_ * x * x for p_, x in zip(Ph, range(1, 5))) == 5)
a3 = 6 / math.sqrt(3)
o3 = optimize.minimize_scalar(lambda t: relerr(t, a3), bounds=(0, 8), method='bounded', options={'xatol': 1e-9})
pl = math.sqrt((1 - Phibar(a3)) / Phibar(a3))
check('h4[1] tail 26.60 per 100,000; slip 2,275; best shift 3.600; errors 1.964 and 61.3; 386 and about 375,800 draws',
      close(Phibar(a3) * 1e5, 26.60, 5e-3) and close(Phibar(2) * 1e5, 2275, 0.5) and close(o3.x, 3.600, 5e-4)
      and close(o3.fun, 1.964, 5e-4) and close(relerr(3.6, a3), 1.964, 5e-4) and close(pl, 61.3, 0.05)
      and close((1.964 / 0.1) ** 2, 386, 0.5) and close((61.3 / 0.1) ** 2, 375800, 100) and close(375769 / 385.7, 970, 10))
rng = np.random.default_rng(13)
L = rng.standard_normal((400_000, 3)).sum(axis=1) / math.sqrt(3) + 3.6
wL = np.exp(-3.6 * L + 3.6 ** 2 / 2) * (L > a3)
check('h4[1] MC: shifting the standardised sum estimates P(L > 6) within 4 s.e.',
      abs(wL.mean() - Phibar(a3)) < 4 * wL.std(ddof=1) / math.sqrt(wL.size))
# h4[2]: dP/dQ in terms of W~ ; MC under Q: W~ is N(0,T); dP/dQ = exp(theta W~ - theta^2 T/2) has Q-mean 1
rng = np.random.default_rng(17)
Wt = rng.standard_normal(2_000_000)
Rq = np.exp(0.4 * Wt - 0.08)
check('h4[2] MC under Q: dP/dQ has mean 1, and W = W~ - theta T has P-mean 0, P-variance T',
      close(Rq.mean(), 1, 0.003) and close((Rq * (Wt - 0.4)).mean(), 0, 0.004) and close((Rq * (Wt - 0.4) ** 2).mean(), 1, 0.01))
check('h4[2] e^0.32 = 1.3771, e^-0.48 = 0.6188, e^0.4 = 1.4918', close(math.exp(0.32), 1.3771, 5e-5)
      and close(math.exp(-0.48), 0.6188, 5e-5) and close(math.exp(0.4), 1.4918, 5e-5))
check('h4[3] q = 0.5, Z_DD = 2.0408, put 4.31, slips 0.49, 2.11, 4.52, 0.69; p = 0.8 gives 6.25 x 0.04 = 0.25',
      close((1.05 - 0.9) / 0.3, 0.5, 1e-12) and close((0.5 / 0.35) ** 2, 2.0408, 5e-5) and close(0.25 * 19 / 1.1025, 4.31, 5e-3)
      and close(0.35 ** 2 / 0.25, 0.49, 1e-9) and close(0.1225 * 19 / 1.1025, 2.11, 5e-3) and close(0.25 * 19 / 1.05, 4.52, 5e-3)
      and close(0.04 * 19 / 1.1025, 0.69, 5e-3) and close(6.25 * 0.04, 0.25, 1e-12) and 100 * 1.2 * 0.9 >= 100)
lo, hi = emm_range([130, 100, 70], [0, 0, 30])
check('h4[4] put range (0, 15)', close(lo, 0, 1e-8) and close(hi, 15, 1e-8))
lo, hi = emm_range([130, 100, 70], [0, 0, 30], extra=([30, 0, 0], 6))
# h4[4] part 0 says "Every martingale measure has q_m > 0": (1/2, 0, 1/2) is a martingale measure, not equivalent to P
qb = (F(1, 2), F(0), F(1, 2))
is_mm = sum(qb) == 1 and 130 * qb[0] + 100 * qb[1] + 70 * qb[2] == 100 and min(qb) >= 0
check('h4[4] part 0: every martingale measure has q_m > 0', not is_mm, expected_fail=True)
check('h4[4] corrected: every EQUIVALENT martingale measure has all chances positive, so the put stays below 15',
      is_mm and 30 * qb[2] == 15)
check('h4[4] with the call at 6 the put is 6 under every martingale measure; the market is complete (rank 3)',
      close(lo, 6, 1e-8) and close(hi, 6, 1e-8)
      and np.linalg.matrix_rank(np.array([[1, 1, 1], [130, 100, 70], [30, 0, 0]])) == 3)
check('h4[5] q = 15/13 = 1.1538; gains 2 and 15', close(0.15 / 0.13, 1.1538, 5e-5) and (110 - 108, 110 - 95) == (2, 15))
# h4[8] long form
q8, p8 = 0.58, 0.65
zu, zd = q8 / p8, (1 - q8) / (1 - p8)
check('h4[8] q = 0.58; weights 0.8923, 1.2; Z_2 = 0.7962, 1.0708, 1.44; Q-chances 0.3364, 0.4872, 0.1764',
      close((1.04 - 0.75) / 0.5, 0.58, 1e-12) and close(zu, 0.8923, 5e-5) and close(zd, 1.2, 1e-12)
      and close(zu * zu, 0.7962, 5e-5) and close(zu * zd, 1.0708, 5e-5) and close(zd * zd, 1.44, 1e-12)
      and close(0.4225 * zu * zu, 0.3364, 1e-9) and close(0.455 * zu * zd, 0.4872, 1e-9) and close(0.1225 * zd * zd, 0.1764, 1e-9))
d8 = lambda t, k: 100 * 1.25 ** k * 0.75 ** (t - k) / 1.04 ** t
check('h4[8] discounted prices 120.19, 72.12, 144.46, 86.68, 52.01; root under P 103.37',
      [round(d8(1, 1), 2), round(d8(1, 0), 2), round(d8(2, 2), 2), round(d8(2, 1), 2), round(d8(2, 0), 2)]
      == [120.19, 72.12, 144.46, 86.68, 52.01] and close(0.65 * d8(1, 1) + 0.35 * d8(1, 0), 103.37, 5e-3)
      and close(0.58 * d8(2, 2) + 0.42 * d8(2, 1), d8(1, 1), 1e-9) and close(0.58 * d8(1, 1) + 0.42 * d8(1, 0), 100, 1e-9))
check('h4[8] call 17.49; with p^2 alone 21.97', close(0.3364 * 56.25 / 1.0816, 17.49, 5e-3)
      and close(0.4225 * 56.25 / 1.0816, 21.97, 5e-3) and 100 * 1.25 * 0.75 < 100)

# ---------------------------------------------------------------------------
fails = [n for n, s in results if s == 'FAIL']
xf = [n for n, s in results if s == 'EXPECTED_FAIL']
fixed = [n for n, s in results if s == 'FIXED']
for n, s in results:
    if s != 'ok':
        print(f'{s}: {n}')
print(f'{len(results)} checks: {sum(s == "ok" for _, s in results)} ok, {len(xf)} EXPECTED_FAIL, '
      f'{len(fixed)} FIXED, {len(fails)} FAIL; {n_tests} hidden tests run')
sys.exit(1 if fails else 0)
