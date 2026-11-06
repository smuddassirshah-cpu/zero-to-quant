"""Recompute every stated number of vector-calc level 1 twice (closed form and SciPy quadrature) and check it in the JSON.
Run: python3 docs/reports/vector-calc-L1-numbers.py   (exits 0 when every check passes)
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level
from scipy.integrate import quad
import numpy as np

lv = Level("vector-calc", 1)
pi, sq2 = math.pi, math.sqrt(2)


def both(exact, numeric, tol=1e-7):
    assert abs(exact - numeric) <= tol * max(1, abs(exact)), (exact, numeric)
    return exact


def work(F, r, rp, a, b):
    return quad(lambda t: sum(f * d for f, d in zip(F(r(t)), rp(t))), a, b, limit=200)[0]


def sline(f, r, rp, a, b):
    return quad(lambda t: f(r(t)) * math.sqrt(sum(c * c for c in rp(t))), a, b, limit=200)[0]


arc = (lambda t: (2 * math.cos(t), 2 * math.sin(t)), lambda t: (-2 * math.sin(t), 2 * math.cos(t)), 0, pi / 2)
uc = (lambda t: (math.cos(t), math.sin(t)), lambda t: (-math.sin(t), math.cos(t)), 0, 2 * pi)
ucw = (lambda t: (math.cos(t), -math.sin(t)), lambda t: (-math.sin(t), -math.cos(t)), 0, 2 * pi)
hel = (lambda t: (math.cos(t), math.sin(t), t), lambda t: (-math.sin(t), math.cos(t), 1), 0, 2 * pi)
seg34 = (lambda t: (3 * t, 4 * t), lambda t: (3, 4), 0, 1)
rot = lambda p: (-p[1], p[0])
vort = lambda p: (-p[1] / (p[0] ** 2 + p[1] ** 2), p[0] / (p[0] ** 2 + p[1] ** 2))

# ---------- l1 ----------
L = "l1"
lv.expect(L, "screens[0].widget.points[0].target", 2); lv.expect(L, "screens[0].widget.points[0].target", 1)
assert (-1, 2) == rot((2, 1)) and rot((-1, 2)) == (-2, -1)
lv.expect(L, "screens[0].feedback.byKey.components", -2)
P, Qv = 2 ** 2 - 3, 2 * 3
lv.expect(L, "screens[2].widget.rows[0][2].answer", both(P, 4 - 3)); lv.expect(L, "screens[2].widget.rows[1][2].answer", both(Qv, 2 * 3))
lv.expect(L, "screens[2].widget.rows[0][2].wrong[0].value", 4 + 3); lv.expect(L, "screens[2].widget.rows[1][2].wrong[0].value", 2 + 3)
m = both(math.sqrt(P ** 2 + Qv ** 2), float(np.linalg.norm([1, 6])))
lv.expect(L, "screens[3].widget.answer", round(m, 3)); lv.expect(L, "screens[3].widget.wrong[0].value", 7); lv.expect(L, "screens[3].widget.wrong[1].value", 37)
lv.expect(L, "screens[3].explain.text", round(m, 3))
# flow line of rotation: dot with radius is zero
assert all(abs(sum(a * b for a, b in zip(rot(p), p))) < 1e-12 for p in [(1, 2), (-3, 0.5)])
lv.expect(L, "screens[5].widget.options[2].why", 2); lv.expect(L, "screens[5].widget.options[3].why", 4)
lv.expect(L, "screens[7].widget.options[1].text", 2)
# generalise: d/dt f = 1 round the circle, total 2pi
assert abs(work(rot, *uc) - 2 * pi) < 1e-9
# transfer: sigma_p^2 gradient
s1, s2, rho = 0.2, 0.1, 0.3
c = 2 * rho * s1 * s2
assert abs(c - 0.012) < 1e-12
g1, g2 = 2 * s1 ** 2 * 0.5 + c * 0.5, 2 * s2 ** 2 * 0.5 + c * 0.5
lv.expect(L, "screens[10].widget.rows[0][2].answer", both(g1, 0.046)); lv.expect(L, "screens[10].widget.rows[1][2].answer", both(g2, 0.016))
lv.expect(L, "screens[10].widget.rows[0][2].wrong[0].value", 0.04); lv.expect(L, "screens[10].widget.rows[1][2].wrong[0].value", 0.01)
lv.expect(L, "screens[10].hints[2].text", 0.046); lv.expect(L, "screens[10].hints[2].text", 0.006)
# min variance: closed form and numeric minimiser on the line
w_closed = (s2 ** 2 - rho * s1 * s2) / (s1 ** 2 + s2 ** 2 - 2 * rho * s1 * s2)
ws = np.linspace(0, 1, 2000001); var = 0.04 * ws ** 2 + 0.01 * (1 - ws) ** 2 + 0.012 * ws * (1 - ws)
w_num = ws[np.argmin(var)]
assert abs(w_closed - 2 / 19) < 1e-12 and abs(w_num - 2 / 19) < 1e-6
lv.expect(L, "screens[11].widget.answer", round(w_closed, 3)); lv.expect(L, "screens[11].widget.accept", 2 / 19)
lv.expect(L, "screens[11].widget.wrong[0].value", 0.5); lv.expect(L, "screens[11].widget.wrong[1].value", both(s2 ** 2 / (s1 ** 2 + s2 ** 2), 0.2))
lv.expect(L, "screens[11].hints[2].text", 0.076); lv.expect(L, "screens[11].hints[2].text", 0.008)
lv.expect(L, "screens[11].explain.text", 0.068); lv.expect(L, "screens[11].explain.text", 0.012)
assert abs(0.08 - 0.012 - 0.068) < 1e-12 and abs(0.02 - 0.012 + 0.0 - 0.008) < 1e-12
lv.expect(L, "screens[11].explain.canvas", round(w_closed, 4))
# quiz
lv.expect(L, "quiz[0].widget.answer", 2); lv.expect(L, "quiz[0].widget.answer", -1)
q3 = both(math.sqrt(3 ** 2 + 1 ** 2), math.hypot(2 + 1, 2 - 1))
lv.expect(L, "quiz[2].widget.answer", round(q3, 3)); lv.expect(L, "quiz[2].widget.wrong[0].value", 4); lv.expect(L, "quiz[2].widget.wrong[1].value", 10)

# ---------- l2 ----------
L = "l2"
ch = lambda n: 4 * n * math.sin(pi / (4 * n))
chn = lambda n: sum(math.dist((2 * math.cos(k * pi / (2 * n)), 2 * math.sin(k * pi / (2 * n))), (2 * math.cos((k + 1) * pi / (2 * n)), 2 * math.sin((k + 1) * pi / (2 * n)))) for k in range(n))
for n in (1, 2, 4, 8):
    both(ch(n), chn(n))
lv.expect(L, "screens[0].widget.answer", round(ch(4), 3)); lv.expect(L, "screens[0].widget.wrong[0].value", round(ch(1), 3)); lv.expect(L, "screens[0].widget.wrong[1].value", round(pi, 3))
lv.expect(L, "screens[0].feedback.correct", round(ch(8), 3))
for n in (1, 2, 4, 8):
    lv.expect(L, "screens[0].explain.text", round(ch(n), 3))
lv.expect(L, "screens[1].widget.answer", r"\pi"); both(pi, sline(lambda p: 1, *arc))
v = both(7.5, sline(lambda p: p[0], *seg34))
lv.expect(L, "screens[2].widget.answer", v); lv.expect(L, "screens[2].widget.wrong[0].value", both(1.5, quad(lambda t: 3 * t, 0, 1)[0])); lv.expect(L, "screens[2].widget.wrong[1].value", 37.5)
lv.expect(L, "screens[2].explain.text", 1.5); lv.expect(L, "screens[2].explain.text", 5)
hl = both(2 * sq2 * pi, sline(lambda p: 1, *hel)); hz = both(2 * sq2 * pi ** 2, sline(lambda p: p[2], *hel))
lv.expect(L, "screens[3].prose", round(hl, 3)); lv.expect(L, "screens[3].widget.answer", round(hz, 3))
lv.expect(L, "screens[3].widget.wrong[0].value", round(2 * pi ** 2, 3)); lv.expect(L, "screens[3].widget.wrong[1].value", round(hl, 3))
lv.expect(L, "screens[3].explain.text", round(hz, 3))
v2 = both(7.5, sline(lambda p: p[0], lambda t: (3 * t * t, 4 * t * t), lambda t: (6 * t, 8 * t), 0, 1))
v3 = both(7.5, sline(lambda p: p[0], lambda t: (3 - 3 * t, 4 - 4 * t), lambda t: (-3, -4), 0, 1))
lv.expect(L, "screens[5].prose", v2); lv.expect(L, "screens[5].widget.options[0].text", v3); lv.expect(L, "screens[5].widget.options[3].text", 15)
avg = both(0.5, sline(lambda p: p[1] ** 2, *uc) / (2 * pi))
lv.expect(L, "screens[6].widget.answer", avg); lv.expect(L, "screens[6].widget.wrong[0].value", round(pi, 4))
t8 = both(8, sline(lambda p: p[0] + p[1], *arc)); ns = both(4, quad(lambda t: 2 * math.cos(t) + 2 * math.sin(t), 0, pi / 2)[0])
lv.expect(L, "screens[7].widget.answer", t8); lv.expect(L, "screens[7].widget.wrong[0].value", ns)
lv.expect(L, "screens[7].widget.wrong[0].canvas.caption", round(pi / 2, 3)); lv.expect(L, "screens[7].widget.wrong[0].canvas.caption", round(pi, 3))
lv.expect(L, "screens[7].feedback.byKey", 1.5); lv.expect(L, "screens[7].feedback.byKey", 7.5)
both(4 * pi, quad(lambda t: 1, 0, 4 * pi)[0]); lv.expect(L, "screens[8].widget.options[0].text", 4)
codev = [7.5, 7.5, 7.5, 8, both(4, sline(lambda p: p[0] * p[1], *arc)), hl, hz, both(pi, sline(lambda p: p[1] ** 2, *uc))]
for k, val in enumerate(codev):
    lv.expect(L, f"screens[9].widget.tests[{k}].expect", val)
# transfer: seeded walk (seed 11) and the Brownian law sqrt(n) sqrt(2/pi)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(11); dw = rng.normal(0, math.sqrt(1 / 64), 64); w = np.concatenate([[0], np.cumsum(dw)])
fun = lv.files['l2-line-integrals']['screens'][10]['canvas']['params']['functions']
for n, f in zip((4, 16, 64), fun):
    pts = f['points']
    assert all(abs(p[1] - round(float(w[k]), 4)) < 1e-9 for p, k in zip(pts, range(0, 65, 64 // n)))
    tot = sum(abs(pts[j + 1][1] - pts[j][1]) for j in range(n))
    lv.expect(L, "screens[10].prose", round(tot, 3), fmt="{:.3f}")
mc = np.abs(np.random.default_rng(5).normal(0, 1, (200000,))).mean()  # E|Z| by simulation
assert abs(mc - math.sqrt(2 / pi)) < 0.005
for n in (4, 16, 64):
    lv.expect(L, "screens[10].prose", round(math.sqrt(n) * math.sqrt(2 / pi), 3))
e256 = math.sqrt(256) * math.sqrt(2 / pi)
lv.expect(L, "screens[10].widget.answer", round(e256, 3)); lv.expect(L, "screens[10].widget.wrong[0].value", round(8 * math.sqrt(2 / pi), 3)); lv.expect(L, "screens[10].widget.wrong[1].value", round(32 * math.sqrt(2 / pi), 3))
lv.expect(L, "quiz[0].widget.answer", 4); lv.expect(L, "quiz[0].widget.wrong[0].value", both(2, quad(lambda t: 4 * math.cos(t) * math.sin(t), 0, pi / 2)[0]))
qc = both(1.5, sline(lambda p: p[0], lambda t: (t, 0), lambda t: (1, 0), 0, 1) + sline(lambda p: p[0], lambda t: (1, t), lambda t: (0, 1), 0, 1))
lv.expect(L, "quiz[1].widget.answer", qc); lv.expect(L, "quiz[1].widget.wrong[0].value", 0.5)
lv.expect(L, "quiz[1].widget.wrong[1].value", round(both(sq2 / 2, sline(lambda p: p[0], lambda t: (t, t), lambda t: (1, 1), 0, 1)), 4))
lv.expect(L, "quiz[3].widget.answer", round(math.sqrt(5), 3)); lv.expect(L, "quiz[3].widget.wrong[0].value", 5); lv.expect(L, "quiz[3].widget.wrong[1].value", 3)

# ---------- l3 ----------
L = "l3"
F0 = lambda p: (0, p[0])
A = both(1, work(F0, lambda t: (t, 0), lambda t: (1, 0), 0, 1) + work(F0, lambda t: (1, t), lambda t: (0, 1), 0, 1))
B = both(0, work(F0, lambda t: (0, t), lambda t: (0, 1), 0, 1) + work(F0, lambda t: (t, 1), lambda t: (1, 0), 0, 1))
D = both(0.5, work(F0, lambda t: (t, t), lambda t: (1, 1), 0, 1))
lv.expect(L, "screens[1].widget.rows[0][1].answer", A); lv.expect(L, "screens[1].widget.rows[1][1].answer", B); lv.expect(L, "screens[1].widget.rows[2][1].answer", D)
lv.expect(L, "screens[1].widget.rows[2][1].wrong[0].value", round(both(sq2 / 2, sline(lambda p: abs(p[0]), lambda t: (t, t), lambda t: (1, 1), 0, 1)), 4))
lv.expect(L, "screens[2].canvas.state.caption", 0.25); lv.expect(L, "screens[2].canvas.state.caption", 0.5)
yx = lambda p: (p[1], p[0])
lv.expect(L, "screens[3].widget.answer", both(1, work(yx, lambda t: (t, t * t), lambda t: (1, 2 * t), 0, 1)))
lv.expect(L, "screens[3].widget.wrong[0].value", round(both(5 / 6, work(yx, lambda t: (t, t * t), lambda t: (1, 1), 0, 1)), 4))
both(1, work(yx, lambda t: (t, t), lambda t: (1, 1), 0, 1)); lv.expect(L, "screens[3].explain.text", 1)
lv.expect(L, "screens[4].widget.answer", r"2\pi"); both(2 * pi, work(rot, *uc))
both(0, work(lambda p: p, *uc))
v7 = both(7 / 3, work(lambda p: (p[1], p[0] ** 2), lambda t: (2 * t, t), lambda t: (2, 1), 0, 1))
lv.expect(L, "screens[6].widget.answer", round(v7, 3)); lv.expect(L, "screens[6].widget.wrong[0].value", round(both(11 / 6, quad(lambda t: t + 4 * t * t, 0, 1)[0]), 4))
hw_ = both(-pi, work(lambda p: (p[1], p[2], p[0]), *hel)); lv.expect(L, "screens[7].widget.answer", r"-\pi")
both(0, quad(lambda t: t * math.cos(t), 0, 2 * pi)[0], 1e-7)
both(-2 * pi, work(rot, *ucw)); lv.expect(L, "screens[8].widget.options[0].text", "-2\\pi")
fl = both(8 * pi, work(rot, lambda t: (2 * math.cos(t), 2 * math.sin(t)), lambda t: (-2 * math.sin(t), 2 * math.cos(t)), 0, 2 * pi))
lv.expect(L, "screens[9].widget.answer", r"8\pi")
codev = [2 * pi, -2 * pi, 0, 1, v7, hw_, A, B]
for k, val in enumerate(codev):
    lv.expect(L, f"screens[10].widget.tests[{k}].expect", val)
h = lambda S: (0, S[0] - 100)
p1 = both(50, work(h, lambda t: (100 + 10 * t, 100), lambda t: (10, 0), 0, 1) + work(h, lambda t: (110, 100 + 5 * t), lambda t: (0, 5), 0, 1))
p2 = both(0, work(h, lambda t: (100, 100 + 5 * t), lambda t: (0, 5), 0, 1) + work(h, lambda t: (100 + 10 * t, 105), lambda t: (10, 0), 0, 1))
lv.expect(L, "screens[11].widget.rows[0][1].answer", p1); lv.expect(L, "screens[11].widget.rows[1][1].answer", p2)
lv.expect(L, "screens[11].explain.text", 50)
lv.expect(L, "quiz[0].widget.answer", both(3, work(lambda p: (1, 0), lambda t: (3 * t, 2 * t), lambda t: (3, 2), 0, 1)))
lv.expect(L, "quiz[0].widget.wrong[0].value", round(math.sqrt(13), 4))
lv.expect(L, "quiz[1].widget.answer", -5)
both(pi, work(lambda p: (0, p[0]), *uc))

# ---------- l4 ----------
L = "l4"
G = lambda p: (2 * p[0] * p[1], p[0] ** 2)
fG = lambda x, y: x * x * y
w_line = both(4, work(G, lambda t: (2 * t, t), lambda t: (2, 1), 0, 1)); w_par = both(4, work(G, lambda t: (2 * t, t * t), lambda t: (2, 2 * t), 0, 1))
w_cor = both(4, work(G, lambda t: (2 * t, 0), lambda t: (2, 0), 0, 1) + work(G, lambda t: (2, t), lambda t: (0, 1), 0, 1))
both(fG(2, 1) - fG(0, 0), w_cor)
lv.expect(L, "screens[0].widget.rows[0][2].answer", w_line); lv.expect(L, "screens[0].widget.rows[1][2].answer", w_par)
lv.expect(L, "screens[1].widget.options[0].text", w_cor); lv.expect(L, "screens[2].prose", 4)
F2 = lambda p: (2 * p[0] * p[1] + 3, p[0] ** 2 + 4 * p[1]); f2 = lambda x, y: x * x * y + 3 * x + 2 * y * y
w13 = both(f2(1, 2) - f2(0, 0), work(F2, lambda t: (t, 2 * t * t), lambda t: (1, 4 * t), 0, 1))
lv.expect(L, "screens[5].explain.text", w13); lv.expect(L, "quiz[1].widget.answer", w13); lv.expect(L, "quiz[1].widget.wrong[0].value", 1 * 2 + 3)
F3 = lambda p: (p[1] * p[2], p[0] * p[2], p[0] * p[1])
w6 = both(1 * 2 * 3, work(F3, lambda t: (t, 2 * t, 3 * t), lambda t: (1, 2, 3), 0, 1))
lv.expect(L, "screens[7].explain.text", w6); lv.expect(L, "quiz[2].widget.answer", w6); lv.expect(L, "quiz[2].widget.wrong[0].value", 6 + 3 + 2)
# vortex: mixed partials by central differences, loop integrals
hh = 1e-5
for (x, y) in [(1, 0.3), (-0.7, 2), (0.4, -1.1)]:
    py = (vort((x, y + hh))[0] - vort((x, y - hh))[0]) / (2 * hh); qx = (vort((x + hh, y))[1] - vort((x - hh, y))[1]) / (2 * hh)
    assert abs(py - qx) < 1e-6 and abs(py - (y * y - x * x) / (x * x + y * y) ** 2) < 1e-6
both(2 * pi, work(vort, *uc))
z = work(vort, lambda t: (3 + math.cos(t), math.sin(t)), lambda t: (-math.sin(t), math.cos(t)), 0, 2 * pi)
assert abs(z) < 1e-9 and abs(math.atan2(0, 4) - math.atan2(0, 4)) == 0
lv.expect(L, "screens[9].widget.answer", 0); lv.expect(L, "screens[9].widget.wrong[0].value", round(2 * pi, 4))
fx = 1.25 * 0.92 * 0.87
lv.expect(L, "screens[10].widget.answer", round(both(fx, math.exp(math.log(1.25) + math.log(0.92) + math.log(0.87))), 4))
lv.expect(L, "screens[10].widget.wrong[0].value", both(1.25 + 0.92 + 0.87, 3.04))
lv.expect(L, "screens[10].hints[1].text", 1.15); lv.expect(L, "screens[10].feedback.correct", round(math.log(fx), 4))
V = lambda a, b: a * b / 100
hV = lambda S: (S[1] / 100, S[0] / 100)
pv = both(V(110, 105) - V(100, 100), work(hV, lambda t: (100 + 10 * t, 100 + 5 * t), lambda t: (10, 5), 0, 1))
both(pv, work(hV, lambda t: (100 + 10 * t, 100), lambda t: (10, 0), 0, 1) + work(hV, lambda t: (110, 100 + 5 * t), lambda t: (0, 5), 0, 1))
lv.expect(L, "screens[11].widget.answer", pv); lv.expect(L, "screens[11].widget.wrong[0].value", 50)
assert 110 * 105 == 11550; lv.expect(L, "screens[11].hints[0].text", "11{,}550"); lv.expect(L, "screens[11].explain.text", 115.5)
lv.expect(L, "quiz[3].explain.text", 0.05)

# ---------- review ----------
R = "review"
lv.expect(R, "items[1].widget.answer", "(-1, 3)")
r3 = both(40, sline(lambda p: p[1], lambda t: (6 * t, 8 * t), lambda t: (6, 8), 0, 1))
lv.expect(R, "items[2].widget.answer", r3); lv.expect(R, "items[2].widget.wrong[0].value", both(4, quad(lambda t: 8 * t, 0, 1)[0])); lv.expect(R, "items[2].widget.wrong[1].value", 400)
both(-18 * pi, work(rot, lambda t: (3 * math.cos(t), -3 * math.sin(t)), lambda t: (-3 * math.sin(t), -3 * math.cos(t)), 0, 2 * pi))
lv.expect(R, "items[3].widget.answer", r"-18\pi"); lv.expect(R, "items[3].explain.text", -9)
f7 = lambda x, y: x * x * y + y ** 3
r7 = both(f7(2, 1) - f7(1, 1), work(lambda p: (2 * p[0] * p[1], p[0] ** 2 + 3 * p[1] ** 2), lambda t: (1 + t, 1), lambda t: (1, 0), 0, 1))
lv.expect(R, "items[6].widget.answer", r7); lv.expect(R, "items[6].widget.wrong[0].value", f7(2, 1))
both(2 * pi, work(vort, lambda t: (0.5 + math.cos(t), math.sin(t)), lambda t: (-math.sin(t), math.cos(t)), 0, 2 * pi))
lv.expect(R, "items[7].widget.answer", r"2\pi")
both(16 * pi, sline(lambda p: p[0] ** 2 + p[1] ** 2, lambda t: (2 * math.cos(t), 2 * math.sin(t)), lambda t: (-2 * math.sin(t), 2 * math.cos(t)), 0, 2 * pi))
lv.expect(R, "items[8].widget.answer", r"16\pi")

# ---------- homework ----------
Hm = "homework"
Fh = lambda p: (p[1] ** 2, p[0])
a1 = both(13 / 15, work(Fh, lambda t: (t, t * t), lambda t: (1, 2 * t), 0, 1)); a2 = both(5 / 6, work(Fh, lambda t: (t, t), lambda t: (1, 1), 0, 1))
lv.expect(Hm, "items[0].parts[0].widget.answer", round(a1, 3)); lv.expect(Hm, "items[0].parts[0].widget.wrong[0].value", both(0.7, work(Fh, lambda t: (t, t * t), lambda t: (1, 1), 0, 1)))
lv.expect(Hm, "items[0].parts[1].widget.answer", round(a2, 3)); lv.expect(Hm, "items[0].parts[1].widget.wrong[0].value", round(a1, 3))
F3b = lambda p: (2 * p[0] + p[1] * p[2], p[0] * p[2] + 2 * p[1], p[0] * p[1]); f3b = lambda x, y, z: x * x + y * y + x * y * z
w4 = both(f3b(1, 1, 2), work(F3b, lambda t: (t, t, 2 * t), lambda t: (1, 1, 2), 0, 1))
lv.expect(Hm, "items[1].parts[1].widget.answer", w4); lv.expect(Hm, "items[1].parts[1].widget.wrong[0].value", 2)
pot = lambda P, Qf, x, y: quad(lambda s: P(s, 0), 0, x)[0] + quad(lambda s: Qf(x, s), 0, y)[0]
pv1 = both(13, pot(lambda x, y: 2 * x * y + 3, lambda x, y: x * x + 4 * y, 1, 2)); pv2 = both(4, pot(lambda x, y: 2 * x * y, lambda x, y: x * x, 2, 1))
pv3 = both(math.sin(pi / 2), pot(lambda x, y: y * math.cos(x * y), lambda x, y: x * math.cos(x * y), 1, pi / 2)); pv4 = both(f2(-1, 1), pot(lambda x, y: 2 * x * y + 3, lambda x, y: x * x + 4 * y, -1, 1))
for k, val in enumerate([pv1, pv2, pv3, pv4]):
    lv.expect(Hm, f"items[3].widget.tests[{k}].expect", val)
lv.expect(Hm, "items[3].feedback.byKey", 10)


def wpoly(F, V):
    tot = 0.0
    for A_, B_ in zip(V, V[1:]):
        d = [b - a for a, b in zip(A_, B_)]
        tot += work(F, lambda t, A_=A_, d=d: tuple(a + t * di for a, di in zip(A_, d)), lambda t, d=d: d, 0, 1)
    return tot


wv = [both(1, wpoly(F0, [(0, 0), (1, 0), (1, 1)])), both(0, wpoly(F0, [(0, 0), (0, 1), (1, 1)])), both(0.5, wpoly(F0, [(0, 0), (1, 1)])),
      both(2, wpoly(rot, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])), both(fG(2, 1), wpoly(G, [(0, 0), (1, 3), (-1, 2), (2, 1)])),
      both(6, wpoly(F3, [(0, 0, 0), (1, 0, 0), (1, 2, 0), (1, 2, 3)])), 0]
for k, val in enumerate(wv):
    lv.expect(Hm, f"items[4].widget.tests[{k}].expect", val)
hm = both(sq2 * (2 * pi + 2 * pi ** 2), sline(lambda p: 1 + p[2], *hel))
lv.expect(Hm, "items[6].widget.answer", round(hm, 3)); lv.expect(Hm, "items[6].widget.wrong[0].value", round(2 * pi + 2 * pi ** 2, 3))
lv.expect(Hm, "items[6].explain.text", round(hl, 3)); lv.expect(Hm, "items[6].explain.text", round(hz, 3))
loop = 1.27 * 150 * 0.00528
lv.expect(Hm, "items[8].parts[0].widget.answer", round(loop, 4)); lv.expect(Hm, "items[8].parts[0].widget.accept", round(loop, 5))
lv.expect(Hm, "items[8].parts[0].widget.wrong[0].value", round(1.27 + 150 + 0.00528, 3)); lv.expect(Hm, "items[8].parts[0].explain.text", 190.5)
lv.expect(Hm, "items[8].parts[1].widget.answer", round(1e6 * (loop - 1))); lv.expect(Hm, "items[8].parts[1].widget.wrong[0].value", round(1e6 * math.log(loop)))
lv.expect(Hm, "items[8].parts[1].explain.text", round(1e6 * loop))

lv.check_wrongs()
lv.report()
