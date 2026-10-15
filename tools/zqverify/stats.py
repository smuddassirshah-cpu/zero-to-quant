"""Twin of @zq/mathcore/stats and writer of its goldens, from docs/ARCHITECTURE.md 5.16 alone.

Written by unit ST without reading the TypeScript, its tests or the module this file replaces (CLAUDE.md hard
rule 4; docs/DECISIONS.md B51 and B54). Where this file and the TypeScript disagree, 5.16 decides.

The rules, in 5.16's words where they are short:
- Data is a sequence of doubles. Every statistic but `sum` needs a value (`variance` and `sd` of kind "sample"
  need two) and every value must be finite. Errors are RangeErrors (here `RangeError`, a ValueError): too few
  values, a NaN or infinite value, a `lerp` end or t that is not finite, p outside [0, 1] (NaN included), and a
  sum, variance or deviation that overflows. Nothing else throws; an unknown kind or method is a TypeError,
  the error TypeScript's types give at compile time.
- `sum` is the exact sum rounded once, ties to even: the values go in order into Shewchuk's non-overlapping
  partials, and a running partial that becomes infinite throws where `math.fsum` raises its intermediate
  overflow. `mean` is that sum over n, one rounding (`statistics.fmean`), moved into [min, max].
- `variance` and `sd` here are the references 5.16 names: the exact variance V of the doubles given, with
  divisor n - 1 or n, rounded once, and the double nearest sqrt(V). Both throw where that double is infinite.
  The TypeScript's Sum2 computation is ported in tests/test_stats.py to check 5.16's error bound.
- Quantiles sort the data, -0 before +0, and take the position h in doubles: "inclusive" (n - 1) * p, one
  rounding; "gcse" ((n + 1) * p) - 1, two. h <= 0 gives the first value and h >= n - 1 the last, unchanged;
  otherwise lerp(s[j], s[j + 1], h - j) with j = floor(h). `quartiles` takes p = 0.25, 0.5, 0.75 from one sort
  and `median` is the inclusive quantile at 0.5.
- `lerp` is NumPy's `_lerp`: a + (b - a) * t for t < 0.5, else b - (b - a) * (1 - t), every operation rounded;
  where that is not finite, the same on a / 2 and b / 2, doubled.

A golden line (packages/mathcore/test/stats.golden.jsonl) holds `xs`; `sum` and `mean`, null where Python's
fsum raises its overflow; `variance` and `sd` as [sample, population]; `median` (`statistics.median`);
`linear` (`numpy.quantile`, method "linear"), `inclusive` and `gcse` (the exact quantile with h exact, rounded
once) at each p of PS; and `quartiles`, [inclusive, exclusive] from `statistics.quantiles(xs, n=4)`, the first
for n >= 2 and the second for n >= 3. A reference that cannot be had, or whose own arithmetic leaves the
doubles, is null; a method's three quartiles are one reference, null together. Data sets are FIXED, each
with its reason, then sets drawn by `random.Random` seeded with the module name. From the repository root:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.stats
"""

from __future__ import annotations

import builtins
import json
import math
import random
import statistics
from collections.abc import Callable, Iterable, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Literal

import numpy as np

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "stats.golden.jsonl"
PS = (0.0, 0.1, 0.25, 0.37, 0.5, 0.75, 0.9, 1.0)
QUARTILE_PS = (0.25, 0.5, 0.75)
U = 2.0**-53
LEAST = math.ulp(0.0)  # 2^-1074, the least subnormal
MAX = 1.7976931348623157e308

Kind = Literal["sample", "population"]
Method = Literal["inclusive", "gcse"]


class RangeError(ValueError):
    """The TypeScript's RangeError."""


# --- exact rounding, shared with zqverify.scale -------------------------------------------------------------


def nearest(q: Fraction) -> float:
    """The double nearest q, ties to even, and +-inf beyond the doubles. `int / int` in CPython is correctly
    rounded [recalled]; tests/test_stats.py checks it against both neighbours of every result."""
    try:
        return q.numerator / q.denominator
    except OverflowError:
        return math.inf if q > 0 else -math.inf


def sqrt_nearest(q: Fraction) -> float:
    """The double nearest sqrt(q) for q >= 0, +inf beyond the doubles.

    With s = isqrt(floor(q * 4^k)) of at least 55 bits, sqrt(q) * 2^k lies in [s, s + 1) and no rounding
    boundary of the result lies strictly inside, so (2s + inexact) / 2^(k + 1) rounds as sqrt(q) does.
    """
    num, den = q.numerator, q.denominator
    if num == 0:
        return 0.0
    k = max(0, (112 - (num.bit_length() - den.bit_length())) // 2 + 1)
    scaled = num << (2 * k)
    s = math.isqrt(scaled // den)
    inexact = s * s * den != scaled
    return nearest(Fraction(2 * s + inexact, 1 << (k + 1)))


# --- the twin ------------------------------------------------------------------------------------------------


def _data(xs: Iterable[float], least: int) -> list[float]:
    values = [float(x) for x in xs]
    if len(values) < least:
        raise RangeError(f"needs at least {least} value{'s' if least > 1 else ''}")
    if not all(map(math.isfinite, values)):
        raise RangeError("every value must be finite")
    return values


def sum(xs: Iterable[float]) -> float:  # the TypeScript's name, so builtins.sum below
    """Shewchuk's partials, then their exact sum rounded once; an infinite running partial throws."""
    partials: list[float] = []
    for x in _data(xs, 0):
        i = 0
        for y in partials:
            if abs(x) < abs(y):
                x, y = y, x
            hi = x + y
            lo = y - (hi - x)  # exact, since |x| >= |y| (Fast2Sum)
            if lo:
                partials[i] = lo
                i += 1
            x = hi
        if not math.isfinite(x):
            raise RangeError("the sum overflows")
        partials[i:] = [x]
    total = nearest(builtins.sum(map(Fraction, partials), Fraction(0)))
    if not math.isfinite(total):  # not reached: the top partial is the rounded running sum [inferred]
        raise RangeError("the sum overflows")
    return total


def mean(xs: Iterable[float]) -> float:
    values = _data(xs, 1)
    m = sum(values) / len(values)
    low, high = min(values), max(values)
    return low if m < low else high if m > high else m


def _divisor(n: int, kind: Kind) -> int:
    if kind == "sample":
        return n - 1
    if kind == "population":
        return n
    raise TypeError(f"unknown kind {kind!r}")


def exact_variance(xs: Iterable[float], kind: Kind) -> Fraction:
    """V: the squared deviations of the doubles from their exact mean, summed, over n - 1 or n.

    Each double is an integer times 2^-1074, so V = (n * sum(m^2) - sum(m)^2) / (n * D * 2^2148) in integers.
    """
    values = _data(xs, 2 if kind == "sample" else 1)
    n, d = len(values), _divisor(len(values), kind)
    ms = []
    for x in values:
        num, den = x.as_integer_ratio()
        ms.append(num * ((1 << 1074) // den))
    s = builtins.sum(ms)
    q = builtins.sum(m * m for m in ms)
    return Fraction(n * q - s * s, n * d << 2148)


def variance(xs: Iterable[float], kind: Kind) -> float:
    v = nearest(exact_variance(xs, kind))
    if math.isinf(v):
        raise RangeError("the variance overflows")
    return v


def sd(xs: Iterable[float], kind: Kind) -> float:
    s = sqrt_nearest(exact_variance(xs, kind))
    if math.isinf(s):
        raise RangeError("the deviation overflows")
    return s


def _lerp(a: float, b: float, t: float) -> float:
    d = b - a
    return a + d * t if t < 0.5 else b - d * (1.0 - t)


def lerp(a: float, b: float, t: float) -> float:
    a, b, t = float(a), float(b), float(t)
    if not (math.isfinite(a) and math.isfinite(b)):
        raise RangeError("lerp's ends must be finite")
    if not math.isfinite(t):
        raise RangeError("lerp's t must be finite")
    r = _lerp(a, b, t)
    return r if math.isfinite(r) else 2.0 * _lerp(a / 2.0, b / 2.0, t)


def _p(p: float) -> float:
    p = float(p)
    if not 0.0 <= p <= 1.0:  # NaN fails both comparisons
        raise RangeError("p must lie in [0, 1]")
    return p


def _sorted(values: list[float]) -> list[float]:
    """Increasing, -0 before +0."""
    return sorted(values, key=lambda x: (x, math.copysign(1.0, x)))


def _position(n: int, p: float, method: Method) -> float:
    if method == "inclusive":
        return (n - 1) * p
    if method == "gcse":
        return ((n + 1) * p) - 1
    raise TypeError(f"unknown method {method!r}")


def _quantile_sorted(s: list[float], p: float, method: Method) -> float:
    n = len(s)
    h = _position(n, p, method)
    if h <= 0:
        return s[0]
    if h >= n - 1:
        return s[-1]
    j = math.floor(h)
    return lerp(s[j], s[j + 1], h - j)  # h - j is exact: j is h's integer part


def quantile(xs: Iterable[float], p: float, method: Method) -> float:
    s = _sorted(_data(xs, 1))
    return _quantile_sorted(s, _p(p), method)


def quartiles(xs: Iterable[float], method: Method) -> list[float]:
    s = _sorted(_data(xs, 1))
    return [_quantile_sorted(s, p, method) for p in QUARTILE_PS]


def median(xs: Iterable[float]) -> float:
    return quantile(xs, 0.5, "inclusive")


def exact_quantile(xs: Iterable[float], p: float, method: Method) -> float:
    """The quantile in exact arithmetic from the doubles, with h exact, rounded once (5.16's golden reference)."""
    s = _sorted(_data(xs, 1))
    n, q = len(s), Fraction(_p(p))
    if method == "inclusive":
        h = (n - 1) * q
    elif method == "gcse":
        h = (n + 1) * q - 1
    else:
        raise TypeError(f"unknown method {method!r}")
    if h <= 0:
        return s[0]
    if h >= n - 1:
        return s[-1]
    j = math.floor(h)
    a, b = Fraction(s[j]), Fraction(s[j + 1])
    return nearest(a + (b - a) * (h - j))


# --- references and goldens ----------------------------------------------------------------------------------


def _or_none[T](f: Callable[[], T], *errors: type[BaseException]) -> T | None:
    try:
        return f()
    except errors:
        return None


def _finite(x: float | None) -> float | None:
    return None if x is None or not math.isfinite(x) else float(x)


def numpy_linear(xs: Sequence[float], p: float) -> float | None:
    """`numpy.quantile(method="linear")`, null where NumPy's own arithmetic overflows (its b - a)."""
    with np.errstate(over="raise", invalid="raise", divide="raise", under="ignore"):
        try:
            return _finite(float(np.quantile(np.asarray(xs, dtype=np.float64), p, method="linear")))
        except FloatingPointError:
            return None


def statistics_quartiles(xs: Sequence[float], method: Literal["inclusive", "exclusive"]) -> list[float] | None:
    """`statistics.quantiles(xs, n=4)`, null as a whole where its arithmetic leaves the doubles: 5.16 names each
    method's three quartiles as one reference ("the first for n >= 2 and the second for n >= 3")."""
    qs = statistics.quantiles(xs, n=4, method=method)
    return [float(q) for q in qs] if all(map(math.isfinite, qs)) else None


def case(xs: Sequence[float]) -> dict[str, object]:
    xs = [float(x) for x in xs]
    n = len(xs)

    def both(f: Callable[[Sequence[float], Kind], float]) -> list[float | None]:
        return [_or_none(lambda: f(xs, kind), RangeError) for kind in ("sample", "population")]

    return {
        "xs": xs,
        "sum": _or_none(lambda: sum(xs), RangeError),
        "mean": _or_none(lambda: mean(xs), RangeError),
        "variance": both(variance),
        "sd": both(sd),
        "median": _finite(statistics.median(xs)),
        "linear": [numpy_linear(xs, p) for p in PS],
        "inclusive": [exact_quantile(xs, p, "inclusive") for p in PS],
        "gcse": [exact_quantile(xs, p, "gcse") for p in PS],
        "quartiles": [
            statistics_quartiles(xs, "inclusive") if n >= 2 else None,
            statistics_quartiles(xs, "exclusive") if n >= 3 else None,
        ],
    }


BIG = 1.7e308
FIXED: list[tuple[str, list[float]]] = [
    ("one value", [1.0]),
    ("a negative zero alone: fsum gives +0", [-0.0]),
    ("zeros of both signs, +0 first: the sort puts -0 first", [0.0, -0.0]),
    ("zeros of both signs, three", [-0.0, 0.0, -0.0]),
    ("two values: gcse's lower quartile is the first value, exclusive extrapolates to 0.75", [1.0, 2.0]),
    ("three values unsorted", [3.0, 1.0, 2.0]),
    ("four values", [1.0, 2.0, 3.0, 4.0]),
    ("five values", [7.0, 1.0, 5.0, 3.0, 9.0]),
    ("three 0.1s: fmean gives 0.10000000000000002, the clamp gives 0.1", [0.1, 0.1, 0.1]),
    ("C5's n = 10, where gcse and inclusive quartiles differ", [2.0, 4.0, 4.0, 5.0, 7.0, 8.0, 9.0, 11.0, 12.0, 15.0]),
    ("an infinite running partial though the exact sum is a double", [BIG, BIG, -BIG]),
    ("the sum throws, so the mean 2e-321 throws", [BIG, BIG, -BIG, -BIG, 1e-320]),
    ("NumPy's b - a overflows; the variances and the sample sd overflow", [-BIG, BIG]),
    ("statistics.median's a + b overflows", [BIG, BIG]),
    ("near the top, mixed signs", [-BIG, -1e308, 1e308, BIG]),
    ("a population variance 1e308 and an overflowing sample variance", [1e154, -1e154]),
    ("subnormals", [5e-324, 1e-323, 1.5e-323, 2e-323]),
    ("subnormals of both signs", [1e-320, -1e-320, 3e-321, -5e-324]),
    ("every value below 2^-400: the TypeScript scales by 2^600", [1e-150, 2e-150, 3e-150, 5e-150]),
    ("every value above 2^400: the TypeScript scales by 2^-600", [1e130, 2e130, 4e130, -3e130]),
    ("cancellation in the sum", [1e16, 1.0, -1e16]),
    ("the exact sum 1 + 2^-53 ties to 1", [1.0, 2.0**-53]),
    ("a tie broken by a third partial", [1.0, 2.0**-53, 2.0**-106]),
    ("a large mean and a small variance", [1e9 + 0.1, 1e9 + 0.2, 1e9 + 0.3, 1e9 + 0.4]),
    ("all the same: variance 0", [2.5, 2.5, 2.5, 2.5, 2.5]),
    ("all the same and huge", [BIG, BIG, BIG]),
    ("mixed magnitudes", [1e300, -1e-300, 3.0, -2.5e10]),
    ("1 to 40", [float(k) for k in range(1, 41)]),
    ("a decimal sample", [12.5, 3.75, 8.0, 3.75, 19.25, 0.5, 11.0]),
]


def _value(rng: random.Random, kind: str, base: float) -> float:
    if kind == "decimal":
        return round(rng.uniform(-100.0, 100.0), rng.randint(0, 3))
    if kind == "integer":
        return float(rng.randint(-20, 20))
    if kind == "spread":
        return rng.choice((-1.0, 1.0)) * math.ldexp(rng.uniform(0.5, 1.0), rng.randint(-1073, 1023))
    if kind == "cluster":
        return base + base * rng.uniform(-1.0, 1.0) * 2.0 ** -rng.randint(20, 52)
    if kind == "tiny":
        return rng.uniform(-1.0, 1.0) * base
    if kind == "huge":
        return rng.uniform(-1.0, 1.0) * base
    if kind == "top":
        return rng.uniform(-1.0, 1.0) * BIG  # uniform(-BIG, BIG) overflows in b - a
    if kind == "zeros":
        return rng.choice((0.0, -0.0, 5e-324, -5e-324, 1.0, -1.0))
    raise AssertionError(kind)


KINDS = ("decimal", "integer", "spread", "cluster", "tiny", "huge", "top", "zeros", "repeats")
WEIGHTS = (6, 4, 4, 4, 2, 2, 1, 2, 3)
SIZES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 20, 25, 31, 40)
RANDOM = 280


def _random_set(rng: random.Random) -> list[float]:
    kind = rng.choices(KINDS, WEIGHTS)[0]
    n = rng.choice(SIZES)
    if kind == "repeats":
        pool = [_value(rng, "decimal", 0.0) for _ in range(3)]
        return [rng.choice(pool) for _ in range(n)]
    base = {
        "cluster": rng.choice((1e9, -3e5, 0.1, 1e15, 7e-200, 3e250)),
        "tiny": 2.0 ** -rng.randint(401, 1060),
        "huge": 2.0 ** rng.randint(401, 510),
    }.get(kind, 0.0)
    return [_value(rng, kind, base) for _ in range(n)]


def data_sets() -> list[list[float]]:
    rng = random.Random("zqverify.stats")
    return [xs for _, xs in FIXED] + [_random_set(rng) for _ in range(RANDOM)]


def goldens() -> list[dict[str, object]]:
    return [case(xs) for xs in data_sets()]


def render() -> str:
    """JSON Lines, one data set a line; allow_nan=False because JSON.parse reads no infinity."""
    return "".join(json.dumps(c, allow_nan=False) + "\n" for c in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
