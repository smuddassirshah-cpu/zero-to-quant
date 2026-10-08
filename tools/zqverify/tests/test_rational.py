"""The rational goldens are fresh, their twin is Fraction under the canonical spelling, and the twin's grammar
refuses each listed spelling with the TypeScript's message."""

from fractions import Fraction

from hypothesis import given, strategies as st

from zqverify import rational


def refusal(text: str) -> str | None:
    try:
        rational.parse(text)
    except ValueError as error:
        return str(error)
    return None


def numerator(text: object) -> int:
    return rational.parse(str(text)).numerator


def test_the_committed_goldens_are_fresh() -> None:
    assert rational.GOLDEN.read_text(encoding="utf-8") == rational.render()


def test_spell_and_terminates() -> None:
    assert rational.spell(Fraction(-6, 4)) == "-3/2"
    assert rational.spell(Fraction(0)) == "0"
    assert rational.terminates(Fraction(3, 40)) and not rational.terminates(Fraction(1, 3))


def test_parse_refuses_each_listed_spelling_with_its_message() -> None:
    assert {text: refusal(text) for text in rational.REFUSED} == rational.REFUSED


def test_parse_reads_the_dot_at_either_end_upper_case_e_and_the_limit() -> None:
    assert rational.parse(".25") == Fraction(1, 4) and rational.parse("305.") == 305
    assert rational.parse("1.E+2") == 100 and rational.parse("-0") == 0
    assert rational.parse("1e1000") == 10**1000 and rational.parse("1e-1000") == Fraction(1, 10**1000)


def test_the_goldens_reach_both_branches_of_eq() -> None:
    pairs = [g for g in rational.goldens() if g["kind"] == "pair"]
    same = [g for g in pairs if g["eq"]]
    shared = [g for g in pairs if not g["eq"] and numerator(g["a"]) == numerator(g["b"])]
    assert len(same) >= rational.SAME // 2 and len(shared) >= rational.SAME // 2


@given(st.fractions())
def test_spelling_reads_back(q: Fraction) -> None:
    assert rational.parse(rational.spell(q)) == q
