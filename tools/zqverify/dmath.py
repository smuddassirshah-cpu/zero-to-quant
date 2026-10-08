"""Goldens for @zq/mathcore/dmath (docs/PLAN.md stage 3): 10,000 inputs over the domains of exp, log, log1p,
expm1, tanh, pow, sin and cos, with references from mpmath at 50 significant digits.

Written from the functions' mathematical definitions and C99 Annex F (F.9), not from the TypeScript; the
hard cases add fdlibm's branch thresholds, read from the C reference the TypeScript ports. Each reference is
mpmath's value at mp.dps = 50, rounded to the nearest double, ties to even, and stored with the remainder
(value - double) / ulp(double) in thousandths of an ulp, so the TypeScript test measures its error against
the 50-digit value, not against a rounded one. Special values (NaN, infinities, signed zeros, the domain
edges) come from Annex F through `special` and `pow_special`, since mpmath has no signed zero.

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
COUNTS = {
    "exp": 1250,
    "log": 1250,
    "log1p": 1250,
    "expm1": 1250,
    "tanh": 1000,
    "pow": 1500,
    "sin": 1250,
    "cos": 1250,
}
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


def log2(x: float) -> float:
    """log2(x) from mpmath, for drawing inputs the same way on every platform."""
    return float(mpmath.log(x, 2))


def special(name: str, x: float) -> float | None:
    """Annex F's value (F.9) where mpmath cannot give one; None for an ordinary input."""
    if math.isnan(x):
        return NAN
    if x == 0:
        return {"exp": 1.0, "cos": 1.0, "log": -INF}.get(name, x)  # the others keep the zero's sign
    if math.isinf(x):
        positive = x > 0
        return {
            "exp": INF if positive else 0.0,
            "expm1": INF if positive else -1.0,
            "log": INF if positive else NAN,
            "log1p": INF if positive else NAN,
            "tanh": math.copysign(1.0, x),
        }.get(name, NAN)
    if name == "log" and x < 0:
        return NAN
    if name == "log1p" and x <= -1:
        return -INF if x == -1 else NAN
    return None


def pow_special(x: float, y: float) -> float | None:
    """Annex F.9.4.4 for pow, in its order; None when x^y is an ordinary real number."""
    if y == 0 or x == 1:
        return 1.0
    if math.isnan(x) or math.isnan(y):
        return NAN
    odd = math.isfinite(y) and y == math.floor(y) and y % 2 == 1
    if x == 0:
        return (math.copysign(INF, x) if odd else INF) if y < 0 else (x if odd else 0.0)
    if math.isinf(y):
        if x == -1:
            return 1.0
        return (INF if y < 0 else 0.0) if abs(x) < 1 else (0.0 if y < 0 else INF)
    if math.isinf(x):
        if x < 0:
            return (-0.0 if odd else 0.0) if y < 0 else (-INF if odd else INF)
        return 0.0 if y < 0 else INF
    if x < 0 and y != math.floor(y):
        return NAN
    return None


MP: dict[str, Callable[[mpmath.mpf], mpmath.mpf]] = {
    "exp": mpmath.exp,
    "log": mpmath.log,
    "log1p": mpmath.log1p,
    "expm1": mpmath.expm1,
    "tanh": mpmath.tanh,
    "sin": mpmath.sin,
    "cos": mpmath.cos,
}


def reference(name: str, args: tuple[float, ...], dps: int = DPS) -> tuple[float, int]:
    """(the correctly rounded double, the remainder in thousandths of its ulp) for name(*args)."""
    exact = pow_special(*args) if name == "pow" else special(name, args[0])
    if exact is not None:
        return exact, 0
    with mpmath.workdps(dps):
        if name == "pow":
            x, y = args
            # A negative base reaches here only with an integer exponent: the sign is the exponent's parity.
            sign = -1 if x < 0 and y % 2 == 1 else 1
            v = sign * mpmath.power(mpmath.mpf(abs(x)), mpmath.mpf(y))
        else:
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
# Within 4.7e-19, about 2^-61, of a multiple of pi/2 (its cosine is -4.687e-19 [measured: mpmath]): the
# hardest double for argument reduction [recalled: K. C. Ng, "Argument reduction for huge arguments: good to
# the last bit", Sun Microsystems, 1992].
NG_WORST = 6381956970095103 * 2.0**797


def switch(*high_words: int) -> list[float]:
    """The first double whose high word is each of these, with its negation: fdlibm tests the high word, so
    this double and the one below it fall on either side of the branch."""
    return [s * from_bits(h << 32) for h in high_words for s in (1.0, -1.0)]


def hard_cases(name: str) -> list[float]:
    """IEEE-754 limits and each function's domain edges, plus fdlibm's branch thresholds taken from the C
    reference [our choice]: a threshold on the high word is centred by `switch`, one on a value by its
    neighbours."""
    if name in ("exp", "expm1"):
        cases = around(LOG_MAX, -745.1332191019411, -708.3964185322641, 1023.5 * LN2, -1021.5 * LN2)
        cases += around(2.0**-28, -(2.0**-28), 2.0**-54, -(2.0**-54), -56 * LN2, 56.5 * LN2, 19.5 * LN2)
        cases += around(*switch(0x3FD62E43, 0x3FF0A2B2, 0x4043687A, 0x40862E42))
        return cases + [-1000.0, 1000.0, -40.0, -38.0, 1e-300, -1e-300]
    if name == "log":
        cases = around(1.0, 2.0, 0.5, math.sqrt(2), math.sqrt(2) / 2, MIN_NORMAL, steps=3)
        # The reduction's split near sqrt(2), in two binades, and the two switches between e_log.c's final forms.
        cases += around(*(from_bits(h << 32) for h in (0x3FF6A09C, 0x3FE6A09C, 0x3FF6147A, 0x4006B852)))
        return cases + [1 + 2.0**-20, 1 - 2.0**-20, 2.0**-1074, 2.0**-1050, -2.0, 1e-300, 1e300]
    if name == "log1p":
        cases = around(-1.0, math.sqrt(2) - 1, math.sqrt(2) / 2 - 1, 2.0**-29, 2.0**-54, -(2.0**-29), 2.0**53)
        cases += around(from_bits(0x3FDA827A << 32), -from_bits(0x3FD2BEC5 << 32))
        # 1 + x crosses the reduction's split near sqrt(2) 2^k at k = 1 and k = 2 (the differences are exact);
        # below k = 1 the split lies inside the unreduced range.
        cases += around(from_bits(0x4006A09E << 32) - 1, from_bits(0x4016A09E << 32) - 1)
        return cases + [-0.5, 0.5, 1e300, -1e-300, 1e-300, -2.0]
    if name == "tanh":
        return around(22.0, -22.0, 1.0, -1.0, 2.0**-28, -(2.0**-28)) + [0.5, -0.5, 20.0, 1e300]
    # sin, cos: the doubles nearest k pi/2, for small k and for k near 2^20, where the medium reduction ends
    with mpmath.workdps(60):
        ks = (1, 2, 3, 4, 5, 6, 7, 8, 9, 100, 2**19, 2**20 - 1, 2**20)
        near = [float(mpmath.mpf(k) * mpmath.pi / 2) for k in ks]
    cases = around(*near, *(-x for x in near), math.pi / 4, 2.0**-26, 2.0**-27 * math.sqrt(2), steps=1)
    return cases + [NG_WORST, -NG_WORST, 2.0**1023, 1e22, 1e300, 2.0**-1074]


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
    if name == "tanh":
        return signed(rng, span(rng, -40, 4))
    # sin, cos
    if u < 0.25:
        return rng.uniform(-10.0, 10.0)
    return signed(rng, span(rng, -30, 21) if u < 0.6 else span(rng, 20, 1023))


def pow_cases(rng: random.Random, count: int) -> list[tuple[float, float]]:
    vals = [0.0, -0.0, 1.0, -1.0, 0.5, -0.5, 2.0, -2.0, 3.0, -3.0, INF, -INF, NAN, TINY, -TINY]
    cases = [(x, y) for x in vals for y in vals]  # Annex F's grid: every pair of these values
    cases += [(2.0, y) for y in around(1024.0, -1074.0, -1075.0, -1022.0)] + [(0.5, 1074.5), (0.5, -1023.9)]
    cases += [(3.0, 34.0), (10.0, 22.0), (10.0, -5.0), (7.0, 1 / 3), (TINY, 0.5), (TINY, -0.01), (MAX, 0.999)]
    cases += [(1 + s * 2.0**-30, t * 2.0**k) for s in (1, -1) for t in (1, -1) for k in (31.5, 40, 65)]
    cases += [(-(1 + 2.0**-40), 2.0**40 + y) for y in (0.0, 1.0, 3.0)] + [(-1.5, 2.0**21 + 1), (-2.0, 1023.0)]
    cases += [(-1.5, y) for y in (1.5, -2.5, 1.1, 2.0**21 + 0.5, 3e6 + 0.25)]  # y not an integer: NaN
    # y log2(x) within 2.5e-16 of 1024 or -1075, so it rounds onto the overflow and underflow edges of 2^z
    # while x^y stays finite and non-zero (found by a search with mpmath at 60 digits).
    edges = "1.cb4b7e363bae9p+911 1.1f7ced916872bp+0 1.429572206c388p+604 1.b1c61223b1974p+0 "
    edges += "1.44e9a0fe9dff0p+557 1.d6585b4843e06p+0 1.18fefb2d7209ep+517 1.faeaa46cd6299p+0 "
    edges += "1.13beac19259c4p+763 -1.68a17fda8d050p+0 1.12cd3c0569130p+585 -1.d6585b4843e06p+0 "
    edges += "1.485002aaffb3dp+506 -1.0fbe76c8b4396p+1 1.3a57492f8c705p+446 -1.3450bfed46828p+1"
    hexes = [float.fromhex(h) for h in edges.split()]
    cases += list(zip(hexes[::2], hexes[1::2]))
    # e_pow.c's branch for |y| > 2^31: x within 2^-21 of 1 with a full significand, 2^31 < |y| < 2^34 and
    # |y log2(x)| <= 1000, so x^y is a normal double. Drawn by a generator of their own, so the draws below
    # do not move.
    near, start = random.Random("dmath:pow:near-one"), len(cases)
    while len(cases) < start + 64:
        x = 1 + signed(near, span(near, -32, -22))
        top = min(2.0**34, 1000 / abs(log2(x)))
        if top > 2.0**31:
            cases.append((x, signed(near, near.uniform(2.0**31, top))))
    while len(cases) < count:
        u = rng.random()
        x = span(rng, -1074, 1023)
        if u < 0.15:
            x = 1 + signed(rng, span(rng, -40, -2))
            y = signed(rng, span(rng, 0, 45))
        elif u < 0.3:
            # A negative base with an integer exponent, odd or even, with a finite result.
            x = -span(rng, -60, 60)
            limit = max(1, int(1000 / max(abs(log2(-x)), 1e-9)))
            y = float(rng.randint(-min(limit, 2**52), min(limit, 2**52)))
        else:
            # The result's binary exponent uniform over the finite and subnormal range, spilling either side.
            if x == 1:
                continue
            y = rng.uniform(-1090.0, 1035.0) / log2(x)
        cases.append((x, y))
    return cases[:count]


def cases() -> Iterator[tuple[str, list[tuple[float, ...]]]]:
    for name, count in COUNTS.items():
        rng = random.Random(f"dmath:{name}")
        if name == "pow":
            yield name, list(pow_cases(rng, count))
            continue
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
