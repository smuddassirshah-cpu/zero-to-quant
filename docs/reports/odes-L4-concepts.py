#!/usr/bin/env python3
"""Concept audit, odes level 4 (l14 to l18, review-4, homework-4).

Run from the repo root: python3 docs/reports/odes-L4-concepts.py
Every claim of method, order, error size, stability limit and code behaviour is
executed here, independently of docs/reports/odes-L4-numbers.py.

Exit code: 0 when every check passes. A check tagged FINDING reads the content
string it is about; it fails while the content says the thing the audit found
false or unqualified, and passes once the sentence is corrected. So the script
exits 1 until the fix pass of docs/reviews/audit-odes-4.md is applied.
"""
import json, math, os, sys, warnings
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

warnings.simplefilter('ignore')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, 'app', 'content', 'courses', 'odes')
FAILS, NPASS = [], [0]
INF = np.inf


def chk(name, cond, detail=''):
    if cond:
        NPASS[0] += 1
    else:
        FAILS.append(name)
        print(f'FAIL  {name}  {detail}')


def near(name, got, want, tol):
    chk(name, abs(got - want) <= tol, f'computed {got!r}, content says {want!r}')


def finding(n, name, content_is_fixed, detail):
    """A check tied to audit finding n. Fails while the content is unfixed."""
    if content_is_fixed:
        NPASS[0] += 1
    else:
        FAILS.append(f'finding {n}: {name}')
        print(f'FAIL  FINDING {n}  {name}  {detail}')


def load(f):
    return json.load(open(os.path.join(C, f + '.json')))


DOC = {f: load(f) for f in ('l14-laplace-transform', 'l15-solving-with-laplace', 'l16-euler-method',
                            'l17-runge-kutta', 'l18-four-decimal-places', 'review-4', 'homework-4')}
L14, L15, L16, L17, L18, REV, HW = DOC.values()


def close(a, b, tol):
    if isinstance(b, (list, tuple)):
        a = list(a)
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    if isinstance(b, bool) or isinstance(a, (bool, np.bool_)):
        return bool(a) == bool(b)
    if tol and 'abs' in tol:
        return abs(a - b) <= tol['abs']
    return abs(a - b) <= max(1e-9 * max(abs(a), abs(b)), 1e-12)


def run_tests(src, tests):
    ns = {}
    try:
        exec(src, ns)
    except Exception as e:
        return [f'load error {type(e).__name__}: {e}'] * len(tests), ns
    res = []
    for t in tests:
        cmp_ = t.get('compare', 'isclose')
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            if cmp_ == 'raises':
                try:
                    v = eval(t['call'], ns)
                    res.append(f'no error, value {v!r}')
                except Exception as e:
                    res.append(True if any(k.__name__ == t['expect'] for k in type(e).__mro__) else f'raised {type(e).__name__}')
                continue
            got = eval(t['call'], ns)
            exp = t['expect']
            if isinstance(exp, str):
                exp = eval(exp, ns)
            if cmp_ == 'equal':
                res.append(True if got == exp else f'got {got!r}, expected {exp!r}')
            else:
                res.append(True if close(got, exp, t.get('tol')) else f'got {got!r}, expected {exp!r}')
        except Exception as e:
            res.append(f'{type(e).__name__}: {e}')
    return res, ns


def widget_check(label, w, min_starter_fail=None):
    """The solution passes every hidden test and example; the starter fails the tests."""
    pre = w.get('prelude', '') + '\n'
    tests = w.get('tests', [])
    allt = tests + w.get('examples', [])
    rs, ns = run_tests(pre + w['solution'], allt)
    bad = [(t['call'], r) for t, r in zip(allt, rs) if r is not True]
    chk(f'{label}: solution passes {len(allt)} tests and examples', not bad, str(bad[:2]))
    rt, _ = run_tests(pre + w['starter'], tests)
    nfail = sum(r is not True for r in rt)
    need = len(tests) if min_starter_fail is None else min_starter_fail
    chk(f'{label}: starter fails at least {need} of {len(tests)} tests', nfail >= need, f'fails {nfail}')
    return ns


def lap(f, s, upper=INF, **kw):
    def g(t):
        w = math.exp(-s * t)
        if w == 0.0:
            return 0.0          # far tail of a convergent integral; divergent cases pass a finite upper limit
        try:
            return w * f(t)
        except OverflowError:
            return 0.0
    return quad(g, 0, upper, limit=400, **kw)[0]


# ---------------------------------------------------------------- reference integrators
def euler(f, t0, y0, h, n):
    y = np.array(y0, dtype=float)
    t = t0
    for _ in range(n):
        y = y + h * np.asarray(f(t, y))
        t += h
    return y


def rk4_step(f, t, y, h):
    k1 = np.asarray(f(t, y)); k2 = np.asarray(f(t + h / 2, y + h / 2 * k1))
    k3 = np.asarray(f(t + h / 2, y + h / 2 * k2)); k4 = np.asarray(f(t + h, y + h * k3))
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def rk4(f, t0, y0, h, n, step=rk4_step):
    y = np.array(y0, dtype=float)
    for i in range(n):
        y = step(f, t0 + i * h, y, h)
    return y


def midpoint(f, t0, y0, h, n):
    y = np.array(y0, dtype=float)
    for i in range(n):
        t = t0 + i * h
        y = y + h * np.asarray(f(t + h / 2, y + h / 2 * np.asarray(f(t, y))))
    return y


def order(errs, hs):
    return float(np.polyfit(np.log(hs), np.log(errs), 1)[0])


grow = lambda t, y: y
E = math.e

# ================================================================= l14 Laplace transform
near('l14 s0 perpetuity at 4% is 25', lap(lambda t: 1, 0.04), 25, 1e-6)
near('l14 s2 L{e^{at}} = 1/(s-a) (a=0.02, s=0.06)', lap(lambda t: math.exp(0.02 * t), 0.06), 25, 1e-6)
chk('l14 s2 area grows without bound at s <= a',
    lap(lambda t: math.exp(0.07 * t), 0.06, 600) > 30 and lap(lambda t: math.exp(0.06 * t), 0.06, 6000) > 5999)
near('l14 s3 L{t}(2) = 1/4', lap(lambda t: t, 2), 0.25, 1e-9)
near('l14 s4 L{t^2}(1) = 2', lap(lambda t: t * t, 1), 2, 1e-8)
near('l14 s4 L{sin 3t}(1) = 0.3', lap(lambda t: math.sin(3 * t), 1, 60), 0.3, 1e-8)
near('l14 s4 L{cos 2t}(1) = 0.2', lap(lambda t: math.cos(2 * t), 1, 60), 0.2, 1e-8)
near('l14 s4 feedback: s on top of the sine row gives 0.1, a different value', 1 / (1 + 9), 0.1, 1e-12)
near('l14 s5 Gordon growth 5/(0.06-0.02)', lap(lambda t: 5 * math.exp(0.02 * t), 0.06), 125, 1e-5)
chk('l14 s5 at r=1% the 600-year area is huge and still growing',
    lap(lambda t: 5 * math.exp(0.02 * t), 0.01, 600) > 1e5 and lap(lambda t: 5 * math.exp(0.02 * t), 0.01, 900) > 10 * lap(lambda t: 5 * math.exp(0.02 * t), 0.01, 600))
near('l14 s5 option d: L{5}L{e^{0.02t}} at 0.01 is -50,000', (5 / 0.01) * (1 / (0.01 - 0.02)), -50000, 1e-6)
chk('l14 s5 transform of a product is not the product of transforms',
    abs(lap(lambda t: t * math.exp(-t), 1) - lap(lambda t: t, 1) * lap(lambda t: math.exp(-t), 1)) > 0.2)
near('l14 s6 L{t^10} = 10!/s^11 at s=2', lap(lambda t: t ** 10, 2), math.factorial(10) / 2 ** 11, 1e-6)
near('l14 s6 sin(t^2) has a transform at s=1 (finite, cut at 60)', lap(lambda t: math.sin(t * t), 1, 40), lap(lambda t: math.sin(t * t), 1, 20), 1e-6)
chk('l14 s6 t^2 - st is least at t = s/2 and positive once t > s',
    all(abs(min(np.linspace(0, 20, 20001), key=lambda t: t * t - s * t) - s / 2) < 2e-3 and (s + .01) ** 2 - s * (s + .01) > 0 for s in (1, 2, 8)))
chk('l14 s6 e^{t^2-st} integral has no limit for s = 8', quad(lambda t: math.exp(t * t - 8 * t), 0, 12)[0] > 1e18)
# finding 6: exponential order alone is not enough; 1/t is below e^{t} for t >= 1 yet has no transform
eps = [1e-2, 1e-4, 1e-6]
vals = [quad(lambda t: math.exp(-t) / t, e_, 1, limit=400)[0] + quad(lambda t: math.exp(-t) / t, 1, INF)[0] for e_ in eps]
chk('l14 s6 counterexample: int_eps^inf e^{-t}/t grows like ln(1/eps)',
    abs((vals[1] - vals[0]) - math.log(100)) < 0.02 and abs((vals[2] - vals[1]) - math.log(100)) < 0.02)
txt = L14['screens'][6]['explain']['text']
finding(6, 'l14 screens[6].explain: "Any function growing no faster than some e^{at} has a transform" needs a condition near 0',
        'Any function growing no faster than some $e^{at}$ has a transform.' not in txt,
        '1/t stays below e^{t} for t >= 1 and has no transform; the theorem needs piecewise continuity (Boyce and DiPrima 6.1.2)')
# derivative rule, with decaying and growing f
for nm, f, df, d2f, f0, df0, s in (
        ('cos 2t', lambda t: math.cos(2 * t), lambda t: -2 * math.sin(2 * t), lambda t: -4 * math.cos(2 * t), 1, 0, 1.5),
        ('e^{0.5t}+t', lambda t: math.exp(.5 * t) + t, lambda t: .5 * math.exp(.5 * t) + 1, lambda t: .25 * math.exp(.5 * t), 1, 1.5, 2.0)):
    F = lap(f, s, 80)
    near(f'l14 s7 L{{f\'}} = sF - f(0) for {nm}', lap(df, s, 80), s * F - f0, 1e-7)
    near(f'l14 s7 L{{f\'\'}} = s^2F - sf(0) - f\'(0) for {nm}', lap(d2f, s, 80), s * s * F - s * f0 - df0, 1e-7)
for s in (0.5, 2.0):
    near(f'l14 s8 shift rule: L{{e^-t cos 2t}}({s})', lap(lambda t: math.exp(-t) * math.cos(2 * t), s, 80), (s + 1) / ((s + 1) ** 2 + 4), 1e-8)
    chk(f'l14 s8 wrong option (s-1)/((s-1)^2+4) differs at s={s}', abs((s - 1) / ((s - 1) ** 2 + 4) - (s + 1) / ((s + 1) ** 2 + 4)) > 0.02)
near('l14 s8 linearity', lap(lambda t: 3 * t + 2 * math.sin(t), 1.3, 80), 3 / 1.3 ** 2 + 2 / (1.3 ** 2 + 1), 1e-8)
w = L14['screens'][9]['widget']
ns = widget_check('l14 s9 laplace_numeric / pv_growing', w)
v = ns['laplace_numeric'](lambda t: t, 2)
near('l14 s9 laplace_numeric(t, 2) is 0.25 less 5.2e-9', v, 0.2499999947916667, 1e-15)
c14 = L14['screens'][9]['canvas']['params']['lines'][1].strip().rstrip('.')
L14_CONSOLE_OK = repr(float(v)).startswith(c14) and '0.24999999479166674'.startswith(c14)   # second value: Pyodide 0.27.7
L14_DETAIL = f'laplace_numeric prints {float(v)!r} here and 0.24999999479166674 in Pyodide, console says {c14}'
chk('l14 s9 console pv_growing prints 125.00000000000001', repr(ns['pv_growing'](5, 0.02, 0.06)) == '125.00000000000001', repr(ns['pv_growing'](5, 0.02, 0.06)))
errs = [abs(ns['laplace_numeric'](f, s) - x) for f, s, x in ((lambda t: np.exp(-t), 1, .5), (lambda t: t, 2, .25), (lambda t: np.sin(3 * t), 1, .3))]
chk('l14 s9 feedback: trapezium values within 1e-7 of 0.5, 0.25, 0.3', max(errs) < 1e-7, str(errs))
chk('l14 s9 explain: accuracy about 1e-8', 1e-9 < max(errs) < 5e-8, str(errs))
tails = [math.exp(-100) / 2, math.exp(-100) * (25 + .25), math.exp(-50), math.exp(-50), math.exp(-50) * (2500 + 100 + 2)]
chk('l14 s9 explain: the cut at T = 50 costs below 1e-18 in every test', max(tails) < 1e-18, str(max(tails)))
near('l14 s10 default claim 100 * 0.02/0.06', 100 * lap(lambda t: 0.02 * math.exp(-0.02 * t), 0.04), 33.3333, 1e-3)
rng = np.random.default_rng(14)
tau = rng.exponential(1 / 0.02, 2_000_000)
pv = 100 * np.exp(-0.04 * tau)
chk('l14 s10 Monte Carlo: hazard 2% gives E[100 e^{-0.04 tau}] = 33.33 (not 50, not 100)',
    abs(pv.mean() - 100 / 3) < 5 * pv.std() / math.sqrt(len(pv)) and pv.std() / math.sqrt(len(pv)) < 0.05)
lam = 0.02
near('l14 s10 MGF of the default time at u = -0.04 is the transform at 0.04', np.exp(-0.04 * tau).mean(), lam / (lam + 0.04), 1e-3)
near('l14 q0', 1 / (5 - 3), 0.5, 0); near('l14 q0 wrong', 1 / (5 + 3), 0.125, 0)
near('l14 q2', lap(lambda t: math.sin(3 * t), 4, 30), 0.12, 1e-8); near('l14 q2 wrong', 4 / 25, 0.16, 1e-12)
chk('l14 q3 exists exactly for s > 2', abs(quad(lambda t: math.exp(-0.5 * t), 0, INF)[0] - 2) < 1e-8 and quad(lambda t: math.exp(0.0 * t), 0, 5000)[0] > 4999 and quad(lambda t: math.exp(0.5 * t), 0, 50)[0] > 1e10)

# ================================================================= l15 solving with Laplace
def ivp(f, y0, T):
    s = solve_ivp(f, (0, T), y0, rtol=1e-11, atol=1e-13, method='DOP853')
    return s.y[:, -1]


y1 = lambda t: 2 - 2 * math.exp(-2 * t)
near('l15 s0 y\'+2y=4 from 0 gives 2-2e^{-2t} at t=1', ivp(lambda t, y: [4 - 2 * y[0]], [0], 1)[0], y1(1), 1e-9)
near('l15 s1 y(1) = 1.7293', y1(1), 1.7293, 5e-5); near('l15 s1 wrong 2-2e^{-1}', 2 - 2 / E, 1.2642, 5e-5)
near('l15 s0 transform of the answer is 4/(s(s+2)) at s=0.7', lap(y1, 0.7), 4 / (0.7 * 2.7), 1e-8)
vas = lambda t: 0.04 + 0.02 * math.exp(-0.5 * t)
near('l15 s2 Vasicek by ODE solver matches 0.04+0.02e^{-0.5t}', ivp(lambda t, r: [0.5 * (0.04 - r[0])], [0.06], 3)[0], vas(3), 1e-10)
for s in (0.05, 1.0):
    near(f'l15 s2 R(s) = (0.06s+0.02)/(s(s+0.5)) at {s}', lap(vas, s), (0.06 * s + 0.02) / (s * (s + 0.5)), 1e-8)
    near(f'l15 s2 split form at {s}', 0.04 / s + 0.02 / (s + 0.5), (0.06 * s + 0.02) / (s * (s + 0.5)), 1e-12)
    chk(f'l15 s2 wrong (no start) differs at {s}', abs(0.02 / (s * (s + 0.5)) - lap(vas, s)) > 1e-3)
y3 = lambda t: 1 - 2 * math.exp(-t) + math.exp(-2 * t)
near('l15 s3 y\'\'+3y\'+2y=2 from rest', ivp(lambda t, z: [z[1], 2 - 3 * z[1] - 2 * z[0]], [0, 0], 1)[0], y3(1), 1e-9)
near('l15 s3 y(1) = 0.399576', y3(1), 0.399576, 5e-7)
p = np.roots([1, 3, 2, 0]); res = np.polyval([2], p) / np.polyval(np.polyder([1, 3, 2, 0]), p)
chk('l15 s3 residues 1, -2, 1 at 0, -1, -2', np.allclose(sorted(zip(np.round(p, 9), np.round(res, 9))), [(-2, 1), (-1, -2), (0, 1)]))
y4 = lambda t: math.exp(-t) * (math.cos(2 * t) + 0.5 * math.sin(2 * t))
osc = lambda t, z: [z[1], -2 * z[1] - 5 * z[0]]
near('l15 s4 oscillator from (1,0)', ivp(osc, [1, 0], 1)[0], y4(1), 1e-9)
near('l15 s4 y(1) = 0.014164', y4(1), 0.014164, 5e-7)
near('l15 s4 transform is (s+2)/((s+1)^2+4) at s=0.3', lap(y4, 0.3, 80), 2.3 / (1.3 ** 2 + 4), 1e-8)
near('l15 s5 option d: from (0,1) the solution is e^{-t} sin(2t)/2', ivp(osc, [0, 1], 1.3)[0], 0.5 * math.exp(-1.3) * math.sin(2.6), 1e-9)
near('l15 s5 from rest the oscillator stays at 0', ivp(osc, [0, 0], 2)[0], 0, 1e-12)
near('l15 s6 L{t e^{-t}} = 1/(s+1)^2 at s=0.4', lap(lambda t: t * math.exp(-t), 0.4), 1 / 1.4 ** 2, 1e-9)
w = L15['screens'][8]['widget']
ns = widget_check('l15 s8 residues / inverse_laplace', w)
pp, rr = ns['residues']([2], [1, 3, 2, 0])
chk('l15 s8 console: poles -2, -1, 0 with residues 1, -2, 1 in that order', np.allclose(pp, [-2, -1, 0], atol=1e-12) and np.allclose(rr, [1, -2, 1], atol=1e-12), f'{pp} {rr}')
near('l15 s8 console 0.39957640089372803', ns['inverse_laplace']([2], [1, 3, 2, 0], 1), 0.39957640089372803, 1e-13)
pc, rc = ns['residues']([1, 2], [1, 2, 5])
chk('l15 s8 explain: a complex pair has conjugate residues, imaginary parts cancel',
    abs(rc[0] - np.conj(rc[1])) < 1e-12 and abs(np.imag(np.sum(rc * np.exp(pc * 1.0)))) < 1e-15)
# finding 7: the residue sum is the inverse only for a proper fraction
got = ns['inverse_laplace']([1, 0], [1, 1], 1.0)          # Y = s/(s+1) = 1 - 1/(s+1)
back = lap(lambda t: -math.exp(-t), 2.0)                  # transform of what the formula returns
chk('l15 s8 improper s/(s+1): the residue sum returns -e^{-t}, whose transform is not s/(s+1)',
    abs(got + math.exp(-1)) < 1e-12 and abs(back - 2 / 3) > 0.9)
finding(7, 'l15 screens[8].prose: y = sum res e^{pt} stated for "distinct poles" with no word that num has lower degree than den',
        any(k in L15['screens'][8]['prose'] for k in ('lower degree', 'degree below', 'smaller degree', 'proper')),
        'for s/(s+1) the formula misses the 1 (a delta at t = 0); partial fractions need a proper fraction (Boyce and DiPrima 6.2)')
near('l15 s9 R(0.05) = 0.8364', lap(vas, 0.05), 0.8364, 5e-5)
near('l15 s9 wrong theta-only', 0.04 / 0.05, 0.8, 1e-12)
near('l15 q0 y\'-3y=0 from 2: Y = 2/(s-3) at s=4', lap(lambda t: 2 * math.exp(3 * t), 4), 2.0, 1e-8)
near('l15 q0 option d from 3/s', 2 / 4 + 3 / 16, (2 + 3 / 4) / 4, 1e-12)
near('l15 q1 residue 1/3', 1 / (1 + 2), 0.3333, 5e-5); near('l15 q1 other residue', 1 / (-2 - 1), -0.3333, 5e-5)

# ================================================================= l16 Euler
near('l16 s0 two steps of 0.5', euler(grow, 0, 1.0, 0.5, 2), 2.25, 1e-12)
near('l16 s1 four steps of 0.25', euler(grow, 0, 1.0, 0.25, 4), 2.4414, 5e-5)
near('l16 s1 gaps 0.47 and 0.28', E - 2.25, 0.47, 5e-3); near('l16 s1 gap 0.28', E - 1.25 ** 4, 0.28, 5e-3)
near('l16 s2 monthly compounding', euler(lambda t, y: 0.05 * y, 0, 1.0, 1 / 12, 12), 1.051162, 5e-7)
near('l16 s2 continuous', math.exp(0.05), 1.051271, 5e-7)
eerr = {h: E - float(euler(grow, 0, 1.0, h, round(1 / h))) for h in (0.1, 0.05, 0.025, 0.0125, 0.02, 0.01)}
near('l16 s3 error at h=0.1', eerr[0.1], 0.124539, 5e-7); near('l16 s3 error at h=0.05', eerr[0.05], 0.064984, 5e-7)
near('l16 s3 error at h=0.01', eerr[0.01], 0.013468, 5e-7); near('l16 s3 ratio 1.92', eerr[0.1] / eerr[0.05], 1.92, 5e-3)
near('l16 s3 fitted order 0.964', order([eerr[h] for h in (0.1, 0.05, 0.025, 0.0125)], [0.1, 0.05, 0.025, 0.0125]), 0.964, 5e-4)
chk('l16 s3 order tends to 1 as h falls', abs(order([E - float(euler(grow, 0, 1.0, h, round(1 / h))) for h in (1e-3, 5e-4)], [1e-3, 5e-4]) - 1) < 2e-3)
near('l16 s3 one-step error is about (h^2/2) y\'\'', (math.exp(0.01) - 1.01) / 0.01 ** 2, 0.5, 5e-3)
vf = lambda t, r: 0.5 * (0.04 - r)
path = [0.06]
for _ in range(4):
    path.append(path[-1] + 0.125 * (0.04 - path[-1]))
chk('l16 s4 quarterly path 5.75, 5.5313, 5.3398, 5.1724 %', np.allclose(np.array(path[1:]) * 100, [5.75, 5.5313, 5.3398, 5.1724], atol=5e-5), str(path))
m12 = float(euler(vf, 0, 0.06, 1 / 12, 12)); q4 = float(euler(vf, 0, 0.06, 0.25, 4))
near('l16 s4 monthly 5.2001%', m12 * 100, 5.2001, 5e-5); near('l16 s4 exact 5.2131%', vas(1) * 100, 5.2131, 5e-5)
chk('l16 s4 Euler undershoots; a third of the step gives about a third of the error', q4 < vas(1) and abs((vas(1) - m12) / (vas(1) - q4) - 1 / 3) < 0.02)
cen = lambda t, z: np.array([z[1], -z[0]])
ze = euler(cen, 0, [1.0, 0.0], 0.1, 63)
near('l16 s5 Euler radius after 63 steps', np.hypot(*ze), 1.3681, 5e-5); near('l16 s5 wrong 1.01^63', 1.01 ** 63, 1.8717, 5e-5)
near('l16 s5 end point of the drawn path', ze[0], 1.3681, 5e-5); near('l16 s5 end point y', ze[1], 0.0056, 5e-5)
chk('l16 s5 63 steps is one turn to within a hundredth of a radian', abs(63 * math.atan(0.1) - 2 * math.pi) < 0.01)
ys = [1.0]
for _ in range(4):
    ys.append(ys[-1] * (1 - 10 * 0.25))
chk('l16 s6 Euler path 1, -1.5, 2.25, -3.375, 5.0625', ys == [1, -1.5, 2.25, -3.375, 5.0625])
chk('l16 s6 true values 0.0821, 0.0067, 0.0006, 0.0000454', np.allclose([math.exp(-2.5), math.exp(-5), math.exp(-7.5)], [0.0821, 0.0067, 0.0006], atol=5e-5) and abs(math.exp(-10) - 4.54e-5) < 5e-8)


def euler_decays(lmb, h, n=40000):
    return abs((1 - h * lmb) ** n) < 1e-6


chk('l16 s7 Euler on y\'=-10y decays for h just under 0.2 and grows just over', euler_decays(10, 0.1999) and abs((1 - 10 * 0.2001) ** 40000) > 1e3)
chk('l16 s7 factor 0.5 at h=0.05 and 0 at h=0.1', abs(1 - 10 * 0.05 - 0.5) < 1e-15 and 1 - 10 * 0.1 == 0)
chk('l16 q2 limit 2/50 and factor 0 at 0.02', euler_decays(50, 0.0399) and not euler_decays(50, 0.0401) and abs(1 - 50 * 0.02) < 1e-15)
# finding 5: at h = 2/lambda itself the factor is -1; the lesson's own test |1 - h lambda| < 1 fails there
chk('l16 s7 at h = 0.2 exactly the Euler factor is -1: the steps neither shrink nor grow', abs((1 - 10 * 0.2) ** 4001 + 1) < 1e-12)
qs = [L16['screens'][7]['question'], L16['quiz'][2]['question'], L17['screens'][7]['question'], REV['items'][5]['question'], REV['items'][7]['question'], HW['items'][3]['question']]
finding(5, 'six questions ask for "the largest stable h" and key the limit 2/lambda (or 2.7853/lambda), where the lesson\'s strict test fails',
        not any('largest stable' in q for q in qs),
        'the stable steps are h < limit, an open interval with no largest member; at the limit |factor| = 1')
w = L16['screens'][8]['widget']
ns = widget_check('l16 s8 euler / observed_order', w)
# finding 3: console lines that the taught code does not print (last digits)
e10 = repr(float(ns['euler'](grow, 0, 1.0, 0.1, 10)[1][-1]))
oo = repr(ns['observed_order']([0.01, 0.0025], [0.1, 0.05]))
near('l16 s8 the taught loop gives 1.1^10 to 1e-12', float(e10), 1.1 ** 10, 1e-12)
cl16 = L16['screens'][8]['canvas']['params']['lines']
L16_CONSOLE_OK = cl16[2].strip() == e10 and (cl16[4].strip() == oo or 'round(' in cl16[3])
L16_DETAIL = f'euler loop prints {e10}, console says {cl16[2]}; observed_order prints {oo} here (1.9999999999999987 in Pyodide), console says {cl16[4]}'
loan = lambda t: 200000 - 100000 * math.exp(0.06 * t)
near('l16 s9 loan closed form by ODE solver', ivp(lambda t, L: [0.06 * L[0] - 12000], [100000], 1)[0], loan(1), 1e-5)
near('l16 s9 continuous 93,816.35', loan(1), 93816.35, 5e-3)
Lm = 100000.0
for _ in range(12):
    Lm = Lm * 1.005 - 1000
near('l16 s9 the bank schedule (0.5% then 1,000) is Euler with h = 1/12', Lm, float(euler(lambda t, L: 0.06 * L - 12000, 0, 100000.0, 1 / 12, 12)), 1e-6)
near('l16 s9 monthly 93,832.22', Lm, 93832.22, 5e-3); near('l16 s9 gap 15.87', Lm - loan(1), 15.87, 5e-3)
near('l16 q0 one step on y\'=t+y', 1 + 0.1 * (0 + 1), 1.1, 1e-12); near('l16 q0 wrong: slope at the end (backward Euler)', 1.01 / 0.9, 1.1222, 5e-5)
near('l16 q1 Euler at the equilibrium with h=1', float(euler(vf, 0, 0.04, 1.0, 50)), 0.04, 1e-15)
near('l16 q3 error at h=0.02 is about 0.027', eerr[0.02], 0.027, 5e-4)

# ================================================================= l17 Runge-Kutta
near('l17 s0 one midpoint step', float(midpoint(grow, 0, 1.0, 0.1, 1)), 1.105, 1e-12)
near('l17 s0 ten midpoint steps', float(midpoint(grow, 0, 1.0, 0.1, 10)), 2.714081, 5e-7)
near('l17 s0 midpoint error', E - float(midpoint(grow, 0, 1.0, 0.1, 10)), 0.004201, 5e-7)
chk('l17 midpoint is second order', abs(order([E - float(midpoint(grow, 0, 1.0, h, round(1 / h))) for h in (0.01, 0.005)], [0.01, 0.005]) - 2) < 0.01)
near('l17 s1 two RK4 steps of 0.5', float(rk4(grow, 0, 1.0, 0.5, 2)), 2.7173, 5e-5)
near('l17 s1 factor 1.6484375', float(rk4(grow, 0, 1.0, 0.5, 1)), 1.6484375, 1e-12)
chk('l17 s1 within 0.001 of e', abs(E - float(rk4(grow, 0, 1.0, 0.5, 2))) < 1e-3)
k1 = 1.0; k2 = 1 + 0.05 * k1; k3 = 1 + 0.05 * k2; k4 = 1 + 0.1 * k3
chk('l17 s2 slopes 1, 1.05, 1.0525, 1.10525 and y1', (k1, k2, k3, k4) == (1.0, 1.05, 1.0525, 1.10525) or np.allclose((k2, k3, k4), (1.05, 1.0525, 1.10525), atol=1e-14))
near('l17 s2 y1 = 1.1051708333', float(rk4(grow, 0, 1.0, 0.1, 1)), 1.1051708333, 5e-11)
near('l17 s2 equals the Taylor polynomial of e^h to h^4', float(rk4(grow, 0, 1.0, 0.1, 1)), sum(0.1 ** k / math.factorial(k) for k in range(5)), 1e-15)
rerr = {h: E - float(rk4(grow, 0, 1.0, h, round(1 / h))) for h in (1.0, 0.5, 0.2, 0.1, 0.05, 0.025, 0.0125)}
near('l17 s3 ten steps reach 2.7182797', float(rk4(grow, 0, 1.0, 0.1, 10)), 2.7182797, 5e-8)
near('l17 s3 error 2.084e-6', rerr[0.1], 2.084e-6, 5e-10); near('l17 s3 error 1.358e-7', rerr[0.05], 1.358e-7, 5e-11)
near('l17 s3 ratio 15.35', rerr[0.1] / rerr[0.05], 15.35, 5e-3)
near('l17 s3 measured order 4', order([rerr[h] for h in (0.1, 0.05, 0.025, 0.0125)], [0.1, 0.05, 0.025, 0.0125]), 4, 0.05)
pts = {p['id']: p['y'] for p in L17['screens'][3]['canvas']['state']['points']}
chk('l17 s3 chart points are log10 of the errors', np.allclose([pts['e0'], pts['e1'], pts['e2'], pts['e3']], [math.log10(eerr[h]) for h in (0.1, 0.05, 0.025, 0.0125)], atol=6e-4)
    and np.allclose([pts['k0'], pts['k1'], pts['k2'], pts['k3']], [math.log10(rerr[h]) for h in (0.1, 0.05, 0.025, 0.0125)], atol=6e-4))
e1e5 = E - (1 + 1e-5) ** 100000
near('l17 s4 Euler with 100,000 steps errs by 1.36e-5', e1e5, 1.36e-5, 5e-8)
chk('l17 s4 ten RK4 steps (40 evaluations) beat it', rerr[0.1] < e1e5 and 100000 / 40 == 2500)
pts = {p['id']: p['y'] for p in L17['screens'][4]['canvas']['state']['points']}
chk('l17 s4 chart: cost points are right', np.allclose([pts[k] for k in ('v0', 'v1', 'v2', 'v3', 'v4')], [math.log10(rerr[h]) for h in (1.0, 0.5, 0.2, 0.1, 0.05)], atol=6e-4)
    and np.allclose([pts['u1'], pts['u2'], pts['u3'], pts['u4']], [math.log10(E - (1 + 1 / n) ** n) for n in (100, 1000, 10000, 100000)], atol=6e-4))
zr = rk4(cen, 0, [1.0, 0.0], 0.1, 63)
near('l17 s5 RK4 radius after 63 steps', np.hypot(*zr), 0.9999995630469712, 1e-12)
Ri = abs(sum((0.1j) ** k / math.factorial(k) for k in range(5)))
near('l17 s5 modulus per step 1 - 6.9e-9', 1 - Ri, 6.9e-9, 5e-11)
chk('l17 s5 RK4 shrinks this orbit, Euler grows it', Ri < 1 < abs(1 + 0.1j))


def bad_step(f, t, y, h):
    k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k1); k4 = f(t + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


hs = [0.1, 0.05, 0.025, 0.0125]
berr = [abs(E - float(rk4(grow, 0, 1.0, h, round(1 / h), step=bad_step))) for h in hs]
near('l17 s6 the slipped step gives 2.71613', float(rk4(grow, 0, 1.0, 0.1, 10, step=bad_step)), 2.71613, 5e-6)
near('l17 s6 its measured order is 1.979', order(berr, hs), 1.979, 5e-4)
near('l17 s6 it matches Taylor only to h^2 (h^3 coefficient 1/12)', (float(bad_step(grow, 0, 1.0, 0.01)) - (1 + 0.01 + 0.01 ** 2 / 2)) / 0.01 ** 3, 1 / 12, 1e-3)
nl = lambda t, y: -y * y + math.sin(t)
ref = ivp(lambda t, y: [nl(t, y[0])], [1.0], 1)[0]
chk('l17 s6 the slip is second order on a nonlinear equation too', abs(order([abs(ref - float(rk4(nl, 0, 1.0, h, round(1 / h), step=bad_step))) for h in (0.02, 0.01)], [0.02, 0.01]) - 2) < 0.1)
chk('l17 RK4 is fourth order on a nonlinear equation', abs(order([abs(ref - float(rk4(nl, 0, 1.0, h, round(1 / h)))) for h in (0.1, 0.05)], [0.1, 0.05]) - 4) < 0.2)
R = lambda z: 1 - z + z ** 2 / 2 - z ** 3 / 6 + z ** 4 / 24
near('l17 s7 R(2.5) = 0.6484', R(2.5), 0.6484, 5e-5); near('l17 s7 R(3) = 1.375', R(3), 1.375, 1e-12)
zlim = brentq(lambda z: abs(R(z)) - 1, 2.5, 3)
near('l17 s7 |R| = 1 at 2.7853', zlim, 2.7853, 5e-5)
chk('l17 s7 |R| < 1 on the whole of (0, 2.7853)', max(abs(R(z)) for z in np.linspace(1e-6, zlim - 1e-6, 20001)) < 1)
near('l17 s7 the RK4 step on y\'=-10y is exactly R(10h)', float(rk4_step(lambda t, y: -10 * y, 0, 1.0, 0.27)), R(2.7), 1e-13)
chk('l17 s7 simulation: h = 0.278 decays, h = 0.279 grows', abs(float(rk4(lambda t, y: -10 * y, 0, 1.0, 0.278, 20000))) < 1e-6 and abs(float(rk4(lambda t, y: -10 * y, 0, 1.0, 0.279, 20000))) > 1e6)
near('l17 s7 about 1.4 times Euler\'s limit', zlim / 2, 1.4, 0.05)
w = L17['screens'][9]['widget']
ns = widget_check('l17 s9 rk4_step / rk4', w)
chk('l17 s9 console: one step prints 1.1051708333333332', repr(float(ns['rk4_step'](grow, 0, 1.0, 0.1))) == '1.1051708333333332')
r10 = repr(float(ns['rk4'](grow, 0, 1.0, 0.1, 10)[1][-1]))
cl17 = L17['screens'][9]['canvas']['params']['lines']
finding(3, 'console lines print digits the taught code does not produce: l14 screens[9] lines[1]; l16 screens[8] lines[2], lines[4]; l17 screens[9] lines[3]',
        L14_CONSOLE_OK and L16_CONSOLE_OK and cl17[3].strip() == r10, L14_DETAIL + '; ' + L16_DETAIL + f'; rk4 ten steps prints {r10}, console says {cl17[3]}')
EX = y4(1)
o7 = rk4(osc_np := (lambda t, z: np.array([z[1], -2 * z[1] - 5 * z[0]])), 0, [1.0, 0.0], 1 / 7, 7)[0]
o5 = rk4(osc_np, 0, [1.0, 0.0], 1 / 5, 5)[0]; o6 = rk4(osc_np, 0, [1.0, 0.0], 1 / 6, 6)[0]
chk('l17 s9 seven RK4 steps are within 5e-5 of 0.014164; five and six are not', abs(o7 - EX) < 5e-5 <= min(abs(o5 - EX), abs(o6 - EX)), f'{o5 - EX} {o6 - EX} {o7 - EX}')
near('l17 s9 RK4 is exact for y\' = t^3 (Simpson)', float(rk4(lambda t, y: t ** 3, 0, 0.0, 0.5, 2)), 0.25, 1e-15)
near('l17 s9 for y\'=f(t) one RK4 step is Simpson\'s rule', float(rk4(lambda t, y: math.cos(t), 0, 0.0, 0.6, 1)), 0.6 / 6 * (1 + 4 * math.cos(0.3) + math.cos(0.6)), 1e-15)
A = np.array([[0.0, 1.0], [-5.0, -2.0]])


def euler_osc_err(n):
    return abs((np.linalg.matrix_power(np.eye(2) + A / n, n) @ np.array([1.0, 0.0]))[0] - EX)


n_need = next(n for n in range(2, 60000) if euler_osc_err(n) < 5e-5 and euler_osc_err(n + 1) < 5e-5)
chk('l17 s9 / homework: Euler needs about 16,000 steps on the oscillator for 5e-5', 15000 < n_need < 17000, str(n_need))
w = L17['screens'][10]['widget']
ns = widget_check('l17 s10 oscillator_ivp', w)
sol = solve_ivp(lambda t, z: [z[1], -2 * z[1] - 5 * z[0]], (0, 1), [1, 0], rtol=1e-10, atol=1e-12)
ivp_err = abs(sol.y[0, -1] - EX)
chk('l17 s10 default solve_ivp method is the RK45 pair', solve_ivp(grow, (0, 1), [1.0]).message is not None and solve_ivp.__defaults__[0] == 'RK45', str(solve_ivp.__defaults__))
shown = L17['screens'][10]['canvas']['params']['lines'][3].strip().rstrip('.')
finding(2, 'l17 screens[10] console lines[3] shows solve_ivp agreeing with the closed form to 12 decimals; it agrees to 10',
        repr(float(sol.y[0, -1])).startswith(shown) and abs(float(shown) - EX) < 1e-9,
        f'solve_ivp gives {float(sol.y[0, -1])!r} (error {ivp_err:.1e}); the console prints {shown}..., the digits of the closed form')
chk('l17 s10 explain: error near 1e-11 (within a factor of 30 either way)', 3e-13 < max(abs(ns['oscillator_ivp'](T) - math.exp(-T) * (math.cos(2 * T) + 0.5 * math.sin(2 * T))) for T in (0.5, 1, 2, 3)) < 3e-10, str(ivp_err))
spread = lambda n: abs(float(rk4(lambda t, x: -40 * x, 0, 1.0, 1 / n, n * 200)))
chk('l17 s11 with lambda = 40: 14 RK4 steps a year grow, 15 decay', spread(14) > 1 and spread(15) < 1e-6)
near('l17 s11 z at 14 steps', 40 / 14, 2.857, 5e-4); chk('l17 s11 Euler needs more than 20', abs(1 - 40 / 20) == 1 and abs(1 - 40 / 21) < 1)
near('l17 q0 one RK4 step on y\'=-y', float(rk4(lambda t, y: -y, 0, 1.0, 0.1, 1)), 0.9048375, 5e-9)
near('l17 q1 midpoint with h=0.2', float(midpoint(grow, 0, 1.0, 0.2, 1)), 1.22, 1e-12)
near('l17 q3 the step factor on y\'=-10y at h=0.3', float(rk4_step(lambda t, y: -10 * y, 0, 1.0, 0.3)), 1.375, 1e-12)
# finding 4: the lesson defines R(z) = 1 - z + z^2/2 - ..., z = h lambda > 0, so the factor is R(3); R(-3) is 16.375
near('l17 q3 with the lesson\'s own R, R(-3) = 16.375 and R(3) = 1.375', R(-3), 16.375, 1e-12)
q3 = json.dumps(L17['quiz'][3])
finding(4, 'l17 quiz[3] writes the factor as R(-3) = 1.375; with screens[7]\'s R(z), z = h lambda = 3, it is R(3)', 'R(-3)' not in q3,
        'R(-3) = 16.375 with the R(z) the lesson defines; R(-3) = 1.375 is the numerics convention z = h lambda < 0')

# ================================================================= l18 four decimal places
kap, th, r0, T = 0.5, 0.04, 0.06, 5.0
I5 = quad(vas, 0, 5)[0]
D = math.exp(-I5)
near('l18 s0 I(5) = 0.236717', I5, 0.236717, 5e-7); near('l18 s0 price 78.92', 100 * D, 78.9215, 5e-5)
near('l18 s1 closed form for I(T)', th * T + (r0 - th) * (1 - math.exp(-kap * T)) / kap, I5, 1e-12)
near('l18 s1 factor 1.835830', (1 - math.exp(-2.5)) / 0.5, 1.835830, 5e-7)
near('l18 s0 wrong values', 100 * math.exp(-0.2), 81.87, 5e-3); near('l18 s0 wrong 6%', 100 * math.exp(-0.3), 74.08, 5e-3)
vsys = lambda t, y: np.array([kap * (th - y[0]), y[0]])
De = lambda n: math.exp(-euler(vsys, 0, [r0, 0.0], T / n, n)[1])
Dr = lambda n: math.exp(-rk4(vsys, 0, [r0, 0.0], T / n, n)[1])
near('l18 s2 caption formula equals Euler on the system (n=10)', math.exp(-(0.2 + 0.04 * (1 - (1 - 2.5 / 10) ** 10))), De(10), 1e-13)
for n, v in ((10, 0.788402), (100, 0.789134), (1000, 0.789207), (60, 0.789080)):
    near(f'l18 Euler D with {n} steps', De(n), v, 5e-7)
chk('l18 s2 error falls tenfold with tenfold n', abs((D - De(100)) / (D - De(1000)) - 10) < 0.2 and abs((D - De(10)) / (D - De(100)) - 10) < 0.2)
ee = {n: D - De(n) for n in range(1, 400)}
near('l18 s3 error at 162', ee[162] * 1e6, 50.02, 5e-3); near('l18 s3 error at 163', ee[163] * 1e6, 49.71, 5e-3)
chk('l18 s3 163 is the smallest n with Euler error below 5e-5, and every larger n stays below', min(n for n in ee if abs(ee[n]) < 5e-5) == 163 and all(abs(ee[n]) < 5e-5 for n in range(163, 400)))
near('l18 s3 hint: error about 8.1e-3/n', ee[200] * 200, 8.1e-3, 1e-4)
for n, v, e in ((1, 0.807298, 18083), (2, 0.789608, 393), (4, 0.789229, 13.9), (8, 0.789216, 0.67)):
    near(f'l18 s4 RK4 D with {n} steps', Dr(n), v, 5e-7); near(f'l18 s4 RK4 error x1e6 with {n} steps', abs(Dr(n) - D) * 1e6, e, 0.5 if e > 100 else 0.05 if e > 1 else 0.005)
near('l18 s4 ten RK4 steps err by 2.6e-7', abs(Dr(10) - D), 2.6e-7, 5e-9)
rk_min = min(n for n in range(1, 20) if abs(Dr(n) - D) < 5e-5)
chk('l18 s4 / summary: 4 is the fewest RK4 steps of any count, not only of 1, 2, 4, 8', rk_min == 4, f'smallest n is {rk_min}, error at 3 is {abs(Dr(3) - D):.2e}')
chk('l18 s5 Euler errors 618.0, 1964.6, 1015.1, 508.2, 253.7 (x1e-6)', np.allclose([ee[n] * 1e6 for n in (2, 4, 8, 16, 32)], [618.0, 1964.6, 1015.1, 508.2, 253.7], atol=0.06))
r1 = r0 + 2.5 * kap * (th - r0)
chk('l18 s5 with 2 steps the rate overshoots below 4% and the factor is -0.25', abs(r1 - 0.035) < 1e-15 and 1 - 2.5 * kap == -0.25)
near('l18 s6 monthly Euler error 1.35e-4', D - De(60), 1.35e-4, 5e-7)
chk('l18 s6 prints 0.7891 against 0.7892; prices differ by 1.35p', f'{De(60):.4f}' == '0.7891' and f'{D:.4f}' == '0.7892' and abs(100 * (D - De(60)) - 0.0135) < 5e-5)
# finding 1: the band does not guarantee the printed digits
inside = D + 4e-5
chk('l18 s3 counterexample: 0.789255 is within 5e-5 of D and prints 0.7893', abs(inside - D) < 5e-5 and f'{inside:.4f}' == '0.7893')
chk('l18 s3 converse counterexample: 0.789151 prints 0.7892 and is outside the band', f'{0.789151:.4f}' == '0.7892' and abs(0.789151 - D) > 5e-5)
finding(1, 'l18 screens[3].prose: "|D_num - D| < 5e-5: then the printed 0.7892 agrees" is false',
        'then the printed 0.7892 agrees' not in L18['screens'][3]['prose'],
        '0.789255 is 4e-5 from D = 0.789215 and prints 0.7893; a band of half a unit does not fix the rounded digit')
# noise: closed form and Monte Carlo
B = (1 - math.exp(-kap * T)) / kap
varI = (T - 2 * B + (1 - math.exp(-2 * kap * T)) / (2 * kap)) / kap ** 2          # per sigma^2
near('l18 s7 half Var(I) per sigma^2 is 4.643', varI / 2, 4.643204, 5e-7)
sig = 0.01
Dn = D * math.exp(0.5 * varI * sig ** 2)
near('l18 s7 noisy D = 0.789581', Dn, 0.789581, 5e-7); near('l18 s7 price gap 0.0367', 100 * (Dn - D), 0.0367, 5e-5)
rng = np.random.default_rng(18)
nst, npath, acc, acc2, cnt, rT = 250, 100_000, 0.0, 0.0, 0, 0.0
dt = T / nst
a = math.exp(-kap * dt); sd = sig * math.sqrt((1 - a * a) / (2 * kap))               # exact OU transition
for _ in range(4):
    z = rng.standard_normal((nst, npath))
    for sgn in (1, -1):
        r = np.full(npath, r0); I = np.zeros(npath)
        for k in range(nst):
            rn = th + (r - th) * a + sd * sgn * z[k]
            I += 0.5 * (r + rn) * dt
            r = rn
        d = np.exp(-I)
        acc += d.sum(); acc2 += (d * d).sum(); cnt += npath; rT += r.sum()
mc = acc / cnt; se = math.sqrt(acc2 / cnt - mc * mc) / math.sqrt(cnt)
chk('l18 s7 Monte Carlo: E[e^{-I}] under noise is 0.789581, above the no-noise 0.789215', abs(mc - Dn) < 4 * se + 2e-6 and (mc - D) > 6 * se, f'mc {mc:.6f} se {se:.1e}')
chk('l18 s7 Monte Carlo: the no-noise path is the expected rate path', abs(rT / cnt - vas(5)) < 1e-4)
w = L18['screens'][9]['widget']
ns = widget_check('l18 s9 vasicek_rhs / discount_* / steps_to_4dp', w)
chk('l18 s9 console values', repr(ns['discount_exact'](0.06, 0.5, 0.04, 5)) == '0.7892149197923242' and abs(ns['discount_rk4'](0.06, 0.5, 0.04, 5, 4) - 0.7892288673245939) < 1e-15)
chk('l18 s9 doubling: RK4 4, Euler 256; Euler misses at 128', ns['steps_to_4dp'](ns['discount_rk4'], .06, .5, .04, 5) == 4 and ns['steps_to_4dp'](ns['discount_euler'], .06, .5, .04, 5) == 256 and abs(ee[128]) > 5e-5)
near('l18 s9 the prelude\'s discount_euler is Euler on the system', ns['discount_euler'](.06, .5, .04, 5, 60), De(60), 1e-14)
# finding 8: steps_to_4dp is the one-run rule that screens[8] told the learner to leave out
finding(8, 'l18 screens[9]: steps_to_4dp stops at the first n within 5e-5 of the closed form, the rule screens[8] rejects, with no word saying so',
        any(k in L18['screens'][9]['prose'] + L18['screens'][9]['explain']['text'] for k in ('two runs', 'successive', 'half of the check', 'not the full check')),
        'screens[8] distractor d1 is this rule ("trusts one lucky grid"); the code screen should say it is only the search')
w = L18['screens'][10]['widget']
ns = widget_check('l18 s10 discount_ivp', w)
d_ivp = abs(ns['discount_ivp'](0.06, 0.5, 0.04, 5) - D)
chk('l18 s10 solve_ivp agrees with the closed form to about 2e-12 (within a factor of 10)', d_ivp < 2e-11, repr(d_ivp))
near('l18 q0 flat 5%', math.exp(-0.25), 0.7788, 5e-5)
chk('l18 q1 only 0.789180 is inside the band', [abs(v - 0.789215) < 5e-5 for v in (0.789180, 0.789134, 0.789080, 0.789290)] == [True, False, False, False])
near('l18 q2 first-order scaling', 100 * 8.1 / 4, 200, 10); near('l18 q2 wrong: square root', 100 * math.sqrt(8.1 / 4), 142, 3)
near('l18 q3 1.4e-5/16', 1.4e-5 / 16, 9e-7, 5e-8); near('l18 q3 true 6.7e-7', abs(Dr(8) - D), 6.7e-7, 5e-9)

# ================================================================= review-4 and homework-4
near('rev 0', lap(lambda t: t ** 3, 2), 0.375, 1e-9); near('rev 0 wrong', 1 / 16, 0.0625, 0)
near('rev 1', lap(lambda t: 2 * math.exp(0.03 * t), 0.05, 20000), 100, 1e-4); near('rev 1 wrong', 2 / 0.08, 25, 1e-12)
near('rev 2 y\'+3y=3 from 0', ivp(lambda t, y: [3 - 3 * y[0]], [0], 0.8)[0], 1 - math.exp(-2.4), 1e-9)
yr = lambda t: 2 * math.exp(-t) - math.exp(-2 * t)
near('rev 3 transform of 2e^{-t}-e^{-2t} at s=0.6', lap(yr, 0.6), (0.6 + 3) / (1.6 * 2.6), 1e-9)
near('rev 3 y(1)', yr(1), 0.6004, 5e-5); near('rev 3 wrong', 2 / E + math.exp(-2), 0.8711, 5e-5)
near('rev 4', float(euler(lambda t, y: -2 * y, 0, 1.0, 0.25, 2)), 0.25, 1e-15); near('rev 4 exact', 1 / E, 0.3679, 5e-5)
Am = np.array([[-2.0, 1.0], [1.0, -2.0]])
chk('rev 5 eigenvalues -1 and -3', np.allclose(sorted(np.linalg.eigvals(Am)), [-3, -1]))
sr = lambda h: max(abs(np.linalg.eigvals(np.eye(2) + h * Am)))
chk('rev 5 Euler on the system: spectral radius below 1 for h < 2/3, above for h > 2/3', sr(0.666) < 1 < sr(0.667) and sr(2 / 3) > 1 - 1e-12)
xs = np.array([1.0, 0.3])
chk('rev 5 simulation: h = 0.66 decays, h = 0.67 grows', np.linalg.norm(np.linalg.matrix_power(np.eye(2) + 0.66 * Am, 4000) @ xs) < 1e-6 and np.linalg.norm(np.linalg.matrix_power(np.eye(2) + 0.67 * Am, 4000) @ xs) > 1e6)
near('rev 6', 48 / 16, 3, 0); near('rev 7', zlim / 25, 0.1114, 5e-5); near('rev 7 wrong', 2 / 25, 0.08, 1e-15)
near('rev 8 estimate 162', 60 * 1.35 / 0.5, 162, 1e-9); near('rev 8 wrong: square root', 60 * math.sqrt(2.7), 99, 0.5)
near('hw 0', lap(lambda t: t * math.exp(-2 * t), 1), 0.1111, 5e-5)
near('hw 1 y\'\'-y=0 from (0,2) is 2 sinh t', ivp(lambda t, z: [z[1], z[0]], [0, 2], 1.2)[0], 2 * math.sinh(1.2), 1e-8)
yh = lambda t: math.exp(-t) * (2 * math.cos(2 * t) + 0.5 * math.sin(2 * t))
near('hw 2 transform at s=0.5', lap(yh, 0.5, 80), (2 * 0.5 + 3) / (0.25 + 1 + 5), 1e-8)
chk('hw 2 wrong option differs', abs(lap(lambda t: math.exp(-t) * (2 * math.cos(2 * t) + math.sin(2 * t)), 0.5, 80) - 4 / 6.25) > 0.05)
chk('hw 3 eigenvalues -1 and -20: Euler decays for h = 0.0999 and grows for 0.1001', max(abs(1 - 0.0999 * 20), abs(1 - 0.0999)) < 1 < abs(1 - 0.1001 * 20))
chk('hw 3 rate 20 a year reverts in weeks, rate 1 in about a year', 1 < 52 * math.log(2) / 20 < 3 and 0.5 < math.log(2) / 1 < 1)
near('hw 4 prediction', 20.84 / 16, 1.30, 5e-3); near('hw 4 wrong', 20.84 / 2, 10.42, 1e-12)
w = HW['items'][5]['widget']
ns = widget_check('hw 5 rk4 / match_to_4dp', w)
bond = lambda t, y: np.array([0.5 * (0.04 - y[0]), -y[0] * y[1]])
near('hw 5 the bond as (r, D)\' = (0.5(0.04-r), -rD) has D(5) = closed form', ivp(bond, [0.06, 1.0], 5)[1], D, 1e-10)
chk('hw 5 bond stops at 8 and oscillator at 16', ns['match_to_4dp'](bond, [0.06, 1.0], 5, D, k=1)[0] == 8 and ns['match_to_4dp'](osc_np, [1.0, 0.0], 1, EX)[0] == 16)
# finding 9: "stops one doubling after RK4 first meets the band" holds for the three tests, not as a rule
first_in = lambda f, y0, T_, ex, k: next(n for n in (1, 2, 4, 8, 16, 32, 64) if abs(np.atleast_1d(rk4(f, 0, y0, T_ / n, n))[k] - ex) < 5e-5)
chk('hw 5 in the three tests the first n in the band is 4, 8, 8 and the check stops at 8, 16, 16',
    (first_in(bond, [0.06, 1.0], 5, D, 1), first_in(osc_np, [1.0, 0.0], 1, EX, 0), first_in(grow, [1.0], 1, E, 0)) == (4, 8, 8))
cx = ns['match_to_4dp'](lambda t, y: -y, 1.0, 1, math.exp(-1) - 4.9e-5)
chk('hw 5 counterexample: with exact shifted down by 4.9e-5 the check stops at the first n in the band', cx is not None and cx[0] == first_in(lambda t, y: -y, [1.0], 1, math.exp(-1) - 4.9e-5, 0), str(cx))
finding(9, 'homework-4 items[5].explain: "So it stops one doubling after RK4 first meets the band" stated as a consequence',
        'So it stops one doubling after RK4 first meets the band.' not in HW['items'][5]['explain']['text'],
        'it stops at the first n in the band whenever the run before is within tol of it; true of the three tests only')
near('hw 6 model: 4- and 8-step RK4 runs agree within 5e-5', abs(Dr(8) - Dr(4)), 1.33e-5, 5e-7)
near('hw 6 model: 5p on 100 is 5e-4 in D, ten times the band', 0.05 / 100 / 5e-5, 10, 1e-9)
near('hw 7 option a 1/0.03', lap(lambda t: math.exp(0.02 * t), 0.05, 20000), 1 / 0.03, 1e-5)
# finding 10: place words in feedback of a shuffled multi
it = HW['items'][7]
finding(10, 'homework-4 items[7].feedback.correct names options by place ("The first and the third") on a multi that shuffles by default',
        it['widget'].get('shuffle') is False or not any(k in it['feedback']['correct'] for k in ('first', 'third')),
        'AUTHORING: choice and multi shuffle by default, so the place words point at the wrong options')

print(f'\n{NPASS[0]} checks pass, {len(FAILS)} fail')
for f in FAILS:
    print('  failing:', f)
sys.exit(1 if FAILS else 0)
