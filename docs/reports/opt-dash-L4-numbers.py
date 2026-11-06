"""opt-dash level 4 (Greeks and the dashboard): second reader's number checks (review-opt-dash-3-4.md).

Recomputed from first principles: Black-Scholes Greeks with a dividend yield (Hull's formulas), central
differences, a 500-step CRR tree with its node values, the P&L explain against full revaluation, the course
generator make_chain (seed 2320) with level 1's cleaning and implied forwards, and the static arbitrage
checks. Checks that fail on the current content mark a finding and pass once the fix is pasted.
"""
import os, sys
from math import erf, exp, log, sqrt, pi
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('opt-dash', 4)
L13, L14, L15, L16, R, H = 'l13', 'l14', 'l15', 'l16', 'review', 'homework'


def N(z): return 0.5 * (1 + erf(z / sqrt(2)))
def phi(z): return exp(-z * z / 2) / sqrt(2 * pi)


def bs(S, K, r, s, T, kind='call', q=0.0):
    d1 = (log(S / K) + (r - q + s * s / 2) * T) / (s * sqrt(T)); d2 = d1 - s * sqrt(T)
    if kind == 'call':
        return S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2)
    return K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1)


def greeks(S, K, r, s, T, kind='call', q=0.0):
    d1 = (log(S / K) + (r - q + s * s / 2) * T) / (s * sqrt(T)); d2 = d1 - s * sqrt(T)
    Sq, Kr = S * exp(-q * T), K * exp(-r * T)
    g = dict(gamma=exp(-q * T) * phi(d1) / (S * s * sqrt(T)), vega=Sq * phi(d1) * sqrt(T), d1=d1, d2=d2)
    decay = -Sq * phi(d1) * s / (2 * sqrt(T))
    if kind == 'call':
        g.update(delta=exp(-q * T) * N(d1), theta=decay - r * Kr * N(d2) + q * Sq * N(d1), rho=K * T * exp(-r * T) * N(d2))
    else:
        g.update(delta=-exp(-q * T) * N(-d1), theta=decay + r * Kr * N(-d2) - q * Sq * N(-d1), rho=-K * T * exp(-r * T) * N(-d2))
    return g


def explain(S, K, r, s, T, dS, ds, dt, kind='call', q=0.0):
    G = greeks(S, K, r, s, T, kind, q)
    terms = [G['delta'] * dS, .5 * G['gamma'] * dS ** 2, G['vega'] * ds, G['theta'] * dt]
    act = bs(S + dS, K, r, s + ds, T - dt, kind, q) - bs(S, K, r, s, T, kind, q)
    return terms, sum(terms), act


g = greeks(100, 100, .05, .2, 1); C0 = bs(100, 100, .05, .2, 1)
f = lambda x: bs(x, 100, .05, .2, 1)

# ---------------- l13 ----------------
lv.expect(L13, 'screens[0].prose', round(C0, 4)); lv.expect(L13, 'screens[0].explain.text', round(g['delta'], 4))
lv.expect(L13, 'screens[2].prose', round(g['d1'], 2)); lv.expect(L13, 'screens[2].prose', round(g['d2'], 2))
for i, (k, n) in enumerate((('delta', 4), ('gamma', 4), ('vega', 2), ('theta', 3), ('rho', 2))):
    lv.expect(L13, f'screens[2].canvas.params.rows[{i}][2]', round(g[k], n))
lv.expect(L13, 'screens[2].widget.rows[0][2].answer', round(g['vega'] / 100, 4))
lv.expect(L13, 'screens[2].widget.rows[1][2].answer', round(g['theta'] / 365, 4))
lv.expect(L13, 'screens[3].canvas.params.lines[3]', round(g['rho'], 4)); lv.expect(L13, 'screens[3].canvas.params.lines[2]', round(g['vega'], 3))
lv.expect(L13, 'screens[3].explain.text', round(greeks(100, 100, .05, .2, 1, 'call', .01)['delta'], 4))
d04 = lambda x: greeks(x, 100, .05, .2, .04)['delta']
lv.expect(L13, 'screens[1].hints[2].text', '{:.1f}'.format(d04(95)))          # finding: content says "about 0.2 to 0.8"
lv.expect(L13, 'screens[1].hints[2].text', '{:.1f}'.format(d04(105)))
err = lambda h: g['delta'] - (f(100 + h) - f(100 - h)) / (2 * h)
lv.expect(L13, 'screens[4].canvas.derive.caption', round(g['delta'], 8))
lv.expect(L13, 'screens[4].widget.accept', round(err(2), 6)); lv.expect(L13, 'screens[4].widget.accept', round(err(1), 6))
lv.expect(L13, 'screens[4].widget.answer', round(err(2) / err(1)))
lv.expect(L13, 'screens[4].prose', round(g['delta'], 6))
lv._rec(abs(err(.01)) < 5e-7, 'l13 s4 explain: h = 0.01 matches delta to six places', f'{err(.01):.1e}')
digits = {e: -log(abs((f(100 + 10.0 ** e) - 2 * f(100) + f(100 - 10.0 ** e)) / 10.0 ** (2 * e) - g['gamma']), 10) for e in range(1, -8, -1)}
lv._rec([e for e in digits if digits[e] > 6] == [-1, -2, -3, -4], 'l13 s5 bumps with gamma error below 1e-6 are 0.1 to 0.0001', str({e: round(v, 2) for e, v in digits.items()}))
lv.expect(L13, 'screens[5].prose', round(g['gamma'], 6))
gam6 = (f(100 + 1e-6) - 2 * f(100) + f(100 - 1e-6)) / 1e-12
lv.expect(L13, 'screens[5].feedback.byKey.hm6', round(gam6, 4)); lv.expect(L13, 'summary.trap', round(gam6, 4))
agree = -log(abs(f(100 + 1e-6) - f(100)) / f(100), 10)
lv.expect(L13, 'screens[5].feedback.byKey.smallest', '{:.0f} digits'.format(agree))     # finding: content says "agree to 15 digits"
eps = 2 ** -52
V4 = (f(100 + .05) - 4 * f(100 + .025) + 6 * f(100) - 4 * f(100 - .025) + f(100 - .05)) / .025 ** 4
hstar = (48 * eps * C0 / abs(V4)) ** .25
lv._rec(0.005 < hstar < 0.01, 'l13 s5 and s8: the balance bump is a few thousandths of a pound (content: near £0.007)', f'{hstar:.4f} with eps = 2^-52')
lv.expect(L13, 'screens[5].explain.text', 0.007)
lv._rec(max(digits, key=digits.get) == -2, 'l13 s9 best bump on the grid is 0.01', '')

def tree(S, K, r, s, T, n):
    dt = T / n; u = exp(s * sqrt(dt)); d = 1 / u; p = (exp(r * dt) - d) / (u - d); disc = exp(-r * dt)
    v = np.maximum(S * u ** (2 * np.arange(n + 1) - n) - K, 0.0); levels = {}
    for i in range(n - 1, -1, -1):
        v = disc * (p * v[1:] + (1 - p) * v[:-1])
        if i <= 2:
            levels[i] = v.copy()
    return levels, u
lev, u = tree(100, 100, .05, .2, 1, 500)
lv.expect(L13, 'screens[7].canvas.params.rows[0][3]', round(float(lev[0][0]), 4))
lv.expect(L13, 'screens[7].canvas.params.rows[1][2]', round(100 / u, 4)); lv.expect(L13, 'screens[7].canvas.params.rows[2][2]', round(100 * u, 4))
lv.expect(L13, 'screens[7].canvas.params.rows[1][3]', round(float(lev[1][0]), 4)); lv.expect(L13, 'screens[7].canvas.params.rows[2][3]', round(float(lev[1][1]), 4))
lv.expect(L13, 'screens[7].canvas.params.rows[3][2]', round(100 / u ** 2, 4)); lv.expect(L13, 'screens[7].canvas.params.rows[5][2]', round(100 * u ** 2, 4))
for i, j in ((3, 0), (4, 1), (5, 2)):
    lv.expect(L13, f'screens[7].canvas.params.rows[{i}][3]', round(float(lev[2][j]), 4))
tdelta = (lev[1][1] - lev[1][0]) / (100 * u - 100 / u)
lv.expect(L13, 'screens[7].widget.answer', round(float(tdelta), 4))
lv.expect(L13, 'screens[7].widget.wrong[0].value', round(float(lev[1][1] - lev[1][0]), 4))
lv.expect(L13, 'screens[7].widget.wrong[1].value', round(float(lev[1][1]) / (100 * u), 4))
tg = ((lev[2][2] - lev[2][1]) / (100 * u * u - 100) - (lev[2][1] - lev[2][0]) / (100 - 100 / u ** 2)) / ((100 * u * u - 100 / u ** 2) / 2)
lv.expect(L13, 'screens[7].explain.text', round(float(tg), 4))
lv.expect(L13, 'screens[7].feedback.byKey', round(100 * u - 100 / u, 2))
lv.expect(L13, 'screens[10].widget.answer', round(5000 * g['vega'] / 100 * 1.5))
lv.expect(L13, 'screens[10].widget.wrong[0].value', round(5000 * g['vega'] * 1.5))
lv.expect(L13, 'screens[10].widget.wrong[1].value', round(5000 * g['vega'] / 100))
lv.expect(L13, 'quiz[0].widget.answer', round(greeks(100, 100, .05, .2, 1, 'put')['delta'], 4))
lv.expect(L13, 'quiz[1].widget.answer', round(-g['theta'] / 365, 4))
lv._rec(greeks(100, 150, .05, .2, 1 / 12)['delta'] < 1e-6, 'l13 quiz[3] one-month 150 call delta below 1e-6', '')

# ---------------- l14 ----------------
dm = lambda K: greeks(100, K, .05, .2, 1 / 12)['delta']
lv._rec(dm(90) > .97 and dm(110) < .07, 'l14 s0 one-month delta close to 1 at 90 and 0 at 110', f'{dm(90):.3f} {dm(110):.3f}')
lv.expect(L14, 'screens[1].hints[2].text', round(greeks(100, 100, .05, .2, .02)['gamma'], 2)); lv.expect(L14, 'screens[1].hints[2].text', round(g['gamma'], 4))
lv.expect(L14, 'screens[2].widget.answer', round(greeks(100, 100, .05, .2, .25)['vega'] / 100, 4))
lv.expect(L14, 'screens[2].widget.wrong[0].value', round(g['vega'] / 100 * .25, 4))
lv.expect(L14, 'screens[3].explain.text', round(greeks(100, 100, .05, .2, 1 / 52)['delta'], 2))
lv.expect(L14, 'screens[3].widget.options[3].why', round(greeks(100, 110, .05, .2, 1)['delta'], 2))
lv.expect(L14, 'screens[4].canvas.params.lines[1]', round(greeks(100, 90, .05, .2, 1)['delta'], 4)); lv.expect(L14, 'screens[4].canvas.params.lines[1]', round(greeks(100, 110, .05, .2, 1)['delta'], 4))
t2, e2, a2 = explain(100, 100, .05, .2, 1, 2, .01, 1 / 365)
for i, t in zip((0, 2, 3), (t2[0], t2[2], t2[3])):
    lv.expect(L14, f'screens[5].widget.rows[{i}][2]', round(t, 4))
lv.expect(L14, 'screens[5].widget.rows[1][2].answer', round(t2[1], 4)); lv.expect(L14, 'screens[5].widget.rows[4][2].answer', round(e2, 4))
lv.expect(L14, 'screens[5].widget.rows[5][2]', round(a2, 4)); lv.expect(L14, 'screens[5].explain.text', round(a2 - e2, 4))
lv.expect(L14, 'screens[5].hints[2].text', '{:.4f}'.format(sum(round(t, 4) for t in t2)))          # finding: the shown terms add to 1.6688
t10, e10, a10 = explain(100, 100, .05, .2, 1, 10, .01, 1 / 365)
lv.expect(L14, 'screens[6].widget.answer', round(t10[1], 4)); lv.expect(L14, 'screens[6].explain.text', round(e10, 4))
lv.expect(L14, 'screens[6].explain.text', round(a10, 4)); lv.expect(L14, 'screens[6].explain.text', round(a10 - e10, 4))
tm, em, am = explain(100, 100, .05, .2, 1, -10, 0, 1 / 365)
lv.expect(L14, 'screens[7].canvas.params.rows[3][1]', round(am, 4)); lv.expect(L14, 'screens[7].explain.text', round(em, 4))
lv.expect(L14, 'screens[7].hints[1].text', round(greeks(90, 100, .05, .2, 1 - 1 / 365)['delta'], 2))
be = sqrt(2 * -g['theta'] / 365 / g['gamma']); cash = g['delta'] * 100 - C0
lv.expect(L14, 'screens[8].widget.answer', round(be, 2)); lv.expect(L14, 'screens[8].widget.wrong[0].value', round(be * be, 2))
lv.expect(L14, 'screens[8].explain.text', round(.2 * 100 * sqrt(1 / 365), 2))
lv._rec(abs(sqrt(2 * (-g['theta'] / 365 - cash * .05 / 365) / g['gamma']) - .2 * 100 * sqrt(1 / 365)) < 1e-9, 'l14 s8 with interest on the hedge cash the break-even is exactly sigma S sqrt(dt)', '')
lv.expect(L14, 'screens[8].explain.text', round(cash, 2))                                           # finding: the hedge's cash and its interest are missing
lv.expect(L14, 'screens[8].explain.text', '{:.2f}p'.format(cash * .05 / 365 * 100))
lv._rec(abs(g['theta'] + .05 * 100 * g['delta'] + .5 * .2 ** 2 * 100 ** 2 * g['gamma'] - .05 * C0) < 1e-9, 'l14 s8 Black-Scholes equation (Hull ch. 15): theta + r S delta + sigma^2 S^2 gamma / 2 = r C, so the hedge with interest earns gamma (dS^2 - sigma^2 S^2 dt) / 2', '')
lv.expect(L14, 'screens[8].explain.text', round(g['delta'] * 100, 2)); lv.expect(L14, 'screens[8].explain.text', round(C0, 2)); lv.expect(L14, 'screens[8].explain.text', round(be, 2))
lv.expect(H, 'items[2].explain.text', round(cash, 2)); lv.expect(H, 'items[2].explain.text', round(be, 2))
lv.expect(L14, 'screens[9].canvas.params.lines[1]', round(a2 - e2, 4))
lv.expect(L14, 'screens[9].explain.text', '0.0000'); lv._rec(abs(explain(100, 100, .05, .2, 1, 0, 0, 1 / 365)[2] - g['theta'] / 365) < 5e-5, 'l14 s9 quiet-day residual rounds to 0.0000', '')
van = -phi(g['d1']) * g['d2'] / .2
lv.expect(L14, 'screens[10].explain.text', round(van, 3)); lv.expect(L14, 'screens[10].explain.text', round(van * .02, 4))
lv.expect(L14, 'screens[10].explain.text', 'twenty'); lv._rec(round((a10 - e10) / (a2 - e2)) == 20, 'l14 s10 the £10 residual is about twenty times the £2 one', f'{(a10 - e10) / (a2 - e2):.1f}')
lv.expect(L14, 'screens[11].hints[2].text', -31900 + 12400)
c3, p3 = greeks(100, 100, .05, .2, .25), greeks(100, 100, .05, .2, .25, 'put')
lv.expect(L14, 'quiz[2].explain.text', round(-(c3['gamma'] + p3['gamma']), 3)); lv.expect(L14, 'quiz[2].explain.text', round(-(c3['vega'] + p3['vega']) / 100, 2))
lv.expect(L14, 'quiz[2].explain.text', '{:.1f}p'.format(-(c3['theta'] + p3['theta']) / 365 * 100))
lv.expect(L14, 'quiz[0].widget.answer', round(g['theta'] / 365, 4))

# ---------------- l15 (chain) ----------------
def true_iv(K, T, S=100.0, r=0.05, q=0.01):
    m = log(K / (S * exp((r - q) * T))) / sqrt(T)
    return 0.22 - 0.045 * exp(-T / 0.3) - 0.08 * m + 0.10 * m * m


def make_chain(seed=2320, S=100.0, r=0.05, q=0.01):
    rng = np.random.default_rng(seed); rows = []
    for T in [1 / 12, 2 / 12, 3 / 12, 6 / 12, 1.0]:
        for K in range(70, 131, 5):
            for kind in ('call', 'put'):
                mid = bs(S, K, r, true_iv(K, T, S, r, q), T, kind, q)
                half = max(0.025, 0.03 * mid); noise = 0.2 * half * rng.standard_normal()
                rows.append([T, K, kind, max(round(mid - half + noise, 2), 0.0), round(mid + half + noise, 2), int(rng.integers(0, 5000)), 0.0])
    df = pd.DataFrame(rows, columns=['T', 'strike', 'type', 'bid', 'ask', 'volume', 'age_min'])
    bad = rng.choice(len(df), 9, replace=False)
    df.loc[bad[:3], 'bid'] = 0.0; df.loc[bad[3:5], 'bid'] = df.loc[bad[3:5], 'ask'] + 0.05
    df.loc[bad[5:7], 'age_min'] = 240.0; df.loc[bad[7:], 'ask'] = (df.loc[bad[7:], 'ask'] * 1.6).round(2)
    return df


raw = make_chain(); m_ = (raw.bid + raw.ask) / 2
ok = (raw.bid > 0) & (raw.bid <= raw.ask) & (raw.age_min <= 30) & ((raw.ask - raw.bid) / m_ < 0.5)
clean = raw[ok].reset_index(drop=True); clean['mid'] = (clean.bid + clean.ask) / 2
Ts = sorted(clean['T'].unique())
c6 = clean[np.isclose(clean['T'], .5) & (clean.type == 'call')].sort_values('strike')
planted = dict(zip(c6.strike, c6.mid)); planted[100] += 1.5
for i, (K, P) in enumerate(sorted(planted.items())):
    lv.expect(L15, f'screens[0].canvas.params.points[{i}][1]', round(P, 3))
lv._rec(105 not in planted, 'l15 s4 cleaning dropped the six-month 105 call', '')
lv.expect(L15, 'screens[1].widget.answer', round(planted[90] - 2 * planted[100] + planted[110], 4))
lv.expect(L15, 'screens[1].widget.wrong[0].value', round(planted[90] - planted[100] + planted[110], 4))
lv.expect(L15, 'screens[2].widget.answer', round(5 * exp(-.025), 4))
wq = (110 - 100) / 15; chord = wq * planted[95] + (1 - wq) * planted[110]
lv.expect(L15, 'screens[4].widget.rows[1][2].answer', round(chord, 4)); lv.expect(L15, 'screens[4].explain.text', round(2 * (planted[100] - chord), 4))
lv.expect(L15, 'screens[3].feedback.correct', round(2 * (planted[100] - chord), 4))
fails = []
for T in Ts:
    d = clean[np.isclose(clean['T'], T) & (clean.type == 'call')].sort_values('strike')
    K, C, sp = list(d.strike), list(d.mid), list(d.ask - d.bid)
    fT = []
    for i in range(1, len(K) - 1):
        w = (K[i + 1] - K[i]) / (K[i + 1] - K[i - 1]); fly = 2 * (w * C[i - 1] + (1 - w) * C[i + 1] - C[i])
        if fly < -1e-12:
            fT.append((K[i], -fly, sp[i]))
    fails.append(fT)
for i, fT in enumerate(fails):
    lv.expect(L15, f'screens[5].canvas.params.rows[{i}][1]', len(fT))
lv.expect(L15, 'screens[5].widget.answer', sum(len(x) for x in fails))
flat = [x for fT in fails for x in fT]
for i, (K, amt, sp) in enumerate(flat):
    lv.expect(L15, f'screens[6].canvas.params.rows[{i}][1]', K); lv.expect(L15, f'screens[6].canvas.params.rows[{i}][2]', round(amt, 3)); lv.expect(L15, f'screens[6].canvas.params.rows[{i}][3]', round(sp, 2))
lv._rec(all(a < s for _, a, s in flat), 'l15 s6 every raw failure is below the middle call spread', '')
lv.expect(L15, 'screens[7].widget.options[0].text', round(.3 ** 2 * .25, 4)); lv.expect(L15, 'screens[7].widget.options[2].why', round(.22 ** 2 * .5, 4))
lv.expect(L15, 'screens[7].explain.text', round(sqrt((.22 ** 2 * .5 - .3 ** 2 * .25) / .25) * 100, 1))
lv.expect(L15, 'quiz[0].widget.answer', round(8 - 2 * 5.2 + 2.6, 4)); lv.expect(L15, 'quiz[1].widget.options[0].text', round(10 * exp(-.05), 2))
lv.expect(L15, 'quiz[1].explain.text', round(15.8 - 5.1 - 10 * exp(-.05), 2))
ks = np.linspace(-.5, .5, 21)
cal = [k for k in ks if any(true_iv(100 * exp(.04 * Ts[i + 1] + k), Ts[i + 1]) ** 2 * Ts[i + 1] < true_iv(100 * exp(.04 * Ts[i] + k), Ts[i]) ** 2 * Ts[i] for i in range(4))]
lv._rec(cal == [], 'l15 s8 the generator surface has no calendar failure at the nodes for k in [-0.5, 0.5]', '')

# ---------------- l16 (implied forwards) ----------------
def implied_forward(dT, T):
    w = dT.pivot(index='strike', columns='type', values='mid').dropna(subset=['call', 'put'])
    return float(np.median(w.index + exp(.05 * T) * (w['call'] - w['put'])))
qT = {T: .05 - log(implied_forward(clean[np.isclose(clean['T'], T)], T) / 100) / T for T in Ts}
lv.expect(L16, 'screens[0].widget.answer', len(raw) - len(clean))
lv.expect(L16, 'screens[0].canvas.params.lines[4]', round(100 * exp(.05 - qT[1.0]), 2)); lv.expect(L16, 'screens[0].canvas.params.lines[4]', '{:.2f}%'.format(qT[1.0] * 100))
lv._rec(float(np.median(list(qT.values()))) == qT[.25], 'l16 s4 the three-month q is the median q the pricer panel uses', '')
lv.expect(L16, 'screens[4].widget.options[3].why', 'median')                                          # finding: the pricer panel also changes
c75 = clean[np.isclose(clean['T'], 1 / 12) & (clean.strike == 75) & (clean.type == 'call')].mid.iloc[0]
q1 = qT[Ts[0]]
d1 = (log(100 / 75) + (.05 - q1 + .02) / 12) / (.2 * sqrt(1 / 12))
jump = .2 - (bs(100, 75, .05, .2, 1 / 12, 'call', q1) - c75) / (100 * exp(-q1 / 12) * sqrt(1 / 12) * phi(d1))
lv.expect(L16, 'screens[7].widget.options[0].text', round(jump))                                     # finding: plain Newton jumps to 2819 then divides by zero
lv.expect(L16, 'screens[9].widget.answer', round(.0425 * 64000)); lv.expect(L16, 'screens[9].widget.wrong[1].value', round(.0425 / 64000, 8))
lv.expect(L16, 'screens[9].feedback.byKey.divide', '64{,}000')                                       # finding: no byKey line for "divide"

# ---------------- review-4 ----------------
g6 = greeks(100, 100, .05, .2, .5)
lv.expect(R, 'items[0].prose', round(g6['vega'], 2)); lv.expect(R, 'items[0].widget.answer', round(300 * g6['vega'] / 100 * 2, 2))
lv.expect(R, 'items[0].widget.wrong[0].value', round(300 * g6['vega'] * 2)); lv.expect(R, 'items[0].widget.wrong[1].value', round(300 * g6['vega'] / 100, 2))
for i, x in enumerate((99, 100, 101)):
    lv.expect(R, f'items[1].canvas.params.rows[{i}][1]', round(f(x), 4))
lv.expect(R, 'items[1].widget.answer', round((f(101) - f(99)) / 2, 4))                                     # finding: (11.0967 - 9.8232)/2 rounds to 0.6367
lv.expect(R, 'items[1].feedback.correct', round((f(101) - f(99)) / 2, 4)); lv.expect(R, 'items[1].widget.wrong[0].value', round(round(f(101), 4) - round(f(100), 4), 4))
gam7 = (f(100 + 1e-7) - 2 * f(100) + f(100 - 1e-7)) / 1e-14
lv.expect(R, 'items[2].prose', round(gam7, 2))
lv.expect(R, 'items[2].widget.options[0].text', '10^{-16}')                                         # finding: "agree to about 15 digits" is false
gp = greeks(100, 100, .05, .2, 1, 'put'); tp, ep, ap = explain(100, 100, .05, .2, 1, -3, .02, 1 / 365, 'put')
lv.expect(R, 'items[3].prose', round(gp['theta'], 3)); lv.expect(R, 'items[3].widget.answer', round(ep, 4))
for t in (tp[0], tp[1], tp[2], tp[3]):
    lv.expect(R, 'items[3].widget.accept', round(abs(t), 4))
lv.expect(R, 'items[3].feedback.correct', round(ap, 4)); lv.expect(R, 'items[3].explain.text', round(ap - ep, 4))
lv.expect(R, 'items[3].widget.wrong[1].value', round(ep - tp[3] + gp['theta'], 4))
lv.expect(R, 'items[4].prose', round(greeks(100, 100, .05, .2, .25)['gamma'], 6)); lv.expect(R, 'items[4].widget.options[1].why', round(greeks(100, 100, .05, .2, .25)['gamma'] / g['gamma'], 2))
w = (105 - 95) / 15; ch = w * 12.10 + (1 - w) * 2.90
lv.expect(R, 'items[5].widget.answer', round(9.40 - ch, 4)); lv.expect(R, 'items[5].explain.text', round(2 * (9.40 - ch), 4))
lv.expect(R, 'items[5].widget.wrong[0].value', round(9.40 - (12.10 + 2.90) / 2, 4))
lv.expect(R, 'items[5].widget.wrong[1].value', round(9.40 - ((1 - w) * 12.10 + w * 2.90), 4))       # finding: content has -2.8333
lv.expect(R, 'items[6].widget.options[0].text', round(.25 ** 2 / 12, 5)); lv.expect(R, 'items[6].widget.options[0].text', round(.17 ** 2 / 6, 5))
lv.expect(R, 'items[7].widget.answer', round(.031 * 58000))

# ---------------- homework-4 ----------------
lv.expect(H, 'items[1].canvas.params.lines[1]', '{:.6f}'.format(van)[:9]); lv.expect(H, 'items[1].canvas.params.lines[3]', round(van * .02, 4))
lv.expect(H, 'items[2].explain.text', round(.2 * 100 * sqrt(1 / 365), 2)); lv.expect(H, 'items[2].explain.text', round(be, 2))
lv.expect(H, 'items[2].explain.text', round(cash, 2))                                               # finding: the gap is the interest on the hedge cash
dS = 5; d = -(c3['delta'] + p3['delta']); gm = -(c3['gamma'] + p3['gamma']); th = -(c3['theta'] + p3['theta'])
lv.expect(H, 'items[3].prose', round(d, 4)); lv.expect(H, 'items[3].prose', round(gm, 5)); lv.expect(H, 'items[3].prose', round(th, 2))
lv.expect(H, 'items[3].widget.answer', round(d * dS + .5 * gm * 25 + th / 365, 4))
act = -(bs(105, 100, .05, .2, .25 - 1 / 365) + bs(105, 100, .05, .2, .25 - 1 / 365, 'put') - bs(100, 100, .05, .2, .25) - bs(100, 100, .05, .2, .25, 'put'))
lv.expect(H, 'items[3].feedback.correct', round(act, 4))
lv.expect(H, 'items[3].widget.wrong[0].value', round(d * dS + th / 365, 4)); lv.expect(H, 'items[3].widget.wrong[1].value', round(d * dS - .5 * gm * 25 + th / 365, 4))
lv.expect(H, 'items[4].feedback.byKey.bias', round(sqrt(2) * .033 / .02, 1))
lv.expect(H, 'items[5].widget.answer', round(sqrt(.26 ** 2 * .25 / .5), 4)); lv.expect(H, 'items[5].explain.text', round(.26 ** 2 * .25, 4))
lv.expect(H, 'items[6].widget.model', round(100 * exp(.05 - qT[1.0]), 2))

lv._rec(round(12.10 / 3 + 2 * 2.90 / 3, 4) == 5.9667 and round(9.40 - (12.10 / 3 + 2 * 2.90 / 3), 4) == 3.4333, 'review-4 items[5] swapped weights: 5.9667 and gap 3.4333', '')
h = 1e-7; p3 = [bs(100 + k * h, 100, .05, .2, 1) for k in (-1, 0, 1)]
lv._rec(abs(g['gamma'] * h * h - 1.9e-16) < 1e-17, 'review-4 items[2] true second difference h^2 gamma = 1.9e-16 at h = 1e-7', '')
lv._rec(round(bs(101, 100, .05, .2, 1), 4) == 11.0967 and round(bs(99, 100, .05, .2, 1), 4) == 9.8232 and abs((11.0967 - 9.8232) / 2 - 0.63675) < 1e-9 and abs(.636745 - 0.6367) < 1e-4 and abs((11.0967 - 9.8232) / 2 - g['delta']) < 1.5e-4, 'review-4 items[1] central difference 0.6367, within 0.0001 of 0.6368', '')
lv.check_wrongs()
lv.report()
