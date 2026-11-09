"""Recompute every number in eigen homework-4 item h-replicate-svd (performance task, code).

Run from anywhere with a Python that has NumPy and SymPy (the scratchpad venv), with -I:
    <venv>/bin/python -I docs/reports/eigen-4-perf-numbers.py      exits 0 when every check passes.
Route A: SymPy's exact pseudoinverse on rational tables, and mpmath's SVD at 50 digits for the
         truncated fit of the keyed table.
Route B: no SVD at all, in Fractions: least squares on independent columns, then the shortest point
         of the solution line (w_p + t n, n the parity direction); A^T (A A^T)^-1 y for the wide table;
         the normal equations for the keyed table at full rank. NumPy's float SVD for the truncated fit.
Then the item's solution must pass every test, the starter must fail every test, and each planted
bug must fail at least one hidden test (prelude, setup, call, expect, isclose with the case's tol).
"""
import json, math, os, sys
from fractions import Fraction as F
import numpy as np
import sympy as sp
import mpmath as mp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/eigen/homework-4.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'h-replicate-svd')
w = item['widget']
fails = []
def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

g = {}
exec(w['prelude'], g)
PAY = g['PAY']
for c in w['tests']:
    if c.get('setup'):
        exec(c['setup'], g)
TWO, KEYED = g['TWO'], g['KEYED']
STATES = [80, 90, 100, 110, 120]
check('PAY rows are bond, stock, call 100, put 100 at 80 to 120', PAY == [[1, s, max(s - 100, 0), max(100 - s, 0)] for s in STATES])
check('TWO is PAY at the states 90 and 110', TWO == [PAY[1], PAY[3]])
check('KEYED is PAY with the put at 90 keyed as 10.01', [r[:] for r in KEYED] == [r if i != 1 else [1, 90, 0, 10.01] for i, r in enumerate(PAY)])
check('parity: call - put = stock - 100 bonds in every state', all(r[2] - r[3] == r[1] - 100 * r[0] for r in PAY))
NULL = [100, -1, 1, -1]
check('parity direction (100, -1, 1, -1) pays nothing', all(sum(a * b for a, b in zip(r, NULL)) == 0 for r in PAY))
STRADDLE = [abs(s - 100) for s in STATES]
COVERED = [s - max(s - 100, 0) for s in STATES]
DIGITAL = [1 if s > 105 else 0 for s in STATES]
check('targets: straddle 20,10,0,10,20; covered call 80,90,100,100,100; digital above 105', STRADDLE == [20, 10, 0, 10, 20] and COVERED == [80, 90, 100, 100, 100] and DIGITAL == [0, 0, 0, 1, 1])

def Q(x):
    return sp.Rational(str(x))
def route_a(A, y):
    M = sp.Matrix([[Q(x) for x in r] for r in A])
    yv = sp.Matrix([Q(x) for x in y])
    wv = M.pinv() * yv
    return [F(int(sp.fraction(x)[0]), int(sp.fraction(x)[1])) for x in wv], [F(int(sp.fraction(x)[0]), int(sp.fraction(x)[1])) for x in (yv - M * wv)], M.rank()

def solve(Mx, b):
    """Gauss-Jordan in Fractions."""
    n = len(Mx)
    A = [list(r) + [bb] for r, bb in zip(Mx, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * yy for x, yy in zip(A[r], A[c])]
    return [A[r][n] for r in range(n)]
def normal_eq(A, y):
    A = [[F(str(x)) for x in r] for r in A]
    y = [F(str(x)) for x in y]
    m = len(A[0])
    AtA = [[sum(r[i] * r[j] for r in A) for j in range(m)] for i in range(m)]
    Aty = [sum(r[i] * yy for r, yy in zip(A, y)) for i in range(m)]
    return solve(AtA, Aty)
def route_b_pay(y):
    wp = normal_eq([r[:3] for r in PAY], y) + [F(0)]      # bond, stock, call; put weight 0
    n = [F(x) for x in NULL]
    t = -sum(a * b for a, b in zip(wp, n)) / sum(b * b for b in n)
    wv = [a + t * b for a, b in zip(wp, n)]
    res = [F(yy) - sum(F(x) * ww for x, ww in zip(r, wv)) for r, yy in zip(PAY, y)]
    return wv, res
def route_b_two(y):
    A = [[F(x) for x in r] for r in TWO]
    AAt = [[sum(a * b for a, b in zip(r1, r2)) for r2 in A] for r1 in A]
    z = solve(AAt, [F(x) for x in y])
    return [sum(A[k][i] * z[k] for k in range(2)) for i in range(4)]

EXW = {}
for name, y in (('straddle', STRADDLE), ('covered', COVERED), ('digital', DIGITAL)):
    wa, ra, rk = route_a(PAY, y)
    wb, rb = route_b_pay(y)
    check(f'{name}: SymPy pinv weights equal the shortest point of the solution line', wa == wb, str(wa))
    check(f'{name}: residuals agree', ra == rb, str(ra))
    check(f'{name}: residual orthogonal to every column (fit is least squares)', all(sum(F(r[i]) * e for r, e in zip(PAY, ra)) == 0 for i in range(4)))
    check(f'{name}: weights orthogonal to the parity direction', sum(a * b for a, b in zip(wa, NULL)) == 0)
    EXW[name] = (wa, ra)
    check(f'PAY rank 3 ({name})', rk == 3)
check('straddle weights (0, 0, 1, 1), residual 0', EXW['straddle'] == ([0, 0, 1, 1], [0] * 5))
check('covered weights 200/10003, 10001/10003, -10001/10003, -2/10003', EXW['covered'][0] == [F(200, 10003), F(10001, 10003), F(-10001, 10003), F(-2, 10003)] and EXW['covered'][1] == [0] * 5)
check('covered: the stock minus a call fits but is longer', sum(x * x for x in EXW['covered'][0]) < 2)
check('digital weights', EXW['digital'][0] == [F(-39, 70021), F(5021, 3501050), F(175033, 3501050), F(-12494, 1750525)])
check('digital residual 1/35, -2/35, -1/7, 12/35, -6/35 (not reachable)', EXW['digital'][1] == [F(1, 35), F(-2, 35), F(-1, 7), F(12, 35), F(-6, 35)])
wa, ra, rk = route_a(TWO, [0, 1])
wb = route_b_two([0, 1])
check('TWO: pinv weights equal A^T (A A^T)^-1 y', wa == wb and ra == [0, 0], str(wa))
check('TWO weights -17/20306, 551/101530, 8201/203060, -9901/203060', wa == [F(-17, 20306), F(551, 101530), F(8201, 203060), F(-9901, 203060)])
check('TWO rank 2', rk == 2)
wa, ra, rk = route_a(KEYED, STRADDLE)
wb = normal_eq(KEYED, STRADDLE)
check('KEYED full rank: pinv equals normal equations, (100, -1, 2, 0)', wa == wb == [100, -1, 2, 0] and rk == 4 and ra == [0] * 5)
check('(100, -1, 2, 0) is two calls, less the stock, plus 100 bonds', [100, -1, 2, 0] == [100, -1, 2, 0] and all(100 - r[1] + 2 * r[2] == abs(r[1] - 100) for r in PAY))

# singular values and cut-offs
mp.mp.dps = 50
def mpm(A):
    return mp.matrix([[mp.mpf(sp.Rational(str(x)).p) / sp.Rational(str(x)).q for x in r] for r in A])
U, s, V = mp.svd_r(mpm(KEYED), full_matrices=False)
sk = [float(x) for x in s]
sn = np.linalg.svd(np.array(KEYED, float), compute_uv=False)
check('KEYED singular values: mpmath and NumPy agree', np.allclose(sk, sn, rtol=1e-9, atol=1e-15), str(sk))
check('KEYED smallest singular value about 0.00008', 7.5e-5 < sk[3] < 8.5e-5, f'{sk[3]:.4e}')
check('it is below 1e-5 times the largest (relative cut drops it)', sk[3] < 1e-5 * sk[0], f'{1e-5 * sk[0]:.4e}')
check('it is above 1e-5 (an absolute cut keeps it)', sk[3] > 1e-5)
check('it is above 1e-10 times the largest (the default keeps it)', sk[3] > 1e-10 * sk[0])
sp_ = np.linalg.svd(np.array(PAY, float), compute_uv=False)
check('PAY fourth singular value is zero to rounding, below 1e-10 times the largest', sp_[3] < 1e-10 * sp_[0], f'{sp_[3]:.2e}')
st = np.linalg.svd(np.array(TWO, float), compute_uv=False)
check('TWO has two singular values, both kept', len(st) == 2 and st[1] > 1e-10 * st[0])
# truncated fit of KEYED at tol 1e-5, by mpmath and by NumPy
yv = mp.matrix(STRADDLE)
wt = [mp.mpf(0)] * 4
for i in range(3):
    cc = sum(U[j, i] * yv[j] for j in range(5)) / s[i]
    for t in range(4):
        wt[t] += V[i, t] * cc
wt = [float(x) for x in wt]
Un, sn2, Vtn = np.linalg.svd(np.array(KEYED, float), full_matrices=False)
wn = Vtn[:3].T @ ((Un[:, :3].T @ np.array(STRADDLE, float)) / sn2[:3])
check('KEYED truncated weights: mpmath equals NumPy', np.allclose(wt, wn, atol=1e-12), str(wt))
check('KEYED truncated weights near (0, 0, 1, 1)', max(abs(a - b) for a, b in zip(wt, [0, 0, 1, 1])) < 3e-4)

# ---- every expect equals the exact answer ----
tests = w['tests']
want = [
    [0, 0, 1, 1], 3, [0] * 5, EXW['covered'][0], 0, EXW['digital'][0], EXW['digital'][1],
    route_b_two([0, 1]), 2, wt, 3, [100, -1, 2, 0], True,
]
check('13 tests, 1 example, the example is test 1', len(tests) == 13 and len(w['examples']) == 1 and w['examples'][0] == tests[0])
check('how says 13 hidden tests and 1e-6', '13 hidden tests' in w['how'] and '1e-6' in w['how'])
def flat(v):
    return [float(x) for x in v] if isinstance(v, list) else [float(v)]
for k, (c, tgt) in enumerate(zip(tests, want)):
    exp = eval(c['expect'], {})
    ok = len(flat(exp)) == len(flat(tgt)) and all(abs(a - b) < 5e-8 for a, b in zip(flat(exp), flat(tgt)))
    check(f'expect of test {k + 1}', ok, c['expect'])
check('every number test has tol abs 1e-6', all(c.get('tol') == {'abs': 1e-06} for c in tests[:12]))

# ---- run code against the tests ----
def close(x, y, tol):
    x = x.tolist() if hasattr(x, 'tolist') else x
    y = y.tolist() if hasattr(y, 'tolist') else y
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(a, b, tol) for a, b in zip(x, y))
    try:
        rt, at = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)
        return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
    except Exception:
        return False
def run(src):
    res = []
    for c in tests:
        gg = {'__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec(w['prelude'], gg)
                exec(src, gg)
                if c.get('setup'):
                    exec(c['setup'], gg)
                a = eval(c['call'], gg)
                e = eval(c['expect'], gg)
            res.append(bool(close(a, e, c.get('tol'))) if c['compare'] == 'isclose' else a == e)
        except Exception:
            res.append(False)
    return res
r = run(w['solution'])
check('solution passes all 13', all(r), str(r))
r = run(w['starter'])
check('starter fails all 13', not any(r), str(r))
SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)
WLINE = 'w = Vt[keep].T @ ((U[:, keep].T @ y) / s[keep])  # V Sigma^+ U^T y'
BUGS = {
    'normal equations, solve': variant(WLINE, 'w = np.linalg.solve(A.T @ A, A.T @ y)'),
    'normal equations, inverse': variant(WLINE, 'w = np.linalg.inv(A.T @ A) @ A.T @ y'),
    'no cut-off': variant('keep = s > tol * s.max()', 'keep = s > 0'),
    'absolute cut-off': variant('keep = s > tol * s.max()', 'keep = s > tol'),
    'residual PAY w - y': variant('y - A @ w', 'A @ w - y'),
    'rank as the number of singular values': variant('int(keep.sum())', 'len(s)'),
    'rank from np.linalg.matrix_rank': variant('int(keep.sum())', 'int(np.linalg.matrix_rank(A))'),
    'drop the put, normal equations on three columns': variant(WLINE, 'w = np.append(np.linalg.solve(A[:, :3].T @ A[:, :3], A[:, :3].T @ y), 0.0)'),
    'no division by the singular values': variant(WLINE, 'w = Vt[keep].T @ (U[:, keep].T @ y)'),
    'multiplies by the singular values': variant(WLINE, 'w = Vt[keep].T @ ((U[:, keep].T @ y) * s[keep])'),
    'full matrices': variant('np.linalg.svd(A, full_matrices=False)', 'np.linalg.svd(A)'),
    'U and V swapped': variant(WLINE, 'w = U[:, keep] @ ((Vt[keep] @ y) / s[keep])'),
    'calls np.linalg.pinv (right numbers)': variant(WLINE, 'w = np.linalg.pinv(A, rcond=tol) @ y'),
    'cut-off relative to the smallest kept value': variant('keep = s > tol * s.max()', 'keep = s > tol * s[s > 0].min()'),
}
for name, src in BUGS.items():
    r = run(src)
    failed = [i + 1 for i, x in enumerate(r) if not x]
    check(f'planted bug fails a test: {name}', bool(failed), f'fails tests {failed}')
ALT = '''import numpy as np
def replicate_payoff(PAY, y, tol=1e-10):
    A = np.array(PAY, dtype=float); y = np.array(y, dtype=float)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    s_inv = np.array([1 / x if x > tol * s[0] else 0.0 for x in s])
    Aplus = Vt.T @ np.diag(s_inv) @ U.T
    w = Aplus @ y
    return list(w), list(y - A @ w), int((s_inv > 0).sum())
'''
check('another correct route (A^+ as a matrix, lists returned) passes all 13', all(run(ALT)), str(run(ALT)))

# ---- feedback numbers ----
fb = item['feedback']['byKey']
check('feedback keys name real tests', all(k == 'error' or 1 <= int(k.split('-')[1]) <= 13 for k in fb))
check('test-10 feedback: 10.01, about 0.00008, below 1e-5 times the largest', '10.01' in fb['test-10'] and '0.00008' in fb['test-10'] and sk[3] < 1e-5 * sk[0])
check('test-6 feedback: digital pays 1 above 105', DIGITAL == [1 if s_ > 105 else 0 for s_ in STATES])
check('test-9 feedback: two states give at most two singular values', min(len(TWO), len(TWO[0])) == 2)
items = doc['items']
check('homework has 6 to 12 items', 6 <= len(items) <= 12, str(len(items)))
check('one performance item in the homework', sum(1 for i in items if i.get('performance')) == 1)
check('the performance item is the last item', items[-1]['id'] == 'h-replicate-svd')
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
