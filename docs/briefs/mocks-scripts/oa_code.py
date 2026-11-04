"""mock-oa-code: the eight drills of pack `oa` (ids `oa-*`), checked.

Run: python3 -I oa_code.py   (standard library only; deterministic, seeded)

For every problem the script holds
  * ref    the reference solution (the text shown in the brief is this source),
  * brute  an independent slow method (exhaustive, or a different algorithm),
  * stub   the starter the learner sees,
  * tests  (call, closed) rows: `closed` is a closed-form value for the large cases (or "ALT": a second fast
           algorithm), None for small ones, where `brute` supplies the second value.
It asserts: ref == brute on thousands of seeded random small cases; every test's expected value (from ref) equals
brute (small) or the closed form (large); the starter fails the tests; the ref runs each large test in well under a
second.  It writes oa_code_tests.json (the full test tables) and oa_code_section.md (what the brief embeds).
"""
import bisect, heapq, inspect, itertools, json, os, random, sys, time
from collections import deque
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = 1_000_000_007
sys.setrecursionlimit(20000)


# ---------------------------------------------------------------- 1 products below k (windows)
def count_products_below(nums, k):
    if k <= 1:
        return 0
    left, prod, count = 0, 1, 0
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:
            prod //= nums[left]
            left += 1
        count += right - left + 1
    return count


def brute_products(nums, k):
    count = 0
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            if p < k:
                count += 1
    return count


def rand_products(r):
    return ([r.randint(1, 6) for _ in range(r.randint(0, 9))], r.randint(0, 40))


# ---------------------------------------------------------------- 2 trapped water (two pointers)
def trapped_water(heights):
    lo, hi = 0, len(heights) - 1
    left_max = right_max = water = 0
    while lo < hi:
        if heights[lo] < heights[hi]:
            left_max = max(left_max, heights[lo])
            water += left_max - heights[lo]
            lo += 1
        else:
            right_max = max(right_max, heights[hi])
            water += right_max - heights[hi]
            hi -= 1
    return water


def brute_water(heights):
    return sum(max(0, min(max(heights[:i + 1]), max(heights[i:])) - h) for i, h in enumerate(heights))


def rand_water(r):
    return ([r.randint(0, 5) for _ in range(r.randint(0, 12))],)


# ---------------------------------------------------------------- 3 fewest jumps (greedy)
def min_jumps(nums):
    n = len(nums)
    if n <= 1:
        return 0
    jumps = end = far = 0
    for i in range(n - 1):
        far = max(far, i + nums[i])
        if i == end:
            if far <= i:
                return -1
            jumps += 1
            end = far
            if end >= n - 1:
                return jumps
    return jumps if end >= n - 1 else -1


def brute_jumps(nums):
    n = len(nums)
    if n <= 1:
        return 0
    dist = [None] * n
    dist[0] = 0
    for i in range(n):  # forward relaxation is exact because every jump goes right
        if dist[i] is None:
            continue
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if dist[j] is None or dist[i] + 1 < dist[j]:
                dist[j] = dist[i] + 1
    return -1 if dist[-1] is None else dist[-1]


def rand_jumps(r):
    return ([r.randint(0, 4) for _ in range(r.randint(0, 9))],)


# ---------------------------------------------------------------- 4 cheapest joins (heap)
def min_merge_cost(sticks):
    heap = list(sticks)
    heapq.heapify(heap)
    cost = 0
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        cost += a + b
        heapq.heappush(heap, a + b)
    return cost


def alt_merge(sticks):  # two sorted queues, no heap
    q1, q2, cost = deque(sorted(sticks)), deque(), 0

    def pop():
        if q1 and (not q2 or q1[0] <= q2[0]):
            return q1.popleft()
        return q2.popleft()
    while len(q1) + len(q2) > 1:
        x, y = pop(), pop()
        cost += x + y
        q2.append(x + y)
    return cost


def brute_merge(sticks):
    @lru_cache(None)
    def go(t):
        if len(t) <= 1:
            return 0
        best = None
        for i in range(len(t)):
            for j in range(i + 1, len(t)):
                rest = list(t[:i] + t[i + 1:j] + t[j + 1:]) + [t[i] + t[j]]
                c = t[i] + t[j] + go(tuple(sorted(rest)))
                if best is None or c < best:
                    best = c
        return best
    return go(tuple(sorted(sticks)))


def rand_merge(r):
    return ([r.randint(1, 9) for _ in range(r.randint(0, 6))],)


# ---------------------------------------------------------------- 5 smallest number after removing digits (stack)
def smallest_after_removing(digits, k):
    stack = []
    for d in digits:
        while k and stack and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)
    if k:
        stack = stack[:-k]
    return "".join(stack).lstrip("0") or "0"


def brute_remove(digits, k):
    n = len(digits)
    if n - k == 0:
        return "0"
    return str(min(int("".join(digits[i] for i in idx)) for idx in itertools.combinations(range(n), n - k)))


def rand_remove(r):
    n = r.randint(0, 9)
    s = "".join(r.choice("0011234567899") for _ in range(n))
    return (s, r.randint(0, n))


# ---------------------------------------------------------------- 6 longest rising subsequence (binary search)
def longest_rising(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def alt_rising(nums):  # the quadratic table
    best = []
    for i, x in enumerate(nums):
        best.append(1 + max([best[j] for j in range(i) if nums[j] < x], default=0))
    return max(best, default=0)


def brute_rising(nums):  # every subsequence
    n, top = len(nums), 0
    for mask in range(1 << n):
        sub = [nums[i] for i in range(n) if mask >> i & 1]
        if all(a < b for a, b in zip(sub, sub[1:])):
            top = max(top, len(sub))
    return top


def rand_rising(r):
    return ([r.randint(0, 7) for _ in range(r.randint(0, 11))],)


# ---------------------------------------------------------------- 7 decodings (dp)
def count_decodings(s):
    prev2, prev1 = 0, 1
    for i, ch in enumerate(s):
        cur = 0
        if ch != "0":
            cur += prev1
        if i >= 1 and "10" <= s[i - 1:i + 1] <= "26":
            cur += prev2
        prev2, prev1 = prev1, cur % MOD
    return prev1


def brute_decodings(s):
    def go(i):
        if i == len(s):
            return 1
        total = 0
        for length in (1, 2):
            seg = s[i:i + length]
            if len(seg) == length and seg[0] != "0" and 1 <= int(seg) <= 26:
                total += go(i + length)
        return total
    return go(0) % MOD


def fib_mod(n):  # fast doubling: F(1) = F(2) = 1
    def fd(k):
        if k == 0:
            return 0, 1
        a, b = fd(k >> 1)
        c = a * ((2 * b - a) % MOD) % MOD
        d = (a * a + b * b) % MOD
        return (d, (c + d) % MOD) if k & 1 else (c, d)
    return fd(n)[0]


def rand_decodings(r):
    return ("".join(r.choice("0112256789") for _ in range(r.randint(0, 12))),)


# ---------------------------------------------------------------- 8 critical path (graph)
def critical_path_length(n, edges, durations):
    indeg = [0] * n
    out = [[] for _ in range(n)]
    for a, b in edges:
        out[a].append(b)
        indeg[b] += 1
    start = [0] * n
    queue = [i for i in range(n) if indeg[i] == 0]
    done = 0
    while queue:
        u = queue.pop()
        done += 1
        finish = start[u] + durations[u]
        for v in out[u]:
            start[v] = max(start[v], finish)
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if done < n:
        return -1
    return max((start[i] + durations[i] for i in range(n)), default=0)


def brute_critical(n, edges, durations):  # memoised recursion with loop detection
    preds = [[] for _ in range(n)]
    for a, b in edges:
        preds[b].append(a)
    state, fin = [0] * n, [0] * n

    def f(v):
        if state[v] == 2:
            return fin[v]
        if state[v] == 1:
            raise ValueError("loop")
        state[v] = 1
        s = max((f(p) for p in preds[v]), default=0)
        state[v] = 2
        fin[v] = s + durations[v]
        return fin[v]
    try:
        return max((f(v) for v in range(n)), default=0)
    except ValueError:
        return -1


def rand_critical(r):
    n = r.randint(0, 6)
    edges = [[r.randrange(n), r.randrange(n)] for _ in range(r.randint(0, 8))] if n else []
    return (n, edges, [r.randint(1, 5) for _ in range(n)])


# ---------------------------------------------------------------- the table
# Each test: (call text, closed form / "ALT" / None).  Small cases carry None: brute supplies the check.
P = [
    dict(id="oa-product-windows", fn="count_products_below", ref=count_products_below, brute=brute_products, rand=rand_products,
         d=3, pace=1200, pattern="windows", tags=["product-windows"], name="Blocks with a small product",
         sig="count_products_below(nums, k)", stub="def count_products_below(nums, k):\n    return 0\n",
         statement=("`nums` holds positive whole numbers. Count the non-empty blocks of neighbouring entries whose product is below `k`. "
                    "Equal blocks at different places count separately. `k` may be 1 or less, and `nums` may be empty."),
         tests=[("count_products_below([3, 4, 2, 5, 1], 20)", None), ("count_products_below([], 10)", None),
                ("count_products_below([5], 5)", None), ("count_products_below([5], 6)", None),
                ("count_products_below([1, 1, 1], 2)", None), ("count_products_below([7, 8], 1)", None),
                ("count_products_below([2, 3, 4], 100)", None), ("count_products_below([6, 2, 9, 1, 3], 30)", None),
                ("count_products_below([1] * 200000, 2)", 200000 * 200001 // 2),
                ("count_products_below([2] * 200000, 3)", 200000)],
         examples=[0, 3], small=8, slow="checking every block is 2 x 10^10 steps on test 9"),
    dict(id="oa-rain-water", fn="trapped_water", ref=trapped_water, brute=brute_water, rand=rand_water,
         d=3, pace=1200, pattern="two-pointers", tags=["water-trapped"], name="Water held between bars",
         sig="trapped_water(heights)", stub="def trapped_water(heights):\n    return 0\n",
         statement=("`heights[i]` is the height of a bar of width 1. After rain, water sits in the dips between taller bars. "
                    "Return how many units of water the bars hold. Water that could run off either end is not held."),
         tests=[("trapped_water([3, 0, 2, 0, 4])", None), ("trapped_water([])", None), ("trapped_water([5])", None),
                ("trapped_water([1, 2, 3])", None), ("trapped_water([3, 1, 3])", None), ("trapped_water([4, 1, 1, 0, 2, 3])", None),
                ("trapped_water([0, 3, 0, 1, 0, 2])", None), ("trapped_water([2, 0, 2])", None),
                ("trapped_water([5] + [0] * 199998 + [5])", 5 * 199998),
                ("trapped_water(list(range(100000)) + list(range(100000, 0, -1)))", 0),
                ("trapped_water([3, 1] * 100000)", 2 * 99999)],
         examples=[0, 4], small=8, slow="finding the walls of every bar by scanning is 4 x 10^10 steps on test 9"),
    dict(id="oa-min-jumps", fn="min_jumps", ref=min_jumps, brute=brute_jumps, rand=rand_jumps,
         d=3, pace=1200, pattern="greedy", tags=["jump-count"], name="Fewest jumps",
         sig="min_jumps(nums)", stub="def min_jumps(nums):\n    return 0\n",
         statement=("`nums[i]` is the longest jump you can make from position `i`, and you may jump any shorter distance. "
                    "Start at position 0. Return the fewest jumps that reach the last position, or -1 if you cannot. "
                    "A list of one or no entries needs 0 jumps."),
         tests=[("min_jumps([4, 1, 1, 3, 1, 1, 1])", None), ("min_jumps([])", None), ("min_jumps([0])", None),
                ("min_jumps([0, 5])", None), ("min_jumps([1, 1, 1, 1])", None),
                ("min_jumps([5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0])", None), ("min_jumps([2, 0, 0])", None), ("min_jumps([10, 1, 1])", None),
                ("min_jumps([1] * 200000)", 199999), ("min_jumps([200000] + [1] * 199999)", 1), ("min_jumps([2] * 200000)", 100000)],
         examples=[0, 4], small=8, slow="trying every earlier position for each position is 2 x 10^10 steps on test 9"),
    dict(id="oa-merge-cost", fn="min_merge_cost", ref=min_merge_cost, brute=brute_merge, alt=alt_merge, rand=rand_merge,
         d=3, pace=1200, pattern="heaps-tries", tags=["merge-cost"], name="Cheapest way to join sticks",
         sig="min_merge_cost(sticks)", stub="def min_merge_cost(sticks):\n    return 0\n",
         statement=("You have sticks with the given lengths. Joining two sticks costs the sum of their lengths and gives one longer stick. "
                    "Return the least total cost to join them all into one. Zero or one stick costs nothing."),
         tests=[("min_merge_cost([5, 3, 8, 2])", None), ("min_merge_cost([])", None), ("min_merge_cost([9])", None),
                ("min_merge_cost([4, 4])", None), ("min_merge_cost([1, 1, 1, 1])", None), ("min_merge_cost([7, 3, 5])", None),
                ("min_merge_cost([10, 20, 30, 40, 50])", None),
                ("min_merge_cost([1] * 131072)", 131072 * 17), ("min_merge_cost([2] * 65536)", 2 * 65536 * 16),
                ("min_merge_cost(list(range(1, 100001)))", "ALT")],
         examples=[0, 3], small=7, slow="searching for the two shortest sticks by scanning is 10^10 steps on test 10"),
    dict(id="oa-remove-digits", fn="smallest_after_removing", ref=smallest_after_removing, brute=brute_remove, rand=rand_remove,
         d=4, pace=1800, pattern="stacks-queues", tags=["digit-removal"], name="Smallest number after removing digits",
         sig="smallest_after_removing(digits, k)", stub='def smallest_after_removing(digits, k):\n    return ""\n',
         statement=("`digits` is a string of the characters 0 to 9. Remove exactly `k` characters, keeping the order of the rest, "
                    "so the number left is as small as possible. Return it as a string with no leading zeros. "
                    "Return \"0\" if nothing is left, or only zeros."),
         tests=[('smallest_after_removing("5291", 2)', None), ('smallest_after_removing("", 0)', None),
                ('smallest_after_removing("10", 2)', None), ('smallest_after_removing("100200", 1)', None),
                ('smallest_after_removing("9", 0)', None), ('smallest_after_removing("1111", 2)', None),
                ('smallest_after_removing("112", 1)', None), ('smallest_after_removing("7654321", 3)', None),
                ('smallest_after_removing("30200", 1)', None),
                ('smallest_after_removing("9" * 100000 + "1" * 100000, 100000) == "1" * 100000', True),
                ('smallest_after_removing("1" * 150000 + "2" * 50000, 50000) == "1" * 150000', True),
                ('smallest_after_removing("5" * 200000, 200000)', "0")],
         examples=[0, 3], small=9, slow="trying every set of digits is hopeless on tests 10 and 11. Removing one digit at a time with a scan is 10^10 steps"),
    dict(id="oa-rising-run", fn="longest_rising", ref=longest_rising, brute=brute_rising, alt=alt_rising, rand=rand_rising,
         d=4, pace=1800, pattern="binary-search", tags=["rising-subsequence"], name="Longest rising subsequence",
         sig="longest_rising(nums)", stub="def longest_rising(nums):\n    return 0\n",
         statement=("Return the length of the longest strictly increasing subsequence of `nums`. "
                    "A subsequence keeps the order but need not use neighbouring entries. An empty list gives 0."),
         tests=[("longest_rising([4, 10, 4, 3, 8, 9])", None), ("longest_rising([])", None), ("longest_rising([7])", None),
                ("longest_rising([5, 5, 5])", None), ("longest_rising([1, 2, 3, 4])", None), ("longest_rising([4, 3, 2, 1])", None),
                ("longest_rising([6, 2, 9, 5, 1, 7, 3, 8])", None), ("longest_rising([0, 8, 4, 12, 2, 10, 6, 14])", None),
                ("longest_rising(list(range(200000)))", 200000), ("longest_rising(list(range(200000, 0, -1)))", 1),
                ("longest_rising([i % 1000 for i in range(200000)])", 1000)],
         examples=[0, 6], small=8, slow="the quadratic table is 2 x 10^10 steps on test 9"),
    dict(id="oa-decodings", fn="count_decodings", ref=count_decodings, brute=brute_decodings, rand=rand_decodings,
         d=4, pace=1800, pattern="dp", tags=["digit-decodings"], name="Ways to decode a message",
         sig="count_decodings(s)", stub="def count_decodings(s):\n    return 0\n",
         statement=("A message of letters was coded as digits. A is 1, B is 2 and so on up to Z as 26. `s` is the digit string. "
                    "Return how many different messages it could be, modulo 1,000,000,007. "
                    "A string that cannot be decoded gives 0, and the empty string gives 1."),
         tests=[('count_decodings("226")', None), ('count_decodings("")', None), ('count_decodings("0")', None),
                ('count_decodings("100")', None), ('count_decodings("2710")', None), ('count_decodings("11106")', None),
                ('count_decodings("1212")', None), ('count_decodings("301")', None),
                ('count_decodings("1" * 200000)', fib_mod(200001)), ('count_decodings("27" * 100000)', 1),
                ('count_decodings("10" * 100000)', 1), ('count_decodings("1" * 100000 + "0" + "9" * 5)', fib_mod(100000))],
         examples=[0, 3], small=8, slow="listing every decoding takes over 10^40 steps on test 9. A recursion without a table never ends"),
    dict(id="oa-critical-path", fn="critical_path_length", ref=critical_path_length, brute=brute_critical, rand=rand_critical,
         d=4, pace=1800, pattern="graphs", tags=["critical-path"], name="Time to finish all tasks",
         sig="critical_path_length(n, edges, durations)", stub="def critical_path_length(n, edges, durations):\n    return 0\n",
         statement=("There are `n` tasks numbered 0 to `n - 1`, and `durations[i]` is the time task `i` takes. "
                    "Each pair `[a, b]` in `edges` means task `a` must finish before task `b` starts. Any number of tasks may run at once. "
                    "Return the least time to finish every task, or -1 if the pairs form a loop."),
         tests=[("critical_path_length(4, [[0, 1], [0, 2], [1, 3], [2, 3]], [3, 2, 4, 1])", None),
                ("critical_path_length(0, [], [])", None), ("critical_path_length(3, [], [5, 2, 9])", None),
                ("critical_path_length(3, [[0, 1], [1, 2], [2, 0]], [1, 1, 1])", None),
                ("critical_path_length(2, [[0, 1], [0, 1]], [4, 3])", None),
                ("critical_path_length(5, [[0, 1], [1, 2], [0, 3], [3, 4], [2, 4]], [2, 2, 2, 5, 1])", None),
                ("critical_path_length(1, [], [7])", None), ("critical_path_length(3, [[0, 1]], [4, 5, 6])", None),
                ("critical_path_length(3, [[1, 1]], [1, 1, 1])", None),
                ("critical_path_length(100000, [[i, i + 1] for i in range(99999)], [1] * 100000)", 100000),
                ("critical_path_length(100001, [[i, 100000] for i in range(100000)], [2] * 100000 + [3])", 5),
                ("critical_path_length(100000, [[i, i + 1] for i in range(99999)] + [[99999, 0]], [1] * 100000)", -1)],
         examples=[0, 3], small=9, slow="a recursive search runs out of stack on test 10. Re-walking every path is exponential"),
]


def run():
    r = random.Random(2701)
    allj = {}
    md = []
    for p in P:
        ref, brute, alt, rand = p["ref"], p["brute"], p.get("alt"), p["rand"]
        N = 4000
        for _ in range(N):
            args = rand(r)
            a = ref(*args)
            assert a == brute(*args), (p["id"], args, a, brute(*args))
            if alt:
                assert a == alt(*args), (p["id"], args, "alt")
        rows = []
        worst = 0.0
        for call, closed in p["tests"]:
            t0 = time.time()
            exp = eval(call, {}, {p["fn"]: ref})
            worst = max(worst, time.time() - t0)
            if closed is None:
                small = eval(call, {}, {p["fn"]: brute})
                assert exp == small, (p["id"], call, exp, small)
                if alt:
                    assert exp == eval(call, {}, {p["fn"]: alt}), (p["id"], call, "alt")
                second = "exhaustive method" + (" and second algorithm" if alt else "")
            elif closed == "ALT":
                assert exp == eval(call, {}, {p["fn"]: alt}), (p["id"], call, "alt")
                second = "two-queue method"
            else:
                assert exp == closed, (p["id"], call, exp, closed)
                second = "closed form" if p["id"] != "oa-decodings" else "Fibonacci by fast doubling"
            rows.append({"call": call, "expect": repr(exp), "group": "small" if closed is None else "large", "second": second})
        assert worst < 1.5, (p["id"], worst)
        assert sum(1 for x in rows if x["group"] == "small") == p["small"], (p["id"], p["small"])
        assert 3 <= len(rows) <= 15
        ns = {}
        exec(p["stub"], ns)
        stub = ns[p["fn"]]

        def stub_fails(row):
            try:
                return eval(row["call"], {}, {p["fn"]: stub}) != eval(row["expect"])
            except Exception:
                return True
        fails = sum(1 for row in rows if stub_fails(row))
        assert fails >= len(rows) - 5 and fails >= 1
        allj[p["id"]] = {"fn": p["fn"], "difficulty": p["d"], "pace": p["pace"], "pattern": p["pattern"], "tags": p["tags"], "name": p["name"],
                         "statement": p["statement"], "starter": p["stub"], "tests": rows, "examples": [rows[i] for i in p["examples"]],
                         "starter_fails": fails, "ref_worst_seconds": round(worst, 3), "random_cases": N}
        md.append(f"#### `{p['id']}`: {p['name']} (difficulty {p['d']}, pattern `{p['pattern']}`, tag `{p['tags'][0]}`, pace {p['pace']} s)\n")
        md.append(f"Statement. {p['statement']}\n")
        md.append(f"Signature `{p['sig']}`. Starter (fails {fails} of {len(rows)}):\n\n```python\n{p['stub']}```\n")
        md.append("Reference (`solution`):\n\n```python\n" + inspect.getsource(ref) + "```\n")
        md.append("Hidden tests, all `compare: \"equal\"`. Each small test is checked against an exhaustive or second method. "
                  "Each large test is checked against the value in the last column. "
                  f"Slow code: {p['slow']}.\n")
        md.append("| # | Call | Expected | Second value from |\n| --- | --- | --- | --- |")
        for i, row in enumerate(rows, 1):
            md.append(f"| {i} | `{row['call']}` | `{row['expect']}` | {row['second']} |")
        md.append(f"\nExamples (visible): tests {p['examples'][0] + 1} and {p['examples'][1] + 1}. Largest reference run {worst:.3f} s in CPython. "
                  f"{N} seeded random cases agree with the exhaustive method" + (" and with the second algorithm" if alt else "") + ".\n")
        print(f"OK  {p['id']}: {len(rows)} tests, starter fails {fails}, ref worst {worst:.3f} s")
    json.dump(allj, open(os.path.join(HERE, "oa_code_tests.json"), "w"), indent=1)
    open(os.path.join(HERE, "oa_code_section.md"), "w").write("\n".join(md))
    assert sorted(v["difficulty"] for v in allj.values()) == [3, 3, 3, 3, 4, 4, 4, 4]
    assert len({v["tags"][0] for v in allj.values()}) == 8 and len({v["pattern"] for v in allj.values()}) == 8
    print("ALL AGREE: 8 problems")


if __name__ == "__main__":
    run()
