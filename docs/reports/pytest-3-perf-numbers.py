"""pytest level 3 performance task (homework-3 `h3-fee-test-first`): every number and claim recomputed.

Run with the scratch venv (pytest 8.1.1, as Pyodide 0.27.7 ships):
    <venv>/bin/python docs/reports/pytest-3-perf-numbers.py
It runs the item as js/engine/widgets/code.js does (one load of prelude, learner code and
postlude in a fresh directory, then every hidden case in order), for the solution, the
starter and eleven plausible wrong files (tests and code). Each stated figure is computed twice.
Exits 0 when every check passes.
"""
import contextlib, io, json, math, os, sys, tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app/content/courses/pytest/homework-3.json")
FAIL = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)


doc = json.load(open(HW, encoding="utf-8"))
item = next(i for i in doc["items"] if i["id"] == "h3-fee-test-first")
w = item["widget"]


def run(src, which="tests"):
    """code.js function mode: load once, then each case's setup and call in one namespace."""
    cwd, path0 = os.getcwd(), list(sys.path)
    os.chdir(tempfile.mkdtemp(prefix="zq-"))
    for m in ("test_mine",):
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
                    if c.get("compare") == "raises":
                        try:
                            eval(c["call"], ns)
                            out.append(False)
                        except Exception as e:
                            out.append(c["expect"] in [k.__name__ for k in type(e).__mro__])
                    elif c.get("compare") == "isclose":
                        out.append(math.isclose(float(eval(c["call"], ns)), float(eval(c["expect"], ns)), rel_tol=1e-9, abs_tol=1e-12))
                    else:
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
check("15 hidden tests and 1 example, as `how` says", len(tests) == 15 and len(w["examples"]) == 1
      and "15 hidden tests" in w["how"])
check("tests 1 to 4 call broker_fee (how)", all(t["call"].startswith("broker_fee(") for t in tests[:4])
      and not any(t["call"].startswith("broker_fee(") for t in tests[4:]) and "Tests 1 to 4 call your `broker_fee`" in w["how"])
broken = [t["call"] for t in tests if t["call"].startswith("trial('") and t["expect"] == "'failed'"]
check("six broken versions (how: 'six broken versions')", len(broken) == 6 and "six broken versions" in w["how"])
check("homework keeps 6 to 12 items, one performance item, one difficulty 5",
      6 <= len(doc["items"]) <= 12 and sum(1 for i in doc["items"] if i.get("performance")) == 1
      and any(i["difficulty"] == 5 for i in doc["items"]))
check("performance code item, no parts, starter and solution present",
      item["performance"] == "code" and "parts" not in item and w["starter"] and w["solution"])

# ---- solution, starter, example ----
sol, ns = run(w["solution"])
check("solution passes all 15 hidden tests " + str(failing(sol)), all(sol))
check("solution passes the example (run_tests() == 0)", all(run(w["solution"], "examples")[0]))
st, _ = run(w["starter"])
check("starter fails (tests failing %s)" % failing(st), not all(st))
check("the hidden stub is the starter's function", ns["_ZQ_VERSIONS"]["stub"].strip() in w["starter"])

stub_seen = ns["_zq_result"]("stub")[1]
check("every solution test fails on the empty function (red first) %s" % sorted(set(stub_seen.values())),
      stub_seen and set(stub_seen.values()) == {"failed"})
for b in ("no_min", "no_cap", "rate_1pc", "rounds_down", "zero_allowed", "max_for_cap"):
    f = sorted({ns["_zq_fn"](n) for n, o in ns["_zq_result"](b)[1].items() if o == "failed"})
    print("     %-13s fails %s" % (b, f))
    check("broken version %s fails a solution test" % b, bool(f))

# ---- the fee schedule, two routes: the hidden Decimal reference and the solution's whole pence ----
g = {}
exec(ns["_ZQ_VERSIONS"]["right"], g)
ref = g["broker_fee"]
own = ns["broker_fee"]
from decimal import Decimal, ROUND_HALF_UP


def by_hand(pence):
    """Whole-pence route written out: 0.1% of the notional in pence, half up, then the floor and the cap."""
    fee = Fraction(pence, 1000)
    up = math.floor(fee + Fraction(1, 2))
    return min(max(up, 495), 2500) / 100


agree = all(ref(p / 100) == own(p / 100) == by_hand(p) for p in range(1, 3_000_001, 7))
ties = all(ref(p / 100) == own(p / 100) == by_hand(p) for p in range(500, 10_000_001, 1000))
check("reference, solution and by-hand agree on every 7th penny to £30,000", agree)
check("and on every half-penny tie to £100,000 (half up)", ties)
for notional, fee, label in [(2000.00, 4.95, "£2,000.00 pays the £4.95 minimum"), (12345.67, 12.35, "£12,345.67 pays £12.35"),
                             (80000.00, 25.00, "£80,000.00 pays the £25.00 cap"), (8765.43, 8.77, "£8,765.43 pays £8.77"),
                             (12345.00, 12.35, "£12,345.00 pays £12.35 (half a penny up)"), (4950.00, 4.95, "£4,950 is where the minimum stops binding"),
                             (25000.00, 25.00, "£25,000 is where the cap starts")]:
    check(label, ref(notional) == fee and own(notional) == fee)
check("0.1% of £2,000.00 is £2.00; of £80,000.00 is £80.00; of £12,345.67 is £12.34567; of £8,765.43 is £8.76543",
      Fraction("2000") / 1000 == 2 and Fraction("80000") / 1000 == 80 and Fraction("12345.67") / 1000 == Fraction("12.34567")
      and Fraction("8765.43") / 1000 == Fraction("8.76543"))
check("the minimum binds below £4,950 and the cap above £25,000 (explain)",
      ref(4949.99) == 4.95 and ref(4960.00) == 4.96 and ref(24990.00) == 24.99 and ref(25010.00) == 25.00
      and Fraction("4.95") * 1000 == 4950 and Fraction("25") * 1000 == 25000)
ex = item["explain"]["text"]
for phrase in ("below £4,950", "above £25,000", "£8.76543", "zero itself"):
    check("explain states: " + phrase, phrase in ex)
fb = item["feedback"]["byKey"]
check("feedback figures: £2.00, £12.34567, £80.00", "£2.00" in fb["test-1"] and "£12.34567" in fb["test-2"] and "£80.00" in fb["test-3"])

# ---- plausible wrong files: each must fail a hidden test ----
FN = w["solution"].split("\n\n\ndef test_")[0] + "\n\n\n"
T_MIN = "def test_min():\n    assert broker_fee(2_000.00) == pytest.approx(4.95)\n\n\n"
T_RATE = "def test_rate():\n    assert broker_fee(8_765.43) == pytest.approx(8.77)\n\n\n"
T_CAP = "def test_cap():\n    assert broker_fee(80_000.00) == pytest.approx(25.00)\n\n\n"
T_ZERO = "def test_zero():\n    with pytest.raises(ValueError):\n        broker_fee(0.00)\n\n\n"
GOOD = T_MIN + T_RATE + T_CAP + T_ZERO
WRONG = {
    "good tests, function forgets the cap": (FN.replace("min(max(pence, 495), 2500)", "max(pence, 495)") + GOOD, [3, 6]),
    "round-number tests only": (FN + T_MIN + T_CAP + T_ZERO + "def test_rate():\n    assert broker_fee(10_000.00) == pytest.approx(10.00)\n", [13]),
    "only a negative notional tested": (FN + T_MIN + T_RATE + T_CAP + "def test_neg():\n    with pytest.raises(ValueError):\n        broker_fee(-500.00)\n", [14]),
    "rounding tested within a penny (abs=0.01)": (FN + GOOD.replace("pytest.approx(8.77)", "pytest.approx(8.77, abs=0.01)"), [13]),
    "expected values taken from broker_fee at import": (
        FN + "EXPECTED = {n: broker_fee(n) for n in (2_000.00, 8_765.43, 80_000.00)}\n\n\n"
        "@pytest.mark.parametrize('n', sorted(EXPECTED))\ndef test_fee(n):\n    assert broker_fee(n) == pytest.approx(EXPECTED[n])\n\n\n"
        + T_ZERO + "def test_other():\n    assert broker_fee(1_000.00) == pytest.approx(4.95)\n", [9]),
    "an assert compares broker_fee with itself": (FN + GOOD + "def test_same():\n    assert broker_fee(9_000.00) == broker_fee(9_000.00)\n", [9]),
    "function and tests in pence": (FN.replace("2500) / 100", "2500)") + GOOD.replace("4.95)", "495)").replace("8.77)", "877)").replace("25.00)", "2500)"), [1, 2, 3, 7]),
    "zero accepted, and never tested": (FN.replace("notional <= 0", "notional < 0") + T_MIN + T_RATE + T_CAP
                                        + "def test_neg():\n    with pytest.raises(ValueError):\n        broker_fee(-1.00)\n", [4, 14]),
    "a shared list one test fills": (
        FN + "SEEN = []\n\n\ndef test_three_fees():\n    for n in (2_000.00, 8_765.43, 80_000.00):\n        SEEN.append(broker_fee(n))\n"
        "    assert SEEN == pytest.approx([4.95, 8.77, 25.00])\n\n\n" + T_ZERO
        + "def test_one_more():\n    SEEN.append(broker_fee(12_345.00))\n    assert SEEN[-1] == pytest.approx(12.35)\n", [8]),
    "a test that is green on the empty function": (FN + GOOD + "def test_not_capped():\n    assert broker_fee(2_000.00) != 25.00\n", [9]),
    "tests written, function left empty": (w["starter"] + "\n\n" + GOOD, [1, 2, 3, 4, 6]),
}
for name, (src, expect) in WRONG.items():
    res, _ = run(src)
    f = failing(res)
    ok = bool(f) and all(k in f for k in expect)
    check("wrong file caught: %-48s fails %s" % (name, f), ok)
res, _ = run(WRONG["a shared list one test fills"][0])
check("shared-list file passes in file order (tests 6, 7) and fails only in reverse (8)", res[5] and res[6] and not res[7])
check("8.76 is within abs 0.01 of 8.77, so that tolerance misses rounding down", abs(8.76 - 8.77) <= 0.01 + 1e-12)

print("\n%d failures" % len(FAIL))
sys.exit(1 if FAIL else 0)
