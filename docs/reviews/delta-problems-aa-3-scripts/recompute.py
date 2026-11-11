"""Delta read of fix passes 0.3 b and 0.3 c: every changed answer, band and wrong value recomputed twice.

Route 1 is exact (fractions, sympy, integer arithmetic); route 2 is a different numeric one (direct summation or
enumeration for series, bisection or month-by-month stepping for logs, coordinates and math.* for trig).
For each part: the key equals both routes; each wrong value equals the slip its feedback line names; the band
takes the printed value and the sensible roundings in the stated form and refuses the neighbours and every wrong
value; a typed slip lands on its own entry (first match, as numeric.js does). Then, on every single-value numeric
part of the nine files: no wrong value in the answer band; bands that meet are listed (NOTE) when an earlier
narrow band sits inside a later wide one, which the widget resolves by first match, and fail otherwise.

Run from the repo root with the scratchpad venv python:  python docs/reviews/delta-problems-aa-3-scripts/recompute.py
"""
import itertools
import json
import math
from fractions import Fraction as F

import sympy as sp

ROOT = 'app/content/courses'
checks = fails = notes = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def note(msg):
    global notes
    notes += 1
    print('NOTE', msg)


def load(course, n):
    return json.load(open(f'{ROOT}/{course}/problems-{n}.json'))


def item(course, n, iid):
    return next(i for i in load(course, n)['items'] if i['id'] == iid)


def part(course, n, iid, k):
    return item(course, n, iid)['parts'][k - 1]


def within(v, a, tol):
    return abs(v - a) <= ((tol or {}).get('abs', 0) or 0) + 1e-9


def grade(w, text):
    """numeric.js: True, a wrong id, or None."""
    t = str(text)
    v = float(F(t.replace('%', '')))
    if w.get('unit') == '%':
        v /= 100
    if within(v, float(w['answer']), w.get('tol')):
        return True
    for x in w.get('wrong', []):
        if within(v, float(x['value']), x.get('tol') or {'abs': 1e-9}):
            return x['id']
    return None


def num(course, n, iid, k, exact, second, takes=(), refuses=(), wrong=None, routes=None, places=6):
    """exact and second: the two routes. wrong: id -> the slip's value. routes: typed -> id."""
    p = part(course, n, iid, k)
    w = p['widget']
    where = f'{course} {n} {iid} p{k}'
    ok(w['kind'] == 'numeric' and 'answers' not in w, f'{where}: not a single numeric part')
    half = 0.5 * 10 ** -places + 1e-12
    ok(abs(float(exact) - float(second)) < 1e-6, f'{where}: the two routes differ: {float(exact)} and {float(second)}')
    ok(abs(float(w['answer']) - float(exact)) <= half, f'{where}: key {w["answer"]} is not {float(exact)}')
    for t in takes:
        ok(grade(w, t) is True, f'{where}: "{t}" should be taken, got {grade(w, t)}')
    for t in refuses:
        ok(grade(w, t) is not True, f'{where}: "{t}" should be refused')
    ids = [x['id'] for x in w.get('wrong', [])]
    if wrong is not None:
        ok(sorted(ids) == sorted(wrong), f'{where}: wrong ids {ids} are not {sorted(wrong)}')
        for x in w.get('wrong', []):
            if x['id'] not in wrong:
                continue
            slip = float(wrong[x['id']])
            tol = (x.get('tol') or {}).get('abs', 0)
            # the stored value is the slip to the places it is written with, and the slip sits in the entry's own band
            dp = len(repr(x['value']).split('.')[1]) if '.' in repr(x['value']) and 'e' not in repr(x['value']) else 0
            ok(abs(slip - float(x['value'])) <= 0.5 * 10 ** -dp + 1e-9 and within(slip, float(x['value']), x.get('tol') or {'abs': 1e-9}) or tol == 0 and slip == x['value'],
               f'{where}: wrong {x["id"]} = {x["value"]} (tol {tol}), the slip gives {slip}')
            ok(not within(float(x['value']), float(w['answer']), w.get('tol')), f'{where}: wrong {x["id"]} inside the answer band')
            shown = x['value'] * 100 if w.get('unit') == '%' else x['value']
            ok(grade(w, f'{shown:.10g}') == x['id'], f'{where}: wrong {x["id"]} typed lands on {grade(w, f"{shown:.10g}")}')
            ok(x['id'] in p['feedback'].get('byKey', {}), f'{where}: wrong {x["id"]} has no line')
    for t, i in (routes or {}).items():
        ok(grade(w, t) == i, f'{where}: "{t}" lands on {grade(w, t)}, expected {i}')
    return p


def text_has(p, *needles):
    blob = json.dumps(p, ensure_ascii=False)
    for s in needles:
        ok(s in blob, f'printed text lacks {s!r}: {blob[:80]}')


def no_stale(course, n, iid, *stale):
    blob = json.dumps(item(course, n, iid), ensure_ascii=False)
    for s in stale:
        ok(s not in blob, f'{course} {n} {iid}: stale {s!r}')


def bisect(f, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(lo) > 0) == (f(mid) > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# =============================== fix pass 0.3 b: exp-log ===============================
E_ = 'exp-log'
# set 1
p = num(E_, 1, 'p-rare-coin', 4, 1250 * sp.sqrt(sp.Rational(5, 4)), 1250 * math.sqrt(1.25),
        takes=['1397', '1398', '1397.5', '1397.54', '1396.6', '1398.5'], refuses=['1399', '1396', '1396.5'], places=2)
ok(p['widget']['tol'] == {'abs': 1}, 'coin 4 tol')
ok(3000 + 2 ** 1 == 3002 and 3000 * 2 ** 1 == 6000, 'yeast line')
text_has(part(E_, 1, 'p-yeast-culture', 1), '3,002 cells, not 6,000')
text_has(part(E_, 1, 'p-curve-point', 4), 'in the y-axis')
ok(4 ** 5.5 == 2048 and F(1, 4) ** -5 * 2 == 2048, 'curve point 4^5.5')

# set 2: forty doublings
lg2 = 0.30103
ok(2 ** 40 == 1099511627776 and 2 ** 53 < 10 ** 16 < 2 ** 54, 'forty: 2^53 < 10^16 < 2^54')
k_exact = next(k for k in itertools.count() if 2 ** (40 + k) > 10 ** 16)          # route 1: whole-number loop
k_logs = math.ceil(math.log10(1e16 / 1.10e12) / lg2)                             # route 2: the question's own figures
k_alt = math.ceil(16 / lg2) - 40                                                 # route 3: 16 / log 2, less the first 40
k_p1 = math.ceil((16 - 12.0412) / lg2)                                           # route 4: part 1's 12.0412
ok(k_exact == k_logs == k_alt == k_p1 == 14, f'forty 4: {k_exact} {k_logs} {k_alt} {k_p1}')
fac = 1e16 / 1.10e12
ok(round(fac) == 9091 and abs(math.log10(9091) - 3.9586) < 5e-5 and round(3.9586 / lg2, 2) == 13.15, 'forty 4 printed 9091, 3.9586, 13.15')
ok(2 ** 13 == 8192 < fac < 2 ** 14, 'forty 4: 8192 short of 9091')
ok(round(13.15) == 13, 'forty 4: nearest whole is the rounded-down slip, not the key')
num(E_, 2, 'p-forty-doublings', 4, 14, k_logs, takes=['14'], refuses=['13', '15', '10'],
    wrong={'rounded-down': math.floor(3.9586 / lg2), 'tenfold-steps': round(math.log10(9091)), 'total': 40 + 14})
text_has(part(E_, 2, 'p-forty-doublings', 4), '10^{16}', '9091', '8192', '13.15', '3.9586')
no_stale(E_, 2, 'p-forty-doublings', '10^{15}', '909$', '9.83', '2.9586')

# set 2: drawdown, 11% a month
n_exact = 2 * sp.log(sp.Rational(5, 4)) / sp.log(sp.Rational(111, 100))
n_bis = bisect(lambda n: 1.11 ** n - 1.5625, 0, 20)
n_given = 2 * 0.09691 / 0.04532
ok(abs(math.log10(1.25) - 0.09691) < 5e-6 and abs(math.log10(1.11) - 0.04532) < 5e-6, 'drawdown: given logs')
ok(round(2 * 0.09691, 5) == 0.19382 and round(n_given, 2) == 4.28 and round(float(n_exact), 2) == 4.28, 'drawdown 3: 4.28 both ways')
num(E_, 2, 'p-drawdown-recovery', 3, n_exact, n_bis, places=4,
    takes=['4.28', '4.2764', '4.2767', '4.277', '4.276'], refuses=['4.27', '4.29', '4.3', '4', '5.80'],
    wrong={'no-power': 0.09691 / 0.04532, 'inverted': 0.04532 / 0.19382, 'simple': 56.25 / 11,
           'carried': math.log10(1.4) / 0.04532, 'divided-numbers': 1.5625 / 1.11},
    routes={'2.138': 'no-power', '0.234': 'inverted', '5.114': 'simple', '3.224': 'carried', '1.408': 'divided-numbers'})
v = 32000.0
hist = []
for m in range(1, 8):
    v *= 1.11
    hist.append(v)
first = next(m for m, x in enumerate(hist, 1) if x > 50000)
ok(first == 5 == math.ceil(float(n_exact)) and round(hist[3]) == 48578 and round(hist[4]) == 53922, f'drawdown 4: {first}, {hist[3]:.1f}, {hist[4]:.1f}')
ok(F(32000) * F(111, 100) ** 4 < 50000 < F(32000) * F(111, 100) ** 5, 'drawdown 4 exact')
ok(round(4.28) == 4, 'drawdown 4: nearest whole is a slip')
num(E_, 2, 'p-drawdown-recovery', 4, 5, first, takes=['5'], refuses=['4', '6', '7'], wrong={'rounded-down': 4, 'with-falls': 5 + 2})
text_has(part(E_, 2, 'p-drawdown-recovery', 4), '48{,}578', '53,922', '4.28')
no_stale(E_, 2, 'p-drawdown-recovery', '8%', '1.08', '5.80', '0.03342', '7.03', '4.37')
ok(50000 * F(4, 5) ** 2 == 32000 and F(50000, 32000) == F(25, 16) == F(5, 4) ** 2 and round(32000 * 1.2 ** 2) == 46080, 'drawdown 1, 2 carried figures')

# set 2: app users
p = part(E_, 2, 'p-app-users', 2)
opts = {o['id']: o for o in p['widget']['options']}
ok([o['id'] for o in p['widget']['options'] if o.get('correct')] == ['ratio'] and set(opts) == {'ratio', 'quotient', 'difference', 'numbers'}, 'app 2 options')
n_app = sp.log(25) / sp.log(sp.Rational(13, 10))
n_app2 = bisect(lambda n: 1.3 ** n - 25, 0, 40)
ok(round(math.log10(25 / 1.3), 3) == 1.284 and round(math.log10(25) - math.log10(1.3), 3) == 1.284 and round(25 / 1.3, 2) == 19.23 and 1.3 ** 19.23 > 150, 'app 2 why lines')
ok(F(50000, 2000) == 25, 'app 2: 1.3^n = 25')
num(E_, 2, 'p-app-users', 3, n_app, n_app2, places=4, takes=['12.27', '12.2687', '12.269', '12.2691'], refuses=['12.26', '12.28', '12.3', '12'],
    wrong={'joined': math.log(50000) / math.log(2600), 'divided': 25 / 1.3, 'rate-only': math.log(25) / math.log(0.3),
           'simple': F(50000 - 2000, 600)},
    routes={'80': 'simple', '80.0': 'simple', '83.33': None})
ok(round(math.log10(25), 5) == 1.39794 and round(math.log10(1.3), 5) == 0.11394 and round(1.39794 / 0.11394, 2) == 12.27, 'app 3 printed logs')
u = [2000 * F(13, 10) ** k for k in range(14)]
ok(u[12] < 50000 < u[13] and round(float(u[12])) == 46596 and round(float(u[13])) == 60575 and math.ceil(float(n_app)) == 13, 'app 4 stands')

# set 3
w = part(E_, 3, 'p-savings-doubling', 4)['widget']
yw = {x['id']: x for x in w['wrong']}
slip_a = float(2400 * sp.exp(sp.Rational(11, 200) * sp.Rational(3, 2)))
slip_b = 2400 * sum(0.0825 ** k / math.factorial(k) for k in range(15))
ok(abs(slip_a - slip_b) < 1e-9 and abs(yw['years']['value'] - slip_a) < 0.05, f"savings 4 years = {yw['years']['value']}, the slip gives {slip_a:.3f}")
ok(not within(yw['years']['value'], w['answer'], w.get('tol')), 'savings 4: years inside the answer band')

fri = 40 * math.exp(0.043)
ok(round(fri, 2) == 41.76 and abs(0.030 - 0.012 + 0.045 - 0.020 - 0.043) < 1e-12, 'weekly 1, 2')
l3 = sp.log(sp.Rational(4500, 4176))
l3b = bisect(lambda x: 41.76 * math.exp(x) - 45, 0, 1)
num(E_, 3, 'p-weekly-target', 3, l3, l3b, places=6, takes=['0.0747', '0.0748', '0.07472', '0.07478', '0.074724'],
    refuses=['0.0746', '0.0749', '0.075', '0.07'],
    wrong={'simple': (45 - 41.76) / 41.76, 'from-monday': math.log(45 / 40), 'inverted': -float(l3), 'difference': 45 - 41.76},
    routes={'-0.0747': 'inverted', '0.0776': 'simple', '0.1178': 'from-monday', '3.24': 'difference'})
ok(round(math.log(45 / 40) - 0.043, 4) == 0.0748 and round(math.log(45 / fri), 4) == 0.0748, 'weekly 3: Monday route 0.0748')
num(E_, 3, 'p-weekly-target', 4, F(747, 10000) / 3, 0.0747 / 3, places=4, takes=['0.0249', '0.02490', '0.024908', '0.024933'], refuses=['0.0247', '0.0251', '0.025867'],
    wrong={'cube-root': 0.0747 ** (1 / 3), 'times-three': 3 * 0.0747, 'carried': 0.0776 / 3},
    routes={'0.0259': 'carried', '0.42115': 'cube-root', '0.2241': 'times-three', '0.2244': 'times-three'})
s5 = sp.exp(sp.Rational(249, 10000)) - 1
s5b = sum(0.0249 ** k / math.factorial(k) for k in range(1, 12))
num(E_, 3, 'p-weekly-target', 5, s5, s5b, places=6, takes=['2.52', '2.521', '2.5213', '2.52%', '2.524'], refuses=['2.51', '2.53', '2.5', '2.49', '2.59'],
    wrong={'log-as-simple': 0.0249, 'simple-split': 0.0776 / 3, 'decimal': 0.000252, 'e-power': math.exp(0.0249)},
    routes={'0.0252': 'decimal', '0.02521': 'decimal', '0.0249': None, '0.0259': None, '2.49': 'log-as-simple', '2.59': 'simple-split', '102.52': 'e-power'})
ok(round(math.exp(0.0249), 4) == 1.0252, 'weekly 5 printed 1.0252')
blob = json.dumps(item(E_, 3, 'p-weekly-target')['parts'][3:])
ok('0.0748' not in blob, 'weekly 4, 5: a stale 0.0748')
w = part(E_, 3, 'p-monthly-deposit', 2)['widget']
ok(grade(w, '0.0479') == 'decimal' and grade(w, '0.04793') == 'decimal' and grade(w, '0.048') is None and grade(w, '0.0491') is None and grade(w, '4.79') is True, 'deposit 2 decimal band')
ok(abs(5 * 0.0479 - part(E_, 3, 'p-monthly-deposit', 3)['widget']['answer']) < 1e-4, 'deposit 3 key')
it = item(E_, 3, 'p-log-chart-line')
ok('2017' in it['prose'] and '2025' in it['prose'] and 2025 - 2017 == 8 and '2021, 4 years in' in it['parts'][2]['question'] and 2021 - 2017 == 4, 'log chart dates')
no_stale(E_, 3, 'p-log-chart-line', '2016', '2026', '2022')
ok(abs(math.sqrt(15 * 135) - 45) < 1e-12 and abs(it['parts'][2]['widget']['answer'] - 45) < 1.5, 'log chart 3: the price 4 years in')

# =============================== fix pass 0.3 c: series ===============================
S_ = 'series'
rows = [8 + 5 * k for k in range(10)]
ok(rows[0] == 8 and len(rows) == 10 and all(rows[k - 1] == 5 * k + 3 for k in range(1, 11)), 'tins: row k = 5k + 3')
num(S_, 2, 'p-tin-display', 1, 8 + (10 - 1) * 5, rows[-1], takes=['53'], refuses=['52', '54'], wrong={'n-steps': 8 + 10 * 5, 'step-only': 10 * 5})
num(S_, 2, 'p-tin-display', 2, F(10, 2) * (8 + 53), sum(rows), takes=['305'], refuses=['304'],
    wrong={'no-halve': 10 * (8 + 53), 'last-only': 5 * 53, 'n-steps': 5 * (16 + 10 * 5)})
num(S_, 2, 'p-tin-display', 3, 10 - 4 + 1, len(rows[3:]), takes=['7'], wrong={'subtract': 10 - 4, 'top': 10})
num(S_, 2, 'p-tin-display', 4, F(7, 2) * (23 + 53), sum(rows[3:]), takes=['266'], refuses=['265'],
    wrong={'six-rows': 3 * (23 + 53), 'four-left': 305 - sum(rows[:4]), 'full': 305})
ok(rows[3] == 23 and sum(rows[:3]) == 39 == 8 + 13 + 18 and sum(rows[:4]) == 62 and 305 - 39 == 266 and 7 * 38 == 266, 'tins 4 printed')
ok(sum(5 * k + 3 for k in range(4, 11)) == 266, 'tins: the sigma sum')
no_stale(S_, 2, 'p-tin-display', '192', ' 27 ', '160', '147', '140', '12 rows')

c = lambda n, k: sum(1 for _ in itertools.combinations(range(n), k))
num(S_, 3, 'p-pizza-toppings', 1, math.comb(11, 4), c(11, 4), takes=['330'],
    wrong={'ordered': 11 * 10 * 9 * 8, 'times': 11 * 4, 'three-orders': F(11 * 10 * 9 * 8, 6)})
num(S_, 3, 'p-pizza-toppings', 2, math.comb(11, 4) + math.comb(11, 7), c(11, 4) + c(11, 7), takes=['660'], wrong={'one-size': 330})
num(S_, 3, 'p-pizza-toppings', 3, math.comb(12, 4), c(12, 4), takes=['495'],
    wrong={'one-more': 330 + 11, 'doubled': 2 * 330, 'ordered': 12 * 11 * 10 * 9})
ok(c(11, 3) == 165 and 330 + 165 == 495 and 7920 // 24 == 330 and 11880 // 24 == 495, 'pizza printed')
row12 = [math.comb(12, k) for k in range(13)]
ok(row12[:5] == [1, 12, 66, 220, 495], 'pizza: row 12 begins')
num(S_, 3, 'p-pizza-toppings', 4, 2 ** 12, sum(1 for _ in itertools.product((0, 1), repeat=12)), takes=['4096'],
    wrong={'no-plain': 2 ** 12 - 1, 'row-eleven': sum(math.comb(11, k) for k in range(12))})
ok(sum(row12) == 4096, 'pizza: row 12 sum')
no_stale(S_, 3, 'p-pizza-toppings', '56', '84', '512', '336', '8 toppings', '9th', '6720')

x = F(1, 100)
terms = [math.comb(7, k) * (-3 * x) ** k for k in range(8)]
ok(math.comb(7, 3) * 27 == 945 and sum(terms[:3]) == F(8089, 10000) and sum(terms) == F(97, 100) ** 7, 'bracket: the expansion')
num(S_, 3, 'p-bracket-estimate', 5, sum(terms[:4]), 0.8089 - 945 * 0.01 ** 3, places=6,
    takes=['0.80796', '0.80795', '0.807955'], refuses=['0.80798', '0.807983', '0.80797', '0.80794', '0.808', '0.8080'],
    wrong={'calculator': 0.97 ** 7, 'added': 0.8089 + 0.000945, 'square': 0.8089 - 945 * 0.0001},
    routes={'0.80798': 'calculator', '0.807983': 'calculator', '0.8079828': 'calculator', '0.80797': None, '0.80985': 'added', '0.80984': 'added'})

# pendulum, tablet, shop: printed figures of the changed lines
g = [160 * F(2, 5) ** (n - 1) for n in range(1, 4)]
ok(g == [160, 64, F(128, 5)] and abs(400 - 374.4 - 25.6) < 1e-9 and 400 - 336 == 64, 'tablet g1, g2, g3 = 160, 64, 25.6')
ok(all(64 * F(3, 2) ** n == 96 * F(3, 2) ** (n - 1) for n in range(1, 9)) and 96 / 1.5 == 64 and 64 * 1.5 ** 3 == 216, 'shop 4: the deleted entry equalled month-two-start')
ok([x['id'] for x in part(S_, 1, 'p-shop-orders', 4)['widget']['wrong']] == ['month-two-start', 'arith'], 'shop 4 wrong ids')

# =============================== fix pass 0.3 c: trig ===============================
T_ = 'trig'
s3 = sp.sqrt(3)
P = {k: sp.Matrix([8 * sp.cos(sp.pi * i / 3), 8 * sp.sin(sp.pi * i / 3)]) for i, k in enumerate('ABCDEF')}
dist = lambda a, b: sp.sqrt(((P[a] - P[b]).T * (P[a] - P[b]))[0])
ok(all(sp.simplify(dist(a, b) - 8) == 0 for a, b in ('AB', 'BC', 'CD')), 'hexagon: sides 8')
h1 = sp.sqrt(8 ** 2 - 4 ** 2)
ok(sp.simplify(h1 - 4 * s3) == 0 and abs(8 * math.sin(math.radians(60)) - 4 * math.sqrt(3)) < 1e-12, 'hexagon 1: 4 sqrt 3')
ok(sp.simplify(dist('A', 'C') - 8 * s3) == 0 and abs(float(dist('A', 'C')) - 13.86) < 0.005, 'hexagon 2: AC = 8 sqrt 3')
ok(sp.simplify(dist('A', 'D') - 16) == 0, 'hexagon: AD = 16')
w1 = {x['id']: x['tex'] for x in part(T_, 1, 'p-hexagon-tile', 1)['widget']['wrong']}
w2 = {x['id']: x['tex'] for x in part(T_, 1, 'p-hexagon-tile', 2)['widget']['wrong']}
ok(w1 == {'added': '\\sqrt{80}', 'whole-side': '8\\sqrt{3}', 'half-square': '4\\sqrt{2}'} and 8 ** 2 + 4 ** 2 == 80 and 16 ** 2 - 8 ** 2 == 192, 'hexagon 1 wrong')
ok(w2 == {'half': '4\\sqrt{3}', 'side': '8', 'long': '16'}, 'hexagon 2 wrong')
ok(part(T_, 1, 'p-hexagon-tile', 1)['widget']['answer'] == '4\\sqrt{3}' and part(T_, 1, 'p-hexagon-tile', 2)['widget']['answer'] == '8\\sqrt{3}', 'hexagon keys')
num(T_, 1, 'p-hexagon-tile', 3, sp.expand(dist('A', 'C') ** 2 + dist('C', 'D') ** 2), (8 * math.sqrt(3)) ** 2 + 8 ** 2, takes=['256'], refuses=['192', '255'],
    wrong={'root-as-three': 8 * 3 + 64, 'root-left': 64 * math.sqrt(3) + 64, 'cd-unsquared': 192 + 8},
    routes={'174.85': 'root-left', '174.9': 'root-left', '175': 'root-left'})
va, vc = P['C'] - P['A'], P['D'] - P['A']
ang = sp.acos((va.T * vc)[0] / (dist('A', 'C') * dist('A', 'D')))
num(T_, 1, 'p-hexagon-tile', 4, sp.deg(sp.simplify(ang)), math.degrees(math.asin(8 / 16)), takes=['30'], refuses=['31', '29'],
    wrong={'angle-d': 60, 'tan': math.degrees(math.atan(8 / 16)), 'half': F(8, 16), 'radians': math.asin(0.5)},
    routes={'0.5': 'half', '0.50': 'half', '0.52': 'radians', '0.524': 'radians', '0.5236': 'radians', '1': 'radians', '0.46': 'radians', '0.87': 'radians', '27': 'tan', '26.6': 'tan'})
no_stale(T_, 1, 'p-hexagon-tile', '10 cm', '5\\sqrt', '400', '300', '\\sqrt{75}', '17.32')

ok(abs(40 * math.sin(math.radians(60)) - 20 * math.sqrt(3)) < 1e-12 and round(20 * math.sqrt(3), 2) == 34.64, 'lamp 1')
aob = sp.deg(sp.atan(sp.Rational(3, 4)))
num(T_, 1, 'p-desk-lamp', 3, aob, math.degrees(math.asin(30 / 50)), places=2, takes=['36.9', '36.87', '36.870'], refuses=['36.8', '37', '37.0'],
    wrong={'flipped': math.degrees(math.atan(40 / 30)), 'sine': math.degrees(math.asin(30 / 40)), 'ratio-tan': F(3, 4), 'ratio-sin': F(3, 5), 'radians': math.atan(0.75)},
    routes={'0.75': 'ratio-tan', '0.6': 'ratio-sin', '0.60': 'ratio-sin', '0.64': 'radians', '0.644': 'radians', '0.6435': 'radians', '0.65': None, '0.8': None, '0.7': None, '53.1': 'flipped', '48.6': 'sine'})
ok(abs(float(20 * s3 - 15) - 19.64) < 0.005 and abs(50 * math.sin(math.radians(60 - 36.9)) - 19.6) < 0.05, 'lamp 4, 5')
ok(part(T_, 1, 'p-desk-lamp', 5)['widget']['answer'] == '20\\sqrt{3}-15' and part(T_, 1, 'p-desk-lamp', 1)['widget']['answer'] == '20\\sqrt{3}', 'lamp keys')
for iid, k in (('p-hexagon-tile', 1), ('p-hexagon-tile', 2), ('p-desk-lamp', 1), ('p-desk-lamp', 5)):
    q = part(T_, 1, iid, k)
    ok(q['widget'].get('form') == 'simplified' and 'simplest form' in q['question'], f'{iid} {k}: form simplified and the question says so')
for iid, k in (('p-hexagon-tile', 4), ('p-lake-markers', 3), ('p-desk-lamp', 3)):
    ok('level 2 teaches' in part(T_, 1, iid, k)['feedback']['byKey']['radians'], f'{iid} {k}: radians line')
ok(abs(math.asin(45 * 0.8192 / 50.27) - 0.8232) < 5e-4, 'lake 3 radians value')
ok(abs(3 + 2.4 * math.sin(math.radians(128.9)) - 4.87) < 0.005 and abs(math.degrees(2.25) - 128.9) < 0.05, 'water wheel 4 restated figures')

# two angles
sinA, cosB = sp.Rational(28, 53), sp.Rational(24, 25)
cosA, sinB = -sp.sqrt(1 - sinA ** 2), sp.sqrt(1 - cosB ** 2)
A_, B_ = math.pi - math.asin(28 / 53), math.acos(24 / 25)
ok(cosA == sp.Rational(-45, 53) and sinB == sp.Rational(7, 25) and 28 ** 2 + 45 ** 2 == 53 ** 2 and 7 ** 2 + 24 ** 2 == 25 ** 2 and 1 - sinA ** 2 == sp.Rational(2025, 2809), 'two angles: triples')
num(T_, 3, 'p-two-angles', 1, cosA, math.cos(A_), takes=['-45/53', '-0.849', '-0.8491', '-0.849057'], refuses=['-0.85', '-0.848', '-0.88', '-0.8'],
    wrong={'sign': -cosA, 'one-minus': 1 - sinA, 'no-root': 1 - sinA ** 2}, routes={'45/53': 'sign', '0.849': 'sign', '25/53': 'one-minus', '2025/2809': 'no-root', '0.721': 'no-root', '0.472': 'one-minus'})
sAB = sinA * cosB + cosA * sinB
cAB = cosA * cosB - sinA * sinB
ok(sAB == sp.Rational(357, 1325) and cAB == sp.Rational(-1276, 1325) and 357 ** 2 + 1276 ** 2 == 1325 ** 2 and 28 * 24 == 672 and 45 * 7 == 315 and 45 * 24 == 1080 and 28 * 7 == 196, 'two angles: 357/1325, -1276/1325')
num(T_, 3, 'p-two-angles', 3, sAB, math.sin(A_ + B_), takes=['0.2694', '357/1325', '0.26943', '0.2695'], refuses=['0.269', '0.27', '0.2696', '0.2692'],
    wrong={'sign': sinA * cosB - cosA * sinB, 'sum-of-sines': sinA + sinB, 'cos-formula': cAB}, routes={'0.7449': 'sign', '0.8083': 'sum-of-sines', '-0.9630': 'cos-formula'})
num(T_, 3, 'p-two-angles', 4, cAB, math.cos(A_ + B_), takes=['-0.9630', '-0.963', '-1276/1325', '-0.96302'], refuses=['-0.96', '-0.9632', '0.9630'],
    wrong={'plus': cosA * cosB + sinA * sinB, 'sign': -cosA * cosB - sinA * sinB}, routes={'-0.6672': 'plus', '0.6672': 'sign'})
tot = math.degrees(A_ + B_)
num(T_, 3, 'p-two-angles', 5, sp.deg(sp.pi - sp.asin(sp.Rational(357, 1325))), tot, places=2, takes=['164.4', '164.37', '164.36', '164.43'], refuses=['164.3', '164.5', '164'],
    wrong={'principal': 180 - tot, 'third': 360 - tot, 'fourth': 180 + tot}, routes={'15.6': 'principal', '15.63': 'principal', '195.6': 'third', '344.4': 'fourth'})
ok(round(math.degrees(math.asin(0.2694)), 1) == 15.6 and round(180 - 15.6, 1) == 164.4 and round(math.degrees(A_), 1) == 148.1 and round(math.degrees(B_), 1) == 16.3
   and round(math.degrees(math.acos(-0.9630)), 1) == 164.4, 'two angles 5 printed')
no_stale(T_, 3, 'p-two-angles', '17}', '15}{17', '425', '0.2047', '168.', '11.8', '0.88')

# daylight
L = lambda t: 4.4 * math.sin(math.pi / 6 * (t - 3)) + 12
t = sp.symbols('t', real=True)
sol = sorted(sp.solveset(sp.Rational(22, 5) * sp.sin(sp.pi / 6 * (t - 3)) + 12 - sp.Rational(49, 5), t, sp.Interval(0, 12)))
scan = [k / 1000 for k in range(0, 12001) if abs(L(k / 1000) - 9.8) < 1e-9]
p = part(T_, 3, 'p-daylight-model', 4)
ok(sol == [2, 10] and scan == [2.0, 10.0] and sorted(p['widget']['answers']) == [2, 10] and p['widget'].get('unordered') is True, f'daylight 4: {sol} {scan}')
w4 = {x['id']: x['value'] for x in p['widget']['wrong']}
ns = [k / 1000 for k in range(0, 12001) if abs(math.sin(math.pi * k / 6000) + 0.5) < 1e-9]
ab = [k / 1000 for k in range(0, 12001) if abs(L(k / 1000) - 14.2) < 1e-9]
ok(w4 == {'no-shift': '7, 11', 'above': '4, 8'} and ns == [7.0, 11.0] and ab == [4.0, 8.0] and abs((9.8 - 12) / 4.4 + 0.5) < 1e-12 and abs(12 + 2.2 - 14.2) < 1e-12, f'daylight 4 wrong: {w4} {ns} {ab}')
above = sum(1 for k in range(12000) if L((k + 0.5) / 1000) > 9.8) / 1000
num(T_, 3, 'p-daylight-model', 5, 10 - 2, above, takes=['8'], refuses=['7'], wrong={'outside': 12 - 8, 'counted': 10 - 2 + 1})
ok(abs(L(6) - 16.4) < 1e-9 and abs(L(12) - 7.6) < 1e-9 and abs(L(0) - 7.6) < 1e-9, 'daylight: peak and trough')

# garden bed
p = part(T_, 3, 'p-garden-bed', 1)
ok(p['widget']['answer'] == '65\\sin C' and sp.Rational(1, 2) * 10 * 13 == 65, 'garden 1 key')
ok({x['id']: x['tex'] for x in p['widget']['wrong']} == {'no-half': '130\\sin C', 'cos': '65\\cos C', 'angle': '65C'}, 'garden 1 wrong')
c1 = math.degrees(math.asin(25 / 65))
c1b = bisect(lambda d: 65 * math.sin(math.radians(d)) - 25, 0, 90)
p = part(T_, 3, 'p-garden-bed', 2)
ok(abs(c1 - c1b) < 1e-9 and p['widget']['answers'] == [22.62, 157.38] and round(c1, 2) == 22.62 and round(180 - c1, 2) == 157.38 and F(25, 65) == F(5, 13), f'garden 2: {c1}')
nh = math.degrees(math.asin(25 / 130))
ok({x['id']: x['value'] for x in p['widget']['wrong']} == {'no-half': f'{nh:.2f}, {180 - nh:.2f}', 'cos-rule': f'{c1:.2f}, {360 - c1:.2f}'}, 'garden 2 wrong')
for tri in (c1, 180 - c1):   # the triangle by coordinates
    X = (10 * math.cos(math.radians(tri)), 10 * math.sin(math.radians(tri)))
    ok(abs(0.5 * abs(13 * X[1]) - 25) < 1e-9, 'garden: area 25 by coordinates')
cosC = -sp.sqrt(1 - sp.Rational(5, 13) ** 2)
num(T_, 3, 'p-garden-bed', 3, cosC, math.cos(math.radians(180 - c1)), takes=['-12/13', '-0.923', '-0.9231', '-0.92308'], refuses=['-0.92', '-0.924', '-0.922', '-0.9'],
    wrong={'sign': -cosC, 'one-minus': 1 - sp.Rational(5, 13), 'no-root': -(1 - sp.Rational(25, 169))}, routes={'12/13': 'sign', '8/13': 'one-minus', '-144/169': 'no-root', '-0.852': 'no-root'})
c2 = 10 ** 2 + 13 ** 2 - 2 * 10 * 13 * cosC
X = (10 * math.cos(math.radians(180 - c1)), 10 * math.sin(math.radians(180 - c1)))
num(T_, 3, 'p-garden-bed', 4, sp.sqrt(c2), math.hypot(X[0] - 13, X[1]), places=3, takes=['22.56', '22.561', '22.5610'], refuses=['22.6', '22.55', '22.57', '23'],
    wrong={'sign': math.sqrt(269 - 240), 'pythagoras': math.sqrt(269), 'no-root': 509, 'no-two': math.sqrt(269 + 120)},
    routes={'5.39': 'sign', '5.385': 'sign', '16.40': 'pythagoras', '16.4': 'pythagoras', '19.72': 'no-two', '509': 'no-root'})
ok(c2 == 509 and 2 * 10 * 13 == 260 and 260 * F(12, 13) == 240 and round(math.sqrt(29), 2) == 5.39, 'garden 4 printed')
no_stale(T_, 3, 'p-garden-bed', '30\\sin', '36.87', '143.13', '16.28', 'tfrac{4}{5}', 'tfrac{3}{5}', '265')

# quadratic in sine 4
ok(sp.Rational(150, 180) * sp.pi == 5 * sp.pi / 6 and 'with no $x =$ in front' in part(T_, 3, 'p-quadratic-in-sine', 4)['question'], 'quadratic 4')

# =============================== all nine files: bands ===============================
nparts = 0
band = lambda v, tol: (v - (tol or {}).get('abs', 0), v + (tol or {}).get('abs', 0))
for course in (E_, S_, T_):
    for n in (1, 2, 3):
        for it in load(course, n)['items']:
            for k, p in enumerate(it['parts'], 1):
                w = p['widget']
                if w['kind'] != 'numeric' or 'answers' in w:
                    continue
                nparts += 1
                where = f'{course} {n} {it["id"]} p{k}'
                bands = [('answer', band(w['answer'], w.get('tol')))] + [(x['id'], band(x['value'], x.get('tol'))) for x in w.get('wrong', [])]
                for x in w.get('wrong', []):
                    ok(not within(x['value'], w['answer'], w.get('tol')), f'{where}: wrong {x["id"]} inside the answer band')
                    ok(x['id'] in p['feedback'].get('byKey', {}), f'{where}: wrong {x["id"]} has no byKey line')
                for i in range(len(bands)):
                    for j in range(i + 1, len(bands)):
                        (na, a), (nb, b) = bands[i], bands[j]
                        if a[1] < b[0] - 1e-9 or b[1] < a[0] - 1e-9:
                            checks += 1
                            continue
                        inside_later = i > 0 and a[0] >= b[0] and a[1] <= b[1]
                        ok(inside_later, f'{where}: bands {na} {a} and {nb} {b} meet and the earlier is not inside the later')
                        if inside_later:
                            note(f'{where}: band {na} {a} sits inside the later {nb} {b}; first match resolves it')
print(f'recompute.py: {checks} checks, {fails} failures, {notes} notes; band pass over {nparts} single-value numeric parts')
raise SystemExit(1 if fails else 0)
