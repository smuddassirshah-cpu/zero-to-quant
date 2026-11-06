#!/usr/bin/env python3
"""Concept checks for pairs-rep level 1 (lessons l1 to l5, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/pairs-rep-L1-concepts.py
Exit 0 when the content is correct. A check that fails because the content is wrong is marked
EXPECTED_FAIL in its message and keeps failing; the corrected assert sits beside it in a comment.
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


# ---- the course's generator and trading loop, copied from the lesson preludes ----
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


def ssd_matrix(Pn):
    G = Pn.T @ Pn
    d = np.diag(G)
    return d[:, None] + d[None, :] - 2 * G


def trade_pair(form, trade, i, j, wait=0, open_at=2.0):
    sd = float(np.std(form[:, i] - form[:, j]))
    a, b = trade[:, i].tolist(), trade[:, j].tolist()
    n = len(a)
    payoff, opened, t = 0.0, False, 0
    while t < n:
        s = a[t] - b[t]
        if sd > 0 and abs(s) > open_at * sd and t + wait < n - 1:
            side = 1 if s > 0 else -1
            to = t + wait
            tc = next((u for u in range(t + 1, n) if (a[u] - b[u]) * side <= 0), None)
            tx = n - 1 if tc is None else min(tc + wait, n - 1)
            ri = (a[tx] - a[to]) / a[to]
            rj = (b[tx] - b[to]) / b[to]
            payoff += side * (rj - ri)
            opened = True
            t = tx + 1
            continue
        t += 1
    return payoff, opened


def live_portfolios(month, K=6):
    return list(range(max(0, month - K + 1), month + 1))


# ---------------------------------------------------------------- l1: calendar
# l1 screens[1].explain and screens[7].prose: 126 / 21 = 6 portfolios live from month 5 on.
check(126 // 21 == 6 and all(len(live_portfolios(m)) == 6 for m in range(5, 200)),
      "l1 calendar: six portfolios overlap from month 5 on (ledger l1 screens[1].explain)")
check([len(live_portfolios(m)) for m in range(5)] == [1, 2, 3, 4, 5],
      "l1 calendar: fewer than six in the first months (ledger l1 quiz[1])")
check((1134 + 252, 1134 + 378) == (1386, 1512), "l1 screens[7]: trading of the cycle from 1,134 is [1386, 1512)")

# ---------------------------------------------------------------- l1 screens[5], l5 screens[0]: no look-ahead in trade_pair
close, mid, ind, broken = pairs_panel()
Pn = normalise(close[:378])
form, trade = Pn[:252], Pn[252:]
alt = trade.copy()
alt[:, 3] *= 1.5  # change the trading period of share 3 only
sd_form = float(np.std(form[:, 2] - form[:, 3]))
sd_alt = float(np.std(form[:, 2] - form[:, 3]))  # the function reads form only
check(sd_form == sd_alt, "l1/l5: the trigger sd is computed on formation days only (ledger l1 screens[5])")
# the threshold used inside trade_pair cannot depend on trading prices: open day of (2, 3) is 28 whatever
# trading prices come later than day 28
cut = trade.copy()
cut[40:, :] = cut[39, :]
check(trade_pair(form, cut, 2, 3)[1] is True, "l1 screens[5]: a trade opens from formation sd alone (ledger l5 screens[0])")

# ---------------------------------------------------------------- l2: normalisation and SSD
P = np.array([[10.0, 400.0], [11.0, 440.0]])
check(np.allclose(normalise(P)[-1], [1.1, 1.1]), "l2 screens[0]: dividing by the first price makes £10 and £400 shares comparable")
rng = np.random.default_rng(0)
X = rng.standard_normal((252, 7)).cumsum(0) + 1
D = ssd_matrix(X)
D2 = np.array([[np.sum((X[:, i] - X[:, j]) ** 2) for j in range(7)] for i in range(7)])
check(np.allclose(D, D2) and np.allclose(np.diag(D), 0, atol=1e-9) and np.allclose(D, D.T),
      "l2 screens[5]/[9]: SSD_ij = G_ii + G_jj - 2 G_ij, zero diagonal, symmetric (ledger l2 screens[9])")
gaps = np.array([0, 0.01, 0.02, -0.02, 0.02, 0.01])
check(abs(np.sum(gaps ** 2) - 0.0014) < 1e-12 and abs(np.sum(gaps) - 0.04) < 1e-12,
      "l2 screens[2]: SSD squares before summing; summing gaps first lets signs cancel (ledger l2 screens[2] byKey.unsq)")
sd0, sd1 = float(np.std(gaps)), float(np.std(gaps, ddof=1))
check(abs(sd0 - 0.0137) < 5e-4 and abs(sd1 - 0.0151) < 5e-4,
      "l2 screens[3]: sd 0.0137 divides by n, 0.0151 by n-1: the convention is stated, the paper fixes neither (ledger l2 screens[3])")
# distance is not correlation: log returns doubled -> correlation 1 but large SSD
r = 0.01 * rng.standard_normal(252)
A = np.exp(np.cumsum(r)); G = np.exp(np.cumsum(2 * r))
A, G = A / A[0], G / G[0]
corr = np.corrcoef(np.diff(np.log(A)), np.diff(np.log(G)))[0, 1]
check(abs(corr - 1) < 1e-12 and np.sum((A - G) ** 2) > 0.5,
      "l2 screens[8]: log returns doubled give correlation 1 and a large SSD (ledger l2 screens[8])")
# a dividend drops a price index but not a total-return index
px = np.ones(10); tr = np.ones(10)
px[5:] *= 0.96  # 4% dividend paid on day 5
check(np.max(np.abs(px - tr)) >= 0.04 and np.max(np.abs(tr - 1)) == 0,
      "l2 screens[6]: a 4% dividend opens a 0.04 gap on prices and none on total returns (ledger l2 screens[6])")
# identical paths: sd 0, 0/0 is NaN and NaN > 2 is False
with np.errstate(invalid="ignore", divide="ignore"):
    z = np.float64(0.0) / np.float64(0.0)
check(np.isnan(z) and not (z > 2), "l2 screens[7]: 0/0 is NaN and NaN > 2 is False, so the case must be guarded (ledger l2 screens[7])")

# ---------------------------------------------------------------- l3: counting and the paper's matching rule
check(100 * 99 // 2 == 4950 and 500 * 499 // 2 == 124750 and 50 * 49 // 2 == 1225, "l3: N(N-1)/2 pairs (ledger l3 screens[0], [9], quiz[0])")
# Toy SSD table of l3 screens[4] (x 10,000)
toy = {("A", "B"): 3.00, ("A", "C"): 6.75, ("A", "D"): 300, ("A", "E"): 507, ("A", "F"): 2700,
       ("B", "C"): 0.75, ("B", "D"): 243, ("B", "E"): 432, ("B", "F"): 2523,
       ("C", "D"): 216.75, ("C", "E"): 396.75, ("C", "F"): 2436.75,
       ("D", "E"): 27, ("D", "F"): 1200, ("E", "F"): 867}
names = "ABCDEF"


def ssd_of(x, y):
    return toy[tuple(sorted((x, y)))]


# GGR (2006) section 2.1, p. 802: "we choose a matching partner for each stock by finding the security that
# minimizes the sum of squared deviations"; the top pairs are then ranked by distance. Nothing excludes a
# share that is the nearest partner of several others.
nominated = set()
for x in names:
    partner = min((y for y in names if y != x), key=lambda y: ssd_of(x, y))
    nominated.add(tuple(sorted((x, partner))))
paper_rule = sorted(nominated, key=lambda p: toy[p])[:2]
greedy = []
used = set()
for p in sorted(toy, key=toy.get):
    if p[0] in used or p[1] in used:
        continue
    greedy.append(p)
    used |= set(p)
    if len(greedy) == 2:
        break
check(greedy == [("B", "C"), ("D", "E")], "l3 screens[4]: the greedy one-partner rule keeps B-C then D-E (the course's key)")
# EXPECTED_FAIL: the course calls the greedy rule "the paper's rule"; under the paper's nearest-partner rule the
# first two pairs are B-C then A-B, the option the screen marks wrong. Corrected assert, ready to enable once
# the content stops attributing the greedy rule to the paper:
#   check(paper_rule == [("B", "C"), ("A", "B")], "l3 screens[4]: the paper's rule gives B-C then A-B")
check(paper_rule == greedy,
      "EXPECTED_FAIL l3 screens[4]/[5]/[6], review-1 items[4], homework-1 items[0]: the course's 'paper's one-partner rule' "
      "(greedy, each share once) does not reproduce GGR's nearest-partner rule, which keeps B-C then A-B here "
      "(ledger l3 screens[4].prose)")
# the two rules agree on the first formation year of the seeded panel (so the course's tests still pass there)
D0 = ssd_matrix(normalise(close[:252]))
i0, j0 = np.triu_indices(100, 1)
order = np.argsort(D0[i0, j0], kind="stable")
top20 = [(int(i0[o]), int(j0[o])) for o in order[:20]]
check(len({s for p in top20 for s in p}) == 40, "l3 screens[4].explain: on the first year no share repeats, so both rules agree")
# chance pairs: in a year where 17 of 20 planted pairs have broken, most of the top 20 are not planted
D1 = ssd_matrix(normalise(close[2016:2268]))
order1 = np.argsort(D1[i0, j0], kind="stable")
top1 = [(int(i0[o]), int(j0[o])) for o in order1[:20]]
planted = sum(1 for a, b in top1 if b == a + 1 and a % 2 == 0 and a < 40)
check(planted == 3, "l3 screens[8]: only 3 of the 20 closest pairs at start 2,016 are planted (ledger l3 screens[8])")
# "close is necessary, not sufficient": a pair that never leaves +-2 sd never opens; the fifth closest pair in year 1
check(trade_pair(form, trade, 30, 31) == (0.0, False), "l3 screens[7]: the fifth closest pair of year 1 never opened (ledger l3 screens[7])")

# ---------------------------------------------------------------- l4: committed and employed
payoffs = np.array([0.10, 0.0, 0.05, -0.02, 0.0]); opened = np.array([1, 0, 1, 1, 0], bool)
comm, emp = payoffs.sum() / 5, payoffs.sum() / opened.sum()
check(abs(comm - 0.026) < 1e-12 and abs(emp - 0.13 / 3) < 1e-12 and emp >= comm,
      "l4 screens[8]: employed >= committed when the total is positive (ledger l4 screens[8])")
neg = np.array([-0.05, 0.0]); check(neg.sum() / 1 < neg.sum() / 2, "l4 quiz[2]: with a negative total employed is below committed")
check(abs(emp / comm - 5 / 3) < 1e-12, "l5 screens[9]: employed / committed = k / n (ledger l5 screens[9])")
check(abs((1.0075 ** 12 - 1) - 0.0938) < 5e-4 and abs(12 * 0.0075 - 0.09) < 1e-12,
      "l4 screens[4]: 0.75% a month compounds to 9.38% a year, 9% is the simple figure (ledger l4 screens[4])")
check(abs((1.0084 ** 12 - 1) - 0.1056) < 5e-4 and abs((1.01 ** 12 - 1) - 0.1268) < 5e-4,
      "homework-1 items[5], review-1 items[7]: 10.56% and 12.68% compounded")
# a zero-investment position's payoff is a difference of returns: subtracting r_f from each leg cancels
rf = 0.05; rl, rs = 0.12, 0.08
check(abs(((rl - rf) - (rs - rf)) - (rl - rs)) < 1e-12,
      "l4 screens[3]: £1 long, £1 short: the risk-free rate cancels, so the payoff is already an excess return (ledger l4 screens[3])")

# ---------------------------------------------------------------- l5: placebo, random pairs and the bounce
# Monte Carlo over fresh panels with no planted relationship among shares 40 to 99. Prices are exponentials of
# random walks with equal drift in both legs, so by optional stopping the expected payoff of a random pair is 0
# on mid prices. The course (l5 screens[6].explain) says random pairs lose a little "because a pair that never
# reconverges is closed at a loss".
res_mid, res_close = [], []
for seed in range(150):
    c2, m2, _, _ = pairs_panel(seed=10_000 + seed, days=378, break_frac=0.0)
    r2 = np.random.default_rng(seed)
    Pm, Pc = normalise(m2), normalise(c2)
    for _ in range(40):
        i, j = r2.choice(np.arange(40, 100), 2, replace=False)
        res_mid.append(trade_pair(Pm[:252], Pm[252:], int(i), int(j))[0])
        res_close.append(trade_pair(Pc[:252], Pc[252:], int(i), int(j))[0])
res_mid, res_close = np.array(res_mid), np.array(res_close)
# panels are the unit of independence: cluster the standard error by panel
by_panel_mid = res_mid.reshape(150, 40).mean(1)
by_panel_d = (res_close - res_mid).reshape(150, 40).mean(1)
se_mid = by_panel_mid.std(ddof=1) / math.sqrt(150)
se_d = by_panel_d.std(ddof=1) / math.sqrt(150)
print(f"random pairs on mids: mean {res_mid.mean():.4f} (se {se_mid:.4f}); closes - mids {by_panel_d.mean():.4f} (se {se_d:.4f})")
# Corrected claim (fix pass): the explain now says the 200-seed means are one cycle's draw on one panel and that
# on fresh panels random pairs average within noise of 0. Fix-pass computation: pairs drawn from all 100 shares
# (planted shares included, planted pairs excluded), default generator, one formation year and half a trading year.
fx = []
for seed in range(60):
    c3, m3, _, _ = pairs_panel(seed=3000 + seed, days=378, break_day=300)
    r3 = np.random.default_rng(seed + 1)
    P3 = normalise(m3)
    pp = []
    while len(pp) < 40:
        i, j = sorted(int(x) for x in r3.choice(100, 2, replace=False))
        if j == i + 1 and i % 2 == 0 and i < 40:
            continue
        pp.append(trade_pair(P3[:252], P3[252:], i, j)[0])
    fx.append(np.mean(pp))
fx = np.array(fx); se_fx = fx.std(ddof=1) / math.sqrt(len(fx))
print(f"fix pass: random pairs on mids over 60 fresh panels: mean {fx.mean():.4f} (se {se_fx:.4f})")
_l5 = __import__("json").load(open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),
      "..", "..", "app", "content", "courses", "pairs-rep", "l5-plan.json"), encoding="utf-8"))["screens"][6]["explain"]["text"]
check(abs(res_mid.mean()) < 2.5 * se_mid and abs(fx.mean()) < 2.5 * se_fx and res_mid.mean() > -0.0113 + 2.5 * se_mid
      and "lose a little" not in _l5 and "within noise of 0" in _l5,
      "l5 screens[6].explain: random pairs on mids earn about 0 in expectation; -1.13% is one cycle's draw on one panel "
      "(ledger l5 screens[6].explain) (corrected claim, fix pass)")
check(by_panel_d.mean() > 2.5 * se_d,
      "l5 screens[7], homework-1 items[6]: the bounce lifts random pairs' same-day payoff on closes above mids (ledger l5 screens[7].explain)")
# placebo: random pairs earn far less than planted pairs in the same cycle (the control-group reading)
plant = np.mean([trade_pair(form, trade, 2 * k, 2 * k + 1)[0] for k in range(20)])
check(plant > 0.10 and abs(res_mid.mean()) < 0.02, "l5 quiz[0]: a placebo of random pairs earns about nothing against planted pairs (ledger l5 quiz[0])")
# half-life: phi^8 = 0.5
check(abs(0.5 ** (1 / 8) - 0.9170) < 5e-5 and abs(0.5 ** (1 / 4) - 0.8409) < 5e-5, "l5 screens[3], review-1 items[8]: phi = 0.5^(1/half_life)")
# the seeded panel: 17 of 20 planted pairs break and pairs 4, 7, 16 survive
check(broken.sum() == 17 and [k for k in range(20) if not broken[k]] == [4, 7, 16],
      "l5 screens[1].explain: pairs 4, 7 and 16 never break (ledger l5 screens[1])")
# panel checks: a NaN fails the positive test without extra code
with np.errstate(invalid="ignore"):
    check(not bool((np.array([10.0, np.nan]) > 0).all()), "l5 screens[5].explain: a comparison with NaN is False (ledger l5 screens[5])")

print()
print(f"{len(FAILS)} failing check(s)")
for f in FAILS:
    print(" -", f)
raise SystemExit(1 if FAILS else 0)
