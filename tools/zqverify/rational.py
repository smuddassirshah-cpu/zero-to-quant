"""Goldens for @zq/mathcore/rational: exact arithmetic on pairs of rationals, computed with `fractions.Fraction`.

The specification the TypeScript must meet, in plain words: a rational is kept in lowest terms with a positive
denominator; its canonical spelling is "n" for an integer and "n/d" otherwise, with an ASCII minus on n; sum,
difference, product and quotient are exact, and division by zero is an error; comparison gives -1, 0 or 1; a
value terminates when its denominator has no prime factor but 2 and 5. Fraction is the independent twin.

Operands are drawn by `random.Random` seeded with the module name, so the file is reproducible. From the
repository root, rewrite it with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.rational
"""

from __future__ import annotations

import json
import random
from fractions import Fraction
from pathlib import Path

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "rational.golden.jsonl"
COUNT = 400


def spell(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def terminates(q: Fraction) -> bool:
    d = q.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def operand(rng: random.Random) -> str:
    """An operand in one of the spellings `parse` accepts: an integer, "n/d" or a decimal with an exponent."""
    kind = rng.randrange(4)
    if kind == 0:
        return str(rng.randint(-(10**12), 10**12))
    if kind == 1:
        return f"{rng.randint(-(10**25), 10**25)}/{rng.randint(1, 10**18)}"
    if kind == 2:
        return f"{rng.choice(['', '-'])}{rng.randint(0, 99999)}.{rng.randint(0, 9999):04d}"
    return f"{rng.choice(['', '-'])}{rng.randint(1, 999)}.{rng.randint(0, 99)}e{rng.randint(-30, 30)}"


def parse(text: str) -> Fraction:
    """Fraction reads all three spellings, "1.5e-3" included."""
    return Fraction(text)


def case(a_text: str, b_text: str) -> dict[str, object]:
    a, b = parse(a_text), parse(b_text)
    return {
        "a": a_text,
        "b": b_text,
        "canonical": spell(a),
        "add": spell(a + b),
        "sub": spell(a - b),
        "mul": spell(a * b),
        "div": spell(a / b) if b else None,
        "cmp": (a > b) - (a < b),
        "terminates": terminates(a),
    }


def goldens() -> list[dict[str, object]]:
    rng = random.Random("zqverify.rational")
    pairs = [("0", "0"), ("-0", "5"), ("1/3", "-1/3"), ("0.1", "1/10"), ("-6/4", "3/2")]
    pairs += [(operand(rng), operand(rng)) for _ in range(COUNT)]
    return [case(a, b) for a, b in pairs]


def render() -> str:
    """JSON Lines: one case per line, so a changed case is a one-line diff."""
    return "".join(json.dumps(case) + "\n" for case in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
