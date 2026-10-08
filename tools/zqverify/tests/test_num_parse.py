"""The twin reads CONTENT-FORMAT.md 7.2's examples as the specification says, and its goldens are fresh."""

import pytest
from hypothesis import given, strategies as st

from zqverify import num_parse


def test_the_committed_goldens_are_fresh() -> None:
    assert num_parse.GOLDEN.read_text(encoding="utf-8") == num_parse.render()


@pytest.mark.parametrize(
    ("text", "form", "value"),
    [
        ("11", "integer", "11"),
        ("−3", "integer", "-3"),
        ("1,000", "integer", "1000"),
        (".25", "decimal", "1/4"),
        ("305.", "decimal", "305"),
        ("-10 / 109", "fraction", "-10/109"),
        ("2 1/3", "mixed", "7/3"),
        ("66.7 %", "percent", "667/10"),
        ("3.2 x 10^5", "standard-form", "320000"),
        ("3.2×10^-3", "standard-form", "2/625"),
    ],
)
def test_reads_the_forms(text: str, form: str, value: str) -> None:
    assert num_parse.parse(text, []) | {"places": 0, "figures": 0} == {
        "ok": True, "form": form, "value": value, "unit": None, "places": 0, "figures": 0,
    }


@pytest.mark.parametrize(
    ("text", "reason"),
    [("", "empty"), ("0,5", "decimal-comma"), ("0,500", "decimal-comma"), ("1/0", "zero-denominator"),
     ("1e1001", "out-of-range"), ("+5", "syntax"), ("2 4/3", "syntax"), ("1" * 201, "too-long")],
)
def test_fails_with_the_nudge_reason(text: str, reason: str) -> None:
    assert num_parse.parse(text, []) == {"ok": False, "reason": reason}


def test_units_places_and_figures() -> None:
    assert num_parse.parse("£12.50", ["£"]) == {
        "ok": True, "form": "decimal", "value": "25/2", "unit": "£", "places": 2, "figures": 4,
    }
    assert num_parse.parse("0.0350", [])["figures"] == 3


@given(st.integers(-(10**30), 10**30))
def test_grouped_integers_read_back(n: int) -> None:
    assert num_parse.parse(f"{n:,}", [])["value"] == str(n)


@given(st.text(max_size=30))
def test_never_raises(text: str) -> None:
    assert num_parse.parse(text, ["£", "bp"])["ok"] in (True, False)
