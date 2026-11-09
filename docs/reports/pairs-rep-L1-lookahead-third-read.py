"""pairs-rep level 1, third read of concept-audit round 2, finding 3 (l1-ggr-design screens[5].explain.text:
"A threshold computed on trading prices sees the future, and it flatters the backtest.").

Question: does a 2 sd trigger taken from the TRADING-period spread earn more than the 2 sd trigger taken from the
FORMATION-period spread? Measured as the paired difference in payoff, look-ahead minus honest, with a standard
error across independent replications.

Part A uses the course's own generator and pair selection (read from the lesson JSON) with this script's own
trading loop (checked against the course's `trade_pair`). Part B uses differently specified panels built here:
true pairs with stationary gaps, and gaps whose volatility changes between formation and trading.

Run from the repo root with `python3 -I`. Exits 0. The asserts are what the third-read verdict rests on."""
import json
import os
import time

import numpy as np

T0 = time.time()
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'pairs-rep')
load = lambda f: json.load(open(os.path.join(ROOT, f + '.json')))
ns = {}
exec(load('l5-plan')['screens'][6]['widget']['prelude'], ns)                 # pairs_panel, normalise, trade_pair, close
exec(load('l2-normalised-paths')['screens'][5]['widget']['solution'], ns)    # ssd_matrix
exec(load('l3-closest-pairs')['screens'][3]['widget']['solution'], ns)       # top_pairs
pairs_panel, normalise, top_pairs, course_trade, CLOSE = ns['pairs_panel'], ns['normalise'], ns['top_pairs'], ns['trade_pair'], ns['close']

FORM, TRADE = 252, 126


def run_rule(a, b, thr, wait=0):
    """This script's own trading loop. Open when |a - b| > thr, close at the first crossing of zero or on the
    last day; with wait = 1 both fills are one day late. Returns (payoff, number of trips)."""
    s = a - b
    n = len(s)
    out = np.abs(s) > thr
    payoff, trips, t = 0.0, 0, 0
    while t < n:
        if thr > 0 and out[t] and t + wait < n - 1:
            side = 1.0 if s[t] > 0 else -1.0
            later = np.nonzero(s[t + 1:] * side <= 0)[0]
            tx = n - 1 if len(later) == 0 else min(t + 1 + int(later[0]) + wait, n - 1)
            to = t + wait
            payoff += side * ((b[tx] - b[to]) / b[to] - (a[tx] - a[to]) / a[to])
            trips += 1
            t = tx + 1
        else:
            t += 1
    return payoff, trips


def both(a_form, b_form, a_tr, b_tr, wait=0):
    """(honest payoff, look-ahead payoff, honest trips, look-ahead trips, formation sd, trading sd)."""
    sd_f = float(np.std(a_form - b_form))
    sd_t = float(np.std(a_tr - b_tr))          # the colleague's number in the lesson: np.std of the trading spread
    ph, nh = run_rule(a_tr, b_tr, 2 * sd_f, wait)
    pl, nl = run_rule(a_tr, b_tr, 2 * sd_t, wait)
    return ph, pl, nh, nl, sd_f, sd_t


def mean_se(x):
    x = np.asarray(x, dtype=float)
    return float(x.mean()), float(x.std(ddof=1) / np.sqrt(len(x)))


ROWS = []


def row(label, honest, look, extra=''):
    d = np.asarray(look) - np.asarray(honest)
    m, se = mean_se(d)
    ROWS.append((label, float(np.mean(honest)), float(np.mean(look)), m, se, m / se, float((d > 0).mean()), extra))
    return m, se


# ---- 0. this script's loop reproduces the course's trade_pair, and the lesson's two sds
P0 = normalise(CLOSE[:378]); F0, R0 = P0[:FORM], P0[FORM:]
for (i, j) in top_pairs(F0, 20):
    for w in (0, 1):
        mine = run_rule(R0[:, i], R0[:, j], 2 * float(np.std(F0[:, i] - F0[:, j])), w)[0]
        assert abs(mine - course_trade(F0, R0, i, j, w)[0]) < 1e-12, 'own loop must equal the course trade_pair'
sd_f, sd_t = both(F0[:, 2], F0[:, 3], R0[:, 2], R0[:, 3])[4:]
assert round(sd_f, 4) == 0.0210 and round(sd_t, 4) == 0.0300, 'l1 screens[5].prose: formation sd 0.0210, trading sd 0.0300'

# ---- A. the course's generator: fresh panels, three cycle positions against the break at day 1512
N_PANELS = 400
STARTS = {'before the break (start 0)': 0, 'break on trading day 0 (start 1260)': 1260, 'after the break (start 2268)': 2268}
A = {}
DIV = []     # pairs whose trading sd is over 3 times the formation sd: (opened honest, opened look-ahead, payoffs)
for brk_label, frac in (('breaks on', 0.8), ('breaks off', 0.0)):
    for seed in range(N_PANELS):
        c_, m_, i_, b_ = pairs_panel(seed=7000 + seed, break_frac=frac)
        for s_label, s in STARTS.items():
            if frac == 0.0 and s != 2268:
                continue                         # breaks off: one late cycle, to set beside the same days with breaks on
            Pn = normalise(c_[s:s + FORM + TRADE]); f, r = Pn[:FORM], Pn[FORM:]
            tp = top_pairs(f, 20)
            for w in (0, 1):
                res = [both(f[:, i], f[:, j], r[:, i], r[:, j], w) for i, j in tp]
                if w == 0 and frac > 0 and s > 0:
                    DIV += [(x[2] > 0, x[3] > 0, x[0], x[1]) for x in res if x[5] > 3 * x[4]]
                for k in (5, 20):
                    key = (brk_label, s_label, k, w)
                    A.setdefault(key, []).append((np.mean([x[0] for x in res[:k]]), np.mean([x[1] for x in res[:k]]),
                                                  np.mean([x[5] / x[4] for x in res[:k]])))
RES_A = {}
for key, v in A.items():
    v = np.array(v)
    brk_label, s_label, k, w = key
    shown = 'same days as the row above (start 2268)' if brk_label == 'breaks off' else s_label
    RES_A[key] = row(f'course generator, {brk_label}, {shown}, top {k},{"one-day wait" if w else "same day"}',
                     v[:, 0], v[:, 1], f'sd ratio {v[:, 2].mean():.2f}')

# the course's own panel (seed 2006), the 22 non-overlapping cycles the lesson's backtest uses
h, l = [], []
for s in range(0, CLOSE.shape[0] - 378 + 1, 126):
    Pn = normalise(CLOSE[s:s + 378]); f, r = Pn[:FORM], Pn[FORM:]
    res = [both(f[:, i], f[:, j], r[:, i], r[:, j]) for i, j in top_pairs(f, 20)]
    h.append(np.mean([x[0] for x in res])); l.append(np.mean([x[1] for x in res]))
COURSE = row('the course panel itself (seed 2006), 22 cycles, top 20, same day', h, l)


# ---- B. differently specified panels: true pairs, no selection, no bounce
def true_pairs(n, vol_ratio, seed, half_life=8.0, ou_sd=0.008, rw_sd=0.015):
    """n independent pairs. Each leg is a shared random walk plus its own mean-reverting gap; the gap's shock sd is
    multiplied by vol_ratio from trading day 0. The pair never breaks."""
    rng = np.random.default_rng(seed)
    days = FORM + TRADE
    phi = 0.5 ** (1.0 / half_life)
    common = np.cumsum(rw_sd * rng.standard_normal((days, n)), axis=0)
    scale = np.where(np.arange(days) >= FORM, vol_ratio, 1.0)[:, None, None]
    eps = ou_sd * scale * rng.standard_normal((days, n, 2))
    g = np.zeros((days, n, 2))
    g[0] = eps[0] / np.sqrt(1 - phi * phi)       # start in the stationary law
    for t in range(1, days):
        g[t] = phi * g[t - 1] + eps[t]
    px = np.exp(common[:, :, None] + g)
    return px / px[0]


RES_B = {}
N_TRUE = 6000
for label, vr in (('true pairs, stationary gaps, same volatility', 1.0),
                  ('true pairs, gap volatility doubles in trading', 2.0),
                  ('true pairs, gap volatility halves in trading', 0.5)):
    for w in (0, 1):
        px = true_pairs(N_TRUE, vr, seed=42)
        res = np.array([both(px[:FORM, p, 0], px[:FORM, p, 1], px[FORM:, p, 0], px[FORM:, p, 1], w) for p in range(N_TRUE)])
        RES_B[(vr, w)] = row(f'{label}, {"one-day wait" if w else "same day"}', res[:, 0], res[:, 1],
                             f'sd ratio {np.mean(res[:, 5] / res[:, 4]):.2f}, trips {res[:, 2].mean():.2f} v {res[:, 3].mean():.2f}')

# ---- the table
print('look-ahead minus honest = payoff with the 2 sd trigger from the trading spread minus the same from the formation spread')
print('payoff per cycle on committed capital (Part A: mean over the top k pairs; Part B: per pair), as a fraction\n')
print(f'{"regime":<86}{"honest":>9}{"look":>9}{"diff":>9}{"se":>8}{"t":>7}{"share>0":>9}  note')
for label, mh, ml, m, se, t, share, extra in ROWS:
    print(f'{label:<86}{mh:>+9.4f}{ml:>+9.4f}{m:>+9.4f}{se:>8.4f}{t:>+7.1f}{share:>9.2f}  {extra}')
# ---- the pair on the lesson's screen, and what happens to pairs that drift apart
h23, l23 = both(F0[:, 2], F0[:, 3], R0[:, 2], R0[:, 3], 0)[:2]
h23w, l23w = both(F0[:, 2], F0[:, 3], R0[:, 2], R0[:, 3], 1)[:2]
print(f'\nthe pair on the screen (shares 2 and 3, start 0): honest {h23:+.4f}, look-ahead {l23:+.4f}; with the wait {h23w:+.4f}, {l23w:+.4f}')
DIV = np.array(DIV, dtype=float)
print(f'pairs with trading sd over 3 times formation sd (breaks on, starts 1260 and 2268, n = {len(DIV)}): opened by the honest rule '
      f'{DIV[:, 0].mean():.2f}, by the look-ahead rule {DIV[:, 1].mean():.2f}; mean payoff {DIV[:, 2].mean():+.4f} against {DIV[:, 3].mean():+.4f}')

# ---- what the verdict rests on
# 1. On the course's generator the look-ahead trigger earns more on average in every top-20 regime (the fixer's side).
for key, (m, se) in RES_A.items():
    if key[2] == 20:
        assert m > 3 * se, f'look-ahead flatters the top-20 average on the course generator: {key}'
    assert m > 0, f'no regime of the course generator has a negative mean difference: {key}'
assert COURSE[0] > 3 * COURSE[1], 'look-ahead flatters on the course panel itself'
m, se = RES_B[(1.0, 0)]
assert m > 3 * se, 'it also flatters, mildly, on true pairs with stationary gaps'
# 2. It is not a law of look-ahead (the auditor's side): on true pairs whose gap volatility doubles and which still
#    converge, the look-ahead trigger earns less; when volatility halves it earns more.
for w in (0, 1):
    m, se = RES_B[(2.0, w)]
    assert m < -3 * se, 'trading volatility up, pairs still converge: the look-ahead trigger earns less'
    m, se = RES_B[(0.5, w)]
    assert m > 3 * se, 'trading volatility down: the look-ahead trigger earns more'
# 3. On the very pair the screen draws, the look-ahead trigger earns less (the replacement text says so).
assert l23 < h23 - 0.05 and l23w < h23w - 0.05, 'pair (2, 3) at start 0: look-ahead earns less than the honest trigger'
# 4. The mechanism is not "diverging pairs are never opened": they are opened nearly always, later, and lose less.
assert DIV[:, 1].mean() > 0.9 and DIV[:, 3].mean() > DIV[:, 2].mean(), 'diverging pairs still open under look-ahead; they lose less'
print(f'\npairs-rep L1 look-ahead third read: all asserts hold, {time.time() - T0:.0f}s')
