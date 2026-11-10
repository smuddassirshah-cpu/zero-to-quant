#!/usr/bin/env python3
"""Concept checks for mental level 3 (l9 to l12, review-3, homework-3).

Run from the repo root: python3 -I docs/reports/mental-L3-concepts.py
Each check names its ledger row (docs/reports/audit-mental-1-3-ledger.md).
Exit 0 means every checked claim holds. A check that fails because the content is
wrong would be marked EXPECTED_FAIL and kept failing; this level has none.
Claims that are true only under a hypothesis the text drops are demonstrated and
printed as "note" lines (findings in docs/reviews/audit-mental-1-3.md), not asserted.
After the fix pass the corrected claims are asserted, marked "(corrected claim, fix pass)".
"""
import json
import os
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction as F

BASE = os.path.join("app", "content", "courses", "mental")


def load(name):
    with open(os.path.join(BASE, name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def check(name, cond, msg):
    assert cond, f"{name}: {msg}"
    print(f"ok  {name}")


def note(name, msg):
    print(f"note {name}: {msg}")


def wrongs(widget):
    return {w["id"]: w["value"] for w in widget.get("wrong", []) if "value" in w}


def rnd(x, places):
    q = Decimal(1).scaleb(-places)
    return (Decimal(x.numerator) / Decimal(x.denominator)).quantize(q, rounding=ROUND_HALF_UP)


def cells(value, n=12):
    return sorted(f"r{r}c{c}" for r in range(1, n + 1) for c in range(1, n + 1) if r * c == value)


# ---- l9: division as a missing factor; splitting, halving, doubling
def division():
    d = load("l9-missing-multiplication")
    check("l9_cells_72", cells(72) == sorted(d["screens"][2]["widget"]["answer"]) and len(cells(72)) == 4,
          "l9 screens[2]: 72 sits in four cells")
    check("l9_84_in_col_7", d["screens"][1]["widget"]["answer"] == ["r12c7"] and 7 * 12 == 84, "l9 screens[1]")
    # splitting the dividend is safe, splitting the divisor is not
    ok = all(F(x + y, b) == F(x, b) + F(y, b) for x in range(0, 300, 7) for y in range(0, 300, 11) for b in range(1, 13))
    check("l9_split_dividend", ok, "l9 screens[8].prose, summary.formula: (x + y) / b = x / b + y / b")
    bad = [(a, b1, b2) for a in range(1, 200) for b1 in range(1, 13) for b2 in range(1, 13) if F(a, b1 + b2) == F(a, b1) + F(a, b2)]
    check("l9_never_split_divisor", bad == [], "l9 screens[7].explain, summary.formula.note: a / (b1 + b2) never equals a / b1 + a / b2 for positive numbers")
    check("l9_trap", F(84, 12) == 7 and F(84, 10) + F(84, 2) == F("50.4"), "l9 screens[7]: 7, not 50.4")
    ok = all(F(F(n, 2), 2) == F(n, 4) and F(F(F(n, 2), 2), 2) == F(n, 8) and F(2 * n, 10) == F(n, 5) for n in range(0, 2000))
    check("l9_halving_doubling", ok, "l9 screens[5], [6], [9]: halve twice for 4, three times for 8; double then divide by 10 for 5")
    check("l9_keys", F(96, 4) == 24 == 20 + 4 and F(136, 4) == 34 and F(115, 5) == 23 and F(156, 12) == 13 and F(184, 8) == 23
          and F(764, 8) == F("95.5") == F(str(d["screens"][10]["widget"]["answer"])), "l9 screens[4..10]: keyed quotients")
    check("l9_quiz", F(72, 6) == 12 and F(700, 7) == 100 and F(135, 5) == 27 and F(192, 8) == 24 and 48 + 48 == 96 and 20 + 32 == 52,
          "l9 quiz[0..3]")
    # quiz[1].prose: default Zetamac division answers go up to 100 (app copy of the settings)
    with open(os.path.join("app", "content", "warmup.json"), encoding="utf-8") as fh:
        wu = json.load(fh)
    mul = next(o for o in wu["operations"] if o["id"] == "mul")
    div = next(o for o in wu["operations"] if o["id"] == "div")
    check("l9_zetamac_division", mul["a"] == [2, 12] and mul["b"] == [2, 100] and div.get("inverseOf") == "mul",
          "l9 quiz[1].prose, l6 screens[4], l7 screens[0]: divisor 2 to 12, answers 2 to 100 (app/content/warmup.json)")
    # screens[4].prose: "96 is off the table" (finding 7): 96 is in the 12 by 12 table, though not in column 4
    in_table = cells(96)
    col4 = [c for c in in_table if c.endswith("c4")]
    p4 = d["screens"][4]["prose"]
    check("l9_96_off_table", in_table == ["r12c8", "r8c12"] and col4 == [] and 4 * 12 == 48 < 96
          and "Column 4 stops at 48" in p4 and "off the table" not in p4,
          "(corrected claim, fix pass) l9 screens[4].prose: 96 is past the end of column 4, though in the table as 8 x 12")


# ---- l10: decimals of common fractions, remainders
def decimals():
    check("l10_eighths", [F(k, 8) for k in (1, 3, 5, 7)] == [F("0.125"), F("0.375"), F("0.625"), F("0.875")] and F(1, 2) + F(1, 8) == F(5, 8),
          "l10 screens[1..3], quiz[0]: eighths")
    check("l10_rounding", (rnd(F(1, 6), 3), rnd(F(2, 3), 3), rnd(F(1, 12), 4), rnd(F(7, 12), 4), rnd(F(5, 12), 4), rnd(F(11, 12), 2), rnd(F(11, 12), 4),
                           rnd(F(5, 6), 3), rnd(F(29, 6), 2), rnd(F(1, 24), 4))
          == tuple(Decimal(s) for s in ("0.167", "0.667", "0.0833", "0.5833", "0.4167", "0.92", "0.9167", "0.833", "4.83", "0.0417")),
          "l10 screens[4], [5], [8], [9], quiz[1], [3]; review-3 items[5]; homework-3 items[3], [7]: rounded decimals")
    # screens[9]: carry five places, then round to four; four-place pieces give the wrong last digit here
    five = Decimal("0.33333") + Decimal("0.08333")
    four = Decimal("0.3333") + Decimal("0.0833")
    check("l10_carry_extra_place", five == Decimal("0.41666") and five.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP) == Decimal("0.4167")
          and four == Decimal("0.4166") != rnd(F(5, 12), 4), "l10 screens[9].explain: the fifth place keeps the rounding right for 5/12")
    # remainders: a / b = q + r / b with 0 <= r < b
    ok = all(F(a, b) == a // b + F(a % b, b) and 0 <= a % b < b for a in range(0, 500) for b in range(1, 13))
    check("l10_remainder_formula", ok, "l10 screens[8].prose, summary.formula: a / b = q + r / b, r less than b")
    check("l10_remainder_keys", F(23, 4) == F("5.75") and divmod(23, 4) == (5, 3) and F(38, 8) == F("4.75") and divmod(38, 8) == (4, 6)
          and divmod(29, 6) == (4, 5) and F(45, 8) == F("5.625") and divmod(45, 8) == (5, 5) and F(7, 2) == F("3.5"),
          "l10 screens[6], [7], [8], quiz[2], summary.trap")
    check("l10_return", F(2500, 30000) == F(25, 300) == F(1, 12), "l10 screens[10]: £2,500 on £30,000 is 1/12")
    check("l10_orderings", F(1, 10) < F(1, 8) < F(1, 4) and F(1, 6) < F(1, 5) and F(1, 12) < F(1, 10) and F(7, 8) > F(7, 10) and F(3, 8) > F(3, 10),
          "l10 byKey lines: eighths are bigger than tenths, a sixth is below a fifth, twelfths are smaller than tenths")
    # numeric tolerances accept the alternatives the accept lines name and reject the keyed slips
    d = load("l10-known-decimals")
    w = d["screens"][4]["widget"]
    t = w["tol"]["abs"]
    check("l10_sixth_tolerance", all(abs(v - w["answer"]) <= t for v in (0.1667, 0.16667)) and all(abs(v - w["answer"]) > t for v in wrongs(w).values()),
          "l10 screens[4].widget.accept: 0.1667 and 0.16667 are accepted, 0.166 is not")


# ---- l11: percentages
def percentages():
    pct = lambda p, a: F(str(p)) * F(str(a)) / 100
    check("l11_pieces", pct(10, 340) == 34 and pct(5, 340) == 17 and pct(1, 340) == F("3.4") and pct(17, 340) == F("57.8") == 34 + 17 + F("6.8"),
          "l11 screens[0..3]")
    check("l11_keys", pct(35, 240) == 84 and pct(49, 260) == F("127.4") == 130 - F("2.6") and pct(0.5, 3600) == 18 and pct(5, 3600) == 180
          and pct(23, 600) == 138 and pct(17.5, 240) == 42 == 24 + 12 + 6 and pct(60, 8450) == 5070 and pct(40, 8450) == 3380,
          "l11 screens[4..9]")
    check("l11_quiz", pct(5, 780) == 39 and pct(1, 2350) == F("23.5") and pct(15, 86) == F("12.9") and pct(21, 300) == 63, "l11 quiz[0..3]")
    ok = all(pct(5, a) == pct(10, a) / 2 and pct(1, a) == pct(10, a) / 10 and pct(0.5, a) == pct(1, a) / 2 for a in range(1, 5000, 7))
    check("l11_halving", ok, "l11 screens[1].explain: halving 10% gives 5% every time; 1% is a tenth of 10%")
    # screens[5].prose: 49% from 10%, 5% and 1% pieces takes nine pieces
    best = min(t + f + o for t in range(0, 6) for f in range(0, 11) for o in range(0, 50) if 10 * t + 5 * f + o == 49)
    check("l11_nine_pieces", best == 9, "l11 screens[5].prose: 49% needs nine pieces of 10%, 5% and 1%")
    ok = all(pct(p, a) == pct(a, p) for p in range(1, 101) for a in range(1, 101))
    check("hw3_swap", ok and pct(36, 25) == 9 == pct(25, 36), "homework-3 items[8]: p% of A equals A% of p")


# ---- l12: pace, triage, splits at multiples of the divisor
def clock():
    d = load("l12-against-the-clock")
    check("l12_pace", F(120, 30) == 4 and 10 * 4 == 40 and F(120, 40) == 3 and F(120, 25) * 10 == 48 and F(120, 24) == 5,
          "l12 screens[1], [2], [5].prose, quiz[0]; review-3 items[3]")
    # "each second you save per answer adds a lot of score at the fast end"
    gain_fast, gain_slow = 120 // 3 - 120 // 4, 120 // 9 - 120 // 10
    check("l12_fast_end", gain_fast == 10 and gain_slow == 1, "l12 screens[2].explain: 4 s to 3 s adds 10; 10 s to 9 s adds 1")
    rows = [("84 ÷ 7", 84, 7), ("96 ÷ 4", 96, 4), ("72 ÷ 8", 72, 8), ("135 ÷ 5", 135, 5), ("132 ÷ 11", 132, 11), ("176 ÷ 8", 176, 8)]
    past = [f"r{i}c1" for i, (_, a, b) in enumerate(rows) if a > 12 * b]
    check("l12_past_table", past == d["screens"][3]["widget"]["answer"], "l12 screens[3]: answers above 12 are exactly a > 12b")
    keyed = [r[1]["answer"] for r in d["screens"][5]["widget"]["rows"]]
    qs = [(63, 9), (108, 4), (145, 5), (132, 12), (248, 8), (91, 7), (195, 5), (144, 6), (168, 12), (88, 11)]
    check("l12_round_of_ten", keyed == [a // b for a, b in qs] and all(a % b == 0 for a, b in qs), "l12 screens[5]: ten quotients")
    kinds = []
    for a, b in qs:
        if a // b <= 12:
            kinds.append("recall")
        elif b in (4, 8):
            kinds.append("halve")
        elif b == 5:
            kinds.append("double")
        else:
            kinds.append("split")
    check("l12_method_counts", [kinds.count(k) for k in ("recall", "halve", "double", "split")] == [3, 2, 2, 3],
          "l12 screens[5].explain: three recall, two halvings, two doublings, three splits")
    scores = d["screens"][6]["canvas"]["state"]["values"]
    avg = F(sum(scores.values()), len(scores))
    check("l12_average", avg == 21 == d["screens"][6]["widget"]["answer"] and [k for k, v in scores.items() if v > avg] == ["Thu", "Fri"],
          "l12 screens[6]: mean 21; Thursday and Friday are above it")
    check("l12_splits", divmod(100, 7) == (14, 2) and divmod(26, 7) == (3, 5) and divmod(120, 7) == (17, 1) and 70 // 7 + 56 // 7 == 18 == 126 // 7
          and divmod(47, 7) == (6, 5) and divmod(27, 7) == (3, 6) and 147 // 7 == 21, "l12 screens[7]; review-3 items[7]: which splits leave remainders")
    idea = d["summary"]["ideas"][2]
    check("l12_split_contrast", 70 % 10 == 0 and 70 % 7 == 0 == 56 % 7 and 100 % 7 and 120 % 7
          and "not at the hundred or the tens" in idea and "not at round numbers" not in idea,
          "(corrected claim, fix pass) l12 summary.ideas[2]: the good split 70 is round; 100 and 120 fail because 7 does not divide them")
    ok = all(F(m * b + n * b, b) == m + n for m in range(0, 30) for n in range(0, 13) for b in range(1, 13))
    check("l12_split_formula", ok, "l12 screens[8].prose, summary.formula: (mb + nb) / b = m + n")
    check("l12_keys", F(232, 8) == 29 and F(204, 12) == 17 == 10 + 7 and F(196, 7) == 28 and F(117, 9) == 13 and F(22 + 25 + 24 + 27 + 27, 5) == 25,
          "l12 screens[8], [9], quiz[1..3]")
    t = [F(str(r[1]["answer"])) for r in d["screens"][10]["widget"]["rows"]]
    check("l12_transfer", t == [F(1182, 12), F("9.60") / 3200, F(1500, 12000), F(40, 100) * 7250] and F(1182, 12) == 100 - F("1.5"),
          "l12 screens[10]: £98.50, 0.003, 0.125, £2,900")


# ---- review-3 and homework-3
def review_homework():
    r = load("review-3")
    ans = {it["id"]: it["widget"].get("answer") for it in r["items"]}
    check("review3_keys", ans["r-missing-factor"] == 96 // 12 and F(str(ans["r-seventeen"])) == F(17, 100) * 260 and F(str(ans["r-remainder"])) == F(53, 4)
          and ans["r-pace"] == 120 // 24 and ans["r-halve-eight"] == 216 // 8 and F(str(ans["r-fee"])) == F("0.25") / 100 * 6400
          and ans["r-by-five"] == 165 // 5 and F(7000, 42000) == F(1, 6), "review-3 items[0..9]")
    h = load("homework-3")
    ans = {it["id"]: it.get("widget", {}).get("answer") for it in h["items"]}
    check("hw3_keys", ans["h-twelve-split"] == 228 // 12 == 10 + 9 and F(228, 10) + F(228, 2) == F("136.8")
          and F(1026, 8) == F("128.25") and F("850.50") / 9 == F(str(ans["h-nine-shares"])) == 90 + F("4.5")
          and F(str(ans["h-twenty-three"])) == F(23, 100) * 1850 and F(1000, 24000) == F(1, 24) == F(1, 12) / 2, "homework-3 items[0], [2], [4], [5], [7]")
    rows = [x[1]["answer"] for x in h["items"][1]["widget"]["rows"]]
    check("hw3_timed", rows == [117 // 9, 184 // 4, 185 // 5, 152 // 8, 98 // 7], "homework-3 items[1]")
    book = [x[1]["answer"] for x in h["items"][6]["widget"]["rows"]]
    check("hw3_book", book == [7500, 5000, 15] and F("0.2") / 100 * 7500 == 15, "homework-3 items[6]: 60:40 of £12,500 and a 0.2% fee on equities")
    fee = F("0.15") / 100 * 1148
    check("hw3_blotter", F(1148, 8) == F("143.5") and divmod(1148, 8) == (143, 4) and fee == F("1.722") == F("1.148") + F("0.574")
          and F("17.22") == F("1.5") / 100 * 1148 and F(287, 1148) == F(1, 4), "homework-3 items[9] model: £143.50, £1.72, 0.25")


if __name__ == "__main__":
    division()
    decimals()
    percentages()
    clock()
    review_homework()
    print("L3 concepts: all checks passed")
