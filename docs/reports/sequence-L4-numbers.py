"""Recompute every number stated in sequence level 4 (The transformer block) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only sequence-L4
(NumPy only; about a minute and a half with one BLAS thread; strict coverage; exits 0 when every check passes).
`--write` retrains the reversal model and rewrites app/content/data/ai/sequence-reverse.json (then exits).

The reversal model (2 pre-norm blocks, width 32, 4 heads, MLP 128, ReLU, vocabulary 11, context 12) is trained here with
autograd.py and seq_ops_l4.py, Adam with warm-up and cosine decay (nt_ops_l1), seed 0, 400 steps of 64 fresh sequences,
none from the 1,000 held out by default_rng(1). Route B for the model: a plain NumPy forward pass written below (no autograd)
reproduces seq_ops_l4's logits and stream; seeds 1 and 2 are retrained to assert the held-out threshold. The new module
seq_ops_l4.py is gradient-checked against central differences. Every code widget is run in CPython with the page's judge
(solution passes, starter fails, each mutant first fails its named test).
"""
import base64
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
from autograd import Tensor, _wrap, cross_entropy, grad_check  # noqa: E402
from nt_ops_l1 import adam_step, warmup_cosine  # noqa: E402
import seq_ops_l4 as S4  # noqa: E402

WFILE = os.path.join(DATA, 'sequence-reverse.json')

# ---------------- the reversal task and its model (trained here; --write ships the weights) ----------------
SEP, VOCAB, CTX, D, H, DM, NB = 10, 11, 12, 32, 4, 128, 2
STEPS, LR, WARM, BS = 400, 3e-3, 50, 64


def make(digits):
    """Rows of 12 input tokens (6 digits, the separator 10, the first 5 reversed digits) and 12 targets (-1 = not scored)."""
    digits = np.asarray(digits)
    n = len(digits)
    rev = digits[:, ::-1]
    X = np.concatenate([digits, np.full((n, 1), SEP), rev[:, :5]], 1)
    Y = np.concatenate([np.full((n, 6), -1), rev], 1)
    return X, Y


HELD = np.random.default_rng(1).integers(0, 10, (1000, 6))
HSET = set(map(tuple, HELD.tolist()))


def batch(rng, n):
    out = []
    while len(out) < n:
        out += [r for r in rng.integers(0, 10, (n, 6)).tolist() if tuple(r) not in HSET]
    return make(np.array(out[:n]))


def init_model(seed, nb=NB):
    g = np.random.default_rng(seed)
    return {'E': g.standard_normal((VOCAB, D)) * 0.5, 'P': g.standard_normal((CTX, D)) * 0.5,
            'blocks': [S4.init_block(D, DM, seed=seed * 10 + i + 1) for i in range(nb)],
            'lnf_g': np.ones(D), 'lnf_b': np.zeros(D), 'U': g.standard_normal((D, VOCAB)) / math.sqrt(D), 'c': np.zeros(VOCAB)}


def tensors(m):
    return {'E': Tensor(np.array(m['E'], float)), 'P': Tensor(np.array(m['P'], float)),
            'blocks': [{k: Tensor(np.array(v, float)) for k, v in p.items()} for p in m['blocks']],
            'lnf_g': Tensor(np.array(m['lnf_g'], float)), 'lnf_b': Tensor(np.array(m['lnf_b'], float)),
            'U': Tensor(np.array(m['U'], float)), 'c': Tensor(np.array(m['c'], float))}


def arrays(m):
    a = lambda v: np.array(v.data if isinstance(v, Tensor) else v, float)  # noqa: E731
    return {'E': a(m['E']), 'P': a(m['P']), 'blocks': [{k: a(v) for k, v in p.items()} for p in m['blocks']],
            'lnf_g': a(m['lnf_g']), 'lnf_b': a(m['lnf_b']), 'U': a(m['U']), 'c': a(m['c'])}


def logits_var(X, m, res=True, ln=True):
    T = X.shape[-1]
    x = _wrap(m['E'])[X] + _wrap(m['P'])[np.arange(T)]
    nrm = S4.layernorm if ln else (lambda x, g, b: x)
    for p in m['blocks']:
        a = S4.mha(nrm(x, p['ln1_g'], p['ln1_b']), p, H)
        x = x + a if res else a
        f = S4.mlp(nrm(x, p['ln2_g'], p['ln2_b']), p)
        x = x + f if res else f
    return nrm(x, m['lnf_g'], m['lnf_b']) @ m['U'] + m['c']


def loss_t(m, X, Y, res=True, ln=True):
    z = logits_var(X, m, res, ln).reshape(-1, VOCAB)
    y = Y.reshape(-1)
    keep = np.nonzero(y >= 0)[0]
    return cross_entropy(z[keep], y[keep])


def train(seed, steps=STEPS, nb=NB, res=True, ln=True, lr=LR, warm=WARM, bs=BS):
    m = tensors(init_model(seed, nb))
    ps = [a for _, a in S4.flat_params(m)]
    mo = [np.zeros_like(p.data) for p in ps]
    ve = [np.zeros_like(p.data) for p in ps]
    rng = np.random.default_rng(100 + seed)
    hist = []
    for t in range(1, steps + 1):
        X, Y = batch(rng, bs)
        for p in ps:
            p.zero_grad()
        L = loss_t(m, X, Y, res, ln)
        L.backward()
        hist.append(L.item())
        new, mo, ve = adam_step([p.data for p in ps], [p.grad for p in ps], mo, ve, t, warmup_cosine(t, lr, warm, steps))
        for p, v in zip(ps, new):
            p.data = v
    return arrays(m), hist


def generate(m, digits):
    digits = np.asarray(digits)
    x = np.concatenate([digits, np.full((len(digits), 1), SEP)], 1)
    for _ in range(6):
        z = S4.lm_logits(x, m, H).data[:, -1, :]
        x = np.concatenate([x, z.argmax(-1)[:, None]], 1)
    return x[:, 7:]


def to_file(m):
    return {k: {'shape': list(np.shape(a)), 'b64': base64.b64encode(np.asarray(a, '<f4').tobytes()).decode()} for k, a in S4.flat_params(m)}


if '--write' in sys.argv:
    m, _ = train(0)
    out = {'about': 'sequence level 4: a 2-block pre-norm transformer (width 32, 4 heads, MLP 128, ReLU, learned positions, context 12) '
                    'that reverses 6 digits written after a separator (token 10). Trained by docs/reports/sequence-L4-numbers.py --write: seed 0, '
                    'Adam 0.003 with 50 warm-up steps and cosine decay, 400 steps of 64 fresh sequences, none from the 1,000 held out by default_rng(1). '
                    'Arrays are little-endian float32 in base64; read with seq_ops_l4.read_model. Generated for this course; no third-party data.',
           'config': {'vocab': VOCAB, 'sep': SEP, 'context': CTX, 'width': D, 'heads': H, 'mlp': DM, 'blocks': NB}}
    out.update(to_file(m))
    with open(WFILE, 'w') as f:
        json.dump(out, f, separators=(',', ':'))
    print('wrote', WFILE, os.path.getsize(WFILE), 'bytes')
    sys.exit(0)

lv = Level('sequence', 4, coverage='strict')
E = lv.expect
LIT = lv.literal


def F(fid):
    return lv._file(fid)[1]


def two(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol * max(1.0, abs(a), abs(b)), f'{label}: routes agree ({a!r} vs {b!r})')
    return a


def sm(s, axis=-1):
    s = np.asarray(s, float)
    z = np.exp(s - s.max(axis=axis, keepdims=True))
    return z / z.sum(axis=axis, keepdims=True)


# ---------------- route B: a plain NumPy transformer, no autograd ----------------
def np_ln(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(((x - mu) ** 2).mean(-1, keepdims=True) + eps) + b


def np_attn(x, p, h):
    T, d = x.shape[-2:]
    w = d // h
    sp = lambda a: np.swapaxes(a.reshape(*a.shape[:-1], h, w), -2, -3)  # noqa: E731
    q, k, v = sp(x @ p['Wq'] + p['bq']), sp(x @ p['Wk'] + p['bk']), sp(x @ p['Wv'] + p['bv'])
    S = q @ np.swapaxes(k, -1, -2) / math.sqrt(w) + np.triu(np.full((T, T), -np.inf), 1)
    A = sm(S)
    o = np.swapaxes(A @ v, -2, -3).reshape(*x.shape[:-1], d)
    return o @ p['Wo'] + p['bo'], A


def np_mlp(x, p):
    return np.maximum(0, x @ p['W1'] + p['b1']) @ p['W2'] + p['b2']


def np_block_parts(x, p, h):
    a = np_attn(np_ln(x, p['ln1_g'], p['ln1_b']), p, h)[0]
    x1 = x + a
    f = np_mlp(np_ln(x1, p['ln2_g'], p['ln2_b']), p)
    return a, f


def np_stream(tokens, m, h=H, skip=0):
    tokens = np.asarray(tokens)
    x = m['E'][tokens] + m['P'][:tokens.shape[-1]]
    out, j = [x], 0
    for p in m['blocks']:
        for part in ('a', 'f'):
            j += 1
            if part == 'a':
                w = np_attn(np_ln(x, p['ln1_g'], p['ln1_b']), p, h)[0]
            else:
                w = np_mlp(np_ln(x, p['ln2_g'], p['ln2_b']), p)
            if j != skip:
                x = x + w
            out.append(x)
    return out


def np_logits(tokens, m, h=H, skip=0):
    x = np_stream(tokens, m, h, skip)[-1]
    return np_ln(x, m['lnf_g'], m['lnf_b']) @ m['U'] + m['c']


def np_generate(m, digits, skip=0):
    x = np.concatenate([np.asarray(digits), np.full((len(digits), 1), SEP)], 1)
    for _ in range(6):
        x = np.concatenate([x, np_logits(x, m, skip=skip)[:, -1].argmax(-1)[:, None]], 1)
    return x[:, 7:]


def bp(d, dm, bias=True):
    return 4 * d * d + (4 * d if bias else 0) + 2 * d * dm + ((dm + d) if bias else 0) + (4 * d if bias else 2 * d)


def mp(V, ctx, d, dm, nb, tied=False):
    return V * d + ctx * d + nb * bp(d, dm) + 2 * d + (0 if tied else d * V) + V


def count_shapes(V, ctx, d, dm, nb, tied=False, bias=True):
    """Route B for counts: build every array as zeros and add their sizes."""
    blk = {'Wq': (d, d), 'Wk': (d, d), 'Wv': (d, d), 'Wo': (d, d), 'W1': (d, dm), 'W2': (dm, d), 'ln1_g': (d,), 'ln2_g': (d,)}
    if bias:
        blk.update({'bq': (d,), 'bk': (d,), 'bv': (d,), 'bo': (d,), 'b1': (dm,), 'b2': (d,), 'ln1_b': (d,), 'ln2_b': (d,)})
    arrs = [np.zeros((V, d)), np.zeros((ctx, d)), np.zeros(d), np.zeros(d), np.zeros(V)] + [np.zeros(s) for _ in range(nb) for s in blk.values()]
    if not tied:
        arrs.append(np.zeros((d, V)))
    return int(sum(a.size for a in arrs))


# ---------------- frozen and new modules ----------------
for name, pre in (('autograd.py', '5917d4ec91f7'), ('seq_ops_l2.py', 'fa2bed08afe4'), ('seq_ops_l3.py', '6187fda66d52'), ('nt_ops_l2.py', '5712fe43db9b'), ('nt_ops_l1.py', '9c1391a33624')):
    lv.claim(hashlib.sha256(open(os.path.join(DATA, name), 'rb').read()).hexdigest().startswith(pre), f'{name} is the frozen copy')
OPS = open(os.path.join(DATA, 'seq_ops_l4.py'), 'rb').read()
print('seq_ops_l4.py SHA-256', hashlib.sha256(OPS).hexdigest(), len(OPS), 'bytes')
g = np.random.default_rng(0)
pb = S4.init_block(8, 16, seed=1)
for k in pb:
    pb[k] = pb[k] + 0.1 * g.standard_normal(pb[k].shape)
Pt = {k: Tensor(v.copy()) for k, v in pb.items()}
Xt = Tensor(g.standard_normal((2, 5, 8)))
Mw = g.standard_normal((2, 5, 8))
lv.claim(grad_check(lambda: (S4.mlp(Xt, Pt) * Mw).sum(), [Xt] + list(Pt.values())) < 1e-6, 'mlp: gradient against central differences')
lv.claim(grad_check(lambda: (S4.mha(Xt, Pt, 2) * Mw).sum(), [Xt] + list(Pt.values())) < 1e-6, 'mha (causal, 2 heads, batch): gradient')
lv.claim(grad_check(lambda: (S4.block(Xt, Pt, 4) * Mw).sum(), [Xt] + list(Pt.values())) < 1e-6, 'block (4 heads, batch): gradient')
mt = tensors(init_model(3, nb=1))
Xs, Ys = make(np.random.default_rng(4).integers(0, 10, (3, 6)))
lv.claim(grad_check(lambda: loss_t(mt, Xs, Ys), [a for _, a in S4.flat_params(mt)]) < 1e-6, 'lm_logits through cross-entropy, every parameter of a 1-block model: gradient')
x2 = g.standard_normal((5, 8))
a_np, f_np = np_block_parts(x2, pb, 2)
lv.claim(np.allclose(S4.attn_update(x2, pb, 2).data, a_np, rtol=1e-12, atol=1e-12) and np.allclose(S4.block(x2, pb, 2).data, x2 + a_np + f_np, rtol=1e-12, atol=1e-12), 'block: seq_ops_l4 equals the plain NumPy block')
lv.claim(S4.n_params(pb) == bp(8, 16) == count_shapes(1, 1, 8, 16, 1) - (1 * 8 + 8 + 16 + 8 + 1), 'n_params of a block equals the formula')

# ---------------- the shipped model ----------------
M = S4.read_model(WFILE)
WJ = json.load(open(WFILE))
print('weights file', os.path.getsize(WFILE), 'bytes')
lv.claim(os.path.getsize(WFILE) < 262144, 'weights file under 256 KB')
m0, hist0 = train(0)
lv.claim(max(float(np.abs(np.asarray(a, '<f4') - b).max()) for (_, a), (_, b) in zip(S4.flat_params(m0), S4.flat_params(M))) < 1e-4, 'retrained seed 0 matches the shipped weights')
NP = S4.n_params(M)
lv.claim(NP == mp(11, 12, 32, 128, 2) == count_shapes(11, 12, 32, 128, 2) == 26571, 'reversal model: 26,571 by arrays, formula and zeros', covers=[26571])
gen_ag, gen_np = generate(M, HELD), np_generate(M, HELD)
lv.claim(np.array_equal(gen_ag, gen_np), 'greedy decoding: seq_ops_l4 and plain NumPy write the same digits')
acc0 = float(np.mean((gen_ag == HELD[:, ::-1]).all(1)))
lv.claim(acc0 == 1.0, f'shipped model reverses {acc0:.3f} of the 1,000 held-out inputs', covers=[1.0])
for seed in (1, 2):
    ms, _ = train(seed)
    a_ = float(np.mean((generate(ms, HELD) == HELD[:, ::-1]).all(1)))
    lv.claim(a_ >= 0.99, f'seed {seed}: held-out sequence accuracy {a_:.3f} >= 0.99')

# ---------------- l13 ----------------
L13 = 'l13-'
E(L13, 'screens[1].widget.answer', 8 * 4 * 64); two('hidden layer 8 x 256', 8 * 256, np.zeros((8, 256)).size)
E(L13, 'screens[1].widget.wrong[0].value', 256); E(L13, 'screens[1].widget.wrong[1].value', 8 * 64)
lv.claim(4 * 64 == 256, '4d at d = 64', covers=[256])
x0 = np.array([1.0, 3.0])
ln0 = lambda v: (v - v.mean()) / np.sqrt(((v - v.mean()) ** 2).mean() + 1e-5)  # noqa: E731
pA = {'ln1_g': np.ones(2), 'ln1_b': np.zeros(2), 'Wq': np.eye(2), 'bq': np.zeros(2), 'Wk': np.eye(2), 'bk': np.zeros(2), 'Wv': np.eye(2), 'bv': np.zeros(2),
      'Wo': 0.5 * np.eye(2), 'bo': np.zeros(2), 'ln2_g': np.ones(2), 'ln2_b': np.zeros(2), 'W1': np.eye(2), 'b1': np.zeros(2), 'W2': 2 * np.eye(2), 'b2': np.zeros(2)}
out_blk = S4.block(x0[None], pA, 1).data[0]
two('hand block by seq_ops_l4 and by hand', float(out_blk[0]), 0.5, 1e-5)
E(L13, 'screens[2].widget.answer', 0.5); E(L13, 'screens[2].explain.text', 5.5); E(L13, 'screens[2].explain.text', 3.5)
lv.claim(abs(out_blk[1] - 5.5) < 1e-4, 'second coordinate 5.5')
x1h = x0 + ln0(x0) * 0.5
E(L13, 'screens[2].widget.wrong[0].value', round(float(x1h[0] + 2 * ln0(x1h)[0]), 4))
E(L13, 'screens[2].widget.wrong[1].value', round(float(2 * max(0, ln0(x1h)[0])), 4))
a1 = ln0(x0) * 0.5
E(L13, 'screens[2].widget.wrong[2].value', round(float(a1[0] + 2 * max(0, ln0(a1)[0])), 4))
lv.claim(np.allclose(ln0(x0), [-1, 1], atol=1e-5) and np.allclose(ln0(x1h), [-1, 1], atol=1e-5), 'both layer norms give (-1, 1)', covers=[1.5])
E(L13, 'screens[7].widget.answer', 1); E(L13, 'screens[7].widget.wrong[0].value', 5)
# with attention the change at position 3 of 8 reaches positions 3..7; without, only 3 (checked on a planted block)
pc = S4.init_block(8, 16, seed=5)
Xc = np.random.default_rng(6).standard_normal((8, 8))
Yc = Xc.copy()
Yc[3] += np.linspace(-1, 1, 8)
moved = lambda f: int((np.abs(f(Yc) - f(Xc)).max(-1) > 1e-12).sum())  # noqa: E731
lv.claim(moved(lambda x: S4.block(x, pc, 2).data) == 5 and moved(lambda x: x + S4.mlp_update(x, pc).data) == 1, 'change at position 3: 5 rows move with attention, 1 without', covers=[5, 1])
Yq = Xc[:6].copy()
Yq[2] += np.linspace(-1, 1, 8)
lv.claim(int((np.abs(S4.block(Yq, pc, 2).data - S4.block(Xc[:6], pc, 2).data).max(-1) > 1e-12).sum()) == 4, 'quiz: 4 rows of 6 move', covers=[4])
E(L13, 'quiz[0].widget.answer', 4 * 48); E(L13, 'quiz[0].widget.wrong[1].value', 48 * 48)
E(L13, 'quiz[2].widget.answer', 4)
LIT('768', why='the width on a vendor card, a given in the transfer')
LIT('50,257', why='GPT-2 vocabulary on a card, a given (checked in l15)')
LIT('2017', why='a year, Vaswani et al.')
LIT('2020', why='a year, Xiong et al.')

# ---------------- l14 ----------------
L14 = 'l14-'
TOK = make([[3, 1, 4, 1, 5, 9]])[0][0]
ST = S4.stream(TOK, M, H)
STn = np_stream(TOK, M)
lv.claim(all(np.allclose(a, b, rtol=1e-10, atol=1e-10) for a, b in zip(ST, STn)), 'stream: seq_ops_l4 equals plain NumPy at every stage')
fr = F(L14)['screens'][0]['canvas']['controls'][0]['frames']
lv.claim(all([fr[k]['values'][f'c{i}'] for i in range(6)] == [round(float(STn[k][6][i]), 2) for i in range(6)] for k in range(5)), 'hook bars: the stream at position 6, first 6 coordinates, 5 stages')
for k in range(5):
    for i in range(6):
        E(L14, 'screens[0].canvas', round(float(STn[k][6][i]), 2))
v0, v4, v3 = round(float(STn[0][6][0]), 2), round(float(STn[4][6][0]), 2), round(float(STn[3][6][0]), 2)
E(L14, 'screens[0].widget.answer', round(v4 - v0, 2)); E(L14, 'screens[0].widget.wrong[1].value', round(v4 - v3, 2)); E(L14, 'screens[0].explain.text', round(v4 - v0, 2))
lv.claim(abs((STn[4][6][0] - STn[0][6][0]) - (v4 - v0)) < 0.02, 'reading the rounded bars lands within the band of the true change')
c2 = [round(float(STn[0][6][2]), 3)] + [round(float(STn[k + 1][6][2] - STn[k][6][2]), 3) for k in range(4)]
for v in c2:
    E(L14, 'screens[1].canvas', v)
fin2 = round(sum(c2), 3)
lv.claim(abs(fin2 - STn[4][6][2]) < 0.003, 'the rounded terms add to the stream value within the band')
E(L14, 'screens[1].widget.answer', fin2); E(L14, 'screens[1].widget.wrong[0].value', round(fin2 - c2[0], 3)); E(L14, 'screens[1].widget.wrong[1].value', round(c2[0] + c2[4], 3))
E(L14, 'screens[5].canvas', round(fin2 - c2[0], 3)); E(L14, 'screens[5].explain.text', fin2)
nx = [float(np.linalg.norm(STn[0][6]))] + [float(np.linalg.norm(STn[k + 1][6] - STn[k][6])) for k in range(4)] + [float(np.linalg.norm(STn[4][6]))]
for v in nx:
    E(L14, 'screens[3].canvas', round(v, 2))
E(L14, 'screens[3].prose', round(sum(nx[:5]), 2)); E(L14, 'screens[3].prose', round(nx[5], 2))
lv.claim(nx[5] < sum(nx[:5]), 'triangle inequality: final length below the sum of lengths')
ACC = []
for k in (1, 2, 3, 4):
    a_np = float(np.mean((np_generate(M, HELD, skip=k) == HELD[:, ::-1]).all(1)))
    ACC.append(a_np)
    E(L14, 'screens[6].canvas', round(a_np * 100, 1))
lv.claim(ACC[3] == max(ACC) and ACC[2] == min(ACC), f'ablation (plain NumPy): {ACC}; MLP 2 matters least, attention 2 most')
E(L14, 'screens[6].widget.answer', 4)
LIT('100%', why='the full model\'s held-out score, claimed above (1.0)')
E(L14, 'quiz[0].widget.answer', -1 + 0.5 + 2); E(L14, 'quiz[0].widget.wrong[1].value', 0.5 + 2)
E(L14, 'quiz[1].widget.answer', 6 * 2); E(L14, 'quiz[1].widget.wrong[1].value', 6 * 2 + 1)
lv.claim(np.allclose(np.array([2, -1]) + [0.5, 0.5] + [-1, 2], [1.5, 1.5]), 'quiz stream (1.5, 1.5)', covers=[1.5])
LIT('1,000', why='the size of the held-out set, a setting')

# ---------------- l15 ----------------
L15 = 'l15-'
blk64 = count_shapes(1, 1, 64, 256, 1) - (64 + 64 + 64 + 64 + 1 + 64)
two('block 64 by zeros', blk64, 49984)
E(L15, 'screens[1].widget.answer', 4 * (64 * 64 + 64)); E(L15, 'screens[1].widget.wrong[0].value', 16 * (64 * 64 + 64)); E(L15, 'screens[1].widget.wrong[1].value', 4 * 64 * 64); E(L15, 'screens[1].widget.wrong[2].value', 3 * (64 * 64 + 64))
mlp64 = 64 * 256 + 256 + 256 * 64 + 64
E(L15, 'screens[2].widget.answer', mlp64); E(L15, 'screens[2].widget.wrong[0].value', 2 * 64 * 256); E(L15, 'screens[2].widget.wrong[1].value', mlp64 - 64); E(L15, 'screens[2].widget.wrong[2].value', 2 * 64 * 64 + 128)
E(L15, 'screens[3].widget.answer', 49984); E(L15, 'screens[3].widget.wrong[0].value', 49984 - 256); E(L15, 'screens[3].widget.wrong[1].value', 49984 - 128)
E(L15, 'screens[4].widget.answer', 16640); E(L15, 'screens[4].widget.wrong[0].value', 8 * 16640); E(L15, 'screens[4].widget.wrong[1].value', 2 * 16640)
SP = mp(65, 32, 64, 256, 1)
two('spike model by formula and zeros', SP, count_shapes(65, 32, 64, 256, 1))
E(L15, 'screens[5].widget.answer', 60545); E(L15, 'screens[5].widget.wrong[0].value', SP - 4160); E(L15, 'screens[5].widget.wrong[1].value', SP - 2048); E(L15, 'screens[5].widget.wrong[2].value', SP - 65)
lv.claim(65 * 64 == 4160 and 32 * 64 == 2048 and 64 * 65 + 65 == 4225 and 2 * 64 == 128 and 64 * 64 == 4096 and 64 * 256 == 16384 and 64 * 64 + 64 == 4160,
         'the parts of the spike model', covers=[4160, 2048, 4225, 128, 4096, 16384, 64 * 256, 16384 * 2])
lv.claim(round(49984 / 60545, 2) == 0.83 and round(mlp64 / 49984, 2) == 0.66 and round(16640 / 49984, 2) == 0.33 and round(256 / 49984, 4) == 0.0051, 'shares: 83%, two thirds, a third, half a per cent', covers=[0.83, 2 / 3, 1 / 3, 0.005])
two('no-bias block by formula and zeros', bp(64, 256, False), count_shapes(1, 1, 64, 256, 1, bias=False) - (64 + 64 + 64 + 64 + 1 + 64))
E(L15, 'screens[7].widget.answer', 49280); E(L15, 'screens[7].widget.wrong[0].value', 49280 + 128); E(L15, 'screens[7].widget.wrong[1].value', 4 * 64 * 64 + 2 * 64 * 256)
lv.claim(49984 - 49280 == 704 and 704 / 49984 < 0.015 and 4 * 64 * 64 == 16384 and 2 * 64 * 256 == 32768, '704 saved, under 1.5%', covers=[704, 0.015, 32768])
TI = mp(65, 32, 64, 256, 1, tied=True)
two('tied by formula and zeros', TI, count_shapes(65, 32, 64, 256, 1, tied=True))
E(L15, 'screens[8].widget.answer', TI); E(L15, 'screens[8].widget.wrong[0].value', TI - 65); E(L15, 'screens[8].widget.wrong[1].value', SP - 2 * 4160)
lv.claim(4160 / 60545 < 0.07 and SP - 4160 - 4160 - 65 == 52160, 'tying saves under 7%; the rest 52,160', covers=[0.07, 52160])
BV = mp(50257, 32, 64, 256, 1)
two('large vocabulary by formula and zeros', BV, count_shapes(50257, 32, 64, 256, 1))
emb = 50257 * 64 * 2 + 50257
E(L15, 'screens[9].widget.answer', round(emb / BV, 3)); E(L15, 'screens[9].widget.wrong[0].value', round(49984 / BV, 3)); E(L15, 'screens[9].widget.wrong[1].value', round(50257 * 64 / BV, 3))
for v in (50257 * 64, 50257 * 65, emb, BV):
    E(L15, 'screens[9]', v)
E(L15, 'screens[9].feedback.correct', round(emb / BV * 100, 1))
G2 = mp(50257, 1024, 768, 3072, 12, tied=True)
two('GPT-2 small by formula and zeros', G2, count_shapes(50257, 1024, 768, 3072, 12, tied=True))
CARD = 124439808
two('the card: our count without the unembedding bias', G2 - 50257, CARD)
E(L15, 'screens[10].widget.answer', G2 - CARD); E(L15, 'screens[10].prose', G2); E(L15, 'screens[10].widget.wrong[0].value', 50257 * 768)
LIT('124,439,808', why='GPT-2 small\'s published count; recomputed above as our formula without the 50,257 output biases')
LIT('3,072', why='GPT-2 small MLP width, a given'); LIT('1,024', why='GPT-2 small context, a given')
E(L15, 'quiz[0].widget.answer', 4 * (32 * 32 + 32)); E(L15, 'quiz[0].widget.wrong[0].value', 4 * 32 * 32); E(L15, 'quiz[0].widget.wrong[1].value', 16 * (32 * 32 + 32))
E(L15, 'quiz[1].widget.answer', 16 * 64 + 64 + 64 * 16 + 16); E(L15, 'quiz[1].widget.wrong[0].value', 2 * 16 * 64)
E(L15, 'quiz[3].widget.answer', 2000 * 128); E(L15, 'quiz[3].widget.wrong[0].value', 2000 * 129); E(L15, 'quiz[3].widget.wrong[1].value', 2 * 2000 * 128)
lv.claim(32 * 32 + 32 == 1056 and 16 * 64 == 1024 and 48 * 48 == 2304, 'quiz workings', covers=[1056, 1024, 2304])

# ---------------- l16 ----------------
L16 = 'l16-'
INP = [[3, 1, 4, 1, 5, 9], [2, 7, 1, 8, 2, 8], [0, 0, 7, 4, 2, 1], [9, 0, 2, 1, 0, 6], [8, 8, 8, 8, 8, 8]]
lv.claim(np.array_equal(np_generate(M, INP), np.array(INP)[:, ::-1]), 'hook: all five inputs reversed (plain NumPy decode)')
E(L16, 'screens[0].widget.answer', 5)


def head_pattern(tokens, m, layer, head):
    x = m['E'][tokens] + m['P'][:len(tokens)]
    for li, p in enumerate(m['blocks']):
        A = np_attn(np_ln(x, p['ln1_g'], p['ln1_b']), p, H)[1]
        if li == layer:
            return A[head]
        a, f = np_block_parts(x, p, H)
        x = x + a + f


A1 = head_pattern(make([INP[0]])[0][0], M, 1, 0)[6:12, :7]
mat = F(L16)['screens'][1]['canvas']['params']['matrices'][0]['rows']
lv.claim(np.allclose(mat, np.round(A1, 2)), 'attention heat: block 2, head 1 on 3 1 4 1 5 9 (plain NumPy)')
lv.claim(all(int(np.argmax(A1[t - 1, :6])) + 1 == 7 - t for t in range(1, 7)), 'every output row t puts its largest input weight on input 7 - t', covers=[7])
E(L16, 'screens[1].widget.answer', 5)
E(L16, 'screens[1].hints[2].text', round(float(A1[1][4]), 2)); E(L16, 'screens[1].explain.text', round(float(A1[4][1]), 2)); E(L16, 'screens[1].explain.text', round(float(A1[5][0]), 2))
for v in np.round(A1, 2).ravel():
    E(L16, 'screens[1].canvas', float(v))
A8 = head_pattern(make([INP[4]])[0][0], M, 1, 0)[6:12, :7]
lv.claim(np.allclose(F(L16)['screens'][8]['canvas']['params']['matrices'][0]['rows'], np.round(A8, 2)), 'edge heat: 8 8 8 8 8 8')
lv.claim(all(int(np.argmax(A8[t - 1, :6])) + 1 == 7 - t for t in range(1, 7)), 'repeated 8s: the pattern still follows the anti-diagonal')
for v in np.round(A8, 2).ravel():
    E(L16, 'screens[8].canvas', float(v))
mh = [round(float(np.mean(hist0[i:i + 20])), 3) for i in range(0, 400, 20)]
lv.claim(F(L16)['screens'][2]['canvas']['params']['series'][0]['values'] == mh, 'training curve: the retrained seed-0 run, means over 20 steps')
for v in mh:
    E(L16, 'screens[2].canvas', v)
E(L16, 'screens[2].widget.answer', round(math.log(11), 3)); E(L16, 'screens[2].widget.wrong[0].value', round(math.log2(11), 3)); E(L16, 'screens[2].widget.wrong[1].value', round(math.log(10), 3))
two('ln 11 two ways', math.log(11), -math.log(1 / 11))
E(L16, 'screens[2].explain.text', round(mh[0], 2)); E(L16, 'screens[2].explain.text', round(mh[-1], 3))
# trap: one batch of 32 for 100 steps
XB, YB = make(np.random.default_rng(5).integers(0, 10, (32, 6)))


def train_fixed(m_, X, Y, steps, lr):
    P = tensors(m_)
    ps = [a for _, a in S4.flat_params(P)]
    mo = [np.zeros_like(p.data) for p in ps]
    ve = [np.zeros_like(p.data) for p in ps]
    out = []
    for t in range(1, steps + 1):
        for p in ps:
            p.zero_grad()
        l_ = loss_t(P, X, Y)
        l_.backward()
        out.append(l_.item())
        new, mo, ve = adam_step([p.data for p in ps], [p.grad for p in ps], mo, ve, t, lr)
        for p, v in zip(ps, new):
            p.data = v
    return arrays(P), out


MEM, LM = train_fixed(init_model(7), XB, YB, 100, 0.003)
gm = np_generate(MEM, HELD)
tr_acc = float(np.mean((np_generate(MEM, XB[:, :6]) == XB[:, :6][:, ::-1]).all(1)))
ho_acc, ho_dig = float(np.mean((gm == HELD[:, ::-1]).all(1))), float(np.mean(gm == HELD[:, ::-1]))
lv.claim(np.array_equal(gm, generate(MEM, HELD)), 'memorised model: both decoders agree')
E(L16, 'screens[5].prose', round(LM[-1], 4)); E(L16, 'screens[5].canvas', round(tr_acc * 100)); E(L16, 'screens[5].canvas', round(ho_acc * 100, 1)); E(L16, 'screens[5].canvas', round(ho_dig * 100, 1))
lv.claim(tr_acc == 1.0 and ho_acc < 0.02, f'memorised: training {tr_acc}, held out {ho_acc}, digits {ho_dig:.4f}', covers=[1.0])
lv.claim(LM[-1] < 0.05 and LM[9] < 1.6, f'graded thresholds: tenth loss {LM[9]:.4f} < 1.6, hundredth {LM[-1]:.4f} < 0.05', covers=[1.6, 0.05])
for s_ in (8, 9):
    lm2 = train_fixed(init_model(s_), XB, YB, 10, 0.003)[1]
    lv.claim(lm2[-1] < 1.6, f'start seed {s_}: tenth loss {lm2[-1]:.4f} also below 1.6')
lv.claim(F(L16)['screens'][6]['canvas']['params']['series'][0]['values'] == [round(v, 3) for v in LM[:10]], 'graded-run canvas: the reference losses of the first 10 steps')
for v in LM[:10]:
    E(L16, 'screens[6].canvas', round(v, 3))
E(L16, 'screens[6].feedback.correct', round(LM[0], 3)); E(L16, 'screens[6].feedback.correct', round(LM[9], 3))
VAR = {}
for name_, res, lnf in (('full', True, True), ('nores', False, True), ('noln', True, False)):
    hv = train(0, steps=300, nb=6, res=res, ln=lnf, bs=32)[1]
    VAR[name_] = [round(float(np.mean(hv[i:i + 25])), 3) for i in range(0, 300, 25)]
ser = {s['id']: s['values'] for s in F(L16)['screens'][7]['canvas']['params']['series']}
# a stalled run is chaotic: its curve differs by machine (BLAS kernels), so the plotted curves are checked to 0.15 and the text states thresholds only
plotted = [v for k in ser for v in ser[k]]
lv.claim(all(len(ser[k]) == 12 and max(abs(a - min(b, 4.0)) for a, b in zip(ser[k], VAR[k])) < 0.15 for k in VAR), 'recorded 6-block curves reproduced to 0.15 (capped at 4 on the canvas)', covers=plotted)
lv.claim(VAR['nores'][-1] > 1.8 and VAR['noln'][-1] < 1.8 and VAR['full'][-1] < 0.01 and VAR['noln'][0] > 4, 'only the run without residuals ends above 1.8; as built below 0.01; without norms it starts above 4', covers=[1.8, 0.01, 4])
hv1 = train(1, steps=300, nb=6, res=False, bs=32)[1]
lv.claim(float(np.mean(hv1[-25:])) > 1.8, f'second seed: no residuals also ends above 1.8 ({np.mean(hv1[-25:]):.3f})')
lv.claim(6 * 2 == 12, '12 parts in 6 blocks', covers=[12])
E(L16, 'quiz[0].widget.answer', 9 - 3); E(L16, 'quiz[1].widget.answer', 993 / 1000); E(L16, 'quiz[1].widget.wrong[0].value', 7 / 1000)
E(L16, 'quiz[3].widget.answer', round(math.log(5), 3)); E(L16, 'quiz[3].widget.wrong[0].value', round(math.log2(5), 3))
LIT('10^6', why='the number of six-digit inputs, 10 to the 6')
LIT('400', why='training steps, a setting'); LIT('300', why='training steps of the deeper runs, a setting')

# ---------------- review ----------------
E('review', 'items[1].widget.answer', bp(32, 128)); two('review block by zeros', bp(32, 128), count_shapes(1, 1, 32, 128, 1) - (32 * 4 + 1 + 32))
E('review', 'items[1].widget.wrong[0].value', bp(32, 128, False)); E('review', 'items[1].widget.wrong[1].value', bp(32, 128) + 3 * 4 * (32 * 32 + 32)); E('review', 'items[1].widget.wrong[2].value', bp(32, 128) - 128)
lv.claim(4 * (1024 + 32) == 4224 and 32 * 128 * 2 + 160 == 8352 and 8192 + 160 == 8352, 'review workings', covers=[4224, 8352, 8192, 160])
E('review', 'items[2].widget.answer', 0.5 + 1 - 2); E('review', 'items[2].widget.wrong[0].value', 1 - 2)
lv.claim(np.allclose(np.array([0.5, -1]) + [1, 0.25] + [-2, 1.5], [-0.5, 0.75]), 'review stream (-0.5, 0.75)', covers=[0.75])
E('review', 'items[5].widget.answer', 4 * (48 * 48 + 48)); E('review', 'items[5].widget.wrong[0].value', 24 * (48 * 48 + 48)); E('review', 'items[5].widget.wrong[1].value', 4 * 48 * 48)
W27 = mp(27, 8, 32, 128, 1)
two('review model by zeros', W27, count_shapes(27, 8, 32, 128, 1))
E('review', 'items[7].widget.answer', W27); E('review', 'items[7].widget.wrong[0].value', W27 - 864); E('review', 'items[7].widget.wrong[1].value', W27 - 256)
lv.claim(27 * 32 == 864 and 8 * 32 == 256 and 32 * 27 + 27 == 891, 'review model parts', covers=[864, 891])
LIT('5,000', why='training sequences in a scenario, a given'); LIT('10^8', why='the number of inputs in a scenario, a given')

# ---------------- problems ----------------
A96, M96, B96 = 4 * (96 * 96 + 96), 96 * 384 + 384 + 384 * 96 + 96, bp(96, 384)
two('block 96 by zeros', B96, count_shapes(1, 1, 96, 384, 1) - (96 * 4 + 1 + 96))
E('problems', 'items[0].parts[0].widget.answer', A96); E('problems', 'items[0].parts[0].widget.wrong[0].value', 4 * A96); E('problems', 'items[0].parts[0].widget.wrong[1].value', 4 * 96 * 96)
E('problems', 'items[0].parts[1].widget.answer', M96); E('problems', 'items[0].parts[1].widget.wrong[0].value', 2 * 96 * 384)
E('problems', 'items[0].parts[2].widget.answer', B96); E('problems', 'items[0].parts[2].widget.wrong[0].value', A96 + M96)
E('problems', 'items[0].parts[3].widget.answer', round(M96 / B96, 3)); E('problems', 'items[0].parts[3].widget.wrong[0].value', round(A96 / B96, 3)); E('problems', 'items[0].parts[3].feedback.correct', round(M96 / B96 * 100, 1))
lv.claim(96 * 384 == 36864 and 4 * 96 == 384, 'problem 1 workings', covers=[36864, 384])
T2, T2t = mp(500, 64, 96, 384, 2), mp(500, 64, 96, 384, 2, tied=True)
two('two-block model by zeros', T2, count_shapes(500, 64, 96, 384, 2)); two('tied by zeros', T2t, count_shapes(500, 64, 96, 384, 2, tied=True))
E('problems', 'items[1].parts[0].widget.answer', T2); E('problems', 'items[1].parts[0].widget.wrong[0].value', T2 - B96); E('problems', 'items[1].parts[0].widget.wrong[1].value', T2 - 48500)
e2, e2t = 500 * 96 * 2 + 500, 500 * 96 + 500
E('problems', 'items[1].parts[1].widget.answer', round(e2 / T2, 3)); E('problems', 'items[1].parts[1].widget.wrong[0].value', round(48000 / T2, 3)); E('problems', 'items[1].parts[1].feedback.correct', round(e2 / T2 * 100, 1))
E('problems', 'items[1].parts[2].widget.answer', T2t); E('problems', 'items[1].parts[2].widget.wrong[0].value', T2t - 500)
E('problems', 'items[1].parts[3].widget.answer', round(e2t / T2t, 3)); E('problems', 'items[1].parts[3].widget.wrong[0].value', round(e2 / T2, 3)); E('problems', 'items[1].parts[3].feedback.correct', round(e2t / T2t * 100, 1))
lv.claim(500 * 96 == 48000 and 64 * 96 == 6144 and 2 * B96 == 223680 and 2 * 96 == 192 and 96 * 500 + 500 == 48500 and round(e2 / T2, 2) == 0.30 and round(e2t / T2t, 2) == 0.17,
         'problem 2 parts and the 30% to 17% summary', covers=[48000, 6144, 223680, 192, 48500, 0.30, 0.17])
LIT('111,840', why='the block count of part 3, restated as a given in problem 2')
x0p, d1p, d2p = np.array([1.0, 0, 2]), np.array([0.5, -1, 0]), np.array([-0.5, 0.5, 1])
x2p = x0p + d1p + d2p
E('problems', 'items[2].parts[0].widget.answer', float(x2p[1])); E('problems', 'items[2].parts[0].widget.wrong[0].value', float(d2p[1])); E('problems', 'items[2].parts[0].widget.wrong[1].value', float((x0p + d1p)[1]))
E('problems', 'items[2].parts[1].widget.answer', round(float(np.linalg.norm(x2p)), 4)); E('problems', 'items[2].parts[1].widget.wrong[0].value', float(x2p @ x2p))
two('length of x2 two ways', float(np.linalg.norm(x2p)), math.sqrt(1 + 0.25 + 9))
E('problems', 'items[2].parts[2].widget.answer', float(d1p @ d2p)); E('problems', 'items[2].parts[2].widget.wrong[0].value', -float(d1p @ d2p))
E('problems', 'items[2].parts[3].widget.answer', round(float(np.linalg.norm(d1p + d2p)), 4)); E('problems', 'items[2].parts[3].widget.wrong[0].value', round(float(np.linalg.norm(d1p) + np.linalg.norm(d2p)), 4))
lv.claim(np.linalg.norm(d1p) > 1.1 and np.linalg.norm(d2p) > 1.1, 'each write longer than 1.1', covers=[1.1, 0.25])
cfg = mp(11, 12, 32, 128, 2)
E('problems', 'items[3].parts[0].widget.answer', 64 * 12 * 11); E('problems', 'items[3].parts[0].widget.wrong[0].value', 64 * 12); E('problems', 'items[3].parts[0].widget.wrong[1].value', 64 * 12 * 32)
two('logits by an array', 64 * 12 * 11, S4.lm_logits(np.zeros((64, 12), int), M, H).data.size)
E('problems', 'items[3].parts[1].widget.answer', cfg); E('problems', 'items[3].parts[1].widget.wrong[0].value', cfg - bp(32, 128)); E('problems', 'items[3].parts[1].widget.wrong[1].value', cfg - 352)
lv.claim(11 * 32 == 352 and 12 * 32 == 384 and 2 * 32 == 64 and 32 * 11 + 11 == 363 and 2 * 12704 == 25408, 'problem 4 parts', covers=[352, 363, 25408])
E('problems', 'items[3].parts[2].widget.answer', round(2 * bp(32, 128) / cfg, 3)); E('problems', 'items[3].parts[2].widget.wrong[0].value', round(bp(32, 128) / cfg, 3)); E('problems', 'items[3].parts[2].feedback.correct', round(2 * bp(32, 128) / cfg * 100, 1))
E('problems', 'items[3].parts[3].widget.answer', round(6 * math.log(11), 3)); E('problems', 'items[3].parts[3].widget.wrong[0].value', round(math.log(11), 3)); E('problems', 'items[3].parts[3].widget.wrong[1].value', round(6 * math.log(10), 3))
two('6 ln 11 two ways', 6 * math.log(11), math.log(11 ** 6))
E('problems', 'items[3].parts[4].widget.answer', round(0.99 ** 6, 4)); E('problems', 'items[3].parts[4].widget.wrong[1].value', 1 - 6 * 0.01)
two('0.99^6 two ways', 0.99 ** 6, math.exp(6 * math.log(0.99)))
LIT('0.99', why='a stated per-digit chance in problem 4, a given')

# ---------------- homework ----------------
H1 = mp(65, 64, 128, 512, 2)
two('homework model by zeros', H1, count_shapes(65, 64, 128, 512, 2))
E('homework', 'items[0].widget.answer', H1); E('homework', 'items[0].widget.wrong[0].value', H1 - bp(128, 512)); E('homework', 'items[0].widget.wrong[1].value', H1 - 65 * 128)
E('homework', 'items[0].widget.wrong[2].value', count_shapes(65, 64, 128, 512, 2, bias=False) - 128 - 65)
lv.claim(bp(128, 512) == 198272 and 4 * (128 * 128 + 128) == 66048 and 2 * 128 * 512 + 640 == 131712 and 65 * 128 == 8320 and 64 * 128 == 8192 and 128 * 65 + 65 == 8385 and 2 * 128 * 512 == 131072,
         'homework workings', covers=[198272, 66048, 131712, 8320, 8192, 8385, 131072, 640])
H5 = mp(32000, 512, 512, 2048, 4, tied=True)
two('homework vocabulary model by zeros', H5, count_shapes(32000, 512, 512, 2048, 4, tied=True))
E('homework', 'items[4].widget.answer', round(32000 * 512 / H5, 3)); E('homework', 'items[4].widget.wrong[0].value', round(32000 * 512 / mp(32000, 512, 512, 2048, 4), 3)); E('homework', 'items[4].widget.wrong[1].value', round(4 * bp(512, 2048) / H5, 3))
lv.claim(bp(512, 2048) == 3152384 and 32000 * 512 == 16384000 and 512 * 512 == 262144, 'homework 5 parts', covers=[3152384, 16384000, 262144, 1024, H5, round(32000 * 512 / H5 * 100, 1)])
lv.claim(round(12 * 64 ** 2 / bp(64, 256), 1) == 1.0, 'longform: about 12 d^2 a block (49,152 against 49,984 at d = 64)', covers=[12])
LIT('300', why='a word limit in the longform prompt'); LIT('48', why='blocks in a scenario, a given')
# the homework reference against seq_ops_l4
ns = {}
pf = F('homework')['items'][7]['widget']
cwd = os.getcwd()
os.chdir(DATA)
exec(pf['prelude'], ns)
os.chdir(cwd)
exec(pf['solution'], ns)
for tk, nb_, h_ in ((ns['TK'], 3, 2), (ns['TK'], 2, 2), (ns['TK'], 3, 4), ([5], 3, 2), (ns['TK'], 0, 2)):
    ref = S4.lm_logits(np.array(tk), dict(ns['PL'], blocks=ns['PL']['blocks'][:nb_]), h_).data
    lv.claim(np.allclose(ns['transformer_lm_forward'](tk, ns['PL'], nb_, h_), ref, rtol=1e-10, atol=1e-12), f'transformer_lm_forward equals seq_ops_l4.lm_logits ({len(tk)} tokens, {nb_} blocks, {h_} heads)')
lv.claim(np.allclose(ns['transformer_lm_forward'](ns['TOKR'], ns['REV'], 2, 4), S4.lm_logits(ns['TOKR'], M, H).data, rtol=1e-10), 'transformer_lm_forward on the reversal model')


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
            return math.isclose(float(x), float(yv), rel_tol=rt, abs_tol=at) or float(x) == float(yv)
        except Exception:
            return x == yv

    def same(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(same(p_, q_) for p_, q_ in zip(x, yv))
        return bool(x == yv)
    return close(a, ex) if cmp == 'isclose' else same(a, ex)


MODS = ('autograd', 'seq_ops_l2', 'seq_ops_l3', 'seq_ops_l4', 'nt_ops_l1', 'nt_ops_l2')


def purge():
    for m_ in [m_ for m_ in sys.modules if m_ in MODS]:
        sys.modules.pop(m_)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    try:
        for kk, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), os.path.join(dd, kk))
        sys.path.insert(0, dd)
        purge()
        ns_ = {'__name__': '__zq__', '__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec(ZQ_LIB, ns_)
                exec((w.get('prelude') or '') + '\n', ns_)
                exec(src, ns_)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns_)
                    got = eval(c['call'], ns_)
                    t = c.get('tol')
                    ok = judge(got, eval(c['expect'], ns_), c.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
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
        for k_, v_ in (w.get('data') or {}).items():
            if k_.endswith('.py'):
                lv.claim(open(os.path.join(APP, v_), 'rb').read() == open(os.path.join(DATA, k_), 'rb').read(), f'{lab}: ships {k_} byte-identical')
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        for mu in w.get('mutants', []):
            nm += 1
            got = first_fail(w, mu['source'])
            lv.claim(got == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')

lv.claim(abs(mlp64 / 16640 - 2) < 0.02 and abs(2 * 2000 * 128 / (2000 * 128) - 2) < 1e-12 and 16 * 4096 * 2 == 2 * 4 * 16384, 'the MLP holds twice what attention holds; a second copy doubles', covers=[2])
lv.claim(abs(-math.log(1 / 11) - math.log(11)) < 1e-12 and abs(-math.log(1 / 5) - math.log(5)) < 1e-12 and 64 / 8 == 8 and 9 - 3 == 6 and 1 + 0.25 + 9 == 10.25,
         'uniform chances 1/11 and 1/5; head width 64/8; 9 - t; the squares under the root', covers=[1 / 11, 1 / 5, 8, 9, 10.25])
for t_, why in [('64', 'a given width'), ('32', 'a given width, batch or context'), ('65', 'the spike\'s vocabulary, a given'), ('16', 'a given width'), ('11', 'the reversal vocabulary, a given'),
                ('24', 'writes in a 12-block model, 2 a block (checked as 12 x 2 above)'), ('27', 'makemore\'s symbols, a given'), ('500', 'a given vocabulary'), ('993', 'right answers in a scenario, a given'),
                ('32,000', 'a given vocabulary'), ('10^-6', 'test tolerances'), ('10^-5', 'the layer-norm epsilon'), ('8', 'given counts of positions and blocks')]:
    LIT(t_, why=why)
lv.claim(12 * 2 == 24, 'a 12-block model holds 24 writes', covers=[24])
lv.check_wrongs()
lv.report()
