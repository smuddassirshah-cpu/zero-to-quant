#!/usr/bin/env python3
"""Second read of the eight new items of topic-1.4 and topic-1.3 (exam second item, NAME 1.3-1.4).

Every key, `wrong` value and printed number is recomputed by a route the author's
script does not use: explicit vectors, numpy solves, the SVD, sympy derivatives,
exact fractions. Prints `ok` or `FINDING` per check and always exits 0.
The last block recomputes the replacement numbers the review proposes.
"""
import json
import math
import os
import re
from fractions import Fraction as F

import numpy as np
import sympy as sp

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CONTENT = os.path.join(ROOT, 'app', 'content')
checks = findings = 0


def check(name, cond, detail=''):
    global checks, findings
    checks += 1
    if cond:
        print('ok      ', name)
    else:
        findings += 1
        print('FINDING ', name, detail)


def load(rel):
    with open(os.path.join(CONTENT, rel), encoding='utf-8') as fh:
        return json.load(fh)


EXAMS = {e: load(f'exams/{e}.json') for e in ('topic-1.4', 'topic-1.3')}


def item(exam, iid):
    for it in EXAMS[exam]['items']:
        if it['id'] == iid:
            return it
    raise KeyError(iid)


def wrong(it):
    return {w['id']: w for w in it['widget'].get('wrong', [])}


def near(a, b, tol=1e-9):
    return abs(a - b) <= tol


def bands(name, it, places_typed=None):
    """Key band holds the stored key and refuses every wrong value; wrong bands do not overlap."""
    w = it['widget']
    key, tol = w['answer'], w['tol']['abs']
    ws = w.get('wrong', [])
    for x in ws:
        check(f'{name}: key band refuses wrong {x["id"]}', abs(x['value'] - key) > tol + x['tol']['abs'])
    for i, x in enumerate(ws):
        for y in ws[i + 1:]:
            check(f'{name}: wrong bands {x["id"]}/{y["id"]} apart',
                  abs(x['value'] - y['value']) > x['tol']['abs'] + y['tol']['abs'])


def text_of(it):
    return json.dumps(it, ensure_ascii=False)


# ---------------------------------------------------------------- topic-1.4
# a-desk-lengths: build real five-day vectors with the stated lengths and dot product.
it = item('topic-1.4', 'a-desk-lengths')
a = np.array([5.0, 0, 0, 0, 0])
b1 = 28 / 5
b = np.array([b1, math.sqrt(144 - b1 * b1), 0, 0, 0])
check('desk: such vectors exist (Cauchy-Schwarz 28 <= 60)', 28 <= 5 * 12 and near(np.linalg.norm(b), 12) and near(a @ b, 28))
check('desk: key |a+b| = 15', near(np.linalg.norm(a + b), it['widget']['answer']) and it['widget']['answer'] == 15)
w = wrong(it)
check('desk: add-lengths 17', w['add-lengths']['value'] == 5 + 12)
check('desk: no-cross 13', near(math.hypot(5, 12), w['no-cross']['value']))
check('desk: cross-once sqrt(197) = 14.0357', round(math.sqrt(25 + 28 + 144), 4) == w['cross-once']['value'])
check('desk: printed 25 + 2(28) + 144 = 225 and 25 + 56 + 144', 25 + 2 * 28 + 144 == 225 and '25 + 56 + 144 = 225' in text_of(it))
bands('desk', it)
check('desk: cross-once slip typed to 2 places (14.04) meets its band',
      abs(round(math.sqrt(197), 2) - w['cross-once']['value']) <= w['cross-once']['tol']['abs'],
      f"14.04 is {abs(14.04 - 14.0357):.4f} from 14.0357, band {w['cross-once']['tol']['abs']}; the question asks no places")

# a-undo-two-steps: invert the stored inverses, push a shock through, recover it.
it = item('topic-1.4', 'a-undo-two-steps')
Ainv = np.array([[1.0, -1], [0, 2]])
Binv = np.array([[3.0, 1], [1, 1]])
A, B = np.linalg.inv(Ainv), np.linalg.inv(Binv)
g = np.array([0.7, -1.3])
p = A @ (B @ g)
key = np.array([[3.0, -1], [1, 1]])
check('undo: key recovers g from p', np.allclose(key @ p, g))
check('undo: key is inv(AB)', np.allclose(np.linalg.inv(A @ B), key))
check('undo: key text', re.sub(r'\s', '', it['widget']['answer']) == r'\begin{pmatrix}3&-1\\1&1\end{pmatrix}')
check('undo: accept forms are the key', all(json.loads(s) == [[3, -1], [1, 1]] for s in it['widget']['accept']))
wr = {x['id']: re.sub(r'\s', '', x['tex']) for x in it['widget']['wrong']}
rev = Ainv @ Binv
check('undo: reversed A^-1 B^-1 = [[2,0],[2,2]]', np.allclose(rev, [[2, 0], [2, 2]]) and wr['reversed'] == r'\begin{pmatrix}2&0\\2&2\end{pmatrix}')
check('undo: reversed does not recover g', not np.allclose(rev @ p, g))
ent = Binv * Ainv
check('undo: entrywise = [[3,-1],[0,2]]', np.allclose(ent, [[3, -1], [0, 2]]) and wr['entrywise'] == r'\begin{pmatrix}3&-1\\0&2\end{pmatrix}')
check('undo: three matrices distinct', not np.allclose(rev, key) and not np.allclose(ent, key) and not np.allclose(ent, rev))
check('undo: explain row 1 gives 3 and 3(-1) + 1(2) = -1, row 2 gives 1 and 1',
      list((Binv @ Ainv)[0]) == [3, -1] and list((Binv @ Ainv)[1]) == [1, 1])

# a-reachable-k: rank test with sympy, not row steps.
it = item('topic-1.4', 'a-reachable-k')
k = sp.symbols('k')
A = sp.Matrix([[1, 2, 1], [2, 5, 3], [1, 4, 3]])
check('reach: rank A = 2', A.rank() == 2)
n = A.T.nullspace()[0]  # left null vector: b is reachable iff n . b = 0
cond = sp.expand((n.T * sp.Matrix([3, k, 1]))[0])
sol = sp.solve(cond, k)
check('reach: key k = 5 (left-null-vector test)', sol == [5] and it['widget']['answer'] == 5)
check('reach: k = 5 solvable, k = 4, 6 not',
      A.row_join(sp.Matrix([3, 5, 1])).rank() == 2 and all(A.row_join(sp.Matrix([3, v, 1])).rank() == 3 for v in (4, 6)))
w = wrong(it)
check('reach: stale-right -2 - 2k = 0 gives -1', sp.solve(-2 - 2 * k, k) == [w['stale-right']['value']])
check('reach: added-row -2 + 2(k - 6) = 0 gives 7', sp.solve(-2 + 2 * (k - 6), k) == [w['added-row']['value']])
check('reach: printed rows (0,1,1|k-6), (0,2,2|-2), (0,0,0|10-2k)',
      list(A.row(1) - 2 * A.row(0)) == [0, 1, 1] and list(A.row(2) - A.row(0)) == [0, 2, 2]
      and sp.expand(-2 - 2 * (k - 6)) == 10 - 2 * k and list(3 * A.col(0) + A.col(1) - 2 * A.col(2)) == [3, 5, 1])
bands('reach', it)
col_hit = [j + 1 for j in range(3) if list(A.col(j))[0] == 3 and list(A.col(j))[2] == 1]
check('reach: b cannot be read off a column of A without eliminating', not col_hit,
      f'b = (3, k, 1) matches column {col_hit} in its two known entries; k = 5 is read by eye (gx-elim not needed)')

# a-qr-solve: least squares on A = QR by numpy, not by back substitution.
it = item('topic-1.4', 'a-qr-solve')
Q = np.array([[2.0, 2], [-1, 2], [2, -1]]) / 3
R = np.array([[2.0, -2], [0, 4]])
bq = np.array([1.0, 5, 6])
A = Q @ R
check('qr: Q has orthonormal columns', np.allclose(Q.T @ Q, np.eye(2)))
xh = np.linalg.lstsq(A, bq, rcond=None)[0]
check('qr: key x1 = 2 (lstsq on A = QR)', near(xh[0], it['widget']['answer'], 1e-9) and near(xh[1], 1 / 2, 1e-9))
check('qr: printed Q^T b = (3, 2)', np.allclose(Q.T @ bq, [3, 2]))
w = wrong(it)
check('qr: raw-b 1.75', near(np.linalg.solve(R, bq[:2])[0], w['raw-b']['value']))
check('qr: no-back 3/2 = 1.5', near(3 / 2, w['no-back']['value']))
check('qr: unscaled 6', near(np.linalg.solve(R, 3 * Q.T @ bq)[0], w['unscaled']['value']))
bands('qr', it)
Qn, Rn = np.linalg.qr(A)
check('qr: prose claims no numpy output', 'np.linalg.qr' not in it['prose'] and 'A QR factorisation of' in it['prose'] and np.allclose(abs(Rn), abs(R)),
      f'numpy returns R = {np.round(Rn, 4).tolist()}, first column of Q = {np.round(Qn[:, 0], 4).tolist()}')
l8 = load('courses/least-squares/l8-qr.json')
l8_text = json.dumps(l8['screens'][2], ensure_ascii=False) + json.dumps(l8['screens'][4], ensure_ascii=False)
lesson_R = '3\\\\mathbf{q}_1 + 3\\\\mathbf{q}_2' in l8_text and '= 3\\\\mathbf{q}_1$' in l8_text
check('qr: R differs from the R of least-squares/l8-qr', not (lesson_R and np.allclose(R, [[3, 3], [0, 3]])) and not np.allclose(bq, [2, 1, 7]),
      'l8-qr screens[2] builds R = [[3, 3], [0, 3]] (a1 = 3q1, a2 = 3q1 + 3q2) and screens[4] fits b = (2, 1, 7); the item prints the same R with b = (4, 1, 7)')
check('qr: no-back slip is exact', w['no-back']['value'] == 1.5)

# a-rank-one: numpy SVD.
it = item('topic-1.4', 'a-rank-one')
A = np.array([[4, 9.5], [-1, 7], [10, 5]])
U, s, Vt = np.linalg.svd(A, full_matrices=False)
A1 = s[0] * np.outer(U[:, 0], Vt[0])
A2 = s[1] * np.outer(U[:, 1], Vt[1])
check('rank1: key entry (1,2) of A1 = 8', near(A1[0, 1], it['widget']['answer'], 1e-9))
check('rank1: sigma = 15, 7.5', np.allclose(s, [15, 7.5]))
check('rank1: A^T A = [[117, 81], [81, 164.25]], eigenvalues 225 and 56.25',
      np.allclose(A.T @ A, [[117, 81], [81, 164.25]]) and np.allclose(sorted(np.linalg.eigvalsh(A.T @ A)), [56.25, 225]))
v1 = Vt[0] * np.sign(Vt[0, 0])
check('rank1: v1 = (0.6, 0.8), A v1 = (10, 5, 10), row 1 of A1 = (6, 8)',
      np.allclose(v1, [0.6, 0.8]) and np.allclose(A @ v1, [10, 5, 10]) and np.allclose(A1[0], [6, 8]))
w = wrong(it)
check('rank1: eigenvalue slip 225 u1 v1^T -> 120', near(s[0] ** 2 * U[0, 0] * Vt[0, 1], w['eigenvalue']['value'], 1e-9))
check('rank1: second piece entry 1.5, v2 = (-0.8, 0.6)',
      near(A2[0, 1], w['second-piece']['value'], 1e-9) and np.allclose(abs(Vt[1]), [0.8, 0.6]))
check('rank1: error energy 56.25 of total 281.25', near(((A - A1) ** 2).sum(), 56.25, 1e-9) and near((A ** 2).sum(), 281.25, 1e-9))
bands('rank1', it)

# ---------------------------------------------------------------- topic-1.3
# c-trapezium: strip by strip in exact fractions, and numpy.
it = item('topic-1.3', 'c-trapezium')
ys = [F(5), F(4), F(9, 2), F(6), F(8)]
strips = [(ys[i] + ys[i + 1]) / 2 for i in range(4)]
check('trap: key 21', sum(strips) == it['widget']['answer'] == 21)
check('trap: numpy trapezoid agrees', near(float(np.trapezoid([float(y) for y in ys], dx=1.0)), 21))
check('trap: printed strips 4.5, 4.25, 5.25, 7', strips == [F(9, 2), F(17, 4), F(21, 4), F(7)])
w = wrong(it)
check('trap: left 19.5, right 22.5, all-full 27.5',
      (sum(ys[:4]), sum(ys[1:]), sum(ys)) == (F(w['left']['value']), F(w['right']['value']), F(w['all-full']['value'])))
check('trap: key is the mean of left and right', (sum(ys[:4]) + sum(ys[1:])) / 2 == 21)
bands('trap', it)

# c-quotient-partial: sympy, and a central difference.
it = item('topic-1.3', 'c-quotient-partial')
x, y = sp.symbols('x y')
f = x * y ** 2 / (x + y)
at = {x: 2, y: 1}
fy = sp.diff(f, y).subs(at)
check('quot: key 10/9', fy == sp.Rational(10, 9) and round(float(fy), 4) == it['widget']['answer'])
h = 1e-6
num = (float(f.subs({x: 2, y: 1 + h})) - float(f.subs({x: 2, y: 1 - h}))) / (2 * h)
check('quot: central difference agrees', near(num, 10 / 9, 1e-7))
w = wrong(it)
check('quot: swapped -10/9', w['swapped']['value'] == -round(10 / 9, 4))
check('quot: split 2xy / 1 = 4', (sp.diff(x * y ** 2, y) / sp.diff(x + y, y)).subs(at) == w['split']['value'])
check('quot: const-bottom 2xy/(x+y) = 4/3', round(float((2 * x * y / (x + y)).subs(at)), 4) == w['const-bottom']['value'])
check('quot: wrong-variable f_x = 1/9', sp.diff(f, x).subs(at) == sp.Rational(1, 9) and w['wrong-variable']['value'] == 0.1111)
check('quot: printed (12 - 2)/9 and (4 x 3 - 2)/9', (2 * 2 * 1 * 3, 2 * 1 ** 2, 3 ** 2) == (12, 2, 9))
bands('quot', it)
tolk = it['widget']['tol']['abs']
asks_places = bool(re.search(r'place|dp|nearest', it['question'], re.I))
check('quot: the key typed to 2 places (1.11) is accepted, or the question asks for places',
      abs(1.11 - it['widget']['answer']) <= tolk or asks_places,
      f'question: "Give a fraction or a decimal."; 1.11 is {abs(1.11 - 1.1111):.4f} from 1.1111, band {tolk}')

# c-terms-needed: exact fractions for the bound, and the true worst error.
it = item('topic-1.3', 'c-terms-needed')


def bound(n, M=F(135, 100)):
    return M * F(3, 10) ** (n + 1) / math.factorial(n + 1)


first = next(n for n in range(0, 30) if bound(n) < F(1, 10 ** 5))
check('terms: key 5', first == it['widget']['answer'] == 5)
check('terms: e^0.3 < 1.35', math.exp(0.3) < 1.35)
check('terms: printed bounds 2.7e-5 at n = 4, 1.4e-6 at n = 5',
      f'{float(bound(4)):.1e}' == '2.7e-05' and f'{float(bound(5)):.1e}' == '1.4e-06')


def true_err(n):
    xs = np.linspace(-0.3, 0.3, 6001)
    T = sum(xs ** j / math.factorial(j) for j in range(n + 1))
    return float(np.max(np.abs(np.exp(xs) - T)))


check('terms: T4 really misses 1e-5 and T5 meets it (the key is not an artefact of the bound)',
      true_err(4) > 1e-5 > true_err(5), f'{true_err(4):.2e}, {true_err(5):.2e}')
w = wrong(it)
last = next(n for n in range(0, 30) if F(3, 10) ** n / math.factorial(n) < F(1, 10 ** 5))
check('terms: last-kept 6 (and T5 has 6 terms)', last == w['last-kept']['value'] == 6)
nofact = next(n for n in range(0, 60) if F(135, 100) * F(3, 10) ** (n + 1) < F(1, 10 ** 5))
check('terms: no-factorial 9', nofact == w['no-factorial']['value'] == 9)
bands('terms', it)
hw2 = load('courses/taylor/homework-2.json')
src = next(u for u in hw2['items'] if u['id'] == 'h2-terms-for-e')
check('terms: story differs from taylor/homework-2 h2-terms-for-e',
      'library' not in it['prose'] and 'microcontroller' in it['prose'],
      f'homework: "{src["prose"]} {src["question"]}"')

# ---------------------------------------------------------------- skill counts
REMOVED = {'topic-1.4': {'a-rank-null': ['gx-rank'], 'a-char-poly': ['eg-eigen'], 'a-beta': ['ls-fit'],
                         'a-det-inverse': ['gx-det'], 'a-pca-share': ['eg-pca']},
           'topic-1.3': {'c-log-return': ['ty-finance'], 'c-pnl-peak': ['in-apply'], 'c-double': ['mv-integrals']}}
PAIRS = {'topic-1.4': ['la-vectors', 'la-product', 'la-inverse', 'gx-elim', 'gx-spaces', 'ls-qr', 'eg-svd'],
         'topic-1.3': ['in-area', 'lm-rules', 'mv-partial', 'ty-converge']}
for e, d in EXAMS.items():
    cnt = {}
    for u in d['items']:
        if u.get('kind') == 'longform':
            continue
        for s in u.get('skills', []):
            cnt[s] = cnt.get(s, 0) + 1
    ids = {u['id'] for u in d['items']}
    check(f'{e}: 30 items, 60 minutes', len(d['items']) == 30 and d['minutes'] == 60)
    check(f'{e}: every listed pair has two auto items', all(cnt.get(s, 0) >= 2 for s in PAIRS[e]), str({s: cnt.get(s, 0) for s in PAIRS[e]}))
    check(f'{e}: no skill of the exam under two auto items', all(cnt.get(s, 0) >= 2 for s in d['skills']),
          str({s: cnt.get(s, 0) for s in d['skills'] if cnt.get(s, 0) < 2}))
    for rid, sk in REMOVED[e].items():
        check(f'{e}: removed {rid} is gone and {sk} keep two auto items', rid not in ids and all(cnt.get(s, 0) >= 2 for s in sk))

# ---------------------------------------------------------------- numbers of the proposed fixes
print('--- proposed replacements (review findings 1 and 2) ---')
# Finding 1: a-reachable-k with b = (3, k, 1).
A = sp.Matrix([[1, 2, 1], [2, 5, 3], [1, 4, 3]])
cond = sp.expand((A.T.nullspace()[0].T * sp.Matrix([3, k, 1]))[0])
check('fix reach: b = (3, k, 1) gives k = 5', sp.solve(cond, k) == [5])
check('fix reach: rows (0,1,1|k-6), (0,2,2|-2), (0,0,0|10-2k)', sp.expand((1 - 3) - 2 * (k - 6)) == 10 - 2 * k)
check('fix reach: stale-right -2 - 2k = 0 gives -1; added-row -2 + 2(k - 6) = 0 gives 7',
      sp.solve(-2 - 2 * k, k) == [-1] and sp.solve(-2 + 2 * (k - 6), k) == [7])
check('fix reach: (3, 5, 1) = 3 c1 + c2 - 2 c3 and matches no column', list(3 * A.col(0) + A.col(1) - 2 * A.col(2)) == [3, 5, 1]
      and all(list(A.col(j)) != [3, 5, 1] for j in range(3)) and all((A.col(j)[0], A.col(j)[2]) != (3, 1) for j in range(3)))
# Finding 2: a-qr-solve with R = [[2, -2], [0, 4]] and b = (1, 5, 6).
R2 = np.array([[2.0, -2], [0, 4]])
b2 = np.array([1.0, 5, 6])
x2 = np.linalg.lstsq(Q @ R2, b2, rcond=None)[0]
check('fix qr: Q^T b = (3, 2), x = (2, 0.5)', np.allclose(Q.T @ b2, [3, 2]) and np.allclose(x2, [2, 0.5]))
check('fix qr: raw-b 1.75, no-back 1.5, unscaled 6; the key is no entry of b',
      near(np.linalg.solve(R2, b2[:2])[0], 1.75) and near(3 / 2, 1.5) and near(np.linalg.solve(R2, 3 * Q.T @ b2)[0], 6) and 2 not in b2)
ls_text = ''.join(open(os.path.join(CONTENT, 'courses', 'least-squares', fn), encoding='utf-8').read()
                  for fn in sorted(os.listdir(os.path.join(CONTENT, 'courses', 'least-squares'))))
ex_text = json.dumps([u for u in EXAMS['topic-1.4']['items'] if u['id'] != 'a-qr-solve'])
check('fix qr: b = (1, 5, 6) and a matrix starting 2 & -2 unused in least-squares and topic-1.4',
      '(1, 5, 6)' not in ls_text + ex_text and not re.search(r'pmatrix\}\s*2\s*&\s*-2', ls_text + ex_text))
# Finding 4: cross-once band of half a unit at 2 places.
check('fix desk: band 0.005 on 14.0357 takes 14.04 and stays clear of 15, 13, 17',
      abs(14.04 - 14.0357) <= 0.005 and all(abs(v - 14.0357) > 0.0055 for v in (15, 13, 17)))

print(f'{checks} checks, {findings} FINDING lines')
