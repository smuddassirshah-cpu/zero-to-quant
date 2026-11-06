"""Recompute every number stated in convex level 4 (Algorithms) by two routes, and check each at its JSON path.
Run: python3 docs/reports/convex-L4-numbers.py   (needs numpy and scipy; exits 0 when every check passes)
Route 1 is a closed form or exact arithmetic (fractions, eigenvalue formulas, rate formulas); route 2 runs the algorithm
itself (descent, Newton, backtracking, SLSQP, HiGHS, numpy.linalg). `two(a, b)` asserts the routes agree; `rnd` checks
that an exact value rounds to the figure shown; `E` checks the shown figure appears at its JSON path. The script also
checks that no numeric `wrong` value lies inside the answer's band (validator rule 581 on main), and runs every code
widget of the level in CPython: each solution passes its hidden tests and each starter fails every one.
"""
import sys, os, math
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog, minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("convex", 4)
fails = []
def E(f, path, *vals, fmt=None):
    for v in vals:
        if isinstance(v, F):
            n, d = abs(v.numerator), v.denominator
            forms = [f'frac{{{n}}}{{{d}}}'] + ([f'frac{n}{d}'] if n < 10 and d < 10 else [])
            txt = lv.text(f, path)
            ok = any(x in txt for x in forms)
            lv._rec(ok, f'{f} {path} = {v}', '' if ok else 'fraction not found')
        else:
            lv.expect(f, path, v, fmt=fmt)
def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')
def rnd(name, exact, shown, places):
    if abs(float(exact) - shown) > 0.51 * 10 ** -places:
        fails.append(f'{name}: {exact!r} does not round to {shown}')
def C(f, path, exact, shown, places):
    """exact value, figure shown to `places` decimals, checked at path"""
    rnd(f'{f} {path}', exact, shown, places); E(f, path, shown)

LN6 = math.log(1e6)
def count(rho, eps=1e-6):
    return 1 if rho <= 0 else math.ceil(math.log(1 / eps) / math.log(1 / rho))
def sim_count(lams, s, x0, eps=1e-6):
    x = np.array(x0, float); lam = np.array(lams, float); e0 = np.linalg.norm(x); n = 0
    while np.linalg.norm(x) > eps * e0:
        x = x - s * lam * x; n += 1
    return n
def gd(grad, x0, s, n):
    x = np.array(x0, float)
    for _ in range(n): x = x - s * np.asarray(grad(x), float)
    return x

# ================= l14 =================
H1 = np.diag([1.0, 10.0])
E('l14', 'screens[0].prose', 10, 1)
two('limit bowl', 2 / np.linalg.eigvalsh(H1).max(), 0.2); two('y factor at 0.2', 1 - 10 * 0.2, -1)
E('l14', 'screens[0].widget.answer', 0.2)
two('multivar limit', 2 / np.linalg.eigvalsh(np.diag([2.0, 4.0])).max(), 0.5)
E('l14', 'screens[0].widget.wrong[0].value', 0.5); E('l14', 'screens[0].widget.wrong[1].value', 0.1)
E('l14', 'screens[0].feedback.byKey.multivar', 0.5); E('l14', 'screens[0].hints[2].text', 0.2)
E('l14', 'screens[0].explain.text', 0.2)
# s = 0.21
two('factor 0.21', 1 - 10 * 0.21, -1.1)
y10 = gd(lambda x: H1 @ x, [10, 1], 0.21, 10)[1]; two('1.1^10', 1.1 ** 10, y10)
C('l14', 'screens[1].widget.answer', y10, 2.5937, 4); E('l14', 'screens[1].prose', 0.21, -1.1)
E('l14', 'screens[1].widget.wrong[0].value', 1.1); E('l14', 'screens[1].widget.wrong[1].value', -2.5937)
E('l14', 'screens[1].explain.text', 2.5937); E('l14', 'screens[1].feedback.correct', 2.5937)
# generalise
two('lmax 4', np.linalg.eigvalsh(np.diag([2.0, 4.0])).max(), 4)
two('limit 0.5,8', 2 / 8, 0.25); E('l14', 'screens[2].widget.answer', 0.25)
E('l14', 'screens[2].widget.wrong[0].value', 4); E('l14', 'screens[2].widget.wrong[1].value', 0.125)
C('l14', 'screens[2].widget.wrong[2].value', 2 / 8.5, 0.2353, 4)
two('0.875', 1 - 0.5 * 0.25, 0.875); E('l14', 'screens[2].explain.text', 0.25, 0.875)
# s = 0.1
x10 = gd(lambda x: H1 @ x, [10, 1], 0.1, 10)
two('x10 at 0.1', x10[0], 10 * 0.9 ** 10); two('y10 at 0.1', x10[1], 0)
C('l14', 'screens[3].widget.answer', x10[0], 3.4868, 4); E('l14', 'screens[3].prose', 0.1, 0.9)
E('l14', 'screens[3].widget.wrong[0].value', 9); E('l14', 'screens[3].explain.text', 3.4868)
rnd('0.9^10', 0.9 ** 10, 0.34868, 5); E('l14', 'screens[3].hints[2].text', 0.34868)
# best step
sb = 2 / (1 + 10); two('best step solve', sb, F(2, 11))
C('l14', 'screens[4].widget.answer', sb, 0.1818, 4); C('l14', 'screens[4].widget.wrong[2].value', 1 / 11, 0.0909, 4)
E('l14', 'screens[4].widget.wrong[0].value', 0.1); E('l14', 'screens[4].widget.wrong[1].value', 0.2)
xb = gd(lambda x: H1 @ x, [10, 1], sb, 10); two('xb', xb[0], 10 * (9 / 11) ** 10); two('yb', xb[1], (9 / 11) ** 10)
C('l14', 'screens[4].feedback.correct', xb[0], 1.3443, 4); C('l14', 'screens[4].feedback.correct', xb[1], 0.1344, 4)
two('factors', abs(1 - sb), abs(1 - 10 * sb)); two('9/11', 1 - sb, F(9, 11))
E('l14', 'screens[4].feedback.correct', F(9, 11)); E('l14', 'screens[4].explain.text', F(2, 11), F(9, 11))
# trap
two('0.25 factor', 1 - 10 * 0.25, -1.5); E('l14', 'screens[5].widget.options[1].why', 2.5, -1.5)
two('s=1 factor', 1 - 10 * 1, -9); y10s1 = gd(lambda x: H1 @ x, [10, 1], 1.0, 10)[1]; two('9^10', y10s1, 9 ** 10)
rnd('3.5e9', y10s1 / 1e9, 3.5, 1); E('l14', 'screens[5].widget.options[2].why', -9, 3.5)
E('l14', 'screens[5].explain.text', 0.2, F(2, 11)); E('l14', 'screens[5].feedback.correct', F(9, 11))
# edge
y11 = gd(lambda x: H1 @ x, [10, 1], 0.2, 11)[1]; two('y11', y11, -1)
E('l14', 'screens[6].widget.answer', -1); E('l14', 'screens[6].widget.wrong[0].value', 1); E('l14', 'screens[6].widget.wrong[1].value', 0)
# logistic curvature
w = np.linspace(-6, 6, 120001); fpp = np.exp(-w) / (1 + np.exp(-w)) ** 2
two('L = 1/4', fpp.max(), 0.25, 1e-8); two('argmax 0', w[fpp.argmax()], 0, 1e-6); E('l14', 'screens[7].prose', F(1, 4), 0)
E('l14', 'screens[7].feedback.correct', 8); E('l14', 'screens[7].explain.text', 8)
# Armijo threshold s <= 1/L: f(x - s g) <= f(x) - s(1 - L s / 2)|g|^2 and 1 - L/(2L) = 1/2
two('armijo 1/L', 1 - 0.5, 0.5)
# penalised portfolio
Sig = np.diag([0.04, 0.09, 0.16]); m = np.array([0.05, 0.08, 0.11]); H3 = 5 * Sig
two('H3', np.linalg.eigvalsh(H3).max(), 0.8); E('l14', 'screens[9].prose', 0.2, 0.45, 0.8)
two('limit 2.5', 2 / np.linalg.eigvalsh(H3).max(), 2.5); E('l14', 'screens[9].widget.answer', 2.5)
E('l14', 'screens[9].widget.wrong[0].value', 10); E('l14', 'screens[9].widget.wrong[1].value', 1.25); E('l14', 'screens[9].widget.wrong[2].value', 0.4)
wstar = m / (5 * np.diag(Sig)); wgd = gd(lambda v: H3 @ v - m, [0, 0, 0], 2.0, 60)
for i, sh in enumerate([0.25, 0.1778, 0.1375]):
    two(f'w* {i}', wstar[i], wgd[i]); rnd(f'w* {i}', wstar[i], sh, 4)
E('l14', 'screens[9].feedback.correct', 0.25, 0.1778, 0.1375, 2.5); E('l14', 'screens[9].explain.text', 0.8, 2.5, 0.25, 0.1778, 0.1375)
rnd('cash', (1 - wstar.sum()) * 100, 43.5, 1); E('l14', 'screens[9].explain.text', 43.5)
E('l14', 'screens[9].canvas.state.values.a2', 0.1778)
# ridge
R2 = np.array([[2.0, 1.0], [1.0, 2.0]]); ev = np.linalg.eigvalsh(R2); two('ridge eig lo', ev[0], 1); two('ridge eig hi', ev[1], 3)
E('l14', 'screens[11].prose', 0.5, 3, 1)
evr = np.linalg.eigvalsh(R2 + 2 * 0.5 * np.eye(2)); two('ridge 4', evr[1], 4); two('ridge 2', evr[0], 2)
two('ridge limit', 2 / evr[1], 0.5); E('l14', 'screens[11].widget.answer', 0.5)
C('l14', 'screens[11].widget.wrong[0].value', 2 / 3, 0.6667, 4); E('l14', 'screens[11].widget.wrong[1].value', 1); E('l14', 'screens[11].widget.wrong[2].value', 0.25)
E('l14', 'screens[11].feedback.correct', 4, 2, 0.5); E('l14', 'screens[11].explain.text', 0.5, F(2, 3), 3, 2)
# quiz
two('q1', 2 / 50, 0.04); E('l14', 'quiz[0].widget.answer', 0.04); E('l14', 'quiz[0].widget.wrong[0].value', 1); E('l14', 'quiz[0].widget.wrong[1].value', 0.02)
two('q2', 1 - 0.25 * 1, 0.75); E('l14', 'quiz[1].widget.answer', 0.75)
def armijo(f, g, x, s=1.0):
    tried = []
    while not f(x - s * g(x)) <= f(x) - 0.5 * s * g(x) ** 2:
        tried.append(s); s /= 2
    return s, tried
sa, tried = armijo(lambda x: 2 * x * x, lambda x: 4 * x, 1.0); two('armijo', sa, 0.25)
E('l14', 'quiz[2].widget.answer', 0.25); E('l14', 'quiz[2].widget.wrong[0].value', 1); E('l14', 'quiz[2].widget.wrong[1].value', 0.5)
two('f(-3)', 2 * 9, 18); two('rhs1', 2 - 0.5 * 1 * 16, -6); two('rhs.5', 2 - 0.5 * 0.5 * 16, -2); two('rhs.25', 2 - 0.5 * 0.25 * 16, 0)
E('l14', 'quiz[2].explain.text', 18, -6, -1, 2, -2, 0.25)

# ================= l15 =================
c2, c100 = count(1 / 3), count(99 / 101)
two('13', c2, sim_count([1, 2], 2 / 3, [1, 1])); two('691', c100, sim_count([1, 100], 2 / 101, [1, 1]))
E('l15', 'screens[0].widget.answer', 691); E('l15', 'screens[0].widget.wrong[0].value', 13); E('l15', 'screens[0].widget.wrong[1].value', 690)
c100w = count(1 - 1 / 100); two('1375', c100w, sim_count([1, 100], 1 / 100, [1, 0])); E('l15', 'screens[0].widget.wrong[2].value', 1375)
rnd('690 err', (99 / 101) ** 690 * 1e6, 1.015, 3); E('l15', 'screens[0].feedback.byKey.early', 1.015)
if not (99 / 101) ** 691 < 1e-6 < (99 / 101) ** 690: fails.append('691 boundary')
E('l15', 'screens[0].feedback.correct', 691, 13); E('l15', 'screens[0].explain.text', 13, 691)
C('l15', 'screens[1].widget.answer', 99 / 101, 0.9802, 4); two('rho100 balance', 1 - 2 / 101, -(1 - 200 / 101))
E('l15', 'screens[1].widget.wrong[0].value', 0.99); C('l15', 'screens[1].widget.wrong[1].value', 2 / 101, 0.0198, 4)
E('l15', 'screens[1].explain.text', 0.9802, 691)
rnd('6.9', LN6 / 2, 6.9, 1); E('l15', 'screens[2].prose', 6.9)
c1000 = count(999 / 1001); two('6908 formula', c1000, 6908); rnd('6908 approx', 500 * LN6, 6908, 0)
E('l15', 'screens[2].widget.answer', 6908); E('l15', 'screens[2].widget.wrong[0].value', count(1 - 1 / 1000))
two('13809', count(1 - 1 / 1000), 13809); two('log10 slip', 1000 / 2 * 6, 3000); E('l15', 'screens[2].widget.wrong[1].value', 3000)
C('l15', 'screens[2].feedback.correct', LN6, 13.8155, 4); E('l15', 'screens[2].feedback.correct', 500)
E('l15', 'screens[3].explain.text', F(9, 11))
table = {2: (13, 20), 4: (28, 49), 10: (69, 132), 39: (270, 532), 100: (691, 1375)}
for k, (b, wv) in table.items():
    two(f'best {k}', count((k - 1) / (k + 1)), b); two(f'sim best {k}', sim_count([1, k], 2 / (1 + k), [1, 1]), b)
    two(f'1/lmax {k}', count(1 - 1 / k), wv); two(f'sim 1/lmax {k}', sim_count([1, k], 1 / k, [1, 0]), wv)
    E('l15', 'screens[4].widget.rows', b, wv)
E('l15', 'screens[4].widget.rows[2][1].wrong[0].value', 68); E('l15', 'screens[4].widget.rows[2][2].wrong[0].value', 131)
C('l15', 'screens[4].hints[1].text', math.log(11 / 9), 0.2007, 4); C('l15', 'screens[4].hints[1].text', math.log(10 / 9), 0.1054, 4)
C('l15', 'screens[4].hints[2].text', LN6 / math.log(11 / 9), 68.85, 2); C('l15', 'screens[4].hints[2].text', LN6 / math.log(10 / 9), 131.13, 2)
C('l15', 'screens[5].widget.answer', math.log(9 / 11), -0.2007, 4); C('l15', 'screens[5].widget.wrong[0].value', 9 / 11, 0.8182, 4)
C('l15', 'screens[5].widget.wrong[1].value', math.log10(9 / 11), -0.0872, 4)
C('l15', 'screens[5].hints[1].text', math.log(9), 2.1972, 4); C('l15', 'screens[5].hints[1].text', math.log(11), 2.3979, 4)
C('l15', 'screens[5].feedback.correct', -math.log(9 / 11) / math.log(10), 0.087, 3)
errs = [(9 / 11) ** k for k in range(30)]; two('fit slope', np.polyfit(range(30), np.log(errs), 1)[0], math.log(9 / 11))
S2 = 0.04 * np.array([[1, 0.95], [0.95, 1]]); e2 = np.linalg.eigvalsh(S2)
two('0.078', e2[1], 0.04 * 1.95); two('0.002', e2[0], 0.04 * 0.05); two('kappa 39', e2[1] / e2[0], 39)
E('l15', 'screens[6].widget.answer', 39); E('l15', 'screens[6].widget.wrong[0].value', 1); E('l15', 'screens[6].widget.wrong[1].value', 1.95)
E('l15', 'screens[6].explain.text', 1.95, 0.078, 0.05, 0.002, 39); E('l15', 'screens[6].prose', 0.95, 0.04)
two('slow dir', abs(np.linalg.eigh(S2)[1][:, 0] @ np.array([1, -1]) / math.sqrt(2)), 1)
two('kappa 4', 0.16 / 0.04, 4); E('l15', 'screens[7].prose', 4)
U = np.diag(1 / np.array([0.2, 0.4])) @ np.diag([0.04, 0.16]) @ np.diag(1 / np.array([0.2, 0.4])); two('rescaled', np.linalg.eigvalsh(U).max(), 1)
u1 = np.array([1, 0.8]) - 0.5 * (2 * np.eye(2) @ np.array([1, 0.8])); two('one step', np.linalg.norm(u1), 0)
E('l15', 'screens[7].widget.answer', 1); E('l15', 'screens[7].widget.wrong[0].value', 28); two('28', count(3 / 5), 28)
x = 1.0; fx = {}
for k in range(1, 1001):
    x = x - (1 / 12) * 4 * x ** 3
    if k in (10, 100, 1000): fx[k] = x ** 4
two('L=12', 12 * 1 ** 2, 12)
rnd('x4 10', fx[10], 0.01234, 5); rnd('x4 100', fx[100], 0.000204, 6); rnd('x4 1000', fx[1000] * 1e6, 2.2, 1)
E('l15', 'screens[8].canvas.params.rows', 0.01234, 0.000204, 2.2)
if not (fx[10] / fx[100] < 100 and fx[100] / fx[1000] < 100): fails.append('tenfold under hundredfold')
two('500000', 1 / (2 * 1e-6), 500000); E('l15', 'screens[8].widget.answer', 500000)
E('l15', 'screens[8].widget.wrong[0].value', 1000000); E('l15', 'screens[8].widget.wrong[1].value', 14); rnd('14', LN6, 14, 0)
c = 0.5 * 0.95; S2s = 0.5 * S2 + 0.5 * np.diag(np.diag(S2)); es = np.linalg.eigvalsh(S2s)
two('shrunk corr', S2s[0, 1] / 0.04, 0.475); ks = es[1] / es[0]; rnd('2.81', ks, 2.81, 2)
two('rho=c', (ks - 1) / (ks + 1), c); two('19', count(c), sim_count(es[::-1] if False else es, 2 / es.sum(), [1, 1]))
two('19 val', count(c), 19)
E('l15', 'screens[10].widget.answer', 19); E('l15', 'screens[10].widget.wrong[0].value', 270); E('l15', 'screens[10].widget.wrong[1].value', 18)
C('l15', 'screens[10].hints[2].text', LN6 / math.log(1 / c), 18.56, 2); C('l15', 'screens[10].explain.text', math.log(1 / c), 0.7444, 4)
E('l15', 'screens[10].hints[0].text', 2.81); E('l15', 'screens[10].prose', 0.95, 0.475)
two('q kappa', 20 / 0.5, 40); E('l15', 'quiz[0].widget.answer', 40); E('l15', 'quiz[0].widget.wrong[0].value', 0.025); E('l15', 'quiz[0].widget.wrong[1].value', 19.5)
two('q rho', 8 / 10, 0.8); E('l15', 'quiz[1].widget.answer', 0.8); C('l15', 'quiz[1].widget.wrong[0].value', 8 / 9, 0.8889, 4)
two('62', count(0.8), 62); C('l15', 'quiz[1].explain.text', math.log(1.25), 0.2231, 4); E('l15', 'quiz[1].explain.text', 62)
two('q kappa19', (1 + 0.9) / (1 - 0.9), 19); E('l15', 'quiz[2].widget.answer', 19); E('l15', 'quiz[2].widget.wrong[0].value', 10)
C('l15', 'quiz[2].widget.wrong[1].value', 1 / 0.9, 1.1111, 4)

# ================= l16 =================
xs = [F(1, 2)]
for _ in range(5): xs.append(2 * xs[-1] - xs[-1] ** 2)
xn = [0.5]
for _ in range(5): xn.append(xn[-1] - (1 - 1 / xn[-1]) / (1 / xn[-1] ** 2))
for a, b in zip(xs, xn): two('newton xlnx', a, b)
for k in range(5): two(f'err sq {k}', 1 - xs[k + 1], (1 - xs[k]) ** 2)
E('l16', 'screens[0].widget.answer', 0.9375); E('l16', 'screens[0].widget.wrong[0].value', 0.75); E('l16', 'screens[0].widget.wrong[1].value', 0.5)
E('l16', 'screens[0].feedback.correct', 0.75, 0.9375, F(1, 16)); E('l16', 'screens[0].explain.text', 0.75, 0.9375)
E('l16', 'screens[1].prose', 0.5, 0.75, 0.9375, F(255, 256), F(65535, 65536), 0.25, 0.0625, 0.00390625)
rnd('1.53e-5', float(1 - xs[4]) * 1e5, 1.53, 2); E('l16', 'screens[1].prose', 1.53); E('l16', 'screens[1].canvas.params.rows', 1.53)
rnd('x4', float(xs[4]), 0.999985, 6); E('l16', 'screens[1].canvas.params.rows', 0.999985, 0.99609375)
x = 0.5; n = 0
while abs(x - 1) > 1e-6: x = x - 0.25 * (1 - 1 / x); n += 1
two('descent 44', n, 44); E('l16', 'screens[3].prose', 44, 0.75); two('0.75 factor', 1 - 0.25 * 1, 0.75)
nn = next(k for k in range(10) if abs(1 - xs[k]) <= 1e-6); two('newton 5', nn, 5)
E('l16', 'screens[3].widget.answer', 5); E('l16', 'screens[3].widget.wrong[0].value', 4); E('l16', 'screens[3].widget.wrong[1].value', 44)
rnd('2.3e-10', float(1 - xs[5]) * 1e10, 2.3, 1); E('l16', 'screens[3].feedback.correct', 1.53, 2.3, 44)
two('28 kappa4', count((4 - 1) / 5), sim_count([0.2, 0.8], 2 / 1.0, [1, 1])); E('l16', 'screens[4].widget.answer', 28)
E('l16', 'screens[4].widget.wrong[0].value', 1); E('l16', 'screens[4].widget.wrong[1].value', 49); two('49', count(1 - 1 / 4), 49)
wn = np.zeros(3) - np.linalg.solve(H3, H3 @ np.zeros(3) - m)
for i, sh in enumerate([0.25, 0.1778, 0.1375]): rnd(f'newton w {i}', wn[i], sh, 4)
E('l16', 'screens[4].prose', 0.25, 0.1778, 0.1375); C('l16', 'screens[4].explain.text', math.log(5 / 3), 0.5108, 4)
for n_, g_, h_ in [(10, 100, 333), (40, 1600, 21333), (300, 90000, 9000000)]:
    two(f'n2 {n_}', n_ ** 2, g_); rnd(f'n3 {n_}', n_ ** 3 / 3, h_, 0); E('l16', 'screens[5].canvas.params.rows', g_, h_)
two('ratio', 300 ** 3 / 3 / 300 ** 2, 100); E('l16', 'screens[5].widget.answer', 100)
E('l16', 'screens[5].widget.wrong[0].value', 300); E('l16', 'screens[5].widget.wrong[1].value', 90000)
gp = lambda f: 0.8 / (1 + 2 * f) - 0.6 / (1 - f); gpp = lambda f: -1.6 / (1 + 2 * f) ** 2 - 0.6 / (1 - f) ** 2
gg = lambda f: 0.4 * math.log(1 + 2 * f) + 0.6 * math.log(1 - f)
h = 1e-5; two("g'(0)", (gg(h) - gg(-h)) / (2 * h), 0.2, 1e-8); two("g''(0)", (gg(h) - 2 * gg(0) + gg(-h)) / h ** 2, -2.2, 1e-4)
E('l16', 'screens[6].prose', 0.2, -2.2, 0.4)
fk = [0.0]
for _ in range(3): fk.append(fk[-1] - gp(fk[-1]) / gpp(fk[-1]))
fF = [F(0)]
gpF = lambda f: F(8, 10) / (1 + 2 * f) - F(6, 10) / (1 - f); gppF = lambda f: -F(16, 10) / (1 + 2 * f) ** 2 - F(6, 10) / (1 - f) ** 2
for _ in range(3): fF.append(fF[-1] - gpF(fF[-1]) / gppF(fF[-1]))
for a, b in zip(fF, fk): two('kelly', a, b)
two('f1 1/11', fF[1], F(1, 11)); C('l16', 'screens[6].widget.answer', fk[1], 0.0909, 4)
E('l16', 'screens[6].widget.wrong[0].value', -0.0909); E('l16', 'screens[6].widget.wrong[1].value', 0.2)
C('l16', 'screens[6].feedback.correct', fk[2], 0.099951, 6); C('l16', 'screens[6].feedback.correct', fk[3], 0.0999999987, 10)
C('l16', 'screens[6].explain.text', fk[1], 0.090909, 6); two('kelly formula', 0.4 - 0.6 / 2, 0.1); two('g root', gp(0.1), 0, 1e-12)
C('l16', 'screens[6].explain.text', gg(0.1), 0.009712, 6); E('l16', 'screens[6].explain.text', 0.1, 0.4, 0.3)
xr = [0.5]
for _ in range(2): xr.append(xr[-1] - (xr[-1] - math.log(xr[-1])) / (1 - 1 / xr[-1]))
rnd('trap x1', xr[1], 1.6931, 4); rnd('trap x2', xr[2], -1.1564, 4); E('l16', 'screens[8].prose', 1.6931, -1.1564)
two('trap x1 exact', xr[1], 0.5 + 0.5 + math.log(2)); E('l16', 'screens[8].explain.text', -1.1564, 0.75)
two('t0', 0.5 - math.log(0.5) + 0.5, 1.6931471805599454)
rnd('t1 f', xr[1] - math.log(xr[1]), 1.1666, 4); rnd('t1 slope', 1 - 1 / xr[1], 0.40938, 5)
two('min of x - ln x', 1 - math.log(1), 1)
two('from 2.5', 2 * 2.5 - 2.5 ** 2, -1.25); two('from 2.5 newton', 2.5 - (1 - 1 / 2.5) * 2.5 ** 2, -1.25)
E('l16', 'screens[9].widget.answer', -1.25); E('l16', 'screens[9].widget.wrong[0].value', 1.25); two('3.75', (1 - 1 / 2.5) * 6.25, 3.75)
E('l16', 'screens[9].widget.wrong[1].value', 3.75); two('from 2', 2 * 2 - 4, 0)
two('damped', 2.5 - 0.5 * 3.75, 0.625); rnd('f(2.5)', 2.5 - math.log(2.5), 1.584, 3); rnd('f(.625)', 0.625 - math.log(0.625), 1.095, 3)
E('l16', 'screens[9].explain.text', 0.625, 1.584, 1.095, -1.25)
rf = lambda x, s2: x - (s2 * x - 0.5 / x) / (s2 + 0.5 / x ** 2)
it = [1.0]
for _ in range(6): it.append(rf(it[-1], 0.04))
two("f'(1)", 0.04 - 0.5, -0.46); two("f''(1)", 0.04 + 0.5, 0.54)
C('l16', 'screens[11].widget.answer', it[1], 1.8519, 4); C('l16', 'screens[11].widget.wrong[0].value', 1 - 0.46 / 0.54, 0.1481, 4)
E('l16', 'screens[11].widget.wrong[1].value', 1.46)
for k, sh in [(2, 2.9064), (3, 3.4687), (4, 3.5349)]: C('l16', 'screens[11].explain.text', it[k], sh, 4)
two('sqrt12.5', it[6], math.sqrt(12.5)); C('l16', 'screens[11].explain.text', math.sqrt(0.5 / 0.04), 3.5355, 4)
it2 = [1.0]
for _ in range(8): it2.append(rf(it2[-1], 0.16))
C('l16', 'screens[11].explain.text', it2[-1], 1.7678, 4); two('rp w', math.sqrt(12.5) / (math.sqrt(12.5) + math.sqrt(0.5 / 0.16)), 2 / 3)
E('l16', 'screens[11].explain.text', F(2, 3), F(1, 3)); E('l16', 'screens[11].feedback.correct', '\\sqrt{12.5}', 3.5355)
rnd('it5', it[5], 3.5355, 4)
if round(it[4], 4) == 3.5355: fails.append('four more steps')
E('l16', 'screens[11].feedback.correct', 'four more steps')
two('q1', 0 - (math.exp(0) - 2) / math.exp(0), 1); E('l16', 'quiz[0].widget.answer', 1); C('l16', 'quiz[0].feedback.correct', math.log(2), 0.6931, 4)
two('q2', 0.9 - 4 * 0.9 ** 3 / (12 * 0.9 ** 2), 0.6); E('l16', 'quiz[1].widget.answer', 0.6); E('l16', 'quiz[1].widget.wrong[0].value', 0.3)
xq = [0.3]
for _ in range(2): xq.append(xq[-1] - (xq[-1] ** 3 - xq[-1]) / (3 * xq[-1] ** 2 - 1))
two("f''(0.3)", 3 * 0.09 - 1, -0.73); rnd('nc1', xq[1], -0.074, 3); rnd('nc2', xq[2], 0.0008, 4)
E('l16', 'quiz[2].prose', -0.73, -0.074); E('l16', 'quiz[2].widget.options[1].why', 0.0008)
E('l16', 'quiz[3].widget.answer', 12); two('12 places', -math.log10((1e-3) ** 4), 12)

# ================= l17 =================
wc = np.array([0.01, 0.3133, 0.6767])
two('budget', wc.sum(), 1); C('l17', 'screens[0].widget.rows[1][1].answer', wc @ m, 0.100001, 6)
vc = wc @ Sig @ wc; two('var two ways', vc, sum(np.diag(Sig) * wc ** 2)); C('l17', 'screens[0].widget.rows[2][1].answer', vc, 0.082106, 6)
E('l17', 'screens[0].widget.rows[1][1].wrong[0].value', 10.0001); E('l17', 'screens[0].widget.rows[2][1].wrong[0].value', 0.081111)
rnd('opt var', 73 / 900, 0.081111, 6); E('l17', 'screens[0].feedback.correct', 0.100001, 10.0001, 0.082106)
g2 = 2 * Sig @ wc; A = np.column_stack([np.ones(3), m]); lm = np.linalg.lstsq(A, g2, rcond=None)[0]
lmn = np.linalg.solve(A.T @ A, A.T @ g2); two('lam', lm[0], lmn[0]); two('mu', lm[1], lmn[1])
rnd('lam', lm[0], -0.1964, 4); rnd('mu', lm[1], 3.5957, 4); E('l17', 'screens[1].prose', -0.1964, 3.5957)
res = g2 - A @ lm
for i, (a_, b_, c_) in enumerate([(0.0008, -0.0166, 0.0174), (0.0564, 0.0912, None), (0.2165, 0.1991, 0.0174)]):
    rnd(f'2sw {i}', g2[i], a_, 4); rnd(f'fit {i}', (A @ lm)[i], b_, 4)
    if c_: rnd(f'res {i}', res[i], c_, 4)
E('l17', 'screens[1].canvas.params.rows', 0.0008, -0.0166, 0.0174, 0.0564, 0.0912, 0.2165, 0.1991)
C('l17', 'screens[1].widget.answer', res[1], -0.0349, 4); E('l17', 'screens[1].widget.wrong[0].value', 0.0349); E('l17', 'screens[1].widget.wrong[1].value', -0.0174)
E('l17', 'screens[1].explain.text', 0.0174, -0.0349, 0.082106, 0.081111); C('l17', 'screens[1].explain.text', vc - 73 / 900, 0.000995, 6)
E('l17', 'screens[2].feedback.correct', 0.0349); E('l17', 'screens[2].widget.options[2].why', 3.5957)
lp = linprog([-60, -40], A_ub=[[1, 1], [3, 1], [1, 0]], b_ub=[10, 18, 5], method='highs')
two('lp', -lp.fun, 480); y = -lp.ineqlin.marginals; two('dual', np.array([10, 18, 5]) @ y, 480); two('y1', y[0], 30); two('y2', y[1], 10)
E('l17', 'screens[3].widget.answer', 480); E('l17', 'screens[3].widget.wrong[0].value', 300); E('l17', 'screens[3].widget.wrong[1].value', -480)
E('l17', 'screens[3].explain.text', 480); E('l17', 'screens[3].hints[1].text', 300, 180)
Si = np.linalg.inv(Sig)
def gdual(lam, mu, nu, r=0.10):
    cc = lam * np.ones(3) + mu * m + nu; return -0.25 * cc @ Si @ cc + lam + mu * r
def gdualF(lam, mu, nu, r=F(1, 10)):
    s2 = [F(4, 100), F(9, 100), F(16, 100)]; mF = [F(5, 100), F(8, 100), F(11, 100)]
    cc = [lam + mu * mF[i] + nu[i] for i in range(3)]; return -F(1, 4) * sum(cc[i] ** 2 / s2[i] for i in range(3)) + lam + mu * r
gsF = gdualF(F(-151, 900), F(29, 9), [0, 0, 0]); two('g short', gsF, gdual(-151 / 900, 29 / 9, np.zeros(3))); two('g short val', gsF, F(139, 1800))
geF = gdualF(F(-157, 450), F(46, 9), [F(7, 75), 0, 0]); two('g exact', geF, F(73, 900))
E('l17', 'screens[4].canvas.params.rows', F(151, 900), F(29, 9), F(157, 450), F(46, 9), F(7, 75), 0.077222, 0.081111)
rnd('0.077222', float(gsF), 0.077222, 6)
C('l17', 'screens[4].widget.answer', vc - float(gsF), 0.004884, 6); E('l17', 'screens[4].widget.wrong[0].value', 0.000995)
C('l17', 'screens[4].widget.wrong[1].value', 0.082106 + 0.077222, 0.159328, 6)
E('l17', 'screens[4].feedback.correct', 0.082106, 0.077222, 0.004884, 0.000995); E('l17', 'screens[4].explain.text', 0.077222, 0.004884, F(73, 900), 0.081111, 0.000995)
gb = gdual(-0.1, 2.5, np.array([0, 0, -0.1])); rnd('bad g', gb, 0.109527, 6); E('l17', 'screens[5].prose', -0.1, 2.5, 0.109527, 0.1095)
if not gb > 73 / 900: fails.append('bad dual not above optimum')
E('l17', 'screens[5].explain.text', 0.109527, 0.081111)
cons = [{'type': 'eq', 'fun': lambda v: v.sum() - 1}, {'type': 'ineq', 'fun': lambda v: 0.10 - v @ m}]
rf_ = minimize(lambda v: v @ Sig @ v, np.ones(3) / 3, method='SLSQP', bounds=[(0, None)] * 3, constraints=cons, options={'ftol': 1e-15})
wb = np.array([36, 16, 9]) / 61; two('flip = budget-only', np.abs(rf_.x - wb).max(), 0, 1e-6); rnd('6.672', wb @ m * 100, 6.672, 3)
E('l17', 'screens[7].prose', 6.672); E('l17', 'screens[7].canvas.params.lines', 0.5902, 0.2623, 0.1475, 0.06672)
for i, sh in enumerate([0.5902, 0.2623, 0.1475]): rnd(f'wb {i}', wb[i], sh, 4)
rr = F(163, 1700); s2F = [F(4, 100), F(9, 100), F(16, 100)]; mF = [F(5, 100), F(8, 100), F(11, 100)]
a_ = sum(1 / (2 * x_) for x_ in s2F); b_ = sum(y_ / (2 * x_) for x_, y_ in zip(s2F, mF)); c_ = sum(y_ * y_ / (2 * x_) for x_, y_ in zip(s2F, mF))
det = a_ * c_ - b_ * b_; lamd = (c_ - b_ * rr) / det; mud = (a_ * rr - b_) / det
wd = [(lamd + mud * y_) / (2 * x_) for x_, y_ in zip(s2F, mF)]
two('deg w1', wd[0], 0); two('deg w2', wd[1], F(8, 17)); two('deg w3', wd[2], F(9, 17)); two('deg lam', lamd, F(-12, 85)); two('deg mu', mud, F(48, 17))
rdeg = minimize(lambda v: v @ Sig @ v, np.ones(3) / 3, method='SLSQP', bounds=[(0, None)] * 3,
                constraints=[cons[0], {'type': 'ineq', 'fun': lambda v: v @ m - 163 / 1700}], options={'ftol': 1e-15})
two('deg slsqp', rdeg.x[1], 8 / 17, 1e-6)
E('l17', 'screens[8].prose', F(163, 1700), 9.588, F(8, 17), F(9, 17), F(12, 85), F(48, 17)); rnd('9.588', 163 / 17, 9.588, 3)
nu1 = -lamd - F(5, 100) * mud; two('nu1 = 0', nu1, 0); E('l17', 'screens[8].widget.answer', 0)
C('l17', 'screens[8].widget.wrong[0].value', 7 / 75, 0.0933, 4); C('l17', 'screens[8].widget.wrong[1].value', 12 / 85, 0.1412, 4)
E('l17', 'screens[8].canvas.state.values.a2', round(8 / 17, 4)); E('l17', 'screens[8].canvas.state.values.a3', round(9 / 17, 4))
wr = np.array([0, 0.333, 0.667]); rnd('rounded var', wr @ Sig @ wr, 0.081162, 6); rnd('rounded ret', wr @ m * 100, 10.001, 3)
rnd('rounded gap', (wr @ Sig @ wr - 73 / 900) * 1e5, 5.1, 1); E('l17', 'quiz[0].prose', 0.081162, 10.001, F(73, 900), 0.081111)
E('l17', 'quiz[0].feedback.correct', 0.081162, 0.081111, 0.000051); E('l17', 'quiz[0].explain.text', 0.000051)
E('l17', 'quiz[2].widget.answer', 20); E('l17', 'quiz[2].widget.wrong[1].value', 960)
E('l17', 'screens[11].prose', 2, 4, 3); two('thirty times', 3e-5 / 1e-6, 30)

# ================= review-4 =================
two('r1', 2 / np.linalg.eigvalsh(np.array([[3.0, 1], [1, 3]])).max(), 0.5); E('review', 'items[0].widget.answer', 0.5)
two('r2', 1 - 0.3 * 4, -0.2); E('review', 'items[1].widget.answer', -0.2); E('review', 'items[1].widget.wrong[1].value', 0.7)
two('r3', count(0.8), 62); two('r3 sim', sim_count([1, 9], 2 / 10, [1, 1]), 62); two('r3 1/l', count(8 / 9), 118)
E('review', 'items[2].widget.answer', 62); E('review', 'items[2].widget.wrong[1].value', 118); C('review', 'items[2].feedback.correct', LN6 / math.log(1.25), 61.91, 2)
e9 = np.linalg.eigvalsh(0.09 * np.array([[1, 0.8], [0.8, 1]])); two('r4', e9[1] / e9[0], 9); rnd('0.162', e9[1], 0.162, 3); rnd('0.018', e9[0], 0.018, 3)
E('review', 'items[3].widget.answer', 9); E('review', 'items[3].feedback.correct', 0.162, 0.018)
two('r5', (1 + 0.6) / (1 - 0.6), 4); E('review', 'items[4].widget.answer', 4); C('review', 'items[4].widget.wrong[1].value', 1 / 0.6, 1.6667, 4)
two('r5 run', 0.6 ** 3, 0.216); two('r5 onelmax', 1 / (1 - 0.6), 2.5)
two('r6', 2 - (2 * 2 - 2 / 2) / (2 + 2 / 4), 0.8); E('review', 'items[5].widget.answer', 0.8); two('r6 sign', 2 + 1.2, 3.2); two('r6 grad', 2 - 3, -1)
E('review', 'items[6].widget.answer', 3)
Ar = np.diag([2.0, 8.0]); br = np.array([2.0, 4.0]); x0r = np.array([5.0, -3.0]); x1r = x0r - np.linalg.solve(Ar, Ar @ x0r - br)
two('r8 x', x1r[0], 1); two('r8 y', x1r[1], 0.5); gr = Ar @ x0r - br; two('r8 g', gr[1], -28); two('r8 grad step', (x0r - gr)[1], 25)
E('review', 'items[7].explain.text', 8, -28, 4, -3.5, 0.5)
lp2 = linprog([-150, -40], A_ub=[[1, 1], [3, 1], [1, 0]], b_ub=[10, 18, 5], method='highs')
two('r9', -lp2.fun, 870); two('r9 dual', np.array([10, 18, 5]) @ (-lp2.ineqlin.marginals), 870); E('review', 'items[8].widget.answer', 870)
two('r9 x', lp2.x[0], 5); E('review', 'items[8].widget.wrong[0].value', 720)
E('review', 'items[9].widget.answer', 2)

# ================= homework-4 =================
eh = np.linalg.eigvalsh(np.array([[5.0, 3], [3, 5]])); two('h1 eig', eh[1], 8); two('h1 rho', (eh[1] - eh[0]) / (eh[1] + eh[0]), 0.6)
E('homework', 'items[0].widget.answer', 0.6); E('homework', 'items[0].widget.wrong[0].value', 0.75); E('homework', 'items[0].widget.wrong[1].value', 0.25)
E('homework', 'items[0].feedback.correct', 0.2)
xf = 0.7
for _ in range(30): xf = 2 * xf / (2 * xf * xf + 1)
two('h3 fixed', xf, 1 / math.sqrt(2)); two('h3 map', 0.7 - (2 * 0.7 - 1 / 0.7) / (2 + 1 / 0.49), 2 * 0.7 / (2 * 0.49 + 1))
gk = lambda f: 0.55 / (1 + f) - 0.45 / (1 - f); two('h4', 0 - gk(0) / (-1), 0.1); two('h4 root', gk(0.1), 0, 1e-12)
E('homework', 'items[3].widget.answer', 0.1); C('homework', 'items[3].explain.text', 0.55 * math.log(1.1) + 0.45 * math.log(0.9), 0.005008, 6)
two('h5', count(2 / 3), 35); C('homework', 'items[4].feedback.correct', LN6 / math.log(1.5), 34.07, 2); E('homework', 'items[4].widget.answer', 35)
rnd('2/3^34', (2 / 3) ** 34 * 1e6, 1.03, 2); rnd('2/3^35', (2 / 3) ** 35 * 1e7, 6.9, 1); E('homework', 'items[4].feedback.byKey.floor', 1.03)
E('homework', 'items[4].explain.text', 6.9); C('homework', 'items[4].explain.text', math.log(1.5), 0.4055, 4)
two('306 formula', math.ceil(math.log(np.linalg.norm([0.06, 0.02]) / 1e-8) / math.log(1 / 0.95)), 306)
E('homework', 'items[5].feedback.correct', 306, 1, 9, 3)
md = lv.text('homework', 'items[6].model')
for v in [0.078, 0.002, 39, 270, 532, 13.8155, 0.05129, 0.0055, 3.5]: E('homework', 'items[6].model', v)
rnd('0.05129', math.log(40 / 38), 0.05129, 5); rnd('0.95^200', 0.95 ** 200 * 1e5, 3.5, 1); rnd('1/l 200', (1 - 1 / 39) ** 200, 0.0055, 4)
two('h7 270', count(0.95), 270); two('h7 532', count(1 - 1 / 39), 532)
two('h8', 0.0650 - 0.0641, 0.0009); E('homework', 'items[7].widget.answer', 0.0009); E('homework', 'items[7].widget.wrong[1].value', 0.1291)

# ================= wrong-band rule (581) =================
def band(t, ans):
    if isinstance(t, dict): return t.get('abs', 0) + t.get('rel', 0) * abs(ans)
    return float(t)
def walk(node, where):
    if isinstance(node, dict):
        if node.get('kind') == 'numeric' and 'wrong' in node:
            a = node['answer']; ta = band(node['tol'], a)
            for w_ in node['wrong']:
                if abs(w_['value'] - a) <= ta + band(w_.get('tol', 0), w_['value']):
                    fails.append(f'{where}: wrong {w_["id"]} inside the answer band')
        if node.get('edit') and 'wrong' in node and isinstance(node.get('answer'), (int, float)):
            a = node['answer']; ta = band(node.get('tol', 0), a)
            for w_ in node['wrong']:
                if 'value' in w_ and abs(w_['value'] - a) <= ta + band(w_.get('tol', 0), w_['value']):
                    fails.append(f'{where}: table wrong {w_["id"]} inside the answer band')
        for k, v in node.items(): walk(v, f'{where}.{k}')
    elif isinstance(node, list):
        for i, v in enumerate(node): walk(v, f'{where}[{i}]')
for fid, doc in lv.files.items(): walk(doc, fid)

# ================= code widgets =================
def close(x, y, rel, ab):
    x = x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x
    y = y.tolist() if hasattr(y, 'tolist') and not isinstance(y, (int, float, complex, str)) else y
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q, rel, ab) for p, q in zip(x, y))
    try:
        return math.isclose(float(x), float(y), rel_tol=rel, abs_tol=ab)
    except Exception:
        return x == y
def run_code(widget, code):
    ns = {}
    try:
        if widget.get('prelude'): exec(widget['prelude'], ns)
        exec(code, ns)
    except Exception:
        return [False] * len(widget['tests'])
    out = []
    for t in widget['tests']:
        try:
            if t.get('setup'): exec(t['setup'], ns)
            got = eval(t['call'], ns); want = eval(t['expect'], ns)
            if t.get('compare') == 'isclose':
                tol = t.get('tol'); rel = tol.get('rel', 0) if tol else 1e-9; ab = tol.get('abs', 0) if tol else 1e-12
                ok = close(got, want, rel, ab)
            else:
                g_ = got.tolist() if hasattr(got, 'tolist') else got; w_ = want.tolist() if hasattr(want, 'tolist') else want
                ok = bool(g_ == w_) and type(g_) is not type(None)
        except Exception:
            ok = False
        out.append(bool(ok))
    return out
ncode = 0
for fid, doc in lv.files.items():
    for key in ('screens', 'items'):
        for i, s_ in enumerate(doc.get(key, [])):
            w_ = s_.get('widget', {})
            if w_.get('kind') != 'code': continue
            ncode += 1
            so = run_code(w_, w_['solution']); st = run_code(w_, w_['starter'])
            if not all(so): fails.append(f'{fid} {key}[{i}] solution fails {so}')
            if any(st): fails.append(f'{fid} {key}[{i}] starter passes a test {st}')
            print(f'code {fid} {key}[{i}]: solution {sum(so)}/{len(so)}, starter {sum(st)}/{len(st)}')
if ncode != 6: fails.append(f'expected 6 code widgets, found {ncode}')

for x_ in fails: print('FAIL', x_)
print(f'two-route checks: {len(fails)} failures')
if fails:
    lv.report(); sys.exit(1)
lv.report()
