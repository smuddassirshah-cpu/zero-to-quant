#!/usr/bin/env python3
"""Second reader's delta read of two problems re-keyed in the fix pass of
docs/reviews/review-delta-ae-1.md:

  eigen/problems-2.json       p-oval-pond
  quadratics/problems-4.json  p-storage-crate

Every key, `wrong` value, band and printed number is rebuilt from givens typed
here. For the pond, every square numeric matrix of app/content/courses/eigen/
(LaTeX matrices, bracketed literals in text and code, nested JSON arrays and
quadratic forms a x^2 + b xy + c y^2) has its eigenvectors computed, and none
outside the item may share the pond's pair (7, -1), (1, 7). For the crate,
every cubic of the quadratics course is factorised and its root pattern
compared with the crate's (a shift, scale or mirror gives the same pattern).

Run: <scratchpad>/venv/bin/python docs/reports/delta-read-eigen-quadratics.py
Exit 0 on correct content.
"""
import glob, json, math, os, re, sys
from fractions import Fraction as F

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CO = os.path.join(ROOT, "app", "content", "courses")
checks = fails = 0


def ok(cond, label):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", label)


def load_item(rel, iid):
    d = json.load(open(os.path.join(CO, rel)))
    return next(i for i in d["items"] if i["id"] == iid)


def wrongs(part):
    return {w["id"]: w for w in part["widget"].get("wrong", [])}


# ====================================================================== pond
pond = load_item("eigen/problems-2.json", "p-oval-pond")
P = pond["parts"]
a, b2, d, c = 41, 14, 89, 360  # typed from the prose: 41x^2 + 14xy + 89y^2 = 360
ok("41x^2 + 14xy + 89y^2 = 360" in pond["prose"], "pond: prose curve as typed")
A = sp.Matrix([[a, F(b2, 2)], [F(b2, 2), d]])
x, y = sp.symbols("x y")
ok(sp.expand((sp.Matrix([[x, y]]) * A * sp.Matrix([x, y]))[0] - (a * x**2 + b2 * x * y + d * y**2)) == 0, "pond: x^T A x is the curve")
# part 1
w = P[0]["widget"]
ok(w["answer"] == A[0, 1] == 7 and w["tol"]["abs"] == 0, "pond p1: off-diagonal 7")
ok(wrongs(P[0])["whole-cross"]["value"] == b2, "pond p1: whole-cross 14")
# part 2: sympy exactly, NumPy numerically
ev = sorted(A.eigenvals().keys())
evn = np.linalg.eigvalsh(np.array(A, float))
ok(ev == [40, 90] and np.allclose(evn, [40, 90]), "pond p2: eigenvalues 40 and 90, two routes")
w = P[1]["widget"]
ok(sorted(w["answers"]) == [40, 90] and w.get("unordered") is True, "pond p2: key {40, 90}, unordered")
ok(A.trace() == 130 and A.det() == 3600 and 41 * 89 == 3649, "pond p2: trace 130, det 3649 - 49 = 3600")
ok(sp.expand((sp.Symbol("l") - 40) * (sp.Symbol("l") - 90) - (sp.Symbol("l") ** 2 - 130 * sp.Symbol("l") + 3600)) == 0, "pond p2: printed factorisation")
ok(wrongs(P[1])["diagonal"]["value"].replace(" ", "") == "41,89", "pond p2: diagonal slip 41, 89")
ok(wrongs(P[1])["sign"]["value"].replace(" ", "") == "-40,-90", "pond p2: sign slip -40, -90")
ok(all(set(map(int, v["value"].split(","))) != {40, 90} for v in wrongs(P[1]).values()), "pond p2: no wrong equals the key")
# part 3
ok(A - 40 * sp.eye(2) == sp.Matrix([[1, 7], [7, 49]]), "pond p3: A - 40I printed")
v40 = (A - 40 * sp.eye(2)).nullspace()[0]
v90 = (A - 90 * sp.eye(2)).nullspace()[0]
par = lambda u, v: sp.Matrix([[u[0], v[0]], [u[1], v[1]]]).det() == 0
ok(par(v40, (7, -1)) and par(v90, (1, 7)), "pond p3: eigenvectors (7, -1) for 40 and (1, 7) for 90")
vec = lambda s: tuple(int(t) for t in re.findall(r"-?\d+", s))
ok(vec(P[2]["widget"]["answer"]) == (7, -1), "pond p3: key (7, -1)")
ok(all(vec(s) == (7, -1) for s in P[2]["widget"]["accept"]), "pond p3: accept forms are the key")
wb, ws = vec(wrongs(P[2])["big"]["tex"]), vec(wrongs(P[2])["sign"]["tex"])
ok(wb == (7, 49) and par(wb, (1, 7)) and A * sp.Matrix(wb) == 90 * sp.Matrix(wb), "pond p3: big (7, 49) is the eigenvector for 90")
ok(ws == (7, 1) and not par(ws, (7, -1)) and not par(ws, (1, 7)), "pond p3: sign (7, 1) is no eigenvector")
ok(v40.dot(v90) == 0, "pond p3: axes perpendicular")
# part 4
long_, short_ = sp.sqrt(sp.Rational(c, 40)), sp.sqrt(sp.Rational(c, 90))
q = np.array([7, -1]) / math.sqrt(50)
ok(long_ == 3 and short_ == 2 and abs((3 * q) @ np.array(A, float) @ (3 * q) - c) < 1e-9, "pond p4: half-axes 3 and 2; the point 3q lies on the edge")
# route 2: scan the curve for the farthest and nearest point from the centre
th = np.linspace(0, 2 * math.pi, 2_000_001)
r = np.sqrt(c / (a * np.cos(th) ** 2 + b2 * np.cos(th) * np.sin(th) + d * np.sin(th) ** 2))
ok(abs(r.max() - 3) < 1e-9 and abs(r.min() - 2) < 1e-9, "pond p4: farthest 3 m, nearest 2 m by a scan of the curve")
k = int(np.argmax(r))
ok(abs(math.cos(th[k]) * (-1) - math.sin(th[k]) * 7) < 1e-5, "pond p4: farthest point lies along (7, -1)")
w = P[3]["widget"]
ok(w["answer"] == 3 and w["tol"]["abs"] == 0, "pond p4: key 3")
W = wrongs(P[3])
ok(W["short"]["value"] == short_ and W["no-root"]["value"] == sp.Rational(c, 40) and W["full-axis"]["value"] == 2 * long_, "pond p4: slips 2, 9, 6")
# part 5
area = math.pi * 3 * 2
ok(abs(area - c * math.pi / math.sqrt(3600)) < 1e-12, "pond p5: 6 pi equals 360 pi / sqrt(det)")
area_num = 0.5 * np.sum(((r[:-1] + r[1:]) / 2) ** 2 * np.diff(th))  # polar area, route 2
ok(abs(area_num - area) < 1e-6, "pond p5: polar integral of the curve")
w = P[4]["widget"]
ok(w["answer"] == round(area, 2) == 18.85 and abs(area - w["answer"]) <= w["tol"]["abs"], "pond p5: key 18.85 and band")
W = wrongs(P[4])
for wid, val in (("no-root", math.pi * 9 * 4), ("full-axes", math.pi * 6 * 4), ("one-axis", math.pi * 9)):
    e = W[wid]
    ok(abs(val - e["value"]) <= e["tol"]["abs"], f"pond p5: {wid} {e['value']} against {val:.4f}")
    ok(abs(round(val, 2) - e["value"]) <= e["tol"]["abs"], f"pond p5: {wid} takes its own 2 dp rounding {round(val, 2)}")
    ok(abs(e["value"] - w["answer"]) > e["tol"]["abs"] + w["tol"]["abs"], f"pond p5: {wid} band clear of the key")
ok(len(W) == 3, "pond p5: three wrongs checked")
# printed numbers in the pond's strings, each tied to a value above
txt = json.dumps(pond)
for s in ("130", "3600", "3649 - 49", "(1, 7)", "6\\\\pi = 18.85", "360\\\\pi/60", "\\\\sqrt{360/90} = 2", "\\\\sqrt{360/40} = 3", "40t^2 = 360", "7 + 7b = 0", "\\\\pi \\\\times 9 \\\\times 4", "\\\\pi \\\\times 3^2"):
    ok(s in txt, f"pond: printed string {s}")

# ---------------------------------------------------- every matrix of the eigen course
NUMCELL = re.compile(r"^-?\d+(?:\.\d+)?$")


def cell(s):
    s = s.strip().replace("−", "-").replace("\\,", "").replace("\\phantom{-}", "").replace("\\;", "")
    s = re.sub(r"\\(?:mathbf|text|mathrm)\{([^}]*)\}", r"\1", s)
    m = re.match(r"^(-?)\\[dt]?frac\{(-?\d+)\}\{(\d+)\}$", s)
    if m:
        return (-1 if m.group(1) else 1) * int(m.group(2)) / int(m.group(3))
    m = re.match(r"^(-?\d+)/(\d+)$", s)
    if m:
        return int(m.group(1)) / int(m.group(2))
    m = re.match(r"^(-?)\\sqrt\{?(\d+)\}?$", s)
    if m:
        return (-1 if m.group(1) else 1) * math.sqrt(int(m.group(2)))
    if NUMCELL.match(s):
        return float(s)
    return None


def from_text(s):
    out = []
    for m in re.finditer(r"\\begin\{([pbvB]?matrix)\}(.*?)\\end\{\1\}", s, re.S):
        rows = [r for r in re.split(r"\\\\", m.group(2)) if r.strip()]
        M = [[cell(c_) for c_ in r.split("&")] for r in rows]
        out.append(M)
    for m in re.finditer(r"\[\s*((?:\[[^\[\]]*\]\s*,?\s*)+)\]", s):
        rows = re.findall(r"\[([^\[\]]*)\]", m.group(1))
        out.append([[cell(c_) for c_ in r.split(",")] for r in rows])
    # quadratic forms a x^2 + b xy + c y^2 (any two letters)
    for m in re.finditer(r"(-?\d*\.?\d*)\s*([a-z])\^2\s*([-+])\s*(\d*\.?\d*)\s*\2([a-z])\s*([-+])\s*(\d*\.?\d*)\s*\5\^2", s.replace("−", "-")):
        co = lambda t: 1.0 if t in ("", "+") else (-1.0 if t == "-" else float(t))
        aa = co(m.group(1)); bb = co(m.group(4)) * (1 if m.group(3) == "+" else -1); dd = co(m.group(7)) * (1 if m.group(6) == "+" else -1)
        out.append([[aa, bb / 2], [bb / 2, dd]])
    return out


def from_json(o):
    out = []
    if isinstance(o, list):
        if o and all(isinstance(r, list) and r and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in r) for r in o):
            out.append([[float(v) for v in r] for r in o])
        for v in o:
            out += from_json(v)
    elif isinstance(o, dict):
        for v in o.values():
            out += from_json(v)
    elif isinstance(o, str):
        out += from_text(o)
    return out


def square(M):
    n = len(M)
    return n >= 2 and all(len(r) == n for r in M) and all(v is not None for r in M for v in r)


TARGET = [np.array([7.0, -1.0]), np.array([1.0, 7.0])]
An = np.array([[41.0, 7.0], [7.0, 89.0]])
files = sorted(glob.glob(os.path.join(CO, "eigen", "*.json")))
n2 = n3 = 0
distinct = set()
share_one, share_pair, multiples = [], [], []
for f in files:
    dj = json.load(open(f))
    if os.path.basename(f) == "problems-2.json":
        dj["items"] = [i for i in dj["items"] if i["id"] != "p-oval-pond"]
    for M in from_json(dj):
        if not square(M):
            continue
        M = np.array(M, float)
        if M.shape != (2, 2):
            n3 += 1
            continue
        n2 += 1
        distinct.add(tuple(np.round(M.flatten(), 9)))
        hits = 0
        if not np.allclose(M, M[0, 0] * np.eye(2)):  # a multiple of I has every vector as eigenvector
            for t in TARGET:
                img = M @ t
                if abs(img[0] * t[1] - img[1] * t[0]) < 1e-9 * max(1.0, np.abs(M).max()):
                    hits += 1
        name = os.path.basename(f)
        if hits == 1:
            share_one.append((name, M.tolist()))
        if hits == 2:
            share_pair.append((name, M.tolist()))
        for T in (M, M.T):
            nz = np.abs(An) > 0
            ratio = T[nz] / An[nz]
            if np.allclose(ratio, ratio[0]) and abs(ratio[0]) > 1e-12 and np.allclose(T, ratio[0] * An):
                multiples.append((name, M.tolist()))
print(f"eigen course: {len(files)} files, {n2} two-by-two matrices read ({len(distinct)} distinct), {n3} larger square matrices")
ok(len(files) > 20 and len(distinct) >= 100, "eigen: the parse found the course's matrices")
ok(not share_pair, f"eigen: a matrix outside the item shares the pair (7, -1), (1, 7): {share_pair[:3]}")
ok(not multiples, f"eigen: a scalar multiple or transpose of A outside the item: {multiples[:3]}")
for nm, M in share_one:
    print("NOTE shares one of the two directions:", nm, M)
ok(not share_one, "eigen: no matrix outside the item has (7, -1) or (1, 7) as an eigenvector")
# the parser sees the pond's own matrices (a self-test of the parse)
own = [np.array(M, float) for M in from_json(pond) if square(M)]
ok(any(np.allclose(M, An) for M in own) and any(np.allclose(M, [[1, 7], [7, 49]]) for M in own), "eigen: parser finds A and A - 40I inside the item")
ok(any(np.allclose(np.array(M, float), An) for M in from_text(pond["prose"]) if square(M)), "eigen: parser reads the quadratic form of the prose as A")

# ---------------------------------------------------- the pond's numbers against each unit of the course
NUMS = re.compile(r"(?<![\w.^])\d[\d,]*\.?\d*")


def numset(o):
    out = set()
    for m in NUMS.findall(json.dumps(o)):
        try:
            out.add(float(m.replace(",", "").rstrip(".")))
        except ValueError:
            pass
    return out


def worst_overlap(N):
    rows = []
    for f in files:
        dj = json.load(open(f))
        for i, u in enumerate(dj.get("items") or (dj.get("screens", []) + dj.get("quiz", []))):
            if u.get("id") == "p-oval-pond":
                continue
            rows.append((len(N & numset(u)), os.path.basename(f), u.get("id", i), sorted(N & numset(u))))
    return max(rows)


# the form's own numbers of 10 or more: entries, cross term, eigenvalues, trace, determinant and its parts, constant
N_now = {41.0, 89.0, 14.0, 40.0, 90.0, 130.0, 3600.0, 3649.0, 49.0, 360.0}
w_now = worst_overlap(N_now)
print("pond: most numbers shared with one unit of the course:", w_now)
ok(w_now[0] <= 2, f"pond: shares {w_now[0]} of its form's numbers with {w_now[1]} {w_now[2]}: {w_now[3]}  [review finding 8; fails until re-keyed]")
# the reader's proposal: 53x^2 + 16xy + 116y^2 = 468
B = sp.Matrix([[53, 8], [8, 116]])
ok(sorted(B.eigenvals()) == [52, 117] and B.trace() == 169 and B.det() == 6084 == 78**2 and 53 * 116 == 6148, "proposal: eigenvalues 52, 117; trace 169; det 6148 - 64 = 6084")
ok(B - 52 * sp.eye(2) == sp.Matrix([[1, 8], [8, 64]]) and B * sp.Matrix([8, -1]) == 52 * sp.Matrix([8, -1]) and B * sp.Matrix([1, 8]) == 117 * sp.Matrix([1, 8]), "proposal: (8, -1) for 52, (1, 8) for 117")
ok(sp.sqrt(sp.Rational(468, 52)) == 3 and sp.sqrt(sp.Rational(468, 117)) == 2 and abs(468 * math.pi / 78 - 6 * math.pi) < 1e-12, "proposal: half-axes 3 and 2, area 6 pi = 468 pi / 78")
Bn = np.array(B, float)
clash = []
for f in files:
    dj = json.load(open(f))
    if os.path.basename(f) == "problems-2.json":
        dj["items"] = [i for i in dj["items"] if i["id"] != "p-oval-pond"]
    for M in from_json(dj):
        if square(M) and len(M) == 2:
            M = np.array(M, float)
            if np.allclose(M, M[0, 0] * np.eye(2)):
                continue
            for t in (np.array([8.0, -1.0]), np.array([1.0, 8.0])):
                img = M @ t
                if abs(img[0] * t[1] - img[1] * t[0]) < 1e-9 * max(1.0, np.abs(M).max()):
                    clash.append((os.path.basename(f), M.tolist()))
ok(not clash, f"proposal: no course matrix has (8, -1) or (1, 8) as an eigenvector: {clash[:2]}")
w_new = worst_overlap({53.0, 116.0, 16.0, 52.0, 117.0, 169.0, 6084.0, 6148.0, 64.0, 468.0})
print("proposal (not applied; the pond stays as keyed): most numbers shared with one unit of the course:", w_new)
# finding 8 resolved by re-keying p-crab-sizes instead (fix pass): the pond shares no key number with the new crab problem
_crab = load_item("eigen/problems-3.json", "p-crab-sizes")
ok(sp.Matrix([[1076, 168], [168, 549]]).eigenvals() == {1125: 1, 500: 1} and "1076 & 168" in _crab["parts"][1]["question"], "crab: new covariance matrix, eigenvalues 1125 and 500")
_cn = numset(_crab)
_pn = {41.0, 89.0, 14.0, 40.0, 90.0, 130.0, 3600.0, 3649.0, 49.0, 360.0}
ok(not (_cn & _pn), f"pond and new crab share no key number: {sorted(_cn & _pn)}")
ok(not any(abs(x - y) < 1e-9 for x in (1076.0, 168.0, 549.0, 1125.0, 500.0) for y in _pn), "pond: no crab matrix entry or eigenvalue among the pond's numbers")

# ===================================================================== crate
crate = load_item("quadratics/problems-4.json", "p-storage-crate")
Q = crate["parts"]
X = sp.Symbol("x")
T_ = standard_transformations + (implicit_multiplication_application, convert_xor)
px = lambda s: parse_expr(s, transformations=T_, local_dict={"x": X})
V = X**3 + 6 * X**2 + 3 * X - 10  # typed from the prose
ok("V(x) = x^3 + 6x^2 + 3x - 10" in crate["prose"], "crate: prose cubic as typed")
Vn = lambda t: t**3 + 6 * t**2 + 3 * t - 10  # route 2: plain arithmetic
# part 1
ok(V.subs(X, -2) == 0 == Vn(-2) == Q[0]["widget"]["answer"], "crate p1: V(-2) = 0")
ok((-8, 24, -6) == ((-2) ** 3, 6 * (-2) ** 2, 3 * (-2)), "crate p1: printed terms -8 + 24 - 6")
W = wrongs(Q[0])
ok(W["sign"]["value"] == Vn(2) == 28, "crate p1: sign slip V(2) = 28")
ok(W["cube-sign"]["value"] == 8 + 24 - 6 - 10 == 16, "crate p1: cube-sign slip 16")
# part 2
quo, rem = sp.div(V, X + 2, X)
ok(rem == 0 and sp.expand(quo - px(Q[1]["widget"]["answer"])) == 0 and quo == X**2 + 4 * X - 5, "crate p2: quotient x^2 + 4x - 5")
ok(all(sp.expand(px(s) - quo) == 0 for s in Q[1]["widget"]["accept"]), "crate p2: accept forms equal the key")
# route 2: synthetic division by hand
co, out = [1, 6, 3, -10], []
acc = 0
for cf in co:
    acc = cf + acc * (-2)
    out.append(acc)
ok(out == [1, 4, -5, 0], "crate p2: synthetic division 1, 4, -5 remainder 0")
W = wrongs(Q[1])
q2, r2 = sp.div(V, X - 2, X)
ok(sp.expand(px(W["sign"]["tex"]) - q2) == 0 and r2 == 28, "crate p2: sign slip is division by (x - 2), quotient x^2 + 8x + 19")
ok(sp.expand(px(W["constant-sign"]["tex"]) - (X**2 + 4 * X + 5)) == 0, "crate p2: constant-sign slip")
ok(all(sp.expand(px(e["tex"]) - quo) != 0 for e in W.values()), "crate p2: no wrong equals the key")
ok(sp.expand(X**2 * (X + 2)) == X**3 + 2 * X**2 and sp.expand(V - X**2 * (X + 2)) == 4 * X**2 + 3 * X - 10 and sp.expand(4 * X**2 + 3 * X - 10 - 4 * X * (X + 2)) == -5 * X - 10, "crate p2: the explain's division steps")
# part 3
fac = sp.factor(V)
ok(sp.expand(px(Q[2]["widget"]["answer"]) - V) == 0 and fac == (X - 1) * (X + 2) * (X + 5), "crate p3: (x + 2)(x + 5)(x - 1)")
ok(sorted(sp.roots(V).keys()) == [-5, -2, 1] and all(abs(Vn(t)) == 0 for t in (-5, -2, 1)), "crate p3: roots -5, -2, 1 two ways")
ok(all(sp.expand(px(s) - V) == 0 for s in Q[2]["widget"]["accept"]), "crate p3: accept forms equal V")
W = wrongs(Q[2])
ok(sp.expand(px(W["signs"]["tex"]) - (X + 2) * (X - 5) * (X + 1)) == 0 and sp.expand((X - 5) * (X + 1)) == X**2 - 4 * X - 5, "crate p3: signs slip and its printed expansion")
ok(sp.expand(px(W["one-root-sign"]["tex"]) - (X + 2) * (X + 5) * (X + 1)) == 0 and Vn(-1) != 0 and Vn(1) == 0, "crate p3: one-root-sign; V(-1) is not 0, V(1) is")
ok(all(sp.expand(px(e["tex"]) - V) != 0 for e in W.values()), "crate p3: no wrong equals the key")
# part 4
base = X**2 + 7 * X + 10
ok("x^2 + 7x + 10" in Q[3]["question"] and sp.factor(base) == (X + 2) * (X + 5), "crate p4: base (x + 2)(x + 5)")
h = sp.cancel(V / base)
ok(h == X - 1 == px(Q[3]["widget"]["answer"]) and all(sp.expand(px(s) - h) == 0 for s in Q[3]["widget"]["accept"]), "crate p4: height x - 1")
W = wrongs(Q[3])
ok(px(W["wrong-pair"]["tex"]) == X + 2 and px(W["sign"]["tex"]) == X + 1, "crate p4: slips x + 2 and x + 1")
ok(all(Vn(t) > 0 and t * t + 7 * t + 10 > 0 and t - 1 > 0 for t in (1.001, 2, 3.5, 50)), "crate p4: x > 1 keeps volume, base and height positive")
# part 5
xs = sp.solve(sp.Eq(h, sp.Rational(5, 2)), X)
vol = V.subs(X, xs[0])
ok(xs == [sp.Rational(7, 2)] and vol == sp.Rational(935, 8) and Vn(3.5) == 116.875 == 5.5 * 8.5 * 2.5, "crate p5: x = 3.5 and volume 116.875 three ways")
w = Q[4]["widget"]
ok(w["answer"] == 116.875 and abs(float(vol) - w["answer"]) <= w["tol"]["abs"], "crate p5: key and band")
W = wrongs(Q[4])
ok(W["x-is-height"]["value"] == Vn(2.5) == 4.5 * 7.5 * 1.5 == 50.625, "crate p5: x-is-height 50.625")
ok(W["base-only"]["value"] == 5.5 * 8.5 == 46.75, "crate p5: base-only 46.75")
for e in W.values():
    ok(abs(e["value"] - w["answer"]) > e["tol"]["abs"] + w["tol"]["abs"], f"crate p5: {e['id']} band clear of the key")
ok(len(W) == 2, "crate p5: two wrongs checked")

# ---------------------------------------------------- cubics of the quadratics course
def pattern(poly):
    """Root pattern up to x -> a x + b: sorted gap ratios of real roots, both directions."""
    rts = sp.roots(sp.Poly(poly, X))
    if sum(rts.values()) != 3 or not all(r.is_real for r in rts):
        return None
    r = sorted(float(v) for v, m in rts.items() for _ in range(m))
    g1, g2 = r[1] - r[0], r[2] - r[1]
    if g1 == 0 and g2 == 0:
        return (0.0, 0.0)
    return tuple(sorted((round(g1 / (g1 + g2), 9), round(g2 / (g1 + g2), 9))))


mine = pattern(V)
ok(mine == (0.5, 0.5), "crate: roots -5, -2, 1 are equally spaced")
CUB = re.compile(r"(?<![\w^])(\d*[a-z]\^3(?:\s*[-+]\s*\d*(?:[a-z](?:\^2)?)?)*)")
FACT = re.compile(r"((?:\d*[a-z])?(?:\([a-z]\s*[-+]\s*\d+\)(?:\^2)?){2,3})")
seen, same = set(), []
for f in sorted(glob.glob(os.path.join(CO, "quadratics", "*.json"))):
    dj = json.load(open(f))
    if os.path.basename(f) == "problems-4.json":
        dj["items"] = [i for i in dj["items"] if i["id"] != "p-storage-crate"]

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                yield from walk(v)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v)
        elif isinstance(o, str):
            yield o

    for s in walk(dj):
        s = s.replace("−", "-")
        for m in CUB.findall(s) + FACT.findall(s):
            letters = set(re.findall(r"[a-z]", m))
            if len(letters) != 1:
                continue
            try:
                e = parse_expr(m.replace(letters.pop(), "x"), transformations=T_, local_dict={"x": X})
                if sp.degree(sp.expand(e), X) != 3:
                    continue
            except Exception:
                continue
            e = sp.expand(e)
            seen.add(e)
            if pattern(e) == mine:
                same.append((os.path.basename(f), str(e)))
print(f"quadratics course: {len(seen)} distinct cubics read outside the item")
ok(len(seen) >= 8, "quadratics: the parse found the course's cubics")
ok(not same, f"quadratics: a cubic with the crate's root pattern (shift, scale or mirror): {same[:4]}")
ok(sp.expand((X + 1) * (X - 2) * (X - 3)) in seen, "quadratics: parser finds review-4's cubic (self-test)")

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
