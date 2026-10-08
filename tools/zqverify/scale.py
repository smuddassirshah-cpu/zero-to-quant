"""Goldens for @zq/mathcore/scale: ticks chosen exactly with Fraction, maps exactly (linear) or with mpmath (log).

The specification the TypeScript must meet, in plain words. A linear scale maps the domain [d0, d1] affinely
onto the range [r0, r1], and inverts; a log scale does the same in log x for a positive domain (the map is the
same in any base). Where the domain is one value every value maps to the middle of the range; where the range
is one value every value inverts to the middle of the domain, the geometric middle on a log scale.

Ticks for a count c, an integer from 1 to 1000, are doubles inside [lo, hi] (the domain's ends in increasing
order), increasing and without repeats; a one-valued domain has that value as its one tick. "The tick of q"
below is the double nearest the rational q, kept when it lies in [lo, hi].
- Linear: r = (hi - lo) / c exactly and p the integer with 10^p <= r < 10^(p+1). The step is 10^(p+1)
  if (r / 10^p)^2 >= 50, 5 * 10^p if it is at least 10, 2 * 10^p if at least 2, else 10^p. The ticks are the
  ticks of the step's integer multiples; if there are none and c is 1, they are the ticks for c = 2.
- Log: for the mantissa sets {1, ..., 9}, {1, 2, 5} and {1} in turn, the ticks of m * 10^p for m in the set
  and every integer p; the first set giving at most c ticks is used. If it gives fewer than c / 2, the linear
  ticks are used instead when the set is {1, ..., 9} or hi < 10 lo. If even {1} gives more than c, the ticks
  of the powers 10^p whose p is a multiple of s, for the least s in 2, 5, 10, 20, 50, ... that gives at most
  max(c, 2).

Maps are exact Fractions for the linear scale and mpmath at 50 digits for the log scale, each rounded once.
Cases are drawn by `random.Random` seeded with the module name. From the repository root, rewrite the file with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.scale
"""

from __future__ import annotations

import json
import math
import random
from collections.abc import Iterable, Iterator
from fractions import Fraction
from pathlib import Path

import mpmath as mp

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "scale.golden.jsonl"
TEN = Fraction(10)
FINEST = (1, 2, 3, 4, 5, 6, 7, 8, 9)
COUNTS = (1, 2, 3, 5, 7, 10, 12, 20, 30, 100)
OVERFLOW = Fraction(2**1024 - 2**970)  # the least magnitude that rounds to infinity
mp.mp.dps = 50


def rounded(q: Fraction) -> float:
    return (math.inf if q > 0 else -math.inf) if abs(q) >= OVERFLOW else float(q)


def decade(x: Fraction) -> int:
    """The integer p with 10^p <= x < 10^(p+1), for x > 0."""
    p = len(str(x.numerator)) - len(str(x.denominator))
    while TEN**p > x:
        p -= 1
    while TEN ** (p + 1) <= x:
        p += 1
    return p


def kept(lo: float, hi: float, qs: Iterable[Fraction]) -> list[float]:
    """The ticks of the increasing rationals qs, without repeats."""
    out: list[float] = []
    for t in map(rounded, qs):
        if lo <= t <= hi and (not out or t != out[-1]):
            out.append(t)
    return out


def linear_ticks(lo: float, hi: float, c: int) -> list[float]:
    if lo == hi:
        return [lo]
    r = (Fraction(hi) - Fraction(lo)) / c
    p = decade(r)
    m2 = (r / TEN**p) ** 2
    step = TEN ** (p + 1) if m2 >= 50 else (5 if m2 >= 10 else 2 if m2 >= 2 else 1) * TEN**p
    ks = range(math.floor(Fraction(lo) / step) - 1, math.ceil(Fraction(hi) / step) + 2)
    ticks = kept(lo, hi, (k * step for k in ks))
    return linear_ticks(lo, hi, 2) if not ticks and c == 1 else ticks


def nice() -> Iterator[int]:
    s = 1
    while True:
        yield from (2 * s, 5 * s, 10 * s)
        s *= 10


def log_ticks(lo: float, hi: float, c: int) -> list[float]:
    if lo == hi:
        return [lo]
    ps = range(decade(Fraction(lo)) - 1, decade(Fraction(hi)) + 2)
    for ms in (FINEST, (1, 2, 5), (1,)):
        ticks = kept(lo, hi, (m * TEN**p for p in ps for m in ms))
        if len(ticks) <= c:
            sparse = 2 * len(ticks) < c and (ms == FINEST or Fraction(hi) < 10 * Fraction(lo))
            return linear_ticks(lo, hi, c) if sparse else ticks
    powers = [p for p in ps if lo <= rounded(TEN**p) <= hi]
    s = next(s for s in nice() if sum(p % s == 0 for p in powers) <= max(c, 2))
    return [rounded(TEN**p) for p in powers if p % s == 0]


def linear(lo: float, hi: float, x: float, a: float, b: float) -> float:
    """The affine map taking [lo, hi] to [a, b], at x, exactly; the middle of [a, b] for a one-valued [lo, hi]."""
    t = Fraction(1, 2) if lo == hi else (Fraction(x) - Fraction(lo)) / (Fraction(hi) - Fraction(lo))
    return float(Fraction(a) + t * (Fraction(b) - Fraction(a)))


def log_map(d: tuple[float, float], r: tuple[float, float], x: float) -> float:
    l0, l1, lx = (mp.log(mp.mpf(v)) for v in (*d, x))
    t = mp.mpf(0.5) if d[0] == d[1] else (lx - l0) / (l1 - l0)
    return float(mp.mpf(r[0]) + t * (mp.mpf(r[1]) - mp.mpf(r[0])))


def log_invert(d: tuple[float, float], r: tuple[float, float], y: float) -> float:
    l0, l1 = (mp.log(mp.mpf(v)) for v in d)
    t = mp.mpf(0.5) if r[0] == r[1] else (mp.mpf(y) - r[0]) / (mp.mpf(r[1]) - r[0])
    return float(mp.exp(l0 + t * (l1 - l0)))


def inside(d0: float, d1: float, v: float) -> float:
    """d0 + (d1 - d0) v, with v kept to [0, 1] where extrapolating would overflow."""
    x = d0 + (d1 - d0) * v
    return x if math.isfinite(x - d0) and math.isfinite(x - d1) else d0 + (d1 - d0) * min(max(v, 0.0), 1.0)


def between(d0: float, d1: float, v: float) -> float:
    """d0 (d1 / d0)^v, kept to [1e-300, 1.7e308]."""
    x = mp.mpf(d0) * (mp.mpf(d1) / d0) ** v
    return float(min(max(x, mp.mpf("1e-300")), mp.mpf("1.7e308")))


def case(kind: str, d: tuple[float, float], r: tuple[float, float], c: int, rng: random.Random) -> dict[str, object]:
    """Ticks, and the maps of both ends and three draws a little beyond them, either way."""
    u = [rng.uniform(-0.2, 1.2) for _ in range(6)]
    if kind == "log":  # each invert a normal double: v kept to [0, 1] where extrapolating leaves them

        def fits(v: float) -> bool:
            return 1e-300 <= log_invert(d, r, r[0] + (r[1] - r[0]) * v) <= 1.7e308

        u[3:] = [v if fits(v) else min(max(v, 0.0), 1.0) for v in u[3:]]
    ys = [r[0], r[1], *(r[0] + (r[1] - r[0]) * v for v in u[3:])]
    if kind == "linear":
        xs = [d[0], d[1], *(inside(*d, v) for v in u[:3])]
        ticks = linear_ticks(min(d), max(d), c)
        maps, inverts = [linear(*d, x, *r) for x in xs], [linear(*r, y, *d) for y in ys]
    else:
        xs = [d[0], d[1], *(between(*d, v) for v in u[:3])]
        ticks = log_ticks(min(d), max(d), c)
        maps, inverts = [log_map(d, r, x) for x in xs], [log_invert(d, r, y) for y in ys]
    return {
        "kind": kind,
        "domain": d,
        "range": r,
        "count": c,
        "ticks": ticks,
        "x": xs,
        "map": maps,
        "y": ys,
        "invert": inverts,
    }


def linear_domain(rng: random.Random, c: int) -> tuple[float, float]:
    shape = rng.randrange(8)
    if shape == 0:
        return (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))
    if shape == 1:  # a large offset and a small span
        return (1e9 + rng.random() * 1e-3, 1e9 + rng.random() * 1e-3)
    if shape == 2:
        scale = 10 ** rng.uniform(-300, 300)
        return (rng.uniform(-1, 1) * scale, rng.uniform(-1, 1) * scale)
    if shape == 3:
        return (0.0, float(rng.choice((1, 7, 10, 24, 100, 365))))
    if shape == 4:
        v = rng.uniform(-5, 5)
        return (v, v)
    if shape == 5:  # (hi - lo) / c within a few ulps of sqrt 2, sqrt 10 or sqrt 50 times a power of ten
        span = float(mp.sqrt(rng.choice((2, 10, 50))) * mp.mpf(10) ** rng.randint(-40, 40) * c)
        lo = rng.choice((0.0, span * rng.uniform(-3, 3)))
        return (lo, math.nextafter(lo + span, rng.choice((-math.inf, math.inf)), steps=rng.randint(0, 3)))
    if shape == 6:  # subnormal spans
        return (rng.randint(-400, 400) * 5e-324, rng.randint(-400, 400) * 5e-324)
    a = rng.uniform(-1.5, 1.5) * 1e308  # ends near the largest doubles, with a finite span
    return (a, min(max(a + rng.uniform(-1.4, 1.4) * 1e308, -1.5e308), 1.5e308))


def log_domain(rng: random.Random) -> tuple[float, float]:
    shape = rng.randrange(7)
    if shape == 0:
        return (10 ** rng.uniform(-300, 300), 10 ** rng.uniform(-300, 300))
    if shape == 1:  # within about a decade
        a = 10 ** rng.uniform(-5, 5)
        return (a, a * rng.uniform(1.01, 12))
    if shape == 2:
        return (10.0 ** rng.randint(-6, 0), 10.0 ** rng.randint(1, 9))
    if shape == 3:
        v = 10 ** rng.uniform(-3, 3)
        return (v, v)
    if shape == 4:  # each end one ulp either side of a power of ten
        p = rng.randint(-300, 300)
        ps = (p, min(p + rng.choice((0, 1, 3, 8, 30, 120)), 307))
        a, b = (math.nextafter(float(f"1e{q}"), rng.choice((0.0, math.inf))) for q in ps)
        return (a, b)
    if shape == 5:  # narrow, far from 1
        a = 10 ** rng.uniform(-300, 300)
        return (a, rng.choice((math.nextafter(a, math.inf), a * (1 + 10 ** rng.uniform(-15, -9)))))
    return (10 ** rng.uniform(306, 307.5), 10 ** rng.uniform(306, 307.5))  # near the top, overflowing powers


def goldens() -> list[dict[str, object]]:
    rng = random.Random("zqverify.scale")
    ranges = ((0.0, 400.0), (300.0, 0.0), (-1.0, 1.0), (5.0, 5.0))
    out = []
    for kind in ("linear", "log"):
        for _ in range(200):
            r = rng.choice(ranges) if rng.random() < 0.7 else (rng.uniform(-1e3, 1e3), rng.uniform(-1e3, 1e3))
            c = rng.choice(COUNTS)
            d = linear_domain(rng, c) if kind == "linear" else log_domain(rng)
            out.append(case(kind, d, r, c, rng))
    return out


def render() -> str:
    """JSON Lines: one case per line, so a changed case is a one-line diff."""
    return "".join(json.dumps(c) + "\n" for c in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
