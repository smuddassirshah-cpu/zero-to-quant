"""The scale goldens are fresh, and the twin's ticks keep the properties the specification states."""

from hypothesis import given, strategies as st

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
