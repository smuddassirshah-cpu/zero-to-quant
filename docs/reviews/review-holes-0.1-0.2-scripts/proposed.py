"""Numbers of the fixes proposed in review-holes-0.1-0.2.md, each worked twice.   python3 proposed.py   (exit 0)"""
import math
import sys
from fractions import Fraction as Fr

fails = 0


def ok(c, m):
    global fails
    if not c:
        fails += 1
        print('FAIL', m)


# finding on e-feed-updates: 6.5 hours read as 6 hours 50 minutes
ok(15 * (6 * 3600 + 50 * 60) == 369000 == 15 * 24600, 'six-fifty 369,000')
ok(abs(369000 - 351000) > 1 and 369000 not in (5850, 324000), 'six-fifty is clear of the key and the other slips')
# finding on e-pit-area: radius rounded to 8 m before squaring
ok(round(50 / (2 * math.pi)) == 8 and round(math.pi * 8 ** 2) == 201 and round(3.14 * 64) == 201 and round(22 / 7 * 64) == 201, 'rounded-radius 201')
ok(abs(201 - 199) > 0.5 + 0.5 and abs(201 - 796) > 2, 'the band 201 +/- 0.5 does not touch 199 +/- 0.5')
# finding on conjugate-bottom: where p*p > q keeps the new bottom at 1 or more
pairs = [(p, q) for p in range(2, 10) for q in (2, 3, 5, 6, 7, 10, 11, 13) if p * p != q]
kept = [(p, q) for p, q in pairs if p * p > q]
ok(all(p * p - q >= 1 for p, q in kept) and len(pairs) - len(kept) == 9 and len(kept) == 55, f'conjugate: {len(kept)} of {len(pairs)} pairs kept')
ok(Fr(9, 64) == Fr(len(pairs) - len(kept), 64), 'conjugate: 9 of 64 pairs give a bottom below 0 (17 of 200 draws seen)')
# finding on other-number: with a > 1 the given number g*a is never the HCF, so the answer g*b is never the LCM g*a*b
ok(all(g * b != g * a * b for g in range(2, 31) for a in range(2, 13) for b in range(1, 13)), 'other-number with a > 1')
# finding on p-hall-tiles: the factorisations the learner now has to find
ok(432 == 2 ** 4 * 3 ** 3 and 540 == 2 ** 2 * 3 ** 3 * 5 and math.gcd(432, 540) == 108, 'hall factorisations')
# finding on e-diameter-ends: halfway along the diameter
ok((Fr(-5 + 7, 2), Fr(2 + 18, 2)) == (1, 10) and math.dist((-5, 2), (7, 18)) == 20, 'diameter ends')
print('proposed:', 'all checks pass' if not fails else f'{fails} failures')
sys.exit(1 if fails else 0)
