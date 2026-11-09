"""Recompute every number and closed form in arma homework-3 item h-derive-arma-fan.

Run with a Python that has numpy, sympy and statsmodels (the scratchpad venv):
    python docs/reports/arma-3-perf-numbers.py
Exits 0 when every check passes.
Route A: sympy (the induction step, the closed form against the raw sum, the limit, the series' variance).
Route B: statsmodels (psi weights from arma2ma, the ARMA autocovariance, ARIMA forecast variances with fixed
parameters) and a seeded simulation of the future from a fixed today.
"""
import json, math, os, sys, warnings
warnings.filterwarnings('ignore')
import numpy as np
import sympy as sp
from statsmodels.tsa.arima_process import arma2ma, ArmaProcess

HERE = os.path.dirname(os.path.abspath(__file__))
ITEM_FILE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'arma', 'homework-3.json')
fails = checks = 0

def check(name, ok, detail=''):
    global fails, checks
    checks += 1
    fails += 0 if ok else 1
    print(('ok   ' if ok else 'FAIL ') + name + ('  ' + detail if detail else ''))

item = next(it for it in json.load(open(ITEM_FILE))['items'] if it['id'] == 'h-derive-arma-fan')
text = item['prompt'] + item['model'] + ' '.join(r['text'] for r in item['rubric'])
pts = [r['points'] for r in item['rubric']]
req = [i for i, r in enumerate(item['rubric']) if r.get('required')]
check('rubric sums to 10', sum(pts) == 10)
# fix pass AR3-1: rows 2 (weights), 3 (variance and limit) are core; row 4 (series check, half-widths) is named by the question
import itertools
_passes = [s for k in range(1, 5) for s in itertools.combinations(range(4), k)
           if sum(pts[i] for i in s) >= 7 and all(r in s for r in req)]
print('     passing tick sets (row numbers):', [[i + 1 for i in s] for s in _passes])
check('required rows are 2 and 4, not every row', req == [1, 3])
check('every passing set has the weights, the variance and the series check', all({1, 2, 3} <= set(s) for s in _passes) and _passes)
check('no pass without the variance-and-limit row', sum(pts) - pts[2] < 7)
check('no derivation item fields that the validator refuses', not any(k in item for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')))
for s in ['0.8', '-0.4', '\\sigma = 2', '0.4', '0.64', '3.92', '2.3117', '5.4795', '4.59', '0.52/0.36', '5.7778',
          '2.4037', '4.71', '6.53', '1.96 \\times 2/0.6']:
    check('stated in item: ' + s, s in text)

# ---------- Route A: sympy ----------
phi, th, sig, yn, en = sp.symbols('phi theta sigma y_n e_n', real=True)
def psi(j):
    return sp.Integer(1) if j == 0 else (phi + th) * phi ** (j - 1)
H = 8
eps = sp.symbols('e1:%d' % (H + 1))          # eps[k-1] is the shock on day n + k
# Run the recursion forward symbolically and compare with the claimed split at every h.
y_prev, e_prev = yn, en
for h in range(1, H + 1):
    y_h = phi * y_prev + eps[h - 1] + th * e_prev
    claim = phi ** (h - 1) * (phi * yn + th * en) + sum(psi(j) * eps[h - 1 - j] for j in range(h))
    check(f'split of y_(n+{h}) into known part and psi-weighted shocks', sp.expand(y_h - claim) == 0)
    y_prev, e_prev = y_h, eps[h - 1]
# The induction step in general: phi*psi_0 + theta = psi_1 and phi*psi_j = psi_(j+1).
j = sp.symbols('j', integer=True, positive=True)
check('phi psi_0 + theta = psi_1', sp.simplify(phi * 1 + th - psi(1)) == 0)
check('phi psi_j = psi_(j+1) for j >= 1', sp.simplify(phi * (phi + th) * phi ** (j - 1) - (phi + th) * phi ** j) == 0)
# Closed form against the raw sum of squared weights.
hh = sp.symbols('h', integer=True, positive=True)
closed = sig ** 2 * (1 + (phi + th) ** 2 * (1 - phi ** (2 * (hh - 1))) / (1 - phi ** 2))
for h in range(1, 9):
    raw = sig ** 2 * sum(psi(k) ** 2 for k in range(h))
    check(f'closed form equals the sum of squared weights at h = {h}', sp.simplify(raw - closed.subs(hh, h)) == 0)
k = sp.symbols('k', integer=True)
gsum = sp.summation(phi ** (2 * (k - 1)), (k, 1, hh - 1))
check('geometric sum (sympy summation)', sp.simplify(sp.piecewise_fold(gsum).args[-1][0] - (1 - phi ** (2 * (hh - 1))) / (1 - phi ** 2)) == 0
      if isinstance(gsum, sp.Piecewise) else sp.simplify(gsum - (1 - phi ** (2 * (hh - 1))) / (1 - phi ** 2)) == 0)
limit_form = sig ** 2 * (1 + 2 * phi * th + th ** 2) / (1 - phi ** 2)
check('one denominator: 1 - phi^2 + (phi + theta)^2 = 1 + 2 phi theta + theta^2', sp.expand(1 - phi ** 2 + (phi + th) ** 2 - (1 + 2 * phi * th + th ** 2)) == 0)
lim_num = sp.limit(closed.subs({phi: sp.Rational(4, 5), th: sp.Rational(-2, 5), sig: 2}), hh, sp.oo)
check('limit at the item values is 52/9 (sympy limit)', lim_num == sp.Rational(52, 9), str(lim_num))
check('limit form at the item values is 52/9', sp.simplify(limit_form.subs({phi: sp.Rational(4, 5), th: sp.Rational(-2, 5), sig: 2})) == sp.Rational(52, 9))
g0 = sp.symbols('gamma0')
g0_sol = sp.solve(sp.Eq(g0, phi ** 2 * g0 + sig ** 2 + th ** 2 * sig ** 2 + 2 * phi * th * sig ** 2), g0)[0]
check("series' variance equals the limit", sp.simplify(g0_sol - limit_form) == 0)
check('theta = 0 gives the AR(1) result', sp.simplify(closed.subs(th, 0) - sig ** 2 * (1 - phi ** (2 * hh)) / (1 - phi ** 2)) == 0)
check('theta = -phi gives sigma^2 at every h', sp.simplify(closed.subs(th, -phi) - sig ** 2) == 0)
for h in range(1, 9):
    check(f'variance never falls: step {h} to {h + 1} adds psi_{h}^2 sigma^2 >= 0',
          sp.simplify(closed.subs(hh, h + 1) - closed.subs(hh, h) - sig ** 2 * psi(h) ** 2) == 0)

# ---------- The numbers, two ways ----------
P, T, S = 0.8, -0.4, 2.0
def var_closed(h):
    return S ** 2 * (1 + (P + T) ** 2 * (1 - P ** (2 * (h - 1))) / (1 - P ** 2))
w = arma2ma(np.r_[1, -P], np.r_[1, T], lags=200)
def var_psi(h):
    return S ** 2 * float(np.sum(w[:h] ** 2))
check('psi weights from statsmodels match (phi + theta) phi^(j-1)', np.allclose(w[1:10], [(P + T) * P ** (j - 1) for j in range(1, 10)]))
check('phi + theta = 0.4, phi^2 = 0.64', round(P + T, 10) == 0.4 and round(P ** 2, 10) == 0.64)
geo5 = (1 - P ** 8) / 0.36
check('h = 5 sum (1 - 0.8^8)/0.36 = 2.3117', round(geo5, 4) == 2.3117 and abs(geo5 - sum(P ** (2 * (j - 1)) for j in range(1, 5))) < 1e-12, f'{geo5:.6f}')
v1, v5, vinf = var_closed(1), var_closed(5), S ** 2 * (1 + 2 * P * T + T ** 2) / (1 - P ** 2)
check('Var(e_1) = 4', abs(v1 - 4) < 1e-12 and abs(var_psi(1) - 4) < 1e-12)
check('Var(e_5) = 5.4795', round(v5, 4) == 5.4795 and abs(var_psi(5) - v5) < 1e-12, f'{v5:.6f}')
check('4(1 + 0.16 x 2.3117) gives 5.4795 also from the rounded sum', round(4 * (1 + 0.16 * 2.3117), 4) == 5.4795)
check('limit 4 x 0.52/0.36 = 5.7778', round(4 * 0.52 / 0.36, 4) == 5.7778 and abs(vinf - 4 * 0.52 / 0.36) < 1e-12, f'{vinf:.6f}')
acov0 = float(ArmaProcess(np.r_[1, -P], np.r_[1, T]).acovf(1)[0]) * S ** 2
check('limit equals the series variance from statsmodels acovf', abs(acov0 - vinf) < 1e-9, f'{acov0:.6f}')
check('limit equals the sum of all squared psi weights', abs(var_psi(200) - vinf) < 1e-9)
check('sqrt(5.7778) = 2.4037', round(math.sqrt(vinf), 4) == 2.4037)
hw = lambda v: 1.96 * math.sqrt(v)
check('half-width h = 1 is 3.92 bp', round(hw(v1), 2) == 3.92)
check('half-width h = 5 is 4.59 bp', round(hw(v5), 2) == 4.59 and round(1.96 * math.sqrt(5.4795), 2) == 4.59, f'{hw(v5):.4f}')
check('half-width limit 1.96 x 2.4037 = 4.71 bp', round(hw(vinf), 2) == 4.71 and round(1.96 * 2.4037, 2) == 4.71, f'{hw(vinf):.4f}')
check('AR(1) with phi 0.8, sigma 2 levels off at 1.96 x 2/0.6 = 6.53 bp', round(1.96 * 2 / 0.6, 2) == 6.53 and abs(hw(S ** 2 / (1 - P ** 2)) - 1.96 * 2 / 0.6) < 1e-12)

# statsmodels ARIMA with the parameters fixed: forecast variances at h = 1, 5 and 200.
from statsmodels.tsa.arima.model import ARIMA
rng = np.random.default_rng(31)
e = rng.standard_normal(3001) * S
x = np.empty(3000); yv = 0.0
for t in range(3000):
    yv = P * yv + e[t + 1] + T * e[t]
    x[t] = 10 + yv
res = ARIMA(x, order=(1, 0, 1)).filter(np.array([10.0, P, T, S ** 2]))
vf = res.get_forecast(200).var_pred_mean
check('ARIMA forecast variance at h = 1, 5, 200 matches', abs(vf[0] - v1) < 1e-6 and abs(vf[4] - v5) < 1e-6 and abs(vf[199] - vinf) < 1e-6,
      f'{vf[0]:.4f}, {vf[4]:.4f}, {vf[199]:.4f}')

# Seeded simulation: fix today's y_n and e_n, simulate 400,000 futures, compare the spread of x_(n+h).
rng = np.random.default_rng(2026)
M = 400_000
y0, e0 = 1.7, -0.9
yy, ee = np.full(M, y0), np.full(M, e0)
emp = {}
for h in range(1, 41):
    new = rng.standard_normal(M) * S
    yy = P * yy + new + T * ee
    ee = new
    if h in (1, 5, 40):
        emp[h] = (float(yy.var()), float(yy.mean()))
for h, v in ((1, v1), (5, v5), (40, var_closed(40))):
    se = v * math.sqrt(2 / M)
    check(f'simulated Var at h = {h} within 4 se of the closed form', abs(emp[h][0] - v) < 4 * se, f'{emp[h][0]:.4f} vs {v:.4f}')
    fc = P ** (h - 1) * (P * y0 + T * e0)
    check(f'simulated mean at h = {h} equals the forecast', abs(emp[h][1] - fc) < 4 * math.sqrt(v / M), f'{emp[h][1]:.4f} vs {fc:.4f}')
check('h = 40 is within 1e-6 of the limit', abs(var_closed(40) - vinf) < 1e-6)

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
