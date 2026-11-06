"""Recompute every number stated in stat-models level 3 and check it at its JSON path.

Run: python3 docs/reports/stat-models-L3-numbers.py   (NumPy and the standard library; exits 0 when all pass)

Second computations: exact enumerations (4,096 sign patterns, 252 and 184,756 splits), a dynamic programme for the
Mann-Whitney null, own IRLS and bisection here; SciPy 1.14.1 / statsmodels 0.14.4 in Pyodide 0.27.7 pasted in SM.
Seeded datasets (67, 96, 73, 83, 53, and the planted cases) give identical streams in local NumPy and Pyodide.
"""
import itertools
import math
import os
import sys
from statistics import NormalDist

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("stat-models", 3)
Z = NormalDist()


def chk(f, path, v, dp=None):
    lv.expect(f, path, (round(v, dp) if dp else int(round(v))) if dp is not None else v)


def agree(a, b, tol, what=''):
    a, b = np.atleast_1d(np.asarray(a, float)), np.atleast_1d(np.asarray(b, float))
    if not np.all(np.abs(a - b) <= tol):
        print('BAD agreement', what, a, b); sys.exit(1)


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 / (1 - qab * x / qap); h = d
    for m in range(1, 400):
        m2 = 2 * m; aa = m * (b - m) * x / ((qam + m2) * (a + m2)); d = 1 / (1 + aa * d); c = 1 + aa / c; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2)); d = 1 / (1 + aa * d); c = 1 + aa / c; de = d * c; h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def betainc(a, b, x):
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * betacf(b, a, 1 - x) / b


t_two = lambda t, df: betainc(df / 2, 0.5, df / (df + t * t))


def welch(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float); va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    t = (a.mean() - b.mean()) / math.sqrt(va + vb); df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    return t, t_two(t, df)


def rankdata(x):
    x = np.asarray(x, float); o = np.argsort(x, kind='mergesort'); r = np.empty(len(x)); i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and x[o[j + 1]] == x[o[i]]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2 + 1; i = j + 1
    return r


def mw_exact(m, n, u):
    f = np.zeros((m + 1, m * n + 1)); f[0, 0] = 1
    for i in range(m + n):
        g = f.copy()
        for k in range(1, m + 1):
            beat = i - (k - 1)
            if 0 <= beat <= n:
                g[k, beat:] += f[k - 1, :m * n + 1 - beat]
        f = g
    dist = f[m] / math.comb(m + n, m); lo = min(u, m * n - u)
    return min(1.0, 2 * dist[:int(lo) + 1].sum())


def signrank_exact(x):
    x = np.asarray(x, float); r = rankdata(np.abs(x)); wneg = r[x < 0].sum(); tot = r.sum(); cnt = 0; n = len(x)
    for signs in itertools.product([0, 1], repeat=n):
        w = sum(rk for rk, s_ in zip(r, signs) if s_)
        cnt += min(w, tot - w) <= min(wneg, tot - wneg) + 1e-12
    return wneg, tot - wneg, cnt / 2 ** n


SM = dict(welchAB=[-0.42761662374929943, 0.6770143539150858], mw=0.008293160601681265, mwnorm=0.010193104991108252, wA=0.01220703125, wB=0.2333984375, tB=0.4612167390553419,
          wD6=0.004841826619822732, perm2=0.20880512676178312, perm1=0.10440256338089156, welchP=[1.312947142927424, 0.2056954408578743], mc=0.20916790832091678,
          signflip=0.2686573134268657, t1=0.25778638127935843, skew=[0.05555555555555555, 0.2607745961509976], block=[0.0002, 0.2769],
          tukey=[0.005174627480889685, 1.1429544064430013], tscale=0.889773309819376, huber=[0.026846337400840907, 1.1679356624239206], hw39=0.05027418241684588,
          theil=1.2345535336436733, ols=[0.38252893, 1.58382799], olsse=[0.41749294, 0.46997611])
# ---------- l10 ----------
A = np.array([0.42, 0.15, -0.08, 0.31, 0.27, -0.12, 0.36, 0.22, 0.05, 0.48, -0.03, 0.19]); B = np.array([-0.21, 0.04, -0.35, 0.10, -0.18, 6.50, -0.27, 0.02, -0.09, -0.40, 0.07, -0.15])
tw, pw = welch(A, B); agree([tw, pw], SM['welchAB'], 1e-9, 'welch AB')
r = rankdata(np.r_[A, B]); RA = r[:12].sum(); UA = RA - 78; UB = 144 - UA; pmw = mw_exact(12, 12, UA); agree(pmw, SM['mw'], 1e-12)
pnorm = 2 * (1 - Z.cdf((UA - 72 - 0.5) / math.sqrt(300))); agree(pnorm, SM['mwnorm'], 1e-9)
wn, wp, pA = signrank_exact(A); agree(pA, SM['wA'], 1e-12); _, _, pB = signrank_exact(B); agree(pB, SM['wB'], 1e-12)
tB = B.mean() / (B.std(ddof=1) / math.sqrt(12)); agree(t_two(tB, 11), SM['tB'], 1e-9)
Bnew = B.copy(); Bnew[5] = 0.5
C_, D_ = [-1, -1, 0, 3, 3], [-3, -3, 0, 1, 1]; UC = sum((c > d) + 0.5 * (c == d) for c in C_ for d in D_)
rng = np.random.default_rng(53); block = rng.normal(0, 8, 200); order = rng.integers(0, 2, 200); eA = 3 * rng.standard_t(4, 200); eB = 3 * rng.standard_t(4, 200); dd = (4 + block + eB) - (5 + block + eA)
rr = rankdata(np.abs(dd)); W = min(rr[dd > 0].sum(), rr[dd < 0].sum()); mu = 200 * 201 / 4; sd = math.sqrt(200 * 201 * 401 / 24)
pd6 = 2 * Z.cdf((W - mu + 0.5) / sd); agree(pd6, SM['wD6'], 2e-4, 'wilcoxon D6 normal approx')
f = 'l10'
chk(f, 'screens[0].explain', A.mean() * 100 / 100, 3); chk(f, 'screens[0].explain', B.mean(), 3); chk(f, 'screens[0].explain', tw, 4); chk(f, 'screens[0].explain', pw, 3)
chk(f, 'screens[1].explain', B.mean(), 3); chk(f, 'screens[1].explain', Bnew.mean(), 3)
chk(f, 'screens[2].widget', UA); chk(f, 'screens[2].widget', UB); chk(f, 'screens[2].canvas', RA); chk(f, 'screens[2].canvas', r[12:].sum())
chk(f, 'screens[2].explain', math.comb(24, 12)); chk(f, 'screens[2].explain', pmw, 5); chk(f, 'screens[2].explain', pnorm, 4)
for v in r[:12]:
    chk(f, 'screens[2].canvas', v)
chk(f, 'screens[3].widget.answer', UA / 144, 4); chk(f, 'screens[3].widget.wrong[0].value', UB / 144, 4); chk(f, 'screens[3].widget.wrong[1].value', RA / 300, 2)
chk(f, 'screens[4].widget', UC, 1); chk(f, 'screens[4].hints', UC / 25, 2)
chk(f, 'screens[5].widget.answer', wn); chk(f, 'screens[5].widget.wrong[0].value', wp); chk(f, 'screens[5].explain', pA, 4); chk(f, 'screens[5].explain', 4096); chk(f, 'screens[5].explain', pB, 3); chk(f, 'screens[5].explain', SM['tB'], 3)
chk(f, 'screens[6].prose', SM['wD6'], 5)
chk(f, 'screens[7].widget.answer', 2 / math.comb(6, 3), 1); chk(f, 'screens[7].widget.wrong[0].value', 1 / math.comb(6, 3), 2)
chk(f, 'screens[8].widget.tests', mw_exact(4, 5, 19), 15); chk(f, 'screens[8].widget.tests', mw_exact(3, 3, 0), 1)
chk(f, 'screens[9].widget', UA / 144, 2); chk(f, 'screens[9].widget', pmw, 3)
chk(f, 'quiz[0].widget.answer', rankdata([-0.2, 0.1, 0.3, 0.3, 0.5])[2], 1)
# ---------- l11 ----------
on = np.array([-0.27, 0.05, 0.6, 1.43, 2.26, 0.23, -1.14, 0.09, 0.68, -0.29]); off = np.array([0.25, -1.01, -0.68, -0.7, -0.26, -2.08, 1.17, -0.01, 0.76, 0.58])
rng = np.random.default_rng(67); on2 = np.round(0.25 + 0.8 * rng.standard_t(3, 10), 2); off2 = np.round(0.8 * rng.standard_t(3, 10), 2); agree(np.r_[on2, off2], np.r_[on, off], 1e-12, 'perm data')
pool = np.r_[on, off]; d0 = on.mean() - off.mean(); tot = pool.sum(); c1 = c2 = 0
sums = np.array([pool[list(c)].sum() for c in itertools.combinations(range(20), 10)])
dif = sums / 10 - (tot - sums) / 10; p1 = float(np.mean(dif >= d0 - 1e-9)); p2 = float(np.mean(np.abs(dif) >= abs(d0) - 1e-9))
agree([p1, p2], [SM['perm1'], SM['perm2']], 1e-12, 'perm exact')
rngm = np.random.default_rng(1); idx = np.argsort(rngm.random((100000, 20)), axis=1); sh = pool[idx]; dmc = sh[:, :10].mean(1) - sh[:, 10:].mean(1)
cmc = int(np.sum(np.abs(dmc) >= abs(d0) - 1e-12)); agree((cmc + 1) / 100001, SM['mc'], 1e-12, 'mc')
tP, pP = welch(on, off); agree([tP, pP], SM['welchP'], 1e-9); s2 = pool.var(ddof=1); nsd = math.sqrt(s2 * 0.2)
a5 = np.array([0.1, 0.2, 0.0, 0.3, 3.0]); b5 = np.array([-0.1, 0.05, -0.2, 0.0, 0.1]); p5 = np.r_[a5, b5]; d5 = a5.mean() - b5.mean()
cnt5 = sum(abs(p5[list(c)].mean() - np.delete(p5, list(c)).mean()) >= abs(d5) - 1e-12 for c in itertools.combinations(range(10), 5))
agree([cnt5 / 252, welch(a5, b5)[1]], SM['skew'], 1e-9, 'skew')
rng = np.random.default_rng(2); fl = rng.choice([-1, 1], size=(100000, 10)); cs = int(np.sum(np.abs((fl * on).mean(1)) >= abs(on.mean()) - 1e-12)); agree((cs + 1) / 100001, SM['signflip'], 1e-12)
t1 = on.mean() / (on.std(ddof=1) / math.sqrt(10)); agree(t_two(t1, 9), SM['t1'], 1e-9)
f = 'l11'
chk(f, 'screens[0].prose', d0, 3); chk(f, 'screens[0].explain', 0.562, 3); chk(f, 'screens[0].widget.accept', p1, 4); chk(f, 'screens[0].widget.wrong[1].value', p2, 3)
chk(f, 'screens[1].widget.answer', math.comb(20, 10)); chk(f, 'screens[1].widget.wrong[0].value', math.factorial(10)); chk(f, 'screens[1].widget.wrong[1].value', 2 ** 20); chk(f, 'screens[1].explain', p2, 4)
chk(f, 'screens[2].prose', cmc); chk(f, 'screens[2].widget.answer', (cmc + 1) / 100001, 5); chk(f, 'screens[2].widget.wrong[0].value', cmc / 100000, 5); chk(f, 'screens[2].explain', tP, 4); chk(f, 'screens[2].explain', pP, 4)
chk(f, 'screens[3].prose', s2, 5); chk(f, 'screens[3].widget.answer', nsd, 4); chk(f, 'screens[3].widget.wrong[0].value', s2 * 0.2, 4); chk(f, 'screens[3].widget.wrong[1].value', math.sqrt(s2 * 0.1), 4)
chk(f, 'screens[3].feedback', float(dmc.std()), 4); chk(f, 'screens[3].explain', d0 / nsd, 2)
chk(f, 'screens[5].canvas', cnt5 / 252, 4); chk(f, 'screens[5].canvas', welch(a5, b5)[1], 3); chk(f, 'screens[5].explain', cnt5)
chk(f, 'screens[6].canvas', SM['block'][0], 4); chk(f, 'screens[6].canvas', SM['block'][1], 3)
chk(f, 'screens[7].widget.answer', 1 / 100, 2); chk(f, 'screens[7].widget.wrong[0].value', 1 / 99, 4)
import itertools; _pat = np.array(list(itertools.product([-1, 1], repeat=10))); _ex = float(np.mean(np.abs((_pat * on).mean(1)) >= abs(on.mean()) - 1e-12)); chk(f, 'screens[8].prose', _ex, 3); chk(f, 'screens[8].prose', t_two(t1, 9), 3)
chk(f, 'screens[9].explain', math.comb(30, 15)); chk(f, 'quiz[0].widget.answer', 1 / 200, 3)
# planted block example (periodic signal, seed 3) recomputed with the lesson's code


def blockex(seed):
    rng = np.random.default_rng(seed); e = rng.normal(0, 1, 200); rr_ = np.zeros(200)
    for t in range(200):
        rr_[t] = (0.9 * rr_[t - 1] if t else 0) + e[t]
    sig = ((np.arange(200) // 25) % 2).astype(bool); d0_ = rr_[sig].mean() - rr_[~sig].mean(); g = np.random.default_rng(seed + 1000)
    S = sig[np.argsort(g.random((5000, 200)), axis=1)]; dn = np.array([rr_[s_].mean() - rr_[~s_].mean() for s_ in S]); pn = (np.sum(np.abs(dn) >= abs(d0_)) + 1) / 5001
    lags = g.integers(1, 200, 5000); db = np.array([rr_[np.roll(sig, L)].mean() - rr_[~np.roll(sig, L)].mean() for L in lags]); pb = (np.sum(np.abs(db) >= abs(d0_)) + 1) / 5001
    return pn, pb


agree(blockex(3), SM['block'], 1e-4, 'block example')
# ---------- l12 ----------
rng = np.random.default_rng(96); R = np.round(0.05 + 0.7 * rng.standard_t(4, 60), 2); s = R.std(ddof=1); iqr = float(np.subtract(*np.percentile(R, [75, 25])))
kurt = float(np.mean((R - R.mean()) ** 4) / np.mean((R - R.mean()) ** 2) ** 2 - 3)
npdf = lambda z: np.exp(-z * z / 2) / math.sqrt(2 * math.pi); Phi = np.vectorize(lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2))))
f0 = lambda h, data=R: float(np.mean(npdf((0 - data) / h)) / h)
hs = 0.9 * min(s, iqr / 1.34) * 60 ** -0.2; h106 = 1.06 * s * 60 ** -0.2; hsc = s * 60 ** -0.2; hsp = s * (45) ** -0.2


def kq(data, h, q):
    lo, hi = data.min() - 10 * h, data.max() + 10 * h
    for _ in range(200):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if Phi((m - data) / h).mean() < q else (lo, m)
    return (lo + hi) / 2


q01 = kq(R, hs, 0.01); qn = R.mean() + s * Z.inv_cdf(0.01); qe = float(np.quantile(R, 0.01))
SP = np.round(np.random.default_rng(73).exponential(1.0, 40), 2); ssp = SP.std(ddof=1); h2 = 0.9 * min(ssp, float(np.subtract(*np.percentile(SP, [75, 25]))) / 1.34) * 40 ** -0.2
below = float(Phi((0 - SP) / h2).mean())
f = 'l12'
chk(f, 'screens[0].explain', R.mean(), 4); chk(f, 'screens[0].explain', s, 4); chk(f, 'screens[0].explain', kurt, 2); chk(f, 'screens[0].prose', R.min(), 2)
chk(f, 'screens[1].widget.answer', f0(0.05), 4); chk(f, 'screens[1].widget.wrong[0].value', f0(1.0), 4); chk(f, 'screens[1].widget.wrong[1].value', f0(hs), 4); chk(f, 'screens[1].explain', f0(1.0), 4)
chk(f, 'screens[2].prose', iqr, 3); chk(f, 'screens[2].widget.answer', hs, 4); chk(f, 'screens[2].widget.accept', iqr / 1.34, 4); chk(f, 'screens[2].widget.wrong[0].value', 0.9 * s * 60 ** -0.2, 4)
chk(f, 'screens[2].widget.wrong[1].value', 60 ** -0.2, 4)
chk(f, 'screens[3].widget.answer', f0(hs), 4); chk(f, 'screens[3].explain', npdf(R.mean() / s) / s, 3)
chk(f, 'screens[4].prose', q01, 3); chk(f, 'screens[4].prose', qe, 3); chk(f, 'screens[4].widget.answer', qn, 4); chk(f, 'screens[4].widget.wrong[0].value', q01, 4); chk(f, 'screens[4].widget.wrong[1].value', qe, 4)
chk(f, 'screens[4].prose', Z.inv_cdf(0.01), 4)
chk(f, 'screens[5].widget.answer', h106, 3); chk(f, 'screens[5].prose', hsc, 4)
chk(f, 'screens[6].widget', 0.29 * s, 2); chk(f, 'screens[6].explain', hsp, 4)
chk(f, 'screens[7].prose', h2, 4); chk(f, 'screens[7].widget.answer', below, 4); chk(f, 'screens[7].explain', 100 * below, 1)
chk(f, 'screens[8].widget.tests', hs, 6); chk(f, 'screens[8].widget.tests', h2, 6); chk(f, 'screens[8].widget.tests', q01, 6); chk(f, 'screens[8].widget.tests', kq(R, 0.5, 0.5), 6); chk(f, 'screens[8].widget.tests', f0(hs), 6)
chk(f, 'screens[9].widget.answer', -q01 * 1e5, 0); chk(f, 'screens[9].widget.wrong[0].value', -qn * 1e5, 0)
# ---------- l13 ----------
FM = np.array([1.2, 0.8, -0.5, 1.5, 0.9, 1.1, -0.2, 0.7, 25.0]); srt = np.sort(FM); tm = srt[1:-1].mean(); madn = float(np.median(np.abs(FM - np.median(FM)))) / Z.inv_cdf(0.75)
mu = np.median(FM)
for _ in range(500):
    u = (FM - mu) / madn; w = np.minimum(1, 1.345 / np.maximum(np.abs(u), 1e-12)); mu = float(np.sum(w * FM) / np.sum(w))
pk = [math.comb(9, j) * (1 / 9) ** j * (8 / 9) ** (9 - j) for j in range(4)]; bsd = FM.std(ddof=0) / 3
rng = np.random.default_rng(83); m = np.round(rng.normal(0, 1, 60), 2); y = np.round(0.02 + 1.2 * m + rng.normal(0, 0.8, 60), 2); y[39] = 25.0; X = np.column_stack([np.ones(60), m])
ols = np.linalg.lstsq(X, y, rcond=None)[0]; res = y - X @ ols; olsse = np.sqrt(np.diag(np.linalg.inv(X.T @ X)) * (res @ res) / 58); agree(ols, SM['ols'], 1e-7); agree(olsse, SM['olsse'], 1e-7)
b = ols.copy()
for _ in range(500):
    rr_ = y - X @ b; sc = np.median(np.abs(rr_)) / Z.inv_cdf(0.75); u = rr_ / (4.685 * sc); w = np.where(np.abs(u) < 1, (1 - u ** 2) ** 2, 0.0)
    nb = np.linalg.solve(X.T @ (w[:, None] * X), X.T @ (w * y))
    if np.max(np.abs(nb - b)) < 1e-13:
        b = nb; break
    b = nb
agree(b, SM['tukey'], 1e-7, 'tukey'); agree(sc, SM['tscale'], 1e-6); agree(w[39], 0, 0)
slopes = [(y[j] - y[i]) / (m[j] - m[i]) for i in range(60) for j in range(i + 1, 60) if m[j] != m[i]]; ts = float(np.median(slopes)); agree(ts, SM['theil'], 1e-12)


def ols_at(v):
    y2 = y.copy(); y2[39] = v
    return np.linalg.lstsq(X, y2, rcond=None)[0][1]


mask = np.arange(60) != 39; drop = np.linalg.lstsq(X[mask], y[mask], rcond=None)[0]
f = 'l13'
chk(f, 'screens[0].widget.answer', FM.mean(), 3); chk(f, 'screens[0].widget.wrong[1].value', FM[:8].mean(), 4); chk(f, 'screens[0].explain', (FM[:8].sum() + 1.0) / 9, 3)
chk(f, 'screens[1].widget.answer', (FM[:8].sum() + 1.0) / 9, 4); chk(f, 'screens[1].feedback', FM.mean() - (FM[:8].sum() + 1) / 9, 1)
chk(f, 'screens[2].widget.answer', tm, 4); chk(f, 'screens[2].widget.wrong[0].value', np.sort(FM)[1:].mean(), 3); chk(f, 'screens[2].widget.wrong[1].value', srt[1:-1].sum() / 9, 4); chk(f, 'screens[2].explain', mu, 2)
chk(f, 'screens[3].widget.answer', madn, 4); chk(f, 'screens[3].widget.wrong[1].value', FM.std(ddof=1), 2); chk(f, 'screens[3].explain', FM.std(ddof=1), 3)
chk(f, 'screens[4].widget.answer', pk[0], 4); chk(f, 'screens[4].widget.wrong[0].value', pk[1], 4)
for j in range(4):
    chk(f, 'screens[4].feedback', 100 * pk[j], 2)
chk(f, 'screens[4].explain', bsd, 3)
chk(f, 'screens[5].prose', ols[1], 3); chk(f, 'screens[5].prose', b[1], 3); chk(f, 'screens[5].widget.answer', ols_at(40), 3)
for v in (8, 15, 40):
    chk(f, 'screens[5].explain', ols_at(v), 3)
chk(f, 'screens[6].prose', drop[1], 3)
chk(f, 'screens[7].widget.answer', math.comb(60, 2)); chk(f, 'screens[7].feedback', len(slopes)); chk(f, 'screens[7].explain', ts, 4)
chk(f, 'screens[8].explain', sc, 5); chk(f, 'screens[8].explain', ((y - X @ b) / sc)[39], 0)
chk(f, 'screens[9].feedback', SM['huber'][1], 6); chk(f, 'screens[9].feedback', SM['hw39'], 4)
chk(f, 'screens[10].widget.answer', 5e6 * (round(ols[1], 6) - round(b[1], 6)), 0); chk(f, 'screens[10].widget.wrong[0].value', 5e6 * round(ols[1], 6), 0)
# ---------- review and homework ----------
f = 'review'
chk(f, 'items[0].widget.answer', 26 - 10); chk(f, 'items[8].widget.answer', 0.9 * (1 / 1.34) * 100 ** -0.2, 4); chk(f, 'items[8].widget.wrong[1].value', 1.06 * 100 ** -0.2, 3)
f = 'homework'
chk(f, 'items[3].widget.answer', (117 - 72.5) / math.sqrt(300), 4); chk(f, 'items[3].explain', pnorm, 4); chk(f, 'items[3].explain', pmw, 5)
chk(f, 'items[4].widget.answer', 1 - 1 / math.sqrt(2), 4); chk(f, 'items[6].widget.answer', 1 - pk[0], 4)
sdS = y.std(ddof=1); iqS = float(np.subtract(*np.percentile(y, [75, 25]))); hS = 0.9 * min(sdS, iqS / 1.34) * 60 ** -0.2
chk(f, 'items[2].model', sdS, 3); chk(f, 'items[2].model', y.mean() + Z.inv_cdf(0.01) * sdS, 2); chk(f, 'items[2].model', hS, 4); chk(f, 'items[2].model', kq(y, hS, 0.01), 2)
chk(f, 'items[2].model', float(np.quantile(y, 0.01)), 2)
lv.report()
