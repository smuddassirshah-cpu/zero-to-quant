"""Second route for the statistics items of bank part 2: seeded simulation or brute force, and the theory
statements in the choice items and explanations. Independent of the authors' scripts. Exit 0 when all hold.
Run: <venv>/bin/python stats_sim.py"""
import sys
import numpy as np
from scipy import stats

rng = np.random.default_rng(20261112)
bad = 0
def chk(name, got, want, tol):
    global bad
    ok = abs(got - want) <= tol
    if not ok: bad += 1
    print('%s %-58s got %.5f want %.5f (tol %g)' % ('ok  ' if ok else 'FAIL', name, got, want, tol))
def claim(name, cond):
    global bad
    if not cond: bad += 1
    print('%s %s' % ('ok  ' if cond else 'FAIL', name))

# s1
chk('median se, n=100 sd 2 (large-sample 0.2507)', np.median(rng.normal(0, 2, (200000, 100)), axis=1).std(), 0.2507, 0.003)
x = rng.normal(size=400000); x2 = 0.4 * x + rng.normal(size=400000); y = 1.5 * x - 2 * x2 + rng.normal(size=400000)
chk('left-out factor: slope of y on x1 alone', np.cov(x, y)[0, 1] / x.var(), 0.7, 0.01)
e = rng.normal(0, 4, 400000); s = np.zeros_like(e)
for t in range(1, len(e)): s[t] = 0.6 * s[t - 1] + e[t]
chk('AR(1) 0.6, noise var 16: variance', s[1000:].var(), 25, 0.3)
m = e[1:] + 0.75 * e[:-1]
chk('MA(1) 0.75 lag-1 autocorrelation', np.corrcoef(m[1:], m[:-1])[0, 1], 0.48, 0.005)
# correlation bounds: smallest eigenvalue at the cap is zero, just above is negative
def mineig(r): return np.linalg.eigvalsh(np.array([[1, .28, r], [.28, 1, .96], [r, .96, 1]])).min()
claim('corr cap 0.5376: matrix psd at 0.5376, not at 0.5386; psd at 0, not at -0.001', mineig(0.5376) > -1e-9 and mineig(0.5386) < 0 and mineig(0.0) > -1e-9 and mineig(-0.001) < 0)
chk('power, n=36 sd 12 mean 4 one-sided 1.645', (rng.normal(4, 12, (200000, 36)).mean(axis=1) / 2 > 1.645).mean(), 0.6387, 0.004)
chk('13 of 16 two-sided exact', 2 * stats.binom.sf(12, 16, 0.5), 0.021271, 1e-6)
# s2
cs = np.linspace(0, 1.5, 1501); mse = 3 * cs ** 2 + 9 * (cs - 1) ** 2
chk('shrinkage: best c on a grid', cs[mse.argmin()], 0.75, 0.0011); chk('shrinkage: mse at best c', mse.min(), 2.25, 1e-3)
xs = np.array([1, 2, 3.]); ys = np.array([2, 3, 7.]); b = np.polyfit(xs, ys, 1); b2 = np.polyfit(np.append(xs, 2), np.append(ys, 10), 1)
claim('point at the mean: slope 2.5 and intercept -1, then 2.5 and 0.5', np.allclose(b, [2.5, -1]) and np.allclose(b2, [2.5, 0.5]))
fell_adj = fell_r2 = 0; R = 4000
for _ in range(R):
    X = rng.normal(size=(50, 1)); yy = 1 + X[:, 0] + rng.normal(size=50); z = rng.normal(size=50)
    def r2(A):
        A = np.column_stack([np.ones(50), A]); res = yy - A @ np.linalg.lstsq(A, yy, rcond=None)[0]
        return 1 - res @ res / ((yy - yy.mean()) @ (yy - yy.mean())), A.shape[1]
    (r_a, k_a), (r_b, k_b) = r2(X), r2(np.column_stack([X, z]))
    adj = lambda r, k: 1 - (1 - r) * 49 / (50 - k)
    fell_r2 += r_b < r_a - 1e-12; fell_adj += adj(r_b, k_b) < adj(r_a, k_a)
claim('noise predictor: R2 never fell', fell_r2 == 0)
chk('noise predictor: share of fits where adjusted R2 fell (|t| < 1, t on 47 df)', fell_adj / R, 2 * stats.t.cdf(1, 47) - 1, 0.025)
chk('content prints 1,362 of 2,000', 1362 / 2000, 2 * stats.t.cdf(1, 47) - 1, 0.025)
xt = rng.normal(0, np.sqrt(5), 400000); yo = 1.2 * xt + rng.normal(size=400000); xo = xt + rng.normal(0, np.sqrt(3), 400000)
chk('noisy regressor: reported slope', np.cov(xo, yo)[0, 1] / xo.var(), 0.75, 0.01)
r = rng.normal(size=400001); ret = r[1:] - 0.1535 * r[:-1]   # MA(1) with rho1 = -0.15
rho = np.corrcoef(ret[1:], ret[:-1])[0, 1]
chk('two-day variance ratio equals 1 + rho1', (ret[1:] + ret[:-1]).var() / (2 * ret.var()), 1 + rho, 0.003)
chk('CLT: mean of 100 skewed draws (gamma, mean 5 sd 4) above 5.8', (rng.gamma(25 / 16, 16 / 5, (200000, 100)).mean(axis=1) > 5.8).mean(), 0.0228, 0.004)
c = np.linspace(0, 3, 3001); d = np.abs(stats.norm.sf(c) - stats.norm.cdf(c - 3))
chk('equal error cut-off', c[d.argmin()], 1.5, 0.0011)
# s3
w = np.linspace(0, 1, 100001); pv = w ** 2 * 4 + (1 - w) ** 2 * 12
chk('pooled variance minimum', pv.min(), 3, 1e-6); chk('pooled weight', w[pv.argmin()], 0.75, 1e-4)
d5 = rng.normal(0, np.sqrt(10), (400000, 5))
chk('variance estimate dividing by n, n=5 var 10', ((d5 - d5.mean(axis=1, keepdims=True)) ** 2).sum(axis=1).mean() / 5, 8, 0.05)
chk('chi-squared 5% point on 5 df', stats.chi2.ppf(0.95, 5), 11.07, 0.005)
chk('sample 197: power', (np.abs(rng.normal(2, 10, (60000, 197)).mean(axis=1)) / (10 / np.sqrt(197)) > 1.96).mean(), 0.8015, 0.006)
# fanning residuals: unbiased slope, usual error understates when the noise grows with x (x uniform on 0 to 10, the authors' design)
sl = []; se = []
for _ in range(4000):
    xx = rng.uniform(0, 10, 50); yy = 1 + 0.5 * xx + rng.normal(0, 0.2 * xx)
    res = stats.linregress(xx, yy); sl.append(res.slope); se.append(res.stderr)
chk('fanning: mean slope', np.mean(sl), 0.5, 0.004); chk('fanning: reported error', np.mean(se), 0.057, 0.002); chk('fanning: true spread', np.std(sl), 0.063, 0.003)
# the same fan with x centred on zero (noise sd 0.2|x|): the usual error is wrong the same way; with noise largest in the middle it overstates
sl = []; se = []
for _ in range(4000):
    xx = rng.uniform(0, 10, 50); yy = 1 + 0.5 * xx + rng.normal(0, 0.2 * (10 - np.abs(2 * xx - 10)))
    res = stats.linregress(xx, yy); sl.append(res.slope); se.append(res.stderr)
print('     note: noise largest mid-range: reported %.4f against true %.4f (the usual error can overstate too, so "wrong", not "too small", is the right word)' % (np.mean(se), np.std(sl)))
# least squares is NOT unbiased "whatever the noise": noise correlated with x biases it
xx = rng.normal(size=200000); u = 0.5 * xx + rng.normal(size=200000); yy = 0.5 * xx + u
claim('counter-example to "unbiased whatever the noise": noise correlated with x gives slope %.3f, not 0.5' % (np.cov(xx, yy)[0, 1] / xx.var()), abs(np.cov(xx, yy)[0, 1] / xx.var() - 1.0) < 0.02)
# Frisch-Waugh-Lovell, exact in sample
n = 500; x2 = rng.normal(size=n); x1 = 0.7 * x2 + rng.normal(size=n); yy = 2 * x1 + 1.3 * x2 + rng.normal(size=n)
full = np.linalg.lstsq(np.column_stack([np.ones(n), x1, x2]), yy, rcond=None)[0][1]
resid = lambda a, b_: a - np.polyval(np.polyfit(b_, a, 1), b_)
ry, r1 = resid(yy, x2), resid(x1, x2)
claim('FWL: residual on residual equals the full coefficient', abs(np.polyfit(r1, ry, 1)[0] - full) < 1e-10)
claim('FWL distractor: residual of y on raw x1 differs', abs(np.polyfit(x1, ry, 1)[0] - full) > 0.05)
claim('FWL distractors: simple slope and mean of two simple slopes differ', abs(np.polyfit(x1, yy, 1)[0] - full) > 0.05 and abs((np.polyfit(x1, yy, 1)[0] + np.polyfit(x2, yy, 1)[0]) / 2 - full) > 0.05)
wn = rng.normal(size=(20000, 400)); wn = wn - wn.mean(axis=1, keepdims=True)
r1s = (wn[:, 1:] * wn[:, :-1]).sum(axis=1) / (wn ** 2).sum(axis=1)
chk('white noise n=400: share of lag-1 sample autocorrelations beyond 0.098', (np.abs(r1s) > 0.098).mean(), 0.05, 0.006)
S = np.full((25, 25), 0.25 * 0.04); np.fill_diagonal(S, 0.04); wv = np.full(25, 1 / 25)
chk('equicorrelation 25 assets: vol', np.sqrt(wv @ S @ wv), 0.10583, 1e-5)
p14 = rng.binomial(200, 0.01, 400000)
chk('200 nulls at 1%: mean false passes', p14.mean(), 2, 0.02)
# s4
chk('se of sample sd, n=50 sd 1.2', rng.normal(0, 1.2, (400000, 50)).std(axis=1, ddof=1).std(), 0.12, 0.002)
chk('sd of the sample proportion, n=100 p=0.2 (reaches the bound)', (rng.binomial(100, 0.2, 400000) / 100).std(), 0.04, 0.0005)
g = rng.normal(10.4, 2, (100000, 50)).mean(axis=1) - rng.normal(9.6, 2, (100000, 50)).mean(axis=1)
chk('two desks (independent): sd of the gap in means', g.std(), 0.4, 0.004)
pr = rng.uniform(size=2000000); three = rng.uniform(size=(2000000, 3)) < pr[:, None]; keep = three.all(axis=1)
chk('uniform prior, three from three: chance of a fourth', (rng.uniform(size=keep.sum()) < pr[keep]).mean(), 0.8, 0.003)
chk('larger of two standard normals', rng.normal(size=(2000000, 2)).max(axis=1).mean(), 0.5642, 0.002)
xl = np.array([1, 2, 3, 4, 20.]); A = np.column_stack([np.ones(5), xl]); H = A @ np.linalg.inv(A.T @ A) @ A.T
claim('leverage: 0.984 at x=20, others at most 0.3', abs(H[4, 4] - 0.984) < 1e-9 and np.diag(H)[:4].max() <= 0.3 + 1e-9)
rej = rejd = 0; R = 1000
for _ in range(R):
    a = rng.normal(size=500).cumsum(); b_ = rng.normal(size=500).cumsum()
    rej += abs(stats.linregress(a, b_).slope / stats.linregress(a, b_).stderr) > 1.96
    da, db = np.diff(a), np.diff(b_); rr = stats.linregress(da, db); rejd += abs(rr.slope / rr.stderr) > 1.96
chk('two walks, 500 steps: share with |t| > 1.96 (content prints 88.0%)', rej / R, 0.88, 0.035)
chk('two walks differenced (content prints 5.0%)', rejd / R, 0.05, 0.02)
r100 = r2000 = 0
for _ in range(600):
    a = rng.normal(size=2000).cumsum(); b_ = rng.normal(size=2000).cumsum()
    q = stats.linregress(a[:100], b_[:100]); r100 += abs(q.slope / q.stderr) > 1.96
    q = stats.linregress(a, b_); r2000 += abs(q.slope / q.stderr) > 1.96
claim('two walks: longer sample rejects more often (100 steps %.2f, 2000 steps %.2f)' % (r100 / 600, r2000 / 600), r2000 > r100)
print('failed:', bad)
sys.exit(1 if bad else 0)
