"""Recompute every number stated in momentum-rep level 3 (Evidence and extension) by two routes, and check each at its JSON path.
Run: python3 docs/reports/momentum-rep-L3-numbers.py   (needs numpy and statsmodels; exits 0 when every check passes)
Data: the course generator, verbatim from docs/briefs/momentum-rep.md: the base panel (seed 2, 500 x 300) and the
extension panel momentum_panel(T=480, c_after=0.005, t_pub=300, crash=420), whose first 300 months equal the base panel.
Route 1 is the lessons' form (statsmodels HAC and OLS, loop composites). Route 2 is independent: Newey-West and OLS
by hand in NumPy (lstsq and the classical covariance), overlapping returns from the cohort-by-month matrix W @ r.T,
rolling betas by polyfit, drawdown by a loop. `two` asserts the routes agree; `lv.expect` checks each stated value
where it is stated. Every code widget of the level is run in CPython: solutions pass, starters fail.
"""
import sys, os, math
import numpy as np
import statsmodels.api as sm
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("momentum-rep", 3)
E = lv.expect
fails = []


def two(name, a, b, tol=1e-9):
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


def form(r, J, skip=0):
    c = np.vstack([np.zeros((1, r.shape[1])), np.cumsum(np.log1p(r), axis=0)])
    f = np.full(r.shape, np.nan)
    t = np.arange(J + skip, r.shape[0])
    f[t] = np.expm1(c[t - skip] - c[t - skip - J])
    return f


def wts(ft, q=10):
    o = np.argsort(ft, kind='mergesort'); rk = np.empty(len(ft), int); rk[o] = np.arange(len(ft))
    dec = rk * q // len(ft); w = np.zeros(len(ft))
    w[dec == q - 1] = 1 / np.count_nonzero(dec == q - 1); w[dec == 0] = -1 / np.count_nonzero(dec == 0)
    return w, dec


def cohorts(r, J, skip=0):
    f = form(r, J, skip); W = np.zeros(r.shape)
    for s in range(J + skip, r.shape[0]):
        W[s] = wts(f[s])[0]
    return W


def wml(r, J, K, skip=0):
    W = cohorts(r, J, skip); S = W @ r.T          # S[s, t]: cohort s in month t
    return np.array([np.mean([S[s, t] for s in range(t - K + 1, t + 1)]) for t in range(J + skip + K - 1, r.shape[0])])


def tst(x):
    x = np.asarray(x); return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))


def nw_hand(x, L):
    x = np.asarray(x, float); n = len(x); u = x - x.mean()
    V = u @ u / n + 2 * sum((1 - j / (L + 1)) * (u[j:] @ u[:-j]) / n for j in range(1, L + 1))
    return x.mean() / math.sqrt(V / n)


def nw_sm(x, L):
    return float(sm.OLS(np.asarray(x, float), np.ones(len(x))).fit(cov_type='HAC', cov_kwds={'maxlags': L}).tvalues[0])


def ols_hand(y, X):
    X = np.column_stack([np.ones(len(y)), X]); b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b; s2 = e @ e / (len(y) - X.shape[1]); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return b, b / se, 1 - (e @ e) / np.sum((y - y.mean()) ** 2), se


def acf(x, k):
    u = np.asarray(x) - np.mean(x); return float(sum(u[i] * u[i - k] for i in range(k, len(u))) / (u @ u))


p2 = lambda v, k=2: round(100 * float(v), k)
r, size, m, F = momentum_panel()
re, se_, me, Fe = momentum_panel(T=480, c_after=0.005, t_pub=300, crash=420)
two('extension starts as base', re[:300], r)
x66 = wml(r, 6, 6)
xe = wml(re, 6, 6, 1)

# ---------- l11 ----------
W = cohorts(r, 6); S = W @ r.T
ov = np.array([S[s, s:s + 6].sum() for s in range(6, 295)])
ov1 = np.array([sum(W[s] @ r[s + h] for h in range(6)) for s in range(6, 295)])
two('overlap returns', ov, ov1)
OVT, OVNW, OV0 = tst(ov), nw_hand(ov, 5), nw_hand(ov, 0)
two('NW overlap 5', OVNW, nw_sm(ov, 5)); two('NW overlap 0', OV0, nw_sm(ov, 0))
CT, CNW0, CNW5 = tst(x66), nw_hand(x66, 0), nw_hand(x66, 5)
two('NW comp 0', CNW0, nw_sm(x66, 0), 1e-12); two('NW comp 5', CNW5, nw_sm(x66, 5), 1e-12)
two('brief comp t', [round(CT, 4), round(CNW0, 4), round(CNW5, 4)], [2.7412, 2.7459, 2.9925])
AO = [acf(ov, k) for k in range(1, 9)]; AC = [acf(x66, k) for k in range(1, 9)]
two('brief comp acf', np.round(AC[1:5], 3), [-0.050, -0.072, -0.041, -0.033])
for k in range(8):
    E('l11', f'screens[1].canvas.state.values.l{k + 1}', round(AO[k], 3))
    E('l11', f'screens[1].canvas.controls[0].frames[1].values.l{k + 1}', round(AC[k], 3))
E('l11', 'screens[1].widget.accept', round(AO[2], 2)); E('l11', 'screens[1].explain.text', round(AO[0], 2))
for j in range(1, 7):
    E('l11', f'screens[2].widget.rows[{j - 1}][2].answer', round((6 - j) / 6, 4))
for path in ('screens[0]', 'screens[11]'):
    E('l11', path, round(OVT, 2)); E('l11', path, round(CT, 2)); E('l11', path, round(OVNW, 2))
E('l11', 'screens[3].widget.answer', round(OVT / math.sqrt(6), 2))
E('l11', 'screens[4].widget.answer', round(1 - 2 / 6, 4))
E('l11', 'screens[5].prose', round(CNW5, 2))
for k in range(1, 5):
    E('l11', 'screens[5].prose', round(AC[k], 3))
E('l11', 'screens[6].prose', round(OV0, 2)); E('l11', 'screens[6].explain.text', round(OVNW, 2))
E('l11', 'screens[7].explain.text', round(CNW0, 4)); E('l11', 'screens[7].explain.text', round(CT, 4))
E('l11', 'screens[8].explain.text', len(ov)); E('l11', 'screens[8].explain.text', p2(ov.mean()))
E('l11', 'screens[9].explain.text', round(CNW0, 4)); E('l11', 'screens[9].explain.text', round(CNW5, 4))
E('l11', 'screens[10].explain.text', round(CNW5, 4)); E('l11', 'quiz[0].widget.answer', 0.75)

# ---------- l12 ----------
idx = np.arange(11, 300)
b, t, r2, se = ols_hand(x66, np.column_stack([m[idx], F[idx]]))
res = sm.OLS(x66, sm.add_constant(np.column_stack([m[idx], F[idx]]))).fit()
two('alpha', b[0], res.params[0], 1e-10); two('alpha t', t[0], res.tvalues[0], 1e-8); two('R2', r2, res.rsquared, 1e-10)
two('brief alpha', [round(b[0], 4), round(t[0], 2), round(r2, 3)], [0.0102, 2.79, 0.023])
b1, t1, r21, _ = ols_hand(x66, m[idx])
TAH = float(sm.OLS(x66, sm.add_constant(np.column_stack([m[idx], F[idx]]))).fit(cov_type='HAC', cov_kwds={'maxlags': 5}).tvalues[0])
E('l12', 'screens[0].canvas.state.caption', round(b1[1], 3)); E('l12', 'screens[0].canvas.state.caption', round(r21, 4))
E('l12', 'screens[0].explain.text', p2(b1[0])); E('l12', 'screens[0].explain.text', round(t1[0], 2)); E('l12', 'screens[0].explain.text', round(t1[1], 2))
E('l12', 'screens[2].widget.answer', round(b[0], 4)); E('l12', 'screens[2].explain.text', round(t[0], 2)); E('l12', 'screens[2].explain.text', round(r2, 3))
E('l12', 'screens[2].canvas.params.rows[0][3]', round(t[0], 2)); E('l12', 'screens[2].canvas.params.rows[0][2]', round(se[0], 4))
E('l12', 'screens[3].prose', p2(b1[0])); E('l12', 'screens[3].prose', p2(b[0]))
E('l12', 'screens[4].explain.text', round(TAH, 2))
mx = me[12:]; i0 = 408
sl24 = np.polyfit(mx[i0:i0 + 24], xe[i0:i0 + 24], 1)[0]
cv = np.cov(mx[i0:i0 + 24], xe[i0:i0 + 24], ddof=1)
two('slope 24', sl24, cv[0, 1] / cv[0, 0])
slall = np.polyfit(mx, xe, 1)[0]
E('l12', 'screens[5].widget.answer', round(sl24, 2)); E('l12', 'screens[5].explain.text', round(slall, 2))
rb24 = [np.polyfit(mx[k - 24:k], xe[k - 24:k], 1)[0] for k in range(24, len(xe) + 1)]
E('l12', 'screens[1].explain.text', round(rb24[i0], 2)); E('l12', 'screens[1].explain.text', round(rb24[i0 - 24], 2))
E('l12', 'screens[10].explain.text', round(rb24[i0], 2)); E('l12', 'screens[6].explain.text', p2(x66.std(ddof=1)))
E('l12', 'screens[9].explain.text', round(b[0], 4)); E('l12', 'screens[9].explain.text', round(t[0], 4)); E('l12', 'screens[9].explain.text', round(r2, 4))
E('l12', 'quiz[0].widget.answer', round(0.0102 / 0.0036, 2))

# ---------- l13 ----------
months = np.arange(12, 480)
pre, post = xe[months < 300], xe[months >= 300]
two('split 288', len(pre), 288)
MPRE, MPOST = pre.mean(), post.mean()
two('brief pre post', [round(100 * MPRE, 2), round(100 * MPOST, 2), round(tst(post), 2)], [1.04, 0.27, 0.57])
SED = math.sqrt(pre.var(ddof=1) / len(pre) + post.var(ddof=1) / len(post)); TD = (MPOST - MPRE) / SED
SEP = post.std(ddof=1) / math.sqrt(len(post))
E('l13', 'screens[0].explain.text', p2(MPRE)); E('l13', 'screens[0].explain.text', p2(MPOST))
E('l13', 'screens[2].widget.rows[0][1].answer', round(MPRE, 4)); E('l13', 'screens[2].widget.rows[1][1].answer', round(MPOST, 4))
E('l13', 'screens[2].widget.rows[2][1].answer', round(1 - MPOST / MPRE, 3)); E('l13', 'screens[2].explain.text', p2(1 - MPOST / MPRE, 0))
E('l13', 'screens[2].explain.text', round(tst(pre), 2)); E('l13', 'screens[2].explain.text', round(tst(post), 2))
E('l13', 'screens[3].widget.answer', round(TD, 2)); E('l13', 'screens[3].prose', p2(SED)); E('l13', 'screens[3].prose', p2(MPOST - MPRE))
E('l13', 'screens[4].prose', p2(SEP)); E('l13', 'screens[4].explain.text', round(abs((MPOST - 0.005) / SEP), 1))
Pn = 0.5 * (1 + math.erf(((round(100 * MPOST, 2) - round(100 * MPRE, 2)) / round(100 * SEP, 3)) / math.sqrt(2)))
E('l13', 'screens[4].explain.text', round(100 * Pn, 1))
E('l13', 'screens[5].prose', p2(1 - MPOST / MPRE, 0)); E('l13', 'screens[6].prose', p2(xe.mean()))
blocks = [xe[a:b].mean() for a, b in ((0, 117), (117, 234), (234, 351), (351, 468))]
for bl in blocks:
    E('l13', 'screens[7].prose', p2(bl)); E('l13', 'screens[10].explain.text', p2(bl))
NOCR = np.mean([v for mo, v in zip(months, xe) if mo >= 300 and mo not in (420, 421, 422)])
E('l13', 'screens[7].explain.text', p2(NOCR))
roll = [xe[k - 60:k].mean() for k in range(60, len(xe) + 1)]
aft = [(roll[k - 60], k - 1 + 12) for k in range(60, len(xe) + 1) if (k - 1 + 12) - 59 >= 300]
best = max(aft)
E('l13', 'screens[1].explain.text', p2(best[0])); E('l13', 'screens[1].explain.text', best[1])
nab = sum(1 for v, _ in aft if v >= MPRE)
E('l13', 'screens[1].explain.text', nab); E('l13', 'screens[1].explain.text', len(aft))
if not best[0] > MPRE:
    fails.append('l13 explore: the keyed answer says a post-1990 window beats the pre-1990 mean')
E('l13', 'screens[9].explain.text', round(MPRE, 4)); E('l13', 'screens[9].explain.text', round(TD, 4))
E('l13', 'quiz[1].widget.answer', 288); E('l13', 'quiz[0].widget.answer', 0.75)

# ---------- l14 ----------
CR = [v for mo, v in zip(months, xe) if mo in (420, 421, 422)]
two('brief crash', np.round(np.array(CR) * 100, 1), [-25.4, -13.3, -15.2])
E('l14', 'screens[0].widget.answer', round(CR[0], 3)); E('l14', 'screens[0].explain.text', p2(CR[1], 1)); E('l14', 'screens[0].explain.text', p2(CR[2], 1))
f1 = form(re, 6, 1); Wt = np.zeros(re.shape); Wl = np.zeros(re.shape)
for s in range(7, 480):
    dec = wts(f1[s])[1]; Wt[s] = (dec == 9) / 50.0; Wl[s] = (dec == 0) / 50.0
win = np.array([Wt[t - 5:t + 1].mean(axis=0) @ re[t] for t in range(12, 480)])
los = np.array([Wl[t - 5:t + 1].mean(axis=0) @ re[t] for t in range(12, 480)])
two('legs make the spread', win - los, xe, 1e-9)
for k in range(3):
    E('l14', f'screens[1].canvas.controls[0].frames[{k}].values.los', p2(los[i0 + k], 1))
    E('l14', f'screens[1].canvas.controls[0].frames[{k}].values.win', p2(win[i0 + k], 1))
E('l14', 'screens[1].explain.text', p2(los[i0], 1))


def lwb(t, window=36):
    dec = wts(f1[t])[1]; X = np.column_stack([np.ones(window), me[t - window:t]])
    bL = np.linalg.lstsq(X, re[t - window:t][:, dec == 0].mean(axis=1), rcond=None)[0][1]
    bW = np.linalg.lstsq(X, re[t - window:t][:, dec == 9].mean(axis=1), rcond=None)[0][1]
    return bL - bW


gap = np.array([lwb(t) for t in range(48, 480)]); tr = np.array([me[t - 12:t].sum() for t in range(48, 480)])
CORR = np.corrcoef(gap, tr)[0, 1]
for path in ('screens[3].explain.text', 'screens[9].explain.text'):
    E('l14', path, round(CORR, 2)); E('l14', path, round(lwb(420), 2)); E('l14', path, round(lwb(300), 2))
E('l14', 'screens[11].explain.text', round(lwb(420), 2)); E('l14', 'screens[11].explain.text', p2(CR[0], 1))
w = 1.0; pk = 1.0; mdd = 0.0; pkm = trm = 0; cur_pk_m = 12
for mo, v in zip(months, xe):
    w *= 1 + v
    if w > pk:
        pk, cur_pk_m = w, mo
    if w / pk - 1 < mdd:
        mdd, trm, pkm = w / pk - 1, mo, cur_pk_m
E('l14', 'screens[4].widget.answer', round(-mdd, 3)); E('l14', 'screens[4].explain.text', pkm); E('l14', 'screens[4].explain.text', trm)
E('l14', 'screens[4].explain.text', round(10 * (1 + mdd), 1))
sd6 = np.array([np.std(xe[k - 6:k], ddof=1) for k in range(6, len(xe))])
vs = xe[6:] * np.minimum(1.0, 0.05 / sd6); vs2 = xe[6:] * np.minimum(2.0, 0.05 / sd6)
VCR = vs[i0 - 6:i0 - 3]; SC = np.minimum(1.0, 0.05 / sd6)[i0 - 6:i0 - 3]
E('l14', 'screens[5].widget.answer', round(VCR[0], 3))
for k in range(3):
    E('l14', f'screens[5].canvas.params.rows[{k}][2]', round(SC[k], 2)); E('l14', f'screens[5].canvas.params.rows[{k}][3]', p2(VCR[k], 1))
E('l14', 'screens[5].explain.text', p2(xe[6:].mean())); E('l14', 'screens[5].explain.text', p2(vs.mean())); E('l14', 'screens[5].explain.text', p2(vs2.min(), 1))
E('l14', 'screens[5].explain.text', int(np.argmin(vs2)) + 18)
E('l14', 'screens[6].prose', p2(NOCR)); E('l14', 'screens[7].widget.answer', -0.9 * 0.12)
wst = np.argsort(xe, kind='stable')[:5]
for i in wst:
    E('l14', 'screens[8].explain.text', int(i) + 12); E('l14', 'screens[8].explain.text', int(i))
E('l14', 'quiz[0].explain.text', round(np.polyfit(me[12:], win, 1)[0], 2))
E('l14', 'quiz[1].prose', round(100 * np.std(xe[i0 - 6:i0], ddof=1), 2)); E('l14', 'quiz[1].widget.answer', round(0.05 / 0.0647, 2))

# ---------- l15 ----------
E('l15', 'screens[0].widget.answer', round(MPOST / MPRE, 3)); E('l15', 'screens[0].explain.text', round(TD, 2))
W0 = cohorts(r, 6); C = np.array([W0[t - 5:t + 1].mean(axis=0) for t in range(11, 300)])
TURN = np.mean([np.abs(C[i + 1] - C[i]).sum() for i in range(len(C) - 1)]); NET = x66.mean() - 0.0025 * TURN
two('brief net 0.82', round(100 * NET, 2), 0.82)
E('l15', 'screens[3].widget.rows[0][1].answer', round(x66.mean(), 4)); E('l15', 'screens[3].widget.rows[1][1].answer', round(b[0], 4))
E('l15', 'screens[3].widget.rows[2][1].answer', round(MPOST, 4)); E('l15', 'screens[3].widget.rows[3][1].answer', round(NET, 4))
E('l15', 'screens[1].canvas.params.lines[3]', round(OVNW, 2)); E('l15', 'screens[1].canvas.params.lines[6]', p2(xe.min(), 1))
E('l15', 'screens[3].canvas.params.rows[1][1]', p2(wml(r, 6, 6, 1).mean()))
E('l15', 'screens[9].explain.text', p2(MPOST / MPRE, 0))
E('l15', 'quiz[0].widget.answer', 0.75)

# ---------- review and homework ----------
E('review', 'items[0].widget.answer', 0.5); E('review', 'items[1].widget.answer', 0.5)
E('review', 'items[5].widget.answer', 300 - 11); two('no-skip 6/6 starts in month 11', len(r) - len(x66), 11)
E('review', 'items[6].prose', p2(MPOST)); E('review', 'items[6].prose', round(tst(post), 2))
E('review', 'items[7].widget.answer', -0.8 * 0.10); E('review', 'items[8].widget.answer', 0.4)
E('homework', 'items[3].widget.answer', round(MPOST - 0.0025 * 0.577, 5))
E('homework', 'items[0].explain.text', p2(x66.mean())); E('homework', 'items[0].explain.text', round(tst(x66), 2))
for v in (p2(MPRE), p2(MPOST), p2(xe.min(), 1), round(tst(x66), 2)):
    E('homework', 'items[5].model', v)


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
    if case.get('compare') == 'raises':
        try:
            eval(case['call'], ns)
            return False
        except Exception as ex:
            return type(ex).__name__ == case['expect']
    got = eval(case['call'], ns); want = eval(case['expect'], ns)
    tol = case.get('tol'); rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)

    def close(a, b):
        a = a.tolist() if hasattr(a, 'tolist') else a; b = b.tolist() if hasattr(b, 'tolist') else b
        if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(close(p, q) for p, q in zip(a, b))
        if isinstance(a, (bool, str)) or isinstance(b, (bool, str)):
            return a == b
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    if case.get('compare', 'equal') == 'isclose':
        return close(got, want)
    g = got.tolist() if hasattr(got, 'tolist') else got
    return g == want


ncode = 0
for fid, doc in lv.files.items():
    for wdg in widgets(doc):
        ncode += 1
        for label, src, must in (('solution', wdg['solution'], True), ('starter', wdg['starter'], False)):
            ns = {'__learner_source__': src}
            if wdg.get('prelude'):
                exec(wdg['prelude'], ns)
            try:
                exec(src, ns)
            except Exception:
                if must:
                    fails.append(f'{fid}: solution does not load')
                continue
            res_ = []
            for case in wdg['tests']:
                try:
                    res_.append(bool(run_case(ns, case)))
                except Exception:
                    res_.append(False)
            if must and not all(res_):
                fails.append(f'{fid}: solution fails tests {[i + 1 for i, v in enumerate(res_) if not v]}')
            if not must and all(res_):
                fails.append(f'{fid}: starter passes every test')
print(f'code widgets checked: {ncode}')
for f_ in fails:
    print('FAIL', f_)
lv.report()
if fails:
    sys.exit(1)
