"""The stats twin against docs/ARCHITECTURE.md 5.16: fresh goldens, every rule and example, the error cases,
CPython's statistics and math.fsum, NumPy, and the error bound of the TypeScript's Sum2 computation as 5.16
describes it (ported here from the text, not from the TypeScript)."""

import json
import math
import statistics
from fractions import Fraction

import mpmath
import numpy as np
import pytest
from hypothesis import assume, given, settings, strategies as st
from numpy.lib import _function_base_impl as numpy_impl

from zqverify import stats as S

U, LEAST, MAX, BIG = S.U, S.LEAST, S.MAX, S.BIG
SLOW = settings(deadline=None, max_examples=300)

FINITE = st.floats(allow_nan=False, allow_infinity=False)
MODERATE = st.floats(min_value=-1e150, max_value=1e150, allow_nan=False)


@st.composite
def clustered(draw: st.DrawFn) -> list[float]:
    """Values a few ulps or a small relative step apart around one base: the cancellation cases."""
    base = draw(st.floats(min_value=1e-300, max_value=1e300) | st.floats(min_value=-1e300, max_value=-1e-300))
    step = draw(st.sampled_from([math.ulp(base), abs(base) * 2.0**-30, abs(base) * 2.0**-10]))
    ks = draw(st.lists(st.integers(-40, 40), min_size=1, max_size=25))
    return [base + k * step for k in ks]


DATA = st.lists(FINITE, min_size=1, max_size=25) | clustered() | st.lists(MODERATE, min_size=1, max_size=40)


def units(xs: list[float]) -> float:
    """5.16's quantile unit, 1.01 max(uM, 2^-1074)."""
    return 1.01 * max(U * max(map(abs, xs)), LEAST)


def raises(f, *args) -> bool:
    try:
        f(*args)
    except S.RangeError:
        return True
    return False


def clamped_fmean(xs: list[float]) -> float:
    m = statistics.fmean(xs)
    return min(max(m, min(xs)), max(xs))


# --- goldens -------------------------------------------------------------------------------------------------


def test_the_committed_goldens_are_fresh() -> None:
    assert S.GOLDEN.read_text(encoding="utf-8") == S.render()


def test_every_golden_line_reads_back_as_the_case_it_was_written_from() -> None:
    lines = [json.loads(line) for line in S.GOLDEN.read_text(encoding="utf-8").splitlines()]
    assert lines == S.goldens()


def test_the_goldens_reach_every_null_and_both_quartile_conventions() -> None:
    gs = S.goldens()
    assert len(gs) > 300
    assert any(g["sum"] is None for g in gs) and any(g["mean"] is None for g in gs)
    assert any(g["variance"][1] is None for g in gs) and any(g["sd"][0] is None and len(g["xs"]) > 1 for g in gs)
    assert any(g["median"] is None for g in gs) and any(None in g["linear"] for g in gs)
    assert any(g["quartiles"][0] is None and len(g["xs"]) >= 2 for g in gs)
    assert {len(g["xs"]) for g in gs} >= {1, 2, 3, 4, 10, 40}
    differ = [g for g in gs if g["quartiles"][0] and g["quartiles"][1] and g["quartiles"][0] != g["quartiles"][1]]
    assert len(differ) > 100


def test_golden_sums_and_means_are_fsum_and_the_clamped_fmean() -> None:
    for g in S.goldens():
        xs = g["xs"]
        try:
            fsum = math.fsum(xs)
        except OverflowError:
            assert g["sum"] is None and g["mean"] is None
            continue
        assert g["sum"] == fsum and math.copysign(1, g["sum"]) == math.copysign(1, fsum)
        assert g["mean"] == clamped_fmean(xs)


def test_golden_variances_and_deviations_are_statistics_where_it_gives_them() -> None:
    for g in S.goldens():
        xs = g["xs"]
        for got, f in zip(g["variance"] + g["sd"], (statistics.variance, statistics.pvariance,
                                                    statistics.stdev, statistics.pstdev)):
            try:
                want = f(xs)
            except (statistics.StatisticsError, OverflowError):
                assert got is None
                continue
            assert got == want


def test_golden_quartiles_are_statistics_quantiles_and_null_as_a_whole() -> None:
    for g in S.goldens():
        xs = g["xs"]
        for got, method, least in zip(g["quartiles"], ("inclusive", "exclusive"), (2, 3)):
            if len(xs) < least:
                assert got is None
                continue
            want = statistics.quantiles(xs, n=4, method=method)
            assert got == (want if all(map(math.isfinite, want)) else None)


# --- exact rounding ------------------------------------------------------------------------------------------


def _even(x: float) -> bool:
    """Whether x's last significand bit, on its binade's grid or the subnormal grid, is 0."""
    e = max(math.frexp(x)[1] - 53, -1074)
    return (Fraction(x) / Fraction(2) ** e).numerator % 2 == 0


@given(st.fractions(max_denominator=2**1100) | st.builds(lambda m, e: Fraction(2 * m + 1, 2) * Fraction(2) ** e,
                                                          st.integers(2**52, 2**53), st.integers(-1130, 960)))
def test_nearest_is_closer_than_either_neighbour_and_ties_go_to_even(q: Fraction) -> None:
    r = S.nearest(q)
    assume(math.isfinite(r))
    gap = abs(q - Fraction(r))
    for side in (math.inf, -math.inf):
        other = math.nextafter(r, side)
        if math.isfinite(other):
            assert gap <= abs(q - Fraction(other))
            if gap == abs(q - Fraction(other)) and gap:
                assert _even(r)


def test_nearest_at_the_ends_of_the_doubles() -> None:
    assert S.nearest(Fraction(2**1024 - 2**970)) == math.inf  # a tie between MAX and 2^1024 goes to even
    assert S.nearest(Fraction(2**1024 - 2**970 - 1)) == MAX
    assert S.nearest(-Fraction(2**1024)) == -math.inf
    assert S.nearest(Fraction(1, 2**1075)) == 0.0  # half the least subnormal: the tie goes to 0
    assert S.nearest(Fraction(3, 2**1075)) == 2 * LEAST
    assert S.nearest(Fraction(1, 2**1075) + Fraction(1, 2**1200)) == LEAST


@given(st.fractions(min_value=0, max_denominator=2**200) | st.builds(lambda m, e: Fraction(m) * Fraction(2) ** e,
                                                                      st.integers(1, 2**60), st.integers(-2200, 1900)))
def test_sqrt_nearest_matches_mpmath_at_200_digits(q: Fraction) -> None:
    with mpmath.workdps(200):
        root = mpmath.sqrt(mpmath.mpf(q.numerator) / q.denominator)
        man, exp = root.man_exp
        exact = Fraction(man) * Fraction(2) ** exp if root else Fraction(0)
    assert S.sqrt_nearest(q) == S.nearest(exact)


def test_sqrt_nearest_of_squares_is_exact() -> None:
    for x in (0.0, 1.0, 3.0, 2.0**-537, 1e-160, 1e154, 1.7e308, LEAST):
        assert S.sqrt_nearest(Fraction(x) ** 2) == x


# --- sum and mean --------------------------------------------------------------------------------------------


def test_sum_examples() -> None:
    assert S.sum([]) == 0.0
    assert S.sum([1.0, 2.0**-53]) == 1.0 and S.sum([1.0, 2.0**-53, 2.0**-106]) == 1.0 + 2.0**-52
    assert math.copysign(1, S.sum([-0.0])) == 1.0  # fsum's value
    assert S.sum([1e16, 1.0, -1e16]) == 1.0
    assert raises(S.sum, [BIG, BIG, -BIG]) and S.nearest(Fraction(BIG)) == BIG  # throws, though exactly 1.7e308


@SLOW
@given(st.lists(FINITE, max_size=30) | clustered())
def test_sum_is_fsum_and_throws_where_fsum_overflows(xs: list[float]) -> None:
    try:
        want = math.fsum(xs)
    except OverflowError:
        assert raises(S.sum, xs)
        return
    assert S.sum(xs) == want
    assert S.sum(xs) == S.nearest(sum(map(Fraction, xs), Fraction(0)))


def test_mean_examples() -> None:
    assert S.mean([0.1, 0.1, 0.1]) == 0.1 and statistics.fmean([0.1, 0.1, 0.1]) == 0.10000000000000002
    spec = [BIG, BIG, -BIG, -BIG, 1e-320]
    assert S.nearest(sum(map(Fraction, spec), Fraction(0)) / 5) == 2e-321 and raises(S.mean, spec)


@SLOW
@given(DATA)
def test_mean_is_the_clamped_fmean_and_throws_where_the_sum_does(xs: list[float]) -> None:
    try:
        want = clamped_fmean(xs)
    except OverflowError:
        assert raises(S.mean, xs)
        return
    assert S.mean(xs) == want and min(xs) <= S.mean(xs) <= max(xs)


# --- variance and sd -----------------------------------------------------------------------------------------


def test_variance_examples() -> None:
    assert S.variance([4.0], "population") == 0.0 and S.sd([4.0], "population") == 0.0
    assert S.variance([2.5] * 5, "sample") == 0.0
    assert S.variance([1e154, -1e154], "population") == 1e308 and raises(S.variance, [1e154, -1e154], "sample")
    assert S.sd([-BIG, BIG], "population") == BIG and raises(S.variance, [-BIG, BIG], "population")
    assert raises(S.sd, [-BIG, BIG], "sample")
    assert S.variance([1.0, 2.0, 3.0, 4.0], "sample") == 5 / 3
    assert S.variance([1.0, 2.0, 3.0, 4.0], "population") == 1.25


@SLOW
@given(DATA)
def test_variance_and_sd_are_the_exact_values_rounded_once_as_statistics_gives_them(xs: list[float]) -> None:
    for twin, library, least in ((S.variance, statistics.variance, 2), (S.variance, statistics.pvariance, 1),
                                 (S.sd, statistics.stdev, 2), (S.sd, statistics.pstdev, 1)):
        kind = "sample" if least == 2 else "population"
        if len(xs) < least:
            assert raises(twin, xs, kind)
            continue
        try:
            want = library(xs)
        except OverflowError:
            assert raises(twin, xs, kind)
            continue
        assert twin(xs, kind) == want


def ts_variance(xs: list[float], kind: str) -> tuple[float, float]:
    """5.16's steps 1 to 4 of the TypeScript's computation, every operation a double; may return inf."""
    n = len(xs)
    d = n - 1 if kind == "sample" else n
    m_abs = max(map(abs, xs))
    c = 2.0**-600 if m_abs > 2.0**400 else 2.0**600 if m_abs < 2.0**-400 else 1.0

    def sum2(values: list[float]) -> float:
        s = e = 0.0
        for x in values:
            t = s + x
            z = t - s
            e = e + ((s - (t - z)) + (x - z))
            s = t
        return s + e

    scaled = [c * x for x in xs]
    m = sum2(scaled) / n
    ds = [x - m for x in scaled]
    s1, s2 = sum2(ds), sum2([x * x for x in ds])
    ss = max(s2 - s1 * s1 / n, 0.0)
    v = ss / d
    return v / c / c, math.sqrt(v) / c


def _mp(q: Fraction) -> mpmath.mpf:
    return mpmath.mpf(q.numerator) / q.denominator


def sum2_within_bound(xs: list[float], kind: str) -> None:
    n = len(xs)
    d = n - 1 if kind == "sample" else n
    v, s = ts_variance(xs, kind)
    with mpmath.workdps(40):
        exact = _mp(S.exact_variance(xs, kind))
        e = 0 if all(x == xs[0] for x in xs) else 2 * mpmath.mpf(U) * max(map(abs, xs))
        var_bound = mpmath.mpf(1.01) * (7 * U * exact + 7 * U * n * e * e / d) + LEAST
        sigma = mpmath.sqrt(exact)
        r = e * mpmath.sqrt(7 * U * n / mpmath.mpf(d))
        sd_bound = mpmath.mpf(1.01) * (5 * U * sigma + (r if sigma == 0 else min(r, r * r / sigma))) + LEAST
        for got, want, bound in ((v, exact, var_bound), (s, sigma, sd_bound)):
            if math.isinf(got):
                assert want + bound >= MAX  # "may throw where the exact value rounds to MAX_VALUE"
            else:
                assert abs(mpmath.mpf(got) - want) <= bound


@settings(deadline=None, max_examples=600)
@given(DATA, st.sampled_from(["sample", "population"]))
def test_the_sum2_computation_meets_5_16s_error_bound(xs: list[float], kind: str) -> None:
    assume(len(xs) >= (2 if kind == "sample" else 1))
    sum2_within_bound(xs, kind)


def test_the_sum2_computation_on_cancellation_both_scalings_and_every_golden() -> None:
    for xs in ([1e9 + 0.1, 1e9 + 0.2, 1e9 + 0.3], [1e-150, 2e-150, 3e-150], [1e130, 2e130, 4e130],
               [1.0 + k * 2.0**-52 for k in range(20)], [1e16, 1.0, -1e16], *S.data_sets()):
        for kind in ("sample", "population"):
            if len(xs) >= (2 if kind == "sample" else 1):
                sum2_within_bound(xs, kind)


# --- quantiles -----------------------------------------------------------------------------------------------


def _sign(x: float) -> float:
    return math.copysign(1.0, x)


def test_the_sort_puts_minus_zero_first_and_the_ends_keep_their_sign() -> None:
    for method in ("inclusive", "gcse"):
        assert _sign(S.quantile([0.0, -0.0], 0.0, method)) == -1.0
        assert _sign(S.quantile([0.0, -0.0], 1.0, method)) == 1.0
        assert _sign(S.quantile([-1.0, -0.0], 1.0, method)) == -1.0
    assert _sign(S.quantile([1.0, 2.0, -0.0], 0.25, "gcse")) == -1.0  # h = 4 * 0.25 - 1 = 0, the first value


def test_gcse_takes_the_end_where_statistics_exclusive_extrapolates() -> None:
    assert S.quantile([1.0, 2.0], 0.25, "gcse") == 1.0
    assert statistics.quantiles([1.0, 2.0], n=4, method="exclusive")[0] == 0.75  # [measured: CPython 3.12.15]
    assert S.quantile([1.0, 2.0], 0.75, "gcse") == 2.0


def test_c5_ten_values_the_methods_agree_on_the_median_and_differ_on_the_quartiles() -> None:
    xs = [2.0, 4.0, 4.0, 5.0, 7.0, 8.0, 9.0, 11.0, 12.0, 15.0]
    assert S.quartiles(xs, "inclusive") == [4.25, 7.5, 10.5]  # positions 1 + 9p, 1-based
    assert S.quartiles(xs, "gcse") == [4.0, 7.5, 11.25]  # positions 11p, 1-based
    assert S.quartiles(xs, "inclusive") == statistics.quantiles(xs, n=4, method="inclusive")
    assert S.quartiles(xs, "gcse") == statistics.quantiles(xs, n=4, method="exclusive")
    assert S.median(xs) == statistics.median(xs) == 7.5


def test_positions_round_as_5_16_says() -> None:
    # gcse rounds (n + 1) p and then the difference: n = 9, p = 0.1 gives 10 * 0.1 - 1 = 0 in doubles, the first.
    xs = [float(k) for k in range(9)]
    assert ((9 + 1) * 0.1) - 1 == 0.0 and S.quantile(xs, 0.1, "gcse") == 0.0
    assert S.quantile(xs, 0.37, "inclusive") == S.lerp(2.0, 3.0, 8 * 0.37 - 2)


@pytest.mark.parametrize("p", [-0.1, 1.1, math.nan, math.inf, -math.inf, -1e-300, 1 + 2**-52])
def test_p_outside_0_1_throws(p: float) -> None:
    for method in ("inclusive", "gcse"):
        assert raises(S.quantile, [1.0, 2.0], p, method)


def test_p_at_the_ends_and_minus_zero_are_inside() -> None:
    assert S.quantile([3.0, 1.0], -0.0, "inclusive") == 1.0 and S.quantile([3.0, 1.0], 1, "gcse") == 3.0


@pytest.mark.parametrize("xs", [[], [math.nan], [1.0, math.inf], [-math.inf, 2.0], [1.0, math.nan, 3.0]])
def test_too_few_or_non_finite_values_throw(xs: list[float]) -> None:
    for f in (S.mean, S.median, lambda v: S.quantile(v, 0.5, "inclusive"), lambda v: S.quartiles(v, "gcse"),
              lambda v: S.variance(v, "population"), lambda v: S.sd(v, "population")):
        assert raises(f, xs)
    assert raises(S.sum, xs) == bool(xs)


def test_sample_statistics_need_two_values() -> None:
    assert raises(S.variance, [1.0], "sample") and raises(S.sd, [1.0], "sample")


def test_unknown_kind_or_method_is_a_type_error() -> None:
    with pytest.raises(TypeError):
        S.variance([1.0, 2.0], "both")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        S.quantile([1.0, 2.0], 0.5, "exclusive")  # type: ignore[arg-type]


@SLOW
@given(DATA, st.sampled_from(S.PS) | st.floats(0, 1))
def test_inclusive_is_numpy_linear_wherever_numpys_b_minus_a_stays_finite(xs: list[float], p: float) -> None:
    want = S.numpy_linear(xs, p)
    if want is not None:
        assert S.quantile(xs, p, "inclusive") == want  # == treats the zeros as equal: their signs are aside


@SLOW
@given(DATA, st.sampled_from(S.PS) | st.floats(0, 1))
def test_both_methods_lie_within_5_16s_units_of_the_exact_quantile(xs: list[float], p: float) -> None:
    n, unit, quartile = len(xs), units(xs), (4 * p).is_integer()
    for method, elsewhere in (("inclusive", 2 * n + 2), ("gcse", 4 * n + 6)):
        got, want = S.quantile(xs, p, method), S.exact_quantile(xs, p, method)
        assert abs(Fraction(got) - Fraction(want)) <= (4 if quartile else elsewhere) * unit


@SLOW
@given(DATA)
def test_quartiles_and_median_against_statistics(xs: list[float]) -> None:
    for method in ("inclusive", "gcse"):
        assert S.quartiles(xs, method) == [S.quantile(xs, p, method) for p in S.QUARTILE_PS]
    assert S.median(xs) == S.quantile(xs, 0.5, "inclusive")
    unit = units(xs)
    med = statistics.median(xs)
    if math.isfinite(med):
        assert abs(S.median(xs) - med) <= 3 * unit
    for method, theirs, least in (("inclusive", "inclusive", 2), ("gcse", "exclusive", 3)):
        if len(xs) >= least:
            want = statistics.quantiles(xs, n=4, method=theirs)
            if all(map(math.isfinite, want)):
                assert all(abs(a - b) <= 4 * unit for a, b in zip(S.quartiles(xs, method), want))


# --- lerp ----------------------------------------------------------------------------------------------------


@given(FINITE, FINITE)
def test_lerp_gives_its_ends_exactly(a: float, b: float) -> None:
    assert S.lerp(a, b, 0.0) == a and S.lerp(a, b, 1.0) == b


@given(FINITE, FINITE, st.floats(-10, 10))
def test_lerp_is_numpys_lerp_where_b_minus_a_is_finite(a: float, b: float, t: float) -> None:
    assume(math.isfinite(b - a))
    with np.errstate(over="ignore", invalid="ignore"):
        want = float(numpy_impl._lerp(np.float64(a), np.float64(b), np.float64(t)))
    if math.isfinite(want):
        assert S.lerp(a, b, t) == want


def test_lerp_examples() -> None:
    assert S.lerp(0.0, 1.0, 2.0) == 2.0 and S.lerp(0.0, 1.0, -1.0) == -1.0  # extrapolates
    assert S.lerp(-BIG, BIG, 0.5) == 0.0  # b - a overflows; the halves give 0
    assert S.lerp(-MAX, MAX, 0.75) == MAX / 2 and S.lerp(-MAX, MAX, 0.0) == -MAX
    assert S.lerp(0.0, MAX, 2.0) == math.inf and S.lerp(MAX, 0.0, 2.0) == -MAX
    assert S.lerp(MAX / 2, MAX, 1.5) == math.inf


@given(FINITE, FINITE, st.floats(-1e6, 1e6))
def test_lerp_is_infinite_only_where_the_interpolant_leaves_the_doubles(a: float, b: float, t: float) -> None:
    got = S.lerp(a, b, t)
    exact = Fraction(a) + (Fraction(b) - Fraction(a)) * Fraction(t)
    # Fractions throughout: a float operand would turn the Fraction into a float, which overflows.
    slack = 4 * Fraction(U) * (abs(Fraction(a)) + abs(Fraction(b))) * max(1, abs(Fraction(t))) + Fraction(LEAST)
    assert not math.isnan(got)
    if math.isinf(got):
        assert abs(exact) + slack > Fraction(MAX) and math.copysign(1, got) == (1 if exact > 0 else -1)
    elif abs(exact) + slack <= Fraction(MAX):
        assert abs(Fraction(got) - exact) <= slack


@pytest.mark.parametrize("args", [(math.nan, 1.0, 0.5), (0.0, math.inf, 0.5), (-math.inf, 0.0, 0.5),
                                  (0.0, 1.0, math.nan), (0.0, 1.0, math.inf), (0.0, 1.0, -math.inf)])
def test_lerp_refuses_non_finite_arguments(args: tuple[float, float, float]) -> None:
    assert raises(S.lerp, *args)


@SLOW
@given(st.lists(MODERATE, min_size=2, max_size=30), st.floats(0, 1))
def test_nothing_else_throws(xs: list[float], p: float) -> None:
    S.sum(xs), S.mean(xs), S.median(xs)
    for kind in ("sample", "population"):
        S.variance(xs, kind), S.sd(xs, kind)
    for method in ("inclusive", "gcse"):
        S.quantile(xs, p, method), S.quartiles(xs, method)
