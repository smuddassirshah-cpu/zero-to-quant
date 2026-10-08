"""Goldens for @zq/mathcore/stats, from Python's own statistics module, NumPy and Fraction.

The specification the TypeScript must meet, in plain words: `sum` is the exactly rounded sum (math.fsum);
`mean` is that sum divided by n (statistics.fmean), moved to the nearer of min(xs) and max(xs) where it falls
outside them; `variance` is the sum of squared deviations from the mean divided by n - 1 ('sample', at least two
values) or n ('population'), and `sd` its square root; a quantile sorts the data and interpolates linearly
between the neighbours at the 0-based position h = (n - 1)p ('inclusive') or h = (n + 1)p - 1 ('gcse'), taking
the end value where h falls outside [0, n - 1]; the median is the 0.5 quantile. A statistic the data cannot give
(an overflow, too few values) is recorded as null, and the TypeScript throws.

Each case records the references the TypeScript test compares with: exactly math.fsum, the clamped fmean and
numpy.quantile(method="linear"); within stated tolerances statistics' variances, deviations, median and
quantiles, and the exact Fraction quantiles of both conventions. Data sets are drawn by `random.Random` seeded
with the module name. From the repository root, rewrite the file with:

    PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.stats
"""

from __future__ import annotations

import json
import math
import random
import statistics
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path

import numpy as np

GOLDEN = Path(__file__).resolve().parents[2] / "packages" / "mathcore" / "test" / "stats.golden.jsonl"
PS = (0.0, 0.1, 0.25, 0.37, 0.5, 0.75, 0.9, 1.0)
PER_FAMILY = 30

# Ill-conditioned (large offset, small spread), repeated, integer, huge, subnormal and mixed-magnitude data.
FAMILIES: dict[str, Callable[[random.Random], float]] = {
    "uniform": lambda r: r.uniform(-100, 100),
    "offset": lambda r: 1e9 + r.random() * 1e-3,
    "offset-far": lambda r: -3e14 + r.random(),
    "repeated": lambda r: r.choice((0.1, 0.2, 0.7, 2.5)),
    "integers": lambda r: float(r.randint(0, 20)),
    "large": lambda r: r.uniform(-1, 1) * 1e150,
    "huge": lambda r: r.uniform(-1, 1) * 1e300,
    "subnormal": lambda r: r.randint(0, 2**20) * 5e-324,
    "magnitudes": lambda r: r.choice((-1, 1)) * 10 ** r.uniform(-20, 20),
}

FIXED = [
    [1.0],
    [3.0, 1.0],
    [0.1, 0.1, 0.1],
    [1e-16, 1.0, 1e16],
    [1e100, 1.0, -1e100, 1e-100],
    [2.3, 4.7],
    # A GCSE set of ten, where the conventions differ on the quartiles (drl.pre.summary-stats).
    [3.0, 7.0, 8.0, 12.0, 15.0, 18.0, 21.0, 22.0, 30.0, 41.0],
]


def attempt(f: Callable[[], float]) -> float | None:
    """f's value, or None where the statistic cannot be had: no data, or a result beyond the doubles."""
    try:
        return f()
    except (statistics.StatisticsError, OverflowError):
        return None


def exact_quantile(xs: list[float], p: float, method: str) -> float:
    """The definition in exact arithmetic over the doubles given, rounded once."""
    s = sorted(Fraction(x) for x in xs)
    n = len(s)
    h = (n - 1) * Fraction(p) if method == "inclusive" else (n + 1) * Fraction(p) - 1
    if h <= 0:
        return float(s[0])
    if h >= n - 1:
        return float(s[-1])
    j = math.floor(h)
    return float(s[j] + (h - j) * (s[j + 1] - s[j]))


def quartiles(xs: list[float], method: str) -> list[float] | None:
    """statistics.quantiles where its convention is ours: two values for 'inclusive', three for 'exclusive'
    (below that its quartile positions leave [1, n] and it extrapolates, where 'gcse' takes the end value)."""
    return statistics.quantiles(xs, n=4, method=method) if len(xs) >= (2 if method == "inclusive" else 3) else None


def case(xs: list[float]) -> dict[str, object]:
    return {
        "xs": xs,
        "sum": attempt(lambda: math.fsum(xs)),
        "mean": attempt(lambda: min(max(statistics.fmean(xs), min(xs)), max(xs))),
        "variance": [attempt(lambda: statistics.variance(xs)), attempt(lambda: statistics.pvariance(xs))],
        "sd": [attempt(lambda: statistics.stdev(xs)), attempt(lambda: statistics.pstdev(xs))],
        "median": statistics.median(xs),
        "linear": [float(q) for q in np.quantile(np.array(xs), PS, method="linear")],
        "inclusive": [exact_quantile(xs, p, "inclusive") for p in PS],
        "gcse": [exact_quantile(xs, p, "gcse") for p in PS],
        "quartiles": [quartiles(xs, "inclusive"), quartiles(xs, "exclusive")],
    }


def goldens() -> list[dict[str, object]]:
    rng = random.Random("zqverify.stats")
    sets = list(FIXED)
    for draw in FAMILIES.values():
        sets += [[draw(rng) for _ in range(rng.randint(1, 40))] for _ in range(PER_FAMILY)]
    return [case(xs) for xs in sets]


def render() -> str:
    """JSON Lines: one case per line, so a changed case is a one-line diff."""
    return "".join(json.dumps(c) + "\n" for c in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
