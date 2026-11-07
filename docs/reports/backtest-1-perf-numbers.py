"""backtest level 1 performance task (h-breakout-twice): every number recomputed.

Run with a Python that has numpy and pandas 2.2 (the scratch venv):
    python docs/reports/backtest-1-perf-numbers.py
Runs the item's solution, its starter and ten planted bugs against every hidden
test, and recomputes the hand-made expectations by a second, exact route.
Exits 0 when every check passes.
"""
import json, math, os, sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app/content/courses/backtest/homework-1.json")
FAIL = []

def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

doc = json.load(open(HW, encoding="utf-8"))
item = next(i for i in doc["items"] if i["id"] == "h-breakout-twice")
w = item["widget"]

# ---- harness: one fresh namespace per case, as strict as the browser ----
def close_enough(a, b, tol):
    if isinstance(b, (list, tuple)):
        a = list(a) if not isinstance(a, list) else a
        return len(a) == len(b) and all(close_enough(x, y, tol) for x, y in zip(a, b))
    try:
        return math.isclose(float(a), float(b), rel_tol=tol.get("rel", 0), abs_tol=tol.get("abs", 0))
    except Exception:
        return False

def run_case(src, case):
    ns = {"__learner_source__": src, "__name__": "__main__"}
    try:
        exec(w["prelude"], ns)
        exec(src, ns)
        if "setup" in case:
            exec(case["setup"], ns)
        got = eval(case["call"], ns)
        want = eval(case["expect"], ns)
        if case.get("compare") == "isclose":
            return close_enough(got, want, case.get("tol", {"rel": 1e-9}))
        if hasattr(got, "tolist"):
            got = got.tolist()
        return got == want
    except Exception:
        return False

def results(src):
    return [run_case(src, c) for c in w["tests"]]

# ---- shape ----
tests, examples = w["tests"], w["examples"]
check("13 hidden tests, as `how` says", len(tests) == 13 and "13 hidden tests" in w["how"])
check("more tests than examples", len(tests) > len(examples) == 2)
check("examples are tests 1 and 2", examples == tests[:2])
check("homework has 6 to 12 items", 6 <= len(doc["items"]) <= 12)
check("one performance item in the homework", sum(1 for i in doc["items"] if i.get("performance")) == 1)

# ---- solution and starter ----
sol = results(w["solution"])
check("solution passes every test", all(sol))
st = results(w["starter"])
check("starter fails (at least one test)", not all(st))
print("     starter passes tests", [k + 1 for k, ok in enumerate(st) if ok])

# ---- planted bugs: each must fail at least one test ----
S = w["solution"]
def bug(old, new, src=None):
    src = S if src is None else src
    assert old in src, old
    return src.replace(old, new)

bugs = {
    "loop: today's target earns today's return": bug(
        "        out.append(target * ret)              # the target set at t - 1 earns it\n",
        "").replace("    return out\n", "        out.append(target * ret)\n    return out\n", 1),
    "vector: target not lagged": bug("(target.shift(1).fillna(0.0) * ret)", "(target * ret)"),
    "loop: channel includes today": bug("window = seen[t - n : t]", "window = seen[t - n + 1 : t + 1]"),
    "vector: channel includes today": bug("hi = c.rolling(n).max().shift(1)", "hi = c.rolling(n).max()").replace(
        "lo = c.rolling(n).min().shift(1)", "lo = c.rolling(n).min()"),
    "loop: no hold inside the channel": bug(
        "                target = -1                   # inside the channel: keep it\n",
        "                target = -1\n            else:\n                target = 0\n"),
    "vector: no hold inside the channel": bug("np.where(c < lo, -1.0, np.nan)", "np.where(c < lo, -1.0, 0.0)"),
    "vector: acts before n earlier closes": bug("hi = c.rolling(n).max().shift(1)", "hi = c.rolling(n, min_periods=1).max().shift(1)").replace(
        "lo = c.rolling(n).min().shift(1)", "lo = c.rolling(n, min_periods=1).min().shift(1)"),
    "vector: returns read with shift(-1)": bug("ret = c.pct_change().fillna(0.0)\n    return (target.shift(1).fillna(0.0) * ret).tolist()",
        "ret = c.pct_change().shift(-1).fillna(0.0)\n    return (target * ret).tolist()"),
    "vector: calls the loop": bug("    c = pd.Series(close, dtype=float)\n", "    return breakout_loop(close, n)\n    c = pd.Series(close, dtype=float)\n"),
    "loop: books the next bar's return": bug(
        "        ret = seen[t] / seen[t - 1] - 1 if t > 0 else 0.0\n        out.append(target * ret)              # the target set at t - 1 earns it\n",
        "").replace("    return out\n", "        out.append(target * (close[t + 1] / close[t] - 1) if t + 1 < len(close) else 0.0)\n    return out\n", 1),
    "agree: zip without a length check": bug("    return a.shape == b.shape and bool(np.allclose(a, b, rtol=0, atol=1e-9))",
        "    return all(abs(x - y) <= 1e-9 for x, y in zip(a, b))"),
    "agree: exact equality": bug("    return a.shape == b.shape and bool(np.allclose(a, b, rtol=0, atol=1e-9))",
        "    return list(a) == list(b)"),
    "agree: always True": bug("    return a.shape == b.shape and bool(np.allclose(a, b, rtol=0, atol=1e-9))", "    return True"),
}
for name, src in bugs.items():
    r = results(src)
    first = next((k + 1 for k, ok in enumerate(r) if not ok), None)
    check(f"planted bug caught: {name} (first failing test {first})", first is not None)

# byKey lines name the test each slip fails first
first_fail = {name: next((k + 1 for k, ok in enumerate(results(src)) if not ok), None) for name, src in bugs.items()}
check("byKey test-9: the loop call fails test 9 first", first_fail["vector: calls the loop"] == 9)
check("byKey test-12: zip fails test 12 first", first_fail["agree: zip without a length check"] == 12)
check("byKey test-13: exact equality fails test 13 first", first_fail["agree: exact equality"] == 13)
check("byKey test-7: the loop that books the next return fails test 7", not results(bugs["loop: books the next bar's return"])[6])
check("byKey test-8: shift(-1) on returns fails test 8", not results(bugs["vector: returns read with shift(-1)"])[7])

# ---- the hand-made expectations by a second, exact route ----
ns = {"__learner_source__": ""}
exec(w["prelude"], ns)
HAND, TIES = ns["HAND"], ns["_TIES"]
check("HAND holds ten closes (prose: ten hand-made ones)", len(HAND) == 10)
# targets worked by hand from the channel rule (see the report)
hand_targets = [0, 0, 0, 0, -1, -1, -1, 1, 1, 1]
tie_targets = [0, 0, 0, 0, 1, 1, -1, -1, -1]
check("hand targets match the reference", ns["_targets"](HAND, 3) == hand_targets)
check("tie targets match the reference", ns["_targets"](TIES, 2) == tie_targets)
def exact(close, tg):
    c = [Fraction(x).limit_denominator() for x in close]
    return [Fraction(0)] + [tg[t - 1] * (c[t] / c[t - 1] - 1) for t in range(1, len(c))]
for label, close, tg, case in (("HAND", HAND, hand_targets, tests[0]), ("ties", TIES, tie_targets, tests[2])):
    want = eval(case["expect"])
    if label == "ties":
        want = want[0]
    ex = exact(close, tg)
    check(f"{label} expectation equals exact fractions within 1e-9",
          all(abs(float(e) - x) <= 1e-9 for e, x in zip(ex, want)) and len(ex) == len(want))
check("HAND bar 5 return is +1/10 (short 1 into a 10% fall)", exact(HAND, hand_targets)[5] == Fraction(1, 10))
check("HAND bar 6 return is -1/9", exact(HAND, hand_targets)[6] == Fraction(-1, 9))

# the four functions handed to agree really do differ (or not) as the tests say
c = ns["walk"](300, 11)
ref, same = ns["_ref"](c, 15), ns["_same_bar"](c, 15)
check("same-bar version differs from the reference somewhere", any(abs(a - b) > 1e-6 for a, b in zip(ref, same)))
check("drop-last version is one shorter and equal elsewhere", ns["_drop_last"](c, 15) == ref[:-1])
check("nudged version is within 1e-9 everywhere", all(abs(a - b) <= 1e-9 for a, b in zip(ref, ns["_nudged"](c, 15))))

print("\n%d failure(s)" % len(FAIL))
sys.exit(1 if FAIL else 0)
