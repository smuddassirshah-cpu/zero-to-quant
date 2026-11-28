"""Recompute every number stated in ml-int level 1 (Theory questions aloud) and check each at its JSON path.

Run through the CI runner (from app/): node tools/run-number-scripts.mjs --python <venv>/bin/python --only ml-int-L1
Direct: ZQ_NUMBERS_STRICT=1 OPENBLAS_NUM_THREADS=1 <venv>/bin/python docs/reports/ml-int-L1-numbers.py

Each figure has two routes. Backprop: the hand formulas (route A) against central differences (route B). Adam: the closed
form (A) against the update coded with its moving averages (B). Double descent: the pseudo-inverse (A) against
np.linalg.lstsq, which also returns the minimum-norm solution (B); ridge by the normal equations (A) against the SVD form (B).
Quickfire: closed forms (A) against a coded softmax, Fractions or a second simulation code path (B). Every code widget's
hidden tests are run against its solution, its starter and each recorded mutant, through ZQ_LIB as the page runs them.
"""
import math
import os
import shutil
import sys
import tempfile
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

lv = Level('ml-int', 1, coverage='strict')
E = lv.expect
L1, L2, L3, L4 = 'l1-backprop', 'l2-why-adam', 'l3-double-descent', 'l4-deep-learning'


def agree(label, a, b, rel=1e-9, covers=()):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = a.shape == b.shape and bool(np.all(np.abs(a - b) <= rel * np.maximum(1e-12, np.maximum(np.abs(a), np.abs(b))) + 1e-12))
    lv.claim(ok, f'{label}: routes agree', covers=[float(x) for x in np.ravel(a)] + list(covers))
    return a


def ans(ref, path, value):
    E(ref, path + '.widget.answer', value)


# ------------------------------------------------------------------ l1: backprop by hand
def fwd(x, W1, w2, y):
    h = W1 @ x
    a = np.maximum(h, 0)
    yh = w2 @ a
    return 0.5 * (yh - y) ** 2, h, a, yh


def grads_A(x, W1, w2, y):
    L, h, a, yh = fwd(x, W1, w2, y)
    d = yh - y
    return L, np.outer(d * w2 * (h > 0), x), d * a, d * w2, d


def grads_B(x, W1, w2, y, e=1e-6):
    g1, g2 = np.zeros_like(W1), np.zeros_like(w2)
    for i in np.ndindex(W1.shape):
        P, M = W1.copy(), W1.copy(); P[i] += e; M[i] -= e
        g1[i] = (fwd(x, P, w2, y)[0] - fwd(x, M, w2, y)[0]) / (2 * e)
    for i in range(len(w2)):
        P, M = w2.copy(), w2.copy(); P[i] += e; M[i] -= e
        g2[i] = (fwd(x, W1, P, y)[0] - fwd(x, W1, M, y)[0]) / (2 * e)
    return g1, g2


x, W1, w2 = np.array([1., 2.]), np.array([[1., -1.], [0.5, 1.]]), np.array([2., -1.])
L, h, a, yh = fwd(x, W1, w2, 1.0)
LA, dW1, dw2, da, dy = grads_A(x, W1, w2, 1.0)
nW1, nw2 = grads_B(x, W1, w2, 1.0)
agree('l1 forward h, a, yhat, L (matrix product against a loop)', [*h, *a, yh, L],
      [x[0] * W1[0, 0] + x[1] * W1[0, 1], x[0] * W1[1, 0] + x[1] * W1[1, 1], max(0, -1), max(0, 2.5), 2 * 0 - 1 * 2.5, 0.5 * 3.5 ** 2])
agree('l1 dW1 by hand against central differences', dW1, nW1, 1e-6)
agree('l1 dw2 by hand against central differences', dw2, nw2, 1e-6)
lv.claim(dy == -3.5 and list(da) == [-7, 3.5], 'dL/dyhat = -3.5 and dL/da = (-7, 3.5)', covers=[-3.5, -7, 3.5, 2.5, 6.125])
slip = np.outer(da, x)
lv.claim(slip.tolist() == [[-7, -14], [3.5, 7]], 'no-gate slip: da x^T = [[-7, -14], [3.5, 7]]', covers=[-14, 7, 3.5])
lv.claim(np.outer(x, da * (h > 0)).tolist() == [[0, 3.5], [0, 7]], 'transposed slip = [[0, 3.5], [0, 7]]')
lv.claim((dy * h).tolist() == [3.5, -8.75], 'used-h slip: -3.5 x h = (3.5, -8.75)', covers=[-8.75])
lv.claim(0.5 * 3.5 ** 2 == 6.125 and 3.5 ** 2 == 12.25 and 2 * (-1) - 2.5 == -4.5, 'no-half 12.25 and no-relu -4.5', covers=[12.25, -4.5])
sg = 1 / (1 + math.exp(2.5))
sg_b = math.exp(-2.5) / (1 + math.exp(-2.5))
agree('sigma(-2.5) two ways', sg, sg_b, covers=[round(sg, 4)])
dlog = sg - 1
# route B for the log-loss gradient: central difference of the log loss in yhat
ll = lambda z: -math.log(1 / (1 + math.exp(-z)))
agree('log-loss dL/dyhat, sigma - y against a central difference', dlog, (ll(-2.5 + 1e-6) - ll(-2.5 - 1e-6)) / 2e-6, 1e-6,
      covers=[round(dlog, 4), round(-dlog, 4), round(-2 * dlog, 4)])
ans(L1, 'screens[7]', round(dlog, 4))
lv.claim(abs(1 - math.tanh(-1) ** 2 - 0.42) < 0.005, 'tanh gate at h = -1 is 0.42 to 2 places', covers=[0.42])
ans(L1, 'screens[2]', -3.5)
for k, v in enumerate([-1, 2.5, 0, 2.5, -2.5, 6.125]):
    E(L1, f'screens[0].widget.rows[{k}][1].answer', v)
# q2: x = (2, 1)
L2_, dW1q, _, _, dq = grads_A(np.array([2., 1.]), W1, w2, 1.0)
nq, _ = grads_B(np.array([2., 1.]), W1, w2, 1.0)
agree('l1 quiz 2: top-left entry by hand and by differences', dW1q[0, 0], nq[0, 0], 1e-6, covers=[-2, -4])
ans(L1, 'quiz[1]', float(dW1q[0, 0]))
lv.claim(dq == -1 and (W1 @ np.array([2., 1.])).tolist() == [1, 2], 'quiz 2: h = (1, 2), yhat = 0, output gradient -1')

# ------------------------------------------------------------------ l2: Adam
def adam_loop(gs, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8, corrected=True):
    m = v = 0.0
    steps = []
    for t, g in enumerate(gs, 1):
        m = b1 * m + (1 - b1) * g
        v = b2 * v + (1 - b2) * g * g
        mh, vh = (m / (1 - b1 ** t), v / (1 - b2 ** t)) if corrected else (m, v)
        steps.append(lr * mh / (math.sqrt(vh) + eps))
    return steps, m, v


for g in (1e-4, 1.0, 100.0):
    agree(f'first corrected step for g = {g}: closed form lr g/(|g| + eps) against the loop', adam_loop([g])[0][0], 1e-3 * g / (abs(g) + 1e-8))
    lv.claim(round(adam_loop([g])[0][0], 6) == 0.001, f'step for g = {g} is 0.001 to 6 places', covers=[0.001, 0.0001, 100])
ratio = 0.1 / math.sqrt(0.001)
agree('uncorrected/corrected first step: closed form against the loop', ratio, adam_loop([1.0], corrected=False)[0][0] / adam_loop([1.0])[0][0], 1e-6, covers=[round(ratio, 4)])
ans(L2, 'screens[3]', round(ratio, 4))
ans(L2, 'screens[2]', 0.001)
agree('m-only slip: 0.001 x 100/sqrt(10)', 0.001 * 100 / math.sqrt(10), 0.001 / math.sqrt(0.001), covers=[0.0316])
st, m2, v2 = adam_loop([1.0, -1.0])
mh2, vh2 = m2 / (1 - 0.81), v2 / (1 - 0.999 ** 2)
agree('noisy: |m2_hat|/sqrt(v2_hat) against 1/19 as a Fraction', abs(mh2) / math.sqrt(vh2), float(Fr(1, 19)), 1e-9, covers=[round(abs(mh2), 4)])
agree('noisy: m2 and v2 against the hand sums', [m2, v2], [0.9 * 0.1 - 0.1, 0.999 * 0.001 + 0.001], covers=[-0.01, 0.001999, 0.19])
ans(L2, 'screens[4]', round(abs(mh2) / math.sqrt(vh2), 4))
agree('rare token: first step for g = 1e-8 against the loop', adam_loop([1e-8])[0][0], 0.0005)
ans(L2, 'screens[6]', 0.0005)
lv.claim(round(1 / (1 - 0.999)) == 1000 and round(1 / (1 - 0.9)) == 10, 'correction factors at step 1: 1000 and 10', covers=[1000, 10])
f40 = 1 / (1 - 0.999 ** 40)
lv.stated(L2, 'screens[1].explain.text', 'still about 25', round(f40) == 25, covers=[25])
print('factor for v at step 40:', f40)
lv.claim(1 / (1 - 0.9 ** 40) < 1.02, 'factor for m at step 40 is almost 1 (under 1.02)')
agree('quiz 2: factor 1/(1 - 0.999^2) against 1/0.001999', 1 / (1 - 0.999 ** 2), 1 / 0.001999, covers=[500.25, 5.26])
ans(L2, 'quiz[1]', round(1 / (1 - 0.999 ** 2), 2))
agree('quiz 1: w after the step, 0.5 - (-0.01)', 0.5 - adam_loop([-3.0], lr=0.01)[0][0], 0.51, 1e-6, covers=[0.49, 0.53, 0.03])
lv.claim(round(0.001 * 100, 4) == 0.1 and round(0.1 / 0.001) == 100, 'slips: lr x g = 0.1 and no root 100', covers=[0.1, 100])

# ------------------------------------------------------------------ l3: double descent
def gen(seed, noise=0.1, n=40, ntest=2000, d=10, P=2000):
    rng = np.random.default_rng(seed); wt = rng.normal(size=d) / math.sqrt(d)
    X = rng.normal(size=(n, d)); Xt = rng.normal(size=(ntest, d))
    y = np.tanh(X @ wt) + noise * rng.normal(size=n); yt = np.tanh(Xt @ wt)
    return X, y, Xt, yt, rng.normal(size=(d, P)) / math.sqrt(d)


PS = [5, 10, 20, 30, 36, 40, 44, 60, 100, 400, 2000]
GRID = [1e-4, 1e-3, 1e-2, 1e-1, 1, 10]
cache = {}


def feats(seed, noise, p):
    key = (seed, noise)
    if key not in cache:
        cache[key] = gen(seed, noise)
    X, y, Xt, yt, Wf = cache[key]
    return np.maximum(X @ Wf[:, :p], 0), y, np.maximum(Xt @ Wf[:, :p], 0), yt


def mn(seed, p, noise=0.1, route='A'):
    F, y, Ft, yt = feats(seed, noise, p)
    b = np.linalg.pinv(F) @ y if route == 'A' else np.linalg.lstsq(F, y, rcond=None)[0]
    return float(np.mean((Ft @ b - yt) ** 2)), float(np.linalg.norm(b))


def ridge(seed, p, lam, route='A'):
    F, y, Ft, yt = feats(seed, 0.1, p)
    if route == 'A':
        b = np.linalg.solve(F.T @ F + lam * np.eye(p), F.T @ y)
    else:
        U, s, Vt = np.linalg.svd(F, full_matrices=False)
        b = Vt.T @ ((s / (s ** 2 + lam)) * (U.T @ y))
    return float(np.mean((Ft @ b - yt) ** 2))


med = lambda f: float(np.median([f(s) for s in range(20)]))
r3 = lambda v: float(f'{v:.3g}')
EA, EB, NA, NB, E2A, E2B = {}, {}, {}, {}, {}, {}
for p in PS:
    EA[p], EB[p] = med(lambda s: mn(s, p)[0]), med(lambda s: mn(s, p, route='B')[0])
    NA[p], NB[p] = med(lambda s: mn(s, p)[1]), med(lambda s: mn(s, p, route='B')[1])
    E2A[p], E2B[p] = med(lambda s: mn(s, p, 0.2)[0]), med(lambda s: mn(s, p, 0.2, 'B')[0])
    agree(f'median test error at p = {p}, pinv against lstsq', EA[p], EB[p], 1e-6 if p != 40 else 1e-4, covers=[r3(EA[p])])
    agree(f'median norm at p = {p}, pinv against lstsq', NA[p], NB[p], 1e-6 if p != 40 else 1e-4, covers=[r3(NA[p])])
    agree(f'noise 0.2: median test error at p = {p}, pinv against lstsq', E2A[p], E2B[p], 1e-6 if p != 40 else 1e-4, covers=[r3(E2A[p])])
print('medians', {p: r3(v) for p, v in EA.items()})
print('noise 0.2', {p: r3(v) for p, v in E2A.items()})
RTA = {p: med(lambda s: min(ridge(s, p, l) for l in GRID)) for p in PS[:-1]}
RTB = {p: med(lambda s: min(ridge(s, p, l, 'B') for l in GRID)) for p in PS[:-1]}
R1A = {p: med(lambda s: ridge(s, p, 0.01)) for p in PS[:-1]}
R1B = {p: med(lambda s: ridge(s, p, 0.01, 'B')) for p in PS[:-1]}
for p in PS[:-1]:
    agree(f'tuned ridge at p = {p}: normal equations against SVD', RTA[p], RTB[p], 1e-6, covers=[r3(RTA[p])])
    agree(f'ridge 0.01 at p = {p}: normal equations against SVD', R1A[p], R1B[p], 1e-6, covers=[r3(R1A[p])])
lv.claim(max(EA, key=EA.get) == 40 and max(R1A, key=R1A.get) == 40, 'the minimum-norm and the lambda = 0.01 curves both peak at p = 40')
lv.claim(RTA[40] < EA[10] and all(RTA[p] < EA[p] for p in PS[:-1]), 'tuned ridge lies below the minimum-norm curve everywhere; at 40 it is below the first minimum')
lv.claim(EA[400] < EA[10] and EA[2000] < EA[10], 'the second descent goes below the first minimum')
r001 = med(lambda s: ridge(s, 40, 1e-3))
lv.claim(round(r001, 2) == 1.64, f'lambda = 0.001 still leaves a peak of about 1.64 at 40 (got {r001:.4f})', covers=[1.64, 0.001])
rp, sh, nr = EA[40] / EA[10], EA[400] / EA[10], NA[40] / NA[10]
agree('peak over first minimum, two routes', rp, EB[40] / EB[10], 1e-4, covers=[round(rp), 31])
agree('error at 400 over first minimum, two routes', sh, EB[400] / EB[10], 1e-6, covers=[round(sh, 2), round(1 / sh, 2)])
agree('norm at 40 over norm at 10, two routes', nr, NB[40] / NB[10], 1e-4, covers=[round(nr, 1), round(1 / nr, 2)])
agree('noise floor ratio at 2000, two routes', E2A[2000] / EA[2000], E2B[2000] / EB[2000], 1e-6, covers=[round(E2A[2000] / EA[2000], 1)])
E0 = med(lambda s: mn(s, 2000, 0.0)[0])
noise_part = (EA[2000] - E0, E2A[2000] - E0)
lv.claim(round(E0, 4) == 0.0461 and round(noise_part[0], 4) == 0.0185 and round(noise_part[1], 4) == 0.0763 and abs(noise_part[1] / noise_part[0] - 4) < 0.2,
         'noise 0 floor at 2000 is 0.0461; the noise part goes from 0.0185 to 0.0763, four times', covers=[0.0461, 0.0185, 0.0763, 0.046])
lv.claim(round(med(lambda s: mn(s, 40, 0.0)[0]), 1) == 2.5, 'with no label noise the peak at p = 40 is about 2.5', covers=[2.5])
lv.claim(round(NA[40], 2) == 10.14 and round(NA[10], 3) == 1.166 and round(NA[40] / NA[10], 1) == 8.7 and round(10.14 / 1.166, 1) == 8.7,
         'norms to four figures: 1.166 and 10.14, ratio 8.7 from the figures as shown', covers=[10.14, 1.166])
ans(L3, 'screens[1]', round(nr, 1))
ans(L3, 'screens[2]', round(rp))
ans(L3, 'screens[3]', round(sh, 2))
ans(L3, 'quiz[2]', round(E2A[2000] / EA[2000], 1))
lv.claim(round(sh * 4) == 1, 'the error at 400 is about a quarter of the first minimum', covers=[0.25])
lv.claim(round(math.log10(2000), 3) == 3.301, 'axis ticks are log10 p')

# ------------------------------------------------------------------ l4: quickfire
ln65, ln27 = math.log(65), math.log(27)


def ce_uniform(V):
    z = np.zeros((3, V))
    p = np.exp(z) / np.exp(z).sum(1, keepdims=True)
    return float(-np.log(p[np.arange(3), [0, 1, 2]]).mean())


agree('ln 65 against the coded softmax cross-entropy of uniform logits', ln65, ce_uniform(65), covers=[round(ln65, 4), round(1 / 65, 4), round(math.log10(65), 4)])
agree('ln 27 against the coded softmax cross-entropy', ln27, ce_uniform(27), covers=[round(ln27, 4), round(1 / 27, 4), round(math.log10(27), 4)])
agree('He sd for fan-in 512 against 1/16', math.sqrt(2 / 512), float(Fr(1, 16)), covers=[0.0625, round(math.sqrt(1 / 512), 4), round(2 / 512, 4)])
agree('He sd for fan-in 128 against 1/8', math.sqrt(2 / 128), 0.125, covers=[round(math.sqrt(1 / 128), 3), round(2 / 128, 3)])
agree('inverted dropout scale 1/0.8 against the Fraction 5/4', 1 / 0.8, float(Fr(5, 4)), covers=[1.25, 0.8, 5, 0.2])
rng = np.random.default_rng(0)
q = rng.standard_normal((20000, 64)); k = rng.standard_normal((20000, 64))
sdA, sdB = float((q * k).sum(1).std()), float(np.einsum('ij,ij->i', q, k).std())
agree('dot-product sd from 20,000 pairs: elementwise sum against einsum', sdA, sdB, 1e-9, covers=[round(sdA, 3), round(sdA / 8, 3), 8, 64, 20000])
lv.claim(abs(sdA - 8) < 0.1, 'the simulated sd is within 0.1 of the exact 8')
agree('9.7 over ln 65', 9.7 / ln65, 9.7 / ce_uniform(65), covers=[round(9.7 / ln65, 2), 9.7])
ans(L4, 'screens[0]', round(ln65, 4))
ans(L4, 'screens[2]', 0.0625)
ans(L4, 'screens[3]', 1.25)
ans(L4, 'quiz[0]', round(ln27, 4))
ans(L4, 'quiz[2]', 0.125)
lv.claim(math.sqrt(16) == 4 and 1 / 0.5 == 2, 'quiz: sd 4 for d = 16, scale 2 for p = 0.5', covers=[4, 16, 2, 0.5])

# ------------------------------------------------------------------ review 1
xr, W1r, w2r = np.array([2., -1.]), np.array([[1., 1.], [-1., 2.]]), np.array([3., 1.])
_, dWr, _, _, dyr = grads_A(xr, W1r, w2r, 1.0)
nWr, _ = grads_B(xr, W1r, w2r, 1.0)
agree('review r1: dW1 by hand against differences', dWr, nWr, 1e-6, covers=[6, 12, 24, 3, -4])
E('review', 'items[0].widget.answer', float(dWr[0, 0]))
lv.claim(dyr == 2 and (W1r @ xr).tolist() == [1, -4], 'r1: h = (1, -4), output gradient 2')
agree('r2: tanh gate at a = 0.6', 1 - 0.6 ** 2, 1 - math.tanh(math.atanh(0.6)) ** 2, covers=[0.64, 0.4, 0.24, 0.36])
agree('r3: uncorrected ratio with betas 0.8 and 0.99', 0.2 / math.sqrt(0.01), adam_loop([1.0], b1=0.8, b2=0.99, corrected=False)[0][0] / adam_loop([1.0], b1=0.8, b2=0.99)[0][0], 1e-6, covers=[2, 20, 0.2, 0.1, 0.01])
lnv = math.log(50257)
agree('r7: ln 50,257 against the coded softmax', lnv, ce_uniform(50257), covers=[round(lnv, 3), round(math.log10(50257), 3), 50257])
agree('r8: He sd for 2,048 against 1/32', math.sqrt(2 / 2048), 1 / 32, covers=[round(1 / 32, 5), round(math.sqrt(1 / 2048), 5), round(2 / 2048, 5), 2048])
lv.claim(250 * 2 == 500 and 250 / 2 == 125, 'r5: the threshold is p = n = 250; slips 500 and 125', covers=[500, 125, 250])
E('review', 'items[4].widget.answer', 250)

# ------------------------------------------------------------------ homework 1
hs, _, _ = adam_loop([2.0, 2.0], lr=0.003)
agree('h4: step 2 with a constant gradient, loop against the closed form lr', hs[1], 0.003, 1e-6, covers=[0.003, 0.006, 0.38, 4])
unc = adam_loop([2.0, 2.0], lr=0.003, corrected=False)[0][1]
agree('h4: uncorrected step 2, loop against 0.003 x 0.19/sqrt(0.001999)', unc, 0.003 * 0.19 / math.sqrt(0.001999), 1e-6, covers=[round(unc, 4)])
lg = 1 / (1 + math.exp(2.5))
agree('h5: log loss with y = 0, row 2 col 2 entry, hand against a central difference', -2 * lg,
      (lambda e: ((lambda W: -math.log(1 - 1 / (1 + math.exp(-(w2 @ np.maximum(W @ x, 0))))))(W1 + np.array([[0, 0], [0, e]])) -
                  (lambda W: -math.log(1 - 1 / (1 + math.exp(-(w2 @ np.maximum(W @ x, 0))))))(W1 - np.array([[0, 0], [0, e]]))) / (2 * e))(1e-6), 1e-6,
      covers=[round(-2 * lg, 4), round(2 * lg, 4), round(-lg, 4), round(lg, 4), 5.0])
E('homework', 'items[4].widget.answer', round(-2 * lg, 4))
lv.claim(round(1 - 0.1 - 0.001, 3) == 0.899, 'h2: first AdamW step lands at 0.899; the decay is 0.1 x 0.01 x 1 = 0.001', covers=[0.899, 0.001, -0.001, 0.01])
for v in (1.17, 10.1):
    lv.claim(any(abs(r - v) < 0.006 for r in (round(NA[10], 2), round(NA[40], 1))), f'model answer norm {v}', covers=[v])
for v in (7.63, 0.249, 0.0644):
    lv.claim(v in (r3(EA[40]), r3(EA[10]), r3(EA[400])), f'model answer error {v}', covers=[v])

# ------------------------------------------------------------------ code widgets: solution, starter, mutants, through ZQ_LIB
def judge(a, e, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def close(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) or isinstance(y, dict):
            return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(close(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
        if isinstance(x, (bool, str)) or isinstance(y, (bool, str)) or x is None or y is None:
            return x == y
        try:
            rt, at = tol if tol else (1e-9, 1e-12)
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y
    return close(a, e) if cmp == 'isclose' else flat(a) == flat(e)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    ns = {'__learner_source__': src}
    exec(ZQ_LIB, ns)
    try:
        try:
            with np.errstate(all='ignore'):
                exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
        except Exception:
            return -1, ns
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns)
                    got = eval(c['call'], ns)
                tl = c.get('tol')
                ok = judge(got, eval(c['expect'], ns), c.get('compare', 'isclose'), (tl.get('rel') or 0, tl.get('abs') or 0) if tl else None)
            except Exception:
                ok = False
            if not ok:
                return i + 1, ns
        return 0, ns
    finally:
        os.chdir(cwd)
        shutil.rmtree(dd, ignore_errors=True)


widgets = {}
nw = nm = 0
for fid, doc in lv.files.items():
    for u in doc.get('screens', []) + doc.get('items', []):
        w = u.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        nw += 1
        lab = f'{fid} {u.get("title") or u.get("id")}'
        widgets[fid] = w
        got, _ = first_fail(w, w['solution'])
        lv.claim(got == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter'])[0] != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        lv.claim(f'Submit runs {len(w["tests"])} hidden tests' in w.get('how', ''), f'{lab}: the how line counts {len(w["tests"])} tests')
        for mu in w.get('mutants', []):
            nm += 1
            g = first_fail(w, mu['source'])[0]
            lv.claim(g == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {g})')
print(f'code widgets {nw}, mutants {nm}')

# the hidden tests' stated values, recomputed by the other route
W = widgets[[k for k in widgets if k.startswith(L1)][0]]
agree('two_layer_grads test 1 to 3 expects = route B', [eval(W['tests'][0]['expect']), *eval(W['tests'][2]['expect'])[0], *eval(W['tests'][2]['expect'])[1], *eval(W['tests'][1]['expect'])],
      [L, *nW1[0], *nW1[1], *nw2], 1e-6)
W = widgets[[k for k in widgets if k.startswith(L2)][0]]
exp2 = [eval(t['expect']) for t in W['tests']]
agree('adam_first_step expects = the moving-average loop', [exp2[0], exp2[1], exp2[2], *exp2[4], exp2[5], exp2[6]],
      [adam_loop([1.0])[0][0], adam_loop([1e-4])[0][0], adam_loop([1.0], corrected=False)[0][0], -adam_loop([100.0])[0][0], adam_loop([1e-4])[0][0], adam_loop([1.0])[0][0],
       adam_loop([2.0], lr=0.01, b1=0.8, b2=0.99, corrected=False)[0][0], ratio], 1e-6)
W = widgets[[k for k in widgets if k.startswith(L3)][0]]
agree('min_norm_test_error test 1 and 2 expects = lstsq route', [eval(W['tests'][0]['expect']), eval(W['tests'][1]['expect'])], [mn(0, 10, route='B')[0], mn(3, 400, route='B')[0]], 1e-6)
lv.claim([eval(t['expect']) for t in W['tests'][2:]] == [r3(EA[10]), r3(EA[40]), r3(EA[400])], 'tests 3 to 5 expect the stated medians')
W = widgets[[k for k in widgets if k.startswith(L4)][0]]
hand = (math.log(math.exp(2) + 2) - 2 + math.log(math.e + 2) - 0) / 2
agree('sanity_checks test 2: hand log-sum-exp', eval(W['tests'][1]['expect']), hand)
agree('sanity_checks test 1: ln 65 twice', eval(W['tests'][0]['expect'])[:2], [ln65, ce_uniform(65)])
lv.claim(eval(W['tests'][0]['expect'])[2] is False and eval(W['tests'][2]['expect']) is True, 'uniform not flagged, leak flagged')
agree('sanity_checks test 4: a logit of 800 gives 800', eval(W['tests'][3]['expect']), 800 + math.log1p(2 * math.exp(-800)), covers=[800])
HW = widgets['homework-1']
hw2 = [w for w in [u.get('widget') for u in lv.files['homework-1']['items']] if w and w.get('kind') == 'code'][1]


def adamw_B(p, g, st, lr, wd, b1=0.9, b2=0.999, eps=1e-8):
    t = st['t'] + 1
    m = b1 * st['m'] + (1 - b1) * g
    v = b2 * st['v'] + (1 - b2) * g * g
    p = p * (1 - lr * wd)                      # torch's order: decay the old weight first, then the Adam step
    return p - lr * (m / (1 - b1 ** t)) / (math.sqrt(v / (1 - b2 ** t)) + eps), {'m': m, 'v': v, 't': t}


w_, s_ = 1.0, {'m': 0.0, 'v': 0.0, 't': 0}
for _ in range(5):
    w_, s_ = adamw_B(w_, 2 * w_, s_, 0.1, 0.1)
agree('adamw five-step run: test 4 expect against a decay-first implementation', eval(hw2['tests'][3]['expect']), w_, 1e-12)
agree('adamw first step: test 1 expect against the decay-first form', eval(hw2['tests'][0]['expect']), adamw_B(1.0, 0.5, {'m': 0.0, 'v': 0.0, 't': 0}, 0.1, 0.01)[0], 1e-12)
_st = eval(hw2['tests'][1]['expect'])
agree('adamw state after one step against the decay-first form', [_st['m'], _st['v'], _st['t']], [adamw_B(1.0, 0.5, {'m': 0.0, 'v': 0.0, 't': 0}, 0.1, 0.01)[1][k] for k in ('m', 'v', 't')], 1e-12)


# settings and structural counts the text states
lv.claim(3.5 / 2 == 1.75 and 7 / 2 == 3.5, 'quiz 1 slip: half the old row, (1.75, 3.5)', covers=[1.75])
lv.claim(round(10 / 0.001) == 10000 and round(10 / 0.1) == 100, 'g = 100: m1 = 10, v1 = 10, corrected 100 and 10,000', covers=[10000, 10])
lv.claim(len(PS) == 11 and PS[5] == 40 and 2 * 60 == 120, 'double descent: 40 training points; quiz threshold 60 (doubled 120); features up to 400 and 2,000',
         covers=[40, 400, 60, 120, 2000])
lv.claim(2 / 512 == 1 / 256 and math.sqrt(2 / 128) == 1 / 8, 'He: 2/512 = 1/256; fan-in 128 gives 1/8', covers=[512, 256, 128])
lv.claim(round(math.exp(ln65)) == 65 and round(math.exp(ln27)) == 27, 'vocabularies of 65 and 27 classes', covers=[65, 27])
lv.claim(0.001 * 1e-8 / (2e-8) == 0.0005, 'rare token: 0.001 x 1e-8 / (2 x 1e-8)', covers=['0.001 \\times 10^-8', '2 \\times 10^-8'])
lv.literal('0.999', why='beta2, a setting of the optimiser stated as the question gives it')
lv.literal('0.99', why='beta2 in a review question, a setting')
lv.literal('10^-8', why='epsilon and a tolerance, settings')
lv.literal('10^-6', why='the tolerance of central-difference tests, a setting')
lv.literal('20,000', why='the size of the simulation, a setting stated with its result')
lv.check_wrongs()
lv.report()
