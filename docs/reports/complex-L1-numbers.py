"""Recompute every number stated in complex level 1 (l1 to l4, review-1, homework-1), each two ways.
Method 1 is exact arithmetic (fractions, closed forms, hand recurrences); method 2 is floating point
(Python complex, cmath, NumPy). Each figure is checked against the value the content states.
It also runs every code widget of the level in CPython: the solution must pass every example and
test, and the starter must fail at least one test (the same comparison rules as the app's code widget).
Run: python3 docs/reports/complex-L1-numbers.py   (exits 0 when every check passes)
"""
import cmath, json, math, os, sys
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'complex')
fails = []


def check(name, a, b, stated, tol=5e-5):
    a, b, s = complex(a), complex(b), complex(stated)
    ok = abs(a - b) <= 1e-9 * max(1, abs(a)) and abs((a - s).real) <= tol and abs((a - s).imag) <= tol  # tol per part: the rounding of the stated figure
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {a:.6g} | {b:.6g} | stated {s:.6g}")
    if not ok:
        fails.append(name)


class Q:
    """Exact complex number with Fraction parts."""
    def __init__(self, re, im=0):
        self.re, self.im = F(re), F(im)
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


I = Q(0, 1)
# ---------------- l1 ----------------
check('l1 hook (x - 2)^2 at x = 2 + i', (((Q(2) + I) - 2) ** 2).c(), ((2 + 1j) - 2) ** 2, -1)
check('l1 discriminant of x^2 + 2x + 5', 2 * 2 - 4 * 5, (2 ** 2 - 20), -16)
check('l1 root -1 + 2i of x^2 + 2x + 5', ((Q(-2) + 4 * I) / 2).c(), (-2 + cmath.sqrt(-16)) / 2, -1 + 2j)
check('l1 (-1 + 2i)^2', (Q(-1, 2) ** 2).c(), (-1 + 2j) ** 2, -3 - 4j)
check('l1 check z^2 + 2z + 5 = 0', (Q(-1, 2) ** 2 + 2 * Q(-1, 2) + 5).c(), (-1 + 2j) ** 2 + 2 * (-1 + 2j) + 5, 0)
check('l1 (3 + 2i)(1 - 4i)', (Q(3, 2) * Q(1, -4)).c(), (3 + 2j) * (1 - 4j), 11 - 10j)
check('l1 i^2026 by cycle (2026 = 4*506 + 2)', [1, 1j, -1, -1j][2026 % 4], (I ** (2026 % 4)).c(), -1)
check('l1 2026 = 4 x 506 + 2', 4 * 506 + 2, 2026, 2026)
check('l1 (3 + 2i)(3 - 2i)', (Q(3, 2) * Q(3, -2)).c(), (3 + 2j) * (3 - 2j), 13)
check('l1 (3 + 2i)/(1 - 4i) = (-5 + 14i)/17', (Q(3, 2) / Q(1, -4)).c(), (3 + 2j) / (1 - 4j), -0.2941 + 0.8235j)
check('l1 trap sqrt(-4) sqrt(-9)', (Q(0, 2) * Q(0, 3)).c(), cmath.sqrt(-4) * cmath.sqrt(-9), -6)
check('l1 1j ** 2026 in floating point', 1j ** 2026, complex(-1, 1.2050400707482638e-13), complex(-1, 1.2e-13), tol=1e-14)
check('l1 spread roots 0.5 + 0.5i', ((Q(1) + I) / 2).c(), (1 + cmath.sqrt(1 - 2)) / 2, 0.5 + 0.5j)
check('l1 hook roots: sum -b/a', (Q(-1, 2) + Q(-1, -2)).c(), -2 / 1, -2)
check('l1 hook roots: product c/a', (Q(-1, 2) * Q(-1, -2)).c(), 5 / 1, 5)
rho_exact, rho_float = [F(1), F(1) / (1 - F(-1, 2))], [1, 1 / 1.5]
for k in range(2, 11):
    rho_exact.append(rho_exact[-1] - F(1, 2) * rho_exact[-2]); rho_float.append(rho_float[-1] - 0.5 * rho_float[-2])
for k, s in zip(range(1, 9), [0.6667, 0.1667, -0.1667, -0.25, -0.1667, -0.0417, 0.0417, 0.0625]):
    check(f'l1 spread rho_{k}', float(rho_exact[k]), rho_float[k], s)
check('l1 quiz (2 - i)(2 + i)', (Q(2, -1) * Q(2, 1)).c(), (2 - 1j) * (2 + 1j), 5)
check('l1 quiz (1 + i)^2', (Q(1, 1) ** 2).c(), (1 + 1j) ** 2, 2j)
check('l1 quiz 1/i', (Q(1) / I).c(), 1 / 1j, -1j)
check('l1 quiz x^2 - 2x + 1 repeated root', (Q(2) / 2).c(), (2 + cmath.sqrt(4 - 4)) / 2, 1)

# ---------------- l2 ----------------
check('l2 |3 + 4i|', math.sqrt(9 + 16), abs(3 + 4j), 5)
check('l2 Arg(3 + 4i)', math.atan(4 / 3), cmath.phase(3 + 4j), 0.9273)
check('l2 Arg(3 + 4i) degrees', math.degrees(math.atan(4 / 3)), math.degrees(cmath.phase(3 + 4j)), 53.13, tol=0.005)
check('l2 slip atan(3/4)', math.atan(3 / 4), math.atan2(3, 4), 0.6435)
check('l2 z zbar for 3 + 4i', (Q(3, 4) * Q(3, -4)).c(), abs(3 + 4j) ** 2, 25)
check('l2 |z - w| = sqrt 13', math.sqrt(13), abs((3 + 4j) - (1 + 1j)), 3.6056)
check('l2 slip 5 - sqrt 2', 5 - math.sqrt(2), abs(3 + 4j) - abs(1 + 1j), 3.5858)
check('l2 slip |z + w| = sqrt 41', math.sqrt(41), abs(4 + 5j), 6.4031)
p_exact = complex(1 - math.sqrt(3), 1 + math.sqrt(3))
check('l2 (1 + i)(1 + sqrt3 i)', p_exact, (1 + 1j) * (1 + math.sqrt(3) * 1j), -0.7321 + 2.7321j)
check('l2 |zw| = 2 sqrt 2', 2 * math.sqrt(2), abs(p_exact), 2.8284)
check('l2 arg zw = 105 degrees', 45 + 60, math.degrees(cmath.phase(p_exact)), 105, tol=1e-9)
check('l2 7 pi / 12 = 105 degrees', 7 * math.pi / 12, math.radians(105), 1.8326)
check('l2 slip sqrt2 + 2', math.sqrt(2) + 2, abs(1 + 1j) + abs(1 + math.sqrt(3) * 1j), 3.4142)
check('l2 trap Arg(-1 - i)', -3 * math.pi / 4, cmath.phase(-1 - 1j), -2.3562)
check('l2 trap 5 pi / 4 (not principal)', 5 * math.pi / 4, cmath.phase(-1 - 1j) + 2 * math.pi, 3.9270)
check('l2 Arg(-2) = pi', math.pi, math.atan2(0, -2), math.pi)
check('l2 signed zero phase', -math.pi, cmath.phase(complex(-1, -0.0)), -math.pi, tol=1e-12)


def ar2(phi1, phi2):
    d = phi1 * phi1 + 4 * phi2
    if d >= 0: return None
    z = complex(phi1 / 2, math.sqrt(-d) / 2)
    return abs(z), 2 * math.pi / cmath.phase(z)


for (a, b), (m, per) in [((1, -0.5), (0.7071067811865476, 8.0)), ((1.2, -0.5), (0.7071067811865476, 11.268290043524956)), ((0, -0.25), (0.5, 4.0)), ((-1, -0.5), (0.7071067811865476, 2.6666666666666665))]:
    r = np.roots([1, -a, -b]); z = r[np.argmax(r.imag)]
    check(f'l2 ar2_cycle{(a, b)} modulus = sqrt(-phi2)', math.sqrt(-b), abs(z), m, tol=1e-12)
    check(f'l2 ar2_cycle{(a, b)} period', ar2(a, b)[1], 2 * math.pi / np.angle(z), per, tol=1e-9)
check('l2 ar2_cycle(1.2, -0.32) real roots 0.8', max(np.roots([1, -1.2, 0.32]).real), (1.2 + math.sqrt(1.44 - 1.28)) / 2, 0.8)
check('l2 spread modulus sqrt 0.5', math.sqrt(0.5), abs(0.5 + 0.5j), 0.7071)
check('l2 spread period 2 pi / (pi / 4)', 2 * math.pi / (math.pi / 4), 2 * math.pi / cmath.phase(0.5 + 0.5j), 8)
check('l2 roots reach circle at phi2 = -1', -1, -abs(complex(0.5, math.sqrt(-1 - 4 * -1) / 2)) ** 2, -1)
check('l2 roots turn complex at phi2 = -0.25', -1 / 4, -(1 ** 2) / 4, -0.25)
check('l2 quiz |-5 + 12i|', math.sqrt(25 + 144), abs(-5 + 12j), 13)
check('l2 triangle bounds 3 + 4 and 4 - 3', 3 + 4, abs(3 + 4), 7)

# ---------------- l3 ----------------
stated_sums = [1, 1 + 3.1416j, -3.9348 + 3.1416j, -3.9348 - 2.0261j, 0.1239 - 2.0261j, 0.1239 + 0.5240j, -1.2114 + 0.5240j]
s, t, z = 0, 1, 1j * math.pi
for k in range(11):
    s += z ** k / math.factorial(k)
    pi_k = math.pi ** k / math.factorial(k)
    if k < len(stated_sums):
        check(f'l3 partial sum to x^{k}', s, sum((1j * math.pi) ** j / math.factorial(j) for j in range(k + 1)), stated_sums[k])
check('l3 partial sum to x^10', s, sum(np.array([(1j * np.pi) ** j / math.factorial(j) for j in range(11)])), -1.0018 + 0.0069j)
check('l3 e^{i pi}', complex(math.cos(math.pi), math.sin(math.pi)), cmath.exp(1j * math.pi), -1, tol=1e-12)
check('l3 e^{2 pi i / 3}', complex(-0.5, math.sqrt(3) / 2), cmath.exp(2j * math.pi / 3), -0.5 + 0.866j)
check('l3 2 pi / 3 rad', 2 * math.pi / 3, math.radians(120), 2.0944)
check('l3 i(2 + i)', (I * Q(2, 1)).c(), 1j * (2 + 1j), -1 + 2j)
check('l3 (3 + 4i) turned 30 degrees', complex(3 * math.sqrt(3) / 2 - 2, 1.5 + 2 * math.sqrt(3)), (3 + 4j) * cmath.exp(1j * math.pi / 6), 0.5981 + 4.9641j)
check('l3 (1 + i)^8', (Q(1, 1) ** 8).c(), math.sqrt(2) ** 8 * cmath.exp(2j * math.pi), 16, tol=1e-9)
check('l3 (1 + i)^10', (Q(1, 1) ** 10).c(), math.sqrt(2) ** 10 * cmath.exp(10j * math.pi / 4), 32j, tol=1e-9)
for th in (0.3, 1.1, 2.5):
    c = math.cos(th)
    check(f'l3 cos 3 theta = 4c^3 - 3c at {th}', 4 * c ** 3 - 3 * c, (cmath.exp(1j * th) ** 3).real, math.cos(3 * th), tol=1e-12)
check('l3 |e^{2 + 3i}| = e^2', math.exp(2), abs(cmath.exp(2 + 3j)), 7.3891)
check('l3 slip e^5', math.exp(5), abs(cmath.exp(5)), 148.41, tol=0.005)
check('l3 slip e^{sqrt 13}', math.exp(math.sqrt(13)), math.exp(abs(2 + 3j)), 36.80, tol=0.005)
check('l3 e^{90i}', complex(math.cos(90), math.sin(90)), cmath.exp(90j), -0.4481 + 0.8940j)
check('l3 e^{i}', complex(math.cos(1), math.sin(1)), cmath.exp(1j), 0.5403 + 0.8415j)
check('l3 coin CF at pi/3', math.cos(math.pi / 3), (0.5 * cmath.exp(1j * math.pi / 3) + 0.5 * cmath.exp(-1j * math.pi / 3)).real, 0.5)
check('l3 slip cosh(pi/3)', math.cosh(math.pi / 3), (math.exp(math.pi / 3) + math.exp(-math.pi / 3)) / 2, 1.6003)
check('l3 slip sin(pi/3)', math.sqrt(3) / 2, math.sin(math.pi / 3), 0.8660)
for n, st in [(10, -1.5934 + 0.1561j), (100, -1.0506 + 0.0011j), (1000, -1.0049 + 0.0000j)]:
    m, a = (1 + math.pi ** 2 / n ** 2) ** (n / 2), n * math.atan(math.pi / n)
    check(f'l3 (1 + i pi / n)^n at n = {n}', m * cmath.exp(1j * a), (1 + 1j * math.pi / n) ** n, st, tol=6e-5)
check('l3 e^pi slip', math.exp(math.pi), cmath.exp(math.pi).real, 23.14, tol=0.005)
check('l3 (2 - i)^5 test value', (Q(2, -1) ** 5).c(), (2 - 1j) ** 5, -38 - 41j)

# ---------------- l4 ----------------
w = [complex(-0.5, math.sqrt(3) / 2), complex(-0.5, -math.sqrt(3) / 2)]
for k, v in enumerate(w, 1):
    check(f'l4 cube root of unity w{k}', v, cmath.exp(2j * math.pi * k / 3), v.real + 1j * round(v.imag, 4), tol=5e-5)
    check(f'l4 w{k}^3 = 1', v ** 3, cmath.exp(2j * math.pi * k), 1, tol=1e-12)
check('l4 i^6 = -1', (I ** 6).c(), 1j ** 6, -1, tol=1e-12)
check('l4 (e^{i pi/6})^6 = -1', cmath.exp(1j * math.pi / 6) ** 6, cmath.exp(1j * math.pi), -1, tol=1e-12)
check('l4 sixth root e^{i pi/3}', complex(0.5, math.sqrt(3) / 2), cmath.exp(1j * math.pi / 3), 0.5 + 0.8660j)
roots8i = [complex(math.sqrt(3), 1), complex(-math.sqrt(3), 1), -2j]
for k, v in enumerate(roots8i):
    check(f'l4 cube root of 8i, k = {k}', v, 2 * cmath.exp(1j * (math.pi / 2 + 2 * math.pi * k) / 3), v, tol=1e-12)
    check(f'l4 cube root of 8i, k = {k}, cubed', v ** 3, 8j, 8j, tol=1e-9)
check('l4 Python (8j) ** (1/3)', (8j) ** (1 / 3), roots8i[0], 1.7321 + 1.0000j)
check('l4 slip 8/3 modulus', F(8, 3), 8 / 3, 2.6667)
check('l4 fourth root of -16, first quadrant', complex(math.sqrt(2), math.sqrt(2)), 2 * cmath.exp(1j * math.pi / 4), 1.4142 + 1.4142j)
check('l4 fourth root of -16 to the 4th', complex(math.sqrt(2), math.sqrt(2)) ** 4, (Q(1, 1) ** 4 * 4).c(), -16, tol=1e-9)
check('l4 slip (2, 2) has modulus 2 sqrt 2', 2 * math.sqrt(2), abs(2 + 2j), 2.8284)
check('l4 fifth roots of unity sum', sum(cmath.exp(2j * math.pi * k / 5) for k in range(5)), np.sum(np.exp(2j * np.pi * np.arange(5) / 5)), 0, tol=1e-12)
check('l4 seventh roots of unity sum', sum(cmath.exp(2j * math.pi * k / 7) for k in range(7)), 0, 0, tol=1e-12)
vol = [10, 12, 11, 9, 8] * 4
Xd = [sum(vol[k] * cmath.exp(-2j * math.pi * j * k / 20) for k in range(20)) for j in range(20)]
Xn = np.fft.fft(vol)
for j, st in [(0, 200), (4, 19.9192), (8, 1.7961), (12, 1.7961), (16, 19.9192)]:
    check(f'l4 |X_{j}| of the volume series', abs(Xd[j]), abs(Xn[j]), st)
check('l4 every other |X_j| is 0', max(abs(Xd[j]) for j in range(20) if j % 4), max(abs(Xn[j]) for j in range(20) if j % 4), 0, tol=1e-9)
check('l4 period 20 / 4', 20 / 4, 20 / (1 + int(np.argmax(np.abs(Xn[1:11])))), 5)
check('l4 dft([1, 2, 3, 4])[1]', sum([1, 2, 3, 4][k] * (Q(0, -1) ** k).c() for k in range(4)), np.fft.fft([1, 2, 3, 4])[1], -2 + 2j, tol=1e-12)
check('l4 cube root of -8: 1 + sqrt3 i', complex(1, math.sqrt(3)), 2 * cmath.exp(1j * math.pi / 3), 1 + 1.7321j)
check('l4 cube root of -8: (1 + sqrt3 i)^3', complex(1, math.sqrt(3)) ** 3, -8, -8, tol=1e-9)

# ---------------- review-1 ----------------
check('r1 (1 + 2i)/(2 - i)', (Q(1, 2) / Q(2, -1)).c(), (1 + 2j) / (2 - 1j), 1j)
check('r1 |-2 + 2i|', 2 * math.sqrt(2), abs(-2 + 2j), 2.8284)
check('r1 Arg(-2 + 2i)', 3 * math.pi / 4, cmath.phase(-2 + 2j), 2.3562)
check('r1 slip arctan(-1)', -math.pi / 4, math.atan(-1), -0.7854)
check('r1 (1 + 2i)(1 - i)', (Q(1, 2) * Q(1, -1)).c(), (1 + 2j) * (1 - 1j), 3 + 1j)
check('r1 |3 + i| = sqrt5 sqrt2', math.sqrt(5) * math.sqrt(2), abs(3 + 1j), math.sqrt(10))
check('r1 i^99', (I ** (99 % 4)).c(), [1, 1j, -1, -1j][99 % 4], -1j)
check('r1 e^{i pi/3}', complex(0.5, math.sqrt(3) / 2), cmath.exp(1j * math.pi / 3), 0.5 + 0.8660j)
check('r1 sqrt(-2) sqrt(-8)', -math.sqrt(16), cmath.sqrt(-2) * cmath.sqrt(-8), -4)
check('r1 roots of z^2 - 0.6z + 0.25', complex(0.3, 0.4), max(np.roots([1, -0.6, 0.25]), key=lambda r: r.imag), 0.3 + 0.4j)
check('r1 modulus 0.5', math.sqrt(0.25), abs(0.3 + 0.4j), 0.5)
check('r1 |e^{1 + i pi}|', math.e, abs(cmath.exp(1 + 1j * math.pi)), 2.7183)
check('r1 slip e^{1 + pi}', math.exp(1 + math.pi), abs(cmath.exp(1 + math.pi)), 62.9029, tol=5e-4)

# ---------------- homework-1 ----------------
check('h1 (2 - 3i)/(1 + i)', (Q(2, -3) / Q(1, 1)).c(), (2 - 3j) / (1 + 1j), -0.5 - 2.5j)
check('h1 Arg(-sqrt3 + i)', 5 * math.pi / 6, cmath.phase(complex(-math.sqrt(3), 1)), 2.618)
check('h1 slip -pi/6', -math.pi / 6, math.atan(1 / -math.sqrt(3)), -0.5236)
check('h1 (1 - i)^12', (Q(1, -1) ** 12).c(), (1 - 1j) ** 12, -64, tol=1e-9)
for k in range(4):
    r = math.sqrt(2) * cmath.exp(1j * (math.pi + 2 * math.pi * k) / 4)
    check(f'h1 fourth root of -4, k = {k}', r, [1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j][k], [1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j][k], tol=1e-12)
check('h1 (1 + i)^4 = -4', (Q(1, 1) ** 4).c(), (1 + 1j) ** 4, -4)
check('h1 sqrt2^4 = 4 (the slip solves z^4 = 4)', (Q(2) ** 2).c(), math.sqrt(2) ** 4, 4, tol=1e-12)
zr = complex(0.6, math.sqrt(0.56) / 2)
check('h1 spread roots 0.6 + 0.3742i', zr, max(np.roots([1, -1.2, 0.5]), key=lambda r: r.imag), 0.6 + 0.3742j)
check('h1 discriminant -0.56', 1.44 - 2, 1.2 ** 2 + 4 * -0.5, -0.56)
check('h1 modulus sqrt 0.5', math.sqrt(0.36 + 0.14), abs(zr), 0.7071)
check('h1 argument 0.5576', math.atan(math.sqrt(0.14) / 0.6), cmath.phase(zr), 0.5576)
check('h1 argument in degrees', math.degrees(math.atan(math.sqrt(0.14) / 0.6)), math.degrees(np.angle(zr)), 31.9, tol=0.05)
check('h1 cycle 11.27 days', 2 * math.pi / math.atan(math.sqrt(0.14) / 0.6), 2 * math.pi / np.angle(zr), 11.27, tol=0.005)
check('h1 lag-polynomial root modulus', 1 / math.sqrt(0.5), abs(1 / zr), 1.4142)
rho = [F(1), F(12, 10) / (1 - F(-5, 10))]
rf = [1.0, 1.2 / 1.5]
for k in range(2, 11):
    rho.append(F(12, 10) * rho[-1] - F(5, 10) * rho[-2]); rf.append(1.2 * rf[-1] - 0.5 * rf[-2])
for k, st in [(1, 0.8), (2, 0.46), (3, 0.152), (4, -0.0476), (5, -0.1331), (6, -0.1359)]:
    check(f'h1 spread rho_{k}', float(rho[k]), rf[k], st)
check('h1 rho back above 0 at lag 10 (rho_9 < 0)', float(rho[9]) < 0 and float(rho[10]) > 0, rf[9] < 0 < rf[10], True)
check('h1 envelope halves every 2 days', math.log(0.5) / math.log(math.sqrt(0.5)), 2, 2, tol=1e-9)
check('h1 half cycle 5.6 days', math.pi / cmath.phase(zr), 11.268290043524956 / 2, 5.6, tol=0.05)
check('h1 stationary test (0.5, 0.3) real roots', max(np.roots([1, -0.5, -0.3]).real), (0.5 + math.sqrt(0.25 + 1.2)) / 2, 0.852, tol=5e-4)
check('h1 stationary test (0.5, 0.3) second root', min(np.roots([1, -0.5, -0.3]).real), (0.5 - math.sqrt(0.25 + 1.2)) / 2, -0.352, tol=5e-4)
check('h1 stationary test (0, -1.2) modulus', math.sqrt(1.2), abs(cmath.sqrt(-4 * 1.2) / 2), 1.0954)
check('h1 FFT steps 4096 log2 4096', 4096 * 12, 4096 * math.log2(4096), 49152, tol=0)
check('h1 DFT terms 4096^2', 4096 ** 2, float(4096) ** 2, 16777216, tol=0)

# ---------------- code widgets: solution passes, starter fails ----------------


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


for name in ['l1-square-root-of-minus-one', 'l2-points-in-a-plane', 'l3-euler', 'l4-roots-of-unity', 'review-1', 'homework-1']:
    doc = json.load(open(os.path.join(COURSE, name + '.json')))
    for where, w in widgets(doc, name):
        sol = run(w['solution'], w, list(w.get('examples', [])) + w['tests'])
        st = run(w['starter'], w, [c for c in w['tests'] if c.get('budget') is None])
        ok = all(sol) and not all(st)
        print(f"{'ok  ' if ok else 'FAIL'} code {where}: solution {sum(sol)}/{len(sol)}, starter fails {len(st) - sum(st)}/{len(st)}")
        if not ok: fails.append('code ' + where)

print(f'\n{len(fails)} failing checks' + (': ' + ', '.join(fails) if fails else ''))
sys.exit(1 if fails else 0)
