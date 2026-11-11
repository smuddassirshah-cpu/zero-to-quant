#!/usr/bin/env python3
"""Concept audit, round 2, odes level 4 (l14 to l18, review-4, homework-4).

Run from the repo root: python3 docs/reports/odes-L4-concepts-r2.py
Exit 0 when every check passes. A check that fails because the content is
wrong stays failing until the content is fixed (FINDING checks, one per
finding where a string can be tested).

Environment used by the auditor: CPython 3.13, NumPy 2.2.6, SciPy 1.14.1
(the app runs Pyodide 0.27.7, NumPy 2.0.2, SciPy 1.14.1). SciPy checks are
skipped with a note if SciPy is missing.
"""
import contextlib
import io
import json
import math
import os
import sys

import numpy as np

try:
    from scipy.integrate import solve_ivp  # noqa: F401
    HAVE_SCIPY = True
except Exception:  # pragma: no cover
    HAVE_SCIPY = False

ROOT = os.path.join("app", "content", "courses", "odes")
FAILS = []
COUNT = [0]


def check(name, ok, detail=""):
    COUNT[0] += 1
    if not ok:
        FAILS.append(name)
    print(("ok   " if ok else "FAIL ") + name + ((" | " + str(detail)) if detail and not ok else ""))


def load(name):
    with open(os.path.join(ROOT, name + ".json")) as fh:
        return json.load(fh)


L14 = load("l14-laplace-transform")
L15 = load("l15-solving-with-laplace")
L16 = load("l16-euler-method")
L17 = load("l17-runge-kutta")
L18 = load("l18-four-decimal-places")
REV = load("review-4")
HW = load("homework-4")


def close(a, b, tol):
    return abs(a - b) <= tol


# ---------------------------------------------------------------- code widgets
def compare(got, test):
    """Mirror of the engine judge: expect is a Python literal held as a string."""
    kind = test.get("compare", "equal")
    exp = test["expect"]
    if isinstance(exp, str):
        exp = eval(exp, {})
    if kind == "equal":
        return got == exp
    tol = test.get("tol", {}).get("abs")

    def one(g, e):
        if tol is not None:
            return abs(g - e) <= tol
        return abs(g - e) <= 1e-9 * max(abs(g), abs(e))
    if isinstance(exp, list):
        return len(got) == len(exp) and all(one(g, e) for g, e in zip(got, exp))
    return one(got, exp)


def run_tests(widget, code):
    """Return (passed, total) for the widget's hidden tests against code."""
    ns = {}
    try:
        exec(widget.get("prelude", ""), ns)
        exec(code, ns)
    except Exception:
        return 0, len(widget["tests"]), ns
    passed = 0
    for t in widget["tests"]:
        try:
            if t.get("setup"):
                exec(t["setup"], ns)
            if t.get("compare") == "raises":
                try:
                    eval(t["call"], ns)
                except Exception as exc:
                    passed += type(exc).__name__ == t["expect"]
                continue
            passed += bool(compare(eval(t["call"], ns), t))
        except Exception:
            pass
    return passed, len(widget["tests"]), ns


def code_widgets(doc):
    for key in ("screens", "items"):
        for i, sc in enumerate(doc.get(key, [])):
            w = sc.get("widget", {})
            if w.get("kind") == "code":
                yield "%s.%s[%d]" % (doc["id"], key, i), sc, w


def console_check(tag, lines, ns, skip=()):
    """Run each '>>> ' line; compare the printed output with the next line."""
    i = 0
    while i < len(lines):
        ln = lines[i]
        if not ln.startswith(">>> "):
            i += 1
            continue
        src = ln[4:]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src, "<console>", "single"), ns)
            out = buf.getvalue().strip()
        except Exception as exc:
            out = "%s: %s" % (type(exc).__name__, exc)
        nxt = lines[i + 1] if i + 1 < len(lines) and not lines[i + 1].startswith(">>> ") else None
        if nxt is not None and i not in skip:
            if nxt.endswith("..."):
                ok = out.startswith(nxt[:-3])
            else:
                ok = out == nxt
            check("%s console: %s -> %s" % (tag, src[:48], nxt[:40]), ok, "got " + out)
        i += 1


NS = {}
for doc in (L14, L15, L16, L17, L18, HW):
    lesson_ns = {}
    for tag, sc, w in code_widgets(doc):
        needs_scipy = "scipy" in w["solution"]
        if needs_scipy and not HAVE_SCIPY:
            print("skip " + tag + " (no SciPy)")
            continue
        p, n, ns = run_tests(w, w["solution"])
        check("%s solution passes %d/%d hidden tests" % (tag, p, n), p == n)
        p0, n0, _ = run_tests(w, w["starter"])
        check("%s starter fails the hidden tests (%d/%d pass)" % (tag, p0, n0), p0 < n0)
        how = w.get("how", "")
        words = {4: "4", 7: "7", 8: "8", 9: "9"}
        check("%s 'how' states the real test count %d" % (tag, n), ("runs %s hidden" % words.get(n, str(n))) in how)
        lesson_ns.update(ns)
        cv = sc.get("canvas", {})
        if cv.get("kind") == "console":
            console_check(tag, cv["params"]["lines"], lesson_ns)
    NS[doc["id"]] = lesson_ns

# ---------------------------------------------------------------- l14
ns14 = NS["l14-laplace-transform"]
lap = ns14["laplace_numeric"]
errs14 = [abs(lap(lambda t: np.exp(-t), 1) - 0.5), abs(lap(lambda t: t, 2) - 0.25),
          abs(lap(lambda t: np.sin(3 * t), 1) - 0.3)]
check("l14 s9 feedback: trapezium values within 1e-7 of 0.5, 0.25, 0.3", max(errs14) < 1e-7, errs14)
check("l14 s9 explain: accuracy about 1e-8", 3e-9 < max(errs14) < 3e-8, errs14)
# Euler-Maclaurin: error = h^2/12 (g'(T) - g'(0)); for t e^{-2t}, g'(0) = 1
h14 = 50 / 200000
check("l14 s9 trapezium error matches h^2/12 by Euler-Maclaurin", close(0.25 - lap(lambda t: t, 2), h14 ** 2 / 12, 1e-11))
tails = [math.exp(-100) / 2, math.exp(-100) * (25 + 0.25), math.exp(-50), math.exp(-50) * (2500 + 100 + 2)]
check("l14 s9 explain: cut at T = 50 costs below 1e-18", max(tails) < 1e-18, tails)
check("l14 s0: perpetuity 1/0.04 = 25", close(1 / 0.04, 25, 1e-12))
check("l14 s4: F(1) column 2, 0.3, 0.2", close(3 / 10, 0.3, 1e-12) and close(1 / 5, 0.2, 1e-12))
check("l14 s5: Gordon 5/(0.06-0.02) = 125; product slip = -50,000",
      close(5 / 0.04, 125, 1e-9) and close((5 / 0.01) * (1 / (0.01 - 0.02)), -50000, 1e-6))
check("l14 s6 option c: 10! / s^11 by numeric transform at s = 2",
      close(lap(lambda t: t ** 10, 2, T=80, n=400000), math.factorial(10) / 2 ** 11, 1e-6))
check("l14 s8: shifted cosine at s = 1 by numeric transform",
      close(lap(lambda t: np.exp(-t) * np.cos(2 * t), 1), 2 / (4 + 4), 1e-6))
check("l14 s10: default claim 100*0.02/0.06 = 33.33; no-shift slip 50", close(100 * 0.02 / 0.06, 33.33, 0.01))
check("l14 quiz: 0.5, 0.125, 0.12, 0.16", close(1 / 8, 0.125, 0) and close(3 / 25, 0.12, 1e-12) and close(4 / 25, 0.16, 1e-12))

# ---------------------------------------------------------------- l15
ns15 = NS["l15-solving-with-laplace"]
inv = ns15["inverse_laplace"]
check("l15 s1: y(1) = 2 - 2e^-2 = 1.7293; slip 1.2642", close(2 - 2 * math.exp(-2), 1.7293, 5e-5) and close(2 - 2 * math.exp(-1), 1.2642, 5e-5))
check("l15 s2: partial fractions 0.04/s + 0.02/(s+0.5)", close(inv([0.06, 0.02], [1, 0.5, 0], 2.0), 0.04 + 0.02 * math.exp(-1), 1e-12))
p3, r3 = ns15["residues"]([2], [1, 3, 2, 0])
check("l15 s3: residues 1, -2, 1 at 0, -1, -2",
      all(close(float(np.real(r3[int(np.argmin(abs(p3 - q)))])), v, 1e-9) for q, v in ((0, 1), (-1, -2), (-2, 1))))
check("l15 s3 explain: y(1) = 0.399576", close(1 - 2 * math.exp(-1) + math.exp(-2), 0.399576, 5e-7))
y7 = lambda t: math.exp(-t) * (math.cos(2 * t) + 0.5 * math.sin(2 * t))
check("l15 s4: y(1) = 0.014164", close(y7(1), 0.014164, 5e-7))
# verify y solves y'' + 2y' + 5y = 0, y(0) = 1, y'(0) = 0 by finite differences
d = 1e-4
res = (y7(1 + d) - 2 * y7(1) + y7(1 - d)) / d ** 2 + 2 * (y7(1 + d) - y7(1 - d)) / (2 * d) + 5 * y7(1)
check("l15 s4: e^-t(cos 2t + sin 2t / 2) solves the oscillator from (1, 0)",
      abs(res) < 1e-5 and close(y7(0), 1, 0) and abs((y7(d) - y7(-d)) / (2 * d)) < 1e-6)
check("l15 s5 option d: sin-only solution is from y(0) = 0, y'(0) = 1",
      close(inv([1], [1, 2, 5], 0.7), 0.5 * math.exp(-0.7) * math.sin(1.4), 1e-12))
check("l15 s9: R(0.05) = 0.8364", close(0.04 / 0.05 + 0.02 / 0.55, 0.8364, 5e-5))
check("l15 quiz q-cover: 1/3 and -1/3", close(1 / (1 + 2), 0.3333, 5e-4) and close(1 / (-2 - 1), -0.3333, 5e-4))

# ---------------------------------------------------------------- l16
ns16 = NS["l16-euler-method"]
euler = ns16["euler"]
order = ns16["observed_order"]
eerr = lambda h: math.e - (1 + h) ** round(1 / h)
check("l16 s0/s1: 2.25, 2.4414, gaps 0.47 and 0.28",
      close(1.5 ** 2, 2.25, 0) and close(1.25 ** 4, 2.4414, 5e-5) and close(math.e - 2.25, 0.47, 0.005) and close(math.e - 1.25 ** 4, 0.28, 0.005))
check("l16 s2: monthly 1.051162 against 1.051271", close((1 + 0.05 / 12) ** 12, 1.051162, 5e-7) and close(math.exp(0.05), 1.051271, 5e-7))
check("l16 s3 prose: errors 0.124539, 0.064984, 0.013468", close(eerr(0.1), 0.124539, 5e-7) and close(eerr(0.05), 0.064984, 5e-7) and close(eerr(0.01), 0.013468, 5e-7))
pts = {p["x"]: p["y"] for p in L16["screens"][3]["canvas"]["state"]["points"]}
check("l16 s3 canvas points are the Euler errors", all(close(eerr(h), y, 1e-9) for h, y in pts.items()), pts)
check("l16 s3: ratio 1.92, fitted slope 0.964", close(eerr(0.1) / eerr(0.05), 1.92, 0.005) and close(order([eerr(h) for h in pts], list(pts)), 0.964, 5e-4))
vas = lambda h: 0.04 + 0.02 * (1 - 0.5 * h) ** round(1 / h)
steps = [0.04 + 0.02 * 0.875 ** k for k in range(1, 5)]
check("l16 s4: 5.75%, 5.5313%, 5.3398%, 5.1724%, exact 5.2131%, monthly 5.2001%",
      all(close(100 * a, b, 5.1e-5) for a, b in zip(steps, (5.75, 5.5313, 5.3398, 5.1724)))
      and close(100 * (0.04 + 0.02 * math.exp(-0.5)), 5.2131, 5e-5) and close(100 * vas(1 / 12), 5.2001, 5e-5))
ex4 = 0.04 + 0.02 * math.exp(-0.5)
check("l16 s4 explain: monthly error about a third of quarterly", 0.28 < (ex4 - vas(1 / 12)) / (ex4 - vas(0.25)) < 0.38)
t5, z5 = euler(lambda t, z: np.array([z[1], -z[0]]), 0, np.array([1.0, 0.0]), 0.1, 63)
cp = L16["screens"][5]["canvas"]["params"]["functions"][1]["points"]
check("l16 s5 canvas: 64 Euler points match the taught code", len(cp) == 64 and np.max(np.abs(np.array(cp) - z5)) < 6e-5)
check("l16 s5: radius 1.3681 = sqrt(1.01)^63; slip 1.8717", close(float(np.hypot(*z5[-1])), 1.3681, 1e-4) and close(1.01 ** 63, 1.8717, 1e-4))
check("l16 s5: 63 steps of 0.1 is about one turn", abs(63 * math.atan(0.1) - 2 * math.pi) < 0.01)
s6 = L16["screens"][6]["canvas"]["params"]["series"]
check("l16 s6 chart: true and Euler series", all(close(math.exp(-2.5 * k), v, 5.1e-5) for k, v in enumerate(s6[0]["values"]))
      and all(close((-1.5) ** k, v, 0) for k, v in enumerate(s6[1]["values"])))
check("l16 s6 explain: e^-10 = 0.0000454", close(math.exp(-10), 0.0000454, 5e-8))
check("l16 s9: loan 93,816.35 (formula), 93,832.22 (monthly), gap 15.87",
      close(200000 - 100000 * math.exp(0.06), 93816.35, 0.005) and close(200000 - 100000 * 1.005 ** 12, 93832.22, 0.005)
      and close(100000 * (math.exp(0.06) - 1.005 ** 12), 15.87, 0.005))
check("l16 quiz q-step slip 1.1222 (slope at the end), q-order 0.027 and 0.013468",
      close(1.01 / 0.9, 1.1222, 5e-5) and close(eerr(0.02), 0.027, 5e-4))

# ---------------------------------------------------------------- l17
ns17 = NS["l17-runge-kutta"]
rk4 = ns17["rk4"]
R = lambda z: 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24
rerr = lambda n: abs(math.e - R(1 / n) ** n)
check("l17 s0: midpoint 1.105; ten steps 2.714081, error 0.004201", close(1.105 ** 10, 2.714081, 5e-7) and close(math.e - 1.105 ** 10, 0.004201, 5e-7))
check("l17 s1: R(0.5) = 1.6484375, squared 2.7173, within 0.001 of e", close(R(0.5), 1.6484375, 1e-12) and close(R(0.5) ** 2, 2.7173, 5e-5) and math.e - R(0.5) ** 2 < 0.001)
check("l17 s2: k values and y1 = 1.1051708", close(1 + 0.1 / 6 * (1 + 2.1 + 2.105 + 1.10525), 1.1051708, 1e-7))
check("l17 s3: errors 2.084e-6 and 1.358e-7, ratio 15.35", close(rerr(10), 2.084e-6, 5e-10) and close(rerr(20), 1.358e-7, 5e-11) and close(rerr(10) / rerr(20), 15.35, 0.01))
p3 = {p["id"]: (p["x"], p["y"]) for p in L17["screens"][3]["canvas"]["state"]["points"]}
check("l17 s3 canvas: Euler and RK4 log10 errors",
      all(close(math.log10(eerr(x)), y, 6e-4) for k, (x, y) in p3.items() if k.startswith("e"))
      and all(close(math.log10(rerr(round(1 / x))), y, 6e-4) for k, (x, y) in p3.items() if k.startswith("k")), p3)
p4 = {p["id"]: (p["x"], p["y"]) for p in L17["screens"][4]["canvas"]["state"]["points"]}
check("l17 s4 canvas: cost points",
      all(close(math.log10(eerr(1 / x)), y, 6e-4) for k, (x, y) in p4.items() if k.startswith("u"))
      and all(close(math.log10(rerr(x // 4)), y, 6e-4) for k, (x, y) in p4.items() if k.startswith("v")), p4)
check("l17 s4: Euler with 100,000 steps errs by 1.36e-5", close(eerr(1e-5), 1.36e-5, 5e-8))
t6, z6 = rk4(lambda t, z: np.array([z[1], -z[0]]), 0, np.array([1.0, 0.0]), 0.1, 63)
kp = L17["screens"][5]["canvas"]["params"]["functions"][1]["points"]
check("l17 s5 canvas: 64 RK4 points match the taught code", len(kp) == 64 and np.max(np.abs(np.array(kp) - z6)) < 6e-5)
modR = abs(R(0.1j))
check("l17 s5: |R(ih)| = 1 - 6.9e-9; radius after 63 steps 0.9999996", close(1 - modR, 6.9e-9, 5e-11) and close(modR ** 63, 0.9999996, 5e-8))


def bad_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h / 2 * k1)
    k3 = f(t + h / 2, y + h / 2 * k1)
    k4 = f(t + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def bad_run(h):
    y = 1.0
    for _ in range(round(1 / h)):
        y = bad_step(lambda t, y: y, 0, y, h)
    return y


hs6 = [0.1, 0.05, 0.025, 0.0125]
ord6 = order([abs(math.e - bad_run(h)) for h in hs6], hs6)
check("l17 s6: slipped step gives 2.71613 and measured order 1.979 (prose 1.98)", close(bad_run(0.1), 2.71613, 5e-6) and close(ord6, 1.979, 5e-4))
Rm = lambda z: R(-z)
lo, hi = 2.5, 3.0
for _ in range(80):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if Rm(mid) < 1 else (lo, mid)
check("l17 s7: R(2.5) = 0.6484, R(3) = 1.375, |R| = 1 at 2.7853", close(Rm(2.5), 0.6484, 5e-5) and close(Rm(3), 1.375, 1e-12) and close(lo, 2.7853, 5e-5))
check("l17 s7: |R| < 1 on the whole of (0, 2.7853)", all(abs(Rm(z)) < 1 for z in np.linspace(1e-6, 2.7852, 20001)))
osc = lambda t, z: np.array([z[1], -2 * z[1] - 5 * z[0]])
EX = y7(1)
eu_err = lambda n: abs(euler(osc, 0, np.array([1.0, 0.0]), 1 / n, n)[1][-1][0] - EX)
check("l17 s9 explain / hw how: Euler needs about 16,000 steps on the oscillator",
      eu_err(15000) > 5e-5 > eu_err(17000), (eu_err(15000), eu_err(17000)))
check("l17 s11: 40/2.7853 = 14.36, so 15 steps; 14 steps give z = 2.857", close(40 / 2.7853, 14.36, 0.005) and close(40 / 14, 2.857, 5e-4))
check("l17 quiz q-step: 0.9048375", close(R(-0.1), 0.9048375, 5e-8))
if HAVE_SCIPY:
    sol = solve_ivp(lambda t, z: [z[1], -2 * z[1] - 5 * z[0]], (0, 1), [1, 0], rtol=1e-10, atol=1e-12)
    e10 = abs(float(sol.y[0, -1]) - EX)
    check("l17 s10 explain: solve_ivp error near 1e-11", 1e-12 < e10 < 1e-10, e10)

# ---------------------------------------------------------------- l18
ns18 = NS["l18-four-decimal-places"]
Dx = ns18["discount_exact"](0.06, 0.5, 0.04, 5)
De = lambda n: ns18["discount_euler"](0.06, 0.5, 0.04, 5, n)
Dk = lambda n: ns18["discount_rk4"](0.06, 0.5, 0.04, 5, n)
check("l18 s0/s1: I(5) = 0.236717, D = 0.789215, bounds 74.08 and 81.87",
      close(-math.log(Dx), 0.236717, 5e-7) and close(Dx, 0.789215, 5e-7) and close(100 * math.exp(-0.3), 74.08, 0.005) and close(100 * math.exp(-0.2), 81.87, 0.005))
check("l18 s1: (1 - e^-2.5)/0.5 = 1.835830", close((1 - math.exp(-2.5)) / 0.5, 1.835830, 5e-7))
cap = lambda n: math.exp(-(0.2 + 0.04 * (1 - (1 - 2.5 / n) ** n)))
check("l18 s2 caption formula equals Euler on the system", all(close(cap(n), De(n), 1e-12) for n in (1, 2, 4, 10, 60, 100, 1000)))
check("l18 s2: D_10 = 0.788402, D_100 = 0.789134, D_1000 = 0.789207", close(De(10), 0.788402, 5e-7) and close(De(100), 0.789134, 5e-7) and close(De(1000), 0.789207, 5e-7))
check("l18 s3: error 50.02 at 162, 49.71 at 163; 163 is the smallest n",
      close(1e6 * (Dx - De(162)), 50.02, 0.005) and close(1e6 * (Dx - De(163)), 49.71, 0.005)
      and min(n for n in range(3, 400) if abs(Dx - De(n)) < 5e-5) == 163)
rows = L18["screens"][4]["canvas"]["params"]["rows"]
check("l18 s4 table: RK4 D_n and errors", all(close(Dk(int(r[0])), float(r[1]), 5e-7) and close(1e6 * abs(Dk(int(r[0])) - Dx), float(r[2]), 0.6 if float(r[2]) > 100 else 0.06) for r in rows),
      [(n, Dk(n), 1e6 * abs(Dk(n) - Dx)) for n in (1, 2, 4, 8)])
check("l18 s4 explain: ten steps err by 2.6e-7", close(abs(Dk(10) - Dx), 2.6e-7, 5e-9), abs(Dk(10) - Dx))
rk_min = min(n for n in range(1, 20) if abs(Dk(n) - Dx) < 5e-5)
print("     note: smallest n with RK4 inside the band = %d (error at n = 3: %.1fe-6)" % (rk_min, 1e6 * abs(Dk(3) - Dx)))
check("l18 s4 explain / summary: 'RK4 needs 4' is the true minimum, as Euler's 163 is", rk_min == 4, rk_min)
p5 = {p["x"]: p["y"] for p in L18["screens"][5]["canvas"]["state"]["points"]}
check("l18 s5 chart: Euler errors for n = 2..32", all(close(1e6 * abs(Dx - De(n)), y, 0.06) for n, y in p5.items()), [(n, 1e6 * (Dx - De(n))) for n in p5])
check("l18 s5: 2 steps overshoot below 4% (r_1 = 3.5%)", close(0.04 + 0.02 * (1 - 1.25), 0.035, 1e-12))
check("l18 s6: monthly D = 0.789080, error 1.35e-4, 1.35p", close(De(60), 0.789080, 5e-7) and close(Dx - De(60), 1.35e-4, 5e-7))
var_coef = (1 / 0.5 ** 2) * (5 - 2 * (1 - math.exp(-2.5)) / 0.5 + (1 - math.exp(-5)) / (2 * 0.5))
check("l18 s7: half Var(I) = 4.643 sigma^2 (Vasicek integrated-rate variance)", close(var_coef / 2, 4.643204, 5e-7), var_coef / 2)
rng = np.random.default_rng(7)
nst, npaths, sig = 250, 200000, 0.01
dt = 5 / nst
r = np.full(npaths, 0.06)
I = np.zeros(npaths)
for _ in range(nst):
    rn = 0.04 + (r - 0.04) * math.exp(-0.5 * dt) + sig * math.sqrt((1 - math.exp(-dt)) / 1.0) * rng.standard_normal(npaths)
    I += 0.5 * (r + rn) * dt
    r = rn
mc = np.exp(-I)
se = mc.std() / math.sqrt(npaths)
check("l18 s7 (Monte Carlo, 200,000 paths): noisy D = 0.789581, above the no-noise 0.789215",
      abs(mc.mean() - 0.789581) < 4 * se and mc.mean() - Dx > 4 * se, (mc.mean(), se))
check("l18 s7: price gap 0.0367", close(100 * Dx * (math.exp(4.643204e-4) - 1), 0.0367, 1e-4))
check("l18 s9 explain: Euler doubling meets the band at 256, not 128", abs(De(128) - Dx) >= 5e-5 > abs(De(256) - Dx))
log = L18["screens"][11]["canvas"]["params"]["lines"]
check("l18 s11 log: RK4 errors 3.9e-04, 1.4e-05, 6.7e-07 and the two runs agree",
      "%.1e" % abs(Dk(2) - Dx) == "3.9e-04" and "%.1e" % abs(Dk(4) - Dx) == "1.4e-05" and "%.1e" % abs(Dk(8) - Dx) == "6.7e-07"
      and abs(Dk(8) - Dk(4)) < 5e-5 and "3.9e-04" in log[1] and "1.4e-05" in log[2] and "6.7e-07" in log[3])
check("l18 quiz: e^-0.25 = 0.7788; band options", close(math.exp(-0.25), 0.7788, 5e-5) and abs(0.789180 - 0.789215) < 5e-5 < abs(0.789290 - 0.789215))

# ---------------------------------------------------------------- review and homework
check("review r-t-cubed 0.375; r-residues 0.6004 and slip 0.8711",
      close(6 / 16, 0.375, 0) and close(2 * math.exp(-1) - math.exp(-2), 0.6004, 5e-5) and close(2 * math.exp(-1) + math.exp(-2), 0.8711, 5e-5))
ev = np.linalg.eigvalsh(np.array([[-2.0, 1.0], [1.0, -2.0]]))
check("review r-system-step: eigenvalues -3 and -1, limit 2/3", close(ev[0], -3, 1e-12) and close(ev[1], -1, 1e-12))
check("review r-monthly: 60 * 1.35/0.5 = 162; second-order slip 99", close(60 * 1.35 / 0.5, 162, 1e-9) and close(60 * math.sqrt(2.7), 99, 0.5))
nsh = NS["homework-4"]
m = nsh["match_to_4dp"]
bond = lambda t, y: np.array([0.5 * (0.04 - y[0]), -y[0] * y[1]])
band = lambda f, y0, T, ex, k: min(n for n in (1, 2, 4, 8, 16, 32) if abs(float(np.atleast_1d(nsh["rk4"](f, 0.0, np.asarray(y0, float), T / n, n)[1][-1])[k]) - ex) < 5e-5)
firsts = (band(bond, [0.06, 1.0], 5, Dx, 1), band(osc, [1.0, 0.0], 1, EX, 0), band(lambda t, y: y, 1.0, 1, math.e, 0))
stops = (m(bond, [0.06, 1.0], 5, Dx, k=1)[0], m(osc, [1.0, 0.0], 1, EX)[0], m(lambda t, y: y, 1.0, 1, np.e)[0])
check("homework h-match-4dp explain: stops one doubling after RK4 first meets the band", all(s == 2 * f for s, f in zip(stops, firsts)), (firsts, stops))
check("homework h-rk4-predict: 20.84/16 = 1.30; true 1.358, ratio 15.35", close(20.84 / 16, 1.30, 0.005))
check("homework h-monthly-note: 4-step and 8-step RK4 runs agree within 5e-5", abs(Dk(8) - Dk(4)) < 5e-5)

# ---------------------------------------------------------------- findings (stay failing until fixed)
tok = open(os.path.join("app", "css", "tokens.css")).read()
slot3_green = "--s3: #1BAF7A" in tok and "--s2: #EB6834" in tok
f5 = {f["id"]: f for f in L17["screens"][5]["canvas"]["params"]["functions"]}
cap5 = L17["screens"][5]["canvas"]["state"]["caption"]
check("FINDING 1 l17 s5 caption: Euler's path (slot %s, green in tokens.css) is not called orange" % f5["E"].get("colour"),
      not (slot3_green and f5["E"].get("colour") == 3 and "Orange: Euler" in cap5), cap5)
s6x = L18["screens"][6]
check("FINDING 2 l18 s6: failure is argued from the band, not from the printed digits",
      "so the fourth decimal is wrong" not in s6x["explain"]["text"] and "fourth decimal of $D$ is wrong" not in s6x["feedback"]["correct"])
p7 = L16["screens"][7]["prose"]
i7 = p7.find("At $h = 0.05$")
check("FINDING 3 l16 s7 prose: the factors 0.5 and 0 are tied to lambda = 10",
      i7 < 0 or "lambda = 10" in p7[max(0, i7 - 40):i7 + 20], p7[max(0, i7 - 40):i7 + 60])
check("FINDING 4 l18 s7 prose: the factor e^(Var/2) is tied to I being normal, not to convexity alone",
      "is normal" in L18["screens"][7]["prose"] or "Gaussian" in L18["screens"][7]["prose"])

print("\n%d checks, %d failed" % (COUNT[0], len(FAILS)))
for f in FAILS:
    print("  failed: " + f)
sys.exit(1 if FAILS else 0)
