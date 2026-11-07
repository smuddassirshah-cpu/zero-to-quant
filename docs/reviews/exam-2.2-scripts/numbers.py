"""Second reader's number script for app/content/exams/topic-2.2.json (review-exam-2.2.md).

Recomputes every graded key and every wrong[] value, the numbers in prose, feedback and explanations, and runs
the three code items (solution passes every example and hidden test, starter fails each). Routes: closed forms
written out again; the shipped series themselves (e-spurious-fit, e-breach-days, the bar charts); and three
datasets regenerated from the courses' own helpers, which reproduce the shipped output exactly:
e-eg-critical is make_pair(3, 400, phi=0.96), e-ma-identify is make_arma([], [-0.7], 500, 63) with the
Yule-Walker ('ywm') PACF, and e-returns-note is make_pair(14, 750).
A check that fails because the content is wrong stays failing; each such check is a finding in the review.
Needs numpy, scipy and statsmodels (0.15.0 used). Run: python3 docs/reviews/exam-2.2-scripts/numbers.py
"""
import os
import sys

# This file is named numbers.py, which shadows the standard library's `numbers` (NumPy imports it).
# Drop the script's own folder from the path before any other import.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:] = [p for p in sys.path if os.path.abspath(p or os.getcwd()) != HERE]

import json  # noqa: E402
import math  # noqa: E402
import warnings  # noqa: E402

import numpy as np  # noqa: E402
from scipy import stats

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

import statsmodels.api as sm  # noqa: E402
from statsmodels.tsa.stattools import adfuller, coint, acf, pacf  # noqa: E402
from statsmodels.tsa.adfvalues import mackinnonp  # noqa: E402
from statsmodels.tsa.coint_tables import c_sjt  # noqa: E402
from statsmodels.tsa.arima.model import ARIMA  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.2.json')
COURSES = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'courses')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
idx = {it['id']: k for k, it in enumerate(doc['items'])}
IT = {it['id']: it for it in doc['items']}


def P(iid):
    return f'items[{idx[iid]}]'


def node(path):
    return _walk(doc, path)[0]


def near(a, b, t):
    return abs(a - b) <= t


def key(iid, value, path='widget', t=None):
    """The graded answer equals the recomputed value, within a tenth of its tolerance (or t)."""
    w = node(f'{P(iid)}.{path}')
    tol = w.get('tol', {}).get('abs', 0)
    t = t if t is not None else max(tol / 10, 1e-9)
    ok = near(w['answer'], value, t)
    ex._rec(ok, f'{iid} {path} answer {w["answer"]!r} = {value:.6g}', '' if ok else 'recomputed value differs')


def inband(iid, typed, path='widget', label='typed answer'):
    """A value typed at the precision asked lies inside the answer's tolerance."""
    w = node(f'{P(iid)}.{path}')
    ok = abs(typed - w['answer']) <= w['tol']['abs'] + 1e-9
    ex._rec(ok, f'{iid} {label} {typed!r} graded right', '' if ok else 'outside the answer tolerance')


def wrong(iid, wid, value, typed=None, t=None):
    w = node(f'{P(iid)}.widget')
    ws = [x for x in w['wrong'] if x['id'] == wid]
    if not ws:
        return ex._rec(False, f'{iid} wrong "{wid}" exists', 'no such wrong id')
    v = ws[0]
    tt = t if t is not None else max(v.get('tol', {}).get('abs', 1e-9), 1e-9)
    ok = near(v['value'], value, tt)
    ex._rec(ok, f'{iid} wrong "{wid}" {v["value"]!r} = {value:.6g}', '' if ok else 'recomputed slip differs')
    if typed is not None:
        ok2 = abs(typed - v['value']) <= v.get('tol', {}).get('abs', 1e-9) + 1e-9
        ex._rec(ok2, f'{iid} wrong "{wid}" catches a typed {typed!r}', '' if ok2 else 'typed slip misses its own band')


def correct_ids(iid):
    return sorted(o['id'] for o in IT[iid]['widget']['options'] if o.get('correct'))


R4 = lambda v: round(v, 4)  # noqa: E731

# ---------------------------------------------------------------- metadata, shape, coverage
ex.claim(doc['minutes'] == 45 and doc['pass'] == 0.7, 'minutes 45 and pass 0.7 as stored')
hours = 60  # docs/curriculum.md row 2.2; learn.js examMinutes(60) = 45
ex.claim((45 if hours <= 60 else 60 if hours <= 150 else 90) == doc['minutes'], 'minutes follow learn.js examMinutes(60 h)')
ex.claim(20 <= len(doc['items']) <= 30, f'{len(doc["items"])} items, inside 20 to 30')
ramp = {d: sum(1 for it in doc['items'] if it['difficulty'] == d) for d in (2, 3, 4, 5)}
ex.claim(ramp == {2: 4, 3: 11, 4: 5, 5: 2}, f'ramp {ramp} (18%, 50%, 23%, 9% against 20, 50, 20, 10)')
union = {}
for c in ('arma', 'garch', 'coint'):
    with open(os.path.join(COURSES, c, 'course.json'), encoding='utf8') as f:
        union.update(json.load(f)['skills'])
ex.claim(doc['skills'] == union, 'skills map equals the union of the three course.json maps')
used = {s for it in doc['items'] for s in it['skills']}
ex.claim(used == set(union), 'every skill is tested by at least one item')
rub = sum(r['points'] for r in IT['e-returns-note']['rubric'])
ex.claim(rub == 10, f'longform rubric sums to {rub}')

# ---------------------------------------------------------------- e-adf-read
p_close = mackinnonp(-1.4365, regression='c', N=1)
p_ret = mackinnonp(-17.4129, regression='c', N=1)
ex.claim(near(p_close, 0.5647, 5e-4), f'e-adf-read MacKinnon p for -1.4365 = {p_close:.4f}')
ex.claim(abs(p_ret / 4.87e-30 - 1) < 0.02, f'e-adf-read MacKinnon p for -17.4129 = {p_ret:.3g}')
ex.claim(correct_ids('e-adf-read') == ['b'] and p_close > 0.05 > p_ret, 'e-adf-read key: closes keep a unit root, returns reject')
ex.expect('exam', f'{P("e-adf-read")}.widget.options[0].text', 0.56)
ex.expect('exam', f'{P("e-adf-read")}.explain.text', 0.56)

# ---------------------------------------------------------------- e-garch-step
v1 = 0.02 + 0.07 * 2.4 ** 2 + 0.91 * 1.6
ex.claim(near(v1, 1.8792, 1e-12), f'e-garch-step variance {v1}')
key('e-garch-step', math.sqrt(v1) / 100)
inband('e-garch-step', 0.0137, label='typed 1.37%')
wrong('e-garch-step', 'variance', v1 / 100, typed=0.0188)
wrong('e-garch-step', 'abs', math.sqrt(0.02 + 0.07 * 2.4 + 0.91 * 1.6) / 100, typed=0.0128)
wrong('e-garch-step', 'sigma', math.sqrt(0.02 + 0.07 * 5.76 + 0.91 * math.sqrt(1.6)) / 100, typed=0.0125)
ex.expect('exam', f'{P("e-garch-step")}.explain.text', 0.4032)
ex.expect('exam', f'{P("e-garch-step")}.explain.text', 1.456)
ex.expect('exam', f'{P("e-garch-step")}.feedback.byKey.variance', 1.88)
# byKey "sigma" tells the learner to "square the 1.6 as given"; the right term is 0.91 x 1.6, unsquared
ex.claim_text('exam', f'{P("e-garch-step")}.feedback.byKey.sigma', 'square the 1.6 as given',
              near(0.91 * 1.6 ** 2, 0.91 * 1.6, 1e-9), 'e-garch-step byKey sigma: "square the 1.6" matches the recursion')

# ---------------------------------------------------------------- e-spurious-fit (from the shipped series)
A = np.array(IT['e-spurious-fit']['canvas']['params']['series'][0]['values'])
B = np.array(IT['e-spurious-fit']['canvas']['params']['series'][1]['values'])
f = sm.OLS(B, sm.add_constant(A)).fit()
res = f.resid
r1 = np.corrcoef(res[1:], res[:-1])[0, 1]
fd = sm.OLS(np.diff(B), sm.add_constant(np.diff(A))).fit()
ex.claim(len(A) == len(B) == 500, 'e-spurious-fit 500 days')
ex.claim(near(f.params[1], -0.38, 0.005), f'e-spurious-fit slope {f.params[1]:.4f} reads -0.38')
ex.claim(near(f.rsquared, 0.67, 0.005), f'e-spurious-fit R2 {f.rsquared:.4f} reads 0.67')
ex.claim(near(f.tvalues[1], -32, 0.5), f'e-spurious-fit t {f.tvalues[1]:.2f} reads -32')
ex.claim(near(r1, 0.95, 0.005), f'e-spurious-fit residual lag-1 correlation {r1:.4f} reads 0.95')
ex.claim(near(fd.rsquared, 0.0008, 0.00005), f'e-spurious-fit changes R2 {fd.rsquared:.5f} reads 0.0008')
ex.claim(correct_ids('e-spurious-fit') == ['c'], 'e-spurious-fit key: nothing yet, test the residual')

# ---------------------------------------------------------------- e-band-lags
band400 = 1.96 / math.sqrt(400)
ex.claim(near(band400, 0.098, 5e-4), f'e-band-lags band {band400:.4f}')
vals = IT['e-band-lags']['canvas']['state']['values']
out = sorted(int(k) for k, v in vals.items() if abs(v) > band400)
ex.claim(['x' + str(k) for k in out] == IT['e-band-lags']['widget']['answer'], f'e-band-lags answer = lags {out}')
ex.claim(near(vals['1'], 0.52, 0.005) and near(vals['2'], 0.24, 0.005) and near(vals['9'], 0.125, 0.0005), 'e-band-lags explain 0.52, 0.24, 0.125')

# ---------------------------------------------------------------- e-ar1-table
phi = -0.7
cells = IT['e-ar1-table']['widget']['rows']
for r, want in [(0, phi), (1, phi ** 2), (2, phi ** 3), (3, 4 / (1 - phi ** 2)), (4, 0.0)]:
    a = cells[r][1]['answer']
    ex.claim(near(a, want, 1e-4), f'e-ar1-table row {r} answer {a} = {want:.6g}')
    typed = round(want, 2)
    ex.claim(abs(typed - a) <= cells[r][1]['tol']['abs'] + 1e-9, f'e-ar1-table row {r} typed {typed} at 2 places graded right')
ex.expect('exam', f'{P("e-ar1-table")}.explain.text', 7.84)

# ---------------------------------------------------------------- e-clusters-multi (Ljung-Box from the shown bars)
band1500 = 1.96 / math.sqrt(1500)
ex.claim(near(band1500, 0.0506, 5e-5), f'e-clusters-multi band {band1500:.4f}')
g = IT['e-clusters-multi']['canvas']['state']['values']
n = 1500
Q = n * (n + 2) * sum(g['r'][str(k)] ** 2 / (n - k) for k in range(1, 11))
Qs = n * (n + 2) * sum(g['sq'][str(k)] ** 2 / (n - k) for k in range(1, 11))
ex.claim(near(stats.chi2.sf(Q, 10), 0.31, 0.01), f'e-clusters-multi Ljung-Box p from the r bars {stats.chi2.sf(Q, 10):.3f} reads 0.31')
ex.claim(stats.chi2.sf(Qs, 10) < 1e-4, f'e-clusters-multi Ljung-Box p from the r2 bars {stats.chi2.sf(Qs, 10):.2g} < 0.0001')
ex.claim(max(abs(v) for v in g['r'].values()) < band1500, 'e-clusters-multi every r bar inside the band')
sz = list(g['abs'].values()) + list(g['sq'].values())
ex.claim(round(min(sz), 2) == 0.14 and round(max(sz), 2) == 0.22, f'e-clusters-multi size bars {min(sz)} to {max(sz)} read 0.14 to 0.22')
ex.claim(correct_ids('e-clusters-multi') == ['a', 'c'], 'e-clusters-multi keys a and c')


# ---------------------------------------------------------------- course helpers (as in the courses and this exam's preludes)
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
    u = np.empty(n)
    u[0] = sd_u * z[0, 1]
    for t in range(1, n):
        u[t] = phi * u[t - 1] + sd_u * z[t, 1]
    return x, alpha + beta * x + u


# ---------------------------------------------------------------- e-eg-critical (regenerated)
x6, y6 = make_pair(3, 400, phi=0.96)
r6 = sm.OLS(y6, sm.add_constant(x6)).fit().resid
a6, c6 = adfuller(r6)[:2], coint(y6, x6)
ex.claim((R4(a6[0]), R4(a6[1])) == (-3.1241, 0.0248), f'e-eg-critical adfuller(res) {R4(a6[0])}, {R4(a6[1])}')
ex.claim((R4(c6[0]), R4(c6[1])) == (-3.1282, 0.0828), f'e-eg-critical coint {R4(c6[0])}, {R4(c6[1])}')
ex.claim([R4(v) for v in c6[2]] == [-3.9241, -3.3515, -3.0551], f'e-eg-critical critical values {[R4(v) for v in c6[2]]}')
ex.claim(correct_ids('e-eg-critical') == ['d'] and c6[2][1] < c6[0] and c6[0] < c6[2][2], 'e-eg-critical key: no rejection at 5%, rejects only at 10%')

# ---------------------------------------------------------------- e-ma-identify (regenerated)
x7 = make_arma([], [-0.7], 500, 63)
ac7 = acf(x7, nlags=10, fft=False)
pa7 = pacf(x7, nlags=10, method='ywm')
L = IT['e-ma-identify']['canvas']['left']['state']['values']
Rr = IT['e-ma-identify']['canvas']['right']['state']['values']
ex.claim(all(near(L[str(k)], ac7[k], 6e-5) for k in range(1, 11)), 'e-ma-identify ACF bars reproduce')
ex.claim(all(near(Rr[str(k)], pa7[k], 6e-5) for k in range(1, 11)), 'e-ma-identify PACF bars reproduce (Yule-Walker)')
b500 = 1.96 / math.sqrt(500)
ex.claim(near(b500, 0.0877, 5e-5), f'e-ma-identify band {b500:.4f}')
ex.claim(abs(ac7[1]) > b500 and all(abs(ac7[k]) < b500 for k in range(2, 11)), 'e-ma-identify ACF stops after lag 1')
ex.claim(all(pa7[k] < 0 for k in range(1, 11)), 'e-ma-identify PACF keeps the sign of the spike')
ex.claim(f'{ac7[1]:.2f}' == '-0.48', f'e-ma-identify explain -0.48 ({ac7[1]:.5f})')
out_p = [k for k in range(1, 11) if abs(pa7[k]) > b500]
ex.claim(out_p == [1, 2, 3, 4], f'e-ma-identify option b text: PACF bars outside the band at lags {out_p}')
# option b's why rules out an AR(4) by "a PACF that stops after lag 4", which the shown PACF also does
ex.claim_text('exam', f'{P("e-ma-identify")}.widget.options[1].why', 'would have a PACF that stops after lag 4',
              out_p != [1, 2, 3, 4], 'e-ma-identify why (AR(4)) names a property that separates AR(4) from this plot')

# ---------------------------------------------------------------- e-breach-days (from the shipped series)
sr = IT['e-breach-days']['canvas']['params']['series']
ret, nv = np.array(sr[0]['values']), np.array(sr[1]['values'])
top8 = sorted(np.argsort(ret)[:8].tolist())
mk = IT['e-breach-days']['canvas']['state']['markers']
ex.claim(top8 == [m['i'] for m in mk], f'e-breach-days markers are the eight largest losses {top8}')
import re as _re  # noqa: E402
rows = [ln for ln in IT['e-breach-days']['prose'].split('\n') if _re.match(r'\| [A-H] \|', ln)]
tab = {}
for ln in rows:
    c = [s.strip() for s in ln.strip('|').split('|')]
    tab[c[0]] = (int(c[1]), float(c[2].replace('−', '-').rstrip('%')), float(c[3].replace('−', '-').rstrip('%')))
ok_tab = all(tab[m['label']][0] == m['i'] + 1 and near(tab[m["label"]][1], 100 * ret[m["i"]], 0.0051)
             and near(tab[m["label"]][2], 100 * nv[m["i"]], 0.0051) for m in mk)
ex.claim(ok_tab, 'e-breach-days table rows match the series (day, return, -VaR)')
br = sorted(m['id'] for m in mk if ret[m['i']] < nv[m['i']])
ex.claim(br == sorted(IT['e-breach-days']['widget']['answer']), f'e-breach-days answer = breaches {br}')
three = sorted(m['id'] for m in mk if m['i'] in np.argsort(ret)[:3])
ex.claim(three == sorted(IT['e-breach-days']['widget']['wrong'][0]['set']), 'e-breach-days wrong "size" = the three largest losses')
exact = [round(100 * (nv[m['i']] - ret[m['i']]), 2) for m in mk if m['id'] in br]
shown = [round(abs(tab[m['label']][1]) - abs(tab[m['label']][2]), 2) for m in mk if m['id'] in br]
print(f'   e-breach-days margins from the series {exact}, from the table {shown}; breaches in all 60 days: {int((ret < nv).sum())}')
ex.claim_text('exam', f'{P("e-breach-days")}.explain.text', 'by 0.22, 0.20 and 0.38 points', shown == [0.22, 0.20, 0.38],
              'e-breach-days explain margins agree with the table the learner reads')

# ---------------------------------------------------------------- e-hedge-flip
b_xy = 0.8073 / 0.8626
key('e-hedge-flip', 1 / b_xy, t=0.002)
wrong('e-hedge-flip', 'same', 0.8626)
wrong('e-hedge-flip', 'inverse', 1 / 0.8626)
wrong('e-hedge-flip', 'uninverted', b_xy)
wrong('e-hedge-flip', 'product', 0.8626 * 0.8073)
ex.expect('exam', f'{P("e-hedge-flip")}.explain.text', 0.936)

# ---------------------------------------------------------------- e-unit-root-steps
ex.claim(IT['e-unit-root-steps']['widget']['answer'] == [f's{i}' for i in range(1, 8)], 'e-unit-root-steps model order s1 to s7')

# ---------------------------------------------------------------- e-vol-ahead
VL = 0.03 / (1 - 0.97)
v11 = VL + 0.97 ** 10 * (2.5 - VL)
key('e-vol-ahead', math.sqrt(v11) / 100, t=2e-5)
inband('e-vol-ahead', 0.0145, label='typed 1.45%')
inband('e-vol-ahead', math.sqrt(v11) / 100, label='exact value')
wrong('e-vol-ahead', 'longrun', math.sqrt(VL) / 100, typed=0.01)
wrong('e-vol-ahead', 'tomorrow', math.sqrt(2.5) / 100, typed=0.0158)
wrong('e-vol-ahead', 'off-by-one', math.sqrt(VL + 0.97 ** 11 * 1.5) / 100, typed=0.0144)
wrong('e-vol-ahead', 'variance', v11 / 100, typed=0.0211)
v_it = 2.5
for _ in range(10):
    v_it = 0.03 + 0.97 * v_it
ex.claim(near(v_it, v11, 1e-12), 'e-vol-ahead closed form = ten steps of the recursion')
ex.expect('exam', f'{P("e-vol-ahead")}.explain.text', 1.106)
ex.expect('exam', f'{P("e-vol-ahead")}.explain.text', 2.106)

# ---------------------------------------------------------------- e-pair-positions
zs = IT['e-pair-positions']['canvas']['params']['series'][0]['values']
pos, out_pos, closed = 0, [], False
for z in zs:
    closed = False
    if pos == -1 and (z <= 0 or z >= 4):
        pos, closed = 0, True
    elif pos == 1 and (z >= 0 or z <= -4):
        pos, closed = 0, True
    if pos == 0 and not closed:
        if 2 <= z < 4:
            pos = -1
        elif -4 < z <= -2:
            pos = 1
    out_pos.append(pos)
rows12 = IT['e-pair-positions']['widget']['rows']
given = []
for r in rows12:
    c = r[2]
    given.append(c['answer'] if isinstance(c, dict) else int(c.replace('−', '-').replace('+', '')))
ex.claim(given == out_pos, f'e-pair-positions every position (given and keyed) {out_pos}')
ex.claim([float(str(r[1]).replace('−', '-')) for r in rows12] == zs, 'e-pair-positions table z equals the chart')
yr = IT['e-pair-positions']['canvas']['params']['y']
hl = IT['e-pair-positions']['canvas']['params']['hlines']
ex.claim(all(yr[0] <= h['y'] <= yr[1] for h in hl), 'e-pair-positions every reference line inside the y range (series.js skips one outside)',
         f'y range {yr}; lines at {[h["y"] for h in hl]}; the labelled stop line at 4 is not drawn')

# ---------------------------------------------------------------- e-aic-bic
lnn, lnn_x = 5.99, math.log(400)
mods = {'AR(1)': (-571.34, 3), 'AR(2)': (-560.97, 4), 'MA(1)': (-554.25, 3), 'MA(2)': (-552.63, 4), 'ARMA(1,1)': (-552.51, 4)}
aic = {m: 2 * k - 2 * l for m, (l, k) in mods.items()}
bic = {m: k * lnn - 2 * l for m, (l, k) in mods.items()}
w13 = IT['e-aic-bic']['widget']['rows']
for r, m in [(2, 'MA(1)'), (4, 'ARMA(1,1)')]:
    for c, d in [(1, aic), (2, bic)]:
        ex.claim(abs(w13[r][c]['answer'] - d[m]) <= w13[r][c]['tol']['abs'], f'e-aic-bic {m} col {c} key {w13[r][c]["answer"]} within tol of hand {d[m]:.2f}')
        ex.claim(near(w13[r][c]['answer'], (2 * mods[m][1] if c == 1 else mods[m][1] * lnn_x) - 2 * mods[m][0], 0.011),
                 f'e-aic-bic {m} col {c} key from exact ln 400')
for r, m in [(0, 'AR(1)'), (1, 'AR(2)'), (3, 'MA(2)')]:
    for c, d in [(1, aic), (2, bic)]:
        g13 = float(w13[r][c])
        ex.claim(near(g13, d[m], 0.015), f'e-aic-bic given {m} col {c} {g13} within rounding of hand {d[m]:.2f}')
        if not near(g13, d[m], 0.005):
            print(f'   note: e-aic-bic given {m} col {c} shows {g13}, the stated recipe gives {d[m]:.2f}')
best = sorted(aic, key=aic.get)
ex.claim(best[0] == 'ARMA(1,1)' and min(bic, key=bic.get) == 'MA(1)', f'e-aic-bic AIC best {best[0]}, BIC best {min(bic, key=bic.get)}')
gap_mA = aic['MA(1)'] - aic['ARMA(1,1)']
gap_run = aic[best[1]] - aic[best[0]]
print(f'   e-aic-bic AIC gap MA(1) - ARMA(1,1) {gap_mA:.2f}; runner-up {best[1]} gap {gap_run:.2f}')
ex.claim_text('exam', f'{P("e-aic-bic")}.explain.text', 'AIC prefers the ARMA(1,1) by only 1.47', near(gap_run, 1.47, 0.011),
              'e-aic-bic explain: AIC prefers the ARMA(1,1) by 1.47 (over every other model)')
ex.claim_text('exam', f'{P("e-aic-bic")}.feedback.correct', 'AIC prefers ARMA(1,1) by 1.47 points', near(gap_run, 1.47, 0.011),
              'e-aic-bic feedback: AIC prefers ARMA(1,1) by 1.47 points (over every other model)')
bic_run = sorted(bic.values())[1] - min(bic.values())
ex.claim(near(1128.98 - 1126.47, 2.51, 1e-9) and near(bic_run, 2.51, 0.011), f'e-aic-bic BIC margin 2.51 over the runner-up ({bic_run:.2f})')

# ---------------------------------------------------------------- e-fan-width
fc = 20 + 0.8 ** 3 * 8
hw = 1.96 * 3 * math.sqrt(1 + 0.64 + 0.4096)
v = 0.0
for _ in range(3):
    v = 0.64 * v + 9
ex.claim(near(1.96 * math.sqrt(v), hw, 1e-12), 'e-fan-width variance by the recursion = closed form')
key('e-fan-width', fc + hw, t=0.005)
wrong('e-fan-width', 'one-step', fc + 1.96 * 3, t=0.005)
wrong('e-fan-width', 'sqrt-h', fc + 1.96 * 3 * math.sqrt(3), t=0.005)
wrong('e-fan-width', 'no-reversion', 28 + hw, t=0.005)
wrong('e-fan-width', 'point', fc, t=0.005)
ex.expect('exam', f'{P("e-fan-width")}.feedback.correct', 24.10)
ex.expect('exam', f'{P("e-fan-width")}.feedback.correct', 8.42)
ex.expect('exam', f'{P("e-fan-width")}.feedback.byKey.one-step', 5.88)

# ---------------------------------------------------------------- e-kupiec
def ll(p, x=10, n=500):
    return x * math.log(p) + (n - x) * math.log(1 - p)


lr = -2 * (ll(0.01) - ll(0.02))
lr2 = -2 * (stats.binom.logpmf(10, 500, 0.01) - stats.binom.logpmf(10, 500, 0.02))
ex.claim(near(lr, lr2, 1e-9), f'e-kupiec LR by the formula = by binom.logpmf ({lr:.4f})')
key('e-kupiec', lr, t=0.005)
zk = (10 - 5) / math.sqrt(500 * 0.01 * 0.99)
wrong('e-kupiec', 'half', lr / 2, t=0.005)
wrong('e-kupiec', 'z-squared', zk ** 2, t=0.005)
wrong('e-kupiec', 'z', zk, t=0.005)
ex.claim(near(stats.chi2.ppf(0.95, 1), 3.841, 5e-4) and lr > stats.chi2.ppf(0.95, 1), 'e-kupiec LR just above chi2(1) 5% point 3.841')
ex.claim(near(ll(0.01), -50.98, 0.005) and near(ll(0.02), -49.02, 0.005), 'e-kupiec explain log-likelihoods -50.98 and -49.02')
ex.expect('exam', f'{P("e-kupiec")}.feedback.byKey.z', 2.22)

# ---------------------------------------------------------------- e-johansen-rank
cv = [c_sjt(3 - i, 0)[1] for i in range(3)]
ex.claim([f'{v:.2f}' for v in cv] == ['29.80', '15.49', '3.84'], f'e-johansen-rank 95% trace values {[round(v, 4) for v in cv]}')
tr = [64.22, 12.91, 4.43]
rank = next((i for i in range(3) if tr[i] < cv[i]), 3)
ex.claim(rank == 1 and correct_ids('e-johansen-rank') == ['b'], 'e-johansen-rank key rank 1 by the sequential rule')
ex.claim(sum(t > c for t, c in zip(tr, cv)) == 2, 'e-johansen-rank option c why: two rows above their values')

# ---------------------------------------------------------------- e-returns-note (regenerated)
x21, y21 = make_pair(14, 750)
f21 = sm.OLS(y21, sm.add_constant(x21)).fit()
res21 = f21.resid
c21 = coint(y21, x21)
a21 = adfuller(res21)
b21 = sm.OLS(np.diff(res21), sm.add_constant(res21[:-1])).fit().params[1]
hl21 = math.log(0.5) / math.log(1 + b21)
rc = np.corrcoef(np.diff(np.log(y21)), np.diff(np.log(x21)))[0, 1]
phi21 = ARIMA(y21, order=(1, 0, 0)).fit().params[1]
tR = math.sqrt(0.9482 * 748 / (1 - 0.9482))
chk = [
    ('ADF p, price y 0.47', round(adfuller(y21)[1], 2) == 0.47),
    ('ADF p, price x 0.46', round(adfuller(x21)[1], 2) == 0.46),
    ('ADF p, changes < 0.0001', max(adfuller(np.diff(y21))[1], adfuller(np.diff(x21))[1]) < 1e-4),
    (f'AR(1) of the price {phi21:.4f} = 0.9906', round(phi21, 4) == 0.9906),
    (f'beta {f21.params[1]:.4f}', round(f21.params[1], 4) == 1.4532),
    (f'R2 {f21.rsquared:.4f}', round(f21.rsquared, 4) == 0.9482),
    (f'slope t {f21.tvalues[1]:.1f} and from R2 {tR:.1f}', round(f21.tvalues[1]) == 117 and round(tR) == 117),
    (f'return correlation {rc:.3f}', round(rc, 2) == 0.88),
    (f'Engle-Granger {c21[0]:.3f}, p {c21[1]:.4f}', round(c21[0], 3) == -3.605 and round(c21[1], 4) == 0.0241),
    ('Engle-Granger values -3.911, -3.344, -3.050', [round(v, 3) for v in c21[2]] == [-3.911, -3.344, -3.050]),
    (f'residual ADF p {a21[1]:.4f}', round(a21[1], 4) == 0.0057),
    (f'ordinary ADF 1% value {a21[4]["1%"]:.3f} about -3.43', round(a21[4]['1%'], 2) == -3.44 or round(a21[4]['1%'], 2) == -3.43),
    (f'half-life {hl21:.2f}', round(hl21, 1) == 19.6),
    ('rejects at 5%, not at 1%', c21[2][1] > c21[0] > c21[2][0]),
]
for lab, ok in chk:
    ex.claim(ok, f'e-returns-note {lab}')


# ---------------------------------------------------------------- code items
def same(got, want, cmp, tol):
    if cmp == 'equal':
        return got == want
    if isinstance(want, list):
        return isinstance(got, (list, tuple)) and len(got) == len(want) and all(same(g, w, cmp, tol) for g, w in zip(got, want))
    if isinstance(want, bool) or isinstance(got, bool):
        return got == want
    if isinstance(want, (int, float)):
        try:
            g = float(got)
        except (TypeError, ValueError):
            return False
        t = tol or {}
        if t.get('rel') is not None:
            return abs(g - want) <= abs(want) * t['rel'] + 1e-12
        return abs(g - want) <= (t.get('abs') or 1e-9) + 1e-9
    return got == want


def run_case(prelude, code, case):
    ns = {}
    try:
        exec(prelude, ns)
        exec(code, ns)
        if case.get('setup'):
            exec(case['setup'], ns)
        got = eval(case['call'], ns)
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"
    want = case['expect']
    if isinstance(want, str):          # expect is a Python literal held as text, as the engine reads it
        want = eval(want, {})
    return same(got, want, case.get('compare', 'equal'), case.get('tol')), got


def code_item(iid, mutants=()):
    w = IT[iid]['widget']
    cases = [('example', c) for c in w['examples']] + [('test', c) for c in w['tests']]
    runs = [run_case(w.get('prelude', ''), w['solution'], c) for _, c in cases]
    sol = [r[0] for r in runs]
    ex.claim(all(sol), f'{iid} solution passes {sum(sol)} of {len(sol)} examples and tests',
             '; '.join(f'case {i}: {r[1]!r}'[:160] for i, r in enumerate(runs) if not r[0]))
    st = [run_case(w.get('prelude', ''), w['starter'], c)[0] for k, c in cases if k == 'test']
    ex.claim(not any(st), f'{iid} starter fails every hidden test ({st.count(False)} of {len(st)})')
    dup = [i for i, t in enumerate(w['tests']) if any(t['call'] == e['call'] and t.get('setup') == e.get('setup') for e in w['examples'])]
    print(f'   {iid}: hidden tests identical to an example: {dup}')
    for name, old, new in mutants:
        assert old in w['solution'], (iid, name)
        bad = w['solution'].replace(old, new)
        fails = [i + 1 for i, (k, c) in enumerate([x for x in cases if x[0] == 'test']) if not run_case(w.get('prelude', ''), bad, c)[0]]
        ex.claim(bool(fails), f'{iid} planted bug "{name}" fails hidden tests {fails}')


code_item('e-code-ar-fan', [
    ('sqrt-k width', 'hw = 1.96 * np.sqrt(sigma2 * sum(terms))', 'hw = 1.96 * np.sqrt(sigma2 * k)'),
    ('no reversion', 'fc = mu + phi ** k * (x[-1] - mu)', 'fc = x[-1]'),
    ('mu = c', 'mu = c / (1 - phi)', 'mu = c'),
])
code_item('e-code-garch-report', [
    ('today for tomorrow', 's2_next = omega + alpha * r[-1] ** 2 + beta * s2_last', 's2_next = s2_last'),
    ('365 days', 'np.sqrt(252 * long_run_var)', 'np.sqrt(365 * long_run_var)'),
    ('VaR in %', 'np.sqrt(s2_next) / 100 * position', 'np.sqrt(s2_next) * position'),
])
code_item('e-code-pair-verdict', [
    ('no I(1) check', 'if min(adfuller(y)[1], adfuller(x)[1]) < alpha:', 'if False:'),
    ('ADF on the residual', 'if coint(y, x)[1] >= alpha:', 'if adfuller(sm.OLS(y, sm.add_constant(x)).fit().resid)[1] >= alpha:'),
    ('alpha ignored in coint', 'if coint(y, x)[1] >= alpha:', 'if coint(y, x)[1] >= 0.05:'),
])
w15 = IT['e-code-ar-fan']['widget']
ex.claim(len(w15['tests']) == 8 and '8 hidden tests' in w15['how'], 'e-code-ar-fan how: 8 hidden tests')
w18 = IT['e-code-garch-report']['widget']
ex.claim(len(w18['tests']) == 9 and '9 hidden tests' in w18['how'], 'e-code-garch-report how: 9 hidden tests')
w20 = IT['e-code-pair-verdict']['widget']
ex.claim(len(w20['tests']) == 9 and '9 hidden tests' in w20['how'], 'e-code-pair-verdict how: 9 hidden tests')

# ---------------------------------------------------------------- wrong values against the answer bands (rule 581)
ex.check_wrongs()
ex.report()
