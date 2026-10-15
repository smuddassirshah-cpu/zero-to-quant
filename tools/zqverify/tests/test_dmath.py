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
@pytest.mark.parametrize("x", GRID)
@pytest.mark.parametrize("y", GRID)
def test_pow_special_agrees_with_cpython(x: float, y: float) -> None:
    want = dmath.pow_special(x, y)
    try:
        got = math.pow(x, y)
    except ValueError:
        assert want is not None and (math.isnan(want) or math.isinf(want))
        return
    except OverflowError:
        assert want is None
        return
    if want is not None:
        assert same(want, got)


@pytest.mark.parametrize("name", ["exp", "log", "log1p", "expm1", "tanh", "sin", "cos"])
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


# e_exp.c's and s_expm1.c's constants (FreeBSD release/14.1.0), to show the hard cases sit on their switches.
INVLN2 = 1.44269504088896338700e00
LN2_HI = 6.93147180369123816490e-01
LN2_LO = 1.90821492927058770002e-10


def c_k(x: float) -> int:
    """The C's k = (int)(invln2*x + (x < 0 ? -0.5 : 0.5)), truncated towards zero."""
    return int(INVLN2 * x + math.copysign(0.5, x))


def test_exp_k2_is_the_first_double_with_k_two() -> None:
    below = math.nextafter(dmath.EXP_K2, 0)
    assert (c_k(below), c_k(dmath.EXP_K2)) == (1, 2)
    assert (c_k(-below), c_k(-dmath.EXP_K2)) == (-1, -2)


def test_ln2_less_a_quarter_is_where_expm1s_k1_test_first_fails() -> None:
    def reduced_below(x: float) -> bool:  # s_expm1.c's k = 1 form: hi = x - ln2_hi, lo = ln2_lo, x = hi - lo
        return (x - LN2_HI) - LN2_LO < -0.25

    switch = dmath.LN2 - 0.25
    assert switch + 0.25 == dmath.LN2
    assert reduced_below(math.nextafter(switch, 0)) and not reduced_below(switch)


def test_references_hold_at_100_digits() -> None:
    for name, rows in dmath.cases():
        for args in rows:
            assert dmath.reference(name, args, 100) == dmath.reference(name, args), (name, args)
