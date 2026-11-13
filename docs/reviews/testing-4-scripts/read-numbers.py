"""Second read, testing L4: every graded key and stated number recomputed by a second route
(SciPy distributions, SymPy integrals and derivatives, seeded simulation), independent of the
author's docs/reports/testing-L4-numbers.py. Also probes each numeric key with the engine's own
tolerance test (grade.js `within`) for sensible roundings and for the values the hints lead to.

Run from the repo root with the scratchpad venv python. A check that fails because the content
is wrong stays failing and is a finding in docs/reviews/review-testing-4.md.
`stated(file, text)` asserts the quoted number is really in the file, so a check cannot drift
from the content."""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy import stats

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'app', 'content', 'courses', 'testing')
F = {k: v for k, v in dict(
    l13='l13-matching-moments.json', l14='l14-what-data-can-forget.json', l15='l15-sharpness-of-the-peak.json',
    l16='l16-best-possible-precision.json', l17='l17-ratio-of-likelihoods.json',
    l18='l18-counts-against-expectations.json', rev='review-4.json', hw='homework-4.json').items()}
RAW = {k: open(os.path.join(ROOT, v), encoding='utf-8').read() for k, v in F.items()}
J = {k: json.loads(v) for k, v in RAW.items()}
passed = failed = 0
notes = []


def rec(ok, label, note=''):
    global passed, failed
    if ok:
        passed += 1
    else:
        failed += 1
        print(f'FAIL {label} {note}')


def near(label, stated, mine, tol=None):
    tol = tol if tol is not None else 0.5 * 10 ** (-dp(stated)) + 1e-12
    rec(abs(stated - mine) <= tol, label, f'stated {stated}, recomputed {mine:.6g}')


def dp(x):
    s = repr(float(x))
    return len(s.split('.')[1]) if '.' in s and 'e' not in s else 0


def stated(f, text):
    rec(text in RAW[f], f'{f}: text "{text}" present')


def W(f, where, i):
    return J[f][where][i]['widget']


def key(f, where, i):
    return W(f, where, i)['answer']


def within(v, a, tol):                      # grade.js within
    if 'rel' in tol:
        return abs(v - a) <= abs(a) * tol['rel'] + 1e-12
    return abs(v - a) <= tol.get('abs', 0) + 1e-9


def wrongs(f, where, i, expected):
    """Each wrong[] value equals the slip the reader computed, and is outside the key's tolerance."""
    w = W(f, where, i)
    got = {x['id']: x['value'] for x in w.get('wrong', [])}
    for k, v in expected.items():
        wt = next((x.get('tol', {}).get('abs', 0) for x in w.get('wrong', []) if x['id'] == k), 0)
        rec(k in got and abs(got[k] - v) <= max(1e-9, wt), f'{f} {where}[{i}] wrong "{k}" fires on the slip', f'stated {got.get(k)}, slip gives {v:.6g}')
    for k, v in got.items():
        rec(not within(v, w['answer'], w['tol']), f'{f} {where}[{i}] wrong "{k}" outside the key tolerance')


rng = np.random.default_rng(20261111)

# ================================================================ l13 method of moments
near('l13 s0 rate', key('l13', 'screens', 0), 1 / 0.5)
wrongs('l13', 'screens', 0, {'mean-as-rate': 0.5, 'double': 1})
a_, l_ = sp.symbols('a lam', positive=True)
sol = sp.solve([a_ / l_ - 6, a_ / l_ ** 2 - 12], [a_, l_], dict=True)[0]
near('l13 s1/s2 gamma shape', key('l13', 'screens', 2), float(sol[a_])); rec(float(sol[l_]) == 0.5, 'l13 s1 rate 0.5')
for lam, why in ((2, (12, 3)), (0.25, (1.5, 24))):
    a = 6 * lam
    rec((a, a / lam ** 2) == why, f'l13 s1 why lam={lam}')
wrongs('l13', 'screens', 2, {'inverted': 12 / 36, 'divided': 6 / 0.5})
# s4 uniform: exact by order statistics (Beta) and by simulation
n = 10
mse_mom = 4 * (1 / 12) / n
mx = stats.beta(n, 1)
mse_mle = mx.var() + (mx.mean() - 1) ** 2
near('l13 s4 mse 2xbar = 1/30', 1 / 30, mse_mom, 1e-12); near('l13 s4 mse max = 1/66', 1 / 66, mse_mle, 1e-12)
near('l13 s4 ratio', key('l13', 'screens', 4), mse_mom / mse_mle)
u = rng.random((400000, 10))
near('l13 s4 ratio by simulation', 2.2, np.mean((2 * u.mean(1) - 1) ** 2) / np.mean((u.max(1) - 1) ** 2), 0.04)
wrongs('l13', 'screens', 4, {'inverted': mse_mle / mse_mom, 'just-one': mse_mom})
stated('l13', '= 0.0152'); near('l13 s4 0.0152', 0.0152, mse_mle)
x, b = sp.symbols('x b', positive=True)
m2 = 2 * sp.integrate(x ** 2 * sp.exp(-x / b) / (2 * b), (x, 0, sp.oo))
rec(sp.simplify(m2 - 2 * b ** 2) == 0, 'l13 s5 Laplace E[X^2] = 2b^2')
near('l13 s5 b', key('l13', 'screens', 5), math.sqrt(2 / 2)); wrongs('l13', 'screens', 5, {'no-half': math.sqrt(2), 'squared': 2})
m, v = 0.52, 0.0016
s_ab = m * (1 - m) / v - 1
near('l13 s9 a', key('l13', 'screens', 9), m * s_ab)
bd = stats.beta(m * s_ab, (1 - m) * s_ab)
near('l13 s9 beta mean', 0.52, bd.mean(), 1e-9); near('l13 s9 beta sd', 0.04, bd.std(), 1e-9)
wrongs('l13', 'screens', 9, {'no-minus-one': m * (s_ab + 1), 'swapped': (1 - m) * s_ab, 'sum': s_ab})
near('l13 q-wait', key('l13', 'quiz', 0), 1 / 4); near('l13 q-gamma', key('l13', 'quiz', 1), 100 / 25)
wrongs('l13', 'quiz', 1, {'rate': 10 / 25, 'inverted': 25 / 100}); near('l13 q-uniform', key('l13', 'quiz', 2), max(2, 3, 4, 11))
rec(2 * np.mean([2, 3, 4, 11]) == 10, 'l13 q-uniform moment estimate 10'); rec(2 * np.mean([1, 2, 9]) == 8, 'l13 s6 moment estimate 8')
import random as _r
_g = _r.Random(7); xs = np.array([_g.gammavariate(3, 2) for _ in range(2000)])
near('l13 s8 seeded shape', 2.9035, xs.mean() ** 2 / xs.var(), 5e-5); near('l13 s8 seeded rate', 0.4911, xs.mean() / xs.var(), 5e-5)
d = np.array([2, 4, 6, 8.]); near('l13 s8 n-1 shape 3.75', 3.75, d.mean() ** 2 / d.var(ddof=1), 1e-9); near('l13 s8 n-1 rate 0.75', 0.75, d.mean() / d.var(ddof=1), 1e-9)
# Gamma MLE differs from moments (q-agree claim), checked on the seeded sample
a_mle = stats.gamma.fit(xs, floc=0)[0]
rec(abs(a_mle - xs.mean() ** 2 / xs.var()) > 1e-3, 'l13 q-agree: Gamma MLE shape differs from the moment shape')

# ================================================================ l14 sufficiency
p = 0.7
near('l14 s1 one order', 0.00222, p ** 7 * (1 - p) ** 3, 5e-6); near('l14 s1 seven wins', 0.2668, stats.binom.pmf(7, 10, p), 5e-5)
near('l14 s1 caption at 0.5', 0.1172, stats.binom.pmf(7, 10, 0.5), 5e-5); near('l14 s1 one order at 0.5', 0.00098, 0.5 ** 10, 5e-6)
near('l14 s2 orders', key('l14', 'screens', 2), math.comb(10, 6)); wrongs('l14', 'screens', 2, {'seven': math.comb(10, 7), 'all': 2 ** 10})
grid = np.linspace(0.3, 0.9, 13); one = grid ** 7 * (1 - grid) ** 3
rec(not np.all(np.diff(one) > 0), 'l14 s1 NOTE: chance of one order is not increasing on the whole slider (peaks at 0.7)')
near('l14 s6 var K/10', key('l14', 'screens', 6), stats.binom(10, 0.6).var() / 100); wrongs('l14', 'screens', 6, {'one-trade': 0.24, 'n-squared': 0.24 / 100})
tr = rng.random((200000, 10)) < 0.6; K = tr.sum(1)
for k in (4, 6, 8):
    near(f'l14 s6 E[X1 | K={k}] by simulation', k / 10, tr[K == k, 0].mean(), 0.01)
near('l14 s9 Monday mean', 0.005, 1.95 / 390, 1e-9)
near('l14 q-same-total', key('l14', 'quiz', 1), 5 / sum([0.1, 0.2, 0.2, 0.5, 1.5])); near('l14 q-rb', key('l14', 'quiz', 2), 0.25 / 20)
wrongs('l14', 'quiz', 2, {'none': 0.25, 'n2': 0.25 / 400})

# ================================================================ l15 Fisher information
ell = lambda k, nn, q: k * math.log(q) + (nn - k) * math.log(1 - q)
near('l15 s0 fall A', 0.216, ell(7, 10, 0.7) - ell(7, 10, 0.6), 5e-4); near('l15 s0 fall B', 2.160, ell(70, 100, 0.7) - ell(70, 100, 0.6), 5e-4)
q = sp.symbols('q', positive=True)
score = sp.diff(7 * sp.log(q) + 3 * sp.log(1 - q), q)
near('l15 s1 score', key('l15', 'screens', 1), float(score.subs(q, 0.6))); wrongs('l15', 'screens', 1, {'sign': -4.1667, 'plus': 7 / 0.6 + 3 / 0.4})
X = sp.symbols('X')
lb = X * sp.log(q) + (1 - X) * sp.log(1 - q)
info_b = sum((sp.diff(lb, q).subs(X, xv)) ** 2 * (q if xv == 1 else 1 - q) for xv in (0, 1))
rec(sp.simplify(info_b - 1 / (q * (1 - q))) == 0, 'l15 s2 Var(S) = 1/(p(1-p)) for one trade')
info_b2 = -sum(sp.diff(lb, q, 2).subs(X, xv) * (q if xv == 1 else 1 - q) for xv in (0, 1))
rec(sp.simplify(info_b2 - info_b) == 0, 'l15 s2 two forms agree for one trade')
near('l15 s2 info', key('l15', 'screens', 2), 100 / 0.21); wrongs('l15', 'screens', 2, {'one': 1 / 0.21, 'binvar': 21, 'inv': 0.21 / 100})
near('l15 s2 ten trades 47.62', 47.62, 10 / 0.21)
# s3 table by Var(score), the other form from the one the screen uses
mu, sg, lam, t = sp.symbols('mu sigma lam t', positive=True)
xr = sp.symbols('xr', real=True)
fn = sp.exp(-(xr - mu) ** 2 / (2 * sg ** 2)) / sp.sqrt(2 * sp.pi * sg ** 2)
In = sp.simplify(sp.integrate(sp.diff(sp.log(fn), mu) ** 2 * fn, (xr, -sp.oo, sp.oo)))
fe = lam * sp.exp(-lam * x)
Ie = sp.simplify(sp.integrate(sp.diff(sp.log(fe), lam) ** 2 * fe, (x, 0, sp.oo)))
kk = sp.symbols('k', integer=True, nonnegative=True)
Ip = sp.simplify(sp.summation((kk / lam - 1) ** 2 * sp.exp(-lam) * lam ** kk / sp.factorial(kk), (kk, 0, sp.oo)))
cells = [r[3]['answer'] for r in W('l15', 'screens', 3)['rows']]
near('l15 s3 normal', cells[0], float(In.subs(sg, 2))); near('l15 s3 exponential', cells[1], float(Ie.subs(lam, 2))); near('l15 s3 Poisson', cells[2], float(Ip.subs(lam, 2)))
near('l15 s4 se', key('l15', 'screens', 4), math.sqrt(0.21 / 100)); wrongs('l15', 'screens', 4, {'var': 0.0021, 'no-n': math.sqrt(0.21), 'info': 476.19})
near('l15 s4 lower line', 0.654, 0.7 - math.sqrt(0.0021), 5e-4); near('l15 s4 upper line', 0.746, 0.7 + math.sqrt(0.0021), 5e-4)
f0 = sp.exp(-xr ** 2 / (2 * sg ** 2)) / (sp.sqrt(2 * sp.pi) * sg)
Is = sp.simplify(sp.integrate(sp.diff(sp.log(f0), sg) ** 2 * f0, (xr, -sp.oo, sp.oo)))
rec(sp.simplify(Is - 2 / sg ** 2) == 0, 'l15 s5 I(sigma) = 2/sigma^2 as Var(S)')
rec(sp.simplify(sp.diff(-sp.log(sg) - xr ** 2 / (2 * sg ** 2), sg, 2) - (1 / sg ** 2 - 3 * xr ** 2 / sg ** 4)) == 0, 'l15 s5 second derivative as printed')
near('l15 s5 se', key('l15', 'screens', 5), 1 / math.sqrt(504)); wrongs('l15', 'screens', 5, {'no-two': 1 / math.sqrt(252), 'var': 1 / 504})
z = rng.standard_normal((40000, 252)); sig_hat = np.sqrt((z ** 2).mean(1))
near('l15 s5 se of sigma-hat by simulation', 0.0445, sig_hat.std(), 0.001)
near('l15 s7 se of variance by simulation', 0.0891, (z ** 2).mean(1).std(), 0.002)
v_ = sp.symbols('v', positive=True)
fv = sp.exp(-xr ** 2 / (2 * v_)) / sp.sqrt(2 * sp.pi * v_)
Iv = sp.simplify(sp.integrate(sp.diff(sp.log(fv), v_) ** 2 * fv, (xr, -sp.oo, sp.oo)))
rec(sp.simplify(Iv - 1 / (2 * v_ ** 2)) == 0, 'l15 s7 I(sigma^2) = 1/(2 sigma^4) directly')
near('l15 s7 se', key('l15', 'screens', 7), math.sqrt(2 / 252)); wrongs('l15', 'screens', 7, {'used-sigma': 1 / math.sqrt(504), 'no-chain': 1 / math.sqrt(504) / 2})
near('l15 s6 uniform score mean', key('l15', 'screens', 6), -1 / 2)
um = 2 * rng.random((100000, 50)).max(1); um2 = 2 * rng.random((100000, 200)).max(1)
near('l15 s6 uniform MLE error shrinks like 1/n (ratio of sds, n 50 to 200)', 4.0, um.std() / um2.std(), 0.15)
near('l15 s10 days', key('l15', 'screens', 10), 1 / (2 * 0.05 ** 2)); wrongs('l15', 'screens', 10, {'no-two': 1 / 0.05 ** 2, 'no-root': 1 / (2 * 0.05)})
near('l15 q-poisson-se', key('l15', 'quiz', 0), math.sqrt(4 / 25)); near('l15 q-exp-se', key('l15', 'quiz', 2), 2 / math.sqrt(100))
wrongs('l15', 'quiz', 2, {'var': 0.04, 'poisson': math.sqrt(2 / 100)})
ex = rng.exponential(1 / 2, (60000, 100)); near('l15 q-exp-se by simulation', 0.2, (1 / ex.mean(1)).std(), 0.01)
# q-overlap: 250 overlapping 5-day returns need 254 daily returns (255 prices); se understated by about sqrt 5
d5 = rng.standard_normal((40000, 254)); c5 = np.cumsum(d5, 1)
r5 = np.concatenate([c5[:, 4:5], c5[:, 5:] - c5[:, :-5]], 1)
rec(r5.shape[1] == 250, 'l15 q-overlap: 254 daily returns give 250 five-day returns')
naive = r5.std(1).mean() / math.sqrt(250)
near('l15 q-overlap se understated by about sqrt 5', math.sqrt(5), r5.mean(1).std() / naive, 0.12)
rec('254 daily prices' not in RAW['l15'], 'l15 q-overlap: "254 daily prices" give 253 daily returns and 249 five-day returns, not 250')
_g = _r.Random(1); est = [sum(1 for _ in range(100) if _g.random() < 0.7) / 100 for _ in range(2000)]
near('l15 s9 simulated spread 0.0474', 0.0474, float(np.std(est)), 5e-5)

# ================================================================ l16 Cramér-Rao
Xn = np.random.default_rng(2016).standard_normal((2000, 101))
sds = (Xn.mean(1).std(), np.median(Xn, 1).std(), ((Xn[:, 0] + Xn[:, -1]) / 2).std())
for lab, st, mine in zip(('mean', 'median', 'ends'), (0.100, 0.126, 0.715), sds):
    near(f'l16 s0 sd of {lab} (author seed)', st, mine, 6e-4)
near('l16 s2 simulated variance of mean', 0.0101, sds[0] ** 2, 6e-5); near('l16 s2 simulated variance of median', 0.0160, sds[1] ** 2, 6e-5)
near('l16 s3 simulated ratio 1.59', 1.59, sds[1] ** 2 / sds[0] ** 2, 6e-3)
big = rng.standard_normal((40000, 101))
near('l16 s0 sd of median, reader seed', 0.1241, np.median(big, 1).std(), 0.002); near('l16 s0 sd of ends, exact 1/sqrt2', 0.7071, 1 / math.sqrt(2), 1e-4)
near('l16 s2 bound', key('l16', 'screens', 2), 1 / 101); wrongs('l16', 'screens', 2, {'sd': 1 / math.sqrt(101), 'info': 101})
near('l16 s3 observations', key('l16', 'screens', 3), 101 * math.pi / 2, 0.06); wrongs('l16', 'screens', 3, {'inverse': 101 * 2 / math.pi, 'same': 101})
near('l16 s3 efficiency 0.6366', 0.6366, 2 / math.pi); near('l16 s3 bar 0.0156', 0.0156, math.pi / 2 / 101)
# exponential: sum ~ Gamma(n, rate lam); moments of 1/sum by SciPy's inverse gamma
n, lam_ = 10, 2.0
ig = stats.invgamma(n, scale=lam_)
near('l16 s4 E[1/xbar]', key('l16', 'screens', 4), n * ig.mean()); wrongs('l16', 'screens', 4, {'unbiased': 2, 'n-plus': 20 / 11})
near('l16 s5 unbiased mean', 2.0, (n - 1) * ig.mean(), 1e-9); near('l16 s5 variance 0.5', 0.5, (n - 1) ** 2 * ig.var(), 1e-9); near('l16 s5 bound 0.4', 0.4, lam_ ** 2 / n, 1e-12)
near('l16 s5 efficiency', key('l16', 'screens', 5), (lam_ ** 2 / n) / ((n - 1) ** 2 * ig.var())); wrongs('l16', 'screens', 5, {'inverted': 1.25, 'diff': 0.1})
ch = stats.chi2(n - 1)                                       # SS / sigma^2 ~ chi2(n - 1)
near('l16 s5 var s^2 = 2/9', 2 / 9, ch.var() / (n - 1) ** 2, 1e-12)
mse = lambda dv: ch.var() / dv ** 2 + (ch.mean() / dv - 1) ** 2
near('l16 s6 MSE n+1', 0.1818, mse(n + 1)); near('l16 s6 MSE n-1', 0.2222, mse(n - 1)); near('l16 s6 mean 9/11', 9 / 11, ch.mean() / (n + 1), 1e-12)
rec(mse(n + 1) < 2 / n < mse(n - 1), 'l16 s6 order: MSE(n+1) < bound < MSE(n-1)'); near('l16 s6 MSE n+1 = 2/(n+1)', 2 / (n + 1), mse(n + 1), 1e-12)
near('l16 s9 days', key('l16', 'screens', 9), (2 / 0.04) ** 2); near('l16 s9 years 9.9', 9.9, 2500 / 252, 0.05); wrongs('l16', 'screens', 9, {'no-square': 50, 'no-two': 625})
ub = stats.beta(10, 1)
near('l16 q-uniform variance 1/120', 1 / 120, (11 / 10) ** 2 * ub.var(), 1e-12); near('l16 q-uniform unbiased', 1.0, 11 / 10 * ub.mean(), 1e-12)
near('l16 q-hit', key('l16', 'quiz', 1), 0.25 / 100); near('l16 q-vol-bound', key('l16', 'quiz', 2), 2 / 50); wrongs('l16', 'quiz', 2, {'sigma': 1 / 100, 'sd': 0.2})
near('l16 q-vol-bound attained: Var(mean of squares)', 0.04, stats.chi2(50).var() / 50 ** 2, 1e-12)
# q-attain: exponential MLE misses the bound at finite n
rec(n ** 2 * ig.var() > lam_ ** 2 / n, 'l16 q-attain: Var(1/xbar) above the bound')

# ================================================================ l17 likelihood-ratio tests
B0, B1 = stats.binom(20, 0.5), stats.binom(20, 0.6)
near('l17 s0 ratio', key('l17', 'screens', 0), B1.pmf(15) / B0.pmf(15)); wrongs('l17', 'screens', 0, {'inverse': B0.pmf(15) / B1.pmf(15), 'ten': B1.pmf(10) / B0.pmf(10)})
rat = [B1.pmf(k) / B0.pmf(k) for k in range(21)]
near('l17 s1 first above 1', key('l17', 'screens', 1), next(k for k in range(21) if rat[k] > 1)); near('l17 s1 ratio at 11', 0.997, rat[11]); near('l17 s1 ratio at 12', 1.496, rat[12]); near('l17 s1 at 8', 0.2955, rat[8], 5e-5)
near('l17 s2 size', 0.0207, B0.sf(14)); near('l17 s2 size k>=14', 0.0577, B0.sf(13)); near('l17 s2 power', key('l17', 'screens', 2), B1.sf(14))
wrongs('l17', 'screens', 2, {'size': B0.sf(14), 'beta': B1.cdf(14), 'fourteen': B1.sf(13)})
near('l17 s3 low size', 0.0207, B0.cdf(5)); near('l17 s3 low power', 0.0016, B1.cdf(5)); near('l17 s3 six power', 0.0467, 0.6 ** 6); near('l17 s3 six size', 0.0156, 0.5 ** 6)
# Neyman-Pearson by brute force over the count: no region of size <= 0.0207 beats k >= 15
order = sorted(range(21), key=lambda k: -rat[k]); best = 0; size = 0
for k in order:
    if size + B0.pmf(k) <= B0.sf(14) + 1e-12:
        size += B0.pmf(k); best += B1.pmf(k)
near('l17 s2 most powerful region of that size has power 0.1256', 0.1256, best)
tot, nn, l0 = 120, 50, 2.0
pois = lambda L: stats.poisson.logpmf(np.array([2] * 30 + [3] * 20), L).sum()
lr = 2 * (pois(2.4) - pois(l0))
near('l17 s4 statistic', key('l17', 'screens', 4), lr); near('l17 s4 p', 0.0526, stats.chi2.sf(lr, 1)); near('l17 s4 cut-off', 3.841, stats.chi2.ppf(0.95, 1))
wrongs('l17', 'screens', 4, {'no-two': lr / 2, 'no-drift': 2 * 120 * math.log(1.2)})
z0 = 0.4 / math.sqrt(2 / 50); z1 = 0.4 / math.sqrt(2.4 / 50)
near('l17 s5 z null', 2.0, z0, 1e-9); near('l17 s5 p null', 0.0455, 2 * stats.norm.sf(z0)); near('l17 s5 z est', 1.826, z1); near('l17 s5 p est', 0.0679, 2 * stats.norm.sf(z1))
near('l17 s6 df', key('l17', 'screens', 6), 4 - 3)
near('l17 s7 chance 0.167', 0.167, 0.2 / 1.2)
# s8: -2 ln Lambda = z^2 on a random sample
smp = rng.normal(0.3, 2, 40); zz = (smp.mean() - 0) / (2 / math.sqrt(40))
near('l17 s8 -2lnL = z^2', zz ** 2, 2 * (stats.norm.logpdf(smp, smp.mean(), 2).sum() - stats.norm.logpdf(smp, 0, 2).sum()), 1e-9)
# s10: two variances, mean 0; data built to have the stated MLE variances
ll = lambda nobs, v_hat, v: -nobs / 2 * math.log(2 * math.pi * v) - nobs * v_hat / (2 * v)
t10 = 2 * (ll(100, 1.0, 1.0) + ll(100, 1.69, 1.69) - ll(100, 1.0, 1.345) - ll(100, 1.69, 1.345))
near('l17 s10 statistic', key('l17', 'screens', 10), t10); near('l17 s10 p', 0.0091, stats.chi2.sf(t10, 1)); near('l17 s10 first term', 29.639, 100 * math.log(1.345)); near('l17 s10 second term', -22.833, 100 * math.log(1.345 / 1.69))
near('l17 s10 pooled', 1.345, (1.0 + 1.69) / 2, 1e-12); wrongs('l17', 'screens', 10, {'one-term': 100 * math.log(1.345), 'sign': -t10})
near('l17 q-lr-number', key('l17', 'quiz', 3), 2 * (-509.1 + 512.4)); near('l17 q-df', key('l17', 'quiz', 0), 5 - 3); near('l17 q-edge cut-off 5.991', 5.991, stats.chi2.ppf(0.95, 2))
near('l17 s9 size_power(10, .5, .7, 8) size', 0.0547, stats.binom(10, 0.5).sf(7)); near('l17 s9 power', 0.3828, stats.binom(10, 0.7).sf(7))
# q-edge: boundary null. Normal mean constrained to mu >= 0, null mu = 0: -2lnL = max(z,0)^2, a 50:50 mix
zs = rng.standard_normal(400000); tb = np.maximum(zs, 0) ** 2
near('l17 q-edge share of zeros', 0.5, (tb == 0).mean(), 0.005); near('l17 q-edge size of the 3.841 cut on the boundary (too strict)', 0.025, (tb > 3.841).mean(), 0.002)

# ================================================================ l18 chi-squared tests
obs = [62, 45, 48, 41, 54]
x2, pv = stats.chisquare(obs)
rows = W('l18', 'screens', 0)['rows']
for r, o in zip(rows[:5], obs):
    near(f'l18 s0 E {r[0]}', r[2]['answer'], 50); near(f'l18 s0 contribution {r[0]}', r[3]['answer'], (o - 50) ** 2 / 50)
near('l18 s0 total', rows[5][3]['answer'], x2); near('l18 s1 p', key('l18', 'screens', 1), pv)
wrongs('l18', 'screens', 1, {'cdf': 1 - pv, 'one-df': stats.chi2.sf(5.4, 1)})
near('l18 s1 start caption', 0.0497, stats.chi2.sf(9.5, 4)); near('l18 s1 cut-off', 9.488, stats.chi2.ppf(0.95, 4))
xx = sp.symbols('xx', positive=True)
rec(sp.simplify(sp.integrate(x / 4 * sp.exp(-x / 2), (x, xx, sp.oo)) - sp.exp(-xx / 2) * (1 + xx / 2)) == 0, 'l18 s1 chi2_4 tail formula')
near('l18 s2 Monday z', 1.897, (62 - 50) / math.sqrt(250 * 0.2 * 0.8))
g, gp = stats.power_divergence(obs, lambda_='log-likelihood')
near('l18 s3 G', key('l18', 'screens', 3), g); near('l18 s3 p', 0.2568, gp); wrongs('l18', 'screens', 3, {'half': g / 2, 'abs': 2 * sum(abs(o * math.log(o / 50)) for o in obs)})
shown = [13.337, -4.741, -1.959, -8.136, 4.156]
for s_, o in zip(shown, obs):
    near(f'l18 s3 table entry {o}', s_, o * math.log(o / 50))
w3 = W('l18', 'screens', 3)
from_table = 2 * round(sum(shown), 3)
rec(within(from_table, w3['answer'], w3['tol']), 'l18 s3 the table column, added and doubled (5.314), is accepted')
rec(abs(from_table - w3['answer']) < 0.8 * w3['tol']['abs'], 'l18 s3 NOTE: 5.314 from the printed column sits on the edge of the tolerance 0.003', f'gap {from_table - w3["answer"]:.4f}')
rec(abs(sum(shown) - 2.657) < 1e-9 and abs(g / 2 - 2.6556) < 5e-5, 'l18 s3 hint sum 2.657 (rounded entries) against feedback 2.6556 (exact): both true')
t22 = [[70, 50], [50, 70]]
c = stats.chi2_contingency(t22, correction=False)
near('l18 s4 X2', key('l18', 'screens', 4), c[0]); near('l18 s4 p', 0.0098, c[1]); wrongs('l18', 'screens', 4, {'one': 100 / 60, 'no-e': 400})
pp = 120 / 240; z2 = (70 / 120 - 50 / 120) / math.sqrt(pp * (1 - pp) * (2 / 120))
near('l18 s4 two-proportion z', 2.582, z2); near('l18 s4 z squared', c[0], z2 ** 2, 1e-9)
t32 = [[45, 35], [60, 60], [15, 25]]
c = stats.chi2_contingency(t32, correction=False)
near('l18 s5 X2', key('l18', 'screens', 5), c[0]); near('l18 s5 p', 0.1534, c[1]); rec(c[2] == 2, 'l18 s5 df 2'); wrongs('l18', 'screens', 5, {'no-stress': 1.25, 'half': 1.875})
po = [30, 62, 56, 32, 20]; pe = [200 * stats.poisson.pmf(k, 1.8) for k in range(4)] + [200 * stats.poisson.sf(3, 1.8)]
for st, mine in zip([33.06, 59.51, 53.56, 32.13, 21.74], pe):
    near('l18 s6 expected', st, mine)
x6 = sum((o - e) ** 2 / e for o, e in zip(po, pe))
near('l18 s6 X2', 0.639, x6); near('l18 s6 p', 0.887, stats.chi2.sf(x6, 3)); near('l18 s6 df', key('l18', 'screens', 6), 5 - 1 - 1)
c10 = stats.chi2_contingency([[700, 500], [500, 700]], correction=False)
near('l18 s7 tenfold', 66.67, c10[0])
fills = [112, 95, 88, 120, 85]; part = [22, 15, 28, 20, 15]; full = [f - q_ for f, q_ in zip(fills, part)]
r10 = W('l18', 'screens', 10)['rows']
e1 = stats.chisquare(fills); e2 = stats.chi2_contingency([full, part], correction=False)
near('l18 s10 even X2', r10[0][1]['answer'], e1[0]); near('l18 s10 even p', 0.052, e1[1]); near('l18 s10 indep X2', r10[1][1]['answer'], e2[0]); near('l18 s10 indep p', 0.043, e2[1])
rec(e2[2] == 4 == r10[1][2]['answer'] == r10[0][2]['answer'], 'l18 s10 both df 4'); near('l18 s10 venue C 32%', 0.32, 28 / 88, 0.005)
near('l18 s10 wrong partial-only', 7.9, sum((o - e) ** 2 / e for o, e in zip(part, e2[3][1])), 0.02); near('l18 s10 wrong half-e', 4.69, sum((o - 100) ** 2 / 200 for o in fills), 0.01)
rec(full == [90, 80, 60, 100, 70] and sum(part) == 100 and sum(fills) == 500, 'l18 s10 table totals')
yc = stats.chi2_contingency(t22, correction=True)
near('l18 q-yates', 6.017, yc[0]); near('l18 q-df23', key('l18', 'quiz', 0), (2 - 1) * (3 - 1)); near('l18 q-overlap windows', 1240, 5 * 252 - 19, 5)
# Pearson's limit and the lost degree of freedom, by simulation (Poisson fit on the five cells, grouped MLE approximated by the raw mean)
sim = rng.poisson(1.8, (20000, 200)); lamh = sim.mean(1)
stat = np.zeros(20000)
for k in range(5):
    o = (sim == k).sum(1) if k < 4 else (sim >= 4).sum(1)
    e = 200 * (stats.poisson.pmf(k, lamh) if k < 4 else stats.poisson.sf(3, lamh))
    stat += (o - e) ** 2 / e
near('l18 s6 simulated mean of X2 is near 3, not 4', 3.0, stat.mean(), 0.1)

# ================================================================ review-4
near('rev r-gamma', key('rev', 'items', 0), 16 / 2); near('rev r-se-hit', key('rev', 'items', 2), math.sqrt(0.55 * 0.45 / 400)); wrongs('rev', 'items', 2, {'var': 0.2475 / 400, 'one': math.sqrt(0.2475)})
near('rev r-se-hit nI', 1616.2, 400 / 0.2475, 0.05); near('rev r-se-hit interval half-width', 0.049, 1.96 * math.sqrt(0.2475 / 400))
near('rev r-eff', key('rev', 'items', 3), 0.03 / 0.05)
lrc = 2 * (stats.binom.logpmf(60, 100, 0.6) - stats.binom.logpmf(60, 100, 0.5))
near('rev r-lrt-coin', key('rev', 'items', 4), lrc); near('rev r-lrt-coin p', 0.0448, stats.chi2.sf(lrc, 1)); wrongs('rev', 'items', 4, {'half': lrc / 2, 'wins': 2 * 60 * math.log(1.2)})
c = stats.chi2_contingency([[30, 50, 20], [20, 30, 50]], correction=False)
near('rev r-chi-23', key('rev', 'items', 5), c[0]); near('rev r-chi-23 p', 0.00005, c[1], 5e-6); wrongs('rev', 'items', 5, {'on-row': c[0] / 2, 'no-e': 700})
sm = rng.normal(0.2, 1, 30)
near('rev r-np likelihood ratio form', 30 * (0.5 * sm.mean() - 0.125), stats.norm.logpdf(sm, 0.5, 1).sum() - stats.norm.logpdf(sm, 0, 1).sum(), 1e-9)
near('rev r-rb-exp', key('rev', 'items', 7), 4 / 8); near('rev r-param', key('rev', 'items', 8), 2 / math.sqrt(50)); wrongs('rev', 'items', 8, {'rate': 0.5 / math.sqrt(50), 'var': 4 / 50})
th = sp.symbols('theta', positive=True); ft = sp.exp(-x / th) / th
rec(sp.simplify(sp.integrate(sp.diff(sp.log(ft), th) ** 2 * ft, (x, 0, sp.oo)) - 1 / th ** 2) == 0, 'rev r-param I(theta) = 1/theta^2')
e8 = rng.exponential(2, (100000, 8)); T8 = e8.sum(1); sel = (T8 > 15.5) & (T8 < 16.5)
near('rev r-rb-exp E[X1 | total near 16] = 2 by simulation', 2.0, e8[sel, 0].mean(), 0.05)

# ================================================================ homework-4
near('hw h-rb-zero', key('hw', 'items', 0), stats.binom.pmf(0, 10, 1 / 5)); wrongs('hw', 'items', 0, {'plugin': math.exp(-2), 'one-fifth': 0.2, 'wrong-power': 0.8 ** 5})
pz = rng.poisson(2.0, (300000, 5)); Tz = pz.sum(1)
near('hw h-rb-zero P(X1 = 0 | T = 10) by simulation', 0.1074, (pz[Tz == 10, 0] == 0).mean(), 0.006)
near('hw h-rb-zero unbiased: E[(4/5)^T] = e^-lam', math.exp(-2), (0.8 ** Tz).mean(), 0.001)
rec(np.exp(-pz.mean(1)).mean() > math.exp(-2), 'hw h-rb-zero plug-in biased upwards')
near('hw h-mom-negative', key('hw', 'items', 1), 1 - 5 / 4); near('hw h-mom-negative N', -16, 4 / (1 - 5 / 4), 1e-9)
mn = 20 * rng.exponential(3.0, (200000, 20)).min(1)
near('hw h-eff-min unbiased by simulation', 3.0, mn.mean(), 0.03); near('hw h-eff-min variance theta^2', 9.0, mn.var(), 0.2); near('hw h-eff-min', key('hw', 'items', 2), 1 / 20)
wrongs('hw', 'items', 2, {'inv': 20, 'root': 1 / math.sqrt(20)})
mxl = lambda nobs, xbar, mean: -nobs * math.log(mean) - nobs * xbar / mean
he = 2 * (mxl(40, 2, 2) + mxl(60, 3, 3) - mxl(40, 2, 2.6) - mxl(60, 3, 2.6))
near('hw h-lrt-exp', key('hw', 'items', 3), he); near('hw h-lrt-exp p', 0.0507, stats.chi2.sf(he, 1)); near('hw h-lrt-exp pooled', 2.6, (40 * 2 + 60 * 3) / 100, 1e-12)
wrongs('hw', 'items', 3, {'half': he / 2, 'one-term': 2 * 40 * math.log(1.3), 'sign': -he}); near('hw h-lrt-exp 0.2624', 0.2624, math.log(1.3)); near('hw h-lrt-exp 0.1431', 0.1431, -math.log(2.6 / 3))
c_ = stats.norm.ppf(0.95) / 4
near('hw h-np-normal', key('hw', 'items', 6), stats.norm.sf(c_, 0.5, 0.25), 2e-4); wrongs('hw', 'items', 6, {'size': 0.05, 'beta': stats.norm.cdf(c_, 0.5, 0.25), 'cut': c_})
wnp = W('hw', 'items', 6)
rec(within(stats.norm.cdf(2 - 1.645), wnp['answer'], wnp['tol']) and within(stats.norm.cdf(2 - 1.6449), wnp['answer'], wnp['tol']), 'hw h-np-normal accepts 1.645 and 1.6449')
rec(within(stats.norm.cdf(0.36), wnp['answer'], wnp['tol']) and within(stats.norm.cdf(0.35), wnp['answer'], wnp['tol']), 'hw h-np-normal: a two-place z-table at 0.35 or 0.36 (0.6368, 0.6406) is accepted', 'both rejected at tol 0.001')
# h-analyst
near('hw h-analyst sigma^2/n', 0.00576, 1.44 / 250, 1e-9); near('hw h-analyst median variance', 0.00905, math.pi / 2 * 1.44 / 250)
near('hw h-analyst se median 0.095', 0.095, math.sqrt(math.pi / 2 * 1.44 / 250)); near('hw h-analyst se mean 0.076', 0.076, 1.2 / math.sqrt(250)); near('hw h-analyst se vol 0.054', 0.054, 1.2 / math.sqrt(500))
near('hw h-analyst chi2_7 cut-off', 14.067, stats.chi2.ppf(0.95, 7)); near('hw h-analyst 1/0.3', 3.3, 1 / 0.3, 0.05)
edges = np.linspace(-6, 6, 41); ecount = 250 * np.diff(stats.norm.cdf(edges, 0.05, 1.2))
below1 = int((ecount < 1).sum()); below5 = int((ecount < 5).sum())
rec(below1 == 20, 'hw h-analyst claim 3: "20 cells had expected counts below 1" (content changed from 31)', f'the fitted normal gives {below1} of 40 below 1 and {below5} below 5')
rec(stats.chi2.sf(61.3, 39) < 0.05 and stats.chi2.sf(61.3, 37) < 0.05, 'hw h-analyst 61.3 rejects on 39 and on 37 df')
# h-cr-poisson: the identities of the model answer
lam_s, n_s = 3.0, 12
ps = rng.poisson(lam_s, (300000, n_s)); S = ps.sum(1) / lam_s - n_s; xb = ps.mean(1)
near('hw h-cr-poisson E[S] = 0', 0.0, S.mean(), 0.02); near('hw h-cr-poisson Var(S) = n/lam', n_s / lam_s, S.var(), 0.05); near('hw h-cr-poisson Cov(xbar, S) = 1', 1.0, np.cov(xb, S)[0, 1], 0.01)
near('hw h-cr-poisson Var(xbar) = lam/n', lam_s / n_s, xb.var(), 0.005); rec(np.allclose(xb, lam_s + lam_s / n_s * S), 'hw h-cr-poisson xbar = lam + (lam/n) S')
med = np.median(ps, 1)                                        # another estimator: Cov with S need not be 1 when biased
rec(sum(r['points'] for r in J['hw']['items'][8]['rubric']) == 10 and sum(r['points'] for r in J['hw']['items'][7]['rubric']) == 10, 'hw rubrics total 10 points each')

# ================================================================ tolerance probe: sensible roundings of every numeric key
def numeric_widgets():
    for f in F:
        for where in ('screens', 'quiz', 'items'):
            for i, s in enumerate(J[f].get(where, [])):
                w = s.get('widget') or {}
                if w.get('kind') == 'numeric':
                    yield f, where, i, w


tight = []
for f, where, i, w in numeric_widgets():
    a, tol = w['answer'], w['tol']
    if float(a).is_integer():
        continue
    two_dp = round(a, 2) if abs(a) >= 1 else float(f'{a:.2g}') if abs(a) < 0.1 else round(a, 2)
    three_sf = float(f'{a:.3g}')
    for lab, v in (('2 dp', two_dp), ('3 s.f.', three_sf)):
        if abs(a) >= 1 and lab == '2 dp' and not within(v, a, tol):
            tight.append(f'{f} {where}[{i}] key {a} tol {tol}: {v} ({lab}) rejected')
        if lab == '3 s.f.' and not within(v, a, tol) and abs(a) < 10:
            tight.append(f'{f} {where}[{i}] key {a} tol {tol}: {v} ({lab}) rejected')
tight = sorted(set(tight))
rec(not tight, 'tolerance probe: a 2 dp (keys of 1 or more) or 3 s.f. rounding of the key is rejected', '\n     ' + '\n     '.join(tight))
w10 = W('l17', 'screens', 10)
rec(within(round(29.64 - 22.83, 2), w10['answer'], w10['tol']), 'l17 s10: the accept line\'s own arithmetic, 29.64 - 22.83 = 6.81, is accepted')

print(f'\nread-numbers: {passed} of {passed + failed} checks pass')
sys.exit(1 if failed else 0)
