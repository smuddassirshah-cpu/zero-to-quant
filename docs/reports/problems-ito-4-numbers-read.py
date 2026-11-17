#!/usr/bin/env python3
"""Second read of app/content/courses/ito/problems-4.json (3 problems, 13 parts).

Every key, every `wrong` value and every printed number is recomputed by a
route the author's script (problems-ito-4-numbers.py) does not use:

- p-band-wait (re-authored from p-tracking-review in the session AF fix pass):
  Gaussian conditional moments for the cubic martingale;
  the boundary-value problems (1/2) s^2 u'' = -1 and (1/2) s^2 w'' = -h for
  E[tau] and E[tau; exit at the top], integrated exactly with sympy; the closed
  form (L^2 - x^2) / (3 s^2) for the conditioned exit time.
- p-two-date-product: Gauss-Hermite quadrature over the two independent
  yearly moves, and the tower rule done as a second quadrature.
- p-dividend-hedge: finite differences of V and the residual of the equation
  with r - q, a share count that reinvests its dividends step by step, and a
  quadrature of S_T with drift r - q.

No root finder is used, so nothing depends on a solver converging.
Always exits 0. A failing check prints a line starting FINDING.
"""
import json
import math
import os
import re
from fractions import Fraction as F

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.path.join(HERE, "..", "..", "app", "content", "courses", "ito", "problems-4.json")
data = json.load(open(SET, encoding="utf-8"))
items = {it["id"]: it for it in data["items"]}

n_checks = 0
n_fail = 0


def check(name, ok, detail=""):
    global n_checks, n_fail
    n_checks += 1
    if not ok:
        n_fail += 1
        print(f"FINDING {name} {detail}".rstrip())


def close(a, b, eps=1e-9):
    return abs(float(a) - float(b)) <= eps


def part(pid, k):
    return items[pid]["parts"][k - 1]


def texts(p):
    out = [p.get("question", "")]
    fb = p.get("feedback", {})
    out += [fb.get("correct", ""), fb.get("generic", "")]
    out += list(fb.get("byKey", {}).values())
    out.append(p.get("explain", {}).get("text", ""))
    for o in p.get("widget", {}).get("options", []):
        out += [o.get("text", ""), o.get("why", "")]
    return " ".join(out)


def band(w):
    return float(w.get("tol", {}).get("abs", 0))


def numeric_part(pid, k, key, places, wrongs, printed=()):
    """key: my value; places: decimals asked (None if exact); wrongs: id -> my value."""
    p = part(pid, k)
    w = p["widget"]
    tag = f"{pid}[{k}]"
    check(f"{tag} key", close(w["answer"], key, 1e-6), f"file {w['answer']} mine {float(key):.6f}")
    tol = band(w)
    if places is not None:
        r = round(float(key), places)
        check(f"{tag} takes the rounding to {places} dp", abs(r - w["answer"]) <= tol + 1e-12, f"{r}")
        # no rounding tie at the asked places
        frac = abs(float(key)) * 10 ** places
        check(f"{tag} no rounding tie", abs((frac % 1) - 0.5) > 1e-6)
        check(f"{tag} band no wider than one unit of the last place", tol <= 10 ** (-places) + 1e-12, f"tol {tol}")
    ids = {x["id"]: x for x in w.get("wrong", [])}
    check(f"{tag} wrong ids", set(ids) == set(wrongs), f"file {sorted(ids)} mine {sorted(wrongs)}")
    for wid, val in wrongs.items():
        if wid not in ids:
            continue
        x = ids[wid]
        check(f"{tag} wrong {wid}", close(x["value"], val, 1e-6), f"file {x['value']} mine {float(val):.6f}")
        gap = abs(x["value"] - w["answer"])
        check(f"{tag} wrong {wid} refused by the key", gap > tol + band(x) + 1e-12, f"gap {gap}")
        check(f"{tag} wrong {wid} has its own feedback", wid in p["feedback"].get("byKey", {}))
        if places is not None:
            rv = round(float(val), places)
            check(f"{tag} wrong {wid} takes its own rounding", abs(rv - x["value"]) <= band(x) + 1e-12)
    vals = sorted((x["value"], band(x)) for x in ids.values())
    for (a, ta), (b, tb) in zip(vals, vals[1:]):
        check(f"{tag} slip bands apart", b - a > ta + tb + 1e-12, f"{a} {b}")
    t = texts(p)
    for s in printed:
        check(f"{tag} prints {s}", s in t)
    q = p["question"]
    stated = bool(re.search(r"decimal|whole number|fraction|nearest|exact", q))
    check(f"{tag} states the form of its answer", stated, "no form sentence in the question")
    return p


# ---------------------------------------------------------------- p-band-wait
# Retargeted in the session AF fix pass: p-tracking-review was re-authored as p-band-wait
# (X = 30 + 2W in pips, exit at 0 or 50). The reader's routes are kept: Gaussian conditional
# moments for the cubic martingale, the boundary-value problems for E[tau] and E[tau; top],
# and the closed form (L^2 - x0^2) / (3 s^2). The old checks of p-tracking-review are removed.
sig, x0, L = 2, 30, 50
s2 = sig * sig
xs = sp.symbols("xs")

# Part 1. Harmonic function h(x) = x / 50 gives P; E[X^3] = 50^3 P.
hfun = xs / sp.Integer(L)
P = F(x0, L)
check("band P = 3/5 from the harmonic function", sp.Rational(3, 5) == hfun.subs(xs, x0) and P == F(3, 5))
EX3 = L**3 * P
numeric_part("p-band-wait", 1, EX3, None,
             {"start-cube": x0**3, "swapped": L**3 * (1 - P), "sure-top": L**3},
             printed=["75{,}000", "30/50 = 0.6"])

# Part 2. E[(x + s sqrt(h) Z)^3 | x] = x^3 + 3 x s^2 h: c = 3 s^2 = 12 keeps the mean.
x_, h_, t_ = sp.symbols("x h t", positive=True)
z = sp.symbols("z")
dens = sp.exp(-z**2 / 2) / sp.sqrt(2 * sp.pi)
cube_mean = sp.integrate((x_ + sig * sp.sqrt(h_) * z) ** 3 * dens, (z, -sp.oo, sp.oo))
gain = sp.simplify(cube_mean - 12 * (t_ + h_) * x_ - (x_**3 - 12 * t_ * x_))
check("band cubic martingale keeps its conditional mean at c = 12", gain == 0, str(gain))
# E[tau; top] from (1/2) s^2 w'' = -h, w(0) = w(50) = 0; then E[tau X_tau] = 50 A
w = sp.Function("w")
solA = sp.dsolve(sp.Eq(sp.Integer(s2) / 2 * w(xs).diff(xs, 2), -hfun), w(xs), ics={w(0): 0, w(L): 0}).rhs
A = sp.nsimplify(solA.subs(xs, x0))
check("band A = 80 by the weighted problem", A == 80, str(A))
EtX = L * A
check("band cubic route agrees", F(EX3 - x0**3, 12) == EtX)
numeric_part("p-band-wait", 2, EtX, None,
             {"no-half": F(EX3 - x0**3, 24), "sigma-unsquared": F(EX3 - x0**3, 6),
              "no-start": F(EX3, 12), "unit-c": F(EX3 - x0**3, 3)},
             printed=["48{,}000/12 = 4{,}000", "27{,}000"])
check("band part 2 states the optional-stopping condition",
      "stays between 0 and 50" in part("p-band-wait", 2)["question"] and "is finite" in part("p-band-wait", 2)["question"])

# Part 3. A = E[tau X_tau] / 50.
numeric_part("p-band-wait", 3, A, None, {"squared-level": F(int(EtX), L**2), "no-divide": EtX},
             printed=["A = 80"])

# Part 4. Closed form (L^2 - x0^2)/(3 s^2) and A / P.
up = F(L**2 - x0**2, 3 * s2)
check("band top wait, closed form 400/3", up == F(400, 3) and sp.Rational(400, 3) == A / sp.Rational(3, 5))
check("band printed working 80/0.6 rounds to 133.33", round(80 / 0.6, 2) == 133.33)
numeric_part("p-band-wait", 4, up, 2, {"times-p": A * sp.Rational(3, 5), "joint": A, "swapped": A / sp.Rational(2, 5)},
             printed=["133.33", "1{,}600/12"])

# Part 5. E[tau] from (1/2) s^2 u'' = -1; floor wait by the reflected closed form.
u = sp.Function("u")
Etau = sp.nsimplify(sp.dsolve(sp.Eq(sp.Integer(s2) / 2 * u(xs).diff(xs, 2), -1), u(xs), ics={u(0): 0, u(L): 0}).rhs.subs(xs, x0))
check("band E[tau] = 150 from the boundary-value problem", Etau == 150, str(Etau))
down = F(L**2 - (L - x0) ** 2, 3 * s2)
check("band floor wait, closed form 175", down == 175 and sp.Rational(175) == (Etau - A) / sp.Rational(2, 5))
numeric_part("p-band-wait", 5, down, None,
             {"wrong-weight": (150 - F(400, 3)) / F(2, 5), "no-condition": 150 - 80, "top-chance": F(70) / F(3, 5)},
             printed=["70/0.4 = 175", "133.33"])
check("band drift of X^3 is 12X, positive inside the band", sp.expand(cube_mean.diff(h_)) == 12 * x_)
check("band far edge slower than the near one", up < Etau < down)

# ---------------------------------------------------------------- p-two-date-product
S0, r, sg = 50.0, 0.03, 0.30
nodes, wts = np.polynomial.hermite_e.hermegauss(80)
wts = wts / math.sqrt(2 * math.pi)
Z1, Z2 = np.meshgrid(nodes, nodes, indexing="ij")
W2 = np.outer(wts, wts)
l1 = math.log(S0) + (r - sg**2 / 2) + sg * Z1          # ln S_1
l2 = l1 + (r - sg**2 / 2) + sg * Z2                    # ln S_2, an independent second year
E = lambda g: float((W2 * g).sum())
m1, m2 = E(l1), E(l2)
cov = E((l1 - m1) * (l2 - m2))
var_sum = E((l1 + l2 - m1 - m2) ** 2)
check("product Cov(ln S1, ln S2) = 0.09 by quadrature", close(cov, 0.09, 1e-9), str(cov))
check("product Var of the sum = 0.45 by quadrature", close(var_sum, 0.45, 1e-9), str(var_sum))
check("product mean of the sum = 2 ln 50 - 0.045", close(m1 + m2, 2 * math.log(50) - 0.045, 1e-9))
check("product 3(r - sigma^2/2) = -0.045", close(3 * (r - sg**2 / 2), -0.045, 1e-12))
numeric_part("p-two-date-product", 1, 0.09, 2,
             {"later-time": sg**2 * 2, "independent": 0, "unsquared": sg * 1}, printed=["0.09"])
numeric_part("p-two-date-product", 2, 0.45, 2,
             {"no-cov": 0.09 + 0.18, "cov-once": 0.09 + 0.18 + 0.09, "later-time": 0.09 + 0.18 + 2 * 0.18},
             printed=["0.45", "0.18"])

mean_payoff = E(np.exp(l1 + l2)) / 100
check("product E_Q[S1 S2 / 100] = 25 e^0.18 by quadrature", close(mean_payoff, 25 * math.exp(0.18), 1e-8), str(mean_payoff))
# tower rule: E[S1 E[S2 | S1]] = e^r E[S1^2], a one-dimensional quadrature
tower = math.exp(r) * float((wts * np.exp(2 * (math.log(S0) + (r - sg**2 / 2) + sg * nodes))).sum()) / 100
check("product tower rule agrees", close(tower, mean_payoff, 1e-8))
numeric_part("p-two-date-product", 3, mean_payoff, 2,
             {"no-cov": 25 * math.exp(-0.045 + 0.27 / 2),
              "r-drift": 25 * math.exp(3 * r + 0.45 / 2),
              "no-half": 25 * math.exp(-0.045 + 0.45)},
             printed=["29.93", "25e^{0.18}", "0.225"])
check("product no-cov is 25 e^0.09 as its line says", close(25 * math.exp(-0.045 + 0.135), 25 * math.exp(0.09)))
price = math.exp(-2 * r) * mean_payoff
fwd1, fwd2 = E(np.exp(l1)), E(np.exp(l2))
check("product each price has mean equal to its forward",
      close(fwd1, S0 * math.exp(r), 1e-8) and close(fwd2, S0 * math.exp(2 * r), 1e-8))
check("product earns e^0.09 over the forwards", close(mean_payoff / (fwd1 * fwd2 / 100), math.exp(0.09), 1e-9))
forwards = math.exp(-2 * r) * fwd1 * fwd2 / 100
numeric_part("p-two-date-product", 4, price, 2,
             {"forwards": forwards, "one-year": math.exp(-r) * mean_payoff, "undiscounted": mean_payoff},
             printed=["28.19", "25e^{0.12}", "25.76", "2.43"])
check("product price is 25 e^0.12", close(price, 25 * math.exp(0.12), 1e-8))
check("product forwards slip is 25 e^0.03 as its line says", close(forwards, 25 * math.exp(0.03), 1e-8))
check("product printed gap 2.43", round(price - forwards, 2) == 2.43 and round(round(price, 2) - round(forwards, 2), 2) == 2.43)
for k in (3, 4):
    check(f"product part {k} unit is pounds", part("p-two-date-product", k)["widget"].get("unit") == "£")

# ---------------------------------------------------------------- p-dividend-hedge
rr, q, S, T = 0.045, 0.02, 120.0, 0.75
p1 = part("p-dividend-hedge", 1)
opts = {o["id"]: o for o in p1["widget"]["options"]}
check("dividend part 1 one correct option", [o["id"] for o in p1["widget"]["options"] if o.get("correct")] == ["with-yield"])

# Numerical book: V = S^2 e^{g (T - t)} is a test claim with V_SS != 0. Take the
# dt coefficient of -dV + V_S dS + q V_S S dt from Ito terms built by finite differences.
mu, sv, g = 0.11, 0.27, 0.07
Vt_ = lambda t, s: s**2 * math.exp(g * (1.0 - t))
t0, s0, hh = 0.3, 95.0, 1e-3
Vt_fd = (Vt_(t0 + hh, s0) - Vt_(t0 - hh, s0)) / (2 * hh)
Vs_fd = (Vt_(t0, s0 + hh) - Vt_(t0, s0 - hh)) / (2 * hh)
Vss_fd = (Vt_(t0, s0 + hh) - 2 * Vt_(t0, s0) + Vt_(t0, s0 - hh)) / hh**2
book_dt = -(Vt_fd + mu * s0 * Vs_fd + 0.5 * sv**2 * s0**2 * Vss_fd) + Vs_fd * mu * s0 + q * s0 * Vs_fd
cand = {
    "with-yield": -Vt_fd - 0.5 * sv**2 * s0**2 * Vss_fd + q * s0 * Vs_fd,
    "no-yield": -Vt_fd - 0.5 * sv**2 * s0**2 * Vss_fd,
    "mu-kept": -Vt_fd - mu * s0 * Vs_fd - 0.5 * sv**2 * s0**2 * Vss_fd + q * s0 * Vs_fd,
    "gamma-sign": -Vt_fd + 0.5 * sv**2 * s0**2 * Vss_fd + q * s0 * Vs_fd,
}
check("dividend part 1 option ids", set(opts) == set(cand))
for oid, val in cand.items():
    same = close(val, book_dt, 1e-6)
    check(f"dividend part 1 option {oid}", same == (oid == "with-yield"), f"{val} vs {book_dt}")

# Part 2: the bracket. Equate the coefficient with r(-V + S V_S) and read the S V_S coefficient.
# with-yield = -rV + r S V_S  =>  V_t + (r - q) S V_S + (1/2) s^2 S^2 V_SS - rV = 0.
rs, qs = sp.symbols("r q")
Vt_s, SVs, G, Vv = sp.symbols("Vt SVs G V")
eqn = sp.expand(-((-Vt_s - G + qs * SVs) - (-rs * Vv + rs * SVs)))
check("dividend part 2 bracket is r - q", sp.simplify(eqn.coeff(SVs) - (rs - qs)) == 0, str(eqn))
check("dividend part 2 other terms", eqn.coeff(Vt_s) == 1 and eqn.coeff(G) == 1 and eqn.coeff(Vv) == -rs)
p2 = part("p-dividend-hedge", 2)
check("dividend part 2 key", sp.simplify(sp.sympify(p2["widget"]["answer"]) - (rs - qs)) == 0)
for acc in p2["widget"]["accept"]:
    check(f"dividend part 2 accept {acc}", sp.simplify(sp.sympify(acc) - (rs - qs)) == 0)
want = {"plus": rs + qs, "no-yield": rs, "sign": qs - rs}
got = {x["id"]: x["tex"] for x in p2["widget"]["wrong"]}
check("dividend part 2 wrong ids", set(got) == set(want))
for wid, ex in want.items():
    if wid in got:
        check(f"dividend part 2 wrong {wid}", sp.simplify(sp.sympify(got[wid]) - ex) == 0)
        check(f"dividend part 2 wrong {wid} differs from the key", sp.simplify(ex - (rs - qs)) != 0)
        check(f"dividend part 2 wrong {wid} has feedback", wid in p2["feedback"]["byKey"])

# Part 3: V = S e^{-q (T - t)}; finite differences and the residual of the equation.
V = lambda t, s: s * math.exp(-q * (T - t))
d = 1e-5
V0 = V(0.0, S)
Vt3 = (V(d, S) - V(-d, S)) / (2 * d)
Vs3 = (V(0.0, S + d) - V(0.0, S - d)) / (2 * d)
Vss3 = (V(0.0, S + 1.0) - 2 * V0 + V(0.0, S - 1.0))
check("dividend V = 118.2134", round(V0, 4) == 118.2134, str(V0))
check("dividend V_S = e^{-q(T - t)} and V_SS = 0", close(Vs3, math.exp(-q * T), 1e-8) and abs(Vss3) < 1e-9)
check("dividend residual of the equation with r - q", abs(Vt3 + (rr - q) * S * Vs3 - rr * V0) < 1e-6)
check("dividend residual with r alone is not zero", abs(Vt3 + rr * S * Vs3 - rr * V0) > 1.0)
# a holder of e^{-qT} shares who reinvests each dividend ends with one share
n = 750000
shares = math.exp(-q * T) * (1 + q * T / n) ** n
check("dividend reinvested holding ends at one share", close(shares, 1.0, 1e-6), str(shares))
numeric_part("p-dividend-hedge", 3, Vt3, 4,
             {"plus": rr * V0 - (rr + q) * S * Vs3, "no-yield": rr * V0 - rr * S * Vs3, "no-discount": q * S},
             printed=["118.2134", "2.3643", "120e^{-0.015}"])
check("dividend printed working 0.02 x 118.2134 inside the key band",
      abs(0.02 * 118.2134 - part("p-dividend-hedge", 3)["widget"]["answer"]) <= 5e-5)
check("dividend V_t > 0: the claim gains value with time", Vt3 > 0)

# Part 4: forward price. Value 0 gives K = V e^{rT}; and E_Q[S_T] with drift r - q by quadrature.
K = V0 * math.exp(rr * T)
sgm = 0.25  # any volatility: the mean does not depend on it
ES = float((wts * S * np.exp((rr - q - sgm**2 / 2) * T + sgm * math.sqrt(T) * nodes)).sum())
check("dividend forward price equals E[S_T] at drift r - q", close(K, ES, 1e-7), f"{K} {ES}")
check("dividend K = 120 e^0.01875", close(K, 120 * math.exp(0.01875), 1e-9))
check("dividend exponents 0.03375 and 0.025 x 0.75", close(rr * T, 0.03375, 1e-12) and close((rr - q) * T, 0.01875, 1e-12))
check("dividend value of the forward at K is 0", abs(V0 - K * math.exp(-rr * T)) < 1e-9)
numeric_part("p-dividend-hedge", 4, K, 2,
             {"prepaid": V0, "no-yield": S * math.exp(rr * T), "plus": S * math.exp((rr + q) * T)},
             printed=["122.27", "118.2134", "e^{0.03375}", "120e^{0.01875}"])
check("dividend printed working 118.2134 e^0.03375 inside the key band",
      abs(118.2134 * math.exp(0.03375) - part("p-dividend-hedge", 4)["widget"]["answer"]) <= 0.005)
check("dividend part 4 unit is pounds", part("p-dividend-hedge", 4)["widget"].get("unit") == "£")
check("dividends lower the forward", K < S * math.exp(rr * T))

# ---------------------------------------------------------------- shape of the set
check("three problems", len(data["items"]) == 3)
check("thirteen parts", sum(len(it["parts"]) for it in data["items"]) == 13)
typed = sum(1 for it in data["items"] for p in it["parts"] if p["widget"]["kind"] in ("numeric", "expression"))
check("typed parts at least two thirds", typed * 3 >= 13 * 2)
check("one problem of difficulty 5", any(it["difficulty"] == 5 for it in data["items"]))
for it in data["items"]:
    for k, p in enumerate(it["parts"], 1):
        ex = p["explain"]["text"]
        n_sent = len(re.findall(r"[.?](?:\s|$)", re.sub(r"\$[^$]*\$", "M", ex)))
        check(f"{it['id']}[{k}] explain at most three sentences", n_sent <= 3, str(n_sent))

print(f"{n_checks - n_fail} of {n_checks} checks passed; {n_fail} FINDING line(s)")
raise SystemExit(0)
