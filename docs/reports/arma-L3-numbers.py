"""Second-reader number checks for arma level 3 (l9 to l12, review-3, homework-3).

Every number is recomputed from the course generators (copied from the lesson preludes) with NumPy and statsmodels
in CPython, or from its closed form, then looked up where it is stated (app/tools/numbers_lib.py). ARIMA values are
compared after rounding to the places shown. Claims that are not single numbers use `claim(...)`.
A failing check means the content is wrong (see docs/reviews/review-arma.md) and stays failing until fixed.
Run: python3 docs/reports/arma-L3-numbers.py
"""
import math, os, sys, warnings
import numpy as np
warnings.filterwarnings('ignore')
from statsmodels.tsa.stattools import acf, pacf, adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('arma', 3)


def claim(ok, label, note=''):
    return lv._rec(bool(ok), 'claim: ' + label, note)


def claim_text(ref, path, phrase, ok, label, note=''):
    """A claim tied to the content: it fails only while `phrase` is still in the text at `path` and the fact is false."""
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', note + ('' if present else ' (phrase gone)'))


def r(v, k):
    return round(float(v), k)


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


def make_pair(seed, n=1000, alpha=5.0, beta=1.5, phi=0.95, sd_u=0.5, x0=40.0, vol=0.015):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    x = x0 * np.exp(np.cumsum(vol * z[:, 0]))
    u = np.empty(n); u[0] = sd_u * z[0, 1]
    for t in range(1, n):
        u[t] = phi * u[t - 1] + sd_u * z[t, 1]
    return x, alpha + beta * x + u


def lb(x, m, df=0):
    o = acorr_ljungbox(x, lags=[m], model_df=df)
    return float(o['lb_stat'].iloc[0]), float(o['lb_pvalue'].iloc[0])


def df_reg(x):
    X = np.column_stack([np.ones(len(x) - 1), x[:-1]])
    y = np.diff(x)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y) - 2)
    return beta[1], math.sqrt(s2 * np.linalg.inv(X.T @ X)[1, 1])


hl = lambda ph: math.log(0.5) / math.log(ph)
band = 1.96 / math.sqrt(500)

# ---------------- l9 ----------------
lv.expect('l9', 'screens[0].widget.rows[0][1].answer', r(3 * 0.6 * 0.6, 2))
M = make_arma([], [0.6], 500, 21)
am, pm = acf(M, nlags=10), pacf(M, nlags=5)
for k in range(1, 6):
    lv.expect('l9', 'screens[1].explain.text', r(am[k], 4))
claim(all(abs(am[k]) < band for k in range(2, 11)), 'MA(1) sample ACF inside the band at lags 2 to 10')
lv.expect('l9', 'screens[1].explain.text', r(0.6 / 1.36, 4))
lv.expect('l9', 'screens[2].explain.text', r(M.var(), 4)); lv.expect('l9', 'screens[2].explain.text', r(M.mean(), 4))
lv.expect('l9', 'screens[2].widget.wrong[2].value', r(1 / (1 - 0.36), 4))
for k, pl in ((1, 4), (2, 3), (3, 4)):
    lv.expect('l9', 'screens[4].explain.text', r(pm[k], pl))
lv.expect('l9', 'screens[4].feedback.byKey.x4', r(pm[4], 4)); lv.expect('l9', 'screens[4].feedback.byKey.x5', r(pm[5], 4))
lv.expect('l9', 'screens[6].widget.options[1].why', r(0.7 / 1.49, 2))
th = (1 - math.sqrt(1 - 4 * 0.4631 ** 2)) / (2 * 0.4631)
lv.expect('l9', 'screens[7].explain.text', r(th, 4))
fm = ARIMA(M, order=(0, 0, 1)).fit()
lv.expect('l9', 'screens[7].explain.text', r(fm.params[0], 4)); lv.expect('l9', 'screens[7].explain.text', r(fm.params[1], 4)); lv.expect('l9', 'screens[7].explain.text', r(fm.params[2], 4))
fa1 = ARIMA(M, order=(1, 0, 0)).fit()
lv.expect('l9', 'screens[8].explain.text', r(0.4631 ** 2, 4))
lv.expect('l9', 'screens[8].explain.text', r(fm.aic, 2)); lv.expect('l9', 'screens[8].explain.text', r(fa1.aic, 2))
q_ar = lb(fa1.resid, 10, 1)
lv.expect('l9', 'screens[8].widget.options[2].why', r(q_ar[0], 2)); claim(q_ar[1] < 1e-5, 'AR(1) residuals fail Ljung-Box, p near 0')
lv.expect('l9', 'screens[8].explain.text', r(lb(fm.resid, 10, 1)[1], 2))
rr = make_wn(3, 1001)
y2 = rr[1:] + rr[:-1]
claim(abs(acf(y2, nlags=1)[1] - 0.4998) < 0.03, 'overlapping 2-day returns from seed 3 give about 0.4998 (draw scheme from the prose)', f'{acf(y2, nlags=1)[1]:.4f}')
lv.expect('l9', 'quiz[0].explain.text', r(acf(np.diff(make_wn(3)), nlags=1)[1], 3))
lv.expect('l9', 'quiz[1].widget.answer', r(-0.4 / 1.16, 4))
lv.expect('l9', 'quiz[3].explain.text', r(-0.25 / 1.5, 4))
# screens[5].explain cites "the two roots from the last screen": the roots first appear on screens[7], and the
# theta / (1/theta) pair on screens[6], both after screens[5].
_, l9 = lv._file('l9')
claim_text('l9', 'screens[5].explain.text', 'the two roots from the last screen', 'root' in l9['screens'][4]['explain']['text'] + l9['screens'][4]['prose'], 'the screen before it shows two roots')

# ---------------- l10 ----------------
S33 = make_arma([0.7], [0.4], 500, 33)
a33, p33 = acf(S33, nlags=10), pacf(S33, nlags=3)
for k, pl in ((1, 4), (2, 3), (3, 3)):
    lv.expect('l10', 'screens[0].explain.text', r(a33[k], pl))
lv.expect('l10', 'screens[0].widget.options[1].why', r(a33[6], 4))
claim(abs(a33[8]) > band, 'ACF still outside the band at lag 8', f'{a33[8]:.4f}')
for k in (1, 2, 3):
    lv.expect('l10', 'screens[0].explain.text', r(p33[k], 4))
ph, t_ = 0.7, 0.4
rho1 = (1 + ph * t_) * (ph + t_) / (1 + 2 * ph * t_ + t_ ** 2)
lv.expect('l10', 'screens[1].explain.text', r(rho1, 3)); lv.expect('l10', 'screens[2].hints[2].text', r(ph * rho1, 3))
fits = {(p, q): ARIMA(S33, order=(p, 0, q)).fit() for p in range(3) for q in range(3)}
for (p, q), fr in fits.items():
    lv.expect('l10', 'screens[3].widget.rows', r(fr.aic, 2))
lv.expect('l10', 'screens[3].hints[2].text', r(-fits[(1, 1)].llf, 3)); lv.expect('l10', 'screens[3].hints[2].text', r(-fits[(2, 2)].llf, 3))
lv.expect('l10', 'screens[6].widget.answer', r(fits[(1, 1)].bic, 2))
claim(min(fits, key=lambda k: fits[k].bic) == (1, 1), 'BIC 1445.31 is the lowest in the grid')
lv.expect('l10', 'screens[6].explain.text', r(fits[(1, 1)].params[1], 4)); lv.expect('l10', 'screens[6].explain.text', r(fits[(1, 1)].params[2], 4))
q11 = lb(fits[(1, 1)].resid, 10, 2)
lv.expect('l10', 'screens[6].explain.text', r(q11[0], 4)); lv.expect('l10', 'screens[6].explain.text', r(q11[1], 4))
lv.expect('l10', 'screens[6].widget.wrong[1].value', r(3 * math.log(500) - 2 * fits[(1, 1)].llf, 2))
lv.expect('l10', 'screens[6].widget.wrong[2].value', r(4 * math.log10(500) - 2 * fits[(1, 1)].llf, 2))
S32 = make_arma([0.7], [0.4], 500, 32)
f32 = {o: ARIMA(S32, order=(o[0], 0, o[1])).fit() for o in [(1, 1), (2, 2)]}
lv.expect('l10', 'screens[7].prose', r(f32[(1, 1)].aic - f32[(2, 2)].aic, 2))
claim(f32[(1, 1)].bic < f32[(2, 2)].bic, 'seed 32: BIC prefers (1, 1)')
tr = {o: ARIMA(S32[:400], order=(o[0], 0, o[1])).fit() for o in [(1, 1), (2, 2)]}
mse_in = {o: float(np.mean(tr[o].resid[1:] ** 2)) for o in tr}   # the first residual (day 0) is left out, as the lesson does
mse_out = {o: float(np.mean((S32[400:] - tr[o].apply(S32).fittedvalues[400:]) ** 2)) for o in tr}
lv.expect('l10', 'screens[8].feedback.byKey.22', r(mse_in[(1, 1)], 4)); lv.expect('l10', 'screens[8].feedback.byKey.22', r(mse_in[(2, 2)], 4))
lv.expect('l10', 'screens[8].feedback.byKey.22', r(mse_out[(1, 1)], 4)); lv.expect('l10', 'screens[8].feedback.byKey.22', r(mse_out[(2, 2)], 4))
claim(tr[(2, 2)].aic < tr[(1, 1)].aic, 'on the 400 training days ARMA(2, 2) wins on AIC')
t55 = ARIMA(S32[:400], order=(5, 0, 5)).fit()
lv.expect('l10', 'quiz[0].prose', r(t55.llf, 2)); lv.expect('l10', 'quiz[0].prose', r(tr[(1, 1)].llf, 2))
lv.expect('l10', 'quiz[0].widget.options[1].why', r(np.mean((S32[400:] - t55.apply(S32).fittedvalues[400:]) ** 2), 3))
cf = make_arma([0.5], [-0.5], 500, 7)
fcf = {o: ARIMA(cf, order=(o[0], 0, o[1])).fit() for o in [(0, 0), (1, 1)]}
lv.expect('l10', 'quiz[1].explain.text', r(fcf[(0, 0)].aic, 2)); lv.expect('l10', 'quiz[1].explain.text', r(fcf[(1, 1)].aic, 2))
claim(abs(fcf[(1, 1)].params[1] + 0.1667) < 0.05 and abs(fcf[(1, 1)].params[2] - 0.2265) < 0.05,
      'common factor fit near -0.1667 and 0.2265 (unstable: CPython and Pyodide may differ)', f'{fcf[(1, 1)].params[1]:.4f}, {fcf[(1, 1)].params[2]:.4f}')
lv.expect('l10', 'quiz[2].widget.answer', r(math.log(500), 3)); lv.expect('l10', 'quiz[2].explain.text', r(math.exp(2), 1))

# ---------------- l11 ----------------
S41 = make_ar1(0.8, 500, 41)
lv.expect('l11', 'screens[0].prose', r(S41[-1], 4))
f41 = ARIMA(S41, order=(1, 0, 0)).fit()
mu, phi, s2 = f41.params
lv.expect('l11', 'screens[2].prose', r(mu, 4)); lv.expect('l11', 'screens[2].prose', r(phi, 4)); lv.expect('l11', 'screens[4].question', r(s2, 4))
fc = f41.get_forecast(30)
ci = fc.conf_int(alpha=0.05)
hw = (ci[:, 1] - ci[:, 0]) / 2
for h in (1, 5, 30):
    lv.expect('l11', 'screens[1].explain.text', r(hw[h - 1], 4))
lv.expect('l11', 'screens[6].prose', r(-ci[29, 0], 4)); lv.expect('l11', 'screens[6].prose', r(ci[29, 1], 4))
lv.expect('l11', 'screens[6].widget.accept', r(1.96 * math.sqrt(s2 / (1 - phi ** 2)), 4))
lv.expect('l11', 'screens[2].widget.answer', r(mu + phi ** 5 * (S41[-1] - mu), 4))
lv.expect('l11', 'screens[2].explain.text', r(phi ** 5, 4))
lv.expect('l11', 'screens[4].widget.answer', r(1.96 * math.sqrt(s2 * (1 + phi ** 2)), 3))
lv.expect('l11', 'screens[4].widget.wrong[0].value', r(1.96 * math.sqrt(2 * s2), 3))
lv.expect('l11', 'screens[4].widget.wrong[1].value', r(1.96 * math.sqrt(s2) * (1 + phi), 3))
lv.expect('l11', 'screens[6].widget.wrong[0].value', r(1.96 * math.sqrt(s2 / (1 - phi)), 3))
lv.expect('l11', 'screens[6].widget.wrong[1].value', r(1.96 * s2 / (1 - phi ** 2), 3))
mt, thh, s2m = fm.params
lv.expect('l11', 'screens[7].prose', r(fm.resid[-1], 4))
lv.expect('l11', 'screens[7].widget.answer', r(1.96 * math.sqrt(s2m * (1 + thh ** 2)), 3))
lv.expect('l11', 'screens[7].widget.wrong[0].value', r(1.96 * math.sqrt(s2m * (1 + 2 * thh ** 2)), 3))
lv.expect('l11', 'screens[7].explain.text', r(mt + thh * fm.resid[-1], 4))
W4 = make_walk(4, 500)
fw = ARIMA(W4, order=(1, 0, 0)).fit()
lv.expect('l11', 'screens[8].prose', r(fw.params[1], 4)); lv.expect('l11', 'screens[8].prose', r(fw.params[0], 2))
cw = fw.get_forecast(500).conf_int(alpha=0.05)
lv.expect('l11', 'screens[8].widget.options[1].text', r((cw[249, 1] - cw[249, 0]) / 2, 1))
lv.expect('l11', 'screens[8].explain.text', r(1.96 * math.sqrt(fw.params[2] / (1 - fw.params[1] ** 2)), 1))
rw = ARIMA(W4, order=(0, 1, 0)).fit()
cr = rw.get_forecast(500).conf_int(alpha=0.05)
lv.expect('l11', 'screens[8].widget.options[0].text', r((cr[249, 1] - cr[249, 0]) / 2, 1))
lv.expect('l11', 'screens[8].explain.text', r((cr[499, 1] - cr[499, 0]) / 2, 1))
lv.expect('l11', 'screens[10].explain.text', r((cr[99, 1] - cr[99, 0]) / 2, 1))
claim(S33[-1] < fits[(1, 1)].params[0] - 1, 'the seed-33 ARMA(1, 1) ends far below its mean (screens[10].explain)', f'last {S33[-1]:.3f}, mean {fits[(1, 1)].params[0]:.3f}')
F = 25 + 3 * make_ar1(0.9, 750, 12)
ff = ARIMA(F, order=(1, 0, 0)).fit()
mF, pF, sF = ff.params
lv.expect('l11', 'screens[11].prose', r(mF, 2)); lv.expect('l11', 'screens[11].prose', r(pF, 4)); lv.expect('l11', 'screens[11].prose', r(sF, 4)); lv.expect('l11', 'screens[11].prose', r(F[-1], 2))
fF = ff.get_forecast(10)
cF = fF.conf_int(alpha=0.05)
lv.expect('l11', 'screens[11].explain.text', r(fF.predicted_mean[9], 2)); lv.expect('l11', 'screens[11].explain.text', r(cF[9, 0], 2)); lv.expect('l11', 'screens[11].explain.text', r(cF[9, 1], 2))
lv.expect('l11', 'screens[11].widget.answer', r(1.96 * math.sqrt(sF * (1 - pF ** 20) / (1 - pF ** 2)), 2))
lv.expect('l11', 'screens[11].explain.text', r(1.96 * math.sqrt(sF / (1 - pF ** 2)), 2))
lv.expect('l11', 'screens[11].widget.wrong[0].value', r(1.96 * math.sqrt(10 * sF), 1))
lv.expect('l11', 'screens[11].feedback.byKey.unc', round(100 * (1 - pF ** 20)))   # 93% of the limiting variance after 10 days (finding 16)
lv.expect('l11', 'screens[11].feedback.byKey.unc', 11.70)

# ---------------- l12 ----------------
e7 = np.random.default_rng(7).standard_normal(200)


def spread(ph):
    x = np.empty(200); x[0] = 3.0
    for t in range(1, 200):
        x[t] = ph * x[t - 1] + 0.3 * e7[t]
    return x


cross = [int(np.argmax(spread(ph) <= 1.5)) for ph in (0.9, 0.98)]
claim(cross == [5, 16], 'noisy paths first reach 1.5 on days 5 and 16 (seed 7, shocks e[1:] assumed)', str(cross))
lv.expect('l12', 'screens[0].explain.text', r(hl(0.9), 1)); lv.expect('l12', 'screens[0].explain.text', round(hl(0.98)))
lv.expect('l12', 'screens[2].widget.answer', r(hl(0.8), 3))
for ph_, pl in ((0.5, 3), (0.99, 3)):
    lv.expect('l12', 'screens[2].explain.text', r(hl(ph_), pl))
lv.expect('l12', 'screens[3].hints[2].text', r(hl(0.98), 2))
lv.expect('l12', 'screens[4].explain.text', r(hl(0.6), 3))
px, py = make_pair(3, 1000)
X = np.column_stack([np.ones(1000), px])
u = py - X @ np.linalg.lstsq(X, py, rcond=None)[0]
b, se = df_reg(u)
lv.expect('l12', 'screens[7].prose', r(b, 4)); lv.expect('l12', 'screens[7].prose', r(se, 4))
lv.expect('l12', 'screens[5].widget.accept', r(1 + b, 4)); lv.expect('l12', 'screens[5].explain.text', r(hl(1 + b), 3))
lv.expect('l12', 'screens[5].widget.wrong[1].value', r(math.log(2) / -b, 2)); lv.expect('l12', 'screens[5].widget.wrong[0].value', r(hl(-b), 2))
lv.expect('l12', 'screens[7].prose', r(1 + b - 1.96 * se, 4)); lv.expect('l12', 'screens[7].prose', r(1 + b + 1.96 * se, 4))
lv.expect('l12', 'screens[7].explain.text', r(hl(1 + b - 1.96 * se), 2)); lv.expect('l12', 'screens[7].explain.text', r(hl(1 + b + 1.96 * se), 2))
lv.expect('l12', 'screens[7].explain.text', r(math.sqrt((1 - 0.95 ** 2) / 1000), 4))
w26 = make_walk(26, 1000)
bw, _ = df_reg(w26)
lv.expect('l12', 'screens[8].prose', r(bw, 4)); lv.expect('l12', 'screens[8].prose', r(1 + bw, 4)); lv.expect('l12', 'screens[8].prose', round(hl(1 + bw)))
lv.expect('l12', 'screens[8].explain.text', r(adfuller(w26)[1], 2))
b100, _ = df_reg(make_ar1(0.95, 100, 1))
lv.expect('l12', 'screens[10].explain.text', r(hl(1 + b100), 1))
lv.expect('l12', 'quiz[1].widget.options[1].text', round(-math.log(2) / math.log(1.002)))
lv.expect('l12', 'quiz[2].widget.answer', r(math.log(0.1) / math.log(0.9), 2)); lv.expect('l12', 'quiz[2].explain.text', r(math.log(0.1) / math.log(0.5), 2))

# ---------------- review-3 and homework-3 ----------------
lv.expect('review', 'items[0].explain.text', r((1 - math.sqrt(1 - 4 * 0.38 ** 2)) / (2 * -0.38), 2))
lv.expect('review', 'items[1].widget.answer', (1 - math.sqrt(1 - 0.64)) / 0.8)
lv.expect('review', 'items[4].widget.answer', r(1.96 * math.sqrt(1.25), 3)); lv.expect('review', 'items[4].explain.text', r(1.96 / math.sqrt(0.75), 3))
lv.expect('review', 'items[5].widget.answer', r(2 + 0.6 ** 3 * 3, 3))
lv.expect('review', 'items[6].widget.answer', r(hl(0.7), 3)); lv.expect('review', 'items[6].widget.wrong[1].value', r(1 / hl(0.7), 3))
lv.expect('review', 'items[7].widget.answer', r(hl(1 - 0.020 + 1.96 * 0.006), 1)); lv.expect('review', 'items[7].explain.text', r(hl(1 - 0.020 - 1.96 * 0.006), 1))
lv.expect('review', 'items[7].prose', r(hl(0.98), 1))
lv.expect('homework', 'items[1].widget.answer', r(0.5 * 1.25 / 1.75, 4)); lv.expect('homework', 'items[1].widget.wrong[1].value', r((1.25 / 1.75) ** 2, 4))
lv.expect('homework', 'items[2].widget.answer', r(2 * math.log(1000) - 12, 2))
lv.expect('homework', 'items[2].explain.text', r(4 * math.log(1000) + 2000, 2)); lv.expect('homework', 'items[2].explain.text', r(6 * math.log(1000) + 1988, 2))
lv.expect('homework', 'items[3].widget.answer', 3 / 5)
lv.expect('homework', 'items[2].explain.text', r((6 * math.log(1000) + 1988) - (4 * math.log(1000) + 2000), 2))   # 1.82, BIC prefers ARMA(1, 1) (finding 19)
lv.expect('homework', 'items[3].explain.text', 3 / 5)
lv.expect('homework', 'items[7].model', r(hl(0.97), 1)); lv.expect('homework', 'items[7].model', r(0.97 ** 10, 3))
se97 = math.sqrt((1 - 0.97 ** 2) / 250)
lv.expect('homework', 'items[7].model', r(se97, 4)); lv.expect('homework', 'items[7].model', r(hl(0.94), 1))
lv.expect('homework', 'items[7].model', r(-0.03 / se97, 2)); lv.expect('homework', 'items[7].model', r((1 + 3 * 0.97) / 250, 3))
lv.expect('homework', 'items[7].model', round(hl(0.985)))
t32 = {o: ARIMA(S32[:400], order=(o[0], 0, o[1])).fit() for o in [(1, 1), (2, 2)]}
lv.expect('homework', 'items[6].explain.text', r(t32[(1, 1)].bic - t32[(2, 2)].bic, 2))
lv.expect('homework', 'items[6].explain.text', r(lb(t32[(2, 2)].resid, 10, 4)[1], 3)); lv.expect('homework', 'items[6].explain.text', r(lb(t32[(1, 1)].resid, 10, 2)[1], 3))

lv.check_wrongs()
lv.report()
