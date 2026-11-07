"""Second read of series level 3 (l9 to l13, review-3, homework-3): every graded key, every wrong[] value and the
numbers stated in prose, hints and feedback, each computed two ways (method 1: brute force, by building Pascal's
triangle by addition, expanding brackets with polynomial multiplication, or adding discounted payments one by one;
method 2: the closed forms n!/(k!(n-k)!), the general term, (1 + x)^n directly, C/r(1 - (1 + r)^-n)), checked
against the JSON with app/tools/numbers_lib.py. Claims that are not one number use lv.stated / lv.claim.
Checks that fail mark content that is wrong (see docs/reviews/review-series-1-3.md); they pass once it is fixed.
Run: python3 docs/reports/series-L3-numbers.py
"""
import math, os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("series", 3)
bad = []


def two(name, a, b, tol=1e-9):
    if abs(a - b) > tol * max(1, abs(a)):
        bad.append(f'{name}: {a} != {b}')
    return a


r2 = lambda x: round(x + 1e-12, 2)
C = math.comb


def pascal(n):                       # method 1: rows by addition
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


def polymul(p, q):                   # coefficient lists, index = power of x
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def ppow(p, n):
    out = [1]
    for _ in range(n):
        out = polymul(out, p)
    return out


def coef_paths(parts, n, want):      # brute force over all 2^n picks: parts = [(coef, power)], sum of matching products
    tot = 0
    for pick in itertools.product(parts, repeat=n):
        if sum(p for _, p in pick) == want:
            tot += math.prod(c for c, _ in pick)
    return tot


# ---------------- l9 ----------------
lv.claim(ppow([1, 1], 2) == [1, 2, 1] and ppow([1, 1], 3) == [1, 3, 3, 1], 'l9 s0, s1: (a + b)^2 and (a + b)^3')
lv.expect("l9", "screens[2].widget.answer", two('l9 s2', pascal(4)[2], C(4, 2)))
lv.expect("l9", "screens[2].widget.wrong[2].value", pascal(4)[1])
lv.claim(pascal(5) == [1, 5, 10, 10, 5, 1] and pascal(4)[1] + pascal(4)[2] == pascal(5)[2], 'l9 s3: 4 + 6 = 10, under the 6')
lv.expect("l9", "screens[4].widget.answer", two('l9 s4', pascal(6)[3], C(6, 3)))
lv.expect("l9", "screens[4].widget.wrong[1].value", pascal(5)[1] + pascal(5)[2])
lv.claim(pascal(7) == [1, 7, 21, 35, 35, 21, 7, 1], 'l9 s6: row 7')
lv.claim(len(pascal(7)) == 8, 'l9 s6: (a + b)^7 has 8 terms')
lv.claim(coef_paths([(1, 0), (1, 1)], 4, 2) == 6 and 2 ** 4 == 16, 'l9 s8: 6 of 16 paths end level')
lv.claim(all(sum(pascal(n)) == 2 ** n for n in range(12)), 'l9 summary: row n adds to 2^n')
lv.expect("l9", "quiz[0].widget.answer", two('l9 q0', pascal(7)[2], C(7, 2)))
lv.expect("l9", "quiz[0].widget.wrong[1].value", pascal(7)[3])
lv.expect("l9", "quiz[1].widget.options[2].text", two('l9 q1', sum(pascal(6)), 2 ** 6))
lv.expect("l9", "quiz[2].widget.options[0].text", two('l9 q2', C(5, 3), coef_paths([(1, 0), (1, 1)], 5, 3)))
lv.claim(pascal(9) == [1, 9, 36, 84, 126, 126, 84, 36, 9, 1], 'l9 q3: row 9')

# ---------------- l10 ----------------
lv.claim(coef_paths([(1, 0), (1, 1)], 3, 1) == 3, 'l10 s0: three paths pick one b')
off = [(i, j) for i in range(1, 5) for j in range(1, 5) if i != j]
lv.expect("l10", "screens[2].widget.answer", two('l10 s2', len(off) // 2, C(4, 2)))
lv.expect("l10", "screens[2].widget.wrong[0].value", len(off))
lv.expect("l10", "screens[3].prose", two('l10 s3a', len(list(itertools.permutations(range(5), 3))), 5 * 4 * 3))
lv.expect("l10", "screens[3].widget.answer", two('l10 s3', len(list(itertools.permutations([1, 2, 4]))), math.factorial(3)))
lv.expect("l10", "screens[4].widget.answer", two('l10 s4', len(list(itertools.combinations(range(5), 3))), C(5, 3)))
for i, v in enumerate([60, 60 // 3, 60 // 2, 5 * 3]):
    lv.expect("l10", f"screens[4].widget.wrong[{i}].value", v)
lv.expect("l10", "screens[5].explain.text", two('l10 s5', C(10, 8), C(10, 2)))
lv.expect("l10", "screens[6].widget.options[0].text", two('l10 s6', C(6, 2), 6 * 5 // 2))
lv.expect("l10", "screens[7].widget.lines[3].text", math.factorial(5))
p3 = C(5, 3) / 2 ** 5
lv.expect("l10", "screens[8].widget.answer", two('l10 s8', p3, sum(1 for s in itertools.product([0, 1], repeat=5) if sum(s) == 3) / 32))
lv.expect("l10", "screens[8].widget.wrong[3].value", 1 / 32)
lv.expect("l10", "quiz[0].widget.answer", two('l10 q0', C(7, 2), 7 * 6 // 2))
lv.expect("l10", "quiz[1].widget.options[3].text", math.factorial(6))
lv.expect("l10", "quiz[2].explain.text", two('l10 q2', C(12, 9), C(12, 3)))
lv.claim(math.factorial(12) // math.factorial(9) == 12 * 11 * 10, 'l10 q2: 12!/9! = 12 x 11 x 10')
lv.expect("l10", "quiz[3].widget.answer", two('l10 q3', C(4, 2) / 16, sum(1 for s in itertools.product([0, 1], repeat=4) if sum(s) == 2) / 16))

# ---------------- l11 ----------------
x2 = ppow([2, 1], 3)                      # (x + 2)^3, index = power of x
lv.claim(x2 == [8, 12, 6, 1], 'l11 s0, s1: (x + 2)^3 = x^3 + 6x^2 + 12x + 8')
lv.claim(ppow([3, 1], 3) == [27, 27, 9, 1], 'l11 s2: (x + 3)^3 = x^3 + 9x^2 + 27x + 27')
lv.expect("l11", "screens[3].widget.answer", two('l11 s3', ppow([1, 2], 4)[2], C(4, 2) * 2 ** 2))
for i, v in enumerate([C(4, 2) * 2, 4, C(4, 2) * 8, C(4, 2)]):
    lv.expect("l11", f"screens[3].widget.wrong[{i}].value", v)
lv.expect("l11", "screens[4].widget.answer", two('l11 s4', ppow([-3, 1], 4)[1], C(4, 3) * (-3) ** 3))
lv.claim(ppow([-3, 1], 4) == [81, -108, 54, -12, 1], 'l11 s4: x^4 - 12x^3 + 54x^2 - 108x + 81')
for i, v in enumerate([108, C(4, 3) * 9, -27, -36]):
    lv.expect("l11", f"screens[4].widget.wrong[{i}].value", v)
lv.expect("l11", "screens[5].widget.answer", two('l11 s5', coef_paths([(1, 1), (2, -1)], 4, 0), C(4, 2) * 2 ** 2))
lv.expect("l11", "screens[5].widget.wrong[3].value", C(4, 3) * 2 ** 3)   # k = 3 only; k = 1 gives 8
lv.stated("l11", "screens[5].feedback.byKey.wrong-k", "$k = 1$ or $k = 3$", C(4, 1) * 2 == C(4, 3) * 2 ** 3)
lv.expect("l11", "screens[5].feedback.byKey.wrong-k", C(4, 3) * 2 ** 3)          # k = 3 gives 32 x^-2 (finding 19)
lv.claim(all((k == 2) == (4 - 2 * k == 0) for k in range(5)) and C(4, 3) * 2 ** 3 == 32 and 4 - 2 * 3 == -2, 'l11 s5: the power of x is 4 - 2k, zero only at k = 2; k = 3 leaves x^-2')
lv.expect("l11", "screens[5].feedback.byKey.wrong-k", next(k for k in range(5) if 4 - 2 * k == 0))   # the powers cancel only at k = 2
lv.claim((1 + 2) ** 3 == 27 and 1 + 8 == 9 and 6 + 12 == 18, 'l11 s6: 27 against 9, gap 18')
# "never just a^n + b^n once n >= 2 and both parts are non-zero": a = 1, b = -1, n = 3 gives 0 = 0
lv.stated("l11", "screens[6].explain.text", "is never just", (1 + -1) ** 3 != 1 ** 3 + (-1) ** 3)
lv.claim(all(C(n, k) > 0 for n in range(2, 12) for k in range(1, n)) and (1 + -1) ** 3 == 1 ** 3 + (-1) ** 3,
         'l11 s6: mixed terms always appear in the expansion once n >= 2 (every C(n, k) > 0), though their values can cancel (a = 1, b = -1, n = 3)')
lv.claim('always has mixed terms once' in lv.text("l11", "screens[6].explain.text") and 'never just' not in lv.text("l11", "screens[6].explain.text"), 'l11 s6: the reworded claim is about terms, not values')
lv.expect("l11", "screens[7].explain.text", C(7, 3))
bal = 1000 * 1.04 ** 3
lv.expect("l11", "screens[9].widget.answer", two('l11 s9', round(bal - 1000 - 120, 3), round(1000 * (3 * 0.04 ** 2 + 0.04 ** 3), 3)))
lv.expect("l11", "screens[9].widget.wrong[0].value", round(bal - 1000, 3))
lv.expect("l11", "screens[9].widget.wrong[2].value", round(1000 * (0.04 ** 2 + 0.04 ** 3), 3))
lv.expect("l11", "screens[9].widget.wrong[3].value", round(bal, 3))
lv.expect("l11", "quiz[0].widget.answer", two('l11 q0', ppow([2, 1], 5)[3], C(5, 2) * 4))
lv.claim(ppow([1, -1], 4) == [1, -4, 6, -4, 1], 'l11 q1: (1 - x)^4')
lv.expect("l11", "quiz[2].widget.answer", two('l11 q2', coef_paths([(2, 1), (1, -1)], 6, 0), C(6, 3) * 8))
lv.expect("l11", "quiz[3].widget.answer", two('l11 q3', ppow([3, 1], 5)[2], C(5, 2) * 27))
lv.expect("l11", "quiz[3].widget.wrong[0].value", C(5, 2) * 9)

# ---------------- l12 ----------------
lv.expect("l12", "screens[0].explain.text", round(1.01 ** 5, 5))
gap = lambda x: (1 + x) ** 5 - (1 + 5 * x)
lv.expect("l12", "screens[1].hints[1].text", round(gap(0.3), 4))
lv.expect("l12", "screens[1].hints[1].text", round(gap(0.01), 4), fmt='{:.4f}')
lv.claim(abs(round(gap(-0.3), 2) - 0.67) < 1e-9 and abs(round(gap(0.3), 2) - 1.21) < 1e-9, 'l12 s1: gaps 1.21 and 0.67 at the ends')
lv.expect("l12", "screens[2].widget.answer", two('l12 s2', 1 + 4 * (-0.02), 1 - 0.08))
lv.expect("l12", "screens[2].explain.text", round(0.98 ** 4, 5))
lv.claim(abs(0.98 ** 4 - 0.92) <= 0.0025, 'l12 s2: the exact 0.9224 lies inside the tolerance')
lv.expect("l12", "screens[3].widget.answer", two('l12 s3', 1 + 10 * 0.02 + C(10, 2) * 0.02 ** 2, sum(C(10, k) * 0.02 ** k for k in range(3))))
lv.expect("l12", "screens[3].explain.text", round(1.02 ** 10, 5))
lv.claim(abs(1.02 ** 10 - 1.218) <= 0.0011, 'l12 s3: the exact value lies inside the tolerance')
for i, v in enumerate([1.2, 1 + 0.2 + 90 * 0.0004, 1 + 0.2 + 100 * 0.0004]):
    lv.expect("l12", f"screens[3].widget.wrong[{i}].value", round(v, 6))
lv.claim(1 + 10 + 45 == 56 and 2 ** 10 == 1024 and 56 + 120 == 176, 'l12 s4: 56 against 1024; one more term gives 176')
lv.expect("l12", "screens[5].explain.text", two('l12 s5', round(1.01 ** 100, 4), round(sum(C(100, k) * 0.01 ** k for k in range(101)), 4)))
lv.expect("l12", "screens[5].hints[2].text", C(100, 2) * 0.0001)
lv.expect("l12", "screens[6].explain.text", round(1.02 ** 5 - 1.10, 4))
lv.expect("l12", "screens[6].explain.text", round(1.01 ** 5 - 1.05, 4))
lv.claim(ppow([1, -2], 5)[:3] == [1, -10, 40], 'l12 s7: (1 - 2x)^5 = 1 - 10x + 40x^2 + ...')
lv.expect("l12", "screens[7].explain.text", round(0.98 ** 5, 5))
lv.expect("l12", "screens[8].widget.answer", two('l12 s8', 10000 * C(5, 2) * 0.04 ** 2, 10000 * 10 * 0.0016))
exact8 = 10000 * (1.04 ** 5 - 1.2)
lv.expect("l12", "screens[8].feedback.correct", r2(exact8))
lv.expect("l12", "screens[8].explain.text", 10000 * C(5, 2) * 0.04 ** 2)
lv.expect("l12", "screens[8].explain.text", r2(exact8))
lv.claim(r2(exact8) == 166.53 and 10000 * C(5, 2) * 0.04 ** 2 == 160 and 0 < exact8 - 160 < 10, 'l12 s8: the gap 166.53 is a little more than the x^2 term, 160 (finding 20)')
lv.claim(abs(exact8 - 160) <= 7, 'l12 s8: the exact gap lies inside the tolerance')
for i, v in enumerate([16, 400, 320, r2(exact8 + 2000)]):
    lv.expect("l12", f"screens[8].widget.wrong[{i}].value", v)
lv.expect("l12", "quiz[0].widget.answer", 50 * (1 + 10 * 0.002))
lv.expect("l12", "quiz[0].explain.text", r2(50 * 1.002 ** 10))
lv.expect("l12", "quiz[1].widget.options[0].text", 1 - 6 * 0.03)
lv.expect("l12", "quiz[1].explain.text", round(0.97 ** 6, 4), fmt='{:.4f}')
lv.expect("l12", "quiz[1].explain.text", C(6, 2) * 0.03 ** 2)
err = lambda x: (1 + x) ** 3 - (1 + 3 * x)
lv.expect("l12", "quiz[2].explain.text", two('l12 q2', round(err(0.9), 3), 3 * 0.81 + 0.729))
lv.expect("l12", "quiz[2].explain.text", round(err(0.1), 3))
lv.expect("l12", "quiz[3].widget.answer", two('l12 q3', round(1 + 0.24 + C(8, 2) * 0.0009, 4), round(sum(C(8, k) * 0.03 ** k for k in range(3)), 4)))
lv.expect("l12", "quiz[3].explain.text", round(1.03 ** 8, 5))
lv.expect("l12", "quiz[3].widget.wrong[1].value", round(1 + 0.24 + 56 * 0.0009, 4))

# ---------------- l13 ----------------
pv = lambda c, r, n: sum(c / (1 + r) ** k for k in range(1, n + 1))
ann = lambda c, r, n: c / r * (1 - (1 + r) ** -n)
lv.expect("l13", "screens[0].widget.answer", round(100 / 1.05, 3))
lv.expect("l13", "screens[0].feedback.byKey.minus", 95 * 1.05)
lv.expect("l13", "screens[1].hints[1].text", r2(100 / 1.2))
lv.expect("l13", "screens[1].hints[1].text", r2(100 / 1.2 ** 5))
lv.expect("l13", "screens[3].widget.answer", two('l13 s3', round(pv(100, 0.05, 5), 3), round(ann(100, 0.05, 5), 3)))
lv.expect("l13", "screens[3].widget.wrong[1].value", r2(500 / 1.05))
lv.expect("l13", "screens[3].widget.wrong[2].value", r2(500 / 1.05 ** 5))
lv.expect("l13", "screens[3].explain.text", r2(500 - ann(100, 0.05, 5)))
lv.expect("l13", "screens[4].widget.options[1].text", two('l13 s4', r2(pv(100, 0.05, 10)), r2(ann(100, 0.05, 10))))
lv.expect("l13", "screens[4].widget.options[0].text", 2 * r2(ann(100, 0.05, 5)))
lv.expect("l13", "screens[4].widget.options[3].text", r2(1000 / 1.05 ** 10))
lv.claim(abs(ann(100, 0.05, 5) * (1 + 1.05 ** -5) - ann(100, 0.05, 10)) < 1e-9, 'l13 s4: payments 6 to 10 are the first five times 1.05^-5')
lv.expect("l13", "screens[5].widget.answer", two('l13 s5', 100 / 0.05, pv(100, 0.05, 3000)))
due = 100 + ann(100, 0.05, 4)
lv.expect("l13", "screens[6].widget.options[1].text", two('l13 s6', r2(due), r2(1.05 * ann(100, 0.05, 5))))
lv.expect("l13", "screens[6].explain.text", r2(ann(100, 0.05, 4)))
bond = ann(5, 0.04, 3) + 100 / 1.04 ** 3
lv.expect("l13", "screens[8].widget.answer", two('l13 s8', round(bond, 3), round(5 / 1.04 + 5 / 1.04 ** 2 + 105 / 1.04 ** 3, 3)))
lv.expect("l13", "screens[8].widget.wrong[1].value", r2(ann(5, 0.04, 3)))
lv.expect("l13", "screens[8].widget.wrong[2].value", r2(100 / 1.04 ** 3))
lv.expect("l13", "screens[8].widget.wrong[3].value", r2(115 / 1.04 ** 3))
lv.expect("l13", "quiz[0].widget.answer", round(200 / 1.04 ** 2, 3))
lv.expect("l13", "quiz[0].widget.wrong[1].value", r2(200 / 1.04))
lv.expect("l13", "quiz[0].widget.wrong[2].value", r2(200 * 1.04 ** 2))
lv.expect("l13", "quiz[1].widget.answer", two('l13 q1', 50 / 0.025, pv(50, 0.025, 6000)))
lv.expect("l13", "quiz[2].widget.answer", two('l13 q2', round(pv(250, 0.03, 4), 3), round(ann(250, 0.03, 4), 3)))
lv.expect("l13", "quiz[2].widget.wrong[1].value", r2(1000 / 1.03))
lv.expect("l13", "quiz[2].widget.wrong[2].value", r2(1000 / 1.03 ** 4))
lv.expect("l13", "quiz[3].widget.options[0].text", two('l13 q3', r2(ann(100, 0.06, 5)), r2(pv(100, 0.06, 5))))
lv.expect("l13", "quiz[3].widget.options[3].text", r2(500 / 1.06 ** 5))

# ---------------- review-3 ----------------
lv.expect("review", "items[0].widget.answer", two('r3 i0', pascal(8)[3], C(8, 3)))
# review-3 items[1] reworded (finding 34): 4 of 9 shares, 126 baskets (two ways), 3024 ordered picks, 24 orders
lv.expect("review", "items[1].widget.answer", two('r3 i1', len(list(itertools.combinations(range(9), 4))), C(9, 4)))
lv.claim(C(9, 4) == 126 == pascal(9)[4] == 3024 // 24 == len(list(itertools.permutations(range(9), 4))) // math.factorial(4), 'review-3 i1: 126 baskets, the fifth number of row 9, 3024 / 24')
lv.expect("review", "items[1].widget.wrong[0].value", len(list(itertools.permutations(range(9), 4))))
lv.expect("review", "items[1].widget.wrong[1].value", 9 * 4)
lv.expect("review", "items[1].widget.wrong[2].value", 9 ** 4)
lv.expect("review", "items[1].feedback.byKey.ordered", math.factorial(4))
lv.expect("review", "items[1].explain.text", len(list(itertools.permutations(range(9), 4))))
lv.expect("review", "items[1].explain.text", math.factorial(4))
lv.expect("review", "items[1].explain.text", C(9, 4))
lv.claim('336' not in lv.text("review", "items[1]") and 'teams' not in lv.text("review", "items[1]"), 'review-3 i1: no longer the counting lesson\'s 8 traders and 336 picks')
lv.expect("review", "items[2].widget.options[0].text", two('r3 i2', ppow([-2, 3], 4)[2], C(4, 2) * 9 * 4))
lv.expect("review", "items[3].widget.answer", round(1 + 25 * 0.004 + C(25, 2) * 0.004 ** 2, 6))
lv.expect("review", "items[3].explain.text", round(1.004 ** 25, 5))
lv.expect("review", "items[4].widget.answer", two('r3 i4', r2(pv(1200, 0.03, 20)), r2(ann(1200, 0.03, 20))))
lv.expect("review", "items[4].widget.wrong[2].value", r2(24000 / 1.03 ** 20))
lv.expect("review", "items[5].widget.answer", two('r3 i5', C(6, 3) / 64, sum(1 for s in itertools.product([0, 1], repeat=6) if sum(s) == 3) / 64))
lv.expect("review", "items[7].widget.options[1].why", r2(1.01 ** 200))
lv.expect("review", "items[7].widget.options[3].why", round(0.9 ** 30, 3))
lv.claim(abs((1.5 ** 2 - 2) / 1.5 ** 2 - 0.11) < 0.005, 'review-3 i7: 2 misses 2.25 by 11%')
lv.claim(abs(1.001 ** 50 - 1.05) < 0.0013, 'review-3 i7: within 0.0013 of 1.0512')
lv.expect("review", "items[8].widget.answer", two('r3 i8', 100 / 0.04 - 100 / 0.05, pv(100, 0.04, 6000) - pv(100, 0.05, 6000), tol=1e-6))
# wrong[1] "pct" says "You divided by 4 and by 5": 100/4 - 100/5 = 5, not 25
lv.expect("review", "items[8].widget.wrong[1].value", 100 / 4 - 100 / 5)
lv.expect("review", "items[8].feedback.byKey.pct", 100 / 4 - 100 / 5)
lv.expect("review", "items[8].explain.text", 100 / 0.05)
lv.expect("review", "items[8].explain.text", 100 / 0.04)
lv.expect("review", "items[8].explain.text", 100 / 0.04 - 100 / 0.05)             # the answer, 500.00 (finding 6)
lv.claim(abs((100 / 0.04 - 100 / 0.05) / (100 / 0.05) - 0.25) < 1e-12, 'review-3 i8: the rise is 25% of 2,000')

# ---------------- homework-3 ----------------
lv.claim(ppow([-1, 2], 4) == [1, -8, 24, -32, 16], 'homework-3 i0: (2x - 1)^4')
lv.expect("homework", "items[1].widget.answer", two('h3 i1', ppow([1, 2], 8)[5], C(8, 5) * 32))
lv.expect("homework", "items[2].widget.answer", two('h3 i2', coef_paths([(1, 2), (-2, -1)], 6, 0), C(6, 4) * 16))
lv.expect("homework", "items[2].widget.wrong[2].value", C(6, 3) * (-2) ** 3)
lv.expect("homework", "items[3].prose", 0.6)
lv.claim(abs(0.6 * 0.6 * 0.4 - 0.144) < 1e-12 and abs(sum(0.6 ** sum(s) * 0.4 ** (3 - sum(s)) for s in itertools.product([0, 1], repeat=3) if s == (1, 1, 0)) - 0.144) < 1e-12, 'homework-3 i3: win, win, loss has chance 0.144 (the rule the item now states)')
lv.expect("homework", "items[3].widget.answer", two('h3 i3', round(C(5, 3) * 0.6 ** 3 * 0.4 ** 2, 6), round(sum(0.6 ** sum(s) * 0.4 ** (5 - sum(s)) for s in itertools.product([0, 1], repeat=5) if sum(s) == 3), 6)))
lv.expect("homework", "items[4].widget.answer", round(80 * (1 + 0.021 + C(21, 2) * 1e-6), 6))
lv.claim(r2(80 * 1.001 ** 21) == 81.70, 'homework-3 i4: the exact price is £81.70 to the penny')
lv.expect("homework", "items[5].widget.answer", two('h3 i5', sum(ppow([-1, 3], 5)), (3 - 1) ** 5))
lv.expect("homework", "items[5].widget.wrong[1].value", 4 ** 5)
lv.expect("homework", "items[7].widget.answer", two('h3 i7', r2(10000 * 0.06 / (1 - 1.06 ** -5)), r2(10000 / sum(1.06 ** -k for k in range(1, 6)))))
lv.expect("homework", "items[7].explain.text", r2(5 * r2(10000 * 0.06 / (1 - 1.06 ** -5))))
terms = [C(10, k) * 0.5 ** k for k in range(11)]
lv.expect("homework", "items[8].widget.answer", two('h3 i8', max(terms), C(10, 3) / 8))
for i, v in enumerate([terms[5], terms[2], terms[4], C(10, 5)]):
    lv.expect("homework", f"items[8].widget.wrong[{i}].value", v)
lv.expect("homework", "items[9].model", r2(5000 * 1.03 ** 10))
lv.expect("homework", "items[9].model", r2(5000 * 1.03 ** 10 - 6500))
lv.expect("homework", "items[9].model", r2(C(10, 3) * 0.03 ** 3 * 5000))
lv.expect("homework", "items[9].model", r2(C(40, 3) * 0.03 ** 3 * 5000))
lv.expect("homework", "items[9].prompt", r2(5000 * 1.03 ** 40 - 11000))
lv.expect("homework", "items[9].model", r2(5000 * 1.03 ** 40 - 11000 - 3510))

lv.claim(not bad, 'every number agrees by both methods', '; '.join(bad))
lv.check_wrongs()
lv.report()
