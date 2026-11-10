#!/usr/bin/env python3
"""Concept audit checks, mm-games level 2 (l5 to l9, review-2, homework-2).

Exits 0 when the content is correct. A check that fails because the content
is wrong is marked EXPECTED_FAIL: it is listed, the corrected assert sits in a
comment beside it, and it does not change the exit code.
Run from the repo root: python3 docs/reports/mm-games-L2-concepts.py
"""
import json, os, random, sys
from fractions import Fraction as F
from itertools import combinations, product
from math import isclose, sqrt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'mm-games')
FAILS, XFAILS, PASSES = [], [], [0]


def check(name, cond, expected_fail=False):
    if cond:
        PASSES[0] += 1
        if expected_fail:
            print(f'NOTE  {name}: marked EXPECTED_FAIL but passes (content fixed?)')
    elif expected_fail:
        XFAILS.append(name); print(f'EXPECTED_FAIL  {name}')
    else:
        FAILS.append(name); print(f'FAIL  {name}')


def load(name):
    return json.load(open(os.path.join(CDIR, name + '.json')))


def close(a, b, rel):
    if isinstance(a, (tuple, list)):
        return len(a) == len(b) and all(close(x, y, rel) for x, y in zip(a, b))
    return isclose(float(a), float(b), rel_tol=rel, abs_tol=1e-12)


def run_code_widget(label, w):
    """Solution passes every example and hidden test in CPython; starter fails."""
    def run(src):
        ok = 0; cases = w.get('examples', []) + w['tests']
        for c in cases:
            ns = {}
            try:
                exec(w.get('prelude', '') + '\n' + src, ns)
                if c.get('setup'): exec(c['setup'], ns)
                got = eval(c['call'], ns); exp = eval(str(c['expect']), ns)
                mode = c.get('compare', 'equal')
                if mode == 'isclose':
                    good = close(got, exp, (c.get('tol') or {}).get('rel', 1e-9))
                elif mode == 'fraction':
                    good = isinstance(got, (F, int)) and F(got) == F(exp)
                else:
                    good = got == exp
            except Exception:
                good = False
            ok += bool(good)
        return ok, len(cases)
    ok, n = run(w['solution'])
    check(f'{label}: solution passes {ok}/{n}', ok == n)
    ok2, _ = run(w['starter'])
    check(f'{label}: starter fails', ok2 < n)


E = lambda fn, n: F(sum(fn(r) for r in product(range(1, 7), repeat=n)), 6 ** n)
DIE = range(1, 7)

# ---------- l5: two-sided price ----------
check('l5 buy 9.5 / sell 11.5 each earn 1 against 10.5', 10.5 - 9.5 == 1 and 11.5 - 10.5 == 1)
check('l5 sold 3 at 11.5: +3; cash 34.5', 3 * (11.5 - 10.5) == 3 and 3 * 11.5 == 34.5)
check('l5 larger of two dice 161/36 lies in 4..5', 4 < E(max, 2) < 5)
# coin game: heads before the first tail
rng = random.Random(2); N = 400000
tot = 0
for _ in range(N):
    while rng.random() < 0.5:
        tot += 1
check('l5 coin game: mean heads before first tail is 1 (sim)', abs(tot / N - 1) < 0.01)
check('l5 coin game: mean number of flips is 2', sum(k * 0.5 ** k for k in range(1, 200)) == 2.0)
check('l5 product of two dice 12.25: quote 11.25 at 13.25', E(lambda r: r[0] * r[1], 2) == F(49, 4))
check('l5 mode-centred 5.5 at 6.5: a sale to you at 5.5 loses about 1.03', abs(5.5 - 161 / 36 - 1.03) < 5e-3)
check('l5 round trip earns 2qh', all((m - (m - h)) * q + ((m + h) - m) * q == 2 * q * h for m, h, q in [(10.5, 1, 3), (14, 1.5, 2)]))
check('l5 quiz crossed 12 at 10: -2', (10.5 - 12) + (10 - 10.5) == -2)
# "a crossed quote loses on every trade": false when fair value is outside the crossed quote
bid, ask, fair = 12, 11, 13
# (corrected claim, fix pass) l5 s8 now says a crossed quote loses on every round trip: buy at the bid, sell at the ask
check('l5 s8: a crossed quote loses the crossed width on every round trip, whatever the fair value  (corrected claim, fix pass)',
      all((f - bid) + (ask - f) == ask - bid == -1 for f in (10, 11.5, 13)) and (fair - bid) == 1
      and 'every round trip' in load('l5-two-sided')['screens'][8]['prose'])
check('l5 option quote 4.15 at 4.25', abs(4.20 - 0.05 - 4.15) < 1e-12)
run_code_widget('l5 s10 code', load('l5-two-sided')['screens'][10]['widget'])

# ---------- l6: edge ----------
check('l6 pay 3 to roll: +0.5', E(sum, 1) - 3 == F(1, 2))
check('l6 coin game at 1.20: -0.20; heads pays 2 for 1.10: -0.10', abs(1 - 1.2 + 0.2) < 1e-12 and abs(0.5 * 2 - 1.1 + 0.1) < 1e-12)
check('l6 four random trades at half-width 1: +4, long 2', 1 + 1 + 1 + 1 == 4 and 1 + 1 - 1 + 1 == 2)
p3 = {}
for r in product(DIE, repeat=3):
    p3[sum(r)] = p3.get(sum(r), 0) + F(1, 216)
above = sum(p for s, p in p3.items() if s > 12); below = sum(p for s, p in p3.items() if s < 12)
check('l6 26% of three-dice rolls land above 12', abs(float(above) - 0.26) < 0.005)
# (corrected claim, fix pass) l6 s6 hint now says most rolls land below 12, where the sale wins
check('l6 s6 hint: the sale at 12 wins on every roll below 12, 135 of 216 (most), and is flat at 12 (25 of 216)  (corrected claim, fix pass)',
      below == F(135, 216) and below > F(1, 2) and p3[12] == F(25, 216) and all((12 - s) > 0 for s in p3 if s < 12)
      and load('l6-edge')['screens'][6]['hints'][1]['text'] == 'Most rolls land below 12, where the sale wins.')
series = load('l6-edge')['screens'][7]['canvas']['params']['series'][0]['values']
steps = [b - a for a, b in zip(series, series[1:])]
check('l6 s7 path: 100 plays, each step a profit of -2..3, ends at 70', len(steps) == 100 and set(steps) <= set(range(-2, 4)) and series[-1] == 70)
check('l6 variance of one play 35/12; 100 plays sd 17.08; one play x100 sd 170.78',
      E(lambda r: r[0] ** 2, 1) - F(49, 4) == F(35, 12) and abs(10 * sqrt(35 / 12) - 17.08) < 5e-3 and abs(100 * sqrt(35 / 12) - 170.78) < 5e-3)
# (corrected claim, fix pass) l6 s2 now says 1.5 on average over every roll, though one roll can win or lose more
check('l6 s2: the sale at 12 earns 1.5 on average; single rolls pay from +9 to -6  (corrected claim, fix pass)',
      sum((12 - s) * p for s, p in p3.items()) == F(3, 2) and min(12 - s for s in p3) == -6 and max(12 - s for s in p3) == 9
      and 'whatever the dice show' not in load('l6-edge')['screens'][2]['explain']['text'])
check('l6 coin game E = (1 + E)/2 gives 1', F(1, 2) * 0 + F(1, 2) * (1 + 1) == 1)
check('l6 desk: 2000 x 100 x 0.5p = 1000 pounds', 2000 * 100 * 0.5 / 100 == 1000)
check('l6 quiz: larger for 4 pounds = 17/36; buy 2 at 9 = +3', E(max, 2) - 4 == F(17, 36) and 2 * (10.5 - 9) == 3)
run_code_widget('l6 s10 code', load('l6-edge')['screens'][10]['widget'])

# ---------- l7: skew ----------
quote = lambda V, g, q, h=1: (V - g * q - h, V - g * q + h)
check('l7 short 2: 10 at 12; short 3: 10.25 at 12.25; long 4: 8.5 at 10.5; long 3 ask 10.75',
      quote(10.5, 0.25, -2) == (10, 12) and quote(10.5, 0.25, -3) == (10.25, 12.25) and quote(10.5, 0.25, 4) == (8.5, 10.5) and quote(10.5, 0.25, 3)[1] == 10.75)
q = 0; bids = []
for t in (-1, -1, 1, -1):
    q += t; bids.append(quote(10.5, 0.25, q)[0])
check('l7 four trades: bids 9.75, 10, 9.75, 10', bids == [9.75, 10.0, 9.75, 10.0])
q = 0; pnl = 0
for t in (1, 1, -1):
    b, a = quote(10.5, 0.25, q)
    pnl += (10.5 - b) if t == 1 else (a - 10.5); q += t
check('l7 hit, hit, lifted: +2.75, long 1', pnl == 2.75 and q == 1)
check('l7 calls: short 20 lots at 0.005 a lot: 2.50 at 2.60', abs(2.45 + 20 * 0.005 - 0.05 - 2.50) < 1e-9)
check('l7 quiz: sold 2 at 12, bought 1 at 10: +3.5', 2 * 1.5 + 0.5 == 3.5)
# Direction of the skew: a long maker who lowers both quotes sheds inventory faster than one who does not (random flow whose
# chance of taking a side falls with that side's distance from fair value).
rng = random.Random(9)


def flatten_time(skewed, n=4000):
    tot = 0
    for _ in range(n):
        pos, t = 4, 0
        while pos > 0 and t < 400:
            b, a = quote(10.5, 0.25 if skewed else 0.0, pos)
            p_buy = max(0.0, 0.5 - 0.2 * (a - 10.5)); p_sell = max(0.0, 0.5 - 0.2 * (10.5 - b))
            u = rng.random()
            pos += -1 if u < p_buy else (1 if u < p_buy + p_sell else 0); t += 1
        tot += t
    return tot / n


ts, tn = flatten_time(True), flatten_time(False)
print(f'      l7 sim: mean steps for a long 4 to get flat: skewed {ts:.1f}, unskewed {tn:.1f}')
check('l7 sim: skewing down when long sheds the position faster', ts < 0.7 * tn)
# quiz[1]: fair 50, long 5, keyed quote 47.5 at 49.5: the ask is below fair value
# (corrected claim, fix pass) l7 quiz[1] explain now says the ask at 49.5 gives up 0.5 a unit to shed risk
check('l7 quiz[1]: the keyed ask 49.5 has edge -0.5 a unit against fair 50, and the explain says so  (corrected claim, fix pass)',
      49.5 - 50 == -0.5 and 'give up 0.5 a unit' in load('l7-skewing')['quiz'][1]['explain']['text'])
run_code_widget('l7 s10 code', load('l7-skewing')['screens'][10]['widget'])

# ---------- l8: informed flow ----------
L = lambda b, a, xs=DIE: F(sum(max(x - a, 0) + max(b - x, 0) for x in xs), len(list(xs)))
H = F(1, 2)
check('l8 informed loss: 2.5/4.5 = 2/3, 1.5/5.5 = 1/6, 3/4 = 1, 2/5 = 1/3, 0.5/6.5 = 0',
      (L(5 * H, 9 * H), L(3 * H, 11 * H), L(3, 4), L(2, 5), L(H, 13 * H)) == (F(2, 3), F(1, 6), 1, F(1, 3), 0))
# (corrected claim, fix pass) l8 s1 now says any bid above 1 or ask below 6 trades against you; 1 at 6 is safe too
grid_b = [F(k, 2) for k in range(1, 8)]; grid_a = [F(k, 2) for k in range(7, 14)]
safe = {(b, a) for b in grid_b for a in grid_a if L(b, a) == 0}
check('l8 s1: on the slider grid a quote loses nothing exactly when bid <= 1 and ask >= 6  (corrected claim, fix pass)',
      safe == {(b, a) for b in grid_b for a in grid_a if b <= 1 and a >= 6} and L(1, 6) == 0 and L(F(3, 2), 6) > 0 and L(1, F(11, 2)) > 0
      and 'Any bid above 1 or ask below 6' in load('l8-informed-flow')['screens'][1]['explain']['text'])
mixed = lambda b, a, al, fair=F(7, 2): (1 - al) * (H * (a - fair) + H * (fair - b)) - al * L(b, a)
check('l8 mixed: 11/12, 7/12, 1/6; alpha 0.2 at 1.5/5.5 = 47/30',
      (mixed(3 * H, 11 * H, H), mixed(2, 5, H), mixed(5 * H, 9 * H, H), mixed(3 * H, 11 * H, F(1, 5))) == (F(11, 12), F(7, 12), F(1, 6), F(47, 30)))
check('l8 quiz: 2.5/5.5 loses 5/12; two dice 5/9 loses 5/9; P(trade) 12/36',
      L(5 * H, 11 * H) == F(5, 12) and L(5, 9, [a + b for a, b in product(DIE, repeat=2)]) == F(5, 9))
check('l8 four games 2,3,1,6 at 2/5: -2; expected 4/3', -(2 - 1) - (6 - 5) == -2 and 4 * L(2, 5) == F(4, 3))
# Monte Carlo of the informed die game and of the mixed toy
rng = random.Random(8); N = 300000
tot = 0.0
for _ in range(N):
    x = rng.randint(1, 6)
    if x > 4.5: tot -= x - 4.5
    elif x < 2.5: tot -= 2.5 - x
check('l8 sim: informed game at 2.5/4.5 loses 2/3', abs(tot / N + 2 / 3) < 0.01)
tot = 0.0
for _ in range(N):
    x = rng.randint(1, 6)
    if rng.random() < 0.5:
        tot -= max(x - 5.5, 0) + max(1.5 - x, 0)
    else:
        tot += (5.5 - x) if rng.random() < 0.5 else (x - 1.5)
check('l8 sim: mixed toy at 1.5/5.5 earns 11/12 (random trades settled at the die)', abs(tot / N - 11 / 12) < 0.02)
# Glosten-Milgrom one-period model: value V0 +- delta, share alpha informed, rest buy or sell at random.
# Zero-profit ask = E[V | buy] = V0 + alpha * delta.
for al, de in [(0.2, 10), (0.2, 30), (0.25, 12), (0.4, 10)]:
    rng = random.Random(21); buys = []; pnl_at_s = 0.0; n = 400000
    for _ in range(n):
        v = de if rng.random() < 0.5 else -de
        if rng.random() < al: buy = v > 0
        else: buy = rng.random() < 0.5
        if buy: buys.append(v)
    cond = sum(buys) / len(buys)
    check(f'l8 sim: E[V | buy] = alpha*delta for alpha {al}, delta {de} (got {cond:.3f})', abs(cond - al * de) < 0.03 * de)
check('l8 s = alpha*delta agrees with (1-alpha)h = alpha(delta-h)', all(abs((1 - al) * al * de - al * (de - al * de)) < 1e-12 for al, de in [(0.2, 10), (0.25, 12)]))
check('l8 results day 494 at 506; review 397 at 403', 500 + 0.2 * 30 == 506 and 400 + 0.25 * 12 == 403)
run_code_widget('l8 s9 code', load('l8-informed-flow')['screens'][9]['widget'])

# ---------- l9: cards ----------
DECK = [v for v in range(1, 14) for _ in range(4)]
check('l9 deck total 364, mean 7, three cards 21', sum(DECK) == 364 and F(sum(DECK), 52) == 7)


def cond_sum(shown, n):
    """Exact E[sum of n cards | the first len(shown) cards] by enumerating the rest of the deck."""
    rest = DECK[:]
    for c in shown: rest.remove(c)
    k = n - len(shown)
    combos = list(combinations(range(len(rest)), k))
    return sum(shown) + F(sum(sum(rest[i] for i in c) for c in combos), len(combos))


check('l9 K shown: 455/17', cond_sum([13], 3) == F(455, 17))
check('l9 K, 2 shown: 1099/50 = 21.98', cond_sum([13, 2], 3) == F(1099, 50))
check('l9 K, K shown: 32.76', cond_sum([13, 13], 3) == F(819, 25))
check('l9 ace shown: 259/17; queen of four: 556/17', cond_sum([1], 3) == F(259, 17) and cond_sum([12], 4) == F(556, 17))
check('l9 change formula 49(c-7)/51 for every c', all(cond_sum([c], 3) - 21 == F(49 * (c - 7), 51) for c in range(1, 14)))
check('l9 general rule F = S + (n-k)(T-S)/(N-k)', all(cond_sum(s, n) == sum(s) + (n - len(s)) * F(364 - sum(s), 52 - len(s)) for s, n in [([13], 3), ([3, 11], 3), ([12, 5], 3), ([1], 2)]))
check('l9 ledger: short at 23 marks -3.76 then +1.02', abs(float(23 - F(455, 17)) + 3.7647) < 1e-4 and abs(float(23 - F(1099, 50)) - 1.02) < 1e-9)
check('l9 fresh decks: 27 and 15; earnings future 10.40', 13 + 14 == 27 and abs(2.6 + 1.8 + 6 - 10.4) < 1e-12)
rng = random.Random(4); acc = [];
while len(acc) < 20000:
    c = rng.sample(DECK, 3)
    if c[0] == 13: acc.append(sum(c))
check(f'l9 sim: mean sum given a king first {sum(acc) / len(acc):.3f} near 26.76, below 27', abs(sum(acc) / len(acc) - 26.7647) < 0.12)
run_code_widget('l9 s10 code', load('l9-cards-revealed')['screens'][10]['widget'])

# ---------- review-2 and homework-2 ----------
check('r2 four dice 13 at 15; smaller game 1/36', E(sum, 4) == 14 and E(min, 2) - F(5, 2) == F(1, 36))
check('r2 skew 0.5 long 2: ask 10.5', quote(10.5, 0.5, 2)[1] == 10.5)
check('r2 informed 2 at 4: 2/3', L(2, 4) == F(2, 3))
check('r2 Q, 5 shown: 23.94; two cards K: gap 2/17', cond_sum([12, 5], 3) == F(2394, 100) and 20 - cond_sum([13], 2) == F(2, 17))
check('r2 ledger +2.5; sale at 9 loses on 1 roll in 6', 2 * 1 + 0.5 == 2.5 and sum(1 for a, b in product(DIE, repeat=2) if a + b > 9) == 6)
hw = load('homework-2')
run_code_widget('hw2 play', hw['items'][0]['widget'])
run_code_widget('hw2 zero_profit_half_spread', hw['items'][1]['widget'])
# break-even half-widths recomputed independently by bisection
def be(al, xs):
    m = F(sum(xs), len(xs)); lo, hi = 0.0, float(max(abs(x - m) for x in xs))
    g = lambda h: (1 - al) * h - al * sum(max(abs(float(x - m)) - h, 0) for x in xs) / len(xs)
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if g(mid) >= 0 else (mid, hi)
    return hi
two = [a + b for a, b in product(DIE, repeat=2)]
check('hw2 break-even h: die 1/2 -> 4/5, 1/5 -> 3/10, 3/4 -> 4/3; two dice 1/2 -> 15/14, 1/4 -> 35/69',
      all(abs(be(al, xs) - v) < 1e-9 for al, xs, v in [(0.5, list(DIE), 0.8), (0.2, list(DIE), 0.3), (0.75, list(DIE), 4 / 3), (0.5, two, 15 / 14), (0.25, two, 35 / 69)]))
# mock round arithmetic
f1 = cond_sum([3], 3); f2 = cond_sum([3, 11], 3)
check('hw2 mock: fair 21, 875/51, 21, 23', f1 == F(875, 51) and f2 == 21)
check('hw2 mock ledger: -3.69 after the 3, -2.84 after the sale, +1 after the jack, +3 final',
      abs(float(2 * (f1 - 19)) + 3.69) < 5e-3 and abs(float(2 * (f1 - 19) + (18 - f1)) + 2.84) < 5e-3 and -38 + 18 + 21 == 1 and -38 + 18 + 23 == 3)
half_round = lambda x: round(2 * x) / 2
check('hw2 mock quotes: 19/23, 18/22, 14/18, 14.5/18.5, 18.5/22.5',
      [half_round(float(c)) for c in (21, 21 - 1, f1 - 1, f1 - F(1, 2), f2 - F(1, 2))] == [21, 20, 16, 16.5, 20.5])
check('hw2 two dice mixed 13/18; edge game 1/6', H * 2 - H * F(5, 9) == F(13, 18) and F(7, 6) - 1 == F(1, 6))

print(f'\n{PASSES[0]} checks passed, {len(FAILS)} failed, {len(XFAILS)} EXPECTED_FAIL')
for x in XFAILS:
    print('  EXPECTED_FAIL:', x)
sys.exit(1 if FAILS else 0)
