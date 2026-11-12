"""Delta read AC-1, finding c1: search for a replacement covariance matrix for p-river-gauges whose leading corner is
in no content file, and print every key and slip of the five parts for it, each by two routes.

    <venv>/bin/python docs/reviews/review-delta-problems-ac-1-scripts/proposed.py            (the proposed matrix)
    <venv>/bin/python docs/reviews/review-delta-problems-ac-1-scripts/proposed.py --search   (list candidates)
Run from the repo root. Exit 0 when the two routes agree on the proposed matrix and its corner and rows are unused."""
import glob
import itertools
import json
import re
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp


def strings_of(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings_of(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings_of(v)


TEXT = {f: re.sub(r"\s+", "", " | ".join(strings_of(json.load(open(f, encoding="utf-8")))))
        for f in glob.glob("app/content/**/*.json", recursive=True)}


def used(a, b, d, f=None, e=None):
    """Files that print the corner (a b; b d) as a 2 by 2 matrix or as the corner of a larger one, or rows of K."""
    pats = [rf"{a}&{b}(&[^\\&]*)*\\\\{b}&{d}(?![\d.])", rf"\[\[{a},{b}(,[^\]]*)?\],\[{b},{d}[,\]]"]
    if f is not None:
        pats += [rf"(?<![\d.&]){a}&{b}&{f}(?![\d.])", rf"(?<![\d.&]){b}&{d}&{e}(?![\d.])"]
    return sorted({p for p, t in TEXT.items() for x in pats if re.search(x, t)})


def dec(x, places=4):
    """True when x is a decimal of at most `places` places."""
    return (F(x) * 10 ** places).denominator == 1


def build(a, b, d, f, e, cplan):
    a, b, d, f, e, cplan = map(F, (a, b, d, f, e, cplan))
    m21 = b / a
    p2 = d - m21 * b
    r2 = e - m21 * f                       # row 2 after step 1: (0, p2, r2)
    if p2 <= 0:
        return None
    m31 = f / a
    s1 = m31 * f                           # taken off c by step 1
    m32 = r2 / p2
    s2 = m32 * r2
    dd = s1 + s2
    bb = -r2 / p2
    aa = -(b * bb + f) / a
    out = dict(m21=m21, p2=p2, mult_one=d - b, mult_two=d - b * b, r2=r2, m31=m31, s1=s1, m32=m32, s2=s2, d=dd,
               big=s1 + r2 * r2, added=s1 - s2, w=(aa, bb, F(1)), no_b=(-f / a, bb, F(1)), var=cplan - dd,
               share=dd / cplan, unexplained=(cplan - dd) / cplan, not_scaled=1 - (cplan - dd))
    ws = (-aa, -bb, F(1))
    K = [[a, b, f], [b, d, e], [f, e, cplan]]
    out["sign_var"] = sum(ws[i] * K[i][j] * ws[j] for i in range(3) for j in range(3))
    return out


def good(o, cplan):
    vals = [o["p2"], o["mult_one"], o["mult_two"]]
    ds = [o["d"], o["s1"], o["big"], o["added"]]
    vs = [o["var"], F(cplan), o["sign_var"], o["d"]]
    sh = [o["share"], o["unexplained"], o["not_scaled"]]
    flat = [o["m21"], o["r2"], o["m31"], o["m32"], o["s2"], *vals, *ds, *o["w"], *o["no_b"], *vs, *sh]
    return (all(dec(x, 3) for x in flat) and len(set(vals)) == 3 and len(set(ds)) == 4 and len(set(vs)) == 4
            and len(set(sh)) == 3 and o["p2"] > 0 and o["var"] > 0 and o["added"] > 0 and o["m21"] != 1 and o["m32"] not in (0, 1)
            and o["w"][0] != o["w"][1] and o["no_b"][0] != o["w"][0] and o["p2"].denominator == 1
            and o["share"] not in (F(3, 4),) and 0 < o["not_scaled"] < 1)


if "--search" in sys.argv:
    n = 0
    for a, b, d, f, e in itertools.product((4, 5, 8, 10), (1, 2, 3, 4), range(2, 9), (1, 2, 3, 4), (1, 2, 3, 4)):
        for cplan in (F(1), F(2), F(5, 2), F(4), F(5), F(8), F(10)):
            o = build(a, b, d, f, e, cplan)
            if o and good(o, cplan) and not used(a, b, d, f, e):
                n += 1
                print(a, b, d, f, e, "c =", float(cplan), "| p2", o["p2"], "d", float(o["d"]), "w", [float(x) for x in o["w"]], "var", float(o["var"]), "share", float(o["share"]))
    print(n, "candidates")
    sys.exit(0)

# ---------------------------------------------------------------- the proposed matrix
A_, B_, D_, F_, E_, CP = 8, 4, 7, 4, 3, F(5, 2)
o = build(A_, B_, D_, F_, E_, CP)
fails = 0


def ok(cond, msg):
    global fails
    if not cond:
        fails += 1
        print("FAIL", msg)


c = sp.symbols("c")
K = sp.Matrix([[A_, B_, F_], [B_, D_, E_], [F_, E_, c]])
ok(not used(A_, B_, D_, F_, E_), f"corner or rows already in content: {used(A_, B_, D_, F_, E_)}")
ok(good(o, CP), "the proposed matrix passes the slip and decimal conditions")
# route 2 for each number
ok(K[:2, :2].det() / A_ == o["p2"], "second pivot by the corner determinant")
third = sp.simplify(K.det() / K[:2, :2].det())
ok(sp.simplify(third - (c - sp.Rational(o["d"].numerator, o["d"].denominator))) == 0, "third pivot by det K over the corner")
K0 = K.subs(c, sp.Rational(o["d"].numerator, o["d"].denominator))
ns = K0.nullspace()[0]; ns = ns / ns[2]
ok([F(int(x.p), int(x.q)) for x in ns] == list(o["w"]), "null vector by sympy")
vt = np.linalg.svd(np.array(K0, float))[2][-1]
ok(np.allclose(vt / vt[2], [float(x) for x in o["w"]]), "null vector by SVD")
Kn = np.array(K.subs(c, sp.Rational(CP.numerator, CP.denominator)), float)
wn = np.array([float(x) for x in o["w"]])
ok(abs(wn @ Kn @ wn - float(o["var"])) < 1e-12, "variance of the mix by NumPy")
beta = np.linalg.solve(Kn[:2, :2], Kn[:2, 2])
ok(np.allclose(-beta, wn[:2]) and abs(1 - (Kn[2, 2] - Kn[:2, 2] @ beta) / Kn[2, 2] - float(o["share"])) < 1e-12, "share by the regression of C on A and B")
for cv in (float(o["d"]) - 0.05, float(o["d"]) + 0.05):
    ok((np.linalg.eigvalsh(np.array(K.subs(c, cv), float)).min() > 0) == (cv > float(o["d"])), f"positive definite only above d (c = {cv})")
print("K rows:", (A_, B_, F_), (B_, D_, E_), (F_, E_, "c"), " planned c =", float(CP), " det K =", sp.expand(K.det()))
for k_, v in o.items():
    print(f"  {k_:12s}", [str(x) for x in v] if isinstance(v, tuple) else f"{v} = {float(v)}")
print("Kw at the planned c:", list(sp.Matrix(Kn) * sp.Matrix(wn)))
print("proposed:", "0 failures" if not fails else f"{fails} failures")
sys.exit(1 if fails else 0)
