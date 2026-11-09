"""Recompute every number in eigen homework-2 item hw-sigma-code (performance task, code).

Run from anywhere with a Python that has NumPy and SymPy (the scratchpad venv), with -I:
    <venv>/bin/python -I docs/reports/eigen-2-perf-numbers.py      exits 0 when every check passes.
Route A: SymPy, exact rationals: demeaned matrix, Sigma = D^T D / n, w^T Sigma w, the characteristic
         polynomial and its roots.
Route B: no Sigma at all: each portfolio's variance as the population variance of its own return
         series (Fractions), and the least unit-length variance by a search over unit vectors (NumPy).
Then the item's solution must pass every test, the starter must fail every test, and each planted
bug must fail at least one hidden test (case rules as the engine: setup, call, expect, isclose
with the case's tol, element by element through tolist()).
"""
import json, math, os, sys
from fractions import Fraction as F
import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, 'app/content/courses/eigen/homework-2.json')
doc = json.load(open(HW))
item = next(i for i in doc['items'] if i['id'] == 'hw-sigma-code')
w = item['widget']
fails = []
def check(name, ok, detail=''):
    print('ok  ' if ok else 'FAIL', name, detail)
    if not ok:
        fails.append(name)

# ---- the three tables, read from the tests' setup lines ----
TABLES = {}
for c in w['tests']:
    g = {}
    exec(c['setup'], g)
    TABLES[len(g['R'])] = (g['R'], g['W'])
check('three tables: 4 days (two of them) and 5 days', sorted(TABLES) == [4, 5] and len({c['setup'] for c in w['tests']}) == 3)
tabs = {}
for c in w['tests']:
    g = {}
    exec(c['setup'], g)
    name = {2: 'R3', 3: ('R1' if len(g['R']) == 5 else 'R2')}[len(g['R'][0])]
    tabs[name] = (g['R'], g['W'])
check('tables R1, R2, R3 found', sorted(tabs) == ['R1', 'R2', 'R3'])

# ---- route A: SymPy exact ----
def route_a(R, W):
    M = sp.Matrix(R)
    n = M.rows
    D = M - sp.ones(n, 1) * (sp.ones(1, n) * M) / n
    S = D.T * D / n
    Wm = sp.Matrix([[sp.Rational(str(x)) for x in row] for row in W])
    v = [(Wm[:, j].T * S * Wm[:, j])[0, 0] for j in range(Wm.cols)]
    lam = sp.symbols('lam')
    poly = sp.Poly((S - lam * sp.eye(S.rows)).det(), lam)
    roots = sorted(float(r) for r in sp.Poly(poly, lam).nroots(n=30))
    rts = list(sp.roots(poly, lam).keys())
    exact = sorted(rts) if all(r.is_rational for r in rts) else None
    return S, v, roots, exact

# ---- route B: Fractions, no Sigma ----
def route_b(R, W):
    n, m = len(R), len(R[0])
    v = []
    for j in range(len(W[0])):
        wj = [F(str(W[i][j])) for i in range(m)]
        p = [sum(F(R[t][i]) * wj[i] for i in range(m)) for t in range(n)]
        mu = sum(p) / n
        v.append(sum((x - mu) ** 2 for x in p) / n)
    S = [[None] * m for _ in range(m)]
    for i in range(m):
        for k in range(m):
            mi = sum(F(r[i]) for r in R) / n
            mk = sum(F(r[k]) for r in R) / n
            S[i][k] = sum((F(r[i]) - mi) * (F(r[k]) - mk) for r in R) / n
    # least variance over |w| = 1: dense search over unit vectors, then refine
    A = np.array([[float(x) for x in row] for row in S])
    if m == 2:
        th = np.linspace(0, np.pi, 200001)
        U = np.stack([np.cos(th), np.sin(th)], 1)
    else:
        k = 400000
        i = np.arange(k) + 0.5
        phi = np.arccos(1 - 2 * i / k)
        th = np.pi * (1 + 5 ** 0.5) * i
        U = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
    q = np.einsum('ij,jk,ik->i', U, A, U)
    u = U[np.argmin(q)]
    for _ in range(200):                      # projected descent on the sphere
        u = u - 0.05 * (A @ u - (u @ A @ u) * u)
        u /= np.linalg.norm(u)
    return S, v, float(u @ A @ u)

EX = {}
for k, (R, W) in tabs.items():
    Sa, va, ra, exact = route_a(R, W)
    Sb, vb, lb = route_b(R, W)
    check(f'{k}: Sigma by SymPy equals Sigma by Fractions', all(sp.Rational(Sb[i][j].numerator, Sb[i][j].denominator) == Sa[i, j] for i in range(Sa.rows) for j in range(Sa.cols)))
    check(f'{k}: Sigma symmetric', Sa == Sa.T)
    check(f'{k}: variances w^T Sigma w equal the variance of each return series', [sp.Rational(x.numerator, x.denominator) for x in vb] == va, str(va))
    check(f'{k}: least eigenvalue by roots equals least by sphere search', abs(ra[0] - lb) < 1e-9, f'{ra[0]:.12f} vs {lb:.12f}')
    check(f'{k}: Sigma positive semidefinite (every root >= 0)', all(r > -1e-12 for r in ra))
    EX[k] = (Sa, va, ra[0], exact)

S1, v1, l1, _ = EX['R1']
S2, v2, l2, e2 = EX['R2']
S3, v3, l3, e3 = EX['R3']
check('R3 Sigma is [[13/2, 3], [3, 2]]', S3 == sp.Matrix([[sp.Rational(13, 2), 3], [3, 2]]))
check('R3 eigenvalues exactly 1/2 and 8', e3 == [sp.Rational(1, 2), 8])
check('R3 variances 5/2 and 2', v3 == [sp.Rational(5, 2), 2])
check('R1 Sigma is [[26/5, -12/5, 1/5], [-12/5, 2, 1/5], [1/5, 1/5, 2]]', S1 == sp.Matrix([[sp.Rational(26, 5), sp.Rational(-12, 5), sp.Rational(1, 5)], [sp.Rational(-12, 5), 2, sp.Rational(1, 5)], [sp.Rational(1, 5), sp.Rational(1, 5), 2]]))
check('R1 variances 26/5, 3/5, 14', v1 == [sp.Rational(26, 5), sp.Rational(3, 5), 14])
check('R1 least 0.6607914 to 7 places', abs(l1 - 0.6607914) < 5e-8, f'{l1:.12f}')
check('R1 least to 4 places is 0.6608', f'{l1:.4f}' == '0.6608')
check('R1 least below every single-asset variance', l1 < min(S1[i, i] for i in range(3)))
check('R1 least above 0.6, the variance of (0.5, 0.5, 0)', l1 > 0.6 and v1[1] == sp.Rational(3, 5))
check('(0.5, 0.5, 0) has length below 1 (sqrt 0.5)', math.isclose(math.hypot(0.5, 0.5), math.sqrt(0.5)) and math.hypot(0.5, 0.5) < 1)
check('(0.5, 0.5, 0) scaled to length 1 has variance 6/5 > least', 2 * v1[1] == sp.Rational(6, 5) and 1.2 > l1)
check('R2: third asset is half of A plus half of B every day', all(F(r[2]) == F(r[0] + r[1], 2) for r in tabs['R2'][0]))
check('R2 variances 0 and 5/2', v2 == [0, sp.Rational(5, 2)])
check('R2 eigenvalues exactly 0, 3/4, 9/2', e2 == [0, sp.Rational(3, 4), sp.Rational(9, 2)])
check('R2 Sigma times (1, 1, -2) is 0', S2 * sp.Matrix([1, 1, -2]) == sp.zeros(3, 1))
check('R1: sum of the roots equals the trace 46/5', abs(sum(float(r) for r in sp.Poly((S1 - sp.Symbol('x') * sp.eye(3)).det(), sp.Symbol('x')).nroots()) - 9.2) < 1e-12 and S1.trace() == sp.Rational(46, 5))

# ---- every expect equals the exact answer ----
want = {
    ('R3', 0): [[float(x) for x in S3.row(i)] for i in range(2)], ('R3', 1): [float(x) for x in v3], ('R3', 2): float(l3),
    ('R1', 0): [[float(x) for x in S1.row(i)] for i in range(3)], ('R1', 1): [float(x) for x in v1], ('R1', 2): l1,
    ('R2', 1): [float(x) for x in v2], ('R2', 2): float(l2),
}
def name_of(c):
    g = {}
    exec(c['setup'], g)
    return {2: 'R3', 3: ('R1' if len(g['R']) == 5 else 'R2')}[len(g['R'][0])]
def flat(v):
    return [x for r in v for x in (r if isinstance(r, list) else [r])] if isinstance(v, list) else [v]
tests = w['tests']
check('8 tests, 1 example, the example is test 1', len(tests) == 8 and len(w['examples']) == 1 and w['examples'][0] == tests[0])
check('how says 8 hidden tests and 1e-6', '8 hidden tests' in w['how'] and '1e-6' in w['how'])
for c in tests:
    k = int(c['call'].split('[')[-1].rstrip(']'))
    tgt = want[(name_of(c), k)]
    exp = eval(c['expect'], {})
    ok = len(flat(exp)) == len(flat(tgt)) and all(abs(a - b) <= 1e-7 for a, b in zip(flat(exp), flat(tgt)))
    check(f"expect of {name_of(c)} part {k}", ok, c['expect'])
    check(f"tol of {name_of(c)} part {k} is abs 1e-6", c.get('tol') == {'abs': 1e-06})

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
        g = {'__learner_source__': src}
        try:
            exec(src, g)
            exec(c['setup'], g)
            a = eval(c['call'], g)
            e = eval(c['expect'], g)
            res.append(bool(close(a, e, c.get('tol'))))
        except Exception:
            res.append(False)
    return res
r = run(w['solution'])
check('solution passes all 8', all(r), str(r))
r = run(w['starter'])
check('starter fails all 8', not any(r), str(r))
SOL = w['solution']
def variant(old, new):
    assert old in SOL, old
    return SOL.replace(old, new)
BUGS = {
    'no demeaning': variant('D = R - R.mean(axis=0)', 'D = R'),
    'divides by n - 1': variant('D.T @ D / len(R)', 'D.T @ D / (len(R) - 1)'),
    'np.cov with its default n - 1': variant('Sigma = D.T @ D / len(R)', 'Sigma = np.cov(R, rowvar=False)'),
    'np.cov with rows as assets': variant('Sigma = D.T @ D / len(R)', 'Sigma = np.cov(R, bias=True)'),
    'diagonal only, no cross terms': variant('np.sum(W * (Sigma @ W), axis=0)', 'np.sum(W ** 2 * np.diag(Sigma)[:, None], axis=0)'),
    'portfolios read along rows of W': variant('np.sum(W * (Sigma @ W), axis=0)', 'np.sum(W.T * (Sigma @ W.T), axis=0)'),
    'largest eigenvalue': variant('np.linalg.eigvalsh(Sigma)[0]', 'np.linalg.eigvalsh(Sigma)[-1]'),
    'least single-asset variance': variant('float(np.linalg.eigvalsh(Sigma)[0])', 'float(np.diag(Sigma).min())'),
    'least of the given portfolios': variant('float(np.linalg.eigvalsh(Sigma)[0])', 'float(variances.min())'),
    'least as the smallest entry of Sigma': variant('float(np.linalg.eigvalsh(Sigma)[0])', 'float(Sigma.min())'),
    'least from the inverse (1 / largest eigenvalue of Sigma)': variant('float(np.linalg.eigvalsh(Sigma)[0])', 'float(1 / np.linalg.eigvalsh(Sigma)[-1])'),
}
for name, src in BUGS.items():
    r = run(src)
    failed = [i + 1 for i, x in enumerate(r) if not x]
    check(f'planted bug fails a test: {name}', bool(failed), f'fails tests {failed}')
# a correct solution by another route passes: np.cov with bias, and eigenvalues by np.linalg.eig sorted
ALT = '''import numpy as np
def risk_from_returns(R, W):
    S = np.cov(np.array(R, float), rowvar=False, bias=True)
    W = np.array(W, float)
    v = [float(W[:, j] @ S @ W[:, j]) for j in range(W.shape[1])]
    return S, v, float(min(np.linalg.eig(S)[0].real))
'''
check('another correct route (np.cov bias, eig) passes all 8', all(run(ALT)))

# ---- feedback and explain numbers ----
fb = item['feedback']['byKey']
check('feedback keys name real tests', all(k == 'error' or 1 <= int(k.split('-')[1]) <= 8 for k in fb))
check('test-1 feedback numbers 6.5, 3, 2 and 4 days', all(s in fb['test-1'] for s in ('6.5', '3', '2', '4 days')) and len(tabs['R3'][0]) == 4)
check('test-2 feedback portfolios (1, -1) and (0, 1) are the columns of W3', [list(col) for col in zip(*tabs['R3'][1])] == [[1, -1], [0, 1]])
check('test-5 feedback 5.2, 0.6 and 14', v1 == [sp.Rational(26, 5), sp.Rational(3, 5), 14])
check('explain 0.6608 and 0.6', '0.6608' in item['explain']['text'] and '0.6' in item['explain']['text'])
items = doc['items']
check('homework has 6 to 12 items', 6 <= len(items) <= 12, str(len(items)))
check('one performance item in the homework', sum(1 for i in items if i.get('performance')) == 1)
check('the performance item is the last item', items[-1]['id'] == 'hw-sigma-code')
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
