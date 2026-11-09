"""linear-maps L1 performance task h-prove-extend-basis: every stated fact and number, checked twice in exact arithmetic.

Run from the repository root with the venv that has sympy:
    <venv>/bin/python -I docs/reports/linear-maps-1-perf-numbers.py
Routes: polynomials by sympy evaluation and expansion, against coefficient vectors in (1, x, x^2, x^3) with exact
ranks and null spaces; random members of U written in the basis by solving exactly.
"""
import itertools
import json
import os
import random
import sys

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("linear-maps", 1)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'linear-maps', 'homework-1.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-extend-basis']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"
P = f"items[{I}].prompt"
rnd = random.Random(20261109)

x = sp.symbols('x')
a0, a1, a2, a3 = sp.symbols('a0:4')
q1 = x**2 - 2*x
q2 = x**3 - 3*x**2 + 2*x
one = sp.Integer(1)
w3 = x**3 - 4*x


def vec(p):
    """coefficient vector of p in (1, x, x^2, x^3)"""
    pol = sp.Poly(sp.expand(p), x)
    return sp.Matrix([pol.coeff_monomial(x**k) for k in range(4)])


def inU_eval(p):
    return sp.expand(p).subs(x, 0) == sp.expand(p).subs(x, 2)


ROW = sp.Matrix([[0, 2, 4, 8]])   # p(2) - p(0) as a row acting on coefficient vectors


def inU_row(p):
    return (ROW * vec(p))[0] == 0


def rank(*ps):
    return sp.Matrix.hstack(*[vec(p) for p in ps]).rank()


# the condition p(0) = p(2)
gen = a0 + a1*x + a2*x**2 + a3*x**3
lv.claim(sp.expand(gen.subs(x, 2) - gen.subs(x, 0)) == 2*a1 + 4*a2 + 8*a3, "p(2) - p(0) = 2a1 + 4a2 + 8a3 (sympy)")
lv.claim(all((ROW * vec(x**k))[0] == 2**k - 0**k for k in range(4)), "the row (0, 2, 4, 8) is 2^k - 0^k on each x^k")
lv.claim(sp.solve(2*a1 + 4*a2 + 8*a3, a1) == [-2*a2 - 4*a3], "p in U exactly when a1 = -2a2 - 4a3")

# (a) subspace: zero, sums, multiples, on random members, both tests
def rand_U():
    b0, b2, b3 = (sp.Integer(rnd.randint(-9, 9)) for _ in range(3))
    return b0 + (-2*b2 - 4*b3)*x + b2*x**2 + b3*x**3

lv.claim(inU_eval(sp.Integer(0)) and inU_row(sp.Integer(0)), "0 is in U")
ok_sum = ok_mul = True
for _ in range(300):
    p, q = rand_U(), rand_U()
    lam = sp.Rational(rnd.randint(-20, 20), rnd.randint(1, 7))
    ok_sum &= inU_eval(p + q) and inU_row(p + q)
    ok_mul &= inU_eval(lam * p) and inU_row(lam * p)
lv.claim(ok_sum, "U closed under sums on 300 random pairs (evaluation and row)")
lv.claim(ok_mul, "U closed under multiples on 300 random pairs (evaluation and row)")

# (b) membership, by evaluation and by the row
for name, p in [("q1", q1), ("q2", q2), ("1", one), ("x^3 - 4x", w3), ("x^2 - 2x", x**2 - 2*x)]:
    lv.claim(inU_eval(p) and inU_row(p), f"{name} lies in U (evaluation and row)")
lv.claim(q1.subs(x, 2) == 0 and 2**2 - 2*2 == 0, "q1(2) = 4 - 4 = 0")
lv.claim(q2.subs(x, 2) == 0 and 8 - 12 + 4 == 0, "q2(2) = 8 - 12 + 4 = 0")
lv.claim(w3.subs(x, 2) == 0 and 8 - 8 == 0, "(x^3 - 4x)(2) = 8 - 8 = 0")
lv.claim(q1.subs(x, 0) == 0 and q2.subs(x, 0) == 0, "q1(0) = q2(0) = 0")
lv.claim(not inU_eval(x) and not inU_row(x), "x is not in U")

# independence of (q1, q2): rank, and solving a q1 + b q2 = 0
A, B = sp.symbols('A B')
sol = sp.solve(sp.Poly(sp.expand(A*q1 + B*q2), x).coeffs(), [A, B], dict=True)
lv.claim(sol == [{A: 0, B: 0}], "a q1 + b q2 = 0 only for a = b = 0 (solve)")
lv.claim(rank(q1, q2) == 2, "(q1, q2) has rank 2")
lv.claim(sp.Poly(q1, x).degree() == 2 and sp.Poly(q2, x).degree() == 3, "q1 has degree 2, q2 degree 3")

# the spanning list of U: substitution identity, and U as the null space of the row
lv.claim(sp.expand(gen.subs(a1, -2*a2 - 4*a3) - (a0*1 + a2*(x**2 - 2*x) + a3*w3)) == 0, "substituted p = a0 + a2(x^2 - 2x) + a3(x^3 - 4x)")
ns = ROW.nullspace()
lv.claim(len(ns) == 3 and 4 - ROW.rank() == 3, "U has dimension 3 by null space and by 4 - rank")
span_list = [one, x**2 - 2*x, w3]
lv.claim(rank(*span_list) == 3 and sp.Matrix.hstack(*ns, *[vec(p) for p in span_list]).rank() == 3,
         "(1, x^2 - 2x, x^3 - 4x) spans the null space of the row")

# the extension, run as the lesson's algorithm (keep a vector when it raises the rank)
kept = [q1, q2]
for w in span_list:
    if rank(*(kept + [w])) > rank(*kept):
        kept.append(w)
lv.claim([sp.expand(k) for k in kept] == [q1, q2, one], "the extension keeps 1 and skips x^2 - 2x and x^3 - 4x")
lv.claim(sp.expand(q2 + 3*q1 - w3) == 0, "x^3 - 4x = q2 + 3 q1 (expansion)")
c1, c2 = sp.symbols('c1 c2')
lv.claim(sp.solve(sp.Poly(sp.expand(c1*q1 + c2*q2 - w3), x).coeffs(), [c1, c2], dict=True) == [{c1: 3, c2: 1}], "x^3 - 4x = 3 q1 + 1 q2 (solve)")
lv.claim(sp.expand(x**3 - 3*x**2 + 2*x + 3*x**2 - 6*x) == w3, "the model's line x^3 - 3x^2 + 2x + 3x^2 - 6x = x^3 - 4x")
lv.claim(rank(q1, q2, one) == 3 and rank(q1, q2) == 2, "1 is not in span(q1, q2) (rank rises)")
lv.claim(all(sp.expand(sp.Integer(s) * q1 + sp.Integer(t) * q2).subs(x, 0) == 0 for s in range(-5, 6) for t in range(-5, 6)),
         "every combination of q1, q2 is 0 at x = 0 (grid)")

# (q1, q2, 1) is a basis of U: random members of U have exactly one set of coordinates
basis = [q1, q2, one]
Mb = sp.Matrix.hstack(*[vec(p) for p in basis])
ok_coord = True
for _ in range(200):
    p = rand_U()
    cs = sp.symbols('k0:3')
    s = sp.solve(list(Mb * sp.Matrix(cs) - vec(p)), cs, dict=True)
    ok_coord &= len(s) == 1 and sp.expand(sum(s[0][c] * b for c, b in zip(cs, basis)) - p) == 0
lv.claim(ok_coord, "200 random members of U each have one set of coordinates in (q1, q2, 1)")

# (c) every basis has length 3: random bases of U, four members always dependent, two never span
ok_len = ok_four = ok_two = True
for _ in range(200):
    Q = sp.Matrix(3, 3, lambda i, j: rnd.randint(-4, 4))
    if Q.det() == 0:
        continue
    newb = [sum(Q[i, j] * basis[i] for i in range(3)) for j in range(3)]
    ok_len &= rank(*newb) == 3 and all(inU_row(p) for p in newb)
    four = [rand_U() for _ in range(4)]
    ok_four &= rank(*four) <= 3
    two = [rand_U() for _ in range(2)]
    ok_two &= sp.Matrix.hstack(*[vec(p) for p in two]).rank() <= 2 < 3
lv.claim(ok_len, "random invertible recombinations of the basis are bases of U of length 3")
lv.claim(ok_four, "any four random members of U are dependent (rank at most 3)")
lv.claim(ok_two, "two members of U span at most a plane, so never U")

# (d) P3 = U (+) span(x)
cc = sp.symbols('cc')
lv.claim(sp.solve(sp.Eq((cc*x).subs(x, 0), (cc*x).subs(x, 2)), cc) == [0], "c x in U only for c = 0")
lv.claim(rank(q1, q2, one, x) == 4, "(q1, q2, 1, x) has rank 4 = dim P3")
lv.claim(3 + 1 - 0 == 4 and len(ns) + 1 == 4, "dimension formula 3 + 1 - 0 = 4")
ok_split = True
for _ in range(100):
    p = sum(sp.Integer(rnd.randint(-9, 9)) * x**k for k in range(4))
    t = (p.subs(x, 2) - p.subs(x, 0)) / 2      # the multiple of x to remove
    ok_split &= inU_eval(p - t*x)
lv.claim(ok_split, "every cubic is (member of U) + (p(2) - p(0))/2 times x, on 100 random cubics")

# the model states these lines
for s in ["4 - 4 = 0", "8 - 12 + 4 = 0", "8 - 8 = 0", "3 + 1 - 0 = 4", "q_2 + 3q_1", "a_1 = -2a_2 - 4a_3", "2a_1 + 4a_2 + 8a_3"]:
    lv.expect("homework", M, s)
lv.expect("homework", P, "p(0) = p(2)")

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 optional")
lv.claim('Optional' in it['prompt'].split('(d)')[1][:20], "part (d), the optional row, is marked optional in the prompt")
parts = {0: 'a', 1: 'b', 2: 'b', 3: 'c', 4: 'd'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({'a', 'b', 'c'} <= {parts[i] for i in s} for s in passes), "every pass covers (a), (b) and (c)")
lv.claim(all(1 in s and 2 in s for s in passes), "every pass has both (b) rows: the spanning list and the extension proved a basis")

lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x_ in items if x_.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(x_.get('difficulty') == 5 for x_ in items), "homework 6 to 12 items with a 5")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")
lv.claim('Axler' not in s, "no book citation in the item")

lv.report()
