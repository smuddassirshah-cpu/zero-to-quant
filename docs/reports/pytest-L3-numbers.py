"""Recompute every number stated in pytest level 3 (l9 to l12, review-3, homework-3), each two ways (float
arithmetic as the code does it, and exact Fractions, enumeration or an independent method), and check it appears
where it is stated (app/tools/numbers_lib.py). Second read: docs/reviews/review-pytest-1-3.md.
Run: python3 docs/reports/pytest-L3-numbers.py   (exits 0 once the content is correct)
"""
import datetime, itertools, math, os, random, statistics, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("pytest", 3)


def two(a, b, label, tol=1e-12):
    lv.claim(abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b))), f'two ways agree: {label}', f'{a} != {b}')
    return a


def mdd(p):                           # positive convention, as l11, l12 and homework-3 write it
    peak, worst = p[0], 0.0
    for x in p:
        peak = max(peak, x)
        worst = max(worst, (peak - x) / peak)
    return worst


def mdd_frac(p):
    return max([F(0)] + [(F(str(max(p[:j + 1]))) - F(str(p[j]))) / F(str(max(p[:j + 1]))) for j in range(len(p))])


def dd(p, label=None):
    a = mdd(p)
    two(a, mdd_frac(p), label or f'drawdown {p}')
    return a


maxmin = lambda p: (max(p) - min(p)) / max(p)
from_first = lambda p: max([0.0] + [(p[0] - x) / p[0] for x in p])

# ---------- l9 ----------
lv.expect('l9', 'screens[0].prose', 104.00 / 100.00 - 1); two(104 / 100 - 1, F(4, 100), 'l9 0.04')
lv.claim(f"{0.04:.2%}" == '4.00%' and f"{-0.0125:.2%}" == '-1.25%' and f"{0.0:.2%}" == '0.00%', 'l9 screens[5]: .2% formats')
lv.expect('l9', 'screens[6].hints[2].text', 102.96 / 104.00 - 1); two(102.96 / 104 - 1, F(-1, 100), 'l9 Tuesday')
lv.expect('l9', 'screens[6].widget.options[0].text', round(100 * (102.96 / 104.00 - 1), 2))
c5 = [101.20, 102.50, 99.80, 100.40, 101.10]
r5 = [b / a - 1 for a, b in zip(c5, c5[1:])]
lv.claim(r5 == [0.012845849802371578, -0.02634146341463417, 0.006012024048096309, 0.006972111553784854], 'l9 screens[8]: hidden expect values')
for got, a, b in zip(r5, c5, c5[1:]):
    two(got, F(str(b)) / F(str(a)) - 1, f'l9 return {a}->{b}')
lv.claim(repr(104.00 / 100.00 - 1) == '0.040000000000000036', 'l9 screens[8]: 104/100 - 1 prints 0.040000000000000036')
lv.expect('l9', 'screens[8].feedback.byKey.test-4', 104.00 / 100.00 - 1)
two(101.92 / 104.00 - 1, F(-2, 100), 'l9 101.92/104')
lv.expect('l9', 'quiz[0].explain.text', 1.50 * 4)
lv.expect('l9', 'quiz[1].widget.answer', 82.00 / 80.00 - 1); two(82 / 80 - 1, F(1, 40), 'l9 quiz 82/80')
lv.expect('l9', 'quiz[1].widget.wrong[0].value', round(82.00 / 84.00 - 1, 4))
lv.expect('l9', 'quiz[1].widget.wrong[1].value', 84.00 / 80.00 - 1)
lv.claim(f"Return: {0.0375:.2%}" == 'Return: 3.75%', 'l9 quiz[3]: format_return(0.0375)')
lv.claim_text('l9', 'screens[8].explain.text', 'one line that reads the file and one loop that prints', False,
              'l9 screens[8]: the script shown builds a text literal and prints once; no file, no loop')

# ---------- l10 ----------
lv.claim([int(1000 / 25), round(1000 / 25), 1000 // 25] == [40, 40, 40.0], 'l10 screens[1]: all three give 40')
lv.claim([int(1000 / 600), round(1000 / 600), 1000 // 600] == [1, 2, 1.0], 'l10 screens[1]: at 600 they give 1, 2, 1.0')
lv.expect('l10', 'screens[1].explain.text', 2 * 600.00)
lv.expect('l10', 'screens[2].widget.options[1].why', round(1000 / 600, 2))
shares = lambda cash, price, fee: max(0, int((cash - fee) / price))
lv.claim([shares(1000, 25, 0), shares(1000, 25, 10), shares(5, 2, 10), shares(1000, 600, 0), shares(2500, 99.99, 9.99), shares(10, 25, 0)]
         == [40, 39, 0, 1, 24, 0], 'l10 screens[3]: the six expected counts')
lv.claim(int(-2.5) == -2 and int((5.00 - 10.00) / 2.00) == -2, 'l10 screens[3]: int(-2.5) is -2')
q = 2700.00 / 5.40
lv.claim(repr(q) == '499.99999999999994' and int(q) == 499, 'l10 screens[4]: 2700/5.40 prints 499.99999999999994')
lv.expect('l10', 'screens[4].canvas.params.rows[0][4]', q)
pence = lambda cash, price, fee: max(0, round((cash - fee) * 100) // round(price * 100))
lv.claim(round(2700.00 * 100) == 270000 and round(5.40 * 100) == 540 and 270000 // 540 == 500, 'l10 screens[6]: pence steps')
lv.claim([pence(2700, 5.40, 0), pence(1000, 25, 10), pence(5, 2, 10), pence(2500, 99.99, 9.99), pence(1000, 600, 0)] == [500, 39, 0, 24, 1],
         'l10 screens[6]: the pence version passes all five')
lv.expect('l10', 'screens[7].widget.answer', 0.5 ** 5); two(0.5 ** 5, F(1, 32), 'l10 1/32')
lv.claim(sum(1 for a in itertools.product((0, 1), repeat=5) for b in itertools.product((0, 1), repeat=5) if a == b) / 4 ** 5 == 1 / 32,
         'l10 screens[7]: enumeration gives 1/32')


def walk(start, moves):
    out = [start]
    for m in moves:
        out.append(round(out[-1] * m, 2))
    return out


lv.claim(walk(100.00, [1.01, 0.99, 1.01, 1.01, 0.99]) == [100.0, 101.0, 99.99, 100.99, 102.0, 100.98]
         and walk(100.00, [0.99, 0.99, 1.01, 0.99, 1.01]) == [100.0, 99.0, 98.01, 98.99, 98.0, 98.98], 'l10 screens[7]: canvas runs')


def seeded(start, steps, seed):
    rng = random.Random(seed)
    return walk(start, [rng.choice([1.01, 0.99]) for _ in range(steps)])


lv.claim(seeded(100.00, 5, 42) == [100.0, 101.0, 102.01, 100.99, 102.0, 103.02] and seeded(250.00, 3, 1) == [250.0, 252.5, 255.03, 252.48],
         'l10 screens[10]: seeded paths')
lv.expect('l10', 'screens[10].explain.text', 103.02)
lv.expect('l10', 'quiz[1].widget.answer', 0.5 ** 4); two(0.5 ** 4, F(1, 16), 'l10 1/16')
lv.expect('l10', 'quiz[1].widget.wrong[1].value', 0.5 ** 3)

# ---------- l11 ----------
lv.claim('l5' in lv.text('l11', 'screens[0].prose'), 'l11 screens[0]: says it returns to the positive sign after l5 to l8',
         'l5 to l8 wrote drawdown as a negative fraction; l11 writes 0.25 with no word of the switch')
hook = [100.00, 120.00, 90.00, 130.00, 117.00]
lv.expect('l11', 'screens[0].widget.answer', dd(hook))
lv.expect('l11', 'screens[0].widget.wrong[0].value', round(maxmin(hook), 4)); two(round(maxmin(hook), 4), round(float(F(40, 130)), 4), 'l11 max-min')
lv.expect('l11', 'screens[0].widget.wrong[1].value', (130 - 117) / 130)
lv.expect('l11', 'screens[0].widget.wrong[2].value', (120 - 90) / 100)            # £30 typed as 30%
tab = [[100.00, 110.00, 121.00], [100.00, 80.00], [100.00], [100.00, 50.00, 200.00, 150.00]]
lv.claim([round(dd(p), 10) for p in tab] == [0, 0.2, 0, 0.5], 'l11 screens[2]: the four table answers')
lv.expect('l11', 'screens[2].hints[2].text', (200 - 150) / 200)
rushed = lambda p: max([0.0] + [(max(p[:i + 1]) - p[i]) / max(p[:i + 1]) for i in range(1, len(p) - 1)])
lv.claim(rushed(hook) == 0.25 and rushed([100.00, 120.00, 90.00]) == 0.0 and round(rushed([100.00, 90.00, 120.00]), 10) == 0.1
         and rushed([100.00, 110.00, 121.00]) == 0.0 and rushed([120.00]) == 0.0, 'l11 screens[3]: the rushed fix on each option')
skip_last = lambda p: mdd(p[:-1]) if len(p) > 1 else 0.0
pounds = lambda p: max([0.0] + [max(p[:i + 1]) - x for i, x in enumerate(p)])
t1, t2 = [100.00, 120.00, 90.00], [80.00, 100.00, 120.00]
lv.claim(skip_last(t1) != 0.25 and from_first(t1) != 0.25 and pounds(t1) != 0.25 and maxmin(t1) == 0.25 and maxmin(t2) != 0.0,
         'l11 screens[4]: path 1 catches skip last, from first and pounds; path 2 catches max - min')
lv.expect('l11', 'screens[5].widget.options[2].text', round(maxmin(t2), 2)); two(maxmin(t2), F(1, 3), 'l11 40/120')
look = lambda c: [0] + [1 if c[t] > c[t - 1] else 0 for t in range(1, len(c))]
lv.claim(look([100.00, 101.00, 102.00, 103.00])[-1] == 1 and look([100.00, 101.00, 102.00, 95.00])[-1] == 0, 'l11 screens[6]: the flip')
pnl = lambda c, p, s, k: [0.0] + [s * p[t] * (c[t] - c[t - 1]) - k * abs(p[t] - p[t - 1]) for t in range(1, len(c))]
lv.claim(pnl([100.00, 102.00, 103.00], [0, 1, 0], 10, 5.00) == [0.0, 15.0, -5.0], 'l11 screens[8]: the cost test')
q0 = [200.00, 250.00, 150.00, 300.00, 240.00]
lv.expect('l11', 'quiz[0].widget.answer', dd(q0))
lv.expect('l11', 'quiz[0].widget.wrong[0].value', maxmin(q0)); lv.expect('l11', 'quiz[0].widget.wrong[1].value', (200 - 150) / 200)
lv.expect('l11', 'quiz[0].widget.wrong[2].value', (300 - 240) / 300)
lv.claim(maxmin([50.00, 100.00]) == 0.5 and dd([50.00, 100.00]) == 0 and maxmin([100.00, 50.00, 100.00]) == dd([100.00, 50.00, 100.00]),
         'l11 quiz[1]: only the rising path splits them')
pos = [0, 1, 1, 0, 1, 1, 1, 0]
changes = sum(abs(b - a) for a, b in zip(pos, pos[1:]))
lv.expect('l11', 'quiz[3].widget.answer', changes * 4.50); two(changes * 4.50, F(18), 'l11 costs')
lv.expect('l11', 'quiz[3].widget.wrong[0].value', sum(pos) * 4.50)
lv.expect('l11', 'quiz[3].widget.wrong[1].value', changes // 2 * 4.50)

# ---------- l12 ----------
lv.expect('l12', 'screens[2].widget.answer', len('..F.') + len('...'))
lv.expect('l12', 'screens[2].explain.text', round(100 * 4 / 7)); two(round(100 * 4 / 7), round(float(F(400, 7))), 'l12 57%')
st, ms = [4, 2, 3, 7, 5], [0, 0, 3, 0, 2]
lv.claim(sum(st) == 21 and sum(ms) == 5 and round(100 * (21 - 5) / 21) == 76 and round(100 * 3 / 5) == 60, 'l12 screens[3]: TOTAL 21, 5, 76%')
lv.expect('l12', 'screens[4].widget.answer', round(19 / 21, 4)); two(19 / 21, F(19, 21), 'l12 19/21')
avg = statistics.mean([1, 1, 1, 1, 0.6])
lv.expect('l12', 'screens[4].widget.wrong[0].value', avg); lv.expect('l12', 'screens[4].widget.wrong[2].value', round(2 / 21, 4))
lv.expect('l12', 'screens[9].canvas.params.rows[2][1]', 5)
lv.expect('l12', 'quiz[1].widget.answer', (40 - 6) / 40); two((40 - 6) / 40, F(17, 20), 'l12 34/40')
# l2 taught test_*.py and *_test.py; l12 must not narrow it to test_*.py alone (finding)
lv.claim('_test.py' in lv.text('l12', 'screens[1].prose'), 'l12 screens[1]: names both file patterns, as l2 taught')
# a src/ + tests/ layout with only `pip install pytest` fails to import the code (ModuleNotFoundError, exit 2) (finding)
lv.claim('pythonpath' in lv.text('l12', 'screens'), 'l12: says how tests in tests/ import code in src/ (pythonpath = ["src"])')

# ---------- review-3 ----------
lv.expect('review', 'items[0].feedback.correct', 4 * 1.50)
up = lambda c: sum(1 for a, b in zip(c, c[1:]) if b > a)
lv.claim([up([100.00, 101.00, 100.50, 102.00]), up([100.00, 100.00]), up([100.00]), up([]), up([99.50, 99.80, 100.10])] == [2, 0, 0, 0, 2],
         'review-3 items[1]: hidden counts')
lv.claim(round(dd([100.00, 150.00, 120.00]), 10) == 0.2 and from_first([100.00, 150.00, 120.00]) == 0.0
         and round(dd([100.00, 80.00]), 10) == round(from_first([100.00, 80.00]), 10) == 0.2
         and round(dd([100.00, 60.00, 90.00]), 10) == round(from_first([100.00, 60.00, 90.00]), 10) == 0.4, 'review-3 items[4]: each path')
p5 = [0, 1, 0, 1, 1, 0, 0, 1]
ch5 = sum(abs(b - a) for a, b in zip(p5, p5[1:]))
lv.expect('review', 'items[5].widget.answer', ch5 * 2.50); two(ch5 * 2.50, F(25, 2), 'r3 costs')
lv.expect('review', 'items[5].widget.wrong[0].value', sum(p5) * 2.50)
lv.expect('review', 'items[5].widget.wrong[1].value', 2 * 2.50)
buys = sum(1 for a, b in zip(p5, p5[1:]) if b > a)
lv.claim(buys * 2.50 == 7.5 and (ch5 - 1) * 2.50 == 10.0, 'review-3 items[5]: 7.5 is three buys; four changes cost 10.0')
lv.claim_text('review', 'items[5].feedback.byKey', 'You missed the last change', False,
              'review-3 items[5]: missing the last change gives £10.00, not £7.50; £7.50 is the three buys alone')
lv.expect('review', 'items[6].widget.answer', (25 - 8) / 25); two((25 - 8) / 25, F(17, 25), 'r3 cover')
lv.expect('review', 'items[6].widget.wrong[0].value', round((1 + 0 + 0.75) / 3, 4))
lv.expect('review', 'items[6].widget.wrong[1].value', 8 / 25)
lv.claim(datetime.date(2026, 10, 17).weekday() == 5, 'review-3 items[7]: 17 October 2026 is a Saturday')

# ---------- homework-3 ----------
lines = [f"{d}: {b / a - 1:.2%}" for d, a, b in zip(['Tue', 'Wed', 'Thu', 'Fri'], c5, c5[1:])]
lv.claim(lines == ['Tue: 1.28%', 'Wed: -2.63%', 'Thu: 0.60%', 'Fri: 0.70%'] and f"{245 / 250 - 1:.2%}" == '-2.00%', 'homework-3 items[0]: report lines')
crash_fixed = lambda p: mdd(p)
start2 = lambda p: mdd([p[0]] + p[2:])
lv.claim(mdd(t1) == 0.25 and skip_last(t1) == 0.0 and round(start2(t1), 10) == 0.1 and round(mdd([100.00, 80.00, 90.00]), 10) == 0.2,
         'homework-3 items[1]: 0.25, stop short 0, start at 2 gives 0.1')
lv.expect('homework', 'items[1].explain.text', 0.1)
n6 = sum(math.comb(10, k) for k in range(6, 11))
enum6 = sum(1 for s in itertools.product((0, 1), repeat=10) if sum(s) >= 6)
lv.claim(n6 == enum6 == 386, 'homework-3 items[5]: 386 of 1,024 by formula and by enumeration')
lv.expect('homework', 'items[5].widget.answer', round(386 / 1024, 3))
lv.expect('homework', 'items[5].widget.wrong[1].value', round((386 + math.comb(10, 5)) / 1024, 3))
lv.expect('homework', 'items[5].feedback.byKey.half', round(100 * 1.01 ** 5 * 0.99 ** 5, 2)); two(1.01 ** 5 * 0.99 ** 5, 0.9999 ** 5, 'hw3 drift')
lv.claim(100 * 1.01 ** 6 * 0.99 ** 4 > 100 > 100 * 1.01 ** 5 * 0.99 ** 5, 'homework-3 items[5]: six ups end above, five below')
reb = [100.00, 104.00, 102.96]
for i in range(len(reb)):
    reb[i] = reb[i] / reb[0]
lv.claim(reb == [1.0, 104.0, 102.96], 'homework-3 items[3]: rebase rewrites the list to [1.0, 104.0, 102.96]')
lv.claim(round(2700.00 * 100) // round(5.40 * 100) == 500 and int(2700.00 / 5.40) == 499, 'homework-3 items[6]: 500, not 499')
lv.claim('pythonpath' in lv.text('homework', 'items[6].widget.model'), 'homework-3 items[6]: model (d) lists the pythonpath setting the src/ layout needs')

lv.check_wrongs()
lv.report()
