"""The num-parse goldens are fresh and read as recorded, and the twin meets each rule of CONTENT-FORMAT.md 7.2:
every example the section gives, the failure reasons in its order, the bounds, and properties over random input.
"~" in a text stands for a narrow space, and a case with one runs once for each of the five."""

from __future__ import annotations

import dataclasses
import json
import string
from fractions import Fraction

import pytest
from hypothesis import assume, example, given, strategies as st

from zqverify import num_parse, rational
from zqverify.num_parse import FORMS, NARROW, REASONS, Failure, Number, code_units, normalise, out, parse

TOO_LONG = num_parse.MAX_LENGTH + 1
LINES = [json.loads(line) for line in num_parse.GOLDEN.read_text(encoding="utf-8").splitlines()]
DIGITS = "0123456789"


def number(text: str, units: tuple[str, ...] = ()) -> Number:
    result = parse(text, units)
    assert isinstance(result, Number), (text, result)
    return result


def reason(text: str, units: tuple[str, ...] = ()) -> str:
    result = parse(text, units)
    assert isinstance(result, Failure), (text, result)
    return result.reason


def spaced(text: str) -> list[str]:
    """text once for each narrow space, where "~" stands for one."""
    return [text.replace("~", s) for s in NARROW] if "~" in text else [text]


def each_spacing(cases: dict[str, object]) -> list[tuple[str, object]]:
    return [(typed, expected) for text, expected in cases.items() for typed in spaced(text)]


# The golden file.


def test_the_committed_goldens_are_fresh() -> None:
    assert num_parse.GOLDEN.read_text(encoding="utf-8") == num_parse.render()


def test_every_golden_line_reads_as_recorded() -> None:
    assert [g for g in LINES if out(parse(g["in"], g["units"])) != g["out"]] == []


def test_every_golden_line_has_the_fields_7_2_names() -> None:
    for g in LINES:
        assert list(g) == ["in", "units", "out"]
        result = g["out"]
        if not result["ok"]:
            assert list(result) == ["ok", "reason"] and result["reason"] in REASONS
            continue
        assert list(result) == ["ok", "form", "value", "places", "figures", "typed", "unit"]
        assert result["form"] in FORMS and rational.spell(rational.parse(result["value"])) == result["value"]
        assert result["unit"] is None or result["unit"] in g["units"]
        typed = result["typed"]
        assert (typed is None) == (result["form"] not in ("fraction", "mixed"))
        assert typed is None or (list(typed) == ["whole", "n", "d"] and all(v == str(int(v)) for v in typed.values()))


def test_the_goldens_reach_every_form_reason_and_narrow_space() -> None:
    assert {g["out"]["form"] for g in LINES if g["out"]["ok"]} == set(FORMS)
    assert {g["out"]["reason"] for g in LINES if not g["out"]["ok"]} == set(REASONS)
    assert all(any(s in g["in"] for g in LINES) for s in NARROW)
    assert any(g["out"]["ok"] and g["out"]["unit"] for g in LINES)
    assert len(LINES) == len({(g["in"], tuple(g["units"])) for g in LINES}) >= 1500


# Rule 1.


def test_rule_1_the_length_counts_utf16_code_units_and_comes_first() -> None:
    assert number("1" * 200).value == int("1" * 200)
    assert number(" " * 199 + "7").value == 7
    for text in ("1" * 201, " " * 201, "x" * 201, "\U0001f600" * 100 + "1", "1" * 199 + "\U0001f600"):
        assert reason(text) == "too-long"
    assert reason("\U0001f600" * 100) == "syntax"
    for s in NARROW:
        assert reason(f"1{s}000/" + " " * 194) == "syntax"
        assert reason(f"1{s}000/" + " " * 195) == "too-long"
    assert len(code_units("\U0001f600")) == 2 and code_units("\U0001f600") == chr(0xD83D) + chr(0xDE00)


# Rule 2.


def test_rule_2_1_lists_ten_dashes_and_minuses() -> None:
    expected = {*map(chr, range(0x2010, 0x2016)), "\u2212", "\ufe58", "\ufe63", "\uff0d"}
    assert num_parse.DASHES == expected and len(expected) == 10


@pytest.mark.parametrize("dash", sorted(num_parse.DASHES))
def test_rule_2_1_each_dash_is_a_minus(dash: str) -> None:
    assert number(f"{dash}5").value == -5
    assert number(f"{dash} 5").value == -5
    assert number(f"1e{dash}3").value == Fraction(1, 1000)
    assert reason(f"5{dash}3") == "syntax"


def test_rule_2_1_other_dashes_are_not_minuses() -> None:
    for dash in ("\u00ad", "\u2043", "\u2e3a", "\u30fc", "\u02d7"):
        assert reason(f"{dash}5") == "syntax"


NORMALISED = {
    "1~000": "1000",
    "1~234~567": "1234567",
    "12~345.5": "12345.5",
    "1~000,5": "1000,5",
    "3/1~000": "3/1000",
    "1~000~0000": "1000 0000",
    "0~500": "0 500",
    "1~2345": "1 2345",
    "0.123~456": "0.123 456",
    "3.2e1~000": "3.2e1 000",
    "1e-1~000": "1e-1 000",
    "1e\u22121~000": "1e-1 000",
    "1E+1~000": "1E+1 000",
    "5x10^1~000": "5x10^1 000",
    "2~1/3": "2 1/3",
    "1~000~1/2": "1000 1/2",
    "1~000~000.5": "1000000.5",
    "-1~000": "-1000",
    "\u22121~000": "-1000",
    "£1~000": "£1000",
    "1234~567": "1234 567",
    ".1~000": ".1 000",
    ",1~000": ",1 000",
    "1/2~000": "1/2000",
    "1~000~1~000": "1000 1000",
    "1~0001~000": "1 0001 000",
    "1~000,000": "1000,000",
    "1,000~000": "1,000 000",
    "~5~": "5",
}


@pytest.mark.parametrize(("text", "expected"), each_spacing(NORMALISED))
def test_rule_2_2_removes_the_narrow_spaces_of_each_grouping_run(text: str, expected: str) -> None:
    assert normalise(code_units(text)) == expected


GROUPED_BEFORE_A_SLASH = [
    "2~125/250",
    "12~345/7",
    "1~000/0",
    "1~000 /3",
    "1~000\t/3",
    "1~000~~/3",
    "1~000~/~3",
    "1~000 \t~/3",
    "1~000/2~000",
    "1~000/2,5",
    "3 1~000/7",
]


@pytest.mark.parametrize("text", [t for text in GROUPED_BEFORE_A_SLASH for t in spaced(text)])
def test_rule_2_2_a_grouping_run_before_a_slash_fails_as_syntax_at_once(text: str) -> None:
    assert normalise(code_units(text)) is None
    assert reason(text) == "syntax"


def test_rule_2_2_the_slash_check_reads_only_grouping_runs() -> None:
    for s in NARROW:
        assert reason(f"1{s}000/s", ("s",)) == "syntax"
        assert number(f"2{s}1/3").typed == (2, 1, 3)
        assert number(f"1{s}000{s}1/2").value == Fraction(2001, 2)
        assert number(f"1{s}000").value == 1000
        assert number(f"3/1{s}000").value == Fraction(3, 1000)
        assert reason(f"1{s}000,5") == "decimal-comma"
        assert reason(f"0{s}500") == reason(f"1{s}2345") == reason(f"1{s}000{s}0000") == "syntax"
    assert reason("1 000/3") == "syntax"  # an ordinary space groups nothing; the body is not a number


def test_rule_2_3_to_2_6_on_their_own() -> None:
    assert normalise("2\u00a01/3") == "2 1/3"
    assert number("2\u00a01/3").form == "mixed"
    assert normalise("3.2\u00d710^5") == normalise("3.2\u00b710^5") == normalise("3.2\u22c510^5") == "3.2*10^5"
    assert normalise("2 \t \t1/3") == "2 1/3" and normalise("1 \t/ \t2") == "1 / 2"
    assert normalise("\r\n\v\f\t 5 \t\f\v\n\r") == "5"
    for kept in ("\u30005", "\ufeff5", "5\u2028", "\u00855", "1\n000", "2 \n 1/3"):
        assert normalise(kept) == kept and reason(kept) == "syntax"
    assert reason("2\u00d73") == "syntax"


# Rules 3 and 4.


def test_rule_3_nothing_left_is_empty() -> None:
    for text in ("", " ", "\t\n\r\v\f", "\u00a0", "\u00a0 \u202f", "\u2007\u2009\u200a"):
        assert reason(text) == "empty"
    assert reason("\u3000") == "syntax"


def test_rule_4_one_sign_at_the_start_then_one_optional_space() -> None:
    pound = ("£",)
    for text in ("+-5", "++5", "-+5", "--5", "- -5", "5-", "-", "+", "- "):
        assert reason(text) == "syntax"
    assert reason("£-5", pound) == reason("£ -5", pound) == "syntax"
    assert number("+33.1%").value == Fraction(331, 10)
    assert number("\u2212 5").value == number("-  5").value == -5
    assert (number("-£5", pound).value, number("-£5", pound).unit) == (-5, "£")
    assert number("+£5", pound).value == 5 and number("- £ 5", pound).value == -5
    assert number("+ 5").value == 5


# Rule 5.


UNITS: list[tuple[str, tuple[str, ...], str, Fraction]] = [
    ("5 ms", ("s", "ms"), "ms", Fraction(5)),
    ("5ms", ("s", "ms"), "ms", Fraction(5)),
    ("5s", ("s", "ms"), "s", Fraction(5)),
    ("5 MS", ("ms",), "ms", Fraction(5)),
    ("Ms 5", ("ms",), "ms", Fraction(5)),
    ("ms5", ("m", "ms"), "ms", Fraction(5)),
    ("5kg", ("KG", "kg"), "KG", Fraction(5)),
    ("5kg", ("kg", "KG"), "kg", Fraction(5)),
    ("5 Kg", ("g", "kg"), "kg", Fraction(5)),
    ("£ 5", ("£",), "£", Fraction(5)),
    ("5 £", ("£",), "£", Fraction(5)),
    ("£  5", ("£",), "£", Fraction(5)),
    ("5s", ("", "s"), "s", Fraction(5)),
    ("25%", ("%",), "%", Fraction(25)),
    ("%25", ("%",), "%", Fraction(25)),
    ("1/4%", ("%",), "%", Fraction(1, 4)),
    ("1e3%", ("%",), "%", Fraction(1000)),
    ("£12.50", ("£",), "£", Fraction(25, 2)),
    ("-5 s", ("s",), "s", Fraction(-5)),
    ("11 Outcomes", ("outcomes",), "outcomes", Fraction(11)),
    ("250 bp", ("bp", "%"), "bp", Fraction(250)),
    ("2 1/3 s", ("s",), "s", Fraction(7, 3)),
    ("5x", ("x",), "x", Fraction(5)),
    ("12 BP", ("bp",), "bp", Fraction(12)),
    ("12 bp", ("BP",), "BP", Fraction(12)),
    ("5\u00df", ("\u00df",), "\u00df", Fraction(5)),
    ("5\u0130", ("\u0130",), "\u0130", Fraction(5)),
    ("5\u212a", ("\u212a",), "\u212a", Fraction(5)),
    ("5\ua7cb", ("\ua7cb",), "\ua7cb", Fraction(5)),
    ("5\U00010400", ("\U00010400",), "\U00010400", Fraction(5)),
    ("5 €", ("$", "€"), "€", Fraction(5)),
]


@pytest.mark.parametrize(("text", "units", "unit", "value"), UNITS)
def test_rule_5_a_listed_unit_longest_first_without_regard_to_case(
    text: str, units: tuple[str, ...], unit: str, value: Fraction
) -> None:
    result = number(text, units)
    assert (result.unit, result.value) == (unit, value)


def test_rule_5_one_unit_only_and_nothing_else_is_tried() -> None:
    assert reason("£5£", ("£",)) == reason("£5p", ("£", "p")) == reason("£25%", ("£",)) == "syntax"
    assert reason("5 s 1", ("s",)) == reason("£", ("£",)) == "syntax"
    assert reason("5SS", ("\u00df",)) == reason("5i", ("\u0130",)) == "syntax"
    assert reason("5 \u03c3\u03b1\u03c3", ("\u03a3\u0391\u03a3",)) == "syntax"
    assert number("5", ("", "s")).unit is None and number("5%", ("",)).form == "percent"
    assert number("12.5", ("£",)).unit is None
    assert number("5x10^3", ("x",)).form == number("5e3", ("e",)).form == "standard-form"
    assert number("25%", ("%",)).form == "integer" and number("2.5 %", ("bp", "%")).form == "decimal"


NO_ASCII_CASE_PAIR = [
    ("5\ua7cb", ("\u0264",)),
    ("5\u0264", ("\ua7cb",)),
    ("5k", ("\u212a",)),
    ("5\u212a", ("k",)),
    ("5\u212a", ("K",)),
    ("5\u03c3", ("\u03a3",)),
    ("5\u03a3", ("\u03c3",)),
    ("5\u03c9", ("\u03a9",)),
    ("5\u00e9", ("\u00c9",)),
    ("5\u0131", ("I",)),
    ("5\U00010428", ("\U00010400",)),
    ("5 \u03c3\u03b1\u03c2", ("\u03a3\u0391\u03a3",)),
]


@pytest.mark.parametrize(("text", "units"), NO_ASCII_CASE_PAIR)
def test_rule_5_no_case_pair_outside_ascii_matches(text: str, units: tuple[str, ...]) -> None:
    assert reason(text, units) == "syntax"


def test_rule_5_compares_code_units_so_a_lone_or_cut_surrogate_is_itself() -> None:
    assert reason("5\ud800") == reason("\udc005") == "syntax"
    assert number("5\ud800", ("\ud800",)).unit == "\ud800"
    assert number("\udc005", ("\udc00",)).unit == "\udc00"
    assert reason("5\U0001f600", ("\ude00",)) == reason("\U0001f6005", ("\ud83d",)) == "syntax"
    assert reason("5\ud83d", ("\U0001f600",)) == "syntax"
    assert number("5\U0001f600", ("\U0001f600",)).unit == "\U0001f600"


def test_rule_5_a_unit_longer_than_the_text_never_matches() -> None:
    """7.2 rule 5: the text lacks the unit's number of code units, so a shorter unit is tried."""
    assert number("5\u0130", ("5i\u0307", "\u0130")).unit == "\u0130"
    assert number("\u01305", ("i\u03075", "\u0130")).unit == "\u0130"
    assert reason("\u0130", ("i\u0307",)) == "syntax"


# Rule 6.


def test_rule_6_a_trailing_percent_without_a_unit() -> None:
    readings = {"25%": 25, "25 %": 25, "25  %": 25, "66.7 %": Fraction(667, 10), "-25%": -25, ".5%": Fraction(1, 2)}
    for text, value in readings.items():
        result = number(text)
        assert (result.form, result.value) == ("percent", value)
    assert (number("5.%").places, number("0%").figures, number("1,000%").value) == (0, 0, 1000)
    for text in ("25%%", "%", "% 25", "1e3%", "1e1001%", "1/0%", "2/3%", "1 1/2%"):
        assert reason(text) == "syntax"


# Rule 7.


DECIMAL_LIKE = {
    "11": ("integer", 11, 0, 2),
    "-3": ("integer", -3, 0, 1),
    "+5": ("integer", 5, 0, 1),
    "1,000": ("integer", 1000, 0, 4),
    "12,345,678": ("integer", 12345678, 0, 8),
    "007": ("integer", 7, 0, 1),
    "0": ("integer", 0, 0, 0),
    "-0": ("integer", 0, 0, 0),
    "1200": ("integer", 1200, 0, 4),
    "0.25": ("decimal", Fraction(1, 4), 2, 2),
    ".25": ("decimal", Fraction(1, 4), 2, 2),
    "305.": ("decimal", 305, 0, 3),
    "1,000.5": ("decimal", Fraction(2001, 2), 1, 5),
    "0.0120": ("decimal", Fraction(3, 250), 4, 3),
    "00.00": ("decimal", 0, 2, 0),
    "3.2e5": ("standard-form", 320000, 1, 2),
    "3.2E+5": ("standard-form", 320000, 1, 2),
    "3.2 x 10^5": ("standard-form", 320000, 1, 2),
    "3.2X10^5": ("standard-form", 320000, 1, 2),
    "3.2 * 10^5": ("standard-form", 320000, 1, 2),
    "3.2\u00d710^-3": ("standard-form", Fraction(2, 625), 1, 2),
    "5.e3": ("standard-form", 5000, 0, 1),
    "5.x10^3": ("standard-form", 5000, 0, 1),
    "5. x 10^3": ("standard-form", 5000, 0, 1),
    "5 x10^3": ("standard-form", 5000, 0, 1),
    "3.20e5": ("standard-form", 320000, 2, 3),
    "0.00e5": ("standard-form", 0, 2, 0),
    "1,000e3": ("standard-form", 10**6, 0, 4),
    "1e1000": ("standard-form", 10**1000, 0, 1),
    "1e-1000": ("standard-form", Fraction(1, 10**1000), 0, 1),
    "1e0001000": ("standard-form", 10**1000, 0, 1),
    "25%": ("percent", 25, 0, 2),
    "66.7 %": ("percent", Fraction(667, 10), 1, 3),
}


@pytest.mark.parametrize(("text", "expected"), DECIMAL_LIKE.items())
def test_rule_7_decimal_like_forms_values_places_and_figures(text: str, expected: tuple[object, ...]) -> None:
    result = number(text)
    assert (result.form, result.value, result.places, result.figures, result.typed) == (*expected, None)


FRACTIONS = {
    "2/3": ("fraction", Fraction(2, 3), (0, 2, 3)),
    "4/6": ("fraction", Fraction(2, 3), (0, 4, 6)),
    "-10 / 109": ("fraction", Fraction(-10, 109), (0, 10, 109)),
    "1 /2": ("fraction", Fraction(1, 2), (0, 1, 2)),
    "007/3": ("fraction", Fraction(7, 3), (0, 7, 3)),
    "-0/5": ("fraction", 0, (0, 0, 5)),
    "1,000/3": ("fraction", Fraction(1000, 3), (0, 1000, 3)),
    "3/1,000": ("fraction", Fraction(3, 1000), (0, 3, 1000)),
    "2 1/3": ("mixed", Fraction(7, 3), (2, 1, 3)),
    "-2 1/3": ("mixed", Fraction(-7, 3), (2, 1, 3)),
    "0 1/2": ("mixed", Fraction(1, 2), (0, 1, 2)),
    "2 1 / 3": ("mixed", Fraction(7, 3), (2, 1, 3)),
    "1,000 1/2": ("mixed", Fraction(2001, 2), (1000, 1, 2)),
    "007 01/02": ("mixed", Fraction(15, 2), (7, 1, 2)),
}


@pytest.mark.parametrize(("text", "expected"), FRACTIONS.items())
def test_rule_7_fractions_and_mixed_numbers_keep_their_parts(text: str, expected: tuple[object, ...]) -> None:
    result = number(text)
    assert (result.form, result.value, result.typed, result.places, result.figures) == (*expected, 0, 0)


FAILURES = {
    "1/0": "zero-denominator",
    "0/0": "zero-denominator",
    "2 1/0": "zero-denominator",
    "1/0%": "syntax",
    "2 0/3": "syntax",
    "2 3/3": "syntax",
    "2 4/3": "syntax",
    "0 0/1": "syntax",
    "1//2": "syntax",
    "1/2/3": "syntax",
    "/2": "syntax",
    "1/": "syntax",
    "1.5/2": "syntax",
    "1/-2": "syntax",
    "1 2 3/4": "syntax",
    ".": "syntax",
    ".e3": "syntax",
    "e5": "syntax",
    "e1001": "syntax",
    "x10^3": "syntax",
    "5 e3": "syntax",
    "5e 3": "syntax",
    "5x10^ 3": "syntax",
    "5x10 ^3": "syntax",
    "5x11^3": "syntax",
    "10^3": "syntax",
    "5e": "syntax",
    "1e5.5": "syntax",
    "1e1001": "out-of-range",
    "1e-1001": "out-of-range",
    "1e01001": "out-of-range",
    "0e1001": "out-of-range",
    "1x10^1001": "out-of-range",
    "1 * 10^-1001": "out-of-range",
    "1e" + "9" * 190: "out-of-range",
    "1,000,00": "syntax",
    "\u00bd": "syntax",
    "\u0663": "syntax",
    "\uff11": "syntax",
    "\U0001d7d1": "syntax",
    "1_000": "syntax",
    "0x10": "syntax",
    "Infinity": "syntax",
}


@pytest.mark.parametrize(("text", "expected"), FAILURES.items())
def test_rule_7_failures_in_the_order_7_2_checks_them(text: str, expected: str) -> None:
    assert reason(text) == expected


# Rule 8.


def test_rule_8_one_comma_that_reads_as_a_point_is_a_decimal_comma() -> None:
    commas = ("0,5", "0,500", "12,5%", ",5", "5,", "1,00", "1,0000", "1,2345", "01,000", "1,5e3", "1,5x10^3", "-0,5")
    for text in (*commas, "12,34", "1,5 %"):
        assert reason(text) == "decimal-comma"
    assert reason("£0,50", ("£",)) == "decimal-comma"
    for text in ("1,5e1001", ",", "1,5,5", "1,5/2", "1,5e3%", "1,5 1/2", "1,000,5", ",e5"):
        assert reason(text) == "syntax"
    assert number("1,000").value == 1000 and number("1,234").value == 1234


# Rule 9 and the table of accepted forms.


ACCEPTED = [
    ("11", (), "integer"),
    ("-3", (), "integer"),
    ("+5", (), "integer"),
    ("1,000", (), "integer"),
    ("0.25", (), "decimal"),
    (".25", (), "decimal"),
    ("305.", (), "decimal"),
    ("2/3", (), "fraction"),
    ("-10 / 109", (), "fraction"),
    ("2 1/3", (), "mixed"),
    ("25%", (), "percent"),
    ("66.7 %", (), "percent"),
    ("3.2e5", (), "standard-form"),
    ("3.2 x 10^5", (), "standard-form"),
    ("3.2\u00d710^-3", (), "standard-form"),
    ("£12.50", ("£",), "decimal"),
    ("12.5", ("£",), "decimal"),
]


@pytest.mark.parametrize(("text", "units", "form"), ACCEPTED)
def test_rule_9_each_accepted_input_form(text: str, units: tuple[str, ...], form: str) -> None:
    assert number(text, units).form == form


def test_rule_9_the_golden_spelling_of_a_result() -> None:
    assert out(parse("007/3")) == {
        "ok": True,
        "form": "fraction",
        "value": "7/3",
        "places": 0,
        "figures": 0,
        "typed": {"whole": "0", "n": "7", "d": "3"},
        "unit": None,
    }
    assert out(parse("-£12.50", ("£",))) == {
        "ok": True,
        "form": "decimal",
        "value": "-25/2",
        "places": 2,
        "figures": 4,
        "typed": None,
        "unit": "£",
    }
    assert out(parse("0,5")) == {"ok": False, "reason": "decimal-comma"}


# Properties.

TOKENS = (*DIGITS, " ", "\t", "\n", *NARROW, *",./%eExX*^+-", "\u2212", "\u00d7", "£", "s", "10^")
TEXTS = st.lists(st.sampled_from(TOKENS) | st.characters(), max_size=30).map("".join)
UNIT_NAMES = ("", "£", "%", "s", "ms", "bp", "x", "e", "\u03a9", "outcomes")


@st.composite
def plain_numbers(draw: st.DrawFn) -> tuple[str, Fraction]:
    """A well-formed unsigned integer, decimal, fraction or mixed number, and its exact value."""
    kind = draw(st.sampled_from(("integer", "decimal", "point first", "fraction", "mixed")))
    a = draw(st.text(DIGITS, min_size=1, max_size=12))
    if kind == "integer":
        return a, Fraction(int(a))
    b = draw(st.text(DIGITS, min_size=1 if kind == "point first" else 0, max_size=8))
    if kind in ("decimal", "point first"):
        head = a if kind == "decimal" else ""
        return f"{head}.{b}", Fraction(int(head + b or "0"), 10 ** len(b))
    d = draw(st.integers(2, 10**9))
    if kind == "fraction":
        return f"{a}/{d}", Fraction(int(a), d)
    n = draw(st.integers(1, d - 1))
    return f"{a} {n}/{d}", int(a) + Fraction(n, d)


@given(
    TEXTS | plain_numbers().map(lambda case: case[0]),
    st.lists(st.sampled_from(UNIT_NAMES) | st.text(max_size=3), max_size=3),
)
@example("4/6", [])
@example("-2 1/3", ["s"])
def test_every_text_reads_or_fails_with_one_of_the_six_reasons(text: str, units: list[str]) -> None:
    result = parse(text, units)
    if isinstance(result, Failure):
        assert result.reason in REASONS
        return
    assert result.form in FORMS and result.places >= 0 and result.figures >= 0
    assert result.unit is None or result.unit in units
    assert result.form != "percent" or result.unit is None
    assert (result.typed is None) == (result.form not in ("fraction", "mixed"))
    if result.typed is not None:
        w, n, d = result.typed
        assert abs(result.value) == w + Fraction(n, d) and d > 0 and result.figures == 0
        assert w == 0 if result.form == "fraction" else 0 < n < d


@given(plain_numbers(), st.text(string.ascii_letters, min_size=1, max_size=4), st.booleans())
def test_a_listed_ascii_unit_matches_in_any_ascii_case(case: tuple[str, Fraction], unit: str, swap: bool) -> None:
    result = number(f"{case[0]} {unit.swapcase() if swap else unit}", (unit,))
    assert (result.unit, result.value) == (unit, case[1])


@given(st.characters(min_codepoint=0x80).filter(lambda c: c.swapcase() != c))
def test_a_cased_letter_outside_ascii_never_matches_its_other_case(c: str) -> None:
    other = c.swapcase()
    assume(c not in other)
    assert reason("5" + other, (c,)) == "syntax"


@given(st.text(min_size=TOO_LONG, max_size=TOO_LONG + 40))
def test_more_than_200_code_points_is_too_long(text: str) -> None:
    assert reason(text) == "too-long"


@given(st.text(st.characters(min_codepoint=0x10000), min_size=1, max_size=110))
def test_an_astral_character_counts_twice(text: str) -> None:
    assert (reason(text) == "too-long") == (len(text) > 100)


@given(st.integers(-(10**60), 10**60), st.sampled_from(NARROW))
def test_an_integer_reads_back_plain_or_grouped(n: int, s: str) -> None:
    for text in (str(n), f"{n:,}", f"{n:,}".replace(",", s)):
        result = number(text)
        figures = len(str(abs(n)).lstrip("0"))
        assert (result.form, result.value, result.places, result.figures) == ("integer", n, 0, figures)


SLASHES = ("/", " /", "\t/", "~/")


@given(st.integers(1000, 10**30), st.integers(0, 10**6), st.sampled_from(NARROW), st.sampled_from(SLASHES))
def test_a_narrow_space_grouped_integer_before_a_slash_is_syntax(n: int, d: int, s: str, slash: str) -> None:
    assert reason(f"{n:,}".replace(",", s) + slash.replace("~", s) + str(d)) == "syntax"


@given(plain_numbers(), st.sampled_from(("", "-", "+", "\u2212", "- ", "\u2013")))
def test_a_well_formed_number_reads_back_exact_with_its_sign(case: tuple[str, Fraction], sign: str) -> None:
    text, value = case
    negative = sign.strip() in ("-", "\u2212", "\u2013")
    unsigned = number(text)
    assert unsigned.value == value
    assert number(sign + text) == (dataclasses.replace(unsigned, value=-value) if negative else unsigned)


@given(plain_numbers(), st.text(" \t\n\r\v\f\u00a0\u202f", max_size=4), st.text(" \t\n\r\v\f\u2009", max_size=4))
def test_surrounding_whitespace_changes_nothing(case: tuple[str, Fraction], before: str, after: str) -> None:
    assert parse(before + case[0] + after) == parse(case[0])


@given(st.integers(0, 10**9), st.integers(0, 4), st.integers(-1000, 1000))
def test_every_spelling_of_standard_form_gives_one_value(m: int, p: int, k: int) -> None:
    digits = str(m).zfill(p + 1)
    mantissa = f"{digits[: len(digits) - p]}.{digits[len(digits) - p :]}" if p else digits
    expected = Fraction(m, 10**p) * Fraction(10) ** k
    marks = ("e", "E+" if k >= 0 else "E", "x10^", " * 10^", "\u00d710^", " \u22c5 10^")
    for text in (f"{mantissa}{mark}{k}" for mark in marks):
        result = number(text)
        assert (result.form, result.value, result.places) == ("standard-form", expected, p)


@given(st.integers(0, 10**6), st.integers(1001, 10**12), st.sampled_from(("e", "e-", "x10^", " * 10^-")))
def test_an_exponent_beyond_1000_is_out_of_range(m: int, k: int, mark: str) -> None:
    assert reason(f"{m}{mark}{k}") == "out-of-range"


@given(st.integers(0, 10**12), st.integers(0, 8), st.sampled_from(("%", " %")))
def test_a_percent_is_the_number_before_it(m: int, p: int, mark: str) -> None:
    digits = str(m).zfill(p + 1)
    text = f"{digits[: len(digits) - p]}.{digits[len(digits) - p :]}" if p else digits
    plain, percent = number(text), number(text + mark)
    assert percent == dataclasses.replace(plain, form="percent")


@given(st.text(DIGITS, max_size=6), st.text(DIGITS, max_size=6))
def test_one_comma_for_a_point_is_a_decimal_comma_unless_it_groups(a: str, b: str) -> None:
    text = f"{a},{b}"
    groups = 1 <= len(a) <= 3 and a[0] != "0" and len(b) == 3
    if groups:
        assert number(text).value == int(a + b)
    elif a or b:
        assert reason(text) == "decimal-comma"
    else:
        assert reason(text) == "syntax"


LISTED = ("£", "s", "ms", "bp", "outcomes")


@given(plain_numbers(), st.sampled_from(LISTED), st.sampled_from(("", " ")), st.booleans(), st.booleans())
def test_a_listed_unit_at_either_end_in_any_case_is_stripped(
    case: tuple[str, Fraction], unit: str, gap: str, first: bool, upper: bool
) -> None:
    typed = unit.upper() if upper else unit
    text = f"{typed}{gap}{case[0]}" if first else f"{case[0]}{gap}{typed}"
    result = number(text, LISTED)
    assert (result.unit, result.value) == (unit, case[1])


@given(TEXTS)
def test_normalisation_leaves_no_narrow_space_tab_dash_times_or_double_space(text: str) -> None:
    t = normalise(code_units(text))
    if t is None:
        return
    assert not set(t) & (num_parse.NARROW_SET | num_parse.DASHES | num_parse.TIMES | {"\t"})
    assert "  " not in t and t == t.strip(num_parse.ENDS)
