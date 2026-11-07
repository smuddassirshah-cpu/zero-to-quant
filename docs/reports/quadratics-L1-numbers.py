"""Second read of quadratics level 1 (l1 to l4, review-1, homework-1): every graded key, every wrong[] value and
the numbers in prose, hints, feedback and explanations, each computed two ways (method 1: expand with exact
polynomial arithmetic; method 2: evaluate both sides at sample points or a direct formula), and checked against the
JSON with app/tools/numbers_lib.py. Every choice option written as a polynomial is expanded and compared with the
target (the correct option) or with the expansion its why claims ("That expands to ...").
Checks written with lv.stated() fail while a false sentence is still in the text: they are review findings
(docs/reviews/review-quadratics-1-3.md) and pass once the fix pass rewords them.
Run: python3 docs/reports/quadratics-L1-numbers.py
"""
import os, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("quadratics", 1)


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


# ================= l1 =================
x = 10
area = two('l1 s0 area', (x + 3) * (x + 2), x * x + 3 * x + 2 * x + 6)
lv.expect('l1', 'screens[0].widget.answer', area)
lv.expect('l1', 'screens[0].explain.text', 156)
lv.expect('l1', 'screens[0].widget.wrong[0].value', two('firsts-lasts', x * x + 3 * 2, 156 - 30 - 20))
lv.expect('l1', 'screens[0].widget.wrong[1].value', two('added', (x + 3) + (x + 2), 25))
lv.expect('l1', 'screens[0].widget.wrong[2].value', two("one-strip (no bottom strip)", 156 - 2 * x, x * x + 3 * x + 6))
lv.expect('l1', 'screens[0].widget.wrong[3].value', two('other-strip (no right strip)', 156 - 3 * x, (x + 2) * x + 6))
for n in (100, 30, 20, 6):
    lv.expect('l1', 'screens[0].explain.canvas.labels', n)
same_two_ways('l1 s1 explain', '(x + 3)(x + 2)', 'x^2 + 3x + 2x + 6')
same_two_ways('l1 s2 explain', '(x + 4)(x + 5)', 'x^2 + 9x + 20')
choice_polys('l1', 'screens[3].widget', '(x + 6)(x + 2)')
lv.claim(poly('x^2 + 12x + 8') == {2: 1, 1: 6 * 2, 0: 6 + 2}, 'l1 s3 swapped: strips multiply, corner adds')
lv.claim(poly('x^2 + 8x + 8') == {2: 1, 1: 8, 0: 6 + 2}, 'l1 s3 corner-added: corner 6 + 2')
b = poly('(x + 5)(x - 2)')[1]
lv.expect('l1', 'screens[4].widget.answer', two('l1 s4 b', b, 5 - 2))
lv.expect('l1', 'screens[4].widget.wrong[0].value', 5 + 2)
lv.expect('l1', 'screens[4].widget.wrong[1].value', -5 + 2)
lv.expect('l1', 'screens[4].widget.wrong[2].value', -5 - 2)
same_two_ways('l1 s4 explain', '(x + 5)(x - 2)', 'x^2 + 3x - 10')
choice_polys('l1', 'screens[5].widget', '(x - 3)(x - 5)')
choice_polys('l1', 'screens[6].widget', '(x + 3)^2')
lv.claim(ev(poly('(x + 3)^2'), 1) == 16 and ev(poly('x^2 + 9'), 1) == 10, 'l1 s6 hint: (1 + 3)^2 = 16, 1 + 9 = 10')
same_two_ways('l1 s7 derive with a = 2, b = 7', '(x + 2)(x + 7)', 'x^2 + 9x + 14')
P, r = 2000, 0.04
lv.expect('l1', 'screens[8].widget.answer', two('l1 s8 r^2 piece', P * r * r, P * (1 + r) ** 2 - P - 2 * P * r))
lv.expect('l1', 'screens[8].widget.wrong[0].value', two('whole gain', P * (1 + r) ** 2 - P, 163.2))
lv.expect('l1', 'screens[8].widget.wrong[1].value', P * r)
lv.expect('l1', 'screens[8].widget.wrong[2].value', 2 * P * r)
lv.expect('l1', 'screens[8].widget.wrong[3].value', r * r)
lv.expect('l1', 'screens[8].explain.text', two('final value', P * (1 + r) ** 2, P + 80 + 80 + 3.2), fmt='{:.2f}')
choice_polys('l1', 'quiz[0].widget', '(x + 7)(x + 3)')
choice_polys('l1', 'quiz[1].widget', '(x + 4)(x - 4)')
choice_polys('l1', 'quiz[3].widget', '(2x + 1)(x + 3)')
lv.claim(poly('2x^2 + 4x + 3')[1] == 3 + 1, 'l1 quiz[3] one-x: 2x*3 taken as 3x, plus x')
# quiz[2]: (r - m)^2 with m a number: squaring each term of r - m gives r^2 + m^2, not r^2 - m^2 (finding 1)
m_ = 3
each_sq = lambda rr: rr ** 2 + (-m_) ** 2
lv.claim(all((rr - m_) ** 2 == rr * rr - 2 * m_ * rr + m_ * m_ for rr in range(-3, 4)), 'l1 quiz[2] key r^2 - 2mr + m^2')
lv.stated('l1', 'quiz[2].widget.options[1].why', 'You squared each term.', all(each_sq(rr) == rr * rr - m_ * m_ for rr in range(-3, 4)))

# ================= l2 =================
pairs = lambda c: [(p, c // p) for p in range(1, abs(c) + 1) if c % p == 0]
fit = lambda b, c: [(p, c // p) for p in range(-abs(c), abs(c) + 1) if p and c % p == 0 and p + c // p == b and p <= c // p]
lv.claim(fit(7, 12) == [(3, 4)], 'l2 s0: only 3 and 4 have product 12 and sum 7')
for i, (p, q) in enumerate([(1, 24), (2, 12), (3, 8), (4, 6)]):
    lv.expect('l2', f'screens[1].canvas.params.rows[{i}][2]', two(f'l2 s1 sum {p}+{q}', p + q, sum((p, q))))
lv.claim([p for p, q in pairs(24) if p <= q and p + q == 10] == [4], 'l2 s1: only 4 and 6 add to 10')
for i, (p, q) in enumerate([(1, 18), (2, 9), (3, 6)]):
    lv.expect('l2', f'screens[2].widget.rows[{i}][2].answer', p + q)
for i, (p, q) in enumerate([(1, -15), (-1, 15), (3, -5), (-3, 5)]):
    lv.expect('l2', f'screens[3].explain.canvas.values.r{i}c2', p + q)
choice_polys('l2', 'screens[3].widget', 'x^2 + 2x - 15')
for i, (p, q) in enumerate([(1, 20), (2, 10), (4, 5), (-1, -20), (-2, -10), (-4, -5)]):
    lv.expect('l2', f'screens[4].explain.canvas.values.r{i}c2', p + q)
same_two_ways('l2 s4 key', '(x - 4)(x - 5)', 'x^2 - 9x + 20')
choice_polys('l2', 'screens[5].widget', 'x^2 + 10x + 25')
choice_polys('l2', 'screens[6].widget', 'x^2 - 2x - 15')
same_two_ways('l2 s6 Priya', '(x - 3)(x + 5)', 'x^2 + 2x - 15')
lv.claim(fit(-1, -12) == [(-4, 3)], 'l2 s7: 3 and -4 is the only pair for product -12, sum -1')
same_two_ways('l2 s7 explain', '(x + 3)(x - 4)', 'x^2 - x - 12')
same_two_ways('l2 s8 profit', 'q(16 - q) - 4q - 27', '-(q^2 - 12q + 27)')
choice_polys('l2', 'screens[8].widget', 'q^2 - 12q + 27')
prof = poly('q(16 - q) - 4q - 27')
for i, qq in enumerate((2, 6, 10)):
    v = ev(prof, qq)
    lv.expect('l2', f'screens[8].canvas.params.rows[{i}][1]', 16 - qq, fmt='£{:.2f}')
    lv.expect('l2', f'screens[8].canvas.params.rows[{i}][2]', two(f'l2 s8 profit q={qq}', float(v), float(-(qq - 3) * (qq - 9))))
lv.claim(all(ev(prof, qq) > 0 for qq in range(4, 9)) and ev(prof, 3) == 0 == ev(prof, 9), 'l2 s8: zero at 3 and 9, positive between')
choice_polys('l2', 'quiz[0].widget', 'x^2 + 8x + 15')
choice_polys('l2', 'quiz[1].widget', 'x^2 - x - 20')
choice_polys('l2', 'quiz[2].widget', 'x^2 - 12x + 36')
lv.expect('l2', 'quiz[3].widget.answer', two('l2 quiz[3] k', 3 + 24 // 3, poly('(x + 3)(x + 8)')[1]))
lv.expect('l2', 'quiz[3].widget.wrong[0].value', 24 // 3)
lv.expect('l2', 'quiz[3].widget.wrong[1].value', 3 + 24)
# quiz[1] explain (finding 2): of -5 and 4 the larger number is 4, which is positive
lv.stated('l2', 'quiz[1].explain.text', 'the larger number is negative', max(-5, 4) < 0)

# ================= l3 =================
choice_polys('l3', 'screens[0].widget', '(2x + 3)(x + 1)')
lv.claim(3 + 2 == 5 and 3 * 2 == 2 * 3, 'l3 s1: 3 and 2 add to 5 and multiply to 6 = 2 x 3')
for i, (p, q) in enumerate([(1, 24), (2, 12), (3, 8), (4, 6)]):
    lv.expect('l3', f'screens[2].explain.canvas.values.r{i}c2', p + q)
lv.claim([(p, q) for p, q in pairs(24) if p <= q and p + q == 10] == [(4, 6)], 'l3 s2: 4 and 6 split 10x for ac = 24')
lv.claim(2 * 8 == 16 and 2 + 8 == 10 and 3 * 8 == 24 and 3 + 8 == 11 and 2 * 4 == 8, 'l3 s2 distractor products and sums')
same_two_ways('l3 s3 split', '3x^2 + 6x + 4x + 8', '3x(x + 2) + 4(x + 2)')
same_two_ways('l3 s3 shared', '3x(x + 2) + 4(x + 2)', '(3x + 4)(x + 2)')
for i, (p, q) in enumerate([(1, -6), (-1, 6), (2, -3), (-2, 3)]):
    lv.expect('l3', f'screens[4].explain.canvas.values.r{i}c2', p + q)
choice_polys('l3', 'screens[4].widget', '3x^2 - 5x - 2')
same_two_ways('l3 s4 split-as-brackets', '(x + 1)(x - 6)', 'x^2 - 5x - 6')
choice_polys('l3', 'screens[5].widget', '2x^2 + 10x + 12')
same_two_ways('l3 s5 not-full', '(2x + 4)(x + 3)', '2x^2 + 10x + 12')
lv.claim(1 * 6 == 6 and 1 + 6 == 7, 'l3 s5 wrong-pair 1 and 6')
choice_polys('l3', 'screens[6].widget', '2x^2 + 7x + 3')
same_two_ways('l3 s6 Ali', '(x + 1)(x + 6)', 'x^2 + 7x + 6')
lv.claim(all(ev(poly('(px+q)(rx+s)'.replace('p', '2').replace('q', '3').replace('r', '5').replace('s', '7')), t) ==
             ev(poly('10x^2 + 29x + 21'), t) for t in (-2, 0, 3)) and (2 * 7) * (3 * 5) == (2 * 5) * (3 * 7), 'l3 s7: ps*qr = pr*qs (p,q,r,s = 2,3,5,7)')
same_two_ways('l3 s8 profit', 'q(30 - 2q) - 6q - 40', '-2q^2 + 24q - 40')
choice_polys('l3', 'screens[8].widget', '-2q^2 + 24q - 40')
same_two_ways('l3 s8 not-full', '(-2q + 4)(q - 10)', '-2q^2 + 24q - 40')
prof = poly('-2q^2 + 24q - 40')
for i, qq in enumerate((1, 6, 11)):
    lv.expect('l3', f'screens[8].canvas.params.rows[{i}][1]', 30 - 2 * qq, fmt='£{:.2f}')
    lv.expect('l3', f'screens[8].canvas.params.rows[{i}][2]', two(f'l3 s8 profit q={qq}', float(ev(prof, qq)), -2 * (qq - 2) * (qq - 10)))
lv.expect('l3', 'screens[8].explain.text', -2 * (6 - 2) * (6 - 10), fmt='£{:.2f}')
choice_polys('l3', 'quiz[0].widget', '2x^2 + 11x + 5')
lv.expect('l3', 'quiz[1].widget.answer', two('l3 quiz[1] ac', 4 * -3, -12))
lv.expect('l3', 'quiz[1].widget.wrong[0].value', -3)
lv.expect('l3', 'quiz[1].widget.wrong[1].value', 12)
same_two_ways('l3 quiz[1] explain', '(2x + 3)(2x - 1)', '4x^2 + 4x - 3')
same_two_ways('l3 quiz[2] key', '3x(2x + 3)', '6x^2 + 9x')
choice_polys('l3', 'quiz[3].widget', '3x^2 + x - 2')
same_two_ways('l3 quiz[3] split-as-brackets', '(x + 3)(x - 2)', 'x^2 + x - 6')

# ================= l4 =================
x = 10
lv.expect('l4', 'screens[0].widget.answer', two('l4 s0 L-shape', x * x - 9, (x - 3) ** 2 + 2 * 3 * (x - 3)))
lv.expect('l4', 'screens[0].widget.wrong[0].value', x * x - 3)
lv.expect('l4', 'screens[0].widget.wrong[1].value', (x - 3) ** 2)
lv.expect('l4', 'screens[0].widget.wrong[2].value', x * x - 3 * x)
lv.expect('l4', 'screens[0].explain.canvas.caption', 3 * (x - 3))
same_two_ways('l4 s2 width', '(x - 3) + 3 + 3', 'x + 3')
same_two_ways('l4 s2 rectangle', '(x + 3)(x - 3)', 'x^2 - 9')
choice_polys('l4', 'screens[3].widget', 'x^2 - 25')
choice_polys('l4', 'screens[4].widget', '4x^2 - 9')
same_two_ways('l4 s4 four-x', '(4x + 3)(4x - 3)', '16x^2 - 9')
choice_polys('l4', 'screens[5].widget', '3x^2 - 48')
same_two_ways('l4 s5 three-in-bracket', '(3x + 4)(x - 4)', '3x^2 - 8x - 16')
same_two_ways('l4 s5 square', '3(x - 4)^2', '3x^2 - 24x + 48')
same_two_ways('l4 s6 right', '(x + 3)^2', 'x^2 + 6x + 9')
same_two_ways('l4 s6 minus', '(x - 3)^2', 'x^2 - 6x + 9')
same_two_ways('l4 s6 dots', '(x + 3)(x - 3)', 'x^2 - 9')
lv.claim(not [p for p in range(-9, 10) if p and 9 % p == 0 and p + 9 // p == 0], 'l4 s6: no whole pair has product 9 and sum 0')
lv.claim(all(-p * p != 9 for p in range(-20, 21)), 'l4 s6: p + q = 0 forces pq = -p^2 <= 0, never 9')
# summary.trap (finding 3): "A sum of two squares has no factors at all" -- 4x^2 + 36 = 4(x^2 + 9)
lv.stated('l4', 'summary.trap', 'A sum of two squares has no factors at all', poly('4x^2 + 36') != poly('4(x^2 + 9)'))
S, r = 50, 0.08
lv.expect('l4', 'screens[8].widget.answer', two('l4 s8 value', S * (1 + r) * (1 - r), S * (1 - r * r)))
lv.expect('l4', 'screens[8].widget.wrong[1].value', S * (1 - r))
lv.expect('l4', 'screens[8].widget.wrong[2].value', S * (1 + r))
lv.expect('l4', 'screens[8].widget.wrong[3].value', round(S * (1 - 2 * r * r), 2))
lv.expect('l4', 'screens[8].hints[2].text', 1 - r * r)
choice_polys('l4', 'quiz[0].widget', 'x^2 - 49')
lv.claim(49 - 1 == 48, 'l4 quiz[0] area-as-side: 49 and -1 add to 48')
lv.expect('l4', 'quiz[1].widget.answer', two('l4 quiz[1]', 51 ** 2 - 49 ** 2, (51 + 49) * (51 - 49)))
lv.expect('l4', 'quiz[1].widget.wrong[0].value', (51 - 49) ** 2)
lv.expect('l4', 'quiz[1].widget.wrong[1].value', (51 + 49) ** 2)
lv.expect('l4', 'quiz[1].explain.text', 51 ** 2)
lv.expect('l4', 'quiz[1].explain.text', 49 ** 2)
choice_polys('l4', 'quiz[2].widget', '2x^2 - 50')
same_two_ways('l4 quiz[3] 9x^2 - 1', '(3x + 1)(3x - 1)', '9x^2 - 1')
same_two_ways('l4 quiz[3] 100 - x^2', '(10 + x)(10 - x)', '100 - x^2')

# ================= review-1 =================
choice_polys('review', 'items[0].widget', '(x - 7)(x + 2)')
lv.expect('review', 'items[1].widget.answer', two('r1 items[1] b', poly('(x + 5)^2')[1], 2 * 5))
lv.expect('review', 'items[1].widget.wrong[0].value', 5)
lv.expect('review', 'items[1].widget.wrong[2].value', 25)
choice_polys('review', 'items[2].widget', 'x^2 + 3x - 28')
lv.claim(14 * -2 == -28 and 14 - 2 == 12 and -7 + 4 == -3, 'r1 items[2] distractor sums')
choice_polys('review', 'items[3].widget', '2x^2 - 5x - 3')
choice_polys('review', 'items[4].widget', '49x^2 - 16')
choice_polys('review', 'items[5].widget', '5x^2 - 20x + 15')
same_two_ways('r1 items[5] not-full', '(5x - 5)(x - 3)', '5x^2 - 20x + 15')
P, r = 5000, 0.03
lv.expect('review', 'items[6].widget.answer', two('r1 items[6]', round(P * (1 + r) ** 2, 6), P * (1 + 2 * r + r * r)))
lv.expect('review', 'items[6].widget.wrong[0].value', P * (1 + 2 * r))
lv.expect('review', 'items[6].widget.wrong[1].value', P * (1 + r * r))
lv.expect('review', 'items[6].widget.wrong[2].value', P * (1 + r))
lv.expect('review', 'items[6].feedback.byKey.simple', P * r * r, fmt='£{:.2f}')
lv.expect('review', 'items[6].explain.text', round((1 + r) ** 2, 6))
S, r = 80, 0.05
lv.expect('review', 'items[7].widget.answer', two('r1 items[7]', S * (1 + r) * (1 - r), S * (1 - r * r)))
lv.expect('review', 'items[7].widget.wrong[1].value', S * (1 - 2 * r * r))
lv.expect('review', 'items[7].explain.text', 1 - r * r)
lv.claim(fit(-14, 40) == [(-10, -4)], 'r1 items[8]: q^2 - 14q + 40 = (q - 4)(q - 10)')
lv.expect('review', 'items[8].widget.answer', 10)
for i, v in enumerate((4, 14, 40)):
    lv.expect('review', f'items[8].widget.wrong[{i}].value', v)

# ================= homework-1 =================
choice_polys('homework', 'items[0].widget', 'x^2 - 11x + 24')
choice_polys('homework', 'items[1].widget', '6x^2 + 7x + 2')
same_two_ways('h1 items[1] not-full', '(3x + 1)(2x + 2)', '6x^2 + 8x + 2')
choice_polys('homework', 'items[2].widget', '(2x - 3)^2')
choice_polys('homework', 'items[3].widget', '18x^2 - 8')
lv.expect('homework', 'items[4].widget.answer', two('h1 items[4]', 1003 ** 2 - 997 ** 2, 2000 * 6))
lv.expect('homework', 'items[4].widget.wrong[0].value', 6 ** 2)
lv.expect('homework', 'items[4].widget.wrong[1].value', 2000)
lv.expect('homework', 'items[5].widget.answer', two('h1 items[5] k', poly('(x + 6)^2')[1], 2 * 6))
for i, v in enumerate((6, 36, 18)):
    lv.expect('homework', f'items[5].widget.wrong[{i}].value', v)
same_two_ways('h1 items[6] profit', 'q(25 - 0.5q) - 7q - 160', '-0.5(q^2 - 36q + 320)')
lv.expect('homework', 'items[6].widget.answer', two('h1 items[6] other root', 320 // 16, 36 - 16))
lv.claim(ev(poly('q^2 - 36q + 320'), 16) == 0 and ev(poly('q^2 - 36q + 320'), 20) == 0, 'h1 items[6]: 16 and 20 are roots')
lv.claim((25 - 0.5 * 20) * 20 == 300 == 7 * 20 + 160, 'h1 items[6] explain: revenue £300 meets cost 140 + 160')
xs = [0.01, 0.03, 0.05]
m = sum(xs) / 3
var1 = sum((t - m) ** 2 for t in xs) / 3
var2 = sum(t * t for t in xs) / 3 - m * m
two('h1 items[7] variance two ways', var1, var2)
lv.claim(abs(var1 - 0.0008 / 3) < 1e-12 and abs(sum(t * t for t in xs) - 0.0035) < 1e-12, 'h1 items[7]: 0.0002(6) and 0.0035/3 - 0.0009')
same_two_ways('h1 items[8] (a)', '2(x + 4)(x - 3)', '2x^2 + 2x - 24')
same_two_ways('h1 items[8] (b)', '(3x + 5)(3x - 5)', '9x^2 - 25')
same_two_ways('h1 items[8] (c)', '(x + 7)(x - 1)', '(x + 3)^2 - 16')
lv.claim(sorted({abs(p + 16 // p) for p in (1, 2, 4, -1, -2, -4)}) == [8, 10, 17], 'h1 items[8] (d): pairs for 16 add to 8, 10, 17')

lv.check_wrongs()
lv.report()
