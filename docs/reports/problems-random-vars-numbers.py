"""Recompute every number in app/content/courses/random-vars/problems-<n>.json twice.

Method 1 is exact (fractions.Fraction and closed forms). Method 2 is independent:
brute enumeration of the outcome space, or a different route (complements against
sums, E[X^2] - E[X]^2 against the definition, simulation-free exact enumeration of
products of independent variables). For each part the script checks: the two methods
agree; the JSON key equals them within its tol; every `wrong` value matches its named
slip and lies outside the key's band; no two wrongs overlap. Choice parts check the
keyed option and the numbers its text states. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-random-vars-numbers.py
"""
import json, os, sys, itertools
from fractions import Fraction as F
from math import comb, isclose

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'random-vars')
fails, checks = [], 0


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {it['id']: it for it in d['items']}


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def num(items, iid, k, exact, alt, slips=None, round_tol=0.0005):
    """Part k (1-based) of item iid: a numeric key, two methods, named slips."""
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e = float(exact)
    ok(isclose(e, float(alt), rel_tol=1e-9, abs_tol=1e-12), f'{tag}: methods differ {e} vs {float(alt)}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= max(tol, 1e-9), f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, round_tol), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
    for a, b in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')


def pick(items, iid, k, correct_id):
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')


def pmf_of(space, X):
    """space: {outcome: chance}; X: outcome -> value. Returns {value: chance}."""
    out = {}
    for w, p in space.items():
        out[X(w)] = out.get(X(w), 0) + p
    return out


def cdf(pmf, x):
    return sum((p for v, p in pmf.items() if v <= x), F(0))


def E(pmf, g=lambda v: v):
    return sum((p * g(v) for v, p in pmf.items()), F(0))


def var(pmf):
    m = E(pmf)
    return E(pmf, lambda v: (v - m) ** 2)


def product_space(*marginals):
    """Independent coordinates: each marginal is {value: chance}."""
    space = {}
    for combo in itertools.product(*[list(m.items()) for m in marginals]):
        vals = tuple(v for v, _ in combo)
        pr = F(1)
        for _, p in combo:
            pr *= p
        space[vals] = space.get(vals, 0) + pr
    return space


# ------------------------------------------------------------------ level 1
L1 = load(1)

# p-spinner-product: two spins of a fair 1..4 spinner, M = product, W = max(M - 6, 0)
spin = {v: F(1, 4) for v in range(1, 5)}
sp2 = product_space(spin, spin)
M = pmf_of(sp2, lambda w: w[0] * w[1])
cells = list(itertools.product(range(1, 5), repeat=2))
count = lambda pred: F(sum(1 for c in cells if pred(c)), 16)
num(L1, 'p-spinner-product', 1, M[4], count(lambda c: c[0] * c[1] == 4),
    {'unordered': F(2, 16), 'double-two': F(4, 16), 'square-only': F(1, 16)})
num(L1, 'p-spinner-product', 2, cdf(M, 4), count(lambda c: c[0] * c[1] <= 4),
    {'strict': cdf(M, 3), 'carried': cdf(M, 3) + F(2, 16)})
F9 = 1 - (M[12] + M[16])
num(L1, 'p-spinner-product', 3, F9 - cdf(M, 4), count(lambda c: 4 < c[0] * c[1] <= 9),
    {'closed': F9 - cdf(M, 3), 'top-only': F9, 'carried': F9 - F(7, 16)})
ok(F9 == cdf(M, 9) == F(13, 16), 'F(9) is not 13/16')
W = pmf_of(sp2, lambda w: max(w[0] * w[1] - 6, 0))
num(L1, 'p-spinner-product', 4, cdf(M, 4) + M[6], W[0],
    {'strict': cdf(M, 5), 'pays': 1 - W[0], 'carried': F(7, 16) + M[6]})
ok(5 not in M, 'a product of 5 is possible')

# p-bond-defaults: N ~ Bin(4, 0.1), L = 25N
q = F(1, 10)
bern = {1: q, 0: 1 - q}
Nd = pmf_of(product_space(*[bern] * 4), sum)
binom = lambda n, k: comb(n, k) * q ** k * (1 - q) ** (n - k)
num(L1, 'p-bond-defaults', 1, binom(4, 1), Nd[1],
    {'one-order': q * (1 - q) ** 3, 'no-survivors': 4 * q, 'plain': q})
num(L1, 'p-bond-defaults', 2, binom(4, 0) + binom(4, 1), cdf(Nd, 1),
    {'zero-only': Nd[0], 'carried': Nd[0] + q * (1 - q) ** 3})
num(L1, 'p-bond-defaults', 3, binom(4, 2), Nd[2],
    {'one-order': q ** 2 * (1 - q) ** 2, 'four-ways': 4 * q ** 2 * (1 - q) ** 2, 'twelve': 12 * q ** 2 * (1 - q) ** 2})
Ld = {25 * k: p for k, p in Nd.items()}
var95 = min(l for l in Ld if cdf(Ld, l) >= F(95, 100))
var95_b = next(25 * k for k in range(5) if sum(binom(4, j) for j in range(k + 1)) >= F(95, 100))
num(L1, 'p-bond-defaults', 4, var95, var95_b, {'just-under': 25, 'count': 2})
ok(cdf(Ld, 25) < F(95, 100) and abs(float(cdf(Ld, 50)) - 0.9963) < 1e-9, 'F_L(25), F_L(50) wrong')
N3 = pmf_of(product_space(*[bern] * 3), sum)
L3d = {25 * k: p for k, p in N3.items()}
var95_3 = min(l for l in L3d if cdf(L3d, l) >= F(95, 100))
ok(var95_3 == 25 and cdf(N3, 1) == F(972, 1000) and N3[0] == F(729, 1000), 'three-bond VaR is not 25')
pick(L1, 'p-bond-defaults', 5, 'halves')

# p-straddle-days: X on -2..2, Y = |X|, T = Y1 + Y2 over two independent days
pX = {-2: F(1, 10), -1: F(3, 10), 0: F(2, 10), 1: F(25, 100)}
c = 1 - sum(pX.values())
num(L1, 'p-straddle-days', 1, c, F(15, 100), {'sum': sum(pX.values()), 'equal': F(1, 5)})
pX[2] = c
Y = pmf_of(pX, abs)
num(L1, 'p-straddle-days', 2, Y[2], pX[-2] + pX[2], {'one-side': pX[2], 'neg-only': pX[-2], 'carried': pX[-2] + F(85, 100)})
num(L1, 'p-straddle-days', 3, 1 - Y[2], cdf(Y, 1), {'strict': Y[0], 'x-cdf': cdf(pX, 1), 'ones-only': Y[1]})
ok(Y[1] == F(55, 100) and Y[0] == F(2, 10), 'P(Y=1), P(Y=0) as stated')
T = pmf_of(product_space(Y, Y), sum)
num(L1, 'p-straddle-days', 4, Y[2] ** 2 + 2 * Y[1] * Y[2], 1 - cdf(T, 2),
    {'one-order': Y[2] ** 2 + Y[1] * Y[2], 'both-two': Y[2] ** 2, 'complement': 1 - (1 - Y[2]) ** 2})

# p-tightest-quote: T = min of three independent uniform 1..5 spreads
u5 = {v: F(1, 5) for v in range(1, 6)}
trip = list(itertools.product(range(1, 6), repeat=3))
Tq = pmf_of(product_space(u5, u5, u5), min)
num(L1, 'p-tightest-quote', 1, 3 ** 3, sum(1 for t in trip if min(t) >= 3),
    {'one-dealer': 3, 'strict': 8, 'complement': 98})
num(L1, 'p-tightest-quote', 2, 1 - F(27, 125), cdf(Tq, 2),
    {'no-complement': F(27, 125), 'all-low': F(2, 5) ** 3, 'one-dealer': F(2, 5)})
ok(cdf(Tq, 1) == 1 - F(4, 5) ** 3 == F(61, 125), 'F_T(1) is not 0.488')
num(L1, 'p-tightest-quote', 3, cdf(Tq, 2) - cdf(Tq, 1), Tq[2],
    {'cdf': cdf(Tq, 2), 'one-dealer': F(1, 5), 'all-two': F(1, 125)})
n_need = next(n for n in range(1, 50) if 1 - F(4, 5) ** n >= F(9, 10))
# part 4: smallest n with P(T <= 2) >= 0.99 on n dealers (exact, then by brute force on 1 - 0.6^n)
n_need = next(n for n in range(1, 60) if 1 - F(3, 5) ** n >= F(99, 100))
n_alt = next(n for n in range(1, 60) if 0.6 ** n <= 0.01)
num(L1, 'p-tightest-quote', 4, n_need, n_alt,
    {'round-down': n_need - 1, 'old-base': next(n for n in range(1, 80) if 0.8 ** n <= 0.01), 'two-fifths': next(n for n in range(1, 60) if 0.4 ** n <= 0.01)})
ok(F(98, 125) == 1 - F(3, 5) ** 3 and abs(0.6 ** 9 - 0.0101) < 0.00005 and abs(0.6 ** 10 - 0.0060) < 0.00005, '0.6^3, 0.6^9, 0.6^10 as stated')

# ------------------------------------------------------------------ level 2
L2 = load(2)

# p-phone-cover: claim X on {0, 200, 500}; excess of 50 on claims only
X = {0: F(85, 100), 200: F(10, 100), 500: F(5, 100)}
EX = E(X)
policies = 2000
num(L2, 'p-phone-cover', 1, EX, sum(v * p for v, p in X.items()),
    {'unweighted': F(700, 3), 'missed-500': 200 * F(1, 10), 'mode': 0})
num(L2, 'p-phone-cover', 2, 60 - EX, E(X, lambda v: 60 - v),
    {'reversed': EX - 60, 'carried-unweighted': 60 - F(700, 3), 'carried-500': 60 - 20})
num(L2, 'p-phone-cover', 3, policies * (60 - EX), policies * 60 - policies * EX,
    {'one-policy': 60 - EX, 'revenue': policies * 60, 'claims': policies * EX})
Xe = pmf_of(X, lambda v: max(v - 50, 0))
num(L2, 'p-phone-cover', 4, EX - 50 * (1 - X[0]) + 20, E(Xe) + 20,
    {'excess-all': EX - 50 + 20, 'old-claims': EX + 20, 'fair': E(Xe)})

# p-reversal-days: 20 independent days, up w.p. 0.6; enumerate exactly on fewer days, then scale
u = F(6, 10)
day = {1: u, 0: 1 - u}
pr = u * (1 - u) + (1 - u) * u
def ER_enum(n):   # exact expectation of reversals over n days by enumeration
    sp = product_space(*[day] * n)
    return sum(p * sum(1 for k in range(1, n) if w[k] != w[k - 1]) for w, p in sp.items())
ok(ER_enum(6) == 5 * pr and ER_enum(8) == 7 * pr, 'enumerated reversals do not match (n-1) * 0.48')
ER = 19 * pr
num(L2, 'p-reversal-days', 1, pr, 1 - (u ** 2 + (1 - u) ** 2),
    {'one-way': u * (1 - u), 'same': u ** 2 + (1 - u) ** 2, 'half': F(1, 2)})
num(L2, 'p-reversal-days', 2, ER, ER_enum(10) / 9 * 19,
    {'twenty': 20 * pr, 'one-way': 19 * u * (1 - u), 'same': 19 * (1 - pr)})
pick(L2, 'p-reversal-days', 3, 'nothing')
num(L2, 'p-reversal-days', 4, 57 - 8 * ER, 3 * (19 - ER) - 5 * ER,
    {'twenty': 3 * (20 - ER) - 5 * ER, 'no-gains': -5 * ER, 'carried': 57 - 8 * 20 * pr})
ok(isclose(float(3 * (20 - ER) - 5 * ER), -12.96), 'twenty slip is not -12.96')
g = 5 * ER / (19 - ER)
num(L2, 'p-reversal-days', 5, g, 5 * pr / (1 - pr), {'flipped': 5 * (19 - ER) / ER, 'equal': 5}, round_tol=0.005)

# p-month-options: S on {34, 38, 42, 48}
Sd = {34: F(1, 10), 38: F(3, 10), 42: F(4, 10), 48: F(2, 10)}
ES = E(Sd)
EC = E(Sd, lambda s: max(s - 40, 0))
EQ = E(Sd, lambda s: max(40 - s, 0))
num(L2, 'p-month-options', 1, ES, sum(Sd[s] * s for s in Sd), {'unweighted': F(34 + 38 + 42 + 48, 4), 'mode': 42})
num(L2, 'p-month-options', 2, EC, 2 * F(4, 10) + 8 * F(2, 10),
    {'mean-payoff': max(ES - 40, 0), 'top-only': 8 * F(2, 10), 'unweighted': F(10, 4)})
num(L2, 'p-month-options', 3, EC - (ES - 40), EQ, {'sign': EC + (ES - 40), 'carried': EC - (F(162, 4) - 40)})
ok(all(max(s - 40, 0) - max(40 - s, 0) == s - 40 for s in Sd), 'C - Q = S - 40 fails')
num(L2, 'p-month-options', 4, (EC - F(210, 100)) + (F(150, 100) - EQ), (ES - 40) - (F(210, 100) - F(150, 100)),
    {'both-bought': (EC - F(210, 100)) + (EQ - F(150, 100)), 'call-only': EC - F(210, 100), 'sign': -((EC - F(210, 100)) + (F(150, 100) - EQ))})

# p-token-draw: 3 gold (20) and 7 silver (5), draw 4 without replacement
bag = ['g'] * 3 + ['s'] * 7
seqs = list(itertools.permutations(range(10), 4))
Pseq = F(1, len(seqs))
third = sum(Pseq for s in seqs if bag[s[2]] == 'g')
num(L2, 'p-token-draw', 1, F(3, 10), third, {'shrunk': F(3, 8), 'summed': F(9, 10)})
Gd = pmf_of({s: Pseq for s in seqs}, lambda s: sum(1 for i in s if bag[i] == 'g'))
num(L2, 'p-token-draw', 2, 4 * F(3, 10), E(Gd),
    {'one-draw': F(3, 10), 'all-gold': 3, 'shrinking': F(3, 10) + F(3, 9) + F(3, 8) + F(3, 7)})
EV = 20 + 15 * E(Gd)
Vd = pmf_of(Gd, lambda k: 20 * k + 5 * (4 - k))
num(L2, 'p-token-draw', 3, EV, E(Vd),
    {'no-silver': 20 * F(12, 10), 'mean-token': 4 * F(25, 2), 'drop-shift': 15 * F(12, 10),
     'carried': 20 + 15 * (F(3, 10) + F(3, 9) + F(3, 8) + F(3, 7))})
ok(isclose(float(4 * (F(3, 10) * 20 + F(7, 10) * 5)), 38), 'per-draw check is not 38')
pge2 = F(comb(3, 2) * comb(7, 2) + comb(3, 3) * comb(7, 1), comb(10, 4))
binge2 = 1 - F(7, 10) ** 4 - 4 * F(3, 10) * F(7, 10) ** 3
num(L2, 'p-token-draw', 4, pge2, Gd[2] + Gd[3],
    {'replaced': binge2, 'exactly-two': Gd[2], 'at-least-one': 1 - Gd[0]})
ok(Gd[2] == F(63, 210) and Gd[3] == F(7, 210), 'hand counts are not 63 and 7')
# part 5: £15 for each gold token after the first, 15 * max(G - 1, 0)
pge3 = Gd[3]
num(L2, 'p-token-draw', 5, EV + 15 * (pge2 + pge3), E(Gd, lambda k: 20 + 15 * k + 15 * max(k - 1, 0)),
    {'no-bonus': EV, 'once-only': EV + 15 * pge2, 'full-bonus': EV + 15, 'bonus-only': 15 * (pge2 + pge3), 'carried': EV + 15 * (binge2 + pge3)})
ok(pge3 == F(1, 30) and EV + 15 * (E(Gd) - (1 - Gd[0])) == F(87, 2), 'p-token-draw p5: 1/30 or 43.50 by the other route wrong')

# ------------------------------------------------------------------ level 3
L3 = load(3)
from math import sqrt

# p-quote-trades: X on {-3, 1, 4}; totals of independent trades
Xq = {-3: F(2, 10), 1: F(5, 10), 4: F(3, 10)}
mq, vq = E(Xq), var(Xq)
num(L3, 'p-quote-trades', 1, mq, sum(v * p for v, p in Xq.items()),
    {'unweighted': F(2, 3), 'sign': 3 * F(2, 10) + F(5, 10) + 4 * F(3, 10), 'mode': 1})
num(L3, 'p-quote-trades', 2, E(Xq, lambda v: v * v) - mq ** 2, vq,
    {'no-mean': E(Xq, lambda v: v * v), 'mean-not-squared': E(Xq, lambda v: v * v) - mq,
     'carried': E(Xq, lambda v: v * v) - F(2, 3) ** 2, 'sd': sqrt(vq)}, round_tol=0.001)
two = pmf_of(product_space(Xq, Xq), sum)        # exact: Var of a sum of two = 2 Var
ok(var(two) == 2 * vq, 'variance of two trades is not 2 Var(X)')
num(L3, 'p-quote-trades', 3, sqrt(100 * vq), 10 * sqrt(float(var(two)) / 2),
    {'sd-times-n': 100 * sqrt(vq), 'variance': 100 * vq, 'one-trade': sqrt(vq)})
n_q = next(n for n in range(1, 5000) if vq * n <= (mq * n / 10) ** 2)
n_alt = next(n for n in range(1, 5000) if sqrt(5.89 * n) <= 0.11 * n)
num(L3, 'p-quote-trades', 4, n_q, n_alt, {'round-down': n_q - 1, 'no-square': 23})
ok(22 < sqrt(5.89) / 0.11 < 23 and isclose(5.89 / 0.0121, 486.7769, abs_tol=1e-3), 'stated 22.06 and 486.8 wrong')

# p-fund-hedge: joint pmf of (A, B)
J = {(-1, -2): F(3, 10), (-1, 2): F(1, 10), (2, -2): F(1, 10), (2, 2): F(5, 10)}
pA = pmf_of(J, lambda w: w[0]); pB = pmf_of(J, lambda w: w[1])
EA, EB, VA, VB = E(pA), E(pB), var(pA), var(pB)
cov = E(J, lambda w: (w[0] - EA) * (w[1] - EB))
EAB = E(J, lambda w: w[0] * w[1])
# part 1 is typed in per cent (unit %), so the key is the fraction E[A] / 100
num(L3, 'p-fund-hedge', 1, EA / 100, (-1 * (J[(-1, -2)] + J[(-1, 2)]) + 2 * (J[(2, -2)] + J[(2, 2)])) / 100,
    {'unweighted': F(1, 2) / 100, 'b-mean': EB / 100}, round_tol=0.000005)
ok(EB == F(4, 10) and VB == F(384, 100), 'E[B], Var(B) as stated')
num(L3, 'p-fund-hedge', 2, E(pA, lambda v: v * v) - EA ** 2, VA,
    {'no-mean': E(pA, lambda v: v * v), 'unsquared-mean': E(pA, lambda v: v * v) - EA, 'carried': E(pA, lambda v: v * v) - F(1, 4)})
num(L3, 'p-fund-hedge', 3, EAB - EA * EB, cov, {'no-means': EAB, 'added': EAB + EA * EB, 'means-only': EA * EB})
rho = float(cov) / sqrt(VA * VB)
ok(VA * VB == F(288, 100) ** 2, 'sd product is not 2.88')
num(L3, 'p-fund-hedge', 4, cov / F(288, 100), rho,
    {'variances': cov / (VA * VB), 'cov-over-var': cov / VA, 'carried': EAB / F(288, 100)})
h = cov / VB
ok(h == F(4375, 10000), 'h is not 0.4375')
hedged = pmf_of(J, lambda w: w[0] - h * w[1])
num(L3, 'p-fund-hedge', 5, VA + h * h * VB - 2 * h * cov, var(hedged),
    {'cov-sign': VA + h * h * VB + 2 * h * cov, 'no-cross': VA + h * h * VB, 'h-unsquared': VA + h * VB - 2 * h * cov})
ok(VA * (1 - (cov / F(288, 100)) ** 2) == var(hedged) == VA * F(95, 144), 'Var(A)(1 - rho^2) check fails')

# p-two-funds: X on {-0.1, 0.1, 0.3}, Y independent with mean 0.05, var 0.0049
Xf = {F(-1, 10): F(2, 10), F(1, 10): F(5, 10), F(3, 10): F(3, 10)}
mX, vX = E(Xf), var(Xf)
mY, vY = F(5, 100), F(49, 10000)
Yf = {mY - F(7, 100): F(1, 2), mY + F(7, 100): F(1, 2)}     # a two-point Y with that mean and variance
ok(E(Yf) == mY and var(Yf) == vY, 'two-point Y does not match')
num(L3, 'p-two-funds', 1, mX, sum(v * p for v, p in Xf.items()), {'unweighted': F(1, 10), 'sign': F(16, 100)})
num(L3, 'p-two-funds', 2, E(Xf, lambda v: v * v) - mX ** 2, vX,
    {'no-mean': E(Xf, lambda v: v * v), 'carried': E(Xf, lambda v: v * v) - F(1, 100), 'sd': sqrt(vX)})
wstar = vY / (vX + vY)
grid = min((F(k, 1000) for k in range(0, 1001)), key=lambda w: w * w * vX + (1 - w) ** 2 * vY)
num(L3, 'p-two-funds', 3, wstar, grid,
    {'flipped': 1 - wstar, 'sd-ratio': F(7, 100) / (F(14, 100) + F(7, 100)), 'carried': vY / (E(Xf, lambda v: v * v) + vY)}, round_tol=0.0005)
port = pmf_of(product_space(Xf, Yf), lambda w: wstar * w[0] + (1 - wstar) * w[1])
sdp = sqrt(wstar ** 2 * vX + (1 - wstar) ** 2 * vY)
num(L3, 'p-two-funds', 4, sdp, sqrt(var(port)),
    {'averaged-sd': wstar * sqrt(vX) + (1 - wstar) * sqrt(vY), 'unsquared': sqrt(wstar * vX + (1 - wstar) * vY),
     'variance': wstar ** 2 * vX + (1 - wstar) ** 2 * vY}, round_tol=0.0001)
mP = wstar * mX + (1 - wstar) * mY
ok(mP == E(port) == F(64, 1000), 'portfolio mean is not 0.064')
ratios = {'x': float(mX) / sqrt(vX), 'y': float(mY) / sqrt(vY), 'mix': float(mP) / sdp}
ok(max(ratios, key=ratios.get) == 'mix', 'the mix does not have the best ratio')
ok(round(ratios['mix'], 2) == 1.02 and round(ratios['x'], 2) == 0.86 and round(ratios['y'], 2) == 0.71, f'ratios as stated {ratios}')
pick(L3, 'p-two-funds', 5, 'mix')

# p-clustered-fills: exchangeable fills, P(fill) 0.5, P(both) 0.3
pf, pboth = F(1, 2), F(3, 10)
cv = pboth - pf * pf
VN = lambda n: n * pf * (1 - pf) + n * (n - 1) * cv
# Method 2: a mixture model with these moments: half the days p = 0.5 + d, half p = 0.5 - d, d^2 = 0.05
d = sqrt(0.05)
def mix_var(n):
    tot = {}
    for p in (0.5 + d, 0.5 - d):
        for s in itertools.product([0, 1], repeat=n):
            pr_ = 0.5
            for x in s:
                pr_ *= p if x else 1 - p
            tot[sum(s)] = tot.get(sum(s), 0) + pr_
    m = sum(k * v for k, v in tot.items())
    return sum((k - m) ** 2 * v for k, v in tot.items())
num(L3, 'p-clustered-fills', 1, cv, (0.5 * (0.5 + d) ** 2 + 0.5 * (0.5 - d) ** 2) - 0.25,
    {'joint': pboth, 'independent': 0, 'minus-half': pboth - pf})
num(L3, 'p-clustered-fills', 2, VN(4), mix_var(4),
    {'independent': 4 * pf * (1 - pf), 'pairs-once': 1 + 6 * cv, 'carried': 1 + 12 * pboth})
num(L3, 'p-clustered-fills', 3, 12 * sqrt(VN(4)), sqrt(144 * mix_var(4)),
    {'no-square': sqrt(12 * VN(4)), 'independent': 12, 'variance': 144 * VN(4)}, round_tol=0.0005)
n_max = max(n for n in range(1, 40) if 144 * VN(n) <= 400)
n_alt2 = max(n for n in range(1, 12) if 144 * mix_var(n) <= 400 + 1e-9)
num(L3, 'p-clustered-fills', 4, n_max, n_alt2,
    {'independent': max(n for n in range(1, 40) if 144 * n * F(1, 4) <= 400),
     'pairs-once': max(n for n in range(1, 40) if 144 * (n * F(1, 4) + n * (n - 1) * cv / 2) <= 400)})
ok(VN(5) == F(225, 100) and VN(6) == 3 and isclose(12 * sqrt(3), 20.78, abs_tol=0.005), 'n = 5, 6 figures as stated')


# every numeric part: form stated, a value rounded as asked is accepted, each value the part's own feedback prints is accepted,
# and an "exact decimal" part has an answer that terminates
import re
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
def form_checks(sets):
    for ref, items in sets:
        if items is None: continue
        for iid, it in items.items():
            for k, p in enumerate(it['parts'], 1):
                w = p['widget']
                if w['kind'] != 'numeric': continue
                tag = f'{ref} {iid} p{k}'
                a, tol, q = w['answer'], w['tol'].get('abs', 0), p['question']
                scale = 100 if w.get('unit') == '%' else 1
                whole = float(a).is_integer() and tol == 0
                ok(whole or bool(re.search(r'\bGive\b', q)), f'{tag}: no sentence stating the form wanted')
                n = None
                m = re.search(r'(\d+) decimal places?|decimal to (\d+) places?', q)
                if m: n = int(m.group(1) or m.group(2))
                m = re.search(r'\b(one|two|three|four) decimal places?', q)
                if m: n = WORDS[m.group(1)]
                if 'nearest penny' in q: n = 2
                if 'nearest pound' in q: n = 0
                if n is not None:
                    r = round(a * scale, n) / scale
                    ok(abs(r - a) <= tol + 1e-9, f'{tag}: tolerance {tol} rejects the key rounded to {n} places ({r})')
                if 'exact decimal' in q:
                    ok(any(abs(a * scale * 10 ** j - round(a * scale * 10 ** j)) < 1e-9 for j in range(0, 5)), f'{tag}: the exact decimal does not end within 4 places')
                texts = [p['feedback'].get('correct', ''), p['explain']['text'], w.get('accept', '')]
                for t in texts:
                    t = t.replace('{,}', '').replace(',', '').replace('\u00a3', '')
                    for v in re.findall(r'(?:\\approx|about) \$?(-?\d+\.?\d*)', t):
                        v = float(v.rstrip('.'))
                        if a and not whole and abs(v - a * scale) <= 0.05 * abs(a * scale):
                            ok(abs(v / scale - a) <= tol + 1e-9, f'{tag}: prints {v} but the key {a} (tol {tol}) rejects it')
form_checks([('problems-1', L1), ('problems-2', L2), ('problems-3', L3)])

present = [n for n in (1, 2, 3) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
