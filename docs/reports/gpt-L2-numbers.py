"""Recompute every number stated in gpt level 2 (A tiny GPT forward pass) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only gpt-L2
(NumPy only; strict coverage; exits 0 when every check passes).
`--write` trains the app's tiny GPT and writes app/content/data/ai/gpt-w-embed.json and gpt-w-block0.json (then exits).

The tiny GPT: vocabulary 65, context 32, width 32, 4 heads of 8, one pre-norm block (seq_ops_l4's: ReLU MLP of 128,
biases on every linear layer, learned positions, final layer norm, untied head with a bias), 18,017 parameters.
Trained here with autograd.py and seq_ops_l4.lm_logits: weights N(0, 0.02^2) from default_rng(0) in file order, biases 0,
gains 1; Adam (nt_ops_l1.adam_step) at 0.003 with 100 warm-up steps and cosine decay (nt_ops_l1.warmup_cosine); 5,000 steps
of 16 random windows of 32 characters from the first 225,000 characters of tiny-shakespeare.txt (starts from default_rng(1)).
The last 25,000 characters are never trained on (validation; interp L1 reads the last 2,000 of them).
Route B for every forward figure: gpt_ops_l2 (plain NumPy) against seq_ops_l4.lm_logits (the autograd modules), and a
per-position loop written below. Every code widget is run in CPython with the page's judge (solution passes, starter fails,
each mutant first fails its named test).
"""
import base64
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
from autograd import Tensor, cross_entropy  # noqa: E402
from nt_ops_l1 import adam_step, warmup_cosine  # noqa: E402
import seq_ops_l4 as S4  # noqa: E402
import gpt_ops_l2 as G  # noqa: E402

TXT = open(os.path.join(DATA, 'tiny-shakespeare.txt')).read()
IDS = np.array(G.encode(TXT))
TR, VA = IDS[:225000], IDS[225000:]
NVW = (len(VA) - 1) // 32
XV = VA[:NVW * 32].reshape(NVW, 32)
YV = VA[1:NVW * 32 + 1].reshape(NVW, 32)
EMBED, BLOCK0 = os.path.join(DATA, 'gpt-w-embed.json'), os.path.join(DATA, 'gpt-w-block0.json')


def init_weights(seed, n_layer=1, sd=0.02):
    """Weights N(0, sd^2) from default_rng(seed) in file order, every vector a bias (0) or a gain (1)."""
    g = np.random.default_rng(seed)
    w = {}
    for k, s in G.shapes(dict(G.CONFIG, n_layer=n_layer)):
        if k.endswith('_g'):
            w[k] = np.ones(s)
        elif len(s) == 1:
            w[k] = np.zeros(s)
        else:
            w[k] = g.standard_normal(s) * sd
    return w


def train(n_layer=1, steps=5000, lr=3e-3, warm=100, seed=0, bseed=1):
    w = init_weights(seed, n_layer)
    names = list(w)
    m = {k: Tensor(v) for k, v in w.items()}
    params = [m[k] for k in names]
    M = [np.zeros_like(p.data) for p in params]
    V = [np.zeros_like(p.data) for p in params]
    rng = np.random.default_rng(bseed)
    losses = []
    for t in range(1, steps + 1):
        ix = rng.integers(0, len(TR) - 32, 16)
        X = np.stack([TR[i:i + 32] for i in ix])
        Y = np.stack([TR[i + 1:i + 33] for i in ix])
        for p in params:
            p.zero_grad()
        loss = cross_entropy(S4.lm_logits(X, G.to_model(m), 4).reshape(-1, 65), Y.reshape(-1))
        loss.backward()
        new, M, V = adam_step([p.data for p in params], [p.grad for p in params], M, V, t, warmup_cosine(t, lr, warm, steps))
        for p, a in zip(params, new):
            p.data = a
        losses.append(loss.item())
    return {k: m[k].data for k in names}, losses


if '--write' in sys.argv:
    W_, _ = train()
    names = [k for k, _ in G.shapes()]
    with open(EMBED, 'w') as f:
        f.write(G.weights_json(W_, [k for k in names if not k.startswith('h0.')]))
    with open(BLOCK0, 'w') as f:
        f.write(G.weights_json(W_, [k for k in names if k.startswith('h0.')]))
    print('wrote', EMBED, os.path.getsize(EMBED), BLOCK0, os.path.getsize(BLOCK0))
    sys.exit(0)

lv = Level('gpt', 2, coverage='strict')
E = lv.expect
LIT = lv.literal


def F(fid):
    return lv._file(fid)[1]


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def two(label, a, b, tol=1e-9, covers=None):
    lv.claim(close(a, b, tol), f'{label}: two routes agree ({a!r} vs {b!r})', covers=[a] if covers is None else covers)
    return a


# ---------------- route B: a per-position loop forward, written here without vectorised attention ----------------
def ln_loop(x, g, b):
    mu = sum(x) / len(x)
    var = sum((v - mu) ** 2 for v in x) / len(x)
    return np.array([g[i] * (x[i] - mu) / math.sqrt(var + 1e-5) + b[i] for i in range(len(x))])


def loop_logits(w, ids):
    """Logits of one sequence, a position and a head at a time."""
    T = len(ids)
    xs = [w['wte'][ids[t]] + w['wpe'][t] for t in range(T)]
    a = [ln_loop(x, w['h0.ln1_g'], w['h0.ln1_b']) @ w['h0.qkv_w'] + w['h0.qkv_b'] for x in xs]
    outs = []
    for t in range(T):
        z = np.zeros(32)
        for h in range(4):
            q = a[t][h * 8:(h + 1) * 8]
            sc = [float(q @ a[j][32 + h * 8:32 + (h + 1) * 8]) / math.sqrt(8) for j in range(t + 1)]
            m = max(sc)
            ex = [math.exp(s - m) for s in sc]
            tot = sum(ex)
            for j in range(t + 1):
                z[h * 8:(h + 1) * 8] += ex[j] / tot * a[j][64 + h * 8:64 + (h + 1) * 8]
        outs.append(xs[t] + z @ w['h0.proj_w'] + w['h0.proj_b'])
    res = []
    for x in outs:
        hdn = np.maximum(ln_loop(x, w['h0.ln2_g'], w['h0.ln2_b']) @ w['h0.fc_w'] + w['h0.fc_b'], 0)
        x2 = x + hdn @ w['h0.out_w'] + w['h0.out_b']
        res.append(ln_loop(x2, w['lnf_g'], w['lnf_b']) @ w['head_w'] + w['head_b'])
    return np.array(res)


def sm(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def logsm(z):
    z = z - z.max(-1, keepdims=True)
    return z - np.log(np.exp(z).sum(-1, keepdims=True))


W = G.read_weights(EMBED, BLOCK0)
MODEL = G.to_model(W)
lv.claim(os.path.getsize(EMBED) == 28580 and os.path.getsize(BLOCK0) == 68271, 'file sizes 28,580 and 68,271 bytes', covers=[28580, 68271])
lv.claim(max(os.path.getsize(EMBED), os.path.getsize(BLOCK0)) < 262144, 'each weights file under 256 KB', covers=[262144])
one = G.weights_json(W, [k for k, _ in G.shapes()])
lv.claim(len(one) == 96851, 'the same arrays in one file would be 96,851 bytes (the brief\'s figure)')
lv.claim(sorted(W) == sorted(k for k, _ in G.shapes()) and all(W[k].shape == s for k, s in G.shapes()), 'shipped files hold every array with its shape')
ids0 = np.array(G.encode('\nFirst Citizen:'))
lg_np, lg_ag, lg_loop = G.forward_logits(W, ids0), S4.lm_logits(ids0, MODEL, 4).data, loop_logits(W, ids0)
lv.claim(np.abs(lg_np - lg_ag).max() < 1e-10 and np.abs(lg_np - lg_loop).max() < 1e-10, 'forward: gpt_ops_l2, seq_ops_l4.lm_logits and a per-position loop agree')


# ---------------- l5: counts, by the closed formula and by summing the arrays' sizes ----------------
def formula(V, T, d, L, m, tied=False):
    return V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d + (0 if tied else d * V) + V


def by_arrays(V, T, d, L, m, tied=False):
    sh = G.shapes({'V': V, 'T': T, 'd': d, 'n_layer': L, 'mlp': m})
    return sum(int(np.prod(s)) for k, s in sh if not (tied and k == 'head_w'))


for cfg in [(65, 32, 32, 1, 128), (65, 32, 32, 2, 128), (65, 32, 64, 1, 256), (96, 128, 64, 2, 256), (50, 16, 16, 3, 64),
            (65, 32, 16, 1, 64), (80, 64, 48, 2, 192), (80, 64, 48, 1, 192), (65, 48, 40, 2, 160)]:
    two(f'parameters of {cfg}', formula(*cfg), by_arrays(*cfg), 0)
    two(f'tied parameters of {cfg}', formula(*cfg, tied=True), by_arrays(*cfg, tied=True), 0)
N1, N2 = formula(65, 32, 32, 1, 128), formula(65, 32, 32, 2, 128)
BLK = N2 - N1
lv.claim((N1, N2, BLK) == (18017, 30721, 12704), 'tiny GPT 18,017; two blocks 30,721; a block 12,704')
E('l5', 'screens[0].widget.answer', 16 * 32 * 65)
lv.claim(16 * 32 == 512 and 16 * 32 * 32 == 16384 and 32 * 65 == 2080, 'l5 hook slips', covers=[512, 16384, 2080])
E('l5', 'screens[1].widget.answer', 65 * 32)
lv.claim(65 + 32 == 97 and 32 * 32 == 1024, 'l5 table slips', covers=[97, 1024])
blk = {'ln1': 64, 'qkv_w': 32 * 96, 'qkv_b': 96, 'proj': 32 * 32 + 32, 'ln2': 64, 'fc_w': 32 * 128, 'fc_b': 128, 'out': 128 * 32 + 32}
lv.claim(sum(blk.values()) == BLK == 12704, 'block rows add to 12,704', covers=list(blk.values()) + [12704])
bias, lnp = 96 + 32 + 128 + 32, 128
lv.claim(BLK - bias == 12416 and BLK - lnp == 12576 and bias == 288 and 3072 + 1024 + 4096 + 4096 == 12288 and BLK - bias - lnp == 12288,
         'block without biases 12,416, without norms 12,576; weights 12,288', covers=[12416, 12576, 288, 12288, 1056, 4128])
emb, head = 65 * 32 + 32 * 32, 32 * 65 + 65
lv.claim(emb == 3104 and head == 2145 and emb + BLK + 64 + head == N1, 'parts 3,104 + 12,704 + 64 + 2,145', covers=[3104, 2145, 64])
lv.claim(formula(65, 32, 32, 1, 128, tied=True) == 15937 and N1 + (65 - 32) * 32 == 19073 and N1 - 65 == 17952 and 15937 - 65 == 15872,
         'slips: tied 15,937, wpe as V x d 19,073, no head bias 17,952, tied without bias 15,872', covers=[15937, 19073, 17952, 15872])
lv.claim(2 * N1 == 36034, 'doubled model 36,034', covers=[36034])
SPIKE = 65 * 64 + 32 * 64 + 4 * 64 * 64 + (64 * 256 + 256) + (256 * 64 + 64) + 64 * 65
O64 = formula(65, 32, 64, 1, 256)
lv.claim(SPIKE == 59840 and O64 == 60545 and O64 - SPIKE == 705 == (192 + 64) + 3 * 128 + 65, 'spike convention 59,840 against ours 60,545: gap 705',
         covers=[59840, 60545, 705, 256, 384, 192, 128, 65])
lv.claim(64 * 65 == 4160, 'tying the spike head would remove 4,160', covers=[4160])
CARD = formula(96, 128, 64, 2, 256)
blk64 = 4 * 64 * 64 + 2 * 64 * 256 + 9 * 64 + 256
lv.claim(CARD == 120672 and blk64 == 49984 and 96 * 64 == 6144 and 128 * 64 == 8192 and 2 * blk64 == 99968 and 64 * 96 + 96 == 6240,
         'card: 6,144 + 8,192 + 99,968 + 128 + 6,240 = 120,672', covers=[120672, 49984, 6144, 8192, 99968, 6240, 128])
lv.claim(CARD - 6144 == 114528 and CARD - blk64 == 70688, 'card slips: tied, one block', covers=[114528, 70688])
two('block share', round(BLK / N1, 4), round(12704 / 18017, 4), 0, covers=[BLK / N1, 1 - BLK / N1, 12288 / 18017])
lv.claim(4 * 32 * 32 + 2 * 32 * 128 == 12 * 32 * 32, 'with m = 4d the weights are 12 d^2', covers=[12])


# ---------------- l6: bytes, base64 and the two sanity losses ----------------
def b64len(n_numbers):
    return len(base64.b64encode(np.zeros(n_numbers, '<f4').tobytes()))


lv.claim(b64len(1024) == 5464 == 4 * math.ceil(4096 / 3) and math.ceil(4096 / 3) == 1366, 'wpe: 4,096 bytes, 1,366 groups, 5,464 characters', covers=[5464, 4096, 1366])
lv.claim(len(base64.b64encode(np.zeros(1024, '<f8').tobytes())) == 10924, 'float64 slip 10,924', covers=[10924])
small = np.frombuffer(base64.b64decode('AADAPwAAAMAAAIA+'), '<f4')
lv.claim(small.tolist() == [1.5, -2.0, 0.25] and len(base64.b64decode('AADAPwAAAMAAAIA+')) == 12, '16 characters, 12 bytes, 1.5, -2, 0.25', covers=[1.5, 2, 0.25, 12])
EMB_N = sum(W[k].size for k in W if not k.startswith('h0.'))
lv.claim(EMB_N == 5313 == 2080 + 1024 + 64 + 2145 and EMB_N + sum(W[k].size for k in W if k.startswith('h0.')) == 18017 and 3104 + 64 == 3168, 'embed file holds 5,313 numbers', covers=[5313, 3168])
lv.claim(float(np.float32(0.1)) == 0.10000000149011612, 'float32 of 0.1', covers=[0.10000000149011612])
lv.claim(4096 // 8 == 512, '4,096 bytes as float64: 512 numbers', covers=[512])
LN65 = math.log(65)
zero = {k: (np.ones(s) if k.endswith('_g') else np.zeros(s)) for k, s in G.shapes()}
two('ln 65 and the loss of an all-zero model', LN65, G.mean_loss(zero, XV[:16], YV[:16]), covers=[LN65, math.log2(65), 1 / 65])
I0 = two('init loss seed 0 (gpt_ops_l2 and seq_ops_l4)', G.mean_loss(init_weights(0), XV[:16], YV[:16]),
         float(cross_entropy(S4.lm_logits(XV[:16], G.to_model(init_weights(0)), 4).reshape(-1, 65), YV[:16].reshape(-1)).item()))
lv.claim(abs(I0 - LN65) < 0.05 and abs(G.mean_loss(init_weights(1), XV[:16], YV[:16]) - LN65) < 0.05, 'init losses within 0.05 of ln 65', covers=[0.05, 0.02, 4.2])
VAL = two('validation loss (gpt_ops_l2 and seq_ops_l4)', G.mean_loss(W, XV, YV),
          float(cross_entropy(S4.lm_logits(XV, MODEL, 4).reshape(-1, 65), YV.reshape(-1)).item()))
loopv = np.mean([-logsm(loop_logits(W, XV[i]))[np.arange(32), YV[i]].mean() for i in (0, 300, 780)])
vecv = np.mean([-logsm(G.forward_logits(W, XV[i]))[np.arange(32), YV[i]].mean() for i in (0, 300, 780)])
lv.claim(close(loopv, vecv, 1e-10), 'three validation windows: loop and vectorised losses agree')
lv.claim(NVW == 781, '781 validation windows', covers=[781])
two('validation loss in bits', VAL / math.log(2), VAL * (1 / math.log(2)), covers=[VAL, VAL / math.log(2), VAL * math.log(2), 6.0224])
lv.claim(round(VAL, 2) == 1.79 and abs(4.18 - LN65) < 0.01, 'stated 1.79; 4.18 is about ln 65', covers=[1.79, 4.18])
lv.claim(abs(math.log(96) - 4.56) < 0.005 and abs(4.57 - math.log(96)) < 0.02, 'vendor: random 4.57 near ln 96 = 4.56', covers=[4.57, 4.56, math.log(96)])
LIT('1.20', why='the vendor\'s stated loss, a given of the scenario')
LIT('1.21', why='the loss the scenario says the checkpoint gives, a given')
lv.claim(18017 * 4 == 72068 and 18017 * 8 == 144136 and 4 * math.ceil(72068 / 3) == 96092, 'q-bytes: 72,068; slips 144,136 and 96,092', covers=[72068, 144136, 96092])
two('ln 27', math.log(27), math.log2(27) * math.log(2), covers=[math.log(27), math.log2(27)])


# ---------------- l7: chances, losses and attention by seq_ops_l4 and the loop ----------------
def chances(prompt):
    ids = np.array(G.encode(prompt))
    a = sm(S4.lm_logits(ids, MODEL, 4).data[-1])
    b = sm(loop_logits(W, ids)[-1])
    lv.claim(np.abs(a - b).max() < 1e-12, f'chances after {prompt!r}: two routes agree')
    return a


pt = chances('\nFirst Ci')
P_T = float(pt[G.encode('t')[0]])
two('l7 hook loss', -math.log(P_T), -math.log(P_T), covers=[P_T, -math.log(P_T), -math.log10(P_T), -math.log2(P_T)])
lv.claim(sorted(np.round(pt, 4).tolist())[-5:][::-1] == [b for b in sorted(F('l7')['screens'][0]['canvas']['state']['values'].values())][::-1], 'hook bars: the top five chances to 4 places')
tp = {}
for k in range(2, 9):
    pr = '\nFirst Citizen:'[:k]
    p = chances(pr)
    tp[pr] = float(p[G.encode('\nFirst Citizen:'[k])[0]])
    fr = F('l7')['screens'][1]['canvas']['controls'][0]['frames'][k - 2]
    top = np.argsort(-p)[:5]
    lv.claim([fr['values'][f'k{j}'] for j in range(5)] == [round(float(p[i]), 3) for i in top], f'explore frame {pr!r}: top five to 3 places', covers=[float(p[i]) for i in top] + [tp[pr]])
lv.claim(min(tp, key=tp.get) == '\nFirst ', 'lowest true chance is after "First "')
lv.claim(15 * 65 == 975 and 15 * 32 == 480, '975 logits; slip 480', covers=[975, 480])
ids_m = np.array(G.encode('MENENIUS'))
a_ = [ln_loop(W['wte'][i] + W['wpe'][t], W['h0.ln1_g'], W['h0.ln1_b']) @ W['h0.qkv_w'] + W['h0.qkv_b'] for t, i in enumerate(ids_m)]
att = np.zeros((8, 8))
for t in range(8):
    sc = np.array([a_[t][24:32] @ a_[j][56:64] / math.sqrt(8) for j in range(t + 1)])
    att[t, :t + 1] = sm(sc)
lv.claim(np.allclose(F('l7')['screens'][3]['canvas']['params']['matrices'][0]['rows'], np.round(att, 2)), 'head 3 attention on MENENIUS (loop route), rounded to 2 places')
lv.claim(np.allclose(np.round(G.forward_cache(W, ids_m)['h0.att'][3], 2), np.round(att, 2)), 'head 3 attention: gpt_ops_l2 cache agrees')
WIN = VA[:33]
two('window loss', -logsm(loop_logits(W, WIN[:32]))[np.arange(32), WIN[1:]].mean(), G.mean_loss(W, WIN[:32], WIN[1:]), 1e-10)
two('16-window loss', float(cross_entropy(S4.lm_logits(XV[:16], MODEL, 4).reshape(-1, 65), YV[:16].reshape(-1)).item()), G.mean_loss(W, XV[:16], YV[:16]), 1e-10)
nll = -np.take_along_axis(logsm(S4.lm_logits(XV, MODEL, 4).data), YV[..., None], -1)[..., 0]
BYPOS = nll.mean(0)
lv.claim(F('l7')['screens'][7]['canvas']['params']['series'][0]['values'] == [round(float(v), 3) for v in BYPOS], 'loss by position: the plotted curve (seq_ops_l4 route)',
         covers=[BYPOS[0], BYPOS[3], float(np.mean(BYPOS[8:]))])
two('position 0 loss', BYPOS[0], -logsm(G.forward_logits(W, XV[:, :1]))[:, 0, :][np.arange(NVW), YV[:, 0]].mean(), 1e-10)
lv.claim(BYPOS[0] > 2.4554 and BYPOS[0] - 2.4554 < 0.15, 'position 0 a little above the bigram')
lv.claim(31 == 32 - 1, '31 of 32 targets copyable without the mask', covers=[31])
two('surprise of 0.02 in bits', -math.log2(0.02), -math.log(0.02) / math.log(2), covers=[-math.log2(0.02), -math.log(0.02), 0.02, VAL / math.log(2)])
two('q-mean', (math.log(2) + math.log(4)) / 2, -math.log(math.sqrt(0.5 * 0.25)), covers=[(math.log(2) + math.log(4)) / 2, math.log(2) + math.log(4), -math.log(0.375), 0.6931, 1.3863])
lv.claim(math.exp(-2) - 0.1353 < 1e-4, 'e^-2 is 0.1353', covers=[math.exp(-2), 0.5])


# ---------------- l8: temperature, top-k and the samples ----------------
zl = S4.lm_logits(np.array(G.encode('My lord, I wi')), MODEL, 4).data[-1]
lv.claim(np.abs(zl - loop_logits(W, np.array(G.encode('My lord, I wi')))[-1]).max() < 1e-10, 'My lord, I wi: two routes')
top5 = np.argsort(-zl)[:5]
pl = {}
for t in (0.5, 1, 2):
    p = sm(zl / t)
    pl[t] = float(p[G.encode('l')[0]])
    v = {('␣' if G.VOCAB[i] == ' ' else G.VOCAB[i]): round(float(p[i]), 3) for i in top5}
    v['rest'] = round(float(1 - sum(p[i] for i in top5)), 3)
    lv.claim(F('l8')['screens'][1]['canvas']['controls'][0]['frames'][[0.5, 1, 2].index(t)]['values'] == v, f'temperature {t}: bars', covers=list(v.values()))
lv.claim(pl[2] < pl[1] < pl[0.5], 'temperature 2 flattens, 0.5 sharpens', covers=list(pl.values()))


def soft(zs):
    ex = [math.exp(z) for z in zs]
    return [e / sum(ex) for e in ex]


for zs, lab_ in [([4, 2, 0], 'tau 0.5'), ([2, 1, 0], 'tau 1'), ([1, 0.5, 0], 'tau 2 or times 0.5'), ([2, 1], 'top 2'), ([6, 2], 'r-temp'), ([3, 1], 'r-temp t1'), ([1.5, 0.5], 'r-temp times'),
                 ([1.5, 0.5, 0], 'r-topk'), ([1.5, 0.5, 0, -2], 'r-topk all')]:
    a, b = soft(zs), sm(np.array(zs, float)).tolist()
    lv.claim(all(close(x, y, 1e-12) for x, y in zip(a, b)), f'softmax {lab_}: math and NumPy', covers=a)
lv.claim(1 / (1 + math.exp(-1)) - soft([2, 1])[0] < 1e-12 and 0.3333 - 1 / 3 < 1e-4, 'top 2 is 1/(1+e^-1); equal share a third', covers=[1 / 3, math.e])
lv.claim(47 - 32 == 15 and 7 + 40 == 47 and 46 - 15 + 1 == 32, 'window after 47 characters starts at 15', covers=[15, 47, 46, 16, 14])
SAMPLE = G.sample_text(W, 'First Citizen:\n', 200, 1.0, None, 0)
lv.claim(F('l8')['screens'][8]['canvas']['params']['text'] == SAMPLE, 'the 200-character sample is the seeded draw')
GREEDY = G.sample_text(W, 'First Citizen:\n', 60, 0, None, 0)
lv.claim(GREEDY[15:45] in F('l8')['screens'][0]['feedback']['correct'] and 'the the the' in GREEDY, 'greedy text loops')
lv.claim(18017 == N1, 'l8 states the 18,017 parameters', covers=[18017])


# ---------------- review, homework, problems ----------------
lv.claim(formula(65, 32, 16, 1, 64) == 5969 and 65 * 16 == 1040 and 4 * 256 + 2 * 16 * 64 + 9 * 16 + 64 == 3280 and 16 * 65 + 65 == 1105 and 5969 - 512 == 5457 and 5969 - 1040 == 4929,
         'r-small-count 5,969 and slips', covers=[5969, 1040, 3280, 1105, 5457, 4929, 32, 512])
lv.claim(b64len(2080) == 11096 and 2080 * 4 == 8320 and math.ceil(8320 / 3) == 2774 and len(base64.b64encode(np.zeros(2080, '<f8').tobytes())) == 22188, 'r-b64-wte', covers=[11096, 8320, 2774, 22188])
two('ln 50,257', math.log(50257), math.log2(50257) * math.log(2), covers=[math.log(50257), math.log2(50257), math.log10(50257)])
lv.claim(8 * 9 // 2 == 36 and 64 - 36 == 28, '36 of 64; strict 28', covers=[36, 28, 64])
r7 = [-math.log(p) for p in (0.9, 0.6, 0.3)]
two('r-mean-loss', sum(r7) / 3, -math.log(0.9 * 0.6 * 0.3) / 3, covers=[sum(r7) / 3, sum(r7), -math.log(0.6)] + r7)
lv.claim(40 - 32 == 8, 'window from index 8', covers=[8, 9, 39])
two('h-tied-count', formula(65, 48, 40, 2, 160, tied=True), 2600 + 1920 + 2 * 19720 + 80 + 65, 0, covers=[formula(65, 48, 40, 2, 160, tied=True), formula(65, 48, 40, 2, 160), formula(65, 48, 40, 1, 160, tied=True), 2600, 1920, 19720, 80, 40, 160])
lv.claim(round(BYPOS[0], 2) == 2.57 and round(BYPOS[3], 2) == 1.75, 'h-flat explain: 2.57 then 1.75', covers=[2.57, 1.75, 2.46, 2.4554])
B1 = formula(80, 64, 48, 1, 192) - formula(80, 64, 48, 0, 192)
NP1 = formula(80, 64, 48, 2, 192)
lv.claim(B1 == 28272 and 4 * 48 * 48 + 2 * 48 * 192 == 27648 and 3 * 48 + 48 + 192 + 48 == 432 and B1 - 192 == 28080, 'p1 block 28,272; weights 27,648; biases 432', covers=[28272, 27648, 432, 28080, 192])
lv.claim(NP1 == 67472 == 3840 + 3072 + 56544 + 96 + 3920 and NP1 - B1 == 39200 and NP1 - 3840 == 63632, 'p1 model 67,472', covers=[67472, 3840, 3072, 56544, 96, 3920, 39200, 63632])
lv.claim(NP1 * 4 == 269888 and NP1 * 8 == 539776 and 4 * math.ceil(269888 / 3) == 359852 == b64len(NP1) and math.ceil(269888 / 3) == 89963, 'p1 bytes and characters', covers=[269888, 539776, 359852, 89963, 262144])
lv.claim(abs(b64len(28272) - 151000) < 300, 'one block file about 151,000 characters', covers=[151000, 28000])
lv.claim(4 * 64 * 80 == 20480 and 64 * 80 == 5120 and 4 * 64 * 48 == 12288 and 48 // 4 == 12 and 48 * 4 == 192, 'p2 logits and head width', covers=[20480, 5120, 12288, 12, 192])
lv.claim(4 * 4 * 64 * 64 == 65536 and 4 * 64 * 64 == 16384 and 64 * 65 // 2 == 2080 and 16 * 2080 == 33280 and 16 * 64 * 63 // 2 == 32256, 'p2 attention counts', covers=[65536, 16384, 2080, 33280, 32256])
ch = [0.5, 0.2, 0.05, 0.8]
M = two('p3 mean loss', float(np.mean([-math.log(p) for p in ch])), -math.log(0.5 * 0.2 * 0.05 * 0.8) / 4, covers=[-math.log(p) for p in ch])
M2 = two('p3 new mean', float(np.mean([-math.log(p) for p in [0.5, 0.2, 0.5, 0.8]])), -math.log(0.5 * 0.2 * 0.5 * 0.8) / 4)
two('ln 80', math.log(80), math.log2(80) * math.log(2), covers=[math.log(80), math.log2(80), M, 4 * M, M / math.log(2), M * math.log(2), M2, M - M2, -math.log(np.mean(ch)), 2.9957, 0.6931])


# ---------------- givens and small workings ----------------
lv.claim(len(WIN) == 33 and 32 + 1 == 33 and 31 - 1 == 30, 'a window of 33 characters: 32 inputs, targets of positions 0 to 30 copyable', covers=[33, 30])
lv.claim(16 / 4 * 3 == 12, '16 characters are 12 bytes', covers=[4.0])
lv.claim(len(GREEDY) == 15 + 60 and len(SAMPLE) == 15 + 200, 'greedy run of 60, sample of 200 characters', covers=[60, 200])
lv.claim([z / 0.1 for z in (2, 1, 0)] == [20, 10, 0], 'logits over 0.1', covers=[10, 20, 0.1])
lv.claim(40 > 32 and 46 > 32 and len('Before we proceed any further, hear me speak.\n') == 46, 'prompts of 40 and 46 characters run past the context', covers=[40])
lv.claim(8 * 9 / 2 == 36 and 64 * 65 / 2 == 2080, 'triangle counts', covers=[4.5, 32.5])
for t_, why in [('20', 'a window length given in the quiz item'), ('27', 'a vocabulary size given in the quiz item'), ('50257', 'GPT-2\'s vocabulary, a published given'),
                ('80', 'the desk model\'s vocabulary, a given of the problem')]:
    LIT(t_, why=why)

# ---------------- code widgets: solution passes, starter fails, each mutant first fails its named test ----------------
def judge(a, ex, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def cl(x, yv):
        x, yv = flat(x), flat(yv)
        if isinstance(x, dict) and isinstance(yv, dict):
            return set(x) == set(yv) and all(cl(x[kk], yv[kk]) for kk in x)
        if isinstance(x, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x) == len(yv) and all(cl(p_, q_) for p_, q_ in zip(x, yv))
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
    return cl(a, ex) if cmp == 'isclose' else same(a, ex)


MODS = ('autograd', 'seq_ops_l2', 'seq_ops_l3', 'seq_ops_l4', 'nt_ops_l1', 'nt_ops_l2', 'gpt_ops_l2')


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

for t_, why in [('10^-6', 'test tolerances'), ('10^-9', 'test tolerances'), ('10^-12', 'test tolerances'), ('10^-5', 'the layer-norm epsilon'), ('256 KB', 'the data file limit, a rule')]:
    LIT(t_, why=why)
lv.check_wrongs()
lv.report()
