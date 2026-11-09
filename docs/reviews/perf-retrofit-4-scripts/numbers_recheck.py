"""Second routes for the numbers in the three longform items (arma L1, arma L3, backtest L4).
Exit 0 when every stated figure matches; the backtest L4 impact figures are checked against the
course's own per-trade impact rule and reported (they fail: finding BT4-1, see findings_assert.py)."""
import math, numpy as np
from scipy import stats
from statsmodels.tsa.adfvalues import mackinnonp, mackinnoncrit
from statsmodels.tsa.arima_process import arma2ma

fails = 0
def check(lab, got, want, tol):
    global fails
    ok = abs(got - want) <= tol
    fails += not ok
    print('%-4s %-64s %.4f (stated %s)' % ('ok' if ok else 'FAIL', lab, got, want))

# ---- arma L1: Dickey-Fuller with a constant, 120 prices (119 changes) ----
def tstats(W):
    dx = np.diff(W, axis=1); xl = W[:, :-1]; m = dx.shape[1]
    xm = xl.mean(1, keepdims=True); ym = dx.mean(1, keepdims=True)
    sxx = ((xl - xm) ** 2).sum(1); b = ((xl - xm) * (dx - ym)).sum(1) / sxx
    a = ym[:, 0] - b * xm[:, 0]; res = dx - a[:, None] - b[:, None] * xl
    return b / np.sqrt((res ** 2).sum(1) / (m - 2) / sxx)
def ar1(phi, n, sims, rng):
    e = rng.standard_normal((sims, n)); X = np.empty_like(e)
    X[:, 0] = e[:, 0] / math.sqrt(1 - phi ** 2)          # stationary start
    for t in range(1, n): X[:, t] = phi * X[:, t - 1] + e[:, t]
    return X
rng = np.random.default_rng(404)
T0 = tstats(np.cumsum(rng.standard_normal((60000, 120)), 1))
check('arma1 null mean of t, 120 days', T0.mean(), -1.53, 0.02)
check('arma1 5% point, simulation', np.quantile(T0, 0.05), -2.89, 0.02)
check('arma1 5% point, MacKinnon surface n=119', mackinnoncrit(1, 'c', 119)[1], -2.89, 0.01)
check('arma1 share of walks below -1.645 (%)', 100 * (T0 < -1.645).mean(), 46, 1.0)
check('arma1 p of -2.10, MacKinnon', mackinnonp(-2.10, 'c', 1), 0.24, 0.006)
check('arma1 p of -2.10, simulation', (T0 < -2.10).mean(), 0.24, 0.01)
phi_d, phi_h = 0.5 ** 0.1, 0.5 ** (1 / 70)
check('arma1 phi daily', phi_d, 0.933, 0.0005)
check('arma1 phi hourly', phi_h, 0.990, 0.0005)
cv = np.quantile(T0, 0.05)
check('arma1 power, 120 days (%)', 100 * (tstats(ar1(phi_d, 120, 40000, rng)) < cv).mean(), 23, 1.5)
check('arma1 power, 840 hourly prices (%)', 100 * (tstats(ar1(phi_h, 840, 20000, rng)) < mackinnoncrit(1, 'c', 839)[1]).mean(), 24, 1.5)
check('arma1 power, 270 days (%)', 100 * (tstats(ar1(phi_d, 270, 40000, rng)) < mackinnoncrit(1, 'c', 269)[1]).mean(), 80, 2.5)
check('arma1 half-lives in sample, daily and hourly', 120 / 10 + 840 / 70, 24, 1e-12)

# ---- arma L3: ARMA(1,1) forecast fan, phi 0.8, theta -0.4, sigma 2 ----
phi, th, s2 = 0.8, -0.4, 4.0
psi = arma2ma([1, -phi], [1, th], lags=200)            # statsmodels' MA(inf) weights
V = lambda h: s2 * (psi[:h] ** 2).sum()
closed = lambda h: s2 * (1 + (phi + th) ** 2 * (1 - phi ** (2 * (h - 1))) / (1 - phi ** 2))
for h in (1, 2, 5, 12, 40): check('arma3 Var(e_%d) closed form vs psi weights' % h, closed(h), V(h), 1e-9)
check('arma3 geometric sum h=5', (1 - 0.8 ** 8) / 0.36, 2.3117, 5e-5)
check('arma3 Var(e_5)', closed(5), 5.4795, 5e-5)
check('arma3 half-width h=1', 1.96 * math.sqrt(closed(1)), 3.92, 0.005)
check('arma3 half-width h=5', 1.96 * math.sqrt(closed(5)), 4.59, 0.005)
lim = s2 * (1 + 2 * phi * th + th ** 2) / (1 - phi ** 2)
check('arma3 limit vs psi sum to 200', lim, V(200), 1e-9)
check('arma3 limit', lim, 5.7778, 5e-5)
check('arma3 half-width limit', 1.96 * math.sqrt(lim), 4.71, 0.005)
check('arma3 AR(1) limit half-width', 1.96 * 2 / math.sqrt(1 - phi ** 2), 6.53, 0.005)
# simulation of the series variance (stationary), 2 million steps
e = np.random.default_rng(7).standard_normal(2_000_001) * 2
y = np.zeros_like(e)
for_t = None
from scipy.signal import lfilter
y = lfilter([1, th], [1, -phi], e)[10_000:]
check('arma3 series variance, simulation', y.var(), lim, 0.03)

# ---- backtest L4 ----
check('bt4 cost drag research (Sharpe)', 252 * 0.40 * 0.0005 / 0.10, 0.504, 1e-9)
check('bt4 net research', 1.12 - 252 * 0.40 * 0.0005 / 0.10, 0.62, 0.005)
check('bt4 net held out', 0.85 - 252 * 0.44 * 0.0005 / 0.11, 0.35, 0.005)
check('bt4 research years', 1003 / 252, 3.98, 0.005)
check('bt4 SE research', 1 / math.sqrt(1003 / 252), 0.50, 0.005)
# expected best of 30 standard normals, by quadrature and by simulation
emax = 30 * stats.norm.expect(lambda x: x * stats.norm.cdf(x) ** 29)
check('bt4 E[max of 30 N(0,1)] quadrature', emax, 2.043, 0.0005)
check('bt4 E[max of 30 N(0,1)] simulation', np.random.default_rng(1).standard_normal((200000, 30)).max(1).mean(), 2.043, 0.005)
check('bt4 expected best under no edge', 2.043 * 0.38, 0.78, 0.005)
check('bt4 gross edge a day (bp)', 1.12 * 0.10 / 252 * 1e4, 4.44, 0.005)
check('bt4 gross edge per unit traded (bp)', 1.12 * 0.10 / 252 * 1e4 / 0.40, 11.1, 0.05)
# the model's route: impact on the average daily trade, 0.40 of the book
avg_imp = 0.015 * math.sqrt(0.4 / 90)
check('bt4 model route: impact on £0.4m (bp)', avg_imp * 1e4, 10, 0.05)
check('bt4 model route: net at £1m', 1.12 - 252 * 0.40 * (0.0005 + avg_imp) / 0.10, -0.39, 0.005)
B = 90 * ((11.1 - 5) / 1e4 / 0.015) ** 2
check('bt4 model route: break-even daily trade (£m)', B, 0.15, 0.005)
check('bt4 model route: break-even book (£m)', B / 0.40, 0.37, 0.005)
# the course's rule (l11 capacity_table, homework-2 "a flip is twice the book"): impact on each
# day's own trade. Unit positions trade one book (or two on a flip), never 0.4 of it.
one = 0.015 * math.sqrt(1.0 / 90)
print('info per-trade impact on a £1m trade %.1f bp, on a £2m flip %.1f bp' % (one * 1e4, 0.015 * math.sqrt(2 / 90) * 1e4))
print('info net research at £1m, every trade one book: %.2f (flips make it lower)' % (1.12 - 252 * 0.40 * (0.0005 + one) / 0.10))
print('info break-even book, every trade one book: £%.2fm' % (90 * ((11.1 - 5) / 1e4 / 0.015) ** 2))
print('checks failing:', fails)
raise SystemExit(1 if fails else 0)
