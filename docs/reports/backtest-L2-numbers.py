"""Recompute every number stated in backtest level 2 (Execution) and check it at its JSON path (second read).

Run: python3 docs/reports/backtest-L2-numbers.py   (NumPy, pandas and the standard library; exits 0 when every check passes;
about a minute: the capacity table runs the impact engine 24 times)

The engine pieces (`backtest`, `trade_cost`, `backtest_with_impact`, the planted engines) are exec'd from the lessons'
own preludes and solutions, so the engine numbers come from the code the learner writes. Each engine figure has a
second route where one exists: the cost totals by direct sums over the fills, the l5 explore sweep by rebuilding
`make_bars` with a different overnight share, the impact figures by the square-root formula by hand. `claim` ties a
statement to a computation; `stated` ties a claim to its wording. A check that fails because the content is wrong is
a finding in docs/reviews/review-backtest-1-2.md and stays failing until the fix pass corrects the content.
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

lv = Level("backtest", 2)
E = lv.expect
fails = []


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


def two(name, a, b, tol=1e-6):
    lv._rec(math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), f'two routes: {name}', f'{a!r} vs {b!r}')


def J(ref, path):
    _, doc = lv._file(ref)
    node = doc
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.isdigit() else node[part]
    return node


def load(ref, path, solution=True):
    ns = {}
    w = J(ref, path)
    exec(w['prelude'], ns)
    if solution:
        exec(w['solution'], ns)
    return ns


g8 = load('l8', 'screens[4].widget')          # engines, backtest, trade_cost, lookahead_check
g7 = load('l7', 'screens[8].widget')          # backtest_with_impact, slippage_bp, capped_qty
g6 = load('l6', 'screens[7].widget')          # net_sharpe_table
gh = load('homework', 'items[0].widget')      # execution_report
gl = load('homework', 'items[1].widget')      # leaky_or_not
make_bars = g8['make_bars']
b = make_bars()
r = np.log(b.close).diff().fillna(0)
shr = lambda x: math.sqrt(252) * np.mean(x) / np.std(x, ddof=1)
eng_sharpe = lambda eq, base=1e6: g8['sharpe'](eq.diff().dropna() / base)

# ---------- l5 ----------
leak = shr(np.sign(r) * r)
honest = shr((np.sign(r) * r.shift(-1)).dropna())
E('l5', 'screens[0].prose', round(leak, 2))
E('l5', 'screens[0].widget.options[1].why', round(honest, 2))
E('l5', 'screens[0].widget.options[3].why', round(leak / honest))           # "25 times"
eq_leak = 100 * np.exp(np.cumsum(np.sign(r) * r))
eq_hon = 100 * np.exp(np.cumsum((np.sign(r) * r.shift(-1)).fillna(0)))
E('l5', 'screens[0].widget.options[2].why', round(eq_hon.iloc[-1]))           # £221
E('l5', 'screens[0].canvas.state.caption', round(eq_hon.iloc[-1]))
claim('l5 screens[0] leak line ends at £17.95m', round(eq_leak.iloc[-1] / 1e6, 2) == 17.95)


def make_bars_f(f, n=1260, seed=2301, mu=0.0003, sigma=0.012, phi=0.06):
    """make_bars with the overnight share f in place of 0.5 (same draws, so the closes do not change)."""
    rng = np.random.default_rng(seed)
    eps = sigma * rng.standard_normal(n)
    rr = np.empty(n)
    prev = 0.0
    for t in range(n):
        rr[t] = mu + phi * prev + eps[t]
        prev = rr[t] - mu
    close = 100 * np.exp(np.cumsum(rr))
    prev_close = np.r_[100.0, close[:-1]]
    gap = f * rr + 0.002 * rng.standard_normal(n)
    return pd.DataFrame({'open': prev_close * np.exp(gap), 'close': close})


def next_open_sharpe(bb):
    lr = np.log(bb.close).diff().fillna(0)
    return shr((np.sign(lr) * np.log(bb.open.shift(-2) / bb.open.shift(-1))).dropna())


sweep = [round(next_open_sharpe(make_bars_f(k / 10)), 4) for k in range(11)]
claim('l5 screens[1] make_bars_f(0.5) reproduces make_bars closes and opens',
      np.allclose(make_bars_f(0.5).close, b.close) and np.allclose(make_bars_f(0.5).open, b.open))
claim('l5 screens[1] next-open sweep matches the canvas nx', np.allclose(sweep, J('l5', 'screens[1].canvas.params.params.nx'), atol=1e-4))
E('l5', 'screens[1].widget.answer', round(sweep[5], 2))
claim('l5 screens[1] prose no longer offers the same close as a choice; label is Overnight share', 'It can fill at that same close' not in lv.text('l5', 'screens[1].prose') and J('l5', 'screens[1].canvas.controls[0].label') == 'Overnight share')
E('l5', 'screens[1].widget.accept', round(sweep[5], 4))
E('l5', 'screens[3].widget.answer', round(1000 * (101.10 - 100.40), 2))
E('l5', 'screens[3].widget.wrong[0].value', round(1000 * (100.90 - 100.40), 2))
E('l5', 'screens[3].widget.wrong[1].value', round(1000 * (101.10 - 100.90), 2))
E('l5', 'screens[3].explain.text', 101_100)
E('l5', 'screens[3].explain.text', 100_400)
claim('l5 screens[4] Mon 27 May 2019 (spring bank holiday, last Monday of May)', dt.date(2019, 5, 27).weekday() == 0 and (dt.date(2019, 5, 27) + dt.timedelta(7)).month == 6)
claim('l5 screens[4] Fri 24 May and Wed 29 May 2019', dt.date(2019, 5, 24).weekday() == 4 and dt.date(2019, 5, 29).weekday() == 2)


def easter(y):
    a, bq, c = y % 19, y // 100, y % 100
    d, e = bq // 4, bq % 4
    f = (bq + 8) // 25
    gg = (bq - f + 1) // 3
    h = (19 * a + bq - d - gg + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    mo = (h + l_ - 7 * m + 114) // 31
    return dt.date(y, mo, (h + l_ - 7 * m + 114) % 31 + 1)


claim('easter() gives 17 April 2022 and 21 April 2019', easter(2022) == dt.date(2022, 4, 17) and easter(2019) == dt.date(2019, 4, 21))
# quiz[0]: FINDING. Friday 22 April 2022 to Tuesday 26 April is not the Easter break (Good Friday was 15 April 2022)
stated('l5', 'quiz[0].prose', 'Friday 22 April 2022', False)
claim('l5 quiz[0] prose is Friday 26 August 2022 then Tuesday 30 August', all(s in lv.text('l5', 'quiz[0].prose') for s in ('Friday 26 August 2022', 'Tuesday 30 August', 'August bank holiday')))
claim('fix: Fri 26 Aug 2022 then Tue 30 Aug (Mon 29 Aug 2022 was the summer bank holiday)',
      dt.date(2022, 8, 26).weekday() == 4 and dt.date(2022, 8, 29).weekday() == 0 and (dt.date(2022, 8, 29) + dt.timedelta(7)).month == 9)
E('l5', 'quiz[1].widget.answer', 2000 * 49.60)
E('l5', 'quiz[1].widget.wrong[0].value', 2000 * 50.00)
E('l5', 'quiz[1].explain.text', 2000 * 0.40)
E('l5', 'quiz[3].widget.answer', 40 - 1)
# quiz[2]: FINDING. signal.shift(-1) * r is not "a worse leak" than signal * r on make_bars
stated('l5', 'quiz[2].widget.options[2].why', 'a worse leak', False)
claim('l5 quiz[2] signal.shift(-1) * r is a far milder leak (Sharpe 1.05 against 20.38)', round(shr((np.sign(r).shift(-1) * r).dropna()), 2) == 1.05 and shr((np.sign(r).shift(-1) * r).dropna()) < leak / 10)
claim('l5 quiz[2] why says tomorrow\'s signal is not known until tomorrow\'s close', 'not known until tomorrow' in lv.text('l5', 'quiz[2].widget.options[2].why'))
# screens[6]: the hand frame through the engine
hb = g8.get('hand_bars') or g7['hand_bars']
ex = g7['backtest'](hb(), [0, 100, 100, -100, -100, 0], 10_000).round(2).values.tolist()
claim('l5 screens[6] example matrix', ex == eval(J('l5', 'screens[6].widget.examples[0].expect')))
E('l5', 'screens[6].explain.text', ex[-1][2])                                # £10,350
# summary: 0.82 to 20.38, 0.57
E('l5', 'summary.ideas[1]', round(honest, 2))
E('l5', 'summary.ideas[2]', round(sweep[5], 2))

# ---------- the engine on make_bars(), lookbacks 1 and 2 ----------
tg1 = g8['target_positions'](g8['momentum_signal'](b.close, 1), 10_000)
tg2 = g8['target_positions'](g8['momentum_signal'](b.close, 2), 10_000)
o1, o2 = g8['orders_from_targets'](tg1), g8['orders_from_targets'](tg2)
f1 = g8['fill_at_next_open'](o1, b)
q1 = o1[o1 != 0].iloc[:len(f1)].values
traded = float((np.abs(q1) * f1.values).sum())
comm = float(sum(max(0.005 * abs(q), 1.0) for q in q1))
eq1 = g8['backtest'](b, tg1)['equity']
gross = eq1.iloc[-1] - 1e6
two('l6 gross P&L: engine vs cash accounting (minus the sum of q x fill, plus final shares x last close)',
    gross, float(-sum(q * p for q, p in zip(q1, f1.values)) + q1.sum() * b.close.iloc[-1]), 1e-6)
E('l6', 'screens[1].prose', round(gross))
E('l6', 'screens[1].prose', round(traded / 1e9, 2))
E('l6', 'screens[1].prose', comm)
E('l6', 'screens[1].explain.text', round(gross - comm))
E('l6', 'screens[1].explain.text', round(traded / 1e4))
E('l6', 'screens[1].widget.answer', round((gross - comm) / (traded / 1e4), 2))
E('l6', 'screens[1].widget.wrong[0].value', round(gross / (traded / 1e4), 2))
E('l6', 'screens[1].canvas.params.functions[0].expr', round((gross - comm) / 1e3, 3))
E('l6', 'screens[1].canvas.params.functions[0].expr', round(traded / 1e7, 3))
E('l6', 'summary.ideas[2]', round(gross - comm))
# a fixed-cost engine run gives the same break-even
eqb = g8['backtest'](b, tg1, costs=lambda q, p: g8['trade_cost'](q, p, half_spread_bp=(gross - comm) / (traded / 1e4)))['equity']
claim('l6 screens[1] net P&L is 0 at the break-even half spread (engine run)', abs(eqb.iloc[-1] - 1e6) < 1.0)
# screens[9] bars, and "about twice as often"
bars9 = J('l6', 'screens[9].canvas.state.values')
for lb, tg in ((1, tg1), (2, tg2)):
    row = [round(eng_sharpe(g8['backtest'](b, tg)['equity']), 3)]
    for h in (1, 2.5, 5, 10):
        row.append(round(eng_sharpe(g8['backtest'](b, tg, costs=lambda q, p, h=h: g8['trade_cost'](q, p, half_spread_bp=h))['equity']), 3))
    claim(f'l6 screens[9] bars lookback {lb}', row == [bars9[f'lb{lb}'][k] for k in ('g', 'c1', 'c25', 'c5', 'c10')])
ratio = o1.abs().sum() / o2.abs().sum()
claim('lookback 1 trades 1.58 times the shares of lookback 2 (12.25m against 7.73m)', round(ratio, 2) == 1.58)
stated('l6', 'screens[9].explain.text', 'about twice as often', False)
stated('l6', 'screens[9].widget.options[1].why', 'about twice as often', False)
E('l6', 'screens[9].explain.text', round(ratio, 1))       # 1.6 times as many shares
E('l6', 'screens[9].widget.options[1].why', round(ratio, 1))
E('l6', 'screens[9].explain.text', round(eng_sharpe(eq1), 2))       # 0.60 gross
E('l6', 'screens[9].explain.text', round(eng_sharpe(g8['backtest'](b, tg2)['equity']), 2))   # 0.51
E('l6', 'screens[1].prose', round(eng_sharpe(eq1), 2))       # 0.60, not l5's 0.57
E('l6', 'screens[1].prose', round(sweep[5], 2))
# hand tickets
tc = g8['trade_cost']
E('l6', 'screens[0].widget.answer', round(500 * (100.02 - 100.00), 2))
E('l6', 'screens[0].widget.wrong[2].value', round(500 * 100.02, 2))
E('l6', 'screens[2].widget.rows[2][1].answer', tc(500, 100.0))
E('l6', 'screens[3].widget.answer', tc(100, 100.0))
E('l6', 'screens[4].widget.options[0].text', tc(-300, 100.0))
E('l6', 'screens[4].widget.options[1].text', tc(1000, 50.0))
E('l6', 'screens[5].widget.options[0].text', 2 * tc(500, 100.0))
E('l6', 'screens[5].widget.options[1].text', 2 * tc(500, 100.0, half_spread_bp=4.0))
E('l6', 'screens[5].widget.options[2].text', tc(500, 100.0) + tc(500, 100.0, half_spread_bp=0.0))
E('l6', 'screens[8].widget.answer', tc(1000, 20.0, half_spread_bp=5.0))
a10, b10 = tc(20_000, 100.0), tc(20_000, 100.0, per_share=0.0, minimum=0.0, half_spread_bp=3.0)
E('l6', 'screens[10].widget.answer', round(b10 - a10, 6))
E('l6', 'screens[10].explain.text', 2_000_000 * 1e-4)
E('l6', 'quiz[0].widget.answer', tc(2000, 25.0, half_spread_bp=4.0))
E('l6', 'quiz[0].widget.wrong[0].value', tc(2000, 25.0, half_spread_bp=8.0))
E('l6', 'quiz[2].widget.answer', 2 * tc(1000, 50.0))
E('l6', 'quiz[2].widget.wrong[1].value', 2 * tc(1000, 50.0, half_spread_bp=4.0))
E('l6', 'quiz[3].widget.answer', 30_000 / 60e6 * 1e4)
b250 = make_bars(250)
t250 = g8['target_positions'](g8['momentum_signal'](b250.close, 1), 10_000)
cost250 = g8['backtest'](b250, t250)['equity'].iloc[-1] - g8['backtest'](b250, t250, costs=tc)['equity'].iloc[-1]
E('l6', 'screens[6].feedback.correct', round(cost250, 2))
o250 = g8['orders_from_targets'](t250)
f250 = g8['fill_at_next_open'](o250, b250)
q250 = o250[o250 != 0].iloc[:len(f250)].values
two('l6 £62,274.03: engine gap vs sum of trade_cost over the fills', cost250, sum(tc(q, p) for q, p in zip(q250, f250.values)), 1e-6)
spread250 = sum(abs(q) * p * 2e-4 for q, p in zip(q250, f250.values))
claim('l6 screens[6] "most of it spread"', spread250 > cost250 / 2)
nst = g6['net_sharpe_table'](make_bars(500), [1, 2], [0.0, 2.5, 10.0]).values.tolist()
claim('l6 screens[7] example table', nst == J('l6', 'screens[7].widget.examples[0].expect') if isinstance(J('l6', 'screens[7].widget.examples[0].expect'), list) else nst == eval(J('l6', 'screens[7].widget.examples[0].expect')))

# ---------- l7 ----------
book = [(2000, 100.02), (2500, 100.03), (1500, 100.05)]
paid = sum(q * p for q, p in book)
avg = paid / 6000
E('l7', 'screens[0].explain.text', round(paid))
E('l7', 'screens[0].widget.answer', round(avg, 4))
E('l7', 'screens[0].widget.wrong[1].value', round((100.02 + 100.03 + 100.05) / 3, 4))
E('l7', 'screens[1].widget.answer', round((avg - 100.02) / 100 * 1e4, 4))
E('l7', 'screens[1].widget.wrong[0].value', round((avg - 100.00) / 100 * 1e4, 4))
E('l7', 'screens[1].widget.wrong[1].value', round(avg - 100.02, 4))
sb = g7['slippage_bp']
E('l7', 'screens[2].widget.answer', round(sb(20_000, 2_000_000, 0.012), 6))
two('l7 12 bp by hand', sb(20_000, 2_000_000, 0.012), 0.012 * math.sqrt(0.01) * 1e4)
E('l7', 'screens[2].widget.wrong[0].value', 0.012 * 0.01 * 1e4)
E('l7', 'screens[3].widget.answer', round(sb(2_000_000, 2_000_000, 0.012), 6))
E('l7', 'screens[3].widget.wrong[0].value', 0.012 * 1 * 1e4 * 10)        # linear in size: 100 x 12
claim('l7 screens[3] £1m book at £100: flip 20,000; £100m: 2,000,000', (2 * 1e6 / 100, 2 * 1e8 / 100) == (20_000, 2_000_000))
flip_share = int((o1.abs() == 20_000).sum()) / (len(b) - 1)
claim('lookback 1 flips on 48.6% of days (612 of 1,259)', round(flip_share, 3) == 0.486)
stated('l7', 'screens[3].prose', 'most days', False)
claim('l7 screens[3] prose says about every other day (flips on 48.6% of days)', 'about every other day' in lv.text('l7', 'screens[3].prose') and 0.45 < flip_share < 0.55)
E('l7', 'screens[4].widget.answer', 300_000 - g7['capped_qty'](300_000, 2_000_000))
s1k, s400k = sb(1000, 2_000_000, 0.012), sb(400_000, 2_000_000, 0.012)
E('l7', 'screens[5].explain.text', round(s1k / 1e4 * 100 * 100, 1))      # 2.7p
E('l7', 'screens[5].explain.text', round(s400k / 1e4 * 100 * 100, 1))    # 53.7p
E('l7', 'screens[5].widget.options[3].text', round(400 * s1k / 1e4 * 100, 2))   # £10.73
E('l7', 'screens[5].widget.options[1].why', round(s400k, 1))
stated('l7', 'screens[5].feedback.correct', 'understates it 50 times', round(s400k / 1.0) in range(50, 55))
E('l7', 'screens[8].canvas.params.rows[1][3]', round(sb(200_000, 2_000_000, 0.012)))   # 38 bp
cost = 0.015 * math.sqrt(2 / 40) * 2e6
E('l7', 'screens[9].widget.answer', round(cost, 1))
E('l7', 'screens[9].widget.wrong[0].value', 0.015 * (2 / 40) * 2e6)
E('l7', 'screens[9].widget.wrong[1].value', round(0.015 * math.sqrt(0.05) * 1e4, 2))
cap = J('l7', 'screens[10].canvas.params.rows')
for i, scale in enumerate((0.01, 0.03, 0.1, 0.3, 1, 10)):
    e = g7['backtest_with_impact'](b, tg2, 1_000_000, scale)['equity']
    ef = g7['backtest_with_impact'](b, tg2, 1_000_000, scale, c=0.0)['equity']
    claim(f'l7 screens[10] capacity row {cap[i][0]}', (f'{eng_sharpe(ef, 1e6 * scale):.2f}', f'{eng_sharpe(e, 1e6 * scale):.2f}'.replace('-', '−')) == (cap[i][1], cap[i][2]))
# finding 14: the engine has no cap, so the prose must not say it does; its largest test book flips about 10% of volume
claim('l7 backtest_with_impact never calls capped_qty', 'capped_qty' not in J('l7', 'screens[8].widget.solution'))
claim('l7 screens[4] says a careful engine caps, not our engine', 'Our engine caps' not in lv.text('l7', 'screens[4].prose') and 'A careful engine caps' in lv.text('l7', 'screens[4].prose'))
claim('l7 screens[8] prose says the engine leaves the cap out', 'leaves the cap out' in lv.text('l7', 'screens[8].prose'))
claim('l7 screens[8] largest test book (10 x the base 10,000 shares) flips 200,000 shares, 10% of 2,000,000', (2 * 10 * 10_000, 2 * 10 * 10_000 / 2_000_000) == (200_000, 0.1))
E('l7', 'screens[8].prose', 200_000)
claim('l7 summary.ideas[2] says a cap carries the rest', 'carries the rest' in lv.text('l7', 'summary.ideas[2]') and 'Our engine' not in lv.text('l7', 'summary.ideas[2]'))
claim('l7 screens[4] explain sets order as target minus shares held', 'target minus the shares actually held' in lv.text('l7', 'screens[4].explain.text'))
E('l7', 'screens[0].explain.text', round(avg, 4))
claim('l7 screens[0] average is 1.17p over the best ask (just over a penny); the last shares paid 3p over', (round((avg - 100.02) * 100, 2), round((100.05 - 100.02) * 100)) == (1.17, 3) and 'just over a penny' in lv.text('l7', 'screens[0].explain.text'))
claim('l7 screens[10] prose says in-sample: the same five years', 'these same five years' in lv.text('l7', 'screens[10].prose'))
E('l7', 'quiz[1].explain.text', 1.5)
E('l7', 'quiz[1].explain.text', 2_000_000)
E('l7', 'quiz[0].widget.answer', round(sb(50_000, 1_000_000, 0.02), 2))
E('l7', 'quiz[0].widget.wrong[0].value', 0.02 * 0.05 * 1e4)
E('l7', 'quiz[2].widget.answer', g7['capped_qty'](-250_000, 1_500_000))
E('l7', 'quiz[3].widget.answer', 1200 * 4 ** 1.5)
E('l7', 'quiz[3].widget.wrong[1].value', 1200 * 2)
claim('l7 quiz[1]: our square-root model still charges a 300-share order about 1.5 bp at V = 2,000,000', round(sb(300, 2_000_000, 0.012), 1) == 1.5)
e250 = [round(float(g7['backtest_with_impact'](b250, t250, 1_000_000, s)['equity'].iloc[-1]), 2) for s in (0.1, 1)]
claim('l7 screens[8] make_bars(250) final equity £77,672.56 and £572,005.40', e250 == [77672.56, 572005.4])

# ---------- l8 ----------
hon, sca, pk = g8['honest_engine'](b), g8['scaled_engine'](b), g8['peek_engine'](b)
E('l8', 'screens[0].prose', round(eng_sharpe(hon.equity), 2))
claim('l8 screens[0] honest and scaled Sharpes agree to 2 places', round(eng_sharpe(hon.equity), 2) == round(eng_sharpe(sca.equity), 2))
E('l8', 'screens[2].widget.options[1].why', round(eng_sharpe(pk.equity), 2))
E('l8', 'screens[6].explain.text', round(eng_sharpe(pk.equity), 2))
claim('l8 screens[1] row 599 is Tue 20 April 2021', b.index[599].date() == dt.date(2021, 4, 20) and b.index[599].weekday() == 1)
cut = g8['peek_engine'](b.iloc[:600])
rows1 = J('l8', 'screens[1].canvas.params.rows')
fmt = lambda x: f'{int(x):,}'.replace('-', '−')
kfmt = lambda x: ('0' if int(x) == 0 else f'{int(x) // 1000}k').replace('-', '−')    # shares in thousands
dfmt = lambda i: f"{b.index[595 + i].day} {b.index[595 + i].strftime('%b')}"                       # '14 Apr', no weekday
claim('l8 screens[1] table (dates without weekday, shares in thousands)', [[dfmt(i), fmt(pk.target.iloc[595 + i]), fmt(cut.target.iloc[595 + i]), kfmt(pk.shares.iloc[595 + i]), kfmt(cut.shares.iloc[595 + i])] for i in range(5)] == rows1)
claim('l8 screens[2] table is the same as screens[1]', J('l8', 'screens[2].canvas.params.rows') == rows1)
vf, v6 = b.close.pct_change().std(), b.close.iloc[:600].pct_change().std()
E('l8', 'screens[3].hints[1].text', round(vf * 100, 3))
E('l8', 'screens[3].hints[1].text', round(v6 * 100, 3))
E('l8', 'screens[3].explain.text', round(0.005 / vf * 10_000))
E('l8', 'screens[3].explain.text', round(0.005 / v6 * 10_000))
scut = g8['scaled_engine'](b.iloc[:600])
rows3 = J('l8', 'screens[3].canvas.params.rows')
money = lambda x: f'{x / 1000:,.1f}'                                                              # equity in £k
claim('l8 screens[3] table (dates without weekday, equity in £k)', [[dfmt(i), fmt(sca.target.iloc[595 + i]), fmt(scut.target.iloc[595 + i]), money(sca.equity.iloc[595 + i]), money(scut.equity.iloc[595 + i])] for i in range(5)] == rows3)
claim('l8 screens[3] equity column headers are in £k', J('l8', 'screens[3].canvas.params.columns')[3:] == ['Equity (all, £k)', 'Equity (cut, £k)'])
# finding 18: engine B fails both forms of the check (the cut form and the noise form), singly
_full = g8['scaled_engine'](b).iloc[:250]
_cutrun = g8['scaled_engine'](b.iloc[:250])
_noisy = g8['scaled_engine'](g8['noise_after'](b, 250)).iloc[:250]
_close = lambda x, y: x.shape == y.shape and bool(np.allclose(x.to_numpy(float), y.to_numpy(float), rtol=0, atol=1e-9))
claim('l8 screens[3] engine B fails the cut form and the noise form', (not _close(_cutrun, _full)) and (not _close(_noisy, _full)))
claim('l8 screens[3] prose says it shows the cut form and that B fails both', 'cut form' in lv.text('l8', 'screens[3].prose') and 'fails both forms' in lv.text('l8', 'screens[3].prose'))
claim('l8 screens[0] prose: engine B holds 10,000 x 0.005 / vol shares', '10{,}000 \\times 0.005' in J('l8', 'screens[0].prose') and 4000 < round(0.005 / vf * 10_000) < 4200)
claim('l8 screens[9] the right option no longer needs "it says what it does not cover"', 'A complete one also says what it does not cover' in lv.text('l8', 'screens[9].explain.text'))
claim('l8 screens[4] lookahead_check: honest True, peek and scaled False at 250',
      (g8['lookahead_check'](g8['honest_engine'], make_bars(500), 250), g8['lookahead_check'](g8['peek_engine'], make_bars(500), 250), g8['lookahead_check'](g8['scaled_engine'], make_bars(500), 250)) == (True, False, False))

# ---------- review-2 ----------
E('review', 'items[0].widget.answer', 500 * 48.30)
E('review', 'items[0].widget.wrong[0].value', 500 * 48.90)
E('review', 'items[1].widget.answer', tc(800, 60.0, half_spread_bp=3.0))
E('review', 'items[1].widget.wrong[0].value', tc(800, 60.0, half_spread_bp=6.0))
E('review', 'items[1].widget.wrong[1].value', round(1 + 48_000 * 3e-4, 2))
# review-2 items[2] and items[5]: fresh setups (new values only, so a revert to the l7 copies fails)
claim('review-2 items[2] is 72,000 shares on 800,000 a day, 1.5%', all(s in lv.text('review', 'items[2].prose') for s in ('72,000', '800,000', '1.5%')))
E('review', 'items[2].widget.answer', round(sb(72_000, 800_000, 0.015), 6))         # 45 bp
claim('review-2 items[2] answer is exactly 45', J('review', 'items[2].widget.answer') == 45)
E('review', 'items[2].widget.wrong[0].value', round(0.015 * 0.09 * 1e4, 6))         # 13.5, no root
E('review', 'items[2].widget.wrong[1].value', round(0.015 * math.sqrt(9) * 1e4, 6))  # 450, 9 for Q/V
E('review', 'items[2].explain.text', 0.09)
E('review', 'items[2].explain.text', 0.3)
E('review', 'items[2].explain.text', 0.0045)
left1 = 180_000 - g7['capped_qty'](180_000, 1_200_000)
claim('review-2 items[5] is a buy of 180,000 on 1,200,000 then 400,000', all(s in lv.text('review', 'items[5].prose') for s in ('180,000', '1,200,000', '400,000')))
E('review', 'items[5].widget.answer', left1 - g7['capped_qty'](left1, 400_000))     # 20,000
claim('review-2 items[5] answer is exactly 20,000', J('review', 'items[5].widget.answer') == 20000)
E('review', 'items[5].widget.wrong[0].value', left1)                                 # 60,000
E('review', 'items[5].explain.text', g7['capped_qty'](180_000, 1_200_000))
E('review', 'items[5].explain.text', g7['capped_qty'](left1, 400_000))
E('review', 'items[5].explain.text', left1)
claim('review-2 items[5] does not say the engine caps fills', 'The engine caps' not in lv.text('review', 'items[5].prose'))
# review-2 items[3]: a late leak passes early cuts (finding 35)
claim('review-2 items[3] late_engine passes lookahead_check at cuts 100 and 200 on 400 bars', all(g8['lookahead_check'](g8['late_engine'], make_bars(400), c_) for c_ in (100, 200)))
claim('review-2 items[3] late_engine fails at a cut after row 300', not g8['lookahead_check'](g8['late_engine'], make_bars(400), 350))
claim('review-2 items[3] options are pass, fail, noise', [o_['id'] for o_ in J('review', 'items[3].widget.options')] == ['pass', 'fail', 'noise'])
E('review', 'items[6].widget.answer', (120_000 - 20_000) / 400e6 * 1e4)
E('review', 'items[6].widget.wrong[0].value', 120_000 / 400e6 * 1e4)
E('review', 'items[8].prose', round(honest, 2))
E('review', 'items[8].prose', round(leak, 2))
stated('review', 'items[8].prose', 'The engine, filling at the next open, gives 0.57', False)
E('review', 'items[8].prose', round(sweep[5], 2))
claim('review-2 items[8] says the vectorised rule filled at the next open', 'same vectorised rule' in lv.text('review', 'items[8].prose'))

# ---------- homework-2 ----------
E('homework', 'items[1].feedback.byKey', 400 * 5 // 6)
claim('homework-2 items[1] cuts on 400 bars', [k * 400 // 6 for k in range(1, 6)] == [66, 133, 200, 266, 333])
claim('homework-2 items[1] leaky_or_not(late_engine, make_bars(600)) = 400', gl['leaky_or_not'](gl['late_engine'], make_bars(600)) == 400)
E('homework', 'items[3].widget.answer', 5000 * 0.80)
imp = sb(20_000, 2_000_000, 0.012)
moved = 100 * (1 + imp / 1e4)
tot = 20_000 * (moved - 100) + tc(20_000, moved)
E('homework', 'items[4].widget.answer', round(tot, 2))
E('homework', 'items[4].explain.text', round(20_000 * moved, 2))
E('homework', 'items[4].explain.text', round(20_000 * moved * 2e-4, 2))
E('homework', 'items[4].widget.wrong[0].value', tc(20_000, 100.0))
E('homework', 'items[4].widget.wrong[1].value', round(20_000 * (moved - 100) + tc(20_000, 100.0), 2))
q5 = (6 / (0.012 * 1e4)) ** 2 * 2_000_000
E('homework', 'items[5].widget.answer', round(q5))
E('homework', 'items[5].widget.wrong[1].value', 0.025 * 2_000_000)
E('homework', 'items[5].explain.text', round(q5 / 2 * 100))                 # book £250,000
lin = 6 / (0.012 * 1e4) * 2_000_000
claim('homework-2 items[5] the linear slip is 100,000 and byKey is keyed linear', J('homework', 'items[5].widget.wrong[0].value') == lin == 100_000 and J('homework', 'items[5].widget.wrong[0].id') == 'linear' and 'half' not in J('homework', 'items[5].feedback.byKey'))
E('homework', 'items[5].feedback.byKey.linear', lin)
E('homework', 'items[5].feedback.byKey.linear', 0.05)
q_all = 0.02 * math.sqrt(50 / 20)
q_cap = 0.02 * math.sqrt(0.1)
E('homework', 'items[7].widget.model', round(q_all * 1e4))
E('homework', 'items[7].widget.model', round(q_all * 50, 2))                # £1.58m
E('homework', 'items[7].widget.model', round(q_cap * 1e4))
E('homework', 'items[7].widget.model', round(q_cap * 50e6 / 1e3))           # £316k
E('homework', 'items[7].widget.model', 50 / 2)                              # 25 days
claim('homework-2 items[7] prompt or question states the £50m order and £20m volume',
      '50m' in lv.text('homework', 'items[7].widget.prompt') + lv.text('homework', 'items[7].question'))
rep = gh['execution_report'](b250, t250, 1_000_000, 0.005, 2.0, 1.0)
claim('homework-2 items[0] impact is the largest part on make_bars(250)', rep['impact_cost'] > max(rep['spread_cost'], rep['commission']))
two('homework-2 items[0] parts add up', rep['gross_pnl'] - rep['net_pnl'], rep['commission'] + rep['spread_cost'] + rep['impact_cost'], 1e-6)

lv.check_wrongs()
lv.report()
