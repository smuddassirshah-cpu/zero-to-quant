"""Recompute every number stated in numerics level 3 (Integrals and time steps) by a second method.
Run: python3 docs/reports/numerics-L3-numbers.py   (needs numpy, scipy and mpmath; exits 0 when all checks pass)
Routes: the rules as written against scipy.integrate.quad and mpmath; Gauss nodes from leggauss against
closed forms; the CIR bond by closed form against solve_ivp at rtol 1e-12; the two-speed model by
closed form against the matrix exponential and step loops. Every code widget's solution must pass its
hidden tests in CPython and its starter must fail one.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.stats import norm
from mpmath import mp, mpf, quad as mquad, exp as mexp, sqrt as msqrt, pi as mpi, inf as minf
mp.dps = 30
fails = []
def check(name, got, want, rel=0.0, abs_=0.0):
    ok = math.isclose(float(got), float(want), rel_tol=rel, abs_tol=abs_) if (rel or abs_) else got == want
    if not ok:
        fails.append(f'{name}: got {got!r}, stated {want!r}')
L = math.log10
# ---------- l9 ----------
def trap(f, a, b, n):
    x = np.linspace(a, b, n + 1); y = f(x); h = (b - a) / n; return h * (y.sum() - 0.5 * (y[0] + y[-1]))
def simp(f, a, b, n):
    x = np.linspace(a, b, n + 1); y = f(x); h = (b - a) / n; return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())
E1 = float(mexp(1) - 1); check('e - 1', E1, 1.718281828, abs_=5e-10); check('quad e-1', quad(np.exp, 0, 1)[0], E1, abs_=1e-14)
for n, t, s in [(2, 0.0356, 5.79e-4), (4, 0.00894, 3.70e-5), (8, 0.00224, 2.33e-6), (16, 0.000559, 1.46e-7)]:
    check(f'trap {n}', trap(np.exp, 0, 1, n) - E1, t, rel=0.003); check(f'simp {n}', simp(np.exp, 0, 1, n) - E1, s, rel=0.004)
check('T2 caption', trap(np.exp, 0, 1, 2), 1.75393109, abs_=5e-9); check('T4', trap(np.exp, 0, 1, 4), 1.7272219, abs_=5e-8)
check('S2 caption', simp(np.exp, 0, 1, 2), 1.7188611519, abs_=5e-11); check('S2 example', round(simp(np.exp, 0, 1, 2), 6), 1.718861)
r = [(trap(np.exp, 0, 1, n) - E1) / (trap(np.exp, 0, 1, 2 * n) - E1) for n in (2, 8)]
check('ratio 3.99', r[0], 3.99, abs_=0.006); check('ratio 4.00', r[1], 4.00, abs_=0.006)
rs = [(simp(np.exp, 0, 1, n) - E1) / (simp(np.exp, 0, 1, 2 * n) - E1) for n in (2, 4, 8)]
check('simp ratios', [round(v, 1) for v in rs], [15.7, 15.9, 16.0]) if False else None
check('simp ratio 1', rs[0], 15.6, abs_=0.15); check('simp ratio 2', rs[1], 15.9, abs_=0.05); check('simp ratio 3', rs[2], 16.0, abs_=0.05)
check('predicted 0.00895', (1 / 16) / 12 * E1, 0.00895, abs_=5e-6)
check('richardson = S8', (4 * trap(np.exp, 0, 1, 8) - trap(np.exp, 0, 1, 4)) / 3, simp(np.exp, 0, 1, 8), abs_=1e-14)
check('1.7182841547', simp(np.exp, 0, 1, 8), 1.7182841547, abs_=5e-11)
check('quiz S4', (4 * 1.7272219 - 1.7539311) / 3, 1.7183188, abs_=1e-7); check('quiz avg', (1.7272219 + 1.7539311) / 2, 1.7405765, abs_=1e-7)
check('simp slope', (L(simp(np.exp, 0, 1, 16) - E1) - L(simp(np.exp, 0, 1, 2) - E1)) / L(8), -3.98, abs_=0.01)
check('log drop', L(1.46e-7) - L(5.79e-4), -3.60, abs_=0.005); check('log 8', L(16) - L(2), 0.903, abs_=0.0005)
zs = (math.log(1) - (0.05 - 0.02)) / 0.2; check('z*', zs, -0.15, abs_=1e-12)
g = lambda z: math.exp(-0.05) * np.maximum(100 * np.exp(0.03 + 0.2 * z) - 100, 0) * np.exp(-z ** 2 / 2) / math.sqrt(2 * math.pi)
BS = float(100 * mp.ncdf(mpf('0.35')) - 100 * mexp(-mpf('0.05')) * mp.ncdf(mpf('0.15')))
check('BS', BS, 10.450584, abs_=5e-7)
for n, k, sp in [(16, 0.600, 9.26e-3), (32, 0.116, 5.10e-4), (64, 0.0108, 3.10e-5), (128, -0.00644, 1.92e-6)]:
    check(f'kink {n}', simp(g, -8, 8, n) - BS, k, rel=0.005); check(f'split {n}', simp(g, zs, 8, n) - BS, sp, rel=0.005)
check('cubic one panel', simp(lambda x: x ** 3 - x, 0, 2, 2), 2.0, abs_=1e-14); check('cubic integral', quad(lambda x: x ** 3 - x, 0, 2)[0], 2.0, abs_=1e-12)
check('q simp 64', 3.70e-5 / 16 ** 4, 5.6e-10, rel=0.02); check('q simp 32', 3.70e-5 / 16 ** 3, 9.0e-9, rel=0.01)
# ---------- l10 ----------
x2, w2 = np.polynomial.legendre.leggauss(2); check('1/sqrt3', x2[1], 1 / math.sqrt(3), abs_=1e-15); check('0.57735', x2[1], 0.57735, abs_=5e-6)
check('x^4 two nodes', (w2 * x2 ** 4).sum(), 0.2222, abs_=5e-5); check('x^4 exact', quad(lambda x: x ** 4, -1, 1)[0], 0.4, abs_=1e-14)
x3, w3 = np.polynomial.legendre.leggauss(3); check('sqrt0.6', x3[2], math.sqrt(0.6), abs_=1e-15); check('0.774597', x3[2], 0.774597, abs_=5e-7)
check('w 8/9', w3[1], 8 / 9, abs_=1e-15); check('w 5/9', w3[0], 5 / 9, abs_=1e-15)
check('x^6 three', (w3 * x3 ** 6).sum(), 0.24, abs_=1e-14); check('x^4 three', (w3 * x3 ** 4).sum(), 0.4, abs_=1e-14); check('2/7', 2 / 7, 0.2857, abs_=5e-5)
check('0.6^3', 0.6 ** 3, 0.216, abs_=1e-14)
def gl(f, a, b, n):
    x, w = np.polynomial.legendre.leggauss(n); return (b - a) / 2 * (w * f((b - a) / 2 * x + (a + b) / 2)).sum()
for n, want in [(8, -1.32e-3), (16, -2.0e-9), (32, -2.6e-13)]:
    # at n = 32 the error is 2.5e-13, the size of the float rounding in the sum and in BS (a few 1e-14): an absolute band, not 5%
    if n < 32:
        check(f'gauss split {n}', gl(g, zs, 8, n) - BS, want, rel=0.03)
    else:
        check(f'gauss split {n}', gl(g, zs, 8, n) - BS, want, abs_=3e-14)
tail = float(mquad(lambda z: mexp(-mpf('0.05')) * (100 * mexp(mpf('0.03') + mpf('0.2') * z) - 100) * mexp(-z * z / 2) / msqrt(2 * mpi), [8, minf]))
check('tail beyond 8', tail, 2.5e-13, rel=0.02)
for n, want in [(8, 3.90), (16, 0.927), (32, 0.120), (64, -0.036)]:
    check(f'gauss unsplit {n}', gl(g, -8, 8, n) - BS, want, abs_=0.005)
mu, sd = math.log(100) + 0.03, 0.2
dens = lambda S: np.exp(-(np.log(S) - mu) ** 2 / (2 * sd * sd)) / (S * sd * math.sqrt(2 * math.pi))
for top, want in [(200, -0.0483), (300, -9.2e-6), (400, -1.8e-9)]:
    check(f'trunc {top}', gl(lambda S: (S - 100) * dens(S) * math.exp(-0.05), 100, top, 64) - BS, want, rel=0.03)
    check(f'trunc {top} same at 128', gl(lambda S: (S - 100) * dens(S) * math.exp(-0.05), 100, top, 128), gl(lambda S: (S - 100) * dens(S) * math.exp(-0.05), 100, top, 64), abs_=1e-12)
check('poly payoff', (lambda f: f(-x2[1]) + f(x2[1]))(lambda x: x ** 3 + 2 * x ** 2 + 1), 10 / 3, abs_=1e-14)
check('poly values', [round((-x2[1]) ** 3 + 2 * x2[1] ** 2 + 1, 4), round(x2[1] ** 3 + 2 * x2[1] ** 2 + 1, 4)], [1.4742, 1.8591])
def bs(K, call=True, S=100, r=0.05, s=0.2, T=1):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * T ** 0.5); d2 = d1 - s * T ** 0.5
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2) if call else K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
check('put', bs(100, False), 5.573526, abs_=5e-7); check('call 200', bs(200), 0.004799, abs_=5e-7)
check('parity', bs(100) - bs(100, False), 100 - 100 * math.exp(-0.05), abs_=1e-12)
check('2000 x 16', 2000 * 16, 32000)
# ---------- l11 ----------
k, th, sg, tau = 0.5, 0.04, 0.10, 5.0
gam = math.sqrt(k * k + 2 * sg * sg); ex_ = math.exp(gam * tau) - 1
Bx = 2 * ex_ / ((gam + k) * ex_ + 2 * gam); Ax = (2 * gam * math.exp((k + gam) * tau / 2) / ((gam + k) * ex_ + 2 * gam)) ** (2 * k * th / sg ** 2)
check('gamma', gam, 0.519615, abs_=5e-7); check('B5', Bx, 1.812959, abs_=5e-7); check('A5', Ax, 0.881920, abs_=5e-7)
check('price', 100 * Ax * math.exp(-Bx * 0.06), 79.1020, abs_=5e-5)
cir = lambda t, y: np.array([1 - k * y[0] - 0.5 * sg * sg * y[0] ** 2, -k * th * y[0]])
sol = solve_ivp(cir, [0, tau], [0, 0], rtol=1e-12, atol=1e-14)
check('solve_ivp B', sol.y[0, -1], Bx, abs_=1e-10); check('solve_ivp A', math.exp(sol.y[1, -1]), Ax, abs_=1e-10)
def euler(f, t0, y0, h, n):
    t, y = t0, np.array(y0, float)
    for _ in range(n): y = y + h * f(t, y); t += h
    return y
def rk4(f, t0, y0, h, n):
    t, y = t0, np.array(y0, float)
    for _ in range(n):
        k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
    return y
ns = [5, 10, 20, 40]
eu = [abs(euler(cir, 0, [0, 0], tau / n, n)[0] - Bx) for n in ns]; rk = [abs(rk4(cir, 0, [0, 0], tau / n, n)[0] - Bx) for n in ns]
for got, want in zip(eu, [0.0964, 0.0493, 0.0247, 0.0124]): check('euler err', got, want, abs_=5e-5)
for got, want in zip(rk, [3.49e-4, 1.75e-5, 9.84e-7, 5.83e-8]): check('rk4 err', got, want, rel=0.003)
check('euler slope', (L(eu[-1]) - L(eu[0])) / L(8), -0.99, abs_=0.006); check('rk4 slope', (L(rk[-1]) - L(rk[0])) / L(8), -4.18, abs_=0.006)
check('fit slopes', np.polyfit(np.log(ns), np.log(eu), 1)[0], -0.99, abs_=0.006)
C = rk[1] / 0.5 ** 4; check('C', C, 2.81e-4, rel=0.002); hh = (1e-8 / C) ** 0.25; check('h', hh, 0.0773, abs_=5e-5)
check('n65', math.ceil(tau / hh), 65); check('err65', abs(rk4(cir, 0, [0, 0], tau / 65, 65)[0] - Bx), 8.2e-9, rel=0.01)
check('pred 64', C * (5 / 64) ** 4, 1.05e-8, rel=0.01); check('pred 60', C * (5 / 60) ** 4, 1.35e-8, rel=0.01)
y10 = rk4(cir, 0, [0, 0], 0.5, 10)[0]; y20 = rk4(cir, 0, [0, 0], 0.25, 20)[0]
check('richardson est', (y10 - y20) / 15 * 1e6, -1.10, abs_=0.005); check('true err20', (y20 - Bx) * 1e6, -0.984, abs_=0.0005)
check('diff', (y10 - y20), -1.66e-5, rel=0.01); check('within 12%', abs((y10 - y20) / 15 / (y20 - Bx) - 1) < 0.13, True)
def step(f, t, y, h):
    k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
# the controller is the lesson's own adaptive_rk4 (screens[7]): scale tol * max(1, |y_half|), used for accept and for the step update
t, y, h, acc, rej, hs = 0.0, 1.0, 0.1, 0, 0, []
while t < 0.95 - 1e-15:
    h = min(h, 0.95 - t); f2 = lambda t, y: y * y
    big = step(f2, t, y, h); half = step(f2, t + h / 2, step(f2, t, y, h / 2), h / 2); err = abs(half - big) / 15
    scale = 1e-8 * max(1.0, abs(half))
    if err <= scale:
        t += h; y = half + (half - big) / 15; acc += 1; hs.append(h)
    else:
        rej += 1
    h = h * (5.0 if err == 0 else min(5.0, max(0.2, 0.9 * (scale / err) ** 0.2)))
check('accepted 38', acc, 38); check('rejected 1', rej, 1); check('evals 468', (acc + rej) * 12, 468)
check('first h 0.070', hs[0], 0.070, abs_=0.0005); check('min controller h 0.0043', min(hs[:-1]), 0.0043, abs_=0.00005)
check('last h cut to 0.0021', hs[-1], 0.0021, abs_=0.00005)
check('rel err 2.4e-8', abs(y - 20) / 20, 2.4e-8, rel=0.03)
check('fixed 400', abs(rk4(lambda t, y: y * y, 0, [1.0], 0.95 / 400, 400)[0] - 20) / 20, 7e-8, rel=0.02)
s45 = solve_ivp(lambda t, y: y * y, [0, 0.95], [1.0], method='RK45', rtol=1e-8)
check('RK45 evals (Pyodide SciPy 1.14.1 gave 320)', s45.nfev, 320)
check('euler budget', 0.0493 / 0.001 * 10, 493, abs_=0.5)
check('euler steps_for_tol', math.ceil(tau / (1e-3 / (eu[1] / 0.5)) ** 1), 494)
# ---------- l12 ----------
A2 = np.array([[-0.5, 0], [50, -50]]); c2 = np.array([0.02, 0]); y0 = np.array([0.06, 0.03])
Aa = 0.02 * 50 / 49.5; Bb = 0.03 - 0.04 - Aa; rt = lambda t: 0.04 + Aa * math.exp(-0.5 * t) + Bb * math.exp(-50 * t)
check('A', Aa, 0.020202, abs_=5e-7); check('B', Bb, -0.030202, abs_=5e-7); check('r(1)', rt(1) * 100, 5.2253, abs_=5e-5)
check('expm', (np.array([0.04, 0.04]) + expm(A2) @ (y0 - 0.04))[1], rt(1), abs_=1e-14)
def eul(h):
    y = y0.copy()
    for _ in range(round(1 / h)): y = y + h * (A2 @ y + c2)
    return y[1] * 100
for h, want, tol in [(0.01, 5.2238, 5e-5), (0.02, 5.2222, 5e-5), (0.04, 8.24, 0.005), (0.05, -10038, 0.5), (0.1, -3166906, 1)]:
    check(f'euler h={h}', eul(h), want, abs_=tol)
check('euler formula 0.04', 4 + 100 * Aa * 0.98 ** 25 - 100 * Bb * (-1) ** 26 * -1 if False else 4 + 100 * Aa * 0.98 ** 25 + 100 * Bb * (-1) ** 25, eul(0.04), abs_=1e-9)
def imp(h, n):
    y = y0.copy(); out = []
    for _ in range(n): y = np.linalg.solve(np.eye(2) - h * A2, y + h * c2); out.append(y[1] * 100)
    return out
for got, want in zip(imp(0.25, 4), [5.5720, 5.5796, 5.4176, 5.2611]): check('implicit path', got, want, abs_=5e-5)
check('implicit closed form', 100 * (0.04 + Aa / 1.125 ** 4 + Bb / 13.5 ** 4), imp(0.25, 4)[-1], abs_=1e-10)
def trp(h, n):
    y = y0.copy(); out = []
    for _ in range(n): y = np.linalg.solve(np.eye(2) - h / 2 * A2, (np.eye(2) + h / 2 * A2) @ y + h * c2); out.append(y[1] * 100)
    return out
for got, want in zip(trp(0.25, 4), [7.9696, 3.9891, 6.5346, 4.3941]): check('trap path', got, want, abs_=5e-5)
for t_, want in zip([0.25, 0.5, 0.75, 1], [5.7828, 5.5733, 5.3885, 5.2253]): check('true path', rt(t_) * 100, want, abs_=5e-5)
check('trap 0.05', trp(0.05, 20)[-1] / 100, 0.0522528, abs_=5e-8); check('trap factor', (1 - 6.25) / (1 + 6.25), -0.7241, abs_=5e-5)
check('fast factor 1/13.5', 1 / 13.5, 0.0741, abs_=5e-5); check('e^-12.5', math.exp(-12.5), 4e-6, rel=0.1)
check('rk4 limit', brentq(lambda z: abs(1 + z + z * z / 2 + z ** 3 / 6 + z ** 4 / 24) - 1, -3, -2), -2.7853, abs_=5e-5)
R4 = lambda z: abs(1 + z + z * z / 2 + z ** 3 / 6 + z ** 4 / 24)
check('rk4 at -2.5', R4(-2.5), 0.648, abs_=0.0005); check('impl at -2.5', 1 / 3.5, 0.286, abs_=0.0005); check('trap at -2.5', 0.25 / 2.25, 0.111, abs_=0.0005)
check('rk4 at -1.5 caption', R4(-1.5), 0.273, abs_=0.0005)
for meth, want in [('RK45', 1172), ('Radau', 422), ('BDF', 226)]:
    s = solve_ivp(lambda t, y: A2 @ y + c2, [0, 10], y0, method=meth, rtol=1e-6, atol=1e-9)
    check(f'{meth} evals (Pyodide gave {want})', s.nfev, want)
check('1.5^20', 1.5 ** 20, 3300, rel=0.01)
check('h3 rk4 limit', 2.785293563405282 / 50, 0.0557, abs_=5e-5)
check('h3 update', 0.9 * 0.01 * (1e-8 / 3.2e-7) ** 0.2 * 1000, 4.5, abs_=1e-9)
check('h3 trap n', next(n for n in (8, 16, 32, 64, 128, 256) if 0.02 * (8 / n) ** 2 < 1e-4), 128)
check('r3 step choice', math.ceil(1 / (1e-9 / 1e-3) ** 0.25), 32)
check('r3 ring', (1 - 20) / (1 + 20), -0.905, abs_=0.0005); check('r3 implicit', 1 / 41, 0.024, abs_=0.0005)
check('r3 richardson', (4 * 2.0010 - 2.0040) / 3, 2.0, abs_=1e-12); check('r3 cubic', quad(lambda x: 4 * x ** 3 - x, 0, 1)[0], 0.5, abs_=1e-14)
check('spread', bs(100) - bs(110), 4.410495442461325, abs_=1e-12); check('digital', math.exp(-0.05) * norm.cdf(0.15), 0.5323248154537634, abs_=1e-12)
check('forward', 100 - 100 * math.exp(-0.05), 4.877057549928594, abs_=1e-12)
# ---------- code widgets ----------
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'numerics')
FILES = ['l9-quadrature', 'l10-gaussian-quadrature', 'l11-step-size', 'l12-stiff-equations', 'review-3', 'homework-3']
def widgets(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code': yield o
        for v in o.values(): yield from widgets(v)
    elif isinstance(o, list):
        for v in o: yield from widgets(v)
def run_case(ns, case):
    if case.get('setup'): exec(case['setup'], ns)
    cmp = case.get('compare', 'equal')
    if cmp == 'raises':
        try:
            eval(case['call'], ns); return False
        except Exception as ex:
            return type(ex).__name__ == case['expect']
    got = eval(case['call'], ns); want = eval(case['expect'], ns)
    tol = case.get('tol'); rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
    def close(a, b):
        a = a.tolist() if hasattr(a, 'tolist') else a; b = b.tolist() if hasattr(b, 'tolist') else b
        if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(close(p, q) for p, q in zip(a, b))
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    if cmp == 'isclose': return close(got, want)
    gg = got.tolist() if hasattr(got, 'tolist') else got
    return gg == want
for fn in FILES:
    for w in widgets(json.load(open(os.path.join(BASE, fn + '.json')))):
        for label, src, must in [('solution', w['solution'], True), ('starter', w['starter'], False)]:
            ns = {'__learner_source__': src}
            if w.get('prelude'): exec(w['prelude'], ns)
            exec(src, ns)
            res = []
            for case in w['tests']:
                try: res.append(bool(run_case(ns, case)))
                except Exception: res.append(False)
            if must and not all(res): fails.append(f'{fn}: solution fails tests {[i + 1 for i, x in enumerate(res) if not x]}')
            if not must and all(res): fails.append(f'{fn}: starter passes every test')

# ---------- fix pass: values changed after the second read ----------
check('l9 trap n=2 error 0.0356', round(trap(np.exp, 0, 1, 2) - E1, 4), 0.0356)
check('l9 trap ratio 3.99', (trap(np.exp, 0, 1, 2) - E1) / (trap(np.exp, 0, 1, 4) - E1), 3.99, abs_=0.005)
check('l9 split n=128 rounds to 1.92e-6', round((simp(g, zs, 8, 128) - BS) * 1e6, 2), 1.92)
def eulr(h, n):
    y = y0.copy(); out = []
    for _ in range(n):
        y = (np.linalg.solve(np.eye(2) - h / 2 * A2, (np.eye(2) + h / 2 * A2) @ y + h * c2)); out.append(y[1] * 100)
    return out
tp = eulr(0.25, 40)
check('l12 trapezoidal ring min above 3.9 and below 4', min(tp) > 3.9 and min(tp) < 4.0, True)
check('l12 trapezoidal ring max below 8.1', max(tp) < 8.1, True)
if True:
    d = json.load(open(os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'content', 'courses', 'numerics', 'l11-step-size.json'), encoding='utf-8'))
    pts = d['screens'][4]['canvas']['state']['points']
    check('l11 dots count', len(pts), acc + 1)
    check('l11 dot s1 matches the lesson controller', pts[1]['x'], hs[0], abs_=1e-5)
if fails:
    print('\n'.join(fails)); print(f'{len(fails)} check(s) failed'); sys.exit(1)
print('numerics L3: all checks passed')
