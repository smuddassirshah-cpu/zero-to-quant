"""Second reader's recomputation of stat-models problems-4 (Bayesian models).

Imports nothing from the author's script. Every prior, data summary and list is typed from the
problem's prose. Route 1 is the conjugate closed form. Route 2 is a different method: a grid or
quadrature posterior, conditioning a joint normal, scipy's log densities, a numerical maximum of
the marginal likelihood, the exact finite-n variance of an AR(1) mean and a seeded simulation.
Every `wrong` value is rebuilt from the slip its line names; every band is tested against the key
band and the other slip bands; every rounded value a part restates is fed forward.
Exit 0 always on a clean run of the script; a failing check prints a FINDING line (CI rule,
session AE). Claims found weak by reading are also printed as FINDING lines.
Run: <venv>/bin/python docs/reports/problems-stat-models-4-numbers-read.py
"""
import json
import math
import os
import re
import sys

import numpy as np
from scipy import integrate, optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'stat-models', 'problems-4.json')
if len(sys.argv) > 1:          # a copy of the set, to test replacement lines
    PATH = sys.argv[1]
SET = json.load(open(PATH))
checks = 0
findings = []


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        findings.append(msg)


def claim(msg):
    findings.append(msg)


def item(iid):
    return next(x for x in SET['items'] if x['id'] == iid)


def key(iid, k):
    w = item(iid)['parts'][k]['widget']
    return w['answer'], w['tol']['abs']


def wrong(iid, k, wid):
    w = next(x for x in item(iid)['parts'][k]['widget']['wrong'] if x['id'] == wid)
    return w['value'], w['tol']['abs']


def check_key(iid, k, *routes, fed=None):
    """Each route within the tolerance of the key; `fed` is the value the restated, rounded inputs give."""
    a, tol = key(iid, k)
    for n, r in enumerate(routes):
        ok(abs(a - r) <= tol + 1e-12, f'{iid} part {k + 1}: key {a} against route {n + 1} = {r:.6f}')
    if fed is not None:
        ok(abs(a - fed) <= tol + 1e-12, f'{iid} part {k + 1}: key {a} refuses the fed-forward value {fed:.6f}')


def check_wrong(iid, k, wid, mine, typed=None):
    """The slip rebuilt lands in its own band; `typed` is what a learner types at the stated places."""
    v, tol = wrong(iid, k, wid)
    ok(abs(v - mine) <= tol + 1e-12, f'{iid} part {k + 1} wrong {wid}: {v} against slip rebuilt {mine:.6f}')
    if typed is not None:
        ok(abs(v - typed) <= tol + 1e-9, f'{iid} part {k + 1} wrong {wid}: band refuses the typed {typed}')


def check_bands(iid):
    for k, p in enumerate(item(iid)['parts']):
        w = p['widget']
        if w['kind'] != 'numeric':
            continue
        bands = [('key', w['answer'], w['tol']['abs'])] + [(x['id'], x['value'], x['tol']['abs']) for x in w.get('wrong', [])]
        for i in range(len(bands)):
            for j in range(i + 1, len(bands)):
                (n1, v1, t1), (n2, v2, t2) = bands[i], bands[j]
                ok(abs(v1 - v2) > t1 + t2, f'{iid} part {k + 1}: bands {n1} and {n2} meet')
        ids = {x['id'] for x in w.get('wrong', [])}
        ok(ids == set(p['feedback'].get('byKey', {})), f'{iid} part {k + 1}: wrong ids and byKey lines differ')


def shown(iid, k, field, text):
    p = item(iid)['parts'][k]
    blob = json.dumps(p['feedback'], ensure_ascii=False) if field == 'feedback' else p['explain']['text'] if field == 'explain' else p['question']
    ok(text in blob, f'{iid} part {k + 1} {field}: expected to print {text!r}')


Phi = stats.norm.cdf

# ---------------------------------------------------------------- p-etf-tracking
E = 'p-etf-tracking'
m0, s0, sig, n, ybar, m_new = -0.3, 0.2, 1.5, 36, -0.82, 20
se = sig / math.sqrt(n)
ok(abs(se - 0.25) < 1e-12, 'etf: the standard error 1.5/6 is 0.25')
prec = 1 / s0 ** 2 + 1 / se ** 2
ok(abs(prec - 41) < 1e-9, 'etf: precisions 25 and 16 sum to 41')
sd1 = 1 / math.sqrt(prec)
mean1 = (m0 / s0 ** 2 + ybar / se ** 2) / prec
# route 2: posterior moments by quadrature of prior times the likelihood of the 36-day mean
kern = lambda t: stats.norm.pdf(t, m0, s0) * stats.norm.pdf(ybar, t, se)
Z = integrate.quad(kern, -3, 2, epsabs=1e-14)[0]
qm = integrate.quad(lambda t: t * kern(t), -3, 2, epsabs=1e-14)[0] / Z
qv = integrate.quad(lambda t: (t - qm) ** 2 * kern(t), -3, 2, epsabs=1e-14)[0] / Z
check_key(E, 0, sd1, math.sqrt(qv))
check_key(E, 1, mean1, qm, fed=(25 * m0 + 16 * ybar) / 41)
ok(abs(25 * m0 + 16 * ybar + 20.62) < 1e-9, 'etf part 2: the weighted sum is -20.62')
check_wrong(E, 0, 'add-var', math.sqrt(s0 ** 2 + se ** 2))
check_wrong(E, 0, 'daily-error', 1 / math.sqrt(1 / s0 ** 2 + 1 / sig ** 2))
check_wrong(E, 1, 'data-only', ybar)
check_wrong(E, 1, 'plain-average', (m0 + ybar) / 2)
check_wrong(E, 1, 'swapped', (16 * m0 + 25 * ybar) / 41)
check_wrong(E, 1, 'sign', -mean1)
ok(abs(25 / 41 - 0.61) < 0.005 and abs(16 / 41 - 0.39) < 0.005, 'etf part 2 explain: weights 0.61 and 0.39')
# part 3, route 1: noise of the average plus the posterior variance
sdp = math.sqrt(sig ** 2 / m_new + 1 / prec)
# route 2: condition the joint normal of (36-day mean, next 20-day mean), theta integrated out
v_old = s0 ** 2 + se ** 2
v_new = s0 ** 2 + sig ** 2 / m_new
cov = s0 ** 2
cond_var = v_new - cov ** 2 / v_old
cond_mean = m0 + cov / v_old * (ybar - m0)
ok(abs(cond_mean - mean1) < 1e-12, 'etf: the conditional mean of the new average is the posterior mean')
check_key(E, 2, sdp, math.sqrt(cond_var), fed=math.sqrt(2.25 / 20 + 1 / 41))
ok(abs(sig ** 2 / m_new - 0.1125) < 1e-12 and abs(1 / 41 - 0.0244) < 5e-5 and abs(sdp ** 2 - 0.1369) < 5e-5, 'etf part 3: 0.1125, 0.0244, 0.1369')
check_wrong(E, 2, 'plug-in', sig / math.sqrt(m_new))
check_wrong(E, 2, 'one-day', math.sqrt(sig ** 2 + 1 / prec))
check_wrong(E, 2, 'variance', sdp ** 2)
check_wrong(E, 2, 'theta-only', sd1)
# part 4, route 1 exact, route 2 the plug-in tail averaged over the posterior by quadrature
tail = Phi((-1 - mean1) / sdp)
tail_q = integrate.quad(lambda t: Phi((-1 - t) / math.sqrt(sig ** 2 / m_new)) * stats.norm.pdf(t, mean1, sd1), -3, 2, epsabs=1e-14)[0]
tail_fed = Phi((-1 + 0.5029) / 0.3700)
check_key(E, 3, tail, tail_q, fed=tail_fed)
ok(abs((-1 + 0.5029) / 0.3700 + 1.3435) < 5e-5, 'etf part 4: z = -1.3435')
check_wrong(E, 3, 'plug-in', Phi((-1 + 0.5029) / 0.3354))
check_wrong(E, 3, 'upper', 1 - tail_fed)
check_wrong(E, 3, 'theta-sd', Phi((-1 + 0.5029) / 0.1562))
ok(abs(Phi((-1 + 0.5029) / 0.3354) - 0.0692) < 5e-5, 'etf part 4 explain: plug-in tail 0.0692')
check_bands(E)
# a learner with a printed normal table reads z to 2 places
a4, t4 = key(E, 3)
table = Phi(-1.34)
if abs(table - a4) > t4 and 'Phi' not in item(E)['parts'][3]['question']:
    claim(f'etf part 4: no source for the normal tail is named; a table at z = -1.34 gives {table:.4f}, refused by the key band {a4} +/- {t4} (review finding 10)')

# ---------------------------------------------------------------- p-circuit-breaker
# Removed in the fix pass: the problem was re-authored as p-iceberg-refills (review finding 4).
# The delta reader checks the new problem; this script only confirms the old id is gone (below).

# ---------------------------------------------------------------- p-quality-six-markets
Q = 'p-quality-six-markets'
y = np.array([1.9, 0.4, 1.1, -0.2, 0.8, 1.4])
s = 0.5
mu = y.mean()
ok(abs(mu - 0.9) < 1e-12, 'quality: the plain mean is 0.9')
gaps = (y - mu) ** 2
ok(np.allclose(gaps, [1, 0.25, 0.04, 1.21, 0.01, 0.25]) and abs(gaps.sum() - 2.76) < 1e-12, 'quality part 1: squared gaps and their sum 2.76')
tot = gaps.sum() / 6
tau2 = tot - s ** 2
# route 2: maximise the marginal likelihood N(mu, 0.25 + tau^2) over (mu, ln tau^2)
nll = lambda p: -stats.norm.logpdf(y, p[0], math.sqrt(s ** 2 + math.exp(p[1]))).sum()
fit = optimize.minimize(nll, [0.5, math.log(0.1)], method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12, 'maxiter': 4000})
ok(abs(fit.x[0] - 0.9) < 1e-5, f'quality prose: the marginal MLE of mu is the plain mean ({fit.x[0]:.6f})')
check_key(Q, 0, tot, s ** 2 + math.exp(fit.x[1]))
check_key(Q, 1, tau2, math.exp(fit.x[1]))
check_wrong(Q, 0, 'divisor-5', gaps.sum() / 5, typed=0.55)
check_wrong(Q, 0, 'root', math.sqrt(tot), typed=0.68)
check_wrong(Q, 1, 'from-divisor-5', gaps.sum() / 5 - s ** 2, typed=0.30)
check_wrong(Q, 1, 'minus-se', tot - s)
B = s ** 2 / (s ** 2 + tau2)
check_key(Q, 2, B, 1 - math.exp(fit.x[1]) / (s ** 2 + math.exp(fit.x[1])), fed=0.25 / (0.25 + 0.21))
check_wrong(Q, 2, 'kept-share', 1 - B)
check_wrong(Q, 2, 'sd-ratio', s / (s + math.sqrt(tau2)))
ok(abs(math.sqrt(tau2) - 0.4583) < 5e-5, 'quality part 3: tau-hat 0.4583')
yj = -0.2
shr = mu + (1 - B) * (yj - mu)
# route 2: posterior mean of theta_j by quadrature of N(theta; mu, tau2) times N(yj; theta, s2)
kq = lambda t: stats.norm.pdf(t, mu, math.sqrt(tau2)) * stats.norm.pdf(yj, t, s)
Zq = integrate.quad(kq, -4, 5, epsabs=1e-14)[0]
shr_q = integrate.quad(lambda t: t * kq(t), -4, 5, epsabs=1e-14)[0] / Zq
check_key(Q, 3, shr, shr_q, fed=0.9 + (1 - 0.5435) * (yj - 0.9))
ok(abs((1 - 0.5435) * 1.1 - 0.5022) < 5e-5, 'quality part 4: the kept gap is 0.5022')
check_wrong(Q, 3, 'kept-b', mu + B * (yj - mu))
check_wrong(Q, 3, 'towards-zero', (1 - B) * yj)
check_wrong(Q, 3, 'raw', yj)
psd = 1 / math.sqrt(1 / s ** 2 + 1 / tau2)
ok(abs(1 / s ** 2 + 1 / tau2 - 8.762) < 5e-4 and abs(psd - 0.3378) < 5e-5, 'quality part 5: precision 8.762, sd 0.3378')
ok(abs(psd - math.sqrt((1 - B) * s ** 2)) < 1e-12, 'quality part 5: sd is also the root of (1 - B) times 0.25')
ppos = 1 - Phi(-shr / psd)
ppos_q = integrate.quad(kq, 0, 5, epsabs=1e-14)[0] / Zq
check_key(Q, 4, ppos, ppos_q, fed=Phi(0.3978 / 0.3378))
check_wrong(Q, 4, 'se-as-sd', Phi(0.3978 / 0.5))
check_wrong(Q, 4, 'raw', Phi(yj / s))
check_wrong(Q, 4, 'lower', 1 - Phi(0.3978 / 0.3378))
check_wrong(Q, 4, 'tau-as-sd', Phi(0.3978 / 0.4583))
ok(round(100 * Phi(yj / s)) == 34 and round(100 * ppos) == 88, 'quality part 5 explain: 34% alone, 88% pooled')
check_bands(Q)
a5, t5 = key(Q, 4)
table = Phi(1.18)
if abs(table - a5) > t5 and 'Phi' not in item(Q)['parts'][4]['question']:
    claim(f'quality part 5: no source for the normal tail is named; a table at z = 1.18 gives {table:.4f}, refused by the key band {a5} +/- {t5} (review finding 10)')

# ---------------------------------------------------------------- p-dealer-enquiries
# Removed in the fix pass: the problem was re-authored as p-four-books (main-session ruling; review
# findings 6 to 9 fall away). The delta reader checks the new problem.

# ---------------------------------------------------------------- findings of the reading, tested on the text
blob = json.dumps(SET, ensure_ascii=False)
ok(not any(x['id'] in ('p-circuit-breaker', 'p-dealer-enquiries') for x in SET['items']),
   're-authored problems p-circuit-breaker and p-dealer-enquiries are gone (review findings 4, 6 to 9)')
ok('So the code has a fault' not in blob, 'the claim of review finding 9 does not return')
ok('You kept $B$ of the gap, not $1 - B$.' not in blob, 'quality part 4 kept-b is word for word l18 screen 4 byKey.b and r4-shrink byKey.keepb (review finding 5)')
ok('Where is the chain after this step' not in blob.replace('where', 'Where'),
   'no part asks the question of q16-step, r4-step and e-metropolis-log (review finding 4)')

# ---------------------------------------------------------------- values for the replacement lines of the review
for name, zval, printed in [('Phi(1.3435)', 1.3435, 0.9104), ('Phi(1.4821)', 1.4821, 0.9308), ('Phi(3.1825)', 3.1825, 0.9993),
                            ('Phi(1.1776)', 1.1776, 0.8805), ('Phi(0.7956)', 0.7956, 0.7869), ('Phi(0.8680)', 0.8680, 0.8073)]:
    ok(abs(Phi(zval) - printed) < 5e-5, f'replacement text: {name} = {Phi(zval):.5f}, printed {printed}')
ok(abs(0.4971 / 0.3354 - 1.4821) < 5e-5 and abs(0.4971 / 0.1562 - 3.1825) < 5e-5 and abs(0.4971 / 0.3700 - 1.3435) < 5e-5, 'replacement text: z of the key and of the plug-in and theta-sd slips')
ok(abs(0.3978 / 0.5 - 0.7956) < 5e-5 and abs(0.3978 / 0.4583 - 0.8680) < 5e-5 and abs(0.3978 / 0.3378 - 1.1776) < 5e-5, 'replacement text: z of the three sds')
ok(abs(1 - 0.9104 - key(E, 3)[0]) <= 1e-4 + 1e-12, 'replacement text: 1 - 0.9104 is taken by the etf part 4 key')
ok(abs(1 - 0.9308 - wrong(E, 3, 'plug-in')[0]) <= 1e-4 + 1e-12 and abs(1 - 0.9993 - wrong(E, 3, 'theta-sd')[0]) <= 1e-4 + 1e-12, 'replacement text: the two slip tails stay in their bands')
ok(abs(0.8805 - key(Q, 4)[0]) <= 1e-4 + 1e-12 and abs(0.7869 - wrong(Q, 4, 'se-as-sd')[0]) <= 1e-4 + 1e-12 and abs(0.8073 - wrong(Q, 4, 'tau-as-sd')[0]) <= 1e-4 + 1e-12
   and abs(1 - 0.8805 - wrong(Q, 4, 'lower')[0]) <= 1e-4 + 1e-12, 'replacement text: quality part 5 values stay in their bands')
ok(abs(math.sqrt(0.04 + 0.0625) - 0.3202) < 5e-5 and abs(1 / 0.04 - 25) < 1e-9 and abs(1 / 0.0625 - 16) < 1e-9, 'replacement text: etf part 1 add-var')
ok(abs((m0 + ybar) / 2 + 0.56) < 1e-12 and abs(25 / 41 * m0 + 16 / 41 * ybar + 0.5029) < 5e-5, 'replacement text: etf part 2')
ok(abs(1.5 / math.sqrt(20) - 0.3354) < 5e-5 and abs(Phi(-0.4971 / 0.3354) - 0.0692) < 5e-5 and abs(Phi(-0.4971 / 0.3700) - 0.0896) < 5e-5, 'replacement text: etf parts 3 and 4 plug-in')
ok(abs(0.5 / (0.5 + 0.4583) - 0.5218) < 5e-5 and abs(0.25 + 0.21 - 0.46) < 1e-12, 'replacement text: quality part 3 sd-ratio')
ok(abs(0.5435 * 1.1 - 0.5978) < 5e-5 and abs(0.9 - 0.5978 - 0.3022) < 5e-5 and abs(1 - 0.5435 - 0.4565) < 1e-12, 'replacement text: quality part 4 kept-b')
ok(abs(1 - 0.8805 - 0.1195) < 1e-12, 'replacement text: quality part 5 lower')
# Replacement-text checks of p-dealer-enquiries (review findings 6 to 9) removed: the problem was re-authored.

print(f'{checks} checks, {len(findings)} failed or claimed')
for f in findings:
    print('FINDING', f)
sys.exit(0)
