"""Recompute every number and printed output stated in numpy-pandas level 2 (DataFrames): l5 to l8, review-2, homework-2.
Second read (session V). Run: python3 docs/reports/numpy-pandas-L2-numbers.py   (needs numpy and pandas; exits 0 when every check passes)
Snippets are executed with pandas and their output or exception compared with the keyed option. Numbers are computed
twice where a second route exists (by hand and by pandas). `lv.claim_text` ties a claim to its wording: it fails while a
false sentence is in the text and passes once it is reworded. Checks that fail on the current content are findings in
docs/reviews/review-numpy-pandas-1-3.md. The app runs pandas 2.2.3 (Pyodide 0.27.7); checks marked VERSION hold there and
are skipped under pandas 3, where copy-on-write changes the warning a chained assignment raises.
"""
import sys, os, io, math, contextlib, warnings
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("numpy-pandas", 2)
E = lv.expect
C = lv.claim
PD2 = pd.__version__.startswith('2.')

DF = ('df = pd.DataFrame({"open": [12.40, 12.55, 12.30, 12.50, 12.60], "close": [12.55, 12.31, 12.48, 12.62, 12.44], '
      '"volume": [18400, 22100, 15700, 19800, 24300]}, index=["2024-03-04", "2024-03-05", "2024-03-06", "2024-03-07", "2024-03-08"])\n')
CSV = 'csv = "date,close,volume\\n2024-02-28,12.18,16900\\n2024-02-29,12.25,15200\\n2024-03-01,12.40,17300\\n2024-03-04,12.55,18400\\n2024-03-05,12.31,22100\\n"\n'
GAPS = ('csv = "date,close,volume\\n2024-03-04,12.55,18400\\n2024-03-05,12.31,22100\\n2024-03-06,,\\n2024-03-07,12.62,19800\\n2024-03-08,12.44,\\n2024-03-11,,21000\\n"\n'
        'df = pd.read_csv(io.StringIO(csv), index_col="date", parse_dates=True)\n')
BOOK = 'book = pd.DataFrame({"price": [118.40, 2.15, 6.62, 0.71], "qty": [50, 2000, 800, 5000]}, index=["AZN", "BARC", "HSBA", "VOD"])\n'


def run(code):
    """Exec a snippet; return (printed text, exception 'Name: message' or None, warning class names)."""
    out = io.StringIO()
    g = {'np': np, 'pd': pd, 'io': io}
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            with contextlib.redirect_stdout(out):
                exec(code, g)
            err = None
        except Exception as e:
            err = type(e).__name__ + ': ' + str(e)
    return out.getvalue(), err, [x.category.__name__ for x in w]


def norm(s):
    return ' '.join(s.replace('`', '').split())


def prints(fid, path, code, label=None, want=None):
    txt, err, _ = run(code)
    want = norm(want if want is not None else lv.text(fid, path))
    C(err is None and norm(txt) == want, label or f'{fid} {path} prints {want!r}', f'printed {txt!r} err {err}')


def raises(fid, path, code, exc, fragment=''):
    _, err, _ = run(code)
    C(err is not None and err.startswith(exc) and fragment in err, f'{fid} {path}: snippet raises {exc} {fragment!r}', f'got {err!r}')


def two(label, a, b, tol=1e-9):
    C(abs(a - b) <= tol * max(1, abs(a)), f'two routes agree: {label} ({a!r})', f'{a!r} vs {b!r}')


g = {'np': np, 'pd': pd, 'io': io}
exec(DF, g)
df = g['df']

# ---------------------------------------------------------------- l5-columns-with-labels
C(df.loc['2024-03-06', 'close'] == 12.48, 'l5 screens[0]: the 6 March close is 12.48')
C(isinstance(df['close'], pd.Series) and df['close'].index.tolist() == df.index.tolist(), 'l5 screens[1]: df["close"] is a Series with the dates')
C(df.loc['2024-03-07'].tolist() == [12.50, 12.62, 19800.0], 'l5 screens[2] explain: open 12.50, close 12.62, volume 19800')
E('l5', 'screens[3].widget.answer', float(df.iloc[1]['close']))
E('l5', 'screens[3].widget.wrong[0].value', float(df.iloc[0]['close']))
two('5 March open equals 4 March close', float(df.loc['2024-03-05', 'open']), 12.55)
E('l5', 'screens[3].widget.wrong[1].value', float(df.iloc[2]['close']))
raises('l5', 'screens[4]', DF + 'first = df[0]', 'KeyError', '0')
E('l5', 'screens[5].widget.answer', len(df.loc['2024-03-05':'2024-03-07', 'close']))
E('l5', 'screens[5].widget.wrong[0].value', len(df.iloc[1:3]))
C(df[df['close'] > df['open']].index.tolist() == ['2024-03-04', '2024-03-06', '2024-03-07'], 'l5 screens[6]: up days 4, 6, 7 March')
raises('l5', 'screens[7].widget.options[1].why', DF + 'df.loc[-1, "volume"]', 'KeyError')
raises('l5', 'screens[7].widget.options[2].why', DF + 'df.iloc[-1, "volume"]', 'ValueError')
E('l5', 'screens[7].explain.text', int(df['volume'].iloc[-1]))
exec(BOOK, g)
book = g['book']
val = book['price'] * book['qty']
C(val.round(2).to_dict() == {'AZN': 5920.0, 'BARC': 4300.0, 'HSBA': 5296.0, 'VOD': 3550.0}, 'l5 screens[10] example: position values')
lv.claim_text('l5', 'screens[10].explain.text', '5296.000000000001', repr(6.62 * 800) == '5296.000000000001',
              f'l5 screens[10] explain: "float noise such as 5296.000000000001", but 6.62 x 800 is {6.62 * 800!r} in floats')
C(repr(1.05 * 7) == '7.3500000000000005', 'l5 screens[10] fix: 7 shares at 1.05 (hidden test 4) give 7.3500000000000005')
E('l5', 'screens[10].feedback.byKey.test-3', -300 * 24.37)
two('-7311', -300 * 24.37, -7311.0)
prints('l5', 'quiz[0].widget.options[0].text', DF + 'print(df[["close"]].shape)')
E('l5', 'quiz[1].widget.answer', len(df.iloc[1:3]))
E('l5', 'quiz[2].widget.answer', float(df.iloc[0, 1]))
E('l5', 'quiz[2].widget.wrong[0].value', float(df.iloc[0, 0]))
E('l5', 'quiz[2].widget.wrong[1].value', int(df.iloc[0, 2]))
txt, _, _ = run(DF + 'print(df.loc["2024-03-07"])')
C('12.50' in txt and '12.62' in txt and '19800.00' in txt, 'l5 quiz[3] prose: the row prints 12.50, 12.62 and 19800.00', repr(txt))
txt, _, _ = run(DF + 'print(df["volume"])')
C('19800' in txt and '19800.' not in txt, 'l5 quiz[3] why: df["volume"] prints whole numbers')
C(type(df.loc['2024-03-07', 'volume']).__name__.startswith('int'), 'l5 quiz[3] why: df.loc[date, "volume"] is a whole number')

# ---------------------------------------------------------------- l6-loading-prices
exec(CSV, g)
csv = g['csv']
raw = pd.read_csv(io.StringIO(csv))
C(raw.index.tolist() == [0, 1, 2, 3, 4] and pd.api.types.is_string_dtype(raw['date']), 'l6 screens[0]: rows labelled 0 to 4, dates a text column')
d1 = pd.read_csv(io.StringIO(csv), index_col='date')
E('l6', 'screens[1].widget.answer', float(d1.loc['2024-03-04', 'close']))
E('l6', 'screens[1].widget.wrong[0].value', float(d1.loc['2024-03-05', 'close']))
E('l6', 'screens[1].widget.wrong[1].value', float(d1.loc['2024-03-01', 'close']))
dp = pd.read_csv(io.StringIO(csv), index_col='date', parse_dates=True)
C([str(x)[:10] for x in dp.loc['2024-03'].index] == ['2024-03-01', '2024-03-04', '2024-03-05'], 'l6 screens[2]: "2024-03" selects 1, 4 and 5 March')
raises('l6', 'screens[2].explain.text', CSV + 'df = pd.read_csv(io.StringIO(csv), index_col="date"); df.loc["2024-03"]', 'KeyError')
E('l6', 'screens[3].widget.answer', float(dp['close'].describe()['50%']))
E('l6', 'screens[3].widget.wrong[0].value', round(float(dp['close'].mean()), 3))
two('mean 12.338', float(dp['close'].mean()), (12.18 + 12.25 + 12.40 + 12.55 + 12.31) / 5)
E('l6', 'screens[3].widget.wrong[1].value', float(dp['close'].iloc[2]))
two('describe std is ddof=1', float(dp['close'].describe()['std']), float(np.std(dp['close'].to_numpy(), ddof=1)))
C(str(dp.sort_values('volume', ascending=False).index[0])[:10] == '2024-03-05', 'l6 screens[4]: 5 March leads by volume')
C(str(dp['volume'].idxmin())[:10] == '2024-02-29', 'l6 screens[4] byKey r1c0: 29 February is the quietest day')
raises('l6', 'screens[5]', CSV + 'df = pd.read_csv(io.StringIO(csv)); print(df.loc["2024-03-04", "close"])', 'KeyError')
rev = 'rev = "date,close,volume\\n2024-03-05,12.31,22100\\n2024-03-04,12.55,18400\\n2024-03-01,12.40,17300\\n2024-02-29,12.25,15200\\n2024-02-28,12.18,16900\\n"\n'
prints('l6', 'screens[6].widget.answer', rev + 'd2 = pd.read_csv(io.StringIO(rev), index_col="date", parse_dates=True); print(d2["close"].iloc[0])', want='12.31')
E('l6', 'screens[6].widget.wrong[0].value', 12.18)
pnl = pd.Series([120.50, -340.25, 85.00, -512.80, -45.10, 230.75, -198.40, -12.00],
                index=['2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08', '2024-03-11', '2024-03-12', '2024-03-13'])
C(pnl.nsmallest(5).index.tolist() == ['2024-03-07', '2024-03-05', '2024-03-12', '2024-03-08', '2024-03-13'], 'l6 screens[10]: the five worst days')
E('l6', 'screens[10].feedback.byKey.test-1', 512.80)
prints('l6', 'quiz[0].widget.options[0].text', 'text = "date,close\\n2024-03-04,12.55\\n2024-03-05,12.31\\n"\nprint(pd.read_csv(io.StringIO(text)).shape)')
cl = pd.Series([12.18, 12.25, 12.40, 12.55, 12.31])
E('l6', 'quiz[1].prose', round(float(cl.std()), 4))
E('l6', 'quiz[1].prose', round(float(np.std(cl.to_numpy())), 4))
two('ratio sqrt(5/4)', float(cl.std() / np.std(cl.to_numpy())), math.sqrt(5 / 4))
E('l6', 'quiz[1].explain.text', round(math.sqrt(5 / 4), 3))
C(abs(0.1283 * 1.118 - 0.1434) < 0.00005, 'l6 quiz[1] explain: 0.1283 x 1.118 = 0.1434')
prints('l6', 'quiz[2].widget.options[0].text', 'print(pd.Series([12.18, 12.25, 12.40, 12.55, 12.31]).nsmallest(2).tolist())')
prints('l6', 'quiz[2].widget.options[1].text', 'print(pd.Series([12.18, 12.25, 12.40, 12.55, 12.31]).nlargest(2).tolist())', 'l6 quiz[2] largest option is nlargest(2)')
# quiz[2] distractor "first" names the same list as the key: on these closes the two smallest are also the first two rows
lv.claim_text('l6', 'quiz[2].widget.options[2].text', 'only because they come first in the file',
              cl.nsmallest(2).tolist() != cl.head(2).tolist(),
              'l6 quiz[2]: the "first" distractor prints the same list as the key (head(2) == nsmallest(2) on these closes)')
raises('l6', 'quiz[3]', CSV + 'df = pd.read_csv(io.StringIO(csv), index_col="date"); march = df.loc["2024-03"]', 'KeyError')

# ---------------------------------------------------------------- l7-gaps
exec(GAPS, g)
dg = g['df']
C(dg.isna().sum().tolist() == [2, 2], 'l7 screens[1]: close 2, volume 2')
C(int(dg.isna().sum().sum()) == 4, 'l7 screens[1] explain: 4 gaps in all')
E('l7', 'screens[2].widget.answer', len(dg.dropna()))
E('l7', 'screens[2].widget.wrong[0].value', len(dg.dropna(subset=['close'])))
E('l7', 'screens[2].widget.wrong[1].value', 6 - 4)
r = pd.Series([0.8, None, -0.4, 1.1, None])
prints('l7', 'screens[3].widget.options[0].text', 'r = pd.Series([0.8, None, -0.4, 1.1, None])\nprint(r.mean())')
two('mean 0.5', float(r.mean()), 1.5 / 3)
txt, _, _ = run('r = pd.Series([0.8, None, -0.4, 1.1, None])\nprint(np.mean(r.to_numpy()))')
C(txt.strip() == 'nan', 'l7 screens[3] why: np.mean on the array gives nan')
E('l7', 'screens[4].widget.answer', round(float(r.fillna(0).mean()), 4))
two('fill mean 0.3', float(r.fillna(0).mean()), 1.5 / 5)
prints('l7', 'screens[5].widget.options[1].text', GAPS + 'print((df["close"] == np.nan).sum())')
E('l7', 'screens[6].widget.answer', float(dg['close'].ffill().loc['2024-03-06']))
E('l7', 'screens[6].widget.wrong[0].value', float(dg['close'].bfill().loc['2024-03-06']))
E('l7', 'screens[6].widget.wrong[1].value', round(float(dg['close'].interpolate().loc['2024-03-06']), 3))
C(dg['close'].ffill().loc['2024-03-11'] == 12.44, 'l7 screens[6] explain: 11 March gets 12.44')
z = dg['close'].fillna(0).pct_change()
C(z.loc['2024-03-06'] == -1.0 and np.isinf(z.loc['2024-03-07']), 'l7 screens[7]: -1.0 on 6 March, infinite on 7 March')
E('l7', 'screens[7].widget.options[3].text', round(12.31 / 12.55 - 1, 4))
vf = dg['volume'].ffill()
E('l7', 'screens[8].widget.options[1].why', int(vf.loc['2024-03-06'] + vf.loc['2024-03-08']))
two('41900', float(vf.loc['2024-03-06'] + vf.loc['2024-03-08']), 22100 + 19800)
E('l7', 'quiz[0].widget.answer', int(pd.Series([12.55, None, 12.62]).count()))
E('l7', 'quiz[1].widget.answer', len(dg.dropna(subset=['volume'])))
E('l7', 'quiz[1].widget.wrong[0].value', len(dg.dropna()))
E('l7', 'quiz[1].widget.wrong[1].value', 6 - 4)
prints('l7', 'quiz[2].widget.options[0].text', 's = pd.Series([12.55, None, None, 12.62])\nprint(s.ffill().tolist())')
C(np.allclose(pd.Series([12.55, None, None, 12.62]).interpolate().round(4).tolist(), [12.55, 12.5733, 12.5967, 12.62]), 'l7 quiz[2] interp option values')
C(pd.Series([12.55, None, None, 12.62]).ffill(limit=1).isna().sum() == 1, 'l7 quiz[2] explain: ffill(limit=1) fills only the first gap')

# ---------------------------------------------------------------- l8-new-columns
c8 = pd.Series([12.55, 12.31, 12.48, 12.62, 12.44], index=['2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08'])
ret = c8.pct_change()
E('l8', 'screens[0].widget.answer', round(12.31 / 12.55 - 1, 6))
two('5 March return', float(ret.iloc[1]), 12.31 / 12.55 - 1)
E('l8', 'screens[0].widget.wrong[0].value', round((12.31 - 12.55) / 100, 4))   # -0.24 typed as a percent
nb = lv.files['l8-new-columns']['screens'][0]['widget']['wrong'][1]['value']
C(abs(-0.24 / 12.31 - nb) < 2e-6, f'l8 screens[0] wrong new-base {nb} is -0.24 / 12.31 = {-0.24 / 12.31:.7f} (last digit rounded up; inside its tolerance)')
for i, v in enumerate([-0.019124, 0.013810, 0.011218, -0.014263]):
    two(f'ret[{i + 1}]', round(float(ret.iloc[i + 1]), 6), v)
C(pd.isna(ret.iloc[0]), 'l8 screens[1]: the first return is NaN')
E('l8', 'screens[2].widget.answer', round(float(ret.iloc[2]), 4))
E('l8', 'screens[2].widget.wrong[0].value', round(float(ret.iloc[1]), 4))
E('l8', 'screens[2].widget.wrong[1].value', round(float(ret.iloc[3]), 4))
sig = np.where(ret > 0, 1, -1)
C(np.flatnonzero(sig == -1).tolist() == [0, 1, 4], 'l8 screens[3]: -1 on 4, 5 and 8 March')
C(np.isnan(np.sign(ret.iloc[0])), 'l8 screens[3] explain: np.sign keeps NaN')
CH = ('df = pd.DataFrame({"close": [12.55, 12.31, 12.48, 12.62, 12.44]})\ndf["ret"] = df["close"].pct_change()\n'
      'df["flag"] = 0\ndf[df["ret"] < 0]["flag"] = -1\nprint((df["flag"] == -1).sum())')
txt, err, ws = run(CH)
C(txt.strip() == '0' and err is None, 'l8 screens[4]: the chained write leaves df unchanged, prints 0')
if PD2:
    C('SettingWithCopyWarning' in ws, 'l8 screens[4] VERSION (pandas 2.2.3): a SettingWithCopyWarning is raised', f'warnings {ws}')
else:
    print('skip l8 screens[4] SettingWithCopyWarning check: pandas', pd.__version__, 'raises', ws)
prints('l8', 'screens[5].widget.answer', 'df = pd.DataFrame({"close": [12.55, 12.31, 12.48, 12.62, 12.44]})\ndf["ret"] = df["close"].pct_change()\n'
       'df["flag"] = 0\ndf.loc[df["ret"] < 0, "flag"] = -1\nprint(df["flag"].sum())', want='-2')
raises('l8', 'screens[6]', BOOK + 'value = book.apply(lambda row: row["price"] * row["qty"])', 'KeyError', 'price')
E('l8', 'screens[6].widget.options[3].text', float(val.sum()))
two('19066', float(val.sum()), 5920 + 4300 + 5296 + 3550)
q = pd.DataFrame({'bid': [12.30, 2.15, 118.40], 'ask': [12.32, 2.16, 118.46]}, index=['XYZ', 'BARC', 'AZN'])
mid = (q['bid'] + q['ask']) / 2
C(((q['ask'] - q['bid']) / mid * 10000).round(1).tolist() == [16.2, 46.4, 5.1], 'l8 screens[9]: spreads 16.2, 46.4, 5.1')
E('l8', 'screens[9].feedback.byKey.test-1', round(0.02 / 12.30 * 10000, 1))
E('l8', 'screens[9].explain.text', round(0.02 / 12.31 * 10000, 1))
prints('l8', 'quiz[0].widget.options[0].text', 's = pd.Series([10.00, 11.00, 9.90])\nprint(s.pct_change().round(2).tolist())')
prints('l8', 'quiz[2].widget.options[0].text', 'ret = pd.Series([None, 0.5, -0.2])\nprint(np.where(ret > 0, 1, -1).tolist())')
E('l8', 'quiz[3].widget.answer', 1)

# ---------------------------------------------------------------- review-2
C(df.iloc[1:4].index.tolist() == df.loc['2024-03-05':'2024-03-07'].index.tolist(), 'review-2 items[0]: iloc[1:4] matches the label slice')
raises('review', 'items[0].widget.options[2].why', DF + 'df.loc[1:4]', 'TypeError')
raises('review', 'items[0].widget.options[3].why', DF + 'df.iloc["2024-03-05":"2024-03-07"]', 'TypeError')
E('review', 'items[1].widget.answer', round(98.00 / 101.50 - 1, 4))
E('review', 'items[1].widget.wrong[0].value', round(101.50 / 98.00 - 1, 4))
prints('review', 'items[1].widget.answer', 'text = "date,close\\n2024-05-03,101.50\\n2024-05-02,100.00\\n2024-05-01,98.00\\n"\n'
       'df = pd.read_csv(io.StringIO(text), index_col="date", parse_dates=True)\nfirst = df["close"].iloc[0]\nlast = df["close"].iloc[-1]\n'
       'print(round(last / first - 1, 4))', want='-0.0345')
E('review', 'items[1].explain.text', round(100 * (101.50 / 98.00 - 1), 2))
r2 = pd.Series([0.012, None, -0.006, 0.009])
E('review', 'items[2].widget.answer', float(r2.isna().mean()))
E('review', 'items[2].widget.wrong[1].value', round(float(r2.mean()), 4))
c6 = pd.Series([50.00, 50.50, 50.50, 49.80, 50.10, 50.10])
rr = c6.pct_change()
s6 = np.where(rr > 0, 1, -1)
E('review', 'items[3].widget.answer', int((s6 == -1).sum()))
E('review', 'items[3].widget.wrong[0].value', int((rr < 0).sum()))
E('review', 'items[3].widget.wrong[1].value', int((s6 == -1).sum()) - 1)
E('review', 'items[3].widget.wrong[2].value', int((s6 == -1).sum()) - 2)
C(np.allclose(rr.iloc[1:].round(4).tolist(), [0.01, 0.0, -0.0139, 0.006, 0.0]), 'review-2 items[3] explain: returns 0.01, 0.0, -0.0139, 0.006, 0.0')
b4 = book.copy()
b4.loc['HSBA', 'qty'] = 1200
E('review', 'items[4].widget.answer', round(float((b4['price'] * b4['qty']).sum()), 2))
two('21714', float((b4['price'] * b4['qty']).sum()), 19066 + 400 * 6.62)
E('review', 'items[4].widget.wrong[0].value', round(float(val.sum()), 2))
E('review', 'items[4].widget.wrong[1].value', round(1200 * 6.62, 2))
prints('review', 'items[5].widget.accept', GAPS + 'print(df["close"].describe()["count"])', want='4.0')
f6 = dg['close'].ffill().pct_change()
E('review', 'items[6].explain.text', round(float(f6.loc['2024-03-07']), 4))
C(f6.loc['2024-03-06'] == 0.0, 'review-2 items[6]: 0.0 on 6 March')
ip = dg['close'].interpolate().pct_change()
C(abs(ip.loc['2024-03-06'] - 0.0126) < 0.0001 and abs(ip.loc['2024-03-07'] - 0.0126) < 0.0003, 'review-2 items[6] split option: about 0.0126 on each day under interpolation',
  f'{ip.loc["2024-03-06"]:.5f}, {ip.loc["2024-03-07"]:.5f}')
w = (val / val.sum()).round(4).to_dict()
C(w == {'AZN': 0.3105, 'BARC': 0.2255, 'HSBA': 0.2778, 'VOD': 0.1862}, 'review-2 items[7]: weights')
E('review', 'items[7].feedback.byKey.test-1', 19066)

# ---------------------------------------------------------------- homework-2
H = "date,close,volume\n2024-04-12,96.40,2950\n2024-04-11,,\n2024-04-10,95.10,3300\n2024-04-09,96.80,2700\n2024-04-08,95.10,3100\n2024-04-05,94.00,2800\n"
hd = pd.read_csv(io.StringIO(H), index_col='date', parse_dates=True).sort_index()
hr = hd['close'].ffill().pct_change().dropna()
C([str(d)[:10] for d in hr.nsmallest(3).index] == ['2024-04-10', '2024-04-11', '2024-04-08'], 'homework-2 items[0] test-1: 10, 11, then 8 April')
C(hr.loc['2024-04-11'].item() == 0.0, 'homework-2 items[0] explain: the filled gap has return 0.0')
E('homework', 'items[1].feedback.byKey.test-4', round(float(hr.min()), 4))
E('homework', 'items[1].feedback.byKey.test-5', round(float(hr.std() * np.sqrt(252)), 4))
two('vol by numpy', float(np.std(hr.to_numpy(), ddof=1) * math.sqrt(252)), float(hr.std() * np.sqrt(252)))
bk = pd.DataFrame({'price': [118.40, 24.37, 6.62, 4.85], 'qty': [50, -300, 800, -1000]}, index=['AZN', 'SHEL', 'HSBA', 'BP'])
v2 = bk['price'] * bk['qty']
lo, sh = float(v2[bk['qty'] > 0].sum()), float(v2[bk['qty'] < 0].sum())
E('homework', 'items[2].feedback.byKey.test-1', round(lo, 2))
E('homework', 'items[2].feedback.byKey.test-1', round(sh, 2))
two('long', lo, 5920 + 5296)
two('short', sh, -7311 - 4850)
E('homework', 'items[2].explain.text', round(lo - sh, 2))
E('homework', 'items[2].explain.text', round(-(lo + sh), 2))
prints('homework', 'items[3].widget.options[0].text', DF + 'print(df.loc[df["volume"] > 20000, "close"].tolist())')
prints('homework', 'items[3].widget.options[2].text', DF + 'print((df["volume"] > 20000).tolist())', 'homework-2 items[3] mask option')
E('homework', 'items[4].widget.answer', round(float(dg['close'].ffill().mean()), 3))
two('74.67 / 6', float(dg['close'].ffill().mean()), 74.67 / 6)
E('homework', 'items[4].prose', round(float(dg['close'].mean()), 2))
E('homework', 'items[4].widget.wrong[0].value', round(float(dg['close'].mean()), 2))
E('homework', 'items[4].widget.wrong[1].value', round(float(dg['close'].fillna(0).mean()), 2))
E('homework', 'items[4].explain.text', round(float(dg['close'].ffill().sum()), 2))
prints('homework', 'items[5].widget.options[0].text', GAPS + 'print(df.describe().loc["count"].tolist())')
E('homework', 'items[6].widget.answer', round(float(df.iloc[-3:]['close'].mean()), 4))
two('37.54 / 3', float(df.iloc[-3:]['close'].mean()), 37.54 / 3)
E('homework', 'items[6].widget.wrong[0].value', float(df.iloc[-3]['close']))
E('homework', 'items[6].widget.wrong[1].value', round(float(df.iloc[-2:]['close'].mean()), 4))
E('homework', 'items[6].widget.wrong[2].value', round(float(df.iloc[:3]['close'].mean()), 4))
# longform h-cleaning-review
LF = ('text = "date,close,volume\\n2024-03-04,12.55,18400\\n2024-03-05,12.31,22100\\n2024-03-06,,\\n2024-03-07,12.62,19800\\n2024-03-08,12.44,\\n2024-03-11,,21000\\n"\n'
      'df = pd.read_csv(io.StringIO(text))\ndf = df.fillna(0)\ndf["ret"] = df["close"].pct_change()\nprint(df["ret"].mean(), df["volume"].mean())\n'
      'print(df.loc["2024-03-06", "close"])')
txt, err, _ = run(LF)
C(err is not None and err.startswith('KeyError') and '2024-03-06' in err, 'homework-2 items[7] (a): KeyError on the last line', repr(err))
C(txt.split()[0] == 'inf' and float(txt.split()[1]) == 13550.0, 'homework-2 items[7] (b), (c): the script prints inf and 13550.0', repr(txt))
zf = dg['close'].fillna(0).pct_change()
C(zf.loc['2024-03-06'] == -1 and np.isinf(zf.loc['2024-03-07']) and zf.loc['2024-03-11'] == -1, 'homework-2 items[7] (b): -1, inf, -1')
E('homework', 'items[7].model', 81300)
E('homework', 'items[7].model', 81300 / 6)
E('homework', 'items[7].model', 81300 / 4)
two('volume total', float(dg['volume'].sum()), 81300)
cr = dg['close'].ffill().pct_change()
for v in [-0.019124, 0.0, 0.025183, -0.014263, 0.0]:
    C(np.isclose(cr.dropna().round(6), v).any(), f'homework-2 items[7] (d): return {v}')
E('homework', 'items[7].model', round(float(cr.mean()), 6))
two('mean return', float(cr.mean()), (-0.019124 + 0.025183 - 0.014263) / 5, tol=1e-5)
E('homework', 'items[7].rubric[4].text', round(float(cr.mean()), 6))

lv.check_wrongs()
lv.report()
