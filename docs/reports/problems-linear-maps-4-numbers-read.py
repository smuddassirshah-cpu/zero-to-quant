#!/usr/bin/env python3
"""Second read of app/content/courses/linear-maps/problems-4.json (Operators).

Imports nothing from the author's script. Every matrix, vector and operator is typed here from the prose.
Route 1 is exact (sympy: eigenvects, nullspace, jordan_form, charpoly, minimal polynomial by Krylov vectors).
Route 2 is another method (numpy eigh / solve / matrix_power, the operator applied to polynomials by
differentiation, block sizes rebuilt from ranks of powers and from sympy's own Jordan form).
Keys and wrong[] values are read from the JSON and compared with the reader's own values.
Exit 0 when every check holds.

Run from the repo root: <scratchpad>/venv/bin/python docs/reports/problems-linear-maps-4-numbers-read.py
"""
import os as _os; _os.chdir(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..'))  # paths below are from the repository root
import json
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp

DOC = json.load(open("app/content/courses/linear-maps/problems-4.json"))
ITEMS = {it["id"]: it for it in DOC["items"]}
I = sp.I
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", msg)


def part(item, k):
    return ITEMS[item]["parts"][k - 1]


def tup(text):
    """'(5, 2-i)' -> sympy tuple."""
    s = text.strip().strip("()[]")
    s = re.sub(r"(\d)i", r"\1*I", s)
    s = re.sub(r"(?<![a-zA-Z])i(?![a-zA-Z])", "I", s)
    return tuple(sp.nsimplify(sp.sympify(c)) for c in s.split(","))


def key_tuple(item, k):
    return tup(part(item, k)["widget"]["answer"])


def wrongs(item, k):
    w = part(item, k)["widget"]
    return {x["id"]: (x.get("tex", x.get("value"))) for x in w.get("wrong", [])}


def same(a, b):
    return len(a) == len(b) and all(sp.simplify(x - y) == 0 for x, y in zip(a, b))


def text_of(item):
    return json.dumps(ITEMS[item], ensure_ascii=False).replace("\\\\", "\\")


# --------------------------------------------------------------------------------------------
# set shape
# --------------------------------------------------------------------------------------------
ok(DOC["level"] == 4 and DOC["course"] == "linear-maps" and 3 <= len(DOC["items"]) <= 5, "set shape")
LEVEL_SKILLS = set()
for l in ["l15-eigenvalues-exist", "l16-self-adjoint", "l17-spectral-theorem", "l18-generalised-eigenvectors", "l19-jordan-form"]:
    LEVEL_SKILLS |= set(json.load(open(f"app/content/courses/linear-maps/{l}.json"))["skills"])
typed = total = 0
for it in DOC["items"]:
    ok(3 <= len(it["parts"]) <= 5, f"{it['id']}: 3 to 5 parts")
    ok(3 <= it["difficulty"] <= 5, f"{it['id']}: difficulty 3 to 5")
    ok(set(it["skills"]) <= LEVEL_SKILLS, f"{it['id']}: skills from the level")
    for p in it["parts"]:
        total += 1
        typed += p["widget"]["kind"] in ("numeric", "expression")
        ok("explain" in p and "feedback" in p, f"{it['id']}: feedback and explain")
        for x in p["widget"].get("wrong", []):
            ok(x["id"] in p["feedback"].get("byKey", {}), f"{it['id']}: wrong {x['id']} has a byKey line")
ok(any(it["difficulty"] == 5 for it in DOC["items"]), "one difficulty 5")
ok(Fr(typed, total) >= Fr(2, 3), "two thirds typed")

# --------------------------------------------------------------------------------------------
# p-footbridge-modes: S = [[6, 2+i], [2-i, 2]] on C^2
# --------------------------------------------------------------------------------------------
P = "p-footbridge-modes"
S = sp.Matrix([[6, 2 + I], [2 - I, 2]])
v = sp.Matrix([1, 0])
ok(S.H == S, "S is self-adjoint (S* = S)")
Sv, S2v = S * v, S * S * v
ok(same(tuple(Sv), (6, 2 - I)), "Sv = (6, 2 - i)")
ok(same(tuple(S2v), (41, 16 - 8 * I)), "S^2 v = (41, 16 - 8i) as the feedback prints")
ok(sp.expand((2 + I) * (2 - I)) == 5, "(2 + i)(2 - i) = 5")
# part 1, route 1: solve S^2 v = a Sv + b v
a, b = sp.symbols("a b")
sol = sp.solve(list(S2v - a * Sv - b * v), [a, b], dict=True)[0]
ok((sol[a], sol[b]) == (8, -7), "part 1 (a, b) = (8, -7) by solve")
# route 2: Cayley-Hamilton, S^2 = tr(S) S - det(S) I
ok((S.trace(), -S.det()) == (8, -7), "part 1 by trace and determinant")
ok(same(key_tuple(P, 1), (8, -7)), "part 1 key")
w1 = wrongs(P, 1)
ok(same(tup(w1["i-squared"]), (8, 36 + 3 - 48)), "part 1 i-squared: (2+i)(2-i) taken as 3 gives b = -9")
ok(same(tup(w1["sign"]), (8, 7)), "part 1 sign slip (8, 7)")
for k_, t_ in w1.items():
    ok(not same(tup(t_), (8, -7)), f"part 1 wrong {k_} differs from key")
# independence of v, Sv (so a, b are unique)
ok(sp.Matrix.hstack(v, Sv).det() != 0, "v and Sv independent, so (a, b) is unique")
# part 2
z = sp.symbols("z")
roots = sorted(sp.roots(z**2 - 8 * z + 7, z, multiple=True))
ok(roots == [1, 7], "part 2 roots 1 and 7")
ev = sorted(S.eigenvals(multiple=True))
ok(ev == [1, 7], "eigenvalues of S by sympy are 1 and 7")
evn = np.linalg.eigvalsh(np.array(S.tolist(), dtype=complex))
ok(np.allclose(evn, [1, 7]), "eigenvalues of S by numpy eigvalsh")
ok(sorted(part(P, 2)["widget"]["answers"]) == [1, 7], "part 2 key")
ok(sorted(sp.roots(z**2 + 8 * z + 7, z, multiple=True)) == [-7, -1], "part 2 wrong: -1, -7 solve z^2 + 8z + 7")
ok(part(P, 2)["widget"]["wrong"][0]["value"].replace(" ", "") == "-1,-7", "part 2 wrong value")
ok(sum(roots) == S.trace() and roots[0] * roots[1] == S.det(), "part 2 explain: sum is the trace, product the determinant")
# part 3
w = (S - sp.eye(2)) * v
ok(same(tuple(w), (5, 2 - I)), "part 3 w = (5, 2 - i)")
ok(same(key_tuple(P, 3), tuple(w)), "part 3 key")
ok((S * w - 7 * w).applyfunc(sp.expand) == sp.zeros(2, 1), "Sw = 7w")
ok(same(tuple(S * w), (35, 7 * (2 - I))), "feedback: Sw = (30 + 5, 7(2 - i))")
w3 = wrongs(P, 3)
other = (S - 7 * sp.eye(2)) * v
ok(same(tup(w3["other-factor"]), tuple(other)), "part 3 other-factor is (S - 7I)v")
ok((S * other - other).applyfunc(sp.expand) == sp.zeros(2, 1), "(S - 7I)v is an eigenvector for 1, as its line says")
ok(same(tup(w3["plus"]), tuple(Sv + v)), "part 3 plus is Sv + v")
# route 2: nullspace of S - 7I is the line through w
ns7 = (S - 7 * sp.eye(2)).nullspace()
ok(len(ns7) == 1 and sp.Matrix.hstack(ns7[0], w).det().expand() == 0, "ker(S - 7I) is the line through w")
# part 4
u = sp.Matrix([-2 - I, 5])
inner = lambda x, y: sp.expand(sum(xi * sp.conjugate(yi) for xi, yi in zip(x, y)))
ok(inner(u, w) == 0, "<u, w> = 0")
ok((S * u - u).applyfunc(sp.expand) == sp.zeros(2, 1), "Su = u")
u1 = sp.symbols("u1")
ok(sp.solve(inner(sp.Matrix([u1, 5]), w), u1) == [-2 - I], "part 4 by solving <u, w> = 0 with u2 = 5")
ns1 = (S - sp.eye(2)).nullspace()[0]
ns1 = (ns1 * 5 / ns1[1]).applyfunc(sp.simplify)
ok(same(tuple(ns1), tuple(u)), "part 4 by the kernel of S - I scaled to second entry 5")
ok(same(key_tuple(P, 4), tuple(u)), "part 4 key")
w4 = wrongs(P, 4)
noconj = sp.solve(sp.expand(u1 * w[0] + 5 * w[1]), u1)[0]
ok(same(tup(w4["no-conjugate"]), (noconj, 5)), "part 4 no-conjugate: bilinear form gives (-2 + i, 5)")
ok(same(tup(w4["sign"]), (2 + I, 5)), "part 4 sign")
ok(inner(sp.Matrix([2 + I, 5]), w) == sp.expand(10 * (2 + I)), "part 4 sign line: 5(2+i) + 5(2+i)")
for k_, t_ in w4.items():
    ok(inner(sp.Matrix(tup(t_)), w) != 0, f"part 4 wrong {k_} is not perpendicular to w")
# part 5
nw2, nu2 = inner(w, w), inner(u, u)
ok((nw2, nu2) == (30, 30), "|w|^2 = |u|^2 = 30")
q1, q2 = w / sp.sqrt(30), u / sp.sqrt(30)
rebuilt = (7 * q1 * q1.H + q2 * q2.H).applyfunc(sp.simplify)
ok(rebuilt == S, "S = 7 q1 q1* + q2 q2*")
m7 = (7 * q1 * q1.H)[0, 0]
frac = sp.nsimplify(m7 / S[0, 0])
ok(m7 == sp.Rational(35, 6) and frac == sp.Rational(35, 36), "part 5: mode carries 35/6, fraction 35/36")
# route 2 numeric
vals, vecs = np.linalg.eigh(np.array(S.tolist(), dtype=complex))
num = vals[1] * abs(vecs[0, 1]) ** 2 / 6
ok(abs(num - 35 / 36) < 1e-12, "part 5 numerically by eigh")
W5 = part(P, 5)["widget"]
ok(abs(W5["answer"] - 35 / 36) <= W5["tol"]["abs"], "part 5 key band holds 35/36")
ok(abs(0.972 - W5["answer"]) <= W5["tol"]["abs"], "part 5 key band takes 0.972")
slips = {"weight": Fr(5, 6), "trace-share": Fr(7, 8), "power": Fr(35, 6)}
for x in W5["wrong"]:
    ok(abs(float(slips[x["id"]]) - x["value"]) <= x["tol"]["abs"], f"part 5 wrong {x['id']} holds its slip value")
    ok(abs(x["value"] - W5["answer"]) > x["tol"]["abs"] + W5["tol"]["abs"], f"part 5 wrong {x['id']} band clear of key band")
ok(sp.expand((q2 * q2.H)[0, 0]) == sp.Rational(1, 6) and sp.Rational(35, 6) + sp.Rational(1, 6) == 6, "explain: mode for 1 carries 1/6; 35/6 + 1/6 = 6")
ok(S.trace() == 8, "trace-share line: tr S = 8")
ok(all(e > 0 for e in ev), "S is positive definite, as a matrix of powers must be")

# --------------------------------------------------------------------------------------------
# p-spring-linkage: K symmetric 3x3
# --------------------------------------------------------------------------------------------
P = "p-spring-linkage"
K = sp.Matrix([[4, -2, 2], [-2, 5, 0], [2, 0, 3]])
ok(K.T == K, "K symmetric")
e1, e2, e3 = sp.Matrix([1, 2, 2]), sp.Matrix([2, 1, -2]), sp.Matrix([2, -2, 1])
ok(tuple(K * e1) == (4, 8, 8), "K(1,2,2) = (4,8,8)")
ok(part(P, 1)["widget"]["answer"] == 4, "part 1 key 4")
lam = sp.symbols("lam")
ok(sp.factor(K.charpoly(lam).as_expr()) == (lam - 1) * (lam - 4) * (lam - 7), "char poly (lam-1)(lam-4)(lam-7)")
ok(np.allclose(np.linalg.eigvalsh(np.array(K.tolist(), dtype=float)), [1, 4, 7]), "eigenvalues 1, 4, 7 by numpy")
w1 = {x["id"]: x["value"] for x in part(P, 1)["widget"]["wrong"]}
ok(w1 == {"entry": 8, "trace": 12} and K.trace() == 12 and (K * e1)[1] == 8, "part 1 wrong values")
# part 2
ns = (K - sp.eye(3)).nullspace()
ok(len(ns) == 1, "ker(K - I) is a line")
v2 = ns[0] * 2 / ns[0][0]
ok(tuple(v2) == (2, 1, -2) and same(key_tuple(P, 2), tuple(v2)), "part 2 key (2, 1, -2) from the kernel")
ok(tuple(K * e2) == tuple(e2), "K(2,1,-2) = (2,1,-2)")
ok((K - sp.eye(3)).tolist() == [[3, -2, 2], [-2, 4, 0], [2, 0, 2]], "K - I as printed")
w2 = wrongs(P, 2)
po = sp.Matrix(tup(w2["plane-only"]))
ok(po.dot(e1) == 0 and tuple(K * po) == (10, -9, 4), "part 2 plane-only: perpendicular, K(2,-1,0) = (10,-9,4)")
ok(tup(w2["sign"]) == (2, -1, -2) and K * sp.Matrix([2, -1, -2]) != sp.Matrix([2, -1, -2]), "part 2 sign is not an eigenvector")
ok(e1.dot(e2) == 0, "(1,2,2).(2,1,-2) = 0")
# part 3
cr = e1.cross(e2)
ok(tuple(cr) == (-6, 6, -3), "cross product (-6, 6, -3)")
ok(tuple(cr / -3) == (2, -2, 1) and same(key_tuple(P, 3), (2, -2, 1)), "part 3 key")
a_, b_, c_ = sp.symbols("a_ b_ c_")
s3 = sp.solve([a_ + 2 * b_ + 2 * c_, 2 * a_ + b_ - 2 * c_, a_ - 2], [a_, b_, c_])
ok((s3[a_], s3[b_], s3[c_]) == (2, -2, 1), "part 3 by two equations")
w3 = wrongs(P, 3)
ok(tup(w3["cross-sign"]) == (2, 2, 1) and e1.dot(sp.Matrix([2, 2, 1])) == 8, "part 3 cross-sign: dot product 8")
ok(tup(w3["unscaled"]) == tuple(cr), "part 3 unscaled is the cross product")
# part 4
ok(tuple(K * e3) == (14, -14, 7) and part(P, 4)["widget"]["answer"] == 7, "part 4: K(2,-2,1) = (14,-14,7), key 7")
ok(K.trace() - 4 - 1 == 7, "part 4 by the trace")
w4 = {x["id"]: x["value"] for x in part(P, 4)["widget"]["wrong"]}
ok(w4 == {"first-entry": 14, "trace-slip": 8}, "part 4 wrong values")
# part 5
F = sp.Matrix([28, 0, 0])
x_exact = K.LUsolve(F)
ok(tuple(x_exact) == (15, 6, -10), "part 5 by LU solve")
qs = [e / 3 for e in (e1, e2, e3)]
lams = [4, 1, 7]
ok(all(q.dot(q) == 1 for q in qs), "the three modes have length 3")
coef = [F.dot(q) for q in qs]
ok(coef == [sp.Rational(28, 3), sp.Rational(56, 3), sp.Rational(56, 3)], "<F, q_i> = 28/3, 56/3, 56/3")
x_sum = sum((c / l * q for c, l, q in zip(coef, lams, qs)), sp.zeros(3, 1))
ok(tuple(x_sum) == (15, 6, -10) and same(key_tuple(P, 5), (15, 6, -10)), "part 5 by the spectral sum; key")
ok([c / l / 3 for c, l in zip(coef, lams)] == [sp.Rational(7, 9), sp.Rational(56, 9), sp.Rational(8, 9)], "feedback multiples 7/9, 56/9, 8/9")
ok(np.allclose(np.linalg.solve(np.array(K.tolist(), dtype=float), [28, 0, 0]), [15, 6, -10]), "part 5 by numpy solve")
w5 = wrongs(P, 5)
ok(tup(w5["times"]) == tuple(K * F), "part 5 times is KF")
x_unit = sum((F.dot(e) / l * e for l, e in zip(lams, (e1, e2, e3))), sp.zeros(3, 1))
ok(tup(w5["unit"]) == tuple(x_unit) and tuple(x_unit) == tuple(9 * x_exact), "part 5 unit: 9 times too big")
ok(tuple(K * x_exact) == (28, 0, 0), "explain check K(15,6,-10) = (28,0,0)")
norms = [abs(c / l) for c, l in zip(coef, lams)]
ok(norms[1] > norms[0] + norms[2], "explain: the mode with eigenvalue 1 gives most of the movement")
# Q^T K Q diagonal (spectral theorem claim)
Q = sp.Matrix.hstack(*qs)
ok(Q.T * Q == sp.eye(3) and Q.T * K * Q == sp.diag(4, 1, 7), "Q orthogonal and Q^T K Q = diag(4, 1, 7)")

# --------------------------------------------------------------------------------------------
# p-curvature-operator: T p = p + p'' on P_3
# --------------------------------------------------------------------------------------------
P = "p-curvature-operator"
x, t = sp.symbols("x t")
basis = [sp.Integer(1), x, x**2, x**3]
Top = lambda p: sp.expand(p + sp.diff(p, x, 2))
coords = lambda p: tuple(sp.Poly(p, x).coeff_monomial(x**k) for k in range(4))
M = sp.Matrix([coords(Top(bp)) for bp in basis]).T
ok(M == sp.Matrix([[1, 0, 2, 0], [0, 1, 0, 6], [0, 0, 1, 0], [0, 0, 0, 1]]), "[T] = I + (2 and 6 above the diagonal)")
ok(coords(Top(x**3)) == (0, 6, 0, 1) and same(key_tuple(P, 1), (0, 6, 0, 1)), "part 1 key")
w1 = wrongs(P, 1)
ok(tup(w1["one-derivative"]) == coords(x**3 + sp.diff(x**3, x)), "part 1 one-derivative is p + p'")
ok(tup(w1["half"]) == (0, 3, 0, 1), "part 1 half")
ok([Top(bp) for bp in basis[:3]] == [1, x, x**2 + 2], "explain: T1 = 1, Tx = x, Tx^2 = x^2 + 2")
N = M - sp.eye(4)
d1, d2 = 4 - N.rank(), 4 - (N * N).rank()
ok((d1, d2) == (2, 4) and same(key_tuple(P, 2), (2, 4)), "part 2 (d1, d2) = (2, 4) by ranks")
ok(len(N.nullspace()) == 2 and N * N == sp.zeros(4), "ker N has dimension 2 and N^2 = 0")
# route 2: on polynomials
gen = sum(c * bp for c, bp in zip(sp.symbols("c0:4"), basis))
ok(sp.Poly(sp.diff(gen, x, 2), x).all_coeffs() == [6 * sp.Symbol("c3"), 2 * sp.Symbol("c2")], "p'' = 0 forces c2 = c3 = 0")
ok(sp.diff(gen, x, 4) == 0, "p'''' = 0 for every p in P_3")
w2 = wrongs(P, 2)
ok(tup(w2["one-chain"]) == (1, 2) and tup(w2["alg"]) == (4, 4), "part 2 wrong values")
# part 3: block sizes
at_least = [d1 - 0, d2 - d1]
sizes = sorted([sum(1 for n_ in at_least if n_ >= j + 1) for j in range(at_least[0])])
ok(sizes == [2, 2] and sorted(part(P, 3)["widget"]["answers"]) == [2, 2], "part 3 blocks 2 and 2 from d_k - d_(k-1)")
Pm, J = M.jordan_form()
ok(J == sp.Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]]), "sympy jordan_form: J_2(1) + J_2(1)")
J31 = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
N31 = J31 - sp.eye(4)
ok((4 - N31.rank(), 4 - (N31**2).rank()) == (2, 3), "three-one line: J_3 + J_1 has d = (2, 3)")
ok(part(P, 3)["widget"]["wrong"][0]["value"].replace(" ", "") == "3,1", "part 3 wrong value")
B = sp.Matrix([coords(p_) for p_ in (6 * x, x**3, sp.Integer(2), x**2)]).T
ok(B.inv() * M * B == J, "explain: in the basis (6x, x^3, 2, x^2) the matrix of T is its Jordan form")
ok(sp.diff(x**3, x, 2) == 6 * x and sp.diff(6 * x, x, 2) == 0 and sp.diff(x**2, x, 2) == 2, "chains x^3 -> 6x -> 0 and x^2 -> 2 -> 0")
# part 4
alg = sp.roots(M.charpoly(lam).as_expr(), lam)
ok(alg == {1: 4} and len((M - sp.eye(4)).nullspace()) == 2 and same(key_tuple(P, 4), (4, 2)), "part 4 (a, g) = (4, 2)")
ok(not M.is_diagonalizable(), "T is not diagonalisable")
ok(sp.factor(M.charpoly(lam).as_expr()) == (lam - 1) ** 4, "char poly (lam - 1)^4")
w4 = wrongs(P, 4)
ok(tup(w4["swapped"]) == (2, 4) and tup(w4["one-block"]) == (2, 2), "part 4 wrong values")
# part 5
for n_ in range(1, 9):
    p_ = x**3
    for _ in range(n_):
        p_ = Top(p_)
    ok(p_ == x**3 + 6 * n_ * x, f"T^{n_}(x^3) = x^3 + {6 * n_}x by applying T")
    ok(coords(x**3 + 6 * n_ * x) == tuple(M**n_ * sp.Matrix([0, 0, 0, 1])), f"T^{n_}(x^3) by matrix power")
key5 = sp.sympify(part(P, 5)["widget"]["answer"].replace("^", "**").replace("6tx", "6*t*x"))
ok(sp.expand(key5 - (x**3 + 6 * t * x)) == 0, "part 5 key x^3 + 6tx")
tt = sp.symbols("tt", integer=True, positive=True)
J2 = sp.Matrix([[lam, 1], [0, lam]])
ok(all((J2**n_)[0, 1] == n_ * lam ** (n_ - 1) for n_ in range(1, 7)), "explain: top-right entry of J_2(lam)^t is t lam^(t-1)")
ok(Top(x**3 + 6 * x) == x**3 + 12 * x, "explain check t = 2")
ok(Top(6 * x) == 6 * x, "power line: T(6x) = 6x")
w5 = wrongs(P, 5)
ok(w5 == {"no-t": "x^3+6x", "power": "x^3+6^tx"}, "part 5 wrong texts")
ok(all(x**3 + 6**n_ * x != x**3 + 6 * n_ * x for n_ in range(2, 6)), "part 5 power slip differs from key for t >= 2")

# --------------------------------------------------------------------------------------------
# numbers printed in prose (spot text checks)
# --------------------------------------------------------------------------------------------
tx = text_of("p-footbridge-modes")
for s_ in ["(41, 16 - 8i)", "z^2 - 8z + 7", "\\tfrac{35}{36} \\approx 0.972", "\\tfrac{25}{30} = \\tfrac56", "\\tfrac{35}{6} + \\tfrac16 = 6"]:
    ok(s_ in tx, f"footbridge text holds {s_}")
ok(round(35 / 36, 3) == 0.972 and round(5 / 6, 3) == 0.833 and round(35 / 6, 3) == 5.833 and 7 / 8 == 0.875, "decimals 0.972, 0.833, 5.833, 0.875")
tx = text_of("p-spring-linkage")
for s_ in ["(4 - 4 + 4, -2 + 10, 2 + 6) = (4, 8, 8)", "(8 + 4 + 2, -4 - 10, 4 + 3) = (14, -14, 7)", "(60 - 12 - 20, -30 + 30, 30 - 30) = (28, 0, 0)", "12 - 4 - 1 = 7"]:
    ok(s_ in tx, f"linkage text holds {s_}")
ok((4 - 4 + 4, -2 + 10, 2 + 6) == (4, 8, 8) and (8 + 4 + 2, -4 - 10, 4 + 3) == (14, -14, 7) and (60 - 12 - 20, -30 + 30, 30 - 30) == (28, 0, 0), "printed sums")

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
