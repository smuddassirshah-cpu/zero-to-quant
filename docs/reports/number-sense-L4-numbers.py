"""Number checks for number-sense level 4 (l15 to l19, review-4, homework-4).

Every stated number is computed twice: once by a direct route (brute-force listing, math.gcd and math.lcm,
statistics, exact Fractions) and once by the route the lesson teaches (index form, Euclid, formulas).
Each value is then tied to the JSON path where it is stated with lv.expect. Rounding is half up (UK GCSE).
"""
import math
import os
import statistics
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('number-sense', 4)
PI = math.pi


def hu(x, d):
    return float(D(repr(x)).quantize(D(1).scaleb(-d), rounding=ROUND_HALF_UP))


def two(a, b, label, tol=1e-9):
    """Two independent routes must agree; returns the value."""
    lv.claim(abs(a - b) <= tol, f'two routes agree: {label} ({a} vs {b})')
    return a


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def factorise(n):
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def count_by_index(n):
    return math.prod(e + 1 for e in factorise(n).values())


def isprime(n):
    return len(factors(n)) == 2


def euclid(a, b):
    rem = []
    while b:
        a, b = b, a % b
        rem.append(b)
    return a, rem

# ---------------- l15 ----------------
f36 = two(len(factors(36)), count_by_index(36), 'factors of 36')
lv.expect('l15', 'screens[1].widget.answer', f36)
lv.expect('l15', 'screens[1].widget.wrong[0].value', f36 + 1)            # 6 counted twice
rect36 = [(a, 36 // a) for a in range(1, 7) if 36 % a == 0]
lv.expect('l15', 'screens[1].widget.wrong[1].value', len(rect36))         # five rectangles
lv.claim(rect36 == [(1, 36), (2, 18), (3, 12), (4, 9), (6, 6)], 'the five rectangles of 36')
lv.claim([w for w in range(1, 9) if 36 % w == 0] == [1, 2, 3, 4, 6], 'row lengths 1 to 8 that divide 36')
lv.claim(7 * 5 == 35 and 5 * 7 == 35 and 4 * 8 == 32, 'leftover checks for rows of 5, 7, 8')
lv.expect('l15', 'screens[2].widget.answer', two(len([a for a in range(1, 7) if 37 % a == 0]), len(factors(37)) // 2, 'rectangles of 37'))
lv.claim(isprime(37), '37 is prime')
mult7 = [n for n in range(14, 101, 7) if all(n % p for p in (2, 3, 5))]
lv.claim(mult7 == [49, 77, 91], 'unshaded multiples of 7: 49, 77, 91')
for n, c in ((30, 10), (50, 15), (100, 25)):
    primes = [k for k in range(2, n) if isprime(k)]
    sieve = [k for k in range(2, n) if all(k % p or k == p for p in (2, 3, 5, 7))]
    two(len(primes), len(sieve), f'primes below {n}')
    lv.claim(len(primes) == c, f'{c} primes below {n}')
lv.expect('l15', 'screens[3].explain.text', 25)
lv.expect('l15', 'screens[3].explain.text', 15)
lv.expect('l15', 'screens[3].explain.text', 10)
lv.claim(isprime(97) and math.isqrt(97) == 9 and 9 ** 2 == 81 and 10 ** 2 == 100, '97 prime, root between 9 and 10')
lv.claim(factorise(360) == {2: 3, 3: 2, 5: 1}, '360 = 2^3 x 3^2 x 5')
treeA = [2, 3, 2, 3, 2, 5]; treeB = [2, 2, 2, 5, 3, 3]
lv.claim(math.prod(treeA) == 360 == math.prod(treeB), 'both factor trees multiply to 360')
for r, p in enumerate((2, 3, 5)):
    lv.expect('l15', f'screens[5].widget.rows[{r}][1].answer', treeA.count(p))
    lv.expect('l15', f'screens[5].widget.rows[{r}][2].answer', treeB.count(p))
lv.claim(91 == 7 * 13 and 51 == 3 * 17 and 57 == 3 * 19 and isprime(53) and isprime(59) and isprime(2) and not isprime(1), 'trap numbers')
f360 = two(len(factors(360)), (3 + 1) * (2 + 1) * (1 + 1), 'factors of 360')
lv.expect('l15', 'screens[7].widget.answer', f360)
lv.expect('l15', 'screens[7].widget.wrong[0].value', 3 * 2 * 1)
lv.expect('l15', 'screens[7].widget.wrong[1].value', 4 + 3 + 2)
lv.expect('l15', 'screens[7].prose', two((2 + 1) * (2 + 1), len(factors(36)), '36 by index form'))
lv.claim(factorise(252) == {2: 2, 3: 2, 7: 1}, '252 = 2^2 x 3^2 x 7')
lv.expect('l15', 'screens[9].prose', two(len(factors(252)), count_by_index(252), 'factors of 252'))
lv.claim(252 // 21 == 12 and 252 // 63 == 4 and 252 // 7 == 36 and 252 // 12 == 21, 'block lengths that divide 252')
lv.claim(252 % 5 == 2 and 252 % 8 == 4 and 252 % 24 == 12 and 10 * 24 == 240, 'remainders for 5, 8 and 24')
lv.expect('l15', 'quiz[0].widget.answer', two(len(factors(49)), count_by_index(49), 'factors of 49'))
lv.claim(87 == 3 * 29 and 7 * 13 == 91, '87 = 3 x 29')
lv.claim(factorise(72) == {2: 3, 3: 2} and 2 ** 2 * 3 ** 3 == 108, '72 = 2^3 x 3^2; the swap is 108')
lv.expect('l15', 'quiz[3].widget.answer', two(len(factors(72)), 4 * 3, 'factors of 72'))

# ---------------- l16 ----------------
lv.expect('l16', 'screens[0].widget.points[0].target', two(math.lcm(12, 18), min(set(range(12, 217, 12)) & set(range(18, 217, 18))), 'LCM 12, 18'))
lv.expect('l16', 'screens[1].widget.answer', two(math.gcd(12, 18), max(set(factors(12)) & set(factors(18))), 'HCF 12, 18'))
lv.expect('l16', 'screens[1].widget.wrong[3].value', 12 * 18)
lv.expect('l16', 'screens[2].widget.answer', two(math.lcm(4, 6), 12, 'LCM 4, 6'))
lv.expect('l16', 'screens[2].explain.text', math.gcd(4, 6))
lv.claim(factorise(84) == {2: 2, 3: 1, 7: 1} and factorise(120) == {2: 3, 3: 1, 5: 1}, '84 and 120 factorised')
lv.expect('l16', 'screens[3].widget.answer', two(math.gcd(84, 120), 2 * 2 * 3, 'HCF 84, 120'))
lv.expect('l16', 'screens[3].widget.wrong[2].value', 2 ** 3 * 3)
lv.expect('l16', 'screens[4].widget.answer', two(math.lcm(84, 120), 2 ** 3 * 3 * 5 * 7, 'LCM 84, 120'))
lv.expect('l16', 'screens[4].widget.wrong[0].value', 84 * 120)
lv.expect('l16', 'screens[4].widget.wrong[2].value', 2 ** 2 * 3 * 5 * 7)
lv.expect('l16', 'screens[4].explain.text', two(12 * 840, 84 * 120, 'HCF x LCM = product'))
lv.claim(F(84, 120) == F(7, 10) and F(84, 120) == F(42, 60) and F(5, 12) + F(7, 18) == F(29, 36), '7/10 and 29/36')
lv.claim(F(5, 12) == F(15, 36) and F(7, 18) == F(14, 36), '15/36 and 14/36')
g, rem = euclid(252, 198)
lv.claim(rem == [54, 36, 18, 0] and g == 18 == math.gcd(252, 198), 'Euclid 252, 198')
for r, v in enumerate(rem):
    lv.expect('l16', f'screens[7].widget.rows[{r}][2].answer', v)
lv.expect('l16', 'screens[7].widget.rows[1][2].wrong[0].value', 198 - 54)
lv.expect('l16', 'screens[7].explain.text', two(252 * 198 // 18, math.lcm(252, 198), 'LCM 252, 198'))
lv.claim(math.gcd(8, 12) == 4 and math.lcm(8, 12) == 24 and 8 * 12 == 96, 'HCF 4, LCM 24 of 8 and 12')
lv.expect('l16', 'screens[9].widget.lines[5].text', 84 * 120)
lv.claim(12 + 840 == 852, 'HCF + LCM = 852')
lv.claim(factorise(150) == {2: 1, 3: 1, 5: 2} and factorise(240) == {2: 4, 3: 1, 5: 1}, '150 and 240 factorised')
lv.expect('l16', 'screens[10].widget.answer', two(math.gcd(150, 240), 2 * 3 * 5, 'HCF 150, 240'))
lv.expect('l16', 'screens[10].widget.wrong[2].value', math.lcm(150, 240))
lv.claim(150 // 30 == 5 and 240 // 30 == 8 and 150 % 90 != 0, 'clips 5 and 8; 90 does not divide 150')
lv.expect('l16', 'quiz[0].widget.answer', two(math.lcm(6, 4), 12, 'LCM 6, 4'))
lv.claim(math.gcd(8, 15) == 1 and math.lcm(8, 15) == 120, '8 and 15')
lv.expect('l16', 'quiz[2].widget.answer', two(math.lcm(6, 18), 18, 'LCM 6, 18'))
lv.claim(math.gcd(6, 18) * math.lcm(6, 18) == 108 == 6 * 18, '6 and 18 product check')
lv.claim(F(18, 24) == F(3, 4) and math.gcd(18, 24) == 6, '18/24 = 3/4')

# ---------------- l17 ----------------
areas = {(w, 12 - w): w * (12 - w) for w in range(1, 12)}
lv.claim(areas[(10, 2)] == 20 and areas[(6, 6)] == 36 == max(areas.values()), 'perimeter 24: areas 20 and 36, max at 6 by 6')
lv.expect('l17', 'screens[1].widget.rows[0][1].answer', two(2 * (8 + 3), 8 + 3 + 8 + 3, 'perimeter 8 by 3'))
lv.expect('l17', 'screens[1].widget.rows[1][1].answer', two(8 * 3, sum(1 for _ in range(8) for _ in range(3)), 'area 8 by 3'))


def shoelace(pts):
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]))) / 2


def perim(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:] + pts[:1]))

lv.expect('l17', 'screens[2].widget.answer', two(F(1, 2) * 8 * 5, shoelace([(0, 0), (8, 0), (3, 5)]), 'triangle'))
lv.expect('l17', 'screens[3].widget.answer', two(7 * 4, shoelace([(0, 0), (7, 0), (10, 4), (3, 4)]), 'parallelogram'))
lv.claim(math.dist((0, 0), (3, 4)) == 5 and 7 * 5 == 35, 'slant side 5; slant slip 35')
lv.expect('l17', 'screens[4].widget.answer', two(F(6 + 10, 2) * 4, shoelace([(0, 0), (10, 0), (8, 4), (2, 4)]), 'trapezium'))
L = [(0, 0), (10, 0), (10, 3), (6, 3), (6, 6), (0, 6)]
lv.expect('l17', 'screens[5].widget.answer', two(60 - 12, 36 + 12, 'L area two ways'))
lv.claim(shoelace(L) == 48, 'L area by shoelace')
lv.expect('l17', 'screens[6].widget.answer', two(perim(L), 2 * (10 + 6), 'L perimeter'))
lv.expect('l17', 'screens[6].widget.wrong[0].value', 32 - 4 - 3)
lv.expect('l17', 'screens[6].widget.wrong[1].value', 32 - 14)
lv.expect('l17', 'screens[6].widget.wrong[3].value', 32 + 14)
lv.expect('l17', 'screens[7].widget.answer', two(100 * 100, 10 ** 4, 'cm2 in a m2'))
v_old, v_new = 1000 * 5, 1100 * 5.5
lv.expect('l17', 'screens[8].widget.answer', two(v_new / v_old, 1.1 * 1.1, 'growth 1.21', 1e-12))
lv.expect('l17', 'screens[8].explain.text', two(v_new, 5000 + 500 + 500 + 50, 'new value 6,050'))
lv.claim(1000 * 0.5 == 500 and 100 * 5 == 500 and 100 * 0.5 == 50, 'strip and corner values')
lv.claim(F(1, 2) * 10 * 6 == 30 and 2 * (7 + 4) == 22 and 9 * 9 == 81 and 9 * 5 == 45, 'l17 quiz values')

# ---------------- l18 ----------------
for r, (d, c) in enumerate(((7, 22), (10, 31.4), (20, 62.8))):
    lv.expect('l18', f'screens[0].widget.rows[{r}][3].answer', two(hu(c / d, 2), hu(float(F(c).limit_denominator(1000) / d), 2), f'ratio row {r}'))
lv.claim(abs(22 / 7 - 3.142857) < 1e-6 and hu(PI, 5) == 3.14159, '22/7 and pi digits')
lv.expect('l18', 'screens[1].widget.answer', two(hu(PI * 50, 1), hu(2 * PI * 25, 1), 'wheel 50 cm'))
lv.claim(abs(3.14 * 50 - 157.1) <= 0.15 and abs(22 / 7 * 50 - 157.1) <= 0.15, 'approximations of pi accepted for the wheel')
lv.expect('l18', 'screens[1].widget.wrong[0].value', hu(PI * 25, 1))
lv.expect('l18', 'screens[1].widget.wrong[2].value', hu(PI * 25 ** 2, 1))
lv.expect('l18', 'screens[3].widget.rows[0][1].answer', 2 * 3 * 5)
lv.expect('l18', 'screens[3].widget.rows[0][2].answer', 3 * 5 * 5)
lv.expect('l18', 'screens[3].widget.rows[1][1].answer', two(hu(2 * PI * 5, 2), hu(PI * 10, 2), 'circumference r 5'))
lv.expect('l18', 'screens[3].widget.rows[1][2].answer', two(hu(PI * 25, 2), hu(PI * 5 * 5, 2), 'area r 5'))
lv.expect('l18', 'screens[3].widget.rows[1][2].wrong[0].value', hu(PI * 100, 2))
lv.expect('l18', 'screens[4].widget.answer', two(hu(4 * PI + 8, 2), hu(PI * 8 / 2 + 8, 2), 'semicircle perimeter'))
lv.expect('l18', 'screens[4].widget.wrong[0].value', hu(4 * PI, 2))
lv.expect('l18', 'screens[4].widget.wrong[1].value', hu(8 * PI, 2))
lv.expect('l18', 'screens[4].widget.wrong[2].value', hu(4 * PI + 4, 2))
lv.expect('l18', 'screens[5].widget.answer', two(72 * 1000 / 3600, 72 / 3.6, '72 km/h'))
lv.expect('l18', 'screens[5].widget.wrong[2].value', two(72 * 3.6, 259.2, '72 x 3.6', 1e-9))
lv.expect('l18', 'screens[5].widget.wrong[3].value', 72 / 3600)
lv.expect('l18', 'screens[6].widget.rows[0][1].answer', two(2.5 * 10000, 2.5 * 100 * 100, '2.5 m2'))
lv.expect('l18', 'screens[6].widget.rows[1][1].answer', two(2 * 3 * 4, sum(1 for _ in range(2) for _ in range(3) for _ in range(4)), 'cuboid'))
lv.expect('l18', 'screens[6].widget.rows[1][1].wrong[1].value', 2 * (2 * 3 + 2 * 4 + 3 * 4))
lv.expect('l18', 'screens[7].widget.answer', two(hu(PI * 5 ** 2, 2), hu(PI * (10 / 2) ** 2, 2), 'pond area'))
lv.expect('l18', 'screens[7].widget.wrong[0].value', hu(PI * 10 ** 2, 2))
lv.expect('l18', 'screens[7].widget.wrong[2].value', two(hu(PI * 2 * 5 * 2, 2), hu(2 * PI * 10, 2), 'two-r: 2 x pi x 10 (diameter used as the radius in the distance rule)'))
lv.claim(hu(PI * 2 * 5, 2) == 31.42 and hu(PI * 10, 2) == 31.42, 'doubling the radius for the area gives pi x 10 = 31.42, the circumference entry, not 62.83')
lv.expect('l18', 'screens[9].widget.rows[0][1].answer', two(1260000 / 252, 1260000 // 252, 'per trading day'))
lv.expect('l18', 'screens[9].widget.rows[1][1].answer', two(round(5000 / 7.5), round(1260000 / (252 * 7.5)), 'per trading hour'))
lv.expect('l18', 'screens[9].explain.text', hu(5000 / 7.5, 2))
lv.expect('l18', 'screens[9].widget.rows[0][1].wrong[0].value', round(1260000 / 365))
lv.expect('l18', 'screens[9].widget.rows[1][1].wrong[0].value', round(5000 / 24))
lv.expect('l18', 'quiz[0].widget.answer', two(hu(6 * PI, 2), hu(2 * PI * 3, 2), 'circumference r 3'))
lv.expect('l18', 'quiz[1].widget.answer', two(hu(9 * PI, 2), hu(PI * 3 * 3, 2), 'area r 3'))
lv.expect('l18', 'quiz[1].widget.wrong[0].value', hu(36 * PI, 2))
for p, lab in ((3.14, '3.14'), (22 / 7, '22/7'), (3.142, '3.142')):
    lv.claim(abs(hu(9 * p, 2) - 28.27) <= 0.02 + 1e-9, f'l18 q-area-3 accepts the value from pi = {lab}: {hu(9 * p, 2)}')
    lv.claim(abs(hu(36 * p, 2) - 113.1) <= 0.1 + 1e-9, f'l18 q-area-3 diameter slip from pi = {lab}: {hu(36 * p, 2)}')
lv.expect('l18', 'quiz[2].widget.answer', two(90 * 1000 / 3600, 90 / 3.6, '90 km/h'))

# ---------------- l19 ----------------
days = [120, -80, 40, 40, 300, -60, 60]
mean = two(statistics.mean(days), F(sum(days), len(days)), 'mean 60')
lv.expect('l19', 'screens[0].widget.points[0].target', mean)
lv.claim(sum(mean - v for v in days if v < mean) == 300 == sum(v - mean for v in days if v > mean), 'balance 300 and 300')
lv.claim(sorted(mean - v for v in days if v < mean) == [20, 20, 120, 140] and sorted(v - mean for v in days if v > mean) == [60, 240], 'distances 140, 120, 20, 20 and 60, 240')
lv.expect('l19', 'screens[2].explain.text', two(statistics.median(days), sorted(days)[3], 'median 40'))
lv.claim(statistics.mode(days) == 40 and statistics.multimode(days) == [40], 'mode 40')
lv.expect('l19', 'screens[3].widget.answer', two(max(days) - min(days), 300 + 80, 'range 380'))
big = [3100 if v == 300 else v for v in days]
lv.expect('l19', 'screens[4].widget.rows[0][1].answer', two(statistics.mean(big), (420 + 2800) / 7, 'mean with 3,100'))
lv.expect('l19', 'screens[4].widget.rows[1][1].answer', statistics.median(big))
lv.expect('l19', 'screens[4].widget.rows[0][1].wrong[1].value', sum(big))
lv.expect('l19', 'screens[5].widget.answer', two(statistics.median([3, 5, 8, 10]), (5 + 8) / 2, 'even median'))
freq = {0: 2, 1: 5, 2: 8, 3: 4, 4: 1}
flat = [k for k, c in freq.items() for _ in range(c)]
lv.expect('l19', 'screens[6].widget.rows[0][1].answer', two(sum(flat), sum(k * c for k, c in freq.items()), 'total trades'))
lv.expect('l19', 'screens[6].widget.rows[1][1].answer', two(statistics.mean(flat), 37 / 20, 'mean 1.85'))
lv.expect('l19', 'screens[6].widget.rows[2][1].answer', two(statistics.median(flat), (flat[9] + flat[10]) / 2, 'median 2'))
lv.expect('l19', 'screens[6].widget.rows[3][1].answer', statistics.mode(flat))
lv.expect('l19', 'screens[6].widget.rows[1][1].wrong[0].value', 37 / 5)
lv.expect('l19', 'screens[6].widget.rows[1][1].wrong[1].value', 20 / 5)
lv.expect('l19', 'screens[7].widget.answer', two(5 * 60 - (120 - 80 + 40 + 40), next(x for x in range(-1000, 1000) if statistics.mean([120, -80, 40, 40, x]) == 60), 'missing day'))
lv.claim(statistics.mean([120, -80, 40, 40, 180]) == 60, 'five days with 180 average 60')
lv.expect('l19', 'screens[8].widget.answer', two((10 * 50000 + 30 * 70000) / 40, statistics.mean([50000] * 10 + [70000] * 30), 'combined average'))
lv.expect('l19', 'screens[9].widget.answer', two(55000 / 50000, F(55000, 50000), 'true ratio 1.1'))
lv.claim((55000 - 45000) / (50000 - 45000) == 2, 'cut-off bars look 2 times')
lv.expect('l19', 'screens[11].widget.options[2].text', 3100 - (-80))
lv.claim(sorted([2, 3, 3, 5, 7, 7, 9]) and statistics.multimode([2, 3, 3, 5, 7, 7, 9]) == [3, 7] and abs(36 / 7 - 5.14) < 0.005, 'two modes 3 and 7; mean 5.14')
hist = [50, 80, 120, 150, 180, 210, 230, 250, 260, 280, 290, 320, 350, 410]
lv.claim(len(hist) == 14 and sum(200 <= v < 300 for v in hist) == 6 == max(sum(lo <= v < lo + 100 for v in hist) for lo in range(0, 500, 100)), 'histogram tallest bar 6')
lv.expect('l19', 'quiz[2].widget.answer', two(statistics.mean([-20, 50, 10, -40, 100]), 100 / 5, 'mean with losses'))
lv.expect('l19', 'quiz[2].widget.wrong[0].value', (20 + 50 + 10 + 40 + 100) / 5)
lv.expect('l19', 'quiz[3].widget.wrong[1].value', two(25 - (-15), 40, 'first-last slip: last minus first listed'))
lv.expect('l19', 'quiz[3].widget.answer', two(max([-15, 40, -30, 25]) - min([-15, 40, -30, 25]), 40 + 30, 'range 70'))

up = [70, -20, 10, 90, 30]
lv.expect('l19', 'quiz[4].widget.answer', two(statistics.median(up), sorted(up)[2], 'unsorted median 30'))
lv.expect('l19', 'quiz[4].widget.wrong[0].value', two(up[2], 10, 'middle of the list as written'))
lv.expect('l19', 'quiz[4].widget.wrong[1].value', two(statistics.mean(up), F(180, 5), 'mean 36'))

# ---------------- review-4 ----------------
lv.claim(factorise(180) == {2: 2, 3: 2, 5: 1} and 2 * 9 * 5 == 90 and 8 * 15 == 120, '180 factorised; slips 90 and 120')
lv.expect('review', 'items[1].widget.answer', two(len(factors(180)), count_by_index(180), 'factors of 180'))
lv.expect('review', 'items[2].widget.answer', two(math.lcm(36, 60), 2 ** 2 * 3 ** 2 * 5, 'LCM 36, 60'))
lv.expect('review', 'items[2].widget.wrong[0].value', 36 * 60)
lv.expect('review', 'items[2].widget.wrong[1].value', math.gcd(36, 60))
lv.claim(F(30, 42) == F(5, 7) and math.gcd(30, 42) == 6, '30/42 = 5/7')
lv.claim(F(30 // 30, 42 // 6) == F(1, 7) and F(1, 7) != F(5, 7), 'review r-cancel slip: top by 30, bottom by 6 gives 1/7')
lv.expect('review', 'items[4].widget.answer', two(8 * 5 - 3 * 2, shoelace([(0, 0), (8, 0), (8, 3), (5, 3), (5, 5), (0, 5)]), 'review L-shape'))
lv.expect('review', 'items[5].widget.answer', two(F(1, 2) * 12 * 7, 42, 'review triangle'))
lv.expect('review', 'items[5].widget.wrong[1].value', F(1, 2) * 12 * 9)
lv.expect('review', 'items[6].widget.answer', two(hu(49 * PI, 2), hu(PI * 7 * 7, 2), 'table top area'))
lv.expect('review', 'items[6].widget.wrong[0].value', hu(196 * PI, 2))
lv.expect('review', 'items[6].widget.wrong[1].value', hu(14 * PI, 2))
for p, lab in ((3.14, '3.14'), (22 / 7, '22/7'), (3.142, '3.142')):
    lv.claim(abs(hu(49 * p, 2) - 153.94) <= 0.1 + 1e-9, f'r-circle-14 key tol 0.1 accepts pi = {lab}: {hu(49 * p, 2)}')
    lv.claim(abs(hu(196 * p, 2) - 615.75) <= 0.35 + 1e-9, f'r-circle-14 diameter slip tol 0.35 for pi = {lab}: {hu(196 * p, 2)}')
    lv.claim(abs(hu(14 * p, 2) - 43.98) <= 0.05 + 1e-9, f'r-circle-14 circumference slip tol 0.05 for pi = {lab}: {hu(14 * p, 2)}')
lv.claim(abs(hu(49 * 22 / 7, 2) - 153.94) > 0.01, 'the old tolerance 0.01 would have rejected 22/7 (fix reverted if this is false)')
lv.expect('review', 'items[7].widget.answer', two(54 * 1000 / 3600, 54 / 3.6, '54 km/h'))
lv.expect('review', 'items[7].widget.wrong[0].value', hu(54 * 3.6, 1))
rf = {0: 3, 1: 4, 2: 2, 3: 1}
rflat = [k for k, c in rf.items() for _ in range(c)]
lv.expect('review', 'items[8].widget.answer', two(statistics.mean(rflat), F(11, 10), 'review frequency mean'))
lv.expect('review', 'items[8].widget.wrong[0].value', 11 / 4)
lv.expect('review', 'items[9].widget.answer', two((6 * 50 - 110) / 5, F(190, 5), 'mean after removal'))
lv.expect('review', 'items[9].widget.wrong[0].value', hu((300 - 110) / 6, 2))
lv.expect('review', 'items[9].widget.wrong[2].value', (300 + 110) / 5)

# ---------------- homework-4 ----------------
lv.claim(factorise(90) == {2: 1, 3: 2, 5: 1} and factorise(126) == {2: 1, 3: 2, 7: 1} and 2 ** 2 * 3 * 7 == 84 and 2 * 27 * 7 == 378, '90 and 126 factorised; slips 84, 378')
lv.expect('homework', 'items[0].parts[1].widget.answer', two(math.gcd(90, 126), 2 * 3 ** 2, 'HCF 90, 126'))
lv.expect('homework', 'items[0].parts[2].widget.answer', two(math.lcm(90, 126), 2 * 3 ** 2 * 5 * 7, 'LCM 90, 126'))
lv.expect('homework', 'items[0].parts[2].widget.wrong[0].value', 90 * 126)
lv.expect('homework', 'items[0].parts[2].widget.wrong[2].value', 2 * 3 * 5 * 7)
lv.expect('homework', 'items[1].parts[0].widget.answer', two(hu(60 + PI * 9 / 2, 2), hu(10 * 6 + 4.5 * PI, 2), 'lawn area'))
lv.expect('homework', 'items[1].parts[0].widget.wrong[0].value', hu(60 + 9 * PI, 2))
lv.expect('homework', 'items[1].parts[0].widget.wrong[1].value', hu(60 + 18 * PI, 2))
lv.expect('homework', 'items[1].parts[1].widget.answer', two(hu(26 + 3 * PI, 2), hu(10 + 6 + 10 + PI * 6 / 2, 2), 'lawn perimeter'))
lv.expect('homework', 'items[1].parts[1].widget.wrong[0].value', hu(32 + 3 * PI, 2))
lv.expect('homework', 'items[1].parts[1].widget.wrong[1].value', hu(26 + 6 * PI, 2))
lv.expect('homework', 'items[2].widget.answer', two(35 * 3600 / 1000, 35 * 3.6, '35 m/s'))
lv.expect('homework', 'items[2].widget.wrong[0].value', two(hu(35 / 3.6, 2), hu(35 * 1000 / 3600, 2), '35 divided by 3.6'))
lv.expect('homework', 'items[2].widget.wrong[1].value', 35 * 60 / 1000)
lv.expect('homework', 'items[2].widget.wrong[2].value', 35 * 3600)
hf = {1: 3, 2: 6, 3: 7, 4: 4}
hflat = [k for k, c in hf.items() for _ in range(c)]
lv.expect('homework', 'items[3].parts[0].widget.answer', two(statistics.mean(hflat), F(52, 20), 'orders mean'))
lv.expect('homework', 'items[3].parts[1].widget.answer', two(statistics.median(hflat), (hflat[9] + hflat[10]) / 2, 'orders median'))
lv.expect('homework', 'items[3].parts[0].widget.wrong[0].value', 52 / 4)
lv.claim(F(273000, 7) == 39000 and 87000 > 45000, 'bonus mean is exactly 39,000')
lv.expect('homework', 'items[4].widget.answer', two((8 * 45000 - 87000) / 7, F(273000, 7), 'bonus mean'))
lv.expect('homework', 'items[4].widget.wrong[1].value', two(273000 / 8, F(273000, 8), 'still dividing by 8'))
lv.expect('homework', 'items[4].widget.wrong[2].value', round(360000 / 7))
lv.expect('homework', 'items[4].explain.text', 273000)
g, rem = euclid(1071, 462)
lv.claim(3 * 147 + 21 == 462 and 462 % 147 == 21 and 462 % 147 != 0, 'Euclid bad line: 147 does not divide 462, so it is not the HCF')
lv.claim(rem == [147, 21, 0] and g == 21 == math.gcd(1071, 462), 'Euclid 1,071 and 462')
lv.claim(2 * 462 == 924 and 3 * 147 == 441 and 7 * 21 == 147 and 1071 - 462 == 609, 'Euclid line arithmetic')
lv.claim(1071 == 21 * 51 and 462 == 21 * 22 and math.gcd(51, 22) == 1, 'Euclid check line')
lv.expect('homework', 'items[5].explain.text', two(21 * 51 * 22, math.lcm(1071, 462), 'LCM 1,071 and 462'))
months = [18, 22, 20, 19, 21, 20, 23, 17, 20, 22, 18, 200]
lv.claim(sum(months) == 420 and statistics.mean(months) == 35 and statistics.median(months) == 20 and statistics.mean(months[:11]) == 20, 'leaflet: total 420, mean 35, median 20, eleven-month mean 20')
lv.claim(sorted(months)[5] == 20 == sorted(months)[6] and max(months[:11]) == 23 and min(months[:11]) == 17, 'leaflet sorted middle and spread')
lv.claim(abs(23 / 20 - 1.15) < 1e-12 and abs((23 - 15) / (20 - 15) - 1.6) < 1e-12 and F(8, 5) == F(8, 5) and F(23, 20) == F(115, 100), 'leaflet: 1.15 times looks like 1.6 times on the cut axis')
lv.expect('homework', 'items[6].model', 1.15)
lv.expect('homework', 'items[6].model', 1.6)
lv.claim('%' not in lv.text('homework', 'items[6].model'), 'leaflet model has no per cent sign')
lv.expect('homework', 'items[6].model', 420)
lv.expect('homework', 'items[6].model', 35)
lv.expect('homework', 'items[7].widget.answer', two(len(factors(2520)), count_by_index(2520), 'factors of 2,520'))
lv.claim(all(2520 % k == 0 for k in range(1, 11)) and math.lcm(*range(1, 11)) == 2520, '2,520 is the LCM of 1 to 10')

lv.check_wrongs()
lv.report()
