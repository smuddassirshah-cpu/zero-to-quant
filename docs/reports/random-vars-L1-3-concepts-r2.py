#!/usr/bin/env python3
"""Round 2 blind concept audit, random-vars levels 1 to 3.

Independent recomputation of graded keys and slip values (exact, with
Fractions or enumeration) and Monte Carlo checks of every empirical claim.
Pure standard library. Exit 0 when every check passes. A check that fails
because the content is wrong is left failing and is a finding.

Run from anywhere: python3 docs/reports/random-vars-L1-3-concepts-r2.py
"""
import json, math, os, random, sys
from fractions import Fraction as Fr
from itertools import product, permutations, combinations

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                    'app', 'content', 'courses', 'random-vars')
FAIL, NOTES, N = [], [], [0]


def load(name):
    with open(os.path.join(ROOT, name + '.json')) as f:
        return json.load(f)


def check(name, cond, detail=''):
    N[0] += 1
    if not cond:
        FAIL.append(f'{name} {detail}')
        print('FAIL', name, detail)


def close(a, b, tol=1e-3):
    return abs(float(a) - float(b)) <= tol


def wrongs(w):
    return {x['id']: x.get('value') for x in w.get('wrong', [])}


def pmf_stats(pm):
    mu = sum(x * p for x, p in pm.items())
    var = sum((x - mu) ** 2 * p for x, p in pm.items())
    return mu, var


dice = [(a, b) for a in range(1, 7) for b in range(1, 7)]
tot = {}
for a, b in dice:
    tot[a + b] = tot.get(a + b, 0) + Fr(1, 36)
die = {k: Fr(1, 6) for k in range(1, 7)}

# ---------------------------------------------------------------- level 1
L1, L2, L3, L4 = (load('l1-number-per-outcome'), load('l2-listing-chances'),
                  load('l3-up-to-a-point'), load('l4-transforming'))
s = L1['screens']
check('l1 S0 total 9 cells', len(s[0]['widget']['answer']) == sum(1 for a, b in dice if a + b == 9))
check('l1 S1 max 4 cells', len(s[1]['widget']['answer']) == sum(1 for a, b in dice if max(a, b) == 4) == 7)
check('l1 S3 gap 1', s[3]['widget']['answer'] == sum(1 for a, b in dice if abs(a - b) == 1))
check('l1 S5 P(max=6)=11/36', sum(1 for a, b in dice if max(a, b) == 6) == 11)
check('l1 quiz distinct diffs', L1['quiz'][3]['widget']['answer'] == len({a - b for a, b in dice}))
check('l1 quiz P(total>=10)=1/6', sum(1 for a, b in dice if a + b >= 10) == 6)
s = L2['screens']
for i, x in enumerate(range(2, 8)):
    check(f'l2 S0 p({x})', close(s[0]['widget']['rows'][i][1]['answer'], tot[x], 1e-5))
check('l2 S2 wrong half 21/36', close(wrongs(s[2]['widget'])['half'], Fr(21, 36), 1e-3))
check('l2 S6 sixes pmf', [sum(1 for a, b in dice if (a == 6) + (b == 6) == k) for k in (0, 1, 2)] == [25, 10, 1])
two = {}
for (m1, p1), (m2, p2) in product([(2, .3), (0, .5), (-2, .2)], repeat=2):
    two[m1 + m2] = two.get(m1 + m2, 0) + p1 * p2
for row in s[8]['widget']['rows']:
    x = int(str(row[0]).replace('−', '-'))
    check(f'l2 S8 p({x})', close(row[1]['answer'], two[x], 1e-9))
check('l2 quiz max=3 is 5/36', sum(1 for a, b in dice if max(a, b) == 3) == 5)
s = L3['screens']
Fmax = lambda y: Fr(sum(1 for a, b in dice if max(a, b) <= y), 36)
check('l3 S5 F(y)=y^2/36', all(Fmax(y) == Fr(y * y, 36) for y in range(1, 7)))
check('l3 S6 jump 7/36', close(s[6]['widget']['answer'], Fmax(4) - Fmax(3), 1e-4))
check('l3 S7 P(2<=Y<=4)=15/36', Fmax(4) - Fmax(1) == Fr(15, 36) and Fmax(4) - Fmax(2) == Fr(12, 36))
loss = [(-2, .30), (0, .25), (1, .20), (2, .15), (5, .06), (10, .03), (20, .01)]


def var_q(pm, level):
    c = 0
    for x, p in sorted(pm):
        c += p
        if c >= level - 1e-12:
            return x


check('l3 S10 VaR 5', s[10]['widget']['answer'] == var_q(loss, .95))
check('l3 quiz P(L>2)=0.10', close(L3['quiz'][3]['widget']['answer'], sum(p for x, p in loss if x > 2), 1e-9))
s = L4['screens']
check('l4 S0 ten cells', len(s[0]['widget']['answer']) == sum(1 for a, b in dice if (a + b - 7) ** 2 == 1))
ysq = {}
for x, p in tot.items():
    ysq[(x - 7) ** 2] = ysq.get((x - 7) ** 2, 0) + p
for row in s[2]['widget']['rows']:
    check(f'l4 S2 pY({row[0]})', close(row[1]['answer'], ysq[int(row[0])], 1e-5))
for K in range(2, 13):  # the canvas formula for P(max(X-K,0)=0) against enumeration
    f = (K - 1) * K / 72 if K <= 7 else 1 - (12 - K) * (13 - K) / 72
    check(f'l4 S1 canvas K={K}', close(f, sum(p for x, p in tot.items() if x <= K), 1e-12))
check('l4 S7 call pmf', [r[1]['answer'] for r in s[7]['widget']['rows']] == [0.61, 0.3, 0.09])
check('l4 S8 short P(L=-1000)', s[8]['widget']['answer'] == 0.09)

# ---------------------------------------------------------------- level 2
L5, L6, L7, L8 = (load('l5-long-run-average'), load('l6-fair-price'),
                  load('l7-linearity'), load('l8-indicators'))
s = L5['screens']
loaded = {1: .1, 2: .1, 3: .1, 4: .1, 5: .1, 6: .5}
check('l5 S4 loaded die 4.5', close(s[4]['widget']['answer'], pmf_stats(loaded)[0], 1e-9))
check('l5 S6 sixes mean 1/3', Fr(10, 36) + 2 * Fr(1, 36) == Fr(1, 3))
avg = s[2]['canvas']['params']['series'][0]['values']
check('l5 S2 series: 4.5 after 10, near 3.5 at 1000', avg[9] == 4.5 and abs(avg[-1] - 3.5) < .01)
check('l5 S2 a new roll moves a 1000-roll average < 0.003', 2.5 / 1001 < .003)


def simulate(pmf, n, seed=1):
    rng = random.Random(seed)
    values = list(pmf)
    weights = [pmf[v] for v in values]
    return sum(rng.choices(values, weights, k=n)) / n


fl = {k: 1 / 6 for k in range(1, 7)}
check('l5 S8 printed 3.50167', simulate(fl, 100000) == 3.50167 == float(s[8]['widget']['examples'][1]['expect']))
for t in s[8]['widget']['tests']:
    pass  # the hidden tests are run by the playthrough; here only the method is audited
# "More draws shrink that gap": true on average (RMS error ~ sd/sqrt(n)), not draw by draw.
rng = random.Random(2026)
rms = {}
for n in (100, 1600):
    e = [abs(sum(rng.choices(range(1, 7), k=n)) / n - 3.5) for _ in range(1500)]
    rms[n] = math.sqrt(sum(x * x for x in e) / len(e))
check('l5 S8 MC: RMS gap falls like 1/sqrt(n)', 3.3 < rms[100] / rms[1600] < 4.8, str(rms))
gaps = [abs(simulate(fl, n) - 3.5) for n in (100000, 200000, 400000, 800000)]
NOTES.append('l5 S8 same seed, gaps at 1e5,2e5,4e5,8e5 draws: ' + ', '.join(f'{g:.5f}' for g in gaps))
# dilution, not correction (quiz q-no-memory)
rng = random.Random(7)
nxt = cnt = 0
while cnt < 4000:
    run = 0
    while True:
        h = rng.random() < .5
        if run >= 6:  # six tails in a row stands in for ten (same Markov argument, far cheaper)
            nxt += h
            cnt += 1
            break
        run = 0 if h else run + 1
check('l5 quiz MC: heads after a run of tails stays 0.5', abs(nxt / cnt - .5) < .03, f'{nxt / cnt:.3f}')
s = L6['screens']
check('l6 S2 fair price 10/6', close(s[2]['widget']['answer'], Fr(10, 6), 1e-4))
check('l6 S4 fair price 7/3', close(s[4]['widget']['answer'], 12 * tot[7] + 6 * (tot[2] + tot[12]), 1e-4))
w = wrongs(s[4]['widget'])
check('l6 S4 slips', close(w['one-end'], 2 + Fr(6, 36), 1e-4) and w['first'] == 2 and w['plain'] == 9)
paths = {}
for (m1, p1), (m2, p2) in product([(2, .4), (0, .4), (-2, .2)], repeat=2):
    paths[100 + m1 + m2] = paths.get(100 + m1 + m2, 0) + p1 * p2
w = wrongs(s[9]['widget'])
check('l6 S9 binary 16 (days independent, as the tree draws them)',
      close(s[9]['widget']['answer'], 100 * sum(p for x, p in paths.items() if x > 102), 1e-9))
check('l6 S9 slips', close(w['at-102'], 100 * sum(p for x, p in paths.items() if x >= 102), 1e-9)
      and close(w['only-102'], 100 * paths[102], 1e-9) and close(w['one-up'], 100 * (1 - .6 ** 2), 1e-9))
check('l6 S10 overround 7p', close(s[10]['widget']['answer'], .52 + .28 + .27 - 1, 1e-9))
q = L6['quiz']
check('l6 quiz lottery -0.5', close(q[0]['widget']['answer'], 1e6 * 1e-6 + 50 * .01 - 2, 1e-9))
check('l6 quiz double six', close(q[1]['widget']['answer'], Fr(20, 36) - 3, 1e-4))
s = L7['screens']
check('l7 S0 row 1 average', s[0]['widget']['answer'] == sum(1 + y for y in range(1, 7)) / 6)
check('l7 S4 E|X-Y| slip 70/36', close(wrongs(s[4]['widget'])['gap'], Fr(sum(abs(a - b) for a, b in dice), 36), 1e-4))
check('l7 S5 E[3X-5]', s[5]['widget']['answer'] == 3 * 3.5 - 5 == sum(3 * k - 5 for k in range(1, 7)) / 6)
check('l7 S6 E[X^2]=91/6 > 3.5^2', Fr(91, 6) == sum(k * k for k in range(1, 7)) * Fr(1, 6))
EA, EB = 200 * .6 - 100 * .4, 50 * .4 - 50 * .6
check('l7 S9 desk 70', close(EA + EB, 70, 1e-9))
# linearity under any coupling: the two extreme couplings of A and B share the mean of A+B
comon = .4 * (200 + 50) + .2 * (200 - 50) + .4 * (-100 - 50)
anti = .4 * (-100 + 50) + .6 * (200 - 50)
check('l7 S9 mean of A+B is 70 under opposite couplings', close(comon, 70, 1e-9) and close(anti, 70, 1e-9))
check('l7 S10 trading costs 900', s[10]['widget']['answer'] == 200 * (3 * .7 + 8 * .3))
s = L8['screens']
check('l8 S5 birthday pairs 253/365', close(s[5]['widget']['answer'], Fr(253, 365), 1e-4))
p_none = 1.0
for i in range(23):
    p_none *= (365 - i) / 365
w = wrongs(s[5]['widget'])
check('l8 S5 slips', close(w['at-least-one'], 1 - p_none, 1e-4) and close(w['ordered'], 506 / 365, 1e-4)
      and close(w['people'], 23 / 365, 1e-3))
rng = random.Random(11)
tp = hit = 0
R = 20000
for _ in range(R):
    b = [rng.randrange(365) for _ in range(23)]
    c = {}
    for x in b:
        c[x] = c.get(x, 0) + 1
    k = sum(v * (v - 1) // 2 for v in c.values())
    tp += k
    hit += k > 0
check('l8 S5 MC expected pairs', abs(tp / R - 253 / 365) < .03, f'{tp / R:.3f}')
check('l8 S5 MC at least one', abs(hit / R - .5073) < .015, f'{hit / R:.3f}')
# matches in a random permutation: exact for n=5, MC for n=52; indicators are dependent
fix5 = [sum(1 for i, x in enumerate(p) if i == x) for p in permutations(range(5))]
check('l8 S3 E[matches]=1, n=5 exact', Fr(sum(fix5), len(fix5)) == 1)
check('l8 S3 dependence: exactly four matches is impossible', 4 not in fix5)
check('l8 S3 slip P(all five)=1/120', close(wrongs(s[3]['widget'])['all'], 1 / 120, 1e-4))
rng = random.Random(3)
m = 0
for _ in range(20000):
    d = list(range(52))
    rng.shuffle(d)
    m += sum(1 for i, x in enumerate(d) if i == x)
check('l8 S6 MC E[matches]=1, n=52', abs(m / 20000 - 1) < .03, f'{m / 20000:.3f}')
fills = [.9, .8, .7, .6, .5, .4, .3, .2, .15, .1]
check('l8 S9 expected fills 4.65', close(s[9]['widget']['answer'], sum(fills), 1e-9))
ind0, ind10 = math.prod(1 - f for f in fills), math.prod(fills)
check('l8 S9 nested fills make 0 or 10 likelier than independence', .1 + .1 > ind0 + ind10)
check('l8 quiz aces 5/13', close(L8['quiz'][1]['widget']['answer'], Fr(5, 13), 1e-4))
check('l8 S1 mode of Bin(10,1/6) is 1', max(range(11), key=lambda k: math.comb(10, k) * 5 ** (10 - k)) == 1)

# ---------------------------------------------------------------- level 3
L9, L10, L11, L12 = (load('l9-measuring-spread'), load('l10-scaling-and-adding'),
                     load('l11-moving-together'), load('l12-diversification'))
s = L9['screens']
mu, var = pmf_stats({1: .5, 3: .25, 7: .25})
w = wrongs(s[2]['widget'])
check('l9 S2 variance 6', close(var, 6) and s[2]['widget']['answer'] == 6)
check('l9 S2 slips', w['abs'] == 2 and w['raw'] == 15 and close(w['unweighted'], 20 / 3, 1e-3) and w['mean'] == 3)
check('l9 S3 die variance and sd', close(s[3]['widget']['rows'][6][1]['answer'], Fr(35, 12), 1e-4)
      and close(s[3]['widget']['rows'][7][1]['answer'], math.sqrt(35 / 12), 1e-4))
check('l9 S5 sd 2', close(math.sqrt(pmf_stats({-1: .8, 4: .2})[1]), 2, 1e-9))
random.seed(9)
rolls = [random.randint(1, 6) for _ in range(100_000)]
mm = sum(rolls) / len(rolls)
check('l9 S7 printed 2.9207', f'{sum((r - mm) ** 2 for r in rolls) / len(rolls):.4f}' == '2.9207')
mA, vA = pmf_stats({-200: .4, 300: .6})
mB, vB = pmf_stats({-400: .5, 600: .5})
w = wrongs(s[8]['widget'])
check('l9 S8 A: mean 100, sd 244.95; B: mean 100, sd 500',
      close(mA, 100) and close(math.sqrt(vA), 244.95, .01) and close(mB, 100) and close(math.sqrt(vB), 500))
check('l9 S8 slips', close(w['raw'], math.sqrt(70000), .01) and w['abs'] == 240 and w['var'] == 60000)
check('l9 S9 both sds 9.95', close(math.sqrt(pmf_stats({-1: .99, 99: .01})[1]), 9.95, .005)
      and close(pmf_stats({-1: .99, 99: .01})[0], 0, 1e-9))
s = L10['screens']
vd = pmf_stats(die)[1]
vt = pmf_stats(tot)[1]
dif = {}
for a, b in dice:
    dif[a - b] = dif.get(a - b, 0) + Fr(1, 36)
check('l10 Var die 35/12, total 35/6, difference 35/6, 2X 35/3',
      vd == Fr(35, 12) and vt == Fr(35, 6) and pmf_stats(dif)[1] == Fr(35, 6)
      and pmf_stats({2 * k: Fr(1, 6) for k in range(1, 7)})[1] == Fr(35, 3))
check('l10 S5 pmf of X-Y is the total pmf slid by 7', all(dif[k - 7] == tot[k] for k in tot))
check('l10 S3 Var(-3X+5)', s[3]['widget']['answer'] == float(9 * vd))
w = wrongs(s[4]['widget'])
check('l10 S4 slips', close(w['raw'], 49 + 35 / 6, 1e-3) and close(w['abs'], 70 / 36, 1e-3))
check('l10 S8 nine days', s[8]['widget']['answer'] == 9 and 100 * math.sqrt(9) == 300 and 20 * 25 == 100 * math.sqrt(25))
rng = random.Random(5)
tots = [sum(rng.gauss(20, 100) for _ in range(9)) for _ in range(20000)]
mt = sum(tots) / len(tots)
sd9 = math.sqrt(sum((t - mt) ** 2 for t in tots) / len(tots))
check('l10 S8 MC sd of 9 independent days is 300', abs(sd9 - 300) < 8, f'{sd9:.1f}')
w = wrongs(s[9]['widget'])
check('l10 S9 annual vol', close(s[9]['widget']['answer'], .012 * math.sqrt(252), 1e-4)
      and close(w['calendar'], .012 * math.sqrt(365), 1e-4) and close(w['linear'], .012 * 252, 1e-9))
w = wrongs(s[10]['widget'])
check('l10 S10 doubled, ten days', close(s[10]['widget']['answer'], 800 * math.sqrt(10), .01)
      and close(w['doublevar'], 400 * math.sqrt(2) * math.sqrt(10), .01)
      and close(w['squared'], 1600 * math.sqrt(10), .01) and close(w['nodouble'], 400 * math.sqrt(10), .01))
s = L11['screens']


def joint_stats(cells, xs, ys):
    ex = sum(xs[i] * cells[i][j] for i in range(len(xs)) for j in range(len(ys)))
    ey = sum(ys[j] * cells[i][j] for i in range(len(xs)) for j in range(len(ys)))
    exy = sum(xs[i] * ys[j] * cells[i][j] for i in range(len(xs)) for j in range(len(ys)))
    vx = sum(xs[i] ** 2 * cells[i][j] for i in range(len(xs)) for j in range(len(ys))) - ex ** 2
    vy = sum(ys[j] ** 2 * cells[i][j] for i in range(len(xs)) for j in range(len(ys))) - ey ** 2
    return ex, ey, exy - ex * ey, vx, vy


cells = lambda sc: [[float(Fr(c)) for c in r] for r in sc['canvas']['params']['cells']]
ex, ey, cov, vx, vy = joint_stats(cells(s[0]), [-1, 0, 1], [-1, 0, 1])
check('l11 S2 covariance 0.36', close(cov, .36, 1e-9) and close(ex, 0, 1e-12) and close(ey, 0, 1e-12))
ex, ey, cov, vx, vy = joint_stats(cells(s[3]), [-1, 2], [-1, 3])
rows = [r[1]['answer'] for r in s[3]['widget']['rows']]
check('l11 S3 table', close(ex, rows[0], 1e-9) and close(ey, rows[1], 1e-9) and close(cov + ex * ey, rows[2], 1e-9)
      and close(cov, rows[3], 1e-9))
check('l11 S4 rho 1/sqrt(6), sds 1.5 and 1.96', close(cov / math.sqrt(vx * vy), 1 / math.sqrt(6), 1e-9)
      and close(math.sqrt(vx), 1.5, 1e-9) and close(math.sqrt(vy), 1.96, .001))
for side, slope in (('left', .8), ('right', 2.4)):
    pts = s[6]['canvas'][side]['params']['points']
    n = len(pts)
    mx, my = sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    syy = sum((p[1] - my) ** 2 for p in pts)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in pts)
    check(f'l11 S6 {side} cloud: fitted slope {slope}, r 0.8', close(sxy / sxx, slope, .002)
          and close(sxy / math.sqrt(sxx * syy), .8, .001))
ex, ey, cov, vx, vy = joint_stats(cells(s[7]), [-1, 0, 1], [0, 1])
check('l11 S7 zero covariance, Y a function of X', close(cov, 0, 1e-12))
ex, ey, cov, vx, vy = joint_stats(cells(s[9]), [-1, 0, 1], [-3, 0, 3])
w = wrongs(s[9]['widget'])
check('l11 S9 rho 0.52', close(cov, .78, 1e-9) and close(cov / math.sqrt(vx * vy), .52, 1e-9)
      and close(w['vars'], .78 / 2.25, 1e-3) and close(w['nosub'], .6, 1e-9))
beta = cov / vx
grid = min((vy + b * b * vx - 2 * b * cov, b) for b in [i / 1000 for i in range(0, 4001)])
check('l11 S10 beta 1.56 minimises Var(Y - bX); residual 3.28',
      close(beta, 1.56, 1e-9) and close(grid[1], 1.56, .002) and close(grid[0], 3.2832, 1e-3)
      and s[10]['widget']['answer'] == 156000)
check('l11 S10 beta = rho sigY/sigX', close(.52 * math.sqrt(vy / vx), 1.56, 1e-9))
s = L12['screens']
pv = lambda w_, sx, sy, r: w_ * w_ * sx * sx + (1 - w_) ** 2 * sy * sy + 2 * w_ * (1 - w_) * r * sx * sy
wstar = lambda sx, sy, r: (sy * sy - r * sx * sy) / (sx * sx + sy * sy - 2 * r * sx * sy)
check('l12 S1 sd 14.14%', close(s[1]['widget']['answer'], math.sqrt(pv(.5, .2, .2, 0)), 1e-4))
check('l12 S2 flat at rho=1', all(close(pv(i / 10, .2, .2, 1), .04, 1e-12) for i in range(11)))
check('l12 S3 riskless at 0.25', close(pv(.25, .3, .1, -1), 0, 1e-15) and s[3]['widget']['answer'] == .25)
gw = min((pv(i / 1000, .3, .1, .8), i / 1000) for i in range(-500, 1001))
check('l12 S4 lowest near -0.27, sd 7.89%', close(gw[1], wstar(.3, .1, .8), .001) and close(wstar(.3, .1, .8), -.2692, 1e-4)
      and close(math.sqrt(gw[0]), .0789, 1e-4))
check('l12 S4 any long X adds risk', all(pv(i / 100, .3, .1, .8) > pv(0, .3, .1, .8) for i in range(3, 101)))
w = wrongs(s[5]['widget'])
check('l12 S5 sd 16.73% and slips', close(s[5]['widget']['answer'], math.sqrt(pv(.5, .3, .1, .2)), 1e-4)
      and close(w['nocov'], math.sqrt(.025), 1e-4) and close(w['onecov'], math.sqrt(.0265), 1e-4))
# "Below 1, the mix is always safer than the average": true for weights strictly between 0 and 1 ...
ok = all(math.sqrt(pv(wi / 20, sx, sy, r / 10)) < wi / 20 * sx + (1 - wi / 20) * sy - 1e-12
         for wi in range(1, 20) for sx in (.1, .2, .3) for sy in (.1, .25) for r in range(-10, 10))
check('l12 S5 long-only mix sd < weighted average of sds when rho < 1', ok)
# ... but not for the short weight the same lesson teaches (finding: hypothesis dropped)
short_sd, short_avg = math.sqrt(pv(-.27, .3, .1, .8)), -.27 * .3 + 1.27 * .1
NOTES.append(f'l12 short weight -0.27, rho 0.8: sd {short_sd:.4f} exceeds the weighted average of sds {short_avg:.4f}')
check('l12 counterexample to the unqualified claim exists', short_sd > short_avg)
w = wrongs(s[7]['widget'])
check('l12 S7 w* 0.1364', close(s[7]['widget']['answer'], wstar(.25, .15, .4), 1e-4)
      and close(w['swap'], 1 - wstar(.25, .15, .4), 1e-4) and close(w['norho'], .0225 / .085, 1e-4))
check('l12 S7 w* turns negative above rho = sigY/sigX', wstar(.25, .15, .59) > 0 > wstar(.25, .15, .61))
eq = lambda n, sd, r: math.sqrt(sd * sd / n + (1 - 1 / n) * r * sd * sd)
w = wrongs(s[8]['widget'])
check('l12 S8 floor 13.42%, 30 assets 14.28%', close(s[8]['widget']['answer'], math.sqrt(.018), 1e-4)
      and close(w['thirty'], eq(30, .3, .2), 1e-4))
rng = random.Random(17)
n, r = 30, .2
vals = []
for _ in range(20000):
    z = rng.gauss(0, 1)
    vals.append(sum(.3 * (math.sqrt(r) * z + math.sqrt(1 - r) * rng.gauss(0, 1)) for _ in range(n)) / n)
mv = sum(vals) / len(vals)
sdp = math.sqrt(sum((v - mv) ** 2 for v in vals) / len(vals))
check('l12 S8 MC equicorrelated 30 assets', abs(sdp - eq(30, .3, .2)) < .004, f'{sdp:.4f}')
check('l12 S9 two funds', close(s[9]['widget']['answer'], math.sqrt(10800 ** 2 + 2400 ** 2 + 2 * .2 * 10800 * 2400), .1)
      and close(wrongs(s[9]['widget'])['nocov'], math.sqrt(10800 ** 2 + 2400 ** 2), .01))
check('l12 S10 index fund 16.47%', close(s[10]['widget']['answer'], eq(500, .3, .3), 1e-4)
      and close(wrongs(s[10]['widget'])['indep'], .3 / math.sqrt(500), 1e-4))

# ------------------------------------------- the seeded explore screens (engine RNG)
# app/js/engine/sim.js uses mulberry32; reproduce it to see what the learner's 1,000 runs show.
M32 = 0xFFFFFFFF


def imul(a, b):
    return (a * b) & M32


def mulberry(seed):
    a = [seed & M32]

    def f():
        a[0] = (a[0] + 0x6D2B79F5) & M32
        t = a[0]
        t = imul(t ^ (t >> 15), t | 1)
        t = (t ^ (t + imul(t ^ (t >> 7), t | 61))) & M32
        return ((t ^ (t >> 14)) & M32) / 4294967296
    return f


d6 = lambda r: 1 + int(r() * 6)
r = mulberry(L6['screens'][1]['canvas']['params']['sim']['seed'])
sev = sum(d6(r) + d6(r) == 7 for _ in range(1000))
NOTES.append(f'l6 S1 seeded run: {sev} sevens in 1,000, average payout {10 * sev / 1000:.2f}')
check('l6 S1 seeded 1,000 tickets return about 1.67', abs(10 * sev / 1000 - 10 / 6) < .15, str(sev))
r = mulberry(L8['screens'][1]['canvas']['params']['sim']['seed'])
six = sum(sum(r() < 1 / 6 for _ in range(10)) for _ in range(1000)) / 1000
NOTES.append(f'l8 S1 seeded run: average sixes {six:.3f}')
check('l8 S1 seeded average near 1.67 and below 2', abs(six - 10 / 6) < .1 and six < 2, f'{six:.3f}')
cv = L7['screens'][1]['canvas']
r = mulberry(cv['left']['params']['sim']['seed'])
a1 = sum(d6(r) + d6(r) for _ in range(1000)) / 1000
r = mulberry(cv['right']['params']['sim']['seed'])
a2 = sum(2 * d6(r) for _ in range(1000)) / 1000
NOTES.append(f'l7 S1 seeded averages: X+Y {a1:.2f}, X+X {a2:.2f}')
check('l7 S1 seeded averages both near 7', abs(a1 - 7) < .15 and abs(a2 - 7) < .2, f'{a1:.2f} {a2:.2f}')

# --------------------------------------------------- reviews, homework, problems
R1, R2, R3 = load('review-1'), load('review-2'), load('review-3')
it = R1['items']
check('r1 c=0.1', it[1]['widget']['answer'] == .1)
check('r1 P(N=2)=0.432', close(it[4]['widget']['answer'], 3 * .6 * .6 * .4, 1e-12))
check('r1 P(C>=2)=3/36', close(it[6]['widget']['answer'], tot[11] + tot[12], 1e-4))
check('r1 VaR 6', it[7]['widget']['answer'] == var_q([(0, .6), (1, .2), (3, .12), (6, .05), (12, .03)], .95))
it = R2['items']
check('r2 round trip 0.85', close(it[0]['widget']['answer'], 4 * .55 - 3 * .45, 1e-12))
check('r2 seller 200', close(it[5]['widget']['answer'], 600 * (2 - 10 / 6), 1e-9))
check('r2 call 2.625', close(it[8]['widget']['answer'], .25 * (50 * 1.1 * 1.1 - 50), 1e-9))
cnt = sum(sum(1 for i in range(9) if t[i] == t[i + 1] == 'H') for t in product('HT', repeat=10))
check('r2 doubles 2.25 exact', Fr(cnt, 2 ** 10) == Fr(9, 4) and it[9]['widget']['answer'] == 2.25)
it = R3['items']
m_, v_ = pmf_stats({-2: .25, 0: .5, 4: .25})
check('r3 variance 4.75', close(v_, 4.75, 1e-12) and close(wrongs(it[0]['widget'])['abs'], 1.75, 1e-9))
ex, ey, cov, vx, vy = joint_stats([[.4, .1], [.1, .4]], [0, 1], [0, 1])
check('r3 rho 0.6', close(cov / math.sqrt(vx * vy), .6, 1e-9))
check('r3 mix 17.32%', close(it[3]['widget']['answer'], math.sqrt(pv(.5, .2, .2, .5)), 1e-4))
check('r3 Var(X-Y)=7', it[7]['widget']['answer'] == 4 + 9 - 2 * 3)
check('r3 w*=0.2, sd 8.94%', close(wstar(.2, .1, 0), .2, 1e-12) and close(math.sqrt(pv(.2, .2, .1, 0)), .0894, 1e-4))
H1, H2, H3 = load('homework-1'), load('homework-2'), load('homework-3')
it = H1['items']
check('h1 P(min=2)=9/36', sum(1 for a, b in dice if min(a, b) == 2) == 9)
check('h1 F_M(2)=20/36', close(it[2]['widget']['answer'], Fr(sum(1 for a, b in dice if min(a, b) <= 2), 36), 1e-4))
three = {}
for mv_ in product([(2, .3), (0, .5), (-2, .2)], repeat=3):
    k = 100 + sum(x for x, _ in mv_)
    three[k] = three.get(k, 0) + math.prod(p for _, p in mv_)
w = wrongs(it[4]['widget'])
check('h1 call pays 0.162', close(it[4]['widget']['answer'], sum(p for x, p in three.items() if x > 102), 1e-9)
      and close(w['at-strike'], sum(p for x, p in three.items() if x >= 102), 1e-9))
check('h1 VaR 4', it[5]['widget']['answer'] == var_q([(-3, .25), (-1, .3), (0, .2), (2, .12), (4, .08), (8, .04), (15, .01)], .95))
check('h1 remainder uniform', all(sum(p for x, p in tot.items() if x % 3 == r_) == Fr(1, 3) for r_ in range(3)))
ns = {}
exec(it[8]['widget']['solution'], ns)
ts = {t_: .7 ** t_.count('H') * .3 ** t_.count('T') for t_ in map(''.join, product('HT', repeat=3))}
got = ns['pmf_of'](ts, lambda q_: max(len(run) for run in q_.split('T')))
check('h1 code: longest run pmf', all(close(got[k], v, 1e-9) for k, v in {0: .027, 1: .336, 2: .294, 3: .343}.items()))
acc = 0
for _ in range(10):
    acc += .1
check('h1 code feedback: ten 0.1s one at a time', repr(acc) == '0.9999999999999999')
check('h1 code feedback: test 7 total with sum', repr(sum(ts.values())) == '0.9999999999999998')
it = H2['items']
check('h2 capped St Petersburg 5', it[4]['widget']['answer'] == sum(2 ** k * Fr(1, 2 ** k) for k in range(1, 6)))
check('h2 distinct faces', close(it[5]['widget']['answer'], 6 * (1 - (5 / 6) ** 6), 1e-4))
rng = random.Random(23)
dd = sum(len({rng.randrange(6) for _ in range(6)}) for _ in range(40000)) / 40000
check('h2 MC distinct faces', abs(dd - 3.9906) < .02, f'{dd:.3f}')
check('h2 E[X(7-X)]=28/3', close(it[6]['widget']['answer'], sum(k * (7 - k) for k in range(1, 7)) / 6, 1e-4))
ov = 1 / 1.8 + 1 / 3.6 + 1 / 4.5
check('h2 overround 5.56%, balanced book keeps 1/19', close(it[7]['widget']['answer'], ov - 1, 1e-4)
      and close((ov - 1) / ov, 1 / 19, 1e-12))
check('h2 empty venues', close(it[9]['widget']['answer'], 10 * .9 ** 10, 1e-4))
ev = sum(10 - len({rng.randrange(10) for _ in range(10)}) for _ in range(40000)) / 40000
check('h2 MC empty venues', abs(ev - 3.4868) < .02, f'{ev:.3f}')
p3 = [sum(1 for i, x in enumerate(p) if i == x) for p in permutations(range(3))]
check('h2 longform n=3: matches 3,1,1,1,0,0', sorted(p3) == [0, 0, 1, 1, 1, 3])
it = H3['items']
check('h3 Var max(X-4,0) = 7/12', close(it[0]['widget']['answer'], pmf_stats({0: Fr(4, 6), 1: Fr(1, 6), 2: Fr(1, 6)})[1], 1e-4))
check('h3 two traders sd', close(it[3]['widget']['answer'], 1000 * math.sqrt(13), .01))
check('h3 smallest n is 13', it[5]['widget']['answer'] == min(n_ for n_ in range(1, 200) if eq(n_, .25, .36) <= .16))
ex, ey, cov, vx, vy = joint_stats([[.2, .2], [.1, .5]], [-10, 20], [-5, 15])
check('h3 longform', close(ex, 8) and close(ey, 9) and close(vx, 216) and close(vy, 84) and close(cov, 48)
      and close(cov / math.sqrt(vx * vy), .356, 1e-3) and close(vx + vy + 2 * cov, 396))
check('h3 70:30 sd 17.15%', close(it[7]['widget']['answer'], math.sqrt(pv(.7, .25, .1, -.2)), 1e-4))
P1, P2, P3 = load('problems-1'), load('problems-2'), load('problems-3')
sp = {}
for a, b in product(range(1, 5), repeat=2):
    sp[a * b] = sp.get(a * b, 0) + Fr(1, 16)
pa = [p['widget'].get('answer') for p in P1['items'][0]['parts']]
check('p1 spinner', [Fr(pa[0]).limit_denominator(16), Fr(pa[1]).limit_denominator(16), Fr(pa[2]).limit_denominator(16),
                     Fr(pa[3]).limit_denominator(16)] ==
      [sp[4], sum(p for x, p in sp.items() if x <= 4), sum(p for x, p in sp.items() if 4 < x <= 9),
       sum(p for x, p in sp.items() if x <= 6)])
b4 = [(25 * k, math.comb(4, k) * .1 ** k * .9 ** (4 - k)) for k in range(5)]
b3 = [(25 * k, math.comb(3, k) * .1 ** k * .9 ** (3 - k)) for k in range(4)]
check('p1 bonds VaR 50 then 25', var_q(b4, .95) == 50 == P1['items'][1]['parts'][3]['widget']['answer'] and var_q(b3, .95) == 25)
y = {0: .2, 1: .55, 2: .25}
check('p1 straddle P(T>=3)', close(P1['items'][2]['parts'][3]['widget']['answer'],
                                  sum(y[a] * y[b] for a in y for b in y if a + b >= 3), 1e-12))
check('p1 dealers', P1['items'][3]['parts'][3]['widget']['answer'] == min(n_ for n_ in range(1, 99) if 1 - .6 ** n_ >= .99)
      and close(P1['items'][3]['parts'][2]['widget']['answer'], Fr(37, 125), 1e-9))
pp = P2['items'][0]['parts']
check('p2 insurer', pp[0]['widget']['answer'] == 45 and pp[3]['widget']['answer'] == 150 * .1 + 450 * .05 + 20)
rev = sum(sum(1 for i in range(1, 6) if t[i] != t[i - 1]) * .6 ** t.count('U') * .4 ** t.count('D')
          for t in product('UD', repeat=6))
check('p2 reversals: 0.48 a day (6-day exact check)', close(rev, 5 * .48, 1e-12))
check('p2 reversals key', close(P2['items'][1]['parts'][1]['widget']['answer'], 19 * .48, 1e-12)
      and close(P2['items'][1]['parts'][3]['widget']['answer'], 57 - 8 * 9.12, 1e-9))
check('p2 one reversal does raise the chance of the next (0.5 > 0.48), mean unchanged',
      close((.6 * .4 * .6 + .4 * .6 * .4) / .48, .5, 1e-12))
S_ = {34: .1, 38: .3, 42: .4, 48: .2}
ec = sum(max(x - 40, 0) * p for x, p in S_.items())
eqp = sum(max(40 - x, 0) * p for x, p in S_.items())
check('p2 call 2.4, put 1.2, parity in expectation', close(ec, 2.4) and close(eqp, 1.2)
      and close(ec - eqp, sum(x * p for x, p in S_.items()) - 40, 1e-12))
hands = list(combinations('GGGSSSSSSS', 4))
hands = list(combinations(range(10), 4))
g = [sum(1 for t in h if t < 3) for h in hands]
price = Fr(sum(20 * k + 5 * (4 - k) + 15 * max(k - 1, 0) for k in g), len(g))
check('p2 tokens: P(G>=2)=1/3, fair price 43.5', Fr(sum(1 for k in g if k >= 2), len(g)) == Fr(1, 3) and price == Fr(87, 2)
      and P2['items'][3]['parts'][4]['widget']['answer'] == 43.5)
rng = random.Random(31)
third = sum(rng.sample(range(10), 4)[2] < 3 for _ in range(40000)) / 40000
check('p2 MC third token gold 0.3', abs(third - .3) < .01, f'{third:.3f}')
m_, v_ = pmf_stats({-3: .2, 1: .5, 4: .3})
pp = P3['items'][0]['parts']
check('p3 market maker', close(m_, 1.1) and close(v_, 5.89, 1e-9) and close(pp[2]['widget']['answer'], math.sqrt(589), 1e-3)
      and pp[3]['widget']['answer'] == min(n_ for n_ in range(1, 2000) if math.sqrt(5.89 * n_) <= .11 * n_))
ex, ey, cov, vx, vy = joint_stats([[.3, .1], [.1, .5]], [-1, 2], [-2, 2])
pp = P3['items'][1]['parts']
h = cov / vy
check('p3 fund and future', close(ex, .8) and close(ey, .4) and close(vx, 2.16) and close(vy, 3.84) and close(cov, 1.68)
      and close(cov / math.sqrt(vx * vy), 7 / 12, 1e-9) and close(h, .4375, 1e-9)
      and close(vx + h * h * vy - 2 * h * cov, 1.425, 1e-9) and close(vx * (1 - 49 / 144), 1.425, 1e-9))
check('p3 fund E[A] stored as a fraction for the % unit', pp[0]['widget']['answer'] == .008 and pp[0]['widget'].get('unit') == '%')
mx_, vx_ = pmf_stats({-.1: .2, .1: .5, .3: .3})
check('p3 two funds', close(mx_, .12, 1e-12) and close(vx_, .0196, 1e-12) and close(.0049 / (vx_ + .0049), .2, 1e-9)
      and close(math.sqrt(.04 * vx_ + .64 * .0049), .0626, 1e-4))
# linked fills: a model with P(fill)=0.5 and P(both)=0.3 exists (20% of days all four share one coin)
rng = random.Random(41)
ns_ = []
for _ in range(60000):
    if rng.random() < .2:
        ns_.append(4 * (rng.random() < .5))
    else:
        ns_.append(sum(rng.random() < .5 for _ in range(4)))
mn = sum(ns_) / len(ns_)
vn = sum((x - mn) ** 2 for x in ns_) / len(ns_)
check('p3 MC linked fills Var(N)=1.6', abs(vn - 1.6) < .04 and abs(mn - 2) < .03, f'{vn:.3f}')
pp = P3['items'][3]['parts']
check('p3 linked fills keys', pp[1]['widget']['answer'] == 1.6 and close(pp[2]['widget']['answer'], 12 * math.sqrt(1.6), 1e-3)
      and pp[3]['widget']['answer'] == max(n_ for n_ in range(1, 50) if 12 * math.sqrt(.25 * n_ + .05 * n_ * (n_ - 1)) <= 20))
# fluency: sd of a two-point trade is sqrt(pq)(a+b) for every draw of the family
FL = load('fluency-l9-measuring-spread')
ok = True
for p, q_ in FL['families'][2]['vars']['pq']['pick']:
    for a in range(1, 13):
        for b in range(1, 13):
            ok &= close(math.sqrt(pmf_stats({a: p, -b: q_})[1]), math.sqrt(p * q_) * (a + b), 1e-9)
check('fluency family 3 closed form', ok)

for n_ in NOTES:
    print('note:', n_)
print(f'{N[0]} checks, {len(FAIL)} failed')
sys.exit(1 if FAIL else 0)
