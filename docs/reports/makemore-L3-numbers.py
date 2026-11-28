"""Recompute every number stated in makemore level 3 (Sampling and held-out loss) and check each value at its JSON path.

Run: <venv>/bin/python docs/reports/makemore-L3-numbers.py   (NumPy and the standard library; under a minute; exits 0 when every check passes)

Route A: NumPy (searchsorted sampling, vectorised losses, softmax of z/T, hand gradients). Route B: plain loops (a running-total
walk for sampling, row-by-row losses, chances raised to 1/T, the shipped autograd for the short run). All MLP figures come from
the supplied weights app/content/data/ai/makemore-mlp.json (written by makemore-L2-numbers.py).
The topic exit (makemore is topic 1.12's third exit): the MLP's dev and test losses beat the bigram's; both are printed below.
"""
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

DATA = os.path.join(ROOT, 'app', 'content', 'data', 'ai')
CANON = open(os.path.join(DATA, 'autograd.py'), encoding='utf8').read()
sys.path.insert(0, DATA)
from autograd import Tensor, cross_entropy, sgd_step  # noqa: E402

lv = Level('makemore', 3)
E = lv.expect
F = lambda ref: lv._file(ref)[1]  # noqa: E731


def two(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol * max(1.0, abs(a)), f'{label}: routes agree ({a!r} vs {b!r})')
    return a


W = open(os.path.join(DATA, 'names.txt')).read().splitlines()
SYM = '.abcdefghijklmnopqrstuvwxyz'; IX = {c: i for i, c in enumerate(SYM)}
perm = np.random.default_rng(42).permutation(len(W))
tr = [W[i] for i in perm[:25626]]; dv = [W[i] for i in perm[25626:28829]]; te = [W[i] for i in perm[28829:]]
R = {k: np.array(v) for k, v in json.load(open(os.path.join(DATA, 'makemore-mlp.json'))).items() if k != 'about'}


def build(ws, block=3):
    X, Y = [], []
    for w in ws:
        ctx = [0] * block
        for ch in w + '.':
            X.append(ctx); Y.append(IX[ch]); ctx = ctx[1:] + [IX[ch]]
    return np.array(X), np.array(Y)


Xtr, Ytr = build(tr); Xdv, Ydv = build(dv); Xte, Yte = build(te)


def logits(P, X):
    return np.tanh(P['C'][np.asarray(X)].reshape(len(X), -1) @ P['W1'] + P['b1']) @ P['W2'] + P['b2']


def loss(P, X, Y, T=1.0):
    z = logits(P, X) / T; m = z.max(1, keepdims=True)
    return float((np.log(np.exp(z - m).sum(1)) + m[:, 0] - z[np.arange(len(Y)), Y]).mean())


def loss_powB(P, X, Y, T):   # route B: chances raised to 1/T and rescaled
    z = logits(P, X); p = np.exp(z - z.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    q = p ** (1 / T); q /= q.sum(1, keepdims=True)
    return float(-np.log(q[np.arange(len(Y)), Y]).mean())


def mlp_p(ctx, T=1.0):
    z = logits(R, [ctx])[0] / T; p = np.exp(z - z.max()); return p / p.sum()


def pick_A(p, u):
    return min(int(np.searchsorted(np.cumsum(p), u, side='right')), 26)


def pick_B(p, u):   # walk the running total
    s = 0.0
    for i, x in enumerate(p):
        s += x
        if s > u:
            return i
    return 26


def sample(prob_fn, rng, pick, max_len=20):
    ctx = [0, 0, 0]; s = ''
    while len(s) < max_len:
        ix = pick(prob_fn(ctx), rng.random())
        if ix == 0:
            break
        s += SYM[ix]; ctx = ctx[1:] + [ix]
    return s


Nt = np.zeros((27, 27))
for w in tr:
    cs = '.' + w + '.'
    for a, b in zip(cs, cs[1:]):
        Nt[IX[a], IX[b]] += 1
Pb = (Nt + 1) / (Nt + 1).sum(1, keepdims=True)
big = lambda c: Pb[c[-1]]  # noqa: E731


def big_loss_B(ws):
    rows = Counter(); pairs = Counter()
    for w in tr:
        cs = '.' + w + '.'
        for a, b in zip(cs, cs[1:]):
            rows[a] += 1; pairs[(a, b)] += 1
    s = n = 0
    for w in ws:
        cs = '.' + w + '.'
        for a, b in zip(cs, cs[1:]):
            s -= math.log((pairs[(a, b)] + 1) / (rows[a] + 27)); n += 1
    return s / n


# ---------------- the topic exit ----------------
bl = {nm: two(f'bigram {nm}', float(-np.mean([math.log(Pb[x[-1], y]) for x, y in zip(*build(ws, 1))])), big_loss_B(ws), 1e-12) for nm, ws in (('train', tr), ('dev', dv), ('test', te))}
ml = {'train': loss(R, Xtr, Ytr), 'dev': loss(R, Xdv, Ydv), 'test': loss(R, Xte, Yte)}
two('MLP dev, vectorised and through the 1/T route at T = 1', ml['dev'], loss_powB(R, Xdv, Ydv, 1.0), 1e-9)
print(f"TOPIC EXIT: bigram dev {bl['dev']:.4f}, test {bl['test']:.4f}; MLP dev {ml['dev']:.4f}, test {ml['test']:.4f}")
lv.claim([round(bl[k], 4) for k in ('train', 'dev', 'test')] == [2.4536, 2.4514, 2.4702], 'bigram 2.4536, 2.4514, 2.4702')
lv.claim([round(ml[k], 4) for k in ('train', 'dev', 'test')] == [2.1356, 2.1609, 2.1742], 'MLP 2.1356, 2.1609, 2.1742')
lv.claim(ml['dev'] < bl['dev'] and ml['test'] < bl['test'], 'topic exit: the MLP beats the bigram on dev and test')

# ---------------- l9 ----------------
L9 = 'l9-sampling-names'
for label, fn, key in (('bigram', big, 0), ('MLP', mlp_p, 1)):
    a = sample_list = [sample(fn, rng, pick_A) for rng in [np.random.default_rng(3)] for _ in range(6)]
    rngB = np.random.default_rng(3); b = [sample(fn, rngB, pick_B) for _ in range(6)]
    lv.claim(a == b and F(L9)['screens'][0]['canvas']['params']['lines'][key].endswith(', '.join(a)), f'{label} samples, seed 3, two pickers: {a}')
s500 = [sample(mlp_p, r, pick_A) for r in [np.random.default_rng(11)] for _ in range(500)]
rB = np.random.default_rng(11); s500B = [sample(mlp_p, rB, pick_B) for _ in range(500)]
lv.claim(s500 == s500B, '500 MLP samples, two pickers')
trs = set(tr); sh = sum(s in trs for s in s500) / 500
b500 = [sample(big, r, pick_A) for r in [np.random.default_rng(11)] for _ in range(500)]; bsh = sum(s in trs for s in b500) / 500
lv.claim(round(sh * 100, 1) == 19.4 and round(bsh * 100, 1) == 9.8, f'shares of training names: MLP {sh}, bigram {bsh}')
E(L9, 'screens[4].prose', 19.4); E(L9, 'screens[4].prose', 9.8); E(L9, 'screens[4].widget.options[1].why', 80.6)
lv.claim(sum(len(s) == 20 for s in s500) == 2, 'two of 500 MLP samples hit the cap'); E(L9, 'screens[6].prose', 2)
ctx = [0, 0, 0]; am = ''
for _ in range(20):
    ix = int(np.argmax(mlp_p(ctx)))
    if ix == 0:
        break
    am += SYM[ix]; ctx = ctx[1:] + [ix]
lv.claim(am == 'alee', 'argmax writes alee'); E(L9, 'screens[5].feedback.correct', 'alee')
TOY = {0: [0, 0.5, 0.3, 0.2], 1: [0.4, 0.1, 0.3, 0.2], 2: [0.3, 0.5, 0.0, 0.2], 3: [0.6, 0.2, 0.2, 0.0]}
toy = lambda c: np.array(TOY[c[-1]] + [0.0] * 23)  # noqa: E731


class FixedU:
    def __init__(self, us):
        self.us = list(us)

    def random(self):
        return self.us.pop(0)


lv.claim(sample(toy, FixedU([0.62, 0.35, 0.40, 0.15]), pick_A) == 'baa' == sample(toy, FixedU([0.62, 0.35, 0.40, 0.15]), pick_B), 'hand sample baa, two pickers')
lv.claim(pick_A(np.array([0.1, 0.6, 0.3]), 0.45) == 1 and pick_A(np.array([0.1, 0.6, 0.3]), 0.7) == 2 == pick_B(np.array([0.1, 0.6, 0.3]), 0.7), 'quiz: 0.45 picks a, 0.7 picks b')
ten = np.zeros(27); ten[17:] = 0.1
lv.claim(np.cumsum([0.1] * 10)[-1] == 0.9999999999999999 and int(np.searchsorted(np.cumsum(ten), 0.9999999999999999, side='right')) == 27, 'ten 0.1s end at 0.9999999999999999; searchsorted gives 27')
lv.claim(max(len(w) for w in W) == 15, 'longest real name: 15 letters')

# ---------------- l10 ----------------
L10 = 'l10-train-dev-test'
lv.claim((len(tr), len(dv), len(te)) == (25626, 3203, 3204) and tr[:3] == ['briah', 'xzayvion', 'amad'], 'split sizes and first training names')
E(L10, 'screens[3].widget.answer', round(2.4702 - round(ml['test'], 4), 4)); E(L10, 'screens[3].widget.wrong[0].value', round(2.4514 - round(ml['dev'], 4), 4))
E(L10, 'screens[3].widget.wrong[1].value', round(2.4536 - round(ml['train'], 4), 4))
dup = sum(w in trs for w in dv); dupB = len([w for w in dv if w in set(tr)])
lv.claim(dup == dupB == 390 and len(set(W)) == 29494, f'{dup} dev names also in training; 29,494 different names')
E(L10, 'screens[6].widget.answer', round(dup / 3203, 2)); E(L10, 'screens[6].widget.wrong[0].value', round(1 - 29494 / 32033, 2))
lv.claim(round(bl['test'] - bl['dev'], 3) == 0.019 and round(bl['train'] - bl['dev'], 4) == 0.0022, 'bigram: dev 0.0022 below train')
p5 = np.random.default_rng(42).permutation(5000); lv.claim(len(p5[int(0.9 * 5000):]) == 500, 'quiz: 5,000 names give 500 test')

# ---------------- l11 ----------------
L11 = 'l11-overfitting'


def init(seed, emb=10, hid=100, block=3):
    g = np.random.default_rng(seed)
    return {'C': g.standard_normal((27, emb)), 'W1': g.standard_normal((block * emb, hid)) * (5 / 3) / math.sqrt(block * emb),
            'b1': np.zeros(hid), 'W2': g.standard_normal((hid, 27)) * 0.01, 'b2': np.zeros(27)}


def step(P, X, Y, lr):
    Em = P['C'][X].reshape(len(X), -1); h = np.tanh(Em @ P['W1'] + P['b1']); z = h @ P['W2'] + P['b2']
    p = np.exp(z - z.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); p[np.arange(len(Y)), Y] -= 1; dz = p / len(Y)
    dW2 = h.T @ dz; db2 = dz.sum(0); dpre = (dz @ P['W2'].T) * (1 - h ** 2); dW1 = Em.T @ dpre; db1 = dpre.sum(0)
    dE = (dpre @ P['W1'].T).reshape(X.shape[0], X.shape[1], -1); dC = np.zeros_like(P['C']); np.add.at(dC, X, dE)
    for k, gr in (('C', dC), ('W1', dW1), ('b1', db1), ('W2', dW2), ('b2', db2)):
        P[k] -= lr * gr


Xs, Ys = build(tr[:1000]); lv.claim(len(Xs) == 7226, '1,000 names give 7,226 rows')
Q = init(0, hid=300); lv.claim(sum(v.size for v in Q.values()) == 17697, 'hidden 300: 17,697 weights (about 18,000)')
g = np.random.default_rng(1); oc = []
for k in range(1, 20001):
    ix = g.integers(0, len(Xs), 32); step(Q, Xs[ix], Ys[ix], 0.1)
    if k % 250 == 0:
        oc.append((k, loss(Q, Xs, Ys), loss(Q, Xdv, Ydv)))
ser = F(L11)['screens'][1]['canvas']['params']
lv.claim(len(oc) == 80 and all(abs(a - c[1]) < 1e-3 and abs(b - c[2]) < 1e-3 for a, b, c in zip(ser['series'][0]['values'], ser['series'][1]['values'], oc)), 'overfitting curve matches a fresh run')
at = {k: (round(a, 4), round(b, 4)) for k, a, b in oc}
lv.claim([at[k] for k in (1000, 3000, 5000, 10000, 20000)] == [(2.2935, 2.4586), (2.044, 2.5016), (1.9043, 2.645), (1.664, 2.8568), (1.5534, 3.0981)], 'recorded points of the brief')
bst = min(oc, key=lambda r: r[2]); lv.claim(bst[0] == 2000 and round(bst[2], 4) == 2.4568 and min(r[2] for r in oc) > 2.4514, 'least dev at step 2,000, 2.4568, never below the bigram')
E(L11, 'screens[2].widget.answer', round(at[20000][1] - at[20000][0], 4)); E(L11, 'screens[3].widget.answer', round(at[5000][1] - at[5000][0], 4))
E(L11, 'screens[5].explain.text', 0.74); E(L11, 'screens[5].explain.text', 0.64)
lv.claim(round(182531 / 7226) == 25, '25 times the rows')
X2, Y2 = build(tr[:200]); P2 = init(0); g2 = np.random.default_rng(1)
for _ in range(200):
    ix = g2.integers(0, len(X2), 32); step(P2, X2[ix], Y2[ix], 0.1)
TA = {k: Tensor(v.copy()) for k, v in init(0).items()}; g3 = np.random.default_rng(1)
for _ in range(200):
    ix = g3.integers(0, len(X2), 32)
    L = cross_entropy((TA['C'][X2[ix]].reshape(32, -1) @ TA['W1'] + TA['b1']).tanh() @ TA['W2'] + TA['b2'], Y2[ix])
    for t in TA.values():
        t.zero_grad()
    L.backward(); sgd_step(list(TA.values()), 0.1)
s_tr = two('short run train loss, hand and autograd', loss(P2, X2, Y2), loss({k: t.data for k, t in TA.items()}, X2, Y2), 1e-9); s_dv = loss(P2, Xdv, Ydv)
lv.claim(round(s_tr, 4) == 2.423 and round(s_dv, 4) == 2.655 and s_tr < 2.54 and s_dv - s_tr > 0.1, f'short run: train {s_tr:.4f}, dev {s_dv:.4f}; thresholds 2.54 and 0.1 hold with a margin')
X30, Y30 = build(tr[:30]); Xd30, Yd30 = build(dv[:30])
P30 = init(0); g30 = np.random.default_rng(2)
for _ in range(5):
    ix = g30.integers(0, len(X30), 32); step(P30, X30[ix], Y30[ix], 0.1)
T30 = {k: Tensor(v.copy()) for k, v in init(0).items()}; g31 = np.random.default_rng(2)
for _ in range(5):
    ix = g31.integers(0, len(X30), 32)
    L = cross_entropy((T30['C'][X30[ix]].reshape(32, -1) @ T30['W1'] + T30['b1']).tanh() @ T30['W2'] + T30['b2'], Y30[ix])
    for t in T30.values():
        t.zero_grad()
    L.backward(); sgd_step(list(T30.values()), 0.1)
two('5 steps on 30 names, hand and autograd', loss(P30, X30, Y30), loss({k: t.data for k, t in T30.items()}, X30, Y30), 1e-10)
lv.claim(F(L11)['screens'][7]['widget']['tests'][5]['expect'] == repr([round(loss(P30, X30, Y30), 6), round(loss(P30, Xd30, Yd30), 6)]), 'exact short-run test of fit_and_gap')

# ---------------- l12 ----------------
L12 = 'l12-temperature'
for T in (0.5, 1.0, 1.5):
    rng = np.random.default_rng(7); a = [sample(lambda c: mlp_p(c, T), rng, pick_A) for _ in range(5)]
    lv.claim(a == {0.5: ['ken', 'arah', 'halee', 'kyris', 'ana'], 1.0: ['mora', 'sarlee', 'daniyahsa', 'lacierah', 'dakole'], 1.5: ['muradu', 'stie', 'emjlzonza', 'mabheuncha', 'claj']}[T], f'samples at T = {T}: {a}')
for T in (0.5, 1.0, 2.0):
    p = mlp_p([0, 0, 0], T); z = logits(R, [[0, 0, 0]])[0]; q = np.exp(z - z.max()); q /= q.sum(); qB = q ** (1 / T); qB /= qB.sum()
    lv.claim(np.allclose(p, qB), f'first letters at T = {T}: softmax(z/T) equals p^(1/T) rescaled')
    shown = F(L12)['screens'][1]['canvas']['controls'][0]['frames'][[0.5, 1.0, 2.0].index(T)]['values']
    lv.claim(all(abs(shown[c] - p[IX[c]]) < 5e-5 for c in shown), f'bars at T = {T}')
DT = {T: two(f'dev loss at T = {T}', loss(R, Xdv, Ydv, T), loss_powB(R, Xdv, Ydv, T), 1e-9) for T in (0.5, 0.9, 1.0, 1.01, 1.1, 1.5, 2.0, 100.0)}
rows = F(L12)['screens'][4]['canvas']['params']['rows']
lv.claim(all(abs(float(r[1]) - DT[float(r[0])]) < 5e-5 for r in rows), 'dev loss table')
grid = [(loss(R, Xdv, Ydv, T), T) for T in np.round(np.arange(0.8, 1.2001, 0.01), 2)]
lv.claim(min(grid)[1] == 1.01 and round(DT[1.0] - DT[1.01], 5) == 0.00007, f'least dev loss at T = 1.01, {DT[1.0] - DT[1.01]:.6f} below T = 1')
E(L12, 'screens[2].widget.answer', round(0.25 / 0.38, 4)); E(L12, 'screens[3].prose', round(DT[100.0], 4))
E(L12, 'quiz[1].widget.answer', round(0.36 / 0.52, 4))

# ---------------- review-3, homework-3, problems-3 ----------------
lv.claim(pick_A(np.array([0.2, 0.5, 0.3]), 0.65) == 1 and pick_A(np.array([0.2, 0.5, 0.3]), 0.2) == 1, 'review: 0.65 and 0.2 both pick a')
E('review', 'items[4].widget.answer', round(0.49 / 0.58, 4))
E('homework', 'items[3].widget.answer', round(0.8 / 1.4, 4)); E('homework', 'items[3].widget.wrong[0].value', round(0.64 ** 2 / (0.64 ** 2 + 0.36 ** 2), 4))
lv.claim([round(DT[T], 4) for T in (0.5, 1.0, 1.5)] == [2.5456, 2.1609, 2.2392], 'homework temperatures 2.5456, 2.1609, 2.2392')
E('homework', 'items[1].explain.text', 2.5456); E('homework', 'items[1].explain.text', 2.2392)
lv.claim(sum(r['points'] for r in F('homework-3')['items'][5]['rubric']) == 10, 'longform rubric sums to 10')
d500, t500 = dv[:500], te[:500]
X5, Y5 = build(d500); X5t, Y5t = build(t500)
lv.claim(loss(R, X5, Y5) < 2.4514, f'MLP on the first 500 dev names: {loss(R, X5, Y5):.4f}, below 2.4514')
q = np.array([0.1, 0.4, 0.3, 0.2]); q2 = q ** 2 / (q ** 2).sum()
E('problems', 'items[0].parts[2].widget.answer', round(float(q2[1]), 4))
lv.claim(pick_A(q, 0.55) == 2 and pick_A(q2, 0.55) == 1, 'problems: 0.55 picks b at T = 1 and a at T = 1/2')
E('problems', 'items[1].parts[1].widget.answer', round(2.44 - 2.18, 2)); E('problems', 'items[1].parts[2].widget.answer', round(2.58 - 2.44, 2))
E('problems', 'items[2].parts[0].widget.answer', int(0.8 * 4500)); E('problems', 'items[2].parts[1].widget.answer', 4500 - int(0.9 * 4500))

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
lv.claim(all(hashlib.sha256(s.encode('utf8')).hexdigest() == sha for s in shipped), f'every shipped autograd.py ({len(shipped)}) is byte-identical (level 3 trains with a NumPy loop in l11, so it may ship none)')


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
        import signal

        def _stop(*_):
            raise TimeoutError('case ran past 20 s')
        signal.signal(signal.SIGALRM, _stop)
        with np.errstate(all='ignore'):
            for i, t in enumerate(w['tests']):
                signal.alarm(20)   # a mutant marked "timeout" loops for ever; the app stops it after 5 s
                try:
                    ok = passes(t, ns)
                finally:
                    signal.alarm(0)
                if not ok:
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
