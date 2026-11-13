#!/usr/bin/env python3
"""Numbers of the fixes proposed in review-problems-vector-calc-1-3.md (findings 1, 2, 3, 4). Each twice. Exit 0."""
import sys
import sympy as sp

x, y, t = sp.symbols('x y t', real=True)
pi, sqrt, sin, cos, R, integ = sp.pi, sp.sqrt, sp.sin, sp.cos, sp.Rational, sp.integrate
bad = 0


def chk(name, cond):
    global bad
    print(('ok    ' if cond else 'FAIL  ') + name)
    bad += 0 if cond else 1


def line(F, c, a, b):
    s = {x: c[0], y: c[1]}
    return sp.simplify(integ(F[0].subs(s) * sp.diff(c[0], t) + F[1].subs(s) * sp.diff(c[1], t), (t, a, b)))


def flux(F, c, a, b):
    s = {x: c[0], y: c[1]}
    return sp.simplify(integ(F[0].subs(s) * sp.diff(c[1], t) - F[1].subs(s) * sp.diff(c[0], t), (t, a, b)))


def seg(p, q):
    return [p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]


def show(name, v, dp=4):
    print('      %-34s %s = %.*f' % (name, v, dp, float(v)))


# Finding 1: the bead on the circle of radius 6
F = [2 * x - y, x + 2 * y]
c = [6 * cos(t), 6 * sin(t)]
size = sqrt(sp.simplify((F[0] ** 2 + F[1] ** 2).subs({x: c[0], y: c[1]})))
S = integ(size * 6, (t, 0, pi))
dot = sp.simplify(F[0].subs({x: c[0], y: c[1]}) * sp.diff(c[0], t) + F[1].subs({x: c[0], y: c[1]}) * sp.diff(c[1], t))
W = line(F, c, 0, pi)
chk('1: |F| = 6 sqrt5, integral 36 sqrt5 pi, F.r\' = 36, W = 36 pi, share 1/sqrt5',
    sp.simplify(size - 6 * sqrt(5)) == 0 and sp.simplify(S - 36 * sqrt(5) * pi) == 0 and dot == 36 and sp.simplify(W - 36 * pi) == 0 and sp.simplify(W / S - 1 / sqrt(5)) == 0)
chk('1: W again by Green on the closed half disc (curl 2, area 18 pi, diameter 0)', sp.simplify(2 * 18 * pi - line(F, seg((-6, 0), (6, 0)), 0, 1) - W) == 0)
show('part 3 key', S); show('part 3 no-speed', S / 6); show('part 3 squared', 180 * 6 * pi, 3); show('part 3 full-circle', 2 * S)
show('part 4 position', sp.simplify(F[0].subs({x: c[0], y: c[1]}) * c[0] + F[1].subs({x: c[0], y: c[1]}) * c[1])); show('part 4 magnitude', size ** 2)
show('part 5 W', W, 2); show('part 5 key', W / S); show('part 5 inverse', S / W); show('part 5 no-integral', dot / S); show('part 5 full-circle', 2 * W / S)

# Finding 2: two routes from (0, 0) to (2, 8)
F = [x * y, x + y]
A, B = [t, t ** 3], [t, 4 * t]
WA, WB = line(F, A, 0, 2), line(F, B, 0, 2)
green = integ(integ(1 - x, (y, x ** 3, 4 * x)), (x, 0, 2))
chk('2: W_A = 252/5, W_B = 152/3, loop -4/15 directly and by Green (A below B on 0 < x < 2, so the loop is anticlockwise)',
    WA == R(252, 5) and WB == R(152, 3) and WA - WB == R(-4, 15) and green == WA - WB)
show('part 2 key', WA); show('part 2 no-dot', integ(t ** 4 + t + t ** 3, (t, 0, 2))); show('part 2 no-chain', integ(t ** 4 + (t + t ** 3) * t ** 2, (t, 0, 2)))
show('part 3 key', WB); show('part 3 ds', WB * sqrt(17)); show('part 3 p-only', integ(4 * t ** 2, (t, 0, 2))); show('part 3 q-only', integ(20 * t, (t, 0, 2)))
show('part 3 no-four', integ(4 * t ** 2 + 5 * t, (t, 0, 2)))
show('part 4 key', WA - WB); show('part 4 added', WA + WB); show('part 4 sign', WB - WA)

# Finding 3: the potential x^4 + 3xy^2
F = [4 * x ** 3 + 3 * y ** 2, 6 * x * y]
f = x ** 4 + 3 * x * y ** 2
chk('3: P_y = Q_x = 6y, grad f = F, f(0, 0) = 0', sp.diff(F[0], y) == 6 * y == sp.diff(F[1], x) and sp.diff(f, x) == F[0] and sp.diff(f, y) == F[1])
chk('3: F(1, 2) = (16, 12)', [g.subs({x: 1, y: 2}) for g in F] == [16, 12])
W = f.subs({x: 2, y: 3}) - f.subs({x: 1, y: 0})
chk('3: work 69 by the potential and along the straight path', W == 69 and line(F, seg((1, 0), (2, 3)), 0, 1) == 69)
fd = integ(F[0], x) + integ(F[1], y)
show('part 1 y-not-squared', sp.Matrix([4 + 3 * 2, 12]).T, 0) if False else print('      part 1 y-not-squared (10, 12), swap (12, 16)')
print('      part 2 px', sp.diff(F[0], x), ' qy', sp.diff(F[1], y))
print('      part 3 double', sp.expand(fd), ' wrong-var', x ** 4 + integ(F[1], x))
show('part 4 end-only', f.subs({x: 2, y: 3}), 0); show('part 4 double', fd.subs({x: 2, y: 3}) - fd.subs({x: 1, y: 0}), 0)

# Finding 4: the triangle (0, 0), (3, 0), (0, 6)
F = [x ** 2 + y, 2 * x * y]
tri = lambda g: integ(integ(g, (y, 0, 6 - 2 * x)), (x, 0, 3))
cs = [(0, 0), (3, 0), (0, 6)]
fl = [flux(F, seg(cs[i], cs[(i + 1) % 3]), 0, 1) for i in range(3)]
chk('4: flux 36 by the divergence; edges 0 (bottom), 54 (long), -18 (left)', tri(4 * x) == 36 and fl == [0, 54, -18] and sum(fl) == 36)
show('part 2 curl', tri(2 * y - 1), 0); show('part 2 rectangle', integ(integ(4 * x, (y, 0, 6)), (x, 0, 3)), 0); show('part 2 only-p', tri(2 * x), 0)
show('part 3 sign', 18, 0); show('part 4 add-edge', 36 - 18, 0); show('part 4 all-out', 36, 0)

print('%d failure(s)' % bad)
sys.exit(1 if bad else 0)
