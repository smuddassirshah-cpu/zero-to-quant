"""analysis L2 performance task h-prove-falling-recursion: every stated number, computed twice.

Run from the repository root: python3 -I docs/reports/analysis-2-perf-numbers.py (standard library only).
Routes: exact Fractions for the first 14 terms; Decimal at 80 digits for 200 terms; floats as a third look.
"""
import itertools
import json
import math
import os
import sys
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("analysis", 2)
HW = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'analysis', 'homework-2.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-prove-falling-recursion']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M = f"items[{I}].model"

# the sequence, exactly and at 80 digits
fr = [None, F(2)]
for n in range(1, 14):
    fr.append((fr[n] ** 2 + 4) / 5)
getcontext().prec = 80
de = [None, D(2)]
for n in range(1, 200):
    de.append((de[n] ** 2 + 4) / 5)
fl = [None, 2.0]
for n in range(1, 60):
    fl.append((fl[n] ** 2 + 4) / 5)
lv.claim(all(abs(D(fr[n].numerator) / D(fr[n].denominator) - de[n]) < D(10) ** -60 for n in range(1, 15)), "Fraction and Decimal agree to 60 digits for n <= 14")
lv.claim(fr[2] == F(8, 5) and float(fr[2]) == 1.6, "a_2 = 8/5 = 1.6")

# (b) P(n): 1 < a_{n+1} < a_n <= 2, exactly for n <= 13, at 80 digits for n <= 150 (later terms sit within 10^-80 of 1)
lv.claim(all(1 < fr[n + 1] < fr[n] <= 2 for n in range(1, 14)), "P(n) holds exactly for n <= 13")
lv.claim(all(1 < de[n + 1] < de[n] <= 2 for n in range(1, 150)), "P(n) holds at 80 digits for n <= 149")
# g keeps the order of positive numbers, and g(1) = 1
g = lambda x: (x * x + 4) / 5
lv.claim(g(F(1)) == 1, "g(1) = 1")
lv.claim(all(g(F(x, 7)) < g(F(y, 7)) for x in range(1, 40) for y in range(x + 1, 41)), "g increasing on positives (grid)")
# the factorised step a_{n+1} - a_n = (a_n - 1)(a_n - 4)/5, checked as polynomials at many points
lv.claim(all(g(F(x, 3)) - F(x, 3) == (F(x, 3) - 1) * (F(x, 3) - 4) / 5 for x in range(-30, 30)), "g(x) - x = (x - 1)(x - 4)/5")
# limit equation: roots 1 and 4, by the quadratic formula and by substitution
disc = 25 - 16
roots = sorted([(5 - math.isqrt(disc)) / 2, (5 + math.isqrt(disc)) / 2])
lv.claim(roots == [1.0, 4.0] and all(r * r - 5 * r + 4 == 0 for r in (1, 4)), "L^2 - 5L + 4 = 0 has roots 1 and 4")
lv.claim(all(F(L) == g(F(L)) for L in (1, 4)), "1 and 4 are the fixed points of g")
lv.claim(de[199] - 1 < D(10) ** -70 and abs(fl[59] - 1) < 1e-15, "the terms tend to 1 (80 digits and floats)")

# (c) a_{n+1} - 1 = (a_n - 1)(a_n + 1)/5 and the bound Q(n)
lv.claim(all(g(F(x, 3)) - 1 == (F(x, 3) - 1) * (F(x, 3) + 1) / 5 for x in range(-30, 30)), "g(x) - 1 = (x - 1)(x + 1)/5")
lv.claim(all(0 < fr[n] - 1 <= F(3, 5) ** (n - 1) for n in range(1, 15)), "Q(n) exactly for n <= 14")
lv.claim(all(0 < de[n] - 1 <= (D(3) / D(5)) ** (n - 1) for n in range(1, 150)), "Q(n) at 80 digits for n <= 149")
lv.claim(fr[1] - 1 == 1 == F(3, 5) ** 0, "base case a_1 - 1 = 1 = (3/5)^0")
p13, p14 = F(3, 5) ** 13, F(3, 5) ** 14
lv.claim(p13 == F(3 ** 13, 5 ** 13) and round(float(p13), 6) == 0.001306 and round(0.6 ** 13, 6) == 0.001306, "(3/5)^13 = 0.001306")
lv.claim(round(float(p14), 6) == 0.000784 and round(0.6 ** 14, 6) == 0.000784, "(3/5)^14 = 0.000784")
lv.claim(p13 > F(1, 1000) > p14, "(3/5)^13 > 0.001 > (3/5)^14")
N1 = next(N for N in range(1, 100) if F(3, 5) ** (N - 1) < F(1, 1000))
N2 = 1 + math.floor(math.log(1000) / math.log(5 / 3)) + 1   # N - 1 > ln 1000 / ln(5/3) = 13.52...
lv.claim(N1 == N2 == 15, "the bound's smallest N is 15, by search and by logarithms")
lv.claim(13 < math.log(1000) / math.log(5 / 3) < 14, "ln 1000 / ln(5/3) lies between 13 and 14")
lv.claim(all(F(3, 5) ** (n - 1) <= p14 for n in range(15, 200)), "powers fall: (3/5)^(n-1) <= (3/5)^14 for n >= 15")
# the true first n with a_n - 1 < 0.001, three routes
t1 = next(n for n in range(1, 15) if fr[n] - 1 < F(1, 1000))
t2 = next(n for n in range(1, 200) if de[n] - 1 < D("0.001"))
t3 = next(n for n in range(1, 60) if fl[n] - 1 < 0.001)
lv.claim(t1 == t2 == t3 == 10, "terms first within 0.001 at n = 10")
lv.claim(round(float(fr[9] - 1), 5) == 0.00167 and round(float(fr[10] - 1), 5) == 0.00067, "a_9 - 1 = 0.00167 and a_10 - 1 = 0.00067")
lv.claim(round(float(fr[9] - 1), 4) == 0.0017, "a_9 - 1 = 0.0017 to four places (rubric)")
lv.claim(15 - 10 == 5, "the bound asks for 5 more terms")
lv.claim(abs(float((fr[14] - 1) / (fr[13] - 1)) - 0.4) < 1e-3 and abs(float((de[60] + 1) / 5) - 0.4) < 1e-12, "the shrink factor tends to 2/5")

for v in ["1.6", "0.001306", "0.000784", "0.00167", "0.00067"]:
    lv.expect("homework", M, float(v))
lv.expect("homework", M, r"N = 15")
lv.expect("homework", M, r"n = 10")
lv.expect("homework", M, r"(L - 1)(L - 4) = 0")

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, True, False], "rows 1 to 4 required, row 5 optional")
parts = {0: 'a', 1: 'b', 2: 'b', 3: 'c', 4: 'c'}
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 3), (0, 1, 2, 3, 4)], "the only passes are rows 1-4 and all five")
lv.claim(all({parts[i] for i in s} == {'a', 'b', 'c'} for s in passes), "every pass covers parts (a), (b) and (c)")
lv.text("homework", f"items[{I}].rubric[3].text")
lv.expect("homework", f"items[{I}].rubric[3].text", 0.000784)
lv.expect("homework", f"items[{I}].rubric[2].text", 1.6)
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(k in it for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x in items if x.get('performance')) == 1, "one performance task in the homework")
s = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in s and '—' not in s and '–' not in s, "no ! or dashes")

lv.report()
