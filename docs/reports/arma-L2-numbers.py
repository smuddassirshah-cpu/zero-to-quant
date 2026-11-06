"""Second-reader number checks for arma level 2 (l5 to l8, review-2, homework-2).

Every number is recomputed from the course generators (copied from the lesson preludes) with NumPy, SciPy and
statsmodels in CPython, or from its closed form, then looked up where it is stated (app/tools/numbers_lib.py).
ARIMA values are compared after rounding to the places shown. Claims that are not single numbers use `claim(...)`.
A failing check means the content is wrong (see docs/reviews/review-arma.md) and stays failing until fixed.
Run: python3 docs/reports/arma-L2-numbers.py
"""
import math, os, sys, warnings
import numpy as np
warnings.filterwarnings('ignore')
from scipy.stats import chi2
from statsmodels.tsa.stattools import acf, pacf, adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('arma', 2)


def claim(ok, label, note=''):
    return lv._rec(bool(ok), 'claim: ' + label, note)


def claim_text(ref, path, phrase, ok, label, note=''):
    """A claim tied to the content: it fails only while `phrase` is still in the text at `path` and the fact is false."""
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', note + ('' if present else ' (phrase gone)'))


def r(v, k):
    return round(float(v), k)


def make_price(seed, n=2000):
    rng = np.random.default_rng(seed)
    return 100 * np.exp(np.concatenate([[0.0], np.cumsum(0.0003 + 0.012 * rng.standard_normal(n - 1))]))


def make_ar1(phi, n, seed, c=0.0):
    e = np.random.default_rng(seed).standard_normal(n)
    x = np.empty(n); x[0] = e[0]
    for t in range(1, n):
        x[t] = c + phi * x[t - 1] + e[t]
    return x


def make_walk(seed, n=500, drift=0.0):
    return np.cumsum(drift + np.random.default_rng(seed).standard_normal(n))


def make_wn(seed, n=500):
    return np.random.default_rng(seed).standard_normal(n)


def make_arma(phis, thetas, n, seed, burn=200):
    e = np.random.default_rng(seed).standard_normal(n + burn)
    x = np.zeros(n + burn)
    for t in range(n + burn):
        v = e[t]
        for i, ph in enumerate(phis, 1):
            if t - i >= 0:
                v += ph * x[t - i]
        for j, th in enumerate(thetas, 1):
            if t - j >= 0:
                v += th * e[t - j]
        x[t] = v
    return x[burn:]


def make_volume(seed, weeks=60):
    rng = np.random.default_rng(seed)
    return np.tile([1.3, 1.0, 0.9, 0.95, 1.25], weeks) * np.exp(0.1 * rng.standard_normal(5 * weeks))


def simulate_garch(omega, alpha, beta, n, seed):
    z = np.random.default_rng(seed).standard_normal(n)
    rr = np.empty(n); s2 = np.empty(n); s2[0] = omega / (1 - alpha - beta)
    for t in range(n):
        if t > 0:
            s2[t] = omega + alpha * rr[t - 1] ** 2 + beta * s2[t - 1]
        rr[t] = np.sqrt(s2[t]) * z[t]
    return rr, s2


def lb(x, m, df=0):
    o = acorr_ljungbox(x, lags=[m], model_df=df)
    return float(o['lb_stat'].iloc[0]), float(o['lb_pvalue'].iloc[0])


def ols_slope(x, k):
    return np.polyfit(x[:-k], x[k:], 1)[0]


band = lambda n: 1.96 / math.sqrt(n)

# ---------------- l5 ----------------
A = make_ar1(0.6, 500, 5)
ra = acf(A, nlags=20)
for k in range(1, 6):
    lv.expect('l5', 'screens[0].hints[2].text', r(ra[k], 2))
lv.expect('l5', 'screens[0].widget.options[1].why', r(ra[5], 2))
claim(abs(ra[6]) < 0.06, 'the hook correlation is about 0.04 at k = 6', f'{ra[6]:.4f}')
for k in (1, 2, 3):
    lv.expect('l5', f'screens[1].widget.rows[{k - 1}][1].answer', r(np.polyfit(A[5 - k:-k], A[5:], 1)[0], 3))
xs = np.array([2, 3, 5, 6, 4, 3, 1, 0.])
d = xs - xs.mean()
lv.expect('l5', 'screens[2].widget.rows[1][1].answer', float((d * d).sum()))
lv.expect('l5', 'screens[2].widget.rows[2][1].answer', float((d[1:] * d[:-1]).sum()))
lv.expect('l5', 'screens[2].widget.rows[3][1].answer', r((d[1:] * d[:-1]).sum() / (d * d).sum(), 4))
claim(all(0.09 <= round(ra[k], 2) <= 0.10 for k in (15, 16, 17)), 'lags 15 to 17 reach about 0.09 to 0.10', str(np.round(ra[15:18], 4)))
lv.expect('l5', 'screens[4].question', r(0.6 ** 15, 4))
lv.expect('l5', 'screens[5].widget.answer', r(band(500), 4))
lv.expect('l5', 'screens[5].widget.wrong[2].value', r(1.645 / math.sqrt(500), 4))
lv.expect('l5', 'screens[5].widget.wrong[1].value', r(1.96 / 500, 4))
bart = math.sqrt((1 + 0.36) / (1 - 0.36) / 500)            # Bartlett sd of an AR(1) acf at long lags
lv.expect('l5', 'screens[4].explain.text', r(bart, 3))    # 0.065: FAILS until the explain uses the AR(1) sd (finding 6)
out = [k for k in range(1, 21) if abs(ra[k]) > band(500)]
lv.expect('l5', 'screens[6].explain.text', '[1, 2, 3, 4, 5, 15, 16, 17]') if out == [1, 2, 3, 4, 5, 15, 16, 17] else claim(False, 'lags outside', str(out))
rw24 = acf(make_wn(24), nlags=20)
claim([k for k in range(1, 21) if abs(rw24[k]) > band(500)] == [6, 12], 'make_wn(24) has lags [6, 12] outside')
w4 = acf(make_walk(4, 500), nlags=20)
lv.expect('l5', 'screens[7].prose', r(w4[1], 3)); lv.expect('l5', 'screens[7].prose', r(w4[10], 3))
lv.expect('l5', 'screens[7].explain.text', r(acf(make_walk(5, 500), nlags=10)[10], 2))
lv.expect('l5', 'screens[7].explain.text', r(acf(make_walk(6, 500), nlags=10)[10], 2))
dw = acf(np.diff(make_walk(4, 500)), nlags=20)
claim(all(abs(dw[k]) < band(499) for k in range(1, 21)), 'the walk changes have no bar outside the band')
v = make_volume(91)
rv = acf(v, nlags=20)
lv.expect('l5', 'screens[8].prose', r(band(300), 3))
claim(all(abs(rv[k] - 0.7) < 0.06 for k in (5, 10, 15, 20)), 'weekly lags about 0.7', str(np.round(rv[[5, 10, 15, 20]], 2)))
claim(rv[2] < -0.3 and rv[3] < -0.3, 'lags 2 and 3 strongly negative', str(np.round(rv[[1, 2, 3, 4]], 2)))
lr = np.diff(np.log(make_price(12)))
rl = acf(lr, nlags=20)
lv.expect('l5', 'screens[10].prose', r(band(1999), 3))
k_max = int(np.argmax(np.abs(rl[1:]))) + 1
lv.expect('l5', 'screens[10].prose', r(rl[k_max], 3)); claim(k_max == 11, 'largest return bar is at lag 11')
lv.expect('l5', 'screens[10].hints[2].text', r(rl[1], 3))
rng = np.random.default_rng(8)
mid = 1000 + np.cumsum(0.3 * rng.standard_normal(1000))
trade = mid + rng.choice([-1, 1], size=1000)
dt = np.diff(trade)
lv.expect('l5', 'screens[11].explain.text', r(-1 / (0.09 + 2), 3))
claim(abs(acf(dt, nlags=1)[1] - (-0.451)) < 0.03, 'bounce: seeded trade changes give about -0.451 (rebuilt from the report; draw order may differ)', f'{acf(dt, nlags=1)[1]:.3f}')
lv.expect('l5', 'quiz[0].widget.answer', r(band(20), 2))
lv.expect('l5', 'quiz[0].widget.wrong[0].value', r(1 / math.sqrt(20), 2))
lv.expect('l5', 'quiz[2].prose', r(band(2500), 3))
lv.expect('l5', 'screens[9].widget.options[0].text', r(band(1000), 3))

# ---------------- l6 ----------------
B = make_ar1(0.3, 500, 7)
rb = acf(B, nlags=12)
lv.expect('l6', 'screens[0].widget.options[1].why', r(rb[1], 2))
lv.expect('l6', 'screens[1].hints[2].text', r(1 - 0.95 ** 20, 3))
lv.expect('l6', 'screens[1].widget.options[3].why', r(0.95 ** 20, 2))
rho = [0.19, 0.17, 0.15, 0.12, 0.10]
s = sum(x * x / (100 - k) for k, x in enumerate(rho, 1))
lv.expect('l6', 'screens[3].widget.rows[0][1].answer', r(s, 6))
lv.expect('l6', 'screens[3].explain.text', r(100 * 102 * s, 2))
lv.expect('l6', 'screens[3].widget.rows[2][1]', r(chi2.ppf(0.95, 5), 2))
lv.expect('l6', 'screens[3].explain.text', r(chi2.sf(100 * 102 * s, 5), 3))
q3 = lb(make_wn(3), 10)
lv.expect('l6', 'screens[4].prose', r(q3[0], 2)); lv.expect('l6', 'screens[4].prose', r(q3[1], 4))
qa = lb(A, 10)
lv.expect('l6', 'screens[4].prose', r(qa[0], 1)); claim(qa[1] < 1e-60, 'AR(0.6) Q(10) p below 1e-60', f'{qa[1]:.1e}')
lv.expect('l6', 'screens[4].prose', r(chi2.ppf(0.95, 10), 2))
s30 = make_ar1(0.3, 30, 7)
q30 = lb(s30, 10)
lv.expect('l6', 'screens[5].explain.text', r(q30[1], 2)); lv.expect('l6', 'quiz[2].prose', r(q30[0], 2))
lv.expect('l6', 'quiz[2].prose', r(acf(s30, nlags=1)[1], 2))
lv.expect('l6', 'quiz[2].widget.options[2].why', r(band(30), 2))
q24 = lb(make_wn(24), 20)
lv.expect('l6', 'screens[6].prose', r(q24[0], 2)); lv.expect('l6', 'screens[6].prose', r(q24[1], 3))
lv.expect('l6', 'screens[6].prose', r(rw24[6], 3)); lv.expect('l6', 'screens[6].prose', r(rw24[12], 3))
lv.expect('l6', 'screens[7].explain.text', r(math.sqrt(0.05 * 0.95 / 200), 3))
g, _ = simulate_garch(2e-6, 0.08, 0.90, 2000, 7)
qg, qg2 = lb(g, 10), lb(g ** 2, 10)
lv.expect('l6', 'screens[8].prose', r(qg[0], 2)); lv.expect('l6', 'screens[8].prose', r(qg[1], 2))
lv.expect('l6', 'screens[8].prose', round(qg2[0])); claim(qg2[1] < 1e-300, 'squared GARCH returns p below 1e-300')
qb = lb(B, 10)
lv.expect('l6', 'screens[11].prose', r(qb[0], 1)); lv.expect('l6', 'screens[11].prose', r(qb[1], 6))
fb = ARIMA(B, order=(1, 0, 0)).fit()
qr = lb(fb.resid, 10, 1)
lv.expect('l6', 'screens[11].prose', r(fb.params[1], 3)); lv.expect('l6', 'screens[11].prose', r(qr[0], 2)); lv.expect('l6', 'screens[11].prose', r(qr[1], 2))
s15 = make_ar1(0.15, 500, 7)
for m, pv in ((1, 3), (10, 3), (20, 3)):
    lv.expect('l6', 'quiz[3].prose', r(lb(s15, m)[1], pv))
q_alt = 100 * 102 * sum((x * (-1) ** k) ** 2 / (100 - k) for k, x in enumerate(rho, 1))
claim_text('l6', 'screens[3].explain.text', 'all on one side', abs(q_alt - 100 * 102 * s) > 0.01, 'Q rejects because the bars are all on one side', f'alternating the signs leaves Q at {q_alt:.2f}')

# ---------------- l7 ----------------
lv.expect('l7', 'screens[0].hints[2].text', r(0.9 ** 21, 3)); lv.expect('l7', 'screens[0].hints[2].text', r(0.9 ** 22, 3))
lv.expect('l7', 'screens[0].feedback.byKey.six', r(0.6 ** 5, 3))
cA, pA = np.polyfit(A[:-1], A[1:], 1)[::-1]
lv.expect('l7', 'screens[3].explain.text', r(cA, 4)); lv.expect('l7', 'screens[3].explain.text', r(pA, 4))
lv.expect('l7', 'screens[3].explain.text', r(np.sum((A[1:] - cA - pA * A[:-1]) ** 2) / (len(A) - 1 - 2), 4))
C = make_ar1(0.6, 500, 5, c=1.0)
fc = ARIMA(C, order=(1, 0, 0)).fit()
lv.expect('l7', 'screens[4].prose', r(fc.params[0], 4)); lv.expect('l7', 'screens[4].prose', r(fc.params[1], 4)); lv.expect('l7', 'screens[4].prose', r(fc.params[2], 4))
oc, op = np.polyfit(C[:-1], C[1:], 1)[::-1]
lv.expect('l7', 'screens[4].prose', r(oc, 4))
lv.expect('l7', 'screens[4].widget.answer', r(fc.params[0] * (1 - fc.params[1]), 2))
lv.expect('l7', 'screens[4].widget.wrong[1].value', r(fc.params[0] / (1 - fc.params[1]), 2))
claim_text('l7', 'screens[4].explain.text', 'differ in the third place', abs(op - fc.params[1]) < 0.005 and abs(oc - fc.params[0] * (1 - fc.params[1])) < 0.005,
           'on the c = 1 series least squares and ARIMA differ only in the third place',
           f'OLS c {oc:.4f}, phi {op:.4f}; ARIMA c {fc.params[0] * (1 - fc.params[1]):.4f}, phi {fc.params[1]:.4f}')
fa = ARIMA(A, order=(1, 0, 0)).fit()
lv.expect('l7', 'screens[5].prose', r(fa.params[1], 4)); lv.expect('l7', 'screens[5].prose', r(fa.bse[1], 3))
lv.expect('l7', 'screens[5].prose', r(math.sqrt(0.64 / 500), 3))
claim(0.0005 < abs(pA - fa.params[1]) < 0.005, 'seed 5: OLS and ARIMA agree to 2 places, differ in the 3rd', f'{pA:.4f} against {fa.params[1]:.4f}')
ph = np.array([np.polyfit(z[:-1], z[1:], 1)[0] for z in (make_ar1(0.6, 100, 1000 + s) for s in range(200))])
lv.expect('l7', 'screens[6].explain.text', r(ph.mean(), 3)); lv.expect('l7', 'screens[6].explain.text', r(ph.std(), 2))
claim(abs(ph.min() - 0.3) < 0.03 and abs(ph.max() - 0.78) < 0.01, 'estimates range from 0.3 to 0.78', f'{ph.min():.3f} to {ph.max():.3f}')
lv.expect('l7', 'screens[6].explain.text', r((1 + 3 * 0.6) / 100, 2))
p12 = make_price(12)
fp = ARIMA(p12, order=(1, 0, 0)).fit()
lv.expect('l7', 'screens[7].prose', r(fp.params[1], 4)); lv.expect('l7', 'screens[7].prose', r(fp.bse[1], 3)); lv.expect('l7', 'screens[7].prose', r(fp.params[0], 2))
lv.expect('l7', 'screens[7].explain.text', r(ARIMA(lr, order=(1, 0, 0)).fit().params[1], 3))
lv.expect('l7', 'screens[10].widget.options[0].text', r(acf(make_ar1(0.05, 600, 2), nlags=1)[1], 3))
lv.expect('l7', 'screens[10].prose', r(band(600), 3))
lv.expect('l7', 'screens[10].hints[2].text', round((1.96 / 0.05) ** 2, -2))
f9 = ARIMA(make_ar1(0.9, 500, 5), order=(1, 0, 0)).fit()
lv.expect('l7', 'screens[11].prose', r(f9.params[0], 3)); lv.expect('l7', 'screens[11].prose', r(f9.params[1], 3))
lv.expect('l7', 'screens[11].widget.answer', r(2 * 0.915 ** 5, 2))
lv.expect('l7', 'screens[11].widget.wrong[1].value', r(2 - 5 * 2 * (1 - 0.915), 2))
w12 = make_walk(12, 60, drift=0.3)
lv.expect('l7', 'quiz[1].prose', r(np.polyfit(w12[:-1], w12[1:], 1)[0], 4))
lv.expect('l7', 'quiz[3].widget.options[0].text', r(math.sqrt(0.75 / 400), 3))
lv.expect('l7', 'quiz[0].widget.wrong[1].value', r(0.3 / (1 + 0.7), 3))     # FAILS: the "plus" slip 0.3/1.7 is 0.176; 0.429 is 0.3/0.7

# ---------------- l8 ----------------
Bb = make_arma([0.5, 0.3], [], 500, 11)


def lag_coefs(x, k):
    n = len(x)
    X = np.column_stack([np.ones(n - k)] + [x[k - j:n - j] for j in range(1, k + 1)])
    return np.linalg.lstsq(X, x[k:], rcond=None)[0][1:]


lv.expect('l8', 'screens[1].widget.rows[0][1].answer', r(lag_coefs(A, 2)[1], 3))
lv.expect('l8', 'screens[1].widget.rows[1][1].answer', r(lag_coefs(Bb, 2)[1], 3))
claim_text('l8', 'screens[1].explain.text', 'both newest coefficients are small', abs(lag_coefs(A, 3)[2]) < 0.05, 'at k = 3 both newest coefficients are small', f'A {lag_coefs(A, 3)[2]:.3f}, B {lag_coefs(Bb, 3)[2]:.3f}; band 0.0877')
pa = pacf(A, nlags=20); pb = pacf(Bb, nlags=20)
lv.expect('l8', 'screens[3].hints[2].text', r(pa[1], 3)); lv.expect('l8', 'screens[3].hints[2].text', r(pa[3], 3))
lv.expect('l8', 'screens[2].hints[2].text', r(ra[1] ** 2, 3)); lv.expect('l8', 'screens[2].hints[2].text', r(ra[2], 3))
for k, pl in ((1, 3), (2, 2), (3, 3), (4, 3), (5, 3)):
    lv.expect('l8', 'screens[4].prose', r(pb[k], pl))
lv.expect('l8', 'screens[4].widget.options[2].why', r(pb[11], 3))
claim(all(abs(pb[k]) < band(500) for k in range(3, 11)), 'B PACF lags 3 to 10 inside the band')
lv.expect('l8', 'screens[5].explain.text', r(pacf(A, nlags=1, method='ols')[1], 4)); lv.expect('l8', 'screens[5].explain.text', r(pa[1], 4))
ab = [ARIMA(Bb, order=(p, 0, 0)).fit() for p in range(5)]
for p in (2, 4):
    lv.expect('l8', 'screens[6].hints[2].text', r(ab[p].aic, 2))
lv.expect('l8', 'screens[6].explain.text', r(ab[3].bic - ab[2].bic, 1))
aa = {p: ARIMA(A, order=(p, 0, 0)).fit() for p in (1, 3)}
for p in (1, 3):
    lv.expect('l8', 'screens[7].prose', r(aa[p].aic, 2)); lv.expect('l8', 'screens[7].prose', r(aa[p].bic, 2))
qa1 = lb(aa[1].resid, 10, 1)
lv.expect('l8', 'screens[7].prose', r(qa1[0], 2)); lv.expect('l8', 'screens[7].prose', r(qa1[1], 2))
lv.expect('l8', 'screens[7].hints[2].text', r(r(aa[1].aic, 2) - r(aa[3].aic, 2), 2)); lv.expect('l8', 'screens[7].hints[2].text', r(aa[3].bic - aa[1].bic, 1))
of = make_arma([0.4, 0.25], [], 600, 1)
po = pacf(of, nlags=20)
lv.expect('l8', 'screens[11].prose', r(ARIMA(of, order=(0, 0, 0)).fit().aic, 1))
for p in range(1, 5):
    lv.expect('l8', 'screens[11].prose', r(ARIMA(of, order=(p, 0, 0)).fit().aic, 1))
lv.expect('l8', 'screens[11].hints[2].text', r(po[1], 2)); lv.expect('l8', 'screens[11].hints[2].text', r(po[2], 3))
q2 = make_arma([0.5, -0.6], [], 500, 11)
aq, pq = acf(q2, nlags=5), pacf(q2, nlags=2)
for k, pl in ((1, 1), (2, 2), (3, 1), (4, 2), (5, 2)):
    lv.expect('l8', 'quiz[2].prose', r(aq[k], pl))
lv.expect('l8', 'quiz[2].explain.text', r(pq[1], 3)); lv.expect('l8', 'quiz[2].explain.text', r(pq[2], 3))
lv.expect('l8', 'quiz[3].widget.options[0].text', r(math.log(500), 1))

# ---------------- review-2 and homework-2 ----------------
lv.expect('review', 'items[0].widget.answer', r(band(250), 3))
lv.expect('review', 'items[0].widget.wrong[0].value', r(1 / math.sqrt(250), 3))
lv.expect('review', 'items[1].explain.text', r(rb[1], 3)); lv.expect('review', 'items[1].explain.text', r(rb[2], 3)); lv.expect('review', 'items[1].explain.text', r(rb[9], 3))
q50 = 50 * 52 * (0.09 / 49 + 0.04 / 48)
lv.expect('review', 'items[2].widget.rows[0][1].answer', r(q50, 2)); lv.expect('review', 'items[2].explain.text', r(chi2.sf(q50, 2), 3))
lv.expect('review', 'items[4].widget.wrong[1].value', r(1 / 0.36, 3))
rv6 = make_arma([0.6, -0.3], [], 500, 7)
p6 = pacf(rv6, nlags=2)
lv.expect('review', 'items[6].explain.text', r(p6[1], 3)); lv.expect('review', 'items[6].explain.text', r(p6[2], 3))
lv.expect('homework', 'items[0].widget.answer', r(1 - 0.95 ** 10, 3)); lv.expect('homework', 'items[0].widget.wrong[2].value', r(0.95 ** 10, 3))
lv.expect('homework', 'items[5].widget.answer', math.ceil((1.96 / 0.05) ** 2))
lv.expect('homework', 'items[5].widget.wrong[1].value', round(1.96 / 0.05 ** 2))
lv.expect('homework', 'items[6].widget.options[0].text', r(math.sqrt((1 - 0.0144) / 250), 3))
lv.expect('homework', 'items[6].explain.text', r(0.12 - 1.96 * math.sqrt(0.9856 / 250), 3))
lv.expect('homework', 'items[6].explain.text', r(0.12 + 1.96 * math.sqrt(0.9856 / 250), 3))
lv.expect('homework', 'items[7].model', r(q24[0], 2)); lv.expect('homework', 'items[7].model', r(1 - 0.95 ** 20, 2))

lv.check_wrongs()
lv.report()
