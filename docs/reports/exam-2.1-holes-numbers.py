"""topic-2.1, stat-learning level 4 items (Option B, skill sl-flexible): every new key computed twice.

Run: <scratchpad>/venv/bin/python docs/reports/exam-2.1-holes-numbers.py   (exit 0 when all pass; NumPy, scikit-learn 1.6.1)
Route 1 is the working the item prints; route 2 is independent: geometry instead of decision values, scikit-learn's KMeans
and a brute-force partition search, a finite-difference gradient, SplineTransformer-free slope read from evaluations.
The script then reads app/content/exams/topic-2.1.json and checks keys, wrong values and the replaced items.
"""
import json, math, os, sys
from itertools import product
import numpy as np
from sklearn.cluster import KMeans

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import _numbers  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', 'app', 'content', 'exams', 'topic-2.1.json')
doc = json.load(open(EXAM, encoding='utf8'))
items = {i['id']: i for i in doc['items']}
fails, n = [], [0]


def check(ok, label):
    n[0] += 1
    print(('ok  ' if ok else 'BAD ') + label)
    if not ok:
        fails.append(label)


def band(t):
    return t.get('abs', 0) if isinstance(t, dict) else t


def numeric(iid, key, wrongs):
    it = items[iid]; w = it['widget']
    a, t = w['answer'], band(w['tol'])
    check(abs(a - key) <= max(t, 1e-9), f'{iid} key {a} = computed {key:.6g}')
    got = {x['id']: x for x in w.get('wrong', [])}
    check(set(got) == set(wrongs), f'{iid} wrong ids {sorted(got)}')
    for k, v in wrongs.items():
        x = got[k]
        check(abs(x['value'] - v) <= band(x['tol']) + 1e-9, f'{iid} wrong {k} {x["value"]} = slip {v:.6g}')
        check(abs(x['value'] - a) > t + band(x['tol']), f'{iid} wrong {k} outside the key band')
        check(k in it['feedback']['byKey'], f'{iid} wrong {k} has a byKey line')
    sc = 100 if w.get('unit') == '%' else 1          # a % part: the key is the fraction, the text prints the percentage
    check(any(abs(x - a * sc) <= max(t, 1e-9) * sc for x in _numbers(it['explain']['text'])), f'{iid} explanation states the key')


# e-spline-slope: f(m) = 4 - m + 2(m - 3)^+ + 1.5(m - 7)^+
f = lambda m: 4 - m + 2 * max(0, m - 3) + 1.5 * max(0, m - 7)
r1 = -1 + 2 + 1.5
r2 = np.polyfit(np.linspace(7.5, 20, 26), [f(m) for m in np.linspace(7.5, 20, 26)], 1)[0]
check(r1 == 2.5 and abs(r2 - 2.5) < 1e-9, f'spline-slope 2.5: coefficient sum and a least-squares slope past 7 ({r2:.6f})')
check(abs((f(6) - f(4)) / 2 - 1) < 1e-12, 'spline-slope slope 1 between the knots')
numeric('e-spline-slope', r1, {'last-hinge': 1.5, 'no-base': 2 + 1.5, 'base-sign': 1 + 2 + 1.5})

# e-street-inside: w = (2, -1), b = 1
w, b = np.array([2.0, -1.0]), 1.0
opts = items['e-street-inside']['widget']['options']
for o in opts:
    pt = np.array([float(v) for v in o['text'].strip('$()').split(',')])
    val = float(w @ pt + b)
    inside1 = -1 < val < 1
    dist = val / np.linalg.norm(w)                  # signed distance to the centre line
    inside2 = abs(dist) < 1 / np.linalg.norm(w) - 1e-12   # half-width of the street is 1 / |w|
    check(inside1 == inside2 == bool(o.get('correct')), f'street-inside {o["text"]} value {val:+.2f}, inside {inside1} (value and geometry agree)')
vals = sorted(round(float(w @ np.array(p) + b), 6) for p in [(0.2, 0.9), (-0.5, 0.5), (-1, -1.4), (1, 0), (0, 2.5), (0, 0)])
check(vals == [-1.5, -0.5, 0.4, 0.5, 1.0, 3.0], f'street-inside printed values {vals}')

# e-kmeans-spreads
x = np.array([2, 3, 7, 11, 12, 13, 22], dtype=float)
c = np.array([2.0, 3.0]); hist = []
while True:
    lab = np.argmin(np.abs(x[:, None] - c[None, :]), axis=1)
    newc = np.array([x[lab == k].mean() for k in range(2)])
    hist.append(newc.copy())
    if np.allclose(newc, c):
        break
    c = newc
inertia = float(((x - c[lab]) ** 2).sum())
km = KMeans(2, init=np.array([[2.0], [3.0]]), n_init=1).fit(x[:, None])
check(abs(inertia - 91) < 1e-9 and abs(km.inertia_ - 91) < 1e-9 and sorted(km.cluster_centers_.ravel()) == [4, 14.5],
      f'kmeans-spreads 91: hand Lloyd loop and sklearn KMeans ({km.inertia_:.4f})')
check([list(np.round(h, 2)) for h in hist] == [[2, 11.33], [2.5, 13], [4, 14.5], [4, 14.5]], f'kmeans-spreads centre path {[list(np.round(h, 2)) for h in hist]}')
best = min(float(((x[:k] - x[:k].mean()) ** 2).sum() + ((x[k:] - x[k:].mean()) ** 2).sum()) for k in range(1, 7))
check(abs(best - 91) < 1e-9, 'kmeans-spreads 91 is also the best split of the sorted spreads (brute force)')
early = float(((x[:2] - 2.5) ** 2).sum() + ((x[2:] - 13) ** 2).sum())
unsq = float(np.abs(x - c[lab]).sum())
check(abs(7 - 2.5) < abs(7 - 13), 'kmeans-spreads at 2.5 and 13 the bond at 7 still moves')
numeric('e-kmeans-spreads', inertia, {'early-stop': early, 'unsquared': unsq})

# e-unit-gradient
x1, x2, y, w1, w2, bb, v = 1.0, 3.0, 1.0, 0.5, -0.2, 0.4, 2.0
def loss(w1_, w2_, v_):
    return 0.5 * (v_ * max(0.0, w1_ * x1 + w2_ * x2 + bb) - y) ** 2
z = w1 * x1 + w2 * x2 + bb; h = max(0, z); yhat = v * h
g1 = (yhat - y) * v * x2
eps = 1e-6
g2 = (loss(w1, w2 + eps, v) - loss(w1, w2 - eps, v)) / (2 * eps)
check(abs(z - 0.3) < 1e-12 and abs(yhat - 0.6) < 1e-12, 'unit-gradient unit on: input 0.3, prediction 0.6')
check(abs(g1 + 2.4) < 1e-12 and abs(g2 + 2.4) < 1e-6, f'unit-gradient -2.4: chain rule and finite difference ({g2:.8f})')
gv = (loss(w1, w2, v + eps) - loss(w1, w2, v - eps)) / (2 * eps)
check(abs(gv + 0.12) < 1e-6, 'unit-gradient dL/dv = -0.12 (the slope-v slip) by finite difference')
check(loss(w1, w2 + 0.01 * 2.4, v) < loss(w1, w2, v), 'unit-gradient a step against the slope lowers the loss')
numeric('e-unit-gradient', g1, {'used-x1': (yhat - y) * v * x1, 'slope-v': (yhat - y) * h, 'sign': -g1, 'no-half': 2 * g1})

# e-odds-update (back in place of e-report-which, review-holes-1.6-2.1 finding 4): logistic coefficient read as odds
odds2 = 0.10 / 0.90 * math.exp(0.45 * 2)            # route 1: odds times e^(0.45 x 2 turns)
p1 = odds2 / (1 + odds2)
logit2 = math.log(0.10 / 0.90) + 0.45 * 2            # route 2: add on the log-odds scale, then the logistic function
p2 = 1 / (1 + math.exp(-logit2))
check(abs(p1 - p2) < 1e-12 and abs(p1 - 0.2146) < 5e-5, f'odds-update probability {p1:.4f} two ways ({p2:.4f})')
check(abs(odds2 - 0.2733) < 5e-5 and abs(0.1 * math.exp(0.9) - 0.2460) < 5e-5, 'odds-update odds 0.273 and the multiplied probability 0.246')
check(abs(round(0.273 / 1.273, 3) - 0.214) < 1e-12 and abs(0.273 / 1.273 - 0.215) <= 0.0015, 'odds-update the printed 0.273 / 1.273 is inside the band')
numeric('e-odds-update', p1, {'prob-times': 0.1 * math.exp(0.9), 'odds-as-prob': odds2})
check(items['e-odds-update']['widget']['unit'] == '%' and items['e-odds-update']['skills'] == ['sl-classify'], 'odds-update unit % and skill sl-classify')
check('e-report-which' not in items, 'e-report-which is out (its choice-on-validation point is in e-code-honest-report and e-best-of-n)')
for pid in ('e-spline-slope', 'e-kmeans-spreads'):
    check(items[pid]['widget']['placeholder'] == 'a number', f'{pid} placeholder invites no unit words')

# replaced items gone, every skill still covered, ramp
gone = ['e-leak-rows', 'e-oob-overlap', 'e-report-which', 'e-ridge-shrink', 'e-walk-first-test']
check(not any(g in items for g in gone), 'five dropped items out (e-odds-update back, e-report-which out)')
used = {s for i in doc['items'] for s in i.get('skills', [])}
check(set(doc['skills']) <= used, 'every exam skill covered')
for s in ('vl-leakage', 'vl-time', 'en-bagging', 'sl-classify', 'sl-regularise', 'vl-cv'):
    k = sum(s in i.get('skills', []) for i in doc['items'])
    check(k >= 2, f'{s} still examined by {k} items')
cnt = {d: sum(1 for i in doc['items'] if i['difficulty'] == d) for d in (2, 3, 4, 5)}
N = len(doc['items'])
for d, s in {2: .2, 3: .5, 4: .2, 5: .1}.items():
    check(abs(cnt[d] / N - s) <= 0.1 + 1e-9, f'ramp d{d} {cnt[d]}/{N}')
check(N == 30, '30 items')
print(f'{n[0] - len(fails)} of {n[0]} checks passed')
sys.exit(1 if fails else 0)
