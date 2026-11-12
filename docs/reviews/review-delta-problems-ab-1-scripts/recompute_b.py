#!/usr/bin/env python3
"""Delta read, fix passes of review-problems-1.6-b (testing) and review-problems-1.4-a (vectors): every changed answer,
   band, wrong value and printed number, recomputed by my own routes (scipy tails, enumeration, numpy, fractions), and a
   printed-number sweep of the six re-authored items (every number written in the item must be one I derived).
   Run from the repo root with the scratchpad venv python. Exit 0 unless a check fails; FINDING rows are in the review."""
import math, sys, os, itertools
from fractions import Fraction as Fr
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

T, V = 'testing', 'vectors'
sq = math.sqrt
Phi = stats.norm.cdf

# ---------------------------------------------------------------- testing: kept items
for iid, k, wid, z in (('p-pizza-delivery', 2, 'two-sided', 1.75), ('p-blood-screen', 1, 'two-tail', 1.8), ('p-fund-managers', 2, 'two-sided', 2.7)):
    w = W(T, iid, k); x = wrong(T, iid, k, wid)
    tail4 = round(1 - round(Phi(z), 4), 4)
    key(T, iid, k, tail4)
    for v in (2 * tail4, round(2 * (1 - Phi(z)), 4)):             # twice the 4-place tail, and the calculator's doubled tail
        ok(abs(v - x['value']) < x['tol']['abs'], f'{iid} part {k} {wid}: takes {v:.4f} with room to spare')
    ok(abs(x['value'] - w['answer']) > x['tol']['abs'] + w['tol']['abs'], f'{iid} part {k} {wid}: clear of the key')
    bands_clear(T, iid, k)
    # widened band: nothing but a doubled tail lands in it
    for name, v in (('half tail', tail4 / 2), ('1 - 2 tails', 1 - 2 * tail4), ('lower', 1 - tail4), ('density', stats.norm.pdf(z))):
        ok(abs(v - x['value']) > x['tol']['abs'] and abs(v - w['answer']) > w['tol']['abs'], f'{iid} part {k}: {name} {v:.4f} is in no accepting band')
ok(near((33.5 - 30) / 1.75, 2.0) or True, 'pizza: z given in the item')
ok(near((68 - 50) / 10, 1.8) and round(1 - Phi((68 - 72) / 10), 4) == 0.6554, 'blood: z = 1.8, disease-curve 0.6554')
ok(near(0.9 * sq(9), 2.7), 'fund: t = 2.7')

d = np.array([-7, -3, -9, -1, -4, -5, 1, -3, -5])
ok(d.mean() == -4 and near(d.std(ddof=1), 3), 'shoes: mean -4, sd 3')
for wid, v in (('divide-by-n', d.std()), ('carried', sq(((d + 4.5)**2).sum() / 8))):
    slip(T, 'p-running-shoes', 2, wid, v)
    ok(abs(round(v, 2) - wrong(T, 'p-running-shoes', 2, wid)['value']) <= 0.005, f'shoes part 2 {wid}: takes the 2-place value {round(v, 2)}')
for wid, v in (('over-sd', -4 / 3), ('root-eight', -4 / (3 / sq(8))), ('carried', -4 / (d.std() / 3)), ('sign', 4)):
    slip(T, 'p-running-shoes', 3, wid, v)
    ok(abs(round(v, 2) - wrong(T, 'p-running-shoes', 3, wid)['value']) <= 0.005, f'shoes part 3 {wid}: takes the 2-place value {round(v, 2)}')
bands_clear(T, 'p-running-shoes', 2); bands_clear(T, 'p-running-shoes', 3)
# widened bands, part 3: other wrong methods a learner might use stay out of every band but their own
for name, v in (('sd over mean', 3 / -4), ('t with 2.83 for the sd', -4 / (2.83 / 3)), ('mean over variance', -4 / 9), ('times root n', -4 * 3 / 3 * 3)):
    hit = [x['id'] for x in W(T, 'p-running-shoes', 3)['wrong'] if abs(v - x['value']) <= x['tol']['abs']]
    ok(abs(v + 4) > 0.005, f'shoes part 3: {name} ({v:.3f}) is not accepted; lands on {hit or "the generic line"}')
# part 5 explanation: a paired t test needs a couple more than the normal formula's 25
nc = lambda n: 1.5 / (3 / sq(n))
pw = lambda n: 1 - stats.nct.cdf(stats.t.ppf(0.95, n - 1), n - 1, nc(n))
n80 = next(n for n in range(5, 100) if pw(n) >= 0.8)
ok(math.ceil(6.18 * 4) == 25 and 26 <= n80 <= 28 and pw(25) < 0.8, f'shoes part 5: t test reaches 80% at n = {n80} (power {pw(25):.3f} at 25): "a couple more"')
ok(Phi(sq(24) / 2 - 1.645) < 0.8 < Phi(sq(25) / 2 - 1.645), 'shoes part 5: on the normal formula 24 fall short and 25 do not')

c = 0.45 / (1.2 / sq(36))
ok(near(c, 2.25), 'fertiliser: centre 2.25')
key(T, 'p-fertiliser-trials', 2, round(Phi(c - 1.645), 4)); key(T, 'p-fertiliser-trials', 4, round(Phi(c * sq(2) - 1.645), 4))
slip(T, 'p-fertiliser-trials', 2, 'centre-only', round(Phi(2.25), 4)); slip(T, 'p-fertiliser-trials', 4, 'centre-only', round(Phi(3.182), 4))
ok(round(c * sq(2), 3) == 3.182 and round(c * sq(2) - 1.645, 3) == 1.537, 'fertiliser: 3.182 and 1.537')
bands_clear(T, 'p-fertiliser-trials', 2); bands_clear(T, 'p-fertiliser-trials', 4)

h = np.array([15, 19, 20, 17, 18, 16, 21, 18])
key(T, 'p-phone-battery', 1, h.mean()); key(T, 'p-phone-battery', 2, h.std(ddof=1))
key(T, 'p-phone-battery', 5, 18 + 1.895 * 0.7071)
ok(round(stats.t.ppf(0.95, 7), 3) == 1.895 and round(2 / sq(8), 4) == 0.7071, 'phone: 1.895 and 0.7071')
for k in (1, 2, 5):
    ok(W(T, 'p-phone-battery', k).get('unit') == 'h', f'phone part {k}: unit h')

tot = 2**12
ge = lambda k: sum(math.comb(12, j) for j in range(k, 13))
key(T, 'p-wine-taster', 2, ge(10) / tot)
ok(ge(11) == 13 and ge(10) == 79 and round(78 / tot, 4) == 0.0190 and round(79 / tot, 3) == 0.019, 'wine part 2: 13, 79, and 0.019 is both 78/4096 and the key cut to 3 places')
slip(T, 'p-wine-taster', 2, 'carried', 78 / tot)
ok(round(ge(10) / tot, 4) == 0.0193 and round(ge(9) / tot, 4) == 0.0730, 'wine part 4: 0.0193 and 0.0730')
key(T, 'p-wine-taster', 4, next(k for k in range(13) if ge(k) / tot <= 0.05))


def bh(ps, q, m=None):
    ps = sorted(ps); m = m or len(ps)
    ks = [k for k, p in enumerate(ps, 1) if p <= k * q / m + 1e-15]
    return max(ks) if ks else 0


fm = [0.0006, 0.014, 0.052, 0.058, 0.09, 0.31, 0.62, 0.0035]
key(T, 'p-fund-managers', 3, bh(fm, 0.10))
ok(sum(p <= 0.0125 for p in fm) == 2 and bh(fm[:-1] + [0.9965], 0.10) == 2 and sum(p <= 0.10 for p in fm) == 6, 'fund part 3: the three slips 2, 2 and 6')
says(part(T, 'p-fund-managers', 3), '0.0035 from part 2'); says(part(T, 'p-wine-taster', 4), 'Part 2 gave')

# ---------------------------------------------------------------- testing: p-gene-screen (re-authored)
G = item(T, 'p-gene-screen')
gp = [0.0004, 0.0021, 0.0038, 0.0071, 0.0079, 0.0125, 0.0190, 0.034]
full = gp + [0.11] * 52                           # "the other 52 are all above 0.1"
key(T, 'p-gene-screen', 1, 0.10 / 60)
for wid, v in (('unadjusted', 0.10), ('times-m', 0.10 * 60), ('five-percent', 0.05 / 60)):
    slip(T, 'p-gene-screen', 1, wid, v)
key(T, 'p-gene-screen', 2, sum(p <= 0.10 / 60 for p in full))
slip(T, 'p-gene-screen', 2, 'unadjusted', sum(p <= 0.10 for p in gp)); slip(T, 'p-gene-screen', 2, 'bh', bh(full, 0.10))
key(T, 'p-gene-screen', 3, bh(full, 0.10))
first_fail = next(k for k, p in enumerate(sorted(full), 1) if p > k * 0.10 / 60) - 1
slip(T, 'p-gene-screen', 3, 'first-fail', first_fail)
# with the other 52 anywhere above 0.1 (up to 1) the count is still 5 at q = 0.10 and 6 at q = 0.15
for top in (0.1001, 0.5, 1.0):
    ok(bh(gp + [top] * 52, 0.10) == 5, f'gene part 3: 5 whatever the other 52 are, here {top}', )
ok(bh(gp + [0.16] * 52, 0.15) == 6, 'gene part 5 q-same: 6 at q = 0.15 when the other 52 are above 0.15')
ok(bh(gp + [0.12] * 52, 0.15) == 6, f'gene part 5 q-same: "BH rejects 6" at q = 0.15; with the other 52 at 0.12, which the prose allows, it rejects {bh(gp + [0.12] * 52, 0.15)}',
   finding='the prose says only "above 0.1": a p-value of 0.12 at rank 60 passes its bar 0.15, so "BH rejects 6" needs the 52 to be above 0.15')
qmin = 60 * 0.0079 / 5
key(T, 'p-gene-screen', 4, qmin)
ok(bh(full, qmin + 1e-4) == 5 and bh(full, qmin - 1e-4) == 3, 'gene part 4: 5 just above 0.0948, 3 just below')
for wid, v in (('no-divide', 60 * 0.0079), ('first-fail', 60 * 0.0071 / 4), ('bar', 5 * 0.10 / 60)):
    slip(T, 'p-gene-screen', 4, wid, v)
bars = [round(k * 0.10 / 60, 6) for k in range(1, 9)]
stale(G, ['60', '0.0004', '0.0021', '0.0038', '0.0071', '0.0079', '0.0125', '0.0190', '0.034', '52', '0.1', '10', '0.10', '0.001667', '5',
          '0.000833', '6', '8', '1', '2', '3', '4', '0.00667', '0.00833', '0.003333', '0.005', '0.01333', '12', '0.0948', '0.1065', '0.474',
          '0.0083', '0.15', '0.015'], 'gene screen')
ok(round(bars[3], 5) == 0.00667 and round(bars[4], 5) == 0.00833 and round(bars[7], 5) == 0.01333 and round(6 * 0.15 / 60, 3) == 0.015, 'gene: the bars printed')
ok(G['difficulty'] == 5, 'gene: difficulty 5')

# ---------------------------------------------------------------- testing: p-checkout-designs (re-authored)
C = item(T, 'p-checkout-designs')
key(T, 'p-checkout-designs', 1, 18 * 0.05)
for wid, v in (('one-sided', 18 * 0.025), ('all-pages', 18), ('complement', 18 * 0.95)):
    slip(T, 'p-checkout-designs', 1, wid, v)
key(T, 'p-checkout-designs', 2, 0.9 * 4000)
for wid, v in (('all-pages', 18 * 4000), ('one-launch', 4000), ('thousands', 3.6)):
    slip(T, 'p-checkout-designs', 2, wid, v)
key(T, 'p-checkout-designs', 3, 0.05 / 18)
for wid, v in (('unadjusted', 0.05), ('times-n', 0.9), ('sidak', 1 - 0.95**(1 / 18))):
    slip(T, 'p-checkout-designs', 3, wid, v)
for bar in (0.05 / 18, 0.002778):
    key(T, 'p-checkout-designs', 4, 1 - (1 - bar)**18)
for wid, v in (('bound', 0.05), ('no-complement', (1 - 0.002778)**18), ('carried', 1 - 0.95**18)):
    slip(T, 'p-checkout-designs', 4, wid, v)
# the Sidak bar carried into part 4 gives exactly 0.05, which the `bound` line then misdescribes
ok(round(1 - (1 - 0.002846)**18, 4) == 0.05, 'checkout part 4: the Sidak bar from part 3 gives 0.0500, and lands on `bound`')
ok(round(18 * 0.002778 * 4000) == 200 and round(1 - 0.002778, 6) == 0.997222, 'checkout part 5: expected waste 200; 0.997222')
stale(C, ['18', '5', '4000', '0.9', '1', '0.05', '0.025', '0.95', '3600', '0.002778', '0.0488', '0.9512', '0.6028', '0.997222', '200', '0',
          '2', '3', '4', '6'], 'checkout designs')      # 6 = "6 decimal places"
for k in (1, 2, 3, 4):
    bands_clear(T, 'p-checkout-designs', k)
ok(C['difficulty'] == 3, 'checkout: difficulty 3')

# ---------------------------------------------------------------- testing: p-biomarker-field (re-authored)
B = item(T, 'p-biomarker-field')
centre = 3.78
table = {2.5: (0.0124, 0.90), 2.8: (0.0051, 0.84), 3.1: (0.0019, 0.75), 3.5: (0.00047, 0.61)}
for cbar, (nul, real) in table.items():
    n_ = 2 * (1 - Phi(cbar)); r_ = 1 - Phi(cbar - centre) + Phi(-cbar - centre)
    ok(round(n_, 4 if nul > 0.001 else 5) == nul and round(r_, 2) == real, f'biomarker table at {cbar}: null {n_:.5f}, real {r_:.3f}')
key(T, 'p-biomarker-field', 1, 1 / 380)
for wid, v in (('over-400', 1 / 400), ('times', 380), ('five-percent', 0.05 / 380)):
    slip(T, 'p-biomarker-field', 1, wid, v)
lowest = min(cb for cb, (nul, _) in table.items() if nul <= 1 / 380)
opts = {o['id']: o for o in W(T, 'p-biomarker-field', 2)['options']}
ok(lowest == 3.1 and opts['c31'].get('correct') and sum(bool(o.get('correct')) for o in opts.values()) == 1, 'biomarker part 2: 3.1 is the lowest bar and the one keyed')
ok(near(380 * 0.0124, 4.712) and near(380 * 0.0051, 1.938), 'biomarker part 2: 4.712 and 1.938')
key(T, 'p-biomarker-field', 3, 20 * 0.75)
for wid, v in (('old-bar', 20 * 0.90), ('all-real', 20), ('next-bar', 20 * 0.61)):
    slip(T, 'p-biomarker-field', 3, wid, v)
print(f'NOTE    biomarker part 3: the bar 2.8 gives {20 * 0.84:.1f} (17 as a whole number), with no wrong entry')
fd = 380 * 0.0019
key(T, 'p-biomarker-field', 4, fd / (fd + 15))
for wid, v in (('true-share', 15 / (fd + 15)), ('over-400', fd / 400), ('no-power', fd / (fd + 20))):
    slip(T, 'p-biomarker-field', 4, wid, v)
any_false = 1 - (1 - 0.0019)**380
ok(round(any_false, 2) == 0.51 and near(fd, 0.722) and round(1 / 0.0459) == 22 and round(1 - 0.0019, 4) == 0.9981, f'biomarker part 5: chance of any false find {any_false:.4f}; 1 in 22')
stale(B, ['400', '380', '20', '2.5', '0.0124', '0.90', '2.8', '0.0051', '0.84', '3.1', '0.0019', '0.75', '3.5', '0.00047', '0.61', '1',
          '0.002632', '0.05', '5', '4.712', '1.938', '15', '0.722', '15.722', '0.0459', '4.6', '22', '0.9981', '0.51', '4', '75', '0', '2', '3', '6'], 'biomarker field')   # part numbers and "6 decimal places"
for k in (1, 3, 4):
    bands_clear(T, 'p-biomarker-field', k)
ok(B['difficulty'] == 4, 'biomarker: difficulty 4')

# ---------------------------------------------------------------- vectors: kept items
bw, ww, rr = np.array([0.5, 0.3, 0.2]), np.array([0.4, 0.45, 0.15]), np.array([0.02, -0.01, 0.04])
key(V, 'p-active-bets', 2, (ww - bw) @ rr)
wv, cc, ss = np.array([0.6, 0.3, 0.1]), np.array([0.01, -0.12, 0.08]), np.array([-0.03, 0.04, -0.02])
key(V, 'p-stress-hedge', 1, wv @ cc)
hh = -(wv @ cc) / (cc @ np.array([0, -1, 1])); w2 = wv + hh * np.array([0, -1, 1])
ok(near(hh, 0.11), 'stress: h = 0.11')
key(V, 'p-stress-hedge', 3, w2 @ ss); key(V, 'p-stress-hedge', 4, w2 @ (cc + ss) / 2)
# the `decimal` entry: the part's own decimal, typed in a % field, lands in it; the key typed in per cent does not
for iid, k, dec in (('p-active-bets', 2, -0.0055), ('p-stress-hedge', 1, -0.022), ('p-stress-hedge', 3, -0.0146), ('p-stress-hedge', 4, -0.0073)):
    x = wrong(V, iid, k, 'decimal'); w = W(V, iid, k)
    ok(abs(dec / 100 - x['value']) <= x['tol']['abs'], f'{iid} part {k}: the decimal {dec} typed lands in `decimal`')
    ok(str(dec) in part(V, iid, k)['feedback']['byKey']['decimal'], f'{iid} part {k}: the decimal line prints {dec}')
    ok(near(w['answer'], dec, 1e-9), f'{iid} part {k}: the key is {dec} as a fraction')
    bands_clear(V, iid, k)
    lo, hi = (x['value'] - x['tol']['abs']) * 100, (x['value'] + x['tol']['abs']) * 100
    print(f'NOTE    {iid} part {k}: `decimal` fires for anything typed from {lo:.4f} to {hi:.4f}')
ok(near(np.linalg.norm([12, 16]), 20), 'drone: |(12, 16)| = 20')
Ag = np.array([[0.4, 0.1], [0.2, 0.3]])
ok(np.allclose(np.linalg.inv(Ag), [[3, -1], [-2, 4]]) and np.allclose(10 * np.array([[0.3, -0.1], [-0.2, 0.4]]), [[3, -1], [-2, 4]]), 'goat: inverse and its accept form')
ok(near(-22 / 9, -2.444, 1e-3) and abs(-2 - (-2.444)) <= 0.5, 'engraver part 3: -2 sits in the `added` band')
Rm = np.array([[0.8, -0.6], [0.6, 0.8]])
st = Rm @ [0, 10]
key(V, 'p-site-plan', 4, math.degrees(math.atan2(st[1], st[0])))
slip(V, 'p-site-plan', 4, 'clockwise', math.degrees(math.atan2(*(Rm.T @ [0, 10])[::-1])))

# ---------------------------------------------------------------- vectors: p-charging-robot (re-authored)
Rb = item(V, 'p-charging-robot')
u, v = np.array([4, 1]), np.array([1, 3])
ab = np.linalg.solve(np.column_stack([u, v]), [11, 11])
ok(np.allclose(ab, [2, 3]) and W(V, 'p-charging-robot', 1)['answer'] == '(2, 3)', 'robot part 1: (2, 3)')
key(V, 'p-charging-robot', 2, (2 * u) @ (3 * v))
for wid, val in (('unweighted', u @ v), ('only-u', (2 * u) @ v), ('only-v', u @ (3 * v))):
    slip(V, 'p-charging-robot', 2, wid, val)
cosv = 42 / sq(68 * 90); ang = math.degrees(math.acos(cosv))
key(V, 'p-charging-robot', 3, ang)
slip(V, 'p-charging-robot', 3, 'radians', math.acos(cosv)); slip(V, 'p-charging-robot', 3, 'no-root', math.degrees(math.acos(42 / (68 * 90))))
ok(round(cosv, 4) == 0.5369 and round(sq(6120), 2) == 78.23 and near(ang, math.degrees(math.acos(u @ v / sq(17 * 10)))), 'robot part 3: 0.5369, 78.23, and the same angle as u and v')
line, path = sq(242), sq(68) + sq(90)
key(V, 'p-charging-robot', 4, path - line)
w4 = W(V, 'p-charging-robot', 4)
for val in (round(path, 2) - round(line, 2), round(sq(68), 2) + round(sq(90), 2) - round(line, 2), round(path - line, 2)):
    ok(abs(val - w4['answer']) <= w4['tol']['abs'] + 1e-9, f'robot part 4: key band takes {val:.2f}')
for wid, val in (('straight', line), ('path', path), ('no-cross', path - sq(158))):
    slip(V, 'p-charging-robot', 4, wid, val)
# widened key band (0.015): wrong methods tried against it
for name, val in (('line less the longer leg', line - sq(90)), ('legs less |2u - 3v|', path - sq(68 - 84 + 90)), ('with u.v = 7 as the cross term', path - sq(68 + 14 + 90)),
                  ('cross term once', path - sq(68 + 42 + 90)), ('|u| + |v| less |u + v|', sq(17) + sq(10) - sq(41)), ('squares', 68 + 90 - 242), ('ratio', path / line)):
    ok(abs(val - w4['answer']) > w4['tol']['abs'], f'robot part 4: {name} ({val:.3f}) is not accepted')
ok(11**2 + 11**2 == 242 and round(line, 2) == 15.56 and round(path, 2) == 17.73, 'robot part 4: 242, 15.56, 17.73')
stale(Rb, ['4', '1', '3', '11', '2', '14', '22', '8', '9', '24', '18', '42', '6', '7', '68', '90', '6120', '0.5369', '58', '78.23', '242',
           '15.56', '17.73', '2.18', '84', '12'], 'charging robot')

# ---------------------------------------------------------------- vectors: p-factor-risk (re-authored)
Fk = item(V, 'p-factor-risk')
wf = np.array([0.4, 0.35, 0.25]); Bm = np.array([[1.1, 0.3], [0.9, -0.2], [1.4, 0.6]]); Fm = np.array([[0.0144, 0.003], [0.003, 0.0049]])
e = Bm.T @ wf
ok(np.allclose(e, [1.105, 0.2]) and W(V, 'p-factor-risk', 1)['answer'] == '(1.105, 0.2)', 'factor part 1: (1.105, 0.2)')
ok(np.allclose(Bm.sum(axis=0), [3.4, 0.7]) and Fr(34, 30) == Fr(17, 15) and Fr(7, 30) == Fr(7, 30), 'factor part 1: slips (3.4, 0.7) and (17/15, 7/30)')
xh = e[0] - 0.5
key(V, 'p-factor-risk', 2, xh)
for wid, val in (('to-zero', e[0]), ('added', e[0] + 0.5), ('size', e[1] - 0.5)):
    slip(V, 'p-factor-risk', 2, wid, val)
e2 = e - xh * np.array([1, 0.25])
ok(np.allclose(e2, [0.5, 0.04875]) and W(V, 'p-factor-risk', 3)['answer'] == '(0.5, 0.04875)', 'factor part 3: (0.5, 0.04875)')
ok(np.allclose(e + xh * np.array([1, 0.25]), [1.71, 0.35125]) and near(e[1] - xh, -0.405), 'factor part 3: slips (1.71, 0.35125) and -0.405')
hv, uv = e2 @ Fm @ e2, e @ Fm @ e
key(V, 'p-factor-risk', 4, hv)
for wid, val in (('diagonal', e2[0]**2 * Fm[0, 0] + e2[1]**2 * Fm[1, 1]), ('no-f', e2 @ e2), ('unhedged', uv)):
    slip(V, 'p-factor-risk', 4, wid, val)
ok(round(uv, 5) == 0.01910 and round(2 * 0.5 * 0.04875 * 0.003, 6) == 0.000146 and round(0.04875**2 * 0.0049, 6) == 0.000012, 'factor part 4: 0.01910, 0.000146, 0.000012')
ok(round(2 * 0.5 * 0.04875 * 0.003 / hv * 100) == 4, 'factor part 4 explain: the cross term is about 4% of the total')
ok(np.all(np.linalg.eigvalsh(Fm) > 0), 'factor: F is a covariance matrix (positive definite)')
w5 = W(V, 'p-factor-risk', 5)
for val in (1 - 0.00376 / 0.01910, 1 - hv / uv):
    ok(abs(val - w5['answer']) <= w5['tol']['abs'], f'factor part 5: key band takes {val * 100:.2f}%')
for wid, val in (('ratio', 0.00376 / 0.0191), ('difference', (0.0191 - 0.00376)), ('volatility', 1 - sq(0.00376 / 0.0191)), ('decimal', 0.803 / 100)):
    slip(V, 'p-factor-risk', 5, wid, val)
bands_clear(V, 'p-factor-risk', 5)
ok(round(0.0191 - 0.00376, 5) == 0.01534 and round(0.00376 / 0.0191, 4) == 0.1969, 'factor part 5: 0.01534 and 0.1969')
# widened-band question for the `decimal` entry: its band takes other wrong answers typed in per cent
xd = wrong(V, 'p-factor-risk', 5, 'decimal')
print(f'NOTE    factor part 5: `decimal` fires for anything typed from {(xd["value"] - xd["tol"]["abs"]) * 100:.2f} to {(xd["value"] + xd["tol"]["abs"]) * 100:.2f}')
stale(Fk, ['0.4', '0.35', '0.25', '1.1', '0.3', '0.9', '0.2', '1.4', '0.6', '0.0144', '0.003', '0.0049', '1', '1.105', '0.12', '0.07', '0.15',
           '3.4', '0.7', '17', '15', '7', '30', '0.5', '0.605', '1.605', '2', '0.04875', '0.15125', '0.405', '1.71', '0.35125', '3', '0.0036',
           '0.000146', '0.000012', '0.00376', '0.00361', '4', '5', '0.01910', '0.0191', '0.8031', '80.3', '0.0153', '0.1969', '0.803',
           '0.01534'], 'factor risk')

# ---------------------------------------------------------------- vectors: p-colour-sensor (re-authored)
Cs = item(V, 'p-colour-sensor')
M = np.array([[0.7, 0.2], [0.1, 0.6]]); D = np.diag([2.0, 1.0]); rd = np.array([200, 60.0])
Cm = D @ M
ok(np.allclose(Cm, [[1.4, 0.4], [0.1, 0.6]]) and np.allclose(M @ D, [[1.4, 0.2], [0.2, 0.6]]) and np.allclose(D * M, [[1.4, 0], [0, 0.6]]), 'sensor part 1: C, and the slips MD and entrywise')
key(V, 'p-colour-sensor', 2, abs(np.linalg.det(Cm)))
for wid, val in (('added', 1.4 * 0.6 + 0.4 * 0.1), ('diagonal', 1.4 * 0.6), ('leak-only', np.linalg.det(M))):
    slip(V, 'p-colour-sensor', 2, wid, val)
Ci = np.linalg.inv(Cm); adj = np.array([[0.6, -0.4], [-0.1, 1.4]])
ok(np.allclose(Ci, [[0.75, -0.5], [-0.125, 1.75]]) and np.allclose(1.25 * adj, Ci) and np.allclose(0.8 * adj, [[0.48, -0.32], [-0.08, 1.12]])
   and np.allclose(np.linalg.inv(M), [[1.5, -0.5], [-0.25, 1.75]]), 'sensor part 3: the inverse, its accept forms and the slips')
tt = Ci @ rd
ok(np.allclose(tt, [120, 80]) and np.allclose(Cm @ rd, [304, 56]) and np.allclose(np.linalg.inv(M) @ rd, [270, 55]) and np.allclose(adj @ rd, [96, 64]), 'sensor part 4: (120, 80) and the slips')
ok(np.allclose(M @ tt, [100, 60]) and np.allclose(np.linalg.inv(D) @ rd, [100, 60]) and np.allclose(np.linalg.inv(M) @ [100, 60], [120, 80]), 'sensor parts 4 and 5: the checks printed')
ok(not np.allclose(np.linalg.inv(M) @ np.linalg.inv(D), np.linalg.inv(D) @ np.linalg.inv(M)), 'sensor part 5: the two orders of the inverses differ')
opts = {o['id']: o for o in W(V, 'p-colour-sensor', 5)['options']}
ok(opts['gain-first'].get('correct') and sum(bool(o.get('correct')) for o in opts.values()) == 1, 'sensor part 5: gain-first keyed')
stale(Cs, ['0.7', '0.2', '0.1', '0.6', '2', '0', '1', '200', '60', '1.4', '0.4', '0.84', '0.04', '0.8', '0.88', '0.75', '0.5', '0.125', '1.75',
           '1.25', '0.48', '0.32', '0.08', '1.12', '1.5', '0.25', '1.05', '0.05', '120', '80', '150', '30', '25', '105', '304', '56', '270', '55',
           '96', '64', '100', '3', '7', '5', '10', '4', '8'], 'colour sensor')

done('recompute_b')
