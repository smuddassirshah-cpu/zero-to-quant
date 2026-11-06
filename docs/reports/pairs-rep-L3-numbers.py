"""pairs-rep level 3: recompute every stated number by a second route and check it at its JSON path. Exit 0 when all pass.

Needs NumPy and statsmodels. Route 1 is the lesson code (Pyodide in the playthrough, CPython in the builders). Route 2 is
this file: the day-by-day state machine of pairs_rep_common.py for distance trading, its own loops for convergence and for
trading a cointegration residual, OLS by hand with NumPy, and statsmodels' coint called directly. Every code widget is run
in CPython: the solution must pass every hidden test and the starter must fail at least one. Takes a few minutes.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
import numpy as np
from numbers_lib import Level
from pairs_rep_common import CLOSE, MKT, BROKEN, pairs_panel, closest, trade, cycle, ssd_all, _close, _widgets
from statsmodels.tsa.stattools import coint

lv = Level("pairs-rep", 3)
C = CLOSE
M = np.exp(MKT)
E = lv.expect
STARTS = list(range(0, 2647, 21))
S126 = list(range(0, 2647, 126))
pre_of = lambda st: st + 378 <= 1512
post_of = lambda st: st + 252 >= 1512
planted = lambda prs: sum(1 for i, j in prs if j == i + 1 and i % 2 == 0 and i < 40)
UNB = {(8, 9), (14, 15), (32, 33)}


def rec(ok, label):
    lv._rec(bool(ok), label, '')


def window(px, st):
    P = px[st:st + 378] / px[st]
    return P[:252], P[252:]


# ---------------------------------------------------------------- shared runs (distance, by the common state machine)
runs = {}
for k in (20, 5):
    for w in (0, 1):
        runs[(k, w)] = [(st, cycle(C, st, k, w)[0]) for st in STARTS]
def split(res):
    return (np.mean([r for s, r in res if pre_of(s)]) / 6, np.mean([r for s, r in res if post_of(s)]) / 6)
SP = {kw: split(v) for kw, v in runs.items()}
pre, post = SP[(20, 0)]; prew, postw = SP[(20, 1)]; pre5, post5 = SP[(5, 0)]; pre5w, post5w = SP[(5, 1)]
m_s = np.mean([r for _, r in runs[(20, 0)]]) / 6; m_w = np.mean([r for _, r in runs[(20, 1)]]) / 6
rec(sum(pre_of(s) for s in STARTS) == 55 and sum(post_of(s) for s in STARTS) == 67, "55 cycles before, 67 after, 5 straddle")


def trips_conv(form, tr, i, j, wait=0, m=2.0):
    """Second state machine: (payoff, converged) per round trip; converged means the prices crossed."""
    sd = float(np.std(form[:, i] - form[:, j])); s = tr[:, i] - tr[:, j]; n = len(s); out = []; t = 0
    while t < n:
        if abs(s[t]) > m * sd and t + wait < n - 1:
            side = 1 if s[t] > 0 else -1
            cross = next((u for u in range(t + 1, n) if s[u] * side <= 0), None)
            en = t + wait; ex = n - 1 if cross is None else min(cross + wait, n - 1)
            out.append((side * ((tr[ex, j] / tr[en, j] - 1) - (tr[ex, i] / tr[en, i] - 1)), cross is not None))
            t = ex + 1
        else:
            t += 1
    return out


# ================================================================ l11
E("l11", "screens[0].canvas.state.caption", round(pre * 100, 2)); E("l11", "screens[0].canvas.state.caption", round(post * 100, 2))
E("l11", "screens[0].explain.text", round(prew * 100, 2)); E("l11", "screens[0].explain.text", round(postw * 100, 2))
roll = lambda v: [np.mean(v[t - 11:t + 1]) for t in range(11, len(v))]
v20 = [r for _, r in runs[(20, 0)]]; v20w = [r for _, r in runs[(20, 1)]]
rec(max(roll(v20)[60:]) < pre * 6 and max(roll(v20w)[60:]) < prew * 6, "l11 explore: no 12-cycle window wholly after the break regains the pre-break mean")
surv = post / pre
E("l11", "screens[1].widget.answer", round(surv, 4)); E("l11", "screens[1].explain.text", round(surv * 100))
E("l11", "screens[1].widget.wrong[0].value", round(1 - surv, 4)); E("l11", "screens[1].widget.wrong[1].value", round(pre - post, 4))
for r, (a, b) in enumerate([(pre, post), (prew, postw), (pre5, post5), (pre5w, post5w)]):
    E("l11", f"screens[1].canvas.params.rows[{r}][1]", round(a * 100, 2)); E("l11", f"screens[1].canvas.params.rows[{r}][2]", round(b * 100, 2))
rec(abs(pre - 0.0150) < 5e-5 and abs(post - 0.0064) < 5e-5 and abs(prew - 0.0114) < 5e-5 and abs(postw - 0.0048) < 5e-5, "brief reference 1.50/0.64 and 1.14/0.48")
rec(abs(pre5 - 0.0168) < 5e-5 and abs(post5 - 0.0119) < 5e-5 and abs(pre5w - 0.0128) < 5e-5 and abs(post5w - 0.0088) < 5e-5, "brief reference top 5 1.68/1.19 and 1.28/0.88")
PL = {st: planted(closest(window(C, st)[0], 20)) for st in (0, 1134, 1512, 2016, 2646)}
rec([PL[s] for s in (0, 1134, 1512, 2016, 2646)] == [20, 16, 4, 3, 3], "planted in the top 20: 20, 16, 4, 3, 3")
E("l11", "screens[2].widget.answer", 20 - PL[2016]); E("l11", "screens[2].widget.wrong[0].value", PL[2016])
for st in (0, 1134, 1512, 2016, 2646):
    E("l11", f"screens[2].canvas.state.values.s{st}", PL[st])
cv = {}
for w in (0, 1):
    for lab, f in (('pre', pre_of), ('post', post_of)):
        c = n = 0
        for st in STARTS:
            if f(st):
                fo, tr = window(C, st)
                T = [x for i, j in closest(fo, 20) for x in trips_conv(fo, tr, i, j, w)]
                c += sum(x[1] for x in T); n += len(T)
        cv[(lab, w)] = (c, n)
cpre, cpost = cv[('pre', 0)][0] / cv[('pre', 0)][1], cv[('post', 0)][0] / cv[('post', 0)][1]
E("l11", "screens[3].widget.answer", round(cpost, 4)); E("l11", "screens[3].widget.wrong[0].value", round(1 - cpost, 4)); E("l11", "screens[3].widget.wrong[1].value", round(cpre, 4))
for key, (lab, w) in (("pre", ('pre', 0)), ("post", ('post', 0))):
    E("l11", f"screens[3].canvas.state.values.{key}", round(cv[(lab, w)][0] / cv[(lab, w)][1], 4))
for lab in ('pre', 'post'):
    for w in (0, 1):
        E("l11", "screens[3].canvas", cv[(lab, w)][0]); E("l11", "screens[3].canvas", cv[(lab, w)][1])
E("l11", "screens[3].explain.text", round(cpre * 100)); E("l11", "screens[3].explain.text", round(cpost * 100))
E("l11", "screens[5].explain.text", round(cpre * 100)); E("l11", "screens[5].explain.text", round(cpost * 100))
C3, _, _, B3, _ = pairs_panel(break_frac=0.3)
rec(int(B3.sum()) == 9, "break_frac 0.3 breaks 9 pairs")
r3 = [(st, cycle(C3, st, 20, 0)[0]) for st in STARTS]
b3pre, b3post = split(r3)
E("l11", "screens[4].explain.text", round(b3post * 100, 2)); E("l11", "screens[4].explain.text", round(b3pre * 100, 2))
E("l11", "screens[4].explain.text", planted(closest(window(C3, 1512)[0], 20))); E("l11", "screens[4].explain.text", planted(closest(window(C3, 2016)[0], 20)))
kinds = {}
for st in STARTS:
    if post_of(st):
        fo, tr = window(C, st)
        for i, j in closest(fo, 20):
            T = trips_conv(fo, tr, i, j, 0)
            kd = 'unb' if (i, j) in UNB else ('brk' if planted([(i, j)]) else 'ch')
            a = kinds.setdefault(kd, [0, 0.0, 0, 0]); a[0] += 1; a[1] += sum(x[0] for x in T); a[2] += sum(x[1] for x in T); a[3] += len(T)
unb_pre = [sum(x[0] for x in trips_conv(*window(C, st), i, j, 0)) for st in STARTS if pre_of(st) for i, j in closest(window(C, st)[0], 20) if (i, j) in UNB]
for r, kd in enumerate(('unb', 'brk', 'ch')):
    n_, pay, cc, nt = kinds[kd]
    E("l11", f"screens[6].canvas.params.rows[{r}][1]", n_); E("l11", f"screens[6].canvas.params.rows[{r}][2]", round(pay / n_ * 100, 2)); E("l11", f"screens[6].canvas.params.rows[{r}][3]", round(cc / nt * 100))
ratio = (kinds['unb'][1] / kinds['unb'][0]) / (kinds['ch'][1] / kinds['ch'][0])
E("l11", "screens[6].widget.answer", round(0.1045 / 0.0237, 2)); rec(abs(ratio - 0.1045 / 0.0237) < 0.05, "l11 ratio from unrounded payoffs within 0.05 of the stated 4.41")
E("l11", "screens[6].explain.text", round(np.mean(unb_pre) * 100, 2)); E("l11", "screens[6].explain.text", round(ratio, 1))
r126 = [(st, cycle(C, st, 20, 0)[0]) for st in S126]
s126 = split(r126)
E("l11", "screens[7].widget.tests[5].expect", round(s126[0], 6)); E("l11", "screens[7].widget.tests[5].expect", round(s126[1], 6))
E("l11", "screens[7].explain.text", round(s126[0] * 100, 2)); E("l11", "screens[7].explain.text", round(s126[1] * 100, 2))
def conv_share(st, k, w):
    fo, tr = window(C, st); T = [x for i, j in closest(fo, k) for x in trips_conv(fo, tr, i, j, w)]
    return sum(x[1] for x in T), len(T)
for t_, (st, k, w) in enumerate([(0, 20, 0), (2016, 20, 0), (2016, 5, 0), (2016, 20, 1), (0, 1, 0)]):
    c_, n_ = conv_share(st, k, w)
    E("l11", f"screens[8].widget.tests[{t_}].expect", round(c_ / n_, 6))
c0, n0 = conv_share(0, 20, 0); c16, n16 = conv_share(2016, 20, 0)
for v in (c0, n0, round(100 * c0 / n0), c16, n16, round(100 * c16 / n16)):
    E("l11", "screens[8].explain.text", v)
E("l11", "screens[9].widget.answer", round(postw / prew, 4)); E("l11", "screens[9].explain.text", round(100 * postw / prew)); E("l11", "screens[9].explain.text", round(100 * surv))
E("l11", "quiz[0].widget.answer", round(post5 / pre5, 4)); E("l11", "quiz[0].explain.text", round(100 * post5 / pre5))
E("l11", "quiz[2].widget.answer", 18 / 30)
E("l11", "summary.ideas[1]", round(cpost * 100)); E("l11", "summary.ideas[0]", round(surv * 100))

# ================================================================ l12
F0, T0 = window(C, 0); L0 = np.log(F0)
D0 = ssd_all(F0)
cand0 = closest(F0, 50)
pv = lambda L, i, j: round(float(coint(L[:, i], L[:, j], trend='c', autolag='aic')[1]), 4)
p0 = {p: pv(L0, *p) for p in cand0}
for p, r in (((38, 39), 2), ((28, 87), 23)):
    rec(cand0.index(p) + 1 == r, f"l12 pair {p} ranks {r} by distance")
    E("l12", "screens[0].canvas.state.caption" if p == (38, 39) else "screens[0].explain.text", p0[p])
E("l12", "screens[0].canvas.controls", round(D0[38, 39], 4)); E("l12", "screens[0].canvas.controls", round(D0[28, 87], 4))
fails = [r for r, p in enumerate(cand0[:20]) if p0[p] >= 0.05]
rec(lv.files['l12-cointegration-selection']['screens'][1]['widget']['answer'] == [f"r{r}" for r in fails], "l12 tap answer is every row with p >= 0.05")
for r, p in enumerate(cand0[:20]):
    E("l12", f"screens[1].canvas.params.rows[{r}][3]", p0[p]); E("l12", f"screens[1].canvas.params.rows[{r}][2]", round(D0[p], 4))
E("l12", "screens[1].explain.text", len(fails)); E("l12", "screens[1].explain.text", max(p0[p] for p in cand0[:20]))


def eg_pick(px, st, nc=50, k=20):
    fo, tr = window(px, st); L = np.log(fo); cand = closest(fo, nc)
    ps = [pv(L, i, j) for i, j in cand]
    order = sorted(range(len(cand)), key=lambda q: (ps[q], q))[:k]
    return [cand[q] for q in order], cand[:k], fo, tr


def trade_resid(fo, tr, i, j, entry=2.0):
    """Second route for trading a cointegration residual: open at |z| >= entry, close when z reaches 0 or on the last day."""
    y, x = np.log(fo[:, i]), np.log(fo[:, j])
    X = np.column_stack([np.ones(252), x]); a, b = np.linalg.lstsq(X, y, rcond=None)[0]
    b, a = round(float(b), 6), round(float(a), 6)
    sd = float(np.std(y - a - b * x))
    z = (np.log(tr[:, i]) - a - b * np.log(tr[:, j])) / sd
    n = len(z); pay = 0.0; t = 0
    while t < n - 1:
        if abs(z[t]) >= entry:
            side = -1 if z[t] > 0 else 1
            ex = next((u for u in range(t + 1, n) if z[u] * side >= 0), n - 1)
            pay += side * ((tr[ex, i] / tr[t, i] - 1) - b * (tr[ex, j] / tr[t, j] - 1))
            t = ex + 1
        else:
            t += 1
    return pay


cmp = {}
for st in (0, 2016, 1134):
    eg, ds, fo, tr = eg_pick(C, st)
    cmp[st] = (planted(ds), planted(eg), sum(trade(fo, tr, i, j)[0] for i, j in ds) / 20, sum(trade_resid(fo, tr, i, j) for i, j in eg) / 20, eg)
E("l12", "screens[2].canvas.params.rows[0][1]", cmp[0][0]); E("l12", "screens[2].canvas.params.rows[1][1]", cmp[0][1])
E("l12", "screens[2].canvas.params.rows[0][2]", cmp[2016][0]); E("l12", "screens[2].canvas.params.rows[1][2]", cmp[2016][1])
E("l12", "screens[2].canvas.params.rows[0][3]", round(cmp[0][2] * 100, 2)); E("l12", "screens[2].canvas.params.rows[1][3]", round(cmp[0][3] * 100, 2))
E("l12", "screens[2].widget.answer", 20 - cmp[0][1]); E("l12", "screens[2].widget.wrong[0].value", 20 - cmp[2016][1])
eg126, ds126 = [], []
for st in S126:
    eg, ds, fo, tr = eg_pick(C, st)
    eg126.append(sum(trade_resid(fo, tr, i, j) for i, j in eg) / 20); ds126.append(sum(trade(fo, tr, i, j)[0] for i, j in ds) / 20)
EG_ALL, DS_ALL = np.mean(eg126) / 6, np.mean(ds126) / 6
E("l12", "screens[2].explain.text", round(EG_ALL * 100, 2)); E("l12", "screens[2].explain.text", round(DS_ALL * 100, 2))
E("l12", "summary.ideas[1]", round(EG_ALL * 100, 2)); E("l12", "summary.ideas[1]", round(DS_ALL * 100, 2))
E("l12", "screens[4].widget.answer", 4950 * 0.05)
allp = [pv(L0, i, j) for i in range(100) for j in range(i + 1, 100)]
pairs_all = [(i, j) for i in range(100) for j in range(i + 1, 100)]
sig = [pairs_all[q] for q, p in enumerate(allp) if p < 0.05]
E("l12", "screens[4].explain.text", len(sig)); E("l12", "screens[4].explain.text", planted(sig))
hist = np.histogram(allp, bins=np.linspace(0, 1, 21))[0].tolist()
for k_, v in enumerate(hist):
    E("l12", f"screens[4].canvas.state.values.b{k_}", v)
F1, T1 = window(C, 1260); L1 = np.log(F1)
pt = pv(L1, 12, 13)
X = np.column_stack([np.ones(252), L1[:, 13]]); a1, b1 = np.linalg.lstsq(X, L1[:, 12], rcond=None)[0]
b1, a1 = round(float(b1), 6), round(float(a1), 6)
res = np.log(np.vstack([F1, T1])[:, 12]) - a1 - b1 * np.log(np.vstack([F1, T1])[:, 13]); z1 = res / np.std(res[:252])
E("l12", "screens[5].prose", pt); E("l12", "screens[5].explain.text", round(float(z1[252:].min()), 1)); E("l12", "screens[5].explain.text", round(float(z1[-1]), 1))
eg1260 = eg_pick(C, 1260)[0]
brk1260 = [p for p in eg1260 if planted([p]) and BROKEN[p[0] // 2]]
E("l12", "quiz[2].widget.options[2].why", len(brk1260))
lx = np.log(F0[:, 2]); ly = 2 * lx + (np.log(F0[:, 3]) - lx)
toy_ssd = float(((np.exp(ly) - F0[:, 2]) ** 2).sum())
iu = np.triu_indices(100, 1); dsort = np.sort(D0[iu])
toy_rank = int((dsort < toy_ssd).sum()) + 1
toy_beta = float(np.linalg.lstsq(np.column_stack([np.ones(252), lx]), ly, rcond=None)[0][1])
E("l12", "screens[6].canvas.params.rows[0][1]", round(toy_ssd, 2)); E("l12", "screens[6].canvas.params.rows[0][2]", toy_rank)
E("l12", "screens[6].canvas.params.rows[0][3]", pv(np.column_stack([ly, lx]), 0, 1)); E("l12", "screens[6].canvas.params.rows[1][1]", round(float(dsort[19]), 4))
E("l12", "screens[6].explain.text", round(toy_beta, 2)); E("l12", "screens[6].widget.accept", round(toy_beta, 2))
for t_, p in enumerate([(2, 3), (38, 39), (28, 87), (4, 5)]):
    E("l12", f"screens[7].widget.tests[{t_}].expect", p0[p])
E("l12", "screens[7].explain.text", p0[(2, 3)]); E("l12", "screens[7].explain.text", p0[(4, 5)])
eg0 = cmp[0][4]; eg16 = cmp[2016][4]
rec(lv.text("l12", "screens[8].widget.tests[2].expect") == str([list(p) for p in eg0[:5]]), "l12 coint_pairs first five at start 0")
rec(lv.text("l12", "screens[8].widget.tests[3].expect") == str(list(eg0[19])), "l12 coint_pairs 20th at start 0")
rec(lv.text("l12", "screens[8].widget.tests[5].expect") == str([list(p) for p in eg16[:3]]), "l12 coint_pairs first three at start 2,016")
E("l12", "screens[8].widget.tests[1].expect", 190 * 0.01); E("l12", "screens[9].widget.answer", 50 * 0.05)
E("l12", "screens[10].prose", 300 * 299 // 2); E("l12", "screens[10].hints[1].text", 300 * 299 // 2 * 0.05)
E("l12", "quiz[0].widget.answer", 1000 * 0.01)

# ================================================================ l13
def ols(y, x):
    y = np.asarray(y); X = np.column_stack([np.ones(len(x)), x]); b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b; s2 = e @ e / (len(y) - 2); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - e @ e / ((y - y.mean()) @ (y - y.mean()))
    return b[0], b[1], b[0] / se[0], b[1] / se[1], r2, se[0], se[1]
x22 = [M[s + 377] / M[s + 252] - 1 for s in S126]
y22 = [r for _, r in r126]; y22w = [cycle(C, st, 20, 1)[0] for st in S126]
al, be, ta, tb, r2, sa, sb = ols(y22, x22)
alw, bew, taw = ols(y22w, x22)[:3]
x127 = [M[s + 377] / M[s + 252] - 1 for s in STARTS]
ta127 = ols(v20, x127)[2]
for r, vals in enumerate([(al, sa, ta), (be, sb, tb)]):
    E("l13", f"screens[1].canvas.params.rows[{r}][1]", round(vals[0], 4)); E("l13", f"screens[1].canvas.params.rows[{r}][2]", round(vals[1], 4)); E("l13", f"screens[1].canvas.params.rows[{r}][3]", round(vals[2], 2))
E("l13", "screens[1].canvas.state.caption", round(r2, 3)); E("l13", "screens[1].explain.text", round(r2 * 100))
E("l13", "screens[1].widget.answer", round(round(al, 4) / 6, 4)); E("l13", "screens[1].widget.wrong[0].value", round(al, 4)); E("l13", "screens[1].widget.wrong[1].value", round(be, 4))
E("l13", "screens[0].explain.text", round(be, 3))
pred = round(al, 4) + round(be, 4) * -0.10
E("l13", "screens[3].widget.answer", round(pred, 4)); E("l13", "screens[3].widget.wrong[0].value", round(round(be, 4) * -0.10, 4)); E("l13", "screens[3].widget.wrong[1].value", round(round(al, 4) + round(be, 4) * 0.10, 4))
E("l13", "screens[4].prose", round(ta, 2)); E("l13", "screens[4].prose", round(ta127, 2))
negw = sum(r < 0 for _, r in runs[(20, 1)]); worstw = min(r for _, r in runs[(20, 1)])
E("l13", "screens[5].prose", negw); E("l13", "screens[5].prose", round(worstw * 100, 1)); E("l13", "screens[5].prose", round(be, 3))
def band(steps, k, lo):
    return [cycle(C, st, k, 0, lo)[0] for st in steps]
def resid(v, x):
    a_, b_ = ols(v, x)[:2]; return np.asarray(v) - a_ - b_ * np.asarray(x)
t5, b21 = band(S126, 5, 0), band(S126, 20, 20); t5b, b21b = band(STARTS, 5, 0), band(STARTS, 20, 20)
cors = [np.corrcoef(t5, b21)[0, 1], np.corrcoef(resid(t5, x22), resid(b21, x22))[0, 1], np.corrcoef(t5b, b21b)[0, 1], np.corrcoef(resid(t5b, x127), resid(b21b, x127))[0, 1]]
for q, (r, c_) in enumerate([(0, 1), (0, 2), (1, 1), (1, 2)]):
    E("l13", f"screens[6].canvas.params.rows[{r}][{c_}]", round(cors[q], 2))
E("l13", "screens[7].widget.answer", 1 - 0.60)
rec(lv.text("l13", "screens[8].widget.tests[2].expect") == str([float(round(v, 4)) for v in x22]), "l13 market_by_cycle 22-cycle list")
E("l13", "screens[8].widget.tests[3].expect", round(x127[60], 6)); E("l13", "screens[8].widget.tests[4].expect", round(378 / 253 - 1, 6))
E("l13", "screens[9].widget.tests[1].expect", round(al, 4)); E("l13", "screens[9].widget.tests[1].expect", round(be, 4)); E("l13", "screens[9].widget.tests[1].expect", round(ta, 4))
E("l13", "screens[9].widget.tests[2].expect", round(alw, 4)); E("l13", "screens[9].widget.tests[2].expect", round(bew, 4)); E("l13", "screens[9].widget.tests[2].expect", round(taw, 4))
ta_toy = ols([2.1, 2.9, 4.2, 4.8], [1, 2, 3, 4])
E("l13", "screens[9].widget.tests[0].expect", round(ta_toy[0], 4)); E("l13", "screens[9].widget.tests[0].expect", round(ta_toy[1], 4)); E("l13", "screens[9].widget.tests[0].expect", round(ta_toy[2], 4))
E("l13", "screens[9].explain.text", round(al, 4)); E("l13", "screens[9].explain.text", round(taw, 2))
E("l13", "quiz[0].widget.answer", 0.006 + 0.10 * -0.05); E("l13", "quiz[2].widget.answer", 1 - 0.70)

# ================================================================ l14
G = {}
for th in (1.5, 2.0, 2.5, 3.0):
    for k in (5, 10, 20):
        rr = [(st, cycle(C, st, k, 1, 0, th)[0]) for st in S126]
        G[(th, k)] = split(rr)
best = max(G, key=lambda x: G[x][0]); bi, bo = G[best]
rec(best == (1.5, 10), "l14 best in-sample setting is 1.5 sd, k = 10")
rec(max(G, key=lambda x: G[x][0] - G[x][1]) == best, "l14 best in-sample setting falls furthest")
rec(max(G, key=lambda x: G[x][1]) == (1.5, 5) and [x for x in G if G[x][1] > G[x][0]] == [(3.0, 5)], "l14 best held-out cell 1.5 sd k 5; only 3 sd k 5 rises")
rec(sum(1 for s in S126 if pre_of(s)) == 10 and sum(1 for s in S126 if post_of(s)) == 12, "l14: 10 in-sample and 12 held-out cycles")
E("l14", "screens[0].widget.answer", 10); E("l14", "screens[0].widget.wrong[0].value", sum(1 for s in S126 if s < 1512)); E("l14", "screens[0].widget.wrong[1].value", sum(1 for s in S126 if s + 251 <= 1511))
for r, th in enumerate((1.5, 2.0, 2.5, 3.0)):
    for c_, k in enumerate((5, 10, 20)):
        E("l14", f"screens[1].canvas.params.rows[{r}][{c_ + 1}]", round(G[(th, k)][0] * 100, 2))
srt = sorted(G, key=lambda x: -G[x][0])
for r, x in enumerate(srt):
    E("l14", f"screens[3].canvas.params.rows[{r}][1]", round(G[x][0] * 100, 2)); E("l14", f"screens[3].canvas.params.rows[{r}][2]", round(G[x][1] * 100, 2))
E("l14", "screens[2].widget.answer", round(bo / bi, 4)); E("l14", "screens[2].explain.text", round(100 * bo / bi))
E("l14", "screens[3].widget.answer", round(bi - bo, 4)); E("l14", "screens[3].explain.text", round((bi - bo) * 100, 2))
E("l14", "screens[4].widget.answer", round(postw / prew, 4)); E("l14", "screens[4].explain.text", round(100 * G[(2.0, 20)][1] / G[(2.0, 20)][0]))
E("l14", "screens[4].canvas.params.rows[1][1]", round(G[(2.0, 20)][0] * 100, 2)); E("l14", "screens[4].canvas.params.rows[1][2]", round(G[(2.0, 20)][1] * 100, 2))
E("l14", "screens[5].prose", round(G[(1.5, 5)][1] * 100, 2))
E("l14", "screens[6].prose", round(G[(3.0, 5)][0] * 100, 2)); E("l14", "screens[6].prose", round(G[(3.0, 5)][1] * 100, 2))
E("l14", "screens[7].widget.tests[0].expect", round(G[(2.0, 20)][0], 6)); E("l14", "screens[7].widget.tests[1].expect", round(G[(1.5, 10)][0], 6)); E("l14", "screens[7].widget.tests[2].expect", round(G[(3.0, 5)][0], 6))
E("l14", "screens[8].widget.tests[0].expect", round(G[(2.0, 20)][1], 6)); E("l14", "screens[8].widget.tests[1].expect", round(bo, 6)); E("l14", "screens[8].widget.tests[2].expect", round(G[(3.0, 5)][1], 6))
E("l14", "screens[10].widget.options[0].text", round(100 * postw / prew))
E("l14", "quiz[0].widget.answer", 0.60 / 1.60); E("l14", "quiz[2].widget.answer", sum(1 for s in range(0, 3024, 126) if s + 378 <= 1008))

# ================================================================ l15
cyc_w = m_w * 6; ann_w = (1 + m_w) ** 12 - 1
trips = []
for st in STARTS:
    fo, tr = window(C, st)
    trips += [trade(fo, tr, i, j, 1)[2] for i, j in closest(fo, 20)]
TR = np.mean(trips)
E("l15", "screens[2].widget.rows[3][1]", round(TR, 4)); be_cost = cyc_w / (4 * TR)
E("l15", "screens[0].widget.answer", round(post5w / pre5w, 4)); E("l15", "screens[0].explain.text", round(100 * postw / prew))
E("l15", "screens[2].widget.rows[0][2].answer", round(m_w, 5)); E("l15", "screens[2].widget.rows[1][2].answer", round(ann_w, 4))
E("l15", "screens[2].widget.rows[2][2].answer", round(postw / prew, 4)); E("l15", "screens[2].widget.rows[3][2].answer", round(be_cost, 5))
E("l15", "screens[2].explain.text", round(ann_w * 100, 1)); E("l15", "screens[2].explain.text", round(be_cost * 100, 2))
E("l15", "screens[1].canvas.params.lines[1]", round(m_w * 100, 2)); E("l15", "screens[1].canvas.params.lines[2]", round(m_s * 100, 2))
E("l15", "screens[1].canvas.params.lines[3]", round(be_cost * 100, 2)); E("l15", "screens[1].canvas.params.lines[7]", round(EG_ALL * 100, 2))
E("l15", "screens[1].canvas.params.lines[6]", round(be, 2)); E("l15", "screens[1].canvas.params.lines[6]", round(tb, 2))
E("l15", "screens[3].widget.options[2].text", round((prew - postw) * 100, 2))
E("l15", "screens[4].prose", 5000 * 4999 // 2); E("l15", "screens[4].prose", round(5000 * 4999 / 2 / 4950))
E("l15", "screens[5].prose", round(pre * 100, 2))
E("l15", "screens[9].widget.options[0].text", round(m_w * 100, 2)); E("l15", "screens[9].widget.options[2].text", round(bi * 100, 2))
E("l15", "quiz[0].widget.answer", 0.36 / 0.90)

# ================================================================ review and homework
E("review", "items[0].widget.answer", 0.54 / 1.20); E("review", "items[2].widget.answer", round(51 / 90, 4)); E("review", "items[2].widget.wrong[0].value", (26 / 40 + 25 / 50) / 2)
E("review", "items[3].widget.answer", 190 * 0.05); E("review", "items[4].explain.text", toy_rank)
E("review", "items[5].prose", 20 - cmp[0][1]); E("review", "items[5].widget.options[2].why", len(fails))
E("review", "items[6].widget.answer", round(round(al, 4) + round(be, 4) * 0.15, 4)); E("review", "items[7].widget.answer", 1 - 1.25)
hw = {}
for st, nc, k in ((0, 50, 20), (2016, 50, 20), (0, 50, 5), (1134, 50, 20)):
    eg, ds, fo, tr = eg_pick(C, st, nc, k)
    hw[(st, nc, k)] = [planted(ds), planted(eg), float(round(sum(trade(fo, tr, i, j)[0] for i, j in ds) / k, 4)), float(round(sum(trade_resid(fo, tr, i, j) for i, j in eg) / k, 4))]
for t_, key in enumerate(((0, 50, 20), (2016, 50, 20), (0, 50, 5), (1134, 50, 20))):
    rec(lv.text("homework", f"items[0].widget.tests[{t_}].expect") == str(hw[key]), f"homework compare_selection {key} = {hw[key]}")
for key in ((0, 50, 20), (2016, 50, 20), (0, 50, 5)):
    E("homework", "items[0].explain.text", round(hw[key][2] * 100, 2)); E("homework", "items[0].explain.text", round(hw[key][3] * 100, 2))
yw = [cycle(C, st, 20, 1)[0] for st in S126]
hit = [round(sum(1 for r in yw[t - 5:t + 1] if r > 0) / 6, 4) for t in range(5, 22)]
rec(lv.text("homework", "items[1].widget.tests[4].expect") == str(hit), "homework rolling hit rate on the 22 waited cycles")
E("homework", "items[2].explain.text", round(100 * bo / bi)); E("homework", "items[2].explain.text", round(100 * postw / prew))
E("homework", "items[3].widget.answer", round((3 * 0.1045 + 17 * 0.0237) / 20, 4)); E("homework", "items[3].prose", round(kinds['unb'][1] / kinds['unb'][0] * 100, 2)); E("homework", "items[3].prose", round(kinds['ch'][1] / kinds['ch'][0] * 100, 2))
E("homework", "items[4].widget.answer", 10 * 45 * 0.05); E("homework", "items[5].explain.text", round(ta127, 2)); E("homework", "items[5].explain.text", round(ta, 2))
note = lv.text("homework", "items[6].model")
for v in (round(m_w * 100, 2), round(ann_w * 100, 1), round(prew * 100, 2), round(postw * 100, 2), round(100 * postw / prew), round(100 * bo / bi),
          round(cpost * 100), round(cpre * 100), round(EG_ALL * 100, 2), round(DS_ALL * 100, 2), round(be, 3), round(ta, 2), round(m_s * 100, 2), round(be_cost * 100, 2)):
    E("homework", "items[6].model", v)


# ---------------------------------------------------------------- further stated figures
E("l11", "summary.ideas[0]", round(pre * 100, 2)); E("l11", "summary.ideas[0]", round(post * 100, 2)); E("l11", "summary.ideas[1]", round(cpre * 100))
E("l12", "screens[0].widget.options[1].why", p0[(38, 39)]); E("l12", "screens[0].widget.options[2].why", p0[(28, 87)])
E("l12", "screens[8].explain.text", 50 * 0.05); E("l12", "screens[4].explain.text", round(4950 * 0.05))
E("l13", "screens[6].widget.options[2].why", round(cors[1], 2)); E("l13", "screens[6].explain.text", round(cors[1], 2)); E("l13", "screens[6].explain.text", round(cors[3], 2))
E("l13", "screens[6].widget.options[3].why", round(cors[0], 2)); E("l13", "summary.ideas[0]", round(ta, 2)); E("l13", "summary.ideas[0]", round(be, 3))
E("l14", "screens[1].feedback.byKey.r0c1", round(G[(1.5, 5)][0] * 100, 2)); E("l14", "screens[1].explain.text", round(bi * 100, 2))
E("l14", "screens[9].explain.text", round(bi * 100, 2)); E("l14", "screens[9].explain.text", round(bo * 100, 2)); E("l14", "screens[9].explain.text", round(100 * postw / prew))
E("l14", "summary.ideas[1]", round(100 * bo / bi)); E("l14", "summary.ideas[2]", round(100 * postw / prew))
E("l15", "summary.ideas[1]", round(m_w * 100, 2)); E("l15", "summary.ideas[1]", round(100 * postw / prew))
E("l15", "screens[8].explain.text", round(100 * 0.0048 / 0.0114)); E("l15", "screens[3].widget.options[0].text", round(100 * postw / prew))
E("homework", "items[5].explain.text", round(be, 3)); E("homework", "items[1].explain.text", round(hit[-3], 2)); E("homework", "items[1].explain.text", round(hit[-1], 2))


c5 = closest(F0, 5)[4]
rec(c5 == (30, 31) and not trade(F0, T0, 30, 31)[1], "l12: in the first cycle the fifth-closest pair (30, 31) never opens")
n3 = sum(all(p in closest(window(C, st)[0], 5) for p in UNB) for st in STARTS if post_of(st))
rec(n3 > 67 / 2, f"l11, l15: the three unbroken pairs are all in the top 5 in {n3} of 67 post-break cycles (usually)")


# ---------------------------------------------------------------- code widgets (solutions pass, starters fail), raises supported
class _Slow(Exception):
    pass


def run_tests(w, src, limit=240):
    import signal
    def _al(*_):
        raise _Slow()
    signal.signal(signal.SIGALRM, _al); signal.alarm(limit)
    fails = 0
    try:
        ns = {'__learner_source__': src}
        exec(w.get('prelude', ''), ns)
        exec(src, ns)
        for t in w['tests']:
            try:
                if t.get('setup'):
                    exec(t['setup'], ns)
                if t.get('compare') == 'raises':
                    try:
                        eval(t['call'], ns); fails += 1
                    except Exception as e:
                        fails += not isinstance(e, eval(t['expect'], ns))
                    continue
                got = eval(t['call'], ns); exp = eval(t['expect'], ns)
                if t.get('compare', 'equal') == 'isclose':
                    tol = t.get('tol', {})
                    ok = _close(got, exp, tol.get('rel', 0 if 'abs' in tol else 1e-9), tol.get('abs', 0 if 'rel' in tol else 1e-12))
                else:
                    ok = (got.tolist() if hasattr(got, 'tolist') else got) == exp
                fails += not ok
            except _Slow:
                raise
            except Exception:
                fails += 1
    except _Slow:
        return len(w['tests'])
    except Exception:
        return len(w['tests'])
    finally:
        signal.alarm(0)
    return fails


for fid, doc in lv.files.items():
    for path, w in _widgets(doc):
        sol, st = run_tests(w, w['solution']), run_tests(w, w['starter'])
        lv._rec(sol == 0, f'{fid}{path} solution passes {len(w["tests"])} tests', '' if sol == 0 else f'{sol} failing')
        lv._rec(st > 0, f'{fid}{path} starter fails', '' if st > 0 else 'starter passes every test')

# Fix pass: starters of l12 eg_pvalue and homework rolling_hit_rate fail every hidden test.
for fid, path in (('l12-cointegration-selection', 'screens[7]'), ('homework-3', 'items[1]')):
    for p_, w in _widgets(lv.files[fid]):
        if p_.startswith(path):
            lv._rec(run_tests(w, w['starter']) == len(w['tests']), f'{fid}{p_} starter fails every test', '')
# Fix pass: the shortlist is chosen on the same formation year, so 5% understates its chance passes.
chp = [p for p in cand0 if not planted([p])]
rec(len(chp) == 30 and sum(p0[p] < 0.05 for p in chp) == 18 and sum(p0[p] < 0.01 for p in chp) == 10, "l12 shortlist: 18 of 30 chance pairs pass at 5%, 10 below 1%")
rec(len(sig) - planted(sig) == 392 and len(sig) == 407, "l12 392 chance passes of 407")
for f_, s_ in (("l12", "screens[9].explain.text"), ("l12", "screens[8].explain.text")):
    rec("18 of the shortlist's 30" in lv.text(f_, s_) or "18 of the shortlist" in lv.text(f_, s_), f"{f_} {s_} states 18 of 30")
rec("392" in lv.text("l12", "screens[4].explain.text"), "l12 screens[4] names the 392 chance passes")
rec(round(pre * 6 * 100, 1) == 9.0 and "9.0%" in lv.text("homework", "items[3].explain.text"), "homework pre-break top 20 earns 9.0% a cycle")
rec(abs(0.015011 / 1 - pre) < 5e-7 and round(100 * post / pre) == 42, "l15 survival test uses the 42% split")

lv.check_wrongs()
lv.report()
