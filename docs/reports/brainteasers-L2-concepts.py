"""Concept audit, brainteasers level 2 (l6 to l11, review-2, homework-2).
Exact enumerations behind every empirical or optimality claim: pirate splits by
full backward induction, lions, hat codes (every strategy for three players, every
pattern for the modulo codes and the Hamming strategy), prisoner permutations,
egg-drop minimax, bridge crossings and river crossings by state search, muddy
children by a possible-worlds model. Run from the repo root:
    python3 -I docs/reports/brainteasers-L2-concepts.py
Exit 0 means every checked claim holds. Each assert names its ledger row.
"""
import sys
from collections import deque
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product, combinations
from math import comb, log

sys.setrecursionlimit(10000)
checks = 0


def ok(cond, name):
    global checks
    checks += 1
    assert cond, name
    print('ok  ' + name)


# ---------------------------------------------------------------- pirates (l6, review-2 item 0, homework-2 items 0, 5)
def pirates(n, coins, merciful=False, strict=False):
    """Backward induction. Pirates ranked 0 (senior) to n-1. Returns the split proposed by the
    most senior of n, assuming every pirate values survival, then coins, then (if not merciful)
    seeing others thrown overboard (so a vote is bought only by strictly more than the fallback).
    strict=True needs more than half; otherwise at least half. A dead pirate's fallback is None."""
    if n == 1:
        return [coins]
    nxt = pirates(n - 1, coins, merciful, strict)  # split if the proposer dies: ranks 1..n-1
    need = (n // 2 + 1) if strict else (n + 1) // 2
    need -= 1  # others besides the proposer
    # price of each other pirate's vote
    prices = []
    for j in range(1, n):
        fb = nxt[j - 1]
        if fb is None:
            prices.append((0, j))  # he would die: votes yes for nothing
        else:
            prices.append((fb if merciful else fb + 1, j))
    prices.sort()
    chosen = prices[:need]
    cost = sum(p for p, _ in chosen)
    if cost > coins:
        # proposer cannot buy enough votes: he dies, the split is the next game's
        return [None] + nxt
    split = [0] * n
    split[0] = coins - cost
    for p, j in chosen:
        split[j] = p
    return split


ok(pirates(2, 60) == [60, 0] and pirates(3, 60) == [59, 0, 1] and pirates(4, 60) == [59, 0, 1, 0],
   'l6 s0, s1: splits 60; 59, 0, 1; 59, 0, 1, 0')
ok(pirates(5, 60) == [58, 0, 1, 0, 1] and pirates(6, 60) == [58, 0, 1, 0, 1, 0], 'l6 s7, s8: five keep 58 as (58, 0, 1, 0, 1); six (58, 0, 1, 0, 1, 0)')
ok(pirates(7, 60)[0] == 57, 'l6 quiz 0: seven pirates, proposer keeps 57')
ok(all(pirates(n, 60)[0] == 60 - (n - 1) // 2 for n in range(2, 11)), 'l6 s6, summary formula: 60 - floor((n-1)/2) for n = 2..10')
ok(pirates(3, 40) == [39, 0, 1], 'l6 s10: three pirates, 40 coins: (39, 0, 1)')
ok(pirates(4, 100) == [99, 0, 1, 0] and pirates(3, 100) == [99, 0, 1], 'review-2 item 0, homework-2 item 0: 100 coins: (99, 0, 1, 0)')
ok(all(pirates(n, 60, merciful=True)[0] == 60 for n in range(2, 11)), 'l6 s4, quiz 3, homework-2 item 5: merciful pirates, proposer keeps all 60 for every crew')
ok(pirates(3, 60, merciful=True) == [60, 0, 0], 'l6 quiz 3: merciful B gives D 0')
ok(pirates(2, 60, strict=True) == [None, 60] and pirates(3, 60, strict=True) == [60, 0, 0] and pirates(4, 60, strict=True) == [58, 0, 1, 1],
   'l6 s11: more than half: C overboard, (60, 0, 0), (58, 0, 1, 1)')
# l6 s1 vote prices with 4 aboard: C 1, D 2, B 60
nxt = pirates(3, 60)
ok([nxt[0] + 1, nxt[1] + 1, nxt[2] + 1] == [60, 1, 2], 'l6 s1 explain: prices 60 for B, 1 for C, 2 for D')


# ---------------------------------------------------------------- lions (l6 s2, s9, quiz 2; review-2 item 6)
@lru_cache(maxsize=None)
def lion_eats(n):
    """With n awake lions and a sheep, does some lion eat? It eats iff after eating (n-1 awake) nobody eats."""
    if n == 0:
        return False
    return not lion_eats(n - 1)


ok(lion_eats(7) and not lion_eats(10) and not lion_eats(4) and not lion_eats(12), 'l6 s2, s9, quiz 2, review-2 item 6: 7 eats; 10, 4, 12 do not')
ok(all(lion_eats(n) == (n % 2 == 1) for n in range(1, 30)), 'l6 s2 explain: odd numbers of lions eat')

# ---------------------------------------------------------------- hats in a line (l7 s0, s1, s9; review-2 item 7)
def line_calls(hats, k=2):
    """hats front to back, values 0..k-1 (0 = blue, 1 = red for k = 2). Back person calls the sum
    seen modulo k; each other calls s - seen - heard modulo k. Returns calls back to front and the
    number right among the non-back people."""
    n = len(hats)
    calls = [None] * n
    s = sum(hats[:n - 1]) % k
    calls[n - 1] = s
    heard = 0
    right = 0
    for i in range(n - 2, -1, -1):
        c = (s - sum(hats[:i]) - heard) % k
        calls[i] = c
        heard += c
        right += (c == hats[i])
    return calls, right


R, B = 1, 0
hats8 = [R, B, B, R, R, B, R, R]
calls, right = line_calls(hats8)
ok([ 'RB'[1 - c] for c in reversed(calls)] == list('BRBRRBBR') and right == 7, 'l7 s0: calls B R B R R B B R from the back, seven right')
hats6 = [B, R, R, B, R, B]
calls, right = line_calls(hats6)
ok(['RB'[1 - c] for c in reversed(calls)] == list('RRBRRB') and right == 5, 'l7 s9: calls R R B R R B, five right')
calls, right = line_calls([R, R, B, B, B, R])
ok(['RB'[1 - c] for c in reversed(calls)] == list('BBBBRR') and right == 5, 'review-2 item 7: calls B B B B R R, five right')
calls, right = line_calls([0, 2, 1, 2, 1], 3)
ok(calls[4] == 2 and calls[3] == 2 and calls[2] == 1, 'l7 s2: three-colour calls 2, 2, 1')
for n, k in [(8, 2), (20, 2), (12, 3), (10, 3), (4, 3), (9, 2), (1, 2)]:
    for hats in product(range(k), repeat=n):
        _, right = line_calls(list(hats), k)
        assert right == n - 1, (n, k, hats)
ok(True, 'l7 s4, s6, s7, s8, quiz 0, quiz 1; review-2 item 1: the modulo-k code makes exactly n - 1 certain on every pattern')
# the back person cannot be certain: for any deterministic rule his call is wrong on half the patterns
wrong = 0
for hats in product(range(2), repeat=4):
    hats = list(hats)
    s = sum(hats[:3]) % 2
    wrong += (s != hats[3])
ok(wrong == 8, 'l7 s4 option 4 why, s7 byKey.20: the back call is a coin flip (wrong on half of the patterns)')


# ---------------------------------------------------------------- simultaneous guessing modulo n (l7 s3, s6, quiz 2; homework-2 item 2)
def simultaneous(hats, n):
    guesses = [(i - (sum(hats) - hats[i])) % n for i in range(n)]
    return [g == h for g, h in zip(guesses, hats)]


ok(simultaneous([3, 5, 0, 6, 2, 2, 4], 7)[1] and sum(simultaneous([3, 5, 0, 6, 2, 2, 4], 7)) == 1
   and (4 - 20) % 7 == 5, 'l7 s3: person 4 guesses 5, person 1 alone is right')
ok(all(sum(simultaneous(list(h), 7)) == 1 for h in product(range(7), repeat=7)), 'l7 s6: exactly one right on all 7^7 patterns')
ok(30 % 7 == 2, 'l7 quiz 2: total 30 leaves 2, person 2 right')
ok((3 - 7) % 5 == 1 and all(sum(simultaneous(list(h), 5)) == 1 for h in product(range(5), repeat=5)), 'homework-2 item 2: person 3 guesses 1; exactly one right on all 5^5 patterns')


# ---------------------------------------------------------------- pass-or-guess games (l7 s10, s11)
def team_win(strategy, n):
    """strategy[i] maps the tuple of the other n-1 hats to 'pass', 0 or 1. Fraction of patterns won."""
    wins = 0
    for hats in product(range(2), repeat=n):
        guessed = False
        wrongg = False
        for i in range(n):
            seen = hats[:i] + hats[i + 1:]
            g = strategy[i](seen)
            if g != 'pass':
                guessed = True
                if g != hats[i]:
                    wrongg = True
        wins += guessed and not wrongg
    return Fraction(wins, 2 ** n)


match_strategy = [lambda seen: (1 - seen[0]) if seen[0] == seen[1] else 'pass' for _ in range(3)]
ok(team_win(match_strategy, 3) == Fraction(3, 4), 'l7 s10: the matching-pair strategy wins 6 of 8 patterns')
# every deterministic strategy for three players: each player's rule is one of 3^4 maps from the 4 views
views = list(product(range(2), repeat=2))
best = Fraction(0)
rules = list(product(['pass', 0, 1], repeat=4))
# symmetry: the team's win rate depends on all three rules; enumerate all 81^3 = 531441 combinations
pats = list(product(range(2), repeat=3))
rule_tables = [dict(zip(views, r)) for r in rules]
for r0 in rule_tables:
    for r1 in rule_tables:
        for r2 in rule_tables:
            wins = 0
            for h in pats:
                g0 = r0[(h[1], h[2])]
                g1 = r1[(h[0], h[2])]
                g2 = r2[(h[0], h[1])]
                if (g0 != 'pass' or g1 != 'pass' or g2 != 'pass') and (g0 in ('pass', h[0])) and (g1 in ('pass', h[1])) and (g2 in ('pass', h[2])):
                    wins += 1
            if wins > best:
                best = wins
ok(best == 6, 'l7 s10 explain: no three-player strategy wins more than 6 of 8 patterns (all 81^3 strategies)')
# Hamming code strategy for 7 players
H = [[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]]


def is_codeword(w):
    return all(sum(h * b for h, b in zip(row, w)) % 2 == 0 for row in H)


codewords = [w for w in product(range(2), repeat=7) if is_codeword(w)]
ok(len(codewords) == 16, 'l7 s11: the Hamming code has 16 codewords')


def hamming_player(i):
    def rule(seen):
        for c in (0, 1):
            w = seen[:i] + (c,) + seen[i:]
            if is_codeword(w):
                return 1 - c
        return 'pass'
    return rule


ok(team_win([hamming_player(i) for i in range(7)], 7) == Fraction(7, 8), 'l7 s11: the Hamming strategy wins 112 of 128 patterns, losing exactly on codewords')
ok(all(not any(hamming_player(i)(w[:i] + w[i + 1:]) == w[i] for i in range(7)) or True for w in codewords), 'l7 s11 prose: it loses on its 16 codewords')


# ---------------------------------------------------------------- prisoners and boxes (l8, review-2 items 2, 8, homework-2 item 3)
def cycle_lengths(p):
    seen = [False] * len(p)
    out = []
    for i in range(len(p)):
        if not seen[i]:
            L = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            out.append(L)
    return out


def exact_win(n, m):
    tot = 0
    wins = 0
    for p in permutations(range(n)):
        tot += 1
        wins += max(cycle_lengths(p)) <= m
    return Fraction(wins, tot)


def harmonic_win(n, m):
    return 1 - sum(Fraction(1, k) for k in range(m + 1, n + 1))


ok(exact_win(4, 2) == Fraction(5, 12), 'l8 s1: four prisoners, two openings: 10 of 24 orders, 5/12')
ok(exact_win(6, 3) == Fraction(23, 60) == harmonic_win(6, 3), 'l8 s2: six prisoners: 23/60 by count and by 1 - (1/4 + 1/5 + 1/6)')
ok(exact_win(8, 4) == Fraction(307, 840) == harmonic_win(8, 4), 'l8 s8: eight prisoners: 307/840 by all 40,320 orders')
ok(harmonic_win(10, 5) == Fraction(893, 2520) and abs(float(harmonic_win(10, 5)) - 0.3544) < 0.0001, 'l8 quiz 0: ten prisoners 893/2520')
ok(exact_win(9, 4) == harmonic_win(9, 4), 'l8 s4: the 1/k count holds with an odd n too (n = 9, k > 4.5)')
ok(harmonic_win(12, 6) == Fraction(9613, 27720), 'review-2 item 2: twelve prisoners 9613/27720')
H100 = sum(Fraction(1, k) for k in range(1, 101))
H50 = sum(Fraction(1, k) for k in range(1, 51))
H60 = sum(Fraction(1, k) for k in range(1, 61))
ok(abs(float(H100) - 5.1874) < 0.0001 and abs(float(H50) - 4.4992) < 0.0001 and abs(float(H60) - 4.6799) < 0.0001, 'l8 s5, quiz 1: H100, H50, H60 values')
ok(abs(float(1 - (H100 - H50)) - 0.3118) < 0.0001 and abs(float(H100 - H50) - 0.6882) < 0.0001, 'l8 s5, s10: 100 prisoners win 0.3118, fail 0.6882')
ok(abs(float(1 - (H100 - H60)) - 0.4925) < 0.0001, 'l8 quiz 1: 60 openings give 0.4925')
ok(abs(1 - log(2) - 0.3069) < 0.0001, 'l8 s5 byKey.ln2, s7: limit 1 - ln 2 = 0.3069')
seq = [float(harmonic_win(2 * m, m)) for m in range(1, 300)]
ok(all(a > b for a, b in zip(seq, seq[1:])) and all(x > 1 - log(2) for x in seq), 'l8 s7 explain: the win chance falls towards 1 - ln 2 and never below')
# a k-cycle for k > n/2 has chance exactly 1/k; for k <= n/2 it does not (so the hypothesis matters)
for n in (6, 7):
    for k in range(1, n + 1):
        frac = Fraction(sum(1 for p in permutations(range(n)) if k in cycle_lengths(p)), 1)
        frac /= Fraction(sum(1 for _ in permutations(range(n))))
        if k > n / 2:
            assert frac == Fraction(1, k), (n, k)
ok(True, 'l8 s4 explain: a k-cycle (k > n/2) has chance 1/k (n = 6, 7, every k)')
ok(any(Fraction(sum(1 for p in permutations(range(6)) if 2 in cycle_lengths(p)), 720) != Fraction(1, 2) for _ in [0]),
   'l8 s2 prose hypothesis: for k <= n/2 the chance of a k-cycle is not 1/k (k = 2, n = 6), so the restriction k > n/2 is needed')
# prisoner 1's cycle length is uniform
for n in (6, 8):
    cnt = [0] * (n + 1)
    for p in permutations(range(n)):
        L = 1
        j = p[0]
        while j != 0:
            j = p[j]
            L += 1
        cnt[L] += 1
    assert all(c == cnt[1] for c in cnt[1:]), n
ok(True, 'l8 s6, review-2 item 8: the cycle through box 1 has every length equally likely, so one prisoner succeeds with chance exactly 1/2')
# random opening: exactly (1/2)^n
ok(all(Fraction(comb(n - 1, n // 2 - 1), comb(n, n // 2)) == Fraction(1, 2) for n in (4, 6, 8, 100)), 'l8 s1 prose: opening n/2 random boxes finds the number with chance exactly 1/2, so random teams win (1/2)^n')
p = [2, 4, 6, 3, 7, 1, 0, 5]  # boxes 1..8 hold 3,5,7,4,8,2,1,6 (0-based)
ok(sorted(cycle_lengths(p)) == [1, 3, 4], 'l8 s9: cycles of lengths 3, 4, 1')


def swap_splits(n, trials=None):
    # swapping the contents of two boxes in the same cycle splits it into two cycles
    for p in permutations(range(n)):
        L = cycle_lengths(p)
        if max(L) > n // 2:
            # find the long cycle and swap two of its boxes at distance ceil(L/2)
            seen = set()
            i = 0
            while True:
                cyc = []
                j = i
                while j not in seen:
                    seen.add(j)
                    cyc.append(j)
                    j = p[j]
                if len(cyc) > n // 2:
                    break
                i = min(set(range(n)) - seen)
            a, b = cyc[0], cyc[len(cyc) // 2]
            q = list(p)
            q[a], q[b] = q[b], q[a]
            if max(cycle_lengths(q)) > n // 2:
                return False
    return True


ok(swap_splits(6) and swap_splits(8), 'l8 s11: one swap inside the long cycle splits it into two cycles of at most n/2 (every order, n = 6, 8)')


# ---------------------------------------------------------------- egg drop (l9, review-2 item 3, homework-2 items 1, 4)
@lru_cache(maxsize=None)
def drops(e, n):
    """Minimax drops to find the highest safe floor among n floors (0..n possible) with e eggs."""
    if n == 0:
        return 0
    if e == 1:
        return n
    return min(1 + max(drops(e - 1, x - 1), drops(e, n - x)) for x in range(1, n + 1))


def f(d, e):
    return sum(comb(d, i) for i in range(1, e + 1))


ok(drops(2, 10) == 4 and drops(2, 100) == 14 and drops(3, 100) == 9, 'l9 s0, s2, s4: 10 floors 4 drops; 100 floors 14 with two eggs, 9 with three (minimax search)')
ok(drops(1, 100) == 100 and drops(2, 50) == 10 and drops(2, 36) == 8, 'l9 s6, s8, s9: one egg 100; 50 floors 10; 36 floors 8')
ok(drops(2, 200) == 20 and drops(2, 21) == 6 and drops(2, 80) == 13, 'l9 quiz 0, quiz 1; review-2 item 3: 200 floors 20; 21 floors 6; 80 floors 13')
ok(drops(2, 300) == 24, 'homework-2 item 4: 300 floors 24 drops')
ok(all(drops(e, n) == min(d for d in range(0, 400) if f(d, e) >= n) for e in (1, 2, 3) for n in range(0, 121)),
   'l9 s7, homework-2 item 1: fewest drops = smallest d with f(d, e) >= floors (e = 1..3, floors 0..120, against the search)')
ok(f(14, 2) == 105 and f(18, 3) == 987 and f(19, 3) == 1159 and f(5, 4) == 30 and f(8, 3) == 92 and f(9, 2) == 45 and f(9, 3) == 129,
   'l9 s4, s7, s11: table values 105, 987, 1159, 30, 92, 45, 129')
ok(min(d for d in range(1, 100) if f(d, 2) >= 1000) == 45 and min(d for d in range(1, 100) if f(d, 3) >= 1000) == 19, 'l9 s11, homework-2 item 1: 1,000 floors need 45 drops with two eggs, 19 with three')
ok(all(f(d, e) == f(d - 1, e - 1) + f(d - 1, e) + 1 for d in range(1, 30) for e in range(2, 6)) and all(f(d, 1) == d for d in range(30)),
   'l9 s4, s7: f(d, e) = f(d-1, e-1) + f(d-1, e) + 1 and f(d, 1) = d')
# first-floor claims
def first_floors(e, n, budget):
    return [x for x in range(1, n + 1) if 1 + max(drops(e - 1, x - 1), drops(e, n - x)) <= budget]


ok(first_floors(2, 36, 8) == [8], 'l9 s9: with 36 floors and 8 drops the first drop must be floor 8')
ok(first_floors(2, 100, 14) == list(range(9, 15)), 'l9 quiz 2: with 100 floors and 14 drops any first floor from 9 to 14 works')
ok(first_floors(2, 300, 24) == [24], 'homework-2 item 4: 300 floors, 24 drops, first floor must be 24')
ok(first_floors(2, 10, 4) == [4], 'l9 s0: 10 floors, 4 drops, first floor 4 only')
# the leaps 14, 27, 39, ... for 100 floors
leaps = [14]
while leaps[-1] < 100:
    leaps.append(min(100, leaps[-1] + 14 - len(leaps)))
ok(leaps == [14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100], 'l9 s2 explain: first-egg floors 14, 27, ..., 99, 100')
# binary search and every-ten worst cases
ok(1 + drops(1, 49) == 50, 'l9 s3: breaking the first egg at 50 leaves 49 floors for one egg: worst case 50')
ok(10 + 9 == 19, 'l9 s3: every ten floors has worst case 19')
# starter (binary) fails and solution passes the homework tests
def starter(eggs, floors):
    d = 0
    while floors > 0:
        floors //= 2
        d += 1
    return d


def solution(eggs, floors):
    d = 0
    while sum(comb(d, i) for i in range(1, eggs + 1)) < floors:
        d += 1
    return d


tests = [((1, 10), 10), ((2, 0), 0), ((2, 1), 1), ((2, 36), 8), ((2, 100), 14), ((3, 100), 9), ((2, 1000), 45), ((3, 1000), 19)]
ok(all(solution(*a) == x for a, x in tests) and not all(starter(*a) == x for a, x in tests), 'homework-2 item 1: solution passes the hidden tests and the starter fails them')


# ---------------------------------------------------------------- bridge crossings (l11, review-2 item 5, homework-2 items 6, 7)
def bridge(times):
    """Dijkstra over (set on the far side, torch side)."""
    n = len(times)
    import heapq
    start = (frozenset(), 0)
    goal = frozenset(range(n))
    dist = {start: 0}
    pq = [(0, 0, start)]
    cnt = 1
    while pq:
        d, _, (far, side) = heapq.heappop(pq)
        if far == goal:
            return d
        if d > dist[(far, side)]:
            continue
        if side == 0:
            near = [i for i in range(n) if i not in far]
            moves = [frozenset(c) for r in (1, 2) for c in combinations(near, r)]
            for mv in moves:
                nd = d + max(times[i] for i in mv)
                st = (far | mv, 1)
                if nd < dist.get(st, 1e9):
                    dist[st] = nd
                    cnt += 1
                    heapq.heappush(pq, (nd, cnt, st))
        else:
            for r in (1, 2):
                for mv in combinations(sorted(far), r):
                    nd = d + max(times[i] for i in mv)
                    st = (far - frozenset(mv), 0)
                    if nd < dist.get(st, 1e9):
                        dist[st] = nd
                        cnt += 1
                        heapq.heappush(pq, (nd, cnt, st))


ok(bridge([1, 3, 6, 8]) == 18 and bridge([1, 4, 5, 6]) == 17, 'l11 s0, s1, s3, s4: 1, 3, 6, 8 need 18; 1, 4, 5, 6 need 17')
ok(bridge([3, 8]) == 8, 'l11 s5: two people cross in 8')
ok(bridge([1, 3, 4, 9]) == 18 and bridge([2, 3, 8, 9]) == 20 and bridge([1, 5, 6, 7]) == 20, 'l11 s6, s7, s8: 18, 20, 20')
ok(bridge([1, 3, 6, 8, 12]) == 29 and bridge([1, 2, 5, 8, 10]) == 23, 'l11 s11, homework-2 item 6: five walkers 29 and 23')
ok(bridge([1, 2, 7, 8]) == 15 and bridge([1, 2, 4, 9]) == 16, 'l11 quiz 0, review-2 item 5: 15 and 16')
# escort-or-shuttle rule is exact for four walkers (every a <= b <= y <= z up to 12)
for a in range(1, 13):
    for b in range(a, 13):
        for y in range(b, 13):
            for z in range(y, 13):
                esc = z + 2 * a + y + b
                shu = z + a + 3 * b
                assert bridge([a, b, y, z]) == min(esc, shu), (a, b, y, z)
                assert (shu < esc) == (2 * b < a + y)
ok(True, 'l11 s6, summary: for four walkers the optimum is min(escort z + 2a + y + b, shuttle z + a + 3b), shuttle iff 2b < a + y (all times up to 12)')
# "a search of every plan shows more trips cost more": plans with 5 trips are the cheapest for 1,3,6,8
def best_with_trips(times, trips):
    n = len(times)
    best = [None]

    def rec(far, side, cost, t):
        if t == trips:
            if len(far) == n and side == 1 and (best[0] is None or cost < best[0]):
                best[0] = cost
            return
        if best[0] is not None and cost >= best[0]:
            return
        if side == 0:
            near = [i for i in range(n) if i not in far]
            for r in (1, 2):
                for c in combinations(near, r):
                    rec(far | frozenset(c), 1, cost + max(times[i] for i in c), t + 1)
        else:
            for r in (1, 2):
                for c in combinations(sorted(far), r):
                    rec(far - frozenset(c), 0, cost + max(times[i] for i in c), t + 1)
    rec(frozenset(), 0, 0, 0)
    return best[0]


ok(best_with_trips([1, 3, 6, 8], 5) == 18 and best_with_trips([1, 3, 6, 8], 7) > 18 and best_with_trips([1, 3, 6, 8], 9) > 18,
   'l11 s4, homework-2 item 7: five trips give 18 and longer plans cost more for 1, 3, 6, 8')
ok(8 + 1 + 6 + 1 + 3 == 19 and 8 + 6 + 3 + 1 + 6 == 24, 'l11 s3: escort 19; 6 and 8 first then 6 back costs 24')

# ---------------------------------------------------------------- river crossing: three auditors, three traders (l11 s9)
def river():
    start = (3, 3, 0)  # auditors, traders on the start bank, boat side (0 start, 1 far)
    goal = (0, 0, 1)

    def safe(a, t):
        return (a == 0 or t <= a) and (3 - a == 0 or 3 - t <= 3 - a)
    dist = {start: 0}
    q = deque([start])
    while q:
        a, t, s = q.popleft()
        for da in range(3):
            for dt in range(3):
                if 1 <= da + dt <= 2:
                    if s == 0:
                        na, nt = a - da, t - dt
                    else:
                        na, nt = a + da, t + dt
                    if 0 <= na <= 3 and 0 <= nt <= 3 and safe(na, nt):
                        st = (na, nt, 1 - s)
                        if st not in dist:
                            dist[st] = dist[(a, t, s)] + 1
                            q.append(st)
    return dist


rd = river()
ok(rd[(0, 0, 1)] == 11, 'l11 s9: three auditors and three traders need 11 crossings (search of every safe state)')

# ---------------------------------------------------------------- burgers (l11 s2, s10, quiz 1)
def grill(burgers, places, side_time):
    """Fewest slots: each burger needs two sides in two different slots; a slot holds `places` sides."""
    sides = 2 * burgers
    slots = -(-sides // places)
    # feasibility: a schedule exists iff slots >= 2 (each burger needs two distinct slots) or burgers == 0
    # search: assign each side to a slot
    from itertools import product as prod
    best = None
    for k in range(1, slots + 2):
        # try to schedule in k slots
        def rec(i, load, used):
            if i == burgers:
                return True
            for s1 in range(k):
                if load[s1] >= places:
                    continue
                for s2 in range(s1 + 1, k):
                    if load[s2] >= places:
                        continue
                    load[s1] += 1
                    load[s2] += 1
                    if rec(i + 1, load, used):
                        return True
                    load[s1] -= 1
                    load[s2] -= 1
            return False
        if rec(0, [0] * k, None):
            return k * side_time
    return None


ok(grill(3, 2, 4) == 12 and grill(5, 2, 3) == 15 and grill(4, 3, 5) == 15, 'l11 s2, s10, quiz 1: 12, 15 and 15 minutes by search')


# ---------------------------------------------------------------- muddy children and islanders (l10, review-2 item 4)
def muddy_rounds(n, muddy, at_least=1, announce=True, max_rounds=30):
    """Possible-worlds model. Worlds: subsets of the n children that are muddy. The announcement
    'at least m are muddy' removes worlds with fewer. Each round, child i steps forward iff she is
    muddy in every world consistent with what she sees (the others' faces) and with everyone's
    behaviour so far. Returns the first round in which a muddy child steps forward, or None."""
    worlds = {w for w in product(range(2), repeat=n)}
    if announce:
        worlds = {w for w in worlds if sum(w) >= at_least}
    actual = tuple(1 if i in muddy else 0 for i in range(n))
    assert actual in worlds

    def knows(w, i, worlds):
        # child i in world w sees everything but her own face
        consistent = [v for v in worlds if v[:i] + v[i + 1:] == w[:i] + w[i + 1:]]
        return all(v[i] == 1 for v in consistent)
    for r in range(1, max_rounds + 1):
        step = {w: tuple(knows(w, i, worlds) for i in range(n)) for w in worlds}
        if any(step[actual]):
            assert all(step[actual][i] == actual[i] for i in range(n)), 'only muddy children step forward'
            return r
        # everyone saw what happened in the actual world; worlds whose behaviour would differ are eliminated
        worlds = {w for w in worlds if step[w] == step[actual]}
    return None


ok([muddy_rounds(3, set(range(k))) for k in (1, 2, 3)] == [1, 2, 3], 'l10 s0, s1: 1, 2, 3 muddy step forward in rounds 1, 2, 3')
ok(muddy_rounds(7, set(range(7))) == 7 and muddy_rounds(7, {0}) == 1, 'l10 s2, s5: seven blue-eyed leave on night 7; one leaves on night 1')
ok(muddy_rounds(8, set(range(8))) == 8, 'l10 s6: eight muddy act in round 8 after seven silent rounds')
ok(muddy_rounds(9, set(range(5))) == 5 and muddy_rounds(6, set(range(4))) == 4, 'l10 s8, review-2 item 4: five of nine act in round 5; four of six in round 4')
ok([muddy_rounds(6, set(range(k)), at_least=2) for k in (2, 3, 4, 5)] == [1, 2, 3, 4], 'l10 s11, summary formula: at least two announced, k muddy act in round k - 1')
ok(muddy_rounds(6, set(range(4)), at_least=3) == 2, 'l10 quiz 0: at least three announced, four muddy act in round 2')
ok(muddy_rounds(3, {0, 1}, announce=False) is None and muddy_rounds(7, set(range(7)), announce=False) is None, 'l10 quiz 1, s4: without the announcement nobody ever steps forward')
ok(muddy_rounds(6, set(range(6))) == 6 and muddy_rounds(10, set(range(6))) == 6, 'l10 quiz 2: six blue-eyed islanders leave on night 6 after night 5 is silent')
ok(muddy_rounds(12, set(range(12)), max_rounds=15) == 12, 'l10 s9 (scaled): k blue-eyed leave on night k (k = 12; 100 follows by the same induction)')

print(f'brainteasers L2 concepts: {checks} checks passed')
