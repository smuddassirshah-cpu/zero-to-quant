"""Second-read number checks for number-sense level 3 (l10 to l14, review-3, homework-3).

Every graded key and wrong[] value is recomputed here. Rounding is half up (UK GCSE), done with Decimal.
Fix pass (review-number-sense-1-3.md): the checks that failed on the original content now pass on the fixed text.
"""
import math
import os
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level('number-sense', 3)


def doc(f):
    return lv._file(f)[1]


def hu(x, d):
    if isinstance(x, D):
        pass
    elif isinstance(x, str):
        x = D(x)
    elif isinstance(x, F):
        x = D(x.numerator) / D(x.denominator)
    else:
        x = D(repr(x))
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


# ---------- l10 ----------
w = node('l10', 'screens[0].widget')
lv.claim(len(w['answer']) == 3 ** 2 and [len(x['set']) for x in w['wrong']] == [3, 6, 3 + 3 - 1], 'l10 screens[0]: 9 tiles; slips of 3, 6 and 5')
num('l10', 'screens[1].widget', 3 ** 3, 3 ** 2, 3 ** 2 + 3, 2 * 3 ** 2)
for i, v in enumerate([5 * 2, 5 + 2, 5 ** 2, 2 ** 5]):
    lv.expect('l10', f'screens[2].widget.options[{i}].text', v)
num('l10', 'screens[3].widget', 3 + 2, 3 * 2, 2 ** 5, 3 - 2)
num('l10', 'screens[4].widget', 5 - 2, 5 / 2, 5 + 2, 2 ** 3)
num('l10', 'screens[5].widget', 3 * 2, 3 + 2, 3 ** 2, 2 ** 6)
lv.claim(2 ** 3 + 2 ** 3 == 16 == 2 ** 4 and 2 ** 6 == 64 == 4 ** 3 == 4 * 16, 'l10 trap: 16 tiles; 2^6 and 4^3 are 64')
lv.expect('l10', 'screens[6].widget.options[3].why', 4 ** 6)
# Finding 2: the dividing law needs a non-zero base.
lv.stated('l10', 'screens[7].prose', 'For any number $a$:', False)
lv.claim(abs(1.072 ** 10 - 2) < 0.01, 'l10 screens[9]: 7.2% a year roughly doubles in 10 years')
num('l10', 'screens[9].widget', 1000 * 2 ** 4, 1000 * 2 * 4, 1000 + 4 * 1000, 1000 * 2 ** 5)
num('l10', 'quiz[0].widget', 3 ** 4, 3 * 4, 4 ** 3, 3 + 4, 3 ** 3)
lv.expect('l10', 'quiz[1].explain.text', 10 ** 7)
num('l10', 'quiz[2].widget', 2 * 3, 2 + 3, 2 ** 3, 3 ** 2)
num('l10', 'quiz[3].widget', float(100 * D('1.02') ** 2), 100 + 2 * 2)
lv.expect('l10', 'quiz[3].explain.text', float(D('1.02') ** 2))
lv.expect('l10', 'quiz[3].feedback.byKey.simple', float(D('0.02') * 102))

# ---------- l11 ----------
num('l11', 'screens[0].widget', math.isqrt(36), 36 // 2, 36 // 4, 36 // 3)
for k, v in (('halved', 18 ** 2), ('quartered', 9 ** 2), ('third', 12 ** 2)):
    lv.expect('l11', f'screens[0].feedback.byKey.{k}', v)
lv.expect('l11', 'screens[1].widget.points[0].target', 7)
inside('l11', 'screens[1].widget', 0, 6.5)
inside('l11', 'screens[1].widget', 1, 7.5)
lv.expect('l11', 'screens[1].feedback.byKey.low', 6.5 ** 2)
lv.expect('l11', 'screens[1].feedback.byKey.high', 7.5 ** 2)
lv.claim(5.0 ** 2 < 26 and 5.5 > 5.1, 'l11 screens[1]: every snapped side in the "half" region (x <= 5) has area under 26')
for i, v in enumerate([64 // 2, round(64 ** (1 / 3)), math.isqrt(64), 64 ** 2]):
    lv.expect('l11', f'screens[2].widget.options[{i}].text', v)
lv.expect('l11', 'screens[2].widget.options[0].why', 32 ** 2)
lv.expect('l11', 'screens[3].explain.text', hu(math.sqrt(50), 2))
lv.expect('l11', 'screens[3].explain.text', hu(7.07 ** 2, 2))
lv.expect('l11', 'screens[3].widget.options[0].why', 64 - 50)
lv.expect('l11', 'screens[3].widget.options[2].why', 25 ** 2)
num('l11', 'screens[4].widget', round(125 ** (1 / 3)), hu(math.sqrt(125), 2), hu(F(125, 3), 2))
lv.claim(abs(41.67 ** 3 - 72000) < 1000, 'l11 screens[4]: 41.67 cubed is about 72,000')
lv.expect('l11', 'screens[5].explain.text', hu(100 ** (1 / 3), 2))
lv.claim(abs(33 ** 3 - 36000) < 100 and 4 ** 3 < 100 < 5 ** 3, 'l11 screens[5]: 64 < 100 < 125; 33^3 about 36,000')
num('l11', 'screens[6].widget', math.sqrt(0.25), 0.25 / 2, 0.25 ** 2, 0.05)
lv.claim(abs(0.125 ** 2 - 0.016) < 0.0005 and abs(0.05 ** 2 - 0.0025) < 1e-12, 'l11 trap byKey squares')
lv.expect('l11', 'screens[7].explain.text', hu(math.sqrt(30), 2))
lv.expect('l11', 'screens[7].widget.options[1].why', 15 ** 2)
lv.expect('l11', 'screens[7].widget.options[3].why', 29 ** 2)
lv.expect('l11', 'screens[8].widget.lines[3].text', float(D('4.4') ** 2))
lv.expect('l11', 'screens[8].widget.lines[3].text', float(D('4.5') ** 2))
lv.expect('l11', 'screens[8].explain.text', hu(math.sqrt(20), 2))
lv.expect('l11', 'screens[8].explain.text', hu(4.47 ** 2, 2))
# Finding 7: the lines stop at 4.4 < sqrt(20) < 4.5, which does not settle one decimal place (4.45^2 = 19.8025 < 20).
lines = ' '.join(l['text'] for l in node('l11', 'screens[8].widget.lines'))
lv.stated('l11', 'screens[8].prose', 'to one decimal place', '4.45' in lines)
num('l11', 'screens[9].widget', hu(0.01 * math.sqrt(252), 4), 0.01 * 252, 0.01 * 126, hu(0.01 * math.sqrt(252) / 100, 5))
wd = node('l11', 'screens[9].widget')
lv.claim(wd['answer'] - wd['tol']['abs'] <= 0.153 and 0.164 <= wd['answer'] + wd['tol']['abs'], 'l11 screens[9]: 15.3% to 16.4% all accepted')
lv.claim(abs(126 ** 2 - 16000) < 200, 'l11 screens[9]: 126^2 is nearly 16,000')
num('l11', 'quiz[0].widget', math.isqrt(81), 81 / 2, 81 ** 2)
lv.claim(40.5 ** 2 > 1600, 'l11 quiz[0]: 40.5^2 over 1,600')
lv.expect('l11', 'quiz[1].widget.options[0].why', 45 ** 2)
lv.expect('l11', 'quiz[1].widget.options[3].why', 30 ** 2)
lv.expect('l11', 'quiz[1].explain.text', hu(math.sqrt(90), 2))
num('l11', 'quiz[2].widget', float(D('0.09').sqrt()), float(D('0.09') / 2), 0.03, float(D('0.09') ** 2))
lv.expect('l11', 'quiz[2].feedback.byKey.kept-zeros', float(D('0.03') ** 2))
lv.claim(7 ** 2 == (-7) ** 2 == 49 and 49 / 2 == 24.5, 'l11 quiz[3]: x = 7 or -7')
num('l11', 'quiz[4].widget', round(8000 ** (1 / 3)), hu(math.sqrt(8000), 2), hu(F(8000, 3), 2))
lv.claim(2666.67 ** 3 > 1e9, 'l11 quiz[4]: cubing 2,666.67 gives billions')

# ---------- l12 ----------
num('l12', 'screens[0].widget', 2 + 3 * 4, (2 + 3) * 4, 2 + 3 + 4)
num('l12', 'screens[2].widget', 10 - 2 * 4, (10 - 2) * 4, 10 - 4)
for i, v in enumerate([(2 * 3) ** 2, 2 * (3 * 2), 2 + 3 ** 2, 2 * 3 ** 2]):
    lv.expect('l12', f'screens[3].widget.options[{i}].text', v)
st = node('l12', 'screens[4].widget.states')
lv.claim(20 - 2 * 3 ** 2 == int(st['s3']['tex']) and (20 - 2) * 3 ** 2 == int(st['m1c']['tex']) and 20 - (2 * 3) ** 2 == int(st['m2c']['tex']), 'l12 screens[4]: manipulate end states 2, 162, -16')
for i, v in enumerate([8 - (3 + 2), 8 - 3 + 2, 8 + 3 + 2]):
    lv.expect('l12', f'screens[5].widget.options[{i}].text', v)
for i, v in enumerate([6 + 4 / 2, (6 + 4) / 2, 6 / 2 + 4, 6 + 4]):
    lv.expect('l12', f'screens[6].widget.options[{i}].text', v)
lv.expect('l12', 'screens[7].widget.lines[3].text', 3 + 2 * (5 - 1) ** 2)
lv.expect('l12', 'screens[7].explain.text', (3 + 2) * (5 - 1) ** 2)
g = D('1.02') ** 3
num('l12', 'screens[8].widget', hu(1000 * g, 2), 1000 + 3 * 20, float((1000 * D('1.02')) ** 3), float(1000 + D('0.02') ** 3))
lv.expect('l12', 'screens[8].explain.text', float(g))
lv.expect('l12', 'screens[8].explain.canvas.values', float(1000 * D('1.02') ** 2))
lv.expect('l12', 'screens[8].explain.text', hu(1000 * g - 1060, 2))
num('l12', 'quiz[0].widget', 5 + 3 * 2 ** 2, (5 + 3) * 2 ** 2, (5 + 3 * 2) ** 2, 5 + (3 * 2) ** 2)
num('l12', 'quiz[1].widget', 18 // 3 * 2, 18 // (3 * 2))
lv.expect('l12', 'quiz[2].widget.options[2].text', -(3 ** 2))
num('l12', 'quiz[3].widget', (12 + 8) // 4 - 1, 12 + 8 // 4 - 1, hu(F(12 + 8, 4 - 1), 4))
lv.claim(float((500 * D('1.03')) ** 2) > 265000, 'l12 quiz[4]: (500 x 1.03)^2 is over 265,000')
lv.expect('l12', 'quiz[4].widget.options[2].why', float(500 * 1 + D('0.03') ** 2))
lv.expect('l12', 'quiz[4].explain.text', float(500 * D('1.03') ** 2))

# ---------- l13 ----------
lv.expect('l13', 'screens[0].explain.text', 48 * 21)
lv.expect('l13', 'screens[1].widget.points[0].target', 400)
inside('l13', 'screens[1].widget', 0, 300)
lv.claim(400 - 387 == 13 and 387 - 300 == 87, 'l13 screens[1]: 13 and 87')
lv.expect('l13', 'screens[2].widget.options[3].text', 0.04)
lv.expect('l13', 'screens[3].widget.points[0].target', 300 * 50)
inside('l13', 'screens[3].widget', 0, 300 * 40)
inside('l13', 'screens[3].widget', 1, 300 * 50 / 10)
lv.expect('l13', 'screens[3].explain.text', 312 * 48)
lv.expect('l13', 'screens[4].widget.options[1].text', 600 / 0.5)
lv.expect('l13', 'screens[4].explain.text', float(D(612) / D('0.48')))
lv.expect('l13', 'screens[5].widget.points[0].target', 40 * 5 / 0.2)
inside('l13', 'screens[5].widget', 0, 40 * 5)
inside('l13', 'screens[5].widget', 1, 40 * 5 / 2)
lv.expect('l13', 'screens[5].explain.text', hu(D('38.7') * D('5.12') / D('0.198'), 1))
vals = node('l13', 'screens[6].canvas.state.values')
lv.claim(vals['B'] == 312 * 48 and vals['A'] == vals['B'] / 10 and vals['C'] == vals['B'] * 10, 'l13 screens[6]: A, B, C are 14,976 over 10, times 1, times 10')
lv.expect('l13', 'screens[7].widget.options[0].text', float(D('0.6') * D('0.4')))
lv.expect('l13', 'screens[7].explain.text', float(D('0.62') * D('0.38')))
lv.expect('l13', 'screens[8].explain.text', float(D('23.80') * 395))
lv.claim(94010 > 10 * 20 * 400, 'l13 screens[8]: 94,010 is more than ten times 8,000')
lv.expect('l13', 'screens[9].explain.text', float(2150 * D('0.38')))
lv.expect('l13', 'screens[9].widget.options[3].text', float(2000 / D('0.4')))
lv.expect('l13', 'quiz[0].widget.options[3].text', 0.006)
num('l13', 'quiz[1].widget', 60 * 300, 50 * 300, 60 * 300 // 10, 59 * 312)
num('l13', 'quiz[2].widget', float(4000 / D('0.2')), float(4000 * D('0.2')), float(4000 / D('0.2') / 10))
lv.expect('l13', 'quiz[2].explain.text', round(4120 / 0.21))
lv.expect('l13', 'quiz[3].widget.options[1].text', 100)
lv.expect('l13', 'quiz[4].explain.text', float(4900 * D('19.70')))

# ---------- l14 ----------
num('l14', 'screens[0].widget', round(math.log10(1_000_000)), len('1000000'), '1,000,000'.count(','))
lv.expect('l14', 'screens[1].widget.points[0].target', math.floor(math.log10(4_500_000)))
inside('l14', 'screens[1].widget', 0, len('4500000'))
inside('l14', 'screens[1].widget', 1, '4500000'.count('0'))
lv.claim(D('3.8') * 10 ** 5 == 380000 and '380000'.count('0') == 4 and len('380000') == 6, 'l14 screens[2]: 3.8 x 10^5')
lv.expect('l14', 'screens[3].widget.points[0].target', math.floor(math.log10(0.00042)))
inside('l14', 'screens[3].widget', 0, -3)
inside('l14', 'screens[3].widget', 1, -5)
lv.claim(3e4 * 2e5 == 6e9 and 4e3 * 5e6 == 2e10, 'l14 screens[4] and [5] products')
lv.claim(2e-3 > 8e-4, 'l14 trap: 2 x 10^-3 beats 8 x 10^-4')
lv.claim(5e-3 * 3e8 == 1.5e6 and 15 * 10 ** (3 + 8) == 1.5e12, 'l14 screens[7]: 1.5 x 10^6; ignoring the minus gives 1.5 x 10^12')
lv.claim(D('4.5e8') / D('9e13') == D('5e-6') and D('9e13') / D('4.5e8') == D('2e5'), 'l14 screens[9]: 5 x 10^-6; upside down 2 x 10^5')
# Finding 3: adding the indices gives 0.5 x 10^21 = 5 x 10^20, not the option's 5 x 10^21.
lv.stated('l14', 'screens[9].widget.options[3].text', '5 \\times 10^{21}', D('0.5') * D(10) ** 21 == 5 * D(10) ** 21)
lv.claim(D('6.7e-3') == D('0.0067'), 'l14 quiz[0]: 0.0067 = 6.7 x 10^-3')
num('l14', 'quiz[1].widget', 3 + 2, 3 * 2, 3 - 2)
lv.expect('l14', 'quiz[1].explain.text', 2 * 4 * 10 ** 5)
lv.claim(max([3e5, 9e4, 1e6, 8e5]) == 1e6, 'l14 quiz[2]: 1 x 10^6 is largest')
lv.claim(D('6e4') / D('3e-2') == D('2e6'), 'l14 quiz[3]: 2 x 10^6')
# Finding 5: 18 x 10^2 is the product of the two numbers, not a division with only the fronts multiplied (that gives 18 x 10^6).
lv.stated('l14', 'quiz[3].widget.options[3].why', 'You multiplied the front numbers.', (6 * 3, 4 - (-2)) == (18, 2))
num('l14', 'quiz[4].widget', 12, 9, 13, 6)
lv.claim(10 ** 6 * 10 ** 6 == 10 ** 12, 'l14 quiz[4]: a million million is 10^12')

# ---------- review-3 ----------
num('review', 'items[0].widget', 3 ** (7 - 5), 7 - 5, 3 ** (7 + 5), 1)
lv.expect('review', 'items[1].explain.text', float(D('0.52') * 7890))
lv.claim(14 ** 2 < 200 < 15 ** 2 and 44 < math.sqrt(2000) < 45, 'review items[2]: 14 < sqrt 200 < 15; sqrt 2,000 is between 44 and 45')
lv.expect('review', 'items[2].explain.text', hu(math.sqrt(200), 2))
num('review', 'items[3].widget', 4 + 6 / 2 * 3, 4 + 6 / (2 * 3), (4 + 6) / 2 * 3)
lv.claim(D('7.2e5') / D('8e2') == 900, 'review items[4]: 900 = 9 x 10^2')
# Finding 4: adding the indices gives 0.9 x 10^7 = 9 x 10^6, not the option's 9 x 10^7.
lv.stated('review', 'items[4].widget.options[1].text', '9 \\times 10^7', D('0.9') * D(10) ** 7 == 9 * D(10) ** 7)
num('review', 'items[5].widget', float(1000 * D('1.1') ** 2), 1000 + 2 * 100, float((1000 * D('1.1')) ** 2))
lv.claim(2e6 * 50 == 1e8 and 2.4e6 * 50 == 1.2e8 and 2e6 * 5 == 1e7, 'review items[6]: about 10^8 bytes')
num('review', 'items[7].widget', 3000 * math.isqrt(16), 3000 * 16, 3000 * 16 // 2, 3000)
lv.expect('review', 'items[8].widget.options[3].text', -(2 ** 4))

# ---------- homework-3 ----------
num('homework', 'items[0].widget', 2 ** (10 + 4 - 11), 10 + 4 - 11, 2 ** (10 + 4 + 11), 2 ** 14)
lv.claim((3 * 4) - 5 == 7, 'homework items[1]: x^7')
num('homework', 'items[2].widget', hu(math.sqrt(1500), 1), 1500 / 2, hu(math.sqrt(15), 2), hu(math.sqrt(150), 2))
for v in (D('38.75') ** 2, 38 ** 2, 39 ** 2):
    lv.expect('homework', 'items[2].explain.text', float(v))
lv.claim(D('38.75') ** 2 > 1500, 'homework items[2]: 38.75^2 > 1,500, so the root rounds to 38.7')
num('homework', 'items[3].widget', round(50000 * 1.27 ** 2), 50000 * (1 + 0.02 * 24), 50000 * 1.27, 50000 * 1.27 * 2)
lv.expect('homework', 'items[3].explain.text', round(50000 * 1.02 ** 24))
lv.claim(abs(1.02 ** 12 - 1.27) < 0.005, 'homework items[3]: 1.02^12 is about 1.27')
sec = D('6.5') * 3600
lv.claim(sec == 23400 and abs(sec * 252 / D('1e6') - D('5.9')) < D('0.01'), 'homework items[4]: 5.9 x 10^6 seconds')
num('homework', 'items[4].widget', math.floor(math.log10(float(sec * 252 * 1000))), 6, 10, 8)
for v in ('9.61', '10.24', '9.9856', '10.0489'):
    lv.expect('homework', 'items[5].widget.lines', float(v))
lv.claim(D('3.1') ** 2 == D('9.61') and D('3.2') ** 2 == D('10.24') and D('3.16') ** 2 == D('9.9856') and D('3.17') ** 2 == D('10.0489'), 'homework items[5]: squares')
lv.expect('homework', 'items[5].widget.lines[3].text', hu(D('3.165') ** 2, 3))
lv.expect('homework', 'items[5].explain.text', hu(math.sqrt(10), 4))
m = lv.text('homework', 'items[6].model')
lv.claim(abs(1.02 ** 36 - 2.04) < 0.01 and abs(240 * 1.02 ** 36 - 490) < 1, 'homework items[6]: 240 x 1.02^36 is about 490')
for v in (float(D('1.02') ** 2), hu(1.02 ** 4, 4), hu(1.02 ** 8, 4), hu(1.02 ** 12, 3), hu(1.27 ** 2, 3), round(240 * 2.05), round(240 * 1.72)):
    lv.expect('homework', 'items[6].model', v)
lv.expect('homework', 'items[7].explain.text', hu(D('0.0391') * 5870 / D('19.6'), 2))
lv.expect('homework', 'items[7].widget.options[1].text', 0.04 * 6000 / 20)
lv.expect('homework', 'items[8].explain.text', 2 ** 30)

# ---- Fix pass checks (new values only; a reverted fix fails these) ----
def has(f, path, s):
    lv.claim(s in lv.text(f, path), f'{f} {path} contains "{s}"')


has('l10', 'screens[7].prose', 'For any number $a$ other than 0:')
has('l10', 'screens[6].explain.text', 'multiplying and dividing powers')
lv.claim(D('0.5') * D(10) ** 21 == 5 * D(10) ** 20 and D('4.5') / D('9') == D('0.5'), 'l14 screens[9]: added indices give 0.5 x 10^21 = 5 x 10^20')
has('l14', 'screens[9].widget.options[3].text', '5 \\times 10^{20}')
has('l14', 'screens[9].widget.options[3].why', '$0.5 \\times 10^{21} = 5 \\times 10^{20}$')
lv.claim(D('0.9') * D(10) ** 7 == 9 * D(10) ** 6 and D('7.2') / D('8') == D('0.9'), 'review items[4]: added indices give 0.9 x 10^7 = 9 x 10^6')
has('review', 'items[4].widget.options[1].text', '9 \\times 10^6')
has('review', 'items[4].widget.options[1].why', '$0.9 \\times 10^7 = 9 \\times 10^6$')
lv.claim(D(6) * D(3) == 18 and D('1e4') * D('1e-2') == 100 and 18 * D(100) == D('6e4') * D('3e-2') * 1, 'l14 quiz[3]: (6 x 10^4)(3 x 10^-2) = 18 x 10^2 is the product of the two whole numbers')
has('l14', 'quiz[3].widget.options[3].why', 'You multiplied the two numbers')
lv.claim(D('4.45') ** 2 == D('19.8025') < 20, 'l11 screens[8]: 4.45^2 = 19.8025 < 20, so sqrt(20) rounds to 4.5')
has('l11', 'screens[8].explain.text', '$4.45^2 = 19.8025$')
has('l11', 'screens[8].prose', 'one tenth apart')
lv.claim(20 ** 3 == 8000 and 2 ** 3 == 8 and 10 ** 3 == 1000, 'l11 quiz[4]: 20 x 20 x 20 = 8,000')
has('l11', 'quiz[4].explain.text', '$20 \\times 20 \\times 20 = 8{,}000$')
lv.claim(D('1.02') == 1 + D('0.02'), 'l10 quiz[3]: 1 + 0.02 = 1.02')
has('l10', 'quiz[3].prose', '$1 + 0.02 = 1.02$')
lv.claim(D('0.6') * D('0.4') == D('0.24') and 6 * 4 == 24, 'l13 screens[7]: 6 tenths of 4 tenths is 24 hundredths = 0.24')
has('l13', 'screens[7].explain.text', '24 hundredths')
# homework-3 items[2]: midpoint check
lv.claim(D('38.75') ** 2 == D('1501.5625') > 1500, 'homework items[2]: 38.75^2 = 1,501.5625 > 1,500')
has('homework', 'items[2].explain.text', '1{,}501.5625')
has('homework', 'items[2].feedback.correct', '1{,}501.5625 > 1{,}500')
wd3 = node('homework', 'items[2].widget')
b15 = [x for x in wd3['wrong'] if x['id'] == 'root-15'][0]
lv.claim(abs(3.9 - b15['value']) <= b15['tol']['abs'] and abs(wd3['answer'] - b15['value']) > b15['tol']['abs'] and abs(math.sqrt(15) - 3.9) < 0.05, 'homework items[2]: the root-15 band holds 3.9 and not the key')
# homework-3 items[6]: part (b) with the £7 trillion index
lv.claim(D('1.02') ** 36 > D('2.039') and D('1.02') ** 12 > D('1.268') and round(1.02 ** 12, 2) == 1.27, 'homework items[6]: 1.02^36 = 2.0399; 1.02^12 = 1.268 rounds up to 1.27')
has('homework', 'items[6].model', 'a touch high since 1.268 was rounded up to 1.27')
lv.claim(D('4.9e8') / D('7e12') == D('7e-5') and D('4.9') / D('7') == D('0.7'), 'homework items[6] (b): 4.9 x 10^8 / 7 x 10^12 = 0.7 x 10^-4 = 7 x 10^-5')
lv.claim(D('7e-3') / D('7e-5') == 100 and D('7e12') * D('7e-3') == D('4.9e10') and D('4.9e10') / D('4.9e8') == 100, 'homework items[6] (b): the note is 100 times too big; 7 x 10^-3 of £7 trillion is £49 billion')
for s in ('$4.9 \\times 10^8$', '$7 \\times 10^{12}$', '$0.7 \\times 10^{-4} = 7 \\times 10^{-5}$', '£49 billion', 'seven hundred-thousandths'):
    has('homework', 'items[6].model', s)
has('homework', 'items[6].prompt', '$7 \\times 10^{-3}$ of a £7 trillion stock index')
lv.claim('90 trillion' not in lv.text('homework', 'items[6].model') and '9 \\times 10^{13}' not in lv.text('homework', 'items[6].model'), 'homework items[6]: no trace of the old £90 trillion figures')

lv.check_wrongs()
lv.report()
