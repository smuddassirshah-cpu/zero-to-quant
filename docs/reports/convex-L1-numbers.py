"""Recompute every number stated in convex level 1 (Convexity) by two routes, and check each at its JSON path.
Run: python3 docs/reports/convex-L1-numbers.py   (needs numpy and scipy; exits 0 when every check passes)
Route 1 is exact arithmetic (fractions) or a closed form; route 2 is floating point (NumPy, SciPy, a simulation).
`two(a, b)` asserts the routes agree; `lv.expect` checks the stated, rounded value appears where it is stated.
The script also runs every code widget of the level in CPython: the solution passes its hidden tests and the
starter fails at least one.
"""
import sys, os, math, json
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog, minimize, brentq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("convex", 1)
fails = []


def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def stated(name, exact, shown, places):
    """the shown value is the exact one rounded to `places`"""
    if round(float(exact), places) != round(shown, places) or abs(float(exact) - shown) > 0.6 * 10 ** -places:
        fails.append(f'{name}: {exact!r} does not round to {shown}')


E = lv.expect
SIG = [F(4, 100), F(9, 100), F(16, 100)]
M = [F(5, 100), F(8, 100), F(11, 100)]
Sig = np.diag([0.04, 0.09, 0.16]); m = np.array([0.05, 0.08, 0.11])
def var_ex(w): return sum(s * F(x) ** 2 for s, x in zip(SIG, w))
def vol_np(w): return float(np.sqrt(np.array(w, float) @ Sig @ np.array(w, float)))
def ret_ex(w): return sum(a * F(x) for a, x in zip(M, w))

# ================= l1 convex sets =================
# screen 0: two discs, midpoint of the centres
d_ex = F(3, 2)  # |(0,0) - (-1.5, 0)|
two('midpoint distance', d_ex, math.hypot(0 - (-1.5), 0)); two('other centre', d_ex, math.hypot(0 - 1.5, 0))
E('l1', 'screens[0].widget.answer', 1.5); E('l1', 'screens[0].explain.text', 1.5)
E('l1', 'screens[0].widget.wrong[1].value', 3); two('centre gap', 3, 1.5 + 1.5)
E('l1', 'screens[0].widget.wrong[0].value', 1)
# screen 2: the mix at theta = 0.4
A = [F(6, 10), F(3, 10), F(1, 10)]; B = [F(1, 10), F(2, 10), F(7, 10)]; th = F(4, 10)
Q = [th * a + (1 - th) * b for a, b in zip(A, B)]
Qn = 0.4 * np.array([0.6, 0.3, 0.1]) + 0.6 * np.array([0.1, 0.2, 0.7])
for i, (q, qn, shown) in enumerate(zip(Q, Qn, [0.30, 0.24, 0.46])):
    two(f'Q[{i}]', q, qn); stated(f'Q[{i}]', q, shown, 2)
two('Q sums to 1', sum(Q), Qn.sum())
E('l1', 'screens[2].widget.answer', 0.46); E('l1', 'screens[2].explain.text', 0.30); E('l1', 'screens[2].explain.text', 0.24)
E('l1', 'screens[2].hints[2].text', 0.04); E('l1', 'screens[2].hints[2].text', 0.42)
swap = (1 - th) * A[2] + th * B[2]; two('swap slip', swap, 0.6 * 0.1 + 0.4 * 0.7)
E('l1', 'screens[2].widget.wrong[0].value', float(swap)); E('l1', 'screens[2].feedback.byKey.swap', 0.34)
E('l1', 'screens[2].widget.wrong[1].value', float(A[2] + B[2]))
# screen 4: corners of the 50%-cap triangle by vertex enumeration (exact) and HiGHS (float)
from itertools import combinations
corners = set()
cons = [([1, 0, 0], F(1, 2)), ([0, 1, 0], F(1, 2)), ([0, 0, 1], F(1, 2)), ([-1, 0, 0], 0), ([0, -1, 0], 0), ([0, 0, -1], 0)]
for (a1, b1), (a2, b2) in combinations(cons, 2):
    Amat = np.array([[1, 1, 1], a1, a2], float)
    if abs(np.linalg.det(Amat)) < 1e-12:
        continue
    x = np.linalg.solve(Amat, np.array([1, float(b1), float(b2)]))
    if all(float(a @ x) <= float(b) + 1e-12 for a, b in [(np.array(a, float), b) for a, b in cons]):
        corners.add(tuple(round(v, 9) for v in x))
if corners != {(0.5, 0.5, 0.0), (0.5, 0.0, 0.5), (0.0, 0.5, 0.5)}:
    fails.append(f'cap corners {corners}')
for k in range(3):
    c = -np.eye(3)[k] + 0.0
    r = linprog(c, A_eq=[[1, 1, 1]], b_eq=[1], bounds=[(0, 0.5)] * 3, method='highs')
    two(f'max w{k} under cap', -r.fun, 0.5)
E('l1', 'screens[4].feedback.correct', '(\\tfrac12, \\tfrac12, 0)$, $(\\tfrac12, 0, \\tfrac12)$ and $(0, \\tfrac12, \\tfrac12)')
E('l1', 'screens[4].prose', 50); E('l1', 'screens[4].prose', 0.5)
# screen 5: risk budget, A = (0.5, 0.5, 0)
vA = var_ex([F(1, 2), F(1, 2), 0]); two('var A', vA, vol_np([0.5, 0.5, 0]) ** 2); stated('vol A', math.sqrt(vA), 0.1803, 4)
E('l1', 'screens[5].widget.answer', 0.1803); E('l1', 'screens[5].widget.wrong[0].value', float(vA)); E('l1', 'screens[5].explain.text', 0.0325)
E('l1', 'screens[5].explain.text', 18.03); E('l1', 'screens[5].feedback.correct', 18.03)
E('l1', 'screens[5].widget.wrong[1].value', 0.25); two('avg of vols', (0.2 + 0.3) / 2, 0.25)
for v, s in [(0.2, 0.04), (0.3, 0.09), (0.4, 0.16)]:
    two(f'sigma {v}', v * v, s); E('l1', 'screens[5].prose', s); E('l1', 'screens[5].prose', round(v * 100))
E('l1', 'screens[5].prose', 0.04); E('l1', 'screens[5].prose', 20)
# screen 6: trap, at least 28%
for w, shown in [([0, 1, 0], 30), ([0, 0, 1], 40), ([0, F(1, 2), F(1, 2)], 25)]:
    two(f'vol {w}', math.sqrt(var_ex(w)), vol_np([float(x) for x in w])); stated(f'vol {w}', 100 * math.sqrt(var_ex(w)), shown, 6)
E('l1', 'screens[6].prose', 30); E('l1', 'screens[6].prose', 40); E('l1', 'screens[6].prose', 28)
E('l1', 'screens[6].widget.answer', 0.25); E('l1', 'screens[6].widget.wrong[0].value', 0.35); E('l1', 'screens[6].widget.wrong[1].value', 0.0625)
two('0.28^2', 0.28 ** 2, 0.0784); two('midpoint var', var_ex([0, F(1, 2), F(1, 2)]), 0.0225 + 0.04)
E('l1', 'screens[6].explain.text', 0.0625); E('l1', 'screens[6].hints[1].text', 0.0225); E('l1', 'screens[6].hints[1].text', 0.0625)
E('l1', 'screens[6].canvas.params.functions[0].levels[0]', 0.0784)
# screen 7: least risky fully invested portfolio, 15.364%
inv = [1 / s for s in SIG]; wmv = [x / sum(inv) for x in inv]
if wmv != [F(36, 61), F(16, 61), F(9, 61)]:
    fails.append(f'min var weights {wmv}')
ones = np.ones(3); wn = np.linalg.solve(Sig, ones); wn /= wn.sum()
for a, b in zip(wmv, wn): two('wmv', a, b)
vmv = var_ex(wmv); two('min var', vmv, F(36, 1525)); two('min var np', vmv, float(wn @ Sig @ wn))
stated('min vol', 100 * math.sqrt(vmv), 15.364, 3)
E('l1', 'screens[7].prose', 15.364); E('l1', 'screens[7].prose', '\\tfrac{36}{61}, \\tfrac{16}{61}, \\tfrac{9}{61}')
E('l1', 'screens[7].feedback.correct', 15.364); E('l1', 'screens[7].explain.text', 15.364)
E('l1', 'screens[7].canvas.state.points[0].x', round(float(wmv[0]), 4)); E('l1', 'screens[7].canvas.state.points[0].y', round(float(wmv[1]), 4))
E('l1', 'screens[7].canvas.state.points[0].label', 15.36)
for lvl, pct in zip([0.0256, 0.0324, 0.04], [16, 18, 20]):
    two(f'level {pct}%', lvl, (pct / 100) ** 2); E('l1', 'screens[7].canvas.state.caption', pct)
# screen 9: two-name midpoint
mid = [(a + b) / 2 for a, b in zip([F(1, 2), F(1, 2), 0], [0, F(1, 2), F(1, 2)])]
if mid != [F(1, 4), F(1, 2), F(1, 4)] or sum(1 for x in mid if x > 0) != 3:
    fails.append(f'two-name midpoint {mid}')
E('l1', 'screens[9].widget.answer', '(1/4, 1/2, 1/4)')
# quiz
two('ring point', 1.5 ** 2, 2.25); E('l1', 'quiz[0].explain.text', 2.25)
qm = F(1, 4) * F(2, 10) + F(3, 4) * F(6, 10); two('quiz mix', qm, 0.25 * 0.2 + 0.75 * 0.6)
E('l1', 'quiz[1].widget.answer', float(qm)); E('l1', 'quiz[1].explain.text', 0.05); E('l1', 'quiz[1].explain.text', 0.45)
E('l1', 'quiz[1].widget.wrong[0].value', float(F(3, 4) * F(2, 10) + F(1, 4) * F(6, 10))); E('l1', 'quiz[1].widget.wrong[1].value', 0.8)

# ================= l2 convex functions =================
f = lambda x: x * x
x1 = F(1, 3) * -1 + F(2, 3) * 2
chord = F(1, 3) * 1 + F(2, 3) * 4; gap = chord - x1 ** 2
two('x1', x1, 1); two('gap', gap, F(1, 3) * F(2, 3) * 9); two('gap float', gap, (1 / 3) * 1 + (2 / 3) * 4 - ((1 / 3) * -1 + (2 / 3) * 2) ** 2)
E('l2', 'screens[0].widget.answer', 2); E('l2', 'screens[0].widget.wrong[0].value', float(chord)); E('l2', 'screens[0].widget.wrong[1].value', 1)
E('l2', 'screens[0].explain.text', 3); E('l2', 'screens[0].explain.text', 9); E('l2', 'screens[0].hints[1].text', 3)
c3 = (F(-8) + 0) / 2; two('x^3 chord', c3, ((-2.0) ** 3 + 0) / 2); two('x^3 curve', (-1) ** 3, -1.0)
E('l2', 'screens[1].widget.answer', -4); E('l2', 'screens[1].widget.wrong[0].value', -1); E('l2', 'screens[1].widget.wrong[2].value', float(c3 - (-1)))
E('l2', 'screens[1].widget.wrong[1].value', 4); E('l2', 'screens[1].explain.text', -8)
eg = math.e - 2; two('e - 2', eg, sum(1 / math.factorial(k) for k in range(30)) - 2); stated('e-2', eg, 0.7183, 4)
E('l2', 'screens[2].widget.answer', 0.7183); E('l2', 'screens[2].widget.wrong[0].value', 1.7183); stated('e-1', math.e - 1, 1.7183, 4)
E('l2', 'screens[2].hints[0].text', 2.7183); E('l2', 'screens[2].explain.text', 0.7183)
# -ln x: second derivative 1/x^2 checked numerically
for xx in [0.5, 1.3, 2.7]:
    h = 1e-4; fd = (-math.log(xx + h) + 2 * math.log(xx) - math.log(xx - h)) / h ** 2
    two(f'(-ln)"({xx})', fd, 1 / xx ** 2, tol=1e-5)
E('l2', 'screens[3].canvas.state.points[0].y', round(-math.log(0.5), 4)); E('l2', 'screens[3].canvas.state.points[1].y', round(-math.log(3), 4))
# eigenvalues 2 +- b
for b, (lo, hi) in [(1, (1, 3)), (2, (0, 4)), (4, (-2, 6))]:
    ev = np.linalg.eigvalsh([[2, b], [b, 2]]); two(f'eig lo b={b}', ev[0], lo); two(f'eig hi b={b}', ev[1], hi)
    E('l2', 'screens[4].explain.text', lo); E('l2', 'screens[4].explain.text', hi)
E('l2', 'screens[4].widget.answer', 2); E('l2', 'screens[4].feedback.correct', 4)
# max(2x - 1, 1 - x) switches at 2/3
two('switch', brentq(lambda x: (2 * x - 1) - (1 - x), 0, 1), F(2, 3)); E('l2', 'screens[5].explain.text', '\\tfrac23')
# trap x^2 + y^2 + 4xy
g = lambda x, y: x * x + y * y + 4 * x * y
two('f(1,-1)', g(1, -1), -2); two('f(-1,1)', g(-1, 1), -2); two('f(0,0)', g(0, 0), 0)
ev = np.linalg.eigvalsh([[2, 4], [4, 2]]); two('trap eig lo', ev[0], -2); two('trap eig hi', ev[1], 6)
E('l2', 'screens[6].prose', -2); E('l2', 'screens[6].feedback.correct', -2); E('l2', 'screens[6].feedback.correct', 6)
for t in [0.3, 1.1]: two(f'diag {t}', g(t, -t), -2 * t * t)
# sqrt|x| chord at 1/4
two('sqrt chord', 0.25 * 1 + 0.75 * 0, 0.25); two('sqrt curve', math.sqrt(0.25), 0.5); E('l2', 'screens[7].widget.options[3].why', 0.25); E('l2', 'screens[7].widget.options[3].why', 0.5)
# code-screen numbers: 4 +- sqrt 13, -0.2 and 2.2
ev = np.linalg.eigvalsh([[2, -3], [-3, 6]]); two('4-sqrt13', ev[0], 4 - math.sqrt(13)); two('4+sqrt13', ev[1], 4 + math.sqrt(13))
stated('0.3944', ev[0], 0.3944, 4); stated('7.6056', ev[1], 7.6056, 4)
E('l2', 'screens[8].feedback.correct', 0.3944); E('l2', 'screens[8].feedback.correct', 7.6056); E('l2', 'screens[8].feedback.correct', '\\sqrt{13}')
ev = np.linalg.eigvalsh([[1, 1.2], [1.2, 1]]); two('corr 1.2 lo', ev[0], 1 - 1.2); two('corr 1.2 hi', ev[1], 2.2)
E('l2', 'screens[8].explain.text', -0.2); E('l2', 'screens[8].explain.text', 2.2); E('l2', 'screens[8].explain.text', 1.2)
# transfer: impact cost
one = 100 * 2 ** 1.5; two('2^1.5', 2 ** 1.5, math.sqrt(8)); stated('2.828', 2 ** 1.5, 2.828, 3)
stated('one day', one, 282.84, 2); stated('two days', 2 * one, 565.69, 2); two('all at once', 100 * 4 ** 1.5, 800)
E('l2', 'screens[9].prose', 2.828); E('l2', 'screens[9].prose', 4); E('l2', 'screens[9].prose', 100)
E('l2', 'screens[9].widget.answer', 565.69); E('l2', 'screens[9].widget.wrong[0].value', 800); E('l2', 'screens[9].widget.wrong[1].value', 400)
E('l2', 'screens[9].widget.wrong[2].value', 282.84); E('l2', 'screens[9].explain.text', 565.69); E('l2', 'screens[9].explain.text', 282.84)
E('l2', 'screens[9].canvas.state.points[3].y', 282.84)
# quiz
ev = np.linalg.eigvalsh([[2, 3], [3, 2]]); two('q eig', ev[0], -1); two('q eig hi', ev[1], 5)
E('l2', 'quiz[1].widget.answer', -1); E('l2', 'quiz[1].widget.wrong[0].value', 5)
qg = F(1, 2) * F(1, 2) * 16; two('quiz gap', qg, (0 + 16) / 2 - 4); E('l2', 'quiz[2].widget.answer', 4); E('l2', 'quiz[2].widget.wrong[0].value', 8); E('l2', 'quiz[2].widget.wrong[1].value', 16)

# ================= l3 local is global =================
fq = lambda x: x ** 4 - 3 * x ** 2 + x; dq = lambda x: 4 * x ** 3 - 6 * x + 1
roots = sorted(np.roots([4, 0, -6, 1]).real)
br = [brentq(dq, -2, -1), brentq(dq, 0, 0.5), brentq(dq, 1, 1.5)]
for a, b in zip(roots, br): two('stationary', a, b)
for r, shown, fshown in [(br[0], -1.3008, -3.5139), (br[2], 1.1309, -1.0702), (br[1], 0.1699, 0.0841)]:
    stated(f'root {shown}', r, shown, 4); stated(f'f({shown})', fq(r), fshown, 4)
E('l3', 'screens[0].widget.answer', 1.1309); E('l3', 'screens[0].widget.wrong[0].value', -1.3008); E('l3', 'screens[0].widget.wrong[1].value', 0.1699)
E('l3', 'screens[0].explain.text', -1.0702); E('l3', 'screens[0].explain.text', -3.5139); E('l3', 'screens[0].explain.text', -1.3008); E('l3', 'screens[0].explain.text', 0.1699)
E('l3', 'screens[1].canvas.state.points[2].y', 0.0841); E('l3', 'screens[1].hints[1].text', -3.51); E('l3', 'screens[1].hints[1].text', -1.07)
# the plane trajectory (RK4 on dx/dt = -f', dy/dt = -f'^2, length 3, step 0.003) ends where descent does
def rk4(x0, L=3.0, N=1000, d=dq):
    h = L / N; x = x0; y = fq(x0)
    for _ in range(N):
        F_ = lambda x: (-d(x), -d(x) ** 2)
        k1 = F_(x); k2 = F_(x + h / 2 * k1[0]); k3 = F_(x + h / 2 * k2[0]); k4 = F_(x + h * k3[0])
        x += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); y += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return x, y
xe, ye = rk4(1.8); two('trajectory end x', xe, br[2], tol=1e-6); two('trajectory end y', ye, fq(br[2]), tol=1e-3)
xe, ye = rk4(-1.9); two('trajectory end left', xe, br[0], tol=1e-6)
# x^2 trajectory: length 6
xb = 1.5
for _ in range(1000):
    h = 0.006; k1 = -2 * xb; k2 = -2 * (xb + h / 2 * k1); k3 = -2 * (xb + h / 2 * k2); k4 = -2 * (xb + h * k3); xb += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
two('bowl end', xb, 0, tol=1e-4)
# s6: f = x^2 + xy + y^2 - 3x
sol = np.linalg.solve([[2, 1], [1, 2]], [3, 0]); two('grad zero x', sol[0], 2); two('grad zero y', sol[1], -1)
f6 = lambda x, y: x * x + x * y + y * y - 3 * x; two('f(2,-1)', f6(2, -1), -3)
ev = np.linalg.eigvalsh([[2, 1], [1, 2]]); two('s6 eig', ev[0], 1); two('s6 eig hi', ev[1], 3)
E('l3', 'screens[5].widget.answer', '(2, -1)'); E('l3', 'screens[5].feedback.correct', -3); E('l3', 'screens[5].prose', 1); E('l3', 'screens[5].prose', 3)
r = minimize(lambda v: f6(*v), [0, 0]); two('s6 by BFGS', r.fun, -3, tol=1e-6)
# s7: x^2 on the gap
E('l3', 'screens[6].feedback.correct', -1); E('l3', 'screens[6].explain.text', 4); E('l3', 'screens[6].explain.text', 1)
stated('e^-1', math.exp(-1), 0.37, 2); E('l3', 'screens[7].widget.options[1].why', 0.37)
# quiz
two('interval', 1 - (-2), 3); E('l3', 'quiz[1].widget.answer', 3); E('l3', 'quiz[1].widget.wrong[0].value', 1.5)
stated('ln 2', math.log(2), 0.6931, 4); two('ln 2 root', brentq(lambda x: math.exp(x) - 2, 0, 1), math.log(2))
E('l3', 'quiz[3].widget.answer', 0.6931); E('l3', 'quiz[3].explain.text', 0.6931)

# ================= l4 recognising =================
# relaxed (c): max m.w, long-only, w'Sw <= 0.0625. Route 1: SLSQP. Route 2: KKT on the active set (w1, w2, w3 > 0,
# variance tight): m - nu*1 = 2*kappa*Sigma*w, solved by bisection on nu with the variance equation.
r = minimize(lambda w: -m @ w, np.ones(3) / 3, method='SLSQP', bounds=[(0, None)] * 3,
             constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}, {'type': 'ineq', 'fun': lambda w: 0.0625 - w @ Sig @ w}], options={'ftol': 1e-14})
def wk(nu):
    u = (m - nu) / np.diag(Sig); return u / u.sum()
nu = brentq(lambda nu: wk(nu) @ Sig @ wk(nu) - 0.0625, 0.0, 0.0498)
w2 = wk(nu)
for a, b in zip(r.x, w2): two('relaxed w', a, b, tol=1e-6)
two('relaxed ret', -r.fun, m @ w2, tol=1e-8); stated('9.51', 100 * (m @ w2), 9.51, 2)
for a, shown in zip(w2, [0.017, 0.465, 0.519]): stated('relaxed w', a, shown, 3)
two('relaxed vol', vol_np(w2), 0.25, tol=1e-9)
E('l4', 'screens[2].prose', 9.51); E('l4', 'screens[2].prose', 0.017); E('l4', 'screens[2].prose', 0.465); E('l4', 'screens[2].prose', 0.519)
E('l4', 'screens[2].canvas.state.points[0].x', round(w2[0], 4)); E('l4', 'screens[2].canvas.state.points[0].y', round(w2[1], 4))
E('l4', 'screens[2].canvas.params.functions[1].levels[2]', round(m @ w2, 4))
# trap: exactly 25%
for w in ([0, 0.5, 0.5], [0, 0.78, 0.22]):
    stated(f'25% {w}', vol_np(w), 0.25, 9); two(f'25% exact {w}', var_ex([F(str(x)) for x in w]), F(625, 10000))
midv = var_ex([0, F(64, 100), F(36, 100)]); two('mid var', midv, 0.0576); two('mid vol', math.sqrt(midv), 0.24)
two('0.09*0.64^2', F(9, 100) * F(64, 100) ** 2, 0.036864); two('0.16*0.36^2', F(16, 100) * F(36, 100) ** 2, 0.020736)
E('l4', 'screens[5].widget.answer', 0.24); E('l4', 'screens[5].widget.wrong[1].value', 0.0576); E('l4', 'screens[5].hints[1].text', 0.036864)
E('l4', 'screens[5].hints[1].text', 0.020736); E('l4', 'screens[5].explain.text', 0.4096); E('l4', 'screens[5].explain.text', 0.1296)
two('0.64^2', 0.64 ** 2, 0.4096); two('0.36^2', 0.36 ** 2, 0.1296)
# capped infeasibility
best = ret_ex([0, F(1, 2), F(1, 2)]); res = linprog(-m, A_eq=[[1, 1, 1]], b_eq=[1], bounds=[(0, 0.5)] * 3, method='highs')
two('best capped', best, -res.fun); E('l4', 'screens[6].widget.answer', float(best)); E('l4', 'screens[6].explain.text', 9.5)
E('l4', 'screens[6].explain.text', 0.04); E('l4', 'screens[6].explain.text', 0.055)
res = linprog(np.zeros(3), A_ub=[-m], b_ub=[-0.10], A_eq=[[1, 1, 1]], b_eq=[1], bounds=[(0, 0.5)] * 3, method='highs')
if res.status != 2: fails.append(f'10% under cap status {res.status}')
E('l4', 'screens[7].canvas.params.rows[1][1]', 2)
# quiz
two('epi t', F(1, 3), 1 - F(2, 3)); E('l4', 'quiz[2].widget.answer', 0.3333); E('l4', 'quiz[2].widget.wrong[0].value', 0.6667)
two('prod mid', 1.25 * 1.25, 1.5625); E('l4', 'quiz[3].widget.options[1].why', 1.5625)

# ================= review-1 =================
v = var_ex([F(1, 2), F(1, 2), 0]); stated('r vol', math.sqrt(v), 0.1803, 4); E('review', 'items[1].widget.answer', 0.1803); E('review', 'items[1].explain.text', 0.0325)
fr = lambda x: x * x + 2 * x
two('r gap', F(1, 2) * fr(-3) + F(1, 2) * fr(1) - fr(-1), F(1, 4) * 16); E('review', 'items[2].widget.answer', 4); E('review', 'items[2].widget.wrong[0].value', 3)
E('review', 'items[2].widget.wrong[1].value', fr(-1))
ev = np.linalg.eigvalsh([[6, 2], [2, 6]]); two('r eig', ev[0], 4); two('r eig hi', ev[1], 8); E('review', 'items[3].widget.answer', 4)
two('r eig slip', np.linalg.eigvalsh([[3, 1], [1, 3]])[0], 2); E('review', 'items[3].widget.wrong[0].value', 2)
fg = lambda x: (x - 1) ** 2; two('r left', fg(0), 1); two('r right', fg(3), 4); E('review', 'items[5].widget.answer', 1); E('review', 'items[5].widget.wrong[0].value', 4)
two('r epi x', brentq(lambda x: (1 - x) - (2 * x - 5), 0, 5), 2); E('review', 'items[8].widget.answer', -1)
b40 = ret_ex([F(2, 10), F(4, 10), F(4, 10)]); res = linprog(-m, A_eq=[[1, 1, 1]], b_eq=[1], bounds=[(0, 0.4)] * 3, method='highs')
two('r cap40', b40, -res.fun); E('review', 'items[9].widget.answer', float(b40)); E('review', 'items[9].explain.text', 0.044); E('review', 'items[9].explain.text', 0.032)

# ================= homework-1 =================
jg = -0.5 * math.log(4) - (-math.log(2.5)); two('jensen', jg, math.log(1.25)); stated('jensen', jg, 0.2231, 4)
rng = np.random.default_rng(1); X = rng.choice([1.0, 4.0], 2_000_000)
two('jensen sim', np.mean(-np.log(X)) + np.log(np.mean(X)), jg, tol=2e-3)
E('homework', 'items[0].widget.answer', 0.2231); E('homework', 'items[0].feedback.correct', -0.6931); E('homework', 'items[0].feedback.correct', -0.9163)
stated('ln4/2', 0.5 * math.log(4), 0.6931, 4); stated('ln2.5', math.log(2.5), 0.9163, 4)
a_max = math.sqrt(2 * 8); two('largest a', a_max, 4)
two('a=4 det', np.linalg.det([[2, 4], [4, 8]]), 0); E('homework', 'items[1].widget.answer', 4)
cmin = (F(9, 100) - F(5, 100)) / F(9, 100); two('cap c', cmin, F(4, 9))
res = linprog(-m, A_eq=[[1, 1, 1]], b_eq=[1], bounds=[(0, 4 / 9)] * 3, method='highs'); two('cap c lp', -res.fun, 0.09, tol=1e-8)
stated('4/9', cmin, 0.4444, 4); E('homework', 'items[4].widget.answer', 0.4444)
lse = lambda x, y: math.log(math.exp(x) + math.exp(y))
p = 0.5; two('lse hess', p * (1 - p), 0.25)
# longform: 9% free optimum
A2 = np.block([[2 * Sig, -np.ones((3, 1)), -m[:, None]], [np.ones((1, 3)), np.zeros((1, 2))], [m[None, :], np.zeros((1, 2))]])
sol = np.linalg.solve(A2, [0, 0, 0, 1, 0.09])
for a, b in zip(sol[:3], [F(5, 42), F(3, 7), F(19, 42)]): two('9% w', a, b)
stated('max weight', max(sol[:3]), 0.4524, 4); stated('9% vol', 100 * math.sqrt(var_ex([F(5, 42), F(3, 7), F(19, 42)])), 22.33, 2)
lf = 'items[8].model'
for val in [9.5, 0.095, 0.0576, 24, 22.33, 0.4524, 0.025, 0.475]:
    E('homework', lf, val)
two('min holding midpoint', (0.05 + 0) / 2, 0.025); two('min holding midpoint 3', (0.45 + 0.5) / 2, 0.475)

# ================= code widgets =================
def run_code(widget, code):
    ns = {}
    if widget.get('prelude'):
        exec(widget['prelude'], ns)
    exec(code, ns)
    out = []
    for t in widget['tests']:
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns); want = eval(t['expect'], ns)
            if t.get('compare') == 'isclose':
                tol = t.get('tol', {}); rel = tol.get('rel', 0 if tol else 1e-9); ab = tol.get('abs', 0 if tol else 1e-12)
                g = np.array(got, float).ravel(); w = np.array(want, float).ravel()
                ok = g.shape == w.shape and all(math.isclose(a, b, rel_tol=rel, abs_tol=ab) for a, b in zip(g, w))
            else:
                ok = got == want
        except Exception:
            ok = False
        out.append(ok)
    return out
widgets = []
for fid, doc in lv.files.items():
    for i, s in enumerate(doc.get('screens', [])):
        if s.get('widget', {}).get('kind') == 'code': widgets.append((f'{fid} screens[{i}]', s['widget']))
    for i, s in enumerate(doc.get('items', [])):
        if s.get('widget', {}).get('kind') == 'code': widgets.append((f'{fid} items[{i}]', s['widget']))
for name, w in widgets:
    sol_ok = run_code(w, w['solution']); st_ok = run_code(w, w['starter'])
    if not all(sol_ok): fails.append(f'{name}: solution fails tests {[i for i, x in enumerate(sol_ok) if not x]}')
    if all(st_ok): fails.append(f'{name}: starter passes every test')
    print(f'code {name}: solution {sum(sol_ok)}/{len(sol_ok)}, starter {sum(st_ok)}/{len(st_ok)}')

for x in fails: print('FAIL', x)
print(f'two-route checks: {len(fails)} failures')
if fails:
    lv.report(); sys.exit(1)
lv.report()
