"""Check for drill sub-pack B (pack dsa): two-pointers, windows, stacks-queues, binary-search.

For every drill it runs the model solution on every example and hidden test, and an
independent method written here (brute force on small inputs; on the large inputs, where
brute force cannot finish, a different algorithm or a closed form; the one 10^9-lot netting case is worked by hand in a comment). Both must
equal every `expect`. It also checks that the starter fails at least one test. Exit 0 on success.
Run: <scratchpad>/venv/bin/python docs/reports/drills-dsa-b-check.py
"""
import json, math, os, re, sys
from bisect import bisect_left, bisect_right
from collections import Counter
from fractions import Fraction
from itertools import accumulate

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DRILLS = os.path.join(HERE, "..", "..", "app", "content", "drills")
SMALL = 3000

# ---------------- independent methods ----------------

def count_pairs_within(p, budget):
    n = len(p)
    if n <= SMALL:
        return sum(1 for i in range(n) for j in range(i + 1, n) if p[i] + p[j] <= budget)
    return sum(bisect_right(p, budget - p[i], i + 1) - (i + 1) for i in range(n))

def closest_pair_gap(sizes, target):
    n = len(sizes)
    if n <= SMALL:
        return min(abs(sizes[i] + sizes[j] - target) for i in range(n) for j in range(n) if i != j)
    s = sorted(sizes)
    best = None
    for i, x in enumerate(s):
        k = bisect_left(s, target - x)
        for j in (k - 1, k, k + 1, i - 1, i + 1):
            if 0 <= j < n and j != i:
                g = abs(x + s[j] - target)
                best = g if best is None else min(best, g)
    return best

def ints(text):
    return [int(v) for v in re.findall(r"-?\d+", text)]

def solve_near_trades(text):
    v = ints(text)
    n, d, t = v[0], v[1], v[2:2 + v[0]]
    if n <= SMALL:
        c = sum(1 for i in range(n) for j in range(i + 1, n) if t[j] - t[i] <= d)
    else:
        c = sum(j - bisect_left(t, t[j] - d, 0, j) for j in range(n))
    return str(c)

def solve_sensor_alarm(text):
    v = ints(text)
    n, k, t, xs = v[0], v[1], v[2], v[3:3 + v[0]]
    if k > n:
        return "0"
    if n * k <= 10 ** 6:
        return str(sum(1 for i in range(n - k + 1) if Fraction(sum(xs[i:i + k]), k) >= t))
    P = [0] + list(accumulate(xs))
    return str(sum(1 for i in range(n - k + 1) if Fraction(P[i + k] - P[i], k) >= t))

def longest_stretch_within(f, budget):
    n = len(f)
    if n <= SMALL:
        best = 0
        for i in range(n):
            for j in range(i, n):
                if sum(f[i:j + 1]) <= budget:
                    best = max(best, j - i + 1)
        return best
    P = [0] + list(accumulate(f))
    return max([r + 1 - bisect_left(P, P[r + 1] - budget, 0, r + 2) for r in range(n)] + [0])

def solve_ticket_desk(text):
    v = ints(text)
    n = v[0]
    arr = v[1:1 + 2 * n:2]
    ser = v[2:2 + 2 * n:2]
    starts, free = [], 0
    for a, s in zip(arr, ser):
        st = max(a, free)
        starts.append(st)
        free = st + s
    waited = sum(st - a for st, a in zip(starts, arr))
    if n <= SMALL:
        longest = max([sum(1 for j in range(n) if arr[j] <= m and starts[j] > m) for m in arr] + [0])
    else:
        longest = max([bisect_right(arr, m) - bisect_right(starts, m) for m in arr] + [0])
    return f"{waited} {free if n else 0} {longest}"

def largest_depth_block(d):
    n = len(d)
    if n <= 2000:
        best = 0
        for i in range(n):
            low = d[i]
            for j in range(i, n):
                low = min(low, d[j])
                best = max(best, low * (j - i + 1))
        return best
    vals = sorted(set(d))
    if len(vals) <= 2000:  # for each depth level v, the longest run with every depth >= v
        a = np.array(d)
        best = 0
        for v in vals:
            m = np.concatenate(([0], (a >= v).astype(np.int8), [0]))
            e = np.flatnonzero(np.diff(m))
            run = int((e[1::2] - e[::2]).max()) if len(e) else 0
            best = max(best, v * run)
        return best
    assert d == sorted(d) and len(vals) == n  # strictly rising: best block starting at i runs to the end
    return max(d[i] * (n - i) for i in range(n))


def plan_filled_in_order(tape, plan):
    it = iter(tape)  # `x in it` consumes the iterator up to the first match
    return all(x in it for x in plan)

def _good_starts(xs, k):
    """Starts i of windows xs[i:i+k] with no repeat, by marking the starts each repeat spoils."""
    n = len(xs)
    if k > n:
        return 0
    bad = [0] * (n + 2)
    last = {}
    for j, x in enumerate(xs):
        if x in last:  # starts in (last[x], j] that also reach j spoil, i.e. max(last+1, j-k+1) .. min(last[x], j)
            lo, hi = max(0, j - k + 1), last[x]
            if lo <= hi:
                bad[lo] += 1
                bad[hi + 1] -= 1
        last[x] = j
    run, good = 0, 0
    for i in range(n - k + 1):
        run += bad[i]
        good += run == 0
    return good

def count_varied_windows(badges, k):
    n = len(badges)
    if n * k <= 10 ** 6:
        return sum(1 for i in range(n - k + 1) if len(set(badges[i:i + k])) == k) if k <= n else 0
    return _good_starts(badges, k)

def longest_without_repeat(rota):
    n = len(rota)
    if n <= SMALL:
        best = 0
        for i in range(n):
            seen = set()
            for j in range(i, n):
                if rota[j] in seen:
                    break
                seen.add(rota[j])
                best = max(best, j - i + 1)
        return best
    lo, hi = 0, n  # binary search on the length, each length checked by _good_starts
    while lo < hi:
        mid = (lo + hi + 1) // 2
        lo, hi = (mid, hi) if _good_starts(rota, mid) > 0 else (lo, mid - 1)
    return lo

def bracket_partners(formula):
    br = [(i, ch) for i, ch in enumerate(formula) if ch in "()[]{}"]
    if len(br) <= SMALL:  # remove adjacent matching pairs until none is left
        pairs = []
        while br:
            for t in range(len(br) - 1):
                if br[t][1] + br[t + 1][1] in ("()", "[]", "{}"):
                    pairs.append((br[t][0], br[t + 1][0]))
                    del br[t:t + 2]
                    break
        return sorted(pairs)
    depth, last, pairs = 0, {}, []  # the partner of a closer is the last opener at its depth
    for i, ch in br:
        if ch in "([{":
            depth += 1
            last[depth] = i
        else:
            pairs.append((last[depth], i))
            depth -= 1
    return sorted(pairs)

def net_tape(orders):
    if sum(abs(q) for q in orders) > 2 * 10 ** 6:
        assert orders == [10 ** 9, -1, -(10 ** 9)]
        return [-1]  # by hand: 10^9 rests, -1 leaves 999,999,999, the last sell uses it and rests as -1
    lots = []  # one entry per lot: +1 a resting buy lot, -1 a resting sell lot, with an order tag
    for tag, q in enumerate(orders):
        if q > 0:
            lots.extend([(1, tag)] * q)
        else:
            for _ in range(-q):
                if lots and lots[-1][0] == 1:
                    lots.pop()
                else:
                    lots.append((-1, tag))
    out = []
    for sign, tag in lots:
        if out and out[-1][1] == tag:
            out[-1][0] += sign
        else:
            out.append([sign, tag])
    return [v for v, _ in out]

_memo = {}
def _cached(fn):
    def wrap(xs):
        if len(xs) < 10000:  # only the big repeated lists are cached (ids of small temporaries get reused)
            return fn(xs)
        key = (fn.__name__, id(xs), len(xs))
        if key not in _memo:
            _memo[key] = fn(xs)
        return _memo[key]
    wrap.__name__ = fn.__name__
    return wrap

@_cached
def missing_seq_number(seqs):
    (gap,) = set(range(seqs[0], seqs[-1] + 1)) - set(seqs)
    return gap

@_cached
def peak_index(path):
    return path.index(max(path))

def _spread_ok(s, gap, k):
    count, last = 0, None
    for x in s:
        if last is None or x - last >= gap:
            count, last = count + 1, x
    return count >= k

def widest_spacing(sites, k):
    from itertools import combinations
    s = sorted(sites)
    if len(s) <= 12:
        return max(min(b - a for a, b in zip(c, c[1:])) for c in combinations(s, k))
    g = (s[-1] - s[0]) // (k - 1)  # no spacing can beat the even split; walk down from it
    while not _spread_ok(s, g, k):
        g -= 1
    return g

INDEP = {f.__name__: f for f in [plan_filled_in_order, count_pairs_within, closest_pair_gap, solve_near_trades,
                                  solve_sensor_alarm, count_varied_windows, longest_stretch_within, longest_without_repeat,
                                  bracket_partners, net_tape, solve_ticket_desk, largest_depth_block,
                                  missing_seq_number, peak_index, widest_spacing]}
MINE = ["dsa-fills-in-order", "dsa-cheap-pairs", "dsa-closest-hedge", "dsa-near-trades", "dsa-sensor-alarm",
        "dsa-varied-windows", "dsa-budget-stretch", "dsa-oncall-rota", "dsa-bracket-partners", "dsa-net-tape",
        "dsa-ticket-desk", "dsa-depth-block", "dsa-missing-seq", "dsa-price-peak", "dsa-kiosk-spacing"]

# ---------------- runner ----------------

def run(code, call, extra=None):
    ns = dict(extra or {})
    if code is not None:
        exec(code, ns)
    return eval(call, ns)

def same(a, b):
    return type(a) == type(b) and a == b

def main():
    errors = 0
    diffs, stdin = Counter(), 0
    for did in MINE:
        d = json.load(open(os.path.join(DRILLS, did + ".json")))
        fn = d["fn"]
        diffs[d["difficulty"]] += 1
        stdin += "stdin" in d.get("tags", [])
        if "stdin" in d.get("tags", []):
            assert fn.startswith("solve_"), did
        assert d["pack"] == "dsa" and 480 <= d["pace"] <= 1500, did
        assert 10 <= len(d["tests"]) <= 14 and 2 <= len(d["examples"]) <= 3, did
        assert all(e.get("note") for e in d["examples"]) and len(d["notes"]) == 3, did
        assert not any("setup" in c for c in d["tests"] + d["examples"]), did  # the drill page ignores setup
        starter_fails = 0
        for kind, cases in (("example", d["examples"]), ("test", d["tests"])):
            for i, c in enumerate(cases):
                want = eval(c["expect"])
                got = run(d["solution"], c["call"])
                if not same(got, want):
                    print(f"FAIL {did} {kind} {i}: solution gave {got!r:.60}, expect {want!r:.60}"); errors += 1
                indep = run(None, c["call"], {fn: INDEP[fn]})
                if not same(indep, want):
                    print(f"FAIL {did} {kind} {i}: independent gave {indep!r:.60}, expect {want!r:.60}"); errors += 1
                if kind == "test":
                    try:
                        starter_fails += not same(run(d["starter"], c["call"]), want)
                    except Exception:
                        starter_fails += 1
        if starter_fails == 0:
            print(f"FAIL {did}: starter passes every test"); errors += 1
        print(f"ok {did}: {len(d['examples'])} examples, {len(d['tests'])} tests, starter fails {starter_fails}")
    if diffs != Counter({1: 5, 2: 6, 3: 4}) or stdin != 3:
        print(f"FAIL mix: difficulties {dict(diffs)}, stdin {stdin}"); errors += 1
    print(f"{len(MINE)} drills, {errors} errors")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
