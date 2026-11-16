"""Delta read AE-1: second-route recomputation of six re-keyed problems.

Run with the scratchpad venv Python (numpy, sympy, scipy). Exit 0 on correct content.
Routes differ from the authors' scripts: numpy eigen and pinv, a polar area integral,
lstsq, a brute k-means loop, term-by-term sums, the eta function for the series sum.
"""
import json
import math
import re
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import sympy as sp
from scipy import integrate, optimize

ROOT = Path(__file__).resolve().parents[2]
COURSES = ROOT / "app" / "content" / "courses"
n_checks = 0
fails = []


def check(name, cond, detail=""):
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(f"{name} {detail}")
        print("FAIL", name, detail)


def close(a, b, eps=1e-9):
    return abs(a - b) <= eps


def item(path, iid):
    d = json.loads((COURSES / path).read_text())
    return next(x for x in d["items"] if x["id"] == iid)


def texts(part):
    fb = part.get("feedback", {})
    out = [part.get("question", ""), fb.get("correct", ""), fb.get("generic", "")]
    out += list(fb.get("byKey", {}).values())
    out.append(part.get("explain", {}).get("text", ""))
    for o in part.get("widget", {}).get("options", []):
        out += [o.get("text", ""), o.get("why", "")]
    return " ".join(out)


def tol(w):
    return w.get("tol", {}).get("abs", 0)


def num_part(tag, part, key, wrongs, typed=()):
    """Key and wrong values against my numbers; bands disjoint; typed forms taken."""
    w = part["widget"]
    check(f"{tag} kind", w["kind"] == "numeric")
    check(f"{tag} key", abs(w["answer"] - key) <= max(tol(w), 1e-9) and abs(w["answer"] - key) < 5e-7 + tol(w),
          f"{w['answer']} vs {key}")
    for t in typed:
        check(f"{tag} typed {t} taken", abs(t - w["answer"]) <= tol(w) + 1e-12)
    got = {x["id"]: x for x in w.get("wrong", [])}
    check(f"{tag} wrong ids", set(got) == set(wrongs), f"{sorted(got)} vs {sorted(wrongs)}")
    for wid, val in wrongs.items():
        if wid not in got:
            continue
        x = got[wid]
        check(f"{tag} wrong {wid}", abs(x["value"] - val) <= tol(x) + 1e-12, f"{x['value']} vs {val}")
        check(f"{tag} wrong {wid} refused by key", abs(val - w["answer"]) > tol(w) + tol(x),
              f"{val} against key {w['answer']}")
        check(f"{tag} wrong {wid} exact value outside key band", abs(x["value"] - w["answer"]) > tol(w) + tol(x))
    ids = list(got)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = got[ids[i]], got[ids[j]]
            check(f"{tag} wrong bands {ids[i]}/{ids[j]} apart", abs(a["value"] - b["value"]) > tol(a) + tol(b))


def has(tag, part, *subs):
    t = texts(part)
    for s in subs:
        check(f"{tag} prints {s!r}", s in t)


def nums_in(s):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s)]


# ---------------------------------------------------------------- eigen/problems-2 p-oval-pond
it = item("eigen/problems-2.json", "p-oval-pond")
P = it["parts"]
check("pond prose", "41x^2 + 14xy + 89y^2 = 360" in it["prose"])
x, y = sp.symbols("x y", real=True)
form = 41 * x**2 + 14 * x * y + 89 * y**2
A = np.array([[41.0, 7.0], [7.0, 89.0]])
check("pond A gives the form", sp.expand(sp.Matrix([[x, y]]) * sp.Matrix([[41, 7], [7, 89]]) * sp.Matrix([x, y]))[0] == sp.expand(form))
num_part("pond p1", P[0], 7, {"whole-cross": 14})
ev, evec = np.linalg.eigh(A)
check("pond eigenvalues 40, 90 (eigh)", close(ev[0], 40, 1e-9) and close(ev[1], 90, 1e-9))
w = P[1]["widget"]
check("pond p2 key", sorted(w["answers"]) == [40, 90] and w.get("unordered") is True and tol(w) == 0)
g = {q["id"]: q["value"] for q in w["wrong"]}
check("pond p2 wrongs", g == {"diagonal": "41, 89", "sign": "-40, -90"})
check("pond p2 trace det", close(np.trace(A), 130) and close(np.linalg.det(A), 3600, 1e-6))
has("pond p2", P[1], "3649 - 49 = 3600", "\\lambda^2 - 130\\lambda + 3600", "(\\lambda - 40)(\\lambda - 90)")
v40 = evec[:, 0] * 7 / evec[0, 0]
check("pond p3 eigenvector (7, -1) (eigh)", close(v40[0], 7) and close(v40[1], -1, 1e-9))
check("pond p3 key", P[2]["widget"]["answer"] == "(7, -1)")
g = {q["id"]: q["tex"] for q in P[2]["widget"]["wrong"]}
v90 = evec[:, 1] * 7 / evec[0, 1]
check("pond p3 big is the 90 eigenvector", g["big"] == "(7, 49)" and close(v90[1], 49, 1e-9))
check("pond p3 sign", g["sign"] == "(7, 1)" and not np.allclose(A @ np.array([7, 1]), 40 * np.array([7, 1])))
check("pond p3 A - 40I", np.allclose(A - 40 * np.eye(2), [[1, 7], [7, 49]]))
has("pond p3", P[2], "\\begin{pmatrix} 1 & 7 \\\\ 7 & 49 \\end{pmatrix}", "7 + 7b = 0")


def radius(theta):
    c, s = math.cos(theta), math.sin(theta)
    return math.sqrt(360 / (41 * c * c + 14 * c * s + 89 * s * s))


th_long = math.atan2(-1, 7)
check("pond p4 edge along (7, -1) is 3 m (direct)", close(radius(th_long), 3, 1e-12))
res = optimize.minimize_scalar(lambda t: -radius(t), bounds=(-math.pi / 2, math.pi / 2), method="bounded")
check("pond long half-axis is the farthest edge point", close(-res.fun, 3, 1e-6) and close(math.tan(res.x), -1 / 7, 1e-4))
res2 = optimize.minimize_scalar(radius, bounds=(0, math.pi), method="bounded")
check("pond short half-axis 2 along (1, 7)", close(res2.fun, 2, 1e-6) and close(math.tan(res2.x), 7, 1e-3))
num_part("pond p4", P[3], 3, {"short": 2, "no-root": 360 / 40, "full-axis": 6})
area = integrate.quad(lambda t: 0.5 * radius(t) ** 2, 0, 2 * math.pi)[0]
check("pond area 6 pi (polar integral)", close(area, 6 * math.pi, 1e-8))
num_part("pond p5", P[4], area, {"no-root": math.pi * 9 * 4, "full-axes": math.pi * 6 * 4, "one-axis": math.pi * 9},
         typed=(round(area, 2), 18.85))
has("pond p5", P[4], "\\sqrt{360/90} = 2", "6\\pi = 18.85", "360\\pi/60")
check("pond p5 det route", close(360 * math.pi / math.sqrt(np.linalg.det(A)), area, 1e-8))
check("pond chain restated", "from part 1" in P[1]["question"] and "from part 2" in P[2]["question"]
      and "from part 3" in P[3]["question"] and "from part 4" in P[4]["question"])

# ---------------------------------------------------------------- eigen/problems-4 p-track-laps
it = item("eigen/problems-4.json", "p-track-laps")
P = it["parts"]
X = np.array([[2.0, 8.0], [1.0, 4.0], [2.0, 8.0]])
yv = np.array([35.0, 17.0, 33.0])
check("laps prose", "2 & 8 \\\\ 1 & 4 \\\\ 2 & 8" in it["prose"] and "(35, 17, 33)" in it["prose"] and "4 laps per km" in it["prose"])
G = X.T @ X
check("laps XtX", np.allclose(G, [[9, 36], [36, 144]]) and "9 & 36 \\\\ 36 & 144" in P[0]["question"])
L11 = math.sqrt(G[0, 0]); L21 = G[1, 0] / L11; L22sq = G[1, 1] - L21**2
check("laps L11 3, L21 12", close(L11, 3) and close(L21, 12))
num_part("laps p1", P[0], math.sqrt(max(L22sq, 0)), {"root-144": 12, "subtract-entry": math.sqrt(144 - 36)}, typed=(0,))
check("laps p1 rank 1", np.linalg.matrix_rank(X) == 1)
evG = np.linalg.eigvalsh(G)
check("laps eigenvalues 0 and 153 (eigvalsh)", close(evG[0], 0, 1e-9) and close(evG[1], 153, 1e-9))
num_part("laps p2", P[1], evG[1], {"diagonal": 144, "first-entry": 9})
check("laps p2 eigenvector", np.allclose(G @ np.array([1, 4]), [153, 612]))
has("laps p2", P[1], "(153, 612)", "\\sqrt{153}")
U, S, Vt = np.linalg.svd(X)
check("laps sigma1", close(S[0], math.sqrt(153), 1e-9) and close(S[1], 0, 1e-9))
check("laps u1, v1", np.allclose(abs(U[:, 0]), np.array([2, 1, 2]) / 3) and np.allclose(abs(Vt[0]), np.array([1, 4]) / math.sqrt(17)))
beta = np.linalg.pinv(X) @ yv
check("laps beta+ = (1, 4) (pinv)", np.allclose(beta, [1, 4]))
check("laps beta+ = lstsq min norm", np.allclose(np.linalg.lstsq(X, yv, rcond=None)[0], [1, 4]))
check("laps p3 key", P[2]["widget"]["answer"] == "(1, 4)")
g = {q["id"]: q["tex"] for q in P[2]["widget"]["wrong"]}
check("laps p3 wrong tex", g == {"all-km": "(17, 0)", "all-laps": "(0, 4.25)"})
r0 = np.linalg.norm(X @ beta - yv)
for b in ([17, 0], [0, 4.25]):
    check(f"laps {b} fits as well", close(np.linalg.norm(X @ np.array(b, float) - yv), r0, 1e-9))
    check(f"laps {b} longer", np.linalg.norm(b) > np.linalg.norm(beta))
check("laps u1.y = 51", close(np.array([2, 1, 2]) @ yv / 3, 51) and close(math.sqrt(17) * math.sqrt(153), 51, 1e-9))
has("laps p3", P[2], "\\tfrac13(70 + 17 + 66) = 51", "\\beta_1 + 4\\beta_2 = 17", "\\sqrt{17}\\sqrt{153} = 51")
num_part("laps p4", P[3], float(np.array([3, 12]) @ beta), {"laps-as-km": 3 + 4 * 3, "km-only": 3})
check("laps p4 any fit predicts 51", close(17 * 3, 51) and close(4.25 * 12, 51))
check("laps chain restated", "from part 1" in P[1]["question"] and "from part 2" in P[2]["question"] and "from part 3" in P[3]["question"])

# ---------------------------------------------------------------- vectors/problems-3 p-goat-feed
it = item("vectors/problems-3.json", "p-goat-feed")
P = it["parts"]
pr = it["prose"]
check("goat prose numbers", nums_in(pr) == [0.2, 0.4, 0.1, 0.7, 10, 40], str(nums_in(pr)))
Af = sp.Matrix([[F(2, 10), F(1, 10)], [F(4, 10), F(7, 10)]])
bf = sp.Matrix([10, 40])


def mat_tex(M):
    def s(v):
        v = sp.nsimplify(v)
        return str(int(v)) if v == int(v) else str(float(v))
    return "\\begin{pmatrix}%s&%s\\\\%s&%s\\end{pmatrix}" % tuple(s(v) for v in M)


check("goat p1 key", P[0]["widget"]["answer"] == mat_tex(Af), mat_tex(Af))
check("goat p1 wrong", P[0]["widget"]["wrong"][0]["tex"] == mat_tex(Af.T))
num_part("goat p2", P[1], float(Af.det()), {"added": 0.14 + 0.04, "flipped": -0.1}, typed=(0.1, 0.10))
check("goat det exact", Af.det() == sp.Rational(1, 10))
Ainv = Af.inv()
check("goat p3 key", P[2]["widget"]["answer"] == mat_tex(Ainv) == "\\begin{pmatrix}7&-1\\\\-4&2\\end{pmatrix}")
g = {q["id"]: q["tex"] for q in P[2]["widget"]["wrong"]}
adj = Af.adjugate()
exp = {"no-divide": mat_tex(adj), "no-negate": mat_tex(Ainv.applyfunc(abs)), "transposed": mat_tex(Af.T.inv()),
       "times-det": mat_tex(adj * Af.det())}
check("goat p3 wrongs", g == exp, f"{g} vs {exp}")
check("goat p3 wrongs differ from key", all(v != mat_tex(Ainv) for v in exp.values()) and len(set(exp.values())) == 4)
sol = np.linalg.solve(np.array(Af, float), np.array([10.0, 40.0]))
check("goat blend (30, 40) (solve)", np.allclose(sol, [30, 40]) and list(Ainv * bf) == [30, 40])
check("goat p4 key", P[3]["widget"]["answer"] == "(30, 40)")
g = {q["id"]: q["tex"] for q in P[3]["widget"]["wrong"]}
tr = Af.T.inv() * bf; nd = adj * bf
exp = {"transposed": f"({tr[0]}, {tr[1]})", "no-divide": f"({nd[0]}, {nd[1]})", "swapped": "(40, 30)"}
check("goat p4 wrongs", g == exp, f"{g} vs {exp}")
has("goat p4", P[3], "(70 - 40,\\ -40 + 80)", "6 + 4 = 10", "12 + 28 = 40")
has("goat p3", P[2], "1.4 - 0.4 = 1")
check("goat chain restated", "from part 1" in P[1]["question"] and "from part 2" in P[2]["question"] and "from part 3" in P[3]["question"])

# ---------------------------------------------------------------- series/problems-2 p-app-users
it = item("series/problems-2.json", "p-app-users")
P = it["parts"]
check("app prose", "4 users on day 1" in it["prose"] and "5 times" in it["prose"])
gain = [None, 4]
for d in range(2, 12):
    gain.append(gain[-1] * 5)
tot = [0]
for d in range(1, 12):
    tot.append(tot[-1] + gain[d])
num_part("app p1", P[0], gain[6], {"power-n": gain[7], "day-five": gain[5]})
has("app p1", P[0], "4 \\times 3125 = 12500")
num_part("app p2", P[1], tot[6], {"no-divide-4": 5 * tot[6] - tot[6], "no-first": F(5 * gain[6], 4)})
check("app p2 shifted copy", 5 * tot[6] - tot[6] == 5 * gain[6] - 4 == 62496)
has("app p2", P[1], "4 + 20 + 100 + \\dots + 12500", "4 + 20 + 100 + 500 + 2500 + 12500 = 15624", "62500 - 4 = 62496")
n = sp.symbols("n", positive=True, integer=True)
k = sp.symbols("k", positive=True, integer=True)
Sn = sp.simplify(sp.summation(4 * 5 ** (k - 1), (k, 1, n)))
check("app p3 closed form", sp.simplify(Sn - (5**n - 1)) == 0 and P[2]["widget"]["answer"] == "5^{n}-1")
check("app p3 brute", all(tot[m] == 5**m - 1 for m in range(1, 12)))
g = {q["id"]: q["tex"] for q in P[2]["widget"]["wrong"]}
check("app p3 wrong tex", g == {"no-divide": "4\\cdot5^{n}-4", "power-n-1": "5^{n-1}-1", "sign": "1-5^{n}"})
for m in range(1, 8):
    check(f"app p3 wrongs differ at n={m}", len({5**m - 1, 4 * 5**m - 4, 5 ** (m - 1) - 1, 1 - 5**m}) == 4)
first = next(d for d in range(1, 12) if tot[d] > 350000)
first_gain = next(d for d in range(1, 12) if gain[d] > 350000)
num_part("app p4", P[3], first, {"one-day": first_gain, "day-before": first - 1})
check("app p4 totals", tot[7] == 78124 and tot[8] == 390624)
has("app p4", P[3], "78124", "390624", "350,000", "390,624", "5^n > 350001")
check("app chain restated", "12500" in P[1]["question"] and "S_n = 5^n - 1" in P[3]["question"])

# ---------------------------------------------------------------- analysis/problems-3 p-cube-root-greedy
it = item("analysis/problems-3.json", "p-cube-root-greedy")
P = it["parts"]
eta = float(sp.N((1 - 2 ** sp.Rational(2, 3)) * sp.zeta(sp.Rational(1, 3)), 20))
check("greedy sum 0.5718 (eta function)", f"{eta:.4f}" == "0.5718" and "0.5718" in it["prose"], str(eta))
check("greedy p1 key", [o["id"] for o in P[0]["widget"]["options"] if o.get("correct")] == ["conditional"])
T = 0.2
pos = (m ** (-1 / 3) for m in range(1, 10**6, 2))
neg = (-(m ** (-1 / 3)) for m in range(2, 10**6, 2))
total, seq, tots = 0.0, [], []
for _ in range(200000):
    t = next(pos) if total <= T else next(neg)
    total += t
    seq.append(t)
    tots.append(total)
check("greedy first term 1", seq[0] == 1.0)
num_part("greedy p2", P[1], tots[1], {"positive": 1 + 3 ** (-1 / 3), "square-root": 1 - 2 ** -0.5},
         typed=(round(tots[1], 4), 1 - 0.7937))
num_part("greedy p3", P[2], seq[2], {"sign": -seq[2], "positive": 3 ** (-1 / 3), "odd-neg": -(3 ** (-1 / 3))},
         typed=(round(seq[2], 4), -0.63))
num_part("greedy p4", P[3], tots[3], {"negative-again": tots[2] - 6 ** (-1 / 3), "skipped": tots[2] + 5 ** (-1 / 3)},
         typed=(round(tots[3], 4), -0.4237 + 0.6934))
num_part("greedy p5", P[4], T, {"original": round(eta, 4), "last-total": round(tots[3], 4)}, typed=(0.2, 0.20))
check("greedy totals close on T", abs(tots[-1] - T) < 0.03 and max(abs(v - T) for v in tots[-1000:]) < 0.03)
has("greedy", P[1], "0.7937", "0.2063")
has("greedy", P[2], "-0.6300", "-0.4237")
has("greedy", P[3], "0.6934", "0.2697")
check("greedy printed roundings", f"{2 ** (-1 / 3):.4f}" == "0.7937" and f"{tots[1]:.4f}" == "0.2063"
      and f"{seq[2]:.4f}" == "-0.6300" and f"{tots[2]:.4f}" == "-0.4237" and f"{seq[3]:.4f}" == "0.6934"
      and f"{tots[3]:.4f}" == "0.2697")
check("greedy chain restated", "from part 2" in P[2]["question"] and "from part 3" in P[3]["question"])
# FINDING row: the reworded rule must still say which unused term is taken.
q2 = P[1]["question"]
check("FINDING greedy p2 rule names the next unused term", bool(re.search(r"(next|first|earliest|largest)[^.]*not yet used|next unused", q2)), q2[:120])

# ---------------------------------------------------------------- stat-learning/problems-4 p-order-sizes
it = item("stat-learning/problems-4.json", "p-order-sizes")
P = it["parts"]
orders = [2, 4, 6, 18, 22, 26]
check("orders prose", nums_in(it["prose"]) == orders + [3, 8], str(nums_in(it["prose"])))


def assign(cs):
    return [min(range(2), key=lambda j: abs(o - cs[j])) for o in orders]


def update(lab):
    return [F(sum(o for o, l in zip(orders, lab) if l == j), sum(1 for l in lab if l == j)) for j in range(2)]


def inertia(cs, lab):
    return sum((o - cs[l]) ** 2 for o, l in zip(orders, lab))


for cs in ([3, 8], [3, 18], [4, 22]):
    check(f"orders no tie at centres {cs}", all(abs(o - cs[0]) != abs(o - cs[1]) for o in orders))
lab1 = assign([3, 8]); c1 = update(lab1)
check("orders round 1", c1 == [3, 18] and lab1 == [0, 0, 1, 1, 1, 1])
num_part("orders p1", P[0], c1[1], {"all-orders": F(sum(orders), 6), "kept-centre": F(8 + 72, 5),
                                    "six-misassigned": F(18 + 22 + 26, 3), "percent-sign": 0.18})
cs, lab, rounds = c1, lab1, 1
while True:
    nl = assign(cs)
    if nl == lab and update(nl) == cs:
        break
    lab, cs, rounds = nl, update(nl), rounds + 1
check("orders settle at 4 and 22", cs == [4, 22] and lab == [0, 0, 0, 1, 1, 1])
num_part("orders p2", P[1], cs[1], {"no-reassign": 18, "all-orders": 13, "percent-sign": 0.22})
num_part("orders p3", P[2], inertia(cs, lab), {"unsquared": sum(abs(o - cs[l]) for o, l in zip(orders, lab)),
                                               "averaged": inertia(cs, lab) / 6, "carried": inertia([3, 18], lab),
                                               "not-settled": inertia([3, 18], lab1)})


def f(xv, c):
    return 1 + 2.5 * xv - 1.8 * max(xv - c, 0)


c = (cs[0] + cs[1]) / 2
check("orders knot 13", c == 13)
num_part("orders p4", P[3], f(20, c), {"no-hinge": 1 + 2.5 * 20, "sign": 51 + 1.8 * 7, "knot-at-centre": f(20, 4),
                                       "carried": f(20, (3 + 18) / 2)}, typed=(38.4, 38.40))
num_part("orders p5", P[4], f(20, c) - f(10, c), {"summed-halves": f(20, c) - 2 * f(10, c),
                                                  "negative-hinge": f(20, c) - (26 - 1.8 * (10 - 13)),
                                                  "carried": 51 - f(10, c)}, typed=(12.4,))
has("orders p1", P[0], "\\tfrac{72}{4} = 18")
has("orders p3", P[2], "(4 + 0 + 4) + (16 + 0 + 16) = 40", "2 + 0 + 2 + 4 + 0 + 4")
has("orders p4", P[3], "1.8 \\times 7 = 12.6", "10.5")
has("orders p5", P[4], "f(10) = 1 + 25 = 26", "38.4 - 26 = 12.4")
check("orders chain restated", "from part 2" in P[2]["question"] and "settled centres 4 and 22" in P[3]["question"]
      and "from part 4" in P[4]["question"])

# ---------------------------------------------------------------- relations and proposals quoted in the review
# Finding 1: the pond matrix is l5's worked covariance matrix scaled by 10 and shifted by -2I.
S5 = sp.Matrix([[sp.Rational(11, 10), sp.Rational(3, 10)], [sp.Rational(3, 10), sp.Rational(19, 10)]])
check("pond A = 10 Sigma(l5) - 2I", 10 * S5 - 2 * sp.eye(2) == sp.Matrix([[9, 3], [3, 17]]))
check("l5 Sigma eigenpairs", S5 * sp.Matrix([1, 3]) == 2 * sp.Matrix([1, 3]) and S5 * sp.Matrix([3, -1]) == sp.Matrix([3, -1]))
# Finding 1 option: 40x^2 + 12xy + 45y^2 = 1764.
B = sp.Matrix([[40, 6], [6, 45]])
check("pond option eigen", B.eigenvals() == {36: 1, 49: 1} and B * sp.Matrix([3, -2]) == 36 * sp.Matrix([3, -2])
      and sp.sqrt(sp.Rational(1764, 36)) == 7 and sp.sqrt(sp.Rational(1764, 49)) == 6 and f"{42 * math.pi:.2f}" == "131.95")
# Part B, row 13: p-storage-crate against review-4, and the proposed renumbering.
Vold = x**3 + 4 * x**2 + x - 6
Rev = x**3 - 4 * x**2 + x + 6
check("crate V(x) = -R(-x) of review-4", sp.expand(Vold + Rev.subs(x, -x)) == 0)
Vnew = x**3 + 6 * x**2 + 3 * x - 10
check("crate proposal V(-2) = 0", Vnew.subs(x, -2) == 0)
check("crate proposal quotient", sp.div(Vnew, x + 2, x) == (x**2 + 4 * x - 5, 0))
check("crate proposal factors", sp.factor(Vnew) == (x - 1) * (x + 2) * (x + 5))
check("crate proposal base", sp.expand((x + 2) * (x + 5)) == x**2 + 7 * x + 10 and sp.cancel(Vnew / (x**2 + 7 * x + 10)) == x - 1)
check("crate proposal volume", Vnew.subs(x, sp.Rational(7, 2)) == sp.Rational(116875, 1000) and 5.5 * 8.5 * 2.5 == 116.875)
crate = item("quadratics/problems-4.json", "p-storage-crate")
check("crate content now holds the renumbered cubic", "x^3 + 6x^2 + 3x - 10" in crate["prose"]
      and crate["parts"][1]["widget"]["answer"] == "x^2+4x-5" and crate["parts"][2]["widget"]["answer"] == "(x+2)(x+5)(x-1)"
      and crate["parts"][4]["widget"]["answer"] == 116.875 and "x^2 + 7x + 10" in crate["parts"][3]["question"])
# Part B, pair rule: the true positive sentence keeps no decimal but the two keys.
check("pair rule keeps 1 - 0.7 = 0.3", [v for v in nums_in("r = 1 - 0.7 = 0.3") if v != int(v)] == [0.7, 0.3])

print(f"{n_checks} checks, {len(fails)} failures")
sys.exit(1 if fails else 0)
