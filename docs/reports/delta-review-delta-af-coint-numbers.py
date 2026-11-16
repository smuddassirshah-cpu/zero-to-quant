#!/usr/bin/env python3
"""Delta read AF, coint problem sets 1 to 3: the three re-authored problems and the changed parts.

Run with the scratchpad venv Python (numpy). Imports no earlier script. Paths come from __file__.

Routes of this reader's own: exact Fractions and a head count for the screen of pairs, a
simulation of the Engle-Granger statistic for the powers the stem supposes, a 200-day data set
built to have the stem's covariance matrix (SVD line, np.std of the spread) for the smelters,
a day-by-day fee accrual and a search for the long entry for the glassmakers, a simulated walk
for the paper mills, powers by repeated multiplication for the half-life lines.

Each numeric part's bands are rebuilt with the engine's rule (|x - a| <= tol + 1e-9, grade.js)
and fed what a learner types in the form the part asks for.

Exit code. A failing check of this script's own arithmetic exits 1. A check that fails because
the content is as the review describes prints a FINDING line and leaves the exit code at 0
(CI runs every script in docs/reports). A fixed finding prints "resolved".
"""
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COINT = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'coint')

checks = fails = findings = 0


def ok(cond, name):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', name)


def finding(n, still_there, name):
    global findings
    if still_there:
        findings += 1
        print(f'FINDING {n}: {name}')
    else:
        print(f'resolved {n}: {name}')


def item(n, iid):
    with open(os.path.join(COINT, f'problems-{n}.json'), encoding='utf-8') as fh:
        return next(it for it in json.load(fh)['items'] if it['id'] == iid)


def within(v, a, tol):
    return abs(v - a) <= tol + 1e-9


def texts(part):
    fb = part['feedback']
    out = [part['question'], fb['correct'], fb['generic'], part['explain']['text']] + list(fb.get('byKey', {}).values())
    for o in part['widget'].get('options', []):
        out += [o['text'], o.get('why', '')]
    return ' '.join(out)


def bands(name, part, key_typed, wrong_typed):
    """key_typed: values the key band must take. wrong_typed: id -> values that must reach that id."""
    w = part['widget']
    pct = w.get('unit') == '%'
    k = 100.0 if pct else 1.0
    a, tol = w['answer'], w['tol']['abs']
    for v in key_typed:
        ok(within(v / k, a, tol), f'{name}: key band takes {v}')
    ids = {x['id']: x for x in w.get('wrong', [])}
    ok(set(ids) == set(wrong_typed), f'{name}: wrong ids {sorted(ids)} all recomputed')
    for wid, vals in wrong_typed.items():
        if wid not in ids:
            continue
        x = ids[wid]
        for v in vals:
            ok(not within(v / k, a, tol), f'{name}: key refuses {wid} {v}')
            ok(within(v / k, x['value'], x['tol']['abs']), f'{name}: {wid} takes {v}')
            first = next((y['id'] for y in w['wrong'] if within(v / k, y['value'], y['tol']['abs'])), None)
            ok(first == wid, f'{name}: {v} routes to {wid}, not {first}')
        ok(wid in part['feedback']['byKey'], f'{name}: {wid} has its line')
    # no wrong band meets the key band
    for x in w.get('wrong', []):
        ok(abs(x['value'] - a) > tol + x['tol']['abs'] + 1e-9, f'{name}: {x["id"]} band clear of the key band')
    if pct:
        ok('percentage' in part['question'], f'{name}: the form says percentage')


def has(text, *needles):
    return all(n in text for n in needles)


def r(x, d):
    """Round half up, as a learner does."""
    q = 10 ** d
    return math.floor(abs(x) * q + 0.5 + 1e-12) / q * (1 if x >= 0 else -1)


# ---------------------------------------------------------------- p-screen-real-share (set 1)
PID = 'p-screen-real-share'
it = item(1, PID)
P = it['parts']
ok(has(it['prose'], '1,200', '36', '3%', '1,164', '0.40', '5%'), f'{PID}: stem numbers')
N, TIED = 1200, 36
UNTIED = N - TIED
ok(UNTIED == 1164 and F(TIED, N) == F(3, 100), f'{PID}: 1,164 untied and 3%')
real1 = TIED * F(40, 100)
false5 = UNTIED * F(5, 100)
ok(real1 == F(144, 10) and false5 == F(582, 10) and real1 + false5 == F(726, 10), f'{PID}: 14.4, 58.2, 72.6')
# head count by simulation: 20,000 screens
rng = np.random.default_rng(20261116)
tp = rng.binomial(TIED, 0.40, 20000)
fp = rng.binomial(UNTIED, 0.05, 20000)
ok(abs(tp.mean() - 14.4) < 0.1 and abs((tp + fp).mean() - 72.6) < 0.25, f'{PID}: simulated means {tp.mean():.2f}, {(tp + fp).mean():.2f}')
ok(abs(tp.sum() / (tp + fp).sum() - 14.4 / 72.6) < 0.003, f'{PID}: simulated real share')
bands(f'{PID} p1', P[0], [14.4], {'no-power': [36], 'miss-rate': [21.6], 'all-pairs': [480]})
ok(TIED * F(6, 10) == F(216, 10) and N * F(4, 10) == 480, f'{PID} p1: slips')
bands(f'{PID} p2', P[1], [72.6], {'all-untied': [74.4], 'false-only': [58.2], 'no-power': [94.2]})
ok(r(N * 0.05 + 14.4, 1) == 74.4 and r(36 + 58.2, 1) == 94.2, f'{PID} p2: slips')
s3 = float(real1 / (real1 + false5))
ok(r(100 * s3, 1) == 19.8, f'{PID} p3: 19.8%')
bands(f'{PID} p3', P[2], [19.8, 100 * s3, 19.83],
      {'all-untied': [r(100 * 14.4 / 74.4, 1)], 'power': [40], 'false-share': [r(100 * 58.2 / 72.6, 1)], 'over-false': [r(100 * 14.4 / 58.2, 1)]})
ok(r(100 * 14.4 / 74.4, 1) == 19.4 and r(100 * 58.2 / 72.6, 1) == 80.2 and r(100 * 14.4 / 58.2, 1) == 24.7, f'{PID} p3: 19.4, 80.2, 24.7')
ok(has(texts(P[2]), '19.4%', '80.2%', '32 to 1') and round(UNTIED / TIED) == 32, f'{PID} p3: printed numbers')
real4 = TIED * F(85, 100)
ok(real4 == F(306, 10) and real4 + false5 == F(888, 10), f'{PID} p4: 30.6 and 88.8')
s4 = float(real4 / (real4 + false5))
ok(r(100 * s4, 1) == 34.5, f'{PID} p4: 34.5%')
bands(f'{PID} p4', P[3], [34.5, 100 * s4, 34.46],
      {'power': [85], 'all-untied': [r(100 * 30.6 / 90.6, 1)], 'old-total': [r(100 * 30.6 / 72.6, 1)], 'false-share': [r(100 * 58.2 / 88.8, 1)]})
ok(r(100 * 30.6 / 90.6, 1) == 33.8 and r(100 * 30.6 / 72.6, 1) == 42.1 and r(100 * 58.2 / 88.8, 1) == 65.5, f'{PID} p4: 33.8, 42.1, 65.5')
ok(has(texts(P[3]), '33.8%', '42.1%', '65.5%', '88.8', '30.6') and 30.6 > 2 * 14.4, f'{PID} p4: printed numbers, "more than doubles"')
real5 = TIED * F(65, 100)
false1 = UNTIED * F(1, 100)
ok(real5 == F(234, 10) and false1 == F(1164, 100) and real5 + false1 == F(3504, 100), f'{PID} p5: 23.4, 11.64, 35.04')
s5 = float(real5 / (real5 + false1))
ok(r(100 * s5, 1) == 66.8, f'{PID} p5: 66.8%')
bands(f'{PID} p5', P[4], [66.8, 100 * s5, 66.78],
      {'old-power': [r(100 * 30.6 / (30.6 + 11.64), 1)], 'five-percent': [r(100 * 23.4 / (23.4 + 58.2), 1)], 'false-share': [r(100 * 11.64 / 35.04, 1)]})
ok(r(100 * 30.6 / 42.24, 1) == 72.4 and r(100 * 23.4 / 81.6, 1) == 28.7 and r(100 * 11.64 / 35.04, 1) == 33.2, f'{PID} p5: 72.4, 28.7, 33.2')
ok(has(texts(P[4]), '72.4%', '28.7%', '33.2%', '7.2', '46.56', '19.8%') and real4 - real5 == F(72, 10) and false5 - false1 == F(4656, 100), f'{PID} p5: printed numbers')
ok(abs(s5 - 2 / 3) < 0.01, f'{PID} p5: "two passes in three"')


# the supposed powers: Engle-Granger statistic by hand (levels fit with a constant, then the
# no-constant residual regression), against the course's -3.34 and -3.90
def eg(phi, T, n, seed):
    g = np.random.default_rng(seed)
    x = np.cumsum(g.standard_normal((n, T)), axis=1)
    e = g.standard_normal((n, T))
    if phi < 1:
        u = np.zeros((n, T))
        u[:, 0] = e[:, 0] / math.sqrt(1 - phi * phi)
        for t in range(1, T):
            u[:, t] = phi * u[:, t - 1] + e[:, t]
        y = x + u
    else:
        y = np.cumsum(e, axis=1)
    xc = x - x.mean(1, keepdims=True)
    yc = y - y.mean(1, keepdims=True)
    res = yc - ((xc * yc).sum(1) / (xc * xc).sum(1))[:, None] * xc
    lag, d = res[:, :-1], np.diff(res, axis=1)
    gam = (lag * d).sum(1) / (lag * lag).sum(1)
    s2 = ((d - gam[:, None] * lag) ** 2).sum(1) / (T - 2)
    return gam / np.sqrt(s2 / (lag * lag).sum(1))


null = eg(1.0, 504, 3000, 1)
ok(abs((null < -3.34).mean() - 0.05) < 0.015 and abs((null < -3.90).mean() - 0.01) < 0.007, f'{PID}: untied pairs pass 5% and 1% at those rates')
fast2, slow2 = eg(0.97, 504, 3000, 2), eg(0.99, 504, 3000, 3)
fast4, slow4 = eg(0.97, 1008, 3000, 4), eg(0.99, 1008, 3000, 5)
mix = lambda a, b, c: 0.8 * (a < c).mean() + 0.2 * (b < c).mean()
p2y, p4y, p4y1 = mix(fast2, slow2, -3.34), mix(fast4, slow4, -3.34), mix(fast4, slow4, -3.90)
print(f'power of a 80/20 mix of ties with phi 0.97 and 0.99: two years {p2y:.2f}, four years {p4y:.2f}, four years at 1% {p4y1:.2f} (stem supposes 0.40, 0.85, 0.65)')
ok(abs(p2y - 0.40) < 0.06 and abs(p4y - 0.85) < 0.06 and abs(p4y1 - 0.65) < 0.06, f'{PID}: the three supposed powers can hold together')
ok(P[3]['widget']['tol']['abs'] == 0.001 and abs(100 * s4 - 34.45) < 0.01, f'{PID} p4: wider band, the key sits 0.0095 points from a rounding tie (validator tight-band)')
finding(3, 'Compared with 34.5%' in P[4]['question'], f'{PID} p5: "Compared with 34.5% in part 4, what share" can be read as asking for the change, 32.3 points')
finding(4, 'caps the false passes per untied pair' in P[2]['explain']['text'], f'{PID} p3: the level fixes a chance per untied pair, it does not cap a count')

# ---------------------------------------------------------------- p-smelter-tls (set 2)
PID = 'p-smelter-tls'
it = item(2, PID)
P = it['parts']
ok(has(it['prose'], '6.25', '4.00', '4.60', '30.00', '22.00', '31.00', '200-day'), f'{PID}: stem numbers')
import re
m = re.search(r'\$y = £(\d+\.\d+)\$', it['prose'])
Y_TODAY = float(m.group(1))
S = np.array([[6.25, 4.60], [4.60, 4.00]])
ok(abs(S[0, 1] / math.sqrt(S[0, 0] * S[1, 1]) - 0.92) < 1e-12, f'{PID}: correlation 0.92')
# 200 days with exactly this sample covariance and these means
g = np.random.default_rng(7)
Z = g.standard_normal((200, 2))
Z -= Z.mean(0)
Lz = np.linalg.cholesky(np.cov(Z.T))
D = Z @ np.linalg.inv(Lz).T @ np.linalg.cholesky(S).T + np.array([30.0, 22.0])
ok(np.allclose(np.cov(D.T), S) and np.allclose(D.mean(0), [30, 22]), f'{PID}: built window has the stem covariance and means')
x, y = D[:, 0], D[:, 1]
sv = np.linalg.svd(D - D.mean(0), full_matrices=False)
lam = sv[1] ** 2 / 199
v = sv[2][0]
tls = v[1] / v[0]
ok(r(lam[0], 2) == 9.86 and r(lam[1], 2) == 0.39, f'{PID} p1: eigenvalues {lam[0]:.4f}, {lam[1]:.4f}')
ok(abs(lam[0] - (10.25 + math.sqrt(89.7025)) / 2) < 1e-9 and abs(10.25 ** 2 - 4 * 3.84 - 89.7025) < 1e-9 and abs(25 - 21.16 - 3.84) < 1e-12, f'{PID} p1: 10.25, 3.84, 89.7025')
nosq = (10.25 + math.sqrt(10.25 ** 2 - 4 * (25 - 4.60))) / 2
bands(f'{PID} p1', P[0], [9.86, lam[0]], {'smaller': [r(lam[1], 2)], 'trace': [10.25], 'no-square': [r(nosq, 2)]})
ok(has(texts(P[0]), '89.7025', '3.84', '10.25', '0.39'), f'{PID} p1: printed numbers')
ok(r(tls, 3) == 0.785 and r((9.86 - 6.25) / 4.60, 3) == 0.785, f'{PID} p2: TLS ratio {tls:.5f}, from 9.86 too')
# perpendicular distances: the TLS line beats the least squares line on them
perp = lambda b: (((y - 22) - b * (x - 30)) ** 2).sum() / (1 + b * b)
ols = S[0, 1] / S[0, 0]
ok(perp(tls) < perp(ols) and perp(tls) < perp(tls + 0.01) and perp(tls) < perp(tls - 0.01), f'{PID} p2: the ratio minimises perpendicular distance')
bands(f'{PID} p2', P[1], [0.785, tls], {'ols': [r(ols, 3)], 'other-ratio': [r(1 / tls, 3), r(1 / 0.785, 3)], 'smaller': [r(-1 / tls, 3), r((0.39 - 6.25) / 4.60, 3)]})
ok(r(ols, 3) == 0.736 and ols < tls < S[1, 1] / S[0, 1], f'{PID} p2: 0.736, and TLS lies between the two regressions')
ok(has(texts(P[1]), '3.61/4.60', '0.736', '1.274'), f'{PID} p2: printed numbers')
sd_tls = float(np.std(y - 0.785 * x, ddof=1))
sd_exact = float(np.std(y - tls * x, ddof=1))
ok(r(sd_tls, 3) == 0.793 and r(sd_exact, 3) == 0.793, f'{PID} p3: spread sd {sd_tls:.5f} ({sd_exact:.5f} unrounded)')
ok(abs(sd_exact ** 2 - lam[1] * (1 + tls * tls)) < 1e-9, f'{PID} p3: equals the small eigenvalue times 1 + b^2')
cross, sq = 2 * 0.785 * 4.60, 0.785 ** 2 * 6.25
ok(r(cross, 3) == 7.222 and r(sq, 3) == 3.851 and r(4 - cross + sq, 3) == 0.629, f'{PID} p3: 7.222, 3.851, 0.629')
bands(f'{PID} p3', P[2], [0.793, sd_tls, sd_exact, r(math.sqrt(0.629), 3)],
      {'variance': [0.629], 'no-cross': [r(math.sqrt(4 + sq), 3)], 'plus-cross': [r(math.sqrt(4 + cross + sq), 3)]})
sd_ols = float(np.std(y - ols * x, ddof=1))
ok(r(sd_ols, 3) == 0.784 and all(np.std(y - b * x, ddof=1) > sd_ols for b in (ols - 0.01, ols + 0.01, tls)), f'{PID} p3: least squares sd 0.784 is the minimum')
ok(0 < sd_tls - sd_ols < 0.01 and has(texts(P[2]), '0.784', 'under a penny', '7.222', '3.851'), f'{PID} p3: "under a penny" ({sd_tls - sd_ols:.4f})')
today = Y_TODAY - 0.785 * 31.00
mean = 22.00 - 0.785 * 30.00
z = (today - mean) / 0.793
ok(abs(mean + 1.55) < 1e-9 and abs(float(np.mean(y - 0.785 * x)) - mean) < 1e-9, f'{PID} p4: window mean of the spread -1.55')
zk = P[3]['widget']['answer']
ok(r(z, 2) == zk and r((today - mean) / sd_tls, 2) == zk and r((Y_TODAY - tls * 31 - (22 - tls * 30)) / sd_exact, 2) == zk, f'{PID} p4: z {z:.4f} gives the key {zk} by every route')
bands(f'{PID} p4', P[3], [r(z, 2)],
      {'no-mean': [r(today / 0.793, 2)], 'variance': [r((today - mean) / 0.629, 2), r((today - mean) / (sd_exact ** 2), 2)], 'no-hedge': [r((Y_TODAY - 22) / 0.793, 2)]})
ok(has(texts(P[3]), f'{today:.3f}', f'{today - mean:.3f}', '1.55', f'{zk:.2f}') and abs(zk) > 2, f'{PID} p4: printed numbers, beyond +2')
lz = item(2, 'p-lessor-window')['parts'][2]['widget']['answer']
finding(6, abs(abs(zk) - abs(lz)) < 1e-9, f'{PID} p4: key {zk} and p-lessor-window part 3 key {lz}, the next problem of the set, are the same number with the sign changed')

# ---------------------------------------------------------------- p-glassmaker-borrow (set 3)
PID = 'p-glassmaker-borrow'
it = item(3, PID)
P = it['parts']
ok(has(it['prose'], '1.15', '48.00', '36.00', '0.5%', '6%', '252', '21', '0.50'), f'{PID}: stem numbers')
BETA, PY, PX, RY, RX, YEAR, HOLD, UNIT = 1.15, 48.0, 36.0, 0.005, 0.06, 252, 21, 0.50
long_borrow = BETA * PX
bands(f'{PID} p1', P[0], [41.40], {'y-leg': [48], 'no-hedge': [36], 'hedge-on-y': [r(BETA * PY, 2)]})
ok(abs(long_borrow - 41.40) < 1e-9 and abs(BETA * PY - 55.2) < 1e-9, f'{PID} p1: 41.40 and 55.20')
accrue = lambda pounds, rate, days=HOLD, year=YEAR: sum(pounds * rate / year for _ in range(days))
fee_long = accrue(long_borrow, RX)
fee_short = accrue(PY, RY)
ok(r(fee_long, 3) == 0.207 and abs(fee_long - 0.207) < 1e-9, f'{PID} p2: 21 daily charges make {fee_long:.4f}')
bands(f'{PID} p2', P[1], [0.207],
      {'calendar-days': [r(accrue(long_borrow, RX, year=365), 3)], 'one-day': [r(accrue(long_borrow, RX, days=1), 3)], 'annual': [r(long_borrow * RX, 3)], 'y-rate': [r(accrue(long_borrow, RY), 3)]})
ok(abs(long_borrow * RX - 2.484) < 1e-9 and F(21, 252) == F(1, 12) and has(texts(P[1]), '2.484', '1/12'), f'{PID} p2: 2.484 and 1/12')
ok(abs(fee_short - 0.020) < 1e-9, f'{PID} p3: short fee {fee_short:.4f}')
gap = fee_long - fee_short
bands(f'{PID} p3', P[2], [0.187, gap], {'short-only': [0.020], 'sum': [r(fee_long + fee_short, 3)], 'x-rate-both': [r(fee_long - accrue(PY, RX), 3)]})
ok(r(gap, 3) == 0.187 and r(fee_long - accrue(PY, RX), 3) == -0.033, f'{PID} p3: 0.187 and -0.033')
ch = P[3]['widget']['options']
ok([o['id'] for o in ch if o.get('correct')] == ['flatters-long'] and has(ch[0]['text'], '0.207', '0.020'), f'{PID} p4: key option and its two fees')
ok(fee_long / fee_short > 10 and 'over ten times' in P[3]['feedback']['correct'], f'{PID} p4: {fee_long / fee_short:.2f} times')
short_net = 2 * UNIT - fee_short
ok(abs(short_net - 0.98) < 1e-9, f'{PID} p5: short nets 0.98')
# search the long entry on a grid of 0.001 of z
zs = np.arange(-4.0, 0.0, 0.001)
net = -zs * UNIT - fee_long
z_long = float(zs[np.argmin(np.abs(net - short_net))])
ok(abs(z_long + 2.374) < 1e-6, f'{PID} p5: grid search gives {z_long:.3f}')
bands(f'{PID} p5', P[4], [-2.37, -2.374], {'sign': [2.37], 'shift-only': [-0.37], 'pounds': [r(-2 - gap, 2)], 'wrong-way': [r(-2 + gap / UNIT, 2)]})
ok(has(texts(P[4]), '1.187', '0.98', '0.374') and abs(2.374 * UNIT - 1.187) < 1e-9, f'{PID} p5: printed numbers')
long_at_2 = 2 * UNIT - fee_long
ok(abs(long_at_2 - 0.793) < 1e-9, f'{PID} p5: a long from -2 nets 0.793')
finding(1, 'prices as fixed while a trade is open' in it['prose'], f'{PID}: the stem holds the prices fixed while a trade is open, and part 5 earns £1.00 from the spread moving')
finding(7, 'stock loan' not in it['prose'], f'{PID}: the fee is the stock loan fee of l10 screens[11] and the Markets course, and the stem does not say so')
finding(2, 'opens its longs too early' in P[4]['explain']['text'], f'{PID} p5: "opens its longs too early" is not shown; a long from -2 still nets £{long_at_2:.3f}')

# ---------------------------------------------------------------- changed parts of kept problems
# paper mills, part 1 (new key 0.0036) and part 2's question
PID = 'p-paper-mill-multiple'
it = item(1, PID)
P = it['parts']
ok(has(it['prose'], '£0.40', '0.75', '£0.50', '0.6', '0.15x_t + u_t') and 'AR(1)' not in json.dumps(it), f'{PID}: stem, and no AR(1) line left')
ok(F(15, 100) ** 2 * F(40, 100) ** 2 == F(36, 10000), f'{PID} p1: 0.0036')
g = np.random.default_rng(11)
steps = 0.15 * 0.40 * g.standard_normal(400000)
ok(abs(steps.var() - 0.0036) < 0.00005, f'{PID} p1: simulated daily variance {steps.var():.5f}')
bands(f'{PID} p1', P[0], [0.0036], {'sd-not-squared': [0.15 ** 2 * 0.40], 'multiple-not-squared': [0.15 * 0.16], 'neither-squared': [0.15 * 0.40]})
ok(has(texts(P[0]), '0.0225', '0.16', '0.0036', '£0.06'), f'{PID} p1: printed numbers')
walk = 0.15 * np.cumsum(0.40 * g.standard_normal((20000, 500)), axis=1)[:, -1] + 0.50 * g.standard_normal(20000)
ok(abs(walk.std() - math.sqrt(0.0036 * 500 + 0.25)) < 0.03 and r(math.sqrt(2.05), 2) == P[1]['widget']['answer'], f'{PID} p2: day 500 sd {walk.std():.3f}, key 1.43')
ok(has(P[1]['question'], '0.0036', '0.50^2 = 0.25', '2 decimal places'), f'{PID} p2: question restates part 1')
ok(math.floor(0.75 / 0.0036) + 1 == P[2]['widget']['answer'] == 209, f'{PID} p3: day 209 still follows')
finding(5, 'one day adds an sd of' in P[0]['explain']['text'], f'{PID} p1: "one day adds an sd of £0.06": sds do not add, variances do')

# cocoa: part 1 lines, part 3 question, part 4 key option
PID = 'p-cocoa-chip-levels'
P = item(1, PID)['parts']
t750 = 0.45 * math.sqrt(748 / (1 - 0.45 ** 2))
t1500 = 0.45 * math.sqrt(1498 / (1 - 0.45 ** 2))
ok(r(t750, 2) == 13.78 and r(math.sqrt(748 / 0.7975), 2) == 30.63 and abs(1 - 0.45 ** 2 - 0.7975) < 1e-12, f'{PID} p1: 13.78, 30.63, 0.7975')
ok(7 <= t750 / 1.96 < 7.5 and 'seven times over' in P[0]['explain']['text'], f'{PID} p1: {t750 / 1.96:.2f} times 1.96')
ok(r(t1500, 2) == 19.5 and r(13.78 * math.sqrt(1498 / 748), 2) == 19.5 and within(13.78 * math.sqrt(1498 / 748), P[2]['widget']['answer'], P[2]['widget']['tol']['abs']), f'{PID} p3: 19.50 from the restated 13.78')
ok(has(P[2]['question'], '13.78', '750 days'), f'{PID} p3: question restates part 1')
key4 = next(o for o in P[3]['widget']['options'] if o.get('correct'))
ok(key4['text'].startswith('No evidence of a tie') and 'No tie' not in P[3]['feedback']['correct'] and 'no evidence of a tie' in P[3]['explain']['text'], f'{PID} p4: key no longer claims there is no tie')
ok(-2.41 > -3.04 > -3.34 > -3.90, f'{PID} p4: -2.41 above every value')

# lessor: part 1 lines, part 3 lines
PID = 'p-lessor-window'
P = item(2, PID)['parts']
p8 = p9 = 1.0
for _ in range(8):
    p8 *= 0.92
p9 = p8 * 0.92
ok(r(p8, 3) == 0.513 and r(p9, 3) == 0.472 and p9 < 0.5 < p8, f'{PID} p1: 0.513 and 0.472 straddle a half')
ok(has(texts(P[0]), '0.513', '0.472', '12.5 is $1/0.08$') and abs(1 / 0.08 - 12.5) < 1e-12 and r(math.log(0.5) / math.log(0.92), 2) == 8.31, f'{PID} p1: printed numbers')
ok(r((-0.18 - 0.62) / 0.35, 2) == -2.29 and has(texts(P[2]), '-0.18 - 0.62', '-£0.80'), f'{PID} p3: -2.29')

# three distributors: part 1 lines, part 4 line
PID = 'p-three-distributors'
P = item(2, PID)['parts']
ok(abs(41.7 - 29.80 - 11.9) < 1e-9 and abs(15.49 - 9.8 - 5.69) < 1e-9 and has(texts(P[0]), '11.9', '5.69'), f'{PID} p1: 11.9 and 5.69')
rank = 0
for stat, crit in ((41.7, 29.80), (9.8, 15.49), (1.6, 3.84)):
    if stat > crit:
        rank += 1
    else:
        break
ok(rank == P[0]['widget']['answer'] == 1, f'{PID} p1: rank 1')
ok(has(P[3]['feedback']['byKey']['no-mean'], '£2.35', '£2.05') and r(2.35 / 0.20, 2) == 11.75, f'{PID} p4: no-mean line')

# tyres: part 1 lines, part 3 line
PID = 'p-tyre-vecm'
P = item(2, PID)['parts']
ok(abs(-0.06 * 1.50 + 0.09) < 1e-12 and abs(0.02 * 1.50 - 0.03) < 1e-12 and has(texts(P[0]), '£0.03', '6%', '£0.09'), f'{PID} p1: -0.09, 0.03')
ok(r(1 / 0.09, 2) == 11.11 and r(math.log(0.5) / math.log(0.91), 2) == 7.35 and '11.11 is $1/0.09$' in P[2]['feedback']['byKey']['one-over-b'], f'{PID} p3: 11.11 and 7.35')

# housebuilders: part 3 lines, part 4 question and band
PID = 'p-housebuilder-trading-years'
P = item(3, PID)['parts']
se = 1 / math.sqrt(504 / 252)
ok(r(se, 3) == 0.707 and r(1.08 / se, 2) == 1.53 and r(1.08 / 0.707, 2) == 1.53, f'{PID} p3: 0.707 and 1.53')
bands(f'{PID} p3', P[2], [1.53, 1.08 / se], {'times-t': [2.16], 'divided': [r(1.08 * 0.707, 2)], 'all-years': [r(1.08 * math.sqrt(6), 2)]})
ok(has(texts(P[2]), '2.16', '0.76', '2.65', '0.707') and r(1.08 * 0.707, 2) == 0.76 and r(1.08 * math.sqrt(6), 2) == 2.65, f'{PID} p3: printed numbers')
T = (2 / 1.08) ** 2
bands(f'{PID} p4', P[3], [3.43, T, 3.42, r(1.85 ** 2, 2), r(1.852 ** 2, 2)], {'no-square': [r(2 / 1.08, 2)], 'inverted': [r((1.08 / 2) ** 2, 2)], 'four-over': [r(4 / 1.08, 2)]})
ok(r(T, 2) == 3.43 and 'that ratio' in P[3]['question'], f'{PID} p4: 3.43; the question follows part 3')
ok(math.ceil(T * 252) - 504 == P[4]['widget']['answer'] or math.ceil(3.43 * 252 - 504) == P[4]['widget']['answer'], f'{PID} p5: the days still follow')

print(f'{checks} checks, {fails} failed, {findings} FINDING rows (findings do not change the exit code)')
sys.exit(1 if fails else 0)
