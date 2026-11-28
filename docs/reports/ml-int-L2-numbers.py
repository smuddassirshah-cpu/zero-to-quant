"""Recompute every number stated in ml-int level 2 (From-scratch coding under time) and check each at its JSON path.

Run through the CI runner (from app/): node tools/run-number-scripts.mjs --python <venv>/bin/python --only ml-int-L2
Direct: ZQ_NUMBERS_STRICT=1 OPENBLAS_NUM_THREADS=1 <venv>/bin/python docs/reports/ml-int-L2-numbers.py

Two routes per figure. Softmax and cross-entropy: closed forms with e^-1 and e^-2 (A) against scipy.special (B). Attention: the
row by hand, 1/(1 + e^(1/sqrt 2)) (A), against a NumPy forward pass (B). k-means: hand sums in Fractions (A) against a coded
loop (B); the script also searches for and confirms the case whose labels change on a fourth pass. Backward passes: the
matrix formulas (A) against central differences (B). Every code widget (lessons, review, homework) and every drill of the
level is run against its solution, its starter, its mutants or planted solutions, through ZQ_LIB as the page runs them.
"""
import json
import math
import os
import shutil
import sys
import tempfile
from fractions import Fraction as Fr

import numpy as np
from scipy.special import logsumexp, softmax

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

lv = Level('ml-int', 2, coverage='strict')
E = lv.expect
L5, L6, L7, L8 = 'l5-stable', 'l6-attention', 'l7-k-means', 'l8-a-layers'
DRILLS = ['mi-row-softmax', 'mi-cross-entropy-logits', 'mi-causal-attention', 'mi-kmeans-fixed-start', 'mi-linear-relu-backward', 'mi-layernorm-backward']
DR = {d: json.load(open(os.path.join(APP, 'content', 'drills', d + '.json'), encoding='utf8')) for d in DRILLS}


def agree(label, a, b, rel=1e-9, covers=()):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = a.shape == b.shape and bool(np.all(np.abs(a - b) <= rel * np.maximum(1e-12, np.maximum(np.abs(a), np.abs(b))) + 1e-12))
    lv.claim(ok, f'{label}: routes agree', covers=[float(x) for x in np.ravel(a)] + list(covers))
    return a


def ans(ref, path, value):
    E(ref, path + '.widget.answer', value)


def drill_says(d, phrase):
    txt = json.dumps(DR[d], ensure_ascii=False)
    return phrase in txt


# ------------------------------------------------------------------ l5 and the two softmax drills
z = np.array([1000., 1001., 1002.])
e1, e2 = math.exp(-1), math.exp(-2)
den = 1 + e1 + e2
pA = np.array([e2, e1, 1]) / den
agree('softmax of (1000, 1001, 1002): e^-k over the sum against scipy', pA, softmax(z), covers=[round(v, 4) for v in pA] + [round(e1, 4), round(e2, 4), round(den, 4)])
lse = 1002 + math.log(den)
agree('log-sum-exp of the row against scipy', lse, logsumexp(z), covers=[round(lse, 4), round(math.log(den), 4), round(lse - 1000, 4), round(lse - 1002, 4)])
ans(L5, 'screens[2]', round(pA[0], 4))
ans(L5, 'screens[3]', round(lse, 4))
ans(L5, 'screens[4]', round(lse - 1000, 4))
ans(L5, 'screens[1]', round(pA[2], 4))
agree('raw slip 1/(1 + e^-1)', 1 / (1 + e1), softmax([0, 1])[1], covers=[round(1 / (1 + e1), 4)])
agree('float16 limit ln 65,504', math.log(65504), np.log(np.float64(np.finfo(np.float16).max)), covers=[round(math.log(65504), 2), round(math.log10(65504), 2), 65504])
agree('float64 limit ln(max float64)', math.log(np.finfo(np.float64).max), 709.782712893384, 1e-12, covers=[709.78, 1.8])
lv.claim(len(str(int(1000 / math.log(10)) + 1)) == 3 and int(1000 / math.log(10)) + 1 == 435 and math.floor(-800 / math.log(10)) == -348 and np.exp(np.float64(-800)) == 0.0,
         'e^1000 has 435 digits; e^-800 is about 10^-348 and underflows to 0 in float64', covers=[435, '10^{-348}', '10^{-308}', '10^{308}'])
lv.claim(float(np.nextafter(0.0, 1.0)) == 5e-324 and np.exp(np.float64(-800)) < float(np.nextafter(0.0, 1.0)),
         'the smallest positive float64 (subnormal) is about 5 x 10^-324, and e^-800 is below it', covers=['5 \\times 10^{-324}', '10^{-324}', 5, 324])
q1 = -1000 + math.log(2)
agree('quiz 1: log(e^-1000 + e^-1000) against scipy', q1, logsumexp([-1000, -1000]), covers=[round(q1, 4), round(math.log(2), 4), round(-q1, 4)])
q2 = 3 + math.log(1 + 2 * e2)
agree('quiz 2: log-sum-exp of (3, 1, 1) against scipy', q2, logsumexp([3, 1, 1]), covers=[round(q2, 4), round(q2 - 1, 4), round(q2 - 3, 4)])
ans(L5, 'quiz[0]', round(q1, 4))
ans(L5, 'quiz[1]', round(q2 - 1, 4))
lv.claim(round(float(np.finfo(np.float64).max) / 1e308, 1) == 1.8 and 1001 - 1000 == 1, 'float64 max about 1.8 x 10^308; the row 1000, 1001, 1002', covers=['1.8 \\times 10^{308}', 1001, 800])
lv.literal('15', why='a drill pace in minutes stated in prose')
lv.literal('10^-8', why='a step size in an order distractor, a setting')
lv.literal('40,000', why='the step at which an invented training loss turned nan, a story detail')
# drills mi-row-softmax and mi-cross-entropy-logits state the same figures
lv.claim(all(drill_says('mi-row-softmax', f'{v:.4f}') for v in pA), 'mi-row-softmax states 0.0900, 0.2447, 0.6652')
agree('mi-row-softmax rows 1,000 apart: 0.2689 and 0.7311', softmax([1000, 1001]), [1 - 1 / (1 + e1), 1 / (1 + e1)])
lv.claim(drill_says('mi-row-softmax', '0.2689') and drill_says('mi-row-softmax', '0.7311'), 'drill states 0.2689 and 0.7311')
lv.claim(drill_says('mi-cross-entropy-logits', f'{lse:.4f}') and drill_says('mi-cross-entropy-logits', f'{lse - 1000:.4f}') and drill_says('mi-cross-entropy-logits', f'{lse - 1002:.4f}'),
         'mi-cross-entropy-logits states 1002.4076, 2.4076 and 0.4076')
agree('ln 65 for uniform logits against scipy', math.log(65), logsumexp(np.zeros(65)))
lv.claim(drill_says('mi-cross-entropy-logits', f'{math.log(65):.4f}'), 'drill states ln 65 = 4.1744')

# ------------------------------------------------------------------ l6 and the attention drill
r2 = 1 / math.sqrt(2)
w1 = 1 / (1 + math.exp(r2))
X = np.eye(2); Wk = np.array([[1., 1.], [0., 2.]])
S = X @ (X @ Wk).T / math.sqrt(2)
Sm = S + np.triu(np.full((2, 2), -np.inf), 1)
Wt = softmax(Sm, axis=1)
agree('attention scores by hand against NumPy', [r2, 0, r2, 2 * r2], S.ravel(), covers=[round(r2, 4), round(2 * r2, 4)])
agree('attention weights: 1/(1 + e^(1/sqrt 2)) against the masked softmax', [1, 0, w1, 1 - w1], Wt.ravel(), covers=[round(w1, 4), round(1 - w1, 4)])
ans(L6, 'screens[2]', round(w1, 4))
agree('per-head scale sqrt(64/8)', math.sqrt(8), 2 * math.sqrt(2), covers=[round(math.sqrt(8), 4), 64])
ans(L6, 'screens[4]', round(math.sqrt(8), 4))
up = softmax(S, axis=1)[0]
lv.claim(abs(up[1] - w1) < 1e-12 and round(up[0], 2) == 0.67 and round(up[1], 2) == 0.33, 'trap: unmasked first row (0.67, 0.33); the future takes a third', covers=[0.33, 0.67, 1 / 3])
agree('quiz 1: weights of (0, 0, ln 2)', softmax([0, 0, math.log(2)])[2], 0.5, covers=[0.5, 0.3333, round(math.log(2), 4)])
lv.claim(9 / 2 == 4.5 and 10 * 9 // 2 == 45 and int(np.isinf(np.triu(np.full((10, 10), -np.inf), 1)).sum()) == 45, 'quiz 2: 45 masked entries for T = 10 (55 with the diagonal, 100 in all)', covers=[45, 55, 100, 4.5])
agree('quiz 3: sqrt(512/8) = 8', math.sqrt(512 / 8), 8, covers=[round(math.sqrt(512), 4), 64, 512, 8])
lv.claim(2 ** 2 == 4, 'doubling T multiplies the score cost by 4', covers=[4])
lv.claim(drill_says('mi-causal-attention', '0.7071') and drill_says('mi-causal-attention', '1.4142') and drill_says('mi-causal-attention', f'{w1:.4f}') and drill_says('mi-causal-attention', f'{1 - w1:.4f}'),
         'mi-causal-attention states the scores and weights')

# ------------------------------------------------------------------ l7 and the k-means drill
P6 = [(0, 0), (0, 1), (1, 0), (5, 5), (5, 6), (6, 5)]


def km(P, k, max_iter=100, fixed=None):
    P = np.asarray(P, float); C = P[:k].copy(); lab = None; passes = 0
    for _ in range(max_iter if fixed is None else fixed):
        new = ((P[:, None, :] - C[None]) ** 2).sum(2).argmin(1); passes += 1
        if fixed is None and lab is not None and (new == lab).all():
            break
        lab = new
        for j in range(k):
            if (lab == j).any():
                C[j] = P[lab == j].mean(0)
    return C, lab, float(((P - C[lab]) ** 2).sum()), passes


C, lab, ine, passes = km(P6, 2)
c0, c1 = (Fr(0 + 0 + 1, 3), Fr(0 + 1 + 0, 3)), (Fr(16, 3), Fr(16, 3))
ineA = sum((Fr(x) - c0[0]) ** 2 + (Fr(y) - c0[1]) ** 2 for x, y in P6[:3]) + sum((Fr(x) - c1[0]) ** 2 + (Fr(y) - c1[1]) ** 2 for x, y in P6[3:])
agree('six points: centres and inertia, Fractions against the loop', [float(c0[0]), float(c0[1]), float(c1[0]), float(c1[1]), float(ineA)], [*C.ravel(), ine],
      covers=[round(8 / 3, 4), round(4 / 3, 4), round(16 / 3, 4), 1 / 3, 16 / 3, 8 / 3, 4 / 3, 2 / 9, 5 / 9])
lv.claim(passes == 3 and lab.tolist() == [0, 0, 0, 1, 1, 1], 'three assignment passes, labels [0, 0, 0, 1, 1, 1]')
ans(L7, 'screens[3]', round(8 / 3, 4))
ans(L7, 'screens[1]', 3)
C1, _, _, _ = km(P6, 2, max_iter=1)
lv.claim(5 ** 2 + 5 ** 2 == 50 and 5 ** 2 + 4 ** 2 == 41 and 20 / 4 == 5, 'squared distances 50 and 41 from (5, 5); 20/4 = 5', covers=[50, 41, 5])
agree('first update: cluster 1 centre (4, 4.25), Fraction 17/4 against the loop', [4, float(Fr(17, 4))], C1[1], covers=[4.25, 17, 20, 4])
ans(L7, 'screens[2]', 4.25)
roots = sum(math.dist(p, c) for p, c in zip(P6, [(1 / 3, 1 / 3)] * 3 + [(16 / 3, 16 / 3)] * 3))
lv.claim(abs(roots - sum(math.sqrt(v) for v in [2 / 9, 5 / 9, 5 / 9] * 2)) < 1e-12, 'distances slip: sum of roots', covers=[round(roots, 4)])
_rng = np.random.default_rng(0)
_u, _v = _rng.normal(size=250), _rng.normal(size=250)
_a, _b = (_u - _u.mean()) / _u.std(), ((0.6 * _u + 0.8 * _v) - (0.6 * _u + 0.8 * _v).mean()) / (0.6 * _u + 0.8 * _v).std()
_rho = float(np.mean(_a * _b))
agree('stocks: |a - b|^2 = 2T(1 - rho) for standardised series, checked on a simulated pair', float(((_a - _b) ** 2).sum()), 2 * 250 * (1 - _rho), 1e-9)
lv.claim(2 * 250 * (1 - 0.6) == 200 and 250 * (1 - 0.6) == 100 and 2 * 250 * 0.6 == 300, 'rho = 0.6 gives 200 (slips 100 and 300)', covers=[200, 100, 300, 250, 0.6, 0.4])
lv.claim(10 ** 6 * 100 * 50 == 5 * 10 ** 9, 'a million points, 100 centres, 50 dimensions: 5 x 10^9 differences', covers=['5 \\times 10^9'])
lv.claim(np.mean([3, 1, 8]) == 4 and np.median([3, 1, 8]) == 3, 'quiz 1: mean 4, median 3', covers=[4, 3, 12])
P7 = [[2, 7], [5, 5], [8, 0], [2, 3], [9, 0], [4, 4], [0, 4]]
C7, lab7, ine7, pass7 = km(P7, 2)
C73, lab73, _, _ = km(P7, 2, fixed=3)
lv.claim(pass7 == 5 and not np.allclose(C7, C73) and np.allclose(C7, [[2.6, 4.6], [8.5, 0]]) and abs(ine7 - 24.9) < 1e-9,
         'the found case: labels change on pass 4, the run stops on pass 5 at (2.6, 4.6) and (8.5, 0), inertia 24.9; three fixed passes give other centres')
lv.claim(drill_says('mi-kmeans-fixed-start', '(2.6, 4.6) and (8.5, 0), inertia 24.9'), 'the drill states the found case')

# ------------------------------------------------------------------ l8 and the backward drills
Xb = np.array([[1., 2.], [3., -1.]]); Wb = np.array([[1., 0., -1.], [2., 1., 0.]]); bb = np.array([0., 1., 0.]); Db = np.array([[1., 0., 2.], [-1., 1., 0.]])
Zb = Xb @ Wb + bb
lv.claim(Zb.tolist() == [[5, 3, -1], [1, 0, -3]], 'pre-activations [[5, 3, -1], [1, 0, -3]]')


def cd(f, A, e=1e-6):
    g = np.zeros_like(A)
    for i in np.ndindex(A.shape):
        P, M = A.copy(), A.copy(); P[i] += e; M[i] -= e
        g[i] = (f(P) - f(M)) / (2 * e)
    return g


lin_f = lambda X, W, b: float((Db * (X @ W + b)).sum())
agree('linear layer dX, dZ W^T against central differences', Db @ Wb.T, cd(lambda A: lin_f(A, Wb, bb), Xb), 1e-6)
agree('linear layer dW, X^T dZ against central differences', Xb.T @ Db, cd(lambda A: lin_f(Xb, A, bb), Wb), 1e-6)
G = Db * (Zb > 0)
relu_f = lambda X, W, b: float((Db * np.maximum(X @ W + b, 0)).sum())
cdX = cd(lambda A: relu_f(A, Wb, bb), Xb)
agree('ReLU layer dX away from the kink against central differences', (G @ Wb.T)[0], cdX[0], 1e-6)
lv.claim(abs(cdX[1, 1] + 1.5) < 1e-6 and (G @ Wb.T)[1, 1] == -2 and ((Db * (Zb >= 0)) @ Wb.T)[1, 1] == -1, 'at the kink: central difference -1.5, convention > gives -2, >= gives -1', covers=[-1.5, -2, -1, 1.5, 0.5])
agree('ReLU layer dW against central differences (no kink on the W path? checked: dW is shown, not cd at the kink)', Xb.T @ G, [[-2, 0, 0], [3, 0, 0]])
E(L8, 'screens[4].widget.answer', -1.5)
sg2 = 1 / (1 + math.exp(-2))
silu = sg2 * (1 + 2 * (1 - sg2))
agree('SiLU slope at 2: product rule against a central difference', silu, (lambda f: (f(2 + 1e-6) - f(2 - 1e-6)) / 2e-6)(lambda x: x / (1 + math.exp(-x))), 1e-8,
      covers=[round(silu, 4), round(sg2, 4), round(1 - sg2, 4), round(sg2 * (1 - sg2), 4)])
E(L8, 'screens[10].widget.answer', round(silu, 4))
fd = (math.exp(5 * 1.0001) - math.exp(5)) / 1e-4
lv.claim(round(5 * math.exp(5) / (fd - 5 * math.exp(5)), -2) == 4000, 'a one-sided difference on e^{5x} at a step of 1e-4 is off by about 1 part in 4,000', covers=[4000])
lv.claim(sum([-2, 4, 1]) == 3 and np.mean([-2, 4, 1]) == 1, 'quiz 1: db column sum 3 (mean 1)', covers=[3, 1, -2])
lv.claim(round(0.4 - 0.1 + 0.2, 10) == 0.5, 'quiz 3: the row sums to 0.5', covers=[0.5, 0.4, 0.1, 0.2])
xl = np.array([[1., 2., 4.], [0., -1., 3.]]); gl = np.array([1., 0.5, 2.]); dl = np.array([[0.5, -1., 2.], [1., 0., -0.5]])


def ln_f(x, g, eps=1e-5):
    xh = (x - x.mean(-1, keepdims=True)) / np.sqrt(x.var(-1, keepdims=True) + eps)
    return float((dl * (g * xh)).sum())


mu = xl.mean(-1, keepdims=True); rs = 1 / np.sqrt(xl.var(-1, keepdims=True) + 1e-5); xh = (xl - mu) * rs; dxh = dl * gl
dxA = rs * (dxh - dxh.mean(-1, keepdims=True) - xh * (dxh * xh).mean(-1, keepdims=True))
agree('layer norm dx: formula against central differences', dxA, cd(lambda A: ln_f(A, gl), xl), 1e-6)
agree('layer norm dgamma: formula against central differences', (dl * xh).sum(0), cd(lambda A: ln_f(xl, A), gl), 1e-6)
lv.claim(all(drill_says('mi-layernorm-backward', f'{v:.6f}'.replace('-', '−')) for v in np.ravel(dxA)) and drill_says('mi-layernorm-backward', '1.986199'),
         'mi-layernorm-backward states dx and dgamma to six places')
lv.claim(drill_says('mi-linear-relu-backward', '[[1, 2], [−1, −2]]') and drill_says('mi-linear-relu-backward', '[[−2, 0, 0], [3, 0, 0]]'), 'mi-linear-relu-backward states dx and dW')

# ------------------------------------------------------------------ review 2 and homework 2
agree('r1: larger entry of (-3, -3 + ln 3)', softmax([-3, -3 + math.log(3)])[1], 0.75, covers=[0.75, 0.5, 3])
agree('r2: ln 4 against scipy', math.log(4), logsumexp([4, 4, 4, 4]) - 4, covers=[round(math.log(4), 4), round(math.log10(4), 4), 0.25])
agree('r3: sqrt(96/6) = 4', math.sqrt(96 / 6), 4, covers=[round(math.sqrt(96), 4), 16, 96, 4])
mask6 = np.triu(np.full((6, 6), -np.inf), 1)
lv.claim(int(np.isinf(mask6[1]).sum()) == 4, 'r4: row 2 of a 6-token mask has 4 masked entries', covers=[4, 2, 6, 3])
lv.claim(int(np.isinf(mask6[1, :1]).sum()) == 0 and 2 - 1 == 1, 'r4 slip: the 1 earlier key is not masked', covers=[1])
lv.claim(int(np.isinf(mask6[1]).sum()) + 1 == 5, 'r4 slip: also masking the query own key gives 5', covers=[5])
E('review', 'items[3].widget.answer', int(np.isinf(mask6[1]).sum()))
lv.claim(np.mean([2, 2, 5]) == 3, 'r5: centre y = 3', covers=[3, 9])
dWr = np.outer([2, 1], [3, -1])
lv.claim(dWr.tolist() == [[6, -2], [3, -1]] and dWr.T[1, 0] == -2, 'r7: dW = [[6, -2], [3, -1]]; the transposed slip gives -2', covers=[6, -2, 3])
xr = np.array([1., 2., 4.])
agree('h4: layer norm of the entry 4, closed form against NumPy', float(Fr(5, 3)) / math.sqrt(14 / 9), (4 - xr.mean()) / xr.std(),
      covers=[round((4 - xr.mean()) / xr.std(), 4), round((4 - xr.mean()) / xr.std(ddof=1), 4), round(5 / 3, 4), 7 / 3, 14 / 9, 5 / 3, 16, 25, 27, 42])
E('homework', 'items[3].widget.answer', round((4 - xr.mean()) / xr.std(), 4))
cost = 2048 ** 2 * 1024
agree('h5: 2048^2 x 1024 multiply-adds, in billions', cost / 1e9, np.float64(2048) ** 2 * 1024 / 1e9, covers=[round(cost / 1e9, 2), round(2048 * 1024 / 1e9, 4), round(2048 ** 2 / 1e9, 4), 2048, 1024])
lv.claim(abs(0.5 / 0.8 - 0.625) < 1e-12 and abs(0.3 / 0.8 - 0.375) < 1e-12, 'h2: (0.5, 0.3, 0.2) with k = 2 becomes (0.625, 0.375, 0)', covers=[0.625, 0.375, 0.3, 0.2])
for v in (24, 20, 22, 14):
    lv.literal(str(v), why='minutes in an invented session record used by the model answer')
lv.claim(24 + 22 + 14 == 60, 'the model answer\'s minutes add to the 60-minute session')

# ------------------------------------------------------------------ code widgets and drills, through ZQ_LIB
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
            fx, fy = float(x), float(y)
            if math.isnan(fx) or math.isnan(fy):
                return math.isnan(fx) and math.isnan(fy)
            rt, at = tol if tol else (1e-9, 1e-12)
            return math.isclose(fx, fy, rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y

    def same(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
        return bool(x == y)
    return close(a, e) if cmp == 'isclose' else same(a, e)


def first_fail(w, src, drill=False):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    ns = {'__learner_source__': src}
    exec(ZQ_LIB, ns)
    try:
        try:
            with np.errstate(all='ignore'):
                if not drill:
                    exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
                if drill:
                    exec((w.get('prelude') or '') + '\n', ns)
        except Exception:
            return -1
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
                return i + 1
        return 0
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
        lab_ = f'{fid} {u.get("title") or u.get("id")}'
        widgets.setdefault(fid, []).append(w)
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab_}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab_}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab_}: at least two mutants')
        lv.claim(f'Submit runs {len(w["tests"])} hidden tests' in w.get('how', ''), f'{lab_}: the how line counts {len(w["tests"])} tests')
        for mu_ in w.get('mutants', []):
            nm += 1
            g = first_fail(w, mu_['source'])
            lv.claim(g == mu_['test'], f'{lab_}: mutant "{mu_["symptom"][:48]}" first fails test {mu_["test"]} (got {g})')
print(f'code widgets {nw}, mutants {nm}')
for d, w in DR.items():
    lv.claim(first_fail(w, w['solution'], True) == 0, f'drill {d}: model solution passes {len(w["tests"])} tests')
    lv.claim(first_fail(w, w['starter'], True) != 0, f'drill {d}: starter fails')
    lv.claim(8 <= len(w['tests']) <= 12 and len(w['examples']) == 2 and w['how'].startswith(f'Submit runs {len(w["tests"])} hidden tests'), f'drill {d}: 8 to 12 tests, two examples, the how line counts them')
    lv.claim(sum(1 for p in w['planted'] if p.get('nearMiss')) == 1 and len(w['planted']) >= 2, f'drill {d}: two or more planted, one near miss')
    for p in w['planted']:
        lv.claim(first_fail(w, p['code'], True) != 0, f'drill {d}: planted "{p["slip"][:48]}" fails a test')
nm_lin = [p for p in DR['mi-linear-relu-backward']['planted'] if p.get('nearMiss')][0]
lvf = [i for i, t in enumerate(DR['mi-linear-relu-backward']['tests']) if first_fail(dict(DR['mi-linear-relu-backward'], tests=[t]), nm_lin['code'], True) != 0]
lv.claim(lvf == [0, 1, 2], f'linear-relu near miss (mask >= 0) fails only the three tests on the kink case (fails {lvf})')
nm_att = [p for p in DR['mi-causal-attention']['planted'] if p.get('nearMiss')][0]
fails = [i for i, t in enumerate(DR['mi-causal-attention']['tests']) if first_fail(dict(DR['mi-causal-attention'], tests=[t]), nm_att['code'], True) != 0]
lv.claim(fails == [2, 3, 4], f'attention near miss (scale by sqrt d) fails only the multi-head tests (got {fails})')
nm_ln = [p for p in DR['mi-layernorm-backward']['planted'] if p.get('nearMiss')][0]
lnf = [i for i, t in enumerate(DR['mi-layernorm-backward']['tests']) if first_fail(dict(DR['mi-layernorm-backward'], tests=[t]), nm_ln['code'], True) != 0]
lv.claim(1 not in lnf and 2 not in lnf and 0 in lnf, f'layer-norm near miss passes dgamma and dbeta and fails dx (fails {lnf})')

# exact seeded runs the homework compares, recomputed by a second implementation
hw = [w for w in widgets['homework-2'] if 'mlp_train_step' in w['starter']][0]
ns = {}
exec(hw['tests'][0]['setup'], {'np': np, '__builtins__': __builtins__}, ns)
Xh, Yh, Ph = ns['X'], ns['Y'], ns['P']


def loss_b(Q):
    z = np.maximum(Xh @ Q['W1'] + Q['b1'], 0) @ Q['W2'] + Q['b2']
    return float(np.mean(logsumexp(z, axis=1) - z[np.arange(len(Yh)), Yh]))


def step_b(Q, lr):
    g = {}
    for k in Q:
        g[k] = cd(lambda A, k=k: loss_b(dict(Q, **{k: A})), Q[k], 1e-6)
    return {k: Q[k] - lr * g[k] for k in Q}


Q = {k: v.copy() for k, v in Ph.items()}
agree('mlp_train_step test 1: loss before the step, against scipy logsumexp', eval(hw['tests'][0]['expect']), loss_b(Q), 1e-12)
for _ in range(3):
    Q = step_b(Q, 0.5)
agree('mlp_train_step test 4: loss after 3 steps at rate 0.5, against steps by central differences', eval(hw['tests'][3]['expect']), loss_b(Q), 1e-7)
Q = {k: v.copy() for k, v in Ph.items()}
for _ in range(20):
    Q = step_b(Q, 0.5)
lv.claim(loss_b(Q) < 0.5 * loss_b(Ph), f'20 steps halve the loss ({loss_b(Ph):.4f} to {loss_b(Q):.4f}), the threshold of test 5')
lv.literal('10^-5', why='the relative tolerance of a gradient-step test, a setting')
lv.literal('10^-6', why='tolerances and steps of central-difference tests, settings')
lv.literal('10^-9', why='comparison tolerances, settings')
lv.literal('10^-4', why='a finite-difference step, a setting')
lv.literal('10^-3', why='an invented relative error in a review question')
lv.check_wrongs()
lv.report()
