"""The dmath goldens: reproducible, correctly rounded, Annex F's special values, stable at 100 digits."""

import math
from fractions import Fraction

import mpmath
import pytest

from zqverify import dmath

GRID = [0.0, -0.0, 0.5, -0.5, 1.0, -1.0, 1.5, -2.0, 3.0, -3.0, math.inf, -math.inf, math.nan, 5e-324]


def same(a: float, b: float) -> bool:
    return dmath.bits(a) == dmath.bits(b) or (math.isnan(a) and math.isnan(b))


def test_the_committed_goldens_are_what_the_script_writes() -> None:
    assert dmath.GOLDENS.read_text(encoding="utf-8") == dmath.render()


def test_ten_thousand_cases_split_as_counted() -> None:
    assert sum(dmath.COUNTS.values()) == 10_000
    assert {name: len(rows) for name, rows in dmath.cases()} == dmath.COUNTS


@pytest.mark.parametrize(
    ("value", "want"),
    [
        (Fraction(1, 2**1075), 0.0),  # half the least subnormal: ties to even, down
        (Fraction(-1, 2**1075), -0.0),
        (Fraction(3, 2**1076), 5e-324),
        (Fraction(2**1024 - 2**970), math.inf),  # halfway past the largest double
        (Fraction(2**1024 - 2**970 - 1), dmath.MAX),
        (1 + Fraction(1, 2**53), 1.0),
        (1 + Fraction(3, 2**53), 1 + 2.0**-51),
    ],
)
def test_nearest_rounds_to_nearest_ties_to_even(value: Fraction, want: float) -> None:
    with mpmath.workdps(400):
        assert same(dmath.nearest(mpmath.mpf(value.numerator) / value.denominator), want)


def test_ulp() -> None:
    assert dmath.ulp(1.0) == Fraction(1, 2**52)
    assert dmath.ulp(-1.5) == Fraction(1, 2**52)
    assert dmath.ulp(dmath.MAX) == 2**971
    assert dmath.ulp(0.0) == dmath.ulp(dmath.MIN_NORMAL) == Fraction(1, 2**1074)


# CPython's math module follows Annex F where it returns, and raises ValueError at a pole or a domain error.
@pytest.mark.parametrize("name", ["exp", "log", "log1p", "expm1", "tanh"])
@pytest.mark.parametrize("x", [*GRID, -1.5, -math.inf])
def test_special_agrees_with_cpython(name: str, x: float) -> None:
    want = dmath.special(name, x)
    try:
        got = getattr(math, name)(x)
    except ValueError:
        assert want is not None and (math.isnan(want) or math.isinf(want))
        return
    if want is not None:
        assert same(want, got)


def test_references_hold_at_100_digits() -> None:
    for name, rows in dmath.cases():
        for args in rows:
            assert dmath.reference(name, args, 100) == dmath.reference(name, args), (name, args)
