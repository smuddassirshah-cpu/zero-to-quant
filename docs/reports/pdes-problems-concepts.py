#!/usr/bin/env python3
"""Blind concept audit, pdes problems-1 to problems-3: independent recompute of every key,
slip and stated number. Closed forms by sympy, finite differences by NumPy, Feynman-Kac and
random-walk claims by Monte Carlo and exact binomials. Exits 0 when the content is right.
INFO lines report an `imprecise` finding (true as worded, see the audit); they do not fail.
Run: python docs/reports/pdes-problems-concepts.py
"""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy.stats import norm, binom
from scipy.integrate import quad
from scipy.linalg import solve_banded

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'pdes')
fails = []
n_checks = 0


def ok(name, cond, detail=''):
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(name)
    detail = str(detail)
    print(('ok   ' if cond else 'FAIL ') + name + (' | ' + detail if detail else ''))


def close(a, b, tol):
    return abs(a - b) <= tol


def load(n):
    with open(os.path.join(ROOT, 'problems-%d.json' % n)) as f:
        d = json.load(f)
    return {it['id']: it['parts'] for it in d['items']}


def W(parts, i):
    return parts[i]['widget']


def key(name, parts, i, value, slips=None, shown=None):
    """value: independent recompute. shown: what a learner types after the asked rounding
    (or from the carried rounded inputs); it must be accepted. slips: {id: recomputed value}."""
    w = W(parts, i)
    tol = w['tol']['abs']
    ok('%s part %d key %s' % (name, i + 1, w['answer']), close(value, w['answer'], max(tol, 1e-9)), 'recomputed %.8g' % value)
    for s in ([shown] if isinstance(shown, (int, float)) else (shown or [])):
        ok('%s part %d accepts typed %.8g' % (name, i + 1, s), close(s, w['answer'], tol + 1e-12))
    got = {x['id']: x for x in w.get('wrong', [])}
    slips = slips or {}
    ok('%s part %d every slip recomputed' % (name, i + 1), set(got) == set(slips), sorted(set(got) ^ set(slips)))
    for sid, v in slips.items():
        if sid in got:
            x = got[sid]
            ok('%s part %d slip %s = %s' % (name, i + 1, sid, x['value']), close(v, x['value'], max(x['tol']['abs'], 1e-9)), 'recomputed %.8g' % v)
            ok('%s part %d slip %s clear of key' % (name, i + 1, sid), abs(x['value'] - w['answer']) > x['tol']['abs'] + tol)


rng = np.random.default_rng(20261126)
P = norm.cdf

# ---------------------------------------------------------------- problems-1
p1 = load(1)
n = 'p-tick-spread'; q = p1[n]
dx, dt = 0.4, 0.1
D = dx**2 / (2 * dt)
key(n, q, 0, D, {'no-half': dx**2 / dt, 'unsquared': dx / (2 * dt)})
sd = math.sqrt(2 * D * 60)
key(n, q, 1, sd, {'variance': 2 * D * 60, 'no-two': math.sqrt(D * 60), 'd-slip': math.sqrt(2 * 1.6 * 60)}, shown=9.80)
ok(n + ' 600 steps of variance 0.16 give 96', close(600 * dx**2, 96, 1e-9))
ok(n + ' table Phi(1.531)=0.9371', close(P(1.531), 0.9371, 5e-5), P(1.531))
ok(n + ' 15/9.798 = 1.531', close(15 / 9.798, 1.531, 5e-4))
key(n, q, 2, 2 * (1 - P(15 / sd)), {'one-tail': 1 - P(15 / sd), 'inside': 2 * P(15 / sd) - 1}, shown=[0.126, 2 * (1 - 0.9371)])
key(n, q, 3, 24**2 / (2 * D), {'linear': 60 * 24 / sd, 'var-24': 24 / (2 * D)})
ok(n + ' 24/9.798 = 2.449 and its square 6', close(24 / sd, 2.449, 5e-4) and close((24 / sd)**2, 6, 1e-9))
# Monte Carlo of the walk itself: sd after 600 steps, and the two-sided tail
steps = (2 * rng.binomial(600, 0.5, size=2_000_000) - 600) * dx
ok(n + ' MC walk sd after one minute near 9.798', close(steps.std(), sd, 0.03), steps.std())
tail_exact = 1 - (binom.cdf(318, 600, 0.5) - binom.cdf(281, 600, 0.5))   # |S| >= 38 ticks, S even
print('INFO %s exact lattice walk P(|move|>15p) = %.4f against the kernel model 0.1258 (MC %.4f)' % (n, tail_exact, (np.abs(steps) > 15).mean()))
ok(n + ' kernel tail within 0.01 of the exact walk', abs(tail_exact - 0.1258) < 0.01, tail_exact)

n = 'p-two-level-bar'; q = p1[n]
D = 0.2
key(n, q, 0, 90 - 30, {'right-value': 90, 'gave-a': 30})
wd = math.sqrt(2 * D * 0.25)
ok(n + ' width 0.3162, z 1.265, Phi 0.8971', close(wd, 0.3162, 5e-5) and close(0.4 / wd, 1.265, 5e-4) and close(P(1.265), 0.8971, 5e-5))
key(n, q, 1, 30 + 60 * P(0.4 / wd), {'no-two': 30 + 60 * P(0.4 / math.sqrt(D * 0.25)), 'no-base': 60 * P(0.4 / wd)}, shown=[83.8, 30 + 60 * 0.8971])
zq = norm.ppf(0.75)
ok(n + ' quantile 0.6745', close(zq, 0.6745, 5e-5))
key(n, q, 2, zq * wd, {'no-width': zq, 'share': 0.75 * wd}, shown=[0.213, 0.6745 * 0.3162])
key(n, q, 3, (0.4 / zq)**2 / (2 * D), {'no-two': (0.4 / zq)**2 / D, 'unsquared': (0.4 / zq) / (2 * D)}, shown=[0.879, (0.4 / 0.6745)**2 / 0.4])
ok(n + ' 0.593 and 0.3517', close(0.4 / 0.6745, 0.5930, 5e-5) and close((0.4 / 0.6745)**2, 0.3517, 5e-5))
x = sp.symbols('x', real=True); tt = sp.symbols('t', positive=True)
u = 30 + 60 * (1 + sp.erf(x / sp.sqrt(2 * sp.Rational(1, 5) * tt) / sp.sqrt(2))) / 2
ok(n + ' sympy: 30+60Phi(x/sqrt(2Dt)) solves u_t = 0.2 u_xx', sp.simplify(sp.diff(u, tt) - sp.Rational(1, 5) * sp.diff(u, x, 2)) == 0)
ts = np.array([0.01, 0.1, 0.8792, 5, 50, 50000.0]); us = 30 + 60 * P(0.4 / np.sqrt(0.4 * ts))
ok(n + ' long bar u(0.4,t) falls through 75 near 0.879 towards 60', bool(np.all(np.diff(us) < 0)) and close(us[2], 75, 0.01) and close(us[-1], 60, 0.1), us.round(3))
key(n, q, 4, 30 + 10 * 3.4, {'centre': 60, 'level': 75})
xs = np.linspace(-3, 3, 121); h = xs[1] - xs[0]; uu = np.where(xs < 0, 30.0, 90.0)
uu[0], uu[-1] = 30, 90; lam = 0.4; dtt = lam * h * h / D
for _ in range(int(400 / dtt)):
    uu[1:-1] += lam * (uu[2:] - 2 * uu[1:-1] + uu[:-2])
ok(n + ' FD cut bar settles at 64 at x=0.4', close(np.interp(0.4, xs, uu), 64, 1e-6), np.interp(0.4, xs, uu))

n = 'p-grid-rod'; q = p1[n]
D, dx = 0.25, 0.1
dtmax = dx**2 / (2 * D)
key(n, q, 0, 1.5 / dtmax, {'lam-one': math.ceil(1.5 / (dx**2 / D) - 1e-9), 'no-d': 1.5 / (dx**2 / 2)})


def rod(nsteps, lam=0.5):
    g = np.full(13, 40.0); g[0], g[-1] = 15, 75
    for _ in range(nsteps):
        g[1:-1] = g[1:-1] + lam * (g[2:] - 2 * g[1:-1] + g[:-2])
    return g


key(n, q, 1, rod(1)[1], {'lam-one': rod(1, 1.0)[1], 'three-mean': (15 + 40 + 40) / 3})
ok(n + ' walk D = dx^2/(2dt) = 0.25 at dt 0.02', close(dx**2 / (2 * 0.02), 0.25, 1e-12))
ok(n + ' after two steps u(0.2)=33.75, u(0.1)=27.5', close(rod(2)[2], 33.75, 1e-12) and close(rod(2)[1], 27.5, 1e-12))
key(n, q, 2, rod(3)[1], {'two-steps': rod(2)[1]})
steady = 15 + 50 * 0.1
key(n, q, 3, rod(3)[1] - steady, {'steady': steady, 'mean-ends': rod(3)[1] - 45, 'left-end': rod(3)[1] - 15})
ok(n + ' grid at lambda 1/2 settles on the line 15+50x', np.allclose(rod(20000), 15 + 50 * np.linspace(0, 1.2, 13), atol=1e-8))
ok(n + ' 74 steps break the bound, 75 meet it', 0.25 * (1.5 / 74) / dx**2 > 0.5 and close(0.25 * (1.5 / 75) / dx**2, 0.5, 1e-12))
g74 = np.full(13, 40.0); g74[0], g74[-1] = 15, 75
lam74 = 0.25 * (1.5 / 74) / dx**2
print('INFO %s at 74 steps lambda = %.5f; worst mode factor %.5f' % (n, lam74, 1 - 4 * lam74 * math.sin(11 * math.pi / 24)**2))

n = 'p-drift-walk'; q = p1[n]
dx, dt, qq = 0.05, 0.001, 0.6
D = dx**2 / (2 * dt); c = (2 * qq - 1) * dx / dt
ok(n + ' D = 1.25', close(D, 1.25, 1e-12))
key(n, q, 0, c, {'no-bias': dx / dt, 'used-q': qq * dx / dt})
a = sp.symbols('a'); xx, t2 = sp.symbols('x t')
cand = sp.exp(-a * t2) * sp.cos(2 * (xx - 10 * t2))
res = sp.simplify((sp.diff(cand, t2) + 10 * sp.diff(cand, xx) - sp.Rational(5, 4) * sp.diff(cand, xx, 2)) / cand)
ok(n + ' sympy residual is (5-a)u', sp.simplify(res - (5 - a)) == 0, res)
key(n, q, 1, float(sp.solve(res, a)[0]), {'unsquared': 1.25 * 2, 'no-freq': 1.25})
m, v = c * 0.32, 2 * D * 0.32
ok(n + ' mean 3.2, sd 0.8944, z 1.342, Phi 0.9102', close(m, 3.2, 1e-12) and close(math.sqrt(v), 0.8944, 5e-5) and close((m - 2) / math.sqrt(v), 1.342, 5e-4) and close(P(1.342), 0.9102, 5e-5))
key(n, q, 2, P((2 - m) / math.sqrt(v)), {'no-drift': P(2 / math.sqrt(v)), 'var-dt': P((2 - m) / math.sqrt(D * 0.32))}, shown=[0.090, 1 - 0.9102])
z99 = norm.ppf(0.99)
ok(n + ' quantile 2.3263 and 6.325', close(z99, 2.3263, 5e-5) and close(10 / math.sqrt(2.5), 6.325, 5e-4))
key(n, q, 3, (z99 / (10 / math.sqrt(2.5)))**2, {'unsquared': z99 / (10 / math.sqrt(2.5)), 'var-dt': (z99 / (10 / math.sqrt(1.25)))**2}, shown=0.135)
kern = sp.exp(-(xx - 10 * tt)**2 / (5 * tt)) / sp.sqrt(5 * sp.pi * tt)
ok(n + ' sympy: N(ct, 2Dt) density solves u_t + 10u_x = 1.25u_xx', sp.simplify(sp.diff(kern, tt) + 10 * sp.diff(kern, xx) - sp.Rational(5, 4) * sp.diff(kern, xx, 2)) == 0)
# the walk itself: mean rate c, variance rate 4q(1-q)dx^2/dt = 2.4, not 2D = 2.5
R = rng.binomial(320, qq, size=2_000_000); pos = dx * (2 * R - 320)
ok(n + ' MC walk mean at t=0.32 is ct = 3.2', close(pos.mean(), 3.2, 0.003), pos.mean())
walk_var = 4 * qq * (1 - qq) * dx**2 / dt * 0.32
print('INFO %s the walk variance at t=0.32 is %.4f (MC %.4f), the model 2Dt = 0.8; exact walk P(below 2) = %.4f (MC %.4f), the model 0.0899'
      % (n, walk_var, pos.var(), binom.cdf(179, 320, qq), (pos < 2).mean()))
ok(n + ' MC: the walk variance is 0.768, apart from the model 0.8 (finding 1, imprecise, does not fail)', abs(pos.var() - 0.768) < 0.004 and abs(pos.var() - 0.8) > 0.02, pos.var())
R2 = rng.binomial(135, qq, size=2_000_000)
print('INFO %s exact walk P(below start) at t=0.135: %.4f (strictly below, binomial), the model 0.0100' % (n, binom.cdf(67, 135, qq)))

# ---------------------------------------------------------------- problems-2
p2 = load(2)
n = 'p-tent-rod'; q = p2[n]
D, L = 0.1, 2
rate = D * (math.pi / L)**2
key(n, q, 0, rate, {'unsquared': D * math.pi / L, 'length-one': D * math.pi**2}, shown=0.2467)
X = sp.symbols('x', positive=True)
bk = lambda k: sp.integrate(6 * X * sp.sin(k * sp.pi * X / 2), (X, 0, 1)) + sp.integrate(6 * (2 - X) * sp.sin(k * sp.pi * X / 2), (X, 1, 2))
ok(n + ' sympy b1 = 48/pi^2, int_0^1 x sin(pi x/2) = 4/pi^2', sp.simplify(bk(1) - 48 / sp.pi**2) == 0 and sp.simplify(sp.integrate(X * sp.sin(sp.pi * X / 2), (X, 0, 1)) - 4 / sp.pi**2) == 0)
b1, b3 = float(bk(1)), float(bk(3))
key(n, q, 1, b1, {'one-over-l': b1 / 2, 'peak': 6}, shown=4.8634)
ok(n + ' b3 = -0.5404, b2 = 0', close(b3, -0.5404, 5e-5) and sp.simplify(bk(2)) == 0, b3)
two = 4.8634 * math.exp(-0.2467 * 1.5) + 0.5404 * math.exp(-9 * 0.2467 * 1.5)
key(n, q, 2, b1 * math.exp(-rate * 1.5) - b3 * math.exp(-9 * rate * 1.5),
    {'one-term': b1 * math.exp(-rate * 1.5), 'sign': b1 * math.exp(-rate * 1.5) + b3 * math.exp(-9 * rate * 1.5)}, shown=[3.38, two])
ok(n + ' e^-0.370 term 3.359 and e^-3.331 term 0.019', close(4.8634 * math.exp(-0.370), 3.359, 2e-3) and close(0.5404 * math.exp(-3.331), 0.019, 5e-4))
xs = np.linspace(0, 2, 401); h = xs[1] - xs[0]; g = np.where(xs <= 1, 6 * xs, 6 * (2 - xs)); lam = 0.25; dtt = lam * h * h / D
for _ in range(int(round(1.5 / dtt))):
    g[1:-1] += lam * (g[2:] - 2 * g[1:-1] + g[:-2])
ok(n + ' FD centre at t=1.5 within 0.001 of the two-term 3.378', close(g[200], 3.3783, 1e-3), g[200])
key(n, q, 3, math.log(b1) / rate, {'peak': math.log(6) / rate, 'sign': -math.log(b1) / rate}, shown=[6.41, math.log(4.8634) / 0.2467])
ok(n + ' k=3 term below 1e-6 at t=6.41', abs(b3) * math.exp(-9 * rate * 6.41) < 1e-6, abs(b3) * math.exp(-9 * rate * 6.41))

n = 'p-exp-series'; q = p2[n]
I1 = sp.integrate(sp.exp(X) * sp.sin(X), (X, -sp.pi, sp.pi))
ok(n + ' sympy int e^x sin x over (-pi,pi) = sinh pi', sp.simplify(I1 - sp.sinh(sp.pi)) == 0)
ok(n + ' sympy antiderivative e^x(sin x - cos x)/2', sp.simplify(sp.diff(sp.exp(X) * (sp.sin(X) - sp.cos(X)) / 2, X) - sp.exp(X) * sp.sin(X)) == 0)
b1 = math.sinh(math.pi) / math.pi
key(n, q, 0, b1, {'no-pi': math.sinh(math.pi), 'sign': -b1}, shown=3.6761)
for kv in range(1, 7):
    bkv = quad(lambda z: math.exp(z) * math.sin(kv * z), -math.pi, math.pi)[0] / math.pi
    ok(n + ' b_%d = (-1)^(k+1) 2k/(1+k^2) b_1' % kv, close(bkv, (-1)**(kv + 1) * 2 * kv / (1 + kv * kv) * b1, 1e-9))
key(n, q, 1, 0.6 * b1, {'sign': -0.6 * b1, 'no-k': 0.2 * b1}, shown=[0.6 * 3.6761, 2.2057, 2.2056])
ks = np.array([1e4, 1e5]); slope = np.diff(np.log(2 * ks / (1 + ks**2))) / np.diff(np.log(ks))
key(n, q, 2, round(float(slope[0]), 6), {'minus-two': -2, 'plus-one': 1})
key(n, q, 3, math.cosh(math.pi), {'left': math.exp(math.pi), 'right': math.exp(-math.pi), 'half-gap': math.sinh(math.pi)}, shown=11.5920)
S = (math.pi / math.tanh(math.pi) - 1) / 2
key(n, q, 4, S, {'no-half': 2 * S, 'keep-one': (math.pi / math.tanh(math.pi)) / 2, 'used-left': (math.pi * math.exp(math.pi) / math.sinh(math.pi) - 1) / 2},
    shown=[1.0767, (math.pi * 11.5920 / 11.5487 - 1) / 2])
kk_ = np.arange(1, 2_000_001, dtype=float); part = (1 / (1 + kk_**2)).sum()
ok(n + ' direct sum of 1/(1+k^2) to 2e6 terms (plus tail) matches', close(part + 1 / 2e6, S, 1e-9), part)
ok(n + ' pi coth pi = 3.15335', close(math.pi / math.tanh(math.pi), 3.15335, 5e-6))
a0 = quad(math.exp, -math.pi, math.pi)[0] / math.pi
ak = lambda k: (-1)**k * 2 * math.sinh(math.pi) / (math.pi * (1 + k * k))
ok(n + ' quadrature a_k matches (-1)^k 2 sinh pi/(pi(1+k^2)); a_0/2 = sinh pi/pi',
   all(close(quad(lambda z: math.exp(z) * math.cos(kq * z), -math.pi, math.pi)[0] / math.pi, ak(kq), 1e-9) for kq in (1, 2, 3)) and close(a0 / 2, b1, 1e-12))
ser_pi = a0 / 2 + sum(ak(k) * (-1)**k for k in range(1, 200001))
ok(n + ' partial sums at x=pi tend to cosh pi, not e^pi', close(ser_pi, math.cosh(math.pi), 1e-4), ser_pi)
x1 = 1.0
ser_in = a0 / 2 + sum(ak(k) * math.cos(k * x1) + (-1)**(k + 1) * 2 * k / (1 + k * k) * b1 * math.sin(k * x1) for k in range(1, 400001))
ok(n + ' series with these a_k, b_k returns e^x inside (x=1)', close(ser_in, math.e, 1e-4), ser_in)

n = 'p-grid-modes'; q = p2[n]
D, dx, dt = 0.75, math.pi / 12, 0.04
lam = D * dt / dx**2
key(n, q, 0, lam, {'no-d': dt / dx**2, 'unsquared': D * dt / dx}, shown=0.4377)
gfac = 1 - 4 * lam * math.sin(dx / 2)**2
key(n, q, 1, gfac, {'exact': math.exp(-D * dt), 'no-half': 1 - 4 * lam * math.sin(dx)**2}, shown=[0.9702, 1 - 4 * 0.4377 * 0.01704])
ok(n + ' sin^2(pi/24) = 0.01704, dx^2 = 0.068539', close(math.sin(dx / 2)**2, 0.01704, 5e-6) and close(dx**2, 0.068539, 5e-7))
key(n, q, 2, gfac**40, {'exact': math.exp(-1.2), 'power-t': 0.9702**1.6}, shown=[0.298, 0.9702**40])
xg = np.linspace(0, math.pi, 13); g = np.sin(xg)
for _ in range(40):
    g[1:-1] = g[1:-1] + lam * (g[2:] - 2 * g[1:-1] + g[:-2])
ok(n + ' explicit scheme run 40 steps on sin x gives the factor^40', close(g[6], gfac**40, 1e-12), g[6])
ok(n + ' every grid mode bounded at lambda 0.4377', all(abs(1 - 4 * lam * math.sin(k * dx / 2)**2) <= 1 for k in range(1, 12)))
key(n, q, 3, (0.3012 - 0.298) / 0.3012, {'absolute': 0.3012 - 0.298, 'ratio': 0.298 / 0.3012}, shown=[0.011, (math.exp(-1.2) - gfac**40) / math.exp(-1.2)])
print('INFO %s unrounded shortfall is %.3f%%; carried 0.298 gives %.3f%%; both type as 1.1' % (n, 100 * (1 - gfac**40 / math.exp(-1.2)), 100 * (0.3012 - 0.298) / 0.3012))

# ---------------------------------------------------------------- problems-3
p3 = load(3)


def bs_call(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    return S * P(d1) - K * math.exp(-r * T) * P(d2)


n = 'p-straddle-vol'; q = p3[n]
taup = sp.symbols('tau', positive=True)
w = W(q, 0)
arg = (0 + 2 * sp.Rational(1, 2) * taup) / sp.sqrt(2 * taup)
ok(n + ' part 1 key sqrt(tau/2)', sp.simplify(arg - sp.sqrt(taup / 2)) == 0 and w['answer'] == '\\sqrt{\\frac{\\tau}{2}}')
forms = {'\\sqrt{\\tau/2}': sp.sqrt(taup / 2), '\\frac{\\sqrt{\\tau}}{\\sqrt{2}}': sp.sqrt(taup) / sp.sqrt(2), '\\frac{\\tau}{\\sqrt{2\\tau}}': taup / sp.sqrt(2 * taup), '\\frac{\\sqrt{2\\tau}}{2}': sp.sqrt(2 * taup) / 2}
ok(n + ' part 1 accept list all equal the key', set(w['accept']) == set(forms) and all(sp.simplify(f - arg) == 0 for f in forms.values()))
ok(n + ' part 1 slips: a=1 gives sqrt(2 tau), top is tau, tau/(2 tau) = 1/2; none equals the key',
   sp.simplify((2 * taup) / sp.sqrt(2 * taup) - sp.sqrt(2 * taup)) == 0
   and [x['tex'] for x in w['wrong']] == ['\\sqrt{2\\tau}', '\\tau', '\\frac{1}{2}']
   and all(sp.simplify(e - arg) != 0 for e in (sp.sqrt(2 * taup), taup, sp.Rational(1, 2))))


def lemma(a, x0, ta):
    return quad(lambda yy: math.exp(a * yy) * math.exp(-(x0 - yy)**2 / (4 * ta)) / math.sqrt(4 * math.pi * ta), 0, 40, points=[max(x0, 0.0)], epsabs=1e-13, epsrel=1e-12)[0]


ok(n + ' lemma: int_0^inf e^{ay} kernel = e^{ax+a^2 tau} Phi((x+2a tau)/sqrt(2 tau))',
   all(close(lemma(a, x0, ta), math.exp(a * x0 + a * a * ta) * P((x0 + 2 * a * ta) / math.sqrt(2 * ta)), 1e-8) for a in (0.5, -0.5, 1.3) for x0 in (0, 0.2) for ta in (0.01, 0.3)))
ok(n + ' C = K(2Phi(sqrt(tau/2)) - 1) equals Black-Scholes at r=0, S=K', all(close(80 * (2 * P(math.sqrt(0.5 * s * s * T / 2)) - 1), bs_call(80, 80, 0, s, T), 1e-10) for s in (0.1, 0.17, 0.4) for T in (0.25, 0.75, 2)))
key(n, q, 1, (4.80 / 80 + 1) / 2, {'whole': (9.60 / 80 + 1) / 2, 'c-over-k': 4.80 / 80})
ok(n + ' table quantile of 0.53 is 0.07527', close(norm.ppf(0.53), 0.07527, 5e-6), norm.ppf(0.53))
key(n, q, 2, 2 * 0.07527**2, {'unsquared': 2 * 0.07527, 'halved': 0.07527**2 / 2, 'no-two': 0.07527**2}, shown=0.01133)
sig = math.sqrt(2 * 0.0113311 / 0.75)
key(n, q, 3, sig, {'no-half': math.sqrt(0.01133 / 0.75), 'calendar': math.sqrt(2 * 0.0113311), 'no-root': 2 * 0.01133 / 0.75}, shown=[0.1738, math.sqrt(2 * 0.01133 / 0.75)])
strad = 2 * bs_call(80, 80, 0, 0.1738, 0.75)
ok(n + ' priced at 17.38% the straddle is 9.60', close(strad, 9.60, 0.005), strad)

n = 'p-log-contract'; q = p3[n]
r, s, T, K0 = 0.02, 0.28, 1.5, 64.0
k = 2 * r / s**2; ta = 0.5 * s * s * T
xs2, tau2, ksy, csy = sp.symbols('x tau k c')
vv = sp.exp(-ksy * tau2) * (xs2 + csy * tau2)
resid = sp.simplify((sp.diff(vv, tau2) - sp.diff(vv, xs2, 2) - (ksy - 1) * sp.diff(vv, xs2) + ksy * vv) * sp.exp(ksy * tau2))
ok(n + ' part 1 sympy: c = k - 1', sp.solve(resid, csy) == [ksy - 1] and W(q, 0)['answer'] == 'k-1' and W(q, 0)['accept'] == ['-1+k'], resid)
ok(n + ' part 1 slips are 1-k, k, k+1', [x['tex'] for x in W(q, 0)['wrong']] == ['1-k', 'k', 'k+1'])
ok(n + ' k 0.5102, tau 0.0588, k tau = rT = 0.03, (k-1)tau = (r - sigma^2/2)T = -0.0288',
   close(k, 0.5102, 5e-5) and close(ta, 0.0588, 1e-12) and close(k * ta, 0.03, 1e-12) and close((k - 1) * ta, (r - s * s / 2) * T, 1e-12) and close((k - 1) * ta, -0.0288, 1e-12))
V = 1000 * math.exp(-k * ta) * (k - 1) * ta
key(n, q, 1, V, {'no-disc': 1000 * (k - 1) * ta, 'used-k': 1000 * math.exp(-k * ta) * k * ta, 'sign': -V}, shown=-27.95)
xstar = 27.95 / 970.45
key(n, q, 2, math.exp(-(k - 1) * ta) - 1, {'log-return': 0.0288, 'no-disc': math.exp(27.95 / 1000) - 1}, shown=[0.0292, math.exp(xstar) - 1])
ok(n + ' 970.45 per unit x, share to 65.87', close(1000 * math.exp(-k * ta), 970.45, 5e-3) and close(64 * math.exp(0.0288), 65.87, 5e-3))
sdl = math.sqrt(2 * ta)
ok(n + ' variance 0.1176, sd 0.34293, 0.0840 sd, Phi 0.5335', close(2 * ta, 0.1176, 1e-12) and close(sdl, 0.34293, 5e-6) and close(0.0288 / sdl, 0.0840, 5e-5) and close(P(0.0840), 0.5335, 5e-5))
pp = P((k - 1) * ta / sdl)
key(n, q, 3, pp, {'wrong-side': 1 - pp, 'no-drift': 0.5}, shown=[0.4665, 1 - 0.5335])
d2 = (0 + (r - s * s / 2) * T) / (s * math.sqrt(T))
ok(n + ' this chance is Phi(d2) at K = S0', close(P(d2), pp, 1e-12))
# Feynman-Kac by Monte Carlo: Euler on dS = rS dt + sigma S dW, 300 steps (no use of the lognormal law)
npaths, nst = 400_000, 300          # antithetic pairs: the same normals with both signs
Sx = np.full(npaths, K0); Sy = np.full(npaths, K0); dtm = T / nst
for _ in range(nst):
    zn = rng.standard_normal(npaths)
    Sx *= 1 + r * dtm + s * math.sqrt(dtm) * zn
    Sy *= 1 + r * dtm - s * math.sqrt(dtm) * zn
pay = 500 * (np.log(Sx / K0) + np.log(Sy / K0)); disc = math.exp(-r * T)
est, se = disc * pay.mean(), disc * pay.std() / math.sqrt(npaths)
ok(n + ' MC Feynman-Kac value is -27.95 (Euler bias allowed 0.05), apart from the undiscounted -28.80', abs(est - V) < 0.05 + 4 * se and abs(est + 28.8) > 0.5, 'est %.3f se %.4f' % (est, se))
ok(n + ' MC rejects the share-growth slip +29.11 and the sign slip', abs(est - 29.1134) > 20 * se and abs(est + V) > 20 * se)
pm = float((Sx > K0).mean()); sep = math.sqrt(pm * (1 - pm) / npaths)
ok(n + ' MC risk-neutral chance of a positive payoff 0.4665, separated from 0.5 and 0.5335', abs(pm - pp) < 4 * sep and abs(pm - 0.5) > 10 * sep, 'p %.4f se %.4f' % (pm, sep))
xg = np.linspace(-1.5, 1.5, 601); h = xg[1] - xg[0]; vg = xg.copy(); nt_ = 8000; dtt = ta / nt_
for j in range(nt_):
    tn = (j + 1) * dtt
    new = vg.copy()
    new[1:-1] = vg[1:-1] + dtt * ((vg[2:] - 2 * vg[1:-1] + vg[:-2]) / h**2 + (k - 1) * (vg[2:] - vg[:-2]) / (2 * h) - k * vg[1:-1])
    new[0] = math.exp(-k * tn) * (xg[0] + (k - 1) * tn); new[-1] = math.exp(-k * tn) * (xg[-1] + (k - 1) * tn)
    vg = new
ok(n + ' explicit FD solve of v_tau = v_xx + (k-1)v_x - kv from v=x gives -27.95 at x=0', close(1000 * vg[300], V, 0.01), 1000 * vg[300])

n = 'p-grid-budget'; q = p3[n]


def cn_price(S, K, r, sigma, T, nx, nt, L=1.0):
    """Own Crank-Nicolson in heat variables (banded solve), exact far edge, left edge 0."""
    k = 2 * r / sigma**2
    al, be = -(k - 1) / 2, -(k + 1)**2 / 4
    a1, a2 = (k + 1) / 2, (k - 1) / 2
    te = 0.5 * sigma**2 * T
    x = np.linspace(-L, L, nx + 1); h = x[1] - x[0]; dt = te / nt; lam = dt / h**2
    u = np.maximum(np.exp(a1 * x) - np.exp(a2 * x), 0.0)
    ab = np.zeros((3, nx - 1)); ab[0, 1:] = -lam / 2; ab[1] = 1 + lam; ab[2, :-1] = -lam / 2
    tau = 0.0
    for _ in range(nt):
        right = math.exp(a1 * L + a1**2 * (tau + dt)) - math.exp(a2 * L + a2**2 * (tau + dt))
        rhs = u[1:-1] + lam / 2 * (u[:-2] - 2 * u[1:-1] + u[2:])
        rhs[-1] += lam / 2 * right
        u[1:-1] = solve_banded((1, 1), ab, rhs); u[0], u[-1] = 0.0, right
        tau += dt
    x0 = math.log(S / K)
    return K * math.exp(al * x0 + be * te) * float(np.interp(x0, x, u))


args = (120, 120, 0.045, 0.18, 1.25)
run = {nx: cn_price(*args, nx, nx // 5) for nx in (200, 300, 400, 600, 1200, 2400)}
ok(n + ' CN run on 200 intervals returns 12.9963192', close(run[200], 12.9963192, 5e-8), '%.7f' % run[200])
ok(n + ' CN run on 300 intervals returns 12.9975576', close(run[300], 12.9975576, 5e-8), '%.7f' % run[300])
gap = 12.9975576 - 12.9963192
C = gap / (0.01**2 - (1 / 150)**2)
ok(n + ' gap 0.0012384 and h^2 difference 1/18000', close(gap, 0.0012384, 1e-9) and close(0.01**2 - (1 / 150)**2, 1 / 18000, 1e-15))
key(n, q, 0, C, {'n-not-h': gap / (1 / 200**2 - 1 / 300**2), 'no-square': gap / (0.01 - 1 / 150), 'one-run': gap / 0.01**2}, shown=22.29)
key(n, q, 1, C * 0.005**2 * 1e6, {'unit-length': 22.29 * (1 / 400)**2 * 1e6, 'wrong-run': 22.29 * (1 / 150)**2 * 1e6}, shown=[557, 22.29 * 0.005**2 * 1e6])
key(n, q, 2, 557.28 / 1.5**2, {'per-interval': 557.28 / 2.25**2, 'first-order': 557.28 / 1.5})
key(n, q, 3, (557.28 / 247.68)**2, {'linear': 557.28 / 247.68, 'root': math.sqrt(557.28 / 247.68)}, shown=5.06)
limit = run[2400] + (run[2400] - run[1200]) / 3      # Richardson guess at the limit (order is a little under 2, so the closed form is the sharper reference)
bs = bs_call(*args)
print('INFO %s grid limit %.7f, Black-Scholes %.7f, shortfalls x1e6: 200 -> %.2f, 300 -> %.2f, 400 -> %.2f, 600 -> %.2f'
      % (n, limit, bs, (limit - run[200]) * 1e6, (limit - run[300]) * 1e6, (limit - run[400]) * 1e6, (limit - run[600]) * 1e6))
ok(n + ' grid limit is the closed form to 2e-6 (far edge does not bind)', close(limit, bs, 2e-6), limit - bs)
ok(n + ' runs fall short of the limit (V - V_h > 0)', all(run[m] < limit for m in (200, 300, 400, 600)))
ok(n + ' 400 run gap about 1% above the predicted 557.28', 0.005 < (bs - run[400]) * 1e6 / 557.28 - 1 < 0.02, (bs - run[400]) * 1e6 / 557.28 - 1)
ok(n + ' 600 run about 253e-6 below the limit', close((bs - run[600]) * 1e6, 253, 1.0), (bs - run[600]) * 1e6)
order = math.log((bs - run[300]) / (bs - run[600])) / math.log(2)
ok(n + ' observed order a little under 2', 1.9 < order < 2.0, order)
ok(n + ' work ratio 2.25 is under half the path factor 5.06', 2.25 / 5.0625 < 0.5)


def se_of(npth, reps=400):
    z = rng.standard_normal((reps, npth))
    ST = 120 * np.exp((0.045 - 0.0162) * 1.25 + 0.18 * math.sqrt(1.25) * z)
    return (math.exp(-0.045 * 1.25) * np.maximum(ST - 120, 0)).mean(axis=1).std()


ratio = se_of(1600) / se_of(8100)
ok(n + ' MC: 5.0625 times the paths cuts the standard error about 2.25 times, not 5.06 or 1.5', close(ratio, 2.25, 0.3), ratio)

print('\n%d checks, %d failed' % (n_checks, len(fails)))
for f in fails:
    print('  FAILED:', f)
sys.exit(1 if fails else 0)
