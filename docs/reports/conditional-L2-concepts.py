"""Concept audit, conditional level 2 (l7 to l12, fluency-l7, review-2, homework-2 with its
performance task, problems-2). Every graded or stated probability recomputed from a joint
distribution with exact fractions; seeded Monte Carlo for repeated tests; counterexamples for
the wording findings. Run from the repo root:
    python3 docs/reports/conditional-L2-concepts.py
Exit 0 means every claim checked holds. Ledger: docs/reports/audit-conditional-1-3-ledger.md.
"""
import math
import os
import random
import sys
from fractions import Fraction as F
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conditional_concepts_lib import cid, eq, get, load, ok, report, says, tab


def post(b, h, f):
    """P(H | E) from base rate b, P(E | H) = h, P(E | not H) = f, by the joint distribution."""
    b, h, f = F(b), F(h), F(f)
    return b * h / (b * h + (1 - b) * f)


def pe(b, h, f):
    return F(b) * F(h) + (1 - F(b)) * F(f)


def many(priors, liks):
    prods = [F(p) * F(l) for p, l in zip(priors, liks)]
    return [x / sum(prods) for x in prods]


def odds(p):
    return F(p) / (1 - F(p))


def prob(o):
    return F(o) / (1 + F(o))


D = lambda s: F(s)  # decimal string to exact fraction

# ---------------------------------------------------------------- l7 turning the condition around
L = 'l7-turning-around'
ill_pos, ill_neg, well_pos, well_neg = 8, 2, 18, 72
ok(ill_pos + ill_neg + well_pos + well_neg == 100, 'l7 100 people')
eq(L, 'screens[1]', F(ill_pos, ill_pos + ill_neg))
cid(L, 'screens[2]', ['AB', 'B'])
eq(L, 'screens[3]', F(ill_pos, ill_pos + well_pos))
eq(L, 'screens[4]', D('0.1') * D('0.8'))
eq(L, 'screens[5]', pe('0.1', '0.8', '0.2'))
eq(L, 'screens[6]', post('0.1', '0.8', '0.2'), atol=6e-3)
ok(post('0.1', '0.8', '0.2') == F(ill_pos, ill_pos + well_pos), 'l7 s6 rates and counts agree at 8/26')
eq(L, 'screens[7]', post('0.2', '0.9', '0.3'))
cid(L, 'screens[8]', ['d1', 'd2', 'd3', 'd4'])
eq(L, 'screens[9]', post('0.55', '0.8', '0.3'))
eq(L, 'quiz[0]', F(4, 12))
eq(L, 'quiz[1]', D('0.6') * D('0.3') / D('0.4'))
eq(L, 'quiz[2]', D('0.6') * D('0.25') / D('0.25'))
cid(L, 'quiz[3]', ['right'])
# summary: with P(A and B) > 0 the two directions agree exactly when P(A) = P(B); random joint tables
rng = random.Random(7)
good = True
for _ in range(20000):
    j, a_only, b_only = rng.uniform(0.01, 0.3), rng.uniform(0, 0.3), rng.uniform(0, 0.3)
    pa, pb = j + a_only, j + b_only
    good &= (abs(j / pa - j / pb) < 1e-12) == (abs(pa - pb) < 1e-12)
ok(good, 'l7 summary P(A|B) = P(B|A) exactly when P(A) = P(B), given a positive overlap')
# review-2 r-bayes-form says "equal only when P(A) = P(B)": disjoint events with unequal chances also agree (finding 13)
ok(F(0) / F(3, 10) == F(0) / F(2, 10), 'review-2 r-bayes-form: disjoint A, B with P(A) != P(B) have equal conditionals, both 0 (finding 13)')

# fluency-l7: every generated variant, key recomputed from the joint distribution
fl = load('fluency-l7-turning-around')['families']
bad = 0
n = 0
for tot in (100, 200, 400):
    for a in range(5, 31):
        for c in range(1, 10):
            for b in range(3, 41):
                if b == c:
                    continue
                n += 1
                key = F(a, a + b)
                env = {'a': a, 'b': b, 'c': c, 'tot': tot}
                got = eval(fl[0]['let']['key'], {}, env)
                bad += abs(got - key) > 1e-12 or a + c + b > tot
                bad += key in (F(a, a + c), F(a, tot))          # the two wrong values never equal the key
ok(bad == 0, f'fluency-l7 from-counts: {n} variants, key a/(a+b), counts fit in the total, wrongs distinct')
bad = n = 0
for pp in (1, 2, 5, 10, 20, 25, 30, 40):
    for s in range(60, 96, 5):
        for f in range(5, 31, 5):
            n += 1
            key = post(F(pp, 100), F(s, 100), F(f, 100))
            got = eval(fl[1]['let']['key'], {}, {'pp': pp, 's': s, 'f': f})
            bad += abs(got - float(key)) > 1e-12
ok(bad == 0, f'fluency-l7 from-rates: {n} variants, key is the posterior')
bad = n = 0
for pp in (5, 10, 15, 20, 25, 30, 40):
    for s in range(60, 96, 5):
        for f in range(5, 41, 5):
            n += 1
            got = eval(fl[2]['let']['key'], {}, {'pp': pp, 's': s, 'f': f})
            bad += abs(got - float(pe(F(pp, 100), F(s, 100), F(f, 100)))) > 1e-12
ok(bad == 0, f'fluency-l7 every-positive-path: {n} variants, key is P(+)')

# ---------------------------------------------------------------- l8 base rates
L = 'l8-base-rates'
p1 = post('0.01', '0.9', '0.05')
ok(abs(p1 - F(15, 100)) < F(1, 100), 'l8 s0 about 15%')
cid(L, 'screens[0]', ['right'])
ok(post('0.05', '0.9', '0.05') < F(1, 2) < post('0.06', '0.9', '0.05'), 'l8 s1 crosses one half between 5% and 6%')
ok(round(float(post('0.05', '0.9', '0.05')), 2) == 0.49 and round(float(post('0.06', '0.9', '0.05')), 2) == 0.53, 'l8 s1 hint 0.49 and 0.53')
cid(L, 'screens[1]', ['right'])
eq(L, 'screens[2]', pe('0.01', '0.9', '0.05'), atol=1e-6)
eq(L, 'screens[3]', p1)
ok(15 < p1 / F(1, 100) < 16, 'l8 s3 the positive raised the chance about fifteenfold')
eq(L, 'screens[4]', 1 - p1)
eq(L, 'screens[5]', post('0.5', '0.9', '0.05'))
ok(post('0.5', '0.9', '0.05') == D('0.9') / (D('0.9') + D('0.05')), 'l8 s5 an even base rate cancels')
ok(post('0.3', '0.9', '0.05') > p1 and abs(post('0.3', '0.9', '0.05') - D('0.885')) < D('0.001'), 'l8 s6 clinic B about 0.89')
cid(L, 'screens[6]', ['right'])
cid(L, 'screens[7]', ['right'])
eq(L, 'screens[8]', post('0.002', '0.95', '0.01'))
eq(L, 'screens[9]', post('0.05', '0.9', '0.1'))
eq(L, 'quiz[0]', post('0.05', '0.6', '0.1'))
r10 = post('0.1', '0.9', '0.05') / p1
ok(1 < r10 < 10 and abs(r10 - D('4.33')) < D('0.01'), 'l8 quiz1 rises about 4.3 times, less than ten')
cid(L, 'quiz[1]', ['right'])
eq(L, 'quiz[2]', post('0.5', '0.8', '0.2'))
eq(L, 'quiz[3]', post('0.02', '1', '0.02'))
# posterior rises with the base rate (quiz1 "it cannot fall"), exhaustive grid
grid = [F(i, 200) for i in range(1, 200)]
ok(all(post(x, '0.9', '0.05') < post(y, '0.9', '0.05') for x, y in zip(grid, grid[1:])), 'l8 quiz1 posterior is increasing in the base rate')
# finding 8: "when a condition is rare, most positive tests are false" needs the false-positive rate not to be tiny
ok(post('0.01', '0.9', '0.001') > F(9, 10), 'l8 summary: rare condition, f = 0.1%: 90% of positives are true, so rarity alone does not make most positives false (finding 8)')
# finding 9: a likelihood ratio is what the result means before any base rate
ok(D('0.9') / D('0.05') == 18, 'l8 s6 the same result multiplies the odds by 18 in both clinics (finding 9)')

# ---------------------------------------------------------------- l9 natural frequencies
L = 'l9-natural-frequencies'
cells = get(L, 'screens[0]')['canvas']['params']['cells']
top = sum(1 for c in cells[0] if c == '+')
rest = sum(1 for row in cells[1:] for c in row if c == '+')
ok((top, rest) == (8, 9) and len(get(L, 'screens[0]')['widget']['answer']) == 17, 'l9 s0 grid holds 8 and 9 positives')
eq(L, 'screens[1]', F(top, top + rest))
eq(L, 'screens[2]', D('0.05') * 990, atol=0.01)
eq(L, 'screens[3]', 9 + D('49.5'), atol=0.51)
k = get(L, 'screens[4]')['widget']
ok(abs(k['answer'] - 9 / 59) < 1e-3 and abs(float(p1) - k['answer']) <= k['tol']['abs'], 'l9 s4 key 9/59 and the exact 2/13 both inside the tolerance')
eq(L, 'screens[5]', 100 * D('0.9') + 9900 * D('0.05'), atol=0)
ok(F(90, 585) == p1, 'l9 s5 90/585 equals the formula value 2/13')
eq(L, 'screens[6]', F(240, 240 + 28), atol=6e-3)
ok(post('0.3', '0.8', '0.04') == F(240, 268), 'l9 s6 counts agree with Bayes')
cid(L, 'screens[7]', ['right'])
cid(L, 'screens[8]', ['s1', 's2', 's3', 's4', 's5'])
cells = get(L, 'screens[9]')['canvas']['params']['cells']
top = sum(1 for c in cells[0] if c == 'S') * 10
rest = sum(1 for row in cells[1:] for c in row if c == 'S') * 10
ok((top, rest) == (140, 80) and len(cells[0]) * 10 == 200, 'l9 s9 grid: 140 signal days in the trend row, 80 below')
eq(L, 'screens[9]', F(top, top + rest))
eq(L, 'quiz[0]', 50 * D('0.8') + 950 * D('0.1'), atol=0)
eq(L, 'quiz[1]', F(40, 135))
eq(L, 'quiz[2]', F(20, 20))
cid(L, 'quiz[3]', ['right'])

# ---------------------------------------------------------------- l10 odds form
L = 'l10-odds-form'
eq(L, 'screens[0]', D('49.5') / 9)
eq(L, 'screens[1]', prob(F(1) / D('5.5')))
eq(L, 'screens[2]', odds(p1) / odds('0.01'))
ok(odds(p1) / odds('0.01') == D('0.9') / D('0.05') == 18, 'l10 s2 the odds factor is the likelihood ratio, 18')
shifts = {round(math.log(odds(prob(odds(F(i, 100)) * 18))) - math.log(odds(F(i, 100))), 9) for i in range(1, 100)}
ok(shifts == {round(math.log(18), 9)}, 'l10 s3 the same evidence is the same step on the log-odds line')
cid(L, 'screens[3]', ['right'])
gains = [float(prob(odds(F(i, 100)) * 18) - F(i, 100)) for i in range(1, 100)]
peak = gains.index(max(gains)) + 1
ok(15 <= peak <= 22 and gains[49] > gains[0] and all(x > y for x, y in zip(gains[peak:], gains[peak + 1:])),
   'l10 s3 the probability gain peaks near a prior of 0.19 and then falls all the way to 1, so it is not smallest "near 50%" (finding 10)')
eq(L, 'screens[4]', prob(odds('0.2') * 6))
eq(L, 'screens[5]', post('0.55', '0.3', '0.3'))
eq(L, 'screens[6]', prob(odds('0.1') * 3))
cid(L, 'screens[7]', ['o1', 'o2', 'o3', 'o4'])
o = F(1, 4)
steps = 0
while o < 1:
    o *= F(3, 2)
    steps += 1
eq(L, 'screens[8]', steps, atol=0)
ok(3 < math.log(4) / math.log(1.5) < 4, 'l10 s8 ln 4 / ln 1.5 is about 3.42')
eq(L, 'quiz[0]', prob(3))
eq(L, 'quiz[1]', prob(odds('0.5') * 4))
ok(F(1, 50) * 10 == F(1, 5), 'l10 quiz2 odds 1 to 5')
cid(L, 'quiz[2]', ['right'])
eq(L, 'quiz[3]', prob(1 * F(1, 4)))
# odds form equals the direct form on a grid of priors and rates
good = all(prob(odds(b) * (F(h) / F(f))) == post(b, h, f)
           for b in (F(1, 100), F(1, 5), F(1, 2), F(9, 10)) for h in (F(3, 10), F(9, 10)) for f in (F(1, 20), F(3, 10)))
ok(good, 'l10 s7 posterior odds = likelihood ratio x prior odds, exact on a grid')

# ---------------------------------------------------------------- l11 updating twice


def two_tests(b, h1, f1, h2, f2, r1, r2):
    """P(H | results r1, r2) from the full joint, tests independent given H and given not H."""
    b = F(b)
    lh = (F(h1) if r1 else 1 - F(h1)) * (F(h2) if r2 else 1 - F(h2))
    ln = (F(f1) if r1 else 1 - F(f1)) * (F(f2) if r2 else 1 - F(f2))
    return b * lh / (b * lh + (1 - b) * ln)


L = 'l11-updating-twice'
pp = two_tests('0.01', '0.9', '0.05', '0.9', '0.05', 1, 1)
eq(L, 'screens[0]', pp)
ok(pp == post(p1, '0.9', '0.05') == F(36, 47), 'l11 s0 one joint update equals two chained updates, 36/47')
cid(L, 'screens[1]', ['right'])
eq(L, 'screens[2]', odds(pp), atol=6e-3)
pn = two_tests('0.01', '0.9', '0.05', '0.9', '0.05', 1, 0)
eq(L, 'screens[3]', pn)
ok(pn == F(4, 213) and two_tests('0.01', '0.9', '0.05', '0.9', '0.05', 0, 1) == pn, 'l11 s3, s4 positive then negative equals negative then positive, 4/213')
cid(L, 'screens[4]', ['right'])
eq(L, 'screens[5]', D('0.81') / D('0.0025'), atol=1e-6)
ok(abs(pp - D('0.766')) < D('0.001'), 'l11 s6 the right option 0.766 is the two-positive posterior')
cid(L, 'screens[6]', ['right'])
cid(L, 'screens[7]', ['c1', 'c2', 'c3', 'c4'])
an = two_tests('0.5', '0.7', '0.3', '0.7', '0.3', 1, 1)
eq(L, 'screens[8]', an)
# B copies A: P(up | both say up) = P(up | A says up)
ok(post('0.5', '0.7', '0.3') == F(7, 10), 'l11 s9 a copied call adds nothing: 0.7')
cid(L, 'screens[9]', ['right'])
eq(L, 'quiz[0]', prob(odds('0.2') * 2 * 3))
ok(prob(odds('0.3') * 4 * F(1, 4)) == D('0.3'), 'l11 quiz1 ratios 4 and 1/4 cancel')
cid(L, 'quiz[1]', ['right'])
cid(L, 'quiz[2]', ['right'])
# Monte Carlo: two positives on a 1% condition (1,000,000 people; about 2,300 double positives)
rng = random.Random(2011)
both = ill = 0
for _ in range(1000000):
    sick = rng.random() < 0.01
    r = 0.9 if sick else 0.05
    if rng.random() < r and rng.random() < r:
        both += 1
        ill += sick
ok(abs(ill / both - 36 / 47) < 0.03, 'l11 s0 Monte Carlo two positives about 0.766', f'{ill / both:.4f}')
# finding 12: "correlated evidence counts for less than its number" holds for shared errors, not for every correlation.
# Two signals on a 50% prior, each right 70% of the time. If their errors never coincide (negatively linked),
# P(both right) = 0.4 and P(both wrong) = 0: agreement is then conclusive, worth more than two independent calls.
ok(F(4, 10) / (F(4, 10) + 0) == 1 and 1 > an, 'l11 summary: errors that never coincide make two agreeing calls worth more than two independent ones (finding 12)')

# ---------------------------------------------------------------- l12 many hypotheses
L = 'l12-many-hypotheses'
dice = (4, 6, 8)
lik5 = [F(1, d) if d >= 5 else F(0) for d in dice]
p5 = many([F(1, 3)] * 3, lik5)
cid(L, 'screens[0]', ['right'])
ok(p5.index(max(p5)) == 1, 'l12 s0 the 6-sided die is likeliest after a 5')
tab(L, 'screens[1]', lik5)
ok(sum(lik5) == F(7, 24), 'l12 s1 likelihoods add to 7/24')
tab(L, 'screens[2]', [F(1, 3) * x for x in lik5])
eq(L, 'screens[3]', p5[1])
p53 = many(p5, [F(1, d) for d in dice])
eq(L, 'screens[4]', p53[1])
ok(p53[0] == 0, 'l12 s5 the 4-sided die stays at 0')
cid(L, 'screens[5]', ['right'])
eq(L, 'screens[6]', many(['0.6', '0.2', '0.2'], ['0.5', '0.8', '0.2'])[1])
cid(L, 'screens[7]', ['right'])
tab(L, 'screens[8]', many(['0.6', '0.3', '0.1'], ['0.05', '0.15', '0.6']))
eq(L, 'screens[9]', many(['0.5', '0.3', '0.2'], ['0.012', '0.03', '0.045'])[0])
eq(L, 'quiz[0]', many(['0.1', '0.6', '0.3'], ['0.8', '0.5', '0.3'])[0])
cid(L, 'quiz[1]', ['right'])
eq(L, 'quiz[2]', F(12, 100) / (F(2, 100) + F(6, 100) + F(12, 100)))
cid(L, 'quiz[3]', ['right'])
# Monte Carlo of the dice bag: a 5, then a 3 (600,000 runs)
rng = random.Random(1212)
seen = six = 0
for _ in range(600000):
    d = rng.choice(dice)
    if rng.randint(1, d) == 5 and rng.randint(1, d) == 3:
        seen += 1
        six += d == 6
ok(abs(six / seen - 0.64) < 0.02, 'l12 s4 Monte Carlo 6-sided die after a 5 and a 3 about 0.64', f'{six / seen:.4f}')
# finding 7: "hypotheses whose priors add to 1" is not enough; they must also be mutually exclusive.
# One fair die, H1 = even, H2 = at most 3 (priors 1/2 + 1/2 = 1, but they overlap), E = the roll is 2.
faces = range(1, 7)
h1 = lambda x: x % 2 == 0
h2 = lambda x: x <= 3
e = lambda x: x == 2
pe1 = F(sum(1 for x in faces if e(x) and h1(x)), 3)
pe2 = F(sum(1 for x in faces if e(x) and h2(x)), 3)
formula = pe1 * F(1, 2) / (pe1 * F(1, 2) + pe2 * F(1, 2))
truth = F(sum(1 for x in faces if e(x) and h1(x)), sum(1 for x in faces if e(x)))
ok(formula == F(1, 2) and truth == 1, 'l12 s7 overlapping hypotheses with priors adding to 1: the formula gives 1/2, the truth is 1 (finding 7)')

# ---------------------------------------------------------------- review-2
L = 'review-2'
eq(L, 'items[0]', F(30, 80))
eq(L, 'items[1]', post('0.005', '0.98', '0.02'))
eq(L, 'items[2]', 400 * D('0.75') + 9600 * D('0.05'), atol=0)
eq(L, 'items[3]', D('0.45') / D('0.15'))
eq(L, 'items[4]', prob(odds('0.25') * 4))
eq(L, 'items[5]', prob(odds('0.1') * 9))
eq(L, 'items[6]', many(['0.5', '0.25', '0.25'], [F(1, 4), F(9, 16), 1])[2])
cid(L, 'items[7]', ['right'])
eq(L, 'items[8]', post('0.5', '0.7', '0.1'))

# ---------------------------------------------------------------- homework-2
L = 'homework-2'
eq(L, 'items[0]', post('0.02', '0.85', '0.03'))
eq(L, 'items[1]', odds('0.5') / odds('0.01'), atol=1e-9)
eq(L, 'items[2]', two_tests('0.05', '0.95', '0.1', '0.8', '0.02', 1, 0))
tab(L, 'items[3]', many(['0.4', '0.3', '0.2', '0.1'], [0, F(1, 6), F(1, 8), F(1, 12)]))
cid(L, 'items[4]', ['s1', 's2', 's3', 's4'])
good = all(post(b, h, f) == 1 / (1 + (F(f) / F(h)) * ((1 - F(b)) / F(b)))
           for b in (F(1, 100), F(3, 10)) for h in (F(1, 2), F(9, 10)) for f in (F(1, 50), F(2, 5)))
ok(good, 'homework-2 h-derive-posterior last line equals the posterior')
# finding 14: "even a small f/h cannot save it" is false as a rule: f/h = 1/1000 lifts a 1% condition past 0.9
ok(post('0.01', '0.9', '0.0009') > F(9, 10), 'homework-2 h-derive-posterior: a small enough f/h does rescue a rare condition (finding 14)')
eq(L, 'items[5]', two_tests(F(10, 200), '0.8', '0.05', '0.8', '0.05', 1, 1))
n = 1
while prob(F(18) ** n / 99) <= D('0.95'):
    n += 1
ok(n == 3 and says(L, 'items[6].model', '$n = 3$'), 'homework-2 h-long-odds three positives are needed to pass 0.95')
# finding 15: part (a) of the long answer divides by P(not H | E), which can be 0 under the stated conditions
ok(post('0.5', '0.5', '0') == 1, 'homework-2 h-long-odds: P(H) = 0.5, P(E) > 0, P(E | not H) = 0 gives P(not H | E) = 0, so the division needs a further condition (finding 15)')
cid(L, 'items[7]', ['right'])
eq(L, 'items[8]', prob(odds('0.6') * F(1, 3)))
# performance task h-two-filters
b, hj, fj, hv, fv = D('0.02'), D('0.9'), D('0.06'), D('0.7'), D('0.03')
one = post(b, hj, fj)
both_f = two_tests(b, hj, fj, hv, fv, 1, 1)
stale = b * hj * hv / (b * hj * hv + (1 - b) * fv)        # on good ticks V only fires with J, so P(J and V | G) = fV
ok(one == F(15, 64) and both_f == F(50, 57) and stale == F(3, 10), 'homework-2 h-two-filters 15/64, 50/57 and 3/10')
ok(all(says(L, 'items[9].model', s) for s in ('\\frac{15}{64}', '\\frac{50}{57}', '\\frac{3}{10}')), 'homework-2 h-two-filters model states the three values')
ok(odds(one) * (hv / (fv / fj)) == odds(stale), 'homework-2 h-two-filters second route: V multiplies the odds by 1.4')
rng = random.Random(909)
jv = bad_jv = 0
for _ in range(2000000):
    is_bad = rng.random() < 0.02
    if is_bad:
        j, v = rng.random() < 0.9, rng.random() < 0.7
    else:
        j = rng.random() < 0.06
        v = j and rng.random() < 0.5                         # P(V | G) = 0.06 x 0.5 = 0.03, only together with J
    if j and v:
        jv += 1
        bad_jv += is_bad
ok(abs(bad_jv / jv - 0.3) < 0.01, 'homework-2 h-two-filters Monte Carlo stale-quote case about 0.3', f'{bad_jv / jv:.4f}')

# ---------------------------------------------------------------- problems-2
L = 'problems-2'
eq(L, 'items[0].parts[0]', 5000 * D('0.08') * D('0.45'), atol=0)
eq(L, 'items[0].parts[1]', 5000 * D('0.08') * D('0.45') + 5000 * D('0.92') * D('0.06'), atol=0)
eq(L, 'items[0].parts[2]', post('0.08', '0.45', '0.06'))
bstar = D('0.06') / (D('0.45') + D('0.06'))
ok(post(bstar, '0.45', '0.06') == F(1, 2), 'problems-2 takeover: base rate 0.06/0.51 gives exactly one half')
eq(L, 'items[0].parts[3]', bstar)
o0 = odds('0.15')
eq(L, 'items[1].parts[0]', o0)
eq(L, 'items[1].parts[1]', o0 * 3)
eq(L, 'items[1].parts[2]', prob(o0 * 3 * 6))
ok(prob(o0 * 18) == two_tests('0.15', '0.6', '0.2', '0.3', '0.05', 1, 1), 'problems-2 downgrade: chained odds equal the joint update')
o = o0 * 18
k = 0
while prob(o) < D('0.95'):
    o *= 3
    k += 1
eq(L, 'items[1].parts[3]', k, atol=0)
cid(L, 'items[1].parts[4]', ['not-independent'])
pri, fill = ['0.5', '0.3', '0.2'], ['0.3', '0.5', '0.8']
pfill = sum(F(p) * F(f) for p, f in zip(pri, fill))
eq(L, 'items[2].parts[0]', pfill)
a1 = many(pri, fill)
eq(L, 'items[2].parts[1]', a1[2])
a2 = many(a1, fill)
eq(L, 'items[2].parts[2]', a2[2])
ok(a2 == many(pri, [F(f) ** 2 for f in fill]), 'problems-2 broker: two updates equal one update on both fills')
eq(L, 'items[2].parts[3]', sum(p * F(f) for p, f in zip(a2, fill)))
eq(L, 'items[3].parts[0]', pe('0.02', '0.95', '0.04'), atol=1e-6)
pa = post('0.02', '0.95', '0.04')
eq(L, 'items[3].parts[1]', pa)
pab = two_tests('0.02', '0.95', '0.04', '0.7', '0.01', 1, 1)
eq(L, 'items[3].parts[2]', pab)
eq(L, 'items[3].parts[3]', 1000000 * D('0.98') * D('0.04') * D('0.01'), atol=0)
eq(L, 'items[3].parts[4]', 1 - pab, atol=2e-4)

report('conditional L2 concepts')
