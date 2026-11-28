"""Recompute every number stated in nn-train level 4 (Experiments you can trust) and check each at its JSON path.

Run through the CI runner (from app/): node tools/run-number-scripts.mjs --python <venv>/bin/python --only nn-train-L4
     (it sets one BLAS thread, as CI does). Direct: ZQ_NUMBERS_STRICT=1 <venv>/bin/python docs/reports/nn-train-L4-numbers.py
     --write retrains every shipped run and rewrites app/content/data/ai/nn-train-seeds.json (about 15 s), then checks.

Route A: the shipped modules (autograd.py v1.0, nt_ops_l1 to l3 frozen, nt_ops_l4.py new) and NumPy on the shipped JSON.
Route B: this script's own NumPy net with a hand-written backward (layer norm and dropout included, masks drawn in the same
order), the standard library's statistics module for means and sds, and SciPy for t tests and t quantiles.
The 130 shipped runs are 300-step runs at moderate rates; a 1e-13 change to the start moves their final loss by at most 5e-7
relative (checked while writing), so they are not chaotic and are compared to the file at 1e-6 relative. The routes are
compared exactly (1e-9) on 20-step runs of every configuration. Every figure the lessons state is a statistic of the file.
"""
import copy
import hashlib
import json
import math
import os
import shutil
import statistics as st
import sys
import tempfile
from statistics import NormalDist

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

sys.path.insert(0, DATA)
from autograd import Tensor, cross_entropy  # noqa: E402
from nt_ops_l1 import adam_step, loss_and_grads, full_loss  # noqa: E402
import nt_ops_l4 as M4  # noqa: E402

lv = Level('nn-train', 4, coverage='strict')
E = lv.expect


def agree(label, a, b, rel=1e-9, extra=()):
    ok = abs(a - b) <= rel * max(1e-12, abs(a), abs(b))
    lv.claim(ok, f'{label}: routes agree ({a!r}, {b!r})', covers=[a, b, *extra])
    return a


def used(label, ok, *inputs):
    """A recomputed answer that equals its key, covering the given inputs it was computed from."""
    lv.claim(bool(ok), label, covers=list(inputs))


def sha(name):
    return hashlib.sha256(open(os.path.join(DATA, name), 'rb').read()).hexdigest()


lv.claim(sha('autograd.py').startswith('5917d4ec91f7'), 'autograd.py is the frozen v1.0')
lv.claim(sha('nt_ops_l1.py') == '9c1391a33624604bf8547607a51ef08c39a9bee2eeef22947aa5126dbc4ff234', 'nt_ops_l1.py unchanged')
lv.claim(sha('nt_ops_l2.py') == '5712fe43db9bb5060f27dbc076b6d2fdddcbf9a582bf908c69c21e38d2a50c42', 'nt_ops_l2.py unchanged')
lv.claim(sha('nt_ops_l3.py') == '52c79ff41ccd14b5eb6e09a23fbc9399c80116f939b704b778426939ee468c7f', 'nt_ops_l3.py unchanged')
print('nt_ops_l4.py SHA-256', sha('nt_ops_l4.py'), os.path.getsize(os.path.join(DATA, 'nt_ops_l4.py')), 'bytes')
shipped = []


def walk(node):
    if isinstance(node, dict):
        for key in ('data', 'files'):
            if isinstance(node.get(key), dict):
                shipped.extend((key, k, v) for k, v in node[key].items())
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)


for doc in lv.files.values():
    walk(doc)
lv.claim(all(key == 'data' and v == f'content/data/ai/{k}' for key, k, v in shipped) and len(shipped) >= 10, f'every shipped file ({len(shipped)}) is sent by path, byte-identical')

# ---------------- nt_ops_l4: the t distribution against SciPy ----------------
worst = 0.0
for df in (1, 2, 4, 5, 7, 9, 11, 19, 60):
    for x in (-30, -3.6, -2.262, -0.4, 0, 0.7, 2.0, 4.4, 25):
        worst = max(worst, abs(M4.t_cdf(x, df) - stats.t.cdf(x, df)))
    for q in (0.0025, 0.025, 0.5, 0.975, 0.99, 0.995, 0.99875):
        worst = max(worst, abs(M4.t_quantile(q, df) - stats.t.ppf(q, df)) / max(1, abs(stats.t.ppf(q, df))))
lv.claim(worst < 1e-10, f't_cdf and t_quantile against scipy.stats.t: worst error {worst:.1e}')

# ---------------- route B: the net by hand ----------------
X, y, tr, va, te = M4.course_data(0)
Xs, ys = __import__('nt_ops_l1').spirals(600, seed=0, noise=0.05)
lv.claim(np.array_equal(X, Xs) and np.array_equal(np.sort(np.r_[tr, va, te]), np.arange(600)) and len(tr) == 400 and len(va) == 100, 'course_data: 600 spiral points split 400/100/100')


def ce_b(z, t):
    m = z.max(1, keepdims=True)
    e = np.exp(z - m)
    s = e.sum(1, keepdims=True)
    return float(np.mean(np.log(s[:, 0]) + m[:, 0] - z[np.arange(len(t)), t])), e / s


def run_b(cfg, seed, steps, split=0, batch_seed=None):
    Xd, yd, trd, vad, ted = M4.course_data(split)
    ss = [np.random.default_rng(s) for s in np.random.SeedSequence(seed).spawn(3)]
    ri, rb, rd = ss
    if batch_seed is not None:
        rb = [np.random.default_rng(s) for s in np.random.SeedSequence(batch_seed).spawn(3)][1]
    H, ln, p = cfg.get('hidden', 16), bool(cfg.get('ln')), cfg.get('p', 0.0)
    P = []
    for a, b in ((2, H), (H, H), (H, 2)):
        P += [ri.standard_normal((a, b)) / math.sqrt(a), np.zeros(b)]
    if ln:
        P += [np.ones(H), np.zeros(H), np.ones(H), np.zeros(H)]
    mo = [np.zeros_like(q) for q in P]
    ve = [np.zeros_like(q) for q in P]

    def fwd(Xb, rng):
        cache, h = [], Xb
        for i in range(2):
            z = h @ P[2 * i] + P[2 * i + 1]
            if ln:
                mu = z.mean(1, keepdims=True)
                inv = 1 / np.sqrt(((z - mu) ** 2).mean(1, keepdims=True) + 1e-5)
                xh = (z - mu) * inv
                a = P[6 + 2 * i] * xh + P[7 + 2 * i]
            else:
                inv = xh = None
                a = z
            hh = np.tanh(a)
            mk = (rng.random(hh.shape) >= p) / (1 - p) if (p > 0 and rng is not None) else np.ones_like(hh)
            cache.append((h, inv, xh, hh, mk))
            h = hh * mk
        return h @ P[4] + P[5], cache, h

    def loss(Xb, yb):
        return ce_b(fwd(Xb, None)[0], yb)[0]

    for t in range(1, steps + 1):
        rows = trd[rb.choice(400, 32, replace=False)]
        out, cache, h2 = fwd(Xd[rows], rd)
        _, pr = ce_b(out, yd[rows])
        g = pr.copy()
        g[np.arange(32), yd[rows]] -= 1
        g /= 32
        G = [None] * len(P)
        G[4], G[5] = h2.T @ g, g.sum(0)
        up = g @ P[4].T
        for i in (1, 0):
            hin, inv, xh, hh, mk = cache[i]
            da = up * mk * (1 - hh ** 2)
            if ln:
                G[6 + 2 * i], G[7 + 2 * i] = (da * xh).sum(0), da.sum(0)
                dx = da * P[6 + 2 * i]
                dz = inv / H * (H * dx - dx.sum(1, keepdims=True) - xh * (dx * xh).sum(1, keepdims=True))
            else:
                dz = da
            G[2 * i], G[2 * i + 1] = hin.T @ dz, dz.sum(0)
            up = dz @ P[2 * i].T
        if cfg['opt'] == 'adam':
            mo = [0.9 * a + 0.1 * q for a, q in zip(mo, G)]
            ve = [0.999 * a + 0.001 * q * q for a, q in zip(ve, G)]
            P = [w - cfg['lr'] * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for w, a, b in zip(P, mo, ve)]
        else:
            P = [w - cfg['lr'] * q for w, q in zip(P, G)]
    return loss(Xd[vad], yd[vad]), loss(Xd[ted], yd[ted])


SEEDS_PATH = os.path.join(DATA, 'nn-train-seeds.json')
CONFIGS = {'A': dict(opt='adam', lr=0.01, ln=False, p=0.0, hidden=16), 'B': dict(opt='adam', lr=0.015, ln=False, p=0.0, hidden=16),
           'B-reshuffled': dict(opt='adam', lr=0.015, ln=False, p=0.0, hidden=16), 'narrow': dict(opt='adam', lr=0.03, ln=False, p=0.0, hidden=6)}
for opt, lr in (('sgd', 0.5), ('adam', 0.02)):
    for ln in (False, True):
        for p in (0.0, 0.1):
            CONFIGS[opt + ('+ln' if ln else '') + ('+do' if p else '')] = dict(opt=opt, lr=lr, ln=ln, p=p, hidden=16)
PLAN = [(n, s, 0, s + 100 if n == 'B-reshuffled' else None) for n in CONFIGS for s in range(10)] + [('A', 0, sp, None) for sp in range(1, 10)]

for name, cfg in CONFIGS.items():
    bs = 103 if name == 'B-reshuffled' else None
    ra = M4.train_run(cfg, 3, steps=20, batch_seed=bs)
    rbv, rbt = run_b(cfg, 3, 20, batch_seed=bs)
    ok = abs(ra['val'] - rbv) <= 1e-9 * rbv and abs(ra['test'] - rbt) <= 1e-9 * rbt
    lv.claim(ok, f'{name}: 20-step run, train_run against the hand backward ({ra["val"]:.12f}, {rbv:.12f})')

if '--write' in sys.argv:
    runs = []
    for name, s, sp, bs in PLAN:
        r = M4.train_run(CONFIGS[name], s, split_seed=sp, batch_seed=bs)
        row = {'config': name, 'seed': s, 'split_seed': sp}
        if bs is not None:
            row['batch_seed'] = bs
        row.update(val=r['val'], test=r['test'], train=r['train'], val_curve=[round(x, 4) for x in r['val_curve']], train_curve=[round(x, 4) for x in r['train_curve']])
        runs.append(row)
    doc = {'about': 'nn-train level 4: final losses (nats) of the 2-16-16-2 tanh spiral net, 300 steps, batch 32, from docs/reports/nn-train-L4-numbers.py --write. Curves hold the validation and training loss every 6 steps.',
           'data': 'spirals(600, seed=0, noise=0.05) from nt_ops_l1, rows split 400/100/100 by default_rng(split_seed).permutation(600)',
           'seeds': 'seed_streams(seed) in nt_ops_l4: init, batch and dropout generators from SeedSequence(seed).spawn(3)',
           'configs': CONFIGS, 'runs': runs}
    open(SEEDS_PATH, 'w').write(json.dumps(doc, separators=(',', ':')))
SEEDS = json.load(open(SEEDS_PATH))
lv.claim(os.path.getsize(SEEDS_PATH) < 262144, f'nn-train-seeds.json is {os.path.getsize(SEEDS_PATH)} bytes, under 256 KB')
lv.claim(SEEDS['configs'] == CONFIGS and [(r['config'], r['seed'], r['split_seed'], r.get('batch_seed')) for r in SEEDS['runs']] == PLAN, 'the file holds the planned 130 runs and configurations')
worst_r = worst_c = 0.0
for (name, s, sp, bs), row in zip(PLAN, SEEDS['runs']):
    r = M4.train_run(CONFIGS[name], s, split_seed=sp, batch_seed=bs)
    for k in ('val', 'test', 'train'):
        worst_r = max(worst_r, abs(r[k] - row[k]) / row[k])
    for k in ('val_curve', 'train_curve'):
        worst_c = max(worst_c, max(abs(a - b) for a, b in zip(r[k], row[k])))
lv.claim(worst_r < 1e-6 and worst_c < 1.0001e-4, f'retraining all 130 runs reproduces the file (final losses to {worst_r:.1e} relative, curves to {worst_c:.1e})')


def V(config, key='val', split=0):
    rs = sorted([r for r in SEEDS['runs'] if r['config'] == config and r['split_seed'] == split], key=lambda r: r['seed'])
    return [r[key] for r in rs]


SPL = [r['val'] for r in sorted([r for r in SEEDS['runs'] if r['config'] == 'A' and r['seed'] == 0], key=lambda r: r['split_seed'])]


def mean2(label, xs):
    return agree(f'{label} mean', float(np.mean(xs)), st.fmean(xs))


def sd2(label, xs):
    return agree(f'{label} sd', float(np.std(xs, ddof=1)), st.stdev(xs))


cfg_lits = [0.01, 0.015, 0.03, 0.02, 0.5, 0.1]
lv.claim(CONFIGS['A']['lr'] == 0.01 and CONFIGS['B']['lr'] == 0.015 and CONFIGS['narrow']['lr'] == 0.03 and CONFIGS['adam']['lr'] == 0.02 and CONFIGS['sgd']['lr'] == 0.5 and CONFIGS['adam+do']['p'] == 0.1,
         'the rates and dropout the lessons name are the file\'s configurations', covers=cfg_lits)

# ---------------- l13 ----------------
L13 = 'l13-one-seed-one-draw'
A = V('A')
mA, sA = mean2('A', A), sd2('A', A)
lo, hi = min(A), max(A)
agree('A lowest (seed 2)', lo, A[2])
agree('A highest (seed 7)', hi, A[7])
line = round(A[0] - 0.02, 3)
lv.claim([i for i in range(10) if A[i] < line] == [2, 5] and line == 0.073, 'two seeds (2 and 5) score below 0.073', covers=[line, A[0], 0.02, A[2], A[5], A[8]])
E(L13, 'screens[0].widget.answer[0]', 's2')
E(L13, 'screens[1].widget.answer', round(hi - lo, 3))
agree('range', hi - lo, float(np.ptp(A)))
lv.claim(round(hi - lo, 3) / 0.02 > 6.5, 'the range is almost seven times 0.02', covers=[0.02])
five = [round(x, 3) for x in A[:5]]
m5, s5 = mean2('five seeds', five), sd2('five seeds', five)
E(L13, 'screens[2].widget.rows[0][1].answer', round(m5, 4))
E(L13, 'screens[2].widget.rows[1][1].answer', round(s5, 4))
agree('five seeds sd over n', float(np.std(five)), st.pstdev(five))
ss5 = agree('five seeds squared deviations', sum((x - m5) ** 2 for x in five), 4 * st.variance(five), extra=[sum(five), st.variance(five)])
sS = sd2('split seeds', SPL)
mean2('split seeds', SPL)
med = agree('A median', float(np.median(A)), st.median(A))
NAR = V('narrow')
good8 = [x for x in NAR if x < 0.3]
lv.claim(len(good8) == 8 and [i for i in range(10) if NAR[i] > 0.3] == [4, 9] and min(x for x in NAR if x > 0.3) > 0.41 and max(good8) < 0.19, 'narrow net: seeds 4 and 9 stall above 0.41, the other eight end below 0.19', covers=[0.42, 0.2])
m8 = mean2('narrow, eight that learned', good8)
mean2('narrow, all ten', NAR)
agree('narrow, eight sum', sum(good8), st.fsum(good8))
E(L13, 'screens[6].widget.answer', round(m8, 3))
se10 = agree('A standard error', sA / math.sqrt(10), st.stdev(A) / 10 ** 0.5)
E(L13, 'screens[9].widget.answer', round(se10, 4))
d2 = agree('transfer: sd of a difference of two runs', math.sqrt(2) * 0.006, math.hypot(0.006, 0.006))
E(L13, 'screens[10].widget.answer', round(d2, 4))
used('transfer: 0.5% of 0.400 is 0.002', abs(0.400 * 0.005 - 0.002) < 1e-12 and abs(0.400 - 0.398 - 0.002) < 1e-12, 0.400, 0.398, 0.005, 0.002, 0.006, 0.012)
q = [0.30, 0.34, 0.28, 0.36]
qs = sd2('quiz four seeds', q)
agree('quiz four seeds over n', float(np.std(q)), st.pstdev(q))
E(L13, 'quiz[0].widget.answer', round(qs, 3))
used('quiz four seeds: mean 0.32, squares 0.004', abs(st.fmean(q) - 0.32) < 1e-12 and abs(sum((x - 0.32) ** 2 for x in q) - 0.004) < 1e-12 and abs(0.004 / 3 - 0.00133) < 5e-6, *q, 0.32, 0.004, 0.00133, 0.02, 0.04)
used('quiz bimodal: 3 of 10 at 0.69 and 7 at 0.05 average about 0.24', abs((3 * 0.69 + 7 * 0.05) / 10 - 0.242) < 1e-9, 0.69, 0.05, 0.24, 0.3)
E(L13, 'quiz[3].widget.answer', 0.02 / math.sqrt(16))
used('quiz se: 0.02/4', abs(0.02 / 16 - 0.00125) < 1e-12, 0.02, 0.001)

# ---------------- l14 ----------------
L14 = 'l14-ablations'
NAMES = ['sgd', 'sgd+ln', 'sgd+do', 'sgd+ln+do', 'adam', 'adam+ln', 'adam+do', 'adam+ln+do']
VV = {k: V(k) for k in NAMES}
MM = {k: mean2(k, VV[k]) for k in NAMES}
SS = {k: sd2(k, VV[k]) for k in NAMES}
REM = {'adam': 'sgd+ln+do', 'ln': 'adam+do', 'do': 'adam+ln'}
DD = {c: [a - b for a, b in zip(VV[r], VV['adam+ln+do'])] for c, r in REM.items()}
DM = {c: mean2(f'removal {c}', DD[c]) for c in REM}
DS = {c: sd2(f'removal {c}', DD[c]) for c in REM}
for c, r in REM.items():
    agree(f'removal {c}: mean of differences equals difference of means', DM[c], MM[r] - MM['adam+ln+do'])
lv.claim(DM['ln'] > DM['adam'] > 0 > DM['do'], 'layer norm\'s removal costs most, Adam next, and removing dropout helps')
lv.claim(DS['adam'] > DM['adam'], 'Adam\'s effect has an sd larger than its mean')
E(L14, 'screens[1].widget.answer[0]', 'noln')
E(L14, 'screens[2].widget.answer', round(DM['do'], 3))
E(L14, 'screens[3].widget.answer[0]', 'ln')
gA0 = agree('Adam gain without layer norm', MM['sgd'] - MM['adam'], st.fmean(VV['sgd']) - st.fmean(VV['adam']))
gA1 = agree('Adam gain with layer norm', MM['sgd+ln'] - MM['adam+ln'], st.fmean(VV['sgd+ln']) - st.fmean(VV['adam+ln']))
E(L14, 'screens[4].widget.rows[0][1].answer', round(gA0, 3))
E(L14, 'screens[4].widget.rows[1][1].answer', round(gA1, 3))
agree('interaction Adam x layer norm', gA0 - gA1, (MM['adam+ln'] - MM['sgd+ln']) - (MM['adam'] - MM['sgd']))
E(L14, 'screens[5].widget.answer', (3 + 1) * 10)
used('both directions with three changes are all 8 mixes', len({'sgd', 'sgd+ln+do', 'adam+do', 'adam+ln', 'adam+ln+do', 'adam', 'sgd+ln', 'sgd+do'}) == 2 ** 3 and 8 * 10 == 80, 80)
s6 = {c: VV[r][6] - VV['adam+ln+do'][6] for c, r in REM.items()}
agree('seed 6: removing Adam', s6['adam'], DD['adam'][6])
agree('seed 6: removing layer norm', s6['ln'], DD['ln'][6])
lv.claim(s6['adam'] > s6['ln'] and DM['ln'] > DM['adam'] and s6['adam'] / s6['ln'] > 1.9, 'seed 6 alone ranks Adam first, about twice layer norm; ten seeds rank layer norm first',
         covers=[VV[k][6] for k in ('adam+ln+do', 'sgd+ln+do', 'adam+do', 'adam+ln')])
used('edge 2x2: the wider layer adds 0.010 alone, removes 0.050 with dropout, interaction -0.060',
     abs((0.310 - 0.300) - 0.010) < 1e-12 and abs((0.240 - 0.290) + 0.050) < 1e-12, 0.300, 0.310, 0.290, 0.240, 0.010, 0.050)
E(L14, 'screens[7].widget.answer', round(0.240 - 0.290, 3))
used('generalise: an effect of -0.03', True and -0.03 < 0, 0.03)
E(L14, 'screens[10].widget.answer', (6 + 1) * 5)
used('transfer: every mix of six changes is 2^6 x 5 = 320 runs', 2 ** 6 * 5 == 320, 320)
E(L14, 'quiz[0].widget.answer', (4 + 1) * 3)
used('quiz removal table', 0.090 / 0.045 == 2 and 0.090 / 0.005 == 18, 0.040, 0.005, 0.045, 0.090)
E(L14, 'quiz[2].widget.answer', round((0.30 - 0.45) - (0.40 - 0.50), 2))
used('quiz 2x2', abs((0.30 - 0.45) + 0.15) < 1e-12 and abs((0.40 - 0.50) + 0.10) < 1e-12, 0.50, 0.40, 0.45, 0.30, 0.10, 0.15)

# ---------------- l15 ----------------
L15 = 'l15-training-log'
row = {(r['config'], r['seed'], r['split_seed']): r for r in SEEDS['runs']}
a00, a01, b4 = row[('A', 0, 0)]['val'], row[('A', 0, 1)]['val'], row[('B', 4, 0)]['val']
agree('A seed 0 split 0 (log 1)', a00, SPL[0])
agree('A seed 0 split 1 (log 2)', a01, SPL[1])
E(L15, 'screens[2].widget.rows[2][1].answer', 0.015)
E(L15, 'screens[2].widget.rows[3][1].answer', round(b4, 3))
agree('B seed 4', b4, run_b(CONFIGS['B'], 4, 300)[0], 1e-6)
agree('A seed 0 test loss', row[('A', 0, 0)]['test'], run_b(CONFIGS['A'], 0, 300)[1], 1e-6)


def segment(state, t0, t1, brng):
    P, m, v = state
    for t in range(t0 + 1, t1 + 1):
        rows = tr[brng.choice(400, 32, replace=False)]
        ts = [Tensor(q) for q in P]
        loss = cross_entropy(M4.net_logits(ts, X[rows]), y[rows])
        loss.backward()
        P, m, v = adam_step(P, [q.grad for q in ts], m, v, t, 0.01)
    return P, m, v


def vl(P):
    return cross_entropy(M4.net_logits(P, X[va]), y[va]).item()


ri, rbg, _ = M4.seed_streams(0)
P0 = M4.init_params(ri)
half = segment((P0, [np.zeros_like(q) for q in P0], [np.zeros_like(q) for q in P0]), 0, 150, rbg)
r_saved = vl(segment(half, 150, 300, copy.deepcopy(rbg))[0])
r_restart = vl(segment(half, 150, 300, M4.seed_streams(0)[1])[0])
r_adam = vl(segment((half[0], [np.zeros_like(q) for q in half[0]], [np.zeros_like(q) for q in half[0]]), 0, 150, copy.deepcopy(rbg))[0])
agree('resume with every state restored equals the run that never stopped', r_saved, a00, 1e-12)
# route B for the restarted stream: the batches of steps 151 to 300 repeat those of steps 1 to 150
rbB = np.random.default_rng(np.random.SeedSequence(0).spawn(3)[1])
first = [tr[rbB.choice(400, 32, replace=False)] for _ in range(150)]
rbC = M4.seed_streams(0)[1]
lv.claim(all(np.array_equal(first[i], tr[rbC.choice(400, 32, replace=False)]) for i in range(150)), 'a restarted batch stream repeats the first 150 batches')
lv.claim(r_restart > a00 + 0.03 and r_adam > a00 + 0.015, 'the two faulty resumes end well above the uninterrupted run', covers=[r_restart, r_adam, r_restart - a00])
cov_resume = agree('resume: restarted stream (route A twice)', r_restart, vl(segment(half, 150, 300, M4.seed_streams(0)[1])[0]))
agree('resume: Adam reset (route A twice)', r_adam, vl(segment((half[0], [np.zeros_like(q) for q in half[0]], [np.zeros_like(q) for q in half[0]]), 0, 150, copy.deepcopy(rbg))[0]))
Xb, yb = X[tr[:8]], y[tr[:8]]
lv.claim(int(yb.sum()) == 4, 'the batch of 8 holds four points of each class')


def ofb_a(P, steps, lr):
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    for t in range(1, steps + 1):
        _, G = loss_and_grads(P, Xb, yb)
        P, m, v = adam_step(P, G, m, v, t, lr)
    return full_loss(P, Xb, yb)


def ofb_b(P, steps, lr):
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    for t in range(1, steps + 1):
        h1 = np.tanh(Xb @ P[0] + P[1])
        h2 = np.tanh(h1 @ P[2] + P[3])
        _, pr = ce_b(h2 @ P[4] + P[5], yb)
        g = pr.copy()
        g[np.arange(8), yb] -= 1
        g /= 8
        d2 = (g @ P[4].T) * (1 - h2 ** 2)
        d1 = (d2 @ P[2].T) * (1 - h1 ** 2)
        G = [Xb.T @ d1, d1.sum(0), h1.T @ d2, d2.sum(0), h2.T @ g, g.sum(0)]
        m = [0.9 * a + 0.1 * q for a, q in zip(m, G)]
        v = [0.999 * a + 0.001 * q * q for a, q in zip(v, G)]
        P = [w - lr * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for w, a, b in zip(P, m, v)]
    return ce_b(np.tanh(np.tanh(Xb @ P[0] + P[1]) @ P[2] + P[3]) @ P[4] + P[5], yb)[0]


g200 = agree('overfit 200 steps: autograd against the hand backward', ofb_a(M4.init_params(M4.seed_streams(0)[0]), 200, 0.01),
             ofb_b(M4.init_params(M4.seed_streams(0)[0]), 200, 0.01), 1e-7)
z200 = ofb_a([np.zeros_like(q) for q in M4.init_params(M4.seed_streams(0)[0])], 200, 0.01)
agree('zero start stays at ln 2', z200, math.log(2), 1e-12)
lv.claim(g200 < 0.001, f'the random start reaches {g200:.5f} on its 8 points', covers=[g200])
F15 = lv._file(L15)[1]
cg = F15['screens'][5]['canvas']['params']['series'][0]['values']
cz = F15['screens'][5]['canvas']['params']['series'][1]['values']
lv.claim(abs(cg[-1] - round(g200, 4)) < 1e-9 and all(abs(c - round(math.log(2), 4)) < 1e-9 for c in cz), 'the two overfitting curves end at the computed losses')
E(L15, 'screens[5].widget.answer', round(z200, 3))
lv.claim(round(row[('A', 0, 0)]['val_curve'][0], 2) == 0.47 and round(row[('A', 0, 0)]['train_curve'][0], 2) == 0.47 and round(row[('A', 0, 0)]['test'], 3) == 0.043,
         'the sample log shows A seed 0\'s step-6 losses and test loss', covers=[0.47, 0.043])
lv.claim(round(row[('sgd', 2, 0)]['val_curve'][0], 2) == 0.43 and round(row[('sgd', 2, 0)]['train_curve'][0], 2) == 0.46 and round(row[('sgd', 2, 0)]['test'], 2) == 0.10,
         'the audited log (SGD at 0.5, seed 2) shows its step-6 losses and test loss', covers=[0.43, 0.46, 0.10])
used('quiz 0.69 is about ln 2', abs(math.log(2) - 0.69) < 0.005, 0.69)
lv.literal('0.005', why='a lowered rate in an invented log, and the rate written in a planted test')
lv.literal('0.1', why='wall seconds in the sample log, a stated setting')
E(L15, 'quiz[2].widget.answer', 1)

# ---------------- l16 ----------------
L16 = 'l16-paired-seeds'
B, Bu = V('B'), V('B-reshuffled')
d = [b - a for a, b in zip(A, B)]
du = [b - a for a, b in zip(A, Bu)]
mB, sB = mean2('B', B), sd2('B', B)
db, sdd = mean2('d', d), sd2('d', d)
t = agree('paired t', db / (sdd / math.sqrt(10)), float(stats.ttest_rel(B, A).statistic))
pP = float(stats.ttest_rel(B, A).pvalue)
agree('paired p', pP, 2 * M4.t_cdf(-abs(t), 9))
tw = agree('Welch t', (mB - mA) / math.sqrt((sA ** 2 + sB ** 2) / 10), float(stats.ttest_ind(B, A, equal_var=False).statistic))
pW = float(stats.ttest_ind(B, A, equal_var=False).pvalue)
wins = sum(x < 0 for x in d)
lv.claim(wins == 10 and mA - mB < min(sA, sB), 'B is lower on all 10 seeds, and the means differ by less than either sd', covers=[mA - mB])
lv.claim(abs(A[7] - B[7]) < 0.005 and round(A[7], 2) == round(B[7], 2) == 0.2, 'seed 7 gives about 0.20 to each set-up', covers=[0.2])
big = int(np.argmin(d))
E(L16, 'screens[1].widget.answer[0]', f'p{big}')
agree('largest gain', -d[big], A[big] - B[big])
E(L16, 'screens[2].widget.answer', round(t, 2))
agree('standard error of d', sdd / math.sqrt(10), st.stdev(d) / 10 ** 0.5, extra=[sdd / 3])
agree('t with sd alone', db / sdd, st.fmean(d) / st.stdev(d))
five = [round(x, 3) for x in d[:5]]
m5, s5 = mean2('five differences', five), sd2('five differences', five)
t5 = agree('t from five', m5 / (s5 / math.sqrt(5)), float(stats.ttest_1samp(five, 0).statistic))
agree('five differences sum', sum(five), st.fsum(five))
E(L16, 'screens[3].widget.rows[0][1].answer', round(m5, 4))
E(L16, 'screens[3].widget.rows[1][1].answer', round(s5, 4))
E(L16, 'screens[3].widget.rows[2][1].answer', round(t5, 2))
agree('five differences sd over n', float(np.std(five)), st.pstdev(five))
E(L16, 'screens[4].widget.answer', round(tw, 2))
agree('Welch standard error', math.sqrt((sA ** 2 + sB ** 2) / 10), math.hypot(st.stdev(A), st.stdev(B)) / 10 ** 0.5)
tq9 = agree('t quantile, 9 df', M4.t_quantile(0.975, 9), float(stats.t.ppf(0.975, 9)))
lv.claim(round(tq9, 3) == 2.262, 't quantile 2.262', covers=[2.262])
hw = agree('interval half-width', tq9 * sdd / math.sqrt(10), float(stats.t.ppf(0.975, 9)) * st.stdev(d) / 10 ** 0.5)
ci = stats.ttest_rel(B, A).confidence_interval(0.95)
agree('interval lower end (SciPy)', db - hw, float(ci.low))
agree('interval upper end (SciPy)', db + hw, float(ci.high))
E(L16, 'screens[5].widget.answer', round(db + hw, 4))
agree('interval with 1.96', db + 1.96 * sdd / math.sqrt(10), db + NormalDist().inv_cdf(0.975) * sdd / math.sqrt(10), 1e-3)
agree('interval without sqrt n', db + tq9 * sdd, db + float(stats.t.ppf(0.975, 9)) * sdd)
fw = agree('FWER of 20 tests', 1 - 0.95 ** 20, 1 - math.exp(20 * math.log(0.95)))
E(L16, 'screens[6].widget.answer', round(fw, 3))
agree('0.95^20', 0.95 ** 20, math.prod([0.95] * 20))
used('Bonferroni level for 20 tests', abs(0.05 / 20 - 0.0025) < 1e-15, 0.0025, 0.05)
cor = agree('correlation A, B', float(np.corrcoef(A, B)[0, 1]), st.correlation(A, B))
coru = agree('correlation A, B with other batches', float(np.corrcoef(A, Bu)[0, 1]), st.correlation(A, Bu))
dbu, sdu = mean2('d other batches', du), sd2('d other batches', du)
tu = agree('paired t, other batches', dbu / (sdu / math.sqrt(10)), float(stats.ttest_rel(Bu, A).statistic))
pU = agree('paired p, other batches', float(stats.ttest_rel(Bu, A).pvalue), 2 * M4.t_cdf(-abs(tu), 9))
agree('se, other batches', sdu / math.sqrt(10), st.stdev(du) / 10 ** 0.5)
lv.claim(0.05 < pU < 0.06 and sdu > 1.9 * sdd, 'with other batches s_d nearly doubles and p falls just short of 5%')
E(L16, 'screens[8].widget.answer', round(tu, 2))
need = agree('seeds needed, our pairs', ((NormalDist().inv_cdf(0.975) + NormalDist().inv_cdf(0.8)) * sdd / 0.02) ** 2, ((stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) * st.stdev(d) / 0.02) ** 2)
needu = agree('seeds needed, other batches', ((NormalDist().inv_cdf(0.975) + NormalDist().inv_cdf(0.8)) * sdu / 0.02) ** 2, ((stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) * st.stdev(du) / 0.02) ** 2)


def power_n(sdv, delta):  # route B: smallest n with normal-approximation power of at least 0.8
    n = 1
    while stats.norm.cdf(delta * math.sqrt(n) / sdv - stats.norm.ppf(0.975)) < 0.8:
        n += 1
    return n


lv.claim(math.ceil(need) == power_n(sdd, 0.02) == 7 and math.ceil(needu) == power_n(sdu, 0.02) == 24, 'seeds needed: 7 and 24, by the formula and by a search', covers=[7, 24])
tq7 = agree('t quantile, 7 df', M4.t_quantile(0.975, 7), float(stats.t.ppf(0.975, 7)))
lo8 = agree('transfer: lower end', 0.12 - tq7 * 0.10 / math.sqrt(8), 0.12 - float(stats.t.ppf(0.975, 7)) * 0.1 / 8 ** 0.5, extra=[0.12 + tq7 * 0.1 / math.sqrt(8), 0.1 / math.sqrt(8), 0.12, 0.10, round(tq7, 3)])
E(L16, 'screens[11].widget.answer', round(lo8, 3))
agree('transfer: lower end with 1.96', 0.12 - 1.96 * 0.1 / math.sqrt(8), 0.12 - 0.196 / 8 ** 0.5)
agree('transfer: lower end without sqrt 8', 0.12 - tq7 * 0.1, 0.12 - float(stats.t.ppf(0.975, 7)) / 10)
E(L16, 'quiz[0].widget.answer', -0.012 / (0.020 / 4))
used('quiz t inputs', abs(0.020 / math.sqrt(16) - 0.005) < 1e-15 and abs(-0.012 / 0.020 + 0.6) < 1e-12, 0.012, 0.020, 0.005, 0.6, 2.4)
f10 = agree('FWER of 10 tests', 1 - 0.95 ** 10, 1 - math.prod([0.95] * 10), extra=[0.95 ** 10, 0.5])
E(L16, 'quiz[2].widget.answer', round(f10, 3))

# ---------------- review ----------------
r1 = [0.31, 0.35, 0.29, 0.33, 0.32]
r1s = sd2('review five', r1)
E('review', 'items[0].widget.answer', round(r1s, 4))
agree('review five over n', float(np.std(r1)), st.pstdev(r1), extra=[st.variance(r1)])
used('review five: mean 0.32, squares 0.002, over 4 0.0005', abs(st.fmean(r1) - 0.32) < 1e-12 and abs(sum((x - 0.32) ** 2 for x in r1) - 0.002) < 1e-12, *r1, 0.32, 0.002, 0.0005, 0.01, 0.03)
r3 = [-0.02, -0.01, -0.03, 0.00, -0.02, -0.01]
r3m, r3s = mean2('review six', r3), sd2('review six', r3)
r3t = agree('review six t', r3m / (r3s / math.sqrt(6)), float(stats.ttest_1samp(r3, 0).statistic), extra=[r3s / math.sqrt(6), r3m / r3s])
E('review', 'items[2].widget.answer', round(r3t, 2))
E('review', 'items[3].widget.answer', (3 + 1) * 5)
used('review bimodal: 2 at 0.70, 8 at 0.12 average about 0.24', abs((2 * 0.70 + 8 * 0.12) / 10 - 0.236) < 1e-9, 0.70, 0.12, 0.24)
rh = agree('review interval half-width', M4.t_quantile(0.975, 9) * 0.02 / math.sqrt(10), float(stats.t.ppf(0.975, 9)) * 0.02 / 10 ** 0.5)
E('review', 'items[5].widget.answer', round(0.03 - rh, 4))
lv.claim(abs(round(0.03 - 2.262 * 0.02 / math.sqrt(10), 4) - round(0.03 - rh, 4)) < 1e-12, 'the review interval with the printed 2.262 rounds the same', covers=[0.03 + rh, 0.03 - 1.96 * 0.02 / math.sqrt(10), 0.03 - 2.262 * 0.02])
used('review overfit batch', 0.002 < 0.01, 0.002)
E('review', 'items[7].widget.answer', round((0.44 - 0.36) - (0.39 - 0.34), 2))
used('review 2x2', abs((0.39 - 0.34) - 0.05) < 1e-12 and abs((0.44 - 0.36) - 0.08) < 1e-12 and abs(0.44 - 0.34 - 0.10) < 1e-12, 0.44, 0.36, 0.39, 0.34, 0.05, 0.08, 0.10)

# ---------------- homework ----------------
nh = agree('homework seeds needed', ((1.960 + 0.842) * 0.015 / 0.01) ** 2, ((stats.norm.ppf(0.975) + stats.norm.ppf(0.8)) * 1.5) ** 2, 1e-3, extra=[17.7, 2.802, 1.5])
lv.claim(math.ceil(nh) == power_n(0.015, 0.01) == 18, 'homework: 18 seeds by the formula and by a search')
E('homework', 'items[4].widget.answer', 18)
used('homework one-sided slip', math.ceil(((1.645 + 0.842) * 1.5) ** 2) == 14, 1.645, 0.842, 1.960, 0.015, 0.01)
E('homework', 'items[5].widget.answer', 0.05 / 8)
agree('Bonferroni for 8 and 9', 0.05 / 8, 0.00625, extra=[0.05 / 9])
ih = agree('homework interval half-width', 2.201 * 0.010 / math.sqrt(12), float(stats.t.ppf(0.975, 11)) * 0.01 / 12 ** 0.5, 1e-3)
lv.claim(round(float(stats.t.ppf(0.975, 11)), 3) == 2.201, 't quantile 2.201 for 11 df', covers=[2.201])
E('homework', 'items[7].widget.answer', round(-0.008 + ih, 4))
used('homework interval ends', True and -0.008 - ih < -0.008 + ih < 0, -0.008 - ih, 0.008, 0.010)
used('longform figures', abs(0.431 - 0.412 - 0.019) < 1e-12 and round(hi - lo, 3) == 0.134, 0.431, 0.412, 0.019, 0.134)

# ---------------- problems ----------------
P = [0.512, 0.468, 0.530, 0.495, 0.551, 0.487]
Q = [0.498, 0.461, 0.509, 0.490, 0.532, 0.480]
dq = [round(b - a, 3) for a, b in zip(P, Q)]
dm, ds = mean2('problem 1 differences', dq), sd2('problem 1 differences', dq)
dt = agree('problem 1 t', dm / (ds / math.sqrt(6)), float(stats.ttest_rel(Q, P).statistic), 1e-6)
agree('problem 1 sum', sum(dq), st.fsum(dq), extra=[sum((x - dm) ** 2 for x in dq), ds / math.sqrt(6), dm / ds])
dh = agree('problem 1 half-width', 2.571 * ds / math.sqrt(6), float(stats.t.ppf(0.975, 5)) * ds / 6 ** 0.5, 1e-3)
lv.claim(round(float(stats.t.ppf(0.975, 5)), 3) == 2.571, 't quantile 2.571 for 5 df', covers=[2.571, dm - dh])
for i, v in enumerate((round(dm, 4), round(ds, 4), round(dt, 2), round(dm + dh, 4))):
    E('problems', f'items[0].parts[{i}].widget.answer', v)
agree('problem 1 sd over n', float(np.std(dq)), st.pstdev(dq), extra=[dm + 1.96 * ds / math.sqrt(6)])
used('problem 1 inputs', all(abs(b - a - c) < 1e-9 for a, b, c in zip(P, Q, dq)), *P, *Q, *dq)
fx, nx = [0.25, 0.27, 0.24, 0.26, 0.28], [0.29, 0.30, 0.28, 0.31, 0.32]
dx = [round(b - a, 2) for a, b in zip(fx, nx)]
xm, xs = mean2('problem 2 differences', dx), sd2('problem 2 differences', dx)
E('problems', 'items[1].parts[0].widget.answer', round(xm, 3))
E('problems', 'items[1].parts[1].widget.answer', round(xs, 4))
agree('problem 2 sd over n', float(np.std(dx)), st.pstdev(dx))
used('problem 2 inputs', all(abs(b - a - c) < 1e-9 for a, b, c in zip(fx, nx, dx)) and abs(sum((x - 0.04) ** 2 for x in dx) - 0.0002) < 1e-12, *fx, *nx, *dx, 0.0002, 0.00005, 0.01)
E('problems', 'items[1].parts[2].widget.answer', round((0.27 - 0.34) - (0.33 - 0.36), 2))
used('problem 2 2x2', abs((0.27 - 0.34) + 0.07) < 1e-12 and abs((0.33 - 0.36) + 0.03) < 1e-12, 0.36, 0.33, 0.34, 0.27, 0.07, 0.03, 0.09)
E('problems', 'items[1].parts[3].widget.answer', (1 + 4 + 1 + 4) * 5)
used('problem 2 runs', 2 ** 4 * 5 == 80, 80)
y5 = [0.142, 0.131, 0.155, 0.138, 0.149]
ym, ys = mean2('problem 3', y5), sd2('problem 3', y5)
yz = agree('problem 3 z of the best', (ym - min(y5)) / ys, (st.fmean(y5) - 0.131) / st.stdev(y5), extra=[sum((x - ym) ** 2 for x in y5), 0.715, 0.012])
agree('problem 3 sd over n', float(np.std(y5)), st.pstdev(y5))
for i, v in enumerate((round(ym, 3), round(ys, 4), round(yz, 2))):
    E('problems', f'items[2].parts[{i}].widget.answer', v)
used('problem 3 inputs', abs(sum(y5) - 0.715) < 1e-12, *y5)

# ---------------- code widgets: solution, starter, mutants; and the stated results they print ----------------


def judge(a, e, cmp, tol=None):
    def flat(x):
        return x.tolist() if hasattr(x, 'tolist') and not isinstance(x, (int, float, complex, str)) else x

    def close(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) or isinstance(y, dict):
            return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(close(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(close(p, q) for p, q in zip(x, y))
        if isinstance(x, (bool, str)) or isinstance(y, (bool, str)) or x is None or y is None:
            return x == y
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x), float(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y

    def same(x, y):
        x, y = flat(x), flat(y)
        if isinstance(x, dict) or isinstance(y, dict):
            return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(same(x[k], y[k]) for k in x)
        if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
            return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(same(p, q) for p, q in zip(x, y))
        return bool(x == y)
    return close(a, e) if cmp == 'isclose' else same(a, e)


def run_widget(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    for k, v in (w.get('data') or {}).items():
        shutil.copy(os.path.join(APP, v), os.path.join(dd, k))
    sys.path.insert(0, dd)
    for mod in [m for m in sys.modules if m == 'autograd' or m.startswith('nt_ops')]:
        sys.modules.pop(mod)
    ns = {'__learner_source__': src}
    exec(ZQ_LIB, ns)
    return cwd, dd, ns


def first_fail(w, src, want=None):
    cwd, dd, ns = run_widget(w, src)
    try:
        try:
            with np.errstate(all='ignore'):
                exec((w.get('prelude') or '') + '\n', ns)
                exec(src, ns)
        except Exception:
            return -1, ns
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns)
                    got = eval(c['call'], ns)
                tl = c.get('tol')
                ok = judge(got, eval(c['expect'], ns), c.get('compare', 'isclose'), (tl.get('rel') or 0, tl.get('abs') or 0) if tl else None)
            except Exception:
                ok = False
            if not ok:
                return i + 1, ns
        return 0, ns
    finally:
        os.chdir(cwd)
        sys.path.remove(dd)
        shutil.rmtree(dd, ignore_errors=True)
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
        got, _ = first_fail(w, w['solution'])
        lv.claim(got == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter'])[0] != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        lv.claim(len(w['tests']) <= 15 and f'Submit runs {len(w["tests"])} hidden tests' in w.get('how', ''), f'{lab}: the how line counts {len(w["tests"])} tests')
        for mu in w.get('mutants', []):
            nm += 1
            g = first_fail(w, mu['source'])[0]
            lv.claim(g == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {g})')
print(f'code widgets {nw}, mutants {nm}')

# the exact short runs the training widgets compare, recomputed by route B
W13 = lv._file(L13)[1]['screens'][8]['widget']
rs = [np.random.default_rng(s) for s in np.random.SeedSequence(7).spawn(3)]
exp13 = float(eval(W13['tests'][0]['expect']))
agree('l13 set_all_seeds: 5-step run of the full set-up from seed 7, the test\'s value against train_run', exp13, run_b(dict(opt='adam', lr=0.02, ln=True, p=0.1), 7, 5)[0], 1e-9)
W15 = lv._file(L15)[1]['screens'][9]['widget']
agree('l15 overfit_one_batch: 5 steps, the test\'s value against the hand backward', float(eval(W15['tests'][0]['expect'])), ofb_b(M4.init_params(M4.seed_streams(0)[0]), 5, 0.01), 1e-9)
init0 = full_loss(M4.init_params(M4.seed_streams(0)[0]), Xb, yb)
agree('l15 overfit_one_batch: the starting loss, against the hand forward', float(eval(W15['tests'][3]['expect'])), ofb_b(M4.init_params(M4.seed_streams(0)[0]), 0, 0.01), 1e-9)
# statements in code-screen feedback
E(L13, 'screens[7].feedback.correct', round(mA, 4))
E(L14, 'screens[9].feedback.correct', round(DM['adam'], 4))
E(L15, 'screens[9].feedback.correct', round(g200, 4))
E(L16, 'screens[10].feedback.correct', math.ceil(need))
E(L16, 'screens[10].feedback.correct', math.ceil(needu))
W16 = lv._file(L16)[1]['screens'][9]['widget']
cc = eval(W16['tests'][2]['expect'])
agree('compare_configs A against B: mean difference', cc['mean_diff'], db)
agree('compare_configs A against B: t', cc['t'], t)
lv.claim(cc['wins'] == 10 and cc['n'] == 10, 'compare_configs: 10 pairs, B lower on all 10')
HWW = lv._file('homework')[1]['items'][0]['widget']
rep = eval(HWW['tests'][4]['expect'])
for c, r in REM.items():
    agree(f'experiment_report on our ablation, {r}: mean difference', rep[r]['mean_diff'], DM[c])
lv.claim([rep[r]['survives'] for r in ('sgd+ln+do', 'adam+do', 'adam+ln')] == [False, True, True], 'with three changes, Adam\'s removal misses the Bonferroni bar; layer norm\'s and dropout\'s pass')
lv.claim(eval(HWW['tests'][1]['expect']) == {'real-down': True, 'null-1': False, 'real-up': True, 'null-2': False}, 'the planted report finds both real effects and neither null')
lv.claim(eval(HWW['tests'][2]['expect']) is True and eval(HWW['tests'][3]['expect']) is False, 'the borderline effect survives alone and fails among five changes')

# structural counts the prose states: runs, steps, split sizes, quantile levels, and ratios in words
n_by = {k: len(V(k)) for k in CONFIGS}
lv.claim(all(v == 10 for v in n_by.values()) and len(SEEDS['runs'][0]['val_curve']) * 6 == 300 and len(SEEDS['runs'][0]['val_curve']) == 50,
         'ten seeds a configuration; curves every 6 of 300 steps', covers=[10, 300, 6])
lv.claim(len(X) == 600 and len(tr) == 400 and len(va) == 100 == len(te), 'data: 600 rows, 400 train, 100 validation, 100 test', covers=[600, 400, 100])
lv.claim(len(cg) == 51 and len(cz) == 51 and (len(cg) - 1) * 4 == 200, 'overfitting curves: 200 steps, every 4', covers=[200, 4, 8])
lv.claim(len(first) == 150, 'resumed at step 150 of 300', covers=[150])
lv.claim(abs(stats.t.ppf(0.975, 9) - tq9) < 1e-12 and abs(stats.norm.ppf(0.8) - 0.8416) < 1e-4, 'the 0.975 and 0.8 quantiles the formulas name', covers=[0.975, 0.8, 9, 11, 5])
lv.claim(round(d2 / 0.002) == 4, 'the 0.002 gain is a quarter of the noise: four times smaller', covers=[4, 0.25])
lv.claim(round(sdu / sdd) == 2 and round(s6['adam'] / s6['ln']) == 2 and 2 * 0.05 * 10 == 1.0, 'twice and doubles in words: s_d with other batches, seed 6 ranking, 20 x 5% counted twice', covers=[2])
lv.claim(4 ** 2 == 16 and 2 ** 3 == 8 and 4 + 1 == 5, 'small counts in hints: 16 seeds, 8 mixes, 5 rows', covers=[16, 8, 5])
lv.literal('10^-7', why='the relative tolerance of an exact short-run test, a setting')
lv.literal('500', why='a step count in an invented quiz scenario')
lv.check_wrongs()
lv.report()
