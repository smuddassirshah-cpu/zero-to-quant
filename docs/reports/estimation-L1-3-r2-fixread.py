"""Fix-pass read of estimation levels 1 to 3, round 2 (content commit f94c24a5).
Independent checks of the changed claims. Exits 0 when every check holds.

1. Divisor for a variance at n = 20 under normal, t8, t5 and uniform data:
   bias of s^2, MSE at c = n - 1, n, n + 1, and the best divisor
   c* = n + 1 + (n - 1) * excess_kurtosis / n  (derived below), by formula and by simulation.
2. SE of the sample sd: sigma / sqrt(2n) for normal data, larger for fat tails.
3. review-1 r-s2-1357: slip bands against the key and the other slips.
4. homework-2 log score: expected score maximised at q = p.
5. l3 s10 and l8, l9 numbers.
"""
import math
import sys
import numpy as np

fails = []


def check(name, ok, detail=''):
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))
    if not ok:
        fails.append(name)


rng = np.random.default_rng(20261126)
n, k = 20, 19

# --- 1. divisor ---------------------------------------------------------------
# Var(s^2) = sigma^4 (2/(n-1) + g/n), g = excess kurtosis (Casella and Berger ex. 5.8; Mood, Graybill and Boes 6.3).
# With SS = (n-1) s^2:  V = Var(SS)/sigma^4 = (n-1)^2 (2/(n-1) + g/n).
# MSE(c)/sigma^4 = (V + (k-c)^2)/c^2, minimised where c = k + V/k = n + 1 + (n-1) g / n.
dists = {
    'normal': (lambda size: rng.standard_normal(size), 1.0, 0.0),
    't8': (lambda size: rng.standard_t(8, size), 8 / 6, 6 / (8 - 4)),
    't5': (lambda size: rng.standard_t(5, size), 5 / 3, 6 / (5 - 4)),
    'uniform': (lambda size: rng.uniform(-1, 1, size), 1 / 3, -1.2),
}
cs = np.arange(15.0, 40.0, 0.05)
for name, (draw, var, g) in dists.items():
    reps = 4_000_000 if name == 't5' else 1_000_000
    ss_parts, chunk = [], 250_000
    for _ in range(reps // chunk):
        x = draw((chunk, n))
        ss_parts.append(((x - x.mean(axis=1, keepdims=True)) ** 2).sum(axis=1) / var)
    ss = np.concatenate(ss_parts)                       # SS in units of sigma^2
    s2 = ss / k
    se_bias = s2.std() / math.sqrt(reps)
    check(f'{name}: s^2 unbiased', abs(s2.mean() - 1) < 5 * se_bias, f'mean {s2.mean():.4f} se {se_bias:.4f}')
    V = k * k * (2 / k + g / n)
    mse_f = {c: (V + (k - c) ** 2) / c ** 2 for c in (19, 20, 21)}
    mse_s = {c: float(((ss / c - 1) ** 2).mean()) for c in (19, 20, 21)}
    cstar_f = n + 1 + k * g / n
    m1, m2 = ss.mean(), (ss ** 2).mean()
    cstar_s = m2 / m1                                   # argmin over c of E(SS/c - 1)^2
    print(f'     {name}: MSE formula {[round(mse_f[c], 4) for c in (19, 20, 21)]} sim {[round(mse_s[c], 4) for c in (19, 20, 21)]}'
          f' c* formula {cstar_f:.2f} sim {cstar_s:.2f}')
    if name == 'normal':
        check('normal: MSE 0.1053, 0.0975, 0.0952', all(abs(mse_f[c] - v) < 5e-5 for c, v in zip((19, 20, 21), (0.1053, 0.0975, 0.0952)))
              and all(abs(mse_s[c] - mse_f[c]) < 0.001 for c in (19, 20, 21)))
        check('normal: best divisor n + 1', abs(cstar_f - 21) < 1e-12 and abs(cstar_s - 21) < 0.05, f'{cstar_s:.3f}')
        check('normal: gain about 10%', abs(1 - mse_f[21] / mse_f[19] - 0.10) < 0.01, f'{1 - mse_f[21] / mse_f[19]:.4f}')
    if name in ('t8', 't5'):
        # t5 has an infinite 8th moment, so the simulated c* converges slowly; the sign is what is tested
        check(f'{name}: fat tails push the best divisor above n + 1', cstar_f > 21 and cstar_s > 21.5, f'formula {cstar_f:.2f} sim {cstar_s:.2f}')
        check(f'{name}: MSE(n + 1) < MSE(n) < MSE(n - 1) in simulation', mse_s[21] < mse_s[20] < mse_s[19])
    if name == 'uniform':
        check('uniform: best divisor below n + 1 but above n - 1', 19 < cstar_f < 21 and abs(cstar_s - cstar_f) < 0.05, f'{cstar_s:.3f}')
# no distribution brings c* back to n - 1: g >= -2 gives c* >= n + 1 - 2(n-1)/n > n - 1
check('best divisor exceeds n - 1 for every distribution (g >= -2)', n + 1 - 2 * k / n > n - 1)

# --- 2. SE of the sd ----------------------------------------------------------
for name in ('normal', 't8', 'uniform'):
    draw, var, g = dists[name]
    x = draw((400_000, n))
    s = x.std(axis=1, ddof=1) / math.sqrt(var)
    ratio = s.std() / (1 / math.sqrt(2 * n))
    print(f'     {name}: sd(s) / (sigma / sqrt(2n)) = {ratio:.3f}')
    if name == 'normal':
        check('normal: SE(s) about sigma / sqrt(2n)', abs(ratio - 1) < 0.03, f'{ratio:.3f}')
    if name == 't8':
        check('t8: SE(s) larger than sigma / sqrt(2n)', ratio > 1.1, f'{ratio:.3f}')
check('l8: 1.0 / sqrt(40) = 0.16, annual 2.5', round(1 / math.sqrt(40), 2) == 0.16 and round(math.sqrt(252) / math.sqrt(40), 1) == 2.5)

# --- 3. review-1 slip band ----------------------------------------------------
r = [1, 3, 5, 7]
key = np.var(r, ddof=1)
check('review-1 key 6.6667', abs(key - 6.6667) < 1e-4 and abs(sum((v - 4) ** 2 for v in r) / 3 - key) < 1e-12)
dec = np.var([v / 100 for v in r], ddof=1)
check('review-1 decimal slip 0.00066667', abs(dec - 0.00066667) < 1e-8 and abs(key / 1e4 - dec) < 1e-12)
band = (0.00066667 - 4e-5, 0.00066667 + 4e-5)
inside = [0.00066667, 0.000667, 0.00067, 0.0007, 0.00066, 0.0006667]
outside = [0.0005,                  # divide by n, decimals
           0.002,                   # sum of squares, decimals
           0.02582,                 # sd, decimals
           0.0006, 0.001, 0.0, 6.6667, 5, 20, 2.582, 0.066667, 0.0066667]
check('review-1 decimal band takes the rounded decimal forms', all(band[0] <= v <= band[1] for v in inside))
check('review-1 decimal band excludes the key, other slips and their decimal forms', not any(band[0] <= v <= band[1] for v in outside))
others = [(6.6667, 0.006), (5, 0.005), (20, 0.005), (2.582, 0.005)]
check('review-1 bands disjoint', all(hi < band[0] - 0 or lo > band[1] for lo, hi in [(v - t, v + t) for v, t in others]))

# --- 4. log score -------------------------------------------------------------
qs = np.linspace(0.001, 0.999, 999)
ok = True
for p in (0.1, 0.35, 0.5, 0.7, 0.9):
    e = p * np.log(qs) + (1 - p) * np.log(1 - qs)
    ok &= abs(qs[e.argmax()] - p) < 1e-9
check('log score: expected score highest at q = p', bool(ok))
check('homework-2: -6.390 and -6.109', round(7 * math.log(.8) + 3 * math.log(.2), 3) == -6.390 and round(7 * math.log(.7) + 3 * math.log(.3), 3) == -6.109)

# --- 5. small numbers ---------------------------------------------------------
a = [2, 4, 6]
check('l3: 2.0, 1.633, 2.667, 4.0', round(float(np.std(a, ddof=1)), 3) == 2.0 and round(float(np.std(a)), 3) == 1.633
      and round(float(np.var(a)), 3) == 2.667 and round(float(np.var(a, ddof=1)), 3) == 4.0)
check('l9: sqrt(0.6 * 0.4 / 150) = 0.04', abs(math.sqrt(0.6 * 0.4 / 150) - 0.04) < 1e-12)
check('l2: 1 / sqrt(100) = 0.10, 1 / sqrt(25) = 0.20', 1 / math.sqrt(100) == 0.1 and 1 / math.sqrt(25) == 0.2)

print('failures:', len(fails))
sys.exit(1 if fails else 0)
