"""conditional L2 h-two-filters (numbers, exact) and L4 h-host-rules-code (code: shipped, starter, reader
solution, brute-force check on random games, planted slips). Run with the venv Python: python -I cond_two.py"""
import sys, pathlib, random, itertools
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from fractions import Fraction as F
from harness11 import item, summary, patched

bad = 0
def check(name, ok):
    global bad
    print(("ok   " if ok else "FAIL ") + name)
    bad += 0 if ok else 1

# ---------- L2: enumerate the eight outcomes (kind, J, V) under both models
b, hJ, fJ, hV, fV = F(2, 100), F(9, 10), F(6, 100), F(7, 10), F(3, 100)
def joint(stale):
    out = {}
    for kind in "BG":
        pk = b if kind == "B" else 1 - b
        for j, v in itertools.product((0, 1), repeat=2):
            if kind == "B" or not stale:
                pj = hJ if kind == "B" else fJ
                pv = hV if kind == "B" else fV
                p = (pj if j else 1 - pj) * (pv if v else 1 - pv)
            else:  # good tick, stale quote: V only with J; P(V | G) = fV, P(J | G) = fJ
                p = {(1, 1): fV, (1, 0): fJ - fV, (0, 1): F(0), (0, 0): 1 - fJ}[(j, v)]
            out[(kind, j, v)] = pk * p
    return out
for stale in (False, True):
    J = joint(stale)
    check(f"stale={stale}: the eight chances sum to 1", sum(J.values()) == 1)
    check(f"stale={stale}: P(V | G) = 0.03, P(J | G) = 0.06", sum(p for (k, j, v), p in J.items() if k == "G" and v) / (1 - b) == fV
          and sum(p for (k, j, v), p in J.items() if k == "G" and j) / (1 - b) == fJ)
J0, J1 = joint(False), joint(True)
pBJ = sum(p for (k, j, v), p in J0.items() if k == "B" and j) / sum(p for (k, j, v), p in J0.items() if j)
check("P(B | J) = 15/64 (enumeration)", pBJ == F(15, 64))
check("P(B | J) = 15/64 (formula)", hJ * b / (hJ * b + fJ * (1 - b)) == F(15, 64))
check("P(J) = 0.0768, paths 0.018 and 0.0588", hJ * b == F("0.018") and fJ * (1 - b) == F("0.0588") and hJ * b + fJ * (1 - b) == F("0.0768"))
pBJV = J0[("B", 1, 1)] / (J0[("B", 1, 1)] + J0[("G", 1, 1)])
check("P(B | J and V) = 50/57 (enumeration)", pBJV == F(50, 57))
check("N_B 0.0126, N_G 0.001764, total 0.014364", b * hJ * hV == F("0.0126") and (1 - b) * fJ * fV == F("0.001764") and b * hJ * hV + (1 - b) * fJ * fV == F("0.014364"))
check("odds 1/49 x 15 x 70/3 = 50/7", F(1, 49) * (hJ / fJ) * (hV / fV) == F(50, 7) and hJ / fJ == 15 and hV / fV == F(70, 3))
pS = J1[("B", 1, 1)] / (J1[("B", 1, 1)] + J1[("G", 1, 1)])
check("stale: P(B | J and V) = 3/10 (enumeration)", pS == F(3, 10))
check("stale: N_G 0.0294, total 0.042", J1[("G", 1, 1)] == F("0.0294") and J1[("B", 1, 1)] + J1[("G", 1, 1)] == F("0.042"))
check("stale: P(V | J, G) = 0.5, ratio 1.4, odds 15/49 to 3/7", J1[("G", 1, 1)] / (J1[("G", 1, 1)] + J1[("G", 1, 0)]) == F(1, 2)
      and hV / F(1, 2) == F(7, 5) and F(15, 49) * F(7, 5) == F(3, 7))
check("stale: the bad-tick part still holds, the good-tick part fails", J1[("B", 1, 1)] / b == hJ * hV and J1[("G", 1, 1)] / (1 - b) != fJ * fV)
check("decimals 0.234, 0.877, 0.3", round(float(F(15, 64)), 3) == 0.234 and round(float(F(50, 57)), 3) == 0.877)
check("0.0018 = fJ fV", fJ * fV == F("0.0018"))
# simulation, route 3
rng = random.Random(5)
hit = {False: [0, 0, 0, 0], True: [0, 0, 0, 0]}
for _ in range(600000):
    bad_t = rng.random() < 0.02
    for stale in (False, True):
        if bad_t:
            j, v = rng.random() < 0.9, rng.random() < 0.7
        elif not stale:
            j, v = rng.random() < 0.06, rng.random() < 0.03
        else:
            u = rng.random(); j, v = u < 0.06, u < 0.03
        h = hit[stale]
        if j:
            h[0] += 1; h[1] += bad_t
        if j and v:
            h[2] += 1; h[3] += bad_t
print(f"  simulated: P(B|J) {hit[False][1] / hit[False][0]:.4f}, P(B|JV) {hit[False][3] / hit[False][2]:.4f}, stale {hit[True][3] / hit[True][2]:.4f}")
check("simulation within 0.02 of 15/64, 50/57, 3/10", abs(hit[False][1] / hit[False][0] - 15 / 64) < 0.02 and abs(hit[False][3] / hit[False][2] - 50 / 57) < 0.03
      and abs(hit[True][3] / hit[True][2] - 0.3) < 0.03)

# ---------- L4 code
it = item("conditional", "homework-4.json", "h-host-rules-code")
w = it["widget"]
sol = w["solution"]
print("L4 h-host-rules-code")
f, _ = summary(w, sol, "shipped solution", "all"); check("shipped passes all", f == [])
f, _ = summary(w, w["starter"], "starter"); check("starter fails", len(f) > 0)
mine = r'''
from fractions import Fraction
def host_likelihood(n, pick, car, opened, host):
    # list the host's possible doors with their chances, then read off `opened` showing a goat
    if host == 'knows':
        doors = [d for d in range(n) if d not in (pick, car)]
        law = {d: Fraction(1, len(doors)) for d in doors}
    elif host == 'random':
        doors = [d for d in range(n) if d != pick]
        law = {d: Fraction(1, len(doors)) for d in doors}
    else:
        law = {min(d for d in range(n) if d not in (pick, car)): Fraction(1)}
    p = law.get(opened, Fraction(0))
    return float(p) if opened != car else 0.0
def door_posterior(prior, pick, opened, host):
    joint = [p * host_likelihood(len(prior), pick, c, opened, host) for c, p in enumerate(prior)]
    z = sum(joint)
    return None if z == 0 else [j / z for j in joint]
'''
f, _ = summary(w, mine, "reader solution (host's law listed per car place)", "all"); check("reader solution passes", f == [])
# brute force on random games: enumerate (car, host's door) with exact Fractions, compare with the shipped functions
ns = {}
exec(sol.replace("print(door_posterior", "_ = (door_posterior"), ns)
rng = random.Random(3)
mism = 0
for trial in range(1500):
    n = rng.randint(3, 8)
    wts = [rng.choice([0, 1, 2, 3, 5]) for _ in range(n)]
    if sum(wts) == 0:
        wts[0] = 1
    prior = [F(x, sum(wts)) for x in wts]
    pick = rng.randrange(n); host = rng.choice(["knows", "random", "lowest"])
    opened = rng.choice([d for d in range(n) if d != pick])
    seen = [F(0)] * n
    for car in range(n):
        if host == "knows":
            opts = [d for d in range(n) if d not in (pick, car)]; law = {d: F(1, len(opts)) for d in opts}
        elif host == "random":
            opts = [d for d in range(n) if d != pick]; law = {d: F(1, len(opts)) for d in opts}
        else:
            law = {min(d for d in range(n) if d not in (pick, car)): F(1)}
        for d, q in law.items():
            if d == opened and d != car:  # opened that door and a goat showed
                seen[car] += prior[car] * q
    z = sum(seen)
    want = None if z == 0 else [s / z for s in seen]
    got = ns["door_posterior"]([float(p) for p in prior], pick, opened, host)
    if (want is None) != (got is None) or (want is not None and any(abs(float(a) - b) > 1e-12 for a, b in zip(want, got))):
        mism += 1
check("shipped door_posterior equals brute force on 1,500 random games (3 to 8 doors, uneven priors)", mism == 0)
plants = [
    ("random host: no goat condition", [("    if opened == pick or opened == car:\n        return 0.0      # not your door; a car is no goat\n",
                                          "    if opened == pick or (opened == car and host != 'random'):\n        return 0.0\n")]),
    ("knowing host: always n - 2 doors", [("return 1 / len(allowed)", "return 1 / (n - 2)")]),
    ("knowing host: always n - 1 doors", [("return 1 / len(allowed)", "return 1 / (n - 1)")]),
    ("lowest host: highest door", [("first = min(", "first = max(")]),
    ("not normalised", [("return [p / total for p in paths]", "return paths")]),
    ("zeros instead of None", [("        return None\n", "        return [0.0] * n\n")]),
    ("even prior assumed", [("paths = [prior[c] *", "paths = [1 / n *")]),
    ("random host over all n doors", [("return 1 / (n - 1)  # any door but yours", "return 1 / n")]),
    ("host ignored: drop the opened door and renormalise", [("    paths = [prior[c] * host_likelihood(n, pick, c, opened, host)\n             for c in range(n)]",
                                                            "    paths = [0.0 if c == opened else prior[c] for c in range(n)]")]),
    ("lowest host may open the car", [("first = min(d for d in range(n) if d != pick and d != car)", "first = min(d for d in range(n) if d != pick)")]),
]
for name, pairs in plants:
    f, _ = summary(w, patched(sol, *pairs), "plant: " + name)
    check("plant caught: " + name, len(f) > 0)
# expects by exact Fractions, route 2
check("test 5 5/11 6/11", F(1, 2) * F(1, 2) / (F(1, 2) * F(1, 2) + F(3, 10)) == F(5, 11))
check("test 7: 4/27 8/27 9/27 6/27", [x / (F(1, 30) + F(2, 30) + F(3, 40) + F(15, 300)) for x in (F(1, 30), F(2, 30), F(3, 40), F(15, 300))] == [F(4, 27), F(8, 27), F(9, 27), F(6, 27)])
check("test 11: 1/10 and 9/80", F(1, 90) / (F(1, 90) + 8 * F(1, 80)) == F(1, 10) and F(1, 80) / (F(1, 90) + 8 * F(1, 80)) == F(9, 80))
print("failures:", bad)
sys.exit(1 if bad else 0)
