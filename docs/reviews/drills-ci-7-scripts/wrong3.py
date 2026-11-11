"""RIGHT solutions written top down (the recursion the constraint line rules out,
with answers remembered), to see whether the drill page accepts them. Each is
at the target order of growth; what varies is how deep the recursion goes and
whether the memo is functools.lru_cache or a dict.
Run natively: harness.py wrong3.py app/content/drills (all pass).
Run in Chromium: pyodide_probe.py <copy> <labels>, then planted-check on the copy:
a label NOT reported as "passes all" is a right solution the page marks wrong."""
CANDIDATES = {}


def add(label, did, comment, src):
    CANDIDATES[label] = (did, src, comment)


add('merge_memo_dict', 'ci-merged-tape', 'top down with a dict, 600 frames deep', '''
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    if len(a) + len(b) != len(tape):
        return 0
    memo = {}
    def ways(i, j):
        if i == len(a) and j == len(b):
            return 1
        if (i, j) in memo:
            return memo[(i, j)]
        total = 0
        if i < len(a) and a[i] == tape[i + j]:
            total += ways(i + 1, j)
        if j < len(b) and b[j] == tape[i + j]:
            total += ways(i, j + 1)
        memo[(i, j)] = total % MOD
        return memo[(i, j)]
    return ways(0, 0)
''')
add('merge_memo_lru_limit_raised', 'ci-merged-tape', 'top down with lru_cache and sys.setrecursionlimit(10000)', '''
import sys
from functools import lru_cache
sys.setrecursionlimit(10000)
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    if len(a) + len(b) != len(tape):
        return 0
    @lru_cache(maxsize=None)
    def ways(i, j):
        if i == len(a) and j == len(b):
            return 1
        total = 0
        if i < len(a) and a[i] == tape[i + j]:
            total += ways(i + 1, j)
        if j < len(b) and b[j] == tape[i + j]:
            total += ways(i, j + 1)
        return total % MOD
    return ways(0, 0)
''')
add('pieces_memo_dict', 'ci-mirror-pieces', 'top down with a dict and plain loops, 400 frames deep', '''
def solve_mirror_pieces(text):
    tok = text.split()
    out = []
    for s in tok[1:1 + int(tok[0])]:
        n = len(s)
        memo = {}
        def fewest(i):
            if i == n:
                return 0
            if i in memo:
                return memo[i]
            best = n
            for j in range(i + 1, n + 1):
                if s[i:j] == s[i:j][::-1]:
                    r = 1 + fewest(j)
                    if r < best:
                        best = r
            memo[i] = best
            return best
        out.append(str(fewest(0)))
    return '\\n'.join(out)
''')
add('pieces_memo_lru_loop', 'ci-mirror-pieces', 'top down with lru_cache and a plain loop (no generator), 400 frames deep', '''
from functools import lru_cache
def solve_mirror_pieces(text):
    tok = text.split()
    out = []
    for s in tok[1:1 + int(tok[0])]:
        n = len(s)
        @lru_cache(maxsize=None)
        def fewest(i):
            if i == n:
                return 0
            best = n
            for j in range(i + 1, n + 1):
                if s[i:j] == s[i:j][::-1]:
                    best = min(best, 1 + fewest(j))
            return best
        out.append(str(fewest(0)))
    return '\\n'.join(out)
''')
add('edits_memo_deep', 'ci-priced-edits', 'top down with lru_cache, delete tried first: 600 frames deep on two codes of 300', '''
from functools import lru_cache
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        @lru_cache(maxsize=None)
        def go(i, j):
            if i == len(s):
                return (len(t) - j) * ins
            if j == len(t):
                return (len(s) - i) * dele
            return min(go(i + 1, j) + dele, go(i, j + 1) + ins, go(i + 1, j + 1) + (0 if s[i] == t[j] else sub))
        out.append(str(go(0, 0)))
    return '\\n'.join(out)
''')
add('edits_memo_dict_deep', 'ci-priced-edits', 'the same with a dict', '''
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        memo = {}
        def go(i, j):
            if i == len(s):
                return (len(t) - j) * ins
            if j == len(t):
                return (len(s) - i) * dele
            if (i, j) not in memo:
                memo[(i, j)] = min(go(i + 1, j) + dele, go(i, j + 1) + ins, go(i + 1, j + 1) + (0 if s[i] == t[j] else sub))
            return memo[(i, j)]
        out.append(str(go(0, 0)))
    return '\\n'.join(out)
''')
add('tol_memo_lru', 'ci-tolerant-common', 'top down with lru_cache, up to 600 frames deep on two feeds of 300', '''
from functools import lru_cache
def tolerant_common(a, b, tol):
    @lru_cache(maxsize=None)
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        if abs(a[i] - b[j]) <= tol:
            return 1 + go(i + 1, j + 1)
        return max(go(i + 1, j), go(i, j + 1))
    return go(0, 0)
''')
add('tol_memo_dict', 'ci-tolerant-common', 'the same with a dict', '''
def tolerant_common(a, b, tol):
    memo = {}
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        if (i, j) not in memo:
            if abs(a[i] - b[j]) <= tol:
                memo[(i, j)] = 1 + go(i + 1, j + 1)
            else:
                memo[(i, j)] = max(go(i + 1, j), go(i, j + 1))
        return memo[(i, j)]
    return go(0, 0)
''')
add('drop_memo_dict', 'ci-drop-point-routes', 'top down with a dict, 400 frames deep on the 200 by 200 floor', '''
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    R, C = len(grid), len(grid[0])
    memo = {}
    def go(r, c, seen):
        if r >= R or c >= C or grid[r][c] == '#':
            return 0
        seen = seen or grid[r][c] == 'P'
        if r == R - 1 and c == C - 1:
            return 1 if seen else 0
        key = (r, c, seen)
        if key not in memo:
            memo[key] = (go(r + 1, c, seen) + go(r, c + 1, seen)) % MOD
        return memo[key]
    return go(0, 0, False)
''')
add('three_memo_dict', 'ci-three-feed-common', 'top down with a dict, 150 frames deep', '''
def three_feed_common(a, b, c):
    memo = {}
    def best(i, j, k):
        if i == len(a) or j == len(b) or k == len(c):
            return 0
        key = (i, j, k)
        if key not in memo:
            if a[i] == b[j] == c[k]:
                memo[key] = 1 + best(i + 1, j + 1, k + 1)
            else:
                memo[key] = max(best(i + 1, j, k), best(i, j + 1, k), best(i, j, k + 1))
        return memo[key]
    return best(0, 0, 0)
''')
add('hold_memo_lru', 'ci-hold-limit', 'top down with lru_cache on (crate, room, crates left), 50 frames deep', '''
from functools import lru_cache
def hold_value(weights, values, cap, k):
    n = len(weights)
    @lru_cache(maxsize=None)
    def go(i, room, left):
        if i == n or left == 0:
            return 0
        best = go(i + 1, room, left)
        if weights[i] <= room:
            best = max(best, values[i] + go(i + 1, room - weights[i], left - 1))
        return best
    return go(0, cap, k)
''')
