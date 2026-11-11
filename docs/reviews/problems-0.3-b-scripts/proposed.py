"""Second read, problems 0.3 (b): the numbers of the fixes proposed in docs/reviews/review-problems-0.3-b.md, each
computed twice, and the freshness of any new number. Exit 0 when every proposed number holds.

Run from the repo root:  <venv>/bin/python docs/reviews/problems-0.3-b-scripts/proposed.py
"""
import glob
import math
import re
import sys

import sympy as sp

checks = fails = 0
ln, log10, e = math.log, math.log10, math.exp


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def close(a, b, t):
    return abs(float(a) - float(b)) <= t


# finding 1: weekly target, part 3 keyed on the value its question names (41.76), parts 4 and 5 following it
r3 = ln(45 / 41.76)
ok(round(r3, 4) == 0.0747 and close(sp.log(sp.Rational(4500, 4176)), 0.0747, 5e-5), 'weekly 3: ln(45/41.76) = 0.0747')
ok(abs(0.0747 - 0.074724) <= 1e-4 and abs(0.0748 - 0.074724) <= 1e-4, 'weekly 3: key 0.074724 ± 0.0001 takes 0.0747 and 0.0748')
ok(abs(0.0746 - 0.074724) > 1e-4 and abs(0.0749 - 0.074724) > 1e-4 and abs(0.0776 - 0.074724) > 2e-4, 'weekly 3: refuses 0.0746, 0.0749; simple slip clear')
ok(round(0.0747 / 3, 4) == 0.0249 and round(0.0748 / 3, 4) == 0.0249, 'weekly 4: 0.0747 / 3 = 0.0249 (and from 0.0748)')
ok(close(0.0747 ** (1 / 3), 0.4212, 5e-5) and close(0.0747 * 3, 0.2241, 1e-9) and close(0.0776 / 3, 0.0259, 5e-5), 'weekly 4 slips from 0.0747')
ok(abs(0.0249 - 0.0249) <= 1e-4 and abs(0.0259 - 0.0249) > 1e-4 + 5e-5, 'weekly 4: bands apart')
s5 = e(0.0249) - 1
ok(close(s5, 0.025213, 5e-7) and round(s5 * 100, 2) == 2.52 and abs(0.0252 - 0.025213) <= 5e-5, 'weekly 5: key 0.025213, 2.52 inside')
ok(abs(0.0251 - 0.025213) > 5e-5 and abs(0.0253 - 0.025213) > 5e-5 and abs(0.0249 - 0.025213) > 1e-4, 'weekly 5: 2.51, 2.53, 2.49 outside')

# finding 2: monthly deposit part 3, the bridge sentence
r = sp.Symbol('r', positive=True)
ok(sp.simplify(sp.log(sp.exp(5 * r)) - 5 * r) == 0 and close(5 * 0.0479, 0.2395, 1e-12), 'deposit 3: ln(e^{5r}) = 5r; 5 x 0.0479 = 0.2395')

# finding 3: forty doublings part 4 through m = 1.10 from part 3
gap = 10 ** 15 / (1.10 * 10 ** 12)
ok(close(gap, 909.09, 0.005) and close(log10(gap), 2.9586, 5e-5) and close(log10(gap) / 0.30103, 9.83, 0.005), 'forty 4 through m: 909.09, log 2.9586, 9.83')
ok(math.ceil(log10(gap) / 0.30103) == 10 and 2 ** 50 > 10 ** 15 > 2 ** 49, 'forty 4: 10 further doublings')
ok(close(1.10 * 10 ** 12 * 2 ** 9, 5.632e14, 1e11) and close(1.10e12 * 2 ** 10, 1.126e15, 1e12), 'forty 4: nine reach 5.63e14, ten reach 1.126e15')

# finding 4: drawdown recovery re-keyed at 11% a month, so that rounding 4.28 to the nearest month fails
l125, l111 = 0.09691, 0.04532
ok(close(log10(1.11), l111, 5e-6), 'log 1.11 = 0.04532')
n_given, n_true = 2 * l125 / l111, 2 * ln(1.25) / ln(1.11)
ok(round(n_given, 2) == 4.28 and round(n_true, 2) == 4.28, f'drawdown 3 at 11%: {n_given:.4f}, {n_true:.4f} -> 4.28')
ok(abs(n_given - 4.2764) <= 0.006 and abs(4.28 - 4.2764) <= 0.006 and abs(4.27 - 4.2764) > 0.006 and abs(4.29 - 4.2764) > 0.006, 'key 4.2764 ± 0.006')
slips = {'no-power': l125 / l111, 'inverted': l111 / (2 * l125), 'simple': 56.25 / 11, 'carried': ln(1.4) / ln(1.11), 'divided-numbers': 1.5625 / 1.11}
want = {'no-power': 2.14, 'inverted': 0.23, 'simple': 5.11, 'carried': 3.22, 'divided-numbers': 1.41}
for k, v in slips.items():
    ok(close(v, want[k], 0.006), f'drawdown 3 slip {k}: {v:.4f} against {want[k]}')
vals = sorted(list(want.values()) + [4.2764])
ok(all(b - a > 0.012 for a, b in zip(vals, vals[1:])), 'drawdown 3 bands apart')
m, v = 0, 32000.0
while v <= 50000:
    v *= 1.11
    m += 1
ok(m == 5 and math.ceil(4.28) == 5 and round(4.28) == 4, 'drawdown 4 at 11%: 5 months, and nearest rounding gives 4')
ok(round(32000 * 1.11 ** 4) == 48578 and round(32000 * 1.11 ** 5) == 53922, 'balances 48,578 and 53,922')
ok(5 + 2 == 7, 'with-falls slip 7')
hits = [f for f in glob.glob('app/content/courses/exp-log/*.json') + ['app/content/exams/topic-0.3.json', 'app/content/exams/stage-0.json']
        if not re.search(r'problems-[123]\.json$', f) and re.search(r'1\.11\^|\b11% a (month|year)|grows 11%', open(f).read())]
ok(not hits, f'11% growth is used in {hits}')

# finding 5: coin part 4 band
ok(all(abs(x - 1397.54) <= 1.0 for x in (1397, 1398, 1397.5, 1397.54, 1250 * 1.118)) and abs(1399 - 1397.54) > 1.0 and abs(1396 - 1397.54) > 1.0,
   'coin 4: 1397.54 ± 1 takes 1397, 1398, 1397.5 and refuses 1396, 1399')
ok(abs(1406.25 - 1397.54) > 1.5 and abs(1375 - 1397.54) > 1.5, 'coin 4: slips clear')

# finding 6: the two wide "decimal" bands
ok(abs(0.000252 - 0.000249) > 5e-7 and abs(0.000252 - 0.000259) > 5e-7 and abs(0.000252 - 0.0002521) <= 5e-7, 'weekly 5 decimal ± 5e-07')
ok(abs(0.000479 - 0.00048) > 5e-7 and abs(0.000479 - 0.000491) > 5e-7 and abs(0.000479 - 0.0004793) <= 5e-7, 'deposit 2 decimal ± 5e-07')

# finding 7: yeast part 1 "added" line; finding 8: app part 3 "simple" value
ok(3000 + 2 ** 1 == 3002 and 3000 * 2 ** 1 == 6000 and 3000 + 2 ** 12 > 2 * 3000, 'yeast 1: 3,002 after an hour; 2^12 more than doubles 3,000')
ok((50000 - 2000) / 600 == 80 and 2000 + 600 * 80 == 50000 and abs(25 / 0.3 - 80) > 1, 'app 3: steady growth reaches 50,000 at n = 80, not 83.33')
ok(all(abs(80 - x) > 0.012 for x in (12.2687, 1.38, 19.23, -2.67)), 'app 3: 80 clear of the other bands')

# finding 9: savings part 4 "years" value
ok(close(2400 * e(0.055 * 1.5), 2606.40, 0.005) and close(2400 * 2 ** (1.5 / 12.6), 2606.44, 0.005), 'savings 4 years slip is 2606.40 (2606.44 by doublings)')

# finding 10: app users part 2 as a change of base judgement
ok(close(log10(25 / 1.3), 1.284, 5e-4) and close(log10(25) - log10(1.3), log10(25 / 1.3), 1e-12), 'app 2: log(25/1.3) = log 25 - log 1.3 = 1.284')
ok(close(25 / 1.3, 19.23, 0.005) and 1.3 ** 19.23 > 150 and close(log10(25) / log10(1.3), 12.27, 0.005), 'app 2: 25/1.3 = 19.23, 1.3^19.23 is about 155')

print(f'proposed: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
