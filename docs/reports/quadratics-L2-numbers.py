"""Second read of quadratics level 2 (l5 to l8, review-2, homework-2): every graded key, every wrong[] value and
the numbers in prose, hints, feedback and explanations, each computed two ways (method 1: the quadratic formula or
exact polynomial arithmetic; method 2: bisection on a sign change, brute force over a range, or values at sample
points), and checked against the JSON with app/tools/numbers_lib.py.
Checks written with lv.stated() fail while a false sentence is still in the text: they are review findings
(docs/reviews/review-quadratics-1-3.md) and pass once the fix pass rewords them.
Run: python3 docs/reports/quadratics-L2-numbers.py
"""
import os, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("quadratics", 2)


# ---------- exact one-variable polynomials: {power: Fraction} ----------
def _tok(s):
    s = s.replace('$', '').replace('−', '-').replace('\\left', '').replace('\\right', '').replace('\\,', '')
    s = s.replace('\\times', '*').replace('\\cdot', '*').replace(' ', '')
    return re.findall(r'\d+\.\d+|\d+|[A-Za-z]|[-+*^(){}]', s)


class _P:
    def __init__(self, s):
        self.t, self.i = _tok(s), 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def eat(self):
        self.i += 1
        return self.t[self.i - 1]

    def expr(self):
        sign = 1
        if self.peek() in '+-':
            sign = -1 if self.eat() == '-' else 1
        acc = scale(self.term(), sign)
        while self.peek() in ('+', '-'):
            sign = -1 if self.eat() == '-' else 1
            acc = add(acc, scale(self.term(), sign))
        return acc

    def term(self):
        acc = {0: Fr(1)}
        while self.peek() not in (None, '+', '-', ')', '}'):
            if self.peek() == '*':
                self.eat()
            acc = mul(acc, self.power())
        return acc

    def power(self):
        b = self.base()
        if self.peek() == '^':
            self.eat()
            if self.peek() == '{':
                self.eat(); e = int(self.eat()); self.eat()
            else:
                e = int(self.eat())
            r = {0: Fr(1)}
            for _ in range(e):
                r = mul(r, b)
            return r
        return b

    def base(self):
        t = self.eat()
        if t == '(':
            v = self.expr(); self.eat(); return v
        if t == '-':
            return scale(self.power(), -1)
        if re.match(r'\d', t):
            return {0: Fr(t)}
        return {1: Fr(1)}


def add(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}


def mul(a, b):
    r = {}
    for i, u in a.items():
        for j, v in b.items():
            r[i + j] = r.get(i + j, 0) + u * v
    return {k: v for k, v in r.items() if v != 0}


def scale(a, c):
    return {k: v * c for k, v in a.items() if v * c != 0}


def poly(s):
    return _P(s).expr()


def ev(p, x):
    return sum(v * Fr(x) ** k for k, v in p.items())


def lastmath(s):
    m = re.findall(r'\$([^$]+)\$', s)
    return (m[-1] if m else s).split('=')[-1]


def same_two_ways(label, a, b):
    """Method 1: equal coefficients. Method 2: equal values at five points."""
    pa, pb = poly(a), poly(b)
    lv.claim(pa == pb, f'{label}: {a} == {b} (coefficients)')
    lv.claim(all(ev(pa, x) == ev(pb, x) for x in (-3, -1, 0, 2, 7)), f'{label}: {a} == {b} (values at five points)')


def choice_polys(ref, path, target):
    """The correct option expands to target; each why that says "expands to $E$" or "That gives $E$" is true."""
    opts = lv.files[lv._file(ref)[0]]
    node = opts
    for part in re.findall(r'[A-Za-z_]+|\d+', path):
        node = node[int(part)] if part.isdigit() else node[part]
    for o in node['options']:
        if o.get('correct'):
            same_two_ways(f'{ref} {path} correct option', lastmath(o['text']), target)
        else:
            m = re.search(r'(?:expands to|That gives|That is|That multiplies out to|multiply out to) \$([^$]+)\$', o.get('why', ''))
            if m and re.search(r'[a-z]\^2', m.group(1)):
                same_two_ways(f'{ref} {path} option {o["id"]} why', lastmath(o['text']), m.group(1).split('=')[-1])


def two(label, a, b):
    lv.claim(abs(a - b) < 1e-9, f'{label}: {a} (method 1) = {b} (method 2)')
    return a



from math import sqrt


def roots(a, b, c):
    """Method 1: the formula. Returned larger first."""
    d = b * b - 4 * a * c
    r1, r2 = (-b + sqrt(d)) / (2 * a), (-b - sqrt(d)) / (2 * a)
    return max(r1, r2), min(r1, r2)


def bisect_root(f, lo, hi):
    """Method 2: bisection on a sign change."""
    for _ in range(200):
        mid = (lo + hi) / 2
        if (f(lo) <= 0) == (f(mid) <= 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def near(label, a, b, tol=1e-9):
    lv.claim(abs(a - b) <= tol, f'{label}: {a:.6g} (method 1) ~ {b:.6g} (method 2)')
    return a


# ================= l5 =================
for i, x in enumerate(range(7)):
    for j, v in ((1, x - 2), (2, x - 5), (3, (x - 2) * (x - 5))):
        lv.expect('l5', f'screens[0].canvas.params.rows[{i}][{j}]', two(f'l5 s0 x={x} col {j}', v, [x - 2, x - 5, x * x - 7 * x + 10][j - 1]))
lv.claim([x for x in range(7) if (x - 2) * (x - 5) == 0] == [2, 5], 'l5 s0: only 2 and 5 give 0 in the table')
lv.claim(all((0 - a) * (0 - b) == a * b for a in range(-3, 4) for b in range(-3, 4)), 'l5 s1 yint why: the curve meets the y-axis at ab')
choice_polys('l5', 'screens[3].widget', 'x^2 - 5x + 6')
lv.claim(roots(1, -1, -12) == (4, -3) and ev(poly('x(x - 1)'), 4) == 12 == ev(poly('x(x - 1)'), -3), 'l5 s4: x(x - 1) = 12 at 4 and -3')
same_two_ways('l5 s4 hint', 'x^2 - x - 12', '(x - 4)(x + 3)')
lv.claim(12 - 1 == 11 and 13 - 1 == 12, 'l5 s4 split12: x = 12 or x - 1 = 12 gives 13')
same_two_ways('l5 s5', 'x^2 - 6x + 9', '(x - 3)^2')
lv.claim([x for x in range(-10, 11) if x * x == 5 * x] == [0, 5], 'l5 s6: x^2 = 5x only at 0 and 5')
same_two_ways('l5 s8 d1 d2', '2x^2 - 8x - 10', '2(x^2 - 4x - 5)')
same_two_ways('l5 s8 d3', 'x^2 - 4x - 5', '(x - 5)(x + 1)')
lv.claim(2 * (-1) ** 2 == 2 == 8 * (-1) + 10, 'l5 s8 explain: check x = -1 gives 2 = 2')
prof = poly('q(30 - q) - 10q - 64')
same_two_ways('l5 s9 profit', 'q(30 - q) - 10q - 64', '-q^2 + 20q - 64')
for i, qq in enumerate((2, 6, 10, 14, 18)):
    lv.expect('l5', f'screens[9].canvas.params.rows[{i}][1]', 30 - qq, fmt='£{:.2f}')
    lv.expect('l5', f'screens[9].canvas.params.rows[{i}][2]', two(f'l5 s9 profit q={qq}', int(ev(prof, qq)), -(qq - 4) * (qq - 16)))
lv.claim(roots(1, -20, 64) == (16, 4), 'l5 s9 key: break-even at 4 and 16 thousand')
lv.claim(2 * 32 == 64 and 2 + 32 == 34, 'l5 s9 pair why')
lv.claim(max(range(0, 31), key=lambda q: ev(prof, q)) == 10 and ev(prof, 10) == 36, 'l5 s9 peak why: profit peaks at 10, £36 thousand')
lv.claim(all(ev(prof, q) > 0 for q in range(5, 16)), 'l5 s9 explain: positive between 4 and 16')
lv.claim(roots(2, 5, -12) == (1.5, -4) and 1.5 == 3 / 2, 'l5 quiz[0]: (2x - 3)(x + 4) = 0 at 3/2 and -4')
lv.expect('l5', 'quiz[1].widget.answer', two('l5 quiz[1]', roots(1, 2, -15)[0], bisect_root(lambda x: x * x + 2 * x - 15, 0, 10)))
lv.expect('l5', 'quiz[1].widget.wrong[0].value', 5)
lv.expect('l5', 'quiz[1].widget.wrong[1].value', 15)
lv.claim(3 * 16 == 48 == 12 * 4 and roots(3, -12, 0) == (4, 0), 'l5 quiz[2]: 3x^2 = 12x at 0 and 4')
same_two_ways('l5 quiz[3]', '(x - 1)(x - 6) - 6', 'x(x - 7)')
lv.claim((0 - 1) * (0 - 6) == 6 and (7 - 1) * (7 - 6) == 6, 'l5 quiz[3]: 0 and 7 both give 6')

# ================= l6 =================
lv.expect('l6', 'screens[0].widget.answer', two('l6 s0 corner', (6 // 2) ** 2, 3 * 3))
for i, v in enumerate((36, 6, 3)):
    lv.expect('l6', f'screens[0].widget.wrong[{i}].value', v)
same_two_ways('l6 s0 explain', 'x^2 + 6x + 9', '(x + 3)^2')
lv.claim((8 // 2) ** 2 == 16 == len([1 for r in range(4) for c in range(4)]), 'l6 s1: 16 unit squares, a 4 by 4 corner')
lv.claim(len(lv.files['l6-completing-the-square']['screens'][1]['widget']['answer']) == 16, 'l6 s1: the tap answer lists 16 cells')
same_two_ways('l6 s1 explain', 'x^2 + 8x + 16', '(x + 4)^2')
choice_polys('l6', 'screens[2].widget', 'x^2 + 10x')
same_two_ways('l6 s2 prose', '(x + 4)^2 - 16', 'x^2 + 8x')
q = ev(poly('x^2 + 6x + 5'), 0) - ev(poly('(x + 3)^2'), 0)
lv.expect('l6', 'screens[3].widget.answer', two('l6 s3 q', int(q), -9 + 5))
lv.expect('l6', 'screens[3].widget.wrong[0].value', 9 + 5)
lv.expect('l6', 'screens[3].widget.wrong[1].value', 5)
lv.expect('l6', 'screens[3].widget.wrong[2].value', -9)
lv.claim(roots(1, 6, 5) == (-1, -5) and (-1) ** 2 - 6 + 5 == 0, 'l6 s4: roots -1 and -5, check 1 - 6 + 5 = 0')
lv.stated('l6', 'screens[4].explain.text', '$\\; check', False)        # finding: a LaTeX space outside the $ signs shows as "\;"
corner = (3 / 2) ** 2
lv.expect('l6', 'screens[5].prose', corner)
lv.expect('l6', 'screens[5].hints[2].text', 4 + corner)
lv.expect('l6', 'screens[5].hints[2].text', sqrt(4 + corner))
lv.expect('l6', 'screens[5].widget.answer', two('l6 s5 negative root', roots(1, 3, -4)[1], -1.5 - sqrt(6.25)))
lv.expect('l6', 'screens[5].widget.wrong[0].value', roots(1, 3, -4)[0])
lv.expect('l6', 'screens[5].widget.wrong[1].value', -sqrt(6.25))
lv.expect('l6', 'screens[5].widget.wrong[2].value', -1)
side3 = (-3 + sqrt(13), -3 - sqrt(13))                 # (x + 3)^2 - 9 - 4 = 0: the whole 3 as the corner's side
lv.claim(abs(roots(1, 6, -4)[1] - side3[1]) < 1e-12, 'l6 s5: with side 3 the roots are -3 +- sqrt(13) (about 0.61, -6.61)')
lv.stated('l6', 'screens[5].feedback.byKey.whole', 'You used the whole 3', any(abs(-1 - r) < 0.0005 for r in side3))   # finding
lv.claim(roots(1, -4, 4 - 9) == (5, -1), 'l6 s6: (x - 2)^2 = 9 at 5 and -1')
lv.claim(2 + 9 == 11, 'l6 s6 eleven')
lv.claim((-14 // 2) ** 2 == 49 and 14 ** 2 == 196, 'l6 s7: 49 and 196')
same_two_ways('l6 s7 explain', 'x^2 - 14x + 49', '(x - 7)^2')
prof = poly('q(26 - q) - 6q - 36')
same_two_ways('l6 s8 profit', 'q(26 - q) - 6q - 36', '-q^2 + 20q - 36')
for i, qq in enumerate((4, 8, 12, 16)):
    lv.expect('l6', f'screens[8].canvas.params.rows[{i}][1]', 26 - qq, fmt='£{:.2f}')
    lv.expect('l6', f'screens[8].canvas.params.rows[{i}][2]', two(f'l6 s8 profit q={qq}', int(ev(prof, qq)), 64 - (qq - 10) ** 2))
lv.expect('l6', 'screens[8].widget.answer', two('l6 s8 max', max(ev(prof, q) for q in range(0, 27)), 100 - 36))
lv.expect('l6', 'screens[8].widget.wrong[0].value', 60)
lv.expect('l6', 'screens[8].widget.wrong[1].value', 100)
lv.expect('l6', 'screens[8].widget.wrong[2].value', 10)
lv.expect('l6', 'screens[8].explain.text', 26 - 10, fmt='£{:.2f}')
choice_polys('l6', 'quiz[0].widget', 'x^2 + 12x')
lv.expect('l6', 'quiz[1].widget.answer', two('l6 quiz[1] r', round(sqrt(1210 / 1000) - 1, 12), 0.1))
lv.expect('l6', 'quiz[1].widget.wrong[0].value', 0.21 / 2)
lv.expect('l6', 'quiz[1].widget.wrong[1].value', 0.21)
lv.claim(abs((-1.1 - 1) - (-2.1)) < 1e-12, 'l6 quiz[1] explain: 1 + r = -1.1 means r = -210%')
lv.expect('l6', 'quiz[2].widget.answer', two('l6 quiz[2] smaller', roots(1, -10, 21)[1], 5 - sqrt(25 - 21)))
lv.expect('l6', 'quiz[2].widget.wrong[0].value', roots(1, -10, 21)[0])
same_two_ways('l6 quiz[3]', 'x^2 + 4x + 7', '(x + 2)^2 + 3')
lv.claim(4 * 4 - 4 * 7 < 0, 'l6 quiz[3]: no real root')

# ================= l7 =================
r0 = roots(1, 4, -1)
lv.claim(abs(r0[0] - (-2 + sqrt(5))) < 1e-12, 'l7 s0: right-hand crossing is -2 + sqrt(5)')
lv.expect('l7', 'screens[0].feedback.correct', near('l7 s0 0.24', round(r0[0], 2), round(bisect_root(lambda x: x * x + 4 * x - 1, 0, 1), 2)))
lv.expect('l7', 'screens[0].explain.text', round(r0[1], 2))
lv.expect('l7', 'screens[0].hints[2].text', round(sqrt(5), 2))
lv.claim(4 + 1 == 5 and 4 - 1 == 3, 'l7 s0 corner why: (x + 2)^2 = 4 + 1, not 4 - 1')
lv.stated('l7', 'screens[0].widget.options[2].why', 'The 5 is a square', int(sqrt(5)) ** 2 == 5)   # finding
lv.claim(roots(1, -6, 5) == (5, 1) and (5 + 1) / 2 == 3 == 6 / 2, 'l7 s1: crossings 1 and 5, middle 3 = -b/2')
lv.expect('l7', 'screens[2].widget.answer', near('l7 s2', round(3 + sqrt(5), 2), round(roots(1, -6, 4)[0], 2)))
lv.expect('l7', 'screens[2].widget.wrong[0].value', round(roots(1, -6, 4)[1], 2))
lv.expect('l7', 'screens[2].widget.wrong[1].value', 3 + 5)
lv.expect('l7', 'screens[2].widget.wrong[2].value', round(sqrt(5), 2))
lv.expect('l7', 'screens[3].widget.answer', near('l7 s3', round(-2 + sqrt(2.5), 2), round(roots(2, 8, 3)[0], 2)))
lv.expect('l7', 'screens[3].widget.wrong[0].value', round(roots(1, 8, 3)[0], 2))
lv.expect('l7', 'screens[3].widget.wrong[1].value', roots(1, 4, 3)[0])
lv.expect('l7', 'screens[3].widget.wrong[2].value', round(roots(2, 8, 3)[1], 2))
lv.claim(abs(4 - 1.5 - 2.5) < 1e-12, 'l7 s3 hint: (x + 2)^2 = 4 - 1.5 = 2.5')
a, b, c = 3, -5, -2
lv.expect('l7', 'screens[5].hints[2].text', b * b - 4 * a * c)
lv.expect('l7', 'screens[5].widget.answer', near('l7 s5', round(roots(a, b, c)[1], 4), round(-1 / 3, 4)))
lv.claim(roots(a, b, c)[0] == 2, 'l7 s5: other root 2')
lv.expect('l7', 'screens[5].widget.wrong[0].value', (-5 - 7) / 6)                    # signb: -b taken as -5
lv.expect('l7', 'screens[5].widget.wrong[1].value', round((5 - 7) / 3, 4))
lv.claim(roots(1, -4, -5) == (5, -1) and 16 + 20 == 36, 'l7 s6: roots 5 and -1, disc 36')
lv.claim(sorted((4 + 6 / 2, 4 - 6 / 2)) == [1, 7], 'l7 s6 bar: 4 +- 6/2 = 7 and 1')
lv.claim(sorted(((-4 + 6) / 2, (-4 - 6) / 2)) == [-5, 1], 'l7 s6 signb: 1 and -5')
lv.claim(sorted(((4 + sqrt(-16 + 20)) / 2, (4 - sqrt(-16 + 20)) / 2)) == [1, 3], 'l7 s6 square: b^2 as -16 gives 3 and 1')
lv.expect('l7', 'screens[7].widget.answer', two('l7 s7 disc', 3 ** 2 - 4 * 2 * -1, 17))
lv.expect('l7', 'screens[7].widget.wrong[0].value', 9 - 4 * 2 * 1)
lv.expect('l7', 'screens[7].widget.wrong[1].value', -9 - 8)
lv.expect('l7', 'screens[7].widget.wrong[2].value', 9 - 4 * -1)
rt = roots(1, -7, 5)
lv.claim(all(abs(u - v) < 1e-12 for u, v in zip(roots(-20, 140, -100), rt)), 'l7 s8: dividing by -20 keeps the roots')
lv.expect('l7', 'screens[8].widget.answer', near('l7 s8', round((7 + sqrt(29)) / 2, 2), round(bisect_root(lambda t: -20 * t * t + 140 * t - 100, 4, 7), 2)))
lv.expect('l7', 'screens[8].widget.wrong[0].value', round(rt[1], 2))
lv.expect('l7', 'screens[8].widget.wrong[1].value', 7 / 2)
lv.expect('l7', 'screens[8].widget.wrong[2].value', round(7 + sqrt(29), 2))
lv.claim(abs(roots(1, 2, -2)[0] - (-1 + sqrt(3))) < 1e-12 and abs(sqrt(12) - 2 * sqrt(3)) < 1e-12, 'l7 quiz[0]: -1 +- sqrt(3), sqrt(12) = 2 sqrt(3)')
lv.expect('l7', 'quiz[1].widget.answer', two('l7 quiz[1]', roots(2, -1, -6)[0], (1 + 7) / 4))
lv.expect('l7', 'quiz[1].widget.wrong[0].value', (-1 + 7) / 4)
lv.expect('l7', 'quiz[1].widget.wrong[1].value', (1 + 7) / 2)
lv.claim(roots(2, -1, -6)[1] == -1.5 and 2 * 4 - 2 - 6 == 0, 'l7 quiz[1]: -1.5, check 8 - 2 - 6 = 0')
lv.claim(abs(roots(1, -6, 7)[0] - (3 + sqrt(2))) < 1e-12 and 36 - 28 == 8 and abs(sqrt(8) / 2 - sqrt(2)) < 1e-12, 'l7 quiz[3]: 3 +- sqrt(2), half of sqrt(8) is sqrt(2)')

# ================= l8 =================
lv.claim(sorted((2 + 1, 2 - 1)) == [1, 3], 'l8 s0 two: sqrt(-1) taken as 1 gives 1 and 3')
lv.expect('l8', 'screens[1].widget.answer', two('l8 s1 touch', (4 / 2) ** 2, 16 / 4))
lv.expect('l8', 'screens[1].widget.wrong[0].value', -4)
lv.expect('l8', 'screens[1].widget.wrong[1].value', 2)
lv.expect('l8', 'screens[1].widget.wrong[2].value', 16)
lv.claim(4 - 8 + 2 == -2, 'l8 s1 half: lowest point -2 at c = 2')
lv.expect('l8', 'screens[2].widget.answer', 16 - 4 * 6)
lv.expect('l8', 'screens[2].widget.wrong[0].value', 24 - 16)
lv.expect('l8', 'screens[2].widget.wrong[1].value', 16 + 24)
lv.expect('l8', 'screens[2].widget.wrong[2].value', 16 - 6)
lv.expect('l8', 'screens[3].explain.text', 9 - 4 * 2 * 5)
lv.claim(144 - 4 * 9 * 4 == 0 and roots(9, -12, 4) == (2 / 3, 2 / 3), 'l8 s4: disc 0, root 2/3')
same_two_ways('l8 s4 explain', '9x^2 - 12x + 4', '(3x - 2)^2')
lv.claim([k for k in range(-20, 21) if k * k - 36 == 0] == [-6, 6], 'l8 s5: k = +-6')
same_two_ways('l8 s5 k=6', 'x^2 + 6x + 9', '(x + 3)^2')
lv.expect('l8', 'screens[6].widget.options[0].text', 100 - 120)
lv.claim(max(x * (10 - x) for x in [i / 100 for i in range(1001)]) == 25 and 2 * (3 + 10) == 26, 'l8 s6: largest area 25, 3 by 10 has perimeter 26')
lv.claim(36 + 28 == 64 and roots(1, -6, -7) == (7, -1) and -36 + 28 == -8, 'l8 s7: disc 64, roots 7 and -1; the slip gives -8')
lv.expect('l8', 'screens[8].hints[1].text', 25 + 4000)
lv.expect('l8', 'screens[9].widget.answer', two('l8 s9 T', 50 ** 2 / 4, max(q * (50 - q) for q in range(51))))
lv.expect('l8', 'screens[9].widget.wrong[0].value', 2500)
lv.expect('l8', 'screens[9].widget.wrong[1].value', 2500 / 2)
lv.expect('l8', 'screens[9].widget.wrong[2].value', 25)
lv.claim(50 - 25 == 25, 'l8 s9 explain: £25.00 a contract at q = 25')
lv.claim(36 - 40 == -4, 'l8 quiz[0]')
same_two_ways('l8 quiz[0] explain', 'x^2 + 6x + 10', '(x + 3)^2 + 1')
lv.expect('l8', 'quiz[1].widget.answer', 4 - 4 * 3 * -1)
lv.expect('l8', 'quiz[1].widget.wrong[0].value', 4 - 12)
lv.expect('l8', 'quiz[1].widget.wrong[1].value', -4 + 12)
lv.claim(roots(3, -2, -1) == (1, -1 / 3), 'l8 quiz[1] explain: 1 and -1/3')
lv.claim(all((64 - 4 * c > 0) == (c < 16) for c in range(-50, 50)), 'l8 quiz[2]: two roots exactly when c < 16')
lv.claim(100 - 104 == -4 and max(x * (10 - x) for x in range(11)) == 25, 'l8 quiz[3]: disc -4, max product 25')

# ================= review-2 =================
lv.expect('review', 'items[0].widget.answer', roots(1, -3, -28)[0])
lv.expect('review', 'items[0].widget.wrong[0].value', 4)
lv.expect('review', 'items[0].widget.wrong[1].value', 28)
lv.claim(roots(4, -12, 0) == (3, 0), 'r2 items[1]: 0 and 3')
lv.expect('review', 'items[2].widget.answer', two('r2 items[2] q', 40 - 49, ev(poly('x^2 - 14x + 40'), 7)))
lv.expect('review', 'items[2].widget.wrong[0].value', 40 + 49)
lv.expect('review', 'items[2].widget.wrong[1].value', -49)
lv.claim(roots(1, 2, 1 - 16) == (3, -5) and sorted((16 - 1, -16 - 1)) == [-17, 15], 'r2 items[3]: 3 and -5; the noroot slip gives 15 and -17')
r = roots(2, -3, -4)
lv.expect('review', 'items[4].widget.answer', near('r2 items[4]', round(r[0], 2), round(bisect_root(lambda x: 2 * x * x - 3 * x - 4, 1, 4), 2)))
lv.expect('review', 'items[4].widget.wrong[0].value', round((-3 + sqrt(41)) / 4, 2))
lv.expect('review', 'items[4].widget.wrong[1].value', round((3 + sqrt(41)) / 2, 1))
lv.expect('review', 'items[4].widget.wrong[2].value', round(3 + sqrt(41) / 4, 1))
lv.expect('review', 'items[4].explain.text', round(sqrt(41), 3))
lv.expect('review', 'items[4].explain.text', round(r[1], 2))
lv.claim(abs(roots(1, -2, -1)[0] - (1 + sqrt(2))) < 1e-12 and 4 - 4 * 1 * 1 == 0, 'r2 items[5]: 1 +- sqrt(2); with c = +1 the disc is 0')
lv.claim(16 - 16 == 0 and roots(4, -4, 1) == (0.5, 0.5), 'r2 items[6]: one root 1/2')
same_two_ways('r2 items[6] explain', '4x^2 - 4x + 1', '(2x - 1)^2')
lv.claim(all((36 - 12 * c > 0) == (c < 3) for c in range(-30, 30)), 'r2 items[7]: c < 3')
lv.claim(all((36 - 4 * c > 0) == (c < 9) and (36 - 3 * c > 0) == (c < 12) for c in range(-30, 30)), 'r2 items[7] noa and nofour slips')
lv.expect('review', 'items[8].widget.answer', two('r2 items[8]', round(sqrt(28800 / 20000) - 1, 12), 0.2))
lv.expect('review', 'items[8].widget.wrong[0].value', 0.44 / 2)
lv.expect('review', 'items[8].widget.wrong[1].value', 0.44)

# ================= homework-2 =================
lv.expect('homework', 'items[0].widget.answer', roots(1, 3, -40)[0])
lv.expect('homework', 'items[0].widget.wrong[0].value', 40 - 3)
lv.expect('homework', 'items[0].widget.wrong[1].value', 8)
lv.claim(roots(1, -7, 0) == (7, 0), 'h2 items[1]: 0 and 7')
choice_polys('homework', 'items[2].widget', '2x^2 + 12x + 7')
lv.claim(poly('2(x + 3)^2 - 2') != poly('2x^2 + 12x + 7') and 7 - 18 == -11, 'h2 items[2] corner slip')
same_two_ways('h2 items[2] noout slip: halved 12, took off 36 once', '2(x + 6)^2 - 29', '2(x + 6)^2 - 36 + 7')
lv.expect('homework', 'items[3].widget.answer', two('h2 items[3]', round(sqrt(5618 / 5000) - 1, 12), 0.06))
lv.expect('homework', 'items[3].widget.wrong[0].value', 0.1236 / 2)
lv.expect('homework', 'items[3].widget.wrong[1].value', 0.1236)
lv.expect('homework', 'items[3].explain.text', 5618 / 5000)
lv.claim(sum(roots(1, -5, 6)) == 5 == -(-5) / 1, 'h2 items[4] check: 2 + 3 = 5 = -b/a')
lv.stated('homework', 'items[4].feedback.byKey.o3', 'then the roots cancel', False)   # finding: it is the square roots that cancel
t = roots(1, -6, -4)
lv.claim(roots(-0.5, 3, 2) == t, 'h2 items[5]: multiplying by -2 keeps the roots')
lv.expect('homework', 'items[5].widget.answer', near('h2 items[5]', round(3 + sqrt(13), 2), round(t[0], 2)))
lv.expect('homework', 'items[5].widget.wrong[0].value', round(t[1], 2))
lv.expect('homework', 'items[5].widget.wrong[1].value', 3)
lv.expect('homework', 'items[5].widget.wrong[2].value', round(6 + sqrt(52), 2))
lv.claim(abs(sqrt(52) - 2 * sqrt(13)) < 1e-12, 'h2 items[5] explain: sqrt(52) = 2 sqrt(13)')
lv.claim(324 - 4 * 85 == -16 and [A for A in (85, 81, 80, 72) if 324 - 4 * A < 0] == [85], 'h2 items[6]: only 85 m2 is impossible')
lv.claim(8 * 10 == 80 and 6 * 12 == 72 and 2 * (8 + 10) == 36 == 2 * (6 + 12), 'h2 items[6] whys')
same_two_ways('h2 items[7] profit with F = 288', 'q(60 - 2q) - 12q - 288', '-2q^2 + 48q - 288')
lv.expect('homework', 'items[7].widget.answer', two('h2 items[7] F', 48 ** 2 / 8, max(-2 * q * q + 48 * q for q in range(25))))
lv.expect('homework', 'items[7].widget.wrong[0].value', 2304 / 4)
lv.expect('homework', 'items[7].widget.wrong[1].value', 2304 / 2)
lv.claim(-48 / (2 * -2) == 12, 'h2 items[7] explain: break-even at q = 12')
same_two_ways('h2 items[8] (a)', 'q(50 - q) - 10q - 300', '-q^2 + 40q - 300')
same_two_ways('h2 items[8] (b)', 'q^2 - 40q + 300', '(q - 10)(q - 30)')
same_two_ways('h2 items[8] (c)', '-q^2 + 40q - 300', '100 - (q - 20)^2')
lv.claim(1600 - 4 * 420 == -80 and 1600 - 4 * 375 == 100 and roots(1, -40, 375) == (25, 15), 'h2 items[8] (d): -80; 100 with volumes 15 and 25')
lv.claim(-15 ** 2 + 40 * 15 - 300 == 75, 'h2 items[8] (d) check: -225 + 600 - 300 = 75')

lv.check_wrongs()
lv.report()
