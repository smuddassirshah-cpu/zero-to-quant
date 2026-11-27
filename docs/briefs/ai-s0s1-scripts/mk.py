"""makemore brief numbers. Method A: NumPy arrays; method B: plain Python dicts (bigram) or a second implementation."""
import os, sys
# names.txt: argument 1, else the app copy (engine A3), else ./dl/names.txt. MD5 401b3c4cac9e28a586ed15e81256680d.
_HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = next(p for p in ([sys.argv[1]] if len(sys.argv) > 1 else []) + [os.path.join(_HERE, '..', '..', '..', 'app', 'content', 'data', 'makemore', 'names.txt'), 'dl/names.txt'] if os.path.exists(p))

import math, time
from collections import Counter
import numpy as np

def check(label, a, b, tol=1e-9):
    ok = abs(a - b) <= tol * max(1, abs(a)) if isinstance(a, float) else a == b
    print(('OK  ' if ok else 'FAIL'), label, a, '|', b); assert ok

words = open(NAMES).read().splitlines()
chars = sorted(set(''.join(words))); stoi = {s: i + 1 for i, s in enumerate(chars)}; stoi['.'] = 0; itos = {i: s for s, i in stoi.items()}
print('names', len(words), 'chars', len(chars), 'shortest', min(len(w) for w in words), 'longest', max(len(w) for w in words), 'mean len', round(sum(map(len, words)) / len(words), 4))
def bigrams(ws):
    for w in ws:
        cs = ['.'] + list(w) + ['.']
        for a, b in zip(cs, cs[1:]): yield a, b
allb = list(bigrams(words)); print('bigrams', len(allb), 'check', sum(len(w) + 1 for w in words))
C = Counter(allb); top = C.most_common(5); print('top bigrams', top)
print('first letters top 3', Counter(w[0] for w in words).most_common(3), 'last letters top 3', Counter(w[-1] for w in words).most_common(3))
N = np.zeros((27, 27), dtype=np.int64)
for a, b in allb: N[stoi[a], stoi[b]] += 1
check('count n then end', int(N[stoi['n'], 0]), C[('n', '.')])
print('zero cells', int((N == 0).sum()), 'of 729')
def nll_counts(Ncnt, ws, alpha=1):
    P = (Ncnt + alpha) / (Ncnt + alpha).sum(1, keepdims=True)
    s = 0.0; n = 0
    for a, b in bigrams(ws): s -= math.log(P[stoi[a], stoi[b]]); n += 1
    return s / n
def nll_counts_B(ws_train, ws_eval, alpha=1):
    # method B: dict counts, no arrays
    row = Counter(); pair = Counter()
    for a, b in bigrams(ws_train): row[a] += 1; pair[(a, b)] += 1
    s = 0.0; n = 0
    for a, b in bigrams(ws_eval):
        s -= math.log((pair[(a, b)] + alpha) / (row[a] + 27 * alpha)); n += 1
    return s / n
full = nll_counts(N, words); check('bigram nll full data +1', round(full, 4), round(nll_counts_B(words, words), 4))
check('bigram nll full data no smoothing', round(nll_counts(N, words, 0), 4), round(nll_counts_B(words, words, 0), 4))
print('full nll nats', round(full, 4), 'bits', round(full / math.log(2), 4), 'perplexity', round(math.exp(full), 4))
print('uniform nll ln 27 =', round(math.log(27), 4))
# a name's probability: "emma"
P1 = (N + 1) / (N + 1).sum(1, keepdims=True)
lp = sum(math.log(P1[stoi[a], stoi[b]]) for a, b in bigrams(['emma']))
print('emma log prob', round(lp, 4), 'avg nll', round(-lp / 5, 4))
# splits
rng = np.random.default_rng(42); perm = rng.permutation(len(words)); n1, n2 = int(0.8 * len(words)), int(0.9 * len(words))
tr = [words[i] for i in perm[:n1]]; dv = [words[i] for i in perm[n1:n2]]; te = [words[i] for i in perm[n2:]]
print('split sizes', len(tr), len(dv), len(te), 'first train names', tr[:3])
Ntr = np.zeros((27, 27), dtype=np.int64)
for a, b in bigrams(tr): Ntr[stoi[a], stoi[b]] += 1
for nm, ws in (('train', tr), ('dev', dv), ('test', te)):
    v = nll_counts(Ntr, ws); check(f'bigram(+1, train counts) {nm}', round(v, 4), round(nll_counts_B(tr, ws), 4))
for al in (0.01, 0.1, 1, 10, 100):
    print(f'  smoothing {al}: train {nll_counts(Ntr, tr, al):.4f} dev {nll_counts(Ntr, dv, al):.4f}')
# one-layer net on bigrams of the first 500 train names, full batch, lr 50
def xy(ws):
    xs, ys = [], []
    for a, b in bigrams(ws): xs.append(stoi[a]); ys.append(stoi[b])
    return np.array(xs), np.array(ys)
def train_net(ws, steps, lr, seed=2147483647, reg=0.0):
    xs, ys = xy(ws); W = np.random.default_rng(seed).standard_normal((27, 27)); out = []
    for k in range(steps):
        logits = W[xs]; logits = logits - logits.max(1, keepdims=True); p = np.exp(logits); p /= p.sum(1, keepdims=True)
        loss = -np.log(p[np.arange(len(ys)), ys]).mean() + reg * (W ** 2).mean(); out.append(loss)
        g = p; g[np.arange(len(ys)), ys] -= 1; g /= len(ys)
        dW = np.zeros_like(W); np.add.at(dW, xs, g); dW += reg * 2 * W / W.size
        W -= lr * dW
    return W, out
sub = tr[:500]; xs_s, _ = xy(sub); print('subset bigrams', len(xs_s))
t0 = time.time(); W, losses = train_net(sub, 100, 50.0); t1 = time.time()
Nsub = np.zeros((27, 27), dtype=np.int64)
for a, b in bigrams(sub): Nsub[stoi[a], stoi[b]] += 1
print('net on 500 names: loss at steps 0, 10, 50, 100:', [round(losses[i], 4) for i in (0, 10, 50, 99)], f'({t1 - t0:.3f} s native)')
print('  count model on the same 500 names, no smoothing:', round(nll_counts(Nsub, sub, 0), 4), '+1:', round(nll_counts(Nsub, sub, 1), 4))
t0 = time.time(); Wf, lf = train_net(tr, 10, 50.0); print(f'full train set 10 steps {time.time() - t0:.3f} s native, loss {lf[-1]:.4f}')

# ---------- MLP (Bengio 2003 shape) ----------
def build(ws, block=3):
    X, Y = [], []
    for w in ws:
        ctx = [0] * block
        for ch in w + '.':
            ix = stoi[ch]; X.append(ctx); Y.append(ix); ctx = ctx[1:] + [ix]
    return np.array(X), np.array(Y)
Xtr, Ytr = build(tr); Xdv, Ydv = build(dv); Xte, Yte = build(te)
print('MLP examples train/dev/test', len(Xtr), len(Xdv), len(Xte))
def init(seed, emb=10, hid=100, block=3):
    g = np.random.default_rng(seed)
    return {'C': g.standard_normal((27, emb)), 'W1': g.standard_normal((block * emb, hid)) * (5 / 3) / math.sqrt(block * emb),
            'b1': np.zeros(hid), 'W2': g.standard_normal((hid, 27)) * 0.01, 'b2': np.zeros(27)}
def forward(P, X, Y=None):
    E = P['C'][X].reshape(len(X), -1); hpre = E @ P['W1'] + P['b1']; h = np.tanh(hpre); logits = h @ P['W2'] + P['b2']
    m = logits - logits.max(1, keepdims=True); lse = np.log(np.exp(m).sum(1));
    if Y is None: return logits
    loss = (lse - m[np.arange(len(Y)), Y]).mean()
    return loss, (E, h, m, lse)
def step(P, X, Y, lr):
    loss, (E, h, m, lse) = forward(P, X, Y)
    p = np.exp(m - lse[:, None]); p[np.arange(len(Y)), Y] -= 1; dl = p / len(Y)
    dW2 = h.T @ dl; db2 = dl.sum(0); dh = dl @ P['W2'].T; dhp = dh * (1 - h ** 2)
    dW1 = E.T @ dhp; db1 = dhp.sum(0); dE = (dhp @ P['W1'].T).reshape(len(X), X.shape[1], -1)
    dC = np.zeros_like(P['C']); np.add.at(dC, X, dE)
    for k, g in (('C', dC), ('W1', dW1), ('b1', db1), ('W2', dW2), ('b2', db2)): P[k] -= lr * g
    return loss
P = init(0); print('MLP params', sum(v.size for v in P.values()))
check('MLP params formula', sum(v.size for v in P.values()), 27 * 10 + 30 * 100 + 100 + 100 * 27 + 27)
print('MLP initial dev loss', round(forward(P, Xdv, Ydv)[0], 4), 'ln 27', round(math.log(27), 4))
g = np.random.default_rng(1); t0 = time.time(); marks = {}
for k in range(1, 40001):
    ix = g.integers(0, len(Xtr), 32); lr = 0.1 if k <= 30000 else 0.01
    step(P, Xtr[ix], Ytr[ix], lr)
    if k in (200, 1000, 3000, 10000, 20000, 30000, 40000):
        marks[k] = (round(forward(P, Xtr, Ytr)[0], 4), round(forward(P, Xdv, Ydv)[0], 4))
print(f'MLP 40k steps native {time.time() - t0:.1f} s; (train, dev) at steps', marks)
print('MLP test loss', round(forward(P, Xte, Yte)[0], 4))
# method B for the final dev loss: a loop over examples in plain NumPy rows
s = 0.0
for xrow, y in zip(Xdv[:2000], Ydv[:2000]):
    e = P['C'][xrow].reshape(-1); hh = np.tanh(e @ P['W1'] + P['b1']); lg = hh @ P['W2'] + P['b2']
    s += math.log(np.exp(lg - lg.max()).sum()) + lg.max() - lg[y]
check('MLP dev loss on first 2000 dev rows, two ways', round(s / 2000, 6), round(forward(P, Xdv[:2000], Ydv[:2000])[0], 6), tol=1e-7)
# learning-rate sweep: 1000 steps from the same init, dev loss
for lr in (0.001, 0.01, 0.1, 0.3, 1.0):
    Q = init(0); gg = np.random.default_rng(1)
    for k in range(1000):
        ix = gg.integers(0, len(Xtr), 32); step(Q, Xtr[ix], Ytr[ix], lr)
    print(f'  sweep lr {lr}: dev after 1000 steps {forward(Q, Xdv, Ydv)[0]:.4f}')
# overfitting: big hidden layer on 1000 train names
small = tr[:1000]; Xs, Ys = build(small); Q = init(0, emb=10, hid=300); gg = np.random.default_rng(1); hist = {}
for k in range(1, 20001):
    ix = gg.integers(0, len(Xs), 32); step(Q, Xs[ix], Ys[ix], 0.1)
    if k in (1000, 3000, 5000, 10000, 20000): hist[k] = (round(forward(Q, Xs, Ys)[0], 4), round(forward(Q, Xdv, Ydv)[0], 4))
print('overfit: 1000 names, hidden 300, (train, dev) at steps', hist, 'examples', len(Xs))
# sampling with temperature from the trained MLP
def sample(P, seed, T=1.0, n=5):
    gg = np.random.default_rng(seed); out = []
    for _ in range(n):
        ctx = [0, 0, 0]; s = ''
        while True:
            lg = forward(P, np.array([ctx]))[0] / T; p = np.exp(lg - lg.max()); p /= p.sum()
            ix = gg.choice(27, p=p)
            if ix == 0: break
            s += itos[ix]; ctx = ctx[1:] + [ix]
        out.append(s)
    return out
for T in (0.5, 1.0, 1.5): print('samples T', T, sample(P, 7, T))
# fraction of T=1 samples that are training names
smp = sample(P, 11, 1.0, 500); trs = set(tr)
print('share of 500 samples that are train names', round(sum(s in trs for s in smp) / 500, 3))
