"""Recomputation behind docs/reviews/review-pass9-hits.md.

Part A recomputes each of the 63 slips flagged by `[rounding-tie]` from the figures of
its own part, rounds it as the question asks, and asserts that the learner's typed value
lands on the slip's own feedback line (key band first, then `wrong` in order).
Part B recomputes the nine keys flagged as near a tie and types the answers a learner
reaches with sensibly rounded intermediate values.
Part C checks the fixes proposed in the review: new bands, new figures.

Usage (from the repo root): python docs/reviews/review-pass9-hits-scripts/check.py
Exits non-zero on any failed assertion.
"""
import json, re, os
from math import sqrt, log, exp, pi, erf, comb, floor

ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..')
EPS = 1e-9


def Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def load(f):
    return json.load(open(os.path.join(ROOT, 'app/content/courses', f), encoding='utf-8'))


def widget(f, pid, part):
    it = [i for i in load(f)['items'] if i.get('id') == pid][0]
    return it['parts'][part - 1]['widget']


def inside(c, tol, v):
    return abs(v - c) <= tol + EPS * max(1, abs(v))


def taker(w, v, key_tol=None):
    if inside(w['answer'], w['tol']['abs'] if key_tol is None else key_tol, v):
        return 'KEY'
    for x in w.get('wrong', []):
        if isinstance(x.get('value'), (int, float)) and inside(x['value'], x.get('tol', {}).get('abs', 0), v):
            return x['id']
    return 'generic'


def rnd(v, step):
    """Round half away from zero to a multiple of step."""
    q = abs(v) / step
    n = floor(q + 0.5 + 1e-9)
    return round((1 if v >= 0 else -1) * n * step, 10)


# ---------------------------------------------------------------- Part A: the 63 slips
SLIPS = {
    ('arma/problems-2', 'p-trust-discount', 'constant'): 1.38,
    ('coint/problems-2', 'p-smelter-tls', 'variance'): 4.00 - 2 * 0.785 * 4.60 + 0.785 ** 2 * 6.25,
    ('coint/problems-3', 'p-glassmaker-borrow', 'y-rate'): 41.40 * 0.005 / 12,
    ('coint/problems-3', 'p-glassmaker-borrow', 'sign'): 2 + 0.187 / 0.5,
    ('coint/problems-3', 'p-glassmaker-borrow', 'shift-only'): -0.187 / 0.5,
    ('coint/problems-3', 'p-glassmaker-borrow', 'pounds'): -2 - 0.187,
    ('coint/problems-3', 'p-glassmaker-borrow', 'wrong-way'): -2 + 0.187 / 0.5,
    ('conditional/problems-3', 'p-three-loans', 'reciprocal'): 0.001 / 0.005536,
    ('conditional/problems-5', 'p-doubling-desk', 'unweighted'): -0.5299 * 20,
    ('convex/problems-4', 'p-variance-log', 'ratio'): 0.0735 / 0.096,
    ('convex/problems-4', 'p-variance-log', 'one-minus'): 1 - 0.0735 / 0.096,
    ('counting/problems-2', 'p-balloon-blocks', 'carried'): 540 / 1260,
    ('counting/problems-2', 'p-balloon-blocks', 'os-only'): 900 / 1260,
    ('counting/problems-2', 'p-quiz-team', 'girl-only'): 325 / 330,
    ('counting/problems-2', 'p-quiz-team', 'bottom'): 310 / 325,
    ('counting/problems-2', 'p-quiz-team', 'carried'): 305 / 330,
    ('counting/problems-2', 'p-signal-flags', 'together'): 30 / 105,
    ('counting/problems-2', 'p-signal-flags', 'carried'): 45 / 105,
    ('counting/problems-3', 'p-sail-ring', 'third'): 1 / 3,
    ('eigen/problems-1', 'p-garden-path', 'sign'): 0.6 * 3 ** 10 - 0.4 * 2 ** 10,
    ('eigen/problems-3', 'p-site-anomalies', 'unsquared'): (30 + 15 + 6 + 3) / 30,
    ('equations/problems-2', 'p-interest-split', 'rhs'): (780000 - 660) / 25,
    ('estimation/problems-1', 'p-reference-mass', 'carried-72'): 2 / sqrt(72 / 5),
    ('estimation/problems-1', 'p-reference-mass', 'no-root'): 2 / (76 / 5),
    ('estimation/problems-2', 'p-tank-sensor', 'sd-not-squared'): 51 + sqrt(2 * log(10)),
    ('estimation/problems-3', 'p-email-clicks', 'ninety'): 0.16 - 1.645 * 0.0150,
    ('estimation/problems-3', 'p-email-clicks', 'upper'): 0.16 + 1.96 * 0.0150,
    ('estimation/problems-3', 'p-routing-test', 'added-se'): 0.8 - 1.96 * 0.65,
    ('exp-log/problems-1', 'p-rare-coin', 'mid-value'): (1600 + 3936.60) / 2,
    ('functions/problems-1', 'p-sapling-log', 'no-c'): 72 / 5,
    ('ito/problems-4', 'p-band-wait', 'squared-level'): 4000 / 50 ** 2,
    ('least-squares/problems-2', 'p-power-line', 'total'): sqrt(45),
    ('least-squares/problems-3', 'p-gas-hubs', 'ratio'): 5 / 7.5,
    ('limits/problems-5', 'p-camera-pan', 'half-sweep'): pi / 12,
    ('limits/problems-5', 'p-camera-pan', 'per-metre'): pi / 120,
    ('markov/problems-3', 'p-stake-size', 'hundreds'): 1000 * 0.5026 - 600,
    ('markov/problems-5', 'p-cash-machine', 'four-hours'): sqrt(48 * 2950),
    ('measure-prob/problems-1', 'p-no-double-four', 'square'): 0.981 ** 2,
    ('measure-prob/problems-2', 'p-boom-bust', 'one-day'): 10 * 0.9 ** 100,
    ('measure-prob/problems-2', 'p-boom-bust', 'no-root'): 0.9 ** 100 / (1 - sqrt(0.9)),
    ('measure-prob/problems-2', 'p-compounding', 'no-phi'): 2 * exp(0.125),
    ('measure-prob/problems-4', 'p-premium-weight', 'cash-once'): 40 * 1.01 - 40 * 1.06 ** 2,
    ('pdes/problems-1', 'p-two-level-bar', 'no-base'): 60 * 0.8971,
    ('pdes/problems-2', 'p-grid-modes', 'absolute'): 0.3012 - 0.298,
    ('ratio/problems-1', 'p-pension-split', 'old-total'): 4140 / 9600,
    ('ratio/problems-1', 'p-pension-split', 'bonds-base'): 4140 / 5760,
    ('regression/problems-2', 'p-freight-summary', 'carried'): 0.85 / 3.24,
    ('regression/problems-2', 'p-sunny-cones', 'carried-n'): 2.4 / 1.414,
    ('regression/problems-3', 'p-overlap-signal', 'no-root'): 0.21 / 0.0036,
    ('stat-models/problems-3', 'p-spread-day-tail', 'classic-normal'): 0.1135 / Phi((-4 - 0.9375) / 4.0306),
    ('stat-models/problems-4', 'p-quality-six-markets', 'divisor-5'): 2.76 / 5,
    ('stat-models/problems-4', 'p-quality-six-markets', 'from-divisor-5'): 2.76 / 5 - 0.25,
    ('testing/problems-3', 'p-checkout-designs', 'thousands'): 0.9 * 4,
    ('testing/problems-4', 'p-website-signups', 'sd'): sqrt(0.375),
    ('validation/problems-1', 'p-rent-seeds', 'worst'): 0.81 + 1.766 * 0.0468,
    ('validation/problems-1', 'p-rent-seeds', 'by-best'): (0.81 - 0.727) / 0.727,
    ('validation/problems-1', 'p-van-prices', 'ddof-one'): sqrt(0.1106 / 4),
    ('validation/problems-2', 'p-spread-blocks', 'by-purged'): (4.62 - 3.85) / 4.62,
    ('validation/problems-3', 'p-closed-funds', 'survivors'): 8.4 / 9,
    ('validation/problems-3', 'p-closed-funds', 'added'): (8.4 + 2.52) / 9,
    ('validation/problems-3', 'p-closed-funds', 'whole-gap'): (8.4 - 14.0) / 9,
    ('validation/problems-3', 'p-closed-funds', 'note'): 1.16 / sqrt(7),
    ('vectors/problems-1', 'p-drone-crosswind', 'swapped'): -8 * 0.8 + 1 * 0.6,
}

n = 0
lines = []
for line in open(os.path.join(ROOT, 'docs/reports/engine-pass-9-hits.md'), encoding='utf-8'):
    m = re.match(r'- \[rounding-tie\] courses/(\S+)\.json \| (\S+) \| part (\d+) \| wrong "([^"]+)" \(([-\d.e]+)\) .*roundings \(([-\d.e]+), ([-\d.e]+)\)', line)
    if not m:
        continue
    f, pid, part, wid, val, r1, r2 = m.groups()
    val, step = float(val), abs(float(r1) - float(r2))
    slip = SLIPS[(f, pid, wid)]
    w = widget(f + '.json', pid, int(part))
    typed = rnd(slip, step)
    t_typed, t_raw = taker(w, typed), taker(w, slip)
    assert t_typed == wid, (f, pid, wid, slip, typed, t_typed)
    assert t_raw == wid, (f, pid, wid, slip, t_raw)
    lines.append(f'{f} | {pid} | part {part} | {wid} | slip {slip:.6g} | typed {typed:.6g} -> {t_typed}')
    n += 1
assert n == 63 == len(SLIPS), n
print('A: 63 slips recomputed; each, rounded as asked and unrounded, lands on its own line')
if os.environ.get('LIST'):
    print('\n'.join(lines))

# ---------------------------------------------------------------- Part B: the 9 keys
def key_case(f, pid, part, true, typed_ok, typed_other, scale=1.0, new_tol=None):
    """typed values are as the learner types them; scale 0.01 for a percentage box."""
    w = widget(f, pid, part)
    assert abs(true * scale - w['answer']) <= w['tol']['abs'], (pid, true * scale, w['answer'])
    out = []
    for v in typed_ok:
        assert taker(w, v * scale) == 'KEY', (pid, v)
    for v in typed_other:
        now = taker(w, v * scale)
        after = taker(w, v * scale, new_tol) if new_tol is not None else now
        out.append((v, now, after))
    return out


# convex/problems-3 p-style-fit part 5: sqrt(11/12) per cent, 3 places
r = key_case('convex/problems-3.json', 'p-style-fit', 5, sqrt(11 / 12), [0.957, rnd(sqrt(0.9167), 0.001)], [rnd(sqrt(0.917), 0.001), 0.956, 0.959], 0.01, 6e-6)
assert r == [(0.958, 'generic', 'KEY'), (0.956, 'generic', 'generic'), (0.959, 'generic', 'generic')], r
# exp-log/problems-3 p-log-chart-line part 1: ln 9 / 8 as a percentage, 2 places
assert abs(log(9) / 8 - 0.274653) < 1e-6 and abs(2.1972 / 8 - 0.27465) < 1e-12
r = key_case('exp-log/problems-3.json', 'p-log-chart-line', 1, 100 * log(9) / 8, [27.47], [rnd(100 * 2.197 / 8, 0.01), 27.45, 27.48], 0.01, 6e-5)
assert r == [(27.46, 'generic', 'KEY'), (27.45, 'generic', 'generic'), (27.48, 'generic', 'generic')], r
# ito/problems-2 p-cable-inverse part 3: e^0.0432, 4 places; the two means to 4 places multiply to 1.0442
ex, ey = round(1.25 * exp(0.06), 4), round(0.8 * exp(-0.0168), 4)
assert (ex, ey) == (1.3273, 0.7867) and rnd(ex * ey, 0.0001) == rnd(1.0442, 0.0001)
r = key_case('ito/problems-2.json', 'p-cable-inverse', 3, exp(0.0432), [1.0441], [1.0442, 1.0440, 1.0443], 1.0, 6e-5)
assert r == [(1.0442, 'generic', 'KEY'), (1.044, 'generic', 'generic'), (1.0443, 'generic', 'generic')], r
# validation/problems-3 p-carry-lookbacks part 1: 1/sqrt 6, 4 places; sqrt 6 = 2.449 gives 0.4083
assert rnd(1 / 2.449, 0.0001) == rnd(0.4083, 0.0001) and rnd(1 / 2.4495, 0.0001) == rnd(0.4082, 0.0001)
r = key_case('validation/problems-3.json', 'p-carry-lookbacks', 1, 1 / sqrt(6), [0.4082], [0.4083, 0.4081, 0.4084], 1.0, 6e-5)
assert r == [(0.4083, 'generic', 'KEY'), (0.4081, 'generic', 'generic'), (0.4084, 'generic', 'generic')], r
# the five that stand: every sensible working lands on the keyed rounding
key_case('markov/problems-4.json', 'p-taxi-rank', 4, 96 * 8 / 65, [11.82, rnd(96 * 0.1231, 0.01)], [])
key_case('markov/problems-5.json', 'p-signal-trial', 5, -1219.51, [-1220, rnd(-200 * 6.10, 1), rnd(4000 * 0.478 - 6000 * 0.522, 1)], [])
key_case('markov/problems-5.json', 'p-two-loss-cut', 2, 130 / 9, [14.44, rnd(11.11 + 3.33, 0.01), rnd(11.111 + 3.333, 0.01)], [])
key_case('number-sense/problems-4.json', 'p-cycle-commute', 5, 20000 / 3600, [5.56, rnd(20 / 3.6, 0.01)], [])
key_case('random-vars/problems-2.json', 'p-reversal-days', 5, 45.6 / 9.88, [4.62], [])
print('B: 9 keys recomputed; 4 refuse a sensibly rounded working and take it at the new band; 5 stand')

# ---------------------------------------------------------------- Part C: other fixes
# validation/problems-1 p-rent-seeds part 1 ([working-band])
w = widget('validation/problems-1.json', 'p-rent-seeds', 1)
true = 0.81 * sqrt(2 / 600)
assert abs(true - w['answer']) < 1e-6
assert rnd(0.81 * 0.0577, 0.0001) == rnd(0.0467, 0.0001) and taker(w, 0.0467) == 'generic'
assert rnd(0.81 * 0.05774, 0.0001) == rnd(0.0468, 0.0001) and abs(sqrt(2 / 600) - 0.05774) < 5e-6
assert [taker(w, v, 7e-5) for v in (0.0467, 0.0468, 0.0466, 0.0469)] == ['KEY', 'KEY', 'generic', 'generic']
# the three [working-band] hits that stand are ceilings
assert (3.34 * 0.1990 / 0.02) ** 2 > 1104 and (3.34 * sqrt(0.0396) / 0.02) ** 2 < 1105
assert 321 < 0.75 * (0.09 * 4761 + 0.03) < 322
assert 3898 < 2 * (1.766 / 0.04) ** 2 < 3899
# limits-thm/problems-2 p-digital-share part 3 ([key-in-question])
assert abs(log(84.95 / 80) - 0.06) < 1e-4
assert round(Phi(0.15), 4) == 0.5596 and round(Phi(0.2), 4) == 0.5793 and round(1 - Phi(0.15), 4) == 0.4404
w = widget('limits-thm/problems-2.json', 'p-digital-share', 3)
assert taker(w, 0.5793) == 'generic'
# markov/problems-3 p-barrier-note part 2 ([key-in-question])
assert (comb(12, 4), comb(12, 5), comb(12, 3)) == (495, 792, 220)
# the [key-in-question] choices that stand
assert round(Phi(2.25 - 1.645), 4) == 0.7274 and round(Phi(2.25 * sqrt(2) - 1.645), 4) == 0.9379
assert abs(0.3978 / sqrt(1 / (1 / 0.25 + 1 / 0.21)) - 1.1776) < 2e-3
assert 200 * 9.849 < 1000 + 300 * 3.3 and 200 * 10.556 > 1000 + 300 * 3.4
assert abs(0.65 ** 12 / 0.65 ** 6 - 0.0754) < 1e-4 and abs(0.2 * (2 / 3) / 0.2 - 0.6667) < 1e-4
print('C: fixes and standing cases check')
