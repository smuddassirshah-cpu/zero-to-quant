"""Recompute every number stated in makemore level 1 (Bigrams) and check each value at its JSON path.

Run: <venv>/bin/python docs/reports/makemore-L1-numbers.py   (NumPy and the standard library; exits 0 when every check passes)

Route A: NumPy arrays (counts with np.add.at, losses as array sums, the one-layer network through the shipped autograd.py).
Route B: plain Python (Counter of pairs, dictionary rows, per-pair loops; the network with a hand-written NumPy gradient).
Every code widget of the level is also run: the model solution passes its hidden tests, the starter fails them, and each
mutant first fails the test it names (ENGINE-BACKLOG 1263; grade-all --code repeats this in Pyodide).
"""
import hashlib
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

lv = Level('makemore', 1)
E = lv.expect


def two(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol * max(1.0, abs(a)), f'{label}: routes agree ({a!r} vs {b!r})')
    return a


# ---------------- data and split ----------------
raw = open(os.path.join(DATA, 'names.txt'), 'rb').read()
lv.claim(hashlib.md5(raw).hexdigest() == '401b3c4cac9e28a586ed15e81256680d', 'names.txt MD5 matches the brief')
W = raw.decode().splitlines()
lv.claim(len(W) == 32033, '32,033 names')
SYM = '.abcdefghijklmnopqrstuvwxyz'
IX = {c: i for i, c in enumerate(SYM)}
perm = np.random.default_rng(42).permutation(len(W))
tr = [W[i] for i in perm[:25626]]; dv = [W[i] for i in perm[25626:28829]]; te = [W[i] for i in perm[28829:]]
lv.claim((len(tr), len(dv), len(te)) == (25626, 3203, 3204) and tr[:3] == ['briah', 'xzayvion', 'amad'], 'the split: sizes and first training names')


def pairs(ws):
    for w in ws:
        cs = '.' + w + '.'
        for a, b in zip(cs, cs[1:]):
            yield a, b


def counts_A(ws):
    a = np.array([IX[x] for x, _ in pairs(ws)]); b = np.array([IX[y] for _, y in pairs(ws)])
    N = np.zeros((27, 27), int); np.add.at(N, (a, b), 1)
    return N


def counts_B(ws):
    return Counter(pairs(ws))


N = counts_A(W); C = counts_B(W)
lv.claim(all(N[IX[a], IX[b]] == C[(a, b)] for a in SYM for b in SYM), 'whole-list counts: array and Counter agree in every cell')
total = int(N.sum()); two('pairs in the file', total, sum(len(w) + 1 for w in W))
letters = sum(len(w) for w in W)


def nll_A(P, ws):
    a = np.array([IX[x] for x, _ in pairs(ws)]); b = np.array([IX[y] for _, y in pairs(ws)])
    p = P[a, b]
    return math.inf if (p == 0).any() else float(-np.log(p).mean())


def nll_B(Cn, ws_eval, alpha):
    row = Counter()
    for (a, b), k in Cn.items():
        row[a] += k
    s = 0.0; n = 0
    for a, b in pairs(ws_eval):
        p = (Cn[(a, b)] + alpha) / (row[a] + 27 * alpha)
        if p == 0:
            return math.inf
        s -= math.log(p); n += 1
    return s / n


def probs(Nm, alpha):
    M = Nm + alpha
    return M / M.sum(1, keepdims=True)


# ---------------- l1 ----------------
L1 = 'l1-counting-pairs'
lastc = Counter(w[-1] for w in W)
lv.claim(lastc.most_common(1)[0] == ('n', 6763) and lastc['a'] == 6640 and lastc['e'] == 3983 and lastc['y'] == 2007, 'last letters: n 6,763, a 6,640, e 3,983, y 2,007')
two('n then end', int(N[IX['n'], 0]), lastc['n'])
for p in ('screens[0].explain.text', 'screens[0].feedback.correct'):
    E(L1, p, 6763); E(L1, p, 6640)
E(L1, 'screens[0].widget.options[2].why', 3983); E(L1, 'screens[0].widget.options[3].why', 2007)
lv.claim(W[:10] == ['emma', 'olivia', 'ava', 'isabella', 'sophia', 'charlotte', 'mia', 'amelia', 'harper', 'evelyn'], 'first ten names in the console')
emma = list(pairs(['emma'])); E(L1, 'screens[1].widget.answer', len(emma)); E(L1, 'screens[1].widget.wrong[0].value', len('emma') - 1)
E(L1, 'screens[1].widget.wrong[2].value', len('.emma.'))
sl = [[int(N[IX[r], IX[c]]) for c in '.aen'] for r in '.ane']
lv.claim(sl == [[C[(r, c)] for c in '.aen'] for r in '.ane'], 'the slice, two ways')
lv.claim(lv.files[L1]['screens'][2]['canvas']['params']['matrices'][0]['rows'] == sl, 'the slice on the canvas matches the counts')
E(L1, 'screens[2].widget.answer', C[('a', 'n')]); E(L1, 'screens[2].widget.wrong[0].value', C[('n', 'a')])
three = counts_B(['ava', 'eve', 'ana'])
rows3 = lv.files[L1]['screens'][3]['widget']['rows']
lv.claim([r[1]['answer'] for r in rows3] == [three[('.', 'a')], three[('a', '.')], three[('e', 'v')], sum(three.values())], 'three names by hand')
lv.claim(rows3[3][1]['wrong'][0]['value'] == sum(len(w) - 1 for w in ['ava', 'eve', 'ana']), 'three names: the no-marks slip')
E(L1, 'screens[4].prose', letters); E(L1, 'screens[4].widget.answer', two('pairs, letters plus names', letters + len(W), total))
E(L1, 'screens[4].widget.wrong[1].value', letters - len(W)); E(L1, 'screens[4].widget.wrong[2].value', letters + 2 * len(W))
first = Counter(w[0] for w in W)
lv.claim(first.most_common(3) == [('a', 4410), ('k', 2963), ('m', 2538)], 'first letters a 4,410, k 2,963, m 2,538')
lv.claim(lv.files[L1]['screens'][5]['canvas']['state']['values'] == {c: int(N[0, IX[c]]) for c in SYM[1:]}, 'start row on the canvas')
E(L1, 'screens[5].widget.answer', two('start row', int(N[0].sum()), len(W)))
two('end column', int(N[:, 0].sum()), len(W))
zeros = [(a, b) for a in SYM for b in SYM if C[(a, b)] == 0]
two('zero cells', len(zeros), int((N == 0).sum())); E(L1, 'screens[6].prose', len(zeros))
lv.claim(('.', '.') in zeros and ('q', 'b') in zeros and ('x', 'r') in zeros and C[('.', 'q')] == 92, 'empty cells named are empty; start then q is 92')
lv.claim(len(list(pairs(['emma']))) - 2 == 3, 'emma without marks: 3 pairs')
lv.claim(int(N[14, 0]) == 6763, 'N[14, 0] holds n then end')
E(L1, 'screens[10].widget.answer', 249 - 70 - 60 - 61)
E(L1, 'quiz[0].widget.answer', two('barbara b a', sum(1 for p in pairs(['barbara']) if p == ('b', 'a')), 'barbara'.count('ba')))
E(L1, 'quiz[1].prose', two('row a', int(N[1].sum()), sum(w.count('a') for w in W)))
lv.claim(sum(len(w) == 2 for w in W) == 65 and 'kc' in W and 'jo' in W, '65 two-letter names, kc and jo among them')
E(L1, 'quiz[2].widget.answer', len(list(pairs(['kc']))))

# ---------------- l2 ----------------
L2 = 'l2-the-counts-are-best'
qrow = {b: C[('q', b)] for b in SYM if C[('q', b)]}
lump = {'u': qrow['u'], 'end': qrow['.'], 'a': qrow['a'], 'i': qrow['i']}; lump['other'] = sum(qrow.values()) - sum(lump.values())
lv.claim(lump == {'u': 206, 'end': 28, 'a': 13, 'i': 13, 'other': 12} and sum(qrow.values()) == 272, 'row q: 272 pairs, u 206, end 28, a 13, i 13, other 12')
A = {'u': 0.9, 'end': 0.04, 'a': 0.02, 'i': 0.02, 'other': 0.02}
llA = sum(k * math.log(A[c]) for c, k in lump.items()); llB = sum(k * math.log(k / 272) for k in lump.values())
llB2 = float(np.dot(list(lump.values()), np.log(np.array(list(lump.values())) / 272)))
two('LL of row B', llB, llB2)
for p in ('screens[0].explain.text', 'screens[0].feedback.correct'):
    E(L2, p, round(llA, 2)); E(L2, p, round(llB, 2))
f = lambda pu: 206 * math.log(pu) + 28 * math.log((1 - pu) * 28 / 66) + 26 * math.log((1 - pu) * 13 / 66) + 12 * math.log((1 - pu) * 12 / 66)
grid = max((f(k / 10000), k / 10000) for k in range(5000, 9900))
lv.claim(abs(grid[1] - 206 / 272) < 2e-4, f'explore: the peak of the caption formula is at 206/272 ({grid[1]})')
E(L2, 'screens[1].widget.answer', round(206 / 272, 2)); E(L2, 'screens[1].explain.text', round(206 / 272, 3))
E(L2, 'screens[2].widget.answer', round(28 / 272, 4)); E(L2, 'screens[2].widget.wrong[0].value', round(28 / total, 4))
E(L2, 'screens[4].prose', int(N[1].sum())); E(L2, 'screens[4].widget.answer', round(C[('a', 'n')] / N[1].sum(), 4))
E(L2, 'screens[4].widget.wrong[0].value', round(C[('a', 'n')] / total, 4))
E(L2, 'screens[5].widget.answer', round(C[('a', '.')] / N[1].sum(), 4)); E(L2, 'screens[5].widget.wrong[0].value', round(C[('a', '.')] / len(W), 4))
E(L2, 'screens[6].widget.answer', round(1 / (272 + 27), 5)); E(L2, 'screens[6].widget.wrong[0].value', round(1 / 273, 5)); E(L2, 'screens[6].widget.wrong[1].value', round(1 / 272, 5))
Nt = counts_A(tr); Ct = counts_B(tr)
two('training zero cells', int((Nt == 0).sum()), sum(1 for a in SYM for b in SYM if Ct[(a, b)] == 0))
lv.claim(int((Nt == 0).sum()) == 109, '109 zero cells on the training names')
sweep = {}
for al in (0.01, 0.1, 1, 10, 100):
    dA = nll_A(probs(Nt, al), dv); dB = nll_B(Ct, dv, al); two(f'dev loss alpha {al}', dA, dB, 1e-12)
    tA = nll_A(probs(Nt, al), tr); two(f'train loss alpha {al}', tA, nll_B(Ct, tr, al), 1e-12)
    sweep[al] = (round(tA, 4), round(dA, 4))
lv.claim([sweep[a][1] for a in (0.01, 0.1, 1, 10, 100)] == [2.452, 2.4514, 2.4514, 2.4606, 2.5507], 'dev sweep 2.4520, 2.4514, 2.4514, 2.4606, 2.5507')
lv.claim([sweep[a][0] for a in (0.01, 0.1, 1, 10, 100)] == [2.4529, 2.4529, 2.4536, 2.4633, 2.554], 'train sweep (brief)')
lv.claim(lv.files[L2]['screens'][7]['canvas']['state']['values'] == {str(a): sweep[a][1] for a in (0.01, 0.1, 1, 10, 100)}, 'sweep bars match')
lv.claim(nll_A(probs(Nt, 0.1), dv) < nll_A(probs(Nt, 1), dv), '0.1 is a hair below 1 (both 2.4514 to 4 places)')
nrow = N[IX['n']]; E(L2, 'screens[8].prose', int(nrow.sum())); E(L2, 'screens[8].widget.answer', round(nrow.sum() / total, 4))
trapv = lv.files[L2]['screens'][8]['canvas']['state']['values']
lv.claim(sum(trapv.values()) == nrow.sum() and all(trapv[k] == nrow[IX['.' if k == 'end' else k]] for k in trapv if k != 'other'), 'row n bars')
unseen = [(w, a + b) for w in dv for a, b in pairs([w]) if Ct[(a, b)] == 0]
unseen2 = [(w, a + b) for w in dv for a, b in pairs([w]) if Nt[IX[a], IX[b]] == 0]
lv.claim(unseen == unseen2 and len(unseen) == 7, f'7 unseen dev pairs, two ways: {unseen}')
lv.claim(sorted(set(w for w, _ in unseen)) == sorted(['tzvi', 'zvi', 'siegfried', 'comfort', 'maxmilian', 'noahh', 'omkar']), 'the seven dev names')
lv.claim(nll_A(probs(Nt, 0), dv) == math.inf and nll_B(Ct, dv, 0) == math.inf, 'unsmoothed dev loss is infinite')
E(L2, 'screens[11].widget.answer', round(7 / 11, 4)); E(L2, 'screens[11].widget.wrong[0].value', round(6 / 9, 4)); E(L2, 'screens[11].widget.wrong[1].value', round(7 / 10, 4))
vrow = N[IX['v']]
lv.claim(vrow.sum() == 2573 and vrow[0] == 88 and vrow[1] == 642, 'row v: 2,573, end 88, a 642')
E(L2, 'quiz[0].widget.answer', round(642 / 2573, 4)); E(L2, 'quiz[0].widget.wrong[0].value', round(642 / total, 4))
E(L2, 'quiz[1].widget.answer', round(5 / 37, 4)); E(L2, 'quiz[1].widget.wrong[1].value', round(5 / 11, 4))
lv.claim(abs(-math.log(0.04) - 3.22) < 0.005, 'row A pays 3.22 nats per ending')

# ---------------- l3 ----------------
L3 = 'l3-one-loss-two-units'
P1 = probs(N, 1); full = two('whole-list loss', nll_A(P1, W), nll_B(C, W, 1), 1e-12)
lv.claim(round(nll_A(probs(N, 0), W), 4) == 2.454, 'unsmoothed whole-list loss 2.4540')
E(L3, 'screens[0].prose', round(full, 4)); E(L3, 'screens[0].widget.answer', round(math.log(27), 4)); E(L3, 'screens[0].widget.wrong[0].value', round(math.log2(27), 4))
E(L3, 'screens[0].feedback.correct', round(math.log(27) - full, 2))
E(L3, 'screens[1].widget.answer', round(full / math.log(2), 4)); E(L3, 'screens[1].widget.wrong[0].value', round(2.4546 * math.log(2), 4)); E(L3, 'screens[1].widget.wrong[1].value', round(2.4546 / math.log(10), 4))
E(L3, 'screens[1].explain.text', round(1 / math.log(2), 4))
E(L3, 'screens[2].widget.answer', round(math.exp(full), 2)); E(L3, 'screens[2].widget.wrong[0].value', round(2 ** 2.4546, 2)); E(L3, 'screens[2].widget.wrong[1].value', round(math.exp(3.5412), 2))
ec = [(a + b, P1[IX[a], IX[b]], -math.log(P1[IX[a], IX[b]])) for a, b in pairs(['emma'])]
ecB = [(C[(a, b)] + 1) / (sum(C[(a, x)] for x in SYM) + 27) for a, b in pairs(['emma'])]
lv.claim(np.allclose([x[1] for x in ec], ecB), 'emma chances, two ways')
rows = lv.files[L3]['screens'][3]['widget']['rows']
for k, (pr, q, c) in enumerate(ec):
    lv.claim(rows[k][1] == f'{q:.6f}', f'emma {pr} chance shown {rows[k][1]}')
    if isinstance(rows[k][2], str):
        lv.claim(rows[k][2] == f'{c:.4f}', f'emma {pr} cost shown')
lv.claim(abs(rows[3][2]['answer'] - round(ec[3][2], 4)) < 1e-12 and abs(rows[3][2]['wrong'][0]['value'] - round(-math.log10(ec[3][1]), 4)) < 1e-12, 'emma m a cost and its log10 slip')
et = sum(x[2] for x in ec)
lv.claim(round(et, 4) == 12.5716 and rows[5][2]['answer'] == 12.5716 and rows[6][2]['answer'] == round(et / 5, 4) and rows[6][2]['wrong'][0]['value'] == round(et / 4, 4), 'emma total 12.5716, average 2.5143, per-letter slip')
Pt = probs(Nt, 1)
splits = {}
for nm, ws in (('train', tr), ('dev', dv), ('test', te)):
    v = two(f'{nm} loss', nll_A(Pt, ws), nll_B(Ct, ws, 1), 1e-12); splits[nm] = v
lv.claim([round(splits[k], 4) for k in ('train', 'dev', 'test')] == [2.4536, 2.4514, 2.4702], 'train, dev, test 2.4536, 2.4514, 2.4702')
E(L3, 'screens[4].widget.answer', round((math.log(27) - splits['dev']) / math.log(2), 4)); E(L3, 'screens[4].widget.wrong[0].value', round(math.log(27) - splits['dev'], 4))
lv.claim(abs((math.log(27) - splits['dev']) / math.log(2) * 7 - 8.5) < 0.05, 'about 8.5 bits over seven symbols')
E(L3, 'screens[5].explain.text', round(3.5 * math.log(2), 4)); lv.claim(abs((2.4514 - 3.5 * math.log(2)) - 0.025) < 0.001, 'their model is better by 0.025 nats')
jo = [-math.log(P1[IX[a], IX[b]]) for a, b in pairs(['jo'])]
lv.claim([round(x, 4) for x in jo] == [2.5826, 1.8079, 2.23], 'jo costs')
E(L3, 'screens[6].widget.answer', round((jo[0] + jo[2]) / sum(jo), 2)); E(L3, 'screens[6].widget.wrong[0].value', round(jo[1] / sum(jo), 2))
em = [x[2] for x in ec]; lv.claim(round((em[0] + em[-1]) / sum(em), 2) == 0.37, 'emma mark share 0.37')
E(L3, 'screens[9].explain.text', 2.4702); lv.claim(round(splits['test'] - splits['dev'], 3) == 0.019, 'dev to test gap 0.019')
E(L3, 'quiz[0].widget.answer', round(2.4702 / math.log(2), 4)); E(L3, 'quiz[0].widget.wrong[0].value', round(2.4702 * math.log(2), 4))
lv.claim(len(list(pairs(dv))) == 22807 and len(list(pairs(te))) == 22808, 'dev 22,807 and test 22,808 pairs')
E(L3, 'quiz[2].widget.options[2].text', round(55900 / 22807, 4)); E(L3, 'quiz[2].widget.options[2].text', round(56300 / 22808, 4))

# ---------------- l4 ----------------
L4 = 'l4-bigram-as-network'
sub = tr[:500]
xs = np.array([IX[a] for a, _ in pairs(sub)]); ys = np.array([IX[b] for _, b in pairs(sub)])
lv.claim(len(xs) == 3610, '3,610 pairs in the first 500 training names')


def run_A(steps, lr):
    Wt = Tensor(np.random.default_rng(2147483647).standard_normal((27, 27))); out = []
    for k in range(steps + 1):
        loss = cross_entropy(Wt[xs], ys); out.append(loss.item())
        if k == steps:
            break
        Wt.zero_grad(); loss.backward(); sgd_step([Wt], lr)
    return out, Wt.data


def run_B(steps, lr):
    Wn = np.random.default_rng(2147483647).standard_normal((27, 27)); out = []
    for k in range(steps + 1):
        z = Wn[xs]; z = z - z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
        out.append(float(-np.log(p[np.arange(len(ys)), ys]).mean()))
        if k == steps:
            break
        g = p; g[np.arange(len(ys)), ys] -= 1; g /= len(ys); dW = np.zeros_like(Wn); np.add.at(dW, xs, g); Wn = Wn - lr * dW
    return out, Wn


cA, _ = run_A(100, 50.0); cB, _ = run_B(100, 50.0)
lv.claim(np.allclose(cA, cB, atol=1e-10), 'network curve: autograd and hand gradient agree')
lv.claim([round(cA[i], 4) for i in (0, 10, 50, 100)] == [3.7441, 2.6236, 2.4387, 2.4122], 'curve 3.7441, 2.6236, 2.4387, 2.4122')
for p in ('screens[5].prose', 'summary.ideas[1]'):
    E(L4, p, 3.7441) if p.startswith('screens') else None
E(L4, 'screens[5].prose', 2.6236); E(L4, 'screens[5].prose', 2.4387); E(L4, 'screens[5].prose', 2.4122)
pts = lv.files[L4]['screens'][5]['canvas']['params']['functions'][0]['points']
lv.claim(len(pts) == 101 and all(abs(y - cA[k]) < 5e-5 for k, y in pts), 'plotted curve matches the run')
Ns = counts_A(sub); cnt = nll_A(np.where(Ns > 0, Ns / np.maximum(Ns.sum(1, keepdims=True), 1), 1.0), sub)
cntB = -sum(k * math.log(k / sum(v for (a2, _), v in counts_B(sub).items() if a2 == a)) for (a, b), k in counts_B(sub).items()) / len(xs)
two('count model on the 500 names', cnt, cntB, 1e-12); lv.claim(round(cnt, 4) == 2.382, 'count model 2.3820')
lv.claim(round(nll_A(probs(Ns, 1), sub), 4) == 2.4554, 'add-one on the 500 names 2.4554')
c3k, W3k = run_A(3000, 50.0); lv.claim(round(c3k[-1], 4) == 2.383, 'after 3,000 steps 2.3830')
lv.claim(Ns[14, 0] == 110 and Ns[14, 1] == 51, '500 names: n then end 110, n then a 51')
E(L4, 'screens[6].widget.answer', round(math.log(110 / 51), 4)); E(L4, 'screens[6].widget.wrong[0].value', round(110 / 51, 4))
lv.claim(abs((W3k[14, 0] - W3k[14, 1]) - math.log(110 / 51)) < 1e-3, f'trained gap {W3k[14, 0] - W3k[14, 1]:.4f} matches ln(110/51)')
lv.claim(round(math.log(27), 4) == 3.2958, 'ln 27')
z = np.array([1.0, 0.0, -1.0]); sm = np.exp(z) / np.exp(z).sum()
E(L4, 'screens[2].widget.answer', round(-math.log(sm[0]), 4)); E(L4, 'screens[2].widget.wrong[1].value', round(-math.log2(sm[0]), 4))
lv.claim(lv.files[L4]['screens'][2]['canvas']['state']['values'] == {'.': round(sm[0], 4), 'a': round(sm[1], 4), 'b': round(sm[2], 4)}, 'softmax bars')
xt = np.array([0, 1, 1, 2]); yt = np.array([1, 2, 0, 0])
Wt = Tensor(np.zeros((3, 3))); l0 = cross_entropy(Wt[xt], yt); l0.backward(); g = Wt.grad.copy(); sgd_step([Wt], 1.0)
gB = np.zeros((3, 3))
for x, y in zip(xt, yt):
    gB[x] += np.full(3, 1 / 3) - np.eye(3)[y]
gB /= 4
lv.claim(np.allclose(g, gB), 'tiny gradient, two ways')
E(L4, 'screens[3].widget.answer', round(float(Wt.data[0, 1]), 4)); E(L4, 'screens[3].widget.wrong[1].value', round(-4 * g[0, 1] * 1, 4))
E(L4, 'screens[4].widget.answer', round(float(Wt.data[1, 1]), 4)); E(L4, 'screens[4].widget.wrong[0].value', round(-gB[1, 1] / 2, 4))
E(L4, 'screens[4].explain.text', round(math.log(3), 4)); E(L4, 'screens[4].explain.text', round(cross_entropy(Wt[xt], yt).item(), 4))
l01, _ = run_A(50, 0.1); lv.claim(round(l01[50], 4) == 3.7007, 'step 0.1: 3.7007 after 50 steps')
xq = np.array([0, 0]); yq = np.array([1, 2]); Wq = Tensor(np.zeros((3, 3))); cross_entropy(Wq[xq], yq).backward(); sgd_step([Wq], 3.0)
E(L4, 'quiz[2].widget.answer', round(float(Wq.data[0, 0]), 4))

# ---------------- review-1 ----------------
E('review', 'items[0].widget.answer', len(list(pairs(['liam']))))
E('review', 'items[2].widget.answer', round(C[('y', 'a')] / N[IX['y']].sum(), 4)); lv.claim(N[IX['y']].sum() == 9776 and C[('y', 'a')] == 2143, 'row y 9,776, y a 2,143')
E('review', 'items[2].widget.wrong[0].value', round(2143 / total, 4))
lv.claim(N[IX['x']].sum() == 697 and C[('x', 'g')] == 0, 'row x 697, x g unseen')
E('review', 'items[3].widget.answer', round(1 / 724, 6)); E('review', 'items[3].widget.wrong[0].value', round(1 / 698, 6))
E('review', 'items[5].widget.answer', round(math.exp(2.4702), 2)); E('review', 'items[5].widget.wrong[0].value', round(2 ** 2.4702, 2))
al = [-math.log(q) for q in (0.1376, 0.0746, 0.0940)]
E('review', 'items[6].widget.answer', round(sum(al) / 3, 4)); E('review', 'items[6].widget.wrong[0].value', round(sum(al), 4)); E('review', 'items[6].widget.wrong[1].value', round(sum(al) / 2, 4))
lv.claim([round(x, 4) for x in al] == [1.9834, 2.5956, 2.3645], 'al costs as printed')
lv.claim(all(abs(q - P1[IX[a], IX[b]]) < 5e-5 for q, (a, b) in zip((0.1376, 0.0746, 0.0940), pairs(['al']))), 'al chances come from the whole-list add-one table')
E('review', 'items[7].explain.text', round(3.4 * math.log(2), 4))
xr = np.array([1, 1, 1]); yr = np.array([0, 0, 2]); Wr = Tensor(np.zeros((3, 3))); cross_entropy(Wr[xr], yr).backward(); sgd_step([Wr], 1.5)
E('review', 'items[8].widget.answer', round(float(Wr.data[1, 0]), 4))

# ---------------- homework-1 ----------------
two_letter = Counter(w[:2] for w in W if len(w) >= 2)
lv.claim(two_letter.most_common(3) == [('ma', 1453), ('ja', 1255), ('ka', 1254)], 'first two letters ma 1,453, ja 1,255, ka 1,254')
perm7 = np.random.default_rng(7).permutation(len(W)); tr7 = [W[i] for i in perm7[:25626]]; dv7 = [W[i] for i in perm7[25626:28829]]
N7, C7 = counts_A(tr7), counts_B(tr7)
s7 = {a: two(f'seed 7 alpha {a}', nll_A(probs(N7, a), dv7), nll_B(C7, dv7, a), 1e-12) for a in (0.01, 0.1, 0.3, 1, 3, 10)}
best7 = min(s7, key=s7.get); lv.claim(best7 == 0.3 and round(s7[0.3], 4) == 2.4629 and round(s7[1], 4) == 2.463, 'seed 7: 0.3 best with 2.4629, 1 gives 2.4630')
E('homework', 'items[0].explain.text', 2.4629)
E('homework', 'items[3].widget.answer', round(206.5 / 285.5, 4)); E('homework', 'items[3].widget.wrong[0].value', round(206 / 272, 4)); E('homework', 'items[3].widget.wrong[1].value', round(206.5 / 272.5, 4))
lv.claim(Ns[1, 0] == 105 and Ns[1, 14] == 81, '500 names: a then end 105, a then n 81')
E('homework', 'items[4].widget.answer', round(math.log(105 / 81), 4)); E('homework', 'items[4].widget.wrong[0].value', round(105 / 81, 4))
E('homework', 'items[5].model', 2.382); E('homework', 'items[5].model', 2.4122); E('homework', 'items[5].model', 2.383)
lv.claim(sum(r['points'] for r in lv.files['homework-1']['items'][5]['rubric']) == 10, 'longform rubric sums to 10')
lv.claim(round(nll_A(probs(Nt, 1), dv), 4) == 2.4514, 'performance task: dev loss 2.4514')

# ---------------- problems-1 ----------------
n8 = ['amy', 'may', 'mae', 'ama', 'mya', 'emma', 'yam', 'maya']; C8 = counts_B(n8)
rowt = lambda a: sum(v for (x, _), v in C8.items() if x == a)
lv.claim((rowt('.'), C8[('.', 'm')], rowt('m'), C8[('m', 'a')], rowt('a'), C8[('a', 'y')], rowt('y'), C8[('y', '.')]) == (8, 4, 9, 5, 10, 2, 5, 2), 'eight names: the row counts quoted')
E('problems', 'items[0].parts[0].widget.answer', rowt('m')); E('problems', 'items[0].parts[1].widget.answer', round(6 / 36, 4))
E('problems', 'items[0].parts[1].widget.wrong[0].value', round(5 / 9, 4))
P8 = probs(counts_A(n8), 1); may = nll_A(P8, ['may']); mayB = nll_B(C8, ['may'], 1); two('may loss', may, mayB, 1e-12)
E('problems', 'items[0].parts[2].widget.answer', round(may, 4)); E('problems', 'items[0].parts[2].widget.wrong[1].value', round(4 * may, 4))
mle = -(math.log(4 / 8) + math.log(5 / 9) + math.log(2 / 10) + math.log(2 / 5)) / 4; E('problems', 'items[0].parts[2].widget.wrong[0].value', round(mle, 4))
E('problems', 'items[0].parts[3].widget.answer', round(round(may, 4) / math.log(2), 4)); E('problems', 'items[0].parts[3].widget.wrong[0].value', round(2.1543 * math.log(2), 4))
E('problems', 'items[0].parts[4].widget.answer', round(math.exp(2.1543), 2)); E('problems', 'items[0].parts[4].widget.wrong[0].value', round(2 ** 2.1543, 2))
E('problems', 'items[1].parts[0].widget.answer', round(math.log(4), 4)); E('problems', 'items[1].parts[0].widget.wrong[0].value', round(math.log(3), 4))
xp = np.array([1, 1, 1]); yp = np.array([2, 2, 3]); Wp = Tensor(np.zeros((4, 4))); cross_entropy(Wp[xp], yp).backward()
E('problems', 'items[1].parts[1].widget.answer', round(float(Wp.grad[1, 2]), 4)); E('problems', 'items[1].parts[1].widget.wrong[0].value', round(3 * float(Wp.grad[1, 2]), 4))
sgd_step([Wp], 2.0); E('problems', 'items[1].parts[2].widget.answer', round(float(Wp.data[1, 2]), 4))
E('problems', 'items[1].parts[3].widget.answer', round(math.log(2), 4))
perm5 = np.random.default_rng(5).permutation(len(W)); tr5 = [W[i] for i in perm5[:25626]]; dv5 = [W[i] for i in perm5[25626:28829]]
N5, C5 = counts_A(tr5), counts_B(tr5)
s5 = {a: two(f'seed 5 alpha {a}', nll_A(probs(N5, a), dv5), nll_B(C5, dv5, a), 1e-12) for a in (0.01, 0.1, 0.3, 1, 3, 10)}
for a, v in s5.items():
    E('problems', 'items[2].prose', round(v, 4))
lv.claim(min(s5, key=s5.get) == 0.3 and nll_A(probs(N5, 0), dv5) == math.inf, 'seed 5: 0.3 best; alpha 0 infinite')
E('problems', 'items[2].parts[1].widget.answer', round(math.exp(2.4623), 2)); E('problems', 'items[2].parts[2].widget.answer', round(2.4623 / math.log(2), 4))
E('problems', 'items[2].parts[2].widget.wrong[0].value', round(2.4623 * math.log(2), 4)); E('problems', 'items[2].parts[1].widget.wrong[0].value', round(2 ** 2.4623, 2))

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
lv.claim(len(shipped) >= 1 and all(hashlib.sha256(s.encode('utf8')).hexdigest() == sha for s in shipped), f'every shipped autograd.py ({len(shipped)}) is byte-identical')


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
        with np.errstate(all='ignore'):
            for i, t in enumerate(w['tests']):
                if not passes(t, ns):
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
