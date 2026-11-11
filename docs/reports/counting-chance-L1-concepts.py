#!/usr/bin/env python3
"""Concept audit, counting-chance level 1 (l1 to l4, review-1, homework-1, problems-1).
Exact enumeration of every counting and probability claim, plus Monte Carlo where a claim is empirical.
Run from the repository root: python3 docs/reports/counting-chance-L1-concepts.py
Exits 0 when the content is correct. A check that fails because the content is wrong stays failing."""
import itertools, json, math, os, random, re, sys
from fractions import Fraction as F

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'counting-chance')
FAIL, N, NOTES = [], [0], []


def load(name):
    return json.load(open(os.path.join(BASE, name + '.json'), encoding='utf-8'))


def get(obj, path):
    for part in re.findall(r'[A-Za-z_][\w-]*|\[\d+\]', path):
        obj = obj[int(part[1:-1])] if part[0] == '[' else obj[part]
    return obj


def check(label, cond):
    N[0] += 1
    if not cond:
        FAIL.append(label)
        print('FAIL', label)


def near(a, b, tol=6e-5):
    return abs(float(a) - float(b)) <= tol


def key(doc, path, value, label, tol=6e-5):
    """The graded answer at path equals the recomputed value."""
    check(f'{label}: key {get(doc, path)} vs {float(value):.6g}', near(get(doc, path), value, tol))


def wrongs(doc, path, values, label, tol=6e-5):
    """Every wrong[].value at path equals, in order, the recomputed slip value, and none equals the key."""
    w = get(doc, path)
    got = [x['value'] for x in w['wrong']]
    check(f'{label}: wrong values {got} vs {[round(float(v), 6) for v in values]}',
          len(got) == len(values) and all(near(g, v, tol) for g, v in zip(got, values)))
    check(f'{label}: no wrong value equals the key', all(not near(g, w['answer'], 1e-9) for g in got))


def correct_option(doc, path):
    return [o for o in get(doc, path)['options'] if o.get('correct')]


def cells(pairs):
    return sorted(f'r{r}c{c}' for r, c in pairs)


def has(doc, path, text, label=None):
    check(label or f'text at {path} holds "{text}"', text in json.dumps(get(doc, path), ensure_ascii=False))


random.seed(20261111)
D6 = range(1, 7)
ROLLS = list(itertools.product(D6, D6))          # (red, blue), 36 equally likely
P = lambda ev, space: F(sum(1 for o in space if ev(o)), len(space))

# ---------------------------------------------------------------- l1
l1 = load('l1-every-outcome')
check('l1 s0 sevens', sorted(get(l1, 'screens[0].widget.answer')) == cells([o for o in ROLLS if sum(o) == 7]))
T3 = [''.join(t) for t in itertools.product('ht', repeat=3)]
path3 = lambda s: '-'.join(s)
check('l1 s1 exactly two heads', sorted(get(l1, 'screens[1].widget.answer')) == sorted(path3(s) for s in T3 if s.count('h') == 2))
check('l1 s3 first and last match', sorted(get(l1, 'screens[3].widget.answer')) == sorted(path3(s) for s in T3 if s[0] == s[2]))
key(l1, 'screens[4].widget.answer', sum(1 for r, b in ROLLS if r > b), 'l1 s4 red beats blue')
wrongs(l1, 'screens[4].widget', [sum(1 for r, b in ROLLS if r >= b), 18, sum(1 for r, b in ROLLS if r != b)], 'l1 s4')
check('l1 s5 C empty and D whole', not [o for o in ROLLS if sum(o) == 13] and all(sum(o) <= 12 for o in ROLLS))
UNORD = sorted({tuple(sorted(o)) for o in ROLLS})
check('l1 s6 Sam has 21 unordered outcomes, 3 total 7', len(UNORD) == 21 and sum(1 for u in UNORD if sum(u) == 7) == 3)
# Sam's outcomes are not equally likely: exact chance of each unordered outcome under two fair independent dice
pu = {u: P(lambda o, u=u: tuple(sorted(o)) == u, ROLLS) for u in UNORD}
check('l1 s6 Sam unordered outcomes have unequal chances (1/36 and 2/36)', set(pu.values()) == {F(1, 36), F(2, 36)})
check('l1 s6 key is 6/36', [o['id'] for o in correct_option(l1, 'screens[6].widget')] == ['right'] and P(lambda o: sum(o) == 7, ROLLS) == F(1, 6))
key(l1, 'screens[7].widget.answer', 6 ** 3, 'l1 s7 three dice')
wrongs(l1, 'screens[7].widget', [len({tuple(sorted(t)) for t in itertools.product(D6, repeat=3)}), 18, 36], 'l1 s7')
MOVES = list(itertools.product((1, 0, -1), repeat=2))   # rows and columns: Up, Flat, Down
above = [(i + 1, j + 1) for i, a in enumerate((1, 0, -1)) for j, b in enumerate((1, 0, -1)) if a + b > 0]
check('l1 s8 share ends above 50', sorted(get(l1, 'screens[8].widget.answer')) == cells(above))
key(l1, 'quiz[0].widget.answer', 2 * 6, 'l1 q coin and die')
key(l1, 'quiz[2].widget.answer', len(MOVES), 'l1 q net moves')
check('l1 q net moves: five net values, net 0 from three paths', len({a + b for a, b in MOVES}) == 5 and sum(1 for a, b in MOVES if a + b == 0) == 3)
key(l1, 'quiz[3].widget.answer', sum(1 for r, b in ROLLS if r % 2 and b % 2 and (r + b) % 2), 'l1 q both odd and odd total')
wrongs(l1, 'quiz[3].widget', [sum(1 for r, b in ROLLS if r % 2 and b % 2), sum(1 for r, b in ROLLS if (r + b) % 2)], 'l1 q empty')

# ---------------------------------------------------------------- l2
l2 = load('l2-equally-likely')
by_total = {t: sum(1 for o in ROLLS if sum(o) == t) for t in range(2, 13)}
check('l2 s2 chart counts by total', all(get(l2, 'screens[2].canvas.state.values')[str(t)] == by_total[t] for t in by_total))
check('l2 s0 seven is the most likely total, six times as likely as 2 and as 12', max(by_total, key=by_total.get) == 7 and by_total[7] == 6 * by_total[2] == 6 * by_total[12])
# Monte Carlo: the 11 totals are not equally likely (claim) against its negation (each 1/11)
n = 200000
c7 = sum(1 for _ in range(n) if random.randint(1, 6) + random.randint(1, 6) == 7)
check(f'l2 MC P(total 7) = {c7 / n:.4f} is 1/6, not 1/11', abs(c7 / n - 1 / 6) < 0.004 and abs(c7 / n - 1 / 11) > 0.05)


def mulberry32(seed):
    a = [seed & 0xFFFFFFFF]

    def imul(x, y):
        return (x * y) & 0xFFFFFFFF

    def r():
        a[0] = (a[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = a[0]
        t = imul(t ^ (t >> 15), t | 1)
        t ^= (t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


sim = get(l2, 'screens[0].canvas.params.sim')
r = mulberry32(sim['seed'])
out = [(1 + int(r() * 6)) + (1 + int(r() * 6)) for _ in range(1000)]
tal = {t: out.count(t) for t in range(2, 13)}
check(f'l2 s0 the seeded 1,000 rolls the learner sees have 7 as the tallest bar ({tal[7]} against next {sorted(tal.values())[-2]})',
      sim['outcome'] == 'd6()+d6()' and max(tal, key=tal.get) == 7 and sorted(tal.values())[-1] > sorted(tal.values())[-2])
check('l2 s1 total 10', sorted(get(l2, 'screens[1].widget.answer')) == cells([o for o in ROLLS if sum(o) == 10]))
key(l2, 'screens[2].widget.answer', P(lambda o: sum(o) == 7, ROLLS), 'l2 s2 P(7)')
wrongs(l2, 'screens[2].widget', [F(1, 11), F(1, 2), F(7, 36), F(1, 36)], 'l2 s2')
key(l2, 'screens[3].widget.answer', P(lambda o: sum(o) >= 10, ROLLS), 'l2 s3 P(>=10)')
wrongs(l2, 'screens[3].widget', [F(3, 11), F(3, 36)], 'l2 s3')
key(l2, 'screens[8].widget.answer', 10 * P(lambda o: o[0] > o[1], ROLLS), 'l2 s8 fair price')
wrongs(l2, 'screens[8].widget', [5, F(10, 3), 10], 'l2 s8', tol=1e-3)
log = 'U U D U D U U D U D'.split()
check('l2 s7 log has 6 up days of 10', log.count('U') == 6 and 'U U D U D U U D U D' in get(l2, 'screens[7].prose'))
# 6 ups in 10 does not separate 0.6 from 0.5: exact binomial tail under p = 0.5
tail = sum(math.comb(10, k) for k in range(6, 11)) / 2 ** 10
NOTES.append(f'l2 s7: P(6 or more ups in 10 | p = 0.5) = {tail:.3f}, so the ten-day log is weak evidence against one half (finding 6, imprecise)')
key(l2, 'quiz[0].widget.answer', P(lambda o: sum(o) == 4, ROLLS), 'l2 q total 4')
wrongs(l2, 'quiz[0].widget', [F(1, 11), F(2, 36)], 'l2 q total 4')
C2 = list(itertools.product('HT', repeat=2))
key(l2, 'quiz[1].widget.answer', P(lambda o: o.count('H') == 1, C2), 'l2 q two coins')
key(l2, 'quiz[2].widget.answer', 12 * P(lambda o: sum(o) == 7, ROLLS), 'l2 q bet seven')
wrongs(l2, 'quiz[2].widget', [F(12, 11), 6, F(12, 36)], 'l2 q bet seven', tol=1e-3)
check('l2 q which-equal: ordered tosses are the equally likely list', [o['id'] for o in correct_option(l2, 'quiz[3].widget')] == ['right'])

# ---------------------------------------------------------------- l3
l3 = load('l3-events-as-sets')
A = {o for o in ROLLS if o[0] % 2 == 0}
B = {o for o in ROLLS if sum(o) >= 8}
check('l3 s0 A and B', sorted(get(l3, 'screens[0].widget.answer')) == cells(A & B))
v = get(l3, 'screens[1].canvas.params.values')
check('l3 Venn region counts 9, 9, 6, 12', (v['A'], v['AB'], v['B'], v['none']) == (len(A - B), len(A & B), len(B - A), 36 - len(A | B)))
key(l3, 'screens[6].widget.answer', len(A | B), 'l3 s6 rolls that pay')
wrongs(l3, 'screens[6].widget', [len(A ^ B), len(A) + len(B), len(A & B), 36], 'l3 s6')
A7 = {o for o in ROLLS if sum(o) == 7}
DB = {o for o in ROLLS if o[0] == o[1]}
check('l3 s5 a double never totals 7', not (A7 & DB) and {sum(o) for o in DB} == {2, 4, 6, 8, 10, 12})
key(l3, 'screens[5].widget.answer', F(len(A7 | DB), 36), 'l3 s5 P(7 or double)')
wrongs(l3, 'screens[5].widget', [F(11, 36), F(6, 36), 0], 'l3 s5')
# De Morgan and the homework identity, over every pair of subsets of a 4-point universe
U = frozenset(range(4))
subs = [frozenset(s) for k in range(5) for s in itertools.combinations(U, k)]
ok = all(U - (a | b) == (U - a) & (U - b) and U - (a & b) == (U - a) | (U - b) for a in subs for b in subs)
check('l3 s4 De Morgan holds for all 256 pairs of subsets', ok)
check('l3 s7 |A or B| = |A| + |B| - |A and B| for all pairs', all(len(a | b) == len(a) + len(b) - len(a & b) for a in subs for b in subs))
rows = get(l3, 'screens[8].canvas.params.rows')
da = {r[0] for r in rows if float(r[1]) > 50}
db = {r[0] for r in rows if float(r[2]) > 1}
check('l3 s8 table counts 11, 8, 5', (len(da), len(db), len(da & db)) == (11, 8, 5))
key(l3, 'screens[8].widget.answer', len(da | db), 'l3 s8 days in A or B')
wrongs(l3, 'screens[8].widget', [19, len(da ^ db), len(da & db), 20 - len(da | db)], 'l3 s8')
key(l3, 'quiz[0].widget.answer', F(18 + 14 - 6, 50), 'l3 q signals')
wrongs(l3, 'quiz[0].widget', [F(32, 50), F(18 + 14 - 12, 50), F(6, 50)], 'l3 q signals')
key(l3, 'quiz[2].widget.answer', 1 - F(45, 100) - F(4, 10), 'l3 q flat')
A10 = {o for o in ROLLS if sum(o) >= 10}
key(l3, 'quiz[3].widget.answer', F(len(A10 | DB), 36), 'l3 q 10 or more, or double')
wrongs(l3, 'quiz[3].widget', [F(12, 36), F(len(A10 ^ DB), 36), F(len(A10 & DB), 36)], 'l3 q3')

# ---------------------------------------------------------------- l4
l4 = load('l4-does-not-happen')
check('l4 s0 at least one head', sorted(get(l4, 'screens[0].widget.answer')) == sorted(path3(s) for s in T3 if 'h' in s))
atl = lambda n, p=F(1, 6): 1 - (1 - p) ** n
key(l4, 'screens[1].widget.answer', min(n for n in range(1, 30) if atl(n) > F(1, 2)), 'l4 s1 smallest n')
check('l4 s1 0.4213 at 3 rolls and 0.5177 at 4', near(atl(3), 0.4213) and near(atl(4), 0.5177))
key(l4, 'screens[2].widget.answer', 1 - F(1, 16), 'l4 s2 four tosses')
R4 = list(itertools.product(D6, repeat=4))
nosix = sum(1 for o in R4 if 6 not in o)
key(l4, 'screens[3].widget.answer', nosix, 'l4 s3 no six by enumeration')
wrongs(l4, 'screens[3].widget', [len(R4) - nosix, 20, len(R4) - 4, len(R4) - 216], 'l4 s3')
key(l4, 'screens[4].widget.answer', F(len(R4) - nosix, len(R4)), 'l4 s4 at least one six in four')
wrongs(l4, 'screens[4].widget', [F(nosix, len(R4)), F(4, 6), F(1, 6)], 'l4 s4')
check('l4 s5 true two-roll chance is 11/36', P(lambda o: 6 in o, ROLLS) == F(11, 36) and [o['text'] for o in correct_option(l4, 'screens[5].widget')] == ['$\\dfrac{11}{36}$'])
check('l4 s5 six rolls miss a six with chance about 0.335 ("often")', 0.3 < float((F(5, 6)) ** 6) < 0.35)
check('l4 s6 0.6651 at six rolls, and 1 - 0.4^20 about 0.99999999', near(atl(6), 0.6651) and abs((1 - 0.4 ** 20) - 0.99999999) < 5e-9)
check('l4 s6 only the two-headed coin has P(none) = 0', (F(5, 6)) ** 100 > 0 and F(4, 10) ** 20 > 0)
key(l4, 'screens[8].widget.answer', 1 - F(6, 10) ** 5, 'l4 s8 losing day')
wrongs(l4, 'screens[8].widget', [2, F(6, 10) ** 5, F(4, 10) ** 5, 1 - F(4, 10) ** 5], 'l4 s8')
key(l4, 'screens[9].widget.answer', F(8, 10) ** 10, 'l4 s9 no fill')
key(l4, 'screens[10].widget.answer', 1 - F(35, 36) ** 24, 'l4 s10 de Mere bet 2')
wrongs(l4, 'screens[10].widget', [F(24, 36), F(35, 36) ** 24, atl(4)], 'l4 s10')
# Monte Carlo: bet 1 wins more often than not and bet 2 less often (claim: 0.5177 and 0.4914)
n = 200000
b1 = sum(1 for _ in range(n) if any(random.randint(1, 6) == 6 for _ in range(4))) / n
b2 = sum(1 for _ in range(n) if any(random.randint(1, 36) == 36 for _ in range(24))) / n
check(f'l4 MC de Mere: bet 1 {b1:.4f} above one half, bet 2 {b2:.4f} below', abs(b1 - 0.5177) < 0.005 and abs(b2 - 0.4914) < 0.005 and b1 > 0.505 and b2 < 0.498)
key(l4, 'quiz[0].widget.answer', 1 - F(1, 32), 'l4 q five tosses')
key(l4, 'quiz[1].widget.answer', F(97, 100) ** 20, 'l4 q margin call')
wrongs(l4, 'quiz[1].widget', [1 - 20 * F(3, 100), 1 - F(97, 100) ** 20], 'l4 q margin call')
check('l4 q three rolls: 91/216', atl(3) == F(91, 216))

# ---------------------------------------------------------------- review-1
r1 = load('review-1')
key(r1, 'items[0].widget.answer', 2 ** 3, 'r1 i0')
check('r1 i1 differ by 4', sorted(get(r1, 'items[1].widget.answer')) == cells([o for o in ROLLS if abs(o[0] - o[1]) == 4]))
key(r1, 'items[2].widget.answer', P(lambda o: sum(o) == 9, ROLLS), 'r1 i2')
C3 = list(itertools.product('HT', repeat=3))
check('r1 i3 exactly two heads 3/8, at least two 1/2', P(lambda o: o.count('H') == 2, C3) == F(3, 8) and P(lambda o: o.count('H') >= 2, C3) == F(1, 2)
      and [o['text'] for o in correct_option(r1, 'items[3].widget')] == ['$\\dfrac{3}{8}$'])
check('r1 i4 complement of the overlap', sorted(get(r1, 'items[4].widget.answer')) == ['A', 'B', 'none'])
key(r1, 'items[5].widget.answer', F(50 + 40 - 15, 120), 'r1 i5')
wrongs(r1, 'items[5].widget', [F(90, 120), F(35 + 25, 120), F(45, 120)], 'r1 i5')
key(r1, 'items[6].widget.answer', atl(3), 'r1 i6')
wrongs(r1, 'items[6].widget', [F(1, 2), F(125, 216), F(1, 216)], 'r1 i6')
key(r1, 'items[7].widget.answer', 1 - F(7, 10) ** 5, 'r1 i7')
wrongs(r1, 'items[7].widget', [F(15, 10), F(7, 10) ** 5, F(3, 10) ** 5, 1 - F(3, 10) ** 5], 'r1 i7')
key(r1, 'items[8].widget.answer', P(lambda o: max(o) == 5, ROLLS), 'r1 i8 larger is 5')
wrongs(r1, 'items[8].widget', [F(10, 36), F(1, 6), P(lambda o: max(o) <= 5, ROLLS)], 'r1 i8')

# ---------------------------------------------------------------- homework-1
h1 = load('homework-1')
M3 = list(itertools.product((1, 0, -1), repeat=3))
key(h1, 'items[0].widget.answer', sum(1 for m in M3 if sum(m) == 0), 'h1 i0 back to start')
key(h1, 'items[1].widget.answer', P(lambda o: max(o) == 4, ROLLS), 'h1 i1 larger is 4')
wrongs(h1, 'items[1].widget', [F(8, 36), F(1, 6), P(lambda o: max(o) <= 4, ROLLS)], 'h1 i1')
key(h1, 'items[2].widget.answer', 18 * F(len(DB), 36), 'h1 i2 double bet')
wrongs(h1, 'items[2].widget', [18 * F(6, 21), 18 * F(1, 36), 9], 'h1 i2', tol=1e-3)
check('h1 i3 (A or B) and not C', sorted(get(h1, 'items[3].widget.answer')) == ['A', 'AB', 'B'])
ident = all((U - a) | (U - b) == U - (a & b) == (a - b) | (b - a) | (U - (a | b)) for a in subs for b in subs)
neq = any((U - a) | (U - b) != (U - a) & (U - b) for a in subs for b in subs)
opts = get(h1, 'items[4].widget.options')
check('h1 i4 multi: the two correct sets equal the target for all subsets, the others do not',
      ident and neq and [bool(o.get('correct')) for o in opts] == [True, True, False, False])
key(h1, 'items[5].widget.answer', min(n for n in range(1, 60) if 1 - F(8, 10) ** n >= F(95, 100)), 'h1 i5 orders')
check('h1 i5 0.9450 at 13 and 0.9560 at 14', near(1 - 0.8 ** 13, 0.9450) and near(1 - 0.8 ** 14, 0.9560))
key(h1, 'items[6].widget.answer', 1 - F(75, 100) * F(7, 10) * F(6, 10), 'h1 i6')
wrongs(h1, 'items[6].widget', [F(95, 100), F(25, 100) * F(3, 10) * F(4, 10), F(315, 1000)], 'h1 i6')
check('h1 i7 order is the authored order', get(h1, 'items[7].widget.answer') == ['s1', 's2', 's3', 's4'])
model = get(h1, 'items[8].model')
ev = [sum(1 for o in R4 if o[i] == 6) for i in range(4)]
check('h1 i8 (c) each event holds 216, sum 864, 671 distinct, 193 repeats', ev == [216] * 4 and len(R4) - nosix == 671 and 864 - 671 == 193 and all(s in model for s in ('864', '671', '193')))
n25 = min(n for n in range(1, 100) if 1 - F(35, 36) ** n > F(1, 2))
check('h1 i8 (d) smallest n is 25, with 0.5055, and ln ratio 24.6', n25 == 25 and near(1 - (35 / 36) ** 25, 0.5055) and near(math.log(0.5) / math.log(35 / 36), 24.6, 0.05) and '25' in model)

# ---------------------------------------------------------------- problems-1
p1 = load('problems-1')
S46 = list(itertools.product(range(1, 5), D6))
key(p1, 'items[0].parts[0].widget.answer', len(S46), 'p1 i0 p0')
key(p1, 'items[0].parts[1].widget.answer', P(lambda o: o[1] > o[0], S46), 'p1 i0 p1')
wrongs(p1, 'items[0].parts[1].widget', [P(lambda o: o[1] >= o[0], S46), F(14, 36), F(1, 2)], 'p1 i0 p1')
key(p1, 'items[0].parts[2].widget.answer', P(lambda o: o[0] > o[1], S46), 'p1 i0 p2')
key(p1, 'items[0].parts[3].widget.answer', 12 * P(lambda o: o[0] <= o[1], S46), 'p1 i0 p3')
S88 = list(itertools.product(range(1, 9), repeat=2))
A8 = {o for o in S88 if o[0] >= 7}
B8 = {o for o in S88 if abs(o[0] - o[1]) >= 6}
key(p1, 'items[1].parts[0].widget.answer', len(B8), 'p1 i1 p0')
key(p1, 'items[1].parts[1].widget.answer', len(A8 & B8), 'p1 i1 p1')
key(p1, 'items[1].parts[2].widget.answer', len(A8 | B8), 'p1 i1 p2')
check('p1 i1 p2 feedback: 16 is also the count in exactly one event', len(A8 ^ B8) == 16)
key(p1, 'items[1].parts[3].widget.answer', F(len(A8 | B8), 64), 'p1 i1 p3')
wrongs(p1, 'items[1].parts[3].widget', [F(22, 64), F(19, len({tuple(sorted(o)) for o in S88})), F(19, 16)], 'p1 i1 p3')
key(p1, 'items[1].parts[4].widget.answer', 16 * F(len(A8 | B8), 64), 'p1 i1 p4')
pf, bf = F(5, 100), F(8, 100)
key(p1, 'items[2].parts[0].widget.answer', pf * bf, 'p1 i2 p0')
wrongs(p1, 'items[2].parts[0].widget', [pf + bf, pf + bf - pf * bf], 'p1 i2 p0')
key(p1, 'items[2].parts[1].widget.answer', 1 - pf * bf, 'p1 i2 p1')
wrongs(p1, 'items[2].parts[1].widget', [1 - (pf + bf), (1 - pf) * (1 - bf), pf * bf], 'p1 i2 p1')
key(p1, 'items[2].parts[2].widget.answer', (1 - pf * bf) ** 20, 'p1 i2 p2')
wrongs(p1, 'items[2].parts[2].widget', [1 - 20 * pf * bf, ((1 - pf) * (1 - bf)) ** 20, 20 * (1 - pf * bf)], 'p1 i2 p2')
key(p1, 'items[2].parts[3].widget.answer', 1 - (1 - pf * bf) ** 20, 'p1 i2 p3')
# Monte Carlo of the feed model: independent failures each day, 20 independent days
n = 100000
hit = sum(1 for _ in range(n) if any(random.random() < 0.05 and random.random() < 0.08 for _ in range(20))) / n
check(f'p1 i2 MC at least one blackout day in 20: {hit:.4f} near 0.0770', abs(hit - 0.0770) < 0.004)
S44 = list(itertools.product(range(1, 5), repeat=2))
key(p1, 'items[3].parts[0].widget.answer', len(S44), 'p1 i3 p0')
wrongs(p1, 'items[3].parts[0].widget', [len({tuple(sorted(o)) for o in S44}), 8, len({sum(o) for o in S44})], 'p1 i3 p0')
p8 = P(lambda o: sum(o) == 8, S44)
key(p1, 'items[3].parts[1].widget.answer', p8, 'p1 i3 p1')
key(p1, 'items[3].parts[2].widget.answer', (1 - p8) ** 10, 'p1 i3 p2')
wrongs(p1, 'items[3].parts[2].widget', [1 - 10 * p8, F(9, 10) ** 10, F(6, 7) ** 10], 'p1 i3 p2')
key(p1, 'items[3].parts[3].widget.answer', 1 - (1 - p8) ** 10, 'p1 i3 p3')
key(p1, 'items[3].parts[4].widget.answer', min(n for n in range(1, 200) if 1 - (1 - p8) ** n > F(9, 10)), 'p1 i3 p4')
check('p1 i3 p4 feedback values 0.6202 at 15, 0.5083 at 11, 0.8955 at 35, 0.9021 at 36',
      all(near(1 - (15 / 16) ** n, v) for n, v in ((15, 0.6202), (11, 0.5083), (35, 0.8955), (36, 0.9021))))

for note in NOTES:
    print('NOTE', note)
print(f'counting-chance L1 concepts: {N[0] - len(FAIL)} of {N[0]} checks passed')
sys.exit(1 if FAIL else 0)
