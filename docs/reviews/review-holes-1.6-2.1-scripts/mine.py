"""Second read, holes 1.6 and 2.1: the reader's own keys and slips for every typed part of testing problems-4,
stat-learning problems-4 and the nine new exam items, worked from the items' text (no import from the authors' scripts),
each by a library or brute-force route where one exists, then compared with the content files: the answer and every
`wrong` value by id. Also the theory claims the items lean on.
   <venv>/bin/python docs/reviews/review-holes-1.6-2.1-scripts/mine.py      (from the repo root)"""
import itertools
import json
import math

import numpy as np
from scipy import integrate, optimize, stats

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def near(a, b, tol=1e-9):
    return abs(a - b) <= tol


def load(path):
    return {it['id']: it for it in json.load(open(path))['items']}


def cells(widget):
    return [c for row in widget['rows'] for c in row if isinstance(c, dict) and c.get('edit')]


def check(spec, where, key, wrongs, show_tol=None):
    """spec: a numeric widget or a table cell. key: mine. wrongs: {id: my value}."""
    tol = spec['tol']['abs']
    ok(near(spec['answer'], key, max(tol, 1e-9)), f'{where}: answer {spec["answer"]} against mine {key}')
    ids = {w['id'] for w in spec.get('wrong', [])}
    ok(ids == set(wrongs), f'{where}: wrong ids {sorted(ids)} against mine {sorted(wrongs)}')
    for w in spec.get('wrong', []):
        if w['id'] in wrongs:
            wt = w.get('tol', {}).get('abs', tol)
            ok(near(w['value'], wrongs[w['id']], max(wt, 1e-9)), f'{where}: wrong {w["id"]} {w["value"]} against mine {wrongs[w["id"]]}')
            ok(abs(w['value'] - spec['answer']) > tol + wt or (tol == 0 and w['value'] != spec['answer']), f'{where}: wrong {w["id"]} inside the answer band')


# ---------------------------------------------------------------- testing problems-4
T = load('app/content/courses/testing/problems-4.json')

# p-disk-failures: 40 exponential gaps, total 100 days
n, tot = 40, 100.0
lam = n / tot
ok(near(stats.expon(scale=1 / lam).mean(), tot / n), 'disk: the moment equation')
P = T['p-disk-failures']['parts']
check(P[0]['widget'], 'disk 1', lam, {'mean-gap': tot / n, 'over-total': 1 / tot})
h = 1e-4
info1 = -(math.log(lam + h) - 2 * math.log(lam) + math.log(lam - h)) / h ** 2      # -d2/dlam2 of ln(lam) - lam x
ok(near(info1, 1 / lam ** 2, 1e-5), 'disk: I(lambda) = 1/lambda^2')
check(P[1]['widget'], 'disk 2', n / lam ** 2, {'one-gap': 1 / lam ** 2, 'no-square': n / lam, 'carried': n / 2.5 ** 2})
check(P[2]['widget'], 'disk 3', 1 / math.sqrt(250), {'variance': 1 / 250, 'root-of-info': math.sqrt(250), 'carried': 1 / math.sqrt(6.4)})
check(P[3]['widget'], 'disk 4', 1 / 250, {'standard-error': 1 / math.sqrt(250), 'one-gap': lam ** 2, 'information': 250})
# (n - 1)/sum x: unbiased with variance lam^2/(n - 2), from the Gamma(n, lam) law of the sum
g = stats.gamma(n, scale=1 / lam)
m1 = integrate.quad(lambda s: (n - 1) / s * g.pdf(s), 0, np.inf)[0]
m2 = integrate.quad(lambda s: ((n - 1) / s) ** 2 * g.pdf(s), 0, np.inf)[0]
ok(near(m1, lam, 1e-7), 'disk: (n - 1)/sum x is unbiased')
ok(near(m2 - m1 ** 2, lam ** 2 / (n - 2), 1e-7), 'disk: its variance is lambda^2/(n - 2)')
var5 = lam ** 2 / (n - 2)
check(P[4]['widget'], 'disk 5', 0.004 / var5, {'inverted': var5 / 0.004, 'n-minus-one': 0.004 / (lam ** 2 / (n - 1)), 'carried': 0.0632 / var5})

# p-website-signups: 12 Poisson hours, T = 54
P = T['p-website-signups']['parts']
ok([o['id'] for o in P[0]['widget']['options'] if o.get('correct')] == ['total'], 'signups 1: the total is keyed')
# E[X1 | T]: given T the counts are multinomial with equal shares
ok(near(stats.binom(54, 1 / 12).mean(), 4.5), 'signups: E[X1 | T = 54] by the binomial law of X1 given T')
check(P[1]['widget'], 'signups 2', 54 / 12, {'total': 54, 'n-minus-one': 54 / 11})
check(P[2]['widget'], 'signups 3', stats.poisson(12 * 4.5).var() / 144, {'one-hour': 4.5, 'n-squared': 4.5 / 144, 'sd': math.sqrt(0.375)})
check(P[3]['widget'], 'signups 4', 0.375 / 4.5, {'inverted': 12, 'improved': 1})
need = next(k for k in range(1, 1000) if math.sqrt(4.5 / k) <= 0.3 + 1e-12)
check(P[4]['widget'], 'signups 5', need, {'no-square': 4.5 / 0.3, 'root-only': math.sqrt(4.5) / 0.3, 'carried': math.ceil(0.375 / 0.09)})

# p-bakery-loaves: 2 by 3 table
P = T['p-bakery-loaves']['parts']
tab = np.array([[50, 40, 30], [20, 40, 20]])
x2, pval, dof, exp = stats.chi2_contingency(tab, correction=False)
ok(exp.round(9).tolist() == [[42, 48, 30], [28, 32, 20]], 'bakery: the six expected counts')
check(P[0]['widget'], 'bakery 1', exp[1, 0], {'averaged': (80 + 70) / 2, 'weekday-cell': exp[0, 0], 'chance': 0.4 * 0.35})
check(P[1]['widget'], 'bakery 2', x2, {'no-divide': ((tab - exp) ** 2).sum(), 'over-observed': ((tab - exp) ** 2 / tab).sum(), 'weekdays-only': ((tab - exp) ** 2 / exp)[0].sum()})
ok(near(x2, 50 / 7), 'bakery: X^2 is 50/7')
check(P[2]['widget'], 'bakery 3', dof, {'cells-minus-one': 5, 'margins': 3})
ok(near(stats.chi2(2).sf(7.143), math.exp(-7.143 / 2), 1e-12), 'bakery: the chi-squared 2 tail is exp(-x/2)')
check(P[3]['widget'], 'bakery 4', stats.chi2(2).sf(7.143), {'no-half': math.exp(-7.143), 'lower-tail': stats.chi2(2).cdf(7.143), 'carried': stats.chi2(2).sf(2.857)})
gstat = stats.chi2_contingency(tab, correction=False, lambda_='log-likelihood')[0]
ok(near(gstat, 7.242, 5e-4), f'bakery 5: G = {gstat}')
ok(gstat > stats.chi2(2).ppf(0.95) and x2 > stats.chi2(2).ppf(0.95) and gstat < stats.chi2(5).ppf(0.95), 'bakery 5: both pass 5.991; 7.242 is below the 5 df cut-off')
ok(near(stats.chi2(5).ppf(0.95), 11.07, 5e-3), 'bakery 5: 11.07')
ok([o['id'] for o in P[4]['widget']['options'] if o.get('correct')] == ['both-reject'], 'bakery 5: key')

# p-night-admissions: 10 Poisson nights, total 38, null 3
P = T['p-night-admissions']['parts']
lr = 2 * (stats.poisson.logpmf(38, 38) - stats.poisson.logpmf(38, 30))
check(P[0]['widget'], 'nights 1', 3.8, {'total': 38, 'excess': 0.8})
check(P[1]['widget'], 'nights 2', lr, {'not-doubled': lr / 2, 'no-mean-term': 2 * 38 * math.log(3.8 / 3), 'no-n': 2 * (38 * math.log(3.8 / 3) - 0.8)})
se = math.sqrt(3.8 / 10)
check(P[2]['widget'], 'nights 3', se, {'variance': 0.38, 'information-flipped': 1 / math.sqrt(38), 'null-value': math.sqrt(0.3)})
check(P[3]['widget'], 'nights 4', 0.8 / 0.6164, {'squared': (0.8 / 0.6164) ** 2, 'null-se': 0.8 / math.sqrt(0.3), 'carried': 0.8 / 0.38})
first = next(k for k in range(1, 200) if 2 * (stats.poisson.logpmf(round(3.8 * k * 10) / 10, 3.8 * k) if False else k * (3.8 * math.log(3.8 / 3) - 0.8)) > 3.841)
check(P[4]['widget'], 'nights 5', first, {'rounded-down': first - 1, 'wald': math.ceil(3.841 / (1.684 / 10)), 'carried': math.ceil(3.841 / 0.0983)})

# ---------------------------------------------------------------- stat-learning problems-4
S = load('app/content/courses/stat-learning/problems-4.json')

P = S['p-spam-filter']['parts']
w, b = np.array([1.5, -2.0]), 0.5
nw = float(np.linalg.norm(w))
check(P[0]['widget'], 'spam 1', 1 / nw, {'gave-norm': nw, 'street-width': 2 / nw, 'squared-norm': 1 / nw ** 2})
xx = np.array([0.2, 0.3])
f = float(w @ xx + b)
foot = xx - f * w / (w @ w)
check(P[1]['widget'], 'spam 2', float(np.linalg.norm(xx - foot)), {'decision-value': f, 'squared-norm': f / nw ** 2, 'carried': f * 2.5})
ok(0 < f < 1 and [o['id'] for o in P[2]['widget']['options'] if o.get('correct')] == ['inside'], 'spam 3: inside the street on the positive side')
tt = lambda hit, base, m: (hit - base) / math.sqrt(base * (1 - base) / m)
check(P[4]['widget'], 'spam 5', tt(0.93, 0.9, 500), {'own-rate': 0.03 / math.sqrt(0.93 * 0.07 / 500), 'no-root': 0.03 / math.sqrt(0.09), 'coin': tt(0.93, 0.5, 500)})

P = S['p-order-sizes']['parts']
pts = np.array([2, 4, 6, 18, 22, 26.0])


def step(c):
    lab = np.array([int(abs(p - c[1]) < abs(p - c[0])) for p in pts])
    return [pts[lab == 0].mean(), pts[lab == 1].mean()], lab


c1, lab1 = step([3, 8])
check(P[0]['widget'], 'orders 1', c1[1], {'all-orders': pts.mean(), 'kept-centre': (8 + pts[lab1 == 1].sum()) / (1 + (lab1 == 1).sum()), 'six-misassigned': pts[3:].mean()})
c, lab = c1, lab1
for _ in range(10):
    c, lab = step(c)
ok(c == [4, 22], f'orders: settles at {c}')
best = min(sum(((pts[list(g)] - pts[list(g)].mean()) ** 2).sum() for g in (grp, [i for i in range(6) if i not in grp]))
           for r in range(1, 6) for grp in itertools.combinations(range(6), r))
inert = sum((p - c[l]) ** 2 for p, l in zip(pts, lab))
ok(near(best, inert), 'orders: the settled split is the best split of all')
check(P[1]['widget'], 'orders 2', c[1], {'no-reassign': 18, 'all-orders': 13})
check(P[2]['widget'], 'orders 3', inert, {'unsquared': sum(abs(p - c[l]) for p, l in zip(pts, lab)), 'averaged': inert / 6, 'carried': sum((p - [3, 18][l]) ** 2 for p, l in zip(pts, lab))})
knot = (4 + 22) / 2
fs = lambda t, k=knot, sgn=-1: 1 + 2.5 * t + sgn * 1.8 * max(0, t - k)
check(P[3]['widget'], 'orders 4', fs(20), {'no-hinge': 51, 'sign': fs(20, sgn=1), 'knot-at-centre': fs(20, k=4), 'carried': fs(20, k=10.5)})
check(P[4]['widget'], 'orders 5', fs(20) - fs(10), {'summed-halves': fs(20) - 2 * fs(10), 'negative-hinge': fs(20) - (26 - 1.8 * (10 - 13)), 'carried': 51 - fs(10)})

P = S['p-one-unit']['parts']
net = lambda w1, x=8, b1=-1, v=2, d=1: v * max(0, w1 * x + b1) + d
L = lambda w1: 0.5 * (net(w1) - 10) ** 2
check(P[0]['widget'], 'unit 1', net(0.5), {'no-hidden-bias': 2 * 4 + 1, 'no-output-bias': 6})
check(P[1]['widget'], 'unit 2', L(0.5), {'no-half': 9, 'unsquared': -1.5, 'carried': 0.5})
grad = (L(0.5 + 1e-6) - L(0.5 - 1e-6)) / 2e-6
check(P[2]['widget'], 'unit 3', round(grad, 5), {'slope-for-v': -9, 'dropped-x': -6, 'sign': 48, 'carried': -16})
check(P[3]['widget'], 'unit 4', 0.5 - 0.01 * grad, {'uphill': 0.5 + 0.01 * grad, 'no-rate': 0.5 - grad, 'carried': 0.5 + 0.09}, )
check(P[4]['widget'], 'unit 5', optimize.brentq(lambda t: 0.98 * t - 1, 0, 5), {'old-knot': 2, 'sign': -1 / 0.98, 'carried': 1 / 0.59})
ok(L(0.98) > L(0.5), f'unit 4: the step to 0.98 raises the loss (4.5 to 10.95), which is what finding 10 reports; if this fails the content was fixed')

P = S['p-renewals']['parts']
check(P[0]['widget'], 'renewals 1', np.zeros((16, 6)).size + 16 + 16 + 1, {'no-biases': 112, 'units': 23})
check(P[2]['widget'], 'renewals 3', tt(0.74, 0.7, 500), {'own-rate': 0.04 / math.sqrt(0.74 * 0.26 / 500), 'no-root': 0.04 / math.sqrt(0.21), 'coin': tt(0.74, 0.5, 500)})
rows = next(k for k in range(1, 5000) if tt(0.74, 0.7, k) >= 3)
own = next(k for k in range(1, 5000) if 0.04 / math.sqrt(0.74 * 0.26 / k) >= 3)
check(P[3]['widget'], 'renewals 4', rows, {'rounded-down': rows - 1, 'no-square': 3 * math.sqrt(0.21) / 0.04, 'carried': own})

# ---------------------------------------------------------------- exam topic-1.6, new items
E = load('app/content/exams/topic-1.6.json')
it = E['s-uniform-moments']
th = math.sqrt(3 * 0.12)
ok(near(stats.uniform(-th, 2 * th).moment(2), 0.12), 'uniform: second moment theta^2/3')
check(it['widget'], 'uniform', th, {'no-root': 0.36, 'no-three': math.sqrt(0.12), 'two-mean': 0.04})
ok(abs(math.sqrt(3 * (0.12 - 0.02 ** 2)) - 0.6) <= it['widget']['tol']['abs'], 'uniform: the central-moment route is inside the band')

it = E['s-chi-order-mix']
obs = [86, 74, 40]
x2 = stats.chisquare(obs, [100, 60, 40]).statistic
c = cells(it['parts'][0]['widget'])
check(c[0], 'order mix X2', x2, {'over-observed': sum((o - e) ** 2 / o for o, e in zip(obs, [100, 60, 40])), 'no-divide': 392})
check(c[1], 'order mix df', 2, {'cells': 3})
ok(x2 < stats.chi2(2).ppf(0.95) and x2 > stats.chi2(1).ppf(0.95), 'order mix 2: below 5.991, above 3.841')
ok(near(stats.chi2(2).sf(x2), 0.073, 5e-4), 'order mix: p-value 0.073')

it = E['s-pool-rates']
lrp = 2 * (stats.poisson.logpmf(90, 90) + stats.poisson.logpmf(60, 60) - stats.poisson.logpmf(90, 75) - stats.poisson.logpmf(60, 75))
c = cells(it['widget'])
check(c[0], 'pools -2 ln Lambda', lrp, {'no-two': lrp / 2, 'pearson': 2 * 15 ** 2 / 75, 'sign': -lrp})
check(c[1], 'pools df', 1, {'model-size': 2})

it = E['s-pareto-losses']
n, s = 80, 32.0
mle = optimize.minimize_scalar(lambda a: -(n * math.log(a) - (a + 1) * s), bounds=(0.1, 20), method='bounded').x
ok(near(integrate.quad(lambda t: 2.5 * t ** -3.5, 1, np.inf)[0], 1, 1e-9), 'pareto: the density integrates to 1')
ok([o['id'] for o in it['parts'][0]['widget']['options'] if o.get('correct')] == ['a'], 'pareto 1: key')
check(it['parts'][1]['widget'], 'pareto 2', n / s, {'upside-down': s / n, 'exponent': n / s - 1})
ok(near(mle, 2.5, 1e-4), 'pareto 2: numeric maximum')
check(it['parts'][2]['widget'], 'pareto 3', 2.5 ** 2 / n, {'sd': 2.5 / math.sqrt(n), 'info': n / 2.5 ** 2, 'alpha-not-squared': 2.5 / n})
# the option's general claim: "the maximum is sufficient when the support moves with the parameter"
# counter-example: the shifted exponential f = exp(-(x - t)) on x > t; two samples with one maximum and different minima
la = lambda t, xs: math.exp(-sum(x - t for x in xs)) if min(xs) > t else 0.0
r1 = la(0.5, [1, 5]) / la(0.5, [2, 5])
r2 = la(1.5, [1, 5]) / max(la(1.5, [2, 5]), 1e-300)
ok(r1 != r2, 'pareto 1 option c: with a moving lower end the maximum is NOT sufficient (likelihood ratio moves with the parameter)')

# ---------------------------------------------------------------- exam topic-2.1, new items
X = load('app/content/exams/topic-2.1.json')
fsp = lambda m: 4 - m + 2 * max(0, m - 3) + 1.5 * max(0, m - 7)
check(X['e-spline-slope']['widget'], 'spline slope', (fsp(12) - fsp(8)) / 4, {'last-hinge': 1.5, 'no-base': 3.5, 'base-sign': 4.5})
w, b = np.array([2.0, -1.0]), 1.0
pt = {'a': (0.2, 0.9), 'b': (-0.5, 0.5), 'c': (-1, -1.4), 'd': (1, 0), 'e': (0, 2.5), 'f': (0, 0)}
inside = sorted(k for k, p in pt.items() if -1 < w @ np.array(p) + b < 1 - 1e-12)
ok(inside == sorted(o['id'] for o in X['e-street-inside']['widget']['options'] if o.get('correct')), f'street: inside {inside}')
sp = np.array([2, 3, 7, 11, 12, 13, 22.0])
cc = [2.0, 3.0]
hist = []
for _ in range(10):
    lab = np.array([int(abs(p - cc[1]) < abs(p - cc[0])) for p in sp])
    cc = [sp[lab == 0].mean(), sp[lab == 1].mean()]
    hist.append(tuple(round(v, 2) for v in cc))
ok(hist[:3] == [(2, 11.33), (2.5, 13), (4, 14.5)] and hist[3] == hist[2], f'kmeans: centres {hist[:4]}')
inert = sum((p - cc[l]) ** 2 for p, l in zip(sp, lab))
early = sum((p - [2.5, 13][int(p > 3)]) ** 2 for p in sp)
check(X['e-kmeans-spreads']['widget'], 'kmeans', inert, {'early-stop': early, 'unsquared': sum(abs(p - cc[l]) for p, l in zip(sp, lab))})
Lw = lambda w2, w1=0.5, v=2.0: 0.5 * (v * max(0, w1 * 1 + w2 * 3 + 0.4) - 1) ** 2
gw = (Lw(-0.2 + 1e-6) - Lw(-0.2 - 1e-6)) / 2e-6
check(X['e-unit-gradient']['widget'], 'gradient', round(gw, 6), {'used-x1': -0.8, 'slope-v': -0.12, 'sign': 2.4, 'no-half': -4.8})
rows = X['e-report-which']['canvas']['params']['rows']
pick = max(rows, key=lambda r: float(r[1]))
ok(pick[2] == '0.63' and near(np.mean([float(r[2]) for r in rows]), 0.6525), 'report: 0.63 and the mean 0.6525')

print(f'mine: {checks} checks, {fails} failures')
raise SystemExit(1 if fails else 0)
