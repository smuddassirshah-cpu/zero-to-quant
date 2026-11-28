"""representations level 1 (Embeddings): every stated number recomputed by a second route.

Route A is the generator (NumPy, the autograd); route B here is independent: pure-Python loops and Fractions for the small
cases, a hand-written NumPy gradient against the autograd for the fits, scikit-learn's KMeans for the clusters, and every
code widget's hidden tests rerun twice in CPython: once with the model solution and once with a separate loop-based
implementation of the same functions. Run with the venv Python (NumPy 2.0.2, scikit-learn 1.6.1); strict coverage.
"""
import json, math, os, sys, hashlib
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
sys.path.insert(0, DATA)
import numpy as np
from numbers_lib import Level, ZQ_LIB
from autograd import Tensor, sgd_step
import representations_ops_l1 as ops

lv = Level("representations", 1, coverage="strict")
SYM = '.abcdefghijklmnopqrstuvwxyz'
MLP = json.load(open(os.path.join(DATA, 'makemore-mlp.json')))
CL = MLP['C']


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def pcos(a, b):                      # pure-Python cosine
    d = sum(x * y for x, y in zip(a, b))
    return d / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


def pdist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def rank_by(vals, i, largest=True):  # stable order of indices, i left out
    idx = [j for j in range(len(vals)) if j != i]
    return sorted(idx, key=lambda j: (-vals[j] if largest else vals[j], j))


# ------------------------------------------------------------------ shared module and data files
ag = open(os.path.join(DATA, 'autograd.py'), 'rb').read()
lv.claim(hashlib.sha256(ag).hexdigest().startswith('5917d4ec91f7'), 'autograd.py byte-identical to the frozen v1.0 (SHA-256 5917d4ec91f7...)')
R7, sec7 = ops.factor_returns(7)
lv.claim(R7.shape == (500, 30) and list(sec7) == [0] * 10 + [1] * 10 + [2] * 10, 'factor_returns(7): 500 days by 30 stocks, sectors of 10')
Rlt, slt = ops.factor_returns(7, lone=True, twin=True)
lv.claim(np.array_equal(Rlt[:, :30], R7) and np.array_equal(Rlt[:, 30], R7[:, 0]) and slt[-1] == -1, 'lone and twin add stocks without moving the first 30')

# ------------------------------------------------------------------ l1
mk6 = json.load(open(os.path.join(APP, 'content', 'courses', 'makemore', 'l6-letters-as-points.json')))
src_frames = mk6['screens'][1]['canvas']['controls'][0]['frames']
l1 = lv.files['l1-a-table-of-vectors']
my_frames = l1['screens'][0]['canvas']['controls'][0]['frames']
lv.claim(all(src_frames[k]['points'] == my_frames[k]['points'] for k in range(2)), 'l1 hook: the two runs are makemore L2\'s recorded coordinates, unchanged')
run = [{SYM[int(p[1:])]: (v['x'], v['y']) for p, v in src_frames[k]['points'].items()} for k in range(2)]
dae = [pdist(run[k]['a'], run[k]['e']) for k in range(2)]
dat = [pdist(run[k]['a'], run[k]['t']) for k in range(2)]
dab = [pdist(run[k]['a'], run[k]['b']) for k in range(2)]
lv.claim(all(dae[k] < dat[k] and dae[k] < dab[k] for k in range(2)), 'a-e closer than a-t and a-b in both runs')
for v in dae + dat:
    lv.expect('l1', 'screens[0]', round(v, 2), fmt='{:.2f}')
lv.claim(dat[0] > 3 and dat[1] > 3, 't is more than 3 from a in both runs', covers=[3])
lv.expect('l1', 'screens[1].question', 2.66)
lv.expect('l1', 'screens[1].question', -0.19)
lv.claim(round(run[0]['a'][0], 2) == 2.66 and round(run[1]['a'][0], 2) == -0.19, 'a dimension 1: 2.66 and -0.19')
E4 = [[0.2, -1.0, 0.5], [1.5, 0.3, -0.4], [-0.7, 0.8, 2.0], [0.0, 1.1, -0.3]]
h = [0, 0, 1, 0]
prod = [sum(h[r] * E4[r][c] for r in range(4)) for c in range(3)]
lv.claim(prod == [-0.7, 0.8, 2.0], 'one-hot of item 2 times E is row 2', covers=prod)
for c, v in enumerate(prod):
    lv.expect('l1', f'screens[2].widget.rows[{c}][1].answer', v)
lv.claim([E4[r][2] for r in range(4)][0] == 0.5 and E4[1][0] == 1.5, 'slips: column 2 starts 0.5, row 1 starts 1.5', covers=[0.5, 1.5])
lv.expect('l1', 'screens[3].widget.answer', 50000 * 300)
lv.claim(4 * 3 == 12, '4 by 3 table: 12 multiplications', covers=[12])
lv.expect('l1', 'screens[3].feedback.correct', 15000000)
dout = [[0.1, -0.2, 0.3], [0.5, 0.0, -0.1], [-0.4, 0.6, 0.2]]
G = [[0.0] * 3 for _ in range(4)]
for t, i in enumerate([2, 0, 2]):
    for c in range(3):
        G[i][c] += dout[t][c]
lv.claim([round(x, 12) for x in G[2]] == [-0.3, 0.4, 0.5] and G[0] == [0.5, 0.0, -0.1] and G[1] == G[3] == [0, 0, 0], 'gradient rows: 0 and 2 non-zero, row 2 = (-0.3, 0.4, 0.5)', covers=[-0.3, 0.4, 0.5, 0.1, 0.2, 0.6, 0.3])
lv.expect('l1', 'screens[5].widget.answer', 3 * 300)
lv.claim(3 * 300 == 900, '3 million rows of 300: 900 million', covers=[900, 300, 3])
# rotation: the shipped model's dev loss, before and after a seeded rotation
W = open(os.path.join(DATA, 'names.txt')).read().splitlines()
perm = np.random.default_rng(42).permutation(len(W))
dv = [W[i] for i in perm[25626:28829]]
IX = {c: i for i, c in enumerate(SYM)}
X, Y = [], []
for w in dv:
    ctx = [0, 0, 0]
    for chh in w + '.':
        X.append(ctx); Y.append(IX[chh]); ctx = ctx[1:] + [IX[chh]]
X, Y = np.array(X), np.array(Y)
Pm = {k: np.array(v) for k, v in MLP.items() if k != 'about'}


def mlp_loss(C, W1):
    Em = C[X].reshape(len(X), -1); hh = np.tanh(Em @ W1 + Pm['b1']); z = hh @ Pm['W2'] + Pm['b2']
    m = z.max(1, keepdims=True)
    return float((np.log(np.exp(z - m).sum(1)) + m[:, 0] - z[np.arange(len(Y)), Y]).mean())


Q, _ = np.linalg.qr(np.random.default_rng(5).standard_normal((10, 10)))
if np.linalg.det(Q) < 0:                      # a reflection is not a spin: flip one column to make a rotation
    Q[:, 0] = -Q[:, 0]
lv.claim(close(np.linalg.det(Q), 1.0) and np.allclose(Q @ Q.T, np.eye(10)), 'Q is a rotation: orthogonal with determinant 1')
Bd = np.zeros((30, 30))
for k in range(3):
    Bd[10 * k:10 * k + 10, 10 * k:10 * k + 10] = Q.T
l0, lr_ = mlp_loss(Pm['C'], Pm['W1']), mlp_loss(Pm['C'] @ Q, Bd @ Pm['W1'])
lv.claim(round(l0, 4) == 2.1609 and abs(l0 - lr_) < 1e-9, f'dev loss {l0:.6f} before and {lr_:.6f} after a rotation of the table', covers=[2.1609])
lv.expect('l1', 'screens[6].question', 2.1609)
lv.claim(len(X) == 22807, 'dev set of 22,807 rows (makemore L2)')
# the stretch: column 0 of the table times 5, the matching rows of W1 divided by 5 (an invertible map the first layer undoes)
Sx = np.diag([5.0] + [1.0] * 9)
Bs = np.zeros((30, 30))
for k in range(3):
    Bs[10 * k:10 * k + 10, 10 * k:10 * k + 10] = np.linalg.inv(Sx)
Cs = Pm['C'] @ Sx
ls_ = mlp_loss(Cs, Bs @ Pm['W1'])
lv.claim(abs(ls_ - l0) < 1e-9 and round(ls_, 4) == 2.1609, f'dev loss {ls_:.6f} after a stretch of column 0 by 5 undone in W1 (unchanged from {l0:.6f})', covers=[2.1609, 5, 0])
dAs = [pdist(Cs[1], Cs[j]) for j in range(27)]
nbS = [SYM[j] for j in rank_by(dAs, 1, largest=False)[:5]]
nbE0 = [SYM[j] for j in rank_by([pdist(CL[1], CL[j]) for j in range(27)], 1, largest=False)[:5]]
lv.claim(nbE0 == ['e', 'z', 't', 'k', 'o'] and nbS == ['k', 'z', 't', 'o', 'p'], f'stretch moves a\'s five nearest rows by distance from {nbE0} to {nbS}')
lv.stated('l1', 'screens[6].explain', 'to k, z, t, o, p', nbS == ['k', 'z', 't', 'o', 'p'])
lv.stated('l1', 'screens[6].explain', 'from e, z, t, k, o', nbE0 == ['e', 'z', 't', 'k', 'o'])
cosC = [pcos(CL[1], CL[j]) for j in range(27)]
cosS = [pcos(Cs[1], Cs[j]) for j in range(27)]
lv.claim([SYM[j] for j in rank_by(cosC, 1)[:5]] == ['o', 'e', 'u', 't', 'k'] and [SYM[j] for j in rank_by(cosS, 1)[:5]] == ['z', 's', 't', 'k', 'c'], 'the same stretch moves a\'s five nearest rows by cosine from o, e, u, t, k to z, s, t, k, c')
# nearest rows by distance in the letter table
dA = [pdist(CL[1], CL[j]) for j in range(27)]
nbE = [SYM[j] for j in rank_by(dA, 1, largest=False)[:5]]
lv.claim(nbE == ['e', 'z', 't', 'k', 'o'], 'l1 code: five nearest a by distance are e, z, t, k, o')
lv.stated('l1', 'screens[10].feedback.correct', 'e, z, t, k, o', nbE == ['e', 'z', 't', 'k', 'o'])
for v in (800 * 16 + 16 * 64, 800 * 16, 800 * 64, 16 * 64):
    lv.expect('l1', 'screens[11]', v)
lv.claim(800 * 16 + 16 * 64 == 13824, '800 x 16 + 16 x 64 = 13,824', covers=[13824, 12800, 1024, 51200, 800, 64, 16])
lv.expect('l1', 'quiz[1].widget.answer', 2)
lv.claim(len({3, 1}) == 2, 'quiz: items 3 and 1 make 2 rows')

# ------------------------------------------------------------------ l2
u, v_, w_ = (Fr(6, 10), Fr(8, 10)), (Fr(3), Fr(4)), (Fr(8, 10), Fr(-6, 10))
duv2 = sum((a - b) ** 2 for a, b in zip(u, v_)); duw2 = sum((a - b) ** 2 for a, b in zip(u, w_))
lv.claim(duv2 == 16 and duw2 == 2, '|u - v| = 4 and |u - w| = sqrt 2', covers=[4, 1.41, 2.4, 3.2, 0.2, 1.4])
lv.expect('l2', 'screens[0].feedback.correct', 1.41)
lv.claim(close(pcos(u, v_), 1.0) and close(pcos(u, w_), 0.0, 1e-12), 'cos(u, v) = 1, cos(u, w) = 0')
lv.claim(pdist((1.5, 2), (0.6, 0.8)) == 1.5 and pdist((3, 4), (0.6, 0.8)) == 4.0, 'explore: distance 1.5 at (1.5, 2) and 4 at (3, 4)', covers=[1.5, 3.6, 4.8])
c12 = Fr(4, 5)
lv.claim(close(pcos((1, 2), (2, 1)), float(c12)), 'cos((1, 2), (2, 1)) = 4/5 = 0.8 (brief)', covers=[0.8, 4 / math.sqrt(5)])
lv.expect('l2', 'screens[2].widget.answer', 0.8)
E3 = [(1, 2), (2, 1), (-1, 1)]
s12 = pcos(E3[1], E3[2]); s02 = pcos(E3[0], E3[2])
lv.claim(close(s12, -1 / math.sqrt(10)) and close(s02, 1 / math.sqrt(10)), 'entries (1, 2) and (0, 2): -0.3162 and 0.3162', covers=[round(s12, 4), round(s02, 4)])
lv.expect('l2', 'screens[3].widget.answer', round(s12, 4))
NL = [[x / math.sqrt(sum(y * y for y in row)) for x in row] for row in CL]
Sa = [sum(p * q for p, q in zip(NL[1], NL[j])) for j in range(27)]
nbC = rank_by(Sa, 1)[:5]
lv.claim([SYM[j] for j in nbC] == ['o', 'e', 'u', 't', 'k'], 'cosine neighbours of a: o, e, u, t, k')
lens = [math.sqrt(sum(x * x for x in row)) for row in CL]
lv.claim(min(range(27), key=lambda j: lens[j]) == 26, 'z has the shortest row', covers=[round(lens[26], 2)])
for c in 'aeztou':
    lv.expect('l2', 'screens[4].canvas.state.values', round(lens[SYM.index(c)], 2))
A_ = [Fr(x) for x in (1, 3, -1, 2, 0)]; B_ = [Fr(x) for x in (2, 1, 0, 4, 3)]
ma, mb = sum(A_) / 5, sum(B_) / 5
ad = [x - ma for x in A_]; bd = [x - mb for x in B_]
dd = sum(x * y for x, y in zip(ad, bd)); la = sum(x * x for x in ad); lb = sum(x * x for x in bd)
lv.claim(dd == 3 and la == 10 and lb == 10, 'demeaned dot 3, squared lengths 10 and 10: cosine 0.3', covers=[0.3, 3, 10])
lv.claim(close(float(np.corrcoef([1, 3, -1, 2, 0], [2, 1, 0, 4, 3])[0, 1]), 0.3), 'np.corrcoef agrees: 0.3')
craw = pcos([1, 3, -1, 2, 0], [2, 1, 0, 4, 3])
lv.expect('l2', 'screens[5].widget.wrong[0].value', round(craw, 4))
lv.claim(close(craw, 13 / math.sqrt(450)), 'raw cosine 13/sqrt(450)', covers=[round(craw, 4)])
lv.claim([float(x) for x in ad] == [0, 2, -2, 1, -1] and [float(x) for x in bd] == [0, -1, -2, 2, 1], 'demeaned table cells', covers=[0, 2, -2, 1, -1])
cols = [math.sqrt(3 ** 2 + 1 ** 2 + 0), math.sqrt(4 ** 2 + 0 + 2 ** 2)]
t00 = Fr(9, 10) + Fr(16, 20)
lv.claim(t00 == Fr(17, 10) and close((3 / cols[0]) ** 2 + (4 / cols[1]) ** 2, 1.7), 'column-normalised (0, 0) = 9/10 + 16/20 = 1.7', covers=[1.7, 25, 9 / 10, 16 / 20])
lv.expect('l2', 'screens[6].widget.answer', 1.7)
X_, Y_ = (40, 30, 30, 0), (100, 100, 150, 150)
cf = pcos(X_, Y_)
lv.claim(sum(a * b for a, b in zip(X_, Y_)) == 11500 and sum(a * a for a in X_) == 3400 and sum(b * b for b in Y_) == 65000, 'funds: dot 11,500, squared lengths 3,400 and 65,000', covers=[11500, 3400, 65000, 4000, 3000, 4500])
lv.expect('l2', 'screens[11].widget.answer', round(cf, 3))
lv.claim(round(cf, 3) == 0.774, 'funds cosine 0.774', covers=[0.774])
lv.expect('l2', 'quiz[0].widget.answer', float(Fr(24, 25)))
lv.claim(Fr(24, 25) == Fr(96, 100), 'quiz: 24/25 = 0.96', covers=[0.96, 24, 25])
cao = Sa[15]
lv.expect('l2', 'screens[10].feedback.correct', round(cao, 4))

# ------------------------------------------------------------------ l3
def toplist(q, k=5):
    i = SYM.index(q)
    Si = [sum(p * r_ for p, r_ in zip(NL[i], NL[j])) for j in range(27)]
    return [(SYM[j], Si[j]) for j in rank_by(Si, i)[:k]]


for q in 'aeop':
    tl = toplist(q)
    for c, s_ in tl:
        lv.expect('l3', 'screens[1].canvas.controls[0].frames', round(s_, 3))
lv.claim([c for c, _ in toplist('p')] == ['t', 'c', 'g', 'b', 'k'], "p's five nearest are all consonants: t, c, g, b, k")
lv.claim(sum(c in 'aeiou' for c, _ in toplist('a')) == 3, 'three vowels in a\'s top five', covers=[3])
for c, s_ in toplist('a'):
    lv.expect('l3', 'screens[0].canvas.state.values', round(s_, 3))
rk = rank_by(Sa, 1).index(9) + 1
lv.claim(rk == 8, 'i is at rank 8 for a', covers=[8, round(Sa[9], 3), 0.29])
lv.expect('l3', 'screens[0].explain.text', round(Sa[9], 3))
S5 = [[1.0, 0.62, 0.15, 0.80, -0.30]]
lv.claim(rank_by(S5[0], 0)[:2] == [3, 1], 'top 2 of item 0: 3 then 1', covers=[0.8, 0.62, 0.15, 0.3])
S6r = [0.9, 0.5, 1.0, 0.5]
lv.claim(rank_by(S6r, 2)[:2] == [0, 1], 'tie rule: item 2 top 2 = 0 then 1', covers=[0.9, 0.5])
vow = [1, 5, 9, 15, 21]


def topk_i(i, k):
    Si = [sum(p * r_ for p, r_ in zip(NL[i], NL[j])) for j in range(27)]
    return rank_by(Si, i)[:k]


recs = {k: Fr(sum(j in topk_i(i, k) for i in vow for j in vow if j != i), 20) for k in (1, 3, 5)}
lv.claim(recs == {1: Fr(1, 5), 3: Fr(1, 2), 5: Fr(3, 5)}, 'vowel recall at 1, 3, 5: 0.2, 0.5, 0.6', covers=[0.2, 0.5, 0.6, 10, 20])
lv.expect('l3', 'screens[5].widget.answer', 0.5)
pq = [sum(j in topk_i(i, 3) for j in vow if j != i) / 4 for i in vow]
lv.claim(len({len([j for j in vow if j != i]) for i in vow}) == 1 and close(sum(pq) / 5, 0.5), 'vowels: every query has 4 partners, so the mean of per-query recall equals the pooled recall (0.5)', covers=[4, 5])
lv.claim(round(10 / 15, 4) == 0.6667, 'slip: 10 of 15 slots', covers=[0.6667])
names = ["Big Bank", "Small Bank", "Big Tech", "Small Tech", "Big Oil", "Small Oil"]
EA = [[float(x) for x in row] for row in lv.files['l3-nearest-in-the-space']['screens'][4]['canvas']['params']['matrices'][0]['rows']]
qv = [EA[1][c] - EA[0][c] + EA[2][c] for c in range(4)]
cq = [pcos(qv, EA[j]) for j in range(6)]
best = [j for j in sorted(range(6), key=lambda j: (-cq[j], j)) if j not in (0, 1, 2)][0]
lv.claim(names[best] == 'Small Tech', 'analogy: Small Tech is nearest to Small Bank - Big Bank + Big Tech')
lv.expect('l3', 'screens[4].feedback.correct', round(cq[3], 3))
for c in range(4):
    lv.expect('l3', 'screens[4].hints[1].text', round(qv[c], 2))
lv.claim(all(abs(EA[j][c]) <= 1.1 for j in range(6) for c in range(4)), 'analogy table entries', covers=[x for row in EA for x in row])
g5 = np.random.default_rng(5)
sds = {}
for d in (2, 10, 300):
    Xr = g5.standard_normal((40, d)).tolist()
    Xr = [[x / math.sqrt(sum(y * y for y in row)) for x in row] for row in Xr]
    vals = [sum(p * q for p, q in zip(Xr[i], Xr[j])) for i in range(40) for j in range(i + 1, 40)]
    m = sum(vals) / len(vals)
    sds[d] = math.sqrt(sum((x - m) ** 2 for x in vals) / len(vals))
lv.claim(len(vals) == 780, '40 directions give 780 pairs', covers=[780])
lv.expect('l3', 'screens[7].feedback.correct', round(sds[300], 3))
lv.expect('l3', 'screens[7].explain.text', round(sds[2], 2))
lv.expect('l3', 'screens[7].explain.text', round(sds[10], 2))
lv.claim(close(round(1 / math.sqrt(300), 4), 0.0577) and abs(sds[300] - 1 / math.sqrt(300)) < 0.005, 'spread in 300 dimensions near 1/sqrt(300) = 0.058', covers=[0.058, 0.0577, 0.7071, 0.0033, 0.15])
lv.expect('l3', 'screens[7].widget.answer', round(1 / math.sqrt(300), 4))
lv.claim(round(0.12 / (1 / math.sqrt(300)), 1) == 2.1, 'quiz: 0.12 is about two spreads', covers=[0.12])
lv.expect('l3', 'quiz[1].widget.answer', 0.75)
lv.claim(Fr(6, 8) == Fr(3, 4) and 6 / 5 == 1.2, 'quiz: recall 6/8 = 0.75; slip 6/5 = 1.2', covers=[1.2, 0.75])
lv.literal('0.10, 0.75, 0.20, 1.00, 0.55', why='the quiz gives one row of a cosine matrix as its data; the answer is a sort of it, checked above by rank_by')


# ------------------------------------------------------------------ l4: fits by a hand gradient (route B) against the autograd (route A, generator)
def corr_b(R):
    return np.corrcoef(np.asarray(R).T)


def fit_b(C, dim=3, steps=300, lr=10.0, seed=0, trace=False):
    n = len(C); E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim)); M = 1 - np.eye(n); out = []
    for _ in range(steps):
        D = (E @ E.T - C) * M; out.append(float((D ** 2).sum() / (n * (n - 1))))
        E = E - lr * 4 * D @ E / (n * (n - 1))
    D = (E @ E.T - C) * M; out.append(float((D ** 2).sum() / (n * (n - 1))))
    return (E, out) if trace else E


def fit_ag(C, dim=3, steps=300, lr=10.0, seed=0):
    n = len(C); T = Tensor(0.1 * np.random.default_rng(seed).standard_normal((n, dim))); M = 1.0 - np.eye(n)
    for _ in range(steps):
        T.zero_grad(); D = (T @ T.T - C) * M; L = (D ** 2).sum() / (n * (n - 1)); L.backward(); sgd_step([T], lr)
    return T.data


def nn_loop(E):
    E = np.asarray(E); out = []
    for i in range(len(E)):
        s = [pcos(E[i], E[j]) if j != i else -2 for j in range(len(E))]
        out.append(max(range(len(E)), key=lambda j: (s[j], -j)))
    return out


C7 = corr_b(R7)
E7, L7 = fit_b(C7, trace=True)
lv.claim(np.allclose(E7, fit_ag(C7), atol=1e-9), 'hand gradient and autograd give the same table (300 steps)')
lv.expect('l4', 'screens[3].canvas.state.caption', round(L7[0], 4))
lv.expect('l4', 'screens[3].question', round(L7[-1], 5))
rms7 = math.sqrt(round(L7[-1], 5))
lv.expect('l4', 'screens[3].widget.answer', round(rms7, 4))
lv.claim(round(math.sqrt(L7[-1]), 3) == round(rms7, 3) == 0.019, 'typical error 0.019', covers=[0.019, 0.02, 0.2, 0.6])
step_vals = [round(L7[s], 5) for s in range(0, 301, 10)]
lv.claim(lv.files['l4-embedding-stocks']['screens'][3]['canvas']['params']['series'][0]['values'] == step_vals, 'l4 loss curve matches the hand-gradient run every 10 steps')
nn7 = nn_loop(E7)
rec7 = sum(sec7[nn7[i]] == sec7[i] for i in range(30)) / 30
lv.claim([i for i in range(30) if sec7[nn7[i]] != sec7[i]] == [9], 'only stock 9 misses its sector', covers=[round(rec7, 3)])
lv.expect('l4', 'screens[4].explain.text', round(rec7, 3))
lv.claim(sum(sec7[nn7[i]] == 0 for i in range(10)) == 9, '9 of the 10 sector-0 stocks have a sector-0 neighbour', covers=[9])
tab = lv.files['l4-embedding-stocks']['screens'][4]['canvas']['params']['rows']
lv.claim([int(r_[1][1:]) for r_ in tab] == nn7[:10], 'neighbour table matches')
rec_seeds, rms_seeds = [], []
for s in range(7, 17):
    Rs, ss = ops.factor_returns(s)
    Es, Ls = fit_b(corr_b(Rs), trace=True)
    nns = nn_loop(Es)
    rec_seeds.append(sum(ss[nns[i]] == ss[i] for i in range(30)) / 30); rms_seeds.append(math.sqrt(Ls[-1]))
lv.claim(abs(min(rec_seeds) - 29 / 30) < 1e-12 and max(rms_seeds) < 0.02, f'seeds 7 to 16: recovery from {min(rec_seeds):.3f}, typical error at most {max(rms_seeds):.4f}', covers=[round(min(rec_seeds), 3)])
lv.claim(max(rms_seeds) < 0.03 / 1.5, 'threshold 0.03 on the fit error holds with margin on 10 seeds', covers=[0.03])
lv.claim(min(rec_seeds) >= 0.9 + 0.05, 'threshold 0.9 on recovery holds with margin on 10 seeds', covers=[0.9])
from sklearn.cluster import KMeans
Un = E7 / np.linalg.norm(E7, axis=1, keepdims=True)
lab = KMeans(3, n_init=10, random_state=0).fit_predict(Un)
pur = sum(np.bincount(sec7[lab == g]).max() for g in range(3))
lv.claim(pur == 29, 'scikit-learn KMeans on the unit rows: 29 of 30 in a group whose majority shares their sector', covers=[29])
ktab = lv.files['l4-embedding-stocks']['screens'][5]['canvas']['params']['rows']
lv.claim(sorted(int(x) for r_ in ktab for x in r_[1:]) == sorted([0] * 5 + [1] + [9] + [10] * 2), 'k-means table: 10, 10, 9 and one stray', covers=[10])
C1, C2 = corr_b(R7[:250]), corr_b(R7[250:])
E1, E2 = fit_b(C1), fit_b(C2)
n1, n2 = nn_loop(E1), nn_loop(E2)
lv.claim(n1[9] == 1 and sec7[n2[9]] == 2 and n2[9] == 20, 'stock 9: neighbour 1 (sector 0) on the first half, 20 (sector 2) on the last')
lv.expect('l4', 'screens[6].prose', round(pcos(E1[9], E1[1]), 2))
m9 = {h_: [float(np.mean([CC[9, j] for j in range(30) if sec7[j] == s and j != 9])) for s in range(3)] for h_, CC in (('h1', C1), ('h2', C2))}
for h_ in m9:
    for s in range(3):
        lv.expect('l4', 'screens[6].canvas.state.values', round(m9[h_][s], 2))
lv.claim(m9['h2'][2] > m9['h2'][0] and m9['h1'][0] > m9['h1'][2], 'stock 9 moves from sector 0 to sector 2')
same_nn = sum(n1[i] == n2[i] for i in range(30)); same_sec = sum(sec7[n1[i]] == sec7[n2[i]] for i in range(30))
lv.claim(same_nn == 6 and same_sec == 28, 'l3 transfer: 6 exact partners and 28 sectors hold', covers=[6, 28, round(6 / 30, 4), round(28 / 30, 4), 0.2, 0.93])
lv.expect('l3', 'screens[11].widget.answer', round(6 / 30, 4))
RL, sL = ops.factor_returns(7, lone=True)
CLn = corr_b(RL)
EL = fit_b(CLn)
lensL = np.linalg.norm(EL, axis=1)
sLc = [pcos(EL[30], EL[j]) for j in range(30)]
top = max(range(30), key=lambda j: (sLc[j], -j))
lv.claim(top == 27, 'lone stock: top cosine with stock 27')
for vv, dp in ((lensL[30], 2), (lensL[:30].min(), 2), (lensL[:30].max(), 2), (sLc[top], 2), (CLn[30, 27], 2)):
    lv.expect('l4', 'screens[7]', round(float(vv), dp))
lv.claim(lensL[30] < 0.1 < 0.25 < lensL[:30].min(), 'lone row below the 0.25 guard; every other row above it', covers=[0.25])


def fit_diag(C, dim=3, steps=300, lr=10.0, seed=0):         # the same fit with the diagonal kept (mask of ones)
    n = len(C); E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    for _ in range(steps):
        E = E - lr * 4 * (E @ E.T - C) @ E / (n * (n - 1))
    return E


ELd = fit_diag(CLn)
lensLd = np.linalg.norm(ELd, axis=1)
wL, VL = np.linalg.eigh(CLn)
eigL = np.linalg.norm(VL[:, -3:] * np.sqrt(wL[-3:]), axis=1)
lv.claim(abs(lensL[30] - 0.0736) < 5e-5 and abs(lensLd[30] - 0.0875) < 5e-5 and abs(eigL[30] - lensLd[30]) < 5e-4, f'diagonal kept: noise-only row {lensLd[30]:.4f} long against {lensL[30]:.4f} without it; the eigenvector closed form gives {eigL[30]:.4f}')
lv.expect('l4', 'screens[8]', round(float(lensL[30]), 3), fmt='{:.3f}')
lv.expect('l4', 'screens[8]', round(float(lensLd[30]), 3), fmt='{:.3f}')
lv.claim(lensLd[:30].min() > 0.25 and lensLd[:30].max() < 1, 'with the diagonal kept the other rows stay between 0.67 and 0.85, nowhere near forced to 1')
blk = lv.files['l4-embedding-stocks']['screens'][0]['canvas']['params']['matrices'][0]
order = [int(x[1:]) for x in blk['rowLabels']]
lv.claim(blk['rows'] == [[round(float(C7[a, b]), 1) for b in order] for a in order], '12 by 12 block equals np.corrcoef rounded to 1 place', covers=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1])
lv.claim(len(order) == 12 == 3 * 4 and len({sec7[a] for a in order}) == 3, '3 blocks of 4 stocks', covers=[3, 4, 12])
e3 = [Fr(8, 10), Fr(7, 10), Fr(3, 10)]; C3 = [[1, Fr(6, 10), Fr(2, 10)], [Fr(6, 10), 1, Fr(3, 10)], [Fr(2, 10), Fr(3, 10), 1]]
errs = [e3[i] * e3[j] - C3[i][j] for i, j in ((0, 1), (0, 2), (1, 2))]
sq = sum(e * e for e in errs)
lv.claim(sq == Fr(113, 10000), '3 by 3: squares add to 0.0113', covers=[0.0113, 0.56, 0.24, 0.21, 0.04, 0.09, 0.0016, 0.0081, 0.6, 0.2, 0.3, 0.8, 0.7])
lv.expect('l4', 'screens[2].widget.answer', round(float(sq / 3), 4))
diag = sum((e3[i] * e3[j] - C3[i][j]) ** 2 for i in range(3) for j in range(3)) / 9
lv.expect('l4', 'screens[2].widget.wrong[1].value', round(float(diag), 4))
lv.claim(all(close(float(e * e), v) for e, v in zip(e3, (0.64, 0.49, 0.09))), 'diagonal of E E^T: 0.8^2, 0.7^2, 0.3^2 = 0.64, 0.49, 0.09', covers=[0.64, 0.49, 0.09])
lv.claim(30 * 3 == 90 and 30 * 29 // 2 == 435, '90 numbers fit 435 pairs', covers=[90, 435])
lv.claim(close(0.6 * 0.5 + 0.2 * 0.5, 0.4) and close((0.4 - 0.5) ** 2, 0.01), 'l4 quiz: 0.4 fitted, error 0.1, squared 0.01', covers=[0.4, 0.1, 0.01])
lv.literal('0.05, 0.8', why='the quiz gives two row lengths as its scenario; the cosine question built on them does not depend on a computed value')

# ------------------------------------------------------------------ review
lv.claim(close(pcos((2, 0, 1), (1, 2, 2)), 4 / (3 * math.sqrt(5))), 'review cosine 4/(3 sqrt 5)', covers=[round(4 / (3 * math.sqrt(5)), 4), round(4 / 9, 4)])
lv.expect('review', 'items[2].widget.answer', round(4 / (3 * math.sqrt(5)), 4))
ra = [Fr(x) for x in (2, 0, 1, -1, 3)]; rb = [Fr(x) for x in (1, 1, 0, 2, 1)]
rad = [x - sum(ra) / 5 for x in ra]; rbd = [x - sum(rb) / 5 for x in rb]
rdot = sum(x * y for x, y in zip(rad, rbd))
lv.claim(rdot == -2 and sum(x * x for x in rad) == 10 and sum(x * x for x in rbd) == 2, 'review: demeaned dot -2, lengths sqrt 10 and sqrt 2')
lv.expect('review', 'items[3].widget.answer', round(-2 / math.sqrt(20), 4))
lv.expect('review', 'items[3].widget.wrong[0].value', round(pcos((2, 0, 1, -1, 3), (1, 1, 0, 2, 1)), 4))
lv.claim(rank_by([1, 0.3, 0.7, 0.7, -0.2], 0)[0] == 2, 'review: tie at 0.7 goes to item 2', covers=[0.7])
lists = {0: (3, 1), 1: (0, 2), 2: (4, 0), 3: (1, 4)}
kp = [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4)]
lv.claim(Fr(sum(j in lists[i] for i, j in kp), 5) == Fr(3, 5), 'review recall at 2 = 3/5', covers=[0.6, 0.375])
rq = {}
for i, j in kp:
    rq.setdefault(i, []).append(j in lists[i])
lv.claim(sum(Fr(sum(v), len(v)) for v in rq.values()) / len(rq) == Fr(5, 8), 'llm-apps alignment: the per-query mean of review recall at 2 is 5/8 = 0.625, not the pooled 3/5, so the pooled definition stays here', covers=[0.625])
lv.claim(close(0.6 * 0.5 + 0.3 * -0.2, 0.24) and close((0.24 - 0.35) ** 2, 0.0121), 'review pair: 0.24 fitted, squared error 0.0121', covers=[0.24, 0.0121, 0.11, 0.35, 0.30, 0.06])
lv.expect('review', 'items[6].widget.answer', 0.0121)
lv.claim(Fr(9, 10) == Fr(9, 10) and close((3 / math.sqrt(10)) ** 2, 0.9), 'review column scaling: row 1 entry 9/10', covers=[0.9])
lv.expect('review', 'items[9].widget.answer', 0.9)
lv.literal('0.06, 0.91, 0.6', why='given figures in the review item setup; the answer built from them is checked in the claim above')

# ------------------------------------------------------------------ homework
lv.expect('homework', 'items[4].widget.answer', 5000 * 32 + 32 * 128)
lv.claim(5000 * 32 == 160000 and 32 * 128 == 4096 and 5000 * 128 == 640000, 'weights: 160,000 + 4,096 = 164,096; one-hot 640,000', covers=[160000, 4096, 164096, 640000])
Hz = [(3, 4), (0, 0), (4, 3), (-4, -3)]
tot = 0
for a in Hz:
    for b in Hz:
        na = math.hypot(*a); nb = math.hypot(*b)
        tot += 0 if na == 0 or nb == 0 else (a[0] * b[0] + a[1] * b[1]) / (na * nb)
lv.claim(close(tot, 1.0), 'guarded matrix sums to 1', covers=[1, 0.96, 3, 2])
lv.expect('homework', 'items[5].widget.answer', 1.0)
qa_ = [1 - 1 + 0, 0 - 1 + 2, 2 - 0 + 1]
lv.claim(qa_ == [0, 1, 3] and close(pcos(qa_, (0, 1, 3)), 1.0), 'homework analogy: q = (0, 1, 3), cosine 1')
lv.expect('homework', 'items[6].widget.answer', 1.0)
sw = [1 - 1 + 0, 1 - 0 + 2, 0 - 2 + 1]
lv.expect('homework', 'items[6].widget.wrong[1].value', round(pcos(sw, (0, 1, 3)), 4))
lv.claim(close(0.35 / 0.1, 3.5), 'background: 0.35 / 0.1 = 3.5', covers=[3.5, 0.35, 0.1, 0.01, 35])
vendor = lv.text('homework', 'items[3].model')
lv.claim('top-5' in vendor and 'top 20' in vendor, 'vendor model answer names its own suggested score', covers=[5, 20])
lv.literal("3,000", why="the vendor's universe size in the long-form prompt is a scenario, not a computed figure")
lv.literal("64", why="the vendor's row width in the long-form prompt is a scenario, not a computed figure")

# ------------------------------------------------------------------ problems
A1 = [Fr(x) for x in ('0.5', '1.5', '-0.5', '1', '2.5')]; B1 = [Fr(x) for x in ('1', '0', '0.5', '2', '1.5')]
a1 = [x - sum(A1) / 5 for x in A1]; b1 = [x - sum(B1) / 5 for x in B1]
d1 = sum(x * y for x, y in zip(a1, b1))
lv.claim(sum(A1) / 5 == 1 and d1 == 1 and sum(x * x for x in a1) == 5 and sum(x * x for x in b1) == Fr(5, 2), 'problem 1: mean 1, dot 1, squared lengths 5 and 2.5', covers=[1, 5, 2.5, 12.5, -0.5, 0.5, -1.5, 1.5])
cab = float(d1) / math.sqrt(12.5)
lv.expect('problems', 'items[0].parts[1].widget.answer', round(cab, 4))
lv.expect('problems', 'items[0].parts[2].widget.answer', round(cab, 4))
lv.expect('problems', 'items[0].parts[1].widget.wrong[0].value', round(pcos([float(x) for x in A1], [float(x) for x in B1]), 4))
lv.expect('problems', 'items[0].parts[2].widget.wrong[0].value', round(pcos([float(x) for x in A1], [float(x) + 0.5 for x in B1]), 4))
Cc = [0.8, 1.2, 0.2, 0.7, 2.1]; Dd = [2.0, -1.0, 1.5, 0.5, -0.5]
cdm = lambda z: [x - sum(z) / 5 for x in z]
cac, cad = pcos([float(x) for x in a1], cdm(Cc)), pcos([float(x) for x in a1], cdm(Dd))
lv.expect('problems', 'items[0].parts[3].question', round(cac, 4))
lv.expect('problems', 'items[0].parts[3].question', round(cad, 4))
lv.claim(cac > cab > cad, 'C is A\'s nearest of B, C and D')
E4p = [(0.7, 0.3), (0.6, 0.4), (0.1, 0.8), (0.2, -0.1)]
lv.claim(close(E4p[0][0] * E4p[1][0] + E4p[0][1] * E4p[1][1], 0.54) and close((0.54 - 0.55) ** 2, 0.0001), 'problem 2: 0.54 and squared error 0.0001', covers=[0.54, 0.0001, 0.01, 0.55, 0.42, 0.12, 0.8, 0.3, 0.1])
lv.expect('problems', 'items[1].parts[3].question', round(math.hypot(*E4p[3]), 2))
lv.claim(min(math.hypot(*e) for e in E4p[:3]) > 0.7, 'other rows above 0.7', covers=[0.7, 0.75])
E5 = [(1.0, 0.2, 0.0), (0.9, 0.3, 0.1), (0.1, 1.0, 0.2), (0.0, 0.9, 0.4), (0.05, 0.0, -0.01)]
lv.expect('problems', 'items[2].parts[0].widget.answer', round(pcos(E5[0], E5[1]), 3))
lv.claim(close(sum(a * b for a, b in zip(E5[0], E5[1])), 0.96), 'problem 3: dot 0.96, squared lengths 1.04 and 0.91', covers=[0.96, 1.04, 0.91, 0.9, 0.06])
l4n = math.sqrt(sum(x * x for x in E5[4]))
lv.expect('problems', 'items[2].parts[1].widget.answer', round(l4n, 3))
lv.claim(close(sum(x * x for x in E5[4]), 0.0026), 'stock 4 squared length 0.0025 + 0 + 0.0001 = 0.0026', covers=[0.0026, 0.0025, 0.0001])
nnp = []
for i in range(5):
    s = [pcos(E5[i], E5[j]) if j != i else -2 for j in range(5)]
    nnp.append(max(range(5), key=lambda j: (s[j], -j)))
found = sum(nnp[i] == j for i, j in [(0, 1), (1, 0), (2, 3), (3, 2)])
lv.claim(found == 4 and nnp[:4] == [1, 0, 3, 2], 'problem 3: stocks 0, 1 and 2, 3 are mutual nearest; recall at 1 is 4/5', covers=[0.8, 4])
lv.claim(nnp == [1, 0, 3, 2, 0] and sum(nnp[i] == j for i, j in [(0, 1), (1, 0), (2, 3), (3, 2), (4, 0)]) == 5, 'problem 3: without the guard stock 4\'s nearest is stock 0 and recall at 1 is 5/5 = 1, so the guard is what loses the pair (4, 0)', covers=[1, 5])
lv.claim(min(math.sqrt(sum(x * x for x in E5[i])) for i in range(4)) > 0.25 > math.sqrt(sum(x * x for x in E5[4])), 'problem 3 guard: only stock 4 is shorter than 0.25', covers=[0.25])

# ------------------------------------------------------------------ code widgets: rerun every hidden test with the solution and with a loop-based twin
TWINS = {
 'one_hot': '''
def one_hot(idx, n):
    return np.array([[1.0 if c == i else 0.0 for c in range(n)] for i in idx])
def one_hot_lookup(E, idx):
    E = np.asarray(E, dtype=float)
    return np.array([[sum(one_hot(idx, len(E))[r][k] * E[k][c] for k in range(len(E))) for c in range(E.shape[1])] for r in range(len(idx))])
def embedding_grad(E, idx, dout):
    E = np.asarray(E, dtype=float); g = np.zeros(E.shape); dout = np.asarray(dout, dtype=float)
    for t, i in enumerate(idx):
        for c in range(E.shape[1]):
            g[i][c] += dout[t][c]
    return g
''',
 'nearest_rows': '''
import math
def nearest_rows(E, i, k):
    E = [list(map(float, r)) for r in np.asarray(E, dtype=float)]
    d = [math.sqrt(sum((a - b) ** 2 for a, b in zip(E[j], E[i]))) for j in range(len(E))]
    return sorted([j for j in range(len(E)) if j != i], key=lambda j: (d[j], j))[:k]
''',
 'cosine': '''
import math
def cosine(u, v):
    u = [float(x) for x in u]; v = [float(x) for x in v]
    nu = math.sqrt(sum(x * x for x in u)); nv = math.sqrt(sum(x * x for x in v))
    if nu == 0 or nv == 0:
        return 0.0
    return sum(a * b for a, b in zip(u, v)) / (nu * nv)
''',
 'safe_normalise': '''
import math
def safe_normalise(E, eps=1e-12):
    out = []
    for r in np.asarray(E, dtype=float):
        n = math.sqrt(sum(x * x for x in r))
        out.append([x / n for x in r] if n > eps else list(r))
    return np.array(out)
def cosine_matrix(E):
    N = safe_normalise(E)
    return np.array([[sum(a * b for a, b in zip(N[i], N[j])) for j in range(len(N))] for i in range(len(N))])
''',
 'top_k': '''
import math
def _c(a, b):
    na = math.sqrt(sum(x * x for x in a)); nb = math.sqrt(sum(x * x for x in b))
    return 0.0 if na == 0 or nb == 0 else sum(x * y for x, y in zip(a, b)) / (na * nb)
def top_k(E, i, k):
    E = [list(map(float, r)) for r in np.asarray(E, dtype=float)]
    return sorted([j for j in range(len(E)) if j != i], key=lambda j: (-_c(E[i], E[j]), j))[:k]
def recall_at_k(E, pairs, k):
    return sum(j in top_k(E, i, k) for i, j in pairs) / len(pairs)
''',
 'analogy': '''
import math
def _c(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))
def analogy(E, a, b, c, k):
    E = [list(map(float, r)) for r in np.asarray(E, dtype=float)]
    q = [E[b][t] - E[a][t] + E[c][t] for t in range(len(E[0]))]
    return sorted([j for j in range(len(E)) if j not in (a, b, c)], key=lambda j: (-_c(q, E[j]), j))[:k]
''',
 'corr_from_returns': '''
def corr_from_returns(R):
    return np.corrcoef(np.asarray(R, dtype=float).T)
def sector_recovery(E, sectors):
    import math
    E = [list(map(float, r)) for r in np.asarray(E, dtype=float)]
    def c(a, b):
        return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))
    hits = 0
    for i in range(len(E)):
        j = max((j for j in range(len(E)) if j != i), key=lambda j: (c(E[i], E[j]), -j))
        hits += sectors[j] == sectors[i]
    return hits / len(E)
''',
 'fit_embeddings': '''
def fit_embeddings(C, dim, steps, lr, seed):
    C = np.asarray(C, dtype=float); n = len(C)
    E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim)); M = 1 - np.eye(n)
    for _ in range(steps):
        D = (E @ E.T - C) * M
        E = E - lr * 4 * D @ E / (n * (n - 1))
    return E
''',
 'similar_stocks': '''
def similar_stocks(R, k, dim, seed):
    C = np.corrcoef(np.asarray(R, dtype=float).T)
    w, V = np.linalg.eigh(C)
    E = V[:, -dim:] * np.sqrt(np.maximum(w[-dim:], 0))
    L = np.sqrt((E ** 2).sum(axis=1)); ok = L >= 0.25; n = len(C); out = []
    for i in range(n):
        if not ok[i]:
            out.append([]); continue
        s = [(-(E[i] @ E[j]) / (L[i] * L[j]), j) for j in range(n) if j != i and ok[j]]
        out.append([j for _, j in sorted(s)[:k]])
    return out
''',
 'nearest_for_queries': '''
import math
def nearest_for_queries(E, Q, k):
    E = [list(map(float, r)) for r in np.asarray(E, dtype=float)]
    out = []
    for q in np.asarray(Q, dtype=float):
        nq = math.sqrt(sum(x * x for x in q))
        if nq == 0:
            out.append([]); continue
        def c(r):
            nr = math.sqrt(sum(x * x for x in r))
            return 0.0 if nr == 0 else sum(a * b for a, b in zip(q, r)) / (nq * nr)
        out.append(sorted(range(len(E)), key=lambda j: (-c(E[j]), j))[:k])
    return out
''',
}


def norm(v):
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    return [norm(x) for x in v] if isinstance(v, list) else v


def same(a, b, cmp, tol):
    a, b = norm(a), norm(b)
    if isinstance(a, list) or isinstance(b, list):
        return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(same(x, y, cmp, tol) for x, y in zip(a, b))
    if cmp == 'isclose' and isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        rel = (tol or {}).get('rel', 1e-9 if not tol else 0) or 0; ab = (tol or {}).get('abs', 1e-12 if not tol else 0) or 0
        return math.isclose(a, b, rel_tol=rel, abs_tol=ab)
    return a == b


def run_widget(w, src, label, twin_ok=None):
    cwd = os.getcwd(); os.chdir(DATA)
    try:
        ns = {'__name__': '__zq__', '__learner_source__': src}; exec(ZQ_LIB, ns); exec('import numpy as np\n', ns); exec(src, ns)
        ok_all = True
        for k, t in enumerate(w['tests']):
            if '__learner_source__' in t['call'] or ('twin' in label and 'zq_' in t['call']):
                continue  # a source check judges the learner's code, not a twin's results
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            want = eval(t['expect'])
            ok = same(got, want, t.get('compare', 'equal'), t.get('tol'))
            if twin_ok is not None and k + 1 in twin_ok:
                continue
            ok_all &= ok
            if not ok:
                print('   mismatch', label, 'test', k + 1, str(got)[:80], 'vs', t['expect'][:80])
        return ok_all
    finally:
        os.chdir(cwd)


def widgets(doc):
    for key in ('screens', 'items'):
        for i, s in enumerate(doc.get(key, [])):
            w = s.get('widget')
            if isinstance(w, dict) and w.get('kind') == 'code':
                yield f'{key}[{i}]', w


n_code = 0
for fid, doc in lv.files.items():
    for path, w in widgets(doc):
        n_code += 1
        lv.claim(run_widget(w, w['solution'], f'{fid} {path}'), f'{fid} {path}: the model solution passes every hidden test in CPython')
        name = next(k for k in TWINS if f'def {k}(' in w['solution'])
        # the twin of fit_embeddings repeats the run by hand; the threshold tests of similar_stocks use eigenvectors instead of the fit
        lv.claim(run_widget(w, TWINS[name], f'{fid} {path} twin'), f'{fid} {path}: an independent loop-based twin gives the same results')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{fid} {path}: at least two mutants')
lv.claim(n_code == 10, 'ten code widgets in the level')
# exact short runs: the 5-step and 3-step fits (l4) by hand gradient, compared with the stored expect
fw = lv.files['l4-embedding-stocks']['screens'][10]['widget']
C4m = [[1, 0.6, 0.2, 0.1], [0.6, 1, 0.3, 0.2], [0.2, 0.3, 1, 0.5], [0.1, 0.2, 0.5, 1]]
e5 = np.round(fit_b(np.array(C4m), 2, 5, 1.0, 0), 6).tolist()
lv.claim(e5 == eval(fw['tests'][0]['expect']), 'exact short run: 5 steps of size 1 of the 4-stock fit match to 6 places by hand gradient')
# timing note values in the how lines and thresholds
lv.literal('6, 15, 4, 0.85, 1e-12, 0.0577', why='test counts, table sizes and tolerances named in how lines are settings of the hidden tests, which this script runs')
# sizes of the data sets, checked against the data itself
lv.claim(len(CL) == 27, "makemore's table has 27 rows", covers=[27])
lv.claim(R7.shape[1] == 30 and R7.shape[0] == 500 and R7[:250].shape[0] == 250, '30 stocks, 500 days, halves of 250', covers=[30, 500, 250])
lv.claim(abs(math.cos(math.pi) + 1) < 1e-12, 'cosine -1 is an angle of 180 degrees', covers=[180])
lv.claim('standard_normal((40, 6))' in lv.files['l1-a-table-of-vectors']['screens'][10]['widget']['tests'][4]['setup'], 'l1 code: seeded table of 40 rows', covers=[40])
lv.claim(10 ** 2 == 100 and close(pcos([10 * x for x in CL[1]], CL[15]), pcos(CL[1], CL[15])), 'a row 10 times as long has a squared length 100 times as large (a distractor), and the same cosines', covers=[100, 10])
lv.literal("150", why="fund Y's holdings in the transfer prompt are given amounts; the cosine built from them is checked")
lv.literal("200", why="the trap's universe size is a scenario figure, not a computed result")
lv.literal("5,000", why="the homework universe size is given; the weight count built from it is checked")
lv.claim(5000 * 32 + 32 * 128 == 164096, 'homework sizes 5,000, 32, 128', covers=[5000, 32, 128])
# performance task threshold: same-sector share of neighbours on ten seeds, model solution and eigenvector twin
hwp = lv.files['homework-1']['items'][0]['widget']
nsA, nsB = {}, {}
exec('import numpy as np\n' + hwp['solution'], nsA)
exec('import numpy as np\n' + TWINS['similar_stocks'], nsB)
shares = []
for s in range(7, 17):
    Rs, ss = ops.factor_returns(s)
    for nsX in (nsA, nsB):
        out = nsX['similar_stocks'](Rs, 3, 3, 0)
        hits = [ss[j] == ss[i] for i, row in enumerate(out) for j in row]
        shares.append(sum(hits) / len(hits))
lv.claim(min(shares) >= 0.85 + 0.1, f'similar_stocks: same-sector share from {min(shares):.3f} on seeds 7 to 16 by both routes, above the 0.85 threshold with margin', covers=[0.85])
lv.check_wrongs()
lv.report()
