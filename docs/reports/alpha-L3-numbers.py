"""Second-reader number checks for alpha level 3 (l9 to l12, review-3, homework-3).

Panel numbers are recomputed in CPython by running the course's own functions (the lesson preludes and the
solutions of the level 3 code screens, read from the content JSON) on make_panel() with seed 2310. The headline
monthly IC is checked a second way with scipy.stats.spearmanr date by date. Hand numbers are recomputed from their
closed forms. Each value is then looked up where it is stated (app/tools/numbers_lib.py). Claims that are not
single numbers use claim_text(...): it fails while the wrong phrase is still in the content.
A failing check means the content is wrong (see docs/reviews/review-alpha-3-4.md) and stays failing until fixed.
Run: python3 docs/reports/alpha-L3-numbers.py
"""
import json, math, os, sys, warnings
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('alpha', 3)
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'alpha')
J = lambda f: json.load(open(os.path.join(C, f + '.json'), encoding='utf8'))
E = lv.expect


def r(v, k):
    return round(float(v), k)


def claim_text(ref, path, phrase, ok, label):
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', '' if present else '(phrase gone)')


# ---- the course's code -------------------------------------------------------------------------------------
g = {}
exec(J('homework-3')['items'][6]['widget']['prelude'], g)          # make_panel .. spread_stats, as the course defines them
exec(J('homework-3')['items'][5]['widget']['solution'], g)         # newey_west_t
exec(J('l10-decay')['screens'][6]['widget']['solution'], g)        # lagged_ic
for i in (3, 4, 8):
    exec(J('l12-combining')['screens'][i]['widget']['solution'], g)  # signal_corr, combine, best_weight
rank_ic, ic_summary, comb = g['rank_ic'], g['ic_summary'], g['combine']
P = g['make_panel']()
ret = P['ret']
mom, rev = g['momentum_12_1'](ret), g['reversal_5d'](ret)
F = {h: g['forward_returns'](ret, h) for h in (5, 21)}
t47 = list(range(252, 1238, 21))

# ---- l9 ------------------------------------------------------------------------------------------------------
ic = rank_ic(mom.iloc[t47], F[21].iloc[t47]); s = ic_summary(ic, 12)
sp = [spearmanr(*[x[m] for x in (mom.iloc[k], F[21].iloc[k])]).correlation
      for k in t47 for m in [mom.iloc[k].notna() & F[21].iloc[k].notna()]]
lv._rec(abs(np.mean(sp) - s['mean']) < 1e-4, 'monthly IC mean by scipy spearmanr equals rank_ic', f'{np.mean(sp):.6f}')
E('l9', 'screens[1].question', len(ic))
neg = int((ic < 0).sum())
E('l9', 'screens[1].widget.answer', neg); E('l9', 'screens[1].widget.accept', len(ic) - neg)
E('l9', 'screens[1].explain.text', s['mean']); E('l9', 'screens[1].explain.text', r(100 * s['hit'], 0))
E('l9', 'screens[1].canvas.params.hlines[1].label', r(s['mean'], 3))
k = ret.index.get_loc(pd.Timestamp('2021-02-04')); m = mom.iloc[k].notna() & F[21].iloc[k].notna()
E('l9', 'screens[0].prose', int(m.sum()))
E('l9', 'screens[0].feedback.correct', r(spearmanr(mom.iloc[k][m], F[21].iloc[k][m]).correlation, 3))
sig_r, ret_r = [5, 2, 3, 6, 1, 4], [4, 2, 5, 6, 3, 1]
d2 = sum((a - b) ** 2 for a, b in zip(sig_r, ret_r))
E('l9', 'screens[2].explain.text', d2); E('l9', 'screens[2].explain.text', r(1 - 6 * d2 / 210, 3))
pts = J('l9-information-coefficient')['screens'][4]['canvas']['params']['points']
x = np.array([p[0] for p in pts], float); y = np.array([p[1] for p in pts], float)
for v in (np.corrcoef(x, y)[0, 1], spearmanr(x, y).correlation, np.corrcoef(x[1:], y[1:])[0, 1], spearmanr(x[1:], y[1:]).correlation):
    E('l9', 'screens[4].explain.text', r(v, 2))
for v in (s['mean'], s['sd'], r(s['ir'], 2), r(s['t'], 2), r(100 * s['hit'], 0)):
    E('l9', 'screens[5].explain.text', v)
br = 185 * 12
E('l9', 'screens[6].widget.answer', r(0.0334 * math.sqrt(br), 2)); E('l9', 'screens[6].widget.accept', br)
for v in (0.0334 * math.sqrt(185), 0.0334 * math.sqrt(12)):
    E('l9', 'screens[6].widget.wrong', r(v, 2))
E('l9', 'screens[6].widget.wrong', r(0.0334 * br, 1))
dic = rank_ic(mom, F[21]); ds = ic_summary(dic, 252)
E('l9', 'screens[7].prose', len(dic)); E('l9', 'screens[7].prose', ds['mean']); E('l9', 'screens[7].prose', r(ds['t'], 2))
E('l9', 'screens[7].explain.text', round(len(dic) / 21)); E('l9', 'screens[7].explain.text', r(ds['t'] / math.sqrt(21), 2))
E('l9', 'screens[8].explain.text', r(s['mean'] / s['sd'], 3)); E('l9', 'screens[8].explain.text', r(math.sqrt(47), 2))
E('l9', 'screens[9].widget.options[0].text', r(0.25 * math.sqrt(52), 2)); E('l9', 'screens[9].widget.options[1].text', r(0.25 * math.sqrt(104), 2))
E('l9', 'quiz[0].widget.answer', r(1 - 6 * 4 / 120, 1)); E('l9', 'quiz[0].widget.wrong', r(1 - 6 * 4 / 240, 1))
E('l9', 'quiz[2].widget.answer', r(0.02 / 0.09 * math.sqrt(60), 2))
E('l9', 'quiz[2].widget.wrong', r(0.02 / 0.09 * math.sqrt(12), 2)); E('l9', 'quiz[2].widget.wrong', r(0.02 / 0.09 * 60, 2))
claim_text('l9', 'screens[1].prose', 'month-ends', False, 'the 47 dates are 21 trading days apart (20 Dec, 20 Jan, 18 Feb ...), not month-ends')

# ---- l10 -----------------------------------------------------------------------------------------------------
hm = g['ic_by_horizon'](mom, ret, [1, 5, 21, 63], 1); hr = g['ic_by_horizon'](rev, ret, [1, 5, 21, 63], 1)
F[1], F[63] = g['forward_returns'](ret, 1), g['forward_returns'](ret, 63)
raw_h = lambda sg, h: rank_ic(sg.iloc[::h], F[h].iloc[::h]).mean()     # unrounded, step 1: dates h rows apart
for h in (1, 5, 21, 63):
    E('l10', 'screens[0].explain.text', r(raw_h(rev, h), 3)); E('l10', 'screens[0].explain.text', r(raw_h(mom, h), 3))
    E('l10', 'screens[4].canvas.params.rows', hr.loc[h, 'mean']); E('l10', 'screens[4].canvas.params.rows', r(hr.loc[h, 't'], 2))
    E('l10', 'screens[4].canvas.params.rows', int(hr.loc[h, 'n']))
    E('l10', 'screens[5].canvas.params.rows', hm.loc[h, 'mean']); E('l10', 'screens[5].canvas.params.rows', int(hm.loc[h, 'n']))
    E('l10', 'screens[7].hints[2].text', r(hm.loc[h, 'mean'] / math.sqrt(h), 4))
E('l10', 'screens[7].widget.options[3].why', r(hm.loc[63, 't'], 2)); E('l10', 'screens[7].widget.options[3].why', r(hm.loc[1, 't'], 2))
lag = g['lagged_ic'](rev, F[5], range(11))
for kk in (0, 1, 2):
    E('l10', 'screens[1].explain.text', lag[kk])
E('l10', 'screens[1].widget.options[1].why', r(lag[0] / 2, 4)); E('l10', 'screens[1].widget.options[2].why', lag[4])
for kk in (0, 63, 252):
    E('l10', 'screens[3].explain.text', r(rank_ic(mom.shift(kk), F[21]).mean(), 3))
E('l10', 'screens[2].hints[2].text', r(math.log(0.5) / math.log(0.8), 2))
E('l10', 'screens[3].widget.answer', r(math.log(0.5) / math.log(0.995), 1))
E('l10', 'screens[3].widget.wrong', 0.5 / 0.005); E('l10', 'screens[3].widget.wrong', 1 / 0.005)
E('l10', 'screens[5].widget.answer', 1260 // 63); E('l10', 'screens[5].widget.wrong', 1260 - 63); E('l10', 'screens[5].widget.wrong', 1260 // 21)
E('l10', 'screens[5].explain.text', int(np.argmax(mom.notna().sum(axis=1).to_numpy() >= 10)))
gh = {}
w6 = J('l10-decay')['screens'][6]['widget']; exec(w6['prelude'], gh)
E('l10', 'screens[6].explain.text', r(gh['rank_ic'](gh['hand_sig'].shift(-1), gh['hand_fwd'], 3).mean(), 2))
E('l10', 'screens[8].widget.options[0].text', r(0.0202 * math.sqrt(5), 3))
for nm, h in (('Daily', 1), ('Weekly', 5), ('Monthly', 21)):
    E('l10', 'screens[9].canvas.params.rows', r(hr.loc[h, 'mean'] * math.sqrt(252 / h), 2))
E('l10', 'quiz[0].widget.answer', r(math.log(0.5) / math.log(0.9), 2))
E('l10', 'quiz[2].widget.answer', r(0.01 * math.sqrt(16), 2))

# ---- l11 -----------------------------------------------------------------------------------------------------
qr = g['quantile_returns'](rev.iloc[::5], F[5].iloc[::5]); st = g['spread_stats'](qr, 52)
E('l11', 'screens[0].prose', len(qr))
for v in qr.mean():
    E('l11', 'screens[0].explain.text', r(100 * v, 2)); E('l11', 'screens[0].explain.canvas.values', r(100 * v, 3))
E('l11', 'screens[0].explain.text', r(100 * st['mean'], 2))
rows = J('l11-quintiles')['screens'][3]['canvas']['params']['rows']
nr = [float(rw[4].replace('%', '').replace('−', '-')) for rw in rows]
for b in range(5):
    E('l11', 'screens[1].explain.text', r((nr[2 * b] + nr[2 * b + 1]) / 2, 2))
qm = g['quantile_returns'](mom.iloc[t47], F[21].iloc[t47]); sm = g['spread_stats'](qm, 12); spr = qm[5] - qm[1]
E('l11', 'screens[2].widget.answer', int((spr > 0).sum())); E('l11', 'screens[2].widget.wrong', int((spr < 0).sum()))
E('l11', 'screens[2].explain.text', r(100 * spr.sum(), 0))
for v in (100 * sm['mean'], 100 * sm['sd'], sm['sharpe']):
    E('l11', 'screens[2].explain.text', r(v, 2)); E('l11', 'screens[6].explain.text', r(v, 2))
for v in qm.mean():
    E('l11', 'screens[5].canvas.state.values', r(100 * v, 3))
E('l11', 'screens[5].explain.text', r(100 * (spr > 0).mean(), 0))
E('l11', 'screens[5].explain.text', r(((mom.iloc[t47].notna() & F[21].iloc[t47].notna()).sum(axis=1) / 5).mean(), 0))
sd10 = g['spread_stats'](g['quantile_returns'](mom.iloc[t47], F[21].iloc[t47], 10), 12)
for v in (100 * sd10['mean'], 100 * sd10['sd'], sd10['sharpe']):
    E('l11', 'screens[6].explain.text', r(v, 2))
S, Fw = mom.iloc[t47], F[21].iloc[t47]; both = S.notna() & Fw.notna()
vals = S.where(both).to_numpy().ravel(); vals = vals[~np.isnan(vals)]
cuts = np.quantile(vals, [0.2, 0.4, 0.6, 0.8])
bk = pd.DataFrame(np.searchsorted(cuts, np.nan_to_num(S.to_numpy(), nan=-9), side='right') + 1, index=S.index, columns=S.columns).where(both)
top = (bk == 5).sum(axis=1); sws = Fw.where(bk == 5).mean(axis=1) - Fw.where(bk == 1).mean(axis=1)
E('l11', 'screens[7].widget.options[0].text', int(top.min())); E('l11', 'screens[7].widget.options[0].text', int(top.max()))
E('l11', 'screens[7].prose', r(sws.mean() / sws.std() * math.sqrt(12), 2))


def buckets(n, q=5, ranks=None):
    ranks = ranks or list(range(1, n + 1))
    out = [0] * q
    for rk in ranks:
        out[math.ceil(q * rk / n - 1e-12) - 1] += 1
    return out


E('l11', 'screens[4].widget.answer', buckets(10, ranks=[1, 2, 3, 4.5, 4.5, 6, 7, 8, 9, 10])[2])
E('l11', 'screens[8].widget.answer', math.ceil(50 / 23))
b23, b12 = buckets(23), buckets(12)
claim_text('l11', 'screens[8].explain.text', '4, 5, 5, 4 and 5', b23 == [4, 5, 5, 4, 5], f'23 shares give buckets {b23}')
claim_text('l11', 'quiz[2].explain.text', '3, 2, 2, 3 and 2', b12 == [3, 2, 2, 3, 2], f'12 shares give buckets {b12}')
E('l11', 'quiz[2].widget.answer', math.ceil(35 / 12))
E('l11', 'quiz[0].widget.answer', r(0.012 - 0.004, 4)); E('l11', 'quiz[0].widget.wrong', r(0.012 - 0.009, 4))
E('l11', 'quiz[0].widget.wrong', r(np.mean([0.004, 0.006, 0.005, 0.009, 0.012]), 4))
claim_text('l11', 'screens[2].prose', 'month-ends', False, 'the 47 dates are 21 trading days apart, not month-ends')

# ---- l12 -----------------------------------------------------------------------------------------------------
wk = list(range(220, 1251, 5)); M, R, F5 = mom.iloc[wk], rev.iloc[wk], F[5].iloc[wk]
E('l12', 'screens[0].prose', len(wk))
sc = g['signal_corr'](M, R); im, irv = rank_ic(M, F5), rank_ic(R, F5)
E('l12', 'screens[0].explain.text', r(sc, 3)); E('l12', 'screens[0].explain.text', r(im.corr(irv), 3))
E('l12', 'screens[2].prose', r(rank_ic(comb([M, R], [0.5, 0.5]), F5).mean(), 4))
E('l12', 'screens[2].prose', r(im.mean(), 4)); E('l12', 'screens[2].prose', r(irv.mean(), 4))
E('l12', 'screens[7].canvas.state.values', r(rank_ic(comb([M, R], [0.4, 0.6]), F5).mean(), 4))
raw = M + R
E('l12', 'screens[4].explain.text', r(rank_ic(raw, F5).mean(), 4)); E('l12', 'screens[4].explain.text', r(g['signal_corr'](raw, M), 2))
E('l12', 'screens[4].explain.text', r(M.std(axis=1).mean(), 2)); E('l12', 'screens[4].explain.text', r(R.std(axis=1).mean(), 3))
bef = M.index < pd.Timestamp('2022-01-03')
for rows_, path in ((bef, 'screens[1].canvas.params.functions[0].expr'), (~bef, 'screens[8].canvas.params.functions[1].expr')):
    E('l12', path, r(rank_ic(M[rows_], F5[rows_]).mean(), 4)); E('l12', path, r(rank_ic(R[rows_], F5[rows_]).mean(), 4))
    E('l12', path, g['signal_corr'](M[rows_], R[rows_]))
dots = {w: r(rank_ic(comb([M[bef], R[bef]], [w, 1 - w]), F5[bef]).mean(), 4) for w in np.round(np.arange(-0.5, 1.51, 0.1), 1)}
E('l12', 'screens[1].explain.text', dots[0.4]); E('l12', 'screens[1].widget.options[2].why', r(dots[0.0], 3))
E('l12', 'screens[1].widget.options[3].why', r(dots[1.5], 3)); E('l12', 'screens[1].widget.options[1].why', r(dots[1.0], 3))
lv._rec(max(dots, key=dots.get) == 0.4, 'claim: research-period dots peak at w = 0.4', '')
grid = list(np.round(np.arange(0, 1.01, 0.1), 1))
bw = g['best_weight'](M, R, F5, grid, '2022-01-03')
for v in bw:
    E('l12', 'screens[8].explain.text', v)
Mm, Rm, Fm = mom.iloc[t47], rev.iloc[t47], F[21].iloc[t47]
E('l12', 'screens[7].prose', r(rank_ic(Rm, Fm).mean(), 4))
E('l12', 'screens[7].prose', max(r(rank_ic(comb([Mm, Rm], [w, 1 - w]), Fm).mean(), 4) for w in np.round(np.arange(-0.5, 1.51, 0.1), 1)))
bm = Mm.index < pd.Timestamp('2022-01-03')
E('l12', 'screens[9].prose', r(rank_ic(Rm[bm], Fm[bm]).mean(), 3)); E('l12', 'screens[9].prose', r(rank_ic(Rm[~bm], Fm[~bm]).mean(), 3))
E('l12', 'screens[9].canvas.state.caption', int(bm.sum())); E('l12', 'screens[9].canvas.state.caption', int((~bm).sum()))
bwm = g['best_weight'](Mm, Rm, Fm, grid, '2022-01-03')
E('l12', 'screens[9].prose', bwm[1]); E('l12', 'screens[9].explain.text', bwm[2])
E('l12', 'screens[9].explain.text', r(rank_ic(Mm[~bm], Fm[~bm]).mean(), 4))
num, var = 0.5 * 0.02 + 0.5 * 0.0242, 0.5 - 2 * 0.25 * 0.019
E('l12', 'screens[6].widget.answer', r(num / math.sqrt(var), 4)); E('l12', 'screens[6].widget.accept', r(math.sqrt(var), 4))
E('l12', 'screens[6].widget.wrong', r(num, 4)); E('l12', 'screens[6].widget.wrong', r(0.02 + 0.0242, 4))
for rho, ic2, row in ((0.8, 0.03, 1), (0.05, 0.02, 2)):
    E('l12', f'screens[10].canvas.params.rows[{row}]', r((0.8 * 0.05 + 0.2 * ic2) / math.sqrt(0.68 + 0.32 * rho), 3))
E('l12', 'quiz[0].widget.answer', r(0.02 / math.sqrt(0.5), 4)); E('l12', 'quiz[1].widget.options[1].text', r(0.03 * math.sqrt(2), 3))
claim_text('l12', 'quiz[3].explain.text', 'helps only if reversal has a negative IC', False,
           'a negative weight helps when IC_rev < rho * IC_mom (optimal weights are proportional to inv(Sigma) IC), not only when IC_rev < 0')

# ---- review-3 ------------------------------------------------------------------------------------------------
E('review', 'items[0].widget.answer', r(1 - 6 * 12 / 210, 3))
lv._rec(sum((a - b) ** 2 for a, b in zip(range(1, 7), [3, 1, 2, 6, 4, 5])) == 12, 'claim: review-3 items[0] sum d^2 = 12', '')
E('review', 'items[2].widget.answer', r(math.log(0.5) / math.log(0.97), 1))
E('review', 'items[2].widget.wrong', r(0.5 / 0.03, 1)); E('review', 'items[2].widget.wrong', r(1 / 0.03, 1))
E('review', 'items[3].widget.answer', r(0.025 / math.sqrt(0.7), 4)); E('review', 'items[3].widget.wrong', r(0.025 / math.sqrt(0.625), 4))
E('review', 'items[4].widget.answer', r(6.1 / math.sqrt(5), 2)); E('review', 'items[4].widget.wrong', r(6.1 / 5, 2))
E('review', 'items[6].widget.options[2].why', r(0.022 / math.sqrt(5), 4)); E('review', 'items[6].widget.options[2].why', r(0.045 / math.sqrt(21), 4))
E('review', 'items[8].widget.answer', r(0.02 * math.sqrt(400 * 52), 2))
E('review', 'items[8].widget.wrong', r(0.02 * math.sqrt(400), 2)); E('review', 'items[8].widget.wrong', r(0.02 * math.sqrt(52), 2))

# ---- homework-3 ----------------------------------------------------------------------------------------------
E('homework', 'items[0].widget.answer', r(0.025 / 0.07 * 6, 2))
E('homework', 'items[0].widget.wrong', r(0.025 / 0.07 * math.sqrt(12), 2)); E('homework', 'items[0].widget.wrong', r(0.025 / 0.07 * 36, 2))
E('homework', 'items[1].widget.answer', r(7 / math.sqrt(10), 2)); E('homework', 'items[1].widget.wrong', r(7 / 10, 2))
E('homework', 'items[1].explain.text', round(1000 / 10)); E('homework', 'items[1].explain.text', r(math.sqrt(10), 2))
E('homework', 'items[2].widget.answer', r(0.025 / math.sqrt(0.75), 4)); E('homework', 'items[2].widget.wrong', r(0.025 / math.sqrt(0.5), 4))
E('homework', 'items[3].widget.answer', r(0.5 ** (1 / 3), 2)); E('homework', 'items[3].widget.wrong', r(1 - 1 / 6, 2))
E('homework', 'items[5].explain.text', r(g['newey_west_t'](dic, 20), 2))
hs = pd.Series([0.05, -0.02, 0.03, 0.01, 0.04])
E('homework', 'items[5].explain.text', r(g['newey_west_t'](hs, 0), 2)); E('homework', 'items[5].explain.text', r(ic_summary(hs, 12)['t'], 2))
E('homework', 'items[7].widget.model', r(0.01 * math.sqrt(2400), 2))

lv.check_wrongs()
lv.report()
