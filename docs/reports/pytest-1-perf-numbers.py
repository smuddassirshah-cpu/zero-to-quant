"""pytest level 1 performance task (homework-1 `h-average-cost-tests`): every number and claim recomputed.

Run with the scratch venv (pytest 8.1.1, as Pyodide 0.27.7 ships):
    <venv>/bin/python docs/reports/pytest-1-perf-numbers.py
It runs the item as js/engine/widgets/code.js does (one load of prelude, learner code and
postlude in a fresh directory, then every hidden case in order), for the solution, the
starter and twelve plausible wrong test files. Each stated figure is computed twice.
Exits 0 when every check passes.
"""
import contextlib, io, json, math, os, sys, tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app/content/courses/pytest/homework-1.json")
FAIL = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)


doc = json.load(open(HW, encoding="utf-8"))
item = next(i for i in doc["items"] if i["id"] == "h-average-cost-tests")
w = item["widget"]


def run(src, which="tests"):
    """code.js function mode: load once, then each case's setup and call in one namespace."""
    cwd, path0 = os.getcwd(), list(sys.path)
    os.chdir(tempfile.mkdtemp(prefix="zq-"))
    for m in ("costs", "test_mine"):
        sys.modules.pop(m, None)
    ns = {"__name__": "__zq__", "__learner_source__": src}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                exec(compile(w["prelude"], "<prelude>", "exec"), ns)
                exec(compile(src, "solution.py", "exec"), ns)
                exec(compile(w["postlude"], "<postlude>", "exec"), ns)
            except Exception:
                return [False] * len(w[which]), ns
            out = []
            for c in w[which]:
                try:
                    if c.get("setup"):
                        exec(c["setup"], ns)
                    out.append(eval(c["call"], ns) == eval(c["expect"], ns))
                except Exception:
                    out.append(False)
            return out, ns
    finally:
        os.chdir(cwd)
        sys.path[:] = path0


def failing(res):
    return [k + 1 for k, ok in enumerate(res) if not ok]


# ---- shape and the counts the item states ----
tests = w["tests"]
check("12 hidden tests and 1 example, as `how` says", len(tests) == 12 and len(w["examples"]) == 1
      and "12 hidden tests" in w["how"])
calls = [t["call"] for t in tests]
right = [c for c in calls if c.startswith("trial('right") and "reverse" not in c]
broken = [c for c in calls if c.startswith("trial(") and "right" not in c]
check("three correct versions, six broken (how: 'three correct', 'six broken')",
      len(right) == 3 and len(broken) == 6 and "three correct versions" in w["how"] and "six broken versions" in w["how"])
check("homework keeps 6 to 12 items, one performance item, one difficulty 5",
      6 <= len(doc["items"]) <= 12 and sum(1 for i in doc["items"] if i.get("performance")) == 1
      and any(i["difficulty"] == 5 for i in doc["items"]))
check("performance code item, no parts, starter and solution present",
      item["performance"] == "code" and "parts" not in item and w["starter"] and w["solution"])

# ---- solution, starter, example ----
sol, ns = run(w["solution"])
check("solution passes all 12 hidden tests " + str(failing(sol)), all(sol))
check("solution passes the example (run_tests() == 0)", all(run(w["solution"], "examples")[0]))
st, _ = run(w["starter"])
check("starter fails (tests failing %s)" % failing(st), not all(st))

# each broken version fails at least one of the solution's own tests, and every solution test fails on one
fails_on = {}
for b in ("no_fee", "fee_once", "fee_per_share", "unweighted", "per_fill", "last_fill"):
    seen = ns["_zq_result"](b)[1]
    fails_on[b] = sorted({ns["_zq_fn"](n) for n, o in seen.items() if o == "failed"})
for b, f in fails_on.items():
    print("     %-14s fails %s" % (b, f))
check("every broken version fails a solution test", all(fails_on.values()))

# ---- the stated figures, two routes each ----
def by_formula(fills, fee):
    return (sum(s * p for s, p in fills) + fee * len(fills)) / sum(s for s, p in fills)


def by_fraction(fills, fee):
    paid = sum(Fraction(s) * Fraction(str(p)) for s, p in fills) + Fraction(str(fee)) * len(fills)
    return paid / sum(s for s, p in fills)


two = [(100, 50.00), (300, 52.00)]
check("100 at £50.00 + 300 at £52.00, no fee: 5,000 + 15,600 = 20,600; / 400 = 51.50",
      100 * 50 + 300 * 52 == 20600 and by_fraction(two, 0) == Fraction(5150, 100)
      and math.isclose(by_formula(two, 0), 51.50))
check("with two £6.00 fees: (20,600 + 12) / 400 = 51.53",
      by_fraction(two, 6) == Fraction(5153, 100) and math.isclose(by_formula(two, 6.0), 51.53))
check("one fill of 200 at £12.50, no fee: 12.50", by_fraction([(200, 12.50)], 0) == Fraction(25, 2))
check("the fee moves the cost by 3p", by_fraction(two, 6) - by_fraction(two, 0) == Fraction(3, 100)
      and abs((by_formula(two, 6.0) - by_formula(two, 0.0)) - 0.03) < 1e-9)
check("3p is inside an absolute 5p tolerance, outside the default relative 1e-6",
      abs(51.50 - 51.53) <= 0.05 and abs(51.50 - 51.53) > 1e-6 * 51.53)
ex = item["explain"]["text"]
for phrase in ("£51.50 to £51.53", "That 3p", "absolute tolerance of 5p"):
    check("explain states: " + phrase, phrase in ex)
check("explain code is the solution's tests", w["solution"].split("\n\n\n", 1)[1] in ex)

# ---- plausible wrong test files: each must fail a hidden test ----
HEAD = "import pytest\n\nfrom costs import average_cost\n\n\n"
GOOD1 = "def test_one_fill():\n    assert average_cost([(200, 12.50)], 0.00) == pytest.approx(12.50)\n\n\n"
GOOD2 = "def test_sizes():\n    assert average_cost([(100, 50.00), (300, 52.00)], 0.00) == pytest.approx(51.50)\n\n\n"
GOOD3 = "def test_fees():\n    assert average_cost([(100, 50.00), (300, 52.00)], 6.00) == pytest.approx(51.53)\n"
WRONG = {
    "two tests only": (HEAD + GOOD1 + GOOD3, [1]),
    "functions named check_ (never collected)": (HEAD + (GOOD1 + GOOD2 + GOOD3).replace("def test_", "def check_"), None),
    "a test compares the function with itself": (HEAD + GOOD1 + GOOD3 + "\n\ndef test_same():\n    f = [(100, 50.00), (300, 52.00)]\n"
                                                 "    assert average_cost(f, 6.00) == average_cost(f, 6.00)\n", [12]),
    "fee checked within 5p only (money tolerance too loose)": (
        HEAD + GOOD1 + GOOD2 + "def test_fees():\n    assert average_cost([(100, 50.00), (300, 52.00)], 6.00) == pytest.approx(51.53, abs=0.05)\n", None),
    "exact == on a hand value (18.09)": (
        HEAD + GOOD1 + GOOD2 + "def test_fees():\n    assert average_cost([(100, 12.34), (300, 19.99)], 2.50) == 18.09\n", None),
    "expected value taken from the function at import": (
        HEAD + "F = [(100, 50.00), (300, 52.00)]\nEXPECTED = average_cost(F, 6.00)\n\n\n" + GOOD1 + GOOD2
        + "def test_fees():\n    assert average_cost(F, 6.00) == pytest.approx(EXPECTED)\n", [12]),
    "asserts in a loop over an empty list": (
        HEAD + GOOD1 + GOOD2 + "def test_fees():\n    for fills, want in []:\n        assert average_cost(fills, 6.00) == pytest.approx(want)\n", [12]),
    "return before the assert": (
        HEAD + GOOD1 + GOOD2 + "def test_fees():\n    cost = average_cost([(100, 50.00), (300, 52.00)], 6.00)\n    return\n"
        "    assert cost == pytest.approx(51.53)\n", [12]),
    "only single fills": (
        HEAD + GOOD1 + "def test_fee():\n    assert average_cost([(100, 50.00)], 6.00) == pytest.approx(50.06)\n\n\n"
        "def test_other():\n    assert average_cost([(300, 52.00)], 0.00) == pytest.approx(52.00)\n", None),
    "fills of equal size only": (
        HEAD + GOOD1 + "def test_sizes():\n    assert average_cost([(100, 50.00), (100, 52.00)], 0.00) == pytest.approx(51.00)\n\n\n"
        "def test_fees():\n    assert average_cost([(100, 50.00), (100, 52.00)], 6.00) == pytest.approx(51.06)\n", None),
    "a shared list one test changes": (
        HEAD + "FILLS = [(100, 50.00), (300, 52.00)]\n\n\n" + GOOD1
        + "def test_fees():\n    assert average_cost(FILLS, 6.00) == pytest.approx(51.53)\n\n\n"
        "def test_third_fill():\n    FILLS.append((100, 40.00))\n    assert average_cost(FILLS, 0.00) == pytest.approx(49.20)\n", [5]),
    "hand answer forgets the fee": (HEAD + GOOD1 + GOOD2 + GOOD3.replace("pytest.approx(51.53)", "pytest.approx(51.50)"), None),
}
for name, (src, expect) in WRONG.items():
    res, _ = run(src)
    f = failing(res)
    ok = bool(f) and (expect is None or all(k in f for k in expect))
    check("wrong file caught: %-52s fails %s" % (name, f), ok)

# the reverse-order catch: 49.20 is right for the third fill, so the file passes in file order
check("third-fill answer: (20,600 + 4,000) / 500 = 49.20",
      by_fraction([(100, 50.00), (300, 52.00), (100, 40.00)], 0) == Fraction(4920, 100))
res, _ = run(WRONG["a shared list one test changes"][0])
check("shared-list file passes the correct versions in file order (tests 2 to 4) and fails only in reverse (5)",
      res[1] and res[2] and res[3] and not res[4])
res, _ = run(WRONG["exact == on a hand value (18.09)"][0])
check("exact == fails on a correct version: 18.09 hand value", not all(res[1:4]))
check("18.09 by hand: (1,234 + 5,997 + 5.00) / 400", by_fraction([(100, 12.34), (300, 19.99)], 2.50) == Fraction(1809, 100))

print("\n%d failures" % len(FAIL))
sys.exit(1 if FAIL else 0)
