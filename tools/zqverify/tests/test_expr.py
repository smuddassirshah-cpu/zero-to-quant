"""The expression twin against the spec's examples, refusals, NaN rules, limits and budget, its rounding against
CPython, Fraction and 100 digits, and fresh goldens. Each table quotes the spec (docs/ARCHITECTURE.md 5.15)."""

from __future__ import annotations

import ast
import json
import math
from fractions import Fraction
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from zqverify import expr as X

INF, NAN = math.inf, math.nan
BIG, NEG_BIG, NOT_A_NUMBER = X.BIG, X.NEG_BIG, X.NOT_A_NUMBER
FINITE = st.floats(allow_nan=False, allow_infinity=False)
NAMES = st.sampled_from(("x", "y", "z", "t", "k", "W_t", "x_1", "lambda", "E", "pi2"))


def same(a: float, b: float) -> bool:
    """Bit-equal for doubles, with every NaN equal to every NaN."""
    return (a != a and b != b) or (a == b and math.copysign(1.0, a) == math.copysign(1.0, b))


def refused(src: str) -> bool:
    try:
        X.parse(src)
    except X.ParseError:
        return True
    return False


def term(nodes: int) -> str:
    """The spec's budget term: an `if` of exactly `nodes` nodes whose value is 1 for every k >= 0."""
    return "if(k<0," + "-" * (nodes - 5) + "k,1)"


# Goldens.


def test_the_committed_goldens_are_fresh() -> None:
    assert X.GOLDEN.read_text(encoding="utf-8") == X.render()


def test_the_goldens_have_the_spec_shape_and_the_parity_tests_counts() -> None:
    lines = [json.loads(line) for line in X.GOLDEN.read_text(encoding="utf-8").splitlines()]
    for line in lines:
        keys = list(line)
        assert keys[:2] == ["src", "scope"]
        assert keys[2:] in (["error"], ["free", "value", "exact"])
        if "error" in line:
            assert line["error"] in ("parse", "scope")
        else:
            assert isinstance(line["value"], float) or line["value"] in ("nan", "inf", "-inf")
    exact = sum(1 for line in lines if line.get("exact") is True)
    inexact = sum(1 for line in lines if line.get("exact") is False)
    assert len(lines) >= 1800 and exact > 350 and inexact > 400
    assert sum(1 for line in lines if line.get("error") == "parse") > 300
    assert sum(1 for line in lines if line.get("error") == "scope") > 30


def test_every_inexact_golden_rounds_the_same_at_100_digits() -> None:
    for line in X.goldens():
        if line.get("exact") is False:
            scope = line["scope"]
            assert isinstance(scope, dict)
            with X.MP.workdps(100):
                v = X.value(str(line["src"]), scope)
            assert json.dumps(X.encode(v)) == json.dumps(line["value"]), line["src"]


def test_every_golden_calls_erf_and_phi_inside_the_parity_tables_range() -> None:
    for line in X.goldens():
        scope = line["scope"]
        assert isinstance(scope, dict)
        assert X.within_table(str(line["src"]), scope), line["src"]


@pytest.mark.parametrize(
    ("src", "inside"),
    [("erf(2)", True), ("erf(-2.0000000000000004)", False), ("Phi(2.8)", True), ("Phi(-2.8000000000000003)", False),
     (f"erf({BIG})", True), (f"Phi({NEG_BIG})", True), ("erf(-0)", True), ("Phi(0/0)", True), ("erf(0/0)", True),
     ("phi(30)", True),
     ("if(1 < 2, 1, erf(3))", True), ("if(1 > 2, 1, erf(3))", False), ("sum(k, 1, 3, Phi(k))", False),
     ("sum(k, 1, 2, Phi(k))", True), ("erf(x)", True), ("sin(", True)],
)
def test_within_table_judges_the_argument_each_call_receives(src: str, inside: bool) -> None:
    assert X.within_table(src, {}) is inside


def test_the_exact_flag_is_syntactic() -> None:
    assert X.parse("sqrt(2) + abs(-1) + floor(x) + min(1, 2) + pi + e + sum(k, 1, 2, k) + if(1 < 2, 3, 4)").exact
    for src in ("2^1", "sin(0)", "erf(0) * 0", "if(1 < 2, 1, x^2)", "atan2(1, 1)", "Phi(0)", "phi(0)", "cbrt(1)"):
        assert not X.parse(src).exact, src
    assert X.parse("PHI + Sin + Exp").exact  # not functions, so ordinary variables


# Section 1: text.

ACCEPTED = {
    "2": 2.0, "007": 7.0, "0.5": 0.5, ".5": 0.5, "1.5e-3": 0.0015, "2E+3": 2000.0, "0e5": 0.0, "00.000": 0.0,
    "100000000000000000000000000": 1e26, "0.00012345678901234567890e3": 0.1234567890123456789,
    "12345678901234567890": 12345678901234567890.0, "1.0000000000000000001": 1.0, "9007199254740993": 2.0**53,
    "9007199254740995": 2.0**53 + 4, "1.7976931348623158e308": 1.7976931348623157e308, "2e-324": 0.0,
    "3e-324": 5e-324, "2.4703282292062327e-324": 0.0, "2.4703282292062328e-324": 5e-324, "1e-99999999999999999999": 0.0,
    "0e99999999999999999999": 0.0, "1e0000000000000000000000000000000300": 1e300, " 1 ": 1.0, "\t1\n": 1.0,
    "1\r\n+\r\n2": 3.0,
}

REFUSED_TEXT = [
    "1.", "1.e5", "123456789012345678901", "12345678901234567890.1", "1.00000000000000000001", "1e999", "1e309",
    "1.7976931348623159e308", "100000000000000000000e289", "1e99999999999999999999", "_x", "__proto__", "\u03c0",
    "x\u00b2", "x\u0661", "\u0661", "x\uff11", "\uff58", "2**3", "x = 1", "x != 1", "[1]", ".", "1 . 2", "1\f", "1\v",
    "1\u00a0", "1\u3000", "\U0001d465", "\ud800", "", " \t\r\n", "1e5.5", "0x10", "1_000",
]


@pytest.mark.parametrize(("src", "expected"), ACCEPTED.items())
def test_numbers_and_white_space_the_spec_accepts(src: str, expected: float) -> None:
    assert same(X.value(src), expected)


@pytest.mark.parametrize("src", REFUSED_TEXT)
def test_text_the_spec_refuses(src: str) -> None:
    assert refused(src)


def test_names() -> None:
    for name in ("x", "x_1", "W_t", "lambda", "E", "pi2", "e5", "constructor", "prototype", "toString", "Infinity"):
        assert X.parse(name).free == [name]
        assert X.value(name, {name: 2.5}) == 2.5
    assert X.value("e") == 2.718281828459045 and X.value("pi") == 3.141592653589793


def test_significant_digits_run_from_the_first_non_zero_digit_to_the_last() -> None:
    assert not refused("1" + "0" * 50) and not refused("0." + "0" * 50 + "1")
    assert not refused("1" + "0" * 18 + "1") and refused("1" + "0" * 19 + "1")  # 20 and 21
    assert not refused("00" + "9" * 20 + "00") and refused("9" * 21)
    assert not refused("1234567890.123456789000000e-5")


@given(st.floats(min_value=0, allow_nan=False, allow_infinity=False))
def test_a_doubles_shortest_spelling_reads_back(x: float) -> None:
    assert same(X.literal(repr(x)), x)


@given(st.text("0123456789", max_size=12), st.text("0123456789", max_size=12), st.integers(-400, 400))
def test_literals_round_as_cpythons_float_does(whole: str, fraction: str, exponent: int) -> None:
    text = (whole or "0") + (f".{fraction}" if fraction else "") + f"e{exponent}"
    if len((whole + fraction).strip("0")) > X.MAX_DIGITS:
        assert refused(text)
    elif float(text) == INF:
        assert refused(text)
    else:
        assert same(X.literal(text), float(text))


@given(st.integers(0, 2**300), st.integers(1, 2**300), st.integers(-1300, 1100), st.booleans())
def test_round_ratio_is_fractions_correctly_rounded_float(num: int, den: int, exp2: int, negative: bool) -> None:
    q = Fraction(num, den) * Fraction(2) ** exp2
    try:
        expected = float(q)
    except OverflowError:
        expected = INF
    assert same(X.round_ratio(negative, num, den, exp2), -expected if negative else expected)


def test_length_limit() -> None:
    assert X.value("1" + " " * 999) == 1 and refused(" " * 1000 + "1")
    assert X.value("1" + "+1" * 499 + " ") == 500 and refused("1" + "+1" * 500)


# Section 2: grammar.

GRAMMAR_VALUES = [
    ("-x^2", {"x": 3}, -9.0), ("2^-1", {}, 0.5), ("2^3^2", {}, 512.0), ("-2^-2^-1", {}, -0.7071067811865476),
    ("1 - 2 - 3", {}, -4.0), ("8/4*2", {}, 4.0), ("--1", {}, 1.0), ("1--1", {}, 2.0), ("2*-3", {}, -6.0),
    ("2^--2", {}, 4.0), ("-2^2", {}, -4.0), ("(-2)^2", {}, 4.0), ("2^-2^2", {}, 0.0625), ("1/2/4", {}, 0.125),
    ("2^2*3", {}, 12.0), ("2*3^2", {}, 18.0), ("sin (0)", {}, 0.0), ("sin\n(0)", {}, 0.0),
    ("if((x) < 0, 1, 2)", {"x": -1}, 1.0), ("min(3, 1, 2)", {}, 1.0), ("max(1, 2, 3, 4, 5)", {}, 5.0),
    ("constructor + prototype + toString", {"constructor": 1, "prototype": 2, "toString": 3}, 6.0),
    ("if(1 <= 1, 1, 2)", {}, 1.0), ("if(1 == 1, 1, 2)", {}, 1.0), ("if(1 >= 2, 1, 2)", {}, 2.0),
    ("if(2 > 1, 1, 2)", {}, 1.0), ("if(1 < 1, 1, 2)", {}, 2.0), ("if(-0 == 0, 1, 2)", {}, 1.0),
]

REFUSED_GRAMMAR = [
    "2x", "x y", "+1", "1 + +1", "sin()", "sin(1, 2)", "min(1)", "sin(1,)", "(sin)(1)", "sin(1)(2)",
    "if((1 < 2), 1, 2)", "if(1 < 2 < 3, 1, 2)", "x < 1", "(1 < 2) + 1", "if(x, 1, 2)", "sum((k), 1, 2, k)",
    "sum(pi, 1, 2, 1)", "sum(e, 1, 2, 1)", "sum(sin, 1, 2, 1)", "sum(if, 1, 2, 1)", "sum(k + 1, 1, 2, k)", "sin",
    "sum + 1", "if", "x(1)", "pi(1)", "e(1)", "foo(1)", "constructor(1)", "atan2(1)", "atan2(1, 2, 3)", "max()",
    "if(1 < 2, 3)", "if(1 < 2, 3, 4, 5)", "sum(k, 1, 2)", "sum(k, 1, 2, k, 1)", "if(1 = 1, 1, 2)", "if(1 < = 2, 1, 2)",
    "()", "(1", "1)", "1 *", "1^^2", "2 3", "pi e",
]


@pytest.mark.parametrize(("src", "scope", "expected"), GRAMMAR_VALUES)
def test_precedence_associativity_and_calls(src: str, scope: dict[str, float], expected: float) -> None:
    assert same(X.value(src, scope), expected)


@pytest.mark.parametrize("src", REFUSED_GRAMMAR)
def test_grammar_the_spec_refuses(src: str) -> None:
    assert refused(src)


def test_nesting_limits() -> None:
    assert X.value("(" * 32 + "1" + ")" * 32) == 1 and refused("(" * 33 + "1" + ")" * 33)
    assert X.value("abs(" * 32 + "-1" + ")" * 32) == 1 and refused("abs(" * 33 + "1" + ")" * 33)
    assert X.value("(abs(" * 16 + "1" + "))" * 16) == 1 and refused("(abs(" * 16 + "(1)" + "))" * 16)
    assert X.value("-" * 999 + "1") == -1 and X.value("-" * 998 + "1") == 1
    assert X.value("2^" + "-" * 997 + "1") == 0.5 and X.value("2" + "^1" * 499) == 2


@settings(deadline=None)
@given(st.text(alphabet="()+-*/^,.<=> \t0123456789eExyk_sinumafPhi\u03c0!", max_size=60))
def test_the_parser_refuses_with_parse_error_only(src: str) -> None:
    try:
        expr = X.parse(src)
    except X.ParseError:
        return
    expr.evaluate(dict.fromkeys(expr.free, 1.5))


def _tree(depth: int) -> st.SearchStrategy[tuple[str, int, float]]:
    """(source printed with the fewest brackets precedence allows, precedence level, value from Python floats)."""
    leaf = st.floats(min_value=0, max_value=1e6, allow_nan=False).map(lambda v: (repr(v), 3, v))
    if depth == 0:
        return leaf

    def binary(parts: tuple[tuple[str, int, float], str, tuple[str, int, float]]) -> tuple[str, int, float]:
        (a, pa, va), op, (b, pb, vb) = parts
        level = 1 if op in "+-" else 2
        left = a if pa >= level else f"({a})"
        right = b if pb > level else f"({b})"
        v = va + vb if op == "+" else va - vb if op == "-" else va * vb if op == "*" else X._divide(va, vb)
        return f"{left}{op}{right}", level, v

    def negate(part: tuple[str, int, float]) -> tuple[str, int, float]:
        a, pa, va = part
        return (f"-{a}" if pa >= 2 else f"-({a})"), 2, -va

    sub = _tree(depth - 1)
    return st.one_of(leaf, st.tuples(sub, st.sampled_from("+-*/"), sub).map(binary), sub.map(negate))


@given(_tree(4))
def test_fewest_brackets_parse_as_precedence_says(tree: tuple[str, int, float]) -> None:
    src, _, expected = tree
    assert same(X.value(src), expected), src


@given(st.integers(-4, 4), st.integers(-3, 3), st.integers(-2, 2))
def test_power_is_right_associative_and_binds_tighter_than_minus(a: int, b: int, c: int) -> None:
    fa, fb, fc = float(a), float(b), float(c)
    scope = {"a": fa, "b": fb, "c": fc}
    assert same(X.value("a^b^c", scope), X.power(fa, X.power(fb, fc)))
    assert same(X.value("-a^b", scope), -X.power(fa, fb))
    assert same(X.value("a^-b^c", scope), X.power(fa, -X.power(fb, fc)))


# Section 3: variables.


def test_free_variables_in_order_of_first_appearance() -> None:
    assert X.parse("y + x*y + z + x").free == ["y", "x", "z"]
    assert X.parse("sum(x, 1, 3, x) + x").free == ["x"] and X.value("sum(x, 1, 3, x) + x", {"x": 10}) == 16
    assert X.parse("sum(k, 1, k, k)").free == ["k"] and X.value("sum(k, 1, k, k)", {"k": 4}) == 10
    assert X.parse("sum(b, a, 3, b) + b").free == ["a", "b"]
    assert X.parse("sum(k, 1, 3, k)").free == [] and X.value("sum(k, 1, 3, k)", {"k": True}) == 6
    assert X.parse("pi * e * E").free == ["E"]
    assert X.value("sum(k, 1, 3, sum(k, 1, k, k))") == 10  # the inner index hides the outer one


@pytest.mark.parametrize("scope", [{}, {"x": True}, {"x": False}, {"x": "1"}, {"x": None}, {"y": 1}])
def test_a_free_variable_without_a_number_is_a_scope_error(scope: dict[str, object]) -> None:
    with pytest.raises(X.ScopeError):
        X.value("x", scope)


def test_a_free_variable_in_a_branch_not_taken_still_needs_a_number() -> None:
    with pytest.raises(X.ScopeError):
        X.value("if(1 < 2, 1, z)")


@given(st.lists(NAMES, min_size=1, max_size=8))
def test_free_lists_each_name_once_in_order(names: list[str]) -> None:
    assert X.parse(" + ".join(names)).free == list(dict.fromkeys(names))


# Section 4: values.

SPECIAL = [
    ("1/0", NAN), ("1/-0", NAN), ("0/0", NAN), (f"{BIG}/0", NAN), ("0^-1", NAN), ("(-0)^-1", NAN),
    (f"0^{NEG_BIG}", NAN),
    ("ln(0)", NAN), ("ln(-0)", NAN), ("log10(-0)", NAN), ("ln(-1)", NAN), ("1^(0/0)", NAN), ("(0/0)^0", NAN),
    ("min(1, 0/0)", NAN), ("sign(0/0)", NAN), ("if(0/0 < 1, 1, 2)", NAN), ("if(1 < 0/0, 1, 2)", NAN),
    ("if(1 < 2, 1, 0/0)", 1.0), ("sum(k, 1.5, 3, k)", NAN), ("sum(k, 1, 9007199254740992, k)", NAN),
    ("sum(k, 0/0, 1, k)", NAN), (f"{BIG}^0", 1.0), ("0^0", 1.0), (f"1^{BIG}", 1.0), (f"(-1)^{NEG_BIG}", 1.0),
    (f"{NEG_BIG}^0.5", INF), ("(-0)^0.5", 0.0), ("(-0)^3", -0.0), (f"2^{BIG}", INF), (f"0.5^{BIG}", 0.0),
    ("(-2)^0.5", NAN), (f"{NEG_BIG}^-3", -0.0), (f"{NEG_BIG}^3", -INF), (f"0.5^{NEG_BIG}", INF), ("(-1)^3", -1.0),
    ("sqrt(-0)", -0.0), ("sqrt(-1)", NAN), ("asin(2)", NAN), ("acos(-2)", NAN), ("cbrt(-27)", -3.0),
    (f"sin({BIG})", NAN), (f"cos({NEG_BIG})", NAN), (f"tan({BIG})", NAN), (f"atan({BIG})", math.pi / 2),
    (f"atan({NEG_BIG})", -math.pi / 2), (f"tanh({BIG})", 1.0), (f"tanh({NEG_BIG})", -1.0), (f"exp({NEG_BIG})", 0.0),
    (f"erf({BIG})", 1.0), (f"erf({NEG_BIG})", -1.0), (f"Phi({NEG_BIG})", 0.0), (f"Phi({BIG})", 1.0),
    (f"phi({BIG})", 0.0), (f"phi({NEG_BIG})", 0.0), ("atan2(0, -0)", math.pi), ("atan2(-0, -0)", -math.pi),
    ("atan2(0, 0)", 0.0), ("atan2(-0, 0)", -0.0), ("atan2(-0, -1)", -math.pi), ("sin(-0)", -0.0), ("tan(-0)", -0.0),
    ("asin(-0)", -0.0), ("atan(-0)", -0.0), ("sinh(-0)", -0.0), ("tanh(-0)", -0.0), ("cbrt(-0)", -0.0),
    ("erf(-0)", -0.0), ("ceil(-0.5)", -0.0), ("sign(-0)", -0.0), ("sign(0)", 0.0), ("abs(-0)", 0.0),
    ("min(0, -0)", -0.0), ("max(-0, 0)", 0.0), ("Phi(0)", 0.5), ("sum(k, 3, 1, k)", 0.0), ("sum(k, 1, 2, -0)", 0.0),
    ("sum(k, 1, 10, 0.1)", 0.9999999999999999), ("2^-1074", 5e-324), ("2^-1075", 0.0), ("(-2)^-1075", -0.0),
]


@pytest.mark.parametrize(("src", "expected"), SPECIAL)
def test_undefined_points_and_special_values(src: str, expected: float) -> None:
    assert same(X.value(src), expected)


def test_nan_in_gives_nan_out_for_every_operator_and_function() -> None:
    sources = [f"{name}(0/0)" for name in X.ONE_ARG] + [
        "atan2(0/0, 1)", "atan2(1, 0/0)", "max(0/0, 1)", "0/0 + 1", "1 - 0/0", "0 * (0/0)", "-(0/0)", "0/0 / 1",
        "(0/0)^1", "1^(0/0)", "sum(k, 1, 2, 0/0)", "sum(k, 0, 0/0, 1)", f"{BIG} * 0", f"{BIG} - {BIG}",
    ]
    for src in sources:
        assert math.isnan(X.value(src)), src


@given(FINITE, FINITE, st.sampled_from("+-*/"))
def test_arithmetic_is_ieee_with_division_by_zero_nan(a: float, b: float, op: str) -> None:
    got = X.value(f"a {op} b", {"a": a, "b": b})
    if op == "/":
        assert same(got, NAN if b == 0 else a / b)
    else:
        assert same(got, a + b if op == "+" else a - b if op == "-" else a * b)


@given(FINITE)
def test_floor_ceil_sign_abs_are_exact(x: float) -> None:
    f, c = float(math.floor(x)), float(math.ceil(x))
    assert X.value("floor(x)", {"x": x}) == f and X.value("ceil(x)", {"x": x}) == c
    assert same(X.value("sign(x)", {"x": x}), x if x == 0 else math.copysign(1.0, x))
    assert same(X.value("abs(x)", {"x": x}), abs(x))
    if c == 0 and x < 0:
        assert same(X.value("ceil(x)", {"x": x}), -0.0)


@given(st.lists(FINITE, min_size=2, max_size=5))
def test_min_and_max_rank_minus_zero_below_plus_zero(values: list[float]) -> None:
    src = ", ".join(f"v{i}" for i in range(len(values)))
    scope = {f"v{i}": v for i, v in enumerate(values)}
    lo = min(values, key=lambda v: (v, math.copysign(1.0, v)))
    hi = max(values, key=lambda v: (v, math.copysign(1.0, v)))
    assert same(X.value(f"min({src})", scope), lo) and same(X.value(f"max({src})", scope), hi)


INEXACT_DOMAINS = {
    "sin": (-1e6, 1e6), "cos": (-1e6, 1e6), "tan": (-1e6, 1e6), "asin": (-1, 1), "acos": (-1, 1),
    "atan": (-1e300, 1e300), "sinh": (-720, 720), "cosh": (-720, 720), "tanh": (-50, 50), "exp": (-750, 720),
    "ln": (5e-324, 1e308), "log10": (5e-324, 1e308), "cbrt": (-1e308, 1e308), "Phi": (-41, 41), "phi": (-41, 41),
    "erf": (-11, 11), "sqrt": (0, 1e308),
}


@settings(max_examples=60, deadline=None)
@given(st.sampled_from(sorted(INEXACT_DOMAINS)), st.floats(0, 1))
def test_each_function_rounds_the_same_at_50_and_100_digits(name: str, t: float) -> None:
    lo, hi = INEXACT_DOMAINS[name]
    x = lo + (hi - lo) * t
    f = X.FUNCTION_TABLE[name]
    at_50 = f(x)
    with X.MP.workdps(100):
        assert same(f(x), at_50), (name, x)


@settings(max_examples=150, deadline=None)
@given(st.floats(1e-3, 1e3), st.floats(-60, 60))
def test_power_rounds_the_same_at_50_and_100_digits(x: float, y: float) -> None:
    at_50 = X.power(x, y)
    with X.MP.workdps(100):
        assert same(X.power(x, y), at_50)


@given(st.floats(1e-3, 1e3), st.integers(-40, 40))
def test_an_integer_power_is_exact_then_rounded(x: float, k: int) -> None:
    exact = Fraction(x) ** k
    assert same(X.power(x, float(k)), float(exact))
    assert same(X.power(-x, float(k)), float(exact) if k % 2 == 0 else -float(exact))


def test_power_rounds_an_exact_half_ulp_to_even() -> None:
    for base in X.TIE_BASES:
        w = math.isqrt(math.isqrt(base))
        assert w**4 == base and w % 2 == 1 and 2**53 <= w**5 < 2**54  # w^5 is halfway between two doubles
        assert X.power(float(base), 1.25) == float(w**5)  # int to float rounds half to even [recalled]
    assert X.value("(2^-860)^1.25") == 0.0 and X.value("(2^-430)^2.5") == 0.0  # exactly 2^-1075
    assert X.value("(2^-859)^1.25") == 5e-324


def test_constants_are_the_nearest_doubles() -> None:
    with X.MP.workdps(100):
        assert X.CONSTANTS == {"pi": X.nearest(X.MP.pi), "e": X.nearest(X.MP.e)}
        assert X.HALF_PI == X.nearest(X.MP.pi / 2) and X.THREE_QUARTERS_PI == X.nearest(3 * X.MP.pi / 4)


def test_the_counter_has_no_signed_zero() -> None:
    assert same(X.value("sum(k, -0, 0, atan2(k, -1))"), math.pi)  # spec 4: lo = -0 starts the counter at +0
    assert same(X.value("sum(k, -0, -0, sign(k))"), 0.0)
    assert same(X.value("sum(k, -1, 0, atan2(k, -1))"), X.value("atan2(-1, -1) + atan2(0, -1)"))  # k reaches +0
    assert X.value("sum(k, -2, 2, k)") == 0 and X.value("sum(k, 1, 4, 1/k)") == 1 + 0.5 + 1 / 3 + 0.25


# Section 5: the work budget.


def test_the_spec_budget_examples() -> None:
    assert X.parse(X.TERM_500).root.size == 500
    assert X.value("sum(k, 1, 2000, " + X.TERM_500 + ")") == 2000
    assert math.isnan(X.value("sum(k, 1, 2001, " + X.TERM_500 + ")"))
    assert X.value("sum(i, 1, 400, sum(j, 1, 2496, 1))") == 998400
    assert math.isnan(X.value("sum(i, 1, 400, sum(j, 1, 2497, 1))"))


@pytest.mark.parametrize(
    ("src", "nodes"),
    [("1", 1), ("x", 1), ("pi", 1), ("-x", 2), ("---x", 4), ("x + y", 3), ("2^3^4", 5), ("-2^-3", 5),
     ("min(1, 2, 3)", 4), ("if(x < 0, 1, 2)", 5), ("sum(k, 1, 2, k)", 4), ("((x))", 1), ("sin(x) * 2", 4), ("2^-3", 4)],
)
def test_node_counts(src: str, nodes: int) -> None:
    assert X.parse(src).root.size == nodes


@settings(max_examples=40, deadline=None)
@given(st.integers(50, 400), st.integers(-1, 1))
def test_a_sum_is_nan_exactly_when_it_costs_more_than_is_left(nodes: int, step: int) -> None:
    n = X.BUDGET // nodes + step
    v = X.value(f"sum(k, 1, {n}, {term(nodes)})")
    assert same(v, NAN if n * nodes > X.BUDGET else float(n))


def test_the_budget_counts_what_runs() -> None:
    assert X.value("if(1 < 2, 1, sum(k, 1, 1e9, k))") == 1  # a branch not taken costs nothing
    assert math.isnan(X.value("if(1 > 2, 1, sum(k, 1, 1e9, k))"))
    assert X.value("sum(k, 1, 0, sum(j, 1, 1e9, j))") == 0  # no terms, so the inner sum never runs
    assert X.value("sum(k, 1, sum(j, 1, 2000, 1), " + term(499) + ")") == 2000  # lo and hi pay first
    assert math.isnan(X.value("sum(k, 1, sum(j, 1, 2001, 1), " + term(499) + ")"))
    assert math.isnan(X.value("0 * sum(k, 1, 1e9, k)")) and math.isnan(X.value("sum(k, 1, 1e9, k)^0"))
    assert X.value("sum(k,1,2000," + term(250) + ")+sum(k,1,2000," + term(250) + ")") == 4000
    assert math.isnan(X.value("sum(k,1,2000," + term(250) + ")+sum(k,1,2001," + term(250) + ")"))


# The security floor: no eval and no platform maths.


def test_the_twin_uses_no_eval_and_no_platform_maths() -> None:
    tree = ast.parse(Path(X.__file__).read_text(encoding="utf-8"))
    calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert not calls & {"eval", "exec", "compile", "__import__"}
    imported = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    imported |= {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    assert imported == {"__future__", "json", "math", "operator", "random", "collections.abc", "functools", "pathlib",
                        "mpmath"}
    used = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute) and getattr(n.value, "id", "") == "math"}
    assert used <= {"inf", "nan", "isfinite", "isinf", "copysign", "ldexp", "isqrt"}  # exact operations only
