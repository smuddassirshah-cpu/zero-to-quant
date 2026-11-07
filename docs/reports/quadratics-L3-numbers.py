"""Second read of quadratics level 3 (l9 to l13, review-3, homework-3): every graded key, every wrong[] value and
the numbers in prose, hints, feedback and explanations, each computed two ways (method 1: the vertex rule -b/2a,
factor midpoints or exact polynomial arithmetic; method 2: a fine scan for the extreme value, brute-force counting,
or values at sample points), and checked against the JSON with app/tools/numbers_lib.py.
Checks written with lv.stated() fail while a false sentence is still in the text: they are review findings
(docs/reviews/review-quadratics-1-3.md) and pass once the fix pass rewords them.
Run: python3 docs/reports/quadratics-L3-numbers.py
"""
import os, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("quadratics", 3)


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


def vertex(a, b, c):
    """Method 1: x = -b/2a; method 2 is a scan over a fine grid, done by the caller."""
    h = -b / (2 * a)
    return h, a * h * h + b * h + c


def scan_extreme(f, lo, hi, n=200000, mx=True):
    xs = [lo + (hi - lo) * i / n for i in range(n + 1)]
    best = max(xs, key=f) if mx else min(xs, key=f)
    return best, f(best)


def near(label, a, b, tol=1e-6):
    lv.claim(abs(a - b) <= tol, f'{label}: {a:.8g} (method 1) ~ {b:.8g} (method 2)')
    return a


heights = lambda f, xs: [f(x) for x in xs]

# ================= l9 =================
lv.claim(3 ** 2 == 9 == 3 * 3 and 2 * 3 == 6 and 4 + 3 == 7, 'l9 s0: target 9; slips 6 (doubled) and 7 (climbed 3 again)')
lv.claim([(k + 1) ** 2 - k ** 2 for k in range(3)] == [1, 3, 5], 'l9 s0 explain: climbs 1, 3, 5')
lv.claim((4 - 2) ** 2 == 4 == (0 - 2) ** 2 and 2 - 0 == 4 - 2, 'l9 s2: Q = (4, 4) mirrors P = (0, 4) in x = 2')
lv.claim(2 ** 2 + -3 == 1 and 2 ** 2 + 3 == 7, 'l9 s3: k = -3; with k = 3 the height at 2 is 7')
lv.claim(-0.5 * 4 == -2 and -1 * 4 == -4, 'l9 s4: a = -1/2; a = -1 gives -4')
lv.claim(heights(lambda x: 4 - x * x, range(-3, 4)) == [-5, 0, 3, 4, 3, 0, -5], 'l9 s5 hint: heights -5, 0, 3, 4, 3, 0, -5')
P = lambda d: 100 - 7 * d + 0.3 * d * d
lv.expect('l9', 'screens[9].widget.answer', near('l9 s9 average', (P(2) + P(-2)) / 2, 100 + 0.3 * 4))
lv.expect('l9', 'screens[9].widget.wrong[1].value', P(2))
lv.expect('l9', 'screens[9].widget.wrong[2].value', P(-2))
lv.expect('l9', 'screens[9].hints[1].text', 0.3 * 4)
lv.expect('l9','quiz[0].widget.answer', (-3) ** 2 - 5)
lv.expect('l9', 'quiz[0].widget.wrong[0].value', -9 - 5)
lv.expect('l9', 'quiz[0].widget.wrong[1].value', -6 - 5)
lv.expect('l9', 'quiz[2].widget.answer', two('l9 quiz[2] mirror', 4 + (4 - 1), [x for x in range(-10, 20) if 2 * (x - 4) ** 2 == 18 and x != 1][0]))
lv.expect('l9', 'quiz[2].widget.wrong[0].value', -1)
lv.expect('l9', 'quiz[2].widget.wrong[1].value', 4)
lv.expect('l9', 'quiz[2].widget.wrong[2].value', 9)

# ================= l10 =================
lv.claim(vertex(1, -4, 5) == (2, 1) and (0 - 2) ** 2 + 1 == 5, 'l10 s0: vertex (2, 1); intercept (0, 5)')
lv.claim(vertex(2, 4, -1) == (-1, -3), 'l10 s2: 2(x + 1)^2 - 3 has vertex (-1, -3)')
lv.expect('l10', 'screens[3].widget.answer', two('l10 s3 max', vertex(-1, 6, -4)[1], scan_extreme(lambda x: 5 - (x - 3) ** 2, -1, 7)[1]))
lv.expect('l10', 'screens[3].widget.wrong[0].value', 3)
lv.expect('l10', 'screens[3].widget.wrong[1].value', -5)
lv.expect('l10', 'screens[3].widget.wrong[2].value', 5 - 9)
same_two_ways('l10 s4', 'x^2 - 6x + 11', '(x - 3)^2 + 2')
lv.claim(vertex(1, -6, 4) == (3, -5) and vertex(1, 6, 4)[0] == -3 and vertex(1, -3, 4)[0] == 1.5, 'l10 s5: b = -6 gives (3, -5); b = 6 gives x = -3; b = -3 gives 1.5')
same_two_ways('l10 s5 explain', 'x^2 - 6x + 4', '(x - 3)^2 - 5')
same_two_ways('l10 s6 explain', '2x^2 - 12x + 7', '2(x - 3)^2 - 11')
lv.expect('l10', 'screens[6].widget.options[0].why', ev(poly('2x^2 - 12x + 7'), 12))
lv.claim(vertex(-1, 4, 1) == (2, 5) and -4 - 8 + 1 == -11, 'l10 s8: max 5 at 2; at x = -2 the value is -11')
pi = lambda q: -0.04 * q * q + 12 * q - 500
lv.expect('l10', 'screens[9].widget.answer', near('l10 s9 max', vertex(-0.04, 12, -500)[1], scan_extreme(pi, 0, 350)[1], 1e-6))
lv.claim(abs(vertex(-0.04, 12, -500)[0] - 150) < 1e-9, 'l10 s9: q = 150')
lv.expect('l10', 'screens[9].widget.wrong[0].value', two('l10 s9 ends', pi(0), round(pi(300), 9)))
lv.expect('l10', 'screens[9].widget.wrong[2].value', round(pi(12), 2))
lv.claim(abs(12 / 0.04 - 300) < 1e-9, 'l10 s9 ends why: -b/a = 300')
lv.claim(vertex(-2, 4, 6) == (1, 8), 'l10 quiz[0]: -2(x - 1)^2 + 8 has vertex (1, 8)')
lv.expect('l10', 'quiz[1].widget.answer', vertex(1, 10, 18)[0])
same_two_ways('l10 quiz[1] explain', 'x^2 + 10x + 18', '(x + 5)^2 - 7')
lv.expect('l10', 'quiz[2].widget.answer', two('l10 quiz[2] min', vertex(3, -12, 5)[1], round(scan_extreme(lambda x: 3 * x * x - 12 * x + 5, -5, 5, mx=False)[1], 6)))
lv.expect('l10', 'quiz[2].widget.wrong[2].value', 3 * 4 + 24 + 5)
lv.claim(vertex(-2, 0, 5) == (0, 5) or vertex(-2, 0, 5) == (-0.0, 5), 'l10 quiz[3]: vertex (0, 5)')

# ================= l11 =================
f = lambda x: (x + 2) * (x - 4)
lv.expect('l11', 'screens[2].widget.answer', two('l11 s2 intercept', f(0), 1 * 2 * -4))
lv.expect('l11', 'screens[2].widget.wrong[0].value', 8)
lv.expect('l11', 'screens[2].widget.wrong[2].value', two('l11 s2 vertex', f(1), vertex(1, -2, -8)[1]))
lv.stated('l11', 'screens[2].feedback.byKey.sum', 'You added the numbers in the brackets', 2 + (-4) == 2)   # finding: 2 + (-4) = -2
lv.claim(heights(lambda x: (x + 1) * (x - 3), range(-2, 5)) == [5, 0, -3, -4, -3, 0, 5], 'l11 s3 hint: heights 5, 0, -3, -4, -3, 0, 5')
lv.expect('l11', 'screens[4].widget.answer', two('l11 s4 min', 2 * (4 - 1) * (4 - 7), vertex(2, -16, 14)[1]))
lv.expect('l11', 'screens[4].widget.wrong[0].value', (4 - 1) * (4 - 7))
lv.expect('l11', 'screens[4].widget.wrong[1].value', 2 * -1 * -7)
lv.claim(16 - 4 * 4 == 0 and vertex(1, -4, 4) == (2, 0), 'l11 s5: c = 4 touches at 2')
lv.claim(vertex(1, -6, 8) == (3, -1) and (3 - 2) * (3 - 4) == -1, 'l11 s6: vertex (3, -1)')
lv.claim((-3 + 5) / 2 == 1 and (5 - -3) / 2 == 4 and -3 + 5 == 2 and (3 + -5) / 2 == -1, 'l11 s8: line x = 1; slips 4, 2, -1')
lv.expect('l11', 'screens[9].widget.answer', two('l11 s9 break-even', sqrt(1.8 / 0.05), [x for x in range(0, 20) if abs(0.05 * x * x - 1.8) < 1e-9][0]))
lv.expect('l11', 'screens[9].widget.wrong[0].value', 36)
lv.expect('l11', 'screens[9].widget.wrong[2].value', 18)
lv.expect('l11', 'quiz[1].widget.answer', 3 * -2 * -6)
lv.expect('l11', 'quiz[1].widget.wrong[0].value', -2 * -6)
lv.expect('l11', 'quiz[1].widget.wrong[1].value', two('l11 quiz[1] vertex', 3 * (4 - 2) * (4 - 6), vertex(3, -24, 36)[1]))
lv.expect('l11', 'quiz[2].widget.answer', two('l11 quiz[2] max', -(2 + 1) * (2 - 5), vertex(-1, 4, 5)[1]))
lv.expect('l11', 'quiz[2].widget.wrong[1].value', -(0 + 1) * (0 - 5))
lv.claim(36 - 36 == 0, 'l11 quiz[3]: disc of (x - 3)^2 is 0')

# ================= l12 =================
lv.claim([x for x in [i / 10 for i in range(-40, 41)] if x * x - 4 < 0] == [i / 10 for i in range(-19, 20)], 'l12 s0: x^2 - 4 < 0 exactly on -2 < x < 2')
lv.claim((-3) ** 2 - 4 == 5, 'l12 s0 linear why: height 5 at x = -3')
crossings = lambda c: sum(1 for i in range(-4000, 4000) if ((i / 400) ** 2 - i / 400 - c) * (((i + 1) / 400) ** 2 - (i + 1) / 400 - c) < 0)
lv.claim(all(crossings(c) == (2 if 1 + 4 * c > 0 else 0) for c in (-1, -0.3, 0.5, 2.2)), 'l12 s1: disc 1 + 4c; two meeting points for c > -0.25, none below')
lv.claim([x for x in range(-5, 6) if x * x == x + 2] == [-1, 2], 'l12 s2: x^2 = x + 2 at -1 and 2')
lv.claim((-2) ** 2 == 4 and -2 + 2 == 0, 'l12 s3 one-side why')
lv.expect('l12', 'screens[4].widget.answer', two('l12 s4 count', len([x for x in range(-10, 11) if x * x - 2 * x - 8 < 0]), 4 - -2 - 1))
lv.expect('l12', 'screens[4].widget.wrong[0].value', 7)
lv.expect('l12', 'screens[4].widget.wrong[1].value', 6)
lv.claim([x for x in range(-10, 11) if x * x - 2 * x - 8 < 0] == [-1, 0, 1, 2, 3], 'l12 s4: -1, 0, 1, 2, 3')
lv.claim(-25 + 20 == -5 and [x for x in [i / 4 for i in range(-20, 30)] if -x * x + 4 * x > 0] == [i / 4 for i in range(1, 16)], 'l12 s8: -x^2 + 4x > 0 on 0 < x < 4')
V = lambda w: 0.01 * w * w + 0.04 * (1 - w) ** 2
lv.claim(all(abs(V(w) - (0.05 * w * w - 0.08 * w + 0.04)) < 1e-12 for w in (0, 0.3, 0.7, 1.2)), 'l12 s9: V(w) = 0.05w^2 - 0.08w + 0.04 from the two volatilities')
lv.claim(all(abs(20 * (0.05 * w * w - 0.08 * w + 0.03) - (w - 0.6) * (w - 1)) < 1e-12 for w in (0, 0.5, 2)), 'l12 s9 hint: x20 gives (w - 0.6)(w - 1)')
ok = [w / 1000 for w in range(-100, 1301) if V(w / 1000) <= 0.01 + 1e-12]
lv.expect('l12', 'screens[9].widget.answer', two('l12 s9 smallest w', round(min(ok), 3), 0.6))
lv.expect('l12', 'screens[9].widget.wrong[0].value', round(max(ok), 3))
lv.expect('l12', 'screens[9].widget.wrong[1].value', round(vertex(0.05, -0.08, 0.04)[0], 9))
lv.expect('l12', 'screens[9].feedback.byKey.equal', round(V(0.5), 6))
lv.claim(25 - 16 == 9, 'l12 quiz[0] b why: x = -5 gives 9')
lv.expect('l12', 'quiz[1].widget.answer', len([x for x in range(-10, 20) if (x - 1) * (x - 6) < 0]))
lv.claim([x for x in range(-5, 6) if x * x == 3 * x - 2] == [1, 2], 'l12 quiz[2]: meet at x = 1, 2 (heights 1, 4)')

# ================= l13 =================
R = lambda p: p * (500 - 10 * p)
lv.claim(scan_extreme(R, 0, 50, 2000) == (25, 6250) and 500 - 250 == 250, 'l13 s0: £25.00, 250 subscribers, £6,250.00')
lv.expect('l13', 'screens[1].widget.answer', two('l13 s1 mirror', 25 + (25 - 20), [p for p in range(21, 51) if R(p) == R(20)][0]))
lv.claim(R(20) == 6000 and R(40) == 4000, 'l13 s1: R(20) = 6000, R(40) = 4000')
same_two_ways('l13 s2 key', 'p(800 - 20p)', '800p - 20p^2')
R2 = lambda p: p * (800 - 20 * p)
lv.expect('l13', 'screens[3].widget.answer', two('l13 s3 best', (0 + 40) / 2, scan_extreme(R2, 0, 40, 4000)[0]))
lv.expect('l13', 'screens[3].widget.wrong[1].value', R2(20))
lv.expect('l13', 'screens[3].widget.wrong[2].value', 10)
same_two_ways('l13 s4', '500p - 10p^2', '-10(p - 25)^2 + 6250')
R3 = lambda p: p * (1500 - 200 * p)
lv.expect('l13', 'screens[5].widget.answer', two('l13 s5 best', 7.5 / 2, scan_extreme(R3, 0, 7.5, 3000)[0]))
lv.expect('l13', 'screens[5].widget.wrong[1].value', R3(3.75))
lv.claim(1500 - 200 * 3.75 == 750 and 1500 / 200 == 7.5, 'l13 s5: 750 notes, demand zero at £7.50')
Pf = lambda p: (p - 4) * (500 - 10 * p)
lv.claim(scan_extreme(Pf, 4, 50, 4600) == (27, 5290) and 23 * 230 == 5290 and Pf(29) < Pf(27), 'l13 s6: £27.00, £5,290.00; £29.00 earns less')
lv.claim(500 / (2 * 10) == 25, 'l13 s7 check: A/2B with A = 500, B = 10 is 25')
lv.claim(900 / 60 == 15 and 900 - 30 * 15 == 450 and 15 * 450 == 6750, 'l13 s8: £15.00, 450 sold, £6,750.00')
V13 = lambda w: 0.01 * w * w + 0.09 * (1 - w) ** 2
lv.claim(all(abs(V13(w) - (0.1 * w * w - 0.18 * w + 0.09)) < 1e-12 for w in (0, 0.3, 1, 1.5)), 'l13 s9: V(w) = 0.1w^2 - 0.18w + 0.09')
lv.claim(abs(vertex(0.1, -0.18, 0.09)[0] - 0.9) < 1e-12 and abs(V13(0.9) - 0.009) < 1e-12 and round(scan_extreme(V13, 0, 1, 10000, mx=False)[0], 3) == 0.9, 'l13 s9: w = 0.9, V = 0.009')
lv.claim(round(sqrt(0.009) * 100, 1) == 9.5, 'l13 s9: volatility 9.5%')
lv.claim(abs(V13(0.5) - 0.025) < 1e-12 and V13(0.1) > V13(0.9), 'l13 s9 equal why: V(0.5) = 0.025; 90% in B is worse')
lv.claim(abs(V13(0.05) - 0.08125) < 1e-12 and 0 < V13(1) < V13(0) <= 0.1, 'l13 s9 start point P (0.05, 0.08125) and y range 0 to 0.1')
lv.expect('l13', 'screens[9].explain.text', 0.009)
lv.expect('l13', 'screens[9].feedback.byKey.equal', 0.025)
lv.expect('l13', 'quiz[0].widget.answer', two('l13 quiz[0]', 600 / 80, scan_extreme(lambda p: p * (600 - 40 * p), 0, 15, 3000)[0]))
lv.claim(600 - 40 * 7.5 == 300 and 7.5 * 300 == 2250, 'l13 quiz[0] explain: 300 sold, £2,250')
lv.claim(vertex(-5, 120, -5 * 144 + 720) == (12, 720), 'l13 quiz[1]: vertex (12, 720)')
Pq = lambda p: (p - 6) * (300 - 15 * p)
lv.expect('l13', 'quiz[2].widget.answer', two('l13 quiz[2]', (6 + 20) / 2, scan_extreme(Pq, 6, 20, 2800)[0]))
lv.claim(Pq(13) == 735 == 7 * 105 and 300 / 30 == 10 and 10 + 6 == 16, 'l13 quiz[2]: £735; slips 10 and 16')
lv.expect('l13', 'quiz[3].widget.answer', two('l13 quiz[3]', 0.1 / (2 * 0.08), round(scan_extreme(lambda w: 0.08 * w * w - 0.1 * w + 0.05, 0, 1, 8000, mx=False)[0], 6)))
lv.expect('l13', 'quiz[3].widget.wrong[0].value', 0.1 / 0.08)

# ================= review-3 =================
lv.claim(vertex(-1, -2, 3) == (-1, 4), 'r3 items[0]: 4 - (x + 1)^2 has vertex (-1, 4)')
lv.claim(vertex(3, -12, 7) == (2, -5), 'r3 items[1]: vertex (2, -5)')
lv.expect('review', 'items[2].widget.answer', vertex(2, 8, 1)[0])
same_two_ways('r3 items[2] explain', '2x^2 + 8x + 1', '2(x + 2)^2 - 7')
lv.expect('review', 'items[2].widget.wrong[2].value', -8 / 2)
lv.expect('review', 'items[3].widget.answer', two('r3 items[3]', (1 + 3) * (1 - 5), vertex(1, -2, -15)[1]))
lv.expect('review', 'items[3].widget.wrong[0].value', 3 * -5)
g = lambda x: 2 * (x - 1) * (x + 4)
lv.expect('review', 'items[4].widget.answer', g(0))
lv.expect('review', 'items[4].widget.wrong[0].value', two('r3 items[4] vertex', g(-1.5), vertex(2, 6, -8)[1]))
lv.expect('review', 'items[4].widget.wrong[1].value', -1 * 4)
lv.claim(25 + 5 - 12 == 18 and [x for x in range(-10, 11) if x * x - x - 12 > 0][:3] == [-10, -9, -8], 'r3 items[5]: x = -5 gives 18')
lv.expect('review', 'items[6].widget.answer', 3 ** 2)
lv.claim([x for x in range(-5, 6) if x * x == 2 * x + 3] == [-1, 3], 'r3 items[6]: crossings at -1 (height 1) and 3 (height 9)')
lv.claim(heights(lambda x: -(x - 1) * (x - 5), range(0, 7)) == [-5, 0, 3, 4, 3, 0, -5], 'r3 items[7]: heights -5, 0, 3, 4, 3, 0, -5')
lv.expect('review', 'items[8].widget.answer', two('r3 items[8]', 7.5 * 600, scan_extreme(lambda p: p * (1200 - 80 * p), 0, 15, 3000)[1]))
lv.claim(1200 / 80 == 15 and 1200 - 80 * 7.5 == 600, 'r3 items[8]: zero at £15, 600 sold at £7.50')
Pr = lambda p: (p - 2) * (60 - 4 * p)
lv.expect('review', 'items[9].widget.answer', two('r3 items[9]', (2 + 15) / 2, scan_extreme(Pr, 2, 15, 2600)[0]))
lv.claim(Pr(8.5) == 169 == 6.5 * 26 and 2 + 15 == 17 and 15 / 2 + 2 == 9.5, 'r3 items[9]: £169; slips 17 and 9.5')

# ================= homework-3 =================
Pb = lambda d: 100 - 6 * d + 0.4 * d * d
lv.expect('homework', 'items[0].widget.answer', two('h3 items[0]', 6 / (2 * 0.4), scan_extreme(Pb, 0, 15, 15000, mx=False)[0]))
lv.expect('homework', 'items[0].widget.wrong[0].value', 6)
lv.expect('homework', 'items[0].widget.wrong[1].value', 6 / 0.4)
lv.expect('homework', 'items[0].widget.wrong[2].value', -7.5)
lv.expect('homework', 'items[0].explain.text', Pb(7.5))
lv.claim(abs(Pb(7.5) - 77.5) < 1e-12 and 100 - 45 + 22.5 == 77.5, 'h3 items[0]: P(7.5) = 77.50')
lv.claim(vertex(-2, 12, -10) == (3, 8) and -2 * 36 + 72 - 10 == -10, 'h3 items[1]: max 8 at 3; at 6 the value is -10')
same_two_ways('h3 items[1] explain', '-2x^2 + 12x - 10', '-2(x - 3)^2 + 8')
lv.claim(heights(lambda x: 0.5 * (x + 2) * (x - 4), range(-3, 6)) == [3.5, 0, -2.5, -4, -4.5, -4, -2.5, 0, 3.5], 'h3 items[2]: the nine heights')
a_ = -32 / ((0 - 2) * (0 - 8))
lv.expect('homework', 'items[3].widget.answer', two('h3 items[3]', a_ * (5 - 2) * (5 - 8), vertex(a_, -10 * a_, 16 * a_)[1]))
lv.expect('homework', 'items[3].widget.wrong[0].value', (5 - 2) * (5 - 8))
lv.expect('homework', 'items[4].widget.answer', two('h3 items[4]', len([x for x in range(-20, 20) if x * x + 3 * x < 10]), 2 - -5 - 1))
lv.expect('homework', 'items[4].widget.wrong[0].value', 8)
lv.expect('homework', 'items[4].widget.wrong[1].value', 7)
lv.claim(len([x for x in range(-20, 20) if -2 < x < 5]) == 6 and 'signs' not in str(lv.text('homework', 'items[4]')), 'h3 items[4]: the signs slip (4) is removed; it counted 6 anyway')
lv.claim([x for x in range(-10, 11) if x * x - 4 * x + 7 == 2 * x - 2] == [3] and 2 * 3 - 2 == 4, 'h3 items[5]: one meeting point (3, 4)')
k = -6 / -36
Q = lambda x: k * (x - 6) * (x + 6)
lv.expect('homework', 'items[6].widget.answer', two('h3 items[6]', round(Q(9) - (abs(9) - 6), 9), (81 - 36) / 6 - 3))
lv.expect('homework', 'items[6].widget.wrong[0].value', round(Q(9), 9))
lv.expect('homework', 'items[6].widget.wrong[2].value', (81 - 36) - 3)
lv.claim(abs(0.09 / (0.01 + 0.09) - 0.9) < 1e-12, 'h3 items[7] explain: 0.09 / 0.10 = 0.9')
lv.expect('homework', 'items[7].explain.text', 0.9)
Vc = lambda w: 0.01 * w * w + 0.04 * (1 - w) ** 2 + 2 * w * (1 - w) * 0.25 * 0.1 * 0.2
lv.claim(all(abs(Vc(w) - (0.04 * w * w - 0.07 * w + 0.04)) < 1e-12 for w in (0, 0.4, 1, 1.5)), 'h3 items[8]: V(w) = 0.04w^2 - 0.07w + 0.04')
lv.expect('homework', 'items[8].widget.answer', two('h3 items[8]', 0.07 / 0.08, round(scan_extreme(Vc, 0, 1, 8000, mx=False)[0], 6)))
lv.expect('homework', 'items[8].explain.text', round(Vc(0.875), 9))
lv.claim(round(sqrt(Vc(0.875)) * 100, 1) == 9.7, 'h3 items[8] explain: volatility about 9.7%')
lv.expect('homework', 'items[8].widget.wrong[1].value', 0.07 / 0.04)
same_two_ways('h3 items[9] profit', '(p - 5)(2000 - 80p)', '-80p^2 + 2400p - 10000')
same_two_ways('h3 items[9] square', '-80p^2 + 2400p - 10000', '-80(p - 15)^2 + 8000')
lv.claim(2000 - 80 * 15 == 800 and 10 * 800 == 8000 and 2000 / 80 == 25 and 12.5 * (2000 - 80 * 12.5) == 12500, 'h3 items[9] model: 800 clients, £8,000; revenue £12,500 at £12.50')

lv.check_wrongs()
lv.report()
