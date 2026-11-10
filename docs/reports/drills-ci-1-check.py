"""Check for drill pack ci 1 (patterns hashing and prefix-sums, tag pack-1).

For every pack-1 drill it runs the model `solution` and an independent slow method on every
example and hidden test, and both must equal `expect`. It checks the claim in each brief's
worked example, that the untouched starter fails at least one hidden test, that the model
solution takes under a second per test in CPython, and that every planted wrong solution
fails at least one hidden test (a wrong answer, an error, or more than 5 s on one test).
Exit 0 when everything holds.

Run: <scratchpad>/venv/bin/python docs/reports/drills-ci-1-check.py
"""
import bisect
import itertools
import json
import math
import os
import signal
import sys
import time
from collections import Counter

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "drills")
LIMIT = 5.0


# ---------------------------------------------------------------- slow methods
def count_code_classes(codes):
    def reach(c):
        # every code reachable by swaps: all orderings of the even letters and of the odd letters
        ev, od = c[0::2], c[1::2]
        out = set()
        for pe in set(itertools.permutations(ev)):
            for po in set(itertools.permutations(od)):
                s = [""] * len(c)
                s[0::2], s[1::2] = pe, po
                out.add("".join(s))
        return frozenset(out)

    if all(len(c) <= 6 for c in codes) and len(codes) <= 50:
        return len({reach(c) for c in codes})
    # independent key: a count of (parity, letter) pairs plus the length
    return len({(len(c), frozenset(Counter((i % 2, ch) for i, ch in enumerate(c)).items())) for c in codes})


def count_steady_pairs(prices):
    n = len(prices)
    if n <= 2000:
        return sum(1 for i in range(n) for j in range(i + 1, n) if prices[j] - prices[i] == j - i)
    keys = np.array(prices, dtype=np.int64) - np.arange(n, dtype=np.int64)
    _, c = np.unique(keys, return_counts=True)
    return int((c * (c - 1) // 2).sum())


def count_row_column_matches(grid):
    if not grid:
        return 0
    g = np.array(grid, dtype=np.int64)
    return int(sum((g[r][None, :] == g.T).all(axis=1).sum() for r in range(len(g))))


def shortest_peak_stretch(badges):
    n = len(badges)
    if n == 0:
        return 0
    if n <= 300:
        peak = max(Counter(badges).values())
        return min(j - i for i in range(n) for j in range(i + 1, n + 1) if max(Counter(badges[i:j]).values()) == peak)
    pos = {}
    for i, b in enumerate(badges):
        pos.setdefault(b, []).append(i)
    peak = max(len(p) for p in pos.values())
    return min(p[-1] - p[0] + 1 for p in pos.values() if len(p) == peak)


def longest_serial_run(serials):
    s = sorted(set(serials))
    best = [0, 0]
    for _, grp in itertools.groupby(enumerate(s), key=lambda t: t[1] - t[0]):
        run = [v for _, v in grp]
        if len(run) > best[1]:
            best = [run[0], len(run)]
    return best


def count_mean_stretches(pnl, target):
    n = len(pnl)
    if n <= 2000:
        pre = list(itertools.accumulate(pnl, initial=0))
        return sum(1 for i in range(n) for j in range(i + 1, n + 1) if pre[j] - pre[i] == target * (j - i))
    pre = np.concatenate([[0], np.cumsum(np.array(pnl, dtype=np.int64) - target)])
    _, c = np.unique(pre, return_counts=True)
    return int((c * (c - 1) // 2).sum())


def best_block_sum(grid, s):
    g = np.array(grid, dtype=np.int64)
    w = np.lib.stride_tricks.sliding_window_view(g, (s, s))
    return int(w.sum(axis=(2, 3)).max())


def solve_unique_counts(text):
    tok = text.split()
    n = int(tok[0])
    counts = sorted(Counter(tok[1:1 + n]).values(), reverse=True)
    if math.prod(c + 1 for c in counts) <= 200000:
        # true brute force: every choice of how many items to keep per code
        best = None
        for keep in itertools.product(*[range(c + 1) for c in counts]):
            pos = [k for k in keep if k > 0]
            if len(pos) == len(set(pos)):
                r = sum(counts) - sum(keep)
                best = r if best is None else min(best, r)
        return str(best if best is not None else 0)
    used, removed = set(), 0
    for c in counts:
        k = c
        while k > 0 and k in used:
            k -= 1
        removed += c - k
        if k:
            used.add(k)
    return str(removed)


def count_zero_quads(a, b, c, d):
    if not (a and b and c and d):
        return 0
    ab = (np.array(a, dtype=np.int64)[:, None] + np.array(b, dtype=np.int64)[None, :]).ravel()
    cd = -(np.array(c, dtype=np.int64)[:, None] + np.array(d, dtype=np.int64)[None, :]).ravel()
    u1, c1 = np.unique(ab, return_counts=True)
    u2, c2 = np.unique(cd, return_counts=True)
    _, i1, i2 = np.intersect1d(u1, u2, return_indices=True)
    return int((c1[i1] * c2[i2]).sum())


def longest_even_vowels(tape):
    n = len(tape)
    if n <= 300:
        return max((j - i for i in range(n) for j in range(i + 1, n + 1)
                    if all(tape[i:j].count(v) % 2 == 0 for v in "aeiou")), default=0)
    bits = np.array([{"a": 1, "e": 2, "i": 4, "o": 8, "u": 16}.get(ch, 0) for ch in tape], dtype=np.int64)
    masks = np.concatenate([[0], np.bitwise_xor.accumulate(bits)])
    best = 0
    for m in np.unique(masks):
        where = np.flatnonzero(masks == m)
        best = max(best, int(where[-1] - where[0]))
    return best


def others_product_grid(grid):
    # group equal values: a cell's answer is the product over distinct values w of w^(count - [w is this cell])
    M = 10010
    cnt = Counter(v for row in grid for v in row)
    full = {}
    for v in cnt:
        p = 1
        for w, k in cnt.items():
            p = p * pow(w, k - (1 if w == v else 0), M) % M
        full[v] = p
    return [[full[v] for v in row] for row in grid]


def solve_equal_three(text):
    tok = text.split()
    n = int(tok[0])
    s = tok[1] if n else ""
    if n <= 300:
        return str(sum(1 for i in range(n) for j in range(i + 1, n + 1)
                       if s[i:j].count("A") == s[i:j].count("B") == s[i:j].count("C")))
    arr = np.frombuffer(s.encode(), dtype=np.uint8)
    a = np.concatenate([[0], np.cumsum(arr == 65)])
    b = np.concatenate([[0], np.cumsum(arr == 66)])
    c = np.concatenate([[0], np.cumsum(arr == 67)])
    key = (a - b) * (4 * n + 1) + (b - c)
    _, k = np.unique(key, return_counts=True)
    return str(int((k * (k - 1) // 2).sum()))


def cells_covered_at_least(rows, cols, rects, m):
    cov = np.zeros((rows, cols), dtype=np.int64)
    for r1, c1, r2, c2 in rects:
        cov[r1:r2 + 1, c1:c2 + 1] += 1
    return int((cov >= m).sum())


def count_target_blocks(grid, target):
    g = np.array(grid, dtype=np.int64)
    R, C = g.shape
    P = np.zeros((R + 1, C + 1), dtype=np.int64)
    P[1:, 1:] = g.cumsum(0).cumsum(1)
    iu = np.triu_indices(C + 1, 1)
    total = 0
    for r1 in range(R + 1):
        for r2 in range(r1 + 1, R + 1):
            band = P[r2] - P[r1]
            total += int(((band[None, :] - band[:, None])[iu] == target).sum())
    return total


def shortest_cut_to_multiple(lots, p):
    n = len(lots)
    total = sum(lots)
    if total % p == 0:
        return 0
    pre = list(itertools.accumulate(lots, initial=0))
    if n <= 2000:
        lens = [j - i for i in range(n) for j in range(i + 1, n + 1) if j - i < n and (total - pre[j] + pre[i]) % p == 0]
        return min(lens, default=-1)
    need = total % p
    pos = {}
    for i, v in enumerate(pre):
        pos.setdefault(v % p, []).append(i)
    best = None
    for j in range(1, n + 1):
        lst = pos.get((pre[j] - need) % p, [])
        k = bisect.bisect_left(lst, j) - 1
        if k >= 0 and j - lst[k] < n and (best is None or j - lst[k] < best):
            best = j - lst[k]
    return -1 if best is None else best


SLOW = {f.__name__: f for f in [count_code_classes, count_steady_pairs, count_row_column_matches, shortest_peak_stretch,
        longest_serial_run, count_mean_stretches, best_block_sum, solve_unique_counts, count_zero_quads,
        longest_even_vowels, others_product_grid, solve_equal_three, cells_covered_at_least, count_target_blocks,
        shortest_cut_to_multiple]}

# The worked example in each brief, recomputed by the slow method.
BRIEF = {
    "ci-code-classes": ('count_code_classes(["mnop", "onmp", "mpon", "nmop"])', 2),
    "ci-steady-climbs": ("count_steady_pairs([5, 6, 4, 8, 9])", 6),
    "ci-row-column-matches": ("count_row_column_matches([[1, 2], [2, 1]])", 2),
    "ci-peak-stretch": ("shortest_peak_stretch([4, 8, 8, 5, 4])", 2),
    "ci-serial-runs": ("longest_serial_run([50, 7, 90, 5, 8, 6, 9])", [5, 5]),
    "ci-mean-stretches": ("count_mean_stretches([2, 4, 3, 1, 5], 3)", 6),
    "ci-best-block": ("best_block_sum([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2)", 28),
    "ci-unique-counts": ('solve_unique_counts("5\\nAX BY AX CZ BY\\n")', "2"),
    "ci-zero-quads": ("count_zero_quads([2, 3], [-3, 1], [-1, 4], [1, -2])", 2),
    "ci-even-vowels": ('longest_even_vowels("xaeyea")', 6),
    "ci-others-product": ("others_product_grid([[2, 5], [3, 7]])", [[105, 42], [70, 30]]),
    "ci-equal-three": ('solve_equal_three("5\\nABCAB\\n")', "3"),
    "ci-camera-cover": ("cells_covered_at_least(3, 3, [[0, 0, 1, 1], [1, 1, 2, 2]], 2)", 1),
    "ci-target-blocks": ("count_target_blocks([[2, 1], [1, 2]], 3)", 4),
    "ci-trim-to-multiple": ("shortest_cut_to_multiple([6, 5, 1, 6], 7)", 2),
}
# Hand sums for the same examples (computed a second way, by reading the brief).
assert 2 + 1 - 1 - 2 == 0 and 3 - 3 - 1 + 1 == 0
assert [5 * 3 * 7, 2 * 3 * 7, 2 * 5 * 7, 2 * 5 * 3] == [105, 42, 70, 30]
assert max(1 + 2 + 4 + 5, 2 + 3 + 5 + 6, 4 + 5 + 7 + 8, 5 + 6 + 8 + 9) == 28
assert (6 + 5 + 1 + 6) % 7 == 4 and (1 + 6) % 7 == 0 and all((18 - x) % 7 for x in [6, 5, 1, 6])
assert sum(1 for k in [5 - 0, 6 - 1, 4 - 2, 8 - 3, 9 - 4] if k == 5) == 4 and 4 * 3 // 2 == 6


class Slow(Exception):
    pass


def _alarm(*_):
    raise Slow()


signal.signal(signal.SIGALRM, _alarm)


def evaluate(src, call, limit=None):
    ns = {}
    exec(src, ns)
    if limit:
        signal.setitimer(signal.ITIMER_REAL, limit)
    try:
        return eval(call, ns)
    finally:
        if limit:
            signal.setitimer(signal.ITIMER_REAL, 0)


def main():
    errors = 0
    files = sorted(f for f in os.listdir(ROOT) if f.startswith("ci-") and f.endswith(".json"))
    drills = [json.load(open(os.path.join(ROOT, f))) for f in files]
    drills = [d for d in drills if "pack-1" in d.get("tags", [])]
    diffs = Counter(d["difficulty"] for d in drills)
    if len(drills) != 15 or diffs != Counter({2: 3, 3: 5, 4: 5, 5: 2}):
        errors += 1
        print("pack shape wrong:", len(drills), dict(diffs))
    if sum("stdin" in d["tags"] for d in drills) != 2:
        errors += 1
        print("expected two stdin drills")
    only = sys.argv[1:]
    for d in drills:
        if only and d["id"] not in only:
            continue
        fn = d["fn"]
        if d["tags"][0] != "pack-1" or d["pattern"] not in ("hashing", "prefix-sums") or not 900 <= d["pace"] <= 2700:
            errors += 1
            print("FIELDS", d["id"])
        slow_ns = {fn: SLOW[fn]}
        call, want = BRIEF[d["id"]]
        if eval(call, dict(slow_ns)) != want:
            errors += 1
            print("BRIEF", d["id"], call)
        worst = 0.0
        for case in d["examples"] + d["tests"]:
            want = eval(case["expect"])
            t0 = time.time()
            got_model = evaluate(d["solution"], case["call"])
            worst = max(worst, time.time() - t0)
            got_slow = eval(case["call"], dict(slow_ns))
            if got_model != want:
                errors += 1
                print("MODEL", d["id"], case["call"][:70], repr(got_model)[:60], "!=", repr(want)[:60])
            if got_slow != want:
                errors += 1
                print("SLOW ", d["id"], case["call"][:70], repr(got_slow)[:60], "!=", repr(want)[:60])
        if worst > 1.0:
            errors += 1
            print("MODEL too slow in CPython:", d["id"], round(worst, 2))
        starter_fails = 0
        for case in d["tests"]:
            try:
                if evaluate(d["starter"], case["call"]) != eval(case["expect"]):
                    starter_fails += 1
            except Exception:
                starter_fails += 1
        if starter_fails == 0:
            errors += 1
            print("STARTER passes every test:", d["id"])
        caught = []
        for k, p in enumerate(d.get("planted", [])):
            why = None
            for t, case in enumerate(d["tests"]):
                try:
                    if evaluate(p["code"], case["call"], LIMIT) != eval(case["expect"]):
                        why = "wrong on test %d" % t
                except Slow:
                    why = "over %ds on test %d" % (LIMIT, t)
                except Exception as e:
                    why = "%s on test %d" % (type(e).__name__, t)
                if why:
                    break
            if why is None:
                errors += 1
                print("PLANTED passes every test:", d["id"], k, p["slip"][:60])
            caught.append(why or "PASSES")
        if len(caught) < 2:
            errors += 1
            print("fewer than two planted:", d["id"])
        print("%-22s d%d %2d tests, starter fails %2d, model %.2fs; planted: %s"
              % (d["id"], d["difficulty"], len(d["tests"]), starter_fails, worst, "; ".join(caught)))
    print("errors:", errors)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
