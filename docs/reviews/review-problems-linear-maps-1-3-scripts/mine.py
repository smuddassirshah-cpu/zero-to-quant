"""Second read, linear-maps problems-1 to -3: the reader's own recompute.

Imports nothing from the author's script. Every vector, matrix and polynomial is typed here from the
prose. Route 1 is exact (sympy, fractions); route 2 is another method (numpy solve, lstsq, rank, QR,
a brute-force search, or direct substitution). Each stored key and each stored `wrong` value is then
read from the JSON and compared with the value rebuilt here from the slip its line names.
A line starting CLAIM is a statement in the content that the recompute does not support (a finding).

Run from the repo root:  <venv>/bin/python docs/reviews/review-problems-linear-maps-1-3-scripts/mine.py
"""
import itertools
import json
import re
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, standard_transformations)

BASE = "app/content/courses/linear-maps/problems-%d.json"
SETS = {n: json.load(open(BASE % n)) for n in (1, 2, 3)}
checks = fails = claims = 0
x, y, t, k, lam = sp.symbols("x y t k lambda")
TR = standard_transformations + (implicit_multiplication_application, convert_xor)


def ok(label, cond):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", label)


def claim(label, cond):
    """A statement of the content. False = a finding, printed and counted apart."""
    global checks, claims
    checks += 1
    if not cond:
        claims += 1
        print("CLAIM", label)


def detex(s):
    s = re.sub(r"\\t?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    return s.replace("\\,", "")


def val(s):
    """A stored answer: number, tuple, pmatrix or polynomial -> sympy object."""
    if isinstance(s, (int, float)):
        return sp.nsimplify(s)
    s = detex(s)
    m = re.match(r"\\begin\{pmatrix\}(.*)\\end\{pmatrix\}", s)
    if m:
        return sp.Matrix([[parse_expr(c, transformations=TR) for c in r.split("&")]
                          for r in m.group(1).split("\\\\")])
    if s.startswith("("):
        inner = s[1:-1]
        parts, depth, cur = [], 0, ""
        for ch in inner:
            if ch == "," and depth == 0:
                parts.append(cur)
                cur = ""
            else:
                depth += ch == "("
                depth -= ch == ")"
                cur += ch
        parts.append(cur)
        if len(parts) > 1:
            return sp.Matrix([parse_expr(p, transformations=TR) for p in parts])
    return parse_expr(s, transformations=TR, local_dict={"x": x, "y": y, "t": t})


def same(a, b):
    if isinstance(a, sp.MatrixBase) or isinstance(b, sp.MatrixBase):
        return isinstance(a, sp.MatrixBase) and isinstance(b, sp.MatrixBase) and a.shape == b.shape \
            and sp.simplify(a - b) == sp.zeros(*a.shape)
    return sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0


def part(n, item, p):
    it = next(i for i in SETS[n]["items"] if i["id"] == item)
    return it["parts"][p - 1]


def key(n, item, p, mine, places=None):
    """The stored key equals mine (to `places` decimals if given); numeric bands hold the key only."""
    w = part(n, item, p)["widget"]
    lab = f"problems-{n} {item} part {p}"
    if w["kind"] == "numeric":
        if places is None:
            ok(lab + " key", same(val(w["answer"]), mine))
        else:
            ok(lab + " key", round(float(mine), places) == w["answer"])
            ok(lab + " band takes the exact value", abs(float(mine) - w["answer"]) <= w["tol"]["abs"])
    else:
        ok(lab + " key", same(val(w["answer"]), mine))
        for a in w.get("accept", []):
            ok(lab + " accept " + a, same(val(a.replace("[[", "(").replace("]]", ")")) if "[[" not in a
                                          else sp.Matrix(json.loads(re.sub(r"(-?\d+)/(\d+)", r'"\1/\2"', a))
                                                         ).applyfunc(sp.Rational), mine)
               or same(val(a.replace("[", "(").replace("]", ")")), mine) if "[[" not in a else True)


def wrongs(n, item, p, mine, places=None):
    """mine = {id: value}. Each stored wrong equals the slip rebuilt here, differs from the key, and has a line."""
    pr = part(n, item, p)
    w = pr["widget"]
    lab = f"problems-{n} {item} part {p}"
    stored = {e["id"]: e for e in w.get("wrong", [])}
    ok(lab + " wrong ids " + str(sorted(stored)) + " vs " + str(sorted(mine)), set(stored) == set(mine))
    for i, e in stored.items():
        ok(f"{lab} wrong {i} has a byKey line", i in pr["feedback"].get("byKey", {}))
        if i not in mine:
            continue
        sv = val(e["value"]) if "value" in e else val(e["tex"])
        if places is None:
            ok(f"{lab} wrong {i} value", same(sv, mine[i]))
        else:
            ok(f"{lab} wrong {i} value", abs(float(sv) - float(mine[i])) <= 0.5 * 10 ** -places + 1e-12)
        if w["kind"] == "numeric":
            ok(f"{lab} wrong {i} outside the key band", abs(float(sv) - w["answer"]) > w["tol"]["abs"] + e["tol"]["abs"])
        else:
            ok(f"{lab} wrong {i} differs from key", not same(sv, val(w["answer"])))


def choice(n, item, p, right_id, n_opts=4):
    w = part(n, item, p)["widget"]
    good = [o["id"] for o in w["options"] if o.get("correct")]
    ok(f"problems-{n} {item} part {p} one correct option {right_id}", good == [right_id] and len(w["options"]) == n_opts)
    ok(f"problems-{n} {item} part {p} every wrong option has a why", all("why" in o for o in w["options"] if not o.get("correct")))


M = sp.Matrix
V = lambda *a: sp.Matrix(list(a))

# ---------------------------------------------------------------- problems-1
# p-hedge-baskets
N = 1
I = "p-hedge-baskets"
cash = M([[1, 1, 1, 1]])
ok("prose: cash-neutral baskets have dimension 3", 4 - cash.rank() == 3 and len(cash.nullspace()) == 3)
# part 1: the four rules, tested on sums and multiples of baskets that obey them
rules = {
    "a": lambda w: w[0] == 2 * w[3],
    "b": lambda w: w[0] == 2 * w[3] + Fr(1, 10),
    "c": lambda w: w[0] * w[3] == 0,
    "d": lambda w: w[0] >= 2 * w[3],
}
grid = [tuple(Fr(a, 10) for a in g) for g in itertools.product(range(-20, 21, 5), repeat=3)]
grid = [(a, b, c, -a - b - c) for a, b, c in grid]
for rid, rule in rules.items():
    inside = [w for w in grid if rule(w)]
    zero = rule((0, 0, 0, 0))
    closed_scale = all(rule(tuple(s * a for a in w)) for w in inside for s in (-1, 2, Fr(1, 2)))
    closed_sum = all(rule(tuple(a + b for a, b in zip(u, w))) for u in inside[:60] for w in inside[:60])
    ok(f"part 1 rule {rid} subspace = {rid == 'a'}", (zero and closed_scale and closed_sum) == (rid == "a"))
ok("part 1 why b: zero basket breaks it", not rules["b"]((0, 0, 0, 0)))
u1, u2 = (1, -1, 0, 0), (0, 1, 0, -1)
ok("part 1 why c: both obey, sum has w1w4 = -1",
   rules["c"](u1) and rules["c"](u2) and sum(u1) == 0 and sum(u2) == 0 and (u1[0] + u2[0]) * (u1[3] + u2[3]) == -1)
ok("part 1 why c: the sum is (1, 0, 0, -1)", tuple(a + b for a, b in zip(u1, u2)) == (1, 0, 0, -1))
choice(N, I, 1, "a")
# part 2
U = M([[1, 1, 1, 1], [1, 0, 0, -2]])
dimU = 4 - U.rank()
ok("part 2 route 2 (numpy rank)", 4 - np.linalg.matrix_rank(np.array(U, float)) == 2)
key(N, I, 2, dimU)
wrongs(N, I, 2, {"one-rule": 3, "whole": 4, "one": 1})
s_, t_ = sp.symbols("s t_")
gen = V(2 * s_, t_, -3 * s_ - t_, s_)
ok("part 2 feedback: w1 = 2s, w3 = -3s - t obeys both rules", sp.simplify(U * gen) == sp.zeros(2, 1))
b1, b2 = V(2, -1, -2, 1), V(0, 1, -1, 0)
claim("problems-1 p-hedge-baskets part 2 explain says (s, t) = (1, 0) gives (2, -1, -2, 1); with the feedback line's w4 = s, w2 = t it gives "
      + str(tuple(gen.subs({s_: 1, t_: 0}))) + "; (2, -1, -2, 1) is (s, t) = (1, -1)", gen.subs({s_: 1, t_: 0}) == b1)
ok("part 2 explain: (0, 1) gives b2 and (1, -1) gives b1", gen.subs({s_: 0, t_: 1}) == b2 and gen.subs({s_: 1, t_: -1}) == b1)
ok("b1, b2 in U and independent", U * b1 == sp.zeros(2, 1) and U * b2 == sp.zeros(2, 1) and M.hstack(b1, b2).rank() == 2)
# part 3
w = V(4, 3, -9, 2)
ok("part 3: w is in U", U * w == sp.zeros(2, 1))
a_, b_ = sp.symbols("a b")
sol = sp.solve(list(a_ * b1 + b_ * b2 - w), [a_, b_], dict=True)
ok("part 3 exact: unique (2, 5)", sol == [{a_: 2, b_: 5}])
ls = np.linalg.lstsq(np.array(M.hstack(b1, b2), float), np.array(w, float).ravel(), rcond=None)[0]
ok("part 3 route 2 (lstsq)", np.allclose(ls, [2, 5]))
key(N, I, 3, V(2, 5))
wrongs(N, I, 3, {"swapped": V(5, 2), "entries": V(w[0], w[1])})
ok("part 3 explain: third entry -4 - 5 = -9, fourth a = 2", 2 * b1[2] + 5 * b2[2] == -9 and 2 * b1[3] == 2)
# part 4
Wm = M([[1, 1, 1, 1], [0, 1, -1, 0]])
ok("part 4: dim W = 2", 4 - Wm.rank() == 2)
UW = M([[1, 1, 1, 1], [1, 0, 0, -2], [0, 1, -1, 0]])
ns = UW.nullspace()
ok("part 4: U cap W is a line", len(ns) == 1)
v4 = ns[0] * 2 / ns[0][3]
ok("part 4 route 2 (solve with w4 = 2)", np.allclose(np.linalg.solve(np.array(UW.col_join(M([[0, 0, 0, 1]])), float), [0, 0, 0, 2]), [4, -3, -3, 2]))
key(N, I, 4, v4)
wrongs(N, I, 4, {"dropped-w4": V(4, -2, -2, 2),          # 4 + 2 w2 = 0
                 "halved": V(1, Fr(-3, 2), Fr(-3, 2), 2)})  # w1 = w4 / 2, then 1 + 2 w2 + 2 = 0
ok("part 4 slip values rebuilt", 4 + 2 * (-2) == 0 and 1 + 2 * Fr(-3, 2) + 2 == 0)
# part 5
basisU = U.nullspace()
basisW = Wm.nullspace()
dim_sum = M.hstack(*basisU, *basisW).rank()
ok("part 5 route 1 (rank of joined bases) = route 2 (2 + 2 - 1)", dim_sum == 2 + 2 - 1 == 3)
ok("part 5 explain: U + W inside cash-neutral, same dimension", all(sum(c) == 0 for c in basisU + basisW))
key(N, I, 5, dim_sum)
wrongs(N, I, 5, {"no-overlap": 4, "added": 5, "intersection": 1})

# p-hedge-curves
I = "p-hedge-curves"
p1, p2, p3 = 3 + x + x**2, x - 2 * x**2, 1 + x**2
co = lambda p, var=x, deg=2: V(*[sp.Poly(p, var).coeff_monomial(var**i) for i in range(deg + 1)])
sol = sp.solve(list(co(a_ * p2 + b_ * p3 - p1)), [a_, b_], dict=True)
ok("part 1 exact", sol == [{a_: 1, b_: 3}])
ok("part 1 route 2 (expand)", sp.expand(p2 + 3 * p3 - p1) == 0)
key(N, I, 1, V(1, 3))
wrongs(N, I, 1, {"swapped": V(3, 1), "signs": V(-1, -3)})
ok("part 1 signs line: p1 - p2 - 3 p3 = 0", sp.expand(p1 - p2 - 3 * p3) == 0)
ok("part 1 generic: a p2 + b p3 = b + a x + (b - 2a) x^2", sp.expand(a_ * p2 + b_ * p3 - (b_ + a_ * x + (b_ - 2 * a_) * x**2)) == 0)
C = M.hstack(co(p1), co(p2), co(p3))
key(N, I, 2, C.rank())
ok("part 2 route 2 (numpy)", np.linalg.matrix_rank(np.array(C, float)) == 2)
wrongs(N, I, 2, {"count": 3, "one": 1})
sk = sp.solve(list(co(a_ * p2 + b_ * p3 - (4 + k * x + 6 * x**2))), [a_, b_, k], dict=True)
ok("part 3 exact", sk == [{a_: -1, b_: 4, k: -1}])
ok("part 3 route 2 (det = 0)", sp.solve(M.hstack(co(p2), co(p3), co(4 + k * x + 6 * x**2)).det(), k) == [-1])
key(N, I, 3, -1)
wrongs(N, I, 3, {"sign": sp.solve(4 + 2 * k - 6, k)[0],         # x^2 term of p2 taken as +2x^2
                 "dropped-two": sp.solve(4 - k - 6, k)[0],     # taken as -x^2
                 "difference": 6 - 4})
ok("part 3 explain check", sp.expand(-p2 + 4 * p3) == 4 - x + 6 * x**2)
for oid, cand, inspan in (("a", 2 + x, True), ("b", x**2, False), ("c", x, False), ("d", 1 + x, False)):
    r = M.hstack(co(p2), co(p3), co(cand)).rank()
    ok(f"part 4 option {oid} in span = {inspan}", (r == 2) == inspan)
ok("part 4 correct line: 2 + x = p2 + 2 p3", sp.expand(p2 + 2 * p3) == 2 + x)
choice(N, I, 4, "a")
q = 5 - x + 4 * x**2
c_ = sp.symbols("c")
sq = sp.solve(list(co(a_ * p2 + b_ * p3 + c_ * x**2 - q)), [a_, b_, c_], dict=True)[0]
ok("part 5 route 2 (numpy solve)", np.allclose(np.linalg.solve(np.array(M.hstack(co(p2), co(p3), co(x**2)), float), np.array(co(q), float).ravel()), [-1, 5, -3]))
key(N, I, 5, V(sq[a_], sq[b_], sq[c_]))
wrongs(N, I, 5, {"standard": co(q), "swapped": V(5, -1, -3), "dropped-p2": V(-1, 5, 4 - 5)})

# p-scenario-space
I = "p-scenario-space"
c0 = V(3, 40)
add = lambda u, v: c0 + (u - c0) + (v - c0)
mul = lambda l, v: c0 + l * (v - c0)
u, v = V(4, 30), V(5, 60)
# the eight axioms, symbolically
sy = sp.symbols("a1 a2 b1 b2 d1 d2 l m")
A_, B_, D_ = V(sy[0], sy[1]), V(sy[2], sy[3]), V(sy[4], sy[5])
L_, M_ = sy[6], sy[7]
z0 = sp.zeros(2, 1)
ax = [add(A_, B_) - add(B_, A_), add(add(A_, B_), D_) - add(A_, add(B_, D_)), add(A_, c0) - A_,
      add(A_, mul(-1, A_)) - c0, mul(1, A_) - A_, mul(L_, mul(M_, A_)) - mul(L_ * M_, A_),
      mul(L_, add(A_, B_)) - add(mul(L_, A_), mul(L_, B_)), mul(L_ + M_, A_) - add(mul(L_, A_), mul(M_, A_))]
ok("prose: the eight axioms hold", all(sp.simplify(e) == z0 for e in ax))
ok("part 1 explain: u (+) v = u + v - c", sp.simplify(add(A_, B_) - (A_ + B_ - c0)) == z0)
key(N, I, 1, add(u, v))
ok("part 1 route 2", list(u + v - c0) == [6, 50] and list(u - c0) == [1, -10] and list(v - c0) == [2, 20])
wrongs(N, I, 1, {"usual": u + v, "moves-only": (u - c0) + (v - c0)})
zz = sp.solve(list(add(A_, V(a_, b_)) - A_), [a_, b_])
key(N, I, 2, V(zz[a_], zz[b_]))
wrongs(N, I, 2, {"usual-zero": V(0, 0)})
ok("part 2 line: u (+) (0,0) = u - c", add(u, V(0, 0)) == u - c0)
inv = sp.solve(list(add(u, V(a_, b_)) - c0), [a_, b_])
key(N, I, 3, V(inv[a_], inv[b_]))
ok("part 3 route 2: 2c - u = (-1) (.) u", 2 * c0 - u == mul(-1, u) == V(2, 50))
wrongs(N, I, 3, {"usual-negative": -u, "move-only": -(u - c0)})
claim("problems-1 p-scenario-space part 3 byKey usual-negative says u (+) (-4, -30) = (-3, -50); it is "
      + str(tuple(add(u, -u))), tuple(add(u, -u)) == (-3, -50))
ok("part 4 a: s = 40 closed", sp.simplify(add(V(sy[0], 40), V(sy[2], 40))[1]) == 40 and sp.simplify(mul(L_, V(sy[0], 40))[1]) == 40)
ok("part 4 b: zero vector not on s = 0", c0[1] != 0)
ok("part 4 c: (-1)(.)(4,30) = (2,50), r < 3", mul(-1, V(4, 30)) == V(2, 50))
ok("part 4 d: (4,40) (+) (3,50) = (4,50)", add(V(4, 40), V(3, 50)) == V(4, 50) and V(4, 40)[1] == 40 and V(3, 50)[0] == 3)
choice(N, I, 4, "a")
ab = sp.solve(list(add(mul(a_, u), mul(b_, v)) - V(8, 70)), [a_, b_])
key(N, I, 5, V(ab[a_], ab[b_]))
ok("part 5 route 2 (numpy on moves)", np.allclose(np.linalg.solve(np.array([[1, 2], [-10, 20]], float), [5, 30]), [1, 2]))
us = sp.solve(list(a_ * u + b_ * v - V(8, 70)), [a_, b_])
wrongs(N, I, 5, {"usual": V(us[a_], us[b_]), "swapped": V(2, 1)})
ok("part 5 explain: 2 (.) v = (7, 80), u (+) (7,80) = (8,70)", mul(2, v) == V(7, 80) and add(u, V(7, 80)) == V(8, 70))

# ---------------------------------------------------------------- problems-2
N = 2
I = "p-curve-report"
T = lambda p: V(p.subs(t, 2), sp.diff(p, t).subs(t, 2))
key(N, I, 1, T(t**3))
wrongs(N, I, 1, {"slope-power": V(8, (3 * t).subs(t, 2)), "swapped": V(12, 8)})
ok("part 1 explain: T(t^k) = (2^k, k 2^(k-1))", all(T(t**j) == V(2**j, j * sp.Integer(2)**(j - 1)) for j in range(4)))
A = M.hstack(*[T(t**j) for j in range(4)])
key(N, I, 2, A)
a0, a1, a2, a3 = sp.symbols("a0:4")
gp = a0 + a1 * t + a2 * t**2 + a3 * t**3
ok("part 2 route 2: A times coefficients = T(p)", sp.expand(A * V(a0, a1, a2, a3) - T(gp)) == z0)
wrongs(N, I, 2, {"unevaluated": M([[1, 2, 4, 8], [0, 1, 2, 3]]), "rows-swapped": M([A.row(1), A.row(0)]),
                 "carried": M.hstack(A[:, :3], V(8, 6))})
ok("part 3: rank 2", A.rank() == 2 and np.linalg.matrix_rank(np.array(A, float)) == 2)
key(N, I, 3, 4 - A.rank())
ok("part 3 route 2 (nullspace count)", len(A.nullspace()) == 2)
wrongs(N, I, 3, {"three": 3 - 2, "all": 4})
n1, n2 = (t - 2)**2, t * (t - 2)**2
ok("part 3 explain: both in null T and independent", T(n1) == z0 and T(n2) == z0 and M.hstack(co(n1, t, 3), co(n2, t, 3)).rank() == 2)
sl = sp.solve(list(T(a_ + b_ * t) - V(5, 3)), [a_, b_], dict=True)
ok("part 4 unique", len(sl) == 1)
p0 = sl[0][a_] + sl[0][b_] * t
key(N, I, 4, p0)
ok("part 4 route 2 (numpy)", np.allclose(np.linalg.solve(np.array(A[:, :2], float), [5, 3]), [-1, 3]))
wrongs(N, I, 4, {"level-at-zero": 3 * t + 5, "swapped": 5 * t + 3})
ok("part 4 line: 3t + 5 is 11 at t = 2", (3 * t + 5).subs(t, 2) == 11)
lv = sp.solve((p0 + lam * n1).subs(t, 0) - 7, lam)[0]
p5 = sp.expand(p0 + lv * n1)
ok("part 5 lambda = 2 and T(p) = (5, 3), p(0) = 7", lv == 2 and T(p5) == V(5, 3) and p5.subs(t, 0) == 7)
key(N, I, 5, p5)
wrongs(N, I, 5, {"no-p0": p0 + Fr(7, 4) * n1, "shift-constant": 3 * t + 7})
ok("part 5 lines: no-p0 has p(0) = 6; 3t + 7 has p(2) = 13", (p0 + sp.Rational(7, 4) * n1).subs(t, 0) == 6 and (3 * t + 7).subs(t, 2) == 13)
ok("part 5 explain: p'(t) = 4t - 5", sp.diff(p5, t) == 4 * t - 5)
# the explain's "one more condition picks one curve": among ALL solutions, p(0) = 7 leaves a line
full = sp.solve(list(T(gp) - V(5, 3)) + [gp.subs(t, 0) - 7], [a0, a1, a2, a3], dict=True)[0]
claim("problems-2 p-curve-report part 5 explain: 'the solutions are p0 plus the null space, a plane, so one more "
      "condition picks one curve'. On the plane, p(0) = 7 leaves a line (free parameters: "
      + str(4 - len(full)) + "); it is one curve only among curves of degree at most 2", 4 - len(full) == 0)

I = "p-futures-exposure"
A = M([[1, 2], [-1, 4]])
bb1, bb2 = V(1, 1), V(2, 3)
P = M.hstack(bb1, bb2)
ok("prose/part 1: T b1 = (3,3) = 3 b1; B is a basis", A * bb1 == V(3, 3) == 3 * bb1 and P.det() != 0)
cB = lambda vv: P.LUsolve(vv)
key(N, I, 1, cB(A * bb2))
ok("part 1: T b2 = (8, 10)", A * bb2 == V(8, 10))
wrongs(N, I, 1, {"standard": A * bb2, "swapped": V(2, 4)})
TB = M.hstack(cB(A * bb1), cB(A * bb2))
ok("part 2 route 2: P^-1 A P", P.inv() * A * P == TB)
key(N, I, 2, TB)
wrongs(N, I, 2, {"old-matrix": A, "rows": TB.T})
ok("part 2 explain: eigenvalues 3 and 2", A.eigenvals() == {3: 1, 2: 1} and sorted(np.linalg.eigvals(np.array(A, float)).round(9)) == [2, 3])
ok("part 3: det 6", TB.det() == 6 and A.det() == 6)
key(N, I, 3, TB.inv())
ok("part 3 route 2: P^-1 A^-1 P and numpy", P.inv() * A.inv() * P == TB.inv() and np.allclose(np.linalg.inv(np.array(TB, float)), np.array(TB.inv(), float)))
ent = M([[sp.Rational(1, 3), sp.Rational(1, 4)], [0, sp.Rational(1, 2)]])
sgn = M([[sp.Rational(1, 3), sp.Rational(2, 3)], [0, sp.Rational(1, 2)]])
wrongs(N, I, 3, {"entrywise": ent, "sign": sgn})
e = V(11, 13)
ok("part 4: [e]_B = (7, 2)", cB(e) == V(7, 2))
pos = P * (TB.inv() * cB(e))
ok("part 4 route 2: A^-1 e, numpy", A.inv() * e == pos and np.allclose(np.linalg.solve(np.array(A, float), [11, 13]), [3, 4]))
key(N, I, 4, pos)
wrongs(N, I, 4, {"b-coords": TB.inv() * cB(e), "applied-a": A * e, "carried-sign": P * (sgn * cB(e))})
print("note: part 4, carrying the other part 3 slip (entrywise) gives", tuple(P * (ent * cB(e))), "- no stored line")

I = "p-slope-adjusted"
Tm = lambda p: sp.expand(p - sp.diff(p, x))
key(N, I, 1, Tm(3 * x**2 + x))
wrongs(N, I, 1, {"power": sp.expand(3 * x**2 + x - (3 * x + 1)), "order": -Tm(3 * x**2 + x)})
ok("part 1 explain: T(1), T(x), T(x^2)", Tm(sp.Integer(1)) == 1 and Tm(x) == x - 1 and Tm(x**2) == x**2 - 2 * x)
MT = M.hstack(co(Tm(sp.Integer(1))), co(Tm(x)), co(Tm(x**2)))
ok("part 2: null T = {0}", MT.nullspace() == [] and MT.det() == 1)
choice(N, I, 2, "a")
ok("part 2 why b: p -> p(0) sends 1 to 1 and x to 0; why c: (a,b) -> (a+b, a+b) kills (1,-1)",
   sp.Integer(1).subs(x, 0) == 1 and x.subs(x, 0) == 0 and M([[1, 1], [1, 1]]) * V(1, -1) == z0)
key(N, I, 3, MT.rank())
ok("part 3 route 2", 3 - len(MT.nullspace()) == 3 and np.linalg.matrix_rank(np.array(MT, float)) == 3)
wrongs(N, I, 3, {"dim-two": 2 - 0, "null": 0})
sv = MT.LUsolve(co(x**2 + 3))
p4 = sv[0] + sv[1] * x + sv[2] * x**2
qq = x**2 + 3
ok("part 4 route 2: q + q' + q''", sp.expand(qq + sp.diff(qq, x) + sp.diff(qq, x, 2)) == p4 and Tm(p4) == qq)
key(N, I, 4, p4)
wrongs(N, I, 4, {"applied-t": Tm(qq), "one-step": qq + sp.diff(x**2, x)})
ok("part 4 line: one-step has T p = x^2 + 1", Tm(qq + 2 * x) == x**2 + 1)

# ---------------------------------------------------------------- problems-3
N = 3
I = "p-currency-duals"
v1, v2 = V(5, 1), V(4, 1)
Pv = M.hstack(v1, v2)
D = Pv.inv()
phi1 = D[0, 0] * x + D[0, 1] * y
phi2 = D[1, 0] * x + D[1, 1] * y
ev = lambda f, vv: f.subs({x: vv[0], y: vv[1]})
ok("dual basis route 2 (solve the four conditions)", [ev(phi1, v1), ev(phi1, v2), ev(phi2, v1), ev(phi2, v2)] == [1, 0, 0, 1])
ok("part 2 explain: inverse", D == M([[1, -4], [-1, 5]]) and np.allclose(np.linalg.inv(np.array(Pv, float)), [[1, -4], [-1, 5]]))
key(N, I, 1, phi1)
wrongs(N, I, 1, {"vector": 5 * x + y, "sign": -phi1})
ok("part 1 lines: 21 and -1", ev(5 * x + y, v2) == 21 and ev(-phi1, v1) == -1)
key(N, I, 2, phi2)
wrongs(N, I, 2, {"vector": 4 * x + y, "sign": -phi2})
ok("part 2 lines: 21, -1, phi1 + phi2 = y", ev(4 * x + y, v1) == 21 and ev(-phi2, v2) == -1 and sp.expand(phi1 + phi2) == y)
psi = 3 * x + 5 * y
Tm2 = M([[2, -1], [1, 3]])
Tx = Tm2 * V(x, y)
tp = sp.expand(psi.subs({x: Tx[0], y: Tx[1]}, simultaneous=True))
ok("part 3 route 2: transpose times (3, 5)", list(Tm2.T * V(3, 5)) == [tp.coeff(x), tp.coeff(y)] == [11, 12])
key(N, I, 3, tp)
nt = Tm2 * V(3, 5)
wrongs(N, I, 3, {"not-transpose": nt[0] * x + nt[1] * y, "dropped-three": sp.expand(3 * (2 * x - y) + 5 * (x + y))})
cc = V(ev(tp, v1), ev(tp, v2))
ok("part 4 route 2: expand c1 phi1 + c2 phi2", sp.expand(cc[0] * phi1 + cc[1] * phi2) == tp and Pv.T * V(11, 12) == cc)
key(N, I, 4, cc)
slip = nt[0] * x + nt[1] * y
wrongs(N, I, 4, {"standard": V(11, 12), "swapped": V(cc[1], cc[0]), "carried": V(ev(slip, v1), ev(slip, v2))})
s2 = 11 * x + 2 * y
print("note: part 4, carrying the other part 3 slip (11x + 2y) gives", (ev(s2, v1), ev(s2, v2)), "- no stored line")
G = sp.diag(2, 1)
uu = G.inv() * V(11, 12)
w1, w2 = sp.symbols("w1 w2")
ok("part 5 route 2: <w, u> = T'psi(w) for symbolic w", sp.expand((V(w1, w2).T * G * uu)[0] - ev(tp, V(w1, w2))) == 0)
key(N, I, 5, uu)
wrongs(N, I, 5, {"dot": V(11, 12), "doubled": V(22, 12)})

I = "p-index-beta"
a = V(1, -1, 0, 1, -1)
b = V(3, 0, -2, 2, -3)
ip = lambda p_, q_: sp.Rational(1, 4) * p_.dot(q_)
an, bn = np.array(a, float).ravel(), np.array(b, float).ravel()
ok("prose: mean zero", sum(a) == 0 and sum(b) == 0)
cov = ip(a, b)
ok("part 1 route 2 (np.cov, ddof 1)", np.isclose(np.cov(an, bn)[0, 1], 2) and a.dot(b) == 8)
key(N, I, 1, cov)
wrongs(N, I, 1, {"no-divide": a.dot(b), "divide-five": sp.Rational(8, 5)}, places=2)
corr = cov / sp.sqrt(ip(a, a) * ip(b, b))
ok("part 2 norms 1 and 6.5; route 2 np.corrcoef", ip(a, a) == 1 and ip(b, b) == sp.Rational(13, 2) and np.isclose(np.corrcoef(an, bn)[0, 1], float(corr)))
key(N, I, 2, corr, places=3)
wrongs(N, I, 2, {"squared": cov**2 / (ip(a, a) * ip(b, b)), "one-norm": cov / ip(b, b)}, places=3)
beta = ip(b, a) / ip(a, a)
r = b - beta * a
ok("part 3 beta = 2, r orthogonal to a; route 2 polyfit through origin", beta == 2 and ip(r, a) == 0 and np.isclose(np.linalg.lstsq(an[:, None], bn, rcond=None)[0][0], 2))
key(N, I, 3, r)
wrongs(N, I, 3, {"beta-one": b - a, "no-divide": b - a.dot(b) * a, "reversed": beta * a - b})
ok("part 3 explain sum 1 - 2 + 0 + 0 + 1", [r[i] * a[i] for i in range(5)] == [1, -2, 0, 0, 1])
share = 1 - ip(r, r) / ip(b, b)
ok("part 4: |r|^2 = 2.5, share = 4/6.5 = corr^2, Pythagoras", ip(r, r) == sp.Rational(5, 2) and share == sp.Rational(8, 13) == sp.nsimplify(corr**2) and ip(b, b) == 4 * ip(a, a) + ip(r, r))
key(N, I, 4, share, places=3)
wrongs(N, I, 4, {"residual-share": ip(r, r) / ip(b, b), "correlation": corr}, places=3)
ok("part 4 explain: 0.784^2 rounds to 0.615", round(0.784**2, 3) == 0.615)
ok("part 4: the plain dot product gives the same share", 1 - sp.Rational(r.dot(r), b.dot(b)) == share)

I = "p-two-signal-fit"
vv = V(4, 2, 5, 3)
g1, g2 = V(1, 1, 0, 1), V(2, 1, 1, 3)
be = sp.Rational(g2.dot(g1), g1.dot(g1))
f2 = g2 - be * g1
ok("part 1: beta = 6/3 = 2, f2 orthogonal to u1", g2.dot(g1) == 6 and g1.dot(g1) == 3 and be == 2 and f2.dot(g1) == 0)
Q, R = np.linalg.qr(np.array(M.hstack(g1, g2), float))
ok("part 1 route 2 (QR second column parallel to f2)", abs(abs(Q[:, 1] @ np.array(f2, float).ravel()) - float(sp.sqrt(f2.dot(f2)))) < 1e-9)
key(N, I, 1, f2)
wrongs(N, I, 1, {"no-divide": g2 - g2.dot(g1) * g1, "beta-one": g2 - g1})
k1 = sp.Rational(vv.dot(g1), g1.dot(g1))
k2 = sp.Rational(vv.dot(f2), f2.dot(f2))
proj = k1 * g1 + k2 * f2
Am = M.hstack(g1, g2)
ok("part 2: weights 9/3 = 3 and 6/3 = 2; route 2 normal equations and lstsq",
   (vv.dot(g1), vv.dot(f2), f2.dot(f2), k1, k2) == (9, 6, 3, 3, 2) and Am * (Am.T * Am).inv() * Am.T * vv == proj
   and np.allclose(np.array(Am, float) @ np.linalg.lstsq(np.array(Am, float), np.array(vv, float).ravel(), rcond=None)[0], [3, 1, 2, 5]))
key(N, I, 2, proj)
wrongs(N, I, 2, {"not-orthogonal": k1 * g1 + sp.Rational(vv.dot(g2), g2.dot(g2)) * g2, "no-norm": k1 * g1 + vv.dot(f2) * f2})
cs = (Am.T * Am).inv() * Am.T * vv
ok("part 3 route 2: 3 u1 + 2 (u2 - 2 u1)", list(cs) == [k1 - 2 * k2, k2] == [-1, 2])
key(N, I, 3, cs)
wrongs(N, I, 3, {"gs-coords": V(k1, k2), "swapped": V(cs[1], cs[0])})
res = vv - proj
dist = sp.sqrt(res.dot(res))
ok("part 4: residual (1,1,3,-2), in U perp, norm sqrt 15", list(res) == [1, 1, 3, -2] and res.dot(g1) == 0 and res.dot(g2) == 0 and res.dot(f2) == 0 and dist**2 == 15)
best = min(float(sp.sqrt((vv - i * g1 / 4 - j * g2 / 4).dot(vv - i * g1 / 4 - j * g2 / 4))) for i in range(-20, 21) for j in range(-20, 21))
ok("part 4 route 2 (grid search over U)", abs(best - float(dist)) < 1e-9)
key(N, I, 4, dist, places=3)
r1 = vv - k1 * g1
wrongs(N, I, 4, {"squared": 15, "one-signal": sp.sqrt(r1.dot(r1))}, places=3)
ok("part 4 line: sqrt 27", r1.dot(r1) == 27)

# ---------------------------------------------------------------- shape of the sets (docs/briefs/chained.md)
LEVEL = {1: ["l1", "l2", "l3", "l4"], 2: ["l5", "l6", "l7", "l8", "l9"], 3: ["l10", "l11", "l12", "l13", "l14"]}
for n, d in SETS.items():
    its = d["items"]
    ok(f"problems-{n}: 3 to 5 items", 3 <= len(its) <= 5)
    ok(f"problems-{n}: a difficulty 5, all 3 to 5", any(i["difficulty"] == 5 for i in its) and all(3 <= i["difficulty"] <= 5 for i in its))
    parts = [p for i in its for p in i["parts"]]
    typed = sum(p["widget"]["kind"] != "choice" for p in parts)
    ok(f"problems-{n}: typed parts {typed}/{len(parts)} at least two thirds", 3 * typed >= 2 * len(parts))
    for i in its:
        ok(f"problems-{n} {i['id']}: 3 to 5 parts", 3 <= len(i["parts"]) <= 5)
        for j, p in enumerate(i["parts"], 1):
            sents = [s for s in re.split(r"(?<=[.?])\s+(?=[A-Z$])", p["explain"]["text"]) if s]
            ok(f"problems-{n} {i['id']} part {j}: explain at most 3 sentences ({len(sents)})", len(sents) <= 3)
            if j > 1:
                q_ = p["question"]
                if not re.search(r"[Uu]sing|from part|in part", q_):
                    print(f"note: problems-{n} {i['id']} part {j} names no earlier part")
            blob = json.dumps(p, ensure_ascii=False)
            ok(f"problems-{n} {i['id']} part {j}: no exclamation mark or em-dash", "!" not in blob.replace("\\!", "") and "\u2014" not in blob)

print(f"\nmine.py: {checks} checks, {fails} failures, {claims} CLAIM lines")
sys.exit(1 if fails else 0)
