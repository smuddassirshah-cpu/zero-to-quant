"""Second-reader number checks for alpha level 4 (l13 to l16, review-4, homework-4).

Panel numbers are recomputed in CPython by running the course's own functions (l16's run_research prelude and
solution, l15's bootstrap and deflation solution, read from the content JSON) on make_panel() with seed 2310, plus
side studies written here: the quintile book, spread-only reversal books, the same-day bug, 12-0 momentum, betas.
Hand numbers are recomputed from their closed forms. Each value is looked up where it is stated
(app/tools/numbers_lib.py). claim_text(...) fails while a wrong phrase is still in the content.
A failing check means the content is wrong (see docs/reviews/review-alpha-3-4.md) and stays failing until fixed.
Run: python3 docs/reports/alpha-L4-numbers.py
"""
import json, math, os, sys, warnings
from statistics import NormalDist
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('alpha', 4)
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'alpha')
J = lambda f: json.load(open(os.path.join(C, f + '.json'), encoding='utf8'))
E = lv.expect
inv = NormalDist().inv_cdf


def r(v, k):
    return round(float(v), k)


def claim_text(ref, path, phrase, ok, label):
    present = phrase in lv.text(ref, path)
    return lv._rec(bool(ok) or not present, f'claim: {ref} {path}: {label}', '' if present else '(phrase gone)')


g = {}
w16 = J('l16-research-note')['screens'][9]['widget']
exec(w16['prelude'] + '\n' + w16['solution'], g)
exec(J('l15-sharpe-after-costs')['screens'][10]['widget']['solution'], g)
P, rr = g['P'], g['run_research']
ret = P['ret']; idx = ret.index; cut = len(idx) - 252
R = rr(P, {'signal': 'momentum', 'rebalance': 'M'})
um = g['universe_mask'](P)
sig = g['momentum_12_1'](ret).where(um); W = g['long_short_weights'](sig)
dates = g['rebalance_dates'](idx, 'M')
sigma = ret.rolling(60, min_periods=20).std().ffill()
gross = g['portfolio_returns'](W, ret, 'M'); res = gross.index < idx[cut]; yrs = res.sum() / 252
cost = g['trade_costs'](W.loc[dates], P['half_spread_bp'], P['adv_gbp'], sigma.loc[dates], 1e8)
net = (gross - g['charge_next_day'](cost, idx).reindex(gross.index))[res]
gret, gvol = gross[res].mean() * 252, gross[res].std() * math.sqrt(252)
spread_bp = (W.loc[dates].pipe(lambda w: (w - w.shift(1).fillna(0)).abs()) * P['half_spread_bp'] / 1e4).sum(axis=1).loc[:idx[cut - 1]].sum() / (res.sum() / 252) * 1e4

# ---- l13 -----------------------------------------------------------------------------------------------------
E('l13', 'screens[0].widget.answer', 1000 - 1000); E('l13', 'screens[0].widget.wrong', 2000); E('l13', 'screens[0].widget.wrong', 1000)
others = [-0.215, -0.105, -0.045, 0.025, 0.085, 0.155, 0.315]
E('l13', 'screens[1].widget.answer', r((8 - 4.5) / 16, 4))
v = np.array(others + [1.8]); d = v - v.mean()
E('l13', 'screens[1].widget.wrong', r(d[-1] / np.abs(d).sum(), 4))
for k, a in enumerate([-0.3333, -0.1667, 0, 0.1667, 0.3333]):
    lv._rec(abs((k + 1 - 3) / 6 - a) < 5e-5, f'l13 screens[2] row {k} weight {a}', '')


def qbook(s):
    rk = s.rank(axis=1, pct=True); n = s.notna().sum(axis=1)
    top, bot = rk > 0.8, rk <= 0.2
    w = top.div(top.sum(axis=1), axis=0) * 0.5 - bot.div(bot.sum(axis=1), axis=0) * 0.5
    return w.where(n >= 10, 0).fillna(0)


Wq = qbook(sig); gq = g['portfolio_returns'](Wq, ret, 'M'); rq = gq.index < idx[cut]
cq = g['trade_costs'](Wq.loc[dates], P['half_spread_bp'], P['adv_gbp'], sigma.loc[dates], 1e8)
nq = gq - g['charge_next_day'](cq, idx).reindex(gq.index)
names = (Wq.loc[dates] != 0).sum(axis=1); names = names[names > 0]
rows3 = 'screens[3].canvas.params.rows'
for val in (r(names.mean(), 0), r(100 * gq[rq].mean() * 252, 2), r(100 * gq[rq].std() * math.sqrt(252), 2), r(g['sharpe'](gq[rq], 252), 2),
            r(g['turnover'](Wq.loc[dates]).loc[:idx[cut - 1]].sum() / yrs, 2), r(g['sharpe'](nq[rq], 252), 2),
            r(100 * gret, 2), r(100 * gvol, 2), r(R['sharpe_gross'], 2), r(R['turnover'], 2), r(R['sharpe_net'], 2)):
    E('l13', rows3, val)
nm_r = (W.loc[dates] != 0).sum(axis=1).loc[:idx[cut - 1]]; E('l13', rows3, r(nm_r[nm_r > 0].mean(), 0))   # research rebalances
wd = W.loc['2020-03-31']; beta = P['beta']
bl = (wd[wd > 0] * beta[wd > 0]).sum() / wd[wd > 0].sum(); bs = (wd[wd < 0] * beta[wd < 0]).sum() / wd[wd < 0].sum()
E('l13', 'screens[4].prose', r(bl, 3)); E('l13', 'screens[4].prose', r(bs, 3))
E('l13', 'screens[4].widget.answer', r(0.5 * 0.957 - 0.5 * 1.073, 3)); E('l13', 'screens[4].widget.wrong', r(0.957 - 1.073, 3))
lv._rec(abs((wd * beta).sum() - (0.5 * bl - 0.5 * bs)) < 1e-9, 'claim: book beta on 2020-03-31 is -0.058', f'{(wd * beta).sum():.4f}')
mkt = ret.where(P['listed']).mean(axis=1).loc[gross.index][res]
E('l13', 'screens[4].explain.text', r(np.cov(gross[res], mkt)[0, 1] / mkt.var(), 2))
s010 = ret['S010'].dropna()
E('l13', 'screens[5].prose', r(W.loc['2021-04-30', 'S010'], 5)); E('l13', 'screens[5].prose', r(100 * s010.iloc[-1], 2))
lv._rec(s010.index[-1] == pd.Timestamp('2021-05-19'), 'claim: S010 delists on 19 May 2021', str(s010.index[-1].date()))
E('l13', 'screens[5].widget.answer', r(-0.01135 * -0.6182 * 1e4, 1))
s181 = ret['S181'].dropna(); w181 = W.loc[dates[dates < s181.index[-1]][-1], 'S181']
E('l13', 'screens[5].explain.text', r(w181, 5)); E('l13', 'screens[5].explain.text', r(-100 * s181.iloc[-1], 1))
E('l13', 'screens[5].explain.text', r(-w181 * s181.iloc[-1] * 1e4, 0))
Wr = g['long_short_weights'](g['reversal_5d'](ret).where(um)); gr = g['portfolio_returns'](Wr, ret, 'D'); rs = gr.index < idx[cut]
bug = (Wr * ret.fillna(0)).sum(axis=1).loc[gr.index]
E('l13', 'screens[6].canvas.params.lines', r(g['sharpe'](gr[rs], 252), 3)); E('l13', 'screens[6].canvas.params.lines', r(g['sharpe'](bug[rs], 252), 2))
mbug = (W.loc[dates].reindex(idx).ffill() * ret.fillna(0)).sum(axis=1).loc[gross.index]
sb = g['sharpe'](mbug[res], 252)
claim_text('l13', 'screens[6].feedback.byKey.d', 'a momentum signal would jump up instead', sb - R['sharpe_gross'] > 0.5,
           f'12-1 momentum with the same bug moves {R["sharpe_gross"]:.2f} to {sb:.2f} (review-4 says so)')
claim_text('l13', 'screens[6].explain.text', 'beyond ±2', g['sharpe'](gr[rs], 252) <= 2,
           'the honest line on this screen is 3.417, beyond 2')
E('l13', 'screens[10].widget.answer', 0.005 * 250 / 500 * 1e4); E('l13', 'screens[10].widget.wrong', 0.005 * 500 / 500 * 1e4)
E('l13', 'quiz[0].widget.answer', 1.5 / 4); E('l13', 'quiz[0].widget.wrong', 4 / 10); E('l13', 'quiz[0].widget.wrong', 0.25)
E('l13', 'quiz[1].widget.answer', r(0.5 * 1.2 - 0.5 * 0.8, 2)); E('l13', 'quiz[1].widget.wrong', r(1.2 - 0.8, 2))
E('l13', 'quiz[3].explain.text', int(um.sum(axis=1).iloc[60:].min()))

# ---- l14 -----------------------------------------------------------------------------------------------------
rev_ = {}
for reb in 'DWM':
    dd = g['rebalance_dates'](idx, reb); grb = g['portfolio_returns'](Wr, ret, reb); rsb = grb.index < idx[cut]
    w_ = Wr.loc[dd]; dw_ = (w_ - w_.shift(1).fillna(0)).abs()
    nt = grb - g['charge_next_day']((dw_ * (P['half_spread_bp'] / 1e4)).sum(axis=1), idx).reindex(grb.index)
    y_ = rsb.sum() / 252; trd = dw_.sum(axis=1).loc[:idx[cut - 1]].sum() / y_
    rev_[reb] = dict(gross=g['sharpe'](grb[rsb], 252), spread=g['sharpe'](nt[rsb], 252), traded=trd, ret=grb[rsb].mean() * 252,
                     slope=trd / 1e4 / (grb[rsb].std() * math.sqrt(252)), full=rr(P, {'signal': 'reversal', 'rebalance': reb}))
for reb, name in (('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')):
    E('l14', f'screens[0].canvas.state.values.{name}', r(rev_[reb]['gross'], 3))
    E('l14', 'screens[0].explain.text', r(rev_[reb]['spread'], 2))
    E('l14', 'screens[1].canvas.params.functions', r(rev_[reb]['slope'], 4 if reb != 'D' else 3))
E('l14', 'screens[0].prose', r(P['half_spread_bp'].median(), 1))
E('l14', 'screens[0].explain.text', round(rev_['D']['traded'], -1))
E('l14', 'screens[1].widget.answer', r((2.351 - 1.171) / (0.2534 - 0.0564), 1)); E('l14', 'screens[1].widget.wrong', r((3.417 - 2.351) / (0.567 - 0.2534), 1))
E('l14', 'screens[2].widget.answer', 0.5 * (0.05 + 0.05 + 0.10 + 0.10)); E('l14', 'screens[2].explain.text', 12 * 0.15)
E('l14', 'screens[3].canvas.params.rows', r(rev_['D']['full']['turnover'], 1)); E('l14', 'screens[3].widget.options', r(rev_['M']['full']['turnover'], 1))
E('l14', 'screens[3].widget.options', r(rev_['W']['full']['turnover'], 1)); E('l14', 'screens[3].widget.options', round(5 * rev_['D']['full']['turnover']))


def sac(s, lag):
    prev = s.shift(lag); both = s.notna() & prev.notna()
    c = s.where(both).rank(axis=1).corrwith(prev.where(both).rank(axis=1), axis=1)
    return float(c[both.sum(axis=1) >= 3].mean())


sr5 = g['reversal_5d'](ret).where(um)
for v in (sac(sig, 21), sac(sr5, 1), sac(sr5, 5)):
    E('l14', 'screens[3].canvas.params.rows', r(v, 3))
cost1 = 400000 * (0.02 * math.sqrt(400000 / 20e6) + 7e-4)
E('l14', 'screens[4].widget.answer', round(cost1)); E('l14', 'screens[4].widget.wrong', 280); E('l14', 'screens[4].widget.wrong', 400000 * (0.02 * 0.02 + 7e-4))
E('l14', 'screens[5].prose', r(100 * rev_['D']['ret'], 2)); E('l14', 'screens[5].prose', r(rev_['D']['traded'], 1))
E('l14', 'screens[5].widget.answer', r(rev_['D']['ret'] / rev_['D']['traded'] * 1e4, 1))
E('l14', 'screens[5].widget.wrong', r(rev_['D']['ret'] / (rev_['D']['traded'] / 2) * 1e4, 1))
E('l14', 'screens[5].explain.text', r(rev_['D']['full']['sharpe_net'], 1)); E('l14', 'screens[5].explain.text', round(R['break_even_bp']))
wr = W.loc[dates].loc[:idx[cut - 1]]; hs = P['half_spread_bp'] / 1e4
dw = (wr - wr.shift(1).fillna(0)).abs(); traded_bp = (dw * hs).sum(axis=1).sum() / yrs * 1e4
held12 = 12 * (wr.abs() * hs).sum(axis=1)[wr.abs().sum(axis=1) > 0].mean() * 1e4
E('l14', 'screens[6].widget.options', r(traded_bp, 1)); E('l14', 'screens[6].widget.options', r(traded_bp / 2, 1))
lv._rec(abs(held12 - 92.7) < 0.2, 'l14 screens[6] spread on the book held, 12 times a year, 92.7 bp', f'{held12:.2f} (12 x mean over the 36 live rebalances; per research year it is 91.1)')
E('l14', 'screens[6].explain.text', r(traded_bp / (2 * R['turnover']), 1)); E('l14', 'screens[6].explain.text', r(P['half_spread_bp'].max(), 0))
E('l14', 'screens[7].explain.text', r(0.5 / 3, 2))
caps = {b: rr(P, {'signal': 'momentum', 'rebalance': 'M', 'book_gbp': b})['sharpe_net'] for b in (1e7, 5e7, 1e8, 2e8, 2.5e8, 3e8, 5e8, 1e9)}
for b, key in zip(caps, ('b10', 'b50', 'b100', 'b200', 'b250', 'b300', 'b500', 'b1000')):
    E('l14', f'screens[11].canvas.state.values.{key}', r(caps[b], 3))
E('l14', 'screens[11].canvas.params.hlines', r(R['sharpe_gross'] / 2, 3))
first = min(b for b in caps if caps[b] < R['sharpe_gross'] / 2)
lv._rec(first == 3e8, 'claim: first book below half the gross is £300m', str(first))
E('l14', 'screens[11].explain.text', r(R['cost_bp'], 0))
E('l14', 'quiz[1].widget.answer', 0.04 / 4 * 1e4); E('l14', 'quiz[2].widget.answer', r(1.5 - 0.05 * 8, 2)); E('l14', 'quiz[2].widget.wrong', r(1.5 * 0.92, 2))
claim_text('l14', 'quiz[0].explain.text', 'apart from going from cash', 0.5 > 1, 'going from cash trades 0.5, less than 1, so it is no exception')

# ---- l15 -----------------------------------------------------------------------------------------------------
def lo(sr, n, ppy):
    per = sr / math.sqrt(ppy); se = math.sqrt((1 + per ** 2 / 2) / n) * math.sqrt(ppy); return sr - 1.96 * se, sr + 1.96 * se, se


for sr in (0.9, 0.6):
    for v in lo(sr, 60, 12)[:2]:
        E('l15', 'screens[0].explain.text', r(v, 2))
E('l15', 'screens[1].widget.accept', r(lo(0.9, 48, 12)[0], 2)); E('l15', 'screens[1].widget.accept', r(lo(0.9, 60, 12)[0], 2))
a, b_, se = lo(R['sharpe_net'], R['n_obs'], 252)
E('l15', 'screens[2].prose', R['sharpe_net']); E('l15', 'screens[2].prose', R['n_obs'])
E('l15', 'screens[2].widget.answer', r(a, 2)); E('l15', 'screens[2].widget.accept', r(se, 4)); E('l15', 'screens[2].explain.text', r(b_, 2))
E('l15', 'screens[2].widget.wrong', r(R['sharpe_net'] - 1.96 * se / math.sqrt(252), 2)); E('l15', 'screens[2].widget.wrong', r(R['sharpe_net'] - se, 2))
mo = (1 + net).groupby(net.index.to_period('M')).prod() - 1; mci = g['sharpe_ci'](mo, 12)
E('l15', 'screens[3].canvas.params.rows', len(mo))
for v in mci:
    E('l15', 'screens[3].canvas.params.rows', r(v, 2))
for v in g['block_bootstrap_ci'](net, 252, 21) + g['block_bootstrap_ci'](net, 252, 1):
    E('l15', 'screens[4].canvas.params.rows', v)
E('l15', 'screens[4].canvas.params.rows', r(net.autocorr(1), 3))
E('l15', 'screens[5].widget.answer', 6 * 2 * 3 + 1)
sd = math.sqrt(252 / (R['n_obs'] - 1)); gam = 0.5772156649015329
emax = sd * ((1 - gam) * inv(1 - 1 / 37) + gam * inv(1 - 1 / (37 * math.e)))
E('l15', 'screens[6].prose', r(sd, 3)); E('l15', 'screens[6].canvas.params.rows', r(inv(1 - 1 / 37), 4))
E('l15', 'screens[6].canvas.params.rows', r(inv(1 - 1 / (37 * math.e)), 4)); E('l15', 'screens[6].widget.answer', r(emax, 2))
per = R['sharpe_net'] / math.sqrt(252)
dsr = NormalDist().cdf((per - emax / math.sqrt(252)) * math.sqrt(R['n_obs'] - 1) / math.sqrt(1 + per ** 2 / 2))
E('l15', 'screens[6].explain.text', r(dsr, 2))
s120 = g['momentum_12_1'](ret, skip=0).where(um); W0 = g['long_short_weights'](s120); g0 = g['portfolio_returns'](W0, ret, 'M')
c0 = g['trade_costs'](W0.loc[dates], P['half_spread_bp'], P['adv_gbp'], sigma.loc[dates], 1e8)
n0 = (g0 - g['charge_next_day'](c0, idx).reindex(g0.index))[g0.index < idx[cut]]
for v in g['sharpe_ci'](n0, 252):
    E('l15', 'screens[7].prose', r(v, 2))
E('l15', 'screens[8].explain.text', r(math.sqrt(3 / 4), 2))
claim_text('l15', 'screens[8].explain.text', '13% more precision', abs(1 / math.sqrt(3 / 4) - 1.13) < 0.005,
           f'the interval narrows by 13%; precision (1/width) rises by {100 * (1 / math.sqrt(0.75) - 1):.1f}%')
E('l15', 'screens[11].prose', r(R['held_out']['sharpe_net'], 2))
for v in R['held_out']['ci']:
    E('l15', 'screens[11].prose', r(v, 2))
E('l15', 'screens[11].prose', r(g['sharpe'](gross[~res], 252), 2))
E('l15', 'quiz[0].widget.wrong', r(1.96 / math.sqrt(252), 4)); E('l15', 'quiz[0].explain.text', r(1.96 * math.sqrt(252 / 63), 1))
sd4 = math.sqrt(252 / (4 * 252 - 1))
E('l15', 'quiz[1].explain.text', r(sd4 * ((1 - gam) * inv(1 - 1 / 30) + gam * inv(1 - 1 / (30 * math.e))), 1))
lo4 = lo(0.8, 4 * 252, 252)
claim_text('l15', 'quiz[1].prose', '−0.1 to 1.7', abs(lo4[0] + 0.1) < 0.05, f'Lo over four years of daily returns gives {lo4[0]:.2f} to {lo4[1]:.2f}')

# ---- l16 -----------------------------------------------------------------------------------------------------
E('l16', 'screens[3].canvas.params.lines', R['ic']['mean']); E('l16', 'screens[3].canvas.params.lines', R['ic']['sd'])
E('l16', 'screens[3].widget.rows[0][1].answer', r(R['ic']['t'], 2))
E('l16', 'screens[3].widget.rows[1][1].answer', r(0.0377 / 0.0971 * math.sqrt(12), 2))
E('l16', 'screens[3].explain.text', r(100 * R['ic']['hit'], 0))
for v in R['quintiles']:
    E('l16', 'screens[3].explain.text', r(100 * v, 2))
h3 = {}
exec(J('l11-quintiles')['screens'][3]['widget']['solution'], h3)
fwd21 = g['forward_returns'](ret, 21); md = dates[dates <= idx[cut - 1 - 21]]
q3 = h3['quantile_returns'](sig.loc[md], fwd21.loc[md]).mean()
claim_text('l16', 'screens[3].explain.text', 'not monotone', not bool((q3.diff().dropna() > 0).all()),
           f'with level 3\'s quantile_returns (ceil(q r / n), ties averaged) the quintiles are {[r(100 * x, 2) for x in q3]}: monotone')
E('l16', 'screens[4].widget.rows[0][1].answer', round(R['break_even_bp']))
E('l16', 'screens[4].widget.rows[1][1].answer', r(gret - R['cost_bp'] / 1e4, 4))
E('l16', 'screens[4].explain.text', r(R['cost_bp'] / (2 * R['turnover']), 0))
claim_text('l16', 'screens[4].explain.text', '5.24% − 1.65% = 3.58%', abs(5.24 - 1.65 - 3.58) < 0.005, '5.24 - 1.65 = 3.59; the 3.58 needs the unrounded gross 5.238%')
E('l16', 'screens[5].prose', r(100 * R['max_drawdown'], 1))
for reb_v in (rev_['D']['full']['sharpe_gross'], rev_['D']['full']['sharpe_net']):
    E('l16', 'screens[6].canvas.params.rows', r(reb_v, 2 if abs(reb_v) < 10 else 1))
combo = rr(P, {'signal': 'combo', 'rebalance': 'M'})
E('l16', 'screens[6].canvas.params.rows', r(combo['sharpe_gross'], 2))
E('l16', 'screens[6].widget.options[0].text', r(rev_['D']['full']['cost_bp'] / 100, 0)); E('l16', 'screens[6].widget.options[3].text', r(combo['turnover'], 1))
claim_text('l16', 'screens[6].widget.options[3].text', 'its reversal leg traded', False, '6.1 is the turnover of the whole combined book (run_research turnover 6.12), not of a leg')
claim_text('l16', 'screens[6].canvas.params.rows[1][2]', '−0.00', False, 'a rounded −0.0042 shows as −0.00; write 0.00')
E('l16', 'screens[9].canvas.params.lines', R['sharpe_net']); E('l16', 'screens[9].canvas.params.lines', R['held_out']['sharpe_net'])
E('l16', 'quiz[0].explain.text', r(lo(2.1, 252, 252)[0], 1)); E('l16', 'quiz[0].explain.text', r(lo(2.1, 252, 252)[1], 1))

# ---- review-4 ------------------------------------------------------------------------------------------------
E('review', 'items[0].widget.answer', r(2.5 / 9, 4)); E('review', 'items[0].widget.wrong', r(6 / 21, 4)); E('review', 'items[0].widget.wrong', r(0.5 / 3, 4))
E('review', 'items[1].prose', r(R['sharpe_gross'], 2)); E('review', 'items[1].prose', r(sb, 2))
E('review', 'items[2].widget.answer', r(0.5 * (0.15 + 0.15 + 0.20 + 0.20), 2))
E('review', 'items[3].widget.answer', round(2e6 * (0.015 * math.sqrt(0.04) + 3e-4)))
E('review', 'items[3].widget.wrong', round(2e6 * 3e-4)); E('review', 'items[3].widget.wrong', round(2e6 * (0.015 * 0.04 + 3e-4)))
# weekly reversal book (finding 26): gross return a year, turnover, break-even, from the course's own functions
RW = rr(P, {'signal': 'reversal', 'rebalance': 'W'})
sigw = g['reversal_5d'](ret).where(um); Ww = g['long_short_weights'](sigw)
grossw = g['portfolio_returns'](Ww, ret, 'W'); gw = grossw[grossw.index < idx[cut]].mean() * 252
E('review', 'items[4].prose', r(gw * 100, 2)); E('review', 'items[4].prose', r(RW['turnover'], 1))
be = gw / (2 * RW['turnover']) * 1e4
E('review', 'items[4].widget.answer', r(be, 1)); E('review', 'items[4].widget.accept', r(be, 1))
E('review', 'items[4].widget.wrong', r(gw / RW['turnover'] * 1e4, 1)); E('review', 'items[4].explain.text', r(2 * RW['turnover'], 1))
E('review', 'items[4].explain.text', r(be, 1)); E('review', 'items[4].explain.text', r(float(np.median(P['half_spread_bp'])), 1))
lv._rec(abs(be - RW['break_even_bp']) < 0.05, 'review-4 items[4]: break-even agrees with run_research', '')
# review-4 items[7] options[0]: weekly reversal gross and net Sharpe at GBP 100m
E('review', 'items[7].widget.options[0].text', r(RW['sharpe_gross'], 2)); E('review', 'items[7].widget.options[0].text', r(RW['sharpe_net'], 2))
E('review', 'items[7].widget.options[0].text', r(RW['break_even_bp'], 1)); E('review', 'items[7].widget.options[0].text', r(float(np.median(P['half_spread_bp'])), 1))
E('review', 'items[5].widget.answer', r(lo(1.0, 504, 252)[0], 2)); E('review', 'items[5].widget.accept', r(lo(1.0, 504, 252)[2], 3))
E('review', 'items[5].explain.text', r(lo(1.0, 504, 252)[1], 2)); E('review', 'items[5].widget.wrong', r(1 - 1.96 * lo(1.0, 504, 252)[2] / math.sqrt(252), 2))
lv._rec('about four years' in lv.text('review', 'items[5].explain.text') and math.ceil(1.96 ** 2) == 4, 'claim: a Sharpe of 1 clears zero after about four years', '')
E('review', 'items[6].widget.answer', 4 * 3 + 2); E('review', 'items[6].widget.wrong', 12); E('review', 'items[6].widget.wrong', 4 + 3 + 2)

# ---- homework-4 ----------------------------------------------------------------------------------------------
E('homework', 'items[3].widget.answer', r(0.058 * 100, 1)); E('homework', 'items[3].widget.wrong', r(0.058 * 50, 1))
E('homework', 'items[4].widget.answer', r(36.6 + 2 * 128.8, 1)); E('homework', 'items[4].widget.wrong', r(2 * 165.4, 1))
E('homework', 'items[4].prose', r(spread_bp, 1)); E('homework', 'items[4].prose', r(R['cost_bp'] - spread_bp, 1))
E('homework', 'items[4].widget.accept', r(2 * 128.8, 1))   # 2 x the stated 128.8 = 257.6
lv._rec(abs(36.6 + 4 * 128.8 - 551.7) < 0.6, 'homework-4 items[4] wrong linear within its tolerance of 36.6 + 4 x 128.8', '')
E('homework', 'items[5].widget.answer', r(0.5 * ((1 - gam) * 1.2816 + gam * 1.7892), 2))
E('homework', 'items[5].widget.wrong', r((1 - gam) * 1.2816 + gam * 1.7892, 2))
lv._rec(abs(inv(1 - 1 / (10 * math.e)) - 1.7892) < 5e-5 and abs(inv(0.9) - 1.2816) < 5e-5, 'claim: homework-4 items[5] quantiles', '')
claim_text('homework', 'items[5].prose', 'about 3 years', abs(math.sqrt(252 / (3 * 252 - 1)) - 0.5) < 0.01,
           f'no-skill sd over 3 years of daily data is {math.sqrt(252 / 755):.3f}, not 0.5 (0.5 is 4 years)')
for v in (R['ic']['mean'], r(R['ic']['t'], 2), r(R['turnover'], 2), r(R['sharpe_gross'], 2), r(R['sharpe_net'], 2), r(R['held_out']['sharpe_net'], 2)):
    E('homework', 'items[7].widget.model', v)
claim_text('homework', 'items[7].widget.model', 'its reversal leg turned the book over', False, '6.1 is the whole combined book\'s turnover')

lv.check_wrongs()
lv.report()
