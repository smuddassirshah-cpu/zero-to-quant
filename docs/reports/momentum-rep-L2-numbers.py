"""Recompute every number stated in momentum-rep level 2 (Data and portfolios) by two routes, and check each at its JSON path.
Run: python3 docs/reports/momentum-rep-L2-numbers.py   (needs numpy; exits 0 when every check passes)
Data: the course generator `momentum_panel`, verbatim from docs/briefs/momentum-rep.md, base panel seed 2 (500 x 300).
Route 1 is the reference form the lessons load (loop formation returns, double stable argsort, averaged weights).
Route 2 is independent: formation returns from cumulative log sums, ranks by one argsort and a scatter, the
composite as the average of each live cohort's own spread. `two(a, b)` asserts the routes agree; `lv.expect`
checks each stated value appears where it is stated. The script also runs every code widget of the level in
CPython: the solution passes its hidden tests and the starter fails at least one. Pyodide is the third route
(the playthrough runs every hidden test there).
"""
import sys, os, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("momentum-rep", 2)
E = lv.expect
fails = []


def two(name, a, b, tol=1e-10):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.shape != b.shape or not np.allclose(a, b, rtol=tol, atol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def momentum_panel(n=500, T=300, seed=2, c=0.015, e=0.03, d=0.006, nf=4, fsd=0.035,
                   c_after=None, t_pub=300, crash=None):
    TMAX, L = 480, 36
    rng = np.random.default_rng(seed)
    size = rng.normal(0.0, 1.0, n)
    sig = 0.09 - 0.02 * np.tanh(size)
    beta = rng.uniform(0.5, 1.5, n)
    lam = rng.standard_normal((n, nf))
    s = rng.standard_normal((TMAX + L, n))[:T + L] * sig
    m = (0.006 + 0.045 * rng.standard_normal(TMAX))[:T]
    F = (fsd * rng.standard_normal((TMAX, nf)))[:T]
    if crash is not None:
        m[crash - 12:crash] = -0.03; F[crash - 12:crash, 0] = -0.03
        m[crash:crash + 3] = [0.12, 0.06, 0.04]; F[crash:crash + 3, 0] = [0.12, 0.06, 0.04]
    ct = np.full(T, c)
    if c_after is not None:
        ct[t_pub:] = c_after
    cont = sum(s[L - k:L - k + T] for k in range(2, 13))
    rev = sum(s[L - k:L - k + T] for k in range(13, 37))
    idio = s[L:L + T] - e * s[L - 1:L - 1 + T] + ct[:, None] * cont - d * rev
    r = 0.004 + beta * m[:, None] + F @ lam.T + idio
    return r, size, m, F


# ---------- route 1: the reference form ----------
def f1(r, J, skip=0):
    T, n = r.shape
    f = np.full((T, n), np.nan)
    for t in range(J + skip, T):
        f[t] = np.prod(1 + r[t - skip - J:t - skip], axis=0) - 1
    return f


def w1(ft, q=10):
    n = len(ft)
    rank = np.argsort(np.argsort(ft, kind="stable"), kind="stable")
    dec = rank * q // n
    top, bot = dec == q - 1, dec == 0
    return np.where(top, 1 / top.sum(), 0.0) - np.where(bot, 1 / bot.sum(), 0.0)


def wml1(r, J, K, skip=0):
    f = f1(r, J, skip)
    W = np.zeros(r.shape)
    for s in range(J + skip, r.shape[0]):
        W[s] = w1(f[s])
    return np.array([W[t - K + 1:t + 1].mean(axis=0) @ r[t] for t in range(J + skip + K - 1, r.shape[0])])


# ---------- route 2: independent ----------
def f2(r, J, skip=0):
    c = np.vstack([np.zeros((1, r.shape[1])), np.cumsum(np.log1p(r), axis=0)])
    f = np.full(r.shape, np.nan)
    t = np.arange(J + skip, r.shape[0])
    f[t] = np.expm1(c[t - skip] - c[t - skip - J])
    return f


def ranks2(ft):
    o = np.argsort(ft, kind="mergesort")
    rk = np.empty(len(ft), int); rk[o] = np.arange(len(ft))
    return rk


def w2(ft, q=10):
    rk = ranks2(ft); n = len(ft); dec = (rk * q) // n
    w = np.zeros(n)
    w[dec == q - 1] = 1.0 / np.count_nonzero(dec == q - 1)
    w[dec == 0] = -1.0 / np.count_nonzero(dec == 0)
    return w


def wml2(r, J, K, skip=0):
    f = f2(r, J, skip)
    T = r.shape[0]
    spreads = {s: None for s in range(J + skip, T)}
    out = []
    for t in range(J + skip + K - 1, T):
        out.append(np.mean([w2(f[s]) @ r[t] for s in range(t - K + 1, t + 1)]))
    return np.array(out)


def tst(x):
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))


r, size, m, F = momentum_panel()
NT, n = r.shape
p2 = lambda v: round(100 * float(v), 2)

# ---------- l6 ----------
two('base mean', r.mean(), np.mean(r))
E('l6', 'screens[8]', p2(r.mean()))
E('l6', 'screens[8].widget.tests[2].expect', round(float(r.mean()), 6))
E('l6', 'screens[8].widget.tests[4].expect', round(float(r[100, 7]), 6))


def spread1m(panel, J=6, fn=f1, wf=w1):
    f = fn(panel, J)
    return np.mean([wf(f[t]) @ panel[t] for t in range(J, panel.shape[0])])


tot = np.log1p(r).sum(axis=0); dead = tot < np.quantile(tot, 0.2)
tot2 = np.log(np.prod(1 + r, axis=0)); dead2 = tot2 < np.sort(tot2)[99] + 1e-15  # bottom 100 of 500
two('dead mask', dead.sum(), dead2.sum())
ALL, SURV = spread1m(r), spread1m(r[:, ~dead])
two('survivor all', ALL, spread1m(r, fn=f2, wf=w2)); two('survivor surv', SURV, spread1m(r[:, ~dead2], fn=f2, wf=w2))
for path in ('screens[10]', 'screens[11].explain.text', 'quiz[1]'):
    E('l6', path, p2(ALL)); E('l6', path, p2(SURV))
E('l6', 'screens[10].canvas.params.lines[1]', round(float(ALL), 4)); E('l6', 'screens[10].canvas.params.lines[1]', round(float(SURV), 4))
E('l6', 'quiz[1].widget.answer', round(float(SURV), 4)); E('l6', 'quiz[1].widget.wrong[0].value', round(float(ALL), 4))
rs, *_ = momentum_panel(n=200, T=120)
ts = np.log1p(rs).sum(axis=0); ds = ts < np.quantile(ts, 0.2)
E('l6', 'screens[10].explain.text', p2(spread1m(rs))); E('l6', 'screens[10].explain.text', p2(spread1m(rs[:, ~ds])))
two('small survivor', spread1m(rs[:, ~ds]), spread1m(rs[:, ~ds], fn=f2, wf=w2))
# NaN ranking: argsort puts NaN last
fnan = np.array([0.05, np.nan, -0.10])
two('nan ranks', np.argsort(np.argsort(fnan, kind='stable')), [1, 2, 0])
E('l6', 'screens[7].canvas.params.lines[2]', '[1, 2, 0]')

# ---------- l7 ----------
fa, fb = f1(r, 6), f2(r, 6)
two('formation 6', np.nan_to_num(fa, nan=-9), np.nan_to_num(fb, nan=-9), 1e-9)
x, y = fb[100], r[100]
slope = np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1)
R2 = np.corrcoef(x, y)[0, 1] ** 2
two('slope', slope, np.polyfit(x, y, 1)[0], 1e-9)
E('l7', 'screens[0].canvas.state.caption', round(float(slope), 3)); E('l7', 'screens[0].canvas.state.caption', round(float(R2), 4))
E('l7', 'screens[0].explain.text', round(float(slope), 3)); E('l7', 'screens[0].question', round(float(R2), 3))


def dmeans(skip, route):
    f = (f1 if route == 1 else f2)(r, 6, skip)
    tot = np.zeros(10)
    for t in range(6 + skip, NT):
        dec = (ranks2(f[t]) if route == 2 else np.argsort(np.argsort(f[t], kind='stable'), kind='stable')) * 10 // n
        tot += np.bincount(dec, weights=r[t], minlength=10) / np.bincount(dec, minlength=10) if route == 2 else np.array([r[t][dec == k].mean() for k in range(10)])
    return tot / (NT - 6 - skip)


D0, D1 = dmeans(0, 1), dmeans(1, 1)
two('deciles no skip', D0, dmeans(0, 2), 1e-9); two('deciles skip', D1, dmeans(1, 2), 1e-9)
two('D10-D1 equals 6/1 spread', D0[9] - D0[0], ALL, 1e-9)
for k in range(10):
    E('l7', f'screens[1].canvas.state.values.d{k + 1}', p2(D0[k]))
    E('l7', f'screens[1].canvas.controls[0].frames[1].values.d{k + 1}', p2(D1[k]))
E('l7', 'screens[1].explain.text', p2(D0[9])); E('l7', 'screens[1].explain.text', p2(D1[9])); E('l7', 'screens[1].explain.text', p2(D1[0]))
E('l7', 'screens[10].explain.text', p2(D0[0])); E('l7', 'screens[10].explain.text', p2(D0[9])); E('l7', 'screens[10].explain.text', p2(D0[9] - D0[0]))
E('l7', 'quiz[3].widget.answer', round(float(D0[9] - D0[0]), 4)); E('l7', 'quiz[3].prose', p2(D0[0])); E('l7', 'quiz[3].prose', p2(D0[9]))
toy = [12, -8, 3, 25, -15, 7, 0, 18, -3, 9]
qn = [sorted(toy).index(v) * 5 // 10 + 1 for v in toy]       # distinct values, so the sorted position is the rank
for i, q in enumerate(qn):
    E('l7', f'screens[3].widget.rows[{i}][2].answer', q)
tie = np.array([0.08, 0.02, 0.08, -0.05, 0.01])
two('tie ranks', ranks2(tie), np.argsort(np.argsort(tie, kind='stable'), kind='stable'))
E('l7', 'screens[4].canvas.params.lines[2]', str(ranks2(tie).tolist()))
cnt23 = [sum(1 for k in range(23) if k * 10 // 23 == d) for d in range(10)]
E('l7', 'screens[5].widget.answer', cnt23[0]); E('l7', 'screens[5].explain.text', cnt23[9])
c = np.vstack([np.zeros((1, n)), np.cumsum(np.log1p(r), axis=0)])
LA = np.mean([w2(np.prod(1 + r[t - 5:t + 1], axis=0) - 1) @ r[t] for t in range(5, NT)])
two('lookahead', LA, np.mean([w1(np.expm1(c[t + 1] - c[t - 5])) @ r[t] for t in range(5, NT)]), 1e-9)
E('l7', 'screens[6]', p2(LA)); E('l7', 'summary.trap', p2(LA))

# ---------- l8 ----------
X1 = {K: wml1(r, 6, K) for K in (3, 6, 9, 12)}
for K in (3, 6, 9, 12):
    two(f'wml 6/{K}', X1[K], wml2(r, 6, K), 1e-9)
    E('l8', 'screens[1].explain.text', p2(X1[K].mean()))
    fr = 'screens[1].canvas.controls[0].frames[%d].caption' % ((3, 6, 9, 12).index(K))
    E('l8', fr, len(X1[K])); E('l8', fr, round(float(np.prod(1 + X1[K])), 2))
x66 = X1[6]
M66, SD66, T66 = x66.mean(), x66.std(ddof=1), tst(x66)
E('l8', 'screens[8].explain.text', 289); E('l8', 'screens[8].explain.text', p2(M66)); E('l8', 'screens[8].explain.text', p2(SD66)); E('l8', 'screens[8].explain.text', round(float(T66), 2))
E('l8', 'screens[5]', p2(6 * M66)); E('l8', 'screens[5].explain.text', p2(M66))
E('l8', 'screens[3].widget.answer', (300 - 6) // 6); E('l8', 'screens[3].prose', 289)
E('l8', 'screens[6].widget.answer', 6 + 1 + 6 - 1); E('l8', 'screens[6].explain.text', len(wml2(r, 6, 6, 1)))
W1 = np.zeros(r.shape)
for s in range(6, NT):
    W1[s] = w2(fb[s])
t0 = 150
share = next(j for j in range(n) if sum(W1[s, j] > 0 for s in range(t0 - 5, t0 + 1)) == 4)
CW = W1[t0 - 5:t0 + 1, share].sum() / 6
two('composite weight 4/300', CW, 4 / 300)
E('l8', 'screens[0].widget.answer', round(4 / 300, 5)); E('l8', 'screens[2].widget.rows[2][1].answer', round(4 / 300, 4)); E('l8', 'screens[2].widget.rows[1][1].answer', 0.1667)


def turnover(J, K, route):
    f = (f1 if route == 1 else f2)(r, J)
    W = np.zeros(r.shape)
    for s in range(J, NT):
        W[s] = (w1 if route == 1 else w2)(f[s])
    if route == 1:
        C = np.array([W[t - K + 1:t + 1].mean(axis=0) for t in range(J + K - 1, NT)])
    else:
        cs = np.vstack([np.zeros((1, n)), np.cumsum(W, axis=0)])
        C = np.array([(cs[t + 1] - cs[t - K + 1]) / K for t in range(J + K - 1, NT)])
    return np.mean([np.abs(C[i + 1] - C[i]).sum() for i in range(len(C) - 1)])


TURN = {K: turnover(6, K, 1) for K in (1, 3, 6, 12)}
for K in (1, 3, 6, 12):
    two(f'turnover K{K}', TURN[K], turnover(6, K, 2), 1e-9)
    E('l8', f'screens[4].canvas.state.values.k{K}', round(TURN[K], 3))
two('turnover 0.577 (brief)', round(TURN[6], 3), 0.577)
E('l8', 'screens[4].explain.text', round(TURN[1], 3)); E('l8', 'screens[4].explain.text', round(TURN[6], 3))
E('l8', 'screens[10].explain.text', round(TURN[6], 3)); E('l8', 'screens[10].explain.text', round(TURN[6] / 2, 3))
cost = 0.0025 * TURN[6] * 10_000_000
E('l8', 'screens[11].widget.answer', round(cost)); E('l8', 'screens[11].explain.text', round(TURN[6] * 1e7))
E('l8', 'screens[11].widget.wrong[0].value', round(2 * cost)); E('l8', 'screens[11].widget.wrong[1].value', round(cost / 2))

# ---------- l9 ----------
x11 = wml1(r, 1, 1)
two('1/1', x11, wml2(r, 1, 1), 1e-9)
for path in ('screens[0].explain.text', 'screens[9].explain.text'):
    E('l9', path, p2(x11.mean())); E('l9', path, round(float(tst(x11)), 2))
two('1/1 brief values', [round(x11.mean(), 4), round(tst(x11), 2)], [-0.0088, -2.08])
ev = np.zeros(12); cnt = 0
for s in range(6, NT - 12):
    w = w2(fb[s]); ev += np.array([w @ r[s + h] for h in range(12)]); cnt += 1
ev /= cnt
for h in range(12):
    E('l9', f'screens[1].canvas.params.series[0].values[{h}]', round(100 * float(ev[h]), 3))
E('l9', 'screens[1].explain.text', p2(ev[0])); E('l9', 'screens[1].explain.text', p2(ev[6]))
E('l9', 'screens[1].explain.text', p2(ev[:6].sum())); E('l9', 'screens[1].explain.text', p2(ev[1:7].sum()))
E('l9', 'screens[1].canvas.state.caption', cnt)
Js = Ks = (3, 6, 9, 12)
M0 = {(J, K): wml1(r, J, K).mean() for J in Js for K in Ks}
M1 = {(J, K): wml1(r, J, K, 1).mean() for J in Js for K in Ks}
for J in Js:
    for K in Ks:
        two(f'skip {J}/{K}', M1[(J, K)], wml2(r, J, K, 1).mean(), 1e-9)
D = {k: M1[k] - M0[k] for k in M0}
for i, J in enumerate(Js):
    for j, K in enumerate(Ks):
        E('l9', f'screens[5].canvas.params.rows[{i}][{j + 1}]', p2(D[(J, K)]) if abs(D[(J, K)]) >= 0.00005 else 0.0)
low = sorted(f'r{i}c{j + 1}' for i, J in enumerate(Js) for j, K in enumerate(Ks) if D[(J, K)] < -0.00005)
if sorted(json.loads(json.dumps(lv.files['l9-skip-month']['screens'][5]['widget']['answer']))) != low:
    fails.append('l9 screens[5] tap answer differs from the negative cells')
for J in Js:
    E('l9', 'screens[3].explain.text', abs(p2(D[(J, 3)])))
E('l9', 'screens[4].widget.answer', round(float(D[(3, 3)]), 4)); E('l9', 'screens[4].prose', p2(M0[(3, 3)])); E('l9', 'screens[4].prose', p2(M1[(3, 3)]))
E('l9', 'screens[8].explain.text', p2(M0[(6, 6)])); E('l9', 'screens[8].explain.text', p2(M1[(6, 6)])); E('l9', 'screens[8].explain.text', p2(D[(6, 6)]))
E('l9', 'quiz[1].widget.answer', round(float(D[(6, 6)]), 4)); E('l9', 'quiz[2].explain.text', p2(D[(3, 3)])); E('l9', 'quiz[2].explain.text', abs(p2(D[(12, 12)])))

# ---------- l10 ----------
SE66 = SD66 / math.sqrt(len(x66))
x123 = wml1(r, 12, 3); SE123 = x123.std(ddof=1) / math.sqrt(len(x123))
two('12/3', x123, wml2(r, 12, 3), 1e-9)
E('l10', 'screens[0].widget.answer', round(SE66, 5)); E('l10', 'screens[0].explain.text', round(100 * SE66, 3)); E('l10', 'screens[0].prose', p2(SD66))
E('l10', 'screens[2].widget.rows[0][4].answer', round((M66 - 0.0095) / SE66, 2)); E('l10', 'screens[2].widget.rows[1][4].answer', round((x123.mean() - 0.0131) / SE123, 2))
E('l10', 'screens[2].widget.rows[1][3]', p2(SE123))
E('l10', 'screens[1].explain.text', p2(M0[(12, 3)])); E('l10', 'screens[1].explain.text', p2(M1[(12, 3)]))
rank0 = sorted(M0, key=lambda k: -M0[k])
E('l10', 'screens[4].widget.answer', rank0.index((6, 6)) + 1)
for k in rank0[:4]:
    E('l10', 'screens[4].explain.text', p2(M0[k]))
seeds = [wml2(momentum_panel(seed=s)[0], 6, 6).mean() for s in range(1, 8)]
two('seed 2 is the base panel', seeds[1], M66, 1e-9)
two('seed range (brief)', [round(100 * min(seeds), 2), round(100 * max(seeds), 2)], [0.37, 1.46])
RS = (max(seeds) - min(seeds)) / SE66
E('l10', 'screens[5].widget.answer', round(RS, 2)); E('l10', 'screens[5].explain.text', round(RS, 1)); E('l10', 'screens[5].explain.text', p2(max(seeds) - min(seeds)))
E('l10', 'screens[5].explain.text', p2(np.std(seeds, ddof=1))); E('l10', 'screens[5].widget.wrong[0].value', p2(max(seeds) - min(seeds)))
E('l10', 'screens[8].question', p2(x123.mean())); E('l10', 'screens[8].explain.text', p2(x123.mean() - 2 * SE123)); E('l10', 'screens[8].explain.text', p2(x123.mean() + 2 * SE123))
E('l10', 'screens[7].explain.text', 1.3); two('hypothetical 1.40 gap', round((1.40 - 0.95) / 0.35, 1), 1.3)
E('l10', 'quiz[0].widget.answer', 2.0); two('quiz gap', (1.10 - 0.30) / 0.40, 2.0)

# ---------- review and homework ----------
cnt505 = [sum(1 for k in range(505) if k * 10 // 505 == d) for d in range(10)]
E('review', 'items[2].widget.answer', cnt505[0])
E('review', 'items[4].widget.answer', (5 - 2) / 50 / 12)
E('review', 'items[5].widget.answer', 300 - 12 - 1 - 12 + 1); E('review', 'items[5].explain.text', (300 - 13) // 12)
E('review', 'items[6].prose', p2(M0[(3, 3)])); E('review', 'items[6].prose', p2(M1[(12, 12)]))
E('review', 'items[7].widget.answer', round((x123.mean() - 0.0131) / SE123, 2))
NET = M66 - 0.0025 * TURN[6]
two('net of 25 bp (brief 0.82%)', round(100 * NET, 2), 0.82)
E('homework', 'items[3].widget.answer', round(float(NET), 5)); E('homework', 'items[3].explain.text', round(100 * NET, 3))
E('homework', 'items[3].prose', round(TURN[6], 3)); E('homework', 'items[3].explain.text', round(0.25 * TURN[6], 3))
E('homework', 'items[4].explain.text', round(100 * SE66, 2))

# ---------- code widgets: solution passes, starter fails ----------
def widgets(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code':
            yield o
        for v in o.values():
            yield from widgets(v)
    elif isinstance(o, list):
        for v in o:
            yield from widgets(v)


def run_case(ns, case):
    if case.get('setup'):
        exec(case['setup'], ns)
    got = eval(case['call'], ns)
    want = eval(case['expect'], ns)
    tol = case.get('tol')
    rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)

    def close(a, b):
        a = a.tolist() if hasattr(a, 'tolist') else a
        b = b.tolist() if hasattr(b, 'tolist') else b
        if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(close(p, q) for p, q in zip(a, b))
        if isinstance(a, bool) or isinstance(b, bool):
            return a == b
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    if case.get('compare', 'equal') == 'isclose':
        return close(got, want)
    g = got.tolist() if hasattr(got, 'tolist') else got
    return g == want


ncode = 0
for fid, doc in lv.files.items():
    for w in widgets(doc):
        ncode += 1
        for label, src, must in (('solution', w['solution'], True), ('starter', w['starter'], False)):
            ns = {'__learner_source__': src}
            if w.get('prelude'):
                exec(w['prelude'], ns)
            try:
                exec(src, ns)
            except Exception:
                if must:
                    fails.append(f'{fid}: solution does not load')
                continue
            res = []
            for case in w['tests']:
                try:
                    res.append(bool(run_case(ns, case)))
                except Exception:
                    res.append(False)
            if must and not all(res):
                fails.append(f'{fid}: solution fails tests {[i + 1 for i, v in enumerate(res) if not v]}')
            if not must and all(res):
                fails.append(f'{fid}: starter passes every test')
# the prelude's wml and route 2 agree on a code-test value
rs, *_ = momentum_panel(n=200, T=120)
two('small 6/6 mean', wml1(rs, 6, 6).mean(), wml2(rs, 6, 6).mean(), 1e-9)
print(f'code widgets checked: {ncode}')
for f_ in fails:
    print('FAIL', f_)
lv.report()
if fails:
    sys.exit(1)
