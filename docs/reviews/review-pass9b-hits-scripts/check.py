"""Recomputes every figure quoted in docs/reviews/review-pass9b-hits.md and asserts it.

Usage (repo root, venv Python): python docs/reviews/review-pass9b-hits-scripts/check.py
Reads the content files as they stand, so it also fails if a key or band named below has moved.
`within` copies app/js/engine/grade.js: |typed - value| <= tol.abs + 1e-9; a `%` field divides the typed number by 100.
"""
import json, math, os
from statistics import NormalDist

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'app', 'content', 'courses')
Phi = NormalDist().cdf


def part(f, i, p):
    d = json.load(open(os.path.join(ROOT, f + '.json'), encoding='utf-8'))
    return d['items'][i]['parts'][p]


def within(v, a, tol):
    return abs(v - a) <= tol + 1e-9


def key(f, i, p):
    w = part(f, i, p)['widget']
    return w['answer'], w['tol']['abs'], (100 if w.get('unit') == '%' else 1)


def takes(f, i, p, typed, tol=None):
    a, t, k = key(f, i, p)
    return within(typed / k, a, t if tol is None else tol)


def wrong(f, i, p, wid):
    x = [x for x in part(f, i, p)['widget']['wrong'] if x['id'] == wid][0]
    return x['value'], x['tol']['abs']


def fires(f, i, p, wid, typed, tol=None):
    """The slip line fires: the typed value misses the key and lands in the slip's band."""
    v, t = wrong(f, i, p, wid)
    k = key(f, i, p)[2]
    return (not takes(f, i, p, typed)) and within(typed / k, v, t if tol is None else tol)


# ---------------------------------------------------------------- [carry-band]
# exp-log/problems-3 p-savings-doubling part 4: both slips are exact means of whole pounds
f = 'exp-log/problems-3'
assert (2400 + 19200) / 2 == 10800 and (4800 + 9600) / 2 == 7200
assert fires(f, 0, 3, 'halfway-pounds', 10800) and fires(f, 0, 3, 'midpoint', 7200)
assert takes(f, 0, 3, 6788) and takes(f, 0, 3, 6787) and round(2400 * math.exp(0.055 * 18.9)) == 6787

# markov/problems-1 p-thin-book part 4: the printed carries give 6.67/10 and 3.33/10
f = 'markov/problems-1'
assert fires(f, 0, 3, 'swapped', round(6.67 / (6.67 + 3.33), 4)) and fires(f, 0, 3, 'swapped', 0.6667)
assert takes(f, 0, 3, round(3.33 / 10, 4)) and takes(f, 0, 3, 0.3333)
# p-carry-pause part 2: neither flagged slip uses the carried 3.33
assert round(0.95 / 1.65, 4) == 0.5758 and fires(f, 3, 1, 'stay-ratio', 0.5758)
assert round(20 / (20 + 1.43), 4) == 0.9333 == round(20 / (20 + 1 / 0.7), 4) and fires(f, 3, 1, 'used-stay', 0.9333)
assert takes(f, 3, 1, round(20 / 23.33, 4)) and fires(f, 3, 1, 'swapped', round(3.33 / 23.33, 4))
# [later-key] on the same part: 1/0.7 and the part 3 key 10/7 are one number by coincidence
assert abs(1 / 0.7 - 10 / 7) < 1e-12 and key(f, 3, 2)[0] == 1.4286

# estimation/problems-3 p-three-month-fund part 4: equal SEs divide to exactly 1
f = 'estimation/problems-3'
assert fires(f, 1, 3, 'same', 1.0) and takes(f, 1, 3, round(1.70 / 2.08, 3)) and takes(f, 1, 3, 0.816)
assert fires(f, 1, 3, 'inverted', round(2.08 / 1.70, 3)) and fires(f, 1, 3, 'squared', round((1.70 / 2.08) ** 2, 3))

# validation/problems-1 p-rent-seeds part 2
f = 'validation/problems-1'
for sd in (0.0468, 0.81 * math.sqrt(2 / 600)):
    assert fires(f, 3, 1, 'worst', round(0.81 + 1.766 * sd, 3)) and takes(f, 3, 1, round(0.81 - 1.766 * sd, 3))
for sd in (0.0209, 0.81 * math.sqrt(2 / 3000)):
    assert fires(f, 3, 1, 'carried', round(0.81 - 1.766 * sd, 3))
assert fires(f, 3, 1, 'worst', 0.8926) and fires(f, 3, 1, 'carried', 0.7731)

# arma/problems-1 p-gold-drift part 2: FAULT 1. The slip from the carried 4.55 misses its own band
f = 'arma/problems-1'
slip_carried, slip_own = round(4.55 / (110 / 500), 2), round(4.5455 / (110 / 500), 2)
assert (slip_carried, slip_own) == (20.68, 20.66)
assert not fires(f, 3, 1, 'no-sqrt', slip_carried) and fires(f, 3, 1, 'no-sqrt', slip_own)
assert fires(f, 3, 1, 'no-sqrt', slip_carried, 0.025) and fires(f, 3, 1, 'no-sqrt', slip_own, 0.025)
assert not within(20.63, 20.661, 0.025) and not within(20.69, 20.661, 0.025)
assert fires(f, 3, 1, 'sd', round(4.55 / 110, 4)) and takes(f, 3, 1, round(4.55 / 4.92, 2))

# garch/problems-1 p-stale-alarm part 3: the slip from the printed 19.2 is the stored value
f = 'garch/problems-1'
assert round(19.2 / 0.0027, 2) == 7111.11 and fires(f, 0, 2, 'percent', 7111.11) and fires(f, 0, 2, 'percent', 7111.1)
assert takes(f, 0, 2, round(19.2 / 0.27, 1))

# numerics/problems-2 p-vol-curve-extension part 5: the peak is flat, so 2.7639 for 2.763889 moves q by 1e-9
f = 'numerics/problems-2'
q = lambda u: 19.6 + 2.4 * u - 1.8 * u * u + 0.2 * u ** 3
assert abs(q(0.7639) - q(0.763889)) < 1e-8 and fires(f, 1, 4, 'peak', round(q(0.7639), 4))
assert takes(f, 1, 4, round(q(0.7639) - 20.4, 4))

# stat-models/problems-2 p-two-looks part 3
f = 'stat-models/problems-2'
for a, b in ((0.0107, 0.0313), (11 / 1024, 1 / 32)):
    assert round(1 - (1 - a) * (1 - b), 4) == 0.0417
assert fires(f, 2, 2, 'independent', 0.0417) and takes(f, 2, 2, 0.0420)

# ---------------------------------------------------------------- [band-edge]
def edge(f, i, p, right, neighbour, other, new_tol):
    """Today the band takes `right` and `neighbour` and refuses `other`; with new_tol it takes `right` only."""
    assert takes(f, i, p, right) and takes(f, i, p, neighbour) and not takes(f, i, p, other), (f, i, p)
    if new_tol is not None:
        assert takes(f, i, p, right, new_tol) and not takes(f, i, p, neighbour, new_tol) and not takes(f, i, p, other, new_tol), (f, i, p)

# faults 2 to 8: the neighbour has no honest route
assert round((1 / 0.975896 - 1) * 100, 2) == 2.47 == round((52000 / 50746.60 - 1) * 100, 2) == round(0.0241 / (1 - 0.0241) * 100, 2)
edge('ratio/problems-2', 3, 3, 2.47, 2.46, 2.48, 5e-05)
assert round(1 - 2 ** (-1 / 3), 4) == 0.2063 == round(1 - 0.7937, 4)
edge('analysis/problems-3', 2, 1, 0.2063, 0.2062, 0.2064, 5e-05)
assert round(-0.4237 + 0.6934, 4) == 0.2697 == round(-0.4237 + 3 ** (-1 / 3), 4) == round(1 - 2 ** (-1 / 3) - 4 ** (-1 / 3) + 3 ** (-1 / 3), 4)
edge('analysis/problems-3', 2, 3, 0.2697, 0.2698, 0.2696, 5e-05)
assert takes('analysis/problems-3', 2, 3, 0.26966, 5e-05) and takes('analysis/problems-3', 2, 3, 0.26974, 5e-05)
assert abs(1.96 * 0.6 * 4 - 4.704) < 1e-12
edge('arma/problems-3', 0, 2, 4.70, 4.71, 4.69, 5e-05)
assert abs(0.25 + 0.82 * (0.472 - 0.25) - 0.43204) < 1e-12
edge('arma/problems-3', 1, 2, 0.4320, 0.4321, 0.4319, 5e-05)
assert round(math.sqrt(22.38 / 8), 3) == 1.673 and abs(math.sqrt(2.7975) - 1.672573) < 1e-6
edge('garch/problems-1', 2, 0, 1.673, 1.672, 1.674, 5e-06)
assert takes('garch/problems-1', 2, 0, 1.6726, 5e-06)
assert round(0.855710 - 0.003656, 6) == 0.852054 == round(2 * 0.855710 - 0.859366, 6)
edge('numerics/problems-3', 2, 2, 0.85205, 0.85206, 0.85204, 5e-06)
assert takes('numerics/problems-3', 2, 2, 0.852054, 5e-06)
# no slip band of the seven parts meets the narrowed key band
for f, i, p, t in (('ratio/problems-2', 3, 3, 5e-05), ('analysis/problems-3', 2, 1, 5e-05), ('analysis/problems-3', 2, 3, 5e-05),
                   ('arma/problems-3', 0, 2, 5e-05), ('arma/problems-3', 1, 2, 5e-05), ('garch/problems-1', 2, 0, 5e-06),
                   ('numerics/problems-3', 2, 2, 5e-06)):
    a = key(f, i, p)[0]
    for x in part(f, i, p)['widget']['wrong']:
        assert abs(x['value'] - a) > t + x['tol']['abs'] + 1e-9

# stands: the neighbour is an honest answer and the edge is taken (grade.js adds 1e-9)
assert round(math.degrees(math.asin(0.733)), 1) == 47.1 and round(math.degrees(math.asin(45 * 0.8192 / 50.27)), 1) == 47.2
edge('trig/problems-1', 2, 2, 47.2, 47.1, 47.3, None)
assert round(0.5 * 5 * 3.142 + 1e-9, 2) == 7.86 and round(2.5 * math.pi, 2) == 7.85   # 7.855 with pi = 3.142, a tie rounded up
edge('vector-calc/problems-2', 1, 3, 7.85, 7.86, 7.84, None)
assert round(0.1 * (3.142 / 2) ** 2, 4) == 0.2468 and round(0.1 * (math.pi / 2) ** 2, 4) == 0.2467
edge('pdes/problems-2', 0, 0, 0.2467, 0.2468, 0.2466, None)

# ---------------------------------------------------------------- [later-key] coincidences
assert 0.44 ** 2 - 0.1936 < 1e-12 and key('arma/problems-2', 0, 2)[0] == 0.1936          # the square this part itself needs
assert 2 ** -3 == 0.125 == 2 * 2 ** -4 and key('topology/problems-3', 2, 1)[0] == 0.125  # a distance, not the gap bound
d = json.load(open(os.path.join(ROOT, 'numerics/problems-4.json'), encoding='utf-8'))
assert '276' in d['items'][2]['prose'] and math.gcd(76, math.gcd(92, 276)) == 4          # the stem prints 276

# ---------------------------------------------------------------- [slip-in-key-band]
f = 'number-sense/problems-2'
for typed in (0.2778, 0.27778, 0.277778):
    assert fires(f, 1, 2, 'unrounded', typed)
assert takes(f, 1, 2, 0.278) and not takes(f, 1, 2, 0.277) and fires(f, 1, 2, 'truncated', 0.277)
for typed in (2.833, 2.8333):
    assert fires(f, 2, 1, 'unrounded', typed)
assert takes(f, 2, 1, 2.83) and not takes(f, 2, 1, 2.84)

# ---------------------------------------------------------------- [shown-arithmetic]
# testing/homework-4 h-np-normal: FAULT 9
assert round((0.5 - 0.411) / 0.25, 3) == 0.356 and round((0.5 - 0.4113) / 0.25, 3) == 0.355
assert abs(1.645 / 4 - 0.41125) < 1e-12 and round(Phi(2 - 1.645), 4) == 0.6387 == round(Phi(0.355), 4)
# fin-ml/l11-deflated-sharpe screen 11: FAULT 10
g = 0.5772156649015329
inv = NormalDist().inv_cdf
sr = 2.1 / math.sqrt(252)
em = math.sqrt(1 / 503) * ((1 - g) * inv(1 - 1 / 40) + g * inv(1 - 1 / (40 * math.e)))
se = math.sqrt((1 + 0.5 * sr + (5 - 1) / 4 * sr ** 2) / 503)
assert (round(sr, 4), round(em, 4), round(em, 5), round(se, 4)) == (0.1323, 0.0976, 0.09762, 0.0464)
assert round((sr - em) / se, 3) == 0.747 and round(Phi((sr - em) / se), 3) == 0.772
assert round((0.1323 - 0.0976) / 0.0464, 3) == 0.748 and round(Phi(0.748), 3) == 0.773      # as printed today
assert round((0.1323 - 0.09762) / 0.0464, 3) == 0.747 and round(Phi(0.747), 3) == 0.772     # after the fix

print('review-pass9b-hits check: all assertions hold')
