"""Second reader's recompute for quadratics level 4 (l14 to l19, review-4, homework-4), by a second route: sympy.
Each graded key and wrong value is read from the content and compared with a symbolic computation; tolerances are probed
with the engine's own rule (grade.js `within`). A check that fails because the content is wrong stays failing and is a
finding in docs/reviews/review-quadratics-4.md. Run from the repository root with the scratchpad venv python."""
import json, sys
from sympy import (symbols, sqrt, simplify, expand, factor, Rational as R, solve, Eq, div, Poly, discriminant, cancel,
                   radsimp, real_roots)

B = 'app/content/courses/quadratics/'
D = {n: json.load(open(B + n + '.json')) for n in ['l14-roots-that-stay', 'l15-fractions-with-letters', 'l16-adding-and-solving',
     'l17-dividing-polynomials', 'l18-circles-on-a-grid', 'l19-line-meets-curve', 'review-4', 'homework-4']}
L14, L15, L16, L17, L18, L19, RV, HW = D.values()
x, y, k, p, m, c, r, a, b, F = symbols('x y k p m c r a b F', real=True)
n_ok = n_bad = 0


def chk(label, cond):
    global n_ok, n_bad
    if cond:
        n_ok += 1
    else:
        n_bad += 1
        print('FAIL', label)


def within(v, ans, tol):
    return abs(v - ans) <= tol.get('abs', 0) + 1e-9


def w(doc, i, sec='screens'):
    return doc[sec][i]['widget']


def cell(doc, i, row, sec='screens', col=1):
    return w(doc, i, sec)['rows'][row][col]


def wrongs(spec):
    return {e['id']: e['value'] for e in spec.get('wrong', [])}


def right(doc, i, sec='screens'):
    return [o['text'] for o in w(doc, i, sec)['options'] if o.get('correct')]


def shoelace(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2


# ---------------- l14 surds
pol = {q['id']: q['points'] for q in L14['screens'][0]['canvas']['state']['polygons']}
chk('l14 s0 small area 2', shoelace(pol['small']) == 2)
chk('l14 s0 large area', shoelace(pol['large']) == w(L14, 0)['answer'] == 8)
chk('l14 s0 wrongs', wrongs(w(L14, 0)) == {'box': 16, 'small-corners': 16 - 4 * R(1, 2)})
chk('l14 s1 sqrt8 = 2 sqrt2', sqrt(8) == 2 * sqrt(2) and w(L14, 1)['answer'] == 2)
for s_ in (1, 2, 3):
    chk(f'l14 s1 caption area s={s_}', shoelace([(s_, 0), (2 * s_, s_), (s_, 2 * s_), (0, s_)]) == 2 * s_ * s_)
chk('l14 s2 a', sqrt(72) / sqrt(2) == w(L14, 2)['answer'])
chk('l14 s2 wrongs', 3 * sqrt(8) == sqrt(72) and 2 * sqrt(18) == sqrt(72) and wrongs(w(L14, 2)) == {'stop-8': 3, 'stop-18': 2, 'no-root': 36})
chk('l14 s3 cells', [sqrt(50) / sqrt(2), sqrt(18) / sqrt(2), (sqrt(50) + sqrt(18)) / sqrt(2)] == [cell(L14, 3, i)['answer'] for i in range(3)])
chk('l14 s3 sqrt68', sqrt(68) == 2 * sqrt(17) and sqrt(68) != sqrt(50) + sqrt(18))
e = expand((1 + sqrt(3)) ** 2)
chk('l14 s4', e.coeff(sqrt(3), 0) == cell(L14, 4, 0)['answer'] and e.coeff(sqrt(3), 1) == cell(L14, 4, 1)['answer'] and expand((3 + sqrt(2)) * (3 - sqrt(2))) == cell(L14, 4, 2)['answer'])
chk('l14 s5', simplify(6 / sqrt(3) - cell(L14, 5, 0)['answer'] * sqrt(3)) == 0 and simplify(1 / (3 - sqrt(2)) - (cell(L14, 5, 1)['answer'] + sqrt(2)) / cell(L14, 5, 2)['answer']) == 0)
rts = solve(x ** 2 - 6 * x + 1, x)
chk('l14 s6 roots', set(rts) == {3 + 2 * sqrt(2), 3 - 2 * sqrt(2)} and right(L14, 6) == ['$3 \\pm 2\\sqrt{2}$'])
chk('l14 s6 decimals', [round(float(v), 3) for v in sorted(rts)] == [0.172, 5.828])
chk('l14 s7', sqrt(9 + 16) == w(L14, 7)['answer'] and sqrt(9) + sqrt(16) == 7)
chk('l14 s9', sqrt(252) == cell(L14, 9, 0)['answer'] * sqrt(7) and within(float(sqrt(252)), cell(L14, 9, 1)['answer'], cell(L14, 9, 1)['tol']) and round(252 / float(sqrt(252))) == 16)
chk('l14 q0 q1', sqrt(45) + sqrt(20) == 5 * sqrt(5) and R(1414, 1000) ** 2 == R(1999396, 1000000))
chk('l14 q3', simplify(5 / (2 + sqrt(3)) - (10 - 5 * sqrt(3))) == 0 and round(float(10 - 5 * sqrt(3)), 2) == 1.34)
# claim: "a root splits over a product, never over a sum" (s7 byKey, summary trap): false when one term is 0
chk('l14 CLAIM "never over a sum" (sqrt(0+9) = sqrt0 + sqrt9 is a counter-example)', sqrt(0 + 9) != sqrt(0) + sqrt(9))
# claim: quiz q14-domain explain "sqrt(a) is the positive number whose square is a" for every a >= 0: sqrt(0) is not positive
chk('l14 CLAIM q14-domain "the positive number" at a = 0', sqrt(0) > 0)

# ---------------- l15 algebraic fractions
chk('l15 s0', R(84, 120) == R(7, 10))
f15 = (x ** 2 + 5 * x + 6) / (x ** 2 + 3 * x + 2)
chk('l15 s1', f15.subs(x, 1) == w(L15, 1)['answer'] and [f15.subs(x, v) for v in (2, 3)] == [R(5, 3), R(3, 2)] and cancel(f15) == (x + 3) / (x + 1))
chk('l15 s3', cancel((x ** 2 - 9) / (x ** 2 + 3 * x) - (x - 3) / x) == 0)
chk('l15 s4', cancel((x ** 2 - 4) / (x + 3) * (2 * x + 6) / (x - 2) - 2 * (x + 2)) == 0)
q5 = (x ** 2 + x) / (x - 2) / ((x + 1) / (x ** 2 - 4))
chk('l15 s5', cancel(q5 - x * (x + 2)) == 0)
chk('l15 s5 wrongs', cancel((x - 2) / (x ** 2 + x) * (x + 1) / (x ** 2 - 4) - 1 / (x * (x + 2))) == 0 and cancel((x ** 2 + x) / (x - 2) * (x + 1) / (x ** 2 - 4) - x * (x + 1) ** 2 / ((x - 2) ** 2 * (x + 2))) == 0)
chk('l15 s7 value', ((x + 6) / (x + 2)).subs(x, 1) == R(7, 3) and solve(Eq((x + 6) / (x + 2), 3), x) == [0])
t7 = w(L15, 7)
chk('l15 s7 TOLERANCE: 2.33 (7/3 to 2 d.p., no precision asked) is refused', within(2.33, t7['answer'], t7['tol']))
chk('l15 s8', solve(x ** 2 + 3 * x + 2, x) == [-2, -1] and ((x + 3) / (x + 1)).subs(x, -2) == -1 and f15.subs(x, -3) == 0 and f15.subs(x, 0) == 3)
vals = [R(84 - 80, 80), R(84, 80) - 1, R(80, 84 - 80), R(80, 84) - 1]
chk('l15 s10', all(within(float(v), cell(L15, 10, i)['answer'], cell(L15, 10, i)['tol']) for i, v in enumerate(vals)))
chk('l15 q0', cancel((x ** 2 + 7 * x + 12) / (x ** 2 - 9) - (x + 4) / (x - 3)) == 0)
chk('l15 q1', cancel((x ** 2 - x) / (x ** 2 - 1) - x / (x + 1)) == 0)
chk('l15 q2', cancel(3 * x / (x + 1) * (x ** 2 - 1) / 6 - x * (x - 1) / 2) == 0)

# ---------------- l16 adding and solving
g16 = 6 / p + 6 / (p + 1)
rows = w(L16, 0)['rows']
chk('l16 s0 table', [c_['answer'] for c_ in rows[1][1:]] == [300, 200, 500] and [c_['answer'] for c_ in rows[2][1:]] == [200, 150, 350])
chk('l16 s1', set(solve(Eq(g16, 5), p)) == {2, R(-3, 5)} and w(L16, 1)['answer'] == -0.6 and g16.subs(p, R(3, 5)) == R(55, 4))
chk('l16 s2', R(5, 12) + R(7, 18) == R(29, 36) and cancel(1 / x + 1 / (x + 1) - (2 * x + 1) / (x * (x + 1))) == 0)
chk('l16 s3', cancel(3 / (x - 1) - 2 / (x + 2) - (x + 8) / ((x - 1) * (x + 2))) == 0)
chk('l16 s4', cancel(2 / (x ** 2 - 1) + 1 / (x + 1) - 1 / (x - 1)) == 0)
chk('l16 s5', expand(6 * (x + 1) + 6 * x - 5 * x * (x + 1)) == -(5 * x ** 2 - 7 * x - 6) and factor(5 * x ** 2 - 7 * x - 6) == (x - 2) * (5 * x + 3) and w(L16, 5)['answers'] == [2, -0.6])
chk('l16 s7 no solution', solve(Eq(x / (x - 2), 2 / (x - 2) + 3), x) == [] and simplify(2 / (x - 2) + 3 - x / (x - 2)) == 2)
chk('l16 s8', 12 * 18 == 216)
chk('l16 s9', R(1200, 500) == R(12, 5) and (2 * a * b / (a + b)).subs({a: 2, b: 3}) == R(12, 5) and round(500 / 1200, 4) == wrongs(w(L16, 9))['per-pound'])
chk('l16 q0', solve(Eq(4 / x + 1, 3), x) == [2] and R(4) / R(5, 3) == R(12, 5))
chk('l16 q2', cancel(2 / (x + 3) + 1 / (x - 3) - (3 * x - 3) / (x ** 2 - 9)) == 0)
chk('l16 q3', solve(Eq(2 * x / (x - 1), 2 / (x - 1) + x), x) == [2])

# ---------------- l17 division and the factor theorem
f = x ** 3 - 2 * x ** 2 - 5 * x + 6
chk('l17 s0', [f.subs(x, v) for v in (1, 2, 3, -2)] == [cell(L17, 0, i)['answer'] for i in range(4)] and f.subs(x, -3) == -24)
q, rem = div(f, x - 1, x)
chk('l17 s2', q == x ** 2 - x - 6 and rem == 0 and [cell(L17, 2, i)['answer'] for i in range(3)] == [1, -1, -6])
lab = L17['screens'][2]['canvas']['right']['params']['labels']
chk('l17 s2 grid cells add to f', expand(x ** 3 - x ** 2 - 6 * x - x ** 2 + x + 6 - f) == 0 and lab['c13'] == '$-6x$' and 200 + 10 + 40 + 2 == 252)
chk('l17 s3', div(f, x - 2, x) == (x ** 2 - 5, -4) and w(L17, 3)['answer'] == -4)
g = 2 * x ** 3 + 3 * x ** 2 - 4 * x + 5
q, rem = div(g, x + 2, x)
chk('l17 s4', Poly(q, x).all_coeffs() + [rem] == [cell(L17, 4, i)['answer'] for i in range(4)] and g.subs(x, 2) == 25)
chk('l17 s5', factor(x ** 3 - 7 * x + 6) == (x - 2) * (x - 1) * (x + 3))
pk = x ** 3 + k * x ** 2 - 4
chk('l17 s6', solve(pk.subs(x, 2), k) == [w(L17, 6)['answer']] and solve(pk.subs(x, -2), k) == [3] and expand((x - 2) * (x ** 2 + x + 2)) == pk.subs(k, -1))
chk('l17 s7', (x ** 3 - 7 * x + 6).subs(x, 3) == 12)
chk('l17 s8', factor(x ** 3 - 3 * x + 2) == (x - 1) ** 2 * (x + 2))
cub = 1000 * x ** 3 - 400 * x ** 2 - 480 * x - 576
chk('l17 s10', expand(8 * (5 * x - 6) * (25 * x ** 2 + 20 * x + 12) - cub) == 0 and discriminant(25 * x ** 2 + 20 * x + 12, x) == w(L17, 10)['answer'] and cub.subs(x, R(6, 5)) == 0)
chk('l17 q0', div(x ** 3 - 7 * x + 6, x - 1, x)[0] == x ** 2 + x - 6)
chk('l17 q1', len(real_roots(x ** 3 + x - 2)) == 1 and expand((x - 1) * (x ** 2 + x + 2)) == x ** 3 + x - 2)
fq = 2 * x ** 3 - x ** 2 + 3 * x - 4
chk('l17 q2', fq.subs(x, -1) == -10 and fq.subs(x, 1) == 0)
chk('l17 q3', factor(x ** 3 - 3 * x ** 2 + 4) == (x - 2) ** 2 * (x + 1) and (x ** 3 - 3 * x ** 2 + 4).subs(x, -2) == -16)
# claim: quiz q17-one-real-root, option "two": "The quadratic factor gives either two roots or none." A quadratic with
# discriminant 0 gives one, and the lesson's own s8 cubic (x-1)^2(x+2) has exactly two distinct real roots.
chk('l17 CLAIM q17 "either two roots or none" (x^2 - 2x + 1 has one; s8 cubic has two distinct roots)',
    len(set(real_roots(x ** 2 - 2 * x + 1))) != 1 and len(set(real_roots(x ** 3 - 3 * x + 2))) != 2)

# ---------------- l18 circles
pol = {q['id']: q['points'] for q in L18['screens'][0]['canvas']['state']['polygons']}
chk('l18 s0', shoelace(pol['s5']) == w(L18, 0)['answer'] == 9 + 16 and shoelace(pol['s3']) == 9 and shoelace(pol['s4']) == 16)
lat = [(i, j) for i in range(-6, 7) for j in range(-6, 7) if i * i + j * j == 25]
chk('l18 s1', len(lat) == w(L18, 1)['answer'] and len(L18['screens'][1]['explain']['canvas']['points']) == 12)
chk('l18 s3', sqrt((3 + 2) ** 2 + (13 - 1) ** 2) == w(L18, 3)['answer'] and round(float(sqrt(1 + 144)), 2) == wrongs(w(L18, 3))['minus-sign'])
chk('l18 s5', expand((x - 3) ** 2 + (y + 2) ** 2 - 25) == x ** 2 + y ** 2 - 6 * x + 4 * y - 12 and (0 - 3) ** 2 + (0 + 2) ** 2 == 13)
chk('l18 s6', expand((x + 2) ** 2 + (y - 5) ** 2 - 36 - (x ** 2 + y ** 2 + 4 * x - 10 * y - 7)) == 0 and w(L18, 6)['answer'] == 6)
tan = 3 * x + 4 * y - 26
chk('l18 s7', tan.subs({x: 6, y: 2}) == 0 and R(2 + 2, 6 - 3) * R(-3, 4) == -1 and len(solve([tan, (x - 3) ** 2 + (y + 2) ** 2 - 25], [x, y])) == 1)
chk('l18 s8', expand((x - 3) ** 2 + (y + 2) ** 2 - (13 - c) - (x ** 2 + y ** 2 - 6 * x + 4 * y + c)) == 0)
chk('l18 s10', within(float(sqrt(32)), w(L18, 10)['answer'], w(L18, 10)['tol']))
chk('l18 q2 q3', 9 + 9 == 18 and expand((x + 5) ** 2 + (y - 2) ** 2 - 9 - (x ** 2 + y ** 2 + 10 * x - 4 * y + 20)) == 0)

# ---------------- l19 line meets curve
circ = x ** 2 + y ** 2 - 25
qk = expand(circ.subs(y, x + k))
chk('l19 s2 general discriminant', expand(discriminant(qk, x) - (200 - 4 * k ** 2)) == 0 and qk.subs(k, 8) == 2 * x ** 2 + 16 * x + 39 and discriminant(qk.subs(k, 8), x) == w(L19, 2)['answer'])
chk('l19 s1', sorted(solve(circ.subs(y, x + 1), x)) == sorted(w(L19, 1)['answers']))
chk('l19 s3', discriminant(x ** 2 - 2 * x - k, x) == 4 + 4 * k and w(L19, 3)['answer'] == -1)
chk('l19 s4', expand(16 * circ.subs(y, (25 - 3 * x) / 4)) == 25 * x ** 2 - 150 * x + 225 and factor(25 * x ** 2 - 150 * x + 225) == 25 * (x - 3) ** 2)
chk('l19 s5', sqrt(50) == 5 * sqrt(2) and 7 < float(sqrt(50)) < 7.5)
chk('l19 s8', expand(discriminant(x ** 2 - m * x - c, x) - (m ** 2 + 4 * c)) == 0)
be = expand(p * (500 - 10 * p) - (100 * p + 3000))
chk('l19 s9', be == -10 * p ** 2 + 400 * p - 3000 and sorted(solve(be, p)) == w(L19, 9)['answers'])
beF = expand(p * (500 - 10 * p) - (100 * p + F))
chk('l19 s10', solve(discriminant(expand(beF / -10), p), F) == [w(L19, 10)['answer']] and solve(beF.subs(F, 4000), p) == [20] and (p * (500 - 10 * p)).subs(p, 20) == 6000)
chk('l19 q0', sorted(solve(Eq(x ** 2 + 3 * x, x), x)) == [-2, 0])
chk('l19 q2', solve(discriminant(x ** 2 + 1 - 4 * x - k, x), k) == [-3])
chk('l19 q3', set(solve([y - 2 * x + 1, x ** 2 + y ** 2 - 2], [x, y])) == {(1, 1), (R(-1, 5), R(-7, 5))})
# slider captions: floating point in the F caption (1600 - 0.4*F) at every stop
stops = [2000 + 250 * i for i in range(13)]
chk('l19 s10 caption shows a clean number at every slider stop', all(len(repr(1600 - 0.4 * s_)) <= 7 for s_ in stops))

# ---------------- review-4
it = {i['id']: i for i in RV['items']}
chk('r4 surd', (sqrt(48) + sqrt(27)) / sqrt(3) == it['r4-surd-sum']['widget']['answer'] and sqrt(75) == 5 * sqrt(3))
chk('r4 conj', simplify(4 / (sqrt(5) - 1) - (sqrt(5) + 1)) == 0 and round(float(sqrt(5) + 1), 3) == 3.236)
chk('r4 cancel', cancel((x ** 2 - x - 6) / (x ** 2 - 4) - (x - 3) / (x - 2)) == 0)
chk('r4 add', cancel(2 / x + 3 / (x - 1) - (5 * x - 2) / (x * (x - 1))) == 0)
chk('r4 reject', solve(Eq(3 / (x - 1), 1 + 6 / (x ** 2 - 1)), x) == [it['r4-reject']['widget']['answer']])
fr = x ** 3 + 2 * x ** 2 - 5 * x + 1
chk('r4 remainder', fr.subs(x, 2) == it['r4-remainder']['widget']['answer'] and fr.subs(x, -2) == 11)
chk('r4 cubic', factor(x ** 3 - 4 * x ** 2 + x + 6) == (x - 3) * (x - 2) * (x + 1))
chk('r4 circle', expand((x + 4) ** 2 + (y - 1) ** 2 - 25 - (x ** 2 + y ** 2 + 8 * x - 2 * y - 8)) == 0)
chk('r4 distance', sqrt(6 ** 2 + 8 ** 2) == it['r4-distance']['widget']['answer'])
chk('r4 tangent', solve(discriminant(x ** 2 + 3 - x - k, x), k) == [R(11, 4)] and it['r4-tangent-k']['widget']['answer'] == 2.75 and solve(1 + 4 * (3 - k), k) == [R(13, 4)])

# ---------------- homework-4
it = {i['id']: i for i in HW['items']}
e = radsimp((5 + sqrt(3)) / (2 - sqrt(3)))
chk('hw surd', simplify(e - (13 + 7 * sqrt(3))) == 0 and round(float(e), 2) == 25.12 and round(13 / 7, 3) == 1.857)
chk('hw fraction eq', solve(Eq(x / (x - 3) - 2 / (x + 1), 12 / (x ** 2 - 2 * x - 3)), x) == [it['hw4-fraction-equation']['widget']['answer']])
chk('hw cubic', factor(2 * x ** 3 + x ** 2 - 13 * x + 6) == (x - 2) * (x + 3) * (2 * x - 1))
pp = x ** 3 + a * x ** 2 + b * x - 6
chk('hw two factors', solve([pp.subs(x, -1), pp.subs(x, 2)], [a, b]) == {a: 2, b: -5} and factor(pp.subs({a: 2, b: -5})) == (x - 2) * (x + 1) * (x + 3))
pts = solve([y - x - 2, x ** 2 + y ** 2 - 10], [x, y])
chk('hw circle line', set(pts) == {(1, 3), (-3, -1)} and round(float(sqrt(32)), 2) == 5.66)
chk('hw tangent', expand(discriminant(expand((x ** 2 + y ** 2 - 20).subs(y, 2 * x + k)), x) - (400 - 4 * k ** 2)) == 0)
chk('hw proof', expand(discriminant(expand((x ** 2 + y ** 2 - r ** 2).subs(y, m * x + c)), x) - 4 * (r ** 2 * (1 + m ** 2) - c ** 2)) == 0)
lhs = (x ** 2 - 9) / (x - 3) + (x + 6) / (x + 2)
chk('hw longform', sorted(solve(Eq(lhs, 7), x)) == [-1, 2] and lhs.subs(x, 1) == R(19, 3) and lhs.subs(x, -5) == R(-7, 3) and sorted(solve(x ** 2 + 6 * x + 5, x)) == [-5, -1])
chk('hw rubric', sum(q['points'] for q in it['hw4-find-the-errors']['rubric']) == 10)

print(f'read-numbers: {n_ok} of {n_ok + n_bad} checks pass')
sys.exit(1 if n_bad else 0)
