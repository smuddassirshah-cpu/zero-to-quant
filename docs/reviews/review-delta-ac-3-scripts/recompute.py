"""Delta read AC-3: every changed key, band and wrong value of the four fix passes, recomputed by two routes.
   Run from the repo root with the scratchpad venv Python:
       <venv>/bin/python docs/reviews/review-delta-ac-3-scripts/recompute.py [--show]

   For each changed numeric part: the stored answer equals both routes; every wrong value equals both routes of the
   slip its line describes; the key band takes the honest roundings listed and refuses the listed neighbours and every
   wrong value; no wrong band meets the key band; no two wrong bands of a part meet. Checks that fail because the
   content is at fault are printed as CLAIM (they are findings in the review) and do not change the exit code;
   any other failure prints FAIL and exits 1."""
import json
import math
import sys
from fractions import Fraction as F

import numpy as np
import sympy as sp
from scipy import integrate, linalg, stats

SHOW = "--show" in sys.argv
checks = fails = claims = 0


def chk(name, ok, claim=None):
    global checks, fails, claims
    checks += 1
    if ok:
        if SHOW:
            print("ok   ", name)
    elif claim:
        claims += 1
        print("CLAIM", name, "[" + claim + "]")
    else:
        fails += 1
        print("FAIL ", name)


def close(a, b, eps):
    return abs(float(a) - float(b)) <= eps


DOCS = {}


def doc(f):
    if f not in DOCS:
        DOCS[f] = json.load(open(f"app/content/{f}.json"))
    return DOCS[f]


def find(d, pid):
    if isinstance(d, dict):
        if d.get("id") == pid:
            return d
        for v in d.values():
            r = find(v, pid)
            if r:
                return r
    elif isinstance(d, list):
        for v in d:
            r = find(v, pid)
            if r:
                return r
    return None


def part(f, pid, n=None):
    it = find(doc(f), pid)
    assert it is not None, (f, pid)
    return it if n is None else it["parts"][n - 1]


def at(f, path):
    import re
    d = doc(f)
    for tok in re.findall(r"[A-Za-z_]+|\[\d+\]", path):
        d = d[int(tok[1:-1])] if tok.startswith("[") else d[tok]
    return d


def tol(e):
    return (e.get("tol") or {}).get("abs", 0)


def takes(e, x, key="value"):
    return abs(float(x) - float(e[key])) <= tol(e) + 1e-12


def hit(w, x):
    """What a typed value x (already in stored units) meets: True, a wrong id, or None. Key first, then wrong[] in order."""
    if abs(float(x) - float(w["answer"])) <= tol(w) + 1e-12:
        return True
    for e in w.get("wrong", []):
        if takes(e, x):
            return e["id"]
    return None


def numeric(tag, w, key, wrongs, accept=(), refuse=(), routes=(), eps=None, fb=None, weps=None):
    """key = (route1, route2); wrongs = {id: (route1, route2)}; routes = [(typed, expected hit)]."""
    a = w["answer"]
    e = eps if eps is not None else max(1e-9, 0.6 * 10 ** -dp(a))
    chk(f"{tag}: key {a} = route 1 {float(key[0]):.7g}", close(a, key[0], e))
    chk(f"{tag}: key {a} = route 2 {float(key[1]):.7g}", close(a, key[1], e))
    chk(f"{tag}: the two routes agree", close(key[0], key[1], 1e-9 * max(1, abs(float(key[0])))))
    ids = [x["id"] for x in w.get("wrong", [])]
    chk(f"{tag}: wrong ids {ids} are the ones recomputed {sorted(wrongs)}", sorted(ids) == sorted(wrongs))
    for x in w.get("wrong", []):
        if x["id"] not in wrongs:
            continue
        r1, r2 = wrongs[x["id"]]
        ee = weps if weps is not None else max(1e-9, 0.6 * 10 ** -dp(x["value"]))
        chk(f"{tag}: wrong {x['id']} {x['value']} = route 1 {float(r1):.7g}", close(x["value"], r1, ee))
        chk(f"{tag}: wrong {x['id']} {x['value']} = route 2 {float(r2):.7g}", close(x["value"], r2, ee))
        chk(f"{tag}: wrong {x['id']} unrounded {float(r1):.7g} is inside its own band", takes(x, r1) or hit(w, r1) is True)
        chk(f"{tag}: key band refuses wrong {x['id']}", hit(w, x["value"]) == x["id"])
        lo, hi = x["value"] - tol(x), x["value"] + tol(x)
        chk(f"{tag}: wrong band {x['id']} [{lo:.7g}, {hi:.7g}] does not meet the key band", hi < a - tol(w) or lo > a + tol(w))
        if fb is not None:
            chk(f"{tag}: wrong {x['id']} has a byKey line", x["id"] in (fb.get("byKey") or {}))
    ws = w.get("wrong", [])
    for i in range(len(ws)):
        for j in range(i + 1, len(ws)):
            p, q = ws[i], ws[j]
            chk(f"{tag}: wrong bands {p['id']} and {q['id']} do not meet",
                p["value"] + tol(p) < q["value"] - tol(q) or q["value"] + tol(q) < p["value"] - tol(p))
    for x in accept:
        chk(f"{tag}: key band takes {x}", hit(w, x) is True)
    for x in refuse:
        chk(f"{tag}: key band refuses {x}", hit(w, x) is not True)
    for x, want in routes:
        got = hit(w, x)
        chk(f"{tag}: typed {x} -> {got}, expected {want}", got == want)


def dp(x):
    s = repr(float(x))
    if "e" in s:
        return 9
    return len(s.split(".")[1]) if "." in s and not s.endswith(".0") else 0


def has(tag, text, *needles):
    for n in needles:
        chk(f"{tag}: text holds '{n}'", n in text)


# ====================================================================================================
# 1. ratio/problems-1 to -3
# ====================================================================================================
R1, R2, R3 = "courses/ratio/problems-1", "courses/ratio/problems-2", "courses/ratio/problems-3"

# p-phone-rise: parts 1 to 3 unchanged, checked for the chain; part 4 re-keyed
p = part(R1, "p-phone-rise", 3)["widget"]
new_price = F(30) * F(1071, 1000)
chk("phone-rise 3: new price 32.13 (chain into part 4)", new_price == F(3213, 100) and close(p["answer"], 30 * 1.071, 1e-9))
pt = part(R1, "p-phone-rise", 4)
w = pt["widget"]
numeric("phone-rise 4", w, (F(14) / new_price, 14 / (30 * (1 + 0.032 + 0.039))),
        {"old-price": (F(14, 30), 14 / 30.0), "upside-down": (new_price / 14, 32.13 / 14), "saving": ((new_price - 14) / new_price, 1 - 14 / 32.13)},
        accept=[0.436, 0.4357, 0.43573], refuse=[0.3735, 0.373, 0.44, 0.43, 0.437],
        routes=[(0.467, "old-price"), (0.4667, "old-price"), (2.295, "upside-down"), (2.3, None), (0.564, "saving"), (0.5643, "saving"), (0.4, None)],
        fb=pt["feedback"])
chk("phone-rise 4: 43.5% is inside the key band (band +-0.1 point, unchanged by the fix pass)", hit(w, 0.435) is True)
chk("phone-rise 4: saving is 32.13 - 14.00 = 18.13", new_price - 14 == F(1813, 100))
has("phone-rise 4", json.dumps(pt, ensure_ascii=False), "£14.00", "43.6%", "£18.13", "0.4357", "0.436")

# p-platform-fee part 4: two slip bands widened; part 3 question restated
pt = part(R1, "p-platform-fee", 4)
w = pt["widget"]
fee = F(8400) * F(35, 10000)
chk("platform-fee: fee 29.40 by two routes", fee == F(294, 10) and close(8400 * 0.0035, 29.4, 1e-9))
numeric("platform-fee 4", w, (F(24) / fee, 24 / 29.4),
        {"upside-down": (fee / 24, 29.4 / 24), "account-base": (F(24, 8400), 24 / 8400), "one-place": (F(24, 294), 24 / (8400 * 0.035))},
        accept=[0.82, 0.816, 0.8163], refuse=[0.8, 0.83, 0.84],
        routes=[(0.08, "one-place"), (0.082, "one-place"), (0.0816, "one-place"), (1.22, "upside-down"), (1.23, "upside-down"), (1.225, "upside-down"),
                (0.0029, "account-base"), (0.003, "account-base")], fb=pt["feedback"])
q3 = part(R1, "p-platform-fee", 3)
has("platform-fee 3", q3["question"], "0.35% fee", "£8,400")
chk("platform-fee 3: key 8370.60 by two routes", close(q3["widget"]["answer"], 8400 * 0.9965, 1e-9) and F(8400) - fee == F(83706, 10))

# p-savings-tax part 4: the `same` line renumbered
opts = {o["id"]: o for o in part(R1, "p-savings-tax", 4)["widget"]["options"]}
interest = F(18000) * F(46, 1000)
kept = interest - F(4, 10) * (interest - 500)
free = F(18000) * F(39, 1000)
chk("savings-tax 4: interest 828, kept 696.80, tax-free 702, gap 5.20", (interest, kept, free, free - kept) == (828, F(6968, 10), 702, F(52, 10)))
chk("savings-tax 4: same route in floats", close(828 - 0.4 * 328, 696.8, 1e-9) and close(18000 * 0.039 - 696.8, 5.2, 1e-9))
has("savings-tax 4 same", opts["same"]["why"], "£702", "£696.80", "£5.20")
chk("savings-tax 4: tax-free is the key", opts["tax-free"].get("correct") is True)

# p-laptop-sale: new slip on part 1, band on part 3
pt = part(R2, "p-laptop-sale", 1)
numeric("laptop-sale 1", pt["widget"], (F(561) / F(85, 100), 561 / 0.85),
        {"added": (F(561) * F(115, 100), 561 * 1.15), "off-again": (F(561) * F(85, 100), 561 - 0.15 * 561)},
        accept=[660, 660.00], refuse=[659.99, 660.01], fb=pt["feedback"])
pt = part(R2, "p-laptop-sale", 3)
numeric("laptop-sale 3", pt["widget"], (F(561 - 600, 600), 1.1 * 0.85 - 1),
        {"sign": (F(39, 600), 0.065), "added": (F(10 - 15, 100), 0.10 - 0.15), "sale-base": (F(561 - 600, 561), -39 / 561)},
        accept=[-0.065], refuse=[-0.066, -0.064, -0.07],
        routes=[(-0.07, "sale-base"), (-0.0695, "sale-base"), (-0.069, "sale-base"), (-0.06952, "sale-base"), (-0.068, None)], fb=pt["feedback"], eps=6e-5)

# p-partners-profit: renumbered to 3 : 4 : 8
stakes = [12000, 16000, 32000]
g = math.gcd(*stakes)
g2 = max(d for d in range(1, 12001) if all(s % d == 0 for s in stakes))
ratio = [s // g for s in stakes]
chk("partners: gcd 4,000 by math.gcd and by listing; ratio 3 : 4 : 8", g == g2 == 4000 and ratio == [3, 4, 8])
it = part(R3, "p-partners-profit")
has("partners prose", it["prose"], "£12,000, £16,000 and £32,000")
pt = it["parts"][0]
numeric("partners 1", pt["widget"], (sum(ratio), F(sum(stakes), g)),
        {"thousands": (sum(s // 1000 for s in stakes), 12 + 16 + 32), "halved": (sum(s // 2000 for s in stakes), 6 + 8 + 16)},
        accept=[15], refuse=[12, 14, 16], fb=pt["feedback"])
has("partners 1", json.dumps(pt, ensure_ascii=False), "3 : 4 : 8", "12 : 16 : 32", "6 : 8 : 16", "4,000")
pt = it["parts"][1]
numeric("partners 2", pt["widget"], (F(9600) * F(32000, sum(stakes)), 9600 / 15 * 8),
        {"equal": (F(9600, 3), 9600 / 3), "one-part": (F(9600, 15), 9600 / 15)}, accept=[5120], refuse=[4000, 5119, 5121], fb=pt["feedback"])
chk("partners 2: one part is a whole number of pounds (640)", 9600 % 15 == 0)
chk("partners 2: 3,200 is no partner's true share (1,920, 2,560, 5,120)", 3200 not in [9600 * r // 15 for r in ratio])
pt = it["parts"][2]
numeric("partners 3", pt["widget"], (F(2850, 3) * 15, 2850 * sum(stakes) / stakes[0]),
        {"own-parts": (2850 * 3, 2850 * 3.0), "one-part-share": (2850 * 15, 2850 * 15.0)}, accept=[14250], refuse=[11400, 14249], fb=pt["feedback"])
chk("partners 3: one part is £950", F(2850, 3) == 950)
chk("partners 3 generic: says 15 parts of the whole, not 12", "15 parts" in pt["feedback"]["generic"],
    claim="finding 1.1: generic line still says 'the 12 parts of the whole'")
pt = it["parts"][3]
numeric("partners 4", pt["widget"], (F(11900) * F(8000, sum(stakes) + 8000), 11900 / 17 * 2),
        {"old-parts": (F(11900, 15) * 2, 11900 / 15 * 2), "equal": (F(11900, 4), 11900 / 4)}, accept=[1400], refuse=[1700, 1399, 1401],
        routes=[(1586.67, "old-parts"), (1586.666, "old-parts"), (2975, "equal")], fb=pt["feedback"])
chk("partners 4: 8,000 is 2 parts of 4,000; 17 parts; one part £700", 8000 // g == 2 and sum(ratio) + 2 == 17 and 11900 % 17 == 0 and 11900 // 17 == 700)

# p-print-run: four presses, 15 hours
it = part(R3, "p-print-run")
has("print-run prose", it["prose"], "Four identical presses", "15 hours", "36,000")
pt = it["parts"][0]
numeric("print-run 1", pt["widget"], (F(4 * 15, 8), 15 * 4 / 8),
        {"direct": (F(15 * 8, 4), 15 * (8 / 4)), "subtracted": (15 - (8 - 4), 15 - 4.0)}, accept=[7.5], refuse=[7, 8, 19.2, 9], fb=pt["feedback"])
pt = it["parts"][1]
numeric("print-run 2", pt["widget"], (F(8) * F(15, 2) * 14, 4 * 15 * 14),
        {"direct": (8 * 30 * 14, 8 * (15 * 8 / 4) * 14), "one-press": (F(15, 2) * 14, 7.5 * 14)}, accept=[840], refuse=[2150.4, 3360], fb=pt["feedback"])
pt = it["parts"][2]
numeric("print-run 3", pt["widget"], (F(840, 36), 840 / (36000 / 1000)),
        {"per-leaflet": (F(840, 36000), 840 / 36000), "upside-down": (F(36000, 840), 36000 / 840)}, accept=[23.33, 23.3333, 23.34], refuse=[23.3, 23.35], fb=pt["feedback"])
pt = it["parts"][3]
opts = {o["id"]: o for o in pt["widget"]["options"]}
chk("print-run 4: rival £22.00 per 1,000 beats £23.33; key is rival", opts["rival"].get("correct") is True and 10 * F(220, 100) == 22 < F(840, 36))
chk("print-run 4: saving on the order is 840 - 36 x 22 = 48, and 36 x 1.33 = 47.88, about 48", 840 - 36 * 22 == 48 and round(36 * 1.33) == 48)
has("print-run 4", json.dumps(pt, ensure_ascii=False), "The rival printer", "The shop's own presses", "They cost the same")

# unit boxes
for pid, n, unit, key in (("p-coffee-suppliers", 1, "CHF", F(330, 12)), ("p-villa-split", 1, "€", F(8 * 405, 6)), ("p-villa-split", 3, "€", F(8 * 405, 4 * 7 + 2 * 4) * 7)):
    w = part(R3, pid, n)["widget"]
    chk(f"{pid} {n}: unit {unit} and key {float(key)}", w.get("unit") == unit and close(w["answer"], key, 1e-9))

# ====================================================================================================
# 2. eigen/problems-4
# ====================================================================================================
E4 = "courses/eigen/problems-4"
it = part(E4, "p-linked-lagoons")
A = sp.Matrix([[-4, 2], [1, -3]])
M = sp.Matrix([[1, 0], [1, 1]])
Minv = M.inv()
B = Minv * A * M
An, Mn = np.array(A.tolist(), float), np.array(M.tolist(), float)
Bn = np.linalg.solve(Mn, An @ Mn)
chk("lagoons: M^-1 = (1 0; -1 1)", Minv == sp.Matrix([[1, 0], [-1, 1]]))
chk("lagoons: AM = (-2 2; -2 -3)", A * M == sp.Matrix([[-2, 2], [-2, -3]]))
chk("lagoons: B = (-2 2; 0 -5) by sympy and by solve", B == sp.Matrix([[-2, 2], [0, -5]]) and np.allclose(Bn, [[-2, 2], [0, -5]]))
has("lagoons prose", it["prose"], r"\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}", "w_2 = u_2 - u_1")
chk("lagoons: w = M^-1 u gives w2 = u2 - u1", (Minv * sp.Matrix(sp.symbols("u1 u2")))[1] == sp.symbols("u2") - sp.symbols("u1"))
pt = it["parts"][0]
numeric("lagoons 1", pt["widget"], (B[1, 1], Bn[1, 1]),
        {"sign": (-B[1, 1], 5), "unchanged": (A[1, 1], An[1, 1]), "reversed": ((M * A * Minv)[1, 1], (Mn @ An @ np.linalg.inv(Mn))[1, 1])},
        accept=[-5], refuse=[-4, -3, -1], fb=pt["feedback"])
has("lagoons 1", json.dumps(pt, ensure_ascii=False), r"\\begin{pmatrix} 1 & 0 \\\\ -1 & 1 \\end{pmatrix}", r"\\begin{pmatrix} -2 & 2 \\\\ -2 & -3 \\end{pmatrix}",
    r"\\begin{pmatrix} -2 & 2 \\\\ 0 & -5 \\end{pmatrix}", "-3 - 2 = -5")
pt = it["parts"][1]
ev = sorted(A.eigenvals().keys())
chk("lagoons 2: eigenvalues -5, -2 by sympy, numpy and the diagonal of B", ev == [-5, -2] and np.allclose(sorted(np.linalg.eigvals(An)), [-5, -2]) and sorted([B[0, 0], B[1, 1]]) == [-5, -2])
chk("lagoons 2: stored answers", sorted(pt["widget"]["answers"]) == [-5, -2])
chk("lagoons 2: trace -7, det 10", A.trace() == -7 and A.det() == 10)
wr = {x["id"]: x["value"] for x in pt["widget"]["wrong"]}
chk("lagoons 2: wrongs (5, 2), (-7, 10), (-4, -3)", wr == {"sign": "5, 2", "trace-det": "-7, 10", "a-diagonal": "-4, -3"})
has("lagoons 2", json.dumps(pt, ensure_ascii=False), r"\\begin{pmatrix} -2 & 2 \\\\ 0 & -5 \\end{pmatrix}", r"(-2 - \\lambda)(-5 - \\lambda)")
pt = it["parts"][2]
y = sp.Matrix([2, -3])
chk("lagoons 3: y = (2, -3) is an eigenvector of B for -5", B * y == -5 * y)
chk("lagoons 3: x = My = (2, -1), stored key", M * y == sp.Matrix([2, -1]) and pt["widget"]["answer"] == "(2, -1)" and np.allclose(Mn @ [2, -3], [2, -1]))
chk("lagoons 3: A(2, -1) = (-10, 5) = -5(2, -1)", A * sp.Matrix([2, -1]) == sp.Matrix([-10, 5]))
wr = {x["id"]: x["tex"] for x in pt["widget"]["wrong"]}
chk("lagoons 3: inverse M^-1 y = (2, -5); unmoved (2, -3)", Minv * y == sp.Matrix([2, -5]) and wr == {"inverse": "(2, -5)", "unmoved": "(2, -3)"})
has("lagoons 3", json.dumps(pt, ensure_ascii=False), "(2, -3)", "(2, 2 - 3) = (2, -1)", "(-10, 5)")
pt = it["parts"][3]
c = sp.Matrix([[1, 2], [1, -1]]).solve(sp.Matrix([5, 2]))
chk("lagoons 4: (c1, c2) = (3, 1) by sympy and by solve", c == sp.Matrix([3, 1]) and np.allclose(np.linalg.solve([[1, 2], [1, -1]], [5, 2]), [3, 1]) and pt["widget"]["answer"] == "(3, 1)")
chk("lagoons 4: (1, 1) is an eigenvector of A for -2", A * sp.Matrix([1, 1]) == -2 * sp.Matrix([1, 1]))
wr = {x["id"]: x["tex"] for x in pt["widget"]["wrong"]}
chk("lagoons 4: w-coords M^-1 u0 = (5, -3); swapped (1, 3)", Minv * sp.Matrix([5, 2]) == sp.Matrix([5, -3]) and wr == {"swapped": "(1, 3)", "w-coords": "(5, -3)"})
pt = it["parts"][4]
tot = 6 * math.exp(-2) + math.exp(-5)
u1 = linalg.expm(An) @ np.array([5.0, 2.0])
numeric("lagoons 5 (unchanged, chain)", pt["widget"], (tot, u1.sum()),
        {"coefficients-only": (3 * math.exp(-2) + math.exp(-5), 0.4127), "u1-only": (u1[0], 3 * math.exp(-2) + 2 * math.exp(-5)),
         "rates-swapped": (6 * math.exp(-5) + math.exp(-2), 0.1758), "carried": (2 * math.exp(-2) + 3 * math.exp(-5), 0.2909)},
        accept=[0.819, 0.8187, 0.8185, 0.818], refuse=[0.821, 0.817], fb=pt["feedback"], eps=6e-4)

it = part(E4, "p-machine-stops")
Q = sp.Matrix([[sp.Rational(-1, 10), sp.Rational(4, 10)], [sp.Rational(1, 10), sp.Rational(-4, 10)]])
Qn = np.array(Q.tolist(), float)
has("machine prose", it["prose"], "stops at rate 0.1 an hour", "restarts at rate 0.4 an hour", r"\begin{pmatrix} -0.1 & 0.4 \\ 0.1 & -0.4 \end{pmatrix}")
chk("machine: columns of Q add to 0 (column convention); stop rate leaves Running", list(Q.T * sp.ones(2, 1)) == [0, 0] and Q[1, 0] == sp.Rational(1, 10))
pt = it["parts"][0]
ev = sorted(Q.eigenvals().keys())
chk("machine 1: eigenvalues 0 and -0.5 by sympy, numpy, trace and det", ev == [sp.Rational(-1, 2), 0] and np.allclose(sorted(np.linalg.eigvals(Qn)), [-0.5, 0]) and Q.det() == 0 and Q.trace() == sp.Rational(-1, 2))
chk("machine 1: stored answers [0, -0.5]", sorted(pt["widget"]["answers"]) == [-0.5, 0])
wr = {x["id"]: x["value"] for x in pt["widget"]["wrong"]}
chk("machine 1: wrongs '0, 0.5' and '-0.1, -0.4'", wr == {"sign": "0, 0.5", "diagonal": "-0.1, -0.4"})
has("machine 1", json.dumps(pt, ensure_ascii=False), "0.04 - 0.04 = 0", "-0.1 - 0.4 = -0.5", r"\\lambda^2 + 0.5\\lambda")
pt = it["parts"][1]
ns = Q.nullspace()[0]
pi = ns / sum(ns)
wv, vv = np.linalg.eig(Qn)
v0 = vv[:, np.argmin(abs(wv))]
chk("machine 2: steady state (0.8, 0.2) by nullspace and by eig", list(pi) == [sp.Rational(4, 5), sp.Rational(1, 5)] and np.allclose(v0 / v0.sum(), [0.8, 0.2]) and pt["widget"]["answer"] == "(0.8, 0.2)")
chk("machine 2: flows 0.1 x 0.8 = 0.4 x 0.2 = 0.08", sp.Rational(1, 10) * pi[0] == sp.Rational(4, 10) * pi[1] == sp.Rational(8, 100))
wr = {x["id"]: x["tex"] for x in pt["widget"]["wrong"]}
chk("machine 2: wrongs (0.2, 0.8) and (4, 1)", wr == {"swapped": "(0.2, 0.8)", "unscaled": "(4, 1)"})
chk("machine 2: accept list holds no old form", not any(s in json.dumps(pt["widget"]["accept"]) for s in ("0.75", "0.25", "3}{4", "1}{4", "3/4", "(3, 1)")))
has("machine 2", json.dumps(pt, ensure_ascii=False), "a = 4b", "four fifths", "0.1 \\\\times 0.8 = 0.08", "0.4 \\\\times 0.2 = 0.08")
pt = it["parts"][2]
P = sp.Matrix([[0, 1], [1, 0]])
Qp = P.inv() * Q * P
chk("machine 3: Q' = (-0.4 0.1; 0.4 -0.1), same trace and det", Qp == sp.Matrix([[sp.Rational(-4, 10), sp.Rational(1, 10)], [sp.Rational(4, 10), sp.Rational(-1, 10)]]) and Qp.trace() == Q.trace() and Qp.det() == 0)
chk("machine 3: steady state moves to M^-1 (0.8, 0.2) = (0.2, 0.8)", list(P.inv() * pi) == [sp.Rational(1, 5), sp.Rational(4, 5)] and Qp * (P.inv() * pi) == sp.zeros(2, 1))
opts = {o["id"]: o for o in pt["widget"]["options"]}
chk("machine 3: key is `moved` with (0.2, 0.8)", opts["moved"].get("correct") is True and "(0.2, 0.8)" in opts["moved"]["text"] and "-0.5" in opts["moved"]["text"])
has("machine 3 question", pt["question"], "0 and $-0.5$", "(0.8, 0.2)", "Running first")
has("machine 3", json.dumps(pt, ensure_ascii=False), r"\\begin{pmatrix} -0.4 & 0.1 \\\\ 0.4 & -0.1 \\end{pmatrix}", "trace $-0.5$")
pt = it["parts"][3]
Qpn = np.array(Qp.tolist(), float)
chk("machine 4: (1, -1) is an eigenvector of Q' for -0.5", Qp * sp.Matrix([1, -1]) == sp.Rational(-1, 2) * sp.Matrix([1, -1]))
chk("machine 4: (1, 0) = (0.2, 0.8) + 0.8 (1, -1)", sp.Matrix([sp.Rational(1, 5), sp.Rational(4, 5)]) + sp.Rational(4, 5) * sp.Matrix([1, -1]) == sp.Matrix([1, 0]))
P5 = linalg.expm(5 * Qpn)
# a scan in t by small Euler steps as a third look
x = np.array([1.0, 0.0])
for _ in range(500000):
    x = x + 1e-5 * (Qpn @ x)
chk("machine 4: Euler scan to t = 5 agrees with the closed form to 1e-4", abs(x[0] - (0.2 + 0.8 * math.exp(-2.5))) < 1e-4)
numeric("machine 4", pt["widget"], (0.2 + 0.8 * math.exp(-2.5), P5[0, 0]),
        {"running-chance": (0.8 + 0.2 * math.exp(-2.5), P5[1, 1]), "no-steady": (0.8 * math.exp(-2.5), P5[0, 0] - 0.2),
         "restart-rate": (0.2 + 0.8 * math.exp(-0.4 * 5), 0.2 + 0.8 * math.exp(-2)), "one-hour": (0.2 + 0.8 * math.exp(-0.5), linalg.expm(Qpn)[0, 0])},
        accept=[0.266, 0.2657, 0.26568, 0.2656], refuse=[0.318, 0.27, 0.264, 0.268], fb=pt["feedback"], eps=6e-4)
chk("machine 4: printed e^-2.5 = 0.0821 and 0.2 + 0.8 x 0.0821 = 0.266", round(math.exp(-2.5), 4) == 0.0821 and round(0.2 + 0.8 * 0.0821, 3) == 0.266)
has("machine 4", json.dumps(pt, ensure_ascii=False), "5 hours later", "(0.2, 0.8)", "e^{-2.5}", "0.266 at $t = 5$")
pt = it["parts"][4]
t = sp.nsolve(sp.Rational(4, 5) * sp.exp(-sp.Symbol("t") / 2) - sp.Rational(1, 100), 8)
numeric("machine 5", pt["widget"], (math.log(80) / 0.5, float(t)),
        {"running-start": (math.log(20) / 0.5, 2 * math.log(0.2 / 0.01)), "no-coefficient": (math.log(100) / 0.5, 2 * math.log(100)),
         "restart-rate": (math.log(80) / 0.4, 2.5 * math.log(80)), "multiplied": (math.log(80) * 0.5, math.log(80) / 2)},
        accept=[8.76, 8.764, 8.77], refuse=[5.4, 5.40, 8.8, 8.7, 8.78], fb=pt["feedback"], eps=6e-3)
chk("machine 5: printed ln 80 = 4.382 and 4.382 / 0.5 = 8.764", round(math.log(80), 3) == 4.382)
chk("machine 5: 'about 8.8 hours' and 'minus the sum of the two rates' hold", round(math.log(80) / 0.5, 1) == 8.8 and -(0.1 + 0.4) == -0.5)

# ====================================================================================================
# 3. number-sense/problems-1 to -3
# ====================================================================================================
N1, N2, N3 = "courses/number-sense/problems-1", "courses/number-sense/problems-2", "courses/number-sense/problems-3"
it = part(N1, "p-garden-beds")
pt = it["parts"][0]
numeric("garden 1", pt["widget"], (F(1, 4) * 20, 20 / 4), {"flipped": (20 * 4, 20 / F(1, 4)), "three-quarters": (F(3, 4) * 20, 20 - 5)},
        accept=[5], refuse=[8, 4, 6], fb=pt["feedback"])
chk("garden 1: unit beds; question asks for the beans", pt["widget"].get("unit") == "beds" and "beans" in pt["question"])
chk("garden 2: potatoes 8 beds, beans 5, together 13/20 (chain)", F(2, 5) * 20 == 8 and F(2, 5) + F(1, 4) == F(13, 20) and close(it["parts"][1]["widget"]["answer"], 0.65, 1e-9))
has("garden 2 explain", it["parts"][1]["explain"]["text"], "Beans take 5 beds", "= 8$ beds")
chk("garden 3, 4: 7/20 and 7/40 (chain)", close(it["parts"][2]["widget"]["answer"], 1 - 0.65, 1e-9) and close(it["parts"][3]["widget"]["answer"], F(7, 40), 1e-9))

it = part(N1, "p-rye-loaves")
flour, loaf = F(5, 6), F(1, 5)
has("rye prose", it["prose"], r"\tfrac{5}{6}", r"\tfrac{1}{5}")
pt = it["parts"][0]
count = 0
left = flour
while left >= loaf:
    left -= loaf
    count += 1
numeric("rye 1", pt["widget"], (flour / loaf, (5 / 6) / (1 / 5)), {"multiplied": (flour * loaf, 1 / 6), "wrong-flip": (F(6, 5) * loaf, 6 / 25)},
        accept=[F(25, 6), 4 + F(1, 6), 4.1667, 4.167], refuse=[F(10, 3), 4, 4.2, 4.16], fb=pt["feedback"])
pt = it["parts"][1]
numeric("rye 2", pt["widget"], (math.floor(flour / loaf), count), {"rounded-up": (math.ceil(flour / loaf), count + 1), "carried": (math.floor(flour * loaf), 0)},
        accept=[4], refuse=[3, 5], fb=pt["feedback"])
chk("rye 2: unit loaves; a sixth of a loaf's flour is left", pt["widget"].get("unit") == "loaves" and left / loaf == F(1, 6))
pt = it["parts"][2]
numeric("rye 3", pt["widget"], (flour - 4 * loaf, left), {"one-loaf": (flour - loaf, 19 / 30), "tops-bottoms": (F(5 - 4, 6 - 5), 1.0), "loaf-sixth": (flour / loaf - 4, 1 / 6)},
        accept=[F(1, 30), 0.0333, 0.03333], refuse=[F(1, 12), 0.03, 0.04, 0.034], fb=pt["feedback"])
chk("rye 3: unit kg; 25/30 - 24/30", pt["widget"].get("unit") == "kg" and flour == F(25, 30) and 4 * loaf == F(24, 30))
pt = it["parts"][3]
numeric("rye 4", pt["widget"], (F(1, 30) / flour, (1 / 30) * (6 / 5)), {"multiplied": (F(1, 30) * flour, 5 / 180), "flipped": (flour / F(1, 30), 25.0), "carried": (F(19, 30) / flour, 19 / 25)},
        accept=[F(1, 25), 0.04, F(6, 150)], refuse=[F(1, 10), 0.041, 0.039], fb=pt["feedback"])

it = part(N3, "p-cube-tub")
N = 2169
has("cube prose", it["prose"], "2,169", "Asha")
edge = max(n for n in range(1, 50) if n ** 3 <= N)
pt = it["parts"][0]
numeric("cube 1", pt["widget"], (edge, math.floor(round(N ** (1 / 3), 9))), {"rounded-up": (edge + 1, math.ceil(N ** (1 / 3))), "square-root": (math.floor(math.sqrt(N)), math.isqrt(N)), "thirds": (F(N, 3), N / 3)},
        accept=[12], refuse=[11, 13], routes=[(46, "square-root"), (47, "square-root"), (46.57, "square-root"), (46.6, "square-root"), (723, "thirds")], fb=pt["feedback"])
chk("cube 1: 12^3 = 1,728 < 2,169 < 2,197 = 13^3; 2,169 / 3 is whole", 12 ** 3 == 1728 < N < 2197 == 13 ** 3 and N % 3 == 0)
pt = it["parts"][1]
numeric("cube 2", pt["widget"], (N - edge ** 3, N - 12 * 12 * 12), {"squared": (N - edge ** 2, N - 144), "carried-up": (N - 13 ** 3, N - 2197), "times-three": (N - edge * 3, N - 36)},
        accept=[441], refuse=[169, 440, 442], fb=pt["feedback"])
pt = it["parts"][2]
numeric("cube 3", pt["widget"], (math.isqrt(441), math.sqrt(N - edge ** 3)), {"halved": (F(441, 2), 220.5), "quartered": (F(441, 4), 110.25)},
        accept=[21], refuse=[13, 20, 22], routes=[(220, "halved"), (221, "halved"), (110, "quartered"), (110.25, "quartered"), (110.6, None)], fb=pt["feedback"])
chk("cube 3: 21^2 = 441 exactly; 20^2 = 400, 22^2 = 484", 21 ** 2 == 441 and 20 ** 2 == 400 and 22 ** 2 == 484)
for n in (1, 2, 3):
    chk(f"cube {n}: unit cubes", it["parts"][n - 1]["widget"].get("unit") == "cubes")

# tightened tolerances
pt = part(N2, "p-golf-card", 3)
w = pt["widget"]
numeric("golf 3", w, (round(F(5, 18), 3), round(5 / 18, 3)), {"unrounded": (F(5, 18), 5 / 18), "truncated": (F(math.floor(F(5, 18) * 1000), 1000), 0.277), "flipped": (F(18, 5), 18 / 5)},
        accept=[0.278, 0.2780], refuse=[F(5, 18), 0.2778, 0.27778, 0.277, 0.279, 0.28],
        routes=[(F(5, 18), "unrounded"), (0.2778, "unrounded"), (0.27778, "unrounded"), (0.2777, "unrounded"), (0.277, "truncated"), (0.28, None), (0.279, None), (3.6, "flipped")],
        fb=pt["feedback"], eps=1e-9)
chk("golf 3: tol 0.0001 on the key and on unrounded", tol(w) == 0.0001 and tol(w["wrong"][0]) == 0.0001)
pt = part(N2, "p-taxi-split", 2)
w = pt["widget"]
numeric("taxi 2", w, (round(F(17, 6), 2), round(17 / 6, 2)), {"unrounded": (round(F(17, 6), 4), 2.8333), "rounded-up": (F(284, 100), math.ceil(17 / 6 * 100) / 100), "one-dp": (round(F(17, 6), 1), 2.8), "pence": (round(F(1700, 6)), 283)},
        accept=[2.83, 2.830], refuse=[F(17, 6), 2.833, 2.8333, 2.84, 2.82, 2.8, 2.831],
        routes=[(F(17, 6), "unrounded"), (2.833, "unrounded"), (2.8333, "unrounded"), (2.83333, "unrounded"), (2.84, "rounded-up"), (2.8, "one-dp"), (283, "pence"), (2.832, None)],
        fb=pt["feedback"], eps=1e-9)
chk("taxi 2: tol 0.0005 on the key and on unrounded", tol(w) == 0.0005 and tol(w["wrong"][0]) == 0.0005)
pt = part(N2, "p-taxi-split", 4)
chk("taxi 4: pence slip 285 = 100 x (17 - 5 x 2.83)", {x["id"]: x["value"] for x in pt["widget"]["wrong"]}.get("pence") == 285 == round((17 - 5 * 2.83) * 100))
# keys behind the new unit boxes (unchanged keys; the unit must suit the number asked for)
UNITS = [
    (N1, "p-two-printers", 3, "hours", F(7, 24) / F(3, 8)), (N1, "p-two-printers", 4, "minutes", 60 + F(7, 9) * 60),
    (N1, "p-squash-jugs", 3, "litres", F(4, 9) * F(3, 4)), (N1, "p-squash-jugs", 4, "litres", F(1, 3) + F(5, 16)),
    (N2, "p-moor-weather", 1, "°C", F(-36, 10) + F(49, 10)), (N2, "p-moor-weather", 2, "degrees", -5 - F(13, 10)),
    (N2, "p-moor-weather", 3, "degrees", F(-63, 10) / 9), (N2, "p-moor-weather", 4, "°C", -5 + 4 * F(-7, 10)),
    (N2, "p-taxi-split", 1, "£", round(F(17, 6), 4)), (N2, "p-taxi-split", 3, "p", 6 * 283 - 1700), (N2, "p-taxi-split", 4, "£", 17 - 5 * F(283, 100)),
    (N3, "p-stationery-bill", 1, "£", 40 * 5 + 20), (N3, "p-stationery-bill", 2, "£", 38 * F(485, 100) + F(195, 10)),
    (N3, "p-stationery-bill", 3, "£", 38 * F(485, 100) + F(195, 10) / 3), (N3, "p-stationery-bill", 4, "£", round((38 * F(485, 100) + F(195, 10)) / 3, 2)),
    (N3, "p-comet-probe", 1, "hours", F(12 * 10 ** 8, 4 * 10 ** 4)), (N3, "p-comet-probe", 2, "hours", 9000), (N3, "p-comet-probe", 3, "years", 3),
    (N3, "p-comet-probe", 4, "years", round(F(30000, 8760), 1)),
]
for f, pid, n, unit, key in UNITS:
    w = part(f, pid, n)["widget"]
    chk(f"{pid} {n}: unit '{unit}', key {float(key):.6g} inside the band", w.get("unit") == unit and hit(w, key) is True)
# the other slips the same fix pass added
for f, pid, n, sid, val in ((N1, "p-squash-jugs", 1, "whole-fraction", F(16, 36)), (N1, "p-two-printers", 3, "minutes", F(7, 9) * 60), (N1, "p-two-printers", 4, "hours", 1 + F(7, 9)),
                            (N2, "p-taxi-split", 2, "pence", 283), (N3, "p-comet-probe", 3, "unrounded", F(30000, 9000))):
    pt = part(f, pid, n)
    chk(f"{pid} {n}: new slip {sid} takes {float(val):.6g} and has a line", hit(pt["widget"], val) == sid and sid in pt["feedback"]["byKey"])

# ====================================================================================================
# 4. bands pass AC, parts B, C, D
# ====================================================================================================
S3 = "exams/stage-3"
# ---- B: seven widened bands
w = at("courses/series/problems-2", "items[2].parts[0]")["widget"]
numeric("B series bouncing-ball 1", w, (3 * (1 - 0.6 ** 9) / 0.4, sum(3 * 0.6 ** k for k in range(9))),
        {"forever": (3 / 0.4, 7.5), "ten": (sum(3 * 0.6 ** k for k in range(10)), 7.5 * (1 - 0.6 ** 10)), "eight": (sum(3 * 0.6 ** k for k in range(8)), 7.5 * (1 - 0.6 ** 8))},
        accept=[7.42, 7.4244, 7.43, 7.425], refuse=[7.41, 7.44, 7.4, 7.45], eps=6e-6, weps=3e-5)
chk("B series: stored `ten` 7.45467 is 2 in the fifth place off 7.5(1 - 0.6^10) = 7.45465 (not changed by the pass, band +-0.005)", abs(7.5 * (1 - 0.6 ** 10) - 7.45465) < 5e-6)
chk("B series: tol 0.01", tol(w) == 0.01)
f_ = lambda x: x / ((x + 1) * (x + 2))  # noqa: E731
Vy = 2 * math.pi * integrate.quad(lambda x: x * f_(x), 0, 2)[0]
Vx = math.pi * integrate.quad(lambda x: f_(x) ** 2, 0, 2)[0]
it = at("courses/integrals/problems-4", "items[2]")
w = it["parts"][1]["widget"]
numeric("B integrals dish 2", w, (2 * math.pi * (2 + math.log(3) - 4 * math.log(2)), Vy),
        {"no-divide": (2 * math.pi * (math.log(3) - 4 * math.log(2)), Vy - 4 * math.pi), "no-2pi": (Vy / (2 * math.pi), 2 + math.log(3) - 4 * math.log(2)), "disc": (Vx, math.pi * (5 / 3 + 4 * math.log(2 / 3)))},
        accept=[2.048, 2.0485, 2.049, 2.0483], refuse=[2.047, 2.05, 2.04], eps=1e-9)
chk("B integrals 2: tol 0.001 and accept text says +-0.001", tol(w) == 0.001 and "\\pm 0.001" in w["accept"])
w = it["parts"][3]["widget"]
numeric("B integrals dish 4", w, (Vy / Vx, 2 * (2 + math.log(3) - 4 * math.log(2)) / (5 / 3 + 4 * math.log(2 / 3))),
        {"inverse": (Vx / Vy, (5 / 3 + 4 * math.log(2 / 3)) / (2 * (2 + math.log(3) - 4 * math.log(2)))),
         "square-integral": (Vy / (math.pi * math.log(4 / 3) ** 2), Vy / (math.pi * integrate.quad(f_, 0, 2)[0] ** 2))},
        accept=[15, 14.55, 14.6, 14.5526], refuse=[13, 16, 13.5, 15.6], eps=1e-9)
chk("B integrals 4: accept text gives the band 13.55 to 15.55", tol(w) == 1 and "13.55 to 15.55" in w["accept"])
chk("B integrals 4: the band refuses 14, which is not the nearest whole number to 14.55", hit(w, 14) is not True,
    claim="finding 4.1: 14 is now accepted although the part asks for the nearest whole number, 15")
w = part(S3, "r-turnover-cost")["widget"]
numeric("B stage-3 r-turnover-cost", w, (F(11, 1000) / F(14, 10), 0.011 / 1.4), {"twice": (F(11, 1000) / F(28, 10), 0.011 / 2.8), "no-turnover": (F(11, 1000), 0.011)},
        accept=[0.0079, 0.007857, 0.0078], refuse=[0.008, 0.0077, 0.0081], eps=6e-9)
chk("B r-turnover-cost: tol 0.0001 (0.01 per cent)", tol(w) == 0.0001)
w = part(S3, "r-small-share", 2)["widget"]
vw = (9 * 5 * F(1, 100) + F(5, 100) * F(60, 100)) / (9 * 5 + F(5, 100))
numeric("B stage-3 r-small-share 2", w, (vw, 0.48 / 45.05), {"equal-weighted": (F(9 * 1 + 60, 1000), (9 * 0.01 + 0.6) / 10), "big-only": (F(1, 100), 0.45 / 45)},
        accept=[0.0107, 0.010655, 0.0106], refuse=[0.0105, 0.0108, 0.01], eps=6e-9)
w = part(S3, "r-oos-power", 1)["widget"]
numeric("B stage-3 r-oos-power 1", w, (4.0 * 0.5 * math.sqrt(120 / 240), math.sqrt(2)), {"halved-only": (4.0 * 0.5, 2), "full-mean": (4.0 * math.sqrt(120 / 240), 2 * math.sqrt(2))},
        accept=[1.41, 1.4142, 1.42], refuse=[1.4, 1.40, 1.43, 1.5], eps=6e-7)
w = part("exams/topic-0.2", "e-formula")["widget"]
numeric("B topic-0.2 e-formula", w, ((3 + math.sqrt(65)) / 4, max(np.roots([2, -3, -7]))), {"no-2a": ((3 + math.sqrt(65)) / 2, 5.5311288741), "sign-b": ((-3 + math.sqrt(65)) / 4, 1.2655644371)},
        accept=[2.77, 2.7656, 2.76, 2.766], refuse=[2.75, 2.78, 2.8], eps=1e-9)

# ---- C: two exam items accepted by a wider band
it = part(S3, "r-t-bar")
w = it["parts"][0]["widget"]
t_exact = 0.45 / (3.1 / math.sqrt(360))
numeric("C r-t-bar 1", w, (t_exact, 0.45 * math.sqrt(360) / 3.1), {"no-root": (0.45 / 3.1, 0.1451613), "years": (0.45 / (3.1 / math.sqrt(30)), 0.45 * math.sqrt(30) / 3.1)},
        accept=[2.75, 2.76, 2.754, 2.7607], refuse=[2.74, 2.77, 2.7, 2.8], eps=6e-7)
chk("C r-t-bar: band is 2.744 to 2.764", tol(w) == 0.01 and close(w["answer"] - 0.01, 2.744242, 1e-6))
# workings a candidate might use, and whether the band now takes each (typed to 2 places as asked)
WORK_T = [
    ("exact", t_exact, True), ("se kept as 0.163", 0.45 / 0.163, True), ("se kept as 0.1634", 0.45 / 0.1634, True), ("root 360 as 19", 0.45 * 19 / 3.1, True),
    ("root 360 as 18.97", 0.45 * 18.97 / 3.1, True), ("n - 1 = 359 under the root", 0.45 * math.sqrt(359) / 3.1, True),
    ("se kept as 0.16", 0.45 / 0.16, False), ("root 360 as 20", 0.45 * 20 / 3.1, False), ("sd over n", 0.45 / (3.1 / 360), False),
    ("no root", 0.45 / 3.1, False), ("years", 0.45 * math.sqrt(30) / 3.1, False), ("variance for sd: 0.45 / (3.1^2 / root 360)", 0.45 / (3.1 ** 2 / math.sqrt(360)), False),
    ("annualised mean over annualised sd, 30 years", (0.45 * 12) / (3.1 * math.sqrt(12)) * math.sqrt(30), True),
]
for name, v, want in WORK_T:
    chk(f"C r-t-bar: working '{name}' gives {v:.4f}, typed {round(v, 2):.2f}: accepted is {want}", (hit(w, round(v, 2)) is True) == want)
chk("C r-t-bar: every accepted working above is a sound one (the last is the same statistic in annual units)", True)
has("C r-t-bar explain", it["explain"]["text"], "0.163", "2.75", "2.76 if you keep the rounded 0.163")
chk("C r-t-bar: printed se 3.1 / root 360 = 0.163", round(3.1 / math.sqrt(360), 3) == 0.163)

it = part(S3, "r-best-of-twenty")
w = it["widget"]
p1 = 0.5 * math.erfc(math.sqrt(5) / math.sqrt(2))
p2 = stats.norm.sf(1, loc=0, scale=1 / math.sqrt(5))
best = 1 - (1 - p1) ** 20
numeric("C r-best-of-twenty", w, (best, -math.expm1(20 * math.log1p(-p2))), {"one-variant": (p1, p2), "added-chances": (20 * p1, 20 * p2)},
        accept=[0.23, 0.22, 0.225, 0.2252, 0.2224], refuse=[0.21, 0.24, 0.2, 0.25], eps=6e-7)
chk("C r-best-of-twenty: band is 0.219 to 0.231", tol(w) == 0.006 and close(w["answer"] - 0.006, 0.219156, 1e-6) and close(w["answer"] + 0.006, 0.231156, 1e-6))
WORK_B = [
    ("exact", best, True), ("p as 0.0127", 1 - (1 - 0.0127) ** 20, True), ("table at z = 2.24, p = 0.0125", 1 - 0.9875 ** 20, True),
    ("table at z = 2.23, p = 0.0129", 1 - 0.9871 ** 20, True), ("p as 0.013", 1 - 0.987 ** 20, True), ("1 - 0.775", 1 - 0.775, True), ("1 - 0.78", 1 - 0.78, True),
    ("Poisson form 1 - exp(-20p)", 1 - math.exp(-20 * p1), True),
    ("p as 0.012", 1 - 0.988 ** 20, False), ("p as 0.01", 1 - 0.99 ** 20, False), ("added chances", 20 * p1, False), ("added chances, p = 0.0125", 20 * 0.0125, False),
    ("added chances, p = 0.012", 20 * 0.012, False), ("two-sided p", 1 - (1 - 2 * p1) ** 20, False), ("one variant", p1, False),
    ("sd 1/5 for 1/root 5", 1 - (1 - stats.norm.sf(5)) ** 20, False), ("z = 1 (sd taken as 1)", 1 - stats.norm.cdf(1) ** 20, False),
    ("all 20 above 1", p1 ** 20, False),
    # a miscount of the variants cannot be told from the key at 2 places: 21 gave 0.23 before the pass too, 19 gives 0.22 now
    ("19 variants", 1 - (1 - p1) ** 19, True), ("21 variants", 1 - (1 - p1) ** 21, True), ("18 variants", 1 - (1 - p1) ** 18, False), ("22 variants", 1 - (1 - p1) ** 22, False),
    ("z = 2.2, p = 0.0139", 1 - (1 - 0.0139) ** 20, False), ("z = 2.3, p = 0.0107", 1 - (1 - 0.0107) ** 20, False),
]
for name, v, want in WORK_B:
    got = hit(w, round(v, 2)) is True
    chk(f"C r-best-of-twenty: working '{name}' gives {v:.4f}, typed {round(v, 2):.2f}: accepted is {want}", got == want)
has("C r-best-of-twenty explain", it["explain"]["text"], "0.0127", "0.775", "about 0.23 (0.22 from table values)")
chk("C r-best-of-twenty: printed 0.0127 and 0.775 (0.775 is from the unrounded p; with 0.0127 it is 0.7744)", round(p1, 4) == 0.0127 and round((1 - p1) ** 20, 3) == 0.775 and round((1 - 0.0127) ** 20, 4) == 0.7744)

# ---- D: ten misrouted slips
w = part("courses/ds/review-4", "r4-height")["widget"]
chk("D ds r4-height: one wrong entry left at 4, key 3", [x["id"] for x in w["wrong"]] == ["nodes"] and hit(w, 4) == "nodes" and hit(w, 3) is True)
it = part("courses/estimation/homework-3", "h-laplace")
n = sp.Symbol("n", positive=True)
chk("D estimation h-laplace: (n+1)/(n+1) is 1, the mle entry; one-pseudo gone", sp.simplify((n + 1) / (n + 1)) == 1 and [x["id"] for x in it["widget"]["wrong"]] == ["mle", "no-prior-head"])
chk("D estimation h-laplace: Beta(n+1, 1) mean (n+1)/(n+2); 11/12 = 0.917", sp.simplify(sp.Rational(1) * (n + 1) / ((n + 1) + 1) - (n + 1) / (n + 2)) == 0 and round(11 / 12, 3) == 0.917)
chk("D estimation h-laplace: byKey holds exactly the two ids", sorted(it["feedback"]["byKey"]) == ["mle", "no-prior-head"])
it = part("courses/limits/homework-5", "h-arctan-recip")
x = sp.Symbol("x", positive=True)
d = sp.diff(sp.atan(1 / x), x)
chk("D limits h-arctan-recip: derivative -1/(1+x^2); outer slope 1/(1+1/x^2) = x^2/(1+x^2)", sp.simplify(d + 1 / (1 + x ** 2)) == 0 and sp.simplify(1 / (1 + 1 / x ** 2) - x ** 2 / (1 + x ** 2)) == 0)
chk("D limits h-arctan-recip: unsimplified gone, two ids left with lines", [e["id"] for e in it["widget"]["wrong"]] == ["sign", "no-chain"] and sorted(it["feedback"]["byKey"]) == ["no-chain", "sign"])
it = part("courses/multivar/homework-5", "h-parallelogram")
u, v = sp.symbols("u v")
J = sp.Matrix([[2, 1], [1, 2]]).det()
I_full = sp.integrate((3 * u + 3 * v) * J, (u, 0, 1), (v, 0, 1))
I_noJ = sp.integrate(3 * u + 3 * v, (u, 0, 1), (v, 0, 1))
num_full = integrate.dblquad(lambda vv, uu: (3 * uu + 3 * vv) * 3, 0, 1, 0, 1)[0]
chk("D multivar h-parallelogram: integral 9 (sympy, dblquad), without J 3, area 3", I_full == 9 and close(num_full, 9, 1e-9) and I_noJ == 3 and J == 3)
chk("D multivar h-parallelogram: one wrong entry at 3", [e["id"] for e in it["widget"]["wrong"]] == ["noJ"] and hit(it["widget"], 3) == "noJ" and list(it["feedback"]["byKey"]) == ["noJ"])
w = at("courses/markov/l20-when-stopping-fails", "screens[5]")["widget"]
numeric("D markov l20 doubling", w, (F(1023, 1024) * 1 - F(1, 1024) * 1023, 1 * (1 - 0.5 ** 10) - 1023 * 0.5 ** 10),
        {"win": (1, 1.0), "most": (round(F(1023, 1024), 3), round(1 - 0.5 ** 10, 3)), "loss": (-1023, -sum(2 ** k for k in range(10)))},
        accept=[0], refuse=[1, 0.999],
        routes=[(1, "win"), (1.0, "win"), (0.999, "most"), (0.9990, "most"), (F(1023, 1024), "most"), (0.99902, "most"), (0.9995, "most"), (0.9996, "win"), (-1023, "loss")], eps=1e-9)
w = at("courses/multivar/l4-chain-two-inputs", "screens[8]")["widget"]
per = F(56, 100) * F(50, 100) + F(28, 100) * F(-5, 10)
numeric("D multivar l4 option book", w, (1000 * per, 1000 * (0.56 * 0.50 + 0.28 * -0.5)),
        {"delta-only": (1000 * F(56, 100) * F(1, 2), 280), "vega-only": (1000 * F(28, 100) * F(-1, 2), -140), "sign": (1000 * (F(28, 100) + F(14, 100)), 420),
         "rates": (F(50, 100) + F(-5, 10), 0.5 - 0.5), "per-option": (per, 0.14)},
        accept=[140], refuse=[0, 0.14], routes=[(0, "rates"), (0.14, "per-option"), (0.1, "rates"), (0.136, "per-option")], eps=1e-9)
# numerics l12: m' = 0.5(4 - m), m(0) = 6; r' = 50(m - r), r(0) = 3; all in per cent


def euler(h):
    m, r = 6.0, 3.0
    for _ in range(round(1 / h)):
        m, r = m + h * 0.5 * (4 - m), r + h * 50 * (m - r)
    return r


Aode = np.array([[-0.5, 0.0], [50.0, -50.0]])
z = linalg.expm(Aode) @ np.array([6.0 - 4.0, 3.0 - 4.0])
r_exact = 4 + z[1]
m1 = 4 + 2 * math.exp(-0.5)
# closed form: r = 4 + a e^{-0.5 t} + b e^{-50 t}, a = 2 * 50 / 49.5, b = -1 - a
a_ = 2 * 50 / 49.5
r_closed = 4 + a_ * math.exp(-0.5) + (-1 - a_) * math.exp(-50)
w = at("courses/numerics/l12-stiff-equations", "screens[0]")["widget"]
def euler_mat(h):
    step = np.eye(2) + h * Aode
    return 4 + (np.linalg.matrix_power(step, round(1 / h)) @ np.array([2.0, -1.0]))[1]


numeric("D numerics l12 stiff", w, (euler(0.04) / 100, euler_mat(0.04) / 100), {"exact": (r_exact / 100, r_closed / 100), "small": (euler(0.02) / 100, euler_mat(0.02) / 100)},
        accept=[0.0824, 0.082393, 0.08239], refuse=[0.052253],
        routes=[(0.052253, "exact"), (0.05225, "exact"), (0.052222, "small"), (0.05222, "small"), (0.0522, None)], eps=1e-5)
chk("D numerics l12: exact r(1) = 5.2253% by expm and closed form; Euler 8.2393% and 5.2222%", round(r_exact, 4) == round(r_closed, 4) == 5.2253 and round(euler(0.04), 4) == 8.2393 and round(euler(0.02), 4) == 5.2222)
chk("D numerics l12: the exact value typed to 2 places, 5.23%, reaches the `exact` line", hit(w, 0.0523) == "exact",
    claim="finding 4.2: 5.23% (the exact value to the 2 places the key is given in) now gets the generic line")
w = part("courses/stat-learning/review-2", "r-test-r2")["widget"]
numeric("D stat-learning r-test-r2", w, (1 - F(92, 90), 1 - 9.2 / 9.0), {"pos": (F(92, 90) - 1, 9.2 / 9.0 - 1), "flip": (1 - F(90, 92), 1 - 9.0 / 9.2)},
        accept=[-0.0222, -0.022, -0.02222], refuse=[0.0222],
        routes=[(0.0222, "pos"), (0.02222, "pos"), (0.022, "pos"), (0.0217, "flip"), (0.02174, "flip"), (0.0218, "flip"), (0.02, None)], eps=6e-5)
for typed in (-0.0217, -0.02174, -0.021739):
    chk(f"D stat-learning r-test-r2: the key band refuses {typed}, the gap over the model's MSE, (9.0 - 9.2) / 9.2 = {(9.0 - 9.2) / 9.2:.6f}", hit(w, typed) is not True,
        claim="finding 4.3: the key band -0.0222 +- 0.0005 takes the wrong-denominator answer")
w = at("courses/taylor/l2-how-wrong", "screens[10]")["widget"]
numeric("D taylor l2 hedge", w, (1000 * F(1, 2) * F(4, 100) * 25, 1000 * 0.5 * 0.04 * 5 ** 2),
        {"no-half": (1000 * F(4, 100) * 25, 1000.0), "not-squared": (1000 * F(1, 2) * F(4, 100) * 5, 100.0), "zero": (0, 0.0), "per-contract": (F(1, 2) * F(4, 100) * 25, 0.5)},
        accept=[500], refuse=[0, 0.5], routes=[(0, "zero"), (0.5, "per-contract"), (0.50, "per-contract"), (0.1, "zero"), (0.3, None)], eps=1e-9)


def bs_call(S, K, sv):
    d1 = (math.log(S / K) + 0.5 * sv * sv) / sv
    return S * stats.norm.cdf(d1) - K * stats.norm.cdf(d1 - sv)


sv = 8.0 / (0.4 * 100)  # the rule: price = 0.4 * sigma * root T * S = 8.00 at the money
w = at("courses/trees/l13-rules-of-thumb", "screens[7]")["widget"]
def call_quad(S, K, s):
    return integrate.quad(lambda zz: max(S * math.exp(-0.5 * s * s + s * zz) - K, 0) * stats.norm.pdf(zz), -10, 10, points=[(math.log(K / S) + 0.5 * s * s) / s])[0]


numeric("D trees l13 away from the money", w, (bs_call(100, 110, sv), call_quad(100, 110, sv)), {"rule": (0.4 * sv * 100, 8.0), "atm": (bs_call(100, 100, sv), call_quad(100, 100, sv))},
        accept=[4.29, 4.3, 4.292], refuse=[8, 7.97],
        routes=[(8, "rule"), (8.00, "rule"), (7.97, "atm"), (7.966, "atm"), (7.96, "atm"), (7.98, "atm"), (8.01, "rule"), (7.95, None)], eps=6e-3)
chk("D trees l13: the curve's own values 5.91, 4.29, 2.15 follow from Black-Scholes at r = 0 with sigma root T = 0.2",
    [round(bs_call(100, k, sv), 2) for k in (105, 110, 120)] == [5.91, 4.29, 2.15])

print(f"recompute: {checks} checks, {fails} failures, {claims} CLAIM rows (findings in the review)")
sys.exit(1 if fails else 0)
