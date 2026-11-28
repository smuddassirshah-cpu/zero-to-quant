"""Recompute every number stated in cnn level 1 (Convolution as a sliding dot product) and check each at its JSON path.

Run: <venv>/bin/python docs/reports/cnn-L1-numbers.py   (NumPy and pandas; exits 0 when every check passes)

Route A is the lesson generators' NumPy (np.correlate, sliding windows, the shipped autograd.py with cnn_ops_l1.py).
Route B, here, is independent: plain Python loops, np.convolve with the kernel reversed, pandas rolling means, closed forms,
and this script's own central differences. The shipped autograd.py and cnn_ops_l1.py are checked byte for byte against the
canonical files; conv1d and conv2d are gradient-checked to 1e-6 in float64 by both routes. Every code widget is run: the model
solution passes its hidden tests, the starter fails, and each mutant first fails the test it names (ENGINE-BACKLOG 1263).
"""
import hashlib
import math
import os
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

AI = os.path.join(ROOT, 'app', 'content', 'data', 'ai')
CANON = open(os.path.join(AI, 'autograd.py'), encoding='utf8').read()
OPS = open(os.path.join(AI, 'cnn_ops_l1.py'), encoding='utf8').read()
sys.path.insert(0, AI)
from autograd import Tensor, grad_check, sgd_step  # noqa: E402
from cnn_ops_l1 import conv1d, conv2d  # noqa: E402

lv = Level('cnn', 1)
E = lv.expect


def two(label, a, b, tol=1e-9):
    a, b = np.asarray(a, float), np.asarray(b, float)
    lv.claim(a.shape == b.shape and np.allclose(a, b, rtol=tol, atol=tol), f'{label}: routes agree')


def corr1(x, k):
    """Route B: the unflipped valid slide by plain loops."""
    x, k = list(map(float, x)), list(map(float, k))
    return [sum(k[j] * x[t + j] for j in range(len(k))) for t in range(len(x) - len(k) + 1)]


def corr2(X, K):
    X, K = np.asarray(X, float), np.asarray(K, float)
    kh, kw = K.shape
    return np.array([[sum(K[a, b] * X[i + a, j + b] for a in range(kh) for b in range(kw)) for j in range(X.shape[1] - kw + 1)] for i in range(X.shape[0] - kh + 1)])


def central(f, arrays, h=1e-5):
    out = []
    for A in arrays:
        g = np.zeros_like(A)
        for i in np.ndindex(A.shape):
            keep = A[i]; A[i] = keep + h; up = f(); A[i] = keep - h; down = f(); A[i] = keep
            g[i] = (up - down) / (2 * h)
        out.append(g)
    return out


def relerr(gs, ns):
    d = max(np.abs(a - b).max() for a, b in zip(gs, ns))
    return d / max(max(np.abs(a).max() for a in gs), max(np.abs(b).max() for b in ns), 1e-12)


# =================== 1. the shipped files and the ops ===================
sha_a, sha_o = hashlib.sha256(CANON.encode()).hexdigest(), hashlib.sha256(OPS.encode()).hexdigest()
lv.claim(sha_a.startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0 (SHA-256 5917d4ec91f7...)')
seen = {'autograd.py': 0, 'cnn_ops_l1.py': 0}


def walk(node):
    if isinstance(node, dict):
        fs = node.get('files')
        if isinstance(fs, dict):
            for name, text in fs.items():
                want = {'autograd.py': sha_a, 'cnn_ops_l1.py': sha_o}.get(name)
                lv.claim(want is not None and hashlib.sha256(text.encode()).hexdigest() == want, f'shipped {name} is byte-identical to the canonical file')
                seen[name] = seen.get(name, 0) + 1
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


for doc in lv.files.values():
    walk(doc)
lv.claim(seen['autograd.py'] >= 2 and seen['cnn_ops_l1.py'] >= 2, f'files shipped: {seen}')
lv.claim(len(OPS.encode()) < 256 * 1024 and 'autograd' in OPS.split('def ')[0], 'cnn_ops_l1.py is small and imports the frozen autograd')

r = np.random.default_rng(2026)
for n, m in [(20, 4), (9, 3), (5, 5)]:
    x, k, W = r.standard_normal(n), r.standard_normal(m), r.standard_normal(n - m + 1)
    xt, kt = Tensor(x.copy()), Tensor(k.copy())
    ra = grad_check(lambda: (conv1d(xt, kt) * W).sum() + (conv1d(xt, kt) ** 2).mean(), [xt, kt])
    xt.zero_grad(); kt.zero_grad(); ((conv1d(xt, kt) * W).sum() + (conv1d(xt, kt) ** 2).mean()).backward()
    f = lambda: float(np.dot(corr1(x, k), W) + np.mean(np.square(corr1(x, k))))  # noqa: E731
    rb = relerr([xt.grad, kt.grad], central(f, [x, k]))
    two(f'conv1d forward n={n} k={m}', conv1d(Tensor(x), Tensor(k)).data, corr1(x, k))
    lv.claim(ra < 1e-6 and rb < 1e-6, f'conv1d gradient n={n}, k={m}: grad_check {ra:.1e}, own central differences {rb:.1e}')
for (h, w_), (kh, kw) in [((7, 6), (3, 2)), ((8, 8), (3, 3)), ((4, 4), (4, 4))]:
    X, K = r.standard_normal((h, w_)), r.standard_normal((kh, kw)); Wt = r.standard_normal((h - kh + 1, w_ - kw + 1))
    Xt, Kt = Tensor(X.copy()), Tensor(K.copy())
    ra = grad_check(lambda: ((conv2d(Xt, Kt) * Wt) ** 2).mean(), [Xt, Kt])
    Xt.zero_grad(); Kt.zero_grad(); ((conv2d(Xt, Kt) * Wt) ** 2).mean().backward()
    rb = relerr([Xt.grad, Kt.grad], central(lambda: float(((corr2(X, K) * Wt) ** 2).mean()), [X, K]))
    two(f'conv2d forward {h}x{w_} k {kh}x{kw}', conv2d(Tensor(X), Tensor(K)).data, corr2(X, K))
    lv.claim(ra < 1e-6 and rb < 1e-6, f'conv2d gradient {h}x{w_}, k {kh}x{kw}: grad_check {ra:.1e}, own central differences {rb:.1e}')

# =================== 2. l1 ===================
C = [12.40, 12.55, 12.31, 12.48, 12.62, 12.44, 12.70, 12.85, 12.66, 12.90, 13.05, 12.98]
ma = pd.Series(C).rolling(3).mean()
E('l1', 'screens[0].feedback.correct', round(ma[6], 4)); two('l1 hook mean', ma[6], sum(C[4:7]) / 3)
E('l1', 'screens[1].widget.answer', 10); E('l1', 'screens[1].widget.wrong[0].value', 12); E('l1', 'screens[1].widget.wrong[1].value', 9)
lv.claim(int(ma.notna().sum()) == 10 == len(corr1(C, [1 / 3] * 3)), '10 valid outputs by pandas and by the loop')
for t in range(10):
    E('l1', f'screens[1].canvas.controls[0].frames[{t}].caption', round(ma[t + 2], 4), fmt='{:.4f}')
E('l1', 'screens[2].widget.answer', 231); E('l1', 'screens[2].widget.wrong[1].value', 230); E('l1', 'screens[2].widget.wrong[2].value', 19)
lv.claim(len(corr1(range(250), [1] * 20)) == 231 and int(pd.Series(range(250)).rolling(20).mean().isna().sum()) == 19, '231 outputs and 19 NaNs')
kw = [0.2, 0.3, 0.5]; yw = corr1(C, kw); yr = np.convolve(C, kw, 'valid')   # convolve reverses kw: the flipped slip
for i in range(2):
    E('l1', f'screens[3].widget.rows[{i}][1].answer', round(yw[i], 3)); E('l1', f'screens[3].widget.rows[{i}][1].wrong[0].value', round(yr[i], 3))
two('l1 weighted outputs', yw[:2], [12.400, 12.443], 1e-9)
raw = [0.5 * 0.5 ** j for j in range(5)]
E('l1', 'screens[4].prose', sum(raw)); E('l1', 'screens[4].widget.answer', round(raw[0] / sum(raw), 3)); E('l1', 'screens[4].widget.wrong[1].value', round(raw[4] / sum(raw), 3))
E('l1', 'screens[4].explain.text', round(raw[1] / sum(raw), 3)); E('l1', 'screens[4].explain.text', round(raw[3] / sum(raw), 3))
E('l1', 'screens[5].widget.answer', 0 + 3 - 1)
xs5 = [3, 5, 4, 8, 6]
lv.claim(corr1(xs5, [1, 0, -1]) == [-1, -3, -2] and np.convolve(xs5, [1, 0, -1], 'valid').tolist() == [1, 3, 2], 'the flip: -1, -3, -2 against 1, 3, 2')
E('l1', 'screens[6].widget.answer', 1); E('l1', 'screens[6].widget.wrong[0].value', -1); E('l1', 'screens[6].widget.wrong[1].value', 3)
spk = [0] * 5 + [1] + [0] * 14; out = corr1(spk, kw)
lv.claim(out[3:6] == [0.5, 0.3, 0.2], 'a spike echoes 0.5, 0.3, 0.2 (the kernel newest first)')
ek = lambda a, L: [a * (1 - a) ** j / sum(a * (1 - a) ** i for i in range(L)) for j in range(L)][::-1]  # noqa: E731
E('l1', 'screens[10].widget.tests[2].expect', str([round(v, 6) for v in ek(0.5, 5)]))
E('l1', 'screens[10].widget.tests[3].expect', str([round(v, 6) for v in ek(0.3, 3)]))
E('l1', 'quiz[0].widget.wrong[0].value', 3 - 5 + 1)
E('l1', 'quiz[2].widget.answer', 0.25 * 4 + 0.25 * 6 + 0.5 * 8); E('l1', 'quiz[2].widget.wrong[0].value', 0.5 * 4 + 0.25 * 6 + 0.25 * 8); E('l1', 'quiz[2].widget.wrong[1].value', corr1([2, 4, 6, 8], [0.25, 0.25, 0.5])[0])

# =================== 3. l2 ===================
rg = np.random.default_rng(22)
P = 100 + np.cumsum(rg.normal(0, 0.4, 30)); P[18] += 3; P = np.round(P, 2)
sp, d2 = corr1(P, [-1, -1, 4, -1, -1]), corr1(P, [1, -2, 1])
lv.claim(int(np.argmax(sp)) == 16 and int(np.argmin(d2)) == 17, 'spike output peaks on the window centred on day 18; the bend dips there')
E('l2', 'screens[0].explain.text', round(sp[16], 2)); E('l2', 'screens[0].explain.text', round(d2[17], 2))
Y = corr1([1, 0, 1, 0, 1, 3, 1, 0, 1, 0, 0, 1], [1, 3, 1])
lv.claim(Y == [2, 3, 2, 6, 11, 6, 2, 3, 1, 1], 'matched-kernel outputs')
E('l2', 'screens[1].widget.answer', int(np.argmax(Y))); E('l2', 'screens[1].feedback.correct', max(Y))
cs = 6 / math.sqrt(10 * 11)
E('l2', 'screens[2].widget.answer', round(cs, 3)); E('l2', 'screens[2].widget.wrong[1].value', round(6 / 11, 3))


def ncorr_b(x, k):
    """Route B: Pearson correlation of each window with the kernel (pandas), 0 on a flat window."""
    out = []
    for t in range(len(x) - len(k) + 1):
        w = pd.Series(x[t:t + len(k)], dtype=float)
        out.append(0.0 if w.std() == 0 else float(w.corr(pd.Series(k, dtype=float))))
    return out


rr = ncorr_b(list(P), [-1, -1, 4, -1, -1])
lv.claim([t for t, v in enumerate(rr) if v > 0.7] == [2, 16] and [t for t, v in enumerate(rr) if v > 0.9] == [16], 'threshold 0.7 flags 2 and 16; 0.9 flags 16')
E('l2', 'screens[5].feedback.correct', round(rr[16], 3)); E('l2', 'screens[5].feedback.correct', round(rr[2], 3))
E('l2', 'screens[5].widget.wrong[1].value', sum(v > 0 for v in rr))
E('l2', 'screens[4].widget.answer', round(C[0] - 2 * C[1] + C[2], 2)); E('l2', 'screens[4].widget.wrong[1].value', round(C[0] - C[1], 2))
XT = [100 + t for t in range(30)]; XT[6] += 4
bt = corr1(XT, [1, 3, 1]); nt = ncorr_b(XT, [1, 3, 1])
E('l2', 'screens[6].prose', bt[5]); E('l2', 'screens[6].prose', max(bt)); lv.claim(int(np.argmax(bt)) == 27 and int(np.argmax(nt)) == 5, 'trap: raw peaks at 27, normalised at 5')
E('l2', 'screens[6].explain.text', round(max(nt), 3))
E('l2', 'screens[7].widget.answer', corr1([0] + C[:2], [1, -2, 1])[0]); E('l2', 'screens[7].widget.wrong[0].value', round(corr1(C[:1] + C[:2], [1, -2, 1])[0], 2))
E('l2', 'screens[10].widget.tests[0].expect', str([round(v, 6) for v in corr1(C[:4], [1, -2, 1])]))
vr = np.random.default_rng(3); V = vr.poisson(200, 60).astype(float); V[40] *= 3
rv = ncorr_b(list(V), [-1, -1, 4, -1, -1])
lv.claim([t for t, v in enumerate(rv) if v > 0.95] == [38] and [t for t, v in enumerate(rv) if v > 0.9] == [38, 47], 'volume detections [38] and [38, 47]')
E('l2', 'quiz[1].widget.answer', round(4 / math.sqrt(2 * 20), 3)); E('l2', 'quiz[2].widget.answer', len(corr1([0, 0] + C + [0, 0], [1] * 5)))

# =================== 4. l3 ===================
STROKE = np.zeros((8, 8), int); STROKE[1, 1:6] = 4; STROKE[2, 5] = 4; STROKE[3, 4] = STROKE[4, 4] = 4; STROKE[5, 3] = STROKE[6, 3] = 4
IMG = STROKE + np.random.default_rng(8).integers(0, 2, (8, 8)) * (STROKE == 0)
KV = np.array([[-1, 0, 1]] * 3); KH = KV.T
GV, GH = corr2(IMG, KV), corr2(IMG, KH)
two('l3 shown image', np.array(lv.files['l3-convolution-in-2d']['screens'][0]['canvas']['params']['matrices'][0]['rows']), IMG)
for i, (a, b) in enumerate([(1, 3), (1, 4), (2, 3)]):
    E('l3', f'screens[0].widget.rows[{i}][1].answer', int(GV[a, b]))
    alt = corr2(IMG, KV[:, ::-1])[a, b]
    if alt != GV[a, b]:
        E('l3', f'screens[0].widget.rows[{i}][1].wrong[0].value', int(alt))
E('l3', 'screens[1].widget.answer', 28 - 5 + 1); E('l3', 'screens[1].explain.text', 24 * 24)
E('l3', 'screens[3].widget.answer', 4 * 6 * 6); E('l3', 'screens[3].widget.wrong[1].value', 4 * 64)
PT = np.array([[1, 2, 0], [0, 1, 3], [2, 0, 1]])
E('l3', 'screens[5].widget.answer', int(corr2(PT, KV)[0, 0])); E('l3', 'screens[5].widget.wrong[0].value', int((PT @ KV)[0, 0]))
E('l3', 'screens[5].widget.wrong[1].value', int((PT @ KV).sum())); E('l3', 'screens[5].widget.wrong[2].value', int(corr2(PT, -KV)[0, 0]))
E('l3', 'screens[6].widget.answer', 0.5 * 8 + 0.25 * 4); E('l3', 'screens[6].widget.wrong[0].value', 4)
E('l3', 'screens[8].widget.tests[0].expect', str([float(v) for v in GV[1]]))
E('l3', 'screens[9].widget.tests[1].expect', str([float(v) for v in GH[0]]))
EM = np.hypot(GV, GH)
E('l3', 'screens[10].widget.tests[0].expect', str([round(float(v), 4) for v in EM[0]]))
E('l3', 'screens[10].explain.text', round(math.sqrt(8), 2))
E('l3', 'quiz[0].widget.answer', 8 * 8); E('l3', 'quiz[1].widget.answer', int(corr2([[2, 0, 1], [3, 1, 0], [0, 2, 4]], KH)[0, 0]))

# =================== 5. l4 ===================
rg = np.random.default_rng(20); x = rg.standard_normal(200); y = np.convolve(x, [0.5, 0.3, 0.2], 'valid') + 0.1 * rg.standard_normal(198)
A = np.array([x[t:t + 3] for t in range(198)]); kls = np.linalg.solve(A.T @ A, A.T @ y)   # route B: normal equations
kt = Tensor(np.zeros(3)); xt = Tensor(x)
for _ in range(100):
    kt.zero_grad(); L = ((conv1d(xt, kt) - y) ** 2).mean(); L.backward(); sgd_step([kt], 0.1)
floor = float(((A @ kls - y) ** 2).mean())
two('l4 learned kernel', kt.data, kls, 1e-8)
E('l4', 'screens[4].prose', round(kls[0], 3), fmt='{:.3f}'); E('l4', 'screens[4].prose', round(kls[2], 3), fmt='{:.3f}')
E('l4', 'screens[4].feedback.correct', round(floor, 4), fmt='{:.4f}'); E('l4', 'screens[4].widget.answer', 0.01)
E('l4', 'screens[1].widget.answer', round(kls[2], 2))
lv.claim(abs(lv.files['l4-learning-a-kernel']['screens'][1]['canvas']['params']['functions'][0]['expr'].count(f'{kls[2]:.6f}')) == 1, 'plane parabola bottom at the least-squares weight')
xh, kh, th = [1, 2, 0, -1, 3], [0.5, 0.5], [1, 1, 0, 2]
eh = [a - b for a, b in zip(corr1(xh, kh), th)]; g0 = 2 / 4 * sum(e * xh[t] for t, e in enumerate(eh))
E('l4', 'screens[2].widget.answer', g0); E('l4', 'screens[2].widget.wrong[0].value', g0 * 2); E('l4', 'screens[2].widget.wrong[1].value', g0 / 2); E('l4', 'screens[2].widget.wrong[2].value', g0 * 4)
kts = Tensor(np.zeros(3)); hs = []
for _ in range(3):
    kts.zero_grad(); L = ((conv1d(xt, kts) - y) ** 2).sum(); L.backward(); hs.append(L.item()); sgd_step([kts], 0.1)
E('l4', 'screens[5].prose', round(hs[0], 1), fmt='{:.1f}'); E('l4', 'screens[5].prose', f'{hs[1]:,.0f}')
lv.claim(hs[2] > hs[1] > 1000 * hs[0], 'summed loss blows up')
r21 = np.random.default_rng(21); X5 = r21.standard_normal(1000); Y5 = np.convolve(X5, [0.5, 0.3, 0.2, -0.2, 0.1], 'valid') + 0.1 * r21.standard_normal(996)
A5 = np.array([X5[t:t + 3] for t in range(996)]); k5 = np.linalg.solve(A5.T @ A5, A5.T @ Y5); fl5 = float(((A5 @ k5 - Y5) ** 2).mean())
E('l4', 'screens[6].prose', round(k5[0], 3), fmt='{:.3f}'); E('l4', 'screens[6].feedback.correct', round(fl5, 4), fmt='{:.4f}')
E('l4', 'screens[6].widget.answer', 0.01 + 0.3 ** 2 + 0.5 ** 2); E('l4', 'screens[6].widget.wrong[1].value', 0.01 + 0.5 ** 2)
lv.claim(abs(fl5 - 0.35) < 0.01, f'short-kernel floor {fl5:.4f} near 0.35')
xg = np.random.default_rng(1).standard_normal(12); kg = np.random.default_rng(2).standard_normal(3); tg = np.random.default_rng(3).standard_normal(10)
X1t, K1t = Tensor(xg.copy()), Tensor(kg.copy())
gc = grad_check(lambda: ((conv1d(X1t, K1t) - tg) ** 2).mean(), [X1t, K1t])
E('l4', 'screens[3].canvas.params.lines[4]', f'{gc:.1e}')
E('l4', 'quiz[0].widget.answer', round(2 / 3 * 4, 2)); E('l4', 'quiz[0].widget.wrong[1].value', round(2 / 3 * 1, 2)); E('l4', 'quiz[2].widget.answer', 0.04 + 0.6 ** 2)
E('l4', 'screens[11].explain.text', 5 / 250 * 100)

# =================== 6. review, homework, problems ===================
E('review', 'items[0].widget.answer', corr1([3, 1, 4, 1], [1, 2, -1])[0]); E('review', 'items[0].widget.wrong[0].value', corr1([3, 1, 4, 1], [-1, 2, 1])[0])
E('review', 'items[1].widget.answer', 60 - 7 + 1); E('review', 'items[4].widget.answer', 12 - 5 + 1)
lv.claim(corr1([5, 7, 6, 6], [-1, 1]) == [2, -1, 0] and np.convolve([1, 2, 4], [1, -1], 'valid').tolist() == [1, 2], 'review kernels and flip')
er = [a - b for a, b in zip(corr1([2, 1, 3, 0], [1, -1]), [0, -1, 2])]
E('review', 'items[6].widget.answer', round(2 / 3 * sum(e * [2, 1, 3, 0][t] for t, e in enumerate(er)), 2))
E('review', 'items[6].widget.wrong[1].value', round(2 / 3 * sum(e * [2, 1, 3, 0][t + 1] for t, e in enumerate(er)), 2))
E('review', 'items[7].widget.answer', round(pd.Series([6, 2, 4.]).corr(pd.Series([1, 0, -1.])), 2))
E('review', 'items[7].widget.wrong[1].value', round((6 - 4) / (math.sqrt(36 + 4 + 16) * math.sqrt(2)), 2))
E('review', 'items[8].widget.answer', 0.1 / 500)
E('homework', 'items[0].widget.tests[4].expect', '[[[122.0]]]'); lv.claim(sum(range(16)) + 2 == 122, '1 by 1 output of a full-size kernel: 120 + 2')
E('homework', 'items[4].widget.answer', 3 + 3 - 0.5)
X6 = np.array([[1, 2, 0], [0, 2, 3], [2, 1, 1]]); G6 = np.array([[2, 0], [0, -1]])
dK = np.array([[sum(G6[i, j] * X6[i + a, j + b] for i in range(2) for j in range(2)) for b in range(2)] for a in range(2)])
E('homework', 'items[5].widget.answer', int(dK[0, 1])); E('homework', 'items[5].widget.wrong[0].value', int(dK[1, 0])); E('homework', 'items[5].widget.wrong[1].value', int(dK[0, 0]))
E('homework', 'items[7].widget.answer', 10 / 500); E('homework', 'items[7].widget.wrong[0].value', 500 / 10)
X1 = np.array([[0, 1, 2, 1], [1, 3, 1, 0], [2, 1, 0, 1], [0, 1, 1, 3]]); K1 = np.array([[1, -1], [0, 2]])
Y1 = corr2(X1, K1)
E('problems', 'items[0].parts[0].widget.answer', int(Y1[0, 0])); E('problems', 'items[0].parts[0].widget.wrong[0].value', int(corr2(X1, K1[::-1, ::-1])[0, 0]))
E('problems', 'items[0].parts[0].widget.wrong[1].value', int((X1[:2, :2] @ K1).sum()))
E('problems', 'items[0].parts[1].widget.answer', int(Y1[0].sum()))
g11 = sum(X1[1, j + 1] for j in range(3)); E('problems', 'items[0].parts[2].widget.answer', int(g11)); E('problems', 'items[0].parts[2].widget.wrong[0].value', int(X1[0, :3].sum()))
E('problems', 'items[0].parts[3].widget.answer', 2 - 0.1 * g11); E('problems', 'items[0].parts[3].widget.wrong[0].value', 2 + 0.1 * g11)
xs8 = [100, 102, 101, 104, 103, 105, 107, 106]; y8 = corr1(xs8, [0.25, 0.25, 0.5]); y8f = np.convolve(xs8, [0.25, 0.25, 0.5], 'valid')
E('problems', 'items[1].parts[0].widget.answer', len(y8)); E('problems', 'items[1].parts[1].widget.answer', y8[1]); E('problems', 'items[1].parts[1].widget.wrong[0].value', y8f[1])
E('problems', 'items[1].parts[1].widget.wrong[1].value', y8[0]); E('problems', 'items[1].parts[2].widget.answer', 1 + 3 - 1)
E('problems', 'items[1].parts[3].widget.answer', corr1([0] + xs8, [0.25, 0.25, 0.5])[0]); E('problems', 'items[1].parts[3].widget.wrong[0].value', corr1([100] + xs8, [0.25, 0.25, 0.5])[0])
x3, t3 = [1, 0, 2, 1], [0.5, 1, 2]
e3 = [a - b for a, b in zip(corr1(x3, [1, 1]), t3)]; L3 = sum(e * e for e in e3) / 3
g = [2 / 3 * sum(e * x3[t + j] for t, e in enumerate(e3)) for j in range(2)]
k3n = [1 - 0.1 * g[0], 1 - 0.1 * g[1]]; e3n = [a - b for a, b in zip(corr1(x3, k3n), t3)]; L3n = sum(e * e for e in e3n) / 3
E('problems', 'items[2].parts[0].widget.answer', L3); E('problems', 'items[2].parts[0].widget.wrong[0].value', 3 * L3)
E('problems', 'items[2].parts[1].widget.answer', round(g[0], 4)); E('problems', 'items[2].parts[1].widget.wrong[1].value', g[1])
E('problems', 'items[2].parts[2].widget.answer', round(k3n[0], 4)); E('problems', 'items[2].parts[2].widget.wrong[0].value', round(1 + 0.1 * g[0], 4))
E('problems', 'items[2].parts[3].widget.answer', round(L3n, 3)); E('problems', 'items[2].parts[3].widget.wrong[1].value', round(3 * L3n, 3))


# =================== 7. every code widget: solution, starter, mutants ===================
def passes(t, ns):
    try:
        if t.get('setup'):
            exec(t['setup'], ns)
        got = eval(t['call'], ns)
    except Exception as e:  # noqa
        return t.get('compare') == 'raises' and type(e).__name__ == t['expect']
    if t.get('compare') == 'raises':
        return False
    try:
        return bool(got == eval(t['expect'], ns)) or repr(got) == t['expect']
    except Exception:  # noqa
        return False


def first_fail(w, src):
    cwd = os.getcwd(); d = tempfile.mkdtemp(); os.chdir(d)
    try:
        for k, v in (w.get('files') or {}).items():
            open(k, 'w').write(v)
        if w.get('files'):
            sys.path.insert(0, d)
            for mname in ('autograd', 'cnn_ops_l1'):
                sys.modules.pop(mname, None)
        ns = {'__learner_source__': src}
        try:
            exec((w.get('prelude') or '') + '\n', ns); exec(src, ns); exec((w.get('postlude') or '') + '\n', ns)
        except Exception:  # noqa
            return -1
        for i, t in enumerate(w['tests']):
            if not passes(t, ns):
                return i + 1
        return 0
    finally:
        os.chdir(cwd)
        if w.get('files'):
            sys.path.remove(d)


nw = nm = 0
with np.errstate(all='ignore'):
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
            for m in w.get('mutants', []):
                nm += 1
                got = first_fail(w, m['source'])
                lv.claim(got == m['test'], f'{lab} mutant "{m["symptom"][:40]}" first fails test {m["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')
lv.check_wrongs()
lv.report()
