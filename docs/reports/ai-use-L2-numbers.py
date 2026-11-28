"""Recompute every number stated in ai-use level 2 (l5 to l8, review-2, homework-2, problems-2), each two ways,
and check it appears in the JSON where it is stated (app/tools/numbers_lib.py).
Method A is floating point (repeated multiplication, percentages as decimals); method B is exact fractions
(Fraction powers, percentages built from 10%, 5%, 2% and 1% parts). The l6 code widget is also run in CPython:
its solution must pass every hidden test and its starter must fail at least one.
Run from the repository root: python3 docs/reports/ai-use-L2-numbers.py   (exits 0 when every check passes)
"""
import json, math, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level('ai-use', 2)


def comp_a(p, r, n):
    b = p
    for _ in range(n):
        b *= (1 + r)
    return b


def comp_b(p, r, n):
    return F(p) * (1 + F(r).limit_denominator(10 ** 6)) ** n


def money(x):
    return float(round(F(x) * 100)) / 100 if isinstance(x, F) else round(x + 1e-9, 2)


def two(label, a, b, places=2):
    ok = abs(float(a) - float(b)) < 10 ** -(places + 3)
    lv.claim(ok, f'{label}: float {float(a):.6f} = exact {float(b):.6f}')
    return round(float(b), places)


def pct(p, amount, parts):
    """p% of amount, directly and as a sum of the given percentage parts."""
    direct = F(p, 100) * amount
    built = sum(F(q, 100) * amount for q in parts)
    lv.claim(direct == built and sum(parts) == p, f'{p}% of {amount} = {float(direct)} directly and by {parts}')
    return float(direct)


# ---------------- l6 ----------------
c = two('l6 £2,400 at 3% for 5 years', comp_a(2400, 0.03, 5), comp_b(2400, '0.03', 5))
lv.claim(c == 2782.26, 'compound = 2782.26')
simple = 2400 * (1 + 5 * F(3, 100))
lv.claim(simple == 2760 and F(3, 100) * 2400 == 72, 'simple interest 2760, £72 a year')
lv.claim(2400 * F(116, 100) == 2784 and 2760 < c < 2784, 'estimate band 2760 to 2784 (15% to 16%) holds the exact figure')
for path in ('screens[1].widget.options[1].why', 'screens[2].widget.answer', 'screens[2].feedback.correct', 'screens[2].explain.text'):
    lv.expect('l6', path, c)
lv.expect('l6', 'screens[1].explain.text', 72)
lv.expect('l6', 'screens[2].widget.wrong[0].value', 2760)
lv.expect('l6', 'screens[2].widget.wrong[1].value', two('l6 four years', comp_a(2400, 0.03, 4), comp_b(2400, '0.03', 4)))
lv.expect('l6', 'screens[2].widget.wrong[2].value', round(c - 2400, 2))
lv.expect('l6', 'screens[2].hints[1].text', round(1.03 ** 5, 6))
lv.claim(round(float(F(103, 100) ** 5), 6) == 1.159274, '1.03^5 = 1.159274 to 6 places')
lv.expect('l6', 'screens[2].feedback.correct', round(c - 2760, 2))
lv.expect('l6', 'summary.formula.note', c)
# 17% of £4,850
v = pct(17, 4850, [10, 5, 2])
lv.claim(v == 824.5 and F(10, 100) * 4850 == 485 and F(5, 100) * 4850 == F(48500, 200) and F(2, 100) * 4850 == 97, '17% = 485 + 242.50 + 97 = 824.50')
lv.expect('l6', 'screens[3].widget.answer', v)
lv.expect('l6', 'screens[3].widget.wrong[0].value', 971.5)
lv.claim(abs(971.5 / 4850 - 0.2) < 0.001 and pct(20, 4850, [10, 10]) == 970, 'the chatbot\'s 971.50 is about 20%; 20% is 970')
lv.expect('l6', 'screens[3].widget.wrong[1].value', 970)
lv.expect('l6', 'screens[3].widget.wrong[2].value', v / 10)
lv.expect('l6', 'screens[3].widget.wrong[3].value', pct(15, 4850, [10, 5]))
# fall from 80 to 60
lv.claim(F(20, 80) == F(1, 4) and abs(20 / 80 - 0.25) < 1e-12, 'fall 80 to 60 is 25%')
lv.expect('l6', 'screens[4].widget.answer', 0.25)
lv.expect('l6', 'screens[4].widget.wrong[0].value', round(20 / 60, 4))
lv.expect('l6', 'screens[4].widget.wrong[1].value', 0.2)
# five monthly costs
costs = {'April': 1240, 'May': 985, 'June': 1415, 'July': 760, 'August': 1130}
tot = sum(costs.values()); tot_b = 0
for k in costs:
    tot_b += costs[k]
lv.claim(tot == tot_b == 5530, 'costs total 5530')
lv.claim(tot - costs['July'] == 4770, 'dropping July gives 4770')
for k, path in (('April', 'r0'), ('May', 'r1'), ('June', 'r2'), ('August', 'r4')):
    lv.expect('l6', f'screens[5].feedback.byKey.{path}', tot - costs[k])
lv.expect('l6', 'screens[5].feedback.correct', tot)
# 15% of 2,400 confirmed
lv.claim(pct(15, 2400, [10, 5]) == 360, '15% of 2400 = 240 + 120 = 360')
lv.expect('l6', 'screens[7].canvas.params.rows[2][1]', 360)
# code widget: run solution and starter
w = lv.files['l6-checking-the-sums']['screens'][8]['widget']
def run(src, tests):
    ns = {}
    exec(src, ns)
    res = []
    for t in tests:
        try:
            got = eval(t['call'], ns)
            res.append(got is not None and math.isclose(got, float(eval(t['expect'])), rel_tol=1e-9))
        except Exception:
            res.append(False)
    return res
lv.claim(all(run(w['solution'], w['tests'])), 'l6 code: solution passes every hidden test')
lv.claim(not all(run(w['starter'], w['tests'])), 'l6 code: starter fails')
exp_b = [money(comp_b(2400, '0.03', 5)), money(comp_b(1000, '0.05', 2)), money(comp_b(500, '0.1', 3)), 4850.0, 100.0]
lv.claim([float(t['expect']) for t in w['tests']] == exp_b, f'l6 code expects recomputed exactly: {exp_b}')
# transfer: 40 to 50
lv.claim(F(10, 40) == F(1, 4) and F(10, 50) == F(1, 5) and F(50, 40) == F(5, 4), 'growth 40 to 50: 25% (wrong base 20%, ratio 1.25)')
lv.expect('l6', 'screens[10].widget.answer', 0.25)
lv.expect('l6', 'screens[10].widget.wrong[0].value', 0.2)
lv.expect('l6', 'screens[10].widget.wrong[1].value', 1.25)
# quiz
lv.claim(pct(4, 6200, [1, 1, 1, 1]) == 248 and 248 * 10 == 2480, 'quiz: 4% of 6200 = 248; 2480 is ten times')
lv.expect('l6', 'quiz[0].explain.text', 248)
q = two('quiz £1,000 at 10% for 2 years', comp_a(1000, 0.1, 2), comp_b(1000, '0.1', 2))
lv.expect('l6', 'quiz[2].widget.answer', q); lv.expect('l6', 'quiz[2].widget.wrong[0].value', 1200); lv.expect('l6', 'quiz[2].widget.wrong[1].value', round(q - 1000, 2))
lv.claim(F(100, 500) == F(1, 5), 'quiz: 500 to 400 is 20%')
lv.expect('l6', 'quiz[3].widget.answer', 0.2); lv.expect('l6', 'quiz[3].widget.wrong[0].value', 0.25)

# ---------------- l8 ----------------
lv.claim(50 * F(120, 100) == 60 and 60 * F(80, 100) == 48 and F(20, 100) * 60 == 12, 'share: 50 to 60 to 48 (20% of 60 is 12)')
lv.expect('l8', 'screens[0].canvas.right.params.lines[4]', 48)
coat = 80 * F(75, 100) * F(125, 100)
lv.claim(coat == 75 and F(25, 100) * 60 == 15 and 60 + F(25, 100) * 80 == 80, 'coat: right path 75, wrong step gives 80')
lv.expect('l8', 'screens[1].feedback.correct', 75); lv.expect('l8', 'screens[1].feedback.correct', 15)
m = two('l8 1% a month for 12 months', comp_a(1, 0.01, 12) - 1, comp_b(1, '0.01', 12) - 1, 4)
lv.claim(m == 0.1268, '1.01^12 - 1 = 0.1268 (12.68%)')
lv.expect('l8', 'screens[2].widget.answer', m); lv.expect('l8', 'screens[2].widget.wrong[0].value', 0.12)
lv.expect('l8', 'screens[2].widget.wrong[1].value', round(1 + m, 4))
lv.expect('l8', 'screens[6].prose', '12.68')
f5 = two('l8 0.5% a month for 12 months', comp_a(1, 0.005, 12) - 1, comp_b(1, '0.005', 12) - 1, 4)
lv.claim(f5 == 0.0617, '1.005^12 - 1 = 0.0617 (6.17%)')
lv.expect('l8', 'screens[7].widget.answer', f5); lv.expect('l8', 'screens[7].widget.wrong[0].value', 0.06)
lv.expect('l8', 'screens[7].widget.wrong[1].value', round(1 + f5, 4))
lv.claim(200 * F(110, 100) * F(90, 100) == 198, 'quiz: 200 up 10% then down 10% = 198')
lv.expect('l8', 'quiz[2].widget.answer', 198); lv.expect('l8', 'quiz[2].widget.wrong[1].value', 2)

# ---------------- review-2 ----------------
lv.claim(pct(6, 3500, [1] * 6) == 210, 'r4: 6% of 3500 = 210')
lv.expect('review', 'items[3].explain.text', 210)
lv.claim(pct(12, 2350, [10, 2]) == 282 and pct(13, 2350, [10, 2, 1]) == 305.5, 'r5: 12% of 2350 = 282; the chatbot\'s 305.50 is 13%')
lv.expect('review', 'items[4].widget.answer', 282); lv.expect('review', 'items[4].widget.wrong[0].value', 305.5)
lv.expect('review', 'items[4].widget.wrong[1].value', 235); lv.expect('review', 'items[4].widget.wrong[2].value', 28.2)
r6 = two('r6 £5,000 at 4% for 3 years', comp_a(5000, 0.04, 3), comp_b(5000, '0.04', 3))
lv.expect('review', 'items[5].widget.answer', r6); lv.expect('review', 'items[5].widget.wrong[0].value', 5600)
lv.expect('review', 'items[5].widget.wrong[1].value', two('r6 two years', comp_a(5000, 0.04, 2), comp_b(5000, '0.04', 2)))
sal = 1200 * F(105, 100) ** 2
lv.claim(sal == 1323 and F(5, 100) * 1260 == 63, 'r9: 1200 to 1260 to 1323 (5% of 1260 is 63)')
lv.expect('review', 'items[8].feedback.correct', 1323)

# ---------------- homework-2 ----------------
h1 = two('h1 £3,000 at 5% for 4 years', comp_a(3000, 0.05, 4), comp_b(3000, '0.05', 4))
lv.claim(h1 == 3646.52, 'h1 3646.52')
lv.expect('homework', 'items[0].parts[1].widget.answer', h1); lv.expect('homework', 'items[0].parts[1].widget.wrong[0].value', 3600)
h1b = comp_b(3000, '0.05', 3)
lv.claim(h1b == F(694575, 200), 'h1 three years = 3472.875 exactly (a tie; the slip band of 0.01 takes 3472.87 and 3472.88)')
lv.expect('homework', 'items[0].parts[1].widget.wrong[1].value', 3472.88)
lv.claim(pct(15, 3000, [10, 5]) == 450 and pct(18, 3000, [10, 5, 2, 1]) == 540, 'h1: 15% of 3000 = 450; 540 is 18%')
lv.expect('homework', 'items[0].parts[2].widget.answer', 450); lv.expect('homework', 'items[0].parts[2].widget.wrong[0].value', 540)
lv.expect('homework', 'items[0].parts[2].widget.wrong[1].value', 300)
car_a = 12000 * 0.85 * 0.85; car_b = 12000 * F(85, 100) ** 2
lv.claim(abs(car_a - 8670) < 1e-6 and car_b == 8670 and 12000 * (1 - 2 * F(15, 100)) == 8400, 'h4 car 8670, slip 8400')
lv.expect('homework', 'items[3].widget.answer', 8670); lv.expect('homework', 'items[3].widget.wrong[1].value', 10200)
lv.expect('homework', 'items[3].widget.wrong[2].value', 12000 - 8670)
lv.expect('homework', 'items[3].explain.text', 1530)
lv.claim(F(16, 64) == F(1, 4) and F(16, 80) == F(1, 5), 'h6: 64 to 80 is 25%; wrong base 20%')
lv.expect('homework', 'items[5].widget.answer', 0.25); lv.expect('homework', 'items[5].widget.wrong[0].value', 0.2)
h7 = two('h7 2% a month for 12 months', comp_a(1, 0.02, 12) - 1, comp_b(1, '0.02', 12) - 1, 4)
lv.claim(h7 == 0.2682, '1.02^12 - 1 = 0.2682')
lv.expect('homework', 'items[6].widget.answer', h7); lv.expect('homework', 'items[6].widget.wrong[1].value', round(1 + h7, 4))

# ---------------- problems-2 ----------------
p1 = two('p1 £8,000 at 6% for 4 years', comp_a(8000, 0.06, 4), comp_b(8000, '0.06', 4))
lv.claim(p1 == 10099.82 and 8000 * (1 + 4 * F(6, 100)) == 9920, 'p1 10099.82; simple 9920')
lv.expect('problems', 'items[0].parts[1].widget.answer', p1)
lv.expect('problems', 'items[0].parts[1].widget.wrong[1].value', two('p1 three years', comp_a(8000, 0.06, 3), comp_b(8000, '0.06', 3)))
lv.expect('problems', 'items[0].parts[2].widget.answer', round(p1 - 9920, 2))
lv.expect('problems', 'items[0].parts[2].widget.wrong[0].value', round(p1 - 8000, 2))
lv.claim(pct(10, 6400, [10]) == 640 and pct(13, 6400, [10, 1, 1, 1]) == 832 and pct(18, 6400, [10, 5, 2, 1]) == 1152, 'p2: 640, 832; the chatbot\'s 1152 is 18%')
lv.expect('problems', 'items[1].parts[0].widget.answer', 640); lv.expect('problems', 'items[1].parts[0].widget.wrong[0].value', 64)
lv.expect('problems', 'items[1].parts[1].widget.answer', 832)
lv.expect('problems', 'items[1].parts[1].widget.wrong[1].value', 640 + float(F(3, 100) * 640))
lv.expect('problems', 'items[1].parts[2].widget.answer', 1152 - 832)
lv.expect('problems', 'items[1].parts[3].widget.answer', 0.18); lv.expect('problems', 'items[1].parts[3].widget.wrong[0].value', float(F(320, 6400)))
p3 = two('p3 1.5% a month for 12 months', comp_a(1, 0.015, 12) - 1, comp_b(1, '0.015', 12) - 1, 4)
lv.claim(p3 == 0.1956, '1.015^12 - 1 = 0.1956')
lv.expect('problems', 'items[2].parts[1].widget.answer', p3)
cost = two('p3 cost on £2,000', 2000 * (comp_a(1, 0.015, 12) - 1), 2000 * (comp_b(1, '0.015', 12) - 1))
lv.claim(cost == 391.24 and round(2000 * 0.1956, 2) == 391.2, 'p3 cost 391.24 (391.20 from the rounded rate)')
lv.expect('problems', 'items[2].parts[2].widget.answer', cost)
lv.expect('problems', 'items[2].parts[2].widget.wrong[1].value', round(2000 + cost, 2))
lv.expect('problems', 'items[2].parts[2].explain.text', 391.20)
lv.claim(F(12 * 15, 1000) * 2000 == 360, 'p3 the chatbot\'s 18% of 2000 = 360')
lv.expect('problems', 'items[2].parts[3].widget.answer', round(cost - 360, 2))

lv.check_wrongs()
lv.report()
