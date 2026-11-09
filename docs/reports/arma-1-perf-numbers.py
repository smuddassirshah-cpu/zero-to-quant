"""Recompute every number in arma homework-1 item h-aloud-two-notes, each by two routes.

Run with a Python that has numpy and statsmodels (the scratchpad venv):
    python docs/reports/arma-1-perf-numbers.py
Exits 0 when every check passes.
Route A is statsmodels (MacKinnon's response surfaces, or adfuller itself on seeded paths).
Route B is a seeded, vectorised NumPy simulation of the Dickey-Fuller regression.
"""
import json, math, os, sys
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import numpy as np
from statsmodels.tsa.adfvalues import mackinnonp, mackinnoncrit
from statsmodels.tsa.stattools import adfuller

HERE = os.path.dirname(os.path.abspath(__file__))
ITEM_FILE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'arma', 'homework-1.json')
fails = 0
checks = 0

def check(name, ok, detail=''):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
    print(('ok   ' if ok else 'FAIL ') + name + ('  ' + detail if detail else ''))

def df_t(X):
    """Dickey-Fuller t on a constant and x_{t-1}, no lagged changes, one row per path."""
    y = np.diff(X, axis=1)
    z = X[:, :-1]
    m = y.shape[1]
    zc = z - z.mean(1, keepdims=True)
    yc = y - y.mean(1, keepdims=True)
    b = (zc * yc).sum(1) / (zc ** 2).sum(1)
    r = yc - b[:, None] * zc
    s2 = (r ** 2).sum(1) / (m - 2)
    return b / np.sqrt(s2 / (zc ** 2).sum(1))

def ar1_paths(phi, n, sims, rng):
    """Seeded AR(1) paths; a stationary start when |phi| < 1, a walk from 0 when phi = 1."""
    e = rng.standard_normal((sims, n))
    X = np.empty((sims, n))
    X[:, 0] = e[:, 0] / math.sqrt(1 - phi ** 2) if phi < 1 else 0.0
    for t in range(1, n):
        X[:, t] = phi * X[:, t - 1] + e[:, t]
    return X

def se_share(p, n):
    return math.sqrt(p * (1 - p) / n)

item = next(it for it in json.load(open(ITEM_FILE))['items'] if it['id'] == 'h-aloud-two-notes')
text = item['prompt'] + item['model'] + ' '.join(r['text'] for r in item['rubric']) + ' '.join(item['followUps'])
check('rubric sums to 10', sum(r['points'] for r in item['rubric']) == 10)
req = [r for r in item['rubric'] if r.get('required')]
# fix pass AR1-1: rows 1 (note A) and 3 (assumptions the question names) are required; never every row
import itertools
_rows = item['rubric']
_passes = [s for k in range(1, 5) for s in itertools.combinations(range(4), k)
           if sum(_rows[i]['points'] for i in s) >= 7 and all(r_ in s for r_, r in enumerate(_rows) if r.get('required'))]
print('     passing tick sets (row numbers):', [[i + 1 for i in s] for s in _passes])
check('required rows are 1 and 3 and not every row', [i for i, r in enumerate(_rows) if r.get('required')] == [0, 2])
check('every passing set has note A, note B and the assumptions', all({0, 1, 2} <= set(s) for s in _passes) and _passes)
check('AR1-3: no Brownian motion in the model, no "not more frequent prices" in a row',
      'Brownian' not in item['model'] and 'not more frequent prices' not in ' '.join(r['text'] for r in _rows))
# A pass (7 of 10) must need both note rows: without the note B row (4 points) the most is 6.
pts = [r['points'] for r in item['rubric']]
best_without = {i: sum(pts) - pts[i] for i in range(len(pts))}
check('no pass without the note A row (required) or the note B row', best_without[1] < 7 and req[0] is item['rubric'][0])
for s in ['−2.10', '−1.645', '0.35', '120', '−1.53', '−2.89', '−2.86', '46%', '0.24', '0.933', '23%',
          '840', '0.990', 'twelve', '24%', '270 days', 'one time in four']:
    check('stated in item: ' + s, s in text)

N = 120
nobs = N - 1  # adfuller drops one value to difference

# 1. One-sided 5% point of the normal.
from statistics import NormalDist
z05 = NormalDist().inv_cdf(0.05)
check('normal 5% point -1.645', round(z05, 3) == -1.645, f'{z05:.4f}')

# 2. Critical values: route A MacKinnon at nobs and asymptotic; route B simulation quantile.
cv_n = mackinnoncrit(1, 'c', nobs)[1]
cv_inf = mackinnoncrit(1, 'c', np.inf)[1]
rng = np.random.default_rng(20261107)
t_walk = df_t(ar1_paths(1.0, N, 200_000, rng))
q05 = float(np.quantile(t_walk, 0.05))
check('5% point on 120 days is -2.89 (MacKinnon)', round(cv_n, 2) == -2.89, f'{cv_n:.4f}')
check('5% point on 120 days is -2.89 (simulation)', round(q05, 2) == -2.89, f'{q05:.4f}')
check('asymptotic 5% point -2.86 (MacKinnon)', round(cv_inf, 2) == -2.86, f'{cv_inf:.4f}')
t_long = df_t(ar1_paths(1.0, 2000, 20_000, np.random.default_rng(7)))
q05_long = float(np.quantile(t_long, 0.05))
check('long-sample 5% point near -2.86 (simulation, n = 2000)', abs(q05_long + 2.86) < 0.04, f'{q05_long:.4f}')
# adfuller itself reports the same critical value on a 120-day series.
cv_adf = adfuller(np.cumsum(np.random.default_rng(3).standard_normal(N)), maxlag=0, regression='c', autolag=None)[4]['5%']
check('adfuller 5% critical value on 120 days agrees', abs(cv_adf - cv_n) < 1e-9, f'{cv_adf:.4f}')

# 3. Mean of the statistic under a unit root, about -1.53: two seeds, and adfuller on 3,000 paths.
m1 = float(t_walk.mean())
rng2 = np.random.default_rng(99)
t_sm = np.array([adfuller(np.cumsum(rng2.standard_normal(N)), maxlag=0, regression='c', autolag=None)[0] for _ in range(3000)])
m2 = float(t_sm.mean())
check('mean statistic under a walk about -1.53 (NumPy)', abs(m1 + 1.53) < 0.01, f'{m1:.4f}')
check('mean statistic under a walk about -1.53 (adfuller)', abs(m2 + 1.53) < 0.05, f'{m2:.4f}')
# "Shifted left", not "skewed": the whole distribution sits left of 0 (median, 95% point below 0).
med = float(np.median(t_walk)); q95 = float(np.quantile(t_walk, 0.95))
check('shifted left: median about -1.5 and 95% point below 0', -1.6 < med < -1.45 and q95 < 0, f'median {med:.3f}, 95% {q95:.3f}')
check('item says shifted, not skewed', 'skewed' not in text and text.count('shifted left') == 3)

# 4. Share of true walks below -1.645: about 46%.
pA = float(mackinnonp(-1.645, 'c', 1))
pB = float(np.mean(t_walk < -1.645))
check('walks below -1.645: 46% (MacKinnon)', round(100 * pA) == 46, f'{pA:.4f}')
check('walks below -1.645: 46% (simulation)', round(100 * pB) == 46, f'{pB:.4f}')

# 5. p-value of -2.10: about 0.24.
p1 = float(mackinnonp(-2.10, 'c', 1))
p2 = float(np.mean(t_walk < -2.10))
check('p of -2.10 is 0.24 (MacKinnon)', round(p1, 2) == 0.24, f'{p1:.4f}')
check('p of -2.10 is 0.24 (simulation)', round(p2, 2) in (0.24, 0.25) and abs(p2 - p1) < 0.01, f'{p2:.4f}')

# 6. phi for a ten-day half-life.
phi = 0.5 ** (1 / 10)
phi2 = math.exp(-math.log(2) / 10)
check('phi = 0.5^(1/10) = 0.933', round(phi, 3) == 0.933 and abs(phi - phi2) < 1e-15, f'{phi:.5f}')
check('half-life of phi is ten days', abs(math.log(0.5) / math.log(phi) - 10) < 1e-12)

# 7. Power on 120 days at the 5% point: about 23%. Route A adfuller loop, route B NumPy.
t_rev = df_t(ar1_paths(phi, N, 200_000, np.random.default_rng(11)))
powB = float(np.mean(t_rev < cv_n))
rng3 = np.random.default_rng(12)
stats = []
for _ in range(4000):
    x = ar1_paths(phi, N, 1, rng3)[0]
    stats.append(adfuller(x, maxlag=0, regression='c', autolag=None)[0])
powA = float(np.mean(np.array(stats) < cv_n))
check('power 23% on 120 days (NumPy)', round(100 * powB) == 23, f'{powB:.4f}')
check('power about 23% on 120 days (adfuller loop)', abs(powA - powB) < 3 * se_share(powB, 4000), f'{powA:.4f}')
check('power is about one time in four', 0.2 <= powB <= 0.3)
check('p = 0.35 would not reject at 5%', 0.35 > 0.05)

# 8. Hourly over the same span: 840 prices, phi 0.990, twelve half-lives, power about 24%.
nh = 120 * 7
phih = 0.5 ** (1 / 70)
check('840 hourly prices', nh == 840)
check('hourly phi = 0.990', round(phih, 3) == 0.990, f'{phih:.5f}')
check('twelve half-lives either way', 120 / 10 == 12 and 840 / 70 == 12)
check('same local-to-unity c', abs(-120 * math.log(phi) - -840 * math.log(phih)) < 1e-12, f'c = {-120 * math.log(phi):.4f}')
cv_h = mackinnoncrit(1, 'c', nh - 1)[1]
t_h = df_t(ar1_paths(phih, nh, 40_000, np.random.default_rng(13)))
powH = float(np.mean(t_h < cv_h))
check('hourly power about 24% (NumPy)', round(100 * powH) == 24, f'{powH:.4f}')
check('hourly power within 2 points of daily', abs(powH - powB) < 0.02)
rng4 = np.random.default_rng(14)
st_h = [adfuller(ar1_paths(phih, nh, 1, rng4)[0], maxlag=0, regression='c', autolag=None)[0] for _ in range(2000)]
powH2 = float(np.mean(np.array(st_h) < cv_h))
check('hourly power agrees with adfuller loop', abs(powH2 - powH) < 3 * se_share(powH, 2000), f'{powH2:.4f}')

# 9. Days for 80% power: about 270. Route A: power at 260, 270 and 280 days by simulation.
# Route B: local-to-unity, c* from a long sample (n = 2000), then N = c* / ln(1/phi).
def power_at(n, sims, seed, ph=phi):
    t = df_t(ar1_paths(ph, n, sims, np.random.default_rng(seed)))
    return float(np.mean(t < mackinnoncrit(1, 'c', n - 1)[1]))
grid = {n: power_at(n, 60_000, 100 + n) for n in (240, 260, 270, 280, 300)}
print('     power by days', {k: round(v, 3) for k, v in grid.items()})
lo, hi = 240, 300
while hi - lo > 4:
    mid = (lo + hi) // 2
    if power_at(mid, 60_000, 500 + mid) < 0.8:
        lo = mid
    else:
        hi = mid
n80 = (lo + hi) / 2
check('80% power at about 270 days (bisection)', abs(n80 - 270) <= 10, f'{n80}')
L = 2000
clo, chi = 10.0, 25.0
while chi - clo > 0.2:
    c = (clo + chi) / 2
    if power_at(L, 8000, int(c * 100), ph=math.exp(-c / L)) < 0.8:
        clo = c
    else:
        chi = c
cstar = (clo + chi) / 2
n80b = cstar / -math.log(phi)
check('80% power at about 270 days (local to unity)', abs(n80b - 270) <= 20, f'c* = {cstar:.2f}, days = {n80b:.1f}')
check('270 days is a little over a trading year of 252', 252 < 270 < 300)

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
