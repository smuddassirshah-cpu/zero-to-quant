"""Number recompute for linear-maps level 2 (Linear maps): l5 to l9, review-2, homework-2. Second reader, session V.

Every graded key, every numeric wrong[] value and the numbers stated in prose, hints, feedback and explanations
are recomputed a second way (exact fractions, exact rank and matrix products). Checks tied to a sentence
(lv.stated) fail while a false sentence is in the text and pass once a fix rewords it. Run from anywhere:
    python3 docs/reports/linear-maps-L2-numbers.py
Failing checks on the current content are findings in docs/reviews/review-linear-maps-1-3.md.
"""
import sys, os
from fractions import Fraction as F
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("linear-maps", 2)


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


def mm(A, B):
    return [[sum(F(A[i][k]) * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, v):
    return tuple(sum(F(A[i][k]) * v[k] for k in range(len(v))) for i in range(len(A)))


def tr(A):
    return [list(r) for r in zip(*A)]


def inv2(A):
    a, b, c, d = (F(x) for x in (A[0][0], A[0][1], A[1][0], A[1][1]))
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def fm(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else repr(float(x))


def tup(*xs):
    return '(' + ', '.join(fm(x) for x in xs) + ')'


def pm(M):
    return '\\begin{pmatrix}' + '\\\\'.join('&'.join(fm(x) for x in r) for r in M) + '\\end{pmatrix}'


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def sc(k, v):
    return tuple(F(k) * x for x in v)


# ---------------- l5 linear maps ----------------
Tm = [[2, 1], [3, -2]]                                   # T(x, y) = (2x + y, 3x - 2y)
T = lambda w: mv(Tm, w)
lv.claim(T((1, 1)) == (3, 1) and T((1, -1)) == (1, 5), "l5 s0: T(1,1) = (3,1), T(1,-1) = (1,5) for T(x,y) = (2x + y, 3x - 2y)")
lv.expect("l5", "screens[0].widget.answer", tup(*T((2, 0))))
lv.expect("l5", "screens[0].widget.wrong[0].tex", tup(*sc(2, T((1, 1)))))
lv.expect("l5", "screens[0].widget.wrong[1].tex", tup(*sc(2, T((1, -1)))))
lv.expect("l5", "screens[0].widget.wrong[2].tex", tup(2, 0))
lv.expect("l5", "screens[2].widget.answer", tup(*T((3, 1))))
lv.claim(add(sc(2, (1, 1)), (1, -1)) == (3, 1), "l5 s2: (3,1) = 2(1,1) + (1,-1)")
lv.expect("l5", "screens[2].widget.wrong[0].tex", tup(*add(sc(3, T((1, 1))), T((1, -1)))))
lv.expect("l5", "screens[2].widget.wrong[1].tex", tup(*T((2, 0))))
G = lambda w: (w[0] * w[1], w[0])
lv.claim(G((2, 2)) == (4, 2) and sc(2, G((1, 1))) == (2, 2), "l5 s3: G(2,2) = (4,2) but 2G(1,1) = (2,2)")
f = lambda x: 2 * x + 3
lv.claim(f(2) == 7 and f(1) + f(1) == 10 and 2 * f(1) == 10 and f(0) == 3, "l5 s6: f(2) = 7, f(1) + f(1) = 10, f(0) = 3")
half = add(sc(F(1, 2), (1, 1)), sc(F(-1, 2), (1, -1)))
lv.claim(half == (0, 1), "l5 s9: (0,1) = 1/2(1,1) - 1/2(1,-1)")
lv.expect("l5", "screens[9].widget.answer", tup(*T((0, 1))))
lv.expect("l5", "screens[9].widget.wrong[0].tex", tup(*add(T((1, 1)), sc(-1, T((1, -1))))))
lv.expect("l5", "screens[9].widget.wrong[1].tex", tup(*add(sc(F(1, 2), T((1, 1))), sc(F(1, 2), T((1, -1))))))
lv.expect("l5", "screens[9].hints[2].text", 1.5)
lv.expect("l5", "screens[9].hints[2].text", 2.5)
h, pr, dp = (100, 50), (12, 30), (F(40, 100), F(-20, 100))
lv.expect("l5", "screens[10].prose", sum(a * b for a, b in zip(h, pr)))
chg = sum(a * b for a, b in zip(h, dp))
lv.expect("l5", "screens[10].widget.answer", float(chg))
lv.expect("l5", "screens[10].widget.wrong[0].value", float(sum(a * b for a, b in zip(h, pr)) + chg))
lv.expect("l5", "screens[10].widget.wrong[1].value", float(h[0] * dp[0] - h[1] * dp[1]))
lv.expect("l5", "screens[10].widget.wrong[2].value", float(dp[0] + dp[1]))
lv.expect("l5", "screens[10].feedback.byKey.total", 2730)
lv.expect("l5", "screens[10].feedback.byKey.sign", 10)
Tq = lambda w: (w[0] + w[1], 1)
lv.claim(Tq((0, 0)) == (0, 1), "l5 quiz[0]: T(0,0) = (0,1)")
lv.expect("l5", "quiz[1].widget.answer", tup(*add(sc(4, (2, 3)), sc(-1, (1, -2)))))
lv.expect("l5", "quiz[1].widget.wrong[0].tex", tup(*add(sc(4, (2, 3)), (1, -2))))
# Misleading: the "rows" slip, A = [[2, 3], [1, -2]] applied to (4, -1), gives (5, 6), not (5, 14)
rows_slip = mv([[2, 3], [1, -2]], (4, -1))
lv.stated("l5", "quiz[1].widget.wrong[1].tex", "(5, 14)", rows_slip == (5, 14))
lv.expect("l5", "quiz[1].widget.wrong[1].tex", tup(*rows_slip))
lv.expect("l5", "quiz[1].feedback.byKey.rows", tup(*rows_slip))
lv.claim(rows_slip == (5, 6), "l5 quiz[1]: the rows slip gives (5, 6)")
# shift S p(x) = p(x + 1) on 3 + 2x + x^2
Sm = [[1, 1, 1], [0, 1, 2], [0, 0, 1]]
lv.expect("l5", "quiz[2].widget.answer", "6 + 4x + x^2")
lv.claim(mv(Sm, (3, 2, 1)) == (6, 4, 1), "l5 quiz[2]: S(3 + 2x + x^2) = 6 + 4x + x^2")
lv.expect("l5", "quiz[2].widget.wrong[0].tex", "4 + 2x + x^2")

# ---------------- l6 kernel and image ----------------
E = [[1, F(6, 10), F(-4, 10)], [0, F(2, 10), F(2, 10)]]
k = (F(-1), F(1), F(-1))
lv.claim(mv(E, k) == (0, 0), "l6 s0: E(-1, 1, -1) = (0, 0)")
lv.expect("l6", "screens[0].widget.answer", tup(*k))
lv.claim(mv(E, (-1, 1, 1))[1] == F(4, 10) and mv(E, (1, 1, 1))[0] == F(12, 10), "l6 s0: wrongs: vega 0.4; delta 1.2")
lv.expect("l6", "screens[0].feedback.byKey.vega", 0.4)
lv.expect("l6", "screens[0].feedback.byKey.long", 1.2)
lv.expect("l6", "screens[1].widget.options[0].text", tup(*sc(2, k)))
lv.claim(mv(E, (-1, 2, -1))[1] == F(2, 10) and mv(E, (-2, 2, 2))[1] == F(8, 10), "l6 s1: (-1,2,-1) leaves vega 0.2; (-2,2,2) has vega 0.8")
lv.expect("l6", "screens[2].widget.answer", 3 - rank(E))
lv.expect("l6", "screens[2].widget.wrong[0].value", 3)
lv.expect("l6", "screens[2].widget.wrong[2].value", rank(E))
lv.expect("l6", "screens[4].widget.options[3].why", tup(*add(mv(E, (1, 0, 0)), mv(E, (0, 1, 0)))))
T6 = [[1, 1, 0], [0, 1, 1]]
lv.expect("l6", "screens[5].widget.answer", tup(1, -1, 1))
lv.claim(mv(T6, (1, -1, 1)) == (0, 0) and mv(T6, (1, 1, 1)) == (2, 2), "l6 s5: T(1,-1,1) = 0, T(1,1,1) = (2,2)")
lv.claim(all(mv(T6, (1 + t, -t, t)) == (1, 0) for t in range(-3, 4)), "l6 s5: (1 + t, -t, t) maps to (1, 0)")
b1, b2 = (10, 2, 3), (5, 7, -2)
lv.claim(mv(E, b1) == (10, 1) and mv(E, b2) == (10, 1), "l6 s11: both books have delta 10 and vega 1")
lv.expect("l6", "screens[11].widget.options[0].text", tup(*add(b2, sc(-1, b1))))
lv.claim(add(b2, sc(-1, b1)) == sc(5, k), "l6 s11: the difference is 5(-1, 1, -1)")
Tq1 = [[1, -2], [2, -4]]
lv.expect("l6", "quiz[1].widget.answer", tup(2, 1))
lv.claim(mv(Tq1, (2, 1)) == (0, 0) and mv(Tq1, (1, 2)) == (-3, -6) and mv(Tq1, (-2, 1)) == (-4, -8), "l6 quiz[1]: T(2,1) = 0, T(1,2) = (-3,-6), T(-2,1) = (-4,-8)")
lv.claim(rank([[1, 0], [1, 1], [0, 1]]) == 2, "l6 quiz[3]: T(x, y) = (x, x + y, y) is injective")

# ---------------- l7 rank-nullity ----------------
Dm = [[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
for i, (dv, dk, di) in enumerate([(4, 4 - rank(Dm), rank(Dm)), (3, 3 - rank(T6), rank(T6)), (2, 2, 0)]):
    lv.expect("l7", f"screens[0].widget.rows[{i}][1]", dv)
    lv.expect("l7", f"screens[0].widget.rows[{i}][2]", dk)
    lv.expect("l7", f"screens[0].widget.rows[{i}][3].answer", di)
lv.claim(mv([[1, 2], [1, 2]], (2, -1)) == (0, 0), "l7 s1: rows (1,2), (1,2) send (2,-1) to 0")
Fm = [[1, 0, 1, 2, 0], [0, 1, 1, 0, 1], [1, 1, 0, 1, 1]]
Bm = [[1, 2, 0, 1, 0], [0, 0, 1, 1, 0], [1, 2, 1, 2, 0]]
lv.claim(rank(Fm) == 3 and rank([[r[j] for j in range(3)] for r in Fm]) == 3, "l7 s8: F has rank 3; its first three columns are independent")
lv.claim(all(any(r[j] != 0 for r in Fm) for j in range(5)), "l7 s2: F has no zero column")
lv.expect("l7", "screens[8].widget.answer", 5 - rank(Fm))
lv.expect("l7", "screens[8].widget.wrong[0].value", rank(Fm))
lv.expect("l7", "screens[8].widget.wrong[1].value", 5)
lv.expect("l7", "screens[8].widget.wrong[2].value", 3 - rank(Fm))
lv.claim([a + b for a, b in zip(Bm[0], Bm[1])] == Bm[2] and rank(Bm) == 2, "l7 s9: B's row 3 = row 1 + row 2, rank 2")
lv.expect("l7", "screens[9].widget.answer", 5 - rank(Bm))
lv.expect("l7", "screens[9].widget.wrong[0].value", 3 - rank(Bm))
lv.expect("l7", "screens[9].widget.wrong[1].value", 5 - 3)
lv.expect("l7", "screens[10].widget.examples[0].expect", "[2, 3]")
lv.expect("l7", "quiz[1].widget.answer", 5 - 2)
lv.expect("l7", "quiz[1].widget.wrong[0].value", 4 - 2)
lv.claim(all(c[0] == 0 and sum(c) == 0 for c in ([0, 1, -1, 0, 0], [0, 1, 0, -1, 0], [0, 1, 0, 0, -1])) and rank([[0, 1, -1, 0, 0], [0, 1, 0, -1, 0], [0, 1, 0, 0, -1]]) == 3,
         "l7 quiz[1]: x - x^2, x - x^3, x - x^4 vanish at 0 and 1 and are independent")
lv.expect("l7", "quiz[3].widget.answer", 3)

# ---------------- l8 maps as matrices ----------------
lv.claim(Dm == [[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]], "l8 s0: [D] columns (0,0,0), (1,0,0), (0,2,0), (0,0,3)")
for i in range(3):
    for j in range(4):
        lv.expect("l8", f"screens[0].widget.rows[{i}][{j + 1}].answer", Dm[i][j])
for i, h in enumerate(["$1$", "$x$", "$x^2$"]):
    lv.expect("l8", f"screens[0].widget.rows[{i}][0]", h)
lv.expect("l8", "screens[2].widget.answer", pm(Sm))
lv.expect("l8", "screens[2].widget.wrong[0].tex", pm(tr(Sm)))
lv.expect("l8", "screens[3].widget.answer", tup(*mv(Sm, (3, 2, 1))))
lv.expect("l8", "screens[3].widget.wrong[0].tex", tup(*mv(tr(Sm), (3, 2, 1))))
D2 = [[0, 1, 0], [0, 0, 2]]
DS = mm(D2, Sm)
lv.expect("l8", "screens[4].hints[2].text", pm(DS))
lv.expect("l8", "screens[4].explain.text", pm(DS))
lv.claim([r[2] for r in DS] == [2, 2], "l8 s4: D((x + 1)^2) = 2x + 2, last column (2, 2)")
lv.expect("l8", "screens[5].widget.options[0].text", "2 & 1\\\\ 3 & -2")
lv.claim(mv(tr(Tm), (1, 0)) == (2, 1), "l8 s5: the transpose sends e1 to (2, 1)")
A8 = [[4, 1], [2, 3]]
X = [[1, 1], [1, -2]]
M8 = mm(inv2(X), mm(A8, X))
lv.expect("l8", "screens[7].widget.answer", pm(M8))
lv.claim(mv(A8, (1, 1)) == (5, 5) and mv(A8, (1, -2)) == (2, -4), "l8 s7: A x1 = (5,5) = 5 x1, A x2 = (2,-4) = 2 x2")
lv.expect("l8", "screens[7].widget.wrong[0].tex", pm(A8))
lv.expect("l8", "screens[7].widget.wrong[1].tex", pm([[2, 0], [0, 5]]))
lv.expect("l8", "screens[7].widget.wrong[2].tex", pm(mm(A8, X)))
P = [[1, 1], [1, -1]]
cc = mv(inv2(P), (5, 1))
lv.expect("l8", "screens[8].widget.answer", tup(*cc))
lv.expect("l8", "screens[8].widget.wrong[1].tex", tup(cc[1], cc[0]))
Sig = [[3, 1], [1, 3]]
lv.claim(mm(inv2(P), mm(Sig, P)) == [[4, 0], [0, 2]], "l8 s10: P^-1 Sigma P = diag(4, 2)")
lv.claim(mm(tr(P), mm(Sig, P)) == [[8, 0], [0, 4]], "l8 s10: P^T Sigma P = diag(8, 4)")
var = sum(a * b for a, b in zip((1, 1), mv(Sig, (1, 1))))
lv.expect("l8", "screens[10].widget.answer", var)
lv.expect("l8", "screens[10].widget.wrong[0].value", 4)
lv.expect("l8", "screens[10].widget.wrong[1].value", 3 + 3)
lv.expect("l8", "quiz[1].widget.options[2].text", "0.5 & 0.5\\\\ 0.5 & -0.5")
lv.claim(inv2(P) == [[F(1, 2), F(1, 2)], [F(1, 2), F(-1, 2)]], "l8 quiz[1]: [I]_E^B = P^-1")
lv.expect("l8", "quiz[2].widget.answer", pm([[1, 2], [0, 3]]))
lv.expect("l8", "quiz[3].widget.answer", pm(D2))
lv.expect("l8", "screens[9].widget.examples[0].expect", "[3, 2]")
Bb = [[1, 1, 1], [0, 1, 1], [0, 0, 1]]
lv.claim(mv(Bb, (0, 2, 1)) == (3, 3, 1), "l8 code test 6: coords of (3,3,1) in (1, 1 + x, 1 + x + x^2) are (0, 2, 1)")

# ---------------- l9 invertible and isomorphic ----------------
C = [[105, 0, 0], [5, 105, 0], [5, 5, 105]]
prices = (F('101.85'), F('103.55'), F('105.10'))
d1 = prices[0] / 105
d2 = (prices[1] - 5 * d1) / 105
d3 = (prices[2] - 5 * d1 - 5 * d2) / 105
lv.claim(mv(C, (d1, d2, d3)) == prices and (d1, d2, d3) == (F('0.97'), F('0.94'), F('0.91')), "l9 s0: C d = prices with d = (0.97, 0.94, 0.91)")
for i, dk in enumerate((d1, d2, d3)):
    lv.expect("l9", f"screens[0].widget.rows[{i}][1].answer", float(dk))
lv.claim(abs(prices[1] / 105 - F('0.9862')) <= F('0.0005') and abs(prices[2] / 105 - F('1.001')) <= F('0.0005'), "l9 s0: wrongs 103.55/105 ~ 0.9862 and 105.10/105 ~ 1.001")
lv.expect("l9", "screens[0].explain.text", float(prices[1] - 5 * d1))
lv.expect("l9", "screens[0].explain.text", float(prices[2] - 5 * d1 - 5 * d2))
lv.expect("l9", "screens[0].feedback.byKey.coupon", float(5 * d1))
lv.expect("l9", "screens[0].feedback.byKey.coupon3", float(5 * d2))
Cp = [[105, 0, 0], [5, 105, 0], [10, 210, 0]]
lv.claim(rank(Cp) == 2 and mv(Cp, (0, 0, 1)) == (0, 0, 0) and 2 * prices[1] == F('207.10'), "l9 s1: C' has rank 2, kills (0,0,1), bond 3' priced 2 x 103.55")
lv.expect("l9", "screens[11].widget.answer", 3 - rank(Cp))
lv.expect("l9", "screens[11].widget.wrong[1].value", rank(Cp))
lv.expect("l9", "screens[10].prose", 10)                                     # 0.1 I of size 10
lv.claim(abs(0.1 ** 10 - 1e-10) < 1e-22, "l9 s10: det(0.1 I_10) = 10^-10")
Ci = [[F(1, 105), 0, 0], [F(-5, 105 ** 2), F(1, 105), 0], [F(-500, 105 ** 3), F(-5, 105 ** 2), F(1, 105)]]
lv.claim(mm(C, Ci) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "l9 code test 1: the inverse of C")
lv.expect("l9", "screens[10].widget.examples[0].expect", "[[1, -1], [-1, 2]]")
lv.claim(inv2([[2, 1], [1, 1]]) == [[1, -1], [-1, 2]], "l9 s10 example: inverse of [[2,1],[1,1]]")
lv.expect("l9", "quiz[1].widget.answer", 2 * 4)
lv.expect("l9", "quiz[1].widget.wrong[0].value", 2 + 4)
lv.expect("l9", "quiz[1].widget.wrong[1].value", 4 * 4)
lv.expect("l9", "quiz[1].explain.text", 2 * 4)
lv.expect("l9", "screens[7].prose", 6)

# ---------------- review-2 ----------------
lv.claim(add((1, -1), (2, -2)) == (3, -3) and (1 + -1, 2 + -2) == (0, 0), "review items[1]: T(1,-1,2,-2) = (0, 0)")
lv.claim((1 + 1, 0 + 0) == (2, 0) and (1 - 1, 2 + 2) == (0, 4), "review items[1]: wrongs (2,0) and (0,4)")
lv.expect("review", "items[2].widget.answer", 6 - 3)
lv.expect("review", "items[2].widget.wrong[0].value", 4 - 3)
lv.expect("review", "items[2].widget.wrong[1].value", 6 - 4)
lv.expect("review", "items[2].widget.wrong[2].value", 6)
Tx = [[0, 0, 0], [0, 1, 0], [0, 0, 2]]                   # T p = x p' in (1, x, x^2)
lv.expect("review", "items[3].widget.answer", tup(*[r[2] for r in Tx]))
lv.expect("review", "items[3].widget.wrong[0].tex", tup(0, 2, 0))
lv.claim(6 == 2 * 3 and 5 + 1 == 6, "review items[4]: dim P5 = 6 = dim R^(2x3)")
t10 = add((1, 0, 1), sc(-2, (0, 1, 1)))
lv.expect("review", "items[5].widget.answer", tup(*t10))
lv.expect("review", "items[5].widget.wrong[0].tex", tup(*add((1, 0, 1), sc(2, (0, 1, 1)))))
lv.expect("review", "items[5].widget.wrong[1].tex", tup(*add((1, 0, 1), sc(-1, (0, 1, 1)))))
A6 = [[2, 0], [0, 3]]; P6 = [[1, 0], [1, 1]]
lv.expect("review", "items[6].widget.options[0].text", "2 & 0\\\\ 1 & 3")
lv.claim(mm(inv2(P6), mm(A6, P6)) == [[2, 0], [1, 3]] and mm(P6, mm(A6, inv2(P6))) == [[2, 0], [-1, 3]], "review items[6]: P^-1 A P and P A P^-1")
T7 = [[1, 0, -1], [0, 1, 1], [1, 1, 0]]
lv.claim(mv(T7, (1, -1, 1)) == (0, 0, 0) and rank(T7) == 2, "review items[7]: T(1,-1,1) = 0, rank 2")

# ---------------- homework-2 ----------------
Pb = [[1, 1, 1], [0, 1, 1], [0, 0, 1]]
D3 = [[0, 1, 0], [0, 0, 2], [0, 0, 0]]
Pinv = [[1, -1, 0], [0, 1, -1], [0, 0, 1]]
lv.claim(mm(Pb, Pinv) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "homework items[1]: P^-1 for (1, 1 + x, 1 + x + x^2)")
DB = mm(Pinv, mm(D3, Pb))
lv.expect("homework", "items[1].widget.answer", pm(DB))
lv.expect("homework", "items[1].widget.wrong[0].tex", pm(D3))
lv.expect("homework", "items[1].widget.wrong[1].tex", pm(tr(DB)))
H = [[1, 2, 0, 1], [0, 0, 1, 1], [1, 2, 1, 2]]
lv.claim(mv(H, (3, 0, 2, 0)) == (3, 2, 5) and rank(H) == 2 and rank([r + [b] for r, b in zip(H, (3, 2, 4))]) == 3, "homework items[3]: H x_p = b, rank 2, b = (3,2,4) inconsistent")
lv.expect("homework", "items[3].widget.answer", 4 - rank(H))
lv.expect("homework", "items[3].widget.wrong[0].value", 3 - rank(H))
lv.expect("homework", "items[3].widget.wrong[2].value", 4)
lv.expect("homework", "items[2].widget.examples[0].expect", "[4, 2]")
lv.expect("homework", "items[5].widget.answer", 4 - 1)
lv.expect("homework", "items[6].widget.answer", 6 - 2)
lv.expect("homework", "items[6].widget.wrong[2].value", 6 - 1)
A7 = [[-4, 3], [3, 4]]; P7 = [[1, 3], [3, -1]]
lv.expect("homework", "items[7].widget.answer", pm(mm(inv2(P7), mm(A7, P7))))
lv.expect("homework", "items[7].widget.wrong[0].tex", pm([[-5, 0], [0, 5]]))
lv.expect("homework", "items[7].widget.wrong[1].tex", pm(A7))
lv.claim(mm(inv2(P7), mm(A7, P7)) == [[5, 0], [0, -5]], "homework items[7]: P^-1 A P = diag(5, -5)")
lv.claim(mv(A7, (1, 3)) == (5, 15) and mv(A7, (3, -1)) == (-15, 5), "homework items[7]: A(1,3) = (5,15) = 5(1,3), A(3,-1) = (-15,5) = -5(3,-1)")
lv.claim(1 + 3 == 4, "homework items[8]: D on P3 has 4 = 1 + 3")

lv.check_wrongs()
lv.report()
