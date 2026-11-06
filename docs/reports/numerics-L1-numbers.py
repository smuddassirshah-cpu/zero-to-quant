"""Recompute every number stated in numerics level 1 (Errors) by a second method.
Run: python3 docs/reports/numerics-L1-numbers.py   (needs numpy, scipy and mpmath; exits 0 when all checks pass)
Each check compares the float computation the lessons describe with an independent route
(mpmath at 50 digits, exact fractions, struct decoding against math.frexp, SVD against eigenvalues).
It also runs every code widget of the level in CPython: the solution must pass its hidden tests
and the starter must fail at least one.
"""
import json, math, struct, sys, os, random, statistics, cmath
from fractions import Fraction
from decimal import Decimal
import numpy as np
from mpmath import mp, mpf, sqrt as msqrt, exp as mexp, log as mlog, ncdf, npdf, factorial as mfact
from scipy.linalg import hilbert
mp.dps = 50
EPS = np.finfo(float).eps
fails = []
def check(name, got, want, rel=0.0, abs_=0.0):
    ok = math.isclose(float(got), float(want), rel_tol=rel, abs_tol=abs_) if (rel or abs_) else got == want
    if not ok:
        fails.append(f'{name}: got {got!r}, stated {want!r}')

# ---------- l1 floating point ----------
eps, n = 1.0, 0
while 1.0 + eps / 2 > 1.0:
    eps /= 2; n += 1
check('halvings', n, 52)
check('eps', eps, float(Fraction(1, 2**52)))
check('eps value', float(mpf(2)**-52), 2.220446e-16, rel=1e-6)
def decode(x):
    b = struct.unpack('>Q', struct.pack('>d', x))[0]
    return b >> 63, ((b >> 52) & 0x7FF), (b & (2**52 - 1)) / 2**52, b & (2**52 - 1)
for x, s, e, m, hexm in [(-6.5, 1, 1025, 0.625, 0xa000000000000), (100.25, 0, 1029, 0.56640625, 0x9100000000000)]:
    ds, de, dm, dh = decode(x)
    fm, fe = math.frexp(abs(x))  # x = fm * 2**fe, fm in [0.5, 1)
    check(f'decode {x} sign', ds, s); check(f'decode {x} exp', de, e); check(f'decode {x} frac', dm, m); check(f'decode {x} hex', dh, hexm)
    check(f'frexp {x} power', fe - 1, e - 1023); check(f'frexp {x} frac', 2 * fm - 1, m)
check('1.625*4', (1 + 0.625) * 4, 6.5); check('1.56640625*64', 1.56640625 * 64, 100.25)
check('0.5+1/16+1/256', 0.5 + 1 / 16 + 1 / 256, 0.56640625)
check('exp bits -6.5', format(decode(-6.5)[1], '011b'), '10000000001')
check('exp bits 100.25', format(decode(100.25)[1], '011b'), '10000000101')
d01 = Fraction(0.1) - Fraction(1, 10)
check('0.1 stored', str(Decimal(0.1))[:36], '0.1000000000000000055511151231257827')
check('0.1 error', float(d01), 5.55e-18, rel=1e-3)
check('0.1 relative error', float(d01 / Fraction(1, 10)), 5.55e-17, rel=1e-3)
check('spacing 100', np.spacing(100.0), 1.42e-14, rel=1e-3); check('spacing 100 by formula', 2.0**(6 - 52), 1.4210854715202004e-14)
check('spacing 1e6', np.spacing(1e6), 1.16e-10, rel=5e-3); check('spacing 1e6 by formula', 2.0**(19 - 52), np.spacing(1e6))
check('2^53', 2**53, 9007199254740992); check('2^53 + 1 lost', float(2**53) + 1 == float(2**53), True)
check('max', sys.float_info.max, 1.797693e308, rel=1e-6)
check('exp 709', math.exp(709), float(mexp(709)), rel=1e-15); check('exp 709 stated', math.exp(709), 8.218407e307, rel=1e-6)
try:
    math.exp(710); fails.append('exp 710 did not raise')
except OverflowError:
    pass
with np.errstate(over='ignore'):
    check('np exp 710', np.exp(710.0), float('inf'))
check('e^710 size', float(mexp(710)), 2.2e308, rel=0.01)
check('tiny', sys.float_info.min, 2.225074e-308, rel=1e-6)
check('subnormal', np.nextafter(0, 1), 2.0**-1074); check('subnormal 5e-324', 2.0**-1074, 5e-324, rel=0.02)
check('u', 2.0**-53, 1.11e-16, rel=1e-2)
check('eps/tiny ~ 1e292', round(math.log10(EPS / sys.float_info.min)), 292)
check('float32 eps', np.finfo(np.float32).eps, 2.0**-23); check('float32 eps value', 2.0**-23, 1.19e-7, rel=0.01)
check('float32 gap 20000', float(np.spacing(np.float32(20000))), 0.001953125); check('20000 in [2^14,2^15)', 2**14 <= 20000 < 2**15, True)
check('float32 20000.01', float(np.float32(20000.01)), 20000.009765625)
check('float32 eps*20000', 2.0**-23 * 20000, 0.00238, rel=0.01)
check('float32 f64 distractor', 2.0**-52 * 2**14, 3.6e-12, rel=0.02)
ts = 1.7e18
check('ts between 2^60, 2^61', 2**60 < ts < 2**61, True)
check('2^60', 2.0**60, 1.15e18, rel=0.01); check('2^61', 2.0**61, 2.31e18, rel=0.01)
check('ts spacing', np.spacing(ts), 256.0); check('ts spacing formula', 2**(60 - 52), 256)
check('log10 2^53', math.log10(2**53), 15.9546, abs_=1e-4); check('log10 1.7e18', math.log10(1.7e18), 18.2304, abs_=1e-4)
toy = sorted(set((1 + m / 8) * 2**e for e in range(-1, 3) for m in range(8)))
check('toy count', len(toy), 32); check('toy min', toy[0], 0.5); check('toy max', toy[-1], 7.5); check('toy after 4', toy[toy.index(4.0) + 1], 4.5)

# ---------- l2 cancellation ----------
b, c = 1e8, 1.0
tb = (b - math.sqrt(b * b - 4 * c)) / 2
true_small = (mpf(b) - msqrt(mpf(b)**2 - 4)) / 2
check('textbook root', tb, 7.450581e-9, rel=1e-6)
check('true root', float(true_small), 1.0e-8, rel=1e-9)
check('25.5%', (float(true_small) - tb) / float(true_small), 0.255, abs_=0.0005)
check('stable root', 2 * c / (b + math.sqrt(b * b - 4 * c)), float(true_small), rel=1e-15)
check('sqrt(b^2-4)', float(msqrt(mpf(10)**16 - 4)), 99999999.99999998, rel=1e-16)
for k, stated in [(1, -14.4), (5, -6.5), (8, -0.6)]:
    bb = 10.0**k; dd = math.sqrt(bb * bb - 4); t1 = (bb - dd) / 2
    ex_ = (mpf(bb) - msqrt(mpf(bb)**2 - 4)) / 2
    check(f'root err b=1e{k}', math.log10(abs(t1 - float(ex_)) / float(ex_)), stated, abs_=0.06)
slope = (math.log10(0.2549) - math.log10(4.26e-15)) / 7
check('two digits per decade', round(slope), 2)
em = math.exp(1e-10) - 1
check('expm1 rel err', abs(em - float(mexp(mpf('1e-10')) - 1)) / float(mexp(mpf('1e-10')) - 1), 8.27e-8, rel=2e-3)
check('expm1 value', math.expm1(1e-10), float(mexp(mpf('1e-10')) - 1), rel=1e-15)
def onepass(xs):
    n = len(xs); s = sum(xs); s2 = sum(x * x for x in xs); return (s2 - s * s / n) / (n - 1)
def exact_var(xs):
    xs = [Fraction(x) for x in xs]; m = sum(xs) / len(xs); return float(sum((x - m)**2 for x in xs) / (len(xs) - 1))
p9 = [1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]; p8 = [1e8 + 4, 1e8 + 7, 1e8 + 13, 1e8 + 16]
check('onepass 1e9', onepass(p9), 0.0); check('exact var', exact_var(p9), 30.0); check('two-pass', statistics.variance(p9), 30.0)
check('onepass 1e8', onepass(p8), 29.33, abs_=0.005); check('population 22.5', 90 / 4, 22.5)
check('gap at 1e18', np.spacing(1e18), 128.0)
for h, stated in [(1e-1, 0.1406), (1e-8, 6.6e-9), (1e-10, 1.55e-6), (1e-15, 0.39)]:
    e_ = abs((math.exp(1 + h) - math.exp(1)) / h - math.e)
    check(f'fwd err h={h}', e_, stated, rel=0.03)
for h, stated in [(1e-4, 4.5e-9), (1e-5, 5.9e-11)]:
    check(f'central err h={h}', abs((math.exp(1 + h) - math.exp(1 - h)) / (2 * h) - math.e), stated, rel=0.03)
errs = {k: abs((math.exp(1 + 10.0**-k) - math.exp(1)) / 10.0**-k - math.e) for k in range(1, 16)}
check('lowest bump', min(errs, key=errs.get), 8)
check('h* 2 sqrt eps', 2 * math.sqrt(EPS), 2.98e-8, rel=2e-3)
check('eps^(1/3)', EPS**(1 / 3), 6e-6, rel=0.02)
# Black-Scholes standard call, twice: erf in floats and mpmath ncdf
def bs(S, K=100.0, r=0.05, s=0.2, T=1.0):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return S * N(d1) - K * math.exp(-r * T) * N(d2)
def bsm(S, K=100, r=mpf('0.05'), s=mpf('0.2'), T=1):
    S = mpf(S); d1 = (mlog(S / K) + (r + s * s / 2) * T) / (s * msqrt(T)); d2 = d1 - s * msqrt(T)
    return S * ncdf(d1) - K * mexp(-r * T) * ncdf(d2), d1
V, d1 = bsm(100)
check('call price', bs(100.0), float(V), rel=1e-14); check('call 10.4506', float(V), 10.450584, abs_=1e-6)
delta = float(ncdf(d1)); gamma = float(npdf(d1) / (100 * mpf('0.2'))); vega = float(100 * npdf(d1))
check('delta', delta, 0.636831, abs_=1e-6); check('gamma', gamma, 0.0187620, abs_=1e-7); check('vega', vega, 37.52, abs_=0.005)
for h, stated in [(1.0, 9.3e-3), (0.01, 9.4e-5), (1e-12, 4.4e-3)]:
    check(f'fwd delta h={h}', abs((bs(100 + h) - bs(100.0)) / h - delta), stated, rel=0.02)
check('fwd delta at 1 = 0.6461', (bs(101.0) - bs(100.0)), 0.6461, abs_=5e-5)
check('fwd delta at 1e-12 = 0.6324', (bs(100 + 1e-12) - bs(100.0)) / 1e-12, 0.6324, abs_=5e-4)
for h, stated in [(1.0, 8.6e-5), (0.01, 8.6e-9)]:
    check(f'central delta h={h}', abs((bs(100 + h) - bs(100 - h)) / (2 * h) - delta), stated, rel=0.02)
check('best forward delta bump', 2 * math.sqrt(EPS * float(V) / gamma), 7e-7, rel=0.03)
for h, est in [(1.0, 0.01875972), (0.01, 0.01876202), (1e-4, 0.01876188), (1e-6, 0.02842171)]:
    g = (bs(100 + h) - 2 * bs(100.0) + bs(100 - h)) / h**2
    check(f'gamma est h={h}', g, est, abs_=5e-9)
check('gamma err 0.01', abs((bs(100.01) - 2 * bs(100.0) + bs(99.99)) / 1e-4 - gamma), 2.7e-10, rel=0.03)
check('gamma err 1', abs((bs(101.0) - 2 * bs(100.0) + bs(99.0)) - gamma), 2.3e-6, rel=0.02)
check('gamma err 1e-4', abs((bs(100.0001) - 2 * bs(100.0) + bs(99.9999)) / 1e-8 - gamma), 1.4e-7, rel=0.03)
check('gamma 51% too big', (0.02842171 - gamma) / gamma, 0.51, abs_=0.005)
check('log(1+1e-12)', math.log(1 + 1e-12), 1.000089e-12, rel=1e-6); check('log1p', math.log1p(1e-12), float(mlog(1 + mpf('1e-12'))), rel=1e-15)
check('sterbenz', 1.5 - 1.25, 0.25)

# ---------- l3 conditioning ----------
A = np.array([[1, 1], [1, 1.0001]])
sv = np.linalg.svd(A, compute_uv=False); ev = np.sqrt(np.linalg.eigvalsh(A.T @ A))[::-1]
check('sigma max', sv[0], 2.00005, rel=1e-6); check('sigma min', sv[1], 4.999875e-5, rel=1e-6)
check('sigma by eig', ev[0], sv[0], rel=1e-9)
check('kappa', sv[0] / sv[1], 40002, rel=1e-6); check('kappa = cond', np.linalg.cond(A), 40002.00007, rel=1e-9)
x1 = np.linalg.solve(A, [2, 2.0001]); x2 = np.linalg.solve(A, [2, 2.0002])
check('meet 2.0001', np.allclose(x1, [1, 1]), True); check('meet 2.0002', np.allclose(x2, [0, 2], atol=1e-9), True)
relb = 1e-4 / math.hypot(2, 2.0001); check('rel db x1e5', relb * 1e5, 3.536, abs_=0.001)
check('amplification', 1 / relb, 28285, rel=1e-4)
check('residual (0,2)', (np.array([2, 2.0001]) - A @ np.array([0, 2.0]))[1], -1e-4, rel=1e-9)
check('digits lost', math.log10(40002), 4.6, abs_=0.005)
H8 = hilbert(8); check('hilbert kappa', np.linalg.cond(H8), 1.53e10, rel=0.005); check('hilbert digits', math.log10(np.linalg.cond(H8)), 10.2, abs_=0.02)
check('kappa x-1', 1.0001 / 0.0001, 10001, rel=1e-9); check('kappa ln', float(1 / mlog(mpf('1.0001'))), 10000.5, abs_=0.01)
check('ln 1.0001', float(mlog(mpf('1.0001'))), 0.00009999500, rel=1e-6)
check('kappa e^x at 20', 20.0, 20); check('kappa sqrt', 0.5, 0.5)
check('vol move call', 0.01 / vega * 100, 0.027, abs_=0.0005)
Vp, d1p = (lambda S, K: (K * mexp(-mpf('0.05')) * ncdf(-((mlog(mpf(S) / K) + mpf('0.07')) / mpf('0.2') - mpf('0.2'))) - S * ncdf(-((mlog(mpf(S) / K) + mpf('0.07')) / mpf('0.2'))), (mlog(mpf(S) / K) + mpf('0.07')) / mpf('0.2')))(100, 60)
vegap = float(100 * npdf(d1p))
check('60 put price', float(Vp), 0.0113, abs_=0.00005); check('60 put vega', vegap, 0.588, abs_=0.0005)
check('60 put vol move', 0.01 / vegap * 100, 1.70, abs_=0.005); check('64 times', (0.01 / vegap) / (0.01 / vega), 64, abs_=0.5)
check('put 0.05 move', 0.05 / vegap * 100, 8.5, abs_=0.05); check('call 0.05 move', 0.05 / vega * 100, 0.133, abs_=0.0005)
check('corr kappa', (1 + 0.95) / (1 - 0.95), 39, rel=1e-9); check('vif', 1 / (1 - 0.95**2), 10.26, abs_=0.005)
check('log10 39', math.log10(39), 1.6, abs_=0.01); check('r 0.99', (1.99) / 0.01, 199, rel=1e-9)
check('predicted error', np.linalg.cond(A) * 1e-8, 4.0002e-4, rel=1e-6)

# ---------- l4 stability ----------
s, t = 0.0, 1.0
for k in range(1, 120):
    s += t; t *= -20 / k
check('series e-20', s, 6.147561828914626e-09); check('true e-20', math.exp(-20), float(mexp(-20)), rel=1e-15)
check('198.3%', (s - math.exp(-20)) / math.exp(-20), 1.983, abs_=0.0005)
check('largest term', float(mpf(20)**20 / mfact(20)), 4.31e7, rel=0.002)
check('largest term at k=19,20', abs(20**19 / math.factorial(19) - 20**20 / math.factorial(20)) < 1e-6, True)
check('decades apart', math.log10(float(mpf(20)**20 / mfact(20)) / math.exp(-20)), 16.3, abs_=0.03)
check('largest term power', math.log10(4.31e7), 7.63, abs_=0.01); check('answer power', math.log10(math.exp(-20)), -8.69, abs_=0.01)
s2, t = 0.0, 1.0
for k in range(1, 120):
    s2 += t; t *= 20 / k
check('reciprocal', 1 / s2, 2.061153622438557e-09)
e = 1e-8
L = np.array([[1, 1], [e, 0], [0, e]]); bL = np.array([2, e, e])
check('AtA stored', (L.T @ L).tolist(), [[1.0, 1.0], [1.0, 1.0]]); check('det stored', np.linalg.det(L.T @ L), 0.0)
check('det exact', float((1 + mpf(e)**2)**2 - 1), 2e-16, rel=1e-6)
check('lstsq lauchli', np.allclose(np.linalg.lstsq(L, bL, rcond=None)[0], [1, 1]), True)
Q, R = np.linalg.qr(L); check('qr lauchli', np.allclose(np.linalg.solve(R, Q.T @ bL), [1, 1]), True)
check('kappa lauchli', np.linalg.cond(L), 1.41e8, rel=0.005); check('kappa lauchli sq digits', 2 * math.log10(np.linalg.cond(L)), 16.3, abs_=0.01)
check('kappa lauchli digits', math.log10(np.linalg.cond(L)), 8.15, abs_=0.01)
check('kappa(AtA)=kappa^2 by svd', np.linalg.svd(np.array([[3., 1], [1, 2], [0, 1]]).T @ np.array([[3., 1], [1, 2], [0, 1]]), compute_uv=False)[0] / np.linalg.svd(np.array([[3., 1], [1, 2], [0, 1]]).T @ np.array([[3., 1], [1, 2], [0, 1]]), compute_uv=False)[-1], np.linalg.cond(np.array([[3., 1], [1, 2], [0, 1]]))**2, rel=1e-9)
e7 = 1e-7; L7 = np.array([[1, 1], [e7, 0], [0, e7]])
check('normal 1e-7', np.allclose(np.linalg.solve(L7.T @ L7, L7.T @ np.array([2, e7, e7])), [1, 1], atol=1e-6), True)
check('kappa^2 u at 1e-7', np.linalg.cond(L7)**2 * 2**-53, 0.02, abs_=0.003)
check('45 gaps', 1e-14 / EPS, 45, abs_=0.1)
tt = np.linspace(0, 1, 100); V15 = np.vander(tt, 15, increasing=True); b15 = np.exp(np.sin(4 * tt)) / 2006.787453080206
check('trefethen kappa', np.linalg.cond(V15), 2.27e10, rel=0.005)
xq = np.linalg.lstsq(V15, b15, rcond=None)[0][-1]
check('trefethen lstsq ~7 digits', abs(xq - 1) < 1e-7, True)
xn = np.linalg.solve(V15.T @ V15, V15.T @ b15)[-1]
check('trefethen normal no digit', abs(xn - 1) > 0.5, True)   # Pyodide 2.0.2: -0.2654; this CPython prints its own value
check('trefethen kappa u', np.linalg.cond(V15) * 2**-53, 2.5e-6, rel=0.01)
check('trefethen kappa^2', np.linalg.cond(V15)**2, 5e20, rel=0.05)
check('trefethen digits bound', 16 - math.log10(2.27e10), 5.6, abs_=0.05)
mat = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30.]); Y = np.vander(mat, 4, increasing=True)
check('yc kappa', np.linalg.cond(Y), 2.98e4, rel=0.002); check('yc kappa AtA', np.linalg.cond(Y.T @ Y), 8.88e8, rel=0.002)
check('yc kappa AtA = kappa^2', np.linalg.cond(Y)**2, np.linalg.cond(Y.T @ Y), rel=1e-4)
z = (mat - mat.mean()) / mat.std(); check('yc scaled', np.linalg.cond(np.vander(z, 4, increasing=True)), 13.3, abs_=0.01)
check('yc digits', math.log10(8.88e8), 8.95, abs_=0.005); check('yc qr digits', math.log10(2.98e4), 4.47, abs_=0.005)
check('kappa 1000 normal', math.log10(1000**2), 6, rel=1e-12)

# ---------- review-1 and homework-1 ----------
check('0.01 stored exp', decode(0.01)[1], 1016); check('0.01 power', math.frexp(0.01)[1] - 1, -7); check('0.01 = 1.28 * 2^-7', 0.01 * 2**7, 1.28, rel=1e-12)
check('sqrt gap', float(msqrt(mpf(10)**12 + 1) - msqrt(mpf(10)**12)), 5e-7, rel=1e-6)
check('sv kappa', 50 / 0.005, 1e4, rel=1e-12)
check('float32 gap 1e6', float(np.spacing(np.float32(1e6))), 0.0625); check('f64 gap 1e6', np.spacing(1e6), 1.16e-10, rel=0.005)
check('bump |f|=100', 2 * math.sqrt(EPS * 100) * 1e7, 2.98, abs_=0.005); check('root of eps*100', math.sqrt(EPS * 100), 1.49e-7, rel=0.003)
check('e^-30', math.exp(-30), 9.4e-14, rel=0.005); check('30^30/30!', float(mpf(30)**30 / mfact(30)), 7.8e11, rel=0.01)
check('25 decades', math.log10(float(mpf(30)**30 / mfact(30)) / math.exp(-30)), 25, abs_=0.15)
check('rounding of largest term', EPS * 7.76e11, 1.7e-4, rel=0.02)
check('spread kappa', 100.01 / 0.01, 10001, rel=1e-9)
check('hex 0x4024', struct.unpack('>d', bytes.fromhex('4024000000000000'))[0], 10.0)
check('float32 2^24 exact', float(np.float32(2**24)) == 2**24 and float(np.float32(2**24 + 1)) == 2**24, True)
check('float32 2^24-1 exact', float(np.float32(2**24 - 1)), 2**24 - 1)
check('normal digits 3e5', 16 - math.log10((3e5)**2), 5.0, abs_=0.05); check('qr digits 3e5', 16 - math.log10(3e5), 10.5, abs_=0.03)
check('gamma bump', (48 * EPS)**0.25 * 1e4, 3.21, abs_=0.005); check('sqrt distractor', math.sqrt(48 * EPS) * 1e7, 1.03, abs_=0.005)
check('48 eps', 48 * EPS, 1.07e-14, rel=0.005)
f32 = np.float32; s32 = f32(0)
for _ in range(10**6):
    s32 = s32 + f32(0.01)
check('naive float32 pennies', round(float(s32), 2), 9865.22)
sk, ck = f32(0), f32(0)
for _ in range(10**6):
    y = f32(0.01) - ck; tk = sk + y; ck = (tk - sk) - y; sk = tk
check('kahan float32 pennies', round(float(sk), 2), 10000.0)
random.seed(7); outs = []; twos = []
for _ in range(200):
    xs = [1e9 + random.gauss(0, 3) for _ in range(250)]
    outs.append(onepass(xs)); twos.append(statistics.variance(xs))
check('sim zeros', sum(v == 0 for v in outs), 100); check('sim range', max(abs(v) for v in outs), 263.2, abs_=0.05)
check('sim two-pass about 9', statistics.mean(twos), 9, abs_=0.3)
check('book ratio^2 u', 2**-53 * (1e9 / 3)**2, 12, abs_=1)

# ---------- every code widget: solution passes, starter fails ----------
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'numerics')
FILES = ['l1-floating-point', 'l2-cancellation', 'l3-conditioning', 'l4-stability', 'review-1', 'homework-1']
def widgets(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code':
            yield o
        for v in o.values():
            yield from widgets(v)
    elif isinstance(o, list):
        for v in o:
            yield from widgets(v)
def run_case(ns, case):
    if case.get('setup'):
        exec(case['setup'], ns)
    cmp = case.get('compare', 'equal')
    if cmp == 'raises':
        try:
            eval(case['call'], ns); return False
        except Exception as ex:
            return type(ex).__name__ == case['expect']
    got = eval(case['call'], ns); want = eval(case['expect'], ns)
    tol = case.get('tol')
    rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
    def close(a, b):
        a = a.tolist() if hasattr(a, 'tolist') else a; b = b.tolist() if hasattr(b, 'tolist') else b
        if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(close(p, q) for p, q in zip(a, b))
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    if cmp == 'isclose':
        return close(got, want)
    g = got.tolist() if hasattr(got, 'tolist') else got
    return g == want
for f in FILES:
    for w in widgets(json.load(open(os.path.join(BASE, f + '.json')))):
        for label, src, must_pass in [('solution', w['solution'], True), ('starter', w['starter'], False)]:
            ns = {'__learner_source__': src}
            exec(src, ns)
            results = []
            for case in w['tests']:
                try:
                    results.append(bool(run_case(ns, case)))
                except Exception:
                    results.append(False)
            if must_pass and not all(results):
                fails.append(f'{f}: solution fails tests {[i + 1 for i, r in enumerate(results) if not r]}')
            if not must_pass and all(results):
                fails.append(f'{f}: starter passes every test')


# ---------- fix pass: values changed after the second read (mpmath reference) ----------
mp.dps = 50
xe = mexp(mpf('1e-10')) - 1
re_ = abs((mpf(math.exp(1e-10) - 1) - xe) / xe)
check('l2 expm1 relative error 8.27e-8', float(re_), 8.27e-8, rel=0.002)
check('l2 correct digits left 7.1 (so 8.9 of 16 lost)', float(-mlog(re_, 10)), 7.08, abs_=0.01)
def troot_err(b):
    bm = mpf(b); true = (bm - msqrt(bm * bm - 4)) / 2
    got = (b - math.sqrt(b * b - 4)) / 2
    return float(abs((mpf(got) - true) / true))
check('l2 b=1e5 leaves about 6.5 digits', -math.log10(troot_err(1e5)), 6.47, abs_=0.3)
check('l2 b=1e1 error near 1e-14.4', math.log10(troot_err(1e1)) < -14, True)
check('l2 b=1e8 error about 0.255', troot_err(1e8), 0.255, abs_=0.01)
check('l2 range costs about 14 digits', -math.log10(troot_err(1e1)) + math.log10(troot_err(1e8)) , 13.8, abs_=0.6)
rt = msqrt(mpf(10) ** 16 - 4)
check('l2 stored root error below half-gap 7.45e-9', float(abs(mpf(math.sqrt(1e16 - 4)) - rt)) <= 2.0 ** -27 + 1e-20, True)
check('l2 gap b - sqrt(b^2-4) is 2e-8', float(mpf(10) ** 8 - rt), 2e-8, rel=1e-6)
check('l2 b and b^2 - 4 are exact', 1e16 - 4 == 9999999999999996.0 and float(10 ** 8) == 10 ** 8, True)
check('l2 ulp at 1e8 is 2^-26, half 7.45e-9', math.ulp(1e8) / 2, 7.450580596923828e-09, rel=1e-12)
check('l2 delta estimate 0.6324 has two correct digits', abs(0.6324 - 0.636831) / 0.636831 < 0.01, True)
rng = np.random.default_rng(3)
def onepass_rel(sd, days=250):
    x = 1e9 + np.round(rng.normal(0, sd, days), 2); xs = [Fraction(float(v)) for v in x]
    m = sum(xs) / days; true = float(sum((v - m) ** 2 for v in xs) / days)
    got = float(np.mean(x ** 2) - np.mean(x) ** 2); return abs(got - true) / true, got
res_small = [onepass_rel(3.0) for _ in range(40)]
check('l2 q-book-variance with moves of a few pounds: one-pass is mostly wrong', sum(r > 0.5 for r, _ in res_small) > 30, True)
check('l2 same with moves of a few thousand pounds: worst error under 1e-3', max(onepass_rel(3000.0)[0] for _ in range(40)) < 1e-3, True)
check('r1 h* = 2 sqrt(100 eps) = 2.98e-7', 2 * math.sqrt(100 * EPS) / 1e-7, 2.98, abs_=0.005)
check('r1 noroot slip 4.44e-7', 2 * 100 * EPS / 1e-7, 4.44e-7, rel=0.002)
check('r1 float32 gap at 1e6 is 0.0625, a penny vanishes', float(np.float32(1e6) + np.float32(0.01)) == 1e6 and np.spacing(np.float32(1e6)) == np.float32(0.0625), True)
A_ = lambda e: np.array([[1, 1], [e, 0], [0, e]]); b_ = lambda e: A_(e) @ np.array([1.0, 1.0])
Ae = A_(1e-7); sol = np.linalg.solve(Ae.T @ Ae, Ae.T @ b_(1e-7))
check('l4 lauchli 1e-7: normal equations lose about one digit', float(np.max(np.abs(sol - 1))) < 1e-13, True)
check('l4 kappa^2 u near 0.02', (math.sqrt(2) / 1e-7) ** 2 * 1.1e-16, 0.02, rel=0.2)
check('h1 expm1: nine digits lost, seven survive', (round(16 + float(mlog(re_, 10))), round(float(-mlog(re_, 10)))), (9, 7))

if fails:
    print('\n'.join(fails)); print(f'{len(fails)} check(s) failed'); sys.exit(1)
print('numerics L1: all checks passed')
