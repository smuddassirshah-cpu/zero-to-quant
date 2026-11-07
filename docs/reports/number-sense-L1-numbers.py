"""Second-read number checks for number-sense level 1 (l1 to l5, review-1, homework-1).

Every graded key and wrong[] value is recomputed here from the setup, with Fraction for exact values,
then rounded to the precision the content stores. Two checks fail on the current content because the
content is wrong (review-number-sense-1-3.md findings 1 and 9): they pass once the fix rewords the text.
"""
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('number-sense', 1)


def doc(f):
    return lv._file(f)[1]


def r(x, d):
    return round(float(x), d)


def num(f, base, ans, *wrongs):
    """Numeric widget: the key, then each wrong[] value in file order."""
    lv.expect(f, base + '.answer', ans)
    for i, v in enumerate(wrongs):
        lv.expect(f, f'{base}.wrong[{i}].value', v)


def inside(f, base, i, value):
    """A drag-point wrong region holds the value its slip produces."""
    node = doc(f)
    for part in base.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.isdigit() else node[part]
    xs = node['wrong'][i]['region']['x']
    lv.claim(xs[0] <= float(value) <= xs[1], f'{f} {base}.wrong[{i}] region {xs} holds {float(value):.4f}')


# ---------- l1 ----------
lv.expect('l1', 'screens[1].hints[2].text', 3 * 8 // 4)                    # 3 pieces of A = 6 of B
num('l1', 'screens[3].widget', r(F(2, 5), 4), r(F(2, 3), 4), r(F(3, 5), 4), r(F(5, 2), 4))
lv.expect('l1', 'screens[4].widget.points[0].target', 0.4)
inside('l1', 'screens[4].widget', 0, F(1, 5))                               # counted the mark at 0
inside('l1', 'screens[4].widget', 1, 1 - F(2, 5))                           # counted back from 1
lv.expect('l1', 'screens[5].widget.points[0].target', 0.75)
inside('l1', 'screens[5].widget', 0, F(3, 8))
inside('l1', 'screens[5].widget', 1, F(4, 8))
lv.expect('l1', 'screens[5].hints[2].text', 6)                              # 3/4 = 6/8
lv.expect('l1', 'screens[6].widget.points[0].target', 1.25)
inside('l1', 'screens[6].widget', 0, 1)
inside('l1', 'screens[6].widget', 1, F(1, 4))
lv.claim(F(2, 2 + 1 + 1) == F(1, 2), 'l1 trap: colSizes [2,1,1], shaded piece is 1/2')
lv.expect('l1', 'screens[7].widget.options[1].text', 0.5)
lv.expect('l1', 'screens[8].explain.text', 10 - 7)
num('l1', 'screens[9].widget', F(3, 4) * 12, 12 // 4, 12 // 3, 12 * 3)
lv.expect('l1', 'screens[9].hints[2].text', 12 // 4)
lv.expect('l1', 'quiz[0].widget.options[0].text', float(F(3, 2 * 4)))
lv.expect('l1', 'quiz[0].widget.options[1].text', float(F(3, 5)))
lv.expect('l1', 'quiz[0].widget.options[2].text', float(F(3, 4)))
lv.expect('l1', 'quiz[0].widget.options[3].text', float(F(5, 8)))
lv.claim(len(doc('l1')['quiz'][0]['canvas']['state']['shade']) == 3, 'l1 quiz[0]: 3 cells shaded')
lv.claim(round(1 / doc('l1')['quiz'][1]['canvas']['params']['step']) + 1 == 4, 'l1 quiz[1]: thirds line has 4 marks')
lv.expect('l1', 'quiz[1].widget.options[0].text', float(F(2, 3)))
num('l1', 'quiz[3].widget', F(2, 5) * 20, 20 // 5, 20 // 2, 20 * 2)
lv.claim(F(7, 4) > 1 and F(4, 7) < 1 and F(3, 3) == 1, 'l1 quiz[4]: only 7/4 passes one whole')

# ---------- l2 ----------
num('l2', 'screens[0].widget', 3 * 2, 3, 8, 3 + 1)
lv.claim(len(doc('l2')['screens'][1]['widget']['answer']) == 9 * F(2, 3), 'l2 screens[1]: 6 of 9 cells is 2/3')
num('l2', 'screens[2].widget', 2 * 4, 2 + (12 - 3), 2, 2 * 3)
lv.claim(F(6, 10) == F(3, 5), 'l2 screens[3]: 6/10 = 3/5')
for i, v in enumerate([F(3, 5), F(3, 10), F(6, 5), F(6 - 2, 10 - 2)]):
    lv.expect('l2', f'screens[3].widget.options[{i}].text', float(v))
num('l2', 'screens[4].widget', F(2, 3) * 15, F(3, 5) * 15, 2 * 3, 2)
lv.expect('l2', 'screens[4].explain.text', 10)
lv.expect('l2', 'screens[4].explain.text', 9)
lv.claim(F(3, 4) > F(2, 3) and F(2, 3) == F(8, 12) and F(3, 4) == F(9, 12), 'l2 trap: 9/12 beats 8/12')
lv.expect('l2', 'screens[5].hints[1].text', 8)
lv.expect('l2', 'screens[5].hints[1].text', 9)
lv.claim(F(9, 12) == F(3, 4) and F(4, 5) != F(3, 4) and F(6, 4) == 2 * F(3, 4) and F(3, 8) == F(3, 4) / 2, 'l2 screens[6] options')
lv.expect('l2', 'screens[7].widget.lines[2].text', 12)
lv.expect('l2', 'screens[7].widget.lines[2].text', 8)
a, b = F(3, 8) * 40, F(2, 5) * 40
lv.claim((a, b) == (15, 16) and 3 * 5 == a and 2 * 8 == b, 'l2 screens[8]: A keeps 15 (3 cols of 5), B keeps 16 (2 rows of 8)')
lv.expect('l2', 'screens[8].widget.options[0].text', b - a)
lv.expect('l2', 'screens[8].hints[2].text', 15)
lv.expect('l2', 'screens[8].hints[2].text', 16)
lv.expect('l2', 'screens[8].widget.options[3].why', 15)
num('l2', 'quiz[0].widget', F(4, 6) * 3, 4 - 3, 4)
for i, v in enumerate([F(4, 10), F(3, 6), F(4, 5), F(2, 10)]):
    lv.expect('l2', f'quiz[1].widget.options[{i}].text', float(v))
lv.claim(F(5, 6) == F(20, 24) and F(7, 8) == F(21, 24), 'l2 quiz[2]: 20/24 and 21/24')
lv.expect('l2', 'quiz[2].explain.text', 20)
lv.expect('l2', 'quiz[2].explain.text', 21)
for i, v in enumerate([F(3, 4), F(9 // 3, 12 // 2), F(9 - 3, 12 - 3)]):
    lv.expect('l2', f'quiz[3].widget.options[{i}].text', float(v))

# ---------- l3 ----------
lv.expect('l3', 'screens[0].widget.points[0].target', 0.75)
inside('l3', 'screens[0].widget', 0, F(1, 2) - F(1, 4))
inside('l3', 'screens[0].widget', 1, F(1, 2) + F(1, 2))
lv.claim(len(doc('l3')['screens'][1]['widget']['answer']) == (F(1, 2) + F(1, 3)) * 6, 'l3 screens[1]: 5 sixths shaded')
num('l3', 'screens[2].widget', r(F(1, 3) + F(1, 4), 4), r(F(2, 7), 4), r(F(2, 12), 4), 4 + 3)
lv.expect('l3', 'screens[3].widget.points[0].target', float(F(3, 4) - F(1, 3)))
inside('l3', 'screens[3].widget', 0, F(9 - 3, 12))
inside('l3', 'screens[3].widget', 1, F(9 - 1, 12))
num('l3', 'screens[4].widget', (F(1, 4) + F(1, 6)) * 12, 1 + 1, 4 + 6)
lv.expect('l3', 'screens[5].widget.points[0].target', float(F(3, 4) + F(1, 2)))
inside('l3', 'screens[5].widget', 0, 1)
lv.claim(F(2, 5) < F(1, 2), 'l3 trap: 2/5 is below 1/2')
lv.expect('l3', 'screens[6].explain.text', float(F(1, 2) + F(1, 3)))
for i, v in enumerate([F(7, 9), F(7, 18), F(10, 81)]):
    lv.expect('l3', f'screens[7].widget.options[{i}].text', float(v))
lv.claim(F(2, 3) == F(10, 15) and F(1, 5) == F(3, 15) and F(2, 3) + F(1, 5) == F(13, 15), 'l3 screens[8]: 10/15 + 3/15 = 13/15')
lv.expect('l3', 'screens[8].widget.lines[3].text', float(F(13, 15)))
num('l3', 'screens[9].widget', (F(1, 3) + F(1, 4)) * 1200, r(F(2, 7) * 1200, 2), F(1, 3) * 1200, (1 - F(7, 12)) * 1200)
lv.expect('l3', 'screens[9].hints[2].text', 1200 // 12)
lv.expect('l3', 'screens[9].feedback.byKey.you-only', F(1, 4) * 1200)
for i, v in enumerate([F(1, 2) + F(1, 6), F(2, 8), F(2, 6)]):
    lv.expect('l3', f'quiz[0].widget.options[{i}].text', float(v))
num('l3', 'quiz[1].widget', float(F(5, 6) - F(1, 3)), r(F(5 - 1, 6 - 3), 4), r(F(5 - 1, 6), 4))
num('l3', 'quiz[2].widget', float(F(3, 4) * 2), float(F(6, 8)))
num('l3', 'quiz[3].widget', float(F(2, 5) + F(1, 2)), r(F(3, 7), 4), float(F(3, 10)))
# Finding 9: the placeholder shows the add-tops-and-bottoms answer itself.
lv.stated('l3', 'quiz[3].widget.placeholder', '3/7', F(3, 7) != F(2 + 1, 5 + 2))

# ---------- l4 ----------
lv.expect('l4', 'screens[0].widget.options[0].text', float(F(1, 2) * F(1, 2)))
lv.claim(F(6, 12) == F(2, 3) * F(3, 4) == F(1, 2), 'l4 screens[1]: 6 of 12 = 2/3 of 3/4 = 1/2')
num('l4', 'screens[2].widget', float(F(1, 2) * F(3, 5)), r(F(1 + 3, 2 + 5), 4), float(F(1, 2) + F(3, 5)), 0.6, 0.5)
lv.claim(F(3, 4) * F(2, 3) == F(6, 12), 'l4 screens[3]: 3/4 of 2/3 = 6/12')
num('l4', 'screens[4].widget', float(F(3, 4) * 2), 0.75, 3 * 2)
lv.claim(F(1, 2) * F(4, 5) == F(2, 5) < F(1, 2) < F(4, 5), 'l4 trap: 2/5 below both')
for i, v in enumerate([F(6, 20), F(5, 9), F(8, 15), F(2, 5) + F(3, 4)]):
    lv.expect('l4', f'screens[6].widget.options[{i}].text', float(v))
num('l4', 'screens[8].widget', F(1, 4) * F(2, 3) * 1200, F(1, 4) * 1200, F(2, 3) * 1200, (F(1, 4) + F(2, 3)) * 1200)
lv.expect('l4', 'screens[8].explain.text', 800)
lv.claim(len(doc('l4')['screens'][8]['canvas']['state']['shade']['yours']) == F(1, 4) * 8, 'l4 screens[8]: 2 of the 8 paid-out cells')
for i, v in enumerate([F(1, 6), F(2, 5), F(5, 6)]):
    lv.expect('l4', f'quiz[0].widget.options[{i}].text', float(v))
num('l4', 'quiz[1].widget', F(3, 5) * 20, 20 // 5, 20 * 3)
for i, v in enumerate([F(2, 5), F(5, 8), F(6, 5)]):
    lv.expect('l4', f'quiz[2].widget.options[{i}].text', float(v))
lv.expect('l4', 'quiz[3].explain.text', 0.25)

# ---------- l5 ----------
num('l5', 'screens[0].widget', 3 * 2, 1.5, 3)
lv.expect('l5', 'screens[1].widget.points[0].target', float(3 * F(2, 3)))
inside('l5', 'screens[1].widget', 0, F(2, 3))
inside('l5', 'screens[1].widget', 1, F(3, 3))
num('l5', 'screens[2].widget', 3 / F(3, 4), float(3 * F(3, 4)), float(F(3, 4) / 3))
num('l5', 'screens[3].widget', float(1 / F(2, 3)), 1, r(F(2, 3), 4), r(1 + F(1, 3), 4))
num('l5', 'screens[4].widget', F(3, 4) / F(1, 8), float(F(1, 8) * F(3, 4)), 3)
lv.expect('l5', 'screens[5].widget.options[0].text', 6 / F(1, 2))
lv.expect('l5', 'screens[5].widget.options[2].text', float(F(1, 2) / 6))
for i, v in enumerate([4 / F(2, 5), 4 * F(2, 5), F(2, 5) / 4, F(4, 2)]):
    lv.expect('l5', f'screens[6].widget.options[{i}].text', float(v))
num('l5', 'screens[8].widget', F(3, 4) / F(1, 8), float(F(1, 8) * F(3, 4)), r(F(1, 8) / F(3, 4), 4), 3)
num('l5', 'quiz[0].widget', 4 / F(1, 3), r(4 * F(1, 3), 4), r(F(1, 3) / 4, 4))
for i, v in enumerate([F(3, 4) / F(1, 4), F(3, 4) * F(1, 4), F(1, 4) / F(3, 4)]):
    lv.expect('l5', f'quiz[1].widget.options[{i}].text', float(v))
num('l5', 'quiz[2].widget', F(1, 2) / F(1, 4), float(F(1, 4) * F(1, 2)), float(F(1, 4) / F(1, 2)))
lv.expect('l5', 'quiz[3].explain.text', 5 / F(1, 2))
lv.expect('l5', 'quiz[3].explain.text', '2\\tfrac{1}{2}')            # 5 x 1/2 = 2 1/2, written as a mixed number
lv.claim(5 * F(1, 2) == 2 + F(1, 2), 'l5 quiz[3]: half of 5 is 2 1/2')

# ---------- review-1 ----------
for i, v in enumerate([F(3, 5), F(3, 6), F(2, 5)]):
    lv.expect('review', f'items[0].widget.options[{i}].text', float(v))
num('review', 'items[1].widget', F(3, 4) * 20, 3 + (20 - 4), 3)
num('review', 'items[2].widget', r(F(2, 3) + F(1, 4), 4), r(F(3, 7), 4), r(F(3, 12), 4))
for i, v in enumerate([F(2, 3) * F(3, 5), F(5, 8), F(2, 3) + F(3, 5), F(10, 9)]):
    lv.expect('review', f'items[3].widget.options[{i}].text', float(v))
num('review', 'items[4].widget', 2 / F(1, 4), float(2 * F(1, 4)), float(F(1, 4) / 2))
lv.claim(F(5, 8) == F(25, 40) and F(3, 5) == F(24, 40), 'review items[5]: 25/40 against 24/40')
num('review', 'items[6].widget', (1 - F(1, 4) - F(1, 3)) * 60, (F(1, 4) + F(1, 3)) * 60, r(60 - F(2, 7) * 60, 3), 60 - 20, 60 - 15)
lv.expect('review', 'items[7].explain.text', float(F(3, 4) / F(2, 3)))
lv.expect('review', 'items[7].explain.text', float(F(3, 4) * F(2, 3)))
cs = doc('review')['items'][8]['canvas']['params']['colSizes']
lv.claim(F(cs[0], sum(cs)) == F(1, 4), 'review items[8]: shaded piece is 1/4 of the bar')

# ---------- homework-1 ----------
lv.expect('homework', 'items[0].widget.points[0].target', 1.75)
inside('homework', 'items[0].widget', 0, 1)
inside('homework', 'items[0].widget', 1, F(3, 4))
lv.claim(all(F(t) == F(2, 3) for t in ['4/6', '10/15', '6/9']) and F(3, 4) != F(2, 3) and F(4, 9) != F(2, 3), 'homework items[1]: three equivalents')
num('homework', 'items[2].widget', r(F(5, 6) - F(3, 4), 4), F(5 - 3, 6 - 4), r(F(5 - 3, 12), 4))
num('homework', 'items[3].widget', F(1, 3) * F(4, 5) * 2400, F(1, 3) * 2400, F(1, 5) * 2400 / 3, F(4, 5) * 2400, F(1, 5) * 2400)
num('homework', 'items[4].widget', F(5, 2) / F(5, 8), float(F(5, 2) * F(5, 8)), float(F(5, 8) / F(5, 2)))
lv.claim(F(3, 4) / F(3, 8) == 2 == F(6, 8) / F(3, 8), 'homework items[5]: 3/4 divided by 3/8 is 2')
p1 = 40 + F(1, 4) * 40
p2 = p1 - F(1, 5) * p1
num('homework', 'items[6].widget', p2 - 40, (F(1, 4) - F(1, 5)) * 40, F(1, 4) * 40, (F(1, 5) - F(1, 4)) * 40)
lv.expect('homework', 'items[7].model', F(3, 4) * F(2, 3) * 900)
lv.expect('homework', 'items[7].model', 900 // 12)
lv.expect('homework', 'items[7].model', F(2, 3) * 900)
lv.expect('homework', 'items[7].model', (F(3, 4) + F(2, 3)) * 900)
# Finding 1: you own three quarters, not a quarter.
lv.stated('homework', 'items[7].model', 'quarter-share', False)
for v in [F(1, 2), F(3, 5), F(2, 3), F(3, 4)]:
    lv.expect('homework', 'items[8].explain.text', v * 60)

lv.check_wrongs()
lv.report()
