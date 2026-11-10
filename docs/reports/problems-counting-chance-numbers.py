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
answer(lv1, r1, 0, 3, 12 * f_hi, sum(12 for f, s in S if f > s) / 24, 'fair price')
wrongs(lv1, r1, 0, 3, {'no-ties': 12 * (1 - s_hi), 'half': 6, 'other-die': 12 * s_hi})
for path, v in [('feedback.correct', 14), ('explain.text', 14), ('widget.accept', 7)]:
    stated(lv1, r1, 0, 1, path, v)
stated(lv1, r1, 0, 2, 'explain.text', 4)
stated(lv1, r1, 0, 3, 'explain.text', 3)

# P2: eight-sided die twice
S8 = list(itertools.product(range(1, 9), repeat=2))
A = {o for o in S8 if o[0] >= 7}
B = {o for o in S8 if abs(o[0] - o[1]) >= 6}
answer(lv1, r1, 1, 0, 3 * 2, len(B), '|B|')
wrongs(lv1, r1, 1, 0, {'one-order': len({tuple(sorted(o)) for o in B}), 'exactly-six': sum(1 for a, b in S8 if abs(a - b) == 6)})
answer(lv1, r1, 1, 1, 3, len(A & B), '|A and B|')
wrongs(lv1, r1, 1, 1, {'one-order': sum(1 for a, b in B if a < b and a >= 7), 'all-b': len(B)})
answer(lv1, r1, 1, 2, 16 + 6 - 3, len(A | B), '|A or B|')
wrongs(lv1, r1, 1, 2, {'no-overlap': len(A) + len(B), 'exactly-one': len(A ^ B)})
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
nmin = next(n for n in range(1, 100) if 1 - (1 - hit) ** n > F(1, 2))
nmin2 = int(sp.ceiling(sp.log(sp.Rational(1, 2)) / sp.log(sp.Rational(15, 16))))
answer(lv1, r1, 3, 4, nmin, nmin2, 'smallest n')
wrongs(lv1, r1, 3, 4, {'adding': next(n for n in range(1, 100) if n * hit >= F(1, 2)), 'ten': 10})
lv1.claim(abs(float(1 - F(15, 16) ** 8) - 0.4033) < 0.00005, 'part 5 byKey: at n = 8 the bet wins with 0.4033')
lv1.claim(abs(float(F(15, 16) ** 11) - 0.4917) < 0.00005 and abs(float(1 - F(15, 16) ** 11) - 0.5083) < 0.00005, 'part 5: 0.4917 and 0.5083')
stated(lv1, r1, 3, 4, 'explain.text', '0.4917')
stated(lv1, r1, 3, 4, 'explain.text', '0.5083')
stated(lv1, r1, 3, 4, 'feedback.byKey.adding', '0.4033')

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
samples = list(itertools.combinations(range(15), 3))
answer(lv2, r2, 1, 4, comb(15, 3) * (1 - three), sum(1 for s_ in samples if not all(map(clean, s_))), 'samples with a breach')
wrongs(lv2, r2, 1, 4, {'ordered': 290 * 6, 'none': comb(11, 3)})
lv2.claim(len(samples) == 455, '455 samples')
stated(lv2, r2, 1, 1, 'explain.text', 0.5238, '0.5238')
stated(lv2, r2, 1, 2, 'explain.text', 0.3626, '0.3626')
stated(lv2, r2, 1, 3, 'explain.text', 0.6374, '0.6374')
stated(lv2, r2, 1, 4, 'explain.text', 165)

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

# ---------------------------------------------------------------- report
results = lv1.results + lv2.results
bad = [r for r in results if not r[0]]
print(f'problems-counting-chance: {len(results) - len(bad)} of {len(results)} checks passed')
sys.exit(1 if bad else 0)
