"""Recompute every number in app/content/courses/validation/problems-<n>.json twice (docs/briefs/chained.md check 1).

Method 1 is exact where it can be (fractions, sympy, math.comb, the formula the lesson teaches). Method 2 takes another
route: a hypergeometric pmf from SciPy, NumPy on the raw fold scores, a brute count of fits by enumerating the loops,
a Monte Carlo draw, scikit-learn's TimeSeriesSplit on real index arrays, or a numerical integral for the mean best of
N normals. For each numeric part the script checks: the two methods agree; the key lies within its tol of them; every
`wrong` value matches its named slip, lies outside the key's band, and does not overlap another wrong; byKey covers the
wrongs. Choice parts check the keyed option and byKey. numbers_lib's Level.check_wrongs runs over each level too.
Exit 0 when all pass.

Run (from anywhere): <scratchpad>/venv/bin/python docs/reports/problems-validation-numbers.py
"""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as Fr

import numpy as np
import sympy as sp
from scipy import integrate, stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))
COURSE = os.path.join(ROOT, 'app', 'content', 'courses', 'validation')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

fails, checks = [], 0
rng = np.random.default_rng(20261116)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)
        print('BAD', msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf8') as f:
        d = json.load(f)
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'validation', f'problems-{n}: header')
    ok(3 <= len(d['items']) <= 5, f'problems-{n}: 3 to 5 items')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'problems-{n}: one item at difficulty 5')
    return {it['id']: it for it in d['items']}


def part(items, iid, k):
    return items[iid]['parts'][k - 1]


def num(items, iid, k, exact, alt, slips, agree=1e-9):
    """exact, alt: two computations of the key. slips: {wrong id: value the named slip gives}."""
    p = part(items, iid, k)
    w = p['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(math.isclose(e, a, rel_tol=agree, abs_tol=agree), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, 1e-9), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')
    ok(set(p['feedback'].get('byKey', {})) == set(wrongs), f'{tag}: byKey keys vs wrongs')
    return e


def printed(items, iid, k, value, places, pct=False):
    """The rounding the part asks for lies inside the key band (the tolerance accepts what the feedback prints)."""
    w = part(items, iid, k)['widget']
    r = round(float(value) * (100 if pct else 1), places) / (100 if pct else 1)
    ok(abs(r - w['answer']) <= w['tol']['abs'] + 1e-12, f'{iid} p{k}: printed rounding {r} outside the key band')
    txt = json.dumps(part(items, iid, k)['feedback']['correct'])
    s = f'{r * (100 if pct else 1):.{places}f}'
    ok(s in txt, f'{iid} p{k}: feedback does not print {s}')


def choice(items, iid, k, correct_id):
    p = part(items, iid, k)
    w = p['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')
    ok(set(p['feedback'].get('byKey', {})) == {o['id'] for o in w['options'] if not o.get('correct')}, f'{iid} p{k}: byKey keys')


def says(items, iid, text):
    ok(text in json.dumps(items[iid], ensure_ascii=False), f'{iid}: text {text!r} not found')


def emax_exact(n):
    """Mean of the largest of n standard normals, by numerical integration of x * n phi(x) Phi(x)^(n-1)."""
    return integrate.quad(lambda x: x * n * stats.norm.pdf(x) * stats.norm.cdf(x) ** (n - 1), -12, 12)[0]


def emax_mc(n, reps=400_000):
    return rng.standard_normal((reps, n)).max(axis=1).mean()


# ===================================================================== level 1
L1 = load(1)
if L1 is not None:
    # ---------- p-flood-claims ----------
    s2 = Fr(36, 100)
    n_exact = 2 * s2 ** 2 / Fr(3, 100) ** 2
    n_alt = next(n for n in range(1, 5000) if 0.36 * math.sqrt(2 / n) <= 0.03 + 1e-15)
    num(L1, 'p-flood-claims', 1, n_exact, n_alt, {'unsquared': 2 * s2 / Fr(3, 100) ** 2, 'no-two': s2 ** 2 / Fr(3, 100) ** 2})
    ok(s2 ** 2 == Fr(1296, 10000) and 2 * s2 ** 2 == Fr(2592, 10000), 'p-flood-claims: 0.1296 and 0.2592')
    rest = 1152 - 288
    num(L1, 'p-flood-claims', 2, Fr(3, 4) * rest, len(np.arange(rest)[: rest * 3 // 4]), {'validation': Fr(1, 4) * rest, 'all-rest': rest})
    num(L1, 'p-flood-claims', 3, 1152 - 1152 // 4, sum(1 for i in range(1152) if i % 4 != 0), {'test-fold': 1152 // 4, 'all': 1152})
    p1 = Fr(math.comb(864, 12), math.comb(1152, 12))
    p1_alt = stats.hypergeom(1152, 12, 288).pmf(0)
    num(L1, 'p-flood-claims', 4, p1, p1_alt, {'independent': Fr(3, 4) ** 12})
    prod = Fr(1)
    for i in range(12):
        prod *= Fr(864 - i, 1152 - i)
    ok(prod == p1, 'p-flood-claims p4: the product 864/1152 ... 853/1141 equals the binomial ratio')
    printed(L1, 'p-flood-claims', 4, p1, 4)
    p2 = Fr(math.comb(576, 12), math.comb(1152, 12))
    p3 = Fr(math.comb(288, 12), math.comb(1152, 12))
    some = 4 * p1 - 6 * p2 + 4 * p3
    # method 2: Monte Carlo over random fold assignments of the 12 flood claims
    pos =np.array([rng.choice(1152, 12, replace=False) for _ in range(60_000)]) // 288
    some_mc = np.mean([len(set(r)) < 4 for r in pos])
    ok(abs(float(some) - some_mc) < 0.006, f'p-flood-claims p5: Monte Carlo {some_mc} vs {float(some)}')
    ok(abs(float(p2) - 0.00023) < 0.000005 and float(p3) < 1e-6, 'p-flood-claims p5: pair chance about 0.00023, triple negligible')
    num(L1, 'p-flood-claims', 5, some, float(some), {
        'union': 4 * p1, 'independent-folds': 1 - (1 - p1) ** 4, 'carried': 4 * Fr(3, 4) ** 12 - 6 * Fr(23, 100000)})
    ok(abs(4 * 0.0311 - 6 * 0.00023 - 0.123) < 0.0005, 'p-flood-claims p5: the rounded working 4(0.0311) - 6(0.00023) gives 0.123')
    printed(L1, 'p-flood-claims', 5, some, 3)

    # ---------- p-van-prices ----------
    f = [Fr(x) for x in ('1.84', '2.11', '1.97', '2.26', '1.92')]
    fa = np.array([1.84, 2.11, 1.97, 2.26, 1.92])
    m = sum(f) / 5
    num(L1, 'p-van-prices', 1, m, fa.mean(), {'median': sorted(f)[2], 'by-four': sum(f) / 4})
    ss = sum((x - m) ** 2 for x in f)
    ok(ss == Fr('0.1106'), 'p-van-prices p2: squares add to 0.1106')
    sd = math.sqrt(ss / 5)
    num(L1, 'p-van-prices', 2, sd, fa.std(), {'ddof-one': fa.std(ddof=1), 'variance': fa.var()})
    printed(L1, 'p-van-prices', 2, sd, 3)
    lim = 2.02 + 0.149
    num(L1, 'p-van-prices', 3, lim, float(m) + round(fa.std(), 3), {'ddof-limit': 2.02 + fa.std(ddof=1), 'se': 2.02 + fa.std() / math.sqrt(5)})
    ok(round(2.02 + fa.std(), 3) == 2.169, 'p-van-prices p3: the unrounded sd gives 2.169 too')
    means = {0.3: 2.05, 1: 2.03, 3: 2.02, 10: 2.12, 30: 2.18, 100: 2.31}

    def one_se(limit):
        return max(a for a, v in means.items() if v <= limit + 1e-12)

    best = min(means, key=means.get)
    ok(best == 3, 'p-van-prices: alpha 3 has the lowest mean')
    pick_ = one_se(lim)
    pick_alt = sorted([a for a in means if means[a] - lim <= 1e-12])[-1]
    num(L1, 'p-van-prices', 4, pick_, pick_alt, {'best': best, 'carried': one_se(2.02 + fa.std(ddof=1))})
    ok(one_se(2.02 + fa.std() / math.sqrt(5)) == 3, 'p-van-prices p4: the sd/sqrt(5) slip also lands on alpha 3 (byKey best)')
    num(L1, 'p-van-prices', 5, sp.sqrt(sp.Rational(225, 100)) * 1000, math.sqrt(2.25) * 1000,
        {'mse-as-price': 2.25 * 1000, 'cv-mean': round(math.sqrt(2.12) * 1000, -1)})
    ok(1430 - 290 == 1140, 'p-van-prices: 1,140 training sales')

    # ---------- p-arrears-grid ----------
    G, K, Kin = 3 * 6, 4, 6
    fits_plain = Kin * G + 1
    enum_plain = sum(1 for _fold in range(Kin) for _s in range(G)) + 1
    num(L1, 'p-arrears-grid', 1, fits_plain, enum_plain, {'no-refit': Kin * G, 'one-knob': Kin * 6 + 1})
    enum_nested = sum(1 for _o in range(K) for _i in range(Kin) for _s in range(G)) + K
    num(L1, 'p-arrears-grid', 2, K * (Kin * G + 1), enum_nested, {'no-refits': K * Kin * G, 'added': K + fits_plain})
    outer_tr = Fr(3, 4) * 640
    inner_tr = Fr(5, 6) * outer_tr
    idx = np.arange(640)
    o_tr = idx[160:]
    i_tr = o_tr[80:]
    num(L1, 'p-arrears-grid', 3, inner_tr, len(i_tr), {'outer': outer_tr, 'all-inner': Fr(5, 6) * 640})
    gap = Fr('0.451') - Fr('0.412')
    num(L1, 'p-arrears-grid', 4, gap / Fr('0.451'), (0.451 - 0.412) / 0.451, {'by-inner': gap / Fr('0.412'), 'gap': gap})
    printed(L1, 'p-arrears-grid', 4, gap / Fr('0.451'), 1, pct=True)
    choice(L1, 'p-arrears-grid', 5, 'nested')
    says(L1, 'p-arrears-grid', '0.4315')
    ok((0.412 + 0.451) / 2 == 0.4315, 'p-arrears-grid p5: the average option is 0.4315')

    # ---------- p-rent-seeds ----------
    sd1 = 0.81 * math.sqrt(2 / 600)
    sd1_mc = (rng.normal(0, 0.9, (20000, 600)) ** 2).mean(axis=1).std()
    ok(abs(sd1 - sd1_mc) < 0.0015, f'p-rent-seeds p1: simulated sd {sd1_mc} vs {sd1}')
    num(L1, 'p-rent-seeds', 1, sd1, float(sp.Rational(81, 100) * sp.sqrt(sp.Rational(2, 600))),
        {'all-flats': 0.81 * math.sqrt(2 / 3000), 'sigma': 0.9 * math.sqrt(2 / 600), 'no-two': 0.81 / math.sqrt(600)})
    printed(L1, 'p-rent-seeds', 1, sd1, 4)
    e16 = emax_exact(16)
    ok(abs(e16 - 1.766) < 0.0005 and abs(emax_mc(16) - e16) < 0.01, f'p-rent-seeds: mean best of 16 normals {e16} is 1.766')
    best16 = 0.81 - 1.766 * 0.0468
    num(L1, 'p-rent-seeds', 2, best16, 0.81 - e16 * sd1, {'worst': 0.81 + 1.766 * 0.0468, 'carried': 0.81 - 1.766 * 0.0209}, agree=2e-4)
    printed(L1, 'p-rent-seeds', 2, best16, 3)
    share = (0.81 - 0.727) / 0.81
    num(L1, 'p-rent-seeds', 3, share, (0.81 - best16) / 0.81, {'by-best': (0.81 - 0.727) / 0.727, 'gap': 0.81 - 0.727}, agree=6e-4)
    printed(L1, 'p-rent-seeds', 3, share, 1, pct=True)
    need = math.ceil(2 * (1.766 / 0.04) ** 2)
    need_alt = next(n for n in range(1, 10000) if 1.766 * math.sqrt(2 / n) < 0.04)
    ok(math.ceil(2 * (e16 / 0.04) ** 2) == need, 'p-rent-seeds p4: the unrounded 1.76599 gives the same count')
    num(L1, 'p-rent-seeds', 4, need, need_alt, {'no-two': math.ceil((1.766 / 0.04) ** 2), 'unsquared': math.ceil(2 * 1.766 / 0.04)})
    ok(need > 3000 and 2 * (1.766 / 0.04) ** 2 - 3898.4 < 0.05, 'p-rent-seeds p4: 3,898.4 and more than the 3,000 flats')

    lv = Level('validation', 1)
    lv.check_wrongs('problems')
    bad = [r for r in lv.results if not r[0]]
    ok(not bad, f'level 1 check_wrongs: {bad}')


print(f'{checks - len(fails)} of {checks} checks passed')
if fails:
    sys.exit(1)
