"""The stats goldens are fresh, and the twin's exact definitions agree with statistics computed on Fractions."""

import statistics
import sys
from fractions import Fraction

from hypothesis import given, strategies as st

from zqverify import stats

values = st.lists(st.floats(-1e6, 1e6, allow_nan=False), min_size=1, max_size=30)


def test_the_committed_goldens_are_fresh() -> None:
    assert stats.GOLDEN.read_text(encoding="utf-8") == stats.render()


def test_the_conventions_differ_on_quartiles_for_ten_values() -> None:
    xs = stats.FIXED[-1]
    assert [stats.exact_quantile(xs, p, "inclusive") for p in (0.25, 0.5, 0.75)] == [9.0, 16.5, 21.75]
    assert [stats.exact_quantile(xs, p, "gcse") for p in (0.25, 0.5, 0.75)] == [7.75, 16.5, 24.0]


def test_statistics_extrapolates_where_gcse_takes_the_end_value() -> None:
    assert statistics.quantiles([1.0, 2.0], n=4, method="exclusive")[0] == 0.75
    assert stats.exact_quantile([1.0, 2.0], 0.25, "gcse") == 1.0
    assert stats.quartiles([1.0, 2.0], "exclusive") is None


@given(values)
def test_exact_quartiles_are_statistics_on_fractions(xs: list[float]) -> None:
    """statistics.quantiles is exact on Fractions, so it must equal the twin's definition after one rounding."""
    exact = [Fraction(x) for x in xs]
    for method, ours in (("inclusive", "inclusive"), ("exclusive", "gcse")):
        if len(xs) >= (2 if method == "inclusive" else 3):
            want = [float(q) for q in statistics.quantiles(exact, n=4, method=method)]
            assert [stats.exact_quantile(xs, p, ours) for p in (0.25, 0.5, 0.75)] == want


@given(values, st.floats(0, 1), st.floats(0, 1))
def test_exact_quantiles_are_monotone_and_inside(xs: list[float], p: float, q: float) -> None:
    for method in ("inclusive", "gcse"):
        a, b = (stats.exact_quantile(xs, v, method) for v in sorted((p, q)))
        assert min(xs) <= a <= b <= max(xs)


def test_overflows_and_short_data_are_null() -> None:
    case = stats.case([1e300, -1e300])
    assert case["variance"] == [None, None] and case["sd"] == [1.4142135623730952e300, 1e300]
    assert stats.case([3.0])["variance"] == [None, 0.0]
    edge = stats.case([-1.7e308, 1.7e308])
    assert edge["sd"] == [None, 1.7e308] and edge["linear"][:7] == [None] * 7 and edge["quartiles"] == [None, None]
    assert stats.case([1.7e308, 1.7e308])["median"] is None


def test_the_edge_witnesses_round_to_max_value() -> None:
    """statistics rounds these to MAX_VALUE, where the TypeScript's own rounding may overflow."""
    variance, deviation = stats.FIXED[-3], stats.FIXED[-2]
    assert stats.case(variance)["variance"][0] == sys.float_info.max
    deviation_case = stats.case(deviation)
    assert deviation_case["sd"][0] == sys.float_info.max and deviation_case["variance"] == [None, None]
