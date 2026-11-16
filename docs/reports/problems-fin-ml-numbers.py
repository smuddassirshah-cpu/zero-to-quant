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

if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == '--level1':
    pass

print(f'{checks - len(fails)} of {checks} checks pass')
for f_ in fails:
    print('FAIL', f_)
sys.exit(1 if fails else 0)
