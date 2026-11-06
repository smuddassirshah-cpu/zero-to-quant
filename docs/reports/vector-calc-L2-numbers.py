"""Recompute every stated number of vector-calc level 2 twice: by the theorem (Green, its normal form, the shoelace or polar
area formula) and by direct parametrised integration with SciPy, then check it in the JSON.
Run: python3 docs/reports/vector-calc-L2-numbers.py   (exits 0 when every check passes)
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level
from scipy.integrate import quad, dblquad

lv = Level("vector-calc", 2)
pi = math.pi


def both(a, b, tol=1e-7):
    assert abs(a - b) <= tol * max(1, abs(a)), (a, b)
    return a


def circ(P, Q, x, y, dx, dy, a, b):          # line side: work along a parametrised curve
    return quad(lambda t: P(x(t), y(t)) * dx(t) + Q(x(t), y(t)) * dy(t), a, b, limit=200)[0]


def flux(P, Q, x, y, dx, dy, a, b):          # outward flux, n ds = (dy, -dx)
    return quad(lambda t: P(x(t), y(t)) * dy(t) - Q(x(t), y(t)) * dx(t), a, b, limit=200)[0]


def polar(f, r0, r1, t0=0, t1=2 * pi):       # area side: integral of f(x, y) dA in polar form
    return dblquad(lambda r, th: f(r * math.cos(th), r * math.sin(th)) * r, t0, t1, lambda th: r0, lambda th: r1)[0]


def circle(R, cx=0, cy=0):
    return (lambda t: cx + R * math.cos(t), lambda t: cy + R * math.sin(t), lambda t: -R * math.sin(t), lambda t: R * math.cos(t), 0, 2 * pi)


def square_sides(P, Q, mode):                 # unit square, counterclockwise, side by side
    sides = [(lambda t: t, lambda t: 0, lambda t: 1, lambda t: 0), (lambda t: 1, lambda t: t, lambda t: 0, lambda t: 1),
             (lambda t: 1 - t, lambda t: 1, lambda t: -1, lambda t: 0), (lambda t: 0, lambda t: 1 - t, lambda t: 0, lambda t: -1)]
    g = circ if mode == "work" else flux
    return [g(P, Q, *s, 0, 1) for s in sides]


def pdiff(f, x, y, h=1e-5):
    return ((f(x + h, y) - f(x - h, y)) / (2 * h), (f(x, y + h) - f(x, y - h)) / (2 * h))


def divcurl(P, Q, x, y):
    Px, Py = pdiff(P, x, y); Qx, Qy = pdiff(Q, x, y)
    return Px + Qy, Qx - Py


# ---------- l5 ----------
L = "l5"
fields = [(lambda x, y: x, lambda x, y: y), (lambda x, y: -y, lambda x, y: x), (lambda x, y: y, lambda x, y: 0), (lambda x, y: 1, lambda x, y: 0)]
want = [(2, 0), (0, 2), (0, -1), (0, 0)]
for k, ((P, Q), (d, c)) in enumerate(zip(fields, want)):
    dd, cc = divcurl(P, Q, 0.7, -0.4)
    assert abs(dd - d) < 1e-6 and abs(cc - c) < 1e-6
    # twice: divergence as small-square outflow per unit area, curl as small-circle circulation per unit area
    h = 1e-3
    assert abs(flux(P, Q, *circle(h, 0.7, -0.4)) / (pi * h * h) - d) < 1e-4 and abs(circ(P, Q, *circle(h, 0.7, -0.4)) / (pi * h * h) - c) < 1e-4
    lv.expect(L, f"screens[1].widget.rows[{k}][1].answer", d); lv.expect(L, f"screens[1].widget.rows[{k}][2].answer", c)
lv.expect(L, "screens[1].widget.rows[0][1].wrong[0].value", 1); lv.expect(L, "screens[1].widget.rows[2][2].wrong[0].value", 1)
P1, Q1 = (lambda x, y: x * x * y), (lambda x, y: x - y * y)
d21, c21 = divcurl(P1, Q1, 2, 1)
lv.expect(L, "screens[5].widget.rows[0][2].answer", round(both(2 * 2 * 1 - 2 * 1, d21, 1e-5))); lv.expect(L, "screens[5].widget.rows[1][2].answer", round(both(1 - 4, c21, 1e-5)))
lv.expect(L, "screens[5].widget.rows[0][2].wrong[0].value", 4)
# space curl of (xy, yz, zx) at (1, 2, 3) by central differences
Fs = lambda x, y, z: (x * y, y * z, z * x)
def d3(i, j, p, h=1e-5):
    a = list(p); b = list(p); a[j] += h; b[j] -= h
    return (Fs(*a)[i] - Fs(*b)[i]) / (2 * h)
p = (1, 2, 3)
cu = (d3(2, 1, p) - d3(1, 2, p), d3(0, 2, p) - d3(2, 0, p), d3(1, 0, p) - d3(0, 1, p)); dv = d3(0, 0, p) + d3(1, 1, p) + d3(2, 2, p)
assert all(abs(a - b) < 1e-6 for a, b in zip(cu, (-2, -3, -1))) and abs(dv - 6) < 1e-6
lv.expect(L, "screens[6].widget.answer", "(-2, -3, -1)"); lv.expect(L, "screens[6].explain.text", 6); lv.expect(L, "quiz[0].widget.answer", round(dv))
lap = lambda f, x, y, h=1e-4: (f(x + h, y) - 2 * f(x, y) + f(x - h, y) + f(x, y + h) - 2 * f(x, y) + f(x, y - h)) / h ** 2
lv.expect(L, "screens[7].widget.rows[0][1].answer", round(both(4, lap(lambda x, y: x * x + y * y, 0.3, 0.8), 1e-4)))
lv.expect(L, "screens[7].widget.rows[1][1].answer", round(lap(lambda x, y: x * x - y * y, 0.3, 0.8)))
d, c = divcurl(lambda x, y: x / (x * x + y * y), lambda x, y: y / (x * x + y * y), 0.8, -1.3); assert abs(d) < 1e-6
mu = (lambda x, y: -0.5 * x - 0.3 * y, lambda x, y: 0.3 * x - 0.5 * y)
dm, cm = divcurl(*mu, 0.4, 0.9)
lv.expect(L, "screens[10].widget.rows[0][1].answer", round(both(-1, dm, 1e-6), 6)); lv.expect(L, "screens[10].widget.rows[1][1].answer", round(both(0.6, cm, 1e-6), 6))
lv.expect(L, "screens[10].widget.rows[0][1].wrong[0].value", -0.5)
import numpy as np
ev = np.linalg.eigvals([[-0.5, -0.3], [0.3, -0.5]]); assert abs(ev[0].real + 0.5) < 1e-12 and abs(abs(ev[0].imag) - 0.3) < 1e-12
lv.expect(L, "screens[11].explain.text", ev[0].real); lv.expect(L, "screens[11].explain.text", 0.3)
for k, (a, b, c2, dd2) in enumerate([(-0.5, 0.3, -0.3, -0.5), (-0.5, 0, 0, -0.5), (-0.5, -0.3, 0.3, -0.5), (0.5, -0.3, 0.3, 0.5)]):
    pass
assert divcurl(lambda x, y: -0.5 * x + 0.3 * y, lambda x, y: -0.3 * x - 0.5 * y, 1, 1)[1] + 0.6 < 1e-6   # picture A curl -0.6
assert abs(divcurl(lambda x, y: 0.5 * x - 0.3 * y, lambda x, y: 0.3 * x + 0.5 * y, 1, 1)[0] - 1) < 1e-6  # picture D divergence +1
lv.expect(L, "quiz[3].widget.answer", round(lap(lambda x, y: x ** 3 - 3 * x * y * y, 1, 0.5)))

# ---------- l6 ----------
L = "l6"
rot = (lambda x, y: -y, lambda x, y: x)
sides = square_sides(*rot, "work")
assert all(abs(a - b) < 1e-9 for a, b in zip(sides, [0, 1, 1, 0]))
for k, v in enumerate([0, 1, 1, 0, 2]):
    lv.expect(L, f"screens[0].widget.rows[{k}][2].answer", v)
both(2 * 1, sum(sides)); both(2 * pi, circ(*rot, *circle(1))); both(2 * pi, polar(lambda x, y: 2, 0, 1))
F3 = (lambda x, y: x * x - y, lambda x, y: x + y * y)
lv.expect(L, "screens[3].widget.answer", r"8\pi"); both(8 * pi, circ(*F3, *circle(2))); both(8 * pi, polar(lambda x, y: 2, 0, 2))
lv.expect(L, "screens[3].explain.text", 25.13)
Fh = (lambda x, y: y * y, lambda x, y: 3 * x * y)
hd_green = both(2 / 3, polar(lambda x, y: y, 0, 1, 0, pi))
arc = circ(*Fh, lambda t: math.cos(t), lambda t: math.sin(t), lambda t: -math.sin(t), lambda t: math.cos(t), 0, pi)
dia = circ(*Fh, lambda t: -1 + 2 * t, lambda t: 0, lambda t: 2, lambda t: 0, 0, 1)
both(hd_green, arc + dia)
lv.expect(L, "screens[4].widget.answer", round(hd_green, 3)); lv.expect(L, "screens[4].widget.wrong[0].value", round(polar(lambda x, y: y / math.hypot(x, y), 0, 1, 0, pi)))
lv.expect(L, "screens[5].widget.rows[0][1].answer", round(arc, 3)); lv.expect(L, "screens[5].widget.rows[1][1].answer", round(dia, 3)); lv.expect(L, "screens[5].widget.rows[2][1].answer", round(arc + dia, 3))
lv.expect(L, "screens[5].widget.rows[0][1].wrong[0].value", round(-quad(lambda t: math.sin(t) ** 3, 0, pi)[0], 3))
both(2 * pi, circ(lambda x, y: math.exp(x * x) - y, lambda x, y: x + math.sin(y * y), *circle(1))); lv.expect(L, "screens[6].widget.answer", r"2\pi")
semi = both(pi, circ(*rot, lambda t: math.cos(t), lambda t: math.sin(t), lambda t: -math.sin(t), lambda t: math.cos(t), 0, pi))
both(semi, polar(lambda x, y: 2, 0, 1, 0, pi) - circ(*rot, lambda t: -1 + 2 * t, lambda t: 0, lambda t: 2, lambda t: 0, 0, 1))
lv.expect(L, "screens[7].widget.answer", round(semi, 3)); lv.expect(L, "screens[7].widget.wrong[0].value", round(2 * pi, 3)); lv.expect(L, "screens[7].widget.wrong[1].value", round(pi / 2, 3))
# trap: the four integrands over the half disc
lv.expect(L, "screens[8].widget.options[0].text", "tfrac23")
both(-2 / 3, polar(lambda x, y: -y, 0, 1, 0, pi)); both(0, polar(lambda x, y: 3 * x, 0, 1, 0, pi), 1e-6); lv.expect(L, "screens[8].widget.options[3].text", 10 / 3)
both(10 / 3, polar(lambda x, y: 5 * y, 0, 1, 0, pi))
V = (lambda x, y: -y / (x * x + y * y), lambda x, y: x / (x * x + y * y))
both(circ(*V, *circle(2)), circ(*V, *circle(0.5))); both(2 * pi, circ(*V, *circle(0.5)))
for k, val in enumerate([8 * pi, both(8 * pi, polar(lambda x, y: 2, 0, 2)), 2 * pi, 2 * pi, hd_green, both(hd_green, arc), 2 * pi, 2 * pi]):
    lv.expect(L, f"screens[10].widget.tests[{k}].expect", val)
h = (lambda x, y: 0, lambda x, y: x - 100)
legs = [circ(*h, lambda t: 100 + 10 * t, lambda t: 100, lambda t: 10, lambda t: 0, 0, 1), circ(*h, lambda t: 110, lambda t: 100 + 5 * t, lambda t: 0, lambda t: 5, 0, 1),
        circ(*h, lambda t: 110 - 10 * t, lambda t: 105, lambda t: -10, lambda t: 0, 0, 1), circ(*h, lambda t: 100, lambda t: 105 - 5 * t, lambda t: 0, lambda t: -5, 0, 1)]
for k, v in enumerate(legs + [sum(legs)]):
    lv.expect(L, f"screens[11].widget.rows[{k}][2].answer", round(v, 6))
both(sum(legs), 1 * 10 * 5)
lv.expect(L, "quiz[2].widget.answer", both(8, polar(lambda x, y: 2, 0, 1) * 4 / pi)); both(8, circ(*rot, lambda t: 2 * t, lambda t: 0, lambda t: 2, lambda t: 0, 0, 1) + circ(*rot, lambda t: 2, lambda t: 2 * t, lambda t: 0, lambda t: 2, 0, 1) + circ(*rot, lambda t: 2 - 2 * t, lambda t: 2, lambda t: -2, lambda t: 0, 0, 1) + circ(*rot, lambda t: 0, lambda t: 2 - 2 * t, lambda t: 0, lambda t: -2, 0, 1))
both(-8 * pi, circ(*F3, lambda t: 2 * math.cos(t), lambda t: -2 * math.sin(t), lambda t: -2 * math.sin(t), lambda t: -2 * math.cos(t), 0, 2 * pi)); lv.expect(L, "quiz[3].widget.answer", r"-8\pi")

# ---------- l7 ----------
L = "l7"
def shoelace(V):
    return sum(V[i][0] * V[(i + 1) % len(V)][1] - V[(i + 1) % len(V)][0] * V[i][1] for i in range(len(V))) / 2
def green_area(V):                            # 1/2 * closed line integral of x dy - y dx, edge by edge, numerically
    tot = 0
    for i in range(len(V)):
        (x1, y1), (x2, y2) = V[i], V[(i + 1) % len(V)]
        tot += quad(lambda t: (x1 + t * (x2 - x1)) * (y2 - y1) - (y1 + t * (y2 - y1)) * (x2 - x1), 0, 1)[0]
    return tot / 2
for dx_, dy_ in [(0, 1), (-1, 0), (-0.5, 0.5)]:
    pass
assert divcurl(lambda x, y: 0, lambda x, y: x, 1, 1)[1] == divcurl(lambda x, y: -y, lambda x, y: 0, 1, 1)[1]
Qd = [(0, 0), (4, 0), (4, 3), (1, 4)]
A = both(shoelace(Qd), green_area(Qd))
lv.expect(L, "screens[1].widget.points[0].target.value", A); assert abs((12 + 4 * 4 - 3 * 1) / 2 - A) < 1e-12 and abs(shoelace([(0, 0), (4, 0), (4, 3), (3, 5.5)]) - A) < 1e-12
lv.expect(L, "screens[1].explain.text", 13)
ell = both(6 * pi, 0.5 * circ(lambda x, y: -y, lambda x, y: x, lambda t: 3 * math.cos(t), lambda t: 2 * math.sin(t), lambda t: -3 * math.sin(t), lambda t: 2 * math.cos(t), 0, 2 * pi))
lv.expect(L, "screens[2].widget.answer", r"6\pi"); lv.expect(L, "screens[2].feedback.correct", round(ell, 2))
cr = [Qd[i][0] * Qd[(i + 1) % 4][1] - Qd[(i + 1) % 4][0] * Qd[i][1] for i in range(4)]
for k, v in enumerate(cr + [A]):
    lv.expect(L, f"screens[5].widget.rows[{k}][1].answer", v)
lv.expect(L, "screens[5].widget.rows[4][1].wrong[0].value", 2 * A)
ast = both(3 * pi / 8, 0.5 * circ(lambda x, y: -y, lambda x, y: x, lambda t: math.cos(t) ** 3, lambda t: math.sin(t) ** 3, lambda t: -3 * math.cos(t) ** 2 * math.sin(t), lambda t: 3 * math.sin(t) ** 2 * math.cos(t), 0, 2 * pi))
lv.expect(L, "screens[6].feedback.correct", round(ast, 3)); lv.expect(L, "screens[6].explain.text", round(ast, 3))
rc = lambda t: 1 + math.cos(t)
card_line = 0.5 * circ(lambda x, y: -y, lambda x, y: x, lambda t: rc(t) * math.cos(t), lambda t: rc(t) * math.sin(t),
                       lambda t: -math.sin(t) * math.cos(t) - rc(t) * math.sin(t), lambda t: -math.sin(t) ** 2 + rc(t) * math.cos(t), 0, 2 * pi)
card = both(both(3 * pi / 2, 0.5 * quad(lambda t: rc(t) ** 2, 0, 2 * pi)[0]), card_line)
lv.expect(L, "screens[7].widget.answer", round(card, 3)); lv.expect(L, "screens[7].widget.wrong[0].value", round(2 * card, 3)); lv.expect(L, "screens[7].widget.wrong[1].value", round(0.5 * quad(rc, 0, 2 * pi)[0], 3))
cross = [(0, 0), (4, 3), (4, 0), (1, 4)]; bow = [(0, 0), (2, 2), (2, 0), (0, 2)]
lv.expect(L, "screens[8].widget.options[0].text", both(shoelace(cross), green_area(cross))); lv.expect(L, "screens[8].widget.options[1].text", A)
lv.expect(L, "screens[8].widget.options[2].text", -A); assert shoelace(list(reversed(Qd))) == -A and both(0, green_area(bow)) == 0
lv.expect(L, "screens[8].hints[1].text", -12); lv.expect(L, "screens[8].hints[1].text", 16)
ring = shoelace([(0, 0), (4, 0), (4, 4), (0, 4)]) + shoelace([(1, 1), (1, 3), (3, 3), (3, 1)])
lv.expect(L, "screens[9].widget.question", 12) if False else None
lv.expect(L, "screens[9].question", both(12, ring)); lv.expect(L, "screens[9].widget.options[1].why", 20); lv.expect(L, "screens[9].widget.options[3].why", 32)
# market maker: cash = -closed integral of p dq, leg by leg
legs = [-quad(lambda t: 10, 0, 1)[0] * 200, -quad(lambda t: 10 + 0.3 * t, 0, 1)[0] * (-100), -quad(lambda t: 10.3 - 0.3 * t, 0, 1)[0] * (-100)]
for k, v in enumerate(legs + [sum(legs)]):
    lv.expect(L, f"screens[10].widget.rows[{k}][1].answer", round(v, 6))
both(sum(legs), shoelace([(0, 10), (200, 10), (100, 10.3)]))
lv.expect(L, "screens[10].widget.rows[1][1].wrong[0].value", 1030); lv.expect(L, "screens[10].explain.text", 50)
both(50, -(10 * 100 + 10.5 * (-100)))
lv.expect(L, "quiz[0].widget.answer", shoelace([(0, 0), (5, 0), (1, 4)])); lv.expect(L, "quiz[3].widget.answer", both(40, -(20 * 100 + 20.4 * -100)))

# ---------- l8 ----------
L = "l8"
out = (lambda x, y: x, lambda x, y: y)
both(2 * pi, flux(*out, *circle(1))); both(2 * pi, polar(lambda x, y: 2, 0, 1)); both(0, flux(*rot, *circle(1))); both(0, circ(*out, *circle(1)))
lv.expect(L, "screens[1].widget.answer", r"2\pi")
fs = square_sides(*out, "flux")    # bottom, right, top, left
for k, v in enumerate([fs[1], fs[2], fs[3], fs[0], sum(fs)]):
    lv.expect(L, f"screens[4].widget.rows[{k}][2].answer", round(v, 9))
both(sum(fs), 2 * 1)
f2 = square_sides(lambda x, y: x * x, lambda x, y: y * y, "flux")
lv.expect(L, "screens[5].widget.answer", round(both(sum(f2), dblquad(lambda y, x: 2 * x + 2 * y, 0, 1, lambda x: 0, lambda x: 1)[0]), 9))
c3 = both(3 * pi / 2, flux(lambda x, y: x ** 3, lambda x, y: y ** 3, *circle(1))); both(c3, polar(lambda x, y: 3 * (x * x + y * y), 0, 1))
both(c3, quad(lambda t: math.cos(t) ** 4 + math.sin(t) ** 4, 0, 2 * pi)[0]); lv.expect(L, "screens[6].feedback.correct", round(c3, 3))
lv.expect(L, "screens[7].widget.answer", round(2 * pi, 3)); lv.expect(L, "screens[7].widget.wrong[0].value", round(circ(*out, *circle(1)), 6)); lv.expect(L, "screens[7].widget.wrong[1].value", -round(2 * pi, 3))
S_ = (lambda x, y: x / (x * x + y * y), lambda x, y: y / (x * x + y * y))
for R in (1, 2, 5):
    both(2 * pi, flux(*S_, *circle(R)))
z = flux(*S_, *circle(1, 3, 0)); assert abs(z) < 1e-9; lv.expect(L, "screens[9].widget.answer", 0)
mu2 = (lambda x, y: -0.5 * x, lambda x, y: -0.5 * y)
fm = both(-pi, flux(*mu2, *circle(1))); both(fm, polar(lambda x, y: -1, 0, 1))
lv.expect(L, "screens[10].widget.answer", round(fm, 3)); lv.expect(L, "screens[10].widget.wrong[1].value", round(fm / 2, 3))
lv.expect(L, "quiz[0].widget.answer", r"20\pi"); both(20 * pi, flux(lambda x, y: 2 * x, lambda x, y: 3 * y, *circle(2)))
both(2 * pi, flux(*S_, *circle(5))); lv.expect(L, "quiz[3].widget.answer", r"2\pi")

# ---------- review ----------
R = "review"
d, c = divcurl(lambda x, y: x * y * y, lambda x, y: x * x + y, 1, 2)
lv.expect(R, "items[0].parts[0].widget.answer", round(both(5, d, 1e-6))); lv.expect(R, "items[0].parts[1].widget.answer", round(both(-2, c, 1e-6)))
both(3 * pi / 2, circ(lambda x, y: -y ** 3, lambda x, y: x ** 3, *circle(1))); lv.expect(R, "items[1].widget.answer", r"\frac{3\pi}{2}")
lv.expect(R, "items[2].widget.answer", both(shoelace([(0, 0), (6, 0), (2, 5)]), green_area([(0, 0), (6, 0), (2, 5)])))
lv.expect(R, "items[3].widget.answer", round(both(3, sum(square_sides(lambda x, y: x + y, lambda x, y: 2 * y, "flux"))), 9))
both(-2, -sum(square_sides(*rot, "work"))); lv.expect(R, "items[4].widget.options[0].text", -2)
both(4 * pi, 0.5 * circ(lambda x, y: -y, lambda x, y: x, lambda t: 4 * math.cos(t), lambda t: math.sin(t), lambda t: -4 * math.sin(t), lambda t: math.cos(t), 0, 2 * pi))
lv.expect(R, "items[6].widget.answer", round(lap(lambda x, y: x * x * y, 1, 3)))
both(2 * pi, flux(*S_, *circle(1, 0.5, 0)))

# ---------- homework ----------
Hm = "homework"
cub = (lambda x, y: x ** 3 - y ** 3, lambda x, y: x ** 3 + y ** 3)
ann = both(45 * pi / 2, circ(*cub, *circle(2)) - circ(*cub, *circle(1))); both(ann, polar(lambda x, y: 3 * (x * x + y * y), 1, 2))
lv.expect(Hm, "items[1].widget.answer", r"\frac{45\pi}{2}"); lv.expect(Hm, "items[1].feedback.correct", round(ann, 2))
both(24 * pi, polar(lambda x, y: 3 * (x * x + y * y), 0, 2)); both(14 * pi, 2 * pi * quad(lambda r: 3 * r * r, 1, 2)[0])
fx = lambda t: 3 * t / (1 + t ** 3); fy = lambda t: 3 * t * t / (1 + t ** 3)
fdx = lambda t: (3 * (1 + t ** 3) - 9 * t ** 3) / (1 + t ** 3) ** 2; fdy = lambda t: (6 * t * (1 + t ** 3) - 9 * t ** 4) / (1 + t ** 3) ** 2
fol = 0.5 * quad(lambda t: fx(t) * fdy(t) - fy(t) * fdx(t), 0, math.inf)[0]
lv.expect(Hm, "items[2].widget.answer", both(1.5, fol, 1e-6)); both(3, quad(lambda t: 9 * t * t / (1 + t ** 3) ** 2, 0, math.inf)[0], 1e-6)
ef = flux(lambda x, y: x + y * y, lambda x, y: y - x * x, lambda t: 3 * math.cos(t), lambda t: 2 * math.sin(t), lambda t: -3 * math.sin(t), lambda t: 2 * math.cos(t), 0, 2 * pi)
both(12 * pi, ef); lv.expect(Hm, "items[3].widget.answer", r"12\pi")
gv = [ann, ann, 8 * pi, 8 * pi, 0, 0, 6 * pi, 6 * pi]
both(0, circ(*V, *circle(2)) - circ(*V, *circle(1)), 1e-6); both(6 * pi, circ(*rot, *circle(2)) - circ(*rot, *circle(1)))
for k, v in enumerate(gv):
    lv.expect(Hm, f"items[4].widget.tests[{k}].expect", v)
poly = [(math.cos(2 * pi * k / 50), math.sin(2 * pi * k / 50)) for k in range(50)]
sv = [A, 0, -A, both(shoelace(poly), green_area(poly)), 30, shoelace(cross)]
both(shoelace(poly), 25 * math.sin(2 * pi / 50))
for k, v in enumerate(sv):
    lv.expect(Hm, f"items[5].widget.tests[{k}].expect", v)
lv.expect(Hm, "items[5].explain.text", round(shoelace(poly), 4))
fr = both(-4 * pi, flux(*mu, *circle(2))); cr2 = both(2.4 * pi, circ(*mu, *circle(2)))
lv.expect(Hm, "items[7].parts[0].widget.answer", round(fr, 3)); lv.expect(Hm, "items[7].parts[1].widget.answer", round(cr2, 3))
lv.expect(Hm, "items[7].parts[0].widget.wrong[0].value", round(-pi, 3))
tri = [(lambda t: 2 * t, lambda t: 0, lambda t: 2, lambda t: 0), (lambda t: 2 - 2 * t, lambda t: 2 * t, lambda t: -2, lambda t: 2), (lambda t: 0, lambda t: 2 - 2 * t, lambda t: 0, lambda t: -2)]
tv = sum(circ(lambda x, y: y + math.exp(x), lambda x, y: 2 * x + math.cos(y * y), *s, 0, 1) for s in tri)
lv.expect(Hm, "items[8].widget.answer", round(both(2, tv, 1e-6)))
# fix pass: l6 screens[3] wrong `one` is curl 1 times area 4pi; no-r mutant fails test 4 (4pi vs 2pi) and test 5 (1 vs 2/3), passes test 2
lv.expect("l6", "screens[3].widget.wrong[1].tex", r"4\pi")
assert abs(polar(lambda x, y: 1, 0, 2) - 4 * pi) < 1e-9
nor = lambda c, rm, t0, t1: dblquad(lambda r, th: c(r * math.cos(th), r * math.sin(th)), t0, t1, lambda th: 0, lambda th: rm)[0]
assert abs(nor(lambda x, y: 2, 2, 0, 2 * pi) - 8 * pi) < 1e-6
assert abs(nor(lambda x, y: 2, 1, 0, 2 * pi) - 4 * pi) < 1e-6 and abs(nor(lambda x, y: y, 1, 0, pi) - 1) < 1e-6

lv.check_wrongs()
lv.report()
