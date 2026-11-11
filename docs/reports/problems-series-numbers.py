"""Recompute every number in app/content/courses/series/problems-<n>.json twice.

Method 1 is exact: fractions, binomial coefficients from math.comb and closed forms (the nth-term,
sum and sum-to-infinity formulas). Method 2 is independent: the story walked term by term (row by
row, swing by swing, tablet by tablet, day by day, payment by payment), counts by brute enumeration
(itertools.combinations over toppings, subsets for row sums), and a full expansion of the bracket by
repeated multiplication of coefficient lists. For each numeric part the script checks that the two
methods agree; that the key lies inside its own band; that the value at the asked rounding, the
figure the feedback prints last and every rounded route the explanation prints are accepted; that
every `wrong` value is the value its named slip gives (rebuilt here), has a byKey line, lies outside
the key's band, does not reach the key and does not overlap another `wrong`. Expression parts are
compared with sympy at sample points: the answer and every accept form equal the key, every wrong
form differs. Choice parts check the keyed option and the arithmetic behind each `why`. Exit 0 when
all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-series-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import comb
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'series')
fails, checks = [], 0


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def close(a, b, eps=1e-9):
    return abs(float(a) - float(b)) <= eps * max(1, abs(float(b)))


def load(n):
    return {it['id']: it for it in json.load(open(os.path.join(COURSE, f'problems-{n}.json')))['items']}


def within(v, key, tol):
    return abs(v - key) <= tol + 1e-12


n_sym = sp.Symbol('n')
x_sym = sp.Symbol('x')


def tex(s):
    """Small LaTeX-to-sympy reader for the forms in these sets."""
    s = s.replace('\\left', '').replace('\\right', '').replace(' ', '')
    while '\\frac' in s:
        i = s.index('\\frac')
        def grab(j):
            depth, k = 0, j
            while True:
                if s[k] == '{':
                    depth += 1
                elif s[k] == '}':
                    depth -= 1
                    if depth == 0:
                        return s[j + 1:k], k + 1
                k += 1
        a, j = grab(i + 5)
        b, j = grab(j)
        s = s[:i] + f'(({a})/({b}))' + s[j:]
    s = s.replace('\\cdot', '*').replace('\\times', '*').replace('{', '(').replace('}', ')').replace('^', '**')
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
    return parse_expr(s, local_dict={'n': n_sym, 'x': x_sym},
                      transformations=standard_transformations + (implicit_multiplication_application,))


def same(e1, e2):
    for v in (1, 2, 3, 5, 7, 0.5, 2.5):
        a = complex(e1.subs({n_sym: v, x_sym: v}).evalf())
        b = complex(e2.subs({n_sym: v, x_sym: v}).evalf())
        if abs(a - b) > 1e-9 * max(1, abs(b)):
            return False
    return True


def printed_last(text):
    t = re.sub(r'\\tfrac\{[^}]*\}\{[^}]*\}|\\dfrac\{[^}]*\}\{[^}]*\}', '', text)
    t = t.replace('{,}', '').replace(',', '')
    hits = re.findall(r'(-?\d+(?:\.\d+)?)', t)
    return float(hits[-1]) if hits else None


def check_numeric(where, part, key1, key2, typed_ok, slips, typed_bad=()):
    w = part['widget']
    ok(close(key1, key2), f'{where}: two methods differ {key1} {key2}')
    ok(within(float(key1), w['answer'], w['tol']['abs']), f'{where}: key {float(key1)} outside band of {w["answer"]}')
    for t in typed_ok:
        ok(within(t, w['answer'], w['tol']['abs']), f'{where}: sensible entry {t} refused')
    for t in typed_bad:
        ok(not within(t, w['answer'], w['tol']['abs']), f'{where}: entry {t} accepted')
    pl = printed_last(part['feedback']['correct'])
    ok(pl is not None and within(pl, w['answer'], w['tol']['abs']), f'{where}: printed last {pl} refused')
    lead = re.match(r'\s*(-?[\d.]+)', w.get('accept', ''))
    ok(lead and within(float(lead.group(1)), w['answer'], w['tol']['abs']), f'{where}: accept figure refused')
    ok('Any form' not in w.get('accept', ''), f'{where}: Any form line')
    ids = {x['id']: x for x in w['wrong']}
    ok(set(ids) == set(slips), f'{where}: wrong ids {sorted(ids)} vs slips {sorted(slips)}')
    for i, val in slips.items():
        x = ids.get(i)
        if not x:
            continue
        ok(within(float(val), x['value'], x['tol']['abs'] + 1e-9), f'{where}: wrong {i} {x["value"]} is not slip value {float(val)}')
        ok(not within(x['value'], w['answer'], w['tol']['abs']), f'{where}: wrong {i} inside answer band')
        ok(abs(x['value'] - w['answer']) > x['tol']['abs'], f'{where}: wrong {i} band reaches key')
        ok(abs(x['value'] - w['answer']) > x['tol']['abs'] + w['tol']['abs'] or True, '')
        ok(i in part['feedback'].get('byKey', {}), f'{where}: no byKey line for {i}')
        for j, y in ids.items():
            if j != i:
                ok(abs(x['value'] - y['value']) > x['tol']['abs'] + y['tol']['abs'], f'{where}: wrong {i} overlaps {j}')
        # the answer band and a wrong band must not overlap either
        ok(abs(x['value'] - w['answer']) > x['tol']['abs'] + w['tol']['abs'], f'{where}: wrong {i} band overlaps answer band')


def check_expr(where, part, key, slips):
    w = part['widget']
    ok(same(tex(w['answer']), key), f'{where}: answer {w["answer"]} not the key {key}')
    for a in w.get('accept', []):
        ok(same(tex(a), key), f'{where}: accept {a} not equal to key')
    ids = {x['id']: x['tex'] for x in w['wrong']}
    ok(set(ids) == set(slips), f'{where}: wrong ids {sorted(ids)} vs {sorted(slips)}')
    for i, e in slips.items():
        if i in ids:
            ok(same(tex(ids[i]), e), f'{where}: wrong {i} {ids[i]} is not slip {e}')
            ok(not same(tex(ids[i]), key), f'{where}: wrong {i} equals key')
            ok(i in part['feedback'].get('byKey', {}), f'{where}: no byKey line for {i}')
    ok('\\ln' not in w['answer'] and 'ln(' not in w['answer'], f'{where}: plain function name')


def check_choice(where, part, key_id):
    opts = part['widget']['options']
    ok([o['id'] for o in opts if o.get('correct')] == [key_id], f'{where}: keyed option')
    ok(all(o.get('why') for o in opts if not o.get('correct')), f'{where}: missing why')


def terms_arith(a, d, k):
    out, t = [], F(a)
    for _ in range(k):
        out.append(t)
        t += d
    return out


def terms_geom(a, r, k):
    out, t = [], F(a)
    for _ in range(k):
        out.append(t)
        t *= F(r)
    return out


# ================================================================ level 1
P = load(1)

it = P['p-theatre-rows']['parts']
rows = terms_arith(18, 3, 40)
ok(rows[:4] == [18, 21, 24, 27], 'theatre prose rows')
check_numeric('1 theatre p1', it[0], rows[6], 18 + 6 * 3, [36], {'seven-steps': 18 + 7 * 3, 'next-row': rows[4]})
check_expr('1 theatre p2', it[1], 3 * n_sym + 15, {'n-steps': 18 + 3 * n_sym, 'swapped': 18 * n_sym + 3, 'step-only': 3 * n_sym})
ok(all(3 * k + 15 == rows[k - 1] for k in range(1, 41)), 'theatre rule matches every row')
check_numeric('1 theatre p3', it[2], 3 * 25 + 15, rows[24], [90], {'n-steps': 18 + 3 * 25, 'step-only': 3 * 25})
half = F(rows[24], 2)
first = next(k for k in range(1, 26) if rows[k - 1] >= half)
check_numeric('1 theatre p4', it[3], first, -(-(half - 15) // 3), [10],
              {'halfway': F(25, 2), 'divided': half / 3, 'steps': (half - 18) / 3})
ok(rows[8] == 42 and rows[9] == 45 and rows[11] == 51 and rows[12] == 54, 'theatre p4 printed rows 9, 10, 12, 13')
ok(within(12, 12.5, 0.5) and within(13, 12.5, 0.5) and not within(10, 12.5, 0.5), 'halfway band takes 12 and 13 only')

it = P['p-pendulum-swings']['parts']
sw = terms_geom(80, F(9, 10), 12)
ok(sw[:3] == [80, 72, F(324, 5)], 'pendulum prose')
check_choice('1 pendulum p1', it[0], 'ratio')
ok(F(72, 80) == F(324, 5) / 72 == F(9, 10), 'pendulum both ratios 0.9')
ok(72 - 8 == 64 and 80 - F(36, 5) == F(364, 5) and 80 * F(8, 10) == 64, 'pendulum why arithmetic')
check_expr('1 pendulum p2', it[1], 80 * sp.Rational(9, 10) ** (n_sym - 1),
           {'power-n': 80 * sp.Rational(9, 10) ** n_sym, 'bracket': 72 ** (n_sym - 1), 'arith': 88 - 8 * n_sym})
check_numeric('1 pendulum p3', it[2], sw[5], 80 * 0.9 ** 5, [47.2, 47.24],
              {'power-n': sw[6], 'swing-five': sw[4], 'arith': 80 - 8 * 5})
ok(float(sw[5]) == 47.2392, 'pendulum swing 6 exact 47.2392')
first = next(k for k in range(1, 13) if sw[k - 1] < 40)
run = 47.2
k2 = 6
while run >= 40:
    run *= 0.9
    k2 += 1
check_numeric('1 pendulum p4', it[3], first, k2, [8], {'seven': 7, 'six': 6})
ok(next(k for k in range(1, 20) if 88 - 8 * k < 40) == 7, 'pendulum arith slip gives swing 7')
ok(round(47.2 * 0.9, 1) == 42.5 and round(42.5 * 0.9, 1) in (38.2, 38.3), 'pendulum printed 42.5 and 38.3')

it = P['p-daily-tablet']['parts']
def doses(keep, k):
    u, out = F(240), []
    for _ in range(k):
        out.append(u)
        u = F(keep) * u + 240
    return out
u = doses(F(2, 5), 12)
ok(u[1] == 336 and u[2] == F(1872, 5), 'tablet u2 u3')
check_numeric('1 tablet p1', it[0], u[2], 0.4 * (0.4 * 240 + 240) + 240, [374.4],
              {'no-clearing': 3 * 240, 'tablet-two': u[1], 'kept-sixty': doses(F(3, 5), 3)[2]})
L = F(240) / (1 - F(2, 5))
lim = 0.0
for _ in range(200):
    lim = 0.4 * lim + 240
check_numeric('1 tablet p2', it[1], L, lim, [400], {'kept-sixty': F(240) / (1 - F(3, 5)), 'sign': F(240) / F(7, 5)})
ok(within(171, 171.43, 0.5), 'tablet sign slip rounded is caught')
gaps = [L - t for t in u]
ok(gaps[0] == 160 and gaps[2] == F(128, 5) and 400 - F(1872, 5) == F(128, 5) == F(256, 10), 'tablet p3 question: g1 = 160 and g3 = 25.6 from u3 = 374.4')
ok(gaps[0] == 160 and all(gaps[k + 1] == F(2, 5) * gaps[k] for k in range(11)), 'tablet gaps geometric 0.4')
check_expr('1 tablet p3', it[2], 160 * sp.Rational(2, 5) ** (n_sym - 1),
           {'power-n': 160 * sp.Rational(2, 5) ** n_sym, 'cleared': 160 * sp.Rational(3, 5) ** (n_sym - 1),
            'level': 400 * sp.Rational(2, 5) ** (n_sym - 1)})
first = next(k for k in range(1, 12) if u[k - 1] > 395)
first2 = next(k for k in range(1, 12) if 160 * 0.4 ** (k - 1) < 5)
v60 = doses(F(3, 5), 6)
check_numeric('1 tablet p4', it[3], first, first2, [5],
              {'power-n': next(k for k in range(1, 12) if 160 * 0.4 ** k < 5),
               'kept-sixty': next(k for k in range(1, 7) if v60[k - 1] > 395)})
ok(u[4] == F(400) - F(4096, 1000) and u[3] == F(38976, 100), 'tablet u4 389.76 and u5 395.904')

it = P['p-shop-orders']['parts']
d = F(216 - 96, 2)
check_numeric('1 shop p1', it[0], d, (216 - 96) / 2, [60], {'no-halve': 216 - 96, 'three-steps': F(120, 3)})
r = sp.sqrt(sp.Rational(216, 96))
check_numeric('1 shop p2', it[1], r, 2.25 ** 0.5, [1.5, 1.50], {'no-halve' if False else 'no-root': F(216, 96), 'halved': F(216, 96) / 2,
              'inverted': sp.sqrt(sp.Rational(96, 216))})
check_choice('1 shop p3', it[2], 'geom')
ok(96 + 60 == 156 and 96 * F(3, 2) == 144 and 144 * F(3, 2) == 216, 'shop month 3 test')
check_expr('1 shop p4', it[3], 64 * sp.Rational(3, 2) ** (n_sym - 1),
           {'month-two-start': 96 * sp.Rational(3, 2) ** (n_sym - 1), 'arith': 60 * n_sym - 24})
ok(same(64 * sp.Rational(3, 2) ** n_sym, 96 * sp.Rational(3, 2) ** (n_sym - 1)), 'shop p4: the removed power-n entry was equal to month-two-start')
o = terms_geom(64, F(3, 2), 20)
ok(o[1] == 96 and o[3] == 216 and o[6] == 729 and o[7] == F(2187, 2), 'shop months 2, 4, 7, 8')
first = next(k for k in range(1, 21) if o[k - 1] > 1000)
m, k2 = 216.0, 4
while m <= 1000:
    m *= 1.5
    k2 += 1
check_numeric('1 shop p5', it[4], first, k2, [8],
              {'power-n': next(k for k in range(1, 21) if 64 * 1.5 ** k > 1000),
               'arith': next(k for k in range(1, 40) if 36 + 60 * (k - 1) > 1000)})

# ================================================================ level 2
P = load(2)

it = P['p-tin-display']['parts']
rows = terms_arith(8, 5, 10)
ok(rows[:3] == [8, 13, 18], 'tins prose rows')
check_numeric('2 tins p1', it[0], rows[9], 8 + 9 * 5, [53], {'n-steps': 8 + 10 * 5, 'step-only': 10 * 5})
check_numeric('2 tins p2', it[1], sum(rows), F(10, 2) * (8 + 53), [305],
              {'no-halve': 10 * 61, 'last-only': F(10, 2) * 53, 'n-steps': F(10, 2) * (16 + 10 * 5)})
ok(all(5 * k + 3 == rows[k - 1] for k in range(1, 11)), 'tins row k is 5k + 3')
check_numeric('2 tins p3', it[2], 10 - 4 + 1, len(range(4, 11)), [7], {'subtract': 10 - 4, 'top': 10})
stand = sum(5 * k + 3 for k in range(4, 11))
check_numeric('2 tins p4', it[3], stand, F(7, 2) * (23 + 53), [266],
              {'six-rows': F(6, 2) * (23 + 53), 'four-left': sum(rows) - sum(rows[:4]), 'full': sum(rows)})
ok(sum(rows[:3]) == 39 and sum(rows[:4]) == 62 and 305 - 39 == stand and rows[3] == 23, 'tins check 305 - 39')

it = P['p-app-users']['parts']
day = terms_geom(4, 3, 15)
check_numeric('2 app p1', it[0], day[5], 4 * 3 ** 5, [972], {'power-n': 4 * 3 ** 6, 'day-five': day[4]})
S6 = sum(day[:6])
check_numeric('2 app p2', it[1], S6, (3 * 972 - 4) / 2, [1456], {'no-halve': 3 * 972 - 4, 'no-first': F(3 * 972, 2)})
check_expr('2 app p3', it[2], 2 * 3 ** n_sym - 2,
           {'no-divide': 4 * 3 ** n_sym - 4, 'power-n-1': 2 * 3 ** (n_sym - 1) - 2, 'sign': 2 - 2 * 3 ** n_sym})
ok(all(2 * (3 ** k - 1) == sum(day[:k]) for k in range(1, 15)), 'app closed form matches running totals')
first = next(k for k in range(1, 15) if sum(day[:k]) > 100000)
tot, k2 = 0, 0
while tot <= 100000:
    k2 += 1
    tot += 4 * 3 ** (k2 - 1)
check_numeric('2 app p4', it[3], first, k2, [10],
              {'one-day': next(k for k in range(1, 15) if day[k - 1] > 100000), 'nine': first - 1})
ok(sum(day[:9]) == 39364 and sum(day[:10]) == 118096, 'app S9 and S10')

it = P['p-bouncing-ball']['parts']
rises = terms_geom(3, F(3, 5), 40)
S9 = sum(rises[:9])
check_numeric('2 ball p1', it[0], S9, 3 * (1 - 0.6 ** 9) / 0.4, [7.42, 7.424],
              {'forever': F(3) / F(2, 5), 'ten': sum(rises[:10]), 'eight': sum(rises[:8])})
ok(within(7.45, float(sum(rises[:10])), 0.005) and within(7.37, float(sum(rises[:8])), 0.005), 'ball 10 and 8 rises at 2 dp caught')
ok(abs(7.5 * (1 - 0.0101) - 7.42) < 0.005, 'ball printed 7.5 x 0.9899')
d10 = 5 + 2 * S9
walk, h = 5.0, 5.0
for _ in range(9):
    h *= 0.6
    walk += 2 * h
check_numeric('2 ball p2', it[1], d10, walk, [19.84, 19.85, 5 + 2 * 7.42],
              {'once': 5 + F(742, 100), 'no-drop': 2 * S9, 'double-drop': 10 + 2 * S9})
ok(within(14.84, float(2 * S9), 0.01) and within(24.84, float(10 + 2 * S9), 0.01), 'ball slips from 7.42 caught')
Sinf = F(3) / (1 - F(3, 5))
part = 0.0
for k in range(400):
    part += 3 * 0.6 ** k
check_numeric('2 ball p3', it[2], Sinf, part, [7.5], {'whole': F(5) / F(2, 5), 'divide-r': F(3) / F(3, 5), 'second': F(9, 5) / F(2, 5)})
walk = 5.0
h = 5.0
for _ in range(400):
    h *= 0.6
    walk += 2 * h
check_numeric('2 ball p4', it[3], 5 + 2 * Sinf, walk, [20], {'once': 5 + Sinf, 'no-drop': 2 * Sinf, 'double-drop': 10 + 2 * Sinf})

it = P['p-two-repayment-plans']['parts']
A = terms_arith(50, 10, 40)
check_expr('2 plans p1', it[0], 5 * n_sym ** 2 + 45 * n_sym,
           {'last-term': 5 * n_sym ** 2 + 50 * n_sym, 'no-halve': 10 * n_sym ** 2 + 90 * n_sym, 'one-month': 10 * n_sym + 40})
ok(all(5 * k * k + 45 * k == sum(A[:k]) for k in range(1, 40)), 'plan A closed form matches running totals')
first = next(k for k in range(1, 40) if sum(A[:k]) >= 3000)
tot, k2 = 0, 0
while tot < 3000:
    k2 += 1
    tot += 50 + 10 * (k2 - 1)
check_numeric('2 plans p2', it[1], first, k2, [21], {'twenty': 20, 'flat': F(3000, 50)})
ok(sum(A[:20]) == 2900 and sum(A[:21]) == 3150, 'plan A S20 and S21')
B = terms_geom(200, F(9, 10), 21)
Binf = F(200) / (1 - F(9, 10))
part = 0.0
for k in range(2000):
    part += 200 * 0.9 ** k
check_numeric('2 plans p3', it[2], Binf, part, [2000], {'ar': F(180) / F(1, 10), 'divide-r': F(200) / F(9, 10), 'plus': F(200) / F(19, 10)})
ok(within(222, 222.22, 0.5) and within(105, 105.26, 0.5), 'plans p3 slips rounded caught')
B21 = sum(B)
check_numeric('2 plans p4', it[3], B21, 2000 * (1 - 0.9 ** 21), [1781, 1782, 1781.16, 2000 * (1 - 0.1094), 2000 * (1 - 0.109)],
              {'twenty': sum(B[:20]), 'forever': Binf, 'left': Binf - B21})
ok(round(0.9 ** 21, 4) == 0.1094, 'plans 0.9^21 to 4 dp')
check_numeric('2 plans p5', it[4], 3000 - B21, 3000 - 2000 * (1 - 0.9 ** 21), [1219, 1218, 3000 - 1781],
              {'forever': 3000 - Binf, 'twenty': 3000 - sum(B[:20]), 'paid': B21})

# ================================================================ level 3
P = load(3)

it = P['p-pizza-toppings']['parts']
tops = range(11)
c4 = sum(1 for _ in itertools.combinations(tops, 4))
check_numeric('3 pizza p1', it[0], comb(11, 4), c4, [330], {'ordered': 11 * 10 * 9 * 8, 'times': 11 * 4, 'three-orders': 11 * 10 * 9 * 8 // 6})
c47 = sum(1 for k in (4, 7) for _ in itertools.combinations(tops, k))
check_numeric('3 pizza p2', it[1], comb(11, 4) + comb(11, 7), c47, [660], {'one-size': comb(11, 4)})
ok(comb(11, 7) == comb(11, 4) == 330, 'pizza symmetry 330 each')
c12 = sum(1 for _ in itertools.combinations(range(12), 4))
with_ham = sum(1 for s_ in itertools.combinations(range(12), 4) if 11 in s_)
ok(with_ham == comb(11, 3) == 165, 'pizza with ham 165')
check_numeric('3 pizza p3', it[2], comb(11, 4) + comb(11, 3), c12, [495], {'one-more': 330 + 11, 'doubled': 2 * 330, 'ordered': 12 * 11 * 10 * 9})
allp = sum(1 for k in range(13) for _ in itertools.combinations(range(12), k))
row12 = [comb(12, k) for k in range(13)]
ok(row12[:5] == [1, 12, 66, 220, 495], 'pizza row 12 begins 1, 12, 66, 220, 495')
check_numeric('3 pizza p4', it[3], sum(row12), allp, [4096], {'no-plain': allp - 1, 'row-eleven': 2 ** 11})

def expand(a, b, n):
    """Coefficients of (a + b x)^n by repeated multiplication."""
    c = [F(1)]
    for _ in range(n):
        nc = [F(0)] * (len(c) + 1)
        for i, v in enumerate(c):
            nc[i] += v * a
            nc[i + 1] += v * b
        c = nc
    return c

it = P['p-bracket-estimate']['parts']
c = expand(1, -3, 7)
check_numeric('3 bracket p1', it[0], comb(7, 2) * (-3) ** 2, c[2], [189], {'not-squared': 21 * 3, 'sign': -189, 'no-count': 9})
check_expr('3 bracket p2', it[1], 1 - 21 * x_sym + 189 * x_sym ** 2,
           {'sign': 1 + 21 * x_sym + 189 * x_sym ** 2, 'square-sign': 1 - 21 * x_sym - 189 * x_sym ** 2, 'no-count': 1 - 3 * x_sym + 9 * x_sym ** 2})
ok(c[0] == 1 and c[1] == -21, 'bracket first two coefficients')
x = F(1, 100)
est = c[0] + c[1] * x + c[2] * x ** 2
check_numeric('3 bracket p3', it[2], est, 1 - 0.21 + 0.0189, [0.8089],
              {'linear': 1 - 21 * x, 'square-sign': 1 - 21 * x - 189 * x ** 2, 'x-three': 1 - 21 * F(3, 100) + 189 * F(3, 100) ** 2,
               'calculator': round(0.97 ** 7, 4)}, typed_bad=[0.808, 0.80798, 0.809])
ok(within(0.97 ** 7, 0.808, 0.00005), 'bracket calculator slip catches 0.80798')
check_numeric('3 bracket p4', it[3], comb(7, 3) * (-3) ** 3, c[3], [-945], {'sign': 945, 'not-cubed': -105, 'no-count': -27})
imp = est + c[3] * x ** 3
check_numeric('3 bracket p5', it[4], imp, 0.8089 - 0.000945, [0.80796, 0.80795],
              {'added': est - c[3] * x ** 3, 'square': est + c[3] * x ** 2, 'calculator': 0.97 ** 7},
              typed_bad=[0.80798, 0.8080])
ok(round(0.97 ** 7, 6) == 0.807983 and within(0.807983, 0.807983, 6e-6) and not within(0.97 ** 7, 0.807955, 6e-6), 'bracket p5 calculator value 0.807983 sits outside the key band')
ok(abs(float(imp) - 0.97 ** 7) < 3e-5, 'bracket improved estimate within 3e-5 of the true value')
ok(F(97, 100) ** 7 == sum(c[k] * x ** k for k in range(8)), 'bracket full expansion equals 0.97^7')

it = P['p-gym-membership']['parts']
g = F(1) + 12 * F(5, 1000) + comb(12, 2) * F(5, 1000) ** 2
cc = expand(1, F(5, 1000), 12)
check_numeric('3 gym p1', it[0], g, float(cc[0] + cc[1] + cc[2]), [1.06165],
              {'linear': F(106, 100), 'calculator': round(1.005 ** 12, 5), 'no-half': 1 + F(6, 100) + 132 * F(5, 1000) ** 2},
              typed_bad=[1.06168, 1.0617])
q = 1 / F(10617, 10000)
check_numeric('3 gym p2', it[1], round(float(q), 4), round(1 / 1.005 ** 12, 4), [0.9419, float(q), 1 / 1.005 ** 12, 1 / 1.06165],
              {'grown': F(10617, 10000), 'subtract': 1 - F(617, 10000), 'one-month': round(1 / 1.005, 3)})
pv_exact = sum(F(100) / F(1005, 1000) ** k for k in range(1, 13))
pv_formula = 100 / 0.005 * (1 - 1.005 ** -12)
check_numeric('3 gym p3', it[2], pv_exact, pv_formula, [1162, 1161, 20000 * (1 - 0.9419), 20000 * (1 - float(q)), 20000 * (1 - 1 / 1.06165)],
              {'undiscounted': 1200, 'no-one-minus': 20000 * F(9419, 10000), 'one-payment': 100 * F(9419, 10000)})
ok(20000 * F(581, 10000) == 1162, 'gym 20000 x 0.0581 = 1162')
check_numeric('3 gym p4', it[3], pv_exact - 1150, pv_formula - 1150, [12, 11, 1162 - 1150, 20000 * (1 - float(q)) - 1150],
              {'undiscounted': 1200 - 1150, 'sign': 1150 - pv_exact})

it = P['p-powers-of-eleven']['parts']
row4 = [comb(4, k) for k in range(5)]
ok(row4 == [1, 4, 6, 4, 1], 'eleven row 4')
v4 = sum(row4[k] * 10 ** (4 - k) for k in range(5))
check_numeric('3 eleven p1', it[0], v4, 11 ** 4, [14641], {'share': 10 ** 4 + 1, 'no-count': 11111})
row5 = [1] + [row4[k - 1] + row4[k] for k in range(1, 5)] + [1]
ok(row5 == [comb(5, k) for k in range(6)], 'eleven row 5 by neighbours')
v5 = sum(row5[k] * 10 ** (5 - k) for k in range(6))
check_numeric('3 eleven p2', it[1], v5, 14641 * 11, [161051],
              {'digits': int(''.join(str(t) for t in row5)), 'times-ten': 146410, 'share': 10 ** 5 + 1})
check_numeric('3 eleven p3', it[2], F(161051, 100000), 1.1 ** 5, [1.61051],
              {'shift': F(161051, 10000), 'too-far': F(161051, 1000000), 'linear': F(3, 2)})
short = F(161051, 100000) - (1 + 5 * F(1, 10))
check_numeric('3 eleven p4', it[3], short, 1.1 ** 5 - 1.5, [0.11051],
              {'three-term': F(161051, 100000) - (1 + F(1, 2) + 10 * F(1, 100)), 'dropped': comb(5, 2) * F(1, 100), 'sign': -short})

# ---------------------------------------------------------------- structure and form
for n in (1, 2, 3):
    doc = json.load(open(os.path.join(COURSE, f'problems-{n}.json')))
    ok(3 <= len(doc['items']) <= 5, f'set {n} item count')
    ok(any(i['difficulty'] == 5 for i in doc['items']), f'set {n} has a 5')
    parts = [p for i in doc['items'] for p in i['parts']]
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for p in parts)
    ok(3 * typed >= 2 * len(parts), f'set {n} typed share {typed}/{len(parts)}')
    for i in doc['items']:
        ok(3 <= len(i['parts']) <= 5, f'set {n} {i["id"]} parts')
        for k, p in enumerate(i['parts']):
            w = p['widget']
            if w['kind'] == 'numeric' and float(w['answer']) != int(w['answer']) or w['kind'] == 'numeric':
                ok(re.search(r'decimal|places?|whole number|nearest|fraction', p['question'], re.I) is not None,
                   f'set {n} {i["id"]} p{k + 1}: no stated form')
            ok(len(re.findall(r'[.?](?:\s|$)', p['explain']['text'])) <= 3, f'set {n} {i["id"]} p{k + 1}: explain over 3 sentences')
            ok('!' not in re.sub(r'\$[^$]*\$', '', json.dumps(p)), f'set {n} {i["id"]} p{k + 1}: exclamation outside maths')

print(f'{checks} checks, {len(fails)} failures')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
