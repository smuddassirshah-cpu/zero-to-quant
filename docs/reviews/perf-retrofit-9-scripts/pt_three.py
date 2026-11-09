"""Reader checks for the three pytest performance tasks (review-perf-retrofit-9): the learner writes tests that run
in real pytest (venv pytest 8.1.1) against correct and broken versions. For each item: the shipped solution, the
starter, a reader test file written independently, and reader-planted weak or gaming test files, each with the hidden
tests it should fail. Run from this folder with the venv Python. Exits 1 if any outcome differs from what is stated."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness9 import item, summary

bad = 0
def expect(widget, src, label, want, which="tests"):
    global bad
    fails, r = summary(widget, src, label, which)
    if want is not None and fails != want:
        bad += 1
        print("     MISMATCH: wanted", want, "got", fails, [x[1] for x in r][:16])
    return fails, r

# ---------------- L1 average_cost ----------------
it = item("pytest", "homework-1.json", "h-average-cost-tests"); w = it["widget"]
print("pytest L1 h-average-cost-tests")
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution, example", [], "examples")
expect(w, w["starter"], "starter", list(range(1, 12)))
expect(w, w["starter"], "starter, example", [1], "examples")
H = "import pytest\nfrom costs import average_cost\n\n"
mine = H + '''
def test_single_fill_with_fee():
    # 50 shares at 20.00 with a 5.00 fee: (1000 + 5) / 50 = 20.10
    assert average_cost([(50, 20.00)], 5.00) == pytest.approx(20.10)

def test_three_fills_weighted_with_fees():
    # 10 @ 4.00, 30 @ 6.00, 60 @ 5.00 with 2.00 each: (40 + 180 + 300 + 6) / 100 = 5.26
    assert average_cost([(10, 4.00), (30, 6.00), (60, 5.00)], 2.00) == pytest.approx(5.26)

def test_two_fills_same_price_fee_spread():
    # 1 @ 10 and 3 @ 10, fee 1: (40 + 2) / 4 = 10.5
    assert average_cost([(1, 10.0), (3, 10.0)], 1.0) == pytest.approx(10.5)
'''
expect(w, mine, "reader tests (independent hand answers)", [])
expect(w, H + "def test_a():\n    assert average_cost([(100, 50.0), (300, 52.0)], 6.0) == pytest.approx(51.53)\n\ndef test_b():\n    assert average_cost([(200, 12.5)], 0.0) == pytest.approx(12.5)\n\ndef test_always_fails():\n    assert False\n",
       "planted: one always-failing test", [2, 3, 4, 5])
expect(w, H + "def test_a():\n    assert average_cost([(100, 50.0), (300, 52.0)], 6.0) == pytest.approx(51.53)\n\ndef test_b():\n    assert average_cost([(200, 12.5)], 0.0) == pytest.approx(12.5)\n\ndef test_c():\n    assert True\n",
       "planted: one always-passing test", [12])
expect(w, H + "".join(f"def test_copy_{k}():\n    assert average_cost([(100, 50.0), (300, 52.0)], 6.0) == pytest.approx(51.53)\n\n" for k in range(3)),
       "planted: one test copied three times", [])
expect(w, H + '''
def ref(f, fee):
    return (sum(s * p for s, p in f) + fee * len(f)) / sum(s for s, p in f)
CASES = [([(100, 50.0), (300, 52.0)], 6.0), ([(7, 3.0)], 1.0), ([(1, 1.0), (2, 2.0), (3, 3.0)], 0.5)]
def test_x():
    for f, fee in CASES: assert average_cost(f, fee) == pytest.approx(ref(f, fee))
def test_y():
    assert average_cost(*CASES[0]) == pytest.approx(ref(*CASES[0]))
def test_z():
    assert average_cost(*CASES[2]) == pytest.approx(ref(*CASES[2]))
''', "planted: oracle (formula copied, no hand answer)", [])
expect(w, H + "def test_a():\n    assert abs(average_cost([(100, 50.0), (300, 52.0)], 6.0) - 51.53) < 0.05\n\ndef test_b():\n    assert abs(average_cost([(100, 50.0), (300, 52.0)], 0.0) - 51.50) < 0.05\n\ndef test_c():\n    assert abs(average_cost([(200, 12.5)], 0.0) - 12.5) < 0.05\n",
       "planted: absolute tolerance 5p", [6, 7])
expect(w, H + "def test_a():\n    assert average_cost([(100, 50.0)], 3.0) == pytest.approx(50.03)\n\ndef test_b():\n    assert average_cost([(10, 50.0)], 3.0) == pytest.approx(50.3)\n\ndef test_c():\n    assert average_cost([(1, 7.0)], 0.0) == pytest.approx(7.0)\n",
       "planted: single fills only", [7, 9, 11, 12])
expect(w, H + "FILLS = [(100, 50.0), (300, 52.0)]\n\ndef test_a():\n    assert average_cost(FILLS, 6.0) == pytest.approx(51.53)\n\ndef test_b():\n    FILLS.append((400, 51.0))\n    assert average_cost(FILLS, 0.0) == pytest.approx(51.25)\n\ndef test_c():\n    assert average_cost([(200, 12.5)], 0.0) == pytest.approx(12.5)\n",
       "planted: shared list changed by a test", [5])
expect(w, H + "def test_a():\n    assert average_cost([(100, 50.0), (300, 52.0)], 6.0) == 51.53\n\ndef test_b():\n    assert average_cost([(3, 0.1), (7, 0.2)], 0.0) == 0.17\n\ndef test_c():\n    assert average_cost([(200, 12.5)], 0.0) == 12.5\n",
       "planted: exact == on floats (passes: same floats here)", [])
expect(w, H + "def test_a():\n    assert average_cost([(100, 50.0), (300, 52.0)], 6.0) == pytest.approx(51.53)\n\ndef test_b():\n    assert average_cost([(200, 12.5)], 0.0) == pytest.approx(12.5)\n\ndef test_empty_raises():\n    with pytest.raises(ZeroDivisionError):\n        average_cost([], 1.0)\n",
       "planted: out-of-spec empty-list test (feedback says rounding)", [3])
expect(w, H + "import inspect, costs\n\ndef test_a():\n    assert 'len(fills)' in inspect.getsource(costs) or 'Fraction' in inspect.getsource(costs) or 'held' in inspect.getsource(costs)\n\ndef test_b():\n    assert 'fee *' in inspect.getsource(costs) or 'fee -' in inspect.getsource(costs) or 'held' in inspect.getsource(costs)\n\ndef test_c():\n    assert '/ shares' in inspect.getsource(costs) or 'Fraction' in inspect.getsource(costs) or 'held' in inspect.getsource(costs)\n",
       "planted: source inspection (needs the hidden versions)", [4])

# ---------------- L2 equity_curve ----------------
it = item("pytest", "homework-2.json", "h2-curve-properties"); w = it["widget"]
print("pytest L2 h2-curve-properties")
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution, example", [], "examples")
expect(w, w["starter"], "starter", list(range(1, 13)))
H = "import math\nimport pytest\nfrom curve import equity_curve\n\n"
mine = H + '''
INPUTS = [(100.0, []), (1.0, [0.5]), (80.0, [0.0, 0.0]), (1000.0, [-0.2, 0.1, 0.03, -0.07]),
          (12.34, [0.001 * k for k in range(-6, 7)]), (5.0, [0.07, -0.99, 3.0])]

@pytest.mark.parametrize("start, rs", INPUTS)
def test_length_and_first(start, rs):
    c = equity_curve(start, rs)
    assert len(c) == len(rs) + 1 and c[0] == start

@pytest.mark.parametrize("start, rs", INPUTS)
def test_ratio_of_neighbours(start, rs):
    c = equity_curve(start, list(rs))
    assert all(c[i + 1] == pytest.approx(c[i] * (1 + r)) for i, r in enumerate(rs))

@pytest.mark.parametrize("start, rs", INPUTS)
def test_input_untouched(start, rs):
    copy = list(rs)
    equity_curve(start, copy)
    assert copy == rs
'''
expect(w, mine, "reader property tests", [])
expect(w, H + '''
def test_a():
    assert equity_curve(100.0, [0.1, -0.1]) == pytest.approx([100.0, 110.0, 99.0])
def test_b():
    r = [0.1]; equity_curve(100.0, r); assert r == [0.1]
def test_c():
    assert equity_curve(100.0, []) == [100.0]
''', "planted: hand answers, one call each", [9, 10, 14])
expect(w, H + '''
P = [[], [0.0], [0.01, 0.02], [0.03, -0.04, 0.05], [0.2] * 6]
@pytest.mark.parametrize("rs", P)
def test_end(rs):
    assert equity_curve(10.0, rs)[-1] == pytest.approx(10.0 * math.prod(1 + r for r in rs))
@pytest.mark.parametrize("rs", P)
def test_len(rs):
    assert len(equity_curve(10.0, rs)) == len(rs) + 1
@pytest.mark.parametrize("rs", P)
def test_same(rs):
    b = list(rs); equity_curve(10.0, rs); assert rs == b
''', "planted: only the end value is checked", [12])
expect(w, H + '''
P = [[], [0.1], [0.01, 0.02], [0.03, -0.04, 0.05], [0.2] * 6]
@pytest.mark.parametrize("rs", P)
def test_len(rs):
    c = equity_curve(10.0, rs); assert len(c) == len(rs) + 1 and c[0] == 10.0
@pytest.mark.parametrize("rs", P)
def test_step(rs):
    c = equity_curve(10.0, list(rs))
    for t, r in enumerate(rs): assert c[t + 1] == pytest.approx(c[t] * (1 + r))
@pytest.mark.parametrize("rs", P)
def test_same(rs):
    b = list(rs); equity_curve(10.0, rs); assert rs == b
''', "planted: no flat day", [10])
expect(w, H + '''
P = [[], [0.0], [0.012, -0.034], [0.03, -0.04, 0.05], [0.2] * 6]
@pytest.mark.parametrize("rs", P)
def test_len(rs):
    c = equity_curve(250.0, rs); assert len(c) == len(rs) + 1 and c[0] == 250.0
@pytest.mark.parametrize("rs", P)
def test_step_exact(rs):
    c = equity_curve(250.0, list(rs))
    for t, r in enumerate(rs): assert c[t + 1] == c[t] * (1 + r)
@pytest.mark.parametrize("rs", P)
def test_same(rs):
    b = list(rs); equity_curve(250.0, rs); assert rs == b
''', "planted: step rule with exact ==", [4])
expect(w, H + '''
P = [[], [0.0], [0.012, -0.034], [0.03, -0.04, 0.05], [0.2] * 6]
@pytest.mark.parametrize("rs", P)
def test_len(rs):
    c = equity_curve(250.0, rs); assert len(c) == len(rs) + 1 and c[0] == 250.0
@pytest.mark.parametrize("rs", P)
def test_step(rs):
    rs.append(0.0)
    c = equity_curve(250.0, list(rs))
    for t, r in enumerate(rs): assert c[t + 1] == pytest.approx(c[t] * (1 + r))
@pytest.mark.parametrize("rs", P)
def test_same(rs):
    b = list(rs); equity_curve(250.0, rs); assert rs == b
''', "planted: a test appends to the shared inputs (rules still hold)", [])

expect(w, H + '''
TABLE = [
    (100.0, [], [100.0]),
    (100.0, [0.0], [100.0, 100.0]),
    (100.0, [0.1, -0.1], [100.0, 110.0, 99.0]),
    (200.0, [0.05, 0.05, -0.5], [200.0, 210.0, 220.5, 110.25]),
    (80.0, [0.013, -0.02], [80.0, 81.04, 79.4192]),
]

@pytest.mark.parametrize("start, rs, want", TABLE)
def test_whole_curve(start, rs, want):
    assert equity_curve(start, rs) == pytest.approx(want)

@pytest.mark.parametrize("start, rs, want", TABLE)
def test_curve_again(start, rs, want):
    assert equity_curve(start, list(rs)) == pytest.approx(want)

@pytest.mark.parametrize("start, rs, want", TABLE)
def test_input_kept(start, rs, want):
    copy = list(rs)
    equity_curve(start, copy)
    assert copy == rs
''', "planted: three tables of hand answers, no rule", [])
# ---------------- L3 broker_fee ----------------
it = item("pytest", "homework-3.json", "h3-fee-test-first"); w = it["widget"]
print("pytest L3 h3-fee-test-first")
expect(w, w["solution"], "shipped solution", [])
expect(w, w["solution"], "shipped solution, example", [], "examples")
expect(w, w["starter"], "starter", [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15])
TESTS = '''

def test_minimum():
    assert broker_fee(3_000.00) == pytest.approx(4.95)

def test_middle():
    assert broker_fee(15_432.10) == pytest.approx(15.43)  # 15.43210

def test_rounds_up_at_half():
    assert broker_fee(5_005.00) == pytest.approx(5.01)  # 5.005

def test_cap():
    assert broker_fee(30_000.00) == pytest.approx(25.00)

@pytest.mark.parametrize("n", [0, -1.0])
def test_bad(n):
    with pytest.raises(ValueError):
        broker_fee(n)
'''
MINE = '''import pytest
from decimal import Decimal, ROUND_HALF_UP

def broker_fee(notional):
    if notional <= 0:
        raise ValueError("not positive")
    fee = (Decimal(str(notional)) * Decimal("0.001")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(min(Decimal("25.00"), max(Decimal("4.95"), fee)))
''' + TESTS
expect(w, MINE, "reader code and tests", [])
FLOAT = '''import pytest

def broker_fee(notional):
    if notional <= 0:
        raise ValueError("not positive")
    return min(max(round(notional * 0.001, 2), 4.95), 25.00)
'''
expect(w, FLOAT + "\n\ndef test_small" + w["solution"].split("\n\n\ndef test_small", 1)[1],
       "planted: float round(), the shipped tests", [2])
expect(w, FLOAT + TESTS, "planted: float round(), own half-penny test at 5,005", [2, 6, 8])
print("     float round() on half-penny notionals:", [(n, round(n * 0.001, 2)) for n in (5005.0, 10005.0, 12345.0)])
expect(w, FLOAT + '''
def test_a():
    assert broker_fee(2_000.00) == broker_fee(2_000.00)
def test_b():
    assert broker_fee(8_765.43) == pytest.approx(8.77)
def test_c():
    assert broker_fee(80_000.00) == pytest.approx(25.00)
@pytest.mark.parametrize("n", [0.0, -5.0])
def test_d(n):
    with pytest.raises(ValueError):
        broker_fee(n)
''', "planted: a test that compares broker_fee with itself", [2, 9, 10])
expect(w, MINE.replace("def test_minimum():\n    assert broker_fee(3_000.00) == pytest.approx(4.95)", "def test_minimum():\n    assert broker_fee(3_000.00) == pytest.approx(4.95)\n\ndef test_always_red():\n    assert broker_fee(1.0) == 99"),
       "planted: one always-failing test", [6, 7, 8])
expect(w, MINE.replace("@pytest.mark.parametrize(\"n\", [0, -1.0])", "@pytest.mark.parametrize(\"n\", [-1.0])").replace("def test_rounds_up_at_half():\n    assert broker_fee(5_005.00) == pytest.approx(5.01)  # 5.005\n", ""),
       "planted: negative notional only, no round-up case", [13, 14])

expect(w, MINE.split("\n\ndef test_minimum")[0] + '''

def test_everything():
    assert broker_fee(2_000.00) == pytest.approx(4.95)
    assert broker_fee(8_765.43) == pytest.approx(8.77)
    assert broker_fee(80_000.00) == pytest.approx(25.00)
    with pytest.raises(ValueError):
        broker_fee(0.0)

def test_gives_a_value():
    assert broker_fee(1_000.00) is not None

def test_gives_another_value():
    assert broker_fee(9_000.00) is not None
''', "planted: one real test and two `is not None` tests", [])
# the shipped solution against a sub-penny notional (the prose does not say notionals are whole pence)
ns = {}
exec(w["solution"].split("\n\n\ndef test_small", 1)[0], ns)
from decimal import Decimal, ROUND_HALF_UP
def half_up(n):
    f = (Decimal(repr(n)) / 1000).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return float(min(max(f, Decimal("4.95")), Decimal("25.00")))
sub = [(x, ns["broker_fee"](x), half_up(x)) for x in (12344.996, 9994.996, 5004.9951)]
print("     shipped solution at sub-penny notionals (got, half up of 0.1%):", sub)
whole = all(ns["broker_fee"](k / 100) == half_up(k / 100) for k in range(1, 3_000_001, 7))
print("     shipped solution equals half-up on every 7th whole-penny notional to 30,000:", whole)
if not whole:
    bad += 1
print("mismatches:", bad)
sys.exit(1 if bad else 0)
