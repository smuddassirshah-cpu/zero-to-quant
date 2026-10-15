"""Goldens for @zq/mathcore/num-parse, the en-GB number parser shared with the graders.

Written from docs/CONTENT-FORMAT.md 7.2 alone, by a session that has not read the TypeScript, its tests, its
golden file or the earlier twin (CLAUDE.md hard rule 4); where the two disagree, 7.2 decides. `parse(text, units)`
applies the section's nine rules in order and returns a `Number` or a `Failure`; `out` spells either as a golden
line's `out`.

Decision notes:
- Code units. 7.2 measures lengths in UTF-16 code units, so `parse` first rewrites the text with each astral code
  point split into its surrogate pair (`code_units`); rule 1's length and rule 5's unit lengths and slices then
  count what JavaScript counts. Rule 5 compares code units after mapping A to Z to a to z and nothing else, so no
  engine's Unicode version enters, and a lone surrogate, or the half of a pair a unit's window cuts, compares as
  itself. A unit with more code units than the text never matches it.
- A hand-written scanner over indices: no grammar in regular expressions, no eval or exec. Every token of rules 2
  to 8 is a listed BMP character, and each rule is one left-to-right pass, so a parse is O(n). The one regular
  expression collapses rule 2.5's runs of spaces and tabs.
- Rule 2.2's runs. A run's leading digits are forced (fewer would leave a digit where its narrow space must
  stand), and of its groups only the last can be followed by a digit, so the longest run that satisfies the rule
  is all of its groups or all but the last. The slash check reads the same runs before any is removed.
- Rule 7's integer part is a grouped integer wherever one starts, else a plain run of digits: what may follow an
  integer part (a space, `/`, `.`, an exponent or the end) is never a digit or a comma, so where the grouped
  reading fails the plain one fails too. The slash and the space after the first integer part tell the three body
  shapes apart, so "tried in this order" never has to backtrack.
- Values are exact Fractions, spelt by zqverify.rational.spell, the spelling 7.2's golden paragraph names.

The golden file holds the fixed cases (every example of 7.2, each typed with every narrow space where the section's
examples stand a space for one, and the bounds) and random cases drawn by `random.Random` seeded with the module
name: well-formed numbers of every form with signs, dashes, units and spaces, a third of them mutated by a few
inserted, deleted or replaced characters. From the repository root, rewrite it with the command 7.2 names:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.num_parse
"""

from __future__ import annotations

import json
import random
import re
import string
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from zqverify.rational import spell

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "num-parse.golden.jsonl"
MAX_LENGTH = 200
EXPONENT_LIMIT = 1000
RANDOM_CASES = 1500

REASONS = ("empty", "too-long", "decimal-comma", "zero-denominator", "out-of-range", "syntax")
FORMS = ("integer", "decimal", "fraction", "mixed", "percent", "standard-form")

DASHES = frozenset([*map(chr, range(0x2010, 0x2016)), "\u2212", "\ufe58", "\ufe63", "\uff0d"])
NARROW = ("\u00a0", "\u2007", "\u2009", "\u200a", "\u202f")
NARROW_SET = frozenset(NARROW)
TIMES = frozenset("\u00d7\u00b7\u22c5")
BEFORE_SLASH = NARROW_SET | {" ", "\t"}
ENDS = " \t\n\v\f\r"
SPACES_AND_TABS = re.compile("[ \t]+")
ASCII_LOWER = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)


@dataclass(frozen=True)
class Number:
    form: str
    value: Fraction
    places: int
    figures: int
    typed: tuple[int, int, int] | None  # whole, numerator and denominator, for a fraction or a mixed number
    unit: str | None


@dataclass(frozen=True)
class Failure:
    reason: str


SYNTAX = Failure("syntax")


def code_units(s: str) -> str:
    """s with each astral code point as its UTF-16 surrogate pair, so len and slices count code units."""
    return "".join(c if ord(c) < 0x10000 else _pair(ord(c) - 0x10000) for c in s)


def _pair(offset: int) -> str:
    return chr(0xD800 + (offset >> 10)) + chr(0xDC00 + (offset & 0x3FF))


def _fold(units: str) -> str:
    """Rule 5's case rule on a code-unit string: A to Z become a to z, and every other code unit stays."""
    return units.translate(ASCII_LOWER)


def _digit(c: str) -> bool:
    return len(c) == 1 and "0" <= c <= "9"


def _run_end(t: str, i: int) -> int | None:
    """The end of the rule 2.2 grouping run that starts at i, or None."""
    if not "1" <= t[i] <= "9":
        return None
    before = t[i - 1] if i else ""
    if _digit(before) or before in (".", ",", "e", "E", "^"):
        return None
    if before in ("+", "-") and i >= 2 and t[i - 2] in ("e", "E", "^"):
        return None
    j = i + 1
    while j < len(t) and j - i < 3 and _digit(t[j]):
        j += 1
    ends = []
    while j + 4 <= len(t) and t[j] in NARROW_SET and all(map(_digit, t[j + 1 : j + 4])):
        j += 4
        ends.append(j)
    if ends and j < len(t) and _digit(t[j]):
        ends.pop()
    return ends[-1] if ends else None


def grouping_runs(t: str) -> list[tuple[int, int]]:
    """Rule 2.2's runs in the text step 1 leaves, left to right, without overlap, each the longest."""
    runs, i = [], 0
    while i < len(t):
        end = _run_end(t, i)
        if end is None:
            i += 1
        else:
            runs.append((i, end))
            i = end
    return runs


def normalise(t: str) -> str | None:
    """Rule 2 on a code-unit string; None where a grouping run stands before a slash (2.2's syntax at once)."""
    t = "".join("-" if c in DASHES else c for c in t)
    runs = grouping_runs(t)
    for _, end in runs:
        k = end
        while k < len(t) and t[k] in BEFORE_SLASH:
            k += 1
        if t[k : k + 1] == "/":
            return None
    kept, last = [], 0
    for start, end in runs:
        kept += (t[last:start], "".join(c for c in t[start:end] if c not in NARROW_SET))
        last = end
    kept.append(t[last:])
    t = "".join(" " if c in NARROW_SET else "*" if c in TIMES else c for c in "".join(kept))
    return SPACES_AND_TABS.sub(" ", t).strip(ENDS)


def strip_unit(t: str, units: Iterable[str]) -> tuple[str | None, str]:
    """Rule 5: the unit as listed and the text without it, or None and the text."""
    for unit in sorted((u for u in units if u), key=lambda u: -len(code_units(u))):
        spelt = code_units(unit)
        k, key = len(spelt), _fold(spelt)
        if len(t) < k:
            continue
        if _fold(t[:k]) == key:
            rest = t[k:]
            return unit, rest[1:] if rest[:1] == " " else rest
        if _fold(t[len(t) - k :]) == key:
            rest = t[: len(t) - k]
            return unit, rest[:-1] if rest[-1:] == " " else rest
    return None, t


def _integer_part(t: str, i: int) -> tuple[int, int] | None:
    """Rule 7's integer part at i as (end, value): a grouped integer where one starts, else a plain run."""
    j = i
    while j < len(t) and _digit(t[j]):
        j += 1
    if j == i:
        return None
    k = j
    if t[i] != "0" and j - i <= 3:
        while k + 4 <= len(t) and t[k] == "," and all(map(_digit, t[k + 1 : k + 4])):
            k += 4
    return k, int(t[i:k].replace(",", ""))


def _signed_digits(t: str, i: int) -> tuple[int, int] | None:
    """An optional sign and one or more digits at i, as (end, value)."""
    j = i + 1 if t[i : i + 1] in ("+", "-") else i
    k = j
    while k < len(t) and _digit(t[k]):
        k += 1
    return (k, int(t[i:k])) if k > j else None


def _fraction(t: str, percent: bool) -> Number | Failure:
    """Rule 7's mixed and fraction shapes and their checks, in 7.2's order."""
    first = _integer_part(t, 0)
    if first is None:
        return SYNTAX
    whole, top = None, first
    if t[first[0] : first[0] + 1] == " ":
        second = _integer_part(t, first[0] + 1)
        if second is not None:
            whole, top = first, second
    i = top[0] + (t[top[0] : top[0] + 1] == " ")
    if t[i : i + 1] != "/":
        return SYNTAX
    i += 1 + (t[i + 1 : i + 2] == " ")
    bottom = _integer_part(t, i)
    if bottom is None or bottom[0] != len(t) or percent:
        return SYNTAX
    w, n, d = 0 if whole is None else whole[1], top[1], bottom[1]
    if d == 0:
        return Failure("zero-denominator")
    if whole is not None and not 0 < n < d:
        return SYNTAX
    return Number("fraction" if whole is None else "mixed", w + Fraction(n, d), 0, 0, (w, n, d), None)


def _decimal_like(t: str, percent: bool) -> Number | Failure:
    """Rule 7's decimal-like shape and its checks, in 7.2's order."""
    head = _integer_part(t, 0)
    i = head[0] if head else 0
    digits, places = t[:i].replace(",", ""), 0
    point = t[i : i + 1] == "."
    if point:
        j = i + 1
        while j < len(t) and _digit(t[j]):
            j += 1
        digits, places, i = digits + t[i + 1 : j], j - i - 1, j
    exponent = None
    if t[i : i + 1] in ("e", "E"):
        read = _signed_digits(t, i + 1)
        if read is None:
            return SYNTAX
        i, exponent = read
    else:
        k = i + (t[i : i + 1] == " ")
        if t[k : k + 1] in ("*", "x", "X"):
            k += 1 + (t[k + 1 : k + 2] == " ")
            read = _signed_digits(t, k + 3) if t[k : k + 3] == "10^" else None
            if read is None:
                return SYNTAX
            i, exponent = read
    if i != len(t) or not digits:
        return SYNTAX
    if exponent is not None and percent:
        return SYNTAX
    if exponent is not None and abs(exponent) > EXPONENT_LIMIT:
        return Failure("out-of-range")
    value = Fraction(int(digits), 10**places) * Fraction(10) ** (exponent or 0)
    form = "percent" if percent else "standard-form" if exponent is not None else "decimal" if point else "integer"
    return Number(form, value, places, len(digits.lstrip("0")), None, None)


def body(t: str, percent: bool) -> Number | Failure:
    """Rule 7 on the text rules 4 to 6 leave: a slash makes it a mixed number or a fraction, or nothing."""
    return _fraction(t, percent) if "/" in t else _decimal_like(t, percent)


def parse(text: str, units: Sequence[str] = ()) -> Number | Failure:
    """Read a typed number under 7.2's rules 1 to 9."""
    typed = code_units(text)
    if len(typed) > MAX_LENGTH:
        return Failure("too-long")
    t = normalise(typed)
    if t is None:
        return SYNTAX
    if not t:
        return Failure("empty")
    negative = t[0] == "-"
    if t[0] in ("-", "+"):
        t = t[2:] if t[1:2] == " " else t[1:]
    unit, t = strip_unit(t, units)
    percent = unit is None and t[-1:] == "%"
    if percent:
        t = t[:-2] if t[-2:-1] == " " else t[:-1]
    read = body(t, percent)
    if isinstance(read, Failure):
        if read == SYNTAX and t.count(",") == 1 and isinstance(body(t.replace(",", "."), percent), Number):
            return Failure("decimal-comma")
        return read
    return Number(read.form, -read.value if negative else read.value, read.places, read.figures, read.typed, unit)


def out(result: Number | Failure) -> dict[str, object]:
    """A result as a golden line's `out`."""
    if isinstance(result, Failure):
        return {"ok": False, "reason": result.reason}
    typed = None if result.typed is None else dict(zip(("whole", "n", "d"), map(str, result.typed), strict=True))
    return {
        "ok": True,
        "form": result.form,
        "value": spell(result.value),
        "places": result.places,
        "figures": result.figures,
        "typed": typed,
        "unit": result.unit,
    }


# Fixed cases. "~" in a text stands for a narrow space: the case is written once for each of the five.
NO_UNITS: tuple[str, ...] = ()
POUND = ("£",)
FIXED: list[tuple[str, tuple[str, ...]]] = [
    # Rule 1: the length in code units, before anything else.
    ("1" * 200, NO_UNITS),
    ("1" * 201, NO_UNITS),
    (" " * 201, NO_UNITS),
    ("x" * 201, NO_UNITS),
    (" " * 199 + "7", NO_UNITS),
    ("\U0001f600" * 100, NO_UNITS),
    ("\U0001f600" * 100 + "1", NO_UNITS),
    ("1" * 199 + "\U0001f600", NO_UNITS),
    ("1~000/" + " " * 194, NO_UNITS),
    ("1~000/" + " " * 195, NO_UNITS),
    # Rule 2.1: every dash and minus, at the start, after a space and in an exponent.
    *((f"{dash}5", NO_UNITS) for dash in sorted(DASHES)),
    ("\u2212 5", NO_UNITS),
    ("1e\u22123", NO_UNITS),
    ("3.2 \u00d7 10^\u20133", NO_UNITS),
    ("5\u20133", NO_UNITS),
    # Rule 2.2: grouping runs, each example of 7.2 and the slash check.
    ("1~000", NO_UNITS),
    ("1~234~567", NO_UNITS),
    ("12~345.5", NO_UNITS),
    ("1~000,5", NO_UNITS),
    ("3/1~000", NO_UNITS),
    ("0~500", NO_UNITS),
    ("1~2345", NO_UNITS),
    ("0.123~456", NO_UNITS),
    ("3.2e1~000", NO_UNITS),
    ("1e-1~000", NO_UNITS),
    ("1e\u22121~000", NO_UNITS),
    ("1E+1~000", NO_UNITS),
    ("5x10^1~000", NO_UNITS),
    ("1~000~0000", NO_UNITS),
    ("2~125/250", NO_UNITS),
    ("12~345/7", NO_UNITS),
    ("1~000/0", NO_UNITS),
    ("1~000/s", ("s",)),
    ("1~000 /3", NO_UNITS),
    ("1~000\t/3", NO_UNITS),
    ("1~000~~/3", NO_UNITS),
    ("1~000~/~3", NO_UNITS),
    ("1~000/2~000", NO_UNITS),
    ("2~1/3", NO_UNITS),
    ("1~000~1/2", NO_UNITS),
    ("1~000~000.5", NO_UNITS),
    ("\u22121~000", NO_UNITS),
    ("£1~000", POUND),
    ("1~000%", NO_UNITS),
    ("1~000,000", NO_UNITS),
    ("1,000~000", NO_UNITS),
    ("1234~567", NO_UNITS),
    (".1~000", NO_UNITS),
    (",1~000", NO_UNITS),
    ("1/2~000", NO_UNITS),
    ("1~000~1~000", NO_UNITS),
    ("1~0001~000", NO_UNITS),
    ("1 000", NO_UNITS),
    ("1~000 1/2", NO_UNITS),
    ("~5~", NO_UNITS),
    ("1~000,5/2", NO_UNITS),
    ("1~000/2,5", NO_UNITS),
    # Rules 2.3 to 2.6.
    ("2\u00a01/3", NO_UNITS),
    ("3.2\u00d710^5", NO_UNITS),
    ("3.2\u00b710^5", NO_UNITS),
    ("3.2\u22c510^5", NO_UNITS),
    ("2\u00d73", NO_UNITS),
    ("2\t1/3", NO_UNITS),
    ("2  1/3", NO_UNITS),
    ("2 \t 1/3", NO_UNITS),
    ("1 \t/ \t2", NO_UNITS),
    (" 5 ", NO_UNITS),
    ("\t5\n", NO_UNITS),
    ("\r\n5\r\n", NO_UNITS),
    ("\v5\f", NO_UNITS),
    ("\u30005", NO_UNITS),
    ("\ufeff5", NO_UNITS),
    ("5\u2028", NO_UNITS),
    ("\u00855", NO_UNITS),
    ("1\n000", NO_UNITS),
    ("2\n1/3", NO_UNITS),
    ("2 \n 1/3", NO_UNITS),
    ("5\v", NO_UNITS),
    # Rule 3.
    ("", NO_UNITS),
    (" ", NO_UNITS),
    ("\t\n\r\v\f", NO_UNITS),
    ("\u00a0", NO_UNITS),
    ("\u00a0 \u202f", NO_UNITS),
    ("\u3000", NO_UNITS),
    # Rule 4.
    ("+-5", NO_UNITS),
    ("++5", NO_UNITS),
    ("£-5", POUND),
    ("+33.1%", NO_UNITS),
    ("-£5", POUND),
    ("+£5", POUND),
    ("-+5", NO_UNITS),
    ("--5", NO_UNITS),
    ("- -5", NO_UNITS),
    ("5-", NO_UNITS),
    ("+ 5", NO_UNITS),
    ("-  5", NO_UNITS),
    ("-", NO_UNITS),
    ("+", NO_UNITS),
    ("- ", NO_UNITS),
    ("- £ 5", POUND),
    ("£ -5", POUND),
    # Rule 5.
    ("5 ms", ("s", "ms")),
    ("5ms", ("s", "ms")),
    ("5s", ("s", "ms")),
    ("5 MS", ("ms",)),
    ("Ms 5", ("ms",)),
    ("ms5", ("m", "ms")),
    ("5kg", ("KG", "kg")),
    ("5kg", ("kg", "KG")),
    ("5 Kg", ("g", "kg")),
    ("£5£", POUND),
    ("£5p", ("£", "p")),
    ("£ 5", POUND),
    ("5 £", POUND),
    ("5£", POUND),
    ("£  5", POUND),
    ("5", ("", "s")),
    ("5s", ("", "s")),
    ("5", ("",)),
    ("5%", ("",)),
    ("25%", ("%",)),
    ("25 %", ("%",)),
    ("%25", ("%",)),
    ("2.5%", ("%",)),
    ("1/4%", ("%",)),
    ("1e3%", ("%",)),
    ("£12.50", POUND),
    ("12.5", POUND),
    ("£25%", POUND),
    ("-5 s", ("s",)),
    ("5 s 1", ("s",)),
    ("11 outcomes", ("outcomes",)),
    ("11 Outcomes", ("outcomes",)),
    ("11", ("outcomes",)),
    ("250 bp", ("bp", "%")),
    ("2.5 %", ("bp", "%")),
    ("5x10^3", ("x",)),
    ("5x", ("x",)),
    ("5e3", ("e",)),
    ("5e", ("e",)),
    ("£", POUND),
    ("£%", POUND),
    ("5\u03c9", ("\u03a9",)),
    ("5k", ("\u212a",)),
    ("5SS", ("\u00df",)),
    ("5\u00df", ("\u00df",)),
    ("5\u0130", ("\u0130",)),
    ("5i", ("\u0130",)),
    ("5\U00010428", ("\U00010400",)),
    ("5 \u03c3\u03b1\u03c2", ("\u03a3\u0391\u03a3",)),
    ("5 \u03c3\u03b1\u03c3", ("\u03a3\u0391\u03a3",)),
    ("5", ("€", "£", "$")),
    ("5 €", ("$", "€")),
    ("1/2 s", ("s",)),
    ("2 1/3 s", ("s",)),
    ("3.2e5 s", ("s",)),
    # Case: A to Z against a to z only, so no pair outside ASCII matches, whatever Unicode version maps it.
    ("12 BP", ("bp",)),
    ("12 bp", ("BP",)),
    ("bP 12", ("Bp",)),
    ("5K", ("k",)),
    ("5\ua7cb", ("\u0264",)),
    ("5\u0264", ("\ua7cb",)),
    ("5\ua7cb", ("\ua7cb",)),
    ("5\u212a", ("k",)),
    ("5\u212a", ("K",)),
    ("5\u212a", ("\u212a",)),
    ("5\u03c3", ("\u03a3",)),
    ("5\u03a3", ("\u03c3",)),
    ("5\u00e9", ("\u00c9",)),
    ("5\U00010400", ("\U00010400",)),
    # Lone surrogates in the text and in a unit, and unit windows that cut an astral pair.
    ("5\ud800", NO_UNITS),
    ("\udc005", NO_UNITS),
    ("5\ud800", ("\ud800",)),
    ("\udc005", ("\udc00",)),
    ("5\U0001f600", ("\ude00",)),
    ("\U0001f6005", ("\ud83d",)),
    ("5\ud83d", ("\U0001f600",)),
    ("5\U0001f600", ("\U0001f600",)),
    # A unit with more code units than the text never matches, so a shorter one is tried.
    ("5\u0130", ("5i\u0307", "\u0130")),
    ("\u01305", ("i\u03075", "\u0130")),
    ("5 \u0130", ("5 i\u0307", "\u0130")),
    ("\u0130", ("i\u0307",)),
    # Rule 6.
    ("25%", NO_UNITS),
    ("25 %", NO_UNITS),
    ("66.7 %", NO_UNITS),
    ("-25%", NO_UNITS),
    ("25%%", NO_UNITS),
    ("%", NO_UNITS),
    ("% 25", NO_UNITS),
    ("25  %", NO_UNITS),
    (".5%", NO_UNITS),
    ("5.%", NO_UNITS),
    ("0%", NO_UNITS),
    ("1,000%", NO_UNITS),
    ("1 %", NO_UNITS),
    # Rule 7: integers, decimals, figures and places.
    ("11", NO_UNITS),
    ("-3", NO_UNITS),
    ("+5", NO_UNITS),
    ("1,000", NO_UNITS),
    ("12,345,678", NO_UNITS),
    ("007", NO_UNITS),
    ("0", NO_UNITS),
    ("-0", NO_UNITS),
    ("0000", NO_UNITS),
    ("0.25", NO_UNITS),
    (".25", NO_UNITS),
    ("305.", NO_UNITS),
    ("1,000.5", NO_UNITS),
    ("0.0120", NO_UNITS),
    ("1200", NO_UNITS),
    ("0.", NO_UNITS),
    ("00.00", NO_UNITS),
    ("-0.0", NO_UNITS),
    ("1,2345", NO_UNITS),
    ("01,000", NO_UNITS),
    ("1,000,00", NO_UNITS),
    # Rule 7: fractions and mixed numbers.
    ("2/3", NO_UNITS),
    ("4/6", NO_UNITS),
    ("-10 / 109", NO_UNITS),
    ("007/3", NO_UNITS),
    ("0/5", NO_UNITS),
    ("-0/5", NO_UNITS),
    ("1,000/3", NO_UNITS),
    ("3/1,000", NO_UNITS),
    ("1/0", NO_UNITS),
    ("0/0", NO_UNITS),
    ("1/0%", NO_UNITS),
    ("2/3%", NO_UNITS),
    ("1 /2", NO_UNITS),
    ("1/ 2", NO_UNITS),
    ("1 / 2", NO_UNITS),
    ("1//2", NO_UNITS),
    ("1/2/3", NO_UNITS),
    ("/2", NO_UNITS),
    ("1/", NO_UNITS),
    ("1.5/2", NO_UNITS),
    ("1/-2", NO_UNITS),
    ("1/+2", NO_UNITS),
    ("2 1/3", NO_UNITS),
    ("-2 1/3", NO_UNITS),
    ("0 1/2", NO_UNITS),
    ("2 1/0", NO_UNITS),
    ("2 0/3", NO_UNITS),
    ("2 3/3", NO_UNITS),
    ("2 4/3", NO_UNITS),
    ("1 1/2%", NO_UNITS),
    ("1,000 1/2", NO_UNITS),
    ("2 1 / 3", NO_UNITS),
    ("2 1/ 3", NO_UNITS),
    ("007 01/02", NO_UNITS),
    ("2 1/3/4", NO_UNITS),
    ("1 2 3/4", NO_UNITS),
    ("0 0/1", NO_UNITS),
    ("2 1/2.5", NO_UNITS),
    # Rule 7: standard form and the exponent's bound.
    ("3.2e5", NO_UNITS),
    ("3.2E5", NO_UNITS),
    ("3.2e+5", NO_UNITS),
    ("3.2e-3", NO_UNITS),
    ("3.2 x 10^5", NO_UNITS),
    ("3.2x10^5", NO_UNITS),
    ("3.2X10^5", NO_UNITS),
    ("3.2 * 10^5", NO_UNITS),
    ("3.2*10^-3", NO_UNITS),
    ("5.e3", NO_UNITS),
    ("5.x10^3", NO_UNITS),
    ("5. x 10^3", NO_UNITS),
    ("5 x10^3", NO_UNITS),
    ("5x 10^3", NO_UNITS),
    ("3.20e5", NO_UNITS),
    ("0.00e5", NO_UNITS),
    ("1,000e3", NO_UNITS),
    ("5 e3", NO_UNITS),
    ("5e 3", NO_UNITS),
    ("5x10^ 3", NO_UNITS),
    ("5x10 ^3", NO_UNITS),
    ("5xx10^3", NO_UNITS),
    ("5x11^3", NO_UNITS),
    ("5^3", NO_UNITS),
    ("10^3", NO_UNITS),
    ("x10^3", NO_UNITS),
    (".e3", NO_UNITS),
    ("e5", NO_UNITS),
    (".", NO_UNITS),
    ("e1001", NO_UNITS),
    ("5e", NO_UNITS),
    ("5e+", NO_UNITS),
    ("1e5.5", NO_UNITS),
    ("1e1000", NO_UNITS),
    ("1e-1000", NO_UNITS),
    ("-9.5E+1000", NO_UNITS),
    ("1e0001000", NO_UNITS),
    ("1e1001", NO_UNITS),
    ("1e-1001", NO_UNITS),
    ("1e01001", NO_UNITS),
    ("0e1001", NO_UNITS),
    ("1x10^1001", NO_UNITS),
    ("1 * 10^-1001", NO_UNITS),
    ("1e1001%", NO_UNITS),
    ("1e3%", NO_UNITS),
    ("1e" + "9" * 190, NO_UNITS),
    # Rule 7: other text.
    ("abc", NO_UNITS),
    ("1.2.3", NO_UNITS),
    ("1..2", NO_UNITS),
    ("--", NO_UNITS),
    ("1,2,3", NO_UNITS),
    ("\u00bd", NO_UNITS),
    ("\u0663", NO_UNITS),
    ("\uff11", NO_UNITS),
    ("0x10", NO_UNITS),
    ("Infinity", NO_UNITS),
    ("NaN", NO_UNITS),
    ("1_000", NO_UNITS),
    ("\U0001d7d1", NO_UNITS),
    # Rule 8.
    ("0,5", NO_UNITS),
    ("0,500", NO_UNITS),
    ("12,5%", NO_UNITS),
    ("1,5e1001", NO_UNITS),
    (",5", NO_UNITS),
    ("5,", NO_UNITS),
    (",", NO_UNITS),
    ("1,5,5", NO_UNITS),
    ("1,5/2", NO_UNITS),
    ("1,00", NO_UNITS),
    ("1,0000", NO_UNITS),
    ("1,5e3", NO_UNITS),
    ("1,5x10^3", NO_UNITS),
    ("1,5e3%", NO_UNITS),
    ("-0,5", NO_UNITS),
    ("£0,50", POUND),
    ("1,5 1/2", NO_UNITS),
    ("1,000,5", NO_UNITS),
    ("12,34", NO_UNITS),
    ("1,234", NO_UNITS),
    ("1,5 %", NO_UNITS),
    (",e5", NO_UNITS),
]


def fixed() -> list[tuple[str, tuple[str, ...]]]:
    """FIXED with each "~" written as each narrow space in turn."""
    return [(text.replace("~", s), units) for text, units in FIXED for s in (NARROW if "~" in text else ("~",))]


# Random cases: the pieces a typed number is made of, and the noise that breaks one.
SIGNS = ("", "", "", "", "-", "+", "- ", "\u2212", "\u2013", "\uff0d", "\u2212 ", "+ ")
UNIT_LISTS: tuple[tuple[str, ...], ...] = (
    NO_UNITS,
    NO_UNITS,
    NO_UNITS,
    POUND,
    ("%",),
    ("s", "ms"),
    ("bp", "%"),
    ("outcomes",),
    ("£", "$"),
    ("m", "km", "cm"),
    ("x",),
)
SPACES = ("", "", "", " ", "\t", "  ", *NARROW)
NOISE = (
    *"0123456789 ,./%eE+-x^*£s\t",
    *NARROW,
    "\u2212",
    "\u00d7",
    "\n",
    "\u3000",
    "10^",
    "1,000",
    "\U0001f600",
    "\u00a0000",
)


def _digits(rng: random.Random, lo: int, hi: int) -> str:
    return "".join(rng.choice("0123456789") for _ in range(rng.randint(lo, hi)))


def _integer_text(rng: random.Random) -> str:
    r = rng.random()
    if r < 0.5:
        return str(rng.randint(0, 10 ** rng.randint(1, 9)))
    if r < 0.6:
        return "0" * rng.randint(1, 3) + _digits(rng, 1, 4)
    sep = "," if r < 0.8 else rng.choice(NARROW)
    groups = (f"{rng.randint(0, 999):03d}" for _ in range(rng.randint(1, 3)))
    return str(rng.randint(1, 999)) + "".join(sep + g for g in groups)


def _mantissa(rng: random.Random) -> str:
    kind = rng.randrange(4)
    if kind == 0:
        return _integer_text(rng)
    if kind == 1:
        return f"{_integer_text(rng)}.{_digits(rng, 0, 6)}"
    if kind == 2:
        return f".{_digits(rng, 1, 6)}"
    return f"{_integer_text(rng)}."


def _exponent(rng: random.Random) -> str:
    mark = rng.choice(("e", "E", "x10^", " x 10^", "*10^", " * 10^", "\u00d710^", " \u00d7 10^", "X10^", "\u22c510^"))
    size = rng.choice((rng.randint(0, 30), rng.randint(990, 1010)))
    return mark + rng.choice(("", "", "+", "-", "\u2212")) + "0" * rng.choice((0, 0, 0, 2)) + str(size)


def _well_formed(rng: random.Random) -> str:
    shape = rng.randrange(6)
    if shape == 0:
        return _integer_text(rng)
    if shape == 1:
        return _mantissa(rng)
    if shape == 2:
        return f"{_integer_text(rng)}{rng.choice(SPACES)}/{rng.choice(SPACES)}{_integer_text(rng)}"
    if shape == 3:
        d = rng.randint(0, 60)
        return f"{_integer_text(rng)}{rng.choice(SPACES)} {rng.randint(0, d + 1)}/{d}"
    if shape == 4:
        return _mantissa(rng) + rng.choice(("%", " %", "\u00a0%"))
    return _mantissa(rng) + _exponent(rng)


def _mutate(rng: random.Random, text: str) -> str:
    for _ in range(rng.randint(1, 3)):
        i = rng.randint(0, len(text))
        op = rng.randrange(4)
        if op == 0:
            text = text[:i] + rng.choice(NOISE) + text[i:]
        elif op == 1:
            text = text[:i] + text[i + 1 :]
        elif op == 2:
            text = text[:i] + rng.choice(NOISE) + text[i + 1 :]
        else:
            text = text.replace(".", ",", 1) if rng.randrange(2) else text.replace(",", ".", 1)
    return text


def _random_case(rng: random.Random) -> tuple[str, tuple[str, ...]]:
    units = rng.choice(UNIT_LISTS)
    text = _well_formed(rng)
    if units and rng.random() < 0.6:
        unit = rng.choice(units)
        unit = unit.upper() if rng.random() < 0.2 else unit
        gap = rng.choice(("", " "))
        text = f"{unit}{gap}{text}" if rng.randrange(2) else f"{text}{gap}{unit}"
    text = rng.choice(SIGNS) + text
    if rng.random() < 0.15:
        text = rng.choice(SPACES) + text + rng.choice(("", " ", "\n", "\t", "\u202f"))
    if rng.random() < 0.35:
        text = _mutate(rng, text)
    if rng.random() < 0.03:
        text = text + " " * (MAX_LENGTH - len(code_units(text)) + rng.randint(-1, 1))
    return text, units


def cases() -> list[tuple[str, tuple[str, ...]]]:
    """Every golden case once, in a reproducible order."""
    rng = random.Random("zqverify.num_parse")
    drawn = fixed() + [_random_case(rng) for _ in range(RANDOM_CASES)]
    return list(dict.fromkeys(drawn))


def goldens() -> list[dict[str, object]]:
    return [{"in": text, "units": list(units), "out": out(parse(text, units))} for text, units in cases()]


def render() -> str:
    """JSON Lines: one case per line, so a changed case is a one-line diff."""
    return "".join(json.dumps(line) + "\n" for line in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
