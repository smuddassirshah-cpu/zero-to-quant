"""The scale goldens are fresh, and the twin's ticks keep the properties the specification states."""

import math
from fractions import Fraction

from hypothesis import assume, given, strategies as st

from zqverify import scale


def test_the_committed_goldens_are_fresh() -> None:
    assert scale.GOLDEN.read_text(encoding="utf-8") == scale.render()


def test_linear_and_log_ticks() -> None:
    assert scale.linear_ticks(0.0, 1.0, 5) == [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    assert scale.linear_ticks(0.1, 0.9, 1) == [0.5]
    assert scale.log_ticks(1.0, 1000.0, 10) == [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0]
    assert scale.log_ticks(1.0, 1000.0, 3) == [1.0, 100.0]
    assert scale.log_ticks(2.0, 3.0, 5) == [2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
    assert scale.log_ticks(1e-300, 1e300, 10) == [float(f"1e{p}") for p in range(-300, 301, 100)]


def test_coarser_log_sets_keep_their_decades_and_narrow_domains_go_linear() -> None:
    decades = [1.0, 10.0, 100.0, 1000.0]
    assert scale.log_ticks(1.0, 1000.0, 9) == decades
    assert scale.log_ticks(1.0, 1000.0, 21) == [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0]
    assert scale.log_ticks(0.1, 1000.0, 11) == [0.1, *decades]
    assert scale.log_ticks(1.0, 1e6, 15) == [*decades, 1e4, 1e5, 1e6]
    assert scale.log_ticks(1.0, 1000.0, 100) == [10.0 * k for k in range(1, 101)]
    assert scale.log_ticks(3.0, 4.0, 1) == [3.0, 4.0]
    assert scale.log_ticks(3.0, 9.0, 3) == [4.0, 6.0, 8.0]
    assert scale.log_ticks(math.nextafter(1e6, math.inf), 1e14, 5) == [1e8, 1e10, 1e12, 1e14]


def test_candidates_past_the_largest_double_round_to_infinity() -> None:
    assert scale.rounded(scale.OVERFLOW) == math.inf and scale.rounded(-scale.OVERFLOW) == -math.inf
    assert scale.linear_ticks(-1e308, 7e307, 3) == [-1e308, -5e307, 0.0, 5e307]
    assert scale.linear_ticks(-1.8745939238210245e307, 5.929848004911144e307, 1) == [0.0]
    assert scale.log_ticks(1e306, 1.7e308, 2) == [1e306, 1e308]


def test_maps_are_exact_at_the_ends_and_degenerate_sides_take_the_middle() -> None:
    assert scale.linear(0.0, 10.0, 10.0, 300.0, 0.0) == 0.0
    assert scale.linear(3.0, 3.0, -7.0, 0.0, 100.0) == 50.0
    assert scale.log_invert((1.0, 100.0), (2.0, 2.0), 2.0) == 10.0
    assert scale.log_map((1.0, 1000.0), (0.0, 300.0), 10.0) == 100.0


@given(st.floats(-1e6, 1e6), st.floats(1e-3, 1e6), st.integers(1, 50))
def test_linear_ticks_are_increasing_inside_and_bounded(lo: float, span: float, c: int) -> None:
    hi = lo + span
    ticks = scale.linear_ticks(lo, hi, c)
    assert 1 <= len(ticks) <= int(1.59 * max(c, 2)) + 1
    assert all(lo <= a < b <= hi for a, b in zip(ticks, ticks[1:])) and lo <= ticks[0] and ticks[-1] <= hi


@given(st.floats(-300, 300), st.floats(0.005, 300), st.integers(1, 30))
def test_log_ticks_are_increasing_inside_and_bounded(e: float, w: float, c: int) -> None:
    lo, hi = 10.0**e, 10.0 ** min(e + w, 307.0)
    ticks = scale.log_ticks(lo, hi, c)
    assert 1 <= len(ticks) <= int(1.59 * max(c, 2)) + 1
    assert all(a < b for a, b in zip(ticks, ticks[1:])) and lo <= ticks[0] and ticks[-1] <= hi


@given(st.integers(-300, 280), st.floats(2, 27), st.integers(1, 30), st.sampled_from((0.0, math.inf)))
def test_wide_log_ticks_start_within_a_decade(p: int, w: float, c: int, side: float) -> None:
    """Over a hundredfold domain whose powers of ten fit c, the first tick is at most 10 lo."""
    lo, hi = math.nextafter(float(f"1e{p}"), side), 10.0 ** (p + w)
    assume(hi >= 100 * lo and sum(lo <= float(f"1e{q}") <= hi for q in range(p - 1, p + 29)) <= c)
    assert scale.log_ticks(lo, hi, c)[0] <= 10 * lo


finite = st.floats(allow_nan=False, allow_infinity=False)


@st.composite
def sides(draw: st.DrawFn) -> tuple[float, float]:
    """Ends a few doubles apart anywhere, subnormal ones included, or far apart, in either order."""
    a = draw(finite)
    b = math.nextafter(a, math.inf, steps=draw(st.integers(0, 4))) if draw(st.booleans()) else draw(finite)
    assume(math.isfinite(b - a))
    return (b, a) if draw(st.booleans()) else (a, b)


def test_values_that_are_not_finite_or_positive_are_refused() -> None:
    for v in scale.REFUSED:
        assert scale.linear(0.0, 10.0, v, 300.0, 0.0) is None and scale.linear(3.0, 3.0, v, 0.0, 1.0) is None
        assert scale.log_map((1.0, 1000.0), (0.0, 300.0), v) is None
        assert scale.log_invert((1.0, 1000.0), (0.0, 300.0), v) is None
    assert scale.log_map((1.0, 1000.0), (0.0, 300.0), 0.0) is None
    assert scale.log_map((1.0, 1000.0), (0.0, 300.0), -1.0) is None


def test_overflowing_fractions_give_signed_infinities_or_finite_values() -> None:
    up1 = math.nextafter(1.0, math.inf)
    assert scale.linear(1.0, up1, 1e300, 0.0, 400.0) == math.inf
    assert scale.linear(up1, 1.0, -1e300, 300.0, 0.0) == -math.inf
    assert scale.linear(0.0, 1e-300, 1e10, 0.0, 1e-300) == 1e10
    assert scale.linear(0.0, scale.TINY, 1.0, 400.0, 0.0) == -math.inf
    assert scale.linear(0.0, scale.TINY, 1e-320, 0.0, 10.0) == 20240.0
    assert scale.log_invert((scale.TINY, scale.MAX), (0.0, 400.0), 600.0) == math.inf
    assert scale.log_invert((scale.TINY, scale.MAX), (0.0, 400.0), -200.0) == 0.0
    assert scale.log_invert((1.0, 1000.0), (0.0, scale.TINY), 1.0) == math.inf
    assert scale.log_invert((5.0, 5.0), (0.0, 1e-323), 1e10) == 5.0


@given(sides(), finite)
def test_a_side_onto_itself_is_the_identity(d: tuple[float, float], x: float) -> None:
    assume(d[0] != d[1])
    assert scale.linear(*d, x, *d) == x


@given(sides(), sides(), finite, finite)
def test_linear_maps_are_monotone_and_signed(
    d: tuple[float, float], r: tuple[float, float], x: float, y: float
) -> None:
    """Monotone in the direction the sides give, constant where one is a single value; and plus or minus
    infinity, signed as the exact value, where that lies beyond the doubles."""
    lo, hi = sorted((x, y))
    a, b = scale.linear(*d, lo, *r), scale.linear(*d, hi, *r)
    assert a is not None and b is not None
    if d[0] == d[1] or r[0] == r[1]:
        assert a == b
        return
    assert a == b or (b - a) * math.copysign(1.0, (d[1] - d[0]) * (r[1] - r[0])) > 0
    exact = Fraction(r[0]) + (Fraction(hi) - Fraction(d[0])) / (Fraction(d[1]) - Fraction(d[0])) * (
        Fraction(r[1]) - Fraction(r[0])
    )
    assert b == (math.inf if exact > 0 else -math.inf) if abs(exact) >= scale.OVERFLOW else math.isfinite(b)
