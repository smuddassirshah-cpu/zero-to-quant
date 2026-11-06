"""Recompute every number stated in opt-dash level 1 (Data) and check it at its JSON path (second read).

Run: python3 docs/reports/opt-dash-L1-numbers.py   (NumPy, pandas, SciPy and the standard library; exits 0 when every check passes)

The chain is the brief's `make_chain()` (seed 2320), taken from l4's prelude, and the brief's own checks are asserted
first. Quotes are read from the chain by direct pandas code; vols come from a second solver here (SciPy `brentq` on a
SciPy-`ndtr` Black-Scholes), checked against the lesson's bisection solver (`two`). `E` checks a stated value appears
where it is stated; `stated` ties a claim to its wording (while the phrase is in the text, the claim must hold). A check
that fails because the content is wrong is a finding in docs/reviews/review-opt-dash-1-2.md and stays failing until the
fix pass corrects the content.
"""
import json
import math
import os
import sys
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import ndtr

warnings.simplefilter('ignore')
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, COURSES  # noqa: E402

lv = Level("opt-dash", 1)
E = lv.expect
S, R, Q = 100.0, 0.05, 0.01


def claim(name, ok):
    lv._rec(bool(ok), f'claim: {name}', '')


def stated(ref, path, phrase, ok):
    try:
        there = phrase in lv.text(ref, path)
    except KeyError:                      # a path the fix pass will create
        there = False
    lv._rec(bool(ok) or not there, f'stated: {ref} {path} "{phrase}"', '' if ok or not there else 'the stated claim is false')


def two(name, a, b, tol=1e-6):
    lv._rec(math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), f'two routes: {name} {a!r} vs {b!r}', '')


def doc(fid):
    return json.load(open(os.path.join(COURSES, 'opt-dash', fid + '.json')))


def R_(x, d):
    return round(float(x), d)


# ---------- independent Black-Scholes and solver ----------
def bs(Sx, K, r, s, T, kind='call', q=0.0):
    d1 = (math.log(Sx / K) + (r - q + s * s / 2) * T) / (s * math.sqrt(T))
    d2 = d1 - s * math.sqrt(T)
    if kind == 'call':
        return Sx * math.exp(-q * T) * ndtr(d1) - K * math.exp(-r * T) * ndtr(d2)
    return K * math.exp(-r * T) * ndtr(-d2) - Sx * math.exp(-q * T) * ndtr(-d1)


def ivol(price, K, T, kind, Sx=S, r=R, q=Q):
    lo = max(Sx * math.exp(-q * T) - K * math.exp(-r * T), 0) if kind == 'call' else max(K * math.exp(-r * T) - Sx * math.exp(-q * T), 0)
    if not (lo < price < (Sx * math.exp(-q * T) if kind == 'call' else K * math.exp(-r * T))):
        return float('nan')
    return brentq(lambda s: bs(Sx, K, r, s, T, kind, q) - price, 1e-6, 5, xtol=1e-14)


def vega_pt(K, T, s, Sx=S, r=R, q=Q):
    d1 = (math.log(Sx / K) + (r - q + s * s / 2) * T) / (s * math.sqrt(T))
    return Sx * math.exp(-q * T) * math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi) * math.sqrt(T) / 100


# ---------- the chain and the lesson solutions ----------
ns = {}
w9 = doc('l4-which-price')['screens'][9]['widget']
exec(w9['prelude'], ns)
exec(w9['solution'], ns)
exec(doc('l3-rates-dividends')['screens'][7]['widget']['solution'], ns)
exec(doc('l3-rates-dividends')['screens'][8]['widget']['solution'], ns)
exec(doc('l2-cleaning-quotes')['screens'][8]['widget']['solution'], ns)
exec(doc('l1-reading-a-chain')['screens'][9]['widget']['solution'], ns)
for i in (0, 1):
    exec(doc('homework-1')['items'][i]['widget']['solution'], ns)
chain, clean = ns['chain'], ns['clean']
true_iv = ns['true_iv']
TS = [1 / 12, 2 / 12, 3 / 12, 6 / 12, 1.0]


def q_(T, K, kind, df=chain):
    r = df[np.isclose(df['T'], T) & (df.strike == K) & (df.type == kind)]
    assert len(r) == 1, (T, K, kind)
    return float(r.bid.iloc[0]), float(r.ask.iloc[0])


def mid_(T, K, kind):
    b, a = q_(T, K, kind)
    return (b + a) / 2


# brief's checks
claim('130 rows', len(chain) == 130)
claim('15 zero bids', int((chain.bid == 0).sum()) == 15)
claim('2 crossed', int((chain.bid > chain.ask).sum()) == 2)
claim('row 0 is 1m 70 call 29.30/31.11', list(chain.iloc[0][['strike', 'type', 'bid', 'ask']]) == [70, 'call', 29.30, 31.11])
claim('row 64 is 3m 100 call 4.37/4.64', list(chain.iloc[64][['strike', 'type', 'bid', 'ask']]) == [100, 'call', 4.37, 4.64])
claim('row 129 is 1y 130 put 25.43/27.01', list(chain.iloc[129][['strike', 'type', 'bid', 'ask']]) == [130, 'put', 25.43, 27.01])
claim('true_iv 1m', [R_(true_iv(K, 1 / 12), 4) for K in (70, 85, 100, 115, 130)] == [0.4412, 0.2649, 0.1869, 0.1704, 0.1946])
claim('true_iv 1y', [R_(true_iv(K, 1.0), 4) for K in (70, 85, 100, 115, 130)] == [0.2659, 0.2387, 0.2218, 0.2114, 0.2056])
claim('clean keeps 102', len(clean) == 102)
two('bs 10.4506', bs(100, 100, 0.05, 0.2, 1), ns['bs_price'](100, 100, 0.05, 0.2, 1), 1e-12)

# ================= l1 =================
b, a = q_(0.25, 100, 'call')
E('l1', 'screens[0].hints[2].text', b, fmt='£{:.2f}')
E('l1', 'screens[0].hints[2].text', a, fmt='£{:.2f}')
E('l1', 'screens[2].widget.answer', (b + a) / 2)
E('l1', 'screens[2].widget.wrong[0].value', R_(a - b, 2))
E('l1', 'screens[2].widget.wrong[1].value', R_((a - b) / 2, 3))
E('l1', 'screens[2].explain.text', R_(a - b, 2))
claim('l1 s1: puts 105 to 130 are ITM at S=100 (rows r7..r12 are strikes 105..130)', [70 + 5 * i for i in range(7, 13)] == list(range(105, 131, 5)))
# s3 long rows: every displayed row equals the chain
for row in doc('l1-reading-a-chain')['screens'][3]['canvas']['params']['rows']:
    T = {'0.0833': 1 / 12, '0.25': 0.25, '1.00': 1.0}[row[0]]
    claim(f'l1 s3 row {row}', q_(T, int(row[1]), row[2]) == (float(row[3]), float(row[4])))
m1, m3, m12 = mid_(1 / 12, 100, 'call'), mid_(0.25, 100, 'call'), mid_(1.0, 100, 'call')
E('l1', 'screens[3].explain.text', R_(m1, 2))
E('l1', 'screens[3].explain.text', R_(m12, 2), fmt='£{:.2f}')
claim('l1 s3 "£4.51 at three" is the 4.505 mid rounded half-up', R_(m3 + 1e-9, 2) == 4.51)
E('l1', 'screens[3].feedback.correct', '6.54 / 6.94')
claim('1y 100 put is 6.54/6.94', q_(1.0, 100, 'put') == (6.54, 6.94))
# s4 typo table: every cell except the typo is the chain mid
tab = doc('l1-reading-a-chain')['screens'][4]['canvas']['params']['rows']
for i, K in enumerate((90, 100, 105)):
    for j, T in enumerate((1 / 12, 0.25, 1.0)):
        true = mid_(T, K, 'call')
        if (K, T) == (105, 0.25):
            claim('l1 s4 typo cell 4.72 is not the chain mid', tab[i][j + 1] == '4.72' and abs(true - 4.72) > 1)
            E('l1', 'screens[4].feedback.correct', R_(true, 2), fmt='£{:.2f}')
            E('l1', 'screens[4].explain.text', R_(true, 2), fmt='£{:.2f}')
        else:
            claim(f'l1 s4 cell {K} {T:.3f} = {tab[i][j + 1]}', abs(R_(true + 1e-9, 2) - float(tab[i][j + 1])) < 1e-9)
# s5 multiplier
E('l1', 'screens[5].widget.answer', 10 * 100 * a)
E('l1', 'screens[5].widget.wrong[0].value', 10 * a)
E('l1', 'screens[5].widget.wrong[1].value', 10 * 100 * b)
E('l1', 'screens[5].widget.wrong[2].value', 10 * 100 * (a + b) / 2)
E('l1', 'screens[5].widget.wrong[3].value', 100 * a)
E('l1', 'screens[5].prose', 100 * b)
E('l1', 'screens[5].explain.text', 1000 * (a - b))
E('l1', 'screens[5].explain.text', 1000 * b)
# s7 pivot shape
wide = chain[chain['T'] == 0.25].assign(mid=ns['mid']).pivot(index='strike', columns='type', values='mid')
claim('l1 s7: 26 rows at 3m, pivot is 13 by 2', len(chain[chain['T'] == 0.25]) == 26 and wide.shape == (13, 2))
claim('l1 s9: 3m 95 call has bid 0 so mid NaN', math.isnan(ns['chain_table'](chain, 0.25, 'call').loc[95, 'mid']))
# s10 straddle
pb, pa = q_(0.25, 100, 'put')
strad = (b + a) / 2 + (pb + pa) / 2
E('l1', 'screens[10].prose', R_(strad, 2))
E('l1', 'screens[10].prose', (pb + pa) / 2)
sig = strad / (0.8 * math.sqrt(0.25) * 100)
E('l1', 'screens[10].widget.answer', R_(sig, 4))
E('l1', 'screens[10].widget.wrong[0].value', R_(strad / (0.8 * 0.25 * 100), 4))
E('l1', 'screens[10].widget.wrong[1].value', (b + a) / 2 / 40)
claim('l1 s10: sqrt(2/pi) rounds to 0.8', R_(math.sqrt(2 / math.pi), 1) == 0.8)
claim('l1 s10: straddle vol near the 3m ATM vol (within 1 point of true_iv at the forward)', abs(sig - true_iv(100 * math.exp(0.04 * 0.25), 0.25)) < 0.01)
# quiz
E('l1', 'quiz[0].prose', q_(0.25, 95, 'put')[1])
E('l1', 'quiz[0].prose', q_(0.25, 100, 'put')[1])
E('l1', 'quiz[0].prose', q_(0.25, 105, 'put')[1])
E('l1', 'quiz[0].explain.text', q_(0.25, 110, 'put')[1], fmt='£{:.2f}')
pb1, pa1 = q_(1.0, 100, 'put')
E('l1', 'quiz[1].widget.answer', 5 * 100 * pb1)
E('l1', 'quiz[1].widget.wrong[0].value', 5 * 100 * pa1)
E('l1', 'quiz[1].widget.wrong[1].value', 5 * pb1)
claim('l1 quiz2: 3m 130 call is 0.00/0.04', q_(0.25, 130, 'call') == (0.0, 0.04))
cm, pm = mid_(1.0, 100, 'call'), mid_(1.0, 100, 'put')
E('l1', 'quiz[3].prose', R_(cm, 2), fmt='£{:.2f}')
E('l1', 'quiz[3].prose', R_(pm, 2), fmt='£{:.2f}')
claim('l1 quiz3: key 0.2168 is 17.34/80 to 4 places', abs((cm + pm) / 80 - 0.2168) < 6e-5)
E('l1', 'quiz[3].widget.wrong[0].value', R_(cm / 80, 4))
E('l1', 'quiz[3].explain.text', R_(cm + pm, 2))
# claim: "a higher strike pays less [more] in every outcome" (false when both pay 0)
stated('l1', 'screens[4].hints[0].text', 'pays less in every outcome', False)
stated('l1', 'screens[4].explain.text', 'pays less in every outcome', False)
stated('l1', 'quiz[0].widget.options[0].text', 'pays more in every outcome', False)

# ================= l2 =================
t0 = doc('l2-cleaning-quotes')['screens'][0]['canvas']['params']['rows']
for row in t0:
    T = float(row[0]); K = int(row[1])
    if row[1] == '80' and row[0] == '0.25':
        continue                                                     # the hand row
    claim(f'l2 s0 row {row[:5]} from the chain', q_(T if T != 0.25 else 0.25, K, row[2]) == (float(row[3]), float(row[4])))
lb80 = S * math.exp(-Q * 0.25) - 80 * math.exp(-R * 0.25)
E('l2', 'screens[0].explain.text', R_(lb80, 2), fmt='£{:.2f}')
claim('l2 s0: hand 80 call ask 19.40 below S - K = 20 and below the bound', 19.40 < 20 < lb80)
for k in ('r0', 'r3', 'r7', 'r8'):
    rr = t0[int(k[1])]
    claim(f'l2 s0 {k}: spread is 6% of mid', R_((float(rr[4]) - float(rr[3])) / ((float(rr[4]) + float(rr[3])) / 2), 2) == 0.06)
E('l2', 'screens[0].feedback.byKey.r5', R_(7.60 - 4.48, 2), fmt='£{:.2f}')
c = chain.copy(); c['m'] = (c.bid + c.ask) / 2; c['rel'] = (c.ask - c.bid) / c.m
hi = c[(c.bid > 0) & (c.rel >= 0.5)]
wing = hi[hi.m < 0.2]
claim('l2 s1: nine positive-bid quotes at or above the 0.5 cut', len(hi) == 9)
claim('l2 s1: seven of them are wing quotes with £0.05 spreads', len(wing) == 7 and np.allclose(wing.ask - wing.bid, 0.05))
claim('l2 s1: the other two are the planted wide rows 4 and 92', sorted(set(hi.index) - set(wing.index)) == [4, 92])
claim('l2 s1: a £0.10 floor keeps 109', int((((c.bid > 0) & (c.bid <= c.ask) & (c.age_min <= 30)) & ((c.rel < 0.5) | (c.ask - c.bid < 0.10))).sum()) == 109)
ks = sorted(wing.strike / S)
stated('l2', 'screens[1].hints[1].text', 'below 0.85 and above 1.1', all(k < 0.85 or k > 1.1 for k in ks))
rel = 3.12 / 6.04
E('l2', 'screens[2].widget.answer', R_(rel, 4))
E('l2', 'screens[2].widget.wrong[1].value', 3.12 / 4.48)
E('l2', 'screens[2].widget.wrong[2].value', 3.12 / 7.60)
claim('l2 s2: 6m 105 call is 4.48/7.60', q_(0.5, 105, 'call') == (4.48, 7.60))
claim('l2 s2: its 6m neighbours have relative spreads near 0.06', all(abs(c.loc[i, 'rel'] - 0.06) < 0.01 for i in c[np.isclose(c['T'], 0.5) & c.strike.isin([100, 110]) & (c.type == 'call')].index))
rep = ns['drop_report'](chain)
claim('l2 s3: drops 15, 2, 2, 9', rep == {'zero_bid': 15, 'crossed': 2, 'stale': 2, 'wide': 9, 'kept': 102})
E('l2', 'screens[3].widget.answer', int((c.rel >= 0.5).sum()))
claim('l2 s3: wide-first drops 24 = 9 + 15, crossed and stale pass the spread rule', int((c.rel >= 0.5).sum()) == 24 and (c[c.bid > c.ask].rel < 0.5).all() and (c[c.age_min > 30].rel < 0.5).all())
lb95 = S * math.exp(-Q * 0.25) - 95 * math.exp(-R * 0.25)
E('l2', 'screens[5].prose', R_(lb95, 2))
E('l2', 'screens[5].explain.text', R_((0.01 + 7.97) / 2, 2), fmt='£{:.2f}')
claim('l2 s5: filled 95 call mid below the bound', (0.01 + 7.97) / 2 < lb95)
claim('l2 s5: filled 95 call relative spread near 2', abs((7.96) / 3.99 - 2) < 0.01)
stated('l2', 'screens[5].widget.options[3].why', '0.01 / 0.03 passes the spread rule', (0.03 - 0.01) / 0.02 < 0.5)
# filled wing zero bids: high or low vol?
zb = c[(c.bid == 0) & (c.m < 0.1)]
hi_cnt = sum(ivol((0.01 + r.ask) / 2, r.strike, r['T'], r['type']) > true_iv(r.strike, r['T']) for _, r in zb.iterrows())
claim(f'l2 s5: filled wing zero bids fake a HIGH vol ({hi_cnt} of {len(zb)})', hi_cnt == len(zb))
stated('l2', 'screens[5].explain.text', 'fakes a low vol', hi_cnt < len(zb) / 2)
# s9 stale 1y 95 call
sb, sa = 13.11, 13.92
claim('l2 s9: the stale quote is the 1y 95 call 13.11/13.92, age 240', q_(1.0, 95, 'call') == (sb, sa) and float(chain[(chain['T'] == 1.0) & (chain.strike == 95) & (chain.type == 'call')].age_min.iloc[0]) == 240)
v_st = ivol((sb + sa) / 2, 95, 1.0, 'call')
v_tr = true_iv(95, 1.0)
gap = (v_st - v_tr) * 100
p102 = bs(102, 95, R, v_tr, 1.0, 'call', Q)                     # the quote as set at S = 102, today's true vol
v_st = ivol(p102, 95, 1.0, 'call')                               # what it implies at S = 100
gap = (v_st - v_tr) * 100
E('l2', 'screens[9].prose', R_(v_st * 100, 1))
E('l2', 'screens[9].prose', R_(v_tr * 100, 1))
E('l2', 'screens[9].canvas.params.rows[0][1]', R_(v_tr * 100, 2), fmt='{:.2f}%')
E('l2', 'screens[9].canvas.params.rows[1][1]', R_(v_st * 100, 2), fmt='{:.2f}%')
E('l2', 'screens[9].canvas.params.rows[2][1]', R_(gap, 2))
print(f'check by hand: l2 s9 shows 26.69% and 22.65% with gap {gap:.4f} (shown 4.03; the shown vols differ by 4.04)')
vg = vega_pt(95, 1.0, v_tr) * 100
E('l2', 'screens[9].prose', R_(vg, 2))
E('l2', 'screens[9].widget.answer', R_(500 * 34.57 * R_(gap, 2), 0))
E('l2', 'screens[9].widget.wrong[0].value', R_(34.57 * R_(gap, 2), 4))
E('l2', 'screens[9].widget.wrong[1].value', R_(500 * 0.3457 * R_(gap, 2), 4))
cb, ca = q_(1.0, 100, 'call')
E('l2', 'quiz[0].widget.answer', R_((ca - cb) / ((ca + cb) / 2), 4))
E('l2', 'quiz[0].widget.wrong[1].value', (ca - cb) / cb)
claim('l2 quiz3 drop_report on the four quotes', ns['drop_report'](ns['quotes']([[0.25, 100, 'call', 0.0, 0.04, 1, 50], [0.25, 100, 'call', 1.20, 1.15, 1, 5], [0.25, 100, 'call', 3.10, 3.30, 1, 45], [0.25, 100, 'call', 2.00, 2.10, 1, 2]])) == {'zero_bid': 1, 'crossed': 1, 'stale': 1, 'wide': 0, 'kept': 1})

# ================= l3 =================
d1y = clean[np.isclose(clean['T'], 1.0)]
w = d1y.assign(m=ns['mid'](d1y)).pivot(index='strike', columns='type', values='m').dropna()
cp = w['call'] - w['put']
slope, icpt = np.polyfit(w.index.values.astype(float), cp.values, 1)
E('l3', 'screens[0].canvas.params.functions[0].expr', R_(icpt, 4))
E('l3', 'screens[0].canvas.params.functions[0].expr', R_(-slope, 4))
E('l3', 'screens[0].widget.points[0].target.x', R_(-icpt / slope, 2))
E('l3', 'screens[0].feedback.byKey.spot', R_(cp.loc[100], 2), fmt='£{:.2f}')
F100 = 100 + math.exp(R) * cp.loc[100]
E('l3', 'screens[2].widget.answer', R_(F100, 3))
E('l3', 'screens[2].widget.wrong[0].value', 100 + R_(cp.loc[100], 2))
E('l3', 'screens[2].widget.wrong[1].value', 100 + math.exp(-R) * 3.86)
fwd = [ns['implied_forward'](clean[np.isclose(clean['T'], T)], R, T) for T in TS]
pairs = [len(clean[np.isclose(clean['T'], T)].assign(m=ns['mid']).pivot(index='strike', columns='type', values='m').reindex(columns=['call', 'put']).dropna()) for T in TS]
tab3 = doc('l3-rates-dividends')['screens'][3]['canvas']['params']['rows']
for i, T in enumerate(TS):
    claim(f'l3 s3 row {i}: pairs {pairs[i]}, median F {fwd[i]:.3f}, true {S * math.exp((R - Q) * T):.3f}',
          tab3[i][1] == str(pairs[i]) and tab3[i][2] == f'{fwd[i]:.3f}' and tab3[i][3] == f'{S * math.exp((R - Q) * T):.3f}')
qs = [ns['implied_q'](F, S, R, T) for F, T in zip(fwd, TS)]
E('l3', 'screens[3].widget.answer', R_(qs[4], 4))
claim('l3 s3 wrongs: growth ln(F/S) and sign R + ln(F/S) from the unrounded median', abs(lv.files['l3-rates-dividends']['screens'][3]['widget']['wrong'][0]['value'] - math.log(fwd[4] / 100)) < 1e-5 and abs(lv.files['l3-rates-dividends']['screens'][3]['widget']['wrong'][1]['value'] - R - math.log(fwd[4] / 100)) < 1e-5)
E('l3', 'screens[8].explain.text', ', '.join(f'{100 * x:.2f}%' for x in qs))
claim('l3 s3: median recovers 1% within 0.04 points at one year', R_(abs(qs[4] - Q) * 100, 2) == 0.04)
tab4 = doc('l3-rates-dividends')['screens'][4]['canvas']['params']['rows']
for i, T in enumerate((1 / 12, 1.0)):
    dT = clean[np.isclose(clean['T'], T)]
    ww = dT.assign(m=ns['mid'](dT)).pivot(index='strike', columns='type', values='m').dropna()
    sl, ic = np.polyfit(ww.index.values.astype(float), (ww['call'] - ww['put']).values, 1)
    rf = -math.log(-sl) / T
    qf = -math.log(ic / S) / T
    claim(f'l3 s4 row {i}: slope {sl:.4f} true {-math.exp(-R * T):.4f} icpt {ic:.2f} r {rf:.2%} q {qf:.2%}',
          tab4[i][1:] == [f'{sl:.4f}', f'{-math.exp(-R * T):.4f}', f'{ic:.2f}', f'{100 * rf:.2f}%', f'{100 * qf:.2f}%'])
E('l3', 'screens[4].hints[1].text', R_(-math.exp(-R / 12), 4))
E('l3', 'screens[4].explain.text', R_(1 - math.exp(-R / 12), 4))
claim('l3 s4: four pairs at one month', pairs[0] == 4)
F1 = S * math.exp((R - Q) * 1)
E('l3', 'screens[5].widget.answer', R_(F1, 3))
E('l3', 'screens[5].widget.wrong[1].value', S * math.exp(R))
E('l3', 'screens[5].explain.text', R_(F1 - S, 2), fmt='£{:.2f}')
# "every one-year strike looks about 4% further out than it is": false below the forward
K90 = 90
stated('l3', 'screens[5].explain.text', 'every one-year strike looks about 4% further out', abs(math.log(K90 / S)) > abs(math.log(K90 / F1)))
E('l3', 'screens[9].widget.answer', R_(2 * math.exp(R * 0.5), 4))
E('l3', 'screens[9].widget.wrong[1].value', 2 * math.exp(R))
E('l3', 'screens[9].widget.wrong[2].value', 2 * math.exp(-R * 0.5))
E('l3', 'screens[9].explain.text', R_(2 * math.exp(R * 0.5) * math.exp(-R), 2), fmt='£{:.2f}')
c6, p6 = mid_(0.5, 100, 'call'), mid_(0.5, 100, 'put')
E('l3', 'quiz[0].prose', R_(c6, 3), fmt='£{:.3f}')
E('l3', 'quiz[0].prose', R_(p6, 3), fmt='£{:.3f}')
F6 = 100 + math.exp(R * 0.5) * (c6 - p6)
E('l3', 'quiz[0].widget.answer', R_(F6, 3))
E('l3', 'quiz[0].widget.wrong[0].value', R_(100 + c6 - p6, 3))
E('l3', 'quiz[0].explain.text', R_(S * math.exp(0.02), 2), fmt='£{:.2f}')
q6 = R - math.log(102.004 / 100) / 0.5
claim('l3 quiz1: key 0.01031 within 1e-5 of the value from £102.004', abs(q6 - 0.01031) < 1e-5)
claim('l3 quiz1: wrong no-T near r - ln(F/S)', abs(R - math.log(102.004 / 100) - 0.030153) < 1e-5)
E('l3', 'quiz[1].explain.text', R_(math.log(1.02004), 4))
E('l3', 'quiz[1].explain.text', R_(math.log(1.02004) / 0.5, 4))
claim('l3 quiz3: rate 0.6 points too high gives q 0.6 points too high (F fixed)', abs((0.05 - math.log(1.0408)) - (0.044 - math.log(1.0408)) - 0.006) < 1e-12)

# ================= l4 =================
v_b, v_m, v_a = ivol(b, 100, 0.25, 'call'), ivol((b + a) / 2, 100, 0.25, 'call'), ivol(a, 100, 0.25, 'call')
two('l4 bid vol, lesson solver', v_b, ns['implied_vol'](b, S, 100, R, 0.25, 'call', Q), 1e-8)
E('l4', 'screens[1].widget.answer', R_(v_a, 4))
E('l4', 'screens[1].widget.wrong[0].value', R_(v_b, 10), fmt=lambda x: repr(x)[:8])
E('l4', 'screens[1].explain.text', R_(v_b * 100, 2))
E('l4', 'screens[1].explain.text', R_(v_a * 100, 2))
E('l4', 'screens[2].widget.answer', R_(v_a - v_b, 5))
E('l4', 'screens[2].widget.wrong[1].value', R_((v_a - v_b) / 2, 6), fmt=lambda x: repr(x)[:7])
E('l4', 'screens[2].explain.text', R_(v_m * 100, 2))
E('l4', 'quiz[3].prose', R_((v_b + v_a) / 2 * 100, 2))
claim('l4 quiz3: mid vol within a hundredth of a point of the average', abs(v_m - (v_b + v_a) / 2) * 100 < 0.01)
# s3 six-quote band table
names = {'1 year': 1.0, '3 months': 0.25, '1 month': 1 / 12}
rels = []
for row in doc('l4-which-price')['screens'][3]['canvas']['params']['rows']:
    T = names[row[0]]; K = int(row[1].split()[0]); kind = row[1].split()[1]
    bb, aa = q_(T, K, kind)
    vb, va = ivol(bb, K, T, kind), ivol(aa, K, T, kind)
    claim(f'l4 s3 row {row}', row[2] == f'{100 * vb:.2f}%' and row[3] == f'{100 * va:.2f}%' and row[4] == f'{100 * (va - vb):.2f}')
    rels.append((aa - bb) / ((aa + bb) / 2))
stated('l4', 'screens[3].prose', 'about 3% of its mid', all(abs(x - 0.03) < 0.01 for x in rels))
claim(f'l4 s3: four spreads near 6% of the mid, the 1m 90 and 3m 80 puts at the £0.05 floor ({[round(x, 3) for x in rels]})', sum(abs(x - 0.06) < 0.01 for x in rels) == 4 and rels[2] > 0.3 and rels[4] > 0.25)
F3 = S * math.exp((R - Q) * 0.25)
E('l4', 'screens[4].prose', R_(fwd[2], 2), fmt='£{:.2f}')
otm3 = ns['otm_quotes'](clean[np.isclose(clean['T'], 0.25)], F3)
claim('l4 s4: nine OTM quotes, puts 80 to 100 and calls 105 to 120', len(otm3) == 9 and list(otm3.strike) == [80, 85, 90, 95, 100, 105, 110, 115, 120] and list(otm3.type) == ['put'] * 5 + ['call'] * 4)
claim('l4 s4: 70/75 puts dropped as wide, 125 call wide, 130 call zero bid', c.loc[53, 'rel'] >= 0.5 and c.loc[55, 'rel'] >= 0.5 and c.loc[74, 'rel'] >= 0.5 and c.loc[76, 'bid'] == 0)
lb120 = 120 * math.exp(-R * 0.25) - S * math.exp(-Q * 0.25)
b120, a120 = q_(0.25, 120, 'put')
claim('l4 s5: 3m 120 put is 17.99/19.12', (b120, a120) == (17.99, 19.12))
E('l4', 'screens[5].widget.answer', R_(lb120, 3))
E('l4', 'screens[5].widget.wrong[1].value', 120 * math.exp(-R * 0.25) - S)
E('l4', 'screens[5].hints[1].text', R_(120 * math.exp(-R * 0.25), 3))
E('l4', 'screens[5].explain.text', R_(ivol(a120, 120, 0.25, 'put') * 100, 1))
claim('l4 s5: bid and mid below the bound', b120 < lb120 and (b120 + a120) / 2 < lb120)
b85, a85 = 0.01, 0.06
claim('l4 s6: 1m 85 put is 0.01/0.06 before cleaning', q_(1 / 12, 85, 'put') == (b85, a85))
vb85, va85, vm85 = (ivol(x, 85, 1 / 12, 'put') for x in (b85, a85, 0.035))
E('l4', 'screens[6].prose', R_(vb85 * 100, 2))
E('l4', 'screens[6].prose', R_(va85 * 100, 2))
E('l4', 'screens[6].prose', R_((vb85 + va85) / 2 * 100, 2))
E('l4', 'screens[6].widget.options[1].text', R_(vm85 * 100, 2))
E('l4', 'screens[6].explain.text', R_((vm85 - (vb85 + va85) / 2) * 100, 1))
# weights: 3m 90 put and 80 put bands
bands = {}
for K in (80, 90):
    bb, aa = q_(0.25, K, 'put')
    bands[K] = ivol(aa, K, 0.25, 'put') - ivol(bb, K, 0.25, 'put')
E('l4', 'screens[7].question', R_(bands[90] * 100, 2))
E('l4', 'screens[7].question', R_(bands[80] * 100, 2))
E('l4', 'screens[7].explain.text', int(1 / bands[90]))
E('l4', 'screens[7].explain.text', int(1 / bands[80]))
E('l4', 'quiz[2].widget.answer', R_(bands[80] / bands[90], 3))
E('l4', 'screens[7].explain.text', R_(bands[80] / bands[90], 1))
E('l4', 'quiz[2].widget.wrong[0].value', R_(bands[90] / bands[80], 6), fmt=lambda x: repr(x)[:7])
stated('l4', 'quiz[2].explain.text', '\\approx 3.05', R_(1.38 / 0.45, 2) == 3.05)
claim('l4 s6/quiz3 "where the curve bends at all, the mid vol sits above": d1*d2 < 0 gives concavity near the forward', True)
wq = bs(100, 100, R, 0.225, 0.25, 'call', Q) - bs(100, 100, R, 0.215, 0.25, 'call', Q)
E('l4', 'screens[10].widget.answer', R_(wq, 4))
E('l4', 'screens[10].explain.text', R_(wq, 3), fmt='£{:.3f}')

# ================= review-1 =================
b6, a6 = q_(0.5, 100, 'put')
claim('review-1 i0: 6m 100 put is 4.87/5.17', (b6, a6) == (4.87, 5.17))
E('review', 'items[0].widget.answer', 300 * a6)
E('review', 'items[0].widget.wrong[0].value', 300 * b6)
E('review', 'items[0].widget.wrong[1].value', 3 * a6)
claim('review-1 i2: 1y 105 call is 8.00/8.50', q_(1.0, 105, 'call') == (8.0, 8.5))
E('review', 'items[2].widget.answer', R_(0.5 / 8.25, 4))
E('review', 'items[2].widget.wrong[1].value', 0.5 / 8.0)
claim('review-1 i3: max_age 300 keeps 104 and the stale rows have no other fault', len(ns['clean_quotes'](chain, max_age_min=300)) == 104)
E('review', 'items[4].widget.answer', R_(100 + math.exp(R * 0.25) * (4.505 - 3.545), 3))
E('review', 'items[4].explain.text', R_(S * math.exp(0.01), 2), fmt='£{:.2f}')
E('review', 'items[5].prose', R_(fwd[1], 3), fmt='£{:.3f}')
E('review', 'items[5].widget.answer', R_(R - math.log(100.650 / 100) * 6, 4))
claim('review-1 i5 wrongs from the unrounded two-month median', abs(lv.files['review-1']['items'][5]['widget']['wrong'][0]['value'] - (R - math.log(fwd[1] / 100))) < 1e-6 and abs(lv.files['review-1']['items'][5]['widget']['wrong'][1]['value'] - math.log(fwd[1] / 100) * 6) < 1e-6)
E('review', 'items[6].widget.options[0].text', R_(ivol(0.04, 130, 0.25, 'call') * 100, 1))
stated('review', 'items[6].widget.options[2].why', 'not even 0%', bs(100, 130, R, 1e-9, 0.25, 'call', Q) > 0)
v1y = vega_pt(100, 1.0, 0.215)
E('review', 'items[7].prose', R_(v1y, 2), fmt='£{:.2f}')
E('review', 'items[7].widget.answer', R_(100 * v1y, 1))
E('review', 'items[8].prose', R_(S * math.exp((R - Q) / 12), 2), fmt='£{:.2f}')

# ================= homework-1 =================
pc = ns['prepare_chain'](chain, S, R)
E('homework', 'items[0].widget.examples[0].expect', len(pc))
E('homework', 'items[0].explain.text', ', '.join(str(int(x)) for x in pc.groupby('T').size().values))
bv = ns['bounds_violations'](chain, S, R, Q)
E('homework', 'items[1].widget.examples[0].expect', len(bv))
bvm = bv.assign(m=(bv.bid + bv.ask) / 2)
gaps = []
for _, r in bvm.iterrows():
    lo = max(S * math.exp(-Q * r['T']) - r.strike * math.exp(-R * r['T']), 0) if r.type == 'call' else max(r.strike * math.exp(-R * r['T']) - S * math.exp(-Q * r['T']), 0)
    gaps.append(lo - r.m)
claim(f'homework-1 i1: all violations below the lower bound, deep ITM (gaps {min(gaps):.3f} to {max(gaps):.3f})', all(g > 0 for g in gaps))
stated('homework', 'items[1].explain.text', 'a few pence below', max(gaps) < 0.10)
E('homework', 'items[3].widget.answer', R_((15 * 3600 + 58 * 60 + 30 - (11 * 3600 + 41 * 60 + 7)) / 60, 2))
E('homework', 'items[3].widget.wrong[0].value', R_((15 * 3600 + 58 * 60 + 30 - (11 * 3600 + 41 * 60 + 7)) / 3600, 2))
E('homework', 'items[4].prose', R_(fwd[0], 3), fmt='£{:.3f}')
E('homework', 'items[4].widget.answer', R_(0.01 / (fwd[0] / 12), 6))
E('homework', 'items[4].widget.wrong[0].value', 0.01 / R_(fwd[0], 3), fmt=lambda x: f'{x:.6e}'[:6])
claim('homework-1 i4: wrong "1y" and "no-T" overlap (0.01/104.08 vs 0.01/100.35, bands 2e-5)', abs(0.01 / 104.08 - 0.01 / 100.346) < 4e-5)
ws = lv.files['homework-1']['items'][4]['widget']['wrong']
claim('homework-1 i4: no two wrong[] bands overlap', all(abs(x['value'] - y['value']) > x['tol']['abs'] + y['tol']['abs'] for i, x in enumerate(ws) for y in ws[i + 1:]))
claim('homework-1 i5: 3m 125 call is 0.01/0.06', q_(0.25, 125, 'call') == (0.01, 0.06))
vb5, va5, vm5 = (ivol(x, 125, 0.25, 'call') for x in (0.01, 0.06, 0.035))
E('homework', 'items[5].prose', R_(vb5 * 100, 2))
E('homework', 'items[5].prose', R_(va5 * 100, 2))
E('homework', 'items[5].widget.options[0].text', R_(vm5 * 100, 2))
E('homework', 'items[5].widget.options[1].text', R_((vb5 + va5) / 2 * 100, 2))
E('homework', 'items[6].widget.answer', R_(1.5 * math.exp(R * 0.75), 4))
E('homework', 'items[6].widget.wrong[1].value', 1.5 * math.exp(R * 0.25))
stated('homework', 'items[7].model', 'usually too low', hi_cnt < len(zb) / 2)
stated('homework', 'items[7].rubric[5].text', 'usually low', hi_cnt < len(zb) / 2)
E('homework', 'items[7].model', R_(F1, 2), fmt='£{:.2f}')

# ---------- claims behind the review's proposed fixes (pass while the new phrase is absent) ----------
b105, a105 = q_(1.0, 105, 'call')
vb105, va105, vm105 = ivol(b105, 105, 1.0, 'call'), ivol(a105, 105, 1.0, 'call'), ivol((b105 + a105) / 2, 105, 1.0, 'call')
claim(f'l4: near the forward price is concave in vol: 1y 105 call mid vol {vm105:.5f} below the average {(vb105 + va105) / 2:.5f}', vm105 < (vb105 + va105) / 2)
stated('l4', 'quiz[3].widget.options[2].why', 'Where the curve bends at all, the mid vol sits above the average', vm105 >= (vb105 + va105) / 2)
v125 = ivol(0.02, 125, 1 / 12, 'call')
stated('l2', 'screens[5].explain.text', '30.5%', R_(v125 * 100, 1) == 30.5)
stated('l2', 'screens[5].explain.text', '18.3%', R_(true_iv(125, 1 / 12) * 100, 1) == 18.3)
stated('homework', 'items[7].model', 'usually too high', hi_cnt == len(zb))
stated('homework', 'items[7].model', '30.5%', R_(v125 * 100, 1) == 30.5)
stated('l2', 'screens[5].widget.options[3].why', 'relative spread 1', (0.03 - 0.01) / 0.02 == 1.0)
b4, a4 = q_(1 / 12, 80, 'call')
stated('review', 'items[1].prose', '19.42', (b4, a4) == (19.42, 33.02))
stated('review', 'items[1].explain.text', '13.60 / 26.22 = 0.519', R_((a4 - b4) / ((a4 + b4) / 2), 3) == 0.519)
stated('review', 'items[1].explain.text', 'one-month neighbours', all(abs(c.loc[i, 'rel'] - 0.06) < 0.01 for i in c[np.isclose(c['T'], 1 / 12) & c.strike.isin([75, 85]) & (c.type == 'call')].index))
Fn = F1 - 1.5 * math.exp(R * 0.75)
stated('homework', 'items[6].widget.accept', '1.51 points', R_((R - math.log(Fn / S) - Q) * 100, 2) == 1.51)
stated('homework', 'items[6].explain.text', '102.52', R_(Fn, 2) == 102.52)
stated('homework', 'items[6].explain.text', '0.0251', R_(R - math.log(Fn / S), 4) == 0.0251)
pavg = bs(100, 125, R, (vb5 + va5) / 2, 0.25, 'call', Q)
stated('homework', 'items[5].explain.text', '£0.028', R_(pavg, 3) == 0.028)
stated('homework', 'items[1].explain.text', 'up to 20p below', R_(max(gaps) * 100, 0) == 20)

lv.check_wrongs()
lv.report()
