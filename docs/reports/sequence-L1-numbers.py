"""Recompute every number stated in sequence level 1 (Recurrent networks) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only sequence-L1
(NumPy only; about a minute; strict coverage; exits 0 when every check passes).

Route A is the closed form or the lesson's own recursion; route B is an independent computation: a loop against a
power, an eigen-decomposition against repeated multiplication, central differences against the autograd, a hand-written
backward pass against autograd.py, NumPy's least squares against the gradient-descent loop. The copy task is retrained
here with the frozen autograd (three seeds, both units), its gradients checked by central differences and its accuracies
recomputed by a plain NumPy forward pass. Every code widget is run in CPython with the page's judge: the solution passes,
the starter fails, and each mutant first fails the hidden test it names (ENGINE-BACKLOG 1263).
"""
import hashlib
import json
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

lv = Level('sequence', 1, coverage='strict')
E = lv.expect
LIT = lv.literal


def two(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol * max(1.0, abs(a), abs(b)), f'{label}: routes agree ({a!r} vs {b!r})')
    return a


def F(fid):
    return lv._file(fid)[1]


# ---------------- frozen module ----------------
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'autograd.py'), 'rb').read()).hexdigest().startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
shipped = []


def walk(node):
    if isinstance(node, dict):
        for key in ('data', 'files'):
            if isinstance(node.get(key), dict):
                shipped.extend((key, k, v) for k, v in node[key].items() if k.endswith('.py'))
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


for doc in lv.files.values():
    walk(doc)
lv.claim(all(key == 'data' and v == f'content/data/ai/{k}' for key, k, v in shipped), f'every shipped module ({len(shipped)}) goes by path, so the page gets the frozen text')


def sim(phi, n, seed):
    e = np.random.default_rng(seed).standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    for t in range(1, n):
        x[t] = phi * x[t - 1] + e[t]
    return x


# ================= l1 =================
L1 = 'l1-'
# hook: the RNN state with w = phi on the same shocks is the AR(1) (route B: closed form sum of w^(t-k) e_k)
e7 = np.random.default_rng(7).standard_normal(60)
closed = [sum(0.6 ** (t - k) * e7[k] for k in range(t + 1)) for t in range(60)]
lv.claim(np.allclose(sim(0.6, 60, 7), closed, atol=1e-12), 'hook: the AR(1) path equals the state of h_t = 0.6 h_{t-1} + e_t')
fr = F(L1)['screens'][0]['canvas']['controls'][0]['frames']
lv.claim(all(np.allclose(fr[k]['series']['rnn']['values'], np.round(sim(k / 10, 60, 7), 4)) for k in range(11)), 'hook frames: each frame is the state for w = 0, 0.1, ..., 1')
lv.claim(np.allclose(F(L1)['screens'][0]['canvas']['params']['series'][0]['values'], np.round(sim(0.6, 60, 7), 4)), 'hook: grey line is simulate_ar1(0.6, 60, 7)')
E(L1, 'screens[0].widget.answer', 0.6)
# three steps by hand (route B: closed form sum)
h = [0.0]
for x in (1.0, -2.0, 0.5):
    h.append(0.5 * h[-1] + x)
hB = [sum(0.5 ** (t - k) * xx for k, xx in enumerate((1.0, -2.0, 0.5)[:t + 1])) for t in range(3)]
lv.claim(np.allclose(h[1:], hB), 'three steps by hand: loop and closed form')
for i, v in enumerate(h[1:]):
    lv.claim(abs(F(L1)['screens'][1]['widget']['rows'][i + 1][2]['answer'] - v) < 1e-12, f'l1 table h_{i + 1} = {v}')
E(L1, 'screens[1].feedback.correct', -1.5); E(L1, 'screens[1].feedback.correct', -0.25); E(L1, 'screens[1].explain.text', -0.75)
lv.claim(F(L1)['screens'][1]['widget']['rows'][2][2]['wrong'][0]['value'] == 1.0 - 2.0 and F(L1)['screens'][1]['widget']['rows'][3][2]['wrong'][0]['value'] == -1.5 + 0.5, 'l1 table slips: h_{t-1} added in full')
# least squares on three days (route B: lstsq)
X3 = np.array([1.0, 0.5, 0.4])
wA = float(X3[1:] @ X3[:-1] / (X3[:-1] @ X3[:-1]))
wB = float(np.linalg.lstsq(X3[:-1, None], X3[1:], rcond=None)[0][0])
two('three-day least squares', wA, wB)
lv.claim(16 * 16 == 256 and 250 - 1 == 249 and 100 - 1 == 99, 'W holds 256; day 1 passes through 249 later updates of 250; 99 of 100', covers=[256, 249, 99])
E(L1, 'screens[2].widget.answer', round(wA, 2)); E(L1, 'screens[2].feedback.correct', 0.7); E(L1, 'screens[2].feedback.correct', 1.25)
two('ratio slip', (0.5 / 1 + 0.4 / 0.5) / 2, 0.65); E(L1, 'screens[2].widget.wrong[0].value', 0.65)
two('all-squares slip', round(0.7 / (1 + 0.25 + 0.16), 2), 0.5); E(L1, 'screens[2].widget.wrong[1].value', 0.5)
two('loss at w = 0', ((0.5) ** 2 + 0.4 ** 2) / 2, 0.205)
lv.claim(abs(-((0.5 - 0) + 0.5 * (0.4 - 0)) - (-0.7)) < 1e-12, 'slope at w = 0 is -0.7 (caption)', covers=[0.205, -0.7])
# fit_w on seed 5 (route B: lstsq through the origin, and the intercept fit of arma l7)
x5 = sim(0.6, 500, 5)
phi0 = float(x5[1:] @ x5[:-1] / (x5[:-1] @ x5[:-1]))
two('phi through origin', phi0, float(np.linalg.lstsq(x5[:-1, None], x5[1:], rcond=None)[0][0]))
ols = np.linalg.lstsq(np.c_[np.ones(499), x5[:-1]], x5[1:], rcond=None)[0]
lv.claim(round(ols[1], 4) == 0.6315 and round(phi0, 4) == 0.6315, f'through the origin {phi0:.4f}, with intercept {ols[1]:.4f}: both 0.6315 as arma l7 states', covers=[0.6315])
E(L1, 'screens[3].prose', round(phi0, 4)); E(L1, 'summary.ideas[1]', round(phi0, 4))
w = 0.0
for _ in range(200):
    w -= 0.1 * (-2 * np.mean(x5[:-1] * (x5[1:] - w * x5[:-1])))
lv.claim(abs(w - phi0) < 1e-6, f'200 steps of 0.1 reach the least-squares value ({w - phi0:.2e})')
lv.claim(abs(0.1 * 0.7 - 0.07) < 1e-12, 'one step from 0 with step 0.1 gives 0.07 (byKey test-1)', covers=[0.07])
# tanh and readout
yh = 2 * math.tanh(0.5 * 0.8 + 0.2)
two('readout', yh, 2 * (math.exp(1.2) - 1) / (math.exp(1.2) + 1))
E(L1, 'screens[4].widget.answer', round(yh, 4)); E(L1, 'screens[4].explain.text', round(math.tanh(0.6), 4)); E(L1, 'screens[4].feedback.correct', 0.53705)
E(L1, 'screens[4].widget.wrong[0].value', 1.2); E(L1, 'screens[4].widget.wrong[1].value', round(math.tanh(0.6), 4))
# parameter count (route B: sizes of arrays)
cnt = sum(np.zeros(s).size for s in ((16, 16), (16,), (16,), (16,), (1,)))
two('16-unit count', cnt, 16 * 16 + 16 * 3 + 1)
E(L1, 'screens[5].widget.answer', cnt); E(L1, 'screens[5].widget.wrong[0].value', cnt * 250); E(L1, 'screens[5].widget.wrong[1].value', cnt - 256)
E(L1, 'quiz[1].widget.answer', cnt); E(L1, 'quiz[1].widget.wrong[0].value', 2 * cnt); E(L1, 'summary.ideas[2]', cnt)
# EWMA transfer (route B: weights as a convex combination of volatilities squared)
var = 0.94 * 0.01 ** 2 + 0.06 * 0.02 ** 2
two('ewma variance', var, 0.000118)
vol = math.sqrt(var)
E(L1, 'screens[9].widget.answer', round(vol, 6)); E(L1, 'screens[9].explain.text', round(vol, 4))
E(L1, 'screens[9].widget.wrong[1].value', round(math.sqrt(0.06 * 0.0001 + 0.94 * 0.0004), 6))
lv.claim(round(vol * 100, 2) == 1.09, 'about 1.09% a day', covers=[1.09, 0.000094, 0.000024, 0.0004, 0.0001, 0.94, 0.06])
# quiz
two('zigzag', -0.5 * (-0.5 * 2), 0.5); E(L1, 'quiz[0].widget.answer', 0.5)
two('0.9^99 exists', 0.9 ** 99, math.exp(99 * math.log(0.9)), 1e-12)

# ================= l2 =================
L2 = 'l2-'
hs = [2.0]
for x in (1.0, 1.0, 0.0, -1.0):
    hs.append(0.5 * hs[-1] + x)
lv.claim(hs == [2.0, 2.0, 2.0, 1.0, -0.5], 'hook forward values 2, 2, 1, -0.5')
dwA = sum(0.5 ** (4 - k) * hs[k - 1] for k in range(1, 5))
eps = 1e-6


def h4(wv):
    hh = 2.0
    for x in (1.0, 1.0, 0.0, -1.0):
        hh = wv * hh + x
    return hh


two('dh4/dw: sum of terms against central differences', dwA, (h4(0.5 + eps) - h4(0.5 - eps)) / (2 * eps), 1e-7)
E(L2, 'screens[1].widget.answer', dwA); E(L2, 'screens[1].widget.wrong[0].value', 1.0); E(L2, 'screens[1].widget.wrong[1].value', 7.0)
lv.claim([0.5 ** k for k in (2, 3, 4)] == [0.25, 0.125, 0.0625], 'powers of 0.5 shown under the nodes', covers=[0.25, 0.125, 0.0625])
lv.claim(len([1 for k in range(1, 5)]) == 4, 'w acts at four arrows (four times)')
LIT('four times', why='w is used at the four arrows of a four-step chain, a count')
two('dh4/dh0', 0.5 ** 4, (lambda f: (f(2 + eps) - f(2 - eps)) / (2 * eps))(lambda h0: 0.5 ** 4 * h0 + 0), 1e-7)
E(L2, 'screens[2].widget.answer', 0.0625); E(L2, 'screens[2].widget.wrong[0].value', 2.0)
# gradient check numbers: loss of the planted series at w = 0.69, 0.71 (route B: autograd derivative)
XP = [0.5, -1.0, 0.8, 0.3, -0.4, 1.2]


def Lw(wv, u=1.1, v=0.9):
    hh, err = 0.0, []
    for t in range(len(XP) - 1):
        hh = math.tanh(wv * hh + u * XP[t])
        err.append((v * hh - XP[t + 1]) ** 2)
    return sum(err) / len(err)


lv.claim(round(Lw(0.69), 6) == 1.27433 and round(Lw(0.71), 6) == 1.266296, 'losses 1.274330 and 1.266296', covers=[1.27433, 1.266296])
cd = (1.266296 - 1.27433) / 0.02
p = {k: Tensor(v) for k, v in dict(w=0.7, u=1.1, v=0.9).items()}
hh, err = Tensor(0.0), []
for t in range(len(XP) - 1):
    hh = (p['w'] * hh + p['u'] * XP[t]).tanh()
    err.append((p['v'] * hh - XP[t + 1]) ** 2)
tot = err[0]
for e_ in err[1:]:
    tot = tot + e_
(tot / len(err)).backward()
lv.claim(abs(cd - float(p['w'].grad)) < 1e-4 and round(float(p['w'].grad), 6) == -0.401705, f'central difference {cd:.4f} against autograd {float(p["w"].grad):.6f}', covers=[-0.401705])
E(L2, 'screens[4].widget.answer', round(cd, 4)); E(L2, 'screens[4].widget.wrong[0].value', round(-cd, 4)); E(L2, 'screens[4].widget.wrong[1].value', round(cd / 2, 4))
two('510 bars a day', (16.5 - 8) * 60, 510); lv.claim(510 / 30 == 17, '17 windows', covers=[510 / 30])
two('quiz dh2/dw', 1.5 + 0.5 * 1, 2.0); E(L2, 'quiz[0].widget.answer', 2.0)

# ================= l3 =================
L3 = 'l3-'
two('0.9^50', 0.9 ** 50, math.exp(50 * math.log(0.9)), 1e-12); E(L3, 'screens[0].widget.answer', round(0.9 ** 50, 4))
two('1.1^50', 1.1 ** 50, math.exp(50 * math.log(1.1)), 1e-12); E(L3, 'screens[1].widget.answer', round(1.1 ** 50)); E(L3, 'screens[1].feedback.correct', round(1.1 ** 50, 2))
lv.claim(round(50 * math.log(1.1), 4) == 4.7655, 'hint exponent 4.7655', covers=[4.7655])
MB = np.array([[0.9, 0.2], [0.1, 0.8]])
v = np.array([1.0, 0.0])
for _ in range(400):
    v = MB.T @ v
ev = np.linalg.eig(MB.T)
two('broker settles: repeated multiplication against the eigenvector part', float(np.linalg.norm(v)), 2 / 3 * math.sqrt(2), 1e-9)
lv.claim(sorted(np.round(ev[0].real, 9)) == [0.7, 1.0], 'broker eigenvalues 1 and 0.7')
E(L3, 'screens[2].widget.answer', round(2 / 3 * math.sqrt(2), 4)); E(L3, 'screens[2].widget.wrong[1].value', round(math.sqrt(5) / 3, 4))
eb = sorted(np.linalg.eigvals([[1.0, 0.3], [0.3, 0.8]]).real)
two('B eigenvalue', eb[1], 0.9 + math.sqrt(0.1)); lv.claim(np.allclose(np.array([1.0, 0.0]), 2 / 3 * np.array([1, 1]) + 1 / 3 * np.array([1, -2])), 'g = 2/3 (1, 1) + 1/3 (1, -2)', covers=[2 / 3, 1 / 3]); E(L3, 'screens[3].explain.text', round(eb[1], 4)); E(L3, 'screens[3].explain.text', round(eb[0], 4))
lv.claim(np.allclose(sorted(abs(np.linalg.eigvals([[0.866, -0.5], [0.5, 0.866]]))), [1.0, 1.0], atol=1e-3), 'the 30-degree turn has eigenvalues of size 1', covers=[0.866, 0.9, 0.1])
two('0.72^20', 0.72 ** 20, (1.2 * 0.6) ** 20); E(L3, 'screens[4].widget.answer', round(0.72 ** 20, 4)); E(L3, 'screens[4].widget.wrong[0].value', round(1.2 ** 20, 2))
R2 = np.random.default_rng(2).standard_normal((16, 16))
rho = float(max(abs(np.linalg.eigvals(R2))))
vv = np.ones(16)
for _ in range(2000):
    vv = R2 @ vv
    vv /= np.linalg.norm(vv)
lv.claim(abs(rho - 4.0766) < 5e-5, f'spectral radius of default_rng(2) 16 by 16: {rho:.4f}', covers=[round(rho, 4)])
E(L3, 'screens[5].widget.answer', round(0.95 / rho, 3)); E(L3, 'screens[5].widget.wrong[0].value', round(rho / 0.95, 3)); E(L3, 'screens[5].widget.wrong[1].value', round(0.95 / math.sqrt(rho), 3))
N = np.array([[0.9, -0.9], [0.9, -0.9]])
lv.claim(np.allclose(N @ N, 0), 'N squared is zero')
two('1.05^50', 1.05 ** 50, math.exp(50 * math.log(1.05))); E(L3, 'screens[6].explain.text', round(1.05 ** 50, 2))
WN = np.array([[0.85, 4.0], [0.0, 0.85]])
nn = []
v = np.array([1.0, 0.0])
for k in range(41):
    nn.append(float(np.linalg.norm(v)))
    v = WN.T @ v
nnB = [math.hypot(0.85 ** k, 4 * k * 0.85 ** (k - 1) if k else 0.0) for k in range(41)]
lv.claim(np.allclose(nn, nnB), 'non-normal sizes: loop against the closed form (0.85^k, 4k 0.85^(k-1))')
E(L3, 'screens[7].widget.answer', int(np.argmax(nnB))); E(L3, 'screens[7].feedback.correct', round(max(nnB), 2))
two('0.95^60', 0.95 ** 60, math.exp(60 * math.log(0.95))); E(L3, 'screens[10].widget.answer', round(0.95 ** 60, 4)); E(L3, 'screens[10].widget.wrong[0].value', -2.0)
lv.claim(round(60 * math.log(0.95), 4) == -3.0776, 'hint exponent', covers=[-3.0776])
E(L3, 'quiz[0].widget.answer', round(0.8 ** 10, 4))

# ================= l4 =================
L4 = 'l4-'


def run(lr, clip, steps=40, T=30, w0=0.5, seed=0, n=32, route='fwd'):
    rng = np.random.default_rng(seed)
    wv, losses = w0, []
    for s in range(steps):
        Xb = rng.standard_normal((n, T))
        y = Xb.sum(1)
        with np.errstate(all='ignore'):
            if route == 'fwd':
                hh, dh = np.zeros(n), np.zeros(n)
                for t in range(T):
                    dh = hh + wv * dh
                    hh = wv * hh + Xb[:, t]
                g = float(np.mean(2 * (hh - y) * dh))
            else:   # route B: the closed form h_T = sum_k w^(T-1-k) x_k and its derivative
                pw = wv ** np.arange(T - 1, -1, -1)
                dpw = np.arange(T - 1, -1, -1) * wv ** np.maximum(np.arange(T - 1, -1, -1) - 1, 0)
                hh = Xb @ pw
                g = float(np.mean(2 * (hh - y) * (Xb @ dpw)))
            losses.append(float(np.mean((hh - y) ** 2)))
        if clip is not None and abs(g) > clip:
            g = g * clip / abs(g)
        wv = wv - lr * g
    return losses


rawA, rawB = run(0.003, None), run(0.003, None, route='B')
clpA, clpB = run(0.003, 5.0), run(0.003, 5.0, route='B')
big = next(i for i, x in enumerate(rawA) if x > 1e4)
lv.claim(next(i for i, x in enumerate(rawB) if x > 1e4) == big and not math.isfinite(rawA[big + 2]) and all(math.isfinite(x) for x in clpA), f'unclipped run passes 10,000 at step {big} on both routes and overflows within two steps; the clipped run stays finite', covers=[10000])
lv.claim(np.allclose(clpA, clpB, rtol=1e-6) and min(clpA[30:]) < 2, 'clipped run: both routes agree and the loss falls below 2')
E(L4, 'screens[0].explain.text', big + 1); E(L4, 'screens[0].prose', 0.003)
cv = F(L4)['screens'][0]['canvas']['controls'][0]['frames']
lv.claim(np.allclose(cv[1]['series']['loss']['values'], np.round(clpA, 4)) and all((a is None) or abs(a - round(b, 4)) < 1e-9 for a, b in zip(cv[0]['series']['loss']['values'], rawA)), 'hook frames hold the two recorded runs')
E(L4, 'screens[1].widget.answer', 0.2); E(L4, 'screens[1].widget.wrong[1].value', round(1 / 7, 4)); E(L4, 'screens[1].explain.text', 0.2)
two('clipped (3,4)', float(np.linalg.norm([3, 4])), 5.0); lv.claim(np.allclose(np.array([3, 4]) / 5, [0.6, 0.8]), '(0.6, 0.8)', covers=[0.6, 0.8])
gl = np.array([3.0, 0.0, 4.0]) * 2.5 / np.linalg.norm([3, 0, 4])
lv.claim(np.allclose(gl, [1.5, 0, 2]), 'list clip to 1.5, 0, 2'); E(L4, 'screens[2].widget.answer', 1.5); E(L4, 'screens[2].widget.wrong[0].value', 2.5)
a0, a1 = math.degrees(math.atan2(0.5, 3)), math.degrees(math.atan2(0.5, 1))
gB = np.array([3, 0.5]) / np.linalg.norm([3, 0.5])
lv.claim(abs(math.degrees(math.acos(gB @ (np.array([1, 0.5]) / np.linalg.norm([1, 0.5])))) - (a1 - a0)) < 1e-9, 'turn: arctangents against the angle between the vectors', covers=[round(a0, 2), round(a1, 2), 0.986, 0.164])
lv.claim(np.allclose(np.round(gB, 3), [0.986, 0.164]), 'by-norm clip of (3, 0.5) is (0.986, 0.164)')
E(L4, 'screens[3].widget.answer', round(a1 - a0, 1)); E(L4, 'screens[3].widget.wrong[1].value', round(a1, 1))
two('gate by hand', 0.9 * 0.8 + 0.1 * -0.5, 0.67); E(L4, 'screens[5].widget.answer', 0.67); E(L4, 'screens[5].widget.wrong[0].value', round(0.1 * 0.8 + 0.9 * -0.5, 4))
lv.claim(abs(0.9 * 0.8 - 0.72) < 1e-12 and abs(0.1 * -0.5 + 0.05) < 1e-12, 'gate bars 0.72 and -0.05', covers=[0.72, -0.05])
two('0.98^50', 0.98 ** 50, math.exp(50 * math.log(0.98))); E(L4, 'screens[6].widget.answer', round(0.98 ** 50, 4))
lv.claim(round(0.5 ** 50 * 1e16, 1) == 8.9, '0.5^50 is about 8.9e-16', covers=[8.9, 0.5 ** 50])
lv.claim(0.98 ** 50 > 1 / 3, 'over a third survives', covers=[1 / 3])
E(L4, 'quiz[0].widget.answer', 3)


# copy task: retrain both units on three seeds with the frozen autograd
def sig(t):
    return 1.0 / (1.0 + (-t).exp())


def copy_batch(T, n, rng, noise=0.2):
    s = rng.choice([-1.0, 1.0], size=n)
    Xb = noise * rng.standard_normal((T, n))
    Xb[0] = s
    Fb = np.zeros((T, n))
    Fb[0] = 1.0
    return Xb, Fb, (s > 0).astype(float)


def init(kind, seed):
    g = np.random.default_rng(seed)
    names = ['w', 'ux', 'uf', 'b', 'v', 'd'] if kind == 'plain' else ['w', 'ux', 'uf', 'b', 'ax', 'af', 'ah', 'c', 'v', 'd']
    pp = {k: Tensor(0.5 * g.standard_normal()) for k in names}
    pp['w'] = Tensor(0.9)
    if kind == 'gated':
        pp['c'] = Tensor(-3.0)
    return pp


def forward(pp, Xb, Fb, kind):
    hh = Tensor(np.zeros(Xb.shape[1]))
    for t in range(Xb.shape[0]):
        cand = (pp['w'] * hh + pp['ux'] * Xb[t] + pp['uf'] * Fb[t] + pp['b']).tanh()
        if kind == 'plain':
            hh = cand
        else:
            z = sig(pp['ax'] * Xb[t] + pp['af'] * Fb[t] + pp['ah'] * hh + pp['c'])
            hh = (1.0 - z) * hh + z * cand
    return pp['v'] * hh + pp['d']


def bce(logit, y):
    m = logit * (2 * y - 1)
    return ((-m).exp() + 1.0).log().mean()


def np_acc(pp, T, kind):   # route B for accuracy: a plain NumPy forward pass from the trained numbers
    q = {k: float(t.data) for k, t in pp.items()}
    Xb, Fb, y = copy_batch(T, 1000, np.random.default_rng(99))
    hh = np.zeros(1000)
    for t in range(T):
        cand = np.tanh(q['w'] * hh + q['ux'] * Xb[t] + q['uf'] * Fb[t] + q['b'])
        if kind == 'plain':
            hh = cand
        else:
            z = 1 / (1 + np.exp(-(q['ax'] * Xb[t] + q['af'] * Fb[t] + q['ah'] * hh + q['c'])))
            hh = (1 - z) * hh + z * cand
    return float(((q['v'] * hh + q['d'] > 0) == (y > 0.5)).mean())


def train(kind, T, steps, seed, lr=0.5, n=64, c=1.0):
    pp = init(kind, seed)
    rng = np.random.default_rng(1000 + seed)
    for _ in range(steps):
        Xb, Fb, y = copy_batch(T, n, rng)
        for q in pp.values():
            q.zero_grad()
        L = bce(forward(pp, Xb, Fb, kind), y)
        L.backward()
        nrm = math.sqrt(sum(float((q.grad ** 2).sum()) for q in pp.values()))
        sc = min(1.0, c / max(nrm, 1e-12))
        for q in pp.values():
            q.data -= lr * sc * q.grad
    Xt, Ft, yt = copy_batch(T, 1000, np.random.default_rng(99))
    accA = float(((forward(pp, Xt, Ft, kind).data > 0) == (yt > 0.5)).mean())
    return accA, np_acc(pp, T, kind), L.item(), pp


# the gradients of both units against central differences, on one batch
for kind in ('plain', 'gated'):
    pp = init(kind, 4)
    Xb, Fb, y = copy_batch(7, 16, np.random.default_rng(5))
    lv.claim(grad_check(lambda: bce(forward(pp, Xb, Fb, kind), y), list(pp.values())) < 1e-6, f'copy task, {kind} unit: autograd against central differences')
ACC = {}
for kind in ('plain', 'gated'):
    for T in (5, 10, 20, 40):
        rs = [train(kind, T, 300, s) for s in range(3)]
        lv.claim(all(r[0] == r[1] for r in rs), f'{kind} T = {T}: accuracy by autograd and by a NumPy forward agree')
        ACC[(kind, T)] = [r[0] for r in rs]
print('copy accuracies', ACC)
st = F(L4)['screens'][7]['canvas']['state']['values']
for kind in ('plain', 'gated'):
    for T in (5, 10, 20, 40):
        lv.claim(abs(st[kind][f't{T}'] - round(sum(ACC[(kind, T)]) / 3, 3)) < 1e-12, f'bar {kind} T = {T} is the mean of the three seeds')
        E(L4, 'screens[7].explain.text', round(sum(ACC[(kind, T)]) / 3, 2))
fail_from = min(T for T in (5, 10, 20, 40) if max(ACC[('plain', T)]) < 0.6)
lv.claim(fail_from == 10 and max(ACC[('plain', 5)]) == 1.0 and sorted(ACC[('plain', 5)])[0] < 0.6, 'plain: two seeds of three solve T = 5; all fail from T = 10')
lv.claim(min(min(ACC[('gated', T)]) for T in (5, 10, 20)) == 1.0 and sorted(ACC[('gated', 40)])[:1][0] < 0.9 and sorted(ACC[('gated', 40)])[1] == 1.0, 'gated: perfect to T = 20; at T = 40 one seed of three falls short')
E(L4, 'screens[7].widget.answer', fail_from); E(L4, 'summary.ideas[2]', fail_from)
# graded training: 150 steps at T = 10 clear 0.95 on seeds 0 to 2 with margin
for s in range(3):
    a, b_, _, _ = train('gated', 10, 150, s)
    lv.claim(a >= 0.99, f'graded run: T = 10, 150 steps, seed {s} reaches {a} (threshold 0.95)')
LIT('0.05', why='the binding cap of test 4, a chosen setting')

# ================= review =================
two('review three steps', 0.8 * (0.8 * (0.8 * 1 + 0.5) - 1), 0.032); E('review', 'items[0].widget.answer', 0.032)
lv.claim(abs(0.8 + 0.5 - 1.3) < 1e-12 and abs(0.8 * 1.3 - 1 - 0.04) < 1e-12, 'review states 1.3 and 0.04', covers=[1.3, 0.04])
two('0.7^12', 0.7 ** 12, math.exp(12 * math.log(0.7))); E('review', 'items[1].widget.answer', round(0.7 ** 12, 5)); E('review', 'items[1].widget.wrong[1].value', round(0.7 ** 11, 5))
two('Q eigenvalue size', float(max(abs(np.linalg.eigvals([[0, 1.1], [0.9, 0]])))), math.sqrt(0.99)); E('review', 'items[2].widget.options', 0.995)
lv.claim(np.allclose(sorted(np.linalg.eigvals([[0.5, 0.5], [0.5, 0.5]]).real), [0, 1]), 'R eigenvalues 0 and 1', covers=[0.95, 0.99])
E('review', 'items[3].widget.answer', -0.5); two('review clip norm', float(np.linalg.norm([2, -1, 2])), 3.0)
two('review sum grad', 0.25 * 4 + 0.5 * 2 + 1, 3.0); E('review', 'items[4].widget.answer', 3)
two('review fit', 2.5 / 5, float(np.linalg.lstsq(np.array([[2.0], [1.0]]), np.array([1.0, 0.5]), rcond=None)[0][0])); E('review', 'items[5].widget.wrong[0].value', round(2.5 / 5.25, 4))
two('review gate', 0.75 * -0.4 + 0.25 * 0.6, -0.15); E('review', 'items[6].widget.answer', -0.15)
two('review count', sum(np.zeros(s).size for s in ((8, 8), (8, 2), (8,), (8,), (1,))), 97); lv.claim(8 * 8 == 64, 'W holds 64', covers=[64]); E('review', 'items[7].widget.wrong[0].value', 97000)
E('review', 'items[8].widget.answer', round(math.tanh(0.5), 4))

# ================= problems =================
ev = sorted(np.linalg.eigvals([[0.6, 0.5], [0.2, 0.9]]).real)
two('problem eigenvalues', ev[1], 0.75 + math.sqrt(0.75 ** 2 - 0.44)); lv.claim(abs(ev[0] - 0.4) < 1e-12, 'smaller eigenvalue 0.4', covers=[0.4, 0.35, 0.1225, 0.75])
g20 = 1.1 ** 20
two('1.1^20', g20, math.exp(20 * math.log(1.1))); E('problems', 'items[0].parts[1].widget.answer', round(g20, 2))
E('problems', 'items[0].parts[2].widget.answer', round(1 / (0.5 * g20), 4)); E('problems', 'items[0].parts[2].widget.wrong[0].value', round(1 / g20, 4))
lv.claim(round(g20, 4) == 6.7275 and round(0.5 * g20, 4) == 3.3637, 'arriving norm 3.3637', covers=[6.7275, 3.3637])
E('problems', 'items[0].parts[3].widget.answer', round(0.9 / 1.1, 4)); E('problems', 'items[0].parts[3].widget.wrong[0].value', round(1.1 / 0.9, 4))
two('problem h2', 0.6 * 2 + 2 * 0.5, 2.2); two('problem dh2/du', 0.6 * 1 + 0.5, 1.1); two('problem dL/dw', 2 * 0.2 * 2, 0.8)
lv.claim(abs((lambda f: (f(0.6 + eps) - f(0.6 - eps)) / (2 * eps))(lambda wv: (wv * 2 * 1 + 2 * 0.5 - 2) ** 2) - 0.8) < 1e-6, 'dL/dw by central differences')
two('0.95^30', 0.95 ** 30, math.exp(30 * math.log(0.95))); E('problems', 'items[2].parts[0].widget.answer', round(0.95 ** 30, 4))
E('problems', 'items[2].parts[1].widget.answer', round(0.63 ** 30 * 1e6, 2)); lv.claim(round(0.63 ** 30 * 1e6, 2) == 0.96, '0.96 x 10^-6', covers=[0.63 ** 30]); E('problems', 'items[2].parts[1].widget.wrong[0].value', round(0.9 ** 30 * 1e6, 2))
kk = math.log(0.01) / math.log(0.95)
lv.claim(math.ceil(kk) == 90 and 0.95 ** 89 > 0.01 > 0.95 ** 90, f'first step below 1%: 90 ({kk:.2f})', covers=[round(kk, 2), round(0.95 ** 89, 4)])
two('0.99^90', 0.99 ** 90, math.exp(90 * math.log(0.99))); E('problems', 'items[2].parts[3].widget.answer', round(0.99 ** 90, 4))
lv.claim(round(0.99 ** 90 / 0.95 ** 90, -1) == 40.0, 'forty times more', covers=[40])
lv.claim(round((math.log(0.01) / math.log(0.99)) / kk) == 5, 'the 1% horizon moves about five times as far back (458 against 90 steps)')
LIT('five times', why='checked above: the 1% horizon moves from 90 to 458 steps')
hl = math.log(0.5) / math.log(0.97)
E('problems', 'items[3].parts[1].widget.answer', round(hl, 1)); E('problems', 'items[3].parts[1].widget.wrong[0].value', round(0.5 / 0.03, 1))
v3 = 0.97 * 0.0004 + 0.03 * 0.0001
two('problem variance', v3, 0.000391); E('problems', 'items[3].parts[2].widget.answer', round(math.sqrt(v3), 6))
lv.claim(round(math.sqrt(v3), 4) == 0.0198, '1.98%', covers=[0.0198, 1.98, 0.000388, 0.000003])

# ================= homework =================
nrm = math.sqrt(20)
two('homework norm', nrm, float(np.linalg.norm(np.r_[[1, -2, 2, 0], [1], [-3, 1]]))); lv.claim(round(nrm, 4) == 4.4721, 'norm sqrt(20)', covers=[4.4721, 20])
E('homework', 'items[0].widget.answer', round(-6 / nrm, 4)); E('homework', 'items[0].widget.wrong[0].value', round(-6 / math.sqrt(10), 4)); E('homework', 'items[0].explain.text', round(2 / nrm, 4))
r = float(abs(np.linalg.eigvals([[0.5, -0.6], [0.6, 0.5]])[0]))
two('homework radius', r, math.sqrt(0.61)); lv.claim(round(r, 4) == 0.781, 'radius 0.7810', covers=[0.781]); E('homework', 'items[2].widget.answer', math.ceil(math.log(0.01) / math.log(r)))
E('homework', 'items[2].explain.text', round(math.log(0.01) / math.log(r), 2)); E('homework', 'items[2].widget.wrong[0].value', math.ceil(math.log(0.01) / math.log(0.6))); E('homework', 'items[2].widget.wrong[1].value', math.ceil(math.log(0.01) / math.log(0.5)))
two('homework windows', 5000 / 50, 100)
lv.claim(round(0.8 ** 10, 2) == 0.11 and round(0.8 ** 20, 3) == 0.012, 'longform figures 0.11 and 0.012', covers=[0.11, 0.012])

# ================= code widgets: solution, starter, mutants =================


def judge(a, e, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def close(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) and isinstance(y, dict):
            return set(x) == set(y) and all(close(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p_, q_) for p_, q_ in zip(x, y))
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y

    def same(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) and isinstance(y, dict):
            return set(x) == set(y) and all(same(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p_, q_) for p_, q_ in zip(x, y))
        return bool(x == y)
    return close(a, e) if cmp == 'isclose' else same(a, e)


def first_fail(w, src):
    cwd, d = os.getcwd(), tempfile.mkdtemp()
    os.chdir(d)
    try:
        for k, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), os.path.join(d, k))
        sys.path.insert(0, d)
        sys.modules.pop('autograd', None)
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
        sys.path.remove(d)
        shutil.rmtree(d, ignore_errors=True)
        sys.modules.pop('autograd', None)
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

# the homework's hand-written backward pass, route B: autograd.py on the same planted nets
hw = F('homework')['items'][7]['widget']
ns = {}
exec(hw['prelude'].replace('def fd_rel_err', 'def _unused'), ns)


def bptt_autograd(x, y, params):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    hh = Tensor(np.zeros((1, P['Wh'].shape[0])))
    tot = None
    for t in range(x.shape[0]):
        hh = (Tensor(x[t:t + 1]) @ P['Wx'] + hh @ P['Wh'] + P['b']).tanh()
        e_ = hh @ P['Wy'] + P['by'] - y[t:t + 1]
        sq = (e_ * e_).sum()
        tot = sq if tot is None else tot + sq
    loss = tot * (0.5 / x.shape[0])
    loss.backward()
    return loss.item(), {k: t.grad for k, t in P.items()}


ns2 = {}
exec(hw['solution'], ns2)
for args in (ns['small'], ns['medium'], ns['planted'](1, 2, 3, 1, 2), ns['planted'](20, 1, 4, 1, 3)):
    la, ga = bptt_autograd(*args)
    lh, gh = ns2['rnn_bptt'](*args)
    lv.claim(abs(la - lh) < 1e-12 and all(np.allclose(ga[k], gh[k], rtol=1e-10, atol=1e-13) for k in ga), f'rnn_bptt equals the autograd on a planted net of {args[0].shape[0]} steps')

lv.check_wrongs()
# ---------------- givens and stated settings (not computed results) ----------------
for t_, why in [('250', 'trading days in a year, a stated setting'), ('500', 'series lengths and day counts set in the questions'), ('1,000', 'test sequences and series lengths, stated settings'),
                ('5,000', 'the homework series length, a given'), ('510', 'minutes of the London session, checked above as 8.5 hours'), ('0.003', 'the hook run\'s step size, a setting'),
                ('0.2', 'noise sd of the copy task and other givens'), ('0.97', 'a given decay'), ('0.03', 'a given weight'), ('1.5', 'given clip thresholds and states'),
                ('1.0', 'a given input value'), ('2.0', 'a given input value'), ('0.8', 'given weights and states'), ('0.5', 'given weights'), ('0.25', 'a given gate'),
                ('0.6', 'given weights'), ('0.4', 'given states and data'), ('0.7', 'given weights'), ('1.1', 'given weights'), ('0.9', 'given weights'),
                ('0.95', 'given factors'), ('0.98', 'a given gate factor'), ('0.02', 'given gate and step sizes'), ('0.01', 'given gate and returns'), ('0.0001', 'a given variance'),
                ('0.0004', 'a given variance'), ('0.1', 'given step sizes and gates'), ('1.05', 'a given eigenvalue'), ('0.85', 'a given eigenvalue'), ('1.2', 'given weights'),
                ('0.63', 'a given per-step factor'), ('0.5370', 'tanh(0.6), checked above'), ('0.53705', 'tanh(0.6), checked above'), ('1.0954', 'the size of the test matrix\'s eigenvalues, sqrt(1.2)'),
                ('3.3637', 'checked above'), ('16.5', 'session end in hours'), ('2.75', 'lesson 2 hook answer, checked above'), ('2.4', 'a given clip threshold'), ('60', 'days in the hook and in the transfer, given'), ('200', 'gradient-descent steps, a setting'), ('10^-6', 'test tolerances and units, settings'), ('10^-5', 'the nudge of autograd.grad_check, as shipped'), ('0.69', 'a given nudge point'), ('0.71', 'a given nudge point'), ('30', 'window lengths, steps and degrees given in the questions'), ('20', 'steps and the series length given in the questions'), ('150', 'graded training steps, a setting'), ('1.06', 'a bound on the entries of D, which are at most 1.05'), ('-1.2', 'a given test input'),
                ('9.46', 'checked above'), ('26.57', 'checked above')]:
    LIT(t_, why=why)
LIT('8.9 \\times 10^{-16}', why='0.5^50, checked by a claim above; the scientific form is read apart from it')
LIT('0.96 \\times 10^{-6}', why='0.63^30, checked by a claim above; the scientific form is read apart from it')
LIT('four times', why='an LSTM has four weight sets per unit and a GRU three, a cost stated in the model answer')
lv.claim(abs(math.sqrt(1.2) - 1.0954) < 5e-5, 'the eigenvalues of [[0, -1.2], [1, 0]] have size sqrt(1.2) = 1.0954')
lv.report()
