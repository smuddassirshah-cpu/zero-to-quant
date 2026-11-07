"""equations level 1 (Expressions): every graded key, wrong[] value and stated number, recomputed (second read, session V).
Run: python3 docs/reports/equations-L1-numbers.py   (exit 0 on correct content)
Checks marked FINDING in docs/reviews/review-equations-1-2.md fail while the content is wrong and pass once it is fixed."""
import os
import sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("equations", 1)
E = lv.expect


def lin(a, b):
    """a*n + b as a function."""
    return lambda n: a * n + b


# ---------- l1 letters for numbers ----------
tray = 3 * 5 + 4
E("l1", "screens[0].widget.answer", tray)
E("l1", "screens[0].widget.wrong[0].value", 3 + 5 + 4)          # added
E("l1", "screens[0].widget.wrong[1].value", 7 * 5)              # all-envelopes
E("l1", "screens[0].widget.wrong[2].value", 3 * (5 + 4))        # coins-inside
E("l1", "screens[0].widget.wrong[3].value", 5 + 4)              # one-envelope
E("l1", "screens[0].explain.text", tray)
E("l1", "screens[0].hints[2].text", 15)
t6 = 3 * 6 + 4
E("l1", "screens[1].widget.points[0].target[0]", t6)
import json
_s1 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'equations', 'l1-letters-for-numbers.json')))['screens'][1]['widget']['wrong']
_reg = {w['id']: w['region']['x'] for w in _s1}
for wid, v in [("added", 3 + 6 + 4), ("one-envelope", 6 + 4), ("coins-inside", 3 * (6 + 4)), ("old", tray)]:
    lv.claim(_reg[wid][0] <= v <= _reg[wid][1], f"l1 screens[1] drag region {wid} holds {v}")
E("l1", "screens[1].hints[2].text", 18)
E("l1", "screens[1].explain.text", 22)
# screens[2]: 2 envelopes and 5 coins -> 2n + 5; slips 7n, 2 + 5n, n + 7
lv.claim(lin(2, 5)(3) != lin(7, 0)(3) and lin(2, 5)(3) != (2 + 5 * 3), "l1 screens[2] 2n + 5 differs from 7n and 2 + 5n")
# FINDING (misleading): option one-each n + 7 is n + 2 + 5, one n plus the count; "counted the 2 envelopes as £2" gives 2 + 5 = 7, no n.
lv.stated("l1", "screens[2].widget.options[3].why", "You counted the 2 envelopes as £2.", False)
# screens[3] and [6]: broker 3 + 2n
cost = lin(2, 3)
E("l1", "screens[4].widget.answer", cost(50))
E("l1", "screens[4].canvas.params.rows[0]", cost(1))
E("l1", "screens[4].canvas.params.rows[1]", cost(10))
E("l1", "screens[4].canvas.params.rows[1]", 2 * 10)
E("l1", "screens[4].widget.wrong[0].value", 250 + 3)            # side-by-side "250"
E("l1", "screens[4].widget.wrong[1].value", (3 + 2) * 50)       # plus-first
E("l1", "screens[4].widget.wrong[2].value", 3 + 2 + 50)         # added
E("l1", "screens[4].explain.text", 100)
E("l1", "screens[4].explain.text", 103)
# screens[5]: 2n + 4 against 3n
L, R = lin(2, 4), lin(3, 0)
E("l1", "screens[5].canvas.state.caption", L(3))
E("l1", "screens[5].canvas.state.caption", R(3))
E("l1", "screens[5].widget.options[1].why", L(5))
E("l1", "screens[5].widget.options[1].why", R(5))
E("l1", "screens[5].widget.options[2].why", L(4))
lv.claim(L(4) == R(4) == 12 and all(L(n) != R(n) for n in range(-50, 51) if n != 4), "l1 screens[5]: n = 4 is the one balancing value")
lv.claim(R(5) > L(5), "l1 screens[5]: right pan heavier at n = 5")
# screens[6] trap at n = 4
E("l1", "screens[6].widget.options[0].text", cost(4))
E("l1", "screens[6].widget.options[1].text", (3 + 2) * 4)
E("l1", "screens[6].widget.options[2].text", 3 + 24)
E("l1", "screens[6].widget.options[3].text", 3 + 2 + 4)
E("l1", "screens[6].explain.text", (3 + 2) * 4 - cost(4))       # overcharges by 9
E("l1", "screens[6].hints[2].text", 8)
# screens[7]
E("l1", "screens[7].widget.options[0].text", 5 * 7)
E("l1", "screens[7].widget.options[1].text", 57)
E("l1", "screens[7].widget.options[2].text", 5 + 7)
# screens[8] gym 25 + 12m
E("l1", "screens[8].explain.text", 25 + 12 * 1)
# screens[9] commission 1.50 + 0.02n against the table
com = lambda n: F(150, 100) + F(2, 100) * n
for n, txt in [(100, "3.50"), (500, "11.50"), (2000, "41.50")]:
    lv.claim(com(n) == F(txt), f"l1 screens[9] table: {n} shares cost £{txt}")
E("l1", "screens[9].widget.options[1].why", float(F(150, 100) + 2 * 100), fmt="201.50")
E("l1", "screens[9].widget.options[2].why", float(F(152, 100) * 100))
E("l1", "screens[9].widget.options[3].why", float(F(2, 100) + F(150, 100) * 100), fmt="150.02")
E("l1", "screens[9].explain.text", float(F(2, 100) * 2000))
E("l1", "screens[9].explain.text", float(com(2000)), fmt="41.50")
# quiz
E("l1", "quiz[1].widget.answer", 4 + 3 * 0)
E("l1", "quiz[1].widget.wrong[0].value", 4 + 3)
E("l1", "quiz[1].widget.wrong[1].value", 4 + 30)
E("l1", "quiz[1].widget.wrong[2].value", 0)
E("l1", "quiz[3].widget.answer", 5 * 6 - 4)
E("l1", "quiz[3].widget.wrong[0].value", 56 - 4)
E("l1", "quiz[3].widget.wrong[1].value", (5 - 4) * 6)
E("l1", "quiz[3].widget.wrong[2].value", 5 + 6 - 4)
E("l1", "quiz[2].widget.wrong[0].tex", 162.4)                    # 12.4 + 150

# ---------- l2 like terms ----------
pile = lin(3, 8)
E("l2", "screens[1].widget.points[0].target[0]", pile(4))
lv.claim(2 * 4 + 3 + 4 + 5 == pile(4), "l2 screens[1]: term by term 8 + 3 + 4 + 5 = 20")
lv.claim(15.7 <= lin(2, 8)(4) <= 16.3, "l2 screens[1] lost-one region holds 2n + 8 = 16")
lv.claim(26.7 <= 3 * 4 + 15 <= 27.3, "l2 screens[1] times region holds 3n + 15 = 27")
lv.claim(10.7 <= 2 * 4 + 3 <= 11.3, "l2 screens[1] tray-a region holds 2n + 3 = 11")
E("l2", "screens[0].widget.options[1].text", 2 + 3 + 1 + 5)      # 11n
E("l2", "screens[0].widget.options[3].text", 3 * 5)              # 3n + 15
E("l2", "screens[2].explain.text", 4 + 2)
E("l2", "screens[4].widget.options[1].text", 6 + 4)              # 7n + 10
E("l2", "screens[4].widget.options[1].text", 5 + 2)
E("l2", "screens[4].widget.options[0].text", 5 - 2)
long2 = lambda n: 4 * n + 7 + 2 * n + 3
E("l2", "screens[5].widget.answer", long2(2))
E("l2", "screens[5].widget.wrong[0].value", 16 * 2)
E("l2", "screens[5].widget.wrong[1].value", long2(1))
lv.claim(long2(1) == 16 * 1, "l2 screens[5]: both give 16 at n = 1")
lv.claim(all(long2(n) == 6 * n + 10 for n in range(-5, 6)), "l2 screens[5]: right answer 6n + 10")
E("l2", "screens[6].hints[2].text", lin(3, 2)(10))
E("l2", "screens[6].hints[2].text", 5 * 10)
# FINDING (misleading): different letters need not stand for different amounts (n = m is allowed).
lv.stated("l2", "screens[7].widget.options[3].why", "so they stand for different amounts", False)
E("l2", "screens[7].hints[1].text", 7 - 2)
profit = lambda n: F(1310, 100) * n - F(1250, 100) * n - 8
E("l2", "screens[9].widget.options[0].text", 0.60)
E("l2", "screens[9].widget.options[1].text", 25.60)
E("l2", "screens[9].widget.options[3].text", -7.40)
lv.claim(F(60, 100) - 8 == F(-740, 100), "l2 screens[9]: 0.60 - 8 = -7.40")
E("l2", "screens[9].explain.text", float(profit(500)))
E("l2", "screens[9].explain.text", 300)
E("l2", "quiz[0].widget.options[1].text", 5 + 3 + 2 + 6)
E("l2", "quiz[0].widget.options[2].text", 5 * 2)
E("l2", "quiz[0].widget.options[3].text", 3 * 6)
E("l2", "quiz[2].widget.options[1].text", 8 + 5)
E("l2", "quiz[2].widget.options[2].text", -(-3 - 7))       # 3x - 10
E("l2", "quiz[2].widget.options[3].text", 3 + 4)

# ---------- l3 opening brackets ----------
E("l3", "screens[0].widget.answer", 3 * (5 + 2))
E("l3", "screens[0].widget.wrong[0].value", 3 * 5 + 2)
E("l3", "screens[0].widget.wrong[1].value", 3 + 5 + 2)
E("l3", "screens[0].widget.wrong[2].value", 3 * 5)
E("l3", "screens[3].explain.text", 4 * 5)
E("l3", "screens[4].widget.options[0].text", 5 * 2)
E("l3", "screens[4].widget.options[2].text", 5 + 2)
neg = lambda n: -2 * (n - 4)
E("l3", "screens[5].canvas.params.rows[0]", neg(0))
E("l3", "screens[5].canvas.params.rows[1]", neg(10))
E("l3", "screens[5].widget.options[3].why", 2 * 10 - 8)
lv.claim(all(neg(n) == -2 * n + 8 for n in range(-5, 6)), "l3 screens[5]: -2(n - 4) = -2n + 8")
E("l3", "screens[6].hints[2].text", 3 * (10 + 2))
E("l3", "screens[6].hints[2].text", 3 * 10 + 2)
E("l3", "screens[6].explain.text", 6 - 2)
E("l3", "screens[7].widget.options[0].text", 6 * 2)
B = F(625, 100)
E("l3", "screens[9].widget.options[0].text", float(40 * B))
E("l3", "screens[9].widget.options[2].text", float(40 + B))
E("l3", "screens[9].widget.options[3].why", float(4 * B))
E("l3", "screens[9].explain.text", float(40 * F(810, 100)))
E("l3", "screens[9].explain.text", float(40 * F(810, 100) + 40 * B))
E("l3", "quiz[2].widget.answer", 7 * (6 + 4))
E("l3", "quiz[2].widget.wrong[0].value", 7 * 6 + 4)
E("l3", "quiz[2].widget.wrong[1].value", 7 + 6 + 4)
E("l3", "quiz[2].explain.text", 7 * 4)
E("l3", "quiz[1].widget.options[2].text", 4 + 2)

# ---------- l4 putting brackets back ----------
E("l4", "screens[0].widget.options[3].text", 12 - 4)
rows = [(1, "6n", 9), (2, "3n", 4.5), (3, "2n", 3), (6, "n", 1.5)]
for h, _, w in rows:
    lv.claim(9 / h == w, f"l4 screens[1] table: 9 / {h} = {w}")
common = [h for h in (1, 2, 3, 6) if 6 % h == 0 and 9 % h == 0]
lv.claim(common == [1, 3], "l4 screens[1]: heights 1 and 3 leave whole widths")
E("l4", "screens[2].hints[2].text", 20 // 5)
E("l4", "screens[3].widget.options[1].why", 3 * 9)
E("l4", "screens[3].widget.options[2].why", 3 * (2 + 3))
E("l4", "screens[3].widget.options[3].why", 6 * 9)
f12 = [d for d in range(1, 13) if 12 % d == 0]
f18 = [d for d in range(1, 19) if 18 % d == 0]
lv.claim(f12 == [1, 2, 3, 4, 6, 12] and f18 == [1, 2, 3, 6, 9, 18], "l4 screens[4] factor lists")
lv.claim(max(set(f12) & set(f18)) == 6, "l4 screens[4] hcf(12, 18) = 6")
E("l4", "screens[4].widget.options[3].why", 6 * 18)
E("l4", "screens[5].widget.options[2].why", 7 * 7)
E("l4", "screens[6].widget.options[0].text", 5 * 10)
E("l4", "screens[6].hints[2].text", 10 // 5)
from math import gcd
E("l4", "screens[7].widget.answer", gcd(8, 20))
E("l4", "screens[9].widget.answer", 600 // 15)
for n, p in [(20, -300), (60, 300), (100, 900)]:
    lv.claim(15 * n - 600 == p, f"l4 screens[9] table: profit at {n} is {p}")
E("l4", "screens[9].widget.wrong[0].value", 600 - 15)
E("l4", "screens[9].widget.wrong[1].value", 600 * 15)
E("l4", "screens[9].widget.wrong[2].value", 600 + 15)
lv.claim(gcd(6, 15) == 3 and gcd(20, 30) == 10, "l4 quiz hcf(6, 15) = 3, hcf(20, 30) = 10")
E("l4", "quiz[2].widget.options[2].why", 81)

# ---------- review-1 ----------
E("review", "items[0].explain.text", float(F(280, 100) + F(160, 100) * 10), fmt="18.80")
E("review", "items[0].widget.options[1].text", float(F(280, 100) + F(160, 100)), fmt="4.40")
E("review", "items[2].widget.options[0].text", -(4 - 9))   # 6n - 5
E("review", "items[2].widget.options[1].text", 7 + 3 + 2)
E("review", "items[2].widget.options[1].text", 4 + 9)
E("review", "items[2].widget.options[2].text", 7 - 3 - 2)
lv.claim(gcd(18, 24) == 6, "review items[3] hcf(18, 24) = 6")
E("review", "items[3].widget.options[3].why", 6 * 24)
E("review", "items[4].widget.answer", 4 + 3 * 2 ** 2)
E("review", "items[4].widget.wrong[0].value", 4 + (3 * 2) ** 2)
E("review", "items[4].widget.wrong[1].value", (4 + 3) * 2 ** 2)
E("review", "items[6].widget.options[1].text", 3 - 2)            # 7n + 1
E("review", "items[6].widget.options[2].text", 6 + 10)
E("review", "items[6].widget.options[3].text", 7 - 4)
E("review", "items[7].widget.options[0].text", float(300 * F(45, 100)))
E("review", "items[8].widget.answer", float(90 / (F(450, 100) - F(225, 100))))
E("review", "items[8].widget.wrong[0].value", float(90 / F(450, 100)))
lv.claim(abs(90 / 6.75 - 13.33) < 0.01, "review items[8] added-cost 90 / 6.75 = 13.33")

# ---------- homework-1 ----------
E("homework", "items[0].explain.text", float(F(320, 100) * 100 + 5))
E("homework", "items[1].widget.answer", float(F(150, 100) + F(2, 100) * 1250))
E("homework", "items[1].widget.wrong[0].value", float(F(152, 100) * 1250))
E("homework", "items[1].widget.wrong[1].value", float(F(150, 100) + 2 * 1250))
E("homework", "items[1].widget.wrong[2].value", float(F(2, 100) * 1250))
h2 = lambda n: 3 * (2 * n - 1) - 2 * (n - 4)
lv.claim(all(h2(n) == 4 * n + 5 for n in range(-5, 6)), "homework items[2]: 4n + 5")
E("homework", "items[2].explain.text", h2(1))
lv.claim(all(6 * n - 3 - 2 * n - 8 == 4 * n - 11 for n in range(3)), "homework items[2] neg-neg gives 4n - 11")
lv.claim(all(6 * n - 3 + 2 * n + 8 == 8 * n + 5 for n in range(3)), "homework items[2] added gives 8n + 5")
# FINDING (misleading): "multiplied only the n by -2" gives 6n - 3 - 2n - 4 = 4n - 7, not the option's 4n + 1.
only_n = [6 * n - 3 - 2 * n - 4 for n in range(3)]
lv.stated("homework", "items[2].widget.options[2].why", "You multiplied only the $n$ by $-2$", only_n == [4 * n + 1 for n in range(3)])
E("homework", "items[4].explain.text", 7 + 8 + 9)
lv.claim(7 + 8 + 9 == 3 * 8, "homework items[4]: 24 = 3 x 8")
E("homework", "items[5].widget.answer", int(120 / F(4, 100)))
E("homework", "items[5].widget.wrong[0].value", 120 // 4)
E("homework", "items[5].widget.wrong[1].value", int(120 / F(4, 10)))
E("homework", "items[5].widget.wrong[2].value", float(120 * F(4, 100)))
E("homework", "items[5].explain.text", float(F(4, 100) * 1000))
E("homework", "items[6].widget.options[3].why", 27)
net = F(12, 100) - F(2, 100)
E("homework", "items[7].widget.answer", int(F(250, 100) / net))
E("homework", "items[7].widget.wrong[0].value", round(float(F(250, 100) / F(12, 100)), 2))
E("homework", "items[7].widget.wrong[1].value", round(float(F(250, 100) / F(14, 100)), 2))
E("homework", "items[7].widget.wrong[2].value", int(F(250, 100) / F(2, 100)))
lhs = lambda n: 3 * (n + 2)
rhs = lambda n: 3 * n + 2
for n in (0, 1, 10):
    E("homework", "items[8].model", lhs(n))
    E("homework", "items[8].model", rhs(n))
lv.claim(all(lhs(n) - rhs(n) == 4 for n in range(-10, 11)), "homework items[8]: the gap is 4 for every n")
E("homework", "items[8].model", 4000)

lv.check_wrongs()
lv.report()
