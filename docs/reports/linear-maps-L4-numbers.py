"""Number recompute for linear-maps level 4 (Operators). Pure standard library.

Every stated number is computed here a second way (exact fractions, complex arithmetic,
or a loop) and checked at the JSON path where the level states it. Run from anywhere:
    python3 docs/reports/linear-maps-L4-numbers.py
"""
import sys, os, math, cmath
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("linear-maps", 4)

# ---------- small exact linear algebra ----------
def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A, v):
    return [sum(A[i][k] * v[k] for k in range(len(v))) for i in range(len(A))]
def eye(n, c=1):
    return [[F(c) if i == j else F(0) for j in range(n)] for i in range(n)]
def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def mpow(A, k):
    R = eye(len(A))
    for _ in range(k):
        R = mm(R, A)
    return R
def rank(A):
    M = [[F(x) for x in r] for r in A]
    r, rows, cols = 0, len(M), len(M[0])
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(rows):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def dims(A, lam):
    n = len(A)
    B = sub([[F(x) for x in r] for r in A], eye(n, lam))
    return [n - rank(mpow(B, k)) for k in range(1, n + 1)]
def blocks(d):
    d = [0] + d
    at = [d[k] - d[k - 1] for k in range(1, len(d))] + [0]
    out = []
    for k in range(len(at) - 1, 0, -1):
        out += [k] * (at[k - 1] - at[k])
    return out
def dot(u, v):
    return sum(a * b for a, b in zip(u, v))
def quad_roots(b, c):            # roots of z^2 + b z + c
    disc = cmath.sqrt(b * b - 4 * c)
    return ((-b + disc) / 2, (-b - disc) / 2)

# ================= l15 =================
A = [[2, 1], [1, 2]]
v = [1, 0]
Av, A2v = mv(A, v), mv(A, mv(A, v))
assert Av == [2, 1] and A2v == [5, 4]
lv.expect("l15", "screens[0].widget.answer", "(5, 4)")
lv.expect("l15", "screens[0].prose", "(2, 1)")
lv.expect("l15", "screens[0].feedback.correct", "(5, 4)")
# a, b with A^2 v = a A v + b v: second entries give a, first give 2a + b
a = F(A2v[1], Av[1]); b = A2v[0] - 2 * a
assert (a, b) == (4, -3)
assert [a * x + b * y for x, y in zip(Av, v)] == A2v        # second check
lv.expect("l15", "screens[1].widget.answer", "(4, -3)")
lv.expect("l15", "screens[1].feedback.correct", "(5, 4)")
lv.expect("l15", "screens[1].explain.text", -3)
# p(z) = z^2 - 4z + 3 = (z - 1)(z - 3)
assert quad_roots(-4, 3) == (3, 1)
lv.expect("l15", "screens[2].prose", "z^2 - 4z + 3")
w = [x - y for x, y in zip(Av, v)]
assert w == [1, 1] and mv(sub(A, eye(2, 3)), w) == [0, 0]
lv.expect("l15", "screens[2].widget.answer", "(1, 1)")
Aw = mv(A, w)
assert Aw == [3, 3]
lv.expect("l15", "screens[3].widget.answer", 3)
lv.expect("l15", "screens[3].feedback.correct", "(3, 3)")
lv.expect("l15", "screens[3].widget.wrong[1].value", 6)      # adding the entries of (3, 3)
R = [[0, -1], [1, 0]]
Rv, R2v = mv(R, v), mv(R, mv(R, v))
assert Rv == [0, 1] and R2v == [-1, 0]
lv.expect("l15", "screens[4].prose", "(-1, 0)")
lv.expect("l15", "screens[4].widget.answer", "z^2+1")
# (R + iI) v = (i, 1), and R (i, 1) = i (i, 1)
Ri = [[1j, -1], [1, 1j]]
wc = [Ri[0][0] * 1 + Ri[0][1] * 0, Ri[1][0] * 1 + Ri[1][1] * 0]
assert wc == [1j, 1]
Rw = [R[0][0] * wc[0] + R[0][1] * wc[1], R[1][0] * wc[0] + R[1][1] * wc[1]]
assert Rw == [-1, 1j] and Rw == [1j * x for x in wc]
lv.expect("l15", "screens[5].widget.answer", "(i, 1)")
lv.expect("l15", "screens[5].explain.text", "(-1, i)")
# AR(2): companion [[1, -0.5], [1, 0]], char poly z^2 - z + 0.5
lam1, lam2 = quad_roots(-1, 0.5)
assert abs(lam1 - (0.5 + 0.5j)) < 1e-12 and abs(lam2 - (0.5 - 0.5j)) < 1e-12
mod = abs(lam1); ang = cmath.phase(lam1)
assert abs(mod - math.sqrt(0.5)) < 1e-12 and abs(ang - math.pi / 4) < 1e-12
period = 2 * math.pi / ang
assert abs(period - 8) < 1e-9
lv.expect("l15", "screens[10].widget.answer", "0.5+0.5i")
lv.expect("l15", "screens[10].explain.text", round(mod, 4))
lv.expect("l15", "screens[10].feedback.byKey.real", -1)
# impulse response x_t = x_{t-1} - 0.5 x_{t-2}, x_0 = 1, x_{-1} = 0
xs, prev = [1.0], 0.0
for t in range(1, 17):
    xs.append(xs[-1] - 0.5 * (xs[-2] if t > 1 else prev))
zeros = [t for t, x in enumerate(xs) if x == 0]
assert zeros == [3, 7, 11, 15]
for t in zeros:
    lv.expect("l15", "screens[11].prose", t)
lv.expect("l15", "screens[11].prose", 8)
c8 = xs[8] / xs[0]
assert c8 == 0.0625 and abs(mod ** 8 - c8) < 1e-12 and 0.5 ** 4 == c8
lv.expect("l15", "screens[11].widget.answer", 0.0625)
lv.expect("l15", "screens[11].widget.wrong[0].value", round(mod, 4))
lv.expect("l15", "screens[11].widget.wrong[1].value", round(0.5 ** 8, 4))
lv.expect("l15", "screens[11].widget.wrong[2].value", abs(xs[6]))
assert xs[6] == -0.125
lv.expect("l15", "screens[11].canvas.params.series[0].values", 0.00390625)
assert lv.text("l15", "screens[11].canvas.params.series[0].values").count("\n") + 1 == len(xs)
# annihilating polynomials (code tests), recomputed by the same Krylov rule in exact arithmetic
def annih(Am, vv):
    K = [[F(x) for x in vv]]
    while True:
        nxt = mv(Am, K[-1])
        M = [list(col) for col in zip(*(K + [nxt]))]
        if rank(M) == len(K):
            break
        K.append(nxt)
    # solve sum c_j K_j = nxt by least squares = exact solve on independent columns
    n = len(K)
    G = [[dot(K[i], K[j]) for j in range(n)] for i in range(n)]
    h = [dot(K[i], nxt) for i in range(n)]
    # Gaussian elimination
    Mx = [G[i] + [h[i]] for i in range(n)]
    for c in range(n):
        p = next(i for i in range(c, n) if Mx[i][c] != 0)
        Mx[c], Mx[p] = Mx[p], Mx[c]
        Mx[c] = [x / Mx[c][c] for x in Mx[c]]
        for i in range(n):
            if i != c:
                Mx[i] = [x - Mx[i][c] * y for x, y in zip(Mx[i], Mx[c])]
    cs = [Mx[i][n] for i in range(n)]
    return [1] + [int(-x) for x in cs[::-1]]
assert annih(A, [1, 0]) == [1, -4, 3]
assert annih(A, [1, 1]) == [1, -3]
assert annih(R, [1, 0]) == [1, 0, 1]
assert annih([[1, 0, 0], [0, 2, 0], [0, 0, 3]], [1, 1, 1]) == [1, -6, 11, -6]
lv.expect("l15", "screens[9].widget.tests[0].expect", "[1, -4, 3]")
lv.expect("l15", "screens[9].widget.tests[1].expect", "[1, -3]")
lv.expect("l15", "screens[9].widget.tests[2].expect", "[1, 0, 1]")
lv.expect("l15", "screens[9].widget.tests[3].expect", "[1, -6, 11, -6]")
lv.expect("l15", "screens[9].canvas", 5)
# quiz
lv.expect("l15", "quiz[0].prose", "(-1, i)")
lv.expect("l15", "quiz[0].widget.answer", "i")
lv.expect("l15", "quiz[4].prose", "(3, 3)")
lv.expect("l15", "quiz[4].widget.answer", 1)
lv.expect("l15", "quiz[2].widget.options[1].why", "(1, 1)")

# ================= l16 =================
A16 = [[2, 2], [2, -1]]
assert mv(A16, [2, 1]) == [6, 3] == [3 * 2, 3 * 1]
assert mv(A16, [1, -2]) == [-2, 4] == [-2 * 1, -2 * -2]
assert dot([2, 1], [1, -2]) == 0
lv.expect("l16", "screens[0].prose", "(6, 3)")
lv.expect("l16", "screens[0].prose", "(-2, 4)")
lv.expect("l16", "screens[0].widget.answer", 0)
lv.expect("l16", "screens[0].widget.wrong[0].value", 2 * 1 - 1 * (-2))
lv.expect("l16", "screens[0].widget.wrong[1].value", 2 * (-2) - 1 * 1)
N = [[2, 1], [0, 3]]
assert mv(N, [1, 0]) == [2, 0] and mv(N, [1, 1]) == [3, 3]
assert dot([1, 0], [1, 1]) == 1
ang = math.degrees(math.acos(1 / math.sqrt(2)))
assert abs(ang - 45) < 1e-9
lv.expect("l16", "screens[1].widget.answer", 1)
lv.expect("l16", "screens[1].prose", "(3, 3)")
lv.expect("l16", "screens[1].widget.wrong[1].value", dot([1, 1], [1, 1]))   # 2 = |(1, 1)|^2, the slip its why names
# eigenvalues of A16: lambda^2 - lambda - 6
tr, det = A16[0][0] + A16[1][1], A16[0][0] * A16[1][1] - A16[0][1] * A16[1][0]
assert (tr, det) == (1, -6)
r1, r2 = quad_roots(-tr, det)
assert (r1, r2) == (3, -2)
lv.expect("l16", "screens[3].widget.answer", -2)
lv.expect("l16", "screens[3].widget.wrong[1].value", -3)
lv.expect("l16", "screens[3].feedback.byKey.sign", -4)       # 4 - 2 - 6
assert 2 ** 2 - 2 - 6 == -4 and (-2) ** 2 + 2 - 6 == 0
# Hermitian [[2, i], [-i, 2]]
assert 1j * (-1j) == 1
h1, h2 = quad_roots(-4, 4 - 1)
assert (h1, h2) == (3, 1)
lv.expect("l16", "screens[4].widget.answer", 1)
lv.expect("l16", "screens[4].widget.wrong[1].value", 3)
# weighted inner product 2 x1 y1 + x2 y2
W = [[2, 0], [0, 1]]
ipW = lambda x, y: dot(x, mv(W, y))
T = [[0, 1], [1, 0]]
e1, e2 = [1, 0], [0, 1]
assert ipW(mv(T, e1), e2) == 1 and ipW(e1, mv(T, e2)) == 2
Winv = [[F(1, 2), 0], [0, 1]]
adj = mm(Winv, mm([list(r) for r in zip(*T)], W))
assert adj == [[0, F(1, 2)], [2, 0]]
lv.expect("l16", "screens[5].prose", 2)
lv.expect("l16", "screens[5].explain.text", 0.5)
lv.expect("l16", "quiz[0].widget.answer", 0.5)
lv.expect("l16", "quiz[0].feedback.correct", 0.5)
# T has eigenvalues 1 and -1
assert quad_roots(0, -1) == (1, -1)
lv.expect("l16", "screens[5].widget.options[2].text", -1)
# transfer: Sigma = [[3, 1], [1, 3]]
Sig = [[3, 1], [1, 3]]
assert dot([1, 1], mv(Sig, [1, -1])) == 0
assert mv(Sig, [1, -1]) == [2, -2]
assert dot([1, 1], mv(Sig, [1, 1])) == 8 and dot([1, -1], mv(Sig, [1, -1])) == 4
assert quad_roots(-6, 8) == (4, 2)
lv.expect("l16", "screens[11].widget.answer", 0)
lv.expect("l16", "screens[11].widget.wrong[0].value", 8)
lv.expect("l16", "screens[11].widget.wrong[1].value", 4)
lv.expect("l16", "screens[11].prose", 4)
lv.expect("l16", "screens[11].prose", 2)
lv.expect("l16", "screens[11].explain.text", -2)
# quiz Hermitian [[1, 2i], [-2i, 1]]
assert (2j) * (-2j) == 4
assert quad_roots(-2, 1 - 4) == (3, -1)
lv.expect("l16", "quiz[1].widget.answer", 3)
lv.expect("l16", "quiz[1].widget.wrong[0].value", -1)
# quiz perp: (1, 2) and (2, -1)
assert dot([1, 2], [2, -1]) == 0 and dot([1, 2], [2, 1]) == 4 and dot([1, 2], [1, -2]) == -3
lv.expect("l16", "quiz[2].widget.options[1].why", 4)
lv.expect("l16", "quiz[2].widget.options[2].why", -3)

# ================= l17 =================
A17 = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
assert mv(A17, [1, 1, 1]) == [4, 4, 4]
lv.expect("l17", "screens[0].widget.answer", 4)
lv.expect("l17", "screens[0].widget.wrong[1].value", sum(sum(r) for r in A17))   # 12, all nine entries
u = [1, 2, -3]
assert mv(A17, u) == u and sum(mv(A17, u)) == 0
lv.expect("l17", "screens[1].widget.rows[2][1].answer", -3)
lv.expect("l17", "screens[1].widget.rows[2][1].wrong[0].value", 2 * -3)   # only the diagonal term of row 3 kept
assert 1 + 2 + 2 * (-3) == -3
lv.expect("l17", "screens[1].feedback.byKey.nine", -6)
# eigenvalues 4, 1, 1: trace 6, and A - I has rank 1
assert sum(A17[i][i] for i in range(3)) == 6 == 4 + 1 + 1
assert rank(sub([[F(x) for x in r] for r in A17], eye(3))) == 1
assert dot([1, -1, 0], [1, 0, -1]) == 1
lv.expect("l17", "screens[2].widget.answer", 1)
cos60 = 1 / (math.sqrt(2) * math.sqrt(2))
assert abs(math.degrees(math.acos(cos60)) - 60) < 1e-9
lv.expect("l17", "screens[2].explain.text", "60")
# Gram-Schmidt inside U
q2 = [1, -1, 0]
coef = F(dot([1, 0, -1], q2), dot(q2, q2))
f = [x - coef * y for x, y in zip([1, 0, -1], q2)]
assert f == [F(1, 2), F(1, 2), -1] and sum(f) == 0
lv.expect("l17", "screens[3].widget.answer", "(0.5, 0.5, -1)")
assert [2 * x for x in f] == [1, 1, -2]
lv.expect("l17", "screens[3].explain.text", "(1, 1, -2)")
# Q^T A Q = diag(4, 1, 1), in floating point and exactly on the unnormalised columns
cols = [[1, 1, 1], [1, -1, 0], [1, 1, -2]]
for i in range(3):
    for j in range(3):
        val = dot(cols[i], mv(A17, cols[j]))
        if i != j:
            assert val == 0 and dot(cols[i], cols[j]) == 0
        else:
            assert F(val, dot(cols[i], cols[i])) == [4, 1, 1][i]
lv.expect("l17", "screens[4].widget.rows[0][1].answer", 4)
lv.expect("l17", "screens[4].widget.rows[1][1].answer", 1)
lv.expect("l17", "screens[4].widget.rows[2][1].answer", 1)
# trap: inner product of the two unit vectors
assert F(dot([1, -1, 0], [1, 0, -1]), 2) == F(1, 2)
lv.expect("l17", "screens[5].explain.text", "\\tfrac12")
# flaw: N(0, 1) = (1, 3)
assert mv(N, [0, 1]) == [1, 3] and dot(mv(N, [0, 1]), [1, 0]) == 1
lv.expect("l17", "screens[9].feedback.correct", "(1, 3)")
lv.expect("l17", "screens[9].explain.text", 1)
# code tests: eigenvalues ascending
lv.expect("l17", "screens[10].widget.tests[0].expect", "[1, 1, 4]")
lv.expect("l17", "screens[10].widget.tests[3].expect", "[0.5, 0.5, 2.0]")
# equicorrelated 3x3: eigenvalues 1 + 2 rho and 1 - rho twice
def equi(r):
    Cm = [[F(1) if i == j else F(r) for j in range(3)] for i in range(3)]
    lam_m = F(sum(mv(Cm, [1, 1, 1])), 3)          # (1,1,1) is an eigenvector
    lam_s = F(mv(Cm, [1, -1, 0])[0], 1)            # (1,-1,0) is an eigenvector
    assert mv(Cm, [1, -1, 0]) == [lam_s, -lam_s, 0]
    return lam_m, lam_s, Cm
for r in [F(1, 2), F(-1, 2), F(-3, 5)]:
    lm, ls, Cm = equi(r)
    assert lm == 1 + 2 * r and ls == 1 - r
lm, ls, Cm = equi(F(1, 2))
assert (lm, ls) == (2, F(1, 2))
var_ew = dot([F(1, 3)] * 3, mv(Cm, [F(1, 3)] * 3))
assert var_ew == F(2, 3) == lm * F(1, 3) == F(3 + 6 * F(1, 2), 9)
lv.expect("l17", "screens[11].widget.answer", round(float(var_ew), 4))
lv.expect("l17", "screens[11].explain.text", round(float(var_ew), 4))
lv.expect("l17", "screens[11].widget.wrong[0].value", 2)
lv.expect("l17", "screens[11].widget.wrong[1].value", round(float(ls * F(1, 3)), 4))
lv.expect("l17", "screens[11].widget.wrong[2].value", round(3 / 9, 4))       # the three diagonal 1s only
lv.expect("l17", "screens[11].feedback.byKey.ninth", "\\tfrac39")
lv.expect("l17", "screens[11].prose", 0.5)
lm2, ls2, _ = equi(F(-1, 2)); assert lm2 == 0 and ls2 == F(3, 2)
lm3, ls3, _ = equi(F(-3, 5)); assert lm3 == F(-1, 5) and ls3 == F(8, 5)
lv.expect("l17", "quiz[2].prose", -0.2)
lv.expect("l17", "quiz[2].prose", 1.6)
lv.expect("l17", "quiz[3].widget.answer", 0)
lv.expect("l17", "quiz[3].widget.wrong[0].value", float(ls2 * F(1, 3)))
lv.expect("l17", "quiz[3].widget.wrong[1].value", float(ls2))
lv.expect("l17", "quiz[4].widget.options[1].why", "(9, 1, 4)")

# ================= l18 =================
A2 = [[4, 1], [0, 4]]
Nn = sub([[F(x) for x in r] for r in A2], eye(2, 4))
assert mv(Nn, [0, 1]) == [1, 0] and mpow(Nn, 2) == [[0, 0], [0, 0]]
assert mv(A2, [0, 1]) == [1, 4] and mv(A2, [1, 1]) == [5, 4]
lv.expect("l18", "screens[0].widget.options[1].why", "(1, 4)")
lv.expect("l18", "screens[0].widget.options[2].why", "(5, 4)")
lv.expect("l18", "screens[1].widget.answer", "(1, 0)")
lv.expect("l18", "screens[2].widget.answer", "(0, 0)")
A3 = [[2, 1, -1], [0, 2, 1], [0, 0, 3]]
assert dims(A3, 2) == [1, 2, 2] and dims(A3, 3) == [1, 1, 1]
lv.expect("l18", "screens[4].widget.rows[0][1].answer", 1)
lv.expect("l18", "screens[4].widget.rows[1][1].answer", 2)
lv.expect("l18", "screens[4].widget.rows[2][1].answer", 2)
lv.expect("l18", "screens[4].widget.rows[3][1].answer", 1)
Sh = [[1, 1, 1], [0, 1, 2], [0, 0, 1]]        # p(x) -> p(x + 1) on (1, x, x^2)
# N = S - I on polynomials: N1 = 0, Nx = 1, Nx^2 = 2x + 1, N(2x + 1) = 2
Ns = sub([[F(x) for x in r] for r in Sh], eye(3))
assert mv(Ns, [0, 0, 1]) == [1, 2, 0] and mv(Ns, [1, 2, 0]) == [2, 0, 0] and mv(Ns, [2, 0, 0]) == [0, 0, 0]
assert dims(Sh, 1) == [1, 2, 3]
lv.expect("l18", "screens[5].canvas.params.matrices[0].rows", 2)
lv.expect("l18", "screens[5].widget.rows[2][1].answer", 3)
assert dims([[2, 0], [0, 2]], 2) == [2, 2]
M = [[2, 1, 0, 0], [0, 2, 1, -1], [0, 0, 2, 0], [0, 0, 0, 2]]
assert dims(M, 2) == [2, 3, 4, 4]
lv.expect("l18", "screens[9].widget.tests[0].expect", "[1, 2, 2]")
lv.expect("l18", "screens[9].widget.tests[1].expect", "[1, 1, 1]")
lv.expect("l18", "screens[9].widget.tests[2].expect", "[1, 2, 3]")
lv.expect("l18", "screens[9].widget.tests[3].expect", "[2, 2]")
lv.expect("l18", "screens[9].widget.tests[4].expect", "[2, 3, 4, 4]")
# hump: top-right entry of [[0.9, 1], [0, 0.9]]^t equals t * 0.9^(t-1)
A9 = [[F(9, 10), 1], [0, F(9, 10)]]
hump = [mpow(A9, t)[0][1] for t in range(21)]
for t in range(1, 21):
    assert hump[t] == t * F(9, 10) ** (t - 1)
vals = [round(float(x), 4) for x in hump]
assert vals[1] == 1 and vals[5] == 3.2805 and vals[20] == 2.7017
assert hump[9] == hump[10] and max(hump) == hump[9] and round(float(hump[9]), 4) == 3.8742
lv.expect("l18", "screens[10].prose", 3.2805)
lv.expect("l18", "screens[10].widget.answer", 3.8742)
lv.expect("l18", "screens[10].widget.wrong[1].value", 3.2805)
lv.expect("l18", "screens[10].widget.wrong[2].value", 2.7017)
lv.expect("l18", "screens[10].explain.text", 3.8742)
lv.expect("l18", "screens[10].explain.text", 2.7017)
for t in (1, 5, 9, 10, 20):
    lv.expect("l18", "screens[10].canvas.params.series[0].values", vals[t])
lv.expect("l18", "screens[10].canvas.params.series[1].values", round(0.9 ** 20, 4))
# quiz
Nil = [[0, 1, 0], [0, 0, 1], [0, 0, 0]]
assert dims(Nil, 0) == [1, 2, 3]
lv.expect("l18", "quiz[1].widget.answer", 3)
lv.expect("l18", "quiz[2].widget.answer", dims(A3, 2)[-1])

# ================= l19 =================
K = [[2, 1, -1, 1], [0, 2, 0, 1], [0, 0, 2, 1], [0, 0, 0, 2]]
T3 = [[2, 1, -1, 1], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]]
assert dims(M, 2)[:3] == [2, 3, 4] and dims(K, 2)[:3] == [2, 4, 4] and dims(T3, 2)[:2] == [3, 4]
# second check: each is P J P^-1 with P upper bidiagonal ones (det 1)
P = [[F(1) if j in (i, i + 1) else F(0) for j in range(4)] for i in range(4)]
Pinv = [[F((-1) ** (j - i)) if j >= i else F(0) for j in range(4)] for i in range(4)]
assert mm(P, Pinv) == eye(4)
def J(bl):
    n = sum(bl); Jm = [[F(0)] * n for _ in range(n)]; i = 0
    for b in bl:
        for k in range(b):
            Jm[i + k][i + k] = F(2)
            if k < b - 1:
                Jm[i + k][i + k + 1] = F(1)
        i += b
    return Jm
assert mm(mm(P, J([3, 1])), Pinv) == M
assert mm(mm(P, J([2, 2])), Pinv) == K
assert mm(mm(P, J([2, 1, 1])), Pinv) == T3
lv.expect("l19", "screens[0].widget.rows[1][1].answer", 3)
lv.expect("l19", "screens[0].widget.rows[1][2].answer", 4)
lv.expect("l19", "screens[0].widget.rows[2][1].answer", 4)
lv.expect("l19", "screens[0].widget.rows[2][2].answer", 4)
assert blocks(dims(M, 2)) == [3, 1] and blocks(dims(K, 2)) == [2, 2] and blocks(dims(T3, 2)) == [2, 1, 1]
lv.expect("l19", "screens[3].widget.rows[0][1].answer", 2)
lv.expect("l19", "screens[3].widget.rows[1][1].answer", 1)
lv.expect("l19", "screens[3].widget.rows[2][1].answer", 1)
for bl, cap in [([3, 1], "2, 3, 4"), ([2, 2], "2, 4, 4"), ([2, 1, 1], "3, 4, 4"), ([1, 1, 1, 1], "4, 4, 4")]:
    d = [4 - rank(mpow(sub(J(bl), eye(4, 2)), k)) for k in (1, 2, 3)]
    assert ", ".join(map(str, d)) == cap
    lv.expect("l19", "screens[1].canvas.controls[0].frames", cap)
# shift in chain basis (2, 2x + 1, x^2) is J_3(1)
B = [[2, 1, 0], [0, 2, 0], [0, 0, 1]]           # columns are the chain basis in (1, x, x^2)
Binv = [[F(1, 2), F(-1, 4), 0], [0, F(1, 2), 0], [0, 0, 1]]
assert mm(B, Binv) == eye(3)
assert mm(mm(Binv, Sh), B) == [[1, 1, 0], [0, 1, 1], [0, 0, 1]]
for (r, c), val in {(0, 1): 1, (0, 2): 1, (1, 3): 1, (1, 2): 1, (2, 3): 1, (0, 3): 0}.items():
    lv.expect("l19", f"screens[5].widget.rows[{r}][{c}].answer", val)
# epsilon matrix
eps = 1e-10
e_pos = math.sqrt(eps)
assert abs(e_pos - 1e-5) < 1e-18
lv.expect("l19", "screens[10].widget.answer", 0.00001)
lv.expect("l19", "screens[10].explain.text", 0.00001)
lv.expect("l19", "screens[10].widget.wrong[0].value", eps)
assert blocks(dims(A3, 2)) == [2] and blocks(dims(Sh, 1)) == [3] and blocks(dims([[2, 0], [0, 2]], 2)) == [1, 1]
lv.expect("l19", "screens[9].widget.tests[0].expect", "[3, 1]")
lv.expect("l19", "screens[9].widget.tests[1].expect", "[2, 2]")
lv.expect("l19", "screens[9].widget.tests[2].expect", "[2, 1, 1]")
lv.expect("l19", "screens[9].widget.tests[3].expect", "[2]")
lv.expect("l19", "screens[9].widget.tests[4].expect", "[3]")
lv.expect("l19", "screens[9].widget.tests[5].expect", "[1, 1]")
lv.expect("l19", "screens[9].widget.tests[6].expect", "[2]")
# quiz: J_3(2) + J_1(2) + J_2(5)
alg2, geo = 3 + 1, 3
lv.expect("l19", "quiz[1].widget.answer", alg2)
lv.expect("l19", "quiz[2].widget.answer", geo)
d6 = [3, 5, 6, 6, 6, 6]
assert d6[1] - d6[0] == 2 and blocks(d6) == [3, 2, 1]
lv.expect("l19", "quiz[4].widget.answer", 2)

# ================= review-4 =================
Bm = [[3, 1], [0, 2]]
bv, b2v = mv(Bm, [0, 1]), mv(Bm, mv(Bm, [0, 1]))
assert bv == [1, 2] and b2v == [5, 4]
ra = b2v[0]; rb = b2v[1] - 2 * ra
assert (ra, rb) == (5, -6) and quad_roots(-5, 6) == (3, 2)
lv.expect("review", "items[0].prose", "(5, 4)")
lv.expect("review", "items[0].widget.answer", "(5, -6)")
Cr = [[0, -2], [1, 0]]
assert mv(Cr, [1, 0]) == [0, 1] and mv(Cr, [0, 1]) == [-2, 0]
lv.expect("review", "items[1].prose", "(-2, 0)")
hdet = 3 * 2 - (1 + 1j) * (1 - 1j)
assert hdet == 4 and quad_roots(-5, 4) == (4, 1)
lv.expect("review", "items[2].widget.answer", 4)
lv.expect("review", "items[2].explain.text", 4)
assert blocks([2, 3, 4, 5, 5]) == [4, 1]
assert [sum(min(b, k) for b in [3, 2]) for k in range(1, 6)] == [2, 4, 5, 5, 5]
lv.expect("review", "items[4].widget.options[1].why", "(2, 4, 5, 5, 5)")
z1, z2 = quad_roots(-1.2, 0.72)
assert abs(z1 - (0.6 + 0.6j)) < 1e-12
rmod = abs(z1)
assert abs(rmod - math.sqrt(0.72)) < 1e-12 and round(rmod, 4) == 0.8485
assert abs(cmath.phase(z1) - math.pi / 4) < 1e-12
lv.expect("review", "items[6].widget.answer", 0.8485)
lv.expect("review", "items[6].explain.text", round(0.72 ** 4, 4))
assert abs(rmod ** 8 - 0.72 ** 4) < 1e-12
assert dot([1, -1, 0], [1, 1, -2]) == 0

# ================= homework-4 =================
d7 = [3, 5, 6, 7, 7, 7, 7]
sizes = blocks(d7)
assert sizes == [4, 2, 1] and sum(sizes) == 7
for row, cnt in enumerate([sizes.count(1), sizes.count(2), sizes.count(3), sizes.count(4)]):
    lv.expect("homework", f"items[2].widget.rows[{row}][1].answer", cnt)
assert blocks([2, 4, 5, 5, 5]) == [3, 2] and blocks([2, 3, 4, 5, 5]) == [4, 1]
Ad = [[2, 0, 0], [0, 2, 0], [0, 0, 5]]
assert mv(Ad, [1, 1, 1]) == [2, 2, 5] and mv(Ad, [2, 2, 5]) == [4, 4, 25]
assert annih(Ad, [1, 1, 1]) == [1, -7, 10]
lv.expect("homework", "items[4].widget.answer", "z^2-7z+10")
lv.expect("homework", "items[4].explain.text", -10)
h8 = [t * F(4, 5) ** (t - 1) for t in range(1, 21)]
assert max(h8) == F(256, 125) == h8[3] == h8[4]
lv.expect("homework", "items[5].widget.answer", float(F(256, 125)))
lv.expect("homework", "items[5].widget.wrong[0].value", float(F(4, 5) ** 4))
lv.expect("homework", "items[5].widget.wrong[2].value", float(3 * F(4, 5) ** 2))
W3 = [[1, 0], [0, 3]]; W3inv = [[1, 0], [0, F(1, 3)]]
T2 = [[1, 2], [2, 1]]
adj3 = mm(W3inv, mm(T2, W3))
assert adj3 == [[1, 6], [F(2, 3), 1]]
lv.expect("homework", "items[6].widget.answer", 6)
lv.expect("homework", "items[6].widget.wrong[1].value", round(2 / 3, 4))
lv.expect("homework", "items[6].explain.text", 6)
# deflation tolerance (stated atol 1e-6); the CPython run reaches errors near 1e-14
lv.expect("homework", "items[1].widget.how", "1e-6")
lv.expect("homework", "items[1].widget.tests[0].expect", "[2.0, 0.5, 0.5]")

lv.check_wrongs()
lv.report()
