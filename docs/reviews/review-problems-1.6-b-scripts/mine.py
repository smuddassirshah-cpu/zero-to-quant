"""Second read, testing problems-1 to -3: the reader's own keys, slips and stated numbers.

Nothing is imported from the author's script. Each key is worked from the item's text (the numbers below are typed from
the prose, not read from the file's answers), by SciPy or exact fractions, and then compared with the stored answer,
each stored `wrong` value and the numbers the feedback and explanations print.

Usage (repo root): <venv>/bin/python docs/reviews/review-problems-1.6-b-scripts/mine.py [-v]"""
import json
import sys
from fractions import Fraction as F
from math import comb, sqrt

import numpy as np
from scipy import stats

V = '-v' in sys.argv
N = stats.norm
checks = fails = 0
notes = []


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)
    elif V:
        print('ok  ', msg)


def near(a, b, tol, msg):
    ok(abs(a - b) <= tol + 1e-12, f'{msg}: mine {a:.7g}, stored or stated {b:.7g}, tol {tol}')


SETS = {n: json.load(open(f'app/content/courses/testing/problems-{n}.json')) for n in (1, 2, 3)}


def part(n, item, k):
    it = next(i for i in SETS[n]['items'] if i['id'] == item)
    return it['parts'][k - 1]


def key(n, item, k, mine, wrongs=None, places=None):
    """mine: my value of the answer; wrongs: {id: my value of that slip}; places: the rounding the question asks."""
    w = part(n, item, k)['widget']
    tol = w['tol']['abs']
    near(mine, w['answer'], tol, f'problems-{n} {item} {k} answer')
    if places is not None:
        ok(abs(round(mine, places) - w['answer']) <= tol + 1e-12, f'problems-{n} {item} {k}: my value rounded to {places} places is accepted')
    stored = {x['id']: x for x in w.get('wrong', [])}
    for wid, val in (wrongs or {}).items():
        ok(wid in stored, f'problems-{n} {item} {k}: wrong id {wid} exists')
        if wid in stored:
            near(val, stored[wid]['value'], stored[wid]['tol']['abs'], f'problems-{n} {item} {k} wrong {wid}')
    ok(set(stored) == set(wrongs or {}), f'problems-{n} {item} {k}: every stored wrong re-derived ({sorted(set(stored) ^ set(wrongs or {}))})')
    vals = sorted([(w['answer'], tol, 'answer')] + [(x['value'], x['tol']['abs'], x['id']) for x in stored.values()])
    for (a, ta, ia), (b, tb, ib) in zip(vals, vals[1:]):
        ok(a + ta < b - tb, f'problems-{n} {item} {k}: bands of {ia} and {ib} do not touch')


def choice(n, item, k, right):
    w = part(n, item, k)['widget']
    got = [o['id'] for o in w['options'] if o.get('correct')]
    ok(got == [right], f'problems-{n} {item} {k}: correct option {got} is {right}')


# ---------------- problems-1 ----------------
# cereal: label 750, sd 18, n 36, mean 743.1, alpha 0.01
se = 18 / sqrt(36)
z = (743.1 - 750) / se
choice(1, 'p-cereal-boxes', 1, 'label-lower')
key(1, 'p-cereal-boxes', 2, se, {'over-n': 18 / 36, 'variance': 18 ** 2 / 36})
key(1, 'p-cereal-boxes', 3, z, {'sign': -z, 'over-sd': -6.9 / 18, 'carried': -6.9 / 0.5})
key(1, 'p-cereal-boxes', 4, N.cdf(z), {'upper-tail': N.cdf(-z), 'two-sided': 2 * N.cdf(z)}, 4)
near(N.cdf(2.3), 0.9893, 5e-5, 'cereal: Phi(2.3) as told')
near(1 / 0.0107, 93, 0.5, 'cereal: "about one time in 93"')
ok(N.cdf(z) > 0.01, 'cereal: p above 0.01, so fail to reject')
choice(1, 'p-cereal-boxes', 5, 'fail')

# phone: 8 lives, advert 19.5
x = np.array([15, 19, 20, 17, 18, 16, 21, 18])
m, s = x.mean(), x.std(ddof=1)
ok(x.sum() == 144, 'phone: total 144')
ok(list(x - 18) == [-3, 1, 2, -1, 0, -2, 3, 0] and ((x - 18) ** 2).sum() == 28, 'phone: deviations and 28')
key(1, 'p-phone-battery', 1, m, {'n-minus-one': 144 / 7})
key(1, 'p-phone-battery', 2, s, {'divide-by-n': x.std(), 'variance': s ** 2, 'carried': sqrt(((x - 144 / 7) ** 2).sum() / 7)})
t = (m - 19.5) / (s / sqrt(8))
near(t, stats.ttest_1samp(x, 19.5).statistic, 1e-12, 'phone: t against scipy ttest_1samp')
key(1, 'p-phone-battery', 3, t, {'root-seven': -1.5 / (2 / sqrt(7)), 'over-s': -1.5 / 2, 'sign': -t, 'carried': -1.5 / (x.std() / sqrt(8))}, 3)
near(2 / sqrt(8), 0.7071, 5e-5, 'phone: se 0.7071')
near(stats.t.ppf(0.95, 7), 1.895, 5e-4, 'phone: t7 one-sided 5% cut-off')
near(stats.t.ppf(0.975, 7), 2.365, 5e-4, 'phone: t7 two-sided 5% cut-off')
near(N.ppf(0.95), 1.645, 5e-4, 'normal one-sided 5% cut-off')
choice(1, 'p-phone-battery', 4, 'one-sided-t7')
b = 18 + 1.895 * 0.7071
key(1, 'p-phone-battery', 5, b, {'normal': 18 + 1.645 * 0.7071, 'two-sided': 18 + 2.365 * 0.7071, 'wrong-side': 18 - 1.895 * 0.7071,
                                'sd-not-se': 18 + 1.895 * 2}, 2)
near(18 + stats.t.ppf(0.95, 7) * 2 / sqrt(8), 19.34, 0.005, 'phone: boundary with unrounded cut-off and se')
near(19.5 - 19.34, 0.16, 1e-9, 'phone: "0.16 hours inside"')

# wine: 12 trials, guessing
tail = lambda k: F(sum(comb(12, j) for j in range(k, 13)), 4096)
ok(2 ** 12 == 4096 and comb(12, 11) == 12 and comb(12, 10) == 66 and comb(12, 9) == 220, 'wine: counts')
ok(tail(11) == F(13, 4096) and tail(10) == F(79, 4096) and tail(9) == F(299, 4096), 'wine: 13, 79, 299 of 4096')
near(float(tail(11)), stats.binom.sf(10, 12, 0.5), 1e-12, 'wine: tail against scipy binom')
key(1, 'p-wine-taster', 1, float(tail(11)), {'eleven-only': 12 / 4096, 'twelve-only': 1 / 4096}, 4)
key(1, 'p-wine-taster', 2, float(tail(10)), {'exactly-ten': 66 / 4096, 'carried': 78 / 4096}, 4)
key(1, 'p-wine-taster', 3, float(tail(9)), {'exactly-nine': 220 / 4096, 'carried': (66 + 220) / 4096}, 4)
near(0.0193 + 0.0537, 0.0730, 1e-9, 'wine 3: the route the question sets, from rounded values')
near(0.0161 + 0.0537, 0.0698, 1e-9, 'wine 3: carried slip from rounded values')
kmin = min(k for k in range(13) if tail(k) <= F(1, 20))
key(1, 'p-wine-taster', 4, kmin, {'nine': 9, 'eleven': 11})
ok(tail(11) <= F(1, 100) < tail(10), 'wine: 11 is the 1% count')

# pizza: promise 30, n 16, mean 33.5, sigma 8, s 9.6
z = 3.5 / (8 / 4)
key(1, 'p-pizza-delivery', 1, z, {'over-sd': 3.5 / 8, 'over-n': 3.5 / (8 / 16), 'no-null': 33.5 / 2}, 2)
key(1, 'p-pizza-delivery', 2, N.sf(z), {'two-sided': 2 * (1 - 0.9599), 'lower-tail': N.cdf(z)}, 4)
notes.append(f'pizza 2: the doubled tail is 0.0802 from the told 0.9599 and {2 * N.sf(z):.5f} unrounded, which types as 0.0801 and misses the two-sided line')
near(N.cdf(1.75), 0.9599, 5e-5, 'pizza: Phi(1.75) as told')
tt = 3.5 / (9.6 / 4)
near(tt, 1.75 * 8 / 9.6, 1e-12, 'pizza: rescaled z equals t')
key(1, 'p-pizza-delivery', 3, tt, {'flipped': 1.75 * 9.6 / 8, 'over-s': 3.5 / 9.6}, 3)
near(stats.t.ppf(0.95, 15), 1.753, 5e-4, 'pizza: t15 one-sided 5% cut-off')
ok(tt < 1.753 and N.sf(z) < 0.05, 'pizza: t fails, z rejects')
choice(1, 'p-pizza-delivery', 4, 't-fails')

# ---------------- problems-2 ----------------
# fertiliser: sd 1.2, n 36, cut 1.645, gain 0.45
c = 0.45 / (1.2 / 6)
key(2, 'p-fertiliser-trials', 1, c, {'over-sd': 0.45 / 1.2, 'over-n': 0.45 / (1.2 / 36)}, 2)
pw = N.cdf(c - 1.645)
near(N.cdf(0.605), 0.7274, 5e-5, 'fertiliser: Phi(0.605) as told')
key(2, 'p-fertiliser-trials', 2, pw, {'beta': 1 - pw, 'alpha': 0.05}, 4)
key(2, 'p-fertiliser-trials', 3, 1 - (1 - 0.7274) ** 2, {'both': 0.7274 ** 2, 'added': 2 * 0.7274, 'carried': 1 - 0.7274 ** 2}, 4)
near(0.2726 ** 2, 0.0743, 5e-5, 'fertiliser: 0.2726 squared')
c2 = c * sqrt(2)
near(c2, 3.182, 5e-4, 'fertiliser: 2.25 root 2')
near(c2 - 1.645, 1.537, 5e-4, 'fertiliser: 1.537 past the cut-off')
near(N.cdf(1.537), 0.9379, 5e-5, 'fertiliser: Phi(1.537) as told')
notes.append(f'fertiliser 4: Phi(1.537) = {N.cdf(1.537):.6f}, Phi(2.25 root 2 - 1.645) = {N.cdf(c2 - 1.645):.6f}, with z_0.05 unrounded {N.cdf(c2 - N.ppf(0.95)):.6f}')
key(2, 'p-fertiliser-trials', 4, N.cdf(1.537), {'beta': 1 - N.cdf(1.537), 'unchanged': 0.7274}, 4)
near(1 - 0.95 ** 2, 0.0975, 1e-12, 'fertiliser: alpha of the either rule')
ok(0.9379 > 0.9257 and 0.05 < 0.0975, 'fertiliser: one large trial wins on both')
choice(2, 'p-fertiliser-trials', 5, 'one-big')

# tyres: A 50 cars 3.2 sd 0.9; B 40 cars 2.8 sd 0.6
va, vb = 0.9 ** 2 / 50, 0.6 ** 2 / 40
se = sqrt(va + vb)
key(2, 'p-tyre-brands', 1, se, {'sum-se': sqrt(va) + sqrt(vb), 'variance': va + vb, 'same-n': sqrt(0.81 / 50 + 0.36 / 50)}, 4)
near(sqrt(va), 0.1273, 5e-5, 'tyres: 0.1273'); near(sqrt(vb), 0.0949, 5e-5, 'tyres: 0.0949')
res = stats.ttest_ind_from_stats(3.2, 0.9, 50, 2.8, 0.6, 40, equal_var=False)
near(0.4 / se, res.statistic, 1e-12, 'tyres: Welch t against scipy')
key(2, 'p-tyre-brands', 2, 0.4 / se, {'carried': 0.4 / 0.2221, 'over-variance': 0.4 / 0.0252}, 3)
near(0.4 / 0.1587, part(2, 'p-tyre-brands', 2)['widget']['answer'], 0.001, 'tyres 2: the value from the rounded se the question hands over')
near(N.cdf(2.52), 0.9941, 5e-5, 'tyres: Phi(2.52) as told')
key(2, 'p-tyre-brands', 3, 2 * (1 - 0.9941), {'one-sided': 1 - 0.9941, 'inside': 1 - 2 * (1 - 0.9941)}, 4)
near(2 * N.sf(0.4 / se), 0.0118, 1e-4, 'tyres 3: p from the unrounded t')
wdf = (va + vb) ** 2 / (va ** 2 / 49 + vb ** 2 / 39)
notes.append(f'tyres: Welch df {wdf:.1f}, exact Welch p {res.pvalue:.5f} against the normal 0.0118')
choice(2, 'p-tyre-brands', 4, 'right')

# shoes: nine paired differences
d = np.array([-7, -3, -9, -1, -4, -5, 1, -3, -5])
ok(d.sum() == -36 and list(d + 4) == [-3, 1, -5, 3, 0, -1, 5, 1, -1] and ((d + 4) ** 2).sum() == 72, 'shoes: total, deviations, 72')
key(2, 'p-running-shoes', 1, d.mean(), {'n-minus-one': -36 / 8, 'sign': 4})
key(2, 'p-running-shoes', 2, d.std(ddof=1), {'divide-by-n': d.std(), 'variance': 9, 'carried': sqrt(((d + 4.5) ** 2).sum() / 8)})
tp = d.mean() / (d.std(ddof=1) / 3)
near(tp, stats.ttest_1samp(d, 0).statistic, 1e-12, 'shoes: paired t against scipy')
key(2, 'p-running-shoes', 3, tp, {'over-sd': -4 / 3, 'root-eight': -4 / (3 / sqrt(8)), 'carried': -4 / (d.std() / 3), 'sign': 4})
near(stats.t.ppf(0.95, 8), 1.860, 5e-4, 'shoes: t8 one-sided 5% cut-off')
choice(2, 'p-running-shoes', 4, 'paired')
near((N.ppf(0.95) + N.ppf(0.8)) ** 2, 6.18, 0.005, 'shoes: 6.18 is (z_alpha + z_beta) squared')
n_raw = 6.18 * (3 / 1.5) ** 2
key(2, 'p-running-shoes', 5, int(np.ceil(n_raw)), {'not-rounded': n_raw, 'rounded-down': 24, 'no-square': 6.18 * 2, 'carried': 6.18 * (d.std() / 1.5) ** 2})
ok(N.cdf(0.5 * sqrt(24) - 1.645) < 0.8 < N.cdf(0.5 * sqrt(25) - 1.645), 'shoes: 24 falls short, 25 passes, on the z formula')
nct = lambda n: stats.nct.sf(stats.t.ppf(0.95, n - 1), n - 1, 0.5 * sqrt(n))
notes.append(f'shoes 5: power of the paired t test (noncentral t) at n = 25 is {nct(25):.4f}, at 26 {nct(26):.4f}, at 27 {nct(27):.4f}; the z formula gives {N.cdf(2.5 - 1.645):.4f} at 25')

# blood: healthy N(50, 10), disease N(72, 10), flag above 68, prevalence 2%
a = N.sf((68 - 50) / 10)
bt = N.cdf((68 - 72) / 10)
key(2, 'p-blood-screen', 1, a, {'lower': 1 - a, 'two-tail': 2 * (1 - 0.9641), 'disease-curve': 1 - bt}, 4)
key(2, 'p-blood-screen', 2, bt, {'power': 1 - bt, 'healthy-curve': 1 - a}, 4)
near(N.cdf(1.8), 0.9641, 5e-5, 'blood: Phi(1.8) as told'); near(N.cdf(0.4), 0.6554, 5e-5, 'blood: Phi(0.4) as told')
fl = 9800 * 0.0359 + 200 * (1 - 0.3446)
near(9800 * 0.0359, 351.8, 0.05, 'blood: 351.8'); near(200 * 0.6554, 131.1, 0.05, 'blood: 131.1')
key(2, 'p-blood-screen', 3, fl, {'true-only': 200 * 0.6554, 'false-only': 9800 * 0.0359, 'beta-not-power': 9800 * 0.0359 + 200 * 0.3446}, 0)
near(9800 * a + 200 * (1 - bt), 483, 0.5, 'blood 3: flags from unrounded alpha and beta')
key(2, 'p-blood-screen', 4, 131.1 / 483, {'flipped': 1 - 131.1 / 483, 'power': 0.6554, 'carried': 200 * 0.3446 / (9800 * 0.0359 + 200 * 0.3446)}, 2)
near(0.02 * (1 - bt) / (0.02 * (1 - bt) + 0.98 * a), 0.27, 0.005, 'blood 4: Bayes with unrounded rates')
choice(2, 'p-blood-screen', 5, 'right')
notes.append(f'doubled-tail slips from unrounded tails: blood 1 {2 * a:.5f} (stored 0.0718), funds 2 {2 * N.sf(2.7):.5f} (stored 0.007); each types to 4 places outside its band')

# ---------------- problems-3 ----------------
# genes: 40 tests, eight smallest p-values
ps = [0.0004, 0.0011, 0.0019, 0.0052, 0.0060, 0.0081, 0.0150, 0.031]
key(3, 'p-gene-screen', 1, 1 - 0.95 ** 40, {'expected': 40 * 0.05, 'no-complement': 0.95 ** 40, 'single': 0.05}, 4)
key(3, 'p-gene-screen', 2, 1 - (1 - 0.05 / 40) ** 40, {'bound': 0.05, 'no-complement': (1 - 0.05 / 40) ** 40, 'carried': 1 - 0.95 ** 40}, 4)


def bh(p, m, q):
    p = sorted(p)
    passing = [k for k in range(1, len(p) + 1) if p[k - 1] <= q * k / m]
    return (max(passing) if passing else 0), passing


kb, passing = bh(ps, 40, 0.05)
ok(passing == [1, 2, 3, 5], 'genes: ranks under their bars are 1, 2, 3 and 5')
key(3, 'p-gene-screen', 3, sum(p <= 0.05 / 40 for p in ps), {'unadjusted': sum(p <= 0.05 for p in ps), 'bh': kb})
key(3, 'p-gene-screen', 4, kb, {'first-fail': 3, 'bonferroni': 2, 'unadjusted': 8})
from statsmodels.stats.multitest import multipletests
full = ps + [0.06 + 0.02 * i for i in range(32)]
ok(multipletests(full, 0.05, 'fdr_bh')[0].sum() == 5 and multipletests(full, 0.05, 'bonferroni')[0].sum() == 2, 'genes: statsmodels BH 5, Bonferroni 2')
choice(3, 'p-gene-screen', 5, 'right')

# fund managers: SR 0.9 over 9 years, 8 managers, q 0.10
t = 0.9 * sqrt(9)
key(3, 'p-fund-managers', 1, t, {'over-root': 0.9 / 3, 'times-t': 0.9 * 9})
near(N.cdf(2.7), 0.9965, 5e-5, 'funds: Phi(2.7) as told')
key(3, 'p-fund-managers', 2, N.sf(t), {'two-sided': 2 * (1 - 0.9965), 'lower': N.cdf(t)}, 4)
others = [0.0006, 0.014, 0.052, 0.058, 0.09, 0.31, 0.62]
k8, passing = bh(others + [0.0035], 8, 0.10)
ok(passing == [1, 2, 3, 5] and sorted(others + [0.0035])[1] == 0.0035, 'funds: ranks 1, 2, 3, 5 pass; H sorts second')
key(3, 'p-fund-managers', 3, k8, {'first-fail': 3, 'bonferroni': sum(p <= 0.10 / 8 for p in others + [0.0035]), 'unadjusted': sum(p <= 0.10 for p in others + [0.0035])})
ok(bh(others + [0.9965], 8, 0.10)[0] == 2, 'funds: with p taken as 0.9965 BH gives 2, as the line says')
ok(bh(others + [0.007], 8, 0.10)[0] == 5, 'funds: with the doubled p 0.007 BH still gives 5')

# checkout: 25 pages, best p 0.004
key(3, 'p-checkout-designs', 1, 1 - 0.996 ** 25, {'single': 0.004, 'bonferroni': 25 * 0.004, 'no-complement': 0.996 ** 25}, 4)
sid = 1 - 0.95 ** (1 / 25)
key(3, 'p-checkout-designs', 2, sid, {'bonferroni': 0.05 / 25, 'no-root': 0.05, 'power-25': 1 - 0.95 ** 25}, 6)
near(0.95 ** (1 / 25), 0.997950, 5e-7, 'checkout: 0.95 to the 1/25')
near(0.004 / sid, 2, 0.06, 'checkout: 0.004 is about twice the threshold')
notes.append(f'checkout 2: threshold {sid:.9f}; the rounded 0.002050 gives a family chance of {1 - (1 - 0.00205) ** 25:.6f}')
choice(3, 'p-checkout-designs', 3, 'holdout')
key(3, 'p-checkout-designs', 4, 1 - 0.97 ** 25, {'single': 0.03, 'bonferroni': 25 * 0.03, 'no-complement': 0.97 ** 25}, 4)

# biomarkers: 380 nulls, 20 real; power 0.9 at 2, 0.6 at 3
near(2 * N.sf(2), 0.0455, 5e-5, 'biomarkers: P(|Z| > 2)'); near(2 * N.sf(3), 0.0027, 5e-5, 'biomarkers: P(|Z| > 3)')
f2, f3 = 380 * 0.0455, 380 * 0.0027
key(3, 'p-biomarker-field', 1, f2, {'all-400': 400 * 0.0455, 'one-sided': 380 * 0.0455 / 2}, 2)
key(3, 'p-biomarker-field', 2, f2 / (f2 + 18), {'true-share': 18 / (f2 + 18), 'over-400': f2 / 400, 'no-power': f2 / (f2 + 20)}, 3)
key(3, 'p-biomarker-field', 3, f3, {'all-400': 400 * 0.0027, 'old-bar': f2}, 3)
key(3, 'p-biomarker-field', 4, f3 / (f3 + 12), {'old-power': f3 / (f3 + 18), 'true-share': 12 / (f3 + 12), 'carried': 1.08 / 13.08}, 3)
near(f2 / f3, 17, 0.5, 'biomarkers: "a factor of about 17"')
near(1 - 0.9973 ** 380, 0.64, 0.005, 'biomarkers: chance of any false find at the bar of 3, about 0.64 (needs independence)')
# a real biomarker with one shift: is 0.9 at 2 consistent with 0.6 at 3?
from scipy.optimize import brentq
mu = brentq(lambda u: N.sf(2 - u) + N.cdf(-2 - u) - 0.9, 0, 10)
notes.append(f'biomarkers: a shift of {mu:.3f} gives power 0.9 at the bar of 2 and {N.sf(3 - mu) + N.cdf(-3 - mu):.3f} at 3 (the prose says 0.6)')
choice(3, 'p-biomarker-field', 5, 'trade')

# ---------------- shape of each set ----------------
for n, d in SETS.items():
    parts = [p for it in d['items'] for p in it['parts']]
    typed = sum(p['widget']['kind'] != 'choice' for p in parts)
    ok(3 * typed >= 2 * len(parts), f'problems-{n}: typed {typed} of {len(parts)} parts, at least two thirds')
    ok(any(it['difficulty'] == 5 for it in d['items']) and all(3 <= it['difficulty'] <= 5 for it in d['items']), f'problems-{n}: difficulties 3 to 5 with a 5')
    ok(all(3 <= len(it['parts']) <= 5 for it in d['items']) and 3 <= len(d['items']) <= 5, f'problems-{n}: 3 to 5 items of 3 to 5 parts')
    for it in d['items']:
        for k, p in enumerate(it['parts'], 1):
            w = p['widget']
            by = p['feedback'].get('byKey', {})
            ids = [x['id'] for x in w.get('wrong', [])] + [o['id'] for o in w.get('options', []) if not o.get('correct')]
            ok(set(ids) == set(by), f'problems-{n} {it["id"]} {k}: byKey lines match the wrong ids')
            ok(p['explain']['text'].count('. ') + 1 <= 4, f'problems-{n} {it["id"]} {k}: explanation length')
    print(f'problems-{n}: {len(d["items"])} problems, {len(parts)} parts, {typed} typed')

for s in notes:
    print('note:', s)
print(f'mine.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
