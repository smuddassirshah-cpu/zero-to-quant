"""Second-read number checks for number-sense level 2 (l6 to l9, review-2, homework-2).

Every graded key and wrong[] value is recomputed here. Rounding is half up (UK GCSE), done with Decimal.
Two checks fail on the current content because the content is wrong (review-number-sense-1-3.md findings 8
and 6): they pass once the fix rewords the text.
"""
import os
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('number-sense', 2)


def doc(f):
    return lv._file(f)[1]


def hu(x, d):
    """Round half up to d places (GCSE convention), from an exact Fraction or a decimal string."""
    x = D(x) if isinstance(x, str) else D(x.numerator) / D(x.denominator) if isinstance(x, F) else D(str(x))
    return float(x.quantize(D(1).scaleb(-d), rounding=ROUND_HALF_UP))


def num(f, base, ans, *wrongs):
    lv.expect(f, base + '.answer', ans)
    for i, v in enumerate(wrongs):
        lv.expect(f, f'{base}.wrong[{i}].value', v)


def node(f, base):
    n = doc(f)
    for part in base.replace(']', '').replace('[', '.').split('.'):
        n = n[int(part)] if part.isdigit() else n[part]
    return n


def inside(f, base, i, value):
    xs = node(f, base)['wrong'][i]['region']['x']
    lv.claim(xs[0] <= float(value) <= xs[1], f'{f} {base}.wrong[{i}] region {xs} holds {float(value):.4f}')


# ---------- l6 ----------
lv.expect('l6', 'screens[1].widget.points[0].target', float(F(7, 10)))
inside('l6', 'screens[1].widget', 0, F(6, 10))          # counted the tick at 0
inside('l6', 'screens[1].widget', 1, 1 - F(7, 10))      # counted back from 1
lv.expect('l6', 'screens[2].widget.points[0].target', 0.74)
inside('l6', 'screens[2].widget', 0, 0.73)
for i, v in enumerate([F(74, 100), F(74, 10), F(7 + 4, 10), F(7, 4)]):
    lv.expect('l6', f'screens[3].widget.options[{i}].text', float(v))
lv.claim(F(74, 10) > 7, 'l6 screens[3]: 74 tenths is more than 7 wholes')
lv.expect('l6', 'screens[4].widget.points[0].target', 1.06)
inside('l6', 'screens[4].widget', 0, 1.6)
lv.claim(F(106, 100) - 1 > F(1, 2) * F(1, 10), 'l6 screens[4] hint: 1.06 is a little more than halfway to 1.1')
lv.expect('l6', 'screens[5].widget.points[0].target', hu('2.37', 1))
inside('l6', 'screens[5].widget', 0, 2.3)
lv.expect('l6', 'screens[5].explain.text', float(D('2.4') - D('2.37')))
lv.expect('l6', 'screens[5].explain.text', float(D('2.37') - D('2.3')))
lv.claim(D('0.5') > D('0.45') and D('0.5') - D('0.45') == D('0.05'), 'l6 trap: 0.45 is half a tenth short of 0.5')
lv.claim(D('3.1') > D('3.09'), 'l6 screens[7]: 3.1 > 3.09')
lv.claim(F(D('2.375')) == F(2375, 1000) == 2 + F(3, 10) + F(7, 100) + F(5, 1000), 'l6 screens[8]: 2.375 = 2375/1000')
for t in (2000, 300, 70, 5):
    lv.expect('l6', 'screens[8].widget.lines[1].text', t)
q = {'a': D('12.5'), 'b': D('12.45'), 'c': D('12.48')}
lv.claim(min(q, key=q.get) == 'b' and [o['id'] for o in node('l6', 'screens[9].widget')['options'] if o.get('correct')] == ['b'], 'l6 screens[9]: broker B is lowest')
lv.claim(max([D('0.6'), D('0.58'), D('0.508')]) == D('0.6'), 'l6 quiz[0]: 0.6 is largest')
num('l6', 'quiz[1].widget', 30, 3, 300)
num('l6', 'quiz[2].widget', hu('3.96', 1), 3.9, 3.1)
lv.expect('l6', 'quiz[2].explain.text', float(D('4.0') - D('3.96')))
num('l6', 'quiz[3].widget', int((D('12.50') - D('12.45')) / D('0.01')), float(D('12.50') - D('12.45')), 50)

# ---------- l7 ----------
lv.claim(len(node('l7', 'screens[1].canvas.state.shade')) == 25, 'l7 screens[1]: 25 cells shaded')
num('l7', 'screens[1].widget', 100 // 4, 4, 10 / 4)
lv.expect('l7', 'screens[2].widget.points[0].target', float(F(3, 5)))
inside('l7', 'screens[2].widget', 0, F(3, 10))
num('l7', 'screens[3].widget', float(F(7, 20)), float(F(7, 10)), 0.72, hu(F(20, 7), 3))
num('l7', 'screens[4].widget', float(F(3, 8)), 0.3, hu(F(8, 3), 3), 0.38)
lv.claim(8 * 125 == 1000, 'l7 screens[4]: 8 x 125 = 1000')
# Finding 8: 0.38 is also 3/8 rounded to two places, not only the digits side by side.
lv.stated('l7', 'screens[4].feedback.byKey.point-three-eight', 'You wrote the digits 3 and 8 side by side.', hu(F(3, 8), 2) != 0.38)
lv.claim(all(10 ** k % 3 == 1 for k in range(1, 10)), 'l7 screens[5]: every power of ten leaves 1 over when divided by 3')
lv.expect('l7', 'screens[7].widget.points[0].target', hu(F(2, 3), 2))
inside('l7', 'screens[7].widget', 0, 0.66)
lv.expect('l7', 'screens[7].hints[2].text', hu(F(2, 3) - F(66, 100), 3))
lv.expect('l7', 'screens[7].hints[2].text', hu(F(67, 100) - F(2, 3), 3))
lv.claim(F(1, 3) - F(33, 100) == F(1, 300) and 3 * D('0.33') == D('0.99'), 'l7 trap: 0.33 is 1/300 short of 1/3')
lv.expect('l7', 'screens[8].explain.text', float(F(1, 300)))


def stops(fr):
    b = fr.denominator
    for p in (2, 5):
        while b % p == 0:
            b //= p
    return b == 1


lv.claim(stops(F(7, 40)) and not any(stops(x) for x in (F(1, 6), F(2, 9), F(5, 12))), 'l7 screens[9]: only 7/40 stops')
lv.expect('l7', 'screens[9].explain.text', float(F(7, 40)))
lv.claim(F(125, 1000) == F(25, 200) == F(1, 8), 'l7 screens[10]: 125/1000 = 25/200 = 1/8')
tot = D('10.00') + D('10.01') + D('10.01')
lv.expect('l7', 'screens[11].canvas.params.rows[3]', float(tot))
num('l7', 'screens[11].widget', hu(tot / 3, 2), 10.0, hu(tot / 3, 5))
num('l7', 'quiz[0].widget', float(F(9, 25)), 0.925, hu(F(25, 9), 3), 0.9)
lv.expect('l7', 'quiz[1].widget.options[0].text', hu(F(5, 6), 2))
lv.claim(stops(F(3, 12)) and F(3, 12) == F(1, 4), 'l7 quiz[2]: 3/12 = 1/4 stops')
num('l7', 'quiz[3].widget', hu(F(100, 3), 2), 33.34, 33.3, hu(F(100, 3), 3))
lv.expect('l7', 'quiz[3].explain.text', float(3 * D('33.33')))

# ---------- l8 ----------
lv.expect('l8', 'screens[1].widget.points[0].target', 3 - 5)
inside('l8', 'screens[1].widget', 0, 5 - 3)
inside('l8', 'screens[1].widget', 1, 0)
lv.expect('l8', 'screens[2].explain.text', -2 - (-7))
num('l8', 'screens[3].widget', -4 + 7, -4 - 7, -(-4 + 7), 4 + 7)
lv.expect('l8', 'screens[4].widget.points[0].target', 6 + (-9))
inside('l8', 'screens[4].widget', 0, 9 - 6)
num('l8', 'screens[5].widget', -2 + (-5) + (-4), 2 + 5 + 4, -2 + (-5), -2 + (-5) - (-4))
for i, v in enumerate([-3 + (-8), -3 - (-8), -(8 - 3), 3 + 8]):
    lv.expect('l8', f'screens[6].widget.options[{i}].text', v)
lv.expect('l8', 'screens[7].feedback.correct', 4 - (-6))
lv.claim(5 + (-8) == -3 and -3 - (-8) == 5 and -3 + (-8) == -11, 'l8 screens[8] lines')
vals = node('l8', 'screens[9].canvas.params.series[0].values')
pk = max(range(len(vals)), key=lambda i: vals[i])
low = min(vals[pk:])
lv.claim(pk == 1 and vals.index(low) == 3, 'l8 screens[9]: peak day 1, low day 3')
num('l8', 'screens[9].widget', vals[pk] - low, -low - vals[pk], -(vals[pk] - low), vals[pk] + low)
lv.claim(min([-12, -3, 0, -15]) == -15 and -12 - (-15) == 3, 'l8 quiz[0]: -15 coldest, 3 below -12')
num('l8', 'quiz[1].widget', -7 + 10, -7 - 10, -3, 7 + 10)
num('l8', 'quiz[2].widget', 4 - (-5), 5 - 4, -(4 - (-5)), -5 + 4)
num('l8', 'quiz[3].widget', -150 + (-75), -150 + 75, 150 + 75)
num('l8', 'quiz[4].widget', float(D('-4.25') - D('-4.25')), float(D('-4.25') * 2), float(D('4.25') * 2))

# ---------- l9 ----------
lv.expect('l9', 'screens[1].widget.points[0].target', 4 * (-3))
inside('l9', 'screens[1].widget', 0, 4 * 3)
inside('l9', 'screens[1].widget', 1, -(3 + 4))
lv.expect('l9', 'screens[2].widget.points[0].target', (-2) * (-3))
inside('l9', 'screens[2].widget', 0, 2 * (-3))
lv.expect('l9', 'screens[3].widget.options[0].text', (-2) * (-3))
rows = node('l9', 'screens[4].widget.rows')
lv.claim(all(row[1]['answer'] == (-3) * int(str(row[0]).strip('$')) for row in rows if isinstance(row[1], dict)), 'l9 screens[4]: table cells are (-3) x k')
num('l9', 'screens[5].widget', (-4) * (-5), -20, -4 + (-5), 4 + 5)
num('l9', 'screens[6].widget', F(-20, -4), -5, (-20) * (-4))
for i, v in enumerate([-4 + (-6), 10, (-4) * (-6)]):
    lv.expect('l9', f'screens[7].widget.options[{i}].text', v)
# Finding 6: taking 4 from 6 gives 2, not the option's -2.
lv.stated('l9', 'screens[7].widget.options[3].why', 'You took 4 from 6.', 6 - 4 == -2)
lv.expect('l9', 'screens[8].feedback.correct', (-2) * (-3) * (-5))
lv.expect('l9', 'screens[9].prose', 3 * 2 + 3 * 5)
lv.claim((-3) * (2 + (-2)) == 0 and (-3) * 2 == -6, 'l9 screens[9] lines')
chg = D('10.90') - D('12.40')
num('l9', 'screens[10].widget', float(-200 * chg), float(200 * chg), float(-200 * D('10.90')), float(chg))
num('l9', 'quiz[0].widget', (-6) * 4, 24, -6 + 4)
num('l9', 'quiz[1].widget', (-7) * (-8), -56, -7 + (-8))
num('l9', 'quiz[2].widget', 36 // -4, 9, 36 * (-4))
num('l9', 'quiz[3].widget', float(300 * D('-0.25')), 75, float(300 + D('-0.25')))
num('l9', 'quiz[4].widget', float(D('-0.5') * D('-0.5') * -4), 1, float(D('-0.5') * D('-0.5')))

# ---------- review-2 ----------
lv.claim(max([D('2.09'), D('2.1'), D('2.089')]) == D('2.1'), 'review items[0]: 2.1 is highest')
num('review', 'items[1].widget', float(F(3, 4)), 0.34, hu(F(4, 3), 3), 0.3)
num('review', 'items[2].widget', -6 + 4, -6 - 4, 6 - 4)
num('review', 'items[3].widget', float(D(-8) * D('-0.5')), -4, float(D(-8) + D('-0.5')), float(D(8) / D('0.5')))
num('review', 'items[4].widget', hu(F(20, 7), 2), 2.85, hu(F(20, 7), 3), float(F(7, 20)))
num('review', 'items[5].widget', float(D('2.5') - D('-7.5')), float(D('2.5') - D('7.5')), float(D('7.5') - D('2.5')), -10)
num('review', 'items[6].widget', hu('12.996', 2), 12.99, 12.1)
lv.expect('review', 'items[6].explain.text', float(D('13.00') - D('12.996')))
num('review', 'items[7].widget', float(-150 * (D('8.65') - D('8.40'))), 37.5, float(-150 * D('8.65')))
num('review', 'items[8].widget', float(D('45.50') - D('-18.25')), float(D('45.50') - D('18.25')), -63.75)
order = sorted([(F(3, 10), 'a'), (F(1, 3), 'b'), (F(34, 100), 'c'), (F(3, 8), 'd')])
lv.claim([t for _, t in order] == ['a', 'b', 'c', 'd'], 'review items[9]: 0.3 < 1/3 < 0.34 < 3/8')

# ---------- homework-2 ----------
amts = {'o1': F(-1, 2), 'o2': F(-1, 3), 'o3': F(3, 10), 'o4': F(1, 3), 'o5': F(34, 100)}
lv.claim(sorted(amts, key=amts.get) == node('homework', 'items[0].widget.answer'), 'homework items[0]: order of the five amounts')
num('homework', 'items[1].widget', hu(F(7, 12), 3), 0.58, hu(F(12, 7), 3), 0.712)
lv.claim(divmod(70, 12) == (5, 10) and divmod(100, 12) == (8, 4) and divmod(40, 12) == (3, 4), 'homework items[1]: remainders 10, 4, 4')
days = [D('84.50'), D('-126.25'), D('-37.80'), D('52.15'), D('-9.60')]
run = []
s = D(0)
for d in days:
    s += d
    run.append(s)
num('homework', 'items[2].widget', float(s), float(-s), float(sum(abs(d) for d in days)), float(sum(d for d in days if d < 0)))
for v in run:
    lv.expect('homework', 'items[2].explain.text', float(v))
lv.expect('homework', 'items[2].explain.text', float(sum(d for d in days if d > 0)))
lv.claim([float(v) for v in run] == node('homework', 'items[3].canvas.params.series[0].values')[1:], 'homework items[3]: series matches the running totals')
dd = max(run[i] - min(run[i:]) for i in range(len(run)))
num('homework', 'items[3].widget', float(dd), float(run[0] + run[2]), float(-days[1]), float(run[0] - run[-1]))
num('homework', 'items[4].widget', float(400 * D('-0.35') + (-250) * D('-1.12')), float(400 * D('-0.35') - 250 * D('1.12')), float(400 * D('0.35') + 250 * D('1.12')), float(400 * D('-0.35')))
digit = int('142857'[(100 - 1) % 6])
num('homework', 'items[5].widget', digit, int('142857'[5]), int('142857'[4]), int('142857'[0]))
lv.claim(16 * 6 == 96, 'homework items[5]: 16 blocks fill 96 places')
cost = 200 * D('20.13') + 100 * D('20.21')
num('homework', 'items[7].widget', hu(F(cost) / 300, 2), hu((D('20.13') + D('20.21')) / 2, 2), 20.15, hu(F(cost) / 300, 3))
for t in (200 * D('20.13'), 100 * D('20.21'), cost):
    lv.expect('homework', 'items[7].explain.text', float(t))
lv.expect('homework', 'items[8].model', -40 - (-15))
lv.expect('homework', 'items[8].model', float(-100 * D('-0.60')))

lv.check_wrongs()
lv.report()
