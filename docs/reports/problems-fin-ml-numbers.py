"""Recompute every number in app/content/courses/fin-ml/problems-<n>.json twice (docs/briefs/chained.md check 1).

Method 1 is exact where it can be (fractions, sympy, the closed form the lesson teaches). Method 2 takes another
route: a loop that walks the closes as `first_touch` does, scikit-learn's precision, recall and F1, a brute-force
concurrency count over every window, NumPy's convolution, pandas ranks, a Monte Carlo draw of the best of N noise
Sharpes, a numerical maximum of Kelly growth, and so on. For each numeric part the script checks: the two methods
agree; the key is within its tol of the exact value; every `wrong` value matches its named slip, lies outside the
key's band, and does not overlap another; byKey covers the wrongs. Choice parts check the keyed option, the
distractors' byKey lines, and the numbers their text states. Printed numbers in feedback and explain are checked
with `said`. Exit 0 when all pass.

Run from anywhere: <scratchpad>/venv/bin/python docs/reports/problems-fin-ml-numbers.py
"""
import itertools
import json
import math
import os
import sys
import warnings
from fractions import Fraction as F
from statistics import NormalDist

import numpy as np
import pandas as pd
import sympy as sp
from sklearn.metrics import f1_score, precision_score, recall_score

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'fin-ml')
ND = NormalDist()
Phi, iPhi = ND.cdf, ND.inv_cdf
EG = 0.5772156649015329
fails, checks = [], 0
rng = np.random.default_rng(20261116)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    d = json.load(open(p))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'fin-ml', f'problems-{n}: header')
    ok(3 <= len(d['items']) <= 5, f'problems-{n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'problems-{n}: no difficulty 5')
    typed = sum(p_['widget']['kind'] in ('numeric', 'expression') for it in d['items'] for p_ in it['parts'])
    total = sum(len(it['parts']) for it in d['items'])
    ok(3 * typed >= 2 * total, f'problems-{n}: typed parts {typed} of {total}')
    return {it['id']: it for it in d['items']}


def part(items, iid, k):
    return items[iid]['parts'][k - 1]


def num(items, iid, k, exact, alt, slips, agree=1e-9):
    """exact: the value by method 1; alt: by method 2; slips: {wrong id: value the slip gives}."""
    w = part(items, iid, k)['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e, a = float(exact), float(alt)
    ok(math.isclose(e, a, rel_tol=agree, abs_tol=agree), f'{tag}: methods differ {e} vs {a}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= wt + 1e-12, f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} inside the key band')
    for a_, b_ in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a_], wrongs[b_]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a_} and {b_} overlap')
    fb = part(items, iid, k)['feedback']
    ok(set(fb.get('byKey', {})) == set(wrongs), f'{tag}: byKey keys vs wrongs')


def pick(items, iid, k, correct_id):
    w = part(items, iid, k)['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')
    fb = part(items, iid, k)['feedback']
    ok(set(fb.get('byKey', {})) == {o['id'] for o in w['options'] if not o.get('correct')}, f'{iid} p{k}: byKey keys')


def said(items, iid, k, *phrases):
    """Each phrase (a number as printed) appears in the part's question, feedback or explain."""
    p_ = part(items, iid, k) if k else items[iid]
    blob = json.dumps(p_, ensure_ascii=False) + (items[iid].get('prose', '') if k else '')
    for ph in phrases:
        ok(ph in blob, f'{iid} p{k}: text does not state "{ph}"')


def r(x, nd):
    return float(round(x, nd))


# ---------------------------------------------------------------- level 1
L1 = load(1)

# p-index-fund-day
P0, sig, k_dz, h, k_tb = F(64), F(16, 1000), F(3, 4), 4, 2
closes = [F('63.10'), F('62.40'), F('61.90'), F('65.28')]
bar = k_dz * sig * sp.sqrt(h)
num(L1, 'p-index-fund-day', 1, bar, 0.75 * 0.016 * np.sqrt(4),
    {'no-root': k_dz * sig, 'times-h': k_dz * sig * h})
ret4 = closes[-1] / P0 - 1
label = 0 if abs(ret4) <= bar else int(np.sign(float(ret4)))
alt_label = int(np.sign(float(ret4))) * (abs(65.28 / 64 - 1) > 0.024)
num(L1, 'p-index-fund-day', 2, label, alt_label, {'sign-only': 1})
ok(label == 0 and int(np.sign(float(ret4))) == 1 and abs(ret4) > k_dz * sig, 'p-index p2: the one-day bar would give +1')
lower, upper = P0 * (1 - k_tb * sig), P0 * (1 + k_tb * sig)
num(L1, 'p-index-fund-day', 3, lower, 64 * 0.968,
    {'root-h': P0 * (1 - k_tb * sig * 2), 'one-sigma': P0 * (1 - sig)})
said(L1, 'p-index-fund-day', 3, '£61.952', '£66.05', '£61.95')
ok(r(float(upper), 2) == 66.05, 'p-index: upper barrier 66.05')


def first_touch(path, up, lo, limit):
    for d_, p_ in enumerate(path[1:], start=1):
        if p_ <= lo:
            return -1, d_
        if p_ >= up:
            return 1, d_
        if d_ == limit:
            break
    return 0, limit


ft = first_touch([P0] + closes, upper, lower, 4)
ok(ft == (-1, 3), f'p-index p4: first_touch {ft}')
ok(first_touch([64.0, 63.10, 62.40, 61.90, 65.28], 66.048, 61.952, 4) == (-1, 3), 'p-index p4: float walk')
pick(L1, 'p-index-fund-day', 4, 'stop-3')
ok(closes[1] > lower and closes[2] <= lower and closes[3] < upper, 'p-index p4: distractor facts')
loss = closes[2] / P0 - 1
num(L1, 'p-index-fund-day', 5, loss, 61.90 / 64 - 1,
    {'at-barrier': lower / P0 - 1, 'day-four': ret4, 'no-sign': -loss}, agree=1e-12)
said(L1, 'p-index-fund-day', 5, '-3.28\\\\%', '3.2%', '£61.90')

# p-copper-breakout
s = [1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
y = [1, -1, -1, 0, 1, 1, -1, -1, 0, 1, 0, -1]
pp = [0.74, 0.61, 0.58, 0.33, 0.47, 0.69, 0.52, 0.63, 0.29, 0.81, 0.41, 0.66]
prose = L1['p-copper-breakout']['prose']
rows = [ln for ln in prose.split('\n') if ln.startswith('| ') and ln[2].isdigit()]
parsed = [[c.strip().strip('$') for c in ln.strip('|').split('|')] for ln in rows]
ok([int(c[1]) for c in parsed] == s and [int(c[2]) for c in parsed] == y and [float(c[3]) for c in parsed] == pp,
   'p-copper: table matches the script')
z = [1 if a * b == 1 else 0 for a, b in zip(s, y)]
z_alt = [int((a == 1 and b == 1) or (a == -1 and b == -1)) for a, b in zip(s, y)]
num(L1, 'p-copper-breakout', 1, sum(z), sum(z_alt),
    {'price-up': sum(v == 1 for v in y), 'time-wins': sum(a * b >= 0 for a, b in zip(s, y))})
num(L1, 'p-copper-breakout', 2, F(sum(z), 12), precision_score(z, [1] * 12),
    {'price-up': F(sum(v == 1 for v in y), 12), 'time-wins': F(sum(a * b >= 0 for a, b in zip(s, y)), 12)})
take = [int(q >= 0.6) for q in pp]
tp = sum(t * zz for t, zz in zip(take, z))
P_, R_ = F(tp, sum(take)), F(tp, sum(z))
num(L1, 'p-copper-breakout', 3, P_, precision_score(z, take), {'recall': R_, 'share-taken': F(sum(take), 12)})
up_z = [int(v == 1) for v in y]
num(L1, 'p-copper-breakout', 4, R_, recall_score(z, take),
    {'precision': P_, 'price-up': F(sum(t * u for t, u in zip(take, up_z)), sum(up_z))})
ok([i + 1 for i in range(12) if z[i] and not take[i]] == [7] and pp[6] == 0.52, 'p-copper p4: trade 7 is missed')
num(L1, 'p-copper-breakout', 5, 2 * P_ * R_ / (P_ + R_), f1_score(z, take),
    {'mean': (F(2, 3) + F(4, 5)) / 2, 'product': F(2, 3) * F(4, 5)})
ok(2 * P_ * R_ / (P_ + R_) == F(8, 11), 'p-copper p5: 8/11')

# p-silver-windows
tbl = {'A': (0, 2, 1), 'B': (1, 4, 0), 'C': (2, 2, 1), 'D': (4, 3, 1), 'E': (6, 2, 0)}
win = {k_: (e, e + d_) for k_, (e, d_, _) in tbl.items()}
ml = {k_: v[2] for k_, v in tbl.items()}
days = range(0, 9)
c = {t: sum(a <= t <= b for a, b in win.values()) for t in days}
c_np = np.zeros(9, int)
for a, b in win.values():
    c_np[a:b + 1] += 1
ok(list(c.values()) == list(c_np), 'p-silver: concurrency two ways')
c_excl = sum(a <= 4 <= b - 1 for a, b in win.values())
num(L1, 'p-silver-windows', 1, c[4], c_np[4], {'exit-left-out': c_excl})
u = {k_: sum(F(1, c[t]) for t in range(a, b + 1)) / (b - a + 1) for k_, (a, b) in win.items()}
u_np = {k_: float(np.mean(1 / c_np[a:b + 1])) for k_, (a, b) in win.items()}
A0, A1 = win['A']
num(L1, 'p-silver-windows', 2, u['A'], u_np['A'],
    {'invert-mean': 1 / (sum(F(c[t]) for t in range(A0, A1 + 1)) / 3), 'sum': sum(F(1, c[t]) for t in range(A0, A1 + 1))},
    agree=1e-12)
said(L1, 'p-silver-windows', 3, 'B 0.4333', 'C 0.3889', 'D 0.4583', 'E 0.6667')
ok([r(float(u[k_]), 4) for k_ in 'BCDE'] == [0.4333, 0.3889, 0.4583, 0.6667], 'p-silver p3: stated weights')
neff = sum(u.values())
num(L1, 'p-silver-windows', 3, neff, sum(u_np.values()), {'count': 5}, agree=1e-12)
ok(neff == F(307, 120), 'p-silver p3: 307/120')
hr = sum(u[k_] * ml[k_] for k_ in u) / neff
num(L1, 'p-silver-windows', 4, hr, np.average([ml[k_] for k_ in u_np], weights=list(u_np.values())),
    {'unweighted': F(3, 5)}, agree=1e-12)
ok(hr == F(175, 307), 'p-silver p4: 175/307')
se = math.sqrt(float(hr * (1 - hr) / neff))
se_alt = math.sqrt(0.57 * 0.43 / 2.5583)
num(L1, 'p-silver-windows', 5, se, se_alt,
    {'naive-n': math.sqrt(float(hr * (1 - hr)) / 5), 'unweighted': math.sqrt(0.6 * 0.4 / float(neff))}, agree=2e-4)
ok(r(math.sqrt(5 / float(neff)), 1) == 1.4 and r(math.sqrt(0.57 * 0.43 / 5), 3) == 0.221, 'p-silver p5: explain numbers')

# p-bond-sign-model
H, NR = 10, 400
num(L1, 'p-bond-sign-model', 1, F(1, H), 1 / np.mean(np.full(H, H)), {'shared-share': F(H - 1, H)})
cov = np.zeros(NR + H + 1, int)
for t in range(1, NR + 1):
    cov[t + 1:t + H + 1] += 1
D = int((cov > 0).sum())
num(L1, 'p-bond-sign-model', 2, NR + H - 1, D, {'rows': NR, 'plus-ten': NR + H})
ok(cov.nonzero()[0].min() == 2 and cov.nonzero()[0].max() == 410, 'p-bond p2: days 2 to 410')
u_brute = [np.mean(1 / cov[t + 1:t + H + 1]) for t in range(1, NR + 1)]
neff4 = F(NR + H - 1, H)
num(L1, 'p-bond-sign-model', 3, neff4, sum(u_brute), {'middle-only': NR * F(1, H), 'no-divide': D}, agree=1e-9)
se4 = math.sqrt(0.605 * 0.395 / float(neff4))
p_sim = rng.binomial(41, 0.605, 200000) / 41  # 41 independent labels: se close to the exact one
num(L1, 'p-bond-sign-model', 4, se4, math.sqrt(float(F(605, 1000) * F(395, 1000) / neff4)),
    {'naive-n': math.sqrt(0.605 * 0.395 / NR), 'base-p': math.sqrt(0.57 * 0.43 / float(neff4))}, agree=1e-12)
ok(abs(p_sim.std() - math.sqrt(0.605 * 0.395 / 41)) < 0.001, 'p-bond p4: simulated se of 41 independent labels')
ok(r(math.sqrt(NR / float(neff4)), 1) == 3.1, 'p-bond p4: ratio 3.1')
t4 = 0.035 / se4
num(L1, 'p-bond-sign-model', 5, t4, (0.605 - 0.57) / 0.0764, {'coin': 0.105 / 0.0764, 'naive-n': 0.035 / 0.0244}, agree=1e-3)
ok(r(t4, 2) == 0.46 and r(0.035 / 0.0764, 2) == 0.46, 'p-bond p5: t 0.46 from exact and rounded se')
ok(r(0.105 / math.sqrt(0.605 * 0.395 / NR), 1) == 4.3, 'p-bond p5: 4.3 naive coin errors')

# ---------------------------------------------------------------- level 2
L2 = load(2)

# p-gold-frac-weights
d = sp.Rational(35, 100)
w_ex = [sp.binomial(d, k_) * (-1) ** k_ for k_ in range(6)]          # (1 - B)^d expanded
w_rec = [1.0]
for k_ in range(1, 6):
    w_rec.append(w_rec[-1] * (k_ - 1 - 0.35) / k_)                    # the recursion as the prose writes it
num(L2, 'p-gold-frac-weights', 1, w_ex[2], w_rec[2],
    {'no-sign': -w_ex[2], 'd-minus-k': w_ex[1] * (2 - d) / 2}, agree=1e-12)
num(L2, 'p-gold-frac-weights', 2, w_ex[3], w_rec[3],
    {'no-sign': -w_ex[3], 'd-minus-k': sp.Rational(-11375, 100000) * (3 - d) / 3}, agree=1e-12)
W = next(k_ for k_ in range(10) if abs(w_ex[k_]) < sp.Rational(5, 100))
num(L2, 'p-gold-frac-weights', 3, W, sum(abs(v) >= 0.05 for v in w_rec[:6]), {'kept-w4': W + 1, 'dropped-w3': W - 1})
ok(r(float(w_ex[4]), 4) == -0.0414 and r(float(-0.0625625 * 2.65 / 4), 4) == -0.0414, 'p-gold p3: w4 = -0.0414')
xs = [sp.Rational(v) for v in ('5.005', '5.020', '4.997', '5.012')]   # oldest first
val = sum(w_ex[k_] * xs[3 - k_] for k_ in range(W))
val_np = float(np.convolve(np.array(xs, float), np.array(w_rec[:W]), 'valid')[0])
w_round = [1, -0.35, -0.11375, -0.0626]
num(L2, 'p-gold-frac-weights', 4, val, val_np,
    {'reversed': sum(w_ex[k_] * xs[k_] for k_ in range(W)), 'return': xs[3] - xs[2]}, agree=1e-12)
ok(abs(sum(a * b for a, b in zip(w_round, xs[::-1])) - 2.379) <= 0.0015, 'p-gold p4: rounded w3 still in band')
ok([r(float(w_ex[k_] * xs[3 - k_]), 3) for k_ in range(4)] == [5.012, -1.749, -0.571, -0.313], 'p-gold p4: terms')
ok(r(float(sum(w_ex[:4])), 3) == 0.474, 'p-gold p4: weights sum 0.474')
spike = np.zeros(12)
spike[7] = 1.0
same = np.convolve(spike, np.array(w_rec[:W]), 'same')
ahead = 7 - int(np.flatnonzero(np.abs(same) > 1e-12).min())
num(L2, 'p-gold-frac-weights', 5, (W - 1) // 2, ahead, {'half': W // 2, 'whole': W - 1})

# p-retail-relative-volume
kes = F('1.38') / F('1.20')
num(L2, 'p-retail-relative-volume', 1, kes, 1.38 / 1.20, {'inverted': F('1.20') / F('1.38'), 'minus-one': kes - 1})
names = ['Avocet', 'Kestrel', 'Merlin', 'Osprey', 'Plover', 'Raven', 'Swift']
vals = [F('0.82'), kes, F('1.15'), F('0.97'), F('2.40'), F('0.64'), F('1.06')]
srt = sorted(vals)
rank_k = F(sum(i + 1 for i, v in enumerate(srt) if v == kes), sum(v == kes for v in srt))
ser = pd.Series([float(v) for v in vals], index=names)
num(L2, 'p-retail-relative-volume', 2, (rank_k - 1) / 6, (ser.rank()['Kestrel'] - 1) / 6,
    {'low-rank': F(4, 6), 'high-rank': F(5, 6), 'over-n': rank_k / 7})
mean7 = sum(vals) / 7
ss = sum((v - mean7) ** 2 for v in vals)
z_ex = (kes - mean7) / sp.sqrt(sp.Rational(ss.numerator, ss.denominator) / 6)
num(L2, 'p-retail-relative-volume', 3, z_ex, (ser['Kestrel'] - ser.mean()) / ser.std(ddof=1),
    {'population': (ser['Kestrel'] - ser.mean()) / ser.std(ddof=0), 'no-sign': -z_ex}, agree=1e-12)
ok(sum(vals) == F('8.19') and mean7 == F('1.17') and ss == F('1.9692') and r(float(ss / 6), 4) == 0.3282
   and r(ser.std(), 4) == 0.5729, 'p-retail p3: stated mean, sum of squares and sd')
pick(L2, 'p-retail-relative-volume', 4, 'outlier')
six = [v for v, n_ in zip(vals, names) if n_ != 'Plover']
ok(sum(six) / 6 == F('0.965') and kes > sum(six) / 6, 'p-retail p4: mean of the six is 0.965')
ok(r((2.40 - ser.mean()) / ser.std(), 2) == 2.15 and sum(v < kes for v in vals) == 4, 'p-retail p4: Plover z, four below')

# p-q3-earnings-join
import datetime as dt
co = {'Agate': (4, 9, '2025-10-16'), 'Beryl': (1, 2, '2025-10-22'), 'Coral': (6, 11, '2025-10-29'),
      'Jasper': (7, 4, '2025-11-05'), 'Onyx': (8, -1, '2025-10-21'), 'Topaz': (3, 5, '2025-10-20')}
prose = L2['p-q3-earnings-join']['prose']
for n_, (q2, q3, pub) in co.items():
    day = dt.date.fromisoformat(pub)
    fmt = f'| {n_} | {q2}% | {q3}% | {day.strftime("%a")} {day.day} {day.strftime("%b")} |'.replace('-1%', '−1%')
    ok(fmt in prose, f'p-q3: table row {n_}')
ok(dt.date(2025, 9, 30).strftime('%A') == 'Tuesday' and dt.date(2025, 10, 24).strftime('%A') == 'Friday', 'p-q3: weekdays')


def usable(pub):
    d_ = dt.date.fromisoformat(pub) + dt.timedelta(1)
    while d_.weekday() >= 5:
        d_ += dt.timedelta(1)
    return d_


on = dt.date(2025, 10, 24)
known = {n_: (q3 if usable(pub) <= on else q2) for n_, (q2, q3, pub) in co.items()}
left = pd.DataFrame({'date': [pd.Timestamp(on)]})
right = pd.DataFrame([{'date': pd.Timestamp(usable(pub)), 'co': n_, 'g': q3} for n_, (q2, q3, pub) in co.items()]
                     + [{'date': pd.Timestamp('2025-08-15'), 'co': n_, 'g': q2} for n_, (q2, q3, pub) in co.items()])
asof = {n_: pd.merge_asof(left, right[right.co == n_].sort_values('date'), on='date', direction='backward')['g'][0]
        for n_ in co}
num(L2, 'p-q3-earnings-join', 1, F(known['Coral'], 100), asof['Coral'] / 100, {'quarter-end': F(co['Coral'][1], 100)})
srt = sorted(known.values())
q_h = F(srt.index(known['Coral']), 5)
num(L2, 'p-q3-earnings-join', 2, q_h, (pd.Series(asof).rank()['Coral'] - 1) / 5,
    {'over-n': F(srt.index(known['Coral']) + 1, 6),
     'dee-early': F(sorted({**known, 'Jasper': co['Jasper'][1]}.values()).index(known['Coral']), 5)})
leak = {n_: v[1] for n_, v in co.items()}
q_l = F(sorted(leak.values()).index(leak['Coral']), 5)
num(L2, 'p-q3-earnings-join', 3, q_l, (pd.Series(leak).rank()['Coral'] - 1) / 5, {'over-n': F(5, 6)})
bd = pd.bdate_range('2025-09-30', '2025-10-29')
early = sum(1 for d_ in range(30) if (dt.date(2025, 9, 30) + dt.timedelta(d_)) < usable(co['Coral'][2])
            and (dt.date(2025, 9, 30) + dt.timedelta(d_)).weekday() < 5)
num(L2, 'p-q3-earnings-join', 4, early, len(bd), {'from-october': early - 1, 'one-too-many': early + 1})
ok(dt.date(2025, 10, 1).strftime('%A') == 'Wednesday' and len(pd.bdate_range('2025-10-01', '2025-10-29')) == 21,
   'p-q3 p4: 21 October weekdays')
ok(usable(co['Coral'][2]) == dt.date(2025, 10, 30), 'p-q3 p1: Coral usable on 30 October')

# p-shipping-z
wk = [F(20), F(22), F(21), F(25), F(30)]
tr = wk[1:4]
m_tr = sum(tr) / 3
ss_tr = sum((v - m_tr) ** 2 for v in tr)
sd_tr = sp.sqrt(sp.Rational(ss_tr.numerator, ss_tr.denominator) / 2)
num(L2, 'p-shipping-z', 1, sd_tr, np.std([22, 21, 25], ddof=1),
    {'population': np.std([22, 21, 25]), 'variance': ss_tr / 2}, agree=1e-12)
num(L2, 'p-shipping-z', 2, (wk[3] - m_tr) / sd_tr, pd.Series([20, 22, 21, 25, 30.]).pipe(
    lambda x: (x - x.rolling(3).mean()) / x.rolling(3).std())[3],
    {'population': (25 - 22 - F(2, 3)) / np.std([22, 21, 25]), 'no-mean': 25 / 2.08}, agree=1e-12)
ok(abs((25 - float(m_tr)) / 2.08 - 1.12) <= 0.005, 'p-shipping p2: from the rounded sd')
ce = wk[2:5]
m_ce = sum(ce) / 3
num(L2, 'p-shipping-z', 3, m_ce, pd.Series([20, 22, 21, 25, 30.]).rolling(3, center=True).mean()[3], {'trailing': m_tr},
    agree=1e-12)
ss_ce = sum((v - m_ce) ** 2 for v in ce)
z_ce = (wk[3] - m_ce) / sp.sqrt(sp.Rational(ss_ce.numerator, ss_ce.denominator) / 2)
xs5 = pd.Series([20, 22, 21, 25, 30.])
z_ce_pd = ((xs5 - xs5.rolling(3, center=True).mean()) / xs5.rolling(3, center=True).std())[3]
num(L2, 'p-shipping-z', 4, z_ce, z_ce_pd,
    {'population': (25 - 76 / 3) / np.std([21, 25, 30]), 'no-sign': -z_ce, 'trailing': (wk[3] - m_tr) / sd_tr}, agree=1e-12)
ok(abs((25 - 25.33) / 4.51 + 0.07) <= 0.005 and r(float(ss_ce), 2) == 40.67 and r(float(ss_ce / 2), 2) == 20.33
   and r(float(ss_tr), 2) == 8.67 and r(np.std([21, 25, 30], ddof=1), 2) == 4.51, 'p-shipping: stated sums and sds')
pick(L2, 'p-shipping-z', 5, 'future')

# ---------------------------------------------------------------- level 3
L3 = load(3)


def afml(p):
    z_ = (p - 0.5) / math.sqrt(p * (1 - p))
    return 2 * Phi(z_) - 1


def afml_erf(p):  # 2*Phi(z) - 1 = erf(z / sqrt 2), the lesson's one-call form
    return math.erf((p - 0.5) / math.sqrt(p * (1 - p)) / math.sqrt(2))


# p-five-day-sizing
ps = [0.67, 0.77, 0.72, 0.37, 0.42]
ok('0.67, 0.77, 0.72, 0.37 and 0.42' in L3['p-five-day-sizing']['prose'], 'p-five: probabilities stated')
z1 = (0.67 - 0.5) / math.sqrt(0.67 * 0.33)
num(L3, 'p-five-day-sizing', 1, afml(0.67), afml_erf(0.67), {'phi-only': Phi(z1), 'kelly': 2 * 0.67 - 1, 'z-only': z1})
sizes = [afml(q) for q in ps]
said(L3, 'p-five-day-sizing', 2, '0.48, 0.38, −0.21 and −0.13')
ok([r(v, 2) for v in sizes[1:]] == [0.48, 0.38, -0.21, -0.13], 'p-five p2: stated sizes')
stated = [F('0.28'), F('0.48'), F('0.38'), F('-0.21'), F('-0.13')]
pos = [F(round(v * 10), 10) for v in stated]
units = sum(abs(b - a) for a, b in zip([F(0)] + pos, pos))
pos_np = np.round(np.array(sizes) * 10) / 10
units_np = np.abs(np.diff(np.concatenate([[0], pos_np]))).sum()
num(L3, 'p-five-day-sizing', 2, units, units_np,
    {'raw-sizes': sum(abs(b - a) for a, b in zip([F(0)] + stated, stated)), 'no-entry': units - pos[0],
     'positions': sum(abs(v) for v in pos)}, agree=1e-12)
ok(r(float(np.abs(np.diff(np.concatenate([[0], sizes]))).sum()), 2) == 1.25, 'p-five p2: raw sizes trade 1.25 unrounded too')
BOOK, CBP = 5_000_000, F(6, 10000)
cost = units * BOOK * CBP
num(L3, 'p-five-day-sizing', 3, cost, float(units_np) * 5e6 * 0.0006,
    {'raw-sizes': F('1.25') * BOOK * CBP, 'both-ways': 2 * cost, 'bp-slip': units * BOOK * F(6, 1000)}, agree=1e-6)
GROSS = F(5850)
be = GROSS / (units * BOOK) * 10000
lo, hi = 0.0, 100.0
for _ in range(60):  # bisect net(c) = gross - units * book * c / 1e4
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if 5850 - float(units) * 5e6 * mid / 1e4 > 0 else (lo, mid)
num(L3, 'p-five-day-sizing', 4, be, lo, {'per-book': GROSS / BOOK * 10000, 'net': (GROSS - cost) / (units * BOOK) * 10000},
    agree=1e-9)
ok(GROSS - cost == 1950 and units * BOOK == 6_500_000, 'p-five p4: £1,950 kept, £6.5m traded')

# p-trial-log-dsr
log = [('ridge', 1), ('ridge', 10), ('ridge', 1), ('ridge', 100), ('forest', 4), ('forest', 4), ('forest', 8)]
ok(L3['p-trial-log-dsr']['prose'].count('\n- ') == len(log), 'p-trial: log length')
N5 = len(set(log))
num(L3, 'p-trial-log-dsr', 1, N5, len(dict.fromkeys(log)), {'runs': len(log), 'one': 1})
n_, V_ = 1260, 1 / 1259


def emax(N_, V):
    return math.sqrt(V) * ((1 - EG) * iPhi(1 - 1 / N_) + EG * iPhi(1 - 1 / (N_ * math.e)))


E5 = emax(N5, V_)
sims = rng.standard_normal((40000, N5)).max(axis=1) * math.sqrt(V_)   # best of 5 noise Sharpes
# the closed form runs high for small N: exact mean of the best of 5 normals by integration, then a simulation
xg = np.linspace(-9, 9, 200001)
e_exact = float(np.sum(xg * 5 * ND.pdf(0) * np.exp(-xg ** 2 / 2) * np.vectorize(Phi)(xg) ** 4) * (xg[1] - xg[0]))
ok(abs(e_exact - 1.16296) < 1e-4 and abs(sims.mean() / math.sqrt(V_) / e_exact - 1) < 0.01, 'p-trial p2: exact best of 5')
ok(0 < E5 / math.sqrt(V_) / e_exact - 1 < 0.03, 'p-trial p2: the formula is within 3% above the exact mean')
num(L3, 'p-trial-log-dsr', 2, E5 * math.sqrt(252),
    math.sqrt(V_) * (0.4228 * iPhi(0.8) + 0.5772 * iPhi(1 - 1 / (5 * math.e))) * math.sqrt(252),
    {'runs': emax(7, V_) * math.sqrt(252), 'daily': E5}, agree=2e-4)
ok([r(iPhi(0.8), 3), r(iPhi(1 - 1 / (5 * math.e)), 3), r(1 - 1 / (5 * math.e), 3)] == [0.842, 1.45, 0.926]
   and r(0.4228 * 0.842 + 0.5772 * 1.450, 3) == 1.193, 'p-trial p2: stated quantiles and bracket')
SRd = 1.3 / math.sqrt(252)
g3, g4 = -0.3, 4.0
se_t = math.sqrt((1 - g3 * SRd + (g4 - 1) / 4 * SRd ** 2) / (n_ - 1))
SRs = sp.Rational(13, 10) / sp.sqrt(252)
se_s = sp.sqrt((1 - sp.Rational(-3, 10) * SRs + sp.Rational(3, 4) * SRs ** 2) / 1259)
num(L3, 'p-trial-log-dsr', 3, se_s, se_t,
    {'annual': math.sqrt((1 + 0.3 * 1.3 + 0.75 * 1.69) / 1259), 'normal': math.sqrt((1 + 0.5 * SRd ** 2) / 1259),
     'skew-sign': math.sqrt((1 + g3 * SRd + 0.75 * SRd ** 2) / 1259)}, agree=1e-12)
ok(r(SRd, 4) == 0.0819 and r(0.3 * SRd, 4) == 0.0246 and r(0.75 * SRd ** 2, 4) == 0.005
   and r(1 - g3 * SRd + 0.75 * SRd ** 2, 4) == 1.0296, 'p-trial p3: stated terms')
dsr = Phi((SRd - E5) / se_t)
dsr_rounded = Phi((0.0819 - 0.53 / math.sqrt(252)) / 0.0286)
num(L3, 'p-trial-log-dsr', 4, dsr, dsr_rounded,
    {'runs': Phi((SRd - emax(7, V_)) / se_t), 'psr-zero': Phi(SRd / se_t)}, agree=2e-3)
ok(r((0.0819 - 0.0336) / 0.0286, 2) == 1.69 and r(Phi(1.69), 3) == 0.954, 'p-trial p4: stated z and Phi')
# simulated DSR check: share of noise searches whose best beats the reported Sharpe is small
ok(np.mean(sims >= SRd) < 0.05, 'p-trial p4: noise rarely reaches 0.0819 with 5 trials')

# p-futures-net-psr
G, SD, TO, C9, n3 = F(6), F(75), F('0.35'), F(9), 750
cday = TO * C9
num(L3, 'p-futures-net-psr', 1, cday, 0.35 * 9, {'divided': C9 / TO, 'both-ways': 2 * cday}, agree=1e-12)
pnl = rng.normal(6e-4, 75e-4, 2_000_000)  # simulate gross P&L, subtract the cost line, re-measure the Sharpe
net_sim = pnl - 0.35 * 9e-4
SR_net = (G - cday) / SD
num(L3, 'p-futures-net-psr', 2, SR_net * sp.sqrt(252), net_sim.mean() / net_sim.std() * math.sqrt(252),
    {'gross': G / SD * math.sqrt(252), 'daily': SR_net}, agree=0.02)
ok(SR_net == F(38, 1000) and r(math.sqrt(252), 2) == 15.87 and r(float(G / SD) * math.sqrt(252), 2) == 1.27,
   'p-futures p2: stated figures')
sr = 0.038
se_f = math.sqrt((1 + 0.6 * sr + 1 * sr ** 2) / (n3 - 1))
se_f_s = sp.sqrt((1 + sp.Rational(6, 10) * sp.Rational(38, 1000) + sp.Rational(38, 1000) ** 2) / 749)
num(L3, 'p-futures-net-psr', 3, se_f_s, se_f,
    {'normal': math.sqrt((1 + 0.5 * sr ** 2) / 749), 'annual': math.sqrt((1 + 0.6 * 0.6032 + 0.6032 ** 2) / 749)},
    agree=1e-12)
ok(r(1 + 0.6 * sr + sr ** 2, 4) == 1.0242 and r(0.6 * sr, 4) == 0.0228 and r(sr ** 2, 4) == 0.0014, 'p-futures p3: terms')
psr = Phi(sr / se_f)
sr_g = 0.08
se_g = math.sqrt((1 + 0.6 * sr_g + sr_g ** 2) / 749)
num(L3, 'p-futures-net-psr', 4, psr, Phi(0.038 / 0.0370),
    {'gross': Phi(sr_g / se_g), 'normal': Phi(sr / math.sqrt((1 + 0.5 * sr ** 2) / 749))}, agree=1e-3)
ok(r(0.038 / 0.0370, 2) == 1.03 and r(Phi(1.03), 3) == 0.848, 'p-futures p4: stated z and Phi')

# p-calibrated-kelly
b = F(9, 5)


def kelly(p):
    return p - (1 - p) / b


def growth(f, p):
    return p * np.log(1 + 1.8 * f) + (1 - p) * np.log(1 - f)


fgrid = np.linspace(0, 0.6, 600001)
num(L3, 'p-calibrated-kelly', 1, kelly(F(47, 100)), fgrid[np.argmax(growth(fgrid, 0.47))],
    {'even-odds': 2 * F(47, 100) - 1, 'times-b': F(47, 100) - F(53, 100) * b}, agree=2e-6)
num(L3, 'p-calibrated-kelly', 2, kelly(F(44, 100)), fgrid[np.argmax(growth(fgrid, 0.44))],
    {'even-odds': 2 * F(44, 100) - 1, 'raw': kelly(F(47, 100))}, agree=2e-6)
fr, ftr = float(kelly(F(47, 100))), float(kelly(F(44, 100)))
wins = rng.random(4_000_000) < 0.44
g_mc = np.where(wins, math.log(1 + 1.8 * fr), math.log(1 - fr)).mean()
num(L3, 'p-calibrated-kelly', 3, growth(fr, 0.44), g_mc,
    {'raw-p': growth(fr, 0.47), 'even-payout': 0.44 * math.log(1 + fr) + 0.56 * math.log(1 - fr)}, agree=3e-4)
ok(abs(growth(0.176, 0.44) - 0.0127) <= 0.00006, 'p-calibrated p3: rounded stake in band')
share = growth(fr, 0.44) / growth(ftr, 0.44)
num(L3, 'p-calibrated-kelly', 4, share, growth(0.176, 0.44) / growth(0.129, 0.44),
    {'inverse': 1 / share, 'stake-ratio': ftr / fr}, agree=3e-3)
ok(r(growth(ftr, 0.44), 4) == 0.0145 and r(growth(fr, 0.44), 6) == 0.012717 and r(growth(ftr, 0.44), 6) == 0.014529
   and r(fr / ftr - 1, 2) == 0.36, 'p-calibrated p4: stated growths and oversize')
ok([r(1 + 1.8 * fr, 3), r(1 - fr, 3), r(1 + 1.8 * ftr, 3), r(1 - ftr, 3)] == [1.316, 0.824, 1.232, 0.871],
   'p-calibrated: stated multipliers')
pick(L3, 'p-calibrated-kelly', 5, 'calibrate')

print(f'{checks - len(fails)} of {checks} checks pass')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
