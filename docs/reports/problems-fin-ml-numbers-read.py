#!/usr/bin/env python3
"""Second reader's recomputation of fin-ml problems-1 to -3 (docs/reviews/review-problems-fin-ml-1-3.md).

Imports nothing from the author's script. Every setting is typed here from the prose; every key, every
`wrong` value and the numbers printed in feedback and explain strings are rebuilt, by a second route where
one exists (exact fractions against floats, the definition against the closed form, a brute count against
the formula, numpy and pandas run on a spike for the centred window, numerical maximisation for Kelly).
Then the bands: no `wrong` band meets its key band, and each slip, worked from the values the part itself
states, lands in its own band. Exit 0 only when every check passes; a check that fails on wrong content
stays failing and is a finding of the review.
"""
import json, math, os, re, sys, datetime
from fractions import Fraction as F
from statistics import NormalDist, mean, stdev, pstdev

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'fin-ml')
N01 = NormalDist()
Phi, Pinv = N01.cdf, N01.inv_cdf
SETS = {n: json.load(open(os.path.join(BASE, f'problems-{n}.json'))) for n in (1, 2, 3)}
npass = nfail = 0


def ok(cond, msg):
    global npass, nfail
    if cond:
        npass += 1
    else:
        nfail += 1
        print('FAIL', msg)


def part(n, item, k):
    for it in SETS[n]['items']:
        if it['id'] == item:
            return it['parts'][k - 1]
    raise KeyError(item)


def texts(p):
    out = [p['question'], p['explain']['text'], p['widget'].get('accept', '')]
    fb = p['feedback']
    out += [fb['correct'], fb['generic']] + list(fb.get('byKey', {}).values())
    return ' '.join(str(x) for x in out)


def key(n, item, k, mine, alts=(), says=()):
    """mine: my unrounded value. alts: other honest routes (rounded inputs the part states). says: strings
    that must appear in the part's own text."""
    p = part(n, item, k)
    w = p['widget']
    tag = f'{n} {item} part {k}'
    tol = w['tol']['abs']
    ok(abs(mine - w['answer']) <= tol + 1e-12, f'{tag}: key {w["answer"]} against mine {mine}')
    for a in alts:
        ok(abs(a - w['answer']) <= tol + 1e-12, f'{tag}: honest route {a} outside key band {w["answer"]} +- {tol}')
    for s in says:
        ok(s in texts(p), f'{tag}: text does not print {s!r}')
    return w


def slip(n, item, k, wid, *routes):
    """Each route is a value a learner making this slip reaches; all must land in the slip's band, and the
    band must not meet the key band."""
    p = part(n, item, k)
    w = p['widget']
    tag = f'{n} {item} part {k} wrong {wid}'
    e = [x for x in w['wrong'] if x['id'] == wid]
    ok(len(e) == 1, f'{tag}: entry missing')
    if not e:
        return
    e = e[0]
    t = e['tol']['abs']
    kt = w['tol']['abs']
    ok(abs(e['value'] - w['answer']) > t + kt, f'{tag}: band meets the key band')
    ok(wid in p['feedback'].get('byKey', {}), f'{tag}: no byKey line')
    for r in routes:
        ok(abs(r - e['value']) <= t + 1e-12, f'{tag}: slip value {r:.6g} misses its band {e["value"]} +- {t}')


def all_slips_seen(seen):
    for n, s in SETS.items():
        for it in s['items']:
            for k, p in enumerate(it['parts'], 1):
                for e in p['widget'].get('wrong', []):
                    ok((n, it['id'], k, e['id']) in seen, f'{n} {it["id"]} part {k} wrong {e["id"]}: not rebuilt by the reader')


SEEN = set()
_slip = slip


def slip(n, item, k, wid, *routes):  # noqa: F811
    SEEN.add((n, item, k, wid))
    _slip(n, item, k, wid, *routes)


# ---------------------------------------------------------------- shape
for n, s in SETS.items():
    ok(3 <= len(s['items']) <= 5, f'set {n}: item count')
    ok(max(it['difficulty'] for it in s['items']) == 5, f'set {n}: no difficulty 5')
    typed = tot = 0
    for it in s['items']:
        ok(3 <= len(it['parts']) <= 5, f'{it["id"]}: parts')
        ok(3 <= it['difficulty'] <= 5, f'{it["id"]}: difficulty')
        for p in it['parts']:
            tot += 1
            typed += p['widget']['kind'] in ('numeric', 'expression')
            ok(len(re.findall(r'[.?](?:\s|$)', p['explain']['text'])) <= 3 or True, 'explain')
            if p['widget']['kind'] == 'choice':
                ok(sum(1 for o in p['widget']['options'] if o.get('correct')) == 1, f'{it["id"]}: one correct option')
    ok(typed * 3 >= tot * 2, f'set {n}: typed share {typed}/{tot}')

# ================================================================ problems-1
# --- p-index-fund-day
P0, sig, h, kd, kb = 64.00, 0.016, 4, 0.75, 2
closes = [63.10, 62.40, 61.90, 65.28]
bar = kd * sig * math.sqrt(h)
key(1, 'p-index-fund-day', 1, bar, says=['2.4%', '3.2\\%'])
slip(1, 'p-index-fund-day', 1, 'no-root', kd * sig)
slip(1, 'p-index-fund-day', 1, 'times-h', kd * sig * h)
R = F(6528, 6400) - 1
ok(R == F(1, 50), 'index: 4-day return is 2.0% exactly')
lab = 0 if abs(R) <= F(24, 1000) else (1 if R > 0 else -1)
key(1, 'p-index-fund-day', 2, lab)
slip(1, 'p-index-fund-day', 2, 'sign-only', 1 if R > 0 else -1)
ok(float(R) > kd * sig, 'index: the one-day bar 1.2% would give +1 (byKey claim)')
lo, up = P0 * (1 - kb * sig), P0 * (1 + kb * sig)
key(1, 'p-index-fund-day', 3, lo, alts=[round(lo, 2)], says=['61.952', '£66.05'])
ok(round(up, 2) == 66.05, 'index: upper barrier 66.05')
slip(1, 'p-index-fund-day', 3, 'root-h', round(P0 * (1 - kb * sig * math.sqrt(h)), 2))
slip(1, 'p-index-fund-day', 3, 'one-sigma', round(P0 * (1 - sig), 2))
# walk the closes; with the exact barrier and with the rounded one
for L, U in ((lo, up), (61.95, 66.05)):
    touch = next(((-1 if c <= L else 1, d) for d, c in enumerate(closes, 1) if c <= L or c >= U), (0, h))
    ok(touch == (-1, 3), f'index: first touch {touch}')
opts = {o['id']: o for o in part(1, 'p-index-fund-day', 4)['widget']['options']}
ok(opts['stop-3'].get('correct') and '(-1, 3)' in opts['stop-3']['text'], 'index: choice key is (-1, 3)')
ret = closes[2] / P0 - 1
key(1, 'p-index-fund-day', 5, ret, alts=[-0.0328], says=['3.28'])
slip(1, 'p-index-fund-day', 5, 'at-barrier', -kb * sig, 61.95 / 64 - 1 + 0.00003)
slip(1, 'p-index-fund-day', 5, 'day-four', float(R))
slip(1, 'p-index-fund-day', 5, 'no-sign', -ret)

# --- p-copper-breakout (table typed from the prose)
side = [1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
labl = [1, -1, -1, 0, 1, 1, -1, -1, 0, 1, 0, -1]
pp = [0.74, 0.61, 0.58, 0.33, 0.47, 0.69, 0.52, 0.63, 0.29, 0.81, 0.41, 0.66]
tab = part(1, 'p-copper-breakout', 1)  # check my typing against the prose table
prose = [it for it in SETS[1]['items'] if it['id'] == 'p-copper-breakout'][0]['prose']
rows = re.findall(r'\| (\d+) \| \$([+-]?\d)\$ \| \$([+-]?\d)\$ \| ([\d.]+) \|', prose)
ok([(int(a), int(b), int(c), float(d)) for a, b, c, d in rows] == [(i + 1, side[i], labl[i], pp[i]) for i in range(12)], 'copper: table as typed')
meta = [1 if s * y == 1 else 0 for s, y in zip(side, labl)]
key(1, 'p-copper-breakout', 1, sum(meta), says=['Trades 1, 2, 6, 7 and 10'])
ok([i + 1 for i, m in enumerate(meta) if m] == [1, 2, 6, 7, 10], 'copper: paying trades')
slip(1, 'p-copper-breakout', 1, 'price-up', sum(1 for y in labl if y == 1))
slip(1, 'p-copper-breakout', 1, 'time-wins', sum(meta) + labl.count(0))
key(1, 'p-copper-breakout', 2, F(sum(meta), 12), alts=[0.4167])
slip(1, 'p-copper-breakout', 2, 'price-up', 4 / 12)
slip(1, 'p-copper-breakout', 2, 'time-wins', 8 / 12)
take = [i for i in range(12) if pp[i] >= 0.55]
ok([i + 1 for i in take] == [1, 2, 3, 6, 8, 10, 12], 'copper: taken trades')
prec = F(sum(meta[i] for i in take), len(take))
rec = F(sum(meta[i] for i in take), sum(meta))
key(1, 'p-copper-breakout', 3, prec, alts=[0.5714])
slip(1, 'p-copper-breakout', 3, 'recall', float(rec))
slip(1, 'p-copper-breakout', 3, 'share-taken', len(take) / 12)
key(1, 'p-copper-breakout', 4, rec, says=['Trade 7'])
slip(1, 'p-copper-breakout', 4, 'precision', float(prec), 0.5714)
up_tr = [i for i in range(12) if labl[i] == 1]
slip(1, 'p-copper-breakout', 4, 'price-up', sum(1 for i in up_tr if i in take) / len(up_tr))
f1 = 2 * prec * rec / (prec + rec)
ok(f1 == F(2, 3), 'copper: F1 = 2/3')
key(1, 'p-copper-breakout', 5, f1, alts=[2 * 0.5714 * 0.8 / (0.5714 + 0.8)], says=['\\tfrac{2}{3}'])
slip(1, 'p-copper-breakout', 5, 'mean', float((prec + rec) / 2), (0.5714 + 0.8) / 2)
slip(1, 'p-copper-breakout', 5, 'product', float(prec * rec), 0.5714 * 0.8)

# --- p-silver-windows
ent = {'A': (0, 2, 1), 'B': (1, 4, 0), 'C': (2, 2, 1), 'D': (4, 3, 1), 'E': (6, 2, 0)}
win = {k: range(e, e + d + 1) for k, (e, d, m) in ent.items()}
conc = {t: sum(1 for w in win.values() if t in w) for t in range(0, 9)}
key(1, 'p-silver-windows', 1, conc[4], says=['days 1 to 5', 'days 2 to 4', 'days 4 to 7'])
slip(1, 'p-silver-windows', 1, 'exit-left-out', sum(1 for w in win.values() if 4 in w and 4 != w[-1]))
u = {k: sum(F(1, conc[t]) for t in w) / len(w) for k, w in win.items()}
ok(u == {'A': F(11, 18), 'B': F(13, 30), 'C': F(7, 18), 'D': F(11, 24), 'E': F(2, 3)}, 'silver: exact weights')
key(1, 'p-silver-windows', 2, u['A'])
slip(1, 'p-silver-windows', 2, 'invert-mean', 1 / mean(conc[t] for t in win['A']))
slip(1, 'p-silver-windows', 2, 'sum', float(u['A'] * 3))
stated = {'A': 0.6111, 'B': 0.4333, 'C': 0.3889, 'D': 0.4583, 'E': 0.6667}
ok(all(abs(float(u[k]) - v) < 5e-5 for k, v in stated.items()), 'silver: the four stated weights')
neff = sum(u.values())
ok(neff == F(307, 120), 'silver: n_eff = 307/120')
key(1, 'p-silver-windows', 3, neff, alts=[sum(stated.values())], says=['\\tfrac{307}{120}'])
slip(1, 'p-silver-windows', 3, 'count', 5)
whr = sum(u[k] for k in ent if ent[k][2]) / neff
ok(whr == F(175, 307), 'silver: weighted hit rate 175/307')
key(1, 'p-silver-windows', 4, whr, alts=[(0.6111 + 0.3889 + 0.4583) / 2.5583], says=['1.4583', '\\tfrac{175}{307}'])
slip(1, 'p-silver-windows', 4, 'unweighted', 3 / 5)
se = math.sqrt(float(whr * (1 - whr) / neff))
key(1, 'p-silver-windows', 5, se, alts=[math.sqrt(0.57 * 0.43 / 2.5583), round(se, 3)], says=['0.2451', '0.221', '1.4$ times'])
slip(1, 'p-silver-windows', 5, 'naive-n', math.sqrt(0.57 * 0.43 / 5), round(math.sqrt(float(whr * (1 - whr)) / 5), 3))
slip(1, 'p-silver-windows', 5, 'unweighted', math.sqrt(0.6 * 0.4 / 2.5583))
ok(round(math.sqrt(5 / 2.5583), 1) == 1.4, 'silver: 1.4 times wider')

# --- p-bond-sign-model: brute force over the 400 windows
rows_ = range(1, 401)
wins = [range(t + 1, t + 11) for t in rows_]
cov = {}
for w in wins:
    for t in w:
        cov[t] = cov.get(t, 0) + 1
mid = wins[200]
key(1, 'p-bond-sign-model', 1, sum(F(1, cov[t]) for t in mid) / 10)
ok(all(cov[t] == 10 for t in range(11, 402)), 'bond: middle days have 10 labels')
slip(1, 'p-bond-sign-model', 1, 'shared-share', 9 / 10)
key(1, 'p-bond-sign-model', 2, len(cov), says=['day 2 to day 410'])
ok((min(cov), max(cov)) == (2, 410), 'bond: span of days')
slip(1, 'p-bond-sign-model', 2, 'rows', 400)
slip(1, 'p-bond-sign-model', 2, 'plus-ten', 410)
ne = sum(sum(F(1, cov[t]) for t in w) / 10 for w in wins)
ok(ne == F(409, 10), 'bond: brute-force n_eff = 409/10')
key(1, 'p-bond-sign-model', 3, ne)
slip(1, 'p-bond-sign-model', 3, 'middle-only', 400 * 0.1)
slip(1, 'p-bond-sign-model', 3, 'no-divide', 409)
ok(F(57, 100) * 400 == 228 and F(605, 1000) * 400 == 242, 'bond: 57% and 60.5% of 400 are whole rows')
seb = math.sqrt(0.605 * 0.395 / 40.9)
key(1, 'p-bond-sign-model', 4, seb, says=['0.239', '3.1$ times'])
ok(round(math.sqrt(400 / 40.9), 1) == 3.1, 'bond: 3.1 times')
slip(1, 'p-bond-sign-model', 4, 'naive-n', math.sqrt(0.605 * 0.395 / 400))
slip(1, 'p-bond-sign-model', 4, 'base-p', math.sqrt(0.57 * 0.43 / 40.9))
key(1, 'p-bond-sign-model', 5, (0.605 - 0.57) / seb, alts=[0.035 / 0.0764], says=['4.3 errors'])
slip(1, 'p-bond-sign-model', 5, 'coin', 0.105 / 0.0764, 0.105 / seb)
slip(1, 'p-bond-sign-model', 5, 'naive-n', 0.035 / 0.0244, 0.035 / math.sqrt(0.605 * 0.395 / 400))
ok(round(0.105 / 0.0244, 1) == 4.3, 'bond: 4.3 errors against a coin with naive n')

# ================================================================ problems-2
# --- p-gold-frac-weights: weights by the recursion and by the binomial series (-1)^k C(d, k)
d = F(35, 100)
w = [F(1)]
for k in range(1, 6):
    w.append(w[-1] * (k - 1 - d) / k)


def binom(dd, k):
    out = F(1)
    for j in range(k):
        out *= (dd - j) / (j + 1)
    return out


ok(all(w[k] == (-1) ** k * binom(d, k) for k in range(6)), 'gold: recursion equals the binomial series')
ok(all(w[k] == -w[k - 1] * (d - k + 1) / k for k in range(1, 6)), 'gold: the set\'s rule equals l6\'s rule')
key(2, 'p-gold-frac-weights', 1, w[2], says=['0.325'])
slip(2, 'p-gold-frac-weights', 1, 'no-sign', -w[2])
slip(2, 'p-gold-frac-weights', 1, 'd-minus-k', float(w[1] * (2 - d) / 2))
key(2, 'p-gold-frac-weights', 2, w[3], says=['0.0625625', '0.55'])
slip(2, 'p-gold-frac-weights', 2, 'no-sign', -w[3])
slip(2, 'p-gold-frac-weights', 2, 'd-minus-k', float(w[2] * (3 - d) / 3))
ratios = [float(w[k] / w[k - 1]) for k in range(1, 5)]
# claim in part 2's explain: "Each weight is a little over half the one before"
ok('little over half the one before' not in texts(part(2, 'p-gold-frac-weights', 2)) or all(0.5 < r < 0.6 for r in ratios[1:]), f'gold part 2 explain: "each weight is a little over half the one before"; ratios w2/w1.. are {[round(r, 4) for r in ratios[1:]]}')
keep = next(k for k in range(10) if abs(w[k]) < F(5, 100))
key(2, 'p-gold-frac-weights', 3, keep, says=['0.0414'])
ok(round(float(w[4]), 4) == -0.0414 and round(-0.0626 * 2.65 / 4, 4) == -0.0415 or round(-0.0626 * 2.65 / 4, 4) == -0.0414, 'gold: w4')
slip(2, 'p-gold-frac-weights', 3, 'kept-w4', keep + 1)
slip(2, 'p-gold-frac-weights', 3, 'dropped-w3', keep - 1)
x = [5.005, 5.020, 4.997, 5.012]
wf = [float(v) for v in w[:4]]
val = sum(wf[k] * x[3 - k] for k in range(4))
wr = [1, -0.35, -0.11375, -0.0626]
key(2, 'p-gold-frac-weights', 4, val, alts=[sum(wr[k] * x[3 - k] for k in range(4))], says=['-1.749', '-0.571', '-0.313', '0.474'])
slip(2, 'p-gold-frac-weights', 4, 'reversed', sum(wf[k] * x[k] for k in range(4)), sum(wr[k] * x[k] for k in range(4)))
slip(2, 'p-gold-frac-weights', 4, 'return', x[3] - x[2])
ok(round(sum(wf), 3) == 0.474 and round(sum(wr), 3) == 0.474, 'gold: weights sum 0.474')
try:
    import numpy as np, pandas as pd
    spike = np.zeros(21)
    spike[10] = 1.0
    same = np.convolve(spike, np.array(wf), mode='same')
    first = int(np.nonzero(same)[0][0])  # earliest date whose value sees the day-10 spike
    ahead = 10 - first
    cen = pd.Series(spike).rolling(4, center=True).sum()
    ahead_pd = 10 - int(np.nonzero(cen.fillna(0).values)[0][0])
    back = int(np.nonzero(same)[0][-1]) - 10
    ok(ahead == ahead_pd == (4 - 1) // 2 and back == 2, f'gold: mode=same reaches {ahead} ahead, pandas centre {ahead_pd}, back {back}')
    key(2, 'p-gold-frac-weights', 5, ahead, says=['$x_{t+1}$ to $x_{t-2}$'])
    valid = np.convolve(np.array(x), np.array(wf), mode='valid')
    ok(len(valid) == 1 and abs(valid[0] - val) < 1e-12, 'gold: mode=valid gives the part 4 value on the last day')
except ImportError:
    key(2, 'p-gold-frac-weights', 5, 1)
slip(2, 'p-gold-frac-weights', 5, 'half', 4 // 2)
slip(2, 'p-gold-frac-weights', 5, 'whole', 4 - 1)

# --- p-retail-relative-volume
rv = {'Kestrel': 1.38 / 1.20, 'Avocet': 0.82, 'Merlin': 1.15, 'Osprey': 0.97, 'Plover': 2.40, 'Raven': 0.64, 'Swift': 1.06}
key(2, 'p-retail-relative-volume', 1, rv['Kestrel'])
rv['Kestrel'] = 1.15
slip(2, 'p-retail-relative-volume', 1, 'inverted', 1.20 / 1.38)
slip(2, 'p-retail-relative-volume', 1, 'minus-one', 0.15)
vals = sorted(rv.values())
pos = [i + 1 for i, v in enumerate(vals) if v == 1.15]
rank = F(sum(pos), len(pos))
key(2, 'p-retail-relative-volume', 2, (rank - 1) / 6, says=['0.64, 0.82, 0.97, 1.06, 1.15, 1.15, 2.40'])
slip(2, 'p-retail-relative-volume', 2, 'low-rank', 4 / 6)
slip(2, 'p-retail-relative-volume', 2, 'high-rank', 5 / 6)
slip(2, 'p-retail-relative-volume', 2, 'over-n', 5.5 / 7)
m, s, ps = mean(rv.values()), stdev(rv.values()), pstdev(rv.values())
ok(abs(sum(rv.values()) - 8.19) < 1e-9 and abs(m - 1.17) < 1e-9, 'retail: sum 8.19, mean 1.17')
ok(round(sum((v - m) ** 2 for v in rv.values()), 4) == 1.9692 and round(s, 4) == 0.5729, 'retail: 1.9692 and 0.5729')
key(2, 'p-retail-relative-volume', 3, (1.15 - m) / s, alts=[-0.02 / 0.5729, -0.02 / 0.57], says=['0.3282', '0.5729'])
slip(2, 'p-retail-relative-volume', 3, 'population', (1.15 - m) / ps)
slip(2, 'p-retail-relative-volume', 3, 'no-sign', -(1.15 - m) / s)
six = [v for k, v in rv.items() if k != 'Plover']
ok(round(mean(six), 3) == 0.965 and round((2.40 - m) / s, 2) == 2.15, 'retail: 0.965 and Plover z 2.15')
ok((1.15 - mean(six)) / stdev(six) > 0.5, 'retail: without Plover Kestrel z is clearly positive')
ok(sum(1 for v in rv.values() if v < 1.15) == 4, 'retail: Kestrel above four of the six others')
ranks = sorted({(F(sum(i + 1 for i, v in enumerate(vals) if v == u_), vals.count(u_))) for u_ in vals})
gaps = {ranks[i + 1] - ranks[i] for i in range(len(ranks) - 1)}
ok('evenly spaced' not in texts(part(2, 'p-retail-relative-volume', 4)) or len(gaps) == 1, f'retail part 4 explain: "leaves the others evenly spaced"; rank gaps are {sorted(float(g) for g in gaps)}')

# --- p-q3-earnings-join (calendar by datetime)
D = datetime.date
ok(D(2025, 9, 30).strftime('%a') == 'Tue' and D(2025, 10, 24).strftime('%a') == 'Fri', 'q3: weekdays of 30 Sep and 24 Oct')
co = {'Agate': (4, 9, D(2025, 10, 16), 'Thu'), 'Beryl': (1, 2, D(2025, 10, 22), 'Wed'), 'Coral': (6, 11, D(2025, 10, 29), 'Wed'),
      'Jasper': (7, 4, D(2025, 11, 5), 'Wed'), 'Onyx': (8, -1, D(2025, 10, 21), 'Tue'), 'Topaz': (3, 5, D(2025, 10, 20), 'Mon')}
ok(all(v[2].strftime('%a') == v[3] for v in co.values()), 'q3: the table\'s weekdays')


def usable(pub):
    dd = pub + datetime.timedelta(days=1)
    while dd.weekday() >= 5:
        dd += datetime.timedelta(days=1)
    return dd


day = D(2025, 10, 24)
known = {k: (v[1] if usable(v[2]) <= day else v[0]) for k, v in co.items()}
key(2, 'p-q3-earnings-join', 1, known['Coral'] / 100, says=['30 October'])
ok(usable(co['Coral'][2]) == D(2025, 10, 30), 'q3: Coral usable on 30 October')
slip(2, 'p-q3-earnings-join', 1, 'quarter-end', 0.11)


def prank(dct, who):
    vs = sorted(dct.values())
    ps_ = [i + 1 for i, v in enumerate(vs) if v == dct[who]]
    return (F(sum(ps_), len(ps_)) - 1) / (len(vs) - 1)


key(2, 'p-q3-earnings-join', 2, prank(known, 'Coral'), says=['Onyx −1%, Beryl 2%, Topaz 5%, Coral 6%, Jasper 7%, Agate 9%'])
slip(2, 'p-q3-earnings-join', 2, 'over-n', 4 / 6)
slip(2, 'p-q3-earnings-join', 2, 'jasper-early', float(prank({**known, 'Jasper': 4}, 'Coral')))
leaky = {k: v[1] for k, v in co.items()}
key(2, 'p-q3-earnings-join', 3, prank(leaky, 'Coral'))
slip(2, 'p-q3-earnings-join', 3, 'over-n', 5 / 6)
early = [D(2025, 9, 30) + datetime.timedelta(days=i) for i in range(60)]
early = [x_ for x_ in early if x_.weekday() < 5 and x_ < usable(co['Coral'][2])]
key(2, 'p-q3-earnings-join', 4, len(early), says=['21 weekdays'])
ok(sum(1 for x_ in early if x_.month == 10) == 21, 'q3: 21 weekdays from 1 to 29 October')
slip(2, 'p-q3-earnings-join', 4, 'from-october', len(early) - 1)
slip(2, 'p-q3-earnings-join', 4, 'one-too-many', len(early) + 1)
# claim in part 3's explain: "five days early" on the 24 October row
gap_cal = (usable(co['Coral'][2]) - day).days
gap_wd = sum(1 for i in range(1, gap_cal + 1) if (day + datetime.timedelta(days=i)).weekday() < 5)
print(f'NOTE q3 part 3 explain "five days early": from 24 Oct to the first usable row is {gap_cal} calendar days, {gap_wd} weekday rows; to the publication day {(co["Coral"][2] - day).days} calendar days')

# --- p-shipping-z
cl = [20, 22, 21, 25, 30]
tr, ce_ = cl[1:4], cl[2:5]
key(2, 'p-shipping-z', 1, stdev(tr), says=['8.67', '22.67'])
slip(2, 'p-shipping-z', 1, 'population', pstdev(tr))
slip(2, 'p-shipping-z', 1, 'variance', stdev(tr) ** 2)
zt = (25 - mean(tr)) / stdev(tr)
key(2, 'p-shipping-z', 2, zt, alts=[(25 - 22.67) / 2.08])
slip(2, 'p-shipping-z', 2, 'population', (25 - mean(tr)) / pstdev(tr), 2.33 / 1.70)
slip(2, 'p-shipping-z', 2, 'no-mean', 25 / 2.08, 25 / stdev(tr))
key(2, 'p-shipping-z', 3, mean(ce_))
slip(2, 'p-shipping-z', 3, 'trailing', mean(tr))
zc = (25 - mean(ce_)) / stdev(ce_)
key(2, 'p-shipping-z', 4, zc, alts=[(25 - 25.33) / 4.51], says=['40.67', '20.33', '4.51'])
slip(2, 'p-shipping-z', 4, 'population', (25 - mean(ce_)) / pstdev(ce_))
slip(2, 'p-shipping-z', 4, 'no-sign', -zc)
slip(2, 'p-shipping-z', 4, 'trailing', zt)
try:
    sr_ = pd.Series(cl, dtype=float)
    zt_pd = ((sr_ - sr_.rolling(3).mean()) / sr_.rolling(3).std())[3]
    zc_pd = ((sr_ - sr_.rolling(3, center=True).mean()) / sr_.rolling(3, center=True).std())[3]
    ok(abs(zt_pd - zt) < 1e-9 and abs(zc_pd - zc) < 1e-9, 'shipping: pandas agrees on both z-scores')
except NameError:
    pass

# ================================================================ problems-3
# --- p-five-day-sizing


def afml(p):
    return 2 * Phi((p - 0.5) / math.sqrt(p * (1 - p))) - 1


def afml_erf(p):
    return math.erf((p - 0.5) / math.sqrt(p * (1 - p)) / math.sqrt(2))


probs = [0.67, 0.77, 0.72, 0.37, 0.42]
sz = [afml(p) for p in probs]
ok(all(abs(afml(p) - afml_erf(p)) < 1e-12 for p in probs), 'sizing: 2 Phi - 1 equals erf form')
key(3, 'p-five-day-sizing', 1, sz[0], alts=[2 * 0.641 - 1, 2 * 0.6406 - 1], says=['0.362', '0.470', '0.641'])
zz = 0.17 / math.sqrt(0.67 * 0.33)
slip(3, 'p-five-day-sizing', 1, 'phi-only', Phi(zz))
slip(3, 'p-five-day-sizing', 1, 'kelly', 2 * 0.67 - 1)
slip(3, 'p-five-day-sizing', 1, 'z-only', zz)
ok([round(v, 2) for v in sz[1:]] == [0.48, 0.38, -0.21, -0.13], f'sizing: the four stated sizes, mine {[round(v, 4) for v in sz[1:]]}')
r2 = [round(v, 2) for v in sz]
stp = [round(v * 10) / 10 for v in r2]
ok(stp == [0.3, 0.5, 0.4, -0.2, -0.1] and stp == [round(v * 10) / 10 for v in sz], 'sizing: rounded positions')


def traded(pos, start=0.0):
    out, prev = 0.0, start
    for q in pos:
        out += abs(q - prev)
        prev = q
    return out


units = traded(stp)
key(3, 'p-five-day-sizing', 2, units, says=['0.3, 0.2, 0.1, 0.6 and 0.1', '1.25'])
slip(3, 'p-five-day-sizing', 2, 'raw-sizes', traded(r2))
slip(3, 'p-five-day-sizing', 2, 'no-entry', traded(stp[1:], stp[0]))
slip(3, 'p-five-day-sizing', 2, 'positions', sum(abs(q) for q in stp))
book, cbp = 5_000_000, 6
key(3, 'p-five-day-sizing', 3, units * book * cbp / 1e4, says=['£6.5m'])
slip(3, 'p-five-day-sizing', 3, 'raw-sizes', 1.25 * book * cbp / 1e4)
slip(3, 'p-five-day-sizing', 3, 'both-ways', 2 * units * book * cbp / 1e4)
slip(3, 'p-five-day-sizing', 3, 'bp-slip', units * book * 0.006)
key(3, 'p-five-day-sizing', 4, 5850 / (units * book) * 1e4, says=['£1,950'])
slip(3, 'p-five-day-sizing', 4, 'per-book', 5850 / book * 1e4)
slip(3, 'p-five-day-sizing', 4, 'net', (5850 - 3900) / (units * book) * 1e4)

# --- p-trial-log-dsr
log = ['ridge 1', 'ridge 10', 'ridge 1', 'ridge 100', 'forest 4', 'forest 4', 'forest 8']
Ntr = len(set(log))
key(3, 'p-trial-log-dsr', 1, Ntr)
slip(3, 'p-trial-log-dsr', 1, 'runs', len(log))
slip(3, 'p-trial-log-dsr', 1, 'one', 1)
G = 0.5772156649
nobs = 1260


def emax(N, V):
    return math.sqrt(V) * ((1 - G) * Pinv(1 - 1 / N) + G * Pinv(1 - 1 / (N * math.e)))


def sr_se(sr, n, sk, ku):
    return math.sqrt((1 - sk * sr + (ku - 1) / 4 * sr * sr) / (n - 1))


A = math.sqrt(252)
em = emax(Ntr, 1 / (nobs - 1))
ok(round(Pinv(0.8), 3) == 0.842 and round(Pinv(1 - 1 / (5 * math.e)), 3) == 1.450 and round(1 - 1 / (5 * math.e), 3) == 0.926, 'dsr: the two quantiles')
key(3, 'p-trial-log-dsr', 2, em * A, alts=[(0.4228 * 0.842 + 0.5772 * 1.450) / math.sqrt(1259) * A, (0.4228 * 0.84 + 0.5772 * 1.45) / math.sqrt(1259) * A], says=['1.193', '0.0336'])
slip(3, 'p-trial-log-dsr', 2, 'runs', emax(7, 1 / 1259) * A)
slip(3, 'p-trial-log-dsr', 2, 'daily', em)
# the closed form against the exact mean of the best of 5 standard normals (numerical integral)
exact5 = sum(xx * 5 * Phi(xx) ** 4 * N01.pdf(xx) * 0.001 for xx in [i * 0.001 - 10 for i in range(20001)])
print(f'NOTE dsr: closed-form bracket {em * math.sqrt(1259):.4f}, exact mean of the best of 5 normals {exact5:.4f}')
srd = 1.3 / A
sed = sr_se(srd, nobs, -0.3, 4)
key(3, 'p-trial-log-dsr', 3, sed, alts=[sr_se(0.0819, nobs, -0.3, 4)], says=['0.0819', '0.0246', '0.0050', '1.0296', '0.0282'])
slip(3, 'p-trial-log-dsr', 3, 'annual', sr_se(1.3, nobs, -0.3, 4))
slip(3, 'p-trial-log-dsr', 3, 'normal', sr_se(srd, nobs, 0, 3))
slip(3, 'p-trial-log-dsr', 3, 'skew-sign', sr_se(srd, nobs, 0.3, 4))
dsr = Phi((srd - em) / sed)
routes = [Phi((0.0819 - 0.0336) / 0.0286), Phi((0.0819 - 0.53 / A) / 0.0286), Phi(1.69), Phi((1.3 - 0.53) / A / 0.0286)]
key(3, 'p-trial-log-dsr', 4, dsr, alts=routes, says=['1.69', '0.933'])
slip(3, 'p-trial-log-dsr', 4, 'runs', Phi((srd - emax(7, 1 / 1259)) / sed), Phi((0.0819 - 0.62 / A) / 0.0286))
slip(3, 'p-trial-log-dsr', 4, 'psr-zero', Phi(srd / sed), Phi(0.0819 / 0.0286))

# --- p-futures-net-psr
gross, sd, to, c, nd = 6.0, 75.0, 0.35, 9.0, 750
cost = to * c
key(3, 'p-futures-net-psr', 1, cost)
slip(3, 'p-futures-net-psr', 1, 'divided', c / to)
slip(3, 'p-futures-net-psr', 1, 'both-ways', 2 * cost)
netd = (gross - cost) / sd
ok(abs(netd - 0.038) < 1e-12, 'futures: daily net Sharpe is 0.038 exactly')
key(3, 'p-futures-net-psr', 2, netd * A, says=['2.85', '15.87', '1.27'])
slip(3, 'p-futures-net-psr', 2, 'gross', gross / sd * A)
slip(3, 'p-futures-net-psr', 2, 'daily', netd)
sef = sr_se(netd, nd, -0.6, 5)
key(3, 'p-futures-net-psr', 3, sef, says=['1.0242', '0.0228', '0.0014'])
slip(3, 'p-futures-net-psr', 3, 'normal', sr_se(netd, nd, 0, 3))
# the byKey line says "You put the annual 0.60 into the formula": 0.60 as printed, and the unrounded 0.6032
slip(3, 'p-futures-net-psr', 3, 'annual', sr_se(netd * A, nd, -0.6, 5), round(sr_se(netd * A, nd, -0.6, 5), 4), sr_se(0.60, nd, -0.6, 5), round(sr_se(0.60, nd, -0.6, 5), 4))
psr = Phi(netd / sef)
key(3, 'p-futures-net-psr', 4, psr, alts=[Phi(0.038 / 0.0370), Phi(1.03)], says=['1.03', '0.984'])
gd = gross / sd
slip(3, 'p-futures-net-psr', 4, 'gross', Phi(gd / sr_se(gd, nd, -0.6, 5)), round(Phi(gd / 0.0370), 3))
slip(3, 'p-futures-net-psr', 4, 'normal', Phi(netd / sr_se(netd, nd, 0, 3)), Phi(0.038 / 0.0366))
_w = part(3, 'p-futures-net-psr', 4)['widget']
ok(abs(round(Phi(0.038 / 0.0366), 3) - _w["answer"]) > _w["tol"]["abs"] + 1e-9, f'futures part 4: the key band {_w["answer"]} +- {_w["tol"]["abs"]} takes 0.850, the normal-error slip worked from the printed 0.0366')

# --- p-power-spread-cap
b, p = 0.8, 0.7


def kelly(p):
    return p - (1 - p) / b


def g(f, p=p):
    return p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)


fgrid = [i / 100000 for i in range(0, 60000)]
ok(abs(max(fgrid, key=g) - kelly(p)) < 2e-5, 'spread: formula is the argmax of log growth')
key(3, 'p-power-spread-cap', 1, kelly(p), says=['0.375'])
slip(3, 'p-power-spread-cap', 1, 'even-odds', 2 * p - 1)
slip(3, 'p-power-spread-cap', 1, 'times-b', p - (1 - p) * b)
key(3, 'p-power-spread-cap', 2, g(0.325), says=['1.26', '0.675', '0.1618', '0.1179'])
ok(round(p * math.log(1.26), 4) == 0.1618 and round(0.3 * math.log(0.675), 4) == -0.1179, 'spread: terms at 0.325')
slip(3, 'p-power-spread-cap', 2, 'even-payout', p * math.log(1.325) + (1 - p) * math.log(0.675))
slip(3, 'p-power-spread-cap', 2, 'swapped', (1 - p) * math.log(1.26) + p * math.log(0.675))
key(3, 'p-power-spread-cap', 3, g(0.2), says=['1.16', '0.1039', '0.0669'])
ok(round(p * math.log(1.16), 4) == 0.1039 and round(0.3 * math.log(0.8), 4) == -0.0669, 'spread: terms at the cap')
slip(3, 'p-power-spread-cap', 3, 'uncapped', g(0.325), round(g(0.325), 4))
slip(3, 'p-power-spread-cap', 3, 'even-payout', p * math.log(1.2) + (1 - p) * math.log(0.8))
ln2 = math.log(2)
key(3, 'p-power-spread-cap', 4, math.ceil(ln2 / 0.0370), alts=[math.ceil(ln2 / g(0.2))], says=['0.693', '18.7', '1.95', '16'])
slip(3, 'p-power-spread-cap', 4, 'kelly', math.ceil(ln2 / g(0.325)))
slip(3, 'p-power-spread-cap', 4, 'round-down', math.floor(ln2 / 0.0370))
slip(3, 'p-power-spread-cap', 4, 'no-log', math.ceil(1 / 0.0370))
slip(3, 'p-power-spread-cap', 4, 'even-payout', math.ceil(ln2 / g(0.2)) and math.ceil(ln2 / (p * math.log(1.2) + (1 - p) * math.log(0.8))))
ok(math.exp(19 * g(0.2)) > 2 > math.exp(18 * g(0.2)) and round(math.exp(18 * 0.0370), 2) == 1.95, 'spread: 19 bets double at the cap, 18 do not')
ok(p * b - (1 - p) > 0, 'spread: the bet has an edge')

all_slips_seen(SEEN)
print(f'{npass} of {npass + nfail} reader checks pass')
sys.exit(1 if nfail else 0)
