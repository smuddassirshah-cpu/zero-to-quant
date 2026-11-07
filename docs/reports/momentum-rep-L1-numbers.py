"""Recompute every number stated in momentum-rep level 1 (The paper) and check each at its JSON path (second read).
Run: python3 docs/reports/momentum-rep-L1-numbers.py   (needs numpy; exits 0 when every check passes)
Data: the course generator `momentum_panel`, verbatim from docs/briefs/momentum-rep.md, base panel seed 2 (500 x 300),
and the small panel momentum_panel(n=200, T=120) for the l5 placebo tests.
Route 1 is the reference form (loop formation returns, double stable argsort, averaged cohort weights).
Route 2 is independent (cumulative log sums, one argsort and a scatter, the composite as the mean of each live
cohort's own spread). `two(a, b)` asserts the routes agree; `lv.expect` checks the stated value at its path.
`lv.claim_text` ties a claim to its wording: it fails while a false sentence is in the text and passes once it is
reworded. Every code widget runs in CPython: the solution passes every hidden test, the starter fails at least one.
Checks that fail on the current content are findings in docs/reviews/review-momentum-rep-1.md.
"""
import sys, os, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("momentum-rep", 1)
E = lv.expect
fails = []


def two(name, a, b, tol=1e-10):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = a.shape == b.shape and np.allclose(a, b, rtol=tol, atol=tol)
    lv.claim(ok, f'two routes agree: {name}', f'{a!r} vs {b!r}')


def J_(fid, path):
    """The raw JSON node at a path, for structural checks."""
    from numbers_lib import _walk
    return _walk(lv._file(fid)[1], path)[0]


def momentum_panel(n=500, T=300, seed=2, c=0.015, e=0.03, d=0.006, nf=4, fsd=0.035,
                   c_after=None, t_pub=300, crash=None):
    TMAX, L = 480, 36
    rng = np.random.default_rng(seed)
    size = rng.normal(0.0, 1.0, n)
    sig = 0.09 - 0.02 * np.tanh(size)
    beta = rng.uniform(0.5, 1.5, n)
    lam = rng.standard_normal((n, nf))
    s = rng.standard_normal((TMAX + L, n))[:T + L] * sig
    m = (0.006 + 0.045 * rng.standard_normal(TMAX))[:T]
    F = (fsd * rng.standard_normal((TMAX, nf)))[:T]
    if crash is not None:
        m[crash - 12:crash] = -0.03; F[crash - 12:crash, 0] = -0.03
        m[crash:crash + 3] = [0.12, 0.06, 0.04]; F[crash:crash + 3, 0] = [0.12, 0.06, 0.04]
    ct = np.full(T, c)
    if c_after is not None:
        ct[t_pub:] = c_after
    cont = sum(s[L - k:L - k + T] for k in range(2, 13))
    rev = sum(s[L - k:L - k + T] for k in range(13, 37))
    idio = s[L:L + T] - e * s[L - 1:L - 1 + T] + ct[:, None] * cont - d * rev
    r = 0.004 + beta * m[:, None] + F @ lam.T + idio
    return r, size, m, F


# ---------- route 1: reference ----------
def f1(r, J, skip=0):
    T, n = r.shape
    f = np.full((T, n), np.nan)
    for t in range(J + skip, T):
        f[t] = np.prod(1 + r[t - skip - J:t - skip], axis=0) - 1
    return f


def dec1(ft, q=10):
    return np.argsort(np.argsort(ft, kind="stable"), kind="stable") * q // len(ft)


def w1(ft, q=10):
    d = dec1(ft, q)
    top, bot = d == q - 1, d == 0
    return np.where(top, 1 / top.sum(), 0.0) - np.where(bot, 1 / bot.sum(), 0.0)


def leg_w1(ft, k, q=10):
    d = dec1(ft, q)
    return (d == k) / (d == k).sum()


def comp1(r, J, K, wfun, skip=0):
    f = f1(r, J, skip)
    W = np.zeros(r.shape)
    for s in range(J + skip, r.shape[0]):
        W[s] = wfun(f[s])
    return np.array([W[t - K + 1:t + 1].mean(axis=0) @ r[t] for t in range(J + skip + K - 1, r.shape[0])])


def wml1(r, J, K, skip=0):
    return comp1(r, J, K, w1, skip)


# ---------- route 2: independent ----------
def f2(r, J, skip=0):
    C = np.vstack([np.zeros((1, r.shape[1])), np.cumsum(np.log1p(r), axis=0)])
    f = np.full(r.shape, np.nan)
    t = np.arange(J + skip, r.shape[0])
    f[t] = np.expm1(C[t - skip] - C[t - skip - J])
    return f


def dec2(ft, q=10):
    n = len(ft)
    rank = np.empty(n, int)
    rank[np.argsort(ft, kind="stable")] = np.arange(n)
    return rank * q // n


def wml2(r, J, K, skip=0, legs=None):
    f = f2(r, J, skip)
    T = r.shape[0]
    spread = {}
    for s in range(J + skip, T):
        d = dec2(f[s])
        if legs is None:
            spread[s] = r[s:s + K, d == 9].mean(axis=1) - r[s:s + K, d == 0].mean(axis=1)
        else:
            spread[s] = r[s:s + K, d == legs].mean(axis=1)
    out = []
    for t in range(J + skip + K - 1, T):
        out.append(np.mean([spread[s][t - s] for s in range(t - K + 1, t + 1)]))
    return np.array(out)


def tstat(x):
    x = np.asarray(x, float)
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x)))


def tstat2(x):
    x = [float(v) for v in x]
    n = len(x); mu = sum(x) / n
    return mu / math.sqrt(sum((v - mu) ** 2 for v in x) / (n - 1) / n)


def shuffle(r, seed):
    rng = np.random.default_rng(seed)
    return np.column_stack([rng.permutation(r[:, j]) for j in range(r.shape[1])])


r, size, mkt, F = momentum_panel()
T, N = r.shape

# ======================= l3 and l4: the J x K table =======================
GRID = {}
for J in (3, 6, 9, 12):
    for K in (3, 6, 9, 12):
        a, b = wml1(r, J, K), wml2(r, J, K)
        two(f'{J}/{K} composite', a, b, 1e-9)
        GRID[J, K] = a
BRIEF = {3: (0.51, 0.60, 0.60, 0.63), 6: (0.91, 0.96, 0.91, 0.77), 9: (1.16, 1.16, 0.96, 0.80), 12: (1.31, 1.12, 0.93, 0.66)}
for i, J in enumerate((3, 6, 9, 12)):
    for j, K in enumerate((3, 6, 9, 12)):
        v = round(100 * GRID[J, K].mean(), 2)
        lv.claim(v == BRIEF[J][j], f'{J}/{K} mean {v} equals the brief')
        for fid, sc in (('l3', 1), ('l3', 7), ('l4', 5)):
            E(fid, f'screens[{sc}].canvas.params.rows[{i}][{j + 1}]', v, fmt='{:.2f}')
x66 = GRID[6, 6]
M66, SD66, N66, T66 = x66.mean(), x66.std(ddof=1), len(x66), tstat(x66)
two('6/6 t', T66, tstat2(x66))
E('l3', 'screens[2].prose', round(100 * M66, 2)); E('l3', 'screens[2].prose', round(100 * SD66, 2)); E('l3', 'screens[2].prose', N66)
E('l3', 'screens[2].hints[1].text', math.sqrt(N66))
t_round = 0.96 / (5.98 / math.sqrt(289))
E('l3', 'screens[2].widget.answer', round(t_round, 2)); E('l3', 'screens[2].hints[2].text', round(5.98 / 17, 3))
E('l3', 'screens[2].explain.text', round(T66, 2)); E('l3', 'screens[2].explain.canvas.points.t.x', round(T66, 2))
E('l3', 'screens[2].widget.wrong[0].value', round(0.96 / 5.98, 4)); E('l3', 'screens[2].widget.wrong[1].value', round(0.96 / 5.98 / 17, 4))
lv.claim(abs(round(T66, 2) - 2.73) <= 0.031, 'l3 screens[2] band accepts the unrounded 2.74')
x1212, x312, x123 = GRID[12, 12], GRID[3, 12], GRID[12, 3]
for fid, path in (('l3', 'screens[3].prose'), ('l3', 'quiz[3].prose'), ('homework', 'items[4].prose')):
    E(fid, path, round(100 * x1212.mean(), 2))
E('l3', 'screens[3].prose', round(tstat(x1212), 2)); E('l3', 'screens[3].prose', round(tstat(x312), 2)); E('l3', 'screens[3].prose', round(100 * x312.mean(), 2))
E('l3', 'screens[3].canvas.state.points[2].x', round(tstat(x1212), 2)); E('l3', 'screens[3].canvas.state.points[3].x', round(tstat(x312), 2))
lv.claim(tstat(x312) > 2.58 and tstat(x1212) < 1.96, 'l3 screens[3] hint: 3/12 past 2.58, 12/12 short of 1.96')
lv.claim(x1212.std(ddof=1) > x312.std(ddof=1), 'l3 screens[3]: 12/12 swings more than 3/12')
E('l4', 'screens[5].prose', round(100 * x123.mean(), 2)); E('l4', 'screens[5].prose', round(tstat(x123), 2))
x912 = GRID[9, 12]
E('review', 'items[5].prose', round(100 * x912.mean(), 2)); E('review', 'items[5].prose', round(100 * x912.std(ddof=1), 2)); E('review', 'items[5].prose', len(x912))
E('review', 'items[5].explain.text', round(math.sqrt(280), 2)); E('review', 'items[5].explain.text', round(5.69 / math.sqrt(280), 3))
E('review', 'items[5].explain.text', round(0.80 / (5.69 / math.sqrt(280)), 2))
E('review', 'items[5].widget.answer', round(0.80 / (5.69 / math.sqrt(280)), 2)); E('review', 'items[5].widget.wrong[0].value', round(0.80 / 5.69, 4))
E('homework', 'items[4].prose', round(100 * x1212.std(ddof=1), 2)); E('homework', 'items[4].prose', len(x1212))
nreq = (1.96 * 6.21 / 0.66) ** 2
E('homework', 'items[4].widget.accept', round(nreq, 1)); E('homework', 'items[4].explain.text', round(1.96 * 6.21 / 0.66, 2))
E('homework', 'items[4].widget.answer', math.ceil(nreq)); E('homework', 'items[4].feedback.correct', math.ceil(nreq) - 277)
E('homework', 'items[4].widget.wrong[0].value', round(277 * 1.96 / 1.77))
nreq2 = (1.96 / tstat(x1212)) ** 2 * len(x1212)
lv.claim(abs(nreq2 - math.ceil(nreq)) <= 1, f'homework items[4]: unrounded inputs need {nreq2:.1f} months, inside the band')

# claim: l3 screens[1] explain "rises as J grows and falls as K grows beyond about 6"
mean = {k: v.mean() for k, v in GRID.items()}
rises_J = all(mean[3, K] < mean[6, K] < mean[9, K] < mean[12, K] for K in (3, 6, 9, 12))
falls_K = all(mean[J, 6] > mean[J, 9] > mean[J, 12] for J in (3, 6, 9, 12))
lv.claim_text('l3', 'screens[1].explain.text', 'The spread rises as J grows and falls as K grows beyond about 6', rises_J and falls_K,
              'l3 screens[1]: "rises as J grows and falls as K grows beyond about 6" holds in every row and column')
lv.claim(max(mean, key=mean.get) == (12, 3) and min(mean, key=mean.get) == (3, 3), 'l3 screens[1]: 12/3 largest, 3/3 smallest')
lv.claim(mean[3, 3] < mean[6, 3] < mean[9, 3] < mean[12, 3] and all(mean[J, 6] > mean[J, 9] > mean[J, 12] for J in (6, 9, 12)),
         'fix value: l3 screens[1] the K = 3 column rises with J; for J of 6 or more the spread falls as K grows past 6')

# l3 layout legs and the ten deciles
for i, J in enumerate((6, 12)):
    for j, K in enumerate((3, 6, 9, 12)):
        s_ = comp1(r, J, K, lambda ft: leg_w1(ft, 0)).mean(); b_ = comp1(r, J, K, lambda ft: leg_w1(ft, 9)).mean()
        two(f'{J}/{K} Sell leg', s_, wml2(r, J, K, legs=0).mean(), 1e-9)
        E('l3', f'screens[0].canvas.params.rows[{3 * i}][{j + 2}]', round(100 * s_, 2), fmt='{:.2f}')
        E('l3', f'screens[0].canvas.params.rows[{3 * i + 1}][{j + 2}]', round(100 * b_, 2), fmt='{:.2f}')
        E('l3', f'screens[0].canvas.params.rows[{3 * i + 2}][{j + 2}]', round(100 * (b_ - s_), 2), fmt='{:.2f}')
        two(f'{J}/{K} Buy - Sell equals the composite', b_ - s_, GRID[J, K].mean(), 1e-9)
DEC = [comp1(r, 6, 6, lambda ft, k=k: leg_w1(ft, k)).mean() for k in range(10)]
two('decile 6 route 2', DEC[5], wml2(r, 6, 6, legs=5).mean(), 1e-9)
for k in range(10):
    E('l3', f'screens[5].canvas.state.values.D{k + 1}', round(100 * DEC[k], 2))
lv.claim(all(DEC[k] < DEC[k + 1] for k in range(9)), 'l3 screens[5]: the ten decile means rise in order')
d1, d10 = round(100 * DEC[0], 2), round(100 * DEC[9], 2)
E('l3', 'screens[5].prose', d1); E('l3', 'screens[5].prose', d10)
E('l3', 'screens[5].widget.options[1].text', round(d1 + d10, 2)); E('l3', 'screens[5].explain.text', round(d10 - d1, 2))
E('l3', 'screens[5].explain.text', round(100 * M66, 2))
lv.claim_text('l3', 'screens[5].hints[2].text', 'about 0.96 after rounding', round(d10 - d1, 2) == 0.96,
              'l3 screens[5] hint: 2.01 - 1.04 is "about 0.96 after rounding"')

# l3 compounding, t from se, costs
for path, m_ in (('screens[4].widget.answer', 0.0095), ('quiz[0].widget.answer', 0.005)):
    a = (1 + m_) ** 12 - 1
    two(f'compound {m_}', a, math.expm1(12 * math.log1p(m_)))
    E('l3', path, round(a, 4))
E('l3', 'screens[4].explain.text', round(12 * 0.95, 2)); E('l3', 'screens[4].explain.canvas.points[0].x', round(12 * 0.95, 2))
E('l3', 'screens[4].widget.wrong[0].value', 0.0095 * 12); E('l3', 'quiz[0].widget.wrong[0].value', 0.06)
E('l3', 'screens[6].widget.options[0].text', 0.80 / 0.40); E('l3', 'screens[6].widget.options[1].text', 0.40 / 0.80)
E('l3', 'screens[6].widget.options[2].text', round(0.80 * 0.40, 2))
E('l3', 'quiz[1].widget.answer', round(1.70 - 1.20, 2)); E('l3', 'quiz[1].widget.wrong[0].value', 2.9)
E('l3', 'quiz[2].widget.answer', 0.8 / (5 / 10)); E('l3', 'quiz[2].widget.wrong[0].value', 0.8 / 5)
fW = f1(r, 6); W = np.zeros(r.shape)
for s in range(6, T):
    W[s] = w1(fW[s])
H = np.array([W[t - 5:t + 1].mean(axis=0) for t in range(11, T)])
TURN = np.abs(np.diff(H, axis=0)).sum(axis=1).mean()
cs = np.cumsum(W, axis=0); H2 = (cs[11:] - cs[5:-6]) / 6      # route 2: rolling sum of cohort weights
two('6/6 turnover', TURN, np.abs(np.diff(H2, axis=0)).sum(axis=1).mean(), 1e-9)
for fid, path in (('l3', 'screens[8].prose'), ('homework', 'items[7].prose')):
    E(fid, path, round(TURN, 3))
E('l3', 'screens[8].widget.answer', round(0.01 - 0.577 * 0.0025, 5)); E('l3', 'screens[8].hints[1].text', round(0.577 * 0.25, 3))
E('l3', 'screens[8].widget.wrong[0].value', round(0.01 - 0.577 / 2 * 0.0025, 5)); E('l3', 'screens[8].widget.wrong[1].value', 0.0075)
E('l3', 'screens[8].explain.text', round(100 * (M66 - TURN * 0.0025), 2))
E('homework', 'items[7].widget.answer', round(0.0096 - 0.577 * 0.005, 6)); E('homework', 'items[7].widget.wrong[0].value', round(0.0096 - 0.577 / 2 * 0.005 + 1e-12, 6))   # 0.0081575: half up
E('homework', 'items[7].explain.text', round(0.577 * 0.5, 2)); E('homework', 'items[7].explain.text', round(100 * (M66 - 0.577 * 0.005), 2))
lv.claim(abs(0.577 * 0.5 / 0.96 - 0.30) < 0.005, 'homework items[7]: 50 bp takes 30% of the spread (the text says a third)')
E('homework', 'items[3].widget.model', round(100 * (M66 - TURN * 0.0025), 2)); E('homework', 'items[3].widget.model', round(TURN, 3))
E('homework', 'items[3].widget.model', round(0.1201 * 50000, -3)); E('homework', 'items[3].widget.model', round(0.1201 * 25000, -3))
lv.claim_text('homework', 'items[3].widget.model', 'The 12% is a choice of leverage, not a property of the strategy', False,
              'homework items[3] model: "The 12% is a choice of leverage" (the 12% is the strategy\'s spread; 12% of £50,000 is the leverage choice)')

# ======================= l1 =======================
E('l1', 'screens[0].canvas.params.rows[1][1]', round(100 * ((1.0095) ** 12 - 1), 2))
E('l1', 'screens[6].canvas.params.rows[0][0]', round(0.1201 * 100000))
E('l1', 'screens[5].widget.options[2].text', round((0.6 + 0.9) / 2, 2)); E('l1', 'quiz[2].widget.options[2].text', round((0.5 + 0.8) / 2, 2))
E('l1', 'quiz[1].widget.answer', 0.03 * 2e6 - 0.01 * 2e6); E('l1', 'quiz[1].widget.wrong[0].value', 0.03 * 2e6 + 0.01 * 2e6)
E('l1', 'quiz[1].widget.wrong[1].value', 0.03 * 2e6)
E('l1', 'quiz[3].widget.answer', 0.12 * 5e5); E('l1', 'quiz[3].widget.wrong[0].value', 0.12 * 1e6)
q7 = lv.text('l1', 'screens[7].question')
E('l1', 'screens[7].widget.options[0].text', round(1.8 - 0.6, 2)); E('l1', 'screens[7].widget.options[1].text', round(1.8 + 0.6, 2))
E('l1', 'screens[7].widget.options[3].text', 0.6); E('l1', 'screens[7].feedback.correct', round(1.8 - 0.6, 2))
lv.claim(all(abs(round(1.8 - 0.6, 2) - v) > 1e-9 for v in (1.8, 0.6)) and 'losers 0.6%' in q7,
         'l1 screens[7]: the correct spread (1.2%) is neither of the two inputs (1.8%, 0.6%)')
lv.claim_text('l1', 'summary.ideas[1]', 'A testable claim names a universe, a period, a signal, a holding rule and a number', False,
              'l1 summary.ideas[1]: every testable claim names all five (the hook keys the Sharpe and reversal claims testable without them)')

# ======================= l2: cohorts =======================
def live(t, J, K, skip=0):
    return list(range(max(J + skip, t - K + 1), t + 1))


def live2(t, J, K, skip=0):
    return [s for s in range(0, t + 1) if s >= J + skip and t - K < s]


stair = sorted(f'r{t - 5}c{s - 5}' for t in range(6, 12) for s in live(6 + (t - 6), 6, 3))
lv.claim(stair == sorted(J_('l2', 'screens[3].widget.answer')), 'l2 screens[3] staircase answer = live cohorts J 6 K 3, months 6 to 11')
lv.claim(all(live(t, 6, 3) == live2(t, 6, 3) for t in range(40)), 'two routes agree: live cohorts')
lv.claim(sorted(J_('l2', 'screens[4].widget.answer')) == [f'r2c{s - 14}' for s in live(20, 6, 3)], 'l2 screens[4] month 20 = cohorts 18 to 20')
E('l2', 'screens[0].widget.answer', 0 + 6 - 1); E('l2', 'screens[0].widget.wrong[1].value', -9)
E('l2', 'screens[5].widget.answer', round(1 / 300, 6)); E('l2', 'screens[5].widget.wrong[1].value', round(1 / 6, 4))
E('l2', 'quiz[0].widget.answer', len(live(100, 9, 6))); E('l2', 'quiz[1].widget.answer', min(t for t in range(40) if len(live(t, 6, 6)) == 6))
E('l2', 'quiz[3].widget.options[0].text', 40 - 1 - 12); E('l2', 'quiz[3].widget.options[0].text', 40 - 1 - 1)
E('l2', 'screens[2].widget.options[0].text', 20 - 1 - 6); E('l2', 'screens[2].widget.options[0].text', 18)
E('l2', 'screens[9].widget.answer', 120e6 / 12)
lv.claim(len(live(31, 6, 6)) == 6 and len(set(live(30, 6, 6)) & set(live(31, 6, 6))) == 5, 'l2 screens[6]: rows 30 and 31 share five cohorts')

# ======================= l4 =======================
for k, lo in ((1, 0.65), (1.5, 0.50), (2, 0.35)):
    lv.claim(abs((0.95 - k * 0.30) - lo) < 1e-9, f'l4 screens[1]: k = {k} band starts at {lo}')
E('l4', 'screens[1].explain.canvas.intervals.band.to', round(0.95 + 0.60, 2)); E('l4', 'screens[1].hints[2].text', round(0.54 / 0.30, 1))
lv.claim(0.95 - 1.5 * 0.30 > 0.41 >= 0.95 - 2 * 0.30, 'l4 screens[1]: k = 2 is the first slider stop covering 0.41')
E('l4', 'screens[3].widget.rows[0][1].answer', round(abs(0.62 - 0.95) / 0.30, 2)); E('l4', 'screens[3].widget.rows[1][1].answer', round(abs(0.52 - 1.31) / 0.33, 2))
E('l4', 'screens[4].widget.answer', round(1.71 - 1.20, 2)); E('l4', 'screens[4].widget.wrong[1].value', round(1.71 + 1.20, 2))
# "Rounding moves a spread by 0.01 at most": the largest gap between a rounded spread and the difference of rounded legs
gap = max(abs(round(b - s, 2) - (round(b, 2) - round(s, 2))) for s in np.arange(1.0, 1.05, 0.00037) for b in np.arange(1.5, 1.55, 0.00041))
lv.claim(gap <= 0.0100001, f'l4 screens[4]: rounding moves a printed spread by at most 0.01 (largest {gap:.4f})')
E('l4', 'screens[6].explain.text', round(5.98 / 17, 2))
E('l4', 'quiz[0].widget.options[0].text', 0.50 / 0.20); E('l4', 'quiz[0].widget.options[2].text', 0.20 / 0.50)
E('l4', 'quiz[1].widget.answer', round(6.0 / 17, 3)); E('l4', 'quiz[1].widget.wrong[1].value', round(6.0 / 289, 4))
E('l4', 'quiz[1].explain.text', round(2 * 6.0 / 17, 2)); E('l4', 'quiz[2].widget.options[1].why', 300 // 12)
# claim: the skip panel "matched in pattern" (paper: skipping raises every cell a little)
up = [(J, K) for J in (3, 6, 9, 12) for K in (3, 6, 9, 12) if wml1(r, J, K, 1).mean() > GRID[J, K].mean()]
lv.claim(len(up) == 8, f'skip raises {len(up)} of 16 cells (l9 says some fall)')
lv.claim_text('l4', 'screens[8].widget.options[0].text', 'three more in pattern', len(up) == 16,
              'l4 screens[8] keyed answer: "three more in pattern" (the skip panel raises only 8 of 16 cells on our panel)')
lv.claim(J_('l4', 'screens[0].hints[1].highlight') != ['r5'], 'l4 screens[0] hint 2 ("only two cells") highlights those cells, not January')
t7 = J_('l4', 'screens[7].widget.tests[7].setup')
lv.claim('(6, 6): 0.0062' in t7, 'l4 screens[7]: the code tests use the colleague cells on the canvas (6/6 at 0.62)', t7[:60])

# ======================= l5 =======================
def bug(r, J=6):
    return np.array([w1(np.prod(1 + r[t - J + 1:t + 1], axis=0) - 1) @ r[t] for t in range(J, r.shape[0])])


def bug2(r, J=6):
    f = f2(r, J)        # the formation return known at t + 1 covers months t - 5 to t
    return np.array([w1(f[t + 1]) @ r[t] for t in range(J, r.shape[0] - 1)] + [w1(np.prod(1 + r[-J:], axis=0) - 1) @ r[-1]])


rsh = shuffle(r, 0)
for lab, x, y in (('base', bug(r), bug2(r)), ('shuffled', bug(rsh), bug2(rsh))):
    two(f'look-ahead bug on {lab} panel', x, y, 1e-9)
b0, b1 = bug(r), bug(rsh)
for fid, path in (('l5', 'screens[0].canvas.params.lines[6]'), ('l5', 'screens[5].canvas.params.lines[1]')):
    E(fid, path, round(100 * b0.mean(), 2)); E(fid, path, round(tstat(b0), 2))
E('l5', 'screens[0].explain.text', round(100 * b0.mean(), 2))
E('l5', 'screens[5].canvas.params.lines[3]', round(100 * b1.mean(), 2)); E('l5', 'screens[5].canvas.params.lines[3]', round(tstat(b1), 2))
E('review', 'items[8].prose', round(100 * GRID[12, 3].mean(), 2))  # the 1.31% target is the real 12/3 cell; the shuffled 1.28% is made up, and says so
lv.claim('Both numbers are made up' in lv.text('review', 'items[8].prose'), 'review items[8]: the invented figures are labelled made up')
pl = wml1(rsh, 6, 1); two('correct 6/1 on the shuffled panel', pl, wml2(rsh, 6, 1), 1e-9)
E('l5', 'screens[4].canvas.params.lines[1]', round(100 * pl.mean(), 2)); E('l5', 'screens[4].canvas.params.lines[1]', round(tstat(pl), 2))
E('l5', 'screens[4].canvas.params.lines[3]', round(100 * M66, 2)); E('l5', 'screens[4].canvas.params.lines[3]', round(T66, 2))
E('l5', 'screens[0].canvas.params.lines[3]', 120 - 6 + 1)
lv.claim(round(100 * np.mean([w1(r[t]) @ r[t] for t in range(T)])) != 17, 'l5 summary.trap: ranking on month t alone is not the 17% bug')
lv.claim_text('l5', 'summary.trap', 'a bug that ranks on month-t returns makes 17%', False,
              'l5 summary.trap: "ranks on month-t returns makes 17%" (ranking on month t alone gives 41%; 17% is the window t - 5 to t)')
lv.claim_text('l5', 'quiz[2].feedback.correct', 'Only the placebo sees it', False,
              'l5 quiz[2] feedback "Only the placebo sees it" (its own explain says the window check catches it too)')
E('l5', 'quiz[1].widget.answer', round(1 / 30, 5)); E('l5', 'quiz[3].widget.answer', 50 * 0.02 * 2)
rsm, *_ = momentum_panel(n=200, T=120)


def placebo(r, J, seed):
    s = shuffle(r, seed); f = f1(s, J)
    return np.array([w1(f[t]) @ s[t] for t in range(J, s.shape[0])])


p0 = placebo(rsm, 6, 0)
E('l5', 'screens[8].explain.text', round(100 * p0.mean(), 2)); E('l5', 'screens[8].explain.text', round(tstat(p0), 2))
E('l5', 'screens[8].explain.text', len(p0)); E('l5', 'screens[8].feedback.correct', round(100 * p0.mean(), 2))
for i, (J, sd) in enumerate(((6, 0), (6, 1), (3, 0), (12, 5))):
    E('l5', f'screens[8].widget.tests[{i}].expect', float(placebo(rsm, J, sd).mean()))
flat = np.tile(0.001 * np.arange(20), (12, 1))
E('l5', 'screens[8].explain.text', round(100 * placebo(flat, 6, 0).mean(), 1))

# ======================= review =======================
E('review', 'items[2].widget.answer', len(live(18, 12, 9, 1))); E('review', 'items[2].widget.wrong[0].value', len(live(18, 12, 9, 0))); E('review', 'items[2].widget.wrong[1].value', 9)
E('review', 'items[2].explain.text', 9); E('review', 'items[2].explain.text', 21); E('review', 'items[2].explain.text', 12 + 1); E('review', 'items[2].explain.text', len(live(18, 12, 9, 1)))
E('review', 'items[2].prose', 12)
E('review', 'items[3].widget.answer', 50 - 1 - 6)
E('review', 'items[4].widget.answer', round((1.0077) ** 12 - 1, 5)); E('review', 'items[4].widget.wrong[0].value', round(12 * 0.0077, 4))
E('review', 'items[6].widget.answer', round((1.31 - 0.70) / 0.30, 2))
E('review', 'items[7].canvas.params.lines[3]', round(50 / 45 - 1, 6)); E('review', 'items[7].canvas.params.lines[3]', round(50 / 45 + 1, 6))


def w45(ft):
    d = dec1(ft)
    return np.where(d == 9, 1 / 45, 0.0) - np.where(d == 0, 1 / 50, 0.0)


fs = f1(rsh, 6)
p45 = np.array([w45(fs[t]) @ rsh[t] for t in range(6, T)])
lv.claim(tstat(p45) < 1.96, f'review items[7]: an unbalanced book still passes the placebo (0.20%, t {tstat(p45):.2f})')
lv.claim_text('review', 'items[7].canvas.params.lines[4]', '0.05% a month, t 0.31', abs(100 * p45.mean() - 0.05) < 0.01,
              f'review items[7] log: placebo 0.05%, t 0.31 (the 1/45 book on our shuffled panel gives {100 * p45.mean():.2f}%, t {tstat(p45):.2f})')

# ======================= homework =======================
for (J, K), (s_, b_) in {(3, 3): (1.2520, 1.7662), (3, 6): (1.1816, 1.7852), (6, 3): (1.0179, 1.9240), (6, 6): (1.0420, 2.0059)}.items():
    lv.claim(round(100 * comp1(r, J, K, lambda ft: leg_w1(ft, 0)).mean(), 4) == s_ and round(100 * comp1(r, J, K, lambda ft: leg_w1(ft, 9)).mean(), 4) == b_,
             f'homework items[0]: the {J}/{K} legs are our panel\'s')
lv.claim(sum(len(live(t, 6, 6)) == 6 for t in range(300)) == 289 == N66, 'homework items[1]: 289 full 6/6 months')
nx = np.array([w1(rsh[t + 1]) @ rsh[t] for t in range(6, T - 1)])        # rank at t on month t + 1, hold month t
lv.claim(abs(tstat(nx)) < 1.96, f'shuffled panel: ranking on next month\'s return gives {100 * nx.mean():.2f}%, t {tstat(nx):.2f}')
lv.claim_text('homework', 'items[6].widget.options[1].text', "computed from next month's return", abs(tstat(nx)) > 1.96,
              'homework items[6]: the placebo catches "the signal is computed from next month\'s return" (read literally it finds 0.01%, t 0.09)')
lv.claim_text('l4', 'screens[8].hints[2].text', 'The first answer', False, 'l4 screens[8] hint names an option by place (choices shuffle)')
# the L2-side continuity fix (homework-2 model) quotes the 6/6 placebo on the shuffled base panel
pl66 = wml1(rsh, 6, 6); two('6/6 placebo, shuffled base panel seed 0', pl66, wml2(rsh, 6, 6), 1e-9)
lv.claim(round(100 * pl66.mean(), 2) == -0.06 and round(tstat(pl66), 2) == -0.53 and len(pl66) == 289, '6/6 placebo: -0.06% a month, t -0.53, 289 months')
lv.claim('−0.06% a month, t −0.53' in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'momentum-rep', 'homework-2.json')))['items'][6]['model'], 'homework-2 items[6]: the shuffled 6/6 placebo is stated (-0.06%, t -0.53)')
E('homework', 'items[5].widget.answer', round((1.0131) ** 12 - 1, 3)); E('homework', 'items[5].explain.text', round(12 * 1.31, 2))

# ======================= values the review's fixes introduce (computed here; no path yet) =======================
x912 = GRID[9, 12]
lv.claim((round(100 * x912.mean(), 2), round(100 * x912.std(ddof=1), 2), len(x912)) == (0.80, 5.69, 280), 'fix value: 9/12 mean 0.80, sd 5.69, 280 months')
t912 = 0.80 / (5.69 / math.sqrt(280))
lv.claim(round(t912, 2) == 2.35 == round(tstat(x912), 2) == round(tstat2(x912), 2), f'fix value: 9/12 t 2.35 from rounded and unrounded inputs ({t912:.4f})')
lv.claim(round(math.sqrt(280), 2) == 16.73 and round(5.69 / math.sqrt(280), 3) == 0.340 and round(0.80 / 5.69, 4) == 0.1406, 'fix value: 9/12 working 16.73, 0.340, wrong 0.1406')
lv.claim(len(live(18, 12, 9, 1)) == 6 and len(live(18, 12, 9, 0)) == 7 and min(t for t in range(60) if len(live(t, 12, 9, 1)) == 9) == 21,
         'fix value: 12/9 skip 1 in month 18: six cohorts (13 to 18), seven without the skip, all nine from month 21')
lv.claim(abs((1.8 - 0.6) - 1.2) < 1e-12 and abs((1.8 + 0.6) - 2.4) < 1e-12, 'fix value: l1 screens[7] 1.8 - 0.6 = 1.2, sum 2.4')
lv.claim(3_000_000 - 2_000_000 == 1_000_000 and 3_000_000 + 2_000_000 == 5_000_000, 'fix value: review items[0] £1,000,000 own capital, £5,000,000 gross')
lv.claim(round(100 * p45.mean(), 2) == 0.20 and round(tstat(p45), 2) == 1.26, 'fix value: review items[7] log placebo 0.20%, t 1.26')
lv.claim(round(100 * 0.577 * 0.005 / 0.0096) == 30, 'fix value: homework items[7] 50 bp takes 30% of 0.96%')

lv.check_wrongs()


# ======================= code widgets: solution passes, starter fails =======================
def widgets(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code':
            yield o
        for v in o.values():
            yield from widgets(v)
    elif isinstance(o, list):
        for v in o:
            yield from widgets(v)


def run_case(ns, case):
    if case.get('setup'):
        exec(case['setup'], ns)
    got = eval(case['call'], ns)
    want = eval(case['expect'], ns)
    tol = case.get('tol')
    rel, ab = (tol.get('rel', 0), tol.get('abs', 0)) if tol else (1e-9, 1e-12)

    def close(a, b):
        a = a.tolist() if hasattr(a, 'tolist') else a
        b = b.tolist() if hasattr(b, 'tolist') else b
        if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(close(p, q) for p, q in zip(a, b))
        if isinstance(a, bool) or isinstance(b, bool):
            return a == b
        return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=ab)
    if case.get('compare', 'equal') == 'isclose':
        return close(got, want)
    g = got.tolist() if hasattr(got, 'tolist') else got
    return type(g) == type(want) and g == want if isinstance(want, bool) else g == want


for fid, doc in lv.files.items():
    for w in widgets(doc):
        for label, src, must in (('solution', w['solution'], True), ('starter', w['starter'], False)):
            ns = {}
            if w.get('prelude'):
                exec(w['prelude'], ns)
            try:
                exec(src, ns)
            except Exception:
                lv.claim(not must, f'{fid} {label} loads')
                continue
            res = []
            for case in w['tests'] + w.get('examples', []):
                try:
                    res.append(bool(run_case(ns, case)))
                except Exception:
                    res.append(False)
            if must:
                lv.claim(all(res), f'{fid} solution passes all {len(res)} tests and examples', f'fails {[i for i, v in enumerate(res) if not v]}')
            else:
                lv.claim(not all(res), f'{fid} starter fails at least one test', f'passes {sum(res)} of {len(res)}')
lv.report()
