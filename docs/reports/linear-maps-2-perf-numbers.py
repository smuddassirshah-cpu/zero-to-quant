"""linear-maps L2 performance task h-prove-commutator-rank: every stated fact and number, checked twice in exact arithmetic.

Run from the repository root with the venv that has sympy:
    <venv>/bin/python -I docs/reports/linear-maps-2-perf-numbers.py
Routes: T(X) = AX - XA multiplied out symbolically, against the 4 x 4 matrix of T in the basis (E11, E12, E21, E22)
with exact ranks, null spaces and augmented ranks; random rational matrices for linearity and the solution family.
"""
import itertools
import json
import os
import random
import sys

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("linear-maps", 2)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'linear-maps', 'homework-2.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-commutator-rank']
lv.claim(len(idx) == 1, "the item exists once")
I_ = idx[0]
it = items[I_]
M = f"items[{I_}].model"
rnd = random.Random(20261109)

A = sp.Matrix([[1, 1], [0, 2]])
I2 = sp.eye(2)
a, b, c, d = sp.symbols('a b c d')
X = sp.Matrix([[a, b], [c, d]])


def T(Y):
    return (A * Y - Y * A).applyfunc(sp.expand)


def E(i, j):
    return sp.Matrix(2, 2, lambda r, s: 1 if (r, s) == (i, j) else 0)


def vec(Y):
    return sp.Matrix(list(Y))     # row-major: (y11, y12, y21, y22)


Es = [E(0, 0), E(0, 1), E(1, 0), E(1, 1)]
MT = sp.Matrix.hstack(*[vec(T(e)) for e in Es])   # the matrix of T in (E11, E12, E21, E22)

# (a) linearity on random rational matrices, and the matrix route
def rmat():
    return sp.Matrix(2, 2, lambda i, j: sp.Rational(rnd.randint(-30, 30), rnd.randint(1, 9)))

ok_add = ok_mul = ok_mat = True
for _ in range(300):
    P_, Q_ = rmat(), rmat()
    lam = sp.Rational(rnd.randint(-30, 30), rnd.randint(1, 9))
    ok_add &= T(P_ + Q_) == T(P_) + T(Q_)
    ok_mul &= T(lam * P_) == lam * T(P_)
    ok_mat &= vec(T(P_)) == MT * vec(P_)
lv.claim(ok_add and ok_mul, "T(X + Y) = TX + TY and T(lam X) = lam TX on 300 random pairs")
lv.claim(ok_mat, "the 4 x 4 matrix of T reproduces T on 300 random matrices")

# (b) the products and the formula
lv.claim((A * X).applyfunc(sp.expand) == sp.Matrix([[a + c, b + d], [2*c, 2*d]]), "AX = [[a + c, b + d], [2c, 2d]]")
lv.claim((X * A).applyfunc(sp.expand) == sp.Matrix([[a, a + 2*b], [c, c + 2*d]]), "XA = [[a, a + 2b], [c, c + 2d]]")
lv.claim(T(X) == sp.Matrix([[c, d - a - b], [c, -c]]), "T(X) = [[c, d - a - b], [c, -c]]")
sol = sp.solve(list(T(X)), [c, d], dict=True)
lv.claim(sol == [{c: 0, d: a + b}], "T(X) = 0 exactly when c = 0 and d = a + b (solve)")
ns = MT.nullspace()
lv.claim(len(ns) == 2 and 4 - MT.rank() == 2, "nullity 2 by null space and by 4 - rank")
lv.claim(sp.Matrix.hstack(*ns, vec(I2), vec(A)).rank() == 2 and sp.Matrix.hstack(vec(I2), vec(A)).rank() == 2,
         "ker T = span(I, A) (same rank-2 span as the null space)")
lv.claim(T(I2) == sp.zeros(2) and T(A) == sp.zeros(2), "T(I) = 0 and T(A) = A^2 - A^2 = 0")
lv.claim(((a - b) * I2 + b * A).applyfunc(sp.expand) == sp.Matrix([[a, b], [0, a + b]]), "(a - b) I + b A = [[a, b], [0, a + b]]")
s_, t_ = sp.symbols('s t')
lv.claim(sp.solve(list(s_ * I2 + t_ * A), [s_, t_], dict=True) == [{s_: 0, t_: 0}], "s I + t A = 0 only for s = t = 0")

# (c) the extension and the images
E12, E21 = E(0, 1), E(1, 0)
ext = [I2, A, E12, E21]
lv.claim(sp.Matrix.hstack(*[vec(Y) for Y in ext]).det() != 0, "(I, A, E12, E21) is a basis of R^{2x2} (det != 0)")
lv.claim(A - I2 - E12 == E(1, 1) and I2 - E(1, 1) == E(0, 0), "E22 = A - I - E12 and E11 = I - E22")
lv.claim(T(E12) == sp.Matrix([[0, -1], [0, 0]]) and T(E21) == sp.Matrix([[1, 0], [1, -1]]), "T(E12) and T(E21) as stated")
lv.claim(T(X).subs({a: 0, b: 1, c: 0, d: 0}) == T(E12) and T(X).subs({a: 0, b: 0, c: 1, d: 0}) == T(E21), "the images agree with the formula")
imgs = sp.Matrix.hstack(vec(T(E12)), vec(T(E21)))
lv.claim(imgs.rank() == 2 and MT.rank() == 2 and sp.Matrix.hstack(MT, imgs).rank() == 2, "T(E12), T(E21) are independent and span the column space of T")
u_, v_ = sp.symbols('u v')
lv.claim((u_ * T(E12) + v_ * T(E21)) == sp.Matrix([[v_, -u_], [v_, -v_]]), "u T(E12) + v T(E21) = [[v, -u], [v, -v]]")
lv.claim(4 == 2 + 2 and MT.shape[1] == len(ns) + MT.rank(), "rank-nullity: 4 = 2 + 2")
# any other extension also works, as the proof says: random completions of (I, A)
ok_any = True
for _ in range(100):
    Y1, Y2 = (sp.Matrix(2, 2, lambda i, j: rnd.randint(-3, 3)) for _ in range(2))
    if sp.Matrix.hstack(vec(I2), vec(A), vec(Y1), vec(Y2)).det() == 0:
        continue
    ok_any &= sp.Matrix.hstack(vec(T(Y1)), vec(T(Y2))).rank() == 2
lv.claim(ok_any, "for random completions of (I, A) to a basis, the two images are independent")

# (d) B1 and B2
B1 = sp.Matrix([[2, 3], [2, -2]])
B2 = sp.Matrix([[1, 0], [0, -1]])
Xp = sp.Matrix([[0, 0], [2, 3]])
lv.claim(T(Xp) == B1, "T(X_p) = B1")
gen = sp.solve(list(T(X) - B1), [c, d], dict=True)
lv.claim(gen == [{c: 2, d: a + b + 3}], "solve: c = 2 and d = a + b + 3, with a, b free (two parameters)")
fam = Xp + s_ * I2 + t_ * A
lv.claim(fam == sp.Matrix([[s_ + t_, t_], [2, 3 + s_ + 2*t_]]), "X_p + s I + t A = [[s + t, t], [2, 3 + s + 2t]]")
lv.claim(T(fam).applyfunc(sp.expand) == B1, "every member of the family solves T(X) = B1 (symbolic)")
ok_fam = True
for _ in range(200):
    av, bv = sp.Rational(rnd.randint(-40, 40), rnd.randint(1, 9)), sp.Rational(rnd.randint(-40, 40), rnd.randint(1, 9))
    Y = sp.Matrix([[av, bv], [2, av + bv + 3]])
    ss, tt = av - bv, bv          # the same matrix as X_p + s I + t A
    ok_fam &= T(Y) == B1 and Y == Xp + ss * I2 + tt * A
lv.claim(ok_fam, "200 random solutions from solve are X_p + s I + t A with s = a - b, t = b")
lv.claim(sp.Matrix.hstack(MT, vec(B1)).rank() == 2, "B1 is in im T (augmented rank 2)")
lv.claim(sp.Matrix.hstack(MT, vec(B2)).rank() == 3, "B2 is not in im T (augmented rank 3)")
lv.claim(sp.solve(list(T(X) - B2), [a, b, c, d], dict=True) == [], "solve finds no X with T(X) = B2")
lv.claim(B2[0, 0] != B2[1, 0], "B2 has 1 top left and 0 bottom left")

# (e) the trace
lv.claim(sp.expand(T(X).trace()) == 0, "tr T(X) = c - c = 0 (symbolic)")
tr_row = sp.Matrix([[1, 0, 0, 1]])
lv.claim(len(tr_row.nullspace()) == 3 and 4 - tr_row.rank() == 3 and E(0, 0).trace() == 1, "trace-0 matrices: dimension 3 by null space and by 4 - 1; tr E11 = 1")
lv.claim(all((tr_row * vec(T(e)))[0] == 0 for e in Es), "im T lies in the trace-0 matrices")
lv.claim(B2.trace() == 0 and MT.rank() == 2 < 3, "B2 has trace 0 and the rank 2 is below 3")

# numbers and lines the model states
for s in ["4 = 2 + 2", "4 - 2 = 2", "4 - 1 = 3", "(0, 0, 2, 3)", "(0, 1, 0, 0)", "(0, 0, 1, 0)", "(a - b)", "c + (-c) = 0"]:
    lv.expect("homework", M, s)

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
lv.claim(all(2 in s and 3 in s for s in passes), "every pass proves the rank-nullity construction and counts solutions")

lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x_ in items if x_.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(x_.get('difficulty') == 5 for x_ in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")
lv.claim('Axler' not in s, "no book citation in the item")

lv.report()
