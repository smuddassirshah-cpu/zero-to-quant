"""The scale twin against docs/ARCHITECTURE.md 5.16: fresh goldens, the refusals, the one-valued rules, exact
ends, the examples, the tick rules and their bounds, a float port of d3-array 3.2.4's ticks on ordinary domains,
and the references against plain double arithmetic and against more digits."""

import json
import math
from fractions import Fraction

import pytest
from hypothesis import assume, given, settings, strategies as st

from zqverify import scale as C
from zqverify.stats import LEAST, MAX, U, RangeError, nearest

SLOW = settings(deadline=None, max_examples=200)
FINITE = st.floats(allow_nan=False, allow_infinity=False)
POSITIVE = st.floats(min_value=LEAST, max_value=MAX)
ORDINARY = st.floats(min_value=-1e12, max_value=1e12, allow_nan=False)
COUNT = st.integers(1, 1000) | st.sampled_from([1, 2, 3, 5, 10])


def refused(f, *args) -> bool:
    try:
        f(*args)
    except RangeError:
        return True
    return False


@st.composite
def linear_scales(draw: st.DrawFn, ends: st.SearchStrategy[float] = FINITE) -> C.Scale:
    d0, d1, r0, r1 = (draw(ends) for _ in range(4))
    assume(math.isfinite(d1 - d0) and math.isfinite(r1 - r0))
    return C.linear_scale((d0, d1), (r0, r1))


@st.composite
def log_scales(draw: st.DrawFn, ends: st.SearchStrategy[float] = POSITIVE) -> C.Scale:
    d0, d1 = draw(ends), draw(ends)
    r0, r1 = draw(FINITE), draw(FINITE)
    assume(math.isfinite(r1 - r0))
    return C.log_scale((d0, d1), (r0, r1))


SCALES = linear_scales() | log_scales()


# --- goldens -------------------------------------------------------------------------------------------------


def test_the_committed_goldens_are_fresh() -> None:
    assert C.GOLDEN.read_text(encoding="utf-8") == C.render()


def test_every_golden_line_reads_back_and_its_strings_are_what_number_reads() -> None:
    lines = [json.loads(line) for line in C.GOLDEN.read_text(encoding="utf-8").splitlines()]
    assert lines == C.goldens()
    strings = {v for g in lines for key in ("x", "map", "y", "invert") for v in g[key] if isinstance(v, str)}
    assert strings == {"Infinity", "-Infinity", "NaN"}


def test_the_goldens_reach_refusals_infinities_zeros_both_kinds_and_both_count_limits() -> None:
    gs = C.goldens()
    assert {g["kind"] for g in gs} == {"linear", "log"} and len(gs) > 350
    results = [v for g in gs for key in ("map", "invert") for v in g[key]]
    assert None in results and "Infinity" in results and "-Infinity" in results and 0.0 in results
    assert {1, C.COUNT_LIMIT} <= {g["count"] for g in gs}
    assert any(g["domain"][0] > g["domain"][1] for g in gs) and any(g["domain"][0] == g["domain"][1] for g in gs)
    log_zero = [g for g in gs if g["kind"] == "log" and 0.0 in g["invert"]]
    assert log_zero and any(g["kind"] == "log" and "Infinity" in g["invert"] for g in gs)


# --- construction and refusals -------------------------------------------------------------------------------


@pytest.mark.parametrize("domain, range_", [
    ((math.inf, 1), (0, 1)), ((0, math.nan), (0, 1)), ((0, 1), (-math.inf, 1)), ((0, 1), (0, math.nan)),
    ((-1e308, 1e308), (0, 1)), ((0, 1), (-1e308, 1e308)),
])
def test_a_linear_scale_needs_finite_ends_and_spans(domain, range_) -> None:
    assert refused(C.linear_scale, domain, range_)


@pytest.mark.parametrize("domain, range_", [
    ((0, 10), (0, 1)), ((-1, 10), (0, 1)), ((-0.0, 1), (0, 1)), ((1, math.inf), (0, 1)), ((1, 10), (-1e308, 1e308)),
    ((math.nan, 10), (0, 1)),
])
def test_a_log_scale_needs_positive_finite_ends_and_a_finite_range_span(domain, range_) -> None:
    assert refused(C.log_scale, domain, range_)


def test_the_widest_scales_that_are_allowed() -> None:
    C.linear_scale((-8e307, 8e307), (-8e307, 8e307))
    C.log_scale((LEAST, MAX), (-8e307, 8e307))


@pytest.mark.parametrize("v", [math.nan, math.inf, -math.inf])
def test_map_and_invert_take_finite_values_only(v: float) -> None:
    for s in (C.linear_scale((0, 1), (0, 1)), C.log_scale((1, 10), (0, 1)), C.linear_scale((2, 2), (5, 5))):
        assert refused(s.map, v) and refused(s.invert, v)


@pytest.mark.parametrize("x", [0.0, -0.0, -1.0, -LEAST])
def test_a_log_map_takes_positive_values_only(x: float) -> None:
    assert refused(C.log_scale((1, 10), (0, 1)).map, x) and refused(C.log_scale((3, 3), (0, 1)).map, x)


@pytest.mark.parametrize("c", [0, 1001, -1, 2.5, math.nan, math.inf, 1e300, 10**400])
def test_ticks_take_an_integer_count_from_1_to_1000(c) -> None:
    assert refused(C.linear_scale((0, 1), (0, 1)).ticks, c) and refused(C.log_scale((1, 9), (0, 1)).ticks, c)


def test_ticks_accept_1_1000_and_an_integral_double() -> None:
    s = C.linear_scale((0, 1), (0, 1))
    assert s.ticks(1) == [0.0, 1.0] and len(s.ticks(1000)) == 1001 and s.ticks(5.0) == s.ticks(5)
    with pytest.raises(TypeError):
        s.ticks(True)


# --- one-valued sides and exact ends -------------------------------------------------------------------------


def test_one_valued_sides() -> None:
    assert C.linear_scale((3, 3), (0, 1)).map(-1e308) == 0.5 and C.log_scale((3, 3), (0, 1)).map(1e-300) == 0.5
    assert C.linear_scale((0, 10), (5, 5)).invert(1e9) == 5.0
    assert C.log_scale((1, 100), (2, 2)).invert(0) == 10.0  # the geometric middle
    assert C.log_scale((2, 3), (1, 1)).invert(7) == math.sqrt(6)  # correctly rounded, as Math.sqrt is
    assert C.log_scale((7, 7), (0, 1)).invert(0.3) == 7.0 and C.log_scale((7, 7), (4, 4)).invert(1) == 7.0
    assert C.linear_scale((2, 2), (7, 7)).invert(1) == 2.0 and C.linear_scale((2, 2), (0, 1)).invert(0.9) == 2.0
    assert C.linear_scale((1, 1), (-1, 2)).map(1) == 0.5
    for s in (C.linear_scale((3, 3), (0, 1)), C.log_scale((3, 3), (0, 1))):
        assert s.ticks(10) == [3.0]


@SLOW
@given(SCALES)
def test_each_end_of_the_domain_maps_to_its_end_of_the_range_and_back(s: C.Scale) -> None:
    (d0, d1), (r0, r1) = s.domain, s.range
    assume(d0 != d1 and r0 != r1)
    assert s.map(d0) == r0 and s.map(d1) == r1 and s.invert(r0) == d0 and s.invert(r1) == d1


# --- the maps ------------------------------------------------------------------------------------------------


def test_map_examples() -> None:
    s = C.linear_scale((0, 1), (0, 100))
    assert [s.map(x) for x in (0.5, 0.3, -2, 7)] == [50.0, 30.0, -200.0, 700.0]
    assert [s.invert(y) for y in (30, 250)] == [0.3, 2.5]
    narrow = C.linear_scale((0, 1e-300), (0, 1))
    assert narrow.map(1e300) == math.inf and narrow.map(-1e300) == -math.inf  # beyond the doubles
    log = C.log_scale((1, 1000), (0, 3))
    assert [log.map(x) for x in (10, 100, 1e6)] == [1.0, 2.0, 6.0] and log.invert(1.5) == 10**1.5
    assert C.log_scale((1, 100), (-1, 1)).map(10) == 0.0  # t is exactly 1/2
    assert C.log_scale((2, 3), (0, 1)).invert(1e5) == math.inf and C.log_scale((2, 3), (0, 1)).invert(-1e5) == 0.0


def _unit(a: float, b: float, t: float) -> float:
    """5.16's unit for the value at t of an affine map onto [a, b], with the least subnormal as a floor."""
    return max(U * (abs(a) + abs(b)) * max(1.0, abs(t)), LEAST)


@SLOW
@given(linear_scales(ORDINARY), ORDINARY)
def test_a_linear_map_is_near_plain_double_arithmetic(s: C.Scale, x: float) -> None:
    (d0, d1), (r0, r1) = s.domain, s.range
    assume(d0 != d1)
    t = (x - d0) / (d1 - d0)
    plain = r0 + (r1 - r0) * t
    assume(abs(plain) < MAX / 2)
    assert abs(s.map(x) - plain) <= 8 * _unit(r0, r1, t)  # the plain formula rounds four times


@SLOW
@given(log_scales(st.floats(min_value=1e-100, max_value=1e100)), st.floats(min_value=1e-100, max_value=1e100))
def test_a_log_map_is_near_plain_double_arithmetic(s: C.Scale, x: float) -> None:
    (d0, d1), (r0, r1) = s.domain, s.range
    assume(abs(math.log(d1) - math.log(d0)) > 1e-3)
    t = (math.log(x) - math.log(d0)) / (math.log(d1) - math.log(d0))
    plain = r0 + (r1 - r0) * t
    assume(abs(plain) < MAX / 2)  # where the plain formula overflows, the reference is +-inf or near MAX
    assert abs(s.map(x) - plain) <= 1e6 * _unit(r0, r1, t)  # the logs' cancellation, at most 1e6 u


@settings(deadline=None, max_examples=60)
@given(log_scales(), POSITIVE, FINITE)
def test_the_log_references_hold_at_80_digits(s: C.Scale, x: float, y: float) -> None:
    at50 = (s.map(x), s.invert(y))
    digits, C.DIGITS = C.DIGITS, 80
    try:
        assert (s.map(x), s.invert(y)) == at50
    finally:
        C.DIGITS = digits


@SLOW
@given(SCALES, FINITE, FINITE)
def test_map_and_invert_are_monotone(s: C.Scale, a: float, b: float) -> None:
    (d0, d1), (r0, r1) = s.domain, s.range
    rising = (d1 > d0) == (r1 > r0)
    if s.kind == "log":
        a, b = abs(a) or 1.0, abs(b) or 1.0
    lo, hi = sorted((a, b))
    if d0 != d1:
        assert (s.map(lo) <= s.map(hi)) if rising else (s.map(lo) >= s.map(hi))
    if r0 != r1 and d0 != d1:
        assert (s.invert(lo) <= s.invert(hi)) if rising else (s.invert(lo) >= s.invert(hi))


@SLOW
@given(linear_scales(ORDINARY), ORDINARY)
def test_a_linear_invert_undoes_the_map(s: C.Scale, x: float) -> None:
    (d0, d1), (r0, r1) = s.domain, s.range
    assume(d0 != d1 and r0 != r1)
    y = s.map(x)
    assume(math.isfinite(y))
    # y is within an ulp of the exact image; carried back through the inverse, plus the invert's own rounding.
    slack = Fraction(math.ulp(y)) * abs(Fraction(d1) - Fraction(d0)) / abs(Fraction(r1) - Fraction(r0))
    assert abs(Fraction(s.invert(y)) - Fraction(x)) <= slack + 2 * Fraction(math.ulp(x))


# --- ticks ---------------------------------------------------------------------------------------------------


TENTHS = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


@pytest.mark.parametrize("kind, domain, count, ticks", [
    ("linear", (0, 1), 10, TENTHS),
    ("linear", (1, 0), 10, TENTHS),
    ("linear", (0, 100), 5, [0.0, 20.0, 40.0, 60.0, 80.0, 100.0]),
    ("linear", (0, 10), 3, [0.0, 5.0, 10.0]),
    ("linear", (-1, 1), 1, [0.0]),
    ("linear", (0.11, 0.19), 1, [0.15]),  # no multiple of 0.1 at c = 1, so c = 2's step 0.05
    ("linear", (0.5, 0.7), 1, [0.6]),
    ("linear", (1, 1 + 2**-52), 10, [1.0, 1 + 2**-52]),  # multiples finer than the doubles count once
    ("log", (2, 9), 4, [2.0, 5.0]),  # 5.16's example
    ("log", (2, 9), 5, [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]),  # {1, 2, 5} gives 2 < 2.5 under a decade
    ("log", (1, 1000), 10, [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0]),
    ("log", (1000, 1), 10, [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0]),
    ("log", (1, 10), 10, [float(k) for k in range(1, 11)]),
    ("log", (1, 2), 10, [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]),  # 2 < 5 from {1..9}: linear
    ("log", (1, 2), 3, [1.0, 2.0]),
    ("log", (1, 5), 3, [1.0, 2.0, 5.0]),
    ("log", (2, 90), 9, [2.0, 5.0, 10.0, 20.0, 50.0]),
    ("log", (2, 90), 11, [2.0, 5.0, 10.0, 20.0, 50.0]),  # 5 < 5.5 from {1, 2, 5}, kept: wider than a decade
    ("log", (1e-300, 1e300), 5, [1e-200, 1.0, 1e200]),  # p a multiple of 200
    ("log", (1, 1000), 1, [1.0, 100.0]),  # max(c, 2) powers
    ("log", (3, 8), 20, [nearest(Fraction(15 + k, 5)) for k in range(26)]),
    ("log", (LEAST, 3 * LEAST), 3, [LEAST, 2 * LEAST]),  # 5e-324 to 9e-324 and 1e-323 round onto these two
])
def test_tick_examples(kind, domain, count, ticks) -> None:
    s = C.linear_scale(domain, (0, 1)) if kind == "linear" else C.log_scale(domain, (0, 1))
    assert s.ticks(count) == ticks


def test_the_step_thresholds_are_exact() -> None:
    # r = 7.1 / 1 with p = 0: 7.1^2 = 50.41 >= 50 gives 10; r = 7 gives 49 < 50, so 5.
    assert C.linear_step(0, 7.1, 1) == 10 and C.linear_step(0, 7, 1) == 5
    assert C.linear_step(0, 3.17, 1) == 5 and C.linear_step(0, 3.16, 1) == 2  # 10.0489 and 9.9856
    assert C.linear_step(0, 1.42, 1) == 2 and C.linear_step(0, 1.41, 1) == 1  # 2.0164 and 1.9881
    assert C.linear_step(0, 1e-320, 10) == Fraction(1, 10**321)


@SLOW
@given(SCALES, COUNT)
def test_ticks_are_increasing_doubles_inside_the_domain_whatever_its_orientation(s: C.Scale, c: int) -> None:
    ticks = s.ticks(c)
    lo, hi = sorted(s.domain)
    assert ticks and all(lo <= t <= hi for t in ticks) and all(a < b for a, b in zip(ticks, ticks[1:]))
    flipped = C.Scale(s.kind, s.domain[::-1], s.range)
    assert flipped.ticks(c) == ticks


@SLOW
@given(linear_scales(), COUNT)
def test_linear_ticks_are_the_multiples_of_one_step_within_5_16s_count(s: C.Scale, c: int) -> None:
    lo, hi = sorted(s.domain)
    assume(lo != hi)
    ticks, step = s.ticks(c), C.linear_step(lo, hi, c)
    if not C._multiples(step, lo, hi):
        assert c == 1
        step = C.linear_step(lo, hi, 2)
    e = C.decade(step)
    assert step / C.pow10(e) in (1, 2, 5)
    for t in ticks:
        assert nearest(round(Fraction(t) / step) * step) == t
    spacing = max(math.ulp(lo), math.ulp(hi))
    limit = math.floor(1.59 * max(c, 2)) + 1
    assert len(ticks) <= (limit if step > 5 * Fraction(spacing) else limit + 2)


def _mantissa(t: float) -> int | None:
    """The m in 1..9 with t the double nearest m 10^p for some p, or None."""
    p = C.decade(Fraction(t))
    for q in (p - 1, p, p + 1):
        m = round(Fraction(t) / C.pow10(q))
        if 1 <= m <= 9 and nearest(m * C.pow10(q)) == t:
            return m
    return None


@SLOW
@given(log_scales(), COUNT)
def test_log_ticks_are_mantissa_ticks_within_the_count_or_the_linear_ticks(s: C.Scale, c: int) -> None:
    lo, hi = sorted(s.domain)
    assume(lo != hi)
    ticks = s.ticks(c)
    if ticks == C.linear_ticks(lo, hi, c):
        return
    assert all(_mantissa(t) is not None for t in ticks) and len(ticks) <= max(c, 2)


def d3_ticks(start: float, stop: float, count: int) -> list[float]:
    """d3-array 3.2.4's ticks for start < stop [recalled: src/ticks.js], in doubles."""
    e10, e5, e2 = math.sqrt(50), math.sqrt(10), math.sqrt(2)

    def js_round(x: float) -> int:
        return math.floor(x + 0.5)

    def spec(count: float) -> tuple[int, int, float]:
        step = (stop - start) / max(0, count)
        power = math.floor(math.log10(step))
        error = step / 10.0**power
        factor = 10 if error >= e10 else 5 if error >= e5 else 2 if error >= e2 else 1
        if power < 0:
            inc = 10.0**-power / factor
            i1, i2 = js_round(start * inc), js_round(stop * inc)
            i1 += i1 / inc < start
            i2 -= i2 / inc > stop
            inc = -inc
        else:
            inc = 10.0**power * factor
            i1, i2 = js_round(start / inc), js_round(stop / inc)
            i1 += i1 * inc < start
            i2 -= i2 * inc > stop
        if i2 < i1 and 0.5 <= count < 2:
            return spec(count * 2)
        return i1, i2, inc

    i1, i2, inc = spec(count)
    return [(i1 + i) / -inc if inc < 0 else (i1 + i) * inc for i in range(i2 - i1 + 1)]


@settings(deadline=None, max_examples=500)
@given(st.integers(-10**6, 10**6), st.integers(-10**6, 10**6), st.sampled_from([1, 10, 100, 1000]),
       st.integers(1, 60))
def test_linear_ticks_are_d3s_on_ordinary_domains(a: int, b: int, scale: int, c: int) -> None:
    assume(a != b)
    lo, hi = sorted((a / scale, b / scale))
    assert C.linear_scale((lo, hi), (0, 1)).ticks(c) == [t + 0.0 for t in d3_ticks(lo, hi, c)]
