#!/usr/bin/env python3
"""Concept checks for pairs-rep level 2 (lessons l6 to l10, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/pairs-rep-L2-concepts.py
Exit 0 when the content is correct. A check that fails because the content is wrong is marked
EXPECTED_FAIL and keeps failing, with the corrected assert in a comment beside it.
Each assert names the ledger row it covers (docs/reports/audit-pairs-rep-1-3-ledger.md).
"""
import math
import numpy as np

FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("FAIL", msg)
    else:
        print("ok  ", msg)


def pairs_panel(seed=2006, n_ind=10, per_ind=10, n_pairs=20, days=3024, half_life=8.0, ou_sd=0.008,
                rw_sd=0.015, break_day=1512, break_frac=0.8, half_spread=0.005):
    rng = np.random.default_rng(seed)
    N = n_ind * per_ind
    ind = np.repeat(np.arange(n_ind), per_ind)
    mkt = np.cumsum(0.0003 + 0.010 * rng.standard_normal(days))
    indf = np.cumsum(0.008 * rng.standard_normal((days, n_ind)), axis=0)
    phi = 0.5 ** (1.0 / half_life)
    u = np.cumsum(rw_sd * rng.standard_normal((days, N)), axis=0)
    common = np.cumsum(rw_sd * rng.standard_normal((days, n_pairs)), axis=0)
    eps = ou_sd * rng.standard_normal((days, 2 * n_pairs))
    a = np.zeros((days, 2 * n_pairs))
    for t in range(1, days):
        a[t] = phi * a[t - 1] + eps[t]
    broken = rng.random(n_pairs) < break_frac
    drift = np.cumsum(rw_sd * rng.standard_normal((days, 2 * n_pairs)), axis=0)
    for k in range(n_pairs):
        for j in (2 * k, 2 * k + 1):
            x = common[:, k] + a[:, j]
            if broken[k]:
                x = x + np.where(np.arange(days) >= break_day, drift[:, j] - drift[break_day, j], 0.0)
            u[:, j] = x
    pair_ind = np.repeat(np.arange(n_ind), 2)[:n_pairs]
    ind[:2 * n_pairs] = np.repeat(pair_ind, 2)
    logp = np.log(50.0) + mkt[:, None] + indf[:, ind] + u
    mid = np.exp(logp)
    bounce = np.where(rng.random((days, N)) < 0.5, 1 + half_spread, 1 - half_spread)
    close = mid * bounce
    return close, mid, ind, broken


def normalise(P):
    P = np.asarray(P, dtype=float)
    return P / P[0]


def trips(form, trade, i, j, wait=0, open_at=2.0, stop=None):
    """The course's trading loop (l7 screens[8]) as a list of (open, close, converged, payoff)."""
    sd = float(np.std(form[:, i] - form[:, j]))
    a, b = trade[:, i].tolist(), trade[:, j].tolist()
    n = len(a)
    out, t = [], 0
    while t < n:
        s = a[t] - b[t]
        if sd > 0 and abs(s) > open_at * sd and t + wait < n - 1:
            side = 1 if s > 0 else -1
            to = t + wait
            tc = next((u for u in range(t + 1, n) if (a[u] - b[u]) * side <= 0
                       or (stop is not None and abs(a[u] - b[u]) > stop * sd)), None)
            stopped = tc is not None and (a[tc] - b[tc]) * side > 0
            tx = n - 1 if tc is None else min(tc + wait, n - 1)
            pnl = side * ((b[tx] - b[to]) / b[to] - (a[tx] - a[to]) / a[to])
            out.append((to, tx, tc is not None and not stopped, pnl))
            if stopped:
                break  # the stop shuts the pair for the cycle
            t = tx + 1
            continue
        t += 1
    return out


def payoff(form, trade, i, j, **kw):
    return sum(p for *_, p in trips(form, trade, i, j, **kw))


close, mid, ind, broken = pairs_panel()
Pn = normalise(close[:378]); form, trade = Pn[:252], Pn[252:]

# ---------------------------------------------------------------- l6: opening rule
# long the cheaper leg gains on convergence; the flipped trade loses the same amount
f = np.array([[1.0, 1.0], [1.01, 1.0], [1.0, 1.0], [0.99, 1.0]])
tr = np.array([[1.0, 1.0], [1.03, 1.0], [1.02, 1.0], [0.99, 1.0], [1.0, 1.0]])
p = payoff(f, tr, 0, 1)
check(p > 0, "l6 screens[2]: buying the cheaper normalised price and selling the dearer gains on convergence (ledger l6 screens[2])")
# flip: trade the mirror by swapping the sign of the spread rule
sd = float(np.std(f[:, 0] - f[:, 1]))
t_open = next(t for t in range(5) if abs(tr[t, 0] - tr[t, 1]) > 2 * sd)
t_close = next(u for u in range(t_open + 1, 5) if (tr[u, 0] - tr[u, 1]) <= 0)
wrong_way = (tr[t_close, 0] / tr[t_open, 0] - 1) - (tr[t_close, 1] / tr[t_open, 1] - 1)
check(abs(wrong_way + p) < 1e-12, "l6 screens[5]: the sign error earns minus the correct payoff (ledger l6 screens[5])")
# the rule is a level test: a spread beyond 2 sd on day 0 opens on day 0
tr0 = np.array([[1.05, 1.0], [1.03, 1.0], [1.0, 1.0], [0.99, 1.0], [1.0, 1.0]])
check(trips(f, tr0, 0, 1)[0][0] == 0, "l6 screens[6]: a spread beyond 2 sd on day 0 opens on day 0 (ledger l6 screens[6])")
check(abs(1 / 1.1715 - 0.8536) < 5e-5 and abs(1 / 1.2247 - 0.8165) < 5e-5, "l6 screens[3]: £1 buys 1/p units (ledger l6 screens[3])")
# more opens at a lower trigger on pair (2, 3) of year 1: 6, 4, 2
opens = [len(trips(form, trade, 2, 3, open_at=m)) for m in (1.5, 2.0, 3.0)]
check(opens == [6, 4, 2], "l6 screens[4]: 6, 4, 2 opens at 1.5, 2, 3 sd on pair (2, 3) (ledger l6 screens[1].explain)")
# a wider trigger never produces more opens on average (Monte Carlo over planted pairs on fresh panels)
cnt = {1.5: 0, 2.0: 0, 3.0: 0}
for seed in range(40):
    c2, _, _, _ = pairs_panel(seed=20_000 + seed, days=378, break_frac=0.0)
    P2 = normalise(c2)
    for k in range(20):
        for m in cnt:
            cnt[m] += len(trips(P2[:252], P2[252:], 2 * k, 2 * k + 1, open_at=m))
check(cnt[1.5] > cnt[2.0] > cnt[3.0], "l6 quiz[2]: raising the trigger means fewer trades, on average (ledger l6 quiz[2])")

# ---------------------------------------------------------------- l7: closing rule
blot = trips(form, trade, 2, 3)
check([(a, b) for a, b, _, _ in blot] == [(28, 43), (50, 58), (86, 97), (116, 125)] and abs(sum(p for *_, p in blot) - 0.2218) < 5e-4,
      "l7 screens[1]/[3]: four round trips on pair (2, 3), total 0.2218 (ledger l7 screens[3])")
check(abs((1.3359 / 1.1715 - 1) - (1.3263 / 1.2247 - 1) - 0.0574) < 5e-4, "l7 screens[2]: payoff = long return - short return (ledger l7 screens[2])")
# with the wait the last signal that can open is day 123 (n = 126); without it day 124
n = 126
check(max(t for t in range(n) if t + 1 < n - 1) == 123 and max(t for t in range(n) if t < n - 1) == 124,
      "l7 screens[7], quiz[2]: last signal day 123 with the wait, 124 without (ledger l7 screens[7])")
# forced close books the loss of a non-converging pair
f2 = np.array([[1.0, 1.0], [1.01, 1.0], [1.0, 1.0], [0.99, 1.0]])
tr2 = np.array([[1.0, 1.0], [1.03, 1.0], [1.05, 1.0], [1.08, 1.0], [1.10, 1.0]])
t2 = trips(f2, tr2, 0, 1)
check(len(t2) == 1 and t2[0][1] == 4 and t2[0][2] is False and t2[0][3] < 0,
      "l7 screens[4]: a pair that never crosses is closed on the last day at a loss (ledger l7 screens[4])")
# closing at the band instead of the crossing books less on (2, 3): 0.1955 against 0.2218, more trips
def band_exit(form, trade, i, j):
    sd = float(np.std(form[:, i] - form[:, j])); a, b = trade[:, i], trade[:, j]
    n, t, tot, k = len(a), 0, 0.0, 0
    while t < n:
        s = a[t] - b[t]
        if abs(s) > 2 * sd and t < n - 1:
            side = 1 if s > 0 else -1
            tc = next((u for u in range(t + 1, n) if abs(a[u] - b[u]) <= 2 * sd), n - 1)
            tot += side * ((b[tc] - b[t]) / b[t] - (a[tc] - a[t]) / a[t]); k += 1
            t = tc + 1; continue
        t += 1
    return tot, k
be, kb = band_exit(form, trade, 2, 3)
check(abs(be - 0.1955) < 5e-4 and kb == 9 and be < 0.2218, "l7 screens[6]: the band exit books 0.1955 in 9 trips, less than the crossing (ledger l7 screens[6])")
# a stop at 4 sd: planted pairs that reach 4 sd usually come back (Monte Carlo over fresh planted pairs)
came_back, reached = 0, 0
for seed in range(60):
    c2, _, _, _ = pairs_panel(seed=30_000 + seed, days=378, break_frac=0.0)
    P2 = normalise(c2)
    for k in range(20):
        fo, tr_ = P2[:252], P2[252:]
        sdk = float(np.std(fo[:, 2 * k] - fo[:, 2 * k + 1]))
        s = tr_[:, 2 * k] - tr_[:, 2 * k + 1]
        for (to, tx, conv, _) in trips(fo, tr_, 2 * k, 2 * k + 1):
            seg = s[to:tx + 1]
            if np.max(np.abs(seg)) > 4 * sdk:
                reached += 1
                came_back += conv
check(reached > 50 and came_back / reached > 0.5, f"l7 screens[5]: a planted pair at 4 sd usually comes back ({came_back}/{reached}) (ledger l7 screens[5].explain)")
sa = np.mean([payoff(form, trade, 2 * k, 2 * k + 1, stop=4.0) for k in range(20)])
check(abs(sa - 0.1068) < 2e-3, f"l7 screens[5]: the stop cuts the first cycle to about 10.68% ({sa:.4f}) (ledger l7 screens[5].explain)")

# ---------------------------------------------------------------- l8: returns, overlap and t statistics
comm = sum(payoff(form, trade, i, j) for i, j in [(2 * k, 2 * k + 1) for k in range(20)]) / 20
check(abs(comm - 0.1424) < 5e-4, "l8 screens[2]: first-cycle top 20 committed 14.24% (ledger l8 screens[2])")
# overlapping six-month cycles inflate a naive t statistic; Newey-West with 5 lags corrects most of it
def nw_t(x, lags):
    x = np.asarray(x, float); n = len(x); m = x.mean(); e = x - m
    s = np.sum(e * e) / n
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        s += 2 * w * np.sum(e[L:] * e[:-L]) / n
    return m / math.sqrt(s / n)
rng = np.random.default_rng(1)
naive, nw = [], []
for _ in range(4000):
    r = rng.standard_normal(132)                       # 132 months of i.i.d. returns, mean 0
    cyc = np.convolve(r, np.ones(6), "valid")           # 127 overlapping six-month sums
    naive.append(cyc.mean() / (cyc.std(ddof=1) / math.sqrt(len(cyc))))
    nw.append(nw_t(cyc, 5))
naive, nw = np.array(naive), np.array(nw)
check(naive.std() > 1.8 and 0.9 < nw.std() < 1.5,
      f"l8 screens[4]: under no effect the naive t has sd {naive.std():.2f}, Newey-West(5) {nw.std():.2f}: overlap inflates the naive t (ledger l8 screens[4])")
check(abs(naive.mean()) < 0.1, "l8 screens[4] byKey.bias: overlap leaves the mean unbiased; only the standard error changes (ledger l8 screens[4])")

# ---------------------------------------------------------------- l9: the bounce, the wait and costs
# Monte Carlo on fresh planted pairs: same-day closes earn more than mids (bounce); the wait removes it and
# gives up a day of convergence, so closes-with-wait sits near mids-with-wait and below mids same day
acc = {"c0": [], "c1": [], "m0": [], "m1": []}
for seed in range(60):
    c2, m2, _, _ = pairs_panel(seed=40_000 + seed, days=378, break_frac=0.0)
    Pc, Pm = normalise(c2), normalise(m2)
    for k in range(20):
        acc["c0"].append(payoff(Pc[:252], Pc[252:], 2 * k, 2 * k + 1))
        acc["c1"].append(payoff(Pc[:252], Pc[252:], 2 * k, 2 * k + 1, wait=1))
        acc["m0"].append(payoff(Pm[:252], Pm[252:], 2 * k, 2 * k + 1))
        acc["m1"].append(payoff(Pm[:252], Pm[252:], 2 * k, 2 * k + 1, wait=1))
mean = {k: np.mean(v) for k, v in acc.items()}
se = {k: np.std(v, ddof=1) / math.sqrt(len(v)) for k, v in acc.items()}
print("planted pairs, mean payoff per cycle:", {k: round(v, 4) for k, v in mean.items()})
check(mean["c0"] - mean["m0"] > 3 * se["c0"], "l9 screens[2]: same-day fills on closes capture the bounce: closes beat mids (ledger l9 screens[2])")
check(mean["m0"] > mean["m1"], "l9 screens[7]: on mids the wait costs only a day of convergence (ledger l9 screens[7])")
check(abs(mean["c1"] - mean["m1"]) < 0.3 * (mean["c0"] - mean["m0"]),
      "l9 screens[3]: filling at the next close removes the bounce: closes with the wait sit near mids with the wait (ledger l9 screens[3])")
check(mean["c1"] < mean["c0"], "l10 screens[7] test: the wait lowers the top-20 figure (ledger l10 screens[7])")
# bounce direction: a signal on a close at the bid is a buy at the bid, so the same-day fill books the rebound
check(50.25 / 50.0 - 1 > 0 and (50.25 - 49.75) / 50 == 0.01, "l9 screens[0]: buying at the printed bid pays 1% less than the ask, the full spread (ledger l9 screens[0])")
# costs: four trades per round trip
check(abs(4 * 0.001 * 1.6886 - 0.00675) < 1e-5 and abs(0.0452 / (4 * 1.6886) - 0.00669) < 1e-5,
      "l9 screens[4]/[5]: cost per pair per cycle = 4 c trips; break-even c* = gross / (4 trips) (ledger l9 screens[5])")
check(0.0452 / (4 * 1.6886) < 0.0452 / 1.6886 < 0.0452, "l9 screens[6]: charging once per pair or once per trip overstates the break-even (ledger l9 screens[6])")
check(abs((0.0452 - 4 * 0.002 * 1.69) / 6 - 0.00528) < 5e-5, "homework-2 items[4]: net monthly = (gross - 4 c trips) / 6")
# normalisation base cancels in each leg's simple return (homework-2 items[6])
x = np.array([10.0, 12.0, 11.0]); base_a = x / x[0]; base_b = x / x[1]
check(abs((base_a[2] / base_a[1] - 1) - (base_b[2] / base_b[1] - 1)) < 1e-12,
      "homework-2 items[6]: the normalisation base cancels in p_out / p_in on the same trade (ledger homework-2 items[6])")
# ... but it changes which trades open: re-basing at the trading start resets any open gap to 0
s_form_end = form[-1, 2] - form[-1, 3]
rebased = trade / trade[0]
check(abs(rebased[0, 2] - rebased[0, 3]) < 1e-12 and abs(trade[0, 2] - trade[0, 3]) > 0,
      "l2 quiz[1], homework-2 items[6]: re-basing at the trading start wipes out the gap open on day 0 (ledger l2 quiz[1])")

print()
print(f"{len(FAILS)} failing check(s)")
for f_ in FAILS:
    print(" -", f_)
raise SystemExit(1 if FAILS else 0)
