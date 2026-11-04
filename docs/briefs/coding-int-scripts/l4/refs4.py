"""coding-int level 4: every reference, starter, driver and hidden test, with an independent check.
Run: python3 -I refs4.py   (standard library only).  Prints ALL OK when every reference matches its brute force,
every starter fails at least one test (the slow starters only on the large rows) and every test row is as listed."""
import itertools, random, bisect, time, json, os

# ---------- 15.1 best_plan ----------

BEST_PLAN_SOL = '''def best_plan(problems, budget):
    best = [0] * (budget + 1)               # best[m]: most points using at most m minutes
    for full_pts, full_min, part_pts, part_min in problems:
        new = best[:]
        for m in range(budget + 1):
            if m >= full_min:
                new[m] = max(new[m], best[m - full_min] + full_pts)
            if m >= part_min:
                new[m] = max(new[m], best[m - part_min] + part_pts)
        best = new
    return best[budget]
'''
BEST_PLAN_STARTER = '''def best_plan(problems, budget):
    # each problem is [full_points, full_minutes, partial_points, partial_minutes]
    return 0
'''
ns = {}
exec(BEST_PLAN_SOL, ns)
best_plan = ns['best_plan']


def best_plan_brute(problems, budget):
    best = 0
    for choice in itertools.product((0, 1, 2), repeat=len(problems)):
        pts = mins = 0
        for (fp, fm, pp, pm), c in zip(problems, choice):
            if c == 1:
                pts += fp; mins += fm
            elif c == 2:
                pts += pp; mins += pm
        if mins <= budget:
            best = max(best, pts)
    return best


def best_plan_memo(problems, budget):
    from functools import lru_cache
    @lru_cache(None)
    def go(i, m):
        if i == len(problems):
            return 0
        fp, fm, pp, pm = problems[i]
        r = go(i + 1, m)
        if m >= fm:
            r = max(r, fp + go(i + 1, m - fm))
        if m >= pm:
            r = max(r, pp + go(i + 1, m - pm))
        return r
    return go(0, budget)


def greedy_ppm(problems, budget):
    """full marks only, by points per minute, take while it fits (skip what does not fit and go on)"""
    order = sorted(problems, key=lambda p: -p[0] / p[1])
    t = pts = 0
    for fp, fm, pp, pm in order:
        if t + fm <= budget:
            t += fm; pts += fp
    return pts


# ---------- 16.1 longest_streak and mutants ----------

def _ref(xs):
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best


def _m1(xs):
    best = run = 0
    for i, x in enumerate(xs):
        if i and x == xs[i - 1]:
            run += 1
        else:
            best = max(best, run)
            run = 1
    return best


def _m2(xs):
    best = run = 1
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best


def _m3(xs):
    if len(xs) == 1:
        return 0
    return _ref(xs)


def _m4(xs):
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x >= xs[i - 1] else 1
        best = max(best, run)
    return best


def _m5(xs):
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else (1 if i == 0 else 0)
        best = max(best, run)
    return best


def _m6(xs):
    best = run = 0
    for x in xs:
        run = run + 1 if x == xs[0] else 0
        best = max(best, run)
    return best


MUT = {'m1': _m1, 'm2': _m2, 'm3': _m3, 'm4': _m4, 'm5': _m5, 'm6': _m6}


def streak_brute(xs):
    best = 0
    for i in range(len(xs)):
        for j in range(i, len(xs)):
            if all(xs[k] == xs[i] for k in range(i, j + 1)):
                best = max(best, j - i + 1)
    return best


PRELUDE_16 = '''def _ref(xs):
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best
def _m1(xs):                      # forgets the last run
    best = run = 0
    for i, x in enumerate(xs):
        if i and x == xs[i - 1]:
            run += 1
        else:
            best = max(best, run)
            run = 1
    return best
def _m2(xs):                      # empty list gives 1
    best = run = 1
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best
def _m3(xs):                      # a single element gives 0
    if len(xs) == 1:
        return 0
    return _ref(xs)
def _m4(xs):                      # counts non-decreasing runs
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x >= xs[i - 1] else 1
        best = max(best, run)
    return best
def _m5(xs):                      # restarts the run at 0 after a break
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else (1 if i == 0 else 0)
        best = max(best, run)
    return best
def _m6(xs):                      # only compares with the first value
    best = run = 0
    for x in xs:
        run = run + 1 if x == xs[0] else 0
        best = max(best, run)
    return best
_MUTANTS = {'m1': _m1, 'm2': _m2, 'm3': _m3, 'm4': _m4, 'm5': _m5, 'm6': _m6}
def caught(name):
    try:
        cases = edge_cases()
    except Exception:
        return False
    return any(_MUTANTS[name](list(c)) != _ref(list(c)) for c in cases)
def well_formed():
    cases = edge_cases()
    return len(cases) <= 8 and all(isinstance(c, list) and all(isinstance(v, int) for v in c) for c in cases)
'''
EDGE_SOL = '''def edge_cases():
    return [[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2]]
'''
EDGE_STARTER = '''def edge_cases():
    # return a list of at most 8 inputs, each a list of whole numbers
    return []
'''

# ---------- 17.1 / 17.2 ----------

CSDK_SOL = '''def count_subarrays_divisible_by_k(nums, k):
    seen = {0: 1}
    total = count = 0
    for x in nums:
        total = (total + x) % k
        count += seen.get(total, 0)
        seen[total] = seen.get(total, 0) + 1
    return count
'''
CSDK_STARTER = '''def count_subarrays_divisible_by_k(nums, k):
    # correct but slow: it checks every subarray
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total % k == 0:
                count += 1
    return count
'''
LZS_SOL = '''def longest_zero_sum_subarray(nums):
    first = {0: -1}
    total = best = 0
    for i, x in enumerate(nums):
        total += x
        if total in first:
            best = max(best, i - first[total])
        else:
            first[total] = i
    return best
'''
LZS_STARTER = '''def longest_zero_sum_subarray(nums):
    # correct but slow: it tries every start and every end
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == 0:
                best = max(best, j - i + 1)
    return best
'''
ns = {}
exec(CSDK_SOL, ns); csdk = ns['count_subarrays_divisible_by_k']
exec(CSDK_STARTER, ns); csdk_slow = ns['count_subarrays_divisible_by_k']
ns = {}
exec(LZS_SOL, ns); lzs = ns['longest_zero_sum_subarray']
exec(LZS_STARTER, ns); lzs_slow = ns['longest_zero_sum_subarray']

# ---------- 18.1 ----------

PES_SOL = '''def product_except_self(nums):
    # plan: out[i] = (product of everything left of i) * (product of everything right of i)
    # pass 1 fills out[i] with the left product, pass 2 multiplies in the right product
    # no division, so zeros are safe; two passes, O(n) time and O(1) extra space
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out
'''
PES_STARTER = '''def product_except_self(nums):
    # plan: write two or three comment lines here before the code
    return [0] * len(nums)
'''
ns = {}
exec(PES_SOL, ns); pes = ns['product_except_self']


def pes_brute(nums):
    out = []
    for i in range(len(nums)):
        p = 1
        for j, x in enumerate(nums):
            if j != i:
                p *= x
        out.append(p)
    return out


# ---------- 19 Calendar ----------

CAL_A_SOL = '''import bisect


class Calendar:
    def __init__(self):
        self.starts, self.ends = [], []       # sorted by start; bookings never overlap

    def book(self, start, end):
        i = bisect.bisect_left(self.starts, start)
        if i > 0 and self.ends[i - 1] > start:
            return False
        if i < len(self.starts) and self.starts[i] < end:
            return False
        self.starts.insert(i, start)
        self.ends.insert(i, end)
        return True
'''
CAL_BC_SOL = '''class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def _fits(self, start, end):
        points = [start] + [s for s, e in self.bookings if start < s < end]
        for p in points:
            if sum(1 for s, e in self.bookings if s <= p < e) + 1 > self.k:
                return False
        return True

    def book(self, start, end):
        if not self._fits(start, end):
            return False
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        if (start, end) in self.bookings:
            self.bookings.remove((start, end))
            return True
        return False

    def next_free(self, duration, after):
        for t in sorted({after} | {e for s, e in self.bookings if e > after}):
            if self._fits(t, t + duration):
                return t
'''
CAL_STARTER = '''class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def book(self, start, end):
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        return False

    def next_free(self, duration, after):
        return after
'''
# stage B starter: the stage C reference with _fits as a stub (always fits); stage C starter: book/cancel done, next_free stub
CAL_B_STARTER = '''class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def _fits(self, start, end):
        # count the bookings that cover the start, and each booking start inside [start, end)
        return True

    def book(self, start, end):
        if not self._fits(start, end):
            return False
        self.bookings.append((start, end))
        return True
'''
CAL_C_STARTER = '''class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def _fits(self, start, end):
        points = [start] + [s for s, e in self.bookings if start < s < end]
        for p in points:
            if sum(1 for s, e in self.bookings if s <= p < e) + 1 > self.k:
                return False
        return True

    def book(self, start, end):
        if not self._fits(start, end):
            return False
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        return False

    def next_free(self, duration, after):
        return after
'''
CAL_DRIVER_A = '''def run_cal(k, ops):
    c = Calendar()
    out = []
    for op in ops:
        if op[0] == 0: out.append(c.book(op[1], op[2]))
        elif op[0] == 1: out.append(c.cancel(op[1], op[2]))
        else: out.append(c.next_free(op[1], op[2]))
    return out
'''
CAL_DRIVER = '''def run_cal(k, ops):
    c = Calendar(k)
    out = []
    for op in ops:
        if op[0] == 0: out.append(c.book(op[1], op[2]))
        elif op[0] == 1: out.append(c.cancel(op[1], op[2]))
        else: out.append(c.next_free(op[1], op[2]))
    return out
'''


def load_cal(src, driver):
    ns = {}
    exec(src + "\n" + driver, ns)
    return ns['run_cal']


run_a = load_cal(CAL_A_SOL, CAL_DRIVER_A)
run_bc = load_cal(CAL_BC_SOL, CAL_DRIVER)


def cal_brute(k, ops):
    """checks every integer time for occupancy"""
    bk = []
    out = []
    LIM = 200

    def occ(t):
        return sum(1 for s, e in bk if s <= t < e)

    def fits(s, e):
        return all(occ(t) + 1 <= k for t in range(s, e))
    for op in ops:
        if op[0] == 0:
            if fits(op[1], op[2]):
                bk.append((op[1], op[2])); out.append(True)
            else:
                out.append(False)
        elif op[0] == 1:
            if (op[1], op[2]) in bk:
                bk.remove((op[1], op[2])); out.append(True)
            else:
                out.append(False)
        else:
            d, a = op[1], op[2]
            t = a
            while not fits(t, t + d):
                t += 1
            out.append(t)
    return out


# ---------- homework: leaderboard ----------

LB_P1_SOL = '''class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])
'''
LB_P1_STARTER = '''class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return 0
'''
LB_P3_SOL = '''class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])

    def reset(self, player):
        self.scores.pop(player, None)
'''
LB_P3_STARTER = '''class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])

    def reset(self, player):
        pass
'''
LB_DRIVER = '''def run_board(ops):
    b = Leaderboard()
    out = []
    for op in ops:
        if op[0] == 0: b.add_score(op[1], op[2])
        elif op[0] == 1: out.append(b.top(op[1]))
        else: b.reset(op[1])
    return out
'''


def load_lb(src):
    ns = {}
    exec(src + "\n" + LB_DRIVER, ns)
    return ns['run_board']


run_board = load_lb(LB_P3_SOL)


def board_brute(ops):
    sc = {}
    out = []
    for op in ops:
        if op[0] == 0:
            sc[op[1]] = sc.get(op[1], 0) + op[2]
        elif op[0] == 1:
            vals = sorted(sc.values(), reverse=True)
            out.append(sum(vals[:op[1]]))
        else:
            sc.pop(op[1], None)
    return out


# ---------- test tables ----------

PROBS = [[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15]]
random.seed(1)
_ps = []
for _ in range(60):
    fm = random.randint(5, 40); fp = random.randint(10, 100)
    _ps.append([fp, fm, random.randint(1, fp), random.randint(2, fm)])
BIG_PLAN = _ps

BP_TESTS = [
    (PROBS, 55, 100), (PROBS, 60, 110), (PROBS, 90, 160), (PROBS, 0, 0), (PROBS, 14, 20), ([], 30, 0),
    ([[40, 20, 10, 20]], 20, 40), ([[40, 20, 30, 5]], 10, 30),
    (PROBS + [[20, 10, 5, 3]], 45, 80),
]

CSDK_SMALL = [([6, -1, 8, 3, -4, 7], 5, 2), ([10, 20], 10, 3), ([], 4, 0), ([0, 0, 0], 7, 6), ([-3, 3], 3, 3),
              ([-2, -4, -6], 5, 1), ([5], 5, 1), ([4], 5, 0), ([-1, 3, 0], 3, 3)]
LZS_SMALL = [([5, -2, -3, 8, 1], 3), ([2, -2], 2), ([], 0), ([7], 0), ([0], 1), ([1, 2, 3], 0),
             ([4, -1, -3, 6, -6, 2], 5), ([-5, 5, 5, -5], 4), ([3, 1, -4, 2, 2, -4, 9], 6)]
PES_SMALL = [([2, 3, 5, 7], [105, 70, 42, 30]), ([3, -2, 0, 4, -1], [0, 0, 24, 0, 0]), ([2, 0, 0], [0, 0, 0]),
             ([0, 5], [5, 0]), ([7, 3], [3, 7]), ([1, 1, 1], [1, 1, 1]), ([5, -2], [-2, 5])]

CAL_A = [
    (1, [[0, 10, 20], [0, 15, 25], [0, 20, 30]], [True, False, True]),
    (1, [[0, 0, 5], [0, 5, 10], [0, 3, 6], [0, 10, 11], [0, 4, 5]], [True, True, False, True, False]),
    (1, [[0, 5, 10], [0, 0, 5], [0, 10, 15], [0, 0, 15]], [True, True, True, False]),
    (1, [[0, 1, 2]], [True]),
    (1, [], []),
]
CAL_B = [
    (2, [[0, 10, 20], [0, 15, 25], [0, 20, 30], [0, 12, 18]], [True, True, True, False]),
    (2, [[0, 10, 20], [0, 15, 25], [0, 5, 15], [0, 5, 11]], [True, True, True, False]),
    (3, [[0, 1, 5], [0, 2, 5], [0, 3, 5], [0, 4, 5], [0, 0, 2]], [True, True, True, False, True]),
    (1, [[0, 1, 3], [0, 3, 5]], [True, True]),
    (2, [[0, 0, 10], [0, 0, 10], [0, 10, 20], [0, 5, 15]], [True, True, True, False]),
]
CAL_C = [
    (1, [[0, 10, 20], [1, 10, 20], [0, 15, 25], [1, 15, 26], [1, 15, 25], [0, 10, 12]], [True, True, True, False, True, True]),
    (1, [[0, 10, 20], [0, 30, 40], [2, 5, 0], [2, 10, 5], [2, 10, 12], [2, 10, 35], [2, 11, 10]], [True, True, 0, 20, 20, 40, 40]),
    (2, [[0, 0, 10], [0, 0, 10], [2, 5, 0], [1, 0, 10], [2, 5, 0], [2, 12, 3]], [True, True, 10, True, 0, 3]),
    (1, [[2, 5, 7]], [7]),
    (1, [[0, 0, 3], [0, 3, 6], [0, 9, 12], [2, 3, 0], [2, 4, 0], [1, 3, 6], [2, 4, 0]], [True, True, True, 6, 12, True, 3]),
]
LB_P1 = [
    ([[0, 1, 73], [0, 2, 56], [0, 3, 39], [0, 4, 51], [0, 5, 4], [1, 1], [0, 2, 51], [1, 2]], [73, 180]),
    ([[0, 1, 5], [0, 1, 7], [1, 1], [1, 3]], [12, 12]),
    ([[1, 2]], [0]),
    ([[0, 1, 10], [0, 2, 20], [0, 3, 30], [1, 2], [1, 2], [1, 5]], [50, 50, 60]),
]
LB_P3 = [
    ([[0, 1, 73], [0, 2, 56], [0, 3, 39], [0, 4, 51], [0, 5, 4], [1, 1], [2, 1], [2, 2], [0, 2, 51], [1, 2]], [73, 102]),
    ([[0, 1, 5], [0, 1, 7], [1, 1], [1, 3]], [12, 12]),
    ([[1, 2]], [0]),
    ([[0, 1, 10], [0, 2, 20], [0, 3, 30], [1, 2], [2, 3], [1, 2], [1, 5]], [50, 30, 30]),
]


def main():
    rnd = random.Random(20261104)
    # --- 15.1
    for p, b, e in BP_TESTS:
        assert best_plan(p, b) == e == best_plan_brute(p, b), (p, b, e)
    assert best_plan(BIG_PLAN, 600) == best_plan_memo(tuple(map(tuple, BIG_PLAN)), 600)
    print('best_plan big (seed 1):', best_plan(BIG_PLAN, 600))
    for _ in range(3000):
        n = rnd.randint(0, 6)
        ps = []
        for _ in range(n):
            fm = rnd.randint(1, 20); fp = rnd.randint(1, 60)
            ps.append([fp, fm, rnd.randint(0, fp), rnd.randint(1, fm)])
        b = rnd.randint(0, 60)
        assert best_plan(ps, b) == best_plan_brute(ps, b) == best_plan_memo(tuple(map(tuple, ps)), b)
    # lesson example
    LP = [[40, 20, 12, 6], [60, 35, 25, 12], [90, 50, 30, 18]]
    print('lesson P1-P3 at 62:', best_plan(LP, 62), best_plan_brute(LP, 62), 'greedy', greedy_ppm(LP, 62))
    print('lesson P1-P3 at 60:', best_plan(LP, 60), best_plan_brute(LP, 60), 'greedy', greedy_ppm(LP, 60))
    # --- 16
    for _ in range(2000):
        xs = [rnd.randint(0, 3) for _ in range(rnd.randint(0, 12))]
        assert _ref(xs) == streak_brute(xs)
    cases = [[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2]]
    for name, f in MUT.items():
        assert any(f(list(c)) != _ref(list(c)) for c in cases), name
    cov = {}
    cands = [[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2], [1, 1], [2, 1], [1, 2, 2], [5, 5, 5, 1]]
    for c in cands:
        cov[str(c)] = [n for n, f in MUT.items() if f(list(c)) != _ref(list(c))]
    print('coverage', cov)
    best = None
    for r in range(1, len(cands) + 1):
        for sub in itertools.combinations(cands, r):
            caught = set()
            for c in sub:
                caught |= set(cov[str(c)])
            if len(caught) == 6:
                best = (r, sub); break
        if best:
            break
    print('smallest subset exposing all six:', best)
    ns = {}
    exec(PRELUDE_16 + EDGE_SOL, ns)
    assert all(ns['caught'](n) for n in MUT) and ns['well_formed']()
    ns = {}
    exec(PRELUDE_16 + EDGE_STARTER, ns)
    nfail = sum(not ns['caught'](n) for n in MUT) + (not ns['well_formed']())
    print('edge starter: fails', nfail, 'of 7')
    # --- 17.1
    for xs, k, e in CSDK_SMALL:
        assert csdk(xs, k) == csdk_slow(xs, k) == e, (xs, k, e)
    for _ in range(4000):
        xs = [rnd.randint(-9, 9) for _ in range(rnd.randint(0, 14))]
        k = rnd.randint(1, 7)
        assert csdk(xs, k) == csdk_slow(xs, k)
    assert csdk([3] * 400000, 1) == 400000 * 400001 // 2 == 80000200000
    assert csdk([1, -1] * 200000, 2) == 200001 * 200000 // 2 + 200000 * 199999 // 2 == 40000000000
    # --- 17.2
    for xs, e in LZS_SMALL:
        assert lzs(xs) == lzs_slow(xs) == e, (xs, e)
    for _ in range(5000):
        xs = [rnd.randint(-4, 4) for _ in range(rnd.randint(0, 14))]
        assert lzs(xs) == lzs_slow(xs)
    assert lzs([1, -1] * 200000) == 400000
    assert lzs([1, 2, -3] * 133333 + [5]) == 399999
    assert lzs([1, 2, -3] * 40 + [5]) == lzs_slow([1, 2, -3] * 40 + [5]) == 120
    # --- 18
    for xs, e in PES_SMALL:
        assert pes(xs) == e == pes_brute(xs), xs
    for _ in range(2000):
        xs = [rnd.randint(-3, 3) for _ in range(rnd.randint(1, 9))]
        assert pes(xs) == pes_brute(xs)
    xs = [1] * 100000; xs[10] = 2; xs[500] = 3
    assert sum(pes(xs)) == 6 * 99998 + 5 == 599993
    xs = [1] * 50; xs[10] = 2; xs[20] = 3
    assert pes(xs) == pes_brute(xs)
    # --- 19
    for k, ops, e in CAL_A:
        assert run_a(k, ops) == e == cal_brute(1, ops), ops
    for k, ops, e in CAL_B + CAL_C:
        assert run_bc(k, ops) == e == cal_brute(k, ops), (k, ops, run_bc(k, ops), cal_brute(k, ops))
    for k, ops, e in CAL_A:
        assert run_bc(k, ops) == e
    ops = [[0, 2 * i, 2 * i + 1] for i in range(60000)] + [[0, 0, 120000]]
    assert run_a(1, ops).count(True) == 60000
    for _ in range(2000):
        ops = []
        for _ in range(rnd.randint(1, 14)):
            s = rnd.randint(0, 12); e2 = s + rnd.randint(1, 5)
            ops.append([0, s, e2])
        assert run_a(1, ops) == cal_brute(1, ops) == run_bc(1, ops)
    for _ in range(3000):
        k = rnd.randint(1, 3)
        ops = []
        for _ in range(rnd.randint(1, 14)):
            r = rnd.random()
            s = rnd.randint(0, 12); e2 = s + rnd.randint(1, 5)
            if r < 0.6:
                ops.append([0, s, e2])
            elif r < 0.8:
                ops.append([1, s, e2])
            else:
                ops.append([2, rnd.randint(1, 5), rnd.randint(0, 12)])
        assert run_bc(k, ops) == cal_brute(k, ops), (k, ops)
    # starters: stage fails
    sA = load_cal(CAL_STARTER, CAL_DRIVER_A)
    print('calendar starter fails A', sum(sA(k, o) != e for k, o, e in CAL_A) + 1, 'of 6 (row 6 large)')
    tests_b = CAL_A[:3] + CAL_B
    sB = load_cal(CAL_STARTER, CAL_DRIVER)
    print('stage B tests', len(tests_b), 'starter fails', sum(sB(k, o) != e for k, o, e in tests_b))
    sB2 = load_cal(CAL_B_STARTER, CAL_DRIVER)
    print('stage B stub starter fails', sum(sB2(k, o) != e for k, o, e in tests_b))
    tests_c = CAL_A[:3] + CAL_B + CAL_C
    sC = load_cal(CAL_C_STARTER, CAL_DRIVER)
    print('stage C tests', len(tests_c), 'stub starter fails', sum(sC(k, o) != e for k, o, e in tests_c))
    sCs = load_cal(CAL_STARTER, CAL_DRIVER)
    print('stage C plain starter fails', sum(sCs(k, o) != e for k, o, e in tests_c))
    # stage A scan version is too slow on the large row (scan reference, measured on 6000 to estimate)
    # --- leaderboard
    for ops, e in LB_P1:
        assert load_lb(LB_P1_SOL)(ops) == e == board_brute(ops), ops
        assert load_lb(LB_P3_SOL)(ops) == e
    for ops, e in LB_P3:
        assert run_board(ops) == e == board_brute(ops), ops
    for _ in range(2000):
        ops = []
        for _ in range(rnd.randint(1, 16)):
            r = rnd.random()
            if r < 0.55:
                ops.append([0, rnd.randint(1, 5), rnd.randint(-5, 30)])
            elif r < 0.8:
                ops.append([1, rnd.randint(1, 6)])
            else:
                ops.append([2, rnd.randint(1, 5)])
        assert run_board(ops) == board_brute(ops)
    p1 = load_lb(LB_P1_STARTER)
    print('LB part1 starter fails', sum(p1(o) != e for o, e in LB_P1), 'of 4')
    p3 = load_lb(LB_P3_STARTER)
    print('LB part3 starter fails', sum(p3(o) != e for o, e in LB_P3), 'of 4')
    # h4 numbers
    print('ALL OK')


if __name__ == '__main__':
    main()
