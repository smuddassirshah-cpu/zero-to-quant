"""Recompute every number stated in complex level 2 (l5 to l8, review-2, homework-2), each two ways.
Method 1 is exact arithmetic or a closed form; method 2 is floating point by another route (cmath, NumPy,
finite differences, SciPy's complex erf, a direct iteration). Each figure is checked against the stated value.
It also runs every code widget of the level in CPython: the solution must pass every example and test,
and the starter must fail at least one test (the app's comparison rules). Needs NumPy and SciPy.
Run: python3 docs/reports/complex-L2-numbers.py   (exits 0 when every check passes)
"""
import cmath, json, math, os, sys
from fractions import Fraction as F

import numpy as np
from scipy.special import erf as cerf

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'complex')
fails = []


def check(name, a, b, stated, tol=5e-5):
    a, b, s = complex(a), complex(b), complex(stated)
    ok = abs(a - b) <= 1e-8 * max(1, abs(a)) and abs((a - s).real) <= tol and abs((a - s).imag) <= tol
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {a:.6g} | {b:.6g} | stated {s:.6g}")
    if not ok:
        fails.append(name)


class Q:
    """Exact complex number with Fraction parts."""
    def __init__(self, re, im=0): self.re, self.im = F(re), F(im)
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.re + o.re, s.im + o.im)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.re - o.re, s.im - o.im)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o); return Q(s.re * o.re - s.im * o.im, s.re * o.im + s.im * o.re)
    __rmul__ = __mul__
    def conj(s): return Q(s.re, -s.im)
    def __truediv__(s, o):
        o = o if isinstance(o, Q) else Q(o); d = o.re ** 2 + o.im ** 2; t = s * o.conj(); return Q(t.re / d, t.im / d)
    def __pow__(s, n):
        r = Q(1)
        for _ in range(n): r = r * s
        return r
    def c(s): return complex(float(s.re), float(s.im))


def partials(f, x, y, h=1e-6):
    fx = (f(complex(x + h, y)) - f(complex(x - h, y))) / (2 * h)
    fy = (f(complex(x, y + h)) - f(complex(x, y - h))) / (2 * h)
    return fx.real, fy.real, fx.imag, fy.imag  # u_x, u_y, v_x, v_y


# ---------------- l5 ----------------
for th in (0.4, 1.9, 3.0):
    check(f'l5 z^2 doubles the angle at {th}', 2 * th, cmath.phase(cmath.exp(1j * th) ** 2) % (2 * math.pi), 2 * th, tol=1e-12)
check('l5 (1 + i)(2 + i)', (Q(1, 1) * Q(2, 1)).c(), (1 + 1j) * (2 + 1j), 1 + 3j)
check('l5 |1 + i| = sqrt 2', math.sqrt(2), abs(1 + 1j), 1.4142)
for t, st in zip(range(-2, 3), [-3 - 4j, -2j, 1, 2j, -3 + 4j]):
    check(f'l5 (1 + {t}i)^2', (Q(1, t) ** 2).c(), complex(1 - t * t, 2 * t), st)
    w = (1 + 1j * t) ** 2
    check(f'l5 parabola u = 1 - v^2/4 at t = {t}', w.real, 1 - w.imag ** 2 / 4, w.real, tol=1e-12)
check('l5 (1 + i)^2 = 2i', (Q(1, 1) ** 2).c(), (1 + 1j) ** 2, 2j)
check('l5 preimage 1 + 2i of -3 + 4i', (Q(1, 2) ** 2).c(), cmath.sqrt(-3 + 4j) ** 2, -3 + 4j)
check('l5 principal sqrt(-3 + 4i)', cmath.sqrt(-3 + 4j), np.sqrt(-3 + 4j), 1 + 2j)
check('l5 slip (2 + i)^2', (Q(2, 1) ** 2).c(), (2 + 1j) ** 2, 3 + 4j)
check('l5 slip (1 - 2i)^2', (Q(1, -2) ** 2).c(), (1 - 2j) ** 2, -3 - 4j)
for z, st in [(0, 0), (1, 1), (1 + 1j, 2j), (1j, -1)]:
    check(f'l5 square corner {z}', (Q(complex(z).real, complex(z).imag) ** 2).c(), complex(z) ** 2, st)
check('l5 1/(1 + i)', (Q(1) / Q(1, 1)).c(), 1 / (1 + 1j), 0.5 - 0.5j)
check('l5 1/2 on Re w = 1/2', (Q(1) / Q(2)).c(), 1 / 2, 0.5)
circ = [1 + cmath.exp(1j * t) for t in np.linspace(0.1, 6.1, 13)]
check('l5 circle |z - 1| = 1 maps to Re w = 1/2', max(abs((1 / z).real - 0.5) for z in circ), 0, 0, tol=1e-12)
check('l5 trap: 1/2 at z = 2 against conj 2', 1 / 2, (Q(2).conj() / 4).c(), 0.5)
check('l5 mean log return r - sigma^2/2', 0.05 - 0.2 ** 2 / 2, F(5, 100) - F(4, 100) / 2, 0.03, tol=1e-12)
phi = lambda u: cmath.exp(0.03j * u - 0.02 * u * u)
check('l5 |phi(5)| = e^-0.5', math.exp(-0.5), abs(phi(5)), 0.6065)
check('l5 angle phi(5) = 0.15', 0.03 * 5, cmath.phase(phi(5)), 0.15, tol=1e-12)
check('l5 |phi(10)| = e^-2', math.exp(-2), abs(phi(10)), 0.1353)
check('l5 angle phi(10) = 0.3', 0.03 * 10, cmath.phase(phi(10)), 0.3, tol=1e-12)
check('l5 slip e^0.5', math.exp(0.5), abs(cmath.exp(0.5)), 1.6487)
check('l5 quiz (2i)^2', (Q(0, 2) ** 2).c(), (2j) ** 2, -4)

# ---------------- l6 ----------------
for a in (0.0, 0.7, 2.0):
    h = 0.001 * cmath.exp(1j * a)
    check(f'l6 z^2 quotient = 2z + h at {a}', ((1 + 1j + h) ** 2 - (1 + 1j) ** 2) / h, 2 * (1 + 1j) + h, 2 + 2j, tol=0.0011)
for a, st in [(0, 1), (math.pi / 4, -1j), (math.pi / 2, -1)]:
    h = 0.001 * cmath.exp(1j * a)
    check(f'l6 conj quotient at {a:.4f}', cmath.exp(-2j * a), h.conjugate() / h, st, tol=1e-12)
check("l6 (z^3 - 2z)' at i", 3 * (Q(0, 1) ** 2).c() - 2, ((1j + 1e-7) ** 3 - 2 * (1j + 1e-7) - ((1j - 1e-7) ** 3 - 2 * (1j - 1e-7))) / 2e-7, -5, tol=1e-6)
check('l6 amplitwist stretch |2 + 2i|', 2 * math.sqrt(2), abs(2 * (1 + 1j)), 2.8284)
check('l6 amplitwist turn 45 degrees', 45, math.degrees(cmath.phase(2 + 2j)), 45, tol=1e-9)
for a, st in [(0, 2), (math.pi / 2, 0)]:
    h = 1e-4 * cmath.exp(1j * a)
    check(f'l6 |z|^2 quotient at 1, direction {a:.4f}', 2 * math.cos(a) * cmath.exp(-1j * a), (abs(1 + h) ** 2 - 1) / h - h.conjugate(), st, tol=1e-6)  # quotient = 2 Re h / h + conj h
for a, st in [(0, 1), (math.pi / 2, 0)]:
    h = 1e-3 * cmath.exp(1j * a)
    check(f'l6 Re h / h at {a:.4f}', math.cos(a) * cmath.exp(-1j * a), h.real / h, st, tol=1e-12)
qs = [cmath.exp(-2j * 2 * math.pi * k / 8) for k in range(8)]
check('l6 spread of conj quotients', max(abs(a - b) for a in qs for b in qs), 2, 2, tol=1e-12)
qs = [math.cos(2 * math.pi * k / 8) * cmath.exp(-2j * math.pi * k / 8) for k in range(8)]
check('l6 spread of Re quotients', max(abs(a - b) for a in qs for b in qs), 1, 1, tol=1e-12)
bond = lambda y: 5 * cmath.exp(-y) + 5 * cmath.exp(-2 * y) + 105 * cmath.exp(-3 * y)
P, dP = bond(0.04).real, -(5 * math.exp(-0.04) + 10 * math.exp(-0.08) + 315 * math.exp(-0.12))
check('l6 bond price', 5 * math.exp(-0.04) + 5 * math.exp(-0.08) + 105 * math.exp(-0.12), P, 102.5462)
check("l6 bond P'(y)", dP, bond(0.04 + 1e-20j).imag / 1e-20, -293.4150)
check('l6 duration', -dP / P, -(bond(0.04 + 1e-20j).imag / 1e-20) / P, 2.8613)
from decimal import Decimal, getcontext
getcontext().prec = 60
_d = Decimal('0.04')
_exact = -(5 * (-_d).exp() + 10 * (-2 * _d).exp() + 315 * (-3 * _d).exp())
cs_err = abs(Decimal(bond(0.04 + 1e-20j).imag / 1e-20) - _exact)
check('l6 complex-step error about 4e-15 (exact reference, Decimal)', float(cs_err), float(cs_err), 4e-15, tol=5e-16)
for hh, st in [(1e-4, 4e-6), (1e-8, 2e-7), (1e-12, 4e-3)]:
    e = abs((bond(0.04 + hh).real - bond(0.04 - hh).real) / (2 * hh) - dP)
    check(f'l6 central-difference error at h = {hh}', e, e, st, tol=st / 2)
check('l6 central diff of x^3 at 2, h = 1e-3', ((2.001) ** 3 - (1.999) ** 3) / 0.002, 12 + 1e-6, 12.000001, tol=1e-9)
check('l6 quiz 4(1 + i)^3', (4 * Q(1, 1) ** 3).c(), 4 * (1 + 1j) ** 3, -8 + 8j)
check("l6 quiz f'(i) for z^3", (3 * Q(0, 1) ** 2).c(), 3 * (1j) ** 2, -3)

# ---------------- l7 ----------------
ux, uy, vx, vy = partials(lambda z: z * z, 1, 2)
for nm, a, st in [('u_x', ux, 2), ('u_y', uy, -4), ('v_x', vx, 4), ('v_y', vy, 2)]:
    check(f'l7 {nm} of z^2 at (1, 2)', {'u_x': 2 * 1, 'u_y': -2 * 2, 'v_x': 2 * 2, 'v_y': 2 * 1}[nm], a, st, tol=1e-6)
ux, uy, vx, vy = partials(lambda z: z.conjugate(), 1, 2)
check('l7 conj u_x = 1, v_y = -1', ux - vy, 2, 2, tol=1e-6)
x, y = 0.7, -1.3
ux, uy, vx, vy = partials(cmath.exp, x, y)
check('l7 e^z: u_x = v_y', ux - vy, 0, 0, tol=1e-6)
check("l7 e^z: f' = u_x + i v_x = e^z", complex(math.exp(x) * math.cos(y), math.exp(x) * math.sin(y)), complex(ux, vx), cmath.exp(complex(x, y)), tol=1e-6)
f5 = lambda z: z * z + z
for xx, yy in [(0.3, 0.8), (-1.1, 0.4)]:
    ux, uy, vx, vy = partials(f5, xx, yy)
    check(f'l7 v = 2xy + y: v_y = u_x at ({xx}, {yy})', 2 * xx + 1, ux, ux, tol=1e-6)
    check(f'l7 v = 2xy + y: v_x = -u_y at ({xx}, {yy})', 2 * yy, -uy, -uy, tol=1e-6)
z0 = complex(1.3, 0.4)
check('l7 f(1.3 + 0.4i)', (Q(F(13, 10), F(4, 10)) ** 2 + Q(F(13, 10), F(4, 10))).c(), z0 * z0 + z0, 2.83 + 1.44j)
check('l7 Laplace for x^2 - y^2', 2 + (-2), (((1.001) ** 2 - 1) - (1 - (0.999) ** 2)) / 1e-6 - 2, 0, tol=1e-6)
ux, uy, vx, vy = partials(lambda z: z.real + 1j * (z.real + z.imag), 1, 2)
check('l7 trap x + i(x + y): u_y = 0, -v_x = -1', complex(uy, -vx), complex(0, -1), complex(0, -1), tol=1e-6)


def cr(f, x, y, h=1e-5):
    fx = (f(complex(x + h, y)) - f(complex(x - h, y))) / (2 * h)
    fy = (f(complex(x, y + h)) - f(complex(x, y - h))) / (2 * h)
    return (fx.real - fy.imag, fy.real + fx.imag)


g = lambda z: z.real ** 2 + 1j * z.imag ** 2
check('l7 x^2 + iy^2 residual at (1, 1)', complex(*cr(g, 1, 1)), 0, 0, tol=1e-6)
check('l7 x^2 + iy^2 residual at (1, 2)', complex(*cr(g, 1, 2)), complex(2 * 1 - 2 * 2, 0), -2, tol=1e-6)
r_good = cr(phi, 1, -0.5)
check('l7 phi_good residuals below 1e-11', max(abs(v) for v in r_good) < 1e-11, True, True)
check('l7 phi_good residual 1', r_good[0], r_good[0], 1.0408e-12, tol=1e-15)
check('l7 phi_good residual 2', r_good[1], r_good[1], -4.5103e-12, tol=1e-15)
phi_abs = lambda u: cmath.exp(0.03j * u - 0.02 * abs(u) ** 2)
r_abs = cr(phi_abs, 1, -0.5)
check('l7 phi_abs residual 1', r_abs[0], cr(phi_abs, 1, -0.5, 1e-6)[0], -0.040178, tol=1e-6)
check('l7 phi_abs residual 2', r_abs[1], cr(phi_abs, 1, -0.5, 1e-6)[1], 0.018604, tol=1e-6)
ux, uy, vx, vy = partials(lambda z: z ** 3, 0.6, -0.9)
check('l7 quiz v = 3x^2 y - y^3: v_y = u_x', 3 * 0.36 - 3 * 0.81, vy, ux, tol=1e-6)

# ---------------- l8 ----------------
check('l8 e^z = -2 at ln 2 + i pi', cmath.exp(complex(math.log(2), math.pi)), -2, -2, tol=1e-12)
check('l8 ln 2', math.log(2), cmath.log(-2).real, 0.6931)
check('l8 e^{1 + i pi/3}', complex(math.e / 2, math.e * math.sqrt(3) / 2), cmath.exp(1 + 1j * math.pi / 3), 1.3591 + 2.3541j)
check('l8 period 2 pi i', cmath.exp(0.5 - 2.5j), cmath.exp(0.5 - 2.5j + 2j * math.pi), cmath.exp(0.5 - 2.5j), tol=1e-12)
check('l8 Log(1 + i)', complex(math.log(math.sqrt(2)), math.pi / 4), cmath.log(1 + 1j), 0.3466 + 0.7854j)
check('l8 i^i', math.exp(-math.pi / 2), (1j ** 1j).real, 0.2079)
check('l8 i^i, k = 1', math.exp(-math.pi / 2 - 2 * math.pi), cmath.exp(1j * (1j * (math.pi / 2 + 2 * math.pi))), 0.000388, tol=5e-7)
check('l8 i^i, k = -1', math.exp(-math.pi / 2 + 2 * math.pi), cmath.exp(1j * (1j * (math.pi / 2 - 2 * math.pi))), 111.3178)
check('l8 slip e^{pi/2}', math.exp(math.pi / 2), cmath.exp(math.pi / 2), 4.8105)
check('l8 Log(-1 + 0.001i)', complex(0.5 * math.log1p(1e-6), math.pi - math.atan(0.001)), cmath.log(-1 + 0.001j), 0.0000005 + 3.1406j)
check('l8 Log(-1 - 0.001i)', complex(0.5 * math.log1p(1e-6), -math.pi + math.atan(0.001)), cmath.log(-1 - 0.001j), 0.0000005 - 3.1406j)
check('l8 trap Log 1 = 0', 0, cmath.log(1), 0)
check('l8 trap 2 Log(-1) = 2 pi i', 2j * math.pi, 2 * cmath.log(-1), 2j * math.pi, tol=1e-12)
check('l8 Log(-e)', complex(1, math.pi), cmath.log(-math.e), 1 + 1j * math.pi, tol=1e-12)
check('l8 Python (-8) ** (1/3)', 2 * cmath.exp(1j * math.pi / 3), (-8) ** (1 / 3), 1 + 1.7321j)
check('l8 continuous log end 4 pi', 4 * math.pi, 9 * 0 + 8 * math.pi / 2, 12.5664)
check('l8 Log i', 1j * math.pi / 2, cmath.log(1j), 1.5708j)

# ---------------- review-2 ----------------
check('r2 (2 - i)^2', (Q(2, -1) ** 2).c(), (2 - 1j) ** 2, 3 - 4j)
check('r2 1/(2i)', (Q(1) / Q(0, 2)).c(), 1 / (2j), -0.5j)
check('r2 Im h / h for h = ik', 1 / 1j, (1j * 1e-3).imag / (1j * 1e-3), -1j, tol=1e-12)
ux, uy, vx, vy = partials(lambda z: cmath.exp(1j * z), 0.4, 0.9)
check('r2 e^{iz} satisfies CR', complex(ux - vy, uy + vx), 0, 0, tol=1e-6)
check('r2 Log(-1 - i)', complex(math.log(math.sqrt(2)), -3 * math.pi / 4), cmath.log(-1 - 1j), 0.3466 - 2.3562j)
check("r2 |f'(2)| for 1/z", 1 / 4, abs(-1 / (2 + 0j) ** 2), 0.25)
check('r2 e^z = i at i pi/2', cmath.exp(1j * math.pi / 2), 1j, 1j, tol=1e-12)
check('r2 2^i', complex(math.cos(math.log(2)), math.sin(math.log(2))), 2 ** 1j, 0.7692 + 0.6390j)

# ---------------- homework-2 ----------------
check('h2 1/(1 + 2i)', (Q(1) / Q(1, 2)).c(), 1 / (1 + 2j), 0.2 - 0.4j)
check("h2 |f'(1 + i)| for z^3", abs((3 * Q(1, 1) ** 2).c()), abs(3 * (1 + 1j) ** 2), 6)
for xx, yy in [(0.5, 0.2), (-0.7, 1.1)]:
    f9 = lambda z: z ** 3 - 1j * z
    w = f9(complex(xx, yy))
    check(f'h2 u + iv = z^3 - iz at ({xx}, {yy})', complex(xx ** 3 - 3 * xx * yy ** 2 + yy, 3 * xx ** 2 * yy - yy ** 3 - xx), w, w, tol=1e-12)
check('h2 (-1)^i', math.exp(-math.pi), ((-1 + 0j) ** 1j).real, 0.0432)
check('h2 slip e^pi', math.exp(math.pi), cmath.exp(math.pi).real, 23.1407)
Phi = lambda v: 0.5 * (1 + math.erf(v / math.sqrt(2)))


def bs(S, K, r, s, T):
    d1 = (cmath.log(S / K) + (r + s ** 2 / 2) * T) / (s * cmath.sqrt(T))
    d2 = d1 - s * cmath.sqrt(T)
    N = lambda v: 0.5 * (1 + cerf(v / math.sqrt(2)))
    return S * N(d1) - K * cmath.exp(-r * T) * N(d2)


for (S, K, r, s, T), (dst, vst) in [((100, 100, 0.05, 0.2, 1), (0.6368306511756191, 37.52403469169379)), ((110, 100, 0.03, 0.25, 0.5), (0.7618905003348194, 24.07595272500711))]:
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T))
    check(f'h2 delta {S, K, r, s, T}', Phi(d1), bs(S + 1e-20j, K, r, s, T).imag / 1e-20, dst, tol=1e-13)
    check(f'h2 vega {S, K, r, s, T}', S * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi) * math.sqrt(T), bs(S, K, r, s + 1e-20j, T).imag / 1e-20, vst, tol=1e-11)
check('h2 d1 = 0.35 at the base case', (math.log(1) + 0.07) / 0.2, 0.35, 0.35, tol=1e-12)
check('h2 call price', 100 * Phi(0.35) - 100 * math.exp(-0.05) * Phi(0.15), bs(100, 100, 0.05, 0.2, 1).real, 10.4506)
om = cmath.exp(2j * math.pi / 3)
roots = [1, om, om * om]


def newton(z0, steps=50):
    z = complex(z0)
    for _ in range(steps):
        if z == 0: return None
        z = z - (z ** 3 - 1) / (3 * z * z)
    return min(range(3), key=lambda k: abs(z - roots[k]))


def newton_np(z0, steps=50):
    z = np.complex128(z0)
    for _ in range(steps):
        if z == 0: return None
        z = z - (z ** 3 - 1) / (3 * z ** 2)
    return int(np.argmin([abs(z - rt) for rt in roots]))


for z0, st in [(2, 0), (-1 + 1j, 1), (-1 - 1j, 2), (-0.5, 0), (1j, 1), (0.5 + 0.5j, 1)]:
    check(f'h2 Newton from {z0}', newton(z0), newton_np(z0), st, tol=0)
check('h2 Newton from 0 is None', newton(0) is None, newton_np(0) is None, True)
check('h2 Newton from -0.5: one step lands on 1', -0.5 - ((-0.5) ** 3 - 1) / (3 * 0.25), float(F(-1, 2) - (F(-1, 8) - 1) / F(3, 4)), 1, tol=1e-12)
check('h2 distance 0.5 + 0.5i to 1', math.sqrt(0.5), abs(0.5 + 0.5j - 1), 0.7071)
check('h2 distance 0.5 + 0.5i to omega', math.sqrt(1 + (0.5 - math.sqrt(3) / 2) ** 2), abs(0.5 + 0.5j - om), 1.0649)

# ---------------- code widgets ----------------


def judge(a, exp, cmp, ns, tol):
    e = eval(exp, ns)
    flat = lambda v: v.tolist() if hasattr(v, 'tolist') and not isinstance(v, (int, float, complex, str)) else v

    def close(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
        rt, at = tol if tol else (1e-9, 1e-12)
        if any(isinstance(v, complex) or type(v).__name__.startswith('complex') for v in (x, y)):
            return cmath.isclose(complex(x), complex(y), rel_tol=rt, abs_tol=at)
        try:
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y
    if cmp == 'isclose':
        return close(a, e)
    return bool(flat(a) == flat(e))


def run(src, w, cases):
    ns = {'__name__': '__main__'}
    try:
        if w.get('prelude'): exec(w['prelude'], ns)
        exec(src, ns)
    except Exception:
        return [False]
    out = []
    for c in cases:
        tol = c.get('tol'); tol = (float(tol.get('rel', 0)), float(tol.get('abs', 0))) if tol else None
        try:
            if c.get('setup'): exec(c['setup'], ns)
            if c.get('compare') == 'raises':
                try:
                    eval(c['call'], ns); out.append(False)
                except Exception as x:
                    out.append(c['expect'] in [k.__name__ for k in type(x).__mro__])
            else:
                out.append(judge(eval(c['call'], ns), c['expect'], c.get('compare', 'equal'), ns, tol))
        except Exception:
            out.append(False)
    return out


def widgets(o, where):
    if isinstance(o, dict):
        if o.get('kind') == 'code' and 'tests' in o:
            yield where, o
            return
        for k, v in o.items(): yield from widgets(v, f'{where}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from widgets(v, f'{where}.{i}')


for name in ['l5-functions-move-the-plane', 'l6-complex-differentiability', 'l7-cauchy-riemann', 'l8-exp-and-log', 'review-2', 'homework-2']:
    doc = json.load(open(os.path.join(COURSE, name + '.json')))
    for where, w in widgets(doc, name):
        sol = run(w['solution'], w, list(w.get('examples', [])) + w['tests'])
        st = run(w['starter'], w, w['tests'])
        ok = all(sol) and not all(st)
        print(f"{'ok  ' if ok else 'FAIL'} code {where}: solution {sum(sol)}/{len(sol)}, starter fails {len(st) - sum(st)}/{len(st)}")
        if not ok: fails.append('code ' + where)

print(f'\n{len(fails)} failing checks' + (': ' + ', '.join(fails) if fails else ''))
sys.exit(1 if fails else 0)
