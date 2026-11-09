"""analysis L1 performance task h-prove-binary-dense: every stated number, computed twice.

Run from the repository root: python3 docs/reports/analysis-1-perf-numbers.py (standard library only).
"""
import itertools
import math
import os
import random
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("analysis", 1)
import json  # noqa: E402
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'analysis', 'homework-1.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-binary-dense']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"


def k_loop(gap):
    """Smallest k >= 0 with 2^k > 1/gap, by counting up."""
    k = 0
    while F(2) ** k <= 1 / gap:
        k += 1
    return k


def k_bits(gap):
    """Second route: from the bit length of the integer part of 1/gap."""
    q = 1 / gap
    n = math.floor(q)            # 2^k is an integer, so 2^k > q exactly when 2^k > floor(q)
    return n.bit_length()        # the smallest k with 2^k > n


def m_floor(x):
    return math.floor(x) + 1


def m_search(x, j):
    """Least integer above x, found among the finitely many integers in (x, 2^j], as the proof does."""
    lo = -(2 ** j)
    cands = [n for n in range(lo, 2 ** j + 1) if n > x]
    return min(cands)


# (a) the contradiction step: for any s >= 2, some 2^j > s/2 and then 2^(j+1) > s
for s in [F(2), F(5, 2), F(1000), F(10 ** 9 + 7, 3)]:
    j = next(j for j in range(200) if F(2) ** j > s / 2)
    lv.claim(F(2) ** (j + 1) > s and s / 2 < s, f"(a) step at s = {s}")

# (b) the general recipe on random pairs, both routes for k and m
random.seed(11)
for _ in range(3000):
    a = F(random.randint(-10 ** 6, 10 ** 6), random.randint(1, 10 ** 4))
    b = a + F(random.randint(1, 10 ** 4), random.randint(1, 10 ** 6))
    k1, k2 = k_loop(b - a), k_bits(b - a)
    x = F(2) ** k1 * a
    j = next(j for j in range(400) if 2 ** j > x and 2 ** j > -x)
    m1 = m_floor(x)
    ok = (k1 == k2 and F(1, 2 ** k1) < b - a and a < F(m1, 2 ** k1) <= a + F(1, 2 ** k1) < b and m1 - 1 <= x)
    if j <= 14:
        ok = ok and m_search(x, j) == m1
    lv.claim(ok, f"(b) recipe on a = {a}, b = {b}")

# (c) the pair 1/3, 0.34
a, b = F(1, 3), F(34, 100)
gap = b - a
lv.claim(gap == F(1, 150) and F(102 - 100, 300) == F(1, 150), "b - a = 1/150, by Fraction and by the shown common denominator")
lv.claim(abs((0.34 - 1 / 3) - 1 / 150) < 1e-15, "b - a = 1/150 in floats")
k1, k2 = k_loop(gap), k_bits(gap)
lv.claim(k1 == k2 == 8, "the proof's k is 8, two routes")
lv.claim(2 ** 7 == 128 and 128 <= 150 < 256 == 2 ** 8, "2^7 = 128 <= 150 < 256 = 2^8")
x = F(256, 3)
lv.claim(x == F(2) ** 8 * a and x == 85 + F(1, 3), "2^8 a = 256/3 = 85 1/3")
m1, m2 = m_floor(x), m_search(x, 9)
lv.claim(m1 == m2 == 86, "m = 86, two routes")
q = F(86, 256)
lv.claim(q == F(43, 128) and float(q) == 0.3359375 and 86 / 256 == 0.3359375, "86/256 = 43/128 = 0.3359375")
lv.claim(a < q < b and 1 / 3 < 0.3359375 < 0.34, "1/3 < 0.3359375 < 0.34")
lv.claim(q <= a + F(1, 256), "m/2^k <= a + 1/2^k")
# smallest k by brute force over every numerator, both as Fractions and as floats
works = {k: [n for n in range(0, 2 ** k + 1) if a < F(n, 2 ** k) < b] for k in range(0, 9)}
works_f = {k: [n for n in range(0, 2 ** k + 1) if 1 / 3 < n / 2 ** k < 0.34] for k in range(0, 9)}
lv.claim(works == works_f, "brute force agrees in Fractions and floats")
lv.claim(min(k for k in works if works[k]) == 7 and works[7] == [43], "smallest k is 7, with 43/128 only")
lv.claim(all(not works[k] for k in range(0, 7)), "k = 0 to 6 give no binary fraction in the gap")
lv.claim(F(21, 64) == F(0.328125) and F(22, 64) == F(0.34375), "21/64 = 0.328125 and 22/64 = 0.34375")
lv.claim(F(21, 64) < a and F(22, 64) > b, "the gap lies inside (21/64, 22/64)")
for j in range(0, 7):
    lv.claim(all(F(n, 2 ** j) == F(2 ** (6 - j) * n, 64) for n in range(-5, 70)), f"n/2^{j} = 2^(6-{j})n/64")

# figures stated in the model
for v in [128, 150, 256, 86, 0.3359375, 0.328125, 0.34375, 0.34]:
    lv.expect("homework", M, v)
lv.expect("homework", M, r"\tfrac{43}{128}")
lv.expect("homework", M, r"\tfrac{256}{3} = 85\tfrac13")

# rubric: sums to 10, rows required as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 optional")
parts = {0: 'a', 1: 'b', 2: 'b', 3: 'c', 4: 'c'}
passes = []
for r in range(1, len(rub) + 1):
    for s in itertools.combinations(range(len(rub)), r):
        if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i]):
            passes.append(s)
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({parts[i] for i in s} == {'a', 'b', 'c'} for s in passes), "every pass covers parts (a), (b) and (c)")
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x in items if x.get('performance')) == 1, "one performance task in the homework")
lv.claim('!' not in json.dumps(it, ensure_ascii=False) and '—' not in json.dumps(it, ensure_ascii=False) and '–' not in json.dumps(it, ensure_ascii=False), "no ! or dashes")

lv.report()
