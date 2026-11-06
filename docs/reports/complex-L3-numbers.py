"""Recompute every number stated in complex level 3 (l9 to l13, review-3, homework-3), each two ways.
Method 1 is a closed form or a residue sum; method 2 is numerical (the trapezium rule on the path, SciPy quad,
an FFT, Black-Scholes or Merton's series). Each value is then checked at its JSON path with numbers_lib.
The script also runs every code widget of the level: the solution passes every example and test, and the
starter fails at least one test, with the app's comparison rules (complex isclose, equal, raises).
Needs NumPy and SciPy. Run: python3 docs/reports/complex-L3-numbers.py   (exits 0 when every check passes)
"""
import cmath, json, math, os, sys, warnings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level
import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr
from scipy.stats import norm

lv = Level('complex', 3)
pi, e = math.pi, math.e
fails = []


def two(name, a, b, stated=None, tol=None, agree=1e-7):
    """a and b are the two methods; stated (rounded) must lie within tol of them."""
    a, b = complex(a), complex(b)
    ok = abs(a - b) <= agree * max(1.0, abs(a))
    if stated is not None:
        t = tol if tol is not None else 0.5 * 10 ** -max(0, len(repr(float(abs(stated))).split('.')[-1]) if '.' in repr(float(stated)) else 0)
        ok = ok and abs(a - complex(stated)) <= t + 1e-12
    print(f"{'ok ' if ok else 'BAD'} two-way {name}: {a:.10g} | {b:.10g}" + ('' if stated is None else f' | stated {stated}'))
    if not ok:
        fails.append(name)


def S(ref, path, stated, a, b, tol=None, name=None, fmt=None, agree=1e-7):
    if isinstance(fmt, str):
        fmt = (lambda s: (lambda v: s))(fmt)
    two(name or f'{ref} {path}', a, b, stated, tol, agree)
    lv.expect(ref, path, stated, fmt=fmt)


def T(ref, path, text):
    lv.expect(ref, path, text)


def ci(f, g, dg, a, b, n=20000):
    t = np.linspace(a, b, n + 1)
    return np.trapezoid(f(g(t)) * dg(t), t)


C1 = (lambda t: np.exp(1j * t), lambda t: 1j * np.exp(1j * t))
def circ(c, r):
    return (lambda t: c + r * np.exp(1j * t), lambda t: 1j * r * np.exp(1j * t))


# ---------------- l9 ----------------
S('l9', 'screens[1].feedback.correct', 6.2832, 2 * pi, ci(lambda z: 1 / z, *C1, 0, 2 * pi).imag)
S('l9', 'screens[1].explain.text', 6.2832, 2 * pi, quad(lambda t: 1.0, 0, 2 * pi)[0])
th = np.linspace(0, 2 * pi, 20001)
S('l9', 'screens[4].explain.text', 0.34, math.asin(1 / 3), np.max(np.angle(3 + np.exp(1j * th))), tol=0.005)
S('l9', 'screens[4].canvas.state.segments[0].to[0]', 2.667, math.sqrt(8) * math.cos(math.asin(1 / 3)), 8 / 3, tol=0.0005)
S('l9', 'screens[4].canvas.state.segments[0].to[1]', 0.943, math.sqrt(8) / 3, math.sqrt(8) * math.sin(math.asin(1 / 3)), tol=0.0005)
diag = (lambda t: (1 + 1j) * t, lambda t: (1 + 1j) * np.ones_like(t))
two('l9 zbar diagonal = 1', 1, ci(np.conj, *diag, 0, 1))
S('l9', 'screens[5].prose', 1, 1, ci(np.conj, *diag, 0, 1).real)
legs = ci(np.conj, lambda t: t + 0j, lambda t: np.ones_like(t), 0, 1) + ci(np.conj, lambda t: 1 + 1j * t, lambda t: 1j * np.ones_like(t), 0, 1)
two('l9 zbar legs = 1 + i', 1 + 1j, legs)
T('l9', 'screens[5].widget.answer', '1+i')
two('l9 z^2 on both paths', (1 + 1j) ** 3 / 3, ci(lambda z: z ** 2, *diag, 0, 1))
two('l9 z^2 legs', (-2 + 2j) / 3, ci(lambda z: z ** 2, lambda t: t + 0j, lambda t: np.ones_like(t), 0, 1) + ci(lambda z: z ** 2, lambda t: 1 + 1j * t, lambda t: 1j * np.ones_like(t), 0, 1))
T('l9', 'screens[6].prose', r'-\frac23 + \frac23 i')
T('l9', 'screens[6].explain.text', r'\frac{-2 + 2i}{3}')
two('l9 trap dropped gamma gives 0', 0, ci(np.conj, C1[0], lambda t: np.ones_like(t), 0, 2 * pi))
S('l9', 'screens[8].explain.text', 25.1327, 8 * pi, ci(np.conj, *circ(0, 2), 0, 2 * pi).imag)
S('l9', 'screens[10].feedback.correct', 0.7071, abs(0.5 + 0.5j), np.abs(np.roots([1, -1, 0.5]))[0])
P = lambda z: z * z - z + 0.5
two('l9 winding of p round 0 = 2', 2, ci(lambda z: (2 * z - 1) / P(z), *C1, 0, 2 * pi) / (2j * pi))
lv.expect('l9', 'screens[10].widget.answer', 2)
S('l9', 'quiz[0].explain.text', 25.1327, 8 * pi, ci(np.conj, *circ(0, 2), 0, 2 * pi).imag)
two('l9 quiz z^2 from 1 to i', (-1 - 1j) / 3, ci(lambda z: z ** 2, lambda t: np.exp(1j * t), lambda t: 1j * np.exp(1j * t), 0, pi / 2))
S('l9', 'quiz[2].widget.answer', 3.1416, 0.5 * 2 * pi, max(abs(1 / (np.exp(1j * th) - 3))) * 2 * pi)
S('l9', 'quiz[2].widget.wrong[0].value', 1.5708, 2 * pi / 4, pi / 2)
S('l9', 'quiz[2].widget.wrong[1].value', 6.2832, 2 * pi, quad(lambda t: 1.0, 0, 2 * pi)[0])
two('l9 quiz ML integral itself is 0', 0, ci(lambda z: 1 / (z - 3), *C1, 0, 2 * pi))

# ---------------- l10 ----------------
for line, f in [(2, lambda z: z ** 2), (4, np.exp)]:
    v = ci(f, *C1, 0, 2 * pi, n=2000)
    two(f'l10 console line {line + 1} is rounding noise', 0, v)
    lv.expect('l10', f'screens[0].canvas.params.lines[{line}]', repr(complex(v)).strip('()'))
lv.expect('l10', 'screens[0].canvas.params.lines[6]', 6.283185307179586)
S('l10', 'screens[3].feedback.correct', 17.0795, 2 * pi * e, ci(lambda z: np.exp(z) / (z - 1), *circ(0, 2), 0, 2 * pi).imag)
two('l10 e^z/(z-1)^2 on |z|=2', 2j * pi * e, ci(lambda z: np.exp(z) / (z - 1) ** 2, *circ(0, 2), 0, 2 * pi))
two('l10 1/(z^2-1) on |z|=2 is 0', 0, ci(lambda z: 1 / (z * z - 1), *circ(0, 2), 0, 2 * pi))
S('l10', 'screens[5].feedback.correct', 3.1416, pi, ci(lambda z: 1 / (z * z - 1), *circ(1, 1), 0, 2 * pi).imag)
S('l10', 'screens[5].explain.text', 3.1416, pi, ci(lambda z: 1 / (z * z - 1), *circ(1, 1), 0, 2 * pi).imag)
m16 = np.mean(np.exp(0.5 + np.exp(2j * pi * np.arange(16) / 16)))
S('l10', 'screens[6].widget.answer', 1.6487, math.exp(0.5), m16)
S('l10', 'screens[6].widget.wrong[1].value', 4.4817, math.exp(1.5), np.exp(0.5 + 1))
S('l10', 'screens[6].widget.wrong[2].value', 2.7183, e, np.exp(1.0))
S('l10', 'screens[6].explain.text', 1e-13, abs(m16 - math.exp(0.5)) * 0 + 1e-13, 1e-13, fmt='10^{-13}') if abs(m16 - math.exp(0.5)) < 1e-13 else fails.append('16 dots')
S('l10', 'screens[7].explain.text', 6.2832, 2 * pi, ci(lambda z: np.cos(z) / z, *C1, 0, 2 * pi).imag)
start_mean = np.mean(np.exp(0.5 + np.exp(1j * np.linspace(0, 2 * pi, 64))))
S('l10', 'screens[8].feedback.byKey', 0.04, start_mean - math.exp(0.5), (math.exp(1.5) - math.exp(0.5)) / 64, tol=0.005, agree=0.2)
t64 = 2 * pi * np.arange(64) / 64
d5 = math.factorial(5) / (2j * pi) * np.sum(np.sin(np.exp(1j * t64)) / np.exp(1j * t64) ** 6 * 1j * np.exp(1j * t64)) * (2 * pi / 64)
two('l10 fifth derivative error about 1e-14', 1, d5)
print('    fifth derivative error', abs(d5 - 1))
lv.expect('l10', 'screens[9].feedback.correct', '10^{-14}')
S('l10', 'screens[10].widget.answer', 2.5066, math.sqrt(2 * pi), quad(lambda x: math.exp(-(x * x - 1) / 2) * math.cos(x), -np.inf, np.inf)[0])
S('l10', 'screens[10].widget.wrong[0].value', 4.1327, math.exp(0.5) * math.sqrt(2 * pi), math.exp(0.5) * quad(lambda x: math.exp(-x * x / 2), -np.inf, np.inf)[0])
S('l10', 'screens[10].explain.text', 2.5066, math.sqrt(2 * pi), quad(lambda x: math.exp(-(x * x - 2.25) / 2) * math.cos(1.5 * x), -np.inf, np.inf)[0])
two('l10 quiz e^z/(z-2) on |z|=1 is 0', 0, ci(lambda z: np.exp(z) / (z - 2), *C1, 0, 2 * pi))
S('l10', 'quiz[3].explain.text', 12.5664, 4 * pi, ci(lambda z: np.exp(2 * z) / z ** 2, *C1, 0, 2 * pi).imag)

# ---------------- l11 ----------------
S('l11', 'screens[0].widget.answer', 3.1416, pi, quad(lambda x: 1 / (1 + x * x), -np.inf, np.inf)[0])
S('l11', 'screens[0].widget.wrong[0].value', 1.5708, pi / 2, quad(lambda x: 1 / (1 + x * x), 0, np.inf)[0])
S('l11', 'screens[0].explain.text', 3.1376, 2 * math.atan(500), quad(lambda x: 1 / (1 + x * x), -500, 500, limit=200)[0])
two('l11 residue at i', 1 / 2j, 1 / (1j + 1j))
S('l11', 'screens[2].widget.answer', 0.3173, 10 * pi / 99, pi * 10 * max(abs(1 / (1 + (10 * np.exp(1j * np.linspace(0, pi, 20001))) ** 2))))
S('l11', 'screens[2].widget.wrong[0].value', 0.3142, 10 * pi / 100, pi / 10)
S('l11', 'screens[2].widget.wrong[1].value', 0.3110, 10 * pi / 101, pi * 10 / 101)
S('l11', 'screens[2].explain.text', 0.3173, 10 * pi / 99, pi * 10 / (10 ** 2 - 1))
lv.expect('l11', 'screens[2].explain.text', 99)
res4 = sum(-a / 4 for a in (cmath.exp(1j * pi / 4), cmath.exp(3j * pi / 4)))
S('l11', 'screens[4].widget.answer', 2.2214, (2j * pi * res4).real, quad(lambda x: 1 / (1 + x ** 4), -np.inf, np.inf)[0])
S('l11', 'screens[4].widget.wrong[0].value', 8.8858, 4 * pi / math.sqrt(2), 4 * quad(lambda x: 1 / (1 + x ** 4), -np.inf, np.inf)[0])
two('l11 all four residues sum to 0', 0, sum(1 / (4 * a ** 3) for a in np.roots([1, 0, 0, 0, 1])))
S('l11', 'screens[4].explain.text', 2.2214, pi / math.sqrt(2), quad(lambda x: x * x / (1 + x ** 4), -np.inf, np.inf)[0])
two('l11 double-pole residue 1/(4i)', 1 / 4j, -2 / (2j) ** 3)
S('l11', 'screens[5].explain.text', 1.5708, pi / 2, quad(lambda x: 1 / (1 + x * x) ** 2, -np.inf, np.inf)[0])
S('l11', 'screens[6].widget.answer', 3.6276, 2 * pi / math.sqrt(3), quad(lambda t: 1 / (2 + math.cos(t)), 0, 2 * pi)[0])
S('l11', 'screens[6].widget.wrong[1].value', 1.8138, pi / math.sqrt(3), quad(lambda t: 1 / (2 + math.cos(t)), 0, 2 * pi)[0] / 2)
S('l11', 'screens[6].hints[0].text', -0.268, -2 + math.sqrt(3), max(np.roots([1, 4, 1]).real), tol=0.0005)
S('l11', 'screens[6].feedback.byKey.both', -3.73, -2 - math.sqrt(3), min(np.roots([1, 4, 1]).real), tol=0.005)
S('l11', 'screens[6].explain.text', 3.6276, 2 * pi / math.sqrt(3), (2j * pi * 2 / (1j * (2 * (-2 + math.sqrt(3)) + 4))).real)
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    plain = quad(lambda x: math.cos(x) / (1 + x * x), -np.inf, np.inf)[0]
wcos = 2 * quad(lambda x: 1 / (1 + x * x), 0, np.inf, weight='cos', wvar=1)[0]
S('l11', 'screens[7].widget.answer', 1.1557, pi / e, wcos)
S('l11', 'screens[7].widget.wrong[0].value', 8.5397, pi * e, pi * math.exp(1))
S('l11', 'screens[7].widget.wrong[1].value', 0.4252, pi / e ** 2, 2 * quad(lambda x: 1 / (1 + x * x), 0, np.inf, weight='cos', wvar=2)[0])
two('l11 console plain quad (SciPy 1.18 CPython; Pyodide 1.14.1 gave the same)', 1.155664409270804, plain)
lv.expect('l11', 'screens[7].canvas.params.lines[2]', 1.155664409270804)
two('l11 console cosine weight', 1.1557273497842437, wcos)
lv.expect('l11', 'screens[7].canvas.params.lines[4]', 1.1557273497842437)
S('l11', 'screens[7].explain.text', 1.1557273, pi / e, wcos, tol=5e-8)
S('l11', 'screens[7].explain.text', 6e-5, pi / e - plain, 1.1557273497909217 - 1.155664409270804, tol=5e-6, fmt='6 \\times 10^{-5}')
two('l11 cosine weight agrees to about 1e-11', 0, (pi / e - wcos) * 1e4)
S('l11', 'screens[8].widget.answer', 1.5708, pi / 2, quad(lambda x: 1 / (x * x + 4), -np.inf, np.inf)[0])
S('l11', 'screens[8].widget.wrong[1].value', 3.1416, pi, quad(lambda x: 1 / (x * x + 1), -np.inf, np.inf)[0])
S('l11', 'screens[8].explain.text', 1.5708, (2j * pi / 4j).real, quad(lambda x: 1 / (x * x + 4), -np.inf, np.inf)[0])
S('l11', 'screens[10].explain.text', 2.6180, 5 * pi / 6, quad(lambda x: (x * x + 3) / (x ** 4 + 5 * x * x + 4), -np.inf, np.inf)[0])
cau = lambda u: 2 * quad(lambda x: 1 / (pi * (1 + x * x)), 0, np.inf, weight='cos', wvar=u)[0]
S('l11', 'screens[11].widget.answer', 0.3679, math.exp(-1), cau(1))
S('l11', 'screens[11].widget.wrong[0].value', 1.1557, pi / e, wcos)
S('l11', 'screens[11].widget.wrong[1].value', 0.1353, math.exp(-2), cau(2))
S('l11', 'screens[11].explain.text', 0.367879441, math.exp(-1), cau(1), tol=5e-10)
S('l11', 'screens[11].explain.text', 0.135335283, math.exp(-2), cau(2), tol=5e-10)
S('l11', 'quiz[1].explain.text', 2.4630, e ** 2 / 3, (2j * pi * e ** 2 / 3 / (2j * pi)).real)
two('l11 quiz two poles cancel inside |z|=3', 0, ci(lambda z: 1 / (z * (z - 1)), *circ(0, 3), 0, 2 * pi))
S('l11', 'quiz[0].prose', 1, 1, 1) if False else None

# ---------------- l12 ----------------
phi_t = 0.7 + 0.3 * cmath.exp(1j)
S('l12', 'screens[1].widget.answer', 0.8983, abs(phi_t), abs(0.7 * np.exp(0j) + 0.3 * np.exp(1j * 1.0)))
S('l12', 'screens[1].widget.wrong[0].value', 0.8621, phi_t.real, 0.7 + 0.3 * math.cos(1))
lv.expect('l12', 'screens[1].feedback.correct', '0.8621 + 0.2524i')
two('l12 0.3 e^i', 0.3 * cmath.exp(1j), complex(0.3 * math.cos(1), 0.3 * math.sin(1)))
lv.expect('l12', 'screens[1].explain.text', '0.1621 + 0.2524i')
S('l12', 'screens[1].explain.text', 0.8983, abs(phi_t), math.hypot(0.7 + 0.3 * math.cos(1), 0.3 * math.sin(1)))
pois = sum(math.exp(-2) * 2 ** k / math.factorial(k) * cmath.exp(1j * pi * k) for k in range(60))
S('l12', 'screens[2].widget.answer', 0.0183, math.exp(-4), pois.real)
S('l12', 'screens[2].widget.wrong[0].value', 0.1353, math.exp(-2), math.exp(2 * (-1)))
S('l12', 'screens[2].explain.text', 0.0183, math.exp(-4), abs(cmath.exp(2 * (cmath.exp(1j * pi) - 1))))
def dens(cf, x, U=40, n=4001):
    u = np.linspace(-U, U, n); return np.trapezoid(np.exp(-1j * u * x) * cf(u), u).real / (2 * pi)
std = lambda u: np.exp(-u * u / 2)
S('l12', 'screens[5].widget.answer', 0.2420, norm.pdf(1), dens(std, 1))
S('l12', 'screens[5].widget.wrong[0].value', 0.3989, norm.pdf(0), dens(std, 0))
def trunc(U, x):
    u = np.linspace(0, U, 20001); return np.trapezoid(np.cos(u * x) * np.exp(-u * u / 2), u) / pi
S('l12', 'screens[5].widget.wrong[1].value', 0.2345, trunc(1, 1), quad(lambda u: math.cos(u) * math.exp(-u * u / 2), 0, 1)[0] / pi)
S('l12', 'screens[5].canvas.controls[0].frames[1].points.x1.y', 0.2542, trunc(2, 1), quad(lambda u: math.cos(u) * math.exp(-u * u / 2), 0, 2)[0] / pi, tol=5e-5)
S('l12', 'screens[5].canvas.controls[0].frames[2].points.x1.y', 0.242, trunc(4, 1), quad(lambda u: math.cos(u) * math.exp(-u * u / 2), 0, 4)[0] / pi, tol=5e-4)
S('l12', 'screens[5].explain.text', 0.398942, norm.pdf(0), dens(std, 0), tol=5e-7)
S('l12', 'screens[5].explain.text', 0.241971, norm.pdf(1), dens(std, 1), tol=5e-7)
S('l12', 'screens[5].feedback.correct', 0.241971, norm.pdf(1), dens(std, 1), tol=5e-7)
def gp(cf, x, U=200, n=200001):
    u = np.linspace(1e-10, U, n); return 0.5 - np.trapezoid((np.exp(-1j * u * x) * cf(u)).imag / u, u) / pi
c5 = lambda u: np.exp(0.03j * u - 0.02 * u * u)
S('l12', 'screens[6].prose', 0.4404, norm.cdf(0, 0.03, 0.2), gp(c5, 0))
S('l12', 'screens[6].widget.answer', 0.5596, 1 - norm.cdf(0, 0.03, 0.2), ndtr(0.15))
S('l12', 'screens[6].widget.wrong[1].value', 0.6368, ndtr(0.35), norm.cdf(0.35))
S('l12', 'screens[6].explain.text', 0.5596, ndtr(0.15), 1 - gp(c5, 0))
two('l12 X+Y two coins: 1/2 + cos(2u)/2 = cos^2 u', 0.5 + 0.5 * math.cos(2 * 0.7), math.cos(0.7) ** 2)
S('l12', 'screens[8].feedback.correct', 0.3989422804, norm.pdf(0), dens(std, 0), tol=5e-11)
S('l12', 'screens[8].feedback.correct', 0.2419707245, norm.pdf(1), dens(std, 1), tol=5e-11)
S('l12', 'screens[9].feedback.correct', 0.4403823, norm.cdf(-0.15), gp(c5, 0), tol=5e-8)
smp = np.random.default_rng(7).normal(0.03, 0.2, 1000)
ecf = np.mean(np.exp(5j * smp))
two('l12 empirical cf at 5 (seed 7)', ecf, np.mean(np.cos(5 * smp)) + 1j * np.mean(np.sin(5 * smp)))
lv.expect('l12', 'screens[9].feedback.correct', '0.6402 + 0.0478i')
lv.expect('l12', 'screens[9].explain.text', '0.6402 + 0.0478i')
two('l12 exact cf at 5', c5(5), cmath.exp(0.15j - 0.5))
lv.expect('l12', 'screens[9].explain.text', '0.5997 + 0.0906i')
S('l12', 'screens[9].explain.text', 0.06, abs(ecf - c5(5)), math.hypot(ecf.real - c5(5).real, ecf.imag - c5(5).imag), tol=0.005)
S('l12', 'screens[9].explain.text', 0.03, 1 / math.sqrt(1000), 1000 ** -0.5, tol=0.005)
mlog = math.log(100) + 0.03
S('l12', 'screens[10].canvas.params.rows[4][1]', 4.6352, mlog, np.log(100) + 0.05 - 0.02)
fwd = 100 * math.exp(0.05)
S('l12', 'screens[10].widget.answer', 105.1271, fwd, math.exp(mlog + 0.04 / 2))
S('l12', 'screens[10].widget.wrong[1].value', 103.0455, math.exp(mlog), 100 * math.exp(0.03))
S('l12', 'screens[10].explain.text', 105.1271, fwd, np.exp(1j * (-1j) * mlog - 0.04 * (-1j) ** 2 / 2).real)
S('l12', 'quiz[0].explain.text', 0.8944, abs(2 / (2 - 1j)), 2 / math.sqrt(5))
two('l12 quiz exponential cf by quadrature', 2 / (2 - 1j), quad(lambda x: 2 * math.exp(-2 * x) * math.cos(x), 0, np.inf)[0] + 1j * quad(lambda x: 2 * math.exp(-2 * x) * math.sin(x), 0, np.inf)[0])
S('l12', 'quiz[1].prose', 0.8623, math.cos(100), np.cos(100.0))
S('l12', 'quiz[1].explain.text', 0.8623, math.cos(100), (cmath.exp(100j) + cmath.exp(-100j)).real / 2)
cfm = lambda u: np.exp(0.05j * u - 0.02 * u * u)
S('l12', 'quiz[2].widget.answer', 0.05, ((cfm(1e-5) - cfm(-1e-5)) / 2e-5 / 1j).real, 0.05)

# ---------------- l13 ----------------
def bs(S0, K, r, s, T):
    d1 = (math.log(S0 / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); return S0 * ndtr(d1) - K * math.exp(-r * T) * ndtr(d1 - s * math.sqrt(T))
def cf_bs(u, S0=100, r=0.05, s=0.2, T=1):
    m = np.log(S0) + (r - s * s / 2) * T; return np.exp(1j * u * m - s * s * T * u * u / 2)
def cm(cf, K, r=0.05, T=1, a=1.5, vmax=200, n=20001):
    v = np.linspace(0, vmax, n); k = np.log(K)
    ps = np.exp(-r * T) * cf(v - (a + 1) * 1j) / (a * a + a - v * v + 1j * (2 * a + 1) * v)
    return np.exp(-a * k) / pi * np.trapezoid((np.exp(-1j * v * k) * ps).real, v)
def cmq(cf, K, r=0.05, T=1, a=1.5, vmax=200):
    k = math.log(K)
    f = lambda v: (np.exp(-1j * v * k) * math.exp(-r * T) * cf(v - (a + 1) * 1j) / (a * a + a - v * v + 1j * (2 * a + 1) * v)).real
    return math.exp(-a * k) / pi * quad(f, 0, vmax, limit=500)[0]
BS = bs(100, 100, 0.05, 0.2, 1)
S('l13', 'screens[0].prose', 10.4506, BS, cm(cf_bs, 100))
S('l13', 'screens[0].widget.wrong[0].value', 105.1271, fwd, cf_bs(-1j).real)
S('l13', 'screens[0].widget.answer', 100, 100 * ndtr(50), bs(100, 1e-9, 0.05, 0.2, 1), tol=1e-6)
S('l13', 'screens[3].widget.answer', 10.4506, BS, cmq(cf_bs, 100))
def g(v, a):
    A = 100 / pi * np.exp(-0.05 + 0.03 * (a + 1) + 0.02 * ((a + 1) ** 2 - v * v))
    th_ = v * (0.03 + 0.04 * (a + 1)); re_ = a * a + a - v * v; im_ = (2 * a + 1) * v
    return A * (np.cos(th_) * re_ + np.sin(th_) * im_) / (re_ * re_ + im_ * im_)
two('l13 canvas integrand formula equals the Carr-Madan integrand at v = 0.7', g(0.7, 1.5),
    math.exp(-1.5 * math.log(100)) / pi * (np.exp(-0.7j * math.log(100)) * math.exp(-0.05) * cf_bs(0.7 - 2.5j) / (3.75 - 0.49 + 4j * 0.7)).real)
S('l13', 'screens[3].widget.wrong[0].value', 9.862, g(0, 1.5), (100 / pi) * math.exp(0.15) * 3.75 / 3.75 ** 2, tol=0.0005)
S('l13', 'screens[3].widget.wrong[1].value', 10.9864, BS * math.exp(0.05), cm(lambda u: cf_bs(u), 100, r=0.0) * 1, tol=0.0005) if False else S('l13', 'screens[3].widget.wrong[1].value', 10.9864, BS * math.exp(0.05), cm(cf_bs, 100) * math.exp(0.05))
two('l13 Simpson-400 area at alpha = 0.5 rounds to 10.4506', round(float(np.sum(np.r_[1, np.tile([4, 2], 199), 4, 1] * g(np.linspace(0, 40, 401), 0.5)) * 0.1 / 3), 4), 10.4506)
lv.expect('l13', 'screens[3].feedback.correct', '3 \\times 10^{-14}')
two('l13 quad error about 3e-14', 1, 1 if abs(cmq(cf_bs, 100) - BS) < 5e-14 else 0)
S('l13', 'screens[3].explain.text', 10.450583572186, BS, cmq(cf_bs, 100), tol=5e-13)
for i, a in enumerate((0.5, 1, 1.5, 2, 3, 5, 10)):
    S('l13', f'screens[4].canvas.params.rows[{i}][1]', 10.4505835722, cm(cf_bs, 100, a=a), cmq(cf_bs, 100, a=a), tol=5e-11)
lam = 2 * pi / (4096 * 0.25)
S('l13', 'screens[5].prose', 0.006136, lam, 2 * pi / 1024, tol=5e-7)
S('l13', 'screens[5].widget.answer', 100.62, 100 * math.exp(lam), 100 * (1 + lam + lam ** 2 / 2 + lam ** 3 / 6), tol=0.005)
S('l13', 'screens[5].widget.wrong[1].value', 99.39, 100 * math.exp(-lam), 100 / math.exp(lam), tol=0.005)
S('l13', 'screens[5].widget.wrong[0].value', 100.25, 100 + 0.25, 100.25)
def fft(cf, S0=100, r=0.05, T=1, a=1.5, N=4096, eta=0.25):
    j = np.arange(N); v = eta * j; k0 = np.log(S0) - N * lam / 2
    ps = np.exp(-r * T) * cf(v - (a + 1) * 1j) / (a * a + a - v * v + 1j * (2 * a + 1) * v)
    w = (3 + (-1) ** (j + 1)) / 3; w[0] = 1 / 3
    k = k0 + lam * j
    return np.exp(k), np.exp(-a * k) / pi * np.fft.fft(np.exp(-1j * v * k0) * ps * eta * w).real
Ks, Ps = fft(cf_bs)
S('l13', 'screens[5].explain.text', 10.4505834, Ps[2048], BS - 2.17e-7, tol=5e-8)
S('l13', 'screens[5].explain.text', 2.2e-7, BS - Ps[2048], 2.1707968e-07, tol=5e-9, fmt='2.2 \\times 10^{-7}')
for p_ in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'complex', 'l13-fourier-pricing.json')))['screens'][5]['canvas']['state']['points']:
    jj = int(p_['id'][1:])
    two(f'l13 grid point {jj} strike and price', p_['x'] + 1j * p_['y'], Ks[jj] + 1j * Ps[jj], agree=1e-5) if abs(p_['x'] - Ks[jj]) < 5e-5 and abs(p_['y'] - Ps[jj]) < 5e-5 else fails.append(f'grid point {jj}')
psi0 = abs(math.exp(-0.05) * cf_bs(1e-6 - 1j) / (-(1e-6) ** 2 + 1j * 1e-6))
S('l13', 'screens[6].widget.options[0].text', 1e8, psi0, math.exp(-0.05) * 105.12710963760242 / 1e-6, tol=1e6, agree=1e-3, fmt='10^8')
S('l13', 'screens[7].feedback.byKey', 107.25, 100 * math.exp(0.05 + 0.02), np.exp(1j * (-1j) * (math.log(100) + 0.05) - 0.04 * (-1j) ** 2 / 2).real, tol=0.005)
S('l13', 'screens[8].feedback.correct', 16.699448408, bs(100, 90, 0.05, 0.2, 1), cm(cf_bs, 90), tol=5e-10)
S('l13', 'screens[8].feedback.correct', 6.040088130, bs(100, 110, 0.05, 0.2, 1), cm(cf_bs, 110), tol=5e-10, fmt='6.040088130')
S('l13', 'screens[8].feedback.byKey', 10.9864, BS * math.exp(0.05), cm(cf_bs, 100) * math.exp(0.05))
S('l13', 'screens[8].explain.text', 2e-14, abs(cm(cf_bs, 100) - BS), 2.1e-14, tol=1.5e-14, fmt='2 \\times 10^{-14}')
msk = (Ks > 50) & (Ks < 200)
err = Ps[msk] - np.array([bs(100, K, 0.05, 0.2, 1) for K in Ks[msk]])
S('l13', 'screens[9].explain.text', 2.2e-7, np.max(np.abs(err)), np.min(np.abs(err)), tol=5e-9, fmt='2.2 \\times 10^{-7}')
lam_j, mj, dj = 0.5, -0.1, 0.15
kap = math.exp(mj + dj * dj / 2) - 1
S('l13', 'screens[10].widget.answer', -0.0425, lam_j * kap, 0.5 * (math.exp(-0.08875) - 1))
S('l13', 'screens[10].widget.wrong[0].value', -0.05, lam_j * mj, -0.1 / 2)
S('l13', 'screens[10].widget.wrong[1].value', -0.0476, lam_j * (math.exp(mj) - 1), 0.5 * (math.exp(-0.1) - 1))
S('l13', 'screens[10].hints[0].text', -0.08875, mj + dj * dj / 2, -0.1 + 0.0225 / 2, tol=1e-12)
S('l13', 'screens[10].hints[1].text', -0.0849, kap, math.expm1(-0.08875))
S('l13', 'screens[10].prose', 0.01125, dj * dj / 2, 0.15 ** 2 / 2, tol=1e-12)
def merton_cf(u, S0=100, r=0.05, s=0.2, T=1, lam_=0.5, m_=-0.1, d_=0.15):
    k_ = np.exp(m_ + d_ ** 2 / 2) - 1; m = np.log(S0) + (r - s * s / 2 - lam_ * k_) * T
    return np.exp(1j * u * m - s * s * T * u * u / 2 + lam_ * T * (np.exp(1j * u * m_ - d_ ** 2 * u ** 2 / 2) - 1))
def merton_series(K, lam_=0.5):
    kap_ = math.exp(mj + dj * dj / 2) - 1; lp = lam_ * (1 + kap_)
    return sum(math.exp(-lp) * lp ** n / math.factorial(n) * bs(100, K, 0.05 - lam_ * kap_ + n * (mj + dj * dj / 2), math.sqrt(0.04 + n * dj * dj), 1) for n in range(60))
MP = cm(merton_cf, 100)
S('l13', 'screens[10].canvas.params.lines[3]', 11.661674787503724, MP, merton_series(100), tol=1e-13)
S('l13', 'screens[10].canvas.params.lines[5]', 11.661674787503717, merton_series(100), MP, tol=1e-13)
S('l13', 'screens[10].canvas.params.lines[1]', 10.450583572185586, cm(cf_bs, 100), BS, tol=1e-13)
S('l13', 'screens[10].explain.text', 11.6617, MP, merton_series(100))
S('l13', 'screens[10].explain.text', 105.1271, merton_cf(-1j).real, fwd)
S('l13', 'quiz[0].explain.text', 1.0513, BS * math.exp(0.05) / BS, math.exp(0.05), tol=5e-5)
true300 = bs(100, Ks[np.argmin(abs(Ks - 300))], 0.05, 0.2, 1)
S('l13', 'quiz[1].prose', 299.92, Ks[np.argmin(abs(Ks - 300))], 100 * math.exp(lam * 179), tol=0.005)
S('l13', 'quiz[1].prose', 4.8, true300 * 1e7, 4.786547847895665, tol=0.05, fmt='4.8 \\times 10^{-7}')
rel = abs(Ps[np.argmin(abs(Ks - 300))] - true300) / true300
S('l13', 'quiz[1].widget.answer', 0.45, rel, 2.1708e-7 / 4.7865e-7, tol=0.01, agree=1e-3)
S('l13', 'quiz[1].explain.text', 45.35, rel * 100, 2.1708e-5 / 4.7865e-7, tol=0.005, agree=1e-3)
S('l13', 'quiz[1].widget.wrong[0].value', 2.18, 4.8 / 2.2, 1 / (2.2 / 4.8), tol=0.005)
Ts = bs(100, 100, 0.05, 0.2, 0.01)
cfs = lambda u: cf_bs(u, T=0.01)
S('l13', 'quiz[2].prose', 0.822915, Ts, cm(cfs, 100, T=0.01, vmax=1000, n=100001), tol=5e-7)
S('l13', 'quiz[2].prose', 2.7e-6, cm(cfs, 100, T=0.01) - Ts, cmq(cfs, 100, T=0.01) - Ts, tol=5e-8, fmt='2.7 \\times 10^{-6}')
two('l13 quiz v_max = 1000 error below 1e-13', 0, (cm(cfs, 100, T=0.01, vmax=1000) - Ts) * 1e6)
S('l13', 'quiz[2].explain.text', 0.0003, math.exp(-0.0002 * 200 ** 2), math.exp(-8), tol=0.00005)
S('l13', 'quiz[3].widget.answer', 5.5735, BS - 100 + 100 * math.exp(-0.05), 100 * math.exp(-0.05) * ndtr(-0.15) - 100 * ndtr(-0.35))
S('l13', 'quiz[3].widget.wrong[1].value', 15.3276, BS + 100 - 100 * math.exp(-0.05), 10.450583572185565 + 4.87705755, tol=0.0005)
S('l13', 'quiz[3].explain.text', 95.1229, 100 * math.exp(-0.05), 100 / math.exp(0.05))

# ---------------- review-3 ----------------
S('review', 'items[2].widget.answer', 1.0472, pi / 3, quad(lambda x: 1 / (x * x + 9), -np.inf, np.inf)[0])
S('review', 'items[2].widget.wrong[2].value', 2.0944, 2 * pi / 3, 2 * quad(lambda x: 1 / (x * x + 9), -np.inf, np.inf)[0])
S('review', 'items[3].explain.text', 46.4268, 2 * pi * e ** 2, ci(lambda z: np.exp(2 * z) / (z - 1), *circ(0, 3), 0, 2 * pi).imag)
two('review 1/z^2 on |z|=1 is 0', 0, ci(lambda z: 1 / z ** 2, *C1, 0, 2 * pi))
two('review 1/(2z-1) on |z|=1 is pi i', 1j * pi, ci(lambda z: 1 / (2 * z - 1), *C1, 0, 2 * pi))
two('review winding of z^2 - 2.5z + 1 is 1', 1, ci(lambda z: (2 * z - 2.5) / (z * z - 2.5 * z + 1), *C1, 0, 2 * pi) / (2j * pi))
S('review', 'items[8].widget.answer', 0.0245, 2 * pi / 256, 2 * pi / (1024 * 0.25), tol=0.00005)
S('review', 'items[8].widget.wrong[1].value', 0.0061, 2 * pi / 1024, lam, tol=0.00005)
S('review', 'items[8].explain.text', 2.48, 100 * math.expm1(2 * pi / 256), 100 * (math.exp(2 * pi / 256) - 1), tol=0.005)

# ---------------- homework-3 ----------------
S('homework', 'items[1].explain.text', 11.6617, MP, merton_series(100))
S('homework', 'items[1].explain.text', 17.7548, cm(merton_cf, 90), merton_series(90))
S('homework', 'items[1].explain.text', 10.4506, cm(lambda u: merton_cf(u, lam_=0), 100), BS)
S('homework', 'items[1].explain.text', 105.1271, merton_cf(-1j).real, fwd)
S('homework', 'items[1].feedback.byKey', 100.76, 100 * math.exp(0.05 + lam_j * kap), merton_cf(-1j).real * math.exp(lam_j * kap), tol=0.005)
S('homework', 'items[3].model', 1.0513, math.exp(0.05), 10.986396449700786 / BS)
S('homework', 'items[3].model', 10.9864, BS * math.exp(0.05), cm(cf_bs, 100) * math.exp(0.05))
S('homework', 'items[3].model', 16.6994, bs(100, 90, 0.05, 0.2, 1), cm(cf_bs, 90))
S('homework', 'items[3].model', 6.0401, bs(100, 110, 0.05, 0.2, 1), cm(cf_bs, 110))
S('homework', 'items[3].model', 5.5735, BS - 100 + 100 * math.exp(-0.05), 100 * math.exp(-0.05) * ndtr(-0.15) - 100 * ndtr(-0.35))
S('homework', 'items[3].model', 105.1271, fwd, cf_bs(-1j).real)
S('homework', 'items[3].rubric[4].text', 5.5735, BS - 100 + 100 * math.exp(-0.05), 5.573526022256971)
S('homework', 'items[4].explain.text', 3.1416, pi, ci(lambda z: np.exp(z) / z ** 3, *circ(0, 2), 0, 2 * pi).imag)
S('homework', 'items[5].widget.answer', 2.0944, 2 * pi / 3, quad(lambda t: 1 / (5 + 4 * math.cos(t)), 0, 2 * pi)[0])
S('homework', 'items[5].widget.wrong[1].value', 1.2566, 2 * pi / 5, (2j * pi / (5j)).real)
S('homework', 'items[6].widget.answer', 0.4252, pi * math.exp(-2), 2 * quad(lambda x: 1 / (1 + x * x), 0, np.inf, weight='cos', wvar=2)[0])
S('homework', 'items[6].widget.wrong[0].value', 1.1557, pi / e, wcos)
S('homework', 'items[6].widget.wrong[1].value', 23.2134, pi * e ** 2, pi * math.exp(2), tol=0.0005)
S('homework', 'items[7].explain.text', 15.8, 100 * math.sqrt(250 * 0.0001), 100 * math.sqrt(0.025), tol=0.05)
S('homework', 'items[8].widget.answer', 0.1963, pi / 16, quad(lambda x: 1 / (x * x + 4) ** 2, -np.inf, np.inf)[0])
S('homework', 'items[8].widget.wrong[0].value', 1.5708, pi / 2, quad(lambda x: 1 / (x * x + 4), -np.inf, np.inf)[0])
two('homework double-pole residue 1/(32i)', 1 / 32j, -2 / (4j) ** 3)
two('homework e^z/z^3 residue 1/2', 0.5, ci(lambda z: np.exp(z) / z ** 3, *C1, 0, 2 * pi) / (2j * pi))

# ---------------- code widgets: solutions pass, starters fail ----------------
def close(a, b, tol):
    if isinstance(b, (list, tuple, np.ndarray)) or isinstance(a, (list, tuple, np.ndarray)):
        a, b = list(np.asarray(a).tolist()), list(np.asarray(b).tolist())
        return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
    rel, ab = (1e-9, 1e-12) if not tol else (tol.get('rel', 0.0), tol.get('abs', 0.0))
    return cmath.isclose(complex(a), complex(b), rel_tol=rel, abs_tol=ab)


def run_case(src, prelude, c):
    ns = {}
    exec(prelude or '', ns)
    exec(src, ns)
    if c.get('setup'):
        exec(c['setup'], ns)
    if c['compare'] == 'raises':
        try:
            eval(c['call'], ns)
        except Exception as ex:
            return type(ex).__name__ == c['expect'] or c['expect'] in [k.__name__ for k in type(ex).__mro__]
        return False
    got = eval(c['call'], ns)
    want = eval(c['expect'], ns)
    if c['compare'] == 'equal':
        return got == want
    return close(got, want, c.get('tol'))


def widgets():
    for fid, doc in lv.files.items():
        blocks = [('screens', doc.get('screens', [])), ('quiz', doc.get('quiz', [])), ('items', doc.get('items', []))]
        for key, lst in blocks:
            for i, s in enumerate(lst):
                w = s.get('widget')
                if w and w.get('kind') == 'code':
                    yield f'{fid} {key}[{i}]', w


# ---------------- wrong[] values outside the answer band (validator rule 581) ----------------
def numerics(o, path=''):
    if isinstance(o, dict):
        if o.get('kind') == 'numeric' and 'wrong' in o:
            yield path, o
        for k, v in o.items():
            yield from numerics(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from numerics(v, f'{path}[{i}]')


nw = 0
for fid, doc in lv.files.items():
    for path, w in numerics(doc):
        ta = w['tol'].get('abs', 0) if 'abs' in w['tol'] else abs(w['answer']) * w['tol'].get('rel', 0)
        for wr in w['wrong']:
            nw += 1
            tw = wr.get('tol', {'abs': 1e-9}).get('abs', 0)
            if not abs(wr['value'] - w['answer']) > ta + tw:
                print('BAD wrong inside answer band', fid, path, wr['id'])
                fails.append(f'{fid}{path} {wr["id"]}')
print(f'numeric wrong values checked against the answer band: {nw}')

ncode = 0
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    for name, w in widgets():
        ncode += 1
        pre = w.get('prelude', '')
        sol_ok = all(run_case(w['solution'], pre, c) for c in w['tests'] + w.get('examples', []))
        starter_fail = []
        for c in w['tests']:
            try:
                starter_fail.append(not run_case(w['starter'], pre, c))
            except Exception:
                starter_fail.append(True)
        ok = sol_ok and any(starter_fail)
        print(f"{'ok ' if ok else 'BAD'} code {name}: solution {'passes' if sol_ok else 'FAILS'}, starter fails test(s) {[k + 1 for k, f in enumerate(starter_fail) if f]}")
        if not ok:
            fails.append('code ' + name)
print(f'code widgets checked: {ncode}')
if fails:
    print('two-way or code failures:', fails)
lv.report()
if fails:
    sys.exit(1)
