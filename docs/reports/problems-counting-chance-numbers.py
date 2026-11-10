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

# ---------------------------------------------------------------- report
results = lv1.results
bad = [r for r in results if not r[0]]
print(f'problems-counting-chance: {len(results) - len(bad)} of {len(results)} checks passed')
sys.exit(1 if bad else 0)
