"""Recompute every number stated in alpha level 2 (Signals) and check it at its JSON path (second read).

Run: python3 docs/reports/alpha-L2-numbers.py   (NumPy, pandas and the standard library; exits 0 when every check passes)

The panel is the brief's `make_panel()` (seed 2310) from l1's prelude. Signals are built here by direct code
(log sums, ranks, z-scores, sector means, least squares) and the lessons' solutions are run as a second route
(`two`). Rank ICs follow the course's Level 2 convention: the forward return is the summed log return over
t+1..t+h (`L[::-1].rolling(h).sum()[::-1].shift(-1)`), monthly dates 252, 273, ... below 1,238 (47), weekly
dates 5, 10, ... `E` checks a stated value appears where it is stated; `stated` ties a claim to its wording.
A check that fails because the content is wrong is a finding in docs/reviews/review-alpha-1-2.md and stays
failing until the fix pass corrects the content.
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

lv = Level("alpha", 2)
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


ns = {}
exec(doc('l1-choosing-a-universe')['screens'][6]['widget']['prelude'], ns)
for fid, idx in [('l5-momentum-signal', [4]), ('l6-reversal-signal', [4, 6]), ('l7-ranks-and-z', [4, 5]), ('l8-neutralising', [3, 5])]:
    for i in idx:
        exec(doc(fid)['screens'][i]['widget']['solution'], ns)
for i in (0, 1):
    exec(doc('homework-2')['items'][i]['widget']['solution'], ns)
P = ns['make_panel']()
ret, listed, beta, sector = P['ret'], P['listed'], P['beta'], P['sector']
Lg = np.log1p(ret)
monthly = list(range(252, 1238, 21))
weekly = list(range(5, 1260, 5))


def fwd(h):
    return Lg[::-1].rolling(h).sum()[::-1].shift(-1)


def ic(sig, f, rows):
    x = []
    for t in rows:
        a, b = sig.iloc[t], f.iloc[t]; ok = a.notna() & b.notna()
        if ok.sum() >= 3:
            x.append(a[ok].rank().corr(b[ok].rank()))
    x = np.array(x)
    return x.mean(), x.mean() / x.std(ddof=1) * math.sqrt(len(x)), len(x)


f21, f5 = fwd(21), fwd(5)
mom = Lg.rolling(231, min_periods=200).sum().shift(21).where(ret.notna())
two('momentum_12_1 agrees', float((ns['momentum_12_1'](ret) - mom).abs().max().max()), 0.0)

# ---------- l5 ----------
L5 = 'l5'
s0 = lv.files['l5-momentum-signal']['screens'][0]['canvas']['params']['series']
A, Bs = s0[0]['values'], s0[1]['values']
claim('both hook shares rose 30% over the year', A[-1] / A[0] == 1.3 and Bs[-1] / Bs[0] == 1.3)
E(L5, 'screens[0].explain.text', A[231]); E(L5, 'screens[0].explain.text', Bs[231]); E(L5, 'screens[0].explain.text', R(-100 * (Bs[231] / Bs[0] - 1), 2))
E(L5, 'screens[0].hints[2]', R(A[231], 0))
idx = np.r_[1.0, (1 + ret['S019'].iloc[1008:]).cumprod().values]
claim('S019 index covers the last 253 closes', len(idx) == 253)
E(L5, 'screens[1].widget.answer', R(idx[231] / idx[0] - 1, 3)); E(L5, 'screens[1].widget.wrong[0].value', R(idx[-1] / idx[0] - 1, 4))
E(L5, 'screens[1].widget.wrong[1].value', R(idx[-1] / idx[231] - 1, 4))
E(L5, 'screens[7].explain.text', R(Lg['S019'].iloc[1008:1239].sum(), 4))
two('S019 log sum equals ln of the window ratio', R(Lg['S019'].iloc[1008:1239].sum(), 6), R(math.log(idx[231] / idx[0]), 6))
two('S019 stored canvas agrees', lv.files['l5-momentum-signal']['screens'][1]['canvas']['params']['params']['px'][231], R(100 * idx[231], 2), 1e-6)
E(L5, 'screens[2].widget.answer', 251 - 21 + 1)
E(L5, 'screens[5].hints[2]', 167 - 21 + 1); E(L5, 'screens[5].explain.text', 200 + 21 - 1)
tab = {'Avon': 20, 'Brent': 42, 'Clyde': 9, 'Dee': 35, 'Esk': 15, 'Forth': 28}
top = sorted(tab, key=tab.get, reverse=True)
claim('top third Brent and Dee, bottom third Clyde and Esk, Forth third, Avon fourth', top[:2] == ['Brent', 'Dee'] and set(top[-2:]) == {'Clyde', 'Esk'} and top[2] == 'Forth' and top[3] == 'Avon')
im, i0, il = ic(mom, f21, monthly), ic(Lg.rolling(252, min_periods=200).sum().where(ret.notna()), f21, monthly), ic(Lg.rolling(231, min_periods=200).sum().shift(-21), f21, monthly)
for p in ('screens[6].feedback.correct', 'screens[6].explain.text', 'summary.ideas[1]'):
    E(L5, p, R(im[0], 4)); E(L5, p, R(i0[0], 4))
claim('momentum IC over 47 dates, t 2.64', im[2] == 47 and R(im[1], 2) == 2.64)
E(L5, 'quiz[0].prose', R(il[0], 2)); E(L5, 'quiz[0].prose', R(il[1], 1)); E(L5, 'quiz[0].explain.text', R(il[0], 4))
E(L5, 'quiz[0].explain.text', 230 - 21)
E(L5, 'quiz[1].widget.answer', R(math.exp(0.18) - 1, 4))
E(L5, 'screens[6].explain.text', 1990)

# ---------- l6 ----------
L6 = 'l6'
s6 = lv.files['l6-reversal-signal']['screens'][0]['canvas']['params']['series']
E(L6, 'screens[0].explain.text', s6[0]['values'][14]); E(L6, 'screens[0].explain.text', s6[1]['values'][-1])
claim('hook falls 8% in five days', R(s6[0]['values'][14] / s6[0]['values'][10] - 1, 4) == -0.08)
E(L6, 'screens[1].widget.answer', R(math.log(0.5) / math.log(0.8), 1)); E(L6, 'screens[1].widget.accept', R(math.log(0.5) / math.log(0.8), 3))
E(L6, 'screens[1].widget.wrong[0].value', 0.5 / 0.2); E(L6, 'screens[1].explain.text', R(100 * 0.8 ** 5, 0))
rs = [-0.02, -0.015, -0.03, 0.005, -0.02]
E(L6, 'screens[2].widget.answer', R(-sum(math.log1p(x) for x in rs), 4)); E(L6, 'screens[2].widget.wrong[1].value', R(-sum(rs), 4))
for x in rs:
    E(L6, 'screens[2].explain.text', R(math.log1p(x), 4))
ics = {h: ic(-Lg.rolling(h, min_periods=h).sum(), f5, weekly) for h in (1, 5, 21)}
for h in (1, 5, 21):
    E(L6, 'screens[3].explain.text', R(ics[h][0], 4))
E(L6, 'screens[3].explain.text', R(ics[5][1], 2)); E(L6, 'summary.ideas[1]', R(ics[5][1], 2)); E(L6, 'summary.ideas[1]', ics[5][2])
two('reversal_5d agrees', float((ns['reversal_5d'](ret) + Lg.rolling(5, min_periods=5).sum()).abs().max().max()), 0.0)
rv = -Lg.rolling(5, min_periods=5).sum()


def autocorr(sig, lag):
    b = sig.shift(lag)
    out = []
    for t in range(len(sig)):
        x, y = sig.iloc[t], b.iloc[t]; ok = x.notna() & y.notna()
        if ok.sum() >= 3:
            out.append(x[ok].rank().corr(y[ok].rank()))
    return R(np.mean(out), 4)


ac = {(n, k): autocorr(s, k) for n, s in (('mom', mom), ('rev', rv)) for k in (1, 5)}
two('signal_autocorr agrees (rev, 5)', ns['signal_autocorr'](rv, 5), ac[('rev', 5)])
E(L6, 'summary.ideas[2]', R(ac[('rev', 1)], 2)); E(L6, 'screens[9].prose', R(ac[('rev', 5)], 2))
E(L6, 'quiz[2].explain.text', R(ac[('mom', 1)], 2))
E(L6, 'screens[7].widget.options', R(-math.log(60.40 / 120.00), 2)); E(L6, 'screens[7].explain.text', R(100 * (60.40 / 60.00 - 1), 2))
E(L6, 'screens[8].widget.answer', R(math.log(0.5) / math.log(0.9), 2)); E(L6, 'screens[8].widget.wrong[0].value', R(math.log(0.9) / math.log(0.5), 3)); E(L6, 'screens[8].widget.wrong[1].value', 0.5 / 0.1)
E(L6, 'quiz[3].widget.answer', R(0.8 ** 5, 4)); E(L6, 'quiz[3].widget.wrong[0].value', 1 - 5 * 0.2)
stated(L6, 'quiz[3].explain.text', 'Half went in the first three days', 1 - 0.8 ** 3 >= 0.5)
E(L6, 'quiz[3].explain.text', R(0.8 ** 3, 2)); claim('0.8^3 = 0.512 is left, 48.8% went (stated as about half)', R(1 - 0.8 ** 3, 3) == 0.488)

# ---------- l7 ----------
L7 = 'l7'
m8 = {'Avon': 12, 'Brent': 8, 'Clyde': 5, 'Hale': 180, 'Dee': 2, 'Esk': -3, 'Forth': -6, 'Glen': -10}
mu = sum(m8.values()) / 8
E(L7, 'screens[0].hints[1]', sum(m8.values())); E(L7, 'screens[0].hints[1]', mu)
claim('only Hale beats the average', [k for k, v in m8.items() if v > mu] == ['Hale'])


def z(vals, x):
    v = np.array(vals, float)
    return (x - v.mean()) / v.std(ddof=1)


others = [v for k, v in m8.items() if k != 'Hale']
E(L7, 'screens[1].widget.options', R(z(others + [180], 180), 2)); E(L7, 'screens[1].widget.options', R(z(others + [20], 20), 2))
ranks = pd.Series(m8).rank()
sc = ((ranks - 1) / 7 - 0.5).round(3)
for i, nm in enumerate(['Glen', 'Dee', 'Avon', 'Hale']):
    E(L7, f'screens[2].widget.rows[{i}][1].answer', sc[nm])
sc3 = pd.Series([1.5, 2.5, 2.5, 4, 5]); E(L7, 'screens[3].widget.rows[1][1].answer', (2.5 - 1) / 4 - 0.5); E(L7, 'screens[3].widget.rows[5][1].answer', (4 - 1) / 4 - 0.5)
E(L7, 'screens[5].explain.text', R(z([0] * 11 + [1], 1), 3)); E(L7, 'screens[5].explain.text', R(7 / math.sqrt(8), 2))
csr, csz = ns['cs_rank'](mom), ns['cs_zscore'](mom)
for s in (csr, csz):
    E(L7, 'screens[7].explain.text', R(ic(s, f21, monthly)[0], 4))
zr = mom.sub(mom.mean(axis=1), axis=0).div(mom.std(axis=1), axis=0)
E(L7, 'screens[7].explain.text', int((zr.abs() > 3).sum().sum())); E(L7, 'screens[7].explain.text', int(zr.notna().sum().sum()))
pos = sum((j + 0.5) / 199 for j in range(100))
E(L7, 'screens[9].widget.answer', R(0.5 / pos, 4)); E(L7, 'screens[9].hints[2]', R(pos, 2)); E(L7, 'screens[9].widget.wrong[1].value', 0.5 / 100)
q1 = pd.Series([0.3, 0.1, 0.5, 0.1, 0.2]).rank()
E(L7, 'quiz[1].widget.answer', (q1[1] - 1) / 4 - 0.5)
E(L7, 'quiz[3].widget.answer', R(z([0] * 7 + [1], 1), 4)); E(L7, 'quiz[3].widget.wrong[0].value', R(0.875 / np.std([0] * 7 + [1]), 4))
E(L7, 'quiz[3].explain.text', R(np.std([0] * 7 + [1], ddof=1), 4))

# ---------- l8 ----------
L8 = 'l8'
s8 = {'Arc': (0.30, 'T'), 'Bit': (0.27, 'T'), 'Core': (0.24, 'T'), 'Dyn': (0.23, 'T'), 'Ely': (0.10, 'B'), 'Fen': (0.04, 'B'), 'Gar': (0.06, 'U'), 'Hol': (-0.04, 'U')}
df = pd.DataFrame(s8, index=['m', 's']).T
means = df.groupby('s')['m'].transform('mean')
dm = (df['m'] - means).round(4)
for sec_, v in df.groupby('s')['m'].mean().round(2).items():
    E(L8, 'screens[1].prose', v)
claim('top four raw are the four Tech shares', set(df['m'].astype(float).nlargest(4).index) == {'Arc', 'Bit', 'Core', 'Dyn'})
claim('Gar leads after demeaning, then Arc and Ely', list(dm.astype(float).nlargest(3).index) == ['Gar', 'Arc', 'Ely'])
for i, nm in enumerate(['Bit', 'Fen', 'Hol', 'Dyn']):
    E(L8, f'screens[2].widget.rows[{i}][1].answer', dm[nm])
corrs = pd.Series({ret.index[t]: mom.iloc[t][mom.iloc[t].notna()].corr(beta[mom.iloc[t].notna()]) for t in monthly})
t7 = list(ret.index).index(corrs.idxmax())
E(L8, 'screens[4].question', R(corrs.max(), 3)); E(L8, 'screens[4].prose', corrs.idxmax().date().isoformat()); E(L8, 'screens[4].prose', int(mom.iloc[t7].notna().sum()))
E(L8, 'screens[4].prose', R(100 * ((1 + ret.mean(axis=1).iloc[t7 - 251:t7 - 20]).prod() - 1), 0))
E(L8, 'screens[4].explain.text', R(corrs.min(), 2)); E(L8, 'screens[4].explain.text', R(corrs.max(), 2))
dmf = ns['demean_by_group'](mom, sector)
sub = mom.iloc[monthly]
nt = ns['neutralise'](sub, beta, sector)
idm, intl = ic(dmf, f21, monthly), ic(nt, f21.iloc[monthly], range(len(monthly)))
E(L8, 'screens[7].explain.text', R(idm[0], 4)); E(L8, 'screens[7].explain.text', R(intl[0], 4)); E(L8, 'screens[7].explain.text', R(intl[1], 2))
E(L8, 'screens[7].explain.text', R(np.nanmean([nt.iloc[i].rank().corr(sub.iloc[i].rank()) for i in range(len(monthly))]), 2))
claim('neutralising keeps about four fifths of the IC', R(intl[0] / im[0], 1) == 0.8)
# a direct least-squares residual on one date agrees with neutralise
t = monthly[10]; y = sub.iloc[10]; ok = y.notna()
X = np.column_stack([np.ones(ok.sum()), beta[ok], pd.get_dummies(sector[ok]).to_numpy(float)])
e = y[ok].to_numpy() - X @ np.linalg.lstsq(X, y[ok].to_numpy(), rcond=None)[0]
two('neutralise agrees with direct lstsq', float(np.abs(e - nt.iloc[10][ok].to_numpy()).max()), 0.0, 1e-12)
claim('residuals sum to 0 in every sector and are uncorrelated with beta', abs(float((e * beta[ok]).sum())) < 1e-12 and all(abs(e[(sector[ok] == k).to_numpy()].sum()) < 1e-12 for k in range(5)))
E(L8, 'quiz[1].widget.answer', R(0.12 - (0.12 + 0.05 - 0.02) / 3, 4))

# ---------- review-2 ----------
RV = 'review'
E(RV, 'items[0].widget.answer', R(math.log(52 / 40), 4)); E(RV, 'items[0].widget.wrong[0].value', R(math.log(49 / 40), 4)); E(RV, 'items[0].widget.wrong[1].value', 52 / 40 - 1)
E(RV, 'items[1].explain.text', R(-math.log(0.93), 3)); E(RV, 'items[1].explain.text', R(-math.log(1.06), 3))
r2 = pd.Series([0.2, np.nan, 0.5, 0.2, 0.9, 0.1, 0.2]).rank()
E(RV, 'items[2].widget.answer', R((r2[0] - 1) / 5 - 0.5, 4)); E(RV, 'items[2].widget.wrong[0].value', R((r2[0] - 1) / 6 - 0.5, 4)); E(RV, 'items[2].widget.wrong[1].value', R(1 / 5 - 0.5, 4))
E(RV, 'items[3].widget.answer', R(0.08 - 0.05, 4)); E(RV, 'items[3].widget.wrong[0].value', R(0.08 - 0.10 / 3, 4))
E(RV, 'items[4].prose', R(ac[('mom', 5)], 2)); E(RV, 'items[4].prose', R(ac[('rev', 5)], 2))
E(RV, 'items[5].explain.text', 115); E(RV, 'items[5].explain.text', 115 - 21)
E(RV, 'items[7].widget.answer', next(n for n in range(2, 50) if (n - 1) / math.sqrt(n) > 3)); E(RV, 'items[7].widget.accept', R(10 / math.sqrt(11), 3)); E(RV, 'items[7].widget.accept', R(9 / math.sqrt(10), 3))
pr8 = lv.text(RV, 'items[8].prose')
if 'keeps 70% of itself' in pr8:
    E(RV, 'items[8].widget.answer', R(math.log(0.5) / math.log(0.7), 3)); E(RV, 'items[8].widget.wrong[0].value', R(0.5 / 0.3, 3))
elif 'half of itself every 2 days' in pr8:
    E(RV, 'items[8].widget.answer', R(math.sqrt(0.5), 4)); E(RV, 'items[8].widget.wrong[0].value', 0.75); E(RV, 'items[8].explain.text', R(math.log(0.5) / math.log(math.sqrt(0.5)), 0))
else:
    claim('review-2 items[8] prose recognised', False)

# ---------- homework-2 ----------
HW = 'homework'
sm = ns['make_panel'](30, 600, 5)
bh = ns['rolling_beta'](sm['ret'], sm['ret'].mean(axis=1)).iloc[-1]; ok = bh.notna()
E(HW, 'items[0].feedback.correct', R(bh[ok].corr(sm['beta'][ok]), 2)); E(HW, 'items[0].explain.text', R((bh[ok] - sm['beta'][ok]).abs().mean(), 2))
sg, bb = np.array([0.10, 0.04, 0.07, -0.01]), np.array([1.2, 0.8, 1.0, 1.0])
slope = ((bb - bb.mean()) * (sg - sg.mean())).sum() / ((bb - bb.mean()) ** 2).sum()
icpt = sg.mean() - slope * bb.mean()
E(HW, 'items[4].widget.answer', R(sg[0] - icpt - slope * bb[0], 4)); E(HW, 'items[4].widget.accept', R(slope, 2)); E(HW, 'items[4].widget.accept', R(icpt, 2))
E(HW, 'items[4].widget.wrong[1].value', R(sg[0] - (sg @ bb) / (bb @ bb) * bb[0], 4)); E(HW, 'items[4].widget.wrong[0].value', R(sg[0] - sg.mean(), 4))
E(HW, 'items[5].prose', R(100 * (1 - R(intl[0], 4) / R(im[0], 4)), 0))
need = int(re.search(r'needs (\d+) returns', lv.text(HW, 'items[6].prose')).group(1))
E(HW, 'items[6].widget.answer', need + 21 - 1); E(HW, 'items[6].widget.wrong[1].value', need + 21)
E(HW, 'items[6].explain.text', need); E(HW, 'items[6].explain.text', need + 20); E(HW, 'items[6].explain.text', (200 + 20) - (need + 20)); E(HW, 'items[6].widget.wrong[0].value', need)
claim('150-return rule: first score 170 days after L', need == 150 and need + 20 == 170)
E(HW, 'items[3].model', R(ics[5][0], 4)); E(HW, 'items[3].model', R(ics[5][1], 2))
# the time-series z-score look-ahead pushes the reversal IC up on our panel
ts = lambda x: (x - x.mean()) / x.std()
claim('per-share whole-history z-score raises reversal IC', ic(ts(rv), f5, weekly)[0] > ics[5][0])
# continuity: level 3 (l9) and level 1 (l3, l4) report momentum IC 0.0334 with forward_returns; level 2 reports 0.0325
fr21 = ns['forward_returns'](ret, 21) if 'forward_returns' in ns else None
if fr21 is not None:
    ic_fr = ic(mom, fr21, monthly)[0]
    E(L5, 'screens[6].prose', R(ic_fr, 4)); claim('level 2 IC 0.0325 (summed log) differs from forward_returns IC 0.0334', R(im[0], 4) == 0.0325 and R(ic_fr, 4) == 0.0334)
lv.check_wrongs()
for f in fails:
    print('BAD', f)
if fails:
    lv.results.append((False, 'route agreement', ''))
lv.report()
