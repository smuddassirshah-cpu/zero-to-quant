"""Second read, eigen L2 hw-sigma-code and eigen L4 h-replicate-svd.
Every expect recomputed by two routes (exact Fractions or SymPy, and a float route), a reader solution of my own,
and my own planted bugs, all through harness13 (a mirror of code.js JUDGE). Exit 0 when every check holds.
Run: <venv>/bin/python -I eig_two.py   or   node pyo13.mjs <pkgs>/pyodide-0.27.7/package eig_two.py numpy"""
import sys, pathlib, math
from fractions import Fraction as Fr
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np
import harness13 as H

BAD = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        BAD.append(msg)


def ev(s):
    return eval(s, {"__builtins__": {}}, {})


# ---------------------------------------------------------------- eigen L2
it2 = H.item("eigen", "homework-2.json", "hw-sigma-code")
w2 = it2["widget"]
print("eigen L2 hw-sigma-code: numpy", np.__version__)


def frac_sigma(R):
    n, k = len(R), len(R[0])
    m = [sum(Fr(r[j]) for r in R) / n for j in range(k)]
    return [[sum((Fr(r[i]) - m[i]) * (Fr(r[j]) - m[j]) for r in R) / n for j in range(k)] for i in range(k)]


def frac_var(S, w):
    k = len(S)
    return sum(Fr(w[i]) * Fr(w[j]) * S[i][j] for i in range(k) for j in range(k))


def lam_min_bisect(S):
    """smallest eigenvalue of a symmetric matrix by bisection on the Sturm count of S - t I (LDL^T pivots), floats"""
    A = [[float(x) for x in row] for row in S]
    k = len(A)

    def below(t):  # number of eigenvalues < t = number of negative pivots of A - tI (Sylvester inertia)
        M = [[A[i][j] - (t if i == j else 0.0) for j in range(k)] for i in range(k)]
        neg = 0
        for p in range(k):
            piv = M[p][p]
            if piv == 0.0:
                piv = -1e-300
            if piv < 0:
                neg += 1
            for i in range(p + 1, k):
                f = M[i][p] / piv
                for j in range(p, k):
                    M[i][j] -= f * M[p][j]
        return neg
    lo, hi = -1e3, 1e3
    for _ in range(200):
        mid = (lo + hi) / 2
        if below(mid) >= 1:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


tables = {}
for c in w2["tests"]:
    g = {}
    exec(c["setup"], {}, g)
    tables.setdefault(c["setup"], g)
for i, c in enumerate(w2["tests"], 1):
    g = tables[c["setup"]]
    R, W = g["R"], g["W"]
    S = frac_sigma(R)
    part = int(c["call"].split("[")[-1].rstrip("]"))
    e = ev(c["expect"])
    if part == 0:
        A = [[float(x) for x in row] for row in S]
        D = np.asarray(R, float) - np.asarray(R, float).mean(axis=0)
        B = (D.T @ D / len(R)).tolist()
        check(all(math.isclose(A[a][b], e[a][b], abs_tol=1e-12) for a in range(len(A)) for b in range(len(A))) and np.allclose(B, e, atol=1e-12, rtol=0), f"L2 test {i} Sigma: Fractions {[[str(x) for x in r] for r in S]} and NumPy agree with expect")
    elif part == 1:
        cols = [[row[j] for row in W] for j in range(len(W[0]))]
        A = [float(frac_var(S, w)) for w in cols]
        Wn = np.asarray(W, float)
        Sg = np.asarray([[float(x) for x in r] for r in S])
        B = [float(Wn[:, j] @ Sg @ Wn[:, j]) for j in range(Wn.shape[1])]
        check(np.allclose(A, e, atol=1e-12, rtol=0) and np.allclose(B, e, atol=1e-12, rtol=0), f"L2 test {i} variances: Fractions {A} and a column loop {B} agree with {e}")
    else:
        a = lam_min_bisect(S)
        Sg = np.asarray([[float(x) for x in r] for r in S])
        rng = np.random.default_rng(13)
        V = rng.normal(size=(200000, len(Sg)))
        V /= np.linalg.norm(V, axis=1, keepdims=True)
        q = np.einsum("ij,jk,ik->i", V, Sg, V)
        check(abs(a - e) < 5e-8 and q.min() >= a - 1e-12 and q.min() - a < 2e-3, f"L2 test {i} least: bisection {a:.9f}, sphere search min {q.min():.6f} (never below), expect {e}")

# explain and feedback numbers
S6 = frac_sigma([[1, 2, -1], [3, 0, 2], [-2, 1, 0], [4, -1, 1], [-1, 3, 3]])
check(frac_var(S6, [Fr(1, 2), Fr(1, 2), 0]) == Fr(3, 5), "L2 explain: (0.5, 0.5, 0) has variance 0.6 exactly, length sqrt(0.5) < 1")
check(lam_min_bisect(S6) < min(float(S6[j][j]) for j in range(3)), "L2 feedback test-6: 0.6608 below every single asset's variance (5.2, 2, 2)")
R7 = [[3, 1, 2], [-1, 3, 1], [2, 0, 1], [0, 4, 2]]
check(all(Fr(r[2]) == Fr(r[0] + r[1], 2) for r in R7), "L2 feedback test-7: third asset is half A plus half B every day")
# the 'least' of length 1 is a weighted average: w = sum c_i q_i, variance sum c_i^2 lambda_i with sum c_i^2 = 1
lam, Q = np.linalg.eigh(np.asarray([[float(x) for x in r] for r in S6]))
wv = np.array([0.3, -0.5, 0.2]); wv /= np.linalg.norm(wv); cc = Q.T @ wv
check(abs(float(wv @ np.asarray([[float(x) for x in r] for r in S6]) @ wv) - float((cc ** 2) @ lam)) < 1e-12 and abs((cc ** 2).sum() - 1) < 1e-12, "L2 explain: variance of a unit w is the average of the eigenvalues weighted by c_i^2 (summing to 1)")
# a budget-constraint reading (weights sum to 1) gives a different number on test 3
S3 = np.asarray([[6.5, 3.0], [3.0, 2.0]])
mv = 1 / (np.ones(2) @ np.linalg.solve(S3, np.ones(2)))
check(abs(mv - 1.6) < 1e-12, "L2: the sum-to-one minimum variance on table 1 is 1.6, not 0.5, so the reading of |w| = 1 decides test 3")

sol2 = w2["solution"]
H.summary(w2, sol2, "L2 shipped solution", show=True)
check(H.run(w2, sol2) and all(x[0] == "pass" for x in H.run(w2, sol2)), "L2 shipped solution passes all 8")
check(all(x[0] == "pass" for x in H.run(w2, sol2, "examples")), "L2 shipped solution passes the example")
check(all(x[0] != "pass" for x in H.run(w2, w2["starter"])), "L2 starter fails all 8")

reader2 = '''
def risk_from_returns(R, W):
    import numpy as np
    n, k = len(R), len(R[0])
    mean = [sum(r[j] for r in R) / n for j in range(k)]
    Sigma = [[sum((r[i] - mean[i]) * (r[j] - mean[j]) for r in R) / n for j in range(k)] for i in range(k)]
    var = []
    for c in range(len(W[0])):
        w = [W[a][c] for a in range(k)]
        var.append(sum(w[a] * Sigma[a][b] * w[b] for a in range(k) for b in range(k)))
    D = np.array([[r[j] - mean[j] for j in range(k)] for r in R], dtype=float) / np.sqrt(n)
    s = np.linalg.svd(D, compute_uv=False)          # singular values of D/sqrt(n): their squares are Sigma's eigenvalues
    sq = sorted(list(s ** 2) + [0.0] * (k - len(s)))  # fewer days than assets leaves zero eigenvalues
    return Sigma, var, sq[0]
'''
check(all(x[0] == "pass" for x in H.run(w2, reader2)), "L2 reader solution (loops, lists, singular values of D) passes all 8")
reader2b = sol2.replace("D = R - R.mean(axis=0)                       # demean each asset\n    Sigma = D.T @ D / len(R)", "Sigma = np.cov(R, rowvar=False, bias=True)")
check(reader2b != sol2 and all(x[0] == "pass" for x in H.run(w2, reader2b)), "L2 np.cov(bias=True) route passes all 8")

plants2 = {
    "n - 1 (np.cov default)": H.patched(sol2, ("Sigma = D.T @ D / len(R) ", "Sigma = np.cov(R.T)      ")),
    "no demeaning": H.patched(sol2, ("D = R - R.mean(axis=0)", "D = R + 0 * R.mean(axis=0)")),
    "demean each day (axis=1)": H.patched(sol2, ("R.mean(axis=0)", "R.mean(axis=1, keepdims=True)")),
    "diagonal only, no cross terms": H.patched(sol2, ("np.sum(W * (Sigma @ W), axis=0)", "np.sum(W ** 2 * np.diag(Sigma)[:, None], axis=0)")),
    "portfolios read along rows of W": H.patched(sol2, ("np.sum(W * (Sigma @ W), axis=0)", "np.sum(W.T * (Sigma @ W.T), axis=0)")),
    "least = budget rule 1/(1' S^+ 1)": H.patched(sol2, ("float(np.linalg.eigvalsh(Sigma)[0])", "float(1 / (np.ones(len(Sigma)) @ np.linalg.pinv(Sigma) @ np.ones(len(Sigma))))")),
    "least = eig()[0], unsorted": H.patched(sol2, ("float(np.linalg.eigvalsh(Sigma)[0])", "float(np.real(np.linalg.eig(Sigma)[0][0]))")),
    "least = smallest asset variance": H.patched(sol2, ("float(np.linalg.eigvalsh(Sigma)[0])", "float(np.diag(Sigma).min())")),
    "least = smallest given portfolio": H.patched(sol2, ("float(np.linalg.eigvalsh(Sigma)[0])", "float(np.min(variances))")),
    "least = largest eigenvalue": H.patched(sol2, ("eigvalsh(Sigma)[0]", "eigvalsh(Sigma)[-1]")),
    "least over unit-sum weights by eigenvector rescale": H.patched(sol2, ("least = float(np.linalg.eigvalsh(Sigma)[0])", "lam, Q = np.linalg.eigh(Sigma); q = Q[:, 0] / Q[:, 0].sum() if abs(Q[:, 0].sum()) > 1e-12 else Q[:, 0]; least = float(q @ Sigma @ q)")),
}
for name, src in plants2.items():
    fails, _ = H.summary(w2, src, "L2 plant: " + name)
    check(len(fails) > 0, f"L2 plant caught: {name} (fails {fails})")

# ---------------------------------------------------------------- eigen L4
it4 = H.item("eigen", "homework-4.json", "h-replicate-svd")
w4 = it4["widget"]
print("\neigen L4 h-replicate-svd")
PAY = [[1, 80, 0, 20], [1, 90, 0, 10], [1, 100, 0, 0], [1, 110, 10, 0], [1, 120, 20, 0]]
check(ev("[" + w4["prelude"].split("=", 1)[1].strip() + "]")[0] == PAY, "L4 prelude PAY is the table in the prose (bond, stock, call 100, put 100)")
for S in (80, 90, 100, 110, 120):
    check([1, S, max(S - 100, 0), max(100 - S, 0)] == PAY[[80, 90, 100, 110, 120].index(S)], f"L4 PAY row for {S} from the payoffs")
nul = [100, -1, 1, -1]
check(all(sum(Fr(r[j]) * nul[j] for j in range(4)) == 0 for r in PAY), "L4 parity direction (100, -1, 1, -1) pays 0 in every state")


def fr_mat(A):
    return [[Fr(x) if not isinstance(x, float) else Fr(str(x)) for x in r] for r in A]


def solve_fr(M, b):
    n = len(M)
    A = [row[:] + [b[i]] for i, row in enumerate(M)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def minnorm_route_a(A, y):
    """route A: rank-3 PAY, solve with the first three columns (independent), then remove the part along the null vector"""
    A = fr_mat(A); y = [Fr(v) for v in y]
    B = [r[:3] for r in A]
    BtB = [[sum(B[k][i] * B[k][j] for k in range(len(B))) for j in range(3)] for i in range(3)]
    Bty = [sum(B[k][i] * y[k] for k in range(len(B))) for i in range(3)]
    x = solve_fr(BtB, Bty) + [Fr(0)]
    nn = [Fr(v) for v in nul]
    t = sum(a * b for a, b in zip(x, nn)) / sum(b * b for b in nn)
    w = [a - t * b for a, b in zip(x, nn)]
    res = [y[k] - sum(A[k][j] * w[j] for j in range(4)) for k in range(len(A))]
    return w, res


def minnorm_wide(A, y):
    """route for a wide full-row-rank table: w = A^T (A A^T)^{-1} y, exact"""
    A = fr_mat(A); y = [Fr(v) for v in y]
    m = len(A)
    AAt = [[sum(A[i][k] * A[j][k] for k in range(4)) for j in range(m)] for i in range(m)]
    z = solve_fr(AAt, y)
    return [sum(A[i][j] * z[i] for i in range(m)) for j in range(4)]


try:
    import sympy as sp
    HAVE_SP = True
except Exception:
    HAVE_SP = False


def route_b(A, y):
    if HAVE_SP:
        M = sp.Matrix([[sp.nsimplify(str(x)) for x in r] for r in A])
        w = M.pinv() * sp.Matrix(y)
        return [Fr(str(sp.nsimplify(v))) if v.is_Rational else Fr(str(v)) for v in w]
    return None


cases = {
    "straddle": ([20, 10, 0, 10, 20], "[0, 0, 1, 1]", "[0, 0, 0, 0, 0]"),
    "covered call": ([80, 90, 100, 100, 100], "[200/10003, 10001/10003, -10001/10003, -2/10003]", None),
    "digital": ([0, 0, 0, 1, 1], "[-39/70021, 5021/3501050, 175033/3501050, -12494/1750525]", "[1/35, -2/35, -1/7, 12/35, -6/35]"),
}
for name, (y, we, re_) in cases.items():
    wa, ra = minnorm_route_a(PAY, y)
    wb = route_b(PAY, y)
    e = [Fr(s.strip()) for s in we[1:-1].split(",")]
    check(wa == e and (wb is None or wb == e), f"L4 {name}: min-norm weights {[str(v) for v in wa]} by null-vector removal and by SymPy pinv equal the expect")
    if re_:
        er = [Fr(s.strip()) for s in re_[1:-1].split(",")]
        check(ra == er, f"L4 {name}: residual {[str(v) for v in ra]} equals the expect")
    check(sum(a * b for a, b in zip(wa, [Fr(v) for v in nul])) == 0, f"L4 {name}: weights have no part along the parity direction (test 5's claim)")
# covered call: 'stock minus a call fits too, but it is longer'
v = [0, 1, -1, 0]; wa, _ = minnorm_route_a(PAY, [80, 90, 100, 100, 100])
check(all(sum(PAY[k][j] * v[j] for j in range(4)) == [80, 90, 100, 100, 100][k] for k in range(5)) and sum(x * x for x in wa) < 2, "L4 feedback test-4: stock minus a call fits exactly and is longer (|v|^2 = 2 > |w|^2)")
TWO = [[1, 90, 0, 10], [1, 110, 10, 0]]
wt = minnorm_wide(TWO, [0, 1])
et = [Fr(s.strip()) for s in "-17/20306, 551/101530, 8201/203060, -9901/203060".split(",")]
wb = route_b(TWO, [0, 1])
check(wt == et and (wb is None or wb == et), f"L4 TWO: A^T (A A^T)^-1 y = {[str(x) for x in wt]} and SymPy pinv equal test 8's expect")
KEYED = [[1, 80, 0, 20], [1, 90, 0, 10.01], [1, 100, 0, 0], [1, 110, 10, 0], [1, 120, 20, 0]]
yk = [20, 10, 0, 10, 20]
K = fr_mat(KEYED)
KtK = [[sum(K[k][i] * K[k][j] for k in range(5)) for j in range(4)] for i in range(4)]
xk = solve_fr(KtK, [sum(K[k][i] * yk[k] for k in range(5)) for i in range(4)])
check(xk == [100, -1, 2, 0], f"L4 KEYED full rank: exact normal equations give {[str(x) for x in xk]} (test 12)")
check(all(sum(K[k][j] * xk[j] for j in range(4)) == yk[k] for k in range(5)), "L4 feedback test-12: two calls, less the stock, plus 100 bonds fits exactly")
sK = np.linalg.svd(np.asarray(KEYED, float), compute_uv=False)
check(7e-5 < sK[-1] < 9e-5 and sK[-1] < 1e-5 * sK[0] and sK[-1] > 1e-5 and sK[-1] > 1e-10 * sK[0], f"L4 KEYED smallest singular value {sK[-1]:.3g}: below 1e-5 x largest ({1e-5 * sK[0]:.3g}), above 1e-5 alone and above 1e-10 x largest")
try:
    import mpmath as mp
    mp.mp.dps = 50
    A = mp.matrix([[mp.mpf(str(x)) for x in r] for r in KEYED])
    U, Sg, V = mp.svd_r(A, full_matrices=False)
    kept = [i for i in range(len(Sg)) if Sg[i] > mp.mpf("1e-5") * max(Sg)]
    wv = [sum(V[i, j] * sum(U[k, i] * yk[k] for k in range(5)) / Sg[i] for i in kept) for j in range(4)]
    e10 = ev(w4["tests"][9]["expect"])
    check(len(kept) == 3 and all(abs(float(a) - b) < 6e-8 for a, b in zip(wv, e10)), f"L4 test 10: 50-digit truncated SVD gives {[mp.nstr(x, 8) for x in wv]}, expect {e10} within rounding")
except ImportError:
    U, s, Vt = np.linalg.svd(np.asarray(KEYED, float), full_matrices=False)
    keep = s > 1e-5 * s.max()
    wv = Vt[keep].T @ ((U[:, keep].T @ np.asarray(yk, float)) / s[keep])
    e10 = ev(w4["tests"][9]["expect"])
    check(int(keep.sum()) == 3 and np.allclose(wv, e10, atol=6e-8, rtol=0), f"L4 test 10 (Pyodide: NumPy only): truncated SVD gives {wv}, expect {e10}")
# truncation: the test 10 answer is the min-norm LS solution of the rank-3 truncated table, not of KEYED itself
check(np.linalg.norm(np.asarray(KEYED) @ np.asarray(e10) - yk) > 1e-4, "L4 test 10: with the cut-off the weights no longer fit KEYED exactly (they solve the truncated table), as the prose's 'counts as zero' implies")

sol4 = w4["solution"]
H.summary(w4, sol4, "L4 shipped solution", show=True)
check(all(x[0] == "pass" for x in H.run(w4, sol4)), "L4 shipped solution passes all 13")
check(all(x[0] == "pass" for x in H.run(w4, sol4, "examples")), "L4 shipped solution passes the example")
check(all(x[0] != "pass" for x in H.run(w4, w4["starter"])), "L4 starter fails all 13")

reader4 = '''
import numpy as np

def replicate_payoff(PAY, y, tol=1e-10):
    A = np.array(PAY, dtype=float)
    b = np.array(y, dtype=float)
    U, s, Vt = np.linalg.svd(A)              # full matrices, then loop over the singular values
    w = np.zeros(A.shape[1])
    kept = 0
    for i, si in enumerate(s):
        if si >= tol * s[0]:
            w += (U[:, i] @ b) / si * Vt[i]
            kept += 1
    return w, b - A @ w, kept
'''
check(all(x[0] == "pass" for x in H.run(w4, reader4)), "L4 reader solution (full SVD, loop of rank-one pieces) passes all 13")

plants4 = {
    "normal equations solve(A'A, A'y)": H.patched(sol4, ("    U, s, Vt = np.linalg.svd(A, full_matrices=False)\n", "    U, s, Vt = np.linalg.svd(A, full_matrices=False)\n    return np.linalg.solve(A.T @ A, A.T @ y), y - A @ np.linalg.solve(A.T @ A, A.T @ y), len(s)\n")),
    "no cut-off": H.patched(sol4, ("keep = s > tol * s.max()", "keep = s > 0")),
    "absolute cut-off s > tol": H.patched(sol4, ("keep = s > tol * s.max()", "keep = s > tol")),
    "residual A w - y": H.patched(sol4, ("return w, y - A @ w,", "return w, A @ w - y,")),
    "rank = len(s)": H.patched(sol4, ("int(keep.sum())", "len(s)")),
    "rank = np.linalg.matrix_rank(A)": H.patched(sol4, ("int(keep.sum())", "int(np.linalg.matrix_rank(A))")),
    "times s instead of divided": H.patched(sol4, ("/ s[keep])", "* s[keep])")),
    "columns of Vt for rows": H.patched(sol4, ("Vt[keep].T @", "Vt[:, keep] @")),
    "always drop the smallest": H.patched(sol4, ("keep = s > tol * s.max() ", "keep = np.arange(len(s)) < len(s) - 1")),
    "cut-off against the sum of s": H.patched(sol4, ("keep = s > tol * s.max()", "keep = s > tol * s.sum() * 1e4")),
    "NumPy pinv": H.patched(sol4, ("w = Vt[keep].T @ ((U[:, keep].T @ y) / s[keep])", "w = np.linalg.pinv(A, rcond=tol) @ y")),
}
for name, src in plants4.items():
    fails, _ = H.summary(w4, src, "L4 plant: " + name)
    check(len(fails) > 0, f"L4 plant caught: {name} (fails {fails})")

print("\nfailures:", len(BAD))
sys.exit(1 if BAD else 0)
