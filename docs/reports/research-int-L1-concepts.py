"""Concept checks for research-int level 1 (l1 to l5, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/research-int-L1-concepts.py
Each assert names the ledger row it covers (docs/reports/audit-research-int-1-3-ledger.md).
A check that fails because the content is wrong stays failing and is a finding in
docs/reviews/audit-research-int-1-3.md.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(20261106)
fails = []


def check(cond, msg):
    if cond:
        print("ok   ", msg)
    else:
        print("FAIL ", msg)
        fails.append(msg)


# ---------------------------------------------------------------- l1: two regressions
# Five points with S_xx = 10, S_yy = 40, S_xy = 16 and means (3, 6).
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([3.0, 4.0, 5.0, 10.0, 8.0])
y = (y - y.mean()) * np.sqrt(40 / ((y - y.mean()) ** 2).sum()) + 6
# rotate y residuals so that S_xy = 16 while keeping S_yy = 40
sxx = ((x - 3) ** 2).sum()
e = (y - 6) - ((x - 3) * ((x - 3) * (y - 6)).sum() / sxx)
e = e / np.sqrt((e ** 2).sum())
y = 6 + 1.6 * (x - 3) + e * np.sqrt(40 - 1.6 ** 2 * 10)
Sxx, Syy, Sxy = ((x - 3) ** 2).sum(), ((y - 6) ** 2).sum(), ((x - 3) * (y - 6)).sum()
byx, bxy = Sxy / Sxx, Sxy / Syy
r = Sxy / np.sqrt(Sxx * Syy)
check(np.allclose([Sxx, Syy, Sxy], [10, 40, 16]), "l1 s0 data sums 10, 40, 16")
check(np.isclose(byx, 1.6) and np.isclose(bxy, 0.4), "l1 s0 and s3: slopes S_xy/S_xx = 1.6, S_xy/S_yy = 0.4")
check(np.isclose(((y - (6 + 1.6 * (x - 3))) ** 2).sum(), 14.4), "l1 s0 explain: minimum RSS 14.4")
check(np.isclose(byx * bxy, r ** 2) and np.isclose(r ** 2, 0.64), "l1 s2 and s5: product of slopes = r^2 = 0.64")
check(np.isclose(1 / bxy, 2.5) and np.isclose(np.sqrt(1.6 * 2.5), 2.0), "l1 s1 and s2: x-on-y line drawn on (x, y) axes has slope 2.5; geometric mean of 1.6 and 2.5 is s_y/s_x = 2")
check(np.isclose(np.corrcoef(x, 6 + 1.6 * (x - 3) + e * np.sqrt(40 - 1.6 ** 2 * 10))[0, 1] ** 2, 0.64), "l1 s5: R^2 of y on x equals r^2 (simple regression)")
# Both R^2 equal r^2
rss_x = ((x - (3 + 0.4 * (y - 6))) ** 2).sum()
check(np.isclose(1 - rss_x / Sxx, 0.64), "l1 s5: R^2 of x on y also equals r^2")

# duplicated rows: slope and R^2 unchanged, t rises by sqrt((2n-2)/(n-2))
import statsmodels.api as sm
n = 10
xx = rng.normal(size=n)
yy = 0.8 * xx + rng.normal(size=n)
m1 = sm.OLS(yy, sm.add_constant(xx)).fit()
m2 = sm.OLS(np.r_[yy, yy], sm.add_constant(np.r_[xx, xx])).fit()
check(np.isclose(m1.params[1], m2.params[1]) and np.isclose(m1.rsquared, m2.rsquared), "l1 s8 and r1 item1 part1: copying rows leaves slope and R^2 unchanged")
check(np.isclose(m2.tvalues[1] / m1.tvalues[1], np.sqrt(18 / 8)), "l1 s8: t rises by sqrt((2n-2)/(n-2)) = 1.5 at n = 10")
check(np.isclose(m2.bse[1] / m1.bse[1], 2 / 3), "l1 s8 hint: standard error falls to 2/3")
check(np.isclose(2 * stats.t.sf(4.962, 8), 0.0011, atol=0.0001) and np.isclose(2 * stats.t.sf(7.443, 18), 6.7e-7, rtol=0.05), "l1 s8 explain: p from 0.0011 (t=4.962, df 8) to 6.7e-7 (t=7.443, df 18)")
check(np.isclose(np.sqrt(10 / 4) * 2.1, 3.32, atol=0.005), "l1 quiz1: n = 6, factor sqrt(10/4), t 2.1 -> 3.32")
n = 20
xx = rng.normal(size=n); yy = 0.5 * xx + rng.normal(size=n)
m1 = sm.OLS(yy, sm.add_constant(xx)).fit(); m2 = sm.OLS(np.r_[yy, yy], sm.add_constant(np.r_[xx, xx])).fit()
check(np.isclose(m2.bse[1] / m1.bse[1], np.sqrt(18 / 38)), "r1 item1 part2: SE ratio sqrt(18/38) = 0.6882 at n = 20")

# attenuation: true slope 2, var(x) = 4, noise var 1 -> plim slope 1.6
N = 400_000
xt = rng.normal(0, 2, N)
yt = 2 * xt + rng.normal(0, 1, N)
xo = xt + rng.normal(0, 1, N)
slope_noisy = np.cov(xo, yt)[0, 1] / np.var(xo, ddof=1)
check(abs(slope_noisy - 1.6) < 0.01, "l1 s9: noise in x (var 1) on var(x) = 4 attenuates slope 2 to 1.6 (probability limit)")
yo = yt + rng.normal(0, 3, N)
check(abs(np.cov(xt, yo)[0, 1] / np.var(xt, ddof=1) - 2) < 0.01, "l1 s9 byKey none: noise in y leaves the slope unbiased")
xt = rng.normal(0, 3, N); yt = xt + rng.normal(0, 1, N); xo = xt + rng.normal(0, np.sqrt(3), N)
check(abs(np.cov(xo, yt)[0, 1] / np.var(xo, ddof=1) - 0.75) < 0.01, "l1 quiz2: var 9, noise 3 -> 0.75")
check(np.isclose(1.5 / (6 / 8), 2.0), "h1 item6: fitted 1.5 with factor 6/8 -> true slope 2")
check(np.isclose(0.5 * 4 / 2, 1.0) and np.isclose(0.5 * 30 / 15, 1.0) and np.isclose(0.5 * 15 / 30, 0.25), "l1 quiz0 and s7: b = r s_x/s_y with the right spreads")
check(np.isclose(0.6 * 2 / 3, 0.4) and np.isclose(np.sqrt(0.5 * 1.2), 0.7746, atol=5e-4), "r1 item0 and item1 part0")

# ---------------------------------------------------------------- l2: correlation limits
def corr_matrix(a, b, c):
    return np.array([[1, a, c], [a, 1, b], [c, b, 1]])

def det3(a, b, c):
    return 1 + 2 * a * b * c - a * a - b * b - c * c

# det formula vs numpy
for _ in range(200):
    a, b, c = rng.uniform(-1, 1, 3)
    assert np.isclose(np.linalg.det(corr_matrix(a, b, c)), det3(a, b, c))
check(True, "l2 s5 and s6: det R = 1 + 2abc - a^2 - b^2 - c^2 (checked against numpy on 200 random triples)")
# range of c equals PSD condition
ok = True
for _ in range(400):
    a, b = rng.uniform(-0.99, 0.99, 2)
    c = rng.uniform(-1, 1)
    lo, hi = a * b - np.sqrt((1 - a * a) * (1 - b * b)), a * b + np.sqrt((1 - a * a) * (1 - b * b))
    psd = np.linalg.eigvalsh(corr_matrix(a, b, c)).min() >= -1e-12
    ok &= (psd == (lo - 1e-12 <= c <= hi + 1e-12))
check(ok, "l2 s5: c in ab +- sqrt((1-a^2)(1-b^2)) iff R is positive semidefinite (400 random triples)")
check(np.isclose(0.64 - 0.36, 0.28) and np.isclose(0.49 - 0.51, -0.02) and np.isclose(-0.81 + 0.19, -0.62) and np.isclose(0.81 - 0.19, 0.62), "l2 s0 to s3: floors 0.28, -0.02, ceiling -0.62, floor 0.62")
check(np.isclose(0.72 - np.sqrt(0.19 * 0.36), 0.4585, atol=5e-4), "l2 quiz0: floor 0.4585")
check(np.isclose(0.48 - np.sqrt(0.64 * 0.36), 0.0), "r1 item2: 0.6 and 0.8 give floor 0")
check(np.isclose(0.24 - np.sqrt(0.36 * 0.91), -0.3324, atol=5e-4) and np.isclose(0.36 - 0.64, -0.28), "h1 item0: floors -0.3324 and -0.28")
check(np.isclose(np.linalg.eigvalsh(corr_matrix(0.9, 0.9, -0.5)).min(), -0.5471, atol=5e-4) and np.isclose(det3(0.9, 0.9, -0.5), -1.68), "l2 s7: vendor matrix det -1.68, smallest eigenvalue -0.5471")
dets = [det3(0.5, 0.5, -0.6), det3(0.5, 0.5, -0.4), det3(0, 0, 0.9), det3(0.8, -0.8, -0.5)]
check(np.allclose(dets, [-0.16, 0.14, 0.19, 0.11]), "l2 quiz1: determinants -0.16, 0.14, 0.19, 0.11")
dets = [det3(0.9, 0.9, 0.7), det3(0.9, 0.9, 0.5), det3(0.9, -0.9, -0.7), det3(0.6, 0.6, 0.1), det3(0.6, 0.6, -0.3)]
check(np.allclose(dets, [0.024, -0.06, 0.024, 0.342, -0.026]), "r1 item3: determinants 0.024, -0.06, 0.024, 0.342, -0.026")
# equicorrelation eigenvalues
for nn, rho in [(3, -0.5), (5, -0.25), (6, -0.2), (4, -1 / 3)]:
    R = (1 - rho) * np.eye(nn) + rho * np.ones((nn, nn))
    ev = np.linalg.eigvalsh(R)
    assert np.isclose(ev.min(), 0, atol=1e-12) and np.isclose(ev.max(), 1 - rho)
check(True, "l2 s4, s8, quiz2, h1 item0 part2: equicorrelation floor -1/(n-1), eigenvalues 1+(n-1)rho and 1-rho")
check(np.isclose(np.sqrt(0 * 0.91), 0), "l2 quiz3: a = 1 forces c = b = 0.3")
# covariance range h1 item5
Sig = lambda c: np.array([[4, 3, c], [3, 9, 6], [c, 6, 16]])
check(np.linalg.eigvalsh(Sig(-4)).min() > -1e-9 and np.linalg.eigvalsh(Sig(8)).min() > -1e-9 and np.linalg.eigvalsh(Sig(-4.05)).min() < 0 and np.linalg.eigvalsh(Sig(8.05)).min() < 0, "h1 item5: covariance c in [-4, 8]")

# ---------------------------------------------------------------- l3: estimators
n, theta = 9, 10.0
M = rng.uniform(0, theta, (200_000, n)).max(axis=1)
check(abs(M.mean() - 9) < 0.01, "l3 s0: E[max of 9 U(0,10)] = 9")
check(abs(M.var() - 0.8182) < 0.01, "l3 s2: Var(M) = n theta^2/((n+1)^2(n+2)) = 0.8182")
check(abs((10 / 9 * M).var() - 1.0101) < 0.012 and abs((10 / 9 * M).mean() - 10) < 0.01, "l3 s1 and s2: (n+1)/n M unbiased with variance 1.0101")
check(abs(((M - 10) ** 2).mean() - 1.8182) < 0.02, "l3 s2: MSE of M = 1.8182")
two_mean = 2 * rng.uniform(0, theta, (200_000, n)).mean(axis=1)
check(abs(two_mean.var() - 3.7037) < 0.03, "l3 s2: twice the mean has variance 100/27 = 3.7037")
c_opt = (n + 2) / (n + 1)
check(((c_opt * M - 10) ** 2).mean() < ((10 / 9 * M - 10) ** 2).mean(), "l3 s9 explain: scaling by (n+2)/(n+1) lowers the MSE below the unbiased (n+1)/n")
# normal divisor
def mse_div(n, d):
    k = n - 1
    return (2 * k + (k - d) ** 2) / d ** 2
check(np.allclose([mse_div(10, 9), mse_div(10, 10), mse_div(10, 11)], [2 / 9, 0.19, 2 / 11]), "l3 s3: MSE 0.2222, 0.19, 0.1818 for divisors 9, 10, 11 (sigma^2 = 1, chi-square(n-1))")
S = ((rng.normal(size=(200_000, 10)) - rng.normal(size=(200_000, 10)).mean(axis=1, keepdims=True) * 0) ** 2)
samp = rng.normal(size=(200_000, 10)); ss = ((samp - samp.mean(axis=1, keepdims=True)) ** 2).sum(axis=1)
check(all(abs(((ss / d - 1) ** 2).mean() - mse_div(10, d)) < 0.01 for d in (9, 10, 11)), "l3 s3: Monte Carlo agrees with the chi-square MSE formula")
for nn in (10, 15, 20, 30):
    assert min(range(1, 3 * nn), key=lambda d: mse_div(nn, d)) == nn + 1
check(True, "l3 quiz1, r1 item5, h1 item2: best integer divisor is n + 1")
check(np.allclose([mse_div(15, 14), mse_div(15, 15), mse_div(15, 16)], [0.1429, 0.1289, 0.125], atol=5e-5), "r1 item5: 0.1429, 0.1289, 0.125")
# shrunk coin
p = np.linspace(0.01, 0.99, 9801)
mse_plain = p * (1 - p) / 10
mse_shr = ((1 - 2 * p) / 12) ** 2 + 10 * p * (1 - p) / 144
cross = p[np.where(np.diff(np.sign(mse_plain - mse_shr)))[0]]
check(np.allclose(cross, [0.138, 0.862], atol=0.002), "l3 s4: shrink (k+1)/(n+2) helps for p in (0.138, 0.862)")
check(np.isclose(mse_shr[np.argmin(abs(p - 0.5))], 0.01736, atol=1e-4) and np.isclose(mse_plain[np.argmin(abs(p - 0.5))], 0.025), "l3 s4 explain: MSEs 0.0174 and 0.025 at p = 0.5")
k = rng.binomial(10, 0.9, 400_000)
check(abs((((k + 1) / 12 - 0.9) ** 2).mean() - 0.0107) < 0.0005, "h1 item7: MSE of shrunk estimate at p = 0.9 is 0.0107 (bias -0.0667, var 0.00625)")
# exponential rate
xb = rng.exponential(0.5, (400_000, 5)).mean(axis=1)
check(abs((1 / xb).mean() - 2.5) < 0.02, "l3 s5: E[1/xbar] = n lambda/(n-1) = 2.5")
check(abs((4 / (5 * xb)).mean() - 2.0) < 0.02, "l3 s5 explain: (n-1)/(n xbar) is unbiased")
check(np.isclose(0.3 ** 2 + 0.16, 0.25) and np.isclose(0.04 + 0.05, 0.09), "l3 s6 and quiz2: MSE = bias^2 + variance")
check(np.isclose(6.3 * 10 / 9, 7.0) and np.isclose(2 * np.mean([3.1, 5.85, 4.4, 6.3, 2.75, 5.2, 4.95, 3.8, 6.05]), 9.42, atol=0.005), "l3 s8: 6.30 x 10/9 = 7.00, twice the mean 9.42")

# ---------------------------------------------------------------- l4: tests in words
check(np.isclose(2 * stats.norm.sf(2), 0.0455, atol=5e-5), "l4 s1: two-sided normal p at z = 2 is 0.0455")
p_one = stats.binom.sf(39, 64, 0.5)
check(np.isclose(p_one, 0.0300, atol=5e-5) and np.isclose(p_one + stats.binom.cdf(24, 64, 0.5), 0.0599, atol=5e-5), "l4 s2: exact binomial one tail 0.0300, two-sided 0.0599")
check(np.isclose(2 * stats.norm.sf((39.5 - 32) / 4), 0.0608, atol=5e-4), "l4 s2 explain: continuity correction gives 0.0608, close to the exact 0.0599")
power = stats.norm.cdf((0.5 - 1.96 * 0.2) / 0.2) + stats.norm.cdf((-0.5 - 1.96 * 0.2) / 0.2)
check(np.isclose(power, 0.7054, atol=5e-4), "l4 s3: power 0.7054 at n = 25, mean 0.5, sigma 1")
n80 = ((1.96 + stats.norm.ppf(0.8)) / 0.5) ** 2
se32 = 1 / np.sqrt(32)
check(np.isclose(n80, 31.4, atol=0.05) and np.isclose(stats.norm.cdf((0.5 - 1.96 * se32) / se32), 0.8074, atol=5e-4), "l4 s3 explain: n = 31.4 for 80% power, n = 32 gives 0.8074")
check(np.isclose(stats.norm.cdf(2 - 1.96) + stats.norm.cdf(-2 - 1.96), 0.516, atol=5e-4), "l4 quiz1: power 0.516")
# Sharpe ratio as a t statistic: t = SR sqrt(T) with T annual observations
T = 4
rets = rng.normal(0.1, 0.1, (200_000, T))
sr_hat = rets.mean(axis=1) / rets.std(axis=1, ddof=1)
t_hat = rets.mean(axis=1) / (rets.std(axis=1, ddof=1) / np.sqrt(T))
check(np.allclose(t_hat, sr_hat * np.sqrt(T)), "l4 s5: t statistic of the mean annual return = SR x sqrt(years)")
p_t3 = 2 * stats.t.sf(2, T - 1)
p_norm = 2 * stats.norm.sf(2)
print(f"      l4 s5: for t = 2 from 4 yearly returns the reference is t_3: p = {p_t3:.3f}; the normal gives {p_norm:.4f}")
# Under the null (zero mean) with 4 yearly returns, how often does |SR sqrt(T)| exceed 2?
null = rng.normal(0, 0.1, (400_000, T))
t_null = null.mean(axis=1) / (null.std(axis=1, ddof=1) / np.sqrt(T))
rate = (abs(t_null) >= 2).mean()
check(abs(rate - p_t3) < 0.003, "l4 s5: Monte Carlo under the null, 4 yearly returns, P(|t| >= 2) matches t_3 (about 0.139)")
# After the fix pass the content says: p approx 0.0455 with the Sharpe estimated from daily returns, t_3 gives about 0.14 from four yearly figures.
hits = 0
for _ in range(4):
    daily = rng.normal(0, 0.01, (10_000, 4 * 252))
    t_daily = daily.mean(axis=1) / daily.std(axis=1, ddof=1) * np.sqrt(252) * np.sqrt(4)
    hits += (abs(t_daily) >= 2).sum()
rate_daily = hits / 40_000
check(abs(rate_daily - 0.0455) < 0.004 and abs(p_t3 - 0.14) < 0.005, f"l4 s5 explain: Sharpe from 4 years of daily returns, P(|t| >= 2) under the null = {rate_daily:.4f} (content 0.0455); from four yearly figures t_3 gives {p_t3:.3f} (content 0.14) (corrected claim, fix pass)")
check(np.isclose(1 - 0.95 ** 10, 0.4013, atol=5e-5) and np.isclose(1 - 0.95 ** 15, 0.5367, atol=5e-5) and 1 - 0.995 ** 10 < 0.05, "l4 s6 and r1 item6: 1 - 0.95^m; Bonferroni keeps the family below 5%")
# MC: ten independent tests at 5% under the null
z = rng.normal(size=(200_000, 10))
check(abs((abs(z) > 1.96).any(axis=1).mean() - 0.4013) < 0.005, "l4 s6: Monte Carlo family-wise rate 0.401 for ten independent 5% tests")
# Holm / BH on the two p-value sets
def bonf(ps, a=0.05): return sum(p <= a / len(ps) for p in ps)
def holm(ps, a=0.05):
    ps = sorted(ps); m = len(ps); k = 0
    for i, p in enumerate(ps):
        if p <= a / (m - i): k += 1
        else: break
    return k
def bh(ps, a=0.05):
    ps = sorted(ps); m = len(ps); ks = [i + 1 for i, p in enumerate(ps) if p <= a * (i + 1) / m]
    return max(ks) if ks else 0
ps = [0.001, 0.008, 0.012, 0.03, 0.2]
check((bonf(ps), holm(ps), bh(ps)) == (2, 3, 4), "l4 s7: Bonferroni 2, Holm 3, BH 4")
ps = [0.001, 0.011, 0.014, 0.038, 0.3]
check((bonf(ps), holm(ps), bh(ps)) == (1, 3, 4), "r1 item7: Bonferroni 1, Holm 3, BH 4")
# Holm and BH are at least as powerful as Bonferroni, and BH is at least Holm, on random p-value sets
ok = True
for _ in range(2000):
    ps = list(rng.uniform(0, 0.1, 6))
    ok &= bonf(ps) <= holm(ps) <= bh(ps)
check(ok, "l4 s7 explain: Holm rejects at least as many as Bonferroni, BH at least as many as Holm (2000 random sets)")
p3 = 2 * stats.norm.sf(3)
check(np.isclose(p3, 0.0027, atol=5e-5) and np.isclose(50 * p3, 0.135, atol=5e-4) and np.isclose(1 - (1 - p3) ** 50, 0.1264, atol=5e-4), "l4 s9: p 0.0027, Bonferroni 0.135, Sidak 0.1264")
z = rng.normal(size=(400_000, 50))
check(abs((abs(z).max(axis=1) >= 3).mean() - 0.1264) < 0.003, "l4 s9 explain: best of fifty noise strategies reaches |t| >= 3 about one time in eight")
check(np.isclose(1 - 0.95 ** 30, 0.7854, atol=5e-5) and np.isclose(30 * 0.05, 1.5), "h1 item3: 30 tests, 1.5 expected false positives, 0.7854 chance of at least one")
check(np.isclose(2 * stats.norm.sf(np.sqrt(5)), 0.025, atol=5e-4), "h1 item8: t = sqrt(5) = 2.24 gives p = 0.025 (daily data, normal reference)")
check(np.isclose(stats.norm.cdf(np.sqrt(5) - 1.96) + stats.norm.cdf(-np.sqrt(5) - 1.96), 0.61, atol=0.005), "h1 item8: power 0.61 against a true Sharpe of 1 over five years")
check(np.isclose(1 - 0.975 ** 20, 0.397, atol=0.002) and np.isclose((1.96 + 0.84) ** 2, 7.84), "h1 item8 model: four in ten chance of a p <= 0.025 among twenty; 7.84 years for 80% power")
# BH on best of twenty with p = 0.025: needs at least ten versions at or below 0.025
check(bh([0.025] + [0.5] * 19) == 0 and bh([0.025] * 10 + [0.5] * 10) == 10 and bh([0.025] * 9 + [0.5] * 11) == 0, "h1 item8 follow-up 3: BH passes the 0.025 winner only with at least ten versions at or below it")

# ---------------------------------------------------------------- l5: matrices
J = np.ones((4, 4))
check(np.allclose(sorted(np.linalg.eigvalsh(J)), [0, 0, 0, 4]), "l5 s0: J_4 has eigenvalues 4, 0, 0, 0")
u = np.array([1, 2, 2.0]); check(np.allclose(sorted(np.linalg.eigvalsh(np.outer(u, u))), [0, 0, 9]), "l5 s1: uu^T has eigenvalue |u|^2 = 9")
u, v = np.array([1, 2.0]), np.array([3, 4.0])
check(np.allclose(sorted(np.linalg.eigvals(np.outer(u, v)).real), [0, 11]), "l5 s2: uv^T has eigenvalue v.u = 11")
R = 0.7 * np.eye(5) + 0.3 * np.ones((5, 5)); ev = np.linalg.eigvalsh(R)
check(np.allclose(sorted(ev), [0.7] * 4 + [2.2]) and np.isclose((ev ** 2).sum(), 6.8) and np.isclose((R ** 2).sum(), 6.8) and np.isclose(np.linalg.det(R), 0.52822, atol=5e-5), "l5 s3, s9, s10: eigenvalues 2.2 and 0.7 x4, squares 6.8, det 0.52822, share 0.44")
w = np.array([1, 2, 2.0]); H = np.eye(3) - 2 * np.outer(w, w) / (w @ w)
check(np.allclose(sorted(np.linalg.eigvalsh(H)), [-1, 1, 1]) and np.isclose(np.trace(H), 1), "l5 s4: Householder reflection eigenvalues -1, 1, 1")
check(np.allclose(sorted(np.linalg.eigvalsh(np.eye(3) + np.ones((3, 3)))), [1, 1, 4]), "l5 s5: I + J has 4, 1, 1")
Q = np.array([[0, -1], [1, 0.0]]); check(np.allclose(sorted(np.linalg.eigvals(Q), key=lambda z: z.imag), [-1j, 1j]), "l5 s6: quarter turn has eigenvalues +-i")
A = np.array([[2, 1], [1, 2.0]]); check(np.allclose(sorted(np.linalg.eigvalsh(A)), [1, 3]) and np.isclose((np.linalg.eigvalsh(A) ** 2).sum(), (A ** 2).sum()), "l5 s7: eigenvalues 3 and 1; sum of squares 10")
P = np.outer(w, w) / (w @ w); check(np.allclose(sorted(np.linalg.eigvalsh(P)), [0, 0, 1]) and np.isclose(np.trace(P), 1), "l5 quiz2 and h1 item4: projection eigenvalues 1 and 0, trace = rank")
# oblique projection also has trace = rank
B = np.array([[1, 1], [0, 0.0]]); check(np.allclose(B @ B, B) and np.isclose(np.trace(B), 1), "l5 quiz2: trace = rank holds for any idempotent matrix")
u, v = np.array([2, 1, 2.0]), np.array([1, 3, 1.0]); check(np.isclose(np.trace(np.outer(u, v)), 7), "h1 item4: uv^T eigenvalue 7")
check(np.allclose(sorted(np.linalg.eigvalsh(0.5 * np.eye(3) + 0.5 * np.ones((3, 3)))), [0.5, 0.5, 2]), "l5 quiz3: equicorrelation 0.5, n = 3: 2, 0.5, 0.5")
# rank-one with v perpendicular to u: all eigenvalues 0 (nilpotent)
u, v = np.array([1, 1.0]), np.array([1, -1.0]); check(np.allclose(np.linalg.eigvals(np.outer(u, v)), 0), "l5 s8 explain: v perpendicular to u gives eigenvalue 0 (nilpotent, not diagonalisable)")

print()
if fails:
    print(f"{len(fails)} check(s) failed:")
    for f in fails:
        print(" -", f)
    raise SystemExit(1)
print("all checks passed")
