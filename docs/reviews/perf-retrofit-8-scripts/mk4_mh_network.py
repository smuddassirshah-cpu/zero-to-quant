"""markov L4 h-mh-network, second read. Run from this folder with the venv Python.
Every matrix expect rebuilt as Fractions from w_i P_ij = min(w_i/deg i, w_j/deg j)
(a route through the balance flow, not the acceptance formula); stationarity and
uniqueness by the rank of P^T - I; the share bands against the exact asymptotic
standard deviation of a correct run (fundamental matrix) and against 300 seeds of
a reader sampler that draws from the matrix rows; reader solutions and slips."""
import math, random, sys
from fractions import Fraction as Fr
import numpy as np
import harness as H

it = H.item("markov", "homework-4.json", "h-mh-network")
w = it["widget"]
bad = 0


def check(c, m):
    global bad
    print(("ok   " if c else "FAIL ") + m)
    bad += not c


g = {}
exec(w["prelude"], g)


def flow_matrix(n, edges, wt):
    nb = [set() for _ in range(n)]
    for u, v in edges:
        nb[u].add(v); nb[v].add(u)
    wt = [Fr(x) for x in wt]
    P = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        for j in nb[i]:
            P[i][j] = min(wt[i] / len(nb[i]), wt[j] / len(nb[j])) / wt[i]   # the balanced flow over w_i
        P[i][i] = 1 - sum(P[i])
    return P


for k, c in enumerate(w["tests"]):
    if c["call"].startswith("mh_network_matrix("):
        P = eval(c["call"].replace("mh_network_matrix", "flow_matrix"), {**g, "flow_matrix": flow_matrix})
        want = eval(c["expect"])
        check(all(abs(float(P[i][j]) - want[i][j]) < 1e-15 for i in range(len(P)) for j in range(len(P))), "test %d matrix expect by the balanced flow" % (k + 1))

# stationarity, uniqueness, and plain Metropolis off target on every network tested
for name, n, E, wt in [("STAR", 4, g["STAR"], [1, 1, 2, 3]), ("KITE", 5, g["KITE"], g["KW"]), ("PATH3", 3, g["PATH3"], [1, 1, 1]), ("two", 2, [(0, 1)], [1, 3])]:
    P = flow_matrix(n, E, wt)
    pi = [Fr(x, sum(wt)) for x in wt]
    check(all(sum(pi[i] * P[i][j] for i in range(n)) == pi[j] for j in range(n)), "%s: pi = w/sum(w) solves pi P = pi exactly" % name)
    A = np.array([[float(P[j][i]) - (i == j) for j in range(n)] for i in range(n)])
    check(np.linalg.matrix_rank(A) == n - 1, "%s: P^T - I has rank n - 1, so pi is the only stationary law" % name)

# ---- the share bands: exact asymptotic sd of a correct run ------------------
def asym_sd(P, pi, steps):
    P = np.array([[float(x) for x in r] for r in P]); pi = np.array([float(x) for x in pi]); n = len(pi)
    Z = np.linalg.inv(np.eye(n) - P + np.outer(np.ones(n), pi))
    out = []
    for j in range(n):
        f = (np.arange(n) == j) - pi[j]
        var = 2 * pi @ (f * (Z @ f)) - pi @ (f * f)
        out.append(math.sqrt(var / steps))
    return max(out)


for k, (n, E, wt) in [(9, (4, g["STAR"], [1, 1, 2, 3])), (10, (5, g["KITE"], g["KW"]))]:
    P = flow_matrix(n, E, wt)
    sd = asym_sd(P, [Fr(x, sum(wt)) for x in wt], 100000)
    check(0.04 / sd >= 7, "test %d: band 0.04 is %.1f asymptotic sd of the widest share (sd %.4f)" % (k, 0.04 / sd, sd))


def row_sampler(n, E, wt, start, steps, seed):
    P = [[float(x) for x in r] for r in flow_matrix(n, E, wt)]
    rng = random.Random(seed); x = start; v = [0] * n
    for _ in range(steps):
        u, acc = rng.random(), 0.0
        for j in range(n):
            acc += P[x][j]
            if u < acc:
                break
        x = j; v[x] += 1
    return [c / steps for c in v]


worst = 0.0
for seed in range(100):
    for n, E, wt, st in [(4, g["STAR"], [1, 1, 2, 3], 1), (5, g["KITE"], g["KW"], 4)]:
        s = row_sampler(n, E, wt, st, 100000, 1000 + seed)
        worst = max(worst, max(abs(a - b / sum(wt)) for a, b in zip(s, wt)))
check(worst < 0.02, "100 seeds of a row sampler on both networks: worst miss %.4f, half the 0.04 band" % worst)

# ---- reader solutions and slips ---------------------------------------------
FRAC = r'''
import random
from fractions import Fraction

def mh_network_matrix(n, edges, w):
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1; deg[v] += 1
    link = {(u, v) for u, v in edges} | {(v, u) for u, v in edges}
    P = []
    for i in range(n):
        row = [Fraction(0)] * n
        for j in range(n):
            if (i, j) in link:
                r = Fraction(w[j]) * deg[i] / (Fraction(w[i]) * deg[j])
                row[j] = min(Fraction(1), r) / deg[i]
        row[i] = 1 - sum(row)
        P.append([float(x) for x in row])
    return P

def mh_network_shares(n, edges, w, start, steps, seed):
    P = mh_network_matrix(n, edges, w)
    rng = random.Random(seed)
    x, seen = start, [0] * n
    for _ in range(steps):
        seen[x] += 1                       # count where it is, then move
        u = rng.random()
        for j in range(n):
            u -= P[x][j]
            if u < 0:
                break
        x = j
    return [c / steps for c in seen]
'''
NP = r'''
import numpy as np

def mh_network_matrix(n, edges, w):
    A = np.zeros((n, n))
    for u, v in edges:
        A[u, v] = A[v, u] = 1
    d = A.sum(1); w = np.asarray(w, float)
    R = np.where(A > 0, np.minimum(1, np.outer(1 / (w * 1.0), w) * np.outer(d, 1 / d)), 0)
    P = R / d[:, None]
    P[np.diag_indices(n)] = 1 - P.sum(1)
    return P.tolist()

def mh_network_shares(n, edges, w, start, steps, seed):
    g = np.random.default_rng(seed)
    nb = [[] for _ in range(n)]
    for u, v in edges:
        nb[u].append(v); nb[v].append(u)
    x, seen = start, np.zeros(n)
    us = g.random(steps); ks = g.random(steps)
    for t in range(steps):
        y = nb[x][int(ks[t] * len(nb[x]))]
        if us[t] * w[x] * len(nb[y]) < w[y] * len(nb[x]):
            x = y
        seen[x] += 1
    return (seen / steps).tolist()
'''
for label, src in [("shipped solution", w["solution"]), ("reader: Fractions, row sampler", FRAC), ("reader: NumPy, pre-drawn uniforms", NP)]:
    ex = [x for x in H.run(w, src, "examples") if x[0] != "pass"]
    f, r = H.summary(w, src, label)
    check(not f and not ex, label + " passes every example and test")
f, _ = H.summary(w, w["starter"], "starter")
check(len(f) == 11, "starter fails all 11")

S = w["solution"]


def mut(old, new):
    assert S.count(old) == 1, old
    return S.replace(old, new)


BUGS = [
    ("degree ratio upside down", mut("(w[j] * len(nb[i])) / (w[i] * len(nb[j]))", "(w[j] * len(nb[j])) / (w[i] * len(nb[i]))")),
    ("matrix without the 1/deg proposal factor", mut("P[i][j] = _accept(nb, w, i, j) / len(nb[i])", "P[i][j] = _accept(nb, w, i, j)")),
    ("diagonal is one proposal's rejection", mut("        P[i][i] = 1 - sum(P[i][j] for j in range(n) if j != i)   # rejections stay", "            P[i][i] = 1 - _accept(nb, w, i, j)")),
    ("sampler proposes any venue, Hastings ratio kept", mut("y = rng.choice(nb[x])", "y = rng.randrange(n)\n        if y not in nb[x]:\n            visits[x] += 1\n            continue")),
    ("sampler target w * deg (acceptance by weights times degrees)", mut("        if rng.random() < _accept(nb, w, x, y):", "        if rng.random() < min(1, w[y] * len(nb[y]) / (w[x] * len(nb[x]))):")),
]
for label, src in BUGS:
    f, _ = H.summary(w, src, "bug: " + label)
    check(bool(f), "reader bug caught: " + label)
print("problems:", bad)
sys.exit(1 if bad else 0)
