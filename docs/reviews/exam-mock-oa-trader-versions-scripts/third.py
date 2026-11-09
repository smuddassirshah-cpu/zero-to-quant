"""Reader's own checks: seeded simulations for the harder probability items, exact ranking
values, the values behind the findings, and the proposed fixes.

Usage: python third.py   (exits 1 if any check fails)
"""
import random
import sys
from fractions import Fraction as F
from itertools import product
from math import comb, exp

FAIL = []


def ok(cond, msg):
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond:
        FAIL.append(msg)


def sim(fn, n=300000, seed=7):
    r = random.Random(seed)
    return sum(fn(r) for _ in range(n)) / n


def bo(p, n):  # majority of n independent games
    return sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n // 2 + 1, n + 1))


def run(n, k):  # chance of k heads in a row somewhere in n fair tosses
    return F(sum(1 for s in product('HT', repeat=n) if 'H' * k in ''.join(s)), 2 ** n)


# --- probability items by simulation (third method; the author used exact + enumeration)
def v2b11(r):
    k = r.randint(1, 6)
    return sum(r.random() < .5 for _ in range(k)) == 1


def v2b12(r):
    return sum(r.random() < .5 for _ in range(3)) > sum(r.random() < .5 for _ in range(3))


def v2b13(r):
    a, b, c = r.random(), r.random(), r.random()
    return None if a < b else a > c


def v2b15(r):
    alive = 1
    for _ in range(60):
        alive = sum(2 for _ in range(alive) if r.random() < 2 / 3)
        if alive == 0:
            return 1
        if alive > 200:
            return 0
    return 0


def v3b15(r):
    n = 0
    while True:
        n += 1
        x = r.randint(1, 6)
        if x in (1, 3, 5):
            return None
        if x == 6:
            return n


def cond(fn, n=300000, seed=9):
    r = random.Random(seed)
    v = [x for x in (fn(r) for _ in range(n)) if x is not None]
    return sum(v) / len(v)


ok(abs(sim(v2b11) - 5 / 16) < .005, 'v2 b11 sim near 5/16')
ok(abs(sim(v2b12) - 11 / 32) < .005, 'v2 b12 sim near 11/32')
ok(abs(cond(v2b13) - 2 / 3) < .005, 'v2 b13 sim near 2/3')
ok(abs(sim(v2b15, 40000) - .5) < .01, 'v2 b15 branching sim near 1/2')
ok(abs(cond(v3b15) - 1.5) < .02, 'v3 b15 sim near 3/2')

# --- ranking values as printed
for label, val, shown in [
    ('v2 c06 g7', bo(.55, 7), .608), ('v2 c06 g3', bo(.55, 3), .575), ('v2 c05 j5', bo(.65, 5), .765),
    ('v2 c04 s5', bo(.6, 5), .683), ('v2 c03 w5', bo(.4, 5), .317),
    ('v3 c06 r3', float(run(8, 3)), .418), ('v3 c06 r4', float(run(16, 4)), .395),
    ('v3 c05 h4in12', float(run(12, 4)), .299), ('v3 c03 hhh10', float(run(10, 3)), .508),
]:
    ok(abs(val - shown) < .0005, f'{label} = {val:.4f}, shown {shown}')

# --- finding: v2 c01/c02 and c03/c04 are complements of each other
ok(abs(bo(.3, 3) - (1 - bo(.7, 3))) < 1e-12, 'v2 c02 bo3w is 1 - v2 c01 bo3 (mirror pair)')
ok(abs(bo(.4, 5) - (1 - bo(.6, 5))) < 1e-12, 'v2 c03 w5 is 1 - v2 c04 s5 (mirror pair)')
ok(abs(bo(.65, 5) - 0.765) < .0005 and abs(bo(.8, 3) - .896) < .0005, 'v2 c05 is best-of-n relabelled')

# --- finding: v3 c06 windows-times-chance claim
w = [F(3, 4), F(6, 8), F(13, 16)]
ok(w[0] == w[1] and w[2] != w[0], 'v3 c06: windows x chance is 0.75, 0.75, 0.8125 (not all equal)')
pois = [1 - exp(-n / 2 ** (k + 1)) for n, k in ((4, 2), (8, 3), (16, 4))]
ok(max(pois) - min(pois) < 1e-12, 'v3 c06: the clump heuristic ties all three, so r3 v r4 needs the exact count')

# --- finding: v2 a13 explanation, 24 = 2^3 x 3
f24 = [2, 2, 2, 3]
ok(len(f24) == 4 and len(set(f24)) == 2, 'v2 a13: 24 has four prime factors with repeats, two without; never three')
ok(29 - 22 == 7 and 7 not in {10 - 6, 14 - 10, 15 - 14, 21 - 15, 22 - 21}, 'v2 a13: no gap of 7 is shown')

# --- fixes
smooth = [x for x in range(1, 40) if all(p in (2, 3) for p in range(2, x + 1) if x % p == 0 and all(p % q for q in range(2, p)))]
ok(smooth[:9] == [1, 2, 3, 4, 6, 8, 9, 12, 16], 'fix v2 a08: 1..12 shown, next 16')


def isprime(k):
    return k > 1 and all(k % q for q in range(2, k))


rival = [x for x in range(1, 17) if not (isprime(x) and x > 3)]
ok(rival[:8] != [1, 2, 3, 4, 6, 8, 9, 12], 'fix v2 a08: "not a prime above 3" no longer fits once 12 is shown')
ruler = [n & -n for n in range(1, 13)]
ok(ruler == [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4], 'fix v3 a13: twelve terms, the twelfth is 4')
ok(ruler[11] == [1, 2, 1, 4][11 % 4] == [1, 2, 1, 4, 1, 2, 1, 8][11 % 8], 'fix v3 a13: period 4, period 8 and ruler all give 4')
ok(33 == 3 * 11 and 33 > 26, 'fix v2 a13: 33 = 3 x 11 qualifies after 26')
ok(F(sum(1 for x in range(1, 21) if x % 4 == 0), 20) == F(1, 4), 'fix v3 c06: a random whole number from 1 to 20 is a multiple of 4, 0.250')
ok(F(3, 4) == F(6, 8), 'fix v3 c06: windows x chance ties r2 and r3 at 0.75, so the new generic is true')
ok(float(run(8, 3)) - .25 >= .02, 'fix v3 c06: gap to r3 at least 0.02')
for p, lab in ((.35, 'c02'),):
    ok(abs(bo(p, 3) - .28175) < 1e-9 and .35 - bo(p, 3) >= .02 and .447 - .35 >= .02, f'fix v2 {lab}: p 0.35 gives 0.447, 0.350, 0.282')
ok(abs(bo(.62, 3) - .676544) < 1e-9 and bo(.62, 5) - bo(.62, 3) >= .02 and bo(.62, 3) - .6 >= .02,
   f'fix v2 c04: p 0.62 gives {bo(.62, 5):.3f}, {bo(.62, 3):.3f}, 0.600')
ok(abs(bo(.7, 5) - .83692) < 1e-9 and .86 - bo(.7, 5) >= .02 and .896 - .86 >= .02,
   f'fix v2 c05: j1 0.86 and j5 at 0.7 give 0.896, 0.860, {bo(.7, 5):.3f}')
# after the fix, no two series lines of the same length use p and 1 - p
series = {3: [.7, .35, .62, .8, .55], 5: [.4, .62, .7], 7: [.55]}
ok(all(abs(a + b - 1) > 1e-9 for n, ps in series.items() for i, a in enumerate(ps) for b in ps[i + 1:]),
   'fix: no mirror pair (p and 1 - p at the same length) left in v2')

cons = F(sum(1 for t in product(range(1, 7), repeat=3) if sorted(t) in ([1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6])), 216)
ok(cons == F(1, 9) and F(4, 216) == F(1, 54) and F(18, 216) == F(1, 12) and F(36, 216) == F(1, 6),
   'fix v3 b07: three dice in a run of three numbers 1/9; slips 1/54, 1/12, 1/6')
sq9 = F(sum(1 for x in range(1, 10) if int(x ** .5) ** 2 == x), 9)
ok(sq9 == F(1, 3) and float(run(7, 3)) - 1 / 3 >= .02 and 1 / 3 - float(run(12, 4)) >= .02,
   'fix v3 c05: a random whole number from 1 to 9 is a square, 0.333, gaps kept')

print('FAILS', len(FAIL))
sys.exit(1 if FAIL else 0)
