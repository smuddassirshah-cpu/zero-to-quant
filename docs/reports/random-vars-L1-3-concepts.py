#!/usr/bin/env python3
"""Concept audit, round 1: random-vars levels 1 to 3 (blind read).

Run from the repo root with no arguments:  python3 docs/reports/random-vars-L1-3-concepts.py

It recomputes the graded keys and stated results the ledger cites with basis E, D or MC
(exact enumeration with fractions, closed forms, seeded Monte Carlo), runs the three
Python widgets against their hidden tests, and holds one failing check per finding
whose text can be tested. It exits 0 only when every check passes, so it exits 1
until the findings in docs/reviews/audit-random-vars-1-3.md are fixed.

Python content was run in CPython (the version is printed), not Pyodide 0.27.7.
"""
import itertools
import json
import math
import random
import sys
from fractions import Fraction as F
from math import comb, isclose, sqrt

ROOT = "app/content/courses/random-vars/"
PASS = FAIL = 0
FAILED = []


def load(name):
    with open(ROOT + name + ".json", encoding="utf-8") as fh:
        return json.load(fh)


def g(obj, path):
    for key in path.split("."):
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj


def chk(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        FAILED.append(name)


def near(a, b, tol=6e-4):
    return abs(float(a) - float(b)) <= tol


def ans(doc, path):
    return g(doc, path + ".widget.answer")


def has(doc, path, text):
    return text in json.dumps(g(doc, path), ensure_ascii=False)


def mean(pmf):
    return sum(x * p for x, p in pmf.items())


def var(pmf):
    m = mean(pmf)
    return sum((x - m) ** 2 * p for x, p in pmf.items())


def pmf_of(space, fn):
    out = {}
    for w, p in space.items():
        out[fn(w)] = out.get(fn(w), 0) + p
    return out


def cells(fn_true):
    return sorted(f"r{a}c{b}" for a in range(1, 7) for b in range(1, 7) if fn_true(a, b))


DICE = {(a, b): F(1, 36) for a in range(1, 7) for b in range(1, 7)}
TOT = pmf_of(DICE, sum)
MAX = pmf_of(DICE, max)
DIE = {k: F(1, 6) for k in range(1, 7)}
L = {i: load(n) for i, n in enumerate([
    "", "l1-number-per-outcome", "l2-listing-chances", "l3-up-to-a-point", "l4-transforming",
    "l5-long-run-average", "l6-fair-price", "l7-linearity", "l8-indicators", "l9-measuring-spread",
    "l10-scaling-and-adding", "l11-moving-together", "l12-diversification"]) if n}
RV = {i: load(f"review-{i}") for i in (1, 2, 3)}
HW = {i: load(f"homework-{i}") for i in (1, 2, 3)}
PB = {i: load(f"problems-{i}") for i in (1, 2, 3)}
FL = load("fluency-l9-measuring-spread")


def run_code(widget, label):
    """Solution passes every hidden test; the starter fails at least one."""
    def run(src):
        ok = 0
        for t in widget["tests"]:
            env = {}
            try:
                exec(src, env)
                if t.get("setup"):
                    exec(t["setup"], env)
                if t.get("compare") == "raises":
                    try:
                        eval(t["call"], env)
                    except Exception as exc:  # noqa: BLE001
                        ok += type(exc).__name__ == t["expect"]
                    continue
                got = eval(t["call"], env)
                want = eval(t["expect"], env)
                if isinstance(want, dict):
                    ok += (isinstance(got, dict) and set(got) == set(want)
                           and all(isclose(float(got[k]), float(want[k]), rel_tol=1e-9, abs_tol=1e-12) for k in want))
                else:
                    ok += isclose(float(got), float(want), rel_tol=1e-9, abs_tol=1e-12)
            except Exception:  # noqa: BLE001
                pass
        return ok
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        n_sol, n_start = run(widget["solution"]), run(widget["starter"])
    chk(f"{label}: solution passes all {len(widget['tests'])} tests", n_sol == len(widget["tests"]))
    chk(f"{label}: starter fails", n_start < len(widget["tests"]))
    chk(f"{label}: stated test count", f"{len(widget['tests'])} hidden tests" in widget["how"])


# ---------------------------------------------------------------- level 1
d = L[1]
chk("l1 s0 total 9", sorted(ans(d, "screens.0")) == cells(lambda a, b: a + b == 9))
chk("l1 s1 max 4", sorted(ans(d, "screens.1")) == cells(lambda a, b: max(a, b) == 4))
chk("l1 s3 gap 1", ans(d, "screens.3") == sum(1 for a, b in DICE if abs(a - b) == 1) == 10)
chk("l1 s3 gap grid", g(d, "screens.3.explain.canvas.cells") == [[str(abs(a - b)) for b in range(1, 7)] for a in range(1, 7)])
chk("l1 s5 P(max 6)", MAX[6] == F(11, 36) and MAX[1] == F(1, 36))
chk("l1 s7 call payoffs", [g(d, f"screens.7.widget.rows.{i}.1.answer") for i in range(5)] == [max(s - 100, 0) for s in (94, 97, 100, 103, 106)])
chk("l1 s8 two fills", sorted(ans(d, "screens.8")) == sorted("-".join(p) for p in itertools.product("fm", repeat=3) if p.count("f") == 2))
chk("l1 q1 P(total>=10)", sum(p for t, p in TOT.items() if t >= 10) == F(1, 6))
chk("l1 q3 values of difference", ans(d, "quiz.3") == len({a - b for a, b in DICE}) == 11)

d = L[2]
chk("l2 s0 pmf 2..7", all(near(g(d, f"screens.0.widget.rows.{i}.1.answer"), TOT[i + 2], 1e-5) for i in range(6)))
chk("l2 s1 exact bars", all(near(e["y"], TOT[int(e["x"])], 6e-5) for e in g(d, "screens.1.canvas.params.exact")))
chk("l2 s2 slip 21/36", near(g(d, "screens.2.widget.wrong.0.value"), sum(TOT[t] for t in range(2, 8)), 1e-4))
coins3 = {"".join(s): F(1, 8) for s in itertools.product("HT", repeat=3)}
heads3 = pmf_of(coins3, lambda s: s.count("H"))
chk("l2 s4 heads pmf", [g(d, f"screens.4.widget.rows.{i}.1.answer") for i in range(4)] == [float(heads3[i]) for i in range(4)])
chk("l2 s6 classmate list adds to 37/36", F(25, 36) + F(11, 36) + F(1, 36) == F(37, 36)
    and sum(1 for a, b in DICE if (a == 6) + (b == 6) == 1) == 10)
day = {2: F(3, 10), 0: F(5, 10), -2: F(2, 10)}
two = pmf_of({(a, b): day[a] * day[b] for a in day for b in day}, sum)
chk("l2 s8 two-day pmf", [g(d, f"screens.8.widget.rows.{i}.1.answer") for i in range(5)] == [float(two[x]) for x in (-4, -2, 0, 2, 4)])
chk("l2 q2 P(max 3)", MAX[3] == F(5, 36))

d = L[3]
Fh = lambda x: sum(p for k, p in heads3.items() if k <= x)  # noqa: E731
steps = g(d, "screens.1.canvas.params.functions")
chk("l3 s1 staircase heights", [eval(s["expr"]) for s in steps] == [float(Fh(x)) for x in (-1, 0, 1, 2, 3)])
chk("l3 s1 right-continuous (closed dot on the upper step)", all(s["endpoints"][0] in (None, "closed") and s["endpoints"][1] in (None, "open") for s in steps))
chk("l3 s2 F(2.4)", ans(d, "screens.2") == float(Fh(2.4)) == 0.875)
chk("l3 s3 P(1<X<=3)", ans(d, "screens.3") == float(Fh(3) - Fh(1)))
chk("l3 s4 P(X>2)", ans(d, "screens.4") == float(1 - Fh(2)))
chk("l3 s5 F_Y(y)=y^2/36", all(sum(p for k, p in MAX.items() if k <= y) == F(y * y, 36) for y in range(1, 7)))
chk("l3 s6 jump at 4", near(ans(d, "screens.6"), MAX[4], 1e-5))
chk("l3 s7 P(2<=Y<=4)=15/36", MAX[2] + MAX[3] + MAX[4] == F(15, 36))
loss = dict(zip([-2, 0, 1, 2, 5, 10, 20], [F(30, 100), F(25, 100), F(20, 100), F(15, 100), F(6, 100), F(3, 100), F(1, 100)]))


def cdf(pmf, x):
    return sum(p for k, p in pmf.items() if k <= x)


def var95(pmf):
    return min(k for k in pmf if cdf(pmf, k) >= F(95, 100))


chk("l3 s9 running totals", [g(d, f"screens.9.widget.rows.{i}.2.answer") for i in range(1, 7)] == [float(cdf(loss, k)) for k in (0, 1, 2, 5, 10, 20)])
chk("l3 s10 VaR 95% is 5", ans(d, "screens.10") == var95(loss) == 5)
chk("l3 q3 P(L>2)", near(ans(d, "quiz.3"), 1 - cdf(loss, 2), 1e-9))

d = L[4]
sq = pmf_of(TOT, lambda t: (t - 7) ** 2)
chk("l4 s0 Y=1 cells", sorted(ans(d, "screens.0")) == cells(lambda a, b: (a + b - 7) ** 2 == 1))
chk("l4 s2 pmf of (X-7)^2", all(near(g(d, f"screens.2.widget.rows.{i}.1.answer"), sq[y], 1e-5) for i, y in enumerate((0, 1, 4, 9, 16, 25))))
dv = {k.split(".")[1]: v for k, v in g(d, "screens.1.canvas.derive").items() if k.startswith("values.")}
cond, rest = dv["0"].split("?")
dv["0"] = f"({rest.split(':')[0]}) if ({cond}) else ({rest.split(':')[1]})"   # the JS ternary, in Python
ok = len(dv) == 11
for K in range(2, 13):
    pay = pmf_of(TOT, lambda t: max(t - K, 0))
    for y in range(11):
        ok &= near(eval(dv[str(y)], {"K": K, "max": max, "abs": abs}), pay.get(y, 0), 1e-12)
chk("l4 s1 slider formulas match enumeration for K=2..12", ok)
ab = pmf_of(two, abs)
chk("l4 s3 pmf of |X|", [g(d, f"screens.3.widget.rows.{i}.1.answer") for i in range(3)] == [float(ab[y]) for y in (0, 2, 4)])
call = pmf_of(two, lambda x: max(x, 0))
chk("l4 s7 call pmf", [g(d, f"screens.7.widget.rows.{i}.1.answer") for i in range(3)] == [float(call[c]) for c in (0, 2, 4)])
chk("l4 s8 short P(L=-1000)", ans(d, "screens.8") == float(two[4]))
chk("l4 s7: 3 of 9 paths pay, chance 0.39", sum(1 for a in day for b in day if a + b > 0) == 3 and 1 - call[0] == F(39, 100))

r = RV[1]
chk("rv1 c", near(ans(r, "items.1"), F(1, 10), 1e-9))
chk("rv1 fills", near(ans(r, "items.4"), 3 * 0.6 ** 2 * 0.4, 1e-9))
chk("rv1 P(Y>=5)=20/36", MAX[5] + MAX[6] == F(20, 36))
chk("rv1 P(C>=2)", near(ans(r, "items.6"), TOT[11] + TOT[12], 1e-5))
chk("rv1 VaR", ans(r, "items.7") == var95(dict(zip([0, 1, 3, 6, 12], [F(60, 100), F(20, 100), F(12, 100), F(5, 100), F(3, 100)]))))

h = HW[1]
MIN = pmf_of(DICE, min)
chk("hw1 P(min 2)=9/36", MIN[2] == F(9, 36))
chk("hw1 four tosses", [g(h, f"items.1.widget.rows.{i}.1.answer") for i in range(5)] == [comb(4, k) / 16 for k in range(5)])
chk("hw1 F_M(2)", near(ans(h, "items.2"), MIN[1] + MIN[2], 1e-5) and all(cdf(MIN, m) == 1 - F(6 - m, 6) ** 2 for m in range(1, 7)))
chk("hw1 pmf of max (2y-1)/36", all(MAX[y] == F(2 * y - 1, 36) for y in range(1, 7)))
three = pmf_of({(a, b, c): day[a] * day[b] * day[c] for a in day for b in day for c in day}, sum)
chk("hw1 three-day call", near(ans(h, "items.4"), three[4] + three[6], 1e-12)
    and near(g(h, "items.4.widget.wrong.2.value"), three[2] + three[4] + three[6], 1e-12))
chk("hw1 VaR tie", ans(h, "items.5") == var95(dict(zip([-3, -1, 0, 2, 4, 8, 15], [F(25, 100), F(30, 100), F(20, 100), F(12, 100), F(8, 100), F(4, 100), F(1, 100)]))))
chk("hw1 remainder uniform", pmf_of(TOT, lambda t: t % 3) == {0: F(1, 3), 1: F(1, 3), 2: F(1, 3)})
chk("hw1 longform Z pmf", pmf_of(MAX, lambda y: max(y - 4, 0)) == {0: F(16, 36), 1: F(9, 36), 2: F(11, 36)})
run_code(g(h, "items.8.widget"), "hw1 pmf_of")
tosses = {s: 0.7 ** s.count("H") * 0.3 ** s.count("T") for s in map("".join, itertools.product("HT", repeat=3))}
tot = 0.0
for _ in range(10):
    tot += 0.1
chk("hw1 byKey test-4: ten 0.1s added one at a time give 0.9999999999999999", tot == 0.9999999999999999)
if sys.version_info >= (3, 12):
    chk("hw1 byKey test-7: these chances sum to 0.9999999999999998 even with sum", sum(tosses.values()) == 0.9999999999999998)

p = PB[1]
spin = pmf_of({(a, b): F(1, 16) for a in range(1, 5) for b in range(1, 5)}, lambda w: w[0] * w[1])
chk("pb1 spinner", [near(ans(p, f"items.0.parts.{i}"), v, 1e-9) for i, v in enumerate(
    [spin[4], cdf(spin, 4), cdf(spin, 9) - cdf(spin, 4), cdf(spin, 6)])] == [True] * 4)
bn = {k: comb(4, k) * 0.1 ** k * 0.9 ** (4 - k) for k in range(5)}
chk("pb1 bonds", near(ans(p, "items.1.parts.0"), bn[1], 1e-9) and near(ans(p, "items.1.parts.1"), bn[0] + bn[1], 1e-9)
    and near(ans(p, "items.1.parts.2"), bn[2], 1e-9) and ans(p, "items.1.parts.3") == 25 * min(k for k in bn if sum(bn[j] for j in range(k + 1)) >= 0.95)
    and near(0.9 ** 3 + 3 * 0.1 * 0.9 ** 2, 0.972, 1e-12))
mv = {-2: 0.1, -1: 0.3, 0: 0.2, 1: 0.25, 2: 0.15}
y = pmf_of(mv, abs)
t2 = pmf_of({(a, b): y[a] * y[b] for a in y for b in y}, sum)
chk("pb1 straddle", near(ans(p, "items.2.parts.0"), 0.15, 1e-9) and near(ans(p, "items.2.parts.1"), y[2], 1e-9)
    and near(ans(p, "items.2.parts.2"), y[0] + y[1], 1e-9) and near(ans(p, "items.2.parts.3"), t2[3] + t2[4], 1e-9))
tmin = pmf_of({w: F(1, 125) for w in itertools.product(range(1, 6), repeat=3)}, min)
chk("pb1 tightest quote", ans(p, "items.3.parts.0") == 27 and near(ans(p, "items.3.parts.1"), cdf(tmin, 2), 1e-9)
    and near(ans(p, "items.3.parts.2"), tmin[2], 1e-9) and ans(p, "items.3.parts.3") == min(n for n in range(1, 50) if 1 - 0.6 ** n >= 0.99))

# ---------------------------------------------------------------- level 2
d = L[5]
series = g(d, "screens.2.canvas.params.series.0.values")
chk("l5 s1 balance 1.5", mean(heads3) == F(3, 2))
chk("l5 s2 series: 4.5 after 10 rolls, ends near 3.5", series[9] == 4.5 and len(series) == 1000 and abs(series[-1] - 3.5) < 0.01)
chk("l5 s2 a roll moves a 1,000-roll average by under 0.003", 2.5 / 1001 < 0.003)
chk("l5 s3 E die", ans(d, "screens.3") == mean(DIE) == 3.5)
loaded = {**{k: F(1, 10) for k in range(1, 6)}, 6: F(1, 2)}
chk("l5 s4 loaded die", ans(d, "screens.4") == mean(loaded) == 4.5)
sixes = pmf_of(DICE, lambda w: (w[0] == 6) + (w[1] == 6))
chk("l5 s6 sixes in two rolls", sixes == {0: F(25, 36), 1: F(10, 36), 2: F(1, 36)} and mean(sixes) == F(1, 3))
chk("l5 s9 P&L mean and sd", near(ans(d, "screens.9"), 0.2, 1e-9) and near(sqrt(250 * var({2: .3, 0: .5, -2: .2})), 22.1, 0.1))
chk("l5 q1, q3", near(ans(d, "quiz.1"), 1.2, 1e-9) and near(ans(d, "quiz.3"), 1.9, 1e-9))
run_code(g(d, "screens.8.widget"), "l5 expectation")
env = {}
exec(g(d, "screens.8.widget.solution"), env)
sim = env["simulate"]({k: 1 / 6 for k in range(1, 7)}, 100000)
chk("l5 s8 simulate prints 3.50167", f"{sim:.5f}" == "3.50167" and has(d, "screens.8.explain", "3.50167"))
rng = random.Random(20261111)
chk("MC: mean of 200,000 die rolls is 3.5", abs(sum(rng.randint(1, 6) for _ in range(200000)) / 200000 - 3.5) < 0.02)

d = L[6]
chk("l6 s2 fair price", near(ans(d, "screens.2"), 10 * TOT[7], 1e-4))
chk("l6 s3 expected profit", near(ans(d, "screens.3"), 10 * TOT[7] - 2, 1e-4))
chk("l6 s4 two ways", near(ans(d, "screens.4"), 12 * TOT[7] + 6 * (TOT[2] + TOT[12]), 1e-4)
    and near(g(d, "screens.4.widget.wrong.3.value"), 12 * TOT[7] + 6 * TOT[2], 1e-4))
dd = {2: F(4, 10), 0: F(4, 10), -2: F(2, 10)}
fin = pmf_of({(a, b): dd[a] * dd[b] for a in dd for b in dd}, lambda w: 100 + sum(w))
chk("l6 s9 binary", ans(d, "screens.9") == 100 * sum(p for s, p in fin.items() if s > 102)
    and g(d, "screens.9.widget.wrong.0.value") == 100 * sum(p for s, p in fin.items() if s >= 102)
    and g(d, "screens.9.widget.wrong.1.value") == 100 * fin[102])
chk("l6 s9 leaves", g(d, "screens.9.canvas.params.leaves") == {f"{a}-{b}": f"£{100 + x + y}" for a, x in (("u", 2), ("f", 0), ("d", -2)) for b, y in (("u", 2), ("f", 0), ("d", -2))})
chk("l6 s10 overround", near(ans(d, "screens.10"), 0.52 + 0.28 + 0.27 - 1, 1e-9))
chk("l6 q0, q1", near(ans(d, "quiz.0"), 1e6 * 1e-6 + 50 * 0.01 - 2, 1e-9) and near(ans(d, "quiz.1"), 20 / 36 - 3, 1e-4))
rng = random.Random(6)
tot_abs = sum(abs(sum(rng.choice((-1, 1)) for _ in range(10000))) for _ in range(300)) / 300
chk("MC: after 10,000 fair £1 bets the typical total is about £80, not about £0", 70 < tot_abs < 90)

d = L[7]
chk("l7 s0 row 1 average", ans(d, "screens.0") == sum(1 + b for b in range(1, 7)) / 6)
chk("l7 row k averages k+3.5 only because Y is uniform in each row; for Y = X row k is the single cell 2k",
    all(F(sum(k + b for b in range(1, 7)), 6) == k + F(7, 2) for k in range(1, 7)) and all(2 * k != k + F(7, 2) for k in range(1, 7) if k != 3.5))
chk("l7 s3 E[X+X]", ans(d, "screens.3") == mean(pmf_of(DIE, lambda k: 2 * k)) == 7)
chk("l7 s4 E[X-Y] and E|X-Y|", mean(pmf_of(DICE, lambda w: w[0] - w[1])) == 0 and near(g(d, "screens.4.widget.wrong.0.value"), mean(pmf_of(DICE, lambda w: abs(w[0] - w[1]))), 1e-4))
chk("l7 s5 E[3X-5]", ans(d, "screens.5") == mean(pmf_of(DIE, lambda k: 3 * k - 5)))
chk("l7 s6 E[X^2]=91/6", mean(pmf_of(DIE, lambda k: k * k)) == F(91, 6))
chk("l7 s9 hedged book", 200 * .6 - 100 * .4 + 50 * .4 - 50 * .6 == 70.0)
chk("l7 s10 costs", near(ans(d, "screens.10"), 200 * (3 * .7 + 8 * .3), 1e-9))
# dependent but uncorrelated: X uniform on -1, 0, 1 and Y = X^2
tri = {(x, x * x): F(1, 3) for x in (-1, 0, 1)}
exy = sum(x * yv * p for (x, yv), p in tri.items())
ex = sum(x * p for (x, yv), p in tri.items())
ey = sum(yv * p for (x, yv), p in tri.items())
chk("D: X on -1,0,1 and Y = X^2 are dependent and E[XY] = E[X]E[Y]", exy == ex * ey == 0 and F(1, 3) != F(1, 3) * F(2, 3))
chk("FINDING 1: l7 screens[2].explain says the row argument did not use independence",
    not has(d, "screens.2.explain", "Nothing in the argument used the dice being independent"))
chk("FINDING 2a: l7 quiz[2].explain says the product rule fails for dependent variables",
    not has(d, "quiz.2.explain", "The product rule fails for dependent variables"))
chk("FINDING 3a: l7 says the product rule 'needs independence'",
    not has(d, "screens.6.explain", "needs independence") and not has(d, "screens.7.widget.options.3", "This needs independence")
    and not has(d, "quiz.2.feedback", "That needs independence"))

d = L[8]
chk("l8 s2 expected sixes", near(ans(d, "screens.2"), 10 / 6, 1e-4))
perms = list(itertools.permutations(range(5)))
chk("l8 s3 matching n=5", F(sum(sum(i == v for i, v in enumerate(pm)) for pm in perms), len(perms)) == 1 and near(g(d, "screens.3.widget.wrong.1.value"), 1 / 120, 1e-4))
chk("l8 s1 mode of Binomial(10,1/6) is 1", max(range(11), key=lambda k: comb(10, k) * 5 ** (10 - k)) == 1)
pno = 1.0
for i in range(23):
    pno *= (365 - i) / 365
chk("l8 s5 birthdays", near(ans(d, "screens.5"), comb(23, 2) / 365, 1e-4) and near(g(d, "screens.5.widget.wrong.2.value"), 1 - pno, 1e-4))
chk("l8 s9 fills", near(ans(d, "screens.9"), sum(float(row[2]) for row in g(d, "screens.9.canvas.params.rows")), 1e-9))
chk("l8 q1 aces", near(ans(d, "quiz.1"), 5 * 4 / 52, 1e-4))
rng = random.Random(8)
deck = list(range(52))
tot_m = 0
for _ in range(40000):
    rng.shuffle(deck)
    tot_m += sum(i == v for i, v in enumerate(deck))
chk("MC: a shuffled deck has 1 match on average", abs(tot_m / 40000 - 1) < 0.03)
tot_p = 0
for _ in range(40000):
    b = [rng.randrange(365) for _ in range(23)]
    c = {}
    for x in b:
        c[x] = c.get(x, 0) + 1
    tot_p += sum(v * (v - 1) // 2 for v in c.values())
chk("MC: 23 people share 0.693 birthday pairs on average", abs(tot_p / 40000 - 253 / 365) < 0.02)
tot_d = sq_d = 0
for _ in range(40000):
    pdef = 0.16 if rng.random() < 0.2 else 0.01   # common shock: mean chance 0.04
    n = sum(rng.random() < pdef for _ in range(50))
    tot_d += n
    sq_d += n * n
chk("MC: clustered defaults keep mean 2 and widen the spread", abs(tot_d / 40000 - 2) < 0.06 and sq_d / 40000 - (tot_d / 40000) ** 2 > 50 * .04 * .96 * 2)

r = RV[2]
chk("rv2 keys", near(ans(r, "items.0"), 4 * .55 - 3 * .45, 1e-9) and near(ans(r, "items.1"), 1.5, 1e-9) and ans(r, "items.3") == 5
    and near(ans(r, "items.4"), 1 * .3 + 4 * .2, 1e-9) and near(ans(r, "items.5"), 600 * (2 - 10 / 6), 1e-6)
    and mean(pmf_of(DICE, lambda w: w[0] * w[1])) == F(49, 4) and near(ans(r, "items.8"), (50 * 1.21 - 50) / 4, 1e-9) and ans(r, "items.9") == 9 / 4)
h = HW[2]
chk("hw2 keys", near(ans(h, "items.0"), 2.7, 1e-9) and near(ans(h, "items.1"), 91 / 6 - 15, 1e-4)
    and near(ans(h, "items.4"), sum(2 ** k / 2 ** k for k in range(1, 6)), 1e-9) and near(ans(h, "items.5"), 6 * (1 - (5 / 6) ** 6), 1e-4)
    and near(ans(h, "items.6"), mean(pmf_of(DIE, lambda k: k * (7 - k))), 1e-4)
    and near(ans(h, "items.7"), 1 / 1.8 + 1 / 3.6 + 1 / 4.5 - 1, 1e-4) and near(ans(h, "items.9"), 10 * 0.9 ** 10, 1e-4))
chk("hw2 matches n=3", sorted(sum(i == v for i, v in enumerate(pm)) for pm in itertools.permutations(range(3))) == [0, 0, 1, 1, 1, 3])
chk("FINDING 2b: hw2 items[6] byKey says dependent, so the product rule fails",
    not has(h, "items.6.feedback.byKey", "are dependent, so the product rule fails"))
p = PB[2]
chk("pb2 phone cover", [ans(p, f"items.0.parts.{i}") for i in range(4)] == [45, 15, 30000, 57.5] and 150 * .1 + 450 * .05 == 37.5)
chk("pb2 reversals", near(ans(p, "items.1.parts.0"), 2 * .6 * .4, 1e-9) and near(ans(p, "items.1.parts.1"), 19 * .48, 1e-9)
    and near(ans(p, "items.1.parts.3"), 57 - 8 * 9.12, 1e-9) and near(ans(p, "items.1.parts.4"), 5 * 9.12 / 9.88, 1e-4)
    and not isclose(.6 * .4 * .6 + .4 * .6 * .4, .48 ** 2))
S = {34: .1, 38: .3, 42: .4, 48: .2}
chk("pb2 options", near(ans(p, "items.2.parts.0"), mean(S), 1e-9) and near(ans(p, "items.2.parts.1"), mean(pmf_of(S, lambda s: max(s - 40, 0))), 1e-9)
    and near(ans(p, "items.2.parts.2"), mean(pmf_of(S, lambda s: max(40 - s, 0))), 1e-9) and near(ans(p, "items.2.parts.3"), 0.6, 1e-9))
hands = list(itertools.combinations("GGG" + "S" * 7, 4))
hands = [sum(1 for i in idx if i < 3) for idx in itertools.combinations(range(10), 4)]
pg = {k: F(hands.count(k), len(hands)) for k in range(4)}
chk("pb2 tokens", near(ans(p, "items.3.parts.1"), mean(pg), 1e-9) and near(ans(p, "items.3.parts.2"), 20 + 15 * mean(pg), 1e-9)
    and near(ans(p, "items.3.parts.3"), pg[2] + pg[3], 1e-4) and near(ans(p, "items.3.parts.4"), 38 + 15 * (pg[2] + 2 * pg[3]), 1e-9))

# ---------------------------------------------------------------- level 3
d = L[9]
chk("l9 s2 variance 6", ans(d, "screens.2") == var({1: .5, 3: .25, 7: .25}) and [g(d, f"screens.2.widget.wrong.{i}.value") for i in (1, 2)] == [2, 15])
chk("l9 s3 die variance and sd", var(DIE) == F(35, 12) and near(g(d, "screens.3.widget.rows.7.1.answer"), sqrt(35 / 12), 1e-4))
chk("l9 s5 sd 2", near(sqrt(var({-1: .8, 4: .2})), 2, 1e-12) and near(mean({-1: .8, 4: .2}), 0, 1e-12))
chk("l9 s8 strategies", near(ans(d, "screens.8"), sqrt(var({-200: .4, 300: .6})), 0.01) and near(sqrt(var({-400: .5, 600: .5})), 500, 1e-9))
chk("l9 s9 both sd 9.95", near(sqrt(var({-1: .99, 99: .01})), 9.95, 0.005) and near(var({1: .99, -99: .01}), 99, 1e-9))
run_code(g(d, "screens.7.widget"), "l9 variance")
random.seed(9)
rolls = [random.randint(1, 6) for _ in range(100_000)]
m = sum(rolls) / len(rolls)
chk("l9 s7 seeded simulation prints 2.9207", f"{sum((x - m) ** 2 for x in rolls) / len(rolls):.4f}" == "2.9207")

d = L[10]
chk("l10 s2, s3", near(ans(d, "screens.2"), 4 * 35 / 12, 1e-4) and ans(d, "screens.3") == 9 * 35 / 12
    and [pt["x"] for pt in g(d, "screens.3.canvas.state.points")] == [-3 * k + 5 for k in range(1, 7)])
chk("l10 s4 Var of the total and of the difference", var(TOT) == F(35, 6) == var(pmf_of(DICE, lambda w: w[0] - w[1])) and near(ans(d, "screens.4"), 35 / 6, 1e-4))
chk("l10 s6 Var(X+X)=35/3", var(pmf_of(DIE, lambda k: 2 * k)) == F(35, 3))
chk("l10 s8 nine days", ans(d, "screens.8") == min(n for n in range(1, 26) if 100 * sqrt(n) >= 300 - 1e-9) and 20 * 25 == 100 * sqrt(25))
chk("l10 s9 annual vol", near(ans(d, "screens.9"), 0.012 * sqrt(252), 1e-4) and near(g(d, "screens.9.widget.wrong.1.value"), 0.012 * sqrt(365), 1e-4))
chk("l10 s10", near(ans(d, "screens.10"), 2 * 400 * sqrt(10), 0.01))
rng = random.Random(10)
lin = [sum(rng.gauss(0, 0.012) for _ in range(252)) for _ in range(4000)]
simp = [math.exp(v) - 1 for v in lin]
sd = lambda xs: sqrt(sum((v - sum(xs) / len(xs)) ** 2 for v in xs) / len(xs))  # noqa: E731
chk("MC: 252 summed (log) returns have sd 1.2% x sqrt(252)", abs(sd(lin) - 0.012 * sqrt(252)) < 0.008)
chk("FINDING 3b: l10 says adding variances 'needs' independence",
    not has(d, "screens.6.explain", "Adding variances needs independence") and not has(d, "summary.formula", "needs $X$ and $Y$ independent"))
chk("FINDING 5: l10 summary calls independent bets 'copies', the word screens[6] uses for X + X",
    not has(d, "summary.ideas", "the sd of $n$ copies grows like"))

d = L[11]


def joint(rows, xs, ys):
    return {(x, yv): F(c) for x, row in zip(xs, rows) for yv, c in zip(ys, row)}


def cov(j):
    exx = sum(x * p for (x, yv), p in j.items())
    eyy = sum(yv * p for (x, yv), p in j.items())
    return sum(x * yv * p for (x, yv), p in j.items()) - exx * eyy


def marg(j, i):
    return pmf_of(j, lambda w: w[i])


def rho(j):
    return float(cov(j)) / sqrt(float(var(marg(j, 0)) * var(marg(j, 1))))


j1 = joint(g(d, "screens.0.canvas.params.cells"), (-1, 0, 1), (-1, 0, 1))
chk("l11 s0 table adds to 1, s2 Cov 0.36", sum(j1.values()) == 1 and near(ans(d, "screens.2"), cov(j1), 1e-12))
j2 = joint(g(d, "screens.3.canvas.params.cells"), (-1, 2), (-1, 3))
chk("l11 s3 table", [g(d, f"screens.3.widget.rows.{i}.1.answer") for i in range(4)] == [0.5, 1.4, 1.9, 1.2] and cov(j2) == F(6, 5))
chk("l11 s4 rho 1/sqrt 6", near(ans(d, "screens.4"), rho(j2), 5e-4) and near(rho(j2), 1 / sqrt(6), 1e-12))
pts = g(d, "screens.6.canvas.left.params.points")
mx = sum(a for a, b in pts) / 40
my = sum(b for a, b in pts) / 40
r_s = sum((a - mx) * (b - my) for a, b in pts) / sqrt(sum((a - mx) ** 2 for a, b in pts) * sum((b - my) ** 2 for a, b in pts))
chk("l11 s6 plotted cloud has correlation 0.8 to one place", abs(r_s - 0.8) < 0.05)
chk("l11 s6 right cloud is 3 times the left", all(abs(3 * b - c) < 0.003 for (a, b), (a2, c) in zip(pts, g(d, "screens.6.canvas.right.params.points"))))
chk("l11 s7 zero covariance, dependent", cov(tri) == 0)
j3 = joint(g(d, "screens.9.canvas.params.cells"), (-1, 0, 1), (-3, 0, 3))
chk("l11 s9 rho 0.52", sum(j3.values()) == 1 and near(ans(d, "screens.9"), rho(j3), 1e-9) and cov(j3) == F(78, 100))
beta = cov(j3) / var(marg(j3, 0))
chk("l11 s10 hedge", ans(d, "screens.10") == 100000 * beta and near(var(pmf_of(j3, lambda w: w[1] - beta * w[0])), 3.2832, 1e-9))
neg = {(x, -yv): p for (x, yv), p in j3.items()}
chk("D: a negative scale flips the sign of rho", near(rho(neg), -rho(j3), 1e-12))
chk("FINDING 4a: l11 summary.trap says scaling either variable leaves rho unchanged",
    not has(d, "summary.trap", "Scaling either variable leaves"))

d = L[12]
pv = lambda w, sx, sy, rr: w * w * sx * sx + (1 - w) ** 2 * sy * sy + 2 * w * (1 - w) * rr * sx * sy  # noqa: E731
wst = lambda sx, sy, rr: (sy * sy - rr * sx * sy) / (sx * sx + sy * sy - 2 * rr * sx * sy)  # noqa: E731
chk("l12 s1 mix sd", near(ans(d, "screens.1"), sqrt(pv(.5, .2, .2, 0)), 1e-4))
chk("l12 s2 rho=1 flat, rho=-1 zero", all(near(pv(w / 10, .2, .2, 1), .04, 1e-12) for w in range(11)) and near(pv(.5, .2, .2, -1), 0, 1e-12))
chk("l12 s3 perfect hedge", near(pv(ans(d, "screens.3"), .3, .1, -1), 0, 1e-12))
chk("l12 s4 short weight", near(ans(d, "screens.4"), wst(.3, .1, .8), 0.01) and near(sqrt(pv(wst(.3, .1, .8), .3, .1, .8)), 0.0789, 1e-4))
chk("l12 s5 sd", near(ans(d, "screens.5"), sqrt(pv(.5, .3, .1, .2)), 1e-4))
chk("l12 s7 w*", near(ans(d, "screens.7"), wst(.25, .15, .4), 1e-4) and wst(.25, .15, .59) > 0 > wst(.25, .15, .61))
nv = lambda n, s, rr: s * s / n + (1 - 1 / n) * rr * s * s  # noqa: E731
chk("l12 s8 floor", near(ans(d, "screens.8"), sqrt(.2 * .09), 1e-4) and near(g(d, "screens.8.widget.wrong.3.value"), sqrt(nv(30, .3, .2)), 1e-4))
chk("l12 s9 two funds", near(ans(d, "screens.9"), sqrt(10800 ** 2 + 2400 ** 2 + 2 * .2 * 10800 * 2400), 0.05))
chk("l12 s10 index", near(ans(d, "screens.10"), sqrt(nv(500, .3, .3)), 1e-4))
rng = random.Random(12)
n, rr, s = 20, 0.2, 0.3
vals = []
for _ in range(20000):
    z = rng.gauss(0, 1)
    vals.append(sum(s * (sqrt(rr) * z + sqrt(1 - rr) * rng.gauss(0, 1)) for _ in range(n)) / n)
chk("MC: equal-weight variance is s^2/n + (1 - 1/n) rho s^2", abs(sd(vals) ** 2 - nv(n, s, rr)) < 0.0012)

r = RV[3]
jr = joint(g(r, "items.2.canvas.params.cells"), (0, 1), (0, 1))
chk("rv3 keys", near(ans(r, "items.0"), var({-2: .25, 0: .5, 4: .25}), 1e-12) and ans(r, "items.1") == 12 and near(ans(r, "items.2"), rho(jr), 1e-12)
    and near(ans(r, "items.3"), sqrt(pv(.5, .2, .2, .5)), 1e-4) and ans(r, "items.4") == 250 * 4 and ans(r, "items.7") == 4 + 9 - 2 * 3
    and near(ans(r, "items.8"), wst(.2, .1, 0), 1e-12) and near(pv(.2, .2, .1, 0), .008, 1e-12))
h = HW[3]
ja = joint(g(h, "items.6.canvas.params.cells"), (-10, 20), (-5, 15))
chk("hw3 keys", near(ans(h, "items.0"), var(pmf_of(DIE, lambda k: max(k - 4, 0))), 1e-4) and near(ans(h, "items.3"), 1000 * sqrt(13), 0.01)
    and ans(h, "items.5") == min(k for k in range(1, 100) if sqrt(nv(k, .25, .36)) <= .16) and near(ans(h, "items.7"), sqrt(pv(.7, .25, .1, -.2)), 1e-4))
chk("hw3 longform", var(marg(ja, 0)) == 216 and var(marg(ja, 1)) == 84 and cov(ja) == 48 and near(rho(ja), 0.356, 5e-4)
    and var(pmf_of(ja, sum)) == 396)
fam = FL["families"]
chk("fluency keys are the pmf variance and its root", all(
    near(p_ * a * a + (1 - p_) * b * b - (p_ * a - (1 - p_) * b) ** 2, var({a: p_, -b: 1 - p_}), 1e-9)
    and near(sqrt(p_ * (1 - p_)) * (a + b), sqrt(var({a: p_, -b: 1 - p_})), 1e-9)
    for p_ in (.1, .2, .5, .8, .9) for a in range(1, 13) for b in range(1, 13))
    and "sqrt(p*q)*(a + b)" == fam[2]["let"]["key"])
p = PB[3]
X = {-3: .2, 1: .5, 4: .3}
chk("pb3 quotes", near(ans(p, "items.0.parts.0"), mean(X), 1e-9) and near(ans(p, "items.0.parts.1"), var(X), 1e-9)
    and near(ans(p, "items.0.parts.2"), sqrt(100 * var(X)), 1e-4) and ans(p, "items.0.parts.3") == min(k for k in range(1, 2000) if sqrt(5.89 * k) <= 0.11 * k))
jf = {(-1, -2): F(3, 10), (-1, 2): F(1, 10), (2, -2): F(1, 10), (2, 2): F(5, 10)}
hh = cov(jf) / var(marg(jf, 1))
chk("pb3 hedge", near(ans(p, "items.1.parts.0"), mean(marg(jf, 0)) / 100, 1e-12) and near(ans(p, "items.1.parts.1"), var(marg(jf, 0)), 1e-12)
    and near(ans(p, "items.1.parts.2"), cov(jf), 1e-12) and near(ans(p, "items.1.parts.3"), rho(jf), 1e-4) and hh == F(7, 16)
    and near(ans(p, "items.1.parts.4"), var(pmf_of(jf, lambda w: w[0] - hh * w[1])), 1e-12))
fx = {-.1: .2, .1: .5, .3: .3}
chk("pb3 two funds", near(ans(p, "items.2.parts.0"), mean(fx), 1e-9) and near(ans(p, "items.2.parts.1"), var(fx), 1e-9)
    and near(ans(p, "items.2.parts.2"), .0049 / (.0196 + .0049), 1e-9) and near(ans(p, "items.2.parts.3"), sqrt(.04 * .0196 + .64 * .0049), 1e-4)
    and .064 / .0626 > .12 / .14 > .05 / .07)
vn = lambda k: .25 * k + .05 * k * (k - 1)  # noqa: E731
chk("pb3 clustered fills", near(ans(p, "items.3.parts.0"), .3 - .25, 1e-12) and near(ans(p, "items.3.parts.1"), vn(4), 1e-12)
    and near(ans(p, "items.3.parts.2"), 12 * sqrt(vn(4)), 1e-4) and ans(p, "items.3.parts.3") == max(k for k in range(1, 30) if 12 * sqrt(vn(k)) <= 20))

# ---------------------------------------------------------------- remaining findings (text checks)
chk("FINDING 4b: l11 quiz[2].feedback.correct says scaling Y leaves rho alone",
    not has(L[11], "quiz.2.feedback", "Scaling and shifting $Y$ leave"))
chk("FINDING 6: l3 screens[10].prose says the loss is at most the VaR on 95% of days (it is 96%)",
    not has(L[3], "screens.10.prose", "On 95% of days the loss is at most this") and cdf(loss, 5) == F(96, 100))
chk("FINDING 7: l6 quiz[3] key says many fair bets roughly break even",
    not has(L[6], "quiz.3.widget.options.0", "you expect to roughly break even"))
chk("FINDING 8: l10 screens[9] does not say the daily returns add",
    has(L[10], "screens.9", "log return") or has(L[10], "screens.9", "returns add"))
chk("FINDING 9: l4 screens[7].explain says 39% of paths",
    not has(L[4], "screens.7.explain", "39% of paths"))
chk("FINDING 10: l5 screens[9].explain says 250 days make about £50",
    not has(L[5], "screens.9.explain", "that is about £50"))

print(f"CPython {sys.version.split()[0]}; checks: {PASS + FAIL}, failed: {FAIL}")
for name in FAILED:
    print("  FAIL", name)
sys.exit(1 if FAIL else 0)
