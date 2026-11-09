"""Check for drill sub-pack A (pack dsa: hashing, prefix sums, simulation).

For every drill file it runs the model `solution` and an independent slow method on
every example and hidden test, and both must equal `expect`. It also checks that the
untouched starter fails at least one hidden test. Exit 0 when everything holds.

Run: <scratchpad>/venv/bin/python docs/reports/drills-dsa-a-check.py
"""
import bisect
import itertools
import json
import os
import re
import sys

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "drills")


# ---------------------------------------------------------------- slow methods
def majority_reading(readings):
    # sort, then measure each run of equal values
    for v, run in itertools.groupby(sorted(readings)):
        if 2 * len(list(run)) > len(readings):
            return v
    return None


def silent_sensors(expected, reported):
    # binary search in a sorted copy of the log
    log = sorted(reported)
    out = []
    for s in expected:
        i = bisect.bisect_left(log, s)
        if i == len(log) or log[i] != s:
            out.append(s)
    return out


def solve_kth_repeat(text):
    # positions of every id; the flagged id has the earliest k-th position
    tokens = re.findall(r"\S+", text)
    n, k = int(tokens[0]), int(tokens[1])
    where = {}
    for pos, oid in enumerate(tokens[2:2 + n]):
        where.setdefault(oid, []).append(pos)
    best = None
    for oid, ps in where.items():
        if len(ps) >= k and (best is None or ps[k - 1] < best[0]):
            best = (ps[k - 1], oid)
    return "NONE" if best is None else best[1]


def traders_by_ticker(trades):
    # first index of each distinct pair, then tickers in first-seen order
    first = {}
    for i, pair in enumerate(trades):
        if pair not in first:
            first[pair] = i
    tickers = []
    for trader, ticker in sorted(first, key=first.get):
        if ticker not in tickers:
            tickers.append(ticker)
    return {t: [tr for tr, tk in sorted(first, key=first.get) if tk == t] for t in tickers}


def largest_shape_group(traces):
    if len(traces) <= 300:
        # true brute force: compare every pair directly
        best = 0
        for a in traces:
            same = sum(1 for b in traces if len(a) == len(b) and len({x - y for x, y in zip(a, b)}) == 1)
            best = max(best, same)
        return best
    # independent key: subtract the minimum, then count equal keys after sorting
    keys = sorted(tuple(x - min(t) for x in t) for t in traces)
    return max((len(list(g)) for _, g in itertools.groupby(keys)), default=0)


def first_overdrawn_day(opening, flows):
    for day, bal in enumerate(itertools.accumulate(flows, initial=opening)):
        if day > 0 and bal < 0:
            return day - 1
    return -1


def solve_range_volumes(text):
    lines = [ln.split() for ln in text.split("\n") if ln.strip()]
    n, q = int(lines[0][0]), int(lines[0][1])
    v = np.array([int(x) for x in lines[1]], dtype=np.int64)
    out = []
    for l, r in lines[2:2 + q]:
        l, r = int(l), int(r)
        # bars l+1..r (1-based) each against the bar before it: 0-based indices l..r-1 against l-1..r-2
        out.append(str(int((v[l:r] > v[l - 1:r - 1]).sum())))
    return "\n".join(out)


def staff_per_hour(hours, shifts):
    # staff at h = shifts started by h minus shifts ended before h
    starts = sorted(s for s, _ in shifts)
    ends = sorted(e for _, e in shifts)
    return [bisect.bisect_right(starts, h) - bisect.bisect_left(ends, h) for h in range(hours)]


def flattest_stretch(pnl):
    # every start and end day, vectorised over the end day
    pre = np.concatenate([[0], np.cumsum(np.array(pnl, dtype=np.int64))])
    best = None
    for i in range(len(pnl)):
        m = int(np.abs(pre[i + 1:] - pre[i]).min())
        best = m if best is None else min(best, m)
    return best


def longest_winning_stretch(pnl):
    # every start day, vectorised over the end day: wins minus losses must be positive
    if not pnl:
        return 0
    s = np.concatenate([[0], np.cumsum(np.where(np.array(pnl) > 0, 1, -1))])
    best = 0
    for i in range(len(pnl)):
        ends = np.nonzero(s[i + 1:] - s[i] > 0)[0]
        if len(ends):
            best = max(best, int(ends[-1]) + 1)
    return best


def push_empty_to_back(qty):
    keep = [x for x in qty if x != 0]
    qty[:] = keep + [0] * (len(qty) - len(keep))
    return qty


def trailing_stop_exit(prices, gap):
    if len(prices) < 2:
        return -1
    p = np.array(prices, dtype=np.int64)
    high = np.maximum.accumulate(p)[:-1]
    hit = np.nonzero(p[1:] <= high - gap)[0]
    return int(hit[0]) + 1 if len(hit) else -1


def solve_stock_ledger(text):
    # each item's lines can be replayed on their own, as no line touches two items
    lines = text.split("\n")
    n = int(lines[0])
    per_item = {}
    for ln in lines[1:1 + n]:
        op, item, k = ln.split()
        per_item.setdefault(item, []).append((op, int(k)))
    refused = 0
    left = {}
    for item, moves in per_item.items():
        have = 0
        for op, k in moves:
            if op == "IN":
                have += k
            elif k <= have:
                have -= k
            else:
                refused += 1
        if have:
            left[item] = have
    return "\n".join([str(refused)] + ["%s %d" % (i, left[i]) for i in sorted(left)])


def rotate_rota(staff, k):
    if staff:
        k %= len(staff)
        staff[:] = staff[len(staff) - k:] + staff[:len(staff) - k]
    return staff


def position_after(route, steps):
    step = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
    if steps <= 10 ** 6:
        # walk every move
        x = y = 0
        for i in range(steps):
            dx, dy = step[route[i % len(route)]]
            x, y = x + dx, y + dy
        return [x, y]
    # move j runs once per pass, plus once more if it lies in the leftover
    full, rest = divmod(steps, len(route))
    dx = np.array([step[c][0] for c in route], dtype=object)
    dy = np.array([step[c][1] for c in route], dtype=object)
    times = np.array([full + (1 if j < rest else 0) for j in range(len(route))], dtype=object)
    return [int((dx * times).sum()), int((dy * times).sum())]


SLOW = {name: fn for name, fn in globals().items() if callable(fn) and not name.startswith("_")}


def evaluate(code, call):
    ns = {}
    exec(code, ns)
    return eval(call, ns)


def main():
    errors = 0
    files = sorted(f for f in os.listdir(ROOT) if f.startswith("dsa-") and f.endswith(".json"))
    pack_a = {"hashing", "prefix-sums", "simulation"}
    seen = 0
    for f in files:
        d = json.load(open(os.path.join(ROOT, f)))
        if d.get("pattern") not in pack_a:
            continue
        seen += 1
        fn = d["fn"]
        slow_ns = {fn: SLOW[fn], "np": np}
        starter_fails = 0
        for case in d["examples"] + d["tests"]:
            want = eval(case["expect"])
            got_model = evaluate(d["solution"], case["call"])
            got_slow = eval(case["call"], dict(slow_ns))
            if got_model != want:
                errors += 1
                print("MODEL", d["id"], case["call"][:70], got_model, "!=", want)
            if got_slow != want:
                errors += 1
                print("SLOW ", d["id"], case["call"][:70], repr(got_slow)[:60], "!=", repr(want)[:60])
        for case in d["tests"]:
            try:
                if evaluate(d["starter"], case["call"]) != eval(case["expect"]):
                    starter_fails += 1
            except Exception:
                starter_fails += 1
        if starter_fails == 0:
            errors += 1
            print("STARTER passes every test:", d["id"])
        print("%-24s %2d tests, starter fails %d" % (d["id"], len(d["tests"]), starter_fails))
    if seen != 15:
        errors += 1
        print("expected 15 drills, found", seen)
    print("errors:", errors)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
