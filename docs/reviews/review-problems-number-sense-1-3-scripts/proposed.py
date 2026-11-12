"""Numbers of the fixes proposed in docs/reviews/review-problems-number-sense-1-3.md, each by two routes,
and a search of the number-sense course for the new numbers (they must be fresh).
Run from the repo root:  python3 docs/reviews/review-problems-number-sense-1-3-scripts/proposed.py   (exit 0)"""
import glob
import math
import re
import sys
from fractions import Fraction as F

checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)


def near(x, stored, label, eps=1e-6):
    ok(abs(float(x) - stored) <= eps, f'{label}: {float(x)!r} against {stored}')


# finding 10: bands that separate the rounded key from the unrounded value
ok(abs(5 / 18 - 0.278) > 0.0001 and abs(5 / 18 - 0.277778) <= 0.0001 and abs(0.2778 - 0.277778) <= 0.0001
   and abs(0.277 - 0.277778) > 0.0001, 'golf part 3: 5/18 and 0.2778 leave the key band and land on unrounded; 0.277 does not')
ok(abs(2.8333 - 2.83) > 0.0005 and abs(17 / 6 - 2.8333) <= 0.0005 and abs(2.833 - 2.8333) <= 0.0005
   and abs(2.84 - 2.83) > 0.0005, 'taxi part 2: 2.8333, 2.833 and 17/6 leave the key band and land on unrounded')
# finding 14
ok(abs(30000 / 9000 - 3.33) <= 0.04 and abs(3.3 - 3.33) <= 0.04 and abs(3 - 3.33) > 0.04 and abs(3.4 - 3.33) > 0.04,
   'comet part 3: 3.3, 3.33 and 10/3 land on unrounded; 3 and 3.4 do not')
# finding 4
near(F(16, 36), 0.444444, 'squash part 1 whole fraction')
# finding 5
near(F(7, 9) * 60, 46.666667, 'printers part 3 in minutes')
near(1 + F(7, 9), 1.777778, 'printers part 4 in hours')
ok((1 + F(7, 9)) * 60 == F(320, 3), 'printers: 1 7/9 hours is 106 2/3 minutes')
# finding 11
ok(round(1700 / 6) == 283 and 1700 - 5 * 283 == 285, 'taxi in pence: 283 and 285')

# finding 1: garden part 1 asks for the beans
ok(F(1, 4) * 20 == 5 == sum(1 for b in range(20) if b % 4 == 0) and 20 * 4 == 80 and 20 - 5 == 15
   and 20 // 5 * 2 == 8 and F(8, 20) + F(5, 20) == F(13, 20), 'garden: 5 beds of beans, slips 80 and 15, 8 beds of potatoes')

# finding 15: the tub with 2,169 cubes
N = 2169
edge = max(n for n in range(1, 60) if n ** 3 <= N)
ok(edge == 12 == math.floor(N ** (1 / 3) + 1e-9) and 12 ** 3 == 1728 and 13 ** 3 == 2197 and 12 * 12 == 144
   and 144 * 12 == 1728, 'tub: edge 12, 1,728 and 2,197')
ok(N - 1728 == 441 and math.isqrt(441) == 21 and 21 * 21 == 441 and 20 ** 2 == 400 and 22 ** 2 == 484, 'tub: 441 left, side 21')
ok(45 <= math.sqrt(N) <= 47 and N / 3 == 723 and N - 144 == 2025 and N - 2197 == -28 and N - 36 == 2133
   and 441 / 2 == 220.5 and 441 / 4 == 110.25, 'tub slips: 46, 723, 2,025, -28, 2,133, 220.5, 110.25')
ok(len({12, 13, 46, 723}) == 4 and len({441, 2025, -28, 2133}) == 4 and len({21, 220.5, 110.25}) == 3, 'tub: no slip equals a key')

# finding 2: the rye loaves at 1/5 kg a loaf (route 2 in units of 1/30 kg: 25 of flour, 6 a loaf)
fl, lf = F(5, 6), F(1, 5)
q = fl / lf
ok(q == F(25, 6) == 4 + F(1, 6) and 25 // 6 == 4, 'rye: 25/6 = 4 1/6, 4 loaves')
near(q, 4.166667, 'rye part 1')
near(fl * lf, 0.166667, 'rye part 1 multiplied')
near(F(6, 5) * lf, 0.24, 'rye part 1 wrong flip')
left = fl - 4 * lf
ok(left == F(25 % 6, 30) == F(1, 30) and F(5, 6) == F(25, 30) and F(4, 5) == F(24, 30) and F(1, 6) * lf == left, 'rye: 1/30 kg left')
near(left, 0.033333, 'rye part 3')
near(fl - lf, 0.633333, 'rye part 3 one loaf')
ok(F(5 - 4, 6 - 5) == 1, 'rye part 3 tops and bottoms')
near(q - 4, 0.166667, 'rye part 3 loaf sixth')
share = left / fl
ok(share == F(1, 25) == F(25 % 6, 25) and left * F(6, 5) == F(6, 150), 'rye: 1/25 of the flour')
near(left * fl, 0.027778, 'rye part 4 multiplied')
ok(fl / left == 25 and (fl - lf) / fl == F(19, 25) and math.floor(fl * lf) == 0, 'rye part 4 flipped 25, carried 19/25; part 2 carried 0')
ok(len({F(25, 6), F(1, 6), F(6, 25)}) == 3 and len({left, F(19, 30), F(1), F(1, 6)}) == 4
   and len({share, F(1, 36), F(25), F(19, 25)}) == 4, 'rye: no slip equals a key or another slip')

# freshness of the new numbers inside the course (outside the three sets)
files = [f for f in glob.glob('app/content/courses/number-sense/*.json')
         if not re.search(r'problems-[123]\.json$', f)]
text = {f: open(f).read() for f in files}
for label, rx in [('2,169', r'2\{,\}169|\b2169\b'), ('2,197', r'2\{,\}197|\b2197\b'),
                  ('5/6 and 1/5 together', r'tfrac\{5\}\{6\}\}? *(\\\\div|-|\\\\times) *\\\\tfrac\{[14]\}\{5\}'),
                  ('1/30', r'tfrac\{1\}\{30\}'), ('25/6', r'tfrac\{25\}\{6\}')]:
    hits = [f.rsplit('/', 1)[1] for f in files if re.search(rx, text[f])]
    ok(not hits, f'fresh in number-sense: {label} found in {hits}')

# read by hand, not failures: 441 is in homework-4 (a line of Euclid's steps, 3 x 147) and 2,025 in an l11 quiz 'why' line (45 squared)
for label, rx in [('441', r'\b441\b'), ('2,025', r'2\{,\}025')]:
    print('NOTE', label, 'also in', [f.rsplit('/', 1)[1] for f in files if re.search(rx, text[f])])

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
