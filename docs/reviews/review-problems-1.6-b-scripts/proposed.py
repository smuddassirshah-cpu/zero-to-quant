"""Numbers of the fixes proposed in docs/reviews/review-problems-1.6-b.md, each worked twice.

Usage (repo root): <venv>/bin/python docs/reviews/review-problems-1.6-b-scripts/proposed.py"""
import sys
from math import erf, sqrt

from scipy import stats

N = stats.norm
phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
    print(('ok   ' if cond else 'FAIL ') + msg)


def clear(bands, msg):
    """bands: (value, tol) pairs; no two may touch."""
    b = sorted(bands)
    ok(all(a + ta < c - tc for (a, ta), (c, tc) in zip(b, b[1:])), msg)


# finding 1: checkout part 2 asked as an equality
p = 1 - 0.95 ** (1 / 25)
ok(round(p, 6) == 0.002050 and abs(1 - (1 - p) ** 25 - 0.05) < 1e-12, f'checkout 2: 1 - (1 - p)^25 = 0.05 at p = {p:.8f}, 0.002050 to 6 places')
ok(1 - (1 - 0.002050) ** 25 > 0.05 > 1 - (1 - 0.002049) ** 25, 'checkout 2: 0.002050 itself is over 0.05, 0.002049 under: "at most" favours the refused 0.002049')

# finding 2: fertiliser parts 2 and 4 with a second Phi value to choose from
ok(round(N.cdf(2.25), 4) == 0.9878 == round(phi(2.25), 4), 'fertiliser 2: Phi(2.25) = 0.9878')
ok(round(N.cdf(3.182), 4) == 0.9993 == round(phi(3.182), 4), 'fertiliser 4: Phi(3.182) = 0.9993')
clear([(0.7274, 5e-5), (0.2726, 5e-5), (0.05, 5e-5), (0.9878, 5e-5)], 'fertiliser 2: bands with centre-only 0.9878')
clear([(0.9379, 5e-5), (0.0621, 5e-5), (0.7274, 5e-5), (0.9993, 5e-5)], 'fertiliser 4: bands with centre-only 0.9993')

# finding 4: wider slip bands on running shoes parts 2 and 3
clear([(3, 0), (2.828, 0.005), (9, 0), (3.046, 0.005)], 'shoes 2: slip bands of 0.005 stay clear')
clear([(-4, 0.005), (-1.333, 0.005), (-3.771, 0.005), (-4.243, 0.005), (4, 0.005)], 'shoes 3: slip bands of 0.005 stay clear')
for typed, val in ((2.83, 2.828), (3.05, 3.046), (-1.33, -1.333), (-4.24, -4.243), (-3.77, -3.771)):
    ok(abs(typed - val) <= 0.005, f'shoes: {typed} lands within 0.005 of {val}')

# finding 5: doubled-tail slips with a band of 0.0001
for name, told, exact, ans in (('pizza 2', 2 * (1 - 0.9599), 2 * N.sf(1.75), 0.0401), ('blood 1', 2 * (1 - 0.9641), 2 * N.sf(1.8), 0.0359),
                               ('funds 2', 2 * (1 - 0.9965), 2 * N.sf(2.7), 0.0035)):
    ok(abs(round(exact, 4) - round(told, 4)) <= 0.0001 + 1e-12 and abs(round(told, 4) - ans) > 0.0002,
       f'{name}: stored {told:.4f}, unrounded {exact:.5f}; a band of 0.0001 takes both and stays clear of the key')

# finding 7: the t test's own power for the shoe trial
nct = lambda n: stats.nct.sf(stats.t.ppf(0.95, n - 1), n - 1, 0.5 * sqrt(n))
ok(nct(26) < 0.8 < nct(27), f'shoes 5: a paired t test first reaches 80% at 27 runners ({nct(26):.4f} at 26, {nct(27):.4f} at 27)')
ok(N.cdf(0.5 * sqrt(24) - 1.645) < 0.8 < N.cdf(0.5 * sqrt(25) - 1.645), 'shoes 5: the normal formula gives 25')
ok(abs(1 - 0.9973 ** 380 - 0.642) < 0.0005, 'biomarkers 5: 1 - 0.9973^380 = 0.642 for independent tests')

# finding 3: wine part 2, a carried value that is not the key cut to 3 places
ok(round(78 / 4096, 5) == 0.01904 and round(79 / 4096, 3) == 0.019, 'wine 2: 78/4096 = 0.01904; the key cut to 3 places is 0.019')

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
