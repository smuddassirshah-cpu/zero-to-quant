"""Recompute every number and printed output stated in numpy-pandas level 3 (Time series and groups): l9 to l13,
review-3, homework-3. Second read (session V).
Run: python3 docs/reports/numpy-pandas-L3-numbers.py   (needs numpy and pandas 2.2 or later for "ME"; exits 0 when every check passes)
Numbers are computed twice where a second route exists (by hand and by pandas); snippets are executed and compared with
the keyed option. `lv.claim_text` ties a claim to its wording: it fails while a false sentence is in the text and passes
once it is reworded. Checks that fail on the current content are findings in docs/reviews/review-numpy-pandas-1-3.md.
"""
import sys, os, io, math, contextlib, warnings
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("numpy-pandas", 3)
E = lv.expect
C = lv.claim
warnings.simplefilter('ignore', FutureWarning)


def run(code):
    out = io.StringIO()
    g = {'np': np, 'pd': pd, 'io': io}
    try:
        with contextlib.redirect_stdout(out):
            exec(code, g)
        return out.getvalue(), None
    except Exception as e:
        return out.getvalue(), type(e).__name__ + ': ' + str(e)


def norm(s):
    return ' '.join(s.replace('`', '').split())


def prints(fid, path, code, label=None, want=None):
    txt, err = run(code)
    want = norm(want if want is not None else lv.text(fid, path))
    C(err is None and norm(txt) == want, label or f'{fid} {path} prints {want!r}', f'printed {txt!r} err {err}')


def two(label, a, b, tol=1e-9):
    C(abs(a - b) <= tol * max(1, abs(a)), f'two routes agree: {label} ({a!r})', f'{a!r} vs {b!r}')


D5 = pd.to_datetime(['2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08'])
c5 = pd.Series([12.55, 12.31, 12.48, 12.62, 12.44], index=D5)

# ---------------------------------------------------------------- l9-returns-with-shift
C(c5.shift(1).loc['2024-03-06'] == 12.31, 'l9 screens[0]: prev on 6 March is 12.31')
E('l9', 'screens[1].widget.answer', int(c5.shift(2).isna().sum()))
r = c5 / c5.shift(1) - 1
E('l9', 'screens[2].widget.answer', round(float(r.loc['2024-03-06']), 4))
two('6 March simple return', float(r.loc['2024-03-06']), 12.48 / 12.31 - 1)
E('l9', 'screens[2].widget.wrong[0].value', round(12.31 / 12.48 - 1, 4))
E('l9', 'screens[2].widget.wrong[1].value', round(12.48 - 12.31, 2))
E('l9', 'screens[2].widget.wrong[2].value', round(float(r.loc['2024-03-07']), 4))
C(np.allclose(r.dropna(), c5.pct_change().dropna()), 'l9 screens[2] explain: pct_change computes exactly this column')
lr = np.log(c5 / c5.shift(1))
for i, v in enumerate([-0.019309, 0.013715, 0.011155, -0.014366]):
    two(f'log return {i + 1}', round(float(lr.iloc[i + 1]), 6), v)
prints('l9', 'screens[3].widget.options[0].text', 'import numpy as np\nc = pd.Series([12.55, 12.31, 12.48, 12.62, 12.44])\nlr = np.log(c / c.shift(1))\nprint(round(lr.sum(), 6))')
two('sum of logs', float(lr.sum()), math.log(12.44 / 12.55))
E('l9', 'screens[3].widget.options[2].text', round(12.44 / 12.55 - 1, 6))
E('l9', 'screens[3].widget.options[3].text', round(float(r.sum()), 6))
a = c5.pct_change().loc['2024-03-05':'2024-03-07']
b = c5.loc['2024-03-05':'2024-03-07'].pct_change()
C(int(a.isna().sum()) == 0 and int(b.isna().sum()) == 1, 'l9 screens[4]: a has 0 NaN and b has 1')
rev = c5.iloc[::-1]
rr = rev.pct_change()
E('l9', 'screens[5].widget.options[0].text', round(float(rr.loc['2024-03-07']), 6))
two('backwards return', float(rr.loc['2024-03-07']), 12.62 / 12.44 - 1)
E('l9', 'screens[5].widget.options[1].text', round(12.62 / 12.48 - 1, 6))
E('l9', 'screens[5].widget.options[3].text', round(12.44 / 12.62 - 1, 6))
fwd = c5.shift(-1) / c5 - 1
two('shift(-1) return on 5 March', float(fwd.loc['2024-03-05']), 12.48 / 12.31 - 1)
E('l9', 'screens[7].explain.text', round(float(r.loc['2024-03-06']), 6))
E('l9', 'screens[7].explain.text', round(float(lr.loc['2024-03-06']), 6))
v2 = pd.Series([12.70, 12.44, 12.62, 12.48], index=pd.to_datetime(['2024-3-11', '2024-3-8', '2024-3-7', '2024-3-6']))
C(v2.sort_index().pct_change().dropna().round(6).tolist() == [0.011218, -0.014263, 0.0209], 'l9 screens[8] example 2: 0.011218, -0.014263, 0.0209')
C(sorted(['2024-3-11', '2024-3-8'])[0] == '2024-3-11', 'l9 screens[8] byKey test-3: as text 2024-3-11 sorts before 2024-3-8')
t2 = pd.Series([50.00, 55.00, 49.50, 54.45])
E('l9', 'screens[9].explain.text', round(float(np.log(t2 / t2.shift(1)).sum()), 4))
two('ln(54.45/50)', float(np.log(t2 / t2.shift(1)).sum()), math.log(54.45 / 50))
sig = pd.Series([1, 0, 1, 1, 0], index=D5)
pnl = (10000 * sig.shift(1) * c5.pct_change()).dropna().round(2)
C(pnl.tolist() == [-191.24, 0.0, 112.18, -142.63], 'l9 screens[10]: P&L -191.24, 0.0, 112.18, -142.63')
E('l9', 'screens[10].feedback.byKey.test-1', round(float(10000 * c5.pct_change().loc['2024-03-06']), 2))
E('l9', 'screens[10].explain.text', round(10000 * (12.31 / 12.55 - 1), 2))
prints('l9', 'quiz[0].widget.options[0].text', 's = pd.Series([10.00, 11.00, 12.10])\nprint(s.shift(1).tolist())')
prints('l9', 'quiz[0].widget.options[1].text', 's = pd.Series([10.00, 11.00, 12.10])\nprint(s.shift(-1).tolist())', 'l9 quiz[0] up option is shift(-1)')
E('l9', 'quiz[1].widget.answer', round(math.log(55 / 50), 4))
E('l9', 'quiz[1].widget.wrong[0].value', 55 / 50 - 1)
C(all(math.log(1 + x) < x for x in (0.001, 0.1, 0.5)), 'l9 quiz[1] explain: a log return is below the simple return on a rise')
# quiz[2] neg why compares the backwards 7 March value with minus 7 March's true return; the sign flip on a newest-first
# frame should be compared with the true return of the later day, 8 March
lv.claim_text('l9', 'quiz[2].widget.options[3].why', '12.62 / 12.44 − 1 is not −(12.62 / 12.48 − 1)', False,
              'l9 quiz[2] neg why: compares two unrelated numbers; the flipped value on 7 March is '
              f'{-(12.62 / 12.44 - 1):.6f}, 8 March\'s true return is {12.44 / 12.62 - 1:.6f}')

# ---------------------------------------------------------------- l10-rolling
D12 = pd.to_datetime(['2024-04-02', '2024-04-03', '2024-04-04', '2024-04-05', '2024-04-08', '2024-04-09', '2024-04-10',
                      '2024-04-11', '2024-04-12', '2024-04-15', '2024-04-16', '2024-04-17'])
c12 = pd.Series([12.40, 12.55, 12.31, 12.48, 12.62, 12.44, 12.70, 12.85, 12.66, 12.90, 13.05, 12.98], index=D12)
ma3 = c12.rolling(3).mean()
can = lv.files['l10-rolling']['screens'][0]['canvas']['params']['series'][1]['values']
C(np.allclose(ma3.round(4).tolist()[2:], can[2:]), 'l10 screens[0] canvas: the 3-day mean line')
E('l10', 'screens[1].widget.answer', round(float(ma3.loc['2024-04-08']), 2))
two('12.47', float(ma3.loc['2024-04-08']), (12.31 + 12.48 + 12.62) / 3)
E('l10', 'screens[1].widget.wrong[0].value', round(float(ma3.loc['2024-04-05']), 4))
E('l10', 'screens[1].widget.wrong[1].value', round(float(c12.rolling(3, center=True).mean().loc['2024-04-08']), 4))
E('l10', 'screens[1].widget.wrong[2].value', round((12.48 + 12.62) / 2, 2))
# hint: "The mean line only moves a third as far as the price on any day" -- the mean moves (p_t - p_{t-3}) / 3
dm, dp = ma3.diff(), c12.diff()
third = bool(np.allclose((dm / dp).dropna().iloc[1:], 1 / 3))
lv.claim_text('l10', 'screens[0].hints[1].text', 'only moves a third as far as the price on any day', third,
              f'l10 screens[0] hint: on 9 April the price moves {dp.loc["2024-04-09"]:+.2f} and the mean {dm.loc["2024-04-09"]:+.4f}')
lv.claim_text('l10', 'screens[0].widget.options[2].why', 'the mean moves by a third of it', abs(dm.loc['2024-04-10'] - dp.loc['2024-04-10'] / 3) < 0.005,
              f'l10 screens[0] same why: on 10 April the price jumps {dp.loc["2024-04-10"]:.2f}, the mean {dm.loc["2024-04-10"]:.4f}, not a third ({dp.loc["2024-04-10"] / 3:.4f})')
ma5 = c12.rolling(5).mean()
E('l10', 'screens[2].widget.answer', int(ma5.isna().sum()))
can5 = lv.files['l10-rolling']['screens'][2]['canvas']['params']['series'][1]['values']
C(np.allclose(ma5.round(4).tolist()[4:], can5[4:]), 'l10 screens[2] canvas: the 5-day mean line')
E('l10', 'screens[2].widget.wrong[2].value', int(ma5.notna().sum()))
vol3 = c12.pct_change().rolling(3).std()
E('l10', 'screens[3].widget.options[0].text', int(vol3.isna().sum()))
vol5 = c12.pct_change().rolling(5).std()
canv = lv.files['l10-rolling']['screens'][4]['canvas']['params']['series'][0]['values']
C(np.allclose(vol5.round(6).tolist()[5:], canv[5:]), 'l10 screens[4] canvas: the 5-day vol line')
last = float(vol5.iloc[-1])
E('l10', 'screens[4].widget.answer', round(last * math.sqrt(252), 4))
E('l10', 'screens[4].widget.wrong[0].value', round(0.013987 * 252, 4))   # from the shown 0.013987 (exact vol gives 3.5246)
C(abs(last * 252 - 3.5247) < 0.002, 'l10 screens[4] wrong times252 within its tolerance of the exact product')
E('l10', 'screens[4].widget.wrong[1].value', round(last * math.sqrt(12), 4))
E('l10', 'screens[4].widget.wrong[2].value', round(last * math.sqrt(365), 4))
E('l10', 'screens[4].hints[2].text', round(math.sqrt(252), 3))
ret = c12.pct_change()
pos = (c12 > ma3).astype(int)
same, lag = float((pos * ret).sum()), float((pos.shift(1) * ret).sum())
E('l10', 'screens[5].explain.text', round(same, 4), fmt='{:.4f}')
E('l10', 'screens[5].explain.text', round(lag, 4), fmt='{:.4f}')
E('l10', 'screens[9].explain.text', round(lag, 6))
E('l10', 'screens[9].explain.text', round(same, 5))
tab = lv.files['l10-rolling']['screens'][5]['canvas']['params']['rows']
for row in tab:
    dte = row[0]
    C(abs(float(row[2]) - ma3.loc[dte]) < 6e-5 and int(row[3]) == pos.loc[dte] and abs(float(row[4].replace('−', '-')) - ret.loc[dte]) < 6e-7,
      f'l10 screens[5] table row {dte}')
E('l10', 'screens[6].widget.options[0].text', 30 - 19)
C(int(pd.Series(np.arange(30.0)).rolling(20).mean().notna().sum()) == 11, 'l10 screens[6]: 11 values of 30 are not NaN')
vf = (c12.pct_change().rolling(5).std() * np.sqrt(252)).round(4)
C(vf.dropna().tolist() == [0.2546, 0.2852, 0.2127, 0.2608, 0.2812, 0.2271, 0.222], 'l10 screens[8] example')
E('l10', 'screens[8].feedback.byKey.test-1', round(float(vol5.dropna().iloc[0]), 3))
C(3.5 < float(vol5.dropna().iloc[0] * 252) < 4.5, 'l10 screens[8] byKey: times 252 gives values near 4')
C(float((pos * ret).loc['2024-04-05']) > 0 and round(float(ret.loc['2024-04-05']), 5) == 0.01381, 'l10 screens[9] byKey test-1: a same-day signal gains 0.01381 on 5 April')
prints('l10', 'quiz[0].widget.options[0].text', 's = pd.Series([1.0, 2.0, 3.0, 4.0])\nprint(s.rolling(2).mean().tolist())')
E('l10', 'quiz[1].widget.answer', round(0.015 * math.sqrt(252), 4))
E('l10', 'quiz[1].widget.wrong[0].value', round(0.015 * 252, 2))
E('l10', 'quiz[1].widget.wrong[1].value', round(0.015 * math.sqrt(365), 4))
prints('l10', 'quiz[2].widget.options[0].text', 's = pd.Series([1.0, 2.0, 3.0, 4.0])\nprint(s.rolling(3, min_periods=1).mean().tolist())')

# ---------------------------------------------------------------- l11-daily-to-monthly
D9 = pd.to_datetime(['2024-01-30', '2024-01-31', '2024-02-01', '2024-02-02', '2024-02-28', '2024-02-29', '2024-03-01', '2024-03-27', '2024-03-28'])
c9 = pd.Series([12.22, 12.05, 12.18, 12.31, 12.40, 12.25, 12.40, 12.71, 12.66], index=D9)
v9 = pd.Series([16100, 18300, 14900, 15600, 17300, 15200, 16900, 14200, 19800], index=D9)
C(c9.resample('ME').last().loc['2024-02'].iloc[0] == 12.25, 'l11 screens[0]: February stands at 12.25')
C(pd.Timestamp('2024-03-31').day_name() == 'Sunday' and str(c9.resample('ME').last().index[2])[:10] == '2024-03-31', 'l11 screens[1]: March bucket labelled Sunday 31 March')
C(pd.Timestamp('2024-03-29').day_name() == 'Friday', 'l11 screens[1] explain: 29 March 2024 is a Friday (Good Friday)')
vm = v9.resample('ME').sum()
E('l11', 'screens[2].widget.answer', int(vm.loc['2024-02'].iloc[0]))
two('63000', float(vm.loc['2024-02'].iloc[0]), 14900 + 15600 + 17300 + 15200)
E('l11', 'screens[2].widget.wrong[1].value', float(v9.resample('ME').mean().loc['2024-02'].iloc[0]))
E('l11', 'screens[2].widget.wrong[2].value', int(v9.sum()))
mm = c9.resample('ME').mean()
E('l11', 'screens[4].prose', round(float(mm.pct_change().loc['2024-02'].iloc[0]), 4))
E('l11', 'screens[4].widget.answer', round(12.25 / 12.05 - 1, 4))
E('l11', 'screens[4].widget.accept', round(12.25 / 12.05 - 1, 6))
E('l11', 'screens[4].widget.wrong[2].value', round(12.05 / 12.25 - 1, 4))
E('l11', 'screens[4].feedback.byKey.mean', round(float(mm.loc['2024-02'].iloc[0]), 3))
E('l11', 'screens[4].feedback.byKey.mean', round(float(mm.loc['2024-01'].iloc[0]), 3))
# the "first" slip: 0.0108 is 12.18 / 12.05 - 1 (ending at February's first close), not starting from it (12.25 / 12.18 - 1)
fv = lv.files['l11-daily-to-monthly']['screens'][4]['widget']['wrong'][1]['value']
two('first slip value', fv, round(12.18 / 12.05 - 1, 4))
lv.claim_text('l11', 'screens[4].feedback.byKey.first', 'You started from February\'s first close', abs(fv - (12.25 / 12.18 - 1)) < 6e-5,
              f'l11 screens[4] byKey.first: 0.0108 ends at February\'s first close; starting from it gives {12.25 / 12.18 - 1:.4f}')
C(c9.resample('ME').last().notna().sum() == 3, 'l11 screens[5] analogue')
s5 = pd.Series([10.00, 11.00], index=pd.to_datetime(['2024-01-31', '2024-03-28'])).resample('ME').last()
C(len(s5) == 3 and pd.isna(s5.iloc[1]), 'l11 screens[5]: three rows, NaN for February')
lv.claim_text('l11', 'screens[7].feedback.byKey.test-1', '12.13 or 12.29', round(float(mm.iloc[0]), 2) == 12.13 and round(float(mm.iloc[1]), 2) == 12.29,
              f'l11 screens[7] byKey test-1: monthly means are {mm.iloc[0]:.3f} and {mm.iloc[1]:.3f}; 12.135 rounds to {round(float(mm.iloc[0]), 2)} in floats')
E('l11', 'screens[7].feedback.byKey.test-1', float(c9.resample('ME').first().iloc[0]))
op = pd.Series([12.30, 12.20, 12.07, 12.20, 12.33, 12.41, 12.27, 12.60, 12.70], index=D9)
hi = pd.Series([12.35, 12.24, 12.25, 12.36, 12.45, 12.43, 12.44, 12.75, 12.74], index=D9)
lo = pd.Series([12.18, 12.01, 12.04, 12.15, 12.30, 12.20, 12.25, 12.58, 12.62], index=D9)
feb = (op.resample('ME').first().iloc[1], hi.resample('ME').max().iloc[1], lo.resample('ME').min().iloc[1], c9.resample('ME').last().iloc[1])
C(feb == (12.07, 12.45, 12.04, 12.25), 'l11 screens[3] explain: February bar 12.07, 12.45, 12.04, 12.25')
me = c9.resample('ME').last()
C(me.pct_change().dropna().round(6).tolist() == [0.016598, 0.033469], 'l11 screens[9] example')
E('l11', 'quiz[2].widget.answer', 52 / 50 - 1)
E('l11', 'quiz[2].widget.wrong[0].value', round(51.5 / 50 - 1, 2))
C(len(pd.Series(1.0, index=pd.bdate_range('2024-01-02', '2024-06-28')).resample('ME').last()) == 6, 'l11 quiz[0]: six month ends')
uk = pd.bdate_range('2024-01-02', '2024-06-28').difference(pd.to_datetime(['2024-03-29', '2024-04-01', '2024-05-06', '2024-05-27']))
C(abs(len(uk) - 124) <= 3, f'l11 quiz[0] days wrong: {len(uk)} London trading days, within 3 of 124')

# ---------------------------------------------------------------- l12-split-apply-combine
L12 = pd.DataFrame({'ticker': ['BARC', 'VOD', 'AZN'] * 3, 'ret': [-1.2, 0.5, 0.8, 1.5, 0.1, -0.4, 0.6, -0.9, 1.1]})
gm = L12.groupby('ticker')['ret'].mean()
E('l12', 'screens[1].widget.answer', round(float(gm['BARC']) / 100, 6))
E('l12', 'screens[1].widget.wrong[0].value', round(float(L12['ret'].mean()) / 100, 6))
E('l12', 'screens[1].widget.wrong[1].value', round(float(L12[L12.ticker == 'BARC']['ret'].sum()) / 100, 6))
E('l12', 'screens[1].explain.text', round(float(gm['AZN']), 4))
E('l12', 'screens[1].explain.text', round(float(gm['VOD']), 4))
C(gm.index.tolist() == ['AZN', 'BARC', 'VOD'], 'l12 screens[2]: groupby sorts AZN, BARC, VOD')
E('l12', 'screens[2].widget.options[2].text', round(float(L12['ret'].mean()), 4))
L3 = L12.copy()
L3.loc[4, 'ret'] = np.nan
agg = L3.groupby('ticker')['ret'].agg(['mean', 'count', 'size']).loc['VOD']
C(round(agg['mean'], 4) == -0.2 and agg['count'] == 2 and agg['size'] == 3, 'l12 screens[3]: VOD -0.2, 2 and 3')
E('l12', 'screens[3].widget.options[1].text', round((0.5 - 0.9) / 3, 4))
wd = pd.Series([0.4, -0.2, 0.6, 0.1, -0.3, -0.8, 0.5, 0.2, 0.3, 0.7], index=pd.bdate_range('2024-03-04', periods=10))
wm = wd.groupby(wd.index.day_name()).mean()
E('l12', 'screens[4].widget.answer', round(float(wm['Monday']), 4))
E('l12', 'screens[4].widget.wrong[1].value', round(float(wd.mean()), 4))
stk = pd.DataFrame({'ticker': ['AZN'] * 3 + ['BARC'] * 3 + ['VOD'] * 3, 'close': [118.40, 119.35, 118.87, 2.15, 2.18, 2.16, 0.72, 0.71, 0.73]})
prints('l12', 'screens[5].widget.options[0].text', 'df = pd.DataFrame({"close": [118.40, 119.35, 118.87, 2.15, 2.18, 2.16, 0.72, 0.71, 0.73]})\n'
       'df["ret"] = df["close"].pct_change()\nprint(round(df.loc[3, "ret"], 4))')
E('l12', 'screens[5].widget.options[2].text', round(2.18 / 2.15 - 1, 4))
gr = stk.groupby('ticker')['close'].pct_change()
E('l12', 'screens[6].widget.answer', int(gr.isna().sum()))
E('l12', 'screens[6].explain.text', round(2.18 / 2.15 - 1, 4), fmt='{:.4f}')
E('l12', 'screens[7].widget.options[1].text', 250 * 4)
b3 = pd.Series([-0.012, 0.015, 0.006])
E('l12', 'screens[9].feedback.byKey.test-1', round(float(b3.std()), 6))
E('l12', 'screens[9].feedback.byKey.test-1', round(float(b3.std(ddof=0)), 6))
wc = pd.Series([50.00, 50.50, 50.00, 51.00, 51.51, 51.00, 50.49, 51.00, 51.51, 51.00, 52.02], index=pd.bdate_range('2024-06-07', periods=11))
wr = wc.pct_change()
C(wr.groupby(wr.index.day_name()).mean().round(6).to_dict() == {'Friday': 0.00505, 'Monday': 0.0, 'Thursday': 5e-05, 'Tuesday': 0.0001, 'Wednesday': 0.015},
  'l12 screens[10] example: weekday means')
prints('l12', 'quiz[0].widget.options[0].text', 't = pd.DataFrame({"ticker": ["VOD", "BARC", "VOD"], "qty": [300, 150, -100]})\nprint(t.groupby("ticker")["qty"].sum().tolist())')
yr = pd.Series(0.0, index=pd.bdate_range('2024-01-01', '2024-12-31'))
C(yr.groupby(yr.index.day_name()).mean().index[0] == 'Friday', 'l12 quiz[3]: Friday sorts first')

# ---------------------------------------------------------------- l13-joining-on-dates
ny = pd.DataFrame({'date': pd.to_datetime(['2024-03-26', '2024-03-27', '2024-03-28', '2024-04-01', '2024-04-02', '2024-04-03']), 'close': [38.40, 38.95, 39.10, 38.70, 39.25, 39.60]})
lon = pd.DataFrame({'date': pd.to_datetime(['2024-03-26', '2024-03-27', '2024-03-28', '2024-04-02', '2024-04-03']), 'close': [12.62, 12.70, 12.66, 12.80, 12.74]})
C(pd.Timestamp('2024-03-29').day_name() == 'Friday' and pd.Timestamp('2024-04-01').day_name() == 'Monday', 'l13 screens[0]: Good Friday 29 March, Easter Monday 1 April 2024')
E('l13', 'screens[0].widget.answer', len(set(ny.date) & set(lon.date)))
E('l13', 'screens[0].widget.wrong[1].value', len(ny) + len(lon))
ml = pd.merge(ny, lon, on='date', how='left', suffixes=('_ny', '_lon'))
C(pd.isna(ml.loc[ml.date == '2024-04-01', 'close_lon']).all(), 'l13 screens[1]: left join gives NaN on 1 April')
mi = pd.merge(ny, lon, on='date', suffixes=('_ny', '_lon'))
E('l13', 'screens[2].widget.answer', float(mi['close_lon'].iloc[3]))
E('l13', 'screens[2].widget.wrong[0].value', float(mi['close_ny'].iloc[3]))
E('l13', 'screens[2].widget.wrong[1].value', float(mi['close_lon'].iloc[2]))
q = ny.set_index('date')['close'] / lon.set_index('date')['close']
C(f'{len(q)} {int(q.isna().sum())}' == '6 1', 'l13 screens[3]: prints 6 1')
lg = pd.concat([ny.assign(ticker='NY'), lon.assign(ticker='LON')])
wide = lg.pivot(index='date', columns='ticker', values='close')
C(wide.shape == (6, 2) and int(wide.isna().sum().sum()) == 1, 'l13 screens[4]: 6 by 2 with 1 NaN')
tr = pd.DataFrame({'date': pd.to_datetime(['2024-03-27', '2024-03-28', '2024-04-02']), 'qty': [500, -200, 300]})
px = pd.DataFrame({'date': pd.to_datetime(['2024-03-26', '2024-03-27', '2024-04-02', '2024-04-03']), 'close': [12.62, 12.70, 12.80, 12.74]})
vv = pd.merge(tr, px, on='date')
E('l13', 'screens[5].widget.answer', len(vv))
C(int(vv.qty.sum()) - int(tr.qty.sum()) == 200, 'l13 screens[5] explain: the book looks 200 shares longer')
pts = np.array(lv.files['l13-joining-on-dates']['screens'][6]['canvas']['params']['points'])
E('l13', 'screens[6].widget.options[0].text', round(float(np.corrcoef(pts[:, 0], pts[:, 1])[0, 1]), 2))
C(round(float(pd.Series(pts[:, 0]).corr(pd.Series(pts[:, 1]))), 2) == 0.97, 'l13 screens[6]: pandas corr agrees, 0.97')
d10 = pd.bdate_range('2024-05-01', periods=10)
L10 = pd.DataFrame({'date': list(d10) * 3, 'ticker': ['AZN'] * 10 + ['BARC'] * 10 + ['XYZ'] * 10,
                    'close': [118.40, 120.11, 122.00, 121.53, 121.14, 121.45, 121.09, 120.80, 122.90, 122.51, 2.15, 2.16, 2.18, 2.17, 2.16, 2.19, 2.22, 2.22, 2.27, 2.23,
                              7.05, 6.98, 6.90, 6.92, 6.88, 6.88, 6.87, 6.86, 6.94, 7.03]})
W10 = L10.pivot(index='date', columns='ticker', values='close').sort_index()
rc, pcor = W10.pct_change().corr(), W10.corr()
C(rc.loc['AZN', 'BARC'] > 0.5 and rc.loc['AZN', 'XYZ'] < 0 and rc.loc['BARC', 'XYZ'] < 0, 'l13 screens[10] explain: AZN and BARC together, XYZ the other way')
offd = [pcor.loc['AZN', 'BARC'], pcor.loc['AZN', 'XYZ'], pcor.loc['BARC', 'XYZ']]
lv.claim_text('l13', 'screens[10].feedback.byKey.test-1', 'near 0.9 or above for every pair', all(x >= 0.85 for x in offd),
              f'l13 screens[10] byKey test-1: correlating test 1\'s closes gives {[round(x, 4) for x in offd]}, not near 0.9')
lv.claim_text('l13', 'screens[10].explain.text', 'prices of almost any two stocks look correlated', all(x >= 0.85 for x in offd),
              'l13 screens[10] explain: on this test the price correlations are 0.69, -0.31 and -0.15')
E('l13', 'screens[8].widget.examples[0].expect', 500 * 12.70)
E('l13', 'screens[8].feedback.byKey.test-2', 100 * 38.70)
E('l13', 'screens[8].feedback.byKey.test-2', 400 * 12.70)
E('l13', 'quiz[1].widget.answer', 5)
a7 = pd.DataFrame({'date': pd.to_datetime(['2024-07-01', '2024-07-02', '2024-07-03', '2024-07-04']), 'x': 1})
b7 = pd.DataFrame({'date': pd.to_datetime(['2024-07-02', '2024-07-03', '2024-07-04', '2024-07-05']), 'y': 1})
C(len(pd.merge(a7, b7, on='date', how='outer')) == 5 and len(pd.merge(a7, b7, on='date')) == 3, 'l13 quiz[1]: outer 5, inner 3')
C(list(pd.merge(ny, lon, on='date').columns) == ['date', 'close_x', 'close_y'], 'l13 quiz[3]: date, close_x, close_y')

# ---------------------------------------------------------------- review-3
prints('review', 'items[0].widget.options[0].text', 's = pd.Series([10.00, 11.00, 12.10])\nprint(s.shift(-1).tolist())')
prints('review', 'items[1].widget.answer', 'r = pd.Series([0.10, -0.10])\nprint(round((1 + r).prod() - 1, 4))', want='-0.01')
s4 = pd.Series([10.0, 12.0, 11.0, 13.0, 14.0])
E('review', 'items[2].widget.answer', float(s4.rolling(4).mean().iloc[-1]))
E('review', 'items[2].widget.wrong[0].value', float(s4.mean()))
E('review', 'items[2].widget.wrong[1].value', float(s4.rolling(4).mean().iloc[3]))
tv = lv.files['review-3']['items'][2]['widget']['wrong'][2]['value']
two('three slip is the mean of the last three', tv, round(float(s4.iloc[-3:].mean()), 4))
lv.claim_text('review', 'items[2].feedback.byKey.three', 'the three before the last', abs(tv - float(s4.iloc[1:4].mean())) < 6e-4,
              f'review-3 items[2] byKey three: {tv} is the mean of the last three (11, 13, 14); the three before the last average {s4.iloc[1:4].mean()}')
C(int(pd.Series(np.arange(1.0, 253.0)).pct_change().rolling(20).std().isna().sum()) == 20, 'review-3 items[3]: 20 NaN rows')
fe = pd.Series([100.00, 98.00, 103.00, 104.50], index=pd.to_datetime(['2024-01-31', '2024-02-27', '2024-02-28', '2024-02-29']))
E('review', 'items[4].widget.answer', round(float(fe.resample('ME').last().pct_change().iloc[1]), 3))
E('review', 'items[4].widget.wrong[0].value', round((98 + 103 + 104.5) / 3 / 100 - 1, 4))
E('review', 'items[4].feedback.byKey.mean', round((98 + 103 + 104.5) / 3, 2))
E('review', 'items[4].widget.wrong[1].value', 98 / 100 - 1)
inter = pd.DataFrame({'ticker': ['AZN', 'BARC'] * 10, 'close': np.r_[[100.0, 2.0] * 10] + np.arange(20) * 0.01})
inter['ret'] = inter['close'].pct_change()
C(int(inter['ret'].notna().sum()) == 19 and all(inter.ticker.iloc[i] != inter.ticker.iloc[i - 1] for i in range(1, 20)), 'review-3 items[5]: 19 values, none within one stock')
E('review', 'items[6].widget.options[0].text', 40 - 7)
a3 = pd.Series([1.0, 2.0, 3.0], index=pd.to_datetime(['2024-07-01', '2024-07-02', '2024-07-03']))
b3_ = pd.Series([1.0, 2.0, 3.0], index=pd.to_datetime(['2024-07-02', '2024-07-03', '2024-07-04']))
qq = a3 / b3_
C(f'{len(qq)} {int(qq.isna().sum())}' == '4 2', 'review-3 items[7]: prints 4 2')
C(len(pd.Series([1.0, 2.0], index=pd.to_datetime(['2024-04-30', '2024-06-28'])).resample('ME').last()) == 3, 'review-3 items[9]: 3 rows')

# ---------------------------------------------------------------- homework-3
cs = c9.sort_index()
E('homework', 'items[0].widget.examples[0].expect', round(float(cs.pct_change().std() * np.sqrt(252)), 4))
two('ann vol by numpy', float(np.std(cs.pct_change().dropna().to_numpy(), ddof=1) * math.sqrt(252)), float(cs.pct_change().std() * np.sqrt(252)))
dates = pd.bdate_range('2024-05-01', periods=6)
pz = pd.DataFrame({'AZN': [118.40, 120.11, 122.00, 121.53, 121.14, 121.45], 'BARC': [2.15, 2.16, 2.18, 2.17, 2.16, 2.19]}, index=dates)
tq = pd.DataFrame({'date': pd.to_datetime(['2024-05-01', '2024-05-01', '2024-05-03', '2024-05-03', '2024-05-06']), 'ticker': ['AZN', 'BARC', 'AZN', 'AZN', 'BARC'], 'qty': [10, 1000, -5, -5, 500]})
held = tq.pivot_table(index='date', columns='ticker', values='qty', aggfunc='sum').reindex(index=dates, columns=pz.columns).fillna(0).cumsum()
bp = (held.shift(1) * pz.diff()).sum(axis=1).iloc[1:].round(2)
C(bp.tolist() == [27.1, 38.9, -10.0, -15.0, 45.0], 'homework-3 items[1] example: 27.1, 38.9, -10.0, -15.0, 45.0')
two('2 May by hand', 10 * (120.11 - 118.40) + 1000 * (2.16 - 2.15), 27.1, tol=1e-6)
C(held.loc['2024-05-03', 'AZN'] == 0, 'homework-3 items[1] byKey test-1: AZN is 0 after 3 May')
E('homework', 'items[1].feedback.byKey.test-2', round(-2000 * (2.18 - 2.16), 2))
lw = pd.DataFrame({'AZN': [107.10, 106.60, 103.40, 104.82, 107.20, 106.94, 111.20, 112.00], 'BARC': [1.62, 1.65, 1.80, 1.94, 2.06, 2.10, 2.08, 2.07]},
                  index=pd.to_datetime(['2024-01-30', '2024-01-31', '2024-02-28', '2024-02-29', '2024-03-27', '2024-03-28', '2024-04-29', '2024-04-30']))
bm = lw.resample('ME').last().pct_change().idxmax()
C({k: v.strftime('%Y-%m') for k, v in bm.items()} == {'AZN': '2024-04', 'BARC': '2024-02'}, 'homework-3 items[2] example')
x3 = pd.DataFrame({'X': [10.00, 10.00, 9.00, 11.00, 12.50, 11.20], 'Y': [5.00, 5.10, 5.20, 5.30, 5.25, 5.60]},
                  index=pd.to_datetime(['2024-01-30', '2024-01-31', '2024-02-28', '2024-02-29', '2024-03-27', '2024-03-28']))
by_last = {k: v.strftime('%Y-%m') for k, v in x3.resample('ME').last().pct_change().idxmax().items()}
by_mean = {k: v.strftime('%Y-%m') for k, v in x3.resample('ME').mean().pct_change().idxmax().items()}
C(by_last == {'X': '2024-02', 'Y': '2024-03'} and by_mean == {'X': '2024-03', 'Y': '2024-02'}, 'homework-3 items[2] byKey test-3: means swap the answer')
wk = pd.Series([50.00, 50.50, 51.00, 50.80, 51.20, 51.50, 51.00, 52.00, 52.40, 52.53], index=pd.bdate_range('2024-07-01', periods=10))
E('homework', 'items[4].widget.answer', round(float(wk.resample('W-FRI').last().pct_change().iloc[1]), 4))
two('Friday to Friday', float(wk.resample('W-FRI').last().pct_change().iloc[1]), 52.53 / 51.20 - 1)
E('homework', 'items[4].widget.wrong[0].value', round(52.53 / 50.00 - 1, 4))
wmean = round(float(wk.resample('W-FRI').mean().pct_change().iloc[1]), 4)
E('homework', 'items[4].widget.wrong[1].value', wmean)      # fails: the content has 0.0262, weekly means give 0.0234
pr = pd.DataFrame({'date': pd.to_datetime(['2024-03-27', '2024-03-28', '2024-03-28', '2024-04-02']), 'close': [12.70, 12.66, 12.68, 12.80]})
tr5 = pd.DataFrame({'date': pd.to_datetime(['2024-03-27', '2024-03-28', '2024-04-02']), 'qty': [500, -200, 300]})
m5 = pd.merge(tr5, pr, on='date')
E('homework', 'items[5].widget.answer', len(m5))
E('homework', 'items[5].explain.text', round(float((m5.qty * m5.close).sum()), 2))
m6 = pd.merge(tr5, pr.drop_duplicates('date', keep='last'), on='date')
E('homework', 'items[5].explain.text', round(float((m6.qty * m6.close).sum()), 2))
dg = pd.DataFrame({'ticker': ['A', 'B', 'A', 'B', 'A', 'B'], 'ret': [0.02, 0.01, None, -0.03, -0.01, 0.05]})
E('homework', 'items[6].widget.answer', round(float(dg.groupby('ticker')['ret'].mean()['A']), 4))
E('homework', 'items[6].widget.wrong[0].value', round(0.01 / 3, 5))
E('homework', 'items[7].model', round((0.01 + 0.02 - 0.01) / 3, 6))
E('homework', 'items[7].model', round(1.01 * 1.02 * 0.99 - 1, 6))
st = pd.Series([0.01, 0.02, -0.01], index=pd.to_datetime(['2024-05-01', '2024-05-02', '2024-05-03']))
two('compounded month', float(((1 + st).resample('ME').prod() - 1).iloc[0]), 1.01 * 1.02 * 0.99 - 1)

lv.check_wrongs()
lv.report()
