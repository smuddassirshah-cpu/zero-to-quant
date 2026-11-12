#!/usr/bin/env python3
"""Concept checks for micro L1 to L3, round 2 blind audit.

Each check tests a claim the content makes, by simulation, by a grid search or
by recomputing a graded key from the item's own data. Exit 0 means every claim
checked here holds. Run: python3 docs/reports/micro-L1-3-r2-concepts.py
(CPython 3; standard library only.)
"""
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "app" / "content" / "courses" / "micro"
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))
    if not ok:
        FAILS.append(name)


def load(name):
    return json.loads((ROOT / (name + ".json")).read_text())


def walk(levels, size):
    left, paid = size, 0.0
    for price, shares in levels:
        take = min(left, shares)
        paid += take * price
        left -= take
        if left == 0:
            break
    assert left == 0
    return paid


# ---------------------------------------------------------------- L1 keys
l2 = load("l2-walking-the-book")
asks = l2["screens"][0]["canvas"]["params"]["asks"]
bids = l2["screens"][0]["canvas"]["params"]["bids"]
mid = (asks[0][0] + bids[0][0]) / 2
paid = walk(asks, 1500)
check("l2 average fill 1,500 is 100.1587", abs(paid / 1500 - l2["screens"][3]["widget"]["answer"]) < 1e-4)
check("l2 slippage v best ask 1.87p", abs((paid / 1500 - asks[0][0]) * 100 - l2["screens"][4]["widget"]["answer"]) < 0.01)
check("l2 cost v mid £58", abs(paid - 1500 * mid - l2["screens"][5]["widget"]["answer"]) < 0.01)
thin = l2["screens"][10]["canvas"]["params"]["asks"]
check("l2 thin share £1,800 over mid", abs(walk(thin, 10000) - 1e6 - l2["screens"][10]["widget"]["answer"]) < 0.01)

l1 = load("l1-bids-and-asks")
p = l1["screens"][5]["canvas"]["params"]
s_bp = (p["asks"][0][0] - p["bids"][0][0]) / ((p["asks"][0][0] + p["bids"][0][0]) / 2) * 1e4
check("l1 spread 4.0 bp", abs(s_bp - l1["screens"][5]["widget"]["answer"]) < 0.05, "%.3f" % s_bp)

# l4 fill-chance model: expected cost by ticks below the ask, as the canvas derives it
ec = {}
for k in range(11):
    pf = max(0.0, min(1.0, 1 - 0.1 * k))
    ec[k] = pf * (2 - k) + (1 - pf) * 3
check("l4 model: 2.0p at the ask, 0.0p at 4 and 5 ticks, 1.2p at 8, 3.0p at 10",
      abs(ec[0] - 2) < 1e-9 and abs(ec[4]) < 1e-9 and abs(ec[5]) < 1e-9
      and abs(ec[8] - 1.2) < 1e-9 and abs(ec[10] - 3) < 1e-9 and min(ec.values()) > -1e-9)

# l4 break-even p = c / (2h + c), and with adverse selection c / (2h + c - a)
ok = True
for h, c, a in [(2, 1, 0), (5, 2, 0), (2, 1, 2), (3, 4, 1)]:
    pstar = c / (2 * h + c - a)
    for eps in (-1e-3, 1e-3):
        pp = pstar + eps
        limit = pp * (a - h) + (1 - pp) * (h + c)
        ok &= (limit < h) == (eps > 0)
check("l4 / hw1 break-even fill chance c/(2h+c-a)", ok)

# ---------------------------------------------------------------- L2 keys and claims
l6 = load("l6-impact")
a6 = l6["screens"][0]["canvas"]["params"]["asks"]
check("l6 2,500 shares average 10.016", abs(walk(a6, 2500) / 2500 - 10.016) < 1e-9)
check("l6 4,500 shares slippage £100", abs(walk(a6, 4500) - 45000 - 100) < 1e-6)
check("l6 10,000 shares cost 35 bp", abs((walk(a6, 10000) - 1e5) / 1e5 * 1e4 - 35) < 1e-6)
check("l6 sqrt model: 20, 40, 63.2 bp", all(abs(0.02 * math.sqrt(x) * 1e4 - y) < 0.05
      for x, y in [(0.01, 20), (0.04, 40), (0.1, 63.2)]))
tot = {n: 50 / n + 2 * n for n in range(1, 13)}
check("l6 slices: minimum at n = 5, 20 bp", min(tot, key=tot.get) == 5 and abs(tot[5] - 20) < 1e-9)
tot = {n: 72 / n + 2 * n for n in range(1, 40)}
check("hw2 slices: minimum at n = 6, 24 bp", min(tot, key=tot.get) == 6 and abs(tot[6] - 24) < 1e-9)
ser = l6["screens"][6]["canvas"]["params"]["series"][0]["values"]
check("l6 impact series: peak 10.06 at minute 15, settles 10.03", max(ser) == 10.06 and ser[15] == 10.06 and ser[-1] == 10.03)

# hw2 longform: timing risk of a three-day schedule, sd of cost about £134,000
rng = random.Random(11)
xs = []
for _ in range(200000):
    r1, r2 = rng.gauss(0, 0.018), rng.gauss(0, 0.018)
    xs.append(1e7 * (2 / 3 * r1 + 1 / 3 * r2))
m = sum(xs) / len(xs)
sd = math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))
check("hw2 timing risk sd about £134,000", abs(sd - 134164) < 1500, "%.0f" % sd)

# l7 claim: in a one-tick book the microprice predicts the mid after its next
# move better than the mid does, and the sign of the imbalance calls the move.
def one_tick_race(rng, add_cancel):
    qb, qa = rng.randint(1, 20), rng.randint(1, 20)
    imb = (qb - qa) / (qb + qa)
    while qb > 0 and qa > 0:
        u = rng.random()
        if add_cancel:
            # market order, cancel or new limit order, each side equally likely
            if u < 0.25:
                qa -= 1
            elif u < 0.5:
                qb -= 1
            elif u < 0.625:
                qa -= 1
            elif u < 0.75:
                qb -= 1
            elif u < 0.875:
                qa += 1
            else:
                qb += 1
        else:
            if u < 0.5:
                qa -= 1
            else:
                qb -= 1
    return imb, (1 if qa == 0 else -1)


for label, ac in (("market orders only", False), ("with adds and cancels", True)):
    rng = random.Random(5)
    n = 100000
    se_mid = se_mu = hits = decided = 0
    for _ in range(n):
        imb, move = one_tick_race(rng, ac)
        # units of half a tick: next mid = m + move, microprice = m + imb, mid = m
        se_mid += move ** 2
        se_mu += (move - imb) ** 2
        if imb != 0:
            decided += 1
            hits += (move > 0) == (imb > 0)
    check("l7 microprice beats mid as predictor, one-tick book (%s)" % label,
          se_mu < 0.9 * se_mid, "MSE %.3f v %.3f half-ticks^2" % (se_mu / n, se_mid / n))
    check("l7 imbalance sign calls the next move (%s)" % label,
          hits / decided > 0.6, "hit rate %.3f" % (hits / decided))

l7 = load("l7-where-is-the-price")
# code-behaviour note: an empty side fails on indexing, not on division
try:
    [][0]
    kind = "none"
except IndexError:
    kind = "IndexError"
print("INFO l7 screens[9] explain says 'Dividing would then crash': without the guard the "
      "first failure on an empty side is " + kind + " at asks[0], not a division")

# l8 keys
l8 = load("l8-liquidity")
la = l8["screens"][0]["canvas"]["left"]["params"]
lb = l8["screens"][0]["canvas"]["right"]["params"]
mida = (la["asks"][0][0] + la["bids"][0][0]) / 2
midb = (lb["asks"][0][0] + lb["bids"][0][0]) / 2
check("l8 both mids 100.005", abs(mida - 100.005) < 1e-9 and abs(midb - 100.005) < 1e-9)
check("l8 book A £143, book B £30", abs(walk(la["asks"], 2000) - 2000 * mida - 143) < 1e-6
      and abs(walk(lb["asks"], 2000) - 2000 * midb - 30) < 1e-6)
check("l8 X about 90 bp, Y about 17 bp", abs(0.02 * math.sqrt(0.2) * 1e4 + 1 - 90.4) < 0.1
      and abs(0.02 * math.sqrt(0.005) * 1e4 + 3 - 17.1) < 0.1)

# ---------------------------------------------------------------- L3 claims
# l9: profit 2 s lam0 exp(-k s) peaks at 1/k; with informed flow at alpha*delta + 1/k
ok = True
for k, ad in [(0.5, 0), (0.25, 0), (1 / 3, 0), (0.5, 2)]:
    grid = [i / 1000 for i in range(0, 20001)]
    best = max(grid, key=lambda s: 2 * 10 * math.exp(-k * s) * (s - ad))
    ok &= abs(best - (ad + 1 / k)) < 2e-3
check("l9 / hw3 optimum half-spread 1/k, and alpha*delta + 1/k", ok)

# l10: inventory of an unskewed maker is a random walk; a skewed one mean-reverts
l10 = load("l10-inventory")
flat, skew = [s["values"] for s in l10["screens"][5]["canvas"]["params"]["series"]]
check("l10 chart: 101 points, unit steps", len(flat) == 101 == len(skew)
      and all(abs(a - b) == 1 for a, b in zip(flat, flat[1:]))
      and all(abs(a - b) == 1 for a, b in zip(skew, skew[1:])))
check("l10 chart: no-skew ends at 14 and reaches 18; skew ends at 0 within 3 lots",
      flat[-1] == 14 and max(map(abs, flat)) == 18 and skew[-1] == 0 and max(map(abs, skew)) <= 3,
      "flat max %d, skew max %d" % (max(map(abs, flat)), max(map(abs, skew))))
rng = random.Random(3)
endf, ends, maxs = [], [], []
for _ in range(20000):
    qf = qs = 0
    mx = 0
    for _ in range(100):
        qf += 1 if rng.random() < 0.5 else -1
        psale = 1 / (1 + math.exp(-qs))  # a sale is e^q times as likely as a purchase
        qs += -1 if rng.random() < psale else 1
        mx = max(mx, abs(qs))
    endf.append(qf)
    ends.append(qs)
    maxs.append(mx)
sdf = math.sqrt(sum(x * x for x in endf) / len(endf))
sds = math.sqrt(sum(x * x for x in ends) / len(ends))
check("l10 unskewed inventory sd after 100 trades about 10 lots; skewed stays near 1",
      abs(sdf - 10) < 0.3 and sds < 1.5, "sd %.2f v %.2f" % (sdf, sds))
check("l10 skewed maker rarely passes 3 lots in 100 trades",
      sum(m <= 3 for m in maxs) / len(maxs) > 0.5, "share within 3 lots %.3f" % (sum(m <= 3 for m in maxs) / len(maxs)))

# l11: Glosten-Milgrom quotes by simulation
def gm(rng, alpha, delta, beta=0.5):
    high = rng.random() < 0.5
    if rng.random() < alpha:
        buy = high
    else:
        buy = rng.random() < beta
    return (delta if high else -delta), buy


rng = random.Random(7)
sb = nb = ss = ns = 0
for _ in range(400000):
    d, buy = gm(rng, 0.2, 10)
    if buy:
        sb += d
        nb += 1
    else:
        ss += d
        ns += 1
check("l11 E[V | buy] = V + alpha*delta = 502, E[V | sell] = 498",
      abs(sb / nb - 2) < 0.08 and abs(ss / ns + 2) < 0.08, "%.3f, %.3f" % (sb / nb, ss / ns))

rng = random.Random(8)
acc = {2: [0, 0], 3: [0, 0]}
for _ in range(1500000):
    high = rng.random() < 0.5
    buys = 0
    for i in range(3):
        if rng.random() < 0.2:
            b = high
        else:
            b = rng.random() < 0.5
        if not b:
            break
        buys += 1
        if buys in acc:
            acc[buys][0] += 10 if high else -10
            acc[buys][1] += 1
e2 = 500 + acc[2][0] / acc[2][1]
e3 = 500 + acc[3][0] / acc[3][1]
check("review-3 two buys 503.85, hw3 three buys 505.43",
      abs(e2 - 503.846) < 0.08 and abs(e3 - 505.429) < 0.1, "%.3f, %.3f" % (e2, e3))

rng = random.Random(9)
sb = nb = ss = ns = 0
for _ in range(600000):
    d, buy = gm(rng, 0.2, 21, 0.75)
    if buy:
        sb += d
        nb += 1
    else:
        ss += d
        ns += 1
check("hw3 tilted quotes a = 3p, b = 7p, P(buy) = 0.7",
      abs(sb / nb - 3) < 0.12 and abs(-ss / ns - 7) < 0.15 and abs(nb / (nb + ns) - 0.7) < 0.005,
      "%.3f, %.3f" % (sb / nb, -ss / ns))


def maker_pnl(n, alpha, delta, s, seed):
    rng = random.Random(seed)
    total = 0.0
    for _ in range(n):
        high = rng.random() < 0.5
        informed = rng.random() < alpha
        if informed:
            buys = high
        else:
            buys = rng.random() < 0.5
        d = delta if high else -delta
        total += (s - d) if buys else (s + d)
    return total / n


code = l11 = load("l11-adverse-selection")["screens"][10]["widget"]
ok = True
for t in code["tests"]:
    got = eval(t["call"])
    ok &= math.isclose(got, float(t["expect"]), rel_tol=1e-9)
check("l11 seeded test values reproduce (CPython Mersenne Twister, as in Pyodide)", ok)
check("l11 long-run profit s - alpha*delta = 1p", abs(maker_pnl(400000, 0.2, 10, 3, 123) - 1) < 0.05)

# l12 auctions
def uncross(buys, sells):
    best = key = None
    for p in sorted({p for p, _ in buys} | {p for p, _ in sells}):
        d = sum(q for lim, q in buys if lim >= p)
        s = sum(q for lim, q in sells if lim <= p)
        v = min(d, s)
        if v and (key is None or (v, -abs(d - s)) > key):
            best, key = (p, v), (v, -abs(d - s))
    return best


b1 = [(503, 600), (502, 400), (501, 500), (500, 300), (499, 700)]
s1 = [(499, 300), (500, 400), (501, 500), (502, 600), (503, 400)]
check("l12 first auction 501p, 1,200; with a 300 market buy 502p, 1,300",
      uncross(b1, s1) == (501, 1200) and uncross(b1 + [(10 ** 9, 300)], s1) == (502, 1300))
rows = load("l12-venues")["screens"][3]["canvas"]["params"]["rows"]
b2 = [(int(r[0]), int(r[1])) for r in rows]
s2 = [(int(r[0]), int(r[2])) for r in rows]
check("l12 second auction 250p, 1,000", uncross(b2, s2) == (250, 1000))

print()
print("%d failing check(s)" % len(FAILS))
sys.exit(1 if FAILS else 0)
