"""Goldens for @zq/mathcore/rational: exact arithmetic on pairs of rationals, computed with `fractions.Fraction`.

The specification the TypeScript must meet, in plain words: a rational is kept in lowest terms with a positive
denominator; its canonical spelling is "n" for an integer and "n/d" otherwise, with an ASCII minus on n; sum,
difference, product, quotient and negation are exact, and division by zero is an error; comparison gives -1, 0
or 1, and two values are equal exactly when comparison gives 0; a value terminates when its denominator has no
prime factor but 2 and 5. Fraction is the independent twin of the arithmetic.

`parse` reads the spellings the TypeScript reads and refuses the rest. The refusals follow the grammar in the
decision notes of packages/mathcore/src/rational.ts and CONTENT-FORMAT.md 7.2: text with a "/" is a fraction,
"n/d" with an optional `-` on n, never `+`, and no sign on d; anything else is a decimal with an optional `-`,
a digit in the mantissa and an exponent of at most EXPONENT_LIMIT in size; ASCII digits only and nothing
around the number. The patterns below check that grammar before Fraction reads the text, because Fraction
alone also accepts `+`, surrounding whitespace, underscores and any exponent. A refusal is ValueError carrying
the TypeScript's RangeError message, and REFUSED lists each refused spelling with the message it must give.

A golden line's `kind` is one of:
- pair: operands `a` and `b` as spelled; `canonical` and `neg` of a; `add`, `sub`, `mul` and `div` (null when
  b is 0); `cmp`, `eq`, and `terminatesA` and `terminatesB`;
- refused: a `text` from REFUSED and the `error` message of the RangeError `parse` must throw.

Operands are drawn by `random.Random` seeded with the module name, so the file is reproducible. From the
repository root, rewrite it with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.rational
"""

from __future__ import annotations

import json
import math
import random
import re
from fractions import Fraction
from pathlib import Path

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "rational.golden.jsonl"
COUNT = 400
SAME = 60
EXPONENT_LIMIT = 1000

NUMERATOR = re.compile(r"-?[0-9]+")
DENOMINATOR = re.compile(r"[0-9]+")
SIGNED = re.compile(r"[-+][0-9]+")
DECIMAL = re.compile(r"-?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:[eE]([-+]?[0-9]+))?")

# Operand kinds for the random pairs, and their weights out of 50.
KINDS = ("integer", "fraction", "decimal", "leading dot", "trailing dot", "exponent", "near the limit")
WEIGHTS = (8, 8, 8, 6, 6, 13, 1)

# Hand-picked operands: the dot at either end, upper-case E, signed exponents and both ends of the limit.
FIXED = [
    ("0", "0"),
    ("-0", "5"),
    ("1/3", "-1/3"),
    ("0.1", "1/10"),
    ("-6/4", "3/2"),
    (".25", "1/4"),
    ("305.", "-.5"),
    ("1.e2", "100"),
    ("1E+3", "1000"),
    ("-0.0", "-0/5"),
    ("1e1000", "1e-1000"),
    ("-9.5E+999", ".5e-1000"),
    ("1e0001000", "7/3"),
    ("-1E-1000", "1.e-999"),
]

# Spellings `parse` refuses, each with the message of the RangeError the TypeScript throws.
REFUSED = {
    "": "not a decimal",
    ".": "not a decimal",
    "-": "not a decimal",
    "e5": "not a decimal",
    ".e5": "not a decimal",
    "1e": "not a decimal",
    "+1": "not a decimal",
    "- 1": "not a decimal",
    " 1": "not a decimal",
    "1\n": "not a decimal",
    "1,000": "not a decimal",
    "1_000": "not a decimal",
    "0x10": "not a decimal",
    "Infinity": "not a decimal",
    "\u22121": "not a decimal",  # a Unicode minus
    "\u0661": "not a decimal",  # an Arabic-Indic one
    "+1/2": "not a fraction",
    "1/2/3": "not a fraction",
    "1.5/2": "not a fraction",
    "1 /2": "not a fraction",
    "/2": "not a fraction",
    "1/": "not a fraction",
    "1/-2": "sign on the denominator",
    "1/+2": "sign on the denominator",
    "-1/-2": "sign on the denominator",
    "1/0": "division by zero",
    "0/0": "division by zero",
    "1e1001": "exponent beyond 1000",
    "1e-1001": "exponent beyond 1000",
    "0e+1001": "exponent beyond 1000",
    "1e" + "9" * 400: "exponent beyond 1000",  # beyond any double, so Number() gives Infinity
}


def spell(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def terminates(q: Fraction) -> bool:
    d = q.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


def parse(text: str) -> Fraction:
    """The value of a spelling the grammar accepts; otherwise ValueError with the TypeScript's message."""
    if "/" in text:
        n, _, d = text.partition("/")
        if NUMERATOR.fullmatch(n) is None or DENOMINATOR.fullmatch(d) is None:
            signed = NUMERATOR.fullmatch(n) is not None and SIGNED.fullmatch(d) is not None
            raise ValueError("sign on the denominator" if signed else "not a fraction")
        if int(d) == 0:
            raise ValueError("division by zero")
        return Fraction(int(n), int(d))
    m = DECIMAL.fullmatch(text)
    if m is None:
        raise ValueError("not a decimal")
    if m[1] is not None and abs(int(m[1])) > EXPONENT_LIMIT:
        raise ValueError(f"exponent beyond {EXPONENT_LIMIT}")
    return Fraction(text)


def operand(rng: random.Random) -> str:
    """An operand in one of the spellings `parse` accepts. One in 50 has an exponent within 10 of the limit:
    its value runs to about 1,000 digits in every column, so the other kinds keep the file small."""
    sign = rng.choice(["", "-"])
    e = f"{rng.choice('eE')}{rng.choice(['', '+', '-'])}"
    kind = rng.choices(KINDS, WEIGHTS)[0]
    if kind == "integer":
        return str(rng.randint(-(10**12), 10**12))
    if kind == "fraction":
        return f"{rng.randint(-(10**25), 10**25)}/{rng.randint(1, 10**18)}"
    if kind == "decimal":
        return f"{sign}{rng.randint(0, 99999)}.{rng.randint(0, 9999):04d}"
    if kind == "leading dot":
        return f"{sign}.{rng.randint(0, 99999):05d}"
    if kind == "trailing dot":
        return f"{sign}{rng.randint(0, 99999)}."
    if kind == "exponent":
        return f"{sign}{rng.randint(1, 999)}.{rng.randint(0, 99)}{e}{rng.randint(0, 30)}"
    return f"{sign}{rng.randint(1, 9)}{rng.choice(['', '.', '.5'])}{e}{rng.randint(990, 1000)}"


def twins(rng: random.Random) -> tuple[str, str]:
    """One value in two spellings, or two values whose canonical numerators are the same."""
    a = Fraction(rng.choice([-1, 1]) * rng.randint(1, 10**12), rng.randint(1, 10**12))
    k = rng.randint(2, 10**6)
    if rng.randrange(2):
        return spell(a), f"{a.numerator * k}/{a.denominator * k}"
    while math.gcd(k, a.numerator) != 1:
        k += 1
    return spell(a), f"{a.numerator}/{a.denominator * k}"


def case(a_text: str, b_text: str) -> dict[str, object]:
    a, b = parse(a_text), parse(b_text)
    return {
        "kind": "pair",
        "a": a_text,
        "b": b_text,
        "canonical": spell(a),
        "neg": spell(-a),
        "add": spell(a + b),
        "sub": spell(a - b),
        "mul": spell(a * b),
        "div": spell(a / b) if b else None,
        "cmp": (a > b) - (a < b),
        "eq": a == b,
        "terminatesA": terminates(a),
        "terminatesB": terminates(b),
    }


def goldens() -> list[dict[str, object]]:
    rng = random.Random("zqverify.rational")
    pairs = FIXED + [(operand(rng), operand(rng)) for _ in range(COUNT)] + [twins(rng) for _ in range(SAME)]
    refused = [{"kind": "refused", "text": text, "error": error} for text, error in REFUSED.items()]
    return [case(a, b) for a, b in pairs] + refused


def render() -> str:
    """JSON Lines: one case per line, so a changed case is a one-line diff."""
    return "".join(json.dumps(case) + "\n" for case in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
