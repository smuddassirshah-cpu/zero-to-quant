"""Second-reader number checks for arma level 1 (l1 to l4, review-1, homework-1).

Every number below is recomputed from the course generators (copied from the lesson preludes) in CPython with
NumPy and statsmodels, or from its closed form, and then looked up in the JSON where it is stated
(app/tools/numbers_lib.py). Claims that are not single numbers are checked with `claim(...)`.
A failing check here means the content is wrong; it stays failing until the fix pass changes the content
(see docs/reviews/review-arma.md). Run: python3 docs/reports/arma-L1-numbers.py
"""
import math, os, sys, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')
from statsmodels.tsa.stattools import adfuller, kpss
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('arma', 1)


def claim(ok, label, note=''):
    return lv._rec(bool(ok), 'claim: ' + label, note)


def claim_text(ref, path, phrase, ok, label, note=''):
    """A claim tied to the content: it fails only while `phrase` is still in the text at `path` and the fact is false."""
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', note + ('' if present else ' (phrase gone)'))


def make_price(seed, n=2000):
    rng = np.random.default_rng(seed)
    r = 0.0003 + 0.012 * rng.standard_normal(n - 1)
    return 100 * np.exp(np.concatenate([[0.0], np.cumsum(r)]))


def make_ar1(phi, n, seed, c=0.0):
    e = np.random.default_rng(seed).standard_normal(n)
    x = np.empty(n); x[0] = e[0]
    for t in range(1, n):
        x[t] = c + phi * x[t - 1] + e[t]
    return x


def make_walk(seed, n=500, drift=0.0):
    return np.cumsum(drift + np.random.default_rng(seed).standard_normal(n))


def fit(x, y):
    b, a = np.polyfit(x, y, 1)
    return a, b, np.corrcoef(x, y)[0, 1] ** 2


def r(v, k):
    return round(float(v), k)


def canvas_series(ref, screen, side=None, idx=0):
    _, doc = lv._file(ref)
    c = doc['screens'][screen]['canvas']
    c = c[side] if side else c
    return np.array([np.nan if v is None else v for v in c['params']['series'][idx]['values']], float)


# ---------------- l1 ----------------
p = make_price(12)
dates = pd.bdate_range('2016-01-04', periods=2000)
yrs = np.array([d.year for d in dates])
tr = p[:750]
lv.expect('l1', 'screens[0].explain.text', r(tr.min(), 2))                 # 98.82
lv.expect('l1', 'screens[0].explain.text', r(tr.max(), 2))                 # 161.42
lv.expect('l1', 'screens[0].explain.text', r(p[yrs == 2023].min(), 2))     # 217.58
lv.expect('l1', 'screens[0].hints[2].text', round(tr.min()))               # 99
claim(abs(p[yrs == 2023].max() - 255.95) < 0.005, '2023 closes end below £256 (screens[0].options[1].why)')
lr = np.diff(np.log(p))
lv.expect('l1', 'screens[0].explain.text', r(100 * lr[:749].std(ddof=1), 2))        # 1.19
lv.expect('l1', 'screens[0].explain.text', r(100 * lr[yrs[1:] == 2023].std(), 2))   # 1.29 (ddof 0; ddof 1 gives 1.30)
lv.expect('l1', 'screens[1].explain.text', round(1.2 * math.sqrt(1000)))            # 38
lv.expect('l1', 'screens[1].explain.text', round(1.2 * math.sqrt(2000)))            # 54
lv.expect('l1', 'screens[1].hints[2].text', round(2 * 1.2 * math.sqrt(1000)))       # 76
bl = np.array_split(p, 4)
means = [b.mean() for b in bl]; sds = [b.std(ddof=1) for b in bl]
claim(max(sds) < min(np.diff(means)), 'every 4-block sd is smaller than every gap between block means (screens[2].explain)')
claim(1.9 < means[-1] / means[0] < 2.1, 'the block mean roughly doubles (screens[2].explain)')
x6 = np.array([100, 102, 99, 97, 96, 94.])
a6, b6, _ = fit(x6[:-1], x6[1:])
lv.expect('l1', 'screens[4].explain.text', r(a6, 2))                        # -0.33
lv.expect('l1', 'screens[4].explain.text', r(b6, 4))                        # 0.9912
lv.expect('l1', 'screens[4].widget.rows[6][2].answer', r(b6, 2))
_, bp, r2p = fit(p[:-1], p[1:]); _, blp, r2lp = fit(np.log(p[:-1]), np.log(p[1:])); _, brr, r2r = fit(lr[:-1], lr[1:])
lv.expect('l1', 'screens[5].explain.text', r(bp, 4))                        # 0.9988
lv.expect('l1', 'screens[5].explain.text', r(blp, 4))                       # 0.9987
lv.expect('l1', 'screens[5].explain.text', r(brr, 4))                       # 0.0161
lv.expect('l1', 'screens[6].prose', r(r2p, 4))                              # 0.9977
lv.expect('l1', 'screens[6].widget.options[2].why', r(r2lp, 4))             # 0.9981
lv.expect('l1', 'screens[6].explain.text', r(r2r, 4))                       # 0.0003
a, b, _ = fit(p[:749], p[1:750])
y, yh = p[750:], a + b * p[749:-1]
oos = 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()
lv.expect('l1', 'screens[6].widget.options[3].why', r(oos, 2))             # FAILS until fixed: content says 0.998, out of sample it is 0.994
lv.expect('l1', 'screens[9].prose', r(a, 3)); lv.expect('l1', 'screens[9].prose', r(b, 4))
lv.expect('l1', 'screens[9].prose', r(a / (1 - b), 2))                      # 144.48
lv.expect('l1', 'screens[9].prose', r(p[-1], 2))                            # 248.15
lv.expect('l1', 'screens[9].widget.options[1].why', r(p[749], 2))           # 153.34
lv.expect('l1', 'screens[9].widget.options[2].why', r(p.mean(), 2))         # 174.88
lv.expect('l1', 'screens[9].hints[2].text', r(0.563 / (1 - 0.9961), 1))     # FAILS: 0.563/0.0039 = 144.4, the hint says 144.5
lv.expect('l1', 'screens[8].widget.options[1].why', round(tr.mean()))       # 126
q6 = make_price(6); _, b6s, _ = fit(q6[:749], q6[1:750])
lv.expect('l1', 'screens[10].explain.text', r(b6s, 2))                      # 0.98
lv.expect('l1', 'screens[10].explain.text', round(100 * (10.8531 / 6.3305 - 1)))   # 71
bond = 100 + 0.25 * make_ar1(0.9, 500, 5)
claim(np.allclose(bond, canvas_series('l1', 7, 'left'), atol=1e-3), 'the bond panel is 100 + 0.25 make_ar1(0.9, 500, 5)')
st = canvas_series('l1', 7, 'right')
lv.expect('l1', 'screens[7].hints[2].text', r(st[:250].std(ddof=1), 1))      # 0.7
claim(abs(st[250:].std(ddof=1) - 2.2) < 0.15, 'stormy sd about 2.2% (sample 2.11)')
lv.expect('l1', 'quiz[0].widget.answer', r(math.log(245 / 250), 4))
lv.expect('l1', 'quiz[0].widget.wrong[0].value', 245 / 250 - 1)
lv.expect('l1', 'quiz[3].widget.options[2].why', 'tripled')
claim(2.1 / 0.6 > 3, 'quiz[3]: 2.1/0.6 more than triples')

# ---------------- l2 ----------------
A = canvas_series('l2', 0, None, 0)
claim(abs(A[:20].mean() - 22) < 1.5 and abs(A[-20:].mean() - 32) < 1.5, 'series A climbs from about 22 to 32 (screens[0].byKey.level)')
B = canvas_series('l2', 0, None, 1)
claim(2.5 < B[250:].std(ddof=1) / B[:250].std(ddof=1) < 3.5, 'series B swings about three times wider after day 250')
top1 = canvas_series('l2', 1, 'left', 0)
lv.expect('l2', 'screens[1].explain.text', r(math.sqrt(1 / 0.75), 2))      # 1.15, the AR(0.5) sd (sample 1.135)
ar161, w1161 = make_ar1(0.95, 250, 161), make_walk(1161, 250)
claim(np.allclose(ar161, canvas_series('l2', 5, 'left'), atol=1e-3), 'l2 trap top panel is make_ar1(0.95, 250, 161)')
lv.expect('l2', 'screens[5].explain.text', r(np.ptp(ar161), 1))             # 18.6
lv.expect('l2', 'screens[5].explain.text', r(np.ptp(canvas_series('l2', 5, 'right')), 1))   # 10.4
lv.expect('l2', 'screens[5].hints[1].text', r(0.95 ** 10, 2)); lv.expect('l2', 'screens[5].hints[1].text', r(0.95 ** 20, 2))
lv.expect('l2', 'screens[5].hints[2].text', round(math.log(0.5) / math.log(0.95)))          # 14
lv.expect('l2', 'screens[7].explain.text', r(1 / (1 - 0.95 ** 2), 2))      # 10.26
lv.expect('l2', 'screens[7].explain.text', r(1 / 0.75, 2))                 # 1.33
lv.expect('l2', 'screens[8].explain.text', r(make_ar1(0.5, 20000, 11)[100:].var(), 3))     # 1.353
lv.expect('l2', 'quiz[1].widget.answer', r(1 / (1 - 0.64), 3))
lv.expect('l2', 'quiz[1].widget.wrong[0].value', 1 / (1 - 0.8))
brk = canvas_series('l2', 6)
claim(abs(brk[:250].mean()) < 0.2 and abs(brk[250:].mean() - 4) < 0.2, 'the break series has means 0 and 4')
ret10 = canvas_series('l2', 10, 'left')
claim(2.7 < ret10[250:].std(ddof=1) / ret10[:250].std(ddof=1) < 3.6, 'the calm-to-stormy sd roughly triples (screens[10].explain)')

# ---------------- l3 ----------------
w71, a72 = make_walk(71, 500), make_ar1(0.9, 500, 72)
claim(np.allclose(w71, canvas_series('l3', 0, 'left'), atol=1e-3), 'l3 hook top is make_walk(71, 500)')
lv.expect('l3', 'screens[0].explain.text', r(math.log(0.5) / math.log(0.9), 1))           # 6.6
import statsmodels.api as sm
f = sm.OLS(np.diff(a72), sm.add_constant(a72[:-1])).fit()
lv.expect('l3', 'screens[1].widget.accept', r(f.params[1], 4)); lv.expect('l3', 'screens[1].widget.accept', r(f.bse[1], 4))
lv.expect('l3', 'screens[1].widget.answer', r(f.tvalues[1], 2))
lv.expect('l3', 'screens[1].widget.wrong[0].value', r(f.bse[1] / f.params[1], 3))
lv.expect('l3', 'screens[1].explain.text', r(1 + f.params[1], 3))
lv.expect('l3', 'screens[2].explain.text', r(adfuller(a72, maxlag=0, regression='c', autolag=None)[0], 4))
W = np.cumsum(np.random.default_rng(2024).standard_normal((2000, 250)), axis=1)


def df_t_many(W):
    dx, xl = np.diff(W, axis=1), W[:, :-1]
    m = dx.shape[1]
    xm, ym = xl.mean(1, keepdims=True), dx.mean(1, keepdims=True)
    sxx = ((xl - xm) ** 2).sum(1)
    bb = ((xl - xm) * (dx - ym)).sum(1) / sxx
    res = dx - ym - bb[:, None] * (xl - xm)
    return bb / np.sqrt((res ** 2).sum(1) / (m - 2) / sxx)


t0 = df_t_many(W)
lv.expect('l3', 'screens[3].explain.text', r(t0.mean(), 2))                 # -1.52
lv.expect('l3', 'screens[3].explain.text', r(100 * (t0 < -1.645).mean(), 2))   # 45.25
lv.expect('l3', 'screens[3].explain.text', r(np.quantile(t0, 0.05), 2))    # -2.89
lv.expect('l3', 'screens[4].explain.text', r(np.quantile(t0, 0.01), 2))
lv.expect('l3', 'screens[4].explain.text', r(np.quantile(t0, 0.10), 2))
sp = adfuller(make_ar1(0.97, 500, 114), autolag='AIC')
lv.expect('l3', 'screens[5].prose', r(sp[0], 2)); lv.expect('l3', 'screens[5].prose', r(sp[1], 3))
for k in ('1%', '5%', '10%'):
    lv.expect('l3', 'screens[5].prose', r(sp[4][k], 2))
aw = adfuller(w71, autolag='AIC')
lv.expect('l3', 'screens[6].explain.text', r(aw[0], 4)); lv.expect('l3', 'screens[6].explain.text', r(aw[1], 4))
lv.expect('l3', 'screens[11].prose', r(aw[0], 2)); lv.expect('l3', 'screens[11].prose', r(aw[1], 2))
lv.expect('l3', 'screens[6].explain.text', r(adfuller(make_ar1(0.8, 500, 73), autolag='AIC')[0], 4))
lv.expect('l3', 'screens[6].explain.text', r(adfuller(p, autolag='AIC')[1], 4))
lv.expect('l3', 'screens[6].explain.text', r(adfuller(lr, autolag='AIC')[0], 4))
lv.expect('l3', 'screens[8].explain.text', r(adfuller(ar161, autolag='AIC')[1], 2))   # 0.45, last lesson's phi = 0.95 series


def power(phi, n, sims, seed):
    e = np.random.default_rng(seed).standard_normal((sims, n))
    X = np.empty_like(e); X[:, 0] = e[:, 0]
    for t in range(1, n):
        X[:, t] = phi * X[:, t - 1] + e[:, t]
    return float(np.mean(df_t_many(X) < -2.86))


pw = {ph: power(ph, 250, 2000, 7) for ph in (0.98, 1.0)}
lv.expect('l3', 'screens[7].explain.text', r(pw[1.0], 2)); claim(pw[1.0] > 0.05, 'size at phi = 1 is slightly above 5%', f'{pw[1.0]:.4f}')
lv.expect('l3', 'screens[8].widget.answer', r(pw[0.98], 2))
lv.expect('l3', 'screens[7].explain.text', round(100 * power(0.98, 1000, 1000, 3)))     # 85
claim(kpss(w71, regression='c', nlags='auto')[1] <= 0.01, 'KPSS rejects stationarity of the walk at 1% (screens[9])')
# no-constant claim (quiz[1], screens[2].explain, screens[10].options[2].why): "the series looks like a walk"
rej = np.mean([adfuller(5 + np.random.default_rng(1000 + s).standard_normal(250), maxlag=0, regression='n', autolag=None)[1] < 0.05 for s in range(200)])
for path, ph in (('quiz[1].widget.options[0].text', 'looks like a walk'), ('screens[2].explain.text', 'would look like a walk'), ('screens[10].widget.options[2].why', 'then looks like a walk')):
    claim_text('l3', path, ph, rej < 0.5, 'with no constant a series around 5 looks like a walk', f'no-constant test rejects {rej:.2f} of 200 at 5%')

# ---------------- l4 ----------------
tr4 = canvas_series('l4', 4, 'left', 0)
d4 = np.diff(tr4)
lv.expect('l4', 'screens[4].explain.text', r(np.corrcoef(d4[:-1], d4[1:])[0, 1], 2))   # -0.49
res6 = canvas_series('l4', 6, 'right')
claim_text('l4', 'screens[6].explain.text', 'start and end near 0', abs(res6[0]) < 2 and abs(res6[-1]) < 2, 'a detrended walk starts and ends near 0', f'first {res6[0]:.2f}, last {res6[-1]:.2f}')
rw = canvas_series('l4', 6, 'left', 0)
tt = np.arange(len(rw)); bb_, aa_ = np.polyfit(tt, rw, 1)
lv.expect('l4', 'screens[6].prose', r(adfuller(rw - (aa_ + bb_ * tt), autolag='AIC')[1], 2))   # 0.46
lv.expect('l4', 'screens[7].widget.options[2].why', r(adfuller(rw, regression='ct', autolag='AIC')[1], 2))   # 0.77
ard = canvas_series('l4', 9, 'left')
a82 = make_ar1(0.5, 500, 82)
claim(np.allclose(np.diff(a82), ard[~np.isnan(ard)], atol=1e-3), 'l4 screens[9] top is diff(make_ar1(0.5, 500, 82))')
ac = ard[~np.isnan(ard)]
lv.expect('l4', 'screens[9].prose', r(np.corrcoef(ac[:-1], ac[1:])[0, 1], 2))   # -0.28: FAILS until the prose states the lag-1 correlation (finding 1)
phi = 0.5
var_x, var_dx = 1 / (1 - phi ** 2), 2 / (1 + phi)
claim_text('l4', 'screens[9].widget.options[0].text', 'adds noise', var_dx > var_x + 1e-9, 'differencing an AR(1) with phi = 0.5 adds noise (raises its variance)', f'theory: Var(x) = {var_x:.4f}, Var(dx) = {var_dx:.4f}')
lv.expect('l4', 'screens[10].explain.text', round(adfuller(lr, autolag='AIC')[0]))   # -44
brd = canvas_series('l4', 9, 'right')
big = int(np.nanargmax(np.abs(brd)))
for path, ph in (('screens[9].widget.options[1].text', 'single spike'), ('screens[9].hints[2].text', 'one large change')):
    claim_text('l4', path, ph, big == 250, 'the break shows as one large change on day 250',
               f'day 250 change {brd[250]:.3f}; largest {brd[big]:.3f} on day {big}; {int((np.abs(brd) > abs(brd[250])).sum())} days larger')


# ---------------- review-1 and homework-1 ----------------
lv.expect('review', 'items[0].widget.answer', r(math.log(1.08), 3))
lv.expect('review', 'items[0].explain.text', r(math.log(1.2), 4)); lv.expect('review', 'items[0].explain.text', r(-math.log(108 / 120), 4))
lv.expect('review', 'items[3].widget.answer', 1.2 / 0.01)
lv.expect('review', 'items[3].widget.wrong[1].value', 1.2 * 0.99)
lv.expect('review', 'items[4].widget.answer', r(0.25 / 0.19, 4))
lv.expect('review', 'items[4].widget.wrong[0].value', r(0.5 / 0.19, 4))
lv.expect('review', 'items[4].widget.wrong[1].value', r(0.25 / 0.1, 4))
p96_250, p96_500 = power(0.96, 250, 2000, 11), power(0.96, 500, 2000, 11)
lv.expect('review', 'items[6].prose', round(100 * p96_250)); lv.expect('review', 'items[6].prose', round(100 * p96_500))
lv.expect('review', 'items[6].widget.options[1].why', round(100 * (1 - p96_250)))
lv.expect('review', 'items[6].explain.text', round(100 * p96_250)); lv.expect('review', 'items[6].explain.text', round(100 * p96_500))
# review-1 items[7]: new seeded pair (finding 22)
rA = make_walk(31, 500, drift=0.1); rB = 5 + 0.03 * np.arange(500) + make_ar1(0.5, 500, 32)
_, _rv = lv._file('review')
_rows = _rv['items'][7]['canvas']['params']['rows']
for _nm, _x, _row in (('A', rA, _rows[0]), ('B', rB, _rows[1])):
    _pc, _pt = adfuller(_x, regression='c', autolag='AIC')[1], adfuller(_x, regression='ct', autolag='AIC')[1]
    for _cell, _p in ((_row[1], _pc), (_row[2], _pt)):
        claim((_cell.startswith('<') and _p < float(_cell.split()[-1])) or (not _cell.startswith('<') and abs(float(_cell) - _p) < 0.0051), f'review items[7] row {_nm}: {_cell} matches ADF p {_p:.4g}')
lv.expect('review', 'items[7].explain.text', 0.995); lv.expect('review', 'items[7].explain.text', 0.40)
# review-1 items[4]: variance 0.5^2 / (1 - 0.81)
lv.expect('review', 'items[4].prose', 0.9); lv.expect('review', 'items[4].prose', 0.5)
# l4 screens[9] (finding 35): day 250's change, and finding 3's residual start
lv.expect('l4', 'screens[9].widget.options[3].why', r(brd[250], 2)); lv.expect('l4', 'screens[9].hints[2].text', r(brd[250], 2))
claim(int((np.abs(brd) > abs(brd[250])).sum()) > 0, 'day 250 change is smaller than some ordinary days (screens[9] explain)')
lv.expect('l4', 'screens[6].explain.text', r(res6[0], 1))
lv.expect('homework', 'items[2].widget.answer', -0.045 / 0.012)
lv.expect('homework', 'items[2].widget.wrong[1].value', r(0.012 / -0.045, 4))
lv.expect('homework', 'items[2].explain.text', round(math.log(0.5) / math.log(0.955)))   # 15
lv.expect('homework', 'items[7].model', round(6.1 / 0.0009, -1))   # 6,780
lv.expect('homework', 'items[7].model', 144.48)
claim_text('homework', 'items[4].widget.options[1].why', 'start and end near 0', abs(res6[0]) < 2 and abs(res6[-1]) < 2, 'a detrended walk is forced to start and end near 0', f'l4 example starts at {res6[0]:.2f}')

lv.check_wrongs()
lv.report()
