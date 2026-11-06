"""opt-dash level 3 (Implied volatility): second reader's number checks (review-opt-dash-3-4.md).

Every value is recomputed here from first principles: Black-Scholes with a dividend yield, a bisection
implied-vol solver, the course generator make_chain (seed 2320, copied from docs/briefs/opt-dash.md), the
cleaning rules of level 1, and least squares in numpy. Checks that fail on the current content mark a
finding in the review and pass once the fix is pasted: they check the new value only.
"""
import json, os, sys
from math import erf, exp, log, sqrt, pi
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('opt-dash', 3)
L9, L10, L11, L12, R, H = 'l9-', 'l10-', 'l11-', 'l12-', 'review', 'homework'
f4 = '{:.4f}'.format


def N(z): return 0.5 * (1 + erf(z / sqrt(2)))
def phi(z): return exp(-z * z / 2) / sqrt(2 * pi)


def bs(S, K, r, s, T, kind='call', q=0.0):
    d1 = (log(S / K) + (r - q + s * s / 2) * T) / (s * sqrt(T)); d2 = d1 - s * sqrt(T)
    if kind == 'call':
        return S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2)
    return K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1)


def vega(S, K, r, s, T, q=0.0):
    d1 = (log(S / K) + (r - q + s * s / 2) * T) / (s * sqrt(T))
    return S * exp(-q * T) * sqrt(T) * phi(d1)


def iv(P, S, K, r, T, kind='call', q=0.0):
    lo, hi = 1e-6, 10.0
    for _ in range(200):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if bs(S, K, r, m, T, kind, q) > P else (m, hi)
    return (lo + hi) / 2


def safe_solver(P, S, K, r, T, kind, q):
    """The level's bracketed Newton, counting price calls."""
    lo, hi, s, calls, path = 1e-4, 5.0, 0.2, 0, []
    for _ in range(50):
        d = bs(S, K, r, s, T, kind, q) - P; calls += 1; path.append(s)
        if abs(d) < 1e-12:
            break
        lo, hi = (lo, s) if d > 0 else (s, hi)
        new = s - d / vega(S, K, r, s, T, q)
        s = new if lo < new < hi else (lo + hi) / 2
    return s, calls, path


def plain_newton(P, S, K, r, T, kind, q, steps):
    s, out = 0.2, [0.2]
    for _ in range(steps):
        d1 = (log(S / K) + (r - q + s * s / 2) * T) / (s * sqrt(T)); d2 = d1 - s * sqrt(T)
        price = (K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1)) if kind == 'put' else (S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2))
        s = s - (price - P) / (S * exp(-q * T) * sqrt(T) * phi(d1)); out.append(s)
    return out


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


S, r, q = 100.0, 0.05, 0.01
raw = make_chain()
mid_ = (raw.bid + raw.ask) / 2
clean = raw[(raw.bid > 0) & (raw.bid <= raw.ask) & (raw.age_min <= 30) & ((raw.ask - raw.bid) / mid_ < 0.5)].reset_index(drop=True)
clean['mid'] = (clean.bid + clean.ask) / 2


def bounds(kind, K, T):
    if kind == 'call':
        return max(S * exp(-q * T) - K * exp(-r * T), 0), S * exp(-q * T)
    return max(K * exp(-r * T) - S * exp(-q * T), 0), K * exp(-r * T)


clean['iv'] = [iv(p, S, K, r, T, k, q) if bounds(k, K, T)[0] < p < bounds(k, K, T)[1] else float('nan')
               for p, K, T, k in zip(clean.mid, clean.strike, clean['T'], clean.type)]
Ts = sorted(clean['T'].unique())
smiles, fits, atm = {}, {}, {}
for T in Ts:
    F = S * exp((r - q) * T); d = clean[np.isclose(clean['T'], T)]
    o = d[((d.type == 'put') & (d.strike < F)) | ((d.type == 'call') & (d.strike >= F))].sort_values('strike')
    o = o[o.iv.notna()].assign(m=lambda x: np.log(x.strike / F) / sqrt(T))
    smiles[T] = o
    fits[T] = tuple(round(float(c), 4) for c in np.linalg.lstsq(np.column_stack([np.ones(len(o)), o.m, o.m ** 2]), o.iv.values, rcond=None)[0])
    atm[T] = float(np.interp(0.0, o.m.values, o.iv.values))


def fit_vol(T, K):
    a, b, c = fits[T]; m = log(K / (S * exp((r - q) * T))) / sqrt(T); return a + b * m + c * m * m


# ---------------- l9 ----------------
star = iv(12, 100, 100, .05, 1)
c0, v0 = bs(100, 100, .05, .2, 1), vega(100, 100, .05, .2, 1)
lv.expect(L9, 'screens[0].explain.text', round(12 - c0, 4))
lv.expect(L9, 'screens[0].explain.text', round(.2 + (12 - c0) / 37.52, 4))
lv.expect(L9, 'screens[0].explain.text', round(star, 4))
lv.expect(L9, 'screens[0].hints[1].text', round(v0, 2))
c5, v5 = bs(100, 100, .05, .05, 1), vega(100, 100, .05, .05, 1)
lv.expect(L9, 'screens[1].widget.answer', round(.05 - (c5 - 12) / v5, 4))
lv.expect(L9, 'screens[1].widget.accept', round(v5, 2))
lv.expect(L9, 'screens[1].explain.text', round((12 - c5) / round(v5, 1), 3))
worst = max(abs(s0 - (bs(100, 100, .05, s0, 1) - 12) / vega(100, 100, .05, s0, 1) - star) for s0 in np.linspace(.2, .6, 81))
lv._rec(worst < 0.006, 'l9 screens[1].explain "within 0.006" for every start 0.2 to 0.6', f'worst {worst:.5f}')
newton = [0.2]
for _ in range(3):
    s = newton[-1]; newton.append(s - (bs(100, 100, .05, s, 1) - 12) / vega(100, 100, .05, s, 1))
lv.expect(L9, 'screens[2].canvas.params.rows[1][1]', round(newton[1], 6))
lv.expect(L9, 'screens[2].canvas.params.rows[1][2]', round(bs(100, 100, .05, newton[1], 1), 6))
lv.expect(L9, 'screens[2].canvas.params.rows[2][1]', round(newton[2], 8))
lv.expect(L9, 'screens[2].canvas.params.rows[3][1]', round(newton[3], 10))
lv.expect(L9, 'screens[2].canvas.params.rows[1][4]', '1.7 × 10⁻⁴'); lv._rec(abs(newton[1] - star - 1.7e-4) < 5e-6, 'l9 Newton error after one step 1.7e-4', '')
lv._rec(abs(newton[2] - star - 1.8e-9) < 1e-10, 'l9 Newton error after two steps 1.8e-9', f'{newton[2] - star:.2e}')
halvings = next(n for n in range(100) if (5 - 1e-4) / 2 ** n < 1e-12)
lv.expect(L9, 'screens[0].prose', halvings)
Sq, Kr = 100 * exp(-.01 * .25), 100 * exp(-.05 * .25)
lv.expect(L9, 'screens[3].hints[1].text', round(Sq, 4)); lv.expect(L9, 'screens[3].hints[1].text', round(Kr, 4))
lv.expect(L9, 'screens[3].widget.answer', round(3.545 + Sq - Kr, 4))
lv.expect(L9, 'screens[3].widget.wrong[0].value', round(3.545 + 100 - Kr, 4))
lv.expect(L9, 'screens[3].explain.text', round(iv(3.545, 100, 100, .05, .25, 'put', .01), 4))
lv._rec(round(iv(3.545 + Sq - Kr, 100, 100, .05, .25, 'call', .01), 4) == 0.2032, 'l9 s3 parity call vol 0.2032', '')
lv.expect(L9, 'screens[3].explain.text', round(iv(4.505, 100, 100, .05, .25, 'call', .01), 4))
p75, vg75 = bs(100, 75, .05, .2, 1 / 12, 'put', .01), vega(100, 75, .05, .2, 1 / 12, .01)
lv.expect(L9, 'screens[4].prose', round(.2 - (p75 - .04) / vg75))
lv.expect(L9, 'screens[4].prose', round(vg75, 5)); lv.expect(L9, 'screens[4].prose', round(p75, 7))
s75, calls75, path75 = safe_solver(.04, 100, 75, .05, 1 / 12, 'put', .01)
lv.expect(L9, 'screens[4].explain.text', round(s75, 4)); lv.expect(L9, 'screens[4].explain.text', 'ten price calls')
lv._rec(calls75 == 10 and [round(x, 3) for x in path75[2:5]] == [0.893, 0.626, 0.510], 'l9 s4 path 2.6, 0.893, 0.626, 0.510 in ten calls', str(path75[:5]))
lv.expect(L9, 'screens[5].prose', round(100 * exp(-.01) - 100 * exp(-.05), 2))
lv.expect(L9, 'screens[5].prose', round(100 * exp(-.01), 2))
lv.expect(L9, 'screens[5].feedback.byKey.q3', round(iv(12, 100, 100, .05, 1, 'call', .01) * 100, 1))   # finding: content says 24.1 (the q = 0 vol)
lv.expect(L9, 'screens[5].feedback.byKey.q4', round(iv(60, 100, 100, .05, 1, 'call', .01), 1))
lv.expect(L9, 'screens[5].explain.text', '£3.882')                                                    # finding: £3.88 is 0.2p below the bound
pn = plain_newton(.04, 100, 80, .05, 1 / 12, 'put', .01, 12)
for i, want in enumerate(['8.736', '−4.501', '2.113', '0.719', '0.497'], start=1):
    lv.expect(L9, f'screens[6].canvas.params.rows[{i}][1]', round(pn[i], 3))
s80, calls80, _ = safe_solver(.04, 100, 80, .05, 1 / 12, 'put', .01)
lv.expect(L9, 'screens[6].explain.text', round(s80, 4)); lv.expect(L9, 'screens[6].widget.options[0].text', round(s80, 3))
lv.expect(L9, 'screens[6].explain.text', round(bs(100, 80, .05, .497, 1 / 12, 'put', .01), 2))
lv._rec(abs(pn[-1] - s80) < 1e-9, 'l9 s6 "more steps happen to land here": plain Newton reaches 0.3511 by step 12', '')
lv.expect(L9, 'screens[9].canvas.params.rows[1][5]', round(clean[(np.isclose(clean['T'], 1 / 12)) & (clean.strike == 100) & (clean.type == 'call')].iv.iloc[0], 4))
lv.expect(L9, 'screens[9].feedback.correct', int(clean.iv.isna().sum()))
lv.expect(L9, 'screens[9].feedback.correct', len(clean))
row70 = clean[(np.isclose(clean['T'], 1 / 12)) & (clean.strike == 70) & (clean.type == 'call')].iloc[0]
lv.expect(L9, 'screens[9].explain.text', round(row70.mid, 3)); lv.expect(L9, 'screens[9].explain.text', round(bounds('call', 70, 1 / 12)[0], 3))
lv.expect(L9, 'screens[10].widget.answer', round(2000 * 20 * 43 * 2e-6, 2))
lv.expect(L9, 'screens[10].widget.wrong[0].value', round(2000 * 20 * 8 * 2e-6, 2))
lv.expect(L9, 'screens[10].widget.wrong[1].value', 43 * 2e-6)
lv.expect(L9, 'quiz[0].widget.answer', round(.25 - .9 / 18, 4))
lv.expect(L9, 'quiz[1].feedback.correct', round(iv(3.545, 100, 100, .05, .25, 'call', .01), 3))
lv._rec(abs(iv(3.545, 100, 100, .05, .25, 'put', 0) - iv(3.545, 100, 100, .05, .25, 'put', .01)) < .01, 'l9 quiz[1] dropping q moves the vol under a point', '')
lv.expect(L9, 'quiz[3].prose', round(sqrt(2 * pi) * .12, 3))
lv.expect(L9, 'quiz[3].explain.text', round(100 * exp(.05), 2)); lv.expect(L9, 'quiz[3].explain.text', round((100 * exp(.05) - 100) * exp(-.05), 2))

# ---------------- l10 ----------------
T3 = 0.25; o3 = smiles[T3]
for i, (K, m, v) in enumerate(zip(o3.strike, o3.m, o3.iv)):
    lv.expect(L10, f'screens[7].canvas.params.rows[{i}][1]', round(m, 4))
    lv.expect(L10, f'screens[7].canvas.params.rows[{i}][2]', round(v, 4))
for i, T in enumerate(Ts):
    for j, c in enumerate(fits[T]):
        lv.expect(L10, f'screens[3].canvas.params.rows[{i}][{j + 2}]', c)
    lv.expect(L10, f'screens[3].canvas.params.rows[{i}][1]', len(smiles[T]))
    lv.expect(L10, f'screens[4].canvas.params.rows[{i}][1]', round(true_iv(90, T) - true_iv(110, T), 4))
lv.expect(L10, 'screens[4].widget.answer', round(round(true_iv(90, 1 / 12) - true_iv(110, 1 / 12), 4) / round(true_iv(90, 1) - true_iv(110, 1), 4), 2))
lv.expect(L10, 'screens[4].explain.text', round(sqrt(12), 2))
for T, a, b, c in ((1 / 12, 0.441, 0.187, None), (1.0, 0.266, 0.222, None)):
    lv._rec(round(true_iv(70, T), 3) == a and round(true_iv(100, T), 3) == b, f'l10 s1 IV(70), IV(100) at T={T:.3f}', '')
lv.expect(L10, 'screens[1].widget.options[2].why', round(true_iv(70, 1) - true_iv(130, 1), 2))
lv.expect(L10, 'screens[1].widget.options[2].why', round(true_iv(70, 1 / 12) - true_iv(130, 1 / 12), 2))
res = o3.iv.values - (fits[T3][0] + fits[T3][1] * o3.m.values + fits[T3][2] * o3.m.values ** 2)
lv.expect(L10, 'screens[2].explain.text', round(sqrt(np.mean(res ** 2)) * 100, 2))
mrow = lambda K: o3[o3.strike == K].iloc[0]
band = lambda K: (iv(mrow(K).ask, S, K, r, T3, mrow(K).type, q) - iv(mrow(K).bid, S, K, r, T3, mrow(K).type, q)) * 100
lv.expect(L10, 'screens[6].explain.text', round(band(90), 2)); lv.expect(L10, 'screens[6].explain.text', round(band(80), 2))
lv.expect(L10, 'screens[6].widget.options[2].why', round(band(80), 1))
d3 = clean[np.isclose(clean['T'], T3)]
itm3 = d3[~d3.index.isin(o3.index) & d3.iv.notna()]
lv.expect(L10, 'quiz[3].prose', round(np.mean([abs(v - true_iv(K, T3)) for v, K in zip(itm3.iv, itm3.strike)]) * 100, 1))
lv.expect(L10, 'quiz[3].prose', round(np.mean([abs(v - true_iv(K, T3)) for v, K in zip(o3.iv, o3.strike)]) * 100, 2))
lv.expect(L10, 'screens[7].explain.text', round(S * exp((r - q) * T3), 2))
lv.expect(L10, 'screens[10].prose', round(mrow(90).iv * 100, 2)); lv.expect(L10, 'screens[10].prose', round(mrow(110).iv * 100, 2))
lv.expect(L10, 'quiz[1].widget.answer', round(log(110 / (100 * exp(.01))) / .5, 4))
lv.expect(L10, 'quiz[1].widget.wrong[0].value', round(log(1.1) / .5, 4))
p125 = bs(S, 125, r, true_iv(125, T3), T3, 'put', q)
lv.expect(L10, 'quiz[3].explain.text', round(p125, 2))                                                # finding: content says £23.80
lv.expect(L10, 'quiz[3].explain.text', round(bounds('put', 125, T3)[0], 2))                          # finding: content says £24.63
lv.expect(L10, 'quiz[2].explain.text', 'LinAlgError')                                               # finding: lstsq raises, not NaN
x = np.array([-0.4, -0.2, 0.0, 0.2, 0.4]); y = np.array([.26, .23, .2, .2, .25]); w = np.array([1, 4, 9, 4, 1.])
b_exact = float(np.sum(w * x * y) / np.sum(w * x * x))
t4 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'opt-dash', 'l10-smile.json')))['screens'][8]['widget']['tests'][4]
lv._rec(abs(abs(b_exact * 1e4 - round(b_exact * 1e4)) - 0.5) > 1e-6 or 'tol' in t4, 'l10 s8 test 4: a rounding tie (b = -0.04375) needs a tol', f'b = {b_exact}')   # finding
sw = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'opt-dash', 'l10-smile.json')))['screens'][2]['widget']
rms = lambda b, c: sqrt(np.mean((o3.iv.values - (0.2001 + b * o3.m.values + c * o3.m.values ** 2)) ** 2)) * 100
wst = max(rms(b, c) for b in np.arange(sw['answer']['b'] - sw['tol']['b'], sw['answer']['b'] + sw['tol']['b'] + 1e-9, 0.005)
          for c in np.arange(sw['answer']['c'] - sw['tol']['c'], sw['answer']['c'] + sw['tol']['c'] + 1e-9, 0.01))
lv._rec(wst < 0.5, 'l10 s2 every accepted (b, c) misses by under half a vol point', f'worst {wst:.2f}')              # finding
lv.expect(L10, 'screens[2].feedback.correct', 'half a vol point')

# ---------------- l11 ----------------
for i, T in enumerate(Ts):
    lv.expect(L11, f'screens[7].canvas.params.rows[{i}][1]', round(atm[T], 4))
lv.expect(L11, 'screens[0].widget.answer', round((round(atm[1.0], 4) - round(atm[Ts[0]], 4)) * 100, 2))
pa = lambda T: 0.22 - 0.045 * exp(-T / .3)
lv.expect(L11, 'screens[1].widget.answer', round(sqrt((pa(1) ** 2 - pa(.5) ** 2 * .5) / .5), 4))
lv.expect(L11, 'screens[1].widget.wrong[0].value', round((pa(.5) + pa(1)) / 2, 4))
lv.expect(L11, 'screens[1].explain.text', round(pa(.5) ** 2 * .5, 5)); lv.expect(L11, 'screens[1].explain.text', round(pa(1) ** 2, 4))
lv.expect(L11, 'screens[1].explain.text', round((pa(1) ** 2 - pa(.5) ** 2 * .5) / .5, 4))
fw = [sqrt((atm[Ts[i + 1]] ** 2 * Ts[i + 1] - atm[Ts[i]] ** 2 * Ts[i]) / (Ts[i + 1] - Ts[i])) for i in range(4)]
for v in fw[:3]:
    lv.expect(L11, 'screens[3].prose', round(v * 100, 2))
fv4 = sqrt((0.2196 ** 2 - 0.2123 ** 2 * .5) / .5)
lv.expect(L11, 'screens[3].widget.answer', round(fv4, 4)); lv.expect(L11, 'screens[3].feedback.correct', round(fv4 * 100, 2))
lv.expect(L11, 'screens[3].hints[1].text', round(0.2123 ** 2 * .5, 5)); lv.expect(L11, 'screens[3].hints[1].text', round(0.2196 ** 2, 5))
lv.expect(L11, 'screens[3].explain.text', round(sqrt((pa(1) ** 2 - pa(.5) ** 2 * .5) / .5), 4))
for path, val in (('screens[4].prose', .45 ** 2 / 12), ('screens[4].prose', .35 ** 2 * .25), ('screens[4].prose', .28 ** 2)):
    lv.expect(L11, path, round(val, 6))
lv.expect(L11, 'screens[4].widget.answer', round(sqrt((.35 ** 2 * .25 - .45 ** 2 / 12) / (2 / 12)), 4))
lv.expect(L11, 'screens[4].explain.text', round(sqrt((.0784 - .030625) / .75) * 100, 1))
w1, w2 = .4 ** 2 / 12, .26 ** 2 * 2 / 12
lv.expect(L11, 'screens[5].prose', round(w1, 5)); lv.expect(L11, 'screens[5].prose', round(w2, 5))
lv.expect(L11, 'screens[5].widget.options[1].text', '−{:.0f}%'.format(sqrt((w1 - w2) * 12) * 100))        # finding: content says −35%
lv.expect(L11, 'screens[5].widget.options[2].text', '{:.0f}%'.format((.26 * 2 / 12 - .40 / 12) * 12 * 100))
lv.expect(L11, 'screens[6].widget.options[0].text', '{:.1f}%'.format(sqrt((.04 - .4 ** 2 / 12) / (11 / 12)) * 100))
lv.expect(L11, 'screens[6].widget.options[1].text', '{:.1f}%'.format((.2 - .4 / 12) / (11 / 12) * 100))
lv.expect(L11, 'screens[6].explain.text', round((.04 - .4 ** 2 / 12) / (11 / 12), 5))
ev = (.34 ** 2 - .24 ** 2) * 27 / 365
lv.expect(L11, 'screens[9].canvas.params.rows[0][3]', round(.24 ** 2 * 20 / 365, 6)); lv.expect(L11, 'screens[9].canvas.params.rows[1][3]', round(.34 ** 2 * 27 / 365, 6))
lv.expect(L11, 'screens[9].widget.answer', round(sqrt(ev), 4)); lv.expect(L11, 'screens[9].hints[1].text', round(ev, 5))
lv.expect(L11, 'screens[9].widget.wrong[1].value', round(sqrt(.34 ** 2 * 27 / 365), 4))
lv.expect(L11, 'quiz[1].prose', round(100 * exp(.04), 2))
lv.expect(L11, 'quiz[1].prose', round(true_iv(100, 1), 4)); lv.expect(L11, 'quiz[1].prose', round(true_iv(100 * exp(.04), 1), 4))
lv.expect(L11, 'quiz[1].explain.text', round((true_iv(100, 1) - true_iv(100 * exp(.04), 1)) * 100, 2))
lv.expect(L11, 'quiz[3].widget.answer', round(.2184 ** 2, 4)); lv.expect(L11, 'quiz[3].explain.text', round(.2115 ** 2 * .5, 4))

# ---------------- l12 ----------------
for lab, (K, T) in zip('ABCD', ((76, .18), (125, .12), (75, .9), (100, .5))):
    lv._rec(True, f'l12 point {lab} planted vol {true_iv(K, T):.4f}', '')
lv.expect(L12, 'screens[0].explain.text', round(true_iv(76, .18) * 100, 1)); lv.expect(L12, 'screens[0].explain.text', round(true_iv(75, .9) * 100, 1))
lv.expect(L12, 'screens[0].explain.text', round(true_iv(100, .5) * 100, 1)); lv.expect(L12, 'screens[0].feedback.byKey.B', round(true_iv(125, .12) * 100, 1))
lv.expect(L12, 'screens[1].explain.text', round(true_iv(75, 1 / 12) * 100, 1)); lv.expect(L12, 'screens[1].explain.text', round(true_iv(75, 1) * 100, 1))
lv.expect(L12, 'screens[1].explain.text', round(true_iv(100, 1 / 12) * 100, 1)); lv.expect(L12, 'screens[1].explain.text', round(true_iv(100, 1) * 100, 1))
k = log(100 / (100 * exp(.04 * .75)))
w6 = fit_vol(.5, 100 * exp(.04 * .5) * exp(k)) ** 2 * .5; w12 = fit_vol(1.0, 100 * exp(.04) * exp(k)) ** 2
lv.expect(L12, 'screens[2].canvas.params.rows[0][1]', round(k / sqrt(.5), 4)); lv.expect(L12, 'screens[2].canvas.params.rows[2][1]', round(k / sqrt(.75), 4))
lv.expect(L12, 'screens[2].canvas.params.rows[0][2]', round(sqrt(w6 / .5), 4)); lv.expect(L12, 'screens[2].canvas.params.rows[1][2]', round(sqrt(w12), 4))
lv.expect(L12, 'screens[2].canvas.params.rows[0][3]', round(w6, 5)); lv.expect(L12, 'screens[2].canvas.params.rows[1][3]', round(w12, 5))
w75 = (w6 + w12) / 2
lv.expect(L12, 'screens[2].widget.accept', round(w75, 5)); lv.expect(L12, 'screens[2].widget.answer', round(sqrt(w75 / .75), 3))
lv.expect(L12, 'screens[2].feedback.correct', round(true_iv(100, .75), 4))
lv.expect(L12, 'screens[2].widget.wrong[0].value', round((round(sqrt(w6 / .5), 4) + round(sqrt(w12), 4)) / 2, 5))
lv.expect(L12, 'screens[2].widget.wrong[2].value', round(sqrt(w75), 4))
lv.expect(L12, 'screens[7].canvas.params.lines[2]', sqrt(w75 / .75))
for i, K in enumerate(range(70, 131, 5)):
    lv.expect(L12, f'screens[3].canvas.params.rows[{i}][1]', round((fit_vol(Ts[0], K) - true_iv(K, Ts[0])) * 100, 2))
    lv.expect(L12, f'screens[3].canvas.params.rows[{i}][2]', round((fit_vol(1.0, K) - true_iv(K, 1.0)) * 100, 2) + 0.0)
lv._rec(list(smiles[Ts[0]].strike) == [90, 95, 100, 105], 'l12 s3 the one-month OTM quotes are 90 to 105', '')
lv.expect(L12, 'screens[3].widget.options[0].text', 'out-of-the-money')                                # finding: the one-month 70 call is clean
lv.expect(L12, 'screens[8].explain.text', '110')                                                     # finding: 110 is outside 90 to 105 too
for i, T in enumerate(Ts):
    for j, K in enumerate((80, 90, 100, 110, 120)):
        lv.expect(L12, f'screens[8].canvas.params.rows[{i}][{j + 1}]', round(fit_vol(T, K), 4))
lin6 = .6 - .3 * (.5 - 1 / 12) / (11 / 12)
lv.expect(L12, 'screens[4].prose', round(lin6 * 100, 1)); lv.expect(L12, 'screens[4].widget.options[0].text', round(lin6 ** 2 * .5, 3))
wl6 = .03 + (.5 - 1 / 12) / (11 / 12) * .06
lv.expect(L12, 'screens[4].explain.text', round(wl6, 4)); lv.expect(L12, 'screens[4].explain.text', round(sqrt(wl6 / .5) * 100, 1))
kk = log(100 / (100 * exp(.06)))
lv.expect(L12, 'quiz[0].explain.text', round(fit_vol(1.0, 100 * exp(.04) * exp(kk)), 4))
T2w = .25 + 7 / 365; wk = .199 ** 2 * T2w
lv.expect(L12, 'quiz[1].explain.text', round(wk, 5)); lv.expect(L12, 'quiz[1].explain.text', round(sqrt((wk - .01) / (7 / 365)), 3))
lv.expect(L12, 'quiz[1].widget.options[3].why', round(wk, 4))                                         # finding: content says 0.0104
lv.expect(L12, 'quiz[2].widget.answer', round(log(100 / (100 * exp(.02))) / sqrt(.5), 4)); lv.expect(L12, 'quiz[2].prose', round(100 * exp(.02), 2))
lv.expect(L12, 'quiz[3].widget.answer', round(sqrt((.04 / 12 + .0625 / 4) / 2 / (2 / 12)), 4))

# ---------------- review-3 ----------------
lv.expect(R, 'items[0].widget.answer', round(.3 - .6 / 12, 4)); lv.expect(R, 'items[1].widget.answer', (1e-4 + .2) / 2)
lv.expect(R, 'items[1].widget.wrong[0].value', (1e-4 + 5) / 2)
p120 = clean[(np.isclose(clean['T'], 1 / 12)) & (clean.strike == 120) & (clean.type == 'put')].iloc[0]     # finding 49: a fresh quote
lv._rec(np.isnan(p120.iv), 'review-3 items[2] the one-month 120 put has no vol', '')
lv.expect(R, 'items[2].prose', round(p120.mid, 3)); lv.expect(R, 'items[2].widget.options[0].text', round(bounds('put', 120, 1 / 12)[0], 3))
lv.expect(R, 'items[2].widget.options[3].why', round(120 * exp(-.05 / 12), 2))
lv.expect(R, 'items[2].widget.options[2].why', '{:.0f}%'.format((p120.ask - p120.bid) / p120.mid * 100))
lv.expect(R, 'items[2].feedback.correct', round((bounds('put', 120, 1 / 12)[0] - p120.mid) * 100, 1))
lv.expect(R, 'items[3].widget.answer', round(log(90 / (100 * exp(.02))) / sqrt(.5), 4)); lv.expect(R, 'items[3].widget.wrong[1].value', round(log(.9) / sqrt(.5), 3))
lv.expect(R, 'items[5].widget.answer', round(sqrt((.24 ** 2 * .5 - .22 ** 2 * .25) / .25), 4)); lv.expect(R, 'items[5].widget.wrong[1].value', round((.24 * .5 - .22 * .25) / .25, 2))
lv.expect(R, 'items[6].canvas.params.rows[0][2]', round(.3 ** 2 * 2 / 12, 4)); lv.expect(R, 'items[6].canvas.params.rows[1][2]', round(.24 ** 2 * .25, 4))
lv.expect(R, 'items[7].widget.answer', round(sqrt(.017 / .375), 4)); lv.expect(R, 'items[7].widget.wrong[1].value', round(sqrt(.017), 4))
T2 = Ts[1]                                                                                           # finding 50: a fresh wing
lv._rec(list(smiles[T2].strike)[0] == 85 and list(smiles[T2].strike)[-1] == 115, 'review-3 items[8] two-month quotes run 85 to 115', '')
lv.expect(R, 'items[8].prose', round(fit_vol(T2, 75) * 100, 1)); lv.expect(R, 'items[8].prose', round(true_iv(75, T2) * 100, 1))
lv.expect(R, 'items[8].widget.options[1].text', round(fit_vol(T2, 75) * 100, 1))
lv.expect(R, 'items[8].explain.text', round(abs(fit_vol(T2, 75) - true_iv(75, T2)) * 100, 2))
lv.expect(R, 'items[8].explain.text', round(max(abs(fit_vol(T2, K) - true_iv(K, T2)) for K in range(85, 116, 5)) * 100, 2))

# ---------------- homework-3 ----------------
lv.expect(H, 'items[0].canvas.params.lines[1]', repr(newton[1])); lv.expect(H, 'items[0].canvas.params.lines[1]', repr(newton[2]))
ex = (.45 ** 2 - .3 ** 2) * 14 / 365
lv.expect(H, 'items[3].widget.answer', round(sqrt(ex), 4)); lv.expect(H, 'items[3].explain.text', round(ex, 5)); lv.expect(H, 'items[3].widget.wrong[0].value', round(sqrt(.45 ** 2 * 14 / 365), 4))
lv.expect(H, 'items[4].widget.answer', round(.0596 / sqrt(12), 4)); lv.expect(H, 'items[4].widget.wrong[0].value', round(.0596 / 12, 5))
w3 = .25 / 12 + 2 / 11 * (.0625 - .25 / 12)
lv.expect(H, 'items[5].widget.answer', round(sqrt(w3 / .25), 4)); lv.expect(H, 'items[5].widget.accept', round(w3, 5))
lv.expect(H, 'items[5].widget.wrong[0].value', round(.5 - .25 * 2 / 11, 4)); lv.expect(H, 'items[5].feedback.byKey.vol', round((.5 - .25 * 5 / 11) ** 2 * .5, 4))
lv.expect(H, 'items[6].widget.model', fits[Ts[0]][1]); lv.expect(H, 'items[6].widget.model', fits[1.0][1])
lv.expect(H, 'items[6].widget.model', round((fit_vol(Ts[0], 70) - true_iv(70, Ts[0])) * -100, 2))

lv.check_wrongs()
lv.report()
