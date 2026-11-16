#!/usr/bin/env python3
"""Numbers of the fixes proposed in review-problems-fin-ml-1-3.md. Exit 0 when every proposed value holds."""
import math, sys
from fractions import Fraction as F
from statistics import NormalDist, stdev
Phi = NormalDist().cdf
bad = 0


def ok(c, m):
    global bad
    if not c:
        bad += 1
        print('FAIL', m)


def inband(x, v, t):
    return abs(x - v) <= t + 1e-12


def se(sr, n, sk, ku):
    return math.sqrt((1 - sk * sr + (ku - 1) / 4 * sr * sr) / (n - 1))


def g(f, p, b=1.8):
    return p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)


# finding 1: copper at threshold 0.55
side = [1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
labl = [1, -1, -1, 0, 1, 1, -1, -1, 0, 1, 0, -1]
pp = [0.74, 0.61, 0.58, 0.33, 0.47, 0.69, 0.52, 0.63, 0.29, 0.81, 0.41, 0.66]
meta = [int(s * y == 1) for s, y in zip(side, labl)]
take = [i for i in range(12) if pp[i] >= 0.55]
ok([i + 1 for i in take] == [1, 2, 3, 6, 8, 10, 12], 'taken')
P, R = F(sum(meta[i] for i in take), len(take)), F(sum(meta[i] for i in take), sum(meta))
ok(P == F(4, 7) and R == F(4, 5), 'P, R')
ok(round(float(P), 4) == 0.5714 and round(len(take) / 12, 4) == 0.5833, 'precision 0.5714, share 0.5833')
up = [i for i in range(12) if labl[i] == 1]
ok(F(sum(1 for i in up if i in take), len(up)) == F(3, 4), 'price-up recall 3/4')
f1 = 2 * P * R / (P + R)
ok(f1 == F(2, 3) and abs(2 * 0.5714 * 0.8 / 1.3714 - 0.6667) <= 0.0001, 'F1 2/3; the decimal route 0.6666 is inside 0.6667 +- 0.0001')
ok(round(float((P + R) / 2), 4) == 0.6857 and round(float(P * R), 4) == 0.4571 and round(0.5714 * 0.8, 4) == 0.4571 and round((0.5714 + 0.8) / 2, 4) == 0.6857, 'mean, product')
ok(abs(0.6857 - 0.6667) > 0.0002 and abs(0.4571 - 0.6667) > 0.0002 and abs(0.5714 - 0.8) > 0.001, 'bands apart')
# finding 2: futures part 4 bands
netd = 0.038
honest = [Phi(netd / se(netd, 750, -0.6, 5)), Phi(0.038 / 0.0370), Phi(1.03), 0.848, 0.849, 0.847]
ok(all(inband(x, 0.848, 0.0015) for x in honest), 'key 0.848 +- 0.0015 takes every honest route')
normal = [Phi(netd / se(netd, 750, 0, 3)), Phi(0.038 / 0.0366), 0.850, 0.851]
ok(all(inband(x, 0.8505, 0.0006) for x in normal) and not any(inband(x, 0.848, 0.0015) for x in normal), 'normal 0.8505 +- 0.0006')
ok(0.8505 - 0.0006 > 0.848 + 0.0015, 'bands apart')
# finding 3: futures part 3 annual band
ann = [se(0.038 * math.sqrt(252), 750, -0.6, 5), se(0.60, 750, -0.6, 5), 0.0479, 0.0480]
ok(all(inband(x, 0.04795, 0.00007) for x in ann), f'annual 0.04795 +- 0.00007 takes {ann}')
ok(0.04795 - 0.00007 > 0.037 + 0.00005, 'annual band clear of the key')
# finding 4: kelly part 3
ok(f'{1 + 1.8 * 0.176:.4f}' == '1.3168' and round(0.44 * math.log(1.3168), 4) == 0.1211 and round(0.56 * math.log(0.824), 4) == -0.1084, 'terms at f = 0.176')
ok(round(g(0.176, 0.44), 4) == 0.0127 and round(0.1211 - 0.1084, 4) == 0.0127, 'growth 0.0127')
fk = 0.47 - 0.53 / 1.8
ep = [0.44 * math.log(1.176) + 0.56 * math.log(0.824), 0.44 * math.log(1 + fk) + 0.56 * math.log(1 - fk), -0.0371, -0.0369]
ok(all(inband(x, -0.0370, 0.00015) for x in ep), f'even-payout -0.0370 +- 0.00015 takes {ep}')
ok(round(ep[0], 4) == -0.0371, 'even-payout from the stated stake is -0.0371')
ok(round(g(0.176, 0.44) / g(0.129, 0.44), 3) == 0.873, 'share from the stated stakes 0.873 (inside 0.875 +- 0.003)')
# finding 5: shipping no-mean
sd = stdev([22, 21, 25])
ok(all(inband(x, 12.015, 0.006) for x in [25 / sd, 25 / 2.08, 12.01, 12.02]), 'no-mean 12.015 +- 0.006')
# finding 6: gold ratios
d = 0.35
ok([round((k - 1 - d) / k, 4) for k in (2, 3, 4)] == [0.325, 0.55, 0.6625], 'ratios')
# finding 7: retail
v = [1.15, 0.82, 1.15, 0.97, 2.40, 0.64, 1.06]
m, s = sum(v) / 7, stdev(v)
ok(sum(1 for x in v if x < m) == 6 and round((0.64 - m) / s, 2) == -0.93, 'six below the mean; Raven z -0.93')
q = sorted([0, F(1, 6), F(2, 6), F(3, 6), F(3, 4), F(3, 4), 1])
ok(q[-2] == F(3, 4), 'the six others rank from 0 to 0.75')
print('proposed.py:', 'ok' if not bad else f'{bad} failures')
sys.exit(1 if bad else 0)
