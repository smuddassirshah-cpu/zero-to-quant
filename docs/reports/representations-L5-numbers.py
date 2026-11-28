"""representations level 5 (Graph networks): every stated number recomputed by a second route.

Route A is the generator (NumPy, the autograd, nt_ops_l1.adam_step, representations_ops_l5). Route B here is independent:
Fractions and loops over neighbours for every small matrix and averaging step, a hand-written forward and backward pass
with a hand-written Adam for every trained network (any depth, so the linear k-step model and the 16-layer stack too),
power iteration instead of eigh for the top eigenvector, and an independent twin for every code widget, rerun against
its hidden tests in CPython beside the model solution. Trained figures are compared to the stated rounding, and every
graded threshold is checked with a margin across several seeds. Run through
`node tools/run-number-scripts.mjs --only representations-L5` (one BLAS thread); strict coverage.
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
from autograd import Tensor, grad_check
import representations_ops_l5 as ops

lv = Level("representations", 5, coverage="strict")
F = lv.files


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(b))


def sha(name):
    return hashlib.sha256(open(os.path.join(DATA, name), 'rb').read()).hexdigest()


lv.claim(sha('autograd.py').startswith('5917d4ec91f7') and sha('nt_ops_l1.py').startswith('9c1391a33624') and sha('representations_ops_l1.py').startswith('097ac4d78867'),
         'autograd.py v1.0, nt_ops_l1.py and representations_ops_l1.py byte-identical to the frozen copies')


# ------------------------------------------------------------------ route B building blocks
def adj_b(n, edges):
    A = [[0] * n for _ in range(n)]
    for i, j in edges:
        A[i][j] = A[j][i] = 1
    return A


def hat_b(A):
    """Normalised adjacency entry by entry from the degrees with loops."""
    n = len(A)
    d = [sum(A[i]) + 1 for i in range(n)]
    return [[((A[i][j] if i != j else 1) / math.sqrt(d[i] * d[j])) for j in range(n)] for i in range(n)]


def step_fr(A, x, loops=False):
    """One averaging step with exact Fractions: mean over neighbours (and self with loops)."""
    n = len(A)
    out = []
    for i in range(n):
        nb = [j for j in range(n) if A[i][j]] + ([i] if loops else [])
        out.append(sum(Fr(x[j]) for j in nb) / len(nb))
    return out


def top_vec_b(M, iters=5000):
    """Top eigenvector by power iteration on M + I (shifts the spectrum to [0, 2])."""
    M = np.asarray(M, float)
    v = np.ones(len(M)) + 0.01 * np.arange(len(M))
    for _ in range(iters):
        v = M @ v + v
        v /= np.linalg.norm(v)
    return v


def pp_b(n, p_in, p_out, seed):
    """Planted partition by a double loop over the same table."""
    U = np.random.default_rng(seed).random((n, n))
    A = np.zeros((n, n))
    y = [0 if i < n // 2 else 1 for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if U[i, j] < (p_in if y[i] == y[j] else p_out):
                A[i, j] = A[j, i] = 1.0
    return A, np.array(y)


def feat_b(y, shift, seed):
    X = np.random.default_rng(seed).standard_normal((len(y), 2))
    return X + np.c_[shift * (2 * np.asarray(y) - 1.0), np.zeros(len(y))]


def train_b(Ah, X, y, tr, layers=2, hidden=16, steps=200, lr=0.05, seed=0, K=None):
    """Hand forward and backward pass of an L-layer graph network, hand Adam; returns (weights, losses)."""
    Ah = np.asarray(Ah, float); X = np.asarray(X, float); y = np.asarray(y); tr = np.asarray(tr)
    K = int(y.max()) + 1 if K is None else K
    sizes = [X.shape[1]] + [hidden] * (layers - 1) + [K]
    g = np.random.default_rng(seed)
    W = [g.standard_normal((a, b)) / math.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]; v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        Hs, Zs, Ms = [X], [], []
        for k, w in enumerate(W):
            M = Ah @ Hs[-1]
            Z = M @ w
            Ms.append(M); Zs.append(Z)
            Hs.append(np.maximum(Z, 0) if k < len(W) - 1 else Z)
        L = Hs[-1][tr]
        L = L - L.max(1, keepdims=True)
        p = np.exp(L) / np.exp(L).sum(1, keepdims=True)
        losses.append(float(-np.mean(np.log(p[np.arange(len(tr)), y[tr]]))))
        dZ = np.zeros_like(Hs[-1])
        p[np.arange(len(tr)), y[tr]] -= 1
        dZ[tr] = p / len(tr)
        grads = [None] * len(W)
        for k in range(len(W) - 1, -1, -1):
            grads[k] = Ms[k].T @ dZ
            if k:
                dZ = (Ah.T @ (dZ @ W[k].T)) * (Zs[k - 1] > 0)
        for k in range(len(W)):
            m[k] = 0.9 * m[k] + 0.1 * grads[k]
            v[k] = 0.999 * v[k] + 0.001 * grads[k] ** 2
            W[k] = W[k] - lr * (m[k] / (1 - 0.9 ** t)) / (np.sqrt(v[k] / (1 - 0.999 ** t)) + 1e-8)
    return W, losses


def pred_b(Ah, X, W):
    H = np.asarray(X, float)
    for k, w in enumerate(W):
        H = np.asarray(Ah) @ H @ w
        if k < len(W) - 1:
            H = np.maximum(H, 0)
    return H.argmax(1)


def within_b(adj, i, k):
    """Nodes within k links of i by breadth-first search over a neighbour list (node i included)."""
    seen, frontier = {i}, [i]
    for _ in range(k):
        frontier = [v for u in frontier for v in adj[u] if v not in seen]
        seen.update(frontier)
    return sorted(seen)


def last_hidden_b(Ah, X, W):
    """Output of the last hidden ReLU layer of a trained stack."""
    H = np.asarray(X, float)
    for w in W[:-1]:
        H = np.maximum(np.asarray(Ah) @ H @ w, 0)
    return H


def acc_b(pred, y, tr):
    o = [i for i in range(len(y)) if i not in set(tr)]
    return sum(int(pred[i] == y[i]) for i in o) / len(o)


# ------------------------------------------------------------------ the ops module
Ag, yg = ops.planted_partition(12, 0.5, 0.1, 2)
Xg = ops.node_features(yg, 0.6, 3)
Pg = [Tensor(w) for w in ops.gcn_init([2, 5, 2], 4)]
gerr = grad_check(lambda: (ops.gcn_logits(ops.normalised_adjacency(Ag), Xg, Pg) ** 2).sum() * 0.1 + ops.gcn_logits(ops.normalised_adjacency(Ag), Xg, Pg)[np.array([0, 7])].sum(), Pg)
lv.claim(gerr < 1e-6, f'gcn_logits through the autograd: gradient check, relative error {gerr:.1e}')
from autograd import cross_entropy
gerr2 = grad_check(lambda: cross_entropy(ops.gcn_logits(ops.normalised_adjacency(Ag), Xg, Pg)[np.array([0, 1, 6, 7])], yg[np.array([0, 1, 6, 7])]), Pg)
lv.claim(gerr2 < 1e-6, f'the training loss of gcn_logits: gradient check, relative error {gerr2:.1e}')
Ab, yb = pp_b(30, 0.4, 0.05, 21)
lv.claim(np.array_equal(ops.planted_partition(30, 0.4, 0.05, 21)[0], Ab) and np.array_equal(ops.planted_partition(30, 0.4, 0.05, 21)[1], yb), 'planted_partition agrees with a double loop over the same table')
lv.claim(np.allclose(ops.normalised_adjacency(Ab), hat_b(Ab.astype(int).tolist()), atol=1e-14), 'normalised_adjacency agrees entry by entry')
lv.claim(np.allclose(ops.node_features(yb, 0.6, 5), feat_b(yb, 0.6, 5), atol=0), 'node_features agrees')
Wa, La = ops.train_gcn_params(ops.normalised_adjacency(Ab), feat_b(yb, 0.6, 5), yb, [0, 1, 15, 16], steps=30, seed=2)
Wb, Lb = train_b(hat_b(Ab.astype(int).tolist()), feat_b(yb, 0.6, 5), yb, [0, 1, 15, 16], steps=30, seed=2)
lv.claim(np.allclose(La, Lb, rtol=1e-9, atol=1e-12) and all(np.allclose(a, b, atol=1e-9) for a, b in zip(Wa, Wb)), 'train_gcn_params (autograd and nt_ops_l1 Adam) agrees with the hand backward pass and hand Adam over 30 steps')

# ================================================================== l17
VA = [[0, 1, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 0]]
deg = [sum(r) for r in VA]
lv.claim(deg == [3, 2, 2, 1] and sum(deg) == 8, 'venue degrees 3, 2, 2, 1, total 8', covers=[3, 2, 1, 8])
lv.expect('l17', 'screens[2].widget.rows[0][1].answer', deg[0])
lv.expect('l17', 'screens[2].widget.rows[3][1].answer', deg[3])
x3 = [4, 1, 2, 7]
Ax = [sum(VA[i][j] * x3[j] for j in range(4)) for i in range(4)]
lv.expect('l17', 'screens[3].widget.answer', Ax[0])
lv.expect('l17', 'screens[3].widget.wrong[0].value', Ax[0] + x3[0])
Px = step_fr(VA, x3)
lv.expect('l17', 'screens[4].widget.answer', round(float(Px[0]), 2))
lv.claim(Px[0] == Fr(10, 3) and step_fr(VA, x3, loops=True)[0] == Fr(7, 2), 'l17 average at A 10/3 = 3.33; with A itself (4 + 1 + 2 + 7) / 4 = 3.5', covers=[3.33, 3.5, 10, 14, 4])
Pp = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
Hp = hat_b(Pp)
lv.claim(close(Hp[0][0], 0.5) and close(Hp[0][1], 1 / math.sqrt(6)) and close(Hp[1][1], 1 / 3), 'path with loops: degrees 2, 3, 2; 1/2, 1/sqrt 6, 1/3',
         covers=[0.5, round(1 / math.sqrt(6), 3), 1 / 3])
lv.expect('l17', 'screens[5].widget.answer', round(Hp[0][1], 3))
lv.claim(close(1 / 6, 0.167, 1e-2) and close(1 / math.sqrt(2), 0.707, 1e-3), 'path slips 1/6 and 1/sqrt 2', covers=[0.167, 0.707, 6])
lv.claim(step_fr(VA, x3)[3] == 4 and step_fr(VA, x3, loops=True)[3] == Fr(11, 2), 'trap: D gets 4 without its loop, 5.5 with it', covers=[4, 5.5, 7])
HV = hat_b(VA)
lam = np.linalg.eigvalsh(np.array(HV))
lv.claim(close(float(lam[-1]), 1.0, 1e-12) and close(float(top_vec_b(HV) @ np.sqrt(np.array(deg) + 1) / np.linalg.norm(np.sqrt(np.array(deg) + 1))), 1.0, 1e-9),
         'venues: top eigenvalue of A_hat is 1, eigenvector along sqrt(d~) (power iteration)', covers=[1])
for i in range(4):
    for j in range(4):
        lv.expect('l17', f'screens[8].canvas.params.matrices[0].rows[{i}][{j}]', round(HV[i][j], 3))
lv.claim(close(HV[0][0], 0.25) and close(HV[0][1], 0.289, 2e-3) and close(HV[0][3], 0.354, 2e-3) and close(sum(HV[0]), 1.18, 3e-3), 'quiz: row A of A_hat is 0.25, 0.289, 0.289, 0.354, sum about 1.18',
         covers=[0.25, 0.289, 0.354, 1.18])
pq = 1 / math.sqrt((3 + 1) * (5 + 1))
lv.expect('l17', 'screens[11].widget.answer', round(pq, 3))
lv.claim(close(1 / math.sqrt(15), 0.258, 2e-3) and close(1 / 24, 0.042, 2e-2), 'bank slips 1/sqrt 15 and 1/24', covers=[0.258, 0.042, 24, 15, 0.25])
star = hat_b(adj_b(4, [(0, 1), (0, 2), (0, 3)]))
lv.expect('l17', 'quiz[0].widget.answer', round(star[0][1], 3))
lv.claim(close(1 / math.sqrt(3), 0.577, 1e-3), 'star slip 1/sqrt 3', covers=[0.577])
lv.expect('l17', 'quiz[2].widget.answer', 2 * 7)

# ================================================================== l18
eD = [0, 0, 0, 1]
xs = [eD]
for _ in range(40):
    xs.append(step_fr(VA, xs[-1]))
lv.claim(xs[1] == [Fr(1, 3), 0, 0, 0] and xs[2] == [0, Fr(1, 6), Fr(1, 6), Fr(1, 3)] and xs[3] == [Fr(2, 9), Fr(1, 12), Fr(1, 12), 0], 'hook: 1/3 at A, then 1/6, 1/6, 1/3, then 2/9, 1/12, 1/12, 0')
fr0 = F['l18-passing-messages']['screens'][0]['canvas']['controls'][0]['frames']
lv.claim(all(abs(fr0[k]['distribution'][v] - float(xs[k][i])) < 6e-4 for k in range(4) for i, v in enumerate('ABCD')), 'hook frames show the exact steps to 3 places',
         covers=[round(float(xs[k][i]), 3) for k in range(4) for i in range(4)])
pi = [Fr(d, 8) for d in deg]
fr1 = F['l18-passing-messages']['screens'][1]['canvas']['controls'][0]['frames']
ks1 = [1, 2, 3, 5, 10, 20, 40]
lv.claim(all(abs(fr1[n]['distribution'][v] - float(xs[k][i])) < 6e-4 for n, k in enumerate(ks1) for i, v in enumerate('ABCD')) and all(abs(float(xs[40][i]) - 0.125) < 1e-5 for i in range(4)),
         'many steps: frames exact to 3 places; settles at pi_D = 1/8', covers=[round(float(xs[k][i]), 3) for k in ks1 for i in range(4)] + [0.125])
lv.expect('l18', 'screens[1].widget.answer', float(pi[3]))
x2 = [2, 0, 4, 6]
lv.expect('l18', 'screens[2].widget.answer', float(step_fr(VA, x2)[1]))
lv.claim(step_fr(VA, x2, loops=True)[1] == 2, 'B with its loop: 2', covers=[2])
chg = [max(abs(a - b) for a, b in zip(xs[k], xs[k - 1])) for k in range(1, 41)]
first_small = next(k for k in range(1, 41) if chg[k - 1] < Fr(1, 1000))
lv.claim(first_small == 22 and chg[20] >= Fr(1, 1000) and float(chg[21]) < 0.00077, 'settles on the venues from 1 at D: the 21st step still moves a value by 0.00105, the 22nd first by less than 0.001 (0.00076)', covers=[22, 21, 0.001, 0.00076])
# reach in two looped steps
g7 = {'S': ['a', 'f'], 'a': ['S', 'b', 'd'], 'f': ['S'], 'b': ['a', 'c'], 'd': ['a', 'e'], 'c': ['b'], 'e': ['d']}
names = list(g7)
A7 = [[1 if names[j] in g7[names[i]] else 0 for j in range(7)] for i in range(7)]
v7 = [1 if n == 'S' else 0 for n in names]
v7 = step_fr(A7, step_fr(A7, v7, True), True)
reach = sorted(names[i] for i in range(7) if v7[i] > 0)
lv.claim(reach == sorted(F['l18-passing-messages']['screens'][3]['widget']['answer']), f'two looped steps from S reach {reach}')
lv.claim(close(1 / 3, 0.333, 1e-3), 'walk slip 1/3', covers=[0.333])
X5 = [[2, 10], [0, 4], [4, 6], [6, 8]]
c2 = step_fr(VA, [r[1] for r in X5])
lv.expect('l18', 'screens[5].widget.answer', float(c2[0]))
lv.expect('l18', 'screens[5].widget.wrong[1].value', round(float(step_fr(VA, [r[0] for r in X5])[0]), 2))
lv.claim(step_fr(VA, [r[1] for r in X5], loops=True)[0] == 7 and step_fr(VA, [r[0] for r in X5])[0] == Fr(10, 3), 'two features: own-included slip (10 + 4 + 6 + 8) / 4 = 7; first coordinate 10/3', covers=[7, 28, 3.33])
# directed
Ad = np.zeros((4, 4))
Ad[1, 0] = Ad[2, 0] = Ad[0, 3] = 1.0   # B to A, C to A, A to D: A_ij = 1 when i has lent to j
xd = np.array([5.0, 1.0, 3.0, 9.0])
out_d, in_d, both_d = (Ad @ xd)[0], (Ad.T @ xd)[0], (np.maximum(Ad, Ad.T) @ xd)[0]
lv.expect('l18', 'screens[6].widget.answer', float(out_d))
lv.expect('l18', 'screens[6].widget.wrong[0].value', float(in_d))
lv.expect('l18', 'screens[6].widget.wrong[1].value', float(both_d))
lv.claim(out_d == 9 and in_d == 4 and both_d == 13 and (Ad.T @ xd)[0] != (Ad @ xd)[0], 'directed: (A x)_A collects D 9; (A^T x)_A the arrows into A, 1 + 3 = 4; symmetrised 1 + 3 + 9 = 13', covers=[9, 4, 13])
SQ = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]
sq = [[1, 0, 0, 0]]
for _ in range(100):
    sq.append(step_fr(SQ, sq[-1]))
sql = [[1, 0, 0, 0]]
for _ in range(60):
    sql.append(step_fr(SQ, sql[-1], True))
lv.claim(sq[100][0] == Fr(1, 2) and sq[99][0] == 0 and abs(float(sql[60][0]) - 0.25) < 1e-9, 'square: A holds 1/2 on even steps, 0 on odd; with loops settles at 1/4', covers=[0.5, 0.25, 100])
frq = F['l18-passing-messages']['screens'][7]['canvas']['controls'][0]['frames']
lv.claim(all(abs(frq[k - 1]['distribution'][v] - float(sq[k][i])) < 6e-4 for k in range(1, 7) for i, v in enumerate('ABCD')), 'square frames exact')
expl = F['l18-passing-messages']['screens'][7]['explain']['canvas']['distribution']
lv.claim(all(abs(expl[v] - float(sql[6][i])) < 6e-4 for i, v in enumerate('ABCD')), 'square with loops at step 6, to 3 places', covers=[round(float(sql[6][i]), 3) for i in range(4)])
lim8 = sum(p * x for p, x in zip(pi, x2))
lv.expect('l18', 'screens[8].widget.answer', float(lim8))
lv.claim(lim8 == Fr(5, 2) and Fr(sum(x2), 4) == 3 and pi == [Fr(3, 8), Fr(2, 8), Fr(2, 8), Fr(1, 8)], 'settled value 20/8 = 2.5 (plain mean 3); pi = 3/8, 2/8, 2/8, 1/8', covers=[2.5, 3, 20, 6, 8, 0.375, 0.125])
hub = adj_b(5, [(0, k) for k in range(1, 5)])
s1 = step_fr(hub, [0, 1, 0, 0, 0], True)
s2 = step_fr(hub, s1, True)
lv.expect('l18', 'screens[11].widget.answer', round(float(s2[2]), 2))
lv.claim(s1[0] == Fr(1, 5) and s2[2] == Fr(1, 10) and step_fr(hub, step_fr(hub, [0, 1, 0, 0, 0]))[2] == Fr(1, 4), 'contagion: H 1/5 after one day, L2 1/10 after two; without loops 1/4',
         covers=[0.2, 0.1, 0.25])
lv.claim(all(abs(F['l18-passing-messages']['screens'][11]['explain']['canvas']['distribution'][n] - float(s2[i])) < 6e-4 for i, n in enumerate(['H', 'L1', 'L2', 'L3', 'L4'])),
         'contagion day-two values to 3 places', covers=[round(float(v), 3) for v in s2])
lv.expect('l18', 'quiz[0].widget.answer', float(step_fr(adj_b(3, [(0, 1), (1, 2)]), [3, 0, 6])[1]))
lv.claim(step_fr(adj_b(3, [(0, 1), (1, 2)]), [3, 0, 6], True)[1] == 3, 'path quiz slip 3', covers=[3])
dl = [4, 2, 2, 2]
lv.expect('l18', 'quiz[2].widget.answer', float(Fr(dl[0], sum(dl)) * 4))
lv.claim(Fr(dl[0], sum(dl)) == Fr(4, 10) and Fr(3, 6) * 4 == 2, 'star limit: 4/10 of 4 = 1.6; without loops 3/6 of 4 = 2', covers=[1.6, 2, 1])

# ================================================================== l19
A19, y19 = pp_b(20, 0.35, 0.05, 9)
X19 = np.round(feat_b(y19, 0.6, 509), 1)
H19 = hat_b(A19.astype(int).tolist())
W1 = np.array([[4.2, -2.5], [-3.6, 1.8]]); W2 = np.array([[-4.4, 4.3], [3.2, -1.7]])
nb1 = [j for j in range(20) if A19[1, j]]
lv.claim(nb1 == [0, 9] and int(A19[0].sum()) == 3 and int(A19[9].sum()) == 2, 'node 1 is linked to 0 (3 links) and 9 (2 links)')
mix1 = sum(H19[1][j] * X19[j] for j in [1] + nb1)
for i, j in enumerate([1, 0, 9]):
    lv.claim(F['l19-a-gcn-layer']['screens'][0]['canvas']['right']['params']['rows'][i][1] == f'{H19[1][j]:.3f}', f'table row {j}: weight {H19[1][j]:.3f}', covers=[round(H19[1][j], 3)])
lv.claim(all(abs(float(F['l19-a-gcn-layer']['screens'][0]['canvas']['right']['params']['rows'][i][2 + c].replace('−', '-')) - X19[j, c]) < 1e-9 for i, j in enumerate([1, 0, 9]) for c in range(2)),
         'table rows: node 1, 0 and 9 features', covers=[abs(X19[j, c]) for j in (1, 0, 9) for c in range(2)])
lv.expect('l19', 'screens[0].widget.rows[0][1].answer', round(float(mix1[0]), 2))
lv.expect('l19', 'screens[0].widget.rows[1][1].answer', round(float(mix1[1]), 2))
lv.claim(close(round(float(X19[[1, 0, 9], 0].mean()), 2), -0.53) and close(float(X19[[1, 0, 9], 0].sum()), -1.6), 'node 1 slips: plain mean -0.53, sum -1.6', covers=[0.53, 1.6])
z1 = mix1 @ W1
lv.claim(close(round(float(z1[0]), 2), -3.27) and close(round(float(z1[1]), 2), 1.84) and abs(np.array([-0.51, 0.32]) @ W1[:, 1] - z1[1]) < 0.02, 'node 1: pre-activation (-3.27, 1.84); from the rounded row within 0.02',
         covers=[3.27, 1.84, 0.51, 0.32, 0.333, 0.289, 0.6, 0.4, 0.1, 1.1, 4.2, 3.6, 2.5, 1.8])
zr = np.array([-0.51, 0.32]) @ W1
lv.claim(close(round(float(zr[0]), 2), -3.29) and close(round(float(zr[1]), 2), 1.85) and close(round(float(z1[0]), 2), -3.27) and close(round(float(z1[1]), 2), 1.84),
         'node 1: the rounded row gives (-3.29, 1.85); the unrounded row (-3.27, 1.84)', covers=[3.29, 1.85, 3.27, 1.84])
lv.expect('l19', 'screens[1].widget.rows[1][1].answer', round(float(max(z1[1], 0)), 2))
lv.expect('l19', 'screens[1].widget.rows[0][1].wrong[0].value', round(float(z1[0]), 2))
mix4 = H19[4][4] * X19[4] + H19[4][8] * X19[8]
z4 = mix4 @ W1
lv.claim(int(A19[4].sum()) == 1 and int(A19[8].sum()) == 4 and close(H19[4][4], 0.5) and close(H19[4][8], 1 / math.sqrt(10)), 'node 4: one link, to node 8 with 4 links; 1/2 and 1/sqrt 10',
         covers=[0.5, round(1 / math.sqrt(10), 3), 10, 1.2, 1.5, 0.3])
lv.expect('l19', 'screens[2].widget.answer', round(float(max(z4[1], 0)), 2))
lv.claim(close(round(float(mix4[0]), 2), -0.77) and close(round(float(mix4[1]), 2), 0.69) and close(round(float(z4[0]), 2), -5.75), 'node 4 mixed row (-0.77, 0.69), pre-activation -5.75', covers=[0.77, 0.69, 5.75, 3.19])
lv.expect('l19', 'screens[2].widget.wrong[0].value', round(float(X19[[4, 8]].mean(0) @ W1[:, 1]), 2))
lv.expect('l19', 'screens[2].widget.wrong[1].value', round(float(X19[[4, 8]].sum(0) @ W1[:, 1]), 2))
lv.expect('l19', 'screens[3].widget.answer', 2 * 16 + 16 * 2)
lv.claim(64 * 20000 == 1280000 and 2 * 2 * 2 == 8 and 2 * 16 == 32, 'weights: 64; slips 1,280,000, 8 and 32', covers=[1280000, 8, 32, 20000, 64, 16])
two = sorted({1, *nb1} | {j for k in nb1 for j in range(20) if A19[k, j]})
lv.claim(two == [int(s[1:]) for s in sorted(F['l19-a-gcn-layer']['screens'][4]['widget']['answer'], key=lambda s: int(s[1:]))] and two == [0, 1, 3, 8, 9, 12], 'two layers see nodes 0, 1, 3, 8, 9, 12', covers=[12])
hi = np.array([0.5, -1.0]); zi = hi @ W1
lv.expect('l19', 'screens[6].widget.answer', round(float(max(zi[0], 0)), 2))
lv.claim(close(float(zi[0]), 5.7) and close(float(zi[1]), -3.05) and close(0.5 * 4.2, 2.1), 'isolated firm: (5.7, -3.05) before ReLU; 2.1 + 3.6', covers=[5.7, 3.05, 2.1, 0.5, 1.0])
out19 = np.array(H19) @ np.maximum(np.array(H19) @ X19 @ W1, 0) @ W2
lv.claim(int((out19.argmax(1) == y19).sum()) == 20, 'the supplied network labels all 20 nodes correctly', covers=[20])
tv = 2.0 / math.sqrt(4 * 4) + 1.0 / math.sqrt(4 * 2) + 4.0 / math.sqrt(4 * 3) + 3.0 / math.sqrt(4 * 5)
lv.expect('l19', 'screens[10].widget.answer', round(tv, 2))
lv.claim(close(round(1 / math.sqrt(8), 3), 0.354) and close(round(4 / math.sqrt(12), 3), 1.155) and close(round(3 / math.sqrt(20), 3), 0.671) and (2 + 1 + 4 + 3) / 4 == 2.5,
         'supply chain: 0.5 + 0.354 + 1.155 + 0.671; slips 2.5 and 10', covers=[0.354, 1.155, 0.671, 2.5, 10, 2.0, 1.0, 4.0, 3.0, 12, 20])
lv.expect('l19', 'quiz[0].widget.answer', 8 * 32 + 32 * 3)
lv.claim(100 * 32 + 32 * 7 == 3424 and 100 * 32 * 7 == 22400, 'gcn_params(100, 32, 7) = 3424 (the product slip 22,400)', covers=[3424, 100, 7])
lv.claim(8 * 32 * 3 == 768 and 8 * 32 + 32 + 32 * 3 + 3 == 387, 'quiz slips 768 and 387', covers=[768, 387, 352])
lv.claim((0.5 * np.array([1, 2]) + 0.5 * np.array([3, 0])) @ np.array([-1, 1]) == -1, 'quiz: mixed row (2, 1), -1 before ReLU', covers=[1, 2, 0])

# ================================================================== l20 (route B retrains everything)
TR = [0, 1, 20, 21]
A20, y20 = pp_b(40, 0.3, 0.03, 13)
X20 = feat_b(y20, 0.6, 113)
H20 = np.array(hat_b(A20.astype(int).tolist()))
Wg, Lg = train_b(H20, X20, y20, TR)
pg = pred_b(H20, X20, Wg)
n_g = sum(int(pg[i] == y20[i]) for i in range(40) if i not in TR)
Wm, _ = train_b(np.eye(40), X20, y20, TR)
n_m = sum(int(pred_b(np.eye(40), X20, Wm)[i] == y20[i]) for i in range(40) if i not in TR)
lv.claim(n_g == 35 and n_m == 21, f'seed 13: graph network {n_g} of 36, per-node {n_m} of 36 (hand backprop)', covers=[35, 21, 36, 40, 200, 16])
lv.expect('l20', 'screens[2].widget.answer', round(n_g / 36, 3))
lv.expect('l20', 'screens[2].widget.wrong[0].value', round((n_g + 4) / 40, 3))
lv.expect('l20', 'screens[3].widget.answer', n_g - n_m)
lv.claim(close(round(n_m / 36, 2), 0.58) and close(round(n_g / 36, 2), 0.97), 'seed 13 rounded: 0.97 and 0.58', covers=[0.97, 0.58, 0.583, 0.972, 15])
wrong_ids = [i for i in range(40) if i not in TR and pg[i] != y20[i]]
lv.claim(wrong_ids == [33], 'the one wrong firm is firm 33', covers=[33])
nb3 = [j for j in range(40) if A20[3, j]]
lv.claim(all(y20[j] == 0 for j in nb3) and len(nb3) == 5 and close(round(float(X20[3, 0]), 2), 1.88), 'firm 3: all 5 links on the blue side; first number 1.88', covers=[5, 1.88, 0.3, 0.03, 10])
means = {'gcn': [], 'mlp': [], 'ns': [], 'deep': []}
KS = [0, 1, 2, 4, 8, 16, 32, 64, 128]
sgc = {k: [] for k in KS}
for s in range(20):
    A, y = pp_b(40, 0.3, 0.03, s)
    X = feat_b(y, 0.6, 100 + s)
    Ah = np.array(hat_b(A.astype(int).tolist()))
    W, _ = train_b(Ah, X, y, TR); means['gcn'].append(acc_b(pred_b(Ah, X, W), y, TR))
    W, _ = train_b(np.eye(40), X, y, TR); means['mlp'].append(acc_b(pred_b(np.eye(40), X, W), y, TR))
    An, _ = pp_b(40, 0.165, 0.165, s)
    Ahn = np.array(hat_b(An.astype(int).tolist()))
    W, _ = train_b(Ahn, X, y, TR); means['ns'].append(acc_b(pred_b(Ahn, X, W), y, TR))
    Ak = np.eye(40)
    for k in range(KS[-1] + 1):
        if k in sgc:
            Z = Ak @ X
            W, _ = train_b(np.eye(40), Z, y, TR, layers=1)
            sgc[k].append(acc_b(pred_b(np.eye(40), Z, W), y, TR))
        Ak = Ah @ Ak
    W, Ld = train_b(Ah, X, y, TR, layers=16); means['deep'].append(acc_b(pred_b(Ah, X, W), y, TR)); means.setdefault('stuck', []).append(Ld[-1] > 0.6)
    means.setdefault('one', []).append(len(set(pred_b(Ah, X, W).tolist())) == 1); means.setdefault('dead', []).append(bool(np.all(last_hidden_b(Ah, X, W) == 0)))
mg, mm, mn, md = (float(np.mean(means[k])) for k in ('gcn', 'mlp', 'ns', 'deep'))
bars3 = F['l20-labels-on-a-graph']['screens'][3]['canvas']['state']['values']
lv.claim(close(bars3['gcn']['mean'], round(mg, 2)) and close(bars3['mlp']['mean'], round(mm, 2)) and close(bars3['gcn']['this'], 0.97) and close(bars3['mlp']['this'], 0.58),
         f'20 graphs: graph network {mg:.3f}, per-node {mm:.3f} (hand backprop)', covers=[round(mg, 2), round(mm, 2)])
bars6 = F['l20-labels-on-a-graph']['screens'][6]['canvas']['state']['values']
lv.claim(close(bars6['gcn']['nosig'], round(mn, 2)) and close(bars6['gcn']['comm'], round(mg, 2)) and close(bars6['mlp']['nosig'], round(mm, 2)) and mn <= mm, f'no signal: graph network {mn:.3f}, no better than per-node {mm:.3f}',
         covers=[round(mn, 2), 0.165])
sgm = {k: round(float(np.mean(v)), 2) for k, v in sgc.items()}
bars5 = F['l20-labels-on-a-graph']['screens'][5]['canvas']['state']['values']
lv.claim(all(close(bars5[str(k)], sgm[k]) for k in KS), f'linear k-step accuracies {sgm} (hand backprop)', covers=list(sgm.values()))
best = max(KS, key=lambda k: np.mean(sgc[k]))
lv.expect('l20', 'screens[5].widget.answer', best)
lv.claim(close(round(md, 2), 0.55), f'16 ReLU layers: mean accuracy {md:.3f}', covers=[round(md, 2), 128])
lv.claim(sum(means['dead']) >= 11 and sum(means['one']) == 17, f"16 ReLU layers, hand backprop: {sum(means['one'])} of 20 runs predict one class, {sum(means['dead'])} have every unit of the last hidden layer dead", covers=[17, 20])
ones_a = dead_a = zero_a = 0
for s_ in range(20):
    Aa, ya = ops.planted_partition(40, 0.3, 0.03, s_)
    Xa = ops.node_features(ya, 0.6, 100 + s_)
    Aha = ops.normalised_adjacency(Aa)
    Wa_, _ = ops.train_gcn_params(Aha, Xa, ya, TR, layers=16)
    Ha = last_hidden_b(Aha, Xa, Wa_)
    out_a = Aha @ Ha @ Wa_[-1]
    ones_a += len(set(out_a.argmax(1).tolist())) == 1
    dead_a += bool(np.all(Ha == 0))
    zero_a += bool(np.all(out_a == 0))
lv.claim(ones_a == 17 and dead_a == 11 and zero_a == 11, f'16 ReLU layers, the generator route (autograd): {ones_a} of 20 runs predict one class; in {dead_a} every unit of the last hidden layer is dead, so the output is 0 at every node ({zero_a})',
         covers=[11, 16, 20])
lv.claim(sum(means['stuck']) == 14, f"16 ReLU layers: {sum(means['stuck'])} of 20 runs end with training loss above 0.6", covers=[14, 0.6])
accs40 = [acc_b(pred_b(H20, X20, train_b(H20, X20, y20, TR, steps=n)[0]), y20, TR) for n in range(1, 41)]
lv.claim(accs40[39] == 35 / 36 and max(accs40) == 1.0 and [n + 1 for n, a_ in enumerate(accs40) if a_ == 1.0] == [36, 37] and round(accs40[39], 6) == 0.972222,
         'train_gcn hidden test 7: accuracy 0.972222 after 40 steps; steps 36 and 37 reach 1.0, so a solution that keeps the best step on the unlabelled nodes reports 1.0', covers=[40, 36, 37])
dt = A20.sum(1) + 1
ratio = math.sqrt(dt[2] / dt[17])
vv = top_vec_b(H20)
lv.claim(close(abs(vv[2] / vv[17]), ratio, 1e-6) and int(dt[2]) == 2 and int(dt[17]) == 11, f'firm 2 (1 link) against firm 17 (10 links): power iteration ratio {abs(vv[2] / vv[17]):.6f} = sqrt(2/11)', covers=[2, 11])
lv.expect('l20', 'screens[7].widget.answer', round(ratio, 3))
lv.expect('l20', 'screens[7].widget.wrong[0].value', round(2 / 11, 3))
lv.expect('l20', 'screens[7].widget.wrong[1].value', round(math.sqrt(1 / 10), 3))


def spread_b(Ah, X, k, v):
    Z = np.linalg.matrix_power(Ah, k) @ X
    return float(np.linalg.norm(Z - np.outer(v, v @ Z)) / np.linalg.norm(Z))


v20 = vv / np.linalg.norm(vv)
spb = [spread_b(H20, X20, k, v20) for k in KS]
sb = F['l20-labels-on-a-graph']['screens'][10]['canvas']['state']['values']
lv.claim(all(close(sb[str(k)], round(spb[i], 2)) for i, k in enumerate(KS)), f'feature spread by power iteration {np.round(spb, 3).tolist()}', covers=[round(x_, 2) for x_ in spb] + [0.69])
# scatter frames of A_hat^k X
sc = F['l20-labels-on-a-graph']['screens'][1]['canvas']
Z2 = H20 @ H20 @ X20
lv.claim(all(abs(sc['controls'][0]['frames'][2]['points'][f'p{i}']['x'] - Z2[i, 0]) < 6e-4 for i in range(40)), 'scatter frame for 2 steps matches')
# transfer and quizzes
lv.claim(close(0.71 - 0.70, 0.01, 1e-9), 'transfer: a 0.01 gap', covers=[0.71, 0.70, 0.01])
lv.literal('2,000', why='the unlisted firms in the transfer scenario are a given count')
lv.literal('150', why='the known firms in the transfer scenario are a given count')
lv.expect('l20', 'quiz[0].widget.answer', 41 / 50)
lv.claim(close(51 / 60, 0.85), 'quiz slip 51/60', covers=[0.85, 41, 50, 51, 60])
lv.expect('l20', 'quiz[2].widget.answer', math.sqrt(4 / 16))
lv.claim(close(round(math.sqrt(3 / 15), 3), 0.447), 'quiz slips 0.25 and sqrt(3/15)', covers=[0.25, 0.447, 4, 16, 15])

# ================================================================== code widgets: model solution and a twin
TW = {
    'adjacency': '''import numpy as np
def adjacency(edges, n):
    A = [[0.0] * n for _ in range(n)]
    for e in edges:
        A[e[0]][e[1]] = A[e[1]][e[0]] = 1.0
    return np.array(A)
def row_normalised(A):
    return np.array([[v / sum(r) for v in r] for r in np.asarray(A, dtype=float).tolist()])
''',
    'normalised_adjacency': '''import numpy as np, math
def normalised_adjacency(A):
    A = np.asarray(A, dtype=float).tolist(); n = len(A)
    d = [sum(A[i]) + 1 for i in range(n)]
    return np.array([[(1.0 if i == j else A[i][j]) / math.sqrt(d[i] * d[j]) for j in range(n)] for i in range(n)])
''',
    'message_step': '''import numpy as np
def message_step(A, X, self_loops):
    A = np.asarray(A, dtype=float); X = np.asarray(X, dtype=float)
    out = []
    for i in range(len(A)):
        nb = [j for j in range(len(A)) if A[i, j] or (self_loops and j == i)]
        w = [A[i, j] + (1.0 if self_loops and j == i else 0.0) for j in nb]
        out.append(sum(wi * X[j] for wi, j in zip(w, nb)) / sum(w))
    return np.array(out)
def k_steps(A, X, k):
    P = np.asarray(A, dtype=float) / np.asarray(A, dtype=float).sum(1)[:, None]
    return np.linalg.matrix_power(P, k) @ np.asarray(X, dtype=float)
''',
    'settles': '''import numpy as np
def settles(A, x, k, tol):
    A = np.asarray(A, dtype=float); P = A / A.sum(1)[:, None]
    a = np.linalg.matrix_power(P, k) @ np.asarray(x, dtype=float)
    b = np.linalg.matrix_power(P, k - 1) @ np.asarray(x, dtype=float) if k > 0 else a
    return bool(all(abs(u - w) < tol for u, w in zip(a, b)))
''',
    'gcn_layer': '''import numpy as np
def gcn_layer(A_hat, H, W):
    return np.clip(np.asarray(A_hat) @ (np.asarray(H) @ np.asarray(W)), 0, None)
def gcn_layer_loop(A_hat, H, W):
    A_hat, H, W = np.asarray(A_hat), np.asarray(H), np.asarray(W)
    rows = []
    for i in range(len(H)):
        z = [sum(A_hat[i, j] * float(H[j] @ W[:, c]) for j in range(len(H)) if A_hat[i, j] != 0) for c in range(W.shape[1])]
        rows.append([max(v, 0.0) for v in z])
    return np.array(rows)
''',
    'gcn_forward': '''import numpy as np
def gcn_forward(A_hat, X, params):
    h = np.asarray(X)
    for k, W in enumerate(params):
        h = np.asarray(A_hat) @ (h @ W)
        if k < len(params) - 1:
            h = np.where(h > 0, h, 0.0)
    return h
def gcn_params(d_in, d_hidden, d_out):
    return sum(a * b for a, b in ((d_in, d_hidden), (d_hidden, d_out)))
''',
    'planted_partition': '''import numpy as np
def planted_partition(n, p_in, p_out, seed):
    U = np.random.default_rng(seed).random((n, n))
    A = np.zeros((n, n)); y = np.array([0 if i < n // 2 else 1 for i in range(n)])
    for i in range(n):
        for j in range(i + 1, n):
            if U[i, j] < (p_in if y[i] == y[j] else p_out):
                A[i, j] = A[j, i] = 1.0
    return A, y
''',
    'train_gcn': '''import numpy as np
def train_gcn(A_hat, X, y, train_idx, steps, lr, seed):
    W, losses = _train(np.asarray(A_hat, dtype=float), X, np.asarray(y), list(train_idx), 2, 16, steps, lr, seed)
    return _acc(_pred(np.asarray(A_hat, dtype=float), X, W), np.asarray(y), list(train_idx)), losses
''',
    'feature_spread': '''import numpy as np
def feature_spread(A_hat, X, depth):
    A_hat = np.asarray(A_hat, dtype=float)
    v = _top(A_hat); v = v / np.linalg.norm(v)
    return [_spread(A_hat, X, k, v) for k in range(depth + 1)]
''',
    'gcn_node_classifier': '''import numpy as np
def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    n = len(X); A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    Ah = np.array(_hat(A.astype(int).tolist()))
    W, losses = _train(Ah, X, np.asarray(y), list(train_idx), layers, 16, steps, lr, seed)
    return _pred(Ah, X, W), losses
''',
    'nodes_within': '''import numpy as np
def nodes_within(A, i, k):
    M = np.linalg.matrix_power(np.asarray(A, dtype=float) + np.eye(len(A)), k)
    return [int(j) for j in np.nonzero(M[i] > 0)[0]]
''',
}
HELP = {'_train': lambda Ah, X, y, tr, L, h, steps, lr, seed: train_b(Ah, X, y, tr, layers=L, hidden=h, steps=steps, lr=lr, seed=seed),
        '_pred': pred_b, '_acc': acc_b, '_top': top_vec_b, '_spread': spread_b, '_hat': hat_b}


def same(got, want, cmp, tol):
    def norm(v):
        if hasattr(v, 'tolist'):
            v = v.tolist()
        if isinstance(v, tuple):
            v = list(v)
        if isinstance(v, list):
            return [norm(x_) for x_ in v]
        return v
    got, want = norm(got), norm(want)
    if cmp == 'isclose':
        def cl(a, b):
            if isinstance(a, list) or isinstance(b, list):
                return isinstance(a, list) and isinstance(b, list) and len(a) == len(b) and all(cl(x_, y_) for x_, y_ in zip(a, b))
            if isinstance(a, bool) or isinstance(b, bool):
                return a == b
            return math.isclose(a, b, rel_tol=(tol or {}).get('rel', 1e-9) or 0, abs_tol=(tol or {}).get('abs', 1e-12) or 0)
        return cl(got, want)
    return got == want


def run_widget(w, src, label, approx=False):
    cwd = os.getcwd(); os.chdir(DATA)
    try:
        ns = {'__name__': '__zq__', '__learner_source__': src}
        ns.update(HELP)
        exec(ZQ_LIB, ns); exec(w.get('prelude', 'import numpy as np\n'), ns); exec('import numpy as np\n', ns); exec(src, ns)
        ok_all = True
        for k, t in enumerate(w['tests']):
            if t.get('setup'):
                exec(t['setup'], ns)
            got = eval(t['call'], ns)
            want = eval(t['expect'], {'None': None})
            ok = same(got, want, t.get('compare', 'equal'), t.get('tol'))
            if not ok and approx:
                ok = same(got, want, 'isclose', {'rel': 1e-6, 'abs': 2e-6})
            ok_all &= ok
            if not ok:
                print('   mismatch', label, 'test', k + 1, str(got)[:80], 'vs', t['expect'][:80])
        return ok_all
    finally:
        os.chdir(cwd)


n_code = 0
for fid, doc in F.items():
    for key in ('screens', 'items'):
        for i, sc_ in enumerate(doc.get(key, [])):
            w_ = sc_.get('widget')
            if not (isinstance(w_, dict) and w_.get('kind') == 'code'):
                continue
            n_code += 1
            lv.claim(run_widget(w_, w_['solution'], f'{fid} {key}[{i}]'), f'{fid} {key}[{i}]: the model solution passes every hidden test in CPython')
            name = next(k for k in TW if f'def {k}(' in w_['solution'])
            lv.claim(run_widget(w_, TW[name], f'{fid} {key}[{i}] twin', approx=True), f'{fid} {key}[{i}]: an independent twin ({name}) agrees (rounded results within 2e-6)')
            lv.claim(len(w_.get('mutants', [])) >= 2, f'{fid} {key}[{i}]: at least two mutants')
lv.claim(n_code == 11, 'eleven code widgets in the level')

# thresholds with margin across seeds (route B)
for sd in range(4):
    for gs in (13, 1):
        A, y = pp_b(40, 0.3, 0.03, gs); X = feat_b(y, 0.6, 100 + gs); Ah = np.array(hat_b(A.astype(int).tolist()))
        W, _ = train_b(Ah, X, y, TR, seed=sd)
        a = acc_b(pred_b(Ah, X, W), y, TR)
        lv.claim(a >= 0.9, f'train_gcn threshold 0.85 holds with margin: graph {gs}, seed {sd}: {a:.3f}')
    A, y = pp_b(40, 0.3, 0.03, 7); X = feat_b(y, 0.6, 107); Ah = np.array(hat_b(A.astype(int).tolist()))
    W, _ = train_b(Ah, X, y, TR, seed=sd)
    lv.claim(acc_b(pred_b(Ah, X, W), y, TR) >= 0.9, f'classifier threshold 0.85 holds with margin on graph 7, seed {sd}')
    A, y = pp_b(40, 0.3, 0.03, 13); X = feat_b(y, 0.6, 113); A[30, :] = 0; A[:, 30] = 0; Ah = np.array(hat_b(A.astype(int).tolist()))
    W, L = train_b(Ah, X, y, TR, seed=sd)
    lv.claim(acc_b(pred_b(Ah, X, W), y, TR) >= 0.85 and np.all(np.isfinite(L)), f'isolated-node threshold 0.8 holds with margin, seed {sd}')
    A, y = pp_b(40, 0.165, 0.165, 4 + 10 * sd); X = feat_b(y, 0.0, 204 + 10 * sd); Ah = np.array(hat_b(A.astype(int).tolist()))
    W, _ = train_b(Ah, X, y, TR, seed=sd)
    a = acc_b(pred_b(Ah, X, W), y, TR)
    lv.claim(a <= 0.7, f'no-signal bound 0.75 holds with margin, graph {4 + 10 * sd}, seed {sd}: {a:.3f}')
lv.literal('0.85, 0.8, 0.75, 0.002, 0.001, 300, 30, 1e-9, 1e-3', why='thresholds, tolerances and graph sizes in how lines are settings of the hidden tests, which this script runs and checks with margin')

# ================================================================== review, homework, problems
lv.expect('review', 'items[0].widget.answer', round(1 / math.sqrt(5 * 3), 3))
lv.claim(close(round(1 / math.sqrt(8), 3), 0.354) and close(round(1 / 15, 3), 0.067) and 1 / 5 == 0.2, 'review slips', covers=[0.354, 0.067, 0.2, 15])
lv.expect('review', 'items[1].widget.answer', float(Fr(6 + 2 + 4, 3)))
path6 = [[v for v in (u - 1, u + 1) if 0 <= v < 6] for u in range(6)]
lv.expect('review', 'items[2].widget.answer', len(within_b(path6, 0, 2)))
lv.expect('review', 'items[2].widget.wrong[0].value', len(within_b(path6, 0, 1)))
lv.expect('review', 'items[2].widget.wrong[1].value', 1 + 2 * 2)
lv.expect('review', 'items[4].widget.answer', 4 * 8 + 8 * 8 + 8 * 2)
lv.claim(4 * 8 == 32 and 8 * 8 == 64 and 8 * 2 == 16 and 4 * 8 + 8 * 2 == 48 and 4 * 8 + 8 + 64 + 8 + 16 + 2 == 130, 'review weights 32 + 64 + 16; slips 48 and 130', covers=[32, 64, 16, 112, 48, 130])
tri = adj_b(4, [(0, 1), (1, 2), (2, 0), (2, 3)])
x_ = [0, 0, 8, 0]
xx = [x_]
for _ in range(200):
    xx.append(step_fr(tri, xx[-1]))
lv.expect('review', 'items[6].widget.answer', round(float(xx[200][0]), 6))
xl = [Fr(v) for v in x_]
for _ in range(300):
    xl = step_fr(tri, xl, loops=True)
lv.claim(abs(float(xx[200][0]) - 3) < 1e-9 and Fr(sum(x_), 4) == 2 and abs(float(xl[0]) - 8 / 3) < 1e-9 and close(round(float(xl[0]), 3), 2.667, 1e-9),
         'review limit 3 (iterated 200 steps, 3/8 of 8); slips: plain mean 2, and 2.667 = 8/3 with self-loops (iterated 300 steps)', covers=[3, 2, 2.667, 8, 0.375])
lv.literal('30', why='the 30 layers in the review prompt are a given setting')
lv.claim(close(1 / 3, 0.3333, 1e-3), 'walk 1/3', covers=[1 / 3])
lv.claim(50 - 6 == 44, 'review: 44 of 50 unlabelled', covers=[44, 6, 50])
# homework
ring = [3, 1, 4, 1, 5]
rg = adj_b(5, [(k, (k + 1) % 5) for k in range(5)])
rr = [ring]
for _ in range(300):
    rr.append([float(v) for v in step_fr(rg, rr[-1])])
lv.expect('homework', 'items[4].widget.answer', round(rr[-1][0], 6))
lv.claim(abs(rr[-1][0] - 2.8) < 1e-9 and Fr(14, 5) == Fr(28, 10), 'ring of 5 settles at 14/5 = 2.8 (iterated)', covers=[2.8, 14, 5, 3])
tree = {0: [1, 2, 3], 1: [0, 4, 5], 2: [0, 6, 7], 3: [0, 8, 9], 4: [1], 5: [1], 6: [2], 7: [2], 8: [3], 9: [3]}
w2, w1 = within_b(tree, 0, 2), within_b(tree, 0, 1)
lv.expect('homework', 'items[5].widget.answer', len(w2))
lv.expect('homework', 'items[5].widget.wrong[0].value', len(w2) - 1)
lv.expect('homework', 'items[5].widget.wrong[1].value', len(w1))
lv.expect('homework', 'items[5].widget.wrong[2].value', len(w2) + len(w1) - 1)
lv.claim(len(w2) == 10 and len(w2) - len(w1) == 6 and len(w1) == 4, 'two links out of F (breadth-first search): 10 firms, 6 of them two links away, 4 within one', covers=[10, 6, 4, 9, 13])
lv.claim(close(sum(HV[0]), 1.18, 3e-3), 'homework order distractor: row A sums to about 1.18', covers=[1.18])
lv.literal('16', why='the hidden width 16 in the classifier prompt is a given setting')
Bn = np.zeros((6, 6)); Bn[0, 1] = Bn[1, 0] = Bn[3, 4] = Bn[4, 3] = Bn[4, 5] = Bn[5, 4] = 1
nbB = [[j for j in range(6) if Bn[u, j]] for u in range(6)]
pat = np.nonzero(np.linalg.matrix_power(Bn, 2)[2] + np.linalg.matrix_power(Bn, 1)[2])[0].tolist()
lv.claim(within_b(nbB, 2, 2) == [2] and pat == [], 'nodes_within on an isolated node: the node itself, though A^2 + A has an empty row there', covers=[2])
rub = F['homework-5']['items'][3]['rubric']
lv.claim(sum(r['points'] for r in rub) == 10, 'longform rubric totals 10', covers=[10])
# problems
SQD = adj_b(4, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)])
HS = hat_b(SQD)
lv.expect('problems', 'items[0].parts[0].widget.answer', round(HS[0][2], 4))
lv.expect('problems', 'items[0].parts[1].widget.answer', round(HS[0][1], 3))
v2 = HS[1][0] * 2 + HS[1][1] * 6 + HS[1][2] * 0
lv.expect('problems', 'items[0].parts[2].widget.answer', round(v2, 3))
lv.expect('problems', 'items[0].parts[3].widget.answer', round(1.5 * v2, 2))
lv.claim(close(HS[1][1], 1 / 3) and close(round(2 / math.sqrt(12), 3), 0.577) and close(round(-v2, 2), -2.58) and close(round(1 / math.sqrt(6), 3), 0.408) and close(round(1 / 12, 3), 0.083),
         'square pieces: 1/3, 0.577, 3.87 and -2.58; slips 0.408, 0.083, 2.667', covers=[0.25, 0.289, 2.577, 3.87, 2.58, 0.577, 0.408, 0.083, 2.667, 1 / 3, 1.5, 4, 16, 12])
P3 = adj_b(3, [(0, 1), (1, 2)])
p1 = step_fr(P3, [6, 0, 0])
p2 = step_fr(P3, p1)
lv.expect('problems', 'items[1].parts[0].widget.answer', float(p1[1]))
lv.expect('problems', 'items[1].parts[1].widget.answer', float(p2[0]))
pl = [[6, 0, 0]]
for _ in range(200):
    pl.append(step_fr(P3, pl[-1], True))
lv.expect('problems', 'items[1].parts[2].widget.answer', round(float(pl[-1][0]), 3))
lv.claim(abs(float(pl[-1][1]) - 12 / 7) < 1e-9 and Fr(2, 7) * 6 == Fr(12, 7) and Fr(1, 4) * 6 == Fr(3, 2), 'path with loops settles at 12/7 (iterated); slip 1.5', covers=[2 / 7, 1.714, 1.5, 12, 7, 2, 6, 3])
tv3 = top_vec_b(hat_b(P3))
lv.expect('problems', 'items[1].parts[3].widget.answer', round(float(tv3[1] / tv3[0]), 3))
lv.claim(close(round(math.sqrt(2), 3), 1.414), 'path ratio slips 1.5 and sqrt 2', covers=[1.414, 1.225])
lv.expect('problems', 'items[2].parts[0].widget.answer', 2 * 16 + 16 * 3)
lv.claim(2 * 16 + 16 * 2 == 64 and 2 * 16 * 3 == 96, 'problem 3 slips 64 and 96', covers=[64, 96, 80])
lv.expect('problems', 'items[2].parts[1].widget.answer', 380 / 475)
lv.claim(close(405 / 500, 0.81) and 380 - 295 == 85 and 475 - 295 == 180, 'problem 3: 405/500 = 0.81; 85 more; slip 180', covers=[0.81, 405, 500, 85, 180, 380, 475, 295, 297, 25])
lv.expect('problems', 'items[2].parts[2].widget.answer', 380 - 295)
lv.check_wrongs()
lv.report()
