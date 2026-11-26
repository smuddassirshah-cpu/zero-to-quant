#!/usr/bin/env python3
"""Blind concept audit, round 2: markets levels 1 to 3 (l1 to l13, review-1..3, homework-1..3).

Recomputes every figure the auditor relied on, checks each slip whose feedback names a mistake
against the value that mistake gives, and runs Monte Carlo checks for the empirical claims.
Exits 0 on correct content. A check that fails because the content is wrong stays failing:
see docs/reviews/audit-markets-1-3-r2.md for the findings behind any FAIL line.

Run from the repository root:  python docs/reports/markets-L1-3-concepts-r2.py
Needs NumPy and SciPy (any recent version; no figure depends on a version).

Fix pass: the two checks that encoded the old text of findings 1 and 2 (the mistake each line named)
are re-pointed to the mistake the fixed line names; each still recomputes the slip's value.
"""
import json
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "markets")
FAILS = []
N = 0


def load(name):
    with open(os.path.join(ROOT, name + ".json")) as f:
        return json.load(f)


def ck(label, got, want, tol=0.006):
    """got: recomputed value; want: the value the content states."""
    global N
    N += 1
    ok = abs(got - want) <= tol
    if not ok:
        FAILS.append(label)
    print(("ok   " if ok else "FAIL ") + f"{label}: computed {got:.6g}, content {want:.6g}")


def true(label, cond):
    global N
    N += 1
    if not cond:
        FAILS.append(label)
    print(("ok   " if cond else "FAIL ") + label)


def ann(r, n):
    return (1 - (1 + r) ** -n) / r


def bond(c, y, T, F=100.0, f=1):
    n = T * f
    return c / f * ann(y / f, n) + F / (1 + y / f) ** n


def npv(r, flows):
    return sum(c / (1 + r) ** t for t, c in enumerate(flows))


def irr(flows, lo=0.0, hi=1.0):
    return brentq(lambda r: npv(r, flows), lo, hi)


def slip(screen_widget, sid):
    return next(w["value"] for w in screen_widget["wrong"] if w["id"] == sid)


L = {k: load(k) for k in ["l1-interest-on-interest", "l2-present-value", "l3-comparing-rates", "l4-npv",
                           "l5-pricing-a-bond", "l6-yield", "l7-shares", "l8-measuring-returns",
                           "l9-agreeing-today", "l10-cost-of-carry", "l11-margin",
                           "l12-selling-what-you-do-not-own", "l13-leverage",
                           "review-1", "review-2", "review-3", "homework-1", "homework-2", "homework-3"]}
S = lambda k, i: L[k]["screens"][i]["widget"]
Q = lambda k, i: L[k]["quiz"][i]["widget"]
I = lambda k, i: L[k]["items"][i]["widget"]

print("== Level 1: interest, present value, rates, NPV ==")
ck("l1 s0 gap at 10 years", 1000 * 1.05 ** 10 - 1500, S("l1-interest-on-interest", 0)["answer"])
ck("l1 s0 gap at 20 years", 1000 * 1.05 ** 20 - 2000, 653.30)
ck("l1 s3 doubling 5% exact", math.log(2) / math.log(1.05), 14.21)
true("l1 s3 first whole year past double is 15", 1.05 ** 14 < 2 < 1.05 ** 15)
ck("l1 s4 -5% ten years compound", 1000 * 0.95 ** 10, 598.74)
ck("l1 s5 trap", 2000 * 1.06 ** 5, S("l1-interest-on-interest", 5)["answer"])
ck("l1 s7 doubling at 20%", math.log(2) / math.log(1.2), S("l1-interest-on-interest", 7)["answer"], 1e-4)
ck("l1 s7 savings double", math.log(2) / math.log(1.04), 17.67)
true("l1 rule of 72 runs short at 20%, long at 5%", 72 / 20 < math.log(2) / math.log(1.2) and 72 / 5 > math.log(2) / math.log(1.05))
ck("l1 s8 1% a month", 1.01 ** 12 - 1, S("l1-interest-on-interest", 8)["answer"], 1e-6)
ck("l1 q negative rate", 1000 * 0.98 ** 10, Q("l1-interest-on-interest", 0)["answer"])
ck("l1 q rule 72 exact", math.log(2) / math.log(1.08), 9.01)
ck("l1 q simple v compound gap", 1000 * 1.09 ** 20 - 3000, 2604.41)
ck("l1 q total interest", 500 * 1.04 ** 3 - 500, Q("l1-interest-on-interest", 3)["answer"])

ck("l2 s0 900 grown", 900 * 1.05 ** 3, 1041.86)
ck("l2 s1 rate for 750", (1000 / 750) ** (1 / 3) - 1, S("l2-present-value", 1)["answer"], 1e-4)
ck("l2 s1 slip simple", (1000 / 750 - 1) / 3, slip(S("l2-present-value", 1), "simple"), 1e-4)
ck("l2 s3 stream", 400 / 1.05 + 500 / 1.05 ** 2 + 600 / 1.05 ** 3, 1352.77)
ck("l2 s4 slip once", 250 / 1.05 + 1352.77, slip(S("l2-present-value", 4), "once"))
ck("l2 s6 trap", 5000 / 1.06 ** 3, S("l2-present-value", 6)["answer"])
ck("l2 s6 overpricing", 5000 / 1.18 - 5000 / 1.06 ** 3, 39.19)
ck("l2 s9 lottery", 50000 * ann(0.04, 20), 679516.32, 0.01)
ck("l2 q rates rise", 1000 / 1.03 ** 10 - 1000 / 1.06 ** 10, Q("l2-present-value", 1)["answer"])
ck("l2 q rates rise slip simple", 1000 / 1.3 - 1000 / 1.6, slip(Q("l2-present-value", 1), "simple"))
ck("l2 q four years over-pricing", 800 / 1.2 - 800 / 1.05 ** 4, 8.50)

ck("l3 s0 bank B", 1000 * 1.01 ** 12, 1126.83)
ck("l3 s3 monthly to daily gain", 1000 * ((1 + .06 / 365) ** 365 - 1.005 ** 12), 0.15)
ck("l3 s4 continuous 12%", math.exp(0.12) - 1, S("l3-comparing-rates", 4)["answer"], 1e-6)
ck("l3 s4 daily 12% in points", 100 * ((1 + .12 / 365) ** 365 - 1), 12.747, 6e-4)
true("l3 s4 daily within 0.003 points of the ceiling", 100 * (math.exp(.12) - (1 + .12 / 365) ** 365) < 0.003)
ck("l3 s4 cubic term in points", 100 * 0.12 ** 3 / 6, 0.03, 0.002)
ck("l3 s6 monthly for 12% effective", 1.12 ** (1 / 12) - 1, S("l3-comparing-rates", 6)["answer"], 1e-6)
ck("l3 s7 AER monthly 4.8%", 100 * (1.004 ** 12 - 1), 4.91)
ck("l3 s7 continuous 4.8%", 100 * (math.exp(0.048) - 1), 4.92)
ck("l3 s8 extra interest", 200000 * ((1 + .059 / 12) ** 12 - 1 - 0.06), 124.38, 0.02)
ck("l3 s9 daily interest", 20000 * ((1 + .045 / 365) ** 365 - 1), S("l3-comparing-rates", 9)["answer"])
ck("l3 s9 continuous slip", 20000 * (math.exp(.045) - 1), slip(S("l3-comparing-rates", 9), "cont"))
ck("l3 q to quarterly", 4 * (1.1 ** .25 - 1), Q("l3-comparing-rates", 3)["answer"], 1e-6)
ck("l3 q saver quarterly", 100 * (1.0125 ** 4 - 1), 5.09)
true("l3: effective rate rises with m and stays below e^r - 1 (m = 1..10000)",
     all((1 + .12 / m) ** m < (1 + .12 / (m + 1)) ** (m + 1) < math.exp(.12) for m in range(1, 10000)))

ck("l4 s0 payments today", 550 / 1.1 + 550 / 1.21, 954.55)
ck("l4 s1 IRR between 6 and 7", irr([-1000, 550, 550]), 0.065, 0.005)
ck("l4 s2 NPV 8%", npv(.08, [-5000, 2000, 2000, 2000]), 154.19)
ck("l4 s3 IRR", irr([-5000, 2000, 2000, 2000]), S("l4-npv", 3)["answer"], 1e-4)
A, B = [-1000, 0, 0, 1331], [-1000, 800, 300, 100]
ck("l4 s4 A at 4%", npv(.04, A), 183.25); ck("l4 s4 B at 4%", npv(.04, B), 135.50)
ck("l4 s4 A at 8%", npv(.08, A), 56.59); ck("l4 s4 B at 8%", npv(.08, B), 77.33)
x = brentq(lambda r: npv(r, A) - npv(r, B), 0.001, 0.15)
ck("l4 s4 crossover", x, 0.067, 0.0006)
gr = np.linspace(0, 0.15, 3001); d = np.array([npv(r, A) - npv(r, B) for r in gr])
true("l4 s4 curves cross exactly once on [0, 15%]", int(np.sum(np.sign(d[1:]) != np.sign(d[:-1]))) == 1)
ck("l4 s5 trap", 300 * ann(.07, 4) - 1100, S("l4-npv", 5)["answer"])
ck("l4 s5 slip once", 1200 / 1.07 - 1100, slip(S("l4-npv", 5), "once"))
ck("l4 s5 slip last", 1200 / 1.07 ** 4 - 1100, slip(S("l4-npv", 5), "last"))
ck("l4 s8 bond NPV", npv(.05, [-95, 4, 4, 104]), S("l4-npv", 8)["answer"])
ck("l4 s8 bond IRR %", 100 * irr([-95, 4, 4, 104]), 5.87)
ck("l4 s8 slip no principal", npv(.05, [-95, 4, 4, 4]), slip(S("l4-npv", 8), "no-principal"))
ck("l4 s9 feed", npv(.07, [-130000, 50000, 50000, 50000]), 1215.80, 0.01)
ck("l4 s9 feed IRR %", 100 * irr([-130000, 50000, 50000, 50000]), 7.51)
ck("l4 s9 at 8%", npv(.08, [-130000, 50000, 50000, 50000]), -1145.15, 0.01)
# NPV of an outlay followed by inflows is strictly decreasing in r > -1 (derivative is -sum t C_t (1+r)^-(t+1) < 0).
rng = np.random.default_rng(7)
mono = True
for _ in range(2000):
    fl = [-rng.uniform(1, 100)] + list(rng.uniform(0, 50, rng.integers(1, 12)))
    v = [npv(r, fl) for r in np.linspace(0, 0.5, 60)]
    mono &= all(a >= b for a, b in zip(v, v[1:]))
true("l4: NPV of outlay-then-inflows falls as the rate rises (2000 random streams)", mono)
true("l4: a non-conventional stream (-100, 230, -132) has two IRRs, 10% and 20%, so the lesson's premise is needed",
     abs(npv(.10, [-100, 230, -132])) < 1e-9 and abs(npv(.20, [-100, 230, -132])) < 1e-9)
ck("r1 compound six", 5000 * 1.03 ** 6, I("review-1", 0)["answer"])
ck("r1 pv four", 2500 / 1.06 ** 4, I("review-1", 1)["answer"])
ck("r1 npv three", npv(.06, [-800, 300, 300, 300]), I("review-1", 3)["answer"])
ck("r1 pv monthly", 10000 / 1.005 ** 24, I("review-1", 5)["answer"])
RA, RB = [-2000, 0, 2600], [-2000, 1300, 1200]
ck("r1 crossing A 5%", npv(.05, RA), 358.28); ck("r1 crossing B 5%", npv(.05, RB), 326.53)
ck("r1 crossing A 10%", npv(.10, RA), 148.76); ck("r1 crossing B 10%", npv(.10, RB), 173.55)
ck("r1 crossing rate", brentq(lambda r: npv(r, RA) - npv(r, RB), .01, .2), 0.077, 0.0006)
ck("hw1 card", 3000 * 1.018 ** 24, I("homework-1", 0)["answer"])
ck("hw1 card EAR", 1.018 ** 12 - 1, 0.2387, 6e-5)
ck("hw1 three flows", 1000 / 1.05 + 2000 / 1.05 ** 3 + 3000 / 1.05 ** 5, I("homework-1", 1)["answer"], 0.02)
aers = [(1 + .046 / 12) ** 12 - 1, 0.047, math.exp(.0455) - 1, (1 + .0465 / 4) ** 4 - 1]
true("hw1 best AER is the quarterly account, and the four AERs are 4.698, 4.700, 4.655, 4.732",
     max(range(4), key=lambda i: aers[i]) == 3 and all(abs(100 * a - b) < 6e-4 for a, b in zip(aers, [4.698, 4.700, 4.655, 4.732])))
ck("hw1 nominal monthly for 5% AER", 12 * (1.05 ** (1 / 12) - 1), 0.0489, 6e-5)
u = (550 + math.sqrt(550 ** 2 + 4 * 1000 * 550)) / 2000
ck("hw1 quadratic IRR", u - 1, I("homework-1", 6)["answer"], 1e-6)
# FINDING 1 (fixed): the 'simple' line now names 1000(1 + 1.5r) = 1100, the gain over the mean wait of 1.5 years.
ck("hw1 quadratic slip 'simple': root of 1000(1 + 1.5r) = 1100, the mistake its feedback names",
   (1100 / 1000 - 1) / 1.5, slip(I("homework-1", 6), "simple"), 2e-4)
true("hw1 quadratic slip 'simple': its feedback quotes 1000(1 + 1.5r) = 1100",
     "1000(1 + 1.5r) = 1100" in load("homework-1")["items"][6]["feedback"]["byKey"]["simple"])
ck("hw1 quadratic slip 'simple' is in fact the gain over the mean wait, 0.10/1.5", 0.10 / 1.5, slip(I("homework-1", 6), "simple"), 2e-4)
ck("hw1 pension 4%", 45000 * ann(.04, 20), 611564.69, 0.01); ck("hw1 pension 5%", 45000 * ann(.05, 20), 560799.47, 0.01)
ck("hw1 pension 4.2%", 45000 * ann(.042, 20), 600875.25, 0.01); ck("hw1 pension 4.3%", 45000 * ann(.043, 20), 595634.83, 0.01)
ck("hw1 pension break-even %", 100 * brentq(lambda r: 45000 * ann(r, 20) - 600000, .01, .1), 4.22)
true("hw1: 34 halvings of [0, 1] first bring the bracket under 1e-10", 2.0 ** -33 > 1e-10 > 2.0 ** -34)

print("== Level 2: bonds, yields, shares, returns ==")
P5 = bond(4, .05, 5)
ck("l5 s1 price at 5%", P5, 95.6705, 1e-4)
ck("l5 s3 half-yearly", bond(4, .05, 5, f=2), S("l5-pricing-a-bond", 3)["answer"])
ck("l5 s3 annual twin: 4.05 coupon at 5.0625%", bond(2 * 1.025 + 2, 1.025 ** 2 - 1, 5), bond(4, .05, 5, f=2), 1e-9)
ck("l5 s3 slip full coupon", bond(8, .05, 5, f=2), slip(S("l5-pricing-a-bond", 3), "full-coupon"), 0.02)
ck("l5 s3 slip full rate", bond(4, .10, 5, f=2), slip(S("l5-pricing-a-bond", 3), "full-rate"), 0.02)
ck("l5 s3 slip five periods", 2 * ann(.025, 5) + 100 / 1.025 ** 5, slip(S("l5-pricing-a-bond", 3), "five-periods"), 0.02)
ck("l5 s5 zero", 100 / 1.05 ** 5, S("l5-pricing-a-bond", 5)["answer"])
ck("l5 s7 premium bond", bond(6, .05, 3), 102.72); ck("l5 s7 swapped", bond(5, .06, 3), 97.33)
ck("l5 q premium", bond(6, .04, 2), 103.77); ck("l5 q semi", bond(6, .04, 2, f=2), 103.81)
ck("l5 q semi slip two periods", 3 * ann(.02, 2) + 100 / 1.02 ** 2, slip(Q("l5-pricing-a-bond", 3), "two-periods"), 0.02)
true("l5: yield = coupon rate gives par for every maturity", all(abs(bond(100 * c, c, T) - 100) < 1e-9 for c in (.01, .04, .09) for T in (1, 5, 30)))
ck("l5 s10 gilt dirty price", 98.50 * 100 + 0.5 * (0.04 / 2) * 10000, S("l5-pricing-a-bond", 10)["answer"])

price = lambda y: bond(4, y, 5)
y92 = brentq(lambda y: price(y) - 92, .01, .2)
ck("l6 s2 yield at 92 (%)", 100 * y92, 5.894, 6e-4)
ck("l6 s2 5.85%", price(.0585), 92.18); ck("l6 s2 5.90%", price(.059), 91.97)
for y, p in [(.06, 91.58), (.05, 95.67), (.055, 93.59), (.0575, 92.58), (.05875, 92.07)]:
    ck(f"l6 s3 bisection price at {y}", price(y), p)
ck("l6 s3 twenty halvings of 4 points, in points", 4 / 2 ** 20, 0.000004, 5e-7)
# Newton from the bracket ends and the midpoint: steps needed to be within 4e-6 points of the yield.
def newton_steps(y0):
    y = y0
    for k in range(1, 20):
        dp = (price(y + 1e-7) - price(y - 1e-7)) / 2e-7
        y -= (price(y) - 92) / dp
        if abs(y - y92) * 100 < 4e-6:
            return k
    return 99
true("l6 s3 Newton reaches the same accuracy in three steps from 4%, 6% and 8%", max(newton_steps(.04), newton_steps(.06), newton_steps(.08)) <= 3)
def durations(c, y, T):
    t = np.arange(1, T + 1); cf = np.full(T, float(c)); cf[-1] += 100
    pv = cf / (1 + y) ** t; P = pv.sum()
    mac = (t * pv).sum() / P
    conv = (t * (t + 1) * pv).sum() / P / (1 + y) ** 2
    return P, mac, mac / (1 + y), conv
P, mac, mod, conv = durations(4, .05, 5)
ck("l6 s4 modified duration", mod, 4.40); ck("l6 s4 tangent slope per point", mod * P / 100, 4.2098, 1e-3)
ck("l6 s4 convexity", conv, 24.47); ck("l6 s4 true fall", P - price(.06), 4.10)
ck("l6 s5 2-year change %", 100 * (bond(4, .06, 2) / bond(4, .05, 2) - 1), -1.84, 0.01)
ck("l6 s5 10-year change %", 100 * (bond(4, .06, 10) / bond(4, .05, 10) - 1), -7.58, 0.01)
ck("l6 s5 modified durations", durations(4, .05, 10)[2], 7.96); ck("l6 s5 modified duration 2y", durations(4, .05, 2)[2], 1.87)
ck("l6 s6 zero's modified duration", durations(0, .05, 5)[2], 4.76)
true("l6 s6 a zero's Macaulay duration is its maturity", all(abs(durations(0, y, T)[1] - T) < 1e-9 for y in (.01, .05, .12) for T in (1, 5, 30)))
true("l6 s9 the 10-year zero has the largest modified duration of the four, at any common yield from 1% to 15%",
     all(durations(0, y, 10)[2] > max(durations(8, y, 10)[2], durations(4, y, 2)[2], durations(0, y, 2)[2]) for y in np.arange(.01, .151, .01)))
true("l6: lower coupon means longer duration at fixed maturity and yield (coupons 0..12, T 2..30, y 5%)",
     all(durations(c, .05, T)[2] > durations(c + 1, .05, T)[2] for c in range(0, 12) for T in range(2, 31)))
ck("l6 s10 portfolio of the 5y bond", 1e7 * (1 - price(.06) / P), 428058, 1.0)
ck("l6 q big move price", price(.08), 84.03); ck("l6 q big move fall %", 100 * (1 - price(.08) / P), 12.2, 0.05)
ck("l6 q big move tangent price", 95.67 * (1 - 0.132), 83.04, 0.01)
ck("l6 q duration + convexity fall %", 100 * (mod * .03 - .5 * conv * .03 ** 2), 12.1, 0.06)
ck("l6 s8 current yield", 4 / 95.67, 0.0418, 1e-4)
ck("r2 semi", bond(5, .06, 3, f=2), 97.29); ck("r2 discount bond", bond(3, .04, 7), 94.00)
ck("r2 sensitive: 2y 8% modified duration", durations(8, .05, 2)[2], 1.84); ck("r2 sensitive: 2y zero", durations(0, .05, 2)[2], 1.90)
ck("r2 ytm prices", bond(5, .06, 2), 98.17); ck("r2 ytm prices 6.5", bond(5, .065, 2), 97.27)
ck("r2 ytm %", 100 * brentq(lambda y: bond(5, y, 2) - 98, .01, .2), 6.09)
ck("hw2 ytm 97 %", 100 * brentq(lambda y: bond(5, y, 3) - 97, .01, .2), 6.1249, 1e-4)
ck("hw2 code test: ytm(110, 6%, 10y)", brentq(lambda y: bond(6, y, 10) - 110, .001, .2), 0.047224, 1e-6)
ck("hw2 bond hold: price with 4 years left", bond(4, .06, 4), 93.07)
ck("hw2 bond hold return", (bond(4, .06, 4) + 4 - 95.67) / 95.67, I("homework-2", 7)["answer"], 2e-4)
ck("hw2 bond hold at unchanged yield", (bond(4, .05, 4) + 4) / P5 - 1, 0.05, 1e-9)
P4, mac4, mod4, conv4 = durations(5, .06, 4)
ck("hw2 longform price", P4, 96.5349, 1e-4); ck("hw2 longform slope", mod4 * P4, 338.58, 0.01); ck("hw2 longform D", mod4, 3.51)
ck("hw2 longform true price 6.5%", bond(5, .065, 4), 94.86); ck("hw2 longform one-year return", (bond(5, .06, 3) + 5) / P4 - 1, 0.06, 1e-9)
ck("hw2 rights", (5 * 6 + 2 * 4) / 7, 5.43)

ck("l7 s5 first 10 dividends", 40 * (1 - (1.03 / 1.08) ** 10), 15.10); ck("l7 s5 first 150", 40 * (1 - (1.03 / 1.08) ** 150), 39.97)
ck("l7 s5 partial sum formula vs direct sum", sum(2 * 1.03 ** (k - 1) / 1.08 ** k for k in range(1, 11)), 40 * (1 - (1.03 / 1.08) ** 10), 1e-9)
ck("l7 s7 price at 10%", 2 / .07, 28.57); ck("l7 s7 fall %", 100 * (1 - (2 / .07) / 40), 29, 0.5)
ck("l7 s8 each dividend at g = r", 2 / 1.08, 1.85)
ck("l7 s11 rights", (20 + 3) / 5, 4.60, 1e-9)
ck("l8 s3 annualised", 1.134 ** (1 / 3) - 1, 0.0428, 1e-4); ck("l8 s4 log sum", math.log(1.2) + math.log(.9) + math.log(1.05), 0.1258, 1e-4)
ck("l8 s5 annualised -25% over 2y (%)", 100 * (0.75 ** .5 - 1), -13.4, 0.05)
# FINDING 2 (fixed): option 'up' (£125) is now explained as halving only the £50 gain.
ck("l8 s5 option 'up': 100 + 50 - 50% of the £50 gain, the mistake its 'why' names, against the option's £125", 100 + 50 - 0.5 * 50, 125, 1e-9)
ck("l8 s5 option 'up' is in fact the loss taken off the gain alone: 150 - 50% of 50", 150 - 0.5 * 50, 125, 1e-9)
ck("l8 s6 monthly", 1.0075 ** 12 - 1, 0.0938, 1e-4); ck("l8 s6 2% a month (%)", 100 * (1.02 ** 12 - 1), 26.82)
ck("l8 s9 total", 1.12 * .92 * 1.15, 1.18496, 1e-9); ck("l8 s9 annualised %", 100 * (1.18496 ** (1 / 3) - 1), 5.82)
ck("l8 q monthly %", 100 * (1.008 ** 12 - 1), 10.03); ck("l8 q logs", math.exp(.04) - 1, 0.0408, 1e-4)
# AM >= GM: the arithmetic mean of yearly returns never understates the annualised return.
r = rng.uniform(-0.6, 0.8, size=(20000, 5))
true("l8: arithmetic average >= annualised return in 20000 random five-year records", bool(np.all(r.mean(1) >= np.prod(1 + r, 1) ** .2 - 1 - 1e-12)))
# Monte Carlo: Sharpe 0.42 (9%, 12%) against 0.40 (12%, 20%), rf 4%. How often does a 5-year record rank them the wrong way?
n = 200000
a = rng.normal(.09, .12, size=(n, 5)); b = rng.normal(.12, .20, size=(n, 5))
sa = (a.mean(1) - .04) / a.std(1, ddof=1); sb = (b.mean(1) - .04) / b.std(1, ddof=1)
wrong_way = float(np.mean(sb > sa))
print(f"     5-year records ranking B above A: {wrong_way:.3f} (se {math.sqrt(.25 / n):.4f})")
true("l8 s11 'a few years of data could not tell them apart': B ranks above A in 45% to 55% of 5-year records", .45 < wrong_way < .55)

print("== Level 3: forwards, futures, shorting, leverage ==")
ck("l10 s6 continuous", 100 * math.exp(.05), 105.13)
Fd = (100 - 2 / 1.05 ** .5) * 1.05
ck("l10 s7 dividend forward", Fd, S("l10-cost-of-carry", 7)["answer"]); ck("l10 s7 other route", 105 - 2 * 1.05 ** .5, Fd, 1e-9)
ck("l10 s7 slip not-disc", (100 - 2) * 1.05, slip(S("l10-cost-of-carry", 7), "not-disc"))
ck("l10 s8 FX forward", 1.25 * 1.05 / 1.04, S("l10-cost-of-carry", 8)["answer"], 6e-4)
ck("l10 s8 slip inverted", 1.25 * 1.04 / 1.05, slip(S("l10-cost-of-carry", 8), "inverted"), 6e-4)
true("l10 s9 index forward: exact 8000*1.04/1.05 lies inside the accepted band round 7,920", abs(8000 * 1.04 / 1.05 - 7920) <= S("l10-cost-of-carry", 9)["tol"]["abs"])
ck("l10 q storage", 2000 * 1.05 + 10, 2110, 1e-9); ck("l10 q two years", 50 * 1.04 ** 2, 54.08)
# Arbitrage tables: both trades pay the same in every state.
ST = rng.uniform(0, 300, 1000)
cc = -105 + 108 + 0 * ST            # borrow, buy, deliver into the forward at 108
rc = 105 - 102 + (ST - ST)         # short sale lent at 5%, forward delivers the share to return
true("l10 s3/s4 cash and carry and its reverse lock in £3.00 at every final price", bool(np.allclose(cc, 3) and np.allclose(rc, 3)))
ck("r3 two-year forward", 80 * 1.03 ** 2, 84.87); ck("r3 dividend forward", (60 - 1.5 / 1.04 ** .25) * 1.04, 60.86)
ck("r3 dividend forward other route", 62.4 - 1.5 * 1.04 ** .75, 60.86)
ck("hw3 carry arb", 104 + 2 * 1.05 ** .5 - 105, I("homework-3", 2)["answer"])
ub = (64 - 1.2 * 1.07 ** -.5) * 1.07; lb = (64 - 1.2 * 1.03 ** -.5) * 1.03 - .5
ck("hw3 two rates upper", ub, 67.2387, 1e-4); ck("hw3 two rates lower", lb, 64.2021, 1e-4)
ck("hw3 upper, dividend deposited", 64 * 1.07 - 1.2 * 1.03 ** .5, 67.2621, 1e-4); ck("hw3 lower, dividend borrowed", 64 * 1.03 - 1.2 * 1.07 ** .5 - .5, 64.1787, 1e-4)
ck("hw3 one rate 5%", (64 - 1.2 * 1.05 ** -.5) * 1.05, 65.9704, 1e-4); ck("hw3 optional profit", 67.80 - ub, 0.5613, 1e-4)
ck("hw3 airline forward", 600 * 1.05 + 12, 642, 1e-9)


def margin_calls(prices, n, m, init, maint, to=None):
    side = 1 if n > 0 else -1; k = abs(n); bal = init * k; calls = []; bals = []
    for p, q in zip(prices, prices[1:]):
        bal += side * k * m * (q - p); bals.append(bal)
        c = (init * k if to is None else to * k) - bal if bal < maint * k else 0
        calls.append(c); bal += c
    return calls, bals


true("l11 s3 table", margin_calls([8000, 7960, 7900, 7830, 7830, 7880], 1, 10, 6000, 4500) == ([0, 0, 1700, 0, 0], [5600, 5000, 4300, 6000, 6500]))
true("l11 s5 trap: one call of 1,600 after day 2", margin_calls([8000, 7930, 7840, 7900, 7880], 1, 10, 6000, 4500)[0] == [0, 1600, 0, 0])
ck("l11 s8 pension fund call", margin_calls([8010, 8260], -10, 10, 6000, 4500)[0][0], 25000, 1e-9)
c2, b2 = margin_calls([8000, 7900, 7820, 7850, 7700, 7640], 2, 10, 6000, 4500)
true("hw3 two calls", c2 == [0, 3600, 0, 0, 3600] and b2 == [10000, 8400, 12600, 9600, 8400])
ck("hw3 two calls slip maint", sum(margin_calls([8000, 7900, 7820, 7850, 7700, 7640], 2, 10, 6000, 4500, to=4500)[0]), slip(I("homework-3", 3), "maint"), 1e-9)
ck("r3 three contracts", margin_calls([8000, 7800], 3, 10, 6000, 4500)[0][0], 6000, 1e-9)
ck("l12 s3 short P&L", 50000 - 50000 * .03 * .25 - 600 - 42000, 7025, 1e-9)
ck("l13 s7 margin loan trigger", 10000 / .75, 13333.33); ck("r3 margin loan", 18000 / .7, 25714.29)
ck("hw3 levered call", 1 - (2 / .75) / 3, I("homework-3", 6)["answer"], 1e-4)
ck("hw3 short margin", brentq(lambda x: (75000 - 50000 * (1 + x)) - .3 * 50000 * (1 + x), 0, 1), I("homework-3", 7)["answer"], 1e-4)
RE = lambda Lv, ra, rr: Lv * ra - (Lv - 1) * rr
true("l13: R_E = L R_A - (L-1) r matches the balance sheet for random cases",
     all(abs((Lv * (1 + ra) - (Lv - 1) * (1 + rr) - 1) - RE(Lv, ra, rr)) < 1e-12 for Lv, ra, rr in rng.uniform([1, -.9, 0], [6, .9, .2], size=(1000, 3))))
ck("l13 s1 L=4 up", RE(4, .1, .05), 0.25, 1e-9); ck("l13 s1 L=4 down", RE(4, -.1, .05), -0.55, 1e-9)
ck("l13 s8 equity fall", (0.2 * 300000 + 200000 * .06 * .25) / 100000, 0.63, 1e-9)
ck("l13 s8 further fall that wipes out", 37000 / 240000, 0.15, 0.006)
# Monte Carlo: leverage and the chance of losing half the equity in a year; volatility scaling.
ra = rng.normal(.07, .15, 1_000_000)
p1, p3 = float(np.mean(RE(1, ra, .05) <= -.5)), float(np.mean(RE(3, ra, .05) <= -.5))
print(f"     P(lose half in a year): L=1 {p1:.5f}, L=3 {p3:.4f}; sd of R_E at L=3 {np.std(RE(3, ra, .05)):.4f}")
true("l13 q-recover 'leverage makes 50% losses far more likely': P at L=3 is over 100 times P at L=1", p3 > 100 * max(p1, 1e-6))
ck("l13 s8 volatility scales with L: 15% market at L=3", float(np.std(RE(3, ra, .05))), 0.45, 0.005)

print(f"\n{N} checks, {len(FAILS)} failing")
for f in FAILS:
    print("  FAIL:", f)
sys.exit(1 if FAILS else 0)
