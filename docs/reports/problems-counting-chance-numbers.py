"""Number recompute for the counting-chance problem sets (docs/briefs/chained.md check 1).

Every part's answer is computed twice: exactly (fractions or sympy) and by a second method (enumeration of the
sample space, or a seeded simulation where enumeration is too large). Every wrong value is recomputed from the
slip it names and shown to lie outside the answer's tolerance (lv.check_wrongs). Stated numbers in feedback and
explanations are tied to their text with lv.expect.
Run: <scratchpad>/venv/bin/python docs/reports/problems-counting-chance-numbers.py  (exit 0 on success)
"""
import itertools
import json
import os
import random
import sys
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'counting-chance')
RNG = random.Random(20261110)


def load(lv, n):
    with open(os.path.join(COURSE, f'problems-{n}.json'), encoding='utf8') as f:
        lv.files[f'problems-{n}'] = json.load(f)
    return f'problems-{n}'


def widget(lv, ref, i, j):
    return lv.files[ref]['items'][i]['parts'][j]['widget']


def answer(lv, ref, i, j, exact, second, label, second_tol=1e-12):
    """exact: Fraction / int / sympy value; second: the same value by another method."""
    ex = float(exact)
    lv.claim(abs(ex - float(second)) <= second_tol, f'{ref} item {i} part {j + 1} ({label}): two methods agree {ex:.6g} vs {float(second):.6g}')
    w = widget(lv, ref, i, j)
    tol = w['tol']['abs']
    lv.claim(abs(w['answer'] - ex) <= max(tol, 0) + 1e-9 if tol else w['answer'] == ex,
             f'{ref} item {i} part {j + 1} key {w["answer"]} equals {ex:.6g} within {tol}')
    if tol:   # the key itself is written to at least the asked precision
        lv.claim(abs(w['answer'] - ex) <= 5e-6, f'{ref} item {i} part {j + 1} key rounded to 6 figures')


def wrongs(lv, ref, i, j, values):
    """values: {wrong id: recomputed value}; every wrong entry must be listed and match."""
    w = widget(lv, ref, i, j)
    got = {x['id']: x['value'] for x in w.get('wrong', [])}
    lv.claim(set(got) == set(values), f'{ref} item {i} part {j + 1} wrong ids {sorted(got)} all recomputed')
    for k, v in values.items():
        if k in got:
            lv.claim(abs(got[k] - float(v)) <= 5e-6, f'{ref} item {i} part {j + 1} wrong "{k}" = {got[k]} recomputed {float(v):.6g}')


def stated(lv, ref, i, j, where, value, fmt=None):
    lv.expect(ref, f'items[{i}].parts[{j}].{where}', value, fmt)


def sim(event_fn, draw_fn, n=200000):
    return sum(1 for _ in range(n) if event_fn(draw_fn())) / n


# ---------------------------------------------------------------- Level 1
lv1 = Level('counting-chance', 1)
r1 = load(lv1, 1)

# P1: four-sided f, six-sided s
S = list(itertools.product(range(1, 5), range(1, 7)))
answer(lv1, r1, 0, 0, 4 * 6, len(S), '|S|')
wrongs(lv1, r1, 0, 0, {'added': 4 + 6, 'two-sixes': 6 * 6})
s_hi = F(sum(1 for f, s in S if s > f), len(S))
answer(lv1, r1, 0, 1, F(5 + 4 + 3 + 2, 24), s_hi, 'P(s > f)')
wrongs(lv1, r1, 0, 1, {'ties-in': F(sum(1 for f, s in S if s >= f), 24), 'thirty-six': F(14, 36), 'half': F(1, 2)})
ties = F(sum(1 for f, s in S if s == f), 24)
f_hi = 1 - s_hi - ties
answer(lv1, r1, 0, 2, f_hi, F(sum(1 for f, s in S if f > s), 24), 'P(f > s)')
wrongs(lv1, r1, 0, 2, {'no-ties': 1 - s_hi, 'tie': ties})
answer(lv1, r1, 0, 3, 12 * (1 - f_hi), sum(12 for f, s in S if s >= f) / 24, 'fair price of the game that pays unless f > s')
wrongs(lv1, r1, 0, 3, {'forgot-ties': 12 * s_hi, 'half': 6, 'wrong-way': 12 * f_hi})
for path, v in [('feedback.correct', 14), ('explain.text', 14), ('widget.accept', 7)]:
    stated(lv1, r1, 0, 1, path, v)
stated(lv1, r1, 0, 2, 'explain.text', 4)
stated(lv1, r1, 0, 3, 'explain.text', 9)

# P2: eight-sided die twice
S8 = list(itertools.product(range(1, 9), repeat=2))
A = {o for o in S8 if o[0] >= 7}
B = {o for o in S8 if abs(o[0] - o[1]) >= 6}
answer(lv1, r1, 1, 0, 3 * 2, len(B), '|B|')
wrongs(lv1, r1, 1, 0, {'one-order': len({tuple(sorted(o)) for o in B}), 'exactly-six': sum(1 for a, b in S8 if abs(a - b) == 6)})
answer(lv1, r1, 1, 1, 3, len(A & B), '|A and B|')
wrongs(lv1, r1, 1, 1, {'one-order': sum(1 for a, b in B if a < b and a >= 7), 'all-b': len(B)})
answer(lv1, r1, 1, 2, 16 + 6 - 3, len(A | B), '|A or B|')
wrongs(lv1, r1, 1, 2, {'no-overlap': len(A) + len(B), 'only-a': len(A ^ B)})
lv1.claim(len(A ^ B) == len(A) == 16, 'part 3 slip 16 is both |A| and the outcomes in exactly one of A, B')
lv1.claim(len(A) == 16, '|A| = 16 as the explanation states')
pAB = F(len(A | B), 64)
answer(lv1, r1, 1, 3, F(19, 64), sim(lambda o: o[0] >= 7 or abs(o[0] - o[1]) >= 6, lambda: (RNG.randint(1, 8), RNG.randint(1, 8))), 'P(A or B)', second_tol=0.005)
wrongs(lv1, r1, 1, 3, {'no-overlap': F(22, 64), 'unordered': F(19, 36), 'sixteen': F(19, 16)})
answer(lv1, r1, 1, 4, 16 * pAB, F(19, 4), 'fair price')
wrongs(lv1, r1, 1, 4, {'no-overlap': 16 * F(22, 64), 'half': 8, 'per-hit': 16})
stated(lv1, r1, 1, 3, 'explain.text', 0.2969, '0.2969')
stated(lv1, r1, 1, 4, 'explain.text', '4.75')

# P3: two feeds
p, q = sp.Rational(5, 100), sp.Rational(8, 100)
blk = p * q
answer(lv1, r1, 2, 0, blk, sim(lambda d: d[0] and d[1], lambda: (RNG.random() < 0.05, RNG.random() < 0.08), 400000), 'P(blackout)', second_tol=0.0006)
wrongs(lv1, r1, 2, 0, {'added': p + q, 'union': p + q - p * q})
up = 1 - blk
answer(lv1, r1, 2, 1, up, 1 - 0.05 * 0.08, 'P(at least one works)', 1e-12)
wrongs(lv1, r1, 2, 1, {'from-added': 1 - (p + q), 'both-work': (1 - p) * (1 - q), 'same': blk})
none20 = up ** 20
lv1.claim(abs(float(none20) - sp.exp(20 * sp.log(sp.Float(0.996, 30)))) < 1e-12, 'p3: 0.996^20 by logs agrees')
answer(lv1, r1, 2, 2, none20, float(sp.exp(20 * sp.log(sp.Float(0.996, 30)))), 'P(no blackout in 20)')
wrongs(lv1, r1, 2, 2, {'linear': 1 - 20 * blk, 'from-both-work': ((1 - p) * (1 - q)) ** 20, 'twenty-times': 20 * up})
ex4 = 1 - none20
# second method: sum over k >= 1 blackout days of the binomial terms
alt4 = sum(sp.binomial(20, k) * blk ** k * up ** (20 - k) for k in range(1, 21))
answer(lv1, r1, 2, 3, ex4, alt4, 'P(at least one blackout)')
wrongs(lv1, r1, 2, 3, {'adding': 20 * blk, 'none': none20})
stated(lv1, r1, 2, 2, 'explain.text', 0.9230, '0.9230')
stated(lv1, r1, 2, 3, 'explain.text', 0.0770, '0.0770')
stated(lv1, r1, 2, 3, 'widget.accept', 0.07703, '0.07703')

# P4: two four-sided dice, total 8
S4 = list(itertools.product(range(1, 5), repeat=2))
answer(lv1, r1, 3, 0, 16, len(S4), 'one throw outcomes')
wrongs(lv1, r1, 3, 0, {'unordered': len({tuple(sorted(o)) for o in S4}), 'added': 8, 'totals': len({a + b for a, b in S4})})
hit = F(sum(1 for a, b in S4 if a + b == 8), 16)
answer(lv1, r1, 3, 1, F(1, 16), hit, 'P(total 8)')
wrongs(lv1, r1, 3, 1, {'totals': F(1, 7), 'unordered': F(1, 10)})
miss10 = (1 - hit) ** 10
# second method: enumerate 16^10 runs by counting misses as 15^10 of 16^10
answer(lv1, r1, 3, 2, miss10, F(15 ** 10, 16 ** 10), 'P(no 8 in 10)')
wrongs(lv1, r1, 3, 2, {'linear': 1 - 10 * hit, 'from-unordered': F(9, 10) ** 10, 'from-totals': F(6, 7) ** 10})
answer(lv1, r1, 3, 3, 1 - miss10, sim(lambda r: any(x == 8 for x in r), lambda: [RNG.randint(1, 4) + RNG.randint(1, 4) for _ in range(10)], 200000), 'P(win, 10)', second_tol=0.005)
wrongs(lv1, r1, 3, 3, {'adding': 10 * hit, 'none': miss10})
nmin = next(n for n in range(1, 200) if 1 - (1 - hit) ** n > F(9, 10))
nmin2 = int(sp.floor(sp.log(sp.Rational(1, 10)) / sp.log(sp.Rational(15, 16)))) + 1
answer(lv1, r1, 3, 4, nmin, nmin2, 'smallest n with a win chance above 0.9')
wrongs(lv1, r1, 3, 4, {'adding': next(n for n in range(1, 100) if F(n, 16) > F(9, 10)),
                       'half': next(n for n in range(1, 100) if 1 - (1 - hit) ** n > F(1, 2)),
                       'one-short': nmin - 1})
lv1.claim(abs(float(1 - F(15, 16) ** 36) - 0.9021) < 0.00005 and abs(float(1 - F(15, 16) ** 35) - 0.8955) < 0.00005, 'part 5: 0.9021 at 36 and 0.8955 at 35')
lv1.claim(abs(float(1 - F(15, 16) ** 15) - 0.6202) < 0.00005 and abs(float(1 - F(15, 16) ** 11) - 0.5083) < 0.00005, 'part 5 byKey: 0.6202 at 15 and 0.5083 at 11')
lv1.claim(abs(float(sp.log(sp.Rational(1, 10)) / sp.log(sp.Rational(15, 16))) - 35.7) < 0.05, 'part 5 explain: n > 35.7')
stated(lv1, r1, 3, 4, 'feedback.byKey.adding', '0.6202')
stated(lv1, r1, 3, 4, 'feedback.byKey.half', '0.5083')

lv1.check_wrongs('problems-1')

# ---------------------------------------------------------------- Level 2
from math import comb, factorial, perm  # noqa: E402

lv2 = Level('counting-chance', 2)
r2 = load(lv2, 2)

# P1: relay team of 4 from 9, then running order; Ada = 0, Bea = 1
teams = list(itertools.combinations(range(9), 4))
answer(lv2, r2, 0, 0, comb(9, 4), len(teams), 'teams')
wrongs(lv2, r2, 0, 0, {'ordered': perm(9, 4), 'times': 9 * 4})
lineups = list(itertools.permutations(range(9), 4))
answer(lv2, r2, 0, 1, comb(9, 4) * factorial(4), len(lineups), 'line-ups')
wrongs(lv2, r2, 0, 1, {'times-four': 126 * 4, 'added': 126 + 24})
both = F(sum(1 for t in teams if 0 in t and 1 in t), len(teams))
answer(lv2, r2, 0, 2, F(comb(7, 2), comb(9, 4)), both, 'P(both in)')
wrongs(lv2, r2, 0, 2, {'one-named': F(4, 9), 'squared': F(4, 9) ** 2})
last2 = F(sum(1 for l in lineups if set(l[2:]) == {0, 1}), len(lineups))
answer(lv2, r2, 0, 3, both * F(2 * 2, 24), last2, 'P(last two legs)')
wrongs(lv2, r2, 0, 3, {'one-order': F(sum(1 for l in lineups if l[2:] == (0, 1)), len(lineups)), 'in-team': both, 'from-squared': F(4, 9) ** 2 * F(1, 6)})
lv2.claim(sum(1 for l in lineups if set(l[2:]) == {0, 1}) == 84, 'part 4: 84 line-ups of 3024')
stated(lv2, r2, 0, 0, 'explain.text', 3024)
stated(lv2, r2, 0, 2, 'explain.text', 21)
stated(lv2, r2, 0, 3, 'explain.text', 84)

# P2: 15 orders, 4 breaches, 3 picks without replacement; orders 0..3 breach
picks = list(itertools.permutations(range(15), 3))
clean = lambda o: o >= 4  # noqa: E731
answer(lv2, r2, 1, 0, F(11, 15), F(sum(1 for p_ in picks if clean(p_[0])), len(picks)), 'P(first clean)')
wrongs(lv2, r2, 1, 0, {'breach': F(4, 15)})
two = F(11, 15) * F(10, 14)
answer(lv2, r2, 1, 1, two, F(sum(1 for p_ in picks if clean(p_[0]) and clean(p_[1])), len(picks)), 'P(two clean)')
wrongs(lv2, r2, 1, 1, {'replace': F(11, 15) ** 2, 'fixed-bottom': F(11 * 10, 15 * 15), 'fixed-top': F(11, 15) * F(11, 14)})
three = two * F(9, 13)
answer(lv2, r2, 1, 2, three, F(comb(11, 3), comb(15, 3)), 'P(three clean)')
wrongs(lv2, r2, 1, 2, {'replace': F(11, 15) ** 3, 'fixed-bottom': F(11 * 10 * 9, 15 ** 3)})
answer(lv2, r2, 1, 3, 1 - three, F(sum(1 for p_ in picks if not all(map(clean, p_))), len(picks)), 'P(at least one breach)')
wrongs(lv2, r2, 1, 3, {'none': three, 'replace': 1 - F(11, 15) ** 3, 'adding': 3 * F(4, 15)})
# part 5: smallest number of picks for P(at least one breach) > 0.9, by running product and by the hypergeometric count
def none_by_product(k):
    pr = F(1)
    for i in range(k):
        pr *= F(11 - i, 15 - i)
    return pr
kmin = next(k for k in range(1, 12) if 1 - none_by_product(k) > F(9, 10))
kmin2 = next(k for k in range(1, 12) if 1 - F(comb(11, k), comb(15, k)) > F(9, 10))
answer(lv2, r2, 1, 4, kmin, kmin2, 'smallest number of picks')
lv2.claim(none_by_product(3) == three, 'the running product starts from 33/91 at 3 picks')
wrongs(lv2, r2, 1, 4, {'five': 5, 'adding': next(n for n in range(1, 20) if n * F(4, 15) > F(9, 10)),
                       'replace': next(n for n in range(1, 40) if 1 - F(11, 15) ** n > F(9, 10))})
for k, v in ((4, 0.7582), (5, 0.8462), (6, 0.9077)):
    lv2.claim(abs(float(1 - none_by_product(k)) - v) < 0.00005, f'breach chance at {k} picks is {v}')
lv2.claim(abs(float(33 * F(8, 12) / 91) - 0.2418) < 5e-5 and abs(float(none_by_product(5)) - 0.1538) < 5e-5 and abs(float(none_by_product(6)) - 0.0923) < 5e-5, 'running products 0.2418, 0.1538, 0.0923')
lv2.claim(comb(11, 6) == 462 and comb(15, 6) == 5005, 'C(11,6) = 462 and C(15,6) = 5005')
stated(lv2, r2, 1, 4, 'feedback.byKey.five', '0.8462')
stated(lv2, r2, 1, 4, 'feedback.byKey.adding', '0.7582')
stated(lv2, r2, 1, 1, 'explain.text', 0.5238, '0.5238')
stated(lv2, r2, 1, 2, 'explain.text', 0.3626, '0.3626')
stated(lv2, r2, 1, 3, 'explain.text', 0.6374, '0.6374')

# P3: 8 votes, 3 proposals
lists = list(itertools.product(range(3), repeat=8))
tallies = {tuple(v.count(k) for k in range(3)) for v in lists}
answer(lv2, r2, 2, 0, comb(10, 2), len(tallies), 'tallies')
wrongs(lv2, r2, 2, 0, {'distinct': 3 ** 8, 'at-least-one': comb(7, 2), 'stars-only': comb(8, 2)})
answer(lv2, r2, 2, 1, comb(10, 2) - comb(7, 2), sum(1 for t in tallies if 0 in t), 'tallies with a zero')
wrongs(lv2, r2, 2, 1, {'all-voted': comb(7, 2), 'unanimous': sum(1 for t in tallies if sorted(t) == [0, 0, 8])})
w = widget(lv2, r2, 2, 2)
lv2.claim([o['id'] for o in w['options'] if o.get('correct')] == ['right'], 'part 3: one correct option, "right"')
n332 = sum(1 for v in lists if tuple(v.count(k) for k in range(3)) == (3, 3, 2))
n800 = sum(1 for v in lists if tuple(v.count(k) for k in range(3)) == (8, 0, 0))
lv2.claim(n332 == factorial(8) // (6 * 6 * 2) == 560 and n800 == 1, 'part 3: 3,3,2 from 560 lists ("hundreds"), 8,0,0 from one')
una = F(3, 3 ** 8)
answer(lv2, r2, 2, 3, una, F(sum(1 for v in lists if len(set(v)) == 1), len(lists)), 'P(unanimous)')
wrongs(lv2, r2, 2, 3, {'tallies': F(3, 45), 'one-proposal': F(1, 3 ** 8)})
lv2.claim(abs(widget(lv2, r2, 2, 3)['answer'] - float(una)) <= 5e-10, 'P(unanimous) key to 9 places')
stated(lv2, r2, 2, 2, 'explain.text', 6561)
stated(lv2, r2, 2, 3, 'explain.text', 2187)

# P4: 30 feeds, audit of 5; yours are 0..4
N = comb(30, 5)
answer(lv2, r2, 3, 0, N, perm(30, 5) // factorial(5), 'sets')
wrongs(lv2, r2, 3, 0, {'ordered': perm(30, 5), 'power': 30 ** 5})


def hyper(k):  # second method: count sets by brute force over the 25 others is too large; use Vandermonde check
    return comb(5, k) * comb(25, 5 - k)


lv2.claim(sum(hyper(k) for k in range(6)) == N, 'Vandermonde: the hypergeometric counts sum to C(30,5)')
p_ex3 = F(hyper(3), N)
answer(lv2, r2, 3, 1, p_ex3, sim(lambda s_: len(s_ & {0, 1, 2, 3, 4}) == 3, lambda: set(RNG.sample(range(30), 5)), 400000), 'P(exactly 3)', second_tol=0.0012)
wrongs(lv2, r2, 3, 1, {'no-others': F(comb(5, 3), N), 'others-ordered': F(comb(5, 3) * 25 * 24, N)})
p_ge3 = F(hyper(3) + hyper(4) + hyper(5), N)
answer(lv2, r2, 3, 2, p_ge3, 1 - F(hyper(0) + hyper(1) + hyper(2), N), 'P(at least 3)')
wrongs(lv2, r2, 3, 2, {'exactly': p_ex3, 'double-four': F(3000 + 250 + 1, N)})
lv2.claim(hyper(4) == 125 and hyper(5) == 1 and hyper(3) == 3000, 'stated counts 3000, 125, 1')
q4 = 1 - (1 - p_ge3) ** 4
alt = sum(comb(4, k) * p_ge3 ** k * (1 - p_ge3) ** (4 - k) for k in range(1, 5))
answer(lv2, r2, 3, 3, q4, alt, 'P(in 4 quarters)')
wrongs(lv2, r2, 3, 3, {'adding': 4 * p_ge3, 'from-exactly': 1 - (1 - p_ex3) ** 4, 'none': (1 - p_ge3) ** 4})
stated(lv2, r2, 3, 0, 'explain.text', 17100720)
stated(lv2, r2, 3, 1, 'explain.text', 0.02105, '0.02105')
stated(lv2, r2, 3, 2, 'explain.text', 0.02194, '0.02194')
stated(lv2, r2, 3, 3, 'explain.text', 0.91510, '0.91510')
stated(lv2, r2, 3, 3, 'explain.text', 0.0849, '0.0849')
lv2.claim(abs(float((1 - p_ge3) ** 4) - 0.91510) < 0.000005, '0.91510 to 5 places')

lv2.check_wrongs('problems-2')

# ---------------------------------------------------------------- Level 3
lv3 = Level('counting-chance', 3)
r3 = load(lv3, 3)


def no_clash(n, d=50):
    p_ = F(1)
    for i in range(n):
        p_ *= F(d - i, d)
    return p_


def sim_clash(n, d=50, trials=200000):
    return sum(1 for _ in range(trials) if len({RNG.randrange(d) for _ in range(n)}) < n) / trials


# P1: shards
nc5 = no_clash(5)
answer(lv3, r3, 0, 0, nc5, 1 - sim_clash(5), 'P(no clash, 5)', second_tol=0.004)
wrongs(lv3, r3, 0, 0, {'your-shard': F(49, 50) ** 4, 'last-only': F(46, 50)})
answer(lv3, r3, 0, 1, 1 - nc5, F(comb(50, 5) * factorial(5), 1) / 50 ** 5 * -1 + 1, 'P(clash, 5)')
wrongs(lv3, r3, 0, 1, {'none': nc5, 'from-your-shard': 1 - F(49, 50) ** 4, 'pairs': F(comb(5, 2), 50)})
nmin3 = next(n for n in range(1, 51) if 1 - no_clash(n) > F(1, 2))
answer(lv3, r3, 0, 2, nmin3, 9 if (sim_clash(9) > 0.5 and sim_clash(8) < 0.5) else -1, 'smallest n (simulated at 8 and 9)')
wrongs(lv3, r3, 0, 2, {'half': 25, 'union-bound': next(n for n in range(2, 51) if F(comb(n, 2), 50) >= F(1, 2)), 'root': 7})
for n_, v in [(6, '0.73224'), (7, '0.64437'), (8, '0.55416'), (9, '0.46550')]:
    lv3.claim(f'{float(no_clash(n_)):.5f}' == v, f'no clash at {n_} = {v}')
for n_, v in [(7, 0.3556), (8, 0.4458), (9, 0.5345)]:
    lv3.claim(abs(float(1 - no_clash(n_)) - v) < 0.00005, f'clash at {n_} = {v}')
stated(lv3, r3, 0, 2, 'explain.text', '0.46550')
stated(lv3, r3, 0, 2, 'feedback.byKey.union-bound', '0.4458')
stated(lv3, r3, 0, 2, 'feedback.byKey.root', '0.3556')
ub = F(comb(nmin3, 2), 50)
answer(lv3, r3, 0, 3, ub, F(sum(1 for _ in itertools.combinations(range(9), 2)), 50), 'union bound at 9')
wrongs(lv3, r3, 0, 3, {'one-symbol': F(8, 50), 'exact': 1 - no_clash(9), 'ordered-pairs': F(72, 50)})
stated(lv3, r3, 0, 3, 'explain.text', '0.5345')

# P2: three borrowers; check with an explicit Venn region model at t = 0.015 and t = 0
PA, PB, PC = sp.Rational(10, 100), sp.Rational(8, 100), sp.Rational(6, 100)
PAB, PAC, PBC = sp.Rational(3, 100), sp.Rational(2, 100), sp.Rational(15, 1000)
t = sp.Symbol('t')
uAB = PA + PB - PAB
answer(lv3, r3, 1, 0, uAB, 0.10 + 0.08 - 0.03, 'P(A or B)')
wrongs(lv3, r3, 1, 0, {'no-overlap': PA + PB, 'both': PAB})
u3 = sp.expand(uAB + PC - (PAC + PBC - t))
lv3.claim(sp.simplify(u3 - (PA + PB + PC - PAB - PAC - PBC + t)) == 0, 'part 2: split form equals the three-event rule')
lv3.claim(sp.simplify(u3 - (sp.Rational(175, 1000) + t)) == 0, 'part 2: 0.175 + t')
w = widget(lv3, r3, 1, 1)
for form in w['accept']:
    lv3.claim(sp.simplify(sp.sympify(form) - u3) == 0, f'part 2 accept form {form} equals 0.175 + t')
for wr in w['wrong']:
    lv3.claim(sp.simplify(sp.sympify(wr['tex']) - u3) != 0, f'part 2 wrong {wr["tex"]} differs from 0.175 + t')


def regions(tv):
    """The seven Venn regions for a given triple overlap; all must be >= 0 for tv to be possible."""
    abc = tv
    ab, ac, bc = PAB - tv, PAC - tv, PBC - tv
    a = PA - ab - ac - abc
    b = PB - ab - bc - abc
    c = PC - ac - bc - abc
    return [a, b, c, ab, ac, bc, abc]


tmax = max(sp.Rational(k, 10000) for k in range(0, 1001) if all(r >= 0 for r in regions(sp.Rational(k, 10000))))
answer(lv3, r3, 1, 2, min(PAB, PAC, PBC), tmax, 't max (grid search over feasible Venn regions)')
wrongs(lv3, r3, 1, 2, {'largest-pair': PAB, 'smallest-single': PC, 'product': PA * PB * PC})
umax = u3.subs(t, tmax)
answer(lv3, r3, 1, 3, umax, sum(regions(tmax)), 'largest P(union) = sum of regions')
wrongs(lv3, r3, 1, 3, {'singles': PA + PB + PC, 'smallest': u3.subs(t, 0), 'from-largest-pair': u3.subs(t, PAB)})
lv3.claim(all(r >= 0 for r in regions(0)) and sum(regions(0)) == sp.Rational(175, 1000), 't = 0 is possible and gives 0.175')

# P3: aces and kings
N52 = comb(52, 5)
answer(lv3, r3, 2, 0, comb(44, 5), sum(comb(4, a) * comb(4, k) * comb(44, 5 - a - k) for a in [0] for k in [0]), 'no ace no king')
wrongs(lv3, r3, 2, 0, {'no-ace-only': comb(48, 5), 'one-each': comb(50, 5)})
pA = F(N52 - comb(48, 5), N52)
pU = 1 - F(comb(44, 5), N52)
both_direct = sum(comb(4, a) * comb(4, k) * comb(44, 5 - a - k) for a in range(1, 5) for k in range(1, 5) if a + k <= 5)
answer(lv3, r3, 2, 1, pU, F(sum(comb(4, a) * comb(4, k) * comb(44, 5 - a - k) for a in range(5) for k in range(5) if a + k <= 5 and a + k > 0), N52), 'P(A or K)')
wrongs(lv3, r3, 2, 1, {'none': 1 - pU, 'added': 2 * pA})
lv3.claim(abs(float(pA) - 0.341158) < 5e-7, 'P(A) = 0.341158 as stated')
pAK = 2 * pA - pU
answer(lv3, r3, 2, 2, pAK, F(both_direct, N52), 'P(A and K), direct sum over ace and king counts')
wrongs(lv3, r3, 2, 2, {'product': pA ** 2, 'once': pU - pA})
answer(lv3, r3, 2, 3, pAK * N52, both_direct, 'hands with an ace and a king')
wrongs(lv3, r3, 2, 3, {'union': N52 - comb(44, 5), 'from-product': 302490, 'from-chance': round(0.100179 * N52)})
lv3.claim(round(0.100179 * N52) == 260361 and abs(0.100179 * N52 - 260360) > 0.5, 'multiplying the rounded chance 0.100179 by 2,598,960 gives 260,361 (not 260,360)')
stated(lv3, r3, 2, 3, 'question', 886656)
stated(lv3, r3, 2, 3, 'question', 1512952)
fp = [x for x in widget(lv3, r3, 2, 3)['wrong'] if x['id'] == 'from-product'][0]
lo, hi = float(pA ** 2) * N52, 0.116389 * N52
lv3.claim(all(abs(v - fp['value']) <= fp['tol']['abs'] for v in (round(lo), round(hi))), f'independence slip band covers {lo:.1f} (exact) and {hi:.1f} (from the rounded square 0.116389)')
lv3.claim(abs(fp['value'] - both_direct) > fp['tol']['abs'], 'independence slip band stays clear of 260,360')
lv3.claim(N52 - comb(48, 5) == 886656 and N52 - comb(44, 5) == 1512952, 'stated counts 886,656 and 1,512,952')
stated(lv3, r3, 2, 3, 'explain.text', 886656)
stated(lv3, r3, 2, 3, 'explain.text', 1512952)

# P4: short deck, ranks 0..4, suits 0..3
deck = [(r_, s_) for r_ in range(5) for s_ in range(4)]
deals3 = list(itertools.permutations(range(20), 3))
answer(lv3, r3, 3, 0, F(16, 19), F(sum(1 for a, b in itertools.permutations(range(20), 2) if deck[a][0] != deck[b][0]), 20 * 19), 'P(new rank)')
wrongs(lv3, r3, 3, 0, {'replace': F(16, 20), 'same': F(3, 19)})
p3r = F(16, 19) * F(12, 18)
answer(lv3, r3, 3, 1, p3r, F(sum(1 for d in deals3 if len({deck[i][0] for i in d}) == 3), len(deals3)), 'P(three ranks)')
wrongs(lv3, r3, 3, 1, {'replace': F(16, 20) * F(12, 20), 'fixed-bottom': F(16, 19) * F(12, 19)})
hands = list(itertools.combinations(range(20), 4))
p4r = p3r * F(8, 17)
n4 = sum(1 for h in hands if len({deck[i][0] for i in h}) == 4)
answer(lv3, r3, 3, 2, p4r, F(n4, len(hands)), 'P(four ranks)')
wrongs(lv3, r3, 3, 2, {'replace': F(16 * 12 * 8, 20 ** 3), 'fixed-bottom': F(16 * 12 * 8, 19 ** 3)})
answer(lv3, r3, 3, 3, len(hands) * p4r, comb(5, 4) * 4 ** 4, 'hands with four ranks')
wrongs(lv3, r3, 3, 3, {'suits-only': 4 ** 4, 'ordered': 1280 * 24})


def cls(h):
    c = sorted((sum(1 for i in h if deck[i][0] == r_) for r_ in range(5)), reverse=True)
    return {(1, 1, 1, 1): 'none', (2, 1, 1, 0): 'pair', (2, 2, 0, 0): 'two', (3, 1, 0, 0): 'trips', (4, 0, 0, 0): 'quads'}[tuple(c[:4])]


from collections import Counter  # noqa: E402
cnt = Counter(cls(h) for h in hands)
lv3.claim(len(hands) == 4845 and cnt['two'] == 360 and cnt['trips'] == 320 and cnt['quads'] == 5 and cnt['none'] == 1280,
          f'short-deck classes by enumeration: {dict(cnt)}')
answer(lv3, r3, 3, 4, 4845 - 1280 - 360 - 320 - 5, cnt['pair'], 'one pair')
wrongs(lv3, r3, 3, 4, {'at-least-pair': 4845 - 1280, 'no-quads': 4845 - 1280 - 360 - 320, 'two-pair-ordered': 4845 - 1280 - 720 - 320 - 5, 'no-two-pair': 4845 - 1280 - 320 - 5})
lv3.claim(cnt['pair'] * 2 > 4845, 'one pair is more than half of all hands')
lv3.claim(5 * 4 * comb(4, 2) * comb(4, 2) == 720 and comb(5, 2) * comb(4, 2) ** 2 == 360, 'two pair: ordered ranks 720, unordered 360')

# typed share and difficulty rules, every set
for lv_, ref in [(lv1, r1), (lv2, r2), (lv3, r3)]:
    its = lv_.files[ref]['items']
    kinds = [p_['widget']['kind'] for it in its for p_ in it['parts']]
    typed = sum(1 for k in kinds if k in ('numeric', 'expression'))
    lv_.claim(3 * typed >= 2 * len(kinds), f'{ref}: {typed} of {len(kinds)} parts typed (at least two thirds)')
    lv_.claim(all(3 <= it['difficulty'] <= 5 for it in its) and any(it['difficulty'] == 5 for it in its), f'{ref}: difficulty 3 to 5 with a 5')
    lv_.claim(all(3 <= len(it['parts']) <= 5 for it in its) and 3 <= len(its) <= 5, f'{ref}: 3 to 5 items of 3 to 5 parts')

lv3.check_wrongs('problems-3')

# every numeric part: form stated, a value rounded as asked is accepted, and each value the part's own feedback prints is accepted
import re  # noqa: E402


def form_checks(lv_, ref):
    for ii, it in enumerate(lv_.files[ref]['items']):
        for jj, p_ in enumerate(it['parts']):
            w = p_['widget']
            if w['kind'] != 'numeric':
                continue
            tag = f'{ref} {it["id"]} p{jj + 1}'
            a, tol, q = w['answer'], w['tol'].get('abs', 0), p_['question']
            whole = float(a).is_integer() and tol == 0
            lv_.claim(whole or w.get('unit') == '£' or bool(re.search(r'\bGive\b', q)), f'{tag}: a sentence states the form wanted (a whole count or a price needs none)')
            m = re.search(r'(\d+) decimal places?|decimal to (\d+) places?', q)
            if m:
                n = int(m.group(1) or m.group(2))
                lv_.claim(tol + 1e-12 >= 0.5 * 10 ** -n, f'{tag}: tolerance {tol} accepts a value rounded to {n} places')
            for t in (p_['feedback'].get('correct', ''), p_['explain']['text'], w.get('accept', '')):
                t = t.replace('{,}', '').replace(',', '').replace('£', '')
                for v in re.findall(r'(?:\\approx|about) \$?(-?\d+\.?\d*)', t):
                    v = float(v.rstrip('.'))
                    if a and not whole and abs(v - a) <= 0.05 * abs(a):
                        lv_.claim(abs(v - a) <= tol + 1e-9, f'{tag}: the printed {v} is accepted by key {a} (tol {tol})')


for lv_, ref in [(lv1, r1), (lv2, r2), (lv3, r3)]:
    form_checks(lv_, ref)

# ---------------------------------------------------------------- report
results = lv1.results + lv2.results + lv3.results
bad = [r for r in results if not r[0]]
print(f'problems-counting-chance: {len(results) - len(bad)} of {len(results)} checks passed')
sys.exit(1 if bad else 0)
