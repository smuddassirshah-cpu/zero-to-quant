"""Reader checks for trees L2 `h-perf-any-payoff` (review-perf-retrofit-10): every expect recomputed by a second
route (a 40-digit mpmath tree with the node price S u^(2j - i) and q from the growth factor), the early-exercise
claims of the feedback checked node by node, a reader solution written independently, reader-planted slips, the
shipped solution and the starter run on every example and hidden test through harness10 (code.js rules: isclose at
rel 1e-9, abs 1e-12; raises by class). Run from this folder with the venv Python, -I. Exits 1 on any mismatch."""
import sys, os, math, time
import mpmath as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness10 import item, summary

mp.mp.dps = 40
bad = 0


def check(name, ok, info=""):
    global bad
    print(("ok   " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""))
    bad += 0 if ok else 1


def expect(widget, src, label, want, which="tests"):
    global bad
    fails, r = summary(widget, src, label, which)
    if want is not None and fails != want:
        bad += 1
        print("     MISMATCH: wanted", want, "got", fails, [x[1][:60] for x in r])
    return fails


it = item("trees", "homework-2.json", "h-perf-any-payoff")
w = it["widget"]
print("trees L2 h-perf-any-payoff")


def tree_mp(S, r, sigma, T, n, payoff, american, log=None):
    S, r, sigma, T = mp.mpf(S), mp.mpf(r), mp.mpf(sigma), mp.mpf(T)
    dt = T / n
    u = mp.e ** (sigma * mp.sqrt(dt))
    g = mp.e ** (r * dt)
    if not (1 / u < g < u):
        raise ValueError
    q = (g - 1 / u) / (u - 1 / u)
    V = {j: mp.mpf(payoff(S * u ** (2 * j - n))) for j in range(n + 1)}
    step1 = None
    for i in range(n - 1, -1, -1):
        W = {}
        for j in range(i + 1):
            hold = (q * V[j + 1] + (1 - q) * V[j]) / g
            ex = mp.mpf(payoff(S * u ** (2 * j - i)))
            W[j] = max(hold, ex) if american else hold
            if log is not None and american and ex > hold:
                log.append((i, j))
        V = W
        if i == 1:
            step1 = dict(V)
    if n == 1:
        step1 = {j: mp.mpf(payoff(S * u ** (2 * j - 1))) for j in range(2)}
    delta = (step1[1] - step1[0]) / (S * u - S / u)
    return V[0], delta


lam = {}
for i, c in enumerate(w["tests"]):
    call = c["call"]
    if c["compare"] == "raises":
        try:
            eval(call.replace("tree_value_delta", "tree_mp"), {"tree_mp": tree_mp})
            check(f"test {i + 1} raises in route 2", False)
        except ValueError:
            check(f"test {i + 1} raises in route 2 (u = e^0.01 < e^0.015)", math.exp(0.01) < math.exp(0.015))
        continue
    v, d = eval(call.replace("tree_value_delta", "tree_mp"), {"tree_mp": tree_mp, "max": max, "min": min})
    ev, ed = eval(c["expect"])
    ok = abs(float(v) / ev - 1) < 1e-12 and abs(float(d) / ed - 1) < 1e-12
    check(f"test {i + 1} expect by a 40-digit tree", ok, f"{float(v):.12f}, {float(d):.12f}")

# the feedback's claims
put = lambda s: max(52 - s, 0)
e3 = tree_mp(50, 0.06, 0.3, 0.5, 3, put, False)[0]
a3 = tree_mp(50, 0.06, 0.3, 0.5, 3, put, True)[0]
check("test 3: American put above its European twin, which is 4.75", a3 > e3 and round(float(e3), 2) == 4.75, f"{float(a3):.4f} > {float(e3):.4f}")
cap = lambda s: min(max(s - 50, 0), 8)
log = []
a5 = tree_mp(50, 0.06, 0.3, 0.5, 4, cap, True, log)[0]
e5 = tree_mp(50, 0.06, 0.3, 0.5, 4, cap, False)[0]
check("test 5: the capped call is exercised early somewhere, and is worth more American", a5 > e5 and len(log) > 0, f"nodes {log}")
call = lambda s: max(s - 50, 0)
log = []
a7 = tree_mp(50, 0.06, 0.3, 0.5, 5, call, True, log)
e7 = tree_mp(50, 0.06, 0.3, 0.5, 5, call, False)
check("test 7: no node exercises the plain call early; American equals European", not log and a7 == e7)
log = []
a9 = tree_mp(100, 0.05, 0.2, 1, 3, lambda s: max(130 - s, 0), True, log)
check("test 9: root and both step-1 nodes exercised, value 30, delta -1", (0, 0) in log and (1, 0) in log and (1, 1) in log and abs(a9[0] - 30) < 1e-30 and abs(a9[1] + 1) < 1e-30, f"{sorted(log)}")
# the prose's hand case
v1, d1 = tree_mp(50, 0.06, 0.3, 0.5, 1, put, False)
check("prose: £5.40 and delta -0.54", round(float(v1), 2) == 5.40 and round(float(d1), 2) == -0.54)

# ---------- shipped solution and starter ----------
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution on the example", [], "examples")
f = expect(w, w["starter"], "starter", None)
check("starter fails every test", len(f) == len(w["tests"]))

# ---------- reader solution: one list, updated in place, node price S u^(2j - i) ----------
READER = '''
import math
def tree_value_delta(S, r, sigma, T, n, payoff, american):
    h = T / n
    u = math.exp(sigma * math.sqrt(h))
    d = math.exp(-sigma * math.sqrt(h))
    a = math.exp(r * h)
    if not (d < a < u):
        raise ValueError("tree admits arbitrage")
    p = (a - d) / (u - d)
    vals = [payoff(S * u ** (2 * j - n)) for j in range(n + 1)]
    one = None
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            cont = (p * vals[j + 1] + (1 - p) * vals[j]) / a
            vals[j] = max(cont, payoff(S * u ** (2 * j - i))) if american else cont
        vals.pop()
        if i == 1:
            one = vals[:]
    if one is None:
        one = [payoff(S * d), payoff(S * u)]
    return vals[0], (one[1] - one[0]) / (S * (u - d))
'''
expect(w, READER, "reader solution", [])

S0 = w["solution"]
SLIPS = {
    "no comparison at the root": (S0.replace("        if american:\n", "        if american and i > 0:\n"), None),
    "delta before the comparison": (S0.replace("        if american:\n            v = [max(hold, payoff(S * u**j * d**(i - j)))\n                 for j, hold in enumerate(v)]\n        if i == 1:\n            first = v",
                                               "        if i == 1:\n            first = v\n        if american:\n            v = [max(hold, payoff(S * u**j * d**(i - j)))\n                 for j, hold in enumerate(v)]"), None),
    "one discount e^(-rT) at the end": (S0.replace("v = [disc * (q *", "v = [(q *").replace("return v[0], delta", "return v[0] * math.exp(-r * T), delta"), None),
    "simple interest 1 + r dt": (S0.replace("grow = math.exp(r * dt)", "grow = 1 + r * dt"), None),
    "no arbitrage check": (S0.replace('        raise ValueError("arbitrage: need d < e^(r dt) < u")', "        pass"), [10]),
    "American ignored": (S0.replace("        if american:\n", "        if False:\n"), None),
    "q on the wrong leaf": (S0.replace("q * v[j + 1] + (1 - q) * v[j]", "q * v[j] + (1 - q) * v[j + 1]"), None),
    "dt = T / (n + 1)": (S0.replace("dt = T / n", "dt = T / (n + 1)"), None),
    "exercise compared with the leaf payoff of the node above": (S0.replace("payoff(S * u**j * d**(i - j))", "payoff(S * u**(j + 1) * d**(i - j))"), None),
}
for name, (src, want) in SLIPS.items():
    if src == S0:
        check(f"slip '{name}' differs from the solution", False)
        continue
    f = expect(w, src, "slip: " + name, want)
    check(f"slip '{name}' is caught", len(f) > 0, f"fails {f}")

# timing: a reasonable but slow correct solution (recursion over paths is not reasonable at n = 200; a dict of nodes is)
DICT = '''
import math
def tree_value_delta(S, r, sigma, T, n, payoff, american):
    dt = T / n; u = math.exp(sigma * math.sqrt(dt)); d = 1 / u; g = math.exp(r * dt)
    if not d < g < u: raise ValueError
    q = (g - d) / (u - d)
    V = {(n, j): payoff(S * u**j * d**(n - j)) for j in range(n + 1)}
    for i in range(n - 1, -1, -1):
        for j in range(i + 1):
            h = (q * V[(i + 1, j + 1)] + (1 - q) * V[(i + 1, j)]) / g
            V[(i, j)] = max(h, payoff(S * u**j * d**(i - j))) if american else h
    return V[(0, 0)], (V[(1, 1)] - V[(1, 0)]) / (S * u - S * d)
'''
t0 = time.time()
expect(w, DICT, "reader dict-of-nodes solution", [])
check("dict-of-nodes solution well inside the 5 s case limit", time.time() - t0 < 2.0, f"{time.time() - t0:.2f} s for all 10")

print("failures:", bad)
sys.exit(1 if bad else 0)
