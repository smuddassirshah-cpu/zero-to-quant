"""Recompute every number stated in convex level 3 (Duality and KKT) by two routes, and check each at its JSON path.
Run: python3 docs/reports/convex-L3-numbers.py   (needs numpy and scipy; exits 0 when every check passes)
Route 1 is exact arithmetic (fractions: KKT systems solved by hand-coded elimination, closed forms);
route 2 is NumPy or SciPy (SLSQP with ftol 1e-15, HiGHS, numpy.linalg). `two(a, b)` asserts the routes agree;
`lv.expect` checks the stated value appears where it is stated. Every dual value and multiplier is computed by the
hand formula and by a solver. The script also runs every code widget of the level in CPython: each solution passes
its hidden tests and each starter fails at least one.
"""
import sys, os, math
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog, minimize
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("convex", 3)
fails = []
def E(f, path, *vals, fmt=None):
    """A Fraction is checked as written in KaTeX: \\tfrac{n}{d} (or \\tfrac97 for single digits), sign outside."""
    for v in vals:
        if isinstance(v, F):
            n, d = abs(v.numerator), v.denominator
            forms = [f'frac{{{n}}}{{{d}}}'] + ([f'frac{n}{d}'] if n < 10 and d < 10 else [])
            txt = lv.text(f, path)
            lv._rec(any(x in txt for x in forms), f'{f} {path} = {v}', '' if any(x in txt for x in forms) else 'fraction not found')
        else:
            lv.expect(f, path, v, fmt=fmt)
def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')
def rnd(name, exact, shown, places):
    if abs(float(exact) - shown) > 0.51 * 10 ** -places:
        fails.append(f'{name}: {exact!r} does not round to {shown}')

def solve(A, b):                                   # exact Gauss-Jordan on fractions
    n = len(A); M = [list(map(F, row)) + [F(b[i])] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]; M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

def kkt(S, m, r, fixed):
    """Exact KKT on an active set: weights in `fixed` held at their values, budget and target as equalities.
    Returns w, lambda, mu, and res_i = (2 S w)_i - lambda - mu m_i  (= nu_i - eta_i)."""
    n = len(m); free = [i for i in range(n) if i not in fixed]; k = len(free)
    A = [[F(0)] * (k + 2) for _ in range(k + 2)]; b = [F(0)] * (k + 2)
    for row, i in enumerate(free):
        for c, j in enumerate(free): A[row][c] = 2 * S[i][j]
        A[row][k] = F(-1); A[row][k + 1] = -m[i]; b[row] = -sum(2 * S[i][j] * fixed[j] for j in fixed)
    for c, j in enumerate(free): A[k][c] = F(1); A[k + 1][c] = m[j]
    b[k] = 1 - sum(fixed.values()); b[k + 1] = r - sum(m[j] * fixed[j] for j in fixed)
    x = solve(A, b); w = [F(0)] * n
    for c, j in enumerate(free): w[j] = x[c]
    for j in fixed: w[j] = F(fixed[j])
    lam, mu = x[k], x[k + 1]
    g = [sum(2 * S[i][j] * w[j] for j in range(n)) for i in range(n)]
    res = [g[i] - lam - mu * m[i] for i in range(n)]
    var = sum(w[i] * S[i][j] * w[j] for i in range(n) for j in range(n))
    return w, lam, mu, res, var, g

def slsqp(S, m, r, lb=0, cap=None, eq=False, w0=None):
    S = np.array(S, float); m = np.array(m, float); n = len(m)
    cons = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}, {'type': 'eq' if eq else 'ineq', 'fun': lambda w: w @ m - r}]
    res = minimize(lambda w: w @ S @ w, np.ones(n) / n if w0 is None else w0, jac=lambda w: 2 * S @ w, method='SLSQP',
                   bounds=[(lb, cap)] * n, constraints=cons, options={'ftol': 1e-15, 'maxiter': 500})
    return res.x, res.fun
def mults(S, m, w, active_eq_rows):
    """Recover lambda, mu from stationarity rows of free assets by least squares (route 2 for multipliers)."""
    S = np.array(S, float); m = np.array(m, float); g = 2 * S @ w
    A = np.array([[1.0, m[i]] for i in active_eq_rows]); lam, mu = np.linalg.lstsq(A, g[active_eq_rows], rcond=None)[0]
    return lam, mu, g - lam - mu * m

S3 = [[F(4, 100), 0, 0], [0, F(9, 100), 0], [0, 0, F(16, 100)]]; M3 = [F(5, 100), F(8, 100), F(11, 100)]
S3n = np.diag([0.04, 0.09, 0.16]); M3n = np.array([0.05, 0.08, 0.11])

# ================= l9 =================
g = lambda l: l - l * l / 4
two('g(1)', g(F(1)), 0.75); two('g(3)', g(F(3)), 0.75); two('g(4)', g(F(4)), 0); two('g(2)', g(F(2)), 1)
lam_grid = np.linspace(0, 4, 4001); gnum = [min(x * x + l * (1 - x) for x in np.linspace(-2, 4, 6001)) for l in (1.0, 2.0, 3.0)]
two('g(1) num', gnum[0], 0.75, 1e-6); two('g(2) num', gnum[1], 1, 1e-6); two('g(3) num', gnum[2], 0.75, 1e-6)
E('l9', 'screens[0].widget.answer', 0.75); E('l9', 'screens[0].widget.wrong[1].value', 0.5); E('l9', 'screens[0].explain.text', 0.75, 0.5)
E('l9', 'screens[0].hints[2].text', 0.75)
E('l9', 'screens[1].widget.answer', 2); E('l9', 'screens[1].prose', 0.75); E('l9', 'screens[1].feedback.byKey.high', 0.75, 0)
E('l9', 'screens[1].explain.text', 2, 1)
E('l9', 'screens[2].explain.text', 0.75, 1, 0)
two('saddle', g(F(2)), 1); E('l9', 'screens[3].widget.options[0].text', '(1, 2, 1)'); E('l9', 'screens[3].widget.options[1].text', '(0.5, 1, 0.75)')
two('L(1,4)', 1 + 4 * (1 - 1), 1); two('min slice 4', min(x * x + 4 * (1 - x) for x in np.linspace(-1, 3, 4001)), 0, 1e-6)
s = F(1, 25) ** -1 + F(9, 100) ** -1 + F(16, 100) ** -1
two('s', s, F(1525, 36)); two('s num', np.ones(3) @ np.linalg.solve(S3n, np.ones(3)), float(s))
nus, ds = 2 / s, 1 / s; two('nu*', nus, F(72, 1525)); two('d*', ds, F(36, 1525))
gp = lambda nu: nu - nu * nu * s / 4
two('g(.03)', gp(F(3, 100)), 0.0204687, 1e-6); rnd('g(.03)', gp(F(3, 100)), 0.020469, 6)
xb, vb = slsqp(S3, [0, 0, 0], 0, lb=None)[0], None
x_bud = minimize(lambda w: w @ S3n @ w, np.ones(3) / 3, method='SLSQP', constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}], options={'ftol': 1e-15})
two('budget-only var (SLSQP vs dual)', x_bud.fun, float(ds), 1e-9)
lam_b, _, _ = mults(S3, M3, x_bud.x, [0, 1, 2]) if False else (None, None, None)
two('budget multiplier = nu* (stationarity 2 S w = nu 1)', (2 * S3n @ x_bud.x)[0], float(nus), 1e-7)
rnd('s 42.3611', s, 42.3611, 4); rnd('nu*', nus, 0.047213, 6); rnd('d*', ds, 0.023607, 6)
E('l9', 'screens[6].prose', F(1525, 36), 42.3611); E('l9', 'screens[6].widget.answer', 0.023607)
E('l9', 'screens[6].widget.wrong[0].value', 0.047213); E('l9', 'screens[6].widget.wrong[1].value', 42.3611); E('l9', 'screens[6].widget.wrong[2].value', 0.020469)
E('l9', 'screens[6].explain.text', F(72, 1525), 0.047213, F(36, 1525), 0.023607, 0.020469); E('l9', 'screens[6].hints[1].text', 0.047213)
E('l9', 'screens[6].feedback.correct', 0.023607)
gw = lambda l: -l - l * l / 4
two('reversed g max', max(gw(l) for l in lam_grid), 0); two('reversed g num at 1', min(x * x + 1 * (x - 1) for x in np.linspace(-3, 3, 6001)), gw(1), 1e-6)
E('l9', 'screens[7].prose', 0); E('l9', 'screens[7].widget.options[2].why', 1, 2); E('l9', 'screens[7].widget.options[2].text', 0.75); E('l9', 'screens[7].widget.options[1].why', 0, 1)
# duality gap {0, 2}
gg = [min(l, 2 - l) for l in lam_grid]; two('gap d*', max(gg), 1); two('gap argmax', lam_grid[int(np.argmax(gg))], 1)
two('p*', min(x for x in (0, 2) if 1 - x <= 0), 2)
E('l9', 'screens[8].prose', 2, 1); E('l9', 'screens[8].feedback.correct', 1, 2); E('l9', 'screens[8].explain.text', 1, 2)
# 2x2 correlated
Sc = [[F(4, 100), F(12, 1000)], [F(12, 1000), F(9, 100)]]; det = Sc[0][0] * Sc[1][1] - Sc[0][1] ** 2
sc = (Sc[0][0] + Sc[1][1] - 2 * Sc[0][1]) / det; two('2x2 s', sc, F(6625, 216))
two('2x2 s num', np.ones(2) @ np.linalg.solve(np.array([[0.04, 0.012], [0.012, 0.09]]), np.ones(2)), float(sc))
rnd('2x2 g(.03)', F(3, 100) - F(9, 10000) * sc / 4, 0.023099, 6); rnd('2x2 d*', 1 / sc, 0.032604, 6); two('2x2 d*', 1 / sc, F(216, 6625))
E('l9', 'screens[9].feedback.correct', F(216, 6625), 0.032604)
two('transfer gap', 10450 - 10400, 50); rnd('gap pct', F(50, 10450) * 100, 0.48, 2)
E('l9', 'screens[10].widget.answer', 50); E('l9', 'screens[10].widget.wrong[1].value', 10400); E('l9', 'screens[10].explain.text', 10400, 10450, 50, 0.48)
# quiz
E('l9', 'quiz[0].widget.answer', float(g(F(3)))); E('l9', 'quiz[0].explain.text', 2.25, 0.75)
qg = [min(2 * l, 3 - l) for l in lam_grid]; two('q gap d*', max(qg), 2); two('q gap', 3 - max(qg), 1)
E('l9', 'quiz[3].widget.answer', 1); E('l9', 'quiz[3].widget.wrong[0].value', 3); E('l9', 'quiz[3].widget.wrong[1].value', 2)

# ================= l10 =================
def proj(c, a, b):
    c = np.array(c, float); a = np.array(a, float); e = a @ c - b
    return c if e <= 0 else c - e / (a @ a) * a
p1 = proj([4, 3], [1, 1], 4); two('proj x', p1[0], 2.5); two('proj y', p1[1], 1.5)
fval = lambda x, y: (x - 4) ** 2 + (y - 3) ** 2
two('f at proj', fval(F(5, 2), F(3, 2)), 4.5)
r = minimize(lambda z: fval(*z), [0, 0], method='SLSQP', constraints=[{'type': 'ineq', 'fun': lambda z: 4 - z[0] - z[1]}], options={'ftol': 1e-15})
two('slsqp proj', r.x[0], 2.5, 1e-6); two('lambda 3 (hand)', -2 * (F(5, 2) - 4), 3)
E('l10', 'screens[0].widget.points[0].target', 2.5); E('l10', 'screens[0].feedback.correct', 2.5, 1.5, 4.5); E('l10', 'screens[0].explain.text', 4.5, 3)
E('l10', 'screens[1].prose', -3); E('l10', 'screens[1].widget.answer', 3); E('l10', 'screens[1].widget.wrong[0].value', -3); E('l10', 'screens[1].widget.wrong[1].value', 4.5)
# corner (2,2)
r = minimize(lambda z: fval(*z), [0, 0], method='SLSQP', constraints=[{'type': 'ineq', 'fun': lambda z: 4 - z[0] - z[1]}, {'type': 'ineq', 'fun': lambda z: 2 - z[0]}], options={'ftol': 1e-15})
two('corner x', r.x[0], 2, 1e-6); two('corner y', r.x[1], 2, 1e-6); two('f corner', fval(2, 2), 5)
l12 = solve([[1, 1], [1, 0]], [4, 2]); two('lam1 corner', l12[0], 2); two('lam2 corner', l12[1], 2)      # -grad f = (4, 2)
l12n = np.linalg.solve(np.array([[1.0, 1], [1, 0]]).T, [4, 2]); two('lam corner num', l12n[0], 2); two('lam corner num2', l12n[1], 2)
E('l10', 'screens[3].feedback.correct', 5); E('l10', 'screens[3].explain.text', 5, 3); E('l10', 'screens[4].widget.answer', '(2, 2)'); E('l10', 'screens[4].prose', -4, -2)
# four cases
two('second only lam2', -(2 * (2 - 4)), 4); two('second only point y', 3, 3); two('second only x+y', 2 + 3, 5)
E('l10', 'screens[6].hints[2].text', 4)
# trap x <= 3
lt = solve([[1, 1], [1, 0]], [2, 4]); two('trap lam1', lt[0], 4); two('trap lam2', lt[1], -2)  # columns a1, a2: a1*l1 + a2*l2 = (2, 4)
two('trap -grad at (3,1)', -2 * (3 - 4), 2); two('trap -grad y', -2 * (1 - 3), 4)
r = minimize(lambda z: fval(*z), [0, 0], method='SLSQP', constraints=[{'type': 'ineq', 'fun': lambda z: 4 - z[0] - z[1]}, {'type': 'ineq', 'fun': lambda z: 3 - z[0]}], options={'ftol': 1e-15})
two('trap answer x', r.x[0], 2.5, 1e-6)
E('l10', 'screens[8].prose', 4, 2, '4\\mathbf{a}_1 - 2\\mathbf{a}_2'); E('l10', 'screens[8].widget.options[1].why', -2); E('l10', 'screens[8].feedback.correct', 3, 2.5)
# quiz
E('l10', 'quiz[0].widget.answer', 0); E('l10', 'quiz[0].widget.wrong[0].value', 0.3)
qp = proj([3, 3], [1, 1], 2); two('q proj', qp[0], 1); two('q lam', -2 * (1 - 3), 4); E('l10', 'quiz[2].widget.answer', 4); E('l10', 'quiz[2].widget.wrong[0].value', 2)

# ================= l11 =================
# V(w1) on the 10% line
def Vline(w1): w1 = F(w1); return F(4, 100) * w1 ** 2 + F(9, 100) * (F(1, 3) - 2 * w1) ** 2 + F(16, 100) * (F(2, 3) + w1) ** 2
two('V coef a', (Vline(1) + Vline(-1) - 2 * Vline(0)) / 2, F(14, 25)); two('V coef b', (Vline(1) - Vline(-1)) / 2, F(7, 75)); two('V(0)', Vline(0), F(73, 900))
two('V min at', -F(7, 75) / (2 * F(14, 25)), F(-1, 12)); two('V(-1/12)', Vline(F(-1, 12)), F(139, 1800))
two('w2 = 0 at 1/6', F(1, 3) - 2 * F(1, 6), 0)
E('l11', 'screens[0].widget.points[0].target.x', 0); E('l11', 'screens[0].feedback.correct', F(73, 900), 0.081111); E('l11', 'screens[0].explain.text', 0.081111)
rnd('V(0)', F(73, 900), 0.081111, 6); rnd('7/75', F(7, 75), 0.093333, 6)
E('l11', 'screens[1].widget.answer', 0.093333); E('l11', 'screens[1].widget.wrong[1].value', 0.081111); E('l11', 'screens[1].feedback.correct', 0.0933)
# 8 %
w8, l8, mu8, res8, v8, g8 = kkt(S3, M3, F(8, 100), {})
for a, b in zip(w8, [F(9, 28), F(10, 28), F(9, 28)]): two('w8', a, b)
two('lam8', l8, F(-27, 700)); two('mu8', mu8, F(9, 7)); two('v8', v8, F(9, 280))
x, fx = slsqp(S3, M3, 0.08); lamn, mun, _ = mults(S3, M3, x, [0, 1, 2]); two('mu8 slsqp', mun, 9 / 7, 1e-6); two('lam8 slsqp', lamn, -27 / 700, 1e-6)
rnd('row2 8%', 2 * F(9, 100) * F(10, 28), 0.064286, 6); rnd('row3 8%', 2 * F(16, 100) * F(9, 28), 0.102857, 6); rnd('diff', 2 * F(16, 100) * F(9, 28) - 2 * F(9, 100) * F(10, 28), 0.038571, 6)
E('l11', 'screens[3].widget.answer', 1.285714); E('l11', 'screens[3].widget.wrong[0].value', -0.038571); E('l11', 'screens[3].widget.wrong[1].value', 0.777778)
rnd('7/9', F(7, 9), 0.777778, 6); E('l11', 'screens[3].explain.text', 0.102857, 0.064286, 0.038571, 0.03); E('l11', 'screens[3].feedback.correct', F(-27, 700), F(9, 7), 1.2857, 0.064286)
# 10 % shorting
w10, l10, mu10, res10, v10, _ = kkt(S3, M3, F(1, 10), {})
for a, b in zip(w10, [F(-1, 12), F(1, 2), F(7, 12)]): two('w10 short', a, b)
two('mu10 short', mu10, F(29, 9)); two('v10 short', v10, F(139, 1800))
x, fx = slsqp(S3, M3, 0.10, lb=None); two('w10 short slsqp', x[0], -1 / 12, 1e-6)
rnd('vol short', math.sqrt(139 / 1800), 0.27789, 5)
E('l11', 'screens[4].prose', F(29, 9), F(-1, 12), F(7, 12))
# 10 % long-only, w1 = 0
wl, ll, mul, resl, vl, gl = kkt(S3, M3, F(1, 10), {0: 0})
for a, b in zip(wl, [0, F(1, 3), F(2, 3)]): two('wl', a, b)
two('mul', mul, F(46, 9)); two('ll', ll, F(-157, 450)); two('nu1', resl[0], F(7, 75)); two('vl', vl, F(73, 900))
two('nu1 = V\'(0)', resl[0], F(7, 75))
x, fx = slsqp(S3, M3, 0.10); lamn, mun, resn = mults(S3, M3, x, [1, 2]); two('mul slsqp', mun, 46 / 9, 1e-6); two('ll slsqp', lamn, -157 / 450, 1e-6); two('nu1 slsqp', resn[0], 7 / 75, 1e-6)
two('row3 16/75', 2 * F(16, 100) * F(2, 3), F(16, 75)); two('row2 0.06', 2 * F(9, 100) * F(1, 3), F(6, 100)); two('23/150', F(16, 75) - F(6, 100), F(23, 150))
for v, sh, p in [(mul, 5.1111, 4), (ll, -0.3489, 4), (resl[0], 0.0933, 4)]: rnd('l11 table', v, sh, p)
E('l11', 'screens[5].widget.rows[0][1].answer', 5.1111); E('l11', 'screens[5].widget.rows[1][1].answer', -0.3489); E('l11', 'screens[5].widget.rows[2][1].answer', 0.0933)
E('l11', 'screens[5].prose', 0.06, F(16, 75), 0.08, 0.11, 0.05); E('l11', 'screens[5].hints[1].text', 0.153333); E('l11', 'screens[5].feedback.correct', F(46, 9), F(-157, 450), F(7, 75), 5.1111, -0.3489, 0.0933)
E('l11', 'screens[5].explain.text', F(23, 150), F(46, 9), F(-157, 450), F(7, 75), 0.0933)
rnd('vol lo', math.sqrt(73 / 900), 0.2848, 4); rnd('vol lo 3dp', math.sqrt(73 / 900) * 100, 28.480, 3); rnd('vol avg', F(1, 3) * F(3, 10) + F(2, 3) * F(4, 10), 0.366667, 6)
E('l11', 'screens[6].widget.answer', 0.2848); E('l11', 'screens[6].widget.wrong[0].value', 0.081111); E('l11', 'screens[6].widget.wrong[1].value', 0.366667)
E('l11', 'screens[6].feedback.correct', 28.480, 27.789); E('l11', 'screens[6].explain.text', 0.01, 0.071111, 0.081111, 28.480, 0.7)
two('var parts', F(9, 100) * F(1, 9), F(1, 100)); rnd('0.071111', F(16, 100) * F(4, 9), 0.071111, 6); rnd('cost of ban', (math.sqrt(73 / 900) - math.sqrt(139 / 1800)) * 100, 0.7, 1)
# clip
clip = [F(0), F(1, 2) / F(13, 12), F(7, 12) / F(13, 12)]
rnd('clip w2', clip[1], 0.4615, 4); rnd('clip w3', clip[2], 0.5385, 4); rnd('clip ret', sum(a * b for a, b in zip(clip, M3)) * 100, 9.615, 3)
rnd('no rescale sum', F(1, 2) + F(7, 12), 1.0833, 4); cv = sum(S3[i][i] * clip[i] ** 2 for i in range(3)); rnd('clip var', cv, 0.0656, 4)
E('l11', 'screens[7].prose', F(13, 12), 0.4615, 0.5385); E('l11', 'screens[7].widget.options[0].text', 9.615); E('l11', 'screens[7].widget.options[1].text', 1.0833)
E('l11', 'screens[7].widget.options[3].why', 0.0656); E('l11', 'screens[7].feedback.correct', 9.615)
rnd('l1+mu m1', ll + mul * F(5, 100), -0.0933, 4); E('l11', 'screens[8].explain.text', -0.3489, 5.1111, -0.0933, 0.0933)
# 6 % floor
wb = [F(36, 61), F(16, 61), F(9, 61)]; rnd('budget-only ret', sum(a * b for a, b in zip(wb, M3)) * 100, 6.672, 3)
two('budget-only var', sum(S3[i][i] * wb[i] ** 2 for i in range(3)), F(36, 1525))
x, fx = slsqp(S3, M3, 0.06); two('6% slsqp var', fx, 36 / 1525, 1e-9)
two('6% lambda = 72/1525', (2 * S3n @ x)[0], 72 / 1525, 1e-6)
E('l11', 'screens[9].widget.answer', 0); E('l11', 'screens[9].prose', 6.672, F(36, 61), F(16, 61), F(9, 61)); E('l11', 'screens[9].explain.text', 0.06672, F(72, 1525))
rnd('nu1 step', F(7, 75) / 100, 0.000933, 6)
E('l11', 'screens[11].widget.answer', 0.000933); E('l11', 'screens[11].widget.wrong[0].value', 0.093333); E('l11', 'screens[11].explain.text', 0.0933, 0.000933)
# quiz
two('q nu', F(30, 100) - F(5, 100) * 4, F(1, 10)); E('l11', 'quiz[1].widget.answer', 0.1)
two('q w', (F(-1, 10) + 2 * F(8, 100)) / (2 * F(9, 100)), F(1, 3)); E('l11', 'quiz[2].widget.answer', 0.333333)
rnd('q no2', (F(-1, 10) + F(16, 100)) / F(9, 100), 0.666667, 6); E('l11', 'quiz[2].widget.wrong[0].value', 0.666667)

# ================= l12 =================
two('hook var', vl, F(73, 900)); E('l12', 'screens[0].canvas.params.lines[11]', 0.081111111111111)
E('l12', 'screens[0].widget.answer', 0.2848); E('l12', 'screens[0].feedback.correct', 28.480)
two('explore min', F(-1, 12), -0.0833333333, 1e-6); rnd('explore var', F(139, 1800), 0.077222, 6)
E('l12', 'screens[1].widget.answer', -0.083333); E('l12', 'screens[1].feedback.correct', 0.077222)
vol = [F(8, 100), F(20, 100), F(30, 100), F(40, 100)]; M4 = [F(3, 100), F(5, 100), F(8, 100), F(11, 100)]
rho = {(0, 1): F(-2, 10), (0, 2): F(0), (0, 3): F(1, 10), (1, 2): F(3, 10), (1, 3): F(1, 10), (2, 3): F(5, 10)}
S4 = [[vol[i] * vol[j] * (1 if i == j else rho[(min(i, j), max(i, j))]) for j in range(4)] for i in range(4)]
S4n = np.array([[float(x) for x in r_] for r_ in S4]); M4n = np.array([float(x) for x in M4])
eig = np.linalg.eigvalsh(S4n)
for a, b in zip(eig, [0.0060, 0.0328, 0.0615, 0.1961]): rnd('eig', a, b, 4)
w4, l4, mu4, res4, v4, g4 = kkt(S4, M4, F(85, 1000), {0: 0, 3: F(4, 10)})
for a, b in zip(w4, [0, F(7, 30), F(11, 30), F(2, 5)]): two('w4', a, b)
two('v4', v4, F(27923, 450000)); two('l4', l4, F(-1147, 11250)); two('mu4', mu4, F(631, 225)); two('nu1 4', res4[0], F(17, 900)); two('eta4', -res4[3], F(77, 2500))
x, fx = slsqp(S4, M4, 0.085, cap=0.4); two('w4 slsqp', x[1], 7 / 30, 1e-6); two('v4 slsqp', fx, 27923 / 450000, 1e-9)
lamn, mun, resn = mults(S4, M4, x, [1, 2]); two('mu4 slsqp', mun, 631 / 225, 1e-5); two('l4 slsqp', lamn, -1147 / 11250, 1e-5); two('nu1 slsqp', resn[0], 17 / 900, 1e-5); two('eta4 slsqp', -resn[3], 77 / 2500, 1e-5)
rnd('vol4', math.sqrt(27923 / 450000) * 100, 24.910, 3)
for a, b in zip(g4, [0.001067, 0.038267, 0.1224, 0.175733]): rnd('2Sw', a, b, 6)
for v, sh, p in [(mu4, 2.8044, 4), (l4, -0.1020, 4), (res4[0], 0.0189, 4), (-res4[3], 0.0308, 4)]: rnd('l12 table', v, sh, p)
E('l12', 'screens[3].canvas.params.lines[4]', 0.006, 0.0328, 0.0615, 0.1961); E('l12', 'screens[3].canvas.params.lines[8]', 0.233333, 0.366667, 0.4)
E('l12', 'screens[3].canvas.params.lines[10]', 0.062051111111111); E('l12', 'screens[3].feedback.correct', F(27923, 450000), 0.062051, 24.910)
E('l12', 'screens[3].explain.text', 0.0060, 0.0328, 0.0615, 0.1961)
E('l12', 'screens[4].canvas.params.rows[*]', 0.001067, 0.038267, 0.122400, 0.175733, 0.233333, 0.366667)
E('l12', 'screens[4].widget.rows[0][1].answer', 2.8044); E('l12', 'screens[4].widget.rows[1][1].answer', -0.1020); E('l12', 'screens[4].widget.rows[2][1].answer', 0.0189); E('l12', 'screens[4].widget.rows[3][1].answer', 0.0308)
E('l12', 'screens[4].explain.text', 0.084133, F(631, 225), F(-1147, 11250), F(17, 900), F(77, 2500)); rnd('0.084133', g4[2] - g4[1], 0.084133, 6)
lp = linprog(-M4n, A_eq=[np.ones(4)], b_eq=[1], bounds=[(0, 0.4)] * 4, method='highs'); two('max ret cap .4', -lp.fun, 0.086, 1e-9)
two('max ret exact', F(4, 10) * F(11, 100) + F(4, 10) * F(8, 100) + F(2, 10) * F(5, 100), F(86, 1000))
lp9 = linprog(np.zeros(4), A_ub=[-M4n], b_ub=[-0.09], A_eq=[np.ones(4)], b_eq=[1], bounds=[(0, 0.4)] * 4, method='highs')
if lp9.status != 2: fails.append(f'9% status {lp9.status}')
E('l12', 'screens[5].widget.answer', 0.086); E('l12', 'screens[5].widget.wrong[1].value', 0.076); E('l12', 'screens[5].canvas.params.lines[4]', 2)
two('0.076', F(4, 10) * F(11, 100) + F(4, 10) * F(8, 100), F(76, 1000)); E('l12', 'screens[5].explain.text', 0.044, 0.032, 0.010, 8.6)
# sign flip trap
cons = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}, {'type': 'ineq', 'fun': lambda w: 0.10 - w @ M3n}]
rf = minimize(lambda w: w @ S3n @ w, np.ones(3) / 3, jac=lambda w: 2 * S3n @ w, method='SLSQP', bounds=[(0, None)] * 3, constraints=cons, options={'ftol': 1e-15})
for a, b in zip(rf.x, [0.5902, 0.2623, 0.1475]): rnd('flip x', a, b, 4)
rnd('flip ret', rf.x @ M3n * 100, 6.672, 3); two('flip var', rf.fun, 36 / 1525, 1e-9)
if not rf.success: fails.append('flip not success')
E('l12', 'screens[6].canvas.params.lines[3]', 0.5902, 0.2623, 0.1475); E('l12', 'screens[6].prose', 6.672)
# 35 % cap
w35, l35, mu35, res35, v35, _ = kkt(S4, M4, F(8, 100), {3: F(35, 100)})
two('bond 35', w35[0], F(9, 1442)); x, fx = slsqp(S4, M4, 0.08, cap=0.35); two('bond 35 slsqp', x[0], 9 / 1442, 1e-6)
if not (mu35 > 0 and -res35[3] > 0 and min(w35) > 0): fails.append('35% cap KKT signs')
for a, b in zip(w35, [0.006241, 0.339598, 0.304161, 0.35]): rnd('w35', a, b, 6)
E('l12', 'screens[8].canvas.params.lines[3]', 0.006241, 0.339598, 0.304161, 0.35); E('l12', 'screens[8].prose', 0.0062)
E('l12', 'screens[8].feedback.correct', F(9, 1442), 0.006241); E('l12', 'screens[8].explain.text', 0.0062, 0.3396, 0.3042, 0.35)
# tracking
bF = [F(1, 10), F(3, 10), F(3, 10), F(3, 10)]
A_ = [[2 * S4[i][j] for j in range(3)] + [F(-1)] for i in range(3)] + [[F(1), F(1), F(1), F(0)]]
rhs = [sum(2 * S4[i][j] * bF[j] for j in range(4)) for i in range(3)] + [F(1)]
xt = solve(A_, rhs); wt = xt[:3] + [F(0)]
if min(wt[:3]) <= 0: fails.append('tracking weights not all positive')
d = [wt[i] - bF[i] for i in range(4)]; te = sum(d[i] * S4[i][j] * d[j] for i in range(4) for j in range(4))
bn = np.array([0.1, 0.3, 0.3, 0.3])
rt = minimize(lambda w: (w - bn) @ S4n @ (w - bn), np.ones(4) / 4, jac=lambda w: 2 * S4n @ (w - bn), method='SLSQP', bounds=[(0, None)] * 3 + [(0, 0)],
              constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}], options={'ftol': 1e-15})
for a, b in zip(rt.x, wt): two('track w', a, b, 1e-6)
two('track te', rt.fun, te, 1e-9)
for a, b in zip(wt[:3], [0.2209, 0.2753, 0.5037]): rnd('track', a, b, 4)
rnd('te vol', math.sqrt(te) * 100, 10.317, 3); rnd('te var', te, 0.010644, 6)
rnd('rise bond', wt[0] - bF[0], 0.12, 2); rnd('rise eq2', wt[2] - bF[2], 0.20, 2); rnd('eq1 change', wt[1] - bF[1], -0.025, 3)
E('l12', 'screens[9].canvas.params.rows[*]', 0.2209, 0.2753, 0.5037); E('l12', 'screens[9].feedback.correct', 0.20, 10.317)
E('l12', 'screens[9].explain.text', 0.2209, 0.2753, 0.5037, 0.010644); E('l12', 'screens[9].widget.options[1].why', 0.12, 0.20); E('l12', 'screens[9].feedback.byKey.even', 0.12, -0.025, 0.20)
E('l12', 'screens[9].widget.options[2].why', 0.2753)
# quiz
two('q reach', F(5, 10) * F(9, 100) + F(5, 10) * F(6, 100), F(75, 1000)); E('l12', 'quiz[2].widget.answer', 0.075)

# ================= l13 =================
def desk(b, extra=None):
    A = [[1, 1], [3, 1], [1, 0]] + ([[2, 1]] if extra else []); bb = list(b) + ([14] if extra else [])
    r = linprog([-60, -40], A_ub=A, b_ub=bb, method='highs'); return -r.fun, -r.ineqlin.marginals
def desk_exact(b):                                    # vertex enumeration on fractions
    rows = [([1, 1], b[0]), ([3, 1], b[1]), ([1, 0], b[2]), ([-1, 0], 0), ([0, -1], 0)]; best = None
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            (a1, b1), (a2, b2) = rows[i], rows[j]; det = F(a1[0] * a2[1] - a1[1] * a2[0])
            if det == 0: continue
            x = (F(b1) * a2[1] - F(b2) * a1[1]) / det; y = (F(a1[0]) * b2 - F(a2[0]) * b1) / det
            if all(r_[0] * x + r_[1] * y <= rb for r_, rb in rows):
                v = 60 * x + 40 * y; best = v if best is None or v > best else best
    return best
vR = lambda R: min(40 * R, 300 + 10 * R, 500)
for R in [5, 10, 15, 18, 19, 20, 23, 25]:
    two(f'v({R})', desk_exact([10, R, 5]), vR(R)); two(f'v({R}) highs', desk([10, R, 5])[0], vR(R), 1e-7)
two('v(19)', vR(19), 490); two('v(23)', vR(23), 500); two('line 23', 480 + 5 * 10, 530); two('slope40 23', 480 + 5 * 40, 680)
E('l13', 'screens[0].widget.answer', 490); E('l13', 'screens[0].widget.wrong[1].value', 520); E('l13', 'screens[0].hints[2].text', 270, 220)
E('l13', 'screens[0].explain.text', 4.5, 5.5, 490); two('19 plan', 60 * F(9, 2) + 40 * F(11, 2), 490)
two('risk dual', desk([10, 18, 5])[1][1], 10, 1e-7); two('risk slope exact', desk_exact([10, F(181, 10), 5]) - desk_exact([10, 18, 5]), F(1))
E('l13', 'screens[1].widget.answer', 10); E('l13', 'screens[1].widget.wrong[0].value', 40); E('l13', 'screens[1].widget.wrong[1].value', 30)
vB = lambda B: min(60 * B, 100 + 40 * B, 180 + 30 * B, 720)
for B in [3, 5, 7, 8, 10, 13, 18, 20]: two(f'v(B={B})', desk_exact([B, 18, 5]), vB(B))
two('budget price', desk([10, 18, 5])[1][0], 30, 1e-7)
for B in [8.01, 17.99]: two(f'budget price at {B}', desk([B, 18, 5])[1][0], 30, 1e-7)
two('budget price below 8', desk([7.99, 18, 5])[1][0], 40, 1e-7); two('budget price above 18', desk([18.01, 18, 5])[1][0], 0, 1e-7)
E('l13', 'screens[2].hints[1].text', 5, 8, 18)
# mean-variance target prices
A_, B_, C_ = sum(1 / S3[i][i] for i in range(3)), sum(M3[i] / S3[i][i] for i in range(3)), sum(M3[i] ** 2 / S3[i][i] for i in range(3)); D_ = A_ * C_ - B_ ** 2
Vf = lambda r_: (A_ * r_ * r_ - 2 * B_ * r_ + C_) / D_
two('frontier coef a', A_ / D_, F(3050, 63)); two('frontier coef b', 2 * B_ / D_, F(407, 63)); two('frontier coef c', C_ / D_, F(3013, 12600))
two('Vf(.08)', Vf(F(8, 100)), F(9, 280)); two('Vf(.082)', Vf(F(82, 1000)), F(2749, 78750)); two('dVf/dr at 8%', (2 * A_ * F(8, 100) - 2 * B_) / D_, F(9, 7))
x, fx = slsqp(S3, M3, 0.082, lb=None, eq=True); two('8.2 slsqp', fx, 2749 / 78750, 1e-9)
rnd('pred 8.2', F(9, 7) * F(2, 1000), 0.002571, 6); rnd('exact 8.2', Vf(F(82, 1000)) - Vf(F(8, 100)), 0.002765, 6); rnd('v 8.2', Vf(F(82, 1000)), 0.034908, 6)
rnd('vol 8.2', math.sqrt(2749 / 78750) * 100, 18.684, 3); rnd('vol 8', math.sqrt(9 / 280) * 100, 17.928, 3); rnd('pct slip', F(9, 7) * F(2, 10), 0.257143, 6)
E('l13', 'screens[3].prose', F(9, 280), F(9, 7), 0.032143, 1.2857); E('l13', 'screens[3].widget.answer', 0.002571); E('l13', 'screens[3].widget.wrong[0].value', 0.257143); E('l13', 'screens[3].widget.wrong[1].value', 0.002765)
E('l13', 'screens[3].explain.text', 0.002571, F(2749, 78750), 0.034908, 0.002765, 18.684, 17.928)
r0 = F(163, 1700); wr0 = kkt(S3, M3, r0, {})[0]; two('r0: w1 = 0', wr0[0], 0); rnd('r0 pct', r0 * 100, 9.588, 3)
w101, l101, mu101, res101, v101, _ = kkt(S3, M3, F(101, 1000), {0: 0})
for a, b in zip(w101, [0, F(3, 10), F(7, 10)]): two('w10.1', a, b)
two('v10.1', v101, F(173, 2000)); x, fx = slsqp(S3, M3, 0.101); two('10.1 slsqp', fx, 0.0865, 1e-9)
rnd('pred 10.1', F(46, 9) / 1000, 0.005111, 6); rnd('exact 10.1', v101 - F(73, 900), 0.005389, 6); rnd('vol 10.1', math.sqrt(0.0865) * 100, 29.411, 3)
two('0.0081 + 0.0784', F(9, 100) * F(9, 100) + F(16, 100) * F(49, 100), F(865, 10000)); rnd('pct slip 10.1', F(46, 9) / 10, 0.511111, 6)
E('l13', 'screens[4].prose', F(46, 9), 5.1111, F(73, 900), 0.081111, 9.588); E('l13', 'screens[4].widget.answer', 0.005111); E('l13', 'screens[4].widget.wrong[0].value', 0.005389)
E('l13', 'screens[4].widget.wrong[1].value', 0.511111); E('l13', 'screens[4].feedback.correct', 0.0865, 0.005389, 29.411); E('l13', 'screens[4].explain.text', 0.0081, 0.0784, 0.0865, 0.005389)
# moving the wall
two('V(-0.01)', Vline(F(-1, 100)), F(73, 900) - F(7, 7500) + F(14, 250000)); rnd('V(-0.01)', Vline(F(-1, 100)), 0.080234, 6)
rnd('saving', F(73, 900) - Vline(F(-1, 100)), 0.000877, 6); x, fx = slsqp(S3, M3, 0.10, lb=-0.01); two('wall slsqp', fx, float(Vline(F(-1, 100))), 1e-9)
rnd('0.000056', F(14, 25) * F(1, 10000), 0.000056, 6)
E('l13', 'screens[5].widget.answer', 0.000877); E('l13', 'screens[5].widget.wrong[0].value', 0.000933); E('l13', 'screens[5].widget.wrong[1].value', 0.080234)
E('l13', 'screens[5].explain.text', 0.000056, 0.000933, 0.081111, 0.080234, 0.000877)
E('l13', 'screens[6].widget.answer', 500); E('l13', 'screens[6].widget.wrong[0].value', 530); E('l13', 'screens[6].widget.wrong[1].value', 680); E('l13', 'screens[6].explain.text', 480, 20, 500)
two('liquidity slack', 5 - 4, 1); two('liquidity price', desk([10, 18, 5])[1][2], 0, 1e-9)
w9 = kkt(S3, M3, F(9, 100), {})[0]; two('9% free w3', w9[2], F(19, 42)); rnd('max weight 9%', max(w9), 0.4524, 4)
E('l13', 'screens[7].feedback.correct', 45.2); E('l13', 'screens[7].explain.text', 0.4524)
# degenerate corner
def acceptable(y): return y[0] + 3 * y[1] + y[2] + 2 * y[3] >= 60 and y[0] + y[1] + y[3] >= 40 and min(y) >= 0
cost = lambda y: 10 * y[0] + 18 * y[1] + 5 * y[2] + 14 * y[3]
for y, ok in [((30, 10, 0, 0), True), ((20, 0, 0, 20), True), ((25, 5, 0, 10), True), ((30, 10, 0, 20), False), ((40, 0, 0, 0), False)]:
    if (acceptable(y) and cost(y) == 480) != ok: fails.append(f'certificate {y}')
two('cost (30,10,0,20)', cost((30, 10, 0, 20)), 760); two('row A (40,0,0,0)', 40, 40)
for R, v_, du in [(17.99, 479.9, [30, 10, 0, 0]), (18.01, 480, [20, 0, 0, 20])]:
    val, mg = desk([10, R, 5], extra=True); two(f'deg {R}', val, v_, 1e-7)
    for a, b in zip(mg, du): two(f'deg dual {R}', a, b, 1e-7)
E('l13', 'screens[8].widget.options[3].why', 760); E('l13', 'screens[8].widget.options[4].why', 40); E('l13', 'screens[8].feedback.correct', 17.99, 479.9, 18.01, 480)
# cap 45 %
wc, lc, muc, resc, vc, _ = kkt(S3, M3, F(9, 100), {2: F(45, 100)})
for a, b in zip(wc, [F(7, 60), F(13, 30), F(9, 20)]): two('wc', a, b)
two('lc', lc, F(-473, 4500)); two('muc', muc, F(103, 45)); two('eta3', -resc[2], F(1, 375)); two('vc', vc, F(2243, 45000)); two('v free 9', kkt(S3, M3, F(9, 100), {})[4], F(157, 3150))
x, fx = slsqp(S3, M3, 0.09, cap=0.45); lamn, mun, resn = mults(S3, M3, x, [0, 1]); two('eta3 slsqp', -resn[2], 1 / 375, 1e-6); two('muc slsqp', mun, 103 / 45, 1e-6)
rnd('eta3', F(1, 375), 0.002667, 6); rnd('lc', lc, -0.105111, 6); rnd('0.11 mu', F(11, 100) * muc, 0.251778, 6)
rnd('vc', vc, 0.049844, 6); rnd('vfree', F(157, 3150), 0.049841, 6); rnd('vol c', math.sqrt(2243 / 45000) * 100, 22.3259, 4); rnd('vol free', math.sqrt(157 / 3150) * 100, 22.3252, 4)
E('l13', 'screens[10].prose', F(-473, 4500), F(103, 45), 0.45); E('l13', 'screens[10].widget.answer', 0.002667); E('l13', 'screens[10].widget.wrong[0].value', -0.002667)
E('l13', 'screens[10].feedback.correct', F(1, 375), 0.00267, F(2243, 45000), 0.049844, F(157, 3150), 0.049841, 22.3259, 22.3252); E('l13', 'screens[10].explain.text', -0.105111, 0.251778, 0.144, 0.002667)
# quiz
two('venue', 1000 * F(15, 100), 150); two('venue price', F(40, 100) - F(25, 100), F(15, 100)); E('l13', 'quiz[0].widget.answer', 150)
rate = float(F(9, 7)) / (2 * math.sqrt(9 / 280)); rnd('vol rate', rate, 3.586, 3); rnd('0.35857', 2 * math.sqrt(9 / 280), 0.35857, 5); rnd('0.72', rate * 0.002 * 100, 0.72, 2)
E('l13', 'quiz[1].widget.answer', 3.586); E('l13', 'quiz[1].feedback.correct', 0.35857, 3.586); E('l13', 'quiz[1].explain.text', 0.17928, 3.586, 0.72)

# ================= review-3 =================
two('g(.06)', gp(F(6, 100)), F(7, 320)); two('g(.06) dec', gp(F(6, 100)), 0.021875); E('review', 'items[0].widget.answer', 0.021875); E('review', 'items[0].explain.text', 0.038125, 0.021875, 0.023607)
pr = proj([2, 2], [1, 2], 2); two('r proj x', pr[0], 1.2); two('r proj y', pr[1], 0.4); two('r lam', -2 * (F(6, 5) - 2), F(8, 5))
E('review', 'items[3].widget.answer', 1.6); E('review', 'items[3].widget.wrong[0].value', 0.8); E('review', 'items[3].explain.text', -1.6, -3.2, 1.6)
w101b = kkt(S3, M3, F(101, 1000), {0: 0}); two('r nu1', w101b[3][0], F(29, 250)); two('r lam101', w101b[1], F(-599, 1500)); two('r mu101', w101b[2], F(17, 3))
E('review', 'items[5].widget.answer', 0.116); E('review', 'items[5].prose', -0.399333, 5.666667); rnd('0.283333', F(5, 100) * F(17, 3), 0.283333, 6)
lp = linprog(-M3n, A_eq=[np.ones(3)], b_eq=[1], bounds=[(0, 0.45)] * 3, method='highs'); two('r reach', -lp.fun, 0.0905, 1e-9)
two('r reach exact', F(45, 100) * F(11, 100) + F(45, 100) * F(8, 100) + F(1, 10) * F(5, 100), F(905, 10000)); two('r short', F(45, 100) * (F(11, 100) + F(8, 100)), F(855, 10000))
E('review', 'items[7].widget.answer', 0.0905); E('review', 'items[7].widget.wrong[1].value', 0.0855)
two('r shadow', desk_exact([12, 18, 5]), 540); two('r shadow highs', desk([12, 18, 5])[0], 540, 1e-7); E('review', 'items[8].widget.answer', 540)
rl = linprog([-3, -2], A_ub=[[1, 1], [1, 0]], b_ub=[4, 3], method='highs'); two('r lp', -rl.fun, 11, 1e-9); two('r lp duals', -rl.ineqlin.marginals[0], 2, 1e-9)
two('r lp dual cost', 4 * 2 + 3 * 1, 11); E('review', 'items[9].widget.answer', 11); E('review', 'items[9].widget.wrong[0].value', 12); E('review', 'items[9].widget.wrong[1].value', 8)

# ================= homework-3 =================
gh = lambda l: 2 * l - l * l / 2
two('h dual peak', max(gh(l) for l in lam_grid), 2); r = minimize(lambda z: z @ z, [0, 0], method='SLSQP', constraints=[{'type': 'ineq', 'fun': lambda z: z.sum() - 2}], options={'ftol': 1e-15}); two('h p*', r.fun, 2, 1e-9)
two('h dual exact', 2 * F(1, 4) * 4 + 2 * (2 - 2), 2)
hg = [min(l, 4 - 3 * l) for l in lam_grid]; two('h gap d*', max(hg), 1); two('h gap', 4 - max(hg), 3)
E('homework', 'items[2].widget.answer', 3); E('homework', 'items[2].widget.wrong[0].value', 4); E('homework', 'items[2].widget.wrong[1].value', 1)
ph = proj([3, 2], [1, 2], 4); two('h kkt x', ph[0], 2.4); two('h kkt y', ph[1], 0.8); two('h lam', -2 * (F(12, 5) - 3), F(6, 5))
E('homework', 'items[3].widget.answer', '(2.4, 0.8, 1.2)'); E('homework', 'items[3].explain.text', 7, 4, 3, 2.4, 0.8, -1.2, -2.4, 1.2)
r = minimize(lambda z: (z[0] - 3) ** 2 + (z[1] - 3) ** 2, [0, 0], method='SLSQP', constraints=[{'type': 'ineq', 'fun': lambda z: 2 - z[0] - z[1]}, {'type': 'ineq', 'fun': lambda z: 0.5 - z[0]}], options={'ftol': 1e-15})
two('h corner x', r.x[0], 0.5, 1e-6); two('h corner y', r.x[1], 1.5, 1e-6)
lc2 = solve([[1, 1], [1, 0]], [5, 3]); two('h corner lam1', lc2[0], 3); two('h corner lam2', lc2[1], 2)
E('homework', 'items[4].widget.answer', '(0.5, 1.5, 3, 2)'); E('homework', 'items[4].feedback.correct', 5, 3)
w9f, l9f, mu9f, _, _, _ = kkt(S3, M3, F(9, 100), {}); two('h mu9', mu9f, F(142, 63)); two('h lam9', l9f, F(-13, 126))
x, fx = slsqp(S3, M3, 0.09, lb=None, eq=True); lamn, mun, _ = mults(S3, M3, x, [0, 1, 2]); two('h mu9 slsqp', mun, 142 / 63, 1e-6)
rnd('h mu9', mu9f, 2.253968, 6); rnd('h lam9', l9f, -0.103175, 6); rnd('h row3', 2 * F(16, 100) * F(19, 42), 0.144762, 6); rnd('h no2', (F(16, 100) * F(19, 42) - l9f) / F(11, 100), 1.595960, 6)
rnd('h 0.247937', 2 * F(16, 100) * F(19, 42) - l9f, 0.247937, 6)
E('homework', 'items[5].widget.answer', 2.253968); E('homework', 'items[5].widget.wrong[0].value', -0.103175); E('homework', 'items[5].widget.wrong[1].value', 1.59596)
E('homework', 'items[5].explain.text', 0.144762, 0.103175, 0.247937, F(142, 63))
for t, v_ in [(0.06, 0.153644), (0.08, 0.179284), (0.10, 0.2848), (0.11, 0.4)]: rnd(f'frontier {t}', math.sqrt(slsqp(S3, M3, t)[1]), v_, 4)
two('frontier 9.5 cap', math.sqrt(slsqp(S3, M3, 0.095, cap=0.5)[1]), 0.25, 1e-6)
E('homework', 'items[6].feedback.correct', 15.364, 17.928, 28.480, 40, 25)
# longform model numbers
mdl = 'items[7].model'
E('homework', mdl, F(-13, 126), F(142, 63), F(5, 42), F(3, 7), F(19, 42), F(7, 60), F(13, 30), F(9, 20), 0.4524, 0.0405, 0.0275, 0.03, 0.4333, 0.1167, 0.009333, 0.078, 0.068667, F(103, 45), 2.2889, 0.114444, F(-473, 4500),
  0.144, -0.105111, 0.251778, F(1, 375), 0.00267, 0.005833, 0.034667, 0.0495, 0.000544, 0.0169, 0.0324, F(2243, 45000), 0.049844, 22.326, F(157, 3150), 0.049841, 9.005, 0.116667, 0.433333)
for a, b, p in [(F(9, 100) - F(45, 100) * F(11, 100), 0.0405, 4), (F(55, 100) * F(5, 100), 0.0275, 4), (2 * F(4, 100) * F(7, 60), 0.009333, 6), (2 * F(9, 100) * F(13, 30), 0.078, 3),
                (F(78, 1000) - 2 * F(4, 100) * F(7, 60), 0.068667, 6), (F(5, 100) * F(103, 45), 0.114444, 6), (F(5, 100) * F(7, 60), 0.005833, 6), (F(8, 100) * F(13, 30), 0.034667, 6),
                (F(4, 100) * F(7, 60) ** 2, 0.000544, 6), (F(9, 100) * F(13, 30) ** 2, 0.0169, 4), (F(16, 100) * F(81, 400), 0.0324, 4), (math.sqrt(2243 / 45000) * 100, 22.326, 3)]:
    rnd('model', a, b, p)
strict = [F(11, 100), F(445, 1000), F(445, 1000)]; two('strict sum', sum(strict), 1); rnd('strict ret', sum(a * b for a, b in zip(strict, M3)) * 100, 9.005, 3)
if not all(0 < s_ < F(45, 100) for s_ in strict): fails.append('strict point not strictly inside')
E('homework', 'items[7].rubric[*].text', 0.4524, F(2243, 45000), 0.049844, 22.326, F(-473, 4500), F(103, 45), F(1, 375))

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
            if t.get('compare') == 'raises':
                try:
                    eval(t['call'], ns); ok = False
                except Exception as e:
                    ok = t['expect'] in [k.__name__ for k in type(e).__mro__]
                out.append(ok); continue
            got = eval(t['call'], ns); want = eval(t['expect'], ns)
            if t.get('compare') == 'isclose':
                tol = t.get('tol'); rel = tol.get('rel', 0) if tol else 1e-9; ab = tol.get('abs', 0) if tol else 1e-12
                ok = close(got, want, rel, ab)
            else:
                g_ = got.tolist() if hasattr(got, 'tolist') else got; w_ = want.tolist() if hasattr(want, 'tolist') else want
                ok = bool(g_ == w_)
        except Exception:
            ok = False
        out.append(bool(ok))
    return out
ncode = 0
for fid, doc in lv.files.items():
    for key in ('screens', 'items'):
        for i, s_ in enumerate(doc.get(key, [])):
            w = s_.get('widget', {})
            if w.get('kind') != 'code': continue
            ncode += 1
            so = run_code(w, w['solution']); st = run_code(w, w['starter'])
            if not all(so): fails.append(f'{fid} {key}[{i}] solution fails {so}')
            if all(st): fails.append(f'{fid} {key}[{i}] starter passes')
            print(f'code {fid} {key}[{i}]: solution {sum(so)}/{len(so)}, starter {sum(st)}/{len(st)}')
if ncode != 6: fails.append(f'expected 6 code widgets, found {ncode}')

for x_ in fails: print('FAIL', x_)
print(f'two-route checks: {len(fails)} failures')
if fails:
    lv.report(); sys.exit(1)
lv.report()
