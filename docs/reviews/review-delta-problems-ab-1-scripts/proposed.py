#!/usr/bin/env python3
"""Delta read of the problems fix passes: the numbers of every fix proposed in review-delta-problems-ab-1.md, each by
   two routes. Run from the repo root with the scratchpad venv python. Exit 0."""
import math, sys
from fractions import Fraction as Fr
import numpy as np

n = f = 0


def ok(c, msg):
    global n, f
    n += 1
    if not c:
        f += 1
    print(('ok      ' if c else 'FAIL    ') + msg)


def bh(ps, q):
    ps = sorted(ps); m = len(ps)
    ks = [k for k, p in enumerate(ps, 1) if p <= k * q / m + 1e-15]
    return max(ks) if ks else 0


def bh_frac(ps, q):                      # second route: exact fractions, scanning down from the top rank
    ps = sorted(Fr(str(p)) for p in ps); m = len(ps); q = Fr(str(q))
    for k in range(m, 0, -1):
        if ps[k - 1] <= k * q / m:
            return k
    return 0


# finding 1: the decimal lines (vectors). The line proposed names no number; here are the slips that land in each band.
for name, typed in (('active-bets 2', (-0.0055, -0.0095, -0.0145, -0.01)), ('stress-hedge 3', (-0.0146, -0.008, -0.0066)), ('stress-hedge 4', (-0.0073, -0.0146, -0.008))):
    ok(all(abs(t / 100 + 0.0001) <= 0.000049 for t in typed), f'{name}: {typed} all land in the band -0.0001 +- 0.000049')
ok(all(abs(t / 100 - 0.008) <= 0.0005 for t in (0.803, 0.76, 0.84, 0.8)), 'factor-risk 5: 0.76 to 0.84 all land in the band 0.008 +- 0.0005')
w, c, s = np.array([0.6, 0.3, 0.1]), np.array([0.01, -0.12, 0.08]), np.array([-0.03, 0.04, -0.02])
w2 = np.array([0.6, 0.19, 0.21])
ok(math.isclose(w @ s, -0.008) and math.isclose(w2 @ s, -0.0146) and math.isclose(w2 @ c, 0, abs_tol=1e-12), 'stress-hedge: old fund -0.008 in the rate rise, hedged -0.0146, hedged crash 0')
ok(math.isclose(0 + w2 @ s, -0.0146) and math.isclose(-0.018 + 0.0076 - 0.0042, -0.0146), 'stress-hedge 4: the no-half slip as a decimal is -0.0146, by both routes')

# finding 3: checkout part 4, the Sidak bar carried from part 3
sid = 1 - 0.95**(1 / 18)
ok(round(sid, 6) == 0.002846 and round(1 - (1 - 0.002846)**18, 4) == 0.05 and math.isclose(1 - (1 - sid)**18, 0.05), 'checkout 4: the Sidak bar gives 0.0500, from the 6-place bar and exactly')

# finding 4: gene part 5, q-same
gp = [0.0004, 0.0021, 0.0038, 0.0071, 0.0079, 0.0125, 0.0190, 0.034]
for top, want in ((0.12, 60), (0.16, 6), (0.5, 6)):
    a, b = bh(gp + [top] * 52, 0.15), bh_frac(gp + [top] * 52, 0.15)
    ok(a == b == want, f'gene 5: at q = 0.15 with the other 52 at {top}, BH rejects {a}')
ok(min(bh(gp + [top] * 52, 0.15) for top in (0.1001, 0.12, 0.14, 0.16, 0.5, 1.0)) == 6, 'gene 5: "at least 6" holds whatever the other 52 are')

# finding 6: a gene list whose BH step is not the fund managers' (rank 4 fails, rank 5 passes, answer 5)
alt = [0.0004, 0.0021, 0.0055, 0.0058, 0.0090, 0.0096, 0.0190, 0.034]
full = alt + [0.25] * 52
ok(bh(full, 0.10) == bh_frac(full, 0.10) == 6, 'alt gene list: BH at 0.10 rejects 6')
ok(sum(p <= 0.10 / 60 for p in full) == 1, 'alt gene list: Bonferroni rejects 1')
passes = [p <= k * 0.10 / 60 for k, p in enumerate(alt, 1)]
ok(passes == [True, True, False, True, False, True, False, False], 'alt gene list: ranks 3 and 5 fail inside the list, rank 6 passes')
ok(next(k for k, x in enumerate(passes, 1) if not x) - 1 == 2, 'alt gene list: the first-fail slip is 2')
q6 = Fr(60) * Fr('0.0096') / 6
ok(q6 == Fr('0.096') and bh(full, 0.0961) == 6 and bh(full, 0.0959) == 4, f'alt gene list: smallest q that keeps rank 6 is {float(q6)}; 6 just above, 4 just below')
ok(math.isclose(60 * 0.0096, 0.576) and math.isclose(60 * 0.0090 / 5, 0.108) and round(6 * 0.10 / 60, 4) == 0.01, 'alt gene list: slips 0.576 (no divide), 0.108 (rank 5 alone), 0.01 (the bar)')
ok(bh(full, 0.15) == 6 and bh(full, 0.20) == bh_frac(full, 0.20) == 7, 'alt gene list: unchanged at q = 0.15, 7 at q = 0.20 (the other 52 above 0.2)')

# finding 7: biomarker part 3, the bar at 2.8
ok(round(20 * 0.84, 1) == 16.8 and all(abs(v - 17) <= 0.5 for v in (16.8, 17)), 'biomarker 3: the 2.8 bar gives 16.8; a band 17 +- 0.5 takes 16.8 and 17')
ok(abs(17 - 15) > 0.5 and abs(17 - 18) > 0.5 + 0 and abs(17 - 20) > 0.5, 'biomarker 3: that band is clear of the key 15 and of 18 and 20')

# finding 8: cars part 4, both old figures
price = np.array([18000, 16600, 15400, 13400, 12400, 6200.0]); age = np.array([1, 2, 3, 4, 5, 9.0])
b, a = np.polyfit(age, price, 1)
ok(round(a + 9 * b) == 6267 and round(price.mean() - 1480 * 5) == 6267, 'cars 4: the uncorrected line gives 6,267 at 9 years, by the fit and by the mean point')
ok(all(abs(6267 - v) > 2 for v in (7850, 6600, 2930, 5350, 7517)), 'cars 4: 6,267 +- 1 is clear of the key and of every entry')

# finding 9: sensor part 3, 5/4 in front
adj = np.array([[0.6, -0.4], [-0.1, 1.4]])
ok(np.allclose(Fr(5, 4) * adj, np.linalg.inv(np.array([[1.4, 0.4], [0.1, 0.6]]))) and Fr(1) / Fr('0.8') == Fr(5, 4), 'sensor 3: 5/4 times the swapped matrix is the inverse; 1/0.8 = 5/4')

print(f'proposed: {n - f} of {n}')
sys.exit(1 if f else 0)
