"""Second read, least-squares L2 h-factor-neutral (code). Every expect recomputed exactly (Fractions: the formula
F (F'F)^-1 F' and Gram-Schmidt), the refusals by exact rank, a reader solution, my own planted bugs, and for every
refusal case the exception each variant raises, so a pass 'for the wrong reason' is visible.
Run: <venv>/bin/python -I ls_two.py   or   node pyo13.mjs <pkgs>/pyodide-0.27.7/package ls_two.py numpy"""
import sys, pathlib
from fractions import Fraction as Fr
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numpy as np
import harness13 as H

BAD = []


def check(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        BAD.append(msg)


it = H.item("least-squares", "homework-2.json", "h-factor-neutral")
w = it["widget"]
T = w["tests"]
print("least-squares L2 h-factor-neutral: numpy", np.__version__, "platform", sys.platform)


def fr(x):
    return Fr(str(x)) if isinstance(x, float) else Fr(x)


def rank_fr(M):
    A = [[fr(x) for x in r] for r in M]
    rk, rows, cols = 0, len(A), len(A[0])
    for c in range(cols):
        p = next((r for r in range(rk, rows) if A[r][c] != 0), None)
        if p is None:
            continue
        A[rk], A[p] = A[p], A[rk]
        for r in range(rows):
            if r != rk and A[r][c] != 0:
                f = A[r][c] / A[rk][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[rk])]
        rk += 1
    return rk


def inv_fr(M):
    n = len(M)
    A = [list(M[i]) + [Fr(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        piv = A[c][c]
        A[c] = [x / piv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [r[n:] for r in A]


def proj_formula(F):
    F = [[fr(x) for x in r] for r in F]
    n, k = len(F), len(F[0])
    FtF = [[sum(F[t][i] * F[t][j] for t in range(n)) for j in range(k)] for i in range(k)]
    G = inv_fr(FtF)
    return [[sum(F[a][i] * G[i][j] * F[b][j] for i in range(k) for j in range(k)) for b in range(n)] for a in range(n)]


def fitted_gs(F, s):
    """route B: orthogonalise the columns in exact arithmetic (no square roots: project on each earlier q unnormalised)"""
    F = [[fr(x) for x in r] for r in F]
    n, k = len(F), len(F[0])
    cols = [[F[t][j] for t in range(n)] for j in range(k)]
    qs = []
    for c in cols:
        v = c[:]
        for q in qs:
            a = sum(x * y for x, y in zip(c, q)) / sum(y * y for y in q)
            v = [x - a * y for x, y in zip(v, q)]
        qs.append(v)
    s = [fr(x) for x in s]
    out = [Fr(0)] * n
    for q in qs:
        a = sum(x * y for x, y in zip(s, q)) / sum(y * y for y in q)
        out = [o + a * y for o, y in zip(out, q)]
    return out


def ns(setup):
    g = {"np": np}
    exec("; ".join(p for p in setup.split(";") if "project_out" not in p), g)  # F and s only, never the item's own call
    return g


for i, c in enumerate(T, 1):
    g = ns(c["setup"])
    F, s = g["F"], g["s"]
    k = len(F[0])
    rk = rank_fr(F)
    if c["compare"] == "raises":
        check(rk < k, f"test {i}: exact rank {rk} < {k} columns, so the refusal is right")
        check(c["expect"] == "ValueError", f"test {i}: expects ValueError")
        continue
    check(rk == k, f"test {i}: exact rank {rk} = {k}, independent")
    P = proj_formula(F)
    fit = [sum(P[a][b] * fr(s[b]) for b in range(len(s))) for a in range(len(s))]
    fit2 = fitted_gs(F, s)
    neu = [fr(x) - y for x, y in zip(s, fit)]
    e = eval(c["expect"])
    call = c["call"]
    if call.endswith("[2]") and "@" not in call:
        got, got2 = [float(x) for x in neu], [float(fr(x) - y) for x, y in zip(s, fit2)]
    elif call.endswith("[1]"):
        got, got2 = [float(x) for x in fit], [float(x) for x in fit2]
    elif call.endswith("[0]"):
        got = [[float(x) for x in r] for r in P]
        got2 = got
    elif "shape" in call:
        PP = [[sum(P[a][m] * P[m][b] for m in range(len(P))) for b in range(len(P))] for a in range(len(P))]
        got = [[len(P), len(P)], PP == P, all(P[a][b] == P[b][a] for a in range(len(P)) for b in range(len(P)))]
        got2 = got
    elif "@" in call:
        got = [float(sum(fr(F[t][j]) * neu[t] for t in range(len(s)))) for j in range(k)]
        got2 = got
    elif "0::2" in call:
        got = [[[float(x) for x in r] for r in P], [float(x) for x in neu]]
        got2 = got
    check(H._close(got, e, (1e-12, 1e-12)) and H._close(got2, e, (1e-12, 1e-12)), f"test {i}: exact formula {str(got)[:70]} and Gram-Schmidt agree with expect")

# feedback claims
g = ns(T[0]["setup"])
check(fitted_gs(g["F"], g["s"]) == [2, 2, 3, 3], "byKey test-1/2: neutral is each score minus its sector mean (sector means 2 and 3)")
g = ns(T[12]["setup"])
FF = np.asarray(g["F"], float)
sv = np.linalg.svd(FF, compute_uv=False)
check(np.corrcoef(FF[:, 1], [1, 1.01, 0.99, 1])[0, 1] > 0.99 and sv[-1] / sv[0] > 1e-3, f"test 13: near-collinear pair, singular value ratio {sv[-1] / sv[0]:.2e} (far above any rounding cut-off)")
g = ns(T[9]["setup"])
F10 = np.asarray(g["F"], float)
sv10 = np.linalg.svd(F10, compute_uv=False)
check(int(np.linalg.matrix_rank(F10)) == 2, f"test 10: float matrix_rank 2 (singular values {sv10[-1]:.1e} of {sv10[0]:.1e})")
d10 = float(np.linalg.det(F10.T @ F10))
print(f"     test 10: det(F'F) in this NumPy = {d10!r} (a 'det == 0' check {'misses' if d10 != 0 else 'catches'} it here)")

sol = w["solution"]
H.summary(w, sol, "shipped solution", show=True)
check(all(x[0] == "pass" for x in H.run(w, sol)), "shipped solution passes all 13")
check(all(x[0] == "pass" for x in H.run(w, sol, "examples")), "shipped solution passes the example")
check(all(x[0] != "pass" for x in H.run(w, w["starter"])), "starter fails all 13")

reader = '''
import numpy as np

def project_out(F, s):
    F = np.asarray(F, dtype=float)
    s = np.asarray(s, dtype=float)
    sv = np.linalg.svd(F, compute_uv=False)
    if F.shape[1] > F.shape[0] or sv[-1] <= 1e-10 * sv[0]:
        raise ValueError("dependent factor columns")
    P = F @ np.linalg.solve(F.T @ F, F.T)
    fitted = P @ s
    return P, fitted, s - fitted
'''
check(all(x[0] == "pass" for x in H.run(w, reader)), "reader solution (SVD ratio check, solve on the normal equations) passes all 13")
reader_b = '''
import numpy as np

def project_out(F, s):
    F = np.array(F, dtype=float)
    s = np.array(s, dtype=float)
    n, k = F.shape
    Q = []
    for j in range(k):                       # Gram-Schmidt, refusing a column that is (nearly) a combination
        v = F[:, j].copy()
        for q in Q:
            v -= (q @ F[:, j]) * q
        if np.linalg.norm(v) <= 1e-9 * max(1.0, np.linalg.norm(F[:, j])):
            raise ValueError("dependent")
        Q.append(v / np.linalg.norm(v))
    Q = np.column_stack(Q)
    P = Q @ Q.T
    return P, P @ s, s - P @ s
'''
check(all(x[0] == "pass" for x in H.run(w, reader_b)), "reader solution B (Gram-Schmidt with its own refusal) passes all 13")

REF = [9, 10, 11]
plants = {
    "no rank check, inv(F'F)": H.patched(sol, ("    if np.linalg.matrix_rank(F) < k:\n        raise ValueError(\"the factor columns are dependent\")\n    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    P = F @ np.linalg.inv(F.T @ F) @ F.T ")),
    "no rank check, solve(F'F, F')": H.patched(sol, ("    if np.linalg.matrix_rank(F) < k:\n        raise ValueError(\"the factor columns are dependent\")\n    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    P = F @ np.linalg.solve(F.T @ F, F.T) ")),
    "no rank check, QR": H.patched(sol, ("    if np.linalg.matrix_rank(F) < k:\n        raise ValueError(\"the factor columns are dependent\")\n", "")),
    "no rank check, Cholesky of F'F": H.patched(sol, ("    if np.linalg.matrix_rank(F) < k:\n        raise ValueError(\"the factor columns are dependent\")\n    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    L = np.linalg.cholesky(F.T @ F)\n    Q = F @ np.linalg.inv(L).T\n    P = Q @ Q.T ")),
    "det(F'F) == 0 check": H.patched(sol, ("if np.linalg.matrix_rank(F) < k:", "if np.linalg.det(F.T @ F) == 0:")),
    "rank compared with rows": H.patched(sol, ("if np.linalg.matrix_rank(F) < k:", "if np.linalg.matrix_rank(F) < F.shape[0]:")),
    "refuses when cond(F) > 100": H.patched(sol, ("if np.linalg.matrix_rank(F) < k:", "if F.shape[1] > F.shape[0] or np.linalg.cond(F) > 100:")),
    "P = Q.T @ Q": H.patched(sol, ("P = Q @ Q.T ", "P = Q.T @ Q ")),
    "last transpose missing (shape error)": H.patched(sol, ("    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    P = F @ np.linalg.inv(F.T @ F) @ F")),
    "no rank check and last transpose missing": H.patched(sol, ("    if np.linalg.matrix_rank(F) < k:\n        raise ValueError(\"the factor columns are dependent\")\n    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    Q, R = np.linalg.qr(F)\n    P = Q @ Q ")),
    "neutral = fitted - s": H.patched(sol, ("neutral = s - fitted", "neutral = fitted - s")),
    "sum of projections on each column": H.patched(sol, ("    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    P = sum(np.outer(F[:, j], F[:, j]) / (F[:, j] @ F[:, j]) for j in range(k)) ")),
    "inverse left out, P = F F'": H.patched(sol, ("    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    P = F @ F.T ")),
    "complete QR": H.patched(sol, ("np.linalg.qr(F)", "np.linalg.qr(F, mode='complete')")),
    "no rank check, pinv": H.patched(sol, ("    if np.linalg.matrix_rank(F) < k:\n        raise ValueError(\"the factor columns are dependent\")\n    Q, R = np.linalg.qr(F)        # reduced: Q is n x k, orthonormal columns\n    P = Q @ Q.T ", "    P = F @ np.linalg.pinv(F) ")),
    "returns (fitted, neutral, P)": H.patched(sol, ("return P, fitted, neutral", "return fitted, neutral, P")),
}
wrong_reason = []
for name, src in plants.items():
    fails, r = H.summary(w, src, "plant: " + name)
    check(len(fails) > 0, f"plant caught: {name} (fails {fails})")
    for t in REF:
        if r[t - 1][0] == "pass" and "ValueError(\"the factor" not in src and "raise ValueError" not in src:
            wrong_reason.append((name, t, r[t - 1][1]))
        elif r[t - 1][0] == "pass" and "raised ValueError" not in r[t - 1][1]:
            wrong_reason.append((name, t, r[t - 1][1]))
print("\nRefusal tests passed by a NumPy error rather than the learner's own ValueError:")
for name, t, v in wrong_reason:
    print(f"     {name}: test {t} {v}")
# none of them passes all 13
check(all(len(H.run(w, plants[n])) and any(x[0] != "pass" for x in H.run(w, plants[n])) for n, _, _ in wrong_reason), "every variant that passes a refusal through NumPy's own error fails some other test")

print("\nfailures:", len(BAD))
sys.exit(1 if BAD else 0)
