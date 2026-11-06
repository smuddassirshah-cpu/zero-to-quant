"""Recompute every stated number of vector-calc level 3 twice: by the theorem (divergence theorem, Stokes, the graph
formula or a closed form) and by direct parametrised integration with SciPy, then check it in the JSON at its path.
Run: python3 docs/reports/vector-calc-L3-numbers.py   (exits 0 when every check passes)
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level
from scipy.integrate import quad, dblquad, tplquad

lv = Level("vector-calc", 3)
pi, sin, cos, sqrt = math.pi, math.sin, math.cos, math.sqrt


def both(a, b, tol=1e-7):
    assert abs(a - b) <= tol * max(1, abs(a)), (a, b)
    return a


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return sqrt(dot(a, a))


def d_u(r, u, v, h=1e-6):
    return tuple((p - q) / (2 * h) for p, q in zip(r(u + h, v), r(u - h, v)))


def d_v(r, u, v, h=1e-6):
    return tuple((p - q) / (2 * h) for p, q in zip(r(u, v + h), r(u, v - h)))


def area(r, u0, u1, v0, v1):                      # direct: |r_u x r_v| by numerical partials
    return dblquad(lambda v, u: norm(cross(d_u(r, u, v), d_v(r, u, v))), u0, u1, lambda u: v0, lambda u: v1)[0]


def sint(f, r, u0, u1, v0, v1):                   # surface integral of a scalar
    return dblquad(lambda v, u: f(*r(u, v)) * norm(cross(d_u(r, u, v), d_v(r, u, v))), u0, u1, lambda u: v0, lambda u: v1)[0]


def flux(F, r, u0, u1, v0, v1):                    # flux with normal r_u x r_v
    return dblquad(lambda v, u: dot(F(*r(u, v)), cross(d_u(r, u, v), d_v(r, u, v))), u0, u1, lambda u: v0, lambda u: v1)[0]


def work(F, r, t0, t1, h=1e-6):
    return quad(lambda t: dot(F(*r(t)), tuple((p - q) / (2 * h) for p, q in zip(r(t + h), r(t - h)))), t0, t1, limit=200)[0]


def ball(f, R=1, ph1=pi):                          # theorem side: integral over a ball in spherical coordinates
    return tplquad(lambda rho, ph, th: f(rho * sin(ph) * cos(th), rho * sin(ph) * sin(th), rho * cos(ph)) * rho * rho * sin(ph),
                   0, 2 * pi, lambda th: 0, lambda th: ph1, lambda th, ph: 0, lambda th, ph: R)[0]


def box(f, x0, x1, y0, y1, z0, z1):
    return tplquad(lambda z, y, x: f(x, y, z), x0, x1, lambda x: y0, lambda x: y1, lambda x, y: z0, lambda x, y: z1)[0]


def curl(F, x, y, z, h=1e-5):
    def p(i, j):                                    # d F_i / d x_j
        e = [0, 0, 0]; e[j] = h
        return (F(x + e[0], y + e[1], z + e[2])[i] - F(x - e[0], y - e[1], z - e[2])[i]) / (2 * h)
    return (p(2, 1) - p(1, 2), p(0, 2) - p(2, 0), p(1, 0) - p(0, 1))


def div(F, x, y, z, h=1e-5):
    return sum((F(*[c + (h if k == j else 0) for k, c in enumerate((x, y, z))])[j] - F(*[c - (h if k == j else 0) for k, c in enumerate((x, y, z))])[j]) / (2 * h) for j in range(3))


sph = lambda R=1: (lambda u, v: (R * sin(u) * cos(v), R * sin(u) * sin(v), R * cos(u)))
circ = lambda t: (cos(t), sin(t), 0)

# ---------- l9 ----------
L = "l9"
c = cross((1, 0, 2), (0, 1, 3)); assert c == (-2, -3, 1) and dot(c, (1, 0, 2)) == 0 and dot(c, (0, 1, 3)) == 0
lv.expect(L, "screens[3].widget.answer", "(-2, -3, 1)"); lv.expect(L, "screens[3].widget.wrong[0].tex", "(2, 3, -1)")
lv.expect(L, "screens[3].explain.text", round(both(sqrt(14), norm(c)), 3))
lv.expect(L, "screens[4].widget.options[0].text", "(2, 3, -1)"); assert cross((0, 1, 3), (1, 0, 2)) == (2, 3, -1)
cyl = lambda u, v: (2 * cos(u), 2 * sin(u), v)
assert abs(norm(cross(d_u(cyl, 1.0, 1.0), d_v(cyl, 1.0, 1.0))) - 2) < 1e-8
lv.expect(L, "screens[1].explain.text", 1.2); lv.expect(L, "screens[1].explain.text", 0.3); lv.expect(L, "screens[1].explain.text", 0.6)
assert abs(2 * 0.6 - 1.2) < 1e-12 and abs(0.6 * 0.5 - 0.3) < 1e-12 and abs(1.2 * 0.5 - 0.6) < 1e-12
assert abs(area(lambda u, v: (2.04 * cos(u), 2.04 * sin(u), v), 1.5, 2.1, 2, 2.5) / (0.6 * 0.5) - 2.04) < 1e-6   # marked patch
assert abs(2 * pi - 2.1 - 4.18) < 0.01 and abs(2 * pi - 1.5 - 4.78) < 0.01 and abs(3 - 2.5 - 0.5) < 1e-12        # distractor patches
rt = d_u(cyl, pi / 2, 1.5); assert all(abs(a - b) < 1e-6 for a, b in zip(rt, (-2, 0, 0)))
lv.expect(L, "screens[2].widget.answer", "(-2, 0, 0)")
A = both(12 * pi, area(cyl, 0, 2 * pi, 0, 3), 1e-6); lv.expect(L, "screens[6].widget.answer", "12\\pi")
lv.expect(L, "screens[6].feedback.correct", round(A, 2)); lv.expect(L, "screens[6].widget.wrong[0].tex", "6\\pi"); lv.expect(L, "screens[6].widget.wrong[1].tex", "20\\pi")
assert abs(12 * pi + 2 * 4 * pi - 20 * pi) < 1e-12 and abs(2 * pi * 3 - 6 * pi) < 1e-12
g = both(sqrt(14), area(lambda u, v: (u, v, 2 * u + 3 * v), 0, 1, 0, 1), 1e-6)
lv.expect(L, "screens[7].widget.answer", round(g, 3)); lv.expect(L, "screens[7].widget.wrong[2].value", round(sqrt(13), 3))
S4 = both(4 * pi, area(sph(), 0, pi, 0, 2 * pi), 1e-6); lv.expect(L, "screens[8].widget.answer", "4\\pi")
lv.expect(L, "screens[9].widget.answer", round(both(2 * pi * pi, dblquad(lambda v, u: 1, 0, pi, lambda u: 0, lambda u: 2 * pi)[0]), 2))
lv.expect(L, "screens[9].widget.wrong[1].value", round(S4, 2))
dotv = dblquad(lambda v, u: abs(dot(d_u(sph(), u, v), d_v(sph(), u, v))), 0.01, pi - 0.01, lambda u: 0, lambda u: 2 * pi)[0]
assert abs(dotv) < 1e-6; lv.expect(L, "screens[9].widget.wrong[0].value", 0)
assert abs(area(sph(), 0, pi, 0, 4 * pi) - 8 * pi) < 1e-5; lv.expect(L, "screens[10].prose", "8\\pi")
assert norm(cross(d_u(sph(), 1e-9, 1.0), d_v(sph(), 1e-9, 1.0))) < 1e-6
tri = both(sqrt(3) / 2, area(lambda u, v: (u, v * (1 - u), 1 - u - v * (1 - u)), 0, 1, 0, 1), 1e-6)
lv.expect(L, "screens[11].widget.answer", round(tri, 3)); lv.expect(L, "screens[11].widget.wrong[1].value", round(sqrt(3), 3))
assert abs(norm((1, -1, 0)) - sqrt(2)) < 1e-12 and abs(sqrt(3) / 4 * 2 - tri) < 1e-12       # equilateral, side sqrt 2
par = both(pi / 6 * (5 * sqrt(5) - 1), area(lambda u, v: (u * cos(v), u * sin(v), u * u), 0, 1, 0, 2 * pi), 1e-6)
lv.expect(L, "quiz[0].widget.answer", round(par, 3)); lv.expect(L, "quiz[0].widget.wrong[0].value", round(pi, 3))
cone = both(sqrt(2) * pi, area(lambda u, v: (u * cos(v), u * sin(v), u), 0, 1, 0, 2 * pi), 1e-6)
lv.expect(L, "quiz[1].widget.answer", round(cone, 3)); lv.expect(L, "quiz[1].widget.wrong[1].value", round(2 * pi, 3))
dens = 2 / sqrt(3); assert abs(dens * tri - 1) < 1e-12 and abs(2 * 0.5 - 1) < 1e-12 and abs(2 * sqrt(3) * tri - 3) < 1e-12
lv.expect(L, "quiz[4].widget.options[1].text", 2)

# ---------- l10 ----------
L = "l10"
roof = lambda u, v: (u, v, u)
lv.expect(L, "screens[0].widget.answer", both(-1, flux(lambda x, y, z: (0, 0, -1), roof, 0, 1, 0, 1)))
lv.expect(L, "screens[0].widget.wrong[0].value", -round(both(sqrt(2), area(roof, 0, 1, 0, 1), 1e-6), 3))
for a in (0.3, 2):
    assert abs(flux(lambda x, y, z: (0, 0, -1), lambda u, v: (u, v, a * u), 0, 1, 0, 1) + 1) < 1e-8
zh = both(pi, sint(lambda x, y, z: z, sph(), 0, pi / 2, 0, 2 * pi), 1e-6); lv.expect(L, "screens[2].widget.answer", "\\pi")
assert abs(dblquad(lambda v, u: cos(u), 0, pi / 2, lambda u: 0, lambda u: 2 * pi)[0] - 2 * pi) < 1e-8   # no-dS slip
lv.expect(L, "quiz[0].widget.answer", both(0.5, zh / area(sph(), 0, pi / 2, 0, 2 * pi), 1e-6))
lv.expect(L, "quiz[0].widget.wrong[1].value", both(0.375, ball(lambda x, y, z: z, 1, pi / 2) / (2 * pi / 3), 1e-6))
F = lambda x, y, z: (x, y, z)
lv.expect(L, "screens[3].widget.answer", "2\\pi"); both(2 * pi, flux(F, sph(), 0, pi / 2, 0, 2 * pi), 1e-6); both(4 * pi, flux(F, sph(), 0, pi, 0, 2 * pi), 1e-6)
fz = both(2 * pi / 3, flux(lambda x, y, z: (0, 0, z), sph(), 0, pi / 2, 0, 2 * pi), 1e-6)
lv.expect(L, "screens[4].widget.answer", round(fz, 3)); lv.expect(L, "screens[4].widget.wrong[0].value", round(both(4 * pi / 3, ball(lambda x, y, z: 1)), 3))
lv.expect(L, "screens[4].widget.wrong[1].value", round(zh, 3))
pb = lambda u, v: (u * cos(v), u * sin(v), 1 - u * u)
fp = both(1.5 * pi, flux(F, pb, 0, 1, 0, 2 * pi), 1e-6); lv.expect(L, "screens[5].widget.answer", round(fp, 3))
lv.expect(L, "screens[5].widget.wrong[1].value", round(both(-pi / 2, dblquad(lambda r, t: (1 - 3 * r * r) * r, 0, 2 * pi, lambda t: 0, lambda t: 1)[0]), 3))
swapped = lambda u, v: sph()(v, u)
lv.expect(L, "screens[7].prose", round(both(-4 * pi, flux(F, swapped, 0, 2 * pi, 0, pi), 1e-6) / pi))
lv.expect(L, "screens[7].widget.options[2].why", both(2 * pi, sint(lambda x, y, z: abs(z), sph(), 0, pi, 0, 2 * pi), 1e-6) / pi)
lv.expect(L, "screens[7].widget.options[2].why", "\\tfrac{4\\pi}{3}"); both(4 * pi / 3, flux(lambda x, y, z: (0, 0, z), sph(), 0, pi, 0, 2 * pi), 1e-6)
assert abs(flux(lambda x, y, z: (-y, x, 0), lambda u, v: (1.5 * cos(u), 1.5 * sin(u), v), 0, 2 * pi, 0, 2)) < 1e-9
lv.expect(L, "screens[8].widget.options[2].text", 1.5); assert abs(area(lambda u, v: (1.5 * cos(u), 1.5 * sin(u), v), 0, 2 * pi, 0, 2) - 6 * pi) < 1e-6
assert abs(work(lambda x, y, z: (-y, x, 0), lambda t: (1.5 * cos(t), 1.5 * sin(t), 0), 0, 2 * pi) - 2 * pi * 1.5 ** 2) < 1e-6
code = lv.files["l10-surface-integrals"]["screens"][9]["widget"]
exp = [4 * pi, 2 * pi, 2 * pi / 3, 1.5 * pi, -1, -4 * pi]
for t, e in zip(code["tests"], exp):
    assert abs(float(t["expect"]) - e) < 1e-12
ns = {}; exec(code["prelude"], ns); exec(code["solution"], ns)
for t in code["tests"]:
    assert abs(eval(t["call"], ns) - float(t["expect"])) < 1e-6, t["call"]
ns2 = {}; exec(code["prelude"], ns2); exec(code["starter"], ns2)
assert all(eval(t["call"], ns2) is None for t in code["tests"])
z2 = both(4 * pi / 3, sint(lambda x, y, z: z * z, sph(), 0, pi, 0, 2 * pi), 1e-6)
lv.expect(L, "screens[10].widget.answer", round(z2 / (4 * pi), 3)); lv.expect(L, "screens[10].widget.wrong[0].value", round(z2, 3))
lv.expect(L, "quiz[2].widget.answer", 0); assert abs(flux(lambda x, y, z: (0, 0, 1), sph(), 0, pi, 0, 2 * pi)) < 1e-8
lv.expect(L, "quiz[2].widget.wrong[0].value", round(both(pi, flux(lambda x, y, z: (0, 0, 1), sph(), 0, pi / 2, 0, 2 * pi), 1e-6), 3))
lv.expect(L, "quiz[2].widget.wrong[1].value", round(4 * pi, 3))

# ---------- l11 ----------
L = "l11"
faces = [(lambda u, v: (1, u, v)), (lambda u, v: (0, v, u)), (lambda u, v: (v, 1, u)), (lambda u, v: (u, 0, v)), (lambda u, v: (u, v, 1)), (lambda u, v: (v, u, 0))]
def cube_faces(F):                                  # outward by parameter order on the unit cube
    return [flux(F, f, 0, 1, 0, 1) for f in faces]
vals = cube_faces(F); want = [1, 0, 1, 0, 1, 0]
for k, (a, b) in enumerate(zip(vals, want)):
    both(b, a); lv.expect(L, f"screens[0].widget.rows[{k}][3].answer", b)
lv.expect(L, "screens[0].widget.rows[6][3].answer", both(3, box(lambda x, y, z: div(F, x, y, z), 0, 1, 0, 1, 0, 1), 1e-6))
G = lambda x, y, z: (x * y, y * z, z * x)
for k, (a, b) in enumerate(zip(cube_faces(G), [0.5, 0, 0.5, 0, 0.5, 0])):
    both(b, a); lv.expect(L, f"screens[3].widget.rows[{k}][2].answer", b)
lv.expect(L, "screens[3].widget.rows[6][2].answer", both(1.5, sum(cube_faces(G))))
lv.expect(L, "screens[3].widget.rows[7][2].answer", both(1.5, box(lambda x, y, z: x + y + z, 0, 1, 0, 1, 0, 1), 1e-6))
C3 = lambda x, y, z: (x ** 3, y ** 3, z ** 3)
f3 = both(12 * pi / 5, ball(lambda x, y, z: div(C3, x, y, z)), 1e-6); both(f3, flux(C3, sph(), 0, pi, 0, 2 * pi), 1e-6)
lv.expect(L, "screens[4].widget.answer", "\\frac{12\\pi}{5}"); lv.expect(L, "screens[4].feedback.correct", round(f3, 3))
assert abs(ball(lambda x, y, z: x * x + y * y + z * z) - 4 * pi / 5) < 1e-6                     # no-3 slip
assert abs(tplquad(lambda r, p, t: 3 * r * r, 0, 2 * pi, lambda t: 0, lambda t: pi, lambda t, p: 0, lambda t, p: 1)[0] - 2 * pi * pi) < 1e-6
Fc = lambda x, y, z: (x, y, z * z)
cylv = both(60 * pi, tplquad(lambda z, r, t: (2 + 2 * z) * r, 0, 2 * pi, lambda t: 0, lambda t: 2, lambda t, r: 0, lambda t, r: 3)[0], 1e-6)
side = flux(Fc, lambda u, v: (2 * cos(u), 2 * sin(u), v), 0, 2 * pi, 0, 3)
top = flux(Fc, lambda u, v: (u * cos(v), u * sin(v), 3), 0, 2, 0, 2 * pi)
bot = flux(Fc, lambda u, v: (u * cos(v), u * sin(v), 0), 0, 2, 2 * pi, 0)
both(24 * pi, side, 1e-6); both(36 * pi, top, 1e-6); assert abs(bot) < 1e-9; both(cylv, side + top + bot, 1e-6)
lv.expect(L, "screens[5].widget.answer", "60\\pi"); lv.expect(L, "screens[5].feedback.correct", round(cylv, 1)); lv.expect(L, "screens[5].widget.wrong[0].tex", "15")
lv.expect(L, "screens[7].widget.answer", round(cylv, 1)); lv.expect(L, "screens[7].widget.wrong[0].value", round(side, 1)); lv.expect(L, "screens[7].widget.wrong[1].value", round(top, 1))
lv.expect(L, "screens[7].prose", 12); lv.expect(L, "screens[7].prose", 9); assert abs(area(lambda u, v: (2 * cos(u), 2 * sin(u), v), 0, 2 * pi, 0, 3) - 12 * pi) < 1e-6
vol = both(pi / 2, tplquad(lambda z, r, t: r, 0, 2 * pi, lambda t: 0, lambda t: 1, lambda t, r: 0, lambda t, r: 1 - r * r)[0], 1e-6)
lv.expect(L, "screens[6].widget.answer", round(both(3 * vol, fp, 1e-6), 3)); lv.expect(L, "screens[6].widget.wrong[0].value", round(vol, 3))
Gs = lambda x, y, z: tuple(c / (x * x + y * y + z * z) ** 1.5 for c in (x, y, z))
assert abs(div(Gs, 0.3, -0.7, 0.5)) < 1e-5
both(4 * pi, flux(Gs, sph(), 0, pi, 0, 2 * pi), 1e-6)
lv.expect(L, "quiz[0].widget.answer", round(both(4 * pi, flux(Gs, sph(2), 0, pi, 0, 2 * pi), 1e-6), 3)); lv.expect(L, "quiz[0].widget.wrong[1].value", round(16 * pi, 3))
lv.expect(L, "quiz[0].widget.wrong[0].value", round(pi, 3))
code = lv.files["l11-divergence-theorem"]["screens"][9]["widget"]
ns = {}; exec(code["solution"], ns)
for t, e in zip(code["tests"], [3, 3, 1.5, 1.5, 36, 36, 1, 0]):
    assert abs(float(t["expect"]) - e) < 1e-12 and abs(eval(t["call"], ns) - e) < 1e-6, t["call"]
ns2 = {}; exec(code["starter"], ns2); assert all(eval(t["call"], ns2) is None for t in code["tests"])
P2 = lambda x, y, z: (x * x, y * y, z * z)
fx = flux(P2, lambda u, v: (2, u, v), 0, 1, 0, 3) - flux(P2, lambda u, v: (0, u, v), 0, 1, 0, 3)
fy = flux(P2, lambda u, v: (v, 1, u), 0, 3, 0, 2); fzf = flux(P2, lambda u, v: (u, v, 3), 0, 2, 0, 1)
for v_, w_ in ((fx, 12), (fy, 6), (fzf, 18)):
    both(w_, v_, 1e-6); lv.expect(L, "screens[9].explain.text", w_)
lv.expect(L, "screens[9].prose", both(36, box(lambda x, y, z: 2 * x + 2 * y + 2 * z, 0, 2, 0, 1, 0, 3), 1e-6))
mu = lambda x, y, z: (-0.5 * x, -0.5 * y, -0.5 * z)
fm = both(-2 * pi, ball(lambda x, y, z: div(mu, x, y, z)), 1e-6); both(fm, flux(mu, sph(), 0, pi, 0, 2 * pi), 1e-6)
lv.expect(L, "screens[10].widget.answer", round(fm, 3)); lv.expect(L, "screens[10].widget.wrong[1].value", round(div(mu, 0.2, 0.1, 0.3), 6))
lv.expect(L, "quiz[2].widget.answer", both(2, sum(cube_faces(lambda x, y, z: (2 * x, 0, 0)))))

# ---------- l12 ----------
L = "l12"
R0 = lambda x, y, z: (-y, x, 0)
c0 = both(2 * pi, work(R0, circ, 0, 2 * pi))
curl0 = lambda x, y, z: curl(R0, x, y, z)
both(c0, flux(curl0, lambda u, v: (u * cos(v), u * sin(v), 0), 0, 1, 0, 2 * pi), 1e-6)
both(c0, flux(curl0, sph(), 0, pi / 2, 0, 2 * pi), 1e-6); lv.expect(L, "screens[1].widget.answer", "2\\pi")
assert abs(2 * area(sph(), 0, pi / 2, 0, 2 * pi) - 4 * pi) < 1e-6
Z = lambda x, y, z: (z, x, y)
assert all(abs(a - 1) < 1e-6 for a in curl(Z, 0.3, -0.2, 0.9)); lv.expect(L, "screens[3].widget.answer", "(1, 1, 1)")
cz = both(pi, work(Z, circ, 0, 2 * pi)); both(cz, flux(lambda x, y, z: curl(Z, x, y, z), lambda u, v: (u * cos(v), u * sin(v), 0), 0, 1, 0, 2 * pi), 1e-6)
lv.expect(L, "screens[5].widget.answer", "\\pi")
P_ = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
edges = [work(Z, (lambda A, B: (lambda t: tuple(a + t * (b - a) for a, b in zip(A, B))))(P_[k], P_[(k + 1) % 3]), 0, 1) for k in range(3)]
for k, e in enumerate(edges):
    both(0.5, e); lv.expect(L, f"screens[6].widget.rows[{k}][2].answer", 0.5)
lv.expect(L, "screens[6].widget.rows[3][2].answer", both(1.5, sum(edges)))
trS = both(1.5, flux(lambda x, y, z: curl(Z, x, y, z), lambda u, v: (u, v * (1 - u), 1 - u - v * (1 - u)), 0, 1, 0, 1), 1e-6)
lv.expect(L, "screens[7].widget.answer", trS); lv.expect(L, "screens[7].widget.wrong[0].value", round(3 / sqrt(3) / 2, 3))
assert abs(0.5 * 1 - 0.5) < 1e-12 and 0.5 * (1 * 1 - 0 * 0) > 0          # projected corner order is counterclockwise
H = lambda x, y, z: (-y, x, z * z * math.exp(x))
assert all(abs(a - b) < 1e-5 for a, b in zip(curl(H, 0.3, 0.4, 0.5), (0, -0.25 * math.exp(0.3), 2)))
both(2 * pi, flux(lambda x, y, z: curl(H, x, y, z), pb, 0, 1, 0, 2 * pi), 1e-6); both(2 * pi, work(H, circ, 0, 2 * pi))
lv.expect(L, "screens[8].widget.answer", "2\\pi")
both(-pi, work(Z, lambda t: (cos(-t), sin(-t), 0), 0, 2 * pi)); lv.expect(L, "screens[9].prose", "-\\pi")
assert abs(flux(lambda x, y, z: curl(H, x, y, z), sph(), 0, pi, 0, 2 * pi)) < 1e-6
lower = flux(lambda x, y, z: curl(H, x, y, z), sph(), pi / 2, pi, 0, 2 * pi); both(-2 * pi, lower, 1e-6)
h = lambda x, y, z: (0, x - 100, 0)
assert all(abs(a - b) < 1e-6 for a, b in zip(curl(h, 105, 102, 101), (0, 0, 1)))
legs = [((100, 100, 100), (110, 100, 100)), ((110, 100, 100), (110, 105, 102)), ((110, 105, 102), (100, 105, 102)), ((100, 105, 102), (100, 100, 100))]
pl = [work(h, (lambda A, B: (lambda t: tuple(a + t * (b - a) for a, b in zip(A, B))))(A, B), 0, 1) for A, B in legs]
for k, (v_, w_) in enumerate(zip(pl, [0, 50, 0, 0])):
    both(w_, v_, 1e-6); lv.expect(L, f"screens[11].widget.rows[{k}][2].answer", w_)
lv.expect(L, "screens[11].widget.rows[4][2].answer", both(50, sum(pl), 1e-6)); lv.expect(L, "screens[11].explain.text", 10 * 5)
lv.expect(L, "screens[11].widget.rows[2][2].wrong[0].value", -100); lv.expect(L, "screens[11].widget.rows[3][2].wrong[0].value", -50)
lv.expect(L, "quiz[3].widget.answer", round(both(4 * pi, work(Z, lambda t: (2 * cos(t), 2 * sin(t), 0), 0, 2 * pi), 1e-6), 3))
lv.expect(L, "quiz[3].widget.wrong[1].value", round(12 * pi, 3))

# ---------- review ----------
Rv = "review"
assert cross((2, 1, 0), (0, 1, 1)) == (1, -2, 2); lv.expect(Rv, "items[0].widget.answer", "(1, -2, 2)")
lv.expect(Rv, "items[1].widget.answer", both(6, area(lambda u, v: (u, v, 1 + 2 * u + 2 * v), 0, 1, 0, 2), 1e-6))
both(4 * pi, flux(lambda x, y, z: (x, y, 0), lambda u, v: (cos(u), sin(u), v), 0, 2 * pi, 0, 2), 1e-6); lv.expect(Rv, "items[2].widget.answer", "4\\pi")
B4 = lambda x, y, z: (2 * x, 3 * y, -z)
lv.expect(Rv, "items[3].widget.answer", both(24, box(lambda x, y, z: div(B4, x, y, z), 0, 1, 0, 2, 0, 3), 1e-6))
S5 = lambda x, y, z: (-3 * y, 2 * x, math.exp(z))
both(5 * pi, work(S5, circ, 0, 2 * pi)); both(5 * pi, flux(lambda x, y, z: curl(S5, x, y, z), lambda u, v: (u * cos(v), u * sin(v), 0), 0, 1, 0, 2 * pi), 1e-6)
lv.expect(Rv, "items[4].widget.answer", "5\\pi")
both(32 * pi, flux(F, sph(2), 0, pi, 0, 2 * pi), 1e-6); both(32 * pi, ball(lambda x, y, z: 3, 2), 1e-6); lv.expect(Rv, "items[6].widget.answer", "32\\pi")
both(-2 * pi, flux(lambda x, y, z: curl(R0, x, y, z), swapped, 0, 2 * pi, 0, pi / 2), 1e-6); lv.expect(Rv, "items[7].widget.answer", "-2\\pi")
cubeG = sum(flux(Gs, f, -1, 1, -1, 1) for f in [lambda u, v: (1, u, v), lambda u, v: (-1, v, u), lambda u, v: (v, 1, u), lambda u, v: (u, -1, v), lambda u, v: (u, v, 1), lambda u, v: (v, u, -1)])
both(4 * pi, cubeG, 1e-6)

# ---------- homework ----------
Hm = "homework"
A_, B_, C_ = (4, 0, 0), (0, 2, 0), (0, 0, 4)
cr = cross(tuple(b - a for a, b in zip(A_, B_)), tuple(c - a for a, c in zip(A_, C_))); assert cr == (8, 16, 8)
lv.expect(Hm, "items[1].parts[0].widget.answer", "(8, 16, 8)")
ar = both(4 * sqrt(6), norm(cr) / 2); both(ar, area(lambda u, v: (u, v * (2 - u / 2), 4 - u - 2 * v * (2 - u / 2)), 0, 4, 0, 1), 1e-6)
lv.expect(Hm, "items[1].parts[1].widget.answer", round(ar, 3)); lv.expect(Hm, "items[1].parts[1].widget.wrong[0].value", round(2 * ar, 3))
Y = lambda x, y, z: (y, z, x)
assert all(abs(a + 1) < 1e-6 for a in curl(Y, 0.2, 0.5, -0.3)); lv.expect(Hm, "items[2].parts[0].widget.answer", "(-1, -1, -1)")
both(-pi, work(Y, circ, 0, 2 * pi)); lv.expect(Hm, "items[2].parts[1].widget.answer", "-\\pi")
t4 = both(0.5, flux(F, lambda u, v: (u, v * (1 - u), 1 - u - v * (1 - u)), 0, 1, 0, 1), 1e-6); lv.expect(Hm, "items[3].widget.answer", t4)
lv.expect(Hm, "items[3].widget.wrong[0].value", round(0.5 / sqrt(3), 3)); lv.expect(Hm, "items[3].widget.wrong[1].value", round(sqrt(3) / 2, 3))
Y5 = lambda x, y, z: (y, x, z * z)
d5 = both(pi / 2, ball(lambda x, y, z: div(Y5, x, y, z), 1, pi / 2), 1e-6); both(d5, flux(Y5, sph(), 0, pi / 2, 0, 2 * pi), 1e-6)
lv.expect(Hm, "items[4].widget.answer", "\\frac{\\pi}{2}"); both(pi / 4, ball(lambda x, y, z: z, 1, pi / 2), 1e-6)
code = lv.files["homework-3"]["items"][5]["widget"]
ns = {}; exec(code["solution"], ns)
for t, e in zip(code["tests"], [4 * pi, 4 * pi, 12 * pi / 5, 12 * pi / 5, 384 * pi / 5, 384 * pi / 5, 4 * pi, 4 * pi]):
    assert abs(float(t["expect"]) - e) < 1e-9 and abs(eval(t["call"], ns) - e) < 1e-6, t["call"]
ns2 = {}; exec(code["starter"], ns2); assert all(eval(t["call"], ns2) is None for t in code["tests"])
both(384 * pi / 5, flux(C3, sph(2), 0, pi, 0, 2 * pi), 1e-6); lv.expect(Hm, "items[5].prose", round(384 * pi / 5, 2))
lv.expect(Hm, "items[6].model", round(cylv, 1)); lv.expect(Hm, "items[6].model", "60\\pi"); lv.expect(Hm, "items[6].model", "24\\pi"); lv.expect(Hm, "items[6].model", "36\\pi")
assert sum(r["points"] for r in lv.files["homework-3"]["items"][6]["rubric"]) == 10
t8 = both(-1.5, flux(lambda x, y, z: curl(Z, x, y, z), lambda u, v: (v * (1 - u), u, 1 - u - v * (1 - u)), 0, 1, 0, 1), 1e-6)
lv.expect(Hm, "items[7].widget.answer", t8); lv.expect(Hm, "items[7].widget.wrong[1].value", round(-sqrt(3) / 2, 3))

lv.check_wrongs()
lv.report()
