#!/usr/bin/env python3
"""Concept audit checks for limits-thm level 4 (l14 to l19, review-4, homework-4, problems-4).

Recomputes every graded key, wrong option and slip value by exact integration
(sympy), by closed form (scipy) and by simulation, runs every code solution
against its hidden tests, and tests the level's general claims by Monte Carlo.

Exit 0 on correct content. A check that fails because the content is wrong
stays failing: those are the checks whose names start with "FINDING".
Run: python3 docs/reports/limits-thm-L4-concepts.py
"""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy import stats, integrate, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'limits-thm')
def load(n): return json.load(open(os.path.join(ROOT, n + '.json')))
L14, L15, L16, L17, L18, L19 = (load(n) for n in (
    'l14-joint-densities', 'l15-new-variables', 'l16-adding-densities',
    'l17-smallest-and-largest', 'l18-gamma-beta', 'l19-generating-functions'))
REV, HW, PROB = load('review-4'), load('homework-4'), load('problems-4')

fails, n_checks = [], 0
def check(name, cond):
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(name)
        print('FAIL', name)

def W(node):
    return node['widget']
def key_ok(name, node, value, slips=()):
    """The graded key equals `value` within its tolerance; each slip value equals the stated quantity."""
    w = W(node)
    tol = w.get('tol', {}).get('abs', 1e-9)
    check(name + ' key', abs(w['answer'] - value) <= tol + 1e-12)
    wr = {x['id']: x for x in w.get('wrong', [])}
    for sid, sval in slips:
        check(f'{name} slip {sid}', sid in wr and abs(wr[sid]['value'] - sval) <= max(wr[sid].get('tol', {}).get('abs', 0), 6e-4))
    # no slip value may itself be within tolerance of the key
    for x in w.get('wrong', []):
        if 'value' in x:
            check(f'{name} slip {x["id"]} distinct from key', abs(x['value'] - w['answer']) > tol)

def run_code(name, node):
    w = W(node)
    for i, t in enumerate(w['tests']):
        env = {}
        exec(w['solution'], env)
        if 'setup' in t: exec(t['setup'], env)
        got = eval(t['call'], env)
        exp = t['expect']
        if isinstance(exp, str):          # expected values are stored as Python literals
            exp = eval(exp, {})
        if t['compare'] == 'equal':
            ok = got == exp
        else:
            tol = t.get('tol', {}).get('abs')
            g = got if isinstance(got, (list, tuple)) else [got]
            e = exp if isinstance(exp, (list, tuple)) else [exp]
            ok = len(g) == len(e) and all(
                (abs(a - b) <= tol) if tol is not None else math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
                for a, b in zip(g, e))
        check(f'{name} solution passes test {i}', ok)

def text_of(node):
    return json.dumps(node, ensure_ascii=False)

rng = np.random.default_rng(20261112)
N = 400_000
x, y, t, s, u, v, a = sp.symbols('x y t s u v a', positive=True)
Phi, phi = stats.norm.cdf, stats.norm.pdf

# ---------------------------------------------------------------- l14 joint densities
S = L14['screens']; Q = L14['quiz']
f = 2 * sp.exp(-x - 2 * y)
check('l14 density integrates to 1', sp.integrate(f, (x, 0, sp.oo), (y, 0, sp.oo)) == 1)
pA = sp.integrate(sp.integrate(f, (y, x, sp.oo)), (x, 0, sp.oo))
check('l14 s1 exact 1/3', pA == sp.Rational(1, 3))
key_ok('l14 s1', S[1], 1 / 3, [('half', 0.5), ('other', 2 / 3)])
A = rng.exponential(1, N); B = rng.exponential(1 / 2, N)
check('l14 s1 MC P(A first)=1/3', abs((A < B).mean() - 1 / 3) < 0.004)
p1, p2 = 1 - math.exp(-1), 1 - math.exp(-2)
check('l14 s2 0.6321 0.8647 0.5466 1.4968', all(abs(p - q) < 6e-5 for p, q in
      ((p1, 0.6321), (p2, 0.8647), (p1 * p2, 0.5466))) and abs(0.6321 + 0.8647 - 1.4968) < 1e-9)
check('l14 s3 marginal e^-x', sp.simplify(sp.integrate(f, (y, 0, sp.oo)) - sp.exp(-x)) == 0)
check('l14 s4 marginals 2x and 2(1-y)', sp.integrate(2, (y, 0, x)) == 2 * x and sp.simplify(sp.integrate(2, (x, y, 1)) - 2 * (1 - y)) == 0)
# P(X+Y<=1) on the triangle: region 0<=y<=min(x,1-x)
pe = sp.integrate(2, (y, 0, x), (x, 0, sp.Rational(1, 2))) + sp.integrate(2, (y, 0, 1 - x), (x, sp.Rational(1, 2), 1))
check('l14 s5 exact 1/2', pe == sp.Rational(1, 2))
key_ok('l14 s5', S[5], 0.5, [('area', 0.25), ('all', 1.0)])
check('l14 s6 E[Y|X=x]=x/2', sp.integrate(y * (2 / (2 * x)), (y, 0, x)) == x / 2)
EX = sp.integrate(x * 2, (y, 0, x), (x, 0, 1)); EY = sp.integrate(y * 2, (y, 0, x), (x, 0, 1)); EXY = sp.integrate(x * y * 2, (y, 0, x), (x, 0, 1))
check('l14 s8 2/3 1/3 1/4 1/36', (EX, EY, EXY, EXY - EX * EY) == (sp.Rational(2, 3), sp.Rational(1, 3), sp.Rational(1, 4), sp.Rational(1, 36)))
U = rng.uniform(-1, 1, N)
check('l14 s10 Cov(X,X^2)=0 for U(-1,1)', abs(np.cov(U, U ** 2)[0, 1]) < 0.003)
g = 1 + (2 * x - 1) * (2 * y - 1)
check('l14 s11 FGM density valid, uniform marginals', sp.integrate(g, (x, 0, 1), (y, 0, 1)) == 1 and sp.integrate(g, (y, 0, 1)) == 1 and g.subs({x: 0, y: 1}) == 0)
check('l14 s11 exact 5/16', sp.integrate(g, (x, 0, sp.Rational(1, 2)), (y, 0, sp.Rational(1, 2))) == sp.Rational(5, 16))
key_ok('l14 s11', S[11], 5 / 16, [('indep', 0.25), ('half', 0.5)])
check('l14 q0', sp.integrate(x + y, (y, 0, 1)).subs(x, sp.Rational(1, 2)) == 1)
key_ok('l14 q0', Q[0], 1.0, [('half', 0.5)])
for nm, d in (('x+y', x + y), ('4xy', 4 * x * y), ('2-x-y', 2 - x - y), ('3/2(x^2+y^2)', sp.Rational(3, 2) * (x ** 2 + y ** 2))):
    check(f'l14 q1 {nm} is a density on the unit square', sp.integrate(d, (x, 0, 1), (y, 0, 1)) == 1)
    fx, fy = sp.integrate(d, (y, 0, 1)), sp.integrate(d, (x, 0, 1))
    check(f'l14 q1 {nm} factorisation verdict', (sp.simplify(d - fx * fy) == 0) == (nm == '4xy'))
key_ok('l14 q2', Q[2], 0.25, [('x', 0.5)])
key_ok('l14 q3', Q[3], 0.25, [('swap', 0.75), ('half', 0.5)])
# FINDING: "uncorrelated implies independent ... fails for any other pair that is not jointly normal".
# Counterexample: two independent exponentials are not jointly normal, are uncorrelated and are independent.
E1, E2 = rng.exponential(1, N), rng.exponential(1, N)
indep_non_normal = abs(np.corrcoef(E1, E2)[0, 1]) < 0.01 and abs(((E1 > 1) & (E2 > 1)).mean() - math.exp(-2)) < 0.004
check('l14 s10 counterexample exists (independent exponentials)', indep_non_normal)
check('FINDING 1: l14 s10 explain must not say the rule fails for ANY non-normal pair',
      not (indep_non_normal and 'any other pair that is not jointly normal' in S[10]['explain']['text']))

# ---------------------------------------------------------------- l15 transformations
S = L15['screens']; Q = L15['quiz']
check('l15 s0 0.3466', abs(-0.5 * math.log(0.5) - 0.3466) < 5e-5)
Y = -0.5 * np.log(rng.uniform(size=N))
check('l15 s1/s2 MC -ln(U)/2 is Exp(rate 2)', stats.kstest(Y[:50_000], 'expon', args=(0, 0.5)).pvalue > 0.001 and abs(Y.mean() - 0.5) < 0.004)
key_ok('l15 s1', S[1], 2.0, [('mean', 0.5)])
xx = sp.exp(-2 * y)
check('l15 s3 |dx/dy| = 2e^{-2y}', sp.simplify(sp.Abs(sp.diff(xx, y)) - 2 * sp.exp(-2 * y)) == 0)
# FINDING: option `inv` (1/2 e^{-2y}) is said to come from using dy/dx. Using |dy/dx| gives e^{2y}/2.
dy_dx_route = sp.simplify(1 / sp.Abs(sp.diff(xx, y)))          # |dy/dx| in terms of y
inv_opt = sp.exp(-2 * y) / 2
route_matches = sp.simplify(dy_dx_route - inv_opt) == 0
inv_why = next(o for o in W(S[3])['options'] if o['id'] == 'inv')['why']
check('FINDING 5: l15 s3 option inv feedback names a route that gives the option',
      route_matches or 'dy}{dx}' not in inv_why)
key_ok('l15 s4', S[4], phi(math.log(2)) / 2, [('nofac', phi(math.log(2))), ('wayround', 2 * phi(math.log(2)))])
Sln = np.exp(rng.standard_normal(N))
check('l15 s4 MC lognormal density at 2', abs(((Sln > 1.95) & (Sln < 2.05)).mean() / 0.1 - phi(math.log(2)) / 2) < 0.004)
run_code('l15 s5 exp_sample', S[5])
check('l15 s5 e^-2 = 0.1353', abs(math.exp(-2) - 0.1353) < 5e-5)
key_ok('l15 s6', S[6], phi(1), [('one', phi(1) / 2), ('nofac', 2 * phi(1))])
check('l15 s6 chi-square(1) density at 1', abs(stats.chi2.pdf(1, 1) - phi(1)) < 1e-12)
run_code('l15 s9 box_muller', S[9])
key_ok('l15 s10', S[10], Phi(0.5), [('tail', 1 - Phi(0.5)), ('zero', 0.0)])
key_ok('l15 s11', S[11], 100 * (1 - math.exp(-0.1)), [('linear', 10.0), ('prob', 1 - math.exp(-0.1))])
key_ok('l15 q0', Q[0], 0.5, [('one', 1.0), ('two', 2.0)])
key_ok('l15 q1', Q[1], -math.log(0.1) / 0.5, [('u', -math.log(0.9) / 0.5)])
check('l15 q1 slip is the 10th percentile', abs(stats.expon.ppf(0.1, scale=2) - (-math.log(0.9) / 0.5)) < 1e-12)
key_ok('l15 q2', Q[2], 2 * Phi(1) - 1, [('half', Phi(1) - 0.5), ('upper', Phi(1))])
key_ok('l15 q3', Q[3], 2.0, [('one', 1.0), ('four', 4.0)])
# FINDING: "A non-constant monotone g keeps a density". The screen's own g = max(s-105, 0) is
# non-constant and monotone (non-decreasing) and leaves an atom of 0.6915 at 0.
Sx = rng.normal(100, 10, N); pay = np.maximum(Sx - 105, 0)
atom = (pay == 0).mean()
check('l15 s10 MC atom at 0 is Phi(0.5)', abs(atom - Phi(0.5)) < 0.003)
check('FINDING 2: l15 s10 explain must not say every non-constant monotone g keeps a density',
      not (atom > 0.5 and 'A non-constant monotone $g$ keeps a density' in S[10]['explain']['text']))

# ---------------------------------------------------------------- l16 convolution
S = L16['screens']; Q = L16['quiz']
U1, U2 = rng.uniform(size=N), rng.uniform(size=N)
key_ok('l16 s1', S[1], 0.5, [('one', 1.0), ('zero', 0.0)])
key_ok('l16 s2', S[2], 0.875, [('unif', 0.75), ('tail', 0.125)])
check('l16 s2 MC', abs((U1 + U2 <= 1.5).mean() - 0.875) < 0.003)
# the flipped copy f_Y(t - x) of a U(0,1) density is supported on [t-1, t]: its centre is t - 1/2, not t.
# FINDING: prose says the copy is "centred on t".
check('FINDING 6: l16 s1 prose must not say the flipped copy is centred on t',
      'centred on $t$' not in S[1]['prose'])
lam = sp.symbols('lambda', positive=True)
conv = sp.integrate(lam * sp.exp(-lam * x) * lam * sp.exp(-lam * (t - x)), (x, 0, t))
check('l16 s4 convolution lambda^2 t e^{-lambda t}', sp.simplify(conv - lam ** 2 * t * sp.exp(-lam * t)) == 0)
check('l16 s5 tail e^{-2t}(1+2t)', sp.simplify(sp.integrate(4 * x * sp.exp(-2 * x), (x, t, sp.oo)) - sp.exp(-2 * t) * (1 + 2 * t)) == 0)
key_ok('l16 s5', S[5], 3 * math.exp(-2), [('single', math.exp(-2)), ('mid', 2 * math.exp(-2))])
G2 = rng.exponential(0.5, N) + rng.exponential(0.5, N)
check('l16 s5 MC', abs((G2 > 1).mean() - 3 * math.exp(-2)) < 0.004)
run_code('l16 s6 convolve_pmf', S[6])
check('l16 s7 density of U1+U2 at 0.5 is 0.5 (MC)', abs(((U1 + U2 > 0.45) & (U1 + U2 < 0.55)).mean() / 0.1 - 0.5) < 0.01)
# FINDING: option `prod` feedback calls both fills at 0.5 one of the ways "to add to 0.5". 0.5 + 0.5 = 1.
prod_why = next(o for o in W(S[7])['options'] if o['id'] == 'prod')['why']
check('FINDING 7: l16 s7 prod feedback must not present (0.5, 0.5) as a split of 0.5',
      not ('every other way to add to 0.5' in prod_why and 0.5 + 0.5 != 0.5))
key_ok('l16 s8', S[8], 1 - Phi(1), [('sd', 1 - Phi(5 / 7)), ('half', 0.5)])
key_ok('l16 s9', S[9], 0.8 * 0.5 + 0.2 * Phi(1), [('never', 0.5), ('always', Phi(1))])
mv = rng.standard_normal(N) - (rng.uniform(size=N) < 0.2)
check('l16 s9 MC', abs((mv <= 0).mean() - (0.4 + 0.2 * Phi(1))) < 0.003)
ex10 = sp.Rational(1, 2) * sp.integrate(sp.exp(-(2 + a)), (a, -1, 1))
check('l16 s10 exact (e^-1 - e^-3)/2', sp.simplify(ex10 - (sp.exp(-1) - sp.exp(-3)) / 2) == 0)
key_ok('l16 s10', S[10], float(ex10), [('ignore', math.exp(-2)), ('worst', math.exp(-1))])
check('l16 s10 MC (independent desks)', abs((rng.exponential(1, N) - rng.uniform(-1, 1, N) > 2).mean() - float(ex10)) < 0.003)
key_ok('l16 q0', Q[0], 0.125, [('unif', 0.25)])
key_ok('l16 q1', Q[1], 4 / 36, [('one', 1 / 36), ('six', 6 / 36)])
key_ok('l16 q2', Q[2], math.sqrt(13), [('add', 5.0), ('var', 13.0)])
key_ok('l16 q3', Q[3], 2 * math.exp(-2), [('prod', math.exp(-4)), ('single', math.exp(-2))])

# ---------------------------------------------------------------- l17 order statistics
S = L17['screens']; Q = L17['quiz']
D5 = rng.exponential(50, (N // 4, 5)).min(axis=1)
check('l17 s0/s1 MC min of 5 Exp(0.02) is Exp(0.1)', abs(D5.mean() - 10) < 0.15 and stats.kstest(D5[:50_000], 'expon', args=(0, 10)).pvalue > 0.001)
key_ok('l17 s2', S[2], 1 - math.exp(-0.1), [('single', 1 - math.exp(-0.02)), ('five', 5 * (1 - math.exp(-0.02)))])
key_ok('l17 s3', S[3], 0.9 ** 5, [('single', 0.9), ('comp', 1 - 0.9 ** 5)])
key_ok('l17 s4', S[4], 5 * 0.9 ** 4, [('cdf', 0.9 ** 5), ('single', 4.5)])
key_ok('l17 s6', S[6], 20 * 0.3 * 0.7 ** 3, [('half', 10 * 0.3 * 0.7 ** 3), ('nocount', 0.3 * 0.7 ** 3)])
U5 = np.sort(rng.uniform(size=(N // 4, 5)), axis=1)
check('l17 s6 MC second smallest of 5: mean 1/3 and Beta(2,4)', abs(U5[:, 1].mean() - 1 / 3) < 0.003 and stats.kstest(U5[:50_000, 1], 'beta', args=(2, 4)).pvalue > 0.001)
emax20 = integrate.quad(lambda z: z * 20 * phi(z) * Phi(z) ** 19, -10, 10)[0]
check('l17 s7 E[max of 20 normals] = 1.8675', abs(emax20 - 1.8675) < 5e-5)
M20 = rng.standard_normal((N // 4, 20)).max(axis=1)
check('l17 s7 MC', abs(M20.mean() - 1.8675) < 0.01)
check('l17 s7 one in 740, one trial in about 40, rarely below 1',
      abs(1 / (1 - Phi(3)) - 740) < 2 and 35 < 1 / (1 - Phi(3) ** 20) < 42 and Phi(1) ** 20 < 0.04)
F10 = 1 - math.exp(-0.2)
key_ok('l17 s8', S[8], 1 - math.exp(-1), [('maxcdf', F10 ** 5), ('five', 5 * F10)])
run_code('l17 s9 first_default_mc', S[9])
check('l17 s9 exact figures', abs(1 - math.exp(-0.3) - 0.2592) < 5e-5)
key_ok('l17 s10', S[10], 5 / 36, [('both', 1 / 36), ('cdf', 9 / 36)])
# FINDING: slip `cdf` feedback says P(max <= 3) "includes totals of 1 and 2". The quantity is the maximum.
check('FINDING 8: l17 s10 cdf feedback must name maxima, not totals',
      'totals of 1 and 2' not in S[10]['feedback']['byKey']['cdf'])
key_ok('l17 s11', S[11], 1 - Phi(2.1) ** 20, [('single', 1 - Phi(2.1)), ('times', 20 * (1 - Phi(2.1)))])
check('l17 s11 MC', abs((M20 >= 2.1).mean() - (1 - Phi(2.1) ** 20)) < 0.006)
key_ok('l17 q0', Q[0], math.exp(-3), [('one', math.exp(-0.5)), ('time', math.exp(-6))])
key_ok('l17 q1', Q[1], 0.5 ** 4, [('half', 0.5), ('quarter', 0.25)])
key_ok('l17 q2', Q[2], 0.3, [('kn', 1 / 3)])
key_ok('l17 q3', Q[3], Phi(1.5) ** 20, [('single', Phi(1.5)), ('comp', 1 - Phi(1.5) ** 20)])
# ties: independent continuous draws tie with chance 0; dependent continuous ones can tie (X, X).
check('l17 s10 MC ties of independent uniforms have chance 0', (U1 == U2).mean() == 0)

# ---------------------------------------------------------------- l18 gamma and beta
S = L18['screens']; Q = L18['quiz']
gd = sp.Integer(2) ** 3 / sp.gamma(3) * t ** 2 * sp.exp(-2 * t)
check('l18 s0 density 4t^2e^{-2t}, peak at 1, mean 1.5', sp.simplify(gd - 4 * t ** 2 * sp.exp(-2 * t)) == 0
      and sp.solve(sp.diff(gd, t), t) == [1] and sp.integrate(t * gd, (t, 0, sp.oo)) == sp.Rational(3, 2))
G3 = rng.exponential(0.5, (N, 3)).sum(axis=1)
check('l18 s0/s1 MC sum of three Exp(2) is Gamma(3, scale 0.5), var 0.75', abs(G3.var() - 0.75) < 0.01 and stats.kstest(G3[:50_000], 'gamma', args=(3, 0, 0.5)).pvalue > 0.001)
key_ok('l18 s1', S[1], 0.75, [('one', 0.25), ('scaled', 2.25)])
key_ok('l18 s2', S[2], stats.poisson.cdf(2, 4), [('single', math.exp(-4)), ('off', stats.poisson.cdf(3, 4))])
check('l18 s2 Gamma tail equals Poisson sum', abs(stats.gamma.sf(2, 3, scale=0.5) - stats.poisson.cdf(2, 4)) < 1e-12)
check('l18 s3 shape 3 scale 0.5: mean 1.5 and density 0.5413 at 1; scale 2 has mean 6',
      abs(stats.gamma.mean(3, scale=0.5) - 1.5) < 1e-12 and abs(stats.gamma.pdf(1, 3, scale=0.5) - 0.5413) < 5e-5 and stats.gamma.mean(3, scale=2) == 6)
check('l18 s3 Gamma(1/2) = sqrt(pi)', abs(math.gamma(0.5) - math.sqrt(math.pi)) < 1e-12)
check('l18 s4 chi-square(n) is Gamma(n/2, rate 1/2)', all(abs(stats.chi2.pdf(q, n) - stats.gamma.pdf(q, n / 2, scale=2)) < 1e-12 for n in (1, 3, 6, 10) for q in (0.5, 2.0, 7.0)))
key_ok('l18 s4', S[4], stats.chi2.var(6), [('mean', 6.0), ('one', 2.0)])
t5 = 2 * stats.t.sf(2, 5); nz = 2 * stats.norm.sf(2)
check('l18 s5 0.1019 and 0.0455', abs(t5 - 0.1019) < 5e-5 and abs(nz - 0.0455) < 5e-5)
key_ok('l18 s5', S[5], 0.1019 / 0.0455, [('same', 1.0), ('inv', 0.0455 / 0.1019)])
check('l18 s6 0.021, 2.57, 0.0698', abs(2 * stats.norm.sf(2.3) - 0.021) < 6e-4 and abs(stats.t.ppf(0.975, 5) - 2.57) < 5e-3 and abs(2 * stats.t.sf(2.3, 5) - 0.0698) < 5e-5)
X6 = rng.standard_normal((N, 6)); tr = X6.mean(axis=1) / (X6.std(axis=1, ddof=1) / math.sqrt(6))
check('l18 s6 MC t-ratio of six normal returns beyond 2.3', abs((np.abs(tr) > 2.3).mean() - 0.0698) < 0.002)
# the definition t = Z / sqrt(V/n) needs Z and V independent: with V = Z^2 (n = 1) the ratio is +-1.
Z1 = rng.standard_normal(N)
check('l18 s5 dependent Z and V do not give a t (ratio is +-1)', np.allclose(np.abs(Z1 / np.sqrt(Z1 ** 2)), 1))
key_ok('l18 s7', S[7], 1 / 3, [('kn', 0.4), ('half', 0.5)])
cdf_arc = sp.integrate(1 / (sp.pi * sp.sqrt(x * (1 - x))), (x, 0, sp.Rational(1, 4)))
check('l18 s8 exact 1/3', abs(float(cdf_arc) - 1 / 3) < 1e-12 and abs(stats.beta.cdf(0.25, 0.5, 0.5) - 1 / 3) < 1e-12)
key_ok('l18 s8', S[8], 1 / 3, [('unif', 0.25), ('half', 0.5)])
p = sp.symbols('p', positive=True)
post = sp.simplify(p * (1 - p) * p ** 14 * (1 - p) ** 6 / (p ** 15 * (1 - p) ** 7))
check('l18 s9 posterior kernel p^15 (1-p)^7', post == 1)
check('l18 s10 0.9534, mean 0.667, sd 0.094', abs(stats.beta.sf(0.5, 16, 8) - 0.9534) < 5e-5 and abs(stats.beta.mean(16, 8) - 2 / 3) < 1e-12 and abs(stats.beta.std(16, 8) - 0.094) < 5e-4)
key_ok('l18 q0', Q[0], 1.25, [('gap', 0.25), ('twenty', 20.0)])
key_ok('l18 q1', Q[1], math.sqrt(20), [('var', 20.0), ('mean', 10.0)])
check('l18 q2 t5 is lower at the centre', stats.t.pdf(0, 5) < stats.norm.pdf(0))
key_ok('l18 q3', Q[3], 4 / 6, [('raw', 0.75), ('prior', 0.5)])

# ---------------------------------------------------------------- l19 MGFs
S = L19['screens']; Q = L19['quiz']
M = sum(sp.exp(k * t) for k in range(1, 7)) / 6
key_ok('l19 s0', S[0], float(sp.diff(M, t).subs(t, 0)), [('sum', 21.0), ('one', 1.0)])
key_ok('l19 s1', S[1], float(sp.diff(M, t, 2).subs(t, 0)), [('mean', 3.5), ('sq', 12.25)])
check('l19 s1 variance 35/12', sp.diff(M, t, 2).subs(t, 0) - sp.diff(M, t).subs(t, 0) ** 2 == sp.Rational(35, 12))
bm = sum(stats.binom.pmf(k, 3, 0.3) * sp.exp(k * t) for k in range(4))
check('l19 s3 Binomial(3, 0.3) MGF', abs(float((bm - (0.7 + 0.3 * sp.exp(t)) ** 3).subs(t, 0.37))) < 1e-12)
key_ok('l19 s4', S[4], stats.poisson.pmf(3, 3.5), [('add', stats.poisson.pmf(3, 2) + stats.poisson.pmf(3, 1.5)), ('none', math.exp(-3.5))])
check('l19 s4 MC sum of independent Poissons', abs((rng.poisson(2, N) + rng.poisson(1.5, N) == 3).mean() - stats.poisson.pmf(3, 3.5)) < 0.003)
key_ok('l19 s5', S[5], 100 * math.exp(0.05), [('mu', 100 * math.exp(0.03)), ('var', 100 * math.exp(0.07))])
check('l19 s5 MC lognormal mean', abs((100 * np.exp(rng.normal(0.03, 0.2, N))).mean() - 105.13) < 0.15)
check('l19 s7 t^4 coefficients 1/24 and 1/8', sp.series(sp.cosh(t), t, 0, 6).coeff(t, 4) == sp.Rational(1, 24) and sp.series(sp.exp(t ** 2 / 2), t, 0, 6).coeff(t, 4) == sp.Rational(1, 8))
run_code('l19 s9 chernoff', S[9])
env = {}; exec(W(S[9])['solution'], env)
cb, et = env['chernoff_bound'](100, 30), env['exact_tail'](100, 30)
tbest = math.atanh(0.3)
check('l19 s9 best t about 0.31, bound six times exact, bound holds', abs(tbest - 0.31) < 0.005 and 5.5 < cb / et < 6.5 and cb >= et)
check('l19 s9 Chernoff holds on a grid of (n, a)', all(env['chernoff_bound'](n, k) >= env['exact_tail'](n, k) for n in (10, 20, 50, 100) for k in range(0, n + 1, 2)))
rows = {r[0]: r[1] for r in S[10]['canvas']['params']['rows']}
check('l19 s10 table figures', abs(float(rows['Chebyshev, both tails']) - 100 / 900) < 5e-5 and abs(float(rows['Chernoff, $e^{-a^2/2n}$']) - math.exp(-4.5)) < 5e-5
      and abs(float(rows['Chernoff, best $t$']) - cb) < 5e-5 and abs(float(rows['Normal approximation']) - stats.norm.sf(3)) < 5e-6 and abs(float(rows['Exact binomial sum']) - et) < 5e-6)
check('l19 s10 63 times', abs((100 / 900) / et - 63) < 1)
key_ok('l19 q0', Q[0], 3.0, [('p', 0.6), ('n', 5.0)])
key_ok('l19 q1', Q[1], 13.0, [('sd', 5.0), ('sq', 25.0)])
Mp = sp.exp(2 * (sp.exp(t) - 1))
key_ok('l19 q3', Q[3], float(sp.diff(Mp, t, 2).subs(t, 0)), [('mean', 2.0), ('sq', 4.0)])
check('l19 q2 geometric MGF finite below -ln(1-p)', abs(sum(0.3 * math.exp(0.3) * (0.7 * math.exp(0.3)) ** (j - 1) for j in range(1, 4000)) - 0.3 * math.exp(0.3) / (1 - 0.7 * math.exp(0.3))) < 1e-9 and 0.3 < -math.log(0.7))
# summary: min over ALL t is not a bound. For a = -30 the unrestricted minimum is 0.0104 but P(S >= -30) is 0.998.
unres = min(math.exp(30 * tt) * math.cosh(tt) ** 100 for tt in (k / 100 - 3 for k in range(601)))
check('l19 summary: unrestricted min over t is not a bound (needs t > 0)', unres < 0.02 < env['exact_tail'](100, -30))
# FINDING: "For dependent variables E[e^{tX}e^{tY}] does not split." Counterexample: a dependent pair on
# {1,2,3}^2 whose sum has exactly the convolution distribution, so M_{X+Y} = M_X M_Y for every t.
e = sp.Rational(1, 18)
P = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 9)) + sp.Matrix([[0, e, -e], [-e, 0, e], [e, -e, 0]])
px = [sum(P[i, j] for j in range(3)) for i in range(3)]; py = [sum(P[i, j] for i in range(3)) for j in range(3)]
dependent = any(P[i, j] != px[i] * py[j] for i in range(3) for j in range(3))
Mxy = sum(P[i, j] * sp.exp(t * (i + j + 2)) for i in range(3) for j in range(3))
Mx = sum(px[i] * sp.exp(t * (i + 1)) for i in range(3)); My = sum(py[j] * sp.exp(t * (j + 1)) for j in range(3))
splits = sp.simplify(sp.expand(Mxy - Mx * My)) == 0
check('l19 s6 counterexample: dependent pair whose MGF of the sum is the product', dependent and splits and all(q >= 0 for q in P))
check('FINDING 3: l19 s6 explain must not say the product never holds for dependent variables',
      not (dependent and splits and 'For dependent variables $E[e^{tX}e^{tY}]$ does not split.' in S[6]['explain']['text']))

# ---------------------------------------------------------------- review-4
I = {i['id']: i for i in REV['items']}
check('rev r-marginal density valid', sp.integrate(3 * x, (y, 0, x), (x, 0, 1)) == 1)
key_ok('rev r-marginal', I['r-marginal'], float(sp.integrate(3 * x, (y, 0, x), (x, 0, sp.Rational(1, 2)))), [('rect', float(sp.integrate(3 * x, (y, 0, 1), (x, 0, sp.Rational(1, 2))))), ('half', 0.5)])
key_ok('rev r-transform', I['r-transform'], 1 / (2 * 0.4), [('nofac', 1.0), ('inv', 0.8)])
key_ok('rev r-sum-uniform', I['r-sum-uniform'], 0.32, [('unif', 0.4), ('sq', 0.64)])
check('rev r-sum-uniform MC', abs((U1 + U2 > 1.2).mean() - 0.32) < 0.003)
key_ok('rev r-max-exp', I['r-max-exp'], (1 - math.exp(-1.5)) ** 5, [('single', 1 - math.exp(-1.5)), ('comp', 1 - (1 - math.exp(-1.5)) ** 5)])
key_ok('rev r-best10', I['r-best10'], 1 - Phi(2) ** 10, [('single', 1 - Phi(2)), ('times', 10 * (1 - Phi(2)))])
# FINDING: "One in five fund pitches this good is luck." In the item's own model every pitch is skill-free,
# so the share of such pitches that are luck is 1. 0.2056 is P(best >= 2 | no skill), not P(no skill | best >= 2).
M10 = rng.standard_normal((N // 4, 10)).max(axis=1)
share_luck_given_good = 1.0            # all simulated teams are skill-free
check('rev r-best10 MC P(best >= 2 | no skill)', abs((M10 >= 2).mean() - 0.2056) < 0.005)
check('FINDING 4: rev r-best10 explain must not read 0.2056 as the share of good pitches that are luck',
      not (share_luck_given_good == 1.0 and 'One in five fund pitches this good is luck' in I['r-best10']['explain']['text']))
key_ok('rev r-gamma-tail', I['r-gamma-tail'], 4 * math.exp(-3), [('first', math.exp(-3)), ('three', 3 * math.exp(-3))])
key_ok('rev r-mgf-mean', I['r-mgf-mean'], float(sp.diff(2 / (2 - t), t).subs(t, 0)), [('rate', 2.0), ('value', 1.0)])
check('rev r-beta-post Beta(8,4) mean 0.667', abs(stats.beta.mean(8, 4) - 0.667) < 5e-4)

# ---------------------------------------------------------------- homework-4
I = {i['id']: i for i in HW['items']}
h = 8 * x * y
check('hw density valid and marginal 4x^3', sp.integrate(h, (y, 0, x), (x, 0, 1)) == 1 and sp.integrate(h, (y, 0, x)) == 4 * x ** 3)
key_ok('hw h-marginal', I['h-marginal'], 0.5 ** 4, [('twox', 0.25), ('half', 0.5)])
check('hw h-condexp 2x/3', sp.simplify(sp.integrate(y * h / (4 * x ** 3), (y, 0, x)) - 2 * x / 3) == 0)
J = sp.Matrix([[sp.diff(u * v, u), sp.diff(u * v, v)], [sp.diff(u * (1 - v), u), sp.diff(u * (1 - v), v)]]).det()
check('hw h-jacobian |J| = u', sp.simplify(sp.Abs(J) - u) == 0)
key_ok('hw h-jacobian', I['h-jacobian'], 2 * math.exp(-2), [('nojac', math.exp(-2)), ('double', 4 * math.exp(-2))])
Xe, Ye = rng.exponential(1, N), rng.exponential(1, N); Uu, Vv = Xe + Ye, Xe / (Xe + Ye)
check('hw h-jacobian MC U Gamma(2,1), V uniform, uncorrelated', stats.kstest(Vv[:50_000], 'uniform').pvalue > 0.001 and abs(np.corrcoef(Uu, Vv)[0, 1]) < 0.01 and abs(Uu.mean() - 2) < 0.01)
key_ok('hw h-convolve', I['h-convolve'], math.exp(-1) - math.exp(-2), [('single', math.exp(-2)), ('prod', 0.0)])
Sm = rng.exponential(1, N) + rng.uniform(size=N)
check('hw h-convolve MC density at 2', abs(((Sm > 1.95) & (Sm < 2.05)).mean() / 0.1 - (math.exp(-1) - math.exp(-2))) < 0.006)
key_ok('hw h-first-default', I['h-first-default'], 0.5 * (1 - math.exp(-0.3)), [('time', 1 - math.exp(-0.3)), ('share', 0.5)])
T3 = np.column_stack([rng.exponential(1 / r, N) for r in (0.01, 0.02, 0.03)])
first, when = T3.argmin(axis=1), T3.min(axis=1)
check('hw h-first-default MC joint chance and independence of who and when',
      abs(((first == 2) & (when <= 5)).mean() - 0.1296) < 0.003 and abs((first == 2).mean() - 0.5) < 0.004
      and abs((first[when <= 5] == 2).mean() - (first[when > 30] == 2).mean()) < 0.01)
run_code('hw h-order-code', I['h-order-code'])
sd_k = lambda n, k: math.sqrt(k * (n - k + 1) / ((n + 1) ** 2 * (n + 2)))
check('hw h-order-code sd 0.18 is the n=5, k=2 case', abs(sd_k(5, 2) - 0.18) < 0.005)
key_ok('hw h-beta-two-batches', I['h-beta-two-batches'], 14 / 24, [('first', 11 / 16), ('prior', 0.5)])
Mp3 = float(sp.diff(Mp, t, 3).subs(t, 0))
key_ok('hw h-poisson-third', I['h-poisson-third'], Mp3, [('lam3', 8.0), ('second', 6.0)])
check('hw h-poisson-third MC', abs((rng.poisson(2, N).astype(float) ** 3).mean() - 22) < 0.4)
model = I['h-best-of-50']['model']
lf = {
    '0.0047': stats.norm.sf(2.6), '0.208': 1 - Phi(2.6) ** 50, '2.20': stats.norm.ppf(0.5 ** (1 / 50)),
    '2.25': integrate.quad(lambda z: z * 50 * phi(z) * Phi(z) ** 49, -10, 10)[0],
    '0.99980': 0.99 ** (1 / 50), '3.54': stats.norm.ppf(0.99 ** (1 / 50)), '0.0073': stats.t.sf(2.6, 29),
    '0.31': 1 - stats.t.cdf(2.6, 29) ** 50, '2.32': stats.t.ppf(0.5 ** (1 / 50), 29), '4.0': stats.t.ppf(0.99 ** (1 / 50), 29)}
for lit, val in lf.items():
    places = len(lit.split('.')[1])
    check(f'hw longform {lit} appears and is right', lit in model and abs(float(lit) - val) <= 0.6 * 10 ** (-places))
check('hw longform Bonferroni cut-off equals 3.54', abs(stats.norm.isf(0.01 / 50) - 3.54) < 5e-3)

# ---------------------------------------------------------------- problems-4
PI = {i['id']: i for i in PROB['items']}
m = PI['p-machine-faults']['parts']
fm = sp.exp(-y)
check('prob faults density valid, marginal e^-x', sp.integrate(sp.integrate(fm, (y, x, sp.oo)), (x, 0, sp.oo)) == 1 and sp.integrate(fm, (y, x, sp.oo)) == sp.exp(-x))
key_ok('prob faults p2', m[1], 1.5, [('unconditional', 2.0), ('half', 0.25), ('gap-only', 1.0)])
key_ok('prob faults p4', m[3], math.exp(-2), [('second-fault', 3 * math.exp(-2)), ('complement', 1 - math.exp(-2)), ('rate-half', math.exp(-1))])
key_ok('prob faults p5', m[4], 4 * math.exp(-3), [('one-wait', math.exp(-3)), ('complement', 1 - 4 * math.exp(-3)), ('dropped-one', 3 * math.exp(-3))])
Xf = rng.exponential(1, N); Yf = Xf + rng.exponential(1, N)
check('prob faults MC', abs(Yf[(Xf > 0.45) & (Xf < 0.55)].mean() - 1.5) < 0.03 and abs((Yf > 3).mean() - 4 * math.exp(-3)) < 0.003)
k = PI['p-ticket-stages']['parts']
fT = sp.integrate(sp.exp(-x) * sp.Rational(1, 2) * sp.exp(-(t - x) / 2), (x, 0, t))
check('prob ticket density', sp.simplify(fT - (sp.exp(-t / 2) - sp.exp(-t))) == 0 and sp.integrate(sp.exp(-t / 2) - sp.exp(-t), (t, 0, sp.oo)) == 1)
ptail = 2 * math.exp(-5) - math.exp(-10)
key_ok('prob ticket p2', k[1], ptail, [('one-stage', math.exp(-5)), ('complement', 1 - ptail), ('equal-rates', 6 * math.exp(-5))])
Tt = rng.exponential(1, 4 * N) + rng.exponential(2, 4 * N)
check('prob ticket MC tail', abs((Tt > 10).mean() - ptail) < 0.0006)
MT = 1 / ((1 - s) * (1 - 2 * s))
check('prob ticket MGF', abs(float(sp.integrate(sp.exp(sp.Rational(1, 4) * t) * (sp.exp(-t / 2) - sp.exp(-t)), (t, 0, sp.oo)) - MT.subs(s, sp.Rational(1, 4)))) < 1e-12)
sopt = optimize.minimize_scalar(lambda q: math.exp(-10 * q) / ((1 - q) * (1 - 2 * q)), bounds=(1e-6, 0.4999), method='bounded').x
key_ok('prob ticket p4', k[3], sopt, [('other-root', (26 + math.sqrt(116)) / 40), ('repair-only', 0.4), ('triage-only', 0.9)])
bnd = math.exp(-10 * 0.3807) / ((1 - 0.3807) * (1 - 0.7614))
key_ok('prob ticket p5', k[4], bnd, [('repair-s', math.exp(-4) / (0.6 * 0.2)), ('no-mgf', math.exp(-3.807)), ('exact', ptail)])
check('prob ticket bound holds, 11 times, one in 74', bnd > ptail and abs(bnd / 0.0134 - 11) < 0.5 and abs(1 / ptail - 74) < 1)
d = PI['p-dealer-quotes']['parts']
key_ok('prob dealer p1', d[0], 0.8 ** 4, [('one-dealer', 0.8), ('worst', 1 - 0.2 ** 4), ('complement', 1 - 0.8 ** 4)])
key_ok('prob dealer p2', d[1], 0.8, [('one-dealer', 0.5), ('worst', 0.2), ('k-over-n', 0.75)])
key_ok('prob dealer p4', d[3], 0.6, [('k-over-n', 0.75), ('swapped', 0.4), ('one-dealer', 0.5)])
key_ok('prob dealer p5', d[4], stats.beta.sf(0.5, 3, 2), [('three-above', stats.binom.sf(2, 4, 0.5)), ('one-above', 1 - 0.5 ** 4), ('half', 0.5)])
U4 = np.sort(rng.uniform(size=(N, 4)), axis=1)
check('prob dealer MC', abs(U4[:, 3].mean() - 0.8) < 0.002 and abs(U4[:, 2].mean() - 0.6) < 0.002 and abs((U4[:, 2] > 0.5).mean() - 11 / 16) < 0.003)
# FINDING: the explain says X_(3) > 0.5 "exactly when at most 1 of the 4 quotes is below 0.5".
# The right event is "at most 2 below". At 0.5 both counts happen to give matching numbers by symmetry,
# so test the two rules at a threshold of 0.6, where they differ.
c = 0.6
truth = (U4[:, 2] > c).mean()
rule_at_most_2_below = stats.binom.cdf(2, 4, c)
rule_at_most_1_below = stats.binom.cdf(1, 4, c)
check('prob dealer p5 the right rule is at most 2 below', abs(truth - rule_at_most_2_below) < 0.003 and abs(truth - rule_at_most_1_below) > 0.2)
check('FINDING 9: prob dealer p5 explain must not say "at most 1 of the 4 quotes is below"',
      'at most 1 of the 4 quotes is below' not in d[4]['explain']['text'])
e4 = PI['p-part-errors']['parts']
mz2 = integrate.quad(lambda z: math.exp(0.2 * z * z) * phi(z), -30, 30)[0]
check('prob part E[e^{sZ^2}] = (1-2s)^{-1/2}', abs(mz2 - (1 - 0.4) ** -0.5) < 1e-9)
MD = (1 - 2 * s) ** -2
check('prob part moments 4, 24, 8', (sp.diff(MD, s).subs(s, 0), sp.diff(MD, s, 2).subs(s, 0)) == (4, 24))
key_ok('prob part p2', e4[1], 8.0, [('second-moment', 24.0), ('one-term', 2.0), ('sd', math.sqrt(8))])
key_ok('prob part p4', e4[3], stats.chi2.sf(8, 4), [('exponential', math.exp(-4)), ('three-terms', 13 * math.exp(-4)), ('rate-one', 9 * math.exp(-8))])
check('prob part p4 chi-square(4) tail formula', all(abs(stats.chi2.sf(q, 4) - math.exp(-q / 2) * (1 + q / 2)) < 1e-12 for q in (1, 8, 9, 10)))
dmin = next(q for q in range(1, 40) if stats.chi2.sf(q, 4) <= 0.05)
key_ok('prob part p5', e4[4], float(dmin), [('normal', float(math.ceil(4 + 1.645 * math.sqrt(8)))), ('ten-per-cent', 8.0), ('too-far', 11.0)])
check('prob part p5 0.0611 and 0.0404', abs(stats.chi2.sf(9, 4) - 0.0611) < 5e-5 and abs(stats.chi2.sf(10, 4) - 0.0404) < 5e-5)
D4 = (rng.standard_normal((N, 4)) ** 2).sum(axis=1)
check('prob part MC', abs((D4 > 8).mean() - 0.0916) < 0.002 and abs(D4.var() - 8) < 0.1)
# FINDING: slip `power` (1-2s)^{-1/8}: feedback says the exponent was "multiplied by 1/2 again" (that is -1/4).
pw = e4[0]['feedback']['byKey']['power']
check('FINDING 10: prob part p1 power feedback names the slip that gives -1/8',
      not ('multiplied the exponent by $\\tfrac12$ again' in pw and (-0.5) * 0.5 != -1 / 8))

print(f'{n_checks} checks, {len(fails)} failed')
sys.exit(1 if fails else 0)
