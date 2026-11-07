"""research-int L4 performance task h4-quote-at: every expected value two ways, then the
solution, the starter and ten planted bugs against every hidden test and example.
Run: python3 docs/reports/research-int-4-perf-numbers.py (exit 0 when all hold)."""
import json, math, os, sys, time
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
hw = json.load(open(os.path.join(here, "..", "..", "app", "content", "courses", "research-int", "homework-4.json")))
it = next(i for i in hw["items"] if i["id"] == "h4-quote-at")
w = it["widget"]
SOL, START, POST = w["solution"], w["starter"], w["postlude"]
fails = []
def ok(name, cond):
    print(("ok  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)

def close(a, b):
    if isinstance(a, (list, tuple)) or isinstance(b, (list, tuple)):
        return isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    if a is None or b is None:
        return a is None and b is None
    try:
        return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return a == b

# Route 2: an independent implementation with numpy (searchsorted and np.interp)
def quote_np(quotes, times, max_gap):
    good = [(t, p) for t, p in quotes if p is not None]
    if not good:
        return [None] * len(times)
    sec = np.array([t for t, _ in good], dtype=float)
    pr = np.array([p for _, p in good], dtype=float)
    xs, inv = np.unique(sec, return_inverse=True)
    ys = np.bincount(inv, weights=pr) / np.bincount(inv)
    tq = np.array(times, dtype=float)
    val = np.interp(tq, xs, ys)
    j = np.searchsorted(xs, tq, side="left")
    out = []
    for q, v, i in zip(tq, val, j):
        if i < len(xs) and xs[i] == q:
            out.append(float(ys[i]))
        elif i == 0:
            out.append(float(ys[0]) if xs[0] - q <= max_gap else None)
        elif i == len(xs):
            out.append(float(ys[-1]) if q - xs[-1] <= max_gap else None)
        else:
            out.append(float(v) if xs[i] - xs[i - 1] <= max_gap else None)
    return out

# Route 1: hand values, worked from the rules
HAND = [
    [100.0 + 1.0 * 4 / 10],
    [100.0 + 1.0 * 5 / 10, 101.0],
    [100.0 + 1.0 * 5 / 10, 101.0 + (99.0 - 101.0) * 10 / 20, 101.0],
    [101.0 + (99.0 - 101.0) * 15 / 20, 100.0, 101.0 + (99.0 - 101.0) * 2 / 20],
    [100.0 + (102.0 - 100.0) * 10 / 20, 102.0],
    [(101.0 + 103.0) / 2, 102.0 + (100.0 - 102.0) * 5 / 10, 100.0 + (102.0 - 100.0) * 5 / 10],
    [None, 110.0, 110.0 + 3.0 * 15 / 30],
    [100.0 + 6.0 * 30 / 60, None, 106.0],
    [50.0, None, 60.0, None],
    [[None, None], [None], [42.0, 42.0, None]],
    [(100.0 + 101.0 + 105.0) / 3 + (110.0 - (100.0 + 101.0 + 105.0) / 3) * 5 / 10, (100.0 + 101.0 + 105.0) / 3,
     (100.0 + 101.0 + 105.0) / 3 + (110.0 - (100.0 + 101.0 + 105.0) / 3) * 5 / 10],
]
cases = w["examples"] + w["tests"]
ns_sol = {}; exec(SOL + "\n" + POST, ns_sol)
ns_np = {"quote_at": quote_np}; exec(POST, ns_np)
for k, c in enumerate(cases):
    exp = eval(c["expect"])
    got = eval(c["call"], ns_sol)
    other = eval(c["call"], ns_np)
    label = f"case {k} {c['call'][:50]}"
    ok(label + ": solution = expect", close(got, exp))
    ok(label + ": numpy route = expect", close(other, exp))
    if k < len(HAND):
        ok(label + ": hand value = expect", close(HAND[k], exp))
big = eval(w["tests"][-1]["expect"])
print("   big_case:", big)

# Random agreement of the two routes, with repeats, None and boundary gaps
rng = np.random.default_rng(7)
agree = True
for _ in range(400):
    m = int(rng.integers(0, 12))
    qs = [(int(rng.integers(0, 60)), None if rng.random() < 0.2 else float(rng.integers(900, 1100)) / 10) for _ in range(m)]
    ts = [int(rng.integers(-20, 80)) for _ in range(15)]
    g = int(rng.integers(0, 25))
    ns = {}; exec(SOL, ns)
    if not close(ns["quote_at"](qs, ts, g), quote_np(qs, ts, g)):
        agree = False; break
ok("solution and numpy route agree on 400 random cases", agree)

# Grading as the engine does: a run passes only when every hidden test passes
def run(src, timed_n=None):
    ns = {}
    exec(src + "\n" + POST, ns)
    res = []
    for c in w["tests"]:
        call = c["call"]
        if call == "big_case()" and timed_n:
            t0 = time.perf_counter()
            try:
                ns["big_case"](timed_n)
            except Exception:
                pass
            dt = (time.perf_counter() - t0) * (40000 / timed_n) ** 2
            res.append(dt < 5.0 and close(eval(call, ns), eval(c["expect"])))
            continue
        try:
            res.append(close(eval(call, ns), eval(c["expect"])))
        except Exception:
            res.append(False)
    return res

t0 = time.perf_counter(); r = run(SOL); dt = time.perf_counter() - t0
ok(f"solution passes all {len(r)} hidden tests ({dt:.2f} s in CPython)", all(r))
ok("starter fails every hidden test", not any(run(START)))
ok("tests > examples and 3 or more", len(w["tests"]) >= 3 and len(w["tests"]) > len(w["examples"]))

def mutate(old, new):
    assert SOL.count(old) == 1, old
    return SOL.replace(old, new)

BUGS = {
    "no sort (arrival order)": mutate("xs = sorted(sums)", "xs = list(sums)"),
    "last quote wins at a repeated second": mutate("sums[t] = sums.get(t, 0.0) + p\n        counts[t] = counts.get(t, 0) + 1",
                                                  "sums[t] = p\n        counts[t] = 1"),
    "cancelled price read as 0": mutate("if p is None:\n            continue", "if p is None:\n            p = 0.0"),
    "no gap rule inside": mutate("elif xs[i] - xs[i - 1] > max_gap:", "elif False:"),
    "ends held for ever": mutate("out.append(ys[0] if xs[0] - t <= max_gap else None)", "out.append(ys[0])")
                          .replace("out.append(ys[-1] if t - xs[-1] <= max_gap else None)", "out.append(ys[-1])"),
    "strict max_gap (>= refuses)": mutate("elif xs[i] - xs[i - 1] > max_gap:", "elif xs[i] - xs[i - 1] >= max_gap:"),
    "answers in sorted order": mutate("for t in times:", "for t in sorted(times):"),
    "repeated asked seconds answered once": mutate("    return out\n", "    return list(dict(zip(times, out)).values())\n"),
    "mean of first and last repeat only": mutate("        sums[t] = sums.get(t, 0.0) + p\n        counts[t] = counts.get(t, 0) + 1\n",
        "        if t in sums:\n            sums[t] = first[t] + p\n            counts[t] = 2\n        else:\n            first[t] = p\n            sums[t], counts[t] = p, 1\n").replace(
        "sums, counts = {}, {}", "sums, counts, first = {}, {}, {}"),
}
# linear scan per asked second: correct but O(n) a query
BUGS["linear scan per second"] = SOL.replace("i = bisect.bisect_left(xs, t)",
                                             "i = 0\n        while i < len(xs) and xs[i] < t:\n            i += 1")
for name, src in BUGS.items():
    r = run(src, timed_n=2000 if "scan" in name else None)
    caught = [k + 1 for k, v in enumerate(r) if not v]
    ok(f"planted bug caught: {name}, fails tests {caught}", len(caught) > 0)
    if name == "linear scan per second":
        ok("linear scan fails only the timing test", caught == [10])

# the two value slips once caught only by the timing test: a fast test 9 now catches them
for name in ("repeated asked seconds answered once", "mean of first and last repeat only"):
    caught = [k + 1 for k, v in enumerate(run(BUGS[name])) if not v]
    ok(f"{name}: caught by value test 9, before the timing test 10 ({caught})", 9 in caught)

# byKey keys point at tests that exist, and the homework still meets its limits
keys = it["feedback"]["byKey"]
ok("byKey keys are tests 1 to 10", all(k.startswith("test-") and 1 <= int(k[5:]) <= len(w["tests"]) for k in keys))
ok("homework items 6 to 12", 6 <= len(hw["items"]) <= 12)
ok("one performance item in the homework", sum(1 for i in hw["items"] if i.get("performance")) == 1)
ok("at most 15 tests", len(w["tests"]) <= 15)

if fails:
    print("FAILED:", fails); sys.exit(1)
print("all checks pass")
