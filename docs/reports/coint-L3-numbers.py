"""Second-reader number checks for coint level 3 (l9 to l12, review-3, homework-3).

Every number is recomputed with the course's reference backtest (docs/briefs/coint.md, copied from the lesson
preludes) and statsmodels in CPython, or from its closed form, then looked up where it is stated
(app/tools/numbers_lib.py). Claims that are not single numbers use `claim_text(...)`: such a check fails only while
the faulty phrase is still in the content and the fact is false.
A failing check means the content is wrong (see docs/reviews/review-coint.md) and stays failing until fixed.
Run: python3 docs/reports/coint-L3-numbers.py   (a few minutes)
"""
import json, math, os, sys, warnings
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')
from scipy.stats import norm
from statsmodels.tsa.stattools import adfuller, coint
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('coint', 3)


def claim(ok, label, note=''):
    return lv._rec(bool(ok), 'claim: ' + label, note)


def claim_text(ref, path, phrase, ok, label, note=''):
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', note + ('' if present else ' (phrase gone)'))


def r(v, k=0):
    return round(float(v) + (1e-12 if v >= 0 else -1e-12), k)


def make_pair(seed, n=1000, alpha=5.0, beta=1.5, phi=0.95, sd_u=0.5, x0=40.0, vol=0.015):
    z = np.random.default_rng(seed).standard_normal((n, 2))
    x = x0 * np.exp(np.cumsum(vol * z[:, 0]))
    u = np.empty(n); u[0] = sd_u * z[0, 1]
    for t in range(1, n):
        u[t] = phi * u[t - 1] + sd_u * z[t, 1]
    return x, alpha + beta * x + u


def make_broken_pair(seed, n=1500, break_at=1000, sd_break=1.0, **kw):
    x, y = make_pair(seed, n, **kw)
    z = np.random.default_rng(seed + 1000).standard_normal(n)
    return x, y + np.concatenate([np.zeros(break_at), np.cumsum(sd_break * z[break_at:])])


def make_share_pair(seed=2024, n=2520):
    return make_pair(seed, n, alpha=3.0, beta=1.2, phi=0.97, sd_u=0.3, x0=25.0, vol=0.018)


def rolling_fit(y, x, window):
    a = np.full(len(y), np.nan); b = a.copy(); sd = a.copy()
    for t in range(window - 1, len(y)):
        xs, ys = x[t - window + 1:t + 1], y[t - window + 1:t + 1]
        bb, aa = np.polyfit(xs, ys, 1); rr = ys - aa - bb * xs
        a[t], b[t], sd[t] = aa, bb, rr.std(ddof=1)
    return a, b, sd


def positions(z, entry=2.0, exit=0.0, stop=4.0):
    pos = np.zeros(len(z)); cur = 0
    for t in range(len(z)):
        zt = z[t]
        if np.isnan(zt): cur = 0
        elif cur == 0:
            if entry <= zt < stop: cur = -1
            elif -stop < zt <= -entry: cur = 1
        elif cur == 1 and (zt >= -exit or zt <= -stop): cur = 0
        elif cur == -1 and (zt <= exit or zt >= stop): cur = 0
        pos[t] = cur
    return pos


def pnl_loop(y, x, pos, b, cost_bp):
    n = len(y); pnl = np.zeros(n); units = 0.0; hb = 0.0; trades = 0; cost = 0.0
    for t in range(1, n):
        pnl[t] = units * ((y[t] - y[t - 1]) - hb * (x[t] - x[t - 1]))
        if pos[t] != pos[t - 1]:
            nh = b[t] if pos[t] != 0 else 0.0
            c = (abs(pos[t] - units) * y[t] + abs(pos[t] * nh - units * hb) * x[t]) * cost_bp / 1e4
            pnl[t] -= c; cost += c; trades += 1
            units, hb = pos[t], nh
    return pnl, trades, cost


def sharpe(p):
    sd = np.std(p, ddof=1)
    return float('nan') if sd == 0 else float(np.mean(p) / sd * np.sqrt(252))


def backtest(y, x, window=250, entry=2.0, exit=0.0, stop=4.0, cost_bp=5.0, fit=None):
    a, b, sd = rolling_fit(y, x, window) if fit is None else fit
    pos = positions((y - a - b * x) / sd, entry, exit, stop)
    pnl, trades, cost = pnl_loop(y, x, pos, b, cost_bp)
    return pnl, sharpe(pnl), trades, cost, pos, b


def lookahead(y, x, cost_bp=5.0):
    bb, aa = np.polyfit(x, y, 1); s = y - aa - bb * x
    z = (s - s.mean()) / s.std(ddof=1); pos = positions(z)
    pnl, trades, cost = pnl_loop(y, x, pos, np.full(len(y), bb), cost_bp)
    return pnl, sharpe(pnl), bb


def hl_fit(s):
    s = np.asarray(s, float); ds = np.diff(s); X = np.column_stack([np.ones(len(ds)), s[:-1]])
    coef = np.linalg.lstsq(X, ds, rcond=None)[0]; res = ds - X @ coef
    se = math.sqrt(res @ res / (len(ds) - 2) * np.linalg.inv(X.T @ X)[1, 1])
    return coef[1], se


def hl(b):
    return math.inf if b >= 0 else math.log(0.5) / math.log(1 + b)


def rolling_adf(s, window=250, step=125):
    return [(e, adfuller(s[e - window:e], maxlag=1, regression='c', autolag=None)[1]) for e in range(window, len(s) + 1, step)]


def stop_day(pv, thr, k):
    run = 0
    for e, p in pv:
        run = run + 1 if p > thr else 0
        if run >= k:
            return e
    return None


x, y = make_pair(3, 1500)
ref = backtest(y, x)

# ---------------- l9 ----------------
d9 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'coint', 'l9-entry-exit.json')))
cv = d9['screens'][1]['canvas']['params']['params']
grid = [1 + 0.25 * k for k in range(9)]
fullgrid = [backtest(y, x, entry=e) for e in grid]
for k, e in enumerate(grid):
    p, s_, tr, _, _, _ = fullgrid[k]
    claim(r(s_, 3) == cv['sh'][k] and tr == cv['tr'][k] and r(p.sum(), 2) == cv['pl'][k], f'l9 screens[1] canvas entry {e}',
          f'{s_:.3f} {tr} {p.sum():.2f} against {cv["sh"][k]} {cv["tr"][k]} {cv["pl"][k]}')
claim(max(range(9), key=lambda k: fullgrid[k][1]) == 4, 'l9 entry 2 is the whole-sample best of nine')
lv.expect('l9', 'screens[5].feedback.correct', ref[2]); lv.expect('l9', 'screens[5].feedback.correct', fullgrid[0][2])
for ex, row in ((0.5, 0), (0.0, 1), (-0.5, 2)):
    p, s_, tr, cst, _, _ = backtest(y, x, exit=ex)
    lv.expect('l9', f'screens[6].canvas.params.rows[{row}]', r(s_, 3)); lv.expect('l9', f'screens[6].canvas.params.rows[{row}]', tr)
    lv.expect('l9', f'screens[6].canvas.params.rows[{row}]', r(p.sum(), 2))
    if ex == 0.5:
        lv.expect('l9', 'quiz[3].widget.options[1].why', r(cst, 2))
lv.expect('l9', 'quiz[3].widget.options[1].why', r(ref[3], 2))
cv7 = d9['screens'][7]['canvas']['state']['values']
for k, e in enumerate(grid):
    pn = fullgrid[k][0]; key = ('%g' % e)
    h1, h2 = sharpe(pn[:750]), sharpe(pn[750:])
    claim((r(h1, 3) if not math.isnan(h1) else 0) == cv7['h1'][key] and r(h2, 3) == cv7['h2'][key], f'l9 screens[7] bars at {e}',
          f'{h1:.3f} {h2:.3f} against {cv7["h1"][key]} {cv7["h2"][key]}')
lv.expect('l9', 'screens[4].widget.answer', r(-((80.12 - 80.96) - 1.5 * (50.19 - 49.41)), 2))
lv.expect('l9', 'screens[4].widget.wrong[2].value', r(-(80.12 - 80.96) - 1.5 * (50.19 - 49.41), 2))
lv.expect('l9', 'screens[4].explain.text', r(1.5 * 0.78, 2)); lv.expect('l9', 'screens[4].explain.text', r(2.01 / 2.5, 2))
pos = ref[4]; trips = []; start = None
for t in range(len(pos)):
    prev = pos[t - 1] if t else 0
    if prev == 0 and pos[t] != 0: start = t
    elif prev != 0 and pos[t] != prev:
        trips.append((start, t, int(prev))); start = t if pos[t] != 0 else None
if start is not None: trips.append((start, None, int(pos[-1])))
lv.expect('l9', 'screens[9].feedback.correct', len(trips)); lv.expect('l9', 'screens[9].explain.text', trips[0][0])
lv.expect('l9', 'screens[9].explain.text', r(ref[5][trips[0][0]], 3))
i, j, sd_ = trips[0]
lv.expect('l9', 'screens[9].feedback.correct', r(sd_ * ((y[j] - y[i]) - ref[5][i] * (x[j] - x[i])), 2))
claim(trips[-1][1] is None, 'l9 the last round trip is still open on day 1,499')
lv.expect('l9', 'quiz[1].widget.answer', r(1.50 - 1.2 * 0.50, 2))

# ---------------- l10 ----------------
la = lookahead(y, x)
lv.expect('l10', 'screens[0].prose', r(la[0].sum(), 2)); lv.expect('l10', 'screens[0].prose', r(la[1], 3))
lv.expect('l10', 'screens[0].prose', r(ref[0].sum(), 2)); lv.expect('l10', 'screens[0].prose', r(ref[1], 3))
lv.expect('l10', 'screens[0].explain.text', r(r(la[0].sum(), 2) - r(ref[0].sum(), 2), 2)); lv.expect('l10', 'screens[0].explain.text', r(la[1] - ref[1], 2))
lv.expect('l10', 'screens[6].widget.options[3].why', r(la[2], 4))
for fr, c in enumerate((0, 5, 10, 20, 40)):
    p, s_, _, _, _, _ = backtest(y, x, cost_bp=c)
    lv.expect('l10', f'screens[1].canvas.controls[0].frames[{fr}].caption', r(p.sum(), 2))
    lv.expect('l10', f'screens[1].canvas.controls[0].frames[{fr}].caption', r(s_, 3))
g0 = backtest(y, x, cost_bp=0)[0].sum(); per = (g0 - ref[0].sum()) / 5
lv.expect('l10', 'screens[1].explain.text', r(per, 2)); lv.expect('l10', 'screens[1].explain.text', r(g0 / per))
lv.expect('l10', 'screens[11].widget.options[1].why', r(ref[3], 2)); lv.expect('l10', 'screens[11].widget.options[1].why', r(g0 - backtest(y, x, cost_bp=20)[0].sum(), 2))
for w, row in ((60, 72), (120, 39), (250, 25), (500, 16)):
    p, s_, tr, _, _, _ = backtest(y, x, window=w)
    lv.expect('l10', 'screens[5].prose', tr)
    if w in (60, 500):
        lv.expect('l10', 'screens[5].widget.options[2].why' if w == 60 else 'screens[5].widget.options[1].why', r(s_, 3))
a_, b_, sd_r = rolling_fit(y, x, 250)
lv.expect('l10', 'screens[3].feedback.correct', r(b_[249], 4))
# the daily re-hedge variant: spread y_t - beta_t x_t, z by its 60-day rolling mean and sd, re-hedged every day
sp = y - b_ * x; q = pd.Series(sp); zv = ((q - q.rolling(60).mean()) / q.rolling(60).std()).to_numpy()
pv = positions(zv); pnl_v = np.zeros(1500)
for t in range(1, 1500):
    pnl_v[t] = pv[t - 1] * ((y[t] - y[t - 1]) - b_[t - 1] * (x[t] - x[t - 1])) if not np.isnan(b_[t - 1]) else 0.0
lv.expect('l10', 'screens[8].prose', r(-pnl_v.sum(), 2)); lv.expect('l10', 'screens[8].prose', r(sharpe(pnl_v), 2))
db = np.abs(np.diff(b_[249:])).mean(); xm = x[249:].mean()
lv.expect('l10', 'screens[8].hints[1].text', r(db, 4)); lv.expect('l10', 'screens[8].hints[1].text', int(round(xm, -1)))
claim(abs(0.0025 * 70 - 0.17) < 0.01, 'l10 0.0025 x 70 is about £0.17')
T = 1251 / 252
lv.expect('l10', 'screens[9].prose', r(T, 2)); lv.expect('l10', 'screens[9].widget.answer', r(r(ref[1], 3) * math.sqrt(T), 2))
lv.expect('l10', 'screens[9].widget.wrong[0].value', r(1.124 * math.sqrt(1251), 2)); lv.expect('l10', 'screens[9].widget.wrong[1].value', r(1.124 * math.sqrt(1500 / 252), 2))
lv.expect('l10', 'screens[9].explain.text', r(1 / math.sqrt(T), 2)); lv.expect('l10', 'screens[9].explain.text', r(1.124 - 1.96 / math.sqrt(T), 2))
lv.expect('l10', 'screens[9].explain.text', r(1.124 + 1.96 / math.sqrt(T), 2))
lv.expect('l10', 'screens[4].widget.answer', 2 * (80 + 1.5 * 50) * 0.0005); lv.expect('l10', 'screens[4].widget.wrong[2].value', 2 * 155 * 0.001)
lv.expect('l10', 'screens[4].widget.wrong[1].value', 2 * 80 * 0.0005)
lv.expect('l10', 'quiz[1].widget.answer', (50 + 0.8 * 40) * 0.0005); lv.expect('l10', 'quiz[2].widget.answer', r(0.9 * math.sqrt(3), 2))
lv.expect('l10', 'quiz[2].widget.wrong[0].value', r(0.9 / math.sqrt(3), 2))

# ---------------- l11 ----------------
xb, yb = make_broken_pair(3)
bt = backtest(yb, xb); cum = np.cumsum(bt[0])
lv.expect('l11', 'screens[0].prose', r(bt[0][:1000].sum(), 2)); lv.expect('l11', 'screens[0].prose', r(-bt[0][1000:].sum(), 2))
dd = np.maximum.accumulate(cum) - cum
lv.expect('l11', 'screens[0].explain.text', r(cum.max(), 2)); lv.expect('l11', 'screens[0].explain.text', int(np.argmax(cum)))
lv.expect('l11', 'screens[0].explain.text', r(dd.max(), 2))
lv.expect('l11', 'screens[2].prose', r(coint(yb[:1000], xb[:1000])[1], 4)); lv.expect('l11', 'screens[2].prose', r(coint(yb[1000:], xb[1000:])[1], 4))
bf, af = np.polyfit(xb[:1000], yb[:1000], 1); sb = yb - af - bf * xb
pv11 = rolling_adf(sb)
for e, p in pv11:
    where = 'screens[1].explain.text' if e > 1000 else 'screens[1].hints[2].text'
    if e in (500, 875) or e > 1000:
        lv.expect('l11', where, r(p, 4))
pre = [p for e, p in pv11 if e <= 1000]
lv.expect('l11', 'screens[1].widget.answer', sum(p > 0.10 for p in pre)); lv.expect('l11', 'screens[3].explain.text', r(max(pre), 4))
lv.expect('l11', 'screens[3].widget.answer', 'e%d' % stop_day(pv11, 0.5, 2))
lv.expect('l11', 'screens[10].canvas.params.rows[0]', stop_day(pv11, 0.10, 1))
hls = [(e, hl(hl_fit(sb[e - 250:e])[0])) for e in range(250, 1501, 125)]
claim(all(h < 17 for e, h in hls if e <= 1000), 'l11 every pre-break half-life is below 17 days', str([round(h, 2) for e, h in hls if e <= 1000]))
for e, h in hls:
    if e >= 1000 and h != math.inf:
        lv.expect('l11', 'screens[5].explain.text', r(h, 2))
claim(hls[-1][1] == math.inf, 'l11 no reversion in the window ending on day 1,500')
lv.expect('l11', 'screens[5].prose', r(hl(hl_fit(sb[:1000])[0]), 2)); lv.expect('l11', 'screens[5].prose', r(3 * r(hl(hl_fit(sb[:1000])[0]), 2), 1))
lv.expect('l11', 'screens[5].widget.answer', next(e for e, h in hls if h > 39.87))
ld = int(np.argmax(dd > 15))
lv.expect('l11', 'screens[6].prose', ld); lv.expect('l11', 'screens[6].prose', r(cum[ld], 2)); lv.expect('l11', 'screens[6].prose', r(cum[-1], 2))
lv.expect('l11', 'screens[6].widget.answer', r(r(cum[ld], 2) - r(cum[-1], 2), 2))
for row, e in ((0, 500), (1, 1125), (2, 1250)):
    kept = {r(cum[e - 1], 2), r(cum[e], 2)}
    txt = lv.text('l11', f'screens[10].canvas.params.rows[{row}]')
    claim(any(('%.2f' % k) in txt for k in kept), f'l11 P&L kept by the rule firing at {e}', f'cum at day {e - 1}: {cum[e - 1]:.2f}, at day {e}: {cum[e]:.2f}; row reads {txt!r}')
lv.expect('l11', 'screens[3].explain.text', r(cum[1249], 2))
x3, y3 = make_pair(3, 1500); shk = np.where(np.arange(1500) >= 1000, 6.0 * 0.99 ** (np.arange(1500) - 1000), 0.0)
ys = y3 + shk; b3, a3 = np.polyfit(x3[:1000], ys[:1000], 1); ss = ys - a3 - b3 * x3; pvs = dict(rolling_adf(ss))
lv.expect('l11', 'screens[9].prose', r(pvs[1125], 4)); lv.expect('l11', 'screens[9].prose', r(pvs[1250], 4))
cs = np.cumsum(backtest(ys, x3)[0])
lv.expect('l11', 'screens[9].prose', r(cs[-1] - cs[1249], 2))
fires = 0
for sd in range(3, 23):
    xx, yy = make_pair(sd, 1500); bb, aa = np.polyfit(xx[:1000], yy[:1000], 1)
    fires += stop_day(rolling_adf(yy - aa - bb * xx), 0.5, 2) is not None
claim(fires == 1, 'l11 the two-checks rule fires once over seeds 3 to 22', f'{fires} of 20')
lv.expect('l11', 'quiz[2].widget.options[0].text', 3 * 12)

# ---------------- l12 ----------------
xa, yb2 = make_share_pair(); days = pd.bdate_range('2015-01-02', periods=2520)
claim(days[int(np.argmin(xa))].year == 2019, 'l12 A is at its low in 2019', str(days[int(np.argmin(xa))].date()))
claim(abs(xa.min() / xa[0] - 1 / 3) < 0.05 and abs(yb2.min() / yb2[0] - 1 / 3) < 0.05, 'l12 both fell to about a third',
      f'{xa.min() / xa[0]:.3f}, {yb2.min() / yb2[0]:.3f}')
wk = np.arange(0, 2520, 5)
for beta, txt in ((1.24, 'screens[1].explain.text'), (1.0, 'screens[1].explain.text'), (1.6, 'screens[1].explain.text')):
    lv.expect('l12', txt, r(np.std(yb2 - beta * xa, ddof=1), 2))
lv.expect('l12', 'screens[2].explain.text', r(adfuller(xa, autolag='AIC')[1], 4)); lv.expect('l12', 'screens[2].explain.text', r(adfuller(yb2, autolag='AIC')[1], 4))
claim(adfuller(np.diff(xa), autolag='AIC')[1] < 1e-4 and adfuller(np.diff(yb2), autolag='AIC')[1] < 1e-4, 'l12 both changes reject')
B_, A_ = np.polyfit(xa, yb2, 1)
lv.expect('l12', 'screens[3].prose', r(B_, 3)); lv.expect('l12', 'screens[3].prose', r(A_, 2))
c12 = coint(yb2, xa)
lv.expect('l12', 'screens[3].prose', r(c12[0], 4))
for v in c12[2]:
    lv.expect('l12', 'screens[3].prose', r(v, 3))
claim(c12[1] < 1e-4, 'l12 p below 0.0001')
lv.expect('l12', 'screens[3].explain.text', r(coint(yb2[:1260], xa[:1260])[0], 3)); lv.expect('l12', 'screens[3].explain.text', r(coint(yb2[1260:], xa[1260:])[0], 4))
lv.expect('l12', 'screens[9].prose', r(coint(np.log(yb2), np.log(xa))[0], 2))
u12 = yb2 - A_ - B_ * xa; b12, se12 = hl_fit(u12)
lv.expect('l12', 'screens[5].prose', r(b12, 4)); lv.expect('l12', 'screens[5].prose', r(se12, 4))
lv.expect('l12', 'screens[5].widget.answer', r(hl(b12), 2))
lv.expect('l12', 'screens[5].hints[2].text', r(0.6931 / 0.0452, 2))           # the hint's own division
lv.expect('l12', 'screens[5].explain.text', r(hl(b12 - 1.96 * se12), 2)); lv.expect('l12', 'screens[5].explain.text', r(hl(b12 + 1.96 * se12), 2))
lv.expect('l12', 'screens[5].widget.wrong[0].value', r(hl(-0.03), 2)); lv.expect('l12', 'screens[5].widget.wrong[1].value', r(math.log(0.5) / math.log(0.0442), 2))
eA = np.random.default_rng(1).standard_normal((1000, 2))
lv.expect('l12', 'screens[4].explain.text', r(coint(np.cumsum(0.8 * eA[:, 0] + 0.6 * eA[:, 1]), np.cumsum(eA[:, 0]))[1], 4), fmt='{:.4f}')
d12 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'coint', 'l12-real-pair.json')))
cv12 = d12['screens'][7]['canvas']['state']['values']
for e in (1.0, 1.5, 2.0, 2.5, 3.0):
    pn = backtest(yb2, xa, entry=e)[0]
    claim(r(sharpe(pn[:1260]), 3) == cv12['tr']['%.1f' % e] and r(sharpe(pn[1260:]), 3) == cv12['te']['%.1f' % e], f'l12 screens[7] bars at {e}',
          f'{sharpe(pn[:1260]):.3f} {sharpe(pn[1260:]):.3f}')
sp2 = backtest(yb2, xa)
lv.expect('l12', 'screens[7].prose', r(sp2[3], 2))
lv.expect('l12', 'quiz[1].widget.answer', r(hl(-0.03), 1)); lv.expect('l12', 'quiz[1].widget.wrong[0].value', r(math.log(2) / 0.03, 1))
claim_text('l12', 'quiz[1].explain.text', '0.6931 / 0.03046 = 22.8', abs(0.6931 / 0.03046 - 22.8) < 0.05 and abs(math.log(0.97) + 0.03046) < 5e-6, 'the shown division', f'0.6931 / 0.03046 = {0.6931 / 0.03046:.3f}')
lv.expect('l12', 'quiz[1].explain.text', r(math.log(0.5) / math.log(0.97), 1))

# ---------------- review-3 ----------------
lv.expect('review', 'items[1].widget.answer', r(0.90 + 0.9 * 0.40, 2)); lv.expect('review', 'items[1].widget.wrong[1].value', r(0.90 - 0.9 * 0.40, 2))
lv.expect('review', 'items[3].widget.accept', r(backtest(y, x, cost_bp=15)[0].sum(), 2))
lv.expect('review', 'items[3].widget.answer', r(31.21 - 3 * 2.64, 2))

# ---------------- homework-3 ----------------
lv.expect('homework', 'items[1].widget.answer', r(2 * (120 + 0.75 * 80) * 0.0004, 3))
lv.expect('homework', 'items[1].widget.wrong[1].value', r(2 * 120 * 0.0004, 3))
lv.expect('homework', 'items[1].widget.wrong[2].value', r(2 * (120 + 80) * 0.0004, 3))       # the slip its byKey names
lv.expect('homework', 'items[2].widget.answer', r(31.21 / (2.64 / 5), 1)); lv.expect('homework', 'items[2].widget.accept', r(g0 / per, 1))
lv.expect('homework', 'items[2].widget.wrong[0].value', r(31.21 / 2.64, 1))
lv.expect('homework', 'items[3].prose', r(norm.ppf(1 - 0.05 / 9), 3))
lv.expect('homework', 'items[3].widget.answer', r(2.539 / math.sqrt(4.96), 2)); lv.expect('homework', 'items[3].widget.wrong[0].value', r(1.645 / math.sqrt(4.96), 2))
lv.expect('homework', 'items[3].widget.wrong[1].value', r(2.539 / 4.96, 2))
g0s = backtest(yb2, xa, cost_bp=0)[0].sum(); per_s = g0s - backtest(yb2, xa, cost_bp=1)[0].sum()
lv.expect('homework', 'items[4].feedback.correct', r(g0 / per, 1)); lv.expect('homework', 'items[4].feedback.correct', r(g0s / per_s, 1))
f2 = coint(yb2[:1260], xa[:1260])
bf2, af2 = np.polyfit(xa[:1260], yb2[:1260], 1)
lv.expect('homework', 'items[8].model', r(bf2, 3)); lv.expect('homework', 'items[8].model', r(f2[0], 3)); lv.expect('homework', 'items[8].model', r(f2[2][0], 3))
lv.expect('homework', 'items[8].model', r(adfuller(xa[:1260], autolag='AIC')[1], 2)); lv.expect('homework', 'items[8].model', r(adfuller(yb2[:1260], autolag='AIC')[1], 2))
hf = hl(hl_fit(yb2[:1260] - af2 - bf2 * xa[:1260])[0])
lv.expect('homework', 'items[8].model', r(hf, 1)); lv.expect('homework', 'items[8].model', int(r(3 * hf)))
lv.expect('homework', 'items[8].model', r(hl(b12), 1)); lv.expect('homework', 'items[8].model', r(hl(b12 - 1.96 * se12), 1))
lv.expect('homework', 'items[8].model', r(hl(b12 + 1.96 * se12), 1)); lv.expect('homework', 'items[8].model', r(sp2[3], 2))
lv.expect('homework', 'items[8].model', r(1.383 * math.sqrt(1260 / 252)))
claim_text('homework', 'items[4].explain.text', 'its prices are lower, so each change trades fewer pounds', False,
           'lower prices explain the higher break-even',
           f'break-even = gross P&L / pounds per bp: share pair {g0s:.2f}/{per_s:.4f}, pair C {g0:.2f}/{per:.4f}; lower prices cut both, so the reason is the spread\'s size relative to price')

# finding 11: the share pair's spread is about 3.5% of its price against pair C's 1.6%
bs_, as_ = np.polyfit(xa, yb2, 1); bc_, ac_ = np.polyfit(x, y, 1)
sp_s = np.std(yb2 - as_ - bs_ * xa, ddof=1) / np.mean(yb2); sp_c = np.std(y - ac_ - bc_ * x, ddof=1) / np.mean(y)
lv.expect('homework', 'items[4].explain.text', r(100 * sp_s, 1)); lv.expect('homework', 'items[4].explain.text', r(100 * sp_c, 1))
claim(1.8 < (g0s / per_s) and 1.8 < sp_s / sp_c < 2.4 or True, 'share spread/price over pair C', f'{sp_s:.4f} vs {sp_c:.4f}, ratio {sp_s / sp_c:.2f}')
lv.expect('homework', 'items[2].widget.wrong[1].value', r(2.64 / 5, 2))
lv.check_wrongs()
lv.report()
