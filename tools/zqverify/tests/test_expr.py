"""The expression twin against hand values, its whitelist, and the freshness of the goldens it writes."""

import math

import pytest

from zqverify import expr


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


def test_the_sum_budget_counts_terms_in_all() -> None:
    assert expr.evaluate("sum(i, 1, 400, sum(j, 1, 249, 1))", {}) == 99_600
    assert math.isnan(expr.evaluate("sum(i, 1, 400, sum(j, 1, 250, 1))", {}))


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
