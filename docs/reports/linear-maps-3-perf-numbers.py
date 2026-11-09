"""linear-maps L3 performance task h-prove-nearest-symmetric: every stated fact and number, checked twice in exact arithmetic.

Run from the repository root with the venv that has sympy and numpy:
    <venv>/bin/python -I docs/reports/linear-maps-3-perf-numbers.py
Routes: matrices as vectors of n^2 entries, so the inner product is the dot product. U-perp found as the exact null
space of the symmetric basis and compared with the antisymmetric matrices; the projection found by solving the normal
equations in sympy and compared with (X + X^T)/2; distances exact, then against a seeded random search over symmetric matrices.
"""
import itertools
import json
import os
import random
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("linear-maps", 3)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'linear-maps', 'homework-3.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-nearest-symmetric']
lv.claim(len(idx) == 1, "the item exists once")
I_ = idx[0]
it = items[I_]
M = f"items[{I_}].model"
rnd = random.Random(20261109)
rng = np.random.default_rng(20261109)


def ip(X, Y):
    return sum(X[i, j] * Y[i, j] for i in range(X.rows) for j in range(X.cols))


def E(n, i, j):
    return sp.Matrix(n, n, lambda r, s: 1 if (r, s) == (i, j) else 0)


def sym_basis(n):
    return [E(n, i, i) for i in range(n)] + [E(n, i, j) + E(n, j, i) for i in range(n) for j in range(i + 1, n)]


def anti_basis(n):
    return [E(n, i, j) - E(n, j, i) for i in range(n) for j in range(i + 1, n)]


def flat(X):
    return sp.Matrix(list(X))


# the inner product is the dot product of the entries
ok_ip = True
for _ in range(100):
    X = sp.Matrix(3, 3, lambda i, j: rnd.randint(-9, 9)); Y = sp.Matrix(3, 3, lambda i, j: rnd.randint(-9, 9))
    ok_ip &= ip(X, Y) == flat(X).dot(flat(Y)) == (X.T * Y).trace()
lv.claim(ok_ip, "sum x_ij y_ij = dot product of entries = tr(X^T Y), 100 random pairs")

for n in (2, 3, 4, 5):
    SB, AB = sym_basis(n), anti_basis(n)
    Smat = sp.Matrix.hstack(*[flat(S) for S in SB])
    # (a) U-perp as a null space: matrices orthogonal to every symmetric basis matrix
    perp = (Smat.T).nullspace()
    Amat = sp.Matrix.hstack(*[flat(K) for K in AB])
    same = sp.Matrix.hstack(*perp, Amat).rank() == Amat.rank() == len(perp)
    lv.claim(same, f"n = {n}: U-perp (null space) equals the span of the antisymmetric basis")
    lv.claim(all(ip(K, S) == 0 for K in AB for S in SB), f"n = {n}: every antisymmetric basis matrix is orthogonal to every symmetric one")
    # (e) dimensions two ways
    lv.claim(Smat.rank() == len(SB) == n * (n + 1) // 2 and len(perp) == n * (n - 1) // 2, f"n = {n}: dim U = n(n+1)/2, dim U-perp = n(n-1)/2")
    lv.claim(Smat.rank() + len(perp) == n * n and sp.Matrix.hstack(Smat, Amat).rank() == n * n, f"n = {n}: dims add to n^2 and the bases together span V")

# (a) subspace and the index swap, on random matrices
ok_sub = ok_swap = ok_test = True
for _ in range(100):
    P = sp.Matrix(3, 3, lambda i, j: rnd.randint(-9, 9))
    S1, S2 = P + P.T, sp.Matrix(3, 3, lambda i, j: rnd.randint(-9, 9))
    S2 = S2 + S2.T
    lam = sp.Rational(rnd.randint(-9, 9), rnd.randint(1, 5))
    ok_sub &= (S1 + S2).T == S1 + S2 and (lam * S1).T == lam * S1
    K = P - P.T
    ok_swap &= ip(K, S1) == -ip(K, S1) == 0
    X = sp.Matrix(3, 3, lambda i, j: rnd.randint(-9, 9))
    ok_test &= all(ip(X, E(3, i, j) + E(3, j, i)) == X[i, j] + X[j, i] for i in range(3) for j in range(3) if i != j) \
        and all(ip(X, E(3, i, i)) == X[i, i] for i in range(3))
lv.claim(ok_sub, "sums and multiples of symmetric matrices are symmetric (100 random)")
lv.claim(ok_swap, "<K, S> = -<K, S> = 0 for antisymmetric K, symmetric S (100 random)")
lv.claim(ok_test, "<X, E_ij + E_ji> = x_ij + x_ji and <X, E_ii> = x_ii (100 random)")

# (b), (c): the projection by normal equations equals (X + X^T)/2, and Pythagoras
SB3 = sym_basis(3)
G = sp.Matrix(len(SB3), len(SB3), lambda i, j: ip(SB3[i], SB3[j]))
ok_proj = ok_pyth = ok_min = True
for _ in range(60):
    X = sp.Matrix(3, 3, lambda i, j: sp.Rational(rnd.randint(-20, 20), rnd.randint(1, 4)))
    rhs = sp.Matrix([ip(X, S) for S in SB3])
    coef = G.LUsolve(rhs)
    PX = sum((coef[k] * SB3[k] for k in range(len(SB3))), sp.zeros(3))
    S = (X + X.T) / 2
    ok_proj &= PX == S and all(ip(X - S, B) == 0 for B in SB3)
    Sp = sp.Matrix(3, 3, lambda i, j: rnd.randint(-9, 9)); Sp = Sp + Sp.T
    ok_pyth &= ip(X - Sp, X - Sp) == ip(X - S, X - S) + ip(S - Sp, S - Sp)
    ok_min &= ip(X - Sp, X - Sp) >= ip(X - S, X - S) and (Sp == S or ip(X - Sp, X - Sp) > ip(X - S, X - S))
lv.claim(ok_proj, "normal equations give P_U X = (X + X^T)/2, residual orthogonal to U (60 random)")
lv.claim(ok_pyth, "||X - S'||^2 = ||X - S||^2 + ||S - S'||^2 for random symmetric S' (exact)")
lv.claim(ok_min, "strictly nearer than every other symmetric S' tried")

# (d) the stated matrix C
C = sp.Matrix([[4, 3, 0], [1, 9, 1], [2, -3, 1]])
lv.claim(C.T == sp.Matrix([[4, 1, 2], [3, 9, -3], [0, 1, 1]]), "C^T as stated")
S0 = (C + C.T) / 2
lv.claim(S0 == sp.Matrix([[4, 2, 1], [2, 9, -1], [1, -1, 1]]), "S0 = (C + C^T)/2 as stated")
K0 = C - S0
lv.claim(K0 == sp.Matrix([[0, 1, -1], [-1, 0, 2], [1, -2, 0]]) and K0.T == -K0, "C - S0 as stated, antisymmetric")
lv.claim(ip(K0, K0) == 12 and 1 + 1 + 1 + 1 + 4 + 4 == 12, "||C - S0||^2 = 12")
lv.claim(sp.sqrt(12) == 2 * sp.sqrt(3) and f"{float(sp.sqrt(12)):.3f}" == "3.464", "sqrt 12 = 2 sqrt 3 = 3.464")
S1 = sp.Matrix(3, 3, lambda i, j: C[min(i, j), max(i, j)])
lv.claim(S1 == sp.Matrix([[4, 3, 0], [3, 9, 1], [0, 1, 1]]), "the copied upper triangle S1 as stated")
lv.claim(C - S1 == sp.Matrix([[0, 0, 0], [-2, 0, 0], [2, -4, 0]]), "C - S1 as stated")
lv.claim(ip(C - S1, C - S1) == 24 and 4 + 4 + 16 == 24, "||C - S1||^2 = 24")
lv.claim(sp.sqrt(24) == 2 * sp.sqrt(6) and f"{float(sp.sqrt(24)):.3f}" == "4.899", "sqrt 24 = 2 sqrt 6 = 4.899")
D = S0 - S1
lv.claim(D == sp.Matrix([[0, -1, 1], [-1, 0, -2], [1, -2, 0]]) and ip(D, D) == 12 == 2 * (1 + 1 + 4), "S0 - S1 has -1, 1, -2 twice each, squared norm 12")
lv.claim(ip(C - S1, C - S1) == ip(K0, K0) + ip(D, D), "24 = 12 + 12 (Pythagoras from (c))")
# a numeric route: seeded random search over symmetric matrices never beats S0
Cn = np.array(C.tolist(), dtype=float)
S0n = np.array(S0.tolist(), dtype=float)
best = np.inf
for _ in range(200_000 // 1000):
    Z = rng.normal(scale=0.5, size=(1000, 3, 3))
    cand = S0n + (Z + np.transpose(Z, (0, 2, 1))) / 2
    d = np.sqrt(((Cn - cand) ** 2).sum(axis=(1, 2)))
    best = min(best, d.min())
lv.claim(best > np.sqrt(12) - 1e-12 and abs(np.sqrt(((Cn - S0n) ** 2).sum()) - 3.4641016) < 1e-6, f"200,000 random symmetric matrices: nearest {best:.4f} > 3.4641")
lv.claim(abs(np.linalg.norm(Cn - np.array(S1.tolist(), dtype=float)) - 4.8989795) < 1e-6, "numpy Frobenius norm of C - S1 is 4.899")
# the caution: symmetry only (positive semi-definiteness is a separate check)
A_ = sp.Matrix([[1, 4], [0, 1]])
lv.claim(min(((A_ + A_.T) / 2).eigenvals()) < 0, "a symmetric part can fail to be positive semi-definite, so the caution is needed")

for s_ in ["1 + 1 + 1 + 1 + 4 + 4 = 12", "3.464", "4 + 4 + 16 = 24", "4.899", "24 = 12 + 12", "2(1 + 1 + 4) = 12", "6 + 3 = 9"]:
    lv.expect("homework", M, s_)
for s_ in ["3.464", "4.899", "24 = 12 + 12"]:
    lv.expect("homework", f"items[{I_}].rubric[3].text", s_)

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 optional")
lv.claim(it['prompt'].split('(e)')[1].lstrip().startswith('Optional'), "part (e), the optional row, is marked optional in the prompt")
parts = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({'a', 'b', 'c', 'd'} <= {parts[i] for i in s} for s in passes), "every pass covers (a) to (d)")
lv.claim(all(1 in s and 2 in s for s in passes), "every pass has both halves of the objective: the split and the minimisation")

lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x_ in items if x_.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(x_.get('difficulty') == 5 for x_ in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")
lv.claim('Axler' not in s, "no book citation in the item")

lv.report()
