"""Number recompute for linear-maps level 1 (Vector spaces): l1 to l4, review-1, homework-1. Second reader, session V.

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations
are recomputed here a second way (exact fractions and an exact rank). Checks tied to a sentence (lv.stated) fail
while a false sentence is still in the text, and pass once a fix rewords it. Run from anywhere:
    python3 docs/reports/linear-maps-L1-numbers.py
Failing checks on the current content are findings in docs/reviews/review-linear-maps-1-3.md.
"""
import sys, os, math, json
from fractions import Fraction as F
from itertools import product
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("linear-maps", 1)


def rank(A):
    M = [[F(x) for x in r] for r in A]
    r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def fm(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else repr(float(x))


def tup(*xs):
    return '(' + ', '.join(fm(x) for x in xs) + ')'


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def sc(k, v):
    return tuple(F(k) * x for x in v)


def in_span(v, vs):
    return rank(list(vs) + [list(v)]) == rank(list(vs)) if vs else all(x == 0 for x in v)


def poly(coeffs, x):                      # coeffs low to high
    return sum(F(c) * F(x) ** k for k, c in enumerate(coeffs))


def pmul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += F(a) * b
    return out


def padd(*ps):
    n = max(len(p) for p in ps)
    return [sum(F(p[k]) if k < len(p) else F(0) for p in ps) for k in range(n)]


# ---------------- l1 axioms ----------------
u, v = (F(6, 10), F(4, 10)), (F(3, 10), F(7, 10))
s = add(u, v)
lv.expect("l1", "screens[0].widget.answer", tup(*s))
lv.expect("l1", "screens[0].widget.wrong[0].tex", tup(*sc(F(1, 2), s)))          # averaged
lv.expect("l1", "screens[0].widget.wrong[1].tex", tup(s[0], 1 - s[0]))           # forced the total back to 1
lv.expect("l1", "screens[0].feedback.correct", sum(s))                           # total weight 2
lv.expect("l1", "screens[0].explain.text", sum(u) + sum(v))
lv.expect("l1", "screens[1].explain.text", 2)
# P2 against degree exactly 2: (x^2 + x) + (-x^2 + 1) = x + 1
lv.claim(padd([0, 1, 1], [1, 0, -1]) == [1, 1, 0], "l1 s3: (x^2 + x) + (-x^2 + 1) = x + 1")
lv.expect("l1", "screens[3].prose", "x + 1")
# R^[0,1]: f = x^2, g = 1 - x at 0.5
fv, gv = F(1, 2) ** 2, 1 - F(1, 2)
lv.expect("l1", "screens[4].widget.answer", float(fv + gv))
lv.expect("l1", "screens[4].widget.wrong[0].value", float(fv))
lv.expect("l1", "screens[4].widget.wrong[1].value", float(gv))
lv.expect("l1", "screens[4].widget.wrong[2].value", float(fv * gv))
lv.expect("l1", "screens[4].explain.text", float(fv + gv))
lv.expect("l1", "screens[4].prose", 252)
# odd scalar rule lambda(a, b) = (lambda a, 0): only 1v = v fails, on a grid
def smul(l, w):
    return (l * w[0], F(0))
grid = [F(k, 2) for k in range(-4, 5)]
vecs = [(a, b) for a in grid[::2] for b in grid[::2]]
dist1 = all(smul(l + m, w) == add(smul(l, w), smul(m, w)) for l in grid for m in grid for w in vecs)
dist2 = all(smul(l, add(w, z)) == add(smul(l, w), smul(l, z)) for l in grid for w in vecs[:9] for z in vecs[:9])
assoc = all(smul(l * m, w) == smul(l, smul(m, w)) for l in grid for m in grid for w in vecs)
lv.claim(dist1 and dist2 and assoc and smul(1, (2, 3)) != (2, 3), "l1 s5: the three other scaling conditions hold; 1v = v fails")
lv.expect("l1", "screens[5].hints[2].text", tup(*smul(1, (F(2), F(3)))))
# fully invested line: 0 off, sums total 2, -u total -1
lv.claim(0 + 0 != 1 and sum(add(u, v)) == 2 and sum(sc(-1, u)) == -1, "l1 s6: (0,0) off x + y = 1; sum total 2; -u total -1")
lv.expect("l1", "screens[6].hints[1].text", -1)
# positive reals: zero is 1, inverse of 2 is 1/2, (xy)^l = x^l y^l
lv.expect("l1", "screens[7].widget.answer", 1)
lv.expect("l1", "screens[7].widget.wrong[0].value", 0)
lv.claim(all(abs((x * y) ** l - x ** l * y ** l) < 1e-12 for x in (0.5, 2.0, 3.0) for y in (0.25, 5.0) for l in (-1.5, 0.5, 2.0)),
         "l1 s7: (xy)^lambda = x^lambda y^lambda on positive reals")
lv.expect("l1", "quiz[1].widget.answer", float(F(1, 2)))
lv.expect("l1", "quiz[1].widget.wrong[0].value", -2)
lv.expect("l1", "quiz[1].widget.wrong[1].value", 2)
lv.expect("l1", "quiz[1].feedback.byKey.same", 2 * 2)
lv.claim(2 ** -1 == 0.5, "l1 quiz[1]: (-1) (.) 2 = 2^-1 = 1/2")
lv.expect("l1", "quiz[3].prose", 252)
# Statement (coverage): the transfer explain argues "they live in some R^n", which long-only portfolios also do
lv.stated("l1", "screens[11].explain.text", "are lists, so they live in some", False)

# ---------------- l2 subspaces ----------------
lv.expect("l2", "screens[0].explain.text", 3 * 2)                        # xy for (3, 2)
x1, x2 = (F(1), F(1), F(-1)), (F(3), F(0), F(-1))
plane = lambda w: w[0] + 2 * w[1] + 3 * w[2]
lv.claim(plane(x1) == 0 and plane(x2) == 0 and plane(add(x1, x2)) == 0, "l2 s3: (1,1,-1), (3,0,-1) and their sum lie in x1 + 2x2 + 3x3 = 0")
lv.expect("l2", "screens[4].prose", 2)                                   # p(0) + q(0) = 1 + 1
lv.claim(poly([1, F(1, 2)], 0) + poly([1, 0, -1], 0) == 2, "l2 s4: (p + q)(0) = 2 for p = 1 + x/2, q = 1 - x^2")
U1 = [[1, 0, 0], [0, 1, 0]]; U2 = [[0, 0, 1]]; U3 = [[0, 1, 1]]
pair0 = lambda A, B: rank(A + B) == rank(A) + rank(B)
lv.claim(pair0(U1, U2) and pair0(U1, U3) and pair0(U2, U3), "l2 s8: U1, U2, U3 meet pairwise in 0")
lv.claim(rank(U1 + U2 + U3) == 3 and 2 + 1 + 1 == 4, "l2 s8: U1 + U2 + U3 = R^3 with dimensions 2 + 1 + 1 = 4")
third = sc(-1, add((0, 1, 0), (0, 0, 1)))
lv.expect("l2", "screens[9].widget.answer", tup(*third))
lv.expect("l2", "screens[9].widget.wrong[0].tex", tup(*sc(-1, third)))
lv.claim(add((0, 1, 0), (0, 0, 1), third) == (0, 0, 0) and third[1] == third[2], "l2 s9: (0,1,0) + (0,0,1) + (0,-1,-1) = 0, and (0,-1,-1) is in U3")
lv.expect("l2", "screens[9].prose", 4)
# Statement: "Lesson 4 shows why that rules out a direct sum" - l4 never mentions a direct sum
lv.stated("l2", "screens[9].prose", "Lesson 4 shows why", 'direct sum' in lv.text("l4", "screens") or '\\oplus' in lv.text("l4", "screens"))
# even part of e^x: cosh, at nine points
lv.claim(all(abs((math.exp(t) + math.exp(-t)) / 2 + (math.exp(t) - math.exp(-t)) / 2 - math.exp(t)) < 1e-12 for t in [k / 2 for k in range(-4, 5)]),
         "l2 s10: cosh x + sinh x = e^x at nine points")
r = (F(3, 100), F(-1, 100), F(1, 100))
c = sum(r) / 3
m = (c, c, c)
z = add(r, sc(-1, m))
lv.expect("l2", "screens[11].widget.answer", tup(*m))
lv.expect("l2", "screens[11].widget.wrong[0].tex", tup(*z))
lv.expect("l2", "screens[11].widget.wrong[1].tex", tup(*(sum(r),) * 3))
lv.expect("l2", "screens[11].hints[1].text", float(sum(r)))
lv.claim(sum(z) == 0, "l2 s11: the zero-sum part sums to 0")
lv.expect("l2", "quiz[3].widget.answer", tup(*z))
lv.expect("l2", "quiz[3].widget.wrong[0].tex", tup(*add(r, m)))
lv.expect("l2", "quiz[0].widget.options[1].why", 8)
# Statement: analysis l15-epsilon-delta "proves" sums of continuous functions are continuous
an = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'analysis', 'l15-epsilon-delta.json')))
an_txt = json.dumps(an)
lv.stated("l2", "screens[4].prose", "l15-epsilon-delta proves it", 'f + g' in an_txt or 'sum of continuous' in an_txt)

# ---------------- l3 span and independence ----------------
A, Bv, C, D = (1, 0, 2), (0, 1, 1), (1, 1, 0), (0, 0, 3)
w = (F(1), F(-1), F(-1))
lv.claim(add(A, sc(w[0], Bv), sc(w[1], C), sc(w[2], D)) == (0, 0, 0), "l3 s0: A + B - C - D = 0")
lv.expect("l3", "screens[0].widget.answer", tup(*w))
lv.expect("l3", "screens[0].widget.wrong[0].tex", tup(*sc(-1, w)))
lv.expect("l3", "screens[1].widget.options[0].text", tup(*sc(2, w)))
lv.claim(add(sc(2, A), sc(2, Bv), sc(-2, C), sc(-2, D)) == (0, 0, 0), "l3 s1: (2, -2, -2) with 2 units of A gives 0")
lv.claim(rank([A, Bv, C]) == 3 and add(A, Bv, sc(-1, C)) == D, "l3 s2: (A, B, C) independent and D = A + B - C")
e1, e2, e3 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
u1, u2 = (1, 1, 0), (0, 1, 1)
lv.claim(add(u1, sc(-1, e1)) == e2 and not in_span(e1, [u1]) and not in_span(u2, [u1]), "l3 s4: e2 = u1 - e1; e1 not in span(u1); u2 not in span(u1)")
lv.claim(not in_span(e1, [u1, u2]) and add(sc(-1, u1), u2, e1) == e3, "l3 s4: e1 not in span(u1, u2); e3 = -u1 + u2 + e1")
# Wrong: the refusal for Remove e3 at s0 says e3 is in the span before it
lv.stated("l3", "screens[4].widget.states.s0.ops[2].why", "is in the span before it", in_span(e3, [u1, e1, e2]))
lv.claim(not in_span(e3, [u1, e1, e2]), "l3 quiz[0]: e3 is not in span(u1, e1, e2) (third entry 0)")
lv.claim(rank([(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]) == 3, "l3 s8: the no-parallel-pair list has rank 3, so it is dependent")
lv.claim(rank([(1, 0, 0), (2, 0, 0), (0, 1, 0)]) == 2, "l3 s7: (e1, 2e1, e2) is dependent")
lv.expect("l3", "screens[11].prose", 251)
lv.claim(500 > 252, "l3 s11: 500 columns in R^252 are dependent")
lv.expect("l3", "screens[10].widget.examples[0].expect", 3)

# ---------------- l4 bases and dimension ----------------
p = [3, 2, 1]                                                    # 3 + 2x + x^2
a = poly(p, 1); cc = F(1); b = F(2) + 2 * cc                     # x-coefficient: b - 2c = 2
q = padd([a], pmul([b], [-1, 1]), pmul([cc], [1, -2, 1]))
lv.claim(q == [F(3), F(2), F(1)], "l4 s0: 6 + 4(x - 1) + (x - 1)^2 = 3 + 2x + x^2")
lv.expect("l4", "screens[0].widget.answer", tup(a, b, cc))
lv.expect("l4", "screens[0].widget.wrong[0].tex", tup(*p))
std = padd([3], pmul([2], [-1, 1]), pmul([1], [1, -2, 1]))      # sliders (3, 2, 1) in the new basis
lv.claim(std == [F(2), F(0), F(1)], "l4 s0: sliders (3, 2, 1) draw x^2 + 2")
# Wrong: "which is p - 1" (p - 1 = x^2 + 2x + 2)
lv.stated("l4", "screens[0].feedback.byKey.std", "which is $p - 1$", std == padd(p, [-1]))
lv.expect("l4", "screens[0].hints[1].text", int(a))
lv.claim(rank([[-1, 1, 0, 0], [-1, 0, 1, 0], [-1, 0, 0, 1]]) == 3 and all(poly(t, 1) == 0 for t in ([-1, 1], [-1, 0, 1], [-1, 0, 0, 1])),
         "l4 s5: x - 1, x^2 - 1, x^3 - 1 are independent and vanish at 1")
for i, (dim, wr) in enumerate([(4, None), (4, 3), (6, None), (3, 4), (0, 1)]):
    lv.expect("l4", f"screens[5].widget.rows[{i}][2].answer", dim)
    if wr is not None:
        lv.expect("l4", f"screens[5].widget.rows[{i}][2].wrong[0].value", wr)
lv.claim(2 * 3 == 6 and 3 + 1 == 4, "l4 s5: dim R^(2x3) = 6, dim P3 = 4")
v1, v2 = (1, 0, 1, 0), (0, 1, 0, 1)
keep = []
for j in range(4):
    e = tuple(1 if i == j else 0 for i in range(4))
    keep.append('keep' if not in_span(e, [v1, v2] + [k for k in []]) and rank([v1, v2] + [tuple(1 if i == jj else 0 for i in range(4)) for jj in range(j) if keep[jj] == 'keep'] + [e]) > rank([v1, v2] + [tuple(1 if i == jj else 0 for i in range(4)) for jj in range(j) if keep[jj] == 'keep']) else 'skip')
lv.claim(keep == ['keep', 'keep', 'skip', 'skip'], f"l4 s6: extension keeps e1, e2 and skips e3, e4 (got {keep})")
lv.claim(add(v1, sc(-1, e1 + (0,))) == (0, 0, 1, 0) and add(v2, sc(-1, (0, 1, 0, 0))) == (0, 0, 0, 1), "l4 s6: e3 = v1 - e1, e4 = v2 - e2")
Uw = [(1, 0, 1, 0), (0, 1, 0, 1)]; Ww = [(1, 1, 0, 0), (0, 0, 1, 1)]
dsum = rank(Uw + Ww); dint = 2 + 2 - dsum
lv.claim(dint == 1 and in_span((1, 1, 1, 1), Uw) and in_span((1, 1, 1, 1), Ww), "l4 s8: U and W meet in span{(1,1,1,1)}")
lv.expect("l4", "screens[8].widget.answer", dsum)
lv.expect("l4", "screens[8].widget.wrong[0].value", 2 + 2)
lv.expect("l4", "screens[8].widget.wrong[1].value", dint)
abc = [(1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 1, 1)]
lv.expect("l4", "screens[9].widget.answer", rank(abc))
lv.expect("l4", "screens[9].widget.wrong[0].value", 3)
lv.expect("l4", "screens[9].widget.wrong[1].value", 4)
L, S = (1, 1, 1, 1), (-3, -1, 1, 3)
days = [add(sc(x, L), sc(y, S)) for x, y in [(2, 1), (-1, 2), (3, 0), (0, -1), (1, 1), (2, -1)]]
lv.expect("l4", "screens[11].widget.answer", rank(days))
lv.claim(days[2] == sc(3, L) and days[3] == sc(-1, S), "l4 s11: day 3 = 3 x level, day 4 = -1 x slope")
lv.expect("l4", "screens[11].widget.wrong[0].value", 6)
lv.expect("l4", "screens[11].widget.wrong[1].value", 4)
lv.claim(padd([0, -1, 1], [1, 0, -1], [-1, 1]) == [0, 0, 0], "l4 quiz[0]: x^2 - x = (x^2 - 1) - (x - 1)")
ab = (F(3 + 5, 2), F(3 - 5, 2))
lv.expect("l4", "quiz[1].widget.answer", tup(*ab))
lv.expect("l4", "quiz[1].widget.wrong[1].tex", tup(ab[1], ab[0]))
lv.expect("l4", "quiz[2].widget.answer", 3 * 4)
lv.expect("l4", "quiz[2].widget.wrong[0].value", 3 + 4)
lv.expect("l4", "quiz[2].widget.wrong[1].value", 3)
lv.expect("l4", "screens[10].widget.examples[0].expect", "[[1, 1, 0], [0, 1, 1], [1, 0, 0]]")

# ---------------- review-1 ----------------
def sm2(l, w):
    return (l * w[0], w[1])
lv.claim(sm2(2, (1, 1)) == (2, 1) and add(sm2(1, (1, 1)), sm2(1, (1, 1))) == (2, 2), "review items[0]: (1+1)v = (2,1) but v + v = (2,2)")
lv.claim(all(sm2(l * m, w) == sm2(l, sm2(m, w)) for l in grid for m in grid for w in vecs) and sm2(1, (2, 3)) == (2, 3), "review items[0]: the other conditions hold")
lv.expect("review", "items[3].widget.answer", 5 - 2)
lv.expect("review", "items[3].widget.wrong[0].value", 5)
lv.expect("review", "items[3].widget.wrong[1].value", 5 - 1)
lv.expect("review", "items[3].widget.wrong[2].value", 4 - 2)
lv.claim(rank([[0, -1, 1, 0, 0], [0, 0, -1, 1, 0], [0, 0, 0, -1, 1]]) == 3, "review items[3]: x(x-1), x^2(x-1), x^3(x-1) independent")
lv.expect("review", "items[4].widget.answer", (2 * 5) ** 3)
lv.expect("review", "items[4].widget.wrong[0].value", 3 * 10)
lv.expect("review", "items[4].widget.wrong[1].value", 3 * (2 + 5))
lv.expect("review", "items[4].explain.text", 2 ** 3)
lv.expect("review", "items[4].explain.text", 5 ** 3)
lv.claim(rank([(1, 0, 0), (0, 1, 0), (1, 1, 1)]) == 3, "review items[5]: U + W = R^3, U and W meet in 0")
lv.expect("review", "items[7].widget.answer", tup(1, 2, 1))
lv.claim(padd([1], pmul([2], [-1, 1]), [1, -2, 1]) == [0, 0, 1], "review items[7]: 1 + 2(x - 1) + (x - 1)^2 = x^2")
lv.claim(padd([1], pmul([-2], [-1, 1]), [1, -2, 1]) == [4, -4, 1], "review items[7]: 1 - 2(x - 1) + (x - 1)^2 = x^2 - 4x + 4")

# ---------------- homework-1 ----------------
lv.claim(rank([(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (1, 1, 1, 1), (0, 0, 0, 1)]) == 4, "homework items[4]: U + W = R^4")
lv.expect("homework", "items[4].widget.answer", 3 + 2 - 4)
lv.expect("homework", "items[4].widget.wrong[2].value", 3 + 2)
lv.claim(in_span((1, 1, 1, 0), [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)]) and add((1, 1, 1, 1), sc(-1, (0, 0, 0, 1))) == (1, 1, 1, 0), "homework items[4]: (1,1,1,0) spans the overlap")
Bh = [(1, 1, 0), (0, 1, 1), (1, 0, 0)]
co = (F(-1), F(4), F(3))
lv.claim(add(*[sc(k, b_) for k, b_ in zip(co, Bh)]) == (2, 3, 4), "homework items[5]: -(1,1,0) + 4(0,1,1) + 3(1,0,0) = (2,3,4)")
lv.expect("homework", "items[5].widget.answer", tup(*co))
lv.claim(poly([1, -1], 0) * poly([1, -1], 1) == 0 and poly([0, 1], 0) * poly([0, 1], 1) == 0 and poly([1], 0) * poly([1], 1) == 1, "homework items[2]: f(0)f(1) = 0 for 1 - x and x, sum gives 1")
lv.claim(2 + 2 - 1 == 3, "homework items[8].model: the lesson check 2 + 2 - 1 = 3")
lv.claim(rank(days[:2]) == 2, "homework items[3]: the first two yield days are independent")

lv.check_wrongs()
lv.report()
