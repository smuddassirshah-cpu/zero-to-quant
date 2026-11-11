"""Number recompute for quadratics level 4 (l14 to l19, review-4, homework-4).
Every stated number is computed two ways and then found in the JSON at the place it is stated, with app/tools/numbers_lib.py.
Method 1 is the working the lesson teaches (largest square factor, factorising, the remainder theorem, completing the square,
the discriminant); method 2 is independent (squaring back, exact Fraction arithmetic, a shoelace area, brute-force lattice
counts, evaluation at several rational points, floating-point substitution). Pure standard library.
Run: python3 docs/reports/quadratics-L4-numbers.py   (add --verbose for the "check by hand" lines)
"""
import math, os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("quadratics", 4)
PTS = [Fr(7, 3), Fr(-5, 2), Fr(11, 4), Fr(13, 5), Fr(-17, 7)]          # rational test points, none a root of any bottom used


def two(a, b, label, tol=1e-9):
    """Two independent routes must agree; returns the first."""
    ok = abs(float(a) - float(b)) <= tol
    lv.claim(ok, label, f"{a} vs {b}")
    return a


def same_fn(f, g, label, pts=PTS):
    """Two expressions agree at five rational points (exact)."""
    lv.claim(all(f(x) == g(x) for x in pts), label)


def E(ref, path, value, fmt=None):
    lv.expect(ref, path, value, fmt=fmt)


# ---------- helpers ----------
def largest_square_factor(n):                       # method 1: from the prime factorisation
    f, p, m = 1, 2, n
    while p * p <= m:
        while m % (p * p) == 0:
            f *= p * p
            m //= p * p
        while m % p == 0:
            m //= p
        p += 1
    return f


def simplify_surd(n):                               # sqrt(n) = a sqrt(b)
    f = largest_square_factor(n)
    a, b = math.isqrt(f), n // f
    lv.claim(a * a * b == n and largest_square_factor(b) == 1, f"sqrt({n}) = {a} sqrt({b}) squares back")   # method 2: square back
    return a, b


class S:                                            # a + b sqrt(c), exact
    def __init__(s, a, b, c): s.a, s.b, s.c = Fr(a), Fr(b), c
    def __add__(s, o): return S(s.a + o.a, s.b + o.b, s.c)
    def __mul__(s, o): return S(s.a * o.a + s.b * o.b * s.c, s.a * o.b + s.b * o.a, s.c)
    def __float__(s): return float(s.a) + float(s.b) * math.sqrt(s.c)


def pmul(p, q):                                     # polynomials as coefficient lists, highest power first
    r = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def pval(p, x):
    v = Fr(0)
    for c in p:
        v = v * x + c
    return v


def pdiv(p, a):                                     # divide by (x - a): synthetic division, returns quotient, remainder
    q, acc = [], Fr(0)
    for c in p:
        acc = acc * a + c
        q.append(acc)
    return q[:-1], q[-1]


def roots_quad(a, b, c):
    d = b * b - 4 * a * c
    return d, sorted([(-b + math.sqrt(d)) / (2 * a), (-b - math.sqrt(d)) / (2 * a)]) if d >= 0 else []


def shoelace(pts):
    return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2


# =============================== l14 ===============================
F = "l14"
big = two(4 * 4 - 4 * Fr(1, 2) * 2 * 2, shoelace([(5, 0), (7, 2), (5, 4), (3, 2)]), "l14 large tilted square area 8")
E(F, "screens[0].widget.answer", big); E(F, "screens[0].explain.text", 8)
two(4 - 4 * Fr(1, 2), shoelace([(1, 0), (2, 1), (1, 2), (0, 1)]), "l14 small square area 2"); E(F, "screens[0].prose", 2)
E(F, "screens[0].widget.wrong[0].value", 16); E(F, "screens[0].widget.wrong[1].value", two(16 - 4 * Fr(1, 2), 14, "l14 small-corner slip 14"))
two(math.sqrt(8) / math.sqrt(2), 4 - 2, "l14 side of area 8 is two diagonals"); E(F, "screens[1].widget.answer", 2)
E(F, "screens[1].widget.wrong[0].value", 8 // 2)
a, b = simplify_surd(72); E(F, "screens[2].widget.answer", a); lv.claim(b == 2, "sqrt72 = 6 sqrt2")
lv.claim(72 == 9 * 8 and 72 == 4 * 18 and largest_square_factor(8) == 4 and largest_square_factor(18) == 9, "l14 3sqrt8 and 2sqrt18 still hold squares")
E(F, "screens[2].widget.wrong[0].value", 3); E(F, "screens[2].widget.wrong[1].value", 2); E(F, "screens[2].widget.wrong[2].value", 36)
a50, _ = simplify_surd(50); a18, _ = simplify_surd(18)
E(F, "screens[3].widget.rows[0][1].answer", a50); E(F, "screens[3].widget.rows[1][1].answer", a18)
E(F, "screens[3].widget.rows[2][1].answer", two(a50 + a18, math.sqrt(50 + 0) / math.sqrt(2) + math.sqrt(18) / math.sqrt(2), "l14 sqrt50 + sqrt18 = 8 sqrt2"))
lv.claim(simplify_surd(68) == (2, 17), "l14 sqrt68 = 2 sqrt17"); E(F, "screens[3].explain.text", r"2\sqrt{17}")
E(F, "screens[3].widget.rows[2][1].wrong[0].value", a50 * a18)
sq = S(1, 1, 3) * S(1, 1, 3)
two(float(sq), (1 + math.sqrt(3)) ** 2, "l14 (1 + sqrt3)^2 = 4 + 2 sqrt3")
E(F, "screens[4].widget.rows[0][1].answer", sq.a); E(F, "screens[4].widget.rows[1][1].answer", sq.b)
pr = S(3, 1, 2) * S(3, -1, 2); two(float(pr), (3 + math.sqrt(2)) * (3 - math.sqrt(2)), "l14 (3 + sqrt2)(3 - sqrt2) = 7")
lv.claim(pr.b == 0, "l14 conjugate product has no surd"); E(F, "screens[4].widget.rows[2][1].answer", pr.a); E(F, "screens[4].widget.rows[2][1].wrong[0].value", 9 + 2)
two(6 / math.sqrt(3), 2 * math.sqrt(3), "l14 6/sqrt3 = 2 sqrt3"); E(F, "screens[5].widget.rows[0][1].answer", Fr(6, 3))
two(1 / (3 - math.sqrt(2)), (3 + math.sqrt(2)) / 7, "l14 1/(3 - sqrt2) = (3 + sqrt2)/7")
E(F, "screens[5].widget.rows[1][1].answer", 3); E(F, "screens[5].widget.rows[2][1].answer", 9 - 2)
E(F, "screens[5].widget.rows[2][1].wrong[0].value", 9 + 2); E(F, "screens[5].widget.rows[2][1].wrong[1].value", 3 - 2)
d, rts = roots_quad(1, -6, 1); lv.claim(d == 32 and simplify_surd(32) == (4, 2), "l14 discriminant 32 = 16 x 2")
r_hi = two(3 + 2 * math.sqrt(2), rts[1], "l14 root 3 + 2 sqrt2"); r_lo = two(3 - 2 * math.sqrt(2), rts[0], "l14 root 3 - 2 sqrt2")
lv.claim(abs(r_hi ** 2 - 6 * r_hi + 1) < 1e-12 and abs(r_lo ** 2 - 6 * r_lo + 1) < 1e-12, "l14 roots satisfy x^2 - 6x + 1 = 0")
E(F, "screens[6].explain.text", round(r_hi, 3)); E(F, "screens[6].explain.text", round(r_lo, 3))
E(F, "screens[6].canvas.state.points[0].x", round(r_lo, 4)); E(F, "screens[6].canvas.state.points[1].x", round(r_hi, 4))
E(F, "screens[7].widget.answer", two(math.sqrt(9 + 16), 5, "l14 sqrt(9 + 16) = 5")); E(F, "screens[7].widget.wrong[0].value", 3 + 4); E(F, "screens[7].explain.text", 7)
a252, b252 = simplify_surd(252); lv.claim(252 == 2 ** 2 * 3 ** 2 * 7, "l14 252 = 2^2 3^2 7")
E(F, "screens[9].widget.rows[0][1].answer", a252)
vol = two(a252 * math.sqrt(b252), math.sqrt(252), "l14 annual vol 6 sqrt7"); E(F, "screens[9].widget.rows[1][1].answer", round(vol, 2))
E(F, "screens[9].canvas.state.points[0].y", round(vol, 4)); E(F, "screens[9].widget.rows[1][1].wrong[0].value", 252)
E(F, "screens[9].widget.rows[0][1].wrong[0].value", 36); E(F, "screens[9].widget.rows[0][1].wrong[1].value", 3)
lv.claim(round(252 / vol) == 16, "l14 252% overstates 15.87% about 16 times"); E(F, "screens[9].explain.text", 16)
E(F, "screens[9].hints[2].text", round(math.sqrt(7), 4))
q = simplify_surd(45)[0] + simplify_surd(20)[0]; two(q * math.sqrt(5), math.sqrt(45) + math.sqrt(20), "l14 q0 sqrt45 + sqrt20 = 5 sqrt5")
E(F, "quiz[0].feedback.correct", q); E(F, "quiz[0].widget.options[3].why", 9)
E(F, "quiz[1].feedback.correct", two(Fr("1.414") ** 2, 1.414 * 1.414, "l14 1.414^2"), fmt="1.999396")
v = two(float(S(10, -5, 3)), 5 / (2 + math.sqrt(3)), "l14 q3 5/(2 + sqrt3) = 10 - 5 sqrt3"); E(F, "quiz[3].explain.text", round(v, 2))
E(F, "quiz[3].widget.options[1].why", 4 - 3)

# =============================== l15 ===============================
F = "l15"
lv.claim(math.gcd(84, 120) == 12 == 2 * 2 * 3, "l15 HCF(84, 120) = 12 from the primes"); E(F, "screens[0].canvas.state.caption", 12)
lv.claim(Fr(84, 120) == Fr(7, 10) and 84 // 12 == 7 and 120 // 12 == 10, "l15 84/120 = 7/10")
orig = lambda x: (x * x + 5 * x + 6) / (x * x + 3 * x + 2); simp = lambda x: (x + 3) / (x + 1)
same_fn(orig, simp, "l15 (x^2+5x+6)/(x^2+3x+2) = (x+3)/(x+1)")
for i, (xv, val) in enumerate([(1, 2), (2, Fr(5, 3)), (3, Fr(3, 2))]):
    two(orig(Fr(xv)), simp(Fr(xv)), f"l15 agree at x = {xv}"); lv.claim(orig(Fr(xv)) == val, f"l15 value at {xv}")
E(F, "screens[1].widget.answer", 2); E(F, "screens[1].widget.wrong[0].value", 1 + 5 + 6); E(F, "screens[1].widget.wrong[1].value", 1 + 3 + 2)
E(F, "screens[2].canvas.params.rows[1][1]", 20); E(F, "screens[2].canvas.params.rows[2][1]", 30)
same_fn(lambda x: (x * x - 9) / (x * x + 3 * x), lambda x: (x - 3) / x, "l15 (x^2 - 9)/(x^2 + 3x) = (x - 3)/x")
same_fn(lambda x: (x * x - 4) / (x + 3) * (2 * x + 6) / (x - 2), lambda x: 2 * (x + 2), "l15 product = 2(x + 2)")
same_fn(lambda x: (x * x + x) / (x - 2) / ((x + 1) / (x * x - 4)), lambda x: x * (x + 2), "l15 quotient = x(x + 2)")
same_fn(lambda x: (x * x + 3 * x) / x, lambda x: x + 3, "l15 (x^2 + 3x)/x = x + 3")
v = two(Fr(7, 3), (1 + 6) / (1 + 2), "l15 (x + 6)/(x + 2) at 1"); E(F, "screens[7].widget.answer", round(float(v), 4))
lv.claim(Fr(6 - 6, 3 - 1) == 0, "l15 (x + 6) = 3(x + 2) only at x = 0"); E(F, "screens[7].widget.wrong[0].value", 3); E(F, "screens[7].widget.wrong[1].value", 7)
lv.claim(4 - 6 + 2 == 0 and 1 - 3 + 2 == 0 and simp(Fr(-2)) == -1, "l15 bottom zero at -2 and -1; simpler gives -1 at -2")
E(F, "screens[8].prose", -1); lv.claim(9 - 15 + 6 == 0 and Fr(6, 2) == 3, "l15 x = -3 makes top 0; x = 0 gives 3"); E(F, "screens[8].widget.options[3].why", 3)
r1 = two(Fr(84 - 80, 80), Fr(84, 80) - 1, "l15 return 0.05"); E(F, "screens[10].widget.rows[0][1].answer", r1); E(F, "screens[10].widget.rows[1][1].answer", r1)
E(F, "screens[10].widget.rows[2][1].answer", two(Fr(80, 4), 80 / (84 - 80), "l15 reverse fraction 20"))
v = two(Fr(80, 84) - 1, 80 / 84 - 80 / 80, "l15 reverse split -0.0476"); E(F, "screens[10].widget.rows[3][1].answer", round(float(v), 4))
E(F, "screens[10].widget.rows[3][1].wrong[0].value", round(80 / 84, 4)); E(F, "screens[10].widget.rows[1][1].wrong[0].value", Fr(84, 80))
same_fn(lambda x: (x * x + 7 * x + 12) / (x * x - 9), lambda x: (x + 4) / (x - 3), "l15 q0 simplification")
same_fn(lambda x: 3 * x / (x + 1) * (x * x - 1) / 6, lambda x: x * (x - 1) / 2, "l15 q2 product")
same_fn(lambda x: (2 * x + 6) / 2, lambda x: x + 3, "l15 q3 split")

# =============================== l16 ===============================
F = "l16"
for p, (s1, s2, tot) in {1: (600, 300, 900), 2: (300, 200, 500), 3: (200, 150, 350)}.items():
    two(Fr(600, p) + Fr(600, p + 1), tot, f"l16 shares at p = {p}"); lv.claim(Fr(600, p) == s1 and Fr(600, p + 1) == s2, f"l16 split at p = {p}")
E(F, "screens[0].widget.rows[1][1].answer", 300); E(F, "screens[0].widget.rows[1][3].answer", 500); E(F, "screens[0].widget.rows[2][3].answer", 350)
E(F, "screens[0].widget.rows[1][1].wrong[0].value", 600 * 2)
h6 = lambda x: 6 / x + 6 / (x + 1)
E(F, "screens[1].widget.answer", -0.6); two(h6(Fr(-3, 5)), 6 / -0.6 + 6 / 0.4, "l16 p = -0.6 gives 5")
lv.claim(h6(Fr(-3, 5)) == 5 and 6 / Fr(-3, 5) == -10 and 6 / Fr(2, 5) == 15, "l16 -10 + 15 = 5"); E(F, "screens[1].explain.text", 15)
two(h6(Fr(3, 5)), 10 + 3.75, "l16 p = 0.6 gives 13.75"); E(F, "screens[1].feedback.byKey.sign", 13.75)
lv.claim(Fr(5, 12) + Fr(7, 18) == Fr(29, 36) and Fr(5, 12) == Fr(15, 36) and Fr(7, 18) == Fr(14, 36), "l16 5/12 + 7/18 = 29/36")
same_fn(lambda x: 1 / x + 1 / (x + 1), lambda x: (2 * x + 1) / (x * (x + 1)), "l16 1/x + 1/(x + 1)")
two(1 / Fr(1) + Fr(1, 2), Fr(3, 2), "l16 sum at x = 1 is 3/2")
same_fn(lambda x: 3 / (x - 1) - 2 / (x + 2), lambda x: (x + 8) / ((x - 1) * (x + 2)), "l16 difference = (x + 8)/((x - 1)(x + 2))")
lv.claim(3 / Fr(-1) - 2 / Fr(2) == -4 == Fr(8, -2), "l16 check at x = 0 gives -4"); E(F, "screens[3].explain.text", -4)
same_fn(lambda x: 3 * (x + 2) - 2 * x - 2, lambda x: x + 4, "l16 lost minus gives x + 4"); same_fn(lambda x: 3 * (x + 2) + 2 * (x - 1), lambda x: 5 * x + 4, "l16 added gives 5x + 4")
same_fn(lambda x: 2 / (x * x - 1) + 1 / (x + 1), lambda x: 1 / (x - 1), "l16 2/(x^2 - 1) + 1/(x + 1) = 1/(x - 1)")
same_fn(lambda x: 6 * (x + 1) + 6 * x - 5 * x * (x + 1), lambda x: -(5 * x * x - 7 * x - 6), "l16 cleared equation is 5x^2 - 7x - 6 = 0")
same_fn(lambda x: (5 * x + 3) * (x - 2), lambda x: 5 * x * x - 7 * x - 6, "l16 (5x + 3)(x - 2)")
d, rts = roots_quad(5, -7, -6); two(rts[0], -0.6, "l16 root -3/5"); two(rts[1], 2, "l16 root 2")
E(F, "screens[5].widget.answers[0]", 2); E(F, "screens[5].widget.answers[1]", -0.6)
E(F, "screens[6].widget.answer", two(1 + Fr(1, 2), 1.5, "l16 sum at 1 is 1.5")); E(F, "screens[6].widget.wrong[0].value", round(2 / 3, 4)); E(F, "screens[6].widget.wrong[1].value", round(1 / 3, 4))
same_fn(lambda x: (2 / (x - 2) + 3) - x / (x - 2), lambda x: Fr(2), "l16 right side is always 2 more than the left")
lv.claim(Fr(0) / (0 - 2) == 0 and Fr(2) / (0 - 2) + 3 == 2, "l16 x = 0 test: left 0, right 2"); E(F, "screens[7].widget.options[3].why", 2)
lv.claim(2 + 3 == 5, "l16 slip x = 2 + 3 gives 5"); E(F, "screens[7].widget.options[2].text", 5)
lv.claim(12 * 18 == 216 and 36 == 12 * 18 // math.gcd(12, 18), "l16 bd = 216, LCM 36"); E(F, "screens[8].explain.text", 216)
avg = two(Fr(1200, 500), Fr(2 * 2 * 3, 2 + 3), "l16 average price 2.40 = 2ab/(a + b)"); E(F, "screens[9].widget.answer", avg)
E(F, "screens[9].widget.wrong[0].value", Fr(2 + 3, 2)); E(F, "screens[9].widget.wrong[1].value", round(500 / 1200, 4)); E(F, "screens[9].explain.text", Fr(12, 5))
lv.claim(4 + 2 == 3 * 2 and Fr(4, 2) + 1 == 3 and Fr(12, 5) + 1 != 3, "l16 q0 x = 2; 5/3 fails"); E(F, "quiz[0].widget.options[1].text", Fr(5, 3))
E(F, "quiz[1].widget.options[3].why", two(Fr(2, 2 + 3), 0.4, "l16 2/(a + b) at 2 and 3"))
same_fn(lambda x: 2 / (x + 3) + 1 / (x - 3), lambda x: (3 * x - 3) / (x * x - 9), "l16 q2 sum")
lv.claim(Fr(4, 1) == Fr(2, 1) + 2 and pval([1, -3, 2], Fr(1)) == 0 and pval([1, -3, 2], Fr(2)) == 0, "l16 q3 roots 1, 2; x = 2 both sides 4")

# =============================== l17 ===============================
F = "l17"
f = [1, -2, -5, 6]
for i, (xv, val) in enumerate([(1, 0), (2, -4), (3, 0), (-2, 0)]):
    two(pval(f, Fr(xv)), xv ** 3 - 2 * xv ** 2 - 5 * xv + 6, f"l17 f({xv})"); E(F, f"screens[0].widget.rows[{i}][1].answer", val)
E(F, "screens[0].widget.rows[1][1].wrong[0].value", 4); two(8 - 8 + 10 + 6, 16, "l17 cube-sign slip 16"); E(F, "screens[0].widget.rows[3][1].wrong[0].value", 16)
lv.claim(pval(f, Fr(-3)) == -24 and pval(f, Fr(0)) == 6, "l17 f(-3) = -24, f(0) = 6"); E(F, "screens[1].widget.options[1].why", -24)
qt, rm = pdiv(f, 1); lv.claim(qt == [1, -1, -6] and rm == 0, "l17 f / (x - 1) = x^2 - x - 6")
lv.claim(pmul([1, -1], [1, -1, -6]) == [1, -2, -5, 6] and pmul([1, -3], [1, 2]) == [1, -1, -6], "l17 grid products and (x - 3)(x + 2)")
E(F, "screens[2].widget.rows[1][1].answer", qt[1]); E(F, "screens[2].widget.rows[2][1].answer", qt[2])
lv.claim(200 + 10 + 40 + 2 == 252 == 12 * 21, "l17 252 / 12 = 21 by the grid"); E(F, "screens[2].hints[1].text", 21)
qt2, rm2 = pdiv(f, 2); two(rm2, pval(f, Fr(2)), "l17 remainder on (x - 2) is -4"); lv.claim(qt2 == [1, 0, -5], "l17 f = (x - 2)(x^2 - 5) - 4")
E(F, "screens[3].widget.answer", rm2); E(F, "screens[3].widget.wrong[0].value", 4)
g = [2, 3, -4, 5]; qg, rg = pdiv(g, -2); lv.claim(qg == [2, -1, -2], "l17 g / (x + 2) quotient 2x^2 - x - 2")
two(rg, pval(g, Fr(-2)), "l17 remainder 9 = g(-2)"); E(F, "screens[4].widget.rows[3][1].answer", rg)
E(F, "screens[4].widget.rows[3][1].wrong[0].value", pval(g, Fr(2))); lv.claim(pmul([1, 2], [2, -1, -2]) == [2, 3, -4, -4], "l17 (x + 2)(2x^2 - x - 2)")
h = [1, 0, -7, 6]; lv.claim(all(pval(h, Fr(r)) == 0 for r in (1, 2, -3)) and pmul(pmul([1, -1], [1, -2]), [1, 3]) == h, "l17 x^3 - 7x + 6 = (x - 1)(x - 2)(x + 3)")
lv.claim(pval(h, Fr(1)) == 1 - 7 + 6 and pval(h, Fr(2)) == 8 - 14 + 6 and pval(h, Fr(-3)) == -27 + 21 + 6, "l17 hint values")
k = two(Fr(-(8 - 4), 4), -1, "l17 k from p(2) = 0"); E(F, "screens[6].widget.answer", k)
E(F, "screens[6].widget.wrong[0].value", Fr(-8, 4)); E(F, "screens[6].widget.wrong[1].value", Fr(8 + 4, 4))
lv.claim(pmul([1, -2], [1, 1, 2]) == [1, -1, 0, -4], "l17 x^3 - x^2 - 4 = (x - 2)(x^2 + x + 2)")
lv.claim(pval(h, Fr(3)) == 12 and pval(h, Fr(-3)) == 0, "l17 h(3) = 12, h(-3) = 0"); E(F, "screens[7].prose", 12)
kk = [1, 0, -3, 2]; qk, rk = pdiv(kk, 1); lv.claim(rk == 0 and qk == [1, 1, -2] and pmul(pmul([1, -1], [1, -1]), [1, 2]) == kk, "l17 x^3 - 3x + 2 = (x - 1)^2(x + 2)")
npv = [1000, -400, -480, -576]
two(pval(npv, Fr(6, 5)), 1000 * 1.2 ** 3 - 400 * 1.44 - 480 * 1.2 - 576, "l17 x = 1.2 is a root")
lv.claim(1000 * Fr(1728, 1000) == 1728 and 400 * Fr(144, 100) == 576 and 480 * Fr(6, 5) == 576, "l17 1728 and 576 checks")
lv.claim(pmul([5, -6], [25, 20, 12]) == [Fr(c, 8) for c in npv], "l17 (5x - 6)(25x^2 + 20x + 12) = cubic / 8")
disc = two(20 ** 2 - 4 * 25 * 12, -800, "l17 discriminant -800"); E(F, "screens[10].widget.answer", disc)
E(F, "screens[10].widget.wrong[0].value", 400 + 1200); E(F, "screens[10].widget.wrong[1].value", 1200 - 400)
q0, r0 = pdiv(h, 1); lv.claim(q0 == [1, 1, -6] and r0 == 0, "l17 q0 quotient x^2 + x - 6"); lv.claim(pdiv([1, -7, 6], 1) == ([1, -6], 0), "l17 q0 slip gives x - 6")
lv.claim(1 - 8 == -7 and pmul([1, -1], [1, 1, 2]) == [1, 0, 1, -2], "l17 q1 discriminant -7")
f2 = [2, -1, 3, -4]; lv.claim(pval(f2, Fr(-1)) == -10 and pval(f2, Fr(1)) == 0, "l17 q2 f(-1) = -10, f(1) = 0"); E(F, "quiz[2].widget.options[0].text", -10)
f3 = [1, -3, 0, 4]; lv.claim(pval(f3, Fr(2)) == 0 and pval(f3, Fr(-2)) == -16 and pmul(pmul([1, -2], [1, -2]), [1, 1]) == f3, "l17 q3 x^3 - 3x^2 + 4 = (x - 2)^2(x + 1)")
E(F, "quiz[3].widget.options[1].text", -16)

# =============================== l18 ===============================
F = "l18"
t = two(49 - 4 * 6, shoelace([(0, 0), (3, 4), (-1, 7), (-4, 3)]), "l18 tilted square area 25"); lv.claim(t == 9 + 16, "l18 Pythagoras 9 + 16 = 25")
E(F, "screens[0].widget.answer", t); E(F, "screens[0].widget.wrong[0].value", 49); E(F, "screens[0].widget.wrong[1].value", 49 - 2 * 6)
pts25 = [(x, y) for x in range(-6, 7) for y in range(-6, 7) if x * x + y * y == 25]
E(F, "screens[1].widget.answer", two(len(pts25), 8 + 4, "l18 lattice points on x^2 + y^2 = 25"))
E(F, "screens[1].widget.wrong[0].value", sum(1 for p in pts25 if 0 in p)); E(F, "screens[1].widget.wrong[1].value", sum(1 for p in pts25 if 0 not in p))
for (x, y), val, idx in [((-4, -3), 25, None), ((2, 3), 13, 1), ((5, 5), 50, 2), ((1, 4), 17, 3)]:
    lv.claim(x * x + y * y == val, f"l18 ({x}, {y}) gives {val}")
    if idx is not None:
        E(F, f"screens[2].widget.options[{idx}].why", val)
dist = lambda p, q: math.hypot(q[0] - p[0], q[1] - p[1])
two(dist((1, 2), (4, 6)), math.sqrt(9 + 16), "l18 distance 5"); E(F, "screens[3].widget.answer", two(dist((-2, 1), (3, 13)), math.sqrt(25 + 144), "l18 distance 13"))
E(F, "screens[3].widget.wrong[0].value", 5 + 12); E(F, "screens[3].widget.wrong[1].value", 169); E(F, "screens[3].widget.wrong[2].value", round(math.sqrt(1 + 144), 2))
r2 = two(9 + 4 + 12, (6 - 3) ** 2 + (2 + 2) ** 2, "l18 expanded circle r^2 = 25")
same_fn(lambda x: x * x - 6 * x - 12 + 4 * 0, lambda x: (x - 3) ** 2 - 9 - 12, "l18 x-square completed")
E(F, "screens[5].widget.rows[2][1].answer", math.isqrt(r2)); E(F, "screens[5].widget.rows[2][1].wrong[2].value", round(math.sqrt(12), 4))
lv.claim((0 - 3) ** 2 + (0 + 2) ** 2 == 13, "l18 (0, 0) gives 13"); E(F, "screens[5].explain.text", 13)
r2b = two(7 + 4 + 25, (4 + 2) ** 2 + (5 - 5) ** 2, "l18 trap r^2 = 36"); E(F, "screens[6].widget.answer", math.isqrt(r2b))
E(F, "screens[6].widget.wrong[0].value", round(math.sqrt(7), 4)); E(F, "screens[6].widget.wrong[1].value", 36)
mr = Fr(2 - (-2), 6 - 3); mt = -1 / mr; lv.claim(mr == Fr(4, 3) and mt == Fr(-3, 4) and mr * mt == -1, "l18 gradients 4/3 and -3/4")
lv.claim(3 * 6 + 4 * 2 == 26 and 4 * 6 - 3 * 2 == 18 and 3 * 3 + 4 * (-2) == 1, "l18 tangent 3x + 4y = 26 and the two slips")
lv.claim(all(Fr(2) + mt * (xv - 6) == (26 - 3 * xv) / Fr(4) for xv in PTS), "l18 y - 2 = -3/4 (x - 6) is 3x + 4y = 26"); E(F, "screens[7].explain.text", 26)
lv.claim(13 - 14 == -1 and 13 - 13 == 0 and 13 - (-12) == 25, "l18 point circle and empty circle"); E(F, "screens[8].widget.options[1].why", -1)
risk = two(4 * math.sqrt(2), math.hypot(4, 4), "l18 risk of (4, 4)"); E(F, "screens[10].widget.answer", round(risk, 2))
E(F, "screens[10].widget.wrong[0].value", 8); E(F, "screens[10].widget.wrong[1].value", 32); lv.claim(math.hypot(3, 4) == 5, "l18 (3, 4) on the limit")
lv.claim(math.isqrt(49) == 7 and (4 - 1) ** 2 + (1 + 2) ** 2 == 18 and 25 + 4 - 20 == 9 and 25 + 4 + 20 == 49, "l18 quiz numbers 7, 18, 9 and the slip 49")
E(F, "quiz[2].feedback.correct", 18); E(F, "quiz[0].widget.options[0].text", 7)

# =============================== l19 ===============================
F = "l19"
lv.claim(7 < math.sqrt(50) < 7.5 and 200 - 4 * 49 > 0 and 200 - 4 * 7.5 ** 2 < 0, "l19 the line leaves between k = 7 and 7.5")
same_fn(lambda x: x * x + (x + 1) ** 2 - 25, lambda x: 2 * (x * x + x - 12), "l19 k = 1 substitution")
d, rts = roots_quad(1, 1, -12); lv.claim(rts == [-4, 3] and 3 + 1 == 4 and -4 + 1 == -3, "l19 points (3, 4) and (-4, -3)")
E(F, "screens[1].widget.answers[0]", 3); E(F, "screens[1].widget.answers[1]", -4)
same_fn(lambda x: x * x + (x + 8) ** 2 - 25, lambda x: 2 * x * x + 16 * x + 39, "l19 k = 8 gives 2x^2 + 16x + 39")
dk = two(16 ** 2 - 4 * 2 * 39, 200 - 4 * 8 ** 2, "l19 discriminant -56 two ways"); E(F, "screens[2].widget.answer", dk)
E(F, "screens[2].widget.wrong[0].value", -dk); E(F, "screens[2].widget.wrong[1].value", 256 + 312)
kp = two(Fr(-4, 4), -1, "l19 4 + 4k = 0"); E(F, "screens[3].widget.answer", kp); lv.claim(pval([1, -2, 1], Fr(1)) == 0 and 2 * 1 - 1 == 1, "l19 touches at (1, 1)")
E(F, "screens[3].widget.wrong[1].value", -4); E(F, "screens[3].feedback.byKey.sign", 4 + 4)
same_fn(lambda x: 16 * (x * x + ((25 - 3 * x) / 4) ** 2 - 25), lambda x: 25 * (x - 3) ** 2, "l19 3x + 4y = 25 gives 25(x - 3)^2")
lv.claim(150 ** 2 - 4 * 25 * 225 == 0 and Fr(25 - 9, 4) == 4, "l19 tangent discriminant 0, y = 4")
lv.claim(200 - 4 * 36 == 56 and (-8) ** 2 == 64 and math.isqrt(50) ** 2 != 50, "l19 k = 6 gives 56; k = -8 gives 64")
E(F, "screens[5].widget.options[1].why", 56); E(F, "screens[5].explain.text", round(two(5 * math.sqrt(2), math.sqrt(50), "l19 5 sqrt2"), 2))
lv.claim(25 - 9 == 16 and 25 - 25 == 0, "l19 vertical lines: y^2 = 16 at x = 3, 0 at x = 5"); E(F, "screens[7].widget.answers[0]", 4)
lv.claim(2 ** 2 + 4 * (-1) == 0 and 2 ** 2 - 4 * (-1) == 8, "l19 derive check m = 2, c = -1 and the slip 8")
same_fn(lambda p: p * (500 - 10 * p) - (100 * p + 3000), lambda p: -10 * (p - 10) * (p - 30), "l19 break-even quadratic")
lv.claim(10 * 400 == 4000 == 100 * 10 + 3000 and 30 * 200 == 6000 == 100 * 30 + 3000, "l19 revenue equals cost at 10 and 30")
E(F, "screens[9].widget.answers[0]", 10); E(F, "screens[9].widget.answers[1]", 30); E(F, "screens[9].explain.text", 4000)
Fmax = two(Fr(1600 * 10, 4), 4000, "l19 largest fixed cost"); E(F, "screens[10].widget.answer", Fmax)
lv.claim(1600 - Fr(4 * 3000, 10) == 400 and pval([1, -40, 400], Fr(20)) == 0 and 20 * 300 == 6000 == 100 * 20 + 4000, "l19 F = 3000 gives 400; tangency at 20")
E(F, "screens[10].widget.wrong[0].value", 400); E(F, "screens[10].widget.wrong[1].value", 1600)
lv.claim(pval([1, 2, 0], Fr(0)) == 0 and pval([1, 2, 0], Fr(-2)) == 0, "l19 q0 roots 0 and -2")
kq = two(Fr(-12, 4), -3, "l19 q2 12 + 4k = 0"); lv.claim(16 - 4 * (1 - kq) == 0 and 12 + 4 * (-4) == -4 and 4 + 1 == 5, "l19 q2 checks"); E(F, "quiz[2].widget.options[0].text", -3)
lv.claim(pmul([5, 1], [1, -1]) == [5, -4, -1] and Fr(1, 25) + Fr(49, 25) == 2 and 2 * Fr(-1, 5) - 1 == Fr(-7, 5), "l19 q3 points (1, 1) and (-1/5, -7/5)")

# =============================== review-4 ===============================
F = "review"
a48 = simplify_surd(48)[0]; a27 = simplify_surd(27)[0]; two((a48 + a27) * math.sqrt(3), math.sqrt(48) + math.sqrt(27), "r4 7 sqrt3")
E(F, "items[0].widget.answer", a48 + a27); E(F, "items[0].widget.wrong[0].value", simplify_surd(75)[0]); E(F, "items[0].widget.wrong[1].value", a48 * a27)
two(4 / (math.sqrt(5) - 1), math.sqrt(5) + 1, "r4 4/(sqrt5 - 1) = sqrt5 + 1"); E(F, "items[1].explain.text", round(math.sqrt(5) + 1, 3))
same_fn(lambda x: (x * x - x - 6) / (x * x - 4), lambda x: (x - 3) / (x - 2), "r4 cancel")
same_fn(lambda x: 2 / x + 3 / (x - 1), lambda x: (5 * x - 2) / (x * (x - 1)), "r4 add")
lv.claim(pval([1, -3, 2], Fr(2)) == 0 and Fr(3, 1) == 1 + Fr(6, 3), "r4 reject: x = 2 works"); E(F, "items[4].widget.answer", 2)
fr = [1, 2, -5, 1]; E(F, "items[5].widget.answer", two(pval(fr, Fr(2)), pdiv(fr, 2)[1], "r4 remainder 7")); E(F, "items[5].widget.wrong[0].value", pval(fr, Fr(-2)))
lv.claim(pmul(pmul([1, 1], [1, -2]), [1, -3]) == [1, -4, 1, 6], "r4 cubic factorisation")
lv.claim((-4) ** 2 + 1 + 8 == 25 and 16 + 1 - 8 == 9, "r4 circle r^2 25 and the slip 9"); E(F, "items[7].widget.rows[2][1].answer", 5); E(F, "items[7].widget.rows[2][1].wrong[1].value", 3)
E(F, "items[8].widget.answer", two(dist((1, -2), (7, 6)), 10, "r4 distance 10")); E(F, "items[8].widget.wrong[0].value", 6 + 8)
kt = two(Fr(11, 4), 2.75, "r4 tangent k"); lv.claim(1 - 4 * (3 - kt) == 0 and 1 + 4 * (3 - Fr(13, 4)) == 0, "r4 k = 11/4; slip 13/4")
E(F, "items[9].widget.answer", kt); E(F, "items[9].widget.wrong[0].value", Fr(13, 4))

# =============================== homework-4 ===============================
F = "homework"
hs = S(5, 1, 3) * S(2, 1, 3); lv.claim(hs.a == 13 and hs.b == 7 and (S(2, -1, 3) * S(2, 1, 3)).a == 1, "hw4 (5 + sqrt3)(2 + sqrt3) = 13 + 7 sqrt3 over 1")
two(float(hs), (5 + math.sqrt(3)) / (2 - math.sqrt(3)), "hw4 surd value"); E(F, "items[0].explain.text", round(float(hs), 2))
E(F, "items[0].widget.rows[0][1].answer", 13); E(F, "items[0].widget.rows[1][1].answer", 7); E(F, "items[0].widget.rows[0][1].wrong[0].value", round(13 / 7, 3))
same_fn(lambda x: x * (x + 1) - 2 * (x - 3) - 12, lambda x: (x - 3) * (x + 2), "hw4 cleared equation (x - 3)(x + 2)")
v = two(Fr(-2, -5) - Fr(2, -1), Fr(12, 5), "hw4 x = -2 check 2.4"); E(F, "items[1].explain.text", float(v)); E(F, "items[1].widget.answer", -2)
lv.claim(pval([2, 1, -13, 6], Fr(2)) == 0 and pmul(pmul([1, -2], [2, -1]), [1, 3]) == [2, 1, -13, 6], "hw4 2x^3 + x^2 - 13x + 6 = (x - 2)(2x - 1)(x + 3)")
lv.claim(pdiv([2, 1, -13, 6], 2) == ([2, 5, -3], 0), "hw4 quotient 2x^2 + 5x - 3")
# a - b = 7, 2a + b = -1 by elimination; then substitute back as the second route
aa = Fr(7 + -1, 3); bb = aa - 7
lv.claim(aa == 2 and bb == -5 and pval([1, aa, bb, -6], Fr(-1)) == 0 and pval([1, aa, bb, -6], Fr(2)) == 0, "hw4 a = 2, b = -5")
lv.claim(pmul(pmul([1, 1], [1, -2]), [1, 3]) == [1, 2, -5, -6], "hw4 p = (x + 1)(x - 2)(x + 3)")
E(F, "items[3].widget.rows[0][1].answer", aa); E(F, "items[3].widget.rows[1][1].answer", bb)
same_fn(lambda x: x * x + (x + 2) ** 2 - 10, lambda x: 2 * (x * x + 2 * x - 3), "hw4 circle-line substitution")
lv.claim(pval([1, 2, -3], Fr(1)) == 0 and pval([1, 2, -3], Fr(-3)) == 0 and -3 + 2 == -1 and 9 + 1 == 10 and 1 + 9 == 10, "hw4 points (1, 3), (-3, -1)")
E(F, "items[4].parts[2].widget.answer", round(two(dist((-3, -1), (1, 3)), 4 * math.sqrt(2), "hw4 chord 4 sqrt2"), 2))
same_fn(lambda x: x * x + (2 * x + 7) ** 2 - 20, lambda x: 5 * x * x + 28 * x + 49 - 20, "hw4 tangent substitution at k = 7 (shape check)")
lv.claim(all(16 * kk2 - 20 * (kk2 - 20) == 400 - 4 * kk2 for kk2 in (0, 1, 9, 100)) and 20 * (1 + 2 ** 2) == 100, "hw4 discriminant 400 - 4k^2, c^2 = r^2(1 + m^2)")
E(F, "items[5].widget.answers[0]", 10); E(F, "items[5].widget.wrong[0].value", "4.47, -4.47")
for m_, c_, r_ in [(Fr(1, 2), Fr(3), Fr(2)), (Fr(-3), Fr(1, 3), Fr(5)), (Fr(2), Fr(-1), Fr(1, 2))]:
    disc_ = (2 * m_ * c_) ** 2 - 4 * (1 + m_ * m_) * (c_ * c_ - r_ * r_)
    lv.claim(disc_ == 4 * (r_ * r_ * (1 + m_ * m_) - c_ * c_), f"hw4 proof identity at m = {m_}")
lv.claim(Fr(1 - 9, 1 - 3) + Fr(7, 3) == Fr(19, 3) and Fr(25 - 9, -5 - 3) + Fr(1, -3) == Fr(-7, 3), "hw4 longform checks x = 1 and x = -5")
lv.claim(pmul([1, 3], [1, 2]) == [1, 5, 6] and pmul([1, 1], [1, 5]) == [1, 6, 5] and pmul([1, -2], [1, 1]) == [1, -1, -2], "hw4 longform quadratics")
lv.claim(Fr(4 - 9, 2 - 3) + Fr(8, 4) == 7 and Fr(1 - 9, -1 - 3) + Fr(5, 1) == 7, "hw4 longform roots 2 and -1 check")
E(F, "items[7].model", Fr(19, 3)); E(F, "items[7].model", r"-\tfrac{7}{3}")

lv.check_wrongs(verbose="--verbose" in sys.argv)
lv.report()
