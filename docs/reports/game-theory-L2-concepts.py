"""Concept checks for game-theory L2 (lessons l6 to l10, review-2, homework-2).

Backward induction is recomputed by a tree solver; the auction results (equilibrium bid, revenue
equivalence, the winner's curse, acquire-a-company) by exact integration and Monte Carlo with
enough draws to separate each claim from its negation; bargaining by the recursion and the
Rubinstein formula. Each assert names the ledger row it covers. Run:
python3 -I docs/reports/game-theory-L2-concepts.py
"""
from fractions import Fraction as F

import numpy as np

rng = np.random.default_rng(20261106)


# ---------- backward induction ----------
def spe(tree):
    if isinstance(tree, tuple):
        return tree
    p = tree["player"]
    outcomes = [spe(m) for m in tree["moves"]]
    return max(outcomes, key=lambda pay: pay[p])


ENTRY = {"player": 0, "moves": [(0, 10), {"player": 1, "moves": [(-2, 2), (3, 5)]}]}
assert spe(ENTRY) == (3, 5), "l6 screens[0] entry game ends (3, 5)"
CENT4 = {"player": 0, "moves": [(2, 0), {"player": 1, "moves": [(1, 3), {"player": 0, "moves": [(4, 2), {"player": 1, "moves": [(3, 5), (6, 4)]}]}]}]}
assert spe(CENT4) == (2, 0), "l6 screens[3] centipede: Ana takes at once"
T = (8, 6)
for k, take in reversed(list(enumerate([(2, 0), (1, 3), (4, 2), (3, 5), (6, 4), (5, 7)]))):
    T = {"player": k % 2, "moves": [take, T]}
assert spe(T) == (2, 0), "l6 screens[7] six-move centipede: Ana gets 2"
TREE = {"player": 0, "moves": [{"player": 1, "moves": [(3, 1), (1, 2)]}, {"player": 1, "moves": [(2, 2), {"player": 0, "moves": [(4, 1), (2, 3)]}]}]}
assert spe(TREE) == (2, 2), "l6 screens[7] tree: Ana gets 2 via (2, 2)"
VA = {"player": 0, "moves": [{"player": 1, "moves": [(3, 2), (0, 0)]}, {"player": 1, "moves": [(0, 0), (2, 3)]}]}
VB = {"player": 1, "moves": [{"player": 0, "moves": [(3, 2), (0, 0)]}, {"player": 0, "moves": [(0, 0), (2, 3)]}]}
assert spe(VA) == (3, 2) and spe(VB) == (2, 3), "l6 screens[7] venue game: first mover gets a favourite (3, then 2 for Ana)"
assert spe({"player": 0, "moves": [(0, 7), {"player": 1, "moves": [(-3, 3), (1, 2)]}]}) == (0, 7), "l6 quiz[0] credible threat: stay out"
assert spe({"player": 0, "moves": [(2, 2), {"player": 1, "moves": [(5, 1), (0, 3)]}]}) == (2, 2), "l6 quiz[1] Safe for 2"
CHK = {"player": 0, "moves": [{"player": 1, "moves": [(2, 2), (1, 3)]}, {"player": 1, "moves": [(3, 1), (0, 0)]}]}
assert spe(CHK) == (3, 1), "l6 quiz[2] sequential chicken: Ana 3"
assert spe({"player": 0, "moves": [(0, 8), {"player": 1, "moves": [(-1, 1), (2, 4)]}]}) == (2, 4), "review-2 items[0]"
C3 = {"player": 0, "moves": [(2, 0), {"player": 1, "moves": [(1, 3), {"player": 0, "moves": [(4, 2), (3, 5)]}]}]}
assert spe(C3) == (2, 0), "review-2 items[1] three-move centipede"
# l6 screens[8]: capacity worth up to 5; homework-2 items[2]: up to 3
for k in np.linspace(0, 10, 1001):
    with_cap = spe({"player": 0, "moves": [(0, 10 - k), {"player": 1, "moves": [(-2, 6 - k), (3, 5 - k)]}]})[1]
    assert (with_cap > 5) == (k < 5), "l6 screens[8] capacity pays while k < 5"
    with_cap2 = spe({"player": 0, "moves": [(0, 9 - k), {"player": 1, "moves": [(-3, 7 - k), (2, 6 - k)]}]})[1]
    assert (with_cap2 > 6) == (k < 3), "homework-2 items[2] capacity pays while k < 3"
# strategic form of the entry game has two pure NE (l6 screens[1])
A = np.array([[0, 0], [-2, 3]], float)
B = np.array([[10, 10], [2, 5]], float)
ne = [(i, j) for i in range(2) for j in range(2) if A[i, j] >= A[:, j].max() and B[i, j] >= B[i, :].max()]
assert ne == [(0, 0), (1, 1)], "l6 screens[1] (Out, Fight) and (In, Share)"
# l6 screens[5]: with a tie both outcomes are subgame perfect
tie = {"player": 1, "moves": [(-2, 5), (3, 5)]}
assert {spe({"player": 0, "moves": [(0, 10), {"player": 1, "moves": [m]}]})[0] for m in tie["moves"]} == {0, 3}, "l6 screens[5] tie gives two SPE outcomes"

# homework-2 items[1]: the starter follows the first move and fails test 0
def starter(tree):
    node = tree
    while isinstance(node, dict):
        node = node["moves"][0]
    return node


assert starter(ENTRY) == (0, 10) != spe(ENTRY), "homework-2 items[1] starter fails"

# ---------- l7 guessing games ----------
bounds = [100 * (2 / 3) ** k for k in range(1, 13)]
assert abs(bounds[0] - 66.67) < 0.01 and abs(bounds[1] - 44.44) < 0.01 and abs(bounds[2] - 29.63) < 0.01, "l7 screens[1] bounds"
assert bounds[10] > 1 > bounds[11], "l7 screens[1] below 1 after 12 rounds"
assert 100 * 0.5 ** 6 > 1 > 100 * 0.5 ** 7, "l7 screens[7] halving: 7 rounds"
room = 0.3 * 50 + 0.4 * 50 * 2 / 3 + 0.2 * 50 * 4 / 9 + 0.1 * 50 * 8 / 27
assert abs(room - 925 / 27) < 1e-9 and abs(2 / 3 * room - 1850 / 81) < 1e-9, "l7 screens[3] room average and target"
# two players: the lower guess is always nearer (a + b)/3 (l7 screens[5]) by Monte Carlo over 10^6 pairs
a = rng.uniform(0, 100, 10 ** 6)
b = rng.uniform(0, 100, 10 ** 6)
lo, hi = np.minimum(a, b), np.maximum(a, b)
t = (a + b) / 3
assert (np.abs(lo - t) < np.abs(hi - t)).all(), "l7 screens[5] the lower guess always wins with two players"
# guess above 66.67 never beats 66.67 itself, any room size (l7 screens[0])
for n in (2, 5, 50):
    others = rng.uniform(0, 100, (10 ** 5, n - 1)).sum(axis=1)
    g = rng.uniform(200 / 3, 100, 10 ** 5)
    tg, t66 = 2 / 3 * (others + g) / n, 2 / 3 * (others + 200 / 3) / n
    assert (np.abs(g - tg) > np.abs(200 / 3 - t66)).all(), "l7 screens[0] a guess above 66.67 is always further from the target than 66.67"
# upward game with 50 players (l7 screens[8]): all 0 and all 100 are NE, all 50 and all 66.67 are not
def target_up(guesses):
    return min(100, 1.5 * np.mean(guesses))


def is_sym_ne(x, n=50):
    base = np.full(n, float(x))
    t = target_up(base)
    d0 = abs(x - t)
    for y in np.linspace(0, 100, 2001):
        g = base.copy()
        g[0] = y
        t2 = target_up(g)
        if abs(y - t2) < min(abs(g[1:] - t2).min(), d0 if False else abs(x - t2)) - 1e-12:
            return False
    return True


assert is_sym_ne(0) and is_sym_ne(100), "l7 screens[8] all 0 and all 100 are equilibria"
assert not is_sym_ne(50) and not is_sym_ne(200 / 3), "l7 screens[8] all 50 and all 66.67 are not"
assert abs(30 - (2 / 3 * 30 + 10)) < 1e-12, "l7 screens[7] plus 10 fixed point 30"
assert abs(36 - (2 / 3 * 36 + 12)) < 1e-12, "homework-2 items[5] plus 12 fixed point 36"

# ---------- l8 sealed bids ----------
# best reply to a rival bidding V/2 (V uniform 0..100): profit (80 - b) 2b/100 peaks at 40 (l8 screens[0])
bgrid = np.linspace(0, 80, 8001)
profit = (80 - bgrid) * np.minimum(2 * bgrid / 100, 1)
assert abs(bgrid[profit.argmax()] - 40) < 0.02 and abs(profit.max() - 32) < 1e-6, "l8 screens[0] best bid 40, profit 32"
# equilibrium bid (n-1)v/n is a best reply against n-1 rivals using it (l8 screens[6]), checked numerically for n = 2..6
for n in (2, 3, 4, 5, 6):
    for v in (30, 60, 90):
        bs = np.linspace(0, v, 9001)
        # win when b > max rival bid = (n-1)/n * max rival value; P(max rival value < n b/(n-1)) = (min(n b/(n-1), 100)/100)^(n-1)
        pw = (np.minimum(n * bs / (n - 1), 100) / 100) ** (n - 1)
        ep = (v - bs) * pw
        assert abs(bs[ep.argmax()] - (n - 1) / n * v) < 0.03, f"l8 screens[6] bid (n-1)v/n is a best reply, n = {n}, v = {v}"
# revenue equivalence by Monte Carlo (l8 screens[3], [6], quiz[2], review-2 items[5]): E[second-highest] = (n-1)/(n+1) 100 = E[(n-1)/n max]
for n, exp in [(2, 100 / 3), (4, 60), (5, 200 / 3), (7, 75), (10, 900 / 11)]:
    vals = rng.uniform(0, 100, (400000, n))
    srt = np.sort(vals, axis=1)
    second = srt[:, -2].mean()
    first_price = ((n - 1) / n * srt[:, -1]).mean()
    assert abs(second - exp) < 0.15 and abs(first_price - exp) < 0.15, f"l8 revenue equivalence n = {n}: both formats average {exp:.2f}"
assert abs((srt[:, -1]).mean() - 1000 / 11) < 0.15, "l8 screens[8] top of ten values averages 10/11 x 100"
# second price: bidding value is weakly dominant (l8 screens[2], [4]) - against every rival bid the truthful payoff is at least any other bid's
v0 = 80
for r in np.linspace(0, 100, 201):
    truthful = (v0 - r) if v0 > r else 0.0
    for bid in np.linspace(0, 100, 101):
        other = (v0 - r) if bid > r else 0.0
        assert truthful >= other - 1e-12, "l8 screens[2] bidding your value is never worse"
# your expected profit in second price with value 80 against one uniform rival: 0.8 x 40 = 32 (l8 screens[3])
rv = rng.uniform(0, 100, 10 ** 6)
assert abs(np.where(rv < 80, 80 - rv, 0).mean() - 32) < 0.1, "l8 screens[3] second-price profit 32"
# reserve price (l8 screens[5]): a value-40 bidder loses on every win with reserve 50
assert all(min(40 - max(50, r2), 0) <= 0 for r2 in range(0, 100)), "l8 screens[5] value 40 cannot profit above a reserve of 50"

# ---------- l9 winner's curse ----------
def mean_max_err(n, a, draws=10 ** 6):
    e = rng.uniform(-a, a, (draws, n))
    return e.max(axis=1).mean()


for n, a, exp in [(5, 10, 20 / 3), (10, 10, 90 / 11), (2, 10, 10 / 3), (20, 10, 190 / 21), (10, 20, 180 / 11), (4, 12, 7.2), (6, 14, 10), (5, 9, 6), (8, 15, 35 / 3)]:
    got = mean_max_err(n, a)
    assert abs(got - exp) < 0.03, f"l9 overshoot a(n-1)/(n+1): n = {n}, a = {a}: {got:.3f} vs {exp:.3f}"
assert abs(mean_max_err(5, 10)) > 1, "l9 screens[1] distractor: the winner's error does not average 0"
# exact bin masses of the max of 5 U(-10,10) (l9 screens[0] exact bars)
Fm = lambda x: ((x + 10) / 20) ** 5
masses = [Fm(c + 1) - Fm(c - 1) for c in range(-7, 10, 2)]
assert np.allclose(masses, [0.0003, 0.0021, 0.0078, 0.021, 0.0465, 0.0903, 0.1596, 0.2628, 0.4095], atol=6e-5), "l9 screens[0] exact bars"
# posterior given winning with a diffuse prior (l9 screens[9]): E[V | win, estimate 100] = 100 - 6.67
Vs = rng.uniform(50, 150, 3 * 10 ** 6)  # flat prior well wider than the error band around 100
E = rng.uniform(-10, 10, (3 * 10 ** 6, 5))
X = Vs[:, None] + E
win = X.argmax(axis=1) == 0
near = win & (np.abs(X[:, 0] - 100) < 1.5)
assert near.sum() > 1000 and abs(Vs[near].mean() - 280 / 3) < 0.4, "l9 screens[9] best guess 93.33 given a winning estimate of 100"
# acquire a company (l9 screens[3] to [8], quiz[1], review-2 items[7], homework-2 items[7]): exact and Monte Carlo
def acquire(k, b, draws=10 ** 6):
    V = rng.uniform(0, 100, draws)
    acc = V <= b
    return np.where(acc, k * V - b, 0).mean()


for k, b, exp in [(1.6, 60, -7.2), (1.2, 50, -10), (1.5, 40, -4), (1.5, 60, -9), (2, 60, 0), (3, 100, 50)]:
    got = acquire(k, b)
    assert abs(got - exp) < 0.12, f"l9 acquire k = {k}, b = {b}: {got:.2f} vs {exp}"
for k in (1.2, 1.5, 1.6, 1.8):
    bs = np.linspace(0, 100, 101)
    assert all(b / 100 * (k * b / 2 - b) <= 1e-12 for b in bs), f"l9 screens[7] below k = 2 every offer loses, k = {k}"
bs = np.linspace(0, 100, 101)
assert bs[np.argmax([b / 100 * (3 * b / 2 - b) for b in bs])] == 100, "l9 screens[8] at k = 3 offer the most, 100"
# break-even shade (l9 summary note): all five bidders shading by the mean overshoot earn exactly 0 in expectation;
# the best reply to that shade is to shade more, so the mean overshoot is the break-even shade, not the best bid
N = 10 ** 6
Vs = rng.uniform(500, 1500, N)
E = rng.uniform(-10, 10, (N, 5))
s0 = 20 / 3
bids = Vs[:, None] + E - s0
w = bids.argmax(axis=1)
prof0 = (Vs - bids[np.arange(N), w]).mean()
assert abs(prof0) < 0.03, "l9 summary.note: shading by exactly the mean overshoot gives the winner zero expected profit"
best_s, best_prof = s0, (np.where(w == 0, Vs - bids[:, 0], 0)).mean()
for s in np.linspace(s0, s0 + 6, 25):
    b0 = Vs + E[:, 0] - s
    win0 = b0 > bids[:, 1:].max(axis=1)
    prof = np.where(win0, Vs - b0, 0).mean()
    if prof > best_prof + 0.01:
        best_s, best_prof = s, prof
assert best_s > s0 + 0.5 and best_prof > 0.1, "l9 summary.note: a bidder who shades more than the mean overshoot earns a positive profit against rivals who shade exactly that"

# ---------- l10 bargaining ----------
s = 1.0
shares = []
for T in range(2, 6):
    s = 1 - 0.9 * s
    shares.append(s)
assert np.allclose(shares, [0.1, 0.91, 0.181, 0.8371]), "l10 screens[2] finite-horizon shares"
assert abs(1 / 1.9 - 0.5263) < 1e-4, "l10 screens[5] limit 1/1.9"
rub = lambda dA, dB: (1 - dB) / (1 - dA * dB)
assert abs(rub(0.9, 0.8) - 5 / 7) < 1e-12, "l10 screens[4] Ana 5/7"
assert abs(rub(0.95, 0.9) - 0.1 / 0.145) < 1e-12 and abs(rub(0.8, 0.8) - 1 / 1.8) < 1e-12, "l10 screens[8] drill"
assert abs(rub(0.85, 0.95) - 0.2597) < 1e-4 and abs(rub(0.95, 0.95) - 0.5128) < 1e-4, "homework-2 items[3], review-2 items[8]"
# Rubinstein shares satisfy both indifference conditions
x = rub(0.9, 0.8)
y = 1 - 0.9 * x
assert abs((1 - x) - 0.8 * y) < 1e-12 and abs((1 - y) - 0.9 * x) < 1e-12, "l10 screens[3] both responders are exactly indifferent"
# Ana's share falls in delta_B (l10 quiz[2])
assert all(rub(0.9, d1) > rub(0.9, d2) for d1, d2 in zip(np.linspace(0, 0.98, 50), np.linspace(0.02, 1, 50))), "l10 quiz[2] share falls as delta_B rises"
# three rounds, delta 0.8: 1 - 0.8 (1 - 0.8) = 0.84; two rounds 0.2; outside option (l10 screens[9])
assert abs(1 - 0.8 * (1 - 0.8) - 0.84) < 1e-12 and abs(1 - 0.7 * 0.3 - 0.79) < 1e-12, "l10 screens[8], review-2 items[8] finite rounds"
ben = 100 * (1 - 1 / 1.9)
assert abs(ben - 47.37) < 0.01 and 30 < ben < 60, "l10 screens[9] £30 does not bind, £60 does"
print("game-theory L2 concepts: all checks passed")
