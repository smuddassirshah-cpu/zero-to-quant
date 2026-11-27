"""info and backprop brief numbers, each computed twice (method A, method B)."""
import os, sys
# names.txt: argument 1, else the app copy (engine A3), else ./dl/names.txt. MD5 401b3c4cac9e28a586ed15e81256680d.
_HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = next(p for p in ([sys.argv[1]] if len(sys.argv) > 1 else []) + [os.path.join(_HERE, '..', '..', '..', 'app', 'content', 'data', 'makemore', 'names.txt'), 'dl/names.txt'] if os.path.exists(p))

import math, heapq, itertools, random
from fractions import Fraction as F
import numpy as np

def check(label, a, b, tol=1e-9):
    if isinstance(a, (list, tuple)):
        ok = len(a) == len(b) and all(abs(x - y) <= tol * max(1, abs(x)) for x, y in zip(a, b))
    elif isinstance(a, float) or isinstance(b, float):
        ok = abs(a - b) <= tol * max(1, abs(a))
    else:
        ok = a == b
    print(('OK  ' if ok else 'FAIL'), label, a, '|', b); assert ok

L2 = math.log2
# ---------- info L1 ----------
check('surprisal 1/8', -L2(1 / 8), 3.0)
check('surprisal die', round(-L2(1 / 6), 4), round(math.log(6) / math.log(2), 4))
check('surprisal 0.9', round(-L2(0.9), 4), round(-math.log(0.9) / math.log(2), 4))
def H(p): return -sum(x * L2(x) for x in p if x > 0)
def H_nat_conv(p): return -sum(x * math.log(x) for x in p if x > 0) / math.log(2)
for p in [(0.5, 0.25, 0.125, 0.125), (0.4, 0.3, 0.2, 0.1), (0.25,) * 4, (0.9, 0.1), (0.5, 0.5), (0.7, 0.1, 0.1, 0.1)]:
    check(f'H{p}', round(H(p), 4), round(H_nat_conv(p), 4))
def huffman_lengths(p):
    h = [(x, i, (i,)) for i, x in enumerate(p)]; heapq.heapify(h); L = [0] * len(p); c = len(p)
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h)
        for s in a[2] + b[2]: L[s] += 1
        heapq.heappush(h, (a[0] + b[0], c, a[2] + b[2])); c += 1
    return L
def huffman_avg_B(p):
    # method B: the average length equals the sum of the merged weights
    q = sorted(p); tot = 0.0
    while len(q) > 1:
        a, b = q[0], q[1]; q = sorted(q[2:] + [a + b]); tot += a + b
    return tot
for p in [(0.5, 0.25, 0.125, 0.125), (0.4, 0.3, 0.2, 0.1), (0.7, 0.1, 0.1, 0.1)]:
    Ls = huffman_lengths(p); avg = sum(x * l for x, l in zip(p, Ls))
    print('huffman', p, Ls, 'avg', round(avg, 4), 'H', round(H(p), 4))
    check(f'huffman avg {p}', round(avg, 10), round(huffman_avg_B(p), 10))
    check(f'kraft {p}', sum(2 ** -l for l in Ls) <= 1 + 1e-12, True)
# names letters (unigram) and bigram conditional entropy
words = open(NAMES).read().splitlines()
seq = ''.join(w + '.' for w in words)
from collections import Counter
cnt = Counter(seq); N = len(seq)
Huni = H([v / N for v in cnt.values()])
Huni_B = (N * L2(N) - sum(v * L2(v) for v in cnt.values())) / N
check('names unigram entropy bits per char (letters + end)', round(Huni, 4), round(Huni_B, 4))
print('names: chars incl end marks', N, 'symbols', len(cnt), 'log2 27 =', round(L2(27), 4))
# ---------- info L2 ----------
def CE(p, q): return -sum(a * L2(b) for a, b in zip(p, q) if a > 0)
def KL(p, q): return sum(a * L2(a / b) for a, b in zip(p, q) if a > 0)
p = (0.5, 0.25, 0.125, 0.125); u = (0.25,) * 4
check('CE(p,u)', CE(p, u), 2.0); check('KL(p,u) = CE - H', round(KL(p, u), 10), round(CE(p, u) - H(p), 10))
check('KL(u,p)', round(KL(u, p), 10), round(CE(u, p) - H(u), 10)); print('KL(p,u), KL(u,p):', KL(p, u), KL(u, p))
a, b = (0.9, 0.1), (0.5, 0.5)
print('KL(a,b), KL(b,a) bits:', round(KL(a, b), 4), round(KL(b, a), 4))
check('KL(a,b) B', round(KL(a, b), 4), round((0.9 * math.log(1.8) + 0.1 * math.log(0.2)) / math.log(2), 4))
check('KL(b,a) B', round(KL(b, a), 4), round((0.5 * math.log(0.5 / 0.9) + 0.5 * math.log(5)) / math.log(2), 4))
# weather forecaster: truth (0.7, 0.2, 0.1), model (0.5, 0.3, 0.2)
t, m = (0.7, 0.2, 0.1), (0.5, 0.3, 0.2)
print('weather H, CE, KL bits:', round(H(t), 4), round(CE(t, m), 4), round(KL(t, m), 4))
check('weather CE = H + KL', round(CE(t, m), 10), round(H(t) + KL(t, m), 10))
# perplexity
check('perplexity of 2 bits', 2 ** 2.0, 4.0)
check('perplexity 2.4 nats', round(math.exp(2.4), 4), round(2 ** (2.4 / math.log(2)), 4))
print('nats to bits factor 1/ln2 =', round(1 / math.log(2), 6))
# MLE of a coin as least cross-entropy: data 7 heads of 10; CE(theta) minimised at 0.7
thetas = [k / 100 for k in range(1, 100)]
ce = [-(0.7 * L2(th) + 0.3 * L2(1 - th)) for th in thetas]
check('coin CE argmin', thetas[int(np.argmin(ce))], 0.7)
nll = [-(7 * math.log(th) + 3 * math.log(1 - th)) for th in thetas]
check('coin NLL argmin', thetas[int(np.argmin(nll))], 0.7)
print('coin CE at 0.7 bits', round(H((0.7, 0.3)), 4), 'at 0.5', round(-(0.7 * L2(0.5) + 0.3 * L2(0.5)), 4))

# ---------- backprop L1 ----------
a, b, c, f = 1.5, -2.0, 4.0, -3.0
def Lf(a, b, c, f): return (a * b + c) * f
e = a * b; d = e + c; Lv = d * f
grads = {'d': f, 'f': d, 'c': f, 'e': f, 'a': f * b, 'b': f * a}
print('bp L1 forward e, d, L:', e, d, Lv, 'grads', grads)
h = 1e-6
num = {k: (Lf(*[v + (h if n == k else 0) for n, v in zip('abcf', (a, b, c, f))]) - Lf(*[v - (h if n == k else 0) for n, v in zip('abcf', (a, b, c, f))])) / (2 * h) for k in 'abcf'}
for k in 'abcf': check(f'bp L1 dL/d{k}', round(num[k], 6), grads[k])
# forward nudge on a: L(a + 0.01) - L(a)
print('bp L1 nudge a by 0.01: change', round(Lf(a + 0.01, b, c, f) - Lv, 6), 'predicted', 0.01 * grads['a'])
# branch: g = (x + y) * x at (2, 3)
g = lambda x, y: (x + y) * x
check('bp L2 dg/dx', round((g(2 + h, 3) - g(2 - h, 3)) / (2 * h), 6), 7.0)
check('bp L2 dg/dy', round((g(2, 3 + h) - g(2, 3 - h)) / (2 * h), 6), 2.0)
# tanh example: o = tanh(w1 x1 + w2 x2 + b) at x=(2,0), w=(-3,1), b=6.8813735870195432 (Karpathy) -> use fresh numbers
x1, x2, w1, w2, bb = 1.0, -2.0, 0.5, 0.25, 0.3
n = x1 * w1 + x2 * w2 + bb; o = math.tanh(n); do_dn = 1 - o ** 2
print('bp L3 neuron n, o, do/dn:', n, round(o, 6), round(do_dn, 6))
check('bp L3 tanh B', round(o, 10), round((math.exp(2 * n) - 1) / (math.exp(2 * n) + 1), 10))
nf = lambda w1_: math.tanh(x1 * w1_ + x2 * w2 + bb)
check('bp L3 do/dw1 = x1 * (1 - o^2)', round((nf(w1 + h) - nf(w1 - h)) / (2 * h), 6), round(x1 * do_dn, 6))
# parameter counts
def nparams(sizes): return sum(a * b + b for a, b in zip(sizes, sizes[1:]))
for s in ([2, 3, 1], [3, 4, 4, 1], [2, 16, 16, 1], [2, 4, 1]):
    check(f'params {s}', nparams(s), sum(s[i] * s[i + 1] for i in range(len(s) - 1)) + sum(s[1:]))
    print('params', s, nparams(s))
# central vs forward difference error for tanh' at 0.5
x0 = 0.5; true = 1 - math.tanh(x0) ** 2
print('tanh\'(0.5) =', round(true, 6))
for hh in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8, 1e-10):
    fwd = (math.tanh(x0 + hh) - math.tanh(x0)) / hh; cen = (math.tanh(x0 + hh) - math.tanh(x0 - hh)) / (2 * hh)
    print(f'  h={hh:g} forward err {abs(fwd - true):.2e} central err {abs(cen - true):.2e}')
# method B for the h^2 law: f'''(x) h^2 / 6 with f''' of tanh = -2 sech^2 (sech^2 - 2 tanh^2)... use numeric third derivative
t0 = math.tanh(x0); s2 = 1 - t0 ** 2; f3 = -2 * s2 * (s2 - 2 * t0 ** 2)
hh = 1e-2; cen = (math.tanh(x0 + hh) - math.tanh(x0 - hh)) / (2 * hh)
check('central err ~ f\'\'\' h^2/6 at h=0.01', round(abs(cen - true), 8), round(abs(f3) * hh ** 2 / 6, 8), tol=2e-2)
# ---------- backprop L4: softmax cross-entropy ----------
z = np.array([2.0, 1.0, 0.1]); pz = np.exp(z - z.max()); pz /= pz.sum()
loss = -math.log(pz[0]); gz = pz.copy(); gz[0] -= 1
print('bp L4 softmax', np.round(pz, 4).tolist(), 'loss', round(loss, 4), 'grad', np.round(gz, 4).tolist())
num = []
for i in range(3):
    zp = z.copy(); zp[i] += h; zm = z.copy(); zm[i] -= h
    lp = -zp[0] + math.log(np.exp(zp).sum()); lm = -zm[0] + math.log(np.exp(zm).sum()); num.append((lp - lm) / (2 * h))
check('bp L4 softmax grad by central difference', np.round(num, 6).tolist(), np.round(gz, 6).tolist())
check('bp L4 loss via logsumexp', round(loss, 10), round(-z[0] + math.log(np.exp(z).sum()), 10))
# matmul backward: L = sum(W * (A @ B)) style -> use L = sum((A@B)**2)/2, dA = (AB) B^T
rng = np.random.default_rng(0)
A = rng.standard_normal((3, 4)); B = rng.standard_normal((4, 2))
G = A @ B; dA = G @ B.T; dB = A.T @ G
def Lab(A, B): return 0.5 * ((A @ B) ** 2).sum()
nA = np.zeros_like(A)
for i in range(3):
    for j in range(4):
        Ap = A.copy(); Ap[i, j] += 1e-5; Am = A.copy(); Am[i, j] -= 1e-5
        nA[i, j] = (Lab(Ap, B) - Lab(Am, B)) / 2e-5
rel = np.abs(nA - dA).max() / max(np.abs(nA).max(), np.abs(dA).max())
print('bp L4 matmul grad max relative error (h=1e-5, float64):', f'{rel:.1e}')
check('bp L4 matmul rel err below 1e-6', bool(rel < 1e-6), True)
# broadcast: y = X + b with X (5,3), b (3,), L = sum(y**2)/2, db = sum over axis 0 of y
X = rng.standard_normal((5, 3)); bvec = rng.standard_normal(3); Y = X + bvec
db = Y.sum(axis=0); nb = np.array([(0.5 * ((X + bvec + np.eye(3)[k] * 1e-5) ** 2).sum() - 0.5 * ((X + bvec - np.eye(3)[k] * 1e-5) ** 2).sum()) / 2e-5 for k in range(3)])
check('bp L4 broadcast grad', np.round(db, 6).tolist(), np.round(nb, 6).tolist())
# float32 vs float64 central difference on tanh MLP layer
for dt in (np.float64, np.float32):
    Xs = rng.standard_normal((4, 3)).astype(dt); Ws = rng.standard_normal((3, 2)).astype(dt)
    def Lt(W): return np.tanh(Xs @ W).sum()
    an = ((1 - np.tanh(Xs @ Ws) ** 2).T @ Xs).T
    hh = dt(1e-5) if dt == np.float64 else dt(1e-3)
    nm = np.zeros_like(Ws)
    for i in range(3):
        for j in range(2):
            Wp = Ws.copy(); Wp[i, j] += hh; Wm = Ws.copy(); Wm[i, j] -= hh
            nm[i, j] = (Lt(Wp) - Lt(Wm)) / (2 * hh)
    r = float(np.abs(nm - an).max() / np.abs(an).max())
    print(f'bp L4 tanh layer rel err {dt.__name__} h={float(hh):g}: {r:.1e}')

# backprop L3 l9: a saturated neuron
import math as _m
check('saturated tanh slope at 5', round(1 - _m.tanh(5) ** 2, 8), round(4 / (_m.exp(5) + _m.exp(-5)) ** 2, 8))
print('1 - tanh(5)^2 =', 1 - _m.tanh(5) ** 2)
