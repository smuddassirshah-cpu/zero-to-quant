"""least-squares level 3 performance task: every number and identity checked twice.

Item: app/content/courses/least-squares/homework-3.json#h-derive-hedge (performance: derivation).
Run: <venv>/bin/python -I docs/reports/least-squares-3-perf-numbers.py   (numpy and sympy; exits 0 when all checks pass)

Route 1: sympy exact arithmetic (normal equations, Cramer's rule, nullspaces, symbolic identities).
Route 2: numpy (lstsq, a brute-force grid over hedges, random checks of the identities).
Also: every passing tick set of the rubric, and the sums printed in the model.
"""
import itertools, json, os, re, sys
import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app", "content", "courses", "least-squares", "homework-3.json")
doc = json.load(open(HW, encoding="utf-8"))
item = [i for i in doc["items"] if i["id"] == "h-derive-hedge"][0]
fails = checks = 0


def check(cond, msg):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", msg)


# ---------- structure ----------
check(item["performance"] == "derivation" and item["kind"] == "longform", "kind")
for k in ("starter", "steps", "order", "derive", "hints", "parts"):
    check(k not in item, f"no {k}")
check(sum(r["points"] for r in item["rubric"]) == 10 and 3 <= len(item["rubric"]) <= 5, "rubric 3 to 5 rows, 10 points")
check(6 <= len(doc["items"]) <= 12 and sum(1 for i in doc["items"] if i.get("performance")) == 1, "homework size, one task")
check("Optional, one more point:" in item["prompt"], "optional part marked")

# ---------- data, read back from the prompt ----------
P = item["prompt"]
def vec(name):
    m = re.search(re.escape(name) + r" = \(([^)]*)\)", P)
    return [int(v) for v in m.group(1).split(",")]
b = vec("\\mathbf{b}"); a1 = vec("\\mathbf{a}_1"); a2 = vec("\\mathbf{a}_2")
check(b == [-13, 15, -7, 7] and a1 == [-1, 1, 1, -1] and a2 == [-4, 4, -3, 3], "data parsed")

# scenario signs: futures lose when their yields rise
check(a1[0] < 0 < a1[1] and a2[0] < 0 < a2[1], "parallel up loses, down gains")
check(a1[2] > 0 and a2[2] < 0 and a1[3] < 0 and a2[3] > 0, "steepener: 2y yield down (2y future gains), 10y up (10y future loses); flattener reverse")
check(abs(a2[0]) > abs(a1[0]), "10-year future more rate-sensitive than 2-year")

A = sp.Matrix([a1, a2]).T; B = sp.Matrix(b)
G = A.T * A; r = A.T * B
check(G == sp.Matrix([[4, 2], [2, 50]]) and r == sp.Matrix([14, 154]), "A^T A and A^T b (exact)")
An = np.array(A.tolist(), float); bn = np.array(b, float)
check(np.allclose(An.T @ An, [[4, 2], [2, 50]]) and np.allclose(An.T @ bn, [14, 154]), "A^T A and A^T b (numpy)")
check(A.rank() == 2 and np.linalg.matrix_rank(An) == 2, "columns independent")
check(G.det() == 196 and 4 * 50 - 2 * 2 == 196, "det 196")

xh = G.solve(r)
cr = [sp.Matrix([[14, 2], [154, 50]]).det() / 196, sp.Matrix([[4, 14], [2, 154]]).det() / 196]
check(list(xh) == [2, 3] and cr == [2, 3], "x-hat = (2, 3) by solve and by Cramer")
xl = np.linalg.lstsq(An, bn, rcond=None)[0]
check(np.allclose(xl, [2, 3]), "lstsq gives (2, 3)")
# the model's substitution: x1 = 3.5 - 0.5 x2; 7 - x2 + 50 x2 = 154; 49 x2 = 147
x2 = sp.symbols("x2")
check(sp.expand(2 * (sp.Rational(7, 2) - x2 / 2) + 50 * x2) == 7 + 49 * x2 and sp.solve(49 * x2 - 147, x2) == [3], "substitution lines")
check(sp.Rational(14, 4) == sp.Rational(7, 2) and sp.Rational(2, 4) == sp.Rational(1, 2), "first equation over 4")

p = A * xh; e = B - p
check(list(p) == [-14, 14, -7, 7] and list(2 * sp.Matrix(a1) + 3 * sp.Matrix(a2)) == [-14, 14, -7, 7], "p two ways")
check(list(e) == [1, 1, 0, 0] and A.T * e == sp.zeros(2, 1), "e = (1, 1, 0, 0) and A^T e = 0")
check(np.allclose(bn - An @ xl, [1, 1, 0, 0]), "numpy residual")
check(B.dot(B) == 492 and 169 + 225 + 49 + 49 == 492 and e.dot(e) == 2, "|b|^2 = 492, |e|^2 = 2")
check(B.dot(B) == p.dot(p) + e.dot(e), "Pythagoras on the hedge: 492 = 490 + 2")
# brute-force grid over hedges, route 2 for the minimum
grid = np.arange(-1, 6.0001, 0.05)
best = min((float(np.sum((bn - An @ np.array([u, v])) ** 2)), u, v) for u in grid for v in grid)
check(abs(best[1] - 2) < 1e-9 and abs(best[2] - 3) < 1e-9 and abs(best[0] - 2) < 1e-9, f"grid minimum {best}")
# the printed sums
for txt, val in [("4 + 4 - 3 - 3 = 2", 2), ("16 + 16 + 9 + 9 = 50", 50), ("13 + 15 - 7 - 7 = 14", 14),
                 ("52 + 60 + 21 + 21 = 154", 154), ("169 + 225 + 49 + 49 = 492", 492), ("-1 + 1 = 0", 0), ("-4 + 4 = 0", 0)]:
    check(txt in item["model"] and eval(txt.split("=")[0]) == val, f"printed sum {txt}")
check(sp.Matrix(a1).dot(sp.Matrix(a2)) == 2 and sp.Matrix(a1).dot(B) == 14 and sp.Matrix(a2).dot(B) == 154, "dot products exact")
# "each future makes opposite amounts in the two parallel moves, and so does any combination"
u, v = sp.symbols("u v")
comb = u * sp.Matrix(a1) + v * sp.Matrix(a2)
check(sp.simplify(comb[0] + comb[1]) == 0, "every combination is opposite in the parallel moves")
check(sp.Matrix([1, 1, 0, 0]).dot(sp.Matrix(a1)) == 0 and sp.Matrix([1, 1, 0, 0]).dot(sp.Matrix(a2)) == 0, "gain in both moves is perpendicular to both")
check(len((A.T).nullspace()) == 2, "left nullspace has dimension 4 - 2 = 2")

# ---------- general identities used in (a), (b), (c) ----------
t, c, n2 = sp.symbols("t c n2", positive=True)
# |e - t a|^2 = |e|^2 - 2 t c + t^2 |a|^2 with c = a.e, n2 = |a|^2; at t = c/n2 it is |e|^2 - c^2/n2
E2 = sp.symbols("E2")
f = E2 - 2 * t * c + t ** 2 * n2
check(sp.simplify(f.subs(t, c / n2) - (E2 - c ** 2 / n2)) == 0, "only-if step value")
check(sp.solve(sp.diff(f, t), t) == [c / n2], "t = c/|a|^2 is the best step")
rng = np.random.default_rng(7)
for _ in range(200):
    m, n = rng.integers(2, 7), rng.integers(1, 4)
    if n > m:
        continue
    M = rng.normal(size=(m, n)); y = rng.normal(size=m); z = rng.normal(size=n)
    # z^T A^T A z = |Az|^2
    check(np.isclose(z @ M.T @ M @ z, np.sum((M @ z) ** 2)), "z^T A^T A z = |Az|^2")
    # entry j of A^T e is a_j . e
    ee = rng.normal(size=m)
    check(np.allclose(M.T @ ee, [M[:, j] @ ee for j in range(n)]), "entry j of A^T e")
    # closest point: residual of the normal-equation solution beats random points, and the only-if step beats a non-orthogonal p
    xs = np.linalg.solve(M.T @ M, M.T @ y); es = y - M @ xs
    q = M @ rng.normal(size=n)
    check(np.sum((y - q) ** 2) >= np.sum(es ** 2) - 1e-12 and np.isclose(np.sum((y - q) ** 2), np.sum(es ** 2) + np.sum((M @ xs - q) ** 2)), "Pythagoras")
    pb = M @ (xs + rng.normal(size=n)); eb = y - pb; j = 0
    cc = M[:, j] @ eb
    if abs(cc) > 1e-9:
        qq = pb + cc / (M[:, j] @ M[:, j]) * M[:, j]
        check(np.sum((y - qq) ** 2) < np.sum(eb ** 2), "only-if step gives a closer point")
# symbolic: A^T A z = 0 has only z = 0 for this A
z1, z2 = sp.symbols("z1 z2")
check(sp.solve(list(G * sp.Matrix([z1, z2])), [z1, z2]) == {z1: 0, z2: 0}, "A^T A z = 0 only at 0 (this A)")

# ---------- optional part: the bundle future ----------
a3 = [x + y for x, y in zip(a1, a2)]
check(a3 == [-5, 5, -2, 2] and "(-5, 5, -2, 2)" in item["model"], "a3 = a1 + a2 = (-5, 5, -2, 2)")
A3 = sp.Matrix([a1, a2, a3]).T
G3 = A3.T * A3
check(A3.rank() == 2 and G3.det() == 0 and np.linalg.matrix_rank(np.array(A3.tolist(), float)) == 2, "three columns dependent, Gram singular")
check(G3 * sp.Matrix([1, 1, -1]) == sp.zeros(3, 1) and len(G3.nullspace()) == 1 and G3.nullspace()[0].cross(sp.Matrix([1, 1, -1])) == sp.zeros(3, 1), "nullspace (1, 1, -1)")
tt = sp.symbols("tt")
fam = sp.Matrix([2 - tt, 3 - tt, tt])
check(sp.simplify(G3 * fam - A3.T * B) == sp.zeros(3, 1), "(2 - t, 3 - t, t) solves the normal equations")
check(sp.simplify(B - A3 * fam) == sp.Matrix([1, 1, 0, 0]), "same hedged P&L for every t")
x3 = np.linalg.lstsq(np.array(A3.tolist(), float), bn, rcond=None)[0]
check(np.allclose(bn - np.array(A3.tolist(), float) @ x3, [1, 1, 0, 0]) and np.isclose(x3[0] - x3[1], -1), "numpy: minimum-norm hedge is in the family")
# C(A3) = C(A): a3 is in the span, and a1, a2 still span it
check(sp.Matrix([a1, a2, a3]).T.rank() == sp.Matrix([a1, a2]).T.rank(), "same column space")

# ---------- rubric: every passing tick set ----------
R = item["rubric"]
req = [i for i, row in enumerate(R) if row.get("required")]
passing = [s for k in range(len(R) + 1) for s in itertools.combinations(range(len(R)), k)
           if sum(R[i]["points"] for i in s) >= 7 and all(i in s for i in req)]
print("passing tick sets (rows from 1):", [[i + 1 for i in s] for s in passing])
check([[i + 1 for i in s] for s in passing] == [[1, 2, 3, 4], [1, 2, 3, 4, 5]], "passing sets")
check(req == [0, 1, 2, 3] and not R[4].get("required"), "rows 1 to 4 required, the optional part not")
for s in passing:
    check(all(i in s for i in (0, 1, 2, 3)), "no pass skips a named part (a) to (d)")
for txt in ["(4, 2)", "(2, 50)", "(14, 154)", "2 two-year and 3 ten-year", "(1, 1, 0, 0)"]:
    check(txt in R[3]["text"], f"row 4 states {txt}")
check("(1, 1, -1)" in R[4]["text"] and "(2 - t, 3 - t, t)" in R[4]["text"], "row 5 numbers")
check("(1, 1, 0, 0)" in item["model"] and "$\\hat x_2 = 3$ and $\\hat x_1 = 2$" in item["model"], "model states the hedge")

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
