"""Check for drill pack py, agent A: 12 `py-found` drills and 6 `plotting` drills.

For every drill it runs the model `solution` and an independent method written separately here on every
example and hidden test, and both must agree with `expect` under the drill page's own comparison (`equal`, or
`isclose` at rel 1e-9 element by element; the prelude runs after the code). It recomputes each brief's worked example by the
independent method against a value worked by hand, checks that the starter fails at least one hidden test,
that every planted wrong solution fails at least one hidden test (a wrong answer, an error, or more than
5 s), that each drill's skills are declared by the lesson it draws on, the `how` count, the pace range and
the difficulty mix (py-found 4 / 5 / 3, plotting 2 / 2 / 2). Exit 0 when everything holds.

Run from the repo root: <scratchpad>/venv/bin/python docs/reports/drills-py-a-check.py
"""
import itertools
import json
import math
import os
import signal
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "..", "app", "content")
DRILLS = os.path.join(APP, "drills")
LIMIT = 5.0

# drill id -> (course, lesson the drill draws on)
LESSON = {
    "py-trimmed-fill-mean": ("py-found", "l2-slicing"),
    "py-holdings-change": ("py-found", "l6-membership"),
    "py-format-pence": ("py-found", "l16-returns-from-a-file"),
    "py-cross-up-days": ("py-found", "l4-one-line-lists"),
    "py-split-pence": ("py-found", "l1-why-not-0-3"),
    "py-fill-summary": ("py-found", "l5-lookup-by-name"),
    "py-quote-ladder": ("py-found", "l7-arguments"),
    "py-wide-to-long": ("py-found", "l10-reading-a-csv"),
    "py-batches": ("py-found", "l13-one-at-a-time"),
    "py-split-adjusted": ("py-found", "l8-who-changes-the-list"),
    "py-guarded-returns": ("py-found", "l11-when-things-go-wrong"),
    "py-cost-basis": ("py-found", "l12-data-with-behaviour"),
    "py-growth-curve": ("plotting", "l7-drawing-drawdown"),
    "py-bar-limits": ("plotting", "l12-charts-that-mislead"),
    "py-bin-counts": ("plotting", "l6-shape-of-returns"),
    "py-paired-returns": ("plotting", "l11-two-variables"),
    "py-underwater-series": ("plotting", "l7-drawing-drawdown"),
    "py-month-grid": ("plotting", "l10-panels"),
}


# ---------------------------------------------------------------- independent methods
def trimmed_fill_mean(prices, k):
    rest = list(prices)
    for _ in range(k):
        if rest:
            rest.remove(min(rest))
        if rest:
            rest.remove(max(rest))
    return math.fsum(rest) / len(rest) if rest else None


def holdings_change(before, after):
    old = dict.fromkeys(before)
    new = dict.fromkeys(after)
    added = [t for t in new if t not in old]
    dropped = [t for t in old if t not in new]
    return (sorted(added), sorted(dropped), sum(1 for t in new if t in old))


def format_pence(p):
    digits = str(abs(p)).rjust(3, "0")
    pounds, pence = digits[:-2], digits[-2:]
    groups = []
    while pounds:
        groups.insert(0, pounds[-3:])
        pounds = pounds[:-3]
    return ("-" if p < 0 else "") + "£" + ",".join(groups) + "." + pence


def cross_up_days(fast, slow):
    above = [f > s for f, s in zip(fast, slow)]
    return [i for i in range(1, len(above)) if above[i] and not above[i - 1]]


def split_pence(fee, n):
    total = int(Decimal(repr(fee)) * 100)
    # share i of `total` split n ways, largest first, is ceil((total - i) / n)
    return [(total - i + n - 1) // n for i in range(n)]


def fill_summary(fills):
    groups = {}
    for oid, q, p in fills:
        groups.setdefault(oid, []).append((q, p))
    return {oid: (sum(q for q, _ in g), float(sum(Fraction(q) * Fraction(p) for q, p in g) / sum(q for q, _ in g))) for oid, g in groups.items()}


def quote_ladder(mid, levels=3, step=0.05, size=100):
    m, s = Decimal(repr(mid)), Decimal(repr(step))
    cent = Decimal("0.01")
    bids = [("bid", float((m - k * s).quantize(cent, ROUND_HALF_EVEN)), k * size) for k in range(1, levels + 1)]
    asks = [("ask", float((m + k * s).quantize(cent, ROUND_HALF_EVEN)), k * size) for k in range(1, levels + 1)]
    return bids + asks


def wide_to_long(text):
    lines = [ln for ln in text.replace("\r\n", "\n").split("\n") if ln != ""]
    if not lines:
        return []
    head = [h.strip() for h in lines[0].split(",")]
    out = []
    for ln in lines[1:]:
        cells = ln.split(",")
        for j in range(1, len(head)):
            if j < len(cells) and cells[j].strip() != "":
                out.append((head[j], cells[0].strip(), float(cells[j])))
    out.sort(key=lambda t: t[1])
    out.sort(key=lambda t: t[0])
    return out


def batches(items, size):
    if size < 1:
        raise ValueError("size")
    it = iter(items)
    while True:
        chunk = list(itertools.islice(it, size))
        if not chunk:
            return
        yield chunk


def split_adjusted(closes, splits):
    return [c / math.prod(r for d, r in splits.items() if d > i) for i, c in enumerate(closes)]


def guarded_returns(pairs):
    def read(t):
        if not isinstance(t, str):
            raise TypeError("not text")
        try:
            return float(t)
        except ValueError:
            return None

    rets, bad, zero = [], 0, 0
    for pair in pairs:
        if not isinstance(pair, tuple):
            raise TypeError("not a pair")
        o, c = read(pair[0]), read(pair[1])
        if o is None or c is None:
            bad += 1
        elif o == 0:
            zero += 1
        else:
            rets.append(c / o - 1)
    return (rets, bad, zero)


class CostBasis:
    # Holds the total cost of the shares still held, reduced at the average on each sale.
    def __init__(self):
        self._cost = Fraction(0)
        self.qty = 0
        self._real = Fraction(0)

    @property
    def avg_cost(self):
        return float(self._cost / self.qty) if self.qty else 0.0

    @property
    def realised(self):
        return float(self._real)

    def buy(self, qty, price):
        if not qty > 0:
            raise ValueError("qty")
        self._cost += qty * Fraction(price)
        self.qty += qty

    def sell(self, qty, price):
        if not 0 < qty <= self.qty:
            raise ValueError("qty")
        avg = self._cost / self.qty
        self._real += qty * (Fraction(price) - avg)
        self._cost -= qty * avg
        self.qty -= qty

    def unrealised(self, price):
        return float(self.qty * Fraction(price) - self._cost)


def growth_curve(rets, start=100.0):
    return [start * math.prod(1 + r for r in rets[:i]) for i in range(len(rets) + 1)]


def bar_limits(values, pad=0.1):
    lo = min(min(values, default=0), 0)
    hi = max(max(values, default=0), 0)
    if lo == hi:
        return (0.0, 1.0)
    w = hi - lo
    return (lo - pad * w * (lo != 0), hi + pad * w * (hi != 0))


def bin_counts(rets, edges):
    counts, _ = np.histogram(np.array(rets, dtype=float), bins=np.array(edges, dtype=float))
    return [int(c) for c in counts]


def paired_returns(a, b):
    df = pd.concat([pd.Series(a, dtype=float), pd.Series(b, dtype=float)], axis=1, join="inner").sort_index()
    r = (df / df.shift(1) - 1).iloc[1:]
    return [(float(x), float(y)) for x, y in r.to_numpy()]


def underwater_series(values):
    v = np.array(values, dtype=float)
    if len(v) == 0:
        return ([], [])
    peak = np.maximum.accumulate(v)
    t = np.arange(len(v))
    last = np.maximum.accumulate(np.where(v >= peak, t, 0))
    return ((v / peak - 1).tolist(), (t - last).tolist())


def month_grid(rows):
    if not rows:
        return ([], [], [])
    df = pd.DataFrame(rows, columns=["date", "ticker", "r"])
    df["month"] = df["date"].str.slice(0, 7)
    cell = (1 + df["r"]).groupby([df["month"], df["ticker"]]).prod() - 1
    table = cell.unstack("ticker").sort_index().sort_index(axis=1)
    grid = [[None if pd.isna(x) else float(x) for x in row] for row in table.to_numpy()]
    return (list(table.index), list(table.columns), grid)


SLOW = {
    "trimmed_fill_mean": trimmed_fill_mean, "holdings_change": holdings_change, "format_pence": format_pence,
    "cross_up_days": cross_up_days, "split_pence": split_pence, "fill_summary": fill_summary, "quote_ladder": quote_ladder,
    "wide_to_long": wide_to_long, "batches": batches, "split_adjusted": split_adjusted, "guarded_returns": guarded_returns,
    "CostBasis": CostBasis, "growth_curve": growth_curve, "bar_limits": bar_limits, "bin_counts": bin_counts,
    "paired_returns": paired_returns, "underwater_series": underwater_series, "month_grid": month_grid,
}

# The worked example in each brief, with the value worked by hand from the brief's own words.
BRIEF = {
    "py-trimmed-fill-mean": ("trimmed_fill_mean([4.2, 9.9, 4.4, 4.3, 0.1], 1)", (4.2 + 4.3 + 4.4) / 3),
    "py-holdings-change": ("holdings_change(['BP', 'VOD', 'BP', 'AZN'], ['VOD', 'SHEL', 'AZN', 'SHEL'])", (["SHEL"], ["BP"], 2)),
    "py-format-pence": ("[format_pence(-123405), format_pence(5)]", ["-£1,234.05", "£0.05"]),
    "py-cross-up-days": ("cross_up_days([1.0, 2.0, 3.0, 2.0, 4.0], [2.0, 2.0, 2.5, 2.5, 3.0])", [2, 4]),
    "py-split-pence": ("split_pence(10.00, 3)", [334, 333, 333]),
    "py-fill-summary": ("fill_summary([('A1', 100, 4.80), ('B7', 50, 72.10), ('A1', 300, 4.84)])", {"A1": (400, 1932 / 400), "B7": (50, 72.1)}),
    "py-quote-ladder": ("quote_ladder(5.0, levels=2)", [("bid", 4.95, 100), ("bid", 4.9, 200), ("ask", 5.05, 100), ("ask", 5.1, 200)]),
    "py-wide-to-long": ("wide_to_long('date,BP,VOD\\n2026-03-02,4.85,\\n2026-03-03,4.91,0.72\\n')",
                        [("BP", "2026-03-02", 4.85), ("BP", "2026-03-03", 4.91), ("VOD", "2026-03-03", 0.72)]),
    "py-batches": ("list(batches([1, 2, 3, 4, 5, 6, 7], 3))", [[1, 2, 3], [4, 5, 6], [7]]),
    "py-split-adjusted": ("split_adjusted([90.0, 30.5, 31.0, 15.0], {1: 3, 3: 2})", [90 / 6, 30.5 / 2, 31 / 2, 15.0]),
    "py-guarded-returns": ("guarded_returns([('4.80', '4.92'), ('n/a', '4.95'), ('0', '5.10'), ('5.00', '4.90')])", ([0.12 / 4.80, -0.10 / 5.00], 1, 1)),
    "py-cost-basis": ("(c := CostBasis(), c.buy(100, 4.00), c.buy(300, 4.40), c.sell(200, 4.50), (c.qty, c.avg_cost, c.realised))[-1]",
                      (200, (400 + 1320) / 400, 200 * 0.20)),
    "py-growth-curve": ("growth_curve([0.10, -0.10])", [100.0, 110.0, 99.0]),
    "py-bar-limits": ("[bar_limits([-2.0, 6.0]), bar_limits([3.0, 5.0, 4.0])]", [(-2 - 0.8, 6 + 0.8), (0.0, 5 + 0.5)]),
    "py-bin-counts": ("bin_counts([-0.015, 0.0, 0.004, 0.01, 0.02, 0.031], [-0.02, -0.01, 0.0, 0.01, 0.02])", [1, 0, 2, 2]),
    "py-paired-returns": ("paired_returns({'2026-03-02': 100.0, '2026-03-03': 102.0, '2026-03-04': 101.0}, {'2026-03-02': 50.0, '2026-03-04': 49.0, '2026-03-05': 51.0})",
                          [(1 / 100, -1 / 50)]),
    "py-underwater-series": ("underwater_series([100.0, 90.0, 95.0, 100.0, 80.0])", ([0.0, -0.1, -0.05, 0.0, -0.2], [0, 1, 2, 0, 1])),
    "py-month-grid": ("month_grid([('2026-01-05', 'BP', 0.01), ('2026-01-06', 'BP', 0.02), ('2026-02-02', 'BP', -0.01), ('2026-01-05', 'VOD', 0.03)])",
                      (["2026-01", "2026-02"], ["BP", "VOD"], [[1.01 * 1.02 - 1, 0.03], [-0.01, None]])),
}
# A second hand check of the arithmetic quoted in the briefs and notes.
assert 1000 // 3 == 333 and 1000 % 3 == 1 and round(0.29 * 100) == 29 and int(0.29 * 100) == 28
assert abs(1932 / 400 - 4.83) < 1e-12 and 100 * 4.80 + 300 * 4.84 == 1932
assert 4.85 - 4 * 0.05 != 4.65 and round(4.85 - 4 * 0.05, 2) == 4.65 and 72.4 - 0.1 != 72.3
assert abs((1 + 0.10) * (1 - 0.10) - 0.99) < 1e-12 and abs(0.5 * 0.5 - 0.25) < 1e-12  # two -50% days make -75%
assert abs((1720 / 400) - 4.30) < 1e-12 and abs(200 * (4.50 - 4.30) - 40) < 1e-9


# ---------------------------------------------------------------- comparisons
def near(x, y):
    """Loose comparison for the hand-worked brief values: dicts, sequences and numbers within rel 1e-9."""
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(near(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(near(a, b) for a, b in zip(x, y))
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-12)
    return x == y


def drill_eq(a, e, mode):
    """The drill page's own test (`__zq_eq` in app/js/screens/drill.js): `equal` is `a == e`; `isclose` takes None,
    lists and tuples element by element and numbers within rel 1e-9, and fails anything else (a string or a dict)."""
    if mode == "isclose":
        if e is None:
            return a is None
        if isinstance(e, (list, tuple)):
            return isinstance(a, (list, tuple)) and len(a) == len(e) and all(drill_eq(x, y, mode) for x, y in zip(a, e))
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            return False
        return math.isclose(a, e, rel_tol=1e-9, abs_tol=1e-12)
    return a == e


class Slow(Exception):
    pass


def _alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, _alarm)


def outcome(code, case, prelude="", limit=LIMIT):
    """Run one case as the drill page does (learner code, then the prelude, then the call); True when it passes."""
    ns = {}
    signal.setitimer(signal.ITIMER_REAL, limit)
    try:
        if isinstance(code, dict):
            ns.update(code)
        else:
            exec(code, ns)
        if prelude:
            exec(prelude, ns)
        got = eval(case["call"], ns)
        return drill_eq(got, eval(case["expect"], ns), case["compare"])
    except Slow:
        return False
    except Exception:  # noqa: BLE001
        return False
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def lesson_skills(course, lesson):
    return set(json.load(open(os.path.join(APP, "courses", course, lesson + ".json")))["skills"])


def main():
    errors = 0
    only = sys.argv[1:]
    drills = [json.load(open(os.path.join(DRILLS, i + ".json"))) for i in LESSON]
    mix = {c: Counter(d["difficulty"] for d in drills if d["course"] == c) for c in ("py-found", "plotting")}
    if mix["py-found"] != Counter({1: 4, 2: 5, 3: 3}) or mix["plotting"] != Counter({1: 2, 2: 2, 3: 2}):
        errors += 1
        print("MIX", mix)
    index = {r["id"]: r for r in json.load(open(os.path.join(DRILLS, "index.json")))}
    planted_total = 0
    for d in drills:
        if only and d["id"] not in only:
            continue
        course, lesson = LESSON[d["id"]]
        row = index.get(d["id"])
        if not row or (row["name"], row["course"], row["difficulty"]) != (d["name"], d["course"], d["difficulty"]):
            errors += 1
            print("INDEX row disagrees:", d["id"])
        if d["course"] != course or d["pack"] != "py" or not 300 <= d["pace"] <= 1200 or "pattern" in d:
            errors += 1
            print("FIELDS", d["id"])
        if not set(d["skills"]) <= lesson_skills(course, lesson):
            errors += 1
            print("SKILLS not declared by", lesson, d["id"], d["skills"])
        if not d["how"].startswith("Submit runs %d hidden tests." % len(d["tests"])) or not 10 <= len(d["tests"]) <= 14:
            errors += 1
            print("HOW count", d["id"])
        if len(d["notes"]) != 3 or not 2 <= len(d["examples"]) <= 3 or not all(e.get("note") for e in d["examples"]):
            errors += 1
            print("NOTES or EXAMPLES", d["id"])
        slow_ns = {d["fn"]: SLOW[d["fn"]]}
        pre = d.get("prelude", "")
        if any("setup" in c or c["compare"] not in ("equal", "isclose") for c in d["examples"] + d["tests"]):
            errors += 1
            print("CASE uses setup or a compare the drill page does not run:", d["id"])
        call, want = BRIEF[d["id"]]
        if not near(eval(call, dict(slow_ns)), want):
            errors += 1
            print("BRIEF", d["id"], call)
        for k, case in enumerate(d["examples"] + d["tests"]):
            if not outcome(d["solution"], case, pre):
                errors += 1
                print("MODEL", d["id"], k, case["call"][:70])
            if not outcome(slow_ns, case, pre):
                errors += 1
                print("SECOND", d["id"], k, case["call"][:70])
        starter_fails = sum(not outcome(d["starter"], c, pre) for c in d["tests"])
        if starter_fails == 0:
            errors += 1
            print("STARTER passes every test:", d["id"])
        caught = []
        for k, p in enumerate(d.get("planted", [])):
            fails = [t for t, c in enumerate(d["tests"]) if not outcome(p["code"], c, pre)]
            if not fails:
                errors += 1
                print("PLANTED passes every test:", d["id"], k, p["slip"][:60])
            caught.append("fails %s" % ",".join(map(str, fails)) if fails else "PASSES")
        planted_total += len(caught)
        if not 2 <= len(caught) <= 3:
            errors += 1
            print("planted count:", d["id"])
        print("%-22s %-9s d%d %4ds %2d tests, starter fails %2d; planted: %s"
              % (d["id"], d["course"], d["difficulty"], d["pace"], len(d["tests"]), starter_fails, "; ".join(caught)))
    print("%d drills, %d planted, errors: %d" % (len(drills), planted_total, errors))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
