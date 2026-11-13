#!/usr/bin/env python3
"""Concept audit checks for ds levels 1 to 3 (round 1 blind audit).

Runs every complexity, operation-count and code-behaviour claim the ledger
marks as "run". Written against CPython 3.13 (Pyodide 0.27.7 is CPython 3.12;
nothing here depends on a 3.13-only behaviour).

A check prints PASS or FAIL. A FAIL means the content's claim is false as
stated; each FAIL is a finding in docs/reviews/audit-ds-1-3.md. Lines tagged
[fix] verify the auditor's own proposed fix text. The script exits 0 only when
every content claim holds, so it exits 1 until the findings are fixed.
"""
import sys
import time
import random
from collections import Counter, defaultdict, deque, OrderedDict

FAILS = []


def check(tag, ok, note=""):
    print(("PASS " if ok else "FAIL ") + tag + (" :: " + note if note else ""))
    if not ok:
        FAILS.append(tag)


# ---------------------------------------------------------------- level 1
# l1 addresses
check("l1.s0 address", 1000 + 4 * 8 == 1032 and 2000 + 10 * 4 == 2040)


def doubling_copies(appends, cap=1):
    size = copies = 0
    for _ in range(appends):
        if size == cap:
            copies += size
            cap *= 2
        size += 1
    return copies


check("l1.s4 16 appends make 15 copies", doubling_copies(16) == 15)
check("hw1 h-doubling 1000 appends make 1023 copies", doubling_copies(1000) == 1023)
bad = [n for n in range(1, 2000) if doubling_copies(n) >= n]
check("l1.s4 explain 'copies always fewer than the appends'", not bad,
      f"false for {len(bad)} of 1999 n; first n={bad[0]}: {doubling_copies(bad[0])} copies; n=17 gives {doubling_copies(17)}")
check("[fix] copies always fewer than twice the appends",
      all(doubling_copies(n) < 2 * n for n in range(1, 5000)))
check("l1.s4 wrong values 120, 31", sum(range(16)) == 120 and 1 + 2 + 4 + 8 + 16 == 31)

# CPython list growth: about one eighth, total copies linear
xs, caps, last = [], [], sys.getsizeof([])
for i in range(200000):
    xs.append(i)
    s = sys.getsizeof(xs)
    if s != last:
        caps.append((len(xs) - 1, (s - sys.getsizeof([])) // 8))
        last = s
ratios = [caps[k + 1][1] / caps[k][1] for k in range(len(caps) - 1) if caps[k][1] > 1000]
check("l1.s4 CPython grows lists by about an eighth", all(1.11 < r < 1.14 for r in ratios),
      f"growth ratios {min(ratios):.4f}..{max(ratios):.4f}")
total_copied = sum(n for n, _ in caps)  # worst case: every regrowth moves the block
check("l1.s4 total copies stay linear at 1/8 growth", total_copied < 10 * 200000,
      f"{total_copied} element moves for 200000 appends")

# amortised append timing: per-append cost flat across sizes
def per_append(n):
    t = time.perf_counter(); a = []
    for i in range(n):
        a.append(i)
    return (time.perf_counter() - t) / n
p_small, p_big = min(per_append(20000) for _ in range(5)), min(per_append(2000000) for _ in range(3))
check("l1 append O(1) amortised (timing)", p_big < 4 * p_small, f"{p_small:.2e}s vs {p_big:.2e}s per append")

# front insert is linear, total quadratic
def t_front(n):
    t = time.perf_counter(); a = []
    for i in range(n):
        a.insert(0, i)
    return time.perf_counter() - t
r = min(t_front(40000) for _ in range(3)) / min(t_front(10000) for _ in range(3))
check("l1.s5 insert(0) loop quadratic (timing, 4x n gives about 16x)", r > 6, f"ratio {r:.1f}")
check("l1.s5 499500 shifts", sum(range(1000)) == 499500 and sum(range(1, 1001)) == 500500)
check("l1.s6 float 24 bytes, pointer 8", sys.getsizeof(1.5) == 24 and
      (sys.getsizeof([0, 0]) - sys.getsizeof([0])) == 8 and (8 + 24) * 10**6 == 32 * 10**6)
check("l1.s7 5,005,000 characters", sum(10 * k for k in range(1, 1001)) == 5005000)
try:
    s = "VOD"; s[0] = "B"; ok = False
except TypeError as e:
    ok = "does not support item assignment" in str(e)
check("l1 quiz str item assignment TypeError", ok)
try:
    [][0]; ok = False
except IndexError as e:
    ok = str(e) == "list index out of range"
check("l1 quiz IndexError text", ok)
check("l1.s9 csv", ",".join(f"{p:.2f}" for p in [99.999]) == "100.00" and ",".join([]) == "")


class Cnt:
    n = 0

    def __init__(self, v):
        self.v = v

    def __eq__(self, o):
        Cnt.n += 1
        return self.v == o.v

    def __hash__(self):
        return hash(self.v)


w = [Cnt(i) for i in range(20)]
probe = Cnt(0)  # equal to w[0] but a different object, so == must run
Cnt.n = 0
w.remove(probe)
check("l1.s10 option 'remove(window[0])' is 'two linear steps' (search is linear)", Cnt.n > 1,
      f"the search stops after {Cnt.n} comparison; with the same object identity matches with 0 calls")
d = deque(maxlen=3)
for i in range(5):
    d.append(i)
check("l1.s10 deque(maxlen) drops oldest", list(d) == [2, 3, 4])

# l2 toy hash
h = lambda t: sum(ord(c) - 64 for c in t) % 5
check("l2 toy buckets", [h(t) for t in ["VOD", "BP", "HSBA", "AZN", "GSK", "RIO", "TSCO", "BT", "BARC", "SHEL"]]
      == [1, 3, 0, 1, 2, 2, 2, 2, 4, 4])
check("l2 letter sums", sum(ord(c) - 64 for c in "BARC") == 24 and sum(ord(c) - 64 for c in "SHEL") == 44
      and round(24 / 5) == 5 and 44 // 5 == 8)


class Bad(Cnt):
    def __hash__(self):
        return 1


def lookups(cls, n):
    d = {cls(i): i for i in range(n)}
    Cnt.n = 0
    for i in range(n):
        d[cls(i)]
    return Cnt.n / n


good, worst = lookups(Cnt, 2000), lookups(Bad, 2000)
check("l2 hash lookup O(1) average, O(n) when all keys collide", good < 3 and worst > 500,
      f"eq calls per lookup: spread {good:.2f}, all-collide {worst:.0f} (n=2000)")
check("l2.s4/s5/s9 counts", 10000 * 10000 == 10**8 and abs(2e6**2 / 2 - 2e12) < 1 and 501 / 2 * 10**6 == 250500000)
random.seed(1)
ref = list(range(500))
sim = sum(ref.index(random.randrange(500)) + 1 for _ in range(200000)) / 200000
check("l2.s9 mean 250.5 comparisons per row (Monte Carlo)", abs(sim - 250.5) < 2, f"{sim:.2f}")
for bad_key in ([1], {1: 2}):
    try:
        {bad_key: 1}; ok = False
    except TypeError as e:
        ok = "unhashable type" in str(e)
    check(f"l2 {type(bad_key).__name__} unhashable", ok)
check("l2 tuple key ok; .get default", {("VOD", "2024-03-01"): 1} and {}.get("VOD") is None)


def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return (seen[need], i)
        seen[x] = i
    return None


def two_sum_bug(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        seen[x] = i
        if target - x in seen:
            return (seen[target - x], i)
    return None


check("l3 two-sum traces", two_sum([6, 1, 9, 4, 7], 13) == (2, 3) and two_sum([3, 3], 6) == (0, 1)
      and two_sum([1250, 830, 2100, 1670, 420], 2500) == (1, 3) and two_sum([300, -100, 200, -300], 0) == (0, 3)
      and two_sum([1, 5, 1, 5], 6) == (0, 1) and two_sum([5], 10) is None
      and two_sum(list(range(100000)), 199997) == (99998, 99999))
check("l3.s5 store-first bug", two_sum_bug([3, 4, 1], 6) == (0, 0) and two_sum_bug([5], 10) == (0, 0))
check("l3 unique pair in [3,8,5,12,6]", sum(1 for i in range(5) for j in range(i + 1, 5)
                                           if [3, 8, 5, 12, 6][i] + [3, 8, 5, 12, 6][j] == 17) == 1)

# l4
try:
    c = {}; c["VOD"] += 1; ok = False
except KeyError as e:
    ok = e.args == ("VOD",)
check("l4.s4 KeyError on +=", ok)
dd = defaultdict(int); dd["VOD"] += 2
check("l4 quiz defaultdict read inserts", (dd["BP"], len(dd)) == (0, 2))
check("l4 Counter", Counter("banana").most_common(1) == [("a", 3)] and set("trades") == set("traders")
      and Counter("") == Counter("") and Counter("Listen") != Counter("silent") and Counter({"a": 1}) == {"a": 1})
check("l4 most_common tie keeps first seen", Counter(["VOD", "BP", "VOD", "AZN", "BP"]).most_common(1)[0][0] == "VOD")
try:
    sum(["a", "b"], ""); ok = False
except TypeError as e:
    ok = "join" in str(e)
check("review-1 r-join sum() of strings refused", ok)
check("review-1 r-key collisions", ord("a") + ord("d") == ord("b") + ord("c") and frozenset("aab") == frozenset("ab"))
check("hw1 pair_count 4999950000", 100000 * 99999 // 2 == 4999950000)
check("hw1 reconcile counts", 200000 * 199999 // 2 == 19999900000 and 200**2 == 40000)

# ---------------------------------------------------------------- level 2
def walk(nums, t):
    i, j, sums = 0, len(nums) - 1, []
    while i < j:
        s = nums[i] + nums[j]; sums.append(s)
        if s == t:
            return (i, j), sums
        if s < t:
            i += 1
        else:
            j -= 1
    return None, sums


a7 = [1, 3, 4, 6, 8, 11, 15]
check("l5 walks", walk(a7, 10) == ((2, 3), [16, 12, 9, 11, 9, 10]) and walk(a7, 20) == (None, [16, 18, 19, 21, 17, 19])
      and walk([-120, -75, -40, 15, 60, 90, 135], 50) == ((2, 5), [15, 60, 15, 50])
      and walk([8, 3, 5, 1, 9], 10)[0] is None and walk([2, 5, 9, 12, 20], 21)[0] == (2, 3))
random.seed(2)
ok = True
for _ in range(3000):
    n = random.randint(0, 12); v = sorted(random.randint(-9, 9) for _ in range(n)); t = random.randint(-12, 12)
    res, sums = walk(v, t)
    exists = any(v[i] + v[j] == t for i in range(n) for j in range(i + 1, n))
    ok &= (res is not None) == exists and len(sums) <= max(n - 1, 0)
check("l5 two pointers correct on sorted input, at most n-1 sums (3000 random lists)", ok)
sq = sorted(x * x for x in [-7, -3, -1, 2, 4, 6])
check("l5.s4 feedback c3 '2 is nearest zero, its square is the smallest, first slot'", sq[0] == 4,
      f"squares sorted {sq}: -1 is nearest zero; 4 is second smallest")
xs5 = [3, 8, 1, 9, 4]
for i in range(len(xs5)):
    xs5[i], xs5[-1 - i] = xs5[-1 - i], xs5[i]
check("l5 quiz double swap", xs5 == [3, 8, 1, 9, 4])
check("l5 quiz strangle payoff (put 100, call 105)",
      [max(100 - s, 0) + max(s - 105, 0) for s in range(90, 120, 5)] == [10, 5, 0, 0, 5, 10])

v8 = [4, 2, 7, 1, 8, 3, 6, 5]
check("l6 window sums", [sum(v8[s:s + 3]) for s in range(6)] == [13, 10, 16, 12, 17, 14]
      and 981 * 20 == 19620 and 20 + 2 * 980 == 1980 and 100 < 751 * 250 / (250 + 2 * 750) < 110)
vol = [420, 380, 510, 610, 450, 390, 700, 650, 300, 480]
check("l6.s9 totals", [sum(vol[s:s + 5]) for s in range(6)] == [2370, 2340, 2660, 2800, 2490, 2520]
      and sum(sorted(vol)[-5:]) == 2950)


def lu_bug(s):
    last, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in last:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best


def lu(s):
    last, left, best = {}, 0, 0
    for right, ch in enumerate(s):
        if ch in last:
            left = max(left, last[ch] + 1)
        last[ch] = right
        best = max(best, right - left + 1)
    return best


check("l6.s6 trap returns 3 on 'abba'", lu_bug("abba") == 3 and lu("abba") == 2)
check("l6.s6 prose 'this version passes abcbdae'", lu_bug("abcbdae") == lu("abcbdae"),
      f"buggy version returns {lu_bug('abcbdae')}, correct is {lu('abcbdae')}")
check("[fix] buggy version passes 'abcbd'", lu_bug("abcbd") == lu("abcbd") == 3)
check("l6 longest_unique tests", [lu(s) for s in ["abcbdae", "pwwkew", "tmmzuxt", ""]] == [5, 3, 5, 0])


def shrink(xs, k):
    left = total = 0; lens = []
    for right, x in enumerate(xs):
        total += x
        while total >= k:
            lens.append(right - left + 1); total -= xs[left]; left += 1
    return lens


check("l6 shrinking window", shrink([2, 3, 1, 2, 4, 3], 7) == [4, 4, 3, 3, 2] and shrink([5, -4, 6], 6) == [3]
      and min(shrink([1, 4, 2, 3, 5], 8)) == 2 and min(shrink([12, 3, 7, 9, 4, 15, 2], 20)) == 3)
check("hw2 h-min-volume feedback '[12,3,7,9] is the first window to reach 20'",
      shrink([12, 3, 7, 9, 4, 15, 2], 20)[0] == 4, "the first window to reach 20 is [12, 3, 7] = 22, length 3")
# l6 quiz off-by-one update: total_k = correct_k + x[0] - x[k]
xs = [3, 9, 3, 5, 3, 1]; w = 2
tot = sum(xs[:w]); wrong_ok = []
for right in range(w, len(xs)):
    tot += xs[right] - xs[right - w + 1]
    wrong_ok.append(tot == sum(xs[right - w + 1:right + 1]))
check("l6 quiz option 'every sum after the first is wrong'", not any(wrong_ok),
      f"on {xs}, w=2 the buggy update is right at steps {[i for i, o in enumerate(wrong_ok) if o]}: error is x[0]-x[k]")
check("l6 max_window_sum big test", sum(range(180000, 200000)) == 3799990000 and 180001 * 20000 > 3.5e9)

p = [3, -1, 4, 2, -5, 6]
pre = [0]
for x in p:
    pre.append(pre[-1] + x)
check("l7 prefix", pre == [0, 3, 2, 6, 8, 3, 9] and pre[4] - pre[1] == 5 and pre[6] - pre[2] == 7
      and [3, 2, 6, 8, 3, 9][2] - [3, 2, 6, 8, 3, 9][-1] == -3)


def cnt(xs, k, start=True):
    seen = {0: 1} if start else {}
    total = count = 0
    for x in xs:
        total += x; count += seen.get(total - k, 0); seen[total] = seen.get(total, 0) + 1
    return count


def brute(xs, k):
    return sum(1 for i in range(len(xs)) for j in range(i + 1, len(xs) + 1) if sum(xs[i:j]) == k)


random.seed(3)
check("l7 count_subarrays equals brute force (2000 random lists with negatives)",
      all(cnt(v, k) == brute(v, k) for v, k in (([random.randint(-3, 3) for _ in range(random.randint(0, 9))],
                                                random.randint(-3, 3)) for _ in range(2000))))
check("l7 counts", cnt([2, -1, 1, 3, -2, 2], 3) == 5 and cnt([0, 0, 0], 0) == 6 and cnt([0, 0, 0], 0, False) == 3
      and cnt([1, -1] * 10000, 0) == 10**8 and cnt([1, 2, 1, 2], 3) == 3 and cnt([3, 4, -7, 3, 1, 3, 1, -4], 7) == 3)
cum = [120, 40, 240, 290, 140, 230, 190, 370, 310, 420]
check("l7.s9", cum[6] - cum[2] == -50 and max(max(cum[:i + 1]) - cum[i] for i in range(10)) == 150)
r2 = [0, 4, 1, 7, 10, 6]
check("review-2 r-range slip 'off' = 9 is pre[4]-pre[0]", r2[4] - r2[0] == 9,
      f"pre[4]-pre[0] = {r2[4] - r2[0]}; 9 is pre[4]-pre[2] = {r2[4] - r2[2]}")
check("review-2 r-slide slip 'kept' = 15 is 'added without dropping'", 6 + 4 + 6 == 15,
      f"adding 4 and 6 without dropping gives {6 + 4 + 6}; 15 = 5 + 4 + 6 keeps the 5 and drops the 1")
G = [[2, -1, 3], [0, 4, 1], [5, -2, 2]]
P = [[0] * 4 for _ in range(4)]
for r_ in range(3):
    for c_ in range(3):
        P[r_ + 1][c_ + 1] = G[r_][c_] + P[r_][c_ + 1] + P[r_ + 1][c_] - P[r_][c_]
check("hw2 grid", P[1][1:] == [2, 1, 4] and P[2][1:] == [2, 5, 9] and P[3][1:] == [7, 8, 14]
      and P[3][3] - P[1][3] - P[3][1] + P[1][1] == 5)

px = [102, 110, 104, 98, 101, 107, 95, 99, 103, 97]


def best_trade(prices):
    lo, best = 0, (0, 0, 0)
    for j in range(1, len(prices)):
        profit = prices[j] - prices[lo]
        if profit > best[2]:
            best = (lo, j, profit)
        if prices[j] < prices[lo]:
            lo = j
    return best


def brute_trade(prices):
    best = (0, 0, 0)
    for j in range(len(prices)):       # earliest sell day, then earliest buy day
        for i in range(j):
            if prices[j] - prices[i] > best[2]:
                best = (i, j, prices[j] - prices[i])
    return best


random.seed(4)
check("l8 best_trade equals brute force with the stated tie rule (3000 random lists)",
      all(best_trade(v) == brute_trade(v) for v in ([random.randint(1, 9) for _ in range(random.randint(1, 9))]
                                                    for _ in range(3000))))
check("l8 numbers", best_trade(px) == (3, 5, 9) and max(px) - min(px) == 15 and 2520 * 2519 // 2 == 3173940
      and max(max(px[:i + 1]) - px[i] for i in range(10)) == 15)
low, best = 110, 104 - 110
for q in [104, 101, 97]:
    best = max(best, q - low); low = min(low, q)
check("l8.s4 colleague returns -3", best == -3)
ch = [px[i + 1] - px[i] for i in range(9)]
check("l8.s6 changes", ch == [8, -6, -6, 3, 6, -12, 4, 4, -6])
run = bst = 0; trace = []
for x in [-2, 5, -1, 4, -6, 3]:
    run = max(run + x, 0); trace.append(run); bst = max(bst, run)
check("l8 quiz Kadane trace", trace == [0, 5, 4, 8, 2, 5] and bst == 8)
# l8.s9: the ceiling already assumes perfect foresight, so look-ahead cannot beat it
check("l8.s9 explain 'a look-ahead bug is a common cause of beating best_trade'",
      max(px[j] - px[i] for j in range(10) for i in range(j)) > 9,
      "max over ALL buy-before-sell pairs on these closes is 9: perfect foresight reaches 9, never 12")
# drawdown convention: absolute and fractional can pick different episodes
dd = [100, 60, 200, 130]
ab = max((max(dd[:i + 1]) - dd[i], i) for i in range(4)); fr = max(((max(dd[:i + 1]) - dd[i]) / max(dd[:i + 1]), i) for i in range(4))
check("[basis] absolute and fractional max drawdown can be different episodes", ab[1] != fr[1], f"abs {ab}, frac {fr}")

# ---------------------------------------------------------------- level 3
def ev(tokens):
    st = []
    for t in tokens.split():
        if t in "+-*/" and len(t) == 1:
            b = st.pop(); a = st.pop()
            st.append({"+": a + b, "-": a - b, "*": a * b, "/": a / b if b else 0}[t])
        else:
            st.append(float(t))
    return st.pop()


check("l9 postfix", ev("5 1 2 + 4 * + 3 -") == 14 and ev("2 3 4 * +") == 14 and ev("4 2 5 * + 1 -") == 13
      and ev("2 3 4 * -") == -10 and (5 + 3 * 4 == 17) and (2 + 3) * 4 == 20 and (4 + 2) * 5 - 1 == 29)


def bal_bug(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in "([{":
            stack.append(c)
        elif stack.pop() != pairs[c]:
            return False
    return True


try:
    bal_bug(")"); ok = False
except IndexError as e:
    ok = str(e) == "pop from empty list"
check("l9.s6 trap", ok and bal_bug("((") is True and bal_bug("{[()]}") is True and bal_bug("([)]") is False)


def first_bad(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for i, c in enumerate(s):
        if c in "([{":
            stack.append(i)
        elif c in pairs:
            if not stack or s[stack.pop()] != pairs[c]:
                return i
    return stack[0] if stack else -1


check("l9.s10 first_bad table", [first_bad(s) for s in ["(spot - strike) * (1 + rate)",
      "max(0, (spot - strike) * (1 + rate)", "vol * sqrt(t))", "[(a + b])", "(a)(b))("]] == [-1, 3, 13, 7, 6])


def next_greater(xs, strict=True):
    ans, st, ops = [-1] * len(xs), [], 0
    for i, x in enumerate(xs):
        while st and (xs[st[-1]] < x if strict else xs[st[-1]] <= x):
            ans[st.pop()] = x; ops += 1
        st.append(i); ops += 1
    return ans, ops, [xs[k] for k in st]


random.seed(5)
ok = True
for _ in range(2000):
    v = [random.randint(0, 6) for _ in range(random.randint(0, 12))]
    a, ops, _ = next_greater(v)
    ok &= a == [next((y for y in v[i + 1:] if y > x), -1) for i, x in enumerate(v)] and ops <= 2 * len(v)
check("l10 monotonic stack equals nested scan, pushes+pops <= 2n (2000 random lists)", ok)
check("l10 traces", next_greater([4, 2, 6, 3, 1, 5, 7])[0] == [6, 6, 7, 5, 5, 7, -1]
      and next_greater([5, 5, 6], False)[0] == [5, 6, -1] and next_greater([6, 4, 5, 2])[2] == [6, 5, 2]
      and next_greater([3, 1, 4, 1, 5, 9, 2, 6])[2] == [9, 6] and next_greater([3, 8, 4, 1, 9])[0] == [8, 9, 9, 9, -1]
      and sum(range(6)) == 15)
hs = [2, 1, 5, 6, 2, 3]
check("l10.s8 largest rectangle 10", max(min(hs[i:j]) * (j - i) for i in range(6) for j in range(i + 1, 7)) == 10)


def days(prices):
    ans, st = [0] * len(prices), []
    for i, p_ in enumerate(prices):
        while st and prices[st[-1]] < p_:
            j = st.pop(); ans[j] = i - j
        st.append(i)
    return ans


check("l10.s9 table", days([101.2, 100.5, 102.0, 101.0, 100.8, 103.5, 103.1]) == [2, 1, 3, 2, 1, 0, 0]
      and days([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0])


def msw(xs, w, front=True, guard=True):
    dq, out = deque(), []
    for i, x in enumerate(xs):
        if front:
            if guard:
                if dq and dq[0] <= i - w:
                    dq.popleft()
            else:
                if dq[0] <= i - w:       # the line as printed in l11.s7 explain
                    dq.popleft()
        while dq and xs[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= w - 1:
            out.append(xs[dq[0]])
    return out


random.seed(6)
check("l11 monotonic deque equals max of each slice (2000 random lists)",
      all(msw(v, w) == [max(v[i:i + w]) for i in range(len(v) - w + 1)]
          for v, w in (([random.randint(0, 6) for _ in range(random.randint(0, 12))], random.randint(1, 5))
                       for _ in range(2000))))
check("l11 traces", msw([5, 3, 4, 1, 2, 6], 3) == [5, 4, 4, 6] and msw([5, 3, 4, 1, 2, 6], 3, front=False) == [5, 5, 5, 6]
      and msw([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7] and msw([2, 7, 3, 1, 5, 4], 2) == [7, 7, 3, 5, 5])
try:
    res = msw([5, 3, 4, 1, 2, 6], 3, guard=False); ok = res == [5, 4, 4, 6]; note = ""
except IndexError as e:
    ok = False; note = f"IndexError on the first pass: {e}"
check("l11.s7 explain fix 'if dq[0] <= i - w: dq.popleft()' before the back pops", ok, note)


def t_drain(n, use_deque):
    q = deque(range(n)) if use_deque else list(range(n))
    t = time.perf_counter()
    if use_deque:
        while q:
            q.popleft()
    else:
        while q:
            q.pop(0)
    return time.perf_counter() - t


rl = min(t_drain(120000, False) for _ in range(3)) / min(t_drain(30000, False) for _ in range(3))
rd = min(t_drain(1200000, True) for _ in range(3)) / min(t_drain(300000, True) for _ in range(3))
check("l11 draining a list with pop(0) is quadratic, a deque linear (timing, 4x n)", rl > 6 and rd < 6,
      f"list ratio {rl:.1f}, deque ratio {rd:.1f}")
big = deque(range(2_000_000))
def t_idx(k):
    t = time.perf_counter()
    for _ in range(300):
        big[k]
    return time.perf_counter() - t
mid, end = min(t_idx(1_000_000) for _ in range(3)), min(t_idx(-1) for _ in range(3))
check("hw3 deque indexing near the middle is O(n), ends O(1) (timing)", mid > 20 * end, f"middle/end {mid / end:.0f}x")


class RateLimiter:
    def __init__(self, k, t):
        self.k, self.t, self.times = k, t, deque()

    def allow(self, now):
        while self.times and self.times[0] <= now - self.t:
            self.times.popleft()
        if len(self.times) < self.k:
            self.times.append(now); return True
        return False


rl_ = RateLimiter(2, 10); rl2 = RateLimiter(100, 1000)
check("l11.s9 limiter", [rl_.allow(x) for x in [0, 5, 9, 10, 15, 20]] == [True, True, False, True, True, True]
      and sum(rl2.allow(x) for x in range(0, 2000, 5)) == 200)
check("l11 quiz", 250 - 20 + 1 == 231 and 100 * 10 + 50 * 12 == 1600 and 100 * 12 + 50 * 10 == 1700
      and 10**12 / 2 == 5e11)
check("hw3 FIFO", 200 * 50 + 100 * 52 + 50 * 49 == 17650 and 300 * 49 + 50 * 52 == 17300
      and round((200 * 50 + 100 * 52 + 300 * 49) / 600 * 350, 2) == 17441.67)


class Node:
    def __init__(self, val, next=None):
        self.val, self.next = val, next


def from_list(vs):
    h = None
    for v in reversed(vs):
        h = Node(v, h)
    return h


def to_list(h, limit=10**6):
    out = []
    while h and len(out) < limit:
        out.append(h.val); h = h.next
    return out


def rev_bug(head):
    prev, cur = None, head
    while cur:
        cur.next = prev; prev = cur; cur = cur.next
    return prev


check("l12.s5 trap returns [7]", to_list(rev_bug(from_list([7, 3, 9, 4]))) == [7])
a = from_list([7, 3, 9, 4]).next
del a.next
try:
    a.next; ok = False
except AttributeError:
    ok = True
check("l12.s3 'del a.next' then walking raises AttributeError", ok)


def remove_nth(head, n, gap=1):
    dummy = Node(0, head); fast = slow = dummy
    for _ in range(n + gap):
        fast = fast.next
    while fast:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next


check("l12 remove_nth", to_list(remove_nth(from_list([7, 3, 9, 4]), 2)) == [7, 3, 4]
      and to_list(remove_nth(from_list([1, 2, 3]), 3)) == [2, 3]
      and to_list(remove_nth(from_list([1, 2, 3, 4, 5]), 2, gap=0)) == [1, 2, 3, 4])


def make_cycle(n, pos):
    nodes = [Node(i) for i in range(n)]
    for i in range(n - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes


def floyd(head, fs=2):
    slow = fast = head; moves = 0; trace = []
    while True:
        for _ in range(fs):
            if fast is None:
                return None, moves, trace
            fast = fast.next
        if fast is None:
            return None, moves, trace
        slow = slow.next; moves += 1; trace.append((slow.val, fast.val))
        if slow is fast:
            return slow, moves, trace
        if moves > 10**5:
            return "never", moves, trace


n6 = make_cycle(6, 2)
check("l13.s2 positions (values are index+1)", [(a + 1, b + 1) for a, b in floyd(n6[0])[2]] == [(2, 3), (3, 5), (4, 3), (5, 5)])
check("review-3 r-meet", floyd(make_cycle(8, 3)[0])[2] == [(1, 2), (2, 4), (3, 6), (4, 3), (5, 5)])
random.seed(7)
ok = True
for _ in range(1500):
    n = random.randint(1, 40); pos = random.randint(-1, n - 1)
    nodes = make_cycle(n, pos)
    meet, moves, _ = floyd(nodes[0])
    if pos < 0:
        ok &= meet is None
    else:
        L = n - pos; a_ = pos
        ok &= meet is not None and moves <= a_ + L and moves % L == 0   # a+b = kL, within L moves of entry
        s2 = nodes[0]
        while s2 is not meet:
            s2, meet = s2.next, meet.next
        ok &= s2 is nodes[pos]
check("l13 Floyd: meets within L moves of slow entering, a+b=kL, reset finds the start (1500 random lists)", ok)
check("l13.s6 'a speed of 3 against 1 could skip over 0'", floyd(make_cycle(4, 0)[1].next and make_cycle(4, 0)[0], 3)[0] is not None
      and any(floyd(make_cycle(L, 0)[0], 3)[0] is not None for L in (3, 5)), "speed 3 still meets from a common start")
# speed 3 vs 1 from an odd gap in an even cycle never meets
nodes = make_cycle(4, 0); s_, f_ = nodes[0], nodes[1]; met = False
for _ in range(1000):
    s_ = s_.next; f_ = f_.next.next.next
    met |= s_ is f_
check("[basis] speeds 3 and 1, gap 1 in a cycle of 4: never meet", not met)


def middle(h):
    slow = fast = h
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow


check("l13 middle", [middle(from_list(list(range(1, k + 1)))).val for k in (1, 2, 4, 5, 6)] == [1, 2, 3, 3, 4]
      and middle(None) is None)
od = OrderedDict(a=1, b=2); od.move_to_end("a")
check("hw3 OrderedDict.move_to_end", list(od) == ["b", "a"])
# review-3 r-depth: evaluator stack height is not the nesting depth
def infix_peak(expr):
    vals, peak = [], 0
    for t in expr.replace("(", " ( ").replace(")", " ) ").split():
        if t.isdigit():
            vals.append(t); peak = max(peak, len(vals))
        elif t == ")":
            vals.pop()   # two operands collapse to one result
    return peak
check("review-3 r-depth prose 'deepest nesting tells you how many intermediate results a stack evaluator holds'",
      infix_peak("(1 + (2 * (3 - 4)))") == 3, f"depth 3 but a two-stack evaluator holds {infix_peak('(1 + (2 * (3 - 4)))')} operands at once")

# homework-2 h-difference: the i == j guard never fires when d > 0
def hpd(nums, d, guard):
    i, j, fired = 0, 1, False
    while j < len(nums):
        if i == j:
            fired = True
            if guard:
                j += 1
                continue
        gap = nums[j] - nums[i]
        if gap == d:
            return True, fired
        if gap < d:
            j += 1
        else:
            i += 1
    return False, fired


random.seed(8)
ok = True
for _ in range(4000):
    v = sorted(random.randint(-9, 9) for _ in range(random.randint(0, 10))); d_ = random.randint(1, 8)
    g, ng = hpd(v, d_, True), hpd(v, d_, False)
    truth = any(v[b] - v[a] == d_ for a in range(len(v)) for b in range(a + 1, len(v)))
    ok &= g[0] == ng[0] == truth
check("[basis] hw2 h-difference: with d > 0 the answer is the same with or without the i == j guard (4000 lists)", ok)
check("[fix] l11 test with w = 20000 has the same first three maxima",
      msw(list(range(200000, 0, -1)), 20000)[:3] == [200000, 199999, 199998])

# ------------------------------------------------- every code widget, run
# Each Python code widget in levels 1 to 3: the solution must pass every
# hidden test and the starter must fail at least one (CPython; the app runs
# the same code in Pyodide).
import json
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "app", "content", "courses", "ds")
course = json.load(open(os.path.join(ROOT, "course.json")))
files = []
for lv in course["levels"][:3]:
    files += lv["lessons"] + [lv["review"], lv["homework"]]


def run_widget(w, src):
    ns = {"__learner_source__": src}
    try:
        exec(w.get("prelude", ""), ns)
        exec(src, ns)
    except Exception as e:
        return [f"load: {e!r}"]
    bad = []
    for k, t in enumerate(w["tests"], 1):
        try:
            if t.get("setup"):
                exec(t["setup"], ns)
            got = eval(t["call"], ns)
            exp = t["expect"]
            exp = eval(exp, ns) if isinstance(exp, str) else exp
            if not (got == exp and (type(got) is type(exp) or isinstance(got, (int, float, bool)))):
                bad.append(f"test {k}: got {got!r}, expected {exp!r}")
        except Exception as e:
            bad.append(f"test {k}: {type(e).__name__}")
    return bad


n_code = 0
for f in files:
    d = json.load(open(os.path.join(ROOT, f + ".json")))
    blocks = [("screens", d.get("screens", [])), ("quiz", d.get("quiz", [])), ("items", d.get("items", []))]
    for name, arr in blocks:
        for i, it in enumerate(arr):
            w = it.get("widget") or {}
            if w.get("kind") != "code":
                continue
            n_code += 1
            assert w.get("language") == "python", (f, name, i)
            sol = run_widget(w, w["solution"])
            sta = run_widget(w, w["starter"])
            check(f"code {f} {name}[{i}] solution passes {len(w['tests'])} tests", not sol, "; ".join(sol[:2]))
            check(f"code {f} {name}[{i}] starter fails", bool(sta))
print(f"{n_code} code widgets run")

print()
print(f"{len(FAILS)} failing check(s)")
for f in FAILS:
    print("  -", f)
sys.exit(1 if FAILS else 0)
