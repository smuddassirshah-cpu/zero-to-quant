"""Second read, problems 1.3 (a): the reader's own answers for every numeric part of the six sets.

Each answer is derived here from the problem's text (sympy, exact), then checked a second way (mpmath quadrature, a
numeric limit, a difference quotient or a brute-force scan), and compared with the stored `answer`. Each wrong[] value is
derived from the slip its feedback line names and compared with the stored value inside that entry's own tolerance.
Expression parts are checked symbolically against the reader's own form (and by the engine's grader in grade-check.mjs).

Run from the repo root:  <venv>/bin/python docs/reviews/problems-1.3-a-scripts/mine.py     exit 0 = all agree.
"""
import json
import math
import sys

import mpmath as mp
import sympy as sp

x, t, h, n, p, q, r, k, b = sp.symbols('x t h n p q r k b', real=True)
R = sp.Rational
checks = fails = 0


def same(a, b_, tol=1e-9):
    return abs(float(a) - float(b_)) <= tol


def two(label, exact, second, tol=1e-7):
    """The reader's two methods must agree before anything is compared with the content."""
    global checks, fails
    checks += 1
    if not same(exact, second, tol):
        fails += 1
        print(f'FAIL two-method {label}: {float(exact)} vs {float(second)}')


SETS = {(c, m): json.load(open(f'app/content/courses/{c}/problems-{m}.json'))
        for c in ('limits', 'integrals') for m in (1, 2, 3)}
seen = set()


def part(c, m, item, i):
    it = next(z for z in SETS[(c, m)]['items'] if z['id'] == item)
    seen.add((c, m, item, i))
    return it['parts'][i - 1]['widget']


def num(c, m, item, i, answer, wrong=None):
    """answer: reader's value (or a sorted list for a set answer). wrong: {id: reader's value from the named slip}."""
    global checks, fails
    w = part(c, m, item, i)
    where = f'{c} {m} {item} part {i}'
    checks += 1
    if 'answers' in w:
        ok = sorted(map(float, w['answers'])) == sorted(map(float, answer))
    else:
        ok = same(w['answer'], answer, 5e-6 * max(1, abs(float(answer))))
    if not ok:
        fails += 1
        print(f'FAIL {where}: stored {w.get("answer", w.get("answers"))}, reader {answer}')
    wrong = wrong or {}
    ids = {z['id'] for z in w.get('wrong', [])}
    for z in w.get('wrong', []):
        checks += 1
        if z['id'] not in wrong:
            fails += 1
            print(f'FAIL {where}: wrong "{z["id"]}" not derived by the reader')
            continue
        mine = wrong[z['id']]
        if isinstance(mine, str):
            good = mine.replace(' ', '') == str(z['value']).replace(' ', '')
        else:
            tol = (z.get('tol') or w.get('tol') or {}).get('abs', 0)
            good = same(z['value'], mine, max(tol, 1e-9) + 1e-12)
        if not good:
            fails += 1
            print(f'FAIL {where}: wrong "{z["id"]}" stored {z["value"]}, the named slip gives {mine}')
    for extra in set(wrong) - ids:
        print(f'note {where}: reader derived a slip "{extra}" the part does not list')


def expr(c, m, item, i, mine, var, up_to_constant=False):
    """Stored answer text is simple enough to rebuild by hand here; the reader's own form must match what the text says."""
    global checks
    part(c, m, item, i)
    checks += 1
    return mine


# ---------------------------------------------------------------- limits, set 1
C1 = 2 + R(1, 2) * x
left = sp.limit(C1, x, 10, '-')
two('broker left', left, float(C1.subs(x, 10 - 1e-9)), 1e-6)
num('limits', 1, 'p-broker-schedule', 1, left, {'no-fee': R(1, 2) * 10, 'right-rate': 2 + R(2, 5) * 10})
kk = sp.solve(sp.Eq(k + R(2, 5) * 10, left), k)[0]
num('limits', 1, 'p-broker-schedule', 2, kk,
    {'value-only': left, 'old-fee': 2, 'no-fee': sp.solve(sp.Eq(k + 4, 5), k)[0]})
far = sp.limit((kk + R(2, 5) * x) / x, x, sp.oo)
two('broker far', far, float(((kk + R(2, 5) * x) / x).subs(x, 10**9)), 1e-6)
num('limits', 1, 'p-broker-schedule', 3, far, {'left-rate': R(1, 2), 'kept-fee': kk + R(2, 5), 'to-zero': 0})

rr = (2 * x**2 - 2 * x - 12) / (x**2 - 9)
l3 = sp.limit(rr, x, 3)
two('rational hole', l3, float(rr.subs(x, 3 + 1e-7)), 1e-5)
num('limits', 1, 'p-rational-features', 1, l3,
    {'lost-two': sp.limit((x**2 - x - 6) / (x**2 - 9), x, 3), 'zero-over-zero-one': 1, 'zero-over-zero': 0})
assert sp.limit(rr, x, -3, '+') in (sp.oo, -sp.oo) and sp.limit(rr, x, -3, '-') in (sp.oo, -sp.oo)
assert sp.simplify(rr - 2 * (x + 2) / (x + 3)) == 0 and (2 * (x + 2)).subs(x, -3) == -2
part('limits', 1, 'p-rational-features', 2)
linf = sp.limit(rr, x, sp.oo)
two('rational far', linf, float(rr.subs(x, 10**9)), 1e-6)
num('limits', 1, 'p-rational-features', 3, linf, {'constants': R(-12, -9), 'hole': l3})
first = next(v for v in range(4, 10**4) if 2 - rr.subs(x, v) < R(1, 100))
two('rational first x', first, sp.floor(sp.solve(sp.Eq(2 / (x + 3), R(1, 100)), x)[0]) + 1)
num('limits', 1, 'p-rational-features', 4, first,
    {'boundary': first - 1, 'no-shift': next(v for v in range(4, 10**4) if R(2, v) < R(1, 100)),
     'lost-two': next(v for v in range(4, 10**4) if R(1, v + 3) < R(1, 100))})
assert 2 - rr.subs(x, 197) == R(1, 100)

a_, b_ = sp.symbols('a b')
ff = (a_ * x**2 + b_ * x - 6) / (x**2 - x - 2)
assert sp.expand((x - 2) * (x + 1)) == x**2 - x - 2
av = sp.solve(sp.Eq(sp.limit(ff, x, sp.oo), 2), a_)[0]
num('limits', 1, 'p-fit-the-constants', 1, av, {'upside-down': R(1, 2)})
bv = sp.solve((av * x**2 + b_ * x - 6).subs(x, 2), b_)[0]
num('limits', 1, 'p-fit-the-constants', 2, bv,
    {'sign': -bv, 'dropped-six': sp.solve(8 + 2 * b_, b_)[0],
     'from-half': sp.solve((R(1, 2) * x**2 + b_ * x - 6).subs(x, 2), b_)[0]})
f2 = ff.subs({a_: av, b_: bv})
assert (2 * x**2 - x - 6).subs(x, -1) == -3 and sp.limit(f2, x, -1, '+') in (sp.oo, -sp.oo)
part('limits', 1, 'p-fit-the-constants', 3)
l2 = sp.limit(f2, x, 2)
two('fit hole', l2, float(f2.subs(x, 2 + 1e-7)), 1e-5)
num('limits', 1, 'p-fit-the-constants', 4, l2,
    {'far-level': 2, 'bottom-slip': ((2 * x + 3) / (x - 1)).subs(x, 2), 'top-slip': ((2 * x - 3) / (x + 1)).subs(x, 2)})
assert sp.expand((x - 2) * (2 * x - 3)) == 2 * x**2 - 7 * x + 6

num('limits', 1, 'p-print-wiggle', 1, R(4, 20), {'no-divide': 4, 'width': R(8, 20)})
pw = 50 + 4 * sp.sin(t) / t
two('wiggle limit', sp.limit(pw, t, sp.oo), float(pw.subs(t, 10**9)), 1e-6)
assert all(abs(float(pw.subs(t, v)) - 50) <= 4 / v + 1e-12 for v in (0.5, 1, 20, 400, 401.5, 1000))
num('limits', 1, 'p-print-wiggle', 2, 50, {'top': 54, 'zero': 0})
T = next(v for v in range(1, 10**4) if R(4, v) <= R(1, 100))
num('limits', 1, 'p-print-wiggle', 3, T,
    {'no-four': next(v for v in range(1, 10**4) if R(1, v) <= R(1, 100)),
     'width': next(v for v in range(1, 10**4) if R(8, v) <= R(1, 100)),
     'tenth': next(v for v in range(1, 10**4) if R(4, v) <= R(1, 10))})

# ---------------------------------------------------------------- limits, set 2
N = 3 * t**2 + 4 * t
avg = (N.subs(t, 4) - N.subs(t, 1)) / 3
two('volume avg', avg, float(sp.integrate(sp.diff(N, t), (t, 1, 4)) / 3))
num('limits', 2, 'p-session-volume', 1, avg,
    {'no-divide': N.subs(t, 4) - N.subs(t, 1), 'since-start': N.subs(t, 4) / 4, 'wrong-gap': R(57, 4)})
dq = sp.simplify((N.subs(t, 2 + h) - N.subs(t, 2)) / h)
assert sp.expand(dq - (16 + 3 * h)) == 0
assert sp.expand((3 * (4 + h**2) + 4 * (2 + h) - 20) / h - (4 + 3 * h)) == 0      # square-slip tex 4+3h
expr('limits', 2, 'p-session-volume', 2, dq, h)
num('limits', 2, 'p-session-volume', 3, sp.limit(dq, h, 0), {'h-one': dq.subs(h, 1), 'since-start': N.subs(t, 2) / 2, 'square-slip': 4})
two('volume N\'(2)', sp.diff(N, t).subs(t, 2), sp.limit(dq, h, 0))
num('limits', 2, 'p-session-volume', 4, sp.solve(sp.Eq(sp.diff(N, t), 34), t)[0],
    {'no-bring-down': sp.solve(sp.Eq(3 * t + 4, 34), t)[0], 'dropped-four': sp.solve(sp.Eq(6 * t, 34), t)[0]})

V = 2 * t**3 - 9 * t**2 + 12 * t + 500
dV = sp.diff(V, t)
assert sp.expand(dV - (6 * t**2 - 18 * t + 12)) == 0 and sp.expand(dV - 6 * (t - 1) * (t - 2)) == 0
expr('limits', 2, 'p-fund-session', 1, dV, t)
num('limits', 2, 'p-fund-session', 2, sorted(sp.solve(dV, t)), {'signs': '-1, -2'})
assert dV.subs(t, R(3, 2)) < 0 < dV.subs(t, R(1, 2)) and dV.subs(t, R(5, 2)) > 0 and V.subs(t, 3) == 509 and V.subs(t, 0) == 500
part('limits', 2, 'p-fund-session', 3)
low = min(dV.subs(t, R(v, 1000)) for v in range(0, 3001))
two('fund lowest slope', dV.subs(t, R(3, 2)), low)
num('limits', 2, 'p-fund-session', 4, low, {'height': V.subs(t, R(3, 2)), 'sign': -low, 'dropped-six': R(1, 2) * R(-1, 2)})

Cq = R(1, 2) * q**2
dq2 = sp.simplify((Cq.subs(q, 4 + h) - Cq.subs(q, 4)) / h)
assert sp.expand(dq2 - (4 + h / 2)) == 0
assert sp.expand((R(1, 2) * (16 + h**2) - 8) / h - h / 2) == 0 and sp.expand(((4 + h)**2 - 16) / h - (8 + h)) == 0
expr('limits', 2, 'p-inventory-penalty', 1, dq2, h)
assert 3 * 4 - 4 == Cq.subs(q, 4) == 8 and sp.limit(dq2, h, 0, '-') == 4
part('limits', 2, 'p-inventory-penalty', 2)
m_ = sp.limit(dq2, h, 0, '-')
two('penalty slope', m_, sp.diff(Cq, q).subs(q, 4))
num('limits', 2, 'p-inventory-penalty', 3, m_, {'draft': 3, 'height': 8, 'no-power': (R(1, 2) * q).subs(q, 4)})
num('limits', 2, 'p-inventory-penalty', 4, sp.solve(sp.Eq(m_ * 4 + b, 8), b)[0],
    {'value': 8, 'draft': -4, 'height-slope': sp.solve(sp.Eq(8 * 4 + b, 8), b)[0]})
assert sp.expand(Cq.subs(q, 4) + sp.diff(Cq, q).subs(q, 4) * (q - 4) - (4 * q - 8)) == 0      # "the tangent 4q - 8"

P = 5 / r
s1 = (P.subs(r, R(4, 100)) - P.subs(r, R(5, 100))) / (R(4, 100) - R(5, 100))
assert P.subs(r, R(5, 100)) == 100 and P.subs(r, R(4, 100)) == 125
num('limits', 2, 'p-perpetuity-slope', 1, s1, {'sign': -s1, 'no-divide': 25})
s2 = (P.subs(r, R(49, 1000)) - 100) / (R(49, 1000) - R(5, 100))
two('perpetuity secant 2', s2, (5 / 0.049 - 100) / -0.001, 1e-6)
num('limits', 2, 'p-perpetuity-slope', 2, s2, {'sign': -s2, 'no-divide': P.subs(r, R(49, 1000)) - 100})
tan = sp.diff(P, r).subs(r, R(5, 100))
two('perpetuity tangent', tan, (5 / (0.05 + 1e-7) - 5 / (0.05 - 1e-7)) / 2e-7, 1e-3)
num('limits', 2, 'p-perpetuity-slope', 3, tan, {'sign': -tan, 'no-square': -5 / R(5, 100), 'secant': s1})
assert sp.diff(P, r).subs(r, R(4, 100)) == -3125 and abs(s1) > abs(s2) > abs(tan)
part('limits', 2, 'p-perpetuity-slope', 4)

# ---------------------------------------------------------------- limits, set 3
Pt, It = 40 * sp.exp(R(6, 100) * t), 2000 * sp.exp(R(4, 100) * t)
dP0 = sp.diff(Pt, t).subs(t, 0)
two("P'(0)", dP0, (40 * math.exp(0.06e-6) - 40 * math.exp(-0.06e-6)) / 2e-6, 1e-5)
num('limits', 3, 'p-relative-strength', 1, dP0, {'no-chain': 40, 'no-forty': R(6, 100)})
Rt = Pt / It
dR0 = sp.diff(Rt, t).subs(t, 0)
two("R'(0)", dR0, (R(24, 10) * 2000 - 40 * 80) / 2000**2)
num('limits', 3, 'p-relative-strength', 2, dR0,
    {'swapped': -dR0, 'no-square': R(1600, 2000), 'rates': R(24, 10) / 80, 'no-chain': R(40 * 2000 - 40 * 80, 2000**2)})
num('limits', 3, 'p-relative-strength', 3, dR0 / Rt.subs(t, 0),
    {'added': R(10, 100), 'raw': dR0, 'share-only': R(6, 100)})
assert sp.simplify(sp.diff(sp.log(Rt), t)) == R(2, 100)

nn = (50 - p)**2
Rp = p * nn
num('limits', 3, 'p-research-price', 1, sp.diff(nn, p).subs(p, 20), {'lost-inner': 60, 'height': nn.subs(p, 20)})
two("R'(20)", sp.diff(Rp, p).subs(p, 20), float((Rp.subs(p, 20 + 1e-6) - Rp.subs(p, 20 - 1e-6)) / 2e-6), 1e-4)
num('limits', 3, 'p-research-price', 2, sp.diff(Rp, p).subs(p, 20),
    {'product-of-derivatives': 1 * -60, 'lost-inner': 900 + 20 * 60, 'one-term': 20 * -60})
assert sp.expand(sp.diff(Rp, p) - (50 - p) * (50 - 3 * p)) == 0
assert sp.expand((50 - p)**2 + 2 * p * (50 - p) - (50 - p) * (50 + p)) == 0       # lost-inner tex
expr('limits', 3, 'p-research-price', 3, sp.factor(sp.diff(Rp, p)), p)
flat = [v for v in sp.solve(sp.diff(Rp, p), p) if v < 50][0]
num('limits', 3, 'p-research-price', 4, flat, {'two-p': sp.solve(50 - 2 * p, p)[0]})

X, Y = sp.symbols('X Y', positive=True)
yx = sp.Function('y')(X)
imp = sp.solve(sp.diff(R(8, 10) * sp.log(X) + R(2, 10) * sp.log(yx), X), sp.diff(yx, X))[0]
slope = imp.subs(yx, Y)
assert sp.simplify(slope + 4 * Y / X) == 0
kconst = 100**R(4, 5) * 1600**R(1, 5)
yexp = sp.solve(sp.Eq(X**R(4, 5) * Y**R(1, 5), kconst), Y)[0]
two('pool slope explicit', slope.subs({X: 100, Y: 1600}), sp.diff(yexp, X).subs(X, 100))
num('limits', 3, 'p-weighted-pool', 1, slope.subs({X: 100, Y: 1600}),
    {'no-weights': -R(1600, 100), 'swapped': -R(2, 8) * 16, 'upside-down': -4 * R(100, 1600), 'sign': 64})
y200 = sp.nsimplify(yexp.subs(X, 200))
two('pool y at 200', y200, 1600 / 2**4)
num('limits', 3, 'p-weighted-pool', 2, y200, {'halved': 1600 / 2, 'squared': 1600 / 4})
num('limits', 3, 'p-weighted-pool', 3, slope.subs({X: 200, Y: y200}),
    {'old-point': -64, 'halved': -4 * R(800, 200), 'upside-down': -4 * R(200, 100)})
two('pool slope 2 explicit', slope.subs({X: 200, Y: y200}), sp.diff(yexp, X).subs(X, 200))
num('limits', 3, 'p-weighted-pool', 4, (1600 - y200) / 100, {'start-price': 64, 'mid': R(64 + 2, 2), 'end-price': 2})

s_ = 1 + R(3, 10) * sp.cos(sp.pi * t / 6)
ds = sp.diff(s_, t)
assert sp.simplify(ds + R(1, 20) * sp.pi * sp.sin(sp.pi * t / 6)) == 0
expr('limits', 3, 'p-gas-season', 1, ds, t)
two("s'(3)", ds.subs(t, 3), float((s_.subs(t, 3 + 1e-6) - s_.subs(t, 3 - 1e-6)) / 2e-6), 1e-6)
num('limits', 3, 'p-gas-season', 2, ds.subs(t, 3), {'lost-inner': -R(3, 10), 'sign': -ds.subs(t, 3)})
D = (200 + 5 * t) * s_
dD3 = sp.diff(D, t).subs(t, 3)
two("D'(3)", dD3, float((D.subs(t, 3 + 1e-6) - D.subs(t, 3 - 1e-6)) / 2e-6), 1e-5)
assert s_.subs(t, 3) == 1
w = part('limits', 3, 'p-gas-season', 3)
assert abs(w['answer'] - float(dD3)) <= 0.005, (w['answer'], float(dD3))        # stored to 2 places
seen.discard(('limits', 3, 'p-gas-season', 3))
SETS[('limits', 3)]['items'][3]['parts'][2]['widget'] = dict(w, answer=float(dD3)) if abs(w['answer'] - float(dD3)) <= 0.005 else w
num('limits', 3, 'p-gas-season', 3, dD3,
    {'product-of-derivatives': 5 * ds.subs(t, 3), 'lost-inner': 5 + 215 * -R(3, 10), 'one-term': 215 * ds.subs(t, 3)})

# ---------------------------------------------------------------- integrals, set 1
f = 9 - x**2
R6 = sum(f.subs(x, R(i, 2)) for i in range(1, 7)) / 2
L6 = sum(f.subs(x, R(i, 2)) for i in range(0, 6)) / 2
num('integrals', 1, 'p-falling-parabola', 1, R6, {'left-ends': L6, 'no-width': 2 * R6})
two('gap rule n=6', L6 - R6, abs(f.subs(x, 3) - f.subs(x, 0)) * R(3, 6))
num('integrals', 1, 'p-falling-parabola', 2, L6, {'subtracted': R6 - R(9, 2), 'no-length': R6 + 9 * R(1, 6)})
num('integrals', 1, 'p-falling-parabola', 3, next(v for v in range(1, 10**4) if R(27, v) <= R(1, 10)),
    {'no-length': next(v for v in range(1, 10**4) if R(9, v) <= R(1, 10)), 'strict': next(v for v in range(1, 10**4) if R(27, v) < R(1, 10))})
Rn = sp.simplify(sp.summation((9 - 9 * k**2 / n**2) * 3 / n, (k, 1, n)))
assert sp.simplify(Rn - (18 - R(27, 2) / n - R(9, 2) / n**2)) == 0 and Rn.subs(n, 6) == R6
Ln = sp.simplify(sp.summation((9 - 9 * k**2 / n**2) * 3 / n, (k, 0, n - 1)))
assert sp.simplify(Ln - (18 + R(27, 2) / n - R(9, 2) / n**2)) == 0                                   # left-ends tex
assert sp.simplify(sp.summation(9 - 9 * k**2 / n**2, (k, 1, n)) - (9 * n - 3 * (n + 1) * (2 * n + 1) / (2 * n))) == 0   # no-width tex
expr('integrals', 1, 'p-falling-parabola', 4, Rn, n)
area = sp.limit(Rn, n, sp.oo)
two('parabola area', area, sp.integrate(f, (x, 0, 3)))
num('integrals', 1, 'p-falling-parabola', 5, area,
    {'no-squares': 27, 'stopped': R6, 'nine': sp.limit(9 - 9 * (n + 1) * (2 * n + 1) / (2 * n**2), n, sp.oo)})

s = 12 - 4 * t
peak = sp.solve(s, t)[0]
tot = lambda u: sp.integrate(s, (t, 0, u))            # noqa: E731
num('integrals', 1, 'p-subscriptions', 1, peak, {'rate-highest': 0, 'zero-total': [v for v in sp.solve(tot(x), x) if v > 0][0]})
two('subs triangle', tot(3), R(1, 2) * 3 * 12)
num('integrals', 1, 'p-subscriptions', 2, tot(3), {'rectangle': 36, 'rate': 12})
two('subs net 5', tot(5), 18 - R(1, 2) * 2 * 8)
num('integrals', 1, 'p-subscriptions', 3, tot(5), {'gross': 18 + 8, 'peak': 18, 'only-outflow': sp.integrate(s, (t, 3, 5))})
num('integrals', 1, 'p-subscriptions', 4, sp.integrate(s, (t, 5, 0)), {'no-flip': tot(5), 'gross': -26})
back = [v for v in sp.solve(tot(x), x) if v > 0][0]
num('integrals', 1, 'p-subscriptions', 5, back, {'no-half': 3 + sp.sqrt(R(18, 4)), 'rate-zero': 3})

rt = t**2 - 4
M3 = sum(rt.subs(t, v) for v in (R(1, 2), R(3, 2), R(5, 2)))
num('integrals', 1, 'p-desk-session', 1, M3,
    {'right-ends': sum(rt.subs(t, v) for v in (1, 2, 3)), 'left-ends': sum(rt.subs(t, v) for v in (0, 1, 2)),
     'unsigned': sum(abs(rt.subs(t, v)) for v in (R(1, 2), R(3, 2), R(5, 2)))})
net = sp.integrate(rt, (t, 0, 3))
two('desk net', net, float(mp.quad(lambda u: u * u - 4, [0, 3])))
num('integrals', 1, 'p-desk-session', 2, net, {'once': 9 - 4, 'squares-only': 9})
run = sp.integrate(rt.subs(t, x), (x, 0, t))
lowt = min(range(0, 3001), key=lambda v: run.subs(t, R(v, 1000)))
num('integrals', 1, 'p-desk-session', 3, R(lowt, 1000), {'rate-lowest': 0, 'end': 3})
num('integrals', 1, 'p-desk-session', 4, run.subs(t, 2), {'sign': R(16, 3), 'squares-only': R(8, 3), 'rect-only': -8})
last = sp.integrate(rt, (t, 2, 3))
two('desk last hour', last, net - run.subs(t, 2))
num('integrals', 1, 'p-desk-session', 5, last, {'added': net + run.subs(t, 2), 'reversed': -last, 'rate-end': rt.subs(t, 3)})

# ---------------------------------------------------------------- integrals, set 2
ft = t**2 - 6 * t + 8
A = sp.integrate(ft, (t, 0, x))
num('integrals', 2, 'p-area-function', 1, ft.subs(t, 3), {'area': A.subs(x, 3), 'derivative-of-f': sp.diff(ft, t).subs(t, 3)})
grid = [R(v, 100) for v in range(0, 601)]
vals = [A.subs(x, v) for v in grid]
locmax = [grid[i] for i in range(1, 600) if vals[i] > vals[i - 1] and vals[i] > vals[i + 1]]
assert locmax == [2]
num('integrals', 2, 'p-area-function', 2, locmax[0], {'min': 4, 'vertex': 3})
F = t**3 / 3 - 3 * t**2 + 8 * t
assert sp.expand(sp.diff(F, t) - ft) == 0
expr('integrals', 2, 'p-area-function', 3, F, t, True)
num('integrals', 2, 'p-area-function', 4, A.subs(x, 2),
    {'at-four': A.subs(x, 4), 'at-three': A.subs(x, 3), 'old-power': (t**3 / 2 - 6 * t**2 + 8 * t).subs(t, 2)})
two('A max on [0,6]', max(vals), A.subs(x, 6))
num('integrals', 2, 'p-area-function', 5, max(vals),
    {'local': A.subs(x, 2), 'unsigned': sp.integrate(sp.Abs(ft), (t, 0, 6))})

v_ = 8 * sp.exp(-t / 2)
Fv = sp.integrate(v_, t)
assert sp.simplify(Fv + 16 * sp.exp(-t / 2)) == 0
expr('integrals', 2, 'p-turnover-decay', 1, Fv, t, True)
num('integrals', 2, 'p-turnover-decay', 2, -Fv.subs(t, 0), {'zero': 0, 'minus': -16})
Tt = 16 - 16 * sp.exp(-t / 2)
two('turnover T(4)', Tt.subs(t, 4), float(mp.quad(lambda u: 8 * mp.e**(-u / 2), [0, 4])))
num('integrals', 2, 'p-turnover-decay', 3, Tt.subs(t, 4),
    {'no-c': Fv.subs(t, 4), 'times-k': 4 - 4 * sp.exp(-2), 'rate': v_.subs(t, 4)})
t12 = sp.solve(sp.Eq(Tt, 12), t)[0]
two('turnover t for 12', t12, float(mp.findroot(lambda u: 16 - 16 * mp.e**(-u / 2) - 12, 3)))
num('integrals', 2, 'p-turnover-decay', 4, t12, {'divided': sp.log(4) / 2, 'wrong-share': sp.solve(sp.Eq(sp.exp(-t / 2), R(3, 4)), t)[0]})

par, line = 2 * x**2, x + 3
cr = sorted(sp.solve(sp.Eq(par, line), x))
num('integrals', 2, 'p-line-and-parabola', 1, cr, {'signs': '1, -1.5'})
a1 = sp.integrate(line - par, (x, cr[0], cr[1]))
two('enclosed area', a1, float(mp.quad(lambda u: u + 3 - 2 * u * u, [-1, 1.5])))
num('integrals', 2, 'p-line-and-parabola', 2, a1,
    {'bottom-top': -a1, 'signs': sp.integrate(line - par, (x, -R(3, 2), 1)), 'line-only': sp.integrate(line, (x, cr[0], cr[1]))})
a2 = sp.integrate(par - line, (x, -2, -1))
assert par.subs(x, -2) == 8 and line.subs(x, -2) == 1
num('integrals', 2, 'p-line-and-parabola', 3, a2, {'signed': -a2, 'parabola-only': sp.integrate(par, (x, -2, -1))})
tot2 = sp.integrate(sp.Abs(line - par), (x, -2, R(3, 2)))
two('total area', tot2, a1 + a2)
num('integrals', 2, 'p-line-and-parabola', 4, tot2,
    {'one-integral': sp.integrate(line - par, (x, -2, R(3, 2))), 'negative': sp.integrate(par - line, (x, -2, R(3, 2)))})

fe = 12 * t - 3 * t**2
Gx = sp.integrate(fe - 9, (t, 0, x))
assert sp.expand(fe - 9 + 3 * (t - 1) * (t - 3)) == 0 and sp.expand(Gx - (-x**3 + 6 * x**2 - 9 * x)) == 0
num('integrals', 2, 'p-etf-units', 1, (fe - 9).subs(t, 2), {'no-redeem': fe.subs(t, 2), 'value': Gx.subs(x, 2)})
expr('integrals', 2, 'p-etf-units', 2, Gx, x)
num('integrals', 2, 'p-etf-units', 3, Gx.subs(x, 1), {'no-redeem': (Gx + 9 * x).subs(x, 1), 'at-three': Gx.subs(x, 3)})
num('integrals', 2, 'p-etf-units', 4, Gx.subs(x, 5), {'sign': 20, 'no-redeem': (Gx + 9 * x).subs(x, 5), 'level': Gx.subs(x, 3)})
ar = sp.integrate(sp.Abs(fe - 9), (t, 0, 5))
two('etf area', ar, float(mp.quad(lambda u: abs(12 * u - 3 * u * u - 9), [0, 1, 3, 5])))
num('integrals', 2, 'p-etf-units', 5, ar, {'net': -20, 'unsigned-net': 20, 'missed-middle': 4 + 20})

# ---------------------------------------------------------------- integrals, set 3
fd = 2 * x / (1 + x**2)**2
assert sp.integrate(fd, (x, 0, sp.oo)) == 1 and sp.simplify(sp.diff(-1 / (1 + x**2), x) - fd) == 0
expr('integrals', 3, 'p-order-size-tail', 1, -1 / (1 + x**2), x, True)
tail2 = sp.integrate(fd, (x, 2, sp.oo))
two('tail P(X>2)', tail2, float(mp.quad(lambda u: 2 * u / (1 + u * u)**2, [2, mp.inf])))
num('integrals', 3, 'p-order-size-tail', 2, tail2, {'below': 1 - tail2, 'x-limits': sp.integrate(x**-2, (x, 2, sp.oo))})
mm = sp.symbols('m', positive=True)
assert sp.simplify(sp.integrate(fd, (x, mm, sp.oo)) - 1 / (1 + mm**2)) == 0
num('integrals', 3, 'p-order-size-tail', 3, sp.solve(sp.Eq(1 / (1 + mm**2), R(1, 2)), mm)[0], {'drop-one': sp.sqrt(2)})
num('integrals', 3, 'p-order-size-tail', 4, sp.solve(sp.Eq(1 / (1 + mm**2), R(1, 100)), mm)[0],
    {'drop-one': 10, 'no-root': 99, 'wrong-tail': sp.solve(sp.Eq(1 / (1 + mm**2), R(99, 100)), mm)[0]})

fx = x * sp.exp(-x)
assert sp.integrate(fx, (x, 0, sp.oo)) == 1 and sp.simplify(sp.diff(-(x + 1) * sp.exp(-x), x) - fx) == 0
expr('integrals', 3, 'p-time-to-fill', 1, -(x + 1) * sp.exp(-x), x, True)
tl = sp.integrate(fx, (x, 2, sp.oo))
two('fill tail', tl, float(mp.quad(lambda u: u * mp.e**-u, [2, mp.inf])))
num('integrals', 3, 'p-time-to-fill', 2, tl, {'dropped-x': sp.exp(-2), 'dropped-one': 2 * sp.exp(-2), 'complement': 1 - tl})
EX = sp.integrate(x * fx, (x, 0, sp.oo))
two('fill mean', EX, float(mp.quad(lambda u: u * u * mp.e**-u, [0, mp.inf])))
num('integrals', 3, 'p-time-to-fill', 3, EX, {'no-factor': 1})
Eg = sp.integrate(100 * sp.exp(-x) * fx, (x, 0, sp.oo))
two('fill E[100e^-X]', Eg, float(mp.quad(lambda u: 100 * u * mp.e**(-2 * u), [0, mp.inf])))
num('integrals', 3, 'p-time-to-fill', 4, Eg, {'mean-wait': 100 * sp.exp(-EX), 'half': 50, 'one': 100})
assert Eg > 100 * sp.exp(-EX) and sp.diff(100 * sp.exp(-x), x, 2).subs(x, 1) > 0      # convex: E[g(X)] above g(E[X])
part('integrals', 3, 'p-time-to-fill', 5)

lnx = sp.log(x)
T2 = R(1, 2) * (lnx.subs(x, R(1, 2)) / 2 + lnx.subs(x, 1) + lnx.subs(x, R(3, 2)) / 2)
num('integrals', 3, 'p-log-return', 1, T2,
    {'full-ends': R(1, 2) * (sp.log(R(1, 2)) + sp.log(R(3, 2))), 'midpoint': R(1, 2) * (sp.log(R(3, 4)) + sp.log(R(5, 4))),
     'lost-strip': R(1, 2) * R(1, 2) * (sp.log(R(1, 2)) + 0)})
ex = sp.integrate(lnx, (x, R(1, 2), R(3, 2)))
two('E[ln X]', ex, float(mp.quad(mp.log, [0.5, 1.5])))
xl = lambda u: u * sp.log(u)             # noqa: E731
num('integrals', 3, 'p-log-return', 2, ex,
    {'plus-x': xl(R(3, 2)) - xl(R(1, 2)) + 1, 'uv-only': xl(R(3, 2)) - xl(R(1, 2)), 'estimate': -0.0719})
num('integrals', 3, 'p-log-return', 3, 0.0267 / 16, {'linear': 0.0267 / 4, 'eight-squared': 0.0267 / 64})
assert abs((float(ex) - float(T2)) - 0.0267) < 5e-5
assert ex < 0 == sp.log(1) and sp.diff(lnx, x, 2).subs(x, 1) < 0
part('integrals', 3, 'p-log-return', 4)


def trap(fn, a, bb, m):
    hh = (bb - a) / m
    return hh * (fn(a) / 2 + sum(fn(a + i * hh) for i in range(1, m)) + fn(bb) / 2)


print('  p-log-return true trapezium errors: n=2 %.5f, n=8 %.5f (predicted 0.00167)' % (
    float(ex) - trap(math.log, 0.5, 1.5, 2), float(ex) - trap(math.log, 0.5, 1.5, 8)))

st = t * sp.exp(-t**2 / 8)
assert sp.simplify(sp.diff(-4 * sp.exp(-t**2 / 8), t) - st) == 0
expr('integrals', 3, 'p-signal-average', 1, -4 * sp.exp(-t**2 / 8), t, True)
I4 = sp.integrate(st, (t, 0, 4))
sf = lambda u: u * math.exp(-u * u / 8)   # noqa: E731
two('signal integral', I4, float(mp.quad(lambda u: u * mp.e**(-u * u / 8), [0, 4])))
num('integrals', 3, 'p-signal-average', 2, I4, {'x-limits': 4 * (1 - sp.exp(-4)), 'quarter': R(1, 4) * (1 - sp.exp(-2)), 'sign': -I4})
num('integrals', 3, 'p-signal-average', 3, I4 / 4, {'no-divide': I4, 'halved': I4 / 2, 'x-limits': (1 - sp.exp(-4))})
num('integrals', 3, 'p-signal-average', 4, trap(sf, 0, 4, 2),
    {'full-ends': 2 * (sf(0) + sf(2) + sf(4)), 'no-h': trap(sf, 0, 4, 2) / 2, 'midpoint': 2 * (sf(1) + sf(3))})
e0, nn_, pred = 0.49, 2, []
while e0 >= 0.01:
    nn_ *= 2
    e0 /= 4
    pred.append(round(e0, 4))
lin_n, e1 = 2, 0.49
while e1 >= 0.01:
    lin_n *= 2
    e1 /= 2
num('integrals', 3, 'p-signal-average', 5, nn_, {'linear': lin_n, 'one-short': nn_ // 2})
print('  p-signal-average predicted errors', pred, '; true errors: ' + ', '.join(
    'n=%d %.4f' % (m_i, float(I4) - trap(sf, 0, 4, m_i)) for m_i in (2, 4, 8, 16)))

# ---------------------------------------------------------------- coverage
allparts = {(c, m, it['id'], i + 1) for (c, m), d in SETS.items() for it in d['items'] for i in range(len(it['parts']))}
seen.add(('limits', 3, 'p-gas-season', 3))
missing = sorted(allparts - seen)
if missing:
    fails += 1
    print('FAIL parts the reader did not solve:', missing)
print(f'mine.py: {len(allparts)} parts in {sum(len(d["items"]) for d in SETS.values())} problems; {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
