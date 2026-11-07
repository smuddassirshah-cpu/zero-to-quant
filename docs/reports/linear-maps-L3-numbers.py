"""Number recompute for linear-maps level 3 (Duality and inner products): l10 to l14, review-3, homework-3.
Second reader, session V.

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations
are recomputed a second way (exact fractions and exact integrals of polynomials). The seeded check in
homework-3 items[6] needs NumPy's default_rng, so it runs only when NumPy is installed.
Checks tied to a sentence (lv.stated) fail while a false sentence is in the text and pass once a fix rewords it.
    python3 docs/reports/linear-maps-L3-numbers.py
Failing checks on the current content are findings in docs/reviews/review-linear-maps-1-3.md.
"""
import sys, os, math
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("linear-maps", 3)


def mm(A, B):
    return [[sum(F(A[i][k]) * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, v):
    return tuple(sum(F(A[i][k]) * v[k] for k in range(len(v))) for i in range(len(A)))


def inv2(A):
    a, b, c, d = (F(x) for x in (A[0][0], A[0][1], A[1][0], A[1][1]))
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def dot(u, v):
    return sum(F(a) * b for a, b in zip(u, v))


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def sc(k, v):
    return tuple(F(k) * x for x in v)


def fm(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else repr(float(x))


def tup(*xs):
    return '(' + ', '.join(fm(x) for x in xs) + ')'


def pm(M):
    return '\\begin{pmatrix}' + '\\\\'.join('&'.join(fm(x) for x in r) for r in M) + '\\end{pmatrix}'


def pint(p, a, b):                      # integral of a polynomial (coeffs low to high) from a to b
    return sum(F(c) * (F(b) ** (k + 1) - F(a) ** (k + 1)) / (k + 1) for k, c in enumerate(p))


def pmul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += F(a) * b
    return out


def pev(p, x):
    return sum(F(c) * F(x) ** k for k, c in enumerate(p))


r4 = lambda x: round(float(x), 4)

# ---------------- l10 dual space ----------------
B = [[1, 1], [1, -1]]
Bi = inv2(B)
lv.claim(Bi == [[F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2)]], "l10 s3: B^-1 rows (0.5, 0.5), (0.5, -0.5)")
lv.expect("l10", "screens[3].widget.answer", pm(Bi))
lv.claim(dot((1, 1), (1, 1)) == 2 and dot((F(1, 2), F(-1, 2)), (1, 1)) == 0, "l10 s3: B^T row 1 gives 2; swapped row 1 gives 0")
phi1 = lambda w: (w[0] + w[1]) / F(2)
lv.claim(phi1((1, 1)) == 1 and phi1((1, -1)) == 0 and phi1((0, 2)) == 1, "l10 s0-1: phi1 = (x + y)/2 is 1 on v1, 0 on v2, 1 at (0, 2)")
lv.expect("l10", "screens[1].widget.options[3].why", 1.41)
lv.claim(abs(math.sqrt(2) - 1.41) < 0.005, "l10 s1: |(1, -1)| ~ 1.41")
l1p = [0, 2, -1]                                        # 2x - x^2
lv.claim([pev(l1p, k) for k in (0, 1, 2)] == [0, 1, 0], "l10 s4: l1 = 2x - x^2 is 0, 1, 0 at 0, 1, 2")
lv.claim(pev(pmul(pmul([0, 1], [-2, 1]), [-1, 1]), 1) == 0, "l10 s4: x(x - 2)(x - 1) is 0 at 1")
for i in range(4):
    lv.expect("l10", f"screens[5].widget.rows[{i}][2].answer", i)          # (x^i)'(1) = i
Dm = [[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
lv.claim(mm([[1, 1, 1]], Dm) == [[0, 1, 2, 3]], "l10 s5: (1, 1, 1) [D] = (0, 1, 2, 3)")
lv.claim(mv(inv2([[1, 1], [0, 1]]), (1, 0)) == (1, 0) and inv2([[1, 1], [0, 1]])[0] == [1, -1], "l10 s6: basis (1,0), (1,1) gives phi1 = x - y")
lv.expect("l10", "screens[10].widget.examples[0].expect", "[[1.0, -1.0], [0.0, 1.0]]")
B3 = [[2, 0, 1], [1, 1, 0], [0, 1, 1]]
B3i = [[F(1, 3), F(1, 3), F(-1, 3)], [F(-1, 3), F(2, 3), F(1, 3)], [F(1, 3), F(-2, 3), F(2, 3)]]
lv.claim(mm(B3i, B3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "l10 code test 3: the inverse of [[2,0,1],[1,1,0],[0,1,1]]")
phi = (3, -1)
P = [[1, 1], [1, -1]]
expo = tuple(dot(phi, col) for col in zip(*P))
lv.expect("l10", "screens[11].widget.answer", tup(*expo))
lv.expect("l10", "screens[11].widget.wrong[0].tex", tup(*mv(inv2(P), phi)))
lv.expect("l10", "screens[11].widget.wrong[1].tex", tup(*phi))
move = (3, 1)
cn = mv(inv2(P), move)
lv.claim(cn == (2, 1) and dot(expo, cn) == dot(phi, move) == 8, "l10 s11: move (3,1) has coordinates (2,1) and 2*2 + 4*1 = 8 = phi(3,1)")
l0p = [1, F(-3, 2), F(1, 2)]
lv.claim([pev(l0p, k) for k in (0, 1, 2)] == [1, 0, 0], "l10 quiz[1]: l0 = 1 - 1.5x + 0.5x^2 is 1, 0, 0 at 0, 1, 2")
lv.expect("l10", "quiz[1].widget.answer", "1-1.5x+0.5x^2")
lv.claim(pev(pmul([-1, 1], [-2, 1]), 0) == 2, "l10 quiz[1]: (x - 1)(x - 2) is 2 at 0")

# ---------------- l11 inner products ----------------
v = (0, 1)
lv.expect("l11", "screens[0].widget.rows[0][1].answer", v[0] * v[0] + v[1] * v[1])
lv.expect("l11", "screens[0].widget.rows[1][1].answer", v[0] * v[0] - v[1] * v[1])
lv.expect("l11", "screens[0].widget.rows[2][1].answer", v[0] * v[0])
lv.claim(1 * 1 - 1 * 1 == 0, "l11 s2: x1y1 - x2y2 gives 0 at (1, 1), so definiteness fails too")
A = [[2, 1], [1, 2]]
ev = sorted([(4 - math.sqrt(16 - 4 * 3)) / 2, (4 + math.sqrt(16 - 4 * 3)) / 2])
lv.claim(ev == [1.0, 3.0], "l11 s3: A = [[2,1],[1,2]] has eigenvalues 1 and 3")
lv.expect("l11", "screens[3].widget.answer", A[0][1])
lv.expect("l11", "screens[3].widget.wrong[1].value", A[0][0])
lv.expect("l11", "screens[3].widget.wrong[2].value", 3)
lv.claim(dot((1, 0), mv(A, (1, 0))) == 2, "l11 s3: ||e1||_A^2 = 2")
lv.claim(1j * 1j == -1 and 1j * (1j).conjugate() == 1, "l11 s5: i * i = -1, i * conj(i) = 1")
lv.expect("l11", "screens[9].widget.answer", max(1, 1) ** 2 + max(1, 1) ** 2)
lv.expect("l11", "screens[9].widget.wrong[0].value", 2 * (1 + 1))
lv.expect("l11", "screens[9].widget.wrong[1].value", 1)
sd = math.sqrt(3 ** 2 + 4 ** 2)
lv.expect("l11", "screens[10].widget.answer", sd * 1000)
lv.expect("l11", "screens[10].widget.wrong[0].value", 7000)
lv.expect("l11", "screens[10].widget.wrong[1].value", 1000)
lv.expect("l11", "quiz[3].widget.answer", float(pint([0, 1], 0, 1)))
lv.expect("l11", "quiz[3].widget.wrong[1].value", r4(pint([0, 0, 1], 0, 1)))
# Statement: "We met five: dot, weighted, x^TAy, int_0^1 fg and ..." - the integral product first appears on this screen
first_int = next(i for i in range(12) if 'int_0' in lv.text("l11", f"screens[{i}]"))
lv.stated("l11", "screens[7].prose", "We met five", first_int < 7)

# ---------------- l12 Cauchy-Schwarz ----------------
u, w3 = (1, 2, 2), (3, 0, 4)
ip, nu, nv = dot(u, w3), math.isqrt(int(dot(u, u))), math.isqrt(int(dot(w3, w3)))
lv.claim(nu * nu == dot(u, u) and nv * nv == dot(w3, w3), "l12 s0: the norms are whole numbers")
for i, val in enumerate((ip, nu, nv, nu * nv)):
    lv.expect("l12", f"screens[0].widget.rows[{i}][1].answer", val)
lv.expect("l12", "screens[0].explain.text", round(ip / (nu * nv), 3))
uu = (2, 1)
lv.claim(dot(uu, (-1, 2)) == 0 and dot(uu, (1, 2)) == 4 and dot(uu, (4, 2)) == 10 and dot((4, 2), (4, 2)) * dot(uu, uu) == 100, "l12 s1: (-1,2) gives 0, (1,2) gives 4, (4,2) gives 10 = 10")
c = F(ip, dot(w3, w3))
lv.expect("l12", "screens[2].widget.answer", float(c))
lv.expect("l12", "screens[2].widget.wrong[0].value", float(F(ip, nv)))
lv.expect("l12", "screens[2].widget.wrong[1].value", r4(F(ip, dot(u, u))))
lv.expect("l12", "screens[2].widget.wrong[2].value", r4(F(ip, nu * nv)))
cv = sc(c, w3); wv = add(u, sc(-1, cv))
lv.expect("l12", "screens[2].explain.text", tup(*cv))
lv.expect("l12", "screens[2].explain.text", tup(*wv))
lv.claim(dot(wv, w3) == 0 and dot(wv, wv) == F('4.16') and c * c * 25 + dot(wv, wv) == 9, "l12 s2: w orthogonal to v, ||w||^2 = 4.16, 4.84 + 4.16 = 9")
lv.expect("l12", "screens[3].prose", float(c * c * 25))
lv.claim(dot(u, wv) == F('4.16'), "l12 s3: <u, w> = 4.16")
disc = (2 * ip) ** 2 - 4 * 25 * 9
lv.expect("l12", "screens[4].hints[2].text", disc)
lv.claim(pev([9, -2 * ip, 25], c) == F('4.16'), "l12 s4: q(0.44) = 4.16, the minimum of q")
s = add(u, w3)
lv.expect("l12", "screens[6].prose", f"\\sqrt{{{dot(s, s)}}}")
lv.expect("l12", "screens[6].prose", round(math.sqrt(dot(s, s)), 3))
lv.claim(dot(s, s) == 56 and 2 * ip == 22 and (nu + nv) ** 2 == 64, "l12 s6: 56 <= 64, cross term 22, bound 30")
cov = F(1, 2) * 3 * 4
var = 9 + 2 * cov + 16
lv.expect("l12", "screens[10].widget.answer", round(math.sqrt(var) * 1000, 2))
lv.expect("l12", "screens[10].hints[2].text", var)
lv.expect("l12", "screens[10].widget.wrong[1].value", 5000)
lv.expect("l12", "quiz[1].widget.answer", r4(pint([1], 0, 1) * pint([0, 0, 1], 0, 1)))
lv.expect("l12", "quiz[1].prose", float(pint([0, 1], 0, 1) ** 2))
lv.expect("l12", "quiz[2].widget.answer", round(1 - 1.2, 10))
lv.expect("l12", "quiz[2].widget.wrong[0].value", 1 + 1.2)
lv.claim(abs((1 - 2 * 1.2 + 1) - (-0.4)) < 1e-12, "l12 quiz[2]: (1, -1) gets variance -0.4")
lv.expect("l12", "quiz[3].widget.answer", dot(u, sc(2, u)))
lv.expect("l12", "quiz[3].widget.wrong[0].value", 6)
lv.expect("l12", "quiz[3].widget.wrong[1].value", dot(u, u))

# ---------------- l13 Gram-Schmidt ----------------
m, f = (1, -1, 2, -2), (2, 0, 1, -3)
beta = F(dot(f, m), dot(m, m))
lv.expect("l13", "screens[0].widget.answer", beta)
lv.expect("l13", "screens[0].widget.wrong[0].value", float(F(dot(f, m), 4)))
lv.expect("l13", "screens[0].widget.wrong[1].value", r4(F(dot(f, m), dot(f, f))))
lv.claim(sum(m) == 0 and sum(f) == 0 and dot(f, f) == 14, "l13 s0: m and f are demeaned; <f, f> = 14")
res = add(f, sc(-beta, m))
lv.expect("l13", "screens[2].widget.answer", tup(*res))
lv.expect("l13", "screens[2].widget.wrong[0].tex", tup(*add(f, m)))
lv.expect("l13", "screens[2].widget.wrong[1].tex", tup(*sc(-1, res)))
lv.claim(dot(res, m) == 0, "l13 s2: the residual is orthogonal to m")
v1, v2, v3 = (1, 1, 0), (1, 0, 1), (0, 1, 1)
p21 = sc(F(dot(v2, v1), dot(v1, v1)), v1)
f2 = add(v2, sc(-1, p21))
lv.expect("l13", "screens[3].widget.answer", tup(*f2))
lv.expect("l13", "screens[3].widget.wrong[1].tex", tup(*add(v2, sc(-1, v1))))
lv.expect("l13", "screens[4].widget.answer", float(dot(f2, f2)))
lv.expect("l13", "screens[4].widget.wrong[0].value", r4(math.sqrt(dot(f2, f2))))
lv.expect("l13", "screens[4].widget.wrong[1].value", float(sum(abs(x) for x in f2)))
f3 = add(v3, sc(-F(dot(v3, v1), dot(v1, v1)), v1), sc(-F(dot(v3, f2), dot(f2, f2)), f2))
lv.claim(f3 == (F(-2, 3), F(2, 3), F(2, 3)), "l13 s5: f3 = (-2/3, 2/3, 2/3)")
lv.expect("l13", "screens[5].widget.answer", "(-2/3, 2/3, 2/3)")
lv.expect("l13", "screens[5].widget.wrong[0].tex", tup(*add(v3, sc(-F(dot(v3, v1), dot(v1, v1)), v1))))
g = add(v3, sc(-F(dot(v3, v1), dot(v1, v1)), v1), sc(-F(dot(v3, v2), dot(v2, v2)), v2))
lv.expect("l13", "screens[5].widget.wrong[1].tex", tup(*g))
lv.expect("l13", "screens[7].prose", tup(*g))
lv.expect("l13", "screens[7].widget.answer", float(dot(g, v1)))
lv.expect("l13", "screens[5].explain.text", r4(math.sqrt(dot(f3, f3))))
lv.expect("l13", "quiz[0].widget.answer", r4(math.sqrt(dot(f3, f3))))
lv.expect("l13", "quiz[0].widget.wrong[0].value", r4(dot(f3, f3)))
lv.claim(dot(f3, v1) == 0 and dot(f3, f2) == 0, "l13 s5: f3 is orthogonal to v1 and f2")
# Legendre on [-1, 1]
ip1 = lambda p, q: pint(pmul(p, q), -1, 1)
lv.claim(ip1([1], [1]) == 2 and ip1([0, 1], [1]) == 0 and ip1([0, 1], [0, 1]) == F(2, 3) and ip1([0, 0, 1], [1]) == F(2, 3) and ip1([0, 0, 1], [0, 1]) == 0,
         "l13 s6: the five inner products on [-1, 1]")
f3p = [F(-1, 3), 0, 1]
lv.claim(ip1(f3p, f3p) == F(8, 45) and ip1(f3p, [1]) == 0 and ip1(f3p, [0, 1]) == 0, "l13 s6: ||x^2 - 1/3||^2 = 8/45, orthogonal to 1 and x")
lv.expect("l13", "screens[6].explain.text", r4(math.sqrt(F(45, 8))))
alt = add(m, sc(-F(dot(m, f), dot(f, f)), f))
lv.expect("l13", "screens[11].widget.options[3].why", "(-\\tfrac37, -1, \\tfrac97, \\tfrac17)")
lv.claim(alt == (F(-3, 7), F(-1), F(9, 7), F(1, 7)) and F(dot(m, f), dot(f, f)) == F(5, 7), "l13 s11: m - (5/7) f = (-3/7, -1, 9/7, 1/7)")
lv.claim(dot((2, 2, 0), (1, 1, 0)) ** 2 == 8 * 2, "l13 quiz[3]: <(2,2,0), e1> = 2 sqrt 2")
lv.expect("l13", "screens[10].widget.examples[0].expect", round(1 / math.sqrt(10), 6))

# ---------------- l14 orthogonal complements ----------------
vv, d = (1, 3), (2, 1)
t = F(dot(vv, d), dot(d, d))
lv.claim(t == 1 and add(vv, sc(-t, d)) == (-1, 2), "l14 s0: nearest point (2, 1), residual (-1, 2)")
lv.expect("l14", "screens[0].feedback.correct", round(math.sqrt(5), 3))
lv.expect("l14", "screens[1].widget.options[1].text", dot(vv, d))
lv.expect("l14", "screens[3].widget.answer", 3 - 1)
v4 = (3, 0, 0)
pu = sc(F(dot(v4, (1, 1, 1)), 3), (1, 1, 1))
lv.expect("l14", "screens[4].widget.answer", tup(*pu))
lv.expect("l14", "screens[4].widget.wrong[0].tex", tup(*sc(dot(v4, (1, 1, 1)), (1, 1, 1))))
lv.expect("l14", "screens[4].widget.wrong[1].tex", "1.732")
lv.claim(abs(3 / math.sqrt(3) - 1.732) < 0.0005, "l14 s4: 3/sqrt 3 ~ 1.732")
resid = add(v4, sc(-1, pu))
lv.expect("l14", "screens[5].widget.answer", tup(*resid))
lv.expect("l14", "screens[5].widget.wrong[0].tex", tup(*sc(-1, resid)))
lv.expect("l14", "screens[5].explain.text", round(math.sqrt(dot(resid, resid)), 3))
lv.claim(sum(resid) == 0, "l14 s5: the residual lies in x + y + z = 0")
cbest = F(ip1([0, 0, 1], [1]), ip1([1], [1]))
lv.expect("l14", "screens[6].widget.answer", r4(cbest))
lv.expect("l14", "screens[6].widget.wrong[2].value", r4(ip1([0, 0, 1], [1])))
qc = lambda cc: ip1([-cc, 0, 1], [-cc, 0, 1])
lv.claim(qc(cbest) == F(8, 45) and all(qc(cbest + F(k, 100)) > qc(cbest) for k in (-5, -1, 1, 5)), "l14 s6: ||x^2 - c||^2 is smallest at c = 1/3, value 8/45")
lv.claim(qc(F(1, 3)) == F(2, 5) - F(4, 3) * F(1, 3) + 2 * F(1, 9), "l14 s6: ||x^2 - c||^2 = 2/5 - 4c/3 + 2c^2")
lv.expect("l14", "screens[6].feedback.correct", r4(math.sqrt(F(8, 45))))
v7 = (1, 1, 1)
single = add(sc(F(dot(v7, (1, 0, 0)), 1), (1, 0, 0)), sc(F(dot(v7, (1, 1, 0)), 2), (1, 1, 0)))
lv.expect("l14", "screens[7].prose", tup(*single))
lv.claim(dot(add(v7, sc(-1, single)), add(v7, sc(-1, single))) == 2, "l14 s7: (2,1,0) is sqrt 2 from v")
lv.expect("l14", "quiz[3].widget.answer", round(math.sqrt(2), 3))
lv.expect("l14", "quiz[3].widget.wrong[1].value", 2)
hed = (1, 1, -1, -1)
lv.expect("l14", "screens[11].widget.answer", F(dot(hed, hed), 4))
lv.expect("l14", "screens[11].widget.wrong[0].value", float(F(dot(f, f), 4)))
lv.expect("l14", "screens[11].widget.wrong[1].value", dot(hed, hed))
lv.claim(dot(hed, m) == 0, "l14 s11: the hedged P&L is orthogonal to the market")
lv.expect("l14", "screens[10].widget.examples[0].expect", "[2.0, 1.0]")

# ---------------- review-3 ----------------
Br = [[2, 1], [1, 1]]
lv.claim(inv2(Br) == [[1, -1], [-1, 2]], "review items[0]: B^-1 = [[1,-1],[-1,2]]")
p2 = lambda w: -w[0] + 2 * w[1]
lv.claim(p2((2, 1)) == 0 and p2((1, 1)) == 1, "review items[0]: phi2 is 0 on v1 and 1 on v2")
ur, vr = (1, 2, 3), (2, 0, 1)
lv.claim(dot(ur, vr) == 5, "review items[2]: <u, v> = 5")
prod = math.sqrt(dot(ur, ur) * dot(vr, vr))
lv.expect("review", "items[2].widget.answer", round(prod, 3))
lv.expect("review", "items[2].widget.wrong[1].value", dot(ur, ur) * dot(vr, vr))
lv.expect("review", "items[2].explain.text", round(5 / prod, 3))
# Misleading: wrong "sum" = 6 names no slip; adding the norms gives 5.978, outside its band
lv.stated("review", "items[2].feedback.byKey.sum", "type terms wrongly", abs(math.sqrt(14) + math.sqrt(5) - 6) <= 0.01)
lv.expect("review", "items[3].widget.answer", 2 * 3)
lv.expect("review", "items[3].widget.wrong[0].value", 2 + 3)
lv.expect("review", "items[3].widget.wrong[1].value", 4 + 9)
fr2 = add((2, 1, 0), sc(-F(dot((2, 1, 0), (1, 0, 1)), 2), (1, 0, 1)))
lv.expect("review", "items[4].widget.answer", tup(*fr2))
lv.expect("review", "items[4].widget.wrong[0].tex", tup(*add((2, 1, 0), sc(-2, (1, 0, 1)))))
pr = sc(F(dot((1, 2, 3), (1, 1, 1)), 3), (1, 1, 1))
lv.claim(pr == (2, 2, 2), "review items[5]: P_U v = (2, 2, 2)")
lv.expect("review", "items[5].widget.answer", round(math.sqrt(dot(add((1, 2, 3), sc(-1, pr)), add((1, 2, 3), sc(-1, pr)))), 3))
lv.expect("review", "items[5].widget.wrong[1].value", round(math.sqrt(12), 3))
lv.expect("review", "items[5].widget.wrong[2].value", round(math.sqrt(14), 3))
lv.expect("review", "items[7].widget.answer", dot((1, 1), mv(A, (1, 1))))
lv.expect("review", "items[7].widget.wrong[2].value", A[0][0] + A[1][1])
pp = [1, 3, 5]
dp = [3, 10]
lv.expect("review", "items[8].widget.answer", pev(dp, 0))
lv.expect("review", "items[8].widget.wrong[0].value", pev(pp, 0))
lv.expect("review", "items[8].widget.wrong[1].value", pev(dp, 1))
lv.expect("review", "items[8].widget.wrong[2].value", pev(pp, 1))

# ---------------- homework-3 ----------------
l2p = [0, F(-1, 2), F(1, 2)]
lv.claim([pev(l2p, k) for k in (0, 1, 2)] == [0, 0, 1], "homework items[1]: l2 = x(x - 1)/2 is 0, 0, 1 at 0, 1, 2")
lv.claim([a + b + cc for a, b, cc in zip(l0p, l1p + [0], l2p)] == [1, 0, 0], "homework items[1]: l0 + l1 + l2 = 1")
Tm = [[1, 2], [0, 3]]
lv.claim(mm([[2, -1]], Tm) == [[2, 1]], "homework items[2]: psi o T = 2x + y")
lv.claim(mv(Tm, (2, -1)) == (0, -3), "homework items[2]: [T] on the column (2, -1) gives (0, -3), the -3y wrong")
ip01 = lambda p, q: pint(pmul(p, q), 0, 1)
f2h = [F(-1, 2), 1]
lv.expect("homework", "items[3].widget.answer", r4(ip01(f2h, f2h)))
lv.expect("homework", "items[3].widget.wrong[0].value", r4(ip01([0, 1], [0, 1])))
lv.expect("homework", "items[3].widget.wrong[2].value", r4(math.sqrt(ip01(f2h, f2h))))
lv.claim(ip01(f2h, f2h) == F(1, 12), "homework items[3]: ||x - 1/2||^2 = 1/12")
# projection of x^2 onto P1 on [0, 1] by normal equations
G = [[ip01([1], [1]), ip01([1], [0, 1])], [ip01([0, 1], [1]), ip01([0, 1], [0, 1])]]
rhs = (ip01([0, 0, 1], [1]), ip01([0, 0, 1], [0, 1]))
ab = mv(inv2(G), rhs)
lv.claim(ab == (F(-1, 6), 1), "homework items[4]: P x^2 = x - 1/6")
lv.claim(ip01([0, 0, 1], [F(-1, 2), 1]) * 2 == F(1, 6), "homework items[4]: <x^2, e2> = 2 sqrt3 (1/4 - 1/6)")
sing = (ip01([0, 0, 1], [1]) / ip01([1], [1]), ip01([0, 0, 1], [0, 1]) / ip01([0, 1], [0, 1]))
lv.claim(sing == (F(1, 3), F(3, 4)), "homework items[4]: single projections give 3/4 x + 1/3")
lv.expect("homework", "items[5].widget.examples[0].expect", round(1 / math.sqrt(2.5), 6))
n = 20
lv.expect("homework", "items[6].model", round(1.03 * (n - 1) / n, 4))
lv.expect("homework", "items[6].model", round(0.98 * n / (n - 1), 4))
lv.expect("homework", "items[6].model", round(n / (n - 1), 4))
try:
    import numpy as np
    rng = np.random.default_rng(7); a = rng.standard_normal(20); b = a + 0.2 * rng.standard_normal(20)
    x, y = a - a.mean(), b - b.mean()
    rho = float((x @ y) / math.sqrt((x @ x) * (y @ y)))
    lv.expect("homework", "items[6].model", round(rho, 4))
    lv.expect("homework", "items[6].model", round(rho * n / (n - 1), 4))
except ImportError:
    print('NumPy absent: the seeded check in homework items[6] is not recomputed')
lv.expect("homework", "items[8].widget.answer", round(0.98 * n / (n - 1), 4))
lv.expect("homework", "items[8].widget.wrong[1].value", round(0.98 * (n - 1) / n, 4))
lv.expect("homework", "items[8].widget.wrong[2].value", round(0.98 * (n / (n - 1)) ** 2, 4))
lv.expect("homework", "items[8].explain.text", (n - 1) / n)

lv.check_wrongs()
lv.report()
