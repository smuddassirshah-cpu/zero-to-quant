"""Fix-pass read, markets levels 1 to 3 (content commit ead4b0b6): every changed number, two ways.

Exits 0 when the content is right. Check 7 fails on purpose while l4 q-different-rates keeps
a key that its own new premise contradicts (see docs/reviews/audit-markets-1-3.md, Fix-pass read).
Run: python docs/reports/markets-L1-3-fixread.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, "..", "..", "app", "content", "courses", "markets")
fails = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (" | " + detail if detail else ""))
    if not cond:
        fails.append(name)


def bond(face, c, n, y):
    return sum(face * c / (1 + y) ** t for t in range(1, n + 1)) + face / (1 + y) ** n


def bond_closed(face, c, n, y):
    d = (1 + y) ** -n
    return face * c * (1 - d) / y + face * d


# 1. l5 screens/3 explain: the half-yearly bond as an annual bond paying 4.05 at 5.0625%.
semi = bond(100, 0.02, 10, 0.025)
semi2 = bond_closed(100, 0.02, 10, 0.025)
ann = bond(100, 0.0405, 5, 1.025 ** 2 - 1)
check("l5 half-yearly price 95.62 two ways", abs(semi - semi2) < 1e-9 and round(semi, 2) == 95.62, f"{semi:.4f}")
check("l5 coupons 17.50 and face 78.12", round(2 * (1 - 1.025 ** -10) / 0.025, 2) == 17.50 and round(100 / 1.025 ** 10, 2) == 78.12)
check("l5 identity: annual 4.05 at 1.025^2 - 1 gives the same price", abs(ann - semi) < 1e-9, f"{ann:.6f}")
check("l5 year-end worth of two coupons is 4.05; yield rounds to 5.06%", abs(2 * 1.025 + 2 - 4.05) < 1e-12 and round((1.025 ** 2 - 1) * 100, 2) == 5.06)
check("l5 coupon shortfall wider: 5.0625 - 4.05 > 5 - 4", (5.0625 - 4.05) > (5 - 4))
check("l5 further below par than 95.67", semi < bond(100, 0.04, 5, 0.05) and round(bond(100, 0.04, 5, 0.05), 2) == 95.67)

# 2. l5 and l8 feedback numbers.
check("l5 test-2 par", abs(bond(100, 0.04, 5, 0.04) - 100) < 1e-9)
check("l5 test-3 zero 61.39", round(100 / 1.05 ** 10, 2) == 61.39 and abs(bond(100, 0, 10, 0.05) - 100 / 1.05 ** 10) < 1e-9)
g = 1.12 * 0.92 * 1.15
check("l8 test-1 growth 1.18496, root 0.0582, mean 6.33%", abs(g - 1.18496) < 1e-12 and round(g ** (1 / 3) - 1, 4) == 0.0582
      and round(math.exp(math.log(g) / 3) - 1, 4) == 0.0582 and round((0.12 - 0.08 + 0.15) / 3 * 100, 2) == 6.33)
check("l8 test-2 -0.134", round(0.75 ** 0.5 - 1, 3) == -0.134 and round(math.sqrt(1.5 * 0.5) - 1, 3) == -0.134)
check("l8 test-6 growth 0 gives -1", (0.0 * 1.5) ** 0.5 - 1 == -1.0)
try:
    math.log(0)
    raised = False
except ValueError:
    raised = True
check("l8 test-6 math.log(0) raises", raised)

# 3. l6 screens/7 explain.
p5, p6 = bond(100, 0.04, 5, 0.05), bond(100, 0.04, 5, 0.06)
check("l6 91.58 and loss 4.10", round(p6, 2) == 91.58 and round(p5 - p6, 2) == 4.10 and round(bond_closed(100, 0.04, 5, 0.06), 2) == 91.58)
# held to maturity: money-weighted return on 95.67 is the 5% purchase yield (bisection on the cash flows)
lo, hi = 0.0, 0.2
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if bond(100, 0.04, 5, mid) > p5 else (lo, mid)
# realised compound return if coupons are reinvested at the new 6%
fv = sum(4 * 1.06 ** (5 - t) for t in range(1, 6)) + 100
real = (fv / p5) ** 0.2 - 1
check("l6 about 5% a year on 95.67", abs(lo - 0.05) < 1e-9 and 0.05 < real < 0.052, f"irr {lo:.4f}, reinvested at 6% {real:.4f}")

# 4. l13 screens/7 and review-3 r-margin-loan: the call level, two ways.
for loan, m, key in ((10000, 0.25, 13333.33), (18000, 0.30, 25714.29)):
    v = loan / (1 - m)
    lo, hi = loan, 3 * loan  # equity share (V - loan) / V rises with V
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (mid - loan) / mid < m else (lo, mid)
    check(f"margin call level {key}", round(v, 2) == key and abs(lo - v) < 1e-6)
    check(f"just below {key} equity is under the maintenance share, at it no call", ((v - 1) - loan) / (v - 1) < m and abs((v - loan) / v - m) < 1e-12)
check("l13 a fall of a third", abs(1 - (10000 / 0.75) / 20000 - 1 / 3) < 1e-12)

# 5. homework-3 h-two-calls: key and the renamed slip `end`.
settles = [8000, 7900, 7820, 7850, 7700, 7640]
N, PT, INIT, MAINT = 2, 10.0, 6000.0, 4500.0


def week(level, restore):
    bal, paid, closes = N * INIT, 0.0, []
    for a, b in zip(settles, settles[1:]):
        bal += N * PT * (b - a)
        closes.append(bal)
        if bal < level:
            paid += restore - bal
            bal = restore
    return paid, closes


paid, closes = week(N * MAINT, N * INIT)
check("hw3 key 7200, calls after days 2 and 5 at 8400", paid == 7200 and closes[1] == 8400 and closes[4] == 8400, str(closes))
end_paid, end_closes = week(MAINT, N * INIT)  # the slip: one contract's maintenance
check("hw3 slip end = 0: balance never under 4500", end_paid == 0 and min(end_closes) == 4800, str(end_closes))
# second way: with no call the balance is 12000 + 20 x (settle - 8000); its low is at 7640
low = N * INIT + N * PT * (min(settles) - settles[0])
check("hw3 slip end second way: low 4800 > 4500, day 2 at 8400 < 9000", low == 4800 > MAINT and N * INIT + N * PT * (7820 - 8000) == 8400 < N * MAINT)
check("hw3 slip maint 4200 and one 3600 unchanged", week(N * MAINT, N * MAINT)[0] == 4200 and (N * INIT - closes[1]) == 3600)
hw = json.load(open(os.path.join(COURSE, "homework-3.json")))
item = next(i for i in hw["items"] if i.get("id") == "h-two-calls")
check("hw3 committed slip end value is 0", next(w for w in item["widget"]["wrong"] if w["id"] == "end")["value"] == 0)

# 6. homework-3 h-airline-hedge: the buy-and-store bound.
F = 600 * 1.05 + 12
check("hw3 forward bound 642, arbitrage above it 18", abs(F - 642) < 1e-9 and abs(660 - 600 * 1.05 - 12 - 18) < 1e-9)
check("hw3 totals 6,420,000 either way", all(abs(10000 * (s - F) * -1 + 10000 * s - 6420000) < 1e-6 for s in (570, 700)))
# a forward below 642 leaves no cash-and-carry profit for anyone who does not already hold fuel:
check("hw3 below the bound: buy-store-sell-forward loses", 620 - F < 0)

# 7. l4 quiz q-irr-bracket and q-different-rates.
check("l4 interpolation 9.23%", round(0.08 + 0.02 * 40 / 65, 4) == 0.0923)


def npv(r, flows):
    return sum(c / (1 + r) ** t for t, c in enumerate(flows))


# conventional flows: NPV strictly falls with the rate (grid check on two streams)
for flows in ([-1000, 0, 0, 1331], [-1000, 800, 300, 100]):
    vals = [npv(k / 1000, flows) for k in range(0, 301)]
    check(f"l4 NPV falls with the rate for {flows}", all(a > b for a, b in zip(vals, vals[1:])))
# non-conventional: NPV can rise with the rate (Brealey-Myers-Allen ch. 5, borrowing and mixed-sign streams)
check("l4 non-conventional stream rises", npv(0.10, [1000, -1100]) > npv(0.05, [1000, -1100]))
# q-different-rates as committed: A 50 at 6%, B 70 at 9%, both conventional.
# Monotone NPV gives B(r) >= 70 > 50 >= A(r) on 6% <= r <= 9%, so "nothing yet" is false there.
q = json.load(open(os.path.join(COURSE, "l4-npv.json")))
prose = next(x for x in q["quiz"] if x["id"] == "q-different-rates")["prose"]
committed_forced = "£50.00 at 6%" in prose and "£70.00 at 9%" in prose and "outlay today followed by inflows" in prose
# with the rates swapped (A 50 at 9%, B 70 at 6%) either ranking is possible at a shared rate:


def scale_to(flows_in, r, target):  # outlay chosen so that NPV at r is the target
    pv = sum(c / (1 + r) ** t for t, c in enumerate(flows_in, start=1))
    return [-(pv - target)] + list(flows_in)


A_long = scale_to([0, 0, 0, 0, 0, 0, 0, 0, 0, 3000], 0.09, 50)   # late cash: gains a lot at 6%
A_short = scale_to([300], 0.09, 50)                                   # early cash: gains little at 6%
B = scale_to([400, 400, 400], 0.06, 70)
check("swapped rates: A can win at 6%", abs(npv(0.09, A_long) - 50) < 1e-9 and npv(0.06, A_long) > npv(0.06, B))
check("swapped rates: B can win at 6%", abs(npv(0.09, A_short) - 50) < 1e-9 and npv(0.06, A_short) < npv(0.06, B))
check("l4 q-different-rates: the key 'nothing yet' is not contradicted by the premise", not committed_forced,
      "A 50 at 6% and B 70 at 9% with conventional flows force B > A at every shared rate from 6% to 9%")

# 8. l3 screens/9 (number unchanged; label reworded).
check("l3 920.50", round(20000 * ((1 + 0.045 / 365) ** 365 - 1), 2) == 920.50)

print("failures:", len(fails))
sys.exit(1 if fails else 0)
