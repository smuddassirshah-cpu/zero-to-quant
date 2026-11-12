"""Second read, proof problems-1 to -3: the numbers and claims of the proposed fixes, each by two routes,
and a grep that the nouns of the proposed re-settings occur nowhere in the proof course or its two exams.
Usage (repo root): <venv>/bin/python docs/reviews/review-problems-proof-1-3-scripts/proposed.py"""
import glob
import itertools
import re
import sys

import sympy as sp

checks = fails = 0


def ok(c, msg):
    global checks, fails
    checks += 1
    if not c:
        fails += 1
        print('FAIL', msg)


imp = lambda a, b: (not a) or b
rows = list(itertools.product([True, False], repeat=3))

# finding 1: the line for `as-and` (problems-1, p-spread-signal part 4)
androws = {r for r in rows if (r[0] or r[1]) and not r[2]}
holds = {r for r in rows if imp(r[0] or r[1], not r[2])}
fails_ = set(rows) - holds
ok(len(androws) == 3 and len(fails_) == 3 and not (androws & fails_), 'two different sets of 3 rows')
ok(androws <= holds and len(holds - androws) == 2 and all(not (p or q) for p, q, r in holds - androws), '3 and rows plus the 2 rows with P or Q false: 5')

# finding 5: the greenhouse re-setting (same truth values as the Monday of the set: P true, Q false, R true)
P, Q, R = 24 < 30, 21 > 25, 40 < 50
ok((P, Q, R) == (True, False, True) and sum([P, Q, R]) == 2 and not ((P or Q) and not R), 'greenhouse Monday: 2 true, no watering')

# finding 4: the judges re-setting keeps the grid, so keys 0, 2 and 6 stand
G = [[7, 3, 6, 2], [4, 8, 5, 1], [2, 6, 9, 4], [5, 4, 3, 9]]
A = lambda t: all(any(x > t for x in row) for row in G)
B = lambda t: any(all(G[f][y] > t for f in range(4)) for y in range(4))
ok(max(t for t in range(-3, 12) if B(t)) == 2 and max(t for t in range(-3, 12) if A(t)) == 6 and not B(5), 'grid keys stand')
ok(all(0 <= x <= 10 for r in G for x in r), 'every cell is a mark out of 10')

# finding 15: part 4 of p-even-test-contra at an even negative n
val = lambda t: t * t + 6 * t + 1
k = sp.symbols('k')
br = 2 * k ** 2 + 6 * k
ok(val(-4) == -7 and br.subs(k, -2) == -4 and 2 * -4 + 1 == -7, 'n = -4: k = -2, bracket -4, value -7 = 2(-4) + 1')
ok({'sign': 4, 'plus-6k': 2 * 4 + 12, 'value': -7, 'k-as-n': br.subs(k, -4)} == {'sign': 4, 'plus-6k': 20, 'value': -7, 'k-as-n': 8}, 'slips 4, 20, -7, 8')
ok(len({-4, 4, 20, -7, 8}) == 5, 'slips distinct from the key -4 and from each other')
ok((-7) % 2 == 1 and -7 == 2 * (-4) + 1, '-7 is odd: 2 times an integer plus 1')

# finding 14 (replacement claim): if n^2 + 2 is a multiple of 3, then n is not a multiple of 3
ints = range(-90, 91)
ok(all(t % 3 != 0 for t in ints if (t * t + 2) % 3 == 0), 'claim true on -90..90')
ok(all((t * t + 2) % 3 == 0 for t in ints if t % 3 != 0), 'its converse is true too')
ok(sp.expand((3 * k) ** 2 + 2 - (3 * (3 * k ** 2) + 2)) == 0, '(3k)^2 + 2 = 3(3k^2) + 2')
ok(all(((3 * t) ** 2 + 2) % 3 == 2 for t in ints), 'remainder 2 for every multiple of 3')
ok((3 * k ** 2).subs(k, -2) == 12 and (-6) ** 2 + 2 == 38 == 3 * 12 + 2, 'n = -6: k = -2, bracket 12, value 38')
ok(len({12, -12, 36, 38}) == 4, 'part 4 slips -12, 36, 38 distinct')
ok(len({sp.expand(e) for e in (3 * k ** 2, 9 * k ** 2, k ** 2, 3 * k)}) == 4, 'part 2 slips 9k^2, k^2, 3k distinct from 3k^2')

# finding 13 (replacement claim, only if the ruling is read strictly): m, n leave remainder 1 on division by 3, then so does mn
j = sp.symbols('j')
prod = sp.expand((3 * j + 1) * (3 * k + 1))
ok(sp.expand(prod - (3 * (3 * j * k + j + k) + 1)) == 0, '(3j+1)(3k+1) = 3(3jk + j + k) + 1')
ok(all((u * v) % 3 == 1 for u in ints for v in ints if u % 3 == 1 and v % 3 == 1), 'claim true on the box')
ok((3 * j * k + j + k).subs({j: 2, k: 3}) == 23 and 7 * 10 == 70 == 3 * 23 + 1, 'm = 7, n = 10: bracket 23')
ref = [t for t in range(1, 30) if (2 * t) % 3 == 1 and not (2 % 3 == 1 and t % 3 == 1)]
ok(ref[0] == 2 and (2 * 1) % 3 == 2, 'converse refuted first at n = 2 with m = 2; n = 1 leaves 2')

# nouns of the re-settings: none in the proof course, its topic exam or the stage exam
own = glob.glob('app/content/courses/proof/*.json') + ['app/content/exams/topic-0.6.json', 'app/content/exams/stage-0.json']
text = ' '.join(open(f).read() for f in own)
for noun in ('parcel', 'heavy label', 'greenhouse', r'\bsoil', r'\btank', 'dancer', r'\bjudges?\b', r'\bferr(y|ies)\b', r'\bberth', r'\bsailings?\b'):
    ok(not re.search(noun, text, re.I), f'noun {noun!r} occurs in the proof course or its exams')
print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
