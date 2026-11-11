"""Recompute every number in app/content/courses/regression/problems-<n>.json twice.

Method 1 is exact or closed form (fractions.Fraction, the course's formulas by hand).
Method 2 takes a different route: NumPy fits on the raw data, statsmodels OLS on a
synthetic dataset built to have exactly the problem's stated summary figures (means,
standard deviations, correlation, SSE, S_xx, centred moment matrix), SciPy quantiles,
statsmodels' VIF and Durbin-Watson, and a fixed-seed simulation of overlapping returns.
For each numeric part: both methods agree; the key matches them within its tol; each
`wrong` value matches its named slip and lies outside the key's band; no two wrong bands
overlap; the question states its form. Choice parts: the keyed option. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-regression-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import isclose, sqrt, ceil
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'regression')
fails, checks = [], 0
FORM = re.compile(r'decimal places?|whole number|fraction', re.I)


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    ok(d['id'] == f'problems-{n}' and d['level'] == n and d['course'] == 'regression', f'set {n}: header')
    ok(3 <= len(d['items']) <= 5, f'set {n}: item count')
    ok(any(it['difficulty'] == 5 for it in d['items']), f'set {n}: no difficulty 5')
    for it in d['items']:
        ok(3 <= len(it['parts']) <= 5, f'{it["id"]}: part count')
        ok(3 <= it['difficulty'] <= 5, f'{it["id"]}: difficulty')
    typed = sum(p['widget']['kind'] in ('numeric', 'expression') for it in d['items'] for p in it['parts'])
    total = sum(len(it['parts']) for it in d['items'])
    ok(3 * typed >= 2 * total, f'set {n}: typed parts {typed} of {total}')
    return {it['id']: it for it in d['items']}


def part(items, iid, k):
    return items[iid]['parts'][k - 1]


def num(items, iid, k, exact, alt, slips=None, rel=1e-9, unit=None):
    """exact: method 1; alt: method 2; slips: {wrong id: value the slip gives}."""
    if items is None:
        return
    p = part(items, iid, k)
    w, tag = p['widget'], f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e = float(exact)
    ok(isclose(e, float(alt), rel_tol=rel, abs_tol=1e-9), f'{tag}: methods differ {e} vs {float(alt)}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-12, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    ok(bool(FORM.search(p['question'])), f'{tag}: question states no form')
    if unit is not None:
        ok(w.get('unit') == unit, f'{tag}: unit {w.get("unit")} expected {unit}')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    ok(set(wrongs) == set(p['feedback'].get('byKey', {})), f'{tag}: byKey lines differ from wrong ids')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, 1e-9), f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} reaches the key band')
        ok(abs(float(val) - e) > tol, f'{tag}: slip {wid} equals the answer')
    for a, b in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')
    return w['answer']


def rounded_ok(items, iid, k, value, msg):
    """a value a learner may reach by a rounded route lies in the key's band"""
    if items is None:
        return
    w = part(items, iid, k)['widget']
    ok(abs(float(value) - w['answer']) <= w['tol']['abs'] + 1e-12, f'{iid} p{k}: {msg} ({float(value)}) outside the band')


def pick(items, iid, k, cid):
    if items is None:
        return
    keyed = [o['id'] for o in part(items, iid, k)['widget']['options'] if o.get('correct')]
    ok(keyed == [cid], f'{iid} p{k}: keyed {keyed}, expected {cid}')


def stated(text_value, exact, msg, tol=1e-9):
    ok(abs(float(text_value) - float(exact)) <= tol, f'stated {msg}: {text_value} vs {float(exact)}')


rng = np.random.default_rng(16)


def unit_noise(n, cols):
    """a vector of length n, mean 0, orthogonal to every column given, with sum of squares 1"""
    e = rng.normal(size=n)
    A = np.column_stack([np.ones(n)] + list(cols))
    e = e - A @ np.linalg.lstsq(A, e, rcond=None)[0]
    return e / np.sqrt(e @ e)


def xy_from_stats(n, mx, sx, my, sy, r):
    """data with exactly these means, sample sds (ddof 1) and correlation"""
    z1 = rng.normal(size=n); z1 = (z1 - z1.mean()) / z1.std(ddof=1)
    z2 = unit_noise(n, [z1]) * np.sqrt(n - 1)
    x = mx + sx * z1
    y = my + sy * (r * z1 + np.sqrt(1 - r * r) * z2)
    return x, y


def line_with(n, xs, a, b, sse):
    """y = a + b x + e with e orthogonal to [1, x] and sum e^2 = sse"""
    return a + b * xs + np.sqrt(sse) * unit_noise(n, [xs])


def ols(y, *cols):
    return sm.OLS(y, sm.add_constant(np.column_stack(cols))).fit()


# ======================================================== level 1: fitting a line
I = load(1)
if I:
    # p-gas-demand
    r, sx, sy, mx, my = F(-8, 10), 3, 45, 4, 300
    b = r * sy / sx
    x, y = xy_from_stats(90, mx, sx, my, sy, -0.8)
    fit = ols(y, x)
    num(I, 'p-gas-demand', 1, b, fit.params[1], {'no-sign': -b, 'variances': r * sy ** 2 / sx ** 2, 'no-r': -F(sy, sx)}, rel=1e-9, unit='GWh per °C')
    a = my - b * mx
    num(I, 'p-gas-demand', 2, a, fit.params[0], {'sign': my + b * mx, 'mean': my, 'swapped': mx - b * my}, unit='GWh')
    fc = a + b * (-5)
    num(I, 'p-gas-demand', 3, fc, fit.predict([[1, -5]])[0], {'minus': a - 60, 'carried': (my + b * mx) + (-b) * 5, 'from-mean': my + 60}, unit='GWh')
    ok((my + b * mx) + (-b) * 5 == 312, 'gas: carried forecast is 252 + 60')
    e = 450 - fc
    num(I, 'p-gas-demand', 4, e, 450 - fit.predict([[1, -5]])[0], {'flipped': -e, 'carried': 450 - 312, 'minus': 450 - 288}, unit='GWh')
    left = sy * sqrt(1 - float(r) ** 2)
    resid_sd = np.sqrt(np.sum(fit.resid ** 2) / 89)           # sd of the unexplained part, divisor n - 1 like s_y
    num(I, 'p-gas-demand', 5, e / left, 42 / resid_sd, {'total-sd': F(42, 45), 'no-root': 42 / (45 * 0.36), 'explained': 42 / 36, 'carried': 138 / 27}, rel=1e-9)
    stated(27, left, 'gas leftover sd', 1e-9)
    stated(408, 300 + 12 * 9, 'gas forecast by deviations')

    # p-car-prices
    ages = np.array([1, 2, 3, 4, 5, 9.]); price = np.array([18000, 16600, 15400, 13400, 12400, 6200.])
    xb = F(24, 6)
    sxx = sum((F(int(t)) - xb) ** 2 for t in ages)
    num(I, 'p-car-prices', 1, sxx, np.var(ages) * 6, {'no-centre': sum(int(t) ** 2 for t in ages), 'by-n': sxx / 6, 'n-1': sxx / 5}, unit='years²')
    sxy = sum((F(int(t)) - xb) * int(v) for t, v in zip(ages, price))
    bcar = sxy / sxx
    num(I, 'p-car-prices', 2, bcar, np.polyfit(ages, price, 1)[0], {'no-sign': -bcar, 'carried': sxy / 136, 'sxy-only': sxy}, unit='£')
    stated(-59200, sxy, 'car S_xy')
    price2 = price.copy(); price2[-1] = 8200
    rise = (9 - xb) * 2000 / sxx
    b2 = np.polyfit(ages, price2, 1)[0]
    num(I, 'p-car-prices', 3, rise, b2 - np.polyfit(ages, price, 1)[0], {'no-deviation': F(2000, 40), 'raw-x': F(9 * 2000, 40), 'carried': F(5 * 2000, 136)}, rel=1e-9, unit='£')
    num(I, 'p-car-prices', 4, bcar + rise, b2, {'wrong-way': bcar - rise, 'carried': bcar + 50, 'raw-x': bcar + 450}, unit='£')
    p4 = np.array(price); p4[3] += 2000
    ok(abs(np.polyfit(ages, p4, 1)[0] - np.polyfit(ages, price, 1)[0]) < 1e-9, 'car: a slip on the 4-year-old car leaves the slope')
    ok(abs(250 / 1480 - 1 / 6) < 0.01, 'car: 250 is about a sixth of 1,480')

    # p-smudged-shift
    xs = [10, 12, 14, 16, 18]; known = [F(50, 10), F(66, 10), None, F(74, 10), F(86, 10)]
    A0, B0 = F(12, 10), F(4, 10)
    ybar = A0 + B0 * F(sum(xs), 5)
    num(I, 'p-smudged-shift', 1, ybar, np.mean(xs) * 0.4 + 1.2, {'four-known': sum(k for k in known if k) / 4, 'intercept': A0, 'mean-x': 14}, unit='hours')
    y3 = 5 * ybar - sum(k for k in known if k)
    # method 2: the y3 for which a refit returns intercept 1.2 and slope 0.4
    from scipy.optimize import brentq
    y3b = brentq(lambda t: np.polyfit(xs, [5.0, 6.6, t, 7.4, 8.6], 1)[1] - 1.2, 0, 20)
    num(I, 'p-smudged-shift', 2, y3, y3b, {'carried': 5 * F(69, 10) - F(276, 10), 'on-line': A0 + B0 * 14, 'total': 5 * ybar}, rel=1e-9, unit='hours')
    full = [F(50, 10), F(66, 10), y3, F(74, 10), F(86, 10)]
    bb, aa = np.polyfit(xs, [float(t) for t in full], 1)
    ok(isclose(bb, 0.4, abs_tol=1e-9) and isclose(aa, 1.2, abs_tol=1e-9), 'smudge: refit returns the printed line')
    res = [t - (A0 + B0 * xx) for t, xx in zip(full, xs)]
    num(I, 'p-smudged-shift', 3, res[2], float(y3b) - (1.2 + 0.4 * 14), {'flipped': -res[2], 'carried': F(69, 10) - F(68, 10), 'on-line': 0}, rel=1e-9, unit='hours')
    sse = sum(t * t for t in res)
    yarr = np.array([float(t) for t in full])
    num(I, 'p-smudged-shift', 4, sse, np.sum((yarr - (aa + bb * np.array(xs))) ** 2), {'abs': sum(abs(t) for t in res), 'no-third': sse - res[2] ** 2, 'carried': sse - res[2] ** 2 + F(1, 100)}, rel=1e-9, unit='hours²')
    sst = sum((t - ybar) ** 2 for t in full)
    num(I, 'p-smudged-shift', 5, 1 - sse / sst, ols(yarr, np.array(xs, float)).rsquared, {'flipped': sse / sst, 'carried': 1 - F(48, 100) / sst, 'unsquared': 1 - F(16, 10) / sst}, rel=1e-9)
    ok(sum(res) == 0 and sum(t * xx for t, xx in zip(res, xs)) == 0, 'smudge: both residual facts hold')
    stated(F(64, 10), B0 ** 2 * 40, 'smudge SSR = b^2 S_xx')
    stated(7.04, sst, 'smudge SST')

    # p-stopping-distances
    v = np.array([20, 30, 40, 50, 60.]); dist = np.array([12, 23, 36, 53, 73.])
    Sxx = sum((F(int(t)) - 40) ** 2 for t in v); Sxy = sum((F(int(t)) - 40) * int(d) for t, d in zip(v, dist))
    bs = Sxy / Sxx
    pf = np.polyfit(v, dist, 1)
    num(I, 'p-stopping-distances', 1, bs, pf[0], {'reverse': Sxx / Sxy, 'mixed': (Sxy / 4) / (Sxx / 5), 'through-origin': F(int(v @ dist), int(v @ v))}, unit='m per mph')
    yb = F(int(dist.sum()), 5)
    a_s = yb - bs * 40
    num(I, 'p-stopping-distances', 2, a_s, pf[1], {'sign': yb + bs * 40, 'mean': yb, 'carried': yb - F(int(v @ dist), int(v @ v)) * 40}, rel=1e-9, unit='m')
    e40 = 36 - (a_s + bs * 40)
    num(I, 'p-stopping-distances', 3, e40, dist[2] - np.polyval(pf, 40), {'flipped': -e40, 'carried': 36 - (yb + bs * 40 + bs * 40), 'no-intercept': 36 - bs * 40}, rel=1e-9, unit='m')
    syy = sum((F(int(d)) - yb) ** 2 for d in dist)
    stated(2345.2, syy, 'stopping S_yy')
    r2 = bs ** 2 * Sxx / syy
    num(I, 'p-stopping-distances', 4, r2, ols(dist, v).rsquared, {'unsquared': bs * Sxx / syy, 'root': sqrt(r2), 'flipped': 1 - r2}, rel=1e-9)
    resid = dist - np.polyval(pf, v)
    ok(np.allclose(resid, [3.0, -1.2, -3.4, -1.6, 3.2]), 'stopping residuals as printed')
    ok(list(np.sign(resid)) == [1, -1, -1, -1, 1], 'stopping residual signs')
    stated(85, a_s + bs * 70, 'stopping line at 70 mph')
    stated(34.8, syy - bs ** 2 * Sxx, 'stopping SSE')
    pick(I, 'p-stopping-distances', 5, 'curve')

# ======================================================== level 2: inference
I = load(2)
if I:
    # p-sunny-cones: synthetic 18 days with S_xx = 64 and SSE = 2,304
    xs = rng.normal(size=18); xs = xs - xs.mean(); xs = 6 + xs * 8 / np.sqrt(xs @ xs)
    ys = line_with(18, xs, 40, 2.4, 2304)
    f1 = ols(ys, xs)
    s = sqrt(F(2304, 16))
    num(I, 'p-sunny-cones', 1, s, np.sqrt(f1.scale), {'by-n': sqrt(2304 / 18), 'n-1': sqrt(2304 / 17), 'no-root': F(2304, 16)}, unit='cones')
    se = s / 8
    num(I, 'p-sunny-cones', 2, se, f1.bse[1], {'no-root': F(12, 64), 'variance': F(144, 8), 'carried': sqrt(2304 / 18) / 8}, unit='cones per hour')
    t = 2.4 / se
    num(I, 'p-sunny-cones', 3, t, f1.tvalues[1], {'inverted': se / 2.4, 'carried': 2.4 / (12 / 64), 'carried-n': 2.4 / (sqrt(2304 / 18) / 8)})
    x72 = np.tile(xs, 4)
    y72 = line_with(72, x72, 40, 2.4, 144 * 70)                 # same s on 70 degrees of freedom
    f4 = ols(y72, x72)
    num(I, 'p-sunny-cones', 4, 2 * t, f4.tvalues[1], {'no-root': 4 * t, 'same': t, 'carried': 2 * 2.4 / (12 / 64)}, rel=1e-9)
    stated(2.120, stats.t.ppf(0.975, 16), 'cones t cut-off 16 df', 0.0005)
    stated(0.75, 12 / 16, 'cones new SE')

    # p-freight-summary: synthetic 42 weeks with R^2 = 0.2 and slope 0.85
    xf = rng.normal(size=42); xf = xf - xf.mean()
    sxxf = xf @ xf
    ssr = 0.85 ** 2 * sxxf
    yf = line_with(42, xf, 100, 0.85, ssr * 0.8 / 0.2)
    ff = ols(yf, xf)
    ok(isclose(ff.rsquared, 0.2, rel_tol=1e-9), 'freight synthetic R^2')
    Fv = F(2, 10) / F(8, 10) * 40
    num(I, 'p-freight-summary', 1, Fv, ff.fvalue, {'no-df': F(1, 4), 'by-n': F(1, 4) * 42, 'n-1': F(1, 4) * 41})
    tf = sqrt(Fv)
    num(I, 'p-freight-summary', 2, tf, ff.tvalues[1], {'no-root': 10, 'half': 5, 'carried': sqrt(10.5), 'carried-df': sqrt(0.25)})
    num(I, 'p-freight-summary', 3, 0.85 / 3.16, 0.85 / round(ff.tvalues[1], 2), {'times': 0.85 * 3.16, 'inverted': 3.16 / 0.85, 'carried-f': 0.085, 'carried': 0.85 / sqrt(10.5)})
    rounded_ok(I, 'p-freight-summary', 3, ff.bse[1], 'the unrounded SE')
    tc = 2.021
    stated(tc, stats.t.ppf(0.975, 40), 'freight t cut-off 40 df', 0.0005)
    lo = 0.85 - tc * 0.269
    num(I, 'p-freight-summary', 4, lo, 0.85 - stats.t.ppf(0.975, 40) * 0.269, {'normal': 0.85 - 1.96 * 0.269, 'upper': 0.85 + tc * 0.269, 'no-crit': 0.85 - 0.269, 'carried': 0.85 - tc * 0.085}, rel=1e-4)
    rounded_ok(I, 'p-freight-summary', 4, ff.conf_int()[1][0], 'statsmodels lower end from the exact SE')
    rounded_ok(I, 'p-freight-summary', 4, 0.31, 'the 2-place rounding')
    stated(1.39, ff.conf_int()[1][1], 'freight upper end', 0.005)

    # p-raw-intercept: synthetic 100 months; excess market mean exactly 0
    rf = 0.25
    xm = rng.normal(size=100); xm = xm - xm.mean(); xm = xm * 4 / xm.std(ddof=1)  # market excess, mean 0
    alpha_true = 0.35
    ye = line_with(100, xm, alpha_true, 0.6, 2.5 ** 2 * 98)                      # fund excess, s = 2.5
    raw = ols(ye + rf, xm + rf)
    ok(isclose(raw.params[0], 0.45, abs_tol=1e-9) and isclose(raw.params[1], 0.6, abs_tol=1e-9), 'raw fit gives 0.45 and 0.6')
    exc = ols(ye, xm)
    al = F(45, 100) - (1 - F(6, 10)) * F(25, 100)
    num(I, 'p-raw-intercept', 1, al / 100, exc.params[0] / 100, {'raw': F(45, 10000), 'beta': (F(45, 100) - F(6, 10) * F(25, 100)) / 100, 'sign': (F(45, 100) + F(4, 10) * F(25, 100)) / 100, 'decimal': F(35, 10000) / 100}, unit='%')
    sea = F(25, 10) / 10
    num(I, 'p-raw-intercept', 2, sea / 100, exc.bse[0] / 100, {'by-n': F(25, 10) / 100 / 100, 'variance': F(625, 100) / 100 / 100, 'decimal': sea / 10000}, unit='%')
    ta = al / sea
    num(I, 'p-raw-intercept', 3, ta, exc.tvalues[0], {'raw': F(45, 100) / sea, 'beta': F(30, 100) / sea, 'carried-n': al / F(25, 1000), 'inverted': sea / al})
    need = lambda t0: ceil(100 * (2 / t0) ** 2 - 1e-12)
    nb = next(n for n in range(100, 1000) if float(al) * sqrt(n) / 2.5 >= 2)
    num(I, 'p-raw-intercept', 4, need(float(ta)), nb, {'raw': need(1.8), 'linear': ceil(100 * 2 / 1.4), 'beta': need(1.2), 'round-down': need(1.4) - 1}, unit='months')
    ok(1.4 * sqrt(2.04) < 2 <= 1.4 * sqrt(2.05), 'alpha: 204 months fall short, 205 reach 2')
    stated(17, 205 / 12, 'alpha years', 0.1)
    stated(4.2, 12 * float(al), 'alpha a year')

    # p-grocer-beta: synthetic 50 months, market sd 5, SSE 588
    xg = rng.normal(size=50); xg = (xg - xg.mean()) / xg.std(ddof=1) * 5 + 0.5
    yg = line_with(50, xg, 0.1, 0.74, 588)
    fg = ols(yg, xg)
    sg = sqrt(F(588, 48))
    num(I, 'p-grocer-beta', 1, sg / 100, np.sqrt(fg.scale) / 100, {'by-n': sqrt(588 / 50) / 100, 'n-1': sqrt(588 / 49) / 100, 'no-root': F(1225, 10000), 'decimal': 0.035 / 100}, unit='%')
    seb = sg / sqrt(49 * 25)
    num(I, 'p-grocer-beta', 2, seb, fg.bse[1], {'no-n': sg / 5, 'variance': sg / sqrt(49 * 5), 'no-root': F(1225, 100) / 1225})
    tb = (0.74 - 1) / seb
    num(I, 'p-grocer-beta', 3, tb, (fg.params[1] - 1) / fg.bse[1], {'zero': 0.74 / seb, 'sign': -tb, 'carried': -0.26 / 0.7, 'variance': -0.26 / (3.5 / sqrt(245))})
    tc48 = 2.011
    stated(tc48, stats.t.ppf(0.975, 48), 'grocer t cut-off 48 df', 0.0005)
    num(I, 'p-grocer-beta', 4, 0.74 + tc48 * seb, fg.conf_int()[1][1], {'normal': 0.74 + 1.96 * 0.1, 'lower': 0.74 - tc48 * 0.1, 'carried': 0.74 + tc48 * 0.7}, rel=1e-4)
    stated(0.539, fg.conf_int()[1][0], 'grocer lower end', 0.0006)
    stated(0.201, tc48 * 0.1, 'grocer half-width', 0.0005)
    pick(I, 'p-grocer-beta', 5, 'below')

# ======================================================== level 3: many variables
I = load(3)
if I:
    # p-power-price: synthetic 200 days with sd 10 and 5, r = 0.6, long slopes 1.5 and 0.8
    g, c = xy_from_stats(200, 50, 10, 30, 5, 0.6)
    pw = 5 + 1.5 * g + 0.8 * c + 3 * unit_noise(200, [g, c]) * np.sqrt(199)
    long_ = ols(pw, g, c); short = ols(pw, g)
    ok(isclose(long_.params[1], 1.5, abs_tol=1e-9) and isclose(long_.params[2], 0.8, abs_tol=1e-9), 'power: long slopes')
    ok(isclose(short.params[1], 1.74, abs_tol=1e-9), 'power: short slope 1.74')
    d = (F(174, 100) - F(15, 10)) / F(8, 10)
    num(I, 'p-power-price', 1, d, ols(c, g).params[1], {'no-divide': F(24, 100), 'sign': -d, 'times': F(24, 100) * F(8, 10)})
    rr = d * 10 / 5
    num(I, 'p-power-price', 2, rr, np.corrcoef(g, c)[0, 1], {'inverted': d * 5 / 10, 'same': d, 'carried': F(24, 100) * 2})
    vif = 1 / (1 - rr ** 2)
    X = sm.add_constant(np.column_stack([g, c]))
    num(I, 'p-power-price', 3, vif, variance_inflation_factor(X, 1), {'no-square': 1 / (1 - rr), 'root': sqrt(vif), 'r2': rr ** 2, 'carried': 1 / (1 - F(48, 100) ** 2)}, rel=1e-9)
    # method 2 for the days: the squared ratio of the gas slope's errors, correlated against uncorrelated, same noise
    c0 = 30 + 5 * unit_noise(200, [g]) * np.sqrt(199)
    pw0 = 5 + 1.5 * g + 0.8 * c0 + 3 * unit_noise(200, [g, c0]) * np.sqrt(199)
    ratio = (long_.bse[1] / ols(pw0, g, c0).bse[1]) ** 2
    num(I, 'p-power-price', 4, ceil(200 * vif), ceil(200 * ratio - 1e-9), {'root': 200 * 1.25, 'no-square': 200 * 2.5, 'carried': ceil(200 * 1.2994), 'round-down': ceil(200 * vif) - 1}, unit='days')
    stated(312.5, 200 * vif, 'power days before rounding')

    # p-solar-output: synthetic 24 days with the stated centred moment matrix
    M = np.array([[40, 24, 88], [24, 30, 45], [88, 45, 250.]])
    Z = rng.normal(size=(24, 3)); Z = Z - Z.mean(0)
    Lz = np.linalg.cholesky(Z.T @ Z); Z = Z @ np.linalg.inv(Lz).T               # Z'Z = I
    D = Z @ np.linalg.cholesky(M).T                                              # D'D = M
    x1, x2, yy = D[:, 0] + 8, D[:, 1] + 20, D[:, 2] + 50
    fs = ols(yy, x1, x2)
    det = 40 * 30 - 24 * 24
    b1 = F(30 * 88 - 24 * 45, det)
    num(I, 'p-solar-output', 1, b1, fs.params[1], {'simple': F(88, 40), 'cramer-sign': F(30 * 88 + 24 * 45, det), 'swapped': F(40 * 45 - 24 * 88, det)}, unit='MWh per hour')
    b2 = (45 - 24 * b1) / 30
    num(I, 'p-solar-output', 2, b2, fs.params[2], {'simple': F(45, 30), 'sign': (45 + 24 * b1) / 30, 'carried': (45 - 24 * F(22, 10)) / 30}, unit='MWh per °C')
    ok(b2 == F(40 * 45 - 24 * 88, det), 'solar: b2 by back-substitution equals Cramer')
    sse_s = 250 - b1 * 88 - b2 * 45
    num(I, 'p-solar-output', 3, sse_s, fs.ssr, {'sign': 250 - b1 * 88 + b2 * 45, 'ess': b1 * 88 + b2 * 45, 'carried': 250 - F(22, 10) * 88 - F(-26, 100) * 45}, unit='MWh²')
    s2 = sse_s / 21
    num(I, 'p-solar-output', 4, s2, fs.scale, {'by-n': sse_s / 24, 'n-2': sse_s / 22, 'n-1': sse_s / 23, 'carried': F(681, 10) / 21}, unit='MWh²')
    adj = 1 - s2 / (F(250) / 23)
    num(I, 'p-solar-output', 5, adj, fs.rsquared_adj, {'plain': 1 - sse_s / 250, 'n': 1 - s2 / (F(250) / 24), 'carried': 1 - (sse_s / 24) / (F(250) / 23), 'carried-n2': 1 - (sse_s / 22) / (F(250) / 23)})
    stated(0.79, fs.rsquared, 'solar plain R^2')
    stated(1.5, ols(yy, x2).params[1], 'solar slope on temperature alone')
    stated(0.23, s2 / (F(250) / 23), 'solar 1 - adj')

    # p-overlap-signal
    s3 = sqrt(F(4500, 500))
    num(I, 'p-overlap-signal', 1, s3 / 100, np.sqrt(4500 / (503 - 3)) / 100, {'by-n': sqrt(4500 / 503) / 100, 'no-root': F(9, 100), 'decimal': F(3, 10000)}, unit='%')
    se3 = sqrt(9 * 0.0004)
    num(I, 'p-overlap-signal', 2, se3, np.sqrt(np.diag(9 * np.diag([0.0004, 0.001, 0.002])))[0], {'no-root-c': 3 * 0.0004, 's2c': 9 * 0.0004, 'carried': 9 * 0.02})
    t3 = 0.21 / se3
    num(I, 'p-overlap-signal', 3, t3, 0.21 / np.sqrt(0.0036), {'carried': 0.21 / 0.18, 'no-root': 0.21 / 0.0036, 'inverted': se3 / 0.21})
    h = 5
    fac = sqrt(1 + 2 * sum((1 - F(j, h)) ** 2 for j in range(1, h)))
    fac2 = np.sqrt(1 + 2 * np.sum(np.square(1 - np.arange(1, h) / h)))
    num(I, 'p-overlap-signal', 4, t3 / fac, 3.5 / fac2, {'no-root': 3.5 / 3.4, 'no-two': 3.5 / sqrt(2.2), 'times': 3.5 * fac, 'carried': (0.21 / 0.18) / fac}, rel=1e-9)
    rounded_ok(I, 'p-overlap-signal', 4, 3.5 / 1.84, 'dividing by the factor rounded to 1.84')
    rounded_ok(I, 'p-overlap-signal', 4, 3.5 / 1.844, 'dividing by 1.844')
    stated(1.2, sum((1 - F(j, h)) ** 2 for j in range(1, h)), 'overlap sum')
    # method 3: simulate the naive t of overlapping 5-day sums with no true effect (fixed seed)
    sim = np.random.default_rng(5)
    ts = []
    for _ in range(1500):
        u, w = sim.normal(size=507), sim.normal(size=507)
        X5 = np.convolve(u, np.ones(5), 'valid')[:503]; Y5 = np.convolve(w, np.ones(5), 'valid')[:503]
        Xc = X5 - X5.mean(); bh = Xc @ Y5 / (Xc @ Xc)
        e5 = Y5 - Y5.mean() - bh * Xc
        ts.append(bh / np.sqrt(e5 @ e5 / 501 / (Xc @ Xc)))
    ok(abs(np.std(ts) - float(fac)) < 0.15, f'overlap: simulated sd of naive t {np.std(ts):.3f} vs factor {float(fac):.3f}')
    stated(1.96, stats.norm.ppf(0.975), 'overlap normal cut-off', 0.001)
    ok(stats.t.ppf(0.975, 500) < 1.97, 't cut-off on 500 df is about 1.96')
    pick(I, 'p-overlap-signal', 5, 'not-sig')

    # p-bond-fund-weeks
    pred = F(5, 100) - F(8, 100) * 10 - F(3, 100) * (-5)
    num(I, 'p-bond-fund-weeks', 1, pred / 100, float(np.dot([0.05, -0.08, -0.03], [1, 10, -5])) / 100,
        {'spread-sign': (F(5, 100) - F(8, 10) - F(15, 100)) / 100, 'no-intercept': (pred - F(5, 100)) / 100, 'all-signs': (F(5, 100) + F(8, 10) - F(15, 100)) / 100, 'decimal': pred / 10000}, unit='%')
    e8 = F(-90, 100) - pred
    num(I, 'p-bond-fund-weeks', 2, e8 / 100, (-0.90 - np.dot([0.05, -0.08, -0.03], [1, 10, -5])) / 100, {'flipped': -e8 / 100, 'carried': 0, 'no-intercept': (F(-90, 100) - (pred - F(5, 100))) / 100}, unit='%')
    e = [F(20, 100), F(30, 100), F(25, 100), F(10, 100), F(-10, 100), F(-20, 100), F(-25, 100)]
    stated(0.315, sum(t * t for t in e), 'bond first seven squares')
    stated(0.0875, sum((e[i] - e[i - 1]) ** 2 for i in range(1, 7)), 'bond first six changes')
    ok(sum(e) + e8 == 0, 'bond: eight residuals add to 0')
    full8 = e + [e8]
    dw = sum((full8[i] - full8[i - 1]) ** 2 for i in range(1, 8)) / sum(t * t for t in full8)
    dwf = lambda x8: (F(875, 10000) + (x8 - e[-1]) ** 2) / (F(315, 1000) + x8 ** 2)
    num(I, 'p-bond-fund-weeks', 3, dw, durbin_watson(np.array([float(t) for t in full8])),
        {'no-week-8': F(875, 10000) / F(315, 1000), 'flipped': dwf(-e8), 'fitted': dwf(F(-60, 100)), 'inverted': 1 / dw})
    rho = 1 - dw / 2
    ar = np.array([float(t) for t in full8])
    num(I, 'p-bond-fund-weeks', 4, rho, 1 - durbin_watson(ar) / 2, {'half': dw / 2, 'no-two': 1 - dw, 'carried': 1 - F(875, 10000) / F(315, 1000) / 2, 'carried-flip': 1 - dwf(-e8) / 2})
    rounded_ok(I, 'p-bond-fund-weeks', 4, 1 - 0.22 / 2, 'the route from d = 0.22')
    stated(0.405, sum(t * t for t in full8), 'bond eight squares')
    pick(I, 'p-bond-fund-weeks', 5, 'hac')

print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
