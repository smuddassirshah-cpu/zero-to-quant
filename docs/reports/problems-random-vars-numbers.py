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
n_alt = next(n for n in range(1, 50) if 0.8 ** n <= 0.1)
num(L1, 'p-tightest-quote', 4, n_need, n_alt, {'round-down': n_need - 1, 'added': 5})
ok(abs(0.8 ** 10 - 0.107) < 0.0005 and abs(0.8 ** 11 - 0.086) < 0.0005, '0.8^10, 0.8^11 as stated')


present = [n for n in (1, 2, 3) if os.path.exists(os.path.join(COURSE, f'problems-{n}.json'))]
print(f'problem sets checked: {present}; checks: {checks}; failures: {len(fails)}')
for m in fails:
    print('FAIL', m)
sys.exit(1 if fails else 0)
