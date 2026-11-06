"""Concept checks for puzzles L1 (lessons l1 to l6, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/puzzles-L1-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-puzzles-1-3-ledger.md).
Exact checks use Fractions; Monte Carlo checks use seeded numpy with enough draws
to separate the claim from its negation (bands are 4 standard errors unless said).
"""
from fractions import Fraction as F
from itertools import permutations, product
from math import comb, exp, factorial, log, sqrt

import numpy as np

rng = np.random.default_rng(20261106)
H = lambda n: sum(F(1, k) for k in range(1, n + 1))


def mc_band(p, n, k=4):
    return k * sqrt(p * (1 - p) / n)


# ---------------------------------------------------------------- l1 dice games
def check_dice_max_min():
    faces = range(1, 7)
    emax = F(sum(max(a, b) for a in faces for b in faces), 36)
    emin = F(sum(min(a, b) for a in faces for b in faces), 36)
    assert emax == F(161, 36), "dice_max_min: E[max of two dice] = 161/36"
    assert emin == F(91, 36) == 7 - emax, "dice_max_min: E[min] = 7 - E[max] = 91/36"
    for m in faces:
        assert sum(1 for a in faces for b in faces if max(a, b) == m) == 2 * m - 1, "dice_max_min: larger face m fills 2m-1 cells"
        assert sum(1 for a in faces for b in faces if min(a, b) == m) == 13 - 2 * m, "dice_max_min: smaller face m fills 13-2m cells"


def check_dice_abs_diff():
    e = F(sum(abs(a - b) for a in range(1, 7) for b in range(1, 7)), 36)
    assert e == F(35, 18), "dice_abs_diff: E|X-Y| = 35/18"
    for d in range(1, 6):
        assert sum(1 for a in range(1, 7) for b in range(1, 7) if abs(a - b) == d) == 2 * (6 - d), "dice_abs_diff: difference d fills 2(6-d) cells"


def check_wald_until_six():
    n = 400_000
    rolls = rng.integers(1, 7, size=(n, 120))
    first_six = np.argmax(rolls == 6, axis=1)
    assert (rolls == 6).any(axis=1).all()
    cum = np.cumsum(rolls, axis=1)
    sums = cum[np.arange(n), first_six]
    m = sums.mean()
    sd = sums.std()
    assert abs(m - 21) < 4 * sd / sqrt(n), f"wald_until_six: E[sum of faces until the first 6] = 21 (got {m:.3f})"
    assert abs((first_six + 1).mean() - 6) < 0.05, "wald_until_six: E[N] = 6"


def check_dice_product():
    assert F(sum(a * b for a in range(1, 7) for b in range(1, 7)), 36) == F(49, 4), "dice_product: E[XY] = 12.25 for independent dice"
    assert F(sum(a * a for a in range(1, 7)), 6) == F(91, 6), "dice_product: E[X^2] = 91/6, not 12.25"
    assert F(91, 6) - F(49, 4) == F(35, 12), "square trap: E[X^2] - (EX)^2 = Var = 35/12"


def reroll_value(faces, cost, iters=3000):
    """Optimal value of keep-or-pay-cost-to-reroll by value iteration (floats)."""
    faces = [float(x) for x in faces]
    v = max(faces)
    for _ in range(iters):
        v = sum(max(x, v - cost) for x in faces) / len(faces)
    return v


def check_reroll_values():
    cases = [([1, 2, 3, 4, 5, 6], 1, F(4)), ([1, 2, 3, 4, 5, 6], 2, F(18, 5)), ([1, 2, 3, 4, 5, 6], F(1, 2), F(9, 2)),
             ([1, 2, 3, 4, 5, 6], 0, F(6)), ([1, 2, 3, 4, 5, 6], 10, F(7, 2)), ([0, 0, 0, 10], 1, F(7)),
             ([1, 2, 3, 4], 1, F(8, 3)), ([2, 4, 9], 3, F(5)), ([5], 1, F(5)), ([7, 7, 7], 2, F(7))]
    for faces, cost, expect in cases:
        v = reroll_value(faces, float(cost))
        assert abs(v - float(expect)) < 1e-9, f"reroll_values: value iteration gives {v}, keyed {expect} for {faces} at cost {cost}"
        # homework-1 items[1]: max over m of (sum kept - m c)/(n - m)
        fs = sorted(F(x) for x in faces)
        n = len(fs)
        vm = max((sum(fs[m:]) - m * F(cost)) / (n - m) for m in range(n))
        assert vm == expect, f"reroll_values: max_m V_m = {vm}, keyed {expect}"
    # l1 screens[7] option c: at cost 1/2 keep 5 and 6, indifferent at 4 (V - c = 4)
    assert abs(reroll_value([1, 2, 3, 4, 5, 6], 0.5) - 0.5 - 4.0) < 1e-9, "reroll_values: at cost 0.5 the continuation value is 4"
    # l1 screens[5]: the Bellman fixed point V = E[max(X, V-1)] is 4 and no threshold rule beats it
    assert abs(reroll_value([1, 2, 3, 4, 5, 6], 1.0) - 4.0) < 1e-9


# ------------------------------------------------------------- l2 coupon collector
def check_coupon_means():
    for n, expect in [(2, F(3)), (6, F(147, 10)), (5, F(137, 12)), (4, F(25, 3)), (10, F(7381, 252)), (12, 12 * H(12)), (1, F(1))]:
        assert n * H(n) == expect, f"coupon_means: n H_n for n = {n}"
    assert sum(F(6, 6 - k) for k in range(3)) == F(37, 10), "coupon_means: first three faces take 3.7"
    assert sum(F(6, 6 - k) for k in range(3, 6)) == F(11), "coupon_means: last three faces take 11"
    assert abs(float(12 * H(12)) - 37.2385) < 5e-5 and abs(float(10 * H(10)) - 29.2897) < 5e-5
    # Monte Carlo for n = 6
    n = 200_000
    draws = rng.integers(0, 6, size=(n, 80))
    seen = np.zeros((n, 6), dtype=bool)
    T = np.zeros(n, dtype=int)
    done = np.zeros(n, dtype=bool)
    for j in range(80):
        seen[np.arange(n), draws[:, j]] = True
        newly = seen.all(axis=1) & ~done
        T[newly] = j + 1
        done |= newly
    assert done.all()
    assert abs(T.mean() - 14.7) < 4 * 6.244 / sqrt(n), f"coupon_means: simulated E[T] for a die = {T.mean():.3f}"
    assert abs(T.std() - 6.244) < 0.06, f"coupon_variance: simulated sd {T.std():.3f} vs 6.244"
    return T


def coupon_pmf(n_types, tmax):
    """P(T = t) exactly by inclusion-exclusion on P(T <= t)."""
    def cdf(t):
        return sum((-1) ** k * comb(n_types, k) * F(n_types - k, n_types) ** t for k in range(n_types + 1))
    return {t: cdf(t) - cdf(t - 1) for t in range(1, tmax + 1)}


def check_coupon_mode():
    pmf = coupon_pmf(6, 80)
    mode = max(pmf, key=pmf.get)
    assert mode == 11, f"coupon_mode: the most likely count for a die is 11 (got {mode})"
    assert pmf[6] == F(720, 46656), "coupon_mode: P(T = 6) = 6!/6^6"
    assert abs(float(pmf[6]) - 0.015) < 0.0005


def check_coupon_variance():
    var6 = sum((1 - p) / p**2 for p in [F(6 - k, 6) for k in range(6)])
    assert abs(float(var6) - 38.99) < 0.01 and abs(sqrt(float(var6)) - 6.244) < 0.001, "coupon_variance: sd of T for a die is 6.24"
    assert 3 * sqrt(float(var6)) / sqrt(20000) < 0.14, "coupon_variance: 3 SE at 20,000 trials is under 0.14 (test band)"
    var4 = sum((1 - p) / p**2 for p in [F(4 - k, 4) for k in range(4)])
    assert 3 * sqrt(float(var4)) / sqrt(20000) < 0.085, "coupon_variance: n = 4 band 0.085 holds 3 SE"
    # homework-1 items[3] model: n H_n ~ n ln n + gamma n + 1/2
    approx = 6 * log(6) + 0.5772156649 * 6 + 0.5
    assert abs(approx - 14.7) < 0.02, "coupon asymptotic: 6 ln 6 + 6 gamma + 1/2 = 14.7"


def check_distinct_faces():
    for rolls, expect in [(6, 6 * (1 - F(5, 6) ** 6)), (3, F(91, 36))]:
        exact = F(sum(len(set(r)) for r in product(range(6), repeat=rolls)), 6**rolls)
        assert exact == expect, f"distinct_faces: E[distinct faces in {rolls} rolls] = {expect}"
    assert abs(float(6 * (1 - F(5, 6) ** 6)) - 3.9906) < 5e-5


# ------------------------------------------------------- l3 pattern waiting times
def pattern_wait(pattern, p):
    """Expected flips until pattern, by an independent Markov chain on prefix states, exact."""
    p = F(p)
    n = len(pattern)

    def nxt(k, flip):
        s = pattern[:k] + flip
        while s and not pattern.startswith(s):
            s = s[1:]
        return len(s)

    # E_k = 1 + p E_{nxt(k,H)} + q E_{nxt(k,T)}, E_n = 0: Gaussian elimination on Fractions
    A = [[F(0)] * (n + 1) for _ in range(n)]
    for k in range(n):
        A[k][k] += 1
        A[k][n] = F(1)
        for flip, ch in (("H", p), ("T", 1 - p)):
            j = nxt(k, flip)
            if j < n:
                A[k][j] -= ch
    for i in range(n):
        piv = next(r for r in range(i, n) if A[r][i] != 0)
        A[i], A[piv] = A[piv], A[i]
        for r in range(n):
            if r != i and A[r][i] != 0:
                f = A[r][i] / A[i][i]
                A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    return A[0][n] / A[0][0]


def conway(pattern):
    """Conway's leading-number formula for a fair coin: sum of 2^k over self-overlaps of length k."""
    return sum(2**k for k in range(1, len(pattern) + 1) if pattern[:k] == pattern[-k:])


def check_pattern_waits():
    half = F(1, 2)
    keyed = [("HT", half, 4), ("HH", half, 6), ("HHH", half, 14), ("HTH", half, 10), ("T", half, 2), ("HH", F(2, 3), F(15, 4)),
             ("TT", F(3, 5), F(35, 4)), ("HTTH", half, 18), ("HTHT", half, 20), ("HHTT", half, 16), ("HTHTH", half, 42),
             ("HHHHH", half, 62), ("H", half, 2), ("HTH", F(1, 3), F(33, 2)), ("HHT", F(3, 5), F(125, 18)),
             ("THTTHHTHTTHH", half, 4160), ("HHHHHHHHHHHH", F(9, 10), F(7175704635190, 282429536481)), ("HHT", half, 8), ("HTT", half, 8)]
    for pat, p, expect in keyed:
        got = pattern_wait(pat, p)
        assert got == F(expect), f"pattern_waits: {pat} at p = {p} gives {got}, keyed {expect}"
        if p == half:
            assert got == conway(pat), f"pattern_waits: Conway's rule for {pat}"
    # (1 + p)/p^2 for HH: 8.75 at p = 0.4; 6 at 1/2; 2 at 1
    for p in (F(2, 5), half, F(1)):
        assert pattern_wait("HH", p) == (1 + p) / p**2, "pattern_waits: HH wait is (1+p)/p^2"
    # die: two sixes 42, six then five 36 (review-1 items[3], homework-1 items[2])
    e66 = (1 + F(1, 6)) / F(1, 36)
    assert e66 == 42, "pattern_waits: two sixes in a row take 42 rolls"
    # 6 then 5: E_6 = 1 + E_6/6 + 4 E_0/6, E_0 = 1 + E_6/6 + 5 E_0/6 -> E_0 = 36
    e0, e6 = F(36), F(30)
    assert e6 == 1 + e6 / 6 + 4 * e0 / 6 and e0 == 1 + e6 / 6 + 5 * e0 / 6, "pattern_waits: 6 then 5 takes 36 rolls"
    # Monte Carlo HH and HT
    n = 200_000
    flips = rng.random((n, 200)) < 0.5
    hh = np.array([(flips[i, :-1] & flips[i, 1:]).argmax() + 2 for i in range(n)])
    ht = np.array([(flips[i, :-1] & ~flips[i, 1:]).argmax() + 2 for i in range(n)])
    assert abs(hh.mean() - 6) < 4 * hh.std() / sqrt(n), f"pattern_waits: simulated HH wait {hh.mean():.3f}"
    assert abs(ht.mean() - 4) < 4 * ht.std() / sqrt(n), f"pattern_waits: simulated HT wait {ht.mean():.3f}"


def check_run_of_three():
    # homework-1 items[4]: three equal faces in a row, fair coin: 7
    e2 = F(1) + F(1, 2) * 0  # placeholder to keep structure clear
    # e_1 = 1 + e_2/2 + e_1/2, e_2 = 1 + e_1/2 -> e_1 = 6
    e1 = F(6)
    e2 = 1 + e1 / 2
    assert e1 == 1 + e2 / 2 + e1 / 2, "run_of_three: run-length chain gives e_1 = 6"
    n = 200_000
    flips = rng.random((n, 120)) < 0.5
    same = flips[:, 1:] == flips[:, :-1]
    triple = same[:, :-1] & same[:, 1:]
    t = triple.argmax(axis=1) + 3
    assert triple.any(axis=1).all()
    assert abs(t.mean() - 7) < 4 * t.std() / sqrt(n), f"run_of_three: simulated wait {t.mean():.3f} vs 7"


def check_penney():
    # review-1 items[4]: HH vs HT race is 1/2; homework-1 items[7]: HT beats TT with 3/4
    n = 400_000
    flips = rng.random((n, 60)) < 0.5
    first_h = flips.argmax(axis=1)
    win_hh = flips[np.arange(n), first_h + 1]
    assert abs(win_hh.mean() - 0.5) < mc_band(0.5, n), "penney: HH vs HT race is even"
    tt_first = (~flips[:, 0]) & (~flips[:, 1])
    assert abs((~tt_first).mean() - 0.75) < mc_band(0.75, n), "penney: HT beats TT with chance 3/4"


# ------------------------------------------------------------ l4 indicator tricks
def check_runs():
    n = 200_000
    flips = rng.random((n, 10)) < 0.5
    runs = 1 + (flips[:, 1:] != flips[:, :-1]).sum(axis=1)
    assert abs(runs.mean() - 5.5) < 4 * runs.std() / sqrt(n), f"runs: E[runs in 10 flips] = 5.5 (got {runs.mean():.3f})"


def check_empty_boxes():
    n = 200_000
    balls = rng.integers(0, 10, size=(n, 10))
    empty = 10 - np.array([len(set(row)) for row in balls])
    assert abs(empty.mean() - 10 * 0.9**10) < 4 * empty.std() / sqrt(n), f"empty_boxes: E[empty] = 3.4868 (got {empty.mean():.4f})"
    both = ((balls != 0) & (balls != 1)).all(axis=1).mean()
    assert abs(both - 0.8**10) < mc_band(0.8**10, n), "empty_boxes: P(boxes 1 and 2 both empty) = 0.8^10"


def check_birthday_pairs():
    n = 100_000
    b = rng.integers(0, 365, size=(n, 30))
    pairs = np.array([sum(comb(c, 2) for c in np.bincount(row)) for row in b])
    assert abs(pairs.mean() - 435 / 365) < 4 * pairs.std() / sqrt(n), f"birthday_pairs: E[pairs] = 1.1918 (got {pairs.mean():.4f})"
    atleast = np.prod([(365 - k) / 365 for k in range(30)])
    assert abs(1 - atleast - 0.7063) < 5e-5, "birthday_pairs: P(at least one shared) = 0.7063"
    assert abs((pairs > 0).mean() - 0.7063) < mc_band(0.7063, n)


def check_birthday_triples():
    n = 100_000
    b = rng.integers(0, 365, size=(n, 50))
    triples = np.array([sum(comb(c, 3) for c in np.bincount(row)) for row in b])
    assert abs(triples.mean() - comb(50, 3) / 365**2) < 4 * triples.std() / sqrt(n), f"birthday_triples: E[triples] = 0.1471 (got {triples.mean():.4f})"


def check_aces_before_king():
    n = 200_000
    deck = np.array([1] * 4 + [2] * 4 + [0] * 44)  # 1 = ace, 2 = king
    count = np.empty(n)
    for i in range(n):
        d = rng.permutation(deck)
        first_king = np.argmax(d == 2)
        count[i] = (d[:first_king] == 1).sum()
    assert abs(count.mean() - 0.8) < 4 * count.std() / sqrt(n), f"aces_before_king: E = 0.8 (got {count.mean():.4f})"


def check_records():
    n = 200_000
    x = rng.random((n, 21))
    rec = (x == np.maximum.accumulate(x, axis=1)).sum(axis=1)
    h21 = float(H(21))
    assert abs(h21 - 3.6454) < 5e-5, "records: H_21 = 3.6454"
    assert abs(rec.mean() - h21) < 4 * rec.std() / sqrt(n), f"records: E[records among 21] = H_21 (got {rec.mean():.4f})"


def check_hh_count():
    n = 200_000
    flips = rng.random((n, 10)) < 0.5
    c = (flips[:, :-1] & flips[:, 1:]).sum(axis=1)
    assert abs(c.mean() - 2.25) < 4 * c.std() / sqrt(n), "hh_count: E[adjacent HH places] = 9/4"


def check_local_maxima():
    n = 200_000
    x = rng.random((n, 10))
    inner = (x[:, 1:-1] > x[:, :-2]) & (x[:, 1:-1] > x[:, 2:])
    ends = (x[:, 0] > x[:, 1]).astype(int) + (x[:, -1] > x[:, -2])
    lm = inner.sum(axis=1) + ends
    assert abs(lm.mean() - 11 / 3) < 4 * lm.std() / sqrt(n), f"local_maxima: E = 11/3 (got {lm.mean():.4f})"


def check_red_pairs():
    n = 100_000
    deck = np.array([1] * 26 + [0] * 26)
    both = np.empty(n)
    changes = np.empty(n)
    for i in range(n):
        d = rng.permutation(deck)
        both[i] = (d[:-1] & d[1:]).sum()
        changes[i] = (d[:-1] != d[1:]).sum()
    assert abs(both.mean() - 12.5) < 4 * both.std() / sqrt(n), f"red_pairs: E[both red adjacent] = 12.5 (got {both.mean():.3f})"
    assert abs(changes.mean() - 26) < 4 * changes.std() / sqrt(n), f"colour_changes: E[changes] = 26 (got {changes.mean():.3f})"
    assert F(26, 52) * F(25, 51) * 51 == F(25, 2) and 51 * 2 * F(26, 52) * F(26, 51) == 26


# -------------------------------------------------------------------- l5 hats
def derangements(n):
    return sum((-1) ** k * F(factorial(n), factorial(k)) for k in range(n + 1))


def check_hats():
    assert [derangements(n) for n in (4, 5, 6, 7, 8)] == [9, 44, 265, 1854, 14833], "hats: derangement numbers"
    for n, want in [(5, 0.367), (6, 0.368), (7, 0.368), (8, 0.368)]:
        assert round(float(derangements(n) / factorial(n)), 3) == want, f"hats: P(no match) for n = {n} rounds to {want}"
    counts = {k: 0 for k in range(5)}
    for perm in permutations(range(4)):
        counts[sum(i == p for i, p in enumerate(perm))] += 1
    assert [counts[k] for k in range(5)] == [9, 8, 6, 0, 1], "hats: match counts for n = 4 are 9, 8, 6, 0, 1"
    assert F(6 * derangements(5), 720) == F(264, 720) and F(derangements(6), 720) == F(265, 720), "hats: exactly one of six matches 264/720, none 265/720"
    assert F(derangements(5), 120) == F(44, 120)
    # E[N] = 1 and Var N = 1 for n = 100 by Monte Carlo
    n = 200_000
    N = np.array([(rng.permutation(100) == np.arange(100)).sum() for _ in range(n)])
    assert abs(N.mean() - 1) < 4 / sqrt(n), f"hats: E[matches] = 1 (got {N.mean():.4f})"
    assert abs(N.var() - 1) < 0.03, f"hats: Var[matches] = 1 (got {N.var():.4f})"
    assert abs((N == 0).mean() - exp(-1)) < mc_band(exp(-1), n), "hats: P(no match) near 1/e for n = 100"
    # pair chance 1/(n(n-1)) and E[N^2] = 2
    for m in (4, 7):
        pair = F(sum(1 for perm in permutations(range(m)) if perm[0] == 0 and perm[1] == 1), factorial(m))
        assert pair == F(1, m * (m - 1)), "hats: E[I_i I_j] = 1/(n(n-1))"
        en2 = F(sum(sum(i == p for i, p in enumerate(perm)) ** 2 for perm in permutations(range(m))), factorial(m))
        assert en2 == 2, "hats: E[N^2] = 2"


def check_cycles():
    # homework-1 items[6]: E[cycles of a random permutation of 10] = H_10; cycle through 0 has uniform length
    n = 100_000
    cyc = np.empty(n)
    len0 = np.empty(n, dtype=int)
    for i in range(n):
        p = rng.permutation(10)
        seen = [False] * 10
        c = 0
        for s in range(10):
            if not seen[s]:
                c += 1
                j = s
                L = 0
                while not seen[j]:
                    seen[j] = True
                    j = p[j]
                    L += 1
                if s == 0:
                    len0[i] = L
        cyc[i] = c
    assert abs(cyc.mean() - float(H(10))) < 4 * cyc.std() / sqrt(n), f"cycles: E[cycles] = H_10 (got {cyc.mean():.4f})"
    freq = np.bincount(len0, minlength=11)[1:] / n
    assert np.all(np.abs(freq - 0.1) < mc_band(0.1, n)), "cycles: the cycle through a fixed element has uniform length on 1..10"
    assert abs(float(H(10)) - 2.929) < 5e-4


def check_two_toys():
    n = 400_000
    draws = rng.random((n, 100)) < 0.8  # True = toy A
    tA = draws.argmax(axis=1) + 1
    tB = (~draws).argmax(axis=1) + 1
    assert draws.any(axis=1).all() and (~draws).any(axis=1).all()
    t = np.maximum(tA, tB)
    assert abs(t.mean() - 5.25) < 4 * t.std() / sqrt(n), f"two_toys: E[boxes] = 5.25 (got {t.mean():.4f})"
    assert 1 + 0.8 * 5 + 0.2 * 1.25 == 5.25 and 1.25 + 5 - 1 == 5.25


# ------------------------------------------------------------- l6 optimal stopping
def card_value(r, b, memo={}):
    if (r, b) in memo:
        return memo[(r, b)]
    if r == 0:
        v = F(0)
    elif b == 0:
        v = F(r)
    else:
        go = F(r, r + b) * (1 + card_value(r - 1, b)) + F(b, r + b) * (-1 + card_value(r, b - 1))
        v = max(F(0), go)
    memo[(r, b)] = v
    return v


def check_card_game():
    assert card_value(1, 1) == F(1, 2) and card_value(1, 2) == 0 and card_value(2, 1) == F(4, 3) and card_value(2, 2) == F(2, 3), "card_game: table values"
    assert card_value(3, 3) == F(17, 20) and card_value(2, 3) == F(1, 5) and card_value(0, 5) == 0 and card_value(5, 0) == 5, "card_game: keyed values"
    v = card_value(26, 26)
    assert v == F(41984711742427, 15997372030584) and abs(float(v) - 2.624475548993925) < 1e-12, "card_game: full deck value"
    # stop-when-ahead rule in the 3R 3B game is worth 3/4: it banks 1 iff the running total ever reaches +1
    orders = set(permutations("RRRBBB"))
    ever_ahead = sum(1 for o in orders if any(sum(1 if c == "R" else -1 for c in o[:k]) >= 1 for k in range(1, 7)))
    assert F(ever_ahead, len(orders)) == F(3, 4), "card_game: stop-when-ahead earns 3/4 in the 3-and-3 game"
    # the forced game is worth 0 and the optional game 2/3
    assert card_value(2, 2) == F(2, 3)
    # optimal 2R 1B after a first red: turn on (value 4/3 > 0)
    assert card_value(2, 1) > 0


def pig_optimal_threshold(gain_faces, wipe_count, tmax=400):
    """Maximise the expected score of one turn. V(t) = max(t, (1/6) sum_{f in gain} V(t + f)); wipe faces give 0."""
    V = np.zeros(tmax + 20)
    V[tmax:] = np.arange(tmax, tmax + 20)  # beyond tmax hold (never reached from a threshold rule anyway)
    for t in range(tmax - 1, -1, -1):
        roll = sum(V[t + f] for f in gain_faces) / 6
        V[t] = max(t, roll)
    roll_set = [t for t in range(tmax) if sum(V[t + f] for f in gain_faces) / 6 > t + 1e-12]
    return max(roll_set) + 1, V


def check_pig_threshold():
    th, V = pig_optimal_threshold([2, 3, 4, 5, 6], 1)
    assert th == 20, f"pig_threshold: maximising one turn's expected score holds at 20 (got {th})"
    th2, _ = pig_optimal_threshold([3, 4, 5, 6], 2)
    assert th2 == 9, f"pig_threshold: 1 or 2 wipe: hold at 9 (got {th2})"
    th3, _ = pig_optimal_threshold([1, 2, 3, 4, 5], 1)
    assert th3 == 15, f"pig_threshold: 6 wipes: hold at 15 (got {th3})"
    # the one-step rule is exact here (monotone problem): the stopping set {t >= 20} is closed under a roll
    for t in range(20, 60):
        assert all(t + f >= 20 for f in range(2, 7))
    # taking-profit transfer: 0.9 x 2000 = 0.1 t at t = 18000
    assert 0.9 * 2000 / 0.1 == 18000


def secretary_prob(n, k):
    """P(the skip-k rule picks the best of n), exact."""
    if k == 0:
        return F(1, n)
    return F(k, n) * sum(F(1, j) for j in range(k, n))


def check_secretary():
    assert secretary_prob(3, 1) == F(1, 2), "secretary: n = 3, skip 1 wins 1/2"
    assert secretary_prob(4, 1) == F(11, 24) and secretary_prob(4, 2) == F(5, 12), "secretary: n = 4: 11/24 and 5/12"
    probs = {k: secretary_prob(100, k) for k in range(100)}
    best = max(probs, key=probs.get)
    assert 35 <= best <= 38 and abs(float(probs[best]) - 0.371) < 0.002, f"secretary: n = 100 best skip {best}, P = {float(probs[best]):.4f}"
    assert abs(float(probs[37]) - (37 / 100) * log(100 / 37)) < 0.005, "secretary: (k/n) ln(n/k) is within 0.005 of the exact chance at k = 37"
    # brute force n = 3 by enumeration of the six orders
    wins = sum(1 for o in permutations([1, 2, 3]) if (next((x for x in o[1:] if x > o[0]), o[-1]) == 3))
    assert wins == 3


def check_dice_two_three_rolls():
    v2 = sum(max(x, F(7, 2)) for x in range(1, 7)) / 6
    v3 = sum(max(x, v2) for x in range(1, 7)) / 6
    assert v2 == F(17, 4) and v3 == F(14, 3), "dice_two_three_rolls: 4.25 and 14/3"


def check_dice_max_three():
    exact = F(sum(max(a, b, c) for a in range(1, 7) for b in range(1, 7) for c in range(1, 7)), 216)
    assert exact == F(119, 24), "dice_max_three: E[max of three dice] = 119/24"
    assert 6 - F(sum((k - 1) ** 3 for k in range(1, 7)), 216) == F(119, 24), "dice_max_three: tail-sum route"


if __name__ == "__main__":
    checks = [check_dice_max_min, check_dice_abs_diff, check_wald_until_six, check_dice_product, check_reroll_values,
              check_coupon_means, check_coupon_mode, check_coupon_variance, check_distinct_faces, check_pattern_waits,
              check_run_of_three, check_penney, check_runs, check_empty_boxes, check_birthday_pairs, check_birthday_triples,
              check_aces_before_king, check_records, check_hh_count, check_local_maxima, check_red_pairs, check_hats,
              check_cycles, check_two_toys, check_card_game, check_pig_threshold, check_secretary, check_dice_two_three_rolls,
              check_dice_max_three]
    failed = []
    for c in checks:
        try:
            c()
            print("ok", c.__name__)
        except AssertionError as err:
            failed.append(c.__name__)
            print("FAIL", c.__name__, "::", err)
    if failed:
        print("puzzles L1 concepts: FAILED", ", ".join(failed))
        raise SystemExit(1)
    print("puzzles L1 concepts: all checks passed")
