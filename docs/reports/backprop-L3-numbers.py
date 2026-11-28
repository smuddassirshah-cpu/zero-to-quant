"""Recompute every number stated in backprop level 3 (Neurons, layers and training) and check it at its JSON path.

Run: <venv>/bin/python docs/reports/backprop-L3-numbers.py   (NumPy and the standard library; exits 0 when every check passes)

Route 1 is the level's own scalar classes, taken from the JSON (the l10 code screen's prelude and solution, the
l11 `train` solution, the l12 `check_gradients` solution). Route 2 is independent: a NumPy network with hand-written
matrix gradients started from the same 13 draws of random.Random(42).uniform(-1, 1), and central differences of a
plain-float loss. The script reruns the 200-step training and asserts every loss the lessons quote.
"""
import math
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("backprop", 3)
E = lv.expect


def D(ref):
    return lv._file(ref)[1]


def two(label, a, b, tol=1e-6):
    lv.claim(math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), f'{label}: routes agree ({a!r} vs {b!r})')


def cd(f, args, i, h=1e-6):
    up = list(args); dn = list(args); up[i] += h; dn[i] -= h
    return (f(*up) - f(*dn)) / (2 * h)


th = math.tanh
X4 = [[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]]; Y4 = [1.0, 1.0, -1.0, -1.0]
X6 = [[2.0, 0.5], [-2.0, -0.5], [0.5, 2.0], [-0.5, -2.0], [1.5, -0.5], [-0.5, 1.5]]; Y6 = [1.0, 1.0, -1.0, -1.0, 1.0, -1.0]

# ---------- route 1: the level's classes from the JSON ----------
w10 = D('l10')['screens'][7]['widget']
NS = {}
exec(w10['prelude'] + '\n' + w10['solution'], NS)
exec(D('l11')['screens'][7]['widget']['solution'], NS)
exec(D('l12')['screens'][8]['widget']['prelude'].split('class Value')[0], NS)   # nothing but imports before the class
exec('def total_loss(model, X, Y):\n    return sum(((model(x) - y) ** 2 for x, y in zip(X, Y)), Value(0.0))\n', NS)
exec(D('l12')['screens'][8]['widget']['solution'], NS)
V, MLP, train, check = NS['Value'], NS['MLP'], NS['train'], NS['check_gradients']

# ---------- route 2: NumPy with hand gradients ----------
def raw(sizes, seed):
    r = random.Random(seed); out = []
    for m, k in zip(sizes, sizes[1:]):
        Wl = np.zeros((k, m)); bl = np.zeros(k)
        for j in range(k):
            for i in range(m):
                Wl[j, i] = r.uniform(-1, 1)
            bl[j] = r.uniform(-1, 1)
        out.append((Wl, bl))
    return out


def np_run(sizes, seed, X, Y, steps, lr, zero=True):
    P = [(W.copy(), b.copy()) for W, b in raw(sizes, seed)]
    Xa, Ya = np.array(X), np.array(Y); losses = []; acc = [(np.zeros_like(W), np.zeros_like(b)) for W, b in P]
    for k in range(steps + 1):
        acts = [Xa]
        for W, b in P:
            acts.append(np.tanh(acts[-1] @ W.T + b))
        out = acts[-1][:, 0]; losses.append(float(((out - Ya) ** 2).sum()))
        if k == steps:
            break
        d = (2 * (out - Ya))[:, None]; grads = [None] * len(P)
        for l in range(len(P) - 1, -1, -1):
            dz = d * (1 - acts[l + 1] ** 2); grads[l] = (dz.T @ acts[l], dz.sum(0)); d = dz @ P[l][0]
        if not zero:
            acc = [(aw + gw, ab + gb) for (aw, ab), (gw, gb) in zip(acc, grads)]; grads = acc
        P = [(W - lr * gw, b - lr * gb) for (W, b), (gw, gb) in zip(P, grads)]
    return losses, P


def np_grads(sizes, seed, X, Y):
    P = raw(sizes, seed); Xa, Ya = np.array(X), np.array(Y); acts = [Xa]
    for W, b in P:
        acts.append(np.tanh(acts[-1] @ W.T + b))
    out = acts[-1][:, 0]; d = (2 * (out - Ya))[:, None]; g = [None] * len(P)
    for l in range(len(P) - 1, -1, -1):
        dz = d * (1 - acts[l + 1] ** 2); g[l] = (dz.T @ acts[l], dz.sum(0)); d = dz @ P[l][0]
    flat = []
    for (gw, gb) in g:
        for j in range(gw.shape[0]):
            flat += list(gw[j]) + [gb[j]]
    return flat, acts


# ---------- l9: the neuron ----------
o_ = lambda w1, w2, b, x1, x2: th(w1 * x1 + w2 * x2 + b)
A = (0.5, 0.25, 0.3, 1.0, -2.0)
o = o_(*A); s = 1 - o * o
rule = [s * 1.0, s * -2.0, s, s * 0.5, s * 0.25]
for i, name in enumerate(['w1', 'w2', 'b', 'x1', 'x2']):
    two(f'l9 do/d{name}', rule[i], cd(o_, A, i))
lv.claim(round(o, 6) == 0.291313 and round(s, 6) == 0.915137 and round(rule[1], 6) == -1.830274 and round(rule[3], 6) == 0.457568 and round(rule[4], 6) == 0.228784, 'l9 neuron figures to 6 places')
E('l9', 'screens[3].widget.rows[3][1].answer', -1.8303); E('l9', 'screens[4].explain.text', 0.457568); E('l9', 'screens[4].explain.text', 0.228784)
E('l9', 'screens[5].widget.wrong[0].value', 1 - 0.3 ** 2)
two('l9 saturated slope at 5', 1 - th(5) ** 2, cd(th, (5.0,), 0)); E('l9', 'screens[6].widget.answer', round(1 - th(5) ** 2, 6))
two('l9 slope at 3', 1 - th(3) ** 2, cd(th, (3.0,), 0)); E('l9', 'screens[8].widget.answer', round(1 - th(3) ** 2, 4))
lv.claim(round((1 - th(0.3) ** 2) / (1 - th(3) ** 2)) in (92, 93), 'l9 transfer: "about 90 times smaller" (ratio 92.8)')
E('l9', 'quiz[0].widget.answer', 1 - 0.36); two('l9 quiz slope at 4', 1 - th(4) ** 2, 0.0013, 0.0001); two('l9 quiz slope at 0.1', 1 - th(0.1) ** 2, 0.990, 0.0005)
for t in D('l9')['screens'][7]['widget']['tests']:
    n = {}; exec(D('l9')['screens'][7]['widget']['solution'], n); exec(t.get('setup', ''), n)
    got = eval(t['call'], n); exp = eval(t['expect'])
    lv.claim(got == exp if t['compare'] == 'equal' else np.allclose(np.atleast_1d(got), np.atleast_1d(exp), rtol=1e-12), f'l9 tanh test {t["call"][:30]}')

# ---------- l10: layers and the network ----------
draws = random.Random(42); first13 = [draws.uniform(-1, 1) for _ in range(13)]
m = MLP(2, [3, 1], seed=42)
lv.claim([p.data for p in m.parameters()] == first13, 'l10 the 13 parameters are the first 13 draws in order')
lv.claim([round(v, 3) for v in first13[:3]] == [0.279, -0.95, -0.45], 'l10 first three draws to 3 places')
count = lambda sizes: sum((a + 1) * b for a, b in zip(sizes, sizes[1:]))
for sizes, n in (([2, 3, 1], 13), ([3, 4, 4, 1], 41), ([2, 16, 16, 1], 337), ([5, 8, 8, 1], 129), ([4, 2, 1], 13)):
    lv.claim(count(sizes) == n == len(MLP(sizes[0], sizes[1:]).parameters()), f'l10 count {sizes} = {n}')
_, acts = np_grads([2, 3, 1], 42, [[1.0, 1.0]], [1.0])
hid = [v.data for v in m.layers[0]([1.0, 1.0])]
two('l10 output at (1, 1)', m([1.0, 1.0]).data, acts[-1][0, 0], 1e-12)
for j in range(3):
    two(f'l10 hidden {j + 1} at (1, 1)', hid[j], acts[1][0, j], 1e-12)
E('l10', 'screens[1].widget.answer', round(acts[-1][0, 0], 4)); E('l10', 'screens[1].explain.text', round(hid[0], 4)); E('l10', 'screens[1].explain.text', round(hid[1], 4))
one_v = train(MLP(2, [1], seed=42), X4, Y4, 200, 0.05); one_n, _ = np_run([2, 1], 42, X4, Y4, 200, 0.05)
two('l10 one neuron after 200 steps', one_v[-1], one_n[-1], 1e-9); lv.claim(abs(one_v[-1] - 4) < 0.005, f'l10 one neuron settles at 4 ({one_v[-1]:.4f})')
E('l10', 'screens[6].prose', round(one_v[0], 4))
for t in w10['tests']:
    n = {}; exec(w10['prelude'] + '\n' + w10['solution'], n); exec(t.get('setup', ''), n)
    got = eval(t['call'], n); exp = eval(t['expect'])
    lv.claim(got == exp if t['compare'] == 'equal' else math.isclose(got, exp, rel_tol=1e-12), f'l10 classes test {t["call"][:40]}')

# ---------- l11: training ----------
Lv = train(MLP(2, [3, 1], seed=42), X4, Y4, 200, 0.05); Ln, _ = np_run([2, 3, 1], 42, X4, Y4, 200, 0.05)
for k, want in ((0, 5.556800), (1, 4.955816), (10, 1.588956), (50, 0.153664), (100, 0.059298), (200, 0.025020)):
    two(f'l11 loss at step {k}', Lv[k], Ln[k], 1e-9); lv.claim(round(Lv[k], 6) == want, f'l11 loss at step {k} is {want}')
E('l11', 'screens[3].prose', 1.5890); E('l11', 'screens[3].prose', 0.1537); E('l11', 'screens[3].prose', round(Lv[200], 4))
first01 = next(i for i, v in enumerate(Lv) if v < 0.1); lv.claim(first01 == 68, f'l11 first step below 0.1 is {first01}'); E('l11', 'screens[3].widget.answer', first01)
for lr, k10, k50 in ((0.2, 0.1756, 0.0241), (0.5, 3.3716, 4.0001), (2.0, 8.0, 8.0)):
    a = train(MLP(2, [3, 1], seed=42), X4, Y4, 50, lr); b, _ = np_run([2, 3, 1], 42, X4, Y4, 50, lr)
    two(f'l11 lr {lr} step 50', a[50], b[50], 1e-6); lv.claim(round(a[10], 4) == k10 and round(a[50], 4) == k50, f'l11 lr {lr}: {k10} after 10, {k50} after 50')
g_flat, _ = np_grads([2, 3, 1], 42, X4, Y4)
m0 = MLP(2, [3, 1], seed=42); L0 = sum(((m0(x) - y) ** 2 for x, y in zip(X4, Y4)), V(0.0)); L0.backward()
bo, go = m0.parameters()[-1].data, m0.parameters()[-1].grad
two('l11 output bias gradient', go, g_flat[-1], 1e-12)
lv.claim(max(abs(p.grad - g) for p, g in zip(m0.parameters(), g_flat)) < 1e-12, 'l11 step-0 gradients: Value and NumPy agree to 1e-12')
E('l11', 'screens[0].widget.answer', round(bo - 0.05 * go, 4)); E('l11', 'screens[0].prose', round(bo, 6)); E('l11', 'screens[0].prose', round(go, 6))
E('l11', 'screens[0].widget.wrong[0].value', round(bo + 0.05 * go, 4))
# no reset
mnz = MLP(2, [3, 1], seed=42); nz = []
for k in range(201):
    loss = sum(((mnz(x) - y) ** 2 for x, y in zip(X4, Y4)), V(0.0)); nz.append(loss.data)
    if k == 200:
        break
    loss.backward()
    for p in mnz.parameters():
        p.data -= 0.05 * p.grad
nzn, Pn = np_run([2, 3, 1], 42, X4, Y4, 200, 0.05, zero=False)
two('l11 no reset, step 10', nz[10], nzn[10], 1e-9); lv.claim(round(nz[50], 4) == 0.0, 'l11 no reset reads 0.0000 by step 50')
nzmax = max(abs(p.data) for p in mnz.parameters()); two('l11 no reset largest parameter (NumPy run)', nzmax, max(max(float(np.abs(W).max()), float(np.abs(b).max())) for W, b in Pn), 1e-6)
lv.claim(round(nzmax) == 74, f'l11 no reset largest parameter {nzmax:.1f}'); E('l11', 'screens[5].prose', 74)
mok = MLP(2, [3, 1], seed=42); train(mok, X4, Y4, 200, 0.05); okmax = max(abs(p.data) for p in mok.parameters())
lv.claim(round(okmax, 1) == 2.2, f'l11 correct run largest parameter {okmax:.2f}'); E('l11', 'screens[5].prose', 2.2)
for seed in (3, 6):
    msd = MLP(2, [3, 1], seed=seed); out = []
    for k in range(201):
        loss = sum(((msd(x) - y) ** 2 for x, y in zip(X4, Y4)), V(0.0)); out.append(loss.data)
        if k == 200:
            break
        loss.backward()
        for p in msd.parameters():
            p.data -= 0.05 * p.grad
    lv.claim(1.95 < out[-1] < 2.1, f'l11 trap: with no reset, seed {seed} sticks near 2 ({out[-1]:.3f})')
outs = [mok(x).data for x in X4]
lv.claim(all((o > 0) == (y > 0) for o, y in zip(outs, Y4)), 'l11 trained network right in sign at all four points')
for v in outs:
    E('l11', 'screens[6].prose', round(v, 4))
for t in D('l11')['screens'][7]['widget']['tests']:
    w = D('l11')['screens'][7]['widget']; n = {}; exec(w['prelude'] + '\n' + w['solution'] + '\n' + w['postlude'], n)
    lv.claim(repr(eval(t['call'], n)) == t['expect'], f'l11 train test {t["call"][:40]}')
E('l11', 'quiz[0].widget.answer', 0.4 - 0.1 * 2)

# ---------- l12: checking ----------
d05 = 1 - th(0.5) ** 2
two('l12 central at 0.1', (th(0.6) - th(0.4)) / 0.2, 0.7855, 0.00005); E('l12', 'screens[1].widget.answer', round((th(0.6) - th(0.4)) / 0.2, 4))
E('l12', 'screens[1].widget.wrong[0].value', round((th(0.6) - th(0.5)) / 0.1, 4)); E('l12', 'screens[1].prose', round(d05, 4))
table = {0.1: (3.71e-2, 9.45e-4), 0.01: (3.64e-3, 9.42e-6), 1e-3: (3.64e-4, 9.42e-8), 1e-4: (3.63e-5, 9.42e-10), 1e-5: (3.63e-6, 1.54e-11), 1e-6: (3.63e-7, 5.40e-11), 1e-8: (3.80e-9, 3.80e-9), 1e-10: (1.59e-7, 4.37e-7)}
for h, (fe, ce) in table.items():
    f_ = abs((th(0.5 + h) - th(0.5)) / h - d05); c_ = abs((th(0.5 + h) - th(0.5 - h)) / (2 * h) - d05)
    lv.claim(float(f'{f_:.2e}') == fe and float(f'{c_:.2e}') == ce, f'l12 error table at h = {h:g}: {f_:.2e}, {c_:.2e}')
t5 = th(0.5); f3 = -2 * (1 - t5 ** 2) * (1 - 3 * t5 ** 2)
two('l12 central error matches |f\'\'\'| h^2 / 6 at h = 0.01', abs(f3) * 1e-4 / 6, 9.42e-6, 0.005)
f2 = -2 * t5 * (1 - t5 ** 2); two('l12 forward error about |f\'\'| h / 2 at h = 0.01', abs(f2) * 0.01 / 2, 0.0036, 0.05)
E('l12', 'screens[6].prose', round((th(0.51) - th(0.5)) / 0.01, 4)); E('l12', 'screens[6].prose', round(d05, 4))
lv.claim(round(abs((th(0.51) - th(0.5)) / 0.01 - d05) / d05, 4) == 0.0046, 'l12 trap: forward relative error 4.6e-3')
E('l12', 'screens[4].widget.answer', round(0.002 / 2.002, 4))
for h, want in ((1e-2, 1.6e-3), (1e-4, 1.6e-7), (1e-6, 2.8e-8)):
    c = check(MLP(2, [3, 1], seed=42), X4, Y4, h)
    gnum = []
    flat = [p.data for p in MLP(2, [3, 1], seed=42).parameters()]

    def loss_at(vals):
        it = iter(vals); ws = [[([next(it) for _ in range(2)], next(it)) for _ in range(3)], [([next(it) for _ in range(3)], next(it))]]
        tot = 0.0
        for x, y in zip(X4, Y4):
            a = x
            for layer in ws:
                a = [th(sum(wi * ai for wi, ai in zip(w, a)) + b) for w, b in layer]
            tot += (a[0] - y) ** 2
        return tot
    for i in range(13):
        up = list(flat); dn = list(flat); up[i] += h; dn[i] -= h; gnum.append((loss_at(up) - loss_at(dn)) / (2 * h))
    rel = max(abs(a - b) / max(abs(a), abs(b), 1e-12) for a, b in zip(g_flat, gnum))
    two(f'l12 course check at h = {h:g}: Value class vs NumPy and plain floats', c, rel, 1e-3)
    lv.claim(float(f'{c:.1e}') == want, f'l12 course check at h = {h:g} is {c:.1e}')
w12 = D('l12')['screens'][8]['widget']; n12 = {}; exec(w12['prelude'] + '\n' + w12['solution'] + '\n' + w12['postlude'], n12)
planted = n12['planted'](); lv.claim(planted > 1e-2, f'l12 planted bug fails at {planted:.2f}'); E('l12', 'screens[8].canvas', round(planted, 2))
for t in w12['tests']:
    exec(t.get('setup', ''), n12)
    lv.claim(repr(eval(t['call'], n12)) == t['expect'], f'l12 check test {t["call"][:40]}')
two('l12 kink', (max(0, 0.001) - max(0, -0.001)) / 0.002, 0.5, 1e-12)
Ncdf = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
d1 = (math.log(1) + (0.05 + 0.02) * 1) / 0.2; d2 = d1 - 0.2
C = lambda S_: S_ * Ncdf((math.log(S_ / 100) + 0.07) / 0.2) - 100 * math.exp(-0.05) * Ncdf((math.log(S_ / 100) + 0.03) / 0.2)
two('l12 transfer: bumped delta equals N(d1)', (C(100.01) - C(99.99)) / 0.02, Ncdf(d1), 1e-6)
lv.claim(round(Ncdf(d1), 4) == 0.6368 and round(Ncdf(d2), 4) == 0.5596, 'l12 transfer: N(d1) = 0.6368, N(d2) = 0.5596')
E('l12', 'screens[9].widget.answer', round((Ncdf(d1) - Ncdf(d2)) / Ncdf(d1), 2)); E('l12', 'screens[9].widget.wrong[1].value', round((Ncdf(d1) - Ncdf(d2)) / Ncdf(d2), 2))
two('l12 quiz cube', (1.1 ** 3 - 0.9 ** 3) / 0.2, 3.01, 1e-9)

# ---------- review-3 ----------
E('review', 'items[0].widget.answer', 1 - 0.64)
two('review do/dw', (1 - th(0.5) ** 2) * -0.5, cd(lambda w: th(w * -0.5 + 1.5), (2.0,), 0)); E('review', 'items[1].widget.answer', -0.3932)
lv.claim(count([3, 5, 2]) == 32, 'review 3-5-2 has 32'); E('review', 'items[3].widget.answer', 0.7 - 0.25 * 1.2)
lv.claim(len(MLP(3, [2, 1], seed=0).layers[0].parameters()) + 1 == 9, 'review: the output\'s first weight is draw 9')
two('review central of x^2', (3.5 ** 2 - 2.5 ** 2) / 1, 6, 1e-12); E('review', 'items[7].widget.answer', round(0.0005 / 0.5, 4))
two('review quarter', 9.42e-6 / 4, 2.4e-6, 0.02)

# ---------- homework-3 ----------
for i in (0, 1, 5):
    w = D('homework')['items'][i]['widget']; n = {}
    exec(w.get('prelude', '') + '\n' + w['solution'] + '\n' + w.get('postlude', ''), n)
    for t in w['tests']:
        got = eval(t['call'], n); exp = eval(t['expect'])
        lv.claim(got == exp if t['compare'] == 'equal' else np.allclose(np.atleast_1d(got), np.atleast_1d(exp), rtol=1e-12), f'homework item {i + 1} test {t["call"][:40]}')
for seed in (42, 7):
    a = train(MLP(2, [4, 1], seed=seed), X6, Y6, 200, 0.05); b, _ = np_run([2, 4, 1], seed, X6, Y6, 200, 0.05)
    two(f'hw 2-4-1 on six points, seed {seed}', a[-1], b[-1], 1e-9); lv.claim(a[-1] < 0.02, f'hw seed {seed}: 2-4-1 below 0.02 ({a[-1]:.4f}), threshold 0.05 has a margin')
    c = train(MLP(2, [1], seed=seed), X6, Y6, 400, 0.05); lv.claim(c[-1] > 4, f'hw seed {seed}: one neuron above 4 ({c[-1]:.4f})')
mf = MLP(2, [2, 1])
for p, v in zip(mf.parameters(), [0.5, -0.25, 0.1, 0.3, 0.8, -0.2, 1.0, -1.5, 0.05]):
    p.data = v
h1 = th(0.5 - 0.5 + 0.1); h2 = th(0.3 + 1.6 - 0.2); two('hw fixed forward', mf([1.0, 2.0]).data, th(1.0 * h1 - 1.5 * h2 + 0.05), 1e-12)
lv.claim(check(MLP(2, [4, 1], seed=5), X6, Y6, 1e-6) < 1e-6, 'hw perf: the 2-4-1 seed 5 check passes')
E('homework', 'items[4].widget.answer', (0.01 / 0.002) ** 2)

# ---------- problems-3 ----------
L1 = lambda w: sum((th(w * x) - y) ** 2 for x, y in ((1, 1), (-1, -1)))
g1 = cd(L1, (0.5,), 0); E('problems', 'items[0].parts[2].widget.answer', round(g1, 4)); E('problems', 'items[0].parts[1].widget.answer', round(L1(0.5), 4))
E('problems', 'items[0].parts[3].widget.answer', round(0.5 - 0.1 * g1, 4)); E('problems', 'items[0].parts[4].widget.answer', round(L1(0.5 - 0.1 * g1), 4))
L2 = lambda w, b: sum((th(w * x + b) - y) ** 2 for x, y in ((2, 1), (0, -1)))
gb = cd(L2, (1.0, -0.5), 1); E('problems', 'items[1].parts[1].widget.answer', round(gb, 4)); E('problems', 'items[1].parts[0].widget.answer', round(L2(1, -0.5), 4))
E('problems', 'items[1].parts[3].widget.answer', round(L2(1, -0.5 - 0.2 * gb), 4))
f3_ = lambda w: (th(2 * w) - 0.5) ** 2
g3 = 2 * (th(0.6) - 0.5) * (1 - th(0.6) ** 2) * 2; two('problems 3 backprop vs central', g3, cd(f3_, (0.3,), 0))
c3 = (f3_(0.31) - f3_(0.29)) / 0.02; E('problems', 'items[2].parts[2].widget.answer', round(c3, 4))
E('problems', 'items[2].parts[3].widget.answer', round(abs(g3 - c3) / g3, 4))
fw3 = (f3_(0.31) - f3_(0.3)) / 0.01; E('problems', 'items[2].parts[4].widget.answer', round(abs(fw3 - g3) / max(fw3, g3), 2))
lv.claim(30 < (abs(fw3 - g3) / max(fw3, g3)) / (abs(g3 - c3) / g3) < 45, 'problems 3: forward error "about 40 times" the central one')


# ---------- fix pass ----------
# l11 and homework-3: the step-10 loss pins the zeroing of the gradients
NOZ = ("        for p in model.parameters():\n            p.grad = 0.0\n        loss.backward()", "        loss.backward()")
w11 = D('l11')['screens'][7]['widget']
lv.claim(w11['tests'][7]['call'] == 'abs(losses_200()[10] - 1.588956) < 1e-5' and w11['mutants'][0]['test'] == 8, 'l11 test 8 pins the step-10 loss at 1.588956')
two('l11 step-10 loss, Value class vs NumPy', Lv[10], np_run([2, 3, 1], 42, X4, Y4, 200, 0.05)[0][10], 1e-9)
lv.claim(round(Lv[10], 6) == 1.588956 and round(nz[10], 6) == 0.358497, 'l11 step-10 loss is 1.588956 with the reset and 0.358497 without')
two('l11 no-reset step-10 loss, Value class vs NumPy', nz[10], nzn[10], 1e-9)
n11 = {}; exec(w11['prelude'] + '\n' + w11['mutants'][0]['source'] + '\n' + w11['postlude'], n11)
res = [repr(eval(t['call'], n11)) == t['expect'] for t in w11['tests']]
lv.claim(res[:7] == [True] * 7 and res[7] is False, f'l11 train() without the reset passes tests 1 to 7 and fails test 8 ({res})')
n11 = {}; exec(w11['prelude'] + '\n' + w11['starter'] + '\n' + w11['postlude'], n11)
try:
    ok11 = repr(eval(w11['tests'][7]['call'], n11)) == 'True'
except Exception:
    ok11 = False
lv.claim(not ok11, 'l11 starter fails the step-10 test')
w3h = D('homework')['items'][5]['widget']
lv.claim(w3h['tests'][6]['call'].endswith('[10] - 1.693188) < 1e-5') and w3h['mutants'][0]['test'] == 7, 'homework-3 test 7 pins the step-10 loss at 1.693188')
a3, _ = np_run([2, 4, 1], 42, X6, Y6, 10, 0.05); b3, _ = np_run([2, 4, 1], 42, X6, Y6, 10, 0.05, zero=False)
lv.claim(round(a3[10], 6) == 1.693188 and round(b3[10], 4) == 0.0786, f'homework-3 step-10 loss is {a3[10]:.6f} with the reset, {b3[10]:.4f} without (NumPy)')
n3h = {}; exec(w3h['prelude'] + '\n' + w3h['mutants'][0]['source'] + '\n' + w3h['postlude'], n3h)
res = [repr(eval(t['call'], n3h)) == t['expect'] if t['compare'] == 'equal' else None for t in w3h['tests']]
lv.claim(all(r is True for r in res[:6] if r is not None) and res[6] is False, f'homework-3 train() without the reset passes tests 1 to 6 and fails test 7 ({res})')
# l11 s6: seeds 1 to 7 without the reset, five reach zero and two stick near 2
reach = []
for seed in range(1, 8):
    msd = MLP(2, [3, 1], seed=seed)
    for k in range(201):
        loss = sum(((msd(x) - y) ** 2 for x, y in zip(X4, Y4)), V(0.0))
        if k == 200:
            break
        loss.backward()
        for p in msd.parameters():
            p.data -= 0.05 * p.grad
    reach.append(loss.data)
lv.claim(sorted(i + 1 for i, v in enumerate(reach) if v > 1.9) == [3, 6] and sum(v < 0.03 for v in reach) == 5, f'l11 seeds 1 to 7 without the reset: two stick near 2 (3 and 6), five reach 0 ({[round(v, 3) for v in reach]})')
# l12 screen 0: the 1 - n^2 closure on the course network (real gradients and real training at 0.05)
w12b = D('l12')['screens'][8]['widget']
bug_src = (w12b['prelude'] + '\n' + w12b['solution']).replace('self.grad += (1 - t * t) * out.grad', 'self.grad += (1 - self.data ** 2) * out.grad')
lv.claim(bug_src != (w12b['prelude'] + '\n' + w12b['solution']), 'l12 s0: the bug source differs from the correct one')
nb = {}; exec(bug_src, nb); exec(D('l11')['screens'][7]['widget']['solution'], nb)
mb = nb['MLP'](2, [3, 1], seed=42); lb = nb['total_loss'](mb, nb['X4'], nb['Y4']); lb.backward()
gb5 = [round(p.grad, 3) for p in mb.parameters()][:5]
cons = D('l12')['screens'][0]['canvas']['params']['lines']
lv.claim(cons[2] == str(gb5), f'l12 s0 console gradients are the real 1 - n^2 gradients {gb5}')
# route 2: NumPy with the wrong derivative 1 - n^2 (n is the pre-activation)
def np_bug(sizes, seed, X, Y, steps, lr):
    P = [(W.copy(), b.copy()) for W, b in raw(sizes, seed)]
    Xa, Ya = np.array(X), np.array(Y); losses = []; g0 = None
    for k in range(steps + 1):
        acts = [Xa]; pre = []
        for W, b in P:
            z = acts[-1] @ W.T + b; pre.append(z); acts.append(np.tanh(z))
        out = acts[-1][:, 0]; losses.append(float(((out - Ya) ** 2).sum()))
        if k == steps:
            break
        d = (2 * (out - Ya))[:, None]; grads = [None] * len(P)
        for l in range(len(P) - 1, -1, -1):
            dz = d * (1 - pre[l] ** 2); grads[l] = (dz.T @ acts[l], dz.sum(0)); d = dz @ P[l][0]
        if g0 is None:
            g0 = [float(v) for v in np.concatenate([np.concatenate([grads[0][0][j], [grads[0][1][j]]]) for j in range(3)] + [np.concatenate([grads[1][0][0], [grads[1][1][0]]])])]
        P = [(W - lr * gw, b - lr * gb) for (W, b), (gw, gb) in zip(P, grads)]
    return losses, g0
lnp, g0 = np_bug([2, 3, 1], 42, X4, Y4, 3, 0.05)
two('l12 s0 buggy gradients, Value class vs NumPy', [p.grad for p in mb.parameters()][0], g0[0], 1e-9)
lv.claim([round(v, 3) for v in g0[:5]] == gb5, f'l12 s0 NumPy buggy gradients agree {gb5}')
lbug = nb['train'](nb['MLP'](2, [3, 1], seed=42), nb['X4'], nb['Y4'], 3, 0.05)
lv.claim(cons[4] == str([round(v, 3) for v in lbug]) and [round(v, 3) for v in lnp] == [round(v, 3) for v in lbug], f'l12 s0 console losses {[round(v, 3) for v in lbug]} (Value class and NumPy agree)')
lv.claim(lbug[1] < lbug[0] and lbug[2] < lbug[1] and lbug[3] > lbug[2] and round(lbug[3], 3) == 9.954, 'l12 s0: the loss falls for two steps then jumps to 9.954')
mg = MLP(2, [3, 1], seed=42); lg = sum(((mg(x) - y) ** 2 for x, y in zip(X4, Y4)), V(0.0)); lg.backward()
lv.claim(sum((a_ > 0) != (b_ > 0) for a_, b_ in zip(gb5, [p.grad for p in mg.parameters()][:5])) == 2, 'l12 s0 sign option: two of the first five buggy signs are wrong')
# l12 screen 9 (check_gradients): a second call on a used model; the no-zeroing version gives 0.5
w12c = D('l12')['screens'][8]['widget']
lv.claim(w12c['tests'][6]['setup'].startswith('m = MLP(2, [3, 1], seed=42)') and w12c['mutants'][0]['test'] == 7, 'l12 check_gradients test 7 reuses a model')
n12m = {}; exec(w12c['prelude'] + '\n' + w12c['mutants'][0]['source'] + '\n' + w12c['postlude'], n12m)
res = []
for t in w12c['tests']:
    exec(t.get('setup', ''), n12m); res.append(repr(eval(t['call'], n12m)) == t['expect'])
lv.claim(res[:6] == [True] * 6 and res[6] is False, f'l12 check_gradients without zeroing passes tests 1 to 6, fails test 7 ({res})')
mm = n12m['MLP'](2, [3, 1], seed=42); n12m['check_gradients'](mm, n12m['X4'], n12m['Y4'], 1e-6)
two('l12 no-zeroing check on a used model reports 0.5', n12m['check_gradients'](mm, n12m['X4'], n12m['Y4'], 1e-6), 0.5, 1e-6)
# l12 option whys
two('l12 course network check at h = 0.1 is 0.14', n12['check_gradients'](n12['MLP'](2, [3, 1], seed=42), n12['X4'], n12['Y4'], 0.1), 0.14, 5e-3)
lv.claim(n12['check_gradients'](n12['MLP'](2, [3, 1], seed=42), n12['X4'], n12['Y4'], 1e-5) < 1e-6, 'l12 central check on the course network at h = 1e-5 passes 1e-6')
E('l9', 'screens[6].feedback.correct', round(1 - math.tanh(5) ** 2, 6)); E('l9', 'screens[6].feedback.correct', 0.92)
two('l9 s7: 1 - tanh^2 0.3 is about 0.92', 1 - math.tanh(0.3) ** 2, 0.915137, 1e-6)

lv.check_wrongs()
lv.report()
