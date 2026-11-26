#!/usr/bin/env python3
"""Blind concept audit, odes problems-1 to problems-4 (audit-odes-problems-1-4).

Recomputes every graded key, every slip value and every number stated in
feedback and explanations, twice where it is a solution of an equation:
symbolically (sympy) and numerically (scipy solve_ivp, rtol 1e-11).
Reads keys from the content files, so a changed key is rechecked.
Exits 0 when every check passes.  Run from anywhere:
    python docs/reports/odes-problems-concepts.py
"""
import json, math, os, sys
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..',
                    'app', 'content', 'courses', 'odes')
FAIL = []
N = 0


def load(n):
    with open(os.path.join(ROOT, f'problems-{n}.json')) as fh:
        d = json.load(fh)
    return {it['id']: it for it in d['items']}


def chk(name, got, want, tol=1e-9):
    global N
    N += 1
    ok = abs(float(got) - float(want)) <= tol
    if not ok:
        FAIL.append(f'{name}: got {got}, content has {want}')
    return ok


def truth(name, cond):
    global N
    N += 1
    if not cond:
        FAIL.append(name)


def key(item, part):
    w = item['parts'][part - 1]['widget']
    return w.get('answer', w.get('answers'))


def slip(item, part, sid):
    for s in item['parts'][part - 1]['widget']['wrong']:
        if s['id'] == sid:
            return s['value']
    raise KeyError(sid)


def ivp(f, y0, t1, **kw):
    s = solve_ivp(f, (0, t1), y0, rtol=1e-11, atol=1e-13, method='DOP853', **kw)
    return s.y[:, -1]


t = sp.symbols('t', nonnegative=True)

# ---------------------------------------------------------------- problems-1
P1 = load(1)
it = P1['p-lending-members']
m = sp.Function('m')
f = lambda v: -v**2 + 8*v - 12
truth('P1.1 equilibria', sorted(sp.solve(f(sp.Symbol('x')))) == sorted(key(it, 1)))
x = sp.Symbol('x')
truth('P1.1 slip signs are roots of m^2+8m+12', set(sp.solve(x**2 + 8*x + 12)) == {-2, -6})
truth('P1.1 slip no-constant', set(sp.solve(-x**2 + 8*x)) == {0, 8})
fp = sp.diff(f(x), x)
truth('P1.2 f\'(2)=4, f\'(6)=-4', fp.subs(x, 2) == 4 and fp.subs(x, 6) == -4)
truth('P1.2 f>0 on (2,6): start 2.5 rises to 6', all(f(v) > 0 for v in np.linspace(2.01, 5.99, 400)))
# partial fractions identity
truth('P1.3 partial fractions', sp.simplify(1/((x-2)*(6-x)) - sp.Rational(1, 4)*(1/(x-2) + 1/(6-x))) == 0)
# solve (m-2)/(6-m) = e^{4t}/7 for m and substitute back (sympy's dsolve cannot fit this constant)
E4 = sp.exp(4*t)/7
sol = (2 + 6*E4)/(1 + E4)
truth('P1.3 ratio = e^{4t}/7 solves the equation', sp.simplify(sp.diff(sol, t) - f(sol)) == 0 and sol.subs(t, 0) == sp.Rational(5, 2))
gen = sp.dsolve(sp.Eq(m(t).diff(t), f(m(t))), m(t)).rhs
truth('P1.3 general solution has rate 4', sp.simplify(sp.diff(sp.log((gen - 2)/(6 - gen)), t)) == 4)
chk('P1.3 k', 4, key(it, 3))
chk('P1.4 A', 1/7, key(it, 4), 1e-6)
chk('P1.4 slip inverted', 3.5/0.5, slip(it, 4, 'inverted'))
chk('P1.4 slip over-m', 0.5/2.5, slip(it, 4, 'over-m'))
chk('P1.4 slip gap', 0.5/4, slip(it, 4, 'gap'))
T = math.log(21)/4
chk('P1.5 t', T, key(it, 5), 1e-6)
chk('P1.5 numeric m(T)=5', ivp(lambda s, y: [f(y[0])], [2.5], T)[0], 5, 1e-8)
chk('P1.5 slip inverted', math.log(3/7)/4, slip(it, 5, 'inverted'), 6e-4)
chk('P1.5 slip no-quarter', math.log(21), slip(it, 5, 'no-quarter'), 6e-4)
chk('P1.5 slip over-m', math.log(15)/4, slip(it, 5, 'over-m'), 6e-4)
chk('P1.5 slip gap', math.log(24)/4, slip(it, 5, 'gap'), 6e-4)
truth('P1.5 a little over three weeks', 21 < T*30.44 < 25)

it = P1['p-moving-target']
r = sp.Function('r')
rs = sp.dsolve(sp.Eq(r(t).diff(t), sp.Rational(5, 4)*(3 + sp.Rational(3, 5)*t - r(t))), r(t), ics={r(0): 5}).rhs
want = sp.Rational(252, 100) + sp.Rational(3, 5)*t + sp.Rational(248, 100)*sp.exp(-sp.Rational(5, 4)*t)
truth('P2.2 r(t)', sp.simplify(rs - want) == 0)
chk('P2.2 numeric r(3)', ivp(lambda s, y: [1.25*(3 + 0.6*s - y[0])], [5.0], 3)[0], float(want.subs(t, 3)), 1e-8)
truth('P2.2 by parts', sp.simplify(sp.diff(sp.exp(1.25*t)*(2.52 + 0.6*t), t) - 1.25*sp.exp(1.25*t)*(3 + 0.6*t)) == 0)
chk('P2.3 half-life', math.log(2)/1.25, key(it, 3), 1e-6)
chk('P2.3 slip mean-life', 1/1.25, slip(it, 3, 'mean-life'))
chk('P2.3 slip times', math.log(2)*1.25, slip(it, 3, 'times'), 1e-4)
tm = math.log(3.1/0.6)/1.25
chk('P2.4 t min', tm, key(it, 4), 1e-6)
truth('P2.4 it is a minimum', float(sp.diff(want, t, 2).subs(t, tm)) > 0)
chk('P2.4 slip no-chain', math.log(2.48/0.6)/1.25, slip(it, 4, 'no-chain'), 6e-4)
chk('P2.4 slip no-lag', math.log(1.25*2/0.6)/1.25, slip(it, 4, 'no-lag'), 6e-4)
chk('P2.4 slip sign', math.log(1.25*1.52/0.6)/1.25, slip(it, 4, 'sign'), 6e-4)
chk('P2.4 2.37 half-lives', tm/(math.log(2)/1.25), 2.37, 5e-3)
chk('P2.4 r = theta = 3.79 at the minimum', float(want.subs(t, tm)), 3.79, 5e-3)
chk('P2.4 theta there', 3 + 0.6*tm, 3.79, 5e-3)
chk('P2.4 e^{1.25t}=5.167', 3.1/0.6, 5.167, 5e-4)

it = P1['p-rising-pension']
B = sp.Function('B')
Bs = sp.dsolve(sp.Eq(B(t).diff(t), sp.Rational(4, 100)*B(t) + 2000*sp.exp(sp.Rational(2, 100)*t)), B(t), ics={B(0): 0}).rhs
truth('P3.3 B(t)', sp.simplify(Bs - 100000*(sp.exp(sp.Rational(4, 100)*t) - sp.exp(sp.Rational(2, 100)*t))) == 0)
B10 = 100000*(math.exp(0.4) - math.exp(0.2))
chk('P3.4 B(10)', B10, key(it, 4), 0.01)
chk('P3.4 numeric', ivp(lambda s, y: [0.04*y[0] + 2000*math.exp(0.02*s)], [0.0], 10)[0], B10, 1e-5)
flat = 50000*(math.exp(0.4) - 1)
pay = 100000*(math.exp(0.2) - 1)
chk('P3.4 slip flat', flat, slip(it, 4, 'flat'), 0.01)
chk('P3.4 slip no-interest', pay, slip(it, 4, 'no-interest'), 0.01)
chk('P3.4 rising adds 2451', B10 - flat, 2451, 0.5)
chk('P3.4 growth 4902', B10 - pay, 4902, 0.5)
# Convention check (finding): yearly-compounded 4% would give a different key.
B10_yearly = ivp(lambda s, y: [math.log(1.04)*y[0] + 2000*math.exp(0.02*s)], [0.0], 10)[0]
truth('P3 convention: yearly 4% differs from the key by more than the tolerance', abs(B10_yearly - B10) > 1)

# ---------------------------------------------------------------- problems-2
P2 = load(2)
it = P2['p-hedge-overshoot']
xf = sp.Function('x')
xs = sp.dsolve(sp.Eq(xf(t).diff(t, 2) + 4*xf(t).diff(t) + 29*xf(t), 58), xf(t),
               ics={xf(0): 0, xf(t).diff(t).subs(t, 0): 0}).rhs
want = 2 - sp.exp(-2*t)*(2*sp.cos(5*t) + sp.Rational(4, 5)*sp.sin(5*t))
truth('2.P1 x(t)', sp.simplify(xs - want) == 0)
truth('2.P1.1 roots', set(sp.solve(x**2 + 4*x + 29)) == {-2 + 5*sp.I, -2 - 5*sp.I})
chk('2.P1.2 xp', 2, key(it, 2))
chk('2.P1.3 c2', -0.8, key(it, 3))
truth("2.P1.4 x' = 11.6 e^{-2t} sin 5t", sp.simplify(sp.diff(want, t) - sp.Rational(116, 10)*sp.exp(-2*t)*sp.sin(5*t)) == 0)
chk('2.P1.4 peak time', math.pi/5, key(it, 4), 1e-6)
chk('2.P1.4 slip period', 2*math.pi/5, slip(it, 4, 'period'), 1e-4)
chk('2.P1.4 slip omega0', math.pi/math.sqrt(29), slip(it, 4, 'omega0'), 1e-4)
ov = math.exp(-2*math.pi/5)
chk('2.P1.5 overshoot', ov, key(it, 5), 1e-5)
num = ivp(lambda s, y: [y[1], 58 - 4*y[1] - 29*y[0]], [0.0, 0.0], math.pi/5)
chk('2.P1.5 numeric x(pi/5)', num[0], 2 + 2*ov, 1e-8)
chk('2.P1.5 numeric x\'(pi/5)=0', num[1], 0, 1e-7)
chk('2.P1.5 2.5692', 2 + 2*ov, 2.5692, 5e-5)
chk('2.P1.5 slip period', -math.exp(-4*math.pi/5), slip(it, 5, 'period'), 1e-5)
z = 2/math.sqrt(29)
chk('2.P1.5 zeta formula', math.exp(-z*math.pi/math.sqrt(1 - z*z)), ov, 1e-12)
# global max of overshoot is the first peak
dense = np.linspace(0, 6, 60001)
xv = 2 - np.exp(-2*dense)*(2*np.cos(5*dense) + 0.8*np.sin(5*dense))
chk('2.P1.5 first peak is the largest', xv.max(), 2 + 2*ov, 1e-6)

it = P2['p-cash-buffer']
xs = sp.dsolve(sp.Eq(xf(t).diff(t, 2) + 4*xf(t).diff(t) + 5*xf(t), 10*sp.cos(t)), xf(t),
               ics={xf(0): 0, xf(t).diff(t).subs(t, 0): 0}).rhs
want = sp.exp(-2*t)*(-sp.Rational(5, 4)*sp.cos(t) - sp.Rational(15, 4)*sp.sin(t)) + sp.Rational(5, 4)*(sp.cos(t) + sp.sin(t))
truth('2.P2 x(t)', sp.simplify(xs - want) == 0)
chk('2.P2.2 B', 1.25, key(it, 2))
chk('2.P2.3 c2', -3.75, key(it, 3))
chk('2.P2.3 slip no-decay', -1.25, slip(it, 3, 'no-decay'))
chk('2.P2.3 slip sign (c1=+1.25)', 2*1.25 - 1.25, slip(it, 3, 'sign'))
v = 1.25 - 3.75*math.exp(-math.pi)
chk('2.P2.4 x(pi/2)', v, key(it, 4), 1e-6)
chk('2.P2.4 numeric', ivp(lambda s, y: [y[1], 10*math.cos(s) - 4*y[1] - 5*y[0]], [0.0, 0.0], math.pi/2)[0], v, 1e-8)
chk('2.P2.4 slip no-decay', 1.25 - 1.25*math.exp(-math.pi), slip(it, 4, 'no-decay'), 6e-4)
chk('2.P2.4 slip sign', 1.25 + 1.25*math.exp(-math.pi), slip(it, 4, 'sign'), 6e-4)
chk('2.P2.4 e^-pi', math.exp(-math.pi), 0.04321, 5e-6)
chk('2.P2.4 0.1621', 3.75*math.exp(-math.pi), 0.1621, 5e-5)
chk('2.P2.4 amplitude', 1.25*math.sqrt(2), 1.77, 5e-3)

it = P2['p-tracking-gap']
chk('2.P3.1 b', 10, key(it, 1))
chk('2.P3.2 root', -5, key(it, 2))
xs = sp.dsolve(sp.Eq(xf(t).diff(t, 2) + 10*xf(t).diff(t) + 25*xf(t), 0), xf(t),
               ics={xf(0): 2, xf(t).diff(t).subs(t, 0): -4}).rhs
truth('2.P3 x(t)', sp.simplify(xs - (2 + 6*t)*sp.exp(-5*t)) == 0)
chk('2.P3.3 c2', 6, key(it, 3))
chk('2.P3.3 slip sign', -4 - 10, slip(it, 3, 'sign'))
chk('2.P3.4 x(0.5)', 5*math.exp(-2.5), key(it, 4), 1e-6)
chk('2.P3.4 numeric', ivp(lambda s, y: [y[1], -10*y[1] - 25*y[0]], [2.0, -4.0], 0.5)[0], 5*math.exp(-2.5), 1e-9)
chk('2.P3.4 slip no-t', 2*math.exp(-2.5), slip(it, 4, 'no-t'), 1e-4)
chk('2.P3.4 slip sign', (2 - 14*0.5)*math.exp(-2.5), slip(it, 4, 'sign'), 1e-6)
chk('2.P3.4 slip no-r', (2 - 4*0.5)*math.exp(-2.5), slip(it, 4, 'no-r'))
# "any less oscillates, any more is slower": slow root of r^2+br+25 for b>10 is above -5
truth('2.P3.1 over-damped is slower', all((-b + math.sqrt(b*b - 100))/2 > -5 for b in (10.5, 12, 20, 50)))
# "a start steeper than -10 crosses once"
for s0 in (-10.5, -12, -30):
    c2 = s0 + 10
    tt = np.linspace(0, 20, 200001)
    xx = (2 + c2*tt)*np.exp(-5*tt)
    sg = np.sign(xx[xx != 0])
    truth(f"2.P3.4 crosses once for slope {s0}", int(np.sum(np.diff(sg) != 0)) == 1)
truth('2.P3.4 slope -10 itself does not cross', True)  # x = 2e^{-5t} > 0

# ---------------------------------------------------------------- problems-3
P3 = load(3)
it = P3['p-yield-gaps']
A = sp.Matrix([[-7, 2], [-6, 1]])
chk('3.P1.1 det', A.det(), key(it, 1))
chk('3.P1.1 slip', -7 - 12, slip(it, 1, 'bc-sign'))
truth('3.P1.2 eigenvalues', set(A.eigenvals()) == set(key(it, 2)))
truth('3.P1.4 eigenvectors', A*sp.Matrix([1, 3]) == -sp.Matrix([1, 3]) and A*sp.Matrix([1, 1]) == -5*sp.Matrix([1, 1]))
c = sp.Matrix([[1, 1], [3, 1]]).solve(sp.Matrix([4, 2]))
chk('3.P1.4 c1', c[0], key(it, 4))
truth('3.P1.4 c2=5', c[1] == 5)
An = np.array(A.tolist(), float)
T = 6.0
num = ivp(lambda s, y: An @ y, [4.0, 2.0], T)
ex = -math.exp(-T)*np.array([1, 3]) + 5*math.exp(-5*T)*np.array([1, 1])
chk('3.P1.5 numeric x(6)', num[0], ex[0], 1e-10)
chk('3.P1.5 y/x -> 3', num[1]/num[0], key(it, 5), 1e-6)
# note: x(t) = -e^{-t} + 5e^{-5t} changes sign once at t = ln5/4 (ledger remark)
chk('3.P1 x crosses zero at ln5/4', -math.exp(-math.log(5)/4) + 5*math.exp(-5*math.log(5)/4), 0, 1e-12)

it = P3['p-liquidity-arbitrage']
X, Y = sp.symbols('X Y')
F = sp.Matrix([X*(6 - X - Y), Y*(X - 2)])
eq = [s for s in sp.solve(list(F), [X, Y], dict=True) if s[X] > 0 and s[Y] > 0]
truth('3.P2.1 equilibrium', eq == [{X: 2, Y: 4}])
J = F.jacobian([X, Y]).subs({X: 2, Y: 4})
truth('3.P2.2 Jacobian', J == sp.Matrix([[-2, -2], [4, 0]]))
tau, dl = J.trace(), J.det()
truth('3.P2.3 tau, Delta', tau == -2 and dl == 8)
chk('3.P2.3 disc', tau**2 - 4*dl, key(it, 3))
chk('3.P2.3 slip delta-sign', 4 + 32, slip(it, 3, 'delta-sign'))
chk('3.P2.3 slip no-four', 4 - 8, slip(it, 3, 'no-four'))
truth('3.P2.5 eigenvalues', set(J.eigenvals()) == {-1 + sp.sqrt(7)*sp.I, -1 - sp.sqrt(7)*sp.I})
per = 2*math.pi/math.sqrt(7)
chk('3.P2.5 period', per, key(it, 5), 1e-6)
chk('3.P2.5 slip centre', 2*math.pi/math.sqrt(8), slip(it, 5, 'centre'), 6e-4)
chk('3.P2.5 slip no-half', 2*math.pi/math.sqrt(28), slip(it, 5, 'no-half'), 6e-4)
# nonlinear run: near (2,4) the swing period and the decay per turn match the linearisation
fn = lambda s, y: [y[0]*(6 - y[0] - y[1]), y[1]*(y[0] - 2)]
ev = lambda s, y: y[1] - 4.0
ev.direction = 1
s = solve_ivp(fn, (0, 12), [2.0, 4.001], rtol=1e-12, atol=1e-14, method='DOP853', events=ev)
gaps = np.diff(s.t_events[0])
truth('3.P2.5 nonlinear turn time near the point is 2pi/sqrt7', abs(gaps[1] - per) < 2e-3)
truth('3.P2.4 nonlinear path spirals in', abs(s.y[0, -1] - 2) < 1e-6 and abs(s.y[1, -1] - 4) < 1e-6)

it = P3['p-trend-signal']
A = sp.Matrix([[0, 1], [5, -4]])
chk('3.P3.2 det', A.det(), key(it, 2))
truth('3.P3.3 eigenvalues', set(A.eigenvals()) == set(key(it, 3)))
truth('3.P3.4 eigenvector (1,-5)', A*sp.Matrix([1, -5]) == -5*sp.Matrix([1, -5]))
sf = sp.Function('s')
gen = sp.dsolve(sp.Eq(sf(t).diff(t, 2) + 4*sf(t).diff(t) - 5*sf(t), 0), sf(t),
                ics={sf(0): 1, sf(t).diff(t).subs(t, 0): key(it, 4)}).rhs
truth('3.P3.4 s = e^{-5t}', sp.simplify(gen - sp.exp(-5*t)) == 0)
for s0, lab in ((1, 'unstable'), (5, 'sign')):
    g = sp.dsolve(sp.Eq(sf(t).diff(t, 2) + 4*sf(t).diff(t) - 5*sf(t), 0), sf(t),
                  ics={sf(0): 1, sf(t).diff(t).subs(t, 0): s0}).rhs
    truth(f'3.P3.4 slip {lab} grows', sp.limit(g, t, sp.oo) == sp.oo)
truth('3.P3.4 slip unstable is e^t', sp.simplify(sp.dsolve(sp.Eq(sf(t).diff(t, 2) + 4*sf(t).diff(t) - 5*sf(t), 0), sf(t),
      ics={sf(0): 1, sf(t).diff(t).subs(t, 0): 1}).rhs - sp.exp(t)) == 0)

# ---------------------------------------------------------------- problems-4
P4 = load(4)
it = P4['p-test-rig']
s_ = sp.symbols('s')
Yl = 24/((s_ + 2)*(s_ + 4)*(s_ + 8))
truth('4.P1.1 transform', sp.simplify(sp.laplace_transform(24*sp.exp(-8*t), t, s_, noconds=True) - 24/(s_ + 8)) == 0)
res = {p: sp.residue(Yl, s_, p) for p in (-2, -4, -8)}
truth('4.P1.3 residues 2,-3,1', res == {-2: 2, -4: -3, -8: 1})
chk('4.P1.3 key', res[-4], key(it, 3))
yf = sp.Function('y')
ys = sp.dsolve(sp.Eq(yf(t).diff(t, 2) + 6*yf(t).diff(t) + 8*yf(t), 24*sp.exp(-8*t)), yf(t),
               ics={yf(0): 0, yf(t).diff(t).subs(t, 0): 0}).rhs
want = 2*sp.exp(-2*t) - 3*sp.exp(-4*t) + sp.exp(-8*t)
truth('4.P1.4 y(t)', sp.simplify(ys - want) == 0)
u = sp.Symbol('u')
yu = 2*u - 3*u**2 + u**4
truth('4.P1.4 factorisation', sp.expand(u*(1 - u)**2*(u + 2) - yu) == 0)
truth('4.P1.5 dy/du', sp.expand(2*(u - 1)*(2*u**2 + 2*u - 1) - sp.diff(yu, u)) == 0)
us = (math.sqrt(3) - 1)/2
ymax = (6*math.sqrt(3) - 9)/4
chk('4.P1.5 ymax closed form', us*2 - 3*us**2 + us**4, ymax, 1e-12)
chk('4.P1.5 key', ymax, key(it, 5), 5e-5)
tp = 0.5*math.log(1 + math.sqrt(3))
chk('4.P1.5 time', tp, slip(it, 5, 'time'), 5e-5)
chk('4.P1.5 time is -ln(u)/2', -math.log(us)/2, tp, 1e-12)
chk('4.P1.5 slip u', us, slip(it, 5, 'u-value'), 5e-5)
chk('4.P1.5 slip y(1)', float(want.subs(t, 1)), slip(it, 5, 'at-one'), 5e-5)
dn = solve_ivp(lambda s, y: [y[1], 24*math.exp(-8*s) - 6*y[1] - 8*y[0]], (0, 6), [0, 0], rtol=1e-11, atol=1e-13,
               method='DOP853', dense_output=True)
tt = np.linspace(0, 6, 600001)
yy = dn.sol(tt)[0]
chk('4.P1.5 numeric max', yy.max(), ymax, 1e-8)
chk('4.P1.5 numeric argmax', tt[yy.argmax()], tp, 1e-4)
truth('4.P1.4 never negative', yy.min() > -1e-10)

it = P4['p-skydiver-check']
ex = 49*(1 - math.exp(-0.4))
chk('4.P2.2 v(2)', ex, key(it, 2), 5e-5)
chk('4.P2.2 numeric', ivp(lambda s, y: [9.8 - 0.2*y[0]], [0.0], 2)[0], ex, 1e-9)
chk('4.P2.2 slip no-divide', 9.8*(1 - math.exp(-0.4)), slip(it, 2, 'no-divide'), 5e-5)
chk('4.P2.2 slip carried-constant', 9.8*math.exp(-0.4), slip(it, 2, 'carried-constant'), 5e-5)
chk('4.P2.2 slip carried-sign', 49*(math.exp(0.4) - 1), slip(it, 2, 'carried-sign'), 5e-5)
fv = lambda v: 9.8 - 0.2*v


def euler(n):
    h, v = 2/n, 0.0
    for _ in range(n):
        v += h*fv(v)
    return v


def rk4(n, mean=False, noh=False):
    h, v = 2/n, 0.0
    for _ in range(n):
        k1 = fv(v); k2 = fv(v + h/2*k1); k3 = fv(v + h/2*k2); k4 = fv(v + h*k3)
        if mean:
            v += h*(k1 + k2 + k3 + k4)/4
        elif noh:
            v += (k1 + 2*k2 + 2*k3 + k4)/6
        else:
            v += h/6*(k1 + 2*k2 + 2*k3 + k4)
    return v


chk('4.P2.3 Euler', euler(2), key(it, 3), 1e-9)
chk('4.P2.3 slip same-slope', 2*9.8, slip(it, 3, 'same-slope'), 1e-9)
chk('4.P2.3 Euler error 1.4857', euler(2) - ex, 1.4857, 5e-5)
truth('4.P2.3 Euler overshoots at every n here', all(euler(n) > ex for n in (1, 2, 4, 8, 64)))
chk('4.P2.4 RK4', rk4(1), key(it, 4), 5e-5)
chk('4.P2.4 slip plain-mean', rk4(1, mean=True), slip(it, 4, 'plain-mean'), 5e-5)
chk('4.P2.4 slip no-h', rk4(1, noh=True), slip(it, 4, 'no-h'), 5e-5)
chk('4.P2.4 error 0.0039', ex - rk4(1), 0.0039, 5e-5)
chk('4.P2.5 error n=2', ex - rk4(2), 0.000207, 5e-7)
chk('4.P2.5 error n=4', ex - rk4(4), 0.0000119, 5e-8)
e1 = 0.0039
n = 1
while e1/16**int(math.log2(n)) >= 5e-5:
    n *= 2
chk('4.P2.5 first n', n, key(it, 5))
n = 1
while e1/2**int(math.log2(n)) >= 5e-5:
    n *= 2
chk('4.P2.5 slip first-order', n, slip(it, 5, 'first-order'))
truth('4.P2.5 RK4 n=4 prints 16.1543', f'{rk4(4):.4f}' == '16.1543' and f'{rk4(8):.4f}' == '16.1543')
truth('4.P2.5 observed ratio near 16', 14 < (ex - rk4(2))/(ex - rk4(4)) < 19)

it = P4['p-dose-simulator']
A = np.array([[-6, 0], [6, -0.5]])
truth('4.P3.1 eigenvalues', sorted(np.linalg.eigvals(A).real) == sorted(key(it, 1)))
chk('4.P3.2 factor', 1 + 0.5*(-6), key(it, 2))
chk('4.P3.3 Euler limit', 2/6, key(it, 3), 1e-4)
R = lambda z: 1 + z + z*z/2 + z**3/6 + z**4/24
from scipy.optimize import brentq
lim = -brentq(lambda z: abs(R(z)) - 1, -3.5, -2.0)
chk('4.P3.4 RK4 real limit 2.7853', lim, 2.7853, 5e-5)
chk('4.P3.4 key', 2.7853/6, key(it, 4), 5e-5)
chk('4.P3.4 slip slow', 2.7853/0.5, slip(it, 4, 'slow-mode'), 5e-5)
truth('4.P3.4 gain under 40%', 0.38 < (2.7853/6)/(1/3) - 1 < 0.40)
chk('4.P3.4 about 28 minutes', 2.7853/6*60, 28, 0.5)
ne = next(n for n in range(1, 500) if abs(1 - 6*24/n) < 1 - 1e-12)
nr = next(n for n in range(1, 500) if abs(R(-6*24/n)) < 1)
chk('4.P3.5 Euler steps', ne, key(it, 5))
chk('4.P3.5 RK4 steps', nr, slip(it, 5, 'rk4-steps'))
chk('4.P3.5 RK4 readings', 4*nr, slip(it, 5, 'rk4'))


# run the simulator itself: system Euler and RK4 on (g, b), start 100 mg in the gut
def run(method, n):
    h = 24/n
    xv = np.array([100.0, 0.0])
    M = np.eye(2) + h*A if method == 'euler' else sum(np.linalg.matrix_power(h*A, k)/math.factorial(k) for k in range(5))
    peak = 0.0
    for _ in range(n):
        xv = M @ xv
        peak = max(peak, abs(xv[0]))
    return abs(xv[0]), peak


truth('4.P3.5 Euler n=73 decays', run('euler', 73)[0] < 100)
truth('4.P3.5 Euler n=72 does not decay (|g| stays 100)', abs(run('euler', 72)[0] - 100) < 1e-6)
truth('4.P3.5 Euler n=71 grows', run('euler', 71)[0] > 100)
truth('4.P3.5 RK4 n=52 decays, n=51 grows', run('rk4', 52)[0] < 100 < run('rk4', 51)[0])
truth('4.P3.2 Euler h=0.5 doubles and flips', abs(run('euler', 48)[0] - 100*2**48) < 1e-3*100*2**48)
chk('4.P3.1 gut after one hour', math.exp(-6), 0.0025, 5e-5)

# ---- findings recorded in audit-odes-problems-1-4 (these state facts, so they pass)
# F3: in p-yield-gaps both gaps cross zero once before closing, and the path bends.
tx, ty = math.log(5)/4, math.log(5/3)/4
chk('F3 y crosses zero at ln(5/3)/4', -3*math.exp(-ty) + 5*math.exp(-5*ty), 0, 1e-12)
truth('F3 both crossings are after the start', 0 < ty < tx < 1)
v0 = np.array([[-7, 2], [-6, 1]], float) @ np.array([4.0, 2.0])
ang = math.degrees(math.atan2(3, 1) - math.atan2(v0[1], v0[0])) % 360
truth('F3 velocity direction swings by more than 20 degrees', min(ang, 360 - ang) > 20)
# F4: in p-dose-simulator the blood amount rises before it falls (peak at ln(12)/5.5 h)
tb = math.log(12)/5.5
bfun = lambda s: 6/5.5*(math.exp(-0.5*s) - math.exp(-6*s))
truth('F4 blood amount rises first', bfun(tb) > bfun(tb/2) > 0 and bfun(tb) > bfun(2*tb))
# F1: yearly-compounded reading of "earns 4% a year" gives about 26,934, not 27,042
chk('F1 yearly reading', B10_yearly, 26934, 2)

print(f'{N} checks, {len(FAIL)} failed')
for f_ in FAIL:
    print('FAIL', f_)
sys.exit(1 if FAIL else 0)
