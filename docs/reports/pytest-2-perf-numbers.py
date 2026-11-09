"""pytest level 2 performance task (homework-2 `h2-curve-properties`): every number and claim recomputed.

Run with the scratch venv (pytest 8.1.1, as Pyodide 0.27.7 ships):
    <venv>/bin/python docs/reports/pytest-2-perf-numbers.py
It runs the item as js/engine/widgets/code.js does (one load of prelude, learner code and
postlude in a fresh directory, then every hidden case in order), for the solution, the
starter and eleven plausible wrong test files. Each stated figure is computed twice.
Exits 0 when every check passes.
"""
import contextlib, io, json, math, os, sys, tempfile
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app/content/courses/pytest/homework-2.json")
FAIL = []


def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)


doc = json.load(open(HW, encoding="utf-8"))
item = next(i for i in doc["items"] if i["id"] == "h2-curve-properties")
w = item["widget"]


def run(src, which="tests"):
    """code.js function mode: load once, then each case's setup and call in one namespace."""
    cwd, path0 = os.getcwd(), list(sys.path)
    os.chdir(tempfile.mkdtemp(prefix="zq-"))
    for m in ("curve", "test_mine"):
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
check("14 hidden tests and 1 example, as `how` says", len(tests) == 14 and len(w["examples"]) == 1
      and "14 hidden tests" in w["how"])
calls = [t["call"] for t in tests]
right = [c for c in calls if c.startswith("trial('right") and "reverse" not in c]
broken = [c for c in calls if c.startswith("trial(") and "right" not in c]
check("three correct versions, seven broken (how: 'three correct', 'seven broken')",
      len(right) == 3 and len(broken) == 7 and "three correct versions" in w["how"] and "seven broken versions" in w["how"])
check("`few()` needs at least five calls, as `how` and the question say",
      "few()" in calls and "at least five times" in w["how"] and "at least five inputs" in item["question"])
check("homework keeps 6 to 12 items, one performance item, one difficulty 5",
      6 <= len(doc["items"]) <= 12 and sum(1 for i in doc["items"] if i.get("performance")) == 1
      and any(i["difficulty"] == 5 for i in doc["items"]))
check("performance code item, no parts, starter and solution present",
      item["performance"] == "code" and "parts" not in item and w["starter"] and w["solution"])

# ---- solution, starter, example ----
sol, ns = run(w["solution"])
check("solution passes all 14 hidden tests " + str(failing(sol)), all(sol))
check("solution passes the example (run_tests() == 0)", all(run(w["solution"], "examples")[0]))
st, _ = run(w["starter"])
check("starter fails (tests failing %s)" % failing(st), not all(st))

fails_on = {}
for b in ("adds", "no_start", "mutates", "pennies", "skips_zero", "percent", "reversed"):
    seen = ns["_zq_result"](b)[1]
    fails_on[b] = sorted({ns["_zq_fn"](n) for n, o in seen.items() if o == "failed"})
    print("     %-11s fails %s" % (b, fails_on[b]))
check("every broken version fails a solution test (explain: 'they catch every broken version')", all(fails_on.values()))
check("only the step rule sees the reversed version (explain)",
      fails_on["reversed"] == ["test_each_day_grows_by_one_plus_its_return"])
calls_per = {}
for n, k in ns["_zq_result"]("right")[2].items():
    calls_per[ns["_zq_fn"](n)] = calls_per.get(ns["_zq_fn"](n), 0) + k
check("each solution test calls equity_curve 5 times (one per path) %s" % calls_per, set(calls_per.values()) == {5})

# ---- the inputs and the claims in feedback, two routes each ----
sol_ns = {}
exec(w["solution"].replace("from curve import equity_curve\n", ""), sol_ns)
paths = sol_ns["PATHS"]
long_path = paths[4]
check("the 40-day path: 40 returns between -0.05 and 0.05 with zeros among them",
      len(long_path) == 40 and min(long_path) == -0.05 and max(long_path) == 0.05 and long_path.count(0.0) >= 3
      and [round(0.01 * (((7 * k) % 11) - 5), 2) for k in range(40)] == [round(x, 2) for x in long_path])
check("PATHS hold an empty list, a flat day and a large loss (explain)", [] in paths and [0.0] in paths and min(map(min, filter(None, paths))) == -0.5)


def curve(fn_name, start, returns):
    g = {}
    exec(sol_ns_versions[fn_name], g)
    return g["equity_curve"](start, list(returns))


sol_ns_versions = dict(ns["_ZQ_VERSIONS"])
for p in paths:
    a = curve("right", 250.0, p)
    b = curve("reversed", 250.0, p)
    if p:
        check("reversed version: same last value on %d-day path (test-12), by loop and by product" % len(p),
              math.isclose(a[-1], b[-1], rel_tol=1e-12) and math.isclose(a[-1], 250.0 * math.prod(1 + r for r in p), rel_tol=1e-12))
check("reversed version differs on a day of the 4-day path", curve("reversed", 250.0, paths[2])[1] != curve("right", 250.0, paths[2])[1])
check("percent reads 0.01 as 0.01%: growth 1.0001, not 1.01 (test-11)",
      math.isclose(curve("percent", 100.0, [0.01])[1], 100.01) and math.isclose(curve("right", 100.0, [0.01])[1], 101.0))
pen = curve("pennies", 250.0, paths[2])
check("pennies: 250 x 1.012 x 0.966 = 244.398 rounds to 244.40, off by more than approx's 1e-6",
      math.isclose(250 * 1.012 * 0.966, 244.398) and pen[2] == 244.40 and abs(pen[2] - 244.398) / 244.398 > 1e-6)
check("skips_zero gives a curve one short for each 0.0 (test-10)", len(curve("skips_zero", 250.0, paths[2])) == 4)
check("adds: 250 x (1 + 0.012 - 0.034) = 244.5 against 244.398 compounded",
      math.isclose(curve("adds", 250.0, paths[2])[2], 250 * (1 + 0.012 - 0.034)) and math.isclose(250 * 0.978, 244.5))

# ---- plausible wrong test files: each must fail a hidden test ----
HEAD = "import pytest\n\nfrom curve import equity_curve\n\n"
TABLE = ("PATHS = [[], [0.0], [0.012, -0.034, 0.0, 0.021], [-0.5, 0.25, 0.1],\n"
         "         [0.01 * ((7 * k) % 11 - 5) for k in range(40)]]\n\n\n")
LEN = ('@pytest.mark.parametrize("returns", PATHS)\ndef test_length(returns):\n'
       "    c = equity_curve(250.00, returns)\n    assert len(c) == len(returns) + 1 and c[0] == 250.00\n\n\n")
STEP = ('@pytest.mark.parametrize("returns", PATHS)\ndef test_step(returns):\n'
        "    c = equity_curve(250.00, list(returns))\n    for t, r in enumerate(returns):\n"
        "        assert c[t + 1] == pytest.approx(c[t] * (1 + r))\n\n\n")
SAME = ('@pytest.mark.parametrize("returns", PATHS)\ndef test_unchanged(returns):\n'
        "    before = list(returns)\n    equity_curve(250.00, returns)\n    assert returns == before\n")
WRONG = {
    "hand answers only, one input each": (
        HEAD + "def test_two_days():\n    assert equity_curve(100.00, [0.1, -0.1]) == pytest.approx([100.00, 110.00, 99.00])\n\n\n"
        "def test_no_days():\n    assert equity_curve(100.00, []) == [100.00]\n\n\n"
        "def test_flat():\n    assert equity_curve(100.00, [0.0]) == pytest.approx([100.00, 100.00])\n", [14]),
    "no flat day among the inputs": (
        HEAD + "PATHS = [[0.012, -0.034, 0.021], [-0.5, 0.25, 0.1], [0.013] * 9, [0.02, -0.01], [0.031, -0.027, 0.004]]\n\n\n"
        + LEN.replace("PATHS", "PATHS") + STEP + SAME, [10]),
    "only the last value checked": (
        HEAD + "import math\n\n" + TABLE + LEN + '@pytest.mark.parametrize("returns", PATHS)\ndef test_end(returns):\n'
        "    c = equity_curve(250.00, list(returns))\n    assert c[-1] == pytest.approx(250.00 * math.prod(1 + r for r in returns))\n\n\n" + SAME, [12]),
    "a rule compared with itself": (
        HEAD + TABLE + LEN + SAME + '\n\n@pytest.mark.parametrize("returns", PATHS)\ndef test_repeatable(returns):\n'
        "    assert equity_curve(250.00, list(returns)) == equity_curve(250.00, list(returns))\n", [13]),
    "a module-scoped fixture one test extends": (
        HEAD + "import math\n\n\n@pytest.fixture(scope='module')\ndef paths():\n"
        "    return [[0.012, -0.034, 0.0, 0.021], [-0.5, 0.25, 0.1], [0.0], [0.02] * 6, [0.031, -0.027]]\n\n\n"
        "def test_end_values(paths):\n    want = [249.5304, 171.875, 250.00, 281.5406, 250.7907]\n"
        "    for r, end in zip(paths, want):\n        assert equity_curve(250.00, list(r))[-1] == pytest.approx(end, abs=0.0001)\n\n\n"
        "def test_step(paths):\n    for r in paths:\n        c = equity_curve(250.00, list(r))\n"
        "        assert all(c[t + 1] == pytest.approx(c[t] * (1 + x)) for t, x in enumerate(r))\n\n\n"
        "def test_one_more_day(paths):\n    for r in paths:\n        r.append(0.01)\n        c = equity_curve(250.00, list(r))\n"
        "        assert len(c) == len(r) + 1 and c[-1] == pytest.approx(c[-2] * 1.01)\n\n\n"
        "def test_unchanged(paths):\n    for r in paths:\n        before = list(r)\n        equity_curve(250.00, r)\n        assert r == before\n", [5]),
    "step rule with == instead of approx": (HEAD + TABLE + LEN + STEP.replace("pytest.approx(c[t] * (1 + r))", "c[t] * (1 + r)") + SAME, [4]),
    "no check that returns are left alone": (HEAD + TABLE + LEN + STEP, [8]),
    "a rule over an empty table (never runs)": (
        HEAD + TABLE + LEN + STEP + SAME + '\n\n@pytest.mark.parametrize("returns", [])\ndef test_scale(returns):\n'
        "    assert equity_curve(500.00, returns) == pytest.approx([2 * v for v in equity_curve(250.00, returns)])\n", [13]),
    "tolerance too loose (rel=1e-3)": (HEAD + TABLE + LEN + STEP.replace("pytest.approx(c[t] * (1 + r))", "pytest.approx(c[t] * (1 + r), rel=1e-3)") + SAME, [9]),
    "round numbers only": (
        HEAD + "PATHS = [[], [0.0], [0.01, 0.02], [0.1, -0.1, 0.0], [0.2, 0.2, 0.2], [0.5, -0.2]]\n\n\n" + LEN + STEP.replace("250.00", "100.00") + SAME, [9]),
    "length and input only, no value rule": (HEAD + TABLE + LEN + SAME + "\n\n" + LEN.replace("test_length", "test_length_again"), [6, 11, 12]),
}
for name, (src, expect) in WRONG.items():
    res, _ = run(src)
    f = failing(res)
    ok = bool(f) and (expect is None or all(k in f for k in expect))
    check("wrong file caught: %-44s fails %s" % (name, f), ok)

# the fixture plant, checked against real pytest: hand ends, the order effect, and fixture builds
check("plant's hand end values, two routes: 249.5304, 171.875, 250.00, 281.5406, 250.7907",
      all(math.isclose(round(250 * math.prod(1 + r for r in p), 4), e) and math.isclose(curve("right", 250.0, p)[-1], e, abs_tol=1e-4)
          for p, e in zip([[0.012, -0.034, 0.0, 0.021], [-0.5, 0.25, 0.1], [0.0], [0.02] * 6, [0.031, -0.027]],
                          [249.5304, 171.875, 250.00, 281.5406, 250.7907])))
res, _ = run(WRONG["a module-scoped fixture one test extends"][0])
check("module-scoped plant: passes the correct versions in file order, fails only in reverse",
      res[1] and res[2] and res[3] and not res[4])
fn_scope = WRONG["a module-scoped fixture one test extends"][0].replace("@pytest.fixture(scope='module')", "@pytest.fixture")
res, _ = run(fn_scope)
check("same file with a default-scope fixture: passes in reverse order too", res[1] and res[4])


def fixture_builds(src):
    """Run real pytest on src with a counter in the fixture; returns how many times it was built."""
    import pytest
    d = tempfile.mkdtemp(prefix="zq-fx-")
    cwd = os.getcwd()
    os.chdir(d)
    try:
        open("curve.py", "w").write(ns["_ZQ_VERSIONS"]["right"])
        open("test_fx.py", "w").write(src.replace("def paths():\n", "def paths():\n    BUILT.append(1)\n").replace("import math\n", "import math\nBUILT = []\n"))
        for m in ("curve", "test_fx"):
            sys.modules.pop(m, None)
        with contextlib.redirect_stdout(io.StringIO()):
            pytest.main(["-q", "-p", "no:cacheprovider", "test_fx.py"])
        return len(sys.modules["test_fx"].BUILT)
    finally:
        os.chdir(cwd)


check("real pytest 8.1.1: a module-scoped fixture is built once for the file's four tests",
      fixture_builds(WRONG["a module-scoped fixture one test extends"][0]) == 1)
check("real pytest 8.1.1: a default-scope fixture is built once per test that asks (4)", fixture_builds(fn_scope) == 4)

print("\n%d failures" % len(FAIL))
sys.exit(1 if FAIL else 0)
