#!/usr/bin/env python3
"""Concept checks for mental level 1 (l1 to l4, review-1, homework-1).

Run from the repo root: python3 -I docs/reports/mental-L1-concepts.py
Each check names its ledger row (docs/reports/audit-mental-1-3-ledger.md).
Exit 0 means every checked claim holds. A check that fails because the content is
wrong would be marked EXPECTED_FAIL and kept failing; this level has none.
Claims that are true only under a hypothesis the text drops are demonstrated and
printed as "note" lines (findings in docs/reviews/audit-mental-1-3.md), not asserted.
"""
import json
import os
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


# ---- l1: adding from the left, bridging through ten
def left_to_right():
    # the split a + b = (a + tens of b) + units of b, for every two-digit pair
    ok = all((a + 10 * (b // 10)) + b % 10 == a + b for a in range(10, 100) for b in range(10, 100))
    check("l1_split_identity", ok, "l1 screens[8].prose: a + b = (a + tens of b) + units of b")
    # bridging: when the units cross a ten, hop to the ten then add the rest
    ok = True
    for a in range(10, 200):
        for u in range(1, 10):
            to_ten = (10 - a % 10) % 10
            if 0 < to_ten < u:
                ok &= (a + to_ten) % 10 == 0 and a + to_ten + (u - to_ten) == a + u
    check("l1_bridge", ok, "l1 screens[4], [5], [6]: hop to the ten, then the rest")
    # keyed slips: lost-ten = units digit kept, ten dropped; side = tens total and units total side by side
    d = load("l1-left-to-right")
    for idx, (a, b) in {2: (47, 36), 3: (58, 27), 5: (66, 58)}.items():
        w = d["screens"][idx]["widget"]
        side = int(f"{a // 10 + b // 10}{a % 10 + b % 10}")
        check(f"l1_s{idx}_key", w["answer"] == a + b and wrongs(w) == {"lost-ten": a + b - 10, "side": side},
              f"l1 screens[{idx}]: key and slip values for {a} + {b}")
    w = d["screens"][9]["widget"]
    check("l1_fills", F(str(w["answer"])) == F("47.65") + F("47.68")
          and F(str(wrongs(w)["lost-pound"])) == F("94.33") and F(str(wrongs(w)["same"])) == 2 * F("47.65"),
          "l1 screens[9]: two fills total £95.33; slips drop the pound, double the first price")
    w = d["quiz"][3]["widget"]
    check("l1_quiz_fills", F(str(w["answer"])) == F("23.85") + F("23.79") and F(str(wrongs(w)["same"])) == 2 * F("23.85"),
          "l1 quiz[3]: £47.64")
    # screens[1].explain: "Adding tens changes only the tens digit" (finding 1): false once the sum passes 100
    cross = [(a, t) for a in range(10, 100) for t in range(10, 100, 10) if (a + t) // 100 != a // 100]
    units_kept = all((a + t) % 10 == a % 10 for a in range(10, 100) for t in range(10, 100, 10))
    check("l1_units_ride_along", units_kept, "l1 screens[1].explain: the units digit never changes when tens are added")
    note("l1_tens_digit_only", f"{len(cross)} of 810 (two-digit a, tens jump) pairs also change the hundreds digit, "
         "for example 66 + 50 = 116 in screens[5] (finding 1, not asserted)")


# ---- l2: round, then adjust, and the direction of the correction
def round_adjust():
    ok = all(a + b == a + (b + d) - d and a - b == a - (b + d) + d
             for a in range(0, 200) for b in range(0, 100) for d in range(-5, 6))
    check("l2_identities", ok, "l2 screens[7].prose: a + b = a + (b + d) - d and a - b = a - (b + d) + d")
    d = load("l2-round-and-adjust")
    # wrong-way slips: the correction applied with the wrong sign; no-fix: no correction
    cases = {1: (54, 29, +1), 3: (67, 38, +1), 4: (46, 97, +1), 5: (47, 39, +1)}
    for idx, (a, b, sgn) in cases.items():
        w = d["screens"][idx]["widget"]
        r = -(-b // 10) * 10 if b < 90 else 100
        gap = r - b
        ws = wrongs(w)
        check(f"l2_s{idx}", w["answer"] == a + b and ws["no-fix"] == a + r and ws["wrong-way"] == a + r + gap,
              f"l2 screens[{idx}]: {a} + {b}, no-fix and wrong-way slips")
    # subtraction: taking away too much gives too little, so the correction is added
    ok = all((a - (b + g)) < a - b and (a - (b + g)) + g == a - b for a in range(50, 200) for b in range(10, 100) for g in range(1, 6))
    check("l2_subtract_direction", ok, "l2 screens[6], [7], summary.trap: after rounding the subtrahend up, give the gap back")
    w = d["screens"][9]["widget"]
    check("l2_profit", F(str(w["answer"])) == F("72.40") - F("48.98") == F("72.40") - 49 + F("0.02")
          and F(str(wrongs(w)["wrong-way"])) == F("72.40") - 49 - F("0.02"), "l2 screens[9]: £23.42")
    w = d["quiz"][3]["widget"]
    check("l2_quiz_profit", F(str(w["answer"])) == F("61.25") - F("35.97"), "l2 quiz[3]: £25.28")


# ---- l3: complements to 100 and counting up
def complements():
    # screens[2].explain: "It works for every pair, except numbers ending in 0."
    holds = [n for n in range(1, 100) if n // 10 + (100 - n) // 10 == 9 and n % 10 + (100 - n) % 10 == 10]
    fails = [n for n in range(1, 100) if n not in holds]
    check("l3_complement_rule", fails == list(range(10, 100, 10)) and len(holds) == 90,
          "l3 screens[2].explain: tens to 9 and units to 10 for every n from 1 to 99 except those ending in 0")
    note("l3_rule_without_exception", "screens[3].prose, summary.ideas[2] and quiz[1].prose state the rule with no "
         f"exception; it fails digit by digit on {len(fails)} of 99 numbers, and on every price ending in 0p (finding 2, not asserted)")
    # quiz[1]: every digit to 9, the last to 10, for prices in pence with a non-zero last digit
    def rule(p):  # p in pence below 10000, as a 4-digit string
        s = f"{p:04d}"
        digs = [9 - int(c) for c in s[:-1]] + [10 - int(s[-1])]
        return digs
    ok, bad = 0, 0
    for p in range(1, 10000):
        digs = rule(p)
        if all(0 <= x <= 9 for x in digs) and int("".join(map(str, digs))) == 10000 - p:
            ok += 1
        else:
            bad += 1
    check("l3_pence_rule", ok == 9000 and bad == 999, "l3 quiz[1].prose: the digit rule gives the change from £100 exactly when the last digit is not 0")
    # the corrected rule (finding 2 fix): digits to 9, the last non-zero digit to 10, end zeros stay 0
    def general(p):
        s = f"{p:04d}"
        k = max(i for i, c in enumerate(s) if c != "0")
        digs = [9 - int(c) for c in s[:k]] + [10 - int(s[k])] + [0] * (len(s) - k - 1)
        return int("".join(map(str, digs)))
    check("l3_pence_rule_general", all(general(p) == 10000 - p for p in range(1, 10000)),
          "finding 2 fix: with 'the last digit that is not 0' the rule gives the change from £100 for every amount")
    d = load("l3-making-100")
    w = d["quiz"][1]["widget"]
    check("l3_change", F(str(w["answer"])) == 100 - F("37.45"), "l3 quiz[1]: change £62.55")
    # counting up: hop to the next ten, then tens, then the rest, whenever the gap reaches the next ten
    ok = True
    for a in range(1, 200):
        for b in range(a + 1, 300):
            nxt = -(-a // 10) * 10
            if nxt <= b:
                hop, tens, rest = nxt - a, (b // 10) * 10 - nxt, b % 10
                ok &= hop + tens + rest == b - a and tens >= 0
    check("l3_count_up", ok, "l3 screens[8].prose: b - a = hop to the next ten + tens + the rest")
    # the paper slips keyed in the lesson
    def smaller(b, a):  # smaller digit from larger in each column
        sb, sa = str(b), str(a).rjust(len(str(b)), "0")
        return int("".join(str(abs(int(x) - int(y))) for x, y in zip(sb, sa)))
    for idx, (b, a) in {4: (83, 47), 5: (132, 68), 6: (92, 86)}.items():
        w = d["screens"][idx]["widget"]
        ws = wrongs(w)
        check(f"l3_s{idx}", w["answer"] == b - a and ws["smaller"] == smaller(b, a) and ws["kept-ten"] == b - a + 10,
              f"l3 screens[{idx}]: {b} - {a}, column slips")
    # spreads
    check("l3_spread", d["screens"][9]["widget"]["answer"] == 4813 - 4786 == 14 + 13 and d["quiz"][3]["widget"]["answer"] == 2411 - 2394,
          "l3 screens[9], quiz[3]: spreads 27p and 17p")


# ---- l4: pairing, signs, running totals, and the rounded-estimate bound
def running_totals():
    # units that add to 10 pair into a whole ten, always
    ok = all((a + b) % 10 == 0 for a in range(1, 200) for b in range(1, 200) if (a % 10 + b % 10) == 10)
    check("l4_pairs", ok, "l4 screens[1].explain, summary.ideas[0]: units adding to 10 make a whole ten")
    # screens[2]: exactly one number has no partner
    nums = [18, 25, 31, 15, 22]
    partnered = {x for i, x in enumerate(nums) for j, y in enumerate(nums) if i != j and (x % 10 + y % 10) == 10}
    check("l4_odd_one", [x for x in nums if x not in partnered] == [31] and sum(nums) == 111, "l4 screens[2]: 31 is the only unpaired number; total 111")
    # sign rule
    ok = all(a - b + c == a + (c - b) for a in range(0, 100) for b in range(0, 100) for c in range(0, 100, 7))
    check("l4_sign_identity", ok, "l4 screens[8].prose, summary.formula: a - b + c = a + (c - b)")
    check("l4_trap", 70 - 18 + 12 == 64 and 70 - (18 + 12) == 40 and 70 + 18 + 12 == 100, "l4 screens[7]: 64; Cara's 40; all-added 100")
    # estimate bound: |sum - sum of rounded| <= sum of |moves| (triangle inequality), and each move <= 5
    import random
    rng = random.Random(4)
    ok = True
    for _ in range(20000):
        xs = [rng.randint(1, 99) for _ in range(4)]
        rs = [int(x / 10 + 0.5) * 10 for x in xs]
        moves = [abs(x - r) for x, r in zip(xs, rs)]
        ok &= abs(sum(xs) - sum(rs)) <= sum(moves) <= 5 * len(xs)
    check("l4_estimate_bound", ok, "l4 screens[5], quiz[3], homework-1 items[7]: the true total lies within the summed moves of the estimate")
    for xs, est, bound, claimed in [([48, 31, 67, 22], 170, 8, 146), ([29, 52, 38, 71], 190, 6, 170), ([58, 23, 41, 87], 210, 9, 229)]:
        rs = [int(x / 10 + 0.5) * 10 for x in xs]
        check(f"l4_estimate_{est}", sum(rs) == est and sum(abs(x - r) for x, r in zip(xs, rs)) == bound and abs(claimed - est) > bound,
              f"estimate {est}, bound {bound}, {claimed} ruled out")
    check("l4_left_out", 48 + 31 + 67 == 146, "l4 screens[5].explain: 146 is the total without the 22")
    check("hw1_check_options", abs(205 - 210) <= 9 and 58 + 23 + 41 + 87 == 209 and abs(229 - 210) > 9,
          "homework-1 items[7]: only 229 falls outside 201 to 219")
    # quiz[3] option b: "Each number moved by at most 2 ..., so the total can be off by no more than 6" (finding 3)
    moves = [abs(x - int(x / 10 + 0.5) * 10) for x in [29, 52, 38, 71]]
    note("l4_quiz3_inference", f"moves are {moves}, summing to {sum(moves)}; 'each at most 2' over four numbers only gives "
         f"at most {2 * len(moves)}, so the stated 'so ... no more than 6' does not follow (finding 3, not asserted)")
    # running totals keyed in tables
    d = load("l4-running-total")
    tot, run = 0, []
    for step in [38, -12, 45, -29, 57]:
        tot += step
        run.append(tot)
    keyed = [r[1]["answer"] for r in d["screens"][4]["widget"]["rows"][1:]]
    check("l4_running", run == keyed == [38, 26, 71, 42, 99], "l4 screens[4]: running total")
    pnl, run = F(0), []
    for step in ["12.40", "-7.85", "23.10", "-15.65"]:
        pnl += F(step)
        run.append(pnl)
    keyed = [F(str(r[2]["answer"])) for r in d["screens"][10]["widget"]["rows"]]
    check("l4_pnl", run == keyed, "l4 screens[10]: running P&L")
    check("l4_below_zero", 0 + 35 - 52 == -17 and -17 + 28 == 11, "l4 screens[6]: 35, -17, 11")
    drill = {"46+37": 83, "58+29": 87, "100-64": 36, "82-47": 35, "67+58": 125, "93-38": 55, "35+98": 133, "121-56": 65, "49+36": 85, "145-99": 46}
    keyed = [r[1]["answer"] for r in d["screens"][9]["widget"]["rows"]]
    check("l4_drill", [eval(k) for k in drill] == list(drill.values()) == keyed, "l4 screens[9]: ten sums")


# ---- review-1 and homework-1
def review_homework():
    r = load("review-1")
    ans = [it["widget"].get("answer") for it in r["items"]]
    check("review1_keys", ans[:8] == [68 + 57, 84 - 39, 100 - 73, 15 + 28 + 35 + 12, 82 - 47, 3614 - 3588, 77.55, 143 - 96]
          and F("29.99") + F("47.56") == F("77.55") and 85 - 35 + 15 == 65, "review-1 items[0..8]")
    run = [F("8.25"), F("8.25") - F("13.50"), F("8.25") - F("13.50") + F("6.40")]
    check("review1_pnl", run == [F(str(x[2]["answer"])) for x in r["items"][9]["widget"]["rows"]], "review-1 items[9]: £8.25, -£5.25, £1.15")
    h = load("homework-1")
    check("hw1_keys", h["items"][0]["widget"]["answer"] == 79 + 86 and h["items"][1]["widget"]["answer"] == 161 - 77 == 23 + 61
          and F(str(h["items"][3]["widget"]["answer"])) == F("36.47") + F("36.53") + F("36.50")
          and h["items"][5]["widget"]["answer"] == 10004 - 9987 and h["items"][8]["widget"]["answer"] == 173 - 88,
          "homework-1 items[0], [1], [3], [5], [8]")
    # h-why-complement: for 10t + u with u != 0 the complement is (9 - t) tens and (10 - u) units
    ok = all(100 - (10 * t + u) == 10 * (9 - t) + (10 - u) for t in range(0, 10) for u in range(1, 10))
    check("hw1_complement_proof", ok, "homework-1 items[2]: complement of 10t + u is 10(9 - t) + (10 - u) when u is not 0")
    pos, run = 0, []
    for step in [45, -28, 36, -17, 9, -40]:
        pos += step
        run.append(pos)
    check("hw1_position", run == [x[1]["answer"] for x in h["items"][4]["widget"]["rows"]] and 45 + 36 + 9 == 90 and 28 + 17 + 40 == 85,
          "homework-1 items[4]: position 45, 17, 53, 36, 45, 5")
    day = F("-18.60") + F("34.95") - F("52.40") + F("41.15")
    check("hw1_day", day == F(str(h["items"][6]["widget"]["answer"])) == F("76.10") - F("71.00"), "homework-1 items[6]: £5.10")
    # longform
    cost = F("47.96") + F("48.04")
    p1, p2 = F("51.25") - F("47.96"), F("51.25") - F("48.04")
    check("hw1_longform", cost == 96 and (p1, p2) == (F("3.29"), F("3.21")) and p1 + p2 == F("6.50") == 2 * F("51.25") - cost
          and F("51.42") - F("51.25") == F("0.17") and 2 * F("51.42") == F("102.84"), "homework-1 items[9] model (a) to (c)")
    moved = [abs(F(x) - round(F(x))) for x in ["47.96", "48.04", "51.25", "51.25"]]
    est = 2 * 51 - (48 + 48)
    check("hw1_longform_estimate", est == 6 and max(moved) <= F("0.25") and sum(moved) <= 1 and F("16.50") - est > 10,
          "homework-1 items[9] model (d): estimate £6, moved by at most £1 in all, £16.50 is more than £10 away")


if __name__ == "__main__":
    left_to_right()
    round_adjust()
    complements()
    running_totals()
    review_homework()
    print("L1 concepts: all checks passed")
