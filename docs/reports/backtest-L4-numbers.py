"""Backtest level 4 (Honest results): second reader's number checks (review-backtest-3-4.md).

Every graded key, every numeric wrong[] value and the numbers in prose, hints, feedback, tables and
model answers, recomputed from their inputs. Engine figures (the lookback grid, run_study, the five
l14 engines) come from running the lessons' own preludes (NumPy, pandas and SciPy needed).
Lo's standard error is taken for daily data, as l9 teaches: SE = sqrt((1 + SR_d^2 / 2) / (252 T)) * sqrt(252).
Checks that fail because the content is wrong are marked CONTENT and listed as findings.
Run: python3 docs/reports/backtest-L4-numbers.py
"""
import contextlib, io, json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level
from scipy.integrate import quad
from scipy.stats import norm

lv = Level('backtest', 4)
E = lv.expect
R252 = math.sqrt(252)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'backtest')


def within(fid, path, value):
    node = lv.files[fid]
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.isdigit() else node[part]
    a = node.get('answer', node.get('value'))
    t = node.get('tol', {}).get('abs', 1e-9)
    return lv._rec(abs(a - value) <= t + 1e-12, f'{fid} {path} accepts {value!r}', f'key {a} tol {t}')


def eq(fid, path, expected, tol=1e-9):
    """The numeric value at path in file fid equals expected (exact fix, not either-or)."""
    node = lv.files[fid]
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.isdigit() else node[part]
    return lv._rec(abs(node - expected) <= tol, f'{fid} {path} == {expected!r}', f'found {node}')


def se_daily(sr, years):
    srd = sr / R252
    return math.sqrt((1 + srd ** 2 / 2) / (252 * years)) * R252


def emax(n):
    return quad(lambda x: x * n * norm.pdf(x) * norm.cdf(x) ** (n - 1), -12, 12)[0]


def ns(fid, i):
    w = json.load(open(os.path.join(BASE, fid + '.json')))['screens'][i]['widget']
    g = {'__name__': 'x'}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(w['prelude'], g)
        exec(w['solution'], g)
    return g

g = ns('l16-results-note', 8)
BARS, LB = g['BARS'], g['LB']
five = [g['net_sharpe'](BARS, L, 2.5) for L in LB]
res, held = g['split_holdout'](BARS)
rs = [g['net_sharpe'](res, L, 2.5) for L in LB]
hs = [g['net_sharpe'](held, L, 2.5) for L in LB]
mi, mo = g['study_metrics'](res, 2, 2.5), g['study_metrics'](held, 2, 2.5)
bh_in = g['buy_and_hold'](res).pct_change().dropna()
bh_out_e = g['buy_and_hold'](held)
bh_out = bh_out_e.pct_change().dropna()

# ---------- l13 ----------
for L, v in zip(LB, five):
    E('l13', 'screens[0].canvas', round(v, 2))
within('l13-locked-away', 'screens[1].widget', 1260 - 252)
s1 = se_daily(0.55, 1)
within('l13-locked-away', 'screens[3].widget', s1)                       # CONTENT: key 1.07 is the one-yearly-return SE
E('l13', 'screens[3].explain.text', round(norm.cdf(-0.547 / se_daily(0.547, 1)) * 100))   # CONTENT: says "about 30%"; daily SE gives 29%
within('l13-locked-away', 'screens[4].widget', 1260 - 252 - 20)
E('l13', 'screens[4].widget.wrong[1].value', 252 - 20)
E('l13', 'screens[4].widget.wrong[2].value', 1260 - 252 + 20)
for v in rs:
    E('l13', 'screens[5].canvas', round(v, 2))       # CONTENT: lookback 3 research 0.2052 shows 0.20
for v in hs:
    E('l13', 'screens[5].canvas', round(v, 2))       # CONTENT: lookback 40 held out 1.2852 shows 1.28
E('l13', 'screens[5].prose', round(hs[4], 2))
E('l13', 'screens[5].hints[2].text', round(rs[4], 2))
E('l13', 'screens[8].explain.text', round(rs[1], 3))
E('l13', 'screens[8].explain.text', round(hs[1], 3))
E('l13', 'screens[10].widget.options[2].text', round((0.2 + 0.3 + 1.4) / 3, 2))
within('l13-locked-away', 'quiz[0].widget', 1260 - 252 - 10)
within('l13-locked-away', 'quiz[2].widget', se_daily(0.0, 2))
eq('l13-locked-away', 'screens[3].canvas.params.params.sigma', round(se_daily(0.55, 1), 1), 1e-9)
eq('l13-locked-away', 'screens[3].widget.wrong[0].value', round(math.sqrt((1 + 0.55 ** 2 / 2) / 1), 2), 1e-9)   # yearly-return form
eq('l13-locked-away', 'screens[3].widget.wrong[1].value', round(se_daily(0.55, 4), 1), 1e-9)                    # T = 4
E('l13', 'screens[1].prose', '14 November 2022')
E('l13', 'screens[6].canvas', str(held.index[0].date()))

# ---------- l14 ----------
w = json.load(open(os.path.join(BASE, 'l14-too-good.json')))['screens'][9]['widget']
g14 = {'__name__': 'x'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(w['prelude'], g14)
eng = {}
for k, run in g14['ENGINES'].items():
    out = run(g14['BARS'])
    eng[k] = (out['ret'].mean() / out['ret'].std() * R252, out['cost'].sum(),
              [g14['lookahead_check'](run, g14['BARS'], c) for c in (315, 630, 945)])
for k in 'abcde':
    E('l14', 'screens[0].canvas', round(eng[k][0], 2))
E('l14', 'screens[4].canvas', round(eng['e'][1], 2))
E('l14', 'screens[4].canvas', round(eng['b'][1], 2))
lv._rec([eng[k][2] for k in 'abcde'] == [[False] * 3, [True] * 3, [False] * 3, [False] * 3, [True] * 3], 'l14 look-ahead results a to e', '')
sr_p = lambda p: R252 * (2 * p - 1) / math.sqrt(1 - (2 * p - 1) ** 2)
within('l14-too-good', 'screens[1].widget', min(p / 100 for p in range(50, 63) if sr_p(p / 100) > 2))
E('l14', 'screens[1].widget.accept', round(sr_p(0.56), 2))
E('l14', 'screens[1].widget.accept', round(sr_p(0.57), 2))
E('l14', 'screens[1].feedback.byKey.60', round(sr_p(0.60), 2))
E('l14', 'screens[1].explain.text', 0.5 + 0.5 * 2 / math.sqrt(252 + 4))
E('l14', 'screens[2].explain.text', 'nearly seven')
lv._rec(6.5 < eng['b'][0] / eng['e'][0] < 7, 'l14 b is nearly seven times e', f"{eng['b'][0] / eng['e'][0]:.2f}")
within('l14-too-good', 'screens[6].widget', 1 * 0.012 * math.sqrt(2) * 1e4)
E('l14', 'screens[6].widget.wrong[0].value', round(0.012 * 2 * 1e4))
E('l14', 'screens[6].widget.wrong[1].value', round(0.012 * math.sqrt(0.5) * 1e4, 1))
E('l14', 'screens[7].prose', round(0.5 + 2 / R252 / 2, 2))
within('l14-too-good', 'quiz[1].widget', sr_p(0.53))
within('l14-too-good', 'quiz[1].widget.wrong[0]', 252 * 0.06 / math.sqrt(1 - 0.06 ** 2))

# ---------- l15 ----------
w15 = json.load(open(os.path.join(BASE, 'l15-how-many-settings.json')))
data = w15['screens'][0]['canvas']['params']['data']
srt = sorted(data)
E('l15', 'screens[0].question', round(max(data), 2))
E('l15', 'screens[0].explain.text', round((srt[23] + srt[24]) / 2, 2))
p1 = 1 - norm.cdf(0.77 / 0.5)
within('l15-how-many-settings', 'screens[1].widget', 1 - (1 - p1) ** 48)
E('l15', 'screens[1].widget.wrong[0].value', round(p1, 3))
E('l15', 'screens[2].prose', round(emax(10), 3))
within('l15-how-many-settings', 'screens[2].widget', 0.5 * emax(10))
E('l15', 'screens[2].widget.wrong[1].value', round(emax(10) / 0.5, 2))
E('l15', 'screens[3].prose', round(emax(100), 3))
E('l15', 'screens[3].prose', round(math.sqrt(2 * math.log(100)), 2))
within('l15-how-many-settings', 'screens[3].widget', 0.5 * emax(100))
E('l15', 'screens[3].widget.wrong[0].value', round(0.5 * math.sqrt(2 * math.log(100)), 2))
E('l15', 'screens[3].feedback.correct', round((emax(100) / emax(10) - 1) * 100, -1))
within('l15-how-many-settings', 'screens[4].widget', 2.24 * 0.451)
E('l15', 'screens[4].widget.wrong[0].value', round(2.24 * 0.397, 2))
E('l15', 'screens[4].widget.wrong[1].value', round(2.24 * 0.5, 2))
pts = w15['screens'][5]['canvas']['params']['points']
mx = sum(p[0] for p in pts) / len(pts)
my = sum(p[1] for p in pts) / len(pts)
slope = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
E('l15', 'screens[5].explain.text', round(slope, 2))
within('l15-how-many-settings', 'screens[6].widget', 72 + 48)
E('l15', 'screens[6].explain.text', round(emax(120), 2))
E('l15', 'summary.formula.note', round(emax(48), 2))
E('l15', 'summary.formula.note', round(emax(10), 2))
E('l15', 'summary.formula.note', round(emax(100), 2))
within('l15-how-many-settings', 'quiz[1].widget', 0.3 * emax(100))

# ---------- l16 ----------
within('l16-results-note', 'screens[2].widget.rows[0][1]', mi['sharpe'])
within('l16-results-note', 'screens[2].widget.rows[0][2]', mo['sharpe'])
within('l16-results-note', 'screens[2].widget.rows[1][2]', mo['max_drawdown'])
within('l16-results-note', 'screens[2].widget.rows[2][2]', mo['ann_return'])
E('l16', 'screens[2].explain.text', round(-g['cagr'](bh_out_e) * 100))
within('l16-results-note', 'screens[5].widget', se_daily(1.863, 1))   # CONTENT: key 1.65 is the one-yearly-return SE
E('l16', 'screens[5].explain.text', round(1.863 / se_daily(1.863, 1), 1))   # CONTENT: says 1.1
E('l16', 'quiz[2].prose', round(se_daily(1.5, 1), 2))                      # CONTENT: says 1.35
E('l16', 'quiz[2].explain.text', f'= {1.5 / se_daily(1.5, 1):.1f}$ standard errors')
eq('l16-results-note', 'screens[5].canvas.params.params.sigma', round(se_daily(1.863, 1), 3), 1e-9)
eq('l16-results-note', 'screens[5].widget.wrong[0].value', round(math.sqrt(1 + 1.863 ** 2 / 2), 2), 1e-9)   # yearly-return form
eq('l16-results-note', 'screens[5].widget.wrong[1].value', round(se_daily(1.863, 1) / R252, 3), 1e-9)       # per-day error

# ---------- review-4 ----------
within('review-4', 'items[0].widget', 1260 - 252 - 5)
p1 = 0.5 + 0.5 / math.sqrt(253)           # hit rate for an annual Sharpe of exactly 1
within('review-4', 'items[3].widget', p1)
eq('review-4', 'items[3].widget.wrong[0].value', round(0.5 + 0.5 / math.sqrt(252 ** 2 + 1), 3), 1e-9)   # used 252, not its root
eq('review-4', 'items[3].widget.wrong[1].value', round(0.5 + 1 / math.sqrt(253), 4), 1e-9)               # p - 0.5 set to 0.0629
lv._rec(abs(sr_p(p1) - 1) < 1e-9, 'review-4 items[3]: sharpe at p1 is 1', f'{sr_p(p1)}')
within('review-4', 'items[5].widget', 0.4 * 1.539)
E('review', 'items[6].explain.text', round(2.24 * 0.451, 2))
E('review', 'items[6].widget.options[1].text', round(1.42 * 0.345, 2))

# ---------- homework-4 ----------
within('homework-4', 'items[0].widget', se_daily(1.0, 2))
eq('homework-4', 'items[0].widget.wrong[0].value', round(math.sqrt((1 + 1.0 / 2) / 2), 2), 1e-9)   # yearly-return form
eq('homework-4', 'items[0].widget.wrong[1].value', round(se_daily(1.0, 1), 1), 1e-9)               # T = 1
eq('homework-4', 'items[0].widget.wrong[2].value', round(se_daily(1.0, 2) ** 2, 1), 1e-9)
within('homework-4', 'items[1].widget', 1260 - 126 - 60)
E('homework', 'items[1].widget.wrong[1].value', 1260 - 252 - 60)
sr8 = [0.458, 0.547, 0.205, -0.42, -0.331, -0.126, 0.086, 0.048]
mu8 = sum(sr8) / 8
sd8 = math.sqrt(sum((v - mu8) ** 2 for v in sr8) / 7)
E('homework', 'items[2].prose', round(sd8, 3))
within('homework-4', 'items[2].widget', 1.417 * sd8)
E('homework', 'items[2].widget.wrong[0].value', round(1.417 * 0.5, 2))
for v in rs:
    E('homework', 'items[2].prose', round(v, 3))
mod = 'items[7].widget.model'
E('homework', mod, '8.26%')
E('homework', mod, '-8.83%')
E('homework', mod, f"{g['cagr'](g['buy_and_hold'](res)) * 100:.2f}%")
E('homework', mod, f"{g['cagr'](bh_out_e) * 100:.2f}%")
E('homework', mod, f"{bh_in.std() * R252 * 100:.2f}%")
E('homework', mod, f"{bh_out.std() * R252 * 100:.2f}%")
E('homework', mod, f"{g['max_drawdown'](g['buy_and_hold'](res)) * 100:.2f}%")
E('homework', mod, f"{g['max_drawdown'](bh_out_e) * 100:.2f}%")
E('homework', mod, f'about {se_daily(0.547, 1):.2f}')        # CONTENT: says about 1.07
E('homework', 'items[6].explain.text', 1.23)

lv.check_wrongs()
lv.report()
