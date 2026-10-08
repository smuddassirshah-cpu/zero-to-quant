"""Goldens for @zq/mathcore/dmath (docs/PLAN.md stage 3): 10,000 inputs over the domains of exp, log, log1p,
expm1 and tanh, with references from mpmath at 50 significant digits.

Written from the functions' mathematical definitions and C99 Annex F (F.9), not from the TypeScript. Each
reference is mpmath's value at mp.dps = 50, rounded to the nearest double, ties to even, and stored with the
remainder (value - double) / ulp(double) in thousandths of an ulp, so the TypeScript test measures its error
against the 50-digit value, not against a rounded one. Special values (NaN, infinities, signed zeros, the
domain edges) come from Annex F through `special`, since mpmath has no signed zero.

Inputs are drawn by `random.Random` seeded with each function's name, so the file is reproducible. From the
repository root, rewrite it with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.dmath
"""

from __future__ import annotations

import math
import random
import struct
from collections.abc import Callable, Iterator
from fractions import Fraction
from pathlib import Path

import mpmath

GOLDENS = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "dmath.goldens.txt"
DPS = 50
COUNTS = {"exp": 2000, "log": 2000, "log1p": 2000, "expm1": 2000, "tanh": 2000}
INF = math.inf
NAN = math.nan
MAX = 1.7976931348623157e308
MIN_NORMAL = 2.2250738585072014e-308
TINY = 5e-324


def bits(x: float) -> int:
    return int.from_bytes(struct.pack(">d", x), "big")


def from_bits(b: int) -> float:
    return struct.unpack(">d", b.to_bytes(8, "big"))[0]


def ulp(x: float) -> Fraction:
    """The gap from |x| to the next double away from zero; 2^-1074 for zeros and subnormals."""
    if x == 0 or abs(x) < MIN_NORMAL:
        return Fraction(1, 1 << 1074)
    return Fraction(2) ** (math.frexp(x)[1] - 53)


def signed_man_exp(v: mpmath.mpf) -> tuple[int, int]:
    """(m, e) with v = m 2^e exactly; mpmath's man_exp drops the sign."""
    man, exp = v.man_exp
    return (-man if v < 0 else man), exp


def nearest(v: mpmath.mpf) -> float:
    """v rounded to the nearest double, ties to even: CPython's int true division rounds correctly."""
    if v == 0:
        return 0.0
    if mpmath.mag(v) > 1030:
        return math.copysign(INF, v)
    if mpmath.mag(v) < -1080:
        return math.copysign(0.0, v)
    man, exp = signed_man_exp(v)
    try:
        return float(man << exp) if exp >= 0 else man / (1 << -exp)
    except OverflowError:
        return math.copysign(INF, v)


# Constants from mpmath rather than the platform's libm, so the inputs, and the file, are the same everywhere.
with mpmath.workdps(30):
    LN2 = nearest(mpmath.log(2))
    LOG_MAX = nearest(mpmath.log(MAX))  # the largest x whose exp is finite, within an ulp


def special(name: str, x: float) -> float | None:
    """Annex F's value (F.9) where mpmath cannot give one; None for an ordinary input."""
    if math.isnan(x):
        return NAN
    if x == 0:
        return {"exp": 1.0, "log": -INF}.get(name, x)  # the others keep the zero's sign
    if math.isinf(x):
        positive = x > 0
        return {
            "exp": INF if positive else 0.0,
            "expm1": INF if positive else -1.0,
            "log": INF if positive else NAN,
            "log1p": INF if positive else NAN,
            "tanh": math.copysign(1.0, x),
        }[name]
    if name == "log" and x < 0:
        return NAN
    if name == "log1p" and x <= -1:
        return -INF if x == -1 else NAN
    return None


MP: dict[str, Callable[[mpmath.mpf], mpmath.mpf]] = {
    "exp": mpmath.exp,
    "log": mpmath.log,
    "log1p": mpmath.log1p,
    "expm1": mpmath.expm1,
    "tanh": mpmath.tanh,
}


def reference(name: str, args: tuple[float, ...], dps: int = DPS) -> tuple[float, int]:
    """(the correctly rounded double, the remainder in thousandths of its ulp) for name(*args)."""
    exact = special(name, args[0])
    if exact is not None:
        return exact, 0
    with mpmath.workdps(dps):
        v = MP[name](mpmath.mpf(args[0]))
        cr = nearest(v)
        if math.isinf(cr) or mpmath.mag(v) < -1090:  # beyond the doubles, or under 2^-16 ulp of zero
            return cr, 0
        man, exp = signed_man_exp(v)
        rem = (Fraction(man) * Fraction(2) ** exp - Fraction(cr)) / ulp(cr)
    return cr, round(rem * 1000)


def span(rng: random.Random, lo: int, hi: int) -> float:
    """A positive double with its binary exponent uniform in [lo, hi] and a random significand."""
    e = rng.randint(lo, hi)
    if e < -1022:  # subnormal: the leading bit at 2^e, the bits below it random
        k = e + 1074
        return from_bits((1 << k) | rng.getrandbits(k)) if k else TINY
    return math.ldexp(1 + rng.getrandbits(52) / (1 << 52), e)


def signed(rng: random.Random, x: float) -> float:
    return -x if rng.random() < 0.5 else x


def around(*centres: float, steps: int = 2) -> list[float]:
    """Each centre with its neighbours up to `steps` doubles either side."""
    out = []
    for c in centres:
        lo = hi = c
        for _ in range(steps):
            lo, hi = math.nextafter(lo, -INF), math.nextafter(hi, INF)
            out += [lo, hi]
        out.append(c)
    return out


EDGES = [0.0, -0.0, INF, -INF, NAN, TINY, -TINY, MIN_NORMAL, -MIN_NORMAL, MAX, -MAX, 1.0, -1.0]

def hard_cases(name: str) -> list[float]:
    """The domain edges and branch thresholds of each function, from its definition and IEEE-754 limits."""
    if name in ("exp", "expm1"):
        cases = around(LOG_MAX, -745.1332191019411, -708.3964185322641, 0.5 * LN2, 1.5 * LN2, 1023.5 * LN2)
        cases += around(2.0**-28, -(2.0**-28), 2.0**-54, -(2.0**-54), -56 * LN2, 56.5 * LN2, 19.5 * LN2)
        cases += around(-1021.5 * LN2)
        return cases + [-1000.0, 1000.0, -40.0, -38.0, 1e-300, -1e-300]
    if name == "log":
        cases = around(1.0, 2.0, 0.5, math.sqrt(2), math.sqrt(2) / 2, MIN_NORMAL, steps=3)
        return cases + [1 + 2.0**-20, 1 - 2.0**-20, 2.0**-1074, 2.0**-1050, -2.0, 1e-300, 1e300]
    if name == "log1p":
        cases = around(-1.0, math.sqrt(2) - 1, math.sqrt(2) / 2 - 1, 2.0**-29, 2.0**-54, -(2.0**-29), 2.0**53)
        return cases + [-0.5, 0.5, 1e300, -1e-300, 1e-300, -2.0]
    return around(22.0, -22.0, 1.0, -1.0, 2.0**-28, -(2.0**-28)) + [0.5, -0.5, 20.0, 1e300]  # tanh


def ordinary(name: str, rng: random.Random) -> float:
    """One input drawn over the function's domain, weighted towards the ranges its algorithm splits."""
    u = rng.random()
    if name in ("exp", "expm1"):
        if u < 0.6:
            return rng.uniform(-746.0 if name == "exp" else -45.0, 709.8)
        return signed(rng, span(rng, -60, 1))
    if name == "log":
        if u < 0.7:
            return span(rng, -1074, 1023)
        return 1 + signed(rng, span(rng, -52, -2))
    if name == "log1p":
        if u < 0.25:
            return -1 + span(rng, -53, -1)
        if u < 0.5:
            return signed(rng, span(rng, -1074, -20))
        return span(rng, -30, 1023) if u < 0.8 else signed(rng, span(rng, -30, -2))
    return signed(rng, span(rng, -40, 4))  # tanh


def cases() -> Iterator[tuple[str, list[tuple[float, ...]]]]:
    for name, count in COUNTS.items():
        rng = random.Random(f"dmath:{name}")
        inputs = EDGES + hard_cases(name)
        while len(inputs) < count:
            inputs.append(ordinary(name, rng))
        yield name, [(x,) for x in inputs[:count]]


HEADER = """\
# Goldens for @zq/mathcore/dmath, written by tools/zqverify/dmath.py (do not edit by hand).
# A line "@name" starts a function's cases. Each case is its argument(s) as IEEE-754 bits in hex, then the
# reference rounded to the nearest double (bits in hex), then (reference - that double) / ulp in thousandths.
# References: mpmath 1.3.0 at 50 significant digits; NaN, infinities and signed zeros from C99 Annex F.
"""


def render() -> str:
    lines = [HEADER.rstrip("\n")]
    for name, rows in cases():
        lines.append(f"@{name}")
        for args in rows:
            cr, rem = reference(name, args)
            lines.append(" ".join([*(f"{bits(a):016x}" for a in args), f"{bits(cr):016x}", str(rem)]))
    return "\n".join(lines) + "\n"


def main() -> None:
    GOLDENS.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
