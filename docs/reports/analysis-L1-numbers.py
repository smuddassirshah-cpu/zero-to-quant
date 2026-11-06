"""Recompute every number stated in analysis level 1 (The real numbers), and check each where it is stated.
Run: python3 docs/reports/analysis-L1-numbers.py   (standard library only; exits 0 when every check passes)

Written by the second reader (docs/reviews/review-analysis-1-2.md). Route 1 is exact arithmetic with
fractions.Fraction or a closed form; route 2 is a brute-force search, a float computation or a second
algorithm (a seen-set walk of the fraction grid, a numerical lognormal integral). `two` asserts that the
routes agree; `E` (numbers_lib expect) checks the value appears at its JSON path.

Checks marked "finding N" test the value the review's fix asks for. They fail until the fix pass applies
that fix, by design: the content there is wrong or is to be replaced.
"""
import sys, os, math
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("analysis", 1)
E = lv.expect


def two(label, a, b, tol=1e-9):
    ok = math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)
    lv._rec(ok, f'two routes: {label}', '' if ok else f'{a!r} vs {b!r}')


def true(label, cond):
    lv._rec(bool(cond), label, '')


def r(x, k):
    return round(float(x), k)


# ---------------- l1 gaps in the rationals ----------------
two('(3/2)^2', F(3, 2) ** 2, 1.5 * 1.5); E('l1', 'screens[0].widget.rows[0][1].answer', 2.25)
two('(7/5)^2', F(7, 5) ** 2, 1.4 * 1.4); E('l1', 'screens[0].widget.rows[1][1].answer', 1.96)
for (p, q), shown, row in [((17, 12), 2.006944, 2), ((41, 29), 1.998811, 3), ((99, 70), 2.000204, 4)]:
    two(f'({p}/{q})^2 to 6 places', r(F(p, q) ** 2, 6), shown)
    E('l1', f'screens[0].widget.rows[{row}][1]', shown)
E('l1', 'screens[0].hints[2].text', 2.25); E('l1', 'screens[0].hints[2].text', 1.96)
E('l1', 'screens[0].feedback.byKey.r0c1', 4.5); two('3^2/2', F(9, 2), 4.5)
pairs = [(3, 2), (7, 5), (17, 12), (41, 29), (99, 70)]
for i, (p, q) in enumerate(pairs):
    v = p * p - 2 * q * q
    two(f'{p}^2 - 2*{q}^2', v, p ** 2 - 2 * q ** 2)
    E('l1', f'screens[1].widget.rows[{i}][2].answer', v)
    two(f'miss of ({p}/{q})^2 is 1/q^2', abs(F(p, q) ** 2 - 2), F(1, q * q))
for a, b in [(9, 8), (49, 50), (289, 288), (1681, 1682), (9801, 9800)]:
    E('l1', 'screens[1].hints[2].text', a); E('l1', 'screens[1].hints[2].text', b)
two('2*29^2', 2 * 29 ** 2, 1682); E('l1', 'screens[1].feedback.byKey.r3c2', 841)
two('2*70^2', 2 * 70 ** 2, 9800); E('l1', 'screens[1].feedback.byKey.r4c2', 4900)
two('1.4142^2', F(14142, 10000) ** 2, 1.99996164); E('l1', 'screens[2].widget.options[1].why', 1.99996164)
two('1.4143^2 to 5 places', r(F(14143, 10000) ** 2, 5), 2.00024); E('l1', 'screens[2].hints[1].text', 2.00024)
true('1.4142^2 < 2 < 1.4143^2', F(14142, 10000) ** 2 < 2 < F(14143, 10000) ** 2)
two('99/70 squared, shown', r(F(99, 70) ** 2, 6), 2.000204); E('l1', 'screens[2].widget.options[3].why', 2.000204)
two('41/29 = 1.413793 (number-line point)', r(F(41, 29), 6), 1.413793)
two('99/70 = 1.414286 (number-line point)', r(F(99, 70), 6), 1.414286)
true('41/29 and 99/70 inside the drag range 1.4135 to 1.415', 1.4135 < F(41, 29) < F(99, 70) < 1.415)
two('(2k+1)^2 = 2(2k^2+2k)+1 at k=7', (2 * 7 + 1) ** 2, 2 * (2 * 49 + 14) + 1)
true('6^2 = 36 is a multiple of 4 but 6 is not', 36 % 4 == 0 and 6 % 4 != 0); E('l1', 'screens[8].hints[2].text', 36)
true('9 divides 36 but not 6', 36 % 9 == 0 and 6 % 9 != 0); E('l1', 'screens[9].widget.options[1].why', 36)
true('2^2 = 4 leaves remainder 1 on division by 3', 4 % 3 == 1)
rows = [[str(p), str(p * p), str(p * p % 3)] for p in range(1, 7)]
true('l1 screen 9 remainder table', lv.files['l1-gaps-in-the-rationals']['screens'][9]['canvas']['params']['rows'] == rows)
x = 2 ** 0.5
true('repr(2 ** 0.5)', repr(x) == '1.4142135623730951')
true('repr(x * x)', repr(x * x) == '2.0000000000000004')
true('(2 ** 0.5) ** 2 == 2 is False', ((2 ** 0.5) ** 2 == 2) is False)
two('x*x - 2 is 2^-51, about 4.4e-16', x * x - 2, 2.0 ** -51, tol=1e-30)
E('l1', 'screens[10].explain.text', 10, fmt='10^{{-16}}')
true('round(9.60) == round(10.40) == 10', round(9.60) == round(10.40) == 10)
E('l1', 'screens[10].widget.options[2].why', 9.60); E('l1', 'screens[10].widget.options[2].why', 10.40)
two('577^2', 577 ** 2, 332929); two('408^2', 408 ** 2, 166464); two('2*408^2', 2 * 408 ** 2, 332928)
E('l1', 'quiz[0].widget.answer', 577 ** 2 - 2 * 408 ** 2)
E('l1', 'quiz[0].explain.text', 332929); E('l1', 'quiz[0].explain.text', 166464); E('l1', 'quiz[0].explain.text', 332928)
true('(3/2)^2 = 9/4', F(3, 2) ** 2 == F(9, 4))
true('sqrt16 = 4 rational', 4 * 4 == 16)
true('repr(0.1 + 0.2)', repr(0.1 + 0.2) == '0.30000000000000004')
true('0.2 + 0.1 == 0.3 is also False', (0.2 + 0.1 == 0.3) is False)
true('exact sum of stored 0.1 and 0.2 is not the stored 0.3', F(0.1) + F(0.2) != F(0.3))
# finding 1: the summary trap must not say the move "needs a prime": it holds for 6 = 2 x 3 as well
true('6 | p^2 implies 6 | p for p < 10000 (so "needs a prime" is false)', all(p % 6 == 0 for p in range(1, 10000) if p * p % 6 == 0))
E('l1', 'summary.trap', 'safe for a prime')

# ---------------- l2 least upper bound ----------------
def first_n(pred, start=1):
    n = start
    while not pred(n):
        n += 1
    return n

two('1 - 1/11', r(1 - F(1, 11), 3), 0.909); E('l2', 'screens[0].feedback.byKey.r0', 0.909)
two('1 - 1/101', r(1 - F(1, 101), 6), 0.990099); E('l2', 'screens[0].feedback.byKey.r1', 0.990099)
two('smallest n with 1 - 1/n > 0.99', first_n(lambda n: 1 - F(1, n) > F(99, 100)), math.floor(1 / 0.01) + 1)
E('l2', 'screens[7].widget.answer', 101)
true('n = 100 gives exactly 0.99', 1 - F(1, 100) == F(99, 100))
two('1 - 1/99 to 4 places', r(1 - F(1, 99), 4), 0.9899); E('l2', 'screens[7].feedback.byKey.ninetynine', 0.9899)
two('smallest n with 1 - 1/n > 0.999', first_n(lambda n: 1 - F(1, n) > F(999, 1000)), 1001); E('l2', 'quiz[1].widget.answer', 1001)
true('n = 1000 gives exactly 0.999', 1 - F(1, 1000) == F(999, 1000))
true('upper-bound candidates: only 1, 1.5, 2 are upper bounds', [c for c in (0.9, 0.99, 1, 1.5, 2) if all(1 - F(1, n) <= c for n in range(1, 5000))] == [1, 1.5, 2])
# finding 3: 0.95 = 1 - 1/20 is a term; the fixed why uses 0.97, which is not a term, and n = 34 passes it
true('0.95 is a term (n = 20)', 1 - F(1, 20) == F(95, 100))
true('0.97 is not a term', all(1 - F(1, n) != F(97, 100) for n in range(1, 10000)))
true('n = 34 gives a term above 0.97', 1 - F(1, 34) > F(97, 100)); two('1 - 1/34 to 4 places', r(1 - F(1, 34), 4), 0.9706)
E('l2', 'screens[6].widget.options[3].why', 0.97); E('l2', 'screens[6].widget.options[3].why', 34)
true('0.0005 is in (0, 3] and below 0.001', 0 < 0.0005 < 0.001 <= 3)
C = [(-1) ** n + F(1, n) for n in range(1, 13)]
for n, shown in [(1, 0), (2, 1.5), (3, -0.6667), (4, 1.25), (5, -0.8)]:
    two(f'C term {n}', r(C[n - 1], 4), shown); E('l2', 'screens[4].prose', shown)
two('C term 6', r(C[5], 4), 1.1667); two('C term 7', r(C[6], 4), -0.8571)
E('l2', 'screens[4].feedback.byKey.r0c1', 1.1667); E('l2', 'screens[4].feedback.byKey.r1c1', -0.8571)
two('sup C', max(C), 1.5); E('l2', 'screens[4].widget.rows[0][1].answer', 1.5)
true('inf C = -1 not attained: odd terms -1 + 1/n > -1 and -> -1', all(c > -1 for c in C) and min((-1) ** n + F(1, n) for n in range(1, 100001, 2)) < -1 + F(1, 10000))
E('l2', 'screens[4].widget.rows[1][1].answer', -1)
sh = [F(12, 10) - F(6, 10) / L for L in range(1, 13)]
for L, shown in [(1, 0.6), (2, 0.9), (3, 1.0), (4, 1.05), (5, 1.08)]:
    two(f'Sharpe at L={L}', sh[L - 1], shown)
for shown in (0.6, 0.9, 1.0, 1.05):
    E('l2', 'screens[11].prose', shown)
E('l2', 'screens[11].feedback.byKey.last', 1.08)
E('l2', 'screens[11].widget.answer', 1.2)
true('Sharpe canvas points match 1.2 - 0.6/L', all(abs(p['x'] - float(sh[i])) < 5e-6 for i, p in enumerate(lv.files['l2-least-upper-bound']['screens'][11]['canvas']['state']['points'])))
for s in (0, 1, 2, 5):
    pts = lv.files['l2-least-upper-bound']['screens'][s]['canvas']
    pts = pts['left'] if 'left' in pts else pts
    ok = all(abs(p['x'] - float(1 - F(1, int(p['id'][1:])))) < 5e-6 for p in pts['state']['points'] if p['id'].startswith('a'))
    true(f'l2 screen {s} points are 1 - 1/n', ok)
true('l2 screen 4 points are (-1)^n + 1/n', all(abs(p['x'] - float(C[int(p['id'][1:]) - 1])) < 5e-6 for p in lv.files['l2-least-upper-bound']['screens'][4]['canvas']['state']['points']))
true('2.9995 is in (-3, 3) and above 2.999', 2.9995 ** 2 < 9 and 2.9995 > 2.999)
true('3 - eps/2 in E and above 3 - eps for 0 < eps < 12', all(-3 < 3 - e / 2 < 3 and 3 - e / 2 > 3 - e for e in (0.001, 0.5, 1, 5, 11.9)))
two('high-water mark', max([100, 104, 101, 107, 103]), 107); E('l2', 'quiz[3].widget.answer', 107)
true('smaller term 1/1001 below 1/1000', F(1, 1001) < F(1, 1000))

# ---------------- l3 completeness ----------------
def bisect(c, a, b, steps, power=2):
    a, b = F(a), F(b)
    out = []
    for _ in range(steps):
        m = (a + b) / 2
        out.append((m, m ** power))
        if m ** power < c:
            a = m
        else:
            b = m
    return a, b, out

a4, b4, mids = bisect(2, 1, 2, 4)
for k, (m, m2) in enumerate(mids):
    two(f'sqrt2 bisection midpoint square {k + 1} to 4 places', r(m2, 4), [2.25, 1.5625, 1.8906, 2.0664][k])
E('l3', 'screens[0].widget.rows[1][1]', 1.5625); E('l3', 'screens[0].widget.rows[2][1]', 1.8906); E('l3', 'screens[0].widget.rows[3][1]', 2.0664)
ends = []
a, b = F(1), F(2)
for k in range(4):
    m = (a + b) / 2
    a, b = (m, b) if m * m < 2 else (a, m)
    ends.append((a, b))
for k, row in [(1, 1), (2, 2), (3, 3)]:
    E('l3', f'screens[0].widget.rows[{row}][2].answer', float(ends[k][0])); E('l3', f'screens[0].widget.rows[{row}][3].answer', float(ends[k][1]))
a10, b10, _ = bisect(2, 1, 2, 10)
true('10 halvings give [181/128, 1449/1024]', (a10, b10) == (F(181, 128), F(1449, 1024)))
two('width after 10 halvings', b10 - a10, 2.0 ** -10); E('l3', 'screens[1].widget.answer', 0.0009765625)
true('181/128 = 1448/1024', F(181, 128) == F(1448, 1024))
two('wrong nine: 1/512', F(1, 512), 0.001953125); E('l3', 'screens[1].widget.wrong[0].value', 0.001953125)
two('case one bound at s = 1.4', (2 * F(14, 10) + 1) / (2 - F(14, 10) ** 2), 3.8 / 0.04); E('l3', 'screens[4].widget.answer', 95)
two('slip 3.8/0.4', F(38, 10) / F(4, 10), 9.5); two('flip 0.04/3.8 to 4 places', r(F(4, 100) / F(38, 10), 4), 0.0105)
two('(1.4 + 1/96)^2 to 5 places', r((F(14, 10) + F(1, 96)) ** 2, 5), 1.98928); E('l3', 'screens[4].feedback.correct', 1.98928)
two('(1.4 + 1/95)^2 to 5 places', r((F(14, 10) + F(1, 95)) ** 2, 5), 1.98958); E('l3', 'screens[4].explain.text', 1.98958)
two('1.4 + 1/96 (canvas point)', r(F(14, 10) + F(1, 96), 6), 1.410417)
two('case two bound at s = 1.5', 2 * F(3, 2) / (F(3, 2) ** 2 - 2), 12); E('l3', 'screens[6].widget.answer', 12)
two('half: s on top', F(3, 2) / F(1, 4), 6); two('flip 0.25/3', r(F(1, 4) / 3, 4), 0.0833); two('nosub 3/2.25', r(3 / F(9, 4), 4), 1.3333)
two('(1.5 - 1/13)^2 to 5 places', r((F(3, 2) - F(1, 13)) ** 2, 5), 2.02515); E('l3', 'screens[6].feedback.correct', 2.02515)
two('(1.5 - 1/12)^2 to 5 places', r((F(3, 2) - F(1, 12)) ** 2, 5), 2.00694); E('l3', 'screens[6].explain.text', 2.00694)
two('1.5 - 1/13 (canvas point)', r(F(3, 2) - F(1, 13), 6), 1.423077)
true('case two: s - 1/n > 0 whenever n > 2s/(s^2 - 2)', all(s - 1 / (2 * s / (s * s - 2) + 1e-9) > 0 for s in (1.42, 1.5, 1.9, 2.0)))
two('quiz s = 1.41 bound', r((2 * F(141, 100) + 1) / (2 - F(141, 100) ** 2), 3), 321.008); E('l3', 'quiz[2].explain.text', 321.008)
two('quiz smallest n beyond the bound', math.floor((2 * F(141, 100) + 1) / (2 - F(141, 100) ** 2)) + 1, 322); E('l3', 'quiz[2].widget.answer', 322)
two('1.41^2', F(141, 100) ** 2, 1.9881); two('(1.41 + 1/322)^2 to 5 places', r((F(141, 100) + F(1, 322)) ** 2, 5), 1.99687)
E('l3', 'quiz[2].explain.text', 1.99687)
a2, b2, _ = bisect(3, 1, 2, 2)
true('sqrt3 bisection after 2: [3/2, 7/4]', (a2, b2) == (F(3, 2), F(7, 4))); E('l3', 'quiz[1].widget.answer', 1.75)
two('1.75^2', F(7, 4) ** 2, 3.0625); E('l3', 'quiz[1].explain.text', 3.0625)
true('cube root of 5 below 2 (2^3 = 8 > 5)', 5 ** (1 / 3) < 2 and 2 ** 3 == 8)
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
def call(sig):
    return 100 * (2 * Phi(sig / 2) - 1)
def call_mc(sig, n=200000):  # route 2: lognormal integral by the midpoint rule
    tot = 0.0
    lo, hi = -10.0, 10.0
    h = (hi - lo) / n
    for i in range(n):
        z = lo + (i + 0.5) * h
        sT = 100 * math.exp(-0.5 * sig * sig + sig * z)
        tot += max(sT - 100, 0) * math.exp(-z * z / 2)
    return tot * h / math.sqrt(2 * math.pi)
for sig, shown in [(0.2, 7.97), (0.25, 9.95), (0.3, 11.92), (0.275, 10.94)]:
    two(f'ATM call at {sig}', r(call(sig), 2), shown); two(f'ATM call at {sig}, integral', r(call_mc(sig), 2), shown)
for shown in ('7.97', '9.95', '11.92'):
    E('l3', 'screens[11].canvas.params.rows', shown)
E('l3', 'screens[11].feedback.correct', 10.94)
lo_, hi_ = 0.2, 0.3
for _ in range(60):
    mid = (lo_ + hi_) / 2
    lo_, hi_ = (mid, hi_) if call(mid) < 10 else (lo_, mid)
two('implied vol for 10.00', r(lo_ * 100, 2), 25.13); E('l3', 'screens[11].explain.text', 25.13)
E('l3', 'screens[11].widget.answer', 0.275)

# ---------------- l4 archimedes ----------------
arch = lambda e: math.floor(1 / F(e)) + 1
for e, n in [(F(3, 1000), 334), (F(7, 100), 15), (F(7, 10000), 1429)]:
    two(f'smallest n with 1/n < {e}', arch(e), first_n(lambda k: F(1, k) < e))
E('l4', 'screens[5].widget.answer', 334); E('l4', 'quiz[0].widget.answer', 15); E('l4', 'screens[11].widget.answer', 1429)
two('1/0.003 to 2 places', r(1 / F(3, 1000), 2), 333.33); two('1/333 to 6', r(F(1, 333), 6), 0.003003); two('1/334 to 6', r(F(1, 334), 6), 0.002994)
E('l4', 'screens[5].explain.text', 0.003003); E('l4', 'screens[5].explain.text', 0.002994)
true('1/300 is above 0.003', F(1, 300) > F(3, 1000))
two('1/0.07 to 2', r(1 / F(7, 100), 2), 14.29); two('1/14 to 4', r(F(1, 14), 4), 0.0714); two('1/15 to 4', r(F(1, 15), 4), 0.0667)
two('1/0.0007 to 2', r(1 / F(7, 10000), 2), 1428.57); two('1/1428 to 8', r(F(1, 1428), 8), 0.00070028); two('1/1429 to 8', r(F(1, 1429), 8), 0.00069979)
E('l4', 'screens[11].feedback.byKey.floor', 0.00070028); E('l4', 'screens[11].feedback.correct', 0.00069979)
two('tick gap', F(100019, 10000) - F(100012, 10000), 0.0007)
def recipe(a, b):
    n = arch(b - a)
    return math.floor(n * a) + 1, n
m, n = recipe(F(31, 100), F(32, 100))
true('density recipe for 0.31, 0.32 gives (32, 101)', (m, n) == (32, 101))
E('l4', 'screens[6].widget.rows[0][1].answer', 101); E('l4', 'screens[6].widget.rows[1][1].answer', 32)
two('32/101 to 6', r(F(32, 101), 6), 0.316832); E('l4', 'screens[6].widget.rows[2][1].answer', 0.316832)
two('101 * 0.31', 101 * F(31, 100), 31.31); two('31/101 to 6', r(F(31, 101), 6), 0.306931); E('l4', 'screens[8].prose', 0.306931)
true('ceil trap: a = 0, b = 0.1 gives n = 11 and ceil(0) = 0', recipe(F(0), F(1, 10))[1] == 11 and math.ceil(0) == 0)
two('0.31 + sqrt2/1000 to 6', r(0.31 + math.sqrt(2) / 1000, 6), 0.311414); two('sqrt2/4 to 4', r(math.sqrt(2) / 4, 4), 0.3536)
true('0.315 = 63/200', F(315, 1000) == F(63, 200))
m, n = recipe(F(1, 3), F(1, 2))
true('recipe for 1/3, 1/2 gives (3, 7)', (m, n) == (3, 7)); two('3/7 to 6', r(F(3, 7), 6), 0.428571); two('2/7 to 6', r(F(2, 7), 6), 0.285714)
true('with n = 6 the recipe lands on b', F(math.floor(6 * F(1, 3)) + 1, 6) == F(1, 2))

# ---------------- l5 counting infinite sets ----------------
Zlist = [0] + [s * k for k in range(1, 50) for s in (1, -1)]
two('position of -3', Zlist.index(-3) + 1, 2 * 3 + 1); E('l5', 'screens[0].widget.answer', 7)
two('position of 4', Zlist.index(4) + 1, 2 * 4); E('l5', 'quiz[0].widget.answer', 8)
def walk(limit):  # route 1: gcd skip
    out = []
    s = 2
    while len(out) < limit:
        for p in range(1, s):
            if math.gcd(p, s - p) == 1:
                out.append(F(p, s - p))
        s += 1
    return out[:limit]
def walk_seen(limit):  # route 2: seen-set skip
    out, seen = [], set()
    s = 2
    while len(out) < limit:
        for p in range(1, s):
            v = F(p, s - p)
            if v not in seen:
                seen.add(v); out.append(v)
        s += 1
    return out[:limit]
W = walk(200)
true('two walks agree on 200 places', W == walk_seen(200))
pos = lambda v: W.index(F(v)) + 1
true('first six of the walk', W[:6] == [F(1), F(1, 2), F(2), F(1, 3), F(3), F(1, 4)])
for v, p, path in [(F(3, 2), 8, 'screens[2].widget.rows[0][1].answer'), (F(2, 3), 7, 'screens[2].widget.rows[1][1].answer'), (F(1, 5), 10, 'screens[2].widget.rows[2][1].answer'), (F(1, 6), 12, 'quiz[1].widget.answer')]:
    two(f'walk position of {v}', pos(v), p); E('l5', path, p)
two('5/1 position', pos(5), 11)
def walk_rep_pos(p, q):  # counting repeats
    s = p + q
    return sum(range(1, s - 1)) + p
two('1/5 counting 2/2 too', pos(F(1, 5)) + 1, 11)
two('1/6 with repeats counted', walk_rep_pos(1, 6), 16)
two('diagonals 2 to 6 hold 11', sum(1 for v in W if v.numerator + v.denominator <= 6), 1 + 2 + 2 + 4 + 2)
xs = ['14159', '71828', '41421', '57751', '30103']
diag = [int(xs[k][k]) for k in range(5)]
true('diagonal digits 1, 1, 4, 5, 3', diag == [1, 1, 4, 5, 3])
newd = [4 if d == 5 else 5 for d in diag]
true('x = 0.55545', newd == [5, 5, 5, 4, 5]); E('l5', 'screens[5].hints[2].text', 0.55545)
for k in range(5):
    E('l5', f'screens[5].widget.rows[{k}][1].answer', diag[k]); E('l5', f'screens[5].widget.rows[{k}][2].answer', newd[k])
true('4s and 5s lie in [4/9, 5/9], inside (0.4, 0.6)', F(4, 10) < F(4, 9) and F(5, 9) < F(6, 10))
true('x < x_2 = 0.71828', 0.5555 < 0.71828)
two('0.4999... = 0.4 + 0.09/(1 - 0.1)', F(4, 10) + F(9, 100) / (1 - F(1, 10)), 0.5)
qd = ['25000', '55500', '12300']
q = [4 if int(qd[k][k]) == 5 else 5 for k in range(3)]
two('quiz diagonal number', F(q[0] * 100 + q[1] * 10 + q[2], 1000), 0.545); E('l5', 'quiz[3].widget.answer', 0.545)
two('quiz copy slip', F(int(qd[0][0]) * 100 + int(qd[1][1]) * 10 + int(qd[2][2]), 1000), 0.253)
# finding 5: the 0-or-9 console example must follow the stated rule (0 becomes 9, any other digit becomes 0)
xl = ['1000', '2000', '3000', '4000']   # x_1 = 0.1000..., x_k has digit k equal to 0 for k >= 2
rule = ''.join('9' if xl[k][k] == '0' else '0' for k in range(4))
true('the 0/9 rule on x_1 = 0.1000... writes 0.0999...', rule == '0999')
true('0.0999... = 0.1 = x_1', F(9, 100) / (1 - F(1, 10)) == F(1, 10))
E('l5', 'screens[9].canvas.params.lines', '0.0999999... = 0.1 = x_1')

# ---------------- review-1 ----------------
Ev = [(-1) ** n * (1 - F(1, n)) for n in range(1, 9)]
true('review E first terms', Ev[:6] == [0, F(1, 2), F(-2, 3), F(3, 4), F(-4, 5), F(5, 6)]); two('E at n = 8', Ev[7], F(7, 8))
true('sup E = 1, inf E = -1, neither attained', all(-1 < v < 1 for v in [(-1) ** n * (1 - F(1, n)) for n in range(1, 2000)]))
# finding 9 (freshness): items[2] becomes 1/(2n + 1) < 0.004
two('smallest n with 1/(2n+1) < 0.004', first_n(lambda k: F(1, 2 * k + 1) < F(4, 1000)), 125)
true('n = 124 gives 1/249 > 0.004', F(1, 249) > F(4, 1000)); two('1/251 to 6', r(F(1, 251), 6), 0.003984)
E('review', 'items[2].widget.answer', 125); E('review', 'items[2].widget.wrong[0].value', 124); E('review', 'items[2].widget.wrong[1].value', 251)
# finding 9 (freshness): items[3] becomes a = -0.3, b = -0.29
m, n = recipe(F(-3, 10), F(-29, 100))
true('recipe for -0.3, -0.29 gives (-30, 101)', (m, n) == (-30, 101))
two('101 * -0.3', 101 * F(-3, 10), -30.3); two('-30/101 to 6', r(F(-30, 101), 6), -0.29703)
true('-30/101 is in the gap', F(-3, 10) < F(-30, 101) < F(-29, 100))
true('truncating -30.3 gives m = -29, outside the gap', F(int(-30.3) + 1, 101) > F(-29, 100))
E('review', 'items[3].widget.rows[0][1].answer', 101); E('review', 'items[3].widget.rows[1][1].answer', -30)
two('review walk position of 3/4', pos(F(3, 4)), 14); E('review', 'items[4].widget.answer', 14)
two('3/4 with repeats counted', walk_rep_pos(3, 4), 18)
# finding 9 (freshness): items[6] becomes sqrt5 on [2, 3]
a5, b5, mids5 = bisect(5, 2, 3, 3)
true('sqrt5 bisection after 3 halvings: [17/8, 9/4]', (a5, b5) == (F(17, 8), F(9, 4)))
for (mm, m2), shown in zip(mids5, (6.25, 5.0625, 4.515625)):
    two(f'sqrt5 midpoint {mm} squared', m2, shown)
E('review', 'items[6].widget.answer', 2.125); E('review', 'items[6].explain.text', 4.515625)
# finding 9: items[0] becomes a multi on n | p^2 => n | p
for nn, holds in [(3, True), (6, True), (10, True), (9, False), (12, False), (8, False)]:
    true(f'n = {nn}: n | p^2 => n | p is {holds}', all(p % nn == 0 for p in range(1, 5000) if p * p % nn == 0) == holds)
true('counterexamples 3 for 9, 6 for 12, 4 for 8', 9 % 9 == 0 and 3 % 9 and 36 % 12 == 0 and 6 % 12 and 16 % 8 == 0 and 4 % 8)

# ---------------- homework-1 ----------------
two('smallest n with 1 - 1/n^2 > 0.9999', first_n(lambda k: 1 - F(1, k * k) > F(9999, 10000)), 101); E('homework', 'items[2].widget.answer', 101)
two('no-root slip 1/eps + 1', first_n(lambda k: F(1, k) < F(1, 10000)), 10001)
m, n = recipe(F(1414, 1000), F(14143, 10000))
true('recipe for 1.414, 1.4143 gives (4715, 3334)', (m, n) == (4715, 3334))
E('homework', 'items[4].widget.rows[0][1].answer', 3334); E('homework', 'items[4].widget.rows[1][1].answer', 4715)
two('3334 * 1.414', 3334 * F(1414, 1000), 4714.276); two('4715/3334 to 7', r(F(4715, 3334), 7), 1.4142172)
two('1/0.0003 to 2', r(1 / F(3, 10000), 2), 3333.33)
two('20th fraction', W[19], F(5, 3)); two('19th', W[18], F(3, 5)); two('21st', W[20], 7)
E('homework', 'items[5].widget.answer', 1.6666667)
grid_rep = [F(p, s - p) for s in range(2, 12) for p in range(1, s)]
two('20th cell with repeats', grid_rep[19], F(5, 2))
two('0.31 - sqrt2 to 4', r(0.31 - math.sqrt(2), 4), -1.1042); two('0.32 - sqrt2 to 4', r(0.32 - math.sqrt(2), 4), -1.0942)
two('sqrt2 - 1.1 to 4', r(math.sqrt(2) - 1.1, 4), 0.3142)
true('rubric totals 10', sum(x['points'] for x in lv.files['homework-1']['items'][7]['rubric']) == 10)
true('-1.1 lies between the shifted ends', 0.31 - math.sqrt(2) < -1.1 < 0.32 - math.sqrt(2))
true('sqrt2+sqrt3 step: sqrt2 = (r^2 - 1)/(2r)', math.isclose(((math.sqrt(2) + math.sqrt(3)) ** 2 - 1) / (2 * (math.sqrt(2) + math.sqrt(3))), math.sqrt(2)))

# fix pass: numbers written by the fixes
true('hint in l1 screens[10]: x*x - 2 is about 4e-16', 4e-16 < (2 ** 0.5) ** 2 - 2 < 5e-16)
E('l1', 'screens[10].hints[1].text', '4 \\times 10^{-16}')
true('1/249 is about 0.004016', r(F(1, 249), 6) == 0.004016); E('review', 'items[2].feedback.byKey.edge', 0.004016)
two('2n + 1 > 250 means n > 124.5', F(250 - 1, 2), 124.5); E('review', 'items[2].explain.text', 124.5)
true('floor(-30.3) = -31, so m = -30', math.floor(F(-303, 10)) == -31 and -31 + 1 == -30); E('review', 'items[3].feedback.byKey.r1c1', -31)
two('2.5^2', 2.5 ** 2, 6.25); two('2.25^2', 2.25 ** 2, 5.0625); E('review', 'items[6].explain.text', 6.25); E('review', 'items[6].explain.text', 5.0625)
true('review-1 items[0] is the multi with keys n3 and n6 only', [o['id'] for o in lv.files['review-1']['items'][0]['widget']['options'] if o.get('correct')] == ['n3', 'n6'])
true('l3 screens[7] names its cases', lv.files['l3-completeness']['screens'][7]['widget']['lines'][1]['text'].startswith('Case one') and lv.files['l3-completeness']['screens'][7]['widget']['lines'][3]['text'].startswith('Case two'))
true('l2 screens[9] and review-1 items[8] label their parts', lv.files['l2-least-upper-bound']['screens'][9]['widget']['lines'][0]['text'].startswith('Part one') and lv.files['review-1']['items'][8]['widget']['lines'][0]['text'].startswith('Part one'))

lv.check_wrongs()
lv.report()
