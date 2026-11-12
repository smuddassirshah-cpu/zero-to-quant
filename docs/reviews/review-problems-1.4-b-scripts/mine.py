"""Second read, elimination and least-squares problems-1 to -3: the reader's own keys, slips and stated numbers.

Imports nothing from the authors' scripts. Every matrix and vector is typed from the item's prose; every key is
computed here (sympy exact, NumPy as a second route where one exists) and then compared with the stored answer;
every `wrong` value is rebuilt from the slip its feedback line names. A CLAIM line is a statement the reader
holds to be false or loose (printed, not a failure).

Run from the repo root:  <venv>/bin/python docs/reviews/review-problems-1.4-b-scripts/mine.py
"""
import json
import re
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp

R = sp.Rational
M = sp.Matrix
k = sp.Symbol('k')
checks = fails = 0
claims = []


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


def claim(text):
    claims.append(text)


def load(course, n):
    return {it['id']: it for it in json.load(open(f'app/content/courses/{course}/problems-{n}.json'))['items']}


def parse(tex):
    """A stored expression answer -> tuple of sympy numbers, or tuple of tuples for a matrix."""
    t = tex.replace('\\left', '').replace('\\right', '')
    t = re.sub(r'\\t?frac\{([^{}]*)\}\{([^{}]*)\}', r'((\1)/(\2))', t)
    m = re.search(r'\\begin\{pmatrix\}(.*)\\end\{pmatrix\}', t)
    conv = lambda s: sp.nsimplify(sp.sympify(s.strip(), locals={'k': k}), rational=True)
    if m:
        return tuple(tuple(conv(c) for c in row.split('&')) for row in m.group(1).split('\\\\'))
    t = t.strip()
    if t.startswith('[['):
        return tuple(tuple(conv(c) for c in row.split(',')) for row in t[2:-2].split('], ['))
    if t[0] in '([' and t[-1] in ')]':
        t = t[1:-1]
    return tuple(conv(c) for c in t.split(','))


def tup(v):
    if isinstance(v, sp.MatrixBase):
        if v.shape[1] == 1 or v.shape[0] == 1:
            return tuple(sp.nsimplify(x, rational=True) for x in v)
        return tuple(tuple(sp.nsimplify(x, rational=True) for x in v.row(i)) for i in range(v.shape[0]))
    return tuple(sp.nsimplify(x, rational=True) for x in v)


def same(a, b):
    if isinstance(a, tuple) != isinstance(b, tuple):
        return False
    if isinstance(a, tuple):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return sp.simplify(a - b) == 0


def part(items, iid, n, key, wrongs=None, tol=None):
    """Compare my key and my slips with part n (1-based) of item iid."""
    w = items[iid]['parts'][n - 1]['widget']
    lab = f'{iid} part {n}'
    if w['kind'] == 'choice':
        right = [o['id'] for o in w['options'] if o.get('correct')]
        ok(right == [key], f'{lab}: correct option {right} vs mine {key}')
        return
    stored = {x['id']: x for x in w.get('wrong', [])}
    wrongs = wrongs or {}
    ok(set(stored) == set(wrongs), f'{lab}: wrong ids {sorted(stored)} vs mine {sorted(wrongs)}')
    if w['kind'] == 'numeric':
        band = w['tol']['abs']
        ok(abs(float(key) - w['answer']) <= max(band, 1e-9) and (tol is None or abs(band - tol) < 1e-12),
           f'{lab}: key {w["answer"]} tol {band} vs mine {float(key)} tol {tol}')
        for i, v in wrongs.items():
            if i in stored:
                ok(abs(float(v) - stored[i]['value']) <= max(stored[i]['tol']['abs'], 1e-9), f'{lab}: wrong {i} {stored[i]["value"]} vs mine {float(v)}')
                ok(abs(float(v) - float(key)) > band + stored[i]['tol']['abs'], f'{lab}: wrong {i} band touches the key band')
        vals = sorted((x['value'], x['tol']['abs'], i) for i, x in stored.items())
        for a, b in zip(vals, vals[1:]):
            ok(a[0] + a[1] < b[0] - b[1], f'{lab}: bands of {a[2]} and {b[2]} overlap')
    else:
        key = tup(key) if not isinstance(key, tuple) else key
        ok(same(parse(w['answer']), key), f'{lab}: key {w["answer"]} vs mine {key}')
        for a in w.get('accept', []):
            ok(same(parse(a), key), f'{lab}: accept {a} is not the key')
        for i, v in wrongs.items():
            v = tup(v) if not isinstance(v, tuple) else v
            if i in stored:
                ok(same(parse(stored[i]['tex']), v), f'{lab}: wrong {i} {stored[i]["tex"]} vs mine {v}')
                ok(not same(v, key), f'{lab}: wrong {i} equals the key')


def text_of(items, iid, n):
    return json.dumps(items[iid]['parts'][n - 1], ensure_ascii=False)


def says(items, iid, n, *needles):
    t = text_of(items, iid, n)
    for s in needles:
        ok(s in t, f'{iid} part {n}: expected the text to hold {s!r}')


def backsub(U, c):
    n = U.shape[0]
    x = [0] * n
    for i in reversed(range(n)):
        x[i] = (c[i] - sum(U[i, j] * x[j] for j in range(i + 1, n))) / U[i, i]
    return M(x)


def fwdsub(L, b):
    n = L.shape[0]
    c = [0] * n
    for i in range(n):
        c[i] = (b[i] - sum(L[i, j] * c[j] for j in range(i))) / L[i, i]
    return M(c)


def lu(A):
    """Doolittle, no swaps: returns L, U."""
    n = A.shape[0]
    U = A.copy()
    L = sp.eye(n)
    for j in range(n):
        for i in range(j + 1, n):
            L[i, j] = U[i, j] / U[j, j]
            U[i, :] = U[i, :] - L[i, j] * U[j, :]
    return L, U


# ============================================================ elimination problems-1
E1 = load('elimination', 1)

# florist: rows are bouquets (roses, tulips, lilies | cost)
Ab = M([[2, 2, 4, 19], [6, 8, 13, 64], [1, 5, 5, R(53, 2)]])
r3 = Ab.row(2) - R(1, 2) * Ab.row(0)
part(E1, 'p-florist-prices', 1, tup(r3), {'upside-down': tup(Ab.row(2) - 2 * Ab.row(0)), 'added': tup(Ab.row(2) + R(1, 2) * Ab.row(0))})
r2 = Ab.row(1) - 3 * Ab.row(0)
ok(tup(r2) == (0, 2, 1, 7), 'florist: row 2 after column 1 is (0, 2, 1 | 7)')
r3b = r3 - (r3[1] / r2[1]) * r2
sol = sp.linsolve((Ab[:, :3], Ab[:, 3]), *sp.symbols('x y z'))
x, y, z = list(sol)[0]
ok(tup(r3b) == (0, 0, 1, 3) and (x, y, z) == (R(3, 2), 2, 3), 'florist: R3 - 2R2 = (0, 0, 1 | 3); prices 1.5, 2, 3')
ok(np.allclose(np.linalg.solve(np.array(Ab[:, :3], float), np.array(Ab[:, 3], float).ravel()), [1.5, 2, 3]), 'florist: NumPy agrees')
part(E1, 'p-florist-prices', 2, z, {'cost-kept': 17}, tol=0)
part(E1, 'p-florist-prices', 3, y, {'no-subtract': R(7, 2), 'added': R(7 + 3, 2)}, tol=0)
part(E1, 'p-florist-prices', 4, x, {'coefficients': R(19 - 2 - 3, 2), 'no-divide': 19 - 2 * 2 - 4 * 3})
part(E1, 'p-florist-prices', 5, 4 * x + 3 * y + 2 * z, {'carried': 4 * 7 + 3 * y + 2 * z, 'counts-swapped': 2 * x + 3 * y + 4 * z})

# three lines
A = M([[2, 2, 2], [6, 7, 9], [1, 3, 9]])
L, U = lu(A)
ok(L * U == A and tup(U) == ((2, 2, 2), (0, 1, 3), (0, 0, 2)), 'three-lines: LU = A and U as printed in part 3')
Lsigns = sp.eye(3) - (L - sp.eye(3))
Lstale = L.copy(); Lstale[2, 1] = A[2, 1]          # the 3 of the original row 3
part(E1, 'p-three-lines', 1, tup(L), {'signs': tup(Lsigns), 'transposed': tup(L.T), 'stale': tup(Lstale)})
b = M([12, 41, 18])
c = fwdsub(L, b)
part(E1, 'p-three-lines', 2, tup(c), {'signs': tup(fwdsub(Lsigns, b)), 'stale': tup(fwdsub(Lstale, b))})
xm = backsub(U, c)
ok(A * xm == b, 'three-lines: A x = b on Monday')
nodiv = [0, 0, 0]
for i in (2, 1, 0):
    nodiv[i] = c[i] - sum(U[i, j] * nodiv[j] for j in range(i + 1, 3))
part(E1, 'p-three-lines', 3, tup(xm), {'b-not-c': tup(backsub(U, b)), 'no-divide': tuple(nodiv)})
extra = M([10, 38, 25])
ce = fwdsub(L, extra)
ye = backsub(U, ce)
ok(tup(ce) == (10, 8, 4) and tup(ye) == (1, 2, 2), 'three-lines: extra gives c = (10, 8, 4), hours (1, 2, 2)')
ok(tup(A.LUsolve(b + extra)) == tup(xm + ye), 'three-lines: solving the whole Tuesday order gives the same')
part(E1, 'p-three-lines', 4, tup(xm + ye), {'extra-only': tup(ye), 'added-c': tup(xm + ce)})

# courier
A = M([[0, 3, 1], [2, 1, 2], [0, 6, 5]]); b = M([15, 14, 39])
P12 = M([[0, 1, 0], [1, 0, 0], [0, 0, 1]]); P13 = M([[0, 0, 1], [0, 1, 0], [1, 0, 0]]); P23 = M([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
ok((P12 * A)[0, 0] != 0 and (P13 * A)[0, 0] == 0 and (P23 * A)[0, 0] == 0, 'courier: only the swap of rows 1 and 2 gives a non-zero first pivot')
part(E1, 'p-courier-rounds', 1, tup(P12), {'swap-1-3': tup(P13)})
L, U = lu(P12 * A)
ok(tup(U) == ((2, 1, 2), (0, 3, 1), (0, 0, 3)), 'courier: U as printed in part 4')
Ls = sp.eye(3) - (L - sp.eye(3))
part(E1, 'p-courier-rounds', 2, tup(L), {'signs': tup(Ls), 'transposed': tup(L.T)})
c = fwdsub(L, P12 * b)
part(E1, 'p-courier-rounds', 3, tup(c), {'unswapped': tup(fwdsub(L, b)), 'signs': tup(fwdsub(Ls, P12 * b))})
xc = backsub(U, c)
ok(A * xc == b, 'courier: A x = b')
nodiv = [0, 0, 0]
for i in (2, 1, 0):
    nodiv[i] = c[i] - sum(U[i, j] * nodiv[j] for j in range(i + 1, 3))
part(E1, 'p-courier-rounds', 4, tup(xc), {'no-divide': tuple(nodiv), 'reversed': tup(xc)[::-1]})
cnt = M([5, 2, 4])
part(E1, 'p-courier-rounds', 5, cnt.dot(xc), {'reversed': cnt.dot(M(tup(xc)[::-1]))}, tol=0)

# roaster
A = M([[2, 1, 3], [6, 3, 10], [4, k, 9]])
r3 = A.row(2) - 2 * A.row(0)
part(E1, 'p-roaster-beans', 1, tup(r3), {'added': tup(A.row(2) + 2 * A.row(0)), 'triple': tup(A.row(2) - 3 * A.row(0))})
ok(tup(A.row(1) - 3 * A.row(0)) == (0, 0, 1), 'roaster: row 2 becomes (0, 0, 1)')
ok(sp.solve(sp.det(A), k) == [2], 'roaster: det A = 0 only at k = 2')
part(E1, 'p-roaster-beans', 2, 2, {'k-zero': 0, 'triple': 3}, tol=0)
A2 = A.subs(k, 2); b2 = M([35, 110, 85])
ok(A2.rank() == 2 and A2.row_join(b2).rank() == 2, 'roaster k = 2, cost 85: consistent, rank 2 (many prices)')
xs = sp.symbols('x y z')
s2 = list(sp.linsolve((A2, b2), *xs))[0]
ok(s2[2] == 5 and sp.simplify(2 * s2[0] + s2[1] - 20) == 0, 'roaster k = 2: z = 5 and 2x + y = 20')
part(E1, 'p-roaster-beans', 3, 'c-only')
A4 = A.subs(k, 4); b4 = M([35, 110, 101])
s4 = list(sp.linsolve((A4, b4), *xs))[0]
part(E1, 'p-roaster-beans', 4, s4[1], {'no-z': R(31, 2), 'cost-kept': R(101 - 15, 2)}, tol=0)
part(E1, 'p-roaster-beans', 5, tuple(s4), {'carried': (R(35 - 15, 2) - R(31, 4), R(31, 2), 5), 'no-divide': (12, 8, 5)})

# ============================================================ elimination problems-2
E2 = load('elimination', 2)
# ethanol C2H6O + O2 -> CO2 + H2O; rows C, H, O; products negative
A = M([[2, 0, -1, 0], [6, 0, 0, -2], [1, 2, -2, -1]])
ok(A.rank() == 3 and len(A.nullspace()) == 1, 'ethanol: rank 3, nullity 1')
ok(tup(A.row(1) - 3 * A.row(0)) == (0, 0, 3, -2) and tup(A.row(2) - R(1, 2) * A.row(0)) == (0, 2, R(-3, 2), -1), 'ethanol: rows after column 1')
part(E2, 'p-burning-ethanol', 1, 3, {'columns': 4}, tol=0)
part(E2, 'p-burning-ethanol', 2, 1, {'rank': 3, 'full': 0}, tol=0)
ns = A.nullspace()[0]; ns = ns / ns[3]
Apos = A.applyfunc(abs)
nsp = Apos.nullspace()[0]; nsp = nsp / nsp[3]
whole = ns * sp.ilcm(*[sp.fraction(v)[1] for v in ns])
part(E2, 'p-burning-ethanol', 3, tup(ns), {'no-minus': tup(nsp), 'scaled': tup(whole)})
part(E2, 'p-burning-ethanol', 4, tup(whole), {'not-whole': tup(ns), 'double': tup(2 * whole)})
ok(np.allclose(np.linalg.svd(np.array(A, float))[2][-1] / np.linalg.svd(np.array(A, float))[2][-1][0], [1, 3, 2, 3]), 'ethanol: SVD null vector is (1, 3, 2, 3)')

# gantry
m1, m2, m3 = M([1, 0, 2]), M([1, 1, 0]), M([0, 2, k])
Mk = m1.row_join(m2).row_join(m3)
kk = sp.solve(sp.det(Mk), k)
part(E2, 'p-tilted-gantry', 1, kk[0], {'sign': -kk[0], 'zero': 0}, tol=0)
a, b_ = sp.symbols('a b')
ab = sp.solve(list(a * m1 + b_ * m2 - m3.subs(k, -4)), [a, b_])
part(E2, 'p-tilted-gantry', 2, (ab[a], ab[b_]), {'sign': (-ab[a], -ab[b_])})
c_ = sp.Symbol('c')
cc = sp.solve(sp.det(m1.row_join(m2).row_join(M([3, 1, c_]))), c_)[0]
part(E2, 'p-tilted-gantry', 3, cc, {'half-step': 6, 'sign': -4}, tol=0)
M4 = Mk.subs(k, -4)
base = M([2, 1, 0]); nsv = M([2, -2, 1])
ok(M4 * nsv == sp.zeros(3, 1) and M4 * base == M([3, 1, 4]), 'gantry: (2, -2, 1) in the nullspace, (2, 1, 0) reaches (3, 1, 4)')
ok(M4 * M([-2, 2, 1]) != sp.zeros(3, 1), 'gantry: (-2, 2, 1) is not in the nullspace')
part(E2, 'p-tilted-gantry', 4, tup(base + nsv), {'no-motor-3': tup(base), 'sign': tup(base + M([-2, 2, 1]))})

# futures
S = M([[1, 0, 1], [-1, 1, -2], [0, -1, 1]])
ok(S.rank() == 2, 'futures: rank 2')
part(E2, 'p-futures-packages', 1, 2, {'columns': 3}, tol=0)
sv = S.nullspace()[0]; sv = sv / sv[2]
part(E2, 'p-futures-packages', 2, tup(sv), {'sign': (1, -1, 1)})
ok(tup(S * M([1, -1, 1])) == (2, -4, 2), 'futures: s1 - s2 + f = (2, -4, 2)')
cc = sp.solve(S.row_join(M([4, -1, c_])).det() if False else M([[1, 0, 4], [-1, 1, -1], [0, -1, c_]]).det(), c_)[0]
part(E2, 'p-futures-packages', 3, cc, {'sign': 3, 'stale-rhs': 1}, tol=0)
x4 = M([4, 3, 0])
ok(tup(S * x4) == (4, -1, -3), 'futures: (4, 3, 0) builds (4, -1, -3)')
part(E2, 'p-futures-packages', 4, tup(x4), {'sign': (4, -3, 0)})
ok((S * M([4, -3, 0]))[1] == -7, 'futures: (4, -3, 0) gives June -7')
part(E2, 'p-futures-packages', 5, tup(x4 + 2 * sv), {'sign': tup(x4 + 2 * M([1, -1, 1])), 'nullspace-only': tup(2 * sv)})
ok(tup(S * M([6, 1, 2])) == (8, -9, 1), 'futures: (6, 1, 2) gives (8, -9, 1)')

# coin hopper
A = M([[20, 50, 100], [1, 1, 1]])
part(E2, 'p-coin-hopper', 1, A.rank(), {'columns': 3, 'one': 1}, tol=0)
ok(tup(A.row(1) - R(1, 20) * A.row(0)) == (0, R(-3, 2), -4), 'coins: R2 - R1/20 = (0, -1.5, -4)')
nv = A.nullspace()[0]; nv = nv / nv[2]
part(E2, 'p-coin-hopper', 2, tup(3 * nv), {'sign': (-5, 8, 3), 'special': tup(nv)})
ok(A[0, :].dot(M([-5, 8, 3])) == 600, 'coins: (-5, 8, 3) changes the value by 600p')
ways = [(p, q, r) for p in range(20) for q in range(20) for r in range(20) if p + q + r == 10 and 20 * p + 50 * q + 100 * r == 370]
ok(ways == [(6, 3, 1)], 'coins: exactly one way to pay 370p in 10 coins, by enumeration')
part(E2, 'p-coin-hopper', 3, (6, 3, 1), {'swapped': (3, 6, 1)})
ok(20 * 3 + 50 * 6 + 100 == 460, 'coins: (3, 6, 1) is worth 460p')
part(E2, 'p-coin-hopper', 4, 'one')

# ============================================================ elimination problems-3
E3 = load('elimination', 3)
T = M([[3, k], [2, 4]])
d1 = T.subs(k, 1).det()
part(E3, 'p-vinyl-cutter', 1, 5 * d1, {'plus': 5 * (12 + 2), 'diagonal': 5 * 12}, tol=0)
ok(sp.expand(T.det()) == 12 - 2 * k, 'vinyl: det T = 12 - 2k')
part(E3, 'p-vinyl-cutter', 2, sp.solve(T.det(), k)[0], {'sign': -6, 'factor': 12}, tol=0)
T6 = T.subs(k, 6)
part(E3, 'p-vinyl-cutter', 3, 6 * T6[1, 0] / T6[0, 0], {'row': 6 * T6[0, 1] / T6[0, 0]}, tol=0)
nv = T6.nullspace()[0]; nv = 2 * nv / nv[0]
part(E3, 'p-vinyl-cutter', 4, tup(nv), {'sign': (2, 1), 'perpendicular': (2, -3)})
ok(tup(T6 * M([2, 1])) == (12, 8) and tup(T6 * M([2, -3])) == (-12, -8) and M([2, -3]).dot(M([3, 2])) == 0, 'vinyl: the two wrong inputs map as stated')

D = M([[2, 1, 0], [0, 3, 1], [1, 0, 2]])
minors = [D.minor(0, j) for j in range(3)]
ok(minors == [6, -1, -3], 'deformed: minors of row 1 are 6, -1, -3')
part(E3, 'p-deformed-part', 1, D.det(), {'no-sign': 2 * 6 + 1 * (-1) + 0, 'diagonal': 2 * 3 * 2}, tol=0)
L, U = lu(D)
ok(L[2, 1] == R(-1, 6) and U[2, 2] == R(13, 6) and U[0, 0] * U[1, 1] * U[2, 2] == 13, 'deformed: l32 = -1/6, third pivot 13/6, pivots multiply to 13')
part(E3, 'p-deformed-part', 2, U[2, 2], {'sign': 2 - R(1, 6)}, tol=0.001)
part(E3, 'p-deformed-part', 3, 15 * D.det(), {'no-sign': 15 * 11, 'diagonal': 15 * 12}, tol=0)
Dp = M([D.row(2), 2 * D.row(1), D.row(0)])
part(E3, 'p-deformed-part', 4, Dp.det(), {'swap-ignored': 26, 'scale-ignored': -13, 'scale-squared': -52}, tol=0)
part(E3, 'p-deformed-part', 5, 195 * abs(Dp.det()), {'signed': 195 * Dp.det(), 'scale-ignored': 195 * 13}, tol=0)
ok(abs(np.linalg.det(np.array(Dp, float)) + 26) < 1e-9, 'deformed: NumPy det of D prime')

# draw bet: rows home, draw, away; columns H, Y, X
H, Y, X, Dd = M([10, 0, 0]), M([10, 0, 10]), M([0, 10, 10]), M([0, 10, 0])
P = H.row_join(Y).row_join(X)
ok(tup(P) == ((10, 10, 0), (0, 0, 10), (0, 10, 10)), 'draw-bet: P as printed matches the three bets in words')
part(E3, 'p-draw-bet', 1, P.det(), {'diagonal': 10 * 0 * 10, 'plus': 10 * (0 * 10 + 10 * 10)}, tol=0)
P4 = P.row_join(Dd)
part(E3, 'p-draw-bet', 2, 4 - P4.rank(), {'none': 0, 'rank': 3}, tol=0)
copy = P.LUsolve(Dd)
part(E3, 'p-draw-bet', 3, tup(copy), {'sign': tup(-copy), 'no-sale': (1, 1, 1)})
ok(tup(P * M([1, 1, 1])) == (20, 10, 20), 'draw-bet: buying all three pays (20, 10, 20)')
price = M([R(9, 2), 7, R(29, 5)])
part(E3, 'p-draw-bet', 4, price.dot(copy), {'all-plus': sum(price), 'sign': -price.dot(copy)})
part(E3, 'p-draw-bet', 5, 50 * (price.dot(copy) - 3), {'per-bet': price.dot(copy) - 3, 'reversed': -50 * (price.dot(copy) - 3)})
q = P.T.LUsolve(price)      # state prices
ok(all(v > 0 for v in q) and sum(q) == R(103, 100), 'draw-bet: state prices positive (0.45, 0.33, 0.25), sum 1.03')
# every one of the four bets is a combination of the other three (all weights of the relation are non-zero)
ok(all(v != 0 for v in P4.nullspace()[0]), 'draw-bet: the dependency H - Y + X - D = 0 has no zero weight')

# ============================================================ least-squares problems-1
L1 = load('least-squares', 1)
a1, a2 = M([1, 2, 1]), M([1, 0, -1])
A = a1.row_join(a2)
yv = A.T.nullspace()[0]; yv = yv / yv[0]
part(L1, 'p-hall-drone', 1, tup(yv), {'sign': tup(a2), 'b-sign': (1, 1, 1)})
ok(a2.dot(a2) == 2 and M([1, 1, 1]).dot(a1) == 4, 'hall-drone: the dot products in the two wrong lines')
cc = sp.solve(yv.dot(M([4, 6, c_])), c_)[0]
added = sp.solve(4 + 6 + c_, c_)[0]
part(L1, 'p-hall-drone', 2, cc, {'sign': -cc, 'added': 10}, tol=0)
if added != 10:
    claim(f'hall-drone part 2 `added`: adding 4 and 6 and solving 4 + 6 + c = 0 gives c = {added}; the stored slip is 10 (the sum, not the solution)')
bt = M([4, 6, 2])
coef = lambda b, vs: tuple(sp.nsimplify(b.dot(v) / v.dot(v)) for v in vs)
ok(a1.dot(a2) == 0, 'hall-drone: a1 . a2 = 0')
part(L1, 'p-hall-drone', 3, coef(bt, [a1, a2]), {'no-divide': (bt.dot(a1), bt.dot(a2)), 'sign-x2': (3, R(4 + 2, 2))})
b5 = M([4, 6, 5])
x5 = coef(b5, [a1, a2, yv])
ok(tup(A.row_join(yv) * M(x5)) == tup(b5), 'hall-drone: the three-direction plan reaches (4, 6, 5)')
part(L1, 'p-hall-drone', 4, x5, {'kept-plan': (3, 1, 1), 'no-divide-y': (x5[0], x5[1], b5.dot(yv)), 'no-divide': (b5.dot(a1), b5.dot(a2), b5.dot(yv)), 'sign': (x5[0], -x5[1], x5[2])})
ok(coef(M([0, 0, 3]), [a1, a2, yv]) == (R(1, 2), R(-3, 2), 1), 'hall-drone: the extra (0, 0, 3) needs (0.5, -1.5, 1)')

c1, c2, c3 = M([1, 1, 1, 1]), M([1, -1, 1, -1]), M([1, 1, -1, -1])
C3 = M([c1.T, c2.T, c3.T])
c4 = C3.nullspace()[0]; c4 = c4 / c4[0]
part(L1, 'p-station-codes', 1, tup(c4), {'c1-only': tup(c2), 'flipped': tup(-c4)})
passes = [n for n, c in (('c1', c1), ('c2', c2), ('c3', c3)) if c2.dot(c) == 0]
if passes != ['c1']:
    claim(f'station-codes part 1 `c1-only`: the line says c2 "passes the test against c1 only"; c2 is orthogonal to {passes} (c2 . c3 = {c2.dot(c3)})')
r = M([5, -1, 3, 5])
part(L1, 'p-station-codes', 2, r.dot(c4) / c4.dot(c4), {'no-divide': r.dot(c4), 'by-length': r.dot(c4) / sp.sqrt(c4.dot(c4))}, tol=0)
xs4 = coef(r, [c1, c2, c3, c4])
ok(tup(xs4[0] * c1 + xs4[1] * c2 + xs4[2] * c3 + xs4[3] * c4) == tup(r), 'station-codes: the readings rebuild r')
part(L1, 'p-station-codes', 3, xs4, {'no-divide': tuple(4 * v for v in xs4), 'by-length': tuple(2 * v for v in xs4), 'sign': (3, 1, 1, 2)})
rnew = r + 3 * c2
part(L1, 'p-station-codes', 4, rnew.dot(rnew) - r.dot(r), {'cross-term': (3 * c2).dot(3 * c2), 'no-four': 16 - 1}, tol=0)
ok(tup(rnew) == (8, -4, 6, 2) and rnew.dot(rnew) == 120 and r.dot(r) == 60, 'station-codes: new r and both powers')

a1, a2, a3 = M([2, 1, 2]), M([6, 0, 3]), M([5, 1, -1])
e2 = a2 - a2.dot(a1) / a1.dot(a1) * a1
part(L1, 'p-crystal-cell', 1, tup(e2), {'length-not-squared': tup(a2 - a2.dot(a1) / a1.norm() * a1), 'added': tup(a2 + 2 * a1)})
area = a1.norm() * e2.norm()
ok(area == a1.cross(a2).norm(), 'crystal: face area equals |a1 x a2|')
part(L1, 'p-crystal-cell', 2, area, {'slanted': a1.norm() * a2.norm(), 'triangle': area / 2}, tol=0)
e3 = a3 - a3.dot(a1) / a1.dot(a1) * a1 - a3.dot(e2) / e2.dot(e2) * e2
e3o = a3 - a3.dot(a1) / a1.dot(a1) * a1 - a3.dot(a2) / a2.dot(a2) * a2
part(L1, 'p-crystal-cell', 3, tup(e3), {'originals': tup(e3o), 'unit-skipped': tup(a3 - a3.dot(a1) / a1.dot(a1) * a1 - a3.dot(e2) * e2)})
vol = area * e3.norm()
ok(vol == abs(a1.row_join(a2).row_join(a3).det()) == 27, 'crystal: volume equals |det| = 27')
part(L1, 'p-crystal-cell', 4, vol, {'no-straightening': a1.norm() * a2.norm() * a3.norm(), 'squared': area * e3.dot(e3), 'carried': area * e3o.norm()}, tol=0)

Ar = M([[1, 1, 1, 1], [0, 1, 0, -1]])
s1 = M([-1, 0, 1, 0])
ok(Ar * s1 == sp.zeros(2, 1), 'rotor: s1 is safe')
x1_, x2_ = sp.symbols('x1 x2')
s2s = sp.solve(list(Ar * M([x1_, x2_, 0, 1])), [x1_, x2_])
s2 = M([s2s[x1_], s2s[x2_], 0, 1])
part(L1, 'p-rotor-changes', 1, tup(s2), {'roll-sign': (0, -1, 0, 1), 'lift-short': (-1, 1, 0, 1), 'no-minus': (2, 1, 0, 1)})
gs = lambda v, u: v - v.dot(u) / u.dot(u) * u
e2 = gs(s2, s1)
s2bad = M([0, -1, 0, 1])
part(L1, 'p-rotor-changes', 2, tup(e2), {'no-divide': tup(s2 - s2.dot(s1) * s1), 'added': tup(s2 + s1), 'carried': tup(gs(s2bad, s1))})
d = M([4, 0, 2, -2])
four = [Ar.row(0).T, Ar.row(1).T, s1, e2]
ok(all(four[i].dot(four[j]) == 0 for i in range(4) for j in range(i)), 'rotor: the two rows, s1 and e2 are mutually orthogonal')
ce = d.dot(e2) / e2.dot(e2)
part(L1, 'p-rotor-changes', 3, ce, {'no-divide': d.dot(e2), 'by-length': d.dot(e2) / e2.norm(), 'no-sign': -ce}, tol=0)
safe = d.dot(s1) / s1.dot(s1) * s1 + ce * e2
rowpart = sum((d.dot(v) / v.dot(v) * v for v in four[:2]), sp.zeros(4, 1))
ok(safe + rowpart == d and Ar * safe == sp.zeros(2, 1), 'rotor: safe part plus row part is d, and the safe part is in N(A)')
Pn = sp.eye(4) - Ar.T * (Ar * Ar.T).inv() * Ar
ok(Pn * d == safe, 'rotor: the projection matrix onto N(A) gives the same safe part')
part(L1, 'p-rotor-changes', 4, tup(safe), {'row-part': tup(rowpart), 'e2-only': tup(ce * e2), 'used-s2': tup(d.dot(s1) / s1.dot(s1) * s1 + d.dot(s2) / s2.dot(s2) * s2)})
t4 = L1['p-rotor-changes']['parts'][3]['question']
if '(-1, 1, -1, 1)' not in t4 or '(4, 0, 2, -2)' not in t4:
    claim('rotor part 4 does not restate e2, s1 or d, which it needs (they are in parts 1 to 3 only)')

# ============================================================ least-squares problems-2
L2 = load('least-squares', 2)
g = M([1, 1, 1]); b = M([200, 140, 80])
Pg = g * g.T / g.dot(g)
part(L2, 'p-grey-pixel', 1, tup(Pg * b), {'no-divide': tup(g * g.T * b)})
col = (sp.eye(3) - Pg) * b
part(L2, 'p-grey-pixel', 2, tup(col), {'reversed': tup(-col), 'carried': tup(b - g * g.T * b)})
Fm = Pg + R(1, 2) * (sp.eye(3) - Pg)
part(L2, 'p-grey-pixel', 3, tup(Fm * b), {'halved-all': tup(b / 2), 'grey-halved': tup(Pg * b / 2 + col)})
part(L2, 'p-grey-pixel', 4, tup(Fm * Fm * b), {'projection': tup(Fm * b), 'halved-twice-all': tup(Fm * b / 2)})
ok(Fm * Fm == Pg + R(1, 4) * (sp.eye(3) - Pg) and Fm * Fm != Fm, 'grey-pixel: F squared is P + (I - P)/4, not F')

a = M([4, 3]); b = M([2, 9])
xh = a.dot(b) / a.dot(a)
part(L2, 'p-power-line', 1, xh, {'no-divide': a.dot(b), 'by-length': a.dot(b) / a.norm()}, tol=0)
p = xh * a; e = b - p
part(L2, 'p-power-line', 2, tup(e), {'p-not-e': tup(p), 'added': tup(b + p), 'carried': tup(b - 7 * a), 'sign': (-e[0], e[1])})
part(L2, 'p-power-line', 3, e.norm(), {'along': p.norm(), 'to-origin': b.norm(), 'squared': e.dot(e)}, tol=0)
J = M([8, 6])
ok(J == 2 * a and (J - p).norm() == 3, 'power-line: J is on the line, 3 km from p')
longer = (b - J).norm() - e.norm()
part(L2, 'p-power-line', 4, longer, {'added': 3, 'total': (b - J).norm(), 'squares': (b - J).dot(b - J) - e.dot(e)}, tol=0.005)
ok(abs(float(longer) - 0.71) < 0.005 and abs((6.71 - 6) - 0.7082) < 0.005, 'power-line: 0.71 and the rounded route 6.71 - 6 are inside the band')

a1, a2 = M([1, 0, 2]), M([0, 1, 1]); b = M([-2, 1, 9])
A = a1.row_join(a2)
n = A.T.nullspace()[0]; n = n / n[2]
part(L2, 'p-solar-drone', 1, tup(n), {'sign': (-2, 1, 1), 'one-edge': (-2, 0, 1)})
ok(M([-2, 1, 1]).dot(a2) == 2 and M([-2, 0, 1]).dot(a1) == 0, 'solar: the dot products in the two wrong lines')
proj = lambda b, v: b.dot(v) / v.dot(v) * v
e = proj(b, n)
nb = M([-2, 1, 1])
part(L2, 'p-solar-drone', 2, tup(e), {'no-divide': tup(b.dot(n) * n), 'carried': tup(proj(b, nb))})
p = b - e
ok(A * (A.T * A).inv() * A.T * b == p, 'solar: the projection matrix gives the same p')
part(L2, 'p-solar-drone', 3, tup(p), {'added': tup(b + e), 'carried': tup(b - b.dot(n) * n)})
xh = (A.T * A).inv() * A.T * b
ok(tup(A.T * b) == (16, 10) and tup(A.T * A) == ((5, 2), (2, 2)), 'solar: normal equations as stated in the explanation')
part(L2, 'p-solar-drone', 4, tup(xh), {'straight-down': (b[0], b[1]), 'carried': ((b + e)[0], (b + e)[1])})
ok(2 * (-6) + (-1) == -13, 'solar: (-6, -1, 11) is off the plane, as its line says')

a1, a2 = M([2, 3, 6]), M([8, 5, 3]); b = M([9, 17, 13])
q1 = a1 / a1.norm()
r12 = q1.dot(a2)
part(L2, 'p-dye-mix', 1, r12, {'no-unit': a1.dot(a2), 'coefficient': a1.dot(a2) / a1.dot(a1)}, tol=0)
v = a2 - r12 * q1; q2 = v / v.norm()
part(L2, 'p-dye-mix', 2, tup(q2), {'not-normalised': tup(v), 'used-a1': tup(a2 - r12 * a1)})
Q = q1.row_join(q2); A = a1.row_join(a2)
Rm = Q.T * A
ok(tup(Rm) == ((7, 7), (0, 7)), 'dye: R = Q^T A is ((7, 7), (0, 7))')
qtb = Q.T * b
part(L2, 'p-dye-mix', 3, tup(qtb), {'a-not-q': tup(A.T * b), 'used-a2': (q1.dot(b), a2.dot(b) / 7)})
xh = backsub(Rm, qtb)
ok(tup((A.T * A).inv() * A.T * b) == tup(xh), 'dye: normal equations agree with QR')
ok(np.allclose(np.linalg.lstsq(np.array(A, float), np.array(b, float).ravel(), rcond=None)[0], [2, 1]), 'dye: lstsq agrees')
part(L2, 'p-dye-mix', 4, tup(xh), {'top-down': (qtb[0] / 7, qtb[1] / 7), 'transposed': tup(fwdsub(Rm.T, qtb))})
miss = (b - A * xh).norm()
part(L2, 'p-dye-mix', 5, miss, {'squared': miss ** 2, 'carried': (b - A * M([3, 1])).norm(), 'lengths': b.norm() - (A * xh).norm()}, tol=0)
ok(b.dot(b) == 539 and qtb.dot(qtb) == 490, 'dye: 539 = 490 + 49')

# ============================================================ least-squares problems-3
L3 = load('least-squares', 3)
x = [8, 9, 10, 11, 12]; y = [128, 135, 139, 146, 152]
xb, yb = F(sum(x), 5), F(sum(y), 5)
sxy = sum((u - xb) * (w - yb) for u, w in zip(x, y)); sxx = sum((u - xb) ** 2 for u in x)
part(L3, 'p-runner-heart', 1, sxy, {'uncentred': sum(u * w for u, w in zip(x, y)), 'sxx': sxx}, tol=0)
beta = sxy / sxx
part(L3, 'p-runner-heart', 2, beta, {'over-n': sxy / 5, 'upside-down': sxx / sxy}, tol=0)
alpha = yb - beta * xb
part(L3, 'p-runner-heart', 3, alpha, {'sign': yb + beta * xb, 'no-xbar': yb - beta}, tol=0)
ok(np.allclose(np.polyfit(x, y, 1), [5.9, 81]), 'runner: polyfit gives 5.9 and 81')
x6, y6 = x + [10], y + [146]
f6 = np.polyfit(x6, y6, 1)
ok(np.allclose(f6, [5.9, 82]) and 146 - (81 + 59) == 6, 'runner: six runs give 5.9 and 82; the new run is 6 above the old line')
part(L3, 'p-runner-heart', 4, 'same')
part(L3, 'p-runner-heart', 5, 82, {'old': 81, 'full-shift': 81 + 6, 'mean-only': F(sum(y6), 6)}, tol=0)

A = M([[1, 1], [1, 4], [1, 9]]); b = M([R(13, 2), R(101, 5), R(463, 10)])
kk = sp.solve(M([5, k, 3]).dot(A[:, 0]), k)[0]
ok(M([5, kk, 3]).dot(A[:, 1]) == 0, 'ramp: (5, -8, 3) is orthogonal to the second column too')
part(L3, 'p-ramp-ball', 1, kk, {'sign': -kk}, tol=0)
yv = M([5, kk, 3])
e = proj(b, yv)
ok(b.dot(yv) == R(49, 5) and yv.dot(yv) == 98, 'ramp: b . y = 9.8 and y . y = 98')
part(L3, 'p-ramp-ball', 2, tup(e), {'no-divide': tup(b.dot(yv) * yv), 'gave-p': tup(b - e)})
xh = (A.T * A).inv() * A.T * b
ok(tup(A * xh) == tup(b - e) and tup(A.T * A) == ((3, 14), (14, 98)) and tup(A.T * b) == (73, 504), 'ramp: normal equations agree and are as stated')
part(L3, 'p-ramp-ball', 3, tup(xh), {'swapped': tup(xh)[::-1]})
part(L3, 'p-ramp-ball', 4, xh[0] + xh[1] * 25, {'t-not-squared': xh[0] + xh[1] * 5, 'no-intercept': xh[1] * 25, 'swapped': xh[1] + xh[0] * 25}, tol=0)

t = M([-1, 0, 1, 2, 3]); yN = M([R(7, 2), 0, R(-1, 2), -3, -5]); yS = M([2, 1, -2, -2, -4])
A = sp.ones(5, 1).row_join(t)
ATA = A.T * A
part(L3, 'p-gas-hubs', 1, ATA[1, 1], {'sum': ATA[0, 1], 'sum-squared': ATA[0, 1] ** 2}, tol=0)
ok(tup(ATA) == ((5, 5), (5, 15)) and tup(A.T * yN) == (-5, -25) and tup(A.T * yS) == (-5, -20), 'gas: the printed arrays')
if ATA[0, 0] == ATA[0, 1]:
    claim('gas-hubs part 1 `sum`: 5 is also entry [0, 0], the count, which a learner counting from 1 gives; the line names only the off-diagonal entry')
fN = ATA.inv() * A.T * yN; fS = ATA.inv() * A.T * yS
diag = lambda rhs: (rhs[0] / ATA[0, 0], rhs[1] / ATA[1, 1])
part(L3, 'p-gas-hubs', 2, tup(fN), {'diagonal': diag(A.T * yN), 'swapped': tup(fN)[::-1], 'no-sign': (fN[0], -fN[1])})
part(L3, 'p-gas-hubs', 3, tup(fS), {'diagonal': diag(A.T * yS), 'no-sign': (fS[0], -fS[1])})
sprd = yN - yS
fD = ATA.inv() * A.T * sprd
ok(fD == fN - fS, 'gas: the fit of the difference is the difference of the fits')
part(L3, 'p-gas-hubs', 4, tup(fD), {'added': tup(fN + fS), 'reversed': tup(fS - fN)})
ok(tup(sprd) == (R(3, 2), -1, R(3, 2), -1, -1) and sum(sprd) == 0, 'gas: the spread series and its zero mean')
r2 = lambda yv_, f: 1 - (yv_ - A * f).dot(yv_ - A * f) / sum((v - sum(yv_) / 5) ** 2 for v in yv_)
eN, eS = yN - A * fN, yS - A * fS
part(L3, 'p-gas-hubs', 5, r2(sprd, fD), {'ratio': 1 - r2(sprd, fD), 'added-sse': 1 - (eN.dot(eN) + eS.dot(eS)) / sprd.dot(sprd), 'hub-n': r2(yN, fN)}, tol=0.0005)
ok(eN.dot(eN) == R(3, 2) and eS.dot(eS) == R(3, 2) and abs(float(r2(yN, fN)) - (1 - 1.5 / 41.5)) < 1e-12, 'gas: hub SSEs 1.5 and 1.5, hub N R2 = 1 - 1.5/41.5')
ok(abs(np.corrcoef(np.array(t, float).ravel(), np.array(sprd, float).ravel())[0, 1] ** 2 - 1 / 3) < 1e-12, 'gas: squared correlation is 1/3')
npA = np.column_stack([np.ones(5), np.array(t, float).ravel()])
printed = repr((npA.T @ npA).tolist())
if printed != '[[5, 5], [5, 15]]':
    claim(f'gas-hubs parts 2, 3: "`A.T @ A` prints `[[5, 5], [5, 15]]`"; with np.ones the array is float and prints {str(npA.T @ npA)!r}')

# ============================================================ set shape
for course, sets in (('elimination', (E1, E2, E3)), ('least-squares', (L1, L2, L3))):
    for n, S_ in enumerate(sets, 1):
        nparts = [len(it['parts']) for it in S_.values()]
        typed = sum(p['widget']['kind'] != 'choice' for it in S_.values() for p in it['parts'])
        diffs = [it['difficulty'] for it in S_.values()]
        ok(3 <= len(S_) <= 5 and all(3 <= v <= 5 for v in nparts), f'{course} {n}: 3 to 5 items of 3 to 5 parts')
        ok(all(3 <= v <= 5 for v in diffs) and 5 in diffs, f'{course} {n}: difficulty 3 to 5 with a 5')
        ok(typed * 3 >= sum(nparts) * 2, f'{course} {n}: two thirds typed')
        for it in S_.values():
            for i, p in enumerate(it['parts'], 1):
                w = p['widget']
                ok(len(re.split(r'(?<=\.)\s+(?=[A-Z$`])', p['explain']['text'].strip())) <= 4, f'{it["id"]} part {i}: explanation length')
                for x_ in w.get('wrong', []):
                    ok(x_['id'] in p['feedback'].get('byKey', {}), f'{it["id"]} part {i}: wrong {x_["id"]} has a line')
        print(f'{course} problems-{n}: {len(S_)} items, {sum(nparts)} parts, {typed} typed, difficulties {diffs}')

print(f'\n{checks} checks, {fails} failures')
for c in claims:
    print('CLAIM', c)
sys.exit(1 if fails else 0)
