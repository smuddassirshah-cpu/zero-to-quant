"""The expression twin against hand values, its whitelist, and the freshness of the goldens it writes."""

import math
from decimal import Decimal

import pytest

from zqverify import expr

INF = expr.INF_TEXT


@pytest.mark.parametrize(
    ("source", "scope", "value"),
    [
        ("1 + 2*3", {}, 7.0),
        ("2^3^2", {}, 512.0),
        ("-2^2", {}, -4.0),
        ("2^-1", {}, 0.5),
        ("x - y - z", {"x": 1.0, "y": 2.0, "z": 3.0}, -4.0),
        ("x/y*z", {"x": 1.0, "y": 4.0, "z": 2.0}, 0.5),
        ("sum(k, 1, 10, k^2)", {}, 385.0),
        ("sum(x, 1, 3, x) + x", {"x": 10.0}, 16.0),
        ("if(x < 0, -x, x)", {"x": -3.0}, 3.0),
        ("lambda*2", {"lambda": 3.0}, 6.0),
        ("Phi(0)", {}, 0.5),
        ("min(0, -0)", {}, -0.0),
        ("ceil(-0.5)", {}, -0.0),
        ("sqrt(-0)", {}, -0.0),
        ("cbrt(-27)", {}, -3.0),
        ("atan2(-0, -1)", {}, -math.pi),
        ("(-0)^3", {}, -0.0),
        # Annex F, where NumPy's power gave nan and -0 [measured, stage 3 review]
        (f"(-{INF})^0.5", {}, math.inf),
        ("(-0)^0.5", {}, 0.0),
        # the language's own rule: (+-1)^(+-inf) is 1
        (f"1^({INF})", {}, 1.0),
        (f"(-1)^(-{INF})", {}, 1.0),
        ("-" * 999 + "1", {}, -1.0),
        ("1" + "+1" * 499, {}, 500.0),
        ("2^" * 499 + "1", {}, math.inf),
    ],
)
def test_values(source: str, scope: dict[str, float], value: float) -> None:
    got = expr.evaluate(source, scope)
    assert got == value and math.copysign(1.0, got) == math.copysign(1.0, value)


@pytest.mark.parametrize(
    "source", ["1/0", "0^-1", "ln(0)", "log10(-1)", "1^(0/0)", "if(0/0 < 1, 1, 2)", "sum(k, 0.5, 1, k)"]
)
def test_undefined_points_are_nan(source: str) -> None:
    assert math.isnan(expr.evaluate(source, {}))


@pytest.mark.parametrize(
    ("source", "digits"),
    [
        ("acos(0.5)", "1.047197551196597746154214461093167628066"),
        ("phi(0.5)", "0.3520653267642994777746804415965176531103"),
        ("Phi(1.5)", "0.9331927987311419339955059590201139204771"),
        ("2^0.5", "1.414213562373095048801688724209698078570"),
    ],
)
def test_inexact_values_are_correctly_rounded(source: str, digits: str) -> None:
    """Against 40-digit decimals, which float() rounds correctly, so no CPU or libm enters."""
    assert expr.evaluate(source, {}) == float(Decimal(digits))


def test_the_sum_budget_counts_term_nodes_in_all() -> None:
    assert expr.evaluate(expr.wide(2000), {}) == 2000
    assert math.isnan(expr.evaluate(expr.wide(2001), {}))
    assert expr.evaluate("sum(i, 1, 400, sum(j, 1, 2496, 1))", {}) == 400 * 2496
    assert math.isnan(expr.evaluate("sum(i, 1, 400, sum(j, 1, 2497, 1))", {}))


@pytest.mark.parametrize(
    "source",
    [
        "__import__('os')",
        "x.real",
        "(1).hex()",
        "[x for x in y]",
        "x if y else z",
        "not x",
        "x and y",
        "x in y",
        "x is y",
        "await x",
        "sin(*x)",
        "sin(x=1)",
        "x(1)",
        "(1, 2)",
        "1 < 2",
        "if(x, 1, 2)",
        "sum(1, 1, 2, 3)",
        "if(x < 0, 1, sin)",
        "+1",
        "sin(1,)",
        "(sin)(1)",
        "if((1 < 2), 1, 2)",
        "sum((k), 1, 2, k)",
        "0x10",
        "1_000",
        "1" + " + 1" * 250,
        "(" * 33 + "1" + ")" * 33,
        "123456789012345678901",
        "\u0661 + 1",
        "\uff11 + 1",
        "1\u0663",
        "\U0001d7cf*2",
    ],
)
def test_rejects_everything_outside_the_grammar(source: str) -> None:
    with pytest.raises(expr.ExprError):
        expr.parse(source)


def test_needs_every_free_variable_in_the_scope() -> None:
    assert expr.parse("sum(k, 1, n, k*x) + x")[1] == ["n", "x"]
    with pytest.raises(expr.ScopeError):
        expr.evaluate("x + y", {"x": 1.0})
    with pytest.raises(expr.ScopeError):
        expr.evaluate("x", {"x": True})


def test_the_goldens_are_fresh() -> None:
    assert expr.GOLDEN.read_text(encoding="utf-8") == expr.render()
