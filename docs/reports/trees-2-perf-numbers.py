"""trees level 2 performance task h-perf-any-payoff: every number twice.

Run from the repository root: venv/bin/python -I docs/reports/trees-2-perf-numbers.py
Reads the item from homework-2.json. Route A is the shipped solution in floats;
route B is an independent tree in mpmath at 40 digits (binomial sums for the
European cases). Runs the solution, a second correct solution, the starter and
planted bugs against every hidden test, as the engine compares (math.isclose,
rel 1e-9, abs 1e-12, element by element; raises by exception name).
Exits 1 on any failure.
"""
import json
import math
import os
import sys

import mpmath as mp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HW = os.path.join(ROOT, "app", "content", "courses", "trees", "homework-2.json")

fails = 0
checks = 0


def check(name, ok):
    global fails, checks
    checks += 1
    if not ok:
        fails += 1
        print("FAIL", name)


hw = json.load(open(HW, encoding="utf-8"))
items = hw["items"]
idx = [i for i, it in enumerate(items) if it["id"] == "h-perf-any-payoff"]
check("item present once", len(idx) == 1)
it = items[idx[0]]
w = it["widget"]
check("item last", idx[0] == len(items) - 1)
check("kind code", it.get("performance") == "code" and w["kind"] == "code" and w["language"] == "python")
check("no parts or hints", "parts" not in it and "hints" not in it)
tests, examples = w["tests"], w["examples"]
check("3 or more tests, more than examples", len(tests) >= 3 and len(tests) > len(examples))
check("example is test 1", examples[0]["call"] == tests[0]["call"] and examples[0]["expect"] == tests[0]["expect"])
check("example compares isclose", examples[0].get("compare") == "isclose")


# ---------- engine-like grading ----------
def close(a, e):
    if isinstance(e, (list, tuple)):
        return isinstance(a, (list, tuple)) and len(a) == len(e) and all(close(x, y) for x, y in zip(a, e))
    try:
        return math.isclose(float(a), float(e), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return False


def grade(src):
    ns = {}
    try:
        exec(src, ns)
    except Exception as x:
        return ["load " + type(x).__name__] * len(tests)
    out = []
    for k, t in enumerate(tests, 1):
        try:
            a = eval(t["call"], ns)
            if t.get("compare") == "raises":
                ok = False
            else:
                ok = close(a, eval(t["expect"]))
        except Exception as x:
            ok = t.get("compare") == "raises" and t["expect"] in [c.__name__ for c in type(x).__mro__]
        if not ok:
            out.append(k)
    return out


SOL = w["solution"]
check("solution passes all", grade(SOL) == [])
st = grade(w["starter"])
check("starter fails all", st == list(range(1, len(tests) + 1)))
check("starter is a stub", "    ...\n" in w["starter"] and "for " not in w["starter"])

# a second correct solution, written differently: the whole tree as a 2-D list
SECOND = '''
import math
def tree_value_delta(S, r, sigma, T, n, payoff, american):
    h = T / n
    up = math.exp(sigma * math.sqrt(h))
    dn = math.exp(-sigma * math.sqrt(h))
    g = math.exp(r * h)
    if g <= dn or g >= up:
        raise ValueError("no-arbitrage condition fails")
    p = (g - dn) / (up - dn)
    price = [[S * math.exp(sigma * math.sqrt(h) * (2 * j - i)) for j in range(i + 1)] for i in range(n + 1)]
    val = [[0.0] * (i + 1) for i in range(n + 1)]
    val[n] = [payoff(s) for s in price[n]]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            hold = (p * val[i + 1][j + 1] + (1 - p) * val[i + 1][j]) / g
            val[i][j] = max(hold, payoff(price[i][j])) if american else hold
    return val[0][0], (val[1][1] - val[1][0]) / (price[1][1] - price[1][0])
'''
check("second solution passes all", grade(SECOND) == [])

# ---------- planted bugs: each must fail at least one hidden test ----------
MUT = {
    "discounting omitted": [("disc = 1 / grow", "disc = 1.0")],
    "q = 1/2": [("q = (grow - d) / (u - d)", "q = 0.5")],
    "q from a simple rate": [("q = (grow - d) / (u - d)", "q = (1 + r * dt - d) / (u - d)")],
    "q from e^{rT}": [("q = (grow - d) / (u - d)", "q = (math.exp(r * T) - d) / (u - d)")],
    "q upside down": [("q = (grow - d) / (u - d)", "q = (u - grow) / (u - d)")],
    "leaves range(n)": [("for j in range(n + 1)]", "for j in range(n)]")],
    "dt = T/(n+1)": [("dt = T / n", "dt = T / (n + 1)")],
    "one step back too few": [("for i in range(n - 1, -1, -1):", "for i in range(n - 1, 0, -1):")],
    "early exercise ignored": [("        if american:\n", "        if False:\n")],
    "exercise today only": [("        if american:\n", "        if american and i == 0:\n")],
    "exercise never today": [("        if american:\n", "        if american and i > 0:\n")],
    "delta from the leaves": [("        if i == 1:\n            first = v\n", "")],
    "delta before the max": [("        if american:\n            v = [max(hold, payoff(S * u**j * d**(i - j)))\n                 for j, hold in enumerate(v)]\n        if i == 1:\n            first = v\n",
                              "        if i == 1:\n            first = v\n        if american:\n            v = [max(hold, payoff(S * u**j * d**(i - j)))\n                 for j, hold in enumerate(v)]\n")],
    "delta over S": [("delta = (first[1] - first[0]) / (S * u - S * d)", "delta = (first[1] - first[0]) / S")],
    "no arbitrage check": [('    if not d < grow < u:\n        raise ValueError("arbitrage: need d < e^(r dt) < u")\n', "")],
    "check with a simple rate": [("    if not d < grow < u:", "    if not d < 1 + r < u:")],
    "one discount at the end": [("disc = 1 / grow", "disc = 1.0"), ("    return v[0], delta", "    return v[0] * math.exp(-r * T), delta * math.exp(-r * (T - dt))")],
    "max before the discount": [("v = [disc * (q * v[j + 1] + (1 - q) * v[j]) for j in range(i + 1)]\n        if american:\n            v = [max(hold, payoff(S * u**j * d**(i - j)))",
                                 "v = [(q * v[j + 1] + (1 - q) * v[j]) for j in range(i + 1)]\n        if american:\n            v = [disc * max(hold, payoff(S * u**j * d**(i - j)))")],
    "u = e^{sigma dt}": [("u = math.exp(sigma * math.sqrt(dt))", "u = math.exp(sigma * dt)")],
    "exercise priced at the leaf index": [("payoff(S * u**j * d**(i - j)))", "payoff(S * u**j * d**(n - j)))")],
}
caught = {}
for name, reps in MUT.items():
    src = SOL
    for a, b in reps:
        check("mutation applies: " + name, src.count(a) == 1)
        src = src.replace(a, b)
    f = grade(src)
    caught[name] = f
    check("caught: " + name, len(f) >= 1)
for name, f in caught.items():
    print(f"  {name:36s} fails tests {f}")
named = ["discounting omitted", "q = 1/2", "q from a simple rate", "q from e^{rT}", "leaves range(n)", "dt = T/(n+1)", "one step back too few", "early exercise ignored"]
check("the four named slips are caught", all(caught[n] for n in named))


# ---------- route B: an independent tree at 40 digits ----------
def route_b(S, r, sigma, T, n, payoff, american):
    S, r, sigma, T = mp.mpf(S), mp.mpf(r), mp.mpf(sigma), mp.mpf(T)
    dt = T / n
    x = sigma * mp.sqrt(dt)
    u, d, g = mp.e ** x, mp.e ** (-x), mp.e ** (r * dt)
    if not (d < g < u):
        raise ValueError
    q = (g - d) / (u - d)
    node = lambda i, j: S * mp.e ** (x * (2 * j - i))
    if not american:
        # binomial sums: value today and the two step-1 values
        def euro(i, j):
            m = n - i
            return sum(mp.binomial(m, k) * q ** k * (1 - q) ** (m - k) * payoff(node(n, j + k)) for k in range(m + 1)) / g ** m
        v0, vd, vu = euro(0, 0), euro(1, 0), euro(1, 1)
    else:
        v = [payoff(node(n, j)) for j in range(n + 1)]
        for i in range(n - 1, -1, -1):
            v = [max((q * v[j + 1] + (1 - q) * v[j]) / g, payoff(node(i, j))) for j in range(i + 1)]
            if i == 1:
                vd, vu = v
        v0 = v[0]
        if n == 1:
            vd, vu = payoff(node(1, 0)), payoff(node(1, 1))
    return v0, (vu - vd) / (node(1, 1) - node(1, 0))


def mpmax(a, b):
    return a if a > b else b


P = {
    "put52": lambda s: mpmax(52 - s, 0),
    "strangle": lambda s: mpmax(45 - s, 0) + mpmax(s - 55, 0),
    "capped": lambda s: min(mpmax(s - 50, 0), mp.mpf(8)),
    "call50": lambda s: mpmax(s - 50, 0),
    "put100": lambda s: mpmax(100 - s, 0),
    "put130": lambda s: mpmax(130 - s, 0),
}
CASES = [
    ((50, 0.06, 0.3, 0.5, 1, "put52", False), 1),
    ((50, 0.06, 0.3, 0.5, 3, "put52", False), 2),
    ((50, 0.06, 0.3, 0.5, 3, "put52", True), 3),
    ((50, 0.06, 0.3, 0.5, 6, "strangle", True), 4),
    ((50, 0.06, 0.3, 0.5, 4, "capped", True), 5),
    ((50, 0.06, 0.3, 0.5, 4, "capped", False), 6),
    ((50, 0.06, 0.3, 0.5, 5, "call50", True), 7),
    ((100, 0.05, 0.2, 1, 200, "put100", True), 8),
    ((100, 0.05, 0.2, 1, 3, "put130", True), 9),
]
for args, k in CASES:
    S, r, sg, T, n, pk, am = args
    e = eval(tests[k - 1]["expect"])
    b = route_b(S, r, sg, T, n, P[pk], am)
    check(f"test {k} route A = route B", all(abs(float(bb) - ee) <= 1e-11 * max(1, abs(ee)) for bb, ee in zip(b, e)))
    check(f"test {k} call matches case", f"tree_value_delta({S}, {r}, {sg}, {T}, {n}," in tests[k - 1]["call"] and str(am) in tests[k - 1]["call"])
# test 7: the American call equals the European call (no dividends)
eu7 = route_b(50, 0.06, 0.3, 0.5, 5, P["call50"], False)
check("test 7 American call = European call", all(abs(float(a) - b) < 1e-11 for a, b in zip(eu7, eval(tests[6]["expect"]))))
# early exercise matters where the byKey lines say so
eu3 = route_b(50, 0.06, 0.3, 0.5, 3, P["put52"], False)
check("test 3 American put above European", eval(tests[2]["expect"])[0] > float(eu3[0]) + 0.1)
check("byKey test-3 European £4.75", f"{float(eu3[0]):.2f}" == "4.75" and "£4.75" in it["feedback"]["byKey"]["test-3"])
eu5 = route_b(50, 0.06, 0.3, 0.5, 4, P["capped"], False)
check("capped call: American above European", eval(tests[4]["expect"])[0] > float(eu5[0]) + 0.5)
eu4 = route_b(50, 0.06, 0.3, 0.5, 6, P["strangle"], False)
check("strangle: American above European", eval(tests[3]["expect"])[0] > float(eu4[0]))
# test 9: exercised today, value 30 and delta -1 exactly
check("test 9 is (30, -1)", eval(tests[8]["expect"]) == (30.0, -1.0))
# test 10: the arbitrage tree
check("test 10 raises", tests[9]["compare"] == "raises" and tests[9]["expect"] == "ValueError")
s10 = 0.02 * math.sqrt(1 / 4)
check("test 10: sigma root dt 0.01 below r dt 0.015", math.isclose(s10, 0.01) and math.isclose(0.06 * 0.25, 0.015) and math.exp(s10) < math.exp(0.015))
check("byKey test-10 numbers", "e^{0.01}" in it["feedback"]["byKey"]["test-10"] and "e^{0.015}" in it["feedback"]["byKey"]["test-10"])
# every other test tree is free of arbitrage
for args, k in CASES:
    S, r, sg, T, n = args[:5]
    dt = T / n
    check(f"test {k} tree has no arbitrage", math.exp(-sg * math.sqrt(dt)) < math.exp(r * dt) < math.exp(sg * math.sqrt(dt)))

# ---------- the hand value in the prose, by the one-step formula ----------
u1 = math.exp(0.3 * math.sqrt(0.5))
d1 = 1 / u1
g1 = math.exp(0.03)
q1 = (g1 - d1) / (u1 - d1)
fu, fd = max(52 - 50 * u1, 0), max(52 - 50 * d1, 0)
v1 = (q1 * fu + (1 - q1) * fd) / g1
D1 = (fu - fd) / (50 * u1 - 50 * d1)
# second route: the copy, Delta shares and cash B
B1 = (u1 * fd - d1 * fu) / (u1 - d1) / g1
check("hand: copy = q price", math.isclose(D1 * 50 + B1, v1, rel_tol=1e-12))
check("hand: test 1 expect", close((v1, D1), eval(tests[0]["expect"])))
check("prose £5.40 and -0.54", f"{v1:.2f}" == "5.40" and f"{D1:.2f}" == "-0.54" and "£5.40" in it["prose"] and "-0.54" in it["prose"])
check("prose inputs", "£50 share" in it["prose"] and "£52 put" in it["prose"] and "r = 6\\%" in it["prose"] and "T = 0.5" in it["prose"])

# ---------- sanity at scale: the 200-step American put near the 2,000-step one ----------
ns = {}
exec(SOL, ns)
v200 = eval(tests[7]["expect"])[0]
v2000 = ns["tree_value_delta"](100, 0.05, 0.2, 1, 2000, lambda s: max(100 - s, 0), True)[0]
check("200 steps within 1p of 2,000 steps", abs(v200 - v2000) < 0.01)
print(f"  American put 100/100: 200 steps {v200:.4f}, 2,000 steps {v2000:.4f}")

# ---------- homework limits ----------
check("6 to 12 items", 6 <= len(items) <= 12)
check("a difficulty 5", any(x.get("difficulty") == 5 for x in items))
check("difficulties 3 to 5", all(3 <= x.get("difficulty", 0) <= 5 for x in items))
check("one performance task", sum(1 for x in items if "performance" in x) == 1)
check("how names 10 tests", "10 hidden tests" in w["how"] and len(tests) == 10)

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
