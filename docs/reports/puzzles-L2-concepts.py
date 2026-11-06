"""Concept checks for puzzles L2 (lessons l7 to l12, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/puzzles-L2-concepts.py
Each assert names the ledger row it supports (docs/reports/audit-puzzles-1-3-ledger.md).
"""
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial, pi, sqrt

import numpy as np

rng = np.random.default_rng(20261107)


def mc_band(p, n, k=4):
    return k * sqrt(p * (1 - p) / n)


# ------------------------------------------------- l7 and l8: symmetry of positions
def check_positions():
    n = 400_000
    urn = np.array([1] * 4 + [0] * 6)  # review-2 items[1]: 4 red, 6 blue
    ninth = np.array([rng.permutation(urn)[8] for _ in range(n // 4)])
    assert abs(ninth.mean() - 0.4) < mc_band(0.4, n // 4), "positions: the 9th of 10 unseen balls is red with chance 4/10"
    urn2 = np.array([1] * 5 + [0] * 3)  # l8 quiz[1]: first and last both red 5/14
    perms = np.array([rng.permutation(urn2) for _ in range(n // 4)])
    both = (perms[:, 0] & perms[:, -1]).mean()
    assert abs(both - 5 / 14) < mc_band(5 / 14, n // 4), "positions: first and last both red = 5/14"
    urn3 = np.array([1] * 7 + [0] * 5)  # homework-2 items[5]: last two differ 35/66
    perms = np.array([rng.permutation(urn3) for _ in range(n // 4)])
    differ = (perms[:, -1] != perms[:, -2]).mean()
    assert abs(differ - 35 / 66) < mc_band(35 / 66, n // 4), "positions: last two balls differ with chance 35/66"
    # exact: every position of a uniform random order has the same marginal (enumeration, 5R 3B)
    orders = list(permutations("RRRRRBBB"))
    for k in range(8):
        assert F(sum(1 for o in orders if o[k] == "R"), len(orders)) == F(5, 8), "positions: P(draw k is red) = 5/8 for every k"
    # l7 quiz[1]: bottom card red given the first two are red = 24/50 (exact by symmetry of the 50 unseen)
    assert F(24, 50) == F(12, 25)


def check_after_first_ace():
    # exact: deck of 52 with 4 aces; P(card after the first ace is the A-spades) = 1/52
    total = F(0)
    for j in range(1, 50):  # first ace at position j; positions 1..j-1 non-aces; position j one of the 3 other aces; j+1 the A-spades
        ways = F(factorial(48), factorial(48 - (j - 1))) * 3 * factorial(52 - j - 1)
        total += ways / factorial(52)
    assert total == F(1, 52), f"after_first_ace: exact chance {total} = 1/52"
    # small-deck brute force: 6 cards with 2 aces (A, a) and 4 others: chance the card after the first ace is A is 1/6
    cards = "Aabcde"
    hits = 0
    for o in permutations(cards):
        first = next(i for i, c in enumerate(o) if c in "Aa")
        hits += o[first + 1] == "A"
    assert F(hits, factorial(6)) == F(1, 6), "after_first_ace: brute force on a 6-card deck gives 1/6"


def check_first_special():
    # (n+1)/(k+1) by enumeration on a small deck and by Monte Carlo on 52 cards
    for n, k in [(6, 2), (7, 3), (5, 1)]:
        deck = ["S"] * k + ["o"] * (n - k)
        orders = set(permutations(deck))
        mean = F(sum(next(i for i, c in enumerate(o) if c == "S") + 1 for o in orders), len(orders))
        assert mean == F(n + 1, k + 1), f"first_special: E[first special] = (n+1)/(k+1) for n = {n}, k = {k}"
    nsim = 200_000
    deck = np.array([1] * 4 + [0] * 48)
    pos = np.empty(nsim)
    second = np.empty(nsim)
    reds_before_black = np.empty(nsim)
    deck_rb = np.array([1] * 26 + [0] * 26)
    for i in range(nsim):
        d = rng.permutation(deck)
        idx = np.flatnonzero(d)
        pos[i] = idx[0] + 1
        second[i] = idx[1] + 1
        reds_before_black[i] = np.argmax(rng.permutation(deck_rb) == 0)
    assert abs(pos.mean() - 10.6) < 4 * pos.std() / sqrt(nsim), f"first_special: first ace at 10.6 (got {pos.mean():.3f})"
    assert abs(second.mean() - 21.2) < 4 * second.std() / sqrt(nsim), f"first_special: second ace at 21.2 (got {second.mean():.3f})"
    assert abs(reds_before_black.mean() - 26 / 27) < 4 * reds_before_black.std() / sqrt(nsim), "first_special: reds before the first black = 26/27"
    assert F(53, 14) == F(39, 14) + 1 and F(53, 13) == F(40, 13) + 1 and F(188, 13) == F(200 - 12, 12 + 1)
    assert F(5, 4) == F(5, 3 + 1) and F(6, 5) == F(6, 4 + 1) and F(10, 5) == 2


def check_polya():
    def path_prob(path, r=1, b=1):
        p = F(1)
        for c in path:
            p *= F(r if c == "R" else b, r + b)
            if c == "R":
                r += 1
            else:
                b += 1
        return p

    assert [path_prob(x) for x in ("RR", "RB", "BR", "BB")] == [F(1, 3), F(1, 6), F(1, 6), F(1, 3)], "polya: two-draw path chances"
    assert path_prob("RRB") == F(1, 12), "polya: R, R, B has chance 1/12"
    for n in (3, 4):
        from itertools import product
        counts = {}
        for path in product("RB", repeat=n):
            counts[path.count("R")] = counts.get(path.count("R"), 0) + path_prob(path)
        assert all(counts[j] == F(1, n + 1) for j in range(n + 1)), f"polya: count of reds in {n} draws is uniform"
    assert path_prob("RRBB") == F(1, 30) and path_prob("RBRB") == F(1, 30), "polya: any path with two reds in four draws has chance 1/30"
    # from (2,1): second draw red with chance 2/3
    assert F(2, 3) * F(3, 4) + F(1, 3) * F(2, 4) == F(2, 3), "polya: from 2R 1B the second draw is red with chance 2/3"
    # unseen third draw from (1,1) is red with chance 1/2 (sum over paths)
    from itertools import product
    third = sum(path_prob(p) for p in product("RB", repeat=3) if p[2] == "R")
    assert third == F(1, 2), "polya: unseen third draw is red with chance 1/2"


# ------------------------------------------------------------ l9: Monty Hall protocol
def check_monty_hall():
    n = 400_000
    car = rng.integers(0, 3, n)
    pick = rng.integers(0, 3, n)
    # standard protocol: host knows, always opens an unchosen goat door (random between two goats)
    switch_wins = car != pick
    assert abs(switch_wins.mean() - 2 / 3) < mc_band(2 / 3, n), "monty_hall: switching wins 2/3 under the standard protocol"
    # ignorant host: opens a random unchosen door; condition on it showing a goat
    other = np.array([[d for d in range(3) if d != p] for p in pick])
    opened = other[np.arange(n), rng.integers(0, 2, n)]
    goat_shown = opened != car
    cond = (car != pick)[goat_shown].mean()
    assert abs(cond - 0.5) < mc_band(0.5, goat_shown.sum()), f"monty_hall: with an ignorant host that happens to show a goat, switching wins 1/2 (got {cond:.4f})"
    assert abs(cond - 2 / 3) > 0.1, "monty_hall: the keyed 2/3 depends on the protocol (finding 2)"


# -------------------------------------------------------------- l10: gambler's ruin
def ruin_prob(k, N, p):
    p = F(p)
    q = 1 - p
    if p == q:
        return F(k, N)
    r = q / p
    return (1 - r**k) / (1 - r**N)


def ruin_duration(k, N, p):
    p = F(p)
    q = 1 - p
    if p == q:
        return F(k * (N - k))
    r = q / p
    return F(k) / (q - p) - F(N) / (q - p) * (1 - r**k) / (1 - r**N)


def solve_first_step(k, N, p, reward_fn):
    """Solve x_k = reward + p x_{k+1} + q x_{k-1} exactly with x_0 = x_N = 0 (duration) via Fractions."""
    p = F(p)
    q = 1 - p
    n = N - 1
    A = [[F(0)] * (n + 1) for _ in range(n)]
    for i in range(n):
        s = i + 1
        A[i][i] = F(1)
        if i + 1 < n:
            A[i][i + 1] = -p
        if i - 1 >= 0:
            A[i][i - 1] = -q
        A[i][n] = reward_fn(s)
    for i in range(n):
        piv = next(r for r in range(i, n) if A[r][i] != 0)
        A[i], A[piv] = A[piv], A[i]
        for r in range(n):
            if r != i and A[r][i] != 0:
                f = A[r][i] / A[i][i]
                A[r] = [x - f * y for x, y in zip(A[r], A[i])]
    return [A[i][n] / A[i][i] for i in range(n)][k - 1]


def check_ruin():
    assert ruin_prob(3, 10, F(1, 2)) == F(3, 10) and ruin_duration(3, 10, F(1, 2)) == 21
    assert ruin_prob(3, 10, F(3, 5)) == F(41553, 58025) and abs(float(ruin_prob(3, 10, F(3, 5))) - 0.7161) < 5e-5
    assert ruin_prob(2, 4, F(9, 20)) == F(81, 202) and ruin_prob(10, 20, F(18, 38)) == F(3486784401, 13486784401)
    assert ruin_prob(0, 10, F(3, 5)) == 0 and ruin_prob(10, 10, F(2, 5)) == 1
    assert ruin_prob(5, 20, F(1, 2)) == F(1, 4) and ruin_prob(7, 10, F(1, 2)) == F(7, 10)
    assert ruin_prob(2, 5, F(2, 5)) == F(40, 211) and abs(float(ruin_prob(2, 5, F(2, 5))) - 0.1896) < 5e-5
    assert abs(float(ruin_prob(20, 40, F(13, 25))) - 0.8321) < 5e-5, "ruin: 52% edge from 20 to 40 gives 0.8321"
    assert abs(float(ruin_prob(10, 20, F(18, 38))) - 0.2585) < 5e-5
    assert ruin_duration(3, 10, F(3, 5)) == F(48291, 2321) and ruin_duration(2, 4, F(9, 20)) == F(400, 101) and ruin_duration(2, 5, F(2, 5)) == F(1110, 211)
    assert ruin_duration(5, 10, F(1, 2)) == 25 and ruin_duration(4, 12, F(1, 2)) == 32 and ruin_duration(4, 10, F(1, 2)) == 24 and ruin_duration(2, 5, F(1, 2)) == 6
    assert abs(float(ruin_duration(20, 40, F(13, 25))) - 332) < 0.5, "ruin: about 332 bets from 20 to 40 at p = 0.52"
    assert abs(float(ruin_duration(3, 10, F(5001, 10000))) - 21) < 0.01, "ruin: the general duration tends to k(N-k) as p -> 1/2"
    # independent route: solve the first-step linear systems directly
    for p in (F(3, 5), F(9, 20), F(1, 2)):
        assert solve_first_step(3, 10, p, lambda s: F(1)) == ruin_duration(3, 10, p), "ruin: closed-form duration matches the linear solve"
    # P(reach N) by the linear solve: x_k = p x_{k+1} + q x_{k-1} with x_N = 1 -> reward p at k = N-1
    for p in (F(3, 5), F(9, 20), F(1, 2)):
        got = solve_first_step(3, 10, p, lambda s: p if s == 9 else F(0))
        assert got == ruin_prob(3, 10, p), "ruin: closed-form probability matches the linear solve"
    # no floor: P(ever reach +1) -> p/q = 2/3 for p = 0.4, and -> 1 for p = 1/2 with E[time] = k -> infinity
    for k in (50, 200):
        assert abs(float(ruin_prob(k, k + 1, F(2, 5))) - 2 / 3) < 1e-6, "ruin: floored chance tends to p/q = 2/3"
        assert ruin_prob(k, k + 1, F(1, 2)) == F(k, k + 1) and ruin_duration(k, k + 1, F(1, 2)) == k, "ruin: fair walk: chance k/(k+1), time k"
    roots = np.roots([0.6, -1, 0.4])
    assert sorted(np.round(roots, 9)) == [2 / 3, 1.0] or np.allclose(sorted(roots), [2 / 3, 1]), "ruin: roots of 0.6P^2 - P + 0.4 are 2/3 and 1"
    # Monte Carlo of the walk
    n = 100_000
    for p, k, N, expect in [(0.6, 3, 10, float(ruin_prob(3, 10, F(3, 5)))), (0.5, 3, 10, 0.3)]:
        x = np.full(n, k)
        alive = np.ones(n, dtype=bool)
        steps = np.zeros(n)
        for _ in range(3000):
            if not alive.any():
                break
            move = np.where(rng.random(n) < p, 1, -1)
            x[alive] += move[alive]
            steps[alive] += 1
            alive &= (x > 0) & (x < N)
        assert not alive.any()
        assert abs((x == N).mean() - expect) < mc_band(expect, n), f"ruin: simulated P(reach {N}) at p = {p}"
        assert abs(steps.mean() - float(ruin_duration(k, N, F(p).limit_denominator(100)))) < 4 * steps.std() / sqrt(n), f"ruin: simulated duration at p = {p}"


def check_ruin_conditional():
    """l10 screens[8] explain: with an edge, both winning and losing runs get shorter, and winning runs dominate (3 -> 10)."""
    def cond_durations(k, N, p):
        # h-transform: E[T | win] from the chain conditioned to hit N
        P = {j: float(ruin_prob(j, N, p)) for j in range(N + 1)}
        q = 1 - p
        # conditioned transition from j: up with p P(j+1)/P(j), down with q P(j-1)/P(j)
        n = N - 1
        A = np.zeros((n, n))
        b = np.ones(n)
        for i in range(n):
            j = i + 1
            A[i, i] = 1
            up = p * P[j + 1] / P[j]
            dn = q * P[j - 1] / P[j] if j > 1 else 0.0
            if j + 1 < N:
                A[i, i + 1] = -up
            if j - 1 >= 1:
                A[i, i - 1] = -dn
        win = np.linalg.solve(A, b)[k - 1]
        D = float(ruin_duration(k, N, p))
        lose = (D - P[k] * win) / (1 - P[k])
        return win, lose

    w5, l5 = cond_durations(3, 10, F(1, 2))
    w6, l6 = cond_durations(3, 10, F(3, 5))
    assert abs(w5 - (100 - 9) / 3) < 1e-9, "ruin_conditional: fair E[T | win] = (N^2 - k^2)/3"
    # Content (l10 screens[8].explain, after the audit fix pass): "The edge shortens both the winning runs and the
    # losing ones, but far more runs are now the long winning kind."
    assert w6 < w5 and l6 < l5 and 0.7161 * w6 > 0.3 * w5, f"ruin_conditional: E[T|win] {w5:.2f} -> {w6:.2f}, E[T|lose] {l5:.2f} -> {l6:.2f}"


# ------------------------------------------------------------- l11: order statistics
def check_order_stats():
    assert F(sum(max(a, b, c) for a in range(1, 7) for b in range(1, 7) for c in range(1, 7)), 216) == F(119, 24)
    assert 1 - F(5, 6) ** 3 == F(91, 216) and F(25, 36) == F(5, 6) ** 2
    assert F(sum(1 for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) if min(a, b, c) >= 4), 216) == F(1, 8)
    assert F(sum(1 for a in range(1, 7) for b in range(1, 7) if min(a, b) >= 3), 36) == F(4, 9)
    for n in (6, 10, 4):
        formula = F((n + 1) * (4 * n - 1), 6 * n)
        direct = F(sum(max(a, b) for a in range(1, n + 1) for b in range(1, n + 1)), n * n)
        assert formula == direct, f"order_stats: E[max of two {n}-sided dice] = (n+1)(4n-1)/(6n)"
    assert F(11 * 39, 60) == F(143, 20)
    nsim = 400_000
    u = rng.random((nsim, 3))
    assert abs(u.max(axis=1).mean() - 0.75) < 4 * 0.2 / sqrt(nsim), "order_stats: E[max of 3 uniforms] = 3/4"
    assert abs(np.sort(u, axis=1)[:, 1].mean() - 0.5) < 4 * 0.25 / sqrt(nsim), "order_stats: E[middle of 3 uniforms] = 1/2"
    assert abs((u.max(axis=1) <= 0.5).mean() - 0.125) < mc_band(0.125, nsim), "order_stats: P(max of 3 uniforms <= 0.5) = 1/8"
    u2 = rng.random((nsim, 2))
    assert abs(u2.min(axis=1).mean() - 1 / 3) < 4 * 0.25 / sqrt(nsim), "order_stats: E[min of 2 uniforms] = 1/3"
    u4 = rng.random((nsim, 4))
    assert abs(u4.max(axis=1).mean() - 0.8) < 4 * 0.2 / sqrt(nsim), "order_stats: E[max of 4 uniforms] = 4/5"
    u10 = rng.random((nsim, 10))
    assert abs((u10.max(axis=1) > 0.9).mean() - (1 - 0.9**10)) < mc_band(0.6513, nsim), "order_stats: P(max of 10 uniforms > 0.9) = 1 - 0.9^10"
    z = rng.standard_normal((nsim, 2))
    m = z.max(axis=1)
    assert abs(m.mean() - 1 / sqrt(pi)) < 4 * m.std() / sqrt(nsim), f"order_stats: E[max of two standard normals] = 1/sqrt(pi) (got {m.mean():.4f})"
    assert np.allclose(m, 0.5 * (z[:, 0] + z[:, 1] + np.abs(z[:, 0] - z[:, 1]))), "order_stats: max = (X+Y+|X-Y|)/2 pointwise"
    e = rng.exponential(1.0, (nsim, 3)).min(axis=1)
    assert abs(e.mean() - 1 / 3) < 4 * e.std() / sqrt(nsim), "order_stats: min of three Exp(1) has mean 1/3"
    assert abs((1 - 0.95**20) - 0.6415) < 5e-5, "order_stats: best of 20 null backtests passes 1.645 with chance 0.6415"


# ------------------------------------------------------------------ l12: ants
def simulate_ants(pos, direction, L=1.0):
    """Event-driven bouncing ants (speed 1). Returns (last fall time, collision count)."""
    pos = list(map(float, pos))
    d = list(direction)
    t = 0.0
    collisions = 0
    alive = [True] * len(pos)
    while any(alive):
        # next exit
        t_exit = min((L - pos[i]) if d[i] > 0 else pos[i] for i in range(len(pos)) if alive[i])
        # next collision between neighbours moving towards each other
        order = sorted(i for i in range(len(pos)) if alive[i])
        t_col = float("inf")
        pair = None
        for a, b in zip(order, order[1:]):
            if d[a] > 0 and d[b] < 0:
                tc = (pos[b] - pos[a]) / 2
                if tc < t_col:
                    t_col, pair = tc, (a, b)
        dt = min(t_exit, t_col)
        for i in range(len(pos)):
            if alive[i]:
                pos[i] += d[i] * dt
        t += dt
        if t_col <= t_exit and pair is not None:
            a, b = pair
            d[a], d[b] = -d[a], -d[b]
            collisions += 1
        for i in range(len(pos)):
            if alive[i] and (pos[i] <= 1e-12 or pos[i] >= L - 1e-12):
                alive[i] = False
    return t, collisions


def check_ants():
    t, c = simulate_ants([0.2, 0.7], [1, -1])
    assert abs(t - 0.8) < 1e-9 and c == 1, "ants: two ants at 0.2 (right) and 0.7 (left): last fall 0.8"
    t, _ = simulate_ants([0.3, 0.6], [1, -1])
    assert abs(t - 0.7) < 1e-9, "ants: 0.3 right and 0.6 left: last fall 0.7"
    t, _ = simulate_ants([0.0, 1.0], [1, -1])
    assert abs(t - 1.0) < 1e-9, "ants: from the two ends both fall at 1"
    # the last fall equals the max ghost exit time, for random configurations (n = 10)
    nsim = 3000
    lasts = np.empty(nsim)
    for i in range(nsim):
        pos = np.sort(rng.random(10))
        d = rng.choice([-1, 1], 10)
        t, _ = simulate_ants(pos, d)
        ghost = max((1 - p) if s > 0 else p for p, s in zip(pos, d))
        assert abs(t - ghost) < 1e-9, "ants: last fall = largest ghost exit time"
        lasts[i] = t
    assert abs(lasts.mean() - 10 / 11) < 4 * lasts.std() / sqrt(nsim), f"ants: E[last fall of 10 ants] = 10/11 (got {lasts.mean():.4f})"
    # ghost exit time uniform: 100 ants mean 100/101 (ghost route, 200,000 configurations)
    n = 200_000
    pos = rng.random((n, 100))
    d = rng.random((n, 100)) < 0.5
    exit_t = np.where(d, 1 - pos, pos)
    assert np.abs(np.histogram(exit_t.ravel(), bins=10, range=(0, 1))[0] / exit_t.size - 0.1).max() < 0.001, "ants: ghost exit times are uniform"
    last = exit_t.max(axis=1)
    assert abs(last.mean() - 100 / 101) < 4 * last.std() / sqrt(n), "ants: 100 ants fall by 100/101 on average"
    # collisions: 3 right-walkers on the left half, 2 left-walkers on the right half -> 6; 4 and 4 -> 16
    for k, m in [(3, 2), (4, 4)]:
        pos = list(np.sort(rng.random(k) * 0.5)) + list(0.5 + np.sort(rng.random(m)) * 0.5)
        _, c = simulate_ants(pos, [1] * k + [-1] * m)
        assert c == k * m, f"ants: {k} right-walkers and {m} left-walkers collide {k * m} times (got {c})"


def check_frog():
    w = {1: 1, 2: 2}
    for n in range(3, 11):
        w[n] = w[n - 1] + w[n - 2]
    assert w[10] == 89 and w[9] == 55, "frog: 89 ways with jumps of 1 or 2"
    v = {1: 1, 2: 2, 3: 4}
    for n in range(4, 11):
        v[n] = v[n - 1] + v[n - 2] + v[n - 3]
    assert v[10] == 274 and v[9] == 149, "frog: 274 ways with jumps of 1, 2 or 3"


# ----------------------------------------------------------------- review-2 / homework-2 Bayes
def check_bayes():
    assert F(40, 135) == F(8, 27) and F(99, 594) == F(1, 6) and F(12, 29) == F(12, 29)
    assert F(1024, 1024 + 999) == F(1024, 2023)
    assert F(198, 198 + 998) == F(99, 598) and abs(198 / 1196 - 0.17) < 0.005
    assert F(9801, 9801 + 2475) == F(99, 124) and F(1, 99) * F(198, 10) ** 2 == F(99, 25)
    odds3 = F(1, 99) * F(198, 10) ** 3
    assert abs(float(odds3 / (1 + odds3)) - 0.9874) < 5e-5, "bayes: three positives give 0.9874"
    assert F(99, 99) * F(1, 99) * F(198, 10) == F(1, 5), "bayes: posterior odds 1:5 for one positive"
    assert F(18, 116) == F(9, 58) and F(180, 196) == F(45, 49) and F(99, F(693, 2)) == F(2, 7)
    assert F(1, 2) * F(9, 16) / (F(1, 2) * F(9, 16) + F(1, 2) * F(1, 4)) == F(9, 13) and F(9, 13) * F(3, 4) + F(4, 13) * F(1, 2) == F(35, 52)
    assert F(95, 95 + 4995) == F(19, 1018) and abs(95 / 5090 - 0.0187) < 5e-4
    assert F(24, 42) == F(4, 7)


if __name__ == "__main__":
    checks = [check_positions, check_after_first_ace, check_first_special, check_polya, check_monty_hall, check_ruin,
              check_ruin_conditional, check_order_stats, check_ants, check_frog, check_bayes]
    failed = []
    for c in checks:
        try:
            c()
            print("ok", c.__name__)
        except AssertionError as err:
            failed.append(c.__name__)
            print("FAIL", c.__name__, "::", err)
    if failed:
        print("puzzles L2 concepts: FAILED", ", ".join(failed))
        raise SystemExit(1)
    print("puzzles L2 concepts: all checks passed")
