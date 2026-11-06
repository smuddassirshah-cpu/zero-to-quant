"""Recompute every number stated in app/content/exams/stage-1.json by a second route and assert it at its path.

Route A is build.py (closed forms and reference code). Route B here is independent: numerical differentiation and
integration, grid searches, exact Fractions, NumPy decompositions, sqlite3 running the printed SQL, replication on the
tree, the closed-form binomial sum, contour and line integrals summed numerically, and a fine-step ODE solve.
Every code solution is run against its hidden tests (Python here, C++ with the local g++) and every starter must fail one.
Expression keys are evaluated from their LaTeX at sample points. A last pass reads every number in every learner-visible
string of each item: whole numbers 0 to 10 count as structure, every other number must match a route-B or given value
for that item to its printed precision. Exits 1 on any failure.
Run: python3 docs/briefs/exam-stage-1-scripts/check_numbers.py
"""
import cmath
import glob
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from statistics import NormalDist

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, _FRAC, _NUM, _walk, normalise  # noqa: E402

EXAM = os.path.join(ROOT, 'app', 'content', 'exams', 'stage-1.json')
N01 = NormalDist()


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
PATH, ITEM = {}, {}
for pi, p in enumerate(doc['parts']):
    for j, it in enumerate(p.get('items', [])):
        PATH[it['id']] = f'parts[{pi}].items[{j}]'
        ITEM[it['id']] = it
ALLOW = {}


def allow(iid, *vals):
    ALLOW.setdefault(iid, []).extend(float(v) for v in vals)


def W(iid, part=None):
    it = ITEM[iid]
    return it['widget'] if part is None else it['parts'][part]['widget']


def rec(ok, label, note=''):
    ex._rec(bool(ok), label, '' if ok else note)


def key(iid, value, part=None):
    w = W(iid, part)
    t = max(w['tol']['abs'] / 10, 1e-9) if w['tol']['abs'] else 1e-9
    rec(abs(w['answer'] - value) <= t, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {value!r}', 'route B differs')
    allow(iid, value)


def wrong(iid, wid, value, part=None):
    w = W(iid, part)
    hit = [x for x in w['wrong'] if x['id'] == wid]
    t = max(hit[0]['tol']['abs'] / 10, 1e-9) if hit and hit[0]['tol']['abs'] else 1e-9
    rec(len(hit) == 1 and abs(hit[0]['value'] - value) <= t, f'{iid} wrong "{wid}" = {value!r}', f'found {hit}')
    allow(iid, value)


def wrongs_all(iid, part=None):
    """every wrong id was checked by wrong()"""
    return sorted(x['id'] for x in W(iid, part).get('wrong', []))


def correct_id(iid, want, part=None):
    w = W(iid, part)
    got = sorted(o['id'] for o in w['options'] if o.get('correct'))
    rec(got == [want], f'{iid} correct option {got} = {want}')
    rec(w.get('shuffle') is True, f'{iid} shuffle true')
    rec(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} every distractor has a why')


def simpson(f, a, b, m=4000):
    h = (b - a) / m
    return h / 3 * (f(a) + f(b) + sum((4 if k % 2 else 2) * f(a + k * h) for k in range(1, m)))


def deriv(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


# ---------------------------------------------------------------- LaTeX evaluation for expression keys
def _group(s, i):
    depth = 0
    for j in range(i, len(s)):
        depth += {'{': 1, '}': -1}.get(s[j], 0)
        if depth == 0:
            return s[i + 1:j], j + 1
    raise ValueError(s)


def tex_py(s):
    s = s.replace(' ', '')
    out, i = '', 0
    while i < len(s):
        if s.startswith('\\frac', i):
            a, i = _group(s, i + 5)
            b, i = _group(s, i)
            out += f'(({tex_py(a)})/({tex_py(b)}))'
        elif s[i] == '^' and i + 1 < len(s) and s[i + 1] == '{':
            a, i = _group(s, i + 1)
            out += f'**({tex_py(a)})'
        else:
            out += s[i]
            i += 1
    out = re.sub(r'(?<=[\d)xs])(?=[xs(])', '*', out)
    return out.replace('^', '**')


def tex_val(src, **v):
    return float(eval(tex_py(src), {}, v))


def expr_check(iid, fn, var, pts, wrong_ids):
    w = W(iid)
    for form in [w['answer']] + w.get('accept', []):
        rec(all(abs(tex_val(form, **{var: p}) - fn(p)) < 1e-9 * max(1, abs(fn(p))) for p in pts), f'{iid} expression {form!r} = route B')
    for x in w.get('wrong', []):
        rec(any(abs(tex_val(x['tex'], **{var: p}) - fn(p)) > 1e-6 for p in pts), f'{iid} wrong "{x["id"]}" differs from the key')
    rec(sorted(x['id'] for x in w.get('wrong', [])) == sorted(wrong_ids), f'{iid} wrong ids {sorted(wrong_ids)}')


def order_check(iid, n_answer, n_distr):
    w = W(iid)
    ids = [ln['id'] for ln in w['lines']]
    rec(len(w['answer']) == n_answer and len(w.get('distractors', [])) == n_distr and sorted(w['answer'] + w.get('distractors', [])) == sorted(ids),
        f'{iid} order: {n_answer} lines in the answer, {n_distr} distractors, nothing else')
    rec(all(ln.get('why') for ln in w['lines'] if ln['id'] in w.get('distractors', [])), f'{iid} every flawed line has a why')
    bk = ITEM[iid]['feedback'].get('byKey', {})
    rec(all(d in bk for d in w.get('distractors', [])) and 'left-out' in bk, f'{iid} byKey names each flawed line and left-out')


# ---------------------------------------------------------------- running code solutions
def _close(a, b, tol):
    if isinstance(a, (list, tuple)):
        return isinstance(b, (list, tuple)) and len(a) == len(b) and all(_close(x, y, tol) for x, y in zip(a, b))
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return False
    rel = tol.get('rel', 0 if 'abs' in tol else 1e-9)
    ab = tol.get('abs', 0 if 'rel' in tol else 1e-12)
    return math.isclose(a, b, rel_tol=rel, abs_tol=ab)


def _plain(v):
    if isinstance(v, np.ndarray):
        return v.tolist()
    if isinstance(v, (np.floating, np.integer)):
        return v.item()
    if isinstance(v, pd.Series):
        return v.tolist()
    return v


def run_py(src, tests):
    """Return the number of tests passed (an exception fails that test)."""
    passed = 0
    for t in tests:
        ns = {'__learner_source__': src}
        try:
            exec(src, ns)
            if t.get('setup'):
                exec(t['setup'], ns)
            got = _plain(eval(t['call'], ns))
            want = eval(t['expect'], {})
            if t['compare'] == 'equal':
                ok = got == want
            else:
                ok = _close(got, want, t.get('tol', {}))
        except Exception:
            ok = False
        passed += bool(ok)
    return passed


def code_py(iid, part=None):
    w = W(iid, part)
    lab = f'{iid}{"" if part is None else f" part {part}"}'
    n = len(w['tests'])
    rec(run_py(w['solution'], w['tests']) == n, f'{lab}: the solution passes all {n} tests')
    rec(run_py(w['starter'], w['tests']) < n, f'{lab}: the starter fails a test')
    rec(all(e['expect'] in [t['expect'] for t in w['tests']] for e in w['examples']), f'{lab}: each example is a hidden test')
    rec(f'{n} hidden tests' in w['how'], f'{lab}: how states {n} tests')
    return w['tests']


def lit_cpp(v, ty):
    if ty == 'bool':
        return 'true' if v else 'false'
    return repr(float(v)) if ty == 'double' else str(int(v))


def run_cpp(src, tests):
    passed = 0
    with tempfile.TemporaryDirectory() as td:
        for t in tests:
            args = ', '.join(lit_cpp(a, ty) for a, ty in zip(t['args'], t['types']))
            main = src + f'\n#include <cstdio>\nint main() {{ std::printf("%.17g\\n", (double){t["call"]}({args})); return 0; }}\n'
            cpp, exe = os.path.join(td, 'm.cpp'), os.path.join(td, 'm')
            open(cpp, 'w').write(main)
            if subprocess.run(['g++', '-std=c++17', '-O1', cpp, '-o', exe], capture_output=True).returncode:
                continue
            out = subprocess.run([exe], capture_output=True, text=True, timeout=20).stdout.strip()
            passed += math.isclose(float(out), float(t['expect']), rel_tol=1e-9, abs_tol=1e-12)
    return passed


# ======================================================================== Paper A
f1 = lambda x: (x ** 3 + 2 * x) ** 4
key('a-chain-power', round(deriv(f1, 1.0), 3))
wrong('a-chain-power', 'no-inner', round(deriv(lambda u: u ** 4, 3.0), 3))
allow('a-chain-power', 27)

key('a-ftc-log', round(simpson(lambda x: 2 * x + 1 / x, 1, 3), 6))
wrong('a-ftc-log', 'dropped-log', round(simpson(lambda x: 2 * x, 1, 3), 6))
wrong('a-ftc-log', 'upper-only', round(simpson(lambda x: 2 * x + 1 / x, 1, 3) + 1, 6))

qs = np.arange(0, 45, 0.0005)
prof = qs * (90 - 2 * qs) - 10 * qs - 50
key('a-desk-profit', round(float(prof.max()), 3))
wrong('a-desk-profit', 'gave-q', round(float(qs[prof.argmax()]), 3))
rev = qs * (90 - 2 * qs)
qr = float(qs[rev.argmax()])
wrong('a-desk-profit', 'revenue-max', round(qr * (90 - 2 * qr) - 10 * qr - 50, 3))
allow('a-desk-profit', 90, 50, qr, 1600, 800, 80)

key('a-parts-exp', round(simpson(lambda x: x * math.exp(3 * x), 0, 1), 6))
wrong('a-parts-exp', 'sign-slip', round(simpson(lambda x: x * math.exp(3 * x), 0, 1) - 2 / 9, 6))

ecoef = [F(1, math.factorial(k)) for k in range(4)]
scoef = [F(1), F(0), F(-1, 2), F(0)]
prod = [sum(ecoef[i] * scoef[k - i] for i in range(k + 1)) for k in range(4)]
rec(prod == [1, 1, 0, F(-1, 3)], f'a-taylor-product: coefficients {prod}')
expr_check('a-taylor-product', lambda x: float(sum(c * x ** k for k, c in enumerate(prod))), 'x', [0.3, 0.7, 1.3, 2.1], ['only-exp', 'dropped-cross'])

f6 = lambda x, y: x * y * y + 2 * x
g6 = np.array([deriv(lambda x: f6(x, 1), 2), deriv(lambda y: f6(2, y), 1)])
key('a-directional', round(float(g6 @ np.array([3, 4]) / 5), 6))
wrong('a-directional', 'unnormalised', round(float(g6 @ np.array([3, 4])), 6))
allow('a-directional', 0.6, 0.8, 1.8, 3.2)

xs7 = np.arange(0, 32, 0.0001)
pr7 = xs7 * (32 - xs7) / 4
key('a-lagrange-product', round(float(pr7.max()), 4))
wrong('a-lagrange-product', 'gave-x', round(float(xs7[pr7.argmax()]), 3))
wrong('a-lagrange-product', 'gave-lambda', round(float((32 - xs7[pr7.argmax()]) / 4), 3))
allow('a-lagrange-product', 32)

m8 = 800
h8 = 3 / m8
cx = (np.arange(m8) + 0.5) * h8
XX, YY = np.meshgrid(cx, cx)
key('a-triangle-integral', round(simpson(lambda x: simpson(lambda y: x + y, 0, x, 40), 0, 3, 40), 9))   # iterated Simpson, inner limit y = x
wrong('a-triangle-integral', 'square', round(float(np.sum(XX + YY) * h8 * h8), 6))
allow('a-triangle-integral', 27)

key('a-cos-limit', round((1 - math.cos(4e-4)) / 1e-8, 4))
wrong('a-cos-limit', 'no-half', round(2 * (1 - math.cos(4e-4)) / 1e-8, 4))
allow('a-cos-limit', 16)

M10 = np.array([[2, 1, 0], [1, 3, 1], [0, 1, 4.0]])
key('a-det-three', round(float(np.linalg.det(M10)), 6))
wrong('a-det-three', 'plus-sign', 2 * 11 + 1 * 4)
allow('a-det-three', 12, 22)

M11 = [[F(v) for v in row] for row in [[1, 2, 0, 1, 3], [2, 4, 1, 3, 1], [3, 6, 1, 4, 4]]]
rk, piv = 0, 0
for c in range(5):
    pr_ = next((i for i in range(rk, 3) if M11[i][c] != 0), None)
    if pr_ is None:
        continue
    M11[rk], M11[pr_] = M11[pr_], M11[rk]
    for i in range(3):
        if i != rk and M11[i][c] != 0:
            fac = M11[i][c] / M11[rk][c]
            M11[i] = [a - fac * b for a, b in zip(M11[i], M11[rk])]
    rk += 1
sv = np.linalg.svd(np.array([[1, 2, 0, 1, 3], [2, 4, 1, 3, 1], [3, 6, 1, 4, 4.0]]), compute_uv=False)
rec(rk == int(np.sum(sv > 1e-10)), f'a-nullity: rank {rk} by Fractions and by SVD')
key('a-nullity', 5 - rk)
wrong('a-nullity', 'gave-rank', rk)

b12, v12 = np.array([4, 1, 3.0]), np.array([1, 2, 2.0])
coef, *_ = np.linalg.lstsq(v12.reshape(3, 1), b12, rcond=None)
key('a-line-distance', round(float(np.linalg.norm(b12 - coef[0] * v12)), 6))
wrong('a-line-distance', 'proj-length', round(float(np.linalg.norm(coef[0] * v12)), 6))
allow('a-line-distance', 12, 9, 4 / 3, 1 / 3, 8, 5, 10)

M13 = np.array([[6, 2], [2, 3.0]])
vals, vecs = np.linalg.eigh(M13)
top = vecs[:, -1]
rec(abs(abs(top @ np.array([2, 1]) / math.sqrt(5)) - 1) < 1e-12, 'a-eigvec: (2, 1) is the top eigenvector')
rec(abs(abs(vecs[:, 0] @ np.array([1, -2]) / math.sqrt(5)) - 1) < 1e-12 and abs(vals[0] - 2) < 1e-12, 'a-eigvec: (1, -2) belongs to eigenvalue 2')
rec(list(M13 @ [1, 2]) == [10, 8] and list(M13 @ [6, 2]) == [40, 18], 'a-eigvec: A(1, 2) = (10, 8), A(6, 2) = (40, 18)')
correct_id('a-eigvec', 'a')
allow('a-eigvec', 10, 40, 18, np.trace(M13), np.linalg.det(M13), *vals)

M14 = np.array([[2, 0], [3, 4.0]])
s14 = np.linalg.svd(M14, compute_uv=False)
key('a-singular', round(float(s14[0]), 6))
wrong('a-singular', 'eig-of-A', float(max(np.linalg.eigvals(M14).real)))
wrong('a-singular', 'no-root', round(float(s14[0] ** 2), 6))
allow('a-singular', *(M14.T @ M14).ravel(), np.trace(M14.T @ M14), np.linalg.det(M14.T @ M14))

ls_t = code_py('a-ls-pca-code', 0)
pc_t = code_py('a-ls-pca-code', 1)
allow('a-ls-pca-code', 1e-9)
for t in ls_t[:2]:
    ns = {}
    exec(t['setup'], {'np': np}, ns)
    Q, R = np.linalg.qr(ns['X'])
    rec(np.allclose(np.linalg.solve(R, Q.T @ ns['y']), eval(t['expect']), rtol=1e-10), f'a-ls-pca-code: {t["setup"][:40]}... expect matches QR')
for t in pc_t:
    ns = {}
    exec(t['setup'], {'np': np}, ns)
    Z = ns['R'] - ns['R'].mean(axis=0)
    S = Z.T @ Z
    w_ = np.ones(S.shape[0])
    for _ in range(3000):
        w_ = S @ w_
        w_ /= np.linalg.norm(w_)
    w_ = w_ if w_.sum() > 0 else -w_
    rec(np.allclose(w_, eval(t['expect']), rtol=1e-8, atol=1e-12), 'a-ls-pca-code: power iteration matches the PCA expect')

# ======================================================================== Paper B
pf = F(4, 100) * F(8, 10) / (F(4, 100) * F(8, 10) + F(96, 100) * F(3, 100))
key('b-fraud-flag', round(float(pf), 4))
wrong('b-fraud-flag', 'sensitivity', 0.8)
wrong('b-fraud-flag', 'base-rate', 0.04)
allow('b-fraud-flag', 4, 80, 3, 0.032, 0.96, 0.03, 0.0288, 0.0608, 0.8)

P2 = np.array([[0.85, 0.15], [0.25, 0.75]])
pi2 = np.linalg.matrix_power(P2, 400)[0]
key('b-regime-share', round(float(pi2[0]), 6))
wrong('b-regime-share', 'stay-prob', 0.85)
wrong('b-regime-share', 'average', round((0.85 + 0.25) / 2, 4))
allow('b-regime-share', 0.15, 0.25, 0.40)

xb = np.array([1, -1.0])
pb = np.array([0.53, 0.47])
mu1 = float(xb @ pb)
var1 = float((xb - mu1) ** 2 @ pb)
sd = math.sqrt(350 * var1)
key('b-many-bets', round(N01.cdf(-350 * mu1 / sd), 4))
wrong('b-many-bets', 'no-root', round(N01.cdf(-350 * mu1 / (350 * var1)), 4))
allow('b-many-bets', 350, 0.53, mu1, mu1 ** 2, var1, 350 * mu1, round(350 * var1, 2), round(sd, 2), round(350 * mu1 / sd, 2))

Sig = np.array([[4, 0.5], [0.5, 1]])
a4 = np.array([2, -3.0])
key('b-var-combo', round(float(a4 @ Sig @ a4), 9))
wrong('b-var-combo', 'plus-cov', round(float(a4 @ Sig @ a4) + 12, 9))
wrong('b-var-combo', 'ignored-cov', round(float(a4 ** 2 @ np.diag(Sig)), 9))
allow('b-var-combo', 0.5, 16, 9, 6, 5)

Mr = np.zeros((6, 6))
rhs = np.zeros(6)
Mr[0, 0] = Mr[5, 5] = 1
rhs[5] = 1
for i in range(1, 5):
    Mr[i, i], Mr[i, i + 1], Mr[i, i - 1] = 1, -0.6, -0.4
hit = np.linalg.solve(Mr, rhs)
key('b-ruin-target', round(float(hit[3]), 6))
wrong('b-ruin-target', 'fair', 0.6)
rec(F(171, 211) == (1 - F(2, 3) ** 3) / (1 - F(2, 3) ** 5), 'b-ruin-target: 171/211 exactly')
allow('b-ruin-target', 0.6, 171, 211)

w6 = [0.8, 1.7, 0.4, 2.3, 1.3]
lam = np.arange(0.01, 3, 0.000005)
ll = len(w6) * np.log(lam) - lam * sum(w6)
key('b-mle-rate', round(float(lam[ll.argmax()]), 4))
wrong('b-mle-rate', 'gave-mean', round(sum(w6) / 5, 4))
allow('b-mle-rate', *w6, 6.5)

se7 = F(12) / 8
key('b-interval-width', round(float(F(196, 100) * se7), 6))
wrong('b-interval-width', 'no-root', round(1.96 * 12 / 64, 4))
wrong('b-interval-width', 'no-se', round(1.96 * 12, 4))
allow('b-interval-width', 64, 12, 1.96, 1.5, 95)

z8 = 0.07 / (1.1 / math.sqrt(484))
key('b-pvalue-mean', round(2 * N01.cdf(-z8), 3))
wrong('b-pvalue-mean', 'one-sided', round(N01.cdf(-z8), 3))
allow('b-pvalue-mean', 484, 0.07, 1.1, 22, 0.05, round(z8, 2))

none = 1.0
for _ in range(40):
    none *= 0.95
key('b-forty-tests', round(1 - none, 4))
wrong('b-forty-tests', 'one-test', 0.05)
wrong('b-forty-tests', 'bonferroni', 0.05 / 40)
allow('b-forty-tests', 40, 5, 0.95, round(none, 4))

ols_t = code_py('b-ols-table', 0)
for k in range(0, len(ols_t), 3):
    ns = {}
    exec(ols_t[k]['setup'], {'np': np}, ns)
    X, y = ns['X'], ns['y']
    Q, R = np.linalg.qr(X)
    beta = np.linalg.solve(R, Q.T @ y)
    res = y - X @ beta
    n, p = X.shape
    Ri = np.linalg.inv(R)
    se = np.sqrt(res @ res / (n - p) * np.sum(Ri ** 2, axis=1))
    r2 = np.corrcoef(X @ beta, y)[0, 1] ** 2
    rec(np.allclose(beta, eval(ols_t[k]['expect']), rtol=1e-10) and np.allclose(se, eval(ols_t[k + 1]['expect']), rtol=1e-10)
        and math.isclose(r2, eval(ols_t[k + 2]['expect']), rel_tol=1e-10), f'b-ols-table: fit {k // 3 + 1} beta, se, r2 by QR')


def betacf(a, b, x):
    qab, qap, qam, c, d = a + b, a + 1, a - 1, 1.0, 1 - (a + b) * x / (a + 1)
    d = 1 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 / (1 + aa * d)
        c = 1 + aa / c
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 / (1 + aa * d)
        c = 1 + aa / c
        h *= d * c
    return h


def ibeta(a, b, x):
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    return math.exp(lb) * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - math.exp(lb) * betacf(b, a, 1 - x) / b


t10 = 0.42 / 0.15
p10 = ibeta(14, 0.5, 28 / (28 + t10 ** 2))
key('b-ols-table', round(t10, 4), part=1)
wrong('b-ols-table', 'inverse', round(0.15 / 0.42, 4), part=1)
q3 = ITEM['b-ols-table']['parts'][2]['question']
rec(f'{p10:.3f}' in q3, f'b-ols-table part 2: P>|t| {p10:.3f} by the incomplete beta')
correct_id('b-ols-table', 'a', part=2)
allow('b-ols-table', 30, 0.42, 0.15, round(t10, 1), 28, round(p10, 3), round(p10 * 100, 1), round(100 - p10 * 100, 1), 1e-9)

pv = 105 / math.exp(0.04 * 0.5)
key('b-parity-put', round(7.20 - (100 - pv), 6))
wrong('b-parity-put', 'no-discount', round(7.20 - 100 + 105, 4))
wrong('b-parity-put', 'sign-flip', round(7.20 + 100 - pv, 6))
allow('b-parity-put', 7.20, 100, 105, 6, 4, round(pv, 4), 0.02)


def replicate(S, Su, Sd, Vu, Vd, g):
    """hold delta shares and a bond that pay Vu and Vd next step; today it costs delta * S + bond"""
    delta = (Vu - Vd) / (Su - Sd)
    bond = (Vu - delta * Su) / g
    return delta * S + bond


S0 = 50
uu, ud, dd = S0 * 1.44, S0 * 1.2 * 0.9, S0 * 0.81
Vuu, Vud, Vdd = max(uu - 52, 0), max(ud - 52, 0), max(dd - 52, 0)
Vu = replicate(S0 * 1.2, uu, ud, Vuu, Vud, 1.02)
Vd = replicate(S0 * 0.9, ud, dd, Vud, Vdd, 1.02)
V0 = replicate(S0, S0 * 1.2, S0 * 0.9, Vu, Vd, 1.02)
key('b-two-step', round(V0, 6))
wrong('b-two-step', 'half', round((0.25 * Vuu + 0.5 * Vud + 0.25 * Vdd) / 1.02 ** 2, 6))
wrong('b-two-step', 'no-discount', round(V0 * 1.02 ** 2, 6))
allow('b-two-step', 50, 1.2, 0.9, 1.02, 52, 0.12, 0.3, 0.4, 72, 54, 40.50, 20, 0.16, 0.48, 1.0404)

key('b-book-orders', round(100.02 - 99.98, 6), part=0)
wrong('b-book-orders', 'mid', (100.02 + 99.98) / 2, part=0)
wrong('b-book-orders', 'second-level', round(100.03 - 99.97, 6), part=0)
need, cost = 500, 0.0
for px, sz in [(100.02, 200), (100.03, 400)]:
    take = min(need, sz)
    cost += take * px
    need -= take
key('b-book-orders', round(cost / 500, 6), part=1)
wrong('b-book-orders', 'top-only', 100.02, part=1)
wrong('b-book-orders', 'level-two', 100.03, part=1)
correct_id('b-book-orders', 'a', part=2)
allow('b-book-orders', 300, 99.98, 100.02, 200, 500, 99.97, 100.03, 400, 100.00, 0.02, 100)


def crr_sum(S, K, r, sig, T, n, call=True, div=0.0):
    dt = T / n
    u = math.exp(sig * math.sqrt(dt))
    d = math.exp(-sig * math.sqrt(dt))
    q = (math.exp((r - div) * dt) - d) / (u - d)
    tot = sum(math.comb(n, j) * q ** (n - j) * (1 - q) ** j * max((S * u ** (n - j) * d ** j - K) * (1 if call else -1), 0) for j in range(n + 1))
    return math.exp(-r * T) * tot


crr_t = code_py('b-crr-python')
for t in crr_t:
    S_, K_, r_, dv, sg, T_, n_ = eval(t['call'][len('crr_put'):])
    rec(math.isclose(crr_sum(S_, K_, r_, sg, T_, n_, call=False, div=dv), eval(t['expect']), rel_tol=1e-9, abs_tol=1e-15), f'b-crr-python: {t["call"]} by the binomial sum')
allow('b-crr-python', 400, 1e-9)

# ======================================================================== Paper C
it_c1 = 'c-price-file'
csv_t, vol_t, dd_t = code_py(it_c1, 0), code_py(it_c1, 1), code_py(it_c1, 2)
for t in csv_t:
    ns = {}
    exec(t['setup'], {}, ns)
    df = pd.read_csv(__import__('io').StringIO(ns['text']))
    c = df.sort_values('date')['close'].to_numpy()
    rec(np.allclose(np.diff(c) / c[:-1], eval(t['expect']), rtol=1e-12), f'{it_c1}: returns by NumPy diff')
for t in vol_t:
    v = np.array(eval(re.search(r'\[.*\]', t['call']).group(0)))
    rec(math.isclose(math.sqrt(np.sum((v - v.mean()) ** 2) / (len(v) - 1) * 252), eval(t['expect']), rel_tol=1e-12), f'{it_c1}: vol by NumPy')
for t in dd_t:
    pz = np.array(eval(re.search(r'\[.*\]', t['call']).group(0)), dtype=float)
    rec(math.isclose(float(np.max(1 - pz / np.maximum.accumulate(pz))), eval(t['expect']), abs_tol=1e-15), f'{it_c1}: drawdown by running maximum')
allow(it_c1, 252, 63.75, 85, 1e-9)

correct_id('c-log-axis', 'a')
allow('c-log-axis', 30, 2.50, 0.9, 20)
correct_id('c-broadcast-shape', 'a')

rows4 = [("rates", 120), ("fx", 30), ("credit", -15), ("rates", -40), ("credit", 210), ("fx", 90), ("rates", 65), ("credit", -60)]
df4 = pd.DataFrame(rows4, columns=['desk', 'pnl'])
g4 = df4.groupby('desk')['pnl'].sum()
key('c-desk-sum', int(g4.max()))
wrong('c-desk-sum', 'single-max', int(df4['pnl'].max()))
allow('c-desk-sum', *[x for _, x in rows4], *g4.tolist())

con = sqlite3.connect(':memory:')
con.execute('CREATE TABLE trades (id INTEGER, desk TEXT, qty INTEGER, px REAL)')
con.executemany('INSERT INTO trades VALUES (?, ?, ?, ?)',
                [(1, 'rates', 200, 10.5), (2, 'fx', 50, 20.0), (3, 'rates', 150, 10.0), (4, 'fx', 300, 2.5), (5, 'credit', 400, 1.25), (6, 'fx', 120, 5.0)])
sql = re.search(r'```sql\n(.*?)```', ITEM['c-sql-having']['prose'], re.S).group(1)
out = con.execute(sql).fetchall()
key('c-sql-having', len(out), part=0)
wrong('c-sql-having', 'no-having', len(con.execute(sql.replace('HAVING COUNT(*) >= 2\n', '')).fetchall()), part=0)
key('c-sql-having', out[1][1], part=1)
wrong('c-sql-having', 'no-where', con.execute(sql.replace('WHERE qty >= 100\n', '')).fetchall()[1][1], part=1)
wrong('c-sql-having', 'first-row', out[0][1], part=1)
allow('c-sql-having', 200, 10.5, 50, 20.0, 150, 10.0, 300, 2.5, 400, 1.25, 120, 5.0, 100)

order_check('c-git-branch', 5, 2)
allow('c-git-branch', 252)
correct_id('c-pytest-catch', 'a')
allow('c-pytest-catch', 100, 110, 0.1, round(10 / 110, 4))

tab = W('c-complexity-table')
rec(all('wrong' in row[1] for row in tab['rows']) and all(row[1]['wrong'][0]['id'] in ITEM['c-complexity-table']['feedback']['byKey'] for row in tab['rows']),
    'c-complexity-table: every slip id has a byKey line')


def combos(v, cs):
    if v == 0:
        return 1
    if not cs or v < 0:
        return 0
    return combos(v - cs[0], cs) + combos(v, cs[1:])


def seqs(v, memo={}):
    if v == 0:
        return 1
    if v < 0:
        return 0
    if v not in memo:
        memo[v] = sum(seqs(v - c) for c in (2, 5, 10))
    return memo[v]


key('c-coin-ways', combos(50, [10, 5, 2]))
wrong('c-coin-ways', 'ordered', seqs(50))
allow('c-coin-ways', 50)

cp_t = code_py('c-close-pairs')
for t in cp_t[:-1]:
    p_, d_ = eval(t['call'][len('count_close_pairs'):])
    rec(sum(1 for i in range(len(p_)) for j in range(i + 1, len(p_)) if p_[j] - p_[i] <= d_) == eval(t['expect']), f'c-close-pairs: {t["call"]} by brute force')
rec(3 * 200000 - 6 == eval(cp_t[-1]['expect']), 'c-close-pairs: 200,000 prices give 3n - 6 pairs')
allow('c-close-pairs', 200000)

wc = W('c-crr-cpp')
nt = len(wc['tests'])
rec(run_cpp(wc['solution'], wc['tests']) == nt, f'c-crr-cpp: the C++ solution passes all {nt} tests (g++)')
rec(run_cpp(wc['starter'], wc['tests']) < nt, 'c-crr-cpp: the starter fails a test')
for t in wc['tests']:
    rec(math.isclose(crr_sum(*t['args'][:6], call=t['args'][6]), t['expect'], rel_tol=1e-9), f'c-crr-cpp: {t["args"]} by the binomial sum')
rec(f'{nt} hidden tests' in wc['how'], 'c-crr-cpp: how states the test count')
allow('c-crr-cpp', 1000, 1e-9)

prog = re.search(r'```cpp\n(.*?)```', ITEM['c-by-reference']['prose'], re.S).group(1)
with tempfile.TemporaryDirectory() as td:
    open(os.path.join(td, 'p.cpp'), 'w').write(prog)
    subprocess.run(['g++', '-std=c++17', os.path.join(td, 'p.cpp'), '-o', os.path.join(td, 'p')], check=True)
    printed = subprocess.run([os.path.join(td, 'p')], capture_output=True, text=True).stdout.strip()
key('c-by-reference', float(printed))
wrong('c-by-reference', 'both-change', float(printed) + 1)
wrong('c-by-reference', 'neither', 300)
allow('c-by-reference', 100, 200, 210)


def worst(n):
    return 0 if n <= 0 else 1 + worst(n - 1 - (n - 1) // 2)


key('c-halvings', worst(4_000_000))
wrong('c-halvings', 'log-ten', len(str(4_000_000)) - 1)
allow('c-halvings', 4_000_000, 2 ** 21, 2 ** 22, 21, 22)

# ======================================================================== Paper D
n1 = 1
while not all(F(1, k + 1) < F(4, 1000) for k in range(n1, n1 + 2000)):
    n1 += 1
key('d-eps-n', n1)
wrong('d-eps-n', 'non-strict', n1 - 1)
allow('d-eps-n', 0.004, 250)

correct_id('d-which-converges', 'a')
part_sums = [sum(4 ** k / math.factorial(k) for k in range(1, n + 1)) for n in (20, 60)]
rec(abs(part_sums[1] - (math.e ** 4 - 1)) < 1e-9, 'd-which-converges: partial sums reach e^4 - 1')
allow('d-which-converges', 0.2, 0.5)

key('d-delta-square', float(F(7, 100) / 7))
wrong('d-delta-square', 'used-six', round(0.07 / 6, 6))
rec(max(abs((3 + s) ** 2 - 9) for s in np.linspace(-0.01, 0.01, 2001)) <= 0.07, 'd-delta-square: delta 0.01 keeps |x^2 - 9| within 0.07')
allow('d-delta-square', 0.07)

lo, hi = 1.0, 4.0
fm = lambda x: x ** 3 + 4 * x
slope = (fm(4) - fm(1)) / 3
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if deriv(fm, mid) < slope else (lo, mid)
key('d-mvt-cubic', round(lo, 6))
allow('d-mvt-cubic', fm(4))
wrong('d-mvt-cubic', 'chord-slope', slope)
allow('d-mvt-cubic', slope)

order_check('d-rank-nullity-proof', 5, 2)
order_check('d-spectral-proof', 6, 2)

ip = lambda f, g: simpson(lambda x: f(x) * g(x), 0, 1)
key('d-poly-angle', round(ip(lambda x: 1, lambda x: x) / math.sqrt(ip(lambda x: 1, lambda x: 1) * ip(lambda x: x, lambda x: x)), 6))
wrong('d-poly-angle', 'coefficient-dot', float(np.dot([1, 0], [0, 1])))

Dm = np.zeros((5, 5))
for k in range(1, 5):
    Dm[k - 1, k] = k
key('d-diff-image', int(np.linalg.matrix_rank(Dm)))
wrong('d-diff-image', 'whole-space', 5)
wrong('d-diff-image', 'kernel', 5 - int(np.linalg.matrix_rank(Dm)))

correct_id('d-compact-set', 'a')
allow('d-compact-set', round(1 / math.sqrt(2), 4))

zp = 1
for _ in range(6):
    zp *= complex(-1, math.sqrt(3))
rec(abs(zp.imag) < 1e-9, 'd-complex-power: z^6 is real')
key('d-complex-power', round(zp.real, 6))
wrong('d-complex-power', 'mod-times', 2 * 6)
wrong('d-complex-power', 'unit-power', round((zp / abs(zp)).real, 9))
allow('d-complex-power', 64)

M = 4000
th = 2 * math.pi * np.arange(M) / M
zc = 2 * np.exp(1j * th)
integral = np.sum(np.cos(zc) / (zc - 1) * 2j * np.exp(1j * th)) * 2 * math.pi / M
rec(abs(integral.real) < 1e-9, 'd-residue: the integral is imaginary')
key('d-residue', round(float(integral.imag), 6))
wrong('d-residue', 'no-2pi', round(float(integral.imag) / (2 * math.pi), 6))
wrong('d-residue', 'pole-at-zero', round(2 * math.pi, 6))

P_ = lambda x, y: x * x * y
Q_ = lambda x, y: x + y * y
edges = [lambda t: (t, 0, 1, 0), lambda t: (1, t, 0, 1), lambda t: (1 - t, 1, -1, 0), lambda t: (0, 1 - t, 0, -1)]
line_int = sum(simpson(lambda t, e=e: P_(e(t)[0], e(t)[1]) * e(t)[2] + Q_(e(t)[0], e(t)[1]) * e(t)[3], 0, 1) for e in edges)
key('d-green-square', round(line_int, 6))
wrong('d-green-square', 'sign', round(-line_int, 6))
wrong('d-green-square', 'dropped-p', simpson(lambda x: 1, 0, 1))


def fine_ode(T, m=20000):
    y, v, h = 1.0, 0.0, T / m
    f = lambda y, v: (v, -4 * v - 13 * y)
    for _ in range(m):
        k1 = f(y, v)
        k2 = f(y + h / 2 * k1[0], v + h / 2 * k1[1])
        k3 = f(y + h / 2 * k2[0], v + h / 2 * k2[1])
        k4 = f(y + h * k3[0], v + h * k3[1])
        y += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        v += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return y


key('d-damped-value', round(fine_ode(1.0), 6))
wrong('d-damped-value', 'no-sine', round(math.exp(-2) * math.cos(3), 6))
allow('d-damped-value', 13)

rk_t = code_py('d-rk4-rate')
closed = {1: 0.04 - 0.03 * math.exp(-3), 2: math.e, 3: math.exp(-2.25)}
for k, v in closed.items():
    rec(abs(eval(rk_t[k]['expect']) - v) < 1e-9, f'd-rk4-rate test {k + 1}: expect is the closed form')
rec(abs(sum(1 / math.factorial(k) for k in range(5)) - eval(rk_t[0]['expect'])) < 1e-12, 'd-rk4-rate test 1: one RK4 step of y\' = y is 1 + 1 + 1/2 + 1/6 + 1/24')
rec(abs(eval(rk_t[4]['expect']) - 4.0) < 1e-12, 'd-rk4-rate test 5: RK4 integrates y\' = t exactly, (9 - 1) / 2')
eul = 0.01
for _ in range(20):
    eul += 0.1 * 1.5 * (0.04 - eul)
gap = closed[1] - eul
rec(abs(abs(gap) - 0.0003) < 0.00005, f'd-rk4-rate: Euler misses by {gap:.5f}, about 0.0003')
allow('d-rk4-rate', 1.5, 0.04, 0.01, 0.03, round(closed[1], 4), 0.0003, 5e-05, 1e-9, 20, 24)


def laplace(s):
    return simpson(lambda t: math.exp(-(s - 2) * t) * math.sin(3 * t), 0, 40, 40000)


expr_check('d-laplace-shift', laplace, 's', [3.0, 4.5, 6.0], ['no-shift', 'cosine'])
allow('d-laplace-shift', 13)

# ---------------------------------------------------------------- every numeric wrong was asserted, every paper is sized
for iid, it in ITEM.items():
    for k, w in ([(None, it['widget'])] if 'widget' in it else [(i, p['widget']) for i, p in enumerate(it['parts'])]):
        if w['kind'] == 'numeric':
            asserted = [v for v in ALLOW.get(iid, [])]
            for x in w.get('wrong', []):
                rec(any(abs(x['value'] - a) <= max(x['tol']['abs'] / 10, 1e-9) for a in asserted), f'{iid} wrong "{x["id"]}" asserted by route B')
for p in doc['parts']:
    if p['kind'] == 'paper':
        n = len(p['items']) + sum(d['n'] for d in p.get('draw', []))
        rec(15 <= n <= 25, f'{p["id"]}: {n} items (15 to 25)')
        pace = sum(it['pace'] for it in p['items']) + {'prob-stats-finance': 7 * 180, 'programming': 1800 + 1500}.get(p['id'], 0)
        rec(p['minutes'] * 60 >= pace, f'{p["id"]}: {p["minutes"]} min covers the pace {pace} s')
topics = {'1.1': ['c-price-file', 'c-log-axis'], '1.2': ['c-sql-having', 'c-git-branch', 'c-pytest-catch'], '1.3': ['a-desk-profit', 'a-lagrange-product'],
          '1.4': ['a-ls-pca-code', 'a-singular'], '1.5': ['b-fraud-flag', 'b-many-bets'], '1.6': ['b-ols-table', 'b-pvalue-mean'],
          '1.7': ['b-book-orders', 'b-parity-put', 'b-crr-python'], '1.8': ['c-coin-ways', 'c-close-pairs'], '1.9': ['c-crr-cpp', 'c-by-reference'],
          '1.10': ['d-rank-nullity-proof', 'd-spectral-proof', 'd-eps-n'], '1.11': ['d-rk4-rate', 'd-residue', 'd-green-square']}
CDIR = os.path.join(ROOT, 'app', 'content')
cur = json.load(open(os.path.join(CDIR, 'curriculum.json')))
skill_topic = {}
for st in cur['stages']:
    for tp in st['topics']:
        for c in tp['courses']:
            for s in json.load(open(os.path.join(CDIR, 'courses', c, 'course.json')))['skills']:
                skill_topic[s] = tp['id']
for tp, iids in topics.items():
    rec(all(skill_topic[ITEM[i]['skills'][0]] == tp for i in iids), f'topic {tp}: auto items {iids} carry its skills')
rec(sorted({skill_topic[s] for it in ITEM.values() for s in it['skills']}) == sorted(topics), 'every topic 1.1 to 1.11 has an item, and no other topic')

# drawn pools hold at least twice n
for p in doc['parts']:
    for d in p.get('draw', []):
        src, name = d['from'].split('/')
        lo_, hi_ = d['difficulty']
        if src == 'bank':
            pool = [it for f in glob.glob(os.path.join(CDIR, 'bank', f'{name}-*.json')) for it in json.load(open(f))['items']
                    if it['tags'][0] in d['tags'] and lo_ <= it['difficulty'] <= hi_]
        else:
            pool = [x for f in glob.glob(os.path.join(CDIR, 'drills', f'{name}-*.json')) for x in [json.load(open(f))] if lo_ <= x['difficulty'] <= hi_]
        rec(len(pool) >= 2 * d['n'], f'{p["id"]} draw {d["from"]} {d.get("tags", "")}: pool {len(pool)} >= 2n = {2 * d["n"]}')

# ---------------------------------------------------------------- every number in every learner-visible string
SKIP = {'id', 'tags', 'kind', 'layout', 'answer', 'tex', 'keyboard', 'starter', 'solution', 'tests', 'examples', 'skills', 'placeholder'}


def strings(o, k=None):
    if isinstance(o, str):
        if k not in SKIP:
            yield o
    elif isinstance(o, dict):
        for kk, v in o.items():
            if kk not in SKIP:
                yield from strings(v, kk)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, k)


def tokens(s):
    s = re.sub(r'```.*?```', ' ', s, flags=re.S)          # printed code is read by its own checks (g++, sqlite3)
    s = _FRAC.sub(lambda m: f' {m.group(1) or m.group(3)} {m.group(2) or m.group(4)} ', s)
    for m in _NUM.finditer(normalise(s)):
        t = m.group(0).rstrip('.')
        yield abs(float(t)), (len(t.split('.')[1]) if '.' in t and 'e' not in t.lower() else 0), t


for iid, it in ITEM.items():
    vals = [abs(v) for v in ALLOW.get(iid, [])]
    bad = []
    for s in strings({k: v for k, v in it.items() if k not in ('difficulty', 'pace')}):
        for v, dec, t in tokens(s):
            if dec == 0 and v == int(v) and v <= 10:
                continue
            half = 0.5 * 10 ** -dec
            if not any(abs(v - a_) < half * (1 - 1e-9) + 1e-12 for a_ in vals):
                bad.append(t)
    rec(not bad, f'{iid}: every stated number matches route B or a given', f'unmatched {sorted(set(bad))}' if bad else '')

ex.check_wrongs()
ex.report()
