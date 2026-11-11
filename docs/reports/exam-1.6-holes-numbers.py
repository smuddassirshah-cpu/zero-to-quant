"""topic-1.6, testing level 4 items (Option B, skills ht-theory and ht-likelihood): every new key computed twice.

Run: <scratchpad>/venv/bin/python docs/reports/exam-1.6-holes-numbers.py   (exit 0 when all pass; needs NumPy and SciPy)
Route 1 is the closed form the item prints; route 2 is independent: SciPy's distributions and optimiser, a numerical
derivative, or a seeded simulation. The script then reads app/content/exams/topic-1.6.json and checks every key and
wrong value (the named slip, outside the key's band, with a feedback line) and that each explanation states its key.
"""
import json, math, os, sys
import numpy as np
from scipy import stats, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import _numbers  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', 'app', 'content', 'exams', 'topic-1.6.json')
doc = json.load(open(EXAM, encoding='utf8'))
items = {i['id']: i for i in doc['items']}
fails, n = [], [0]
rng = np.random.default_rng(20261111)


def check(ok, label):
    n[0] += 1
    print(('ok  ' if ok else 'BAD ') + label)
    if not ok:
        fails.append(label)


def band(t):
    return t.get('abs', 0) if isinstance(t, dict) else t


def cell_or_widget(where, w, byKey, key, wrongs, explain=None):
    a, t = w['answer'], band(w['tol'])
    check(abs(a - key) <= max(t, 1e-9), f'{where} key {a} = computed {key:.6g}')
    got = {x['id']: x for x in w.get('wrong', [])}
    check(set(got) == set(wrongs), f'{where} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        x = got[k]
        check(abs(x['value'] - v) <= band(x['tol']) + 1e-9, f'{where} wrong {k} {x["value"]} = slip {v:.6g}')
        check(abs(x['value'] - a) > t + band(x['tol']), f'{where} wrong {k} outside the key band')
        check(k in byKey, f'{where} wrong {k} has a byKey line')
    if explain is not None:
        check(any(abs(x - a) <= max(t, 1e-9) for x in _numbers(explain)), f'{where} explanation states the key')


# s-uniform-moments: theta^2 / 3 = 0.12
m2, xbar = 0.12, 0.02
r1 = math.sqrt(3 * m2)
U = stats.uniform(loc=-r1, scale=2 * r1)
r2 = optimize.brentq(lambda th: stats.uniform(loc=-th, scale=2 * th).moment(2) - m2, 0.01, 5)
check(abs(r1 - 0.6) < 1e-12 and abs(r2 - 0.6) < 1e-9 and abs(U.mean()) < 1e-12, f'uniform-moments 0.6 closed form and root-finding on SciPy moments ({r2:.6f})')
central = math.sqrt(3 * (m2 - xbar ** 2))
check(abs(central - 0.6) <= 0.005, f'uniform-moments the central-moment route {central:.4f} is inside the band')
sim = rng.uniform(-0.6, 0.6, size=(4000, 50))
check(abs(np.sqrt(3 * (sim ** 2).mean(axis=1)).mean() - 0.6) < 0.01, 'uniform-moments simulation: the estimator centres on 0.6')
it = items['s-uniform-moments']
cell_or_widget('s-uniform-moments', it['widget'], it['feedback']['byKey'], r1,
               {'no-root': 3 * m2, 'no-three': math.sqrt(m2), 'two-mean': 2 * xbar}, it['explain']['text'])

# s-chi-order-mix: goodness of fit to 50/30/20 of 200
O = np.array([86, 74, 40]); E = 200 * np.array([0.5, 0.3, 0.2])
x2 = float(((O - E) ** 2 / E).sum())
x2b, pb = stats.chisquare(O, E)
check(abs(x2 - 5.226667) < 1e-5 and abs(x2b - x2) < 1e-9, f'chi-order-mix X^2 {x2:.4f} by hand and scipy.chisquare')
p1, p2 = math.exp(-x2 / 2), float(stats.chi2.sf(x2, 2))
check(abs(p1 - p2) < 1e-12 and abs(p2 - pb) < 1e-12 and round(p1, 3) == 0.073, f'chi-order-mix p {p1:.4f}: e^(-x/2) and chi2.sf agree')
check(abs(stats.chi2.ppf(0.95, 1) - 3.841) < 5e-4 and abs(stats.chi2.ppf(0.95, 2) - 5.991) < 5e-4 and abs(stats.chi2.ppf(0.95, 3) - 7.815) < 5e-4,
      'chi-order-mix cut-offs 3.841, 5.991, 7.815')
check(3.841 < x2 < 5.991 and E.min() == 40, 'chi-order-mix 5.23 between the 1 and 2 df cut-offs; smallest E is 40')
part = items['s-chi-order-mix']['parts'][0]
row = part['widget']['rows'][0]
bk = part['feedback']['byKey']
cell_or_widget('s-chi-order-mix X^2', row[0], bk, x2, {'over-observed': float(((O - E) ** 2 / O).sum()), 'no-divide': float(((O - E) ** 2).sum())})
cell_or_widget('s-chi-order-mix df', row[1], bk, 2, {'cells': 3})
check(any(abs(v - 5.23) < 1e-9 for v in _numbers(part['explain']['text'])), 's-chi-order-mix explanation states 5.23')
check(abs(1.96 + 3.27 - 5.23) < 1e-9 and round(196 / 60, 2) == 3.27, 'chi-order-mix printed sum 1.96 + 3.27 = 5.23')

# s-pool-rates: two Poisson counts, one shared rate
a, b = 90, 60
G = 2 * (a * math.log(a / 75) + b * math.log(b / 75))
ll = lambda lam_a, lam_b: stats.poisson.logpmf(a, lam_a) + stats.poisson.logpmf(b, lam_b)
lam0 = optimize.minimize_scalar(lambda l: -ll(l, l), bounds=(1, 200), method='bounded').x
G2 = 2 * (ll(a, b) - ll(lam0, lam0))
check(abs(G - 6.04061) < 1e-4 and abs(G2 - G) < 1e-6 and abs(lam0 - 75) < 1e-4, f'pool-rates -2 ln Lambda {G:.4f}: closed form and SciPy likelihoods ({G2:.4f})')
check(G > 3.841 and stats.chi2.sf(G, 1) < 0.05, f'pool-rates rejects at 5% (p {stats.chi2.sf(G, 1):.4f})')
check(abs(90 * math.log(1.2) - 16.41) < 0.005 and abs(60 * math.log(0.8) + 13.39) < 0.005, 'pool-rates printed terms 16.41 and 13.39')
row = items['s-pool-rates']['widget']['rows'][0]
bk = items['s-pool-rates']['feedback']['byKey']
cell_or_widget('s-pool-rates stat', row[0], bk, G, {'no-two': G / 2, 'pearson': 2 * 15 ** 2 / 75, 'sign': -G})
cell_or_widget('s-pool-rates df', row[1], bk, 1, {'model-size': 2})
check(any(abs(v - 6.04) < 1e-9 for v in _numbers(items['s-pool-rates']['explain']['text'])), 's-pool-rates explanation states 6.04')
# simulation of the chi^2_1 limit: under one shared rate the statistic exceeds 3.841 about 5% of the time
sa, sb = rng.poisson(75, 200000), rng.poisson(75, 200000)
pool = (sa + sb) / 2
with np.errstate(divide='ignore', invalid='ignore'):
    term = lambda o: np.where(o > 0, o * np.log(o / pool), 0.0)
    Gs = 2 * (term(sa) + term(sb))
check(abs((Gs > 3.841).mean() - 0.05) < 0.005, f'pool-rates simulated size {(Gs > 3.841).mean():.4f} near 0.05 (one degree of freedom)')

# s-pareto-losses
nloss, S = 80, 32.0
ahat = nloss / S
loglik = lambda al: nloss * math.log(al) - (al + 1) * S
a2 = optimize.minimize_scalar(lambda al: -loglik(al), bounds=(0.1, 20), method='bounded').x
check(ahat == 2.5 and abs(a2 - 2.5) < 1e-5, f'pareto alpha-hat 2.5: n / sum ln x and numeric maximisation ({a2:.6f})')
h = 1e-4
lnf = lambda al, xx: math.log(al) - (al + 1) * math.log(xx)
d2 = (lnf(2.5 + h, 3.0) - 2 * lnf(2.5, 3.0) + lnf(2.5 - h, 3.0)) / h ** 2
check(abs(-d2 - 1 / 2.5 ** 2) < 1e-4, f'pareto I(alpha) = 1/alpha^2 by numerical second derivative ({-d2:.6f})')
crb = 2.5 ** 2 / nloss
sims = stats.pareto(b=2.5).rvs(size=(20000, nloss), random_state=7)
ah = nloss / np.log(sims).sum(axis=1)
check(abs(crb - 0.078125) < 1e-15 and abs(ah.var() / crb - 1) < 0.08, f'pareto bound 0.078125; simulated var of the MLE {ah.var():.4f} near it')
check(abs(np.log(sims).mean() - 1 / 2.5) < 0.002, 'pareto ln X is exponential with mean 1/alpha (simulation)')
parts = items['s-pareto-losses']['parts']
check([o['id'] for o in parts[0]['widget']['options'] if o.get('correct')] == ['a'] and parts[0]['widget']['options'][0]['text'] == '$\\sum \\ln x_i$', 'pareto sufficient statistic key')
# factorisation check: two samples with one sum of logs give proportional likelihoods in alpha
s1 = np.exp(rng.exponential(0.4, 80)); s2 = np.exp(rng.exponential(0.4, 80)); s2 = np.exp(np.log(s2) * np.log(s1).sum() / np.log(s2).sum())
r = [nloss * math.log(al) - (al + 1) * np.log(s1).sum() - (nloss * math.log(al) - (al + 1) * np.log(s2).sum()) for al in (1.0, 2.5, 4.0)]
check(max(r) - min(r) < 1e-8, 'pareto equal sum ln x gives a likelihood ratio free of alpha')
cell_or_widget('s-pareto-losses p2', parts[1]['widget'], parts[1]['feedback']['byKey'], ahat,
               {'upside-down': S / nloss, 'exponent': ahat - 1}, parts[1]['explain']['text'])
cell_or_widget('s-pareto-losses p3', parts[2]['widget'], parts[2]['feedback']['byKey'], crb,
               {'sd': math.sqrt(crb), 'info': nloss / 2.5 ** 2, 'alpha-not-squared': 2.5 / nloss}, parts[2]['explain']['text'])
check(round(math.sqrt(crb), 2) == 0.28, 'pareto standard error about 0.28')

# exam shape
cnt = {d: sum(1 for i in doc['items'] if i['difficulty'] == d) for d in (2, 3, 4, 5)}
N = len(doc['items'])
for d, s in {2: .2, 3: .5, 4: .2, 5: .1}.items():
    check(abs(cnt[d] / N - s) <= 0.1 + 1e-9, f'ramp d{d} {cnt[d]}/{N}')
check(N <= 30 and 's-summary-dw' not in items, f'{N} items, s-summary-dw replaced')
used = {s for i in doc['items'] for s in i.get('skills', [])}
check(set(doc['skills']) <= used, 'every exam skill covered')
check(sum('rg-diagnostics' in i.get('skills', []) for i in doc['items']) >= 2, 'rg-diagnostics still examined twice')
print(f'{n[0] - len(fails)} of {n[0]} checks passed')
sys.exit(1 if fails else 0)
