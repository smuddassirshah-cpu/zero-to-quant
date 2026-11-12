"""Round 2 concept audit, course `conditional`, level 1 (l1 to l6, review-1,
homework-1, problems-1). Run from the repo root:
    python3 docs/reports/conditional-L1-concepts-r2.py
Every key, slip value and stated number is recomputed by exact enumeration
(Fractions over the outcome space) and the main results are also confirmed by
seeded Monte Carlo. Exits 0 on correct content.
"""
from conditional_concepts_r2_lib import *

die = list(range(1, 7))
two = list(product(die, die))

# ---------------- l1 what changes ----------------
L = 'l1-what-changes'
even = lambda x: x % 2 == 0
C(L, 'screens[1]', 'more')
ok('l1 s1 6 given even rises', cond(die, lambda x: x == 6, even) > F(1, 6))
TAP(L, 'screens[2]', ['r1c2', 'r1c4', 'r1c6'])
A(L, 'screens[3]', cond(die, lambda x: x == 6, even), before=F(1, 6), half=F(1, 2))
S(L, 'screens[3].explain.text', 'doubled the chance by halving', cond(die, lambda x: x == 6, even) == 2 * F(1, 6))
C(L, 'screens[4]', 'right', cond(die, even, lambda x: x > 3), before=F(1, 2), whole=F(2, 6), odd=F(1, 3))
A(L, 'screens[5]', cond(die, lambda x: x == 1, lambda x: x > 3), before=F(1, 6), third=F(1, 3))
C(L, 'screens[6]', 'same')
ok('l1 s6 even given at most 4 is 1/2', cond(die, even, lambda x: x <= 4) == F(1, 2))
C(L, 'screens[7]', 'right')
days = {'A': 24, 'AB': 56, 'B': 64, 'none': 56}
ok('l1 s8 venn totals 200', sum(days.values()) == 200 and get(L, 'screens[8].canvas.params.values') == days)
hv = days['A'] + days['AB']
up = days['B'] + days['AB']
A(L, 'screens[8]', F(56, hv), **{'all-up': F(up, 200), 'wrong-bottom': F(56, up), 'all-days': F(56, 200)})
S(L, 'screens[8].explain.text', r'\tfrac{120}{200} = 0.6', up == 120)
# the "removes outcomes unevenly" sentence: equal counts removed from A and not-A
# leave the share unchanged only when P(A) was 1/2 (finding: imprecise)
A3 = lambda x: x in (1, 2)
ok('l1 s6 counter-example exists: remove one A face and one non-A face, share moves',
   cond(die, A3, lambda x: x not in (1, 6)) != prob(die, A3))
deck = [(r, s) for r in range(13) for s in 'HDSC']
C(L, 'quiz[0]', 'right', cond(deck, lambda c: c[1] == 'H', lambda c: c[1] in 'HD'), before=F(1, 4), certain=1,
  **{'one-card': F(1, 26)})
A(L, 'quiz[1]', cond(die, lambda x: x == 6, lambda x: x >= 3), before=F(1, 6), boundary=F(1, 3))
C(L, 'quiz[2]', 'right', cond(die, lambda x: x <= 3, lambda x: x % 2 == 1), same=F(1, 2), flipped=F(1, 3), whole=F(2, 6))

# ---------------- l2 counting what is left ----------------
L = 'l2-counting-left'
trees(L)
bag = ['R1', 'R2', 'R3', 'B1', 'B2']
pairs = list(permutations(bag, 2))
red = lambda c: c[0] == 'R'
ok('l2 20 ordered pairs', len(pairs) == 20)
C(L, 'screens[1]', 'right', cond(pairs, lambda p: red(p[1]), lambda p: red(p[0])),
  **{'put-back': F(3, 5), 'kept-total': F(2, 5), 'kept-reds': F(3, 4)})
both_red = [f'r{bag.index(a) + 1}c{bag.index(b) + 1}' for a, b in pairs if red(a) and red(b)]
TAP(L, 'screens[2]', both_red)
A(L, 'screens[3]', cond(pairs, lambda p: red(p[1]), lambda p: red(p[0])), **{'all-cells': F(6, 20), 'put-back': F(3, 5)})
A(L, 'screens[4]', cond(pairs, lambda p: red(p[1]), lambda p: not red(p[0])),
  **{'put-back': F(3, 5), 'after-red': F(1, 2), 'blue': F(1, 4)})
A(L, 'screens[5]', prob(pairs, lambda p: red(p[0]) and red(p[1])), **{'put-back': F(9, 25), 'given': F(1, 2), 'first-only': F(3, 5)})
A(L, 'screens[6]', prob(pairs, lambda p: red(p[1])),
  **{'assumed-red': F(1, 2), 'average': (F(2, 4) + F(3, 4)) / 2, 'assumed-blue': F(3, 4)})
S(L, 'screens[6].explain.text', '12 of the 20 pairs end in red', sum(1 for p in pairs if red(p[1])) == 12)
C(L, 'screens[7]', 'right')
ok('l2 s7 blue blue 1/10', prob(pairs, lambda p: not red(p[0]) and not red(p[1])) == F(1, 10))
w = get(L, 'screens[8].widget')
ok('l2 s8 derive factor 6/12', F(6, 20) / F(12, 20) == F(6, 12) and w['answer'] == r'\frac{6}{12}'
   and all(F(a) == F(1, 2) for a in w['accept']))
stocks = ['W'] * 4 + ['L'] * 6
sp = list(permutations(range(10), 2))
A(L, 'screens[9]', prob(sp, lambda p: stocks[p[0]] == 'W' and stocks[p[1]] == 'W'),
  **{'put-back': F(16, 100), 'second-only': F(3, 9), 'first-only': F(4, 10)})
chips = ['G'] * 4 + ['X'] * 2
cp = list(permutations(range(6), 2))
C(L, 'quiz[0]', 'right', cond(cp, lambda p: chips[p[1]] == 'X', lambda p: chips[p[0]] == 'X'),
  **{'put-back': F(2, 6), 'kept-faulty': F(2, 5), 'both': prob(cp, lambda p: chips[p[0]] == 'X' and chips[p[1]] == 'X')})
A(L, 'quiz[1]', F(4, 52) * F(3, 51), **{'put-back': F(4, 52) ** 2, 'second-only': F(3, 51)})
C(L, 'quiz[2]', 'right', prob(pairs, lambda p: not red(p[1])),
  **{'assumed-blue': F(1, 4), 'assumed-red': F(1, 2), 'one-path': F(3, 10)})
# Monte Carlo: an unseen first draw leaves the second at 3/5
m = mc(lambda r: red(r.sample(bag, 2)[1]), 200000, 11)
ok(f'l2 MC second red unseen {m:.4f} vs 0.6', abs(m - 0.6) < 0.005)

# ---------------- l3 shrinking the sample space ----------------
L = 'l3-shrinking'
tot = lambda t: (lambda o: o[0] + o[1] == t)
has5 = lambda o: 5 in o
TAP(L, 'screens[1]', [f'r{a}c{b}' for a, b in two if a + b == 8])
S(L, 'screens[1].explain.text', r'\tfrac{5}{36}', prob(two, tot(8)) == F(5, 36))
C(L, 'screens[2]', 'right', cond(two, tot(8), lambda o: o[0] == 5), before=F(5, 36), whole=F(1, 36), complement=F(5, 6))
n5 = sum(1 for o in two if has5(o))
A(L, 'screens[3]', n5, **{'corner-twice': 12, 'corner-removed': 10, 'one-row': 6, 'everything': 36, 'no-five': 25})
C(L, 'screens[4]', 'right', cond(two, tot(10), has5), **{'fixed-die': F(1, 6), 'corner-twice': F(1, 12), 'whole': F(3, 36)})
S(L, 'screens[4].explain.text', r'\tfrac{3}{36} = \tfrac{1}{12}', prob(two, tot(10)) == F(1, 12))
ORD(L, 'screens[5]', ['counted', 'divide', 'probs'])
S(L, 'screens[5].explain.text', r'\tfrac{1/36}{11/36} = \tfrac{1}{11}',
  prob(two, lambda o: tot(10)(o) and has5(o)) / prob(two, has5) == F(1, 11))
A(L, 'screens[6]', 1000 * F(11, 36), **{'ten-share': 1000 * F(1, 11), 'one-die': 1000 * F(1, 6), 'corner-twice': 1000 * F(12, 36),
                                         'everything': 1000})
ex = get(L, 'screens[6].canvas.params.exact')
ok('l3 s6 exact bars', close(ex[0]['y'], F(11, 36), 6e-5) and close(ex[1]['y'], F(25, 36), 6e-5))
m = mc(lambda r: r.randint(1, 6) == 5 or r.randint(1, 6) == 5, 400000, 4226)
ok(f'l3 MC kept share {m:.4f} vs 11/36', abs(m - 11 / 36) < 0.004)
m = mc_cond(lambda r: (lambda a, b: (a == 5 or b == 5, a + b == 10))(r.randint(1, 6), r.randint(1, 6)), 600000, 7)
ok(f'l3 MC total 10 given at least one 5 {m:.4f} vs 1/11', abs(m - 1 / 11) < 0.004)
st = list(product('UD', 'UD'))
C(L, 'screens[7]', 'right', cond(st, lambda o: o == ('U', 'U'), lambda o: 'U' in o),
  before=F(1, 4), **{'known-stock': F(1, 2), 'exactly-one': F(2, 3)})
S(L, 'summary.trap', 'The first leaves 11 outcomes; the second leaves 6',
  n5 == 11 and sum(1 for o in two if o[0] == 5) == 6)
S(L, 'summary.formula.note', 'Defined only when $P(B) > 0$')
C(L, 'quiz[0]', 'right', cond(two, lambda o: 3 in o, tot(7)),
  **{'one-order': F(1, 6), 'reversed': cond(two, tot(7), lambda o: 3 in o), 'whole': F(1, 18)})
A(L, 'quiz[1]', cond(die, lambda x: x > 3, even), before=F(1, 2), **{'one-face': F(1, 3)})
C(L, 'quiz[2]', 'right', cond(st, lambda o: o == ('U', 'U'), lambda o: o[0] == 'U'),
  **{'at-least-one': F(1, 3), 'before': F(1, 4), 'either': prob(st, lambda o: 'U' in o)})

# ---------------- l4 multiplication rule ----------------
L = 'l4-multiplication-rule'
cards = ['2H', '5H', '9H', 'JH', '3S', '8S']
H = lambda c: c[-1] == 'H'
d2 = list(permutations(cards, 2))
d3 = list(permutations(cards, 3))
TAP(L, 'screens[1]', ['h2', 'h5', 'hj'])
S(L, 'screens[1].explain.text', r'\tfrac{3}{5}', cond(d2, lambda p: H(p[1]), lambda p: p[0] == '9H') == F(3, 5))
TAP(L, 'screens[2]', ['h2', 'h5', 'h9', 'hj'])
S(L, 'screens[2].explain.text', r'\tfrac{4}{5}', cond(d2, lambda p: H(p[1]), lambda p: p[0] == '3S') == F(4, 5))
bothH = prob(d2, lambda p: H(p[0]) and H(p[1]))
A(L, 'screens[3]', bothH, fixed=F(4, 6) ** 2, **{'second-only': F(3, 5), 'first-only': F(4, 6), 'after-spade': F(4, 6) * F(4, 5)})
A(L, 'screens[4]', prob(d3, lambda p: all(H(c) for c in p)), fixed=F(4, 6) ** 3, **{'two-only': bothH, 'last-only': F(2, 4)})
A(L, 'screens[5]', F(4, 6) ** 2, **{'took-out': bothH, 'first-only': F(4, 6), 'added': F(4, 6) * 2})
C(L, 'screens[6]', 'right', bothH, sam=F(4, 9), **{'after-spade': F(8, 15), 'first-only': F(2, 3)})
S(L, 'screens[6].feedback.correct', '12 of the 30 deals', sum(1 for p in d2 if H(p[0]) and H(p[1])) == 12 and len(d2) == 30)
ok('l4 s6 Sam: second card alone is a heart 4/6', prob(d2, lambda p: H(p[1])) == F(4, 6))
hsh = prob(d3, lambda p: H(p[0]) and not H(p[1]) and H(p[2]))
C(L, 'screens[7]', 'right')
ok('l4 s7 heart spade heart 1/5', hsh == F(4, 6) * F(2, 5) * F(3, 4) == F(1, 5))
S(L, 'screens[7].feedback.correct', r'= \tfrac{1}{5}', hsh == F(1, 5))
pb = prob(d2, lambda p: not H(p[1]))
pab = prob(d2, lambda p: H(p[0]) and not H(p[1]))
w = get(L, 'screens[8].widget')
ok('l4 s8 P(A|B) = 8/10', pb == F(10, 30) and pab == F(8, 30) and pab / pb == F(8, 10) and w['answer'] == r'\frac{8}{10}')
ok('l4 s8 wrongs', [x['tex'] for x in w['wrong']] == [r'\frac{4}{6}', r'\frac{10}{8}', r'\frac{2}{5}'])
A(L, 'screens[9]', 0.4 * 0.6, unrelated=0.16, added=1.0, **{'second-only': 0.6})
S(L, 'screens[9].explain.text', 'understates the clustering by a third', abs((0.24 - 0.16) / 0.24 - 1 / 3) < 1e-9)
vals = get(L, 'screens[9].canvas.state.values')
ok('l4 s9 shares add to 1', abs(sum(vals.values()) - 1) < 1e-9 and vals['A'] == 0.4)
A(L, 'quiz[0]', F(3, 12) * F(2, 11), fixed=F(3, 12) ** 2, **{'second-only': F(2, 11)})
C(L, 'quiz[1]', 'right', F(4, 52) * F(4, 51), fixed=F(1, 169), added=F(2, 13), **{'kings-down': F(4, 52) * F(3, 51)})
C(L, 'quiz[2]', 'right', F(13, 52) ** 2, added=F(1, 2), one=F(1, 4), **{'kept-out': F(13, 52) * F(12, 51)})
A(L, 'quiz[3]', F(3, 5) * F(2, 4) * F(1, 3), fixed=F(3, 5) ** 3, **{'two-only': F(3, 5) * F(2, 4)})
m = mc(lambda r: all(H(c) for c in r.sample(cards, 3)), 300000, 3)
ok(f'l4 MC three hearts {m:.4f} vs 0.2', abs(m - 0.2) < 0.004)

# ---------------- l5 trees ----------------
L = 'l5-trees'
trees(L)   # includes Kim's tree: its leaves add to 1 although the second stage is wrong
socks = ['B'] * 5 + ['W'] * 3
s2 = list(permutations(range(8), 2))
s3 = list(permutations(range(8), 3))
col = lambda i: socks[i]
TB(L, 'screens[1]', {(0, 1): cond(s2, lambda p: col(p[1]) == 'B', lambda p: col(p[0]) == 'B'),
                     (1, 1): cond(s2, lambda p: col(p[1]) == 'W', lambda p: col(p[0]) == 'B'),
                     (2, 1): cond(s2, lambda p: col(p[1]) == 'B', lambda p: col(p[0]) == 'W'),
                     (3, 1): cond(s2, lambda p: col(p[1]) == 'W', lambda p: col(p[0]) == 'W')})
TAP(L, 'screens[2]', ['w', 'w-w'])
pw = lambda a, b: prob(s2, lambda p: col(p[0]) == a and col(p[1]) == b)
A(L, 'screens[3]', pw('W', 'W'), unconditional=F(3, 8) ** 2, added=F(3, 8) + F(2, 7), **{'leaf-only': F(2, 7)})
TB(L, 'screens[4]', {(0, 1): pw('B', 'B'), (1, 1): pw('B', 'W'), (2, 1): pw('W', 'B'), (3, 1): pw('W', 'W'), (4, 1): 1})
TAP(L, 'screens[5]', ['w-w'])
A(L, 'screens[6]', prob(s3, lambda p: (col(p[0]), col(p[1]), col(p[2])) == ('B', 'B', 'W')),
  unconditional=F(5, 8) * F(5, 8) * F(3, 8), **{'stale-third': F(5, 8) * F(4, 7) * F(3, 8), 'seven-left': F(5, 8) * F(4, 7) * F(3, 7)})
C(L, 'screens[7]', 'right', pw('B', 'W'), kim=F(15, 64), added=F(5, 8) + F(3, 7), branch=F(3, 7))
kim = get(L, 'screens[7].canvas.params.leaves')
ok('l5 s7 Kim leaves add to 1 yet b-w is wrong', sum(F(v) for v in kim.values()) == 1 and F(kim['b-w']) != pw('B', 'W'))
C(L, 'screens[8]', 'right')
S(L, 'screens[8].explain.text', r'chance $\tfrac{5}{8}$, a third number', prob(s2, lambda p: col(p[1]) == 'B') == F(5, 8))
ORD(L, 'screens[9]', ['leaves', 'multiply', 'factor', 'one'])
A(L, 'screens[10]', 0.6 * 0.45, unconditional=0.6 * 0.52, branch=0.45, added=0.6 + 0.45, **{'fill-only': 0.6})
A(L, 'quiz[0]', 0.08 * 0.05, branch=0.05, added=0.13)
S(L, 'quiz[0].explain.text', '4 bonds in 1,000', abs(0.08 * 0.05 * 1000 - 4) < 1e-9)
C(L, 'quiz[1]', 'right', F(12, 51), unconditional=F(13, 52), leaf=F(13, 52) * F(12, 51), **{'kept-hearts': F(13, 51)})
A(L, 'quiz[2]', 1 - (0.42 + 0.18 + 0.28), sum=0.88, **{'one-leaf': 1 - 0.28})
C(L, 'quiz[3]', 'right')
b4 = ['R', 'R', 'R', 'B']
p4 = list(permutations(range(4), 2))
pp = lambda a, b: prob(p4, lambda p: b4[p[0]] == a and b4[p[1]] == b)
ok('l5 q-prune path chances', (pp('R', 'R'), pp('R', 'B'), pp('B', 'R'), pp('B', 'B')) == (F(1, 2), F(1, 4), F(1, 4), 0))

# ---------------- l6 adding up the branches ----------------
L = 'l6-adding-branches'
trees(L)
TAP(L, 'screens[1]', ['a-r', 'b-r'])
C(L, 'screens[2]', 'right')
ltp = lambda ws, ps: sum(a * b for a, b in zip(ws, ps))
red2 = ltp([F(1, 3), F(2, 3)], [F(3, 4), F(1, 4)])
A(L, 'screens[3]', red2, average=F(1, 2), added=1, **{'a-only': F(3, 12), 'b-only': F(2, 12)})
S(L, 'screens[3].explain.text', "nearer bag B's chance", abs(red2 - F(1, 4)) < abs(red2 - F(3, 4)))
red3 = ltp([F(1, 6), F(2, 6), F(3, 6)], [F(4, 4), F(2, 4), F(1, 4)])
A(L, 'screens[4]', red3, average=(1 + F(1, 2) + F(1, 4)) / 3, added=1 + F(1, 2) + F(1, 4), **{'c-only': F(3, 6) * F(1, 4)})
A(L, 'screens[5]', ltp([F(1, 6), F(2, 6), F(3, 6)], [F(1, 4)] * 3), added=F(3, 4), third=F(1, 12))
C(L, 'screens[6]', 'right', ltp([0.8, 0.2], [0.01, 0.06]), average=0.035, added=0.07, **{'y-only': 0.012})
C(L, 'screens[7]', 'right')
ORD(L, 'screens[8]', ['split', 'add', 'mult'])
A(L, 'screens[9]', ltp([0.7, 0.3], [0.4, 0.8]), average=0.6, added=1.2, **{'calm-only': 0.28, 'volatile-only': 0.24})
book = ltp([0.5, 0.3, 0.2], [0.01, 0.03, 0.10])
A(L, 'quiz[0]', book, average=(0.01 + 0.03 + 0.10) / 3, added=0.14)
S(L, 'quiz[0].explain.text', 'more than half the defaults', 0.2 * 0.10 / book > 0.5)
flag = ltp([0.1, 0.9], [0.9, 0.2])
A(L, 'quiz[1]', flag, average=0.55, added=1.1, **{'drop-only': 0.09})
S(L, 'quiz[1].explain.text', 'Two thirds of the flags', abs(0.18 / flag - 2 / 3) < 1e-9)
C(L, 'quiz[2]', 'right', ltp([0.5, 0.3, 0.2], [0.3] * 3), added=0.9, third=0.1, bull=0.15)
C(L, 'quiz[3]', 'right', F(13, 52) * F(12, 51) + F(39, 52) * F(13, 51),
  **{'after-heart': F(12, 51), 'after-other': F(13, 51), 'one-path': F(1, 17)})
S(L, 'quiz[3].explain.text', r'\tfrac{663}{2652}', F(156 + 507, 2652) == F(1, 4))
# weighted average claim (summary): P(B) always lies between the extreme conditionals
rng = random.Random(5)
okk = True
for _ in range(2000):
    ws = [rng.random() for _ in range(3)]
    s_ = sum(ws)
    ws = [x / s_ for x in ws]
    ps = [rng.random() for _ in range(3)]
    v = ltp(ws, ps)
    okk &= min(ps) - 1e-12 <= v <= max(ps) + 1e-12
ok('l6 summary: total probability lies between smallest and largest conditional', okk)
m = mc(lambda r: (r.random() < 0.75) if r.randint(1, 6) <= 2 else (r.random() < 0.25), 400000, 6)
ok(f'l6 MC red {m:.4f} vs 5/12', abs(m - 5 / 12) < 0.004)

# ---------------- review-1 ----------------
L = 'review-1'
trees(L)
C(L, 'items[0]', 'a', cond(die, lambda x: x == 6, even), b=F(1, 6), c=F(1, 2))
A(L, 'items[1]', F(8, 10) * F(7, 9), fixed=F(8, 10) ** 2, **{'not-both': 1 - F(2, 10) * F(1, 9)})
C(L, 'items[2]', 'a', cond(two, lambda o: o[1] == 6, lambda o: o[0] == 4), b=F(1, 36), c=F(1, 5))
c3 = list(product('HT', repeat=3))
A(L, 'items[3]', cond(c3, lambda o: o.count('H') == 3, lambda o: o.count('H') >= 2), whole=F(1, 8), **{'third-coin': F(1, 2)})
A(L, 'items[4]', F(3, 51), replaced=F(4, 52), deck=F(3, 52))
A(L, 'items[5]', 0.15 * 0.12, branch=0.12, added=0.27)
C(L, 'items[6]', 'a', cond(two, lambda o: o[0] % 2 == 0, tot(9)), b=F(2, 36), c=F(1, 4))
ok('review-1 total nine cells', sorted(get(L, 'items[6].canvas.state.shade.nine')) == sorted(f'r{a}c{b}' for a, b in two if a + b == 9))
A(L, 'items[7]', F(5, 8) * F(4, 7), replaced=F(5, 8) ** 2, **{'same-bag': F(5, 8) * F(4, 8)})
A(L, 'items[8]', prob(pairs, lambda p: not red(p[1])), **{'one-path': F(3, 10), 'blue-blue': F(1, 10)})
A(L, 'items[9]', ltp([0.4, 0.6], [0.3, 0.1]), average=0.2, **{'trend-only': 0.12})

# ---------------- homework-1 ----------------
L = 'homework-1'
trees(L)
hi = lambda o: o[0] + o[1] >= 10
C(L, 'items[0]', 'a', cond(two, lambda o: o[0] == o[1], hi), b=F(1, 6), c=F(1, 2), d=F(2, 36))
ok('homework-1 item 0: six outcomes reach a total of at least 10 (three totals)',
   sum(1 for o in two if hi(o)) == 6 and len({a + b for a, b in two if a + b >= 10}) == 3)
C(L, 'items[1]', 'a', F(12, 51), b=F(1, 4), c=F(13, 51), d=F(3, 51))
six = lambda o: 6 in o
A(L, 'items[2]', cond(two, lambda o: o == (6, 6), six), whole=F(1, 36), **{'one-die': F(1, 6)})
a_, b_, c_ = (lambda o: o[0] == 6), tot(7), tot(8)
truth = {'a': cond(two, a_, b_) == F(1, 6), 'b': cond(two, a_, c_) == F(1, 6), 'c': cond(two, c_, a_) == F(1, 6),
         'd': cond(two, a_, c_) == cond(two, c_, a_), 'e': cond(two, b_, c_) == 0}
M(L, 'items[3]', [k for k, v in truth.items() if v])
A(L, 'items[4]', F(13, 52) * F(12, 51) * F(11, 50), replaced=F(1, 4) ** 3)
S(L, 'items[4].explain.text', r'\tfrac{11}{850}', F(13, 52) * F(12, 51) * F(11, 50) == F(11, 850))
S(L, 'items[4].explain.text', 'Item 8 shows why', get(L, 'items[7].id') == 'h-order-three')
A(L, 'items[5]', 0.35 * 0.55 * 0.55, unrelated=0.35 ** 3, added=0.35 + 0.55 + 0.55, **{'two-only': 0.35 * 0.55})
S(L, 'items[5].explain.text', 'about two and a half times', 2.3 < 0.105875 / 0.042875 < 2.7)
hands, noace = math.comb(52, 3), math.comb(48, 3)
C(L, 'items[6]', 'a', F(4, hands - noace), b=F(3, 51) * F(2, 50), c=F(4, hands), d=F(4, 52) * F(3, 51))
S(L, 'items[6].explain.text', '4804', hands == 22100 and noace == 17296 and hands - noace == 4804)
ORD(L, 'items[7]', ['s1', 's2', 's3', 's4'])
TB(L, 'items[8]', {(0, 1): 0.05 * 0.002, (1, 1): 0.85 * 0.01, (2, 1): 0.10 * 0.08, (3, 1): 0.05 * 0.002 + 0.85 * 0.01 + 0.10 * 0.08})
S(L, 'items[8].explain.text', 'almost half the default risk', 0.45 < 0.008 / 0.0166 < 0.5)
A(L, 'items[9]', (0.033 - 0.6 * 0.015) / 0.4, difference=0.033 - 0.015, **{'equal-weights': (0.033 - 0.5 * 0.015) / 0.5, 'no-divide': 0.024})
M(L, 'items[10]', ['between', 'equal'])
S(L, 'items[11].model', r'\tfrac{3}{10} + \tfrac{1}{10} = \tfrac{2}{5}', F(3, 5) * F(2, 4) + F(2, 5) * F(1, 4) == F(2, 5))
ok('homework-1 rubric total 10', sum(r['points'] for r in get(L, 'items[11].rubric')) == 10)
# Monte Carlo: all aces given at least one ace
fulldeck = [r for r in range(13) for _ in range(4)]


def aces(r):
    h = r.sample(fulldeck, 3)
    k = h.count(0)
    return k >= 1, k == 3


m = mc_cond(aces, 1500000, 21)
ok(f'homework-1 MC all aces given one {m:.5f} vs 1/1201', abs(m - 1 / 1201) < 0.0002)

# ---------------- problems-1 ----------------
L = 'problems-1'
d8 = list(product(range(1, 9), repeat=2))
t10 = lambda o: o[0] + o[1] == 10
h8 = lambda o: 8 in o
I = 'items[0].parts'
A(L, I + '[0]', prob(d8, t10), unordered=F(4, 64), **{'double-five': F(8, 64), 'six-sided': F(3, 36)})
A(L, I + '[1]', cond(d8, t10, h8), sixteen=F(2, 16), whole=F(2, 64), **{'no-news': F(7, 64)})
A(L, I + '[2]', cond(d8, h8, t10), turned=F(2, 15), **{'eight-pairs': F(2, 8), 'one-order': F(1, 7)})
A(L, I + '[3]', prob(d8, lambda o: t10(o) and h8(o)), added=F(7, 64) + F(2, 7),
  **{'plain-product': F(7, 64) * F(15, 64), 'eight-slip': F(7, 64) * F(1, 4)})
wl = ['B'] * 5 + ['M'] * 4
w2 = list(permutations(range(9), 2))
w3 = list(permutations(range(9), 3))
k = lambda p: ''.join(wl[i] for i in p)
I = 'items[1].parts'
A(L, I + '[0]', prob(w2, lambda p: k(p) == 'BB'), replace=F(5, 9) ** 2, **{'fixed-bottom': F(5, 9) * F(4, 9), 'same-count': F(5, 9) * F(5, 8)})
A(L, I + '[1]', cond(w3, lambda p: k(p)[2] == 'M', lambda p: k(p)[:2] == 'BB'), bank=F(3, 7), **{'full-list': F(4, 9), 'one-gone': F(4, 8)})
bbm = prob(w3, lambda p: k(p) == 'BBM')
A(L, I + '[2]', bbm, replace=F(5, 9) ** 2 * F(4, 9), added=F(5, 18) + F(4, 7), **{'replace-slip': F(5, 9) ** 2 * F(4, 7)})
two_b = prob(w3, lambda p: k(p).count('B') == 2)
A(L, I + '[3]', two_b, **{'one-order': bbm, 'six-orders': 6 * bbm, 'replace-slip': 3 * F(5, 9) ** 2 * F(4, 9)})
A(L, I + '[4]', cond(w3, lambda p: k(p)[2] == 'M', lambda p: k(p).count('B') == 2),
  **{'no-news': F(4, 9), 'not-divided': bbm, 'six-slip': F(1, 6)})
first = ltp([0.5, 0.3, 0.2], [0.6, 0.8, 0.9])
I = 'items[2].parts'
A(L, I + '[0]', 0.5 * 0.6, added=1.1, **{'branch-only': 0.6})
A(L, I + '[1]', first, average=(0.6 + 0.8 + 0.9) / 3, **{'x-only': 0.3, 'rates-added': 2.3})
within = first + (1 - first) * 0.8
avg = (0.6 + 0.8 + 0.9) / 3
A(L, I + '[2]', within, both=first * 0.8, **{'second-only': (1 - first) * 0.8, 'average-slip': avg + (1 - avg) * 0.8})
zf = 0.9 + 0.1 * 0.8
A(L, I + '[3]', zf, product=0.72, **{'no-resend': 0.9})
C(L, I + '[4]', 'z-first')
S(L, I + '[4].feedback.correct', '0.036', abs(zf - within - 0.036) < 1e-9)
dl = ['G'] * 4 + ['N'] * 6
q3 = list(permutations(range(10), 3))
kk = lambda p: ''.join(dl[i] for i in p)
stop = lambda n: (lambda p: kk(p).find('G') == n - 1)
I = 'items[3].parts'
A(L, I + '[0]', prob(q3, stop(2)), replace=0.6 * 0.4, **{'cond-only': F(4, 9)})
A(L, I + '[1]', prob(q3, stop(3)), replace=0.6 * 0.6 * 0.4, **{'last-factor': F(4, 8), 'two-misses': F(6, 10) * F(5, 9)})
w3c = prob(q3, lambda p: 'G' in kk(p))
A(L, I + '[2]', w3c, replace=0.4 + 0.24 + 0.144, product=F(4, 10) * F(4, 15) * F(1, 6), **{'no-first': F(4, 15) + F(1, 6)})
S(L, I + '[2].explain.text', r'= \tfrac{1}{6}', prob(q3, lambda p: 'G' not in kk(p)) == F(1, 6))
A(L, I + '[3]', cond(q3, stop(2), lambda p: 'G' in kk(p) and not stop(1)(p)),
  **{'keeps-call-1': F(4, 15) / F(5, 6), 'no-news': F(4, 15), 'third-call': cond(q3, stop(3), lambda p: 'G' in kk(p) and not stop(1)(p)),
     'replace-slip': 0.24 / 0.384})

done()
