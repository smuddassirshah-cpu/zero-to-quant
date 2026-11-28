"""Recompute every number stated in backprop level 4 (Gradients for arrays), test the canonical autograd.py, and check
each value at its JSON path.

Run: <venv>/bin/python docs/reports/backprop-L4-numbers.py   (NumPy and the standard library; exits 0 when every check passes)

Route A is the canonical app/content/data/ai/autograd.py (its grad_check and its ops). Route B is independent: plain NumPy
with the gradients written by hand, and a central-difference helper of this script that never touches autograd.
Every code widget of the level is run here as well: the model solution must pass its hidden tests, the starter must fail
them, and each mutant must first fail the test it names (ENGINE-BACKLOG 1263; grade-all --code repeats this in Pyodide).
"""
import hashlib
import json
import math
import os
import random
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

CANON_PATH = os.path.join(ROOT, 'app', 'content', 'data', 'ai', 'autograd.py')
CANON = open(CANON_PATH, encoding='utf8').read()
sys.path.insert(0, os.path.dirname(CANON_PATH))
import autograd as ag  # noqa: E402
from autograd import Tensor, cross_entropy, softmax, sgd_step, grad_check, concat, unbroadcast  # noqa: E402

lv = Level('backprop', 4)
E = lv.expect
D = lambda ref: lv._file(ref)[1]  # noqa: E731


def two(label, a, b, tol=1e-9):
    a, b = np.asarray(a, float), np.asarray(b, float)
    lv.claim(a.shape == b.shape and np.allclose(a, b, rtol=tol, atol=tol), f'{label}: routes agree')


def central(f, arrays, h=1e-5):
    """Route B: central differences of a plain-float function f() over every entry of the given NumPy arrays."""
    out = []
    for A in arrays:
        g = np.zeros_like(A)
        for i in np.ndindex(A.shape):
            keep = A[i]
            A[i] = keep + h
            up = f()
            A[i] = keep - h
            down = f()
            A[i] = keep
            g[i] = (up - down) / (2 * h)
        out.append(g)
    return out


def rel(gs, ns):
    diff = max(np.abs(a - b).max() for a, b in zip(gs, ns))
    return diff / max(max(np.abs(a).max() for a in gs), max(np.abs(b).max() for b in ns), 1e-12)


# =================== 1. the canonical file ===================
sha = hashlib.sha256(CANON.encode('utf8')).hexdigest()
print('autograd.py sha256', sha)
lv.claim(CANON.startswith('"""backprop level 4 autograd') and '__version__ = "1.0"' in CANON.split('import numpy')[0], 'docstring names it and __version__ = "1.0" comes first')
lv.claim(ag.__version__ == '1.0', 'version 1.0')
lv.claim(len(CANON.encode('utf8')) < 256 * 1024, f'well under 256 KB ({len(CANON)} bytes)')
lv.claim(set(l.split()[1] for l in CANON.splitlines() if l.startswith('import ') or l.startswith('from ')) == {'numpy'}, 'imports NumPy only')
shipped = []


def find_files(node):
    if isinstance(node, dict):
        if isinstance(node.get('files'), dict) and 'autograd.py' in node['files']:
            shipped.append(node['files']['autograd.py'])
        for v in node.values():
            find_files(v)
    elif isinstance(node, list):
        for v in node:
            find_files(v)


for fid, doc in lv.files.items():
    find_files(doc)
lv.claim(len(shipped) >= 1 and all(hashlib.sha256(s.encode('utf8')).hexdigest() == sha for s in shipped), f'every shipped files["autograd.py"] ({len(shipped)}) equals the canonical file byte for byte')

rng = np.random.default_rng(2026)
R = lambda *s: rng.standard_normal(s)  # noqa: E731


def op_check(label, build, arrays):
    """Route A: autograd's grad_check. Route B: autograd's backward against this script's own central differences."""
    ts = [Tensor(a) for a in arrays]
    ra = grad_check(lambda: build(*ts), ts)
    for t in ts:
        t.zero_grad()
    build(*ts).backward()
    rb = rel([t.grad for t in ts], central(lambda: float(build(*[Tensor(a) for a in [t.data for t in ts]]).data), [t.data for t in ts]))
    lv.claim(ra < 1e-6 and rb < 1e-6, f'op {label}: grad_check {ra:.1e}, independent check {rb:.1e}')


W3 = R(3, 3)
op_check('+ broadcast row', lambda a, b: ((a + b) * W3).sum(), [R(3, 3), R(3)])
op_check('+ broadcast column', lambda a, b: ((a + b) * W3).sum(), [R(3, 3), R(3, 1)])
op_check('+ scalar and leading axis', lambda a, b: ((a + b) ** 2).mean(), [R(2, 3, 3), R(1)])
op_check('- both ways', lambda a, b: ((a - b) * W3).sum() + ((2.0 - a) * W3).sum(), [R(3, 3), R(1, 3)])
op_check('* broadcast', lambda a, b: (a * b * W3).sum(), [R(3, 3), R(3, 1)])
op_check('/ both ways', lambda a, b: (a / (b * b + 1.0)).sum() + (1.0 / (a * a + 2.0)).sum(), [R(3, 3), R(3)])
op_check('** 3 and ** 0.5', lambda a: (a ** 3).sum() + ((a * a + 1.0) ** 0.5).sum(), [R(2, 4)])
op_check('neg', lambda a: (-a * W3).sum(), [R(3, 3)])
op_check('@ 2-D', lambda a, b: ((a @ b) ** 2).sum(), [R(4, 3), R(3, 2)])
op_check('@ batched with broadcast W', lambda a, b: ((a @ b) ** 2).mean(), [R(2, 3, 4), R(4, 2)])
op_check('sum axis keepdims', lambda a: (a.sum(axis=1, keepdims=True) * a).sum() + (a.sum(axis=0) ** 2).sum(), [R(3, 4)])
op_check('mean axis', lambda a: (a.mean(axis=0) ** 2).sum() + (a.mean(axis=-1, keepdims=True) * a).mean(), [R(3, 4)])
op_check('tanh', lambda a: (a.tanh() * W3).sum(), [R(3, 3)])
op_check('relu', lambda a: (a.relu() * W3).sum(), [R(3, 3)])
op_check('exp and log', lambda a: (a.exp() + (a * a + 1.0).log()).mean(), [R(3, 3)])
V6 = R(6, 1)
op_check('reshape', lambda a: (a.reshape(2, 6) @ Tensor(V6)).sum(), [R(3, 4)])
op_check('T', lambda a: ((a.T @ a) ** 2).sum(), [R(3, 2)])
IDX = np.array([[1, 2, 1], [0, 4, 4]])
op_check('index with repeats', lambda c: (c[IDX] ** 2).sum(), [R(5, 3)])
op_check('index tuple and slice', lambda c: (c[np.array([0, 2, 2]), np.array([1, 0, 1])] * 3.0).sum() + (c[:, 1:] ** 2).sum(), [R(3, 3)])
op_check('concat axis 1 and -1', lambda a, b: ((concat([a, b], axis=1)) ** 2).sum() + (concat([a, b], axis=-1) * 2.0).sum(), [R(2, 3), R(2, 2)])
op_check('cross_entropy', lambda z: cross_entropy(z, [2, 0, 1, 2]), [R(4, 3) * 3])
op_check('reused tensor', lambda a: (a * a + a).sum() + (a @ a).sum(), [R(3, 3)])
# reused tensor and repeats by hand
a = Tensor([1.5, -2.0]); (a * a + a).sum().backward(); two('reused tensor gradient 2a + 1', a.grad, [4.0, -3.0])
C = Tensor(np.arange(12.0).reshape(4, 3)); C[np.array([1, 1, 3])].sum().backward(); two('repeated index adds', C.grad, [[0, 0, 0], [2, 2, 2], [0, 0, 0], [1, 1, 1]])
b = Tensor(np.zeros(3)); out = Tensor(np.zeros((5, 3))) + b; out.grad = np.arange(15.0).reshape(5, 3); out._backward(); two('row bias sums down rows', b.grad, [30, 35, 40])
c = Tensor(np.zeros((5, 1))); out = Tensor(np.zeros((5, 3))) + c; out.grad = np.arange(15.0).reshape(5, 3); out._backward(); two('column bias sums across', c.grad, [[3], [12], [21], [30], [39]])
two('unbroadcast to ()', unbroadcast(np.arange(6.0).reshape(2, 3), ()), 15.0)
two('unbroadcast (2,4,3) to (4,1)', unbroadcast(np.arange(24.0).reshape(2, 4, 3), (4, 1)), np.arange(24.0).reshape(2, 4, 3).sum(0).sum(1, keepdims=True))
# conventions
lv.claim(Tensor([1, 2]).data.dtype == np.float64 and Tensor(np.float32([1])).data.dtype == np.float64, 'data is float64 whatever comes in')
lv.claim(isinstance(np.ones(3) + Tensor([1.0, 2, 3]), Tensor) and isinstance(np.ones((2, 3)) @ Tensor(np.ones((3, 1))), Tensor), 'an ndarray on the left is wrapped (__array_ufunc__ = None)')
lv.claim(isinstance(2 - Tensor([1.0]), Tensor) and float((2 / Tensor([4.0])).data[0]) == 0.5, 'number on the left: b - a, b / a')
try:
    Tensor(np.ones(2)).backward(); lv.claim(False, 'backward on size 2 raises ValueError')
except ValueError:
    lv.claim(True, 'backward on size 2 raises ValueError')
try:
    Tensor([2.0]) ** Tensor([2.0]); lv.claim(False, 'a ** Tensor raises TypeError')
except TypeError:
    lv.claim(True, 'a ** Tensor raises TypeError')
t = Tensor([[3.0]]); lv.claim(t.item() == 3.0 and isinstance(t.item(), float) and t.shape == (1, 1), 'item() and shape')
p = Tensor([1.0, 2.0]); p.grad += 5; g0 = p.grad; p.zero_grad(); lv.claim(p.grad is g0 and not p.grad.any(), 'zero_grad zeroes in place')
p = Tensor([1.0, 2.0]); p.grad = np.array([1.0, -1.0]); sgd_step([p], 0.5); two('sgd_step', p.data, [0.5, 2.5]); lv.claim(p.grad.tolist() == [1.0, -1.0], 'sgd_step leaves grad alone')
two('softmax of a plain array, rows', softmax(np.array([[2.0, 1.0, 0.1], [1000.0, 999.0, 998.1]])), np.array([[0.659001, 0.242433, 0.098566]] * 2), 1e-5)
lv.claim(np.allclose(softmax(np.array([0.0, 3.0]), axis=0).sum(), 1.0), 'softmax axis argument')
for depth in (200, 5000):
    old = sys.getrecursionlimit(); sys.setrecursionlimit(150)
    try:
        x = Tensor([1.0]); y = x
        for _ in range(depth):
            y = (y * 0.999).tanh() + 0.001
        y.sum().backward(); ok = np.isfinite(x.grad).all() and x.grad[0] > 0
    except RecursionError:
        ok = False
    finally:
        sys.setrecursionlimit(old)
    lv.claim(ok, f'{depth}-step chain backward runs with the recursion limit at 150 (no recursion)')
lv.claim(math.isclose(cross_entropy(Tensor([[0.0, -800.0]]), [1]).item(), 800.0) and math.isclose(cross_entropy(Tensor([[1000.0, 999.0, 998.1]]), [0]).item(), 0.417030016, rel_tol=1e-8), 'cross_entropy stable at both extremes')
z = R(5, 4); y = [3, 0, 1, 1, 2]; L = Tensor(z); cross_entropy(L, y).backward()
pz = np.exp(z) / np.exp(z).sum(1, keepdims=True); oh = np.eye(4)[y]
two('cross_entropy value vs plain NumPy', cross_entropy(Tensor(z), y).item(), np.mean(-np.log(pz[np.arange(5), y])))
two('cross_entropy backward is (P - Y)/n', L.grad, (pz - oh) / 5)

# =================== 2. the course network (level 3) rebuilt ===================
def course():
    r = random.Random(42); Ws, bs = [], []
    for nin, nout in ((2, 3), (3, 1)):
        rows = [([r.uniform(-1, 1) for _ in range(nin)], r.uniform(-1, 1)) for _ in range(nout)]
        Ws.append(Tensor(np.array([w for w, _ in rows]).T)); bs.append(Tensor(np.array([bb for _, bb in rows])))
    return Ws, bs


X4 = np.array([[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0], [-1.0, 1.0]]); Y4 = np.array([[1.0], [1.0], [-1.0], [-1.0]])
Ws, bs = course()


def net_loss():
    a = Tensor(X4)
    for W, bb in zip(Ws, bs):
        a = (a @ W + bb).tanh()
    return ((a - Y4) ** 2).mean()


L0 = net_loss(); L0.backward(); b2_mean = float(bs[1].grad[0])
# route B: NumPy by hand from the same draws, summed loss
W1, b1, W2, b2 = [t.data.copy() for t in (Ws[0], bs[0], Ws[1], bs[1])]
H = np.tanh(X4 @ W1 + b1); O = np.tanh(H @ W2 + b2); Ls = ((O - Y4) ** 2).sum()
dO = 2 * (O - Y4) * (1 - O ** 2); db2_sum = dO.sum(0)[0]
two('loss at step 0, sum = 4 x mean', 4 * L0.item(), Ls, 1e-12)
lv.claim(round(Ls, 6) == 5.5568 and round(L0.item(), 4) == 1.3892, f'5.556800 summed, 1.3892 as a mean ({Ls:.6f}, {L0.item():.6f})')
two('output-bias gradient: sum = 4 x mean', 4 * b2_mean, db2_sum, 1e-12)
lv.claim(round(db2_sum, 6) == -2.41249 and round(b2_mean, 4) == -0.6031, f'b2 gradient -2.412490 summed, -0.6031 as a mean ({db2_sum:.6f}, {b2_mean:.6f})')
lv.claim(grad_check(net_loss, Ws + bs) < 1e-6, 'course network passes grad_check')
for k in range(200):
    for q in Ws + bs:
        q.zero_grad()
    net_loss().backward(); sgd_step(Ws + bs, 0.2)
lsum = 4 * net_loss().item()
w1, c1, w2, c2 = W1.copy(), b1.copy(), W2.copy(), b2.copy()
for k in range(200):
    Hh = np.tanh(X4 @ w1 + c1); Oo = np.tanh(Hh @ w2 + c2); dO = 2 * (Oo - Y4) * (1 - Oo ** 2); dH = dO @ w2.T * (1 - Hh ** 2)
    w2 -= 0.05 * Hh.T @ dO; c2 -= 0.05 * dO.sum(0); w1 -= 0.05 * X4.T @ dH; c1 -= 0.05 * dH.sum(0)
lsum_b = ((np.tanh(np.tanh(X4 @ w1 + c1) @ w2 + c2) - Y4) ** 2).sum()
two('200 steps: mean at 0.2 vs sum at 0.05', lsum, lsum_b, 1e-9)
lv.claim(round(lsum, 6) == 0.02502, f'0.025020 after 200 steps ({lsum:.6f})')

# =================== 3. lesson numbers ===================
# l13
X2 = np.array([[2., -1], [1, 3]]); G2 = np.array([[1., 2], [-1, 0.5]]); XtG = X2.T @ G2
two('l13 2x2 by hand', XtG, [[2 * 1 + 1 * -1, 2 * 2 + 1 * 0.5], [-1 * 1 + 3 * -1, -1 * 2 + 3 * 0.5]])
E('l13', 'screens[3].widget.answer', XtG[0, 1]); E('l13', 'screens[3].widget.wrong[0].value', (X2 @ G2)[0, 1]); E('l13', 'screens[3].widget.wrong[1].value', (G2.T @ X2)[0, 1])
tr = np.abs(XtG - G2.T @ X2).max() / max(np.abs(XtG).max(), np.abs(G2.T @ X2).max())
E('l13', 'screens[6].canvas.params.lines[3]', f'{tr:.2f}'); E('l13', 'screens[6].explain.text', '8.5/4.5 = 1.89')
r0 = np.random.default_rng(0); A0 = r0.standard_normal((3, 4)); B0 = r0.standard_normal((4, 2))
ra = rel([(A0 @ B0) @ B0.T], central(lambda: 0.5 * ((A0 @ B0) ** 2).sum(), [A0]))
At = Tensor(A0.copy()); Bt = Tensor(B0.copy()); rb = grad_check(lambda: 0.5 * ((At @ Bt) ** 2).sum(), [At])
lv.claim(f'{ra:.1e}' == f'{rb:.1e}' == '9.5e-12', f'l13 1/2||AB||^2 check {ra:.2e} and {rb:.2e}')
E('l13', 'screens[5].canvas.params.lines[5]', '9.5e-12'); E('l13', 'screens[5].explain.text', '9.5 \\times 10^{-12}')
E('l13', 'screens[1].widget.answer', 4)
F = np.array([[1.0, -0.5, 0.8], [0.2, 0.4, -0.3]]); be = np.array([1.2, 0.5]); rr = np.array([1.5, -0.4, 0.9]); res_ = be @ F - rr
gF = res_ @ F.T; gB = central(lambda: 0.5 * ((be @ F - rr) ** 2).sum(), [be])[0]
two('l13 factor model gradient', gF, gB, 1e-8)
E('l13', 'screens[9].widget.answer', round(gF[0], 3)); E('l13', 'screens[9].widget.wrong[1].value', round(gF[1], 3)); E('l13', 'screens[9].explain.text', '(-0.272, -0.013)')
for i, v in enumerate(be @ F):
    E('l13', f'screens[9].canvas.params.rows[{i}][3]', f'{v:.2f}')
Xq = np.array([[1, 2], [0, -1], [3, 1]], float); Gq = np.array([[0.5], [-1], [2]]); E('l13', 'quiz[1].widget.answer', (Xq.T @ Gq)[1, 0]); E('l13', 'quiz[1].widget.wrong[1].value', (Xq.T @ Gq)[0, 0])
# l14
G5 = np.array([[0.4, -0.1, 0.4], [0.5, 0.3, -0.2], [-0.1, 0.2, 0.1], [0.3, -0.4, 0.0], [0.1, 0.2, 0.3]])
bt = Tensor([0.5, -1.0, 2.0]); out = Tensor(np.zeros((5, 3))) + bt; out.grad = G5; out._backward()
two('l14 bias gradient two routes', bt.grad, central(lambda: float((G5 * (np.zeros((5, 3)) + bvec)).sum()), [bvec := np.array([0.5, -1.0, 2.0])])[0], 1e-8)
E('l14', 'screens[0].widget.answer', round(0.01 * G5[:, 1].sum(), 6)); E('l14', 'screens[0].widget.wrong[0].value', 0.01 * G5[0, 1]); E('l14', 'screens[0].widget.wrong[1].value', round(0.01 * G5[:, 1].mean(), 6))
E('l14', 'screens[1].widget.answer', round(G5[:, 2].sum(), 6)); E('l14', 'screens[1].widget.wrong[1].value', round(G5[:, 2].mean(), 6))
E('l14', 'screens[2].canvas.right.params.cells', round(G5[:, 0].sum(), 6))
E('l14', 'screens[3].widget.answer', round(G5[1].sum(), 6)); E('l14', 'screens[3].widget.wrong[1].value', round(G5[1].mean(), 6)); E('l14', 'screens[3].explain.text', '(0.7, 0.6, 0.2, -0.1, 0.6)')
E('l14', 'screens[5].widget.answer', round(1 / 15, 4)); E('l14', 'screens[7].widget.answer', round(G5.sum(), 6)); E('l14', 'screens[7].widget.wrong[1].value', round(G5.sum() / 15, 4))
E('l14', 'screens[9].widget.answer', round(0.0001 * (20000 + 35000 + 15000 + 30000), 6)); E('l14', 'screens[9].widget.wrong[0].value', 0.0001 * 25000)
E('l14', 'quiz[0].widget.answer', -2 + 1 + 0.5); E('l14', 'quiz[0].widget.wrong[1].value', round(-0.5 / 3, 4)); E('l14', 'quiz[2].widget.answer', 1 / 40)
# l15
zc = np.array([2.0, 1.0, 0.1]); pc = softmax(zc); gc = pc - np.eye(3)[0]
gcb = central(lambda: float(-zc2[0] + np.log(np.exp(zc2).sum())), [zc2 := zc.copy()])[0]
two('l15 gradient p - y vs central differences', gc, gcb, 1e-8)
E('l15', 'screens[0].widget.answer', round(pc[0], 3)); E('l15', 'screens[0].widget.wrong[0].value', round(2 / 3.1, 3))
E('l15', 'screens[0].explain.text', '(0.659, 0.2424, 0.0986)')
E('l15', 'screens[2].widget.answer', round(-math.log(pc[0]), 3)); E('l15', 'screens[2].widget.wrong[0].value', round(-math.log2(pc[0]), 3)); E('l15', 'screens[2].widget.wrong[1].value', round(-math.log10(pc[0]), 3))
E('l15', 'screens[4].widget.answer', round(gc[0], 3)); E('l15', 'screens[4].feedback.correct', '(-0.341, 0.2424, 0.0986)')
E('l15', 'screens[6].widget.answer', round(gc[0] / 2, 4))
z2 = np.array([0.5, 0.5, 1.5]); g2 = softmax(z2) - np.eye(3)[2]; E('l15', 'screens[6].canvas.params.rows[1][3]', f'({g2[0]:.4f}, {g2[1]:.4f}, −{-g2[2]:.4f})')
zr = np.array([-1.5, 0.0, 2.0]); gin = np.array([0.4, 0.3, -0.2]); th = gin * (1 - np.tanh(zr) ** 2)
E('l15', 'screens[7].explain.text', f'({th[0]:.4f}, {th[1]:.1f}, {th[2]:.4f})')
lv.claim(np.exp(-800.0) == 0.0 and cross_entropy(Tensor([[0.0, -800.0]]), [1]).item() == 800.0, 'l15 e^-800 underflows; fused loss 800')
lv.claim(np.isnan(np.exp(np.array([1000.0, 999.0])) / np.exp(np.array([1000.0, 999.0])).sum()).all(), 'l15 direct softmax at 1000 is nan')
E('l15', 'screens[10].widget.answer', 0.3 - 1); E('l15', 'quiz[0].widget.answer', round(math.log(27), 4)); E('l15', 'quiz[0].widget.wrong[0].value', round(math.log2(27), 4))
# l16
E('l16', 'screens[1].widget.answer', round(Ls / 4, 4)); E('l16', 'screens[1].widget.wrong[1].value', round(Ls * 4, 4))
E('l16', 'screens[3].widget.answer', round(db2_sum / 4, 4)); E('l16', 'screens[3].widget.wrong[1].value', round(db2_sum * 4, 4)); E('l16', 'screens[3].prose', '-2.412490')
r0 = np.random.default_rng(0); r0.standard_normal((3, 4)); r0.standard_normal((4, 2)); r0.standard_normal((5, 3)); r0.standard_normal(3)
prec = {}
for dt in (np.float64, np.float32):
    Xs = r0.standard_normal((4, 3)).astype(dt); Wsd = r0.standard_normal((3, 2)).astype(dt)
    an = Xs.T @ (1 - np.tanh(Xs @ Wsd) ** 2); hh = dt(1e-5) if dt == np.float64 else dt(1e-3); nm = np.zeros_like(Wsd)
    for i in range(3):
        for j in range(2):
            Wp = Wsd.copy(); Wp[i, j] += hh; Wm = Wsd.copy(); Wm[i, j] -= hh
            nm[i, j] = (np.tanh(Xs @ Wp).sum() - np.tanh(Xs @ Wm).sum()) / (2 * hh)
    prec[dt.__name__] = float(np.abs(nm - an).max() / np.abs(an).max())
lv.claim(f"{prec['float64']:.1e}" == '2.6e-11' and f"{prec['float32']:.1e}" == '8.0e-05', f'l16 tanh layer {prec}')
E('l16', 'screens[5].canvas.params.lines[1]', '2.6e-11'); E('l16', 'screens[5].canvas.params.lines[3]', '8.0e-05')
r5 = np.random.default_rng(5); Xr = r5.standard_normal((6, 3)); W1r = r5.standard_normal((3, 4)); W2r = r5.standard_normal((4, 1))
T1, T2 = Tensor(W1r.copy()), Tensor(W2r.copy())


def inplace_relu(t):
    t.data[t.data < 0] = 0
    return t


ok_a = grad_check(lambda: (((Tensor(Xr) @ T1).relu() @ T2) ** 2).mean(), [T1, T2])
bug_a = grad_check(lambda: ((inplace_relu(Tensor(Xr) @ T1) @ T2) ** 2).mean(), [T1, T2])
Hh = Xr @ W1r; Hr = np.maximum(Hh, 0); O = Hr @ W2r; Gd = 2 * O / O.size
dW2 = Hr.T @ Gd; dW1_bug = Xr.T @ (Gd @ W2r.T); dW1_ok = Xr.T @ ((Gd @ W2r.T) * (Hh > 0))
num = central(lambda: float(((np.maximum(Xr @ W1r, 0) @ W2r) ** 2).mean()), [W1r, W2r])
bug_b = rel([dW1_bug, dW2], num); ok_b = rel([dW1_ok, dW2], num)
lv.claim(f'{bug_a:.3f}' == f'{bug_b:.3f}' == '0.161' and f'{ok_a:.1e}' == '7.0e-12' and ok_b < 1e-9, f'l16 in-place ReLU {bug_a:.4f} / {bug_b:.4f}; ordinary {ok_a:.1e} / {ok_b:.1e}')
E('l16', 'screens[6].canvas.params.lines[5]', '0.161'); E('l16', 'screens[6].canvas.params.lines[7]', '7.0e-12')
E('l16', 'screens[7].widget.answer', 2 * 3)
rD = np.random.default_rng(31); Cd = rD.standard_normal((10, 4)); Wd = rD.standard_normal((12, 5)); idxD = np.array([[1, 2, 1], [0, 9, 9]]); yD = [3, 0]
zD = Cd[idxD].reshape(2, 12) @ Wd; lossD = np.mean(np.log(np.exp(zD).sum(1)) - zD[np.arange(2), yD])
lv.claim(f'{lossD:.6f}' in D('l16')['screens'][9]['widget']['tests'][0]['expect'], f'l16 lookup loss {lossD:.6f} by plain NumPy matches the test')
npar = 64 * 32 + 32 + 32 * 3 + 3; E('l16', 'screens[10].widget.answer', 2 * npar); E('l16', 'screens[10].widget.wrong[0].value', npar); E('l16', 'screens[10].feedback.correct', '2179')
E('l16', 'quiz[2].widget.answer', 4 * 0.05)
# review-4
Xr4 = np.array([[2, 1], [-1, 0], [1, 3]], float); Gr4 = np.array([[1], [2], [-1]], float); E('review', 'items[1].widget.answer', (Xr4.T @ Gr4)[1, 0]); E('review', 'items[1].widget.wrong[1].value', (Xr4.T @ Gr4)[0, 0])
Wr = np.array([[1, -1], [2, 1]], float); gr = np.array([[3, -2]], float); E('review', 'items[2].widget.answer', (gr @ Wr.T)[0, 1]); E('review', 'items[2].widget.wrong[0].value', (gr @ Wr)[0, 1])
G4 = np.array([[0.5, 1], [-1, 2], [0.25, -0.5], [1.5, 0]]); E('review', 'items[3].widget.answer', G4[:, 0].sum()); E('review', 'items[3].widget.wrong[0].value', round(G4[:, 0].mean(), 2))
pr = softmax(np.log([6.0, 3.0, 1.0])); two('review softmax of logs', pr, [0.6, 0.3, 0.1])
E('review', 'items[5].widget.answer', round(pr[1] - 1, 6)); E('review', 'items[6].widget.answer', round(-math.log(0.3), 4)); E('review', 'items[6].widget.wrong[0].value', round(-math.log2(0.3), 4))
E('review', 'items[6].widget.wrong[1].value', round(-math.log10(0.3), 4)); E('review', 'items[6].widget.wrong[2].value', round(-math.log(0.6), 4))
E('review', 'items[7].widget.answer', -0.4 / 8); E('review', 'items[9].widget.answer', round(0.03 / 1.2, 6)); E('review', 'items[9].widget.wrong[0].value', round(0.03 / 1.17, 4))
# homework-4
X5 = np.array([[1, 0], [0, 2], [1, 1]], float); W5 = np.array([[0.5], [-1]]); Y5 = np.array([[1], [-1], [0]], float)
g5 = X5.T @ (X5 @ W5 - Y5); g5b = central(lambda: float(0.5 * ((X5 @ W5c - Y5) ** 2).sum()), [W5c := W5.copy()])[0]
two('homework regression gradient', g5, g5b, 1e-8); E('homework', 'items[4].widget.answer', g5[1, 0]); E('homework', 'items[4].widget.wrong[1].value', g5[0, 0])
# problems-4
X1 = np.array([[1, 2], [0, -1], [2, 1]], float); W1p = np.array([[1, 0.5], [-2, 1]]); G1 = np.array([[0.5, -1], [1.5, 0], [-0.5, 2]])
E('problems', 'items[0].parts[0].widget.answer', (X1 @ W1p).size); E('problems', 'items[0].parts[1].widget.answer', (X1.T @ G1)[0, 1]); E('problems', 'items[0].parts[1].widget.wrong[1].value', (X1.T @ G1)[0, 0])
E('problems', 'items[0].parts[2].widget.answer', G1[:, 1].sum()); E('problems', 'items[0].parts[3].widget.answer', (G1 @ W1p.T)[2, 0]); E('problems', 'items[0].parts[3].widget.wrong[0].value', (G1 @ W1p)[2, 0])
pb = softmax(np.log([5.0, 3.0, 2.0])); E('problems', 'items[1].parts[0].widget.answer', round(pb[2], 6))
E('problems', 'items[1].parts[1].widget.answer', round(-math.log(pb[2]), 4)); E('problems', 'items[1].parts[1].widget.wrong[0].value', round(-math.log2(0.2), 4)); E('problems', 'items[1].parts[1].widget.wrong[1].value', round(-math.log(0.5), 4))
E('problems', 'items[1].parts[2].widget.answer', round(pb[2] - 1, 6)); E('problems', 'items[1].parts[3].widget.answer', round((pb[2] - 1) / 4, 6))
E('problems', 'items[1].parts[4].widget.answer', round(math.log(2) - 0.5 * (pb[2] - 1) / 4, 4)); E('problems', 'items[1].parts[4].widget.wrong[1].value', round(math.log(2) - 0.5 * (pb[2] - 1), 4))
X3 = np.array([[2.0, 0], [0, 1]]); W3t = Tensor(np.zeros((2, 2))); L3 = cross_entropy(Tensor(X3) @ W3t, [0, 1]); L3.backward()
E('problems', 'items[2].parts[0].widget.answer', round(L3.item(), 4)); E('problems', 'items[2].parts[0].widget.wrong[0].value', round(2 * L3.item(), 4))
E('problems', 'items[2].parts[1].widget.answer', float(W3t.grad[0, 0])); sgd_step([W3t], 1.0); E('problems', 'items[2].parts[2].widget.answer', float(W3t.data[0, 0]))
E('problems', 'items[2].parts[3].question', '0.5 & -0.5 \\\\ -0.25 & 0.25'); lv.claim(np.allclose(W3t.data, [[0.5, -0.5], [-0.25, 0.25]]), 'problems 3: W after the step')
newL = cross_entropy(Tensor(X3) @ W3t, [0, 1]).item(); newB = (math.log(1 + math.exp(-2)) + math.log(1 + math.exp(-0.5))) / 2
two('problems 3 new loss', newL, newB, 1e-12); E('problems', 'items[2].parts[3].widget.answer', round(newL, 4)); E('problems', 'items[2].parts[3].widget.wrong[0].value', round(math.log(1 + math.exp(-2)), 4))

# =================== 4. every code widget: solution, starter, mutants ===================
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
            sys.path.insert(0, d); sys.modules.pop('autograd', None)
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


old = sys.getrecursionlimit()
nw = nm = 0
for fid, doc in lv.files.items():
    units = doc.get('screens', []) + doc.get('items', [])
    for u in units:
        w = u.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        sys.setrecursionlimit(3000)  # the app's limit
        nw += 1
        lv.claim(first_fail(w, w['solution']) == 0, f'{fid} {u.get("title") or u.get("id")}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{fid} {u.get("title") or u.get("id")}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{fid}: at least two mutants')
        for m in w.get('mutants', []):
            nm += 1
            got = first_fail(w, m['source'])
            lv.claim(got == m['test'], f'{fid} mutant "{m["symptom"][:50]}" first fails test {m["test"]} (got {got})')
sys.setrecursionlimit(old)
print(f'code widgets {nw}, mutants {nm}')
sys.modules['autograd'] = ag
lv.check_wrongs()
lv.report()
