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


# ===================================================================== level 2
L2 = load(2)
if L2 is not None:
    from sklearn.model_selection import TimeSeriesSplit

    def purged_train(n, s, e, h, b, first=0):
        """Rows first..first+n-1; test block s..e-1; drop h-1 before, h-1 after, then b more (l7's rule), clipped."""
        lo, hi = max(first, s - (h - 1)), min(first + n, e + (h - 1) + b)
        return [i for i in range(first, first + n) if i < lo or i >= hi]

    def overlaps(r, s, e, h):
        """Does training row r's label (days r+1..r+h) share a day with any test label (days s+1..e-1+h)?"""
        return max(r + 1, s + 1) <= min(r + h, e - 1 + h)

    # ---------- p-gas-demand ----------
    x = [Fr(v) for v in (2, 4, 8, 9, 10, 9)]
    xm = sum(x) / 6
    d = [v - xm for v in x]
    rho = sum(d[i] * d[i + 1] for i in range(5)) / sum(v * v for v in d)
    xa = np.array([2, 4, 8, 9, 10, 9.0])
    da = xa - xa.mean()
    num(L2, 'p-gas-demand', 1, rho, np.correlate(da, da, 'full')[6] / (da @ da),
        {'pearson': np.corrcoef(xa[:-1], xa[1:])[0, 1], 'averaged': (sum(d[i] * d[i + 1] for i in range(5)) / 5) / (sum(v * v for v in d) / 6)})
    ok(sum(d[i] * d[i + 1] for i in range(5)) == 26 and sum(v * v for v in d) == 52 and xm == 7, 'p-gas-demand p1: 26, 52 and mean 7')
    ok(abs(np.corrcoef(xa[:-1], xa[1:])[0, 1] - 0.869) < 0.0005, 'p-gas-demand p1: Pearson slip 0.869')
    folds = list(TimeSeriesSplit(n_splits=6).split(np.arange(1400)))
    num(L2, 'p-gas-demand', 2, 1400 - 1400 // 7, len(folds[-1][0]), {'block': len(folds[-1][1]), 'six-pieces': 1400 - 1400 // 6})
    ok(folds[0][1][0] == 200 and folds[-1][1][0] == 1200 and len(folds[0][0]) == 200, 'p-gas-demand p2: blocks start at 200 and 1,200; fold 1 trains on 200')
    mses = [Fr(v) for v in ('5.2', '4.6', '4.4', '4.9', '6.1', '5.6')]
    total = 200 * sum(mses) + 75 * Fr(8)
    ok(sum(mses) == Fr('30.8') and total == 6760, 'p-gas-demand p3: 30.8 and 6,760')
    errs = np.concatenate([np.full(200, float(v)) for v in mses] + [np.full(75, 8.0)])
    joined = total / 1275
    num(L2, 'p-gas-demand', 3, joined, errs.mean(), {'seven-mean': (sum(mses) + 8) / 7, 'six-only': sum(mses) / 6})
    printed(L2, 'p-gas-demand', 3, joined, 2)
    num(L2, 'p-gas-demand', 4, joined / Fr('2.12'), errs.mean() / 2.12,
        {'inverted': Fr('2.12') / Fr('5.30'), 'carried': (sum(mses) + 8) / 7 / Fr('2.12'), 'difference': Fr('5.30') - Fr('2.12')})
    printed(L2, 'p-gas-demand', 4, joined / Fr('2.12'), 2)

    # ---------- p-forward-label ----------
    h, look, n = 15, 30, 1260
    s, e = 560, 700                      # a middle block of 140 rows
    before = [r for r in range(0, s) if overlaps(r, s, e, h)]
    num(L2, 'p-forward-label', 1, h - 1, len(before), {'horizon': h, 'both-sides': 2 * (h - 1)})
    ok(before == list(range(s - 14, s)), 'p-forward-label p1: rows s-14 to s-1')
    after_feat = [r for r in range(e, n) if r - (look - 1) <= e - 1]
    num(L2, 'p-forward-label', 2, look - 1, len(after_feat), {'window': look, 'none': 0})
    keep = purged_train(n, s, e, h, look - 1)
    keep_alt = [r for r in range(n) if not (s <= r < e) and not overlaps(r, s, e, h)
                and not (e + (h - 1) <= r < e + (h - 1) + (look - 1))]
    num(L2, 'p-forward-label', 3, n - 140 - 2 * (h - 1) - (look - 1), len(keep),
        {'no-embargo': len(purged_train(n, s, e, h, 0)), 'horizon': len(purged_train(n, s, e, h + 1, look - 1)), 'block-only': n - 140})
    ok(keep == keep_alt, 'p-forward-label p3: purge by overlap test equals the l7 formula')
    ok(abs((140 + 57) / 1260 - 0.156) < 0.001, 'p-forward-label p3: nearly 16% out of each fold')
    tss = list(TimeSeriesSplit(n_splits=8, test_size=140, gap=14).split(np.arange(n)))
    num(L2, 'p-forward-label', 4, n - 8 * 140 - 14 - 1, tss[0][0][-1],
        {'no-gap': list(TimeSeriesSplit(n_splits=8, test_size=140).split(np.arange(n)))[0][0][-1],
         'horizon-gap': list(TimeSeriesSplit(n_splits=8, test_size=140, gap=15).split(np.arange(n)))[0][0][-1],
         'embargo': 125 - 29})
    num(L2, 'p-forward-label', 5, 140 + 7 * 140 - 14, len(tss[-1][0]),
        {'no-gap': 1120, 'embargo': len(tss[-1][0]) - 29, 'last-day': tss[-1][0][-1]})
    ok(tss[-1][1][0] == 1120 and len(tss[-1][0]) - len(keep) == 43, 'p-forward-label p5: fold 8 tests from 1,120; 43 more rows than part 3')

    # ---------- p-signal-break ----------
    hits = [Fr(v) for v in ('0.585', '0.565', '0.605', '0.575', '0.490', '0.470', '0.455')]
    tb = list(TimeSeriesSplit(n_splits=7).split(np.arange(1600)))
    ok(all(len(t) == 200 for _, t in tb) and tb[4][1][0] == 1000 and tb[5][1][0] == 1200, 'p-signal-break: blocks of 200; fold 5 from day 1,000, fold 6 from 1,200')
    se = math.sqrt(0.25 / 200)
    se_mc = rng.binomial(200, 0.5, 400_000).std() / 200
    num(L2, 'p-signal-break', 1, se, float(sp.sqrt(sp.Rational(1, 800))), {'variance': 0.00125, 'all-days': math.sqrt(0.25 / 1600)})
    ok(abs(se_mc - se) < 0.0005, f'p-signal-break p1: simulated {se_mc}')
    printed(L2, 'p-signal-break', 1, se, 4)
    z = (0.47 - 0.52) / 0.0354
    lvl = float(sum(hits[:4]) / 4)
    num(L2, 'p-signal-break', 2, round(z, 1), round((0.47 - 0.52) / se, 1),
        {'sign': -round(z, 1), 'earlier-level': round((0.47 - lvl) / se, 1), 'carried': round((0.47 - 0.52) / math.sqrt(0.25 / 1600), 1)})
    ok(lvl == 0.5825, 'p-signal-break p2: first four folds average 0.5825')

    def alarm(scores, base, k):
        run = 0
        for i, v in enumerate(scores, 1):
            run = run + 1 if v < base else 0
            if run == k:
                return i
        return None

    below = [i for i, v in enumerate(hits, 1) if v < Fr('0.52')]
    num(L2, 'p-signal-break', 3, alarm(hits, Fr('0.52'), 2), next(b for b in below if b - 1 in below), {'run-start': alarm(hits, Fr('0.52'), 1), 'seventh': 7})
    num(L2, 'p-signal-break', 4, sum(hits) / 7, np.mean([float(v) for v in hits]), {'first-four': sum(hits[:4]) / 4, 'last-three': sum(hits[4:]) / 3})
    ok(sum(hits) == Fr('3.745'), 'p-signal-break p4: the seven add to 3.745')
    printed(L2, 'p-signal-break', 4, sum(hits) / 7, 3)
    choice(L2, 'p-signal-break', 5, 'old-sign')
    ok(1600 - 1000 == 600, 'p-signal-break p5: 1,000 old days against 600 new')

    # ---------- p-spread-blocks ----------
    test = [3, 8, 11, 15, 19, 24]
    sand = [t for t in test if t - 1 >= 1 and t + 1 <= 24 and t - 1 not in test and t + 1 not in test]
    sand_alt = sum(1 for t in test if {t - 1, t + 1} <= (set(range(1, 25)) - set(test)))
    num(L2, 'p-spread-blocks', 1, len(sand), sand_alt, {'all': len(test)})
    blocks = [list(range(1 + 6 * j, 7 + 6 * j)) for j in range(4)]
    later = [dday for j in (0, 2, 3) for dday in blocks[j] if dday > 12]
    num(L2, 'p-spread-blocks', 2, 12, len(later), {'all-train': 18, 'one-fold': 6})
    tr = purged_train(24, 7, 13, 4, 2, first=1)
    tr_alt = [r for r in range(1, 25) if not (7 <= r <= 12) and not overlaps(r, 7, 13, 4) and r not in (16, 17)]
    num(L2, 'p-spread-blocks', 3, 24 - 6 - 3 - 3 - 2, len(tr),
        {'horizon': len(purged_train(24, 7, 13, 5, 2, first=1)), 'no-embargo': len(purged_train(24, 7, 13, 4, 0, first=1)), 'before-only': 24 - 6 - 3})
    ok(tr == tr_alt == [1, 2, 3] + list(range(18, 25)), 'p-spread-blocks p3: days 1 to 3 and 18 to 24')
    num(L2, 'p-spread-blocks', 4, Fr('4.62') / Fr('3.85') - 1, 4.62 / 3.85 - 1, {'by-purged': (4.62 - 3.85) / 4.62})
    printed(L2, 'p-spread-blocks', 4, Fr('4.62') / Fr('3.85') - 1, 1, pct=True)

    lv = Level('validation', 2)
    lv.check_wrongs('problems')
    bad = [r for r in lv.results if not r[0]]
    ok(not bad, f'level 2 check_wrongs: {bad}')


# ===================================================================== level 3
L3 = load(3)
if L3 is not None:
    import pandas as pd
    from sklearn.preprocessing import StandardScaler

    # ---------- p-fund-flows ----------
    fl = [14, 18, 16, 21, 19, 17, 22, 20, 15, 31, 27, 32]
    Xf = np.array(fl, float).reshape(-1, 1)
    num(L3, 'p-fund-flows', 1, Fr(sum(fl), 12), StandardScaler().fit(Xf).mean_[0], {'train': Fr(sum(fl[:9]), 9), 'test-mean': Fr(sum(fl[9:]), 3)})
    ok(sum(fl[:9]) == 162 and sum(fl[9:]) == 90 and sum(fl) == 252, 'p-fund-flows: 162, 90 and 252')
    num(L3, 'p-fund-flows', 2, Fr(sum(fl[:9]), 9), StandardScaler().fit(Xf[:9]).mean_[0], {'with-day-10': Fr(sum(fl[:10]), 10), 'twelve': Fr(sum(fl[:9]), 12)})
    fl2 = fl[:11] + [50]
    num(L3, 'p-fund-flows', 3, Fr(sum(fl2) - sum(fl), 12), StandardScaler().fit(np.array(fl2, float).reshape(-1, 1)).mean_[0] - 21,
        {'moved-value': 18, 'test-mean': Fr(18, 3), 'train': StandardScaler().fit(np.array(fl2[:9], float).reshape(-1, 1)).mean_[0] - 18})
    ok(Fr(sum(fl2), 12) == Fr(45, 2), 'p-fund-flows p3: the mean moves to 22.5')
    s_ = pd.Series(np.arange(1, 13, dtype=float), index=range(1, 13))
    win = s_.rolling(5, center=True).apply(lambda w: w.max(), raw=True)        # the last day each centred window reads
    used = [dd for dd in range(int(win[9]) - 4, int(win[9]) + 1) if dd >= 10]
    num(L3, 'p-fund-flows', 4, 2, len(used), {'all-test': 3, 'trailing': len([dd for dd in range(5, 10) if dd >= 10])})
    ok(int(win[9]) == 11, 'p-fund-flows p4: day 9 window ends on day 11')
    choice(L3, 'p-fund-flows', 5, 'log')
    ok(min(fl) > 0, 'p-fund-flows p5: every flow is positive, so the log exists')

    # ---------- p-fund-encoding ----------
    rho = 1 / sp.sqrt(49)
    sims = rng.standard_normal((200_000, 49))
    rho_mc = np.corrcoef(sims.mean(axis=1), sims[:, 0])[0, 1]
    num(L3, 'p-fund-encoding', 1, rho, rho_mc, {'one-over-n': sp.Rational(1, 49)}, agree=0.005)
    printed(L3, 'p-fund-encoding', 1, rho, 4)
    hit = 1 - sp.acos(rho) / sp.pi
    hit_alt = 0.5 + math.asin(1 / 7) / math.pi
    hit_mc = np.mean(np.sign(sims.mean(axis=1)) == np.sign(sims[:, 0]))
    ok(abs(hit_mc - float(hit)) < 0.004, f'p-fund-encoding p2: simulated sign agreement {hit_mc}')
    num(L3, 'p-fund-encoding', 2, hit, hit_alt, {'no-one': sp.acos(rho) / sp.pi, 'carried': 1 - math.acos(1 / 49) / math.pi})
    printed(L3, 'p-fund-encoding', 2, hit, 4)
    ok(abs(math.acos(1 / 7) - 1.4274) < 0.00005, 'p-fund-encoding p2: arccos(1/7) = 1.4274')
    se = math.sqrt(0.25 / 1200)
    t = (0.5456 - 0.5) / se
    num(L3, 'p-fund-encoding', 3, round(t, 2), round((float(hit) - 0.5) / se, 2),
        {'carried': round((0.4544 - 0.5) / se, 2), 'months': round((0.5456 - 0.5) / math.sqrt(0.25 / 49), 2)})
    ok(abs(se - 0.01443) < 0.000005, 'p-fund-encoding p3: se 0.01443')
    bar40 = stats.norm.ppf(1 - 0.05 / 40)
    ok(round(bar40, 2) == 3.02 and t > bar40, f'p-fund-encoding p4: Bonferroni bar {bar40} and t clears it')
    ok(round(stats.norm.ppf(0.95), 2) == 1.64, 'p-fund-encoding p4: one try gives about 1.64')
    choice(L3, 'p-fund-encoding', 4, 'leak')

    # ---------- p-closed-funds ----------
    over = Fr(26, 100) * Fr(65, 1000)
    # method 2: a panel of 100 funds, 26 closed, survivors at r, closed at r - 6.5 points: mean of all vs survivors
    r_s = 0.08
    panel = np.r_[np.full(74, r_s), np.full(26, r_s - 0.065)]
    num(L3, 'p-closed-funds', 1, over, r_s - panel.mean(), {'gap': Fr(65, 1000), 'survivor-share': Fr(74, 100) * Fr(65, 1000)})
    printed(L3, 'p-closed-funds', 1, over, 2, pct=True)
    honest = (Fr('7.4') - Fr('1.69')) / 12
    num(L3, 'p-closed-funds', 2, honest, (0.074 - float(over)) / 0.12,
        {'survivors': Fr('7.4') / 12, 'added': (Fr('7.4') + Fr('1.69')) / 12, 'carried': (Fr('7.4') - Fr('4.81')) / 12})
    printed(L3, 'p-closed-funds', 2, honest, 3)
    for nn, v in ((4, 1.03), (18, 1.82), (22, 1.91)):
        ex = emax_exact(nn)
        ok(round(ex, 2) == v and abs(emax_mc(nn, 200_000) - ex) < 0.01, f'p-closed-funds p3: mean best of {nn} is {ex}')
    noise = 1.82 / 3
    num(L3, 'p-closed-funds', 3, noise, emax_exact(18) / math.sqrt(9), {'wiki': 1.03 / 3, 'double-count': 1.91 / 3, 'by-years': 1.82 / 9}, agree=5e-4)
    printed(L3, 'p-closed-funds', 3, noise, 3)
    hc = round(0.476 - 0.607, 2)
    num(L3, 'p-closed-funds', 4, hc, round(float(honest) - emax_exact(18) / 3, 2),
        {'wiki': round(0.476 - 0.343, 2), 'clipped': 0, 'survivors': round(0.617 - 0.607, 2)})

    # ---------- p-carry-lookbacks ----------
    ceil_ = math.sqrt(2 * math.log(60)) / 2
    num(L3, 'p-carry-lookbacks', 1, ceil_, float(sp.sqrt(2 * sp.log(60)) / 2),
        {'no-root-t': round(math.sqrt(2 * math.log(60)), 2), 'by-years': round(math.sqrt(2 * math.log(60)) / 4, 2), 'wiki': round(math.sqrt(2 * math.log(9)) / 2, 2)})
    printed(L3, 'p-carry-lookbacks', 1, ceil_, 2)
    e60 = emax_exact(60)
    ok(round(e60, 3) == 2.319 and abs(emax_mc(60, 100_000) - e60) < 0.01, f'p-carry-lookbacks p2: mean best of 60 is {e60}')
    keep = 1.48 - 2.319 / 2
    num(L3, 'p-carry-lookbacks', 2, keep, 1.48 - e60 / 2, {'ceiling': round(1.48 - 1.43, 2), 'no-root': round(1.48 - 2.319, 2)}, agree=5e-4)
    printed(L3, 'p-carry-lookbacks', 2, keep, 2)
    corr = math.sqrt(0.2) * 1.16
    z0 = rng.standard_normal((100_000, 1))
    zi = rng.standard_normal((100_000, 60))
    corr_mc = ((math.sqrt(0.8) * z0 + math.sqrt(0.2) * zi) / 2).max(axis=1).mean()
    ok(abs(corr_mc - math.sqrt(0.2) * e60 / 2) < 0.01, f'p-carry-lookbacks p3: simulated correlated best {corr_mc}')
    num(L3, 'p-carry-lookbacks', 3, corr, math.sqrt(0.2) * e60 / 2, {'rho': round(math.sqrt(0.8) * 1.16, 2), 'no-root': round(0.2 * 1.16, 2)}, agree=5e-4)
    printed(L3, 'p-carry-lookbacks', 3, corr, 2)
    ok(round(1.48 - 0.52, 2) == 0.96, 'p-carry-lookbacks p3 and p5: 1.48 - 0.52 = 0.96')
    bar60 = stats.norm.ppf(1 - 0.05 / 60)
    ok(round(bar60, 2) == 3.14, f'p-carry-lookbacks p4: Bonferroni bar for 60 is {bar60}')
    num(L3, 'p-carry-lookbacks', 4, 3.14 / 2, round(bar60, 2) / math.sqrt(4), {'bar': 3.14, 'by-years': round(3.14 / 4, 2)})
    ok(1.48 * 2 < 3.14 and abs(1.48 * 2 - 2.96) < 1e-12, 'p-carry-lookbacks p4: t = 2.96 falls short of 3.14')
    choice(L3, 'p-carry-lookbacks', 5, 'locked')

    lv = Level('validation', 3)
    lv.check_wrongs('problems')
    bad = [r for r in lv.results if not r[0]]
    ok(not bad, f'level 3 check_wrongs: {bad}')


print(f'{checks - len(fails)} of {checks} checks passed')
if fails:
    sys.exit(1)
