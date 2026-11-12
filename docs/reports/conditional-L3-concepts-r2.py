"""Round 2 concept audit, course `conditional`, level 3 (l13 to l17, review-3,
homework-3, problems-3). Run from the repo root:
    python3 docs/reports/conditional-L3-concepts-r2.py
Independence claims are checked by exact enumeration of the outcome space;
factor-model tails by the binomial formula and by seeded Monte Carlo; both
code solutions are executed against their hidden tests. Exits 0 on correct
content.
"""
from conditional_concepts_r2_lib import *

ltp = lambda ws, ps: sum(a * b for a, b in zip(ws, ps))
die = list(range(1, 7))
two = list(product(die, die))
indep = lambda space, a, b: prob(space, lambda o: a(o) and b(o)) == prob(space, a) * prob(space, b)

# ---------------- l13 when knowing tells you nothing ----------------
L = 'l13-knowing-nothing'
A6 = lambda o: o[0] == 6
tot = lambda t: (lambda o: o[0] + o[1] == t)
C(L, 'screens[1]', 'same')
ok('l13 s1 first six given total 7 stays 1/6', cond(two, A6, tot(7)) == F(1, 6))
TAP(L, 'screens[2]', ['r6c6'])
C(L, 'screens[3]', 'no')
ok('l13 s3 P(A | total 12) = 1', cond(two, A6, tot(12)) == 1)
TB(L, 'screens[4]', {(1, 1): prob(two, tot(7)), (1, 2): prob(two, tot(12)),
                     (2, 1): F(1, 6) * prob(two, tot(7)), (2, 2): F(1, 6) * prob(two, tot(12)),
                     (3, 1): prob(two, lambda o: A6(o) and tot(7)(o)), (3, 2): prob(two, lambda o: A6(o) and tot(12)(o))})
ok('l13 s4 product test passes for 7 and fails for 12', indep(two, A6, tot(7)) and not indep(two, A6, tot(12)))
ev = {'second': lambda o: o[1] == 6, 'even': lambda o: (o[0] + o[1]) % 2 == 0, 'atleast': lambda o: 6 in o,
      'firsteven': lambda o: o[0] % 2 == 0}
M(L, 'screens[5]', [k for k, e in ev.items() if indep(two, A6, e)])
S(L, 'screens[5].explain.text', r'\tfrac{6}{11}', cond(two, A6, ev['atleast']) == F(6, 11) and cond(two, A6, ev['firsteven']) == F(1, 3))
C(L, 'screens[6]', 'no')
C1 = lambda o: o[0] == 1
ok('l13 s6 disjoint, positive chances, dependent', prob(two, lambda o: A6(o) and C1(o)) == 0 and not indep(two, A6, C1))
ORD(L, 'screens[7]', ['s1', 's2', 's3', 's4'])
C(L, 'screens[8]', 'ends')
ok('l13 s8 x = x^2 only at 0 and 1', [x for x in [F(i, 20) for i in range(21)] if x == x * x] == [0, 1])
rows = get(L, 'screens[9].canvas.params.rows')
tally = {(y, t): sum(1 for r in rows if (r[1], r[2]) == (y, t)) for y in ('Up', 'Down') for t in ('Up', 'Down')}
TB(L, 'screens[9]', {(0, 1): tally['Up', 'Up'], (0, 2): tally['Up', 'Down'], (1, 1): tally['Down', 'Up'], (1, 2): tally['Down', 'Down']})
ok('l13 s9 the 20 rows chain as consecutive days', all(rows[i][2] == rows[i + 1][1] for i in range(19)) and len(rows) == 20)
ok('l13 s9 hint days', [int(r[0]) for r in rows if (r[1], r[2]) == ('Up', 'Up')] == [7, 8, 15, 16, 17, 18, 19])
upup = F(tally['Up', 'Up'], tally['Up', 'Up'] + tally['Up', 'Down'])
A(L, 'screens[10]', upup, indep=F(10, 20), all=F(7, 20), rev=1 - upup)
ok('l13 s10 P(up) = 0.5', tally['Up', 'Up'] + tally['Down', 'Up'] == 10)
# overlapping pairs share a day, so "the pairs are independent" cannot be the claim tested
ok('l13 s9 consecutive pairs overlap (pair i today is pair i+1 yesterday)', rows[0][2] == rows[1][1])
deck = [(r, s) for r in range(13) for s in range(4)]
C(L, 'quiz[0]', 'yes')
ok('l13 q ace/heart independent', indep(deck, lambda c: c[0] == 0, lambda c: c[1] == 0))
A(L, 'quiz[1]', 0.4 * 0.5, add=0.9, disjoint=0)
A(L, 'quiz[2]', 0, indep=0.3, prod=0.06)
C(L, 'quiz[3]', 'always')

# ---------------- l14 independent trials ----------------
L = 'l14-independent-trials'
trees(L)
A(L, 'screens[1]', 0.45 ** 2, add=0.9, one=0.45)
A(L, 'screens[2]', 0.45 ** 5, add=5 * 0.45, one=0.45, win=1 - 0.45 ** 5)
S(L, 'screens[2].explain.text', 'about once in 54 runs', round(1 / 0.45 ** 5) == 54)
S(L, 'screens[2].explain.text', 'At six trades the chance drops below 1%', 0.45 ** 6 < 0.01 < 0.45 ** 5)
A(L, 'screens[3]', 0.55 ** 2 * 0.45, any=3 * 0.55 ** 2 * 0.45, add=0.55 + 0.55 + 0.45, two=0.55 ** 2)
paths3 = [''.join(p) for p in product('wl', repeat=3)]
TAP(L, 'screens[4]', ['-'.join(p) for p in paths3 if p.count('w') == 2])
S(L, 'screens[4].explain.text', '= 0.4084', round(binom_pmf(3, 2, 0.55), 4) == 0.4084)
C(L, 'screens[5]', 'right')
C(L, 'screens[6]', 'right', 1 - 0.7 ** 3, add=0.9, all=0.3 ** 3, one=0.3)
S(L, 'screens[6].explain.text', 'with four ideas it would give 1.2', abs(4 * 0.3 - 1.2) < 1e-12)
C(L, 'screens[7]', 'zero', binom_pmf(10, 7, 1.0), one=1, seven=0.7, count=math.comb(10, 7))
d = get(L, 'screens[7].canvas.derive')
ok('l14 s7 slider coefficients are the binomial counts', all(d[f'values.k{k}'].startswith(f'{math.comb(10, k)} *') for k in range(11)))
ORD(L, 'screens[8]', ['s1', 's2', 's3', 's4'])
fn, w = run_code(L, 'screens[9]', 'p_at_least')
for t in w['tests'] + w['examples']:
    k_, n_, p_ = eval(t['call'].replace('p_at_least', ''))
    ok(f'l14 code test {t["call"]} expect {t["expect"]}', math.isclose(binom_tail(k_, n_, p_), expect_of(t), rel_tol=1e-9))
S(L, 'screens[9].explain.text', 'chance 0.2660', round(binom_tail(7, 10, 0.55), 4) == 0.2660)
S(L, 'screens[9].explain.text', 'only about a quarter of the time', 0.22 < binom_tail(7, 10, 0.55) < 0.28)
S(L, 'screens[9].widget.how', '8 hidden tests', len(w['tests']) == 8)
luck = binom_tail(30, 50, 0.5)
S(L, 'screens[10].prose', '= 0.1013', round(luck, 4) == 0.1013)
A(L, 'screens[10]', 20 * luck, none=0, sixty=12, one=1)
A(L, 'quiz[0]', 0.5 ** 4, add=2, half=0.5)
C(L, 'quiz[1]', 'right', 1 - 0.9 ** 3, add=0.3, all=0.001, none=0.729)
C(L, 'quiz[2]', 'right', binom_pmf(5, 1, 0.6), order=0.6 * 0.4 ** 4, single=0.6, noloss=0.4 ** 4)
n = 1
while 0.45 ** n >= 0.01:
    n += 1
A(L, 'quiz[3]', n, five=5, hundred=100)
m = mc(lambda r: sum(r.random() < 0.55 for _ in range(10)) >= 7, 400000, 141)
ok(f'l14 MC 7 or more wins in 10: {m:.4f} vs 0.2660', abs(m - 0.2660) < 0.004)
m = mc(lambda r: sum(r.random() < 0.5 for _ in range(50)) >= 30, 200000, 142)
ok(f'l14 MC 30 or more of 50 at 0.5: {m:.4f} vs 0.1013', abs(m - 0.1013) < 0.004)
m = mc(lambda r: any(r.random() < 0.3 for _ in range(3)), 400000, 143)
ok(f'l14 MC at least one of three: {m:.4f} vs 0.657', abs(m - 0.657) < 0.004)

# ---------------- l15 pairwise is not enough ----------------
L = 'l15-pairwise'
coins = list(product('HT', repeat=2))
Aa, Bb = (lambda o: o[0] == 'H'), (lambda o: o[1] == 'H')
Cc, Dd = (lambda o: o[0] == o[1]), (lambda o: o[0] != o[1])
C(L, 'screens[1]', 'same')
ok('l15 s1 P(C | A) = 1/2', cond(coins, Cc, Aa) == F(1, 2))
TAP(L, 'screens[2]', ['r0'])
quarter = F(1, 4)
TB(L, 'screens[3]', {(i, j): quarter for i in range(3) for j in (1, 2)})
ok('l15 pairwise independent', indep(coins, Aa, Bb) and indep(coins, Aa, Cc) and indep(coins, Bb, Cc))
triple = prob(coins, lambda o: Aa(o) and Bb(o) and Cc(o))
A(L, 'screens[4]', triple, product=F(1, 8), zero=0)
C(L, 'screens[5]', 'one', cond(coins, Cc, lambda o: Aa(o) and Bb(o)), half=F(1, 2), quarter=F(1, 4), zero=0)
C(L, 'screens[6]', 'right')
# three events of chance 1/2, pairwise independent: P(all three) = x forces the eight
# atoms x, 1/4 - x (three times), x (three times), 1/4 - x; all are valid for 0 <= x <= 1/4
feasible = []
for i in range(0, 41):
    x = F(i, 80)
    atoms = [x] + [quarter - x] * 3 + [x] * 3 + [quarter - x]
    if all(a >= 0 for a in atoms) and sum(atoms) == 1:
        feasible.append(x)
ok('l15 s6 pairwise independence leaves P(all three) anywhere in [0, 1/4]', min(feasible) == 0 and max(feasible) == quarter)
ok('l15 s6 coins differ gives 0', prob(coins, lambda o: Aa(o) and Bb(o) and Dd(o)) == 0 and indep(coins, Aa, Dd) and indep(coins, Bb, Dd))
vv = get(L, 'screens[6].canvas.params.values')
ok('l15 s6 venn regions', sum(F(v) for v in vv.values()) == 1 and F(vv['ABC']) == quarter and vv['AB'] == '0')
C(L, 'screens[7]', 'eleven', sum(math.comb(4, k) for k in (2, 3, 4)), six=math.comb(4, 2), seven=7, fifteen=15)
M(L, 'screens[8]', ['mut', 'null'])
# counter-example in the wrong option: P(C) = 0, A = B with chance 1/2
ok('l15 s8 triple equation can hold while a pair fails', F(0) == F(1, 2) * F(1, 2) * 0 and F(1, 2) != F(1, 2) * F(1, 2))
states = [(1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, -1)]
tab = get(L, 'screens[9].canvas.params.rows')
sign = lambda s: 1 if s.startswith('+') else -1
ok('l15 s9 table rows match Z = -(X Y)', [(sign(r[2]), sign(r[3]), sign(r[4])) for r in tab] == states
   and all(z == -x * y for x, y, z in states))
allfall = prob(states, lambda s: s == (-1, -1, -1))
A(L, 'screens[9]', allfall, indep=F(1, 8), zero=0)
for i, j in combinations(range(3), 2):
    ok(f'l15 s9 assets {i},{j} independent and uncorrelated',
       indep(states, lambda s: s[i] == 1, lambda s: s[j] == 1) and sum(s[i] * s[j] for s in states) == 0)
S(L, 'screens[9].explain.text', 'half the true crash risk', F(1, 8) == allfall / 2)
C(L, 'screens[10]', 'pairs')
S(L, 'summary.formula.note', 'Neither part implies the other')
C(L, 'quiz[0]', 'yes')
ok('l15 q-differ', cond(coins, Dd, Aa) == prob(coins, Dd) == F(1, 2))
C(L, 'quiz[1]', 'four', math.comb(3, 2) + 1, three=3, one=1)
C(L, 'quiz[2]', 'zero', cond(coins, Dd, lambda o: Aa(o) and Bb(o)), half=F(1, 2), one=1, quarter=F(1, 4))
C(L, 'quiz[3]', 'yes')

# ---------------- l16 conditional independence ----------------
L = 'l16-conditional-independence'
trees(L)
sector = [((g, a, b), (F(1, 2)) * (pa if a else 1 - pa) * (pa if b else 1 - pa))
          for g, pa in (('good', F(8, 10)), ('bad', F(2, 10))) for a in (1, 0) for b in (1, 0)]
pA = wprob(sector, lambda o: o[1] == 1)
pAB = wprob(sector, lambda o: o[1] == 1 and o[2] == 1)
C(L, 'screens[1]', 'rises')
TAP(L, 'screens[2]', ['g-u-u', 'b-u-u'])
S(L, 'screens[2].explain.text', '= 0.34', pAB == F(34, 100))
A(L, 'screens[3]', pAB / pA, indep=pA, joint=pAB, good=0.8)
TB(L, 'screens[4]', {(2, 1): 0.8 * 0.8, (2, 2): pA * pA,
                     (3, 1): wprob(sector, lambda o: o[1] == 1 and o[2] == 1, lambda o: o[0] == 'good'), (3, 2): pAB})
A(L, 'screens[5]', wprob(sector, lambda o: o[2] == 1, lambda o: o[0] == 'good' and o[1] == 1), overall=pAB / pA, both=0.64, joint=0.32)
C(L, 'screens[6]', 'right', pAB, indep=0.25, good=0.64, onepath=0.32)
alert = [((n, d), (F(2, 10) if n else F(8, 10)) * (F(1, 10) if d else F(9, 10))) for n in (1, 0) for d in (1, 0)]
fires = lambda o: o[0] == 1 or o[1] == 1
rws = get(L, 'screens[7].canvas.params.rows')
ok('l16 s7 table chances', [F(r[2]) for r in rws] == [w for _, w in alert] and [r[3] for r in rws] == ['Fires', 'Fires', 'Fires', 'Silent'])
pn = wprob(alert, lambda o: o[0] == 1, fires)
A(L, 'screens[7]', pn, prior=F(2, 10), onerow=F(18, 28))
pnd = wprob(alert, lambda o: o[0] == 1, lambda o: fires(o) and o[1] == 1)
C(L, 'screens[8]', 'right', pnd)
ok('l16 s8 explaining away: 5/7 falls back to the prior 0.2', pn == F(5, 7) and pnd == F(2, 10))
ORD(L, 'screens[9]', ['s1', 's2', 's3', 's4'])
S(L, 'screens[9].prose', r'with $P(A \cap C) > 0$')
an = [((t, x, y), (F(4, 10) if t else F(6, 10)) * (q if x else 1 - q) * (q if y else 1 - q))
      for t, q in ((1, F(3, 4)), (0, F(1, 4))) for x in (1, 0) for y in (1, 0)]
p1 = wprob(an, lambda o: o[1] == 1)
p12 = wprob(an, lambda o: o[1] == 1 and o[2] == 1)
A(L, 'screens[10]', p12 / p1, indep=p1, acc=0.75, joint=p12)
ok('l16 s10 numbers', p1 == F(45, 100) and p12 == F(2625, 10000) and p12 / p1 == F(7, 12))
C(L, 'quiz[0]', 'no')
A(L, 'quiz[1]', 0.6 * 0.5, add=1.1, one=0.6)
C(L, 'quiz[2]', 'falls')
# q-explain-away, for any chances of the two causes: P(bad | loss, crash) = P(bad) < P(bad | loss).
# So "falls" is right against the chance after the loss, and "unchanged" is right against the prior.
good = True
for pb in (0.1, 0.3, 0.6):
    for pc in (0.05, 0.2, 0.5):
        fund = [((b_, c_), (pb if b_ else 1 - pb) * (pc if c_ else 1 - pc)) for b_ in (1, 0) for c_ in (1, 0)]
        loss = lambda o: o[0] == 1 or o[1] == 1
        after_loss = wprob(fund, lambda o: o[0] == 1, loss)
        after_both = wprob(fund, lambda o: o[0] == 1, lambda o: loss(o) and o[1] == 1)
        good &= after_both < after_loss and abs(after_both - pb) < 1e-12
ok('l16 q-explain-away: falls relative to after the loss, equals the prior', good)
coin = [((k, a, b), F(1, 2) * (q if a else 1 - q) * (q if b else 1 - q)) for k, q in (('fair', F(1, 2)), ('two', F(1))) for a in (1, 0) for b in (1, 0)]
A(L, 'quiz[3]', wprob(coin, lambda o: o[2] == 1, lambda o: o[1] == 1), indep=wprob(coin, lambda o: o[2] == 1), fair=F(1, 2))


def stocks(r):
    q = 0.8 if r.random() < 0.5 else 0.2
    return r.random() < q, r.random() < q


m = mc_cond(stocks, 500000, 161)
ok(f'l16 MC B up given A up {m:.4f} vs 0.68', abs(m - 0.68) < 0.004)


def explain_away(r):
    news, drop = r.random() < 0.2, r.random() < 0.1
    return (news or drop) and drop, news


m = mc_cond(explain_away, 2000000, 162)
ok(f'l16 MC news given alert and drop {m:.4f} vs 0.2', abs(m - 0.2) < 0.004)

# ---------------- l17 correlated defaults ----------------
L = 'l17-correlated-defaults'
# screens[5]: since the round 3 fix pass the regime tails are second-level branches
# and the leaves are path products, so the generic tree check covers this tree too.
trees(L)
S(L, 'screens[5].prose', 'The second branches show $P(3 \\text{ or more defaults})$ in each regime')
ind = [binom_pmf(10, k, 0.05) for k in range(3)]
ind.append(1 - sum(ind))
st = get(L, 'screens[1].canvas.state.values')
ok('l17 independent bars', all(close(st[f'k{i}'], ind[i], 6e-5) for i in range(4)))


def mix(q, pb=0.2, mean=0.05, n=10):
    pg = (mean - pb * q) / (1 - q) if q < 1 else 0
    pm = [q * binom_pmf(n, k, pb) + (1 - q) * binom_pmf(n, k, pg) for k in range(3)]
    return pm + [1 - sum(pm)]


C(L, 'screens[1]', 'rises')
C(L, 'screens[2]', 'both')
grid = [i / 100 for i in range(0, 26)]
ms = [mix(q) for q in grid]
ok('l17 s2 slider: bars for 0 and for 3 or more rise at every step from 0 to 0.25',
   all(ms[i + 1][0] > ms[i][0] and ms[i + 1][3] > ms[i][3] for i in range(25)))
m20 = mix(0.2)
S(L, 'screens[2].hints[2].text', '0.7269 against 0.5987, and 3 or more is 0.0646 against 0.0115',
  (round(m20[0], 4), round(ind[0], 4), round(m20[3], 4), round(ind[3], 4)) == (0.7269, 0.5987, 0.0646, 0.0115))
ok('l17 s2 the middle thins out', m20[1] < ind[1] and m20[2] < ind[2])
A(L, 'screens[3]', 0.2 * 0.2 + 0.8 * 0.0125, add=0.2 + 0.0125, avg=(0.2 + 0.0125) / 2, rec=0.2)
pair = 0.2 * 0.2 ** 2 + 0.8 * 0.0125 ** 2
A(L, 'screens[4]', pair, indep=0.05 ** 2, recpath=0.008, given=0.04)
S(L, 'screens[4].explain.text', 'more than three times as likely', pair / 0.0025 > 3)
tr, tn = binom_tail(3, 10, 0.2), binom_tail(3, 10, 0.0125)
tp = get(L, 'screens[5].canvas.params.levels[1].branches[0].p')
ok('l17 s5 regime tails', close(tp['r'], tr, 6e-5) and close(tp['n'], tn, 6e-5))
A(L, 'screens[5]', 0.2 * tr + 0.8 * tn, indep=ind[3], rec=tr, avg=(0.3222 + 0.0002) / 2, recw=0.2 * 0.3222)
S(L, 'screens[5].explain.text', '5.6 times', round((0.2 * tr + 0.8 * tn) / ind[3], 1) == 5.6)
C(L, 'screens[6]', 'right')
bars = get(L, 'screens[6].canvas.state.values')
ok('l17 s6 bars at q = 0.2', all(close(bars[f'k{i}'], m20[i], 6e-5) for i in range(4)))
A(L, 'screens[7]', 0.05, indep=ind[3], ten=0.5, pow=0)
S(L, 'screens[7].explain.text', 'more than four times', 0.05 / ind[3] > 4)
C(L, 'screens[8]', 'cond')
fn, w = run_code(L, 'screens[9]', 'book_tail')
for t in w['tests'] + w['examples']:
    k_, n_, q_, pb_, pg_ = eval(t['call'].replace('book_tail', ''))
    ok(f'l17 code test {t["call"]}', math.isclose(q_ * binom_tail(k_, n_, pb_) + (1 - q_) * binom_tail(k_, n_, pg_), expect_of(t), rel_tol=1e-9))
S(L, 'screens[9].widget.how', '7 hidden tests', len(w['tests']) == 7)
S(L, 'screens[9].explain.text', 'gives 0.0646', round(fn(3, 10, 0.2, 0.2, 0.0125), 4) == 0.0646)
C(L, 'screens[10]', 'right')
# the shared factor never lowers the tail or the chance of a quiet year (any two-regime mix with mean 0.05)
rng = random.Random(17)
good = True
for _ in range(3000):
    q = rng.uniform(0.01, 0.99)
    pb = rng.uniform(0.05, min(1.0, 0.05 / q))
    mm = mix(q, pb)
    good &= mm[3] >= ind[3] - 1e-12 and mm[0] >= ind[0] - 1e-12
ok('l17 s1 and q-quiet: any recession mix with mean 0.05 has a tail and a zero bar at least the independent ones', good)
C(L, 'quiz[0]', 'y')
A(L, 'quiz[1]', 0.5 * 0.08 + 0.5 * 0.02, add=0.1, rec=0.08)
A(L, 'quiz[2]', 0.5 * 0.08 ** 2 + 0.5 * 0.02 ** 2, indep=0.05 ** 2, rec=0.08 ** 2)
C(L, 'quiz[3]', 'rec')


def book(r):
    p = 0.2 if r.random() < 0.2 else 0.0125
    return sum(r.random() < p for _ in range(10)) >= 3


m = mc(book, 600000, 171)
ok(f'l17 MC 3 or more defaults {m:.4f} vs 0.0646', abs(m - 0.0646) < 0.002)


def pool(r):
    p = 0.2 if r.random() < 0.2 else 0.0125
    return sum(r.random() < p for _ in range(1000)) >= 100


m = mc(pool, 3000, 172)
ok(f'l17 MC big pool, at least 10% default: {m:.3f} vs 0.2', abs(m - 0.2) < 0.03)

# ---------------- review-3 ----------------
L = 'review-3'
C(L, 'items[0]', 'no')
ok('review-3 r-total-eight', cond(two, lambda o: o[0] % 2 == 0, tot(8)) == F(3, 5))
A(L, 'items[1]', 0, indep=0.12, add=0.7)
A(L, 'items[2]', 1 - 0.8 ** 4, add=0.8, all=0.2 ** 4, none=0.8 ** 4)
A(L, 'items[3]', binom_pmf(4, 2, 0.6), order=0.6 ** 2 * 0.4 ** 2, twopaths=2 * 0.6 ** 2 * 0.4 ** 2)
C(L, 'items[4]', 'no')
A(L, 'items[5]', 250 * allfall, indep=250 / 8, none=0)
sy = [((dz, s1, s2), (F(1, 10) if dz else F(9, 10)) * (q if s1 else 1 - q) * (q if s2 else 1 - q))
      for dz, q in ((1, F(9, 10)), (0, F(2, 10))) for s1 in (1, 0) for s2 in (1, 0)]
A(L, 'items[6]', wprob(sy, lambda o: o[2] == 1, lambda o: o[1] == 1), indep=wprob(sy, lambda o: o[2] == 1), sick=0.9,
  joint=wprob(sy, lambda o: o[1] == 1 and o[2] == 1))
mg = [((a, b), (F(3, 10) if a else F(7, 10)) * (F(5, 10) if b else F(5, 10))) for a in (1, 0) for b in (1, 0)]
call = lambda o: o[0] == 1 or o[1] == 1
S(L, 'items[7].prose', r'\tfrac{0.3}{0.65} \approx 0.46', wprob(mg, lambda o: o[0] == 1, call) == F(30, 65))
C(L, 'items[7]', 'prior', wprob(mg, lambda o: o[0] == 1, lambda o: call(o) and o[1] == 1), same=0.46, one=1, zero=0)
ovr = 0.1 * 0.3 + 0.9 * 0.02
A(L, 'items[8]', 0.1 * 0.09 + 0.9 * 0.0004, indep=ovr ** 2, rec=0.009, given=0.09)
S(L, 'items[8].explain.text', 'four times likelier', 3.9 < 0.00936 / ovr ** 2 < 4.2)

# ---------------- homework-3 ----------------
L = 'homework-3'
t = get(L, 'items[0].canvas.params.rows')
ok('homework-3 table', [int(x) for x in t[0][1:]] == [33, 27, 60] and [int(x) for x in t[1][1:]] == [77, 63, 140] and [int(x) for x in t[2][1:]] == [110, 90, 200])
C(L, 'items[0]', 'yes')
ok('homework-3 signal independent', F(33, 60) == F(77, 140) == F(110, 200))
A(L, 'items[1]', 0.7 ** 12, one=0.7, all=0.3 ** 12)
S(L, 'items[1].explain.text', 'about once in 72', round(1 / 0.7 ** 12) == 72)
n = 1
while 1 - 0.45 ** n < 0.999:
    n += 1
A(L, 'items[2]', n, eight=8, add=2)
S(L, 'items[2].explain.text', '= 8.65', abs(math.log(0.001) / math.log(0.45) - 8.65) < 0.005)
truth = {'zx': cond(states, lambda s: s[2] == -1, lambda s: s[0] == -1) == F(1, 2),
         'zxy': cond(states, lambda s: s[2] == -1, lambda s: s[0] == -1 and s[1] == -1) == 1,
         'mutual': prob(states, lambda s: s == (1, 1, 1)) == F(1, 8) and allfall == F(1, 8),
         'allup': prob(states, lambda s: s == (1, 1, 1)) == F(1, 8)}
M(L, 'items[3]', [k for k, v in truth.items() if v])
A(L, 'items[4]', wprob(an, lambda o: o[0] == 1, lambda o: o[1] == 1 and o[2] == 1), one=wprob(an, lambda o: o[0] == 1, lambda o: o[1] == 1), lik=0.75 ** 2)
tb, tg = binom_tail(2, 5, 0.32), binom_tail(2, 5, 0.02)
ok('homework-3 h-book-five: each loan alone is 0.05', abs(0.1 * 0.32 + 0.9 * 0.02 - 0.05) < 1e-12)
A(L, 'items[5]', 0.1 * tb + 0.9 * tg, indep=binom_tail(2, 5, 0.05), rec=tb, recterm=0.1 * tb, normterm=0.9 * tg)
S(L, 'items[5].explain.text', '= 0.5125', round(tb, 4) == 0.5125 and round(tg, 4) == 0.0038)
S(L, 'items[5].feedback.correct', 'about 2.4 times', round((0.1 * tb + 0.9 * tg) / binom_tail(2, 5, 0.05), 1) == 2.4)
ORD(L, 'items[6]', ['s1', 's2', 's3', 's4', 's5'])
rng = random.Random(8)
good = True
for _ in range(3000):
    q, pb, pg = rng.random(), rng.random(), rng.random()
    m1 = q * pb + (1 - q) * pg
    good &= abs((q * pb ** 2 + (1 - q) * pg ** 2 - m1 * m1) - q * (1 - q) * (pb - pg) ** 2) < 1e-12
S(L, 'items[7].prompt', 'q(1-q)(p_b - p_g)^2', good)
mod = get(L, 'items[7].model')
ok('homework-3 long (d)', abs(0.2 * 0.8 * 0.1875 ** 2 - 0.005625) < 1e-12 and abs(0.008125 - 0.0025 - 0.005625) < 1e-12
   and '0.005625' in mod and '3.25 times' in mod and abs(0.008125 / 0.0025 - 3.25) < 1e-9)
ok('homework-3 rubric total', sum(r['points'] for r in get(L, 'items[7].rubric')) == 10)

# ---------------- problems-3 ----------------
L = 'problems-3'
I = 'items[0].parts'
A(L, I + '[0]', F(78, 120), reversed=F(78, 260), **{'over-all': F(78, 400)})
C(L, I + '[1]', 'yes')
ok('problems-3 gap independent of up', F(78, 120) == F(260, 400) and F(120, 400) * F(260, 400) == F(78, 400))
A(L, I + '[2]', binom_pmf(4, 3, 0.65), **{'one-path': 0.65 ** 3 * 0.35, 'all-four': 0.65 ** 4, 'joint-slip': binom_pmf(4, 3, 0.195)})
A(L, I + '[3]', 1 - 0.65 ** 4, sum=4 * 0.35, **{'exactly-one': binom_pmf(4, 3, 0.65), 'all-down': 0.35 ** 4})
wk = [((s, z), (F(3, 10) if s else F(7, 10)) * (F(25, 100) if z else F(75, 100))) for s in (1, 0) for z in (1, 0)]
loss = lambda o: o[0] == 1 or o[1] == 1
pl = wprob(wk, loss)
I = 'items[1].parts'
A(L, I + '[0]', pl, sum=0.55, both=0.075)
fl = wprob(wk, lambda o: o[0] == 1, loss)
A(L, I + '[1]', fl, times=0.3 * 0.475, **{'no-news': 0.3, 'sum-slip': 0.3 / 0.55})
fls = wprob(wk, lambda o: o[0] == 1, lambda o: loss(o) and o[1] == 1)
A(L, I + '[2]', fls, still=fl, cancelled=0, **{'over-loss': 0.075 / 0.475})
C(L, I + '[3]', 'no')
ok('problems-3 explaining away', fls == F(3, 10) and fl == F(12, 19))
I = 'items[2].parts'
one = 0.25 * 0.28 + 0.75 * 0.04
A(L, I + '[0]', one, average=(0.28 + 0.04) / 2, **{'recession-only': 0.07})
three = 0.25 * 0.28 ** 3 + 0.75 * 0.04 ** 3
A(L, I + '[1]', three, independent=one ** 3, **{'no-weights': 0.28 ** 3 + 0.04 ** 3, 'cube-average': 0.16 ** 3})
A(L, I + '[2]', one ** 3, sum=0.3, squared=0.01)
A(L, I + '[3]', three / one ** 3, reciprocal=one ** 3 / three, difference=three - one ** 3, **{'weights-slip': 0.022016 / 0.001})
feeds = list(product((0, 1), repeat=3))        # F, G, H
dA, dB, dC = (lambda o: o[0] == o[1]), (lambda o: o[0] == o[2]), (lambda o: o[1] == o[2])
I = 'items[3].parts'
A(L, I + '[0]', cond(feeds, dC, dA), joint=F(1, 4), certain=1)
C(L, I + '[1]', 'pairwise')
ok('problems-3 desks pairwise independent, each 1/2', all(indep(feeds, x, y) for x, y in ((dA, dB), (dA, dC), (dB, dC)))
   and prob(feeds, dA) == prob(feeds, dB) == prob(feeds, dC) == F(1, 2))
tri = prob(feeds, lambda o: dA(o) and dB(o) and dC(o))
A(L, I + '[2]', tri, product=F(1, 8), single=F(1, 2))
A(L, I + '[3]', cond(feeds, dC, lambda o: dA(o) and dB(o)), pairwise=F(1, 2), joint=F(1, 4))
A(L, I + '[4]', 1 - (1 - tri) ** 8, sum=8 * tri, complement=(1 - tri) ** 8, **{'product-slip': 1 - F(7, 8) ** 8})

done()
