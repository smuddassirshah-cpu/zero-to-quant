"""markov L2 hw-absorb-code, second read. Run from this folder with the venv Python.
Reader solutions by other routes (exact Fractions by Gauss-Jordan, value iteration
to convergence, rng.choices and NumPy Generator samplers), reader-planted slips
(none from the author's nine), every expect recomputed as Fractions by first-step
equations solved one state at a time, and the simulation bands in standard errors."""
import math, sys, time
from fractions import Fraction as F
import harness as H

it = H.item("markov", "homework-2.json", "hw-absorb-code")
w = it["widget"]
bad = 0


def check(c, m):
    global bad
    print(("ok   " if c else "FAIL ") + m)
    bad += not c


# ---- exact expects by elimination over Fractions ---------------------------
g = {}
exec(w["prelude"], g)
CH = {k: [[F(x).limit_denominator(1000) for x in r] for r in g[k]] for k in ["WALK", "TENNIS", "SIX", "CYCLE", "DIRECT", "STUCK"]}


def solve(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def exact(P):
    n = len(P)
    ends = [i for i in range(n) if P[i][i] == 1]
    mov = [i for i in range(n) if P[i][i] != 1]
    A = [[(1 if i == j else 0) - P[i][j] for j in mov] for i in mov]
    Hm = [[F(0)] * n for _ in range(n)]
    for a in ends:
        Hm[a][a] = F(1)
    for e in ends:
        col = solve(A, [P[i][e] for i in mov]) if mov else []
        for k, i in enumerate(mov):
            Hm[i][e] = col[k]
    t = [F(0)] * n
    if mov:
        for k, x in enumerate(solve(A, [F(1)] * len(mov))):
            t[mov[k]] = x
    return Hm, t


for k, c in enumerate(w["tests"]):
    name = c["call"].split("(")[1].split(",")[0].rstrip(")")
    want = eval(c["expect"])
    Hm, t = exact(CH[name])
    if c["call"].startswith("absorb_chances"):
        got = Hm
    elif c["call"].startswith("steps_to_absorb"):
        got = t
    else:
        start = int(c["call"].split(",")[1])
        got = Hm[start]
    flat = lambda v: [x for r in v for x in (r if isinstance(r, list) else [r])]
    check(all(abs(float(a) - b) < 1e-12 for a, b in zip(flat(got), flat(want))) and len(flat(got)) == len(flat(want)), "test %d %s: expect matches exact first-step solve" % (k + 1, c["call"]))
    if "tol" in c:
        runs = int(c["call"].split(",")[2])
        se = max(math.sqrt(float(p) * (1 - float(p)) / runs) for p in got)
        check(c["tol"]["abs"] / se >= 7, "test %d band 0.02 is %.1f standard errors of the widest share" % (k + 1, c["tol"]["abs"] / se))

# tennis closed forms with p = 0.6
p, q = F(3, 5), F(2, 5)
check(p * p / (p * p + q * q) == F(9, 13) and 2 / (p * p + q * q) == F(50, 13), "deuce: p^2/(p^2+q^2) = 9/13 and 2/(p^2+q^2) = 50/13")
check(round(9 / 13, 3) == 0.692 and round(50 / 13, 2) == 3.85, "explain: 9/13 = 0.692 and 50/13 = 3.85")

# ---- reader solutions -------------------------------------------------------
EXACT = r'''
import random
from fractions import Fraction

def _solve(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]

def _parts(P):
    P = [[Fraction(x).limit_denominator(10**6) for x in r] for r in P]
    n = len(P)
    mov = [i for i in range(n) if P[i][i] != 1]
    A = [[(1 if i == j else 0) - P[i][j] for j in mov] for i in mov]
    return P, n, mov, A

def absorb_chances(P):
    P, n, mov, A = _parts(P)
    H = [[0.0] * n for _ in range(n)]
    for e in range(n):
        if P[e][e] == 1:
            H[e][e] = 1.0
            if mov:
                for k, x in enumerate(_solve(A, [P[i][e] for i in mov])):
                    H[mov[k]][e] = float(x)
    return H

def steps_to_absorb(P):
    P, n, mov, A = _parts(P)
    t = [0.0] * n
    if mov:
        for k, x in enumerate(_solve(A, [Fraction(1)] * len(mov))):
            t[mov[k]] = float(x)
    return t

def simulate_absorb(P, start, runs, seed):
    rng = random.Random(seed)
    n = len(P)
    out = [0] * n
    for _ in range(runs):
        s = start
        while P[s][s] != 1:
            s = rng.choices(range(n), weights=P[s])[0]
        out[s] += 1
    return [c / runs for c in out]
'''
ITER = r'''
import random

def _sweep(P, f, init):
    n = len(P)
    x = init[:]
    for _ in range(100000):
        y = [x[i] if P[i][i] == 1 else f(i) + sum(P[i][j] * x[j] for j in range(n)) for i in range(n)]
        if max(abs(a - b) for a, b in zip(x, y)) < 1e-15:
            return y
        x = y
    return x

def absorb_chances(P):
    n = len(P)
    cols = []
    for e in range(n):
        if P[e][e] == 1:
            cols.append(_sweep(P, lambda i: 0.0, [1.0 if i == e else 0.0 for i in range(n)]))
        else:
            cols.append([0.0] * n)
    return [[cols[e][i] for e in range(n)] for i in range(n)]

def steps_to_absorb(P):
    return _sweep(P, lambda i: 1.0, [0.0] * len(P))

def simulate_absorb(P, start, runs, seed):
    import numpy as np
    g = np.random.default_rng(seed)
    n = len(P)
    out = [0] * n
    for _ in range(runs):
        s = start
        while P[s][s] != 1:
            s = int(g.choice(n, p=P[s]))
        out[s] += 1
    return [c / runs for c in out]
'''
for label, src in [("shipped solution", w["solution"]), ("reader: Fractions, rng.choices", EXACT), ("reader: value iteration, NumPy Generator", ITER)]:
    ex = [x for x in H.run(w, src, "examples") if x[0] != "pass"]
    f, r = H.summary(w, src, label)
    check(not f and not ex, label + " passes every example and test")
H.summary(w, w["starter"], "starter")
check(len(H.summary(w, w["starter"], "starter (again)")[0]) == 12, "starter fails all 12")

S = w["solution"]


def mut(old, new):
    assert S.count(old) == 1, old
    return S.replace(old, new)


BUGS = [
    ("Q transposed", mut("np.linalg.inv(np.eye(len(moving)) - P[np.ix_(moving, moving)])", "np.linalg.inv(np.eye(len(moving)) - P[np.ix_(moving, moving)].T)")),
    ("time counts the absorbing step as well", mut("t[moving] = N @ np.ones(len(moving))", "t[moving] = N @ np.ones(len(moving)) + 1")),
    ("H written back as if moving states came first", mut("H[np.ix_(moving, ends)] = B", "H[np.ix_(list(range(len(moving))), ends)] = B")),
    ("uniform next state, not the row", mut("u, acc = rng.random(), 0.0", "u, acc = rng.random(), 0.0\n            j = rng.randrange(n)\n            if P[s][j] == 0: continue\n            s = j; continue")),
    ("reseeded inside every run", mut("    for _ in range(runs):\n        s = start", "    for _ in range(runs):\n        rng = random.Random(seed)\n        s = start")),
    ("50 sweeps of t = 1 + Qt", mut("t[moving] = N @ np.ones(len(moving))", "x = np.zeros(len(moving))\n        for _ in range(50): x = 1 + P[np.ix_(moving, moving)] @ x\n        t[moving] = x")),
    ("first step drawn from row 0, not the start", mut("        s = start\n        while", "        s = 0 if P[0][0] != 1 else start\n        while")),
]
for label, src in BUGS:
    f, _ = H.summary(w, src, "bug: " + label)
    check(bool(f), "reader bug caught: " + label)

# a deliberately slow pure-Python sampler: rebuild a cumulative list per step
SLOW = EXACT.replace("s = rng.choices(range(n), weights=P[s])[0]", "cum = [sum(P[s][:j + 1]) for j in range(n)]\n            u = rng.random()\n            s = next(j for j in range(n) if u < cum[j])")
f, r = H.summary(w, SLOW, "slow pure-Python sampler")
check(not f and max(x[2] for x in r) < 1.0, "slowest pure-Python case under 1 s in CPython (5 s budget in Pyodide)")
print("problems:", bad)
sys.exit(1 if bad else 0)
