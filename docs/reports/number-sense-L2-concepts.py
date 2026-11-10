#!/usr/bin/env python3
"""Concept checks for number-sense level 2 (l6 to l9, review-2, homework-2).

Run from the repo root: python3 -I docs/reports/number-sense-L2-concepts.py
Each check names its ledger row (docs/reports/audit-number-sense-1-3-ledger.md).
Exit 0 means every checked claim holds on the domain the lesson uses. A line
starting "note" records where a claim stops holding outside that domain; those
are the `imprecise` findings of docs/reviews/audit-number-sense-1-3.md and are
not asserted. A failing assert names the claim.

Fix pass: the notes for findings 4, 6, 7 and 8 are now checks marked "(corrected
claim, fix pass)", and findings 5 and 9 and the two doubled sentences gained text
checks; each recomputes the corrected claim and asserts the content states it.
"""
import json
import random
from pathlib import Path
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_FLOOR
from fractions import Fraction as F
from math import gcd

COURSE = Path("app/content/courses/number-sense")
N = 0
random.seed(20261109)


def txt(file, *path):
    d = json.loads((COURSE / file).read_text(encoding="utf-8"))
    for p in path:
        d = d[p]
    return d


def check(name, cond, msg):
    global N
    assert cond, f"{name}: {msg}"
    N += 1
    print(f"ok  {name}")


def note(name, msg):
    print(f"note {name}: {msg}")


# ---- l6: place value, comparing, rounding
def place_value():
    ok = True
    for _ in range(4000):
        digits = random.randint(1, 5)
        s = f"{random.randint(0, 99)}." + "".join(random.choice("0123456789") for _ in range(digits))
        whole, frac = s.split(".")
        by_place = int(whole) + sum(F(int(ch), 10 ** (i + 1)) for i, ch in enumerate(frac))
        ok &= by_place == F(int(whole + frac), 10 ** digits) == F(D(s))
    check("decimal_is_fraction_over_power_of_ten", ok,
          "l6 screens[3], [8], summary.formula.note: n digits after the point give a bottom of 10^n")
    check("third_is_not_over_power_of_ten", all((10 ** n) % 3 == 1 for n in range(1, 60)),
          "l7 screens[5]: every power of ten leaves 1 when divided by 3")
    e3 = txt("l6-place-value.json", "screens", 3, "explain", "text")
    p8 = txt("l6-place-value.json", "screens", 8, "prose")
    check("decimal_definition", all((10 ** n) % 3 == 1 for n in range(0, 60))
          and "A decimal that stops is a fraction whose bottom is 10, 100, 1000" in e3 and "A decimal is a fraction" not in e3
          and "any decimal that stops can be written as one fraction over 10, 100, 1000" in p8,
          "(corrected claim, fix pass) l6 screens[3].explain, screens[8].prose: only a decimal that stops has a power of "
          "ten for a bottom; 1/3 = 0.333... has none (finding 4)")

    def digitwise(a, b):                     # compare place by place from the left, padding with zeros
        aw, af = a.split(".")
        bw, bf = b.split(".")
        if int(aw) != int(bw):
            return (int(aw) > int(bw)) - (int(aw) < int(bw))
        n = max(len(af), len(bf))
        for x, y in zip(af.ljust(n, "0"), bf.ljust(n, "0")):
            if x != y:
                return (x > y) - (x < y)
        return 0
    ok = True
    for _ in range(6000):
        a = f"{random.randint(0, 20)}." + "".join(random.choice("0123456789") for _ in range(random.randint(1, 4)))
        b = f"{random.randint(0, 20)}." + "".join(random.choice("0123456789") for _ in range(random.randint(1, 4)))
        ok &= digitwise(a, b) == (D(a) > D(b)) - (D(a) < D(b))
    check("compare_by_place", ok, "l6 screens[7], summary.ideas[1]: the first place that differs decides (positive decimals)")
    check("longer_is_not_larger", D("0.45") < D("0.5") and D("3.09") < D("3.1") and D("0.508") < D("0.58") < D("0.6")
          and min(D("12.5"), D("12.45"), D("12.48")) == D("12.45") and max(D("2.09"), D("2.1"), D("2.089")) == D("2.1"),
          "l6 screens[6], [7], [9], quiz[0]; review-2 items[0]")
    note("compare_negatives", "for negatives the order flips: -3.1 < -3.09 although 1 tenth 'beats' 0 tenths; "
         "homework-2 items[0] says so ('among negatives, the one closer to zero is larger')")


def rounding():
    # the rule 'next digit 5 or more rounds up' against 'pick the closer neighbour', every 3-place decimal below 10
    ok, ties = True, 0
    for k in range(0, 10000):
        x = D(k) / D(1000)
        rule = x.quantize(D("0.1"), rounding=ROUND_HALF_UP)
        lo = x.quantize(D("0.1"), rounding=ROUND_FLOOR)
        hi = lo + D("0.1")
        if x - lo == hi - x:
            ties += 1                         # no closer neighbour: the rule sends it up
            ok &= rule == hi
        else:
            ok &= rule == (lo if x - lo < hi - x else hi)
        ok &= (rule == hi) == (int(str(x.quantize(D("0.001")))[-2]) >= 5) or x == lo
    check("round_half_up_is_nearest", ok,
          "l6 screens[5], summary.ideas[2]: the digit rule picks the closer neighbour, and sends an exact half up")
    print(f"    ({ties} exact halves in 10,000 cases: the 5-or-more convention decides those)")

    def r(x, places):
        return D(x.numerator).__truediv__(D(x.denominator)).quantize(D(1).scaleb(-places), rounding=ROUND_HALF_UP)
    check("rounding_keys", r(F(237, 100), 1) == D("2.4") and r(F(396, 100), 1) == D("4.0") and r(F(2, 3), 2) == D("0.67")
          and r(F(5, 6), 2) == D("0.83") and r(F(3002, 300), 2) == D("10.01") and r(F(100, 3), 2) == D("33.33")
          and r(F(20, 7), 2) == D("2.86") and r(F(12996, 1000), 2) == D("13.00") and r(F(7, 12), 3) == D("0.583")
          and r(F(6047, 300), 2) == D("20.16"),
          "l6 screens[5], quiz[2]; l7 screens[7], [11], quiz[1], quiz[3]; review-2 items[4], [6]; homework-2 items[1], [7]")
    check("three_point_nine", r(F(39, 10), 1) == D("3.9") and r(F(396, 100), 1) == D("4.0"),
          "l6 quiz[2].feedback.byKey.ten-tenths: it is 3.96 that rounds to 4.0; 3.9 to the nearest tenth is 3.9 (finding 5)")
    fb = txt("l6-place-value.json", "quiz", 2, "feedback")
    check("three_point_nine_text", "so 3.96 rounds up to 4.0." in fb["byKey"]["ten-tenths"]
          and "3.9 rounds" not in fb["byKey"]["ten-tenths"]
          and fb["correct"].count("Write the 0: it shows one decimal place.") == 1,
          "(corrected claim, fix pass) l6 quiz[2].feedback: the ten-tenths line names 3.96; the correct line says its "
          "sentence once (finding 5; doubled sentence)")
    tick = F(1, 100)
    e9 = txt("l6-place-value.json", "screens", 9, "explain", "text")
    check("two_places_reason", tick * 100 == 1 and "so every digit lines up" not in e9
          and "Writing every price to two places lines the digits up." in e9,
          "(corrected claim, fix pass) l6 screens[9].explain: a penny is 1/100 of a pound, which sets the two places; "
          "lining up is what two places give the reader, not the reason for them (finding 9)")


# ---- l7: stopping and recurring decimals
def terminating():
    def stops(a, b):
        return any((10 ** n * a) % b == 0 for n in range(0, 40))

    def only_2_and_5(n):
        for p in (2, 5):
            while n % p == 0:
                n //= p
        return n == 1
    ok = True
    for b in range(1, 401):
        for a in range(1, b + 1):
            ok &= stops(a, b) == only_2_and_5(b // gcd(a, b))
    check("stops_iff_2s_and_5s", ok,
          "l7 screens[9], summary.ideas[1]: a/b stops exactly when the bottom in lowest terms has only 2s and 5s (b up to 400)")
    twelfths = [a for a in range(1, 12) if stops(a, 12)]
    check("twelfths_that_stop", twelfths == [3, 6, 9] and not stops(7, 12),
          "l7 quiz[2]: 3/12 stops; homework-2 items[1]: 7/12 does not")
    hw = txt("homework-2.json", "items", 1, "prose")
    check("no_power_of_ten_for_twelfths", twelfths == [a for a in range(1, 12) if (12 // gcd(a, 12)) % 3 != 0]
          and gcd(7, 12) == 1 and not stops(7, 12) and "works for twelfths" not in hw
          and "No power of ten works for $\\tfrac{7}{12}$" in hw and "the 3 does not cancel with the 7" in hw,
          f"(corrected claim, fix pass) homework-2 items[1].prose: a/12 stops for a in {twelfths}, where the 3 cancels; "
          "7/12 does not stop because the 3 does not cancel (finding 6)")
    check("lesson_examples", F(7, 40) == F(175, 1000) and not stops(1, 6) and not stops(2, 9) and not stops(5, 12)
          and F(3, 8) == F(375, 1000) and F(7, 20) == F(35, 100) and F(9, 25) == F(36, 100) and F(125, 1000) == F(1, 8),
          "l7 screens[3], [4], [9], [10], quiz[0]")
    check("point_three_three", F(1, 3) - F(33, 100) == F(1, 300) and 3 * F(33, 100) == F(99, 100),
          "l7 screens[8], summary.trap: 0.33 is 1/300 short of a third")
    # long division of 1/7: block of 6, 100th digit
    digits, rem = [], 1
    for _ in range(120):
        rem *= 10
        digits.append(rem // 7)
        rem %= 7
    check("one_seventh", digits[:6] == [1, 4, 2, 8, 5, 7] and digits[:114] == digits[6:120] and digits[99] == 8,
          "homework-2 items[5]: the block 142857 repeats and the 100th digit is 8")
    order = sorted([F(3, 10), F(1, 3), F(34, 100), F(3, 8), F(-1, 2), F(-1, 3)])
    check("mixed_order", order == [F(-1, 2), F(-1, 3), F(3, 10), F(1, 3), F(34, 100), F(3, 8)],
          "review-2 items[9]; homework-2 items[0]")


# ---- l8: negatives on the line
def signed_addition():
    Z = range(-12, 13)
    check("subtract_is_add_opposite", all(a - b == a + (-b) and a - (-b) == a + b for a in Z for b in Z),
          "l8 screens[7], summary.formula")
    check("subtraction_undoes_addition", all((a + b) - b == a for a in Z for b in Z),
          "l8 screens[8]: taking away what you added returns you to the start")
    neg = range(-12, 0)
    check("two_negatives_added", all(a + b < a and a + b < b and a + b < 0 for a in neg for b in neg),
          "l8 screens[5]; l9 screens[7]: adding two negatives gives a total below both")
    e5 = txt("l8-below-zero.json", "screens", 5, "explain", "text")
    trap = txt("l9-negative-times-negative.json", "summary", "trap")
    check("bigger_negative", -2 + -9 == -11 < -2 and (-4) + (-6) == -10 < -6
          and "Adding two negatives gives a number lower than both." in e5
          and "Adding two negatives gives a lower number: $(-4) + (-6) = -10$." in trap
          and all("bigger negative" not in (COURSE / f).read_text(encoding="utf-8")
                  for f in ("l8-below-zero.json", "l9-negative-times-negative.json")),
          "(corrected claim, fix pass) l8 screens[5].explain, l9 summary.trap: the sum of two negatives is lower than "
          "both (finding 7)")
    why = txt("l8-below-zero.json", "quiz", 0, "widget", "options", 2, "why")
    check("second_coldest_once", why.count("You picked the second coldest.") == 1 and -15 == -12 - 3,
          "(fix pass) l8 quiz[0].widget.options[2].why says its sentence once; -15 is 3 lower than -12 (doubled sentence)")
    check("order_on_the_line", -7 < -2 and min(-12, -3, 0, -15) == -15, "l8 screens[2], quiz[0]")
    check("l8_keys", 3 - 5 == -2 and -4 + 7 == 3 and 6 + (-9) == -3 and -2 + (-5) + (-4) == -11
          and -3 - (-8) == 5 and 4 - (-5) == 9 and D("-4.25") - D("-4.25") == 0 and D("2.5") - D("-7.5") == 10,
          "l8 screens[1] to [6], quiz[2], quiz[4]; review-2 items[5]")


def drawdown(series):
    peak, worst = series[0], D(0)
    for x in series:
        peak = max(peak, x)
        worst = max(worst, peak - x)
    return worst


def drawdowns():
    check("drawdown_l8", drawdown([D(v) for v in (0, 120, -130, -210, -150, -110)]) == 330,
          "l8 screens[9]: peak 120 to the low after it, -210, is a fall of 330")
    run = [D(0)]
    for d in ("84.50", "-126.25", "-37.80", "52.15", "-9.60"):
        run.append(run[-1] + D(d))
    check("running_pnl", run[1:] == [D("84.50"), D("-41.75"), D("-79.55"), D("-27.40"), D("-37.00")],
          "homework-2 items[2]")
    check("drawdown_hw2", drawdown(run) == D("164.05") and D("45.50") - D("-18.25") == D("63.75"),
          "homework-2 items[3]; review-2 items[8]: largest peak-to-later-low fall")


# ---- l9: sign rules
def sign_rules():
    Z = [z for z in range(-9, 10) if z != 0]

    def sign(x):
        return (x > 0) - (x < 0)
    check("sign_rule_products", all(sign(a * b) == (1 if sign(a) == sign(b) else -1) for a in Z for b in Z),
          "l9 screens[8]: matching signs give a positive, different signs a negative (non-zero numbers)")
    check("sign_rule_division", all(sign(F(a, b)) == sign(a * b) and F(a, b) * b == a for a in Z for b in Z),
          "l9 screens[6], summary.formula.note: division follows the same sign rules because it undoes multiplication")
    ok = True
    for _ in range(4000):
        xs = [random.choice(Z) for _ in range(random.randint(2, 7))]
        p = 1
        for x in xs:
            p *= x
        ok &= (p < 0) == (sum(1 for x in xs if x < 0) % 2 == 1)
    check("odd_number_of_negatives", ok, "l9 screens[8].explain, quiz[4]: an odd number of negatives leaves a negative")
    # the pattern: (-3) x k rises by 3 as k falls by 1
    check("pattern_table", [(-3) * k for k in (3, 2, 1, 0, -1, -2)] == [-9, -6, -3, 0, 3, 6],
          "l9 screens[4]")
    # the part-by-part argument: the product is forced
    ok = True
    for a in range(1, 13):
        for b in range(1, 13):
            x = 0 - (-a) * b                 # the only x with (-a)*b + x = 0
            ok &= x == a * b == (-a) * (-b)
    check("part_by_part_forces_sign", ok,
          "l9 screens[9]; homework-2 items[6]: (-a)(b + (-b)) = 0 forces (-a)(-b) = ab")
    check("pnl_keys", D("-200") * (D("10.90") - D("12.40")) == 300 and 300 * D("-0.25") == -75
          and D("-150") * (D("8.65") - D("8.40")) == D("-37.5")
          and 400 * D("-0.35") + D("-250") * D("-1.12") == 140 and D("-100") * D("-0.60") == 60 and -40 - (-15) == -25,
          "l9 screens[10], quiz[3]; review-2 items[7]; homework-2 items[4], items[8]")


def division_by_zero():
    Z = range(-20, 21)
    # 'a / b asks: what times b gives a?' has exactly one answer for b != 0 among fractions ...
    ok = all(F(a, b) * b == a for a in Z for b in Z if b != 0)
    # ... none for b = 0 and a != 0, and every number for a = b = 0
    none = all(not any(x * 0 == a for x in Z) for a in Z if a != 0)
    every = all(x * 0 == 0 for x in Z)
    check("what_times_b_gives_a", ok and none and every,
          "l9 screens[6]: the question has one answer when b is not 0, none for a/0, and no single answer for 0/0")
    p6 = txt("l9-negative-times-negative.json", "screens", 6, "prose")
    check("division_by_zero", none and not any(x * 0 == 5 for x in range(-1000, 1001))
          and p6.endswith("Nothing times 0 gives 5, so we never divide by 0."),
          "(corrected claim, fix pass) l9 screens[6].prose: no number times 0 gives 5, so a / 0 has no answer and "
          "the course says we never divide by 0 (finding 8)")


if __name__ == "__main__":
    place_value()
    rounding()
    terminating()
    signed_addition()
    drawdowns()
    sign_rules()
    division_by_zero()
    print(f"L2 concepts: all {N} checks passed")
