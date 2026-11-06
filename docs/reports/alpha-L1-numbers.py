"""Recompute every number stated in alpha level 1 (Universe) and check it at its JSON path (second read).

Run: python3 docs/reports/alpha-L1-numbers.py   (NumPy, pandas and the standard library; exits 0 when every check passes)

The panel is the brief's `make_panel()` (seed 2310), taken verbatim from l1's prelude, and the brief's own checks are
asserted first. Universe, split adjustment, total returns, forward returns and the survivorship numbers are computed
here by direct code; where the lesson's solution gives the same quantity it is run as a second route (`two`).
`E` checks a stated value appears where it is stated; `stated` ties a claim to its wording (while the phrase is in
the text, the claim must hold). A check that fails because the content is wrong is a finding in
docs/reviews/review-alpha-1-2.md and stays failing until the fix pass corrects the content.
"""
import json
import math
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, COURSES  # noqa: E402

lv = Level("alpha", 1)
E = lv.expect
fails = []


def two(name, a, b, tol=1e-9):
    if not math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol):
        fails.append(f'{name}: routes disagree {a!r} vs {b!r}')


def claim(name, ok):
    lv._rec(bool(ok), f'claim: {name}', '')


def stated(ref, path, phrase, ok):
    there = phrase in lv.text(ref, path)
    lv._rec(bool(ok) or not there, f'stated: {ref} {path} "{phrase}"', '' if ok or not there else 'the stated claim is false')


def R(x, d):
    return round(float(x), d)


def doc(fid):
    return json.load(open(os.path.join(COURSES, 'alpha', fid + '.json')))


# ---------- the panel and the lesson solutions (second routes) ----------
ns = {}
exec(doc('l1-choosing-a-universe')['screens'][6]['widget']['prelude'], ns)
for fid, idx in [('l1-choosing-a-universe', [6, 7]), ('l2-splits-and-dividends', [5, 6]), ('l3-including-the-dead', [6, 7]), ('l4-returns-panel', [6, 7])]:
    for i in idx:
        exec(doc(fid)['screens'][i]['widget']['solution'], ns)
for i in (0, 1):
    exec(doc('homework-1')['items'][i]['widget']['solution'], ns)
make_panel, toy = ns['make_panel'], ns['toy']
P = make_panel()
ret, listed, rc, sp, dv, adv = P['ret'], P['listed'], P['raw_close'], P['split'], P['dividend'], P['adv_gbp']
D = ret.index
row = {d.date().isoformat(): i for i, d in enumerate(D)}

# brief checks
claim('235,497 listed cells, 16,503 NaN', ret.notna().sum().sum() == 235497 and ret.isna().sum().sum() == 16503)
claim('15 split days', int((sp != 1).sum().sum()) == 15)
rebuild = (sp * (rc + dv) / rc.shift(1) - 1 - ret).abs().max().max()
claim('rebuild identity within 1e-15', rebuild < 1e-15)

# ---------- direct universe ----------
vol = (listed * adv).where(listed)
advroll = vol.rolling(60, min_periods=60).mean()
mask = listed & (advroll >= 5e6)
two('universe_mask agrees', int((mask != ns['universe_mask'](P)).sum().sum()), 0)
cnt = mask.sum(axis=1)
first = int((cnt > 0).values.argmax())
late = [c for c in ret.columns if not listed[c].iloc[0]]
dead = [c for c in ret.columns if listed[c].any() and not listed[c].iloc[-1]]
today = listed.columns[listed.iloc[-1]]

L1 = 'l1'
E(L1, 'screens[1].widget.answer', len([c for c in today if not listed[c].iloc[0]]))
E(L1, 'screens[1].widget.accept', int(listed.iloc[0][today].sum()))
E(L1, 'screens[1].widget.accept', int(listed.iloc[0].sum()))
E(L1, 'screens[1].prose', int(listed.iloc[-1].sum()))
claim('20 of the day-0 shares die later (stated as Twenty)', len([c for c in dead if listed[c].iloc[0]]) == 20); E(L1, 'screens[1].explain.text', 'Twenty')
E(L1, 'screens[1].widget.wrong[0].value', int(listed.iloc[0].sum())); E(L1, 'screens[1].widget.wrong[1].value', int(listed.iloc[0][today].sum()))
# toy: trailing 60-day means on 2 and 3 May, the whole-sample mean of E
tv = toy['volume_gbp']; troll = tv.rolling(60, min_periods=60).mean()
r3, r2 = list(tv.index).index(pd.Timestamp('2019-05-03')), list(tv.index).index(pd.Timestamp('2019-05-02'))
E(L1, 'screens[2].hints[2]', R(troll['E'].iloc[r3] / 1e6, 2)); claim('E on 2 May below 5m (4.975)', R(troll['E'].iloc[r2] / 1e6, 3) == 4.975)
E(L1, 'screens[2].hints[1]', int(toy['listed']['C'].iloc[:r3 + 1].sum()))
E(L1, 'screens[5].widget.answer', R(tv['E'].mean() / 1e6, 3))
E(L1, 'screens[5].widget.accept', R(tv['E'].sum() / 1e6, 0))
E(L1, 'screens[5].widget.wrong[0].value', (2 + 12.5) / 2)
claim('E jumps on row 70 = 10 April 2019', tv.index[70].date().isoformat() == '2019-04-10' and tv['E'].iloc[70] == 12.5e6 and tv['E'].iloc[69] == 2e6)
claim('universe on 3 May = A, D, E', ns['universe_on'](toy, '2019-05-03') == ['A', 'D', 'E'])
claim('C joins on 7 May, its 60th day', ns['universe_on'](toy, '2019-05-07') == ['A', 'C', 'D', 'E'] and int(toy['listed']['C'].loc[:'2019-05-07'].sum()) == 60)
claim('D last day 21 May', toy['listed']['D'].loc[:'2019-05-21'].iloc[-1] and not toy['listed']['D'].loc['2019-05-22'])
stated(L1, 'screens[2].feedback.byKey.r2', 'listed 58 days ago', r3 - 30 == 58)   # C lists on row 30; 3 May is row 87
# S046 and S012
for nm, lst, join, last in [('S046', '2021-04-07', '2021-06-29', None), ('S012', '2019-01-02', '2019-03-26', '2022-01-18')]:
    ld = listed.index[listed[nm]]; md = mask.index[mask[nm]]
    claim(f'{nm} lists {lst}, joins {join}', ld[0].date().isoformat() == lst and md[0].date().isoformat() == join)
    if last:
        claim(f'{nm} last day {last}', ld[-1].date().isoformat() == last and md[-1].date().isoformat() == last)
E(L1, 'screens[3].prose', R(adv['S046'] / 1e6, 1)); E(L1, 'screens[3].prose', '7 April 2021'); E(L1, 'screens[3].prose', '29 June 2021')
E(L1, 'screens[4].prose', R(adv['S012'] / 1e6, 1)); E(L1, 'screens[4].prose', R(-100 * ret.loc['2022-01-18', 'S012'], 2))
E(L1, 'screens[4].widget.options', '26 March 2019')
# the mask on make_panel
E(L1, 'screens[7].explain.text', int((cnt == 0).sum())); E(L1, 'screens[7].explain.text', int(cnt.iloc[first]))
claim('first universe date 26 March 2019', D[first].date().isoformat() == '2019-03-26')
E(L1, 'screens[7].explain.text', int(cnt.iloc[first:].min())); E(L1, 'screens[7].explain.text', int(cnt.iloc[first:].max()))
E(L1, 'quiz[0].widget.answer', 59)
claim('S039 lists 15 May 2020; S007 dies 2 October 2023', listed.index[listed['S039']][0].date().isoformat() == '2020-05-15'
      and listed.index[listed['S007']][-1].date().isoformat() == '2023-10-02')
claim('20 deaths', len(dead) == 20); E(L1, 'screens[8].hints[2]', 'Twenty')
# a centred 60-row window reaches 29 rows ahead
s = pd.Series(np.arange(200.0)); claim('center=True, window 60, covers t-30..t+29', s.rolling(60, center=True).mean()[100] == np.mean(np.arange(70, 130)))
# quiz[1]: W 4.90 below, X 45 days, Y not listed, Z exactly 5.00
qt = [('W', True, 300, 4.90), ('X', True, 45, 30.0), ('Y', False, 410, 12.0), ('Z', True, 800, 5.00)]
E(L1, 'quiz[1].widget.answer', sum(1 for _, l, n, v in qt if l and n >= 60 and v >= 5))

# ---------- l2 ----------
L2 = 'l2'
E(L2, 'screens[0].prose', R(rc.loc['2021-08-27', 'S089'], 2)); E(L2, 'screens[0].prose', R(rc.loc['2021-08-26', 'S089'], 2))
raw89 = rc.loc['2021-08-27', 'S089'] / rc.loc['2021-08-26', 'S089'] - 1
E(L2, 'screens[1].explain.text', R(-100 * raw89, 1)); E(L2, 'screens[0].widget.options[3].why', R(100 * ret.loc['2021-08-27', 'S089'], 1))
E(L2, 'screens[1].widget.answer', R(200 * 260.09, 0)); E(L2, 'screens[1].widget.wrong[0].value', R(100 * 260.09, 0)); E(L2, 'screens[1].widget.wrong[1].value', R(100 * 528.61, 0))
E(L2, 'screens[1].explain.text', R(-100 * (200 * 260.09 / (100 * 528.61) - 1), 2))
two('S089 true return from the panel and from the shown prices', R(ret.loc['2021-08-27', 'S089'], 4), R(200 * 260.09 / (100 * 528.61) - 1, 4), 2e-4)
for i, dd in enumerate(['2021-08-25', '2021-08-26', '2021-08-27']):
    E(L2, f'screens[2].widget.rows[{i}][1]', R(rc.loc[dd, 'S089'], 2))
    E(L2, f'screens[2].widget.rows[{i}][3].answer', R(rc.loc[dd, 'S089'] / (2 if i < 2 else 1), 2) if i == 2 else round(R(rc.loc[dd, 'S089'], 2) / 2, 3))
E(L2, 'screens[2].widget.rows[3][3]', R(rc.loc['2021-08-30', 'S089'], 2))
E(L2, 'screens[3].prose', R(dv.loc['2019-04-01', 'S000'], 2)); E(L2, 'screens[3].prose', R(rc.loc['2019-03-29', 'S000'], 2)); E(L2, 'screens[3].prose', R(rc.loc['2019-04-01', 'S000'], 2))
E(L2, 'screens[3].widget.answer', R((103.66 + 0.52) / 104.39 - 1, 5)); E(L2, 'screens[3].widget.wrong[0].value', R(103.66 / 104.39 - 1, 5))
E(L2, 'screens[3].widget.wrong[1].value', R((103.66 + 1.04) / 104.39 - 1, 5))
claim('110 dividend payers (about half), every 63 days (four a year)', int((dv > 0).any().sum()) == 110 and sorted(set(np.where(dv.values > 0)[0]))[:2] == [63, 126])
hand = [(50.00, 1, 0), (51.00, 1, 0), (25.80, 2, 0), (26.10, 1, 0), (25.90, 1, 0.39)]
for i in range(1, 5):
    E(L2, f'screens[4].widget.rows[{i}][4].answer', R(hand[i][1] * (hand[i][0] + hand[i][2]) / hand[i - 1][0] - 1, 6 if i < 4 else 5))
E(L2, 'screens[4].explain.text', R(100 * (25.80 / 51.00 - 1), 1))
sa = rc / sp[::-1].cumprod()[::-1].shift(-1, fill_value=1.0)
E(L2, 'screens[5].explain.text', float((sa - P['adj_close']).abs().max().max()))
two('split_adjust agrees', float((ns['split_adjust'](rc, sp) - sa).abs().max().max()), 0.0)
trr = sp * (rc + dv) / rc.shift(1) - 1
claim('total-return error is 5e-16 (5.2e-16)', R((trr - ret).abs().max().max() * 1e16, 0) == 5)
E(L2, 'screens[6].widget.examples', 0) if False else None
E(L2, 'screens[6].feedback.byKey', R(2 * (39.5 + 0.5), 0))
pc = rc.pct_change(fill_method=None)
low = pc.where(pc < -0.4).stack(); low = low[low.notna()]
nsplit = sum(sp.loc[a, b] != 1 for a, b in low.index)
E(L2, 'screens[7].prose', len(low)); E(L2, 'screens[7].explain.text', len(low) - nsplit); E(L2, 'screens[7].explain.text', nsplit)
E(L2, 'screens[10].explain.text', nsplit)
tab = [('2023-10-02', 'S007'), ('2021-08-27', 'S089'), ('2021-04-21', 'S120'), ('2022-11-14', 'S002'), ('2023-01-23', 'S024'), ('2021-07-19', 'S016')]
for i, (dd, nm) in enumerate(tab):
    E(L2, f'screens[7].canvas.params.rows[{i}]', R(100 * pc.loc[dd, nm], 2))
    E(L2, f'screens[7].canvas.params.rows[{i}]', int(sp.loc[dd, nm]))
E(L2, 'screens[7].feedback.byKey.r3', R(100 * ret.loc['2022-11-14', 'S002'], 2)); E(L2, 'screens[7].feedback.byKey.r5', R(100 * ret.loc['2021-07-19', 'S016'], 2))
six = set(low.sort_values().index[:6]); shown = {(pd.Timestamp(a), b) for a, b in tab}
stated(L2, 'screens[7].prose', 'The six largest drops among them are shown', six == shown)
# the hold rule flags drops below -40% with no split and no delisting record; every one of the 14 split days has a record
flagged = [ix for ix in low.index if sp.loc[ix] == 1 and listed[ix[1]].loc[ix[0]:].iloc[1:].any()]
claim('the hold rule flags none of the 34 panel drops', len(flagged) == 0)
stated(L2, 'screens[10].explain.text', 'split days that would trip it', len(flagged) > 0)
claim('key 0.0201 within its tolerance of 1.005^4 - 1 = 0.02015', abs(lv.files['l2-splits-and-dividends']['screens'][9]['widget']['answer'] - (1.005 ** 4 - 1)) < 0.0006); E(L2, 'screens[9].widget.accept', R(100 * (1.005 ** 4 - 1), 1))
E(L2, 'quiz[0].widget.answer', R(3 * 30.60 / 90 - 1, 4)); E(L2, 'quiz[0].widget.wrong[0].value', R(30.60 / 90 - 1, 2))
E(L2, 'quiz[2].widget.answer', R((39.40 + 0.80) / 40 - 1, 4)); E(L2, 'quiz[2].widget.wrong[0].value', R(39.40 / 40 - 1, 3))
E(L2, 'quiz[3].widget.answer', 300 / 2); E(L2, 'quiz[3].explain.text', R(100 * (160 / 150 - 1), 1)); E(L2, 'quiz[3].explain.text', R(-100 * (160 / 300 - 1), 0))

# ---------- l3 ----------
L3 = 'l3'
everyone, surv = ret.mean(axis=1).mean() * 252, ret[today].mean(axis=1).mean() * 252
two('survivorship_gap agrees', R(everyone, 4), ns['survivorship_gap'](ret, listed)[0]); two('survivors agree', R(surv, 4), ns['survivorship_gap'](ret, listed)[1])
for p in ('screens[0].explain.text', 'summary.ideas[0]'):
    E(L3, p, R(100 * everyone, 2)); E(L3, p, R(100 * surv, 2))
E(L3, 'screens[0].explain.text', R(100 * surv, 2) - R(100 * everyone, 2))
E(L3, 'screens[0].canvas.state.values', R(everyone, 4)); E(L3, 'screens[0].canvas.state.values', R(surv, 4))
ia, ib = 100 * (1 + ret.mean(axis=1)).prod(), 100 * (1 + ret[today].mean(axis=1)).prod()
E(L3, 'screens[1].widget.accept', R(ia, 2)); E(L3, 'screens[1].widget.accept', R(ib, 2)); E(L3, 'screens[1].widget.answer', R(ib, 2) - R(ia, 2))
E(L3, 'screens[1].explain.text', R(listed.sum(axis=1).mean(), 0))
E(L3, 'screens[2].prose', R(rc.loc['2023-09-29', 'S007'], 2)); E(L3, 'screens[2].prose', R(rc.loc['2023-10-02', 'S007'], 2)); E(L3, 'screens[2].prose', R(100 * ret.loc['2023-10-02', 'S007'], 2))
Lg = np.log1p(ret); mom = Lg.rolling(231, min_periods=200).sum().shift(21)
fr21 = ns['forward_returns'](ret, 21)
monthly = list(range(252, 1238, 21))


def study(cols, sig=mom, fwd=fr21):
    ics, tops, bots = [], [], []
    for t in monthly:
        a, b = sig[cols].iloc[t], fwd[cols].iloc[t]
        ok = a.notna() & b.notna()
        ics.append(a[ok].rank().corr(b[ok].rank()))
        q = pd.qcut(a[ok].rank(method='first'), 5, labels=False)
        tops.append(b[ok][q == 4].mean()); bots.append(b[ok][q == 0].mean())
    ic = np.array(ics)
    return ic.mean(), ic.mean() / ic.std(ddof=1) * math.sqrt(len(ic)), 12 * np.mean(tops), 12 * np.mean(bots)


A_ = study(ret.columns); S_ = study(today)
for i, st in enumerate((A_, S_)):
    E(L3, f'screens[3].canvas.params.rows[{i}]', R(st[0], 4))
    for v in (st[2], st[3], st[2] - st[3]):
        E(L3, f'screens[3].canvas.params.rows[{i}]', R(100 * v, 2))
E(L3, 'screens[3].widget.answer', R(100 * (S_[2] - A_[2]), 2)); E(L3, 'screens[3].widget.wrong[0].value', R(100 * (S_[3] - A_[3]), 2))
E(L3, 'screens[3].widget.wrong[1].value', R(100 * ((S_[2] - S_[3]) - (A_[2] - A_[3])), 2))
dl = ns['delisting_return_kept'](ret, listed)
r2 = ret.copy()
for nm, dd, _ in dl:
    r2.loc[dd, nm] = np.nan
nodl = r2.mean(axis=1).mean() * 252
E(L3, 'screens[4].canvas.params.rows[1]', R(100 * nodl, 2))
E(L3, 'screens[4].widget.answer', R((R(100 * nodl, 2) - R(100 * everyone, 2)) / (R(100 * surv, 2) - R(100 * everyone, 2)), 3))
two('share of gap, rounded and exact', R((nodl - everyone) / (surv - everyone), 2), 0.87, 0.006)
E(L3, 'screens[4].widget.wrong[0].value', R(nodl - everyone, 4)); E(L3, 'screens[4].widget.wrong[1].value', 1 - 0.873)
sm = make_panel(30, 300, 5)
sg = ns['survivorship_gap'](sm['ret'], sm['listed'])
E(L3, 'screens[6].explain.text', R(100 * sg[0], 2)); E(L3, 'screens[6].explain.text', R(100 * sg[1], 2))
sdead = ns['delisting_return_kept'](sm['ret'], sm['listed'])
# the gap is larger on small because its 3 deaths come in 300 days: deaths per share-year, not deaths per share, differ
claim('small and full panels lose the same share of names (3/30 = 20/200)', len(sdead) / 30 == len(dl) / 200)
stated(L3, 'screens[6].explain.text', 'three deaths in 30 shares weigh more than 20 in 200', len(sdead) / 30 > len(dl) / 200)
E(L3, 'screens[7].explain.text', len(dl)); E(L3, 'screens[7].explain.text', R(100 * min(x[2] for x in dl), 2)); E(L3, 'screens[7].explain.text', R(100 * max(x[2] for x in dl), 2))
r3_ = ret.copy()
for nm, dd, _ in dl:
    r3_.loc[pd.Timestamp(dd) + pd.Timedelta(days=1):, nm] = 0.0
E(L3, 'screens[8].prose', R(100 * r3_.mean(axis=1).mean() * 252, 2))
stated(L3, 'screens[8].explain.text', 'keeps 200 shares in every row', bool((r3_.notna().sum(axis=1) == 200).all()))
mdl = np.mean([x[2] for x in dl])
E(L3, 'screens[9].prose', R(100 * mdl, 1)); E(L3, 'screens[9].widget.answer', R(4 / 187 * 0.709, 4))
E(L3, 'screens[9].widget.wrong[0].value', R(20 / 187 * 0.709, 4)); E(L3, 'screens[9].widget.wrong[1].value', R(4 / 187, 4))
E(L3, 'screens[9].feedback.correct', R(100 * (nodl - everyone), 2)); E(L3, 'screens[9].explain.text', R(100 * 0.02 * 0.7, 1))
E(L3, 'quiz[1].widget.answer', 10 / 500 * 0.6); E(L3, 'quiz[1].widget.wrong[0].value', 10 / 500)

# ---------- l4 ----------
L4 = 'l4'
Pc = [100, 101, 99.5, 102, 103.5, 101, 104, 106, 105, 107.5, 108, 110]
E(L4, 'screens[1].widget.answer', R(Pc[8] / Pc[3] - 1, 6)); E(L4, 'screens[1].widget.wrong[0].value', R(Pc[4] / Pc[3] - 1, 6))
rb = [0.01, 0.02, -0.01, 0.03, 0.0, 0.01, -0.02]
f5b = [np.prod([1 + x for x in rb[t + 1:t + 6]]) - 1 for t in range(2)]
E(L4, 'screens[3].widget.rows[0][2].answer', R(f5b[0], 6)); E(L4, 'screens[3].widget.rows[1][2].answer', R(f5b[1], 6))
E(L4, 'screens[3].explain.text', R(100 * f5b[0], 2)); E(L4, 'screens[3].explain.text', R(100 * sum(rb[1:6]), 2))
E(L4, 'screens[4].widget.answer', R(1.02 * 0.40 - 1, 3)); E(L4, 'screens[4].widget.wrong[2].value', 0.02 - 0.60)
claim('forward_returns compounds a death: 1.02 x 0.40 - 1', R(ns['forward_returns'](pd.DataFrame({'D': [0.0, 0.02, -0.6, None, None, None, None]}, dtype=float), 5)['D'].iloc[0], 6) == -0.592)
E(L4, 'screens[5].explain.text', int(ret.notna().sum().sum())); E(L4, 'screens[5].canvas.params.lines', int(ret.notna().sum().sum()))
E(L4, 'screens[7].explain.text', int(sm['ret'].notna().sum().sum()))
claim('to_long on small has one row per listed cell', len(ns['to_long'](sm['ret'])) == int(sm['ret'].notna().sum().sum()))
# the off-by-one study: weekly dates 5, 10, ..., where forward_returns(ret, 5) exists
fr5 = ns['forward_returns'](ret, 5)
past5 = Lg.rolling(5).sum()
leak5 = np.expm1(Lg.rolling(5).sum().shift(-4))
wk = [t for t in range(5, 1260, 5) if fr5.iloc[t].notna().any()]


def ic(sig, fwd, rows):
    x = []
    for t in rows:
        a, b = sig.iloc[t], fwd.iloc[t]; ok = a.notna() & b.notna()
        x.append(a[ok].rank().corr(b[ok].rank()))
    x = np.array(x)
    return x.mean(), x.mean() / x.std(ddof=1) * math.sqrt(len(x)), len(x)


ica, icb = ic(past5, fr5, wk), ic(past5, leak5, wk)
icl = ic(past5, Lg[::-1].rolling(5).sum()[::-1].shift(-1), wk)
print(f'l4 off-by-one: a {ica}, b {icb}, a with summed-log forward return {icl}')
claim('IC with a is -0.0243 (log route) or -0.0242 (forward_returns)', R(icl[0], 4) == -0.0243 or R(ica[0], 4) == -0.0243)
E(L4, 'screens[8].canvas.params.lines', R(icb[0], 4))          # stated 0.1697; recomputed 0.1694 on these 250 dates
E(L4, 'screens[8].prose', len(wk))                              # stated 249
E(L4, 'screens[8].prose', R(icb[1], 0))
mleak = ic(mom, np.expm1(Lg.rolling(21).sum().shift(-20)), monthly)
E(L4, 'screens[8].explain.text', R(A_[0], 4)); E(L4, 'screens[8].explain.text', R(mleak[0], 4))   # stated 0.0366; recomputed 0.0356
E(L4, 'screens[9].feedback.byKey.log', R(100 * (math.log(1.1) + math.log(0.9)) / 2, 2))
E(L4, 'quiz[1].widget.answer', R(1.05 ** 2 - 1, 4)); E(L4, 'quiz[3].widget.answer', 1260 * 200 - 16503); E(L4, 'quiz[3].widget.wrong[0].value', 1260 * 200)
claim('the last 21 rows of forward_returns(ret, 21) are NaN', int(fr21.iloc[-21:].notna().sum().sum()) == 0 and fr21.iloc[-22].notna().any())

# ---------- review-1 ----------
RV = 'review'
rt = [('P', True, 900, 12.0), ('Q', True, 40, 50.0), ('R', False, 700, 30.0), ('S', True, 300, 5.20), ('T', True, 650, 4.10)]
E(RV, 'items[0].widget.answer', sum(1 for _, l, n, v in rt if l and n >= 60 and v >= 5))
E(RV, 'items[1].widget.answer', 240 / 4); E(RV, 'items[1].feedback.correct', R(100 * (63 / 60 - 1), 0))
pr2 = lv.text(RV, 'items[2].prose')
if 'loses 6 a year' in pr2:
    E(RV, 'items[2].widget.answer', 6 / 300 * 0.8)
elif 'lost 40 shares to delisting over 5 years' in pr2:
    E(RV, 'items[2].widget.answer', R(8 / 250 * 0.75, 4)); E(RV, 'items[2].widget.wrong[0].value', 8 / 250); E(RV, 'items[2].widget.wrong[1].value', R(40 / 250 * 0.75, 2))
else:
    claim('review-1 items[2] prose recognised', False)
E(RV, 'items[3].widget.answer', R(1.01 * 0.98 * 1.03 - 1, 6))
claim('3 March to 1 June 2021 is at least 60 trading days', len(pd.bdate_range('2021-03-03', '2021-06-01')) >= 60)
E(RV, 'items[5].widget.answer', R(2 * (74.25 + 0.75) / 150 - 1, 4)); E(RV, 'items[5].widget.wrong[0].value', R(2 * 74.25 / 150 - 1, 4)); E(RV, 'items[5].widget.wrong[1].value', R(74.25 / 150 - 1, 3))
pr7 = lv.text(RV, 'items[7].prose')
if 'Z returns +2% and then −60%' in pr7:
    z = 1.02 * 0.40 - 1; xs = (0.03, -0.01); zl = -0.60
elif 'Z returns +3% and then −50%' in pr7:
    z = 1.03 * 0.50 - 1; xs = (0.04, -0.02); zl = -0.50
else:
    z = None; claim('review-1 items[7] prose recognised', False)
if z is not None:
    E(RV, 'items[7].widget.answer', R((sum(xs) + z) / 3, 6)); E(RV, 'items[7].widget.wrong[0].value', R(sum(xs) / 2, 4)); E(RV, 'items[7].widget.wrong[1].value', R((sum(xs) + zl) / 3, 6))
k = next(k for k in range(1, 61) if (60 - k + 10 * k) / 60 >= 5)
E(RV, 'items[8].widget.answer', k); E(RV, 'items[8].widget.accept', R((60 - k + 10 * k) / 60, 2)); E(RV, 'items[8].widget.accept', R((60 - (k - 1) + 10 * (k - 1)) / 60, 2))
E(RV, 'items[8].explain.text', R(240 / 9, 1)); E(RV, 'items[8].feedback.byKey.thirty', (30 + 300) / 60); E(RV, 'items[8].feedback.byKey.one', (59 + 10) / 60)

# ---------- homework-1 ----------
HW = 'homework'
cp = ns['clean_panel'](rc, sp, dv, listed, 5e6, adv)
held = mask.shift(1, fill_value=False)
two('clean_panel kept count, two routes', int(cp.notna().sum().sum()), int(trr.where(held).notna().sum().sum()))
E(HW, 'items[0].explain.text', int(cp.notna().sum().sum())); E(HW, 'items[0].explain.text', R(100 * cp.mean(axis=1).mean() * 252, 2))
E(HW, 'items[1].explain.text', R(100 * ns['universe_turnover'](mask), 2))
E(HW, 'items[1].feedback.byKey', R((1 / 3 + 1 / 4) / 2, 4))
pr3 = lv.text(HW, 'items[3].prose')
if 'pays £0.40 per new share' in pr3:
    E(HW, 'items[3].widget.answer', R(3 * (31.60 + 0.40) / 96 - 1, 4)); E(HW, 'items[3].widget.wrong[0].value', R(3 * 31.60 / 96 - 1, 4)); E(HW, 'items[3].widget.wrong[1].value', R(31.60 / 96 - 1, 6))
else:
    E(HW, 'items[3].widget.answer', R(96 / 3 - 31.60, 2)); E(HW, 'items[3].widget.wrong[0].value', R(96 - 3 * 31.60, 2))
E(HW, 'items[4].widget.answer', R(0.024 * 400 / 0.6, 6)); E(HW, 'items[4].widget.wrong[0].value', R(0.024 / 0.6, 4))
E(HW, 'items[4].widget.wrong', R(0.024 * 400, 1))            # the "left out the 60% loss" slip is 9.6; the item has 40
# items[5]: the two correct lines blank the last 21 rows too, and give NaN on a window with a death
la, lb = Lg.rolling(21).sum().shift(-21), Lg[::-1].rolling(21).sum()[::-1].shift(-1)
two('lines a and b agree', float((la - lb).abs().max().max()), 0.0, 1e-12)
blank = int(la.iloc[-21:].notna().sum().sum()) == 0
lost = int((fr21.notna() & la.isna()).iloc[:-21].sum().sum())
print(f'homework-1 items[5]: line a NaN where forward_returns has a value on {lost} cells')
stated(HW, 'items[5].explain.text', 'both sum only days that exist', not blank and lost == 0)
md = lv.text(HW, 'items[6].widget.model')
E(HW, 'items[6].widget.model', '26 March 2019'); E(HW, 'items[6].widget.model', nsplit); E(HW, 'items[6].widget.model', 110)
E(HW, 'items[6].widget.model', R(100 * min(x[2] for x in dl), 1)); E(HW, 'items[6].widget.model', R(100 * max(x[2] for x in dl), 1))
joins = [c for c in late if mask[c].any() and int(listed[c].loc[:mask.index[mask[c]][0]].sum()) == 60]
print(f'late listings that join on their 60th day: {len(joins)} of {len(late)}; never: {[c for c in late if not mask[c].any()]}')
stated(HW, 'items[6].widget.model', '20 shares listed late and join on their 60th trading day', len(joins) == 20)
full = listed.columns[listed.all()]
F_ = study(full)
print(f'full histories only ({len(full)} shares): top {F_[2]:.4f}, bottom {F_[3]:.4f}, spread {F_[2] - F_[3]:.4f}')
stated(HW, 'items[6].widget.model', 'lowers the spread slightly (11.02% against 11.88%)', (F_[2] - F_[3]) < (A_[2] - A_[3]))

# ---------- fix pass additions (second read findings 1 to 9, 15, 19 to 22) ----------
claim('f1: the six tabled rows are six distinct drops among the 34', len(shown) == 6 and shown <= set(low.index))
E(L2, 'screens[7].prose', 'Six of them are shown')
E(L2, 'screens[10].explain.text', len(low))
claim("f2: 20 of the 34 drops are a share's last listed day, 14 carry a split ratio", len(low) - nsplit == 20 and nsplit == 14 and len(dl) == 20)
E(L2, 'screens[10].explain.text', len(low) - nsplit)
sm_days = len(sm['ret'])
claim('f3: small has 300 days, full 1,260; 3 deaths in 30 shares and 20 in 200 are both 10%', sm_days == 300 and len(D) == 1260 and len(sdead) == 3 and len(sdead) / 30 == len(dl) / 200)
claim('f3: deaths per share-year are 0.084 on small, 0.02 on full', R(3 / 30 / (300 / 252), 3) == 0.084 and R(20 / 200 / (1260 / 252), 2) == 0.02)
E(L3, 'screens[6].explain.text', sm_days); E(L3, 'screens[6].explain.text', '1,260'); E(L3, 'screens[6].explain.text', len(sdead))
rows200 = int((r3_.notna().sum(axis=1) == 200).sum())
claim('f4: only 647 of 1,260 zero-filled rows hold 200 shares, so "every row" is false', rows200 == 647)
claim('f4: after its death a dead share is 0.0 in the filled panel, not NaN', all((r3_[nm].loc[pd.Timestamp(dd) + pd.Timedelta(days=1):] == 0.0).all() for nm, dd, _ in dl))
E(L3, 'quiz[1].widget.wrong[1].value', R(10 * 0.6 / 100, 4)); E(L3, 'quiz[1].feedback.byKey', 1.2)
E(RV, 'items[2].feedback.byKey', 8); E(RV, 'items[2].explain.text', 8); E(RV, 'items[2].explain.text', R(100 * 8 / 250, 1)); E(RV, 'items[2].explain.text', R(100 * 8 / 250 * 0.75, 1))
E(RV, 'items[2].widget.accept', R(100 * 8 / 250 * 0.75, 1))
E(RV, 'items[7].feedback.byKey', 48.5); E(RV, 'items[7].explain.text', R(100 * (0.04 - 0.02 + (1.03 * 0.5 - 1)) / 3, 1)); E(RV, 'items[7].widget.accept', R(100 * (0.04 - 0.02 + (1.03 * 0.5 - 1)) / 3, 1))
E(HW, 'items[4].feedback.byKey.forty', R(0.024 * 400, 1)); E(HW, 'items[4].feedback.byKey.forty', 0.6)
claim('f8: both right lines blank the last 21 rows and lose cells before them', blank and lost > 0)
print('f8 lost cells', lost)
E(HW, 'items[6].widget.model', len(full)); E(HW, 'items[6].widget.model', R(100 * F_[2], 2)); E(HW, 'items[6].widget.model', R(100 * F_[3], 2)); E(HW, 'items[6].widget.model', R(100 * (F_[2] - F_[3]), 2))
E(HW, 'items[6].widget.model', R(100 * A_[2], 2)); E(HW, 'items[6].widget.model', R(100 * A_[3], 2)); E(HW, 'items[6].widget.model', R(100 * (A_[2] - A_[3]), 2))
E(HW, 'items[6].widget.rubric[2].text', R(100 * (F_[2] - A_[2]), 1)); E(HW, 'items[6].widget.rubric[2].text', R(100 * ((F_[2] - F_[3]) - (A_[2] - A_[3])), 1))
claim('f9: 160 shares listed on every day (200 less 20 deaths and 20 late)', len(full) == 160)
claim('f9: 19 of 20 late listings join on their 60th day; S073 never passes the filter', len(joins) == 19 and [c for c in late if not mask[c].any()] == ['S073'])
E(HW, 'items[6].widget.model', 'S073')
claim('f9: S073 trades about £3.3m a day', R(adv['S073'] / 1e6, 1) == 3.3)
claim('f9: bias 3 on the panel raises both fifths and the spread', F_[2] > A_[2] and F_[3] > A_[3] and (F_[2] - F_[3]) > (A_[2] - A_[3]))
claim('f15: 1m for 500 days then 10m for 100 days averages 2.5m, below 5m', (1 * 500 + 10 * 100) / 600 == 2.5)
E(HW, 'items[3].widget.wrong[1].value', R(96 - 31.60, 2)); E(HW, 'items[3].feedback.byKey', 1.2); E(HW, 'items[3].explain.text', 32)
claim('f22: a 3-for-1 split with D = 0.40 gives total return 0', abs(3 * (31.60 + 0.40) / 96 - 1) < 1e-12)

lv.check_wrongs()
# a % key is a fraction: every % wrong value must be at or below 1 (validator item 515 warning)
for fid, d in lv.files.items():
    def walk(n, p):
        if isinstance(n, dict):
            if n.get('unit') == '%' and isinstance(n.get('wrong'), list) and not n.get('over100'):
                for i, w in enumerate(n['wrong']):
                    v = w.get('value')
                    if isinstance(v, (int, float)):
                        lv._rec(abs(v) <= 1, f'{fid} {p}.wrong[{i}] "{w.get("id")}" = {v} is a fraction (unit %)', '' if abs(v) <= 1 else 'typed as a per cent figure this is never reached')
            for k2, v2 in n.items():
                walk(v2, f'{p}.{k2}' if p else k2)
        elif isinstance(n, list):
            for i, v2 in enumerate(n):
                walk(v2, f'{p}[{i}]')
    walk(d, '')
for f in fails:
    print('BAD', f)
if fails:
    lv.results.append((False, 'route agreement', ''))
lv.report()
