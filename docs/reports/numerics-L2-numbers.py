"""Recompute every number stated in numerics level 2 (Equations and curves) by a second method.
Run: python3 docs/reports/numerics-L2-numbers.py   (needs numpy, scipy and mpmath; exits 0 when all checks pass)
Routes: hand loops against scipy.optimize (brentq, newton); hand barycentric sums against
scipy BarycentricInterpolator and np.polyfit; a hand tridiagonal solve against CubicSpline;
mpmath for the Black-Scholes prices. Every code widget's solution must pass its hidden tests
in CPython and its starter must fail one.
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import brentq, newton as sp_newton
from scipy.interpolate import BarycentricInterpolator, CubicSpline
from mpmath import mp, mpf, ncdf as mncdf, exp as mexp, log as mlog, sqrt as msqrt, npdf as mnpdf, findroot
mp.dps = 40
fails = []
def check(name, got, want, rel=0.0, abs_=0.0):
    ok = math.isclose(float(got), float(want), rel_tol=rel, abs_tol=abs_) if (rel or abs_) else got == want
    if not ok:
        fails.append(f'{name}: got {got!r}, stated {want!r}')
R2 = math.sqrt(2)

# ---------- l5 ----------
lo, hi, mids = 1.0, 2.0, []
for _ in range(45):
    m = (lo + hi) / 2; mids.append(abs(m - R2))
    lo, hi = (lo, m) if m * m > 2 else (m, hi)
for k, v in enumerate([0.0858, 0.164, 0.0392, 0.0233]):
    check(f'bisect mid err {k}', mids[k], v, abs_=6e-4)
check('40 halvings', next(k for k in range(1, 60) if 1 / 2**k < 1e-12), 40)
x, ne = 1.0, []
for _ in range(4):
    x -= (x * x - 2) / (2 * x); ne.append(abs(x - float(msqrt(2))))
for got, want in zip(ne, [0.0858, 0.00245, 2.12e-6, 1.59e-12]):
    check('newton err', got, want, rel=0.01)
check('newton iterates 1.5, 1.4167', round(1 - (1 - 2) / 2, 4), 1.5)
x0, x1, se = 1.0, 2.0, []
for _ in range(5):
    f0, f1 = x0 * x0 - 2, x1 * x1 - 2; x0, x1 = x1, x1 - f1 * (x1 - x0) / (f1 - f0); se.append(abs(x1 - R2))
for got, want in zip(se, [0.0809, 0.0142, 4.21e-4, 2.12e-6, 3.16e-10]):
    check('secant err', got, want, rel=0.01)
check('first chord 4/3', 2 - 2 * (2 - 1) / (2 - (-1)), 4 / 3, rel=1e-12)
order = lambda e0, e1, e2: math.log(e2 / e1) / math.log(e1 / e0)
check('newton p 1.98', order(*ne[0:3]), 1.98, abs_=0.005); check('newton p 2.00', order(*ne[1:4]), 2.00, abs_=0.005)
check('secant p 1.50', order(*se[1:4]), 1.50, abs_=0.005); check('secant p 1.67', order(*se[2:5]), 1.67, abs_=0.005)
check('log ratios', math.log(2.12e-6 / 0.00245), -7.05, abs_=0.01); check('log ratio 2', math.log(0.00245 / 0.0858), -3.56, abs_=0.01)
check('phi', (1 + 5**0.5) / 2, 1.618, abs_=0.0005); check('sqrt2 eff', 2**0.5, 1.414, abs_=0.0005)
check('C theory', 1 / (2 * R2), 0.353553, abs_=1e-6)
for got, want in zip([ne[k + 1] / ne[k]**2 for k in range(3)], [0.3333, 0.3529, 0.3535]):
    check('C measured', got, want, abs_=6e-5)
P = lambda y: sum(5 / (1 + y)**t for t in range(1, 6)) + 100 / (1 + y)**5 - 95
dP = lambda y: sum(-5 * t / (1 + y)**(t + 1) for t in range(1, 6)) - 500 / (1 + y)**6
yb = brentq(P, 0, 0.2, xtol=1e-15); ym = findroot(lambda y: sum(5 / (1 + y)**t for t in range(1, 6)) + 100 / (1 + y)**5 - 95, mpf('0.06'))
check('bond yield', yb, float(ym), abs_=1e-14); check('bond 6.193228%', yb * 100, 6.193228, abs_=5e-7)
y = 0.05; its = []
for _ in range(3):
    y -= P(y) / dP(y); its.append(y * 100)
check('bond it1', its[0], 6.15487, abs_=5e-6); check('bond it2', its[1], 6.193188, abs_=5e-7); check('bond it3', its[2], 6.1932283, abs_=5e-8)
check('scipy newton agrees', sp_newton(P, 0.05, fprime=dP), yb, abs_=1e-12)
check('31 halvings', next(k for k in range(1, 60) if 0.2 / 2**k < 1e-10), 31)
check('0.2/2^31', 0.2 / 2**31, 9.3e-11, rel=0.01); check('0.2/2^30', 0.2 / 2**30, 1.9e-10, rel=0.03)
check('31/8', 31 / 8, 3.875)
check('20 halvings', next(k for k in range(1, 60) if 1 / 2**k < 1e-6), 20)

# ---------- l6 ----------
S, r, T = 100, mpf('0.05'), mpf(1) / 12
def mprice(K, s, kind):
    s = mpf(s); d1 = (mlog(mpf(S) / K) + (r + s * s / 2) * T) / (s * msqrt(T)); d2 = d1 - s * msqrt(T)
    return S * mncdf(d1) - K * mexp(-r * T) * mncdf(d2) if kind == 'c' else K * mexp(-r * T) * mncdf(-d2) - S * mncdf(-d1)
def mvega(K, s):
    s = mpf(s); d1 = (mlog(mpf(S) / K) + (r + s * s / 2) * T) / (s * msqrt(T)); return S * msqrt(T) * mnpdf(d1)
smile = lambda K: 0.20 - 0.40 * math.log(K / 100) + 2.0 * math.log(K / 100)**2
Ks = list(range(75, 130, 5)); kinds = ['p'] * 5 + ['c'] * 6
stated_q = [0.0766, 0.0794, 0.1154, 0.2448, 0.6958, 2.5121, 0.6182, 0.0872, 0.0093, 0.0012, 0.0003]
for K, k, q in zip(Ks, kinds, stated_q):
    check(f'quote {K}', round(float(mprice(K, smile(K), k)), 4), q)
ivs = [float(findroot(lambda s: mprice(K, s, k) - q, mpf(smile(K)))) for K, k, q in zip(Ks, kinds, stated_q)]
check('iv 125', ivs[-1], 0.2124, abs_=5e-5); check('smile 125', smile(125), 0.2103, abs_=5e-5)
check('vega 125', float(mvega(125, ivs[-1])), 0.0218, abs_=5e-5); check('0.0023', 0.00005 / float(mvega(125, ivs[-1])), 0.0023, abs_=5e-5)
s1 = 0.2 - float((mprice(75, 0.2, 'p') - 0.0766) / mvega(75, 0.2)); check('75 put jump', s1, 2724, abs_=1)
s1 = 0.2 - float((mprice(80, 0.2, 'p') - 0.0794) / mvega(80, 0.2)); check('80 put jump', s1, 18.14, abs_=0.005)
s2 = s1 - float((mprice(80, s1, 'p') - 0.0794) / mvega(80, s1)); check('80 put second', s2, -218, abs_=0.5)
check('75 vega at 0.2', float(mvega(75, 0.2)), 0.000028, abs_=5e-7); check('80 vega at 0.2', float(mvega(80, 0.2)), 0.0044, abs_=5e-5)
check('85 step to 0.89', 0.2 - float((mprice(85, 0.2, 'p') - 0.1154) / mvega(85, 0.2)), 0.885, abs_=0.001)
check('75 from 0.3', 0.3 - float((mprice(75, 0.3, 'p') - 0.0766) / mvega(75, 0.3)), 2.53, abs_=0.005)
check('75 from 0.5', 0.5 - float((mprice(75, 0.5, 'p') - 0.0766) / mvega(75, 0.5)), 0.482, abs_=0.0005)
check('75 root 0.48', ivs[0], 0.48, abs_=0.005)
check('price at 0.3', float(mprice(75, 0.3, 'p')), 0.0007, abs_=5e-5); check('vega at 0.3', float(mvega(75, 0.3)), 0.034, abs_=5e-4)
fl = lambda x: float(x)
def safe(K, k, q):
    f = lambda s: fl(mprice(K, s, k)) - q; df = lambda s: fl(mvega(K, s))
    lo, hi, x, its, bis = 1e-4, 5.0, 0.2, 0, 0
    step = older = hi - lo  # fix pass: rtsafe's second test, as in the l6 solution
    flo = f(lo)
    for its in range(1, 101):
        fx = f(x)
        if abs(fx) < 1e-12: break
        if (fx > 0) == (flo > 0): lo, flo = x, fx
        else: hi = x
        d = df(x); xn = x - fx / d if d else lo - 1
        if not (lo < xn < hi) or abs(xn - x) > 0.5 * older: xn = 0.5 * (lo + hi); bis += 1
        older, step = step, abs(xn - x)
        if step < 1e-10: x = xn; break
        x = xn
    return x, its, bis
res = [safe(K, k, q) for K, k, q in zip(Ks, kinds, stated_q)]
check('75 its', res[0][1:], (9, 1)); check('80 its', res[1][1:], (9, 1))
check('others 2..8', all(2 <= rr[1] <= 8 and rr[2] == 0 for rr in res[2:]), True)
check('85 its 8', res[2][1], 8); check('100 its 2', res[5][1], 2); check('125 its 6', res[10][1], 6)
for rr, iv in zip(res, ivs):
    check('safe vs mpmath root', rr[0], iv, abs_=1e-9)
check('brentq agrees 1e-10', max(abs(brentq(lambda s: fl(mprice(K, s, k)) - q, 1e-4, 5, xtol=1e-14) - iv) for K, k, q, iv in zip(Ks, kinds, stated_q, ivs)) < 1e-10, True)
check('36 bisections', next(k for k in range(1, 80) if 5 / 2**k < 1e-10), 36)
check('5/2^36', 5 / 2**36, 7.3e-11, rel=0.01); check('5/2^35', 5 / 2**35, 1.5e-10, rel=0.04)
check('call bound 95', float(S - 95 * mexp(-r * T)), 5.3950, abs_=5e-5)
check('put bound 110', float(110 * mexp(-r * T) - S), 9.5426, abs_=5e-5)
check('cubic root', brentq(lambda x: x**3 - 2 * x + 2, -3, 0, xtol=1e-15), -1.769292, abs_=5e-7)
xx = 0.0
for _ in range(4):
    xx -= (xx**3 - 2 * xx + 2) / (3 * xx * xx - 2)
check('newton cycles 0 -> 1 -> 0', xx, 0.0)
check('0.0001/0.5', 0.0001 / 0.5, 0.0002, rel=1e-12); check('5/1024', 5 / 1024, 0.00488, abs_=5e-6)
check('one-month vol move ratio', (0.00005 / 0.0218), 0.0023, abs_=5e-5)

# ---------- l7 ----------
f = lambda x: 1 / (1 + 25 * x**2)
g = np.linspace(-1, 1, 20001)
def bary(xs, ys, x):
    w = np.array([1 / np.prod(xj - np.delete(xs, j)) for j, xj in enumerate(xs)])
    d = x[:, None] - xs[None, :]; ex = d == 0; d[ex] = 1; t = w / d; p = (t @ ys) / t.sum(1)
    rw, cl = np.nonzero(ex); p[rw] = ys[cl]; return p
for n, eqv, chv in [(4, 0.4384, 0.4600), (8, 1.0452, 0.2047), (10, 1.9157, 0.1322), (20, 59.82, 0.0177)]:
    e = np.linspace(-1, 1, n + 1); c = np.cos(np.arange(n + 1) * np.pi / n)
    a1 = np.max(abs(bary(e, f(e), g) - f(g))); a2 = np.max(abs(BarycentricInterpolator(e, f(e))(g) - f(g)))
    b1 = np.max(abs(bary(c, f(c), g) - f(g))); b2 = np.max(abs(BarycentricInterpolator(c, f(c))(g) - f(g)))
    check(f'equal {n}', a1, eqv, abs_=6e-5 if n < 20 else 0.006); check(f'equal {n} scipy', a1, a2, rel=1e-6)
    check(f'cheb {n}', b1, chv, abs_=6e-5); check(f'cheb {n} scipy', b1, b2, rel=1e-6)
e11 = np.linspace(-1, 1, 11)
check('p10(0.95)', float(np.polyval(np.polyfit(e11, f(e11), 10), 0.95)), 1.9236, abs_=5e-5)
check('f(0.95)', f(0.95), 0.0424, abs_=5e-5); check('1.8812', 1.9236 - 0.0424, 1.8812, abs_=1e-9)
def leb(nodes):
    L = np.zeros_like(g)
    for j in range(len(nodes)):
        yy = np.zeros(len(nodes)); yy[j] = 1; L += np.abs(bary(nodes, yy, g))
    return L.max()
check('lebesgue equal', leb(e11), 29.9, abs_=0.05); check('lebesgue cheb', leb(np.cos(np.arange(11) * np.pi / 10)), 2.42, abs_=0.005)
prod = lambda x, nd: abs(np.prod(x - nd))
check('node prod 0.95', prod(0.95, e11), 0.00845, abs_=5e-6); check('node prod 0.05', prod(0.05, e11), 0.0000671, abs_=5e-8)
check('ratio 126', prod(0.95, e11) / prod(0.05, e11), 126, abs_=0.5)
check('cheb prod max', max(prod(x, np.cos(np.arange(11) * np.pi / 10)) for x in g) <= 2**-9 + 1e-12, True)
check('2^-9', 2**-9, 0.00195, abs_=5e-6)
check('x^3 exact', np.max(abs(bary(np.array([0, 0.3, 1.1, 2.0]), np.array([0, 0.3, 1.1, 2.0])**3, np.linspace(-1, 3, 101)) - np.linspace(-1, 3, 101)**3)) < 1e-12, True)
Kq = np.arange(75, 130, 5.0); kg = np.linspace(75, 125, 50001); wv = bary(Kq, 0.001 * (-1.0)**np.arange(11), kg)
check('vol wiggle', np.max(abs(wv)), 0.0292, abs_=5e-5); check('wiggle near 123.4', kg[np.argmax(abs(wv[kg > 100])) + np.sum(kg <= 100)], 123.4, abs_=0.05)
check('29.9*0.001', 29.9 * 0.001, 0.0299, abs_=1e-9); check('2.42*0.002', 2.42 * 0.002, 0.00484, abs_=1e-9)
check('p(1.5) quadratic', float(bary(np.array([0., 1, 2]), np.array([1., 3, 2]), np.array([1.5]))[0]), 2.875, abs_=1e-12)

# ---------- l8 ----------
t = np.array([1, 2, 3, 5, 7, 10, 20, 30.]); z = np.array([4.10, 3.95, 3.90, 3.95, 4.05, 4.25, 4.70, 4.80])
cs = CubicSpline(t, z, bc_type='natural')
h = np.diff(t); A = np.zeros((6, 6)); b = np.zeros(6)
for i in range(1, 7):
    j = i - 1
    if j > 0: A[j, j - 1] = h[i - 1]
    A[j, j] = 2 * (h[i - 1] + h[i])
    if j < 5: A[j, j + 1] = h[i]
    b[j] = 6 * ((z[i + 1] - z[i]) / h[i] - (z[i] - z[i - 1]) / h[i - 1])
M = np.linalg.solve(A, b)
check('M matches CubicSpline', np.allclose(M, cs(t, 2)[1:-1], atol=1e-12), True)
for got, want in zip(M, [0.1372, 0.0510, 0.0033, 0.0107, -0.0047, -0.0041]):
    check('M', got, want, abs_=5e-5)
check('rhs 5y', b[2], 0.15, abs_=1e-12); check('diag 5y', A[2, 2], 8); check('rhs list', np.allclose(b, [0.6, 0.45, 0.15, 0.1, -0.13, -0.21]), True)
check('row check', 4 * 0.1372 + 0.0510, 0.6, abs_=0.002)
check('linear 4', np.interp(4, t, z), 3.925, abs_=1e-12); check('linear 15', np.interp(15, t, z), 4.475, abs_=1e-12)
poly = np.polyfit(t, z, 7); B8 = BarycentricInterpolator(t, z)
for x, want in [(4, 3.9103), (15, 5.1921), (25, -2.58)]:
    check(f'poly {x}', np.polyval(poly, x), want, abs_=0.006 if x == 25 else 5e-5); check(f'poly {x} bary', float(B8(x)), np.polyval(poly, x), abs_=1e-8)
check('spline 4', cs(4), 3.9114, abs_=5e-5); check('spline 15', cs(15), 4.5297, abs_=5e-5)
def hand(x, MM):
    MM = np.r_[0, MM, 0]; k = min(max(np.searchsorted(t, x) - 1, 0), 6); a, bb = t[k], t[k + 1]; hh = bb - a
    return MM[k] * (bb - x)**3 / (6 * hh) + MM[k + 1] * (x - a)**3 / (6 * hh) + (z[k] / hh - MM[k] * hh / 6) * (bb - x) + (z[k + 1] / hh - MM[k + 1] * hh / 6) * (x - a)
check('hand spline 4', hand(4, M), cs(4), abs_=1e-12); check('hand spline 15', hand(15, M), cs(15), abs_=1e-12)
fw = lambda x: cs(x) + x * cs(x, 1)
check('fwd 4', fw(4), 4.0273, abs_=5e-5); check('fwd 15', fw(15), 5.2010, abs_=5e-5)
check('lin fwd below 5', 3.95 + 5 * (3.95 - 3.90) / 2, 4.075, abs_=1e-12); check('lin fwd above 5', 3.95 + 5 * (4.05 - 3.95) / 2, 4.20, abs_=1e-12)
check('zcb spline', 100 * math.exp(-4 * cs(4) / 100), 85.5169, abs_=5e-5); check('zcb linear', 100 * math.exp(-4 * 0.03925), 85.4704, abs_=5e-5)
check('zcb annual distractor', 100 / 1.03925**4, 85.7274, abs_=5e-4); check('4.65p', 85.5169 - 85.4704, 0.0465, abs_=1e-9)
z2 = z.copy(); z2[3] += 0.10; cs2 = CubicSpline(t, z2, bc_type='natural')
for x, want in [(4, 5.51), (6, 6.42), (8.5, -2.67), (15, 3.25)]:
    check(f'bump {x}', (cs2(x) - cs(x)) * 100, want, abs_=0.006)
check('bumped 15', cs2(15), 4.5622, abs_=5e-5); check('bumped 4', cs2(4), 3.9665, abs_=5e-5)
check('three-point M2', 6 * ((0 - 1) / 1 - (1 - 0) / 1) / 4, -3)
check('three-point CubicSpline', CubicSpline([0, 1, 2], [0, 1, 0], bc_type='natural')(1, 2), -3, abs_=1e-12)
check('line spline', np.allclose(CubicSpline([0, 1, 3, 4], [1, 3, 7, 9], bc_type='natural')(2.5), 6.0), True)

# ---------- review-2 and homework-2 ----------
check('30 halvings', next(k for k in range(1, 60) if 1 / 2**k < 1e-9), 30)
check('wing vol', 0.0001 / 0.0218 * 100, 0.46, abs_=0.005)
check('fwd 5%', 4 + 10 * 0.1, 5.0, abs_=1e-12)
check('29 halvings', next(k for k in range(1, 60) if 5 / 2**k < 1e-8), 29); check('log2', math.log2(5 / 1e-8), 28.9, abs_=0.01)
check('eff 1.587', 2**(1 / 1.5), 1.587, abs_=5e-4)
check('M2 = -2', 6 * ((2 - 2) / 2 - (2 - 0) / 1) / (2 * (1 + 2)), -2); check('M2 scipy', CubicSpline([0, 1, 3], [0, 2, 2], bc_type='natural')(1, 2), -2, abs_=1e-12)
check('2.5 vol points', 0.0005 / 0.02 * 100, 2.5, abs_=1e-12)
check('order 1.5', math.log(3.16e-5 / 1e-3) / math.log(1e-3 / 1e-2), 1.5, abs_=0.002)
check('zcb yield', (100 / 60)**0.1 - 1, 0.0524097791, abs_=1e-10)

# ---------- every code widget: solution passes, starter fails ----------
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'numerics')
FILES = ['l5-bisection-and-newton', 'l6-safe-root-finder', 'l7-interpolation', 'l8-splines', 'review-2', 'homework-2']
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

# ---------- fix pass: values changed after the second read (mpmath reference) ----------
mp.dps = 40
s0, s1, mse = mpf(1), mpf(2), []
for _ in range(6):
    g0, g1 = s0 * s0 - 2, s1 * s1 - 2; s0, s1 = s1, s1 - g1 * (s1 - s0) / (g1 - g0); mse.append(abs(s1 - msqrt(2)))
check('l5 secant step 5 error 3.16e-10', float(mse[4]), 3.16e-10, rel=0.005)
check('l5 secant step 6 error 2.37e-16 (so 12 digits at step 6, not 5)', float(mse[5]), 2.37e-16, rel=0.005)
check('l5 secant first reaches 1e-12 at step 6', next(k + 1 for k, e in enumerate(mse) if e < mpf('1e-12')), 6)
mpP = lambda y: sum(5 / (1 + y)**t for t in range(1, 6)) + 100 / (1 + y)**5 - 95
mdP = lambda y: sum(-5 * t / (1 + y)**(t + 1) for t in range(1, 6)) - 500 / (1 + y)**6
yt = findroot(mpP, mpf('0.06')); ym_ = mpf('0.05')
for _ in range(3): ym_ -= mpP(ym_) / mdP(ym_)
rel3 = float(abs(ym_ - yt) / yt)
check('l5 bond Newton step 3 relative error 7.1e-12 (about 11 digits)', rel3, 7.1e-12, rel=0.05)
check('l5 about 11 correct digits', round(-math.log10(rel3)), 11)
check('l5 bisection on [0, 0.2]: 31 halvings plus 2 end checks is 33 evaluations', 31 + 2, 33)
check('l6 from width 1, 34 halvings reach 1e-10 (2^33 is too few)', (next(k for k in range(1, 60) if 1 / 2**k < 1e-10), 2**33 < 1e10 < 2**34), (34, True))
check('l6 from width 5, 36 halvings; 35 too few', (next(k for k in range(1, 60) if 5 / 2**k < 1e-10), 5 / 2**35 > 1e-10), (36, True))
check('l6 w34 stays distinct from 36 and 35', len({34, 35, 36}), 3)
check('r2 safeguard: bracket [0.3, 0.9] has midpoint 0.6', (0.3 + 0.9) / 2, 0.6, abs_=1e-12)
check('r2 Newton step 2.53 lies outside [0.3, 0.9]', not (0.3 <= 2.53 <= 0.9), True)
check('r2 Newton wins only when f-prime costs under 0.44 of f', 1 / math.log2((1 + 5 ** 0.5) / 2) - 1, 0.4405, abs_=5e-4)
check('r2 at cost 0.44 Newton rate is above 1.618, at 0.45 below', (2 ** (1 / 1.44) > 1.618, 2 ** (1 / 1.45) < 1.618), (True, True))

if fails:
    print('\n'.join(fails)); print(f'{len(fails)} check(s) failed'); sys.exit(1)
print('numerics L2: all checks passed')
