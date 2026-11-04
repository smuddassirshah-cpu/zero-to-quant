#### `oa-product-windows`: Blocks with a small product (difficulty 3, pattern `windows`, tag `product-windows`, pace 1200 s)

Statement. `nums` holds positive whole numbers. Count the non-empty blocks of neighbouring entries whose product is below `k`. Equal blocks at different places count separately. `k` may be 1 or less, and `nums` may be empty.

Signature `count_products_below(nums, k)`. Starter (fails 7 of 12):

```python
def count_products_below(nums, k):
    return 0
```

Reference (`solution`):

```python
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
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: checking every block is 2 x 10^10 steps on test 11.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `count_products_below([3, 4, 2, 5, 1], 20)` | `10` | exhaustive method |
| 2 | `count_products_below([], 10)` | `0` | exhaustive method |
| 3 | `count_products_below([5], 5)` | `0` | exhaustive method |
| 4 | `count_products_below([5], 6)` | `1` | exhaustive method |
| 5 | `count_products_below([1, 1, 1], 2)` | `6` | exhaustive method |
| 6 | `count_products_below([7, 8], 1)` | `0` | exhaustive method |
| 7 | `count_products_below([2, 3, 4], 100)` | `6` | exhaustive method |
| 8 | `count_products_below([6, 2, 9, 1, 3], 30)` | `11` | exhaustive method |
| 9 | `count_products_below([3, 4], 0)` | `0` | exhaustive method |
| 10 | `count_products_below([3, 4], -5)` | `0` | exhaustive method |
| 11 | `count_products_below([1] * 200000, 2)` | `20000100000` | closed form |
| 12 | `count_products_below([2] * 200000, 3)` | `200000` | closed form |

Examples (visible): tests 1 and 4. Largest reference run 0.035 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-rain-water`: Water held between bars (difficulty 3, pattern `two-pointers`, tag `water-trapped`, pace 1200 s)

Statement. `heights[i]` is the height of a bar of width 1. After rain, water sits in the dips between taller bars. Return how many units of water the bars hold. Water that could run off either end is not held.

Signature `trapped_water(heights)`. Starter (fails 7 of 11):

```python
def trapped_water(heights):
    return 0
```

Reference (`solution`):

```python
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
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: finding the walls of every bar by scanning is 4 x 10^10 steps on test 9.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `trapped_water([3, 0, 2, 0, 4])` | `7` | exhaustive method |
| 2 | `trapped_water([])` | `0` | exhaustive method |
| 3 | `trapped_water([5])` | `0` | exhaustive method |
| 4 | `trapped_water([1, 2, 3])` | `0` | exhaustive method |
| 5 | `trapped_water([3, 1, 3])` | `2` | exhaustive method |
| 6 | `trapped_water([4, 1, 1, 0, 2, 3])` | `8` | exhaustive method |
| 7 | `trapped_water([0, 3, 0, 1, 0, 2])` | `5` | exhaustive method |
| 8 | `trapped_water([2, 0, 2])` | `2` | exhaustive method |
| 9 | `trapped_water([5] + [0] * 199998 + [5])` | `999990` | closed form |
| 10 | `trapped_water(list(range(100000)) + list(range(100000, 0, -1)))` | `0` | closed form |
| 11 | `trapped_water([3, 1] * 100000)` | `199998` | closed form |

Examples (visible): tests 1 and 5. Largest reference run 0.030 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-min-jumps`: Fewest jumps (difficulty 3, pattern `greedy`, tag `jump-count`, pace 1200 s)

Statement. `nums[i]` is the longest jump you can make from position `i`, and you may jump any shorter distance. Start at position 0. Return the fewest jumps that reach the last position, or -1 if you cannot. A list of one or no entries needs 0 jumps.

Signature `min_jumps(nums)`. Starter (fails 10 of 12):

```python
def min_jumps(nums):
    return 0
```

Reference (`solution`):

```python
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
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: trying every earlier position for each position is 2 x 10^10 steps on test 9.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `min_jumps([4, 1, 1, 3, 1, 1, 1])` | `2` | exhaustive method |
| 2 | `min_jumps([])` | `0` | exhaustive method |
| 3 | `min_jumps([0])` | `0` | exhaustive method |
| 4 | `min_jumps([0, 5])` | `-1` | exhaustive method |
| 5 | `min_jumps([1, 1, 1, 1])` | `3` | exhaustive method |
| 6 | `min_jumps([5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0])` | `3` | exhaustive method |
| 7 | `min_jumps([2, 0, 0])` | `1` | exhaustive method |
| 8 | `min_jumps([10, 1, 1])` | `1` | exhaustive method |
| 9 | `min_jumps([1] * 200000)` | `199999` | closed form |
| 10 | `min_jumps([200000] + [1] * 199999)` | `1` | closed form |
| 11 | `min_jumps([2] * 200000)` | `100000` | closed form |
| 12 | `min_jumps([200000] * 200000)` | `1` | closed form |

Examples (visible): tests 1 and 5. Largest reference run 0.022 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-merge-cost`: Cheapest way to join sticks (difficulty 3, pattern `heaps-tries`, tag `merge-cost`, pace 1200 s)

Statement. You have sticks with the given lengths. Joining two sticks costs the sum of their lengths and gives one longer stick. Return the least total cost to join them all into one. Zero or one stick costs nothing.

Signature `min_merge_cost(sticks)`. Starter (fails 9 of 11):

```python
def min_merge_cost(sticks):
    return 0
```

Reference (`solution`):

```python
def min_merge_cost(sticks):
    heap = list(sticks)
    heapq.heapify(heap)
    cost = 0
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        cost += a + b
        heapq.heappush(heap, a + b)
    return cost
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: searching for the two shortest sticks by scanning is 10^10 steps on test 10. Keeping a sorted list with `insort` takes several seconds on test 11.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `min_merge_cost([5, 3, 8, 2])` | `33` | exhaustive method and second algorithm |
| 2 | `min_merge_cost([])` | `0` | exhaustive method and second algorithm |
| 3 | `min_merge_cost([9])` | `0` | exhaustive method and second algorithm |
| 4 | `min_merge_cost([4, 4])` | `8` | exhaustive method and second algorithm |
| 5 | `min_merge_cost([1, 1, 1, 1])` | `8` | exhaustive method and second algorithm |
| 6 | `min_merge_cost([7, 3, 5])` | `23` | exhaustive method and second algorithm |
| 7 | `min_merge_cost([10, 20, 30, 40, 50])` | `330` | exhaustive method and second algorithm |
| 8 | `min_merge_cost([1] * 131072)` | `2228224` | closed form |
| 9 | `min_merge_cost([2] * 65536)` | `2097152` | closed form |
| 10 | `min_merge_cost(list(range(1, 100001)))` | `81782502640` | two-queue method |
| 11 | `min_merge_cost(list(range(1, 200001)))` | `347128407168` | two-queue method |

Examples (visible): tests 1 and 4. Largest reference run 0.152 s in CPython. 4000 seeded random cases agree with the exhaustive method and with the second algorithm.

#### `oa-remove-digits`: Smallest number after removing digits (difficulty 4, pattern `stacks-queues`, tag `digit-removal`, pace 1800 s)

Statement. `digits` is a string of the characters 0 to 9. Remove exactly `k` characters, keeping the order of the rest, so the number left is as small as possible. Return it as a string with no leading zeros. Return "0" if nothing is left, or only zeros.

Signature `smallest_after_removing(digits, k)`. Starter (fails 13 of 13):

```python
def smallest_after_removing(digits, k):
    return ""
```

Reference (`solution`):

```python
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
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: trying every set of digits is hopeless on tests 11 and 12. Removing one digit at a time with a scan is 10^10 steps.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `smallest_after_removing("5291", 2)` | `'21'` | exhaustive method |
| 2 | `smallest_after_removing("", 0)` | `'0'` | exhaustive method |
| 3 | `smallest_after_removing("10", 2)` | `'0'` | exhaustive method |
| 4 | `smallest_after_removing("100200", 1)` | `'200'` | exhaustive method |
| 5 | `smallest_after_removing("9", 0)` | `'9'` | exhaustive method |
| 6 | `smallest_after_removing("1111", 2)` | `'11'` | exhaustive method |
| 7 | `smallest_after_removing("112", 1)` | `'11'` | exhaustive method |
| 8 | `smallest_after_removing("7654321", 3)` | `'4321'` | exhaustive method |
| 9 | `smallest_after_removing("30200", 1)` | `'200'` | exhaustive method |
| 10 | `smallest_after_removing("2561", 2)` | `'21'` | exhaustive method |
| 11 | `smallest_after_removing("9" * 100000 + "1" * 100000, 100000) == "1" * 100000` | `True` | closed form |
| 12 | `smallest_after_removing("1" * 150000 + "2" * 50000, 50000) == "1" * 150000` | `True` | closed form |
| 13 | `smallest_after_removing("5" * 200000, 200000)` | `'0'` | closed form |

Examples (visible): tests 1 and 4. Largest reference run 0.011 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-rising-run`: Longest rising subsequence (difficulty 4, pattern `binary-search`, tag `rising-subsequence`, pace 1800 s)

Statement. Return the length of the longest strictly increasing subsequence of `nums`. A subsequence keeps the order but need not use neighbouring entries. An empty list gives 0.

Signature `longest_rising(nums)`. Starter (fails 10 of 11):

```python
def longest_rising(nums):
    return 0
```

Reference (`solution`):

```python
def longest_rising(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: the quadratic table is 2 x 10^10 steps on test 9.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `longest_rising([4, 10, 4, 3, 8, 9])` | `3` | exhaustive method and second algorithm |
| 2 | `longest_rising([])` | `0` | exhaustive method and second algorithm |
| 3 | `longest_rising([7])` | `1` | exhaustive method and second algorithm |
| 4 | `longest_rising([5, 5, 5])` | `1` | exhaustive method and second algorithm |
| 5 | `longest_rising([1, 2, 3, 4])` | `4` | exhaustive method and second algorithm |
| 6 | `longest_rising([4, 3, 2, 1])` | `1` | exhaustive method and second algorithm |
| 7 | `longest_rising([6, 2, 9, 5, 1, 7, 3, 8])` | `4` | exhaustive method and second algorithm |
| 8 | `longest_rising([0, 8, 4, 12, 2, 10, 6, 14])` | `4` | exhaustive method and second algorithm |
| 9 | `longest_rising(list(range(200000)))` | `200000` | closed form |
| 10 | `longest_rising(list(range(200000, 0, -1)))` | `1` | closed form |
| 11 | `longest_rising([i % 1000 for i in range(200000)])` | `1000` | closed form |

Examples (visible): tests 1 and 7. Largest reference run 0.039 s in CPython. 4000 seeded random cases agree with the exhaustive method and with the second algorithm.

#### `oa-decodings`: Ways to decode a message (difficulty 4, pattern `dp`, tag `digit-decodings`, pace 1800 s)

Statement. A message of letters was coded as digits. A is 1, B is 2 and so on up to Z as 26. A code never starts with 0, so 06 is not a letter. `s` is the digit string. Return how many different messages it could be, modulo 1,000,000,007. A string that cannot be decoded gives 0, and the empty string gives 1.

Signature `count_decodings(s)`. Starter (fails 10 of 14):

```python
def count_decodings(s):
    return 0
```

Reference (`solution`):

```python
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
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: listing every decoding takes over 10^40 steps on test 11. A recursion without a table never ends.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `count_decodings("226")` | `3` | exhaustive method |
| 2 | `count_decodings("")` | `1` | exhaustive method |
| 3 | `count_decodings("0")` | `0` | exhaustive method |
| 4 | `count_decodings("100")` | `0` | exhaustive method |
| 5 | `count_decodings("2710")` | `1` | exhaustive method |
| 6 | `count_decodings("11106")` | `2` | exhaustive method |
| 7 | `count_decodings("1212")` | `5` | exhaustive method |
| 8 | `count_decodings("301")` | `0` | exhaustive method |
| 9 | `count_decodings("2020")` | `1` | exhaustive method |
| 10 | `count_decodings("260")` | `0` | exhaustive method |
| 11 | `count_decodings("1" * 200000)` | `835799900` | Fibonacci by fast doubling |
| 12 | `count_decodings("27" * 100000)` | `1` | Fibonacci by fast doubling |
| 13 | `count_decodings("10" * 100000)` | `1` | Fibonacci by fast doubling |
| 14 | `count_decodings("1" * 100000 + "0" + "9" * 5)` | `911435502` | Fibonacci by fast doubling |

Examples (visible): tests 1 and 4. Largest reference run 0.042 s in CPython. 4000 seeded random cases agree with the exhaustive method.

#### `oa-critical-path`: Time to finish all tasks (difficulty 4, pattern `graphs`, tag `critical-path`, pace 1800 s)

Statement. There are `n` tasks numbered 0 to `n - 1`, and `durations[i]` is the time task `i` takes. Each pair `[a, b]` in `edges` means task `a` must finish before task `b` starts. Any number of tasks may run at once. Each duration is a whole number of at least 0. A pair `[a, a]` is a loop. Return the least time to finish every task, or -1 if the pairs form a loop.

Signature `critical_path_length(n, edges, durations)`. Starter (fails 13 of 14):

```python
def critical_path_length(n, edges, durations):
    return 0
```

Reference (`solution`):

```python
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
```

Hidden tests, all `compare: "equal"`. Each small test is checked against an exhaustive or second method. Each large test is checked against the value in the last column. Slow code: a recursive search runs out of stack on test 12. Re-walking every path is exponential.

| # | Call | Expected | Second value from |
| --- | --- | --- | --- |
| 1 | `critical_path_length(4, [[0, 1], [0, 2], [1, 3], [2, 3]], [3, 2, 4, 1])` | `8` | exhaustive method |
| 2 | `critical_path_length(0, [], [])` | `0` | exhaustive method |
| 3 | `critical_path_length(3, [], [5, 2, 9])` | `9` | exhaustive method |
| 4 | `critical_path_length(3, [[0, 1], [1, 2], [2, 0]], [1, 1, 1])` | `-1` | exhaustive method |
| 5 | `critical_path_length(2, [[0, 1], [0, 1]], [4, 3])` | `7` | exhaustive method |
| 6 | `critical_path_length(5, [[0, 1], [1, 2], [0, 3], [3, 4], [2, 4]], [2, 2, 2, 5, 1])` | `8` | exhaustive method |
| 7 | `critical_path_length(1, [], [7])` | `7` | exhaustive method |
| 8 | `critical_path_length(3, [[0, 1]], [4, 5, 6])` | `9` | exhaustive method |
| 9 | `critical_path_length(3, [[1, 1]], [1, 1, 1])` | `-1` | exhaustive method |
| 10 | `critical_path_length(4, [[0, 1], [2, 3], [3, 2]], [1, 1, 1, 1])` | `-1` | exhaustive method |
| 11 | `critical_path_length(3, [[0, 1], [1, 2], [2, 1]], [1, 1, 1])` | `-1` | exhaustive method |
| 12 | `critical_path_length(100000, [[i, i + 1] for i in range(99999)], [1] * 100000)` | `100000` | closed form |
| 13 | `critical_path_length(100001, [[i, 100000] for i in range(100000)], [2] * 100000 + [3])` | `5` | closed form |
| 14 | `critical_path_length(100000, [[i, i + 1] for i in range(99999)] + [[99999, 0]], [1] * 100000)` | `-1` | closed form |

Examples (visible): tests 1 and 4. Largest reference run 0.077 s in CPython. 4000 seeded random cases agree with the exhaustive method.
