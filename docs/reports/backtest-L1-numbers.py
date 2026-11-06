"""Recompute every number stated in backtest level 1 (Design) and check it at its JSON path (second read).

Run: python3 docs/reports/backtest-L1-numbers.py   (NumPy, pandas and the standard library; exits 0 when every check passes)

`make_bars()` (seed 2301) is taken from the lessons' own preludes, and the brief's checks are asserted first.
Ledgers, orders, counts and dates are recomputed here by direct arithmetic; pandas behaviour that a claim rests on
(centred windows, busday counts, rounding) is run, not assumed. `claim` ties a statement to a computation;
`stated` ties a claim to its wording (while the phrase is in the text, the claim must hold). A check that fails
because the content is wrong is a finding in docs/reviews/review-backtest-1-2.md and stays failing until the fix
pass corrects the content.
"""
import datetime as dt
import math
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("backtest", 1)
E = lv.expect


def claim(name, ok):
    lv._rec(bool(ok), f'claim: {name}', '')


def stated(ref, path, phrase, ok):
    try:
        txt = lv.text(ref, path)
    except KeyError:                              # the field itself was removed by a fix
        txt = ''
    if phrase in txt:
        lv._rec(bool(ok), f'stated: {ref} {path} "{phrase}"', '' if ok else 'the wording claims something false')
    else:
        lv._rec(True, f'stated: {ref} {path} "{phrase}" (phrase gone)', '')


def J(ref, path):
    _, doc = lv._file(ref)
    node = doc
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.isdigit() else node[part]
    return node


# ---------- the shared generator, from the l1 prelude ----------
g = {}
exec(J('l1', 'screens[3].widget.prelude'), g)
make_bars = g['make_bars']
b = make_bars()
r = np.log(b.close).diff().fillna(0)
sh = lambda x: math.sqrt(252) * np.mean(x) / np.std(x, ddof=1)
claim('brief: first row open 100.0463, close 99.5909, volume 2,424,184',
      (round(b.open.iloc[0], 4), round(b.close.iloc[0], 4), int(b.volume.iloc[0])) == (100.0463, 99.5909, 2424184))
claim('brief: same-bar Sharpe 20.3828', round(sh(np.sign(r) * r), 4) == 20.3828)
claim('brief: honest close-to-close Sharpe 0.8228', round(sh((np.sign(r) * r.shift(-1)).dropna()), 4) == 0.8228)

# ---------- l1 ----------
rows = J('l1', 'screens[1].canvas.params.rows')
mine = [[str(d.date()), f'{o:.2f}', f'{h:.2f}', f'{lo:.2f}', f'{c:.2f}', f'{v / 1e6:.2f}m']
        for d, (o, h, lo, c, v) in zip(b.index[:12], b.iloc[:12][['open', 'high', 'low', 'close', 'volume']].values)]
claim('l1 screens[1] table is the first 12 rows of make_bars()', rows == mine)
claim('l1 screens[2] cells are the same 12 closes', J('l1', 'screens[2].canvas.params.cells') == [f'{c:.2f}' for c in b.close[:12]])
claim('l1 row 1 close beats row 0', b.close.iloc[1] > b.close.iloc[0])
E('l1', 'screens[1].explain.text', 100.28)
E('l1', 'screens[1].explain.text', 99.59)
E('l1', 'screens[1].explain.text', round(b.open.iloc[2], 2))           # 98.81, the earliest fill
E('l1', 'screens[2].widget.answer', len(range(0, 8)))                   # bars 0..7
E('l1', 'screens[2].widget.wrong[1].value', 12)
# screens[4]: Tuesday 10 March 2020, February 2020 has 29 days
claim('l1 screens[4] Tue 10 March is a Tuesday (2020)', dt.date(2020, 3, 10).weekday() == 1)
claim('l1 screens[4] Mon 9 and Mon 16 March 2020 are Mondays', dt.date(2020, 3, 9).weekday() == 0 == dt.date(2020, 3, 16).weekday())
claim('l1 screens[4] February 2020 ended on the 29th', (dt.date(2020, 3, 1) - dt.timedelta(days=1)).day == 29)
E('l1', 'screens[4].explain.text', 29)
# screens[5]: the hand series
s5 = pd.Series([100, 102, 101, 101, 104.0])
claim('l1 screens[5] example [0, 1, -1, 0, 1]', np.sign(s5.pct_change(1)).fillna(0).tolist() == [0.0, 1.0, -1.0, 0.0, 1.0])
# screens[6]: lookback 5, bars 0..4 have no return
claim('l1 screens[6] bars 0 to 4 have no 5-day return', b.close[:12].pct_change(5).isna().tolist() == [True] * 5 + [False] * 7)
# screens[7]: rolling(5, center=True) at bar 7 uses bars 5..9
ar = pd.Series(np.arange(12.0))
claim('l1 screens[7] centred 5-window at bar 7 averages bars 5 to 9', ar.rolling(5, center=True).mean()[7] == np.mean([5, 6, 7, 8, 9]))
# screens[10]: average of 1.3 and 0.4
E('l1', 'screens[10].widget.options[1].text', (1.3 + 0.4) / 2)
# quiz[1]: pct_change(20) NaN for bars 0..19
claim('l1 quiz[1] pct_change(20) has 20 NaNs', int(b.close.pct_change(20).isna().sum()) == 20)
E('l1', 'quiz[1].widget.answer', 20)
# quiz[2]: a 10-bar centred window covers t-5..t+4 (four bars ahead, not five)
m10 = ar.rolling(10, center=True).mean()
claim('l1 quiz[2] centred 10-window at t covers t-5..t+4', m10[6] == np.mean(np.arange(1, 11)))
stated('l1', 'quiz[2].feedback.correct', 'five bars ahead', False)   # FINDING: it reaches four bars ahead
# quiz[3]: a shift(-1) on vector_targets(close, 3) disagrees on 337 of 1,260 bars, not 412
v3 = np.sign(b.close.pct_change(3)).fillna(0)
n_dis = int((v3 != v3.shift(-1).fillna(0)).sum())
claim('l1 quiz[3] shift(-1) disagreement count is 337', n_dis == 337)
E('l1', 'quiz[3].prose', n_dis)                                          # FINDING: the prose says 412
E('l1', 'quiz[3].prose', len(b))

# ---------- l2 ----------
lines0 = J('l2', 'screens[0].canvas.params.lines')
claim('l2 screens[0] four fetch lines + 35 more + one = 40', sum(l.startswith('[') and 'fetch' in l for l in lines0) + 35 == 40)
E('l2', 'screens[0].widget.wrong[0].value', 40)
claim('l2 screens[1] network lines are l2 and l6 (1-based)', [i + 1 for i, l in enumerate(J('l2', 'screens[1].canvas.params.lines')) if 'network' in l] == [2, 6])
# screens[4]: the planted table
t4 = J('l2', 'screens[4].canvas.params.rows')
bad = []
for i, (d, o, h, lo, c, v) in enumerate(t4):
    o, h, lo, v = float(o), float(h), float(lo), float(v.replace(',', ''))
    c = float(c) if c else None
    why = []
    if i and d <= t4[i - 1][0]:
        why.append('date')
    if c is None:
        why.append('nan')
    else:
        if h < max(o, c):
            why.append('high')
        if lo > min(o, c):
            why.append('low')
    if v < 0:
        why.append('vol')
    if why:
        bad.append(f'r{i}')
claim('l2 screens[4] the five bad rows are r3, r5, r7, r9, r10', bad == J('l2', 'screens[4].widget.answer'))
E('l2', 'screens[4].explain.text', 97.70)
E('l2', 'screens[4].explain.text', 97.75)
E('l2', 'screens[4].explain.text', 98.43)
E('l2', 'screens[4].explain.text', 98.40)
claim('l2 screens[4] byKey.r8 high 99.47 above open and close', float(t4[8][2]) >= max(float(t4[8][1]), float(t4[8][4])))
claim('l2 screens[4] row 4 skips one business day (7 Jan)', int(np.busday_count('2019-01-04', '2019-01-08')) == 2)
# screens[5] byKey test-9: seven missing business days -> busday_count 8
claim('l2 screens[5] seven missing days give busday_count 8', int(np.busday_count('2019-01-02', np.busday_offset('2019-01-02', 8))) == 8)
E('l2', 'screens[5].feedback.byKey', 8)
# screens[6]: 783 bars 2019-01-02..2021-12-31
E('l2', 'screens[6].canvas.params.lines[2]', len(b.loc[:'2021-12-31']))
claim('l2 make_bars() ends 2023-10-31 with 1,260 bars', (str(b.index[-1].date()), len(b)) == ('2023-10-31', 1260))
# quiz[1]: 3 keys, 2 tickers
reqs = [('AAPL', 2019, 2021), ('AAPL', 2019, 2023), ('MSFT', 2019, 2023), ('AAPL', 2019, 2021), ('AAPL', 2019, 2023)]
E('l2', 'quiz[1].widget.answer', len(set(reqs)))
E('l2', 'quiz[1].widget.wrong[0].value', len({q[0] for q in reqs}))
E('l2', 'quiz[1].widget.wrong[1].value', len(reqs))
# quiz[2]: Fri 6 March 2020 to Fri 20 March 2020
bc = int(np.busday_count('2020-03-06', '2020-03-20'))
claim('l2 quiz[2] both dates are Fridays', dt.date(2020, 3, 6).weekday() == 4 == dt.date(2020, 3, 20).weekday())
E('l2', 'quiz[2].explain.text', bc)
stated('l2', 'quiz[2].explain.text', 'Nine trading days', bc - 1 == 9)
E('l2', 'quiz[2].widget.options[3].why', bc)

# ---------- l3 ----------
E('l3', 'screens[0].widget.answer', round(0.4 * 10_000) - round(0.25 * 10_000))
claim('l3 screens[0] position series = signal x 10,000', [round(x * 10_000) for x in J('l3', 'screens[0].canvas.left.params.series[0].values')] == J('l3', 'screens[0].canvas.right.params.series[0].values'))
claim('l3 screens[0] £1m / £100 = 10,000 shares', 1_000_000 / 100 == 10_000)
E('l3', 'screens[1].widget.answer', round(-0.5 * 10_000) - 2500)
E('l3', 'screens[1].widget.wrong[0].value', -5000)
tg4 = [0, 4000, 4000, 10000, -10000, -10000, 0]
o4 = [tg4[0]] + [tg4[i] - tg4[i - 1] for i in range(1, 7)]
claim('l3 screens[4] orders', o4 == [J('l3', f'screens[4].widget.rows[{i}][2].answer') for i in range(7)])
claim('l3 screens[4] orders add back to the final target 0', sum(o4) == 0)
claim('l3 screens[5] np.round(3.5) = 4 and np.round(0.861) = 1', (np.round(3.5), np.round(0.861)) == (4.0, 1.0))
claim('l3 screens[5] example', np.round(pd.Series([0.4, -1, 0, 1.7]).clip(-1, 1) * 10_000).astype(int).tolist() == [4000, -10000, 0, 10000])
E('l3', 'screens[7].widget.answer', 10 * 4000)
claim('l3 screens[9] £50m / £100 = 500_000', 50_000_000 / 100 == 500_000)
E('l3', 'screens[9].prose', 'max_units = 500_000')
E('l3', 'screens[9].widget.options[0].text', 0.05 * 2_000_000)           # 100,000
E('l3', 'screens[9].explain.text', 0.4 * 500_000)                        # 200,000
E('l3', 'quiz[0].widget.answer', 0.6 * 5000)
E('l3', 'quiz[1].widget.answer', -3000 - 2000)
E('l3', 'quiz[1].widget.wrong[1].value', -3000 + 2000)
tq = [0, 3000, 3000, -2000, -2000, 1000]
oq = [tq[0]] + [tq[i] - tq[i - 1] for i in range(1, 6)]
E('l3', 'quiz[3].widget.answer', sum(map(abs, oq)))
E('l3', 'quiz[3].widget.wrong[0].value', sum(oq))
E('l3', 'quiz[3].widget.wrong[1].value', 3000 + 2000 + 3000)

# ---------- l4: the ledger ----------
px = J('l4', 'screens[0].canvas.params.series[0].values')
cash, sh_ = 10_000.0, 0
ledger = []
for day, (q, p) in {1: (100, 50.10), 2: (0, 0), 3: (50, 49.70), 4: (-150, 50.60), 5: (-80, 51.00), 6: (0, 0)}.items():
    if q:
        cash -= q * p + 1.0
        sh_ += q
    ledger.append((round(cash, 2), sh_, round(cash + sh_ * px[day], 2)))
claim('l4 ledger cash/shares/equity', ledger == [(4989.0, 100, 10029.0), (4989.0, 100, 9969.0), (2503.0, 150, 10033.0),
                                                   (10092.0, 0, 10092.0), (14171.0, -80, 10067.0), (14171.0, -80, 10107.0)])
E('l4', 'screens[0].widget.rows[1][2].answer', ledger[0][0])
E('l4', 'screens[0].widget.rows[1][5].answer', ledger[0][2])
E('l4', 'screens[0].widget.rows[2][5].answer', ledger[1][2])
E('l4', 'screens[0].explain.text', ledger[0][2] - ledger[1][2])          # equity fell £60
E('l4', 'screens[1].widget.answer', (10_000 - 4989) / 100)               # 50.11
E('l4', 'screens[1].feedback.byKey.fill', 4989 + 100 * 50.10)            # 9,999
E('l4', 'screens[1].feedback.byKey.start', 4989 + 100 * 50.00)           # 9,989
E('l4', 'screens[2].widget.answer', 4989 + 100 * 50.10 - 10_000)
E('l4', 'screens[3].widget.rows[1][2].answer', ledger[2][0])
E('l4', 'screens[3].widget.rows[1][5].answer', ledger[2][2])
E('l4', 'screens[3].widget.rows[2][2].answer', ledger[3][0])
E('l4', 'screens[3].explain.text', ledger[3][2] - 10_000)                # £92
E('l4', 'screens[4].widget.rows[1][2].answer', ledger[4][0])
E('l4', 'screens[4].widget.rows[1][5].answer', ledger[4][2])
E('l4', 'screens[4].explain.text', -round(80 * 51.30, 2))                # -£4,104
E('l4', 'screens[4].explain.text', ledger[3][2] - ledger[4][2])          # £25
E('l4', 'screens[5].widget.answer', round(-80 * (50.80 - 51.30), 2))
E('l4', 'screens[5].explain.text', ledger[5][2])
E('l4', 'screens[7].widget.options[2].text', ledger[0][2] - 1)
E('l4', 'screens[7].widget.options[3].text', ledger[0][2] + 1)
E('l4', 'screens[9].hints[1].text', 61_240 / 3_062)                      # £20 a trade
E('l4', 'quiz[0].widget.answer', 10_000 - 200 * 25.05 - 1)
E('l4', 'quiz[1].widget.answer', 4989 + 200 * 25.30)
E('l4', 'quiz[1].explain.text', 200 * 0.25 - 1)                          # £49
qc = 20_000 + 100 * 40 - 2
E('l4', 'quiz[2].widget.options[0].text', qc)
E('l4', 'quiz[2].widget.options[0].text', qc - 100 * 40)
# l4 quiz[3]: now a copy of screens[5]; review finding gives fresh numbers (-120 x 0.35 = -42). Either passes.
claim('l4 quiz[3] answer: -80 x (50.80 - 51.30) now, or -120 x (37.10 - 36.75) after the fix',
      J('l4', 'quiz[3].widget.answer') in (round(-80 * (50.80 - 51.30), 2), round(-120 * (37.10 - 36.75), 2)))

# ---------- review-1 ----------
E('review', 'items[0].widget.answer', sum(range(1, 251)))
E('review', 'items[0].widget.wrong[1].value', 250 * 250)
E('review', 'items[0].widget.wrong[2].value', sum(range(0, 250)))
claim('review-1 items[2] Thursday 14 May (2020)', dt.date(2020, 5, 14).weekday() == 3)
claim('review-1 items[3] high 101.20 below the open 101.50', 101.20 < max(101.50, 100.90) and 100.40 <= min(101.50, 100.90))
E('review', 'items[5].widget.answer', -0.25 * 8000 - 1000)
cs = 12_000 + 150 * 40 - 1.5
E('review', 'items[7].widget.answer', cs - 150 * 39.20)
E('review', 'items[7].widget.wrong[0].value', cs)
E('review', 'items[7].widget.wrong[1].value', cs + 150 * 39.20)
E('review', 'items[7].widget.wrong[2].value', cs - 150 * 40)
E('review', 'items[7].explain.text', -150 * 39.20)
stated('review', 'items[1].explain.text', 'Only the first', False)       # FINDING: names an option by place

# ---------- homework-1 ----------
sig = [np.nan, np.nan, 0.4, 0.4, -0.6, 1.3, 0]
tgt = [int(np.round(np.clip(0 if np.isnan(s) else s, -1, 1) * 5000)) for s in sig]
od = [tgt[0]] + [tgt[i] - tgt[i - 1] for i in range(1, 7)]
E('homework', 'items[3].widget.answer', sum(map(abs, od)))
raw = [0, 0, 2000, 2000, -3000, 6500, 0]
E('homework', 'items[3].widget.wrong[0].value', sum(abs(raw[i] - raw[i - 1]) for i in range(1, 7)))
E('homework', 'items[3].widget.wrong[2].value', 2000 + 5000 + 5000 + 5000)
c1 = 25_000 - 300 * 40.20 - 2
c2 = c1 + 500 * 41.00 - 2
E('homework', 'items[5].widget.answer', c2 - 200 * 40.60)
E('homework', 'items[5].widget.wrong[0].value', c2)
E('homework', 'items[5].widget.wrong[1].value', c2 - 200 * 41.00)
E('homework', 'items[5].widget.wrong[2].value', c2 + 200 * 40.60)
E('homework', 'items[5].feedback.generic', c1)
# items[4]: rolling(20, center=True) reads nine bars ahead, not ten
ar40 = pd.Series(np.arange(40.0))
claim('homework-1 items[4] centred 20-window at t covers t-10..t+9', ar40.rolling(20, center=True).mean()[20] == np.mean(np.arange(10, 30)))
stated('homework', 'items[4].explain.text', 'reads ten bars ahead', False)   # FINDING: nine
# items[0]: 14 trades on make_bars(60), so the £1 fee costs £14
gh = {}
exec(J('homework', 'items[0].widget.prelude'), gh)
exec(J('homework', 'items[0].widget.solution'), gh)
b60 = gh['make_bars'](60)
e0 = gh['run_loop_with_portfolio'](b60, lambda h: 100 * gh['decide_mom'](h, 3), 10_000)
e1 = gh['run_loop_with_portfolio'](b60, lambda h: 100 * gh['decide_mom'](h, 3), 10_000, 1.0)
tr = np.diff([0] + gh['run_loop'](b60, lambda h: 100 * gh['decide_mom'](h, 3)))
claim('homework-1 items[0] 14 trades', int((tr != 0).sum()) == 14)
E('homework', 'items[0].explain.text', int((tr != 0).sum()))
claim('homework-1 items[0] £10,495.02 and £10,481.02', (round(e0[-1], 2), round(e1[-1], 2)) == (10495.02, 10481.02))
# items[6] model: the honest long-or-flat rule has a Sharpe below 1 on make_bars()
lf = ((b.close.pct_change() > 0).astype(int).shift(1) * b.close.pct_change()).dropna()
claim('homework-1 items[6] honest long-or-flat Sharpe below 1', sh(lf) < 1)

lv.check_wrongs()
lv.report()
