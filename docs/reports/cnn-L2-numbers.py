"""Recompute every number stated in cnn level 2 (Stride, padding and pooling) and check each at its JSON path.

Run: <venv>/bin/python docs/reports/cnn-L2-numbers.py   (NumPy only; exits 0 when every check passes)

Route A is the lesson generators (closed forms, reshapes, im2col). Route B, here, is independent: sizes by listing every
window start, parameter counts by building the weight arrays, multiply-adds by counting terms in explicit loops, pooling by
loops over windows, col2im counts by stamping windows. The shipped cnn_ops_l2.py (conv2d, maxpool2d, avgpool2d, im2col,
col2im) is checked against loops and by central differences to 1e-6 in float64 by two routes. Every code widget is run:
model passes, starter fails, each mutant first fails the test it names (ENGINE-BACKLOG 1263).
"""
import hashlib
import itertools
import math
import os
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

AI = os.path.join(ROOT, 'app', 'content', 'data', 'ai')
sys.path.insert(0, AI)
from autograd import Tensor, grad_check  # noqa: E402
import cnn_ops_l2 as ops  # noqa: E402

lv = Level('cnn', 2)
E = lv.expect
CANON = open(os.path.join(AI, 'autograd.py'), encoding='utf8').read()
lv.claim(hashlib.sha256(CANON.encode()).hexdigest().startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
lv.claim(ops.__version__ == '1.0' and 'from autograd import Tensor' in open(os.path.join(AI, 'cnn_ops_l2.py')).read(), 'cnn_ops_l2.py v1.0 imports the frozen autograd')


def starts(n, k, p, s):
    """Route B: list every start of a window that fits in the padded side."""
    return [c for c in range(0, n + 2 * p) if c % s == 0 and c + k <= n + 2 * p]


def osz(n, k, p, s):
    return len(starts(n, k, p, s))


def conv_loop(x, W, b, s, p):
    x = np.pad(np.asarray(x, float), ((0, 0), (p, p), (p, p)))
    f, c, k, _ = W.shape
    rs, cs = starts(x.shape[1] - 2 * p, k, p, s), starts(x.shape[2] - 2 * p, k, p, s)
    return np.array([[[sum(W[o, ch, a, bb] * x[ch, r + a, q + bb] for ch in range(c) for a in range(k) for bb in range(k)) + b[o] for q in cs] for r in rs] for o in range(f)])


def central(f, A, h=1e-5):
    g = np.zeros_like(A)
    for i in np.ndindex(A.shape):
        keep = A[i]; A[i] = keep + h; up = f(); A[i] = keep - h; down = f(); A[i] = keep
        g[i] = (up - down) / (2 * h)
    return g


def relerr(a, b):
    return np.abs(a - b).max() / max(np.abs(a).max(), np.abs(b).max(), 1e-12)


def params(layer):
    """Route B: build the arrays and count their entries."""
    if layer[0] == 'conv':
        _, ci, co, k = layer
        return np.zeros((co, ci, k, k)).size + np.zeros(co).size
    if layer[0] == 'dense':
        _, ni, no = layer
        return np.zeros((ni, no)).size + np.zeros(no).size
    return 0


def macs(n, ci, co, k, p, s):
    side = osz(n, k, p, s)
    return sum(1 for _ in itertools.product(range(side), range(side), range(co))) * ci * k * k


def rf(layers):
    """Route B: grow the set of input pixels one output depends on, layer by layer, from the top down."""
    span = 1
    for k, s in reversed(layers):
        span = (span - 1) * s + k
    return span


# =================== 1. the ops module ===================
r = np.random.default_rng(2026)
for shape, f, k, s, p in [((2, 3, 7, 7), 4, 3, 2, 1), ((1, 1, 8, 8), 2, 3, 1, 1), ((3, 6, 6), 2, 2, 2, 0)]:
    x = r.standard_normal(shape); W = r.standard_normal((f, shape[-3], k, k)); b = r.standard_normal(f)
    y = ops.conv2d(Tensor(x), Tensor(W), Tensor(b), s, p).data
    xb = x if x.ndim == 4 else x[None]
    ref = np.stack([conv_loop(xi, W, b, s, p) for xi in xb])
    lv.claim(np.allclose(y if y.ndim == 4 else y[None], ref), f'conv2d forward {shape} k{k} s{s} p{p} matches loops')
    M = r.standard_normal(y.shape)
    xt, Wt, bt = Tensor(x.copy()), Tensor(W.copy()), Tensor(b.copy())
    ga = grad_check(lambda: ((ops.conv2d(xt, Wt, bt, s, p) * M) ** 2).mean(), [xt, Wt, bt])
    for t in (xt, Wt, bt):
        t.zero_grad()
    ((ops.conv2d(xt, Wt, bt, s, p) * M) ** 2).mean().backward()
    lossB = lambda: float(((np.stack([conv_loop(xi, W, b, s, p) for xi in (x if x.ndim == 4 else x[None])]).reshape(M.shape) * M) ** 2).mean())  # noqa: E731
    gb = max(relerr(t.grad, central(lossB, A)) for t, A in ((xt, x), (Wt, W), (bt, b)))
    lv.claim(ga < 1e-6 and gb < 1e-6, f'conv2d gradient {shape} k{k} s{s} p{p}: grad_check {ga:.1e}, loops and own differences {gb:.1e}')
x = r.standard_normal((2, 3, 4, 6)); M = r.standard_normal((2, 3, 2, 3))


def pool_loop(x, kind):
    out = np.zeros(x.shape[:2] + (x.shape[2] // 2, x.shape[3] // 2))
    for idx in np.ndindex(out.shape):
        n, c, i, j = idx
        win = x[n, c, 2 * i:2 * i + 2, 2 * j:2 * j + 2]
        out[idx] = win.max() if kind == 'max' else win.mean()
    return out


for kind, op in (('max', ops.maxpool2d), ('avg', ops.avgpool2d)):
    lv.claim(np.allclose(op(Tensor(x)).data, pool_loop(x, kind)), f'{kind} pool forward matches loops')
    xt = Tensor(x.copy())
    ga = grad_check(lambda: ((op(xt) * M) ** 2).sum(), [xt])
    xt.zero_grad(); ((op(xt) * M) ** 2).sum().backward()
    gb = relerr(xt.grad, central(lambda: float(((pool_loop(x, kind) * M) ** 2).sum()), x))
    lv.claim(ga < 1e-6 and gb < 1e-6, f'{kind} pool gradient: grad_check {ga:.1e}, loops and own differences {gb:.1e}')
tie = Tensor(np.array([[[3.0, 3.0], [1.0, 0.0]]]))
ops.maxpool2d(tie).sum().backward()
lv.claim(tie.grad.tolist() == [[[1.0, 0.0], [0.0, 0.0]]], 'max pool routes a tie to the first maximum')
g = r.standard_normal((2 * 9, 2 * 9)); xx = r.standard_normal((2, 2, 5, 5))
lv.claim(np.isclose(np.sum(ops.im2col(xx, 3, 2, 1) * g), np.sum(xx * ops.col2im(g, xx.shape, 3, 2, 1))), 'im2col and col2im are adjoint (stride 2, padding 1)')

# =================== 2. l5 ===================
for i, (n, k, p, s) in enumerate([(8, 3, 0, 1), (8, 3, 1, 1), (8, 3, 1, 2)]):
    E('l5', f'screens[0].widget.rows[{i}][2].answer', osz(n, k, p, s))
E('l5', 'screens[0].widget.rows[2][2].wrong[0].value', (8 + 2 - 3) / 2 + 1)
E('l5', 'screens[1].widget.answer', osz(32, 5, 2, 2)); E('l5', 'screens[1].widget.wrong[0].value', (32 + 4 - 5) / 2 + 1); E('l5', 'screens[1].widget.wrong[1].value', (32 + 2 - 5) // 2 + 1)
for i, (n, k, p, s) in enumerate([(12, 3, 0, 3), (7, 3, 1, 2), (10, 5, 0, 1), (28, 3, 1, 2)]):
    E('l5', f'screens[2].widget.rows[{i}][4].answer', osz(n, k, p, s))
E('l5', 'screens[4].widget.answer', (5 - 1) // 2); E('l5', 'screens[5].widget.answer', osz(64, 2, 0, 2)); E('l5', 'screens[5].widget.wrong[0].value', osz(64, 2, 0, 1))
E('l5', 'screens[5].explain.text', osz(64, 2, 0, 2) ** 2); E('l5', 'screens[5].explain.text', 64 * 64)
E('l5', 'screens[6].widget.answer', osz(10, 3, 0, 2)); E('l5', 'screens[6].widget.wrong[0].value', (10 - 3) / 2 + 1)
covered = {c for st in starts(9, 2, 0, 3) for c in (st, st + 1)}
E('l5', 'screens[7].widget.answer', 9 - len(covered)); E('l5', 'screens[7].explain.text', len(starts(9, 2, 0, 3)))
E('l5', 'screens[10].explain.text', osz(9, 3, 1, 2))
E('l5', 'quiz[0].widget.answer', osz(20, 3, 1, 2)); E('l5', 'quiz[1].widget.answer', 3)
cov12 = {c for st in starts(12, 3, 0, 4) for c in range(st, st + 3)}; E('l5', 'quiz[2].widget.answer', 12 - len(cov12))
lv.claim(osz(16, 3, 1, 2) == 8 and osz(16, 3, 1, 1) == 16, 'l5 transfer shapes 16, 16, 16, 8')

# =================== 3. l6 ===================
Mx = np.array([[1, 3, 2, 0], [4, 2, 1, 1], [0, 1, 5, 2], [3, 2, 0, 6]], float)
Ms = np.zeros_like(Mx); Ms[:, 1:] = Mx[:, :-1]
P1, A1, P2 = pool_loop(Mx[None, None], 'max')[0, 0], pool_loop(Mx[None, None], 'avg')[0, 0], pool_loop(Ms[None, None], 'max')[0, 0]
for i in range(2):
    for j in range(2):
        E('l6', f'screens[0].widget.rows[{i}][{j + 1}].answer', P1[i, j]); E('l6', f'screens[0].widget.rows[{i}][{j + 1}].wrong[0].value', A1[i, j])
E('l6', 'screens[1].widget.answer', int((P1 != P2).sum())); E('l6', 'screens[2].widget.answer', A1[0, 0]); E('l6', 'screens[2].widget.wrong[1].value', Mx[:2, :2].sum())
E('l6', 'screens[4].widget.answer', 2 / 4); E('l6', 'screens[11].widget.answer', 410)
PNL = [120, -340, 80, -95, 210, -60, -410, 150, -220, 30]
lv.claim(max(-v for v in PNL[5:]) == 410 and max(PNL[5:]) == 150 and sum(-v for v in PNL[5:]) / 5 == 102 and max(-v for v in PNL[:5]) == 340, 'weekly worst losses 340 and 410; best day 150; mean loss 102')
E('l6', 'quiz[0].widget.answer', 28 // 2); E('l6', 'quiz[2].widget.answer', 1.8 / 9)

# =================== 4. l7 ===================
E('l7', 'screens[1].widget.answer', params(('conv', 8, 16, 3))); E('l7', 'screens[1].widget.wrong[1].value', 16 * 72)
E('l7', 'screens[2].widget.answer', params(('dense', 64, 1024))); E('l7', 'screens[2].widget.wrong[0].value', 64 * 1024); E('l7', 'screens[2].widget.wrong[1].value', params(('dense', 64, 64)))
E('l7', 'screens[0].explain.text', params(('conv', 1, 16, 3))); lv.claim(params(('dense', 64, 1024)) / params(('conv', 1, 16, 3)) == 416, 'ratio 416, "about 400 times"')
E('l7', 'screens[3].widget.answer', macs(8, 1, 16, 3, 1, 1)); E('l7', 'screens[3].widget.wrong[0].value', macs(8, 1, 1, 3, 1, 1))
NET3 = [('conv', 1, 16, 3), ('pool',), ('dense', 4 * 4 * 16, 10)]
E('l7', 'screens[4].widget.rows[0][2].answer', params(NET3[0])); E('l7', 'screens[4].widget.rows[2][2].answer', params(NET3[2])); E('l7', 'screens[4].widget.rows[3][2].answer', sum(map(params, NET3)))
E('l7', 'screens[4].widget.rows[3][2].wrong[0].value', params(NET3[0]) + params(('dense', 1024, 10)))
E('l7', 'screens[4].explain.text', round(100 * params(NET3[2]) / sum(map(params, NET3))))
E('l7', 'screens[5].widget.answer', rf([(3, 1)] * 3)); lv.claim(rf([(3, 1)] * 2) == 5, 'two 3 by 3 layers see 5 by 5')
E('l7', 'screens[6].widget.answer', params(('conv', 3, 8, 5))); E('l7', 'screens[6].widget.wrong[0].value', params(('conv', 1, 8, 5)))
E('l7', 'screens[6].widget.wrong[1].value', 8 * 75 + 8 * osz(32, 5, 2, 1) ** 2)
E('l7', 'screens[7].explain.text', macs(16, 1, 16, 3, 1, 1))
E('l7', 'screens[9].widget.tests[1].expect', params(('dense', 64, 40)) + params(('dense', 40, 10)))
E('l7', 'screens[10].widget.tests[2].expect', rf([(3, 1), (2, 2), (3, 1)])); E('l7', 'screens[10].widget.tests[3].expect', rf([(3, 2), (3, 2)]))
E('l7', 'screens[11].widget.answer', 500 * macs(8, 1, 16, 3, 1, 1)); E('l7', 'screens[11].widget.wrong[1].value', 500 * 2730)
E('l7', 'quiz[0].widget.answer', params(('conv', 64, 32, 1))); E('l7', 'quiz[1].widget.answer', rf([(3, 1)] * 4)); E('l7', 'quiz[2].widget.answer', macs(16, 8, 8, 3, 1, 1))

# =================== 5. l8 ===================
X4 = np.array([[1, 2, 0, 1], [3, 1, 2, 0], [0, 2, 1, 3], [1, 0, 2, 1]], float)
C16 = ops.im2col(X4[None, None], 3, 1, 1)
XP = np.pad(X4, 1)
loop_rows = np.array([XP[i:i + 3, j:j + 3].ravel() for i in range(4) for j in range(4)])
lv.claim(np.array_equal(C16, loop_rows) and C16.shape == (16, 9), 'im2col of the 4 by 4 example by the op and by loops; 16 by 9')
for a in range(3):
    for bb in range(3):
        E('l8', f'screens[0].widget.rows[{a}][{bb + 1}].answer', int(XP[a, 1 + bb]))
E('l8', 'screens[1].widget.answer', C16.shape[0]); E('l8', 'screens[1].widget.wrong[0].value', 36)
E('l8', 'screens[3].widget.answer', int(conv_loop(X4[None], np.array([[[[0, 1, 0], [1, -4, 1], [0, 1, 0]]]], float), [0.0], 1, 1)[0, 0, 0]))
stamp = np.zeros((6, 6))
for i in range(4):
    for j in range(4):
        stamp[i:i + 3, j:j + 3] += 1
CNT = stamp[1:5, 1:5]
E('l8', 'screens[4].widget.answer', CNT[0, 0]); E('l8', 'screens[5].widget.answer', CNT[1, 1])
lv.claim(np.array_equal(ops.col2im(np.ones((16, 9)), (1, 1, 4, 4), 3, 1, 1)[0, 0], CNT), 'col2im of all ones gives the stamped counts 4, 6, 9')
E('l8', 'screens[10].widget.tests[0].expect', str(CNT.tolist()))
E('l8', 'screens[11].widget.answer', 390 * 500 * 9 * 8 / 1e6); E('l8', 'screens[11].widget.wrong[0].value', 390 * 500 * 8 / 1e6); E('l8', 'screens[11].widget.wrong[1].value', 390 * 500 * 9 * 4 / 1e6)
E('l8', 'quiz[1].widget.answer', osz(8, 3, 1, 2) ** 2); E('l8', 'quiz[2].widget.answer', CNT[0, 1])
lv.claim(ops.im2col(np.zeros((1, 3, 10, 10)), 3, 1, 0).shape == (64, 27) and ops.im2col(np.zeros((1, 1, 8, 8)), 3, 1, 1).shape == (64, 9), 'shapes 64 by 27 and 64 by 9')

# =================== 6. review, homework, problems ===================
E('review', 'items[0].widget.answer', osz(16, 3, 1, 2)); E('review', 'items[1].widget.answer', params(('conv', 4, 6, 5))); E('review', 'items[1].widget.wrong[0].value', params(('conv', 1, 6, 5)))
E('review', 'items[2].widget.answer', rf([(3, 1), (2, 2), (3, 1), (2, 2), (3, 1)])); E('review', 'items[2].widget.wrong[0].value', rf([(3, 1), (2, 1), (3, 1), (2, 1), (3, 1)]))
E('review', 'items[4].widget.answer', 0.8 / 4); E('review', 'items[6].widget.answer', (9 - 1) // 2); E('review', 'items[7].widget.answer', macs(8, 2, 4, 3, 1, 1))
lv.claim(ops.im2col(np.zeros((1, 2, 6, 6)), 3, 1, 0).shape == (16, 18), 'review im2col shape 16 by 18')
E('homework', 'items[4].widget.answer', macs(32, 3, 16, 3, 1, 2)); E('homework', 'items[4].widget.wrong[0].value', macs(32, 3, 16, 3, 1, 1))
side = osz(osz(28, 5, 0, 1) // 2, 3, 1, 2); E('homework', 'items[5].widget.answer', side)
design = [('conv', 1, 8, 3), ('conv', 8, 16, 3), ('conv', 16, 16, 3), ('dense', 256, 10)]
E('homework', 'items[3].model', sum(map(params, design))); E('homework', 'items[3].model', params(('dense', 16 * 32 * 32, 10)))
E('homework', 'items[3].model', rf([(3, 1), (2, 2), (3, 1), (2, 2), (3, 1)]))
E('problems', 'items[0].parts[0].widget.answer', osz(osz(12, 3, 1, 1) // 2, 3, 0, 1))
net = [('conv', 1, 8, 3), ('conv', 8, 16, 3), ('dense', 256, 10)]
E('problems', 'items[0].parts[1].widget.answer', sum(map(params, net)))
E('problems', 'items[0].parts[2].widget.answer', macs(12, 1, 8, 3, 1, 1) + macs(6, 8, 16, 3, 0, 1)); E('problems', 'items[0].parts[2].widget.wrong[1].value', macs(12, 1, 8, 3, 1, 1))
Hbest = max(h for h in range(1, 200) if params(('dense', 144, h)) + params(('dense', h, 10)) <= 3818)
E('problems', 'items[0].parts[3].widget.answer', Hbest); E('problems', 'items[0].parts[3].explain.text', params(('dense', 144, 25)) + params(('dense', 25, 10)))
E('problems', 'items[1].parts[0].widget.answer', osz(50, 4, 1, 3)); E('problems', 'items[1].parts[2].widget.answer', osz(50, 7, 3, 2))
E('problems', 'items[2].parts[0].widget.answer', osz(5, 3, 1, 2)); E('problems', 'items[2].parts[2].widget.answer', 9 * 18 * 4)
st7 = np.zeros((7, 7))
for i in starts(5, 3, 1, 2):
    for j in starts(5, 3, 1, 2):
        st7[i:i + 3, j:j + 3] += 1
E('problems', 'items[2].parts[3].widget.answer', st7[2, 2])
lv.claim(st7[3, 3] == 1, 'the centre pixel sits in one stride-2 window')


# =================== 7. every code widget ===================
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
        ns = {'__learner_source__': src}
        exec(ZQ_LIB, ns)
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
