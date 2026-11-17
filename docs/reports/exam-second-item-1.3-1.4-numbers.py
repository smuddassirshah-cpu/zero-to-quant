"""Second auto items for one-item exam skills, topic-1.4 and topic-1.3 (session AG, docs/briefs/exam-second-item.md).

Run: <scratchpad>/venv/bin/python docs/reports/exam-second-item-1.3-1.4-numbers.py   (exit 0 when every check passes; NumPy)
Every key and wrong value of the eight new items is computed twice: route 1 by the working the item prints (exact fractions),
route 2 independently (NumPy: matrix_rank, svd, lstsq, inv, finite differences, brute-force remainder). The script then reads
both exam files and checks each key, each wrong value, the printed numbers, that every (exam, skill) pair from the report has
two auto items, and that no skill of either exam has fewer than two.
"""
import json, math, os, sys
from fractions import Fraction as F
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import _numbers  # noqa: E402

EX = os.path.join(HERE, '..', '..', 'app', 'content', 'exams')
docs = {e: json.load(open(os.path.join(EX, e + '.json'), encoding='utf8')) for e in ('topic-1.4', 'topic-1.3')}
items = {it['id']: it for d in docs.values() for it in d['items']}
fails, n = [], [0]


def check(ok, label):
    n[0] += 1
    print(('ok  ' if ok else 'BAD ') + label)
    if not ok:
        fails.append(label)


def close(a, b, t=1e-9):
    return abs(float(a) - float(b)) <= t


def numeric(iid, key, wrongs):
    w = items[iid]['widget']
    check(abs(w['answer'] - float(key)) <= w['tol']['abs'] + 1e-12, f'{iid} key {w["answer"]} = computed {float(key):.6g}')
    got = {x['id']: x for x in w['wrong']}
    check(set(got) == set(wrongs), f'{iid} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        g = got[k]
        check(abs(g['value'] - float(v)) <= g['tol']['abs'] + 1e-12, f'{iid} wrong {k} {g["value"]} = computed {float(v):.6g}')
        check(abs(g['value'] - w['answer']) > w['tol']['abs'] + g['tol']['abs'], f'{iid} wrong {k} outside the key band')
        check(k in items[iid]['feedback']['byKey'], f'{iid} byKey line for {k}')


def printed(iid, *vals):
    txt = json.dumps(items[iid], ensure_ascii=False)
    nums = _numbers(txt.replace('\\\\', '\\'))
    for v in vals:
        check(any(abs(x - v) <= 1e-9 * max(1, abs(v)) for x in nums), f'{iid} prints {v}')


# ---------------- topic-1.4 ----------------
# a-desk-lengths: |a + b|^2 = |a|^2 + 2 a.b + |b|^2
r1 = math.sqrt(5**2 + 2 * 28 + 12**2)
cos = 28 / (5 * 12)
ang = math.acos(cos)                                    # route 2: law of cosines with the angle between them
r2 = math.sqrt(5**2 + 12**2 + 2 * 5 * 12 * math.cos(ang))
check(close(r1, 15) and close(r2, 15, 1e-9), 'a-desk-lengths |a+b| = 15 both routes')
a = np.array([5.0, 0, 0]); b = np.array([12 * cos, 12 * math.sin(ang), 0])   # route 3: explicit vectors with those lengths and dot product
check(close(np.linalg.norm(a + b), 15, 1e-9), 'a-desk-lengths explicit vectors give 15')
numeric('a-desk-lengths', 15, {'add-lengths': 5 + 12, 'no-cross': math.sqrt(25 + 144), 'cross-once': math.sqrt(25 + 28 + 144)})
check(close(round(math.sqrt(197), 4), 14.0357), 'sqrt(197) = 14.0357 to 4 dp')
printed('a-desk-lengths', 5, 12, 28, 15, 225, 56, 144, 25, 13)

# a-undo-two-steps: g = (AB)^-1 p = B^-1 A^-1 p
Ai = np.array([[1, -1], [0, 2]], float); Bi = np.array([[3, 1], [1, 1]], float)
key = Bi @ Ai
A, B = np.linalg.inv(Ai), np.linalg.inv(Bi)
check(np.allclose(np.linalg.inv(A @ B), key) and np.allclose(key, [[3, -1], [1, 1]]), 'a-undo-two-steps (AB)^-1 = [[3,-1],[1,1]] both routes')
g = np.array([0.7, -1.3]); check(np.allclose(key @ (A @ (B @ g)), g), 'a-undo-two-steps recovers a test g')
w = items['a-undo-two-steps']['widget']
check(w['answer'].replace(' ', '') == '\\begin{pmatrix}3&-1\\\\1&1\\end{pmatrix}', 'a-undo-two-steps answer tex')
rev = Ai @ Bi; ent = Ai * Bi
check(np.allclose(rev, [[2, 0], [2, 2]]) and not np.allclose(rev, key), 'reversed slip = [[2,0],[2,2]], differs from key')
check(np.allclose(ent, [[3, -1], [0, 2]]) and not np.allclose(ent, key), 'entrywise slip = [[3,-1],[0,2]], differs from key')
wt = {x['id']: x['tex'].replace(' ', '') for x in w['wrong']}
check(wt == {'reversed': '\\begin{pmatrix}2&0\\\\2&2\\end{pmatrix}', 'entrywise': '\\begin{pmatrix}3&-1\\\\0&2\\end{pmatrix}'}, 'a-undo-two-steps wrong tex')
check(close(3 * (-1) + 1 * 2, -1), 'explain: 3(-1) + 1(2) = -1')

# a-reachable-k: elimination on [A | b], b = (3, k, 1)
Am = [[F(1), F(2), F(1)], [F(2), F(5), F(3)], [F(1), F(4), F(3)]]
def last_rhs(k, stale=False, add=False):
    r1, r2, r3 = [row[:] + [rhs] for row, rhs in zip(Am, [F(3), F(k), F(1)])]
    r2o = r2[:]
    r2 = [x - 2 * y for x, y in zip(r2, r1)]
    r3 = [x - y for x, y in zip(r3, r1)]
    m = r3[1] / r2[1]
    if stale:
        r3 = [x - m * y for x, y in zip(r3[:3], r2[:3])] + [r3[3] - m * r2o[3]]
    elif add:
        r3 = [x + m * y for x, y in zip(r3, r2)]
    else:
        r3 = [x - m * y for x, y in zip(r3, r2)]
    return r2, r3
r2, r3 = last_rhs(0)
check(r3[:3] == [0, 0, 0] and r2[:3] == [0, 1, 1], 'a-reachable-k: row 3 of U is zero, row 2 is (0, 1, 1)')
ks = [k for k in range(-20, 21) if last_rhs(k)[1][3] == 0]
An = np.array(Am, float)
ks2 = [k for k in range(-20, 21) if np.linalg.matrix_rank(np.column_stack([An, [3, k, 1]])) == np.linalg.matrix_rank(An)]
check(ks == [5] and ks2 == [5] and np.linalg.matrix_rank(An) == 2, 'a-reachable-k key 5 by elimination and by rank')
stale = [k for k in range(-20, 21) if last_rhs(k, stale=True)[1][3] == 0]
added = [k for k in range(-20, 21) if last_rhs(k, add=True)[1][3] == 0]
check(stale == [-1] and added == [7], f'slips: stale right side {stale}, added row {added}')
numeric('a-reachable-k', 5, {'stale-right': -1, 'added-row': 7})
check(np.allclose(3 * An[:, 0] + An[:, 1] - 2 * An[:, 2], [3, 5, 1]), 'b at k = 5 is 3 c1 + c2 - 2 c3')
check(not any(np.allclose(An[:, j], [3, 5, 1]) for j in range(3)), 'b is not a column of A')
check(last_rhs(0)[0][3] == -6 and last_rhs(0)[1][3] == 10, 'explain: rows (0,1,1 | k-6), (0,0,0 | 10-2k)')

# a-qr-solve
Q = np.array([[2, 2], [-1, 2], [2, -1]]) / 3; R = np.array([[2, -2], [0, 4]], float); bq = np.array([1, 5, 6], float)
check(np.allclose(Q.T @ Q, np.eye(2)), 'a-qr-solve Q has orthonormal columns')
qtb = Q.T @ bq
x = np.linalg.solve(R, qtb)
x2, *_ = np.linalg.lstsq(Q @ R, bq, rcond=None)           # route 2: lstsq on A = QR
check(np.allclose(qtb, [3, 2]) and np.allclose(x, [2, 1 / 2]) and np.allclose(x2, x), 'a-qr-solve Q^T b = (3, 2), x = (2, 1/2) both routes')
check(not np.allclose(Q @ R @ x, bq), 'a-qr-solve b is not in C(A), so this is a real least squares fit')
rawb = np.linalg.solve(R, bq[:2]); unsc = np.linalg.solve(R, 3 * qtb)
numeric('a-qr-solve', x[0], {'raw-b': rawb[0], 'no-back': qtb[0] / R[0, 0], 'unscaled': unsc[0]})
printed('a-qr-solve', 1, 5, 6, 3, 2)

# a-rank-one
Ar = np.array([[4, 9.5], [-1, 7], [10, 5]])
AtA = Ar.T @ Ar
lam, V = np.linalg.eigh(AtA)
v1 = V[:, 1] * np.sign(V[0, 1])
A1 = np.outer(Ar @ v1, v1)
U, s, Vt = np.linalg.svd(Ar)
A1b = s[0] * np.outer(U[:, 0], Vt[0])                    # route 2: NumPy SVD
check(np.allclose(AtA, [[117, 81], [81, 164.25]]) and np.allclose(lam, [56.25, 225]), 'a-rank-one A^T A and eigenvalues 225, 56.25')
check(np.allclose(s, [15, 7.5]) and np.allclose(v1, [0.6, 0.8]) and np.allclose(Ar @ v1, [10, 5, 10]), 'a-rank-one sigma = (15, 7.5), v1 = (0.6, 0.8), A v1 = (10, 5, 10)')
check(np.allclose(A1, A1b) and close(A1[0, 1], 8) and close(A1[0, 0], 6), 'a-rank-one A1 row 1 = (6, 8) both routes')
check(close(np.sum((Ar - A1) ** 2), 56.25) and close(np.sum(Ar ** 2), 281.25), 'a-rank-one error energy 56.25 of 281.25')
v2 = np.array([-0.8, 0.6]); piece2 = np.outer(Ar @ v2, v2)
numeric('a-rank-one', A1[0, 1], {'eigenvalue': 225 / 15 * A1[0, 1], 'second-piece': piece2[0, 1]})
printed('a-rank-one', 117, 81, 164.25, 225, 56.25, 15, 7.5, 0.6, 0.8, 10, 5, 6, 8, 281.25)

# ---------------- topic-1.3 ----------------
# c-trapezium
fv = [5, 4, 4.5, 6, 8]
T = sum((fv[i] + fv[i + 1]) / 2 for i in range(4))
L, Rr = sum(fv[:4]), sum(fv[1:])
check(close(T, 21) and close((L + Rr) / 2, 21) and close(np.trapezoid(fv, dx=1) if hasattr(np, 'trapezoid') else np.trapz(fv, dx=1), 21), 'c-trapezium T4 = 21 three ways')
numeric('c-trapezium', 21, {'left': L, 'right': Rr, 'all-full': sum(fv)})
printed('c-trapezium', 4.5, 4.25, 5.25, 7, 21, 19.5, 22.5)

# c-quotient-partial: f = x y^2 / (x + y), df/dy at (2, 1)
def fq(x, y): return x * y * y / (x + y)
X, Y = F(2), F(1)
dfy = (2 * X * Y * (X + Y) - X * Y * Y) / (X + Y) ** 2
h = 1e-6; fd = (fq(2, 1 + h) - fq(2, 1 - h)) / (2 * h)
dfx = (Y * Y * (X + Y) - X * Y * Y) / (X + Y) ** 2
check(dfy == F(10, 9) and close(fd, 10 / 9, 1e-8), 'c-quotient-partial df/dy = 10/9 by quotient rule and finite difference')
numeric('c-quotient-partial', F(10, 9), {'swapped': -F(10, 9), 'split': 2 * X * Y / 1, 'const-bottom': 2 * X * Y / (X + Y), 'wrong-variable': dfx})
check(close((fq(2 + h, 1) - fq(2 - h, 1)) / (2 * h), 1 / 9, 1e-8), 'wrong-variable value 1/9 confirmed by finite difference')
printed('c-quotient-partial', 12, 2, 9, 3)

# c-terms-needed: Lagrange bound e^0.3 * 0.3^(n+1)/(n+1)! < 1e-5
def bound(n, M=1.35): return M * 0.3 ** (n + 1) / math.factorial(n + 1)
nmin = min(n for n in range(20) if bound(n) < 1e-5)
nmin_e = min(n for n in range(20) if math.exp(0.3) * 0.3 ** (n + 1) / math.factorial(n + 1) < 1e-5)
true_err = {n: max(abs(math.exp(x) - sum(x ** k / math.factorial(k) for k in range(n + 1))) for x in np.linspace(-0.3, 0.3, 601)) for n in range(3, 7)}
check(nmin == 5 and nmin_e == 5 and math.exp(0.3) < 1.35, 'c-terms-needed n = 5 with 1.35 and with e^0.3')
check(true_err[4] > 1e-5 and true_err[5] < 1e-5, f'true worst error {true_err[4]:.3g} at n=4, {true_err[5]:.3g} at n=5: the bound is not loose here')
last = min(n for n in range(20) if 1.35 * 0.3 ** n / math.factorial(n) < 1e-5)
nofact = min(n for n in range(30) if 1.35 * 0.3 ** (n + 1) < 1e-5)
numeric('c-terms-needed', nmin, {'last-kept': last, 'no-factorial': nofact})
check(f'{bound(4):.1e}' == '2.7e-05' and f'{bound(5):.1e}' == '1.4e-06', f'printed bounds 2.7e-5 ({bound(4):.4g}) and 1.4e-6 ({bound(5):.4g})')

# ---------------- coverage ----------------
PAIRS = {'topic-1.4': ['eg-svd', 'gx-elim', 'gx-spaces', 'la-inverse', 'la-product', 'la-vectors', 'ls-qr'],
         'topic-1.3': ['in-area', 'lm-rules', 'mv-partial', 'ty-converge']}
for e, d in docs.items():
    auto = [it for it in d['items'] if it.get('kind') != 'longform' and (it.get('widget') or {}).get('kind') != 'longform']
    cnt = {s: sum(s in it['skills'] for it in auto) for s in d['skills']}
    check(len(d['items']) == 30 and d['minutes'] == 60, f'{e} still 30 items, 60 minutes')
    for s in PAIRS[e]:
        check(cnt[s] >= 2, f'{e} pair {s}: {cnt[s]} auto items')
    low = [s for s, c in cnt.items() if c < 2]
    check(not low, f'{e} no skill under two auto items {low}')
for gone in ['a-rank-null', 'a-char-poly', 'a-beta', 'a-det-inverse', 'a-pca-share', 'c-log-return', 'c-pnl-peak', 'c-double']:
    check(gone not in items, f'removed {gone}')

print(f'{n[0] - len(fails)} of {n[0]} checks passed')
sys.exit(1 if fails else 0)
