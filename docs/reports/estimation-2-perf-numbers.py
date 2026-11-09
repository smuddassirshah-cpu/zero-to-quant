"""Recompute every number in estimation homework-2 item hw2-pareto-tail (performance task, derivation).

Run with the scratchpad venv (numpy, scipy, sympy):
    <venv>/bin/python -I docs/reports/estimation-2-perf-numbers.py      exits 0 when every check passes.
Each claim is checked twice: a closed form (sympy, exact) and an independent route
(numerical quadrature, scipy distributions, or a seeded simulation of the estimator).
It also lists every passing tick set of the rubric and checks none skips a named part.
"""
import itertools, json, math, os, re, sys

import numpy as np
import sympy as sp
from scipy import integrate, optimize, stats

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/estimation/homework-2.json')
doc = json.load(open(HW, encoding='utf-8'))
item = next(i for i in doc['items'] if i['id'] == 'hw2-pareto-tail')
fails = []


def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)


# ---------- shape ----------
rub = item['rubric']
check('performance kind derivation', item.get('performance') == 'derivation' and item.get('kind') == 'longform')
check('rubric 3 to 5 rows summing to 10', 3 <= len(rub) <= 5 and sum(r['points'] for r in rub) == 10)
req = [i for i, r in enumerate(rub) if r.get('required')]
check('required rows 1 to 4, not every row', req == [0, 1, 2, 3])
check('homework item count within 6 to 12', 6 <= len(doc['items']) <= 12, str(len(doc['items'])))
check('no hints, steps, starter, parts', not any(k in item for k in ('hints', 'steps', 'starter', 'parts', 'order', 'derive')))

# ---------- (a) symbolic: likelihood, stationary point, second derivative, ends ----------
a, S, n, y, s, x = sp.symbols('alpha S n y s x', positive=True)
ell = n * sp.log(a) - (a + 1) * S
d1 = sp.diff(ell, a)
d2 = sp.diff(ell, a, 2)
sol = sp.solve(sp.Eq(d1, 0), a)
check('(a) l\'(alpha) = n/alpha - S', sp.simplify(d1 - (n / a - S)) == 0)
check('(a) alpha-hat = n/S', sol == [n / S], str(sol))
check('(a) l\'\'(alpha) = -n/alpha^2', sp.simplify(d2 + n / a**2) == 0)
check('(a) l -> -oo as alpha -> 0+', sp.limit(ell, a, 0, '+') == -sp.oo)
check('(a) l -> -oo as alpha -> oo', sp.limit(ell, a, sp.oo) == -sp.oo)
check('(a) rewrite alpha(n ln a / a - S) - S equals l', sp.simplify(a * (n * sp.log(a) / a - S) - S - ell) == 0)
check('(a) ln(a)/a -> 0', sp.limit(sp.log(a) / a, a, sp.oo) == 0)
# the log-likelihood from the product of densities, on concrete data, two routes
xs = [1.5, 1.2, 3.0, 1.1, 2.4, 1.8]
def ll_prod(al):
    return math.log(math.prod(al * xi ** (-al - 1) for xi in xs))
Sd = sum(math.log(v) for v in xs)
check('(a) product route equals n ln a - (a+1)S at 4 points',
      all(abs(ll_prod(al) - (6 * math.log(al) - (al + 1) * Sd)) < 1e-9 for al in (0.3, 1.0, 1.85, 4.0)))

# ---------- (b) law of Y = ln X ----------
tail = sp.integrate(a * x ** (-a - 1), (x, sp.exp(y), sp.oo))
check('(b) P(Y > y) = exp(-alpha y), sympy', sp.simplify(tail - sp.exp(-a * y)) == 0, str(tail))
for al in (0.7, 1.5, 3.0):
    for yy in (0.1, 0.8, 2.0):
        q = integrate.quad(lambda t: al * t ** (-al - 1), math.exp(yy), np.inf)[0]
        if abs(q - math.exp(-al * yy)) > 1e-8:
            check('(b) tail by quadrature', False, f'{al} {yy} {q}')
check('(b) tail by quadrature at 9 points', True)
rng = np.random.default_rng(20261109)
Y = np.log(stats.pareto.rvs(1.5, size=200_000, random_state=rng))
ks = stats.kstest(Y, 'expon', args=(0, 1 / 1.5))
check('(b) seeded: ln of Pareto(1.5) draws pass a KS test for Exp(1.5)', ks.pvalue > 0.01, f'p = {ks.pvalue:.3f}, mean {Y.mean():.4f} vs {1/1.5:.4f}')

# ---------- (b) E[1/S] = alpha/(n-1) ----------
for m in range(2, 9):
    dens = a**m * s**(m - 1) * sp.exp(-a * s) / sp.factorial(m - 1)
    e = sp.integrate(dens / s, (s, 0, sp.oo))
    if sp.simplify(e - a / (m - 1)) != 0:
        check(f'(b) E[1/S] sympy n={m}', False, str(e))
    # the step: alpha^n/(n-1)! = alpha/(n-1) * alpha^(n-1)/(n-2)!
    if sp.simplify(a**m / sp.factorial(m - 1) - a / (m - 1) * a**(m - 1) / sp.factorial(m - 2)) != 0:
        check(f'(b) factorial step n={m}', False)
    # the remaining integrand is a density (integrates to 1)
    if sp.simplify(sp.integrate(a**(m - 1) * s**(m - 2) * sp.exp(-a * s) / sp.factorial(m - 2), (s, 0, sp.oo)) - 1) != 0:
        check(f'(b) remaining integral 1, n={m}', False)
check('(b) E[1/S] = alpha/(n-1), factorial step and unit integral, sympy n = 2..8', True)
for m, al in ((2, 1.5), (6, 1.5), (6, 2.5), (10, 0.8)):
    q = stats.gamma(m, scale=1 / al).expect(lambda t: 1 / t)
    check(f'(b) E[1/S] by scipy gamma expectation, n={m}, alpha={al}', abs(q - al / (m - 1)) < 1e-7, f'{q:.8f} vs {al/(m-1):.8f}')
# the fact's density is the law of a sum of m exponentials: seeded check
for m in (1, 3, 6):
    Ssim = rng.exponential(1 / 1.5, size=(100_000, m)).sum(axis=1)
    ks = stats.kstest(Ssim, stats.gamma(m, scale=1 / 1.5).cdf)
    check(f'(b) seeded: sum of {m} Exp(1.5) matches the given density', ks.pvalue > 0.01, f'p = {ks.pvalue:.3f}')
# n = 1: E[1/Y] diverges
eps = sp.symbols('epsilon', positive=True)
lower = sp.integrate(a * sp.exp(-a) / y, (y, eps, 1))
check('(b) n = 1: the lower bound alpha e^{-alpha} ln(1/eps) -> oo as eps -> 0', sp.limit(lower, eps, 0, '+') == sp.oo, str(sp.simplify(lower)))
qs = [integrate.quad(lambda t: 1.5 * math.exp(-1.5 * t) / t, 10.0 ** -k, 50, limit=200)[0] for k in (2, 4, 8)]
check('(b) n = 1: quadrature of E[1/Y] from eps grows without bound (eps = 1e-2, 1e-4, 1e-8)', qs[0] < qs[1] < qs[2] and qs[2] - qs[1] > 1.5 * 4 * math.log(10) * math.exp(-1.5), str([round(q, 2) for q in qs]))
check('(b) bound e^{-alpha y} > e^{-alpha} on 0<y<1 (alpha = 1.5, grid)',
      all(math.exp(-1.5 * t) > math.exp(-1.5) for t in np.linspace(1e-6, 1 - 1e-6, 1000)))
# bias and the unbiased multiple, symbolic
Ea = n * a / (n - 1)
check('(b) bias = alpha/(n-1)', sp.simplify(Ea - a - a / (n - 1)) == 0)
check('(b) (n-1)/n alpha-hat has mean alpha', sp.simplify((n - 1) / n * Ea - a) == 0)

# seeded simulation of the bias: the estimator itself, Pareto draws
for nn, al in ((6, 1.5), (6, 2.5), (3, 1.0), (20, 1.8)):
    X = stats.pareto.rvs(al, size=(200_000, nn), random_state=rng)
    est = nn / np.log(X).sum(axis=1)
    unb = (nn - 1) / np.log(X).sum(axis=1)
    target = nn * al / (nn - 1)
    if nn >= 3:
        se = est.std(ddof=1) / math.sqrt(len(est))
        check(f'sim n={nn} alpha={al}: mean MLE {est.mean():.4f} vs n alpha/(n-1) = {target:.4f}', abs(est.mean() - target) < 5 * se, f'se {se:.4f}')
        se2 = unb.std(ddof=1) / math.sqrt(len(unb))
        check(f'sim n={nn} alpha={al}: mean unbiased {unb.mean():.4f} vs {al}', abs(unb.mean() - al) < 5 * se2, f'se {se2:.4f}')

# ---------- (c) the six losses ----------
logs = [math.log(v) for v in xs]
r4 = [round(v, 4) for v in logs]
check('(c) logs to 4 dp', r4 == [0.4055, 0.1823, 1.0986, 0.0953, 0.8755, 0.5878], str(r4))
check('(c) S = 3.2450 (sum of logs and log of product)', round(Sd, 4) == 3.2450 and abs(math.log(math.prod(xs)) - Sd) < 1e-12 and round(sum(r4), 4) == 3.2450, f'{Sd:.6f}')
ah = 6 / Sd
au = 5 / Sd
check('(c) alpha-hat = 1.85', round(ah, 2) == 1.85 and round(6 / 3.2450, 2) == 1.85, f'{ah:.5f}')
check('(c) unbiased = 1.54', round(au, 2) == 1.54 and round(5 / 3.2450, 2) == 1.54, f'{au:.5f}')
opt = optimize.minimize_scalar(lambda al: -ll_prod(al), bounds=(0.01, 20), method='bounded', options={'xatol': 1e-10})
check('(c) numerical maximiser of the product likelihood = 6/S', abs(opt.x - ah) < 1e-6, f'{opt.x:.6f}')
check('(c) 20% high: 6/5 - 1', abs(6 / 5 - 1 - 0.20) < 1e-12)
# tail chance P(X > 10) = 10^-alpha, by the formula and by scipy's Pareto survival function
for al, want in ((ah, 0.014), (au, 0.029), (1.85, 0.014), (1.54, 0.029)):
    p1 = 10 ** (-al)
    p2 = stats.pareto.sf(10, al)
    check(f'(c) 10^-{al:.4f} = {p1:.5f} rounds to {want}', round(p1, 3) == want and abs(p1 - p2) < 1e-12)
check('(c) about half as likely: ratio 0.45 to 0.55', 0.45 < 10 ** (-ah) / 10 ** (-au) < 0.55, f'{10 ** (-ah) / 10 ** (-au):.3f}')
pct = [round(100 * 10 ** (-v), 1) for v in (ah, au)]
check('(c) the chances as 1.4% and 2.9%', pct == [1.4, 2.9], str(pct))

# ---------- the numbers printed in the item ----------
text = item['prompt'] + item['model'] + ' '.join(r['text'] for r in rub)
for token in ['0.4055', '0.1823', '1.0986', '0.0953', '0.8755', '0.5878', '3.2450', '1.85', '1.54', '0.014', '0.029', '20%', '\\tfrac{6}{5}']:
    check(f'printed {token}', token in text)

# ---------- rubric: every passing tick set ----------
pts = [r['points'] for r in rub]
named = {0: '(a) MLE', 1: '(a) maximum check', 2: '(b) law, E[1/S], bias, fix', 3: '(c) numbers'}
passing = []
for k in range(len(rub) + 1):
    for c in itertools.combinations(range(len(rub)), k):
        if sum(pts[i] for i in c) >= 7 and all(i in c for i in req):
            passing.append(c)
for c in passing:
    print('     pass set rows', [i + 1 for i in c], 'points', sum(pts[i] for i in c))
check('every passing set contains every named part', all(all(i in c for i in named) for c in passing), f'{len(passing)} sets')
check('row 5 (optional part) can be left out', any(4 not in c for c in passing))

# ---------- voice ----------
def sentences(t):
    t = re.sub(r'\$\$.*?\$\$', ' MATH ', t, flags=re.S)
    t = re.sub(r'\$[^$]*\$', 'MATH', t)
    out = []
    for line in t.split('\n'):
        out += [p for p in re.split(r'(?<=[.?:])\s+', line.strip()) if p]
    return out
longest = max(len(p.split()) for p in sentences(text))
outside = re.sub(r'\$\$.*?\$\$|\$[^$]*\$', ' ', text, flags=re.S)  # a factorial inside maths is not an exclamation
check('voice: no ! outside maths, no em or en dash', '!' not in outside and '—' not in text and '–' not in text)
check('voice: longest sentence at most 35 words', longest <= 35, str(longest))

print('failures:', len(fails))
sys.exit(1 if fails else 0)
