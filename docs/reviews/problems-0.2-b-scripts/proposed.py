"""Second read, problems 0.2 (b): the numbers of the fixes the review proposes, each by two routes, and a grep that the
new expressions and words are not already in the three 0.2 courses or the Stage 0 exams.

Run from the repo root: <venv>/bin/python docs/reviews/problems-0.2-b-scripts/proposed.py
"""
import glob
import json
import math
import re
import sys

import sympy as sp

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


x, t = sp.symbols('x t')

# ---- finding 1: cinema block, x + 4 rows of x + 11 seats, 8 seats out
old = sp.expand((x + 4) * (x + 11))
ok(old == x**2 + 15 * x + 44, 'cinema: (x+4)(x+11)')
ok(all(sum(1 for r in range(k + 4) for s in range(k + 11)) == old.subs(x, k) for k in range(1, 25)), 'cinema: by counting')
ok(sp.expand(x**2 + 44) != old and 4 + 11 == 15 and 4 * 11 == 44, 'cinema: part 1 wrongs (x^2+44, x^2+15x+15, x^2+44x+15)')
new = old - 8
ok(sp.factor(new) == (x + 3) * (x + 12), 'cinema: x^2+15x+36 = (x+3)(x+12)')
pairs = [(a, 36 // a) for a in range(1, 7) if 36 % a == 0]
ok(pairs == [(1, 36), (2, 18), (3, 12), (4, 9), (6, 6)] and [a + b for a, b in pairs] == [37, 20, 15, 13, 12], 'cinema: pairs of 36 and their sums')
ok(sp.expand((x + 4) * (x + 9)) == x**2 + 13 * x + 36 and sp.expand((x + 6)**2) == x**2 + 12 * x + 36, 'cinema: part 2 wrongs')
ok(old.subs(x, 10) == 294 == 14 * 21 and new.subs(x, 10) == 286 == 13 * 22 and 294 - 8 == 286, 'cinema: 294 and 286')
ok(14 * 19 == 266 and 16 * 16 == 256 and 100 + 150 + 44 == 294, 'cinema: part 3 wrong values and the check line')
ok(44 - 8 == 36 and 44 - 19 == 25 and sp.expand((x + 5)**2) == x**2 + 10 * x + 25, 'cinema: part 4 options')
ok(not any(2 * k == 15 for k in range(0, 50)) and 15 / 2 == 7.5 and math.isqrt(44)**2 != 44, 'cinema: no whole k, 44 not a square')

# ---- finding 2: allotment plots, A = (x+5)(x+6), B = (x+5)(2x+9), x = 5
A, B = sp.expand((x + 5) * (x + 6)), sp.expand((x + 5) * (2 * x + 9))
ok(A == x**2 + 11 * x + 30 and B == 2 * x**2 + 19 * x + 45, 'plots: expansions')
ok(sp.factor(A) == (x + 5) * (x + 6) and sp.factor(B) == (x + 5) * (2 * x + 9), 'plots: factor')
ok([(a, 30 // a) for a in range(1, 6) if 30 % a == 0] == [(1, 30), (2, 15), (3, 10), (5, 6)], 'plots: pairs of 30')
ok(sp.expand((x + 3) * (x + 10)) == x**2 + 13 * x + 30 and sp.expand((x + 2) * (x + 15)) == x**2 + 17 * x + 30, 'plots: part 1 wrongs')
ok([(a, b) for a in range(1, 91) for b in range(a, 91) if a * b == 90 and a + b == 19] == [(9, 10)], 'plots: 9 and 10 split 19x')
ok(sp.expand(2 * x * (x + 5) + 9 * (x + 5)) == B and sp.expand(2 * x**2 + 10 * x + 9 * x + 45) == B, 'plots: grouping')
ok(sp.expand((x + 9) * (x + 10)) == x**2 + 19 * x + 90 and sp.expand((2 * x + 5) * (x + 9)) == 2 * x**2 + 23 * x + 45, 'plots: part 2 wrongs')
ok(sp.expand((x + 6) + (2 * x + 9)) == 3 * x + 15 and sp.factor(A + B) == 3 * (x + 5)**2, 'plots: total 3(x+5)^2')
ok((A + B).subs(x, 5) == 300 and A.subs(x, 5) == 110 == 10 * 11 and B.subs(x, 5) == 190 == 10 * 19, 'plots: 300, 110, 190')
ok((3 * 10)**2 == 900 and 6 * 10**2 == 600, 'plots: part 4 wrongs')

# ---- finding 6: Sam 6 m behind the stop
sam = sp.expand(t**2 - (6 * t - 6))
ok(sam == sp.expand((t - 3)**2 - 3) and sp.simplify((t**2 - 6 * t + 10) - sam) == 4, 'Sam: (t-3)^2 - 3, 4 m less than Jo')
r = sorted(sp.solve(sam, t))
ok(abs(float(r[0]) - 1.26795) < 5e-6 and abs(float(r[1]) - 4.73205) < 5e-6, 'Sam: roots 1.26795 and 4.73205')
ok(round(float(r[0]), 2) == 1.27 and abs(math.sqrt(3) - 1.732) < 5e-4 and round(3 - 1.732, 3) == 1.268, 'Sam: 1.27, 1.732, 1.268')
ok(abs((6 - math.sqrt(36 - 24)) / 2 - float(r[0])) < 1e-12, 'Sam: formula route')
ok(abs((3 - math.sqrt(12)) - (-0.46410)) < 5e-6 and 3 - 3 == 0, 'Sam: half-root -0.46410, no-root 0')
ok(all(abs(v - float(r[0])) > 0.011 for v in (4.73205, -0.46410, 0)), 'Sam: wrong values clear of the answer band')

# ---- finding 5: bus part 4 band
ok(6.32**2 < 40 < 6.33**2, 'bus 4: 6.32 falls short, 6.33 reaches')
ok(all(abs(v - 6.32456) <= 0.006 for v in (6.32, 6.33, 6.325)) and all(abs(v - 6.32456) > 0.006 for v in (6.3, 6.31, 6.34, 3.16228, 40)), 'bus 4: band 0.006')

# ---- finding 9: sprinkler part 1 accept forms are equal to the key
key = sp.Rational(5, 2) * x - x**2 / 2
for f in (sp.Rational(5, 2) * x - x**2 / 2, (5 * x) / 2 - x**2 / 2, (5 * x - x**2) / 2, x * (5 - x) / 2):
    ok(sp.expand(f - key) == 0, 'sprinkler 1: extra accept form')


# ---- freshness of the new expressions and words: none in the three 0.2 courses or the Stage 0 exams
files = [f for c in ('equations', 'functions', 'quadratics') for f in glob.glob(f'app/content/courses/{c}/*.json')]
files += glob.glob('app/content/exams/stage-0.json') + glob.glob('app/content/exams/topic-0.2.json')


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


blob = {f: ' \n '.join(texts(json.load(open(f)))) for f in files}
for pat in [r'[a-z]\^2 ?\+ ?15[a-z] ?\+ ?44', r'\([a-z] ?\+ ?4\)\([a-z] ?\+ ?11\)', r'\([a-z] ?\+ ?11\)\([a-z] ?\+ ?4\)', r'[a-z]\^2 ?\+ ?15[a-z] ?\+ ?36\b',
            r'\([a-z] ?\+ ?3\)\([a-z] ?\+ ?12\)', r'\([a-z] ?\+ ?12\)\([a-z] ?\+ ?3\)', r'[a-z]\^2 ?\+ ?11[a-z] ?\+ ?30', r'\([a-z] ?\+ ?5\)\([a-z] ?\+ ?6\)', r'\([a-z] ?\+ ?6\)\([a-z] ?\+ ?5\)',
            r'2[a-z]\^2 ?\+ ?19[a-z] ?\+ ?45', r'[a-z]\^2 ?- ?6[a-z] ?\+ ?6\b', r'\bflare', r'\bdeck\b']:
    hits = [f for f, b in blob.items() if re.search(pat, b)]
    ok(not hits, f'fresh: /{pat}/ found in {hits}')

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
