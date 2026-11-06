"""Recompute every number stated in analysis level 2 (Sequences), and check each where it is stated.
Run: python3 docs/reports/analysis-L2-numbers.py   (standard library only; exits 0 when every check passes)

Written by the second reader (docs/reviews/review-analysis-1-2.md). Route 1 is exact arithmetic with
fractions.Fraction or a closed form; route 2 is a brute-force scan (the last index that fails up to a horizon,
plus one), float arithmetic or a recursion. `two` asserts the routes agree; `E` (numbers_lib expect) checks the
value appears at its JSON path.

Checks marked "finding N" test the value the review's fix asks for. They fail until the fix pass applies that
fix, by design.
"""
import sys, os, math
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("analysis", 2)
E = lv.expect


def two(label, a, b, tol=1e-9):
    ok = math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol)
    lv._rec(ok, f'two routes: {label}', '' if ok else f'{a!r} vs {b!r}')


def true(label, cond):
    lv._rec(bool(cond), label, '')


def r(x, k):
    return round(float(x), k)


def tail_start(gap, eps, horizon=20000):
    """Route 2: one past the last n <= horizon whose gap is not below eps."""
    last = 0
    for n in range(1, horizon + 1):
        if not gap(n) < eps:
            last = n
    return last + 1


def first_n(pred, start=1):
    n = start
    while not pred(n):
        n += 1
    return n


def pts(file, s, key='screens'):
    import re
    return [q for q in lv.files[file][key][s]['canvas']['state']['points'] if re.fullmatch(r'[a-z]+\d+', q['id'])]

# ---------------- l6 epsilon and N ----------------
L6 = 'l6-epsilon-and-n'
a = lambda n: F(2 * n + 1, n + 3)
gap = lambda n: abs(a(n) - 2)
true('a_n starts 3/4, 1, 7/6, 9/7', [a(n) for n in range(1, 5)] == [F(3, 4), 1, F(7, 6), F(9, 7)])
true('|a_n - 2| = 5/(n+3) for n <= 500', all(gap(n) == F(5, n + 3) for n in range(1, 501)))
two('gap at n = 40', r(gap(40), 4), 0.1163); E('l6', 'screens[0].canvas.state.caption', 0.1163)
true('gap at 47 is exactly 0.1', gap(47) == F(1, 10)); two('gap at 48', r(gap(48), 4), 0.098)
two('first index inside 2 +- 0.1', tail_start(gap, F(1, 10)), math.floor(5 / F(1, 10) - 3) + 1); E('l6', 'screens[0].widget.points[0].target', 48)
for e, n in [(F(1, 4), 18), (F(1, 2), 8), (F(1, 20), 98)]:
    two(f'first good n at eps {e}', tail_start(gap, e), n)
E('l6', 'screens[1].canvas.state.caption', 18); E('l6', 'screens[1].hints[1].text', 8); E('l6', 'screens[1].hints[1].text', 98)
true('canvas points of screens 0, 1 are a_n', all(abs(p['y'] - float(a(int(p['id'][1:])))) < 5e-6 for s in (0, 1) for p in pts(L6, s)))
two('threshold at eps = 0.1', 5 / F(1, 10) - 3, 47)
two('N at eps = 0.01', tail_start(gap, F(1, 100)), 498); E('l6', 'screens[4].widget.answer', 498)
true('gap at 497 is exactly 0.01', gap(497) == F(1, 100)); two('5/501 to 5', r(F(5, 501), 5), 0.00998)
two('no-shift slips', math.ceil(5 / F(1, 100)), 500); two('no-shift-1', math.floor(5 / F(1, 100)) + 1, 501); two('plus slip', math.floor(5 / F(1, 100) + 3) + 1, 504)
for shown, n in [(1.75, 1), (1.5, 2), (1.33, 3), (1.21, 4)]:
    two(f'gap to 2.5 at n = {n}', r(abs(a(n) - F(5, 2)), 2), shown)
true('gap to 2.5 is 0.5 + 5/(n+3) > 0.5', all(abs(a(n) - F(5, 2)) == F(1, 2) + F(5, n + 3) for n in range(1, 300)))
two('threshold at eps = 2', 5 / F(2) - 3, -0.5); E('l6', 'screens[8].prose', -0.5)
two('eps where threshold reaches 1', F(5, 4), 1.25); E('l6', 'screens[8].explain.text', 1.25)
two('binomial steps', first_n(lambda n: F(3, n) < F(1, 100)), 301); E('l6', 'screens[11].widget.answer', 301)
true('300 steps gives exactly 0.01', F(3, 300) == F(1, 100))
# finding 24: the transfer's slips at the asked rounding are 31 (0.1p) and 30001 (pounds)
two('0.1p slip', first_n(lambda n: F(3, n) < F(1, 10)), 31); two('pounds slip', first_n(lambda n: F(3, n) < F(1, 10000)), 30001)
E('l6', 'screens[11].widget.wrong[*].value', 31); E('l6', 'screens[11].widget.wrong[*].value', 30001)
b = lambda n: F(3 * n, n + 1)
true('|3n/(n+1) - 3| = 3/(n+1)', all(abs(b(n) - 3) == F(3, n + 1) for n in range(1, 300)))
two('quiz N at 0.05', tail_start(lambda n: abs(b(n) - 3), F(1, 20)), 60); E('l6', 'quiz[2].widget.answer', 60)
two('3/61 to 4', r(F(3, 61), 4), 0.0492)
true('quiz alt: |a_n - 1| >= 1/2 for n >= 2', all(abs(F((-1) ** n, n) - 1) >= F(1, 2) for n in range(2, 500)))
# finding 21: the code exercise needs a test that a float version fails
def smallest_n(eps):
    t = 5 / F(eps) - 3
    return max(1, math.floor(t) + 1)
def smallest_n_float(eps):
    t = 5 / float(eps) - 3
    return max(1, math.floor(t) + 1)
two('smallest_n(5/29) exact', smallest_n(F(5, 29)), tail_start(gap, F(5, 29)))
true('a float version gets 5/29 wrong (26)', smallest_n_float(F(5, 29)) == 26)
true('code tests include Fraction(5, 29) -> 27', any(t['call'] == 'smallest_n(Fraction(5, 29))' and t['expect'] == '27' for t in lv.files[L6]['screens'][10]['widget']['tests']))
for e, n in [(F(1, 10), 48), (F(1, 100), 498), (F(1, 2), 8), (1, 3), (2, 1), (F(3, 100), 164), (F(5, 51), 49), (F(1, 1000), 4998), (F(7, 3), 1)]:
    two(f'smallest_n({e}) by scan', tail_start(gap, F(e)), n)
E('l6', 'quiz[0].prose', 'Four students')   # finding 30

# ---------------- l7 limit laws ----------------
L7 = 'l7-limit-laws-proved'
sg = lambda n: F(3, n)   # a_n + b_n - 5
two('sum gap at 24', r(sg(24), 4), 0.125); E('l7', 'screens[0].canvas.state.caption', 0.125)
two('first index for the sums', tail_start(sg, F(1, 10)), 31); E('l7', 'screens[0].widget.points[0].target', 31)
two('3/31 to 4', r(F(3, 31), 4), 0.0968)
true('screen 0 points are 5 + 3/n', all(abs(p['y'] - (5 + 3 / int(p['id'][1:]))) < 5e-6 for p in pts(L7, 0)))
two('N1 at eps 0.2', tail_start(lambda n: F(1, n), F(1, 10)), 11); two('N2 at eps 0.2', tail_start(lambda n: F(2, n), F(1, 10)), 21)
E('l7', 'screens[1].canvas.state.caption', 11); E('l7', 'screens[1].canvas.state.caption', 21)
two('N1 at eps 0.1', tail_start(lambda n: F(1, n), F(1, 20)), 21); two('N2 at eps 0.1', tail_start(lambda n: F(2, n), F(1, 20)), 41)
E('l7', 'screens[2].widget.rows[0][1].answer', 21); E('l7', 'screens[2].widget.rows[1][1].answer', 41); E('l7', 'screens[2].widget.rows[2][1].answer', 41)
two('2/25', F(2, 25), 0.08); two('3/25', F(3, 25), 0.12); E('l7', 'screens[3].explain.text', 0.12)
an = lambda n: 3 + F(1, n); bn = lambda n: 2 - F(1, n)
true('|a_n| <= 4', all(abs(an(n)) <= 4 for n in range(1, 1000)))
two('product: b index', tail_start(lambda n: abs(bn(n) - 2), F(1, 100) / 8), 801)
two('product: a index', tail_start(lambda n: abs(an(n) - 3), F(1, 100) / 4), 401)
E('l7', 'screens[8].widget.rows[0][1].answer', 801); E('l7', 'screens[8].widget.rows[1][1].answer', 401); E('l7', 'screens[8].widget.rows[2][1].answer', 801)
true('|a_n b_n - 6| = 1/n + 1/n^2', all(abs(an(n) * bn(n) - 6) == F(1, n) + F(1, n * n) for n in range(1, 500)))
two('direct first index', tail_start(lambda n: abs(an(n) * bn(n) - 6), F(1, 100)), 101); E('l7', 'screens[8].widget.rows[3][1].answer', 101)
two('direct gap at 100', abs(an(100) * bn(100) - 6), 0.0101); two('direct gap at 101 to 6', r(abs(an(101) * bn(101) - 6), 6), 0.009999)
two('801/101 is nearly 8', r(F(801, 101), 2), 7.93); E('l7', 'screens[8].explain.text', 'nearly eight')
two('quiz sum-law N', max(tail_start(lambda n: F(1, n), F(1, 10)), tail_start(lambda n: F(3, n), F(1, 10))), 31); E('l7', 'quiz[0].widget.answer', 31)
two('quiz direct', tail_start(lambda n: F(4, n), F(1, 5)), 21)
two('quiz M', max(6, 5, 1, 2 + 1), 6); E('l7', 'quiz[2].widget.answer', 6)
two('valuation bound', 5010 * F(2, 100) + 40 * 10, 500.2); E('l7', 'screens[11].widget.answer', 500.2)
two('worst case directly', max(abs(x * y - 200000) for x in (4990, 5010) for y in (F(3998, 100), F(4002, 100))), 500.2)
two('no-cross slip', 5000 * F(2, 100) + 400, 500); two('cross term', 10 * F(2, 100), 0.2); two('shares-only', 400, 40 * 10); two('price-only', 5000 * F(2, 100), 100)
true('d1 counterexample: right side 0, left side 3/n', all(abs(3 * (2 + F(1, n)) - 6) == F(3, n) for n in range(1, 50)))
true('quotient bound: |b_n| > |b|/2 gives |1/b_n - 1/b| < 2|b_n - b|/|b|^2', all(abs(1 / (F(2) + F(1, n)) - F(1, 2)) < 2 * abs(F(1, n)) / 4 for n in range(1, 200)))

# ---------------- l8 bounded and monotone ----------------
L8 = 'l8-bounded-and-monotone'
seq = [1.0]
for _ in range(15):
    seq.append(math.sqrt(2 + seq[-1]))
for k, shown in enumerate([1, 1.7321, 1.9319, 1.9829, 1.9957]):
    two(f'term {k + 1}', r(seq[k], 4), shown)
two('term 2 is sqrt3', seq[1], 3 ** 0.5)
true('terms rise and stay below 2', all(seq[k] < seq[k + 1] < 2 for k in range(14)))
for k, shown in enumerate([1, 0.268, 0.068, 0.017, 0.0043]):
    two(f'gap {k + 1}', r(2 - seq[k], 4 if k == 4 else 3), shown)
E('l8', 'screens[9].explain.text', 0.268); E('l8', 'screens[9].explain.text', 0.0043)
two('digits per step', r(math.log(10) / math.log(4), 2), 1.66)
true('(2 + a_n) >= 3 since a_n >= 1', min(seq) >= 1)
true('L^2 - L - 2 roots 2 and -1', 2 * 2 - 2 - 2 == 0 and 1 + 1 - 2 == 0)
x = [F(2)]
for _ in range(3):
    x.append((x[-1] + 2 / x[-1]) / 2)
true('Babylonian 2, 3/2, 17/12, 577/408', x == [2, F(3, 2), F(17, 12), F(577, 408)])
true('x_n^2 - 2 = 2, 1/4, 1/144, 1/166464', [v * v - 2 for v in x] == [2, F(1, 4), F(1, 144), F(1, 166464)])
true('x_{n+1} - sqrt2 = (x_n - sqrt2)^2/(2x_n)', all(math.isclose((float(v) + 2 / float(v)) / 2 - 2 ** .5, (float(v) - 2 ** .5) ** 2 / (2 * float(v)), abs_tol=1e-15) for v in x))
for n, shown in [(1, 2), (2, 2.25), (3, 2.3704), (10, 2.5937), (100, 2.7048)]:
    two(f'(1 + 1/{n})^{n}', r((1 + 1 / n) ** n, 4), shown)
two('e', r(math.e, 4), 2.7183); true('(1+1/n)^n rises and stays below 3 to n = 2000', all((1 + 1 / n) ** n < (1 + 1 / (n + 1)) ** (n + 1) < 3 for n in range(1, 2000)))
true('doubling points 1..32', [p['y'] for p in pts(L8, 8)] == [2 ** k for k in range(6)])
def first_within(eps):
    a_, n = 1.0, 1
    while 2 - a_ >= eps:
        a_ = math.sqrt(2 + a_); n += 1
    return n
for e, n in [(0.1, 3), (0.01, 5), (0.001, 7), (1e-6, 12), (1, 2), (2, 1)]:
    two(f'first_within({e})', first_within(e), n)
two('iterate_sqrt(0, 3)', math.sqrt(2 + math.sqrt(2)), 1.8477590650225735); two('iterate_sqrt(3, 4)', math.sqrt(2 + math.sqrt(2 + math.sqrt(5))), 2.0144902648738445)
V = [F(90)]
for _ in range(20):
    V.append(F(8, 10) * V[-1] + 20)
true('EMA 90, 92, 93.6, 94.88', V[:4] == [90, 92, F(936, 10), F(9488, 100)])
true('gap 100 - V_n = 10 * 0.8^(n-1)', all(100 - V[k] == 10 * F(8, 10) ** k for k in range(20)))
two('first day within 0.50', first_n(lambda n: 100 - V[n - 1] < F(1, 2)), 15); E('l8', 'screens[10].widget.answer', 15)
two('0.8^13 to 4', r(0.8 ** 13, 4), 0.055); two('0.8^14 to 4', r(0.8 ** 14, 4), 0.044); two('day 14 gap to 2', r(10 * 0.8 ** 13, 2), 0.55)
two('exponent slip', first_n(lambda n: 10 * F(8, 10) ** n < F(1, 2)), 14); two('pound slip', first_n(lambda n: 100 - V[n - 1] < 1), 12)
true('EMA canvas points', all(abs(p['y'] - float(V[int(p['id'][1:]) - 1])) < 5e-6 for p in pts(L8, 10)))
h = [F(0)]
for _ in range(5):
    h.append(h[-1] / 2 + 3)
true('quiz recursion 0, 3, 4.5, 5.25', h[:4] == [0, 3, F(9, 2), F(21, 4)]); true('gaps to 6 halve', [6 - v for v in h[:4]] == [6, 3, F(3, 2), F(3, 4)])
E('l8', 'quiz[2].widget.answer', 6)

# ---------------- l9 subsequences ----------------
L9 = 'l9-subsequences'
s9 = lambda n: (-1) ** n * (1 + F(1, n))
for n, shown in [(1, -2), (2, 1.5), (3, -1.3333), (4, 1.25), (5, -1.2), (6, 1.1667)]:
    two(f'a_{n}', r(s9(n), 4), shown)
true('l9 screen 0 points', all(abs(p['y'] - float(s9(int(p['id'][1:])))) < 5e-6 for p in pts(L9, 0)))
true('every |a_n| > 1', all(abs(s9(n)) > 1 for n in range(1, 500)))
true('even terms in (1, 1.5]; only a_2 in [1.5, 2]; only a_2, a_4 in [1.25, 1.5]', all(1 < s9(n) <= F(3, 2) for n in range(2, 400, 2)) and [n for n in range(2, 400, 2) if s9(n) >= F(3, 2)] == [2] and [n for n in range(2, 400, 2) if s9(n) >= F(5, 4)] == [2, 4])
two('length after 10 halvings of [-2, 2]', F(4, 2 ** 10), 0.00390625); E('l9', 'screens[6].widget.answer', 0.00390625)
two('nine halvings', F(4, 2 ** 9), 0.0078125); two('from length 1', F(1, 2 ** 10), 0.0009765625)
true('caption lengths 4, 2, 1, 0.5, 0.25', [F(4, 2 ** k) for k in range(5)] == [4, 2, 1, F(1, 2), F(1, 4)])
two('quiz odd limit', r((-1) ** 100001 + 1 / 100001, 4), -1)
true('n_k = k^2 >= k and 2^k rises', all(k * k >= k and 2 ** (k + 1) > 2 ** k for k in range(1, 100)))
true('a_n = n(1 + (-1)^n): 0, 4, 0, 8, 0, 12', [n * (1 + (-1) ** n) for n in range(1, 7)] == [0, 4, 0, 8, 0, 12])

# ---------------- l10 Cauchy ----------------
L10 = 'l10-cauchy'
S = [F(0)]
for k in range(1, 3001):
    S.append(S[-1] + F(1, k * k))
two('S_40', r(S[40], 6), 1.620244)
true('l10 screen 0 points are S_n', all(abs(p['y'] - float(S[int(p['id'][1:])])) < 5e-6 for p in pts(L10, 0)))
true('S_m - S_n < 1/n - 1/m for sampled m > n', all(S[m] - S[n] < F(1, n) - F(1, m) for n in (1, 2, 5, 40, 100) for m in (n + 1, 2 * n, 3000) if m > n))
two('S_200 - S_100', r(S[200] - S[100], 6), 0.004963); two('S_3000 - S_100', r(S[3000] - S[100], 6), 0.009617)
two('bound at (200, 100)', F(1, 100) - F(1, 200), 0.005); two('bound at (3000, 100)', r(F(1, 100) - F(1, 3000), 6), 0.009667)
for v in ('0.004963', '0.009617', '0.005', '0.009667'):
    E('l10', 'screens[3].canvas.params.rows', v)
two('N from the bound at 0.01', math.ceil(1 / F(1, 100)), 100); E('l10', 'screens[3].widget.answer', 100)
two('sq slip at 0.01', math.ceil(math.sqrt(1 / 0.01)), 10)
true('1/2^k < 1/k^2 fails at k = 2, 4 and every k >= 5', [k for k in range(2, 40) if not F(1, k * k) < F(1, 2 ** k)] == [2, 4] + list(range(5, 40)))
Hg = lambda n: sum(F(1, k) for k in range(n + 1, 2 * n + 1))
for n, shown in [(1, 0.5), (2, 0.583333), (3, 0.616667), (10, 0.6688)]:
    two(f'H_2n - H_n at {n}', r(Hg(n), 6 if n < 10 else 4), shown)
true('H_4 - H_2 = 7/12, H_6 - H_3 = 37/60', Hg(2) == F(7, 12) and Hg(3) == F(37, 60))
true('H_20 - H_10 = 155685007/232792560', Hg(10) == F(155685007, 232792560))
true('every gap up to 59 is at least 1/2', all(Hg(n) >= F(1, 2) for n in range(1, 60)))
H = [0.0]
for k in range(1, 41):
    H.append(H[-1] + 1 / k)
true('l10 screen 9 points are H_n', all(abs(p['y'] - H[int(p['id'][1:])]) < 5e-6 for p in pts(L10, 9)))
two('x_n at 10^8', r(math.log(1e8) + 0.5772, 0), 19); two('ln 2', r(math.log(2), 2), 0.69)
two('quiz N at 0.002', math.ceil(1 / F(2, 1000)), 500); E('l10', 'quiz[1].widget.answer', 500); two('quiz sq slip', math.ceil(math.sqrt(500)), 23)
true('truncations of sqrt2 past the Nth differ by less than 10^(1-N)', all(abs(math.floor(2 ** .5 * 10 ** (m - 1)) / 10 ** (m - 1) - math.floor(2 ** .5 * 10 ** (n - 1)) / 10 ** (n - 1)) < 10 ** (1 - N) for N in range(1, 8) for m in range(N, 10) for n in range(N, 10)))
true('sqrt(4n) - sqrt(n) = sqrt(n) >= 1', all(math.isclose(math.sqrt(4 * n) - math.sqrt(n), math.sqrt(n)) for n in range(1, 100)))
# finding 22: the code exercise needs a test that a float version fails
true('a float ceil gets 1/49 wrong (50)', math.ceil(1 / float(F(1, 49))) == 50 and math.ceil(1 / F(1, 49)) == 49)
true('code tests include Fraction(1, 49) -> 49', any(t['call'] == 'cauchy_n(Fraction(1, 49))' and t['expect'] == '49' for t in lv.files[L10]['screens'][10]['widget']['tests']))
E('l10', 'screens[10].explain.text', 49)

# ---------------- review-2 ----------------
ra = lambda n: F(4 * n - 1, 2 * n + 1)
true('|a_n - 2| = 3/(2n+1)', all(abs(ra(n) - 2) == F(3, 2 * n + 1) for n in range(1, 300)))
two('review N at 0.01', tail_start(lambda n: abs(ra(n) - 2), F(1, 100)), 150); E('review', 'items[0].widget.answer', 150)
two('3/301 to 5', r(F(3, 301), 5), 0.00997); two('3/299 to 5', r(F(3, 299), 5), 0.01003)
rs = [2.0]
for _ in range(5):
    rs.append(math.sqrt(6 + rs[-1]))
for k, shown in enumerate([2, 2.8284, 2.9713, 2.9952, 2.9992]):
    two(f'sqrt(6 + a) term {k + 1}', r(rs[k], 4), shown)
true('L^2 - L - 6 roots 3, -2', 9 - 3 - 6 == 0 and 4 + 2 - 6 == 0)
true('cos(n pi/2) starts 0, -1, 0, 1', [round(math.cos(n * math.pi / 2)) for n in range(1, 9)] == [0, -1, 0, 1, 0, -1, 0, 1])
two('n/(n+1): N at 0.1', tail_start(lambda n: F(1, n + 1), F(1, 10)), 10); two('1/11 to 3', r(F(1, 11), 3), 0.091)
# finding 28 (freshness): items[6] becomes a three-term sum law with eps/3
idx = [tail_start(lambda n, c=c: F(c, n), F(1, 10)) for c in (1, 2, 3)]
true('three first indices 11, 21, 31', idx == [11, 21, 31]); two('direct: 2/n < 0.3', tail_start(lambda n: F(2, n), F(3, 10)), 7)
two('halves slip: 3/n < 0.15', tail_start(lambda n: F(3, n), F(15, 100)), 21)
E('review', 'items[6].widget.answer', 31)
y = [F(1)]
for _ in range(4):
    y.append((y[-1] + 8) / 3)
true('(a + 8)/3: 1, 3, 11/3, 35/9', y[:4] == [1, 3, F(11, 3), F(35, 9)]); true('gaps to 4: 3, 1, 1/3, 1/9', [4 - v for v in y[:4]] == [3, 1, F(1, 3), F(1, 9)])
two('eight-thirds slip', F(8, 3), 2.6667, tol=1e-4)

# ---------------- homework-2 ----------------
hq = lambda n: F(3 * n * n + 1, n * n + 2)
true('|a_n - 3| = 5/(n^2+2)', all(abs(hq(n) - 3) == F(5, n * n + 2) for n in range(1, 300)))
two('homework N at 0.01', tail_start(lambda n: abs(hq(n) - 3), F(1, 100)), 23); E('homework', 'items[1].widget.answer', 23)
two('threshold 498', 5 / F(1, 100) - 2, 498); two('5/531 to 4', r(F(5, 531), 4), 0.0094); two('5/486 to 4', r(F(5, 486), 4), 0.0103)
two('sqrt 498 to 1', r(math.sqrt(498), 1), 22.3); two('sqrt 500 to 2', r(math.sqrt(500), 2), 22.36)
pa = lambda n: 2 + F(1, n); pb = lambda n: 5 - F(2, n)
true('|a_n| <= 3', all(abs(pa(n)) <= 3 for n in range(1, 1000)))
Nb = tail_start(lambda n: abs(pb(n) - 5), F(1, 100) / 6, 5000); Na = tail_start(lambda n: abs(pa(n) - 2), F(1, 100) / 12, 5000)
two('product N b', Nb, 1201); two('product N a', Na, 1201); E('homework', 'items[2].widget.answer', 1201)
two('a-only slip', tail_start(lambda n: F(1, n), F(1, 1000), 5000), 1001)
two('direct first index', tail_start(lambda n: abs(pa(n) * pb(n) - 10), F(1, 100), 5000), 98)
true('|a_n b_n - 10| = 1/n - 2/n^2 for n >= 2', all(abs(pa(n) * pb(n) - 10) == F(1, n) - F(2, n * n) for n in range(2, 500)))
true('squares: 2, 4, 16, 256, 65536', [2 ** (2 ** (n - 1)) for n in range(1, 6)] == [2, 4, 16, 256, 65536])
def fn(eps):
    n = 1
    while F(5, n * n + 2) >= F(eps):
        n += 1
    return n
for e, n in [(F(1, 100), 23), (F(1, 10), 7), (1, 2), (2, 1), (F(5, 27), 6), (F(1, 1000), 71)]:
    two(f'first_n({e})', fn(e), n)
true('70^2 = 4900 < 4998 < 71^2', 70 ** 2 < 4998 < 71 ** 2)
true('homework rubric totals 10', sum(x['points'] for x in lv.files['homework-2']['items'][7]['rubric']) == 10)

# fix pass: numbers and structure written by the fixes
true('l7 first version of the product proof: 401 and 801 from |b|, 601 from |b| + 1', tail_start(lambda n: F(1, n), F(1, 400)) == 401 and tail_start(lambda n: F(1, n), F(1, 800)) == 801 and tail_start(lambda n: F(1, n), F(1, 600)) == 601)
true('l7 screens[5] same group is c2, c3', lv.files[L7]['screens'][5]['widget'].get('same') == [['c2', 'c3']])
true('l10 screens[7] same group is k1, k2', lv.files[L10]['screens'][7]['widget'].get('same') == [['k1', 'k2']])
true('homework-2 items[4] same group is q2, q3', lv.files['homework-2']['items'][4]['widget'].get('same') == [['q2', 'q3']])
true('Cauchy sum: x = y = 0.1 gives sum 0.2 > product 0.01, so d2 is false', abs(0.1 + 0.1) > abs(0.1 * 0.1))
bq = lambda n: F(n, n + 1)
true('review-2 items[1]: line 3 gives 1/n, line 4 claims 1/(n+1), for b = 1', all(abs(1 / bq(n) - 1) == F(1, n) and F(1, n) > F(1, n + 1) for n in range(1, 300)))
E('review', 'items[1].explain.text', '\\tfrac{1}{n+1}')
true('review-2 items[6]: eps/3 = 0.1', F(3, 10) / 3 == F(1, 10))

lv.check_wrongs()
lv.report()
