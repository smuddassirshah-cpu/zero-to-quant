"""Recompute every number stated in makemore level 2 (A network with embeddings) and check each value at its JSON path.

Run: <venv>/bin/python docs/reports/makemore-L2-numbers.py   (NumPy and the standard library; about a minute; exits 0 when every check passes)
     add --write to rewrite app/content/data/ai/makemore-mlp.json from a fresh 40,000-step run (weights rounded to 6 places).

Route A: NumPy with the gradients written by hand (index lookups, np.add.at). Route B: the shipped autograd.py for short runs,
and a row-by-row loop for every loss computed from the supplied weights. The supplied weights file is the source of every
stated MLP loss; a fresh 40,000-step run must agree with it to 1e-3 (BLAS sums may differ between machines).
Every code widget is run: solution passes, starter fails, each mutant first fails the test it names (ENGINE-BACKLOG 1263).
"""
import hashlib
import itertools
import json
import math
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

DATA = os.path.join(ROOT, 'app', 'content', 'data', 'ai')
CANON = open(os.path.join(DATA, 'autograd.py'), encoding='utf8').read()
sys.path.insert(0, DATA)
from autograd import Tensor, cross_entropy, sgd_step  # noqa: E402

lv = Level('makemore', 2)
E = lv.expect
F = lambda ref: lv._file(ref)[1]  # noqa: E731


def two(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol * max(1.0, abs(a)), f'{label}: routes agree ({a!r} vs {b!r})')
    return a


W = open(os.path.join(DATA, 'names.txt')).read().splitlines()
SYM = '.abcdefghijklmnopqrstuvwxyz'; IX = {c: i for i, c in enumerate(SYM)}
perm = np.random.default_rng(42).permutation(len(W))
tr = [W[i] for i in perm[:25626]]; dv = [W[i] for i in perm[25626:28829]]; te = [W[i] for i in perm[28829:]]


def build(ws, block=3):
    X, Y = [], []
    for w in ws:
        ctx = [0] * block
        for ch in w + '.':
            X.append(ctx); Y.append(IX[ch]); ctx = ctx[1:] + [IX[ch]]
    return np.array(X), np.array(Y)


def build_B(ws, block=3):   # route B: slide over the padded string
    X, Y = [], []
    for w in ws:
        s = '.' * block + w + '.'
        for i in range(block, len(s)):
            X.append([IX[c] for c in s[i - block:i]]); Y.append(IX[s[i]])
    return np.array(X), np.array(Y)


Xtr, Ytr = build(tr); Xdv, Ydv = build(dv); Xte, Yte = build(te)
XtrB, YtrB = build_B(tr)
lv.claim(np.array_equal(Xtr, XtrB) and np.array_equal(Ytr, YtrB), 'dataset: two builders agree')
lv.claim((len(Xtr), len(Xdv), len(Xte)) == (182531, 22807, 22808), 'rows 182,531, 22,807, 22,808')


def init(seed, emb=10, hid=100, block=3):
    g = np.random.default_rng(seed)
    return {'C': g.standard_normal((27, emb)), 'W1': g.standard_normal((block * emb, hid)) * (5 / 3) / math.sqrt(block * emb),
            'b1': np.zeros(hid), 'W2': g.standard_normal((hid, 27)) * 0.01, 'b2': np.zeros(27)}


def loss(P, X, Y):
    Em = P['C'][X].reshape(len(X), -1); h = np.tanh(Em @ P['W1'] + P['b1']); z = h @ P['W2'] + P['b2']
    m = z.max(1, keepdims=True)
    return float((np.log(np.exp(z - m).sum(1)) + m[:, 0] - z[np.arange(len(Y)), Y]).mean())


def loss_rows(P, X, Y):   # route B: one row at a time
    s = 0.0
    for x, y in zip(X, Y):
        e = np.concatenate([P['C'][i] for i in x]); hh = np.tanh(e @ P['W1'] + P['b1']); z = hh @ P['W2'] + P['b2']
        s += math.log(sum(math.exp(v - z.max()) for v in z)) + z.max() - z[y]
    return s / len(Y)


def step(P, X, Y, lr):
    Em = P['C'][X].reshape(len(X), -1); h = np.tanh(Em @ P['W1'] + P['b1']); z = h @ P['W2'] + P['b2']
    p = np.exp(z - z.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); bl = float(-np.log(p[np.arange(len(Y)), Y]).mean())
    p[np.arange(len(Y)), Y] -= 1; dz = p / len(Y)
    dW2 = h.T @ dz; db2 = dz.sum(0); dpre = (dz @ P['W2'].T) * (1 - h ** 2); dW1 = Em.T @ dpre; db1 = dpre.sum(0)
    dE = (dpre @ P['W1'].T).reshape(X.shape[0], X.shape[1], -1); dC = np.zeros_like(P['C']); np.add.at(dC, X, dE)
    for k, gr in (('C', dC), ('W1', dW1), ('b1', db1), ('W2', dW2), ('b2', db2)):
        P[k] -= lr * gr
    return bl


def autograd_run(P0, X, Y, steps, lr, seed):
    P = {k: Tensor(v.copy()) for k, v in P0.items()}; g = np.random.default_rng(seed); out = []
    for _ in range(steps):
        ix = g.integers(0, len(X), 32)
        z = (P['C'][X[ix]].reshape(32, -1) @ P['W1'] + P['b1']).tanh() @ P['W2'] + P['b2']
        L = cross_entropy(z, Y[ix])
        for t in P.values():
            t.zero_grad()
        L.backward(); sgd_step(list(P.values()), lr); out.append(L.item())
    return {k: t.data for k, t in P.items()}, out


# ---------------- the 40,000-step run and the weights file ----------------
P = init(0)
lv.claim(sum(v.size for v in P.values()) == 6097 == 27 * 10 + 30 * 100 + 100 + 100 * 27 + 27, '6,097 parameters')
init_dev = loss(P, Xdv, Ydv); lv.claim(round(init_dev, 4) == 3.301, 'initial dev loss 3.3010')
g = np.random.default_rng(1); marks = {}; curve = []; batch = []
for k in range(1, 40001):
    ix = g.integers(0, len(Xtr), 32); bl = step(P, Xtr[ix], Ytr[ix], 0.1 if k <= 30000 else 0.01)
    if k <= 200:
        batch.append(bl)
    if k % 500 == 0 or k in (200, 1000, 3000):
        tl, dl = loss(P, Xtr, Ytr), loss(P, Xdv, Ydv)
        if k % 500 == 0:
            curve.append((k, tl, dl))
        marks[k] = (tl, dl)
wpath = os.path.join(DATA, 'makemore-mlp.json')
if '--write' in sys.argv:
    R0 = {k: np.round(v, 6) for k, v in P.items()}
    doc = {'about': 'makemore level 2 MLP: context 3, embedding 10, hidden 100 (tanh), 27 outputs; trained 40,000 minibatch steps by docs/reports/makemore-L2-numbers.py; weights rounded to 6 places.'}
    doc.update({k: R0[k].tolist() for k in ('C', 'W1', 'b1', 'W2', 'b2')})
    open(wpath, 'w').write(json.dumps(doc, separators=(',', ':')))
raw = open(wpath).read()
lv.claim(len(raw.encode()) < 256 * 1024, f'weights file under 256 KB ({len(raw)} bytes)')
R = {k: np.array(v) for k, v in json.loads(raw).items() if k != 'about'}
lv.claim({k: v.shape for k, v in R.items()} == {k: v.shape for k, v in P.items()}, 'weights file shapes')
lv.claim(max(float(np.abs(R[k] - P[k]).max()) for k in R) < 1e-3, 'fresh run agrees with the weights file to 1e-3')
rl = {nm: loss(R, X, Y) for nm, (X, Y) in (('train', (Xtr, Ytr)), ('dev', (Xdv, Ydv)), ('test', (Xte, Yte)))}
two('dev loss of the supplied weights, vectorised and row by row', rl['dev'], loss_rows(R, Xdv, Ydv), 1e-9)
lv.claim([round(rl[k], 4) for k in ('train', 'dev', 'test')] == [2.1356, 2.1609, 2.1742], 'supplied weights: train 2.1356, dev 2.1609, test 2.1742')
want = {200: (2.5816, 2.5876), 1000: (2.4201, 2.4249), 3000: (2.3128, 2.3209), 10000: (2.2411, 2.2488), 20000: (2.2117, 2.2353), 30000: (2.1972, 2.2198), 40000: (2.1356, 2.1609)}
lv.claim(all(abs(marks[k][0] - a) < 6e-5 and abs(marks[k][1] - b) < 6e-5 for k, (a, b) in want.items()), 'recorded (train, dev) marks of the brief')
ser = F('l8-minibatches-and-rates')['screens'][1]['canvas']['params']
lv.claim(len(ser['series'][0]['values']) == 80 and all(abs(a - c[1]) < 1e-3 and abs(b - c[2]) < 1e-3 for a, b, c in zip(ser['series'][0]['values'], ser['series'][1]['values'], curve)), 'plotted curve matches the run')
lv.claim(ser['xValues'][59] == 30000 and ser['vlines'][0]['i'] == 59, 'step-drop line at 30,000')
D = round(rl['dev'], 4)

# ---------------- l5 ----------------
L5 = 'l5-three-letters-of-context'
from collections import Counter  # noqa: E402
m, em = Counter(), Counter()
for w in W:
    s = '..' + w + '.'
    for i in range(2, len(s) - 1):
        if s[i] == 'm':
            m[s[i + 1]] += 1
            if s[i - 1] == 'e':
                em[s[i + 1]] += 1
lv.claim(sum(m.values()) == 6642 and sum(em.values()) == 769 and em.most_common(1)[0] == ('i', 160) and m['a'] == 2590 and em['a'] == 140 and em['.'] == 128 and em['m'] == 100, 'after m and after em counts')
hv = F(L5)['screens'][0]['canvas']['state']['values']
lv.claim(all(abs(hv['em'][k] - em['.' if k == 'end' else k] / 769) < 5e-5 and abs(hv['m'][k] - m['.' if k == 'end' else k] / 6642) < 5e-5 for k in hv['em']), 'hook bars')
E(L5, 'screens[1].widget.answer', len(build(['emma'])[0]))
lv.claim(build(['emma'])[0].tolist()[3] == [5, 13, 13] and build(['emma'])[1].tolist()[3] == 1, 'emm row (5, 13, 13) then 1')
lv.claim(sum(map(len, tr)) == 156905, '156,905 training letters'); E(L5, 'screens[3].widget.answer', 156905 + 25626)
E(L5, 'screens[3].widget.wrong[1].value', 156905 + 25626 + 2 * 25626)
ctxs = len(set(map(tuple, Xtr.tolist()))); lv.claim(ctxs == 5440 and 27 ** 3 == 19683, '5,440 contexts seen of 19,683')
E(L5, 'screens[4].widget.answer', round((19683 - ctxs) / 19683, 2)); E(L5, 'screens[4].widget.wrong[0].value', round(ctxs / 19683, 2))
lv.claim(len(build(['jo'])[0]) == 3 and all(0 in r for r in build(['jo'])[0].tolist()), 'jo: 3 rows, each with a start mark')
lv.claim(len(build(['ava'])[0]) == 4 and 27 ** 4 == 531441, 'ava 4 rows; 531,441 cells')
X1, Y1 = build(tr, 1); lv.claim(len(X1) == 182531, 'block 1 gives the 182,531 bigram pairs')

# ---------------- l6 ----------------
L6 = 'l6-letters-as-points'
E(L6, 'screens[0].widget.answer', round(math.sqrt(2), 4))


def run2d(seed):
    Q = init(seed, emb=2); gg = np.random.default_rng(1)
    for _ in range(20000):
        ix = gg.integers(0, len(Xtr), 32); step(Q, Xtr[ix], Ytr[ix], 0.1)
    return Q


for run, seed, cap in ((0, 0, 'dev loss 2.32'), (1, 3, 'dev loss 2.33')):
    Q = run2d(seed); fr = F(L6)['screens'][1]['canvas']['controls'][0]['frames'][run]
    shown = np.array([[fr['points'][f'p{i}']['x'], fr['points'][f'p{i}']['y']] for i in range(27)])
    lv.claim(np.abs(shown - Q['C']).max() < 0.05, f'2D run {run + 1}: plotted points match a fresh run')
    lv.claim(cap in fr['caption'] and round(loss(Q, Xdv, Ydv), 2) == float(cap.split()[-1]), f'2D run {run + 1}: {cap}')
    V = [IX[c] for c in 'aeiou']; K = [i for i in range(1, 27) if i not in V]
    md = lambda A: np.mean([np.linalg.norm(shown[i] - shown[j]) for i, j in itertools.combinations(A, 2)])  # noqa: E731
    lv.claim(md(V) < 0.75 * md(K), f'2D run {run + 1}: vowels sit closer together ({md(V):.2f}) than consonants ({md(K):.2f})')
    lv.claim((round(md(V), 1), round(md(K), 1)) == ((1.1, 1.8), (1.2, 2.1))[run], f'2D run {run + 1}: mean distances stated on l6 s1, vowels about {md(V):.1f} apart, consonants {md(K):.1f}')
_A, _B = [np.array([[F(L6)['screens'][1]['canvas']['controls'][0]['frames'][r]['points'][f'p{i}'][a] for a in 'xy'] for i in range(27)]) for r in (0, 1)]
_A, _B = _A - _A.mean(0), _B - _B.mean(0)
_u, _s, _vt = np.linalg.svd(_B.T @ _A)
_res = np.linalg.norm(_B @ (_u @ _vt) - _A) / np.linalg.norm(_A)
lv.claim(_res > 0.9, f'the two 2D runs are not a turn and a flip of each other: best rotation or reflection leaves {_res:.2f} of the spread')
TC = np.array([[0.5, -1.0], [2.0, 0.3], [-0.4, 1.1], [1.0, 1.0]])
E(L6, 'screens[2].widget.answer', TC[[2, 0, 2]].reshape(-1)[2])
dC = np.zeros(3); np.add.at(dC, [1, 2, 1], [0.5, -0.2, 0.3]); dC2 = np.zeros(3); dC2[[1, 2, 1]] += [0.5, -0.2, 0.3]
E(L6, 'screens[4].widget.answer', round(dC[1], 4)); lv.claim(round(dC2[1], 4) == 0.3, 'fancy += keeps one copy: 0.3')
zc = sum('z' in ''.join(SYM[i] for i in r) for r in Xtr.tolist()); lv.claim(round(len(Xtr) / zc) == 35 and round((1 - zc / len(Xtr)) ** 32, 1) == 0.4, 'z in 1 context in 35; 4 batches in 10 without')
E(L6, 'screens[7].widget.answer', 270); E(L6, 'screens[9].widget.answer', 500 * 8)
E(L6, 'quiz[2].widget.answer', round(0.1 + 0.2 - 0.05 + 0.3 + 0.15, 4))

# ---------------- l7 ----------------
L7 = 'l7-the-mlp-model'
lv.claim(round(531441 / 6097) == 87, 'one weight per 87 table cells')
T = {'C': np.array([[0.0], [1.0], [-1.0]]), 'W1': np.array([[0.5, -1.0], [1.0, 0.5]]), 'b1': np.array([0.0, 0.1]), 'W2': np.array([[1.0, -1.0, 0.0], [0.5, 0.0, 2.0]]), 'b2': np.array([0.0, 0.0, 0.2])}
hA = np.tanh(np.array([1.0, -1.0]) @ T['W1'] + T['b1']); hB = [math.tanh(1 * 0.5 - 1 * 1.0 + 0.0), math.tanh(1 * -1.0 - 1 * 0.5 + 0.1)]
lv.claim(np.allclose(hA, hB), 'planted hidden values, two ways')
E(L7, 'screens[3].widget.answer', round(hA[0], 4)); E(L7, 'screens[4].widget.answer', round(float((hA @ T['W2'] + T['b2'])[1]), 4))
E(L7, 'screens[3].widget.wrong[2].value', round(math.tanh(1.5), 4))
z0 = (np.tanh(R['C'][[0, 0, 0]].reshape(-1) @ R['W1'] + R['b1']) @ R['W2'] + R['b2']); p0 = np.exp(z0 - z0.max()); p0 /= p0.sum()
fv = F(L7)['screens'][7]['canvas']['state']['values']; lv.claim(all(abs(fv[c] - p0[IX[c]]) < 5e-5 for c in fv) and list(fv) == [SYM[i] for i in np.argsort(-p0)[:5]], 'first-letter bars from the supplied weights')
E(L7, 'screens[7].question', round(sum(w[0] == 'a' for w in tr) / len(tr), 4))
E(L7, 'screens[8].widget.answer', round((2.4514 - D) / math.log(2), 4)); E(L7, 'screens[8].feedback.correct', round(math.exp(D), 2))
E(L7, 'quiz[0].widget.answer', 27 * 8 + 32 * 64 + 64 + 64 * 27 + 27); E(L7, 'screens[11].widget.answer', 11 * 4 + 3 * 2)

# ---------------- l8 ----------------
L8 = 'l8-minibatches-and-rates'
E(L8, 'screens[0].widget.answer', round(182531 / 32)); E(L8, 'screens[2].widget.answer', round(40000 * 32 / 182531, 2))
sweep = {}
for lr in (0.001, 0.01, 0.1, 0.3, 1.0, 5.0):
    Q = init(0); gg = np.random.default_rng(1); bls = []
    with np.errstate(all='ignore'):
        for _ in range(1000):
            ix = gg.integers(0, len(Xtr), 32); bls.append(step(Q, Xtr[ix], Ytr[ix], lr))
        sweep[lr] = (loss(Q, Xdv, Ydv), bls)
lv.claim([round(sweep[k][0], 4) for k in (0.001, 0.01, 0.1, 0.3, 1.0)] == [3.0666, 2.6407, 2.4249, 2.419, 2.4529], 'sweep 3.0666, 2.6407, 2.4249, 2.4190, 2.4529')
_, b5 = autograd_run(init(0), Xtr, Ytr, 3, 5.0, 1)
lv.claim(np.allclose(b5, sweep[5.0][1][:3], atol=1e-6) and [round(x, 2) for x in b5] == [3.28, 7.93, 7.93], 'step 5: first losses 3.28, 7.93, 7.93, two ways')
# the step-5 run diverges, so its exact value depends on BLAS summation order (31.89 single-thread, 44.33 multi-thread): check a threshold only
lv.claim(sweep[5.0][0] > 30 and sweep[5.0][0] > 10 * sweep[0.1][0], f'step 5 diverges: dev after 1,000 steps above 30 and far above the step-0.1 run ({sweep[5.0][0]:.1f} here, order-sensitive)')
E(L8, 'screens[5].widget.answer', round(2.2198 - 2.1609, 4))
lv.claim([round(x, 4) for x in batch[-5:]] == [2.6831, 2.5913, 2.3616, 2.5334, 2.2918], 'batch losses at steps 196 to 200')
Pa, la = autograd_run(init(0), Xtr, Ytr, 200, 0.1, 1)
lv.claim(np.allclose(la, batch, atol=1e-9), '200 steps: autograd and hand gradient give the same batch losses')
lv.claim(round(loss(Pa, Xtr, Ytr), 4) == 2.5816 and np.mean(la[:20]) - np.mean(la[-20:]) > 0.3, '200 autograd steps: train 2.5816, batch losses fall more than 0.3')
seeds = {}
for bs in (1, 2, 3, 4, 5):
    Q = init(0); gg = np.random.default_rng(bs)
    for _ in range(1000):
        ix = gg.integers(0, len(Xtr), 32); step(Q, Xtr[ix], Ytr[ix], 0.1)
    seeds[bs] = round(loss(Q, Xdv, Ydv), 4)
lv.claim(seeds[1] == 2.4249 and seeds[2] == 2.416 and min(seeds.values()) == 2.416 and max(seeds.values()) == 2.4321, f'five batch seeds: {seeds}')
E(L8, 'quiz[1].widget.answer', round(182531 / 64)); E(L8, 'screens[9].widget.answer', 2500 // 250)

# ---------------- review-2 ----------------
E('review', 'items[0].widget.answer', len(build(['isabella'])[0]))
lv.claim(build(['olivia'])[0].tolist()[3] == [15, 12, 9] and build(['olivia'])[1].tolist()[3] == IX['v'] and build(['olivia'])[0].tolist()[2] == [0, 15, 12], 'olivia: (15, 12, 9) predicts v; (0, 15, 12) predicts the first i')
E('review', 'items[3].widget.answer', 27 * 5 + 10 * 50 + 50 + 50 * 27 + 27)
dr = np.zeros(8); np.add.at(dr, [4, 7, 4], [0.6, 0.1, -0.25]); E('review', 'items[5].widget.answer', round(dr[4], 4))
E('review', 'items[6].widget.answer', round(182531 / 128))

# ---------------- homework-2 ----------------
X4, Y4 = build(tr, 4); X4B, Y4B = build_B(tr, 4); lv.claim(np.array_equal(X4, X4B) and X4.shape == (182531, 4), 'block 4 dataset, two ways')
P4 = init(0, block=4); l40 = loss(P4, X4, Y4); P4a, _ = autograd_run(P4, X4, Y4, 200, 0.1, 1)
g4 = np.random.default_rng(1); P4b = init(0, block=4)
for _ in range(200):
    ix = g4.integers(0, len(X4), 32); step(P4b, X4[ix], Y4[ix], 0.1)
two('block 4 after 200 steps', loss(P4a, X4, Y4), loss(P4b, X4, Y4), 1e-9)
lv.claim(round(l40, 4) == 3.2937 and round(loss(P4b, X4, Y4), 4) == 2.5619, 'block 4: 3.2937 then 2.5619')
X12, Y12 = build(tr[:12], 4); P12 = init(0, block=4); g12 = np.random.default_rng(1)
for _ in range(5):
    ix = g12.integers(0, len(X12), 32); step(P12, X12[ix], Y12[ix], 0.1)
P12a, _ = autograd_run(init(0, block=4), X12, Y12, 5, 0.1, 1)
two('block 4, 5 steps on 12 names, hand and autograd', loss(P12, X12, Y12), loss(P12a, X12, Y12), 1e-10)
E('homework', 'items[0].widget.tests[6].expect', round(loss(P12, X12, Y12), 6))
E('homework', 'items[0].explain.text', 3.2937); E('homework', 'items[0].explain.text', 2.5619)
npar = lambda k, d, H: 27 * d + k * d * H + H + H * 27 + 27  # noqa: E731
rows = F('homework-2')['items'][1]['widget']['rows']
lv.claim([r[3]['answer'] for r in rows] == [npar(3, 10, 100), npar(3, 2, 100), npar(5, 16, 200)] == [6097, 3481, 22059], 'three sizes 6,097, 3,481, 22,059')
dh = np.zeros(8); np.add.at(dh, [2, 2, 5, 5, 1, 2], [0.2, -0.1, 0.4, 0.3, 0.05, -0.15]); E('homework', 'items[4].widget.answer', round(dh[2], 4))
E('homework', 'items[3].widget.answer', round(math.exp(D), 2))
mdl = F('homework-2')['items'][5]['model']
for v in (round(2.4514 - D, 4), round((2.4514 - D) / math.log(2), 4), round(math.exp(D), 2)):
    E('homework', 'items[5].model', v)
lv.claim(abs(7 * (2.4514 - D) / math.log(2) - 2.93) < 0.01 and round(2 ** 2.93, 1) == 7.6, 'a 7-symbol name: 2.93 bits, 7.6 times likelier')
lv.claim(abs(sum(map(len, W)) / len(W) - 6.1222) < 1e-4, 'mean name length 6.1222 (about 6 letters)')
lv.claim(sum(r['points'] for r in F('homework-2')['items'][5]['rubric']) == 10, 'longform rubric sums to 10')

# ---------------- problems-2 ----------------
E('problems', 'items[0].parts[1].widget.answer', 4 * 2 + 4 * 3 + 3 + 3 * 4 + 4); E('problems', 'items[0].parts[1].widget.wrong[0].value', 4 * 2 + 2 * 3 + 3 + 3 * 4 + 4); E('problems', 'items[0].parts[1].widget.wrong[1].value', 4 * 2 + 4 * 3 + 3 * 4)
e = np.array([-1.0, 0.5, 1.0, -1.0]); pre = float(e @ np.array([0.4, -0.3, 1.0, 0.2])) + 0.1
two('toy hidden unit', pre, -0.4 - 0.15 + 1.0 - 0.2 + 0.1, 1e-12); E('problems', 'items[0].parts[2].widget.answer', round(math.tanh(pre), 4))
zt = np.array([0.3, -0.2, 1.1, 0.0]); pt = np.exp(zt) / np.exp(zt).sum(); E('problems', 'items[0].parts[3].widget.answer', round(-math.log(pt[2]), 4))
E('problems', 'items[1].parts[0].widget.answer', 12000 // 40); E('problems', 'items[1].parts[1].widget.answer', 4500 // 300)
E('problems', 'items[1].parts[3].widget.answer', round(2.31 - 2.24, 2))
dp = np.zeros(10); np.add.at(dp, [3, 6, 3], [0.5, 0.2, -0.1]); E('problems', 'items[2].parts[0].widget.answer', round(dp[3], 4))
E('problems', 'items[2].parts[1].widget.answer', round(0.8 - 0.5 * dp[3], 4))

# ---------------- autograd shipped byte for byte ----------------
sha = hashlib.sha256(CANON.encode('utf8')).hexdigest()
lv.claim(sha.startswith('5917d4ec91f7'), 'canonical autograd.py is v1.0 (5917d4ec91f7)')
shipped = []


def find(node):
    if isinstance(node, dict):
        if isinstance(node.get('files'), dict) and 'autograd.py' in node['files']:
            shipped.append(node['files']['autograd.py'])
        for v in node.values():
            find(v)
    elif isinstance(node, list):
        for v in node:
            find(v)


for doc in lv.files.values():
    find(doc)
lv.claim(len(shipped) >= 1 and all(hashlib.sha256(s.encode('utf8')).hexdigest() == sha for s in shipped), f'every shipped autograd.py ({len(shipped)}) is byte-identical')


# ---------------- every code widget: solution, starter, mutants ----------------
def passes(t, ns):
    try:
        if t.get('setup'):
            exec(t['setup'], ns)
        got = eval(t['call'], ns)
    except Exception as e:  # noqa
        return t.get('compare') == 'raises' and type(e).__name__ == t['expect']
    try:
        want = eval(t['expect'], ns)
        if t.get('compare') == 'isclose':
            return bool(np.allclose(got, want, rtol=1e-9, atol=1e-12))
        return bool(got == want)
    except Exception:  # noqa
        return False


def first_fail(w, src):
    cwd = os.getcwd(); d = tempfile.mkdtemp(); os.chdir(d)
    try:
        for k, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(ROOT, 'app', v), os.path.join(d, k))
        for k, v in (w.get('files') or {}).items():
            open(k, 'w').write(v)
        sys.path.insert(0, d); sys.modules.pop('autograd', None)
        ns = {'__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec((w.get('prelude') or '') + '\n', ns); exec(src, ns); exec((w.get('postlude') or '') + '\n', ns)
        except Exception:  # noqa
            return -1
        with np.errstate(all='ignore'):
            for i, t in enumerate(w['tests']):
                if not passes(t, ns):
                    return i + 1
        return 0
    finally:
        os.chdir(cwd); sys.path.remove(d)


nw = nm = 0
for fid, doc in lv.files.items():
    units = doc.get('screens', []) + doc.get('items', [])
    for u in units:
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
            lv.claim(got == m['test'], f'{lab} mutant "{m["symptom"][:50]}" first fails test {m["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')
lv.check_wrongs()
lv.report()
