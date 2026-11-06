"""Concept audit, brainteasers level 3 (l12 to l16, review-3, homework-3).
Exact checks behind every empirical, optimality or numerical-rule claim: clock
angles and event counts by direct computation, doubling times and the rule of 72
against the exact formula, constants, last digits and trailing zeros from the
integers themselves, sums by direct addition, and the mixed set's searches
(coins, weighings, tilings, pirates, bridges, prisoners, eggs, jugs).
Run from the repo root:
    python3 -I docs/reports/brainteasers-L3-concepts.py
Exit 0 means every checked claim holds. Each assert names its ledger row.
"""
import sys
from collections import deque
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb, log, factorial, sqrt, pi, e, isclose, gcd

sys.setrecursionlimit(10000)
checks = 0


def ok(cond, name):
    global checks
    checks += 1
    assert cond, name
    print('ok  ' + name)


# ---------------------------------------------------------------- clocks (l12, l16 quiz 2, review-3 item 0, homework-3 item 2)
def hands(h, m):
    minute = 6.0 * m
    hour = 30.0 * (h % 12) + 0.5 * m
    return hour, minute


def angle(h, m):
    a, b = hands(h, m)
    d = abs(a - b) % 360
    return min(d, 360 - d)


def formula(h, m):
    t = abs(30 * h - 5.5 * m)
    return 360 - t if t > 180 else t


ok(hands(3, 40) == (110.0, 240.0) and angle(3, 40) == 130, 'l12 s0: at 3:40 the hands are at 110 and 240 degrees, 130 apart')
for (h, m), want in [((9, 15), 172.5), ((2, 20), 50), ((6, 30), 15), ((4, 50), 155), ((10, 10), 115), ((12, 0), 0)]:
    assert angle(h, m) == want and formula(h, m) == want, (h, m)
ok(True, 'l12 s5, s7, s8, quiz 2; l16 quiz 2; review-3 item 0: formula |30h - 5.5m| (then 360 - theta) agrees with the hand positions at 9:15, 2:20, 6:30, 4:50, 10:10, 12:00')
ok(all(isclose(formula(h, m), angle(h, m)) for h in range(1, 13) for m in range(60)), 'l12 s5 formula: agrees with the hand positions at every minute of 12 hours')
ok(isclose(90 / 5.5, 180 / 11) and isclose(180 / 11, 16.36, abs_tol=0.005), 'l12 s1: hands meet 180/11 = 16.36 minutes after 3:00')


def count_events(hours, target):
    """Count the minutes t in [0, hours*60) at which the relative angle (5.5 t mod 360) equals target."""
    # relative angle 5.5 t; solutions t = (target + 360 k) / 5.5
    n = 0
    k = 0
    while True:
        t = (target + 360 * k) / 5.5
        if t >= hours * 60:
            break
        n += 1
        k += 1
    return n


ok(count_events(12, 0) == 11 and isclose(720 / 11, 65 + 5 / 11), 'l12 s1 explain, summary note: the hands meet 11 times in 12 hours, every 720/11 minutes')
ok(count_events(12, 90) + count_events(12, 270) == 22, 'l12 s9: right angles 22 times in 12 hours')
ok(count_events(24, 180) == 22 and count_events(12, 180) == 11, 'l12 s11: opposite 22 times in a day, 11 in 12 hours')
ok(count_events(24, 90) + count_events(24, 270) == 44, 'l12 s9 byKey.day: 44 right angles in a day')
ok(isclose(30 / 5.5, 60 / 11) and isclose(60 / 11, 5.45, abs_tol=0.005) and isclose(210 / 5.5, 38.18, abs_tol=0.005),
   'homework-3 item 2: opposite 60/11 = 5.45 minutes after 7:00; the hands meet after 38.18')

# ---------------------------------------------------------------- rates (l12, l16 s9, review-3 item 4)
ok(isclose(6 / 18 * 60, 20) and isclose(6 / 90 * 60, 4) and isclose(6 / 162 * 60, 2.22, abs_tol=0.005), 'l12 s2: 20 minutes; 4 ignores the lorry; 2.22 adds the speeds')
hm = lambda a, b: 2 * a * b / (a + b)
ok(isclose(240 / (2 + 3), 48) and isclose(hm(60, 40), 48) and isclose(hm(30, 60), 40) and isclose(hm(45, 90), 60), 'l12 s3, s6; l16 s9; review-3 item 4: harmonic means 48, 40, 60')
ok(isclose(40 / 80 * 60, 30) and isclose(20 / 40 * 60, 30) and isclose(40 / (30 + 20 / 160 * 60) * 60, 64), 'l12 s4: the 80 km/h budget is 30 minutes, all spent; at 160 back the average is 64')
ok(isclose(1 / (1 / 4 + 1 / 12), 3) and isclose(1 / (1 / 6 - 1 / 9), 18) and isclose(60 / 2.5, 24), 'l12 s10, quiz 3, quiz 1: pipes 3 hours, tap and drain 18 hours, walkway 24 s')
ok(isclose(200 / (100 / 40 + 100 / 60), 48), 'l12 quiz 0: equal pounds at 40 and 60 average 48 a share')

# ---------------------------------------------------------------- rule of 72 and doubling (l15, review-3 item 3, homework-3 items 6, 7)
T = lambda r: log(2) / log(1 + r)
ok(isclose(T(0.08), 9.006, abs_tol=0.0005) and isclose(T(0.06), 11.90, abs_tol=0.005) and isclose(T(0.36), 2.254, abs_tol=0.0005),
   'l15 s3, s4: exact doubling 9.006 at 8%, 11.90 at 6%, 2.254 at 36%')
ok(isclose(8 * T(0.08), 72.05, abs_tol=0.005) and isclose(36 * T(0.36), 81, abs_tol=0.2), 'l15 s3, s4: the numerator r T is 72.05 at 8% and about 81 at 36%')
ok(abs(72 / 8 - T(0.08)) < abs(69.3 / 8 - T(0.08)) and isclose(abs(69.3 / 8 - T(0.08)), 0.34, abs_tol=0.01), 'l15 s3: at 8% the rule of 72 is closer than 69.3 (off by 0.006 against 0.34)')
rs = [i / 1000 for i in range(1, 1001)]
ok(all(a < b for a, b in zip([r * T(r) for r in rs], [r * T(r) for r in rs][1:])), 'l15 s3 explain, homework-3 model: the right numerator r T rises with the rate (r up to 100%)')
ok(isclose(log(1.36), 0.3075, abs_tol=0.00005) and isclose(log(2), 0.6931, abs_tol=0.00005) and isclose(log(1.72), 0.5423, abs_tol=0.00005),
   'l15 s4, quiz 1: ln 1.36 = 0.3075, ln 2 = 0.6931, ln 1.72 = 0.5423')
ok(isclose(T(0.09), 8.04, abs_tol=0.005) and isclose(T(0.72), 1.278, abs_tol=0.0005) and isclose(T(0.04), 17.67, abs_tol=0.005) and isclose(T(0.07), 10.24, abs_tol=0.005),
   'l15 s8, quiz 1; review-3 item 3; homework-3 model: 8.04 at 9%, 1.278 at 72%, 17.67 at 4%, 10.24 at 7%')
ok(isclose(log(4) / log(1.08), 18.01, abs_tol=0.005) and isclose(log(10) / log(1.08), 29.92, abs_tol=0.005) and isclose(log(8) / log(1.09), 24.13, abs_tol=0.005),
   'l15 s10, s11; homework-3 item 6: 18.01, 29.92, 24.13 years')
ok(isclose(log(10) / log(2), 3.32, abs_tol=0.005), 'l15 s11: log2 10 = 3.32')
ok(isclose(log(1.07), 0.06766, abs_tol=0.000005) and isclose(0.07 - 0.07 ** 2 / 2, 0.06755) and isclose(69.3 * (1 + 0.04), 72.07, abs_tol=0.005),
   'homework-3 model: ln 1.07 = 0.06766, r - r^2/2 = 0.06755, 69.3(1 + r/2) = 72.07 at 8%')
ok(all(72 % d == 0 for d in (2, 3, 4, 6, 8, 9, 12, 18)) and isclose(log(2) / 0.08 * 8, 69.3, abs_tol=0.02), 'homework-3 model: 72 divides by 2, 3, 4, 6, 8, 9, 12, 18; continuous compounding numerator 69.3')
ok(isclose(1 / 0.08, 12.5), 'l15 s6 d1 why: simple interest gives 12.5 years at 8%')

# ---------------------------------------------------------------- constants (l15, homework-3 item 5, review-3 item 7)
ok(2 ** 19 == 524288 and 2 ** 20 == 1048576 and 2 ** 30 == 1073741824 and isclose(2 ** 32 / 1e9, 4.29, abs_tol=0.005) and 2 ** 16 == 65536,
   'l15 s0, s1, quiz 4: powers of two')
ok(isclose(1.024 ** 3, 1.074, abs_tol=0.0005) and isclose(1.024 ** 10, 1.27, abs_tol=0.005) and 2 ** 100 > 10 ** 30 and isclose(2 ** 100 / 10 ** 30, 1.27, abs_tol=0.005),
   'l15 s1 byKey.rough; review-3 item 7: the 2.4% excess compounds to 7.4% by 2^30 and 27% by 2^100')
ok(1.41 ** 2 < 2 < 1.42 ** 2 and 1.415 ** 2 > 2 and isclose(1.415 ** 2, 2.0022, abs_tol=0.00005) and round(sqrt(2), 2) == 1.41, 'l15 s2: sqrt 2 brackets and rounds to 1.41')
ok(2.235 ** 2 < 5 and round(sqrt(5), 2) == 2.24 and isclose(2.235 ** 2, 4.9952, abs_tol=0.00005), 'homework-3 item 5: sqrt 5 rounds up to 2.24 since 2.235^2 = 4.9952 < 5')
table = {'sqrt2': (sqrt(2), 1.414), 'sqrt3': (sqrt(3), 1.732), 'e': (e, 2.718), '1/e': (1 / e, 0.368), 'ln2': (log(2), 0.693), 'ln10': (log(10), 2.303), 'pi2': (pi ** 2, 9.870)}
ok(all(isclose(v, t, abs_tol=0.0005) for v, t in table.values()), 'l15 s5: the table of constants to three decimals')
ok(isclose(log(5), 1.6094, abs_tol=0.00005) and isclose(2.303 - 0.693, 1.610), 'l15 s5: ln 5 = ln 10 - ln 2 = 1.61')
ok(isclose(pi ** 2, 9.8696, abs_tol=0.00005) and isclose(9 + 2 * 3 * 0.1416 + 0.1416 ** 2, 9.8696, abs_tol=0.0001), 'l15 s7: pi^2 = 9.8696 by (3 + 0.1416)^2')
ok(isclose(1.01 ** 100, 2.7048, abs_tol=0.00005) and isclose(100 * log(1.01), 0.995, abs_tol=0.0005) and 1.01 ** 100 < e, 'l15 s9: 1.01^100 = 2.7048, below e')
ok(isclose(0.99 ** 100, 0.3660, abs_tol=0.00005) and isclose(log(0.99), -0.01005, abs_tol=0.000005) and 0.99 ** 100 < 1 / e, 'l15 quiz 2: 0.99^100 = 0.3660, below 1/e')
ok(e ** pi > pi ** e and isclose(e ** pi, 23.14, abs_tol=0.005) and isclose(pi ** e, 22.46, abs_tol=0.005) and isclose(e * log(pi), 3.1117, abs_tol=0.00005),
   'l15 quiz 0: e^pi = 23.14 beats pi^e = 22.46; e ln pi = 3.1117')
ok(isclose(0.3 * 2.303, 0.691, abs_tol=0.0005) and isclose(log(2), 0.6931, abs_tol=0.00005), 'l15 quiz 3: ln 2 = 0.3 ln 10 = 0.691 against 0.6931')
ok(isclose(2.718 * 0.995, 2.704, abs_tol=0.0005) and isclose(0.368 * 0.995, 0.366, abs_tol=0.0005), 'l15 s9, quiz 2: e times 0.995 and 1/e times 0.995')

# ---------------------------------------------------------------- digits and remainders (l13, l16 quiz 3, quiz 4, review-3 items 1, 5, homework-3 items 0, 3)
ok([7 ** n % 10 for n in range(1, 9)] == [7, 9, 3, 1, 7, 9, 3, 1] and 7 ** 2026 % 10 == 9 and 2026 % 4 == 2, 'l13 s0, s1, homework-3 item 0: cycle 7, 9, 3, 1; 7^2026 ends in 9')
ok(3 ** 2027 % 10 == 7 and 2027 % 4 == 3 and 9 ** 2027 % 10 == 9 and 13 ** 47 % 10 == 7 and 47 % 4 == 3, 'l13 s7; l16 quiz 3; review-3 item 1: 3^2027 ends in 7, 9^2027 in 9, 13^47 in 7')
ok(123456789 % 11 == 5 and 123456789 % 9 == 0 and sum(map(int, '123456789')) == 45, 'l13 s2: 123456789 leaves 5 mod 11 and 0 mod 9')
ok(all(10 ** k % 11 == (1 if k % 2 == 0 else 10) for k in range(10)) and all(10 ** k % 9 == 1 for k in range(10)), 'l13 s2 explain, s6: 10 is -1 mod 11 and 1 mod 9')


def trailing(n, base):
    f = factorial(n)
    z = 0
    while f % base == 0:
        f //= base
        z += 1
    return z


def legendre(n, p):
    s = 0
    q = p
    while q <= n:
        s += n // q
        q *= p
    return s


ok(trailing(60, 10) == 14 == legendre(60, 5) and trailing(30, 10) == 7 and trailing(125, 10) == 31 and trailing(80, 10) == 19 and trailing(200, 10) == 49,
   'l13 s4, s5, s8; l16 quiz 4; review-3 item 5: trailing zeros of 60!, 30!, 125!, 80!, 200! are 14, 7, 31, 19, 49 (from the factorials themselves)')
ok(trailing(60, 2) == 56 == legendre(60, 2) and legendre(60, 2) == 30 + 15 + 7 + 3 + 1, 'l13 s11: 60! ends in 56 binary zeros')
ok(len([k for k in range(1, 61) if k % 5 == 0]) == 12, 'l13 s3: twelve multiples of 5 up to 60')
ok(all(legendre(n, 5) <= legendre(n, 2) for n in range(2, 500)), 'l13 s3 prose: even numbers supply more 2s than 5s (n < 500)')
rep = 0
for k in range(1, 10):
    rep = rep * 10 + 1
    if rep % 7 == 0:
        break
ok(k == 6 and 111111 == 7 * 15873 and [int('1' * j) % 7 for j in range(1, 7)] == [1, 4, 6, 5, 2, 0], 'l13 s9: the shortest repunit 7 divides has 6 digits; remainders 1, 4, 6, 5, 2, 0')
ok(2 ** 20 % 100 == 76 and 2 ** 10 == 1024 and 24 ** 2 == 576, 'l13 s10: 2^20 ends in 76')
ok({d for d in range(10) if d * d % 10 == d} == {0, 1, 5, 6} and all(d ** n % 10 == d for d in (0, 1, 5, 6) for n in range(1, 20)), 'l13 quiz 0: digits 0, 1, 5, 6 keep their last digit under every power')
ok(2 ** 100 % 7 == 2 and 3 ** 100 % 7 == 4 and 3 ** 6 % 7 == 1 and 2 ** 3 % 7 == 1, 'l13 quiz 1; homework-3 item 3: 2^100 leaves 2 and 3^100 leaves 4 mod 7')
ok(sum(factorial(k) for k in range(1, 100)) % 10 == 3 and all(factorial(k) % 10 == 0 for k in range(5, 100)), 'l13 quiz 2: 1! + ... + 99! ends in 3')

# ---------------------------------------------------------------- sums and counts (l14, review-3 items 2, 6, 8, homework-3 items 1, 4)
ok(sum(range(1, 21)) == 210 and sum(range(1, 201)) == 20100 and sum(range(1, 151)) == 11325 and sum(range(1, 301)) == 45150, 'l14 s0, s1, s8; review-3 item 2: 210, 20100, 11325, 45150')
S = lambda a, b: sum(Fraction(1, k * (k + 1)) for k in range(a, b + 1))
ok(S(1, 49) == Fraction(49, 50) and S(2, 9) == Fraction(2, 5) and S(3, 11) == Fraction(1, 4) and all(S(1, n) == Fraction(n, n + 1) for n in range(1, 60)),
   'l14 s2, s9; review-3 item 6; homework-3 item 1: telescoping sums 49/50, 2/5, 1/4 and n/(n+1)')
ok(Fraction(50, 51) == S(1, 50) and isclose(float(Fraction(50, 51)), 0.98039, abs_tol=0.00001), 'l14 s2 byKey.extra: 50 terms give 50/51 = 0.98039')


def knockout(n):
    matches = 0
    while n > 1:
        matches += n // 2
        n = n - n // 2
    return matches


ok(knockout(50) == 49 and all(knockout(n) == n - 1 for n in range(1, 200)), 'l14 s4, s6: a knockout of n players has n - 1 matches, byes or not')
ok(comb(12, 2) == 66 and comb(20, 2) == 190 and (144 - 12) // 2 == 66, 'l14 s5; review-3 item 8: 66 and 190 handshakes')
ok(10 * 7 // 2 == 35 and comb(10, 2) - 10 == 35, 'l14 s7: 35 diagonals of a decagon')
ok(sum(k * k for k in range(1, 9)) == 204 and comb(9, 2) ** 2 == 1296 and comb(6, 2) ** 2 == 225 and sum(k * k for k in range(1, 6)) == 55,
   'l14 s10, s11; homework-3 item 4: 204 squares, 1296 rectangles; 225 rectangles and 55 squares on 5 x 5')
count_rect = sum(1 for a, b in combinations(range(9), 2) for c, d in combinations(range(9), 2))
ok(count_rect == 1296 and comb(50, 2) == 1225, 'l14 s11: rectangles counted as pairs of lines; 1225 stock pairs')
ok(sum(sum(map(int, str(n))) for n in range(1, 1000)) == 13500, 'l14 quiz 0: digit sum of 1 to 999 is 13,500')
ok(sum(range(1, 200, 2)) == 10000 and sum((-1) ** (k + 1) * k for k in range(1, 101)) == -50, 'l14 quiz 1, quiz 2: odd sum 10,000; alternating sum -50')

# ---------------------------------------------------------------- mixed set (l16)
def heads_reach(n, k):
    dist = {n: 0}
    q = deque([n])
    while q:
        h = q.popleft()
        for a in range(0, k + 1):
            if a <= h and k - a <= n - h:
                t = h - a + (k - a)
                if t not in dist:
                    dist[t] = dist[h] + 1
                    q.append(t)
    return dist


ok(0 not in heads_reach(13, 4), 'l16 s1: thirteen coins, turn four: never all tails')


def heavy_ok(n, k):
    if n <= 1:
        return True
    if k == 0:
        return False
    return any(heavy_ok(a, k - 1) and heavy_ok(n - 2 * a, k - 1) for a in range(1, n // 2 + 1))


ok(not heavy_ok(30, 3) and heavy_ok(30, 4) and heavy_ok(10, 3) and heavy_ok(4, 2), 'l16 s3: 30 coins need 4 weighings; 10, 10, 10 then 4, 3, 3 works')


def tile(cells, shapes):
    def rec(free):
        if not free:
            return True
        c = min(free)
        for sh in shapes:
            for anchor in sh:
                placed = [(c[0] + di - anchor[0], c[1] + dj - anchor[1]) for di, dj in sh]
                if all(p in free for p in placed):
                    if rec(free - set(placed)):
                        return True
        return False
    return rec(frozenset(cells))


DOM = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
b7 = {(i, j) for i in range(7) for j in range(7)}
ok(not tile(b7 - {(0, 1)}, DOM) and sum(1 for c in b7 - {(0, 1)} if sum(c) % 2 == 0) == 25, 'l16 s4: 7 x 7 minus the square next to a corner: 25 dark against 23 light, no tiling (search)')
ok(5 + 1 == 6 and 4 * 2 + 1 == 9, 'l16 s0: five colours, six socks force a pair')


def pirates(n, coins):
    if n == 1:
        return [coins]
    nxt = pirates(n - 1, coins)
    need = (n + 1) // 2 - 1
    prices = sorted((fb + 1, j) for j, fb in enumerate(nxt, start=1))
    chosen = prices[:need]
    split = [0] * n
    split[0] = coins - sum(p for p, _ in chosen)
    for p, j in chosen:
        split[j] = p
    return split


ok(pirates(3, 50) == [49, 0, 1], 'l16 s6, s7: three pirates, 50 coins: (49, 0, 1)')


def bridge(times):
    import heapq
    n = len(times)
    goal = frozenset(range(n))
    dist = {(frozenset(), 0): 0}
    pq = [(0, 0, frozenset(), 0)]
    cnt = 0
    while pq:
        d, _, far, side = heapq.heappop(pq)
        if far == goal:
            return d
        if d > dist[(far, side)]:
            continue
        pool = [i for i in range(n) if i not in far] if side == 0 else sorted(far)
        for r in (1, 2):
            for mv in combinations(pool, r):
                nd = d + max(times[i] for i in mv)
                nf = far | frozenset(mv) if side == 0 else far - frozenset(mv)
                st = (nf, 1 - side)
                if nd < dist.get(st, 10 ** 9):
                    dist[st] = nd
                    cnt += 1
                    heapq.heappush(pq, (nd, cnt, nf, 1 - side))


ok(bridge([1, 2, 6, 9]) == 16 and bridge([1, 2, 6, 9, 12]) == 26, 'l16 s8, s11: 1, 2, 6, 9 need 16; with a 12-minute walker 26 (search)')
ok(2 + 1 + 6 + 1 + 9 == 19 and 2 + 1 + 6 + 1 + 9 + 1 + 12 == 32, 'l16 s8, s11 byKey.escort: escorting costs 19 and 32')
H = lambda n: sum(Fraction(1, k) for k in range(1, n + 1))
ok(isclose(float(1 - (H(20) - H(10))), 0.3312, abs_tol=0.00005), 'l16 quiz 0: twenty prisoners win with chance 0.3312')


@lru_cache(maxsize=None)
def drops(eggs, n):
    if n == 0:
        return 0
    if eggs == 1:
        return n
    return min(1 + max(drops(eggs - 1, x - 1), drops(eggs, n - x)) for x in range(1, n + 1))


ok(drops(2, 120) == 15 and 15 * 16 // 2 == 120 and 14 * 15 // 2 == 105, 'l16 quiz 1: 120 floors need 15 drops')


def jug_bfs(a, b, first=None):
    start = (0, 0)
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        moves = [(a, y), (x, b), (0, y), (x, 0)]
        p = min(x, b - y)
        moves.append((x - p, y + p))
        p = min(y, a - x)
        moves.append((x + p, y - p))
        for i, t in enumerate(moves):
            if dist[(x, y)] == 0 and first is not None and i != first:
                continue
            if t not in dist:
                dist[t] = dist[(x, y)] + 1
                q.append(t)
    return dist


def fewest(a, b, target, first=None):
    d = jug_bfs(a, b, first)
    return min(n for (x, y), n in d.items() if target in (x, y))


ok(fewest(5, 7, 1) == 8 and fewest(5, 7, 1, first=0) == 8 and fewest(5, 7, 1, first=1) == 10, 'review-3 item 9: 1 litre with jugs 5 and 7 in 8 steps starting with the 5; 10 at best starting with the 7')
route = [(0, 0), (5, 0), (0, 5), (5, 5), (3, 7), (3, 0), (0, 3), (5, 3), (1, 7)]
d57 = jug_bfs(5, 7)
ok(all(d57[s] == i for i, s in enumerate(route)), 'review-3 item 9 explain: the listed route is a shortest route')

print(f'brainteasers L3 concepts: {checks} checks passed')
