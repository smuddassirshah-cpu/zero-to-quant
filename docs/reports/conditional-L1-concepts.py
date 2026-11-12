"""Concept audit, conditional level 1 (l1 to l6, review-1, homework-1, problems-1).
Every probability the level grades or states, recomputed by exact enumeration, plus seeded
Monte Carlo runs for the simulation screen and the protocol finding. Run from the repo root:
    python3 docs/reports/conditional-L1-concepts.py
Exit 0 means every claim checked holds. Ledger: docs/reports/audit-conditional-1-3-ledger.md.
"""
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations, permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conditional_concepts_lib import cid, cond, eq, get, ok, pr, report, says, tab

die = list(range(1, 7))
two = list(product(die, die))
even = lambda x: x % 2 == 0

# ---------------------------------------------------------------- l1 what changes
L = 'l1-what-changes'
ok(cond(die, lambda x: x == 6, even) > pr(die, lambda x: x == 6), 'l1 s1 a 6 is more likely given even')
cid(L, 'screens[1]', ['more'])
cid(L, 'screens[2]', [f'r1c{x}' for x in die if even(x)])
eq(L, 'screens[3]', cond(die, lambda x: x == 6, even))
ok(cond(die, lambda x: x == 6, even) == 2 * F(1, 6), 'l1 s3 the news doubled the chance')
eq(L, 'screens[4]', cond(die, even, lambda x: x > 3))
eq(L, 'screens[5]', cond(die, lambda x: x == 1, lambda x: x > 3))
ok(cond(die, even, lambda x: x <= 4) == pr(die, even), 'l1 s6 at most 4 leaves even at 1/2')
cid(L, 'screens[6]', ['same'])
days = ['hv-up'] * 56 + ['hv-not'] * 24 + ['nv-up'] * 64 + ['nv-not'] * 56
ok(len(days) == 200, 'l1 s8 200 days')
eq(L, 'screens[8]', cond(days, lambda d: d.endswith('up'), lambda d: d.startswith('hv')))
ok(pr(days, lambda d: d.endswith('up')) == F(3, 5), 'l1 s8 all days 0.6')
deck = [(r, s) for r in range(1, 14) for s in 'HDCS']
eq(L, 'quiz[0]', cond(deck, lambda c: c[1] == 'H', lambda c: c[1] in 'HD'))
eq(L, 'quiz[1]', cond(die, lambda x: x == 6, lambda x: x >= 3))
eq(L, 'quiz[2]', cond(die, lambda x: x <= 3, lambda x: x % 2 == 1))

# ---------------------------------------------------------------- l2 counting what is left
L = 'l2-counting-left'
bag = ['R1', 'R2', 'R3', 'B1', 'B2']
draws = list(permutations(bag, 2))
red = lambda c: c[0] == 'R'
ok(len(draws) == 20, 'l2 20 ordered pairs')
eq(L, 'screens[1]', cond(draws, lambda d: red(d[1]), lambda d: red(d[0])))
ok(len(get(L, 'screens[2]')['widget']['answer']) == sum(1 for d in draws if red(d[0]) and red(d[1])), 'l2 s2 six both-red pairs')
eq(L, 'screens[3]', cond(draws, lambda d: red(d[1]), lambda d: red(d[0])))
eq(L, 'screens[4]', cond(draws, lambda d: red(d[1]), lambda d: not red(d[0])))
eq(L, 'screens[5]', pr(draws, lambda d: red(d[0]) and red(d[1])))
eq(L, 'screens[6]', pr(draws, lambda d: red(d[1])))
ok(pr(draws, lambda d: red(d[1])) == pr(draws, lambda d: red(d[0])), 'l2 s6 unseen first draw: second draw has the first draw chance')
ok(pr(draws, lambda d: not red(d[0]) and not red(d[1])) == F(2, 5) * F(1, 4), 'l2 s7 blue then blue is 2/5 x 1/4')
cid(L, 'screens[7]', ['right'])
eq(L, 'screens[8]', cond(draws, lambda d: red(d[1]), lambda d: red(d[0])))
stocks = ['W'] * 4 + ['L'] * 6
picks = list(permutations(range(10), 2))
eq(L, 'screens[9]', pr(picks, lambda p: stocks[p[0]] == 'W' and stocks[p[1]] == 'W'))
chips = list(permutations(['G'] * 4 + ['X'] * 2, 2))
chips = list(permutations(range(6), 2))
bad = lambda i: i >= 4
eq(L, 'quiz[0]', cond(chips, lambda p: bad(p[1]), lambda p: bad(p[0])))
cards2 = list(permutations(range(52), 2))
ace = lambda i: i < 4
eq(L, 'quiz[1]', pr(cards2, lambda p: ace(p[0]) and ace(p[1])), atol=1e-5)
eq(L, 'quiz[2]', pr(draws, lambda d: not red(d[1])))
# Monte Carlo: an unseen first draw leaves the second at 3/5 (200,000 runs, se about 0.0011)
rng = random.Random(1501)
hits = 0
for _ in range(200000):
    a, b = rng.sample(bag, 2)
    hits += red(b)
ok(abs(hits / 200000 - 0.6) < 0.006, 'l2 s6 Monte Carlo second draw red about 0.6', f'{hits / 200000:.4f}')

# ---------------------------------------------------------------- l3 shrinking the sample space
L = 'l3-shrinking'
tot = lambda n: (lambda r: r[0] + r[1] == n)
has = lambda n: (lambda r: n in r)
ok(len(get(L, 'screens[1]')['widget']['answer']) == sum(1 for r in two if tot(8)(r)) == 5, 'l3 s1 five ways to make 8')
eq(L, 'screens[2]', cond(two, tot(8), lambda r: r[0] == 5))
eq(L, 'screens[3]', sum(1 for r in two if has(5)(r)), atol=0)
eq(L, 'screens[4]', cond(two, tot(10), has(5)))
ok(pr(two, tot(10)) == F(1, 12), 'l3 s4 before the news 3/36')
ok(abs(get(L, 'screens[6]')['widget']['answer'] - 1000 * F(11, 36)) <= 1, 'l3 s6 about 305.6 of 1,000 survive')
four = list(product('UD', repeat=2))
eq(L, 'screens[7]', cond(four, lambda s: s == ('U', 'U'), lambda s: 'U' in s))
eq(L, 'quiz[0]', cond(two, has(3), tot(7)))
ok(cond(two, tot(7), has(3)) == F(2, 11), 'l3 quiz0 reversed option is 2/11')
eq(L, 'quiz[1]', cond(die, lambda x: x > 3, even))
eq(L, 'quiz[2]', cond(four, lambda s: s == ('U', 'U'), lambda s: s[0] == 'U'))
# Monte Carlo of the filter screen (the canvas runs the same experiment with its own seed)
rng = random.Random(4226)
kept = sum(1 for _ in range(360000) if 5 in (rng.randint(1, 6), rng.randint(1, 6)))
ok(abs(kept / 360000 - 11 / 36) < 0.004, 'l3 s6 Monte Carlo share kept about 11/36', f'{kept / 360000:.4f}')
# Protocol (finding 1). The key 1/11 is the event reading: the friend answers "is there at least one 5?".
# If instead the friend looks at one die chosen at random and reports its face, a report of 5 gives 1/6,
# the value of the wrong option "fixed-die". Both are enumerated exactly; the item states neither protocol.
num = F(0)
den = F(0)
for r in two:
    for shown in (0, 1):                      # each die equally likely to be the one reported
        w = F(1, 36) * F(1, 2)
        if r[shown] == 5:
            den += w
            num += w if sum(r) == 10 else 0
ok(num / den == F(1, 6), 'l3 s4 report-a-random-die protocol gives 1/6, the fixed-die option (finding 1)')
ok(cond(two, tot(10), has(5)) == F(1, 11), 'l3 s4 yes-or-no question protocol gives 1/11, the key')
rng = random.Random(77)
n5 = t10 = 0
for _ in range(600000):
    r = (rng.randint(1, 6), rng.randint(1, 6))
    if r[rng.randint(0, 1)] == 5:
        n5 += 1
        t10 += sum(r) == 10
ok(abs(t10 / n5 - 1 / 6) < 0.006, 'l3 s4 Monte Carlo of the report protocol about 1/6', f'{t10 / n5:.4f}')
# same protocol, two stocks: "at least one finished up" told by naming a random stock that is up gives 1/2
num = den = F(0)
for s in four:
    for shown in (0, 1):
        w = F(1, 8)
        if s[shown] == 'U':
            den += w
            num += w if s == ('U', 'U') else 0
ok(num / den == F(1, 2), 'l3 s7 report protocol gives 1/2, the known-stock option (finding 2)')

# ---------------------------------------------------------------- l4 multiplication rule
L = 'l4-multiplication-rule'
small = ['h2', 'h5', 'h9', 'hj', 's3', 's8']
heart = lambda c: c[0] == 'h'
d2 = list(permutations(small, 2))
d3 = list(permutations(small, 3))
cid(L, 'screens[1]', [c for c in small if heart(c) and c != 'h9'])
cid(L, 'screens[2]', [c for c in small if heart(c)])
eq(L, 'screens[3]', pr(d2, lambda d: heart(d[0]) and heart(d[1])))
eq(L, 'screens[4]', pr(d3, lambda d: all(heart(c) for c in d)))
eq(L, 'screens[5]', F(4, 6) ** 2)
eq(L, 'screens[6]', pr(d2, lambda d: heart(d[0]) and heart(d[1])))
ok(pr(d2, lambda d: heart(d[1])) == F(4, 6), 'l4 s6 second card alone is a heart 4/6 of the time')
ok(pr(d3, lambda d: heart(d[0]) and not heart(d[1]) and heart(d[2])) == F(4, 6) * F(2, 5) * F(3, 4) == F(1, 5), 'l4 s7 heart, spade, heart is 1/5')
cid(L, 'screens[7]', ['right'])
A = lambda d: heart(d[0])
B = lambda d: not heart(d[1])
eq(L, 'screens[8]', cond(d2, A, B))
ok(pr(d2, A) * cond(d2, B, A) == pr(d2, B) * cond(d2, A, B) == F(8, 30), 'l4 s8 both orders give 8/30')
eq(L, 'screens[9]', F(4, 10) * F(6, 10))
ok(abs((0.24 - 0.16) / 0.24 - 1 / 3) < 1e-9, 'l4 s9 0.16 understates 0.24 by a third')
loans = list(permutations(range(12), 2))
eq(L, 'quiz[0]', pr(loans, lambda p: p[0] < 3 and p[1] < 3), atol=6e-5)
ranks = [i % 13 for i in range(52)]
ok(abs(pr(cards2, lambda p: ranks[p[0]] == 0 and ranks[p[1]] == 12) - F(4, 663)) == 0, 'l4 quiz1 ace then king is 4/663')
eq(L, 'quiz[1]', F(4, 663), atol=1e-6)
eq(L, 'quiz[2]', F(1, 4) ** 2)
rota = list(permutations(range(5), 3))
eq(L, 'quiz[3]', pr(rota, lambda p: all(i < 3 for i in p)))

# ---------------------------------------------------------------- l5 trees
L = 'l5-trees'
socks = list(permutations(['b'] * 5 + ['w'] * 3, 2))
socks = list(permutations(range(8), 2))
blk = lambda i: i < 5
tab(L, 'screens[1]', [cond(socks, lambda p: blk(p[1]), lambda p: blk(p[0])), cond(socks, lambda p: not blk(p[1]), lambda p: blk(p[0])),
                      cond(socks, lambda p: blk(p[1]), lambda p: not blk(p[0])), cond(socks, lambda p: not blk(p[1]), lambda p: not blk(p[0]))])
eq(L, 'screens[3]', pr(socks, lambda p: not blk(p[0]) and not blk(p[1])))
leaves = [pr(socks, lambda p, a=a, b=b: blk(p[0]) == a and blk(p[1]) == b) for a in (True, False) for b in (True, False)]
tab(L, 'screens[4]', leaves + [sum(leaves)])
one_white = list(permutations(range(6), 2))
ok(pr(one_white, lambda p: p[0] == 5 and p[1] == 5) == 0, 'l5 s5 white then white has chance 0')
cid(L, 'screens[5]', ['w-w'])
s3 = list(permutations(range(8), 3))
eq(L, 'screens[6]', pr(s3, lambda p: blk(p[0]) and blk(p[1]) and not blk(p[2])))
eq(L, 'screens[7]', pr(socks, lambda p: blk(p[0]) and not blk(p[1])))
ok(F(25 + 15 + 15 + 9, 64) == 1, 'l5 s7 Kim leaves add to 1 although the tree is wrong')
cid(L, 'screens[8]', ['right'])
ok(pr(socks, lambda p: blk(p[1])) == F(5, 8), 'l5 s8 with no news a black second sock is 5/8')
eq(L, 'screens[10]', F(6, 10) * F(45, 100))
eq(L, 'quiz[0]', F(8, 100) * F(5, 100), atol=1e-6)
eq(L, 'quiz[1]', F(12, 51))
eq(L, 'quiz[2]', 1 - F(42, 100) - F(18, 100) - F(28, 100))
rb = list(permutations(range(4), 2))
ok(pr(rb, lambda p: p[0] == 3 and p[1] == 3) == 0, 'l5 quiz3 blue then blue is 0')
cid(L, 'quiz[3]', ['right'])

# ---------------------------------------------------------------- l6 adding branches
L = 'l6-adding-branches'
red_two = F(1, 3) * F(3, 4) + F(2, 3) * F(1, 4)
cid(L, 'screens[1]', ['a-r', 'b-r'])
ok(min(a * F(3, 4) + (1 - a) * F(1, 4) for a in (F(0), F(1))) == F(1, 4) and max(a * F(3, 4) + (1 - a) * F(1, 4) for a in (F(0), F(1))) == F(3, 4), 'l6 s2 chance of red runs from 1/4 to 3/4')
cid(L, 'screens[2]', ['right'])
eq(L, 'screens[3]', red_two)
eq(L, 'screens[4]', F(1, 6) * 1 + F(2, 6) * F(2, 4) + F(3, 6) * F(1, 4))
eq(L, 'screens[5]', F(1, 6) * F(1, 4) + F(2, 6) * F(2, 8) + F(3, 6) * F(3, 12))
eq(L, 'screens[6]', F(8, 10) * F(1, 100) + F(2, 10) * F(6, 100))
cid(L, 'screens[7]', ['right'])
eq(L, 'screens[9]', F(7, 10) * F(4, 10) + F(3, 10) * F(8, 10))
eq(L, 'quiz[0]', F(5, 10) * F(1, 100) + F(3, 10) * F(3, 100) + F(2, 10) * F(10, 100), atol=1e-5)
ok(F(2, 10) * F(10, 100) / F(34, 1000) > F(1, 2), 'l6 quiz0 grade C brings more than half the defaults')
eq(L, 'quiz[1]', F(1, 10) * F(9, 10) + F(9, 10) * F(2, 10))
ok(F(18, 100) / F(27, 100) == F(2, 3), 'l6 quiz1 two thirds of flags come on days with no drop')
eq(L, 'quiz[2]', F(3, 10))
eq(L, 'quiz[3]', pr(cards2, lambda p: p[1] % 4 == 0))
# a weighted average of conditional chances lies between the smallest and the largest (summary), random search
rng = random.Random(6)
good = True
for _ in range(20000):
    k = rng.randint(2, 5)
    w = [rng.random() for _ in range(k)]
    w = [x / sum(w) for x in w]
    c = [rng.random() for _ in range(k)]
    tp = sum(a * b for a, b in zip(w, c))
    good &= min(c) - 1e-12 <= tp <= max(c) + 1e-12
ok(good, 'l6 summary total probability lies between the smallest and largest conditional chance')

# ---------------------------------------------------------------- review-1
L = 'review-1'
eq(L, 'items[0]', cond(die, lambda x: x == 6, even))
l10 = list(permutations(range(10), 2))
eq(L, 'items[1]', pr(l10, lambda p: p[0] >= 2 and p[1] >= 2))
eq(L, 'items[2]', cond(two, lambda r: r[1] == 6, lambda r: r[0] == 4))
c3 = list(product('HT', repeat=3))
eq(L, 'items[3]', cond(c3, lambda s: s.count('H') == 3, lambda s: s.count('H') >= 2))
eq(L, 'items[4]', cond(cards2, lambda p: ranks[p[1]] == 12, lambda p: ranks[p[0]] == 12))
eq(L, 'items[5]', F(15, 100) * F(12, 100))
eq(L, 'items[6]', cond(two, lambda r: even(r[0]), tot(9)))
r8 = list(permutations(range(8), 2))
eq(L, 'items[7]', pr(r8, lambda p: p[0] < 5 and p[1] < 5))
eq(L, 'items[8]', pr(draws, lambda d: not red(d[1])))
eq(L, 'items[9]', F(4, 10) * F(3, 10) + F(6, 10) * F(1, 10))
# r-two-heads under a report protocol: a random pair of coins is shown and both are heads -> 1/2, the third-coin option
num = den = F(0)
for s in c3:
    for pair in combinations(range(3), 2):
        if all(s[i] == 'H' for i in pair):
            den += 1
            num += s.count('H') == 3
ok(num / den == F(1, 2), 'review-1 r-two-heads show-two-coins protocol gives 1/2, the third-coin option (finding 4)')

# ---------------------------------------------------------------- homework-1
L = 'homework-1'
eq(L, 'items[0]', cond(two, lambda r: r[0] == r[1], lambda r: sum(r) >= 10))
eq(L, 'items[1]', cond(cards2, lambda p: p[1] % 4 == 0, lambda p: p[0] % 4 == 0))
eq(L, 'items[2]', cond(two, lambda r: r == (6, 6), has(6)), atol=6e-5)
A6 = lambda r: r[0] == 6
want = []
if cond(two, A6, tot(7)) == F(1, 6): want.append('a')
if cond(two, A6, tot(8)) == F(1, 6): want.append('b')
if cond(two, tot(8), A6) == F(1, 6): want.append('c')
if cond(two, A6, tot(8)) == cond(two, tot(8), A6): want.append('d')
if cond(two, tot(7), tot(8)) == 0: want.append('e')
cid(L, 'items[3]', want)
eq(L, 'items[4]', F(13, 52) * F(12, 51) * F(11, 50), atol=6e-6)
eq(L, 'items[5]', F(35, 100) * F(55, 100) ** 2, atol=1e-6)
hands = list(combinations(range(52), 3))
eq(L, 'items[6]', cond(hands, lambda h: all(ace(i) for i in h), lambda h: any(ace(i) for i in h)), atol=1e-6)
ok(sum(1 for h in hands if any(ace(i) for i in h)) == 4804, 'homework-1 h-aces 4,804 hands hold an ace')
cid(L, 'items[7]', ['s1', 's2', 's3', 's4'])
paths = [F(5, 100) * F(2, 1000), F(85, 100) * F(1, 100), F(10, 100) * F(8, 100)]
tab(L, 'items[8]', paths + [sum(paths)], atol=1e-6)
ok(F(4, 10) < paths[2] / sum(paths) < F(1, 2), 'homework-1 h-credit-paths downgrade path brings almost half the default risk')
eq(L, 'items[9]', (F(33, 1000) - F(6, 10) * F(15, 1000)) / F(4, 10))
# h-weighted: which statements hold for every P(A) in (0,1)? random search for counterexamples
rng = random.Random(11)
between = equal = True
plain_sum = plain_avg = True
for _ in range(50000):
    p, x, y = rng.uniform(0.01, 0.99), rng.random(), rng.random()
    pb = p * x + (1 - p) * y
    between &= min(x, y) - 1e-12 <= pb <= max(x, y) + 1e-12
    plain_sum &= abs(pb - (x + y)) < 1e-9
    plain_avg &= abs(pb - (x + y) / 2) < 1e-9
    z = rng.random()
    equal &= abs(p * z + (1 - p) * z - z) < 1e-12
cid(L, 'items[10]', [i for i, t in (('between', between), ('equal', equal), ('sum', plain_sum), ('average', plain_avg)) if t])
ok(pr(draws, lambda d: not red(d[1])) == F(2, 5) and says(L, 'items[11]', '\\tfrac{2}{5}'), 'homework-1 h-long-total second counter blue is 2/5')

# ---------------------------------------------------------------- problems-1
L = 'problems-1'
d8 = list(product(range(1, 9), repeat=2))
eq(L, 'items[0].parts[0]', pr(d8, tot(10)))
eq(L, 'items[0].parts[1]', cond(d8, tot(10), has(8)))
eq(L, 'items[0].parts[2]', cond(d8, has(8), tot(10)))
eq(L, 'items[0].parts[3]', pr(d8, lambda r: sum(r) == 10 and 8 in r))
w3 = list(permutations(range(9), 3))
bank = lambda i: i < 5
eq(L, 'items[1].parts[0]', pr(w3, lambda p: bank(p[0]) and bank(p[1])))
eq(L, 'items[1].parts[1]', cond(w3, lambda p: not bank(p[2]), lambda p: bank(p[0]) and bank(p[1])))
eq(L, 'items[1].parts[2]', pr(w3, lambda p: bank(p[0]) and bank(p[1]) and not bank(p[2])))
two_banks = lambda p: sum(bank(i) for i in p) == 2
eq(L, 'items[1].parts[3]', pr(w3, two_banks))
eq(L, 'items[1].parts[4]', cond(w3, lambda p: not bank(p[2]), two_banks))
first = F(5, 10) * F(6, 10) + F(3, 10) * F(8, 10) + F(2, 10) * F(9, 10)
eq(L, 'items[2].parts[0]', F(5, 10) * F(6, 10))
eq(L, 'items[2].parts[1]', first)
eq(L, 'items[2].parts[2]', first + (1 - first) * F(8, 10))
eq(L, 'items[2].parts[3]', F(9, 10) + F(1, 10) * F(8, 10))
cid(L, 'items[2].parts[4]', ['z-first'])
ok(F(98, 100) - (first + (1 - first) * F(8, 10)) == F(36, 1000), 'problems-1 router gap is 0.036')
calls = list(permutations(range(10), 3))
goodq = lambda i: i < 4
stop = lambda p: next((k + 1 for k, i in enumerate(p) if goodq(i)), None)
eq(L, 'items[3].parts[0]', pr(calls, lambda p: stop(p) == 2))
eq(L, 'items[3].parts[1]', pr(calls, lambda p: stop(p) == 3))
eq(L, 'items[3].parts[2]', pr(calls, lambda p: stop(p) is not None))
eq(L, 'items[3].parts[3]', cond(calls, lambda p: stop(p) == 2, lambda p: stop(p) in (2, 3)))

# Protocol, findings 3 and 4: the same report-a-random-die (or card) reading lands on a listed wrong value each time.
num = den = F(0)
for r in d8:
    for shown in (0, 1):
        if r[shown] == 8:
            den += 1
            num += sum(r) == 10
ok(num / den == F(1, 8) and abs(get(L, 'items[0].parts[1]')['widget']['wrong'][0]['value'] - 0.125) < 1e-9,
   'problems-1 p-eight-sided part 2: report protocol gives 1/8, the wrong value "sixteen" (finding 3)')
num = den = F(0)
for r in two:
    for shown in (0, 1):
        if r[shown] == 6:
            den += 1
            num += r == (6, 6)
ok(num / den == F(1, 6), 'homework-1 h-both-sixes: report protocol gives 1/6, the wrong value "one-die" (finding 4)')
shown_ace = F(4, 52)                                   # one of the three cards, picked at random, is turned over
ok(F(4, 22100) / shown_ace == F(1, 425), 'homework-1 h-aces: show-one-card protocol gives 1/425, option b (finding 4)')

# finding 21 (wrong): the summary trap states the two counts the wrong way round. This check fails until the text is fixed.
n_at_least = sum(1 for r in two if 5 in r)
n_first = sum(1 for r in two if r[0] == 5)
swapped = says('l3-shrinking', 'summary.trap', '“At least one is a 5” is not “the first is a 5”. The first leaves 6 outcomes; the second leaves 11.')
fixed = says('l3-shrinking', 'summary.trap', '“At least one is a 5” is not “the first is a 5”. The first leaves 11 outcomes; the second leaves 6.')
ok((n_at_least, n_first) == (11, 6) and not swapped and fixed, 'l3 summary.trap gives each statement its own count (finding 21)',
   f'"at least one is a 5" leaves {n_at_least} outcomes and "the first is a 5" leaves {n_first}; the trap says 6 and 11 in that order')

report('conditional L1 concepts')
