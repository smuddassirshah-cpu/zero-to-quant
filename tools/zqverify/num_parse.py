"""Twin of @zq/mathcore/num-parse: how a typed answer reads as a number (docs/CONTENT-FORMAT.md 7.2).

Not yet independent of the TypeScript (CLAUDE.md hard rule 4). The session that wrote num-parse.ts wrote this
module after it, and the rules below restate that file's decided rules, so the goldens show that two copies of
one design agree, not that an independent reading of 7.2 agrees. The scanner is this module's own; the top-level
algorithm follows num-parse.ts step for step [measured: adversarial review of 8 October 2026]. Before the stage 3
gate a blind twin replaces it, written from 7.2 and a plain list of the decided rules by a session that has not
read num-parse.ts; it keeps EDGES below [unverified until then].

The rules this module implements:

1. Input over 200 UTF-16 code units fails as too-long. Normalise: U+2212 and the dashes U+2010 to U+2015, U+FE58,
   U+FE63 and U+FF0D become "-". A narrow space (U+00A0, U+2007, U+2009, U+200A, U+202F) is removed where it
   separates digit groups as a grouping comma would: a first group of 1 to 3 digits that does not start with 0
   and does not follow a digit, "." or ",", nor an exponent's "e", "E" or "^" with or without a sign after it
   ("3.2e1 000" does not group), then one or more times a narrow space and exactly 3 digits not followed by a
   digit. Every other narrow space is an ordinary space. U+00D7, U+00B7 and U+22C5 become "*"; runs of spaces
   and tabs become one space; ASCII whitespace is trimmed from the ends. Nothing left: empty. A grouping so
   spelled and then "/", after optional spaces, tabs or narrow spaces, is syntax: "2 125/250" typed with a
   no-break space reads both as the grouped 2125/250 and as the mixed 2 125/250, which differ. The test is the
   shape alone, so "12 345/7" (its mixed reading improper) and "1 000/0" are syntax too.
2. An optional leading "-" or "+", then an optional space. Then at most one listed unit, compared without case,
   longest first: at the start (then an optional space) or else at the end (after an optional space). With no
   unit, a final "%" (after an optional space) makes the form percent.
3. An integer is a run of ASCII digits, or a grouped run: 1 to 3 digits not starting with 0, then one or more
   groups of a comma and exactly 3 digits. The number is then one of:
   - mixed: integer, one space, integer, optional space, "/", optional space, integer; the numerator lies
     strictly between 0 and the denominator;
   - fraction: integer, optional space, "/", optional space, integer;
   - decimal: an optional integer, optionally "." and digits (at least one digit in all), then optionally an
     exponent: "e" or "E" and a signed integer, or an optional space, one of "*", "x", "X", an optional space,
     "10^" and a signed integer (standard form). An exponent beyond 1000 in size is out-of-range.
   A zero denominator is zero-denominator; a percent must be an integer or a decimal with no exponent.
4. Anything else is syntax, unless the text has exactly one comma and reads with that comma as a point, which
   is decimal-comma. A "-" negates the value; a percent's value is the number before its sign.
5. places: digits after the point as typed. figures: the digits typed, without commas or leading zeros. typed:
   for a fraction or a mixed number, its whole part (0 for a fraction), numerator and denominator as typed,
   unsigned and unreduced; otherwise null.

From the repository root, rewrite the golden file with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.num_parse
"""

from __future__ import annotations

import json
import random
from fractions import Fraction
from pathlib import Path

from zqverify.rational import spell

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "num-parse.golden.jsonl"
DIGITS = "0123456789"
TO_MINUS = "\u2010\u2011\u2012\u2013\u2014\u2015\u2212\uFE58\uFE63\uFF0D"
NARROW = "\u00A0\u2007\u2009\u200A\u202F"
TO_TIMES = "\u00D7\u00B7\u22C5"
SIGNS = "+-" + TO_MINUS


def starts_grouping(text: str, i: int) -> bool:
    """A grouping may start at i: a digit 1 to 9, not inside another number or an exponent (rule 1)."""
    before, sign_before = (text[i - 1] if i else " "), (text[i - 2] if i > 1 else " ")
    if before in SIGNS:
        return text[i] in DIGITS[1:] and sign_before not in "eE^"
    return text[i] in DIGITS[1:] and before not in DIGITS + ".,eE^"


def groupings(text: str) -> list[tuple[int, int]]:
    """Start and end of each digit grouping spelled with narrow spaces (rule 1)."""
    runs: list[tuple[int, int]] = []
    i = 0
    while i < len(text):
        if not starts_grouping(text, i):
            i += 1
            continue
        j = i
        while j < len(text) and text[j] in DIGITS:
            j += 1
        lead = j
        if j - i <= 3:
            while (
                j < len(text)
                and text[j] in NARROW
                and len(group := text[j + 1 : j + 4]) == 3
                and all(c in DIGITS for c in group)
                and (j + 4 == len(text) or text[j + 4] not in DIGITS)
            ):
                j += 4
        if j > lead:
            runs.append((i, j))
        i = j
    return runs


def grouped_before_slash(text: str) -> bool:
    """A grouping, then "/" after optional spaces, tabs or narrow spaces: syntax (rule 1)."""
    for _, end in groupings(text):
        while end < len(text) and text[end] in " \t" + NARROW:
            end += 1
        if text[end : end + 1] == "/":
            return True
    return False


def normalise(text: str) -> str:
    drop = {k for start, end in groupings(text) for k in range(start, end) if text[k] in NARROW}
    out = []
    for i, c in enumerate(text):
        if c in TO_MINUS:
            c = "-"
        elif i in drop:
            continue
        elif c in NARROW or c == "\t":
            c = " "
        elif c in TO_TIMES:
            c = "*"
        if not (c == " " and out and out[-1] == " "):
            out.append(c)
    return "".join(out).strip(" \t\n\r\v\f")


class Scan:
    def __init__(self, text: str) -> None:
        self.s, self.i = text, 0

    def peek(self, k: int = 0) -> str:
        return self.s[self.i + k] if self.i + k < len(self.s) else ""

    def take(self, c: str) -> bool:
        if self.s.startswith(c, self.i):
            self.i += len(c)
            return True
        return False

    def digits(self) -> str:
        j = self.i
        while self.peek() and self.peek() in DIGITS:
            self.i += 1
        return self.s[j : self.i]

    def integer(self) -> str | None:
        """Digits with grouping commas removed, or None when no digit is here."""
        run = self.digits()
        if not run:
            return None
        if len(run) <= 3 and run[0] != "0":
            while self.peek() == "," and all(self.peek(k) in DIGITS and self.peek(k) for k in (1, 2, 3)):
                if self.peek(4) and self.peek(4) in DIGITS:
                    break
                run += self.s[self.i + 1 : self.i + 4]
                self.i += 4
        return run

    def signed(self) -> int | None:
        sign = -1 if self.take("-") else 1
        if sign == 1:
            self.take("+")
        run = self.digits()
        return sign * int(run) if run else None

    def done(self) -> bool:
        return self.i == len(self.s)


def typed(whole: str, n: str, d: str) -> dict[str, str]:
    return {"whole": str(int(whole)), "n": str(int(n)), "d": str(int(d))}


def body(text: str, percent: bool) -> dict[str, object] | str:
    sc = Scan(text)
    first = sc.integer()
    if first is not None:
        at = sc.i
        if sc.take(" ") and (num := sc.integer()) is not None:
            sc.take(" ")
            if sc.take("/"):
                sc.take(" ")
                den = sc.integer()
                if den is not None and sc.done():
                    if percent:
                        return "syntax"
                    if int(den) == 0:
                        return "zero-denominator"
                    if not 0 < int(num) < int(den):
                        return "syntax"
                    value = int(first) + Fraction(int(num), int(den))
                    return {"form": "mixed", "value": value, "places": 0, "figures": 0,
                            "typed": typed(first, num, den)}
        sc.i = at
        sc.take(" ")
        if sc.take("/"):
            sc.take(" ")
            den = sc.integer()
            if den is None or not sc.done() or percent:
                return "syntax"
            if int(den) == 0:
                return "zero-denominator"
            value = Fraction(int(first), int(den))
            return {"form": "fraction", "value": value, "places": 0, "figures": 0,
                    "typed": typed("0", first, den)}
        sc.i = at
    whole = first or ""
    frac = sc.digits() if sc.take(".") else None
    if whole + (frac or "") == "":
        return "syntax"
    exp = None
    if sc.peek() in ("e", "E") and sc.peek():
        sc.i += 1
        exp = sc.signed()
        if exp is None:
            return "syntax"
    else:
        at = sc.i
        sc.take(" ")
        if sc.peek() and sc.peek() in "*xX":
            sc.i += 1
            sc.take(" ")
            if not sc.take("10^") or (exp := sc.signed()) is None:
                return "syntax"
        else:
            sc.i = at
    if not sc.done() or (percent and exp is not None):
        return "syntax"
    if exp is not None and abs(exp) > 1000:
        return "out-of-range"
    value = Fraction(int(whole + (frac or "") or "0"), 10 ** len(frac or "")) * Fraction(10) ** (exp or 0)
    form = "percent" if percent else "standard-form" if exp is not None else "integer" if frac is None else "decimal"
    figures = len((whole + (frac or "")).lstrip("0"))
    return {"form": form, "value": value, "places": len(frac or ""), "figures": figures, "typed": None}


def parse(raw: str, units: list[str]) -> dict[str, object]:
    if len(raw.encode("utf-16-le", "surrogatepass")) // 2 > 200:
        return {"ok": False, "reason": "too-long"}
    text = normalise(raw)
    if not text:
        return {"ok": False, "reason": "empty"}
    if grouped_before_slash(raw):
        return {"ok": False, "reason": "syntax"}
    sign = text[0] if text[0] in "+-" else ""
    rest = text[len(sign) :].removeprefix(" ") if sign else text
    unit = None
    for u in sorted((u for u in units if u), key=len, reverse=True):
        if rest[: len(u)].lower() == u.lower():
            rest = rest[len(u) :].removeprefix(" ")
        elif len(u) <= len(rest) and rest[-len(u) :].lower() == u.lower():
            rest = rest[: -len(u)].removesuffix(" ")
        else:
            continue
        unit = u
        break
    percent = unit is None and rest.endswith("%")
    if percent:
        rest = rest[:-1].removesuffix(" ")
    read = body(rest, percent)
    if read == "syntax" and rest.count(",") == 1 and not isinstance(body(rest.replace(",", "."), percent), str):
        read = "decimal-comma"
    if isinstance(read, str):
        return {"ok": False, "reason": read}
    value = -read["value"] if sign == "-" else read["value"]  # type: ignore[operator]
    return {"ok": True, **read, "value": spell(value), "unit": unit}


EDGES = [
    "11", "-3", "1,000", "0.25", ".25", "305.", "2/3", "-10 / 109", "2 1/3", "25%", "66.7 %", "3.2e5",
    "3.2 x 10^5", "3.2\u00D710^-3", "3.2\u00B710^4", "\u22125", "\u20135", "1\u202F000", "1\u00A0234.5", "0,5",
    "1,5", "12,34", "1,00", "0,500", "1,000,000", "12,345.678", "1234,567", "1,0001", "", "   ", "-", "--5",
    "+5", "abc", "1/0", "2 0/3", "2 4/3", "2 3/3", "0 1/2", "1e1000", "1e1001", "1e-1000", "2.5e+3", "3.2 e5",
    "10^5", "x10^5", "5.e3", "007", "0.0350", "1200", "1.20e3", "-0", "-.5", ".", "1.2.3", "1/2/3", "1 000",
    "1  /  2", "1\t1/2", "25 %", "-25%", "1/2%", "1e3%", "0,5%", "12,5e3", "\u00A312.50", "-\u00A35", "\u00A3-5",
    "12.50 \u00A3", "11 outcomes", "11 OUTCOMES", "250 bp", "250bp", "5 ms", "5s", "\u00A3", "% 5", "5%%",
    "\uFF15", "\u0665", "1\u00B2", "3.2 * 10^ 5", "3.2 *10^5", "3.2X10^5", "1e", "1e+", "4 1 / 2", "1,000/3",
    "1,000 1/2", "1" * 201, " 7 ", "7\n", "\n7",
    # Added after the adversarial review of 8 October 2026: signs, typed parts and narrow spaces.
    "+33.1%", "+ 5", "- 5", "\u2212 5", "+-5", "-+5", "++5", "+", "+\u00A35", "- \u00A35", "4/6", "2 2/4",
    "-4 / 6", "0/5", "2\u00A01/3", "1\u202F1/2", "2\u20091/3", "1\u00A0234\u00A0567", "12\u2009345.678",
    "0\u00A0500", "1\u00A02345", "1\u00A0000,5", "0.123\u2009456", "1234\u00A0567\u00A0890",
    "1\u00A0234 1/2", "-1\u202F000", "1\u00A0000\u00A0\u00A0000", "1,234\u00A0567", "3.2\u2009\u00D7\u200910^5",
    # Added after the review of b46c9e0: a narrow-space grouping before "/", and inside an exponent.
    "2\u00A0125/250", "1\u202F125/250", "3\u2009100/200", "2\u2007125/250", "2\u200A125/250", "12\u00A0345/7",
    "1\u00A0000 / 3", "1\u00A0000\u00A0/3", "1\u00A0000\t/3", "1\u00A0000/0", "-1\u00A0000/3", "\u22121\u00A0000/3",
    "1\u00A0000\u00A0000/7", "\u00A31\u00A0000/3", "3/1\u00A0000", "1\u00A0000\u00A01/2", "0\u00A0500/3",
    "3.2e1\u00A0000", "3.2E1\u00A0000", "1e-1\u00A0000", "1e+1\u00A0000", "1e\u22121\u00A0000", "3.2 x 10^1\u00A0000",
    "3.2\u00D710^\u22121\u202F000", "1e1\u00A0000/3", "5-1\u00A0000",
]
UNITS = [[], ["\u00A3"], ["bp", "%"], ["outcomes"], ["s", "ms"]]
PIECES = [
    "1", "2", "0", "7", "05", "123", ",", ".", " ", "/", "-", "e", "%", "\u00A3", "x", "^", "10", "\u2212",
    "\u00A0", "bp", "+", "\u2009",
]


def wellformed(rng: random.Random) -> str:
    """A number in one of the forms, with random signs, grouping, spacing and exponent spellings."""
    whole = rng.randint(0, 10 ** rng.randint(1, 10))
    grouped = f"{whole:,}".replace(",", rng.choice([",", ",", "\u00A0", "\u202F"]))
    head = rng.choice(["", "-", "\u2212", "+", "- ", "+ "]) + (grouped if rng.random() < 0.5 else str(whole))
    point = "." + str(rng.randint(0, 10 ** rng.randint(0, 6))) if rng.random() < 0.6 else ""
    den = rng.randint(0, 10**6)
    gap = rng.choice([" ", "\u00A0", "\u2009"])
    return rng.choice([
        head + point,
        head + point + rng.choice(["e", "E", " x 10^", "\u00d710^", " * 10^"]) + str(rng.randint(-40, 40)),
        head + point + rng.choice(["%", " %"]),
        head + rng.choice(["/", " / "]) + str(den),
        f"{head}{gap}{rng.randint(0, den)}/{den}",
    ])


def goldens() -> list[dict[str, object]]:
    rng = random.Random("zqverify.num_parse")
    inputs = [(text, units) for text in EDGES for units in UNITS[:1]]
    inputs += [(text, units) for text in EDGES for units in UNITS[1:] if any(u and u in text for u in units)]
    inputs += [(wellformed(rng), rng.choice(UNITS)) for _ in range(500)]
    for _ in range(1500):
        text = "".join(rng.choice(PIECES) for _ in range(rng.randint(1, 8)))
        inputs.append((text, rng.choice(UNITS)))
    return [{"in": text, "units": units, "out": parse(text, units)} for text, units in inputs]


def render() -> str:
    """JSON Lines: one case per line, so a changed case is a one-line diff."""
    return "".join(json.dumps(case) + "\n" for case in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
