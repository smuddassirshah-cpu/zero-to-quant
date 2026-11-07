"""Recompute every number in coint homework-1 item h-spurious-aloud, each by two routes.

Run with a Python that has numpy, scipy and statsmodels (the scratchpad venv):
    python docs/reports/coint-1-perf-numbers.py
Exits 0 when every check passes.
Route A is the lesson's own generator (make_two_walks: one seeded normal draw per pair, seeds 0 to 1,999)
with |t| = |r| sqrt((n - 2)/(1 - r^2)) from np.corrcoef.
Route B is a separate seeded stream with the slope, its standard error and R^2 computed from the OLS
formulas (vectorised), checked against statsmodels OLS on a subset; or theory where the item quotes a limit.
"""
import itertools, json, math, os, sys
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from scipy.signal import lfilter
from scipy.stats import norm
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'coint', 'homework-1.json')
fails = 0
checks = 0


def check(name, ok, detail=''):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
    print(('ok   ' if ok else 'FAIL ') + name + ('  ' + str(detail) if detail != '' else ''))


hw = json.load(open(HW))
item = next(it for it in hw['items'] if it['id'] == 'h-spurious-aloud')
text = item['prompt'] + ' ' + item['model'] + ' ' + ' '.join(r['text'] for r in item['rubric']) + ' ' + ' '.join(item['followUps'])

# ---------------------------------------------------------------- 0. shape, homework limits, rubric passes
check('performance aloud, longform', item.get('performance') == 'aloud' and item.get('kind') == 'longform')
check('seconds 180, think 30, 3 follow-ups', item['seconds'] == 180 and item['think'] == 30 and len(item['followUps']) == 3)
pts = [r['points'] for r in item['rubric']]
req = [bool(r.get('required')) for r in item['rubric']]
check('rubric sums to 10, 5 rows', sum(pts) == 10 and len(pts) == 5, pts)
check('rows 1 to 4 required, row 5 not (so not every row is required)', req == [True, True, True, True, False])
named = {0: 'conditions', 1: 't statistic', 2: 'R^2', 3: 'what to run instead'}
passing = []
for k in range(1, 6):
    for s in itertools.combinations(range(5), k):
        if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(5) if req[i]):
            passing.append(s)
print('     passing tick sets:', [[i + 1 for i in s] for s in passing])
check('every passing tick set holds every named part', all(all(i in s for i in named) for s in passing) and len(passing) == 2)
best_wo = {i: max((sum(pts[j] for j in s) for k in range(1, 6) for s in itertools.combinations([j for j in range(5) if j != i], k)), default=0) for i in named}
print('     best total leaving out each named row (points alone):', {named[i]: best_wo[i] for i in named})
items = hw['items']
check('homework holds 6 to 12 items', 6 <= len(items) <= 12, len(items))
check('one performance item in the homework', sum(1 for it in items if it.get('performance')) == 1)
check('a difficulty 5 and a longform item present', any(it['difficulty'] == 5 for it in items) and any(it.get('kind') == 'longform' for it in items))

# ---------------------------------------------------------------- 1. the prompt's t from R^2 = 0.60, n = 1,000
n = 1000
r = math.sqrt(0.60)
tA = r * math.sqrt((n - 2) / (1 - r * r))
rng = np.random.default_rng(1)
a = rng.standard_normal(n); a -= a.mean(); a /= np.linalg.norm(a)
e = rng.standard_normal(n); e -= e.mean(); e -= (e @ a) * a; e /= np.linalg.norm(e)
xs, ys = a * 40 + 100, (r * a + math.sqrt(1 - r * r) * e) * 25 + 80
fit = sm.OLS(ys, sm.add_constant(xs)).fit()
tB = abs(fit.tvalues[1])
check('t from R^2 = 0.60 at n = 1,000 is 38.7 (formula)', round(tA, 1) == 38.7, round(tA, 4))
check('t from statsmodels on a sample with R^2 = 0.60 is 38.7', abs(tA - tB) < 1e-8 and abs(fit.rsquared - 0.6) < 1e-12, round(tB, 4))
check('prompt quotes 38.7, 0.60 and 1,000', all(s in item['prompt'] for s in ('38.7', '0.60', '1,000')))


# ---------------------------------------------------------------- 2. route A: the lesson generator
def make_two_walks(seed, n=500):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    return np.cumsum(z[:, 0]), np.cumsum(z[:, 1])


def route_a(n, sims=2000):
    T, R2, B, SE = [], [], [], []
    for seed in range(sims):
        x, y = make_two_walks(seed, n)
        rr = np.corrcoef(x, y)[0, 1]
        T.append(abs(rr) * math.sqrt((n - 2) / (1 - rr * rr)))
        R2.append(rr * rr)
        xc, yc = x - x.mean(), y - y.mean()
        b = (xc @ yc) / (xc @ xc)
        res = yc - b * xc
        B.append(b)
        SE.append(math.sqrt((res @ res) / (n - 2) / (xc @ xc)))
    return np.array(T), np.array(R2), np.array(B), np.array(SE)


A = {m: route_a(m) for m in (250, 500, 1000, 2000, 4000)}
T, R2, B, SE = A[1000]
pA = (T > 1.96).mean()
q95A = np.quantile(T, 0.95)
shareA = (R2 >= 0.60).mean()
check('lesson figure reproduced: 90.0% at 500 days', abs((A[500][0][:1000] > 1.96).mean() - 0.900) < 1e-12)
check('91.9% of 2,000 pairs of 1,000 days give |t| > 1.96', round(100 * pA, 1) == 91.9, pA)
check('95th percentile of |t| is 48.0', round(q95A, 1) == 48.0, round(q95A, 3))
check('38.7 lies below that 5% point', tA < q95A)
check('R^2 >= 0.60 is the same event as |t| >= 38.7 at fixed n', np.array_equal(R2 >= 0.60, T >= tA - 1e-9))
check('9.4% reach R^2 >= 0.60, about one in eleven', round(100 * shareA, 1) == 9.4 and round(1 / shareA) == 11, (shareA, 1 / shareA))
med = {m: np.median(A[m][1]) for m in A}
check('median R^2 0.18 at 1,000 days', round(med[1000], 2) == 0.18, round(med[1000], 4))
check('median R^2 between 0.16 and 0.18 from 250 to 4,000 days', all(0.155 <= v < 0.185 for v in med.values()), {k: round(v, 3) for k, v in med.items()})
sdB = {m: A[m][2].std() for m in (250, 1000, 4000)}
check('spread of beta-hat about 0.6 at 250, 1,000 and 4,000 days', all(round(v, 1) == 0.6 for v in sdB.values()), {k: round(v, 3) for k, v in sdB.items()})
seR = np.median(A[250][3]) / np.median(A[1000][3]), np.median(A[1000][3]) / np.median(A[4000][3])
check('standard error shrinks like 1/sqrt n (halves when n quadruples)', all(1.8 < v < 2.2 for v in seR), [round(v, 3) for v in seR])
tg = [np.median(A[m][0]) / math.sqrt(m) for m in (250, 1000, 4000)]
check('|t| grows like sqrt n: median |t|/sqrt n steady', max(tg) / min(tg) < 1.15, [round(v, 3) for v in tg])
x, y = make_two_walks(103, 1000)
r0 = np.corrcoef(x, y)[0, 1]; r1 = np.corrcoef(0.3 * x, -7 * y)[0, 1]
f0 = sm.OLS(y, sm.add_constant(x)).fit(); f1 = sm.OLS(7 * y + 3, sm.add_constant(0.3 * x)).fit()
check('t and R^2 unchanged when a series is rescaled', abs(abs(f0.tvalues[1]) - abs(f1.tvalues[1])) < 1e-8 and abs(r0 ** 2 - r1 ** 2) < 1e-12)

# ---------------------------------------------------------------- 3. route B: separate stream, OLS formulas
rngB = np.random.default_rng(20261107)
Z = rngB.standard_normal((4000, 1000, 2))
X, Y = Z[:, :, 0].cumsum(1), Z[:, :, 1].cumsum(1)
Xc, Yc = X - X.mean(1, keepdims=True), Y - Y.mean(1, keepdims=True)
b = (Xc * Yc).sum(1) / (Xc ** 2).sum(1)
res = Yc - b[:, None] * Xc
se = np.sqrt((res ** 2).sum(1) / (n - 2) / (Xc ** 2).sum(1))
tBv = np.abs(b / se)
r2B = 1 - (res ** 2).sum(1) / (Yc ** 2).sum(1)
sm_t = [abs(sm.OLS(Y[i], sm.add_constant(X[i])).fit().tvalues[1]) for i in range(40)]
check('route B: vectorised t equals statsmodels on 40 pairs', np.allclose(sm_t, tBv[:40], rtol=1e-9))
pB = (tBv > 1.96).mean()
seP = math.sqrt(pA * (1 - pA) / 2000 + pB * (1 - pB) / 4000)
check('route B agrees on the |t| > 1.96 share (within 3 se)', abs(pA - pB) < 3 * seP, (round(pB, 4), round(seP, 4)))
shB = (r2B >= 0.60).mean()
seS = math.sqrt(shareA * (1 - shareA) / 2000 + shB * (1 - shB) / 4000)
check('route B agrees on the R^2 >= 0.60 share (within 3 se)', abs(shareA - shB) < 3 * seS, round(shB, 4))
boot = np.random.default_rng(3)
qs = [np.quantile(T[boot.integers(0, 2000, 2000)], 0.95) for _ in range(300)]
q95B = np.quantile(tBv, 0.95)
check('route B agrees on the 95th percentile (within 3 bootstrap se)', abs(q95A - q95B) < 3 * np.std(qs) * math.sqrt(1.5), (round(q95B, 2), round(np.std(qs), 2)))
check('route B median R^2 rounds to 0.18', round(np.median(r2B), 2) == 0.18, round(np.median(r2B), 4))
check('route B spread of beta-hat about 0.6', round(b.std(), 1) == 0.6, round(b.std(), 3))
# independent noise: R^2 falls like 1/n, so n R^2 is steady (median of chi-square 1 is 0.455)
nr = []
for m in (250, 4000):
    W = np.random.default_rng(m).standard_normal((2000, m, 2))
    cc = [np.corrcoef(W[i, :, 0], W[i, :, 1])[0, 1] ** 2 for i in range(2000)]
    nr.append(m * np.median(cc))
check('independent noise: median n R^2 near 0.455 at 250 and 4,000 (R^2 like 1/n)', all(abs(v - norm.ppf(0.75) ** 2) < 0.06 for v in nr), [round(v, 3) for v in nr])


# ---------------------------------------------------------------- 4. follow-up 1: drift 0.05 a day in each
def drift_stats(m, sims, seed0, mu=0.05, chunk=250):
    R, Tt = [], []
    for c0 in range(0, sims, chunk):
        Zd = np.random.default_rng(seed0 + c0).standard_normal((min(chunk, sims - c0), m, 2))
        Xd, Yd = (mu + Zd[:, :, 0]).cumsum(1), (mu + Zd[:, :, 1]).cumsum(1)
        xc, yc = Xd - Xd.mean(1, keepdims=True), Yd - Yd.mean(1, keepdims=True)
        bb = (xc * yc).sum(1) / (xc ** 2).sum(1)
        rs = yc - bb[:, None] * xc
        R.extend(1 - (rs ** 2).sum(1) / (yc ** 2).sum(1))
        Tt.extend(np.abs(bb) / np.sqrt((rs ** 2).sum(1) / (m - 2) / (xc ** 2).sum(1)))
    return np.median(R), np.median(Tt)


dA = {m: drift_stats(m, 1000, 10 ** 6) for m in (1000, 4000, 16000)}
dB = {m: drift_stats(m, 1000, 5 * 10 ** 6) for m in (1000, 16000)}
check('drift: median R^2 0.49 at 1,000 days', round(dA[1000][0], 2) == 0.49 and abs(dA[1000][0] - dB[1000][0]) < 0.03, (round(dA[1000][0], 4), round(dB[1000][0], 4)))
check('drift: median R^2 0.97 at 16,000 days', round(dA[16000][0], 2) == 0.97 and abs(dA[16000][0] - dB[16000][0]) < 0.01, (round(dA[16000][0], 4), round(dB[16000][0], 4)))
ratio = dA[16000][1] / dA[4000][1]
check('drift: |t| grows like n (x4 from 4,000 to 16,000 days, not x2)', 3.4 < ratio < 4.6, round(ratio, 3))

# ---------------------------------------------------------------- 5. follow-up 2: cointegrated pair
def coint_case(phi, m, sims=2000, seed=7):
    Zc = np.random.default_rng(seed).standard_normal((sims, m, 2))
    Xc_ = Zc[:, :, 0].cumsum(1)
    Zu = Zc[:, :, 1].copy()
    if phi > 0:
        Zu[:, 0] /= math.sqrt(1 - phi ** 2)
    U = lfilter([1.0], [1.0, -phi], Zu, axis=1)
    Yc_ = 1.5 * Xc_ + U
    xc, yc = Xc_ - Xc_.mean(1, keepdims=True), Yc_ - Yc_.mean(1, keepdims=True)
    bb = (xc * yc).sum(1) / (xc ** 2).sum(1)
    rs = yc - bb[:, None] * xc
    s_ = np.sqrt((rs ** 2).sum(1) / (m - 2) / (xc ** 2).sum(1))
    return np.std(bb - 1.5), (np.abs((bb - 1.5) / s_) > 1.96).mean()


c250, c1000 = coint_case(0.8, 250), coint_case(0.8, 1000)
check('cointegrated: error of beta-hat shrinks like 1/n (x4 from 250 to 1,000)', 3.4 < c250[0] / c1000[0] < 4.6, round(c250[0] / c1000[0], 3))
i1000 = coint_case(0.0, 1000)
check('cointegrated, independent residual: about 5% pass 1.96', abs(i1000[1] - 0.05) < 0.015, i1000[1])
check('spread sqrt((1 + 0.8)/(1 - 0.8)) = 3', abs(math.sqrt(1.8 / 0.2) - 3) < 1e-12)
lim = 2 * norm.sf(1.96 / 3)
check('limit: about 51% pass 1.96 (2 P(Z > 0.653))', round(100 * lim) == 51, round(lim, 4))
check('seeded run of 1,000 days agrees with the limit (within 0.03)', abs(c1000[1] - lim) < 0.03, c1000[1])
U = lfilter([1.0], [1.0, -0.8], np.random.default_rng(11).standard_normal((4000, 2000)), axis=1)[:, 200:]
var_u, lrv = U.var(), (U.shape[1] * U.mean(1).var())
check('AR(0.8) variance 1/(1 - 0.64) = 2.78 and long-run variance 1/0.04 = 25', abs(var_u - 1 / 0.36) < 0.1 and abs(lrv - 25) < 2, (round(var_u, 3), round(lrv, 2)))
check('long-run over plain variance is (1 + phi)/(1 - phi) = 9', abs((1 / 0.04) / (1 / 0.36) - 9) < 1e-12)

# ---------------------------------------------------------------- 6. follow-up 3: a share that copies another a day late
cs, ps = [], []
for s in range(300):
    z = np.random.default_rng(3 * 10 ** 6 + s).standard_normal((1001, 2))
    xo = np.cumsum(z[:, 0]); yl = xo[:-1] + z[1:, 1]; xl = xo[1:]
    if s == 0:
        check('gap y_t - x_t equals v_t - eps_t exactly', np.allclose(yl - xl, z[1:, 1] - z[1:, 0]))
    cs.append(np.corrcoef(np.diff(xl), np.diff(yl))[0, 1])
    if s < 100:
        ps.append(coint(yl, xl)[1])
cs = np.array(cs); m = 999
tc = np.abs(cs) * np.sqrt((m - 2) / (1 - cs ** 2))
check('same-day changes uncorrelated: mean corr near 0', abs(cs.mean()) < 3 * cs.std() / math.sqrt(300), round(cs.mean(), 4))
check('changes regression passes 1.96 about 5% of the time', abs((tc > 1.96).mean() - 0.05) < 0.03, round((tc > 1.96).mean(), 4))
check('Engle-Granger rejects the tie at 1% on all 100', max(ps) < 0.01, max(ps))

# ---------------------------------------------------------------- 7. every quoted figure is in the item
for sfig in ('91.9%', '48.0', '38.7', '0.60', '9.4%', 'one in eleven', 'is 0.18 at 1,000', 'between 0.16 and 0.18', 'about 0.6 at 250, 1,000 and 4,000',
             '0.49 at 1,000 days and 0.97 at 16,000', '0.05 a day', 'about 51%', '= 3', '2,000 independent pairs', 'seeds 0 to 1,999', 'nine unrelated pairs in ten', '$\\phi = 0.8$'):
    check('item states ' + sfig, sfig in text)
for bad in ('!', '—', '–'):
    check('no ' + repr(bad), bad not in text)

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
