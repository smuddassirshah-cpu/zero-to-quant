"""Second reader, bank part 2 (b): independent recompute of every finance key, wrong value and feedback figure.
Written from the item statements, not from the authors' scripts. Exit 0 when every stored value agrees.
Run: python3 docs/reviews/review-bank-2-b-scripts/finance_recompute.py"""
import json, math, os, random, sys
from fractions import Fraction as F

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content', 'bank')
ITEMS = {}
for n in (1, 2, 3, 4):
    for it in json.load(open(os.path.join(ROOT, f'finance-{n}.json')))['items']:
        ITEMS[it['id']] = it
fails = []
checks = 0
seen = set()


def N(x):
    return 0.5 * math.erfc(-x / math.sqrt(2))


def phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def Ninv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        m = (lo + hi) / 2
        if N(m) < p:
            lo = m
        else:
            hi = m
    return lo


def key(iid, value, wrongs=None, places=None):
    """value: my unrounded key. wrongs: {id: my value}. A stored wrong must equal mine rounded as stored."""
    global checks
    it = ITEMS[iid]
    seen.add(iid)
    w = it['widget']
    checks += 1
    tol = (w.get('tol') or {}).get('abs', 0)
    if abs(w['answer'] - value) > max(tol / 10, 1e-6 * max(1, abs(value))) + 1e-12:
        fails.append(f'{iid}: key stored {w["answer"]}, mine {value}')
    stored = {x['id']: x for x in w.get('wrong', [])}
    for k, v in (wrongs or {}).items():
        checks += 1
        if k not in stored:
            fails.append(f'{iid}: no wrong id {k}')
            continue
        st = stored[k]
        t = (st.get('tol') or {}).get('abs', 0)
        if abs(st['value'] - v) > t + 1e-9:
            fails.append(f'{iid}: wrong {k} stored {st["value"]} tol {t}, mine {v}')
    for k in stored:
        if k not in (wrongs or {}):
            fails.append(f'{iid}: wrong id {k} not recomputed')
    # no band touches
    bands = [(w['answer'] - tol, w['answer'] + tol, 'key')] + [(x['value'] - x['tol']['abs'], x['value'] + x['tol']['abs'], x['id']) for x in w.get('wrong', [])]
    for i in range(len(bands)):
        for j in range(i + 1, len(bands)):
            a, b = bands[i], bands[j]
            if a[0] <= b[1] and b[0] <= a[1]:
                fails.append(f'{iid}: bands touch {a[2]} {b[2]}')


def says(iid, text, where=None):
    """the item prints this text somewhere in feedback, accept, why or explain."""
    global checks
    checks += 1
    it = ITEMS[iid]
    blob = json.dumps(it, ensure_ascii=False)
    if text not in blob:
        fails.append(f'{iid}: text not found: {text!r}')


def choice(iid, correct_startswith):
    global checks
    checks += 1
    seen.add(iid)
    opts = ITEMS[iid]['widget']['options']
    c = [o for o in opts if o.get('correct')]
    if len(c) != 1 or not c[0]['text'].startswith(correct_startswith):
        fails.append(f'{iid}: key option is {c[0]["text"] if c else None}, mine starts {correct_startswith!r}')


def close(iid, a, b, tol, what):
    global checks
    checks += 1
    if abs(a - b) > tol:
        fails.append(f'{iid}: {what}: {a} against {b}')


# ---------------- finance-1 ----------------
key('fi-interest-monthly-to-annual', (1 + 0.06 / 12) ** 12 - 1, {'continuous': math.exp(0.06) - 1, 'nominal': 0.06})
close('fi-interest-monthly-to-annual', round(100 * ((1.005) ** 12 - 1), 2), 6.17, 1e-9, 'printed 6.17')
key('fi-bonds-duration-move', -7 * 0.0025, {'sign': 0.0175, 'basis-points': -7 * 0.025})
key('fi-forwards-six-month-fair', 80 * math.exp(0.05 * 0.5), {'simple': 80 * 1.025, 'full-year': 80 * math.exp(0.05)})
# Gordon growth, by the closed form and by summing 3000 terms
g = sum(3 * 1.04 ** (k - 1) / 1.09 ** k for k in range(1, 3000))
close('fi-equity-growing-dividend', g, 60, 1e-6, 'series against 3/(r-g)')
key('fi-equity-growing-dividend', 3 / (0.09 - 0.04), {'no-growth': 3 / 0.09, 'grew-again': 3 * 1.04 / 0.05})
kd = 52 * math.exp(-0.04 * 0.5)
key('op-parity-price-the-put', 3.10 - 50 + kd, {'undiscounted': 3.10 - 50 + 52, 'signs-swapped': 3.10 + 50 - kd})
close('op-parity-price-the-put', round(kd, 2), 50.97, 1e-9, 'printed 50.97')


def spread_pnl(s):
    return max(s - 100, 0) - max(s - 110, 0) - 6 + 2


assert spread_pnl(104) == 0 and spread_pnl(103.99) < 0 < spread_pnl(104.01)
key('op-strategies-bull-spread-breakeven', 104, {'one-premium': 106, 'both-premiums': 108})
key('op-greeks-second-order-estimate', 4 + 0.45 * 2 + 0.5 * 0.05 * 4, {'delta-only': 4.9, 'no-half': 4 + 0.9 + 0.05 * 4})
q = (105 - 90) / (120 - 90)
# replication route: delta shares and a bond
d = (15 - 0) / (120 - 90)
b = (0 - d * 90) / 1.05
close('tp-riskneutral-one-step-with-rate', d * 100 + b, q * 15 / 1.05, 1e-12, 'replication against q')
key('tp-riskneutral-one-step-with-rate', q * 15 / 1.05, {'undiscounted': 7.5, 'zero-rate': (100 - 90) / 30 * 15})


def tree(S, u, dn, R, steps, payoff, american):
    qq = (R - dn) / (u - dn)

    def v(s, k):
        if k == steps:
            return payoff(s)
        cont = (qq * v(s * u, k + 1) + (1 - qq) * v(s * dn, k + 1)) / R
        return max(cont, payoff(s)) if american else cont
    return v(S, 0)


put = lambda s: max(100 - s, 0)
am = tree(100, 1.1, 0.9, 1.05, 2, put, True)
eu = tree(100, 1.1, 0.9, 1.05, 2, put, False)
vu = 0.25 * 1 / 1.05
key('tp-multistep-american-put-two-step', am, {'european': eu, 'root-undiscounted': 0.75 * vu + 0.25 * 10})
close('tp-multistep-american-put-two-step', (0.75 + 0.25 * 19) / 1.05, 5.24, 0.005, 'wait value at 90')
close('tp-multistep-american-put-two-step', vu, 0.238, 0.0005, 'value at 110')
cost = 100 * 10.01 + 200 * 10.02 + 100 * 10.04
close('ms-book-sweep-four-hundred', cost, 4009, 1e-9, 'cost')
key('ms-book-sweep-four-hundred', cost / 400, {'unweighted': (10.01 + 10.02 + 10.04) / 3, 'last-price': 10.04})
mid = (19.98 + 20.02) / 2
key('ms-costs-effective-spread', 2 * (20.01 - mid) / mid * 1e4, {'quoted': 0.04 / mid * 1e4, 'not-doubled': 0.01 / mid * 1e4})
choice('ms-orders-stop-through-a-gap', 'The stop sells near £93; the stop-limit rests')


def bs_greeks(S, K, vol, T):
    d1 = (math.log(S / K) + vol * vol * T / 2) / (vol * math.sqrt(T))
    return dict(delta=N(d1), gamma=phi(d1) / (S * vol * math.sqrt(T)), vega=S * phi(d1) * math.sqrt(T), theta=-S * phi(d1) * vol / (2 * math.sqrt(T)),
                price=S * N(d1) - K * N(d1 - vol * math.sqrt(T)))


def bs_bump(S, K, vol, T):
    """Greeks by finite differences of the price, sharing no formula with bs_greeks beyond the price."""
    p = lambda s, v, t: bs_greeks(s, K, v, t)['price']
    h = 0.01
    return dict(gamma=(p(S + h, vol, T) - 2 * p(S, vol, T) + p(S - h, vol, T)) / h / h, vega=(p(S, vol + 1e-5, T) - p(S, vol - 1e-5, T)) / 2e-5,
                theta=-(p(S, vol, T + 1e-5) - p(S, vol, T - 1e-5)) / 2e-5)


lg, sh = bs_greeks(100, 100, 0.2, 1), bs_greeks(100, 100, 0.2, 0.25)
lb, sb = bs_bump(100, 100, 0.2, 1), bs_bump(100, 100, 0.2, 0.25)
for nm, want in (('gamma', -0.0200), ('vega', 19.77), ('theta', 4.00)):
    close('greek-signs-calendar-spread', lg[nm] - sh[nm], want, 0.006 if nm != 'gamma' else 0.00006, nm)
    close('greek-signs-calendar-spread', lb[nm] - sb[nm], lg[nm] - sh[nm], 1e-3, nm + ' bump')
choice('greek-signs-calendar-spread', 'Negative gamma, positive vega, positive theta')
# the claim "short-dated carry more gamma and theta, long-dated more vega" at the money, for a grid of vols
for vol in (0.1, 0.2, 0.4, 0.8):
    a, c = bs_greeks(100, 100, vol, 1), bs_greeks(100, 100, vol, 0.25)
    assert a['gamma'] < c['gamma'] and a['vega'] > c['vega'] and a['theta'] > c['theta'], vol
v1 = 3_000_000 * 0.012 * 2.326
key('gv-risk-one-day-var', v1, {'used-1-645': 3_000_000 * 0.012 * 1.645, 'ten-day': v1 * math.sqrt(10)})
key('option-estimate-short-dated-call', 0.4 * 150 * 0.32 * 0.25, {'no-root': 0.4 * 150 * 0.32 / 16, 'no-time': 0.4 * 150 * 0.32})
close('option-estimate-short-dated-call', bs_greeks(150, 150, 0.32, 1 / 16)['price'], 4.79, 0.005, 'full Black-Scholes 4.79')

# ---------------- finance-2 ----------------
pv = sum(500 / 1.08 ** k for k in (1, 2, 3))
key('fi-interest-three-payments-pv', pv, {'not-discounted': 1500, 'all-three-years': 1500 / 1.08 ** 3})
for k, s in ((1, 462.96), (2, 428.67), (3, 396.92)):
    close('fi-interest-three-payments-pv', 500 / 1.08 ** k, s, 0.005, f'term {k}')
y = (100 / 78.35) ** 0.2 - 1
key('fi-bonds-zero-coupon-yield', y, {'simple-interest': 21.65 / 78.35 / 5, 'gain-over-five': 21.65 / 5 / 100})
close('fi-bonds-zero-coupon-yield', 1.05 ** 5, 1.27628, 5e-6, '1.05^5')
close('fi-bonds-zero-coupon-yield', 100 / 78.35, 1.27632, 5e-6, '100/78.35')
# arbitrage cash flows at delivery: +205 forward, +4 dividend, -206 loan
key('fi-forwards-rich-forward', 205 + 4 - 200 * 1.03, {'no-dividend': 205 - 206, 'dividend-twice': 205 - (206 - 8)})
key('fi-forwards-futures-daily-loss', (4000 - 3960) * 50 * 10, {'one-contract': 2000, 'points-times-contracts': 400})
key('op-strategies-covered-call-at-fifty', (50 - 40) - max(50 - 45, 0) + 2, {'no-cap': 12, 'no-premium': 5})
bf = lambda s: max(s - 90, 0) - 2 * max(s - 100, 0) + max(s - 110, 0) - (12.5 - 12 + 2.5)
best = max(bf(s / 100) for s in range(5000, 20001))
key('op-strategies-butterfly-best-case', best, {'ignored-cost': 10, 'gave-cost': 3})
worst = min(-4.5 + 100 + max(s / 100 - 95, 0) - s / 100 for s in range(0, 30001))
key('op-parity-call-under-its-floor', worst, {'gave-floor': 5, 'gave-price': 4.5})
key('gamma-pnl-break-even-move', math.sqrt(2 * 0.045 / 0.04), {'no-half': math.sqrt(0.045 / 0.04), 'no-root': 2.25})
d2 = -0.3 * math.sqrt(0.25) / 2
key('digital-option-at-the-money', N(d2), {'one-half': 0.5, 'used-d1': N(-d2)})
close('digital-option-at-the-money', d2, -0.075, 1e-12, 'd2')
q = F(1) - F(4, 5)
q = q / (F(5, 4) - F(4, 5))
assert q == F(4, 9)
c2 = q * q * F(45, 2)
assert c2 == F(40, 9)
close('tp-multistep-two-step-call', tree(40, 1.25, 0.8, 1.0, 2, lambda s: max(s - 40, 0), False), 40 / 9, 1e-12, 'tree against closed form')
key('tp-multistep-two-step-call', 40 / 9, {'even-chances': 0.25 * 22.5, 'q-once': 4 / 9 * 22.5})
key('ms-book-weighted-mid', (99.98 * 100 + 100.02 * 900) / 1000, {'own-side': (99.98 * 900 + 100.02 * 100) / 1000, 'plain-mid': 100})
key('ms-costs-impact-four-times-size', 40 * math.sqrt(16 / 4), {'linear': 160, 'no-change': 40})
key('ms-mm-spread-less-drift', 1000 * (1 - 0.4) / 100, {'ignored-move': 10, 'added-move': 14})
key('gv-risk-two-desks', math.sqrt(1 + 1 + 2 * 0.5), {'added': 2, 'no-correlation': math.sqrt(2)})
choice('exotic-ranking-basket-or-calls', 'The two half calls')
half = bs_greeks(100, 100, 0.25, 1)['price']
close('exotic-ranking-basket-or-calls', half, 9.95, 0.005, 'two half calls 9.95')
rng = random.Random(20261112)
tot = 0.0
tot2 = 0.0
n = 400_000
for _ in range(n // 2):
    z1 = rng.gauss(0, 1)
    z2 = 0.3 * z1 + math.sqrt(1 - 0.09) * rng.gauss(0, 1)
    for s in (1, -1):  # antithetic
        a = 100 * math.exp(-0.03125 + 0.25 * s * z1)
        b2 = 100 * math.exp(-0.03125 + 0.25 * s * z2)
        p = max((a + b2) / 2 - 100, 0)
        tot += p
        tot2 += p * p
        assert 0.5 * max(a - 100, 0) + 0.5 * max(b2 - 100, 0) >= p - 1e-12  # the convexity claim, path by path
basket = tot / n
se = math.sqrt((tot2 / n - basket ** 2) / n)
print(f'basket call by simulation: {basket:.3f} (standard error about {se:.3f}); the item says about 8.05')
close('exotic-ranking-basket-or-calls', basket, 8.05, 0.06, 'basket call 8.05')

# ---------------- finance-3 ----------------
P = 10000 * 0.1 / (1 - 1.1 ** -3)
bal = 10000.0
for _ in range(3):
    bal = bal * 1.1 - P
close('fi-interest-loan-payment', bal, 0, 1e-8, 'balance after three payments')
close('fi-interest-loan-payment', sum(1.1 ** -k for k in (1, 2, 3)), 2.4869, 5e-5, 'annuity factor')
key('fi-interest-loan-payment', P, {'simple-interest': 13000 / 3, 'no-interest': 10000 / 3})
terms = [6 / 1.04, 6 / 1.04 ** 2, 106 / 1.04 ** 3]
for t, s in zip(terms, (5.769, 5.547, 94.234)):
    close('fi-bonds-three-year-coupon', t, s, 0.0005, 'term')
key('fi-bonds-three-year-coupon', sum(terms), {'par': 100, 'not-discounted': 118})
key('fi-bonds-pound-per-basis-point', 10e6 * 0.98 * 4.5 * 1e-4, {'face-not-price': 4500, 'ten-basis-points': 44100})
stake = 200000 * 0.9 - 100000 * 1.04
key('fi-forwards-geared-loss', stake / 100000 - 1, {'no-interest': -0.2, 'no-gearing': -0.1, 'sign': 0.24})
key('fi-forwards-currency-forward', 1.25 * 1.05 / 1.03, {'rates-swapped': 1.25 * 1.03 / 1.05, 'added-gap': 1.25 * 1.02})
key('op-payoff-short-strangle-loss', 2.2 + 1.8 - max(95 - 88, 0) - max(88 - 105, 0), {'no-premium': -7, 'premium-only': 4})
one_two = lambda s: max(s - 100, 0) - 2 * max(s - 110, 0) - 5 + 5
roots = [s / 100 for s in range(11001, 20001) if abs(one_two(s / 100)) < 1e-9]
assert roots == [120.0], roots
key('op-strategies-one-by-two-breakeven', 120, {'peak': 110, 'two-for-one': 115})
key('op-parity-implied-forward', 100 + (7.2 - 5.1) / 0.98, {'not-compounded': 102.1, 'gave-spot': 2.1 + 100 * 0.98})
key('op-greeks-vol-move-pnl', 50 * 100 * 0.12 * 3, {'no-multiplier': 50 * 0.12 * 3, 'one-point': 600, 'one-contract': 36})
key('tp-bs-at-the-money-delta', N(0.2), {'one-half': 0.5, 'used-d2': N(-0.2)})
close('tp-bs-at-the-money-delta', bs_greeks(100, 100, 0.4, 1)['delta'], 0.5793, 5e-5, 'delta 0.5793')
choice('tp-riskneutral-analyst-view', '£12')
qq = (100 - 80) / 50
close('tp-riskneutral-analyst-view', (1 - qq) * 20, 12, 1e-12, 'put')
# replication: short 0.4 share, lend 52
close('tp-riskneutral-analyst-view', -0.4 * 100 + 52, 12, 1e-12, 'replication')
assert abs(-0.4 * 130 + 52) < 1e-12 and abs(-0.4 * 80 + 52 - 20) < 1e-12
key('tp-multistep-monthly-up-factor', math.exp(0.3 * math.sqrt(1 / 12)), {'no-root': math.exp(0.025), 'no-time-step': math.exp(0.3)})
close('tp-multistep-monthly-up-factor', math.sqrt(1 / 12), 0.2887, 5e-5, 'root')
bids = sorted([('A', 200, 50.00, 900), ('B', 300, 50.00, 901), ('C', 100, 50.01, 902)], key=lambda r: (-r[2], r[3]))
left, got = 450, {}
for nm, sz, _, _ in bids:
    got[nm] = min(sz, left)
    left -= got[nm]
key('ms-book-who-gets-filled', got['B'], {'time-first': 250, 'filled-in-full': 300})
paper = 10000 * (25.20 - 25.00)
real = 6000 * (25.20 - 25.06) - 30
key('ms-costs-shortfall-with-unfilled', paper - real, {'filled-only': 390, 'no-commission': 1160})
vg = bs_greeks(100, 100, 0.2, 0.25)['vega'] / 100
key('tp-bs-vega-rule', vg, {'no-time': 0.4, 'used-t': 0.1})
close('tp-bs-vega-rule', vg, 0.1992, 5e-5, 'vega 0.1992')

# ---------------- finance-4 ----------------
key('fi-interest-one-year-forward-rate', 1.04 ** 2 / 1.03 - 1, {'linear': 0.05, 'gap': 0.01})
key('fi-bonds-duration-and-convexity', -8 * 0.01 + 0.5 * 80 * 0.01 ** 2, {'duration-only': -0.08, 'no-half': -0.08 + 0.008, 'sign': 0.076})
# best Sharpe of a mix of two uncorrelated strategies: grid search over the weight, vols 1 and 1 (Sharpe is scale free)
bestS = max((w * 0.6 + (1 - w) * 0.8) / math.sqrt(w * w + (1 - w) ** 2) for w in [i / 10000 for i in range(10001)])
key('fi-equity-combine-two-sharpes', bestS, {'average': 0.7, 'sum': 1.4})
key('fi-forwards-implied-rate', 2 * math.log(1.02), {'simple': 0.04, 'annual-effective': 1.02 ** 2 - 1})
key('digital-option-from-two-calls', (5.9 - 3.7) / 4, {'no-width': 2.2, 'half-width': 1.1})
key('op-strategies-protective-put-floor', max(123 - (s / 10 + max(110 - s / 10, 0)) for s in range(0, 3001)), {'no-premium': 10, 'took-off-premium': 7})
choice('op-parity-exercise-before-dividend', 'Yes')
close('op-parity-exercise-before-dividend', 58 - (50 - 0.30) + 0.50, 8.80, 1e-9, 'held call')
choice('gamma-pnl-hedger-trades', 'Sell more shares')
close('gamma-pnl-hedger-trades', bs_greeks(100, 100, 0.2, 0.25)['delta'], 0.52, 0.005, 'delta at 100')
close('gamma-pnl-hedger-trades', bs_greeks(101, 100, 0.2, 0.25)['delta'], 0.56, 0.005, 'delta at 101')
key('op-greeks-put-delta-from-call', 0.62 - 1, {'sign': 0.38, 'copied-call': -0.62})
paths = [(1.2, 1.2), (1.2, 0.8), (0.8, 1.2), (0.8, 0.8)]
pay = [max(100, 100 * a, 100 * a * b) - 100 for a, b in paths]
assert sorted(round(p, 9) for p in pay) == [0, 0, 20, 44]
key('tp-multistep-lookback-two-step', sum(pay) / 4, {'plain-call': 44 / 4, 'paying-paths': 32})
buys = [(10.3, 300), (10.2, 200), (10.1, 400)]
sells = [(10.0, 250), (10.1, 300), (10.2, 300)]
vol = {p: min(sum(s for bp, s in buys if bp >= p - 1e-9), sum(s for sp, s in sells if sp <= p + 1e-9)) for p in (10.0, 10.1, 10.2, 10.3)}
assert vol == {10.0: 250, 10.1: 550, 10.2: 500, 10.3: 300}, vol
key('ms-book-opening-auction', max(vol.values()), {'cleared-high': 500, 'all-sells': 850})
key('ms-orders-immediate-or-cancel', sum(s for p, s in ((30.03, 400), (30.05, 300), (30.06, 600)) if p <= 30.05 + 1e-9), {'ignored-limit': 1000, 'first-level': 400})
key('ms-costs-participation-time', 60000 / (0.1 * 150000), {'no-rate': 0.4, 'rate-twice': 40})
key('option-estimate-straddle-implied-move', 4 / 0.8 / 50, {'no-factor': 0.08, 'times-factor': 0.064})
x = 2 * Ninv(0.5 + 4 / (4 * 50))  # straddle = 2 S (2 N(x/2) - 1) at the money with zero rates
close('option-estimate-straddle-implied-move', x * 100, 10.03, 0.005, 'Black-Scholes 10.03%')
close('option-estimate-straddle-implied-move', math.sqrt(2 / math.pi), 0.798, 0.0005, 'root 2/pi')
choice('tp-bs-delta-and-finishing-chance', 'Below 30%')
close('tp-bs-delta-and-finishing-chance', N(Ninv(0.30) - 0.25 * math.sqrt(0.5)) * 100, 24.2, 0.05, 'chance 24.2%')

missing = [i for i in ITEMS if i not in seen]
if missing:
    fails.append('not recomputed: ' + ', '.join(missing))
print(f'{len(ITEMS)} items, {checks} checks, {len(fails)} failed')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
