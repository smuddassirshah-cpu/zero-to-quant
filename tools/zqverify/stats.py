"""Goldens for @zq/mathcore/stats, from Python's own statistics module, NumPy and Fraction.

The specification the TypeScript must meet, in plain words: `sum` is the exactly rounded sum (math.fsum);
`mean` is that sum divided by n (statistics.fmean), moved to the nearer of min(xs) and max(xs) where it falls
outside them; `variance` is the sum of squared deviations from the mean divided by n - 1 ('sample', at least two
values) or n ('population'), and `sd` its square root; a quantile sorts the data and interpolates linearly
between the neighbours at the 0-based position h = (n - 1)p ('inclusive') or h = (n + 1)p - 1 ('gcse'), taking
the end value where h falls outside [0, n - 1]; the median is the 0.5 quantile. A statistic the data cannot give
(an overflow, too few values) is recorded as null, and the TypeScript throws.

Each case records the references the TypeScript test compares with: exactly math.fsum, the clamped fmean and
numpy.quantile(method="linear"); within the tolerances the test derives, statistics' variances, deviations,
median and quantiles, and the exact Fraction quantiles of both conventions. A NumPy or statistics median or
quantile that leaves the doubles in its own arithmetic (NumPy's b - a overflows on [-1.7e308, 1.7e308], and
statistics.median's a + b on [1.7e308, 1.7e308]) is recorded as null and checked only against the Fractions. Data sets are drawn by `random.Random` seeded with the module name.
From the repository root, rewrite the file with:

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
    # The deviation overflows for a sample, not for the population; NumPy's quantiles overflow.
    [-1.7e308, 1.7e308],
    # statistics.median overflows; the median does not.
    [1.7e308, 1.7e308],
    # Signed zeros: NumPy's quantiles may differ from ours in the sign of a zero only.
    [0.0, -0.0, -0.0, 0.0],
    # The sum overflows on the way, so fmean has no value, though the exact mean is 2e-321.
    [1.7e308, 1.7e308, -1.7e308, -1.7e308, 1e-320],
    # 38 partials, one per value: the TypeScript's buffer of 32 grows.
    [2.0 ** (1023 - 54 * k) for k in range(38)],
    # Beyond the tolerances fitted to the first goldens: 'gcse' at p = 0.37 and 0.75, and a sample variance.
    [-0.010106646676021076, 0.009232663778297238],
    [35672547.274824, -7.324550220499934e-29, 1.167244689349999e-18, 7147531090310.019],
    [3.6779024824843e-23, -2.4841613297240173e-05, -1.5708659099333112e18, -6007820616.431649],
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


def finite(qs: list[float]) -> list[float] | None:
    """The values, or None where the reference's own arithmetic left the doubles."""
    return qs if all(math.isfinite(q) for q in qs) else None


def median(xs: list[float]) -> float | None:
    """statistics.median, or None where its (a + b) / 2 overflows."""
    m = statistics.median(xs)
    return m if math.isfinite(m) else None


def quartiles(xs: list[float], method: str) -> list[float] | None:
    """statistics.quantiles where its convention is ours: two values for 'inclusive', three for 'exclusive'
    (below that its quartile positions leave [1, n] and it extrapolates, where 'gcse' takes the end value)."""
    if len(xs) < (2 if method == "inclusive" else 3):
        return None
    return finite(statistics.quantiles(xs, n=4, method=method))


def linear(xs: list[float]) -> list[float | None]:
    """numpy.quantile(method="linear") at PS, None where its b - a overflows."""
    with np.errstate(over="ignore", invalid="ignore"):
        qs = np.quantile(np.array(xs), PS, method="linear")
    return [float(q) if math.isfinite(q) else None for q in qs]


def case(xs: list[float]) -> dict[str, object]:
    return {
        "xs": xs,
        "sum": attempt(lambda: math.fsum(xs)),
        "mean": attempt(lambda: min(max(statistics.fmean(xs), min(xs)), max(xs))),
        "variance": [attempt(lambda: statistics.variance(xs)), attempt(lambda: statistics.pvariance(xs))],
        "sd": [attempt(lambda: statistics.stdev(xs)), attempt(lambda: statistics.pstdev(xs))],
        "median": median(xs),
        "linear": linear(xs),
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
    """JSON Lines: one case per line, so a changed case is a one-line diff; NaN and infinities refused."""
    return "".join(json.dumps(c, allow_nan=False) + "\n" for c in goldens())


def main() -> None:
    GOLDEN.write_text(render(), encoding="utf-8")


if __name__ == "__main__":
    main()
