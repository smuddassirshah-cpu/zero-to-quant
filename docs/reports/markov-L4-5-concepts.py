#!/usr/bin/env python3
"""Concept checks for the blind audit of markov levels 4 and 5 (round 1).

Run with the venv Python (NumPy needed):
    python docs/reports/markov-L4-5-concepts.py

Every check reads the graded value from the content JSON where it can, and
compares it with an exact computation (fractions or linear algebra) or a seeded
Monte Carlo run sized so the claim and its negation are several standard errors
apart. The script exits 0 when every check passes. A check that fails because
the content is wrong stays failing: it is a finding in
docs/reviews/audit-markov-4-5.md (the F-number is in the check name).
Lines marked NOTE print evidence for an `imprecise` finding and never fail.

Fix pass (Opus fixer): three checks encoded the old defects and are re-pointed
to the fixed text. F3 now checks that rejections are most common at the two
ends of the grid, as the reworded option reason says. F7 now checks the new
slip 'stay' (4/7, the share of steps that stay put) and that the equal-weight
average of the move chances is the slip 'half'. F8 now checks that 'half' is
the even split between the two venues that lead to B and that 'forward' is
the reversible reading P_BA. The two F9 checks were already correct tests and
pass once the slip values were set to what their mistakes give.
"""
import json
import math
import os
import random
import sys
from fractions import Fraction as Fr
from itertools import product

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "app", "content", "courses", "markov")
FAILS = []
COUNT = [0]


def load(name):
    with open(os.path.join(ROOT, name + ".json")) as fh:
        return json.load(fh)


def check(name, ok, detail=""):
    COUNT[0] += 1
    tag = "ok  " if ok else "FAIL"
    print(f"{tag} {name}" + (f"  [{detail}]" if detail else ""))
    if not ok:
        FAILS.append(name)


def near(a, b, tol):
    return abs(float(a) - float(b)) <= tol


def note(text):
    print("NOTE " + text)


def stationary(P):
    P = np.asarray(P, float)
    n = len(P)
    A = np.vstack([P.T - np.eye(n), np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1
    return np.linalg.lstsq(A, b, rcond=None)[0]


def balanced(P, pi, tol=1e-12):
    P = np.asarray(P, float)
    F = pi[:, None] * P
    return np.abs(F - F.T).max() < tol


def birth_death(n, up, down):
    P = np.zeros((n, n))
    for i in range(n):
        if i + 1 < n:
            P[i, i + 1] = up
        if i > 0:
            P[i, i - 1] = down
        P[i, i] = 1 - P[i].sum()
    return P


def wrongs(widget):
    return {w["id"]: w["value"] for w in widget.get("wrong", []) if "id" in w}


def return_time(P, i):
    """Exact mean return time to i by first-step analysis (not 1/pi)."""
    P = np.asarray(P, float)
    n = len(P)
    idx = [k for k in range(n) if k != i]
    A = np.eye(n - 1) - P[np.ix_(idx, idx)]
    h = np.linalg.solve(A, np.ones(n - 1))
    return 1 + sum(P[i, k] * h[j] for j, k in enumerate(idx))


def graph_P(n, edges):
    W = np.zeros((n, n))
    for u, v, w in edges:
        W[u, v] += w
        W[v, u] += w
    return W / W.sum(1, keepdims=True), W.sum(1)


# --------------------------------------------------------------------------
# Level 4, l13: reversibility and detailed balance
# --------------------------------------------------------------------------
l13 = load("l13-balanced-flows")
S = l13["screens"]
P = np.array([[0.9, 0.1], [0.2, 0.8]])
pi = stationary(P)
check("l13 s0 regime flows 100 and 100", near(1500 * pi[0] * 0.1, 100, 1e-9) and near(1500 * pi[1] * 0.2, 100, 1e-9))
check("l13 s1 backward share 1/15", near(S[1]["widget"]["answer"], pi[1] * 0.2, 5e-4))
P = birth_death(4, 0.3, 0.5)
pi = stationary(P)
check("l13 s2-s4 inventory chain: ratio 0.6, P(2 or 3) = 0.2647, reversible",
      near(pi[1] / pi[0], 0.6, 1e-9) and near(pi[2] + pi[3], S[4]["widget"]["answer"], 5e-4) and balanced(P, pi))
w = wrongs(S[4]["widget"])
check("l13 s4 slips", near(w["unscaled"], 0.576, 1e-9) and near(w["two-only"], pi[2], 5e-4) and near(w["weights-over-4"], 0.576 / 4, 1e-9))
P = birth_death(6, 0.6, 0.1)
pi = stationary(P)
check("l13 s6 drifting walker is reversible with ratio 6", balanced(P, pi) and near(pi[1] / pi[0], 6, 1e-9))
C = np.array([[0, 0.8, 0.2], [0.2, 0, 0.8], [0.8, 0.2, 0]])
pi = stationary(C)
check("l13 s7 cycle: uniform pi, flows 0.267 and 0.067, not reversible",
      np.allclose(pi, 1 / 3) and near(pi[0] * 0.8, 0.267, 1e-3) and near(pi[1] * 0.2, 0.067, 1e-3) and not balanced(C, pi))
check("l13 s8 Kolmogorov cycle product 64", near((0.8 / 0.2) ** 3, S[8]["widget"]["answer"], 1e-9))
P = birth_death(4, 0.3, 0.6)
pi = stationary(P)
check("l13 s10 queue empty 8/15", near(pi[0], S[10]["widget"]["answer"], 1e-3) and near(pi[0], 8 / 15, 1e-12))
# F1 evidence: a birth-death chain with a one-way step
B = np.array([[0.5, 0.5, 0], [0, 0.5, 0.5], [0, 0.5, 0.5]])
pib = stationary(B)
note(f"F1: line chain with P01 > 0, P10 = 0 has pi = {np.round(pib, 3)}; the formula pi1 = pi0 P01/P10 divides by zero")
P = birth_death(3, 0.2, 0.4)
check("l13 q0 4/7", near(stationary(P)[0], l13["quiz"][0]["widget"]["answer"], 1e-3))
check("l13 q3 P21 = 1/3 and slips", near(0.5 * 0.2 / 0.3, l13["quiz"][3]["widget"]["answer"], 1e-3)
      and near(wrongs(l13["quiz"][3]["widget"])["inverted"], 0.3 * 0.2 / 0.5, 1e-9))

# --------------------------------------------------------------------------
# l14: walks on networks
# --------------------------------------------------------------------------
l14 = load("l14-walks-on-networks")
S = l14["screens"]
# D=0 A=1 B=2 C=3
V = [(1, 2, 1), (1, 3, 1), (1, 0, 1), (2, 3, 1)]
P, deg = graph_P(4, V)
pi = stationary(P)
check("l14 s0-s4 venue walk: pi = deg/8, reversible, return to D is 8 by first-step solve",
      np.allclose(pi, deg / 8) and balanced(P, pi) and near(return_time(P, 0), S[4]["widget"]["answer"], 1e-9))
rng = random.Random(1)
x, visits = 0, [0] * 4
for _ in range(200000):
    x = rng.choices(range(4), weights=P[x])[0]
    visits[x] += 1
check("l14 s0 simulated shares follow degree (A 0.375, D 0.125)", near(visits[1] / 2e5, 0.375, 0.01) and near(visits[0] / 2e5, 0.125, 0.01))
P5, deg5 = graph_P(5, V + [(1, 4, 1)])
check("l14 s2 with E added, D has 1/10", near(stationary(P5)[0], S[2]["widget"]["answer"], 1e-9))
Pw, st = graph_P(3, [(0, 1, 1), (1, 2, 2), (0, 2, 3)])
check("l14 s5 weighted return to B is 4", near(return_time(Pw, 1), S[5]["widget"]["answer"], 1e-9) and st.sum() == 12)


def board(moves):
    sq = [(r, c) for r in range(8) for c in range(8)]
    ix = {s: k for k, s in enumerate(sq)}
    W = np.zeros((64, 64))
    for (r, c) in sq:
        for dr, dc in moves:
            if (r + dr, c + dc) in ix:
                W[ix[(r, c)], ix[(r + dr, c + dc)]] = 1
    return W / W.sum(1, keepdims=True), W.sum(1)


KN = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
Pk, dk = board(KN)
cells = [[int(v) for v in row] for row in S[6]["canvas"]["params"]["cells"]]
check("l14 s6 knight degree grid and total 336", np.array_equal(np.array(cells).ravel(), dk.astype(int)) and dk.sum() == 336)
check("l14 s7 knight corner return 168 by exact hitting equations", near(return_time(Pk, 0), S[7]["widget"]["answer"], 1e-6))
C4, _ = graph_P(4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)])
P1001 = np.linalg.matrix_power(C4, 1001)
check("l14 s8 square walk: P(at A at step 1001) = 0, B and D 1/2 each", near(P1001[0, 0], 0, 1e-12) and near(P1001[0, 1], 0.5, 1e-9))
St, ds = graph_P(4, [(0, 1, 1), (0, 2, 1), (0, 3, 1)])
check("l14 s9 star hub 1/2, q0 leaf return 6", near(stationary(St)[0], 0.5, 1e-9) and near(return_time(St, 1), l14["quiz"][0]["widget"]["answer"], 1e-9))
D5, d5 = graph_P(5, [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 2, 1), (2, 3, 1)])
check("l14 s11 dealer D1 share 1/3", near(d5[0] / d5.sum(), S[11]["widget"]["answer"], 1e-3))
Q2, s2 = graph_P(4, [(0, 1, 2), (1, 2, 2), (2, 3, 1), (3, 0, 1)])
check("l14 q2 weighted return to D is 6", near(return_time(Q2, 3), l14["quiz"][2]["widget"]["answer"], 1e-9))

# --------------------------------------------------------------------------
# l15: Metropolis
# --------------------------------------------------------------------------
l15 = load("l15-sampling-by-chain")
S = l15["screens"]
grid = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
w = np.array([p ** 12 * (1 - p) ** 8 for p in grid])
post = w / w.sum()


def metropolis_P(w):
    n = len(w)
    P = np.zeros((n, n))
    for i in range(n):
        for j in (i - 1, i + 1):
            if 0 <= j < n:
                P[i, j] = 0.5 * min(1, w[j] / w[i])
        P[i, i] = 1 - P[i].sum()
    return P


PM = metropolis_P(w)
check("l15 s0 acceptance 0.898 and slips", near(w[5] / w[4], S[0]["widget"]["answer"], 2e-3)
      and near(wrongs(S[0]["widget"])["inverse"], w[4] / w[5], 2e-3) and near(wrongs(S[0]["widget"])["half"], 0.5 * w[5] / w[4], 2e-3))
check("l15 s1 canvas matrix is the Metropolis chain", np.abs(np.array(S[1]["canvas"]["params"]["P"]) - PM).max() < 6e-5)
check("l15 s3 chain is reversible for the posterior", balanced(PM, post) and np.allclose(stationary(PM), post))
stay = np.diag(PM)
why_done = next(o["why"] for o in S[1]["widget"]["options"] if o["id"] == "done")
check("F3 l15 s1 rejections are most common at the two ends of the grid, as the option reason says",
      stay[0] == stay.max() and stay[-1] == stay.max() and stay[4] == stay.min() and "two ends" in why_done,
      f"stay chances {np.round(stay, 3)}; lowest at the peak")
d = np.zeros(7)
d[0] = 1
at0, tv = [], []
for k in range(0, 201):
    at0.append(d[0])
    tv.append(0.5 * np.abs(d - post).sum())
    d = d @ PM
first = next(k for k in range(201) if at0[k] < 0.06)
check("l15 s2 burn-in numbers: 0.187 at k=5, 0.099 at k=10, first below 0.06 at 18 (give or take 1)",
      near(at0[5], 0.187, 1e-3) and near(at0[10], 0.099, 1e-3) and abs(first - S[2]["widget"]["answer"]) <= 1, f"first k = {first}")
note(f"F4: at k=18 bar {at0[18]:.4f} against target {post[0]:.4f}; total variation distance {tv[18]:.4f} at k=18, "
     f"{tv[20]:.4f} at k=20, {tv[40]:.4f} at k=40 (never exactly 0)")
Pacc = np.zeros((7, 7))
for i in range(7):
    for j in (i - 1, i + 1):
        if 0 <= j < 7:
            Pacc[i, j] = 0.5
    Pacc[i, i] = 1 - Pacc[i].sum()
check("l15 s4 always accepting gives uniform shares", np.allclose(stationary(Pacc), 1 / 7))
rng = random.Random(5)
x, rec, full = 0, [], []
for _ in range(200000):
    y = 1 - x
    if rng.random() < min(1, [1, 3][y] / [1, 3][x]):
        x = y
        rec.append(x)
    full.append(x)
check("l15 s5 two-state chain samples 3/4 at H; moves-only record gives 1/2",
      near(sum(full) / len(full), 0.75, 0.01) and near(sum(rec) / len(rec), S[5]["widget"]["answer"], 0.01))
check("l15 s6 posterior mean 0.578", near(post @ np.array(grid), 0.578, 5e-4))
check("l15 s7 Hastings 9/14 and slips", near(3 * 0.3 / (2 * 0.7), S[7]["widget"]["answer"], 2e-3)
      and near(wrongs(S[7]["widget"])["q-only"], 0.3 / 0.7, 1e-3) and near(wrongs(S[7]["widget"])["flip"], 3 * 0.7 / (2 * 0.3), 1e-3))


def metropolis(weights, steps, seed, start):
    rng = random.Random(seed)
    k = len(weights)
    state = start
    visits = [0] * k
    for _ in range(steps):
        proposal = state + (1 if rng.random() < 0.5 else -1)
        if 0 <= proposal < k:
            if rng.random() < min(1, weights[proposal] / weights[state]):
                state = proposal
        visits[state] += 1
    return [v / steps for v in visits]


errs = [max(abs(a - b) for a, b in zip(metropolis(list(w), 100000, s, 0), post)) for s in range(1, 9)]
check("l15 s8 100,000 steps agree with the posterior 'to about 0.003' (mean max error over 8 seeds within 0.001 to 0.008)",
      0.001 < np.mean(errs) < 0.008, f"mean {np.mean(errs):.4f}")
bars = [S[9]["canvas"]["state"]["values"][k] for k in ("p3", "p4", "p5", "p6")]
check("l15 s9 P(p > 0.5): exact 0.7301, bars 0.7296, slips", near(post[3:].sum(), S[9]["widget"]["answer"], 1e-4) and near(sum(bars), 0.7296, 1e-4)
      and near(wrongs(S[9]["widget"])["with-half"], sum(bars) + 0.1426, 1e-3) and near(wrongs(S[9]["widget"])["top-two"], 0.191 + 0.136, 1e-3))
check("l15 s9 'the chain moved on 79% of its steps'", near(1 - post @ stay, 0.79, 0.005), f"{1 - post @ stay:.4f}")
check("l15 q2 5/8, q3 1/3", near(5 / 8, l15["quiz"][2]["widget"]["answer"], 1e-9) and near(0.25 / 0.75, l15["quiz"][3]["widget"]["answer"], 1e-3))

# --------------------------------------------------------------------------
# l16: Poisson process (exact values, then Monte Carlo of each structural fact)
# --------------------------------------------------------------------------
l16 = load("l16-arrivals")
S = l16["screens"]


def pois(k, m):
    return math.exp(-m) * m ** k / math.factorial(k)


vals = S[0]["canvas"]["params"]["series"][0]["values"]
empty = sum(1 for m in range(10) if vals[20 * (m + 1)] == vals[20 * m])
check("l16 s0 one empty minute in the seeded staircase", empty == S[0]["widget"]["answer"])
check("l16 s1 e^-2 and slips", near(pois(0, 2), S[1]["widget"]["answer"], 5e-4) and near(wrongs(S[1]["widget"])["gap"], math.exp(-0.5), 5e-4))
check("l16 s2 P(N(3)=5) = 0.1606 and slips", near(pois(5, 6), S[2]["widget"]["answer"], 5e-4)
      and near(wrongs(S[2]["widget"])["one-minute"], pois(5, 2), 5e-4) and near(wrongs(S[2]["widget"])["three-times"], 3 * pois(5, 2), 5e-4))
check("l16 s6 no buys in 2 minutes e^-6 and slips", near(math.exp(-6), S[6]["widget"]["answer"], 3e-4)
      and near(wrongs(S[6]["widget"])["five-rate"], math.exp(-10), 1e-6) and near(wrongs(S[6]["widget"])["sells"], math.exp(-4), 1e-4))
rs = np.random.default_rng(16)
M = 400000
# superposition: independent Exp(3) and Exp(2) waits
tb, ts = rs.exponential(1 / 3, M), rs.exponential(1 / 2, M)
check("l16 s4/s5 MC: next order is a buy with chance 3/5; first order of either kind has rate 5",
      near((tb < ts).mean(), 0.6, 0.004) and near(np.minimum(tb, ts).mean(), 0.2, 0.002))
# thinning: orders at rate 5 per minute, each a buy w.p. 0.6
n = rs.poisson(5, M)
buys = rs.binomial(n, 0.6)
sells = n - buys
check("l16 s6/s7 MC thinning: buys ~ Poisson(3), sells ~ Poisson(2), correlation 0 (a fixed total of 5 would give -1)",
      near(buys.mean(), 3, 0.02) and near(buys.var(), 3, 0.05) and near((sells == 0).mean(), math.exp(-2), 0.003)
      and abs(np.corrcoef(buys, sells)[0, 1]) < 0.01, f"corr {np.corrcoef(buys, sells)[0, 1]:+.4f}")
hi, lo = sells[buys >= 5], sells[buys == 0]
check("l16 s7 MC: sells given 5+ buys and given 0 buys both match Poisson(2) at 0 sells (13.5%)",
      near((hi == 0).mean(), 0.1353, 0.006) and near((lo == 0).mean(), 0.1353, 0.01))
# memorylessness and the inspection paradox
g = rs.exponential(0.5, M)
check("l16 MC memorylessness: P(gap > 1.5 | gap > 0.5) = P(gap > 1) = e^-2", near((g[g > 0.5] > 1.5).mean(), math.exp(-2), 0.004))


def covering_gap(t, reps, rs):
    out = np.empty(reps)
    age = np.empty(reps)
    for r in range(reps):
        s, last = 0.0, 0.0
        while True:
            x = rs.exponential(0.5)
            if s + x > t:
                out[r] = (s + x) - last
                age[r] = t - last
                break
            s += x
            last = s
    return out.mean(), age.mean()


cg, ag = covering_gap(10.0, 40000, rs)
check("l16 s8 MC inspection paradox: gap covering t=10 has mean 1 (typical gap 0.5)", near(cg, S[8]["widget"]["answer"], 0.02), f"{cg:.3f}")
cg2, ag2 = covering_gap(0.5, 40000, rs)
note(f"F5: at t = 0.5 minutes the time since the last trade has mean {ag2:.3f} (formula (1-e^-1)/2 = {(1 - math.exp(-1)) / 2:.3f}), "
     f"not 0.5, and the covering gap {cg2:.3f}; at t = 10 the age is {ag:.3f}")
# uniform arrival given exactly one in 10 minutes (any rate; rate 0.3 used so N=1 is common)
hits = tot = 0
for _ in range(200000):
    t1 = rs.exponential(1 / 0.3)
    if t1 < 10 and t1 + rs.exponential(1 / 0.3) > 10:
        tot += 1
        hits += t1 < 2
check("l16 q1 MC: given one arrival in 10 minutes, P(in first 2) = 0.2", near(hits / tot, l16["quiz"][1]["widget"]["answer"], 0.006), f"{hits / tot:.4f} over {tot}")
wq = wrongs(l16["quiz"][1]["widget"])
note(f"F6: l16 q1 slips {wq['at-least-one']} and {wq['empty']} equal 1-e^-4 and e^-2 only at rate 2, which the item does not state")
seq = rs.random((M, 3)) < 0.6
check("l16 s10 MC: next three fills all buys 0.216", near(seq.all(1).mean(), S[10]["widget"]["answer"], 0.003))
check("l16 q0, q2, q3", near(math.exp(-1), l16["quiz"][0]["widget"]["answer"], 1e-4) and l16["quiz"][2]["widget"]["answer"] == 4 * 10 + 50
      and near(math.exp(-5), l16["quiz"][3]["widget"]["answer"], 1e-4))

# --------------------------------------------------------------------------
# review-4, homework-4, problems-4
# --------------------------------------------------------------------------
r4 = load("review-4")["items"]
P = birth_death(3, 0.4, 0.2)
check("review-4 i0 4/7", near(stationary(P)[2], r4[0]["widget"]["answer"], 1e-3))
Pr, sr = graph_P(4, [(0, 1, 2), (0, 2, 1), (1, 2, 1), (2, 3, 3)])
check("review-4 i1 return to C 2.8", near(return_time(Pr, 2), r4[1]["widget"]["answer"], 1e-9))
check("review-4 i2 0.7402", near(w[2] / w[3], r4[2]["widget"]["answer"], 3e-3))
check("review-4 i3 e^-4 = 0.0183", near(pois(1, 1) * pois(0, 3), r4[3]["widget"]["answer"], 1e-4))
P4 = np.array([[0.5, 0.5, 0], [0.25, 0.5, 0.25], [0, 0.25, 0.75]])
check("review-4 i4 reversible with pi (0.2, 0.4, 0.4)", np.allclose(stationary(P4), [0.2, 0.4, 0.4]) and balanced(P4, stationary(P4)))
w3 = np.array([1.0, 2, 4])
P3 = metropolis_P(w3)
move = 1 - np.diag(P3)
check("review-4 i6 share of steps that move 3/7", near((w3 / 7) @ move, r4[6]["widget"]["answer"], 1e-3))
w6 = wrongs(r4[6]["widget"])
check("F7 review-4 i6 slip 'stay' is the share of steps that stay put, 4/7, and 'half' is the equal-weight average",
      "third" not in w6 and near(w6["stay"], (w3 / 7) @ np.diag(P3), 1e-3) and near(w6["stay"], 4 / 7, 1e-3)
      and near(w6["half"], move.mean(), 1e-3), f"stay share {(w3 / 7) @ np.diag(P3):.4f}, equal-weight average {move.mean():.4f}")
key7 = pois(2, 6) * pois(1, 4)
check("review-4 i7 key 0.00327 and the binomial identity", near(key7, r4[7]["widget"]["answer"], 1e-4)
      and near(key7, pois(3, 10) * 3 * 0.36 * 0.4, 1e-12))
w7 = wrongs(r4[7]["widget"])
check("F9 review-4 i7 slip 'one-minute' equals P(2 buys; mean 3) x P(1 sell; mean 2)", near(w7["one-minute"], pois(2, 3) * pois(1, 2), 1e-3),
      f"content {w7['one-minute']}, computed {pois(2, 3) * pois(1, 2):.4f}")
check("F9 review-4 i7 slip 'sum' equals the two chances added", near(w7["sum"], pois(2, 6) + pois(1, 4), 1e-3),
      f"content {w7['sum']}, computed {pois(2, 6) + pois(1, 4):.4f}")
check("review-4 i7 slip 'merged' = P(N=3; mean 10)", near(w7["merged"], pois(3, 10), 5e-4))

h4 = load("homework-4")["items"]
KG = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
Pg, dg = board(KG)
check("homework-4 i0 king: total degree 420, corner return 140 by hitting equations", dg.sum() == 420 and near(return_time(Pg, 0), h4[0]["widget"]["answer"], 1e-6))
pi = stationary(C)
back = pi[0] * C[0, 1] / pi[1]
check("homework-4 i2 P(A yesterday | B today) = 0.8", near(back, h4[2]["widget"]["answer"], 1e-9))
w2 = wrongs(h4[2]["widget"])
fb2 = h4[2]["feedback"]["byKey"]
check("F8 homework-4 i2 slip 'half' is the even split between A and C, and 'forward' is the reversible reading P_BA",
      C[0, 1] > 0 and C[2, 1] > 0 and C[1, 1] == 0 and near(w2["half"], 1 / 2, 1e-9) and near(w2["forward"], C[1, 0], 1e-9)
      and "evenly" in fb2["half"] and "reversible" in fb2["forward"],
      f"reversible reading gives P_BA = {C[1, 0]}, the slip 'forward'")
check("homework-4 i4 Bin(4,0.6) at 3 = 0.3456; sells mean 6", near(4 * 0.6 ** 3 * 0.4, h4[4]["widget"]["rows"][0][1]["answer"], 1e-6)
      and h4[4]["widget"]["rows"][1][1]["answer"] == 6)
nb = rs.poisson(9, M)
ns = rs.poisson(6, M)
check("homework-4 i4 MC: mean sells in 3 minutes given exactly 7 buys is 6", near(ns[nb == 7].mean(), 6, 0.05))
u = rs.uniform(0, 3, (M, 3)).min(1)
check("homework-4 i5 19/27", near((u < 1).mean(), h4[5]["widget"]["answer"], 0.003) and near(19 / 27, h4[5]["widget"]["answer"], 1e-4))
marks = rs.random((M, 40)) < 0.6          # True = buy
sell_no = np.cumsum(~marks, 1)
third = (sell_no == 3).argmax(1)           # index of the third sell
check("homework-4 i6 MC: exactly 2 buys before the third sell 0.13824", near((third == 4).mean(), h4[6]["widget"]["answer"], 0.003), f"{(third == 4).mean():.4f}")
# homework-4 i8 model answer numbers
jump = post * (1 - stay)
jump = jump / jump.sum()
ref = [0.027, 0.081, 0.145, 0.212, 0.243, 0.207, 0.086]
check("homework-4 i8 moves-only shares, mean 0.5764 and P(p>0.5) 0.747", np.abs(jump - ref).max() < 6e-4 and near(jump @ np.array(grid), 0.5764, 2e-4)
      and near(jump[3:].sum(), 0.747, 1e-3))
d = np.zeros(7)
d[0] = 1
means = []
for k in range(200):
    d = d @ PM
    means.append(d @ np.array(grid))
check("homework-4 i8 first 200 steps from 0.40 average 0.5721; after dropping 20 steps 0.5776",
      near(np.mean(means), 0.5721, 2e-4) and near(np.mean(means[20:]), 0.5776, 2e-4), f"{np.mean(means):.4f}, {np.mean(means[20:]):.4f}")
rng = random.Random(8)
pool, pool20 = [], []
gridv = grid
for rep in range(300):
    tot = tot20 = 0.0
    for c in range(20):
        x = 0
        for t in range(200):
            y = x + (1 if rng.random() < 0.5 else -1)
            if 0 <= y < 7 and rng.random() < min(1, w[y] / w[x]):
                x = y
            tot += gridv[x]
            if t >= 20:
                tot20 += gridv[x]
    pool.append(tot / 4000)
    pool20.append(tot20 / 3600)
check("homework-4 i8 MC: sd of the pooled mean about 0.004 (all steps) and about 0.005 (first 20 dropped), each within 0.003 to 0.006",
      0.003 < np.std(pool) < 0.006 and 0.003 < np.std(pool20) < 0.006, f"{np.std(pool):.4f}, {np.std(pool20):.4f}")

p4 = load("problems-4")["items"]
# i0: H=0 A=1 B=2 C=3 D=4
E0 = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 2, 1)]
Pa, da = graph_P(5, E0)
MH = np.zeros((5, 5))
SQ = np.zeros((5, 5))
for i in range(5):
    for j in range(5):
        if Pa[i, j] > 0:
            MH[i, j] = Pa[i, j] * min(1, da[i] / da[j])
            SQ[i, j] = Pa[i, j] / da[i]
    MH[i, i] = 1 - MH[i].sum()
    SQ[i, i] = 1 - SQ[i].sum()
check("problems-4 i0: pi_C 0.1; corrected walk uniform; stay at C 0.75; repeats 0.4; accept 1/deg(i) gives H 16/26",
      near(stationary(Pa)[3], 0.1, 1e-9) and np.allclose(stationary(MH), 0.2) and near(MH[3, 3], p4[0]["parts"][3]["widget"]["answer"], 1e-9)
      and near(np.diag(MH).mean(), p4[0]["parts"][4]["widget"]["answer"], 1e-9) and near(stationary(SQ)[0], 16 / 26, 1e-9))
P = birth_death(4, 0.6, 0.4)
pi4 = stationary(P)
P5b = birth_death(5, 0.6, 0.4)
check("problems-4 i1 taxi rank: pi0 8/65, 11.8154 lost an hour; with a fourth space 7.2796",
      near(pi4[0], 8 / 65, 1e-12) and near(96 * pi4[0], p4[1]["parts"][3]["widget"]["answer"], 1e-3)
      and near(96 * stationary(P5b)[0], p4[1]["parts"][4]["widget"]["answer"], 1e-3))
# continuous-time simulation of the rank: do passengers see the embedded chain's pi0?
rng = random.Random(4)
lvl, lost, pax = 0, 0, 0
for _ in range(600000):
    if rng.random() < 0.6:
        lvl = min(3, lvl + 1)
    else:
        pax += 1
        if lvl == 0:
            lost += 1
        else:
            lvl -= 1
check("problems-4 i1 MC: share of passengers who find the rank empty is 8/65 = 0.1231", near(lost / pax, 8 / 65, 0.003), f"{lost / pax:.4f}")
E2 = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1)]
Pb, db = graph_P(6, E2)
check("problems-4 i2: pi_D 3/14, return to F 14, audits 8/7, e^(-8/7), 17 hours",
      near(stationary(Pb)[3], 3 / 14, 1e-9) and near(return_time(Pb, 5), 14, 1e-9) and near(8 / 7, p4[2]["parts"][2]["widget"]["answer"], 1e-4)
      and near(math.exp(-8 / 7), p4[2]["parts"][3]["widget"]["answer"], 1e-4) and math.ceil(7 * math.log(10)) == p4[2]["parts"][4]["widget"]["answer"])
wv = np.array([2.0, 5, 3])
q = np.array([[0, 1, 0], [0.3, 0, 0.7], [0, 1, 0]])
H3 = np.zeros((3, 3))
PL = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        if q[i, j] > 0:
            H3[i, j] = q[i, j] * min(1, wv[j] * q[j, i] / (wv[i] * q[i, j]))
            PL[i, j] = q[i, j] * min(1, wv[j] / wv[i])
    H3[i, i] = 1 - H3[i].sum()
    PL[i, i] = 1 - PL[i].sum()
check("problems-4 i3: Hastings chain 0.75, 0.6, 0.3, targets (0.2,0.5,0.3), rejections 0.1; plain rule gives Mid 50/77",
      near(H3[0, 1], 0.75, 1e-9) and near(H3[1, 2], 0.6, 1e-9) and near(H3[1, 0], 0.3, 1e-9) and np.allclose(stationary(H3), [0.2, 0.5, 0.3])
      and near(stationary(H3) @ np.diag(H3), 0.1, 1e-9) and near(stationary(PL)[1], p4[3]["parts"][4]["widget"]["answer"], 1e-4))

# --------------------------------------------------------------------------
# Level 5, l17 and l18: martingales (exact one-step checks)
# --------------------------------------------------------------------------
l17 = load("l17-fair-bets")
S = l17["screens"]
check("l17 s1 13.2, s4 4/9, s6 -1/37, s11 20", near(0.6 * 14 + 0.4 * 12, S[1]["widget"]["answer"], 1e-9) and near(Fr(4, 9), S[4]["widget"]["answer"], 1e-4)
      and near(-1 / 37, S[6]["widget"]["answer"], 1e-3) and near((40 - 0.4 * 70) / 0.6, S[11]["widget"]["answer"], 1e-9))
# forecaster tree and Polya urn
f = {s: Fr(sum(1 for t in product("HT", repeat=3 - len(s)) if (s + "".join(t)).count("H") >= 2), 2 ** (3 - len(s))) for s in ["", "H", "T", "HH", "HT", "TH", "TT"]}
check("l17 s5 forecasts 3/4, 1/4, 1, 1/2, 1/2, 0 and each averages to the one before",
      [f[s] for s in ["H", "T", "HH", "HT", "TH", "TT"]] == [Fr(3, 4), Fr(1, 4), 1, Fr(1, 2), Fr(1, 2), 0]
      and all(f[s] == (f[s + "H"] + f[s + "T"]) / 2 for s in ["", "H", "T"]))
dist = {(1, 1): Fr(1)}
ok_urn = True
for _ in range(3):
    new = {}
    for (r, b), pr in dist.items():
        share = Fr(r, r + b)
        nxt = share * Fr(r + 1, r + b + 1) + (1 - share) * Fr(r, r + b + 1)
        ok_urn &= nxt == share
        new[(r + 1, b)] = new.get((r + 1, b), 0) + pr * share
        new[(r, b + 1)] = new.get((r, b + 1), 0) + pr * (1 - share)
    dist = new
check("l17 s8 Polya urn share is a martingale; after three draws 1/5..4/5 with chance 1/4 each",
      ok_urn and sorted((Fr(r, r + b), pr) for (r, b), pr in dist.items()) == [(Fr(k, 5), Fr(1, 4)) for k in range(1, 5)])
note("F11: l17 q3 slip 5 solves 0.2x = 1; dropping the chances (3 + 1 + x = 2) gives -2 and an equal average ((3 + 1 + x)/3 = 2) gives 2")


def drift(f, s, n, p):
    p = Fr(p)
    return p * f(s + 1, n + 1) + (1 - p) * f(s - 1, n + 1) - f(s, n)


def mart(f, p):
    return all(drift(f, s, n, p) == 0 for s in range(-6, 7) for n in range(0, 6))


p6 = Fr(3, 5)
check("l18 exact: S^2-n, S^3-3nS fair for p=1/2; S-0.2n, (S-0.2n)^2-0.96n, (2/3)^S fair for p=0.6; S^2 and (3/2)^S are not",
      mart(lambda s, n: s * s - n, Fr(1, 2)) and mart(lambda s, n: s ** 3 - 3 * n * s, Fr(1, 2)) and mart(lambda s, n: s - n * Fr(1, 5), p6)
      and mart(lambda s, n: (s - n * Fr(1, 5)) ** 2 - Fr(24, 25) * n, p6) and mart(lambda s, n: Fr(2, 3) ** s, p6)
      and not mart(lambda s, n: s * s, Fr(1, 2)) and drift(lambda s, n: Fr(3, 2) ** s, 0, 0, p6) == Fr(1, 6))
l18 = load("l18-hidden-martingales")
check("l18 s5 (7/6)^10 = 4.6716; s1 sd of S_100^2 about 141; s9 sd 5000", near((7 / 6) ** 10, 4.6716, 1e-4) and near(math.sqrt(2 * 100 * 100 - 2 * 100), 141, 0.5)
      and l18["screens"][9]["widget"]["answer"] == 1000 * math.sqrt(25))

# --------------------------------------------------------------------------
# l19: optional stopping against first-step linear solves
# --------------------------------------------------------------------------


def ruin_exact(i, N, p):
    """(chance of N before 0, expected steps) from first-step equations, exact."""
    p = Fr(p)
    q = 1 - p
    n = N - 1
    A = [[Fr(0)] * n for _ in range(n)]
    for k in range(1, N):
        A[k - 1][k - 1] = Fr(1)
        if k + 1 < N:
            A[k - 1][k] = -p
        if k - 1 > 0:
            A[k - 1][k - 2] = -q
    def solve(b):
        Mx = [row[:] + [bv] for row, bv in zip(A, b)]
        for c in range(n):
            piv = next(r for r in range(c, n) if Mx[r][c] != 0)
            Mx[c], Mx[piv] = Mx[piv], Mx[c]
            Mx[c] = [v / Mx[c][c] for v in Mx[c]]
            for r in range(n):
                if r != c and Mx[r][c] != 0:
                    Mx[r] = [a - Mx[r][c] * bb for a, bb in zip(Mx[r], Mx[c])]
        return [row[-1] for row in Mx]
    h = solve([p if k == N - 1 else Fr(0) for k in range(1, N)])
    t = solve([Fr(1)] * n)
    return h[i - 1], t[i - 1]


def ruin_mart(i, N, p):
    p = Fr(p)
    q = 1 - p
    if p == q:
        return Fr(i, N), Fr(i * (N - i))
    r = q / p
    win = (1 - r ** i) / (1 - r ** N)
    return win, (N * win - i) / (p - q)


cases = [(3, 10, Fr(1, 2)), (2, 5, Fr(1, 2)), (2, 4, Fr(3, 5)), (5, 10, Fr(2, 5)), (3, 10, Fr(3, 5)), (4, 10, Fr(11, 20)), (2, 4, Fr(9, 20)), (3, 5, Fr(9, 20)), (6, 20, Fr(1, 2)), (4, 12, Fr(1, 2))]
check("l19 optional-stopping formulas equal the exact first-step solutions in 10 cases", all(ruin_exact(*c) == ruin_mart(*c) for c in cases))
l19 = load("l19-optional-stopping")
S = l19["screens"]
check("l19 keys: 3/10, 21, 32/275, 50/13, 9/13", near(ruin_mart(3, 10, Fr(1, 2))[0], S[1]["widget"]["answer"], 1e-9) and ruin_mart(3, 10, Fr(1, 2))[1] == S[4]["widget"]["answer"]
      and near(ruin_mart(5, 10, Fr(2, 5))[0], S[5]["widget"]["answer"], 1e-4) and near(ruin_mart(2, 4, Fr(3, 5))[1], S[6]["widget"]["answer"], 1e-3)
      and ruin_mart(5, 10, Fr(2, 5)) == (Fr(32, 275), Fr(211, 11)) and ruin_mart(3, 10, Fr(3, 5)) == (Fr(41553, 58025), Fr(48291, 2321)))
w49, t49 = ruin_mart(50, 100, Fr(49, 100))
check("l19 s6/s9 p=0.49 from 50 of 100: chance 0.1192, about 1,904.1 bets, 10P = stopped mean", near(w49, 0.1192, 1e-4) and near(t49, 1904.1, 0.1))
rs = np.random.default_rng(19)
tot = 0
G = 200000
for _ in range(G):
    while True:
        r = rs.integers(1, 7)
        tot += r
        if r == 6:
            break
check("l19 s7 MC Wald: total of die rolls up to the first 6 averages 21 (3.5 alone would be 3.5, six sixes 36)", near(tot / G, S[7]["widget"]["answer"], 0.15), f"{tot / G:.3f}")
# quiz 3: independent P&L with mean 30, stop after the first loser (chance 0.2): winners +50, losers -50
pl = 0.0
for _ in range(G):
    while True:
        if rs.random() < 0.2:
            pl -= 50
            break
        pl += 50
check("l19 q3 MC Wald with a stop at the first loss: mean total 150 (not 120)", near(pl / G, l19["quiz"][3]["widget"]["answer"], 2.5), f"{pl / G:.2f}")
check("l19 s11 stop and target: 2/3, 8 trades, P&L 0", ruin_mart(4, 6, Fr(1, 2)) == (Fr(2, 3), 8) and Fr(2, 3) * 2000 - Fr(1, 3) * 4000 == 0)

# --------------------------------------------------------------------------
# l20: when stopping fails
# --------------------------------------------------------------------------
l20 = load("l20-when-stopping-fails")
S = l20["screens"]


def stop_when_up_exact(max_steps, floor=None):
    dist = {0: Fr(1)}
    reached = Fr(0)
    done = Fr(0)
    tsum = Fr(0)
    for k in range(1, max_steps + 1):
        new = {}
        for s, pr in dist.items():
            for t in (s + 1, s - 1):
                if t == 1:
                    reached += pr / 2
                    tsum += k * pr / 2
                elif floor is not None and t == floor:
                    done += pr / 2 * t
                    tsum += k * pr / 2
                else:
                    new[t] = new.get(t, 0) + pr / 2
        dist = new
    mean = reached + done + sum(s * pr for s, pr in dist.items())
    tmean = tsum + max_steps * sum(dist.values())
    return reached, mean, dist, tmean


r100, m100, d100, _ = stop_when_up_exact(100)
fail = 1 - r100
cond = sum(s * pr for s, pr in d100.items()) / fail
check("l20 s4 cap at 100 bets: E[S_T] = 0 exactly, P(fail) = C(100,50)/2^100 = 0.0796, mean when failing -11.56",
      m100 == 0 and fail == Fr(math.comb(100, 50), 2 ** 100) and near(fail, S[4]["widget"]["rows"][0][1]["answer"], 1e-4) and near(cond, S[4]["widget"]["rows"][1][1]["answer"], 0.01))
check("l20 s1/s2 floor at -9: chance 0.9, mean 0, E[T] = 9", ruin_mart(9, 10, Fr(1, 2)) == (Fr(9, 10), 9))
check("l20 no floor: E[S_T at +1] is 1 while every capped version has mean 0 (caps 1..60)", all(stop_when_up_exact(n)[1] == 0 for n in range(1, 61)))
_, m99, _, t99 = stop_when_up_exact(1000, floor=-99)
note(f"l20 s2: with the floor at -99 the chart's 1,000-step window shows E[min(T, 1000)] = {float(t99):.1f}, not 99 (the text reports about 40)")
check("l20 s2 'about 40 at L = 99' is what a 1,000-step window shows on average (30 to 50)", 30 < float(t99) < 50 and m99 == 0)


def doubling(d, p):
    p = Fr(p)
    return (1 - (1 - p) ** d) - (1 - p) ** d * (2 ** d - 1)


# brute force over all win/lose sequences for d = 10
def doubling_brute(d, p):
    p = Fr(p)
    ev = Fr(0)
    for k in range(1, d + 1):          # first win on bet k
        ev += (1 - p) ** (k - 1) * p * (2 ** (k - 1) - (2 ** (k - 1) - 1))
    ev -= (1 - p) ** d * (2 ** d - 1)
    return ev


check("l20 s5/s6 doubling: fair 0, red -0.3056 (branch sum agrees), d=7 -0.2052; sd of a fair cycle about 32",
      doubling(10, Fr(1, 2)) == 0 and near(doubling(10, Fr(18, 37)), S[6]["widget"]["answer"], 1e-4) and doubling(10, Fr(18, 37)) == doubling_brute(10, Fr(18, 37))
      and near(doubling(7, Fr(18, 37)), -0.2052, 1e-4) and near(math.sqrt(1023 / 1024 + 1023 ** 2 / 1024), 32, 0.1))
check("l20 s7 unlimited doubling: E[T] = 2 and partial sums of E[last stake] grow without bound (each term is 1/2)",
      near(sum(k * 0.5 ** k for k in range(1, 200)), 2, 1e-9) and all(Fr(1, 2) ** k * 2 ** (k - 1) == Fr(1, 2) for k in range(1, 40)))
rv = load("review-5")["items"]
check("review-5 i5 doubling at p=0.48, 8 bets: -0.3686", near(doubling(8, Fr(12, 25)), rv[5]["widget"]["answer"], 1e-4))

# --------------------------------------------------------------------------
# l21: pattern waits: exact first-step solve (automaton) against the casino rule, then Monte Carlo
# --------------------------------------------------------------------------


def casino(pattern, probs):
    total = Fr(0)
    for k in range(1, len(pattern) + 1):
        if pattern[:k] == pattern[-k:]:
            c = Fr(1)
            for ch in pattern[:k]:
                c *= probs[ch]
            total += 1 / c
    return total


def first_step_wait(pattern, probs):
    """Exact expected wait from the prefix automaton, by Gaussian elimination in fractions."""
    m = len(pattern)
    letters = list(probs)

    def nxt(state, ch):
        s = pattern[:state] + ch
        while s and not pattern.startswith(s):
            s = s[1:]
        return len(s)
    A = [[Fr(0)] * (m + 1) for _ in range(m)]
    for st in range(m):
        A[st][st] += 1
        A[st][m] = Fr(1)
        for ch in letters:
            t = nxt(st, ch)
            if t < m:
                A[st][t] -= probs[ch]
    for c in range(m):
        piv = next(r for r in range(c, m) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        A[c] = [v / A[c][c] for v in A[c]]
        for r in range(m):
            if r != c and A[r][c] != 0:
                A[r] = [a - A[r][c] * b for a, b in zip(A[r], A[c])]
    return A[0][m]


fair = {"H": Fr(1, 2), "T": Fr(1, 2)}
b6 = {"H": Fr(3, 5), "T": Fr(2, 5)}
b23 = {"H": Fr(2, 3), "T": Fr(1, 3)}
LW4 = {"L": Fr(2, 5), "W": Fr(3, 5)}
LW3 = {"L": Fr(3, 10), "W": Fr(7, 10)}
pats = [("H", fair, 2), ("HT", fair, 4), ("HH", fair, 6), ("HHT", fair, 8), ("HTH", fair, 10), ("THT", fair, 10), ("HHH", fair, 14), ("HTHH", fair, 18),
        ("HTHT", fair, 20), ("HHHH", fair, 30), ("HH", b23, Fr(15, 4)), ("LLL", LW4, Fr(195, 8)), ("HT", b6, Fr(25, 6)), ("HHH", b6, None),
        ("HTH", b6, Fr(155, 18)), ("LL", LW3, Fr(130, 9)), ("LWL", LW3, None)]
check("l21 casino rule equals the exact first-step wait for 17 patterns, with the stated values",
      all(casino(p, pr) == first_step_wait(p, pr) and (v is None or casino(p, pr) == v) for p, pr, v in pats))
abc = {c: Fr(1, 26) for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
ab = first_step_wait("ABRACADABRA", abc)
check("l21 s7 ABRACADABRA: exact first-step solve gives 26^11 + 26^4 + 26 = 3,670,344,487,444,778", ab == 26 ** 11 + 26 ** 4 + 26 == 3670344487444778)
note("F12: l21 s7 says gamblers bet 'at odds of 26 to 1'; a fair bet on a 1-in-26 letter returns 26 for 1, which is odds of 25 to 1. "
     f"At 26 to 1 (27 for 1) the rule would give {27 ** 11 + 27 ** 4 + 27:,}")
rs = np.random.default_rng(21)


def sim_wait(pat, p, games):
    tot = 0
    for _ in range(games):
        s = ""
        n = 0
        while not s.endswith(pat):
            s = (s + ("H" if rs.random() < p else "T"))[-len(pat):]
            n += 1
        tot += n
    return tot / games


a, b = sim_wait("HTH", 0.5, 60000), sim_wait("HHT", 0.5, 60000)
check("l21 MC: HTH waits 10 and HHT waits 8 (60,000 games each; standard error under 0.04)", near(a, 10, 0.15) and near(b, 8, 0.12), f"{a:.3f}, {b:.3f}")
l21 = load("l21-waiting-for-patterns")
check("l21 keys: s3 10, s5 14, s6 3.75, s10 24.375, q3 4.1667", l21["screens"][3]["widget"]["answer"] == 10 and l21["screens"][5]["widget"]["answer"] == 14
      and l21["screens"][6]["widget"]["answer"] == 3.75 and l21["screens"][10]["widget"]["answer"] == 24.375 and near(casino("HT", b6), l21["quiz"][3]["widget"]["answer"], 1e-4))
check("review-5 i6 HTHH 18, i7 HHH at 0.6 = 9.07", rv[6]["widget"]["answer"] == 18 and near(casino("HHH", b6), rv[7]["widget"]["answer"], 5e-3))

# --------------------------------------------------------------------------
# l22: compensated and compound Poisson
# --------------------------------------------------------------------------
l22 = load("l22-arrivals-fair-game")
S = l22["screens"]
rs = np.random.default_rng(22)
M = 400000
n3 = rs.poisson(6, M)
inc = rs.poisson(4, M)
sel = n3 == 4
n5 = n3[sel] + inc[sel]
check("l22 s0/s1 MC: E[N5 | N3 = 4] = 8 and E[N5 - 10 | N3 = 4] = -2", near(n5.mean(), S[0]["widget"]["answer"], 0.03) and near((n5 - 10).mean(), -2, 0.03))
check("l22 s3 MC: E[(N5 - 10)^2 | N3 = 4] = 8 (4 would ignore the new trades)", near(((n5 - 10.0) ** 2).mean(), S[3]["widget"]["answer"], 0.12), f"{((n5 - 10.0) ** 2).mean():.3f}")
t3 = rs.exponential(0.5, (M, 3)).sum(1)
check("l22 s4 MC: E[T_3] = 1.5 and E[N_T3 - 2 T_3] = 0", near(t3.mean(), S[4]["widget"]["answer"], 0.01) and near((3 - 2 * t3).mean(), 0, 0.02))
sizes, pr = np.array([100, 200, 500]), [0.5, 0.3, 0.2]
ey, ey2 = float(sizes @ pr), float(sizes ** 2 @ pr)
rows = S[5]["widget"]["rows"]
check("l22 s5 moments 210, 67,000, 22,900", rows[0][1]["answer"] == ey and rows[1][1]["answer"] == ey2 and near(rows[2][1]["answer"], ey2 - ey ** 2, 1e-6))
G = 200000
cnt = rs.poisson(20, G)
tot = np.array([rs.choice(sizes, size=c, p=pr).sum() for c in cnt])
check("l22 s6/s7 MC compound Poisson: mean 4,200, variance 1,340,000 (458,000 and 882,000 are each far outside)",
      near(tot.mean(), S[6]["widget"]["answer"], 12) and near(tot.var() / 1.34e6, 1, 0.015), f"mean {tot.mean():.1f}, var {tot.var():.0f}")
check("l22 s8 inventory mean 10 sd 7.07; s10 capacity 6,515 and slips", near(math.sqrt(50), S[8]["widget"]["rows"][1][1]["answer"], 5e-3)
      and near(4200 + 2 * math.sqrt(1.34e6), S[10]["widget"]["answer"], 0.5) and near(wrongs(S[10]["widget"])["sizes"], 4200 + 2 * math.sqrt(458000), 0.5))
note("F13: l22 s6 calls the count N_10 'a stopping-time sum'; N_10 is independent of the sizes, and E[S] = E[N]E[Y] follows from conditioning on N")
check("review-5 i8 sd 12,247; i9 8 minutes", near(math.sqrt(30 * 5e6), rv[8]["widget"]["answer"], 0.5) and rv[9]["widget"]["answer"] == 4 / 0.5)

# --------------------------------------------------------------------------
# review-5, homework-5, problems-5
# --------------------------------------------------------------------------
check("review-5 i1 9/11, i2 81/202, i3 84", near(Fr(9, 11), rv[1]["widget"]["answer"], 1e-4) and near(ruin_exact(2, 4, Fr(9, 20))[0], rv[2]["widget"]["answer"], 1e-4)
      and ruin_exact(6, 20, Fr(1, 2))[1] == rv[3]["widget"]["answer"])
h5 = load("homework-5")["items"]
w55, t55 = ruin_exact(4, 10, Fr(11, 20))
check("homework-5 i0 0.6376 and 23.76 by first-step solve", near(w55, h5[0]["widget"]["rows"][0][1]["answer"], 1e-4) and near(t55, h5[0]["widget"]["rows"][1][1]["answer"], 5e-3))
# i2: E[0.8^T] for the first hit of +-2, by exact distribution of T and by Monte Carlo
dist = {0: Fr(1)}
g = Fr(0)
for k in range(1, 400):
    new = {}
    for s, prb in dist.items():
        for t in (s + 1, s - 1):
            if abs(t) == 2:
                g += prb / 2 * Fr(4, 5) ** k
            else:
                new[t] = new.get(t, 0) + prb / 2
    dist = new
check("homework-5 i2 E[0.8^T] = 8/17 (direct sum over the law of T)", near(g, 8 / 17, 1e-12) and near(8 / 17, h5[2]["widget"]["answer"], 1e-4))
check("homework-5 i3 HTH at 0.6 = 155/18; i4 mean 192,000 sd 36,661; i8 100 days", near(casino("HTH", b6), h5[3]["widget"]["answer"], 1e-4)
      and near(math.sqrt(48 * 2.8e7), h5[4]["widget"]["rows"][1][1]["answer"], 0.5) and ruin_mart(10, 20, Fr(1, 2))[1] == h5[8]["widget"]["answer"])
check("homework-5 i6 capped walk: 193/256 at 10 steps, 793/1024 at 11", stop_when_up_exact(10)[0] == Fr(193, 256) and stop_when_up_exact(11)[0] == Fr(793, 1024))
# i10 lazy walk: p=0.3, q=0.2, stay 0.5, from 2, ends 0 and 5
A = np.eye(4)
bvec = np.zeros(4)
for k in range(1, 5):
    A[k - 1, k - 1] = 0.5
    if k + 1 <= 4:
        A[k - 1, k] = -0.3
    else:
        bvec[k - 1] = 0.3
    if k - 1 >= 1:
        A[k - 1, k - 2] = -0.2
hz = np.linalg.solve(A, bvec)
p_, q_ = Fr(3, 10), Fr(1, 5)
okl = all(p_ * ((s + 1 - (p_ - q_) * (n + 1)) ** 2) + q_ * ((s - 1 - (p_ - q_) * (n + 1)) ** 2) + Fr(1, 2) * ((s - (p_ - q_) * (n + 1)) ** 2)
          - (p_ + q_ - (p_ - q_) ** 2) * (n + 1) == (s - (p_ - q_) * n) ** 2 - (p_ + q_ - (p_ - q_) ** 2) * n for s in range(-4, 5) for n in range(4))
check("homework-5 i10 lazy walk: square martingale with a = p-q, b = p+q-(p-q)^2; theta = q/p; chance 135/211 by linear solve",
      okl and near(hz[1], 135 / 211, 1e-12) and p_ * Fr(2, 3) + Fr(1, 2) + q_ / Fr(2, 3) == 1)
p5 = load("problems-5")["items"]
check("problems-5 i0 ATM: 45, 2,620, 2,950, sd 325.88, cash 2,271.77", p5[0]["parts"][0]["widget"]["answer"] == 45 and p5[0]["parts"][1]["widget"]["answer"] == 1000 + 3 * 540
      and near(math.sqrt(36 * 2950), p5[0]["parts"][3]["widget"]["answer"], 5e-3) and near(1620 + 2 * math.sqrt(36 * 2950), p5[0]["parts"][4]["widget"]["answer"], 5e-3))
w45, t45 = ruin_exact(3, 5, Fr(9, 20))
check("problems-5 i1 signal trial: 0.4780, 6.0975 days, P&L -1,219.51 both ways", near(w45, p5[1]["parts"][2]["widget"]["answer"], 1e-4) and near(t45, p5[1]["parts"][3]["widget"]["answer"], 1e-4)
      and near(-200 * t45, p5[1]["parts"][4]["widget"]["answer"], 0.01) and near(4000 * w45 - 6000 * (1 - w45), -200 * t45, 1e-9))
check("problems-5 i2 cut rules: LL 130/9 days and 866.67; LWL 1,152.38", near(casino("LL", LW3), p5[2]["parts"][1]["widget"]["answer"], 1e-4)
      and near(60 * casino("LL", LW3), p5[2]["parts"][3]["widget"]["answer"], 5e-3) and near(60 * first_step_wait("LWL", LW3), p5[2]["parts"][4]["widget"]["answer"], 5e-3))
rs = np.random.default_rng(55)
G = 60000
tt = pp = 0.0
for _ in range(G):
    run = 0
    while run < 2:
        tt += 1
        if rs.random() < 0.3:
            run += 1
            pp -= 500
        else:
            run = 0
            pp += 300
check("problems-5 i2 MC Wald: total P&L at the LL cut averages 866.67 = 60 E[T] (E[T] 14.44)", near(tt / G, 130 / 9, 0.2) and near(pp / G, 866.67, 30), f"T {tt / G:.2f}, P&L {pp / G:.1f}")
# i3 reflected walk on 0..7 from 2
A = np.zeros((7, 7))
bT = np.ones(7)
for k in range(7):
    A[k, k] = 1
    if k == 0:
        A[k, 1] -= 1
    else:
        A[k, k - 1] -= 0.5
        if k + 1 < 7:
            A[k, k + 1] -= 0.5
tk = np.linalg.solve(A, bT)
bZ = np.zeros(7)
bZ[0] = 1
zk = np.linalg.solve(A, bZ)
check("problems-5 i3 print shop: E[T] = 45 from 2 (t_k = 49 - k^2), P(empties first) 5/7, E[idle hours] = 5, profit 500",
      np.allclose(tk, [49 - k * k for k in range(7)]) and near(zk[2], p5[3]["parts"][3]["widget"]["answer"], 1e-9)
      and near(ruin_mart(2, 7, Fr(1, 2))[0], 2 / 7, 1e-12) and 20 * (45 - 5) - 60 * 5 == p5[3]["parts"][4]["widget"]["answer"])

print()
print(f"{COUNT[0]} checks, {len(FAILS)} failing")
for f_ in FAILS:
    print("  failing: " + f_)
sys.exit(1 if FAILS else 0)
