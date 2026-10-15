"""Twin of @zq/mathcore/scale and writer of its goldens, from docs/ARCHITECTURE.md 5.16 alone.

Written by unit ST without reading the TypeScript, its tests or the module this file replaces (CLAUDE.md hard
rule 4; docs/DECISIONS.md B51 and B54). Where this file and the TypeScript disagree, 5.16 decides. Every result
here is 5.16's reference, not the TypeScript's arithmetic: the exact value rounded once.

The rules:
- `linear_scale([d0, d1], [r0, r1])` maps the domain affinely onto the range; `log_scale` does so in ln x over a
  positive domain. Every end and each side's span (d1 - d0 and r1 - r0 in doubles) must be finite and a log
  domain's ends positive, else RangeError. `map` and `invert` take finite values only, a log `map` positive
  ones only. A one-valued domain maps everything to the middle of the range; a one-valued range inverts
  everything to the middle of the domain, the geometric middle on a log scale; a log scale with a one-valued
  domain inverts to it.
- map(x) = r0 + (r1 - r0) t with t = (x - d0) / (d1 - d0), or ln(x / d0) / ln(d1 / d0) on a log scale; invert is
  the inverse of the same map. Linear results are exact Fractions rounded once; log results take ln and exp
  from mpmath at 50 digits, rounded once from the exact value of the mpf, so +-inf beyond the doubles and 0
  below half the least subnormal. A log t that is a rational a / b with b <= 64 is found and proved exactly
  ((x / d0)^b = (d1 / d0)^a), so a map that is exactly zero, such as 10 on [1, 100] -> [-1, 1], is 0.
- ticks(c), c an integer from 1 to 1,000: with lo <= hi the domain's ends, "the tick of q" is the double nearest
  the rational q, kept when it lies in [lo, hi], and ticks of distinct q on one double count once. Linear: r =
  (hi - lo) / c exactly, 10^p <= r < 10^(p + 1), step 10^(p + 1), 5 10^p, 2 10^p or 10^p as (r / 10^p)^2 is at
  least 50, 10 or 2 or less; the ticks of the step's integer multiples; none with c = 1 takes c = 2. Log: the
  first of the mantissa sets {1..9}, {1, 2, 5}, {1} whose ticks of m 10^p number at most c; fewer than c / 2
  from {1..9}, or from a domain narrower than a decade (hi < 10 lo), gives the linear ticks for c instead; if
  {1} gives more than c, the powers 10^p with p a multiple of the least s in 2, 5, 10, 20, 50, ... that gives at
  most max(c, 2). A one-valued domain has its value as its one tick.

A golden line (packages/mathcore/test/scale.golden.jsonl) holds `kind`, `domain`, `range`, `count`, `ticks`, and
the lists `x` with `map` and `y` with `invert`: each result the exact value rounded once, or null where the
scale refuses the value; a non-finite number is the string Number reads back ("Infinity", "-Infinity", "NaN").
Scales are FIXED, each with its reason, then drawn by `random.Random` seeded with the module name. From the
repository root:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.scale
"""

from __future__ import annotations

import json
import math
import random
from collections.abc import Callable, Iterable, Iterator, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Literal

import mpmath

from zqverify.stats import MAX, RangeError, nearest, sqrt_nearest

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "scale.golden.jsonl"
DIGITS = 50
COUNT_LIMIT = 1000
NINE = (1, 2, 3, 4, 5, 6, 7, 8, 9)
MANTISSAS = (NINE, (1, 2, 5), (1,))
HALF = Fraction(1, 2)

Kind = Literal["linear", "log"]


def pow10(p: int) -> Fraction:
    return Fraction(10**p) if p >= 0 else Fraction(1, 10**-p)


def decade(r: Fraction) -> int:
    """The integer p with 10^p <= r < 10^(p + 1), for r > 0."""
    p = len(str(r.numerator)) - len(str(r.denominator))
    while pow10(p) > r:
        p -= 1
    while pow10(p + 1) <= r:
        p += 1
    return p


def mp_fraction(v: mpmath.mpf) -> Fraction:
    """The exact value of an mpf. Callers keep it within the doubles' exponents, or 2^exp grows without bound."""
    man, exp = v.man_exp  # man_exp drops the sign [measured: mpmath 1.3.0, mpf(-1.5).man_exp is (3, -1)]
    man = -man if v < 0 else man
    return Fraction(man << exp) if exp >= 0 else Fraction(man, 1 << -exp)


def _ends(ends: Iterable[float], what: str) -> tuple[float, float]:
    a, b = (float(v) for v in ends)
    if not (math.isfinite(a) and math.isfinite(b)):
        raise RangeError(f"the {what}'s ends must be finite")
    if not math.isfinite(b - a):
        raise RangeError(f"the {what}'s span must be finite")
    return a, b


def _count(count: int | float) -> int:
    if isinstance(count, bool) or not isinstance(count, int | float):
        raise TypeError("the count must be a number")
    if isinstance(count, float) and not (math.isfinite(count) and count.is_integer()):
        raise RangeError("the count must be an integer from 1 to 1000")
    if not 1 <= count <= COUNT_LIMIT:
        raise RangeError("the count must be an integer from 1 to 1000")
    return int(count)


# --- ticks ---------------------------------------------------------------------------------------------------


def _multiples(step: Fraction, lo: float, hi: float) -> list[float]:
    """The ticks of step's integer multiples: the doubles nearest k * step that lie in [lo, hi], once each.

    Rounding is monotone, so the kept k are consecutive. From the least k with k * step >= lo, walk down while
    a smaller multiple still rounds into the range: at most about 1.6c steps, since lo's spacing is at most
    twice the gap to the next double and that gap is at most hi - lo [inferred].
    """
    k = math.ceil(Fraction(lo) / step)
    while nearest((k - 1) * step) >= lo:
        k -= 1
    out: list[float] = []
    while (v := nearest(k * step)) <= hi:
        if not out or v != out[-1]:
            out.append(v)
        k += 1
    return out


def linear_step(lo: float, hi: float, count: int) -> Fraction:
    r = (Fraction(hi) - Fraction(lo)) / count
    p = decade(r)
    e2 = (r / pow10(p)) ** 2
    if e2 >= 50:
        return pow10(p + 1)
    if e2 >= 10:
        return 5 * pow10(p)
    if e2 >= 2:
        return 2 * pow10(p)
    return pow10(p)


def linear_ticks(lo: float, hi: float, count: int) -> list[float]:
    """5.16's linear ticks for lo < hi."""
    ticks = _multiples(linear_step(lo, hi, count), lo, hi)
    return linear_ticks(lo, hi, 2) if not ticks and count == 1 else ticks


def _kept(qs: Iterator[Fraction], lo: float, hi: float) -> list[float]:
    return sorted({v for v in map(nearest, qs) if lo <= v <= hi})


def _one_two_five() -> Iterator[int]:
    scale = 1
    while True:
        yield from (2 * scale, 5 * scale, 10 * scale)
        scale *= 10


def log_ticks(lo: float, hi: float, count: int) -> list[float]:
    """5.16's log ticks for 0 < lo < hi."""
    low, high = Fraction(lo), Fraction(hi)
    powers = range(decade(low) - 1, decade(high) + 2)
    for mantissas in MANTISSAS:
        ticks = _kept((m * pow10(p) for p in powers for m in mantissas), lo, hi)
        if len(ticks) <= count:
            if 2 * len(ticks) < count and (mantissas is NINE or high < 10 * low):
                return linear_ticks(lo, hi, count)
            return ticks
    for s in _one_two_five():
        ticks = _kept((pow10(p) for p in powers if p % s == 0), lo, hi)
        if len(ticks) <= max(count, 2):
            return ticks
    raise AssertionError("unreachable: some s leaves at most one power")


# --- the scale -----------------------------------------------------------------------------------------------


class Scale:
    def __init__(self, kind: Kind, domain: Iterable[float], range_: Iterable[float]) -> None:
        self.kind = kind
        self.domain = _ends(domain, "domain")
        self.range = _ends(range_, "range")
        if kind == "log" and not (self.domain[0] > 0 and self.domain[1] > 0):
            raise RangeError("a log domain's ends must be positive")

    def _t_log(self, x: float) -> Fraction:
        d0, d1 = self.domain
        with mpmath.workdps(DIGITS):
            num = mpmath.log(mpmath.mpf(x) / mpmath.mpf(d0))
            den = mpmath.log(mpmath.mpf(d1) / mpmath.mpf(d0))
            t = num / den  # num and den are the same mpf at x = d1, so t is exactly 1 there
        approx = mp_fraction(t)
        guess = approx.limit_denominator(64)
        a, b = guess.numerator, guess.denominator
        close = abs(approx - guess) < Fraction(1, 10**40) and abs(a) <= 256
        if close and (Fraction(x) / Fraction(d0)) ** b == (Fraction(d1) / Fraction(d0)) ** a:
            return guess
        return approx

    def map(self, x: float) -> float:
        x = float(x)
        if not math.isfinite(x):
            raise RangeError("map takes a finite value")
        if self.kind == "log" and not x > 0:
            raise RangeError("a log scale maps positive values only")
        (d0, d1), (r0, r1) = self.domain, self.range
        if d0 == d1:
            return nearest((Fraction(r0) + Fraction(r1)) / 2)
        if self.kind == "linear":
            t = (Fraction(x) - Fraction(d0)) / (Fraction(d1) - Fraction(d0))
        else:
            t = self._t_log(x)
        return nearest(Fraction(r0) + (Fraction(r1) - Fraction(r0)) * t)

    def _log_point(self, t: Fraction) -> float:
        """d0 (d1 / d0)^t: from d0 for t < 1/2 and from d1 otherwise, so both ends come back exactly."""
        d0, d1 = self.domain
        base, a = (d0, t) if t < HALF else (d1, t - 1)
        with mpmath.workdps(DIGITS):
            e = mpmath.mpf(a.numerator) / a.denominator * mpmath.log(mpmath.mpf(d1) / mpmath.mpf(d0))
            ln_value = mpmath.log(mpmath.mpf(base)) + e
            if ln_value > 710:  # ln MAX is 709.78
                return math.inf
            if ln_value < -746:  # ln 2^-1075 is -745.13
                return 0.0
            value = mpmath.mpf(base) * mpmath.exp(e)
        return nearest(mp_fraction(value))

    def invert(self, y: float) -> float:
        y = float(y)
        if not math.isfinite(y):
            raise RangeError("invert takes a finite value")
        (d0, d1), (r0, r1) = self.domain, self.range
        if self.kind == "log" and d0 == d1:
            return d0
        if r0 == r1:
            if self.kind == "log":
                return sqrt_nearest(Fraction(d0) * Fraction(d1))
            return nearest((Fraction(d0) + Fraction(d1)) / 2)
        t = (Fraction(y) - Fraction(r0)) / (Fraction(r1) - Fraction(r0))
        if self.kind == "log":
            return self._log_point(t)
        return nearest(Fraction(d0) + (Fraction(d1) - Fraction(d0)) * t)

    def ticks(self, count: int | float) -> list[float]:
        c = _count(count)
        d0, d1 = self.domain
        if d0 == d1:
            return [d0]
        lo, hi = min(d0, d1), max(d0, d1)
        return linear_ticks(lo, hi, c) if self.kind == "linear" else log_ticks(lo, hi, c)


def linear_scale(domain: Iterable[float], range_: Iterable[float]) -> Scale:
    return Scale("linear", domain, range_)


def log_scale(domain: Iterable[float], range_: Iterable[float]) -> Scale:
    """The TypeScript takes { log, exp }; the twin's references need neither, so it takes none."""
    return Scale("log", domain, range_)


# --- goldens -------------------------------------------------------------------------------------------------


def encode(v: float | None) -> float | str | None:
    if v is None or math.isfinite(v):
        return v
    return "NaN" if math.isnan(v) else "Infinity" if v > 0 else "-Infinity"


def decode(v: float | str | None) -> float | None:
    return float(v) if isinstance(v, str) else v


def _result(f: Callable[[float], float], v: float) -> float | None:
    try:
        return f(v)
    except RangeError:
        return None


def case(kind: Kind, domain: Sequence[float], range_: Sequence[float], count: int,
         xs: Sequence[float], ys: Sequence[float]) -> dict[str, object]:
    s = Scale(kind, domain, range_)
    return {
        "kind": kind,
        "domain": [float(v) for v in domain],
        "range": [float(v) for v in range_],
        "count": count,
        "ticks": s.ticks(count),
        "x": [encode(float(x)) for x in xs],
        "map": [encode(_result(s.map, x)) for x in xs],
        "y": [encode(float(y)) for y in ys],
        "invert": [encode(_result(s.invert, y)) for y in ys],
    }


INF, NAN = math.inf, math.nan
REFUSED = (NAN, INF, -INF)
FIXED: list[tuple[str, Kind, tuple[float, float], tuple[float, float], int, list[float], list[float]]] = [
    ("tenths: the tick of 3/10 is 0.3", "linear", (0, 1), (0, 100), 10,
     [0, 1, 0.5, 0.3, -2, 7, *REFUSED], [0, 100, 50, 30, -1, 250, *REFUSED]),
    ("twenties", "linear", (0, 100), (0, 1), 5, [0, 100, 37.5, -12, 1e300], [0, 1, 0.25, 2, -1e300]),
    ("a reversed domain gives the same ticks", "linear", (10, 0), (0, 1), 3, [10, 0, 2.5, 11], [0, 1, 0.4, -3]),
    ("a reversed range", "linear", (0, 1), (1, 0), 1, [0, 1, 0.75, 3], [1, 0, 0.25, 9]),
    ("one tick, at 0", "linear", (-1, 1), (-100, 100), 1, [-1, 1, 0, 0.5], [-100, 100, 0, 50]),
    ("no multiple of 0.1 in [0.11, 0.19] at c = 1, so c = 2", "linear", (0.11, 0.19), (0, 1), 1,
     [0.11, 0.19, 0.15], [0, 1, 0.5]),
    ("a domain two doubles wide: the step is below the spacing", "linear", (1, 1 + 2**-52), (0, 1), 10,
     [1, 1 + 2**-52, 0.5, 2], [0, 1, 0.5, -1, 0.25]),
    ("a one-valued domain maps to the middle of the range", "linear", (3, 3), (0, 1), 5, [3, 4, -1e308], [0, 1, 2]),
    ("a one-valued range inverts to the middle of the domain", "linear", (0, 10), (5, 5), 4, [0, 10, 3], [5, 0, 1e9]),
    ("both one-valued", "linear", (2, 2), (7, 7), 3, [2, 0], [7, 1]),
    ("wide, spanning zero", "linear", (-8e307, 8e307), (0, 1), 7, [-8e307, 8e307, 0, MAX, -MAX], [0, 1, 0.5, 3, -3]),
    ("up to the top, a thousand ticks", "linear", (0, 1.7e308), (-1, 1), 1000, [0, 1.7e308, 1e308, MAX], [-1, 1, 0]),
    ("subnormal domain", "linear", (5e-324, 3.5e-323), (0, 1), 3, [5e-324, 3.5e-323, 1e-323, 1], [0, 1, 0.5, 2]),
    ("a narrow span: maps overflow far outside", "linear", (0, 1e-300), (0, 1), 4,
     [0, 1e-300, 5e-301, 1e300, -1e300, 1e-10], [0, 1, 0.5, 1e300, -1e300]),
    ("a span of 1e-15 about 1e-10", "linear", (1e-10, 1.00000000000001e-10), (0, 1), 6, [1e-10, 1.000000000000005e-10],
     [0, 1, 0.5, 3]),
    ("temperatures", "linear", (-273.15, 100), (0, 1), 20, [-273.15, 100, 0, 37, -300], [0, 1, 0.5, 0.1, 1.2]),
    ("a wide range", "linear", (0, 1), (-8e307, 8e307), 2, [0, 1, 0.5, 0.25, 2, -2], [-8e307, 8e307, 0, 1e307]),
    ("0.1 to 0.3", "linear", (0.1, 0.3), (0, 1), 2, [0.1, 0.3, 0.2], [0, 1, 0.5]),
    ("decades", "log", (1, 1000), (0, 1), 10, [1, 1000, 10, 100, 31.6, 1e6, 0, -1, -0.0, *REFUSED],
     [0, 1, 1 / 3, 0.5, 2, -1, *REFUSED]),
    ("5.16's example: [2, 9] at c = 4 is [2, 5]", "log", (2, 9), (0, 1), 4, [2, 9, 3, 5], [0, 1, 0.5]),
    ("[2, 9] at c = 5: {1, 2, 5} gives 2 < 2.5 in less than a decade, so the linear ticks", "log", (2, 9), (0, 1), 5,
     [2, 9, 4], [0, 1, 0.25]),
    ("one decade, ten ticks", "log", (1, 10), (0, 300), 10, [1, 10, 2, 5], [0, 300, 150, 100]),
    ("[1, 2] at c = 10: two from {1..9}, so the linear ticks", "log", (1, 2), (0, 1), 10, [1, 2, 1.5], [0, 1, 0.5]),
    ("[1, 2] at c = 3 keeps {1..9}", "log", (1, 2), (0, 1), 3, [1, 2, 1.4142135623730951], [0, 1, 0.5]),
    ("[1, 5] at c = 3 is {1, 2, 5}", "log", (1, 5), (0, 1), 3, [1, 5, 2], [0, 1, 0.5]),
    ("[3, 8] at c = 20: linear by 0.2", "log", (3, 8), (0, 1), 20, [3, 8, 5], [0, 1]),
    ("[2, 90] at c = 9 is {1, 2, 5}", "log", (2, 90), (0, 1), 9, [2, 90, 20], [0, 1, 0.5]),
    ("[2, 90] at c = 11: five ticks, under 5.5, kept, since it is wider than a decade", "log", (2, 90), (0, 1), 11,
     [2, 90], [0, 1]),
    ("under a decade", "log", (0.5, 0.7), (0, 1), 5, [0.5, 0.7, 0.6], [0, 1, 0.5]),
    ("powers of 10^200", "log", (1e-300, 1e300), (0, 1), 5, [1e-300, 1e300, 1, 5e-324, MAX], [0, 1, 0.5, 2, -1]),
    ("[1, 1000] at c = 1: two powers", "log", (1, 1000), (0, 1), 1, [1, 1000, 10], [0, 1]),
    ("the whole positive line", "log", (5e-324, MAX), (0, 1), 10, [5e-324, MAX, 1, 1e-300, 1e300], [0, 1, 0.5, -1, 2]),
    ("a reversed log domain", "log", (1000, 1), (0, 1), 3, [1000, 1, 10], [0, 1, 0.5]),
    ("an exact zero: 10 on [1, 100] -> [-1, 1]", "log", (1, 100), (-1, 1), 3, [1, 100, 10, 1000], [-1, 1, 0, 3]),
    ("a one-valued log domain inverts to it", "log", (7, 7), (0, 1), 5, [7, 1, 100], [0, 1, 0.3]),
    ("a one-valued range inverts to the geometric middle", "log", (1, 100), (2, 2), 5, [1, 100, 10], [2, 0, 9]),
    ("a log invert beyond the doubles and below half the least subnormal", "log", (2, 3), (0, 1), 2,
     [2, 3, 2.5], [0, 1, 1e5, -1e5, 1749.5, -1838.2]),
    ("two adjacent doubles", "log", (1, 1 + 2**-52), (0, 1), 4, [1, 1 + 2**-52, 1.5], [0, 1, 0.5, 2]),
]

LINEAR_KINDS = ("plain", "magnitude", "narrow", "integer", "adjacent", "subnormal")
LOG_KINDS = ("decades", "wide", "narrow", "plain", "extreme")
RANGE_KINDS = ("unit", "plain", "magnitude", "pixels")
COUNTS = (1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 30, 50, 100)
RANDOM = 170


def _magnitude(rng: random.Random, low: float, high: float) -> float:
    return 10.0 ** rng.uniform(low, high)


def _linear_domain(rng: random.Random) -> tuple[float, float]:
    kind = rng.choice(LINEAR_KINDS)
    sign = rng.choice((-1.0, 1.0))
    if kind == "plain":
        return round(rng.uniform(-1000, 1000), rng.randint(0, 3)), round(rng.uniform(-1000, 1000), rng.randint(0, 3))
    if kind == "magnitude":
        return sign * _magnitude(rng, -300, 307), rng.choice((-1.0, 1.0)) * _magnitude(rng, -300, 307)
    if kind == "narrow":
        base = sign * _magnitude(rng, -300, 300)
        return base, base + base * rng.choice((-1.0, 1.0)) * 2.0 ** -rng.randint(1, 52)
    if kind == "integer":
        return float(rng.randint(-10**6, 10**6)), float(rng.randint(-10**6, 10**6))
    if kind == "adjacent":
        base = sign * _magnitude(rng, -300, 300)
        top = base
        for _ in range(rng.randint(1, 6)):
            top = math.nextafter(top, math.inf)
        return (base, top) if rng.random() < 0.5 else (top, base)
    return rng.randint(-40, 40) * 5e-324, rng.randint(-40, 40) * 5e-324


def _log_domain(rng: random.Random) -> tuple[float, float]:
    kind = rng.choice(LOG_KINDS)
    if kind == "decades":
        return 10.0 ** rng.randint(-12, 12), 10.0 ** rng.randint(-12, 12)
    if kind == "wide":
        return _magnitude(rng, -323, 308), _magnitude(rng, -323, 308)
    if kind == "narrow":
        base = _magnitude(rng, -300, 300)
        return base, base * (1 + 2.0 ** -rng.randint(1, 50))
    if kind == "plain":
        return round(rng.uniform(0.001, 1000), 3) or 0.5, round(rng.uniform(0.001, 1000), 3) or 2.0
    return rng.randint(1, 10) * 5e-324, MAX * rng.uniform(0.5, 1.0)


def _range(rng: random.Random) -> tuple[float, float]:
    kind = rng.choice(RANGE_KINDS)
    if kind == "unit":
        return (0.0, 1.0) if rng.random() < 0.7 else (1.0, 0.0)
    if kind == "plain":
        return round(rng.uniform(-500, 500), 2), round(rng.uniform(-500, 500), 2)
    if kind == "magnitude":
        r0 = rng.choice((-1.0, 1.0)) * _magnitude(rng, -300, 307)
        return r0, rng.choice((-1.0, 1.0)) * _magnitude(rng, -300, 307)
    return 0.0, float(rng.randint(100, 1000))


def _between(a: float, b: float, t: float) -> float:
    return nearest(Fraction(a) + (Fraction(b) - Fraction(a)) * Fraction(t))


def _geometric(a: float, b: float, t: float) -> float:
    """A test point a (b / a)^t; out of the doubles is inf or 0, decided in logs so no huge mpf is made."""
    with mpmath.workdps(30):
        ln_value = mpmath.log(a) + t * mpmath.log(mpmath.mpf(b) / mpmath.mpf(a))
        if not -746 < ln_value < 710:
            return math.inf if ln_value > 0 else 0.0
        v = mpmath.exp(ln_value)
    return nearest(mp_fraction(v))


def _points(rng: random.Random, a: float, b: float, geometric: bool) -> list[float]:
    """The ends, the middle, three inside, two near outside and one far, and sometimes a refusal or two."""
    at = _geometric if geometric else _between
    ts = [0.5, *(rng.random() for _ in range(3)), rng.uniform(-3, -1), rng.uniform(1, 4), rng.uniform(-1e6, 1e6)]
    points = [a, b, *(at(a, b, t) for t in ts)]
    points = [p for p in points if math.isfinite(p) and (p > 0 or not geometric)]
    if rng.random() < 0.15:
        points.append(rng.choice((MAX, -MAX, 5e-324)))
    if rng.random() < 0.2:
        points.append(rng.choice(REFUSED + ((0.0, -2.0) if geometric else ())))
    return points


def _random_case(rng: random.Random, kind: Kind) -> tuple[Kind, tuple[float, float], tuple[float, float], int,
                                                           list[float], list[float]]:
    while True:
        domain = _linear_domain(rng) if kind == "linear" else _log_domain(rng)
        range_ = _range(rng)
        try:
            Scale(kind, domain, range_)
        except RangeError:
            continue
        count = rng.choice(COUNTS) if rng.random() < 0.97 else COUNT_LIMIT
        xs = _points(rng, *domain, geometric=kind == "log")
        ys = _points(rng, *range_, geometric=False)
        return kind, domain, range_, count, xs, ys


def scales() -> list[tuple[Kind, tuple[float, float], tuple[float, float], int, list[float], list[float]]]:
    rng = random.Random("zqverify.scale")
    fixed = [(kind, d, r, c, xs, ys) for _, kind, d, r, c, xs, ys in FIXED]
    drawn = [_random_case(rng, kind) for _ in range(RANDOM) for kind in ("linear", "log")]
    return fixed + drawn


def goldens() -> list[dict[str, object]]:
    return [case(*s) for s in scales()]


def render() -> str:
    """JSON Lines, one scale a line; allow_nan=False because every non-finite value is already a string."""
    return "".join(json.dumps(c, allow_nan=False) + "\n" for c in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
