"""Concept audit, conditional level 3 (l13 to l17, review-3, homework-3, problems-3).
Independence, pairwise against mutual, conditional independence and the two-regime default model,
recomputed from explicit joint distributions with exact fractions; seeded Monte Carlo for the
portfolio tail and the large pool; both code solutions executed against their hidden tests.
Run from the repo root:
    python3 docs/reports/conditional-L3-concepts.py
Exit 0 means every claim checked holds. Ledger: docs/reports/audit-conditional-1-3-ledger.md.
"""
import math
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conditional_concepts_lib import cid, cond, eq, get, ok, pr, report, says, tab, wcond, wpr

D = lambda s: F(s)
die = range(1, 7)
two = list(product(die, die))


def indep(space, a, b):
    return pr(space, lambda s: a(s) and b(s)) == pr(space, a) * pr(space, b)


def tail(k, n, p):
    p = F(p)
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))


def run_code(name, path):
    """Solution passes every test; the starter fails at least one. Returns (solution ok, starter fails)."""
    w = get(name, path)['widget']

    def passes(src):
        env = {}
        try:
            exec(src, env)
            return all(math.isclose(float(eval(t['call'], env)), float(t['expect']), rel_tol=1e-9, abs_tol=1e-12) for t in w['tests'])
        except Exception:
            return False
    return passes(w['solution']), not passes(w['starter']), len(w['tests'])


# ---------------------------------------------------------------- l13 when knowing tells you nothing
L = 'l13-knowing-nothing'
A = lambda r: r[0] == 6
tot = lambda n: (lambda r: sum(r) == n)
ok(cond(two, A, tot(7)) == F(1, 6) == pr(two, A), 'l13 s1 a total of 7 leaves a first 6 at 1/6')
cid(L, 'screens[1]', ['same'])
cid(L, 'screens[2]', [f'r{a}c{b}' for a, b in two if a + b == 12])
ok(cond(two, A, tot(12)) == 1 and not indep(two, A, tot(12)), 'l13 s3 a total of 12 makes a first 6 certain: dependent')
cid(L, 'screens[3]', ['no'])
tab(L, 'screens[4]', [pr(two, tot(7)), pr(two, tot(12)), pr(two, A) * pr(two, tot(7)), pr(two, A) * pr(two, tot(12)),
                      pr(two, lambda r: A(r) and sum(r) == 7), pr(two, lambda r: A(r) and sum(r) == 12)], atol=6e-5)
ev = {'second': lambda r: r[1] == 6, 'even': lambda r: sum(r) % 2 == 0, 'atleast': lambda r: 6 in r, 'firsteven': lambda r: r[0] % 2 == 0}
cid(L, 'screens[5]', [k for k, e in ev.items() if indep(two, A, e)])
ok(cond(two, A, ev['atleast']) == F(6, 11) and cond(two, A, ev['firsteven']) == F(1, 3), 'l13 s5 6/11 and 1/3 in the feedback')
C1 = lambda r: r[0] == 1
ok(not indep(two, A, C1) and cond(two, A, C1) == 0, 'l13 s6 disjoint events with positive chances are dependent')
cid(L, 'screens[6]', ['no'])
cid(L, 'screens[7]', ['s1', 's2', 's3', 's4'])
ok([x for x in (F(i, 100) for i in range(0, 101)) if x == x * x] == [0, 1], 'l13 s8 x = x^2 only at 0 and 1')
cid(L, 'screens[8]', ['ends'])
rows = get(L, 'screens[9]')['canvas']['params']['rows']
tally = [sum(1 for r in rows if (r[1], r[2]) == pair) for pair in (('Up', 'Up'), ('Up', 'Down'), ('Down', 'Up'), ('Down', 'Down'))]
ok(len(rows) == 20, 'l13 s9 the table has 20 days')
tab(L, 'screens[9]', tally, atol=0)
eq(L, 'screens[10]', F(tally[0], tally[0] + tally[1]))
ok(F(sum(1 for r in rows if r[2] == 'Up'), 20) == F(1, 2), 'l13 s10 10 of the 20 days were up')
deck = [(r, s) for r in range(13) for s in range(4)]
ok(indep(deck, lambda c: c[0] == 0, lambda c: c[1] == 0), 'l13 quiz0 ace and heart are independent')
cid(L, 'quiz[0]', ['yes'])
eq(L, 'quiz[1]', D('0.4') * D('0.5'))
eq(L, 'quiz[2]', 0, atol=0)
cid(L, 'quiz[3]', ['always'])
# the two tests agree whenever P(B) > 0, on every pair of events of a small space
space = list(range(6))
events = [set(c) for k in range(0, 7) for c in combinations(space, k)]
good = True
for a in events:
    for b in events:
        if b:
            good &= (F(len(a & b), len(b)) == F(len(a), 6)) == (F(len(a & b), 6) == F(len(a), 6) * F(len(b), 6))
ok(good, 'l13 s4 conditional test and product test agree for every pair of events with P(B) > 0 (4,096 pairs)')
ok(F(0, 6) == F(len(events[5]), 6) * 0, 'l13 summary a chance-0 event passes the product test, where P(A | B) is undefined')

# ---------------------------------------------------------------- l14 independent trials
L = 'l14-independent-trials'
eq(L, 'screens[1]', D('0.45') ** 2, atol=1e-6)
eq(L, 'screens[2]', D('0.45') ** 5, atol=6e-5)
ok(54 < 1 / D('0.45') ** 5 < 55 and D('0.45') ** 6 < D('0.01') < D('0.45') ** 5, 'l14 s2 once in 54 runs, below 1% at six trades')
eq(L, 'screens[3]', D('0.55') ** 2 * D('0.45'), atol=6e-5)
paths = list(product('wl', repeat=3))
cid(L, 'screens[4]', ['-'.join(p) for p in paths if p.count('w') == 2])
ok(tail(2, 3, '0.55') - tail(3, 3, '0.55') == 3 * D('0.55') ** 2 * D('0.45'), 'l14 s4 two wins in three is 3 x 0.1361')
cid(L, 'screens[5]', ['right'])
eq(L, 'screens[6]', 1 - D('0.7') ** 3)
cid(L, 'screens[7]', ['zero'])
cid(L, 'screens[8]', ['s1', 's2', 's3', 's4'])
sol, starter_fails, nt = run_code(L, 'screens[9]')
ok(sol and starter_fails, f'l14 s9 code: solution passes {nt} tests and the starter fails')
ok(abs(tail(7, 10, '0.55') - D('0.2660')) < D('0.0001'), 'l14 s9 P(7 or more of 10 at 0.55) = 0.2660')
exact7 = tail(7, 10, '0.55') - tail(8, 10, '0.55')
ok(abs(exact7 - D('0.1665')) < D('0.0001'), 'l14 s9 exactly 7 of 10 has chance 0.1665: "a 70% hit rate about a quarter of the time" is true of 70% or more (finding 17)')
ok(abs(tail(30, 50, '0.5') - D('0.1013')) < D('0.0001'), 'l14 s10 P(30 or more of 50 at 0.5) = 0.1013')
eq(L, 'screens[10]', 20 * tail(30, 50, '0.5'), atol=0.01)
eq(L, 'quiz[0]', F(1, 2) ** 4)
eq(L, 'quiz[1]', 1 - D('0.9') ** 3)
eq(L, 'quiz[2]', 5 * D('0.6') * D('0.4') ** 4, atol=6e-5)
n = 1
while D('0.45') ** n >= D('0.01'):
    n += 1
eq(L, 'quiz[3]', n, atol=0)
rng = random.Random(1410)
hit = sum(1 for _ in range(200000) if sum(rng.random() < 0.55 for _ in range(10)) >= 7)
ok(abs(hit / 200000 - 0.2660) < 0.005, 'l14 s9 Monte Carlo 7 or more wins in 10 about 0.266', f'{hit / 200000:.4f}')
hit = sum(1 for _ in range(100000) if sum(rng.random() < 0.5 for _ in range(50)) >= 30)
ok(abs(hit / 100000 - 0.1013) < 0.005, 'l14 s10 Monte Carlo no-edge 60% backtest about 0.10', f'{hit / 100000:.4f}')

# ---------------------------------------------------------------- l15 pairwise is not enough
L = 'l15-pairwise'
coins = list(product('HT', repeat=2))
a = lambda s: s[0] == 'H'
b = lambda s: s[1] == 'H'
c = lambda s: s[0] == s[1]
d = lambda s: s[0] != s[1]
ok(cond(coins, c, a) == pr(coins, c) == F(1, 2), 'l15 s1 A leaves C at 1/2')
cid(L, 'screens[1]', ['same'])
cid(L, 'screens[2]', ['r0'])
both = [pr(coins, lambda s, x=x, y=y: x(s) and y(s)) for x, y in ((a, b), (a, c), (b, c))]
tab(L, 'screens[3]', [v for j in both for v in (j, F(1, 4))])
ok(all(indep(coins, x, y) for x, y in ((a, b), (a, c), (b, c))), 'l15 s3 A, B, C are pairwise independent')
abc = pr(coins, lambda s: a(s) and b(s) and c(s))
eq(L, 'screens[4]', abc)
ok(abc != F(1, 8), 'l15 s4 the triple is 1/4, not 1/8: not mutually independent')
eq(L, 'screens[5]', cond(coins, c, lambda s: a(s) and b(s)))
cid(L, 'screens[6]', ['right'])
ok(all(indep(coins, x, y) for x, y in ((a, b), (a, d), (b, d))) and pr(coins, lambda s: a(s) and b(s) and d(s)) == 0, 'l15 s6 with "coins differ" every pair passes and the triple is 0')
# finding 18: the pairs do bound the triple. Three events of chance 1/2, pairwise independent: with t = P(all three),
# the eight atoms are t, 1/4 - t (three times), t (three times) and 1/4 - t, so t can be anything in [0, 1/4] and nothing else.
feasible = [t for t in (F(i, 80) for i in range(-10, 60)) if min(t, F(1, 4) - t) >= 0]
ok(min(feasible) == 0 and max(feasible) == F(1, 4), 'l15 s6 pairwise independence at chance 1/2 pins the triple to the range 0 to 1/4 (finding 18)')
cid(L, 'screens[7]', ['eleven'])
ok(sum(comb(4, k) for k in (2, 3, 4)) == 11, 'l15 s7 eleven product equations for four events')
cid(L, 'screens[8]', ['mut', 'null'])
six = list(range(4))
e_a = lambda x: x < 2
ok(pr(six, lambda x: e_a(x) and e_a(x) and False) == pr(six, e_a) * pr(six, e_a) * 0 and not indep(six, e_a, e_a), 'l15 s8 triple equation with a chance-0 event holds while the pair A = B fails')
states = [(1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1)]
ok(all(z == (-1 if x == y else 1) for x, y, z in states), 'l15 s9 Z falls exactly when X and Y move the same way')
eq(L, 'screens[9]', pr(states, lambda s: s == (-1, -1, -1)))
pairs_ok = all(indep(states, lambda s, i=i, u=u: s[i] == u, lambda s, j=j, v=v: s[j] == v) for i, j in ((0, 1), (0, 2), (1, 2)) for u in (1, -1) for v in (1, -1))
corr0 = all(sum(s[i] * s[j] for s in states) == 0 for i, j in ((0, 1), (0, 2), (1, 2)))
ok(pairs_ok and corr0, 'l15 s9 every pair of X, Y, Z is independent with zero correlation')
cid(L, 'screens[10]', ['pairs'])
ok(indep(coins, a, d), 'l15 quiz0 first heads and coins differ are independent')
cid(L, 'quiz[0]', ['yes'])
cid(L, 'quiz[1]', ['four'])
eq(L, 'quiz[2]', cond(coins, d, lambda s: a(s) and b(s)), atol=0)
cid(L, 'quiz[3]', ['yes'])

# ---------------------------------------------------------------- l16 conditional independence
L = 'l16-conditional-independence'
sector = {}
for g, pa in (('good', D('0.8')), ('bad', D('0.2'))):
    for ua in (1, 0):
        for ub in (1, 0):
            sector[(g, ua, ub)] = F(1, 2) * (pa if ua else 1 - pa) * (pa if ub else 1 - pa)
upA = lambda s: s[1] == 1
upB = lambda s: s[2] == 1
good = lambda s: s[0] == 'good'
ok(wcond(sector, upB, upA) > wpr(sector, upB) == F(1, 2), 'l16 s1 A rising lifts B above 0.5')
cid(L, 'screens[1]', ['rises'])
cid(L, 'screens[2]', ['g-u-u', 'b-u-u'])
eq(L, 'screens[3]', wcond(sector, upB, upA))
tab(L, 'screens[4]', [wcond(sector, upA, good) * wcond(sector, upB, good), wpr(sector, upA) * wpr(sector, upB),
                      wcond(sector, lambda s: upA(s) and upB(s), good), wpr(sector, lambda s: upA(s) and upB(s))])
eq(L, 'screens[5]', wcond(sector, upB, lambda s: good(s) and upA(s)))
eq(L, 'screens[6]', wpr(sector, lambda s: upA(s) and upB(s)))
alert = {(1, 1): D('0.02'), (1, 0): D('0.18'), (0, 1): D('0.08'), (0, 0): D('0.72')}
fires = lambda s: s[0] or s[1]
ok(wpr(alert, lambda s: s[0] and s[1]) == wpr(alert, lambda s: s[0]) * wpr(alert, lambda s: s[1]), 'l16 s7 news and the market drop are independent in the table')
eq(L, 'screens[7]', wcond(alert, lambda s: s[0], fires))
ok(wcond(alert, lambda s: s[0], lambda s: fires(s) and s[1]) == D('0.2'), 'l16 s8 given the alert and the drop, news is back at 0.2')
cid(L, 'screens[8]', ['right'])
cid(L, 'screens[9]', ['s1', 's2', 's3', 's4'])
an = {}
for beat, pb, q in ((1, D('0.4'), D('0.75')), (0, D('0.6'), D('0.25'))):
    for x in (1, 0):
        for y in (1, 0):
            an[(beat, x, y)] = pb * (q if x else 1 - q) * (q if y else 1 - q)
eq(L, 'screens[10]', wcond(an, lambda s: s[2] == 1, lambda s: s[1] == 1))
cid(L, 'quiz[0]', ['no'])
eq(L, 'quiz[1]', D('0.6') * D('0.5'))
cid(L, 'quiz[2]', ['falls'])
coin = {(k, t1, t2): F(1, 2) * (h if t1 else 1 - h) * (h if t2 else 1 - h) for k, h in (('fair', F(1, 2)), ('two', F(1))) for t1 in (1, 0) for t2 in (1, 0)}
eq(L, 'quiz[3]', wcond(coin, lambda s: s[2] == 1, lambda s: s[1] == 1))
# explaining away holds for any independent causes of an either-or effect (quiz2), random search
rng = random.Random(16)
okay = True
for _ in range(20000):
    p, q = rng.uniform(0.01, 0.99), rng.uniform(0.01, 0.99)
    okay &= p / (1 - (1 - p) * (1 - q)) > p - 1e-12          # P(cause 1 | effect) > P(cause 1 | effect, cause 2) = p
ok(okay, 'l16 quiz2 learning the other cause lowers the first back to its prior, for every pair of chances')
# finding 19: conditioning on a shared effect does not always link its causes. Effect fires with chance f(a) g(b):
causes = {}
fa, gb = {1: D('0.9'), 0: D('0.3')}, {1: D('0.8'), 0: D('0.4')}
for x in (1, 0):
    for y in (1, 0):
        for e in (1, 0):
            pe_ = fa[x] * gb[y]
            causes[(x, y, e)] = F(1, 4) * (pe_ if e else 1 - pe_)
given_e = lambda s: s[2] == 1
lhs = wcond(causes, lambda s: s[0] == 1 and s[1] == 1, given_e)
rhs = wcond(causes, lambda s: s[0] == 1, given_e) * wcond(causes, lambda s: s[1] == 1, given_e)
ok(lhs == rhs, 'l16 s8 an effect with chance f(a) g(b) leaves its causes independent given the effect, so "links its causes" needs "can" (finding 19)')

# ---------------------------------------------------------------- l17 correlated defaults
L = 'l17-correlated-defaults'


def book(k, n, q, pb, pg):
    return F(q) * tail(k, n, pb) + (1 - F(q)) * tail(k, n, pg)


def bars(q, pb=D('0.2'), mean=D('0.05'), n=10):
    q = F(q)
    pg = (mean - q * pb) / (1 - q)
    exact = lambda k, p: comb(n, k) * p ** k * (1 - p) ** (n - k)
    v = [q * exact(k, pb) + (1 - q) * exact(k, pg) for k in (0, 1, 2)]
    return v + [1 - sum(v)]


ind = bars(0)
ok([round(float(x), 4) for x in ind] == [0.5987, 0.3151, 0.0746, 0.0115], 'l17 s1 independent bars 0.5987, 0.3151, 0.0746, 0.0115')
cid(L, 'screens[1]', ['rises'])
at2 = bars('0.2')
ok([round(float(x), 4) for x in at2] == [0.7269, 0.143, 0.0655, 0.0646], 'l17 s2 bars at a recession chance of 0.2')
qs = [F(i, 100) for i in range(0, 26)]
zero_bar = [bars(q)[0] for q in qs]
tail_bar = [bars(q)[3] for q in qs]
ok(all(x < y for x, y in zip(zero_bar, zero_bar[1:])) and all(x < y for x, y in zip(tail_bar, tail_bar[1:])), 'l17 s2 both end bars rise all the way as the recession chance goes from 0 to 0.25')
cid(L, 'screens[2]', ['both'])
eq(L, 'screens[3]', D('0.2') * D('0.2') + D('0.8') * D('0.0125'))
eq(L, 'screens[4]', book(2, 2, '0.2', '0.2', '0.0125'), atol=1e-6)
ok(book(2, 2, '0.2', '0.2', '0.0125') / D('0.0025') > 3, 'l17 s4 more than three times the independent 0.0025')
ok(round(float(tail(3, 10, '0.2')), 4) == 0.3222 and round(float(tail(3, 10, '0.0125')), 4) == 0.0002, 'l17 s5 regime tails 0.3222 and 0.0002')
eq(L, 'screens[5]', book(3, 10, '0.2', '0.2', '0.0125'), atol=1e-4)
ok(abs(book(3, 10, '0.2', '0.2', '0.0125') / tail(3, 10, '0.05') - D('5.6')) < D('0.05'), 'l17 s5 5.6 times the independent tail')
cid(L, 'screens[6]', ['right'])
eq(L, 'screens[7]', D('0.05'))
cid(L, 'screens[8]', ['cond'])
sol, starter_fails, nt = run_code(L, 'screens[9]')
ok(sol and starter_fails, f'l17 s9 code: solution passes {nt} tests and the starter fails')
cid(L, 'screens[10]', ['right'])
cid(L, 'quiz[0]', ['y'])
# Jensen: mixing the default chance always raises P(no defaults) and, for regime chances up to 2/9, the tail of 3 or more
rng = random.Random(17)
okay0 = okay3 = True
for _ in range(4000):
    q, pb = rng.uniform(0.02, 0.9), rng.uniform(0.051, 0.22)
    pg = (0.05 - q * pb) / (1 - q)
    if pg < 0:
        continue
    okay0 &= q * (1 - pb) ** 10 + (1 - q) * (1 - pg) ** 10 >= 0.95 ** 10 - 1e-12
    okay3 &= q * float(tail(3, 10, F(pb).limit_denominator(10 ** 6))) + (1 - q) * float(tail(3, 10, F(pg).limit_denominator(10 ** 6))) >= float(tail(3, 10, '0.05')) - 1e-9
ok(okay0, 'l17 quiz0 a shared factor with the same mean always makes a year with no defaults likelier')
ok(okay3, 'l17 s1 a shared factor with the same mean raises P(3 or more) for every regime pair tried')
eq(L, 'quiz[1]', D('0.5') * D('0.08') + D('0.5') * D('0.02'))
eq(L, 'quiz[2]', book(2, 2, '0.5', '0.08', '0.02'), atol=1e-6)
cid(L, 'quiz[3]', ['rec'])
rng = random.Random(1717)
big = 0
runs = 4000
for _ in range(runs):
    p = 0.2 if rng.random() < 0.2 else 0.0125
    big += sum(rng.random() < p for _ in range(2000)) >= 200
ok(abs(big / runs - 0.2) < 0.025, 'l17 quiz3 Monte Carlo: a pool of 2,000 loans loses 10% or more in about 0.2 of years', f'{big / runs:.3f}')
three = 0
runs = 400000
for _ in range(runs):
    p = 0.2 if rng.random() < 0.2 else 0.0125
    three += sum(rng.random() < p for _ in range(10)) >= 3
ok(abs(three / runs - 0.0646) < 0.002, 'l17 s5 Monte Carlo 3 or more defaults about 0.0646', f'{three / runs:.4f}')

# ---------------------------------------------------------------- review-3
L = 'review-3'
ok(cond(two, lambda r: r[0] % 2 == 0, tot(8)) == F(3, 5) and not indep(two, lambda r: r[0] % 2 == 0, tot(8)), 'review-3 r-total-eight 3/5, dependent')
cid(L, 'items[0]', ['no'])
eq(L, 'items[1]', 0, atol=0)
eq(L, 'items[2]', 1 - D('0.8') ** 4)
eq(L, 'items[3]', comb(4, 2) * D('0.6') ** 2 * D('0.4') ** 2)
cid(L, 'items[4]', ['no'])
eq(L, 'items[5]', 250 * pr(states, lambda s: s == (-1, -1, -1)), atol=0.01)
sym = {}
for dis, pd, ps in ((1, D('0.1'), D('0.9')), (0, D('0.9'), D('0.2'))):
    for x in (1, 0):
        for y in (1, 0):
            sym[(dis, x, y)] = pd * (ps if x else 1 - ps) * (ps if y else 1 - ps)
eq(L, 'items[6]', wcond(sym, lambda s: s[2] == 1, lambda s: s[1] == 1))
call = {(x, y): (D('0.3') if x else D('0.7')) * (D('0.5') if y else D('0.5')) for x in (1, 0) for y in (1, 0)}
ok(wcond(call, lambda s: s[0], lambda s: s[0] or s[1]) == D('0.3') / D('0.65'), 'review-3 r-alarm P(A bad | call) = 0.3/0.65')
eq(L, 'items[7]', wcond(call, lambda s: s[0], lambda s: (s[0] or s[1]) and s[1]))
eq(L, 'items[8]', book(2, 2, '0.1', '0.3', '0.02'), atol=1e-6)
ok(4 < book(2, 2, '0.1', '0.3', '0.02') / D('0.048') ** 2 < D('4.1'), 'review-3 r-two-loans four times the independent product')

# ---------------------------------------------------------------- homework-3
L = 'homework-3'
ok(F(33, 60) == F(77, 140) == F(110, 200), 'homework-3 h-signal-table the up share is 0.55 either way')
cid(L, 'items[0]', ['yes'])
eq(L, 'items[1]', D('0.7') ** 12, atol=6e-6)
n = 1
while 1 - D('0.45') ** n < D('0.999'):
    n += 1
eq(L, 'items[2]', n, atol=0)
zf = lambda s: s[2] == -1
want = []
if cond(states, zf, lambda s: s[0] == -1) == F(1, 2): want.append('zx')
if cond(states, zf, lambda s: s[0] == -1 and s[1] == -1) == 1: want.append('zxy')
if pr(states, lambda s: s == (-1, -1, -1)) == F(1, 8): want.append('mutual')
if pr(states, lambda s: s == (1, 1, 1)) == F(1, 8): want.append('allup')
cid(L, 'items[3]', want)
eq(L, 'items[4]', wcond(an, lambda s: s[0] == 1, lambda s: s[1] == 1 and s[2] == 1))
ok(D('0.1') * D('0.32') + D('0.9') * D('0.02') == D('0.05'), 'homework-3 h-book-five each loan alone is 0.05')
eq(L, 'items[5]', book(2, 5, '0.1', '0.32', '0.02'))
cid(L, 'items[6]', ['s1', 's2', 's3', 's4', 's5'])
rng = random.Random(33)
okay = True
for _ in range(20000):
    q, pb, pg = (F(rng.randint(0, 100), 100) for _ in range(3))
    okay &= q * pb ** 2 + (1 - q) * pg ** 2 - (q * pb + (1 - q) * pg) ** 2 == q * (1 - q) * (pb - pg) ** 2
ok(okay, 'homework-3 h-long-factor identity q(1-q)(pb-pg)^2 holds exactly on 20,000 random rates')
ok(D('0.2') * D('0.8') * D('0.1875') ** 2 == D('0.005625') == D('0.008125') - D('0.0025') and says(L, 'items[7].model', '0.005625'), 'homework-3 h-long-factor part (d) 0.005625')

# ---------------------------------------------------------------- problems-3
L = 'problems-3'
eq(L, 'items[0].parts[0]', F(78, 120))
ok(F(78, 120) == F(260, 400) and F(120, 400) * F(260, 400) == F(78, 400), 'problems-3 gap days: both tests pass')
cid(L, 'items[0].parts[1]', ['yes'])
eq(L, 'items[0].parts[2]', tail(3, 4, '0.65') - tail(4, 4, '0.65'))
eq(L, 'items[0].parts[3]', 1 - D('0.65') ** 4)
week = {(x, y): (D('0.3') if x else D('0.7')) * (D('0.25') if y else D('0.75')) for x in (1, 0) for y in (1, 0)}
loss = lambda s: s[0] or s[1]
eq(L, 'items[1].parts[0]', wpr(week, loss))
eq(L, 'items[1].parts[1]', wcond(week, lambda s: s[0], loss))
eq(L, 'items[1].parts[2]', wcond(week, lambda s: s[0], lambda s: loss(s) and s[1]))
cid(L, 'items[1].parts[3]', ['no'])
eq(L, 'items[2].parts[0]', D('0.25') * D('0.28') + D('0.75') * D('0.04'))
eq(L, 'items[2].parts[1]', book(3, 3, '0.25', '0.28', '0.04'), atol=1e-6)
eq(L, 'items[2].parts[2]', D('0.1') ** 3, atol=1e-7)
eq(L, 'items[2].parts[3]', book(3, 3, '0.25', '0.28', '0.04') / D('0.1') ** 3, atol=1e-6)
feeds = list(product((0, 1), repeat=3))                    # F, G, H
dA = lambda s: s[0] == s[1]                                  # desk 1 reads F and G
dB = lambda s: s[0] == s[2]                                  # desk 2 reads F and H
dC = lambda s: s[1] == s[2]                                  # desk 3 reads G and H
eq(L, 'items[3].parts[0]', cond(feeds, dC, dA))
ok(all(indep(feeds, x, y) for x, y in ((dA, dB), (dA, dC), (dB, dC))), 'problems-3 desks: every pair is independent')
cid(L, 'items[3].parts[1]', ['pairwise'])
triple = pr(feeds, lambda s: dA(s) and dB(s) and dC(s))
eq(L, 'items[3].parts[2]', triple)
eq(L, 'items[3].parts[3]', cond(feeds, dC, lambda s: dA(s) and dB(s)))
eq(L, 'items[3].parts[4]', 1 - (1 - triple) ** 8)

# finding 22 (wrong): the lesson 16 summary trap prescribes the junior analyst's method. This check fails until the text is fixed.
add_then_multiply = wpr(sector, upA) * wpr(sector, upB)                       # weight each branch and add, then multiply: 0.25
multiply_then_add = wpr(sector, lambda s: upA(s) and upB(s))                # multiply inside each branch, then weight and add: 0.34
backwards = says('l16-conditional-independence', 'summary.trap', 'Weight each branch and add before you multiply anything')
ok(add_then_multiply == D('0.25') and multiply_then_add == D('0.34') and not backwards, 'l16 summary.trap names the right order of steps (finding 22)',
   'adding before multiplying gives 0.25, the trap answer; the true 0.34 multiplies inside each branch first')

report('conditional L3 concepts')
