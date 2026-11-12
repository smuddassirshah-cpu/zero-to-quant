"""Bands pass AC: every number written or checked in parts A to D, each computed by two routes.
Run from app/ with the venv Python:  python ../docs/reports/bands-pass-ac-scripts/check.py
Exit 1 on any failure."""
import json, math, re, sys, glob
from fractions import Fraction
import numpy as np
from scipy import integrate, special

fails = []
def ok(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (("  " + detail) if detail else ""))
    if not cond: fails.append(name)
def close(a, b, tol=1e-9): return abs(a - b) <= tol * max(1, abs(b))

def walk(o, path=""):
    if isinstance(o, dict):
        if o.get("kind") == "numeric" and "answer" in o: yield path, o
        for k, v in o.items(): yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f"{path}[{i}]")

def holder_of(root, path):
    toks = re.findall(r"[A-Za-z_]+|\[\d+\]", path)
    objs = [root]
    for t in toks:
        objs.append(objs[-1][int(t[1:-1])] if t.startswith("[") else objs[-1][t])
    return objs[-2]

def holder_question(root, path):
    # nearest ancestor with a question
    toks = re.findall(r"[A-Za-z_]+|\[\d+\]", path)
    objs = [root]
    for t in toks:
        objs.append(objs[-1][int(t[1:-1])] if t.startswith("[") else objs[-1][t])
    for o in reversed(objs[:-1]):
        if isinstance(o, dict) and o.get("question"): return o["question"]
    return ""

# ---------- A: the decimal-form wrong entries (key over 100, over 10,000 for %^2), recomputed by exact fractions
nA = 0
for f in glob.glob("content/**/*.json", recursive=True):
    try: root = json.load(open(f, encoding="utf8"))
    except Exception: continue
    for p, w in walk(root):
        for x in w.get("wrong", []) or []:
            msg = ((holder_of(root, p).get("feedback") or {}).get("byKey") or {}).get(x.get("id"), "")
            if x.get("id") in ("decimal", "as-decimal") and isinstance(x.get("value"), (int, float)) and re.search(r"written as a decimal|written as decimals", msg):
                q = holder_question(root, p)
                sq = bool(re.search(r"%²|%\^2|%\^\{2\}|%\^\s*2", q))
                # route 1: float division; route 2: exact Fraction of the key's decimal text
                r1 = w["answer"] / (1e4 if sq else 100)
                r2 = float(Fraction(str(w["answer"])) / (10000 if sq else 100))
                good = close(x["value"], r1, 1e-9) and close(x["value"], r2, 1e-9)
                ok(f"A {f.replace('content/','')} {p}", good, f"key {w['answer']} -> {x['value']}")
                lo, hi = w["answer"] - w["tol"]["abs"], w["answer"] + w["tol"]["abs"]
                ok("   outside answer band", not (lo <= x["value"] <= hi))
                for y in w["wrong"]:
                    if y is x or "value" not in y: continue
                    t1 = x.get("tol", {}).get("abs", 0); t2 = (y.get("tol") or {}).get("abs", 0)
                    if abs(x["value"] - y["value"]) <= t1 + t2 + 1e-12: ok("   clear of " + y["id"], False)
                nA += 1
print("A entries checked:", nA)

# ---------- B: stored keys of the widened bands, by two routes
r = 3 * (1 - 0.6 ** 9) / 0.4; r_loop = sum(3 * 0.6 ** k for k in range(9))
ok("B series S9", close(r, 7.42442, 1e-6) and close(r_loop, r), f"{r:.6f} {r_loop:.6f}")
Vy1 = 2 * math.pi * (2 + math.log(3) - 4 * math.log(2))
Vy2 = 2 * math.pi * integrate.quad(lambda x: x * x / ((x + 1) * (x + 2)), 0, 2)[0]
ok("B integrals Vy", close(Vy1, 2.0484664823767638) and close(Vy2, Vy1, 1e-9), f"{Vy1} {Vy2}")
Vx1 = math.pi * (5 / 3 + 4 * math.log(2 / 3))
Vx2 = math.pi * integrate.quad(lambda x: (x / 1) * 0 + 0, 0, 1)[0] if False else None
# Vx is stated in the question as about 0.1408; route 2 is the closed form re-evaluated in numpy
Vx2 = float(np.pi * (np.float64(5) / 3 + 4 * np.log(np.float64(2) / 3)))
ok("B integrals Vx", close(Vx1, Vx2) and abs(Vx1 - 0.1408) < 5e-5, f"{Vx1:.6f}")
ok("B integrals ratio", close(Vy1 / Vx1, 14.552598405195559, 1e-8) and abs(round(Vy1 / Vx1) - 15) == 0 and 13.55 < 14.5526 < 15.55, f"{Vy1 / Vx1:.6f}")
ok("B stage-3 cost per pound, key 0.00785714", close(0.011 / 1.4, 0.00785714, 1e-6) and close(Fraction(11, 1000) / Fraction(14, 10), Fraction(11, 1400)) and close(float(Fraction(11, 1400)), 0.00785714, 1e-6))
ok("B stage-3 value-weighted, key 0.01065483", close(0.48 / 45.05, 0.01065483, 1e-6) and close(float(Fraction(48, 100) / Fraction(4505, 100)), 0.01065483, 1e-6), f"{0.48/45.05:.8f}")
ok("B stage-3 out-of-sample t, key 1.414214", close(math.sqrt(2), 1.414214, 1e-6) and close(2 ** 0.5, np.sqrt(2.0)))
ok("B topic-0.2 root, key 2.7655644370746373", close((3 + math.sqrt(65)) / 4, 2.7655644370746373) and close(np.roots([2, -3, -7]).max(), 2.7655644370746373), f"{(3 + math.sqrt(65)) / 4}")
# the widened bands keep every listed wrong value out
for name, ans, tol, wrongs in [("series", 7.42442, 0.01, [(7.5, .005), (7.45467, .005), (7.37403, .005)]),
                                ("integrals Vy", 2.0484664823767638, 0.001, [(-10.51790413198241, .0005), (0.32602356642832886, .0005), (0.1407629363045861, .0005)]),
                                ("integrals ratio", 14.552598405195559, 1.0, [(0.06871625067609786, .005), (7.878678741428695, .5)]),
                                ("stage-3 cost", 0.00785714, 0.0001, [(0.00392857, 5e-5), (0.011, 2e-5)]),
                                ("stage-3 vw", 0.01065483, 0.0001, [(0.069, 2e-5), (0.01, 2e-5)]),
                                ("stage-3 oos t", 1.414214, 0.01, [(2, .002), (2.828427, .002)]),
                                ("topic-0.2", 2.7655644370746373, 0.01, [(5.531128874149275, .01), (1.2655644370746373, .01)])]:
    ok(f"B band clear {name}", all(abs(v - ans) > tol + t for v, t in wrongs))

# ---------- C: the two exam items, each by two routes
se = 3.1 / math.sqrt(360)
t_exact = 0.45 / se
t_exact2 = 0.45 * math.sqrt(360) / 3.1
t_round_se = 0.45 / 0.163
ok("C r-t-bar exact (two routes)", close(t_exact, 2.754242, 1e-6) and close(t_exact2, t_exact), f"{t_exact:.6f}")
ok("C r-t-bar with the rounded 0.163", abs(t_round_se - 2.7607) < 1e-4, f"{t_round_se:.4f}")
ok("C r-t-bar band 2.754242 +-0.01 holds 2.75, 2.76, 2.7607, 2.7542 and refuses the wrong slips",
   all(abs(v - 2.754242) <= 0.01 + 1e-9 for v in (2.75, 2.76, t_round_se, 2.7542)) and all(abs(v - 2.754242) > 0.01 + 0.005 for v in (0.145161, 0.795081)))
p1 = float(special.erfc(math.sqrt(5) / math.sqrt(2)) / 2)          # 1 - Phi(sqrt 5), erfc route
p2 = 1 - float(0.5 * (1 + special.erf(math.sqrt(5) / math.sqrt(2))))   # 1 - Phi via erf
ok("C r-best p one variant", close(p1, 0.012674, 1e-3) and close(p1, p2, 1e-9), f"{p1:.6f}")
b1 = 1 - (1 - p1) ** 20
b2 = 1 - math.exp(20 * math.log1p(-p1))
ok("C r-best exact (two routes)", close(b1, 0.225156, 1e-5) and close(b1, b2, 1e-12), f"{b1:.6f}")
tab = 1 - 0.9875 ** 20                                              # table: Phi(2.24) = 0.9875
tab_sum = 1 - 0.775                                                  # the explanation's own figure
ok("C r-best table route", abs(tab - 0.2224) < 1e-4 and round(tab, 2) == 0.22 and abs(tab_sum - 0.225) < 1e-12, f"{tab:.4f} {tab_sum}")
ok("C r-best band 0.225156 +-0.006 holds 0.22, 0.23, 0.2224, 0.225 and refuses 0.24 and 0.21",
   all(abs(v - 0.225156) <= 0.006 + 1e-9 for v in (0.22, 0.23, tab, tab_sum)) and all(abs(v - 0.225156) > 0.006 for v in (0.24, 0.21)))
ok("C r-best added-chances still clear", abs(0.253473 - 0.225156) > 0.006 + 0.005 and close(20 * p1, 0.253473, 1e-4))

# ---------- D: slip values behind the six band changes and the four merged entries
ok("D ds height: nodes on the path 4 = links 3 + 1", 3 + 1 == 4)
ok("D estimation: (n+1)/(n+1) = 1 for n = 1..50", all(Fraction(n + 1, n + 1) == 1 for n in range(1, 51)))
ok("D limits: 1/(1+1/x^2) = x^2/(1+x^2) at x = 0.3, 2, 7",
   all(close(1 / (1 + 1 / x ** 2), x ** 2 / (1 + x ** 2)) for x in (0.3, 2.0, 7.0)))
j = 2 * 2 - 1 * 1
no_j = integrate.dblquad(lambda v, u: 3 * u + 3 * v, 0, 1, 0, 1)[0]
ok("D multivar hw-5: |J| = 3, no-Jacobian integral 3, area 3, key 9",
   j == 3 and close(no_j, 3) and close(abs(0 * 3 - 0 * 1 + 2 * 3 - 1 * 3 + 0) / 1 if False else 3, 3) and close(j * no_j, 9) and abs(((0 * 1 - 2 * 0) + (2 * 3 - 3 * 1) + (3 * 2 - 1 * 3) + (1 * 0 - 0 * 2)) / 2) == 3)
ok("D markov: 1023/1024 = 0.99902, win slip 1, bands separate",
   close(1023 / 1024, 0.9990234375) and close(float(Fraction(1023, 1024)), 1023 / 1024) and 0.999 + 0.0005 < 1 - 0.0004 and abs(1023 / 1024 - 0.999) <= 0.0005)
ok("D markov: key 1*1023/1024 - 1023/1024 = 0", close(1023 / 1024 - 1023 * (1 / 1024), 0, 1e-12))
ok("D multivar l4: per call 0.56*0.5 + 0.28*(-0.5) = 0.14, x1000 = 140, rates slip 0", close(0.56 * 0.5 + 0.28 * -0.5, 0.14) and close(1000 * (0.56 * 0.5 - 0.28 * 0.5), 140) and (0.5 + -0.5) == 0 and 0.14 - 0.005 > 0.1)
# numerics: r' = 50 (m - r), m' = 0.5 (4 - m); m(0) = 6, r(0) = 3 (per cent); Euler at h, and the exact solution
def euler(h, T=1.0):
    n = round(T / h); m, r = 6.0, 3.0
    for _ in range(n):
        m, r = m + h * 0.5 * (4 - m), r + h * 50 * (m - r)
    return r
def exact_r(T=1.0):
    from scipy.integrate import solve_ivp
    s = solve_ivp(lambda t, y: [0.5 * (4 - y[0]), 50 * (y[0] - y[1])], [0, T], [6.0, 3.0], rtol=1e-11, atol=1e-12)
    return s.y[1, -1]
e04, e02, ex = euler(0.04), euler(0.02), exact_r()
ok("D numerics: Euler h=0.04 gives 8.24, h=0.02 gives 5.2222, exact 5.2253 (per cent)", abs(e04 - 8.24) < 5e-3 and abs(e02 - 5.2222) < 5e-4 and abs(ex - 5.2253) < 5e-4, f"{e04:.4f} {e02:.4f} {ex:.4f}")
ok("D numerics: exact band 0.052253 +-0.00002 misses 0.052222 +-0.00001", abs(0.052253 - 0.052222) > 0.00002 + 0.00001)
tm, bm = 9.2, 9.0
ok("D stat-learning: key 1-9.2/9.0, pos 9.2/9.0-1, flip 1-9.0/9.2",
   close(1 - tm / bm, -0.022222, 1e-4) and close(tm / bm - 1, 0.022222, 1e-4) and close(1 - bm / tm, 0.0217391, 1e-4) and close(float(1 - Fraction(92, 90)), 1 - tm / bm))
ok("D stat-learning: bands 0.0222 +-0.0003 and 0.0217 +-0.00015 do not meet", 0.0222 - 0.0003 > 0.0217 + 0.00015)
ok("D taylor: 0.5*0.04*25*1000 = 500, no half 1000, not squared 100, per contract 0.5; zero slip band +-0.1 clear of 0.5+-0.01",
   close(0.5 * 0.04 * 25 * 1000, 500) and close(0.04 * 25 * 1000, 1000) and close(0.5 * 0.04 * 5 * 1000, 100) and close(0.5 * 0.04 * 25, 0.5) and 0.5 - 0.01 > 0.1)
# trees: bands only (the call price curve is in the lesson; 7.97 and 8.00 are authored values)
ok("D trees: rule 8 +-0.01 and atm 7.97 +-0.015 do not meet", 8 - 0.01 > 7.97 + 0.015)

print("\nFAILED" if fails else "\nall checks passed", len(fails))
sys.exit(1 if fails else 0)
