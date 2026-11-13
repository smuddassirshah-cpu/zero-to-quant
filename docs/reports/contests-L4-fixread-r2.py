#!/usr/bin/env python3
"""Fix-pass read, contests level 4, round 2 (commit 445e2e55).

Rebuilds every number in the changed sentences by two routes and submits each
mistake named by a changed feedback.byKey.test-N line to the widget's hidden
tests. Exits 0 when the content agrees with the checks. Rows judged
`imprecise` in the review are printed as NOTE lines and do not fail the run;
their replacement texts are checked here too.
Run from the repo root: python docs/reports/contests-L4-fixread-r2.py
"""
import itertools, json, math, os, random, re, subprocess, sys, time

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
C = os.path.join(ROOT, "app", "content", "courses", "contests")
fails = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (" | " + str(detail) if detail != "" else ""))
    if not ok:
        fails.append(name)


def load(f):
    return json.load(open(os.path.join(C, f), encoding="utf-8"))


def screen(d, title):
    return next(s for s in d["screens"] if s.get("title") == title)


def first_fail(widget, src):
    """Number N of the key test-N the page would give (0 when all pass).

    app/js/engine/widgets/code.js keys a failed check on the first failing
    row: `test-${first + 1}`.
    """
    env = {}
    exec(widget.get("prelude", "") + "\n" + src, env)
    for n, t in enumerate(widget["tests"], 1):
        try:
            if t.get("setup"):
                exec(t["setup"], env)
            ok = eval(t["call"], env) == eval(t["expect"], env)
        except Exception:
            ok = False
        if not ok:
            return n
    return 0


def correct_ids(s):
    return [o["id"] for o in s["widget"]["options"] if o.get("correct")]


# ---------------------------------------------------------------- l13
d13 = load("l13-virtual-contest.json")
s13 = next(x for x in d13["screens"] if "min_capacity" in x.get("widget", {}).get("solution", ""))
w = s13["widget"]
check("l13 solution passes", first_fail(w, w["solution"]) == 0)


def greedy_groups(ws, cap):
    out, cur = [], []
    for x in ws:
        if sum(cur) + x > cap:
            out.append(cur)
            cur = []
        cur.append(x)
    return out + [cur]


def best_cap(ws, k):
    """Second route: brute force over every split into at most k runs."""
    n, best = len(ws), None
    for r in range(0, k):
        for cuts in itertools.combinations(range(1, n), r):
            b = [0, *cuts, n]
            m = max(sum(ws[b[i]:b[i + 1]]) for i in range(len(b) - 1))
            best = m if best is None else min(best, m)
    return best


EX = [4, 8, 2, 7, 5, 3]
check("l13 test-1: 11 needs 4 days, grouped 4 | 8 2 | 7 | 5 3", greedy_groups(EX, 11) == [[4], [8, 2], [7], [5, 3]])
check("l13 test-1: answer 12 by brute force over splits", best_cap(EX, 3) == 12 and w["tests"][0]["expect"] == "12")
check("l13 test-2 is can_ship alone at 11 in 3 days",
      w["tests"][1]["call"] == "can_ship([4, 8, 2, 7, 5, 3], 3, 11)" and w["tests"][1]["expect"] == "False")

SEARCH = '''
def min_capacity(weights, k):
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(weights, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
'''
days0 = '''
def can_ship(weights, k, cap):
    days, load = 0, 0
    for w in weights:
        if w > cap:
            return False
        if load + w > cap:
            days += 1
            load = 0
        load += w
    return days <= k
''' + SEARCH
env = {}
exec(w["prelude"] + days0, env)
check("l13 test-1 mistake A (days counted from 0) lands test-1 with less than 12",
      first_fail(w, days0) == 1 and env["min_capacity"](EX, 3) < 12, env["min_capacity"](EX, 3))
nolast = '''
def can_ship(weights, k, cap):
    days, load = 0, 0
    for w in weights:
        if w > cap:
            return False
        load += w
        if load > cap:
            days += 1
            load = w
    return days <= k
''' + SEARCH
check("l13 test-1 mistake B (last part-day never counted) lands test-1", first_fail(w, nolast) == 1)
good_ship = w["solution"].split("def min_capacity")[0]
lo1 = good_ship + SEARCH.replace("return lo", "return lo - 1")
check("l13 test-1 mistake C (search returns lo - 1 = 11) lands test-1", first_fail(w, lo1) == 1)
comp = days0.replace("can_ship(weights, k, mid)", "can_ship(weights, k - 1, mid)")
check("l13 test-2 mistake (can_ship a day generous, search compensates) lands test-2", first_fail(w, comp) == 2)

# ---------------------------------------------------------------- l14
d14 = load("l14-which-first.json")
s = screen(d14, "One score")
check("l14 rule on screen: v/250 a minute, floor 0.3v", "v / 250" in s["prose"] and "0.3v" in s["prose"])
check("l14 a two-hour round is stated by the lesson", "two-hour round" in d14["screens"][0]["prose"])
check("l14 B = 810", 1000 - 4 * 35 - 50 == 810 and max(0.3 * 1000, 1000 * (1 - 35 / 250) - 50) == 810)
check("l14 'at most 48%': 120/250", abs(120 / 250 - 0.48) < 1e-12 and "at most 48%" in s["explain"]["text"])
TABLE = (500, 1000, 1500, 2000)
worst = max((v - (v - v / 250 * t)) / v for v in TABLE for t in range(121))
check("l14 48% by scan of every problem and minute", abs(worst - 0.48) < 1e-12)
check("l14 no rejections: score always above the floor", all(v - v / 250 * t > 0.3 * v for v in TABLE for t in range(121)))
check("l14 floor is reachable with rejections (A, minute 120, three rejections)", 500 - 240 - 150 < 0.3 * 500)

s = screen(d14, "How long on D?")
check("l14 curve on screen",
      s["canvas"]["params"]["functions"][0]["expr"] == "1000*(1 - exp(-x/50)) + 800*(1 - exp(-(60 - x)/15))")
E = lambda x: 1000 * (1 - math.exp(-x / 50)) + 800 * (1 - math.exp(-(60 - x) / 15))
xb = max((i / 1000 for i in range(60001)), key=E)
x_closed = (60 / 15 - math.log(800 / 15 / 20)) / (1 / 50 + 1 / 15)  # E'(x) = 0
check("l14 best fixed split about 35 minutes, about 1,152",
      abs(xb - x_closed) < 2e-3 and round(xb) == 35 and round(E(xb)) == 1152, (round(xb, 2), round(E(xb), 1)))
check("l14 all D 699, all E 785", round(E(60)) == 699 and round(E(0)) == 785)
check("l14 E is the better rate (points per mean minute)", 800 / 15 > 1000 / 50)


# leave a problem once solved: the first until solved (or the hour ends), the second gets the rest
def leave_closed(v1, m1, v2, m2, T=60.0):
    a, b = 1 / m1, 1 / m2
    second = (1 - math.exp(-a * T)) - a * math.exp(-b * T) * (1 - math.exp(-(a - b) * T)) / (a - b)
    return v1 * (1 - math.exp(-a * T)) + v2 * second


def leave_quad(v1, m1, v2, m2, T=60.0, n=200000):
    h, tot = T / n, 0.0
    for i in range(n):
        t = (i + 0.5) * h
        tot += math.exp(-t / m1) / m1 * (v1 + v2 * (1 - math.exp(-(T - t) / m2))) * h
    return tot


def leave_mc(v1, m1, v2, m2, T=60.0, n=400000, seed=14):
    g, tot = random.Random(seed), 0.0
    for _ in range(n):
        t1 = g.expovariate(1 / m1)
        if t1 < T:
            tot += v1
            if g.expovariate(1 / m2) < T - t1:
                tot += v2
    return tot / n


e_first, d_first = leave_closed(800, 15, 1000, 50), leave_closed(1000, 50, 800, 15)
mc_e, mc_d = leave_mc(800, 15, 1000, 50), leave_mc(1000, 50, 800, 15)
# Monte Carlo standard error is under 1.5 points at n = 400,000
check("l14 E first then D: about 1,363 (closed form, quadrature, Monte Carlo)",
      round(e_first) == 1363 and abs(leave_quad(800, 15, 1000, 50) - e_first) < 0.01 and abs(mc_e - e_first) < 5,
      (round(e_first, 2), round(mc_e, 1)))
check("l14 D first then E is worse", d_first < e_first - 50 and abs(mc_d - d_first) < 5,
      (round(d_first, 2), round(mc_d, 1)))
check("l14 text: start with E, about 1,363",
      "start with E, the better rate, and give D the rest: about 1,363 expected" in s["explain"]["text"])


def dp(T=60.0, n=60000):
    """Best rule of any kind: value with both unsolved and t minutes left."""
    h, V, always_e = T / n, 0.0, True
    for i in range(1, n + 1):
        t = i * h
        VD, VE = 1000 * (1 - math.exp(-t / 50)), 800 * (1 - math.exp(-t / 15))
        gE, gD = (800 + VD - V) / 15, (1000 + VE - V) / 50
        always_e = always_e and gE >= gD
        V += h * max(gE, gD)
    return V, always_e


V, always_e = dp()
check("l14 E first is the best rule in this model (dynamic programme)", always_e and abs(V - e_first) < 0.5, round(V, 2))


def d_cap(c, n=100000, seed=7):
    """D first for at most c minutes, then E, then back to D once E is solved."""
    g, tot = random.Random(seed), 0.0
    for _ in range(n):
        td, te = g.expovariate(1 / 50), g.expovariate(1 / 15)
        if td < c:
            tot += 1000 + (800 if te < 60 - td else 0)
        elif te < 60 - c:
            tot += 800 + (1000 if td - c < 60 - c - te else 0)
    return tot / n


caps = {c: d_cap(c) for c in (15, 30, 35, 45, 60)}
check("l14 D first under caps of 15 to 60 minutes never beats E first",
      all(v < e_first + 4 for v in caps.values()), {c: round(v) for c, v in caps.items()})

s = screen(d14, "Triage on a desk")
rows = {r[0]: (int(re.sub(r"[^\d]", "", r[1])), int(r[2])) for r in s["canvas"]["params"]["rows"]}
q, hdg, rec = rows["Quote a client"], rows["Hedge a position"], rows["Reconcile a break"]
check("l14 rates 600, 480, 100", (q[0] / q[1], hdg[0] / hdg[1], rec[0] / rec[1]) == (600, 480, 100))
check("l14 quote and hedge fill the half hour; the break does not fit", q[1] + hdg[1] == 30 and rec[1] > 0)
check("l14 waiting costs £600 and £750 at 1% a minute", 0.01 * q[1] * hdg[0] == 600 and 0.01 * hdg[1] * q[0] == 750)


def desk_value(order):
    tot, clock = 0.0, 0
    for k in order:
        v, m = rows[k]
        if clock + m <= 30:
            tot += v * (1 - 0.01 * clock)
            clock += m
    return tot


best = max(itertools.permutations(rows), key=desk_value)
check("l14 best order by enumeration: quote, hedge", best[:2] == ("Quote a client", "Hedge a position"), desk_value(best))
check("l14 keyed choice is the quote", correct_ids(s) == ["quote"])

# ---------------------------------------------------------------- l15
d15 = load("l15-debugging-under-time.json")
titles = [x["title"] for x in d15["screens"]]
i = titles.index("The debugging routine")
check("l15 the two screens before the routine: reread, then hand cases",
      "reread the statement" in d15["screens"][i - 2]["prose"] and "hand-made edge cases" in d15["screens"][i - 1]["prose"])
check("l15 routine key s1..s4", d15["screens"][i]["widget"]["answer"] == ["s1", "s2", "s3", "s4"])

s = screen(d15, "Fix 2: strictly greater")
w = s["widget"]
check("l15 inversions: solution passes, starter fails at 3", first_fail(w, w["solution"]) == 0 and first_fail(w, w["starter"]) == 3)
X = [2, 1, 2, 1]
pairs = [(a, b) for a in range(4) for b in range(a + 1, 4) if X[a] > X[b]]
check("l15 test-6: [2,1,2,1] has inversions (0,1), (0,3), (2,3)", pairs == [(0, 1), (0, 3), (2, 3)] and w["tests"][5]["expect"] == "3")
BODY = w["solution"].split("\n", 1)[1]
dedupe_ordered = "def count_inversions_small(xs):\n    xs = list(dict.fromkeys(xs))\n" + BODY
dedupe_set = "def count_inversions_small(xs):\n    xs = list(set(xs))\n" + BODY
dedupe_sorted = "def count_inversions_small(xs):\n    xs = sorted(set(xs))\n" + BODY
value_pairs = ("def count_inversions_small(xs):\n    n = len(xs)\n    seen = set()\n    for i in range(n):\n"
               "        for j in range(i + 1, n):\n            if xs[i] > xs[j]:\n                seen.add((xs[i], xs[j]))\n"
               "    return len(seen)\n")
r = [first_fail(w, x) for x in (dedupe_ordered, value_pairs, dedupe_set, dedupe_sorted)]
check("l15 test-6: order-keeping dedupe and counting each value pair once land test-6", r[:2] == [6, 6], r)
if r[2:] != [6, 6]:
    print("NOTE l15 test-6: list(set(xs)) and sorted(set(xs)) land test-%d and test-%d, not test-6 (row imprecise)" % tuple(r[2:]))

s = screen(d15, "Debug prints")
check("l15 debug-print key is stderr", correct_ids(s) == ["stderr"])
PROG = "import sys\nfor c in range(2):\n    %s\n    print(c + 1)\n"


def stdout_of(body):
    return subprocess.run([sys.executable, "-c", PROG % body], capture_output=True, text=True).stdout


check("l15 a debug line on stdout changes what is compared; on stderr it does not",
      stdout_of("print('debug', c)") != "1\n2\n" and stdout_of("print('debug', c, file=sys.stderr)") == "1\n2\n")


def timed(body):
    src = "import sys\nfor i in range(300000):\n    %s\n" % body
    best = 9e9
    for _ in range(3):
        t0 = time.perf_counter()
        subprocess.run([sys.executable, "-c", src], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        best = min(best, time.perf_counter() - t0)
    return best


quiet, loud = timed("pass"), timed("print('debug: case', i, file=sys.stderr)")
check("l15 writing 300,000 debug lines to stderr costs run time", loud > quiet + 0.03, (round(quiet, 3), round(loud, 3)))

# ---------------------------------------------------------------- l16
d16 = load("l16-upsolving.json")
s = screen(d16, "Upsolve D")
w = s["widget"]
check("l16 equal_thirds solution passes", first_fail(w, w["solution"]) == 0)
T6 = [1, -1, 1, -1, 1, -1]
check("l16 test-6: negatives, total 0, prefix rises and falls",
      min(T6) < 0 and sum(T6) == 0 and list(itertools.accumulate(T6)) == [1, 0, 1, 0, 1, 0]
      and w["tests"][5]["call"] == "equal_thirds(%r)" % T6)


def brute(xs):
    n = len(xs)
    return sum(1 for a in range(1, n) for b in range(a + 1, n) if sum(xs[:a]) == sum(xs[a:b]) == sum(xs[b:]))


def formula(xs):
    """Summary formula: j <= n-1 with P_j = 2S/3, counting 1 <= i < j with P_i = S/3."""
    n, S = len(xs), sum(xs)
    Pk = [0, *itertools.accumulate(xs)]
    return sum(sum(1 for a in range(1, b) if 3 * Pk[a] == S) for b in range(1, n) if 3 * Pk[b] == 2 * S)


g = random.Random(16)
cases = [[g.randint(-2, 2) for _ in range(g.randint(1, 9))] for _ in range(4000)] + [T6, [1, 2, 3, 0, 3], [0] * 5]
env = {}
exec(w["solution"], env)
check("l16 summary formula = brute force = solution on 4,003 cases",
      all(brute(c) == formula(c) == env["equal_thirds"](c) for c in cases))
tex = d16["summary"]["formula"]["tex"]
check("l16 formula text carries both bounds", "j \\le n-1" in tex and "1 \\le i < j" in tex)
check("l16 test-6 expects 1", brute(T6) == 1 and w["tests"][5]["expect"] == "1")
HEAD = ("def equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n"
        "    ways, firsts, prefix = 0, 0, 0\n    for j in range(len(xs) - 1):\n        prefix += xs[j]\n")
TAIL = ("        if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n"
        "            firsts += 1\n    return ways\n")
stop_top = HEAD + "        if prefix > 2 * third:\n            break\n" + TAIL
stop_end = HEAD + TAIL.replace("    return ways", "        if prefix > 2 * third:\n            break\n    return ways")
stop_while = ("def equal_thirds(xs):\n    total = sum(xs)\n    if total % 3 != 0:\n        return 0\n    third = total // 3\n"
              "    n, ways, firsts, prefix, j = len(xs), 0, 0, 0, 0\n"
              "    while j < n - 1 and prefix + xs[j] <= 2 * third:\n        prefix += xs[j]\n        j += 1\n"
              "        if prefix == 2 * third:\n            ways += firsts\n        if prefix == third:\n"
              "            firsts += 1\n    return ways\n")
r = [first_fail(w, x) for x in (stop_top, stop_end, stop_while)]
check("l16 test-6: three codings of 'stop once the prefix passes 2S/3' land test-6", r == [6, 6, 6], r)
stop_first = HEAD + TAIL.replace("            ways += firsts\n", "            ways += firsts\n            break\n")
check("l16 the old wording (stop at the first match) lands test-1, so the change was needed", first_fail(w, stop_first) == 1)

s = screen(d16, "A week's plan")
check("l16 100 to 200 above 1,250 is 1,350 to 1,450; 2000 is 750 above",
      (1250 + 100, 1250 + 200, 2000 - 1250) == (1350, 1450, 750) and "rated 1350 to 1450" in json.dumps(s)
      and correct_ids(s) == ["a"])
check("l16 the upsolving rule (300 above) is a separate rule on its own screens",
      "at most about 300 above" in json.dumps(d16) and "practise about 100 to 200 above" in json.dumps(s))

# ---------------------------------------------------------------- voice, changed strings and replacements
hw = load("homework-4.json")
CHANGED = {
    "l13 test-1": s13["feedback"]["byKey"]["test-1"],
    "l13 test-2": s13["feedback"]["byKey"]["test-2"],
    "l14 one score explain": screen(d14, "One score")["explain"]["text"],
    "l14 split explain": screen(d14, "How long on D?")["explain"]["text"],
    "l14 desk explain": screen(d14, "Triage on a desk")["explain"]["text"],
    "l14 desk correct": screen(d14, "Triage on a desk")["feedback"]["correct"],
    "l15 routine prose": screen(d15, "The debugging routine")["prose"],
    "l15 routine generic": screen(d15, "The debugging routine")["feedback"]["generic"],
    "l15 routine explain": screen(d15, "The debugging routine")["explain"]["text"],
    "l15 test-6": screen(d15, "Fix 2: strictly greater")["feedback"]["byKey"]["test-6"],
    "l15 prints prose": screen(d15, "Debug prints")["prose"],
    "l15 prints explain": screen(d15, "Debug prints")["explain"]["text"],
    "l16 D prose": screen(d16, "Upsolve D")["prose"],
    "l16 test-6": screen(d16, "Upsolve D")["feedback"]["byKey"]["test-6"],
    "replacement l15 test-6": "Test 6, `[2, 1, 2, 1]`, has 3 inversions: the first 2 is larger than both 1s, and the "
                              "second 2 than the last 1. If you dropped repeats but kept their order, or counted each "
                              "pair of values once, count every copy.",
}


def sentences(txt):
    txt = re.sub(r"`[^`]*`|\$[^$]*\$", "X", txt)
    return [x for x in re.split(r"(?<=[.?])\s+(?=[A-Z`$])", txt) if x.strip()]


for name, txt in CHANGED.items():
    longest = max(len(x.split()) for x in sentences(txt))
    check("voice " + name, longest <= 35 and "!" not in txt and "—" not in txt, longest)
for d, names in ((d14, ("One score", "How long on D?", "Triage on a desk")), (d15, ("The debugging routine", "Debug prints"))):
    for name in names:
        check("explain at most three sentences: " + name, len(sentences(screen(d, name)["explain"]["text"])) <= 3)
check("homework-4 ratings are given as our estimate",
      sum("by our estimate)" in x.get("prose", "") for x in hw.get("problems", hw.get("items", hw.get("screens", [])))) == 3
      or json.dumps(hw).count("by our estimate)") == 3)

print("\n%d failing" % len(fails))
sys.exit(1 if fails else 0)
