"""Backtest level 3 (Metrics): second reader's number checks (review-backtest-3-4.md).

Every graded key, every numeric wrong[] value and the numbers in prose, hints, feedback and
explanations, recomputed from their inputs. Engine-derived figures (rule A, rule B, buy and hold)
are recomputed by running the lessons' own preludes (NumPy and pandas needed).
Checks that fail because the content is wrong are marked CONTENT and listed as findings.
Run: python3 docs/reports/backtest-L3-numbers.py
"""
import contextlib, io, json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('backtest', 3)
E = lv.expect
R252, R12, R52 = math.sqrt(252), math.sqrt(12), math.sqrt(52)
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'backtest')


def within(fid, path, value):
    """The widget at path (a numeric widget or a wrong entry) accepts value within its tol."""
    node = lv.files[fid]
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.isdigit() else node[part]
    a = node.get('answer', node.get('value'))
    t = node.get('tol', {}).get('abs', 1e-9)
    return lv._rec(abs(a - value) <= t + 1e-12, f'{fid} {path} accepts {value!r}', f'key {a} tol {t}')


def band(fid, path, typed):
    """A slip rounded as the question asks still falls inside that wrong entry's band (wrong-band)."""
    return within(fid, path, typed)


# ---------- engine figures from the lessons' own preludes ----------
def ns(fid, i):
    w = json.load(open(os.path.join(BASE, fid + '.json')))['screens'][i]['widget']
    g = {'__name__': 'x'}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(w['prelude'], g)
        exec(w['solution'], g)
    return g

g = ns('l12-benchmark', 9)
eq = g['equity_a']
dd = eq / eq.cummax() - 1
ra = eq.pct_change().dropna()
bh = g['buy_and_hold'](g['bars'], 1_000_000)
rb = bh.pct_change().dropna()
resB = g['backtest'](g['bars'], g['target_positions'](g['momentum_signal'](g['bars']['close'], 2), 6000), costs=g['trade_cost'])
eB = resB['equity']
rB = eB.pct_change().dropna()
uw, pk, run = 0, -1e18, 0
for x in eq:
    if x >= pk:
        pk, run = x, 0
    else:
        run += 1
        uw = max(uw, run)

# ---------- l9 ----------
E('l9', 'screens[0].prose', round(eq.iloc[-1] / 1e6, 2))
E('l9', 'screens[0].explain.text', round(ra.std() * R252 * 100, 1))
E('l9', 'screens[0].explain.text', round(rB.std() * R252 * 100, 1))
E('l9', 'screens[0].widget.options[2].why', round(-dd.min() * 100))
E('l9', 'screens[0].widget.options[2].why', round(-(eB / eB.cummax() - 1).min() * 100, 1))
E('l9', 'screens[0].feedback.correct', round((eq.iloc[-1] / 1e6 - 1) * 100))
x = [0.5, -0.3, 0.8, 0.1, -0.6, 0.4, 0.2, -0.1, 0.7, -0.2]
m = sum(x) / 10
ss = sum((v - m) ** 2 for v in x)
sd = math.sqrt(ss / 9)
E('l9', 'screens[2].widget.rows[0][1].answer', m)
within('l9-sharpe', 'screens[2].widget.rows[1][1]', sd)
within('l9-sharpe', 'screens[2].widget.rows[2][1]', m / sd)
E('l9', 'screens[2].hints[1].text', f'{ss:.3f}')
E('l9', 'screens[2].explain.text', round(math.sqrt(ss / 10), 3))
E('l9', 'screens[2].explain.text', round(m / math.sqrt(ss / 10), 3))
E('l9', 'screens[1].explain.text', round(3 * sd, 3), fmt='{:.3f}')
E('l9', 'screens[1].explain.text', round(m / sd, 2))
within('l9-sharpe', 'screens[3].widget', 0.0139 / 0.652 * R252)
E('l9', 'screens[3].widget.wrong[0].value', round(0.0139 / 0.652 * 252, 3))
E('l9', 'screens[3].explain.text', round(0.0166 / 0.978 * R252, 2))
E('l9', 'screens[3].prose', round(R252, 2))
within('l9-sharpe', 'screens[4].widget', 0.8 / 3.5 * R12)
E('l9', 'screens[4].widget.wrong[0].value', round(0.8 / 3.5 * R252, 3))
E('l9', 'screens[4].widget.wrong[1].value', round(0.8 / 3.5 * 12, 3))
E('l9', 'screens[4].hints[2].text', round(R12, 2))
pooled = math.sqrt((126 * 1.0 ** 2 + 126 * 0.04 ** 2 + 126 * 0.04 ** 2) / 252)
E('l9', 'screens[5].canvas', round(pooled, 3))
E('l9', 'screens[5].widget.options[0].text', round(0.04 / pooled * R252, 2), fmt='{:.2f}')
E('l9', 'screens[5].widget.options[1].text', round(0.08 / 1.0 * R252, 2))
E('l9', 'screens[5].widget.options[2].text', round(0.04 / 1.0 * R252, 2))
E('l9', 'screens[5].widget.options[3].text', round(0.08 / pooled * R252, 2))   # CONTENT: shows 1.80, the slip gives 1.79
E('l9', 'screens[6].widget.options[0].text', round(0.05 * R252, 2))
E('l9', 'screens[6].widget.options[1].text', round(0.05 * 252, 1))
E('l9', 'screens[6].widget.options[2].text', round(0.05 * math.sqrt(365), 2))
se = lambda n: math.sqrt((1 + 1 / 504) / n)
P = lambda z: 0.5 * math.erfc(z / math.sqrt(2))
E('l9', 'screens[8].widget.answer', min(n for n in range(1, 11) if P(1 / se(n)) < 0.025))
E('l9', 'screens[8].widget.accept', round(P(1 / se(4)) * 100, 1))
E('l9', 'screens[8].feedback.byKey.three', round(P(1 / se(3)) * 100, 1))
E('l9', 'screens[8].feedback.byKey.one', round(P(1 / se(1)) * 100))
E('l9', 'screens[10].canvas', round(se(1), 6))
E('l9', 'screens[10].canvas', round(math.sqrt(1.5), 6))
E('l9', 'screens[10].explain.text', round(ra.iloc[-252:].mean() / ra.iloc[-252:].std() * R252, 2))
srm = 1.4 / R12
se_f = math.sqrt((1 + srm ** 2 / 2) / 18) * R12
within('l9-sharpe', 'screens[11].widget', se_f)
E('l9', 'screens[11].widget.wrong[0].value', round(math.sqrt((1 + 1.4 ** 2 / 2) / 1.5), 3))
E('l9', 'screens[11].widget.wrong[1].value', round(math.sqrt((1 + srm ** 2 / 2) / 18), 3))
E('l9', 'screens[11].widget.accept', round(srm, 3))
E('l9', 'screens[11].explain.text', round(1.4 / se_f, 2))
within('l9-sharpe', 'quiz[0].widget', 0.03 / 0.9 * R252)
E('l9', 'quiz[0].widget.wrong[0].value', round(0.03 / 0.9 * 252, 1))
E('l9', 'quiz[0].widget.wrong[1].value', round(0.03 / 0.9, 4))
band('l9-sharpe', 'quiz[0].widget.wrong[1]', 0.03)          # CONTENT (wrong-band): 0.03 typed misses the 'daily' band
E('l9', 'quiz[1].widget.options[0].text', round(0.1 * R52, 2))
E('l9', 'quiz[1].widget.options[1].text', round(0.1 * 52, 1))
E('l9', 'quiz[1].widget.options[2].text', round(0.1 * R252, 2))
E('l9', 'quiz[3].widget.options[0].text', round(1 / math.sqrt(2), 2))
E('l9', 'quiz[3].feedback.correct', round(0.8 / (1 / math.sqrt(2)), 1))

# ---------- l10 ----------
E('l10', 'screens[0].explain.text', round(-dd.min() * 100, 1))
E('l10', 'screens[0].feedback.byKey.second', round(-dd['2020'].min() * 100))
within('l10-drawdown-calmar', 'screens[1].widget', dd.min())
E('l10', 'screens[1].widget.wrong[1].value', round(eq.min() / eq.max() - 1, 4))
E('l10', 'screens[1].widget.wrong[2].value', round(dd['2020'].min(), 4))
E('l10', 'screens[2].prose', round(eq.iloc[-1]))
E('l10', 'screens[2].prose', round(eq.max()))
within('l10-drawdown-calmar', 'screens[2].widget', dd.iloc[-1])
E('l10', 'screens[2].widget.wrong[1].value', round(eq.iloc[-1] / 1e6 - 1, 4))
E('l10', 'screens[2].explain.text', uw)
X = [100.0]
Y = [100.0]
for r in [0.03, -0.02] * 5:
    X.append(X[-1] * (1 + r))
for r in [0.03] * 5 + [-0.02] * 5:
    Y.append(Y[-1] * (1 + r))
E('l10', 'screens[3].canvas', round(max(Y), 2))
E('l10', 'screens[3].canvas', round(Y[-1], 2))
within('l10-drawdown-calmar', 'screens[3].widget', 0.98 ** 5 - 1)
E('l10', 'screens[3].feedback.byKey.sum', round(0.98 ** 5, 3))
cg = (eq.iloc[-1] / eq.iloc[0]) ** (252 / (len(eq) - 1)) - 1
within('l10-drawdown-calmar', 'screens[4].widget.rows[0][1]', cg)
within('l10-drawdown-calmar', 'screens[4].widget.rows[1][1]', cg / -dd.min())
E('l10', 'screens[4].hints[0].text', round(252 / 1259, 4))
E('l10', 'screens[4].explain.text', round(cg / -dd.min(), 3))
E('l10', 'screens[4].explain.text', round((eq.iloc[-1] / 1e6 - 1) * 100 / 5, 1))
E('l10', 'screens[5].prose', -round((1 - eq.min() / eq.max()) * 100, 1))
E('l10', 'screens[5].widget.options[2].text', -round((eq.max() / eq.min() - 1) * 100, 1))
E('l10', 'screens[5].explain.text', round((eq.max() / eq.min() - 1) * 100, -1))
E('l10', 'screens[10].explain.text', round(uw / 21))
E('l10', 'quiz[0].widget.wrong[0].value', round(200 / 300 - 1, 4))
E('l10', 'quiz[1].widget.options[0].text', 0.08 / 0.2)
E('l10', 'quiz[1].widget.options[2].text', 0.2 / 0.08)
E('l10', 'quiz[1].widget.options[3].text', 0.08 * 20)
# screens[9].explain: "half a year too much" (CONTENT): two yearly values give 1.1 ** 0.5 - 1, not a half-year error
E('l10', 'screens[9].explain.text', round((1.1 ** 0.5 - 1) * 100, 1))   # CONTENT

# ---------- l11 ----------
E('l11', 'screens[0].explain.text', round(1.0 * 252 * 0.0005 * 100, 1))
E('l11', 'screens[0].explain.text', round(0.05 * 252 * 0.0005 * 100, 2))
E('l11', 'screens[0].feedback.correct', round(1 - 0.05 * 252 * 0.0005 / 0.15, 2))
E('l11', 'screens[0].feedback.correct', round(1 - 1 * 252 * 0.0005 / 0.15, 2))
within('l11-turnover', 'screens[1].widget', 0.5658 / 0.16438)
E('l11', 'screens[1].explain.text', round(3.335 / 0.9698, 2))
pos = [0, 1, 1, -1, -1, 0]
tv = sum(abs(b - a) for a, b in zip([0] + pos[:-1], pos)) / 6
within('l11-turnover', 'screens[2].widget', tv)
E('l11', 'screens[2].widget.wrong[1].value', round(4 / 5, 4))
p3 = [0.5, 0.6, 0.6, 0.4, 0.5]
within('l11-turnover', 'screens[3].widget', sum(abs(b - a) for a, b in zip([0] + p3[:-1], p3)) / 5)
E('l11', 'screens[3].widget.wrong[0].value', round(0.4 / 5, 4))
E('l11', 'screens[3].widget.wrong[1].value', round(sum(p3) / 5, 4))
within('l11-turnover', 'screens[4].widget', 2 * 252 * 0.00025)
E('l11', 'screens[4].widget.wrong[0].value', round(252 * 0.00025, 4))
E('l11', 'screens[5].widget.options[0].text', round(0.485 * 2, 2))
E('l11', 'screens[5].widget.options[3].text', round(0.97 * 252))
E('l11', 'screens[5].feedback.byKey.flips', round(0.97 * 252 * 0.00025 * 100, 1))
E('l11', 'screens[5].feedback.byKey.flips', round(0.485 * 252 * 0.00025 * 100, 1))
within('l11-turnover', 'screens[6].widget', 1 / 1260 * 252 * 2.5)
E('l11', 'screens[6].widget.wrong[1].value', 252 * 2.5)
E('l11', 'screens[7].prose', round(7.31 / 0.927, 1))
E('l11', 'screens[7].widget.options[0].text', round(3.54 / 0.61, 1))
E('l11', 'screens[7].widget.options[1].text', round(3.54 * 0.61, 1))
E('l11', 'screens[7].widget.options[2].text', round(0.61 / 3.54, 2))
E('l11', 'screens[9].hints[0].text', round(0.394 / 2, 3))
E('l11', 'quiz[1].widget.options[0].text', round(0.4 * 252 * 0.0005 * 100, 2))
E('l11', 'quiz[1].widget.options[1].text', round(0.4 * 0.0005 * 100, 2))
E('l11', 'quiz[1].widget.options[3].text', round(0.4 * 252 * 0.005 * 100, 1))
E('l11', 'quiz[1].explain.text', round(0.4 * 252, 1))
within('l11-turnover', 'quiz[2].widget', 2 / 0.25)
E('l11', 'quiz[3].widget.options[0].text', 4 * math.sqrt(4))

# ---------- l12 ----------
E('l12', 'screens[0].prose', round(bh.iloc[-1] / 1e3))
E('l12', 'screens[0].widget.options[1].text', round((eq.iloc[-1] - bh.iloc[-1]) / 1e4))
E('l12', 'screens[3].prose', round(ra.mean() * 100, 4))
E('l12', 'screens[3].prose', round(rb.mean() * 100, 4))
within('l12-benchmark', 'screens[3].widget', (0.0166 - 0.0138 * 0.0035) * 252 / 100)
E('l12', 'screens[3].widget.wrong[1].value', round((0.0166 - 0.0035) * 252 / 100, 3))
band('l12-benchmark', 'screens[3].widget.wrong[0]', 0.0)    # CONTENT (wrong-band): 0.0% typed misses 'daily'
E('l12', 'screens[3].explain.text', round((ra - rb).mean() / (ra - rb).std() * R252, 2))
within('l12-benchmark', 'screens[4].widget', 3 / 6)
E('l12', 'screens[4].widget.wrong[0].value', 3 / 8)
E('l12', 'screens[4].widget.wrong[1].value', 5 / 8)
E('l12', 'screens[7].widget.options[0].text', round((0.04 - 0.5 * 0.03) * 252, 1))
E('l12', 'screens[7].widget.options[1].text', round((0.04 - 0.03) * 252, 1))
E('l12', 'screens[7].widget.options[3].text', round(0.04 * 252, 1))
E('l12', 'screens[8].canvas', 200 * 50.5 - 3)
E('l12', 'screens[8].canvas', 200 * 52 - 3)
E('l12', 'screens[8].feedback.correct', '947,384.39')
E('l12', 'screens[8].feedback.correct', round(g['beta_alpha'](ra, rb)[0], 4))
E('l12', 'screens[11].canvas', round(dd.min() * 100, 2))
E('l12', 'screens[11].canvas', round(rb.std() * R252 * 100, 1))
E('l12', 'screens[11].canvas', round(g['max_drawdown'](bh) * 100, 2))
E('l12', 'screens[11].widget.options[3].text', 0.66)
within('l12-benchmark', 'quiz[1].widget', (0.05 - 1.2 * 0.04) * 252 / 100)
E('l12', 'quiz[1].widget.wrong[0].value', round((0.05 - 0.04) * 252 / 100, 4))
E('l12', 'quiz[2].widget.options[1].text', round(110 / 252, 2))
E('l12', 'quiz[2].widget.options[2].text', round((110 + 52) / 252, 2))   # CONTENT: shows 0.65
E('l12', 'quiz[2].widget.options[3].why', 162)                          # CONTENT: "140 non-losing days" (110 + 52 = 162)

# ---------- review-3 ----------
within('review-3', 'items[0].widget', 1.2 / 4 * R12)
E('review', 'items[0].widget.wrong[1].value', round(0.3 * R252, 2))
within('review-3', 'items[1].widget', 98 / 140 - 1)
E('review', 'items[1].widget.wrong[1].value', round(98 / 130 - 1, 4))
within('review-3', 'items[2].widget', 1.2 - 0.5 * 252 * 0.0005 / 0.12)
E('review', 'items[2].widget.wrong[0].value', 1.2 - 0.25 * 252 * 0.0005 / 0.12)
E('review', 'items[2].widget.wrong[1].value', round(1.2 - 0.5 * 0.0005 / 0.12, 3))
within('review-3', 'items[3].widget', (0.05 - 0.8 * 0.04) * 252 / 100)
band('review-3', 'items[3].widget.wrong[1]', 0.0)            # CONTENT (wrong-band)
se3 = math.sqrt((1 + 0.9 ** 2 / 504) / 3)
within('review-3', 'items[5].widget', se3)
E('review', 'items[5].widget.wrong[0].value', round(math.sqrt((1 + 0.81 / 2) / 3), 3))
E('review', 'items[5].widget.wrong[1].value', round(se3 / R252, 4))
band('review-3', 'items[5].widget.wrong[1]', 0.04)           # CONTENT (wrong-band)
E('review', 'items[5].feedback.correct', round(0.9 / se3, 1))
within('review-3', 'items[6].widget', (1.5 ** (252 / 1008) - 1) / 0.25)
E('review', 'items[7].widget.options[0].text', round(1.2 * 252 * 0.00025 * 100, 1))
within('review-3', 'items[8].widget', 99 / 180)
E('review', 'items[8].widget.wrong[0].value', round(99 / 252, 4))
E('review', 'items[8].widget.wrong[1].value', round((99 + 72) / 252, 4))

# ---------- homework-3 ----------
within('homework-3', 'items[1].widget', 1.8 * 252 * 0.0003)
E('homework', 'items[1].explain.text', 1.8 * 252)
within('homework-3', 'items[2].widget', (2 / 0.5) ** 2)
within('homework-3', 'items[3].widget', 10 * ((10 / 0.5 - 2) / 6) ** 2)
E('homework', 'items[3].widget.wrong[0].value', round(10 * ((10 / 0.5) / 6) ** 2, 1))
E('homework', 'items[3].widget.wrong[1].value', 10 * (10 / 0.5 - 2) / 6)
E('homework', 'items[4].explain.text', round(0.4 * 3 - 0.6, 1))
E('homework', 'items[7].widget.model', round(1 / math.sqrt(6), 2))
E('homework', 'items[7].widget.model', round(1.1 * math.sqrt(6), 1))
E('homework', 'items[7].widget.model', round(1.1 * 0.15 / 0.38, 2))
E('homework', 'items[7].widget.model', round(1.8 * 252 * 0.00025 * 100, 1))
E('homework', 'items[7].widget.model', round(1.8 * 252 * 0.0005 * 100, 1))

lv.check_wrongs()
lv.report()
