#!/usr/bin/env python3
"""Concept checks for pairs-rep level 3 (lessons l11 to l15, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/pairs-rep-L3-concepts.py
Exit 0 when the content is correct. A check that fails because the content is wrong is marked
EXPECTED_FAIL and keeps failing, with the corrected assert in a comment beside it.
Each assert names the ledger row it covers (docs/reports/audit-pairs-rep-1-3-ledger.md).
Needs numpy and statsmodels; about two minutes.
"""
import math
import warnings
import numpy as np

warnings.filterwarnings("ignore")
from statsmodels.tsa.stattools import coint  # noqa: E402

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
    return close, mid, ind, broken, np.exp(mkt)


def normalise(P):
    P = np.asarray(P, dtype=float)
    return P / P[0]


def ssd_matrix(Pn):
    G = Pn.T @ Pn
    d = np.diag(G)
    return d[:, None] + d[None, :] - 2 * G


def top_pairs(Pn, k):
    D = ssd_matrix(Pn)
    i, j = np.triu_indices(D.shape[0], 1)
    order = np.argsort(D[i, j], kind="stable")[:k]
    return [(int(i[o]), int(j[o])) for o in order]


def trips(form, trade, i, j, wait=0, open_at=2.0):
    sd = float(np.std(form[:, i] - form[:, j]))
    a, b = trade[:, i].tolist(), trade[:, j].tolist()
    n = len(a)
    out, t = [], 0
    while t < n:
        s = a[t] - b[t]
        if sd > 0 and abs(s) > open_at * sd and t + wait < n - 1:
            side = 1 if s > 0 else -1
            to = t + wait
            tc = next((u for u in range(t + 1, n) if (a[u] - b[u]) * side <= 0), None)
            tx = n - 1 if tc is None else min(tc + wait, n - 1)
            pnl = side * ((b[tx] - b[to]) / b[to] - (a[tx] - a[to]) / a[to])
            out.append((to, tx, tc is not None, pnl))
            t = tx + 1
            continue
        t += 1
    return out


def payoff(form, trade, i, j, **kw):
    return sum(p for *_, p in trips(form, trade, i, j, **kw))


close, mid, ind, broken, M = pairs_panel()

# ---------------------------------------------------------------- l11: the decline and the convergence share
# survival ratios and the pooled convergence share are plain arithmetic
check(abs(0.64 / 1.50 - 0.4267) < 5e-3 and abs(0.48 / 1.14 - 0.4211) < 5e-3, "l11 screens[1]/[9]: survived = after / before (ledger l11 screens[9])")
check(abs(51 / 90 - 0.5667) < 5e-4 and (26 / 40 + 25 / 50) / 2 != 51 / 90, "review-3 items[2]: pool the trades, do not average the shares (ledger review-3 items[2])")
# broken pairs (random walks) open about as readily as real ones but converge less often; faster reversion
# ("crowding": shorter half-life) keeps convergence high while shrinking the gain. Monte Carlo on fresh panels.
conv = {"planted": [0, 0], "fast": [0, 0], "broken": [0, 0]}
gain = {"planted": [], "fast": [], "broken": []}
for seed in range(40):
    c_p, _, _, _, _ = pairs_panel(seed=50_000 + seed, days=378, break_frac=0.0)
    c_f, _, _, _, _ = pairs_panel(seed=50_000 + seed, days=378, break_frac=0.0, half_life=2.0)
    c_b, _, _, _, _ = pairs_panel(seed=50_000 + seed, days=378, break_frac=1.0, break_day=252)
    for name, c in (("planted", c_p), ("fast", c_f), ("broken", c_b)):
        P = normalise(c)
        for k in range(20):
            tr = trips(P[:252], P[252:], 2 * k, 2 * k + 1)
            conv[name][0] += sum(1 for t in tr if t[2]); conv[name][1] += len(tr)
            gain[name] += [t[3] for t in tr]
share = {k: v[0] / v[1] for k, v in conv.items()}
print("convergence share:", {k: round(v, 3) for k, v in share.items()}, "trades:", {k: v[1] for k, v in conv.items()})
check(share["broken"] < share["planted"] - 0.15, "l11 screens[3]/[5]: pairs that stop co-moving open but converge far less often (ledger l11 screens[5])")
check(share["fast"] >= share["planted"] - 0.03 and conv["fast"][1] > 0,
      "l11 screens[5], review-3 items[1]: faster convergence (crowding) leaves the crossing share intact (ledger review-3 items[1])")
check(share["planted"] > 0.6, "l11 screens[6]: unbroken planted pairs converge most of the time (ledger l11 screens[6])")

# ---------------------------------------------------------------- l12: Engle-Granger size, power and selection bias
F0 = normalise(close[:252]); L0 = np.log(F0)
p23 = coint(L0[:, 2], L0[:, 3])[1]; p23s = coint(np.log(5 * F0[:, 2]), L0[:, 3])[1]
check(abs(p23 - p23s) < 1e-12, "l12 screens[7]: scaling a price adds a constant to its log, absorbed by the intercept (ledger l12 screens[7].explain)")
# size on chance pairs (shares 40 to 99, independent random walks with shared market and industry factors)
# Disputes read: 24 fresh panels, all 4,930 chance pairs each, the lesson's eg_pvalue: closes mean 366 chance
# passes (size 0.074, se 22), mids 314 (0.064); per-panel sd 106, range 169 to 546 (sim8.py, disputes-pairs-rep)
rej_c, rej_m, n_tests, per_panel = 0, 0, 0, []
for seed in range(24):
    c2, m2, _, _, _ = pairs_panel(seed=60_000 + seed, days=252, break_frac=0.0)
    r2 = np.random.default_rng(seed)
    Lc, Lm = np.log(c2), np.log(m2)
    r = 0
    for _ in range(120):
        i, j = r2.choice(np.arange(40, 100), 2, replace=False)
        pc = coint(Lc[:, i], Lc[:, j])[1]; pm = coint(Lm[:, i], Lm[:, j])[1]
        rej_c += pc < 0.05; rej_m += pm < 0.05; r += pc < 0.05; n_tests += 1
    per_panel.append(r / 120)
size_c, size_m = rej_c / n_tests, rej_m / n_tests
print(f"EG rejection rate on chance pairs at 5%: closes {size_c:.3f}, mids {size_m:.3f}; per panel min {min(per_panel):.3f} max {max(per_panel):.3f}")
check(0.04 < size_m < 0.08, "l12 screens[4]: on mid prices the test rejects about 5% of chance pairs (ledger l12 screens[4].prose)")
check(size_c > size_m and size_c < 0.10,
      "l12 screens[4].explain (corrected claim, fix pass): the short year and the closing bounce lift the false-alarm rate to about 7% (ledger l12 screens[4].explain)")
check(max(per_panel) - min(per_panel) > 0.04,
      "l12 screens[4].explain (corrected claim, fix pass): tests sharing 100 shares are dependent, so one year's count can sit far from 248 (ledger l12 screens[4].explain)")
# power on planted pairs: well below 100% on one year, so a real relationship can fail
rej, m = 0, 0
for seed in range(20):
    c2, _, _, _, _ = pairs_panel(seed=70_000 + seed, days=252, break_frac=0.0)
    L = np.log(c2)
    for k in range(20):
        rej += coint(L[:, 2 * k], L[:, 2 * k + 1])[1] < 0.05; m += 1
power = rej / m
print(f"EG power on planted pairs over one year: {power:.3f}")
check(0.45 < power < 0.95, "l12 screens[1].explain: one year is a small sample: 5 of 20 planted pairs failing is typical (ledger l12 screens[1].explain)")
# selection bias: the 50 closest pairs by SSD among chance pairs pass far more often than 5%
rej_sel, n_sel = 0, 0
for seed in range(12):
    c2, _, _, _, _ = pairs_panel(seed=80_000 + seed, days=252, break_frac=0.0)
    P = normalise(c2[:, 40:])
    L = np.log(P)
    for i, j in top_pairs(P, 30):
        rej_sel += coint(L[:, i], L[:, j])[1] < 0.05; n_sel += 1
sel = rej_sel / n_sel
print(f"EG rejection rate among the 30 closest chance pairs by SSD: {sel:.3f}")
check(sel > 0.25, "l12 screens[9].explain, review-3 items[5]: pairs picked by distance on the same year already look stationary (ledger l12 screens[9].explain)")
check(abs(4950 * 0.05 - 247.5) < 1e-9 and abs(190 * 0.05 - 9.5) < 1e-9 and abs(10 * 45 * 0.05 - 22.5) < 1e-9,
      "l12 screens[4], review-3 items[3], homework-3 items[4]: expected chance passes = tests x level (ledger l12 screens[4])")
# hedge ratio 2 for ln L = 2 ln A + u: Engle-Granger finds it, distance ranks the pair far down
rng = np.random.default_rng(3)
lnA = np.log(F0[:, 2]); u = 0.01 * rng.standard_normal(252)
for t in range(1, 252):
    u[t] += 0.917 * u[t - 1]
lnL = 2 * lnA + u
beta = np.polyfit(lnA, lnL, 1)[0]
Lp = np.exp(lnL - lnL[0])
ssd_LA = float(np.sum((Lp - F0[:, 2]) ** 2))
D = ssd_matrix(F0); i0, j0 = np.triu_indices(100, 1)
rank = int(np.sum(np.sort(D[i0, j0]) < ssd_LA))
check(abs(beta - 2) < 0.15 and rank > 20 and coint(lnL, lnA)[1] < 0.05,
      f"l12 screens[6]: slope {beta:.2f}, p < 0.05, yet SSD rank {rank}: a hedge far from 1 is invisible to distance (ledger l12 screens[6])")
# a formation p-value says nothing about the trading period: planted pairs with p near 0 at 1,260 break at 1,512
F1 = np.log(normalise(close[1260:1512]))
kept = [k for k in range(20) if coint(F1[:, 2 * k], F1[:, 2 * k + 1])[1] < 0.05]
check(sum(1 for k in kept if broken[k]) >= 8, "l12 screens[5], quiz[2]: low formation p-values precede a break the test never saw (ledger l12 screens[5])")

# ---------------------------------------------------------------- l13: factor regression
# dollar-neutral pairs with equal market loadings: beta near 0 on fresh panels
betas = []
for seed in range(30):
    c2, _, _, _, M2 = pairs_panel(seed=90_000 + seed, days=3024, break_frac=0.0)
    starts = range(0, 3024 - 378 + 1, 126)
    y = []
    x = []
    for s in starts:
        P = normalise(c2[s:s + 378]); fo, tr = P[:252], P[252:]
        y.append(np.mean([payoff(fo, tr, i, j) for i, j in top_pairs(fo, 20)]))
        x.append(M2[s + 377] / M2[s + 252] - 1)
    betas.append(np.polyfit(x, y, 1)[0])
betas = np.array(betas)
print(f"market beta of the top-20 book across panels: mean {betas.mean():.3f}, sd {betas.std():.3f}")
check(abs(betas.mean()) < 0.1 and np.mean(np.abs(betas) < 0.3) > 0.8, "l13 screens[2]: equal market loadings cancel in a £1 long, £1 short pair, so beta is near 0 (ledger l13 screens[2])")
check(abs(0.0623 + 0.0529 * (-0.10) - 0.0570) < 5e-5 and abs(0.0623 + 0.0529 * 0.15 - 0.0702) < 5e-5, "l13 screens[3], review-3 items[6]: the fitted line alpha + beta R_m")
check(abs(1 - 0.60 - 0.40) < 1e-12 and abs(1 - 1.25 + 0.25) < 1e-12, "l13 screens[7], review-3 items[7]: net factor exposure = long - short when loadings are equal")
# a beta near 0 is not riskless: the panel with the break loses in some cycles while beta stays small
starts = range(0, 3024 - 378 + 1, 21)
ys = [np.mean([payoff(normalise(close[s:s + 378])[:252], normalise(close[s:s + 378])[252:], i, j, wait=1)
               for i, j in top_pairs(normalise(close[s:s + 378])[:252], 20)]) for s in starts]
check(sum(1 for v in ys if v < 0) >= 10 and min(ys) < -0.05, "l13 screens[5]: with the wait, cycles lose money while beta is near 0 (ledger l13 screens[5])")

# ---------------------------------------------------------------- l14: out of sample and the winner's curse
# twelve settings with the same true mean: the best in-sample cell's held-out return falls back
rng = np.random.default_rng(7)
fall_best, fall_random = [], []
for _ in range(4000):
    ins = 0.01 + 0.004 * rng.standard_normal(12)   # in-sample means of 12 settings
    outs = 0.01 + 0.004 * rng.standard_normal(12)  # held-out means, same truth
    b = int(np.argmax(ins))
    fall_best.append(outs[b] - ins[b]); fall_random.append(outs[0] - ins[0])
print(f"winner's curse: mean held-out fall of the best cell {np.mean(fall_best):.4f}, of a fixed cell {np.mean(fall_random):.4f}")
check(np.mean(fall_best) < -0.003 and abs(np.mean(fall_random)) < 0.0005,
      "l14 screens[2]/[3]: the best of 12 in-sample cells is partly the luckiest, so its held-out share falls below 1 (ledger l14 screens[3].explain)")
check(len(range(0, 1135, 126)) == 10 and len(range(1260, 2647, 126)) == 12, "l14 screens[0]: 10 cycles end by day 1,512 and 12 start trading on or after it")
check(abs(0.55 / 1.97 - 0.2792) < 5e-3, "l14 screens[2]: 28% survived for the tuned setting")
# survival line: zero or below reads none; a zero in-sample effect is undefined
def survival(pre, post):
    if pre <= 0:
        raise ValueError
    r = post / pre
    return "none" if r <= 0 else round(100 * r)
check(survival(0.0114, 0.0048) == 42 and survival(0.01, -0.0005) == "none" and survival(0.0043, 0.0045) == 105,
      "l15 screens[8]: the survival line (ledger l15 screens[8])")

print()
print(f"{len(FAILS)} failing check(s)")
for f_ in FAILS:
    print(" -", f_)
raise SystemExit(1 if FAILS else 0)
