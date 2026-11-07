"""functions level 1 (Functions): every graded key, wrong[] value and stated number, recomputed (second read, session V).
Run: python3 docs/reports/functions-L1-numbers.py   (exit 0 on correct content)
Checks marked FINDING in docs/reviews/review-functions-1-2.md fail while the content is wrong and pass once it is fixed."""
import os
import sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("functions", 1)
E = lv.expect


def W(f, sect, i, k, v):
    E(f, f"{sect}[{i}].widget.wrong[{k}].value", v)


# ---------- l1 machines ----------
f = lambda x: 2 * x + 3
for x, y in [(1, 5), (2, 7), (5, 13)]:
    lv.claim(f(x) == y, f"l1 screens[1] table row {x} -> {y} fits 2x + 3")
E("l1", "screens[1].widget.answer", f(10))
W("l1", "screens", 1, 0, 2 * 10)            # double-only
W("l1", "screens", 1, 1, (10 + 3) * 2)      # add-first
W("l1", "screens", 1, 2, 10 + 3)            # add-only
E("l1", "screens[1].feedback.correct", 20)
E("l1", "screens[1].hints[1].text", 13)
E("l1", "screens[2].widget.answer", f(2) - f(1))
W("l1", "screens", 2, 0, 1)                 # same: keeps pace
W("l1", "screens", 2, 1, 3)                 # plus3
E("l1", "screens[2].hints[2].text", f(2))
E("l1", "screens[3].prose", f(1))
E("l1", "screens[3].widget.answer", f(-4))
W("l1", "screens", 3, 0, 2 * 4 + 3)         # lost-sign
W("l1", "screens", 3, 1, (-4 + 3) * 2)      # add-first
W("l1", "screens", 3, 2, 2 * -4 - 3)        # subtracted
E("l1", "screens[3].hints[2].text", -8)
g = lambda x: x * x - 1
E("l1", "screens[4].widget.answer", g(-3))
W("l1", "screens", 4, 0, -(3 ** 2) - 1)     # neg-square
W("l1", "screens", 4, 1, 2 * -3 - 1)        # doubled
W("l1", "screens", 4, 2, (-3 - 1) ** 2)     # subtract-first
lv.claim(g(3) == g(-3) == 8, "l1 screens[4] explain g(3) = g(-3) = 8")
E("l1", "screens[5].widget.answer", 7)
W("l1", "screens", 5, 0, 700)
W("l1", "screens", 5, 1, 107)
W("l1", "screens", 5, 2, 100)
lv.claim(f(2) == 7 and f(3) == 9 and f(5) == 13 and f(2) + f(3) - f(5) == 3, "l1 screens[6] f(5) is 3 less than f(2) + f(3)")
E("l1", "screens[6].widget.options[0].why", 13)
E("l1", "screens[6].widget.options[1].why", 16)
E("l1", "screens[6].hints[2].text", 16)
lv.claim(3 * (-2) ** 2 == 12 and 3 * -(2 ** 2) == -12 and (3 * -2) ** 2 == 36, "l1 screens[7] 3(-2)^2 = 12; slips -12 and 36")
E("l1", "screens[7].widget.options[1].why", -12)
E("l1", "screens[7].feedback.correct", 12)
h = lambda x: 5 * (x - 4)
lv.claim(h(6) == 10 and 5 * 6 - 4 == 26 and all(h(x) == 5 * x - 20 for x in range(-5, 6)), "l1 screens[8] 5(x - 4) = 5x - 20; x = 6 gives 10 against 26")
E("l1", "screens[8].feedback.byKey.order", 26)
gain = F("13.15") - F("12.40")
lv.claim(gain == F("0.75"), "l1 screens[9] gain per share 0.75")
P = lambda q: gain * q - 6
E("l1", "screens[9].canvas.params.rows[0][1]", float(P(100)))
E("l1", "screens[9].canvas.params.rows[1][1]", float(P(200)))
E("l1", "screens[9].widget.answer", float(P(240)))
W("l1", "screens", 9, 0, float(gain * 240))                 # no-fee
W("l1", "screens", 9, 1, float(F("13.15") * 240 - 6))       # revenue: sale price per share, fee once
W("l1", "screens", 9, 2, float(gain * 240 - 12))            # double-fee
E("l1", "screens[9].hints[2].text", 180)
f4 = lambda x: 4 * x - 1
E("l1", "quiz[0].widget.answer", f4(-2))
W("l1", "quiz", 0, 0, 4 * 2 - 1)
W("l1", "quiz", 0, 1, 4 * (-2 - 1))
lv.claim((-3) ** 2 + (-3) == 6 and -(3 ** 2) + (-3) == -12 and 9 + 3 == 12, "l1 quiz[1] g(-3) = 6; slips -12 and 12")
lv.claim((4 + 6) / 2 == 5 and 4 / 2 + 6 == 8 and 2 * (4 + 6) == 20, "l1 quiz[2] x = 4 checks: 5, 8, 20")
E("l1", "quiz[3].widget.answer", -9)
W("l1", "quiz", 3, 0, 0)
W("l1", "quiz", 3, 1, 9)
lv.claim(F("8.25") - F("8.60") == F("-0.35"), "l1 quiz[4] loss 0.35 per share")
E("l1", "quiz[4].explain.text", -0.35)

# ---------- l2 table to rule ----------
lv.claim([3 * x + 1 for x in range(1, 5)] == [4, 7, 10, 13], "l2 screens[0] rows fit 3x + 1")
E("l2", "screens[0].widget.answer", 16)
W("l2", "screens", 0, 0, 14)
W("l2", "screens", 0, 1, 26)
lv.claim(2 + 3 == 5 and 4 * 2 == 8 and 3 * 1 + 4 == 7, "l2 screens[1] distractor checks: x + 3 at 2 is 5, 4x at 2 is 8, 3x + 4 at 1 is 7")
lv.claim([4 * x + 5 for x in range(4)] == [5, 9, 13, 17] and 5 * 0 + 4 == 4 and 2 + 4 == 6, "l2 screens[2] 4x + 5 fits; slips give 4 and 6")
lv.claim([3 * x + 2 for x in (1, 3, 5, 7)] == [5, 11, 17, 23] and 6 * 3 - 1 == 17 and 3 + 4 == 7, "l2 screens[3] 3x + 2 fits; 6x - 1 gives 17 at 3; x + 4 gives 7")
E("l2", "screens[4].widget.answer", 36)
W("l2", "screens", 4, 0, 25)
W("l2", "screens", 4, 1, 16 + 7 + 7)       # last-climb kept: f(5) = 23, f(6) = 30
lv.claim(all(x * x == y for x, y in [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]), "l2 screens[4] rows fit x^2")
inv = lambda y: F(y - 1, 3)
E("l2", "screens[5].widget.answer", float(inv(31)))
W("l2", "screens", 5, 0, 3 * 31 + 1)                         # forward
W("l2", "screens", 5, 1, round(31 / 3 - 1, 4))               # wrong-order
W("l2", "screens", 5, 2, round((31 + 1) / 3, 4))             # add-back
lv.claim(3 * 2 + 1 == 7 and 3 * 5 + 1 == 16, "l2 screens[5] rows 2 -> 7, 5 -> 16")
# four rows 2, 4, 8, 16 then f(5): doubling, 32. The climbs 2, 4, 8 are not constant, so the quiz[2] method gives no rival answer.
t6 = [2 ** x for x in range(1, 6)]
lv.claim(t6 == [2, 4, 8, 16, 32] and [t6[i + 1] - t6[i] for i in range(3)] == [2, 4, 8] and 2 * 5 == 10 and t6[3] + 8 == 24, "l2 screens[6] rows 2, 4, 8, 16 double; f(5) = 32; slips 10 and 24")
q = lambda x: x * x - x + 2
lv.claim([q(1), q(2), q(3), q(4)] == [2, 4, 8, 14] and q(4) != 16, "l2 screens[6] the rival x^2 - x + 2 fails the fourth row (14, not 16)")
lv.claim(lv.files['l2-table-to-rule']['screens'][6]['canvas']['params']['rows'] == [["1", "2"], ["2", "4"], ["3", "8"], ["4", "16"], ["5", "?"]], "l2 screens[6] table has four known rows and asks f(5)")
E("l2", "screens[6].question", "What is $f(5)$?")
E("l2", "screens[6].widget.options[1].text", "$32$")
E("l2", "screens[6].widget.options[0].text", "$10$")
E("l2", "screens[6].widget.options[2].text", "$24$")
E("l2", "screens[6].hints[2].text", "so the next is 32")
E("l2", "screens[6].feedback.correct", "$f(5) = 32$")
E("l2", "screens[6].explain.text", "$f(5) = 32$")
lv.claim(lv.files['l2-table-to-rule']['screens'][6]['explain']['canvas']['values'] == {"r4c1": "32"}, "l2 screens[6] explain puts 32 in the fifth row")
lv.claim(2 * 3 == 6, "l2 screens[6] 2x gives f(3) = 6")
E("l2", "screens[7].widget.answer", 3)
W("l2", "screens", 7, 0, 6)
W("l2", "screens", 7, 1, round(1 / 3, 4))
lv.claim(1 - 3 * 2 == -5 and 3 * 6 - 5 == 13 and 3 * 4 - 5 == 7, "l2 screens[8] c = -5; checks 13 and 7")
P2 = lambda s: 40 * (F(s) - F("15.25"))
lv.claim(P2("15") == -10 and P2("16") == 30 and P2("17.50") == 90, "l2 screens[9] table rows -10, 30, 90")
lv.claim(40 * 16 == 640 and F("16") - F("15.25") == F("0.75") and 60 * 16 - 930 == 30 and 90 - 30 == 60, "l2 screens[9] distractor values 640, 0.75, 60s - 930 through row 2")
E("l2", "screens[9].hints[2].text", -610)
lv.claim([7 - 2 * x for x in range(4)] == [7, 5, 3, 1], "l2 quiz[0] 7 - 2x fits")
E("l2", "quiz[1].widget.answer", (25 + 3) / 4)
W("l2", "quiz", 1, 0, 4 * 25 - 3)
W("l2", "quiz", 1, 1, 25 / 4 + 3)
W("l2", "quiz", 1, 2, (25 - 3) / 4)
lv.claim([x * x + 2 for x in range(1, 6)] == [3, 6, 11, 18, 27], "l2 quiz[2] x^2 + 2 fits and gives 27")
E("l2", "quiz[2].widget.answer", 27)
W("l2", "quiz", 2, 0, 18 + 7)
lv.claim([2 * x + 2 for x in (0, 5, 10)] == [2, 12, 22], "l2 quiz[3] 2x + 2 fits")
E("l2", "quiz[3].widget.answer", 42)
W("l2", "quiz", 3, 0, 10 * 20 + 2)
W("l2", "quiz", 3, 1, 2 * 15 + 2)

# ---------- l3 what goes in ----------
lv.claim(all(12 / x == y for x, y in [(4, 3), (3, 4), (2, 6), (1, 12)]), "l3 screens[0] rows of 12/x")
lv.claim(min(x * x / 4 for x in range(-8, 13)) == 0 and (-2) ** 2 == 4 and 3 ** 2 == 9, "l3 screens[1] x^2 on [-2, 3]: least 0, ends 4 and 9")
E("l3", "screens[2].feedback.correct", 9)
E("l3", "screens[2].feedback.byKey.ends", 4)
lv.claim(2 - 2 == 0 and 0 - 2 == -2 and -2 - 2 == -4, "l3 screens[3] bottoms at 2, 0, -2: 0, -2, -4")
lv.claim(10 - 3 == 7 and 10 - 8 == 2, "l3 screens[4] f(3) = 7, f(8) = 2")
E("l3", "screens[4].feedback.correct", 2)
E("l3", "screens[4].feedback.correct", 7)
lv.claim((-3) ** 2 == 9 and 2 ** 2 == 4, "l3 screens[5] ends -3 -> 9 (open) and 2 -> 4; x = 0 -> 0")
lv.claim((-1) ** 2 + 1 == 2 and min(x * x + 1 for x in range(-5, 6)) == 1, "l3 screens[6] f(-1) = 2; least output 1")
lv.claim(5 * 1 == 5 and 5 * 4 == 20, "l3 screens[7] range 5 to 20")
lv.claim(100 - 0 == 100, "l3 screens[8] put pays 100 at S = 0")
lv.claim(-4 + 4 == 0 and 4 + 4 == 8 and 0 + 4 == 4, "l3 quiz[0] bottoms 0, 8, 4")
lv.claim(2 * -1 - 1 == -3 and 2 * 3 - 1 == 5, "l3 quiz[1] range -3 to 5")
for amt, qn, ok in [("37.50", 75, True), ("10.25", F("20.5"), False), ("60", 120, False), ("-5", -10, False)]:
    need = F(amt) / F("0.5")
    lv.claim(need == qn and ((need.denominator == 1 and 0 <= need <= 100) == ok), f"l3 quiz[2] £{amt} needs q = {need}")
# FINDING (misleading): screens[4] wrong region `reversed` (x 6.7 to 7.3) also holds the correct target of `hi` (7); drag-point checks every region against every point
_s4 = lv.files['l3-what-goes-in']['screens'][4]['widget']
_hit = [r['id'] for r in _s4.get('wrong', []) for p in _s4['points'] if r['region']['x'][0] <= p['target'][0] <= r['region']['x'][1]]
lv.claim(not _hit, "l3 screens[4] no wrong[] region holds a correct target", f"regions {_hit} hold a correct target")

# ---------- l4 one output ----------
lv.claim(2 ** 2 == 4 and (-2) ** 2 == 4, "l4 screens[1] x = 4 meets y = 2 and y = -2")
lv.claim((-2) ** 2 - 4 == 0 and 2 ** 2 - 4 == 0, "l4 screens[2] -2 and 2 share output 0")
E("l4", "screens[3].widget.answer", 3)
W("l4", "screens", 3, 0, 1)
W("l4", "screens", 3, 1, 2)
lv.claim(3 ** 2 == 9 and (-3) ** 2 == 9, "l4 screens[6] x = 0 meets the circle at 3 and -3")
E("l4", "screens[8].widget.answer", 8)
W("l4", "screens", 8, 0, 12)
W("l4", "screens", 8, 1, 10)
lv.claim(2 ** 2 == 4, "l4 quiz[1] input 4 gives 2 and -2")
# quiz[3] has no canvas, so its prose must not say the graphs are drawn on one
E("l4", "quiz[3].prose", "Picture three graphs drawn on one pair of axes.")
lv.claim('canvas' not in lv.files['l4-one-output']['quiz'][3], "l4 quiz[3] has no canvas, so the prose asks the learner to picture the graphs")

# ---------- review-1 ----------
r0 = lambda x: 5 - 2 * x
E("review", "items[0].widget.answer", r0(-3))
W("review", "items", 0, 0, 5 - 2 * 3)
W("review", "items", 0, 1, (5 - 2) * -3)
lv.claim([3 * x + 3 for x in (2, 5, 8)] == [9, 18, 27] and 9 * 5 - 9 == 36 and 5 + 7 == 12 and 9 * 2 - 9 == 9, "review items[1] 3x + 3 fits; 9x - 9 gives 36 at 5; x + 7 gives 12")
lv.claim(2 * -1 + 1 == -1 and 2 * 3 + 1 == 7 and 2 * 0 + 1 == 1, "review items[2] range -1 to 7; f(0) = 1")
E("review", "items[4].widget.answer", 9.5 * 2 - 4)
W("review", "items", 4, 0, (9.5 + 4) / 2)
W("review", "items", 4, 1, (9.5 - 4) * 2)
loss = F("23.85") - F("24.60")
E("review", "items[7].widget.answer", float(loss * 120 - F("4.5")))
W("review", "items", 7, 0, float(-loss * 120 - F("4.5")))   # gain-sign
W("review", "items", 7, 1, float(loss * 120 + F("4.5")))    # fee-added
W("review", "items", 7, 2, float(loss * 120))               # no-fee
E("review", "items[7].explain.text", -90)

# ---------- homework-1 ----------
lv.claim(4 * 10 - 7 == 33 and 4 * (10 - 7) == 12, "homework items[0] x = 10: 33 against 12")
lv.claim([7 - 2 * x for x in (-2, 1, 4, 7)] == [11, 5, -1, -7], "homework items[1] 7 - 2x fits")
E("homework", "items[1].widget.answer", 7 - 2 * 10)
W("homework", "items", 1, 0, -6 * 10 + (11 - 12))      # climb-m: -6x through row 1, c = -1
W("homework", "items", 1, 1, 2 * 10 + 7)               # sign: +2 with c = 7
hq = lambda x: (x - 1) ** 2
lv.claim(hq(1) == 0 and hq(4) == 9 and hq(0) == 1 and hq(2) == 1, "homework items[2] (x - 1)^2: 0 at 1, 9 at 4, 1 at 0 and at 2")
fa = lambda x: 3 * x - 2
lv.claim(all(fa(a) + fa(b) - fa(a + b) == -2 for a in range(-4, 5) for b in range(-4, 5)), "homework items[3] f(a) + f(b) - f(a + b) = -2 always")
E("homework", "items[3].widget.answer", -2)
W("homework", "items", 3, 0, 0)
W("homework", "items", 3, 1, 2)
W("homework", "items", 3, 2, -4)
lv.claim(fa(1) + fa(2) - fa(3) == 1 + 4 - 7, "homework items[3] explain a = 1, b = 2: 1 + 4 - 7")
E("homework", "items[4].widget.answer", -4.5)
W("homework", "items", 4, 0, 0)
W("homework", "items", 4, 1, -120)
W("homework", "items", 4, 2, 4.5)
lv.claim(F(2 * 2 + 5, 3) == 3 and F(3 * 3 - 5, 2) == 2, "homework items[5] f(2) = 3 and g(3) = 2")
fee = lambda t: F(3) if t <= 500 else F("7.5") if t <= 2500 else F("0.004") * t
E("homework", "items[6].widget.answer", float(fee(500) + fee(2500) + fee(4000)))
W("homework", "items", 6, 0, float(F("7.5") + F("0.004") * 2500 + F("0.004") * 4000))   # boundaries moved up
W("homework", "items", 6, 1, float(3 + F("7.5") + F("0.4") * 4000))                      # 0.4 for 0.4%
E("homework", "items[6].explain.text", 16)
Pq = lambda q: F("0.65") * q - 15
lv.claim(F("19.05") - F("18.40") == F("0.65"), "homework items[7] gain per share 0.65")
for q, v in [(10, "-8.50"), (100, "50"), (1000, "635"), (1, "-14.35"), (23, "-0.05"), (24, "0.60")]:
    lv.claim(Pq(q) == F(v), f"homework items[7] model P({q}) = {v}")
lv.claim(23 < F(15) / F("0.65") < 24 and round(15 / 0.65, 2) == 23.08, "homework items[7] model 15 / 0.65 = 23.08")
lv.claim((F(50) + 15) / F("0.65") == 100, "homework items[7] model q = (50 + 15)/0.65 = 100")
lv.claim(all(Pq(q) != 0 for q in range(1, 1001)), "homework items[7] model: £0.00 is never reached")
E("homework", "items[7].model", -14.35)
E("homework", "items[7].model", 23.08)

lv.check_wrongs()
lv.report()
