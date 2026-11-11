"""Second read, problem sets 1.6 (a): every part's key and every `wrong` value of estimation and regression problems-1 to -3,
recomputed by the reader from the item's text. No import from the authors' scripts. Where another route exists it is used
(numerical maximisation for each MLE, enumeration of all 27 bootstrap resamples, a statsmodels fit of data built to the stated
sums, SciPy quantiles, a simulation for the overlap factor and HAC).
Run from the repo root with the scratchpad venv:  python docs/reviews/review-problems-1.6-a-scripts/mine.py [--sim]
A line starting CLAIM is a check that confirms a false or loose statement in the content (a finding); it does not fail the run."""
import itertools
import json
import math
import sys
from fractions import Fraction as Fr

import numpy as np
from scipy import optimize, stats
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson

ROOT = 'app/content/courses/'
DOCS = {}
checks = fails = 0


def part(course, n, item, k):
    key = (course, n)
    if key not in DOCS:
        DOCS[key] = json.load(open(f'{ROOT}{course}/problems-{n}.json'))
    it = next(i for i in DOCS[key]['items'] if i['id'] == item)
    return it['parts'][k - 1]


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def close(a, b, tol):
    return abs(a - b) <= tol + 1e-12


SEEN = set()


def num(course, n, item, k, answer, wrong=None, pct=False):
    """answer: my value (in % if pct); wrong: {id: my value}. The stored key must be within its own tol of mine,
    each stored wrong value within its own tol of mine, and every stored wrong id must be in my table."""
    p = part(course, n, item, k)
    w = p['widget']
    SEEN.add((course, n, item, k))
    where = f'{course}/problems-{n} {item} part {k}'
    ok(w['kind'] == 'numeric', f'{where}: numeric')
    s = 0.01 if pct else 1
    ok((w.get('unit') == '%') == pct, f'{where}: unit % flag {w.get("unit")}')
    tol = w['tol']['abs']
    ok(close(w['answer'], answer * s, max(tol, 1e-9)), f'{where}: key {w["answer"]} against mine {answer * s}')
    wrong = wrong or {}
    for x in w.get('wrong', []):
        ok(x['id'] in wrong, f'{where}: wrong "{x["id"]}" not in my table')
        if x['id'] in wrong:
            mine = wrong[x['id']] * s
            ok(close(x['value'], mine, max(x['tol']['abs'], 1e-9)), f'{where}: wrong "{x["id"]}" {x["value"]} against mine {mine}')
            ok(not close(mine, w['answer'], tol), f'{where}: wrong "{x["id"]}" inside the key band')
        ok(x['id'] in p['feedback'].get('byKey', {}), f'{where}: wrong "{x["id"]}" has a line')


def choice(course, n, item, k, right):
    p = part(course, n, item, k)
    SEEN.add((course, n, item, k))
    got = [o['id'] for o in p['widget']['options'] if o.get('correct')]
    ok(got == [right], f'{course}/problems-{n} {item} part {k}: correct option {got} against mine {right}')


def expr(course, n, item, k, f, wrongs, var):
    """f: my function of the variable; each stored form is evaluated at five points by a tiny LaTeX-to-Python rewrite."""
    p = part(course, n, item, k)
    SEEN.add((course, n, item, k))
    w = p['widget']

    def ev(tex, x):
        s = tex.replace('\\ln\\lambda', '\\ln(\\lambda)').replace('\\lambda', 'L').replace('\\ln', '§').replace('\\frac{w^2}{2}', '(w^2/2)')
        s = s.replace('e^', 'E^').replace('^{', '^(').replace('}', ')')
        out, prev = '', ''
        for ch in s:
            if prev and (prev.isdigit() or prev in ')wpL') and (ch in 'wpLE§('):
                out += '*'
            out += ch
            prev = ch
        out = out.replace('§', 'log').replace('^', '**')
        return eval(out, {'log': math.log, 'E': math.e, 'L': x, 'w': x, 'p': x})
    pts = [0.13, 0.31, 0.47, 0.62, 0.88]
    for form in [w['answer']] + w.get('accept', []):
        ok(all(close(ev(form, x), f(x), 1e-9) for x in pts), f'{course}/problems-{n} {item} part {k}: form {form} equals mine')
    for x in w.get('wrong', []):
        ok(x['id'] in wrongs, f'{item} part {k}: wrong "{x["id"]}" not in my table')
        if x['id'] in wrongs:
            ok(all(close(ev(x['tex'], t), wrongs[x['id']](t), 1e-9) for t in pts), f'{item} part {k}: wrong "{x["id"]}" {x["tex"]} is the slip named')
            ok(any(not close(wrongs[x['id']](t), f(t), 1e-6) for t in pts), f'{item} part {k}: wrong "{x["id"]}" differs from the key')


sq = math.sqrt
E, R = 'estimation', 'regression'

# ---------------------------------------------------------------- estimation 1
x = [304, 318, 296, 322, 310]
m = sum(x) / 5
ss = sum((v - m) ** 2 for v in x)
ok(ss == np.var(x) * 5, 'ping SS by numpy')
num(E, 1, 'p-ping-latency', 1, m, {'by-four': sum(x) / 4, 'range': max(x) - min(x)})
num(E, 1, 'p-ping-latency', 2, np.var(x, ddof=1), {'by-n': ss / 5, 'no-divide': ss, 'abs': sum(abs(v - m) for v in x) / 4})
num(E, 1, 'p-ping-latency', 3, sq(110 / 5), {'carried': sq(88 / 5), 'root-of-n': sq(110) / 5, 'sd': sq(110), 'variance': 22})
num(E, 1, 'p-ping-latency', 4, 110, {'carried': 88, 'unsquared': sq(110), 'from-se': 22})

v = 36 / 16
num(E, 1, 'p-route-delays', 1, v, {'se': 1.5, 'sd-over-n': 6 / 16, 'root-n': 36 / 4})
num(E, 1, 'p-route-delays', 2, 0.5 * 3 - 3, {'mean-not-bias': 1.5, 'unbiased': 3})
mse_half = lambda vv, mu: vv / 4 + (mu / 2) ** 2
num(E, 1, 'p-route-delays', 3, mse_half(v, 3), {'unquartered': v + 2.25, 'bias-unsquared': v / 4 + 1.5, 'carried': mse_half(1.5, 3), 'variance-only': v / 4})
cut = optimize.brentq(lambda mu: mse_half(v, mu) - v, 0.1, 10)
num(E, 1, 'p-route-delays', 4, cut, {'no-root': 3 * v, 'bias-unquartered': sq(0.75 * v), 'carried': sq(3 * 1.5)})
rng = np.random.default_rng(7)
xb = rng.normal(3, 6, size=(400000, 16)).mean(axis=1)
ok(abs(np.mean((xb / 2 - 3) ** 2) - 2.8125) < 0.02 and abs(np.mean((xb - 3) ** 2) - 2.25) < 0.02, 'route-delays MSEs by simulation')

num(E, 1, 'p-sulphur-labs', 1, 36 / 9, {'se': 2, 'root-n': 12})
num(E, 1, 'p-sulphur-labs', 2, 9 / 36 + 0.25, {'variance-only': 0.25, 'bias-unsquared': 0.75})
blend = lambda b: (lambda w: b * w * w + 4 * (1 - w) ** 2)
expr(E, 1, 'p-sulphur-labs', 3, blend(0.5), {'unsquared-weights': lambda w: 0.5 * w + 4 * (1 - w), 'no-bias': blend(0.25), 'swapped': lambda w: 4 * w * w + 0.5 * (1 - w) ** 2}, 'w')
best = lambda b: optimize.minimize_scalar(blend(b), bounds=(0, 1), method='bounded', options={'xatol': 1e-10})
num(E, 1, 'p-sulphur-labs', 4, best(0.5).x, {'swapped': 1 - best(0.5).x, 'no-bias': best(0.25).x, 'carried': best(0.75).x, 'half': 0.5})
num(E, 1, 'p-sulphur-labs', 5, best(0.5).fun, {'half-half': blend(0.5)(0.5), 'no-bias': best(0.25).fun, 'carried': best(0.75).fun, 'swapped': blend(0.5)(1 / 9), 'b-alone': 0.5})
a_ = rng.normal(100, 6, size=(300000, 9)).mean(axis=1)
b_ = rng.normal(100.5, 3, size=(300000, 36)).mean(axis=1)
ok(abs(np.mean((8 / 9 * b_ + 1 / 9 * a_ - 100) ** 2) - 4 / 9) < 0.01, 'sulphur blend MSE by simulation')

r = [12, -6, 6, -10, 8]
mr = sum(r) / 5
ssr = sum((t - mr) ** 2 for t in r)
num(E, 1, 'p-reference-mass', 1, mr, {'by-four': sum(r) / 4, 'sizes': sum(map(abs, r)) / 5})
num(E, 1, 'p-reference-mass', 2, ssr, {'from-zero': sum(t * t for t in r), 's-squared': ssr / 4, 'by-n': ssr / 5})
num(E, 1, 'p-reference-mass', 3, sum(t * t for t in r) / 5, {'ss-by-n': ssr / 5, 's-squared': ssr / 4, 'by-four': sum(t * t for t in r) / 4, 'subtracted': (ssr - 5 * mr ** 2) / 5})
choice(E, 1, 'p-reference-mass', 4, 'known')
num(E, 1, 'p-reference-mass', 5, math.ceil(76 / 4), {'unsquared': sq(76) / 2, 'carried-90': 90 / 4, 'carried-72': 72 / 4, 'sd-not-se': 76 / 2})
ok(95 / 76 == 1.25, 'reference-mass option "close": 76 and 95 differ by a quarter')

# ---------------------------------------------------------------- estimation 2
L = lambda p: p ** 9 * (1 - p) ** 3
expr(E, 2, 'p-robot-deliveries', 1, L, {'swapped': lambda p: p ** 3 * (1 - p) ** 9, 'added': lambda p: 9 * p + 3 * (1 - p), 'one-failure': lambda p: p ** 9 * (1 - p), 'any-order': lambda p: 220 * L(p)}, 'p')
ok(math.comb(12, 9) == 220, 'robot C(12,9)')
ph = optimize.minimize_scalar(lambda p: -L(p), bounds=(0.01, 0.99), method='bounded', options={'xatol': 1e-10}).x
num(E, 2, 'p-robot-deliveries', 2, ph, {'failure-share': 0.25, 'odds': 3})
pr = optimize.minimize_scalar(lambda p: -L(p), bounds=(0.9, 1), method='bounded', options={'xatol': 1e-12}).x
num(E, 2, 'p-robot-deliveries', 3, pr, {'unrestricted': 0.75, 'top': 1})
num(E, 2, 'p-robot-deliveries', 4, L(0.75) / L(0.9), {'inverted': L(0.9) / L(0.75), 'no-failures': (0.75 / 0.9) ** 9, 'same': 1})
ok(abs((0.9 / 0.75) ** 9 - 5.16) < 0.01 and (0.25 / 0.1) ** 3 == 15.625, 'robot explain: 5.2 and 15.6')

t = np.array([52, 47, 55, 50.0])
ll = lambda mu, s=4.0: stats.norm.logpdf(t, mu, s).sum()
mh = optimize.minimize_scalar(lambda mu: -ll(mu)).x
num(E, 2, 'p-tank-sensor', 1, mh, {'by-three': t.sum() / 3, 'middle-two': 52.5})
d = ll(51) - ll(48)
num(E, 2, 'p-tank-sensor', 2, d, {'no-two': 36 / 16, 'sd-not-squared': 36 / 8, 'reversed': -d})
num(E, 2, 'p-tank-sensor', 3, math.exp(d), {'carried': math.exp(2.25), 'no-exp': d, 'inverted': math.exp(-d)})
top = optimize.brentq(lambda mu: ll(51) - ll(mu) - math.log(10), 51, 70)
num(E, 2, 'p-tank-sensor', 4, top, {'log-ten': 51 + sq(8), 'no-root': 51 + 8 * math.log(10), 'sd-not-squared': 51 + sq(2 * math.log(10)), 'no-n': 51 + sq(32 * math.log(10))})
ok(sorted(t)[1:3] == [50.0, 52.0], 'CLAIM tank-sensor part 1 "middle-two": the middle two readings are 50 and 52 (mean 51, the key), not 50 and 55')
print('CLAIM tank-sensor part 1: wrong id "middle-two" is 52.5 = (50 + 55)/2, the last two readings; the middle two average 51')

w8 = np.array([1.4, -0.6, 0.7, -1.3, 1.1, -0.1, 1.8, -1.0])
ok(abs((w8 ** 2).sum() - 9.96) < 1e-9, 'currency squares add to 9.96')
res = optimize.minimize(lambda q: -stats.norm.logpdf(w8, q[0], abs(q[1])).sum(), [0.0, 1.0], method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-12})
muh, sgh = res.x[0], abs(res.x[1])
num(E, 2, 'p-currency-vol', 1, muh, {'by-seven': w8.sum() / 7, 'sizes': abs(w8).sum() / 8})
num(E, 2, 'p-currency-vol', 2, sgh, {'n-minus-one': w8.std(ddof=1), 'zero-mean': sq(9.96 / 8), 'variance': sgh ** 2})
num(E, 2, 'p-currency-vol', 3, 1.0874 * sq(52), {'times-52': 1.0874 * 52, 'trading-days': 1.0874 * sq(252), 'carried': w8.std(ddof=1) * sq(52), 'variance': 52 * 1.1825})
num(E, 2, 'p-currency-vol', 4, 7.84 / sq(16), {'no-two': 7.84 / sq(8), 'weeks-in-year': 7.84 / sq(104), 'no-root': 7.84 / 16})
n5 = math.ceil((7.84 / 0.5) ** 2 / 2)
num(E, 2, 'p-currency-vol', 5, n5, {'no-two': math.ceil((7.84 / 0.5) ** 2), 'unsquared': 7.84 / 0.5 / 2, 'no-two-unsquared': 7.84 / 0.5})
ok(math.ceil((sgh * sq(52) / 0.5) ** 2 / 2) == 123, 'currency part 5 from the unrounded volatility is 123 too')
# the given rule SE(sigma-hat) ~ sigma/sqrt(2n): sd of the MLE over normal samples of 8 (sigma 1)
sim = rng.normal(0, 1, size=(200000, 8)).std(axis=1)
print(f'NOTE currency part 4: sd of sigma-hat over 200,000 normal samples of 8 is {sim.std():.4f}; the rule gives {1 / 4:.4f}')

waits = [2, 7, 4, 1, 6]
lam = lambda z: 5 * math.log(z) - 20 * z
expr(E, 2, 'p-ride-waits', 1, lambda z: sum(stats.expon.logpdf(waits, scale=1 / z)), {'likelihood': lambda z: z ** 5 * math.exp(-20 * z), 'sign': lambda z: 5 * math.log(z) + 20 * z, 'one-log': lambda z: math.log(z) - 20 * z}, 'L')
l1 = optimize.minimize_scalar(lambda z: -lam(z), bounds=(0.01, 2), method='bounded', options={'xatol': 1e-10}).x
num(E, 2, 'p-ride-waits', 2, l1, {'mean-wait': 4, 'one-log': 1 / 20})
cens = lambda z: sum(stats.expon.logpdf(waits, scale=1 / z)) + stats.expon.logsf(8, scale=1 / z)
l2 = optimize.minimize_scalar(lambda z: -cens(z), bounds=(0.01, 2), method='bounded', options={'xatol': 1e-10}).x
num(E, 2, 'p-ride-waits', 3, l2, {'as-complete': 6 / 28, 'dropped': 0.25, 'no-time': 6 / 20})
num(E, 2, 'p-ride-waits', 4, stats.expon.sf(10, scale=1 / l2), {'old-rate': math.exp(-2.5), 'as-complete': math.exp(-60 / 28), 'complement': 1 - math.exp(-50 / 28)})

# ---------------------------------------------------------------- estimation 3
ph = 96 / 600
se = sq(ph * (1 - ph) / 600)
num(E, 3, 'p-email-clicks', 1, ph, {'non-clicks': 1 - ph, 'count': 96})
num(E, 3, 'p-email-clicks', 2, se, {'no-root': se ** 2, 'no-n': sq(ph * (1 - ph)), 'root-n-only': ph * (1 - ph) / sq(600)})
z95, z90 = stats.norm.ppf(0.975), stats.norm.ppf(0.95)
num(E, 3, 'p-email-clicks', 3, ph - z95 * se, {'ninety': ph - z90 * se, 'one-se': ph - 0.015, 'upper': ph + z95 * se})
choice(E, 3, 'p-email-clicks', 4, 'excluded')

f3 = [2, 4, 9]
means = [np.mean(c) for c in itertools.product(f3, repeat=3)]
boot = np.std(means)
num(E, 3, 'p-three-month-fund', 1, np.std(f3, ddof=1) / sq(3), {'sd': np.std(f3, ddof=1), 'by-n': np.std(f3) / sq(3), 'no-root': 13 / 3})
num(E, 3, 'p-three-month-fund', 2, np.var(f3), {'s-squared': 13, 'no-divide': 26, 'sd': np.std(f3)})
num(E, 3, 'p-three-month-fund', 3, boot, {'carried': sq(13 / 3), 'no-root': 26 / 9, 'one-draw': np.std(f3)})
num(E, 3, 'p-three-month-fund', 4, boot / (np.std(f3, ddof=1) / sq(3)), {'inverted': sq(1.5), 'squared': 2 / 3, 'same': 1})
ok(round(1.70 / 2.08, 3) == 0.817 and round(sq(2 / 3), 3) == 0.816, 'CLAIM three-month-fund part 4: the feedback prints 0.817 and calls it sqrt(2/3); the explanation prints 0.816')
print('CLAIM three-month-fund part 4: feedback "1.70/2.08 = 0.817, which is sqrt(2/3)" against explain "sqrt(2/3) = 0.816"')

post = stats.beta(8 + 21, 12 + 9)
num(E, 3, 'p-ticket-bot', 1, post.mean(), {'mle': 0.7, 'prior': 0.4, 'swapped': 17 / 50})
num(E, 3, 'p-ticket-bot', 2, (post.mean() - 0.4) / (0.7 - 0.4), {'prior-weight': 0.4, 'ratio': 1.5})
gap = lambda n: abs(0.7 - stats.beta(8 + 0.7 * n, 12 + 0.3 * n).mean())
n3 = next(n for n in range(1, 5000) if gap(n) <= 0.01 + 1e-12)
num(E, 3, 'p-ticket-bot', 3, n3, {'no-prior-size': 600, 'wrong-gap': 20 * 0.7 / 0.01 - 20, 'prior-mean': 20 * 0.4 / 0.01 - 20})
se580 = sq(0.21 / 580)
num(E, 3, 'p-ticket-bot', 4, 0.01 / se580, {'inverted': se580 / 0.01, 'se': se580, 'no-root': 0.01 / se580 ** 2})

sea, seb = 3 / 10, 4.2 / 12
sed = sq(sea ** 2 + seb ** 2)
num(E, 3, 'p-routing-test', 1, sea, {'by-n': 0.03, 'variance': 0.09})
num(E, 3, 'p-routing-test', 2, sed, {'added': sea + seb, 'no-root': sed ** 2, 'subtracted': seb - sea})
num(E, 3, 'p-routing-test', 3, 0.8 - 1.96 * 0.461, {'added-se': 0.8 - 1.96 * 0.65, 'no-root': 0.8 - 1.96 * 0.2125, 'upper': 0.8 + 1.96 * 0.461, 'ninety': 0.8 - 1.645 * 0.461})
choice(E, 3, 'p-routing-test', 4, 'no-proof')

# ---------------------------------------------------------------- regression 1
b = -0.8 * 45 / 3
a = 300 - b * 4
num(R, 1, 'p-gas-demand', 1, b, {'no-sign': -b, 'variances': -0.8 * 45 ** 2 / 3 ** 2, 'no-r': -15})
num(R, 1, 'p-gas-demand', 2, a, {'sign': 300 - 48, 'mean': 300, 'swapped': 4 - b * 300})
num(R, 1, 'p-gas-demand', 3, a + b * -5, {'minus': a - 60, 'carried': 252 + 60, 'from-mean': 300 + 60})
num(R, 1, 'p-gas-demand', 4, 450 - 408, {'flipped': -42, 'carried': 450 - 312, 'minus': 450 - 288})
num(R, 1, 'p-gas-demand', 5, 42 / (45 * sq(1 - 0.64)), {'total-sd': 42 / 45, 'no-root': 42 / (45 * 0.36), 'explained': 42 / 36, 'carried': 138 / 27})
# s_y sqrt(1 - r^2) is the sd of the residuals with the divisor of s_y: a fit of built data
xx = rng.normal(size=90); yy = -0.5 * xx + rng.normal(size=90)
fit = sm.OLS(yy, sm.add_constant(xx)).fit()
ok(abs(np.std(fit.resid, ddof=1) - np.std(yy, ddof=1) * sq(1 - fit.rsquared)) < 1e-12, 'gas-demand part 5: s_y sqrt(1 - r^2) is the residual sd, divisor n - 1')

age = np.array([1, 2, 3, 4, 5, 9.0]); price = np.array([18000, 16600, 15400, 13400, 12400, 6200.0])
sxx = ((age - age.mean()) ** 2).sum()
slope = np.polyfit(age, price, 1)[0]
p2 = price.copy(); p2[5] = 8200
slope2 = np.polyfit(age, p2, 1)[0]
num(R, 1, 'p-car-prices', 1, sxx, {'no-centre': (age ** 2).sum(), 'by-n': sxx / 6, 'n-1': sxx / 5})
num(R, 1, 'p-car-prices', 2, slope, {'no-sign': -slope, 'carried': -59200 / 136, 'sxy-only': -59200})
num(R, 1, 'p-car-prices', 3, slope2 - slope, {'no-deviation': 2000 / 40, 'raw-x': 9 * 2000 / 40, 'carried': 10000 / 136})
num(R, 1, 'p-car-prices', 4, slope2, {'wrong-way': -1480 - 250, 'carried': -1480 + 50, 'raw-x': -1480 + 450})
ok(abs(250 / 1480 - 1 / 6) < 0.003, 'car-prices: the slope moved by about a sixth')

px = np.array([10, 12, 14, 16, 18.0]); known = [5.0, 6.6, 7.4, 8.6]
ybar = 1.2 + 0.4 * px.mean()
y3 = 5 * ybar - sum(known)
py = np.array([5.0, 6.6, y3, 7.4, 8.6])
bb, aa = np.polyfit(px, py, 1)
ok(abs(bb - 0.4) < 1e-9 and abs(aa - 1.2) < 1e-9, 'smudged-shift: with 6.4 the least squares line is 1.2 + 0.4x')
e = py - (aa + bb * px)
num(R, 1, 'p-smudged-shift', 1, ybar, {'four-known': sum(known) / 4, 'intercept': 1.2, 'mean-x': 14})
num(R, 1, 'p-smudged-shift', 2, y3, {'carried': 5 * 6.9 - 27.6, 'on-line': 6.8, 'total': 34})
num(R, 1, 'p-smudged-shift', 3, e[2], {'flipped': -e[2], 'carried': 6.9 - 6.8, 'on-line': 0})
num(R, 1, 'p-smudged-shift', 4, (e ** 2).sum(), {'abs': abs(e).sum(), 'no-third': (e ** 2).sum() - e[2] ** 2, 'carried': (e ** 2).sum() - e[2] ** 2 + 0.01})
sst = ((py - py.mean()) ** 2).sum()
num(R, 1, 'p-smudged-shift', 5, 1 - (e ** 2).sum() / sst, {'flipped': (e ** 2).sum() / sst, 'carried': 1 - 0.48 / sst, 'unsquared': 1 - 1.6 / sst})

sp = np.array([20, 30, 40, 50, 60.0]); dist = np.array([12, 23, 36, 53, 73.0])
fit = sm.OLS(dist, sm.add_constant(sp)).fit()
a1, b1 = fit.params
syy = ((dist - dist.mean()) ** 2).sum()
sxy = ((sp - 40) * dist).sum()
num(R, 1, 'p-stopping-distances', 1, b1, {'reverse': 1000 / sxy, 'mixed': (sxy / 4) / (1000 / 5), 'through-origin': (sp * dist).sum() / (sp ** 2).sum()})
num(R, 1, 'p-stopping-distances', 2, a1, {'sign': 39.4 + 1.52 * 40, 'mean': 39.4, 'carried': 39.4 - 1.0444 * 40})
num(R, 1, 'p-stopping-distances', 3, fit.resid[2], {'flipped': -fit.resid[2], 'carried': 36 - (100.2 + 60.8), 'no-intercept': 36 - 60.8})
num(R, 1, 'p-stopping-distances', 4, fit.rsquared, {'unsquared': 1.52 * 1000 / syy, 'root': sq(fit.rsquared), 'flipped': 1 - fit.rsquared})
choice(R, 1, 'p-stopping-distances', 5, 'curve')
ok(np.allclose(fit.resid, [3.0, -1.2, -3.4, -1.6, 3.2]) and abs(a1 + b1 * 70 - 85) < 1e-9, 'stopping: residuals listed in part 5 and the 85 m at 70 mph')
rev = sm.OLS(sp, sm.add_constant(dist)).fit().params[1]
ok(abs(rev - sxy / syy) < 1e-12 and abs(rev - 0.6481) < 1e-4 and abs(1000 / sxy - 0.6579) < 1e-4, 'reverse slope')
print(f'CLAIM stopping part 1 "reverse": the least squares slope of speed on distance is S_xy/S_yy = {rev:.4f}; the line calls S_xx/S_xy = {1000 / sxy:.4f} that slope')
print(f'CLAIM stopping part 5 option "outlier": |residual at 40 mph| = {abs(fit.resid[2]):.1f} m, the end misses are {fit.resid[0]:.1f} and {fit.resid[4]:.1f} m; "no larger than the misses at the ends" is false')
ok(abs(fit.resid[2]) > max(abs(fit.resid[0]), abs(fit.resid[4])), 'stopping: the 40 mph miss is the largest of the five')

# ---------------------------------------------------------------- regression 2
s = sq(2304 / 16)
num(R, 2, 'p-sunny-cones', 1, s, {'by-n': sq(2304 / 18), 'n-1': sq(2304 / 17), 'no-root': 144})
num(R, 2, 'p-sunny-cones', 2, s / sq(64), {'no-root': s / 64, 'variance': 144 / 8, 'carried': sq(128) / 8})
num(R, 2, 'p-sunny-cones', 3, 2.4 / 1.5, {'inverted': 1.5 / 2.4, 'carried': 2.4 / 0.1875, 'carried-n': 2.4 / (sq(128) / 8)})
num(R, 2, 'p-sunny-cones', 4, 2.4 / (s / sq(4 * 64)), {'no-root': 6.4, 'same': 1.6, 'carried': 25.6})
ok(abs(stats.t.ppf(0.975, 16) - 2.120) < 5e-4 and stats.t.ppf(0.975, 70) < 3.2, 'sunny-cones cut-offs')

# a fit with n = 42 and R^2 = 0.2 exactly, coefficient 0.85: statsmodels' own F, t, bse and interval
n = 42
xf = rng.normal(size=n); xf -= xf.mean()
ef = rng.normal(size=n); ef -= ef.mean(); ef -= xf * (xf @ ef) / (xf @ xf)
ef *= sq(4 * 0.85 ** 2 * (xf @ xf) / (ef @ ef))          # SSE = 4 ESS, so R^2 = 0.2
fr = sm.OLS(2 + 0.85 * xf + ef, sm.add_constant(xf)).fit()
ok(abs(fr.rsquared - 0.2) < 1e-12 and abs(fr.params[1] - 0.85) < 1e-12, 'freight: built fit has R^2 0.2 and slope 0.85')
num(R, 2, 'p-freight-summary', 1, fr.fvalue, {'no-df': 0.25, 'by-n': 0.25 * 42, 'n-1': 0.25 * 41})
num(R, 2, 'p-freight-summary', 2, fr.tvalues[1], {'no-root': 10, 'half': 5, 'carried': sq(10.5), 'carried-df': 0.5})
num(R, 2, 'p-freight-summary', 3, fr.bse[1], {'times': 0.85 * 3.16, 'inverted': 3.16 / 0.85, 'carried-f': 0.085, 'carried': 0.85 / 3.24})
num(R, 2, 'p-freight-summary', 4, fr.conf_int()[1][0], {'normal': 0.85 - 1.96 * 0.269, 'upper': 0.85 + 2.021 * 0.269, 'no-crit': 0.85 - 0.269, 'carried': 0.85 - 2.021 * 0.085})
ok(abs(stats.t.ppf(0.975, 40) - 2.021) < 5e-4, 'freight t cut-off')

# raw on raw against excess on excess: built data
mkt = rng.normal(0.7, 4, size=100); rf = 0.25
exc = 0.35 + 0.6 * (mkt - rf) + rng.normal(0, 2.5, size=100)
fe = sm.OLS(exc, sm.add_constant(mkt - rf)).fit(); fraw = sm.OLS(exc + rf, sm.add_constant(mkt)).fit()
ok(abs(fraw.params[1] - fe.params[1]) < 1e-10 and abs(fraw.params[0] - (fe.params[0] + (1 - fe.params[1]) * rf)) < 1e-10, 'raw intercept = alpha + (1 - beta) r_f, same slope')
num(R, 2, 'p-raw-intercept', 1, 0.45 - 0.4 * 0.25, {'raw': 0.45, 'beta': 0.45 - 0.6 * 0.25, 'sign': 0.45 + 0.1}, pct=True)
num(R, 2, 'p-raw-intercept', 2, 2.5 / 10, {'by-n': 0.025, 'variance': 2.5 ** 2 / 100}, pct=True)
num(R, 2, 'p-raw-intercept', 3, 0.35 / 0.25, {'raw': 1.8, 'beta': 1.2, 'carried-n': 14, 'inverted': 0.25 / 0.35})
need = lambda t0: next(k for k in range(1, 10 ** 5) if t0 * sq(k / 100) >= 2 - 1e-12)
num(R, 2, 'p-raw-intercept', 4, need(1.4), {'raw': need(1.8), 'linear': math.ceil(100 * 2 / 1.4), 'beta': need(1.2), 'round-down': need(1.4) - 1})

s = sq(588 / 48)
seb = s / sq(49 * 25)
tq = stats.t.ppf(0.975, 48)
ok(abs(tq - 2.011) < 5e-4, 'grocer t cut-off')
num(R, 2, 'p-grocer-beta', 1, s, {'by-n': sq(588 / 50), 'n-1': sq(588 / 49), 'no-root': 12.25}, pct=True)
num(R, 2, 'p-grocer-beta', 2, seb, {'no-n': 3.5 / 5, 'variance': 3.5 / sq(49 * 5), 'no-root': 12.25 / 1225})
num(R, 2, 'p-grocer-beta', 3, (0.74 - 1) / seb, {'zero': 7.4, 'sign': 2.6, 'carried': -0.26 / 0.7, 'variance': -0.26 / 0.2236})
num(R, 2, 'p-grocer-beta', 4, 0.74 + 2.011 * 0.1, {'normal': 0.74 + 0.196, 'lower': 0.74 - 0.2011, 'carried': 0.74 + 2.011 * 0.7})
choice(R, 2, 'p-grocer-beta', 5, 'below')

# ---------------------------------------------------------------- regression 3
dl = (1.74 - 1.5) / 0.8
rr = dl * 10 / 5
vif = 1 / (1 - rr ** 2)
num(R, 3, 'p-power-price', 1, dl, {'no-divide': 0.24, 'sign': -0.3, 'times': 0.24 * 0.8})
num(R, 3, 'p-power-price', 2, rr, {'inverted': dl * 5 / 10, 'same': dl, 'carried': 0.24 * 2})
num(R, 3, 'p-power-price', 3, vif, {'no-square': 1 / (1 - rr), 'root': sq(vif), 'r2': rr ** 2, 'carried': 1 / (1 - 0.48 ** 2)})
num(R, 3, 'p-power-price', 4, math.ceil(200 * vif), {'root': 250, 'no-square': 500, 'carried': math.ceil(200 * 1.2994), 'round-down': 312})
# built data: gas sd 10, carbon sd 5, r 0.6, slopes 1.5 and 0.8 exactly; the short regression and statsmodels' VIF
g = rng.normal(size=200); g = (g - g.mean()) / g.std(ddof=1)
c0 = rng.normal(size=200); c0 -= c0.mean(); c0 -= g * (g @ c0) / (g @ g); c0 /= c0.std(ddof=1)
gas = 10 * g; carbon = 5 * (0.6 * g + 0.8 * c0)
u = rng.normal(size=200); X2 = sm.add_constant(np.column_stack([gas, carbon])); u -= X2 @ np.linalg.lstsq(X2, u, rcond=None)[0]
pw = 40 + 1.5 * gas + 0.8 * carbon + u
ok(abs(sm.OLS(pw, sm.add_constant(gas)).fit().params[1] - 1.74) < 1e-9, 'power-price: slope on gas alone is 1.74 when r = 0.6')
from statsmodels.stats.outliers_influence import variance_inflation_factor
ok(abs(variance_inflation_factor(X2, 1) - 1.5625) < 1e-9, 'power-price: statsmodels VIF 1.5625')

# solar: data with the stated sums of squares and products, then statsmodels
Sg = np.array([[40, 24, 88], [24, 30, 45], [88, 45, 250.0]])
Z = rng.normal(size=(24, 3)); Z -= Z.mean(axis=0)
Q, _ = np.linalg.qr(Z)
D = Q @ np.linalg.cholesky(Sg).T
ok(np.allclose(D.T @ D, Sg), 'solar: built data has the stated sums')
fs = sm.OLS(D[:, 2] + 30, sm.add_constant(D[:, :2] + [6, 15])).fit()
b1s, b2s = fs.params[1:]
num(R, 3, 'p-solar-output', 1, b1s, {'simple': 88 / 40, 'cramer-sign': (30 * 88 + 24 * 45) / 624, 'swapped': b2s})
num(R, 3, 'p-solar-output', 2, b2s, {'simple': 45 / 30, 'sign': (45 + 60) / 30, 'carried': (45 - 24 * 2.2) / 30})
num(R, 3, 'p-solar-output', 3, fs.ssr, {'sign': 250 - (220 + 22.5), 'ess': fs.ess, 'carried': 250 - (2.2 * 88 - 0.26 * 45)})
num(R, 3, 'p-solar-output', 4, fs.scale, {'by-n': 52.5 / 24, 'n-2': 52.5 / 22, 'n-1': 52.5 / 23, 'carried': 68.1 / 21})
num(R, 3, 'p-solar-output', 5, fs.rsquared_adj, {'plain': fs.rsquared, 'n': 1 - 2.5 / (250 / 24), 'carried': 1 - 2.1875 / (250 / 23), 'carried-n2': 1 - (52.5 / 22) / (250 / 23)})

s = sq(4500 / 500)
num(R, 3, 'p-overlap-signal', 1, s, {'by-n': sq(4500 / 503), 'no-root': 9}, pct=True)
num(R, 3, 'p-overlap-signal', 2, s * sq(0.0004), {'no-root-c': 3 * 0.0004, 's2c': 9 * 0.0004, 'carried': 9 * sq(0.0004)})
num(R, 3, 'p-overlap-signal', 3, 0.21 / 0.06, {'carried': 0.21 / 0.18, 'no-root': 0.21 / 0.0036, 'inverted': 0.06 / 0.21})
fac = sq(1 + 2 * sum((1 - j / 5) ** 2 for j in range(1, 5)))
num(R, 3, 'p-overlap-signal', 4, 3.5 / fac, {'no-root': 3.5 / fac ** 2, 'no-two': 3.5 / sq(2.2), 'times': 3.5 * fac, 'carried': (0.21 / 0.18) / fac})
choice(R, 3, 'p-overlap-signal', 5, 'not-sig')
bart = sq(1 + 2 * sum((1 - j / 5) ** 3 for j in range(1, 5)))
print(f'CLAIM overlap part 4 explain: with the part\'s own autocorrelations (1 - j/5)^2, Bartlett weights at 4 lags give a factor {bart:.3f}, not {fac:.3f}: t = {3.5 / bart:.2f}, above 1.96')

pred = 0.05 - 0.08 * 10 - 0.03 * -5
e7 = [0.20, 0.30, 0.25, 0.10, -0.10, -0.20, -0.25]
e8 = -0.90 - pred
ee = np.array(e7 + [e8])
ok(abs(ee.sum()) < 1e-12, 'bond-fund: the eight residuals add to 0')
ok(abs(sum(v * v for v in e7) - 0.315) < 1e-12 and abs(sum((e7[i] - e7[i - 1]) ** 2 for i in range(1, 7)) - 0.0875) < 1e-12, 'bond-fund: 0.315 and 0.0875')
dwf = lambda z: durbin_watson(np.array(e7 + [z]))
num(R, 3, 'p-bond-fund-weeks', 1, pred, {'spread-sign': 0.05 - 0.8 - 0.15, 'no-intercept': pred - 0.05, 'all-signs': 0.05 + 0.8 - 0.15}, pct=True)
num(R, 3, 'p-bond-fund-weeks', 2, e8, {'flipped': -e8, 'carried': 0, 'no-intercept': -0.90 + 0.65}, pct=True)
num(R, 3, 'p-bond-fund-weeks', 3, dwf(e8), {'no-week-8': 0.0875 / 0.315, 'flipped': dwf(0.30), 'fitted': dwf(-0.60), 'inverted': 1 / dwf(e8)})
num(R, 3, 'p-bond-fund-weeks', 4, 1 - dwf(e8) / 2, {'half': dwf(e8) / 2, 'no-two': 1 - dwf(e8), 'carried': 1 - 0.0875 / 0.315 / 2, 'carried-flip': 1 - dwf(0.30) / 2})
choice(R, 3, 'p-bond-fund-weeks', 5, 'hac')
rho = (ee[1:] @ ee[:-1]) / (ee @ ee)
print(f'CLAIM bond-fund part 4: the lag-1 autocorrelation of the eight residuals is {rho:.3f}; 1 - d/2 gives {1 - dwf(e8) / 2:.3f} (end terms (e1^2 + e8^2)/sum = {(ee[0] ** 2 + ee[-1] ** 2) / (ee @ ee):.3f} matter at n = 8)')

# every part of the six sets was checked
total = 0
for c in (E, R):
    for k in (1, 2, 3):
        part(c, k, DOCS.get((c, k), {'items': [{'id': None}]})['items'][0]['id'] or json.load(open(f'{ROOT}{c}/problems-{k}.json'))['items'][0]['id'], 1)
        for it in DOCS[(c, k)]['items']:
            for j in range(1, len(it['parts']) + 1):
                total += 1
                ok((c, k, it['id'], j) in SEEN, f'{c}/problems-{k} {it["id"]} part {j} not checked')
print(f'parts: {total}')

if '--sim' in sys.argv:
    # overlap: next-5-day return on (a) the past-5-day return, (b) an independent daily signal; no true effect; 503 days
    def run(kind, reps=1500, h=5, n=503):
        out = {'naive': [], 'hac4': [], 'hac8': [], 'hac20': []}
        for _ in range(reps):
            d_ = rng.normal(size=n + 2 * h)
            cs = np.cumsum(d_)
            past = cs[h:n + h] - cs[:n]
            nxt = cs[2 * h:n + 2 * h] - cs[h:n + h]
            xs = past if kind == 'past' else rng.normal(size=n)
            Xs = sm.add_constant(np.column_stack([xs, rng.normal(size=n)]))
            m0 = sm.OLS(nxt, Xs)
            out['naive'].append(m0.fit().tvalues[1])
            for lag in (4, 8, 20):
                out[f'hac{lag}'].append(m0.fit(cov_type='HAC', cov_kwds={'maxlags': lag}).tvalues[1])
        return {k_: (np.std(v_), np.mean(np.abs(v_) > 1.96)) for k_, v_ in out.items()}
    for kind in ('past', 'iid'):
        r_ = run(kind)
        print(f'SIM overlap h = 5, signal = {kind}: ' + '; '.join(f'{k_} sd of t {a_:.2f}, |t| > 1.96 in {100 * b_:.0f}%' for k_, (a_, b_) in r_.items()))

print(f'mine.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
