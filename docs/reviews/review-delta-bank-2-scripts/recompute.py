#!/usr/bin/env python3
"""Delta read of the two bank part 2 fix passes: every changed key, band, wrong value and stated number, recomputed by the
reader from the item's own prose (formulae written here, not taken from the authors' scripts), with a second route where
one exists (fractions, enumeration, a scan, a simulation, finite differences).
K(id, value) checks the stored answer; W(id, wrong id, value) a wrong value; T(id, text...) that each text is printed
somewhere in the item; S(id, text...) that a number of the item's OLD version is printed nowhere (stale check).
A row marked FINDING is content the review reports; it does not fail the run.
Usage (repo root): <venv>/bin/python docs/reviews/review-delta-bank-2-scripts/recompute.py"""
import glob, json, math, re, sys
from fractions import Fraction as F
from itertools import product

items = {}
for f in sorted(glob.glob('app/content/bank/*.json')):
    for it in json.load(open(f)).get('items', []):
        items[it['id']] = it

def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, list):
        for x in o: yield from strings(x)
    elif isinstance(o, dict):
        for x in o.values(): yield from strings(x)

checks = fails = 0
def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', label)

def K(i, v, tol=5e-7):  # answers are stored to six places
    w = items[i]['widget']
    ok(abs(w['answer'] - float(v)) <= max(tol, 1e-9), f'{i}: key {w["answer"]} against {float(v)}')
    band = w['tol'].get('abs', 0)
    ok(abs(w['answer'] - float(v)) <= band + 1e-12, f'{i}: exact value inside the band')

def W(i, wid, v, places=None):
    x = next((x for x in items[i]['widget'].get('wrong', []) if x['id'] == wid), None)
    ok(x is not None, f'{i}: wrong id {wid} present')
    if x is None: return
    v = float(v)
    ok(abs(x['value'] - v) <= x['tol'].get('abs', 0) + 1e-12, f'{i}: slip {wid} unrounded {v} inside the band of {x["value"]}')
    if places is not None:
        ok(abs(round(v, places) - x['value']) < 1e-9, f'{i}: slip {wid} stored as {x["value"]}, {v} to {places} places')

def text(i): return ' | '.join(strings(items[i]))
def T(i, *subs):
    t = text(i)
    for s in subs: ok(s in t, f'{i}: expected to print "{s}"')
def S(i, *subs):
    t = text(i)
    for s in subs: ok(re.search(s, t) is None, f'{i}: stale text matching /{s}/')
def option(i): return next(o['text'] for o in items[i]['widget']['options'] if o.get('correct'))

Phi = lambda z: 0.5 * math.erfc(-z / math.sqrt(2))
phi = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)

# ================= statistics =================
# es-bayes-seven-in-ten: Beta(3, 1) prior, 7 of 10
post = F(3 + 7, 3 + 1 + 10)
grid = [(k + 0.5) / 200000 for k in range(200000)]
num = sum(p * p ** 9 * (1 - p) ** 3 for p in grid); den = sum(p ** 9 * (1 - p) ** 3 for p in grid)
ok(abs(num / den - float(post)) < 1e-6, 'bayes: midpoint integral of the posterior mean')
K('es-bayes-seven-in-ten', post); W('es-bayes-seven-in-ten', 'no-prior', F(7, 10)); W('es-bayes-seven-in-ten', 'one-each', F(8, 12), 4)
T('es-bayes-seven-in-ten', '5/7', '0.7143', 'Beta(10, 4)', '10/14'); S('es-bayes-seven-in-ten', r'Beta\(2, 2\)', r'9/14', r'0\.6429', 'heads', 'coin')

# rg-inference-overall-f: k = 4, n = 65, R^2 = 0.2
Fst = (F(1, 5) / 4) / (F(4, 5) / (65 - 4 - 1))
K('rg-inference-overall-f', Fst); ok(Fst == F(15, 4), 'F is 15/4')
W('rg-inference-overall-f', 'df-61', (0.2 / 4) / (0.8 / 61), 2); W('rg-inference-overall-f', 'no-df', 0.2 / 0.8, 2)
T('rg-inference-overall-f', '15/4', '0.013333', '65 - 4 - 1 = 60'); ok(abs(0.8 / 60 - 0.013333) < 5e-7, '0.8/60 = 0.013333')
S('rg-inference-overall-f', r'5\.71', r'\b44\b', r'0\.3\b')

# ts-acf-noise-band: n = 625
K('ts-acf-noise-band', 1.96 / math.sqrt(625)); W('ts-acf-noise-band', 'no-multiplier', 1 / 25, 4); W('ts-acf-noise-band', 'divided-by-n', 1.96 / 625, 4); W('ts-acf-noise-band', 'rule-of-two', 2 / 25, 4)
T('ts-acf-noise-band', '1.96/25 = 0.0784', '= 0.04'); S('ts-acf-noise-band', r'0\.098', r'\b400\b')

# rg-inference-t-from-r-squared: n = 27, R^2 = 0.2
t2 = F(1, 5) * 25 / F(4, 5)
K('rg-inference-t-from-r-squared', math.sqrt(t2)); ok(t2 == F(25, 4), 't squared is 6.25')
W('rg-inference-t-from-r-squared', 'no-one-minus', math.sqrt(0.2 * 25), 2); W('rg-inference-t-from-r-squared', 'used-n', math.sqrt(0.2 * 27 / 0.8), 2); W('rg-inference-t-from-r-squared', 'no-root', 6.25, 2)
# second route: r = sqrt(0.2), t = r sqrt(n-2)/sqrt(1-r^2)
ok(abs(math.sqrt(0.2) * 5 / math.sqrt(0.8) - 2.5) < 1e-12, 't by the correlation form')
T('rg-inference-t-from-r-squared', '0.2 \\times 25 / 0.8 = 6.25', 'The slope is positive'); S('rg-inference-t-from-r-squared', r'\b102\b', r'5\.05', r'4\.47')

# collinear-features-inflation-factor: r = 0.6
K('collinear-features-inflation-factor', 1 / (1 - F(3, 5) ** 2)); W('collinear-features-inflation-factor', 'one-minus-r', 1 / (1 - 0.6), 2); W('collinear-features-inflation-factor', 'standard-error-factor', math.sqrt(1 / 0.64), 2)
T('collinear-features-inflation-factor', '1/0.64', '0.36'); S('collinear-features-inflation-factor', r'5\.26', r'0\.81', r'0\.9\b')

# measurement-error-noisy-regressor: slope 1.4, var 7, noise 3
K('measurement-error-noisy-regressor', F(14, 10) * F(7, 10)); W('measurement-error-noisy-regressor', 'no-attenuation', 1.4); W('measurement-error-noisy-regressor', 'wrong-way', F(14, 10) * F(10, 7))
T('measurement-error-noisy-regressor', '7/(7 + 3) = 0.7', '1.4 \\times 0.7 = 0.98'); S('measurement-error-noisy-regressor', r'0\.75', r'9/\(9')

# sample-size-for-signal-sharpe-years: Sharpe 0.7, t of 3
K('sample-size-for-signal-sharpe-years', (3 / 0.7) ** 2, tol=5e-4); W('sample-size-for-signal-sharpe-years', 'no-square', 3 / 0.7, 1); W('sample-size-for-signal-sharpe-years', 'aimed-at-two', (2 / 0.7) ** 2, 1)
T('sample-size-for-signal-sharpe-years', '18.37', '18.4')

# ht-pvalue-z-two-and-a-half (z = 2.2 now)
p2 = 2 * (1 - Phi(2.2))
ok(option('ht-pvalue-z-two-and-a-half') == 'About 0.028' and abs(p2 - 0.028) < 5e-4, f'p-value {p2:.5f}')
ok(abs((1 - Phi(2.2)) - 0.0139) < 5e-5 and abs((1 - Phi(1.96)) - 0.025) < 5e-5 and 0.01 < p2 < 0.05, 'one tail 0.0139; beyond 1.96 is 0.025; between 1% and 5%')
T('ht-pvalue-z-two-and-a-half', '0.0139', 'About 0.014', 'About 0.025', 'About 0.050'); S('ht-pvalue-z-two-and-a-half', r'2\.5\b', r'0\.012')

# weak-signal-daily-edge: 0.04% a day, sd 1%, 625 days
K('weak-signal-daily-edge', F(4, 100) / (F(1) / 25)); W('weak-signal-daily-edge', 'no-root', 0.04, 2); W('weak-signal-daily-edge', 'annual-sharpe', 0.04 * math.sqrt(252), 2)
ok((2 * 1 / 0.04) ** 2 == 2500, 't of 2 needs 2,500 days'); T('weak-signal-daily-edge', '2,500 days'); S('weak-signal-daily-edge', r'0\.05%', r'\b400\b', r'1,600')

# dl-clt-mean-of-hundred
K('dl-clt-mean-of-hundred', 1 - Phi((5.8 - 5) / (4 / 10)), tol=5e-6); W('dl-clt-mean-of-hundred', 'no-root', 1 - Phi(0.8 / 4), 3); W('dl-clt-mean-of-hundred', 'both-tails', 2 * (1 - Phi(2)))
# ht-errors-sample-for-power
n_exact = ((1.96 + 0.8416) * 10 / 2) ** 2
K('ht-errors-sample-for-power', math.ceil(n_exact)); W('ht-errors-sample-for-power', 'no-power', math.ceil((1.96 * 5) ** 2)); W('ht-errors-sample-for-power', 'one-sided', math.ceil(((1.645 + 0.8416) * 5) ** 2))
W('ht-errors-sample-for-power', 'rounded-down', math.floor(n_exact)); W('ht-errors-sample-for-power', 'two-groups', math.ceil(2 * n_exact))
power = lambda n: Phi(math.sqrt(n) * 0.2 - 1.96) + Phi(-math.sqrt(n) * 0.2 - 1.96)
ok(abs(power(196) - 0.7995) < 5e-5 and power(197) >= 0.80, f'power at 196 is {power(196):.4f}, at 197 {power(197):.4f}')
ok(abs(n_exact - 196.2) < 0.05 and abs(2.8016 * 5 - 14.008) < 1e-9, '196.2 and 14.008'); T('ht-errors-sample-for-power', '196.2', '14.008', '79.95%', '0.7995')
ok(items['ht-errors-sample-for-power']['difficulty'] == 4 and items['shrinkage-mse-best-multiplier']['difficulty'] == 4, 'the two difficulty changes')
# rg-inference-new-observation
K('rg-inference-new-observation', 2 * math.sqrt(1 + 1 / 25), tol=5e-5); W('rg-inference-new-observation', 'added-errors', 2 + 0.4); W('rg-inference-new-observation', 'fitted-mean', 0.4); W('rg-inference-new-observation', 'noise-only', 2)
# es-intervals-poll-margin
K('es-intervals-poll-margin', 100 * 1.96 * math.sqrt(0.6 * 0.4 / 400), tol=5e-4); W('es-intervals-poll-margin', 'used-half', 100 * 1.96 * math.sqrt(0.25 / 400)); W('es-intervals-poll-margin', 'used-half', 100 * 2 * math.sqrt(0.24 / 400))
W('es-intervals-poll-margin', 'no-multiplier', 100 * math.sqrt(0.24 / 400))
# power-one-sided-shift
K('power-one-sided-shift', Phi((4 - 1.645 * 2) / 2), tol=5e-7); ok(abs(Phi(0.355) - 0.6387) < 5e-5, 'Phi(0.355) = 0.6387')
W('power-one-sided-shift', 'miss-rate', 1 - Phi(0.355), 4); W('power-one-sided-shift', 'two-sided', Phi((4 - 3.92) / 2) + Phi((-4 - 3.92) / 2), 3)
# es-intervals-two-desk-gap
se = math.sqrt(4 / 50 + 4 / 50); K('es-intervals-two-desk-gap', 0.8 - 1.96 * se); W('es-intervals-two-desk-gap', 'one-mean', 0.8 - 1.96 * 2 / math.sqrt(50), 3); W('es-intervals-two-desk-gap', 'upper-end', 0.8 + 1.96 * se, 3)
T('es-intervals-two-desk-gap', 'different days', 'independent')
# es-mle-waits-between-trades
gaps = [4, 9, 2, 7, 5, 3]; K('es-mle-waits-between-trades', F(len(gaps), sum(gaps))); W('es-mle-waits-between-trades', 'mean-wait', F(sum(gaps), len(gaps))); W('es-mle-waits-between-trades', 'five-gaps', 5 / 30, 4)
ll = lambda lam: 6 * math.log(lam) - 30 * lam
ok(max(range(1, 1000), key=lambda k: ll(k / 1000)) == 200, 'log-likelihood peaks at 0.2 on a grid')
print('FINDING es-mle-waits-between-trades: "the time between six of your own fills" then six gaps (six fills leave five gaps); the `five-gaps` line says "Six gaps were timed"')
# shrinkage-mse-best-multiplier
mse = lambda c: 3 * c * c + 9 * (c - 1) ** 2
K('shrinkage-mse-best-multiplier', F(9, 12)); ok(min(range(0, 2001), key=lambda k: mse(k / 1000)) == 750 and mse(0.75) == 2.25 and mse(1) == 3, 'grid minimum at 0.75, error 2.25 against 3')

# claims in the text-only items
try:
    import numpy as np
    from scipy import stats
    ok(abs((stats.t.cdf(1, 47) - stats.t.cdf(-1, 47)) - 2 / 3) < 0.02, 'P(|t| < 1) on 47 df is about two in three')
    rng = np.random.default_rng(20261112)
    # adjusted R^2 falls exactly when the added coefficient has |t| < 1
    agree = 0
    for rep in range(400):
        n = 50; x = rng.normal(size=n); z = rng.normal(size=n); y = 1 + 0.5 * x + rng.normal(size=n)
        def fit(X):
            b, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X @ b; return b, r @ r, X
        X1 = np.column_stack([np.ones(n), x]); X2 = np.column_stack([np.ones(n), x, z])
        _, s1, _ = fit(X1); b2, s2, _ = fit(X2)
        tss = ((y - y.mean()) ** 2).sum()
        adj1 = 1 - (s1 / (n - 2)) / (tss / (n - 1)); adj2 = 1 - (s2 / (n - 3)) / (tss / (n - 1))
        tz = b2[2] / math.sqrt(s2 / (n - 3) * np.linalg.inv(X2.T @ X2)[2, 2])
        agree += (adj2 < adj1) == (abs(tz) < 1); ok(s2 <= s1 + 1e-9, 'R^2 cannot fall') if rep < 3 else None
    ok(agree == 400, f'adjusted R^2 falls exactly when |t| < 1 ({agree} of 400)')
    # Frisch-Waugh-Lovell, and the factor on a cleaned-y-only slope
    n = 300; x2 = rng.normal(size=n); x1 = 0.7 * x2 + rng.normal(size=n); y = 2 * x1 - x2 + rng.normal(size=n)
    one = np.ones(n)
    res = lambda v, u: v - np.column_stack([one, u]) @ np.linalg.lstsq(np.column_stack([one, u]), v, rcond=None)[0]
    slope = lambda v, u: np.linalg.lstsq(np.column_stack([one, u]), v, rcond=None)[0][1]
    full = np.linalg.lstsq(np.column_stack([one, x1, x2]), y, rcond=None)[0][1]
    ok(abs(slope(res(y, x2), res(x1, x2)) - full) < 1e-9, 'partial-out: residual on residual equals the full coefficient')
    r12 = np.corrcoef(x1, x2)[0, 1]
    ok(abs(slope(res(y, x2), x1) - full * (1 - r12 ** 2)) < 1e-9, 'partial-out: cleaned y on raw x1 is the full slope times one minus r squared')
    # two independent walks, 500 steps
    rej = rejd = 0; R = 4000
    for _ in range(R):
        a = rng.normal(size=500).cumsum(); b = rng.normal(size=500).cumsum()
        def tstat(u, v):
            X = np.column_stack([np.ones(len(u)), u]); bb = np.linalg.lstsq(X, v, rcond=None)[0]; r = v - X @ bb
            return bb[1] / math.sqrt(r @ r / (len(u) - 2) * np.linalg.inv(X.T @ X)[1, 1])
        rej += abs(tstat(a, b)) > 1.96; rejd += abs(tstat(np.diff(a), np.diff(b))) > 1.96
    ok(0.86 < rej / R < 0.92, f'two walks: share beyond 1.96 is {rej / R:.3f} ("about nine in ten")')
    ok(0.035 < rejd / R < 0.065, f'differenced: {rejd / R:.3f} ("about one in twenty")')
    print(f'   two walks, 500 steps, {R} pairs: |t| > 1.96 in {rej / R:.3f}; after differencing {rejd / R:.3f}; adjusted R^2 fell exactly when |t| < 1 in {agree} of 400 fits')
    # fanning residuals: slope unbiased, usual error wrong
    est = []; se_usual = []
    for _ in range(2000):
        x = rng.uniform(0, 10, 100); y = 1 + 0.5 * x + rng.normal(size=100) * (0.2 + 0.4 * x)
        X = np.column_stack([np.ones(100), x]); bb = np.linalg.lstsq(X, y, rcond=None)[0]; r = y - X @ bb
        est.append(bb[1]); se_usual.append(math.sqrt(r @ r / 98 * np.linalg.inv(X.T @ X)[1, 1]))
    ok(abs(np.mean(est) - 0.5) < 0.01 and np.mean(se_usual) < 0.95 * np.std(est), f'fanning: mean slope {np.mean(est):.3f}, usual se {np.mean(se_usual):.4f} against true spread {np.std(est):.4f}')
    print(f'   fanning noise: mean slope {np.mean(est):.3f} (true 0.5), usual standard error {np.mean(se_usual):.4f} against a true spread of {np.std(est):.4f}')
except ImportError:
    print('numpy or scipy missing: the four simulation checks were skipped')

# behavioural numbers
ok(15 + 8 == 23 and abs(23 / 5 + 3 - 7.6) < 1e-12 and 7.6 <= 8, 'chose-to-stop: 23 working days sunk; 7.6 of 8 weeks')
T('star-story-chose-to-stop', 'eight weeks', 'about 23 working days', 'another eight days', 'last three weeks'); S('star-story-chose-to-stop', 'six weeks', 'eleven days')
se83 = math.sqrt(0.83 * 0.17 / 400)
ok(abs(se83 - 0.0188) < 5e-5 and 84 - 80 == 4 and 91 - 80 == 11 and abs((0.83 - 0.80) / 0.02 - 1.5) < 1e-9, f'too-good: se {se83:.4f}, edge 4 not 11, 3 points over "about 2" is 1.5')
print(f'   too-good: with the unrounded standard error the edge is {(0.83 - 0.80) / se83:.2f} standard errors')
for i in ('star-story-chose-to-stop', 'project-account-too-good-to-be-true', 'after-rejection-applied-before', 'why-us-a-first-year-day', 'project-account-decision-to-redo', 'final-round-questions-for-us', 'star-story-unpopular-decision'):
    w = items[i]['widget']; n = len(w['model'].split())
    ok([r['points'] for r in w['rubric']] == [2, 2, 2, 2, 1, 1], f'{i}: rubric 2, 2, 2, 2, 1, 1')
    ok(120 <= n <= 180, f'{i}: model of {n} words (brief: 120 to 180)')
ok(items['project-account-too-good-to-be-true']['pace'] == 150, 'too-good pace 150')
# no run of eight words shared between any two of the 62 behavioural models
beh = {i: re.findall(r"[a-z0-9']+", it['widget']['model'].lower()) for i, it in items.items() if it.get('widget', {}).get('kind') == 'longform'}
seen = {}; shared = set()
for i, ws in beh.items():
    for k in range(len(ws) - 7):
        g = ' '.join(ws[k:k + 8])
        if g in seen and seen[g] != i: shared.add((seen[g], i, g))
        seen.setdefault(g, i)
ok(len(beh) == 62 and not shared, f'{len(beh)} behavioural models, shared runs of eight words: {sorted(shared)[:3]}')

# ================= finance =================
# op-parity-price-the-put
pv = 84 * math.exp(-0.06 * 0.25); put = 4.10 - 80 + pv
K('op-parity-price-the-put', put, tol=5e-5); W('op-parity-price-the-put', 'undiscounted', 4.10 - 80 + 84, 2); W('op-parity-price-the-put', 'signs-swapped', 4.10 + 80 - pv, 2)
ok(abs(pv - 82.75) < 5e-3 and put > pv - 80 > 0 and 4.10 > max(80 - pv, 0), 'discounted strike 82.75; both prices inside the no-arbitrage bounds')
# second route: Black-Scholes at the vol implied by the call
def bs(S, Kk, r, T_, v, call=True):
    d1 = (math.log(S / Kk) + (r + v * v / 2) * T_) / (v * math.sqrt(T_)); d2 = d1 - v * math.sqrt(T_)
    c = S * Phi(d1) - Kk * math.exp(-r * T_) * Phi(d2)
    return c if call else c - S + Kk * math.exp(-r * T_)
lo, hi = 0.01, 2.0
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if bs(80, 84, 0.06, 0.25, mid) < 4.10 else (lo, mid)
d1 = (math.log(80 / 84) + (0.06 + lo * lo / 2) * 0.25) / (lo * 0.5); d2 = d1 - lo * 0.5
ok(abs((84 * math.exp(-0.015) * Phi(-d2) - 80 * Phi(-d1)) - put) < 1e-6, f'put by its own Black-Scholes formula at the implied vol {lo:.4f}')
print(f'   put {put:.4f} by parity and by Black-Scholes at the implied vol {lo:.4f}')
T('op-parity-price-the-put', '82.75', '6.85'); S('op-parity-price-the-put', r'50\.97', r'\b52\b', r'4\.07')
# fi-forwards-currency-forward
fwd = F(86, 100) * F(1045, 1000) / F(102, 100)
K('fi-forwards-currency-forward', fwd, tol=5e-7); W('fi-forwards-currency-forward', 'rates-swapped', 0.86 * 1.02 / 1.045, 4); W('fi-forwards-currency-forward', 'added-gap', 0.86 * 1.025, 4)
ok(F(86, 100) * F(1045, 1000) == F(8987, 10000), '0.86 x 1.045 = 0.8987 exactly'); T('fi-forwards-currency-forward', '0.8987', '0.8811', '2.5% gap'); S('fi-forwards-currency-forward', r'1\.25', r'1\.27', 'dollar')
# ms-costs-shortfall-with-unfilled
paper = 8000 * (12.70 - 12.50); real = 5000 * (12.70 - 12.54) - 25
K('ms-costs-shortfall-with-unfilled', 5000 * 0.04 + 3000 * 0.20 + 25); ok(abs(paper - real - 825) < 1e-6, 'paper less real is 825')
W('ms-costs-shortfall-with-unfilled', 'filled-only', 5000 * 0.04 + 25); W('ms-costs-shortfall-with-unfilled', 'no-commission', 800); W('ms-costs-shortfall-with-unfilled', 'filled-cost', 5000 * 0.04)
S('ms-costs-shortfall-with-unfilled', r'1,?190', r'25\.0', r'\b360\b')
ok(items['ms-costs-shortfall-with-unfilled'].get('requires') == ['micro/l6-impact'], 'shortfall requires micro/l6-impact')
# op-strategies-bull-spread-breakeven: scan of the payoff
pl = lambda s: max(s - 40, 0) - max(s - 50, 0) - 7 + 3
be = [s / 100 for s in range(0, 10001) if abs(pl(s / 100)) < 1e-9]
K('op-strategies-bull-spread-breakeven', 40 + 7 - 3); ok(be == [44.0], f'break-even by a scan: {be}'); W('op-strategies-bull-spread-breakeven', 'one-premium', 47); W('op-strategies-bull-spread-breakeven', 'both-premiums', 50)
S('op-strategies-bull-spread-breakeven', r'\b104\b', r'\b110\b')
# op-payoff-short-strangle-loss
K('op-payoff-short-strangle-loss', 3.20 + 2.80 - max(90 - 81, 0) - max(81 - 110, 0)); W('op-payoff-short-strangle-loss', 'no-premium', -9); W('op-payoff-short-strangle-loss', 'premium-only', 6)
S('op-payoff-short-strangle-loss', r'2\.20', r'\b95\b', r'\b105\b')
# op-strategies-butterfly-best-case
cost = 13.00 - 2 * 6.50 + 2.00; pay = lambda s: max(s - 70, 0) - 2 * max(s - 80, 0) + max(s - 90, 0)
best = max(pay(s / 10) for s in range(0, 2001))
K('op-strategies-butterfly-best-case', best - cost); ok(cost == 2 and best == 10 and 13.0 > 6.5 > 2.0 and 13.0 - 6.5 < 10 and 6.5 - 2.0 < 10, 'cost 2, peak payoff 10, prices inside the no-arbitrage bounds')
W('op-strategies-butterfly-best-case', 'ignored-cost', 10); W('op-strategies-butterfly-best-case', 'gave-cost', 2)
# greek-signs-calendar-spread: long 1 month, short 6 months, at the money, r = 0, spot 100, vol 20%
def greeks(T_):
    d1 = 0.5 * 0.2 * math.sqrt(T_)
    return phi(d1) / (100 * 0.2 * math.sqrt(T_)), 100 * phi(d1) * math.sqrt(T_), -100 * phi(d1) * 0.2 / (2 * math.sqrt(T_))
net = [a - b for a, b in zip(greeks(1 / 12), greeks(0.5))]
ok(option('greek-signs-calendar-spread') == 'Positive gamma, negative vega, negative theta' and net[0] > 0 > net[1] and net[2] < 0, f'calendar signs {net}')
ok(abs(net[0] - 0.0409) < 5e-5 and abs(net[1] + 16.63) < 5e-3 and abs(net[2] + 8.19) < 5e-3, 'calendar: +0.0409, -16.63, -8.19')
h = 1e-3; price = lambda S, v, T_: bs(S, 100, 0.0, T_, v)
fd_g = sum(sg * (price(100 + h * 100, 0.2, T_) - 2 * price(100, 0.2, T_) + price(100 - h * 100, 0.2, T_)) / (h * 100) ** 2 for sg, T_ in ((1, 1 / 12), (-1, 0.5)))
fd_v = sum(sg * (price(100, 0.2 + h, T_) - price(100, 0.2 - h, T_)) / (2 * h) for sg, T_ in ((1, 1 / 12), (-1, 0.5)))
fd_t = sum(sg * -(price(100, 0.2, T_ + 1e-5) - price(100, 0.2, T_ - 1e-5)) / 2e-5 for sg, T_ in ((1, 1 / 12), (-1, 0.5)))
ok(abs(fd_g - net[0]) < 1e-4 and abs(fd_v - net[1]) < 1e-2 and abs(fd_t - net[2]) < 1e-2, 'calendar: finite differences agree')
# ms-book-weighted-mid
wm = lambda A: (F(9998, 100) * A + F(10002, 100) * 900) / (900 + A)
ok([A for A in range(1, 5000) if wm(A) == 100] == [900], 'weighted mid is 100.00 only when the offer holds 900'); K('ms-book-weighted-mid', 900 - 100)
W('ms-book-weighted-mid', 'size-wanted', 900); W('ms-book-weighted-mid', 'size-now', 100); T('ms-book-weighted-mid', '0.02A = 18'); S('ms-book-weighted-mid', r'100\.016', 'next trade')
# the three loss items
K('fi-forwards-futures-daily-loss', (4000 - 3960) * 50 * 10); W('fi-forwards-futures-daily-loss', 'signed', -20000); W('fi-forwards-futures-daily-loss', 'one-contract', 2000); W('fi-forwards-futures-daily-loss', 'points-times-contracts', 400)
K('fi-bonds-pound-per-basis-point', 0.98 * 10_000_000 * 4.5 * 0.0001); W('fi-bonds-pound-per-basis-point', 'signed', -4410); W('fi-bonds-pound-per-basis-point', 'face-not-price', 4500); W('fi-bonds-pound-per-basis-point', 'ten-basis-points', 44100)
K('op-strategies-protective-put-floor', max(120 + 3 - (s + max(110 - s, 0)) for s in range(0, 400))); W('op-strategies-protective-put-floor', 'signed', -13); W('op-strategies-protective-put-floor', 'no-premium', 10); W('op-strategies-protective-put-floor', 'took-off-premium', 7)
for i in ('fi-forwards-futures-daily-loss', 'fi-bonds-pound-per-basis-point', 'op-strategies-protective-put-floor'):
    ok(items[i]['question'].endswith('Give the size of the loss as a positive number.'), f'{i}: the question states the sign')
    ok('minus sign' in items[i]['feedback']['byKey']['signed'], f'{i}: signed line')
# the step-short lines
vega = 100 * phi(0.5 * 0.2 * 0.5) * 0.5
K('tp-bs-vega-rule', vega / 100, tol=5e-5); W('tp-bs-vega-rule', 'per-unit-vol', vega); W('tp-bs-vega-rule', 'no-time', 100 * 0.4 / 100); W('tp-bs-vega-rule', 'used-t', 100 * 0.4 * 0.25 / 100)
ok(abs((bs(100, 100, 0, 0.25, 0.205) - bs(100, 100, 0, 0.25, 0.195)) - vega / 100) < 1e-5, 'vega per point by a finite difference')
K('gv-risk-one-day-var', 3_000_000 * 0.012 * 2.326); W('gv-risk-one-day-var', 'one-sd', 36000); W('gv-risk-one-day-var', 'used-1-645', 36000 * 1.645); W('gv-risk-one-day-var', 'ten-day', 83736 * math.sqrt(10))
K('fi-forwards-rich-forward', 205 - (200 * 1.03 - 4)); W('fi-forwards-rich-forward', 'fair-value', 202); W('fi-forwards-rich-forward', 'no-dividend', 205 - 206); W('fi-forwards-rich-forward', 'dividend-twice', 205 - (206 - 8))
ok(205 + 4 - 206 == 3, 'rich forward: cash at delivery')
K('op-greeks-second-order-estimate', 4 + 0.45 * 2 + 0.5 * 0.05 * 4); W('op-greeks-second-order-estimate', 'change-only', 1); W('op-greeks-second-order-estimate', 'delta-only', 4.9); W('op-greeks-second-order-estimate', 'no-half', 5.1)
buys = [(10.30, 300), (10.20, 200), (10.10, 400)]; sells = [(10.00, 250), (10.10, 300), (10.20, 300)]
vol = {p: min(sum(q for b, q in buys if b >= p - 1e-9), sum(q for s, q in sells if s <= p + 1e-9)) for p in (10.00, 10.10, 10.20, 10.30)}
K('ms-book-opening-auction', max(vol.values())); ok(vol == {10.0: 250, 10.1: 550, 10.2: 500, 10.3: 300}, f'auction volumes {vol}')
W('ms-book-opening-auction', 'gave-price', 10.10); W('ms-book-opening-auction', 'cleared-high', 500); W('ms-book-opening-auction', 'all-sells', 850)
S('ms-book-opening-auction', r'£10\.\d(?!\d)')
K('ms-mm-spread-less-drift', 1000 * (1 - 0.4) / 100); W('ms-mm-spread-less-drift', 'in-pence', 600); W('ms-mm-spread-less-drift', 'ignored-move', 10); W('ms-mm-spread-less-drift', 'added-move', 14)
K('op-parity-implied-forward', 100 + (7.20 - 5.10) / 0.98, tol=5e-5); W('op-parity-implied-forward', 'gap-only', 2.10 / 0.98, 2); W('op-parity-implied-forward', 'not-compounded', 102.10); W('op-parity-implied-forward', 'gave-spot', 2.10 + 98)
q = F(1 - F(8, 10), F(125, 100) - F(8, 10)); tree = sum(q ** u * (1 - q) ** (2 - u) * max(40 * F(125, 100) ** u * F(8, 10) ** (2 - u) - 40, 0) * math.comb(2, u) for u in range(3))
K('tp-multistep-two-step-call', tree, tol=5e-5); ok(q == F(4, 9) and tree == F(40, 9), 'q = 4/9, price 40/9')
W('tp-multistep-two-step-call', 'top-payoff', 22.5); W('tp-multistep-two-step-call', 'q-once', float(q) * 22.5); W('tp-multistep-two-step-call', 'even-chances', 22.5 / 4)
left = 450; fills = {}
for name, size in (('C', 100), ('A', 200), ('B', 300)):
    fills[name] = min(size, left); left -= fills[name]
K('ms-book-who-gets-filled', fills['B']); W('ms-book-who-gets-filled', 'left-after-c', 450 - 100); W('ms-book-who-gets-filled', 'time-first', 450 - 200); W('ms-book-who-gets-filled', 'filled-in-full', 300)
# the stop item
st = items['ms-orders-stop-through-a-gap']
ok(st['difficulty'] == 3 and st.get('requires') == ['micro/l4-market-or-limit'] and st['prose'].endswith('Each order wakes once a trade prints at or below its stop price.'), 'stop item: difficulty 3, requires, trigger sentence')
ok(option('ms-orders-stop-through-a-gap').startswith('The stop sells near £93; the stop-limit rests unfilled'), 'stop item key')
import os
ok(os.path.exists('app/content/courses/micro/l4-market-or-limit.json') and os.path.exists('app/content/courses/micro/l6-impact.json'), 'required lessons exist')
l4 = open('app/content/courses/micro/l4-market-or-limit.json').read()
print(f'   note: micro/l4-market-or-limit mentions "stop-limit" {l4.count("stop-limit")} times and "stop order" or "sell stop" {len(re.findall("stop order|sell stop", l4))} times')

# ================= coding: the four reasoning items =================
ns = {}
exec('def mark(x, seen={}):\n    seen[x] = seen.get(x, 0) + 1\n    return len(seen)\n\ntotal = mark("a") + mark("b") + mark("a")\n', ns)
ok(('def mark(x, seen={}):\n    seen[x] = seen.get(x, 0) + 1\n    return len(seen)\n\ntotal = mark("a") + mark("b") + mark("a")') in items['pf-functions-default-list']['prose'], 'default-list: the code run here is the code shown')
K('pf-functions-default-list', ns['total']); W('pf-functions-default-list', 'fresh-dict', 1 + 1 + 1); W('pf-functions-default-list', 'count-of-x', 1 + 1 + 2)
src = re.search(r'```python\n(.*?)```', items['pf-classes-shared-class-list']['prose'], re.S).group(1)
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf): exec(src, {})
K('pf-classes-shared-class-list', int(buf.getvalue())); W('pf-classes-shared-class-list', 'own-list', 1 + 6); W('pf-classes-shared-class-list', 'shared-cap', 2 + 7)
src = re.search(r'```python\n(.*?)```', items['pf-types-round-half-even']['prose'], re.S).group(1)
K('pf-types-round-half-even', eval(src)); ok((int(-3.5), round(-3.5), -9 // 2) == (-3, -4, -5), 'the three terms')
W('pf-types-round-half-even', 'all-towards-zero', -3 + -3 + -4); W('pf-types-round-half-even', 'half-up', -3 + -3 + -5)
away = -3 + -4 + -5  # round half away from zero, the school rule, also gives -4 for -3.5
print(f'FINDING pf-types-round-half-even: the school rule (half away from zero) gives round(-3.5) = -4 too, so its total is {away}, the key')
ok((7 // -2, 7 % -2) == (-4, -1) and (int(7 / -2), 7 - (-2) * int(7 / -2)) == (-3, 1), 'division: Python -4 and -1; towards zero -3 and 1')
ok(option('integer-division-toward-zero') == 'C++: -3 and 1. Python: -4 and -1.', 'division key')
src = re.search(r'```python\n(.*?)```', items['pf-functions-late-binding']['prose'], re.S).group(1); ns = {}; exec(src, ns)
K('pf-functions-late-binding', ns['total'])
ok(items['pf-functions-late-binding'].get('requires') == ['py-found/l14-sorting-by-what-matters'] and items['pf-functions-binom-tail'].get('requires') == ['py-found/l7-arguments', 'conditional/l14-independent-trials'], 'requires of the two coding items')

print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
