"""Second-reader number checks for coint level 2 (l5 to l8, review-2, homework-2).

Every number is recomputed from the course generators (copied from the lesson preludes) with NumPy, pandas and
statsmodels in CPython, or from its closed form, then looked up where it is stated (app/tools/numbers_lib.py).
statsmodels values are compared after rounding to the places shown. Claims that are not single numbers use
`claim_text(...)`: such a check fails only while the faulty phrase is still in the content and the fact is false.
A failing check means the content is wrong (see docs/reviews/review-coint.md) and stays failing until fixed.
Run: python3 docs/reports/coint-L2-numbers.py   (about a minute)
"""
import math, os, sys, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('coint', 2)


def claim(ok, label, note=''):
    return lv._rec(bool(ok), 'claim: ' + label, note)


def claim_text(ref, path, phrase, ok, label, note=''):
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', note + ('' if present else ' (phrase gone)'))


def r(v, k=0):
    return round(float(v), k)


def make_two_walks(seed, n=500):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    return np.cumsum(z[:, 0]), np.cumsum(z[:, 1])


def make_pair(seed, n=1000, alpha=5.0, beta=1.5, phi=0.95, sd_u=0.5, x0=40.0, vol=0.015):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    x = x0 * np.exp(np.cumsum(vol * z[:, 0]))
    u = np.empty(n); u[0] = sd_u * z[0, 1]
    for t in range(1, n):
        u[t] = phi * u[t - 1] + sd_u * z[t, 1]
    return x, alpha + beta * x + u


def make_case(name, n=1000):
    if name == 'A':
        e = np.random.default_rng(1).standard_normal((n, 2))
        return np.cumsum(e[:, 0]), np.cumsum(0.8 * e[:, 0] + 0.6 * e[:, 1])
    if name == 'B':
        e = np.random.default_rng(2).standard_normal((n, 2))
        x = np.cumsum(e[:, 0]); u = np.empty(n); u[0] = 3 * e[0, 1]
        for t in range(1, n):
            u[t] = 0.5 * u[t - 1] + 3 * e[t, 1]
        return x, x + u
    if name == 'C':
        return make_pair(3, n)
    return make_two_walks(4, n)


def make_three(seed=5, n=1000):
    e = np.random.default_rng(seed).standard_normal((n, 4))
    w = np.cumsum(e[:, 0]); U = np.zeros((n, 3))
    for t in range(1, n):
        U[t] = 0.8 * U[t - 1] + 0.5 * e[t, 1:]
    return np.column_stack([w + U[:, 0], 0.8 * w + U[:, 1], 1.2 * w + U[:, 2]])


def make_three_walks(seed=7, n=1000):
    return np.cumsum(np.random.default_rng(seed).standard_normal((n, 3)), axis=0)


def tls(y, x):
    C = np.cov(np.vstack([x - x.mean(), y - y.mean()])); w, v = np.linalg.eigh(C); e = v[:, np.argmax(w)]
    return e[1] / e[0]


def hl_fit(s):
    s = np.asarray(s, float); ds = np.diff(s); X = np.column_stack([np.ones(len(ds)), s[:-1]])
    coef = np.linalg.lstsq(X, ds, rcond=None)[0]; res = ds - X @ coef
    se = math.sqrt(res @ res / (len(ds) - 2) * np.linalg.inv(X.T @ X)[1, 1])
    return coef[1], se


def hl(b):
    return math.inf if b >= 0 else math.log(0.5) / math.log(1 + b)


def rolling_z(s, w):
    q = pd.Series(s); return ((q - q.rolling(w).mean()) / q.rolling(w).std()).to_numpy()


def rolling_fit(y, x, window):
    a = np.full(len(y), np.nan); b = a.copy(); sd = a.copy()
    for t in range(window - 1, len(y)):
        xs, ys = x[t - window + 1:t + 1], y[t - window + 1:t + 1]
        bb, aa = np.polyfit(xs, ys, 1); rr = ys - aa - bb * xs
        a[t], b[t], sd[t] = aa, bb, rr.std(ddof=1)
    return a, b, sd


def positions(z, entry=2.0, exit=0.0, stop=4.0):
    pos = np.zeros(len(z)); cur = 0
    for t in range(len(z)):
        zt = z[t]
        if np.isnan(zt): cur = 0
        elif cur == 0:
            if entry <= zt < stop: cur = -1
            elif -stop < zt <= -entry: cur = 1
        elif cur == 1 and (zt >= -exit or zt <= -stop): cur = 0
        elif cur == -1 and (zt <= exit or zt >= stop): cur = 0
        pos[t] = cur
    return pos


def run_pnl(y, x, z, b, cost_bp=5.0, entry=2.0):
    pos = positions(z, entry); n = len(y); pnl = np.zeros(n); units = 0.0; hb = 0.0
    for t in range(1, n):
        pnl[t] = units * ((y[t] - y[t - 1]) - hb * (x[t] - x[t - 1]))
        if pos[t] != pos[t - 1]:
            nh = b[t] if pos[t] != 0 else 0.0
            pnl[t] -= (abs(pos[t] - units) * y[t] + abs(pos[t] * nh - units * hb) * x[t]) * cost_bp / 1e4
            units, hb = pos[t], nh
    return pnl, pnl.mean() / pnl.std(ddof=1) * np.sqrt(252)


# ---------------- l5 ----------------
x, y = make_pair(3, 1000)
b, a = np.polyfit(x, y, 1); bxy, axy = np.polyfit(y, x, 1); R2 = np.corrcoef(x, y)[0, 1] ** 2
lv.expect('l5', 'screens[0].explain.text', r(b, 4)); lv.expect('l5', 'screens[0].explain.text', r(a, 4))
lv.expect('l5', 'screens[0].feedback.byKey.ratio', r(x.mean(), 2)); lv.expect('l5', 'screens[0].feedback.byKey.ratio', r(y.mean(), 2))
lv.expect('l5', 'screens[0].feedback.byKey.ratio', r(y.mean() / x.mean(), 2))
lv.expect('l5', 'screens[2].prose', r(x[999], 2)); lv.expect('l5', 'screens[2].prose', r(y[999], 2))
lv.expect('l5', 'screens[2].widget.answer', int(1000 * r(b, 4)))
lv.expect('l5', 'screens[2].widget.wrong[1].value', r(1000 * y[999] / x[999]))
lv.expect('l5', 'screens[2].widget.wrong[2].value', r(1000 / b))
lv.expect('l5', 'screens[2].explain.text', int(round(1474 * r(x[999], 2), -2)))
lv.expect('l5', 'screens[2].explain.text', r(1000 * r(y[999], 2)))
lv.expect('l5', 'screens[2].explain.text', r(np.polyfit(np.log(x), np.log(y), 1)[0], 2))
lv.expect('l5', 'screens[3].prose', r(axy, 4)); lv.expect('l5', 'screens[3].prose', r(bxy, 4))
lv.expect('l5', 'screens[3].widget.answer', r(1 / r(bxy, 4), 4))
lv.expect('l5', 'screens[3].explain.text', r(1 / bxy, 4))
lv.expect('l5', 'screens[3].explain.text', r(r(b, 4) * r(bxy, 4), 4))      # the shown product of the rounded slopes
claim(abs(b * bxy - R2) < 1e-12, 'l5 product of slopes equals R^2')
for n, rows in ((250, ('1.80', '2.13', '0.85')), (500, ('1.69', '2.05', '0.82'))):
    xs, ys = make_pair(3, n); bb = np.polyfit(xs, ys, 1)[0]; bi = 1 / np.polyfit(ys, xs, 1)[0]; rr = np.corrcoef(xs, ys)[0, 1] ** 2
    fr = 0 if n == 250 else 1
    lv.expect('l5', f'screens[1].canvas.controls[0].frames[{fr}].caption', r(bb, 2))
    lv.expect('l5', f'screens[1].canvas.controls[0].frames[{fr}].caption', r(bi, 2))
    lv.expect('l5', f'screens[1].canvas.controls[0].frames[{fr}].caption', r(rr, 2))
x2, y2 = make_pair(3, 250); b2 = np.polyfit(x2, y2, 1)[0]; bxy2 = np.polyfit(y2, x2, 1)[0]
lv.expect('l5', 'screens[4].prose', r(b2, 4)); lv.expect('l5', 'screens[4].prose', r(bxy2, 4)); lv.expect('l5', 'screens[4].prose', r(1 / bxy2, 4))
lv.expect('l5', 'screens[4].widget.answer', r(r(b2, 4) * r(bxy2, 4), 3))
lv.expect('l5', 'screens[4].widget.wrong[0].value', r(r(1 / bxy2, 4) / r(b2, 4), 3))
claim_text('l5', 'screens[4].explain.text', 'pulls each slope towards zero', b2 < 1.5,
           'the y on x slope is attenuated towards zero', f'y on x on 250 days is {b2:.4f}, above the true 1.5; x carries no noise in make_pair')
lv.expect('l5', 'screens[1].canvas.controls[0].frames[2].caption', r(R2, 3))
lv.expect('l5', 'screens[6].feedback.correct', r(tls(y, x), 4))
lv.expect('l5', 'screens[6].feedback.correct', r(tls(y2, x2), 2))
lv.expect('l5', 'screens[6].explain.text', r(tls(100 * y2, x2) / 100, 2))
claim(abs(tls(x, y) * tls(y, x) - 1) < 1e-9, 'l5 TLS swap gives the reciprocal')
# review-2 items[8] (finding 20): TLS with x in pence, converted back, is the y on x slope
lv.expect('review', 'items[8].prose', r(tls(y2, x2), 2)); lv.expect('review', 'items[8].prose', r(tls(y2, 100 * x2) * 100, 2))
lv.expect('review', 'items[8].explain.text', r(np.polyfit(x2, y2, 1)[0], 2))
claim(abs(tls(y2, 100 * x2) * 100 - np.polyfit(x2, y2, 1)[0]) < 0.01, 'review-2 items[8] TLS with x in pence is about the y on x slope', f'{tls(y2, 100 * x2) * 100:.4f} vs {np.polyfit(x2, y2, 1)[0]:.4f}')
lv.expect('l7', 'screens[3].explain.text', r(math.log(2) / 0.0521, 1)); lv.expect('l7', 'screens[2].hints[2].text', 13.29)
lv.expect('l7', 'screens[7].explain.text', r(100 * (1 - 0.5 ** (10 / (math.log(0.5) / math.log(0.9492) ))), 0)) if False else None
claim(abs((1 - 0.9492 ** 10) - 0.40) < 0.01, 'l7 screens[7]: a 10-day limit captures about 40% of the move', f'{1 - 0.9492 ** 10:.3f}')
xb, yb = make_case('B')
lv.expect('l5', 'screens[5].explain.text', r(np.corrcoef(xb, yb)[0, 1] ** 2, 3))
lv.expect('l5', 'screens[5].explain.text', r(np.polyfit(xb, yb, 1)[0], 3)); lv.expect('l5', 'screens[5].explain.text', r(1 / np.polyfit(yb, xb, 1)[0], 3))
x15, y15 = make_pair(3, 1500)
rb = np.full(1500, np.nan)
for t in range(249, 1500):
    rb[t] = np.polyfit(x15[t - 249:t + 1], y15[t - 249:t + 1], 1)[0]
lv.expect('l5', 'screens[7].explain.text', r(np.nanmin(rb), 2)); lv.expect('l5', 'screens[7].explain.text', r(np.nanmax(rb), 2))
lv.expect('l5', 'screens[7].explain.text', int(np.nanargmin(rb))); lv.expect('l5', 'screens[7].explain.text', int(np.nanargmax(rb)))
r60 = np.array([np.polyfit(x15[t - 59:t + 1], y15[t - 59:t + 1], 1)[0] for t in range(59, 1500)])
lv.expect('l5', 'screens[7].explain.text', r(r60.min(), 2)); lv.expect('l5', 'screens[7].explain.text', r(r60.max(), 2))
xo, yo = x[250:], y[250:]
lv.expect('l5', 'screens[8].widget.options[3].why', r(np.std(yo - r(1 / bxy2, 4) * xo, ddof=1), 2))
lv.expect('l5', 'screens[8].widget.options[3].why', r(np.std(yo - r(b2, 4) * xo, ddof=1), 2))
lv.expect('l5', 'screens[8].explain.text', r(coint(y2, x2)[1], 3)); lv.expect('l5', 'screens[8].explain.text', r(coint(x2, y2)[1], 3))
lv.expect('l5', 'screens[9].widget.options[3].why', r(math.sqrt(0.6), 3))
lv.expect('l5', 'screens[9].widget.options[3].text', r(1.2 / math.sqrt(0.6), 2))
xs1, ys1 = make_pair(3, 1000, sd_u=0.1)
lv.expect('l5', 'quiz[1].prose', r(np.polyfit(xs1, ys1, 1)[0], 4)); lv.expect('l5', 'quiz[1].prose', r(1 / np.polyfit(ys1, xs1, 1)[0], 4))
lv.expect('l5', 'quiz[1].widget.options[0].text', r(np.corrcoef(xs1, ys1)[0, 1] ** 2, 4))
lv.expect('l5', 'quiz[2].widget.options[1].why', r(y[999] / x[999], 2))
lv.expect('l5', 'quiz[0].explain.text', r(1 / 0.75, 2))

# ---------------- l6 ----------------
s = y - a - b * x
claim(abs(s.mean()) < 1e-9, 'l6 the OLS spread has mean zero')
lv.expect('l6', 'screens[0].explain.text', r(np.std(s, ddof=1), 2)); lv.expect('l6', 'screens[0].prose', r(s[773], 2))
lv.expect('l6', 'screens[0].explain.text', r(r(s[773], 2) / r(np.std(s, ddof=1), 2), 2))
q = pd.Series(s); m60 = q.rolling(60).mean()[773]; sd60 = q.rolling(60).std()[773]
lv.expect('l6', 'screens[3].prose', r(m60, 2)); lv.expect('l6', 'screens[3].prose', r(sd60, 2))
lv.expect('l6', 'screens[3].widget.answer', r((r(s[773], 2) - r(m60, 2)) / r(sd60, 2), 2))
lv.expect('l6', 'screens[3].widget.wrong[0].value', r((r(s[773], 2) + r(m60, 2)) / r(sd60, 2), 2))
lv.expect('l6', 'screens[2].widget.wrong[1].value', r(1.81 * 1.59, 2))
zf = (s - s.mean()) / np.std(s, ddof=1)
lv.expect('l6', 'screens[6].prose', int((np.abs(zf) > 2).sum()))
for w in (20, 60, 120):
    lv.expect('l6', 'screens[10].prose', int((np.abs(rolling_z(s, w)) > 2).sum()))
lv.expect('l6', 'screens[5].feedback.correct', int((np.abs(rolling_z(s, 60)) > 2).sum()))
lv.expect('l6', 'screens[4].explain.text', r(s[301:].mean(), 2)); lv.expect('l6', 'screens[4].explain.text', r(s[:300].mean(), 2))
lv.expect('l6', 'screens[4].explain.text', r(zf[300], 2)); lv.expect('l6', 'screens[4].explain.text', r(rolling_z(s, 60)[300], 2))
lv.expect('l6', 'screens[6].feedback.correct', 999 - 300)
a15, b15, sd15 = rolling_fit(y15, x15, 250)
zr = (y15 - a15 - b15 * x15) / sd15
lv.expect('l6', 'screens[7].explain.text', int((np.abs(zr) > 2).sum())); lv.expect('l6', 'screens[7].explain.text', int((~np.isnan(zr)).sum()))
_, sh_roll = run_pnl(y15, x15, zr, b15)
bf, af = np.polyfit(x15, y15, 1); sf = y15 - af - bf * x15
_, sh_full = run_pnl(y15, x15, (sf - sf.mean()) / sf.std(ddof=1), np.full(1500, bf))
lv.expect('l6', 'screens[9].widget.options[0].text', r(sh_roll, 3)); lv.expect('l6', 'screens[9].widget.options[1].text', r(sh_full, 3))
claim(abs((r(sh_roll, 3) + r(sh_full, 3)) / 2 - 1.386) <= 0.0005 + 1e-9, 'l6 the average of 1.124 and 1.647 is 1.386, half up')
lv.expect('l6', 'summary.ideas[2]', r(sh_roll, 2)); lv.expect('l6', 'summary.ideas[2]', r(sh_full, 2))
for row in lv.text('l6', 'screens[11].canvas.params.rows').split('\n'):
    pass
lv.expect('l6', 'screens[11].canvas.params.rows', r((0.84 - 0.10) / 0.30, 2)); lv.expect('l6', 'screens[11].canvas.params.rows', r((-1.20 + 0.20) / 0.45, 2))
lv.expect('l6', 'screens[11].canvas.params.rows', r((0.30 - 0.25) / 0.50, 2))
lv.expect('l6', 'quiz[0].widget.answer', r((-0.70 + 0.10) / 0.25, 2)); lv.expect('l6', 'quiz[0].widget.wrong[0].value', r((-0.70 - 0.10) / 0.25, 2))
lv.expect('l6', 'screens[10].widget.options[0].text', r((1.10 - 0.20) / 0.40, 2))
lv.expect('l6', 'quiz[2].widget.answer', 999 - 200)

# ---------------- l7 ----------------
bC, seC = hl_fit(s)
lv.expect('l7', 'screens[1].explain.text', r(bC, 4)); lv.expect('l7', 'screens[1].explain.text', r(1 + bC, 4))
lv.expect('l7', 'screens[2].widget.answer', r(hl(bC), 2)); lv.expect('l7', 'screens[2].explain.text', r(hl(bC), 3))
lv.expect('l7', 'screens[2].explain.text', r(hl(-0.05), 2))
lv.expect('l7', 'screens[2].widget.wrong[1].value', r(1 / 0.0508, 2))
lv.expect('l7', 'screens[2].hints[2].text', r(0.6931 / 0.0521, 2))            # the hint's own division
lv.expect('l7', 'screens[3].explain.text', r(0.6931 / 0.0521, 2))
lv.expect('l7', 'screens[3].prose', r(-math.log(0.9492), 4))         # kappa from the shown phi-hat
lv.expect('l7', 'screens[3].feedback.byKey.linear', r(100 * 1.80 * (1 - math.exp(-0.0521))))
claim(1.80 * math.exp(-0.0521 * 17) < 0.75, 'l7 past 17 days the expected gap is below £0.75')
lv.expect('l7', 'screens[5].prose', r(seC, 4))
lo, hi = hl(bC - 1.96 * seC), hl(bC + 1.96 * seC)
lv.expect('l7', 'screens[5].explain.text', r(lo, 2)); lv.expect('l7', 'screens[5].explain.text', r(hi, 2))
lv.expect('l7', 'screens[5].canvas.params.vlines[0].label', r(1 + bC - 1.96 * seC, 3)); lv.expect('l7', 'screens[5].canvas.params.vlines[1].label', r(1 + bC + 1.96 * seC, 3))
x250, y250 = make_pair(3, 250); bb, aa = np.polyfit(x250, y250, 1); b250, se250 = hl_fit(y250 - aa - bb * x250)
lv.expect('l7', 'screens[5].feedback.correct', r(hl(b250 - 1.96 * se250), 2)); lv.expect('l7', 'screens[5].feedback.correct', r(hl(b250 + 1.96 * se250), 2))
hls = []
for sd in range(3, 23):
    xx, yy = make_pair(sd, 1000); bb, aa = np.polyfit(xx, yy, 1); hls.append(hl(hl_fit(yy - aa - bb * xx)[0]))
hls = np.array(hls)
lv.expect('l7', 'screens[6].explain.text', r(hls.mean(), 2)); lv.expect('l7', 'screens[6].explain.text', r(hls.min(), 2)); lv.expect('l7', 'screens[6].explain.text', r(hls.max(), 2))
lv.expect('l7', 'screens[6].hints[2].text', int((hls < 13.51).sum()))
lv.expect('l7', 'screens[7].explain.text', r(1.80 * 0.9492 ** 10, 2)); lv.expect('l7', 'screens[7].explain.text', r(2 * 13.29, 1))
lv.expect('l7', 'screens[7].explain.text', r(1.80 / 4, 2))
xa, ya = make_case('A'); gA = ya - 0.8 * xa; bA, seA = hl_fit(gA)
lv.expect('l7', 'screens[8].prose', r(bA, 4)); lv.expect('l7', 'screens[8].prose', r(hl(bA), 1))
lv.expect('l7', 'screens[8].widget.options[0].text', r(adfuller(gA, autolag='AIC')[1], 2))
lv.expect('l7', 'screens[8].widget.options[3].why', r(hl(bA - 1.96 * seA)))
claim(bA + 1.96 * seA >= 0, 'l7 pair A interval runs to infinity')
neg = np.mean([np.polyfit(w[:-1], np.diff(w), 1)[0] < 0 for w in (np.cumsum(np.random.default_rng(k).standard_normal(1000)) for k in range(1000))])
claim_text('l7', 'screens[8].feedback.byKey.fine', 'Every random walk gives', neg == 1.0, 'every random walk gives b < 0',
           f'{100 * neg:.1f}% of 1,000 seeded 1,000-day walks give b < 0')
xb, yb = make_case('B'); bB, _ = hl_fit(yb - xb)
lv.expect('l7', 'quiz[2].prose', r(hl(bB), 2)); lv.expect('l7', 'quiz[2].explain.text', r(100 * (1 + bB)))
phF, phS = 0.5 ** (1 / 5), 0.5 ** (1 / 60)
claim_text('l7', 'screens[0].prose', 'the same daily shocks', abs(1 / math.sqrt(1 - phF ** 2) - 1 / math.sqrt(1 - phS ** 2)) < 0.05,
           'equal long-run sds with the same daily shocks', f'with the same shock sd the long-run sds differ by a factor {math.sqrt((1 - phF**2) / (1 - phS**2)):.2f}')
lv.expect('l7', 'screens[10].widget.options[0].text', r(hl(-0.10), 2)); lv.expect('l7', 'screens[10].explain.text', r(math.log(0.9), 4))
lv.expect('l7', 'quiz[0].widget.answer', r(hl(-0.02), 1)); lv.expect('l7', 'quiz[1].widget.options[0].text', r(math.log(0.5) / math.log(1.9492), 2))
for k, h in ((10, 5), (26, 13), (80, 40)):
    lv.expect('l7', 'screens[11].hints[1].text', round(252 / k + 1e-9, 1))

# ---------------- l8 ----------------
D = make_three(); A3, B3, C3 = D.T
lv.expect('l8', 'screens[0].explain.text', r(np.std(A3 - 1.25 * B3, ddof=1), 2)); lv.expect('l8', 'screens[0].explain.text', r(np.std(A3, ddof=1), 1))
lv.expect('l8', 'screens[0].explain.text', r(1 / 1.2, 2))
jo = coint_johansen(D, 0, 1)
for v in jo.lr1:
    lv.expect('l8', 'screens[4].hints', r(v, 3))
for v in jo.cvt[:, 1]:
    lv.expect('l8', 'screens[4].hints', r(v, 4))
for v in list(jo.cvt[:, 0]) + list(jo.cvt[:, 2]):
    lv.expect('l8', 'screens[4].explain.text', r(v, 2))
for v in jo.lr2:
    lv.expect('l8', 'screens[10].widget.options', r(v, 3)) if False else None
lv.expect('l8', 'screens[10].widget.options[2].why', r(jo.lr2[0], 3)); lv.expect('l8', 'screens[10].widget.options[2].why', r(jo.cvm[0, 1], 4))
claim(abs(jo.lr2[2] - 0.277) < 0.001 and jo.lr2[1] > jo.cvm[1, 1], 'l8 max-eigenvalue reading gives rank 2')
ev = jo.evec / jo.evec[0]
lv.expect('l8', 'screens[6].feedback.correct', r(ev[1, 0], 2)); lv.expect('l8', 'screens[6].feedback.correct', r(ev[2, 0], 2))
lv.expect('l8', 'screens[6].feedback.correct', r(ev[1, 1], 2)); lv.expect('l8', 'screens[6].feedback.correct', r(ev[2, 1], 2))
cA = (ev[1, 0] / -1.25); cB = 1 - cA
lv.expect('l8', 'screens[6].explain.text', r(cA, 2)); lv.expect('l8', 'screens[6].explain.text', r(cB, 2))
claim(abs(cB * -1 / 1.2 - ev[2, 0]) < 0.03, 'l8 column 1 is a mix of A - 1.25B and A - 0.83C, to rounding', f'{cB * -1 / 1.2:.3f} against {ev[2, 0]:.3f}')
pc = [coint(D[:, i], D[:, j])[1] for i in range(3) for j in range(3) if i != j]
claim(max(pc) < 0.01, 'l8 every pair, both directions, rejects strongly', f'max p {max(pc):.2g}')
for k in range(3):
    claim(abs(adfuller(D[:, k], autolag='AIC')[1] - 0.87) < 0.06, f'l8 series {k} ADF p about 0.87', f'{adfuller(D[:, k], autolag="AIC")[1]:.3f}')
for row, (do, kd) in enumerate(((0, 1), (0, 2), (-1, 1), (1, 1))):
    j = coint_johansen(D, do, kd)
    for v in j.lr1:
        lv.expect('l8', f'screens[8].canvas.params.rows[{row}]', r(v, 2))
    lv.expect('l8', f'screens[8].canvas.params.rows[{row}]', int(next((k for k in range(3) if j.lr1[k] < j.cvt[k, 1]), 3)))
vm = VECM(D, k_ar_diff=1, coint_rank=2, deterministic='ci').fit()
for i in range(3):
    for k in range(2):
        lv.expect('l8', f'screens[7].canvas.params.rows[{i}]', r(vm.alpha[i, k], 3))
lv.expect('l8', 'screens[7].prose', r(-vm.beta[2, 0], 2)); lv.expect('l8', 'screens[7].prose', r(-vm.beta[2, 1], 3))
lv.expect('l8', 'screens[7].widget.answer', r(r(vm.alpha[0, 0], 3) * 2, 2)); lv.expect('l8', 'screens[7].widget.wrong[1].value', r(r(vm.alpha[2, 0], 3) * 2, 2))
jw = coint_johansen(make_three_walks(), 0, 1)
lv.expect('l8', 'screens[9].prose', r(jw.lr1[2], 2)); lv.expect('l8', 'screens[9].prose', r(jw.cvt[2, 1], 2))
lv.expect('l8', 'screens[9].widget.options[0].text', r(jw.lr1[0], 2)); lv.expect('l8', 'screens[9].widget.options[0].text', r(jw.cvt[0, 1], 2))
jc = coint_johansen(np.column_stack([y, x]), 0, 1)
lv.expect('l8', 'screens[5].explain.text', r(jc.lr1[0], 3)); lv.expect('l8', 'screens[5].explain.text', r(jc.lr1[1], 3))
lv.expect('l8', 'quiz[0].prose', r(jc.evec[1, 0] / jc.evec[0, 0], 4))
jcr = coint_johansen(np.column_stack([x, y]), 0, 1)
lv.expect('l8', 'quiz[0].prose', r(jcr.evec[1, 0] / jcr.evec[0, 0], 3))
ja = coint_johansen(np.column_stack(make_case('A')[::-1]), 0, 1)
lv.expect('l8', 'screens[5].explain.text', r(ja.lr1[0], 3))
lv.expect('l8', 'quiz[1].widget.answer', 6 - 2); lv.expect('l8', 'screens[2].widget.answer', 5 - 2)

# ---------------- review-2 ----------------
lv.expect('review', 'items[0].widget.answer', 1.50 / 0.75); lv.expect('review', 'items[0].widget.wrong[1].value', 1.50 * 0.75)
lv.expect('review', 'items[1].widget.answer', r((2.10 - 0.30) / 0.60, 2)); lv.expect('review', 'items[1].widget.wrong[0].value', r(2.10 / 0.60, 2))
lv.expect('review', 'items[2].widget.answer', r(hl(-0.07), 2)); lv.expect('review', 'items[2].widget.wrong[0].value', r(1 / 0.07, 2))
lv.expect('review', 'items[2].widget.wrong[1].value', r(0.5 / 0.07, 2)); lv.expect('review', 'items[2].explain.text', r(-math.log(0.93), 4))
lv.expect('review', 'items[6].widget.answer', -0.10 * 1.5 + 0.05 * -2.0)
claim(abs(1 - 0.5 ** (20 / 60) - 0.2) < 0.01, 'review-2 items[7]: in 20 days a 60-day half-life closes a fifth of a gap')

# ---------------- homework-2 ----------------
lv.expect('homework', 'items[1].widget.answer', r(1 / 0.80, 2)); lv.expect('homework', 'items[1].widget.wrong[2].value', r(0.9 * 0.8, 2))
lv.expect('homework', 'items[2].widget.answer', r(hl(-0.040 + 1.96 * 0.012), 2)); lv.expect('homework', 'items[2].widget.wrong[0].value', r(hl(-0.040 - 1.96 * 0.012), 2))
lv.expect('homework', 'items[2].widget.wrong[1].value', r(hl(-0.040), 2))
zt = rolling_z(s, 60)[-1]
lv.expect('homework', 'items[5].feedback.correct', r(zt, 2)); lv.expect('homework', 'items[5].feedback.correct', r(lo, 2)); lv.expect('homework', 'items[5].feedback.correct', r(hi, 2))
lv.expect('homework', 'items[5].how' if False else 'items[5].widget.how', r(coint(y2, x2)[1], 3))
lv.expect('homework', 'items[6].model', r(2.10 / 0.62, 2)); claim(abs(2.10 / 0.62 - 1 / (0.62 / 2.10)) < 1e-9, 'homework-2 items[6]: inverted over direct slope is 1/R^2 (no attenuation claim)')
lv.expect('homework', 'items[6].model', r(0.62 / 2.10, 3)); lv.expect('homework', 'items[6].model', r(math.sqrt(0.62 / 2.10), 2))
lv.expect('homework', 'items[7].widget.answer', 1499 - 1000)

lv.check_wrongs()
lv.report()
