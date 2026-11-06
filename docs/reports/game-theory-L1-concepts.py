"""Concept checks for game-theory L1 (lessons l1 to l5, review-1, homework-1).

Every equilibrium claim in the level is recomputed from the payoff tables by enumeration:
pure Nash equilibria by best-reply marking, 2 by 2 mixed equilibria by the indifference
equations, zero-sum values by linear programming, iterated strict dominance by a solver that
also checks domination by mixtures. Each assert names the ledger row it covers
(docs/reports/audit-game-theory-1-3-ledger.md). Run: python3 -I docs/reports/game-theory-L1-concepts.py
"""
from fractions import Fraction as F
from itertools import product

import numpy as np
from scipy.optimize import linprog


def pure_nash(A, B):
    A, B = np.array(A, float), np.array(B, float)
    out = []
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if A[i, j] >= A[:, j].max() and B[i, j] >= B[i, :].max():
                out.append((i, j))
    return out


def mixed_2x2(A, B):
    """(p, q): p = P(row 1) making the column player indifferent, q = P(col 1) making the row player indifferent."""
    A, B = [[F(x) for x in r] for r in A], [[F(x) for x in r] for r in B]
    p = (B[1][1] - B[1][0]) / (B[0][0] - B[0][1] - B[1][0] + B[1][1])
    q = (A[1][1] - A[0][1]) / (A[0][0] - A[0][1] - A[1][0] + A[1][1])
    return p, q


def zero_sum_value(M):
    """Value and row player's optimal mix of a zero-sum matrix game by LP."""
    M = np.array(M, float)
    m, n = M.shape
    shift = abs(M.min()) + 1
    Ms = M + shift
    # maximise v s.t. x^T Ms >= v for every column, sum x = 1
    c = np.zeros(m + 1)
    c[-1] = -1
    A_ub = np.hstack([-Ms.T, np.ones((n, 1))])
    b_ub = np.zeros(n)
    A_eq = np.hstack([np.ones((1, m)), np.zeros((1, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1], bounds=[(0, 1)] * m + [(None, None)])
    assert res.success
    return res.x[-1] - shift, res.x[:m]


def strictly_dominated_by_mix(payoffs, k, others_axis):
    """Is pure strategy k strictly dominated by some mixture of the others? payoffs: rows are own strategies."""
    P = np.array(payoffs, float)
    rows = [i for i in range(P.shape[0]) if i != k]
    if not rows:
        return False
    # maximise eps s.t. sum_i w_i P[i, j] - P[k, j] >= eps for all j, sum w = 1, w >= 0
    r = len(rows)
    c = np.zeros(r + 1)
    c[-1] = -1
    A_ub = np.hstack([-P[rows, :].T, np.ones((P.shape[1], 1))])
    b_ub = -P[k, :]
    A_eq = np.hstack([np.ones((1, r)), np.zeros((1, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1], bounds=[(0, 1)] * r + [(None, None)])
    return res.success and res.x[-1] > 1e-9


def iesds(A, B):
    """Iterated elimination of strictly dominated strategies (mixtures allowed), simultaneous rounds.
    Returns (surviving rows, surviving cols, rounds)."""
    A, B = np.array(A, float), np.array(B, float)
    rows, cols = list(range(A.shape[0])), list(range(A.shape[1]))
    rounds = 0
    while True:
        subA, subB = A[np.ix_(rows, cols)], B[np.ix_(rows, cols)].T
        dr = [rows[i] for i in range(len(rows)) if strictly_dominated_by_mix(subA, i, 1)]
        dc = [cols[j] for j in range(len(cols)) if strictly_dominated_by_mix(subB, j, 1)]
        if not dr and not dc:
            return rows, cols, rounds
        rounds += 1
        rows = [r for r in rows if r not in dr]
        cols = [c for c in cols if c not in dc]


# ---------- l3 drill and spread table ----------
G1 = ([[0, 4, 5], [4, 0, 0], [5, 3, 2]], [[4, 0, 3], [1, 3, 2], [4, 3, 5]])
G2 = ([[1, 4, 2], [5, 3, 1], [4, 6, 5]], [[0, 5, 2], [1, 3, 1], [1, 6, 4]])
G3 = ([[2, 3, 0], [6, 0, 4], [4, 0, 3]], [[1, 5, 0], [4, 2, 0], [1, 0, 3]])
assert pure_nash(*G1) == [], "l3 screens[7] game 1: no pure NE"
assert pure_nash(*G2) == [(2, 1)], "l3 screens[7] game 2: one pure NE at (B, C)"
assert sorted(pure_nash(*G3)) == [(0, 1), (1, 0)], "l3 screens[7] game 3: (T, C) and (M, L)"
VEN = ([[3, 0], [0, 1]], [[3, 0], [0, 1]])
assert sorted(pure_nash(*VEN)) == [(0, 0), (1, 1)], "l3 screens[7] venue game: two pure NE"
SPR_A = [[50, 100, 100], [0, 100, 200], [0, 0, 150]]
SPR_B = [[50, 0, 0], [100, 100, 0], [100, 200, 150]]
assert sorted(pure_nash(SPR_A, SPR_B)) == [(0, 0), (1, 1)], "l3 screens[8] spread table: (1, 1) and (2, 2) only"
assert pure_nash([[1, 3, 0], [2, 1, 4]], [[2, 1, 0], [0, 3, 2]]) == [], "l3 quiz[1]: no pure NE"
assert pure_nash([[1, -1], [-1, 1]], [[-1, 1], [1, -1]]) == [], "l3 screens[5] matching pennies"
assert sorted(pure_nash([[-2, 4], [0, 3]], [[-2, 0], [4, 3]])) == [(0, 1), (1, 0)], "l3 screens[3] race"
assert pure_nash([[2, 5], [1, 4]], [[2, 1], [5, 4]]) == [(0, 0)], "l3 screens[4] PD"

# ---------- l4 mixed equilibria ----------
p, q = mixed_2x2([[3, 0], [0, 2]], [[2, 0], [0, 3]])
assert (p, q) == (F(3, 5), F(2, 5)), "l4 screens[2] venues p = 3/5, q = 2/5"
assert 3 * q == F(6, 5) and 2 * p == F(6, 5), "l4 screens[2] each expects 1.2"
p2, q2 = mixed_2x2([[6, 0], [0, 2]], [[2, 0], [0, 3]])
assert (p2, q2) == (F(3, 5), F(1, 4)), "l4 screens[3] and [4]: raising Ana's prize moves Ben's q to 1/4, Ana's p stays 3/5"
assert 6 * q2 == F(3, 2), "l4 screens[3] Ana now expects 1.5"
pr, qr = mixed_2x2([[-2, 4], [0, 3]], [[-2, 0], [4, 3]])
assert pr == qr == F(1, 3), "l4 screens[7] race: aggressive with 1/3"
assert 3 * (1 - pr) == 2, "l4 screens[7] race payoff 2"
pv, qv = mixed_2x2([[3, 0], [0, 1]], [[3, 0], [0, 1]])
assert pv == qv == F(1, 4) and 3 * qv == F(3, 4), "l4 screens[7] venues 1/4 and 0.75"
pn, qn = mixed_2x2([[2, 0], [1, 3]], [[1, 3], [2, 0]])
assert (pn, qn) == (F(1, 2), F(3, 4)), "l4 screens[7] new game: Ana T 1/2, Ben L 3/4"
assert 2 * qn == F(3, 2) and 3 * pn == F(3, 2), "l4 screens[7] new game each expects 1.5"
assert pure_nash([[2, 0], [1, 3]], [[1, 3], [2, 0]]) == [], "l4 screens[7] new game has no pure NE"
pq, qq = mixed_2x2([[1, 4], [2, 1]], [[3, 0], [1, 2]])
assert (pq, qq) == (F(1, 4), F(3, 4)), "l4 quiz[0] p = 1/4, q = 3/4"
assert pure_nash([[1, 4], [2, 1]], [[3, 0], [1, 2]]) == [], "l4 quiz[0] no pure NE"

# modified RPS games: value 0, optimal mixes, uniqueness by LP on both sides
RPS2 = [[0, -1, 2], [1, 0, -1], [-2, 1, 0]]
v, x = zero_sum_value(RPS2)
assert abs(v) < 1e-9 and np.allclose(x, [0.25, 0.5, 0.25], atol=1e-6), "l4 screens[8] RPS with rock 2: rock 1/4, paper 1/2, scissors 1/4"
# uniqueness: any optimal q satisfies A q <= 0; check the vertex set of that polytope is the single point
for cand in product(np.linspace(0, 1, 101), repeat=2):
    r_, p_ = cand
    s_ = 1 - r_ - p_
    if s_ < -1e-12:
        continue
    if (np.array(RPS2) @ np.array([r_, p_, s_]) <= 1e-9).all():
        assert np.allclose([r_, p_, s_], [0.25, 0.5, 0.25], atol=0.011), "l4 screens[8] uniqueness of the RPS mix"
RPS3 = [[0, -1, 1], [1, 0, -3], [-1, 3, 0]]
v3, x3 = zero_sum_value(RPS3)
assert abs(v3) < 1e-9 and np.allclose(x3, [0.6, 0.2, 0.2], atol=1e-6), "l4 quiz[1] RPS with scissors 3: rock 3/5"

# ---------- l5 zero-sum ----------
v, x = zero_sum_value([[4, 2, 5], [6, 3, 4], [1, 0, 7]])
assert abs(v - 3) < 1e-9 and np.allclose(x, [0, 1, 0], atol=1e-6), "l5 screens[1] saddle at midday worth 3"
PEN = [[0.55, 0.95], [0.90, 0.65]]
v, x = zero_sum_value(PEN)
assert abs(v - 199 / 260) < 1e-9 and abs(x[0] - 5 / 13) < 1e-6, "l5 screens[2] penalty value 199/260 at p = 5/13"
vq, xq = zero_sum_value(-np.array(PEN).T)
assert abs(xq[0] - 6 / 13) < 1e-6, "l5 screens[2] keeper dives left 6/13"
v, x = zero_sum_value([[6, 1, 3], [0, 4, 2]])
assert abs(v - 2.5) < 1e-9 and abs(x[0] - 0.5) < 1e-6, "l5 screens[3] 2 by 3 value 2.5 at p = 1/2"
vb, xb = zero_sum_value(-np.array([[6, 1, 3], [0, 4, 2]]).T)
assert np.allclose(xb, [0, 0.25, 0.75], atol=1e-6), "l5 screens[3] Ben mixes columns 2, 3 at 1/4, 3/4"
UNEQ = [[3, -2], [-2, 1]]
v, x = zero_sum_value(UNEQ)
assert abs(v + 1 / 8) < 1e-9 and abs(x[0] - 3 / 8) < 1e-6, "l5 screens[4] and [5] unequal pennies value -1/8, heads 3/8"
assert abs(np.mean(UNEQ)) < 1e-12, "l5 screens[4] cell average is 0 (the trap)"
v, x = zero_sum_value([[3, 1], [5, 2]])
assert abs(v - 2) < 1e-9 and np.allclose(x, [0, 1], atol=1e-6), "l5 screens[6] saddle worth 2, formula p = 3 does not apply"
assert F(2 - 5, 3 - 1 - 5 + 2) == 3, "l5 screens[6] the formula gives p = 3"
for M, pv, vv, name in [([[3, -4], [-4, 5]], 9 / 16, -1 / 16, "Morra"), ([[5, 1], [2, 4]], 1 / 3, 3, "game B")]:
    v, x = zero_sum_value(M)
    assert abs(v - vv) < 1e-9 and abs(x[0] - pv) < 1e-6, f"l5 screens[8] {name}"
v, x = zero_sum_value([[4, 6], [3, 2]])
assert abs(v - 4) < 1e-9 and np.allclose(x, [1, 0], atol=1e-6), "l5 screens[8] game C saddle worth 4"
v, x = zero_sum_value([[6, 2], [3, 4]])
assert abs(v - 3.6) < 1e-9 and abs(x[0] - 0.2) < 1e-6, "l5 quiz[0] value 3.6, p = 1/5"
v, x = zero_sum_value([[2, 4], [1, 3]])
assert abs(v - 2) < 1e-9, "l5 quiz[1] saddle worth 2"
# l5 quiz[2]: in a 2 by 2 without saddle the row player's optimal mix equalises both columns
v, x = zero_sum_value([[6, 2], [3, 4]])
col_payoffs = x @ np.array([[6, 2], [3, 4]], float)
assert np.allclose(col_payoffs, [v, v]), "l5 quiz[2] equaliser: Ana's mix pays the value against either pure column"

# ---------- review-1 ----------
assert pure_nash([[6, 2, 1], [3, 4, 4], [0, 1, 2]], [[4, 0, 1], [6, 5, 0], [1, 3, 0]]) == [(0, 0)], "review-1 items[3] one NE at (T, L)"
pr1, qr1 = mixed_2x2([[2, 0], [0, 1]], [[0, 3], [2, 0]])
assert (pr1, qr1) == (F(2, 5), F(1, 3)), "review-1 items[4] p = 2/5, q = 1/3"
rows, cols, rounds = iesds([[4, 2, 9], [6, 7, 7], [9, 0, 1]], [[7, 7, 6], [2, 7, 2], [2, 9, 8]])
assert (rows, cols) == ([1], [1]), "review-1 items[5] IESDS ends at (M, C)"
assert pure_nash([[2, 4, 1], [0, 3, 5], [6, 1, 2]], [[5, 1, 3], [2, 6, 1], [0, 2, 4]]) == [], "review-1 items[6] no NE"
v, x = zero_sum_value([[5, 0, 3], [1, 4, 2]])
assert abs(v - 2.4) < 1e-9 and abs(x[0] - 0.4) < 1e-6, "review-1 items[7] value 2.4 at p = 2/5"
vb, xb = zero_sum_value(-np.array([[5, 0, 3], [1, 4, 2]]).T)
assert np.allclose(xb, [0, 0.2, 0.8], atol=1e-6), "review-1 items[7] Ben mixes columns 2, 3 at 1/5, 4/5"
assert sorted(pure_nash([[3, 5, 5], [1, 0, 3], [5, 3, 6]], [[2, 4, 2], [3, 2, 2], [6, 5, 4]])) == [(0, 1), (2, 0)], "review-1 items[8] two NE"

# ---------- l2 iterated dominance ----------
rows, cols, rounds = iesds([[4, 5, 6], [2, 8, 3], [3, 9, 2]], [[3, 1, 2], [1, 4, 6], [0, 6, 8]])
assert (rows, cols, rounds) == ([0], [0], 3), "l2 screens[2] and screens[8] rows[2]: (T, L) in three rounds"
rows, cols, rounds = iesds([[1, 4, 0], [7, 9, 5], [2, 1, 6]], [[7, 0, 0], [4, 5, 8], [5, 5, 7]])
assert (rows, cols, rounds) == ([2], [2], 3), "l2 screens[8] drill: (B, R), Ana 6, three rounds (C goes by a mix of L and R)"
assert strictly_dominated_by_mix([[3, 0], [0, 3], [1, 1]], 2, 1), "l2 screens[3] D is dominated by a mix of U and M"
assert not any(strictly_dominated_by_mix([[1, -1], [-1, 1]], k, 1) for k in range(2)), "l2 screens[6] matching pennies: nothing dominated"
rows, cols, rounds = iesds([[1, 0, 3], [0, 6, 1], [5, 9, 2]], [[0, 1, 2], [8, 8, 7], [5, 4, 9]])
assert (rows, cols) == ([0], [2]), "homework-1 items[2] IESDS ends at (T, R)"
# weak-deletion trap: all four cells are pure NE
assert sorted(pure_nash([[1, 0], [1, 2], [0, 2]], [[1, 0], [1, 1], [0, 1]])) == [(0, 0), (1, 0), (1, 1), (2, 1)], "l2 screens[5] four pure NE survive"

# ---------- homework-1 ----------
ph, qh = mixed_2x2([[4, 0], [1, 2]], [[1, 2], [3, 0]])
assert (ph, qh) == (F(3, 4), F(2, 5)) and 4 * qh == F(8, 5), "homework-1 items[3] q = 2/5, p = 3/4, Ana expects 1.6"
v, x = zero_sum_value([[1, 5, 3], [6, 0, 2]])
assert abs(v - 8 / 3) < 1e-9 and abs(x[0] - 2 / 3) < 1e-6, "homework-1 items[6] value 8/3 at p = 2/3"
vb, xb = zero_sum_value(-np.array([[1, 5, 3], [6, 0, 2]]).T)
assert np.allclose(xb, [1 / 6, 0, 5 / 6], atol=1e-6), "homework-1 items[6] Ben mixes columns 1, 3 at 1/6, 5/6"
v, x = zero_sum_value([[5, -2], [-2, 1]])
assert abs(v - 0.1) < 1e-9 and abs(x[0] - 0.3) < 1e-6, "homework-1 items[7] value +0.10 at p = 3/10"

# homework-1 code items: run the solutions against every hidden test; the starters must fail
NS = {}
exec(
    "def pure_nash_s(A, B):\n    m, n = len(A), len(A[0])\n    out = []\n    for i in range(m):\n        for j in range(n):\n"
    "            ana_best = all(A[k][j] <= A[i][j] for k in range(m))\n            ben_best = all(B[i][l] <= B[i][j] for l in range(n))\n"
    "            if ana_best and ben_best:\n                out.append((i, j))\n    return out\n", NS)
tests = [
    ([[3, 0, 2], [1, 2, 4], [2, 3, 1]], [[1, 2, 4], [3, 1, 0], [2, 3, 1]], [(2, 1)]),
    (SPR_A, SPR_B, [(0, 0), (1, 1)]),
    ([[1, -1], [-1, 1]], [[-1, 1], [1, -1]], []),
    ([[2, 5], [1, 4]], [[2, 1], [5, 4]], [(0, 0)]),
    ([[1, 0], [1, 2], [0, 2]], [[1, 0], [1, 1], [0, 1]], [(0, 0), (1, 0), (1, 1), (2, 1)]),
    (G3[0], G3[1], [(0, 1), (1, 0)]),
    (G1[0], G1[1], []),
]
for A, B, exp in tests:
    assert NS["pure_nash_s"](A, B) == exp, "homework-1 items[1] solution passes its tests"
    assert pure_nash(A, B) == exp, "homework-1 items[1] expected values agree with the independent solver"
assert all([] != exp for A, B, exp in tests[:1]), "homework-1 items[1] starter (returns []) fails test 0"


def solve_zs(a):
    a = [[F(x) for x in row] for row in a]
    row_min = [min(r) for r in a]
    col_max = [max(a[0][j], a[1][j]) for j in range(2)]
    if max(row_min) == min(col_max):
        i = row_min.index(max(row_min))
        j = col_max.index(min(col_max))
        return F(1 - i), F(1 - j), max(row_min)
    d = a[0][0] - a[0][1] - a[1][0] + a[1][1]
    return (a[1][1] - a[1][0]) / d, (a[1][1] - a[0][1]) / d, (a[0][0] * a[1][1] - a[0][1] * a[1][0]) / d


zs_tests = [
    ([[55, 95], [90, 65]], (F(5, 13), F(6, 13), F(995, 13))),
    ([[3, -2], [-2, 1]], (F(3, 8), F(3, 8), F(-1, 8))),
    ([[3, -4], [-4, 5]], (F(9, 16), F(9, 16), F(-1, 16))),
    ([[5, 1], [2, 4]], (F(1, 3), F(1, 2), F(3))),
    ([[3, 1], [5, 2]], (F(0), F(0), F(2))),
    ([[4, 6], [3, 2]], (F(1), F(1), F(4))),
    ([[5, -2], [-2, 1]], (F(3, 10), F(3, 10), F(1, 10))),
]
for a, exp in zs_tests:
    got = solve_zs(a)
    assert got == exp, f"homework-1 items[4] solution on {a}"
    v, x = zero_sum_value(a)
    assert abs(v - float(exp[2])) < 1e-9 and abs(x[0] - float(exp[0])) < 1e-6, f"homework-1 items[4] expected (p, v) agree with LP on {a}"
    vq, xq = zero_sum_value(-np.array(a, float).T)
    assert abs(xq[0] - float(exp[1])) < 1e-6, f"homework-1 items[4] expected q agrees with LP on {a}"
# the starter (formula only) gives p = 3 on the saddle game
a = [[F(3), F(1)], [F(5), F(2)]]
d = a[0][0] - a[0][1] - a[1][0] + a[1][1]
assert (a[1][1] - a[1][0]) / d == 3, "homework-1 items[4] starter fails the saddle test with p = 3"

# homework-1 items[5]: a weakly dominated action can be played in a Nash equilibrium (the explain drops 'strictly')
A5, B5 = [[1, 0], [1, 2], [0, 2]], [[1, 0], [1, 1], [0, 1]]
assert (0, 0) in pure_nash(A5, B5), "homework-1 items[5].explain: (U, L) is a NE although U is weakly dominated by M"
assert not strictly_dominated_by_mix(A5, 0, 1), "homework-1 items[5].explain: U is not strictly dominated"
print("game-theory L1 concepts: all checks passed")
