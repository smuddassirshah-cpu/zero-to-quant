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
C = 'p-circuit-breaker'
a0, r0, trips, weeks, cur, prop, u = 3, 0.5, 41, 8, 5.2, 6.1, 0.40
a1, r1 = a0 + trips, r0 + weeks
ok((a1, r1) == (44, 8.5), 'circuit: posterior Gamma(44, rate 8.5)')
# route 2: posterior mean on a grid from prior density times a Poisson likelihood for 8 weekly counts summing to 41
counts = [6, 4, 7, 5, 3, 6, 5, 5]
ok(sum(counts) == trips and len(counts) == weeks, 'circuit: planted weeks sum to 41')
g = np.linspace(0.01, 15, 150000)
lp = stats.gamma.logpdf(g, a0, scale=1 / r0) + sum(stats.poisson.logpmf(c, g) for c in counts)
w = np.exp(lp - lp.max())
gm = float((g * w).sum() / w.sum())
check_key(C, 0, a1 / r1, gm)
check_wrong(C, 0, 'mle', trips / weeks)
check_wrong(C, 0, 'prior', a0 / r0)
check_wrong(C, 0, 'no-rate', a1 / r0)
ok(abs(a1 / r1 - trips / weeks) < abs(a1 / r1 - a0 / r0), 'circuit part 1 explain: nearer 5.125 than 6')
lr = (a1 - 1) * math.log(prop / cur) - r1 * (prop - cur)
lr2 = stats.gamma.logpdf(prop, a1, scale=1 / r1) - stats.gamma.logpdf(cur, a1, scale=1 / r1)
lr3 = float(np.interp(prop, g, lp) - np.interp(cur, g, lp))          # from the unnormalised grid posterior
check_key(C, 1, lr, lr2, lr3)
ok(abs(43 * math.log(prop / cur) - 6.8641) < 5e-5 and abs(r1 * 0.9 - 7.65) < 1e-9, 'circuit part 2: 6.8641 and 7.65')
check_wrong(C, 1, 'power-44', 44 * math.log(prop / cur) - r1 * (prop - cur))
check_wrong(C, 1, 'as-scale', 43 * math.log(prop / cur) - (prop - cur) / r1)
check_wrong(C, 1, 'reversed', -lr)
thr = math.exp(lr)
check_key(C, 2, thr, stats.gamma.pdf(prop, a1, scale=1 / r1) / stats.gamma.pdf(cur, a1, scale=1 / r1), fed=math.exp(-0.7859))
check_wrong(C, 2, 'reject-chance', 1 - thr)
check_wrong(C, 2, 'inverted', math.exp(0.7859))
check_key(C, 3, prop if u < thr else cur, prop if math.log(u) < lr else cur)
check_wrong(C, 3, 'stayed', cur)
ok(0.50 > thr, 'circuit part 4 explain: u = 0.50 would be rejected')
check_bands(C)

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
D = 'p-dealer-enquiries'
a, b, k_tr, n_enq = 7, 13, 17, 40
a2, b2 = a + k_tr, b + n_enq - k_tr
ok((a2, b2) == (24, 36), 'dealer: posterior Beta(24, 36)')
gp = np.linspace(1e-6, 1 - 1e-6, 400001)
lw = stats.beta.logpdf(gp, a, b) + stats.binom.logpmf(k_tr, n_enq, gp)
ww = np.exp(lw - lw.max())
pm = float((gp * ww).sum() / ww.sum())
pv = float(((gp - pm) ** 2 * ww).sum() / ww.sum())
check_key(D, 0, a2 / (a2 + b2), pm)
ok(abs(40 / 60 * 0.425 + 20 / 60 * 0.35 - 0.4) < 1e-12, 'dealer part 1 explain: the blend of 0.425 and 0.35 is 0.4')
check_wrong(D, 0, 'raw', k_tr / n_enq)
check_wrong(D, 0, 'population', a / (a + b))
check_wrong(D, 0, 'a-only', (a + k_tr) / (a + n_enq))
bsd = math.sqrt(a2 * b2 / ((a2 + b2) ** 2 * (a2 + b2 + 1)))
check_key(D, 1, bsd, math.sqrt(pv), stats.beta(a2, b2).std())
ok(a2 * b2 == 864 and (a2 + b2) ** 2 * (a2 + b2 + 1) == 219600 and abs(864 / 219600 - 0.003934) < 5e-7, 'dealer part 2: 864/219,600 = 0.003934')
check_wrong(D, 1, 'binomial', math.sqrt(0.4 * 0.6 / 40))
check_wrong(D, 1, 'variance', bsd ** 2)
check_wrong(D, 1, 'no-plus-one', math.sqrt(a2 * b2 / (a2 + b2) ** 3))
# the chain numbers are read from the questions, so a re-keyed part is recomputed, not refused
q3 = item(D)['parts'][2]['question']
q4 = item(D)['parts'][3]['question']
phi = float(re.search(r'\\phi = (0\.\d+)', q3).group(1))
n_chain = int(re.search(r'each keep ([\d,]+) draws', q3).group(1).replace(',', ''))
n_all = int(re.search(r'all ([\d,]+) draws', q3).group(1).replace(',', ''))
chain_mean = float(re.search(r'chain mean is (0\.\d+)', q4).group(1))
m_chain = 4
ok(n_all == m_chain * n_chain, 'dealer part 3: four chains make the stated total')
ess1 = n_chain * (1 - phi) / (1 + phi)
ok(abs(ess1 - round(ess1)) < 1e-9, f'dealer part 3: effective draws a chain are whole ({ess1})')
shown(D, 2, 'feedback', f'= {round(ess1)}$ draws')
mcse = 0.0627 / math.sqrt(m_chain * ess1)
# route 2: exact finite-n variance of the mean of an AR(1) chain with unit variance, four independent chains
infl = (1 + phi) / (1 - phi) - 2 * phi * (1 - phi ** n_chain) / (n_chain * (1 - phi) ** 2)
mcse_exact = bsd * math.sqrt(infl / (n_chain * m_chain))
# route 3: seeded simulation of 3,000 runs of four chains
rng = np.random.default_rng(20261116)
runs = 3000
z = rng.standard_normal(runs * m_chain)
acc = np.zeros(runs * m_chain)
for _ in range(n_chain):
    acc += z
    z = phi * z + math.sqrt(1 - phi ** 2) * rng.standard_normal(runs * m_chain)
means = (acc / n_chain).reshape(runs, m_chain).mean(axis=1) * bsd
check_key(D, 2, mcse, mcse_exact)
ok(abs(means.std(ddof=1) - mcse) < 5 * mcse / math.sqrt(2 * runs), f'dealer part 3: simulated sd of the pooled mean {means.std(ddof=1):.6f} against {mcse:.6f}')
se_ind = 0.0627 / math.sqrt(n_all)
se_one = 0.0627 / math.sqrt(ess1)
check_wrong(D, 2, 'independent', se_ind)
check_wrong(D, 2, 'one-chain', se_one)
check_wrong(D, 2, 'no-plus-phi', 0.0627 / math.sqrt(n_all * (1 - phi)))
gap = chain_mean - 0.4
k3 = key(D, 2)[0]
check_key(D, 3, gap / k3, gap / mcse, gap / mcse_exact)
k4 = key(D, 3)[0]
shown(D, 3, 'question', f'{k3:.5f}')
shown(D, 4, 'question', f'{k4:.2f}')
ok(round(chain_mean, 2) == 0.40, 'dealer part 5: the chain mean and 0.4 agree to two places, as option 2 says')
# each slip with the exact error and with the error as its own line prints it (5 places)
check_wrong(D, 3, 'independent', gap / se_ind, typed=round(gap / round(se_ind, 5), 2))
check_wrong(D, 3, 'posterior-sd', gap / 0.0627)
check_wrong(D, 3, 'one-chain', gap / se_one, typed=round(gap / round(se_one, 5), 2))
once = 1 / (2 * (1 - Phi(k4)))
said = int(re.search(r'once in ([\d,]+) runs', item(D)['parts'][4]['explain']['text']).group(1).replace(',', ''))
ok(abs(once - said) < 0.03 * once, f'dealer part 5 explain: once in about {once:.0f} runs, printed {said}')
opts = item(D)['parts'][4]['widget']['options']
ok(sum(1 for o in opts if o.get('correct')) == 1 and opts[0]['id'] == 'fault', 'dealer part 5: one keyed option, the fault')
check_bands(D)

# ---------------------------------------------------------------- findings of the reading, tested on the text
blob = json.dumps(SET, ensure_ascii=False)
ok(not (phi == 0.6 and n_chain == 2000),
   'dealer part 3 reuses lesson 17: phi = 0.6 with the working "x 0.4/1.6" is its quiz item q17-ess, and 2,000 draws is its screen 4 (review finding 8)')
ok('So the code has a fault' not in blob, 'dealer part 5 explain: "So the code has a fault" is stronger than a 1 in 750 event allows; lesson 17 names non-convergence first (review finding 9)')
ok('You kept $B$ of the gap, not $1 - B$.' not in blob, 'quality part 4 kept-b is word for word l18 screen 4 byKey.b and r4-shrink byKey.keepb (review finding 5)')
ok('Where is the chain after this step' not in blob.replace('where', 'Where'),
   'circuit part 4 asks the question of q16-step, r4-step and e-metropolis-log, with their outcome (review finding 4, re-author)')

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
ok(abs(24 / 47 - 0.5106) < 5e-5 and 17 / 40 == 0.425 and 7 / 20 == 0.35 and 40 - 17 == 23 and abs(2 / 3 * 0.425 + 1 / 3 * 0.35 - 0.4) < 1e-12, 'replacement text: dealer part 1')
ok(abs(math.sqrt(0.24 / 40) - 0.0775) < 5e-5 and abs(0.24 / 61 - 864 / 219600) < 1e-12 and abs(math.sqrt(0.003934) - 0.0627) < 5e-5 and abs(864 / 219600 - 0.0039) < 5e-5, 'replacement text: dealer part 2')
# the re-key of dealer parts 3 to 5: phi = 0.7, four chains of 2,550, pooled mean 0.4046
rp, rn, rmean = 0.7, 2550, 0.4046
re1 = rn * (1 - rp) / (1 + rp)
ok(abs(re1 - 450) < 1e-9 and abs(4 * re1 - 1800) < 1e-9 and 4 * rn == 10200 and abs(10200 * 0.3 - 3060) < 1e-9, 'replacement text: 450 a chain, 1,800 in all, 3,060 without the 1.7')
rk3 = 0.0627 / math.sqrt(1800)
rinfl = (1 + rp) / (1 - rp) - 2 * rp * (1 - rp ** rn) / (rn * (1 - rp) ** 2)
rk3x = bsd * math.sqrt(rinfl / (4 * rn))
ok(abs(rk3 - 0.00148) <= 1e-5 and abs(rk3x - 0.00148) <= 1e-5, f'replacement key part 3: 0.00148 against {rk3:.6f} and exact {rk3x:.6f}')
rw3 = {'independent': (0.0627 / math.sqrt(10200), 0.00062), 'one-chain': (0.0627 / math.sqrt(450), 0.00296), 'no-plus-phi': (0.0627 / math.sqrt(3060), 0.00113)}
for nm, (val, printed) in rw3.items():
    ok(abs(val - printed) <= 1e-5, f'replacement wrong part 3 {nm}: {printed} against {val:.6f}')
vals3 = [0.00148] + [v for _, v in rw3.values()]
ok(all(abs(x - yv) > 2e-5 for i, x in enumerate(vals3) for yv in vals3[i + 1:]), 'replacement part 3: bands apart')
rgap = rmean - 0.4
ok(abs(rgap / 0.00148 - 3.11) <= 0.01 and abs(rgap / rk3 - 3.11) <= 0.01 and abs(rgap / rk3x - 3.11) <= 0.01, 'replacement key part 4: 3.11 by the printed, the unrounded and the exact error')
rw4 = {'independent': (rw3['independent'], 7.41), 'one-chain': (rw3['one-chain'], 1.56)}
for nm, ((val, printed), v4) in rw4.items():
    ok(abs(rgap / val - v4) <= 0.01 and abs(round(rgap / printed, 2) - v4) <= 0.01 + 1e-9, f'replacement wrong part 4 {nm}: {v4} against {rgap / val:.4f} and {rgap / printed:.4f}')
ok(abs(rgap / 0.0627 - 0.07) <= 0.01, 'replacement wrong part 4 posterior-sd: 0.07')
ok(round(rmean, 2) == 0.40 and abs(rgap - 0.0046) < 1e-12, 'replacement text: 0.4046 and 0.4 agree to two places; the gap is 0.0046')
ok(abs(1 / (2 * (1 - Phi(3.11))) - 530) < 16 and abs(1 / (2 * (1 - Phi(3))) - 370) < 1, 'replacement text: once in about 530 runs at 3.11, once in 370 at 3')

print(f'{checks} checks, {len(findings)} failed or claimed')
for f in findings:
    print('FINDING', f)
sys.exit(0)
