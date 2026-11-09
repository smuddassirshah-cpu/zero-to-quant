"""Check for drill sub-pack C (pack dsa: trees, heaps and tries, intervals).

For every drill file it runs the model `solution` and an independent slow method on
every example and hidden test, and both must equal `expect`. It also checks that the
untouched starter fails at least one hidden test, and it compares each model with a
brute force on random small inputs. Exit 0 when everything holds.

Run: <scratchpad>/venv/bin/python docs/reports/drills-dsa-c-check.py
"""
import bisect
import heapq
import itertools
import json
import os
import random
import re
import sys
from collections import deque

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "drills")


def inorder(tree):
    # iterative left, node, right reading
    out, stack, node = [], [], tree
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node[1]
        node = stack.pop()
        out.append(node[0])
        node = node[2]
    return out


# ---------------------------------------------------------------- slow methods
def route_order(legs):
    # walk backwards from the tail through a reverse dict
    prev = {after: stop for stop, after in legs if after is not None}
    tail = next((stop for stop, after in legs if after is None), None)
    out = []
    while tail is not None:
        out.append(tail)
        tail = prev.get(tail)
    return out[::-1]


def solve_shared_tail(text):
    # mark queue A in a set, walk queue B
    tok = re.findall(r"-?\d+", text)
    n, a, b = int(tok[0]), int(tok[1]), int(tok[2])
    nxt = list(map(int, tok[3:3 + n]))
    seen = set()
    while a != -1:
        seen.add(a)
        a = nxt[a]
    while b != -1 and b not in seen:
        b = nxt[b]
    return str(b)


def fewest_checks(tree):
    # breadth-first: the first leaf met is the shallowest
    if tree is None:
        return 0
    queue = deque([(tree, 1)])
    while queue:
        node, depth = queue.popleft()
        if node[1] is None and node[2] is None:
            return depth
        for child in node[1:]:
            if child is not None:
                queue.append((child, depth + 1))


def shared_manager(chart, a, b):
    # parent map, ancestors of a, then climb from b
    parent, stack = {chart[0]: None}, [chart]
    while stack:
        node = stack.pop()
        for child in node[1:]:
            if child is not None:
                parent[child[0]] = node[0]
                stack.append(child)
    ups = set()
    while a is not None:
        ups.add(a)
        a = parent[a]
    while b not in ups:
        b = parent[b]
    return b


def nearest_levels(book, prices):
    # sorted levels and bisect
    levels = inorder(book)
    out = []
    for p in prices:
        i = bisect.bisect_left(levels, p)
        cands = levels[max(0, i - 1):i + 1]
        out.append(min(cands, key=lambda v: (abs(v - p), v)))
    return out


def swapped_levels(book):
    # compare the reading with its sorted copy
    seq = inorder(book) if book is not None else []
    wrong = [v for v, w in zip(seq, sorted(seq)) if v != w]
    assert len(wrong) in (0, 2), "test tree is not one swap away from a search tree"
    return sorted(wrong)


def nearest_strikes(strikes, spot, k):
    return sorted(strikes, key=lambda s: (abs(s - spot), s))[:k]


def short_codes(names):
    # longest common prefix with the sorted neighbours
    def lcp(x, y):
        m = 0
        while m < len(x) and m < len(y) and x[m] == y[m]:
            m += 1
        return m
    order = sorted(names)
    need = {}
    for i, w in enumerate(order):
        best = 0
        if i > 0:
            best = max(best, lcp(w, order[i - 1]))
        if i + 1 < len(order):
            best = max(best, lcp(w, order[i + 1]))
        need[w] = w[:min(len(w), best + 1)]
    return [need[w] for w in names]


def solve_print_queue(text):
    # buckets by page count, each in (arrival, id) order, and a heap of non-empty page counts
    tok = text.split()
    n = int(tok[0])
    jobs = sorted((int(tok[2 + 3 * i]), int(tok[1 + 3 * i]), int(tok[3 + 3 * i])) for i in range(n))
    buckets, live, out, clock, i = {}, [], [], 0, 0
    waiting = 0
    while len(out) < n:
        if waiting == 0 and clock < jobs[i][0]:
            clock = jobs[i][0]
        while i < n and jobs[i][0] <= clock:
            arr, jid, pages = jobs[i]
            if not buckets.get(pages):
                buckets[pages] = deque()
                heapq.heappush(live, pages)
            buckets[pages].append(jid)
            waiting += 1
            i += 1
        pages = live[0]
        out.append(str(buckets[pages].popleft()))
        waiting -= 1
        if not buckets[pages]:
            heapq.heappop(live)
        clock += pages
    return " ".join(out)


def tightest_window(feeds):
    # every distinct time as a start; numpy finds each venue's first time at or after it
    starts = np.unique(np.concatenate([np.array(f, dtype=np.int64) for f in feeds]))
    big = np.int64(1) << 62
    high = np.full(len(starts), -big, dtype=np.int64)
    for f in feeds:
        arr = np.array(f, dtype=np.int64)
        idx = np.searchsorted(arr, starts, side="left")
        val = np.where(idx < len(arr), arr[np.minimum(idx, len(arr) - 1)], big)
        high = np.maximum(high, val)
    length = high - starts
    j = int(np.argmin(length))
    return [int(starts[j]), int(high[j])]


def booked_minutes(bookings):
    # sweep over event points with a live counter
    events = sorted([(s, 1) for s, _ in bookings] + [(e, -1) for _, e in bookings])
    total, live, last = 0, 0, None
    for t, step in events:
        if live > 0:
            total += t - last
        live += step
        last = t
    return total


def any_clash(slots):
    # a clash exists exactly when the union is shorter than the sum of lengths
    return booked_minutes(slots) < sum(e - s for s, e in slots)


def solve_peak_calls(text):
    # longest busy stretch: live count on every stretch between distinct event times, via searchsorted
    tok = text.split()
    n, k = int(tok[0]), int(tok[1])
    s = np.array([int(tok[2 + 2 * i]) for i in range(n)], dtype=np.int64)
    e = np.array([int(tok[3 + 2 * i]) for i in range(n)], dtype=np.int64)
    ss, es = np.sort(s), np.sort(e)
    times = np.unique(np.concatenate((s, e)))
    live = np.searchsorted(ss, times, side="right") - np.searchsorted(es, times, side="right")
    best = run = 0
    for i in range(len(times) - 1):  # live[i] holds on [times[i], times[i + 1])
        if live[i] >= k:
            run += int(times[i + 1] - times[i])
            best = max(best, run)
        else:
            run = 0
    return str(best)


def fewest_shifts(shifts, close):
    # dp over shifts in end order: best[i] = fewest shifts covering 0 up to end_i, last one i
    order = sorted(shifts, key=lambda se: se[1])
    ends = [e for _, e in order]
    m = len(order)
    inf = float("inf")
    tree = [inf] * (m + 1)  # Fenwick, prefix min over reversed rank

    def update(pos, val):
        while pos <= m:
            tree[pos] = min(tree[pos], val)
            pos += pos & -pos

    def query(pos):
        out = inf
        while pos > 0:
            out = min(out, tree[pos])
            pos -= pos & -pos
        return out

    answer = inf
    for rank, (s, e) in enumerate(order):
        if s <= 0:
            best = 1
        else:
            lo = bisect.bisect_left(ends, s)  # ends >= s have rank >= lo
            best = 1 + query(m - lo) if lo < m else inf
        update(m - rank, best)
        if e >= close:
            answer = min(answer, best)
    return -1 if answer == inf else answer


def shortest_windows(windows, parcels):
    # windows by length; each claims the still-unanswered parcel times it covers (union-find skip)
    times = sorted(set(parcels))
    ans = {}
    skip = list(range(len(times) + 1))

    def find(i):
        while skip[i] != i:
            skip[i] = skip[skip[i]]
            i = skip[i]
        return i

    for s, e in sorted(windows, key=lambda w: w[1] - w[0]):
        i = find(bisect.bisect_left(times, s))
        while i < len(times) and times[i] < e:
            ans[times[i]] = e - s
            skip[i] = i + 1
            i = find(i + 1)
    return [ans.get(t, -1) for t in parcels]


SLOW = {name: fn for name, fn in globals().items() if callable(fn) and not name.startswith("_")}


# ---------------------------------------------------------------- brute forces for random checks
def rand_tree(rng, vals):
    if not vals:
        return None
    k = rng.randrange(len(vals))
    return (vals[k], rand_tree(rng, vals[:k]), rand_tree(rng, vals[k + 1:]))


def brute_cases(rng):
    """Yield (fn, args, brute answer) on small random inputs."""
    for _ in range(300):
        n = rng.randrange(1, 9)
        vals = rng.sample(range(-20, 40), n)
        tree = rand_tree(rng, sorted(vals))
        # swap two levels, or not
        seq = inorder(tree)
        if rng.random() < 0.8 and n >= 2:
            i, j = sorted(rng.sample(range(n), 2))
            swap = {seq[i]: seq[j], seq[j]: seq[i]}
            relabel = lambda t: None if t is None else (swap.get(t[0], t[0]), relabel(t[1]), relabel(t[2]))
            yield "swapped_levels", (relabel(tree),), sorted([seq[i], seq[j]])
        else:
            yield "swapped_levels", (tree,), []
        qs = [rng.randrange(-30, 50) for _ in range(5)]
        yield "nearest_levels", (tree, qs), [min(vals, key=lambda v: (abs(v - q), v)) for q in qs]
        a, b = rng.choice(vals), rng.choice(vals)
        # brute: lowest node whose subtree holds both

        def holds(t, x):
            return t is not None and (t[0] == x or holds(t[1], x) or holds(t[2], x))

        def lca(t):
            for child in t[1:]:
                if child is not None and holds(child, a) and holds(child, b):
                    return lca(child)
            return t[0]
        yield "shared_manager", (tree, a, b), lca(tree)

        def depths(t, d):
            if t[1] is None and t[2] is None:
                return [d]
            return [x for c in t[1:] if c is not None for x in depths(c, d + 1)]
        yield "fewest_checks", (tree,), min(depths(tree, 1))
        # intervals
        iv = []
        for _ in range(rng.randrange(0, 7)):
            s = rng.randrange(0, 15)
            iv.append([s, s + rng.randrange(1, 6)])
        minutes = set(m for s, e in iv for m in range(s, e))
        yield "booked_minutes", (iv,), len(minutes)
        yield "any_clash", (iv,), any(max(p[0], q[0]) < min(p[1], q[1]) for p, q in itertools.combinations(iv, 2))
        if iv:
            kk = rng.randrange(1, 5)
            text = "%d %d\n" % (len(iv), kk) + "\n".join("%d %d" % (s, e) for s, e in iv) + "\n"
            best = run = 0
            for t in range(0, 25):  # one second at a time
                if sum(s <= t < e for s, e in iv) >= kk:
                    run += 1
                    best = max(best, run)
                else:
                    run = 0
            yield "solve_peak_calls", (text,), str(best)
        close = rng.randrange(1, 15)
        best = -1
        for r in range(1, len(iv) + 1):
            if any(all(any(s <= t < e for s, e in c) for t in range(close)) for c in itertools.combinations(iv, r)):
                best = r
                break
        yield "fewest_shifts", (iv, close), best
        ps = [rng.randrange(-2, 22) for _ in range(rng.randrange(0, 6))]
        yield "shortest_windows", (iv, ps), [min([e - s for s, e in iv if s <= t < e], default=-1) for t in ps]
        # heaps and tries
        k = rng.randrange(1, 4)
        feeds = [sorted(rng.randrange(0, 20) for _ in range(rng.randrange(1, 4))) for _ in range(k)]
        allt = sorted(set(t for f in feeds for t in f))
        wins = [(hi - lo, lo, hi) for lo in allt for hi in allt if hi >= lo and all(any(lo <= t <= hi for t in f) for f in feeds)]
        _, lo, hi = min(wins)
        yield "tightest_window", (feeds,), [lo, hi]
        words = list(set("".join(rng.choice("ab") for _ in range(rng.randrange(1, 4))) for _ in range(rng.randrange(1, 6))))

        def code(w):
            for m in range(1, len(w) + 1):
                if sum(x.startswith(w[:m]) for x in words) == 1:
                    return w[:m]
            return w
        yield "short_codes", (words,), [code(w) for w in words]
        jobs = [(j, rng.randrange(0, 8), rng.randrange(1, 4)) for j in rng.sample(range(10), rng.randrange(0, 5))]
        text = "%d\n" % len(jobs) + "".join("%d %d %d\n" % j for j in jobs)
        clock, left, out = 0, list(jobs), []
        while left:
            ready = [j for j in left if j[1] <= clock]
            if not ready:
                clock = min(j[1] for j in left)
                continue
            j = min(ready, key=lambda j: (j[2], j[1], j[0]))
            left.remove(j)
            out.append(str(j[0]))
            clock += j[2]
        yield "solve_print_queue", (text,), " ".join(out)
        strikes = rng.sample(range(-10, 10), rng.randrange(0, 6))
        kk = rng.randrange(0, len(strikes) + 1)
        spot = rng.randrange(-12, 12)
        picked, pool = [], list(strikes)
        for _ in range(kk):
            s = min(pool, key=lambda s: (abs(s - spot), s))
            pool.remove(s)
            picked.append(s)
        yield "nearest_strikes", (strikes, spot, kk), picked
        # linked lists
        stops = ["s%d" % i for i in rng.sample(range(50), rng.randrange(0, 6))]
        legs = [[s, stops[i + 1] if i + 1 < len(stops) else None] for i, s in enumerate(stops)]
        rng.shuffle(legs)
        yield "route_order", (legs,), stops


def evaluate(code, call):
    ns = {}
    exec(code, ns)
    return eval(call, ns)


def main():
    errors = 0
    pack_c = {"trees", "heaps-tries", "intervals"}
    models = {}
    seen = 0
    for f in sorted(x for x in os.listdir(ROOT) if x.startswith("dsa-") and x.endswith(".json")):
        d = json.load(open(os.path.join(ROOT, f)))
        if d.get("pattern") not in pack_c:
            continue
        seen += 1
        fn = d["fn"]
        ns = {}
        exec(d["solution"], ns)
        models[fn] = ns[fn]
        starter_fails = 0
        for case in d["examples"] + d["tests"]:
            want = eval(case["expect"])
            got_model = evaluate(d["solution"], case["call"])
            got_slow = eval(case["call"], {fn: SLOW[fn]})
            if got_model != want:
                errors += 1
                print("MODEL", d["id"], case["call"][:70], repr(got_model)[:60], "!=", repr(want)[:60])
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
    rng = random.Random(18)
    checked = 0
    for fn, args, want in brute_cases(rng):
        checked += 1
        got = models[fn](*args)
        if got != want:
            errors += 1
            print("BRUTE", fn, repr(args)[:80], got, "!=", want)
    print("random brute-force cases:", checked)
    print("errors:", errors)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
