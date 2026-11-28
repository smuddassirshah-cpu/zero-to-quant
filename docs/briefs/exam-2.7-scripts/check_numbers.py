"""Recompute every number stated in app/content/exams/topic-2.7.json by a second route and assert it at its path.

Route A is build.py (floats and closed forms). Route B here is independent: exact Fractions for every sum, product and
chance the data allow, brute-force counting for the layer arithmetic, numpy.linalg for the eigen and graph items, central
differences and the shipped autograd.py for the gradients, a backward interval walk for the receptive field, and both code
items run in CPython as the page runs them (one namespace, prelude, then the code, then each case's setup and call in order,
judged by the engine's own __zq_judge read from code.js). Their expects are recomputed by the shipped modules
cnn_ops_l3.cnn_logits and seq_ops_l3.attention. The solution passes every hidden test and example, the starter fails every
test, each mutant first fails its named test, and each byKey test line is some mutant's first failure.
Coverage runs strict: every number on screen is compared or marked literal with a reason.
Run through the CI runner: node tools/run-number-scripts.mjs --python <venv> --only exam-2.7
"""
import json
import math
import os
import re
import signal
import sys
import time
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', '..', 'app')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, _walk, ZQ_LIB  # noqa: E402

EXAM = os.path.join(APP, 'content', 'exams', 'topic-2.7.json')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, DATA)
_here0 = os.getcwd()
os.chdir(DATA)                       # cnn_ops_l3.load_split reads its file by bare name
import autograd as AG  # noqa: E402  the shipped modules, read only
import cnn_ops_l3 as CNN  # noqa: E402
import seq_ops_l3 as SEQ  # noqa: E402
os.chdir(_here0)


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam"), coverage strict."""

    def __init__(self, path):
        self.course, self.n, self.results, self.coverage = 'exam', 0, [], 'strict'
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = doc['items']
idx = {it['id']: k for k, it in enumerate(items)}


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def key(iid, value, part=None, nd=None):
    w = node(W(iid, part))
    v = float(value)
    want = round(v, nd) if nd is not None else v
    ok = abs(w['answer'] - want) <= 1e-9 and abs(w['answer'] - v) <= w['tol']['abs'] + 1e-12
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {want!r}', '' if ok else 'route B differs')


CHECKED = set()


def wrong(iid, wid, value, part=None):
    CHECKED.add((iid, part, wid))
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - float(value)) <= max(hit[0]['tol']['abs'], 1e-12)
    ex._rec(ok, f'{iid} wrong "{wid}" = {float(value)!r}', '' if ok else f'found {hit}')


def say(iid, path, value, part=None, nd=None):
    """A number stated in the item's text at `path` (None: anywhere in the item or part)."""
    v = float(value) if isinstance(value, F) else value
    if nd is not None:
        v = round(v, nd)
    base = P(iid, part)
    ex.expect('exam', base if path is None else f'{base}.{path}', v)


def correct_id(iid, part=None):
    return [o['id'] for o in node(W(iid, part))['options'] if o.get('correct')]


def sqrt(x):
    return math.sqrt(float(x))


# ------------------------------------------------------------------ difficulty 2
iid = 'e-misreads-allowed'
n, bar = 540, F(95, 100)
m = max(k for k in range(n + 1) if F(n - k, n) >= bar)          # count up: the most misreads that still meet the bar
key(iid, m)
wrong(iid, 'strict', max(k for k in range(n + 1) if F(n - k, n) > bar))
wrong(iid, 'right', n - m)
wrong(iid, 'share', 1 - bar)
for v in (540, 0.95):
    say(iid, 'prose', v)
for v in (540, 0.05, 27, 513, 0.95):
    say(iid, 'feedback.correct', v)
    say(iid, 'explain.text', v) if v != 0.05 else None
os.chdir(DATA)
_split = CNN.load_split()
_exitp = CNN.load_weights('cnn-w-exit.json')
os.chdir(_here0)
X_te, y_te = _split[4], _split[5]
_pred = CNN.predict(CNN.cnn_logits, _exitp, X_te)
n_wrong_exit = int((_pred != y_te).sum())
ex.claim(n_wrong_exit == 8 and len(y_te) == 540, 'e-misreads-allowed: the exit net misreads 8 of the 540 (cnn_ops_l3)', covers=[n_wrong_exit])

iid = 'e-seeds-for-se'
s, se = F(3, 100), F(5, 1000)
nn = next(k for k in range(1, 1000) if s * s / k <= se * se)
key(iid, nn)
wrong(iid, 'root', sqrt(nn))
say(iid, 'prose', 0.03)
say(iid, 'question', 0.005)
for v in (0.03, 0.005, 6, 36):
    say(iid, 'feedback.correct', v)
ex.claim(s / 6 == se, 'e-seeds-for-se: 0.03/6 = 0.005', covers=[0.03, 6, 0.005, 36])

iid = 'e-repeated-lookup'
looks = [4, 1, 4]
G = [(F(1, 2), -1), (2, F(3, 10)), (F(-2, 10), F(6, 10))]
g4 = sum(G[k][0] for k, r_ in enumerate(looks) if r_ == 4)
key(iid, g4, nd=4)
wrong(iid, 'last', G[2][0])
wrong(iid, 'first', G[0][0])
wrong(iid, 'mean', g4 / 2)
wrong(iid, 'row1', G[1][0])
for v in (0.5, -1, 2, 0.3, -0.2, 0.6):
    say(iid, 'prose', v)
say(iid, 'feedback.correct', 0.3)
say(iid, 'explain.text', 0.3)

iid = 'e-he-for-a-conv'
fan = int(np.prod((16, 3, 3)))
key(iid, sqrt(F(2, fan)), nd=4)
wrong(iid, 'lecun', sqrt(F(1, fan)))
wrong(iid, 'fan9', sqrt(F(2, 9)))
wrong(iid, 'var', F(2, fan))
for v in (144, 0.1179):
    say(iid, 'feedback.correct', v)
    say(iid, 'explain.text', v)
say(iid, 'feedback.byKey.lecun', 144)
say(iid, 'feedback.byKey.var', 144)
say(iid, 'feedback.byKey.fan9', 144)


def kl2(m1, s1, m2, s2):
    """KL(N(m1, s1^2) || N(m2, s2^2)) by the two-normal formula (route B for the one-coordinate closed form)."""
    return math.log(s2 / s1) + (s1 * s1 + (m1 - m2) ** 2) / (2 * s2 * s2) - 0.5


iid = 'e-kl-wide-code'
kl = kl2(0, 2, 0, 1)
key(iid, kl, nd=3)
wrong(iid, 'nolog', F(3, 2))
wrong(iid, 'sd', 0.5 * (2 - 1) - 0.5 * math.log(2))
wrong(iid, 'logsd', 0.5 * 3 - 0.5 * math.log(2))
say(iid, 'feedback.correct', round(math.log(4), 3))
say(iid, 'feedback.correct', round(kl, 3))
say(iid, 'explain.text', round(kl, 3))

iid = 'e-gradient-kept'
w = F(92, 100)
key(iid, w ** 25, nd=4)
wrong(iid, 'linear', 1 - 25 * (1 - w))
wrong(iid, 'one-fewer', w ** 24)
say(iid, 'prose', 0.92)
say(iid, 'feedback.correct', round(float(w ** 25), 4))
say(iid, 'feedback.byKey.linear', 0.08)
say(iid, 'explain.text', round(float(w ** 25), 4))
ex.claim(round(float(w ** 25) * 100) == 12, 'e-gradient-kept: 0.1244 is about 12%', covers=['12%'])

# ------------------------------------------------------------------ difficulty 3
iid = 'e-adam-tiny-gradient'
eta, g, eps = F(1, 100), F(1, 10 ** 8), F(1, 10 ** 8)
mh = (F(1, 10) * g) / (1 - F(9, 10))               # corrected first moment: g exactly
vh = (F(1, 1000) * g * g) / (1 - F(999, 1000))     # corrected second moment: g^2 exactly
ex._rec(mh == g and vh == g * g, 'e-adam-tiny-gradient: the corrections give g and g^2 exactly', '')
key(iid, eta * mh / (g + eps), nd=6)                # sqrt(vh) = g exactly
wrong(iid, 'noeps', eta * mh / g)
wrong(iid, 'sgd', eta * g)
wrong(iid, 'raw', float(eta) * float(F(1, 10) * g) / (math.sqrt(float(F(1, 1000) * g * g)) + float(eps)))
for v in ('10^{-8}', 0.01, 0.9, 0.999):
    say(iid, 'prose', v)
say(iid, 'feedback.correct', 0.005)
say(iid, 'feedback.byKey.raw', 0.1)
say(iid, 'feedback.byKey.raw', 0.001)
say(iid, 'explain.text', 0.005)

iid = 'e-scaled-warmup'
peak = F(5, 100) * F(512, 128)
rate = peak * F(10, 40)
key(iid, rate, nd=6)
wrong(iid, 'noscale', F(5, 100) * F(10, 40))
wrong(iid, 'nowarm', peak)
wrong(iid, 'sqrt', 0.05 * sqrt(F(512, 128)) * 10 / 40)
for v in (128, 0.05, 512, 40):
    say(iid, 'prose', v)
for v in (0.05, 512, 128, 0.2, 10, 40):
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.byKey.sqrt', 0.1)
say(iid, 'feedback.byKey.sqrt', 4)
say(iid, 'explain.text', 0.05)
say(iid, 'explain.text', 0.2)

iid = 'e-relu-variance'
eh2 = F(3, 2) / 2
key(iid, 200 * F(8, 100) ** 2 * eh2, nd=2)
wrong(iid, 'nohalf', 200 * F(8, 100) ** 2 * F(3, 2))
wrong(iid, 'sd', 200 * F(8, 100) * eh2)
for v in (1.5, 200, 0.08):
    say(iid, 'prose', v)
for v in (1.5, 0.75, 200, 0.08, 0.96):
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.byKey.sd', 0.0064)
say(iid, 'explain.text', 0.96)

iid = 'e-stop-then-ridge'
Ls = [F(x) for x in node(P(iid) + '.prose').split('step 0: ')[1].split('.')[0].replace(' ', '').split(',')] if False else None
Ls = [F(90, 100), F(70, 100), F(58, 100), F(55, 100), F(56, 100), F(53, 100), F(52, 100), F(54, 100), F(55, 100), F(57, 100)]
for v in Ls:
    say(iid, 'prose', v)
since, best_i, stop_i = 0, 0, None                 # count evaluations since the last new best
for i in range(1, len(Ls)):
    if Ls[i] < min(Ls[:i]):
        best_i, since = i, 0
    else:
        since += 1
    if since == 3:
        stop_i = i
        break
key(iid, stop_i, part=0)
wrong(iid, 'best', best_i, part=0)
wrong(iid, 'p2', best_i + 2, part=0)
first_rise = next(i for i in range(1, len(Ls)) if Ls[i] > Ls[i - 1])
wrong(iid, 'first-rise', first_rise, part=0)
eta, every = F(5, 1000), 50
key(iid, 1 / (eta * best_i * every), part=1, nd=4)
wrong(iid, 'stopstep', 1 / (eta * stop_i * every), part=1)
wrong(iid, 'prod', eta * best_i * every, part=1)
wrong(iid, 'evals', 1 / (eta * best_i), part=1)
say(iid, 'prose', 0.005)
say(iid, 'prose', 50)
say(iid, 'feedback.correct', 0.52, part=0)
for v in (300, 0.005, 0.6667):
    say(iid, 'feedback.correct', v, part=1)
say(iid, 'feedback.byKey.stopstep', stop_i * every, part=1)
say(iid, 'feedback.byKey.stopstep', best_i * every, part=1)
say(iid, 'feedback.byKey.evals', best_i * every, part=1)

iid = 'e-min-norm-three'
A = np.array([[1.0, 2.0, 2.0]])
wmn = np.linalg.pinv(A) @ np.array([18.0])
key(iid, wmn[1], nd=4)
wrong(iid, 'equal', F(18, 5))
wrong(iid, 'one', F(18, 2))
wrong(iid, 'nonorm', 18 * 2)
say(iid, 'prose', 18)
nrm = float(np.linalg.norm(wmn))
ex.claim(abs(nrm - 6) < 1e-12 and np.allclose(wmn, [2, 4, 4]), 'e-min-norm-three: the fit is (2, 4, 4) with norm 6', covers=[6, 2, 4])
say(iid, 'feedback.byKey.equal', 3.6)
say(iid, 'feedback.byKey.one', 9)
say(iid, 'feedback.byKey.nonorm', 1 * 18 + 2 * 36 + 2 * 36)
say(iid, 'feedback.byKey.nonorm', 36)

iid = 'e-paired-sd'
sa, sb, rho = F(40, 1000), F(45, 1000), F(9, 10)
v_ = sa * sa + sb * sb - 2 * rho * sa * sb
key(iid, sqrt(v_), nd=4)
wrong(iid, 'indep', sqrt(sa * sa + sb * sb))
wrong(iid, 'half', sqrt(sa * sa + sb * sb - rho * sa * sb))
wrong(iid, 'nosqrt', v_)
for v in (0.040, 0.045, 0.9):
    say(iid, 'prose', v)
for v in (sa * sa, sb * sb, v_, round(sqrt(v_), 4)):
    say(iid, 'feedback.correct', v)
say(iid, 'explain.text', round(sqrt(sa * sa + sb * sb), 4))
say(iid, 'explain.text', round(sqrt(v_), 4))


def receptive(layers):
    """Walk one output back through the layers: an output interval [lo, hi] reads inputs [s lo, s hi + k - 1]."""
    lo, hi = 0, 0
    for k, s_ in reversed(layers):
        lo, hi = s_ * lo, s_ * hi + k - 1
    return hi - lo + 1


iid = 'e-receptive-field'
layers = [(3, 1), (2, 2), (3, 1), (3, 1)]
key(iid, receptive(layers))
wrong(iid, 'nostride', receptive([(k, 1) for k, _ in layers]))
wrong(iid, 'sum-k', sum(k for k, _ in layers))
say(iid, 'feedback.correct', 12)
say(iid, 'explain.text', 12)
ex.claim(receptive(layers[2:]) == 5 and receptive([(3, 1), (2, 2), (3, 1)]) - receptive([(3, 1), (2, 2)]) == 4,
         'e-receptive-field: after the pool each 3 by 3 conv adds 4 pixels, not 2', covers=[4])

iid = 'e-scaled-attention'
q = [1, -1, 2, 0]
Ks = [(2, 0, 1, 1), (0, 2, 1, 0), (1, 1, 0, 3)]
Vs = [10, -5, 3]
raw = [sum(a * b for a, b in zip(q, k_)) for k_ in Ks]
ex._rec(raw == [4, 0, 0], 'e-scaled-attention: raw scores 4, 0, 0', str(raw))


def soft(sc):
    m_ = max(sc)
    e_ = [math.exp(x - m_) for x in sc]
    return [x / sum(e_) for x in e_]


a_ = soft([x / 2 for x in raw])
ex._rec(abs(a_[0] - 1 / (1 + 2 * math.exp(-2))) < 1e-15, 'e-scaled-attention: weight 1 is 1/(1 + 2e^-2)', '')
key(iid, a_[0], part=0, nd=4)
wrong(iid, 'raw', soft(raw)[0], part=0)
wrong(iid, 'byd', soft([x / 4 for x in raw])[0], part=0)
wrong(iid, 'third', F(1, 3), part=0)
out0 = sum(x * y for x, y in zip(a_, Vs))
out1 = sum(x * y for x, y in zip(a_, [10, -4, 3]))
key(iid, out1 - out0, part=1, nd=4)                # the move, by differencing two outputs
wrong(iid, 'one', 1, part=1)
wrong(iid, 'first', a_[0], part=1)
wrong(iid, 'third', F(1, 3), part=1)
for v in (10, -5, 3):
    say(iid, 'prose', v)
say(iid, 'feedback.correct', round(a_[0], 4), part=0)
say(iid, 'question', round(a_[0], 4), part=1)
say(iid, 'question', round(a_[1], 4), part=1)
say(iid, 'feedback.correct', round(a_[1], 4), part=1)
say(iid, 'explain.text', round(soft(raw)[0], 4))

iid = 'e-pe-offset'


def pe(t):
    return np.array([math.sin(t), math.cos(t), math.sin(t / 100), math.cos(t / 100)])


dots = [float(pe(t) @ pe(t + 2)) for t in (0.0, 0.7, 5.0, 31.0)]
ex._rec(max(dots) - min(dots) < 1e-12, 'e-pe-offset: the dot product is the same at t = 0, 0.7, 5 and 31', str(dots))
key(iid, dots[1], nd=4)
wrong(iid, 'one-pair', math.sin(0.7) * math.sin(2.7) + math.cos(0.7) * math.cos(2.7))
wrong(iid, 'deg', math.cos(math.radians(2)) + math.cos(math.radians(0.02)))
wrong(iid, 'self', float(pe(0.7) @ pe(0.7)))
say(iid, 'feedback.correct', round(math.cos(2), 4))
say(iid, 'feedback.correct', round(math.cos(0.02), 4))
say(iid, 'feedback.correct', round(dots[1], 4))
say(iid, 'feedback.correct', 0.02)
say(iid, 'feedback.byKey.one-pair', round(math.cos(0.02), 4))
say(iid, 'explain.text', round(dots[1], 4))
say(iid, 'prose', 100)


def block_shapes(d, mlp, heads=1, bias=True):
    """The arrays of one pre-norm block, by name and shape (route B counts their sizes)."""
    sh = {}
    for nm in ('q', 'k', 'v', 'o'):
        sh[f'W{nm}'] = (d, d)
        if bias:
            sh[f'b{nm}'] = (d,)
    sh['W1'], sh['b1'], sh['W2'], sh['b2'] = (d, mlp), (mlp,), (mlp, d), (d,)
    for nm in ('ln1', 'ln2'):
        sh[f'{nm}_g'], sh[f'{nm}_b'] = (d,), (d,)
    return sh


def size(sh):
    return sum(int(np.prod(s_)) for s_ in sh.values())


iid = 'e-model-count-80'
d, Vt, C = 80, 100, 16
blk = block_shapes(d, 320)
model = dict(blk)
model.update({'E': (Vt, d), 'P': (C, d), 'lnf_g': (d,), 'lnf_b': (d,), 'U': (d, Vt), 'c': (Vt,)})
tot = size(model)
key(iid, tot)
wrong(iid, 'tied', tot - Vt * d)
wrong(iid, 'nopos', tot - C * d)
wrong(iid, 'nobias', tot - Vt)
att = size({k_: v for k_, v in blk.items() if k_[1] in 'qkvo'})
wrong(iid, 'heads', tot - att + 4 * att)
mlp_ = size({k_: blk[k_] for k_ in ('W1', 'b1', 'W2', 'b2')})
for v in (att, mlp_, 4 * d, size(blk), Vt * d, C * d, 2 * d, d * Vt + Vt, tot):
    say(iid, 'feedback.correct', v)
for v in (100, 16, 80, 320):
    say(iid, 'prose', v)
say(iid, 'explain.text', tot)
say(iid, 'explain.text', 320)
ex.claim(round(100 * size(blk) / tot) == 82, 'e-model-count-80: the block is 82% of the model', covers=['82%'])

iid = 'e-width-doubling'
c64, c128 = size(block_shapes(64, 256)), size(block_shapes(128, 512))
ex._rec(c64 == 49984, 'e-width-doubling: the block at d = 64 holds 49,984 (shapes summed)', str(c64))
key(iid, c128 / c64, nd=2)
wrong(iid, 'two', 2)
wrong(iid, 'four', 4)
wrong(iid, 'eight', 8)
say(iid, 'prose', 49984)
say(iid, 'prose', 64)
say(iid, 'feedback.correct', c128)
say(iid, 'feedback.correct', c64)
say(iid, 'feedback.correct', round(c128 / c64, 2))
say(iid, 'explain.text', round(c128 / c64, 2))
ex.claim(all(size(block_shapes(dd, 4 * dd)) == 12 * dd * dd + 13 * dd for dd in (8, 64, 80, 128)),
         'e-width-doubling: a block holds 12d^2 + 13d', covers=[12, 13])

iid = 'e-distance-to-cosine'
th = 2 * math.asin(0.3)                             # unit rows 0.6 apart: chord 2 sin(theta/2) = 0.6
u_, v2 = np.array([1.0, 0.0]), np.array([math.cos(th), math.sin(th)])
ex._rec(abs(np.linalg.norm(u_ - v2) - 0.6) < 1e-12, 'e-distance-to-cosine: the two unit rows lie 0.6 apart', '')
key(iid, float(u_ @ v2), nd=2)
wrong(iid, 'lin', F(4, 10))
wrong(iid, 'sq', 1 - F(36, 100))
wrong(iid, 'half', F(7, 10))
say(iid, 'prose', 0.6)
say(iid, 'feedback.correct', 0.36)
say(iid, 'feedback.correct', 0.82)
say(iid, 'explain.text', 0.6)
say(iid, 'explain.text', 0.82)

iid = 'e-one-code-rebuild'
Sig = np.array([[3.0, 1.0], [1.0, 3.0]])
lam, vec = np.linalg.eigh(Sig)
u_ = vec[:, 1]
key(iid, np.trace(Sig) - u_ @ Sig @ u_, part=0, nd=4)
wrong(iid, 'kept', u_ @ Sig @ u_, part=0)
wrong(iid, 'total', np.trace(Sig), part=0)
wrong(iid, 'diag', Sig[0, 0], part=0)
x = np.array([2.0, -1.0])
z = x @ u_
key(iid, float(np.sum((x - z * u_) ** 2)), part=1, nd=4)
wrong(iid, 'code', z * z, part=1)
wrong(iid, 'whole', x @ x, part=1)
ex.claim(np.allclose(sorted(lam), [2, 4]), 'e-one-code-rebuild: the eigenvalues are 4 and 2', covers=[4, 2])
say(iid, 'feedback.correct', round(abs(z), 4), part=1)
say(iid, 'feedback.correct', 0.5, part=1)
say(iid, 'feedback.correct', 1.5, part=1)
say(iid, 'feedback.correct', 4.5, part=1)
ex.claim(np.allclose(np.abs(z * u_), [0.5, 0.5]) and np.allclose(np.abs(x - z * u_), [1.5, 1.5]),
         'e-one-code-rebuild: the rebuild is (0.5, 0.5) and the gap 1.5 a coordinate', covers=[0.5, 1.5])

iid = 'e-kl-two-coords'
mus, ells = [0.8, -0.6], [math.log(2), math.log(0.25)]
klc = [kl2(m_, math.exp(l_ / 2), 0, 1) for m_, l_ in zip(mus, ells)]
key(iid, sum(klc), nd=3)
wrong(iid, 'nolog', sum(0.5 * (m_ * m_ + math.exp(l_) - 1) for m_, l_ in zip(mus, ells)))
wrong(iid, 'first', klc[0])
wrong(iid, 'sd', sum(0.5 * (m_ * m_ + math.exp(l_ / 2) - 1 - l_ / 2) for m_, l_ in zip(mus, ells)))
for v in (0.8, -0.6, 0.25):
    say(iid, 'prose', v)
for v in (0.64, 2, 0.693, round(klc[0], 3), 0.36, 0.25, 1.386, round(klc[1], 3), round(sum(klc), 3)):
    say(iid, 'feedback.correct', v)
say(iid, 'explain.text', round(sum(klc), 3))
say(iid, 'feedback.byKey.nolog', 1.386)

iid = 'e-x0-from-noise'
ab, xt, eh = F(36, 100), F(11, 10), F(1, 2)
ra, rb = F(6, 10), F(8, 10)                         # exact square roots of 0.36 and 0.64
ex._rec(ra * ra == ab and rb * rb == 1 - ab, 'e-x0-from-noise: sqrt(0.36) = 0.6 and sqrt(0.64) = 0.8', '')
x0 = (xt - rb * eh) / ra
ex._rec(x0 == F(7, 6), 'e-x0-from-noise: x0 estimate is 7/6', str(x0))
key(iid, x0, nd=4)
wrong(iid, 'noroot', (xt - (1 - ab) * eh) / ab)
wrong(iid, 'nodiv', xt - rb * eh)
wrong(iid, 'sign', (xt + rb * eh) / ra)
for v in (0.36, 1.1, 0.5):
    say(iid, 'prose', v)
for v in (1.1, 0.8, 0.5, 0.7, 0.6, round(float(x0), 4)):
    say(iid, 'feedback.correct', v)
say(iid, 'explain.text', round(float(x0), 4))

iid = 'e-settle-path'
Ap = np.zeros((4, 4))
for i_, j_ in ((0, 1), (1, 2), (2, 3)):
    Ap[i_, j_] = Ap[j_, i_] = 1
At = Ap + np.eye(4)
Pm = At / At.sum(axis=1, keepdims=True)
xs = np.linalg.matrix_power(Pm, 4000) @ np.array([4.0, 0, 0, 0])
ex._rec(np.ptp(xs) < 1e-12, 'e-settle-path: every firm settles on one value', str(xs))
key(iid, xs[0], nd=4)
wrong(iid, 'mean', F(4, 4))
P0 = Ap / Ap.sum(axis=1, keepdims=True)
x_even = np.linalg.matrix_power(P0, 4000) @ np.array([4.0, 0, 0, 0])
x_odd = P0 @ x_even
wrong(iid, 'noloop', float(Ap.sum(axis=1)[0] * 4 / Ap.sum()))
ex.claim(abs((x_even + x_odd).mean() / 2 - Ap.sum(axis=1)[0] * 4 / Ap.sum()) < 1e-9,
         'e-settle-path: without loops the walk alternates around the degree-weighted mean 0.6667', covers=[0.6667])
say(iid, 'prose', 4)
say(iid, 'feedback.correct', 0.8)
ex.claim(list(At.sum(axis=1)) == [2, 3, 3, 2] and At.sum() == 10, 'e-settle-path: degrees with loops 2, 3, 3, 2, total 10',
         covers=[2, 3, 10])
say(iid, 'explain.text', 0.8)
say(iid, 'explain.text', 10)

# ------------------------------------------------------------------ difficulty 4
iid = 'e-layernorm-backward'
xv = np.array([1.0, 3.0, 5.0, 7.0])
dvec = np.array([1.0, 0.0, 0.0, 0.0])


def ln_loss(x_):
    return float(dvec @ ((x_ - x_.mean()) / np.sqrt(x_.var())))


hh = 1e-6
num_g = np.array([(ln_loss(xv + hh * e_) - ln_loss(xv - hh * e_)) / (2 * hh) for e_ in np.eye(4)])
key(iid, num_g[0], part=0, nd=4)
wrong(iid, 'plain', 1 / math.sqrt(5), part=0)
wrong(iid, 'centred', (1 - F(1, 4)) / math.sqrt(5), part=0)
key(iid, round(float(num_g.sum()), 6) + 0.0, part=1)
wrong(iid, 'd', dvec.sum(), part=1)
wrong(iid, 's', 1 / math.sqrt(5), part=1)
ex.claim(xv.mean() == 4 and xv.var() == 5, 'e-layernorm-backward: mean 4 and variance 5', covers=[4, 5])
xh = (xv - 4) / math.sqrt(5)
mdx = float((dvec * xh).mean())
ex.claim(abs(mdx + 3 / (4 * math.sqrt(5))) < 1e-15 and abs(xh[0] * mdx - 0.45) < 1e-15,
         'e-layernorm-backward: mean(d xhat) = -3/(4 sqrt 5) and xhat_1 times it is 0.45', covers=[0.45, 0.75, 0.25])
say(iid, 'feedback.correct', 0.25, part=0)
say(iid, 'feedback.correct', 0.75, part=0)
say(iid, 'feedback.correct', 0.45, part=0)
say(iid, 'feedback.correct', round(num_g[0], 4), part=0)
say(iid, 'feedback.byKey.centred', 0.45, part=0)

iid = 'e-two-kernels-in-turn'


def slide(x_, k_):
    return np.array([sum(k_[j] * x_[t + j] for j in range(len(k_))) for t in range(len(x_) - len(k_) + 1)])


basis = [slide(slide(e_, [-1, 1]), [0.5, 0.5])[0] for e_ in np.eye(3)]
ex._rec(np.allclose(basis, [-0.5, 0, 0.5]), 'e-two-kernels-in-turn: the two slides act as (-0.5, 0, 0.5)', str(basis))
opts = {o['id']: o['text'] for o in node(W(iid, 0))['options']}
ex._rec(correct_id(iid, 0) == ['full'] and opts['full'] == '$(-0.5, 0, 0.5)$', 'e-two-kernels-in-turn: the key is (-0.5, 0, 0.5)', '')
xr = np.random.default_rng(3).standard_normal(30)
ex._rec(np.allclose(slide(slide(xr, [-1, 1]), [0.5, 0.5]), slide(xr, basis)), 'e-two-kernels-in-turn: one slide of the combined kernel matches on 30 closes', '')
ex._rec(opts['prod'] == '$(-0.5, 0.5)$' and opts['flip'] == '$(0.5, 0, -0.5)$' and opts['nohalf'] == '$(-1, 0, 1)$',
        'e-two-kernels-in-turn: distractors are the entrywise product, the reversed kernel and the kernel without 0.5', '')
nout = len(slide(slide(xr, [-1, 1]), [0.5, 0.5]))
key(iid, nout, part=1)
wrong(iid, 'one', len(slide(xr, [-1, 1])), part=1)
wrong(iid, 'sum', 30 - 2 - 2 + 1, part=1)
wrong(iid, 'all', 30, part=1)
say(iid, 'prose', 0.5)
say(iid, 'feedback.correct', 0.5, part=0)
say(iid, 'feedback.correct', 28, part=1)
say(iid, 'question', 30, part=1)
ex.claim(len(slide(xr, [1, 1, 1])) == nout, 'e-two-kernels-in-turn: one slide of length 3 gives the same count', covers=[3])

iid = 'e-conv-layer-costs'
nside, k, p_, s_, cin, Fn = 20, 5, 2, 2, 3, 12
starts = list(range(0, nside + 2 * p_ - k + 1, s_))  # every start of the window along one side
o = len(starts)
key(iid, o, part=0)
wrong(iid, 'nofloor', F(nside + 2 * p_ - k, s_) + 1, part=0)
wrong(iid, 'same', nside, part=0)
wrong(iid, 'nopad', len(range(0, nside - k + 1, s_)), part=0)
Wshape, bshape = (Fn, cin, k, k), (Fn,)
key(iid, int(np.prod(Wshape)) + Fn, part=1)
wrong(iid, 'nobias', int(np.prod(Wshape)), part=1)
wrong(iid, 'nocin', Fn * (k * k + 1), part=1)
macs = sum(1 for _ in starts for _ in starts for _ in range(Fn)) * cin * k * k
key(iid, macs, part=2)
wrong(iid, 'stride1', len(range(0, nside + 2 * p_ - k + 1)) ** 2 * Fn * cin * k * k, part=2)
wrong(iid, 'onech', o * o * Fn * k * k, part=2)
wrong(iid, 'params', int(np.prod(Wshape)) + Fn, part=2)
say(iid, 'feedback.correct', 9.5, part=0)
say(iid, 'feedback.byKey.nofloor', 9.5, part=0)
say(iid, 'feedback.byKey.nopad', 24, part=0)
say(iid, 'feedback.correct', 912, part=1)
say(iid, 'feedback.correct', 25, part=1)
for v in (75, 100, 90000):
    say(iid, 'feedback.correct', v, part=2)
say(iid, 'feedback.byKey.stride1', 400, part=2)
say(iid, 'feedback.byKey.onech', 75, part=2)
say(iid, 'feedback.byKey.params', 100, part=2)
ex.claim(len(range(0, nside + 2 * p_ - k + 1)) ** 2 == 400 and o * o == 100, 'e-conv-layer-costs: 400 positions at stride 1, 100 at stride 2',
         covers=[400, 100])

iid = 'e-gcn-hub'
names = ['H', 'A', 'B', 'C', 'D', 'E', 'F']
ix = {c_: i_ for i_, c_ in enumerate(names)}
Ag = np.zeros((7, 7))
for a_, b_ in (('H', 'A'), ('H', 'B'), ('H', 'C'), ('H', 'D'), ('H', 'E'), ('A', 'F')):
    Ag[ix[a_], ix[b_]] = Ag[ix[b_], ix[a_]] = 1
Atl = Ag + np.eye(7)
Dm = np.diag(1 / np.sqrt(Atl.sum(axis=1)))
Ah = Dm @ Atl @ Dm
key(iid, Ah[ix['A'], ix['H']], part=0, nd=3)
wrong(iid, 'noloop', 1 / math.sqrt(Ag.sum(axis=1)[ix['A']] * Ag.sum(axis=1)[ix['H']]), part=0)
wrong(iid, 'row', 1 / Atl.sum(axis=1)[ix['A']], part=0)
wrong(iid, 'noroot', 1 / (Atl.sum(axis=1)[ix['A']] * Atl.sum(axis=1)[ix['H']]), part=0)
hv = np.zeros(7)
hv[ix['A']], hv[ix['H']], hv[ix['F']] = 3, -1, 2
mix = float((Ah @ hv)[ix['A']])
key(iid, max(0.0, 1.5 * mix), part=1, nd=2)
wrong(iid, 'mean', 1.5 * (3 - 1 + 2) / 3, part=1)
wrong(iid, 'sum', 1.5 * (3 - 1 + 2), part=1)
reach = int(((np.linalg.matrix_power(Atl, 2))[ix['F']] > 0).sum())
key(iid, reach, part=2)
wrong(iid, 'onehop', int((Atl[ix['F']] > 0).sum()), part=2)
wrong(iid, 'all', 7, part=2)
ex.claim(Atl.sum(axis=1)[ix['A']] == 3 and Atl.sum(axis=1)[ix['H']] == 6 and Atl.sum(axis=1)[ix['F']] == 2,
         'e-gcn-hub: degrees with loops A 3, H 6, F 2', covers=[3, 6, 2, 18])
say(iid, 'feedback.correct', round(Ah[ix['A'], ix['H']], 3), part=0)
say(iid, 'feedback.correct', round(Ah[ix['A'], ix['H']], 3), part=1)
say(iid, 'feedback.correct', round(Ah[ix['A'], ix['F']] * 2, 3), part=1)
say(iid, 'feedback.correct', round(1 - round(Ah[ix['A'], ix['H']], 3) + round(2 * Ah[ix['A'], ix['F']], 3), 3), part=1)
say(iid, 'feedback.correct', round(1.5 * round(1 - round(Ah[ix['A'], ix['H']], 3) + round(2 * Ah[ix['A'], ix['F']], 3), 3), 2), part=1)
say(iid, 'feedback.correct', 1.5, part=1)
say(iid, 'question', 1.5, part=1)

iid = 'e-reverse-step'
beta, abar, xt, ehat, zz = 0.1, 0.5, 0.8, -0.6, 0.5
alpha = 1 - beta
xnew = xt / math.sqrt(alpha) - beta / (math.sqrt(alpha) * math.sqrt(1 - abar)) * ehat + math.sqrt(beta) * zz
key(iid, xnew, nd=3)
wrong(iid, 'noz', xnew - math.sqrt(beta) * zz)
wrong(iid, 'abar', xt / math.sqrt(abar) - beta / (math.sqrt(abar) * math.sqrt(1 - abar)) * ehat + math.sqrt(beta) * zz)
wrong(iid, 'noscale', xt / math.sqrt(alpha) - beta / math.sqrt(alpha) * ehat + math.sqrt(beta) * zz)
for v in (0.1, 0.5, 0.8, -0.6):
    say(iid, 'prose', v)
br = xt - beta / math.sqrt(1 - abar) * ehat
for v in (0.9, 0.8, 0.1, round(math.sqrt(1 - abar), 4), 0.6, round(br, 4), round(br / math.sqrt(alpha), 4), round(math.sqrt(beta) * zz, 4), round(xnew, 3)):
    say(iid, 'feedback.correct', v)
say(iid, 'feedback.byKey.noz', round(math.sqrt(beta) * zz, 4))
say(iid, 'explain.text', round(xnew, 3))

iid = 'e-ae-dropped-part'
Vm = np.array([[1, 1, 1], [1, -1, 0], [1, 1, -2]], dtype=float)
Vm = Vm / np.linalg.norm(Vm, axis=1, keepdims=True)
ex._rec(np.allclose(Vm @ Vm.T, np.eye(3)), 'e-ae-dropped-part: the three eigenvectors are orthonormal', '')
x = np.array([2.0, 0.0, -1.0])
Pk = Vm[:2].T @ Vm[:2]                              # projection on the kept plane
res = x - Pk @ x
key(iid, F(int(round(float(Vm[2] @ x * math.sqrt(6)))) ** 2, 6), nd=4)
ex._rec(abs(res @ res - 8 / 3) < 1e-12, 'e-ae-dropped-part: the residual of the projection has squared length 8/3', '')
wrong(iid, 'onecode', float(x @ x - (Vm[0] @ x) ** 2))
wrong(iid, 'whole', float(x @ x))
wrong(iid, 'kept', float((Pk @ x) @ (Pk @ x)))
say(iid, 'feedback.correct', 16)
say(iid, 'feedback.correct', 6)
say(iid, 'feedback.correct', round(8 / 3, 4))
say(iid, 'feedback.byKey.whole', 5)
say(iid, 'feedback.byKey.kept', '1/3')
ex.claim(abs(float((Vm[0] @ x) ** 2) - 1 / 3) < 1e-12 and abs(float((Vm[1] @ x) ** 2) - 2) < 1e-12,
         'e-ae-dropped-part: the kept parts are 1/3 and 2', covers=['1/3'])
say(iid, 'feedback.byKey.kept', 2)
say(iid, 'explain.text', round(8 / 3, 4))

iid = 'e-dropout-spread'
a, p = F(2), F(1, 5)
outcomes = [(1 - p, a / (1 - p)), (p, F(0))]
mean_ = sum(pr * v for pr, v in outcomes)
ex2 = sum(pr * v * v for pr, v in outcomes)
key(iid, mean_, part=0, nd=4)
wrong(iid, 'noscale', (1 - p) * a, part=0)
wrong(iid, 'surv', a / (1 - p), part=0)
key(iid, ex2 - mean_ ** 2, part=1, nd=4)
wrong(iid, 'noscale', a * a * p * (1 - p), part=1)
wrong(iid, 'second', ex2, part=1)
wrong(iid, 'p', a * a * p, part=1)
ex._rec(ex2 - mean_ ** 2 == a * a * p / (1 - p), 'e-dropout-spread: the variance is a^2 p/(1 - p)', '')
ex._rec(correct_id(iid, 2) == ['grows'] and all((a * a * q_ / (1 - q_)) > (a * a * (q_ - F(1, 100)) / (1 - q_ + F(1, 100))) for q_ in (F(1, 2), F(9, 10), F(99, 100))),
        'e-dropout-spread: 4p/(1 - p) keeps rising as p nears 1', '')
for v in (0.2, 0.8):
    say(iid, 'prose', v)
for v in (0.8, 0.2):
    say(iid, 'feedback.correct', v, part=0)
say(iid, 'feedback.byKey.noscale', 1.6, part=0)
say(iid, 'feedback.byKey.noscale', 0.8, part=0)
say(iid, 'feedback.byKey.surv', 2.5, part=0)
say(iid, 'feedback.correct', 0.8, part=1)
say(iid, 'feedback.correct', 2.5, part=1)
say(iid, 'feedback.correct', ex2, part=1)
say(iid, 'feedback.byKey.noscale', 0.2, part=1)
say(iid, 'feedback.byKey.noscale', 0.8, part=1)
say(iid, 'feedback.byKey.noscale', 0.64, part=1)
say(iid, 'feedback.byKey.second', 5, part=1)
say(iid, 'feedback.byKey.second', 4, part=1)
say(iid, 'feedback.byKey.p', 0, part=1) if False else None
ex.claim(a * a == 4 and 1 - p == F(4, 5), 'e-dropout-spread: a^2 = 4, which with p/(1 - p) gives 4p/(1 - p)', covers=[4])
say(iid, None, 0.5, part=2)

# ------------------------------------------------------------------ difficulty 5
iid = 'e-bptt-two-steps'
wT = AG.Tensor(np.array(0.5))
h = AG.Tensor(np.array(1.0))
for xin in (0.0, 0.2):
    h = (wT * h + xin).tanh()
h.backward()
h2_ag, g_ag = float(h.data), float(wT.grad)
key(iid, h2_ag, part=0, nd=4)
wrong(iid, 'notanh', 0.5 * (0.5 * 1 + 0) + 0.2, part=0)
wrong(iid, 'one-step', math.tanh(0.5), part=0)
H1, H2 = round(math.tanh(0.5), 4), round(h2_ag, 4)
say(iid, 'question', H1, part=1)
say(iid, 'question', H2, part=1)
fd = (math.tanh((0.5 + 1e-6) * math.tanh(0.5 + 1e-6) + 0.2) - math.tanh((0.5 - 1e-6) * math.tanh(0.5 - 1e-6) + 0.2)) / 2e-6
ex._rec(abs(fd - g_ag) < 1e-8, 'e-bptt-two-steps: autograd and central differences agree on dh2/dw', f'{fd} {g_ag}')
w_ = node(W(iid, 1))
ex._rec(abs(w_['answer'] - g_ag) <= w_['tol']['abs'], 'e-bptt-two-steps: the exact gradient lies inside the key band', '')
from_printed = (1 - H2 ** 2) * (H1 + 0.5 * (1 - H1 ** 2) * 1)
key(iid, from_printed, part=1, nd=4)
wrong(iid, 'last', (1 - H2 ** 2) * H1, part=1)
wrong(iid, 'noinner', (1 - H2 ** 2) * (H1 + 0.5), part=1)
wrong(iid, 'noouter', H1 + 0.5 * (1 - H1 ** 2), part=1)
GP = round(from_printed, 4)
say(iid, 'question', GP, part=2)
dL = 2 * (H2 - 1) * GP
key(iid, dL, part=2, nd=4)
wrong(iid, 'sign', -dL, part=2)
wrong(iid, 'nochain', 2 * (H2 - 1), part=2)
wrong(iid, 'half', (H2 - 1) * GP, part=2)
gc = dL * min(1.0, 0.5 / abs(dL))
key(iid, 0.5 - 0.2 * gc, part=3, nd=4)
wrong(iid, 'noclip', 0.5 - 0.2 * dL, part=3)
wrong(iid, 'sign', 0.5 + 0.2 * gc, part=3)
for v in (0.5, 0.2):
    say(iid, 'prose', v)
say(iid, 'feedback.correct', H1, part=0)
say(iid, 'feedback.correct', round(0.5 * H1, 4), part=0)
say(iid, 'feedback.correct', round(0.5 * H1 + 0.2, 4), part=0)
say(iid, 'feedback.correct', H2, part=0)
say(iid, 'feedback.correct', round(1 - H2 ** 2, 3), part=1)
say(iid, 'feedback.correct', round(H1 + 0.5 * (1 - H1 ** 2), 4), part=1)
say(iid, 'feedback.correct', GP, part=1)
say(iid, 'feedback.byKey.noinner', round(1 - H1 ** 2, 4), part=1)
say(iid, 'feedback.byKey.noouter', round(1 - H2 ** 2, 3), part=1)
say(iid, 'feedback.correct', round(H2 - 1, 4), part=2)
say(iid, 'feedback.correct', round(dL, 4), part=2)
say(iid, 'feedback.correct', round(abs(dL), 4), part=3)
say(iid, 'feedback.correct', round(0.5 - 0.2 * gc, 4), part=3)
say(iid, 'feedback.byKey.noclip', round(abs(dL), 4), part=3)
say(iid, 'question', 0.2, part=3)
say(iid, 'question', 0.5, part=3)

# ------------------------------------------------------------------ code items, run in CPython as the page runs them
with open(os.path.join(APP, 'js', 'engine', 'widgets', 'code.js'), encoding='utf8') as f:
    _js = f.read()
JUDGE_SRC = re.search(r'(def __zq_judge\(.*?)`;', _js, re.S).group(1)
_jns = {}
exec(JUDGE_SRC, _jns)
zq_judge = _jns['__zq_judge']


class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)
TIMES = {}


def run_page(src, w, cases, tag=None, cwd=None, swap=None):
    """One namespace: ZQ_LIB, the prelude, the code, then each case's setup and call in order. `swap` replaces names
    after the code loads (route B puts the shipped modules in place of the learner's functions)."""
    here = os.getcwd()
    if cwd:
        os.chdir(cwd)
    out = []
    try:
        ns = {'__learner_source__': src}
        exec(ZQ_LIB, ns)
        exec(w.get('prelude', ''), ns)
        try:
            exec(src, ns)
        except Exception:
            return ['load-error'] * len(cases)
        if swap:
            swap(ns)
        for k, c in enumerate(cases):
            signal.setitimer(signal.ITIMER_REAL, 5.0)
            try:
                t0 = time.perf_counter()
                if c.get('setup'):
                    exec(c['setup'], ns)
                got = eval(c['call'], ns)
                if tag:
                    TIMES[(tag, k + 1)] = time.perf_counter() - t0
                tol = c.get('tol')
                tl = (tol.get('rel', 0), tol.get('abs', 0)) if tol else None
                want = eval(c['expect'], {**ns})
                out.append('ok' if zq_judge(got, want, c.get('compare', 'equal'), tl) == 1.0 else 'fail')
            except TO:
                out.append('timeout')
            except Exception:
                out.append('error')
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
    finally:
        os.chdir(here)
    return out


def code_checks(iid, cwd=None, swap=None):
    w = node(W(iid))
    sol = run_page(w['solution'], w, w['tests'], tag=iid, cwd=cwd)
    ex._rec(all(r_ == 'ok' for r_ in sol), f'{iid}: solution passes all {len(sol)} hidden tests', str(sol))
    sol_ex = run_page(w['solution'], w, w['examples'], cwd=cwd)
    ex._rec(all(r_ == 'ok' for r_ in sol_ex), f'{iid}: solution passes the examples', str(sol_ex))
    st = run_page(w['starter'], w, w['tests'], cwd=cwd)
    ex._rec(all(r_ != 'ok' for r_ in st), f'{iid}: starter fails all {len(st)} hidden tests', str(st))
    ex._rec(f'runs {len(w["tests"])} hidden tests' in w['how'], f'{iid}: how names {len(w["tests"])} tests', '')
    ex._rec(len(w['mutants']) >= 2, f'{iid}: at least two mutants', '')
    for m_ in w['mutants']:
        res = run_page(m_['source'], w, w['tests'], cwd=cwd)
        first = next((k + 1 for k, r_ in enumerate(res) if r_ != 'ok'), None)
        ex._rec(first == m_['test'], f'{iid}: mutant first fails test {m_["test"]} ({m_["symptom"][:50]})', str(res))
    fbk = node(P(iid) + '.feedback').get('byKey', {})
    firsts = {m_['test'] for m_ in w['mutants']}
    for kk in fbk:
        n_ = int(kk.split('-')[1])
        ex._rec(1 <= n_ <= len(w['tests']), f'{iid}: byKey {kk} names a real test', '')
        ex._rec(n_ in firsts, f'{iid}: byKey {kk} is the first failure of some mutant, so a learner can reach it', '')
    for t_ in sorted(firsts):
        ex._rec(f'test-{t_}' in fbk, f'{iid}: test {t_}, some mutant\'s first failure, has a byKey line', '')
    if swap:
        rb = run_page('', w, w['tests'] + w['examples'], cwd=cwd, swap=swap)
        ex._rec(all(r_ == 'ok' for r_ in rb), f'{iid}: route B (the shipped modules) reproduces every expect', str(rb))
    slow = max(v for (t, _), v in TIMES.items() if t == iid)
    ex._rec(slow < (5 + w.get('budget', 0) / 1000) / 3, f'{iid}: the slowest case takes {slow:.3f} s, under a third of its limit', '')
    return w


def cnn_route_b(ns):
    """Replace the learner's two functions by the shipped cnn_ops_l3 (autograd Tensors)."""
    ns['cnn_logits_np'] = lambda params, X: CNN.cnn_logits([np.asarray(a, dtype=float) for a in params], np.asarray(X)).data
    ns['held_out_accuracy'] = lambda params, X, y: CNN.accuracy(CNN.cnn_logits, [np.asarray(a, dtype=float) for a in params],
                                                               np.asarray(X), np.asarray(y))


iid = 'e-cnn-exit'
wc = code_checks(iid, cwd=DATA, swap=cnn_route_b)
acc_b = CNN.accuracy(CNN.cnn_logits, _exitp, X_te, y_te)
ex._rec(abs(acc_b - 532 / 540) < 1e-15 and acc_b >= 0.95, 'e-cnn-exit: cnn_ops_l3 scores the exit net 532/540, above 0.95', str(acc_b))
say(iid, 'feedback.correct', 532)
say(iid, 'feedback.correct', round(acc_b, 4))
say(iid, 'feedback.correct', 0.95)
say(iid, 'explain.text', 532)
say(iid, 'question', 0.95)
say(iid, 'widget.how', 0.95)
say(iid, 'widget.how', '10^{-9}')
pre = wc['prelude']
pns = {}
os.chdir(DATA)
exec(pre, pns)
os.chdir(_here0)
ex._rec(pns['X_test'].shape == (540, 1, 8, 8) and np.array_equal(pns['X_test'], X_te) and np.array_equal(pns['y_test'], y_te),
        'e-cnn-exit: the prelude loads the same 540 held-out digits as cnn_ops_l3.load_split', '')
ex._rec([a_.shape for a_ in pns['EXIT']] == [(16, 1, 3, 3), (16,), (256, 10), (10,)], 'e-cnn-exit: EXIT shapes as the prose says', '')
for v in (540, 16, 256):
    say(iid, 'prose', v)
say(iid, 'feedback.byKey.test-1', 256)
ex._rec(np.allclose(pns['X_test'].max(), 1.0) and 16 * pns['X_test'].max() == 16, 'e-cnn-exit: grey levels are divided by 16', '')

iid = 'e-padded-heads'


def att_route_b(ns):
    """Replace the learner's function by the shipped seq_ops_l3 attention (masks as -inf, fully masked rows give zeros)."""
    def f(X, params, h, pad):
        X = np.asarray(X, dtype=float)
        T_, d_ = X.shape
        mask = np.where(np.tril(np.ones((T_, T_), dtype=bool)) & ~np.asarray(pad, dtype=bool)[None, :], 0.0, -np.inf)
        Q, K, V = (SEQ.split_heads(AG.Tensor(X @ params[k_]), h) for k_ in ('Wq', 'Wk', 'Wv'))
        return (SEQ.merge_heads(SEQ.attention(Q, K, V, mask)) @ AG.Tensor(params['Wo'])).data
    ns['padded_attention'] = f


with np.errstate(invalid='ignore'):
    wa = code_checks(iid, cwd=DATA, swap=att_route_b)
say(iid, 'widget.how', '10^{-9}')

# ------------------------------------------------------------------ exam-wide checks
allw = {(it['id'], None, w_['id']) for it in items if 'widget' in it for w_ in it['widget'].get('wrong', [])}
allw |= {(it['id'], k, w_['id']) for it in items for k, pt in enumerate(it.get('parts', [])) for w_ in pt['widget'].get('wrong', [])}
ex._rec(allw <= CHECKED, f'every one of the {len(allw)} numeric slips is recomputed', str(sorted(allw - CHECKED)))
ramp = {dd: sum(1 for it in items if it['difficulty'] == dd) for dd in (2, 3, 4, 5)}
ex._rec(ramp == {2: 6, 3: 16, 4: 7, 5: 3}, f'ramp {ramp} for 32 items', '')
pace = sum(it['pace'] for it in items)
ex._rec(pace / 60 <= doc['minutes'] - 5, f'paces add to {pace / 60:.1f} min, inside the {doc["minutes"]} minutes with slack', '')
ex.check_wrongs()
ex.report()
