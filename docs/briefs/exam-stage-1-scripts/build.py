"""Build app/content/exams/stage-1.json, the Stage 1 exit test (topics 1.1 to 1.11).

Route A for every key: the closed forms and reference implementations below. check_numbers.py recomputes each value
by a second route and asserts it at its path in the written file. Run: python3 docs/briefs/exam-stage-1-scripts/build.py
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'stage-1.json')


def r(x, n=6):
    return round(float(x), n)


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), unit=None, placeholder="a number", accept=None):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": placeholder}
    if unit:
        w["unit"] = unit
    if accept:
        w["accept"] = accept
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong]
    return w


def expr(answer, accept, wrong=(), keyboard="calculus"):
    w = {"kind": "expression", "answer": answer, "accept": list(accept), "keyboard": keyboard}
    if wrong:
        w["wrong"] = [{"id": i, "tex": t} for i, t in wrong]
    return w


def choice(options):
    return {"kind": "choice", "layout": "stack", "shuffle": True, "options": options}


def opt(id, text, why=None, correct=False):
    o = {"id": id, "text": text}
    if correct:
        o["correct"] = True
    if why:
        o["why"] = why
    return o


def order(lines, answer, distractors=(), same=None):
    w = {"kind": "order", "lines": lines, "answer": answer}
    if distractors:
        w["distractors"] = list(distractors)
    if same:
        w["same"] = same
    return w


def line(id, text, why=None):
    d = {"id": id, "text": text}
    if why:
        d["why"] = why
    return d


def item(id, d, skills, tags, pace, title, prose, question, widget, feedback, explain):
    it = {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title}
    if prose:
        it["prose"] = prose
    it.update({"question": question, "widget": widget, "feedback": feedback, "explain": {"text": explain}})
    return it


def parts(id, d, skills, tags, pace, title, prose, ps, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "parts": [{"question": q, "widget": w, "feedback": f} for q, w, f in ps],
            "explain": {"text": explain}}


def code_fb(correct, by_key):
    by_key = dict(by_key)
    by_key.setdefault("error", "Your code stopped with an error. Read the first line of the message under the editor.")
    return fb(correct, "Some tests failed. Open the first one that failed below the editor.", by_key)


def py_tests(rows):
    """rows: (setup or None, call, expected value, compare). Expected values are written with repr."""
    out = []
    for setup, call, val, cmp in rows:
        t = {}
        if setup:
            t["setup"] = setup
        t.update({"call": call, "expect": val if isinstance(val, str) else repr(val), "compare": cmp})
        out.append(t)
    return out


def pyval(x):
    if isinstance(x, np.ndarray):
        return repr([float(v) for v in x])
    if isinstance(x, (list, tuple)):
        return repr([float(v) for v in x])
    return repr(float(x))


A, B, C, D = [], [], [], []

# ======================================================================== Paper A: calculus and linear algebra
# A1 chain rule
a1 = 4 * (1 ** 3 + 2 * 1) ** 3 * (3 * 1 ** 2 + 2)
A.append(item("a-chain-power", 2, ["lm-chain"], ["chain-rule"], 90, "A power of a cubic",
    "Let $f(x) = (x^3 + 2x)^4$.", "What is $f'(1)$?",
    num(a1, 0, [("no-inner", 4 * 3 ** 3, 0)]),
    fb("The outer power times the inner derivative.", "Differentiate the outer power, then multiply by the derivative of $x^3 + 2x$.",
       {"no-inner": "You left out the inner derivative $3x^2 + 2$. The chain rule multiplies by it."}),
    f"The chain rule gives $f'(x) = 4(x^3 + 2x)^3 (3x^2 + 2)$. At $x = 1$ that is $4 \\cdot 27 \\cdot 5 = {a1}$."))

# A2 fundamental theorem
a2 = 8 + math.log(3)
A.append(item("a-ftc-log", 2, ["in-ftc"], ["definite-integral"], 90, "A line and a reciprocal",
    None, "What is $\\int_1^3 \\left(2x + \\tfrac{1}{x}\\right) dx$? Give 4 decimal places.",
    num(r(a2), 0.0005, [("dropped-log", 8, 0.0005), ("upper-only", r(9 + math.log(3)), 0.0005)]),
    fb("An antiderivative, evaluated at both ends.", "Find an antiderivative of each term, then subtract its value at 1 from its value at 3.",
       {"dropped-log": "You integrated $2x$ but left out $\\tfrac{1}{x}$. Its antiderivative is $\\ln x$.",
        "upper-only": "You evaluated at 3 only. Subtract the value at 1, which is $1 + \\ln 1 = 1$."}),
    f"An antiderivative is $x^2 + \\ln x$. So the integral is $(9 + \\ln 3) - (1 + 0) = 8 + \\ln 3 \\approx {a2:.4f}$."))

# A3 optimisation
q3 = 80 / 4
p3 = 80 * q3 - 2 * q3 ** 2 - 50
q3r = 90 / 4
p3r = 80 * q3r - 2 * q3r ** 2 - 50
A.append(item("a-desk-profit", 3, ["lm-optimise"], ["profit-max"], 150, "A desk's best volume",
    "A desk sells $q$ units at $90 - 2q$ pounds each. Its cost for $q$ units is $10q + 50$ pounds.",
    "What is the largest profit the desk can make, in pounds?",
    num(p3, 0.01, [("gave-q", q3, 0.01), ("revenue-max", p3r, 0.01)], unit="£"),
    fb("Profit is revenue minus cost, maximised where its derivative is zero.", "Write profit as one quadratic in $q$, then set its derivative to zero.",
       {"gave-q": f"You found the best volume, $q = {q3:.0f}$. Put it back into the profit.",
        "revenue-max": f"You maximised revenue, at $q = {q3r}$. Maximise revenue minus cost."}),
    f"Profit is $q(90 - 2q) - 10q - 50 = 80q - 2q^2 - 50$. Its derivative $80 - 4q$ is zero at $q = {q3:.0f}$. "
    f"The profit there is $1600 - 800 - 50 = {p3:.0f}$ pounds."))

# A4 integration by parts
a4 = (2 * math.e ** 3 + 1) / 9
A.append(item("a-parts-exp", 3, ["in-techniques"], ["by-parts"], 150, "A line times a growth",
    None, "What is $\\int_0^1 x e^{3x} dx$? Give 4 decimal places.",
    num(r(a4), 0.0005, [("sign-slip", r((2 * math.e ** 3 - 1) / 9), 0.0005)]),
    fb("By parts, with $u = x$.", "Take $u = x$ and $dv = e^{3x} dx$, so $v = \\tfrac13 e^{3x}$.",
       {"sign-slip": "You added the lower limit's term instead of subtracting it. At 0 the bracket is $-\\tfrac19$."}),
    f"By parts, the integral is $\\left[\\tfrac{{x}}{{3}}e^{{3x}} - \\tfrac{{1}}{{9}}e^{{3x}}\\right]_0^1$. "
    f"That is $\\tfrac{{2e^3}}{{9}} + \\tfrac19 \\approx {a4:.4f}$."))

# A5 Taylor product
A.append(item("a-taylor-product", 3, ["ty-taylor"], ["series-product"], 150, "A product of two series",
    None, "Write the Maclaurin series of $e^x \\cos x$ up to and including the $x^3$ term.",
    expr("1+x-\\frac{x^3}{3}", ["1 + x - x^3/3"],
         [("only-exp", "1+x+\\frac{x^2}{2}+\\frac{x^3}{6}"), ("dropped-cross", "1+x+\\frac{x^3}{6}")]),
    fb("The $x^2$ terms cancel.", "Multiply $1 + x + \\tfrac{x^2}{2} + \\tfrac{x^3}{6}$ by $1 - \\tfrac{x^2}{2}$ and keep powers up to 3.",
       {"only-exp": "You kept the series of $e^x$ alone. The $-\\tfrac{x^2}{2}$ of $\\cos x$ multiplies every term.",
        "dropped-cross": "You cancelled the $x^2$ terms but dropped $x \\cdot (-\\tfrac{x^2}{2})$. It adds $-\\tfrac{x^3}{2}$ to the cube term."}),
    "The $x^2$ terms are $\\tfrac{x^2}{2} - \\tfrac{x^2}{2} = 0$. "
    "The $x^3$ terms are $\\tfrac{x^3}{6} - \\tfrac{x^3}{2} = -\\tfrac{x^3}{3}$."))

# A6 directional derivative
g6 = np.array([1 ** 2 + 2, 2 * 2 * 1])
u6 = np.array([3, 4]) / 5
a6 = float(g6 @ u6)
A.append(item("a-directional", 3, ["mv-gradient"], ["directional-derivative"], 120, "A slope in a direction",
    "Let $f(x, y) = xy^2 + 2x$.", "What is the rate of change of $f$ at $(2, 1)$ in the direction of $(3, 4)$?",
    num(r(a6), 0.001, [("unnormalised", float(g6 @ np.array([3, 4])), 0.001)]),
    fb("The gradient dotted with a unit vector.", "Find $\\nabla f$ at $(2, 1)$, then dot it with $(3, 4)$ scaled to length 1.",
       {"unnormalised": "You dotted with $(3, 4)$ itself. Divide by its length 5 first."}),
    f"$\\nabla f = (y^2 + 2, 2xy) = (3, 4)$ at $(2, 1)$. The unit direction is $(0.6, 0.8)$. So the rate is $1.8 + 3.2 = {a6:.0f}$."))

# A7 Lagrange multipliers
lam7 = 32 / 8
x7, y7 = 4 * lam7, lam7
a7 = x7 * y7
A.append(item("a-lagrange-product", 4, ["mv-lagrange"], ["lagrange"], 180, "A product on a budget line",
    "Positive $x$ and $y$ satisfy $x + 4y = 32$.", "What is the largest value of $xy$?",
    num(a7, 0.01, [("gave-x", x7, 0.01), ("gave-lambda", lam7, 0.01)]),
    fb("The gradients are parallel at the best point.", "Set $(y, x) = \\lambda(1, 4)$ and use the constraint.",
       {"gave-x": f"You found $x = {x7:.0f}$. The question asks for the product $xy$.",
        "gave-lambda": f"That is the multiplier $\\lambda$, which equals $y$ here. Multiply $x = {x7:.0f}$ by $y = {y7:.0f}$."}),
    f"$\\nabla(xy) = \\lambda \\nabla(x + 4y)$ gives $y = \\lambda$ and $x = 4\\lambda$. The constraint gives $8\\lambda = 32$, so $\\lambda = {lam7:.0f}$. "
    f"Then $x = {x7:.0f}$, $y = {y7:.0f}$ and $xy = {a7:.0f}$."))

# A8 double integral over a triangle
a8 = 1.5 * 3 ** 3 / 3
A.append(item("a-triangle-integral", 4, ["mv-integrals"], ["double-integral"], 180, "An integral over a triangle",
    "Let $R$ be the triangle $0 \\le y \\le x \\le 3$.", "What is $\\iint_R (x + y) \\, dA$?",
    num(a8, 0.001, [("square", 27, 0.001)]),
    fb("Inner limits in $y$ run from 0 to $x$.", "Integrate $x + y$ in $y$ from 0 to $x$, then in $x$ from 0 to 3.",
       {"square": "You integrated over the square $[0, 3]^2$. The triangle stops $y$ at $x$."}),
    f"The inner integral is $\\int_0^x (x + y) \\, dy = \\tfrac{{3x^2}}{{2}}$. Then $\\int_0^3 \\tfrac{{3x^2}}{{2}} dx = \\tfrac{{27}}{{2}} = {a8}$."))

# A9 a limit
A.append(item("a-cos-limit", 3, ["lm-limits"], ["small-angle"], 90, "A cosine near zero",
    None, "What is $\\lim_{x \\to 0} \\dfrac{1 - \\cos 3x}{x \\sin x}$?",
    num(4.5, 0.001, [("no-half", 9, 0.001)]),
    fb("Near 0, $1 - \\cos u \\approx \\tfrac{u^2}{2}$ and $\\sin x \\approx x$.", "Use $1 - \\cos u \\approx \\tfrac{u^2}{2}$ with $u = 3x$, and $\\sin x \\approx x$.",
       {"no-half": "You took $1 - \\cos u$ as $u^2$. It is $\\tfrac{u^2}{2}$ to leading order."}),
    "With $u = 3x$, $1 - \\cos 3x \\approx \\tfrac{9x^2}{2}$. The bottom, $x \\sin x$, is about $x^2$. So the limit is $\\tfrac92 = 4.5$."))

# A10 determinant
M10 = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
a10 = 2 * (3 * 4 - 1 * 1) - 1 * (1 * 4 - 1 * 0) + 0
A.append(item("a-det-three", 2, ["gx-det"], ["determinant"], 90, "A three by three determinant",
    "$\\mathbf{M} = \\begin{pmatrix} 2 & 1 & 0 \\\\ 1 & 3 & 1 \\\\ 0 & 1 & 4 \\end{pmatrix}$.", "What is $\\det \\mathbf{M}$?",
    num(a10, 0, [("plus-sign", 2 * 11 + 1 * 4, 0)]),
    fb("Expand along the first row with alternating signs.", "Expand along the first row: the signs go $+, -, +$.",
       {"plus-sign": "You added the second term. Its cofactor sign is minus."}),
    f"Along the first row, $\\det \\mathbf{{M}} = 2(12 - 1) - 1(4 - 0) + 0 = 22 - 4 = {a10}$."))

# A11 nullity
M11 = np.array([[1, 2, 0, 1, 3], [2, 4, 1, 3, 1], [3, 6, 1, 4, 4]])
rank11 = int(np.linalg.matrix_rank(M11))
A.append(item("a-nullity", 3, ["gx-rank"], ["rank-nullity"], 150, "Solutions of a wide system",
    "$\\mathbf{A} = \\begin{pmatrix} 1 & 2 & 0 & 1 & 3 \\\\ 2 & 4 & 1 & 3 & 1 \\\\ 3 & 6 & 1 & 4 & 4 \\end{pmatrix}$.",
    "What is the dimension of the null space of $\\mathbf{A}$?",
    num(5 - rank11, 0, [("gave-rank", rank11, 0)]),
    fb("Five columns minus the rank.", "Find the rank by elimination, then subtract it from the number of columns.",
       {"gave-rank": f"You found the rank, {rank11}. The null space has dimension 5 minus the rank."}),
    f"Row 3 is row 1 plus row 2, and rows 1 and 2 are independent. So the rank is {rank11}. "
    f"The null space has dimension $5 - {rank11} = {5 - rank11}$."))

# A12 distance to a line
b12 = np.array([4, 1, 3.0])
v12 = np.array([1, 2, 2.0])
p12 = (b12 @ v12) / (v12 @ v12) * v12
a12 = float(np.linalg.norm(b12 - p12))
A.append(item("a-line-distance", 3, ["ls-proj"], ["projection"], 120, "How far from a line",
    "Let $\\mathbf{b} = (4, 1, 3)$ and let $L$ be the line through $\\mathbf{0}$ along $(1, 2, 2)$.",
    "What is the distance from $\\mathbf{b}$ to $L$? Give 4 decimal places.",
    num(r(a12), 0.0005, [("proj-length", r(np.linalg.norm(p12)), 0.0005)]),
    fb("The error vector is perpendicular to the line.", "Project $\\mathbf{b}$ onto $(1, 2, 2)$, then take the length of what is left.",
       {"proj-length": "You gave the length of the projection. The distance is the length of $\\mathbf{b} - \\mathbf{p}$."}),
    f"The projection is $\\tfrac{{12}}{{9}}(1, 2, 2) = \\tfrac43(1, 2, 2)$. The error is $\\tfrac13(8, -5, 1)$, of length $\\sqrt{{10}} \\approx {a12:.4f}$."))

# A13 eigenvector
M13 = np.array([[6, 2], [2, 3.0]])
A.append(item("a-eigvec", 3, ["eg-eigen"], ["eigenvector"], 120, "The larger eigenvalue's direction",
    "$\\mathbf{A} = \\begin{pmatrix} 6 & 2 \\\\ 2 & 3 \\end{pmatrix}$.",
    "Which vector is an eigenvector for the larger eigenvalue of $\\mathbf{A}$?",
    choice([opt("a", "$(2, 1)$", correct=True),
            opt("b", "$(1, -2)$", "You found the eigenvector of the other eigenvalue, 2."),
            opt("c", "$(1, 2)$", "You swapped the entries. $\\mathbf{A}(1, 2) = (10, 8)$, which is not a multiple of $(1, 2)$."),
            opt("d", "$(6, 2)$", "You took the first column. $\\mathbf{A}(6, 2) = (40, 18)$, not a multiple of it.")]),
    fb("Trace 9 and determinant 14 give eigenvalues 7 and 2.", "Find the eigenvalues from the trace and determinant, then solve $(\\mathbf{A} - 7\\mathbf{I})\\mathbf{v} = \\mathbf{0}$."),
    "The eigenvalues solve $\\lambda^2 - 9\\lambda + 14 = 0$, so they are 7 and 2. "
    "For 7, the first row of $\\mathbf{A} - 7\\mathbf{I}$ reads $-v_1 + 2v_2 = 0$, so $\\mathbf{v} = (2, 1)$."))

# A14 singular value
M14 = np.array([[2, 0], [3, 4.0]])
ev14 = np.linalg.eigvalsh(M14.T @ M14)
a14 = math.sqrt(ev14[-1])
A.append(item("a-singular", 4, ["eg-svd"], ["singular-value"], 180, "The largest stretch",
    "$\\mathbf{A} = \\begin{pmatrix} 2 & 0 \\\\ 3 & 4 \\end{pmatrix}$.", "What is the largest singular value of $\\mathbf{A}$? Give 4 decimal places.",
    num(r(a14), 0.0005, [("eig-of-A", 4, 0.0005), ("no-root", r(ev14[-1]), 0.0005)]),
    fb("Singular values are square roots of the eigenvalues of $\\mathbf{A}^T\\mathbf{A}$.", "Form $\\mathbf{A}^T\\mathbf{A}$, find its largest eigenvalue, then take the square root.",
       {"eig-of-A": "You gave an eigenvalue of $\\mathbf{A}$. Singular values come from $\\mathbf{A}^T\\mathbf{A}$.",
        "no-root": "You gave the eigenvalue of $\\mathbf{A}^T\\mathbf{A}$. Take its square root."}),
    f"$\\mathbf{{A}}^T\\mathbf{{A}} = \\begin{{pmatrix}} 13 & 12 \\\\ 12 & 16 \\end{{pmatrix}}$, whose eigenvalues solve $\\lambda^2 - 29\\lambda + 64 = 0$. "
    f"The larger is about {ev14[-1]:.4f}, so the largest singular value is about {a14:.4f}."))

# A15 least squares and PCA in NumPy (code parts)
X15a = [[1, 0.0], [1, 1.0], [1, 2.0], [1, 4.0]]
y15a = [1.2, 1.9, 3.1, 4.8]
X15b = [[1, 2.0, 1.0], [1, 3.0, 0.0], [1, 5.0, 2.0], [1, 7.0, 1.0], [1, 8.0, 3.0]]
y15b = [3.1, 2.8, 6.2, 6.9, 9.4]
X15c = [[1, 1.5], [1, 1.5]]
y15c = [2.0, 2.0]


def ls_ref(X, y):
    beta, *_ = np.linalg.lstsq(np.array(X), np.array(y), rcond=None)
    return beta


R15a = [[0.010, 0.012], [-0.020, -0.018], [0.015, 0.011], [0.000, 0.004], [-0.005, -0.009]]
R15b = [[0.02, -0.01, 0.00], [0.01, 0.00, 0.02], [-0.03, 0.02, -0.01], [0.00, 0.01, 0.01], [0.04, -0.03, 0.02], [-0.01, 0.00, -0.02]]
R15c = [[1.0, 0.0], [-1.0, 0.0], [3.0, 0.0], [-3.0, 0.0]]


def pc_ref(R):
    R = np.array(R)
    Z = R - R.mean(axis=0)
    _, _, vt = np.linalg.svd(Z, full_matrices=False)
    w = vt[0]
    return w if w.sum() > 0 else -w


ls_tests = py_tests([
    ("import numpy as np; X = np.array(%r); y = np.array(%r)" % (X15a, y15a), "ls_fit(X, y)", pyval(ls_ref(X15a, y15a)), "isclose"),
    ("import numpy as np; X = np.array(%r); y = np.array(%r)" % (X15b, y15b), "ls_fit(X, y)", pyval(ls_ref(X15b, y15b)), "isclose"),
    ("import numpy as np; X = np.array(%r); y = np.array(%r)" % (X15a, y15a), "float(np.sum(ls_fit(X, y)))", pyval(ls_ref(X15a, y15a).sum()), "isclose"),
    (None, "'lstsq' not in __learner_source__ and 'polyfit' not in __learner_source__", "True", "equal"),
])
pc_tests = py_tests([
    ("import numpy as np; R = np.array(%r)" % (R15a,), "first_pc(R)", pyval(pc_ref(R15a)), "isclose"),
    ("import numpy as np; R = np.array(%r)" % (R15b,), "first_pc(R)", pyval(pc_ref(R15b)), "isclose"),
    ("import numpy as np; R = np.array(%r)" % (R15c,), "first_pc(R)", pyval(pc_ref(R15c)), "isclose"),
    ("import numpy as np; R = np.array(%r) + 5.0" % (R15b,), "first_pc(R)", pyval(pc_ref(R15b)), "isclose"),
])
ls_sol = ("import numpy as np\n\n\ndef ls_fit(X, y):\n    # solve the normal equations X^T X b = X^T y\n"
          "    return np.linalg.solve(X.T @ X, X.T @ y)\n")
pc_sol = ("import numpy as np\n\n\ndef first_pc(R):\n    Z = R - R.mean(axis=0)            # centre each column\n"
          "    S = Z.T @ Z / (len(R) - 1)         # sample covariance\n    vals, vecs = np.linalg.eigh(S)    # eigenvalues in rising order\n"
          "    w = vecs[:, -1]\n    return w if w.sum() > 0 else -w\n")
A.append({"id": "a-ls-pca-code", "difficulty": 5, "skills": ["ls-fit", "eg-pca"], "tags": ["numpy-from-matrices"], "pace": 900,
    "title": "Least squares and PCA from the matrix operations",
    "prose": "Write both in NumPy from matrix products and one solver. Do not call `np.linalg.lstsq` or `np.polyfit`.",
    "parts": [
        {"question": "Write `ls_fit(X, y)`: the least-squares coefficients from the normal equations. `X` already holds a column of ones.",
         "widget": {"kind": "code", "language": "python",
                    "starter": "import numpy as np\n\n\ndef ls_fit(X, y):\n    # X: n by p array, y: length-n array\n    ...\n",
                    "solution": ls_sol,
                    "examples": [{"setup": ls_tests[0]["setup"], "call": "ls_fit(X, y)", "expect": "[1.14, 0.92]", "compare": "isclose"}],
                    "tests": ls_tests,
                    "how": "Check runs 4 hidden tests. Arrays are compared entry by entry with `math.isclose` at a relative tolerance of 1e-9. Test 4 reads your source for `lstsq` and `polyfit`."},
         "feedback": code_fb("The normal equations give the coefficients in one solve.",
                             {"test-2": "Test 2 has two regressors and an intercept. Solve $\\mathbf{X}^T\\mathbf{X}\\boldsymbol\\beta = \\mathbf{X}^T\\mathbf{y}$ for all three.",
                              "test-4": "Your source calls `lstsq` or `polyfit`. Build the normal equations yourself and use `np.linalg.solve`."})},
        {"question": "Write `first_pc(R)`: the unit loading vector of the first principal component of `R`, whose rows are days. Sign it so its entries sum to a positive number.",
         "widget": {"kind": "code", "language": "python", "cumulative": False,
                    "starter": "import numpy as np\n\n\ndef first_pc(R):\n    # R: days by assets array of returns\n    ...\n",
                    "solution": pc_sol,
                    "examples": [{"setup": pc_tests[0]["setup"], "call": "first_pc(R)", "expect": pc_tests[0]["expect"], "compare": "isclose"}],
                    "tests": pc_tests,
                    "how": "Check runs 4 hidden tests. Vectors are compared entry by entry at a relative tolerance of 1e-9. Test 4 adds 5 to every return."},
         "feedback": code_fb("Centre, form the covariance, take the top eigenvector.",
                             {"test-2": "Test 2's returns do not average 0. Centre each column before you form the covariance.",
                              "test-3": "Test 3 has a column of zeros. The loading is $(1, 0)$, with the sign rule applied.",
                              "test-4": "Test 4 shifts every return by 5. Centre each column before you form the covariance."})}],
    "explain": {"text": "Least squares solves $\\mathbf{X}^T\\mathbf{X}\\boldsymbol\\beta = \\mathbf{X}^T\\mathbf{y}$, so `np.linalg.solve(X.T @ X, X.T @ y)` is the fit. "
                        "The first principal component is the top eigenvector of the sample covariance of the centred columns. "
                        "`eigh` lists eigenvalues in rising order, so the last column is the one we want."}})

# ======================================================================== Paper B: probability, statistics and finance
# B1 Bayes
pb, sens, fpr = 0.04, 0.8, 0.03
b1 = pb * sens / (pb * sens + (1 - pb) * fpr)
B.append(item("b-fraud-flag", 3, ["bayes"], ["bayes-flag"], 150, "A flagged trade",
    "4% of trades are bad. A fraud flag fires on 80% of bad trades and on 3% of honest ones.",
    "A trade is flagged. What is the probability that it is bad? Give 4 decimal places.",
    num(r(b1, 4), 0.0005, [("sensitivity", sens, 0.0005), ("base-rate", pb, 0.0005)]),
    fb("Flagged bad trades over all flagged trades.", "Compare the share of trades that are bad and flagged with the share that are flagged at all.",
       {"sensitivity": "You gave $P(\\text{flag} \\mid \\text{bad})$. The question asks for $P(\\text{bad} \\mid \\text{flag})$.",
        "base-rate": "You gave the share of bad trades before the flag. Update it on the flag."}),
    f"Bad and flagged is $0.04 \\times 0.8 = 0.032$; honest and flagged is $0.96 \\times 0.03 = 0.0288$. "
    f"So $P(\\text{{bad}} \\mid \\text{{flag}}) = \\tfrac{{0.032}}{{0.0608}} \\approx {b1:.4f}$."))

# B2 two-state chain
puu, pdu = 0.85, 0.25
b2 = pdu / ((1 - puu) + pdu)
B.append(item("b-regime-share", 3, ["mc-longrun"], ["stationary"], 120, "Up days in the long run",
    "Each day a market is in an up or a down regime. From up it stays up with probability 0.85. From down it moves to up with probability 0.25.",
    "In the long run, what share of days are up days?",
    num(r(b2, 4), 0.0005, [("stay-prob", puu, 0.0005), ("average", r((puu + pdu) / 2, 4), 0.0005)]),
    fb("Flow out of up balances flow into up.", "Set $\\pi_u \\times 0.15 = (1 - \\pi_u) \\times 0.25$ and solve.",
       {"stay-prob": "You gave the chance of staying up for one day. The long-run share balances both moves.",
        "average": "You averaged the two transition chances. Balance the flows instead."}),
    f"In balance, $0.15\\pi_u = 0.25(1 - \\pi_u)$. So $\\pi_u = \\tfrac{{0.25}}{{0.40}} = {b2}$."))

# B3 CLT
n3, p3w = 350, 0.53
mu3 = 2 * p3w - 1
var3 = 1 - mu3 ** 2
sd3 = math.sqrt(n3 * var3)
b3 = Phi(-n3 * mu3 / sd3)
B.append(item("b-many-bets", 4, ["dl-clt"], ["clt-sum"], 180, "Three hundred and fifty small bets",
    "A trader makes 350 independent bets. Each wins £1 with probability 0.53 and loses £1 otherwise.",
    "With the normal approximation and no continuity correction, what is the probability of an overall loss? Give 4 decimal places.",
    num(r(b3, 4), 0.001, [("no-root", r(Phi(-n3 * mu3 / (n3 * var3)), 4), 0.001)]),
    fb(f"Mean {n3 * mu3:.0f}, standard deviation about {sd3:.2f}.", "Find the mean and variance of one bet, scale both by 350, then standardise 0.",
       {"no-root": f"You divided by the variance, {n3 * var3:.2f}. Divide by its square root."}),
    f"One bet has mean $0.06$ and variance $1 - 0.0036 = 0.9964$. The total has mean {n3 * mu3:.0f} and standard deviation $\\sqrt{{{n3 * var3:.2f}}} \\approx {sd3:.2f}$. "
    f"So $P(\\text{{total}} < 0) \\approx \\Phi(-{n3 * mu3 / sd3:.4f}) \\approx {b3:.4f}$."))

# B4 variance of a combination
vx, vy, cxy = 4, 1, 0.5
b4 = 4 * vx + 9 * vy - 2 * 2 * 3 * cxy
B.append(item("b-var-combo", 3, ["rv-variance"], ["variance-rules"], 120, "Variance of a spread",
    "$Var(X) = 4$, $Var(Y) = 1$ and $Cov(X, Y) = 0.5$.", "What is $Var(2X - 3Y + 5)$?",
    num(b4, 0.001, [("plus-cov", 4 * vx + 9 * vy + 12 * cxy, 0.001), ("ignored-cov", 4 * vx + 9 * vy, 0.001)]),
    fb("Squares on the coefficients, and a covariance term with its sign.", "Use $Var(aX + bY + c) = a^2 Var(X) + b^2 Var(Y) + 2ab\\,Cov(X, Y)$.",
       {"plus-cov": "You added the covariance term. With $a = 2$ and $b = -3$, $2ab$ is negative.",
        "ignored-cov": "You left out $2ab\\,Cov(X, Y)$. The two are correlated."}),
    f"$Var = 4 \\cdot 4 + 9 \\cdot 1 + 2(2)(-3)(0.5) = 16 + 9 - 6 = {b4:.0f}$. The constant 5 adds nothing."))

# B5 gambler's ruin
rr = 0.4 / 0.6
b5 = (1 - rr ** 3) / (1 - rr ** 5)
B.append(item("b-ruin-target", 4, ["mc-walks"], ["gamblers-ruin"], 180, "Reach £5 before £0",
    "You hold £3 and bet £1 at a time. Each bet wins with probability 0.6. You stop at £0 or at £5.",
    "What is the probability that you reach £5? Give 4 decimal places.",
    num(r(b5, 4), 0.0005, [("fair", 0.6, 0.0005)]),
    fb("The ruin formula with ratio $\\tfrac{q}{p} = \\tfrac23$.", "Use $\\dfrac{1 - (q/p)^i}{1 - (q/p)^N}$ with $i = 3$ and $N = 5$.",
       {"fair": "You used $\\tfrac{i}{N}$, the answer for a fair game. These bets favour you."}),
    f"With $\\tfrac{{q}}{{p}} = \\tfrac23$, the chance is $\\dfrac{{1 - (2/3)^3}}{{1 - (2/3)^5}} = \\tfrac{{171}}{{211}} \\approx {b5:.4f}$."))

# B6 MLE of an exponential rate
w6 = [0.8, 1.7, 0.4, 2.3, 1.3]
m6 = sum(w6) / len(w6)
b6 = 1 / m6
B.append(item("b-mle-rate", 3, ["es-mle"], ["mle-exponential"], 120, "A rate from waiting times",
    "Waiting times between trades, in seconds, are 0.8, 1.7, 0.4, 2.3 and 1.3. Model them as exponential with rate $\\lambda$.",
    "What is the maximum likelihood estimate of $\\lambda$, per second? Give 4 decimal places.",
    num(r(b6, 4), 0.0005, [("gave-mean", r(m6, 4), 0.0005)]),
    fb("The estimate is one over the sample mean.", "Maximise $n \\ln \\lambda - \\lambda \\sum x_i$, or recall the result.",
       {"gave-mean": "You gave the mean waiting time. The rate is its reciprocal."}),
    f"The log-likelihood $5 \\ln \\lambda - 6.5\\lambda$ peaks at $\\lambda = \\tfrac{{5}}{{6.5}}$. That is $\\tfrac{{1}}{{1.3}} \\approx {b6:.4f}$."))

# B7 interval half-width
n7, s7 = 144, 30
b7 = 1.96 * s7 / math.sqrt(n7)
B.append(item("b-interval-width", 3, ["es-intervals"], ["interval-width"], 90, "How wide is the interval",
    "A market maker's profit on each of 144 trades has sample standard deviation 30p.",
    "What is the half-width of a 95% confidence interval for the mean profit per trade, in pence? Use 1.96.",
    num(r(b7, 4), 0.005, [("no-root", r(1.96 * s7 / n7, 4), 0.005), ("no-se", r(1.96 * s7, 4), 0.005)], unit="pence"),
    fb("1.96 standard errors.", "The standard error is $\\tfrac{s}{\\sqrt{n}}$.",
       {"no-root": "You divided by 144. The standard error divides by $\\sqrt{144} = 12$.",
        "no-se": "You used the standard deviation of one trade. The mean has the standard error."}),
    f"The standard error is $\\tfrac{{30}}{{12}} = 2.5$p. The half-width is $1.96 \\times 2.5 = {b7:.1f}$p."))

# B8 p-value
n8, m8, s8 = 484, 0.07, 1.1
z8 = m8 / (s8 / math.sqrt(n8))
b8 = 2 * (1 - Phi(z8))
B.append(item("b-pvalue-mean", 3, ["ht-pvalue"], ["z-test"], 150, "Is the mean return zero",
    "A strategy's mean daily return over 484 days is 0.07%, with standard deviation 1.1%.",
    "With the normal approximation, what is the two-sided p-value for a true mean of zero? Give 3 decimal places.",
    num(r(b8, 3), 0.005, [("one-sided", r(1 - Phi(z8), 3), 0.005)]),
    fb(f"$z \\approx {z8:.2f}$, which is not far out.", "Standardise with the standard error $\\tfrac{1.1}{\\sqrt{484}}$, then double the tail.",
       {"one-sided": "You gave one tail. A two-sided test doubles it."}),
    f"The standard error is $\\tfrac{{1.1}}{{22}} = 0.05$, so $z = \\tfrac{{0.07}}{{0.05}} = {z8:.1f}$. "
    f"The p-value is $2(1 - \\Phi({z8:.2f})) \\approx {b8:.3f}$."))

# B9 multiple testing
p0_9, p1_9 = 0.95 ** 40, 40 * 0.05 * 0.95 ** 39
b9 = 1 - p0_9 - p1_9
B.append(item("b-forty-tests", 4, ["ht-multiple"], ["family-wise"], 120, "Forty strategies with no edge",
    "You backtest 40 independent strategies, none with any edge. Each is tested at the 5% level.",
    "What is the probability that at least two look significant? Give 4 decimal places.",
    num(r(b9, 4), 0.0005, [("at-least-one", r(1 - p0_9, 4), 0.0005), ("expected", 2, 0.0005)]),
    fb("One minus the chances of none and of exactly one.", "Find $P(0) = 0.95^{40}$ and $P(1) = 40 \\times 0.05 \\times 0.95^{39}$ first.",
       {"at-least-one": "You found the chance of at least one. Subtract the chance of exactly one too.",
        "expected": "You gave the expected number of false finds, $40 \\times 0.05$. The question asks for a probability."}),
    f"None fires with probability $0.95^{{40}} \\approx {p0_9:.4f}$. Exactly one fires with probability $2 \\times 0.95^{{39}} \\approx {p1_9:.4f}$. "
    f"So at least two fire with probability about {b9:.4f}."))

# B10 OLS by hand, then read its table
X10a = [[1, 1.0], [1, 2.0], [1, 3.0], [1, 4.0], [1, 6.0]]
y10a = [2.1, 2.9, 4.2, 4.8, 7.1]
X10b = [[1, 0.5, 1.0], [1, 1.5, 0.0], [1, 2.0, 2.0], [1, 3.5, 1.0], [1, 4.0, 3.0], [1, 5.5, 1.0], [1, 6.0, 2.0]]
y10b = [1.4, 2.2, 4.1, 4.0, 6.3, 5.9, 7.2]


def ols_ref(X, y):
    X, y = np.array(X), np.array(y)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    n, p = X.shape
    s2 = res @ res / (n - p)
    se = np.sqrt(np.diag(s2 * np.linalg.pinv(X.T @ X)))
    r2 = 1 - (res @ res) / np.sum((y - y.mean()) ** 2)
    return beta, se, r2


ba, sa, ra = ols_ref(X10a, y10a)
bb, sb, rb = ols_ref(X10b, y10b)
ols_tests = []
for X_, y_, (bt, se_, r2_) in ((X10a, y10a, (ba, sa, ra)), (X10b, y10b, (bb, sb, rb))):
    st = "import numpy as np; X = np.array(%r); y = np.array(%r)" % (X_, y_)
    ols_tests += py_tests([(st, "ols(X, y)[0]", pyval(bt), "isclose"), (st, "ols(X, y)[1]", pyval(se_), "isclose"),
                           (st, "float(ols(X, y)[2])", pyval(r2_), "isclose")])


def t_density(x, k):
    return math.gamma((k + 1) / 2) / (math.sqrt(k * math.pi) * math.gamma(k / 2)) * (1 + x * x / k) ** (-(k + 1) / 2)


def t_two_sided(t, k, m=20000):
    """Simpson's rule for 2 * integral from |t| to infinity, after the substitution x = |t| / u."""
    a, b, h = 1e-9, 1.0, (1.0 - 1e-9) / m
    f = lambda u: t_density(abs(t) / u, k) * abs(t) / u ** 2
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, m))
    return 2 * s * h / 3


coef10, se10, n10 = 0.42, 0.15, 30
t10 = coef10 / se10
p10 = t_two_sided(t10, n10 - 2)
ols_sol = ("import numpy as np\n\n\ndef ols(X, y):\n    n, p = X.shape\n    XtX_inv = np.linalg.inv(X.T @ X)\n    beta = XtX_inv @ X.T @ y\n"
           "    resid = y - X @ beta\n    s2 = resid @ resid / (n - p)          # residual variance, n - p degrees of freedom\n"
           "    se = np.sqrt(np.diag(s2 * XtX_inv))\n    r2 = 1 - resid @ resid / np.sum((y - y.mean()) ** 2)\n    return beta, se, r2\n")
B.append({"id": "b-ols-table", "difficulty": 4, "skills": ["rg-fit", "rg-inference"], "tags": ["ols-summary"], "pace": 900,
    "title": "A regression by hand, then its table",
    "prose": "statsmodels' `OLS(y, X).fit()` reports coefficients, standard errors and $R^2$. Your NumPy version must match them.",
    "parts": [
        {"question": "Write `ols(X, y)`: return `beta`, `se` and `r2` as statsmodels does. `X` already holds a column of ones.",
         "widget": {"kind": "code", "language": "python",
                    "starter": "import numpy as np\n\n\ndef ols(X, y):\n    # return beta, se, r2\n    ...\n",
                    "solution": ols_sol,
                    "examples": [{"setup": ols_tests[0]["setup"], "call": "ols(X, y)[0]", "expect": ols_tests[0]["expect"], "compare": "isclose"}],
                    "tests": ols_tests,
                    "how": "Check runs 6 hidden tests: the coefficients, standard errors and $R^2$ of two fits. Each is compared at a relative tolerance of 1e-9."},
         "feedback": code_fb("Coefficients, standard errors and $R^2$ all match.",
                             {"test-2": "The standard errors differ. statsmodels divides the residual sum of squares by $n - p$, not $n$.",
                              "test-3": "$R^2$ differs. Use $1 - \\tfrac{\\text{RSS}}{\\text{TSS}}$ with TSS about the mean of $y$.",
                              "test-5": "The standard errors of the two-regressor fit differ. Take the diagonal of $s^2(\\mathbf{X}^T\\mathbf{X})^{-1}$."})},
        {"question": "Another fit has 30 rows, an intercept and one regressor. The regressor's row reads coef 0.42 and std err 0.15. What is its t statistic?",
         "widget": num(r(t10, 4), 0.005, [("inverse", r(se10 / coef10, 4), 0.005)]),
         "feedback": fb("The coefficient over its standard error.", "Divide the coefficient by its standard error.",
                        {"inverse": "You divided the standard error by the coefficient. Turn the fraction over."})},
        {"question": f"The same row reports P>|t| as {p10:.3f}. What does that number say?",
         "widget": choice([
             opt("a", f"If the coefficient were 0, a $\\lvert t \\rvert \\ge {t10:.1f}$ would have chance {p10 * 100:.1f}%.", correct=True),
             opt("b", f"The probability that the true coefficient is zero is {p10 * 100:.1f}%.", "You read the p-value as a probability about the coefficient. It is a probability about the data, given zero."),
             opt("c", f"The coefficient is right with probability {100 - p10 * 100:.1f}%.", "You took one minus the p-value as a confidence in the estimate. No such reading exists."),
             opt("d", f"The regressor explains {p10 * 100:.1f}% of the variance of $y$.", "You mixed the p-value up with $R^2$, which is another line of the table.")]),
         "feedback": fb("A p-value is computed as if the null were true.", "Ask what the test assumes when it computes the tail.")}],
    "explain": {"text": f"The standard errors are the square roots of the diagonal of $s^2(\\mathbf{{X}}^T\\mathbf{{X}})^{{-1}}$, with $s^2 = \\tfrac{{\\text{{RSS}}}}{{n - p}}$. "
                        f"The t statistic is $\\tfrac{{0.42}}{{0.15}} = {t10:.1f}$, on $30 - 2 = 28$ degrees of freedom. "
                        f"Its two-sided tail under a zero coefficient is about {p10:.3f}."}})

# B11 put-call parity
C11, S11, K11, r11, T11 = 7.20, 100, 105, 0.04, 0.5
pv11 = K11 * math.exp(-r11 * T11)
b11 = C11 - S11 + pv11
B.append(item("b-parity-put", 3, ["op-parity"], ["put-call-parity"], 150, "The put that parity forces",
    "A European call costs £7.20. The share is at £100 and the strike is £105. Expiry is in 6 months, and the rate is 4% a year, continuously compounded.",
    "What must the European put with the same strike and expiry cost, in pounds? Give 2 decimal places.",
    num(r(b11, 4), 0.005, [("no-discount", r(C11 - S11 + K11, 4), 0.005), ("sign-flip", r(C11 + S11 - pv11, 4), 0.005)], unit="£"),
    fb("Call plus discounted strike equals put plus share.", "Use $C + Ke^{-rT} = P + S$.",
       {"no-discount": "You used the strike itself. Parity holds with its present value, $105e^{-0.02}$.",
        "sign-flip": "You moved the share and the strike to the wrong sides. Solve $C + Ke^{-rT} = P + S$ for $P$."}),
    f"$Ke^{{-rT}} = 105e^{{-0.02}} \\approx {pv11:.4f}$. So $P = 7.20 + {pv11:.4f} - 100 \\approx {b11:.2f}$ pounds."))

# B12 two-step tree
S12, u12, d12, g12, K12 = 50, 1.2, 0.9, 1.02, 52
q12 = (g12 - d12) / (u12 - d12)
pay12 = [max(S12 * u12 ** (2 - j) * d12 ** j - K12, 0) for j in range(3)]
w12 = [q12 ** 2, 2 * q12 * (1 - q12), (1 - q12) ** 2]
b12 = sum(a * b for a, b in zip(w12, pay12)) / g12 ** 2
half12 = (0.25 * pay12[0] + 0.5 * pay12[1] + 0.25 * pay12[2]) / g12 ** 2
B.append(item("b-two-step", 4, ["tp-multistep"], ["binomial-tree"], 210, "A two-step tree",
    "A share is at £50. Each step it moves up by a factor 1.2 or down by 0.9. £1 grows to £1.02 per step.",
    "What is a European call with strike £52, expiring after two steps, worth now? Give 2 decimal places.",
    num(r(b12, 4), 0.005, [("half", r(half12, 4), 0.005), ("no-discount", r(b12 * g12 ** 2, 4), 0.005)], unit="£"),
    fb(f"$q = {q12:.1f}$, then discount twice.", "Find $q = \\tfrac{1.02 - 0.9}{1.2 - 0.9}$, weight the three payoffs, then divide by $1.02^2$.",
       {"half": "You used probability one half. The pricing probability is $q = 0.4$.",
        "no-discount": "You did not discount. Divide the expected payoff by $1.02^2$."}),
    f"$q = \\tfrac{{0.12}}{{0.3}} = {q12:.1f}$. The payoffs are 20, 2 and 0, at £72, £54 and £40.50. "
    f"So the call is $\\tfrac{{0.16 \\times 20 + 0.48 \\times 2}}{{1.0404}} \\approx {b12:.2f}$ pounds."))

# B13 order book
bids = [(99.98, 300), (99.97, 500)]
asks = [(100.02, 200), (100.03, 400)]
spread13 = asks[0][0] - bids[0][0]
avg13 = (200 * 100.02 + 300 * 100.03) / 500
book = ("| Bid size | Bid | Ask | Ask size |\n|---|---|---|---|\n| 300 | 99.98 | 100.02 | 200 |\n| 500 | 99.97 | 100.03 | 400 |")
B.append(parts("b-book-orders", 3, ["ms-book", "ms-orders"], ["order-book"], 240, "Orders against a book",
    "A share's order book, in pounds:\n\n" + book,
    [("What is the bid-ask spread, in pounds?",
      num(r(spread13, 4), 0.001, [("mid", 100.0, 0.001), ("second-level", r(asks[1][0] - bids[1][0], 4), 0.001)], unit="£"),
      fb("Best ask minus best bid.", "Subtract the best bid from the best ask.",
         {"mid": "You gave the mid-price. The spread is the gap between the best quotes.",
          "second-level": "You used the second level of the book. The spread uses the best bid and the best ask."})),
     ("A market order buys 500 shares. What is its average price, in pounds? Give 3 decimal places.",
      num(r(avg13, 4), 0.0005, [("top-only", 100.02, 0.0002), ("level-two", 100.03, 0.0002)], unit="£"),
      fb("It walks the book: 200 at the first ask, 300 at the next.", "Fill 200 at £100.02, the rest at £100.03, then average by size.",
         {"top-only": "Only 200 shares rest at £100.02. The other 300 fill at £100.03.",
          "level-two": "The first 200 shares fill at £100.02, before the order reaches £100.03."})),
     ("Instead, a limit order to buy 100 shares at £100.00 arrives. What happens to it?",
      choice([opt("a", "It rests as the new best bid, so the spread is £0.02.", correct=True),
              opt("b", "It fills at once at £100.02.", "You treated it as a market order. A buy limit at £100.00 cannot pay £100.02."),
              opt("c", "It fills at once at £99.98.", "You matched it with the best bid. A buy order trades only against asks."),
              opt("d", "It is rejected, because nobody sells at £100.00.", "You thought an order needs a seller at its price. A limit order that does not cross waits in the book.")]),
      fb("A limit buy below the best ask waits.", "Compare the limit price with the best ask."))],
    f"The spread is $100.02 - 99.98 = 0.04$ pounds. The market order pays $\\tfrac{{200 \\times 100.02 + 300 \\times 100.03}}{{500}} = {avg13:.3f}$ pounds. "
    "The limit order does not reach the ask, so it rests at £100.00 above the old best bid."))

# B14 CRR pricer in Python


def crr(S, K, r_, sig, T, n, call=True):
    dt = T / n
    u = math.exp(sig * math.sqrt(dt))
    d = 1 / u
    q = (math.exp(r_ * dt) - d) / (u - d)
    disc = math.exp(-r_ * dt)
    v = [max((S * u ** (n - j) * d ** j - K) if call else (K - S * u ** (n - j) * d ** j), 0.0) for j in range(n + 1)]
    for step in range(n, 0, -1):
        v = [disc * (q * v[j] + (1 - q) * v[j + 1]) for j in range(step)]
    return v[0]


def crr_div_put(S, K, r, div, sig, T, n):
    dt = T / n
    u = math.exp(sig * math.sqrt(dt))
    d = 1 / u
    q = (math.exp((r - div) * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    v = [max(K - S * u ** (n - j) * d ** j, 0.0) for j in range(n + 1)]
    for step in range(n, 0, -1):
        v = [disc * (q * v[j] + (1 - q) * v[j + 1]) for j in range(step)]
    return v[0]


CRR_PY = [(100, 100, 0.0, 0.0, 0.2, 1.0, 1), (100, 105, 0.03, 0.02, 0.25, 0.5, 1), (100, 105, 0.03, 0.02, 0.25, 0.5, 3),
          (80, 70, 0.05, 0.04, 0.3, 1.0, 4), (95, 120, 0.01, 0.0, 0.15, 2.0, 50), (150, 60, 0.02, 0.01, 0.2, 0.25, 10),
          (100, 100, 0.02, 0.03, 0.2, 1.0, 400)]
crr_tests = py_tests([(None, "crr_put(%s)" % ", ".join(repr(a) for a in args), pyval(crr_div_put(*args)), "isclose") for args in CRR_PY])
crr_tests[-1]["budget"] = 2000
crr_sol = ("import math\n\n\ndef crr_put(S, K, r, div, sigma, T, n):\n    dt = T / n\n    u = math.exp(sigma * math.sqrt(dt))\n    d = 1 / u\n"
           "    q = (math.exp((r - div) * dt) - d) / (u - d)   # the dividend lowers the drift\n    disc = math.exp(-r * dt)\n"
           "    v = [max(K - S * u ** (n - j) * d ** j, 0.0) for j in range(n + 1)]\n"
           "    for step in range(n, 0, -1):\n        v = [disc * (q * v[j] + (1 - q) * v[j + 1]) for j in range(step)]\n    return v[0]\n")
B.append(item("b-crr-python", 4, ["tp-multistep", "tp-riskneutral"], ["crr-pricer"], 900, "A put on a share that pays dividends",
    "The share pays a continuous dividend yield $\\delta$. On an $n$-step Cox-Ross-Rubinstein tree, $\\Delta t = \\tfrac{T}{n}$, "
    "$u = e^{\\sigma\\sqrt{\\Delta t}}$ and $d = \\tfrac1u$. Then $q = \\tfrac{e^{(r - \\delta)\\Delta t} - d}{u - d}$, and each step discounts by $e^{-r\\Delta t}$.",
    "Write `crr_put(S, K, r, div, sigma, T, n)`: the price of a European put by backward induction on that tree.",
    {"kind": "code", "language": "python",
     "starter": "import math\n\n\ndef crr_put(S, K, r, div, sigma, T, n):\n    # S spot, K strike, r rate, div dividend yield,\n    # sigma volatility, T years, n steps\n    ...\n",
     "solution": crr_sol,
     "examples": [{"call": crr_tests[0]["call"], "expect": crr_tests[0]["expect"], "compare": "isclose"}],
     "tests": crr_tests,
     "how": "Check runs 7 hidden tests. Each price is accepted at a relative tolerance of 1e-9. Test 7 has 400 steps."},
    code_fb("The tree prices match to rounding.",
            {"test-1": "Test 1 is one step at the money, with no rate or dividend. Check $u$, $d$ and $q$, and floor each payoff at 0.",
             "test-2": "Test 2 has a dividend yield. It enters $q$ as $e^{(r - \\delta)\\Delta t}$, but the discount stays $e^{-r\\Delta t}$.",
             "test-3": "Test 3 has three steps. Discount at every step, not once at the end with the wrong power.",
             "test-6": "Test 6 is far out of the money. A negative payoff must be floored at 0."}),
    "At expiry the put pays $\\max(K - S u^{n-j} d^j, 0)$ at each node. "
    "Each step back replaces a pair of values by $e^{-r\\Delta t}(q v_{\\text{up}} + (1 - q) v_{\\text{down}})$. "
    "The dividend only lowers the growth inside $q$."))

# ======================================================================== Paper C: programming in Python and C++
# C1 the price-file exit task, in three code parts


def rets(prices):
    return [prices[i] / prices[i - 1] - 1 for i in range(1, len(prices))]


def csv_closes(text):
    lines = [ln for ln in text.strip().split('\n')]
    head = lines[0].split(',')
    rows = [dict(zip(head, ln.split(','))) for ln in lines[1:]]
    return [float(rw['close']) for rw in sorted(rows, key=lambda rw: rw['date'])]


def avol(rs):
    m = sum(rs) / len(rs)
    return math.sqrt(sum((x - m) ** 2 for x in rs) / (len(rs) - 1)) * math.sqrt(252)


def mdd(prices):
    peak, worst = prices[0], 0.0
    for p in prices:
        peak = max(peak, p)
        worst = max(worst, 1 - p / peak)
    return worst


CSV1 = "date,close\n2026-03-04,102.0\n2026-03-02,100.0\n2026-03-03,98.0\n"
CSV2 = "date,close\n2025-11-03,312.4\n2025-11-04,309.9\n2025-11-05,314.6\n2025-11-06,313.1\n2025-11-07,317.8\n"
CSV3 = "date,close\n2026-01-09,41.25\n2026-01-08,40.5\n"
CSV4 = "close,date\n73.1,2026-05-13\n72.4,2026-05-12\n74.9,2026-05-15\n70.2,2026-05-14\n"
csv_tests = py_tests([("text = %r" % t, "returns_from_csv(text)", pyval(rets(csv_closes(t))), "isclose") for t in (CSV1, CSV2, CSV3, CSV4)])
V1 = [0.012, -0.004, 0.007, -0.011, 0.003]
V2 = [0.02, -0.02]
V3 = [0.001, 0.0035, -0.0022, 0.0041, -0.0007, 0.0012, -0.0031, 0.0026]
vol_tests = py_tests([(None, "annual_vol(%r)" % v, pyval(avol(v)), "isclose") for v in (V1, V2, V3)]
                     + [("import numpy as np", "annual_vol(np.array(%r))" % V1, pyval(avol(V1)), "isclose")])
P1 = [100, 120, 90, 130, 104]
P2 = [50, 51, 53, 58]
P3 = [80, 72, 76, 62, 66, 79, 85, 59.5]
P4 = [200, 150, 180, 120]
dd_tests = py_tests([(None, "worst_drawdown(%r)" % p, pyval(mdd(p)), "isclose") for p in (P1, P2, P3, P4)])
csv_sol = ("import io\nimport pandas as pd\n\n\ndef returns_from_csv(text):\n    df = pd.read_csv(io.StringIO(text)).sort_values('date')\n"
           "    return df['close'].pct_change().dropna().tolist()\n")
vol_sol = ("import numpy as np\n\n\ndef annual_vol(returns):\n    # sample standard deviation, scaled by the square root of 252 days\n"
           "    return float(np.std(returns, ddof=1) * np.sqrt(252))\n")
dd_sol = ("def worst_drawdown(prices):\n    peak, worst = prices[0], 0.0\n    for p in prices:\n        peak = max(peak, p)\n"
          "        worst = max(worst, 1 - p / peak)\n    return worst\n")
C.append({"id": "c-price-file", "difficulty": 4, "skills": ["pd-time", "np-arrays", "pf-functions"], "tags": ["price-file-risk"], "pace": 900,
    "title": "Risk figures from a price file",
    "prose": "A CSV of daily closes has the columns `date` and `close`, with dates as `YYYY-MM-DD`. Rows may come in any order.",
    "parts": [
        {"question": "Write `returns_from_csv(text)`: the simple daily returns, oldest first, as a list. `text` is the whole file as a string.",
         "widget": {"kind": "code", "language": "python",
                    "starter": "import io\nimport pandas as pd\n\n\ndef returns_from_csv(text):\n    # text: the file's contents, header line first\n    ...\n",
                    "solution": csv_sol,
                    "examples": [{"setup": csv_tests[0]["setup"], "call": "returns_from_csv(text)", "expect": csv_tests[0]["expect"], "compare": "isclose"}],
                    "tests": csv_tests,
                    "how": "Check runs 4 hidden tests. Lists are compared entry by entry at a relative tolerance of 1e-9."},
         "feedback": code_fb("Sorted by date, then one return per pair of days.",
                             {"test-1": "Test 1 is out of date order. Sort by `date` before you take returns.",
                              "test-4": "Test 4 puts `close` before `date`. Read the columns by name, not by position."})},
        {"question": "Write `annual_vol(returns)`: the annualised volatility, from the sample standard deviation and 252 trading days.",
         "widget": {"kind": "code", "language": "python", "cumulative": False,
                    "starter": "import numpy as np\n\n\ndef annual_vol(returns):\n    ...\n",
                    "solution": vol_sol,
                    "examples": [{"call": vol_tests[0]["call"], "expect": vol_tests[0]["expect"], "compare": "isclose"}],
                    "tests": vol_tests,
                    "how": "Check runs 4 hidden tests at a relative tolerance of 1e-9. Test 4 passes a NumPy array."},
         "feedback": code_fb("The sample standard deviation times $\\sqrt{252}$.",
                             {"test-1": "Use the sample standard deviation, which divides by $n - 1$: `ddof=1`.",
                              "test-2": "Test 2 has two returns. With `ddof=1` the standard deviation divides by 1."})},
        {"question": "Write `worst_drawdown(prices)`: the largest fall from a running peak, as a positive fraction of that peak.",
         "widget": {"kind": "code", "language": "python", "cumulative": False,
                    "starter": "def worst_drawdown(prices):\n    ...\n",
                    "solution": dd_sol,
                    "examples": [{"call": dd_tests[0]["call"], "expect": dd_tests[0]["expect"], "compare": "isclose"}],
                    "tests": dd_tests,
                    "how": "Check runs 4 hidden tests at a relative tolerance of 1e-9. A price path that only rises has drawdown 0."},
         "feedback": code_fb("A running peak and the worst fall below it.",
                             {"test-1": "Test 1 falls 25% from 120, then 20% from 130. Measure each fall from the running peak and keep the worst.",
                              "test-3": "Test 3's worst fall, 30%, comes after a new peak at 85. Update the peak as you go."})}],
    "explain": {"text": "Sorting by date first makes the returns run oldest to newest, and `pct_change` gives $\\tfrac{p_t}{p_{t-1}} - 1$. "
                        "Annualised volatility is the sample standard deviation times $\\sqrt{252}$. "
                        "The drawdown keeps a running peak and the largest $1 - \\tfrac{p}{\\text{peak}}$."}})

# C2 an honest axis
C.append(item("c-log-axis", 3, ["pl-honest"], ["axis-choice"], 120, "Two growth paths on one chart",
    "You plot the value of £1 in two strategies over 10 years. One ends at £30, the other at £2.50.",
    "Which y-axis lets a reader compare their percentage swings by eye?",
    choice([opt("a", "A log scale for both lines.", correct=True),
            opt("b", "A linear scale starting at 0.", "You kept a linear scale. The £30 line then dwarfs the other, so its swings look larger."),
            opt("c", "Two linear axes, one for each line.", "You gave each line its own scale. Two scales can make any two lines look alike."),
            opt("d", "A linear scale from £1 to £3.", "You cut the axis to fit the small line. The large one runs off the chart.")]),
    fb("A log axis turns ratios into distances.", "Ask which axis makes a 10% fall the same height at £2 and at £20."),
    "On a log scale, $\\ln(0.9p) - \\ln p = \\ln 0.9$ whatever $p$ is. So a 10% fall has one height on both lines."))

# C3 broadcasting
C.append(item("c-broadcast-shape", 2, ["np-broadcast"], ["broadcast-shape"], 60, "Two shapes meet",
    "`a` has shape `(5, 1)` and `b` has shape `(3,)`.", "What is the shape of `a - b`?",
    choice([opt("a", "`(5, 3)`", correct=True),
            opt("b", "`(5, 1)`", "You kept the shape of `a`. Its axis of length 1 stretches to 3."),
            opt("c", "An error", "You expected the last sizes to be equal. A size of 1 matches any size."),
            opt("d", "`(3, 5)`", "You put the axis of `b` first. `b` lines up with the last axis.")]),
    fb("Shapes align from the right, and 1 stretches.", "Line the shapes up from the right: `(5, 1)` against `(1, 3)`."),
    "NumPy reads `b` as shape `(1, 3)`. Each axis of length 1 stretches to match, giving `(5, 3)`."))

# C4 group-by
pnl4 = {"rates": [120, -40, 65], "fx": [30, 90], "credit": [-15, 210, -60]}
sums4 = {k: sum(v) for k, v in pnl4.items()}
c4 = max(sums4.values())
rows4 = [("rates", 120), ("fx", 30), ("credit", -15), ("rates", -40), ("credit", 210), ("fx", 90), ("rates", 65), ("credit", -60)]
assert sorted(rows4) == sorted((k, x) for k, v in pnl4.items() for x in v)
tab4 = "| desk | pnl |\n|---|---|\n" + "\n".join(f"| {k} | {x} |" for k, x in rows4)
C.append(item("c-desk-sum", 2, ["pd-group"], ["group-by"], 90, "The best desk",
    "A frame `df` holds eight trades:\n\n" + tab4, "What does `df.groupby('desk')['pnl'].sum().max()` return?",
    num(c4, 0, [("single-max", 210, 0)]),
    fb("Sum within each desk, then take the largest sum.", "Add the P&L of each desk first.",
       {"single-max": "You took the largest single trade. The sum comes first, per desk."}),
    f"The desk sums are rates {sums4['rates']}, fx {sums4['fx']} and credit {sums4['credit']}. The largest is {c4}."))

# C5 SQL
tr5 = [(1, 'rates', 200, 10.5), (2, 'fx', 50, 20.0), (3, 'rates', 150, 10.0), (4, 'fx', 300, 2.5), (5, 'credit', 400, 1.25), (6, 'fx', 120, 5.0)]


def q5(rows, where=True, having=True):
    g = {}
    for _, desk, qty, px in rows:
        if where and qty < 100:
            continue
        g.setdefault(desk, []).append((qty * px, px))
    out = [(dk, sum(n for n, _ in v)) for dk, v in g.items() if not having or sum(p for _, p in v) / len(v) > 3]
    return sorted(out, key=lambda t: -t[1])


res5 = q5(tr5)
tab5 = "| id | desk | qty | px |\n|---|---|---|---|\n" + "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in tr5)
sql5 = ("```sql\nSELECT desk, SUM(qty * px) AS notional\nFROM trades\nWHERE qty >= 100\nGROUP BY desk\n"
        "HAVING AVG(px) > 3\nORDER BY notional DESC;\n```")
C.append(parts("c-sql-having", 3, ["sql-aggregate"], ["group-having"], 180, "A grouped query",
    "The table `trades`:\n\n" + tab5 + "\n\n" + sql5,
    [("How many rows does the query return?", num(len(res5), 0, [("no-having", len(q5(tr5, having=False)), 0)]),
      fb("WHERE drops rows, HAVING drops groups.", "Filter the rows, group them, then keep groups whose average price is above 3.",
         {"no-having": "You kept the credit desk. Its average price, 1.25, fails HAVING."})),
     ("What is the notional on the second row?", num(res5[1][1], 0.001, [("no-where", q5(tr5, where=False)[1][1], 0.001), ("first-row", res5[0][1], 0.001)]),
      fb("The fx desk, from trades 4 and 6.", "Order the surviving groups by notional, largest first.",
         {"no-where": "You kept trade 2, with quantity 50. WHERE removes it before grouping.",
          "first-row": "That is the first row, the rates desk. The second row is fx."}))],
    f"WHERE drops trade 2. Rates keeps trades 1 and 3, with notional {res5[0][1]:g}; fx keeps 4 and 6, with {res5[1][1]:g}. "
    "Credit's average price is 1.25, so HAVING drops it."))

# C6 Git
C.append(item("c-git-branch", 3, ["gt-branches"], ["branch-workflow"], 120, "A fix on its own branch",
    "You fix the annualisation in `vol.py` of your price-file project and want it on GitHub for review.",
    "Put the steps in order. Leave out any that do not belong.",
    order([line("g1", "`git switch -c fix-vol`"), line("g2", "Edit `vol.py` and run `pytest`"), line("g3", "`git add vol.py`"),
           line("g4", "`git commit -m \"Use 252 trading days\"`"), line("g5", "`git push -u origin fix-vol`"),
           line("x1", "`git push origin main`", "You pushed main. The commit is on fix-vol, so main has nothing new."),
           line("x2", "`git reset --hard`", "This throws away your edit before it is committed.")],
          ["g1", "g2", "g3", "g4", "g5"], ["x1", "x2"], same=[["g1", "g2"]]),
    fb("Branch and edit, stage, commit, push the branch.", "Commit on the new branch, then push that branch.",
       {"x1": "You pushed main. The commit is on fix-vol, so main has nothing new.",
        "x2": "`git reset --hard` throws away your edit before it is committed.",
        "left-out": "One step that belongs is missing. Each of branch, edit, add, commit and push is needed."}),
    "The branch must exist before the commit, so the commit lands on it. Staging picks the file, and the commit records it. "
    "`push -u` sends fix-vol and links it to the remote branch."))

# C7 pytest
C.append(item("c-pytest-catch", 3, ["pt-basics"], ["test-catches-bug"], 120, "Which test catches the bug",
    "This function should return the change from `old` to `new` as a fraction of `old`:\n\n"
    "```python\ndef pct_change(old, new):\n    return (new - old) / new\n```",
    "Which test fails on this bug?",
    choice([opt("a", "`assert pct_change(100, 110) == pytest.approx(0.1)`", correct=True),
            opt("b", "`assert pct_change(100, 100) == 0`", "You tested a flat price. Both formulas give 0 there, so the bug passes."),
            opt("c", "`assert pct_change(100, 110) > 0`", "You tested only the sign. Both formulas give a positive change, so the bug passes."),
            opt("d", "`assert round(pct_change(100, 110), 1) == 0.1`", "You rounded before comparing. The bug gives 0.0909, which rounds to 0.1.")]),
    fb("A test catches a bug only where the two formulas differ.", "Work out what the buggy function returns for each test."),
    "The bug returns $\\tfrac{10}{110} \\approx 0.0909$ for 100 to 110. Only the exact check against 0.1 tells that from the right answer."))

# C8 complexity table
C.append(item("c-complexity-table", 3, ["at-complexity"], ["big-o"], 150, "How each operation grows",
    None, "Give the time each operation takes for $n$ items, in big-O form.",
    {"kind": "table", "columns": ["Operation", "Time"], "rows": [
        ["Binary search in a sorted list", {"edit": True, "answer": "O(log n)", "accept": ["log n", "O(logn)", "O(log(n))"], "placeholder": "e.g. O(n^2)",
                                            "wrong": [{"id": "scan", "text": "O(n)"}]}],
        ["Build a heap from a list with heapify", {"edit": True, "answer": "O(n)", "accept": ["n"], "placeholder": "e.g. O(n^2)",
                                                   "wrong": [{"id": "push-each", "text": "O(n log n)"}]}],
        ["Find a repeated id using a set", {"edit": True, "answer": "O(n)", "accept": ["n"], "placeholder": "e.g. O(n^2)",
                                            "wrong": [{"id": "pairs", "text": "O(n^2)"}]}],
        ["Sort with merge sort", {"edit": True, "answer": "O(n log n)", "accept": ["n log n", "O(nlogn)"], "placeholder": "e.g. O(n^2)",
                                  "wrong": [{"id": "quadratic-sort", "text": "O(n^2)"}]}]]},
    fb("Halving, a bottom-up build, one pass with a set, and a log of merges.", "Ask how much work each item causes, and how often the problem halves.",
       {"scan": "You scanned the list. Binary search halves the range each step, so it takes $\\log n$ steps.",
        "push-each": "You pushed items one at a time. heapify sifts down from the middle, which sums to $O(n)$.",
        "pairs": "You compared every pair. A set checks each id in $O(1)$ on average.",
        "quadratic-sort": "That is insertion sort's worst case. Merge sort has $\\log n$ levels of $O(n)$ merging."}),
    "Binary search halves the range, so $O(\\log n)$. heapify and a set scan are $O(n)$. "
    "Merge sort does $O(n)$ work on each of $\\log n$ levels."))

# C9 DP count
coins9, total9 = [2, 5, 10], 50
ways = [1] + [0] * total9
for cn in coins9:
    for v in range(cn, total9 + 1):
        ways[v] += ways[v - cn]
c9 = ways[total9]
ordw = [1] + [0] * total9
for v in range(1, total9 + 1):
    ordw[v] = sum(ordw[v - cn] for cn in coins9 if cn <= v)
C.append(item("c-coin-ways", 4, ["gd-dp"], ["coin-change"], 180, "Ways to pay 50p",
    "A machine pays 50p using 2p, 5p and 10p coins. Two payouts are the same when they use the same coins.",
    "How many different payouts are there?",
    num(c9, 0, [("ordered", ordw[total9], 0)]),
    fb("Count by coin, so order never matters.", "Fill a table of ways to make each amount, one coin type at a time.",
       {"ordered": "You counted sequences of coins, so 2p then 5p differs from 5p then 2p. Loop over coins outside the amounts."}),
    f"Loop over the coins outside and the amounts inside, adding `ways[v - c]`. Then each payout is counted once, in coin order. "
    f"The table ends at {c9}."))

# C10 two pointers in Python


def close_pairs(p, dd):
    cnt, j = 0, 0
    for i in range(len(p)):
        while p[i] - p[j] > dd:
            j += 1
        cnt += i - j
    return cnt


CP = [([1, 2, 4, 7, 8], 2), ([], 5), ([3, 3, 3, 3], 0), ([10, 20, 30], 5), ([0.5, 1.0, 1.4, 2.6, 2.7, 3.0], 1.0)]
cp_tests = py_tests([(None, "count_close_pairs(%r, %r)" % (p, dd), repr(close_pairs(p, dd)), "equal") for p, dd in CP])
big10 = close_pairs(list(range(200000)), 3)
cp_tests.append({"setup": "p = list(range(200000))", "call": "count_close_pairs(p, 3)", "expect": repr(big10), "compare": "equal"})
cp_sol = ("def count_close_pairs(p, d):\n    count, j = 0, 0\n    for i in range(len(p)):\n        while p[i] - p[j] > d:    # move the left end up\n"
          "            j += 1\n        count += i - j             # pairs (j..i-1, i)\n    return count\n")
C.append(item("c-close-pairs", 3, ["ds-pointers"], ["two-pointer-count"], 600, "Pairs within a gap",
    "Fill prices arrive sorted from low to high. A pair of fills is close when their prices differ by at most `d`.",
    "Write `count_close_pairs(p, d)`: the number of pairs `i < j` with `p[j] - p[i] <= d`, in $O(n)$ time.",
    {"kind": "code", "language": "python", "starter": "def count_close_pairs(p, d):\n    # p is sorted from low to high\n    ...\n",
     "solution": cp_sol, "examples": [{"call": cp_tests[0]["call"], "expect": cp_tests[0]["expect"]}], "tests": cp_tests,
     "how": "Check runs 6 hidden tests. Test 6 has 200,000 prices, so a loop over every pair runs out of time."},
    code_fb("One pass with a left end that only moves up.",
            {"test-3": "Test 3 has equal prices and `d = 0`. A gap of 0 counts as close.",
             "test-6": "Test 6 ran out of time. Keep a left pointer and move it up, instead of rescanning."}),
    "For each right end `i`, move `j` up until `p[i] - p[j] <= d`. Every index from `j` to `i - 1` then pairs with `i`. "
    "Each pointer moves at most $n$ times, so the count takes $O(n)$."))

# C11 the CRR pricer in C++
CRR_CPP = [(100, 100, 0.0, 0.2, 1.0, 1, True), (100, 110, 0.0, 0.2, 1.0, 1, False), (50, 55, 0.04, 0.3, 0.75, 3, True),
           (50, 55, 0.04, 0.3, 0.75, 3, False), (210, 200, 0.015, 0.18, 1.5, 120, True), (90, 100, 0.03, 0.4, 2.0, 1000, False)]
cpp_tests = []
for a in CRR_CPP:
    cpp_tests.append({"call": "crr_price", "args": list(a), "types": ["double", "double", "double", "double", "double", "int", "bool"],
                      "expect": r(crr(*a[:6], call=a[6]), 12), "compare": "isclose"})
cpp_starter = ("#include <algorithm>\n#include <cmath>\n#include <vector>\n\n"
               "double crr_price(double S, double K, double r, double sigma, double T, int n, bool call) {\n"
               "    // a European call (call is true) or put on an n-step CRR tree\n    return 0.0;\n}\n")
cpp_sol = ("#include <algorithm>\n#include <cmath>\n#include <vector>\n\n"
           "double crr_price(double S, double K, double r, double sigma, double T, int n, bool call) {\n"
           "    const double dt = T / n;\n    const double u = std::exp(sigma * std::sqrt(dt));\n    const double d = 1.0 / u;\n"
           "    const double q = (std::exp(r * dt) - d) / (u - d);\n    const double disc = std::exp(-r * dt);\n"
           "    std::vector<double> v(n + 1);\n    for (int j = 0; j <= n; ++j) {\n"
           "        const double s = S * std::pow(u, n - j) * std::pow(d, j);\n        v[j] = std::max(call ? s - K : K - s, 0.0);\n    }\n"
           "    for (int step = n; step > 0; --step)\n        for (int j = 0; j < step; ++j)\n"
           "            v[j] = disc * (q * v[j] + (1 - q) * v[j + 1]);   // reuse one vector\n    return v[0];\n}\n")
C.append(item("c-crr-cpp", 4, ["cx-pricers"], ["crr-pricer-cpp"], 900, "The binomial pricer in C++",
    "Use the Cox-Ross-Rubinstein tree: $\\Delta t = \\tfrac{T}{n}$, $u = e^{\\sigma\\sqrt{\\Delta t}}$, $d = \\tfrac1u$, "
    "$q = \\tfrac{e^{r\\Delta t} - d}{u - d}$, and a discount of $e^{-r\\Delta t}$ per step.",
    "Write `crr_price(S, K, r, sigma, T, n, call)`: a European call when `call` is true, else a put.",
    {"kind": "code", "language": "cpp", "starter": cpp_starter, "solution": cpp_sol,
     "examples": [cpp_tests[0]], "tests": cpp_tests,
     "how": "Check runs 6 hidden tests, calls and puts. Each price is accepted at a relative tolerance of 1e-9. Test 6 has 1,000 steps."},
    code_fb("Calls and puts match the tree to rounding.",
            {"test-2": "Test 2 is a put. Its payoff is $\\max(K - S, 0)$.",
             "test-6": "Test 6 has 1,000 steps. One `std::vector` reused in place keeps it fast."}),
    "The payoff fills one vector of $n + 1$ values. Each step back overwrites `v[j]` with the discounted $q$-average of `v[j]` and `v[j + 1]`. "
    "Only the payoff line differs between a call and a put."))

# C12 by value and by reference
C.append(item("c-by-reference", 3, ["cp-references"], ["value-or-reference"], 120, "Which change survives",
    "```cpp\n#include <iostream>\n#include <vector>\n\nvoid bump(std::vector<double> v) { v[0] += 1; }\n"
    "void bump_ref(std::vector<double>& v) { v[1] += 10; }\n\nint main() {\n    std::vector<double> p{100, 200};\n"
    "    bump(p);\n    bump_ref(p);\n    std::cout << p[0] + p[1] << \"\\n\";\n}\n```",
    "What does the program print?",
    num(310, 0, [("both-change", 311, 0), ("neither", 300, 0)]),
    fb("Only the reference parameter reaches the caller's vector.", "Ask which function gets a copy.",
       {"both-change": "You let `bump` change `p`. It receives a copy, so its change is lost.",
        "neither": "You treated `bump_ref` as a copy too. The `&` makes `v` another name for `p`."}),
    "`bump` adds 1 to a copy, which is then destroyed. `bump_ref` adds 10 to `p[1]` itself. So the sum is $100 + 210 = 310$."))

# C13 binary search steps
n13 = 4_000_000
c13 = math.ceil(math.log2(n13 + 1))
C.append(item("c-halvings", 2, ["at-search"], ["binary-search-steps"], 60, "Four million prices",
    "A sorted list holds 4,000,000 prices. Each comparison of a binary search halves the range left.",
    "At most how many comparisons does it need to find a price or rule it out?",
    num(c13, 0, [("log-ten", 6, 0)]),
    fb("$2^{22}$ is just over 4 million.", "Find the smallest $k$ with $2^k > 4{,}000{,}000$.",
       {"log-ten": "You counted digits, a base-10 log. Each step halves the range, so use base 2."}),
    f"$2^{{21}} = 2{{,}}097{{,}}152$ is too few and $2^{{22}} = 4{{,}}194{{,}}304$ is enough. So at most {c13} comparisons."))

# ======================================================================== Paper D: analysis, proof and 1.11 methods
# D1 epsilon and N
eps1 = 0.004
d1 = math.floor(1 / eps1 - 1) + 1          # smallest n with 1 / (n + 1) < eps
D.append(item("d-eps-n", 3, ["an-sequences"], ["epsilon-n"], 150, "How far out is close enough",
    "Let $a_n = \\dfrac{3n + 2}{n + 1}$, so $a_n \\to 3$.",
    "What is the smallest $N$ such that $|a_n - 3| < 0.004$ for every $n \\ge N$?",
    num(d1, 0, [("non-strict", d1 - 1, 0)]),
    fb("$|a_n - 3| = \\tfrac{1}{n + 1}$, which falls as $n$ grows.", "Simplify $a_n - 3$ first, then solve the inequality.",
       {"non-strict": f"At $n = {d1 - 1}$ the gap is exactly $\\tfrac{{1}}{{{d1}}} = 0.004$, which is not below 0.004."}),
    f"$a_n - 3 = \\tfrac{{3n + 2 - 3n - 3}}{{n + 1}} = -\\tfrac{{1}}{{n + 1}}$. We need $n + 1 > {1 / eps1:.0f}$, so $n \\ge {d1}$. "
    "The gap only shrinks after that."))

# D2 which series converges
D.append(item("d-which-converges", 2, ["an-series"], ["convergence-tests"], 90, "One series that converges",
    None, "Which series converges?",
    choice([opt("a", "$\\sum_{n \\ge 1} \\dfrac{4^n}{n!}$", correct=True),
            opt("b", "$\\sum_{n \\ge 1} \\dfrac{n + 1}{n^2 + 3}$", "You saw terms tending to 0. They behave like $\\tfrac1n$, whose sum diverges."),
            opt("c", "$\\sum_{n \\ge 1} \\dfrac{1}{\\sqrt{n}}$", "You took terms tending to 0 as enough. This is a $p$-series with $p = \\tfrac12 \\le 1$."),
            opt("d", "$\\sum_{n \\ge 1} \\dfrac{n}{5n - 1}$", "You saw terms below 1. They tend to $\\tfrac15$, not 0, so the sum diverges.")]),
    fb("The ratio test settles the factorial.", "Try the ratio test on the factorial, and compare the others with $\\tfrac1n$."),
    "For $\\tfrac{4^n}{n!}$ the ratio of terms is $\\tfrac{4}{n + 1} \\to 0 < 1$. The others diverge by comparison, by $p = \\tfrac12$, or by the term test."))

# D3 epsilon-delta for a quadratic
eps3, bound3 = 0.09, 6
d3 = min(1, eps3 / bound3)
D.append(item("d-delta-square", 3, ["an-continuity"], ["epsilon-delta"], 150, "A delta for a quadratic",
    "To show $x^2 + 3x$ is continuous at 1, write $|x^2 + 3x - 4| = |x - 1||x + 4|$. Taking $\\delta \\le 1$ keeps $|x + 4| \\le 6$.",
    "For $\\varepsilon = 0.09$, what is the largest $\\delta$ this argument allows?",
    num(r(d3), 0.00005, [("used-five", r(eps3 / 5), 0.00005)]),
    fb("$\\delta = \\min(1, \\tfrac{\\varepsilon}{6})$.", "Make $6\\delta \\le \\varepsilon$ and keep $\\delta \\le 1$.",
       {"used-five": "You used $|x + 4| = 5$, its value at 1 itself. Near 1 it can reach 6."}),
    f"With $|x + 4| \\le 6$, $|x^2 + 3x - 4| \\le 6\\delta$. So $\\delta = \\min(1, \\tfrac{{0.09}}{{6}}) = {d3:.3f}$ works."))

# D4 mean value theorem
d4 = math.sqrt(7)
D.append(item("d-mvt-cubic", 3, ["an-calculus"], ["mean-value"], 120, "Where the slope matches",
    "Let $f(x) = x^3 + 4x$ on $[1, 4]$.", "At which $c$ in $(1, 4)$ does $f'(c)$ equal the slope of the chord? Give 4 decimal places.",
    num(r(d4), 0.0005, [("chord-slope", 25, 0.0005)]),
    fb("The chord slope is 25.", "Find $\\tfrac{f(4) - f(1)}{3}$, then solve $3c^2 + 4 = $ that slope.",
       {"chord-slope": "You gave the slope itself. The question asks where $f'$ takes it."}),
    f"The chord slope is $\\tfrac{{80 - 5}}{{3}} = 25$. Then $3c^2 + 4 = 25$ gives $c = \\sqrt{{7}} \\approx {d4:.4f}$."))

# D5 rank-nullity proof
D.append(item("d-rank-nullity-proof", 4, ["lx-maps"], ["rank-nullity-proof"], 300, "Prove rank-nullity",
    "Let $T : V \\to W$ be linear, with $V$ finite-dimensional. We prove $\\dim V = \\dim \\ker T + \\dim \\operatorname{im} T$.",
    "Put the proof in order. Leave out the two flawed lines.",
    order([line("r1", "Choose a basis $\\mathbf{u}_1, \\dots, \\mathbf{u}_k$ of $\\ker T$."),
           line("r2", "Extend it to a basis $\\mathbf{u}_1, \\dots, \\mathbf{u}_k, \\mathbf{v}_1, \\dots, \\mathbf{v}_m$ of $V$, so $\\dim V = k + m$."),
           line("r3", "Each $T\\mathbf{u}_i = \\mathbf{0}$, so every $T\\mathbf{x}$ is a combination of the $T\\mathbf{v}_j$. They span $\\operatorname{im} T$."),
           line("r4", "If $\\sum c_j T\\mathbf{v}_j = \\mathbf{0}$, then $\\sum c_j \\mathbf{v}_j$ lies in $\\ker T$, so it equals some $\\sum a_i \\mathbf{u}_i$. Independence of the basis forces every $c_j = 0$."),
           line("r5", "So the $T\\mathbf{v}_j$ are a basis of $\\operatorname{im} T$, and $\\dim V = k + m = \\dim \\ker T + \\dim \\operatorname{im} T$."),
           line("x1", "The $T\\mathbf{v}_j$ are independent because the $\\mathbf{v}_j$ are.", "A linear map can send independent vectors to dependent ones. Independence needs the kernel step."),
           line("x2", "Take preimages of a basis of $\\operatorname{im} T$; they form a basis of $V$.", "The preimages miss the kernel, so they cannot span $V$ unless the kernel is zero.")],
          ["r1", "r2", "r3", "r4", "r5"], ["x1", "x2"], same=[["r3", "r4"]]),
    fb("Extend a kernel basis, then show the new images are a basis.", "Start from a basis of the kernel and extend it to all of $V$.",
       {"x1": "A linear map can send independent vectors to dependent ones. Independence needs the kernel step.",
        "x2": "The preimages miss the kernel, so they cannot span $V$ unless the kernel is zero.",
        "left-out": "A line that belongs is missing. The proof needs the basis, its extension, span, independence and the count."}),
    "The extended basis splits $V$ into the kernel part and $m$ further vectors. Their images span the image and are independent, by the kernel step. "
    "So the image has dimension $m$, and the dimensions add up."))

# D6 spectral theorem proof
D.append(item("d-spectral-proof", 5, ["lx-spectral"], ["spectral-proof"], 360, "Prove the spectral theorem",
    "Let $\\mathbf{A}$ be a real symmetric $n \\times n$ matrix. We prove by induction on $n$ that $\\mathbb{R}^n$ has an orthonormal basis of eigenvectors of $\\mathbf{A}$.",
    "Put the inductive step in order. Leave out the two flawed lines.",
    order([line("s1", "The characteristic polynomial has a root $\\lambda \\in \\mathbb{C}$, with $\\mathbf{A}\\mathbf{z} = \\lambda\\mathbf{z}$ for some $\\mathbf{z} \\ne \\mathbf{0}$."),
           line("s2", "As $\\mathbf{A}$ is real and symmetric, $\\bar{\\mathbf{z}}^T\\mathbf{A}\\mathbf{z}$ equals its own conjugate. So $\\lambda = \\tfrac{\\bar{\\mathbf{z}}^T\\mathbf{A}\\mathbf{z}}{\\bar{\\mathbf{z}}^T\\mathbf{z}}$ is real."),
           line("s3", "Take a real unit eigenvector $\\mathbf{q}$ for $\\lambda$, and let $U = \\{\\mathbf{x} : \\mathbf{q}^T\\mathbf{x} = 0\\}$."),
           line("s4", "For $\\mathbf{x} \\in U$, $\\mathbf{q}^T\\mathbf{A}\\mathbf{x} = (\\mathbf{A}\\mathbf{q})^T\\mathbf{x} = \\lambda\\mathbf{q}^T\\mathbf{x} = 0$. So $\\mathbf{A}$ maps $U$ into $U$."),
           line("s5", "$\\mathbf{A}$ restricted to $U$, of dimension $n - 1$, is still symmetric. By induction $U$ has an orthonormal basis of eigenvectors."),
           line("s6", "Adding $\\mathbf{q}$ gives an orthonormal basis of $\\mathbb{R}^n$ made of eigenvectors of $\\mathbf{A}$."),
           line("x1", "Every real matrix has a real eigenvalue, so take one.", "A rotation of the plane has no real eigenvalue. Symmetry is what makes $\\lambda$ real."),
           line("x2", "$\\mathbf{A}$ maps $U$ into $U$ because $U$ is orthogonal to $\\mathbf{q}$.", "Orthogonality alone proves nothing here. The step needs $\\mathbf{A}^T = \\mathbf{A}$ to move $\\mathbf{A}$ onto $\\mathbf{q}$.")],
          ["s1", "s2", "s3", "s4", "s5", "s6"], ["x1", "x2"]),
    fb("A real eigenvalue, an invariant complement, then induction.", "First show an eigenvalue is real, then find a subspace that $\\mathbf{A}$ keeps.",
       {"x1": "A rotation of the plane has no real eigenvalue. Symmetry is what makes $\\lambda$ real.",
        "x2": "Orthogonality alone proves nothing here. The step needs $\\mathbf{A}^T = \\mathbf{A}$ to move $\\mathbf{A}$ onto $\\mathbf{q}$.",
        "left-out": "A line that belongs is missing. Each of the six steps is used."}),
    "Symmetry makes the eigenvalue real and the complement of $\\mathbf{q}$ invariant. "
    "Induction then handles the complement, and $\\mathbf{q}$ completes the basis."))

# D7 angle in a function space
d7 = 0.25 / math.sqrt(1 / 3 * 1 / 5)
D.append(item("d-poly-angle", 3, ["lx-inner"], ["function-inner-product"], 150, "An angle between polynomials",
    "On polynomials, let $\\langle p, q \\rangle = \\int_0^1 p(x)q(x)\\,dx$.", "What is the cosine of the angle between $x$ and $x^2$? Give 4 decimal places.",
    num(r(d7), 0.0005, [("coefficient-dot", 0, 0.0005)]),
    fb("$\\langle x, x^2 \\rangle = \\tfrac14$, $\\|x\\|^2 = \\tfrac13$ and $\\|x^2\\|^2 = \\tfrac15$.", "Find $\\langle x, x^2 \\rangle$, $\\|x\\|$ and $\\|x^2\\|$ from the integral.",
       {"coefficient-dot": "You dotted the coefficient vectors. This inner product integrates the product over $[0, 1]$."}),
    f"$\\langle x, x^2 \\rangle = \\int_0^1 x^3\\,dx = \\tfrac14$. The norms are $\\tfrac{{1}}{{\\sqrt3}}$ and $\\tfrac{{1}}{{\\sqrt5}}$. So $\\cos\\theta = \\tfrac{{\\sqrt{{15}}}}{{4}} \\approx {d7:.4f}$."))

# D8 image of differentiation
D.append(item("d-diff-image", 2, ["lx-maps"], ["kernel-image"], 90, "What differentiation reaches",
    "Let $D$ send each polynomial of degree at most 4 to its derivative.", "What is the dimension of the image of $D$?",
    num(4, 0, [("whole-space", 5, 0), ("kernel", 1, 0)]),
    fb("The kernel is the constants, so one dimension is lost.", "Find the kernel, then use rank-nullity on a space of dimension 5.",
       {"whole-space": "You gave the dimension of the whole space. The constants all map to 0.",
        "kernel": "You gave the dimension of the kernel, the constants."}),
    "The space has basis $1, x, \\dots, x^4$, so dimension 5. The kernel is the constants, of dimension 1. So the image, all polynomials of degree at most 3, has dimension 4."))

# D9 compactness
D.append(item("d-compact-set", 3, ["an-metric"], ["compact-sets"], 120, "Which set is compact",
    None, "Which subset of $\\mathbb{R}$ is compact?",
    choice([opt("a", "$\\{0\\} \\cup \\{\\tfrac1n : n \\ge 1\\}$", correct=True),
            opt("b", "$\\{\\tfrac1n : n \\ge 1\\}$", "You saw a bounded set. Its points tend to 0, which it leaves out, so it is not closed."),
            opt("c", "$[0, \\infty)$", "You checked closed only. It is not bounded."),
            opt("d", "$[0, 1] \\cap \\mathbb{Q}$", "You saw a set inside $[0, 1]$. It is not closed: rationals converge to $\\tfrac{1}{\\sqrt2}$.")]),
    fb("In $\\mathbb{R}$, compact means closed and bounded.", "Check each set for both closed and bounded."),
    "By Heine-Borel, a subset of $\\mathbb{R}$ is compact when it is closed and bounded. The set with 0 added contains the limit of $\\tfrac1n$, so it is closed."))

# D10 a complex power
z10 = complex(-1, math.sqrt(3))
d10 = (z10 ** 6).real
D.append(item("d-complex-power", 2, ["cz-polar"], ["de-moivre"], 90, "A sixth power",
    "Let $z = -1 + i\\sqrt{3}$, which has modulus 2 and argument $\\tfrac{2\\pi}{3}$.", "$z^6$ is a real number. What is it?",
    num(round(d10), 0.001, [("mod-times", 12, 0.001), ("unit-power", 1, 0.001)]),
    fb("Raise the modulus to the 6th power and multiply the argument by 6.", "Use $z^6 = 2^6 e^{6i \\cdot 2\\pi/3}$.",
       {"mod-times": "You multiplied the modulus by 6. Raise it to the power 6.",
        "unit-power": "You kept only the angle. The modulus contributes $2^6$."}),
    "$z^6 = 2^6 e^{4\\pi i} = 64 \\times 1$. The angle $4\\pi$ is two full turns."))

# D11 residue
d11 = -math.pi * math.cos(1)
res_both = 2 * math.pi * (-math.cos(1) / 2 + math.cos(3) / 2)
D.append(item("d-residue", 3, ["cz-contour"], ["residue"], 150, "One pole inside",
    "Let $C$ be the circle $|z| = 2$, traversed anticlockwise.",
    "$\\oint_C \\dfrac{\\cos z}{z^2 - 4z + 3}\\,dz$ is $i$ times a real number. What is that number? Give 4 decimal places.",
    num(r(d11), 0.0005, [("both-poles", r(res_both), 0.0005), ("no-2pi", r(-math.cos(1) / 2), 0.0005)]),
    fb("Only $z = 1$ lies inside, with residue $-\\tfrac{\\cos 1}{2}$.", "Factor the bottom as $(z - 1)(z - 3)$, then keep only the pole inside $C$.",
       {"both-poles": "You added the residue at $z = 3$. That pole lies outside $|z| = 2$.",
        "no-2pi": "You gave the residue. The integral is $2\\pi i$ times it."}),
    f"The bottom is $(z - 1)(z - 3)$, and only $z = 1$ lies inside $C$. Its residue is $\\tfrac{{\\cos 1}}{{1 - 3}} = -\\tfrac{{\\cos 1}}{{2}}$. "
    f"So the integral is $-\\pi \\cos 1$ times $i$, about ${d11:.4f}i$."))

# D12 Green's theorem
d12 = 1 - 1 / 3
D.append(item("d-green-square", 3, ["vk-theorems"], ["greens-theorem"], 150, "Round the unit square",
    "Let $C$ be the boundary of $[0, 1]^2$, anticlockwise.", "What is $\\oint_C x^2 y\\,dx + (x + y^2)\\,dy$? Give 4 decimal places.",
    num(r(d12), 0.0005, [("sign", r(-d12), 0.0005), ("dropped-p", 1, 0.0005)]),
    fb("Green's theorem turns it into $\\iint (1 - x^2)\\,dA$.", "Compute $\\tfrac{\\partial Q}{\\partial x} - \\tfrac{\\partial P}{\\partial y}$ and integrate it over the square.",
       {"sign": "You took $P_y - Q_x$. Green's theorem uses $Q_x - P_y$.",
        "dropped-p": "You left out $\\tfrac{\\partial P}{\\partial y} = x^2$."}),
    f"$Q_x - P_y = 1 - x^2$. Its integral over the square is $1 - \\tfrac13 \\approx {d12:.4f}$."))

# D13 damped oscillation
d13 = math.exp(-2) * (math.cos(3) + (2 / 3) * math.sin(3))
D.append(item("d-damped-value", 4, ["de-second"], ["second-order-ode"], 210, "A damped return to rest",
    "$y'' + 4y' + 13y = 0$, with $y(0) = 1$ and $y'(0) = 0$.", "What is $y(1)$? Give 4 decimal places.",
    num(r(d13), 0.0005, [("no-sine", r(math.exp(-2) * math.cos(3)), 0.0005)]),
    fb("Roots $-2 \\pm 3i$.", "Solve $m^2 + 4m + 13 = 0$, write $y = e^{-2t}(A\\cos 3t + B\\sin 3t)$, then fit both conditions.",
       {"no-sine": "You fitted $y(0)$ but not $y'(0)$. That condition gives $B = \\tfrac23$."}),
    f"The roots are $-2 \\pm 3i$, so $y = e^{{-2t}}(A\\cos 3t + B\\sin 3t)$. $y(0) = 1$ gives $A = 1$, and $y'(0) = -2A + 3B = 0$ gives $B = \\tfrac23$. "
    f"So $y(1) = e^{{-2}}(\\cos 3 + \\tfrac23 \\sin 3) \\approx {d13:.4f}$."))

# D14 RK4 on a mean-reverting rate


def rk4(f, t0, y0, t1, n):
    h = (t1 - t0) / n
    t, y = t0, y0
    for _ in range(n):
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h * k1 / 2)
        k3 = f(t + h / 2, y + h * k2 / 2)
        k4 = f(t + h, y + h * k3)
        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h
    return y


kap, th, r0 = 1.5, 0.04, 0.01
closed14 = th + (r0 - th) * math.exp(-kap * 2)
rk_tests = [
    {"call": "rk4(lambda t, y: y, 0.0, 1.0, 1.0, 1)", "expect": repr(rk4(lambda t, y: y, 0.0, 1.0, 1.0, 1)), "compare": "isclose"},
    {"call": "rk4(lambda t, r: 1.5 * (0.04 - r), 0.0, 0.01, 2.0, 20)", "expect": repr(r(closed14, 10)), "compare": "isclose", "tol": {"abs": 5e-05}},
    {"call": "rk4(lambda t, y: y, 0.0, 1.0, 1.0, 10)", "expect": repr(r(math.e, 10)), "compare": "isclose", "tol": {"abs": 5e-05}},
    {"call": "rk4(lambda t, y: -2 * t * y, 0.0, 1.0, 1.5, 30)", "expect": repr(r(math.exp(-2.25), 10)), "compare": "isclose", "tol": {"abs": 5e-05}},
    {"call": "rk4(lambda t, y: t, 1.0, 0.0, 3.0, 2)", "expect": repr(r((9 - 1) / 2, 10)), "compare": "isclose"},
]
rk_sol = ("def rk4(f, t0, y0, t1, n):\n    h = (t1 - t0) / n\n    t, y = t0, y0\n    for _ in range(n):\n        k1 = f(t, y)\n"
          "        k2 = f(t + h / 2, y + h * k1 / 2)\n        k3 = f(t + h / 2, y + h * k2 / 2)\n        k4 = f(t + h, y + h * k3)\n"
          "        y += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6\n        t += h\n    return y\n")
D.append(item("d-rk4-rate", 4, ["de-numeric"], ["runge-kutta"], 900, "A short rate pulled to its mean",
    "A short rate follows $r' = 1.5(0.04 - r)$ with $r(0) = 0.01$. Its closed form is $r(t) = 0.04 - 0.03e^{-1.5t}$.",
    "Write `rk4(f, t0, y0, t1, n)`: the classical fourth-order Runge-Kutta value at `t1` after `n` equal steps, for $y' = f(t, y)$.",
    {"kind": "code", "language": "python", "starter": "def rk4(f, t0, y0, t1, n):\n    # f(t, y) is the slope; take n equal steps\n    ...\n",
     "solution": rk_sol, "examples": [{"call": rk_tests[0]["call"], "expect": rk_tests[0]["expect"], "compare": "isclose"}], "tests": rk_tests,
     "how": "Check runs 5 hidden tests. Tests 2 to 4 compare with the closed form to 4 decimal places (absolute 5e-05). Tests 1 and 5 check single steps at a relative tolerance of 1e-9."},
    code_fb("RK4 matches the closed form to four decimal places.",
            {"test-1": "Test 1 is one step of $y' = y$, which RK4 makes $1 + 1 + \\tfrac12 + \\tfrac16 + \\tfrac1{24}$. Check the weights 1, 2, 2, 1 over 6.",
             "test-2": f"Test 2 is the rate model. The closed form gives $r(2) \\approx {closed14:.4f}$; Euler's method misses by about 0.0003.",
             "test-5": "Test 5 starts at $t_0 = 1$. Advance $t$ from `t0`, not from 0."}),
    f"Each step averages four slopes with weights 1, 2, 2 and 1. With 20 steps the rate at $t = 2$ is ${closed14:.4f}$, as the closed form gives. "
    "Euler's method with the same steps misses by about 0.0003."))

# D15 Laplace transform with a shift
D.append(item("d-laplace-shift", 3, ["de-laplace"], ["laplace-shift"], 120, "A transform with a shift",
    None, "What is the Laplace transform of $e^{2t}\\sin 3t$, as a function of $s$?",
    expr("\\frac{3}{(s-2)^2+9}", ["3/((s-2)^2+9)", "\\frac{3}{s^2-4s+13}"],
         [("no-shift", "\\frac{3}{s^2+9}"), ("cosine", "\\frac{s-2}{(s-2)^2+9}")]),
    fb("Multiplying by $e^{2t}$ shifts $s$ to $s - 2$.", "Start from $\\mathcal{L}\\{\\sin 3t\\} = \\tfrac{3}{s^2 + 9}$, then shift.",
       {"no-shift": "You transformed $\\sin 3t$ only. The factor $e^{2t}$ replaces $s$ by $s - 2$.",
        "cosine": "You used the transform of $\\cos 3t$. Sine has 3 on top."}),
    "$\\mathcal{L}\\{\\sin 3t\\} = \\tfrac{3}{s^2 + 9}$. The factor $e^{2t}$ shifts it to $\\tfrac{3}{(s - 2)^2 + 9}$."))

# ======================================================================== the exam document
CHECKS = [
    ("finals-calculus", "MIT 18.01 final at 70%, and the 18.02 sets on partial derivatives and Lagrange multipliers",
     "A full 18.01 past final from MIT OpenCourseWare, timed and marked against its solutions. Then the 18.02 problem sets on partial derivatives and Lagrange multipliers, every part attempted."),
    ("final-linear-algebra", "MIT 18.06 final at 70%",
     "A full 18.06 past final from MIT OpenCourseWare, timed and marked against its solutions."),
    ("finals-probability", "Two Stat 110 past finals at 70%",
     "Two different Harvard Stat 110 past finals, each timed and marked against its solutions."),
    ("project-repository", "Your price-file project is in a Git repository with a passing test",
     "The script reads a CSV of daily prices, computes returns, annualised volatility and maximum drawdown, and plots them. It lives in a Git repository with at least one pytest test that passes."),
    ("problems-150", "150 algorithm problems solved, and a fresh medium in 30 minutes",
     "150 problems from one list, such as NeetCode 150, each accepted by the judge. Then a medium you have not seen, finished in 30 minutes more often than not."),
    ("cpp-pricer-timed", "Your C++ binomial pricer has tests and is timed against the Python one",
     "The pricer from paper C, built with tests in your own repository. Time it against your Python pricer at 1,000 steps and write down both times."),
    ("final-analysis", "An MIT 18.100A past final at 60%, and two proofs without notes",
     "A proof-based analysis final from MIT OpenCourseWare, timed, with every proof written out and marked against the solutions. "
     "Then prove rank-nullity and the spectral theorem for symmetric matrices on a blank page, without notes. Check each line against the course proofs."),
    ("final-odes", "MIT 18.03 final at 70%",
     "A full 18.03 past final from MIT OpenCourseWare, timed and marked against its solutions."),
    ("ols-summary-explained", "Your NumPy regression matches statsmodels, and you can explain every number in its summary",
     "Fit one regression on real returns in NumPy and with statsmodels. Write one line on each number in the summary. "
     "Cover the coefficients, standard errors, t, P>|t|, the interval, R² and adjusted R². Then the F statistic, log-likelihood, AIC and BIC."),
]


def minutes(items, extra=0):
    return int(math.ceil(1.25 * (sum(it["pace"] for it in items) + extra) / 60 / 5) * 5)


# at-least-one and bayes-in-a-minute stay out of the draws: their pool items are twins of b-forty-tests and b-fraud-flag
PROB_TAGS = ["dice-ev", "every-coupon", "hats"]
PROB_TAGS_2 = ["indicator-tricks", "given-the-total", "urns"]
MM_TAGS = ["quote-centre", "informed-loss", "position-limit", "skew"]
DRAW_B = [{"from": "bank/probability", "tags": PROB_TAGS, "difficulty": [3, 4], "n": 3},
          {"from": "bank/probability", "tags": PROB_TAGS_2, "difficulty": [3, 4], "n": 2},
          {"from": "bank/market-making", "tags": MM_TAGS, "difficulty": [3, 4], "n": 2}]
DRAW_C = [{"from": "drills/oa", "difficulty": [3, 4], "n": 1}, {"from": "drills/ci-cpp", "difficulty": [3, 4], "n": 1}]
doc = {
    "id": "stage-1", "stage": 1, "name": "Stage 1 exit test",
    "description": "The exit test for Foundations, in four papers and nine checks. "
                   "The papers cover calculus and linear algebra, probability, statistics and finance, programming, and analysis with the 1.11 methods. "
                   "The checks cover the past finals, your project, the problem count and a regression you can explain.",
    "parts": [
        {"kind": "paper", "id": "calc-linalg", "name": "Paper A: calculus and linear algebra", "minutes": minutes(A), "pass": 0.7, "items": A},
        {"kind": "paper", "id": "prob-stats-finance", "name": "Paper B: probability, statistics and finance", "minutes": minutes(B, 7 * 180), "pass": 0.7,
         "items": B, "draw": DRAW_B},
        {"kind": "paper", "id": "programming", "name": "Paper C: programming in Python and C++", "minutes": minutes(C, 1800 + 1500), "pass": 0.7,
         "items": C, "draw": DRAW_C},
        {"kind": "paper", "id": "analysis-methods", "name": "Paper D: analysis, proof and the 1.11 methods", "minutes": minutes(D), "pass": 0.7, "items": D},
    ] + [{"kind": "check", "id": i, "name": n, "detail": dt} for i, n, dt in CHECKS],
}

if __name__ == '__main__':
    with open(OUT, 'w', encoding='utf8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for p in doc["parts"]:
        if p["kind"] == "paper":
            ds = [it["difficulty"] for it in p["items"]]
            print(p["id"], len(p["items"]), "authored +", sum(d_["n"] for d_ in p.get("draw", [])), "drawn,",
                  p["minutes"], "min, ramp", [ds.count(k) for k in (2, 3, 4, 5)])
    print("wrote", os.path.relpath(OUT))
