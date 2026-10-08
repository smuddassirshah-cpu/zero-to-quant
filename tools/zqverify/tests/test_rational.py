"""The rational goldens are fresh, and their twin is Fraction under the canonical spelling."""

from fractions import Fraction

from hypothesis import given, strategies as st

from zqverify import rational


def test_the_committed_goldens_are_fresh() -> None:
    assert rational.GOLDEN.read_text(encoding="utf-8") == rational.render()


def test_spell_and_terminates() -> None:
    assert rational.spell(Fraction(-6, 4)) == "-3/2"
    assert rational.spell(Fraction(0)) == "0"
    assert rational.terminates(Fraction(3, 40)) and not rational.terminates(Fraction(1, 3))


@given(st.fractions())
def test_spelling_reads_back(q: Fraction) -> None:
    assert rational.parse(rational.spell(q)) == q
