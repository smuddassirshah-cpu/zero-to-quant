"""Numbers for the fixes the review proposes, each computed twice. Run from the repo root; exit 0 = all hold."""
import json
import math
import sys

import sympy as sp

R = sp.Rational
x, n, k, t = sp.symbols('x n k t', positive=True)
bad = 0


def ok(label, cond):
    global bad
    print(('ok   ' if cond else 'FAIL ') + label)
    bad += 0 if cond else 1


def within(v, a, tol):
    return abs(v - a) <= tol + 1e-12


def widget(c, m, item, i):
    d = json.load(open(f'app/content/courses/{c}/problems-{m}.json'))
    return next(z for z in d['items'] if z['id'] == item)['parts'][i - 1]['widget']


# Findings 1 to 4: widened bands take the rounded route and still refuse every wrong[] value.
for c, m, item, i, tol, route in [
    ('limits', 2, 'p-perpetuity-slope', 2, 1, -2040),
    ('integrals', 3, 'p-signal-average', 4, 0.001, 2.968),
    ('integrals', 3, 'p-log-return', 1, 0.0001, -0.0720),
    ('integrals', 2, 'p-turnover-decay', 3, 0.01, 13.84),
]:
    w = widget(c, m, item, i)
    ok(f'{item} part {i}: tol {tol} takes {route}', within(route, w['answer'], tol))
    ok(f'{item} part {i}: tol {tol} still refuses every wrong value',
       all(not within(z['value'], w['answer'], tol) for z in w['wrong']))
ok('perpetuity: penny route is -2040', round((round(5 / 0.049, 2) - 100) / -0.001) == -2040)
ok('signal: printed working gives 2.9676', abs(2 * (1.2131 + 0.2707) - 2.9676) < 1e-9)
ok('log-return: printed working gives -0.07195', abs(0.5 * (-0.3466 + 0.2027) + 0.07195) < 1e-9)
ok('turnover: e^-2 to 4 places gives 13.8352', abs(16 - 16 * 0.1353 - 13.8352) < 1e-9)

# Finding 5: p-relative-strength part 3, a `decimal` wrong entry at 0.0002 (typed 0.02 beside the % unit).
w = widget('limits', 3, 'p-relative-strength', 3)
ok('relative-strength 3: 0.02 typed beside % is read as 0.0002 and refused', not within(0.02 / 100, w['answer'], w['tol']['abs']))
ok('relative-strength 3: 0.0002 with tol 0.00001 is clear of the answer and of every wrong value',
   all(abs(0.0002 - z['value']) > z['tol']['abs'] + 0.00001 for z in w['wrong']) and abs(0.0002 - w['answer']) > 0.0005)

# Finding 7: p-falling-parabola on a new curve, f(x) = 12 - 3x^2 on [0, 2], n = 4 strips of 0.5.
f = 12 - 3 * x**2
R4 = sum(f.subs(x, R(i, 2)) for i in range(1, 5)) / 2
L4 = sum(f.subs(x, R(i, 2)) for i in range(0, 4)) / 2
ok('new curve: heights 11.25, 9, 5.25, 0 sum 25.5', [f.subs(x, R(i, 2)) for i in range(1, 5)] == [R(45, 4), 9, R(21, 4), 0])
ok('new curve: R_4 = 12.75, L_4 = 18.75', (R4, L4) == (R(51, 4), R(75, 4)))
ok('new curve: gap rule 12 * 2/4 = 6', L4 - R4 == 12 * R(2, 4) == 6)
ok('new curve: part 2 wrongs 6.75 and 15.75', (R4 - 6, R4 + 12 * R(1, 4)) == (R(27, 4), R(63, 4)))
ok('new curve: gap 24/n <= 0.1 first at 240; 12/n at 120; strict 241',
   (next(v for v in range(1, 999) if R(24, v) <= R(1, 10)), next(v for v in range(1, 999) if R(12, v) <= R(1, 10)),
    next(v for v in range(1, 999) if R(24, v) < R(1, 10))) == (240, 120, 241))
Rn = sp.simplify(sp.summation((12 - 12 * k**2 / n**2) * 2 / n, (k, 1, n)))
ok('new curve: R_n = 16 - 12/n - 4/n^2 = 24 - 4(n+1)(2n+1)/n^2',
   sp.simplify(Rn - (16 - 12 / n - 4 / n**2)) == 0 and sp.simplify(Rn - (24 - 4 * (n + 1) * (2 * n + 1) / n**2)) == 0 and Rn.subs(n, 4) == R4)
Ln = sp.simplify(sp.summation((12 - 12 * k**2 / n**2) * 2 / n, (k, 0, n - 1)))
ok('new curve: L_n = 16 + 12/n - 4/n^2', sp.simplify(Ln - (16 + 12 / n - 4 / n**2)) == 0)
ok('new curve: heights only 12n - 2(n+1)(2n+1)/n',
   sp.simplify(sp.summation(12 - 12 * k**2 / n**2, (k, 1, n)) - (12 * n - 2 * (n + 1) * (2 * n + 1) / n)) == 0)
ok('new curve: area 16 by limit and by antiderivative', sp.limit(Rn, n, sp.oo) == 16 == sp.integrate(f, (x, 0, 2)))
ok('new curve: "12 counted once" tends to 4', sp.limit(12 - 4 * (n + 1) * (2 * n + 1) / n**2, n, sp.oo) == 4)

# Finding 8: p-relative-strength on new numbers, P = 30e^{0.07t}, I = 1500e^{0.05t}.
P, I = 30 * sp.exp(R(7, 100) * t), 1500 * sp.exp(R(5, 100) * t)
Rt = P / I
dP0, dI0 = sp.diff(P, t).subs(t, 0), sp.diff(I, t).subs(t, 0)
ok('new ratio: R(0) = 0.02, P\'(0) = 2.1, I\'(0) = 75', (Rt.subs(t, 0), dP0, dI0) == (R(1, 50), R(21, 10), 75))
dR0 = sp.diff(Rt, t).subs(t, 0)
ok('new ratio: R\'(0) = 900 / 2,250,000 = 0.0004', dR0 == R(900, 2250000) == R(1, 2500)
   and abs(float(dR0) - (2.1 * 1500 - 30 * 75) / 1500**2) < 1e-12)
ok('new ratio: wrongs 0.6, 0.028, 0.019', (R(900, 1500), dP0 / dI0, R(30 * 1500 - 30 * 75, 1500**2)) == (R(3, 5), R(7, 250), R(19, 1000)))
ok('new ratio: growth 2% a year; added 12%; share alone 7%', dR0 / Rt.subs(t, 0) == R(1, 50) and sp.simplify(sp.diff(sp.log(Rt), t)) == R(1, 50))

# Finding 10: shorter correct option for p-inventory-penalty part 2.
new = '$C$ is continuous, with a corner: slope 4 from the left, 3 from the right'
w = widget('limits', 2, 'p-inventory-penalty', 2)
others = [len(o['text']) for o in w['options'] if not o.get('correct')]
ok(f'penalty option: new length {len(new)} against others {others}', len(new) <= 1.25 * max(others))
print('proposed.py:', 'all hold' if not bad else f'{bad} FAILED')
sys.exit(1 if bad else 0)
