"""Second reader's recompute of measure-prob problems-1 to problems-3 (review-problems-measure-prob-1-3.md).

Imports nothing from the author's script. Every key, every wrong value and the numbers printed in the lines are
rebuilt from the prose by enumeration, exact fractions or sympy, then compared with the JSON. Band rules are checked
on every numeric part. Exit code is always 0; each failing check prints a line starting FINDING (CI reads those).
No numerical solver is used, so nothing depends on a SciPy build.
"""
import itertools
import json
import math
import os
import re
from fractions import Fraction as Fr

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
COURSE = os.path.join(ROOT, "app", "content", "courses", "measure-prob")
SETS = {k: json.load(open(os.path.join(COURSE, f"problems-{k}.json"), encoding="utf-8")) for k in (1, 2, 3)}

checks = 0
findings = 0


def check(ok, label):
    global checks, findings
    checks += 1
    if not ok:
        findings += 1
        print("FINDING", label)


def close(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def part(k, item, j):
    for it in SETS[k]["items"]:
        if it["id"] == item:
            return it["parts"][j - 1]
    raise KeyError(item)


def key_is(k, item, j, value, wrongs=None):
    """The key equals `value`; each wrong id equals the slip value given."""
    w = part(k, item, j)["widget"]
    tol = w.get("tol", {}).get("abs", 0)
    check(abs(w["answer"] - float(value)) <= max(tol, 1e-9), f"problems-{k} {item} part {j}: key {w['answer']} against {float(value):.6f}")
    got = {x["id"]: x for x in w.get("wrong", [])}
    for wid, v in (wrongs or {}).items():
        check(wid in got and abs(got[wid]["value"] - float(v)) <= max(got[wid]["tol"]["abs"], 1e-9),
              f"problems-{k} {item} part {j}: wrong {wid} is {got.get(wid, {}).get('value')} against {float(v):.6f}")
    check(set(got) == set(wrongs or {}), f"problems-{k} {item} part {j}: wrong ids {sorted(got)} not all rebuilt")


def expr_is(k, item, j, sym, expected, wrongs):
    w = part(k, item, j)["widget"]

    def val(tex, x):
        s = tex.replace("\\frac", "F").replace("\\left", "").replace("\\right", "").replace("\\cdot", "*")
        for _ in range(6):
            s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
            s = re.sub(r"F\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = s.replace("^", "**")
        s = re.sub(r"(\d)([a-z(])", r"\1*\2", s)
        s = re.sub(r"\)\(", ")*(", s)
        s = re.sub(r"([a-z])\(", r"\1*(", s)
        try:
            return float(eval(s, {"__builtins__": {}}, {sym: x}))
        except Exception:  # an unreadable form is a finding, not a crash
            return float("nan")

    for x in (2.0, 3.0, 7.0):
        for form in [w["answer"]] + w.get("accept", []):
            check(close(val(form, x), expected(x), 1e-9), f"problems-{k} {item} part {j}: form {form} at {sym}={x}")
    got = {x["id"]: x["tex"] for x in w.get("wrong", [])}
    for wid, f in wrongs.items():
        check(wid in got and all(close(val(got[wid], x), f(x), 1e-9) for x in (2.0, 3.0, 7.0)), f"problems-{k} {item} part {j}: wrong {wid}")
        check(wid in got and any(not close(val(got[wid], x), expected(x), 1e-6) for x in (2.0, 3.0, 7.0)), f"problems-{k} {item} part {j}: wrong {wid} equals the key")
    check(set(got) == set(wrongs), f"problems-{k} {item} part {j}: wrong ids {sorted(got)} not all rebuilt")


# ---------------------------------------------------------------- level 1
# p-fat-cantor: build the intervals exactly.
def fat_stage(n):
    ivs = [(Fr(0), Fr(1))]
    removed = []
    for s in range(1, n + 1):
        gap, nxt, rem = Fr(1, 4 ** s), [], Fr(0)
        for a, b in ivs:
            m = (a + b) / 2
            assert b - a > gap
            nxt += [(a, m - gap / 2), (m + gap / 2, b)]
            rem += gap
        removed.append(rem)
        ivs = nxt
    return ivs, removed


ivs1, _ = fat_stage(1)
check(ivs1 == [(Fr(0), Fr(3, 8)), (Fr(5, 8), Fr(1))], "fat Cantor: stage 1 removes (3/8, 5/8)")
ivs3, rem3 = fat_stage(3)
key_is(1, "p-fat-cantor", 1, rem3[2], {"one-gap": Fr(1, 64), "eight-gaps": Fr(8, 64)})
for n in range(1, 9):
    iv, rem = fat_stage(n)
    check(len(iv) == 2 ** n and sum(b - a for a, b in iv) == Fr(1, 2) + Fr(1, 2 ** (n + 1)), f"fat Cantor: length of C_{n}")
    check(rem[-1] == Fr(1, 2 ** (n + 1)), f"fat Cantor: stage {n} removes 2^-(n+1)")
expr_is(1, "p-fat-cantor", 2, "n", lambda n: 0.5 + 2 ** -(n + 1),
        {"shift": lambda n: 0.5 + 2 ** -n, "last-only": lambda n: 1 - 2 ** -(n + 1), "removed": lambda n: 2 ** -(n + 1)})
key_is(1, "p-fat-cantor", 3, sp.limit(sp.Rational(1, 2) + 2 ** (-(sp.Symbol("n") + 1)), sp.Symbol("n"), sp.oo),
       {"zero": 0, "stage-three": sum(b - a for a, b in ivs3)})
check(part(1, "p-fat-cantor", 4)["widget"]["options"][0].get("correct") is True, "fat Cantor part 4 key")

# p-ball-machine: sigma-algebras by closure on bit masks.
balls = range(1, 13)
pr = {w: Fr(w, 78) for w in balls}
check(sum(pr.values()) == 1, "ball machine: chances add to 1")
X = {w: w % 4 for w in balls}
Y = {w: int(w >= 10) for w in balls}


def atoms(*fs):
    out = {}
    for w in balls:
        out.setdefault(tuple(f[w] for f in fs), []).append(w)
    return sorted(out.values())


def closure(gens):
    full = (1 << 12) - 1
    fam = {0, full} | set(gens)
    while True:
        new = {full & ~a for a in fam} | {a | b for a in fam for b in fam}
        if new <= fam:
            return fam
        fam |= new


def mask(s):
    return sum(1 << (w - 1) for w in s)


sx = closure([mask([w for w in balls if X[w] == v]) for v in range(4)])
sxy = closure([mask([w for w in balls if X[w] == v]) for v in range(4)] + [mask([w for w in balls if Y[w] == 1])])
check(atoms(X) == [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]], "ball machine: atoms of X")
key_is(1, "p-ball-machine", 1, len(sx), {"atoms": len(atoms(X)), "all": 2 ** 12})
check(len(atoms(X, Y)) == 7, "ball machine: 7 atoms of (X, Y)")
key_is(1, "p-ball-machine", 2, len(sxy), {"product": 2 ** 8, "side-by-side": 2 ** 6})
law = {v: sum(pr[w] for w in balls if X[w] == v) for v in range(4)}
check([law[v] * 78 for v in range(4)] == [24, 15, 18, 21], "ball machine: law of X")
F = lambda x: sum(p for v, p in law.items() if v <= x)  # noqa: E731
key_is(1, "p-ball-machine", 3, F(2.5), {"uniform": Fr(9, 12), "strict": law[0] + law[1], "complement": law[3]})
check(F(2.5) == Fr(57, 78), "ball machine: F_X(2.5) = 57/78")
key_is(1, "p-ball-machine", 4, min(v for v in range(4) if F(v) >= Fr(3, 4)), {"equal-chances": min(v for v in range(4) if Fr(3 * (v + 1), 12) >= Fr(3, 4))})
meas = lambda f: all(len({f(w) for w in a}) == 1 for a in atoms(X))  # noqa: E731
opts = {o["id"]: o.get("correct", False) for o in part(1, "p-ball-machine", 5)["widget"]["options"]}
check(opts == {"parity": meas(lambda w: w % 2 == 0), "flag": meas(lambda w: Y[w]), "row": meas(lambda w: -(-w // 4)), "mod3": meas(lambda w: w % 3)},
      "ball machine part 5: which variables are sigma(X)-measurable")
check((Y[10], Y[2], -(-1 // 4), -(-9 // 4), 4 % 3, 8 % 3) == (1, 0, 1, 3, 1, 2), "ball machine part 5: values in the why lines")

# p-reciprocal-grid: lengths of preimages, and a fine exact grid of U.
PN = lambda n: Fr(1, n) - Fr(1, n + 1)  # noqa: E731  {n <= 1/U < n+1} = (1/(n+1), 1/n]
GRID = 27720 * 4  # divisible by 1..12, so the cut points 1/n for n <= 12 fall on the grid
cnt = {}
for i in range(1, GRID + 1):  # U = (i - 1/2)/GRID, a midpoint rule that is exact for these step sets
    nn = (2 * GRID) // (2 * i - 1)
    cnt[nn] = cnt.get(nn, 0) + 1
check(all(Fr(cnt[n], GRID) == PN(n) for n in range(1, 12)), "reciprocal grid: P(N = n) = 1/(n(n+1)) on the grid")
key_is(1, "p-reciprocal-grid", 1, PN(3), {"third": Fr(1, 3), "two": PN(2)})
tail = lambda n: sum(Fr(c, GRID) for m, c in cnt.items() if m >= n)  # noqa: E731
check(all(tail(n) == Fr(1, n) for n in range(1, 13)), "reciprocal grid: P(N >= n) = 1/n on the grid")
expr_is(1, "p-reciprocal-grid", 2, "n", lambda n: 1 / n,
        {"shift": lambda n: 1 / (n + 1), "below": lambda n: 1 - 1 / n, "point": lambda n: 1 / (n * (n + 1))})
FX = lambda x, strict=False: sum(Fr(c, GRID) for m, c in cnt.items() if (Fr(1, m) < x if strict else Fr(1, m) <= x))  # noqa: E731
key_is(1, "p-reciprocal-grid", 3, FX(Fr(3, 10)), {"as-u": Fr(3, 10), "three": Fr(1, 3)})
key_is(1, "p-reciprocal-grid", 4, FX(Fr(1, 5), strict=True), {"at-point": FX(Fr(1, 5)), "jump": FX(Fr(1, 5)) - FX(Fr(1, 5), strict=True)})
check(part(1, "p-reciprocal-grid", 5)["widget"]["options"][0].get("correct") is True and FX(Fr(0)) == 0, "reciprocal grid part 5 key")

# p-no-double-seven: every digit string.
good = lambda n: sum(1 for s in itertools.product(range(10), repeat=n) if all(not (s[i] == 7 and s[i + 1] == 7) for i in range(n - 1)))  # noqa: E731
a = {n: good(n) for n in range(1, 6)}
check(a[2] == 99 and a[3] == 981 and a[4] == 9720 and all(a[n] == 9 * a[n - 1] + 9 * a[n - 2] for n in (3, 4, 5)), "no 77: counts and recursion by enumeration")
three = [s for s in itertools.product(range(10), repeat=3)]
check((sum(s[0] == s[1] == 7 for s in three), sum(s[1] == s[2] == 7 for s in three), 1000 - a[3]) == (10, 10, 19), "no 77: 10, 10 and 19 strings")
key_is(1, "p-no-double-seven", 1, Fr(a[3], 1000), {"overlap": Fr(980, 1000), "first-pair": Fr(990, 1000)})
key_is(1, "p-no-double-seven", 2, Fr(a[4], 10 ** 4), {"one-term": Fr(9 * a[3], 10 ** 4), "square": Fr(a[3], 1000) ** 2})
key_is(1, "p-no-double-seven", 3, Fr(99, 100) ** 100, {"all-places": Fr(99, 100) ** 199, "all-digits": Fr(99, 100) ** 200})
big = [Fr(1), Fr(10)]
for n in range(2, 201):
    big.append(9 * big[-1] + 9 * big[-2])
check(Fr(big[200], 10 ** 200) <= Fr(99, 100) ** 100, "no 77: P(D_200) lies under the bound 0.99^100")
check(all(Fr(big[2 * m], 10 ** (2 * m)) <= Fr(99, 100) ** m for m in range(1, 100)), "no 77: P(D_2m) <= 0.99^m")
check(Fr(big[200], 10 ** 200) > Fr(99, 100) ** 199, "no 77: 0.99^199 is not an upper bound on P(D_200), as the all-places line says")
key_is(1, "p-no-double-seven", 4, 0, {"complement": 1})
check(part(1, "p-no-double-seven", 5)["widget"]["options"][0].get("correct") is True, "no 77 part 5 key")

hw1 = open(os.path.join(COURSE, "homework-1.json"), encoding="utf-8").read()
check(not ("\\tfrac{1}{k(k+1)}" in hw1 and "\\frac{1}{n(n+1)}" in json.dumps(SETS[1], ensure_ascii=False)),
      "problems-1 p-reciprocal-grid: the law 1/(k(k+1)) with tails 1/n and continuity from above is homework-1 h-build-space and l3 q-above")

# ---------------------------------------------------------------- level 2
t, r, u, x = sp.symbols("t r u x", positive=True)
n_ = sp.Symbol("n", positive=True, integer=True)
# p-billed-hours: E floor(X) as sum of k P(floor X = k), a route that does not use the tail sum.
pk = lambda k, h=1.0: math.exp(-k * h) - math.exp(-(k + 1) * h)  # noqa: E731
key_is(2, "p-billed-hours", 1, pk(2), {"tail": math.exp(-2), "cdf": 1 - math.exp(-2)})
bill = lambda h: sum(k * h * pk(k, h) for k in range(1, int(60 / h)))  # noqa: E731
key_is(2, "p-billed-hours", 2, bill(1.0), {"from-zero": bill(1.0) + 1, "mean": 1, "half-lost": 0.5})
check(close(bill(1.0), 1 / (math.e - 1), 1e-10) and close(sp.summation(sp.exp(-n_), (n_, 1, sp.oo)), 1 / (math.e - 1), 1e-12), "billed hours: 1/(e - 1)")
key_is(2, "p-billed-hours", 3, bill(0.5), {"no-half": 2 * bill(0.5), "from-zero": bill(0.5) + 0.5})
check(all(close(bill(h), h / math.expm1(h), 1e-9) for h in (1.0, 0.5, 0.25, 1 / 32, 1 / 64)), "billed hours: mean h/(e^h - 1)")
first = min(n for n in range(0, 20) if bill(2.0 ** -n) > 0.99)
key_is(2, "p-billed-hours", 4, first, {"one-minus-h": min(n for n in range(0, 20) if 1 - 2.0 ** -n > 0.99)})
check(round(bill(1 / 32), 4) == 0.9845 and round(bill(1 / 64), 4) == 0.9922, "billed hours: 0.9845 and 0.9922")
check(1 - bill(1.0) < 0.5, "billed hours: rounding down loses under half an hour")
check("simple function" not in part(2, "p-billed-hours", 4)["question"],
      "problems-2 p-billed-hours part 4: h*floor(X/h) of an exponential X takes infinitely many values, so it is not a simple function as l5 defines one")

# p-compounding: moments by exact normal integrals.
z = sp.Symbol("z", real=True)
phi = sp.exp(-z ** 2 / 2) / sp.sqrt(2 * sp.pi)
EZ = lambda f: sp.integrate(f * phi, (z, -sp.oo, sp.oo))  # noqa: E731
R = z / 2
check(EZ(R ** 2) == sp.Rational(1, 4) and EZ(R ** 4) == sp.Rational(3, 16), "compounding: E[R^2] and E[R^4]")
g2, g4 = EZ(sp.expand((1 + R / 2) ** 2)), EZ(sp.expand((1 + R / 4) ** 4))
key_is(2, "p-compounding", 1, g2, {"no-square": 1, "half-square": 1 + sp.Rational(1, 4) / 2})
key_is(2, "p-compounding", 2, g4, {"no-fourth": 1 + 6 * sp.Rational(1, 4) / 16, "fourth-one": 1 + 6 * sp.Rational(1, 4) / 16 + sp.Rational(1, 16) / 256})
check(close(6 * 0.25 / 16, 0.09375) and round(0.1875 / 256, 6) == 0.000732, "compounding: 0.09375 and 0.000732")
dom_exact = float(2 * sp.integrate(sp.exp(z / 2) * phi, (z, 0, sp.oo)))
dom_stated = 2 * math.exp(0.125) * 0.6915
check(close(dom_exact, 2 * math.exp(0.125) * 0.5 * (1 + math.erf(0.5 / math.sqrt(2))), 1e-12), "compounding: E e^|R| = 2 e^0.125 Phi(0.5)")
check(round(0.5 * (1 + math.erf(0.5 / math.sqrt(2))), 4) == 0.6915, "compounding: Phi(0.5) = 0.6915")
key_is(2, "p-compounding", 3, dom_stated, {"no-abs": math.exp(0.125), "no-phi": 2 * math.exp(0.125)})
check(round(dom_exact, 3) == round(dom_stated, 3) == 1.567, "compounding: 1.567 from the table value and from the exact value")
check(all(abs((1 + rr / n) ** n) <= math.exp(abs(rr)) + 1e-12 for n in range(1, 60) for rr in [i / 10 for i in range(-80, 81)]), "compounding: |G_n| <= e^|R|")
check(((1 - 3) ** 1, (1 - 1.5) ** 2, (1 - 1) ** 3) == (-2, 0.25, 0), "compounding: G_1, G_2, G_3 at R = -3")
key_is(2, "p-compounding", 5, float(EZ(sp.exp(R))), {"jensen": 1, "no-half": math.exp(0.25), "bound": dom_stated})
check(float(g2) < float(g4) < math.exp(0.125), "compounding: 1.0625 < 1.0945 < limit")
check(part(2, "p-compounding", 4)["widget"]["options"][0]["id"] == "dct" and part(2, "p-compounding", 4)["widget"]["options"][0].get("correct") is True, "compounding part 4 key")
p3 = part(2, "p-compounding", 3)
leak = json.dumps(p3["feedback"], ensure_ascii=False)
check(not ("1.1331" in leak and "E[e^R]" in leak),
      "problems-2 p-compounding part 3: its lines print E[e^R] = e^{0.125} and 1.1331, the key of part 5, two parts early")

# p-root-of-uniform.
EXn = sp.integrate(1 - t ** n_, (t, 0, 1))
check(sp.simplify(EXn - n_ / (n_ + 1)) == 0, "root of uniform: E[X_n] = n/(n+1) by layer cake")
key_is(2, "p-root-of-uniform", 1, sp.integrate(u ** sp.Rational(1, 4), (u, 0, 1)), {"tail-only": Fr(1, 5), "jensen": 0.5 ** 0.25})
ms = lambda n: sp.integrate((u ** sp.Rational(1, n) - 1) ** 2, (u, 0, 1))  # noqa: E731
check(all(ms(n) == sp.Rational(2, (n + 1) * (n + 2)) for n in (1, 2, 3, 4, 10)), "root of uniform: mean-square distance by direct integration")
var = lambda n: float(sp.integrate(u ** sp.Rational(2, n), (u, 0, 1)) - sp.integrate(u ** sp.Rational(1, n), (u, 0, 1)) ** 2)  # noqa: E731
check(all(close(var(n), n / ((n + 2) * (n + 1) ** 2), 1e-12) for n in (2, 3, 7)), "root of uniform: variance slip formula")
expr_is(2, "p-root-of-uniform", 2, "n", lambda n: 2 / ((n + 1) * (n + 2)),
        {"mean-gap": lambda n: 1 / (n + 1) ** 2, "variance": lambda n: n / ((n + 2) * (n + 1) ** 2)})
key_is(2, "p-root-of-uniform", 3, ms(10) / sp.Rational(1, 100), {"no-eps": ms(10), "eps": ms(10) * 10})
key_is(2, "p-root-of-uniform", 4, 0.9 ** 10, {"complement": 1 - 0.9 ** 10, "root": 0.9 ** 0.1})
check(part(2, "p-root-of-uniform", 5)["widget"]["options"][0].get("correct") is True, "root of uniform part 5 key")
exam = open(os.path.join(ROOT, "app", "content", "exams", "topic-3.2.json"), encoding="utf-8").read()
check(not ("U^{1/n}" in exam and "U^{1/n}" in json.dumps(SETS[2], ensure_ascii=False)),
      "problems-2 p-root-of-uniform: the sequence U^{1/n} with mean n/(n+1) is option a of exam e-swap-limits (topic-3.2.json)")

# p-random-maturity.
V = sp.integrate(sp.exp(-r * t), (t, 0, 4)) / 4
V05 = float(V.subs(r, sp.Rational(1, 20)))
dV05 = float(-sp.diff(V, r).subs(r, sp.Rational(1, 20)))
direct = float(sp.integrate(t * sp.exp(-t / 20), (t, 0, 4)) / 4)
check(close(dV05, direct, 1e-12), "random maturity: -V'(0.05) equals E[T e^{-0.05 T}]")
key_is(2, "p-random-maturity", 1, V05, {"mean-time": math.exp(-0.1), "end": math.exp(-0.2)})
key_is(2, "p-random-maturity", 3, direct, {"jensen": 2 * math.exp(-0.1), "no-discount": 2})
check(close(direct, (1 - 1.2 * math.exp(-0.2)) / 0.01, 1e-12), "random maturity: closed form of part 3")
key_is(2, "p-random-maturity", 4, direct / V05, {"mean": 2, "no-divide": direct, "inverse": V05 / direct})
check(round(1.7523 / 0.9063, 2) == round(direct / V05, 2) == 1.93, "random maturity: 1.93 from rounded and from exact inputs")
check(all(abs((math.exp(-(rr + h) * T) - math.exp(-rr * T)) / h) <= T + 1e-12 for T in (0.5, 2, 4) for rr in (0, 0.3, 0.9) for h in (0.1, 0.01, 1e-4)), "random maturity: quotients bounded by T <= 4")
check(part(2, "p-random-maturity", 2)["widget"]["options"][0].get("correct") is True, "random maturity part 2 key")

# ---------------------------------------------------------------- level 3
# p-nested-forecasts.
P = [Fr(1, 10), Fr(3, 20), Fr(1, 4), Fr(1, 5), Fr(1, 5), Fr(1, 10)]
XV = [-3, 1, 5, 2, 6, -4]
check(sum(P) == 1, "nested forecasts: chances add to 1")
G_AT, H_AT = [[0], [1, 2], [3, 4], [5]], [[0, 1, 2], [3, 4, 5]]


def cond(vals, ats):
    out = [None] * 6
    for at in ats:
        m = sum(P[i] * vals[i] for i in at) / sum(P[i] for i in at)
        for i in at:
            out[i] = m
    return out


E_ = lambda v: sum(p * a for p, a in zip(P, v))  # noqa: E731
EG, EH = cond(XV, G_AT), cond(XV, H_AT)
key_is(3, "p-nested-forecasts", 1, 2 ** 4 - 2 ** 2, {"all": 16, "atoms": 2})
key_is(3, "p-nested-forecasts", 2, EG[1], {"unweighted": 3, "no-divide": P[1] * XV[1] + P[2] * XV[2]})
check(cond(EG, H_AT) == EH and [EG[0], EG[1], EG[3], EG[5]] == [-3, Fr(7, 2), 4, -4] and EH[0] == Fr(11, 5) and EH[3] == Fr(12, 5), "nested forecasts: tower and the printed forecasts")
key_is(3, "p-nested-forecasts", 3, cond(EG, H_AT)[0], {"unweighted": Fr(1, 4), "finer": EG[1]})
mse = lambda f: E_([(a - b) ** 2 for a, b in zip(XV, f)])  # noqa: E731
key_is(3, "p-nested-forecasts", 4, mse(EG), {"one-atom": P[1] * (XV[1] - EG[1]) ** 2 + P[2] * (XV[2] - EG[2]) ** 2, "overall-mean": mse([E_(XV)] * 6)})
gap = E_([(a - b) ** 2 for a, b in zip(EG, EH)])
check(mse(EH) == mse(EG) + gap and E_(XV) == Fr(23, 10), "nested forecasts: Pythagoras and E[X] = 2.3")
key_is(3, "p-nested-forecasts", 5, gap, {"mse-h": mse(EH), "one-side": sum(P[i] * (EG[i] - EH[i]) ** 2 for i in (0, 1, 2))})
p5 = json.dumps(part(3, "p-nested-forecasts", 5), ensure_ascii=False)
check(not ("cut scenarios" in p5 or "hold side" in p5), "problems-3 p-nested-forecasts part 5: the one-side line says 'cut' and 'hold', which the prose never defines")

# p-doob-split: all paths of 3 steps.
pu = Fr(7, 10)
paths = list(itertools.product((1, -1), repeat=3))
pp = lambda w: math.prod(pu if s == 1 else 1 - pu for s in w)  # noqa: E731
S = lambda w, n: sum(w[:n])  # noqa: E731
A = lambda w, n: sum(Fr(4, 5) * S(w, k) + 1 for k in range(n))  # noqa: E731
for n in (0, 1, 2):  # martingale property of S^2 - A at every node
    for pre in itertools.product((1, -1), repeat=n):
        nxt = sum((pu if s == 1 else 1 - pu) * ((sum(pre) + s) ** 2 - A(pre + (s,), n + 1)) for s in (1, -1))
        check(nxt == sum(pre) ** 2 - A(pre, n), f"Doob split: martingale step at {pre}")
        inc = sum((pu if s == 1 else 1 - pu) * ((sum(pre) + s) ** 2 - sum(pre) ** 2) for s in (1, -1))
        check(inc == Fr(4, 5) * sum(pre) + 1, f"Doob split: drift 0.8s + 1 at {pre}")
expr_is(3, "p-doob-split", 1, "s", lambda s: 0.8 * s + 1, {"fair": lambda s: 1.0, "no-square": lambda s: 0.8 * s, "half-drift": lambda s: 0.4 * s + 1})
uud = (1, 1, -1)
key_is(3, "p-doob-split", 2, A(uud, 3), {"one-more": A(uud, 3) + Fr(4, 5) * S(uud, 3) + 1, "shifted": sum(Fr(4, 5) * S(uud, k) + 1 for k in (1, 2, 3)), "fair": 3})
check(A((-1, -1, 1), 3) == Fr(3, 5), "Doob split: A_3 = 0.6 on down, down, up")
check(part(3, "p-doob-split", 3)["widget"]["options"][0].get("correct") is True, "Doob split part 3 key")
ES2 = sum(pp(w) * S(w, 3) ** 2 for w in paths)
check(ES2 == sum(pp(w) * A(w, 3) for w in paths) == 3 * Fr(84, 100) + Fr(12, 10) ** 2, "Doob split: E[S_3^2] three ways")
key_is(3, "p-doob-split", 4, ES2, {"fair": 3, "mean-squared": sum(pp(w) * S(w, 3) for w in paths) ** 2, "path": A(uud, 3)})

# p-two-ups-stop: all 16 paths.
def stop(w):
    for n in range(2, 5):
        if w[n - 2] == 1 and w[n - 1] == 1:
            return n
    return 4


p4 = list(itertools.product((1, -1), repeat=4))
T_ = {w: stop(w) for w in p4}
PT = lambda n: Fr(sum(1 for w in p4 if T_[w] == n), 16)  # noqa: E731
ET = sum(Fr(T_[w], 16) for w in p4)
EST = sum(Fr(sum(w[:T_[w]]), 16) for w in p4)
EST2 = sum(Fr(sum(w[:T_[w]]) ** 2, 16) for w in p4)
late = sum(Fr(sum(w[:T_[w]]), 16) for w in p4 if T_[w] == 4)
check((PT(2), PT(3), PT(4)) == (Fr(1, 4), Fr(1, 8), Fr(5, 8)), "two ups: law of T")
for n in (2, 3, 4):  # {T = n} is decided by the first n days
    seen = {}
    for w in p4:
        seen.setdefault(w[:n], set()).add(T_[w] == n)
    check(all(len(v) == 1 for v in seen.values()), f"two ups: T = {n} is decided by day {n}")
key_is(3, "p-two-ups-stop", 1, PT(3), {"any-pair": Fr(1, 4), "four-days": Fr(1, 16)})
key_is(3, "p-two-ups-stop", 2, ET, {"any-pair": 2 * Fr(1, 4) + 3 * Fr(1, 4) + 4 * Fr(1, 2), "equal": 3})
key_is(3, "p-two-ups-stop", 3, EST, {"early-only": EST - late})
key_is(3, "p-two-ups-stop", 4, EST2, {"fixed-day": 4, "square-of-mean": EST ** 2})
check(EST2 == ET, "two ups: E[S_T^2] = E[T] by enumeration")
key_is(3, "p-two-ups-stop", 5, late, {"sign": -late, "conditional": late / PT(4)})

# p-red-card-call: all 35 orders of 4 red and 3 black.
orders = sorted(set(itertools.permutations("RRRRBBB")))
check(len(orders) == 35, "red card: 35 orders")
share = lambda w, n: Fr(w[n:].count("R"), 7 - n)  # noqa: E731
for n in range(0, 6):  # martingale property at every node
    for pre in sorted({w[:n] for w in orders}):
        grp = [w for w in orders if w[:n] == pre]
        check(sum(share(w, n + 1) for w in grp) / len(grp) == share(grp[0], n), f"red card: martingale step after {''.join(pre)}")
key_is(3, "p-red-card-call", 1, sum(share(w, 1) for w in orders) / 35, {"unweighted": (Fr(3, 6) + Fr(4, 6)) / 2, "red-shown": Fr(3, 6)})
red1 = [w for w in orders if w[0] == "R"]
key_is(3, "p-red-card-call", 2, sum(share(w, 2) for w in red1) / len(red1), {"red-again": Fr(2, 5), "start": Fr(4, 7)})


def call_time(w):
    for n in range(0, 6):
        if share(w, n) > Fr(4, 7):
            return n
    return 6


win = Fr(sum(1 for w in orders if w[call_time(w)] == "R"), 35)
first = Fr(sum(1 for w in orders if call_time(w) == 1 and w[1] == "R"), 35)
key_is(3, "p-red-card-call", 3, first, {"call-only": Fr(sum(1 for w in orders if call_time(w) == 1), 35), "win-only": Fr(4, 6)})
key_is(3, "p-red-card-call", 4, win, {"threshold": Fr(4, 6), "coin": Fr(1, 2)})
check(win == Fr(4, 7) and max(call_time(w) for w in orders) == 6, "red card: the rule wins with chance 4/7 and calls by card 6")

# ---------------------------------------------------------------- bands, every numeric part
for k, d in SETS.items():
    for it in d["items"]:
        for j, p in enumerate(it["parts"], 1):
            w = p["widget"]
            if w["kind"] != "numeric":
                continue
            where = f"problems-{k} {it['id']} part {j}"
            m = re.search(r"(\d) (?:decimal )?places", p["question"])
            check(bool(m) or re.search(r"whole number|Give a decimal|exact fraction", p["question"]) is not None, f"{where}: no form stated")
            ans, tol = w["answer"], w["tol"]["abs"]
            if m:
                pl = int(m.group(1))
                check(abs(round(ans, pl) - ans) <= tol + 1e-12, f"{where}: key band refuses the key at {pl} places")
            for num in re.findall(r"(?:\\approx|=) (-?\d+\.\d+)\$?[.,]?(?: years\.)?$", p["feedback"]["correct"]):
                check(abs(float(num) - ans) <= tol + 1e-12, f"{where}: key band refuses the printed {num}")
            bands = [(ans - tol, ans + tol, "key")]
            for xw in w.get("wrong", []):
                lo, hi = xw["value"] - xw["tol"]["abs"], xw["value"] + xw["tol"]["abs"]
                for blo, bhi, name in bands:
                    check(hi < blo - 1e-12 or lo > bhi + 1e-12, f"{where}: wrong {xw['id']} band meets the {name} band")
                bands.append((lo, hi, xw["id"]))
                check(xw["id"] in p["feedback"].get("byKey", {}), f"{where}: wrong {xw['id']} has no line")
                if m:
                    step = 10 ** -int(m.group(1))
                    lo_r, hi_r = math.floor(xw["value"] / step + 1e-9) * step, math.ceil(xw["value"] / step - 1e-9) * step
                    near = lo_r if xw["value"] - lo_r < hi_r - xw["value"] - 1e-12 else hi_r
                    tie = abs((xw["value"] - lo_r) - (hi_r - xw["value"])) < 1e-12 and hi_r > lo_r
                    for v in ([lo_r, hi_r] if tie else [near]):
                        check(abs(v - xw["value"]) <= xw["tol"]["abs"] + 1e-9,
                              f"{where}: slip {xw['id']} ({xw['value']}) typed to the {m.group(1)} places asked, {v:.{int(m.group(1))}f}, falls outside its band +-{xw['tol']['abs']}")
            if any(s in p["question"] for s in ("%", "per cent")):
                check(w.get("unit") == "%", f"{where}: percentage part without unit")

print(f"{checks} checks, {findings} findings")
