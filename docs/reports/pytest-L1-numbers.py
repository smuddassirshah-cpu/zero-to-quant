"""Recompute every number stated in pytest level 1 (l1 to l4, review-1, homework-1), each two ways (float
arithmetic as the code does it, and exact Fractions or an independent formula), and check it appears where it is
stated (app/tools/numbers_lib.py). Claims about pytest output are checked against pytest 8.1.1, the version
Pyodide 0.27.7 bundles (second read, docs/reviews/review-pytest-1-3.md).
Run: python3 docs/reports/pytest-L1-numbers.py   (exits 0 once the content is correct)
"""
import math, os, statistics, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("pytest", 1)


def two(a, b, label, tol=1e-12):
    lv.claim(abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b))), f'two ways agree: {label}', f'{a} != {b}')
    return a


def approx_ok(x, y, rel=1e-6, abs_=1e-12):        # pytest.approx default rule: |x - y| <= max(rel |y|, abs)
    return abs(x - y) <= max(rel * abs(y), abs_)


def r2(x):                                         # a percentage to two places
    return round(100 * x, 2)


# ---------- l1 ----------
fall1, fall2 = (110.00 - 121.00) / 121.00, (100.00 - 110.00) / 110.00
two(fall1, float(F(-1, 11)), 'l1 11/121'); two(fall2, float(F(-1, 11)), 'l1 10/110')
lv.expect('l1', 'screens[0].widget.options[0].text', r2(-fall1))            # about 9.09%
lv.expect('l1', 'screens[0].hints[2].text', r2(-fall1))
lv.expect('l1', 'screens[0].explain.text', r2(-fall1))
lv.expect('l1', 'screens[0].widget.options[3].text', r2(-fall1))
lv.expect('l1', 'screens[0].explain.canvas.caption', round(fall1, 4))      # -0.0909
lv.expect('l1', 'screens[1].canvas.state.caption', round(fall2, 4))
r = (255.00 - 250.00) / 250.00
two(r, float(F(5, 250)), 'l1 5/250')
lv.expect('l1', 'screens[3].widget.answer', r)
lv.expect('l1', 'screens[3].widget.wrong[0].value', 255.00 - 250.00)
lv.expect('l1', 'screens[3].widget.wrong[1].value', round(5 / 255, 4)); two(round(5 / 255, 4), round(float(F(5, 255)), 4), 'l1 5/255')
lv.expect('l1', 'screens[3].widget.wrong[2].value', 255.00 / 250.00)
lv.expect('l1', 'screens[3].widget.wrong[3].value', 100 * r)
lv.claim((3.00 - 1.00) / 1.00 == 3.00 - 1.00 == 2.0, 'l1 screens[4]: both versions give 2.0 at p0 = 1')
lv.expect('l1', 'screens[4].canvas.params.rows[0][2]', 2.0)
lv.claim((110.00 - 100.00) / 100.00 == 0.1, 'l1 screens[6]: 10/100 == 0.1 in floats')
p = [100.00, 110.00, 121.00]
rets = [(b - a) / a for a, b in zip(p, p[1:])]
lv.claim(rets == [0.1, 0.1], 'l1 screens[7]: daily_returns([100, 110, 121]) == [0.1, 0.1] exactly')
lv.expect('l1', 'quiz[1].explain.text', round(10 / 110, 4)); two(10 / 110, float(F(1, 11)), 'l1 quiz 10/110')
lv.expect('l1', 'quiz[1].widget.options[3].why', round(10 / 110, 4))
lv.expect('l1', 'quiz[2].widget.answer', len(list(zip([1, 2], [2]))))

# ---------- l2 ----------
lv.claim((90.00 - 100.00) / 100.00 == -0.1, 'l2 screens[4]: (90 - 100)/100 == -0.1 in floats')
pnl_up, pnl_dn = 40 * (13.75 - 12.50), 40 * (11.25 - 12.50)
two(pnl_up, 40 * F(5, 4), 'l2 profit'); two(pnl_dn, -40 * F(5, 4), 'l2 loss')
lv.claim(pnl_up == 50.0 and pnl_dn == -50.0, 'l2 screens[8]: the P&L floats are exact')
lv.expect('l2', 'screens[8].explain.text', 50.00); lv.expect('l2', 'screens[8].explain.text', -50.00)
lv.expect('l2', 'screens[8].hints[1].text', 1.25)
lv.expect('l2', 'screens[6].canvas.params.lines[2]', 2)                      # 2 passed (a console line since finding 29)

# ---------- l3 ----------
bad = (90.00 - 100.00) / 90.00
two(bad, float(F(-1, 9)), 'l3 -10/90')
lv.expect('l3', 'screens[2].canvas.params.lines[2]', bad)
lv.claim(repr(bad) == '-0.1111111111111111', 'l3 screens[2]: pytest shows -0.1111111111111111')
lv.expect('l3', 'screens[2].widget.options[0].text', bad)
lv.expect('l3', 'screens[3].explain.text', round(bad, 4)); lv.expect('l3', 'screens[3].explain.text', 0.1)
lv.expect('l3', 'screens[4].explain.text', 5.00 / 250.00)
mm = (121.00 - 100.00) / 121.00
two(mm, float(F(21, 121)), 'l3 21/121')
lv.claim(repr(mm) == '0.17355371900826447', 'l3 screens[8]: range bug value as pytest prints it')
lv.expect('l3', 'screens[8].canvas.right.params.lines[1]', mm)
lv.expect('l3', 'screens[8].explain.text', round(mm, 4))
lv.claim(('.F..F.F'.count('.'), '.F..F.F'.count('F'), len('.F..F.F')) == (4, 3, 7), 'l3 quiz[0]: 4 passed, 3 failed, 7 tests')
lv.expect('l3', 'quiz[0].widget.answer', 4); lv.expect('l3', 'quiz[0].widget.wrong[1].value', 7)
lv.claim(repr(10 / 110) == '0.09090909090909091', 'l3 quiz[1] list value as pytest prints it')
lv.expect('l3', 'quiz[2].explain.text', (60 - 80) / 80); two((60 - 80) / 80, F(-1, 4), 'l3 quiz[2]')
dd_dip = max((125 - x) / 125 for x in (100, 110))
lv.claim(dd_dip == (125 - 100) / 125 == 0.2, 'l3 screens[8]: dip path, range and true drawdown agree (0.2)')

# ---------- l4 ----------
x = (11.11 - 10.10) / 10.10
lv.claim(repr(x) == '0.09999999999999998', 'l4 screens[0]: (11.11 - 10.10)/10.10 prints 0.09999999999999998')
gap = 0.1 - x
two(gap, 2.7755575615628914e-17, 'l4 gap')
lv.expect('l4', 'screens[0].explain.text', float(f'{gap:.1e}'))                # 2.8e-17
bug = (11.11 - 10.10) / 11.11
lv.expect('l4', 'screens[1].canvas.params.rows[1][1]', round(bug, 4))
lv.expect('l4', 'screens[1].canvas.params.rows[1][2]', round(0.1 - bug, 4)); two(round(0.1 - bug, 4), round(float(F(1, 10) - F(101, 1111)), 4), 'l4 bug gap')
band = [k for k in range(-18, 0) if 2.8e-17 <= 10 ** k and 0.0091 > 10 ** k]
lv.claim(band == list(range(-16, -2)), 'l4 screens[1]: the safe band is 1e-16 to 1e-3', str(band))
lv.expect('l4', 'screens[2].canvas.state.caption', 1e-7)
lv.expect('l4', 'screens[3].widget.answer', 1250000.00 * 1e-6); two(1250000.00 * 1e-6, F(125, 100), 'l4 1.25')
for i, v in enumerate([1e-6, 0.125, 12.5]):
    lv.expect('l4', f'screens[3].widget.wrong[{i}].value', v)
z = 0.10 + 0.20 - 0.30
lv.claim(repr(z) == '5.551115123125783e-17', 'l4 screens[4]: 0.10 + 0.20 - 0.30 prints 5.551115123125783e-17')
lv.claim(approx_ok(z, 0.0) and not approx_ok(0.001, 0.0), 'l4 screens[4]: approx(0.0) takes 5.6e-17, rejects 0.001')
y = 110.00 / 100.00 - 1
lv.claim(repr(y) == '0.10000000000000009', 'l4 screens[5]: 110/100 - 1 prints 0.10000000000000009')
lv.expect('l4', 'screens[5].explain.canvas.caption', float(f'{y - 0.1:.1e}'))  # 8.3e-17
misses = [abs(f - 0.1) / 0.1 for f in (1.01 / 11.11, 11.11 / 10.10, -0.1, 10.0)]
lv.claim(min(misses) >= 0.09, 'l4 screens[6]: every bug misses by at least 9%', str(misses))
vol = statistics.stdev([0.01, -0.01]) * math.sqrt(252)
two(vol, math.sqrt(0.0002 * 252), 'l4 vol two ways')
lv.expect('l4', 'screens[8].explain.text', round(vol, 4))
lv.claim(not approx_ok(0.2245, vol), 'l4 screens[8]: a rounded 0.2245 is outside approx')
lv.claim(statistics.stdev([0.003] * 3) == 0.0, 'l4 screens[8]: a constant series has stdev 0.0')
lv.claim(repr(0.10 + 0.20) == '0.30000000000000004' and round(0.10 + 0.20) == 0, 'l4 quiz[0] values')
lv.expect('l4', 'quiz[1].widget.answer', 250.00 * 1e-6); two(250.00 * 1e-6, F(25, 100000), 'l4 0.00025')
lv.claim(len(list(zip(range(5), range(1, 5)))) == 4, 'l4 quiz[2]: five prices give four returns')
lv.expect('l4', 'quiz[2].explain.text', 'five prices, four returns')

# ---------- review-1 ----------
lv.expect('review', 'items[2].explain.text', r2(-fall1))
r1dd = (100.00 - 75.00) / 100.00                           # review-1 items[3]: peak 100.00, trough 75.00 (finding 25)
two(r1dd, float(F(25, 100)), 'r1 25/100')
lv.claim(r1dd == 0.25 and max(100.00 - x for x in (80.00, 100.00, 75.00, 90.00)) == 25.0, 'review-1 items[3]: the dip path 80, 100, 75, 90 has drawdown 0.25 exactly')
lv.expect('review', 'items[3].explain.text', r1dd); lv.expect('review', 'items[3].explain.text', 25); lv.expect('review', 'items[3].explain.text', 100)
lv.expect('review', 'items[3].widget.lines[3].text', r1dd)
lv.claim('0.2)' not in lv.text('review', 'items[3]') and '125' not in lv.text('review', 'items[3]'), 'review-1 items[3]: no trace of the l3 prices or 0.2')
# review-1 items[2] (finding 24): the reversed path 242, 220, 200 gives two falls of about 9.09%
rev = [(b - a) / a for a, b in zip([242.00, 220.00, 200.00], [242.00, 220.00, 200.00][1:])]
two(rev[0], float(F(-22, 242)), 'r1 22/242'); two(rev[1], float(F(-20, 220)), 'r1 20/220')
lv.claim(abs(rev[0] - rev[1]) < 1e-12 and r2(-rev[0]) == 9.09, 'review-1 items[2]: both falls of the reversed path are 9.09%')
lv.expect('review', 'items[2].explain.text', r2(-rev[0]))
lv.claim(all(x in lv.text('review', 'items[2].widget.options') for x in ('£200.00, £220.00, £242.00', '£200.00, £220.00, £200.00', '£200.00, £200.00, £200.00')),
         'review-1 items[2]: options use the £200.00 paths, not l1 screens[7]')
lv.expect('review', 'items[4].explain.text', (120 - 90) / 120); two((120 - 90) / 120, F(1, 4), 'r1 30/120')
lv.expect('review', 'items[6].widget.options[1].why', 1000000.00 * 1e-6)
lv.expect('review', 'items[6].widget.options[2].why', 1000000.00 * 0.005)
tr = 121.00 / 100.00 - 1
lv.claim(repr(tr) == '0.20999999999999996', 'review-1 items[7]: 121/100 - 1 prints 0.20999999999999996')
lv.expect('review', 'items[7].prose', tr)
lv.expect('review', 'items[7].explain.text', sum(rets))                     # 0.2
# pytest 8.1.1 prints approx(1000000.0, abs=0.005) as "1000000.0 ± 5.0e-03"; "± 0.005" is pytest 9 (finding)
lv.claim('1000000.0 ± 5.0e-03' in lv.text('review', 'items[6].explain.text'), 'review-1 items[6]: the explanation quotes the pytest 8.1.1 form 1000000.0 ± 5.0e-03')
lv.claim_text('review', 'items[6].explain.text', '1000000.0 ± 0.005', False,
              'review-1 items[6]: Pyodide pytest 8.1.1 prints 1000000.0 ± 5.0e-03, not ± 0.005')

# ---------- homework-1 ----------
# finding 25: homework-1 items[0] now tests the path 40, 50, 35, 45 (0.3) and the rise 100, 105, 120
dip, rise = [40.00, 50.00, 35.00, 45.00], [100.00, 105.00, 120.00]
hdd = (50.00 - 35.00) / 50.00
two(hdd, float(F(15, 50)), 'hw1 15/50')
lv.claim(hdd == 0.3, 'homework-1 items[0]: (50 - 35)/50 == 0.3 exactly')
lv.expect('homework', 'items[0].explain.text', hdd); lv.expect('homework', 'items[0].explain.text', 15); lv.expect('homework', 'items[0].explain.text', 50)
alt = 1 - 35.00 / 50.00
lv.claim(repr(alt) == '0.30000000000000004', 'homework-1 items[0]: 1 - 35/50 prints 0.30000000000000004')
lv.expect('homework', 'items[0].explain.text', alt)
lv.claim(alt != 0.3 and approx_ok(alt, 0.3), 'homework-1 items[0]: == fails the alternative correct version, approx accepts it')
right_h = lambda p: max((max(p[:i + 1]) - x) / max(p[:i + 1]) for i, x in enumerate(p))
alt_h = lambda p: max(1 - x / max(p[:i + 1]) for i, x in enumerate(p))
broken = {'range': lambda p: (max(p) - min(p)) / max(p), 'first': lambda p: (p[0] - min(p)) / p[0],
          'low': lambda p: max((max(p[:i + 1]) - x) / x for i, x in enumerate(p)), 'pounds': lambda p: max(max(p[:i + 1]) - x for i, x in enumerate(p)),
          'neg': lambda p: min((x - max(p[:i + 1])) / max(p[:i + 1]) for i, x in enumerate(p))}
paths = {'dip': (dip, 0.3), 'flat': ([100.00] * 3, 0.0), 'rise': (rise, 0.0)}
lv.claim(all(approx_ok(f(q), e) for f in (right_h, alt_h) for q, e in paths.values()), 'homework-1 items[0]: both correct versions pass all three paths under approx')
lv.claim(all(not all(approx_ok(f(q), e) for q, e in paths.values()) for f in broken.values()), 'homework-1 items[0]: every broken version fails at least one path',
         str({k: [round(f(q), 4) for q, _ in paths.values()] for k, f in broken.items()}))
lv.claim(not approx_ok(broken['range'](rise), 0.0) and approx_ok(broken['range'](dip), 0.3), 'homework-1 items[0]: the range bug hides on the dip and the steady rise catches it (0.1667)')
lv.claim(not approx_ok(broken['first'](dip), 0.3), 'homework-1 items[0]: the first-price bug fails the dip (0.125)')
lv.claim('125' not in lv.text('homework', 'items[0]') and '121' not in lv.text('homework', 'items[0]'), 'homework-1 items[0]: no trace of the l3 prices')
hw = [(52.00 - 50.00) / 50.00, (49.40 - 52.00) / 52.00, (49.40 - 49.40) / 49.40]
lv.claim(repr(hw[1]) == '-0.05000000000000003' and hw[0] == 0.04 and hw[2] == 0.0, 'homework-1 items[3] floats', repr(hw))
lv.expect('homework', 'items[3].explain.text', hw[1])
pvol = statistics.pstdev([0.01, -0.01]) * math.sqrt(252)
two(pvol, math.sqrt(0.0001 * 252), 'hw1 pstdev vol')
lv.claim(repr(pvol) == '0.15874507866387544' and repr(math.sqrt(0.0002 * 252)) == '0.22449944320643647',
         'homework-1 items[4]: the two values in the report')
lv.expect('homework', 'items[4].prose', float(f'{1e-6 * math.sqrt(0.0002 * 252):.1e}'))   # 2.2e-07
lv.expect('homework', 'items[4].explain.text', round(vol / pvol, 4)); two(vol / pvol, math.sqrt(2), 'hw1 ratio')
lv.expect('homework', 'items[4].widget.options[2].why', round(math.sqrt(365 / 252), 2))
lv.expect('homework', 'items[4].widget.options[3].why', round(vol - pvol, 3))
lv.expect('homework', 'items[4].feedback.correct', round(vol / pvol, 3))
d20 = [(22.00 - 20.00) / 20.00, (24.20 - 22.00) / 22.00]
lv.claim(d20 == [0.1, 0.09999999999999996], 'homework-1 items[6]: [20, 22, 24.20] gives [0.1, 0.09999999999999996]', repr(d20))
lv.claim((2.00 - 1.00) == (2.00 - 1.00) / 1.00, 'homework-1 items[6]: base price 1 hides the missing division')
lv.claim((100.00 - 90.00) / 100.00 == 0.1, 'homework-1 items[6]: 10/100 == 0.1')
# items[1]: a negative price also catches the version that accepts any price, so "exactly zero" is false (finding)
accepts_any = lambda line: (line.split(',')[0], float(line.split(',')[1]))
lv.claim(accepts_any('2024-03-06,-5.00')[1] < 0, 'a negative row passes through the planted version')
lv.claim('zero or less' in lv.text('homework', 'items[1].explain.text') and 'divide-by-100 and swap bugs' in lv.text('homework', 'items[1].explain.text'), 'homework-1 items[1]: the raises test needs a price of zero or less')
lv.claim_text('homework', 'items[1].explain.text', 'needs a price of exactly zero', False,
              'homework-1 items[1]: any price of zero or less catches the planted version, not only zero')

lv.check_wrongs()
lv.report()
