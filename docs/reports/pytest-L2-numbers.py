"""Recompute every number stated in pytest level 2 (l5 to l8, review-2, homework-2), each two ways (float
arithmetic as the code does it, and exact Fractions or an independent method), and check it appears where it is
stated (app/tools/numbers_lib.py). Second read: docs/reviews/review-pytest-1-3.md.
Run: python3 docs/reports/pytest-L2-numbers.py   (exits 0 once the content is correct)
"""
import itertools, math, os, statistics, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("pytest", 2)


def two(a, b, label, tol=1e-12):
    lv.claim(abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b))), f'two ways agree: {label}', f'{a} != {b}')
    return a


def dd_loop(p):                       # negative convention, as l6 to l8 and homework-2 write it
    peak, worst = p[0], 0.0
    for x in p:
        peak = max(peak, x)
        worst = min(worst, x / peak - 1)
    return worst


def dd_frac(p):                       # the same, exact, by every (peak, later price) pair
    return min([F(0)] + [F(str(p[j])) / F(str(max(p[:j + 1]))) - 1 for j in range(len(p))])


def dd(p, label=None):
    a = dd_loop(p)
    two(a, dd_frac(p), label or f'drawdown {p}')
    return a


first_price = lambda p: min(x / p[0] - 1 for x in p)
after_top = lambda p: min(p[p.index(max(p)):]) / max(p) - 1
skip_last = lambda p: min([0.0] + [x / max(p[:i + 1]) - 1 for i, x in enumerate(p[:-1])])
positive = lambda p: max(1 - x / max(p[:i + 1]) for i, x in enumerate(p))
vol = lambda r: statistics.stdev(r) * math.sqrt(252)

# ---------- l5 ----------
r1 = 102.00 / 100.00 - 1
lv.claim(repr(r1) == '0.020000000000000018', 'l5 screens[2]: 102/100 - 1 prints 0.020000000000000018')
lv.expect('l5', 'screens[2].widget.options[1].why', r1)
two(99.96 / 102.00 - 1, F(-2, 100), 'l5 99.96/102 - 1')
lv.expect('l5', 'screens[2].explain.text', -0.02)
lv.expect('l5', 'screens[2].widget.options[2].text', round(99.96 / 100.00 - 1, 4)); two(round(99.96 / 100 - 1, 4), F(-4, 10000), 'l5 from first')
lv.claim(all(x / x - 1 == 0 for x in [50.0, 98.4, 123.45]), 'l5 screens[4]: a constant series gives zero returns')
lv.claim(dd([100.0, 110.0, 121.0]) == 0.0, 'l5 screens[4]: a rising series has drawdown exactly 0')
lv.expect('l5', 'screens[4].feedback.byKey.sum', 1.1 * 0.9); two(1.1 * 0.9, F(99, 100), 'l5 1.1 x 0.9')
lv.claim(len([b / a - 1 for a, b in zip([5.0], [])]) == 0, 'l5 screens[4]: one price gives 0 returns')
# the course measured drawdown as a positive fraction in level 1 (l3, review-1, homework-1); l5 must say it flips (finding)
lv.claim('negative' in lv.text('l5', 'screens[4].prose'), 'l5 screens[4]: states that max_drawdown is now a negative fraction',
         'max_drawdown(prices) <= 0 is false for the level-1 function, which returns 0.2 for a dip')
lv.expect('l5', 'screens[5].canvas.params.rows[1][1]', round(100.00 / 102.00 - 1, 4))
lv.expect('l5', 'screens[5].canvas.params.rows[1][1]', round(102.00 / 99.96 - 1, 4))
lv.expect('l5', 'screens[5].canvas.params.rows[2][1]', 1.02); lv.expect('l5', 'screens[5].canvas.params.rows[2][1]', 0.98)
rr = [0.01, -0.02, 0.015, 0.005, -0.01]
two(vol([2 * x for x in rr]), 2 * vol(rr), 'l5 doubling doubles vol')
two(vol([x + 0.003 for x in rr]), vol(rr), 'l5 shift leaves vol', tol=1e-9)
var_v = lambda r: statistics.variance(r) * 252
two(var_v([2 * x for x in rr]) / var_v(rr), 4, 'l5 variance scales by 4')
nomean = lambda r: math.sqrt(sum(x * x for x in r) / (len(r) - 1)) * math.sqrt(252)
lv.claim(abs(nomean([x + 0.003 for x in rr]) - nomean(rr)) > 1e-3, 'l5 screens[7]: the shift property catches the no-mean version')
pv = lambda r: statistics.pstdev(r) * math.sqrt(252)
lv.claim(abs(pv([2 * x for x in rr]) - 2 * pv(rr)) < 1e-12 and abs(pv([x + 0.003 for x in rr]) - pv(rr)) < 1e-9,
         'l5 screens[7]: pstdev keeps both properties')
lv.expect('l5', 'quiz[0].widget.answer', 63.00 / 84.00 - 1); two(63 / 84 - 1, F(-1, 4), 'l5 quiz 63/84')
lv.expect('l5', 'quiz[0].widget.wrong[0].value', 63.00 / 80.00 - 1)
lv.expect('l5', 'quiz[0].widget.wrong[2].value', round((63.00 - 84.00) / 63.00, 4))
try:
    statistics.stdev([0.01]); raised = False
except statistics.StatisticsError:
    raised = True
lv.claim(raised and issubclass(statistics.StatisticsError, ValueError), 'l5 quiz[1]: stdev of one value raises StatisticsError, a ValueError')
lv.expect('l5', 'quiz[2].explain.text', dd([100.00, 120.00, 90.00])); lv.expect('l5', 'quiz[2].widget.options[3].text', 90.00 / 100.00 - 1)

# ---------- l6 ----------
rows = [[100.00, 120.00, 90.00], [100.00, 110.00], [80.00, 60.00, 70.00], [50.00]]
exp = [dd(p) for p in rows]
lv.claim([round(e, 10) for e in exp] == [-0.25, 0.0, -0.25, 0.0], 'l6 screens[0]: the four expected values', str(exp))
lv.claim([round(first_price(p), 10) for p in rows] == [-0.1, 0.0, -0.25, 0.0], 'l6 screens[1]: first-price version fails only row 1')
lv.expect('l6', 'screens[1].explain.text', -0.10)
ids = [f'prices{i}-{e}' for i, e in enumerate([-0.25, 0.0, -0.25, 0.0])]
lv.claim(ids == ['prices0--0.25', 'prices1-0.0', 'prices2--0.25', 'prices3-0.0'], 'l6 screens[2]: ids as pytest 8.1.1 builds them')
for i, s in enumerate(ids):
    lv.expect('l6', f'screens[2].canvas.params.rows[{i}][0]', f'test_max_drawdown[{s}]')
lv.claim(all(abs(after_top(p) - dd_loop(p)) < 1e-12 for p in rows), 'l6 screens[4]: the after-the-top version passes all four rows')
A, B, C, D = [100.00, 120.00, 60.00], [120.00, 100.00, 110.00], [100.00, 50.00, 120.00, 110.00], [100.00, 90.00]
lv.claim(abs(after_top(A) - dd(A)) < 1e-12 and round(dd(A), 2) == -0.5, 'l6 screens[4]: row A -0.50 both')
lv.expect('l6', 'screens[4].widget.options[1].why', round(dd(B), 4)); two(dd(B), F(-1, 6), 'l6 row B')
lv.expect('l6', 'screens[4].feedback.correct', round(after_top(C), 4)); two(after_top(C), F(-1, 12), 'l6 row C wrong')
lv.claim(round(dd(C), 10) == -0.5 and abs(after_top(D) - dd(D)) < 1e-12, 'l6 screens[4]: row C true -0.5, row D agrees')
paths = [[250.00, 262.50, 210.00, 231.00], [200.00, 150.00, 220.00, 209.00], [120.00, 121.50, 125.00], [98.40],
         [100.00, 90.00, 105.00, 84.00]]
hand = [-0.20, -0.25, 0.0, 0.0, -0.20]
lv.claim(all(abs(dd(p) - h) < 1e-12 for p, h in zip(paths, hand)), 'l6 screens[7]: the five hand answers')
lv.expect('l6', 'screens[7].hints[2].text', -0.25)
caught = lambda f: [i for i, (p, h) in enumerate(zip(paths, hand)) if abs(f(p) - h) > 1e-9]
lv.claim(caught(first_price) == [0, 4], 'l6 screens[7]: paths a and e catch the first-price version', str(caught(first_price)))
lv.claim(caught(after_top) == [1], 'l6 screens[7]: only path b catches the after-the-top version', str(caught(after_top)))
lv.claim(caught(skip_last) == [4], 'l6 screens[7]: only path e catches the skipped last day', str(caught(skip_last)))
lv.claim(len([1 for s in itertools.product(range(3), range(2))]) == 6, 'l6 quiz[0]: 3 x 2 = 6 tests')
lv.expect('l6', 'quiz[0].widget.answer', 6)

# ---------- l7 ----------
wk = [100.00, 110.00, 99.00, 108.90, 98.01]
two(dd(wk), F(9801, 11000) - 1, 'l7 week drawdown')
lv.claim([round(b / a - 1, 12) for a, b in zip(wk, wk[1:])] == [0.1, -0.1, 0.1, -0.1], 'l7 screens[2]: returns +-10%')
lv.expect('l7', 'screens[2].explain.text', round(dd(wk), 3))
lv.expect('l7', 'screens[2].feedback.byKey.test-5', round(100 * dd(wk), 1))
lv.claim(0.9 * 1.1 * 0.9 == F(891, 1000) or abs(0.9 * 1.1 * 0.9 - 0.891) < 1e-12, 'l7: fall, rise, fall compound to 0.891')
lv.expect('l7', 'screens[2].explain.text', 0.891)
lv.claim_text('l7', 'screens[2].explain.text', 'Two falls in a row compound', False,
              'l7 screens[2]: the path from the peak is fall, rise, fall, not two falls in a row')
lv.expect('l7', 'screens[3].widget.answer', sum(1 for asks in [{'prices'}, {'flat'}, {'prices', 'flat'}, set()] if 'prices' in asks))
csv_closes = [180.00, 182.70, 179.45, 176.20, 178.90, 183.35, 181.10, 185.60, 184.05, 187.25]
two(dd(csv_closes), F('176.20') / F('182.70') - 1, 'l7 file drawdown')
lv.expect('l7', 'screens[7].explain.text', round(100 * dd(csv_closes), 2))
lv.expect('l7', 'quiz[0].widget.answer', 3)

# ---------- l8 ----------
lv.expect('l8', 'screens[1].feedback.byKey.r2c0', round(100 * vol([0.01, -0.01]), 2))
v = 40.00 / 50.00 - 1
lv.claim(repr(v) == '-0.19999999999999996', 'l8 screens[4]: 40/50 - 1 prints -0.19999999999999996')
lv.expect('l8', 'screens[4].prose', v); lv.expect('l8', 'screens[4].hints[2].text', -0.2)
# finding 11: pytest 8.1.1 prints the default approx(-0.3) rule as "-0.3 ± 3.0e-07" (rel 1e-6 of 0.3) under the id header
lv.claim(f'{1e-6 * 0.3:.1e}' == '3.0e-07' and 'E       assert -0.19999999999999996 == -0.3 ± 3.0e-07' in lv.text('l8', 'screens[4].prose')
         and '_ test_max_drawdown[prices2--0.3] _' in lv.text('l8', 'screens[4].prose') and 'left:' not in lv.text('l8', 'screens[4].prose'),
         'l8 screens[4]: the failure block is the real pytest 8.1.1 report lines')
lv.claim('DID NOT RAISE <class' in lv.text('l8', 'screens[2].explain.text') and 'DID NOT RAISE ValueError' not in lv.text('l8', 'screens[2]'),
         'l8 screens[2]: DID NOT RAISE is quoted as pytest 8.1.1 prints it')
cl = [100.00, 102.00, 101.00, 103.00, 104.00]
right = [0] * min(2, len(cl)) + [1 if cl[t - 1] > cl[t - 2] else 0 for t in range(2, len(cl))]
peek = [0] + [1 if b > a else 0 for a, b in zip(cl, cl[1:])]
lv.claim(right == [0, 0, 1, 0, 1] and peek == [0, 1, 0, 1, 1], 'l8 screens[8]: hand positions and the peeking ones')
lv.expect('l8', 'screens[8].explain.text', '[0, 1, 0, 1, 1]')
try:
    float("12.50"); float("n/a"); bad = False
except ValueError:
    bad = True
lv.claim(bad and float("12.50") == 12.5, 'l8: float("n/a") raises ValueError, float("12.50") is 12.5')

# ---------- review-2 ----------
r2p = [120.00, 150.00, 105.00, 140.00]
lv.expect('review', 'items[0].widget.answer', dd(r2p))
lv.expect('review', 'items[0].widget.wrong[0].value', 105.00 / 120.00 - 1)
lv.expect('review', 'items[0].widget.wrong[2].value', round(140.00 / 150.00 - 1, 4))
lv.expect('review', 'items[1].explain.text', round(vol([0.01, -0.01]), 4))
lv.expect('review', 'items[2].widget.answer', 4 * 3)
worst_day = lambda p: min(b / a - 1 for a, b in zip(p, p[1:]))
worst_day0 = lambda p: min([0.0] + [b / a - 1 for a, b in zip(p, p[1:])])
lv.claim(round(dd([100.00, 90.00, 80.00]), 10) == -0.2 and round(worst_day([100.00, 90.00, 80.00]), 3) == -0.111,
         'review-2 items[4]: two-down row, drawdown -0.2, worst day -0.111')
lv.expect('review', 'items[4].explain.text', round(80 / 90 - 1, 3))
lv.claim(worst_day([100.00, 110.00]) > 0 and worst_day0([100.00, 110.00]) == 0.0,
         'review-2 items[4]: the rise row gives +0.1 unless the version floors at 0')
lv.claim('no day falls' in lv.text('review', 'items[4].prose'), 'review-2 items[4]: the prose says the wrong version gives 0.0 when no day falls',
         'without that, the rise row also catches it: its worst single-day return is +0.1')
# finding 26: review-2 items[5] is a module-level FEES dict whose sell fee an earlier test sets to 0.00
FEES = {"buy": 2.50, "sell": 2.50}
lv.claim(FEES["buy"] + FEES["sell"] == 5.0 and FEES["buy"] + 0.00 == 2.5, 'review-2 items[5]: fee total is 5.00 normally, 2.50 once the sell fee is 0.00')
lv.expect('review', 'items[5].prose', 2.50); lv.expect('review', 'items[5].prose', 0.00)
lv.expect('review', 'items[5].widget.options[2].why', 0.00); lv.expect('review', 'items[5].widget.options[2].why', 2.50)
lv.claim('107.81' not in lv.text('review', 'items[5]') and 'CLOSES' not in lv.text('review', 'items[5]'), 'review-2 items[5]: no trace of l7 screens[5]')
lv.expect('review', 'items[6].widget.answer', sum(1 for t in [{'prices'}, {'returns'}, {'prices', 'returns'}, set(), {'returns'}, {'prices'}] if t))

# ---------- homework-2 ----------
lv.claim(dd_loop([100.00, 120.00, 90.00, 120.00]) == -0.25 and dd([100.00, 50.00, 75.00]) == -0.5, 'homework-2 items[0] row worst points')
dly = lambda p: [0.0] + [min(b / a - 1, 0.0) for a, b in zip(p, p[1:])]
lv.claim(dly([100.00, 50.00, 75.00])[2] == 0.0, 'homework-2 items[0]: the daily-change version gives 0 on day 3')
peak_excl = lambda p: [x / max(p[:max(i, 1)]) - 1 for i, x in enumerate(p)]
PATH = [250.00, 262.50, 210.00, 231.00, 273.00, 245.70, 286.65, 229.32, 240.79, 300.00, 285.00, 270.00]
lv.claim(any(d > 0 for d in peak_excl(PATH)), 'homework-2 items[0]: the property on PATH catches the peak-excludes-today version')
lv.claim_text('homework', 'items[0].explain.text', 'Only hand-worked rows catch a wrong peak', False,
              'homework-2 items[0]: test-7 also has a wrong peak, and the property catches it')
first_peak = lambda p: [min(x / p[0] - 1, 0.0) for x in p]          # test-4's planted version: clipped, so never positive
lv.claim(all(d <= 0 for d in first_peak(PATH)) and first_peak([100.00, 120.00, 90.00, 120.00]) != [0.0, 0.0, -0.25, 0.0],
         'homework-2 items[0]: the properties pass the first-price peak version on PATH; only a hand row (100, 120, 90, 120) catches it')
lv.claim(abs(dly([100.00, 50.00, 75.00])[2] - (-0.25)) > 0.2 and dd([100.00, 50.00, 75.00]) == -0.5, 'homework-2 items[0]: on 100, 50, 75 day 3 should be -0.25 and the daily-change version gives 0')
lv.expect('homework', 'items[0].explain.text', -0.25)
lv.claim(len(PATH) == 12 and len([x for x in peak_excl(PATH) if x > 0]) > 0 and not any(d > 0 for d in [x / max(PATH[:i + 1]) - 1 for i, x in enumerate(PATH)]),
         'homework-2 items[0]: the never-positive property catches the peak-without-today version (positive on a new high) and not the right one')
m = [100.00, 108.00, 110.00, 99.00, 104.50]
lv.expect('homework', 'items[1].explain.text', round(100 * (m[-1] / m[0] - 1), 1)); two(m[-1] / m[0] - 1, F(45, 1000), 'hw2 total')
lv.expect('homework', 'items[1].explain.text', round(100 * dd(m)))
text_sorted = [99.00, 104.50, 100.00, 108.00, 110.00]
lv.claim(abs(text_sorted[-1] / text_sorted[0] - 1 - 0.045) > 0.01, 'homework-2 items[1]: the text sort changes the total return')
cl = [100.00, 104.00, 102.00, 107.00, 103.00, 108.00]
ma = lambda c, n: [1 if t >= n and c[t - 1] > sum(c[t - n:t]) / n else 0 for t in range(len(c))]
mpeek = lambda c, n: [1 if t >= n - 1 and c[t] > sum(c[t - n + 1:t + 1]) / n else 0 for t in range(len(c))]
lv.claim(ma(cl, 2) == [0, 0, 1, 0, 1, 0] and ma(cl, 3) == [0, 0, 0, 0, 1, 0] and mpeek(cl, 2) == [0, 1, 0, 1, 0, 1],
         'homework-2 items[2]: hand rows and the peeking version')
lv.expect('homework', 'items[2].widget.solution', 104.33); two(round((104 + 102 + 107) / 3, 2), round(float(F(313, 3)), 2), 'hw2 3-day mean')
lv.claim((100.00 + 104.00 + 102.00) / 3 == 102.00, 'homework-2 items[2]: 102.00 equals its 3-day mean')
lv.expect('homework', 'items[2].canvas.params.series[1].values[3]', 104.5)
lv.expect('homework', 'items[3].widget.options[0].text', 'test_dd[prices0--0.1]')
p4 = [250.00, 275.00, 220.00, 264.00, 198.00]
lv.expect('homework', 'items[4].widget.answer', dd(p4))
lv.expect('homework', 'items[4].widget.wrong[0].value', 198.00 / 250.00 - 1)
lv.expect('homework', 'items[4].widget.wrong[1].value', worst_day(p4)); two(worst_day(p4), F(-1, 4), 'hw2 worst day')
lv.expect('homework', 'items[4].widget.wrong[2].value', 220.00 / 275.00 - 1)
lv.expect('homework', 'items[6].widget.model', round(dd(wk), 3))

lv.check_wrongs()
lv.report()
