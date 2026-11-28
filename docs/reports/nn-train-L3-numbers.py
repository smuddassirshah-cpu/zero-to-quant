"""Recompute every number stated in nn-train level 3 (Generalisation in networks) and check each at its JSON path.

Run: <venv>/bin/python docs/reports/nn-train-L3-numbers.py   (NumPy only; about a minute; exits 0 when every check passes)
     ZQ_NUMBERS_STRICT=1 makes an on-screen number that no check compared fail the run (the AI strand's rule).

Route A: the shipped modules, autograd.py (frozen v1.0), nt_ops_l1.py (adam_step) and nt_ops_l3.py, as the lessons use them.
Route B: this script's own NumPy: the 1-64-64-1 net with a hand-written backward pass (dropout masks drawn the same way),
closed forms for ridge and the minimum-norm fit beside lstsq and descent, central differences for the dropout op.
Every code widget is run in CPython with the page's judge (ENGINE-BACKLOG 1263).
"""
import hashlib
import math
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
APP = os.path.join(ROOT, 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, _stated, _text_strings  # noqa: E402

sys.path.insert(0, DATA)
from autograd import Tensor, grad_check  # noqa: E402
from nt_ops_l1 import adam_step  # noqa: E402
import nt_ops_l3 as B3  # noqa: E402

lv = Level('nn-train', 3)
E = lv.expect
_STATED = []
_strs = []
for _fid, _doc in lv.files.items():
    _text_strings(_doc, '', _fid, _strs)
for _fid, _path, _text in _strs:
    for _v, _tol, _pct, _shown, _strong in _stated(_text):
        _STATED.append((abs(_v), _tol, _pct))
NCOV = {'matched': 0, 'unstated': 0}


def is_stated(x):
    """True when a figure on screen equals x to its stated precision (the comparison coverage makes by value)"""
    a = abs(float(x))
    return any(abs(a - t) <= tol for v, tol, pct in _STATED for t in ((v, v / 100) if pct else (v,)))


def cov(*vals):
    """Computed values, recomputed in this script: each one is compared with the figures the level states, at their stated precision.
    A value that matches covers them; a value no figure matches covers nothing (it is simply not stated)."""
    for x in vals:
        if is_stated(x):
            lv._cover(float(x))
            NCOV['matched'] += 1
        else:
            NCOV['unstated'] += 1


def agree(label, a, b, rel=1e-9):
    ok = abs(a - b) <= rel * max(1e-12, abs(a), abs(b))
    lv.claim(ok, f'{label}: routes agree ({a!r}, {b!r})')
    return b


lv.claim(hashlib.sha256(open(os.path.join(DATA, 'autograd.py'), 'rb').read()).hexdigest().startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'nt_ops_l1.py'), 'rb').read()).hexdigest() == '9c1391a33624604bf8547607a51ef08c39a9bee2eeef22947aa5126dbc4ff234', 'nt_ops_l1.py unchanged since level 1')
lv.claim(hashlib.sha256(open(os.path.join(DATA, 'nt_ops_l2.py'), 'rb').read()).hexdigest() == '5712fe43db9bb5060f27dbc076b6d2fdddcbf9a582bf908c69c21e38d2a50c42', 'nt_ops_l2.py unchanged since level 2')
OPS3 = open(os.path.join(DATA, 'nt_ops_l3.py'), 'rb').read()
print('nt_ops_l3.py SHA-256', hashlib.sha256(OPS3).hexdigest(), len(OPS3), 'bytes')
shipped = []


def walk(node):
    if isinstance(node, dict):
        for key in ('data', 'files'):
            if isinstance(node.get(key), dict):
                for k, v in node[key].items():
                    if k.endswith('.py'):
                        shipped.append((key, k, v))
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


for doc in lv.files.values():
    walk(doc)
lv.claim(all(key == 'data' and v == f'content/data/ai/{k}' for key, k, v in shipped) and len(shipped) >= 3, f'every shipped module ({len(shipped)}) is sent by path')

# ---------------- the dropout op: gradient with the mask held fixed ----------------
g = np.random.default_rng(3)
Xo, Ro = g.standard_normal((5, 4)), g.standard_normal((5, 4))
rngA = np.random.default_rng(9)
xo = Tensor(Xo.copy())
out, mask = B3.dropout(xo, 0.3, rng=rngA)
(out * Tensor(Ro)).sum().backward()
num = np.zeros_like(Xo)
for i in np.ndindex(Xo.shape):
    a, b = Xo.copy(), Xo.copy()
    a[i] += 1e-6
    b[i] -= 1e-6
    num[i] = (((a * mask) - (b * mask)) * Ro).sum() / 2e-6
err = float(np.abs(num - xo.grad).max() / np.abs(num).max())
lv.claim(err < 1e-6, f'dropout op: backward with the mask fixed against central differences, relative error {err:.1e}')
lv.claim(set(np.unique(mask)) <= {0.0, 1 / 0.7}, 'dropout mask holds 0 and 1/(1 - p)')
big = B3.dropout(Tensor(np.full(400000, 3.0)), 0.4, rng=np.random.default_rng(1))[0].data
lv.claim(abs(big.mean() - 3) < 0.02 and abs((big == 0).mean() - 0.4) < 0.005, 'dropout keeps the mean and drops a share p (400,000 draws)')
lv.claim(B3.dropout(Tensor(np.ones(3)), 0.5, mode='eval')[1] is None, 'dropout eval mode changes nothing')
lv.claim(B3.early_stop([0.3, 0.2, 0.2, 0.25, 0.26], 2) == (3, 1) and B3.early_stop([0.5, 0.4, 0.3], 2) == (2, 2), 'early_stop: ties and a list that never stops')
lv.claim(abs(B3.decayed_sgd_step(2.0, 0.5, 0.1, 0.01) - 1.948) < 1e-12, 'decayed_sgd_step')
aw = B3.adamw_step([np.array(1.0)], [np.array(0.2)], [np.array(0.0)], [np.array(0.0)], 1, 0.01, 0.1)[0][0]
lv.claim(abs(float(aw) - 0.989) < 1e-9, 'adamw_step at step 1')

# ---------------- route B: the 1-64-64-1 net by hand ----------------
gd0 = np.random.default_rng(0)
xt = np.sort(gd0.uniform(-1, 1, 30))
yt = np.sin(3 * xt) + 0.3 * gd0.standard_normal(30)
xv = gd0.uniform(-1, 1, 200)
yv = np.sin(3 * xv) + 0.3 * gd0.standard_normal(200)
Xt, Yt, Xv, Yv = xt[:, None], yt[:, None], xv[:, None], yv[:, None]


def init_b(seed=0):
    gg = np.random.default_rng(seed)
    P = []
    for a, b in zip((1, 64, 64), (64, 64, 1)):
        P += [gg.standard_normal((a, b)) / math.sqrt(a), np.zeros(b)]
    return P


def fwd_b(P, X):
    h = np.tanh(X @ P[0] + P[1])
    h = np.tanh(h @ P[2] + P[3])
    return h @ P[4] + P[5]


def mse_b(P, X, Y):
    return float(np.mean((fwd_b(P, X) - Y) ** 2))


def train_b(lam=0.0, p=0.0, steps=2000, lr=0.01, every=0, seed=0):
    P = init_b(seed)
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(seed + 100)
    hist = []
    n = len(Xt)
    for t in range(steps):
        z1 = Xt @ P[0] + P[1]
        h1 = np.tanh(z1)
        m1 = (rng.random(h1.shape) >= p) / (1 - p) if p > 0 else 1.0
        a1 = h1 * m1
        z2 = a1 @ P[2] + P[3]
        h2 = np.tanh(z2)
        m2 = (rng.random(h2.shape) >= p) / (1 - p) if p > 0 else 1.0
        a2 = h2 * m2
        out = a2 @ P[4] + P[5]
        d = 2 * (out - Yt) / n
        G = [None] * 6
        G[4], G[5] = a2.T @ d + lam * P[4], d.sum(0)
        dz2 = (d @ P[4].T) * m2 * (1 - h2 ** 2)
        G[2], G[3] = a1.T @ dz2 + lam * P[2], dz2.sum(0)
        dz1 = (dz2 @ P[2].T) * m1 * (1 - h1 ** 2)
        G[0], G[1] = Xt.T @ dz1 + lam * P[0], dz1.sum(0)
        m = [0.9 * a + 0.1 * q for a, q in zip(m, G)]
        v = [0.999 * a + 0.001 * q * q for a, q in zip(v, G)]
        P = [q - lr * (a / (1 - 0.9 ** (t + 1))) / (np.sqrt(b / (1 - 0.999 ** (t + 1))) + 1e-8) for q, a, b in zip(P, m, v)]
        if every and (t + 1) % every == 0:
            hist.append((t + 1, mse_b(P, Xt, Yt), mse_b(P, Xv, Yv)))
    return P, hist


def train_a(lam=0.0, p=0.0, steps=2000, lr=0.01, seed=0, every=0, hist=None):
    """route A: autograd, the shipped dropout op and adam_step; with every > 0, hist gets (step, train error, validation error)"""
    P = init_b(seed)
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(seed + 100)
    for t in range(steps):
        ts = [Tensor(q) for q in P]
        h = Tensor(Xt)
        for i in range(3):
            h = h @ ts[2 * i] + ts[2 * i + 1]
            if i < 2:
                h = h.tanh()
                if p > 0:
                    h, _ = B3.dropout(h, p, rng=rng)
        loss = ((h - Tensor(Yt)) ** 2).mean()
        for i in (0, 2, 4):
            loss = loss + 0.5 * lam * (ts[i] ** 2).sum()
        loss.backward()
        P, m, v = adam_step(P, [q.grad for q in ts], m, v, t + 1, lr)
        if every and (t + 1) % every == 0:
            hist.append((t + 1, mse_b(P, Xt, Yt), mse_b(P, Xv, Yv)))
    return P


# 2,000 full-batch Adam steps on a net that can memorise 30 points amplify rounding: the final validation error depends on
# the BLAS thread count (lambda 0.01 gives 0.1041 to 0.1048, lambda 0.03 gives 0.1134 to 0.1143, lambda 0 differs in the third place).
# So the long runs are single-route results (route A) shown to 2 places, and the routes are compared on a 50-step run, where they
# agree to 1e-9. The lessons state only what holds under both thread settings.
LAMS = [0, 1e-4, 1e-3, 1e-2, 3e-2, 1e-1]
WD, WDB = {}, {}
for lam in LAMS:
    PA = train_a(lam=lam)
    PB, _ = train_b(lam=lam)
    WD[lam] = (mse_b(PA, Xt, Yt), mse_b(PA, Xv, Yv))
    WDB[lam] = (mse_b(PB, Xt, Yt), mse_b(PB, Xv, Yv))
    PA50 = train_a(lam=lam, steps=50)
    PB50, _ = train_b(lam=lam, steps=50)
    agree(f'weight decay {lam}: validation error after 50 steps, autograd against the hand backward', mse_b(PA50, Xv, Yv), mse_b(PB50, Xv, Yv), 1e-9)
    E('l9-weight-decay', f'screens[3].canvas.state.values.l{str(lam).replace(".", "")}', round(WD[lam][1], 2))
cov(*WD[lam])
lv.claim(min(WD, key=lambda k: WD[k][1]) == 0.01, 'weight decay 0.01 gives the lowest validation error of the six (route A)')
lv.claim(WD[0][1] > WD[1e-3][1] and WD[0.1][1] > WD[0.03][1] > WD[0.01][1], 'validation error against lambda is a U')
lv.claim(round(WD[0.01][1], 2) < round(WD[1e-3][1], 2), 'at 2 places weight decay 0.01 reads below 0.001')
var_yv = float(Yv.var())
cov(var_yv)
P1 = train_a(lam=1.0)
v1 = mse_b(P1, Xv, Yv)
cov(v1)
lv.claim(float(np.ptp(fwd_b(P1, np.linspace(-1, 1, 81)[:, None]))) < 1e-6, 'at lambda 1 the net predicts one constant')
lv.claim(abs(v1 - (var_yv + (Yv.mean() - Yt.mean()) ** 2)) < 0.01, 'a constant at the training mean scores the variance plus the squared gap of the means')
E('l9-weight-decay', 'screens[1].widget.answer', 1 - 0.1 * 0.01)
cov(0.999 ** 1000)
E('l9-weight-decay', 'screens[2].widget.answer', round(0.999 * 2 - 0.1 * 0.5, 3))
cov(2 - 0.1 * 0.51, 0.999 * 2 + 0.05)
E('l9-weight-decay', 'screens[3].widget.answer', 0.01)
E('l9-weight-decay', 'screens[4].widget.answer', round(1 - 0.01 * (1 + 0.1 * 1), 3))
cov(1 - 0.01 * 0.3)
E('l9-weight-decay', 'screens[7].widget.answer', round(0.9999 ** 1000, 4))
cov(math.exp(-0.1), 1 - 1000 * 0.0001, 0.99 ** 1000)
E('l9-weight-decay', 'quiz[0].widget.answer', round(1 - 0.05 * 0.002, 4))
# early stopping
_, ES = train_b(lam=0, steps=3000, every=10)
best = min(ES, key=lambda r: r[2])
# route A, recomputed here (not read back from the lesson's series): the 3,000-step run of l10
HA = []
train_a(lam=0, steps=3000, every=10, hist=HA)
bestA = min(HA, key=lambda r: r[2])
F10 = lv._file('l10-early-stopping')[1]
shown_v = F10['screens'][0]['canvas']['params']['series'][1]['values']
shown_t = F10['screens'][0]['canvas']['params']['series'][0]['values']
lv.claim(abs(bestA[0] - best[0]) <= 50, f'best step: route A {bestA[0]}, route B {best[0]} (within 50)')
agree('best validation error, route A against route B (0.5%)', bestA[2], best[2], 0.005)
agree('final validation error, route A against route B (1%)', HA[-1][2], ES[-1][2], 0.01)
lv.claim(bestA[0] == 660 and round(bestA[2], 4) == 0.1029 and round(bestA[1], 4) == 0.0528, f'best step 660 with validation 0.1029 and training 0.0528 (route A: {bestA[0]}, {bestA[2]:.4f}, {bestA[1]:.4f})')
# the 3,000-step end depends on the BLAS thread count in the third place (validation 0.16667 to 0.16677, training 0.01052 to 0.01058): stated to 3 places
E('l10-early-stopping', 'screens[0].widget.answer', bestA[0])
E('l10-early-stopping', 'screens[0].feedback.correct', round(bestA[2], 4))
E('l10-early-stopping', 'screens[0].feedback.correct', round(bestA[1], 4))
E('l10-early-stopping', 'screens[0].feedback.correct', round(HA[-1][2], 3))
E('l10-early-stopping', 'screens[0].feedback.correct', round(HA[-1][1], 3))
E('l10-early-stopping', 'summary.ideas[0]', round(HA[-1][2], 3))
lv.claim(round(ES[-1][2], 2) == round(HA[-1][2], 2) and round(ES[-1][1], 3) == round(HA[-1][1], 3), f'route B ends at the same figures to the places stated ({ES[-1][2]:.4f}, {ES[-1][1]:.5f} against {HA[-1][2]:.5f}, {HA[-1][1]:.5f})')
lv.claim(abs((int(np.argmin(shown_v)) + 1) * 10 - bestA[0]) <= 50, 'the chart marks the best step within 50 of the recomputed one (it is one run)')
cov(bestA[2], bestA[1], round(HA[-1][2], 3), round(HA[-1][1], 3), HA[-1][0])
E('l10-early-stopping', 'screens[1].widget.answer', 1 / (0.01 * 400))
VL = [0.31, 0.24, 0.20, 0.19, 0.195, 0.21, 0.205, 0.23, 0.25]
st, bi = B3.early_stop(VL, 3)
E('l10-early-stopping', 'screens[2].widget.answer', st)
cov(*VL, 100 * (st - bi))
E('l10-early-stopping', 'screens[3].widget.answer', B3.early_stop([0.30, 0.22, 0.23, 0.24, 0.20, 0.18, 0.19, 0.21], 2)[0])
gq = np.random.default_rng(21)
Xp = gq.standard_normal((50, 2)) @ np.array([[1.0, 0.0], [0.8, 0.6]])
yp = Xp @ np.array([1.0, -0.5]) + 0.3 * gq.standard_normal(50)
w = np.zeros(2)
for _ in range(40):
    w = w - 0.1 * Xp.T @ (Xp @ w - yp) / 50
r40 = np.linalg.solve(Xp.T @ Xp / 50 + 0.25 * np.eye(2), Xp.T @ yp / 50)
cov(*w.tolist(), *r40.tolist())
lv.claim(np.linalg.norm(w - r40) / np.linalg.norm(r40) < 0.25, 'step 40 lies within 25% of ridge at 0.25')
E('l10-early-stopping', 'quiz[0].widget.answer', B3.early_stop([0.40, 0.31, 0.28, 0.29, 0.30, 0.27, 0.33, 0.34, 0.35], 3)[1])
E('l10-early-stopping', 'quiz[1].widget.answer', 1 / (0.05 * 200))
# dropout
DP, DPB = {}, {}
for p in (0.0, 0.1, 0.2, 0.3, 0.5):
    DP[p] = mse_b(train_a(p=p), Xv, Yv)
    PB, _ = train_b(p=p)
    DPB[p] = mse_b(PB, Xv, Yv)
    agree(f'dropout {p}: validation error after 50 steps, autograd against the hand backward', mse_b(train_a(p=p, steps=50), Xv, Yv), mse_b(train_b(p=p, steps=50)[0], Xv, Yv), 1e-9)
    E('l11-dropout', f'screens[3].canvas.state.values.p{str(p).replace(".", "")}', round(DP[p], 3))
cov(DP[p])
lv.claim(min(DP, key=DP.get) == 0.2, 'the lowest validation error is at p = 0.2 (route A)')
E('l11-dropout', 'screens[0].widget.answer', 0.2)
E('l11-dropout', 'screens[1].widget.answer', 1 / (1 - 0.2))
cov(1 / 0.2)
E('l11-dropout', 'screens[2].widget.answer', round(8 / 0.75, 3))
cov(2 / 0.75, 6 / 0.75, 4 / 3, 8 * 0.75, 8 / 0.25)
E('l11-dropout', 'screens[3].widget.answer', 0.6 * 3 / 0.6)
cov(3 / 0.6)
P02 = train_a(p=0.2)


def mc_b(P, x, p, draws, seed):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(draws):
        h = np.array([[x]])
        for i in range(3):
            h = h @ P[2 * i] + P[2 * i + 1]
            if i < 2:
                h = np.tanh(h) * (rng.random((1, 64)) >= p) / (1 - p)
        out.append(float(h[0, 0]))
    return float(np.std(out))


mc05, mc15 = mc_b(P02, 0.5, 0.2, 500, 1), mc_b(P02, 1.5, 0.2, 500, 1)
cov(mc05, mc15)
lv.claim(mc15 / mc05 < 1.2, 'the Monte Carlo spread barely grows outside the data')
E('l11-dropout', 'quiz[0].widget.answer', round(1 / 0.7, 4))
E('l11-dropout', 'quiz[1].widget.answer', 0.5 ** 2)
cov(1 / 0.3)
# double descent
PS = [5, 10, 15, 20, 25, 30, 35, 38, 40, 42, 45, 50, 60, 70, 80, 100, 120, 150, 200]


def dd_b(ps, n, noise, seed, lam=0.0, d=10):
    gg = np.random.default_rng(seed)
    beta = gg.standard_normal(d)
    beta /= np.linalg.norm(beta)
    Xa = gg.standard_normal((n, d))
    ya = Xa @ beta + noise * gg.standard_normal(n)
    Xs = gg.standard_normal((2000, d))
    ys = Xs @ beta
    out = []
    for p in ps:
        W = np.random.default_rng(seed + 1000).standard_normal((d, p)) / np.sqrt(d)
        F = np.maximum(np.vstack([Xa, Xs]) @ W, 0)
        Fa, Fs = F[:n], F[n:]
        if lam:
            wv = np.linalg.solve(Fa.T @ Fa + lam * np.eye(p), Fa.T @ ya)
        else:
            wv = np.linalg.lstsq(Fa, ya, rcond=None)[0]
        out.append(float(np.mean((Fs @ wv - ys) ** 2)))
    return out


DD = {s: dd_b(PS, 40, 0.5, s) for s in range(5)}
DDR = dd_b(PS, 40, 0.5, 0, lam=0.1)
i40, i10, i200 = PS.index(40), PS.index(10), PS.index(200)
for s in range(5):
    lv.claim(DD[s][i40] > DD[s][i10] and DD[s][i40] > DD[s][i200], f'double descent, seed {s}: error at p = 40 above p = 10 and p = 200 ({DD[s][i10]:.3f}, {DD[s][i40]:.3f}, {DD[s][i200]:.3f})')
F12 = lv._file('l12-double-descent')[1]
shown = F12['screens'][0]['canvas']['params']['series'][0]['values']
lv.claim(all(abs(a - round(b, 4)) <= max(2e-4, 1e-6 * abs(b)) for a, b in zip(shown, DD[0])), 'the minimum-norm curve (pinv, route A) matches lstsq (route B)')
cov(DD[0][i10], DD[0][i40], DD[0][i200], DDR[i40])
E('l12-double-descent', 'screens[2].widget.answer', round(DDR[i40], 3))
cov(DDR[-1], DD[0][i40])
lv.claim(max(DDR) < 2, 'with ridge 0.1 the curve stays below 2')
E('l12-double-descent', 'screens[1].widget.answer', 1)
cov(math.sqrt(2))
gc = np.random.default_rng(0)
_b = gc.standard_normal(10)
Xa0 = gc.standard_normal((40, 10))
_ = gc.standard_normal(40)
Xs0 = gc.standard_normal((2000, 10))
conds = []
for p in (10, 30, 40, 50, 200):
    W = np.random.default_rng(1000).standard_normal((10, p)) / np.sqrt(10)
    sv = np.linalg.svd(np.maximum(np.vstack([Xa0, Xs0]) @ W, 0)[:40], compute_uv=False)
    conds.append(float(sv.max() / sv.min()))
cov(*[round(c) for c in conds])
lv.claim(max(range(5), key=lambda i: conds[i]) == 2, 'the condition number peaks at p = 40')
E('l12-double-descent', 'screens[3].widget.answer', 40)
E('l12-double-descent', 'quiz[0].widget.answer', 60)
E('l12-double-descent', 'quiz[2].widget.answer', 5)
cov(9 + 16)
lv.literal('2,000', why='the test-set size of the double-descent runs, a stated choice')
lv.literal('10,000', why='the transfer scenario\'s weight count')
# review, problems, homework
E('review', 'items[0].widget.answer', 1 - 0.2 * 0.005)
E('review', 'items[1].widget.answer', B3.early_stop([0.62, 0.51, 0.46, 0.44, 0.45, 0.43, 0.46, 0.47, 0.48, 0.50], 3)[0])
E('review', 'items[2].widget.answer', 1 / 0.4)
E('review', 'items[4].widget.answer', round(2 - 0.001 * (-1 + 0.01 * 2), 5))
cov(2 - 0.001 * 1.02)
E('review', 'items[5].widget.answer', 1 / (0.02 * 250))
E('problems', 'items[0].parts[0].widget.answer', 1 - 0.2 * 0.1)
E('problems', 'items[0].parts[1].widget.answer', round(0.98 ** 3, 6))
E('problems', 'items[0].parts[2].widget.answer', round(3 / 2.1, 4))
E('problems', 'items[0].parts[3].widget.answer', round(6 / 2.1, 4))
cov(0.98 ** 2)
wr = np.linalg.solve(np.array([[2.0 + 0.1]]), np.array([3.0]))[0]
agree('ridge weight: closed form against a solve', 3 / 2.1, float(wr), 1e-12)
E('problems', 'items[1].parts[0].widget.answer', 5 / 0.8)
E('problems', 'items[2].parts[1].widget.answer', round(math.sqrt(20), 4))
wmn = np.linalg.pinv(np.array([[2.0, 1.0]])) @ np.array([10.0])
lv.claim(np.allclose(wmn, [4, 2]), 'minimum norm of 2w1 + w2 = 10 is (4, 2)')
cov(10 / 5)
E('problems', 'items[2].parts[2].widget.answer', 45 - 30)
E('homework', 'items[3].widget.answer', round((4 - 0.01) - (4 - 0.01 * (1 + 0.05 * 4)), 3))
for lit in ('1,000', '3,000', '5,000', '2 million', '1 million', '10^-8', '10^-9', '10^-6', '10^-7', '200,000', '400', '0.005', '250'):
    lv.literal(lit, why='a stated size, step count, setting or test tolerance')
# ---------------- code widgets: solution, starter, mutants ----------------


def judge(a, e, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def nan(x):
        try:
            return bool(x != x)
        except Exception:
            return False

    def close(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) or isinstance(y, dict):  # as the page's judge: same keys, then each value within tolerance
            return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(close(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
        if nan(x) and nan(y):
            return True
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y

    def same(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
        return (nan(x) and nan(y)) or bool(x == y)
    return close(a, e) if cmp == 'isclose' else same(a, e)


def first_fail(w, src):
    cwd, d = os.getcwd(), tempfile.mkdtemp()
    os.chdir(d)
    try:
        for k, v in (w.get('data') or {}).items():
            shutil.copy(os.path.join(APP, v), os.path.join(d, k))
        sys.path.insert(0, d)
        for mod in [m for m in sys.modules if m == 'autograd' or m.startswith('nt_ops')]:
            sys.modules.pop(mod)
        ns = {'__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns)
                    got = eval(c['call'], ns)
                if c.get('compare') == 'raises':
                    return i + 1
                t = c.get('tol')
                ok = judge(got, eval(c['expect'], ns), c.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
            except Exception as e:  # noqa
                ok = c.get('compare') == 'raises' and type(e).__name__ == c.get('expect')
            if not ok:
                return i + 1
        return 0
    finally:
        os.chdir(cwd)
        sys.path.remove(d)
        shutil.rmtree(d, ignore_errors=True)
        for mod in [m for m in sys.modules if m == 'autograd' or m.startswith('nt_ops')]:
            sys.modules.pop(mod)
        sys.path.insert(0, DATA)


nw = nm = 0
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
        for mu in w.get('mutants', []):
            nm += 1
            got = first_fail(w, mu['source'])
            lv.claim(got == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')

# figures worked by hand in the text, recomputed from their definitions (the settings below are the only literals)
cov(0.999 * 2, 0.1 * (0.5 + 0.01 * 2), 0.3 ** 2, 0.001 * 0.01 * 2, 4 - 0.01, 4 - 0.01 * (1 + 0.2), 0.01 * 0.2, 2.0 + 0.1, 3 ** 2, 4 ** 2, 60 - 1)
lv.literal('0.03', why='a lambda of the weight-decay sweep LAMS, a stated setting')
lv.literal('50', why='a feature count of the sweep grid PS, a stated setting')
lv.literal('halved', why='the factor one half in the loss definition, a stated convention')
lv.literal('0.30, 0.22, 0.23, 0.24, 0.20, 0.18, 0.19, 0.21', why='the validation curve given in l10 screens[3], the input of the early_stop call above')
lv.literal('0.40, 0.31, 0.28, 0.29, 0.30, 0.27, 0.33, 0.34, 0.35', why='the validation curve given in the l10 quiz, the input of the early_stop call above')
lv.literal('0.62, 0.51, 0.46, 0.44, 0.45, 0.43, 0.46, 0.47, 0.48, 0.50', why='the validation curve given in the review item, the input of the early_stop call above')
lv.claim(NCOV['matched'] > 0, f'recomputed values compared with the figures the level states: {NCOV["matched"]} equal a stated figure at its stated precision, {NCOV["unstated"]} are not stated')
lv.check_wrongs()
lv.report()
