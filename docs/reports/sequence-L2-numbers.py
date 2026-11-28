"""Recompute every number stated in sequence level 2 (Attention as a soft lookup) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only sequence-L2
(NumPy only; well under a minute; strict coverage; exits 0 when every check passes).

Route A is the closed form or the lesson's formula; route B is independent: a sorted list against argsort, a log-sum-exp
against the direct softmax, a loop over queries against the vectorised sweep, central differences against the analytic
slope and against the autograd, a hand-written attention backward pass against autograd.py with seq_ops_l2.py. The new
module seq_ops_l2.py (softmax along an axis, swap of the last two axes) is gradient-checked here in float64. Every code
widget is run in CPython with the page's judge: the solution passes, the starter fails, each mutant first fails its test.
"""
import hashlib
import math
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

sys.path.insert(0, DATA)
from autograd import Tensor, grad_check  # noqa: E402
import seq_ops_l2 as S2  # noqa: E402

lv = Level('sequence', 2, coverage='strict')
E = lv.expect
LIT = lv.literal
e = math.e


def two(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol * max(1.0, abs(a), abs(b)), f'{label}: routes agree ({a!r} vs {b!r})')
    return a


def F(fid):
    return lv._file(fid)[1]


def sm(s, axis=-1):
    s = np.asarray(s, float)
    z = np.exp(s - s.max(axis=axis, keepdims=True))
    return z / z.sum(axis=axis, keepdims=True)


def sm_lse(s):   # route B: exp(s - logsumexp(s)) computed by a loop
    s = [float(x) for x in s]
    m = max(s)
    lse = m + math.log(sum(math.exp(x - m) for x in s))
    return np.array([math.exp(x - lse) for x in s])


# ---------------- frozen and new modules ----------------
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'autograd.py'), 'rb').read()).hexdigest().startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
OPS = open(os.path.join(DATA, 'seq_ops_l2.py'), 'rb').read()
print('seq_ops_l2.py SHA-256', hashlib.sha256(OPS).hexdigest(), len(OPS), 'bytes')
g = np.random.default_rng(0)
for shape, axis, scale in (((5,), -1, 1.0), ((3, 4), -1, 1.0), ((3, 4), 0, 3.0), ((2, 3, 4), -1, 1.0), ((2, 3, 4), 1, 10.0)):
    X = Tensor(scale * g.standard_normal(shape))
    W = g.standard_normal(shape)
    lv.claim(grad_check(lambda: (S2.softmax(X, axis=axis) * W).sum(), [X]) < 1e-6, f'softmax {shape} axis {axis}: autograd against central differences')
    lv.claim(np.allclose(S2.softmax(X, axis=axis).data, sm(X.data, axis)), f'softmax {shape} axis {axis}: forward equals NumPy')
X = Tensor(np.array([[1000.0, 999.0, -1000.0]]))
lv.claim(np.allclose(S2.softmax(X).data, sm_lse([1000, 999, -1000])[None]) and np.isfinite(S2.softmax(X).data).all(), 'softmax with scores near 1,000 stays finite')
A = Tensor(g.standard_normal((2, 3, 4)))
Wt = g.standard_normal((2, 4, 3))
lv.claim(grad_check(lambda: (S2.swap_last(A) * Wt).sum(), [A]) < 1e-6 and S2.swap_last(A).shape == (2, 4, 3), 'swap_last on a stack: shape and gradient')
B = Tensor(g.standard_normal((3, 3)))
lv.claim(grad_check(lambda: (S2.softmax(B @ S2.swap_last(B)) * B).sum(), [B]) < 1e-6, 'a node used twice (B and its transpose) accumulates')

# ---------------- l5 ----------------
L5 = 'l5-'
K = np.array([[-1, 1.5], [1, 1], [-0.5, 0.5], [1.5, 0.5], [-1.5, 0], [0.5, 0], [-1, -0.5], [0, -1], [1.5, -1], [0.5, -1.5]], float)
V = np.array([-0.8, -0.5, 0.2, 0.6, 0.1, 0.4, 0.9, -0.3, -1.1, 1.2])
pts = F(L5)['screens'][0]['canvas']['state']['points']
lv.claim(all(abs(p['x'] - K[i, 0]) + abs(p['y'] - K[i, 1]) < 1e-12 for i, p in enumerate(pts[:10])), 'the ten keys are stat-learning l4\'s grid days')
d = np.hypot(*(K - [0, 0]).T)
srt = sorted(range(10), key=lambda i: (math.hypot(*K[i]), i))
lv.claim(list(np.argsort(d, kind='stable')[:3]) == srt[:3], 'nearest three: argsort against a sorted list')
E(L5, 'screens[0].widget.answer', -1.1); E(L5, 'screens[1].widget.answer', V[srt[0]]); E(L5, 'screens[1].widget.wrong[0].value', V[srt[1]])
lv.claim(round(d[srt[1]], 2) == 0.71 and d[srt[0]] == 0.5 and d[srt[2]] == 1.0, 'distances 0.5, 0.71, 1', covers=[0.71, 0.5])
two('3-NN', float(np.mean(V[srt[:3]])), (0.4 + 0.2 - 0.3) / 3); E(L5, 'screens[2].widget.answer', 0.1); E(L5, 'screens[2].widget.wrong[0].value', 0.3)
two('tie distances', math.hypot(0.25 - 0.5, -0.5), math.hypot(0.25, -0.5 + 1)); lv.claim(round(math.hypot(0.25, 0.5), 3) == 0.559 and abs(0.0625 + 0.25 - 0.3125) < 1e-12, 'tie at 0.559 = sqrt(0.3125)', covers=[0.559, 0.3125, 0.0625])
E(L5, 'screens[5].widget.answer', 0.4); E(L5, 'screens[5].widget.wrong[1].value', 0.05)
E(L5, 'screens[3].widget.wrong[0].value', 0.2)
lv.claim(round(math.hypot(1.2, 0.5), 2) == 1.3 and round(math.hypot(0.8, 0.5), 3) == 0.943 and round(math.hypot(1.2, 2.5), 2) == 2.77, 'quiz distances 1.3, 0.94, 2.77', covers=[1.3, 0.94, 2.77, 0.64, 0.25])
LIT('0.002', why='the width 2h of the central difference in the flat-slope quiz, a given')
LIT('0.001', why='the step h of the central difference in the flat-slope quiz, a given')

# ---------------- l6 ----------------
L6 = 'l6-'
soft0 = float(sm(-((K - 0) ** 2).sum(1) / 0.5) @ V)
two('soft forecast at today, tau 0.5', soft0, float(sm_lse(-((K) ** 2).sum(1) / 0.5) @ V))
E(L6, 'screens[0].widget.answer', round(soft0, 3)); E(L6, 'screens[0].widget.wrong[1].value', round(float(V.mean()), 3))
w1, w2 = sm([2, 1, 0]), sm(np.array([2, 1, 0]) / 2)
two('0.665', float(w1[0]), e ** 2 / (e ** 2 + e + 1)); two('0.506', float(w2[0]), e / (e + e ** 0.5 + 1))
E(L6, 'screens[1].widget.answer', round(float(w1[0]), 3)); E(L6, 'screens[2].widget.answer', round(float(w2[0]), 3))
lv.claim(round(e ** 2, 3) == 7.389 and round(e ** 2 + e + 1, 3) == 11.107 and round(e ** 0.5, 3) == 1.649 and round(e + e ** 0.5 + 1, 3) == 5.367 and round(e, 3) == 2.718, 'shown exponentials', covers=[7.389, 11.107, 1.649, 5.367, 2.718])
E(L6, 'screens[1].explain.text', round(float(w1[1]), 3)); E(L6, 'screens[1].explain.text', round(float(w1[2]), 3))


def make_knn(n, seed):
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, (n, 2))
    signal = (0.8 * X[:, 0] * np.tanh(2 * X[:, 1]) - 0.3 * X[:, 1] ** 2 + 0.3)
    y = (signal + rng.normal(0, 0.7, n)).round(2)
    return X, y


X, y = make_knn(300, 11)
Xtr, ytr, Xte, yte = X[:200], y[:200], X[200:], y[200:]
TAUS = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
mseA = [float(np.mean((sm(-((Xte[:, None] - Xtr[None]) ** 2).sum(-1) / t, 1) @ ytr - yte) ** 2)) for t in TAUS]
mseB = [float(np.mean([(float(sm_lse(-((Xtr - xq) ** 2).sum(1) / t) @ ytr) - yv) ** 2 for xq, yv in zip(Xte, yte)])) for t in TAUS]
lv.claim(np.allclose(mseA, mseB, rtol=1e-9), 'tau sweep: vectorised against a loop over held-out days')
lv.claim(F(L6)['screens'][3]['canvas']['params']['series'][0]['values'] == [round(v, 4) for v in mseA], 'the chart holds the sweep')
best = TAUS[int(np.argmin(mseA))]
E(L6, 'screens[3].widget.answer', best); E(L6, 'screens[3].hints[2].text', round(min(mseA), 4)); E(L6, 'screens[3].feedback.byKey.small', round(mseA[0], 4)); E(L6, 'screens[3].feedback.byKey.large', round(mseA[-1], 4))
two('training mean', float(np.mean((ytr.mean() - yte) ** 2)), 1.0082, 5e-5)
a1 = sm(-(K ** 2).sum(1))
yh = float(a1 @ V)
gx = float(np.sum(a1 * (V - yh) * 2 * K[:, 0]))
gy = float(np.sum(a1 * (V - yh) * 2 * K[:, 1]))


def soft_at(q):
    return float(sm(-((K - q) ** 2).sum(1)) @ V)


h = 1e-6
two('slope x: formula against central differences', gx, (soft_at([h, 0]) - soft_at([-h, 0])) / (2 * h), 1e-7)
two('slope y: formula against central differences', gy, (soft_at([0, h]) - soft_at([0, -h])) / (2 * h), 1e-7)
E(L6, 'screens[4].widget.answer', round(gx, 3)); E(L6, 'screens[4].explain.text', round(gy, 3)); E(L6, 'screens[4].hints[2].text', round(gx, 4))
rows = F(L6)['screens'][4]['canvas']['params']['rows']
terms = a1 * (V - yh) * 2 * K[:, 0]
lv.claim(all(abs(float(r[2].replace('−', '-')) - t) < 5e-5 for r, t in zip(rows, terms)), 'the table terms', covers=[round(float(t), 4) for t in terms])
ov = sm([1000.0, 999.0])
two('stable softmax 1000, 999', float(ov[0]), 1 / (1 + math.exp(-1))); E(L6, 'screens[6].widget.answer', round(float(ov[0]), 4)); E(L6, 'screens[6].explain.text', round(float(ov[1]), 4))
lv.claim(round(math.exp(-1), 4) == 0.3679, 'e^-1', covers=[0.3679, 1.3679])
fc = 0.6 * 1.2 + 0.3 * -0.4 + 0.1 * 0.5
two('transfer forecast', fc, 0.72 - 0.12 + 0.05); E(L6, 'screens[9].widget.answer', round(fc, 2)); E(L6, 'screens[9].widget.wrong[0].value', round((1.2 - 0.4 + 0.5) / 3, 2))
E(L6, 'quiz[0].widget.answer', round(float(sm([3, 1])[0]), 3))

# ---------------- l7 ----------------
L7 = 'l7-'
q = np.array([1.0, 2.0]) @ np.array([[1.0, 0.0], [0.5, 1.0]])
k = np.array([1.0, -1.0]) @ np.array([[1.0, 1.0], [0.0, 1.0]])
lv.claim(q.tolist() == [2, 2] and k.tolist() == [1, 0], 'q = (2, 2), k = (1, 0)')
E(L7, 'screens[0].widget.answer', float(q @ k)); E(L7, 'screens[0].widget.wrong[0].value', -1.0); E(L7, 'screens[0].widget.wrong[1].value', 4.0)
o1 = float(sm([1, 0, 1]) @ [2, 4, 9])
two('one output row', o1, (11 * e + 4) / (2 * e + 1)); E(L7, 'screens[2].widget.answer', round(o1, 4))
lv.claim(round(e / (2 * e + 1), 4) == 0.4223 and round(1 / (2 * e + 1), 4) == 0.1554 and round(2 * e / (2 * e + 1), 4) == 0.8446 and round(4 / (2 * e + 1), 4) == 0.6214 and round(9 * e / (2 * e + 1), 4) == 3.8009, 'shown weights and products', covers=[0.4223, 0.1554, 0.8446, 0.6214, 3.8009])
E(L7, 'screens[2].widget.wrong[2].value', 5.5)
rw, cw = sm([[1.0, 0.0], [3.0, 0.0]], 1), sm([[1.0, 0.0], [3.0, 0.0]], 0)
E(L7, 'screens[4].widget.answer', round(float(rw[0, 0]), 4)); E(L7, 'screens[4].widget.wrong[0].value', round(float(cw[0, 0]), 4)); E(L7, 'screens[4].explain.text', round(float(rw[0, 1]), 4))
two('column slip', float(cw[0, 0]), 1 / (1 + e ** 2))
lv.claim(abs(float(sm([0.7])[0]) - 1) < 1e-15, 'one key: weight 1 whatever the score', covers=[0.7])

# ---------------- l8 ----------------
L8 = 'l8-'


def dv(dd, n, seed, route='A'):
    r = np.random.default_rng(seed)
    qq, kk = r.standard_normal((n, dd)), r.standard_normal((n, dd))
    s = (qq * kk).sum(1)
    return float(np.var(s)) if route == 'A' else float(np.mean((s - s.mean()) ** 2))


v64, v16, v4 = (two(f'simulated variance d = {dd}', dv(dd, 20000, 1), dv(dd, 20000, 1, 'B')) for dd in (64, 16, 4))
lv.claim(abs(v64 - 64) < 1.5 and abs(v16 - 16) < 0.5 and abs(v4 - 4) < 0.2, 'simulations near d')
E(L8, 'screens[1].explain.text', round(v64, 2)); E(L8, 'screens[2].prose', round(v16, 2)); E(L8, 'screens[2].prose', round(v4, 2)); E(L8, 'screens[2].feedback.correct', round(math.sqrt(v16), 3))
lv.claim(round(v64, 2) == 63.73, 'the brief writer\'s 63.7 from seed 1 reproduced', covers=[63.73])


def sat(dd, seed):
    r = np.random.default_rng(seed)
    qq = r.standard_normal(dd)
    KK = r.standard_normal((16, dd))
    s = KK @ qq
    return float(sm(s).max()), float(sm(s / math.sqrt(dd)).max()), float(sm(s / dd).max()), float(sm_lse(s).max())


s64, s4 = sat(64, 4), sat(4, 4)
two('saturation route B', s64[0], s64[3])
for path in ('screens[0].explain.text', 'screens[5].explain.text', 'screens[8].feedback.correct'):
    E(L8, path, round(s64[0], 4))
E(L8, 'screens[0].explain.text', round(s4[0], 4)); E(L8, 'screens[5].explain.text', round(s64[1], 4)); E(L8, 'screens[6].explain.text', round(s64[2], 4))
lv.claim(s64[0] > 0.99 and s4[0] < 0.5 and s64[2] < 0.1, 'seed 4: saturated at 64, not at 4; dividing by d flattens')
sw = 1 / (1 + math.exp(-8))
sl = sw * (1 - sw)
two('sigmoid slope at 8', sl, math.exp(-8) / (1 + math.exp(-8)) ** 2); E(L8, 'screens[3].widget.answer', round(sl, 6)); E(L8, 'screens[3].widget.wrong[1].value', round(sw, 6))
lv.claim(round(0.25 / sl, -1) == 750 and round(sw, 4) == 0.9997 and round(sw, 5) == 0.99966 and round(1 - sw, 5) == 0.00034, '750 times smaller; 0.9997', covers=[750, 0.9997, 0.99966, 0.00034])
two('16/8', 16 / math.sqrt(64), 2.0); two('/d spread', 8 / 64, 0.125); E(L8, 'screens[6].widget.answer', 0.125); E(L8, 'screens[6].widget.wrong[1].value', round(1 / 64, 4))
two('edge sd', math.sqrt(81 * 64 / 64), 9.0); lv.claim(3 ** 2 * 3 ** 2 == 81, 'product variance 81 for entries of sd 3', covers=[81]); two('transfer sd', math.sqrt(100), 10.0)
lv.claim(round(math.sqrt(512), 1) == 22.6, 'sqrt 512', covers=[22.6])
E(L8, 'quiz[1].widget.wrong[0].value', round(24 / 36, 4))

# ---------------- review, problems, homework ----------------
w3 = sm([3, 1, 0])
two('review softmax', float(w3[0]), e ** 3 / (e ** 3 + e + 1)); E('review', 'items[0].widget.answer', round(float(w3[0]), 4))
lv.claim(round(e ** 3, 3) == 20.086, 'e cubed', covers=[20.086])
lv.claim(math.hypot(2, 1.5) == 2.5 and abs(math.hypot(1, 0.5) - math.sqrt(1.25)) < 1e-12 and abs(math.hypot(1, 0.5) - math.hypot(-1, 0.5)) < 1e-12, 'review distances 2.5, 1.12, 1.12 (a tie)', covers=[2.5, 1.12, 1.25])
E('review', 'items[6].widget.wrong[0].value', round(12 / 9, 4)); E('review', 'items[7].widget.wrong[1].value', round(7.5 * math.exp(-2), 4)); E('review', 'items[8].widget.answer', 0.3)
s = np.array([2, 2, 3]) / math.sqrt(2)
w = sm(s)
two('scaled weight', float(w[2]), 1 / (1 + 2 * math.exp(-1 / math.sqrt(2)))); E('problems', 'items[0].parts[2].widget.answer', round(float(w[2]), 4))
E('problems', 'items[0].parts[1].widget.answer', round(3 / math.sqrt(2), 4)); E('problems', 'items[0].parts[2].widget.wrong[0].value', round(float(sm([2, 2, 3])[2]), 4))
out = float(w @ [10, 20, 30]); E('problems', 'items[0].parts[3].widget.answer', round(out, 2))
lv.claim(round(float(w[0]), 4) == 0.2483 and round(float(w[2]), 4) == 0.5035 and round(math.sqrt(2), 4) == 1.4142 and round(1 / math.sqrt(2), 4) == 0.7071, 'shown problem weights', covers=[0.2483, 0.5035, 1.4142, 0.7071, 2.1213])
wt1 = sm([0, -1, -4])
two('problem weights tau 1', float(wt1[0]), float(sm_lse([0, -1, -4])[0]))
E('problems', 'items[1].parts[0].widget.answer', round(float(wt1[0]), 4)); E('problems', 'items[1].parts[0].explain.text', round(float(wt1[1]), 4)); E('problems', 'items[1].parts[0].explain.text', round(float(wt1[2]), 4))
f1 = float(wt1 @ [1, 2, 4]); f025 = float(sm([0, -4, -16]) @ [1, 2, 4]); f2 = float(sm([0, -0.5, -2]) @ [1, 2, 4])
E('problems', 'items[1].parts[1].widget.answer', round(f1, 4)); E('problems', 'items[1].parts[1].widget.wrong[0].value', round(7 / 3, 4)); E('problems', 'items[1].parts[2].widget.answer', round(f025, 4))
E('problems', 'items[1].parts[2].widget.wrong[1].value', round(float(sm(np.array([0, -1, -4]) * 0.25) @ [1, 2, 4]), 4)); E('problems', 'items[1].parts[3].question', round(f2, 4))
lv.claim(min((abs(f - 1.5), t) for f, t in ((f025, 0.25), (f1, 1), (f2, 2)))[1] == 2, 'tau 2 has the smallest error', covers=[round(abs(f2 - 1.5), 4), round(abs(f1 - 1.5), 4), round(abs(f025 - 1.5), 4)])
lv.claim(round(0.7214 + 0.5308 + 0.0528, 4) == round(f1, 4) and round(float(sm([0, -4, -16])[0]), 4) == 0.982, 'shown products and 0.98', covers=[0.7214, 0.5308, 0.0528, 0.2654, 0.0132, 0.98, 0.02])
two('25 products', float(np.var((np.random.default_rng(9).standard_normal((40000, 25)) * np.random.default_rng(10).standard_normal((40000, 25))).sum(1))), 25.0, 0.03)
E('problems', 'items[2].parts[1].widget.answer', math.sqrt(25))
w12 = sm([2.0] + [0.0] * 11)
two('scaled allocation', float(w12[0]), e ** 2 / (e ** 2 + 11)); E('problems', 'items[2].parts[2].widget.answer', round(float(w12[0]), 4)); E('problems', 'items[2].parts[2].widget.wrong[0].value', round(e ** 2 / (e ** 2 + 1), 4)); E('problems', 'items[2].parts[2].widget.wrong[1].value', round(2 / 13, 4))
w12b = sm([10.0] + [0.0] * 11)
two('unscaled allocation', float(w12b[0]), e ** 10 / (e ** 10 + 11)); E('problems', 'items[2].parts[3].widget.answer', round(float(w12b[0]), 4))
lv.claim(round(e ** 10) == 22026 and 2 / 5 - 0.01 < float(w12[0]) < 2 / 5 + 0.01, 'e^10 = 22026; about two fifths', covers=[22026, 2 / 5])
sv = np.array([0.7, 0.2, 0.1])
J = np.diag(sv) - np.outer(sv, sv)
gz = J.T @ np.array([1.0, 0, 0])
lv.claim(np.allclose(gz, sv * (np.array([1.0, 0, 0]) - sv[0])) and np.allclose(gz, [0.21, -0.14, -0.07]) and abs(gz.sum()) < 1e-15, 'Jacobian rule: matrix against the s * (g - g.s) form', covers=[0.21, -0.14, -0.07, 0.3])
two('homework sqrt 128', math.sqrt(128), 128 ** 0.5); E('homework', 'items[0].widget.answer', round(math.sqrt(128), 2))
wt = sm([-2, -6]); two('homework weight', float(wt[0]), 1 / (1 + math.exp(-4))); E('homework', 'items[1].widget.answer', round(float(wt[0]), 4))
E('homework', 'items[1].widget.wrong[0].value', round(float(sm([-0.5, -1.5])[0]), 4)); E('homework', 'items[1].widget.wrong[1].value', round(float(sm([-0.125, -0.375])[0]), 4))

# ---------------- code widgets ----------------


def judge(a, ex, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def close(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, dict) and isinstance(yv, dict):
            return set(x) == set(yv) and all(close(x[kk], yv[kk]) for kk in x)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(close(p_, q_) for p_, q_ in zip(x, yv))
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x), float(yv), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == yv

    def same(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, dict) and isinstance(yv, dict):
            return set(x) == set(yv) and all(same(x[kk], yv[kk]) for kk in x)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(same(p_, q_) for p_, q_ in zip(x, yv))
        return bool(x == yv)
    return close(a, ex) if cmp == 'isclose' else same(a, ex)


def purge():
    for m in [m for m in sys.modules if m in ('autograd', 'seq_ops_l2')]:
        sys.modules.pop(m)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    try:
        for kk, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), os.path.join(dd, kk))
        sys.path.insert(0, dd)
        purge()
        ns = {'__name__': '__zq__', '__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec(ZQ_LIB, ns)
                exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns)
                    got = eval(c['call'], ns)
                t = c.get('tol')
                ok = judge(got, eval(c['expect'], ns), c.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
            except Exception:
                ok = False
            if not ok:
                return i + 1
        return 0
    finally:
        os.chdir(cwd)
        sys.path.remove(dd)
        shutil.rmtree(dd, ignore_errors=True)
        purge()
        sys.path.insert(0, DATA)


nw = nm = 0
for fid, doc in lv.files.items():
    for u in doc.get('screens', []) + doc.get('items', []):
        w = u.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        nw += 1
        lab = f'{fid} {u.get("title") or u.get("id")}'
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        for mu in w.get('mutants', []):
            nm += 1
            got = first_fail(w, mu['source'])
            lv.claim(got == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')
import autograd as _ag  # noqa: E402
import seq_ops_l2 as S2  # noqa: E402,F811

# the homework's hand-written attention backward against autograd.py and seq_ops_l2.py
hw = F('homework')['items'][7]['widget']
ns = {}
exec(hw['prelude'].replace('def fd_err', 'def _unused'), ns)
ns2 = {}
exec(hw['solution'], ns2)
for args in (ns['small'], ns['mid'], ns['planted'](2, 1, 3, 2, 2), ns['planted'](2, 4, 4, 1, 3, scale=30.0)):
    Qt, Kt, Vt = (_ag.Tensor(a.copy()) for a in args[:3])
    O = S2.softmax(Qt @ S2.swap_last(Kt) * (1 / math.sqrt(args[0].shape[-1])), axis=-1) @ Vt
    (O * args[3]).sum().backward()
    gh = ns2['attention_backward'](*args)
    lv.claim(all(np.allclose(a.grad, b, rtol=1e-9, atol=1e-12) for a, b in zip((Qt, Kt, Vt), gh)), f'attention_backward equals the autograd on a planted case of {args[1].shape[0]} keys')

lv.check_wrongs()
for t_, why in [('20,000', 'draws in the simulation, a setting'), ('1,000', 'scores near 1,000 in a test, a given'), ('1.0082', 'stat-learning l4\'s figure, checked above'), ('0.01', 'the sweep\'s lowest tau, a setting'),
                ('0.5', 'given temperatures and distances'), ('0.25', 'a given temperature'), ('1.2', 'given returns'), ('0.6', 'given weights and values'), ('0.3', 'given values'), ('0.9', 'a given value'),
                ('0.8', 'a given value'), ('0.4', 'given values'), ('0.2', 'given values'), ('0.1', 'given values'), ('1.5', 'given coordinates and a realised return'), ('1.1', 'a given value'),
                ('7.5', 'a given value'), ('0.7', 'given weights'), ('0.001', 'a given nudge'), ('0.11', 'a given coordinate'), ('16', 'keys in the saturation test, a setting'),
                ('300', 'days in make_knn, a setting'), ('200', 'training days, a setting'), ('100', 'held-out days and features, settings'), ('800', 'a test score, a given'), ('30', 'a test scale, a given'),
                ('10^-6', 'test tolerances'), ('10^-9', 'test tolerances'), ('0.0001', 'a tolerance'), ('5', 'tau at the warm end, a setting'), ('999', 'a given score'), ('50', 'a given shift of every score'), ('900', 'a given test score'), ('60', 'past days in the transfer, given'), ('36', 'a given width'), ('512', 'a given width'), ('250', 'the word count asked of the long answer')]:
    LIT(t_, why=why)
lv.report()
