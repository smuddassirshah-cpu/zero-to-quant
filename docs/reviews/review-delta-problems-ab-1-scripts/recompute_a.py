#!/usr/bin/env python3
"""Delta read, fix pass of review-problems-1.6-a: every changed answer, band, wrong value and printed number of the
   estimation and regression problem sets, recomputed by my own routes (raw data, fractions, numpy least squares).
   Run from the repo root with the scratchpad venv python. Exit 0 unless a check fails; FINDING rows are in the review."""
import math, sys, os
from fractions import Fraction as Fr
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

E, R = 'estimation', 'regression'
sq = math.sqrt

# ---------------------------------------------------------------- estimation
# p-robot-deliveries part 3: the likelihood on [0.9, 1]
L = lambda p: p**9 * (1 - p)**3
grid = np.linspace(0.9, 1, 100001)
key(E, 'p-robot-deliveries', 3, grid[np.argmax(L(grid))])
ok(all(np.diff(L(grid)) < 0), 'robot: L falls all the way from 0.9 to 1')
for wid, v in (('unrestricted', 9 / 12), ('top', 1), ('middle', 0.95)):
    slip(E, 'p-robot-deliveries', 3, wid, v)
bands_clear(E, 'p-robot-deliveries', 3)
ok(L(1) == 0, 'robot: L(1) = 0')

# p-currency-vol: eight weekly returns in %; the unit % field stores value / 100
r = np.array([1.4, -0.6, 0.7, -1.3, 1.1, -0.1, 1.8, -1.0])
ok(near(r.sum(), 2.0) and near((r**2).sum(), 9.96), 'currency: returns add to 2.0, squares to 9.96')
mu = r.mean(); sig = sq(((r - mu)**2).sum() / 8); s1 = sq(((r - mu)**2).sum() / 7)
for k in (1, 2, 3, 4):
    ok(W(E, 'p-currency-vol', k).get('unit') == '%', f'currency part {k} has unit %')
key(E, 'p-currency-vol', 1, mu / 100)
slip(E, 'p-currency-vol', 1, 'by-seven', r.sum() / 7 / 100); slip(E, 'p-currency-vol', 1, 'sizes', abs(r).sum() / 8 / 100)
key(E, 'p-currency-vol', 2, sig / 100)
slip(E, 'p-currency-vol', 2, 'n-minus-one', s1 / 100); slip(E, 'p-currency-vol', 2, 'zero-mean', sq(9.96 / 8) / 100)
slip(E, 'p-currency-vol', 2, 'variance', sig**2 / 100)
ok(near(sig**2, 1.1825) and round(sig, 4) == 1.0874 and near(9.96 - 8 * 0.25**2, 9.46), 'currency: 9.46, 1.1825, 1.0874')
ann = sig * sq(52)
key(E, 'p-currency-vol', 3, ann / 100)
w3 = W(E, 'p-currency-vol', 3)
# each widened slip band must take the slip from the exact sd, from 1.0874 and from the 2-place value part 2 accepts
for wid, f, bases in (('times-52', lambda s: s * 52, (sig, 1.0874, 1.09)), ('trading-days', lambda s: s * sq(252), (sig, 1.0874, 1.09)),
                      ('carried', lambda s: s * sq(52), (s1, 1.1625, 1.16)), ('variance', lambda s: 52 * s * s, (sig, 1.0874, 1.09))):
    x = wrong(E, 'p-currency-vol', 3, wid)
    for b in bases:
        v = f(b)
        for typed in (v, round(v, 2)):
            ok(abs(typed / 100 - x['value']) <= x['tol']['abs'] + 1e-12, f'currency part 3 {wid}: takes {typed:.4f} (from {b:.4f})',
               finding='the slip worked from the rounded value the part before accepts falls outside its band' if b in (1.16,) else None)
    ok(abs(x['value'] - w3['answer']) > x['tol']['abs'] + w3['tol']['abs'], f'currency part 3 {wid}: clear of the key')
bands_clear(E, 'p-currency-vol', 3)
# the key band takes the answer from 1.0874 (the question's value) and from 1.09
for v in (1.0874 * sq(52), 1.09 * sq(52), 7.84):
    ok(abs(v / 100 - w3['answer']) <= w3['tol']['abs'], f'currency part 3: key band takes {v:.4f}')
key(E, 'p-currency-vol', 4, 7.84 / 4 / 100)
for wid, v in (('no-two', 7.84 / sq(8)), ('weeks-in-year', 7.84 / sq(104)), ('no-root', 7.84 / 16)):
    slip(E, 'p-currency-vol', 4, wid, v / 100)
n5 = next(n for n in range(1, 1000) if 7.84 / sq(2 * n) <= 0.5)
key(E, 'p-currency-vol', 5, n5)
slip(E, 'p-currency-vol', 5, 'round-down', n5 - 1)
ok(7.84 / sq(244) > 0.5 and 7.84 / sq(246) <= 0.5, 'currency part 5: 122 weeks leave the SE above 0.5, 123 do not')
slip(E, 'p-currency-vol', 5, 'no-two', next(n for n in range(1, 1000) if 7.84 / sq(n) <= 0.5))
ok(122 < 8 * (1.96 / 0.5)**2 < 123 and near((7.84 / 0.5)**2 / 2, 122.9312), 'currency part 5: 122.9 by both routes')

# p-three-month-fund
x = np.array([2.0, 4.0, 9.0])
ss = ((x - x.mean())**2).sum()
ok(x.mean() == 5 and ss == 26, 'fund: mean 5, squares 26')
se, bse = sq(ss / 2 / 3), sq(ss / 3 / 3)
key(E, 'p-three-month-fund', 1, se / 100); key(E, 'p-three-month-fund', 3, bse / 100)
for wid, v in (('sd', sq(13)), ('by-n', sq(26 / 3 / 3)), ('no-root', 13 / 3)):
    slip(E, 'p-three-month-fund', 1, wid, v / 100)
for wid, v in (('carried', sq(13 / 3)), ('no-root', 26 / 9), ('one-draw', sq(26 / 3))):
    slip(E, 'p-three-month-fund', 3, wid, v / 100)
# bootstrap SE by enumeration of the 27 resamples
import itertools
means = [np.mean(c) for c in itertools.product(x, repeat=3)]
ok(near(np.std(means), bse), 'fund: the 27 resample means have sd sqrt(26/9)')
key(E, 'p-three-month-fund', 4, bse / se)
w4 = W(E, 'p-three-month-fund', 4)
ok(round(1.70 / 2.08, 3) == 0.817 and round(sq(2 / 3), 3) == 0.816, 'fund part 4: 0.817 from the rounded SEs, 0.816 exact')
ok(abs(0.817 - w4['answer']) <= w4['tol']['abs'] and abs(0.816 - w4['answer']) <= w4['tol']['abs'], 'fund part 4: both printed values accepted')
for wid, vals in (('inverted', (2.08 / 1.70, sq(1.5), 1.224, 1.225)), ('squared', ((1.70 / 2.08)**2, 2 / 3, 0.668, 0.667))):
    xw = wrong(E, 'p-three-month-fund', 4, wid)
    for v in vals:
        ok(abs(v - xw['value']) <= xw['tol']['abs'] + 1e-12, f'fund part 4 {wid}: takes {v:.4f}')
    ok(abs(xw['value'] - w4['answer']) > xw['tol']['abs'] + w4['tol']['abs'], f'fund part 4 {wid}: clear of the key')
bands_clear(E, 'p-three-month-fund', 4)

# p-ping-latency
p = np.array([304, 318, 296, 322, 310])
key(E, 'p-ping-latency', 1, p.mean()); key(E, 'p-ping-latency', 2, p.var(ddof=1))
slip(E, 'p-ping-latency', 1, 'by-four', p.sum() / 4); slip(E, 'p-ping-latency', 1, 'range', p.max() - p.min())
ok(abs(round(p.sum() / 4) - 387.75) <= 0.25, 'ping part 1 by-four takes the slip as a whole number, 388')
n4 = next(n for n in range(1, 500) if sq(110 / n) <= 2)
key(E, 'p-ping-latency', 4, n4)
slip(E, 'p-ping-latency', 4, 'carried', next(n for n in range(1, 500) if sq(88 / n) <= 2))
slip(E, 'p-ping-latency', 4, 'no-square', 110 / 2); slip(E, 'p-ping-latency', 4, 'round-down', n4 - 1)
slip(E, 'p-ping-latency', 4, 'unsquared', sq(110) / 2)
ok(round(sq(110) / 2, 1) == 5.2 and round(sq(110 / 27), 2) == 2.02 and sq(110 / 28) < 2 and near(110 / 4, 27.5), 'ping part 4: 5.2, 2.02, 27.5')
ok(abs(5 * 4.69**2 - 110) < 0.05, 'ping part 4 explain: 5 x 4.69^2 is about 110')
bands_clear(E, 'p-ping-latency', 4)
P4 = part(E, 'p-ping-latency', 4)
stale(P4, ['110', '2', '27.5', '28', '88', '4', '5.2', '27', '2.02', '3', '4.69', '5', '2'], 'ping part 4')
ok('1 microsecond' not in text(P4) and '19' not in numbers(P4), 'ping part 4: nothing of the old part')

# p-reference-mass
m = np.array([12, -6, 6, -10, 8])
key(E, 'p-reference-mass', 1, m.mean() - 0)
slip(E, 'p-reference-mass', 1, 'by-four', m.sum() / 4); slip(E, 'p-reference-mass', 1, 'sizes', abs(m).sum() / 5)
ok(abs(round(abs(m).sum() / 5) - 8.2) <= 0.2, 'mass part 1 sizes takes the slip as a whole number, 8')
key(E, 'p-reference-mass', 2, ((m - m.mean())**2).sum()); key(E, 'p-reference-mass', 3, (m**2).sum() / 5)
se5 = sq(76 / 5)
key(E, 'p-reference-mass', 5, 2 / se5)
key(E, 'p-reference-mass', 5, m.mean() / sq((m**2).mean() / 5))
w5 = W(E, 'p-reference-mass', 5)
for v in (0.51, round(2 / 3.90, 2), 2 / 3.90):
    ok(abs(v - w5['answer']) <= w5['tol']['abs'], f'mass part 5: key band takes {v:.4f}')
for wid, v in (('carried-90', 2 / sq(90 / 5)), ('carried-72', 2 / sq(72 / 5)), ('no-root', 2 / (76 / 5)), ('sd-not-se', 2 / sq(76)), ('inverted', se5 / 2)):
    slip(E, 'p-reference-mass', 5, wid, v)
    xw = wrong(E, 'p-reference-mass', 5, wid)
    ok(abs(round(v, 2) - xw['value']) <= xw['tol']['abs'], f'mass part 5 {wid}: takes the slip to 2 places, {round(v, 2)}')
ok(abs(3.90 / 2 - wrong(E, 'p-reference-mass', 5, 'inverted')['value']) <= 0.005, 'mass part 5 inverted takes 3.90 / 2 = 1.95')
bands_clear(E, 'p-reference-mass', 5)
ok(round(se5, 2) == 3.90 and round(2 / se5, 2) == 0.51, 'mass part 5: 3.90 and 0.51')
P5 = part(E, 'p-reference-mass', 5)
stale(P5, ['1', '2', '0', '76', '5', '3.90', '0.51', '90', '4', '72', '3', '15.2'], 'mass part 5')
ok('19' not in numbers(P5) and 'readings must the lab average' not in text(P5), 'mass part 5: nothing of the old part')

# p-tank-sensor
t = np.array([52, 47, 55, 50])
key(E, 'p-tank-sensor', 1, t.mean()); slip(E, 'p-tank-sensor', 1, 'by-three', t.sum() / 3); slip(E, 'p-tank-sensor', 1, 'last-two', (55 + 50) / 2)
ok((47 + 55) / 2 == 51 and (52 + 50) / 2 == 51, 'tank: other pairs average the key itself')
ll = lambda mu: -((t - mu)**2).sum() / 32
ok(round(math.exp(ll(51) - ll(48)), 2) == 3.08, 'tank part 4: 3.08 times as likely at 51 as at 48')
key(E, 'p-tank-sensor', 4, 51 + sq(8 * math.log(10)))

# p-ticket-bot part 4, p-routing-test part 3
g = 0.01 / sq(0.7 * 0.3 / 580)
key(E, 'p-ticket-bot', 4, g)
xw = wrong(E, 'p-ticket-bot', 4, 'no-root')
for v in (0.01 / (0.21 / 580), 27.6, 27.62):
    ok(abs(v - xw['value']) <= xw['tol']['abs'], f'ticket part 4 no-root takes {v:.3f}')
bands_clear(E, 'p-ticket-bot', 4)
seR = sq(3.0**2 / 100 + 4.2**2 / 144)
ok(round(seR, 3) == 0.461, 'routing: SE 0.461')
key(E, 'p-routing-test', 3, 0.8 - 1.96 * 0.461)
slip(E, 'p-routing-test', 3, 'no-sign', abs(0.8 - 1.96 * 0.461))
bands_clear(E, 'p-routing-test', 3)

# ---------------------------------------------------------------- regression
# p-stopping-distances
sx = np.array([20, 30, 40, 50, 60.0]); sy = np.array([12, 23, 36, 53, 73.0])
b, a = np.polyfit(sx, sy, 1)
key(R, 'p-stopping-distances', 1, b); key(R, 'p-stopping-distances', 2, a)
Sxx = ((sx - sx.mean())**2).sum(); Sxy = ((sx - sx.mean()) * (sy - sy.mean())).sum(); Syy = ((sy - sy.mean())**2).sum()
ok(near(Sxx, 1000) and near(Sxy, 1520) and near(Syy, 2345.2), 'stopping: Sxx 1000, Sxy 1520, Syy 2345.2')
slip(R, 'p-stopping-distances', 1, 'reverse', Sxx / Sxy)
slip(R, 'p-stopping-distances', 1, 'other-way', np.polyfit(sy, sx, 1)[0])
slip(R, 'p-stopping-distances', 1, 'mixed', (Sxy / 4) / (Sxx / 5)); slip(R, 'p-stopping-distances', 1, 'through-origin', (sx * sy).sum() / (sx**2).sum())
bands_clear(R, 'p-stopping-distances', 1)
for typed, wid in ((0.66, 'reverse'), (0.658, 'reverse'), (0.65, 'other-way'), (0.648, 'other-way')):
    xw = wrong(R, 'p-stopping-distances', 1, wid)
    ok(abs(typed - xw['value']) <= xw['tol']['abs'] + 1e-12, f'stopping part 1: {typed} lands in {wid}')
slip(R, 'p-stopping-distances', 2, 'no-sign', -a); slip(R, 'p-stopping-distances', 2, 'carried', sy.mean() - 1.0444 * 40)
bands_clear(R, 'p-stopping-distances', 2)
res = sy - (a + b * sx)
ok(np.allclose(res, [3.0, -1.2, -3.4, -1.6, 3.2]) and abs(1 - (res**2).sum() / Syy - 0.985) < 0.0005, 'stopping part 5: residuals and R^2')
ok(abs(res[2]) - 3.2 < 0.5 and near(a + b * 70, 85), 'stopping part 5: the middle miss is about the size of the end ones; 85 m at 70 mph')

# p-car-prices
age = np.array([1, 2, 3, 4, 5, 9.0]); price = np.array([18000, 16600, 15400, 13400, 12400, 6200.0])
b0, a0 = np.polyfit(age, price, 1)
key(R, 'p-car-prices', 2, b0, slack=1e-6)
price2 = price.copy(); price2[5] = 8200
b1, a1 = np.polyfit(age, price2, 1)
key(R, 'p-car-prices', 3, b1 - b0, slack=1e-6)
ok(near(b1, -1230) and near(price2.mean(), 14000), 'cars: corrected slope -1230, corrected mean 14000')
key(R, 'p-car-prices', 4, a1 + 9 * b1, slack=1e-6)
key(R, 'p-car-prices', 4, 14000 - 1230 * 5)
for wid, v in (('old-slope', 14000 - 1480 * 5), ('raw-x', 14000 - 1230 * 9), ('wrong-way', 14000 - 1730 * 5), ('old-mean', price.mean() - 1230 * 5)):
    slip(R, 'p-car-prices', 4, wid, v)
bands_clear(R, 'p-car-prices', 4)
ok(8200 - (a1 + 9 * b1) == 350 or near(8200 - (a1 + 9 * b1), 350, 1e-6), 'cars part 4 explain: the car sold 350 above its own line')
ok(round(price.mean()) == 13667 and 1230 * 5 == 6150, 'cars part 4: 13,667 and 6,150')
C4 = part(R, 'p-car-prices', 4)
stale(C4, ['2', '1480', '3', '250', '1230', '14000', '9', '7850', '5', '4', '0', '1730', '13667', '6150', '8200', '350'], 'cars part 4')
ok('corrected slope?' not in text(C4) and not ({'1430', '1030'} & numbers(C4)), 'cars part 4: nothing of the old part')
# the old line's own value at 9 years: both old figures together, a slip with no line
print(f'NOTE    cars part 4: old slope with old mean gives {price.mean() - 1480 * 5:.0f} (no wrong entry)')

# p-power-price part 4, and the theory it rests on: a synthetic two-predictor fit with r = 0.6 against one with r = 0
ok(near(1 / (1 - 0.6**2), 1.5625) and near(sq(1.5625), 1.25), 'power: VIF 1.5625, root 1.25')
key(R, 'p-power-price', 4, 0.05 / sq(1.5625))
for wid, v in (('by-vif', 0.05 / 1.5625), ('times', 0.05 * 1.25), ('times-vif', 0.05 * 1.5625), ('carried', 0.05 / sq(1 / (1 - 0.48**2)))):
    slip(R, 'p-power-price', 4, wid, v)
bands_clear(R, 'p-power-price', 4)
ok(round(1 / (1 - 0.48**2), 4) == 1.2994, 'power: the carried VIF is 1.2994')


def gas_var(rho):                       # exact: sigma^2 [(X'X)^-1]_gas for centred predictors with sds 10 and 5, n = 200
    S = 199 * np.array([[100, rho * 50], [rho * 50, 25.0]])
    return np.linalg.inv(S)[0, 0]


ok(near(sq(gas_var(0.6) / gas_var(0.0)), 1.25), 'power: SE(gas) with r = 0.6 over SE with r = 0, same spreads and noise, is 1.25')
Pw = part(R, 'p-power-price', 4)
stale(Pw, ['0.05', '1.5625', '3', '1.25', '0.04', '1.2994'], 'power part 4')
ok(not ({'313', '312', '250', '500', '260'} & numbers(Pw)) and 'days' not in text(Pw), 'power part 4: nothing of the old part')

# p-freight-summary part 1; p-solar-output part 2; p-raw-intercept part 4; p-bond-fund-weeks
key(R, 'p-freight-summary', 1, 0.2 / 0.8 * 40)
ok('ESS' not in text(item(R, 'p-freight-summary')), 'freight: no ESS left')
b12 = np.linalg.solve([[40, 24], [24, 30]], [88, 45])
ok(near(b12[0], 2.5), 'solar: b1 = 2.5'); key(R, 'p-solar-output', 2, b12[1]); slip(R, 'p-solar-output', 2, 'no-sign', -b12[1])
bands_clear(R, 'p-solar-output', 2)
nn = next(n for n in range(100, 1000) if 1.4 * sq(n / 100) >= 2)
key(R, 'p-raw-intercept', 4, nn); slip(R, 'p-raw-intercept', 4, 'extra', nn - 100); slip(R, 'p-raw-intercept', 4, 'round-down', nn - 1)
bands_clear(R, 'p-raw-intercept', 4)
key(R, 'p-bond-fund-weeks', 1, (0.05 - 0.08 * 10 - 0.03 * -5) / 100); slip(R, 'p-bond-fund-weeks', 1, 'no-sign', 0.006)
bands_clear(R, 'p-bond-fund-weeks', 1)
e = np.array([0.20, 0.30, 0.25, 0.10, -0.10, -0.20, -0.25]); e = np.append(e, -e.sum())
d = (np.diff(e)**2).sum() / (e**2).sum(); r1 = (e[1:] * e[:-1]).sum() / (e**2).sum()
ok(round(d, 2) == 0.22 and round(r1, 2) == 0.73 and near(e[-1], -0.30), f'bond: d = {d:.4f}, lag-1 correlation {r1:.3f}, week 8 residual -0.30')
key(R, 'p-bond-fund-weeks', 4, 1 - d / 2)
says(part(R, 'p-bond-fund-weeks', 4), '0.73')

# p-overlap-signal part 4 (the simulation of the factor and of HAC is overlap-sim.py)
f = sq(1 + 2 * sum((1 - j / 5)**2 for j in range(1, 5)))
ok(round(f, 3) == 1.844, 'overlap: factor 1.844')
key(R, 'p-overlap-signal', 4, 3.5 / f); slip(R, 'p-overlap-signal', 4, 'root-h', 3.5 / sq(5))
bands_clear(R, 'p-overlap-signal', 4)
ok(near(sq(4500 / 500), 3) and near(3 * sq(0.0004), 0.06) and near(0.21 / 0.06, 3.5), 'overlap: s = 3, SE 0.06, t 3.5')

done('recompute_a')
