"""Wrong or too-slow candidates, second file (drills 7 to 15 of the pack).
Run: harness.py wrong2.py app/content/drills --limit 15. Same shape as wrong.py."""
CANDIDATES = {}


def add(label, did, comment, src):
    CANDIDATES[label] = (did, src, comment)


# ------------------------------------------------------------ ci-pillar-queens
add('queens_pillars_block', 'ci-pillar-queens', 'a pillar blocks the view (the brief says it never does)', '''
def queen_count(board, q):
    n = len(board)
    free = [(r, c) for r in range(n) for c in range(n) if board[r][c] == '.']
    def sees(p, s):
        (r, c), (a, b) = p, s
        if not (r == a or c == b or abs(r - a) == abs(c - b)):
            return False
        dr = (a > r) - (a < r)
        dc = (b > c) - (b < c)
        r, c = r + dr, c + dc
        while (r, c) != (a, b):
            if board[r][c] == '#':
                return False
            r, c = r + dr, c + dc
        return True
    def walk(start, placed):
        if len(placed) == q:
            return 1
        total = 0
        for i in range(start, len(free)):
            if all(not sees(free[i], p) for p in placed):
                total += walk(i + 1, placed + [free[i]])
        return total
    return walk(0, [])
''')
add('queens_on_pillars', 'ci-pillar-queens', 'pillars ignored', '''
def queen_count(board, q):
    n = len(board)
    def walk(row, left, cols, ups, downs):
        if left == 0:
            return 1
        if n - row < left:
            return 0
        total = walk(row + 1, left, cols, ups, downs)
        for c in range(n):
            if c not in cols and row + c not in ups and row - c not in downs:
                total += walk(row + 1, left - 1, cols | {c}, ups | {row + c}, downs | {row - c})
        return total
    return walk(0, q, frozenset(), frozenset(), frozenset())
''')
add('queens_at_most', 'ci-pillar-queens', 'counts placements of at most q guards', '''
def queen_count(board, q):
    n = len(board)
    def walk(row, left, cols, ups, downs):
        if row == n or left == 0:
            return 1
        total = walk(row + 1, left, cols, ups, downs)
        for c in range(n):
            if board[row][c] == '.' and c not in cols and row + c not in ups and row - c not in downs:
                total += walk(row + 1, left - 1, cols | {c}, ups | {row + c}, downs | {row - c})
        return total
    return walk(0, q, frozenset(), frozenset(), frozenset())
''')
add('queens_prune_off_by_one', 'ci-pillar-queens', 'the rows-left prune uses <=', '''
def queen_count(board, q):
    n = len(board)
    def walk(row, left, cols, ups, downs):
        if left == 0:
            return 1
        if n - row <= left:
            return 0
        total = walk(row + 1, left, cols, ups, downs)
        for c in range(n):
            if board[row][c] == '.' and c not in cols and row + c not in ups and row - c not in downs:
                total += walk(row + 1, left - 1, cols | {c}, ups | {row + c}, downs | {row - c})
        return total
    return walk(0, q, frozenset(), frozenset(), frozenset())
''')
add('queens_zero_is_zero', 'ci-pillar-queens', 'q = 0 answered 0', '''
def queen_count(board, q):
    n = len(board)
    if q == 0:
        return 0
    def walk(row, left, cols, ups, downs):
        if left == 0:
            return 1
        if n - row < left:
            return 0
        total = walk(row + 1, left, cols, ups, downs)
        for c in range(n):
            if board[row][c] == '.' and c not in cols and row + c not in ups and row - c not in downs:
                total += walk(row + 1, left - 1, cols | {c}, ups | {row + c}, downs | {row - c})
        return total
    return walk(0, q, frozenset(), frozenset(), frozenset())
''')
add('queens_rows_cols_swapped', 'ci-pillar-queens', 'board read as board[c][row] (the transpose)', '''
def queen_count(board, q):
    n = len(board)
    def walk(row, left, cols, ups, downs):
        if left == 0:
            return 1
        if n - row < left:
            return 0
        total = walk(row + 1, left, cols, ups, downs)
        for c in range(n):
            if board[c][row] == '.' and c not in cols and row + c not in ups and row - c not in downs:
                total += walk(row + 1, left - 1, cols | {c}, ups | {row + c}, downs | {row - c})
        return total
    return walk(0, q, frozenset(), frozenset(), frozenset())
''')
add('queens_all_squares_slow', 'ci-pillar-queens', 'every set of q free squares tested pair by pair (the search the constraint line steers away from)', '''
from itertools import combinations
def queen_count(board, q):
    n = len(board)
    free = [(r, c) for r in range(n) for c in range(n) if board[r][c] == '.']
    return sum(1 for pick in combinations(free, q)
               if all(a != c and b != e and abs(a - c) != abs(b - e) for (a, b), (c, e) in combinations(pick, 2)))
''')

# ------------------------------------------------------------ ci-invoice-matches
add('invoice_skip_i_gt_0', 'ci-invoice-matches', 'repeat skipped with i > 0, so two equal invoices are never used together', '''
def invoice_matches(amounts, target, k):
    vals = sorted(amounts)
    out, pick = [], []
    def walk(start, left):
        if left == 0:
            out.append(pick[:])
            return
        if len(pick) == k:
            return
        for i in range(start, len(vals)):
            if vals[i] > left:
                break
            if i > 0 and vals[i] == vals[i - 1]:
                continue
            pick.append(vals[i])
            walk(i + 1, left - vals[i])
            pick.pop()
    walk(0, target)
    return out
''')
add('invoice_k_before_total', 'ci-invoice-matches', 'the k check comes before the total check, so a way of exactly k is lost', '''
def invoice_matches(amounts, target, k):
    vals = sorted(amounts)
    out, pick = [], []
    def walk(start, left):
        if len(pick) == k:
            return
        if left == 0:
            out.append(pick[:])
            return
        for i in range(start, len(vals)):
            if vals[i] > left:
                break
            if i > start and vals[i] == vals[i - 1]:
                continue
            pick.append(vals[i])
            walk(i + 1, left - vals[i])
            pick.pop()
    walk(0, target)
    return out
''')
add('invoice_k_plus_one', 'ci-invoice-matches', 'allows k + 1 invoices', '''
def invoice_matches(amounts, target, k):
    vals = sorted(amounts)
    out, pick = [], []
    def walk(start, left):
        if left == 0:
            out.append(pick[:])
            return
        if len(pick) > k:
            return
        for i in range(start, len(vals)):
            if vals[i] > left:
                break
            if i > start and vals[i] == vals[i - 1]:
                continue
            pick.append(vals[i])
            walk(i + 1, left - vals[i])
            pick.pop()
    walk(0, target)
    return out
''')
add('invoice_unsorted_dedupe', 'ci-invoice-matches', 'duplicates removed with a set of sorted tuples, list left in set order', '''
from itertools import combinations
def invoice_matches(amounts, target, k):
    seen = set()
    for r in range(1, min(k, len(amounts)) + 1):
        for c in combinations(amounts, r):
            if sum(c) == target:
                seen.add(tuple(sorted(c)))
    return [list(t) for t in seen]
''')
add('invoice_sorted_by_len', 'ci-invoice-matches', 'ways sorted by number of invoices first', '''
def invoice_matches(amounts, target, k):
    vals = sorted(amounts)
    out, pick = [], []
    def walk(start, left):
        if left == 0:
            out.append(pick[:])
            return
        if len(pick) == k:
            return
        for i in range(start, len(vals)):
            if vals[i] > left:
                break
            if i > start and vals[i] == vals[i - 1]:
                continue
            pick.append(vals[i])
            walk(i + 1, left - vals[i])
            pick.pop()
    walk(0, target)
    return sorted(out, key=lambda w: (len(w), w))
''')
add('invoice_combos_set_OK_slow', 'ci-invoice-matches', 'every combination of up to k invoices, a set to drop repeats, sorted: right, about a million sums', '''
from itertools import combinations
def invoice_matches(amounts, target, k):
    seen = set()
    vals = sorted(amounts)
    for r in range(1, min(k, len(vals)) + 1):
        for c in combinations(vals, r):
            if sum(c) == target:
                seen.add(c)
    return sorted(list(t) for t in seen)
''')
add('invoice_no_copy', 'ci-invoice-matches', 'the pick stored without a copy, then popped', '''
def invoice_matches(amounts, target, k):
    vals = sorted(amounts)
    out, pick = [], []
    def walk(start, left):
        if left == 0:
            out.append(pick)
            return
        if len(pick) == k:
            return
        for i in range(start, len(vals)):
            if vals[i] > left:
                break
            if i > start and vals[i] == vals[i - 1]:
                continue
            pick.append(vals[i])
            walk(i + 1, left - vals[i])
            pick.pop()
    walk(0, target)
    return out
''')
add('invoice_distinct_amounts_counted', 'ci-invoice-matches', 'k counts distinct amounts used, not invoices', '''
from collections import Counter
def invoice_matches(amounts, target, k):
    cnt = sorted(Counter(amounts).items())
    out = []
    def go(i, left, room, cur):
        if left == 0:
            out.append(cur)
            return
        if i == len(cnt) or room == 0:
            return
        a, c = cnt[i]
        if a > left:
            return
        for use in range(0, min(c, left // a) + 1):
            go(i + 1, left - use * a, room - (1 if use else 0), cur + [a] * use)
    go(0, target, k, [])
    return sorted(out)
''')

# ------------------------------------------------------------ ci-trace-count
add('trace_final_sum_no_mod', 'ci-trace-count', 'counts reduced per square, the final sum not', '''
MOD = 10 ** 9 + 7
def trace_count(board, word):
    R, C = len(board), len(board[0])
    cur = [[1 if board[r][c] == word[0] else 0 for c in range(C)] for r in range(R)]
    for ch in word[1:]:
        nxt = [[0] * C for _ in range(R)]
        for r in range(R):
            for c in range(C):
                if board[r][c] == ch:
                    s = 0
                    for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= a < R and 0 <= b < C:
                            s += cur[a][b]
                    nxt[r][c] = s % MOD
        cur = nxt
    return sum(map(sum, cur))
''')
add('trace_no_immediate_return', 'ci-trace-count', 'a trace may not step straight back to the square it came from', '''
MOD = 10 ** 9 + 7
def trace_count(board, word):
    R, C = len(board), len(board[0])
    ways = {}
    for r in range(R):
        for c in range(C):
            if board[r][c] == word[0]:
                ways[(r, c, -1, -1)] = 1
    for ch in word[1:]:
        nxt = {}
        for (r, c, pr, pc), w in ways.items():
            for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= a < R and 0 <= b < C and board[a][b] == ch and (a, b) != (pr, pc):
                    key = (a, b, r, c)
                    nxt[key] = (nxt.get(key, 0) + w) % MOD
        ways = nxt
    return sum(ways.values()) % MOD
''')
add('trace_stay_allowed', 'ci-trace-count', 'a step may stay on the same square', '''
MOD = 10 ** 9 + 7
def trace_count(board, word):
    R, C = len(board), len(board[0])
    cur = [[1 if board[r][c] == word[0] else 0 for c in range(C)] for r in range(R)]
    for ch in word[1:]:
        nxt = [[0] * C for _ in range(R)]
        for r in range(R):
            for c in range(C):
                if board[r][c] == ch:
                    s = cur[r][c]
                    for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= a < R and 0 <= b < C:
                            s += cur[a][b]
                    nxt[r][c] = s % MOD
        cur = nxt
    return sum(map(sum, cur)) % MOD
''')
add('trace_wraps_negative_index', 'ci-trace-count', 'no lower bound check: index -1 wraps to the far edge', '''
MOD = 10 ** 9 + 7
def trace_count(board, word):
    R, C = len(board), len(board[0])
    cur = [[1 if board[r][c] == word[0] else 0 for c in range(C)] for r in range(R)]
    for ch in word[1:]:
        nxt = [[0] * C for _ in range(R)]
        for r in range(R):
            for c in range(C):
                if board[r][c] == ch:
                    s = cur[r - 1][c] + cur[r][c - 1]
                    if r + 1 < R:
                        s += cur[r + 1][c]
                    if c + 1 < C:
                        s += cur[r][c + 1]
                    nxt[r][c] = s % MOD
        cur = nxt
    return sum(map(sum, cur)) % MOD
''')
add('trace_distinct_ends', 'ci-trace-count', 'a set of squares per letter: counts where traces can end, not traces', '''
def trace_count(board, word):
    R, C = len(board), len(board[0])
    cur = {(r, c) for r in range(R) for c in range(C) if board[r][c] == word[0]}
    for ch in word[1:]:
        cur = {(a, b) for r, c in cur for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
               if 0 <= a < R and 0 <= b < C and board[a][b] == ch}
    return len(cur)
''')
add('trace_in_place', 'ci-trace-count', 'one table updated in place, so a letter reads counts already moved on', '''
MOD = 10 ** 9 + 7
def trace_count(board, word):
    R, C = len(board), len(board[0])
    cur = [[1 if board[r][c] == word[0] else 0 for c in range(C)] for r in range(R)]
    for ch in word[1:]:
        for r in range(R):
            for c in range(C):
                s = 0
                if board[r][c] == ch:
                    for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= a < R and 0 <= b < C:
                            s += cur[a][b]
                cur[r][c] = s % MOD
    return sum(map(sum, cur)) % MOD
''')
add('trace_memo_recursion_OK', 'ci-trace-count', 'the one-by-one walk with lru_cache on (square, letter): right, 60 frames deep', '''
from functools import lru_cache
MOD = 10 ** 9 + 7
def trace_count(board, word):
    R, C = len(board), len(board[0])
    @lru_cache(maxsize=None)
    def walk(i, j, k):
        if k == len(word) - 1:
            return 1
        t = 0
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < R and 0 <= b < C and board[a][b] == word[k + 1]:
                t += walk(a, b, k + 1)
        return t % MOD
    return sum(walk(i, j, 0) for i in range(R) for j in range(C) if board[i][j] == word[0]) % MOD
''')

# ------------------------------------------------------------ ci-mirror-pieces
add('pieces_greedy_both_ends', 'ci-mirror-pieces', 'the longest-start greedy and the longest-end greedy, the smaller taken', '''
def solve_mirror_pieces(text):
    tok = text.split()
    def g(s):
        pieces, i = 0, 0
        while i < len(s):
            j = len(s)
            while s[i:j] != s[i:j][::-1]:
                j -= 1
            pieces += 1
            i = j
        return pieces
    return '\\n'.join(str(min(g(s), g(s[::-1]))) for s in tok[1:1 + int(tok[0])])
''')
add('pieces_branch_and_bound', 'ci-mirror-pieces', 'the ruled-out search, longest piece first, cut off when it cannot beat the best found', '''
import sys
def solve_mirror_pieces(text):
    sys.setrecursionlimit(5000)
    tok = text.split()
    out = []
    for s in tok[1:1 + int(tok[0])]:
        n = len(s)
        best = [n]
        def go(i, used):
            if i == n:
                best[0] = used
                return
            if used + 1 >= best[0]:
                return
            for j in range(n, i, -1):
                if s[i:j] == s[i:j][::-1]:
                    go(j, used + 1)
                    if used + 1 >= best[0]:
                        return
        go(0, 0)
        out.append(str(best[0]))
    return '\\n'.join(out)
''')
add('pieces_odd_only', 'ci-mirror-pieces', 'pieces grown from letters only, never from a gap', '''
def solve_mirror_pieces(text):
    tok = text.split()
    out = []
    for s in tok[1:1 + int(tok[0])]:
        n = len(s)
        best = [0] + [n] * n
        for c in range(n):
            lo = hi = c
            while lo >= 0 and hi < n and s[lo] == s[hi]:
                best[hi + 1] = min(best[hi + 1], best[lo] + 1)
                lo -= 1
                hi += 1
        out.append(str(best[n]))
    return '\\n'.join(out)
''')
add('pieces_centres_evens_after', 'ci-mirror-pieces', 'all letter centres first, then all gap centres: best[lo] read before it is final', '''
def solve_mirror_pieces(text):
    tok = text.split()
    out = []
    for s in tok[1:1 + int(tok[0])]:
        n = len(s)
        best = [0] + [n] * n
        for lo0, hi0 in [(c, c) for c in range(n)] + [(c, c + 1) for c in range(n - 1)]:
            lo, hi = lo0, hi0
            while lo >= 0 and hi < n and s[lo] == s[hi]:
                best[hi + 1] = min(best[hi + 1], best[lo] + 1)
                lo -= 1
                hi += 1
        out.append(str(best[n]))
    return '\\n'.join(out)
''')
add('pieces_ignores_q_OK', 'ci-mirror-pieces', 'every later token treated as a tape, q ignored: right on any valid input', '''
def solve_mirror_pieces(text):
    tok = text.split()
    out = []
    for s in tok[1:]:
        n = len(s)
        best = [0] + [n] * n
        for c in range(2 * n - 1):
            lo, hi = c // 2, (c + 1) // 2
            while lo >= 0 and hi < n and s[lo] == s[hi]:
                best[hi + 1] = min(best[hi + 1], best[lo] + 1)
                lo -= 1
                hi += 1
        out.append(str(best[n]))
    return '\\n'.join(out)
''')
add('pieces_memo_recursion', 'ci-mirror-pieces', 'the ruled-out recursion with lru_cache on the start: right method, 400 frames deep at the default limit', '''
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
            return min(1 + fewest(j) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1])
        out.append(str(fewest(0)))
    return '\\n'.join(out)
''')

# ------------------------------------------------------------ ci-three-feed-common
add('three_best_of_three_orders', 'ci-three-feed-common', 'one LCS of each pair matched with the third string, the best of the three orders', '''
def three_feed_common(a, b, c):
    def common(s, t):
        best = [[''] * (len(t) + 1) for _ in range(len(s) + 1)]
        for i in range(1, len(s) + 1):
            for j in range(1, len(t) + 1):
                if s[i - 1] == t[j - 1]:
                    best[i][j] = best[i - 1][j - 1] + s[i - 1]
                else:
                    best[i][j] = max(best[i - 1][j], best[i][j - 1], key=len)
        return best[len(s)][len(t)]
    return max(len(common(common(a, b), c)), len(common(common(b, c), a)), len(common(common(a, c), b)))
''')
add('three_contiguous', 'ci-three-feed-common', 'longest common run of neighbours', '''
def three_feed_common(a, b, c):
    best = 0
    for i in range(len(a)):
        for j in range(i + 1, len(a) + 1):
            if j - i > best and a[i:j] in b and a[i:j] in c:
                best = j - i
    return best
''')
add('three_ab_match_moves', 'ci-three-feed-common', 'when a and b agree but c does not, only c is stepped back', '''
def three_feed_common(a, b, c):
    na, nb, nc = len(a), len(b), len(c)
    d = [[[0] * (nc + 1) for _ in range(nb + 1)] for _ in range(na + 1)]
    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            for k in range(1, nc + 1):
                if a[i-1] == b[j-1] == c[k-1]:
                    d[i][j][k] = d[i-1][j-1][k-1] + 1
                elif a[i-1] == b[j-1]:
                    d[i][j][k] = d[i][j][k-1]
                else:
                    d[i][j][k] = max(d[i-1][j][k], d[i][j-1][k], d[i][j][k-1])
    return d[na][nb][nc]
''')
add('three_two_moves_only', 'ci-three-feed-common', 'on a mismatch only two of the three ends are stepped back', '''
def three_feed_common(a, b, c):
    na, nb, nc = len(a), len(b), len(c)
    d = [[[0] * (nc + 1) for _ in range(nb + 1)] for _ in range(na + 1)]
    for i in range(1, na + 1):
        for j in range(1, nb + 1):
            for k in range(1, nc + 1):
                if a[i-1] == b[j-1] == c[k-1]:
                    d[i][j][k] = d[i-1][j-1][k-1] + 1
                else:
                    d[i][j][k] = max(d[i-1][j][k], d[i][j-1][k])
    return d[na][nb][nc]
''')
add('three_letter_counts', 'ci-three-feed-common', 'letters all three hold, counted with multiplicity, order ignored', '''
from collections import Counter
def three_feed_common(a, b, c):
    return sum((Counter(a) & Counter(b) & Counter(c)).values())
''')
add('three_memo_recursion_OK', 'ci-three-feed-common', 'the ruled-out recursion with lru_cache: right, 150 frames deep', '''
from functools import lru_cache
def three_feed_common(a, b, c):
    @lru_cache(maxsize=None)
    def best(i, j, k):
        if i == len(a) or j == len(b) or k == len(c):
            return 0
        if a[i] == b[j] == c[k]:
            return 1 + best(i + 1, j + 1, k + 1)
        return max(best(i + 1, j, k), best(i, j + 1, k), best(i, j, k + 1))
    return best(0, 0, 0)
''')
add('three_recursion_bounded', 'ci-three-feed-common', 'the ruled-out recursion, unremembered, cut off by min(letters left) against the best found', '''
def three_feed_common(a, b, c):
    best = [0]
    def go(i, j, k, got):
        if got > best[0]:
            best[0] = got
        if got + min(len(a) - i, len(b) - j, len(c) - k) <= best[0]:
            return
        if a[i] == b[j] == c[k]:
            go(i + 1, j + 1, k + 1, got + 1)
        else:
            go(i + 1, j, k, got)
            go(i, j + 1, k, got)
            go(i, j, k + 1, got)
    go(0, 0, 0, 0)
    return best[0]
''')

# ------------------------------------------------------------ ci-even-desks
add('desks_sorted_alternate', 'ci-even-desks', 'sorted, dealt in turn', '''
def even_desks(skills):
    s = sorted(skills)
    return abs(sum(s[::2]) - sum(s[1::2]))
''')
add('desks_greedy_then_swaps', 'ci-even-desks', 'the planted greedy, then swaps of one trader for one while the gap shrinks', '''
def even_desks(skills):
    m = len(skills) // 2
    desks = [[], []]
    for x in sorted(skills, reverse=True):
        lighter = 0 if sum(desks[0]) <= sum(desks[1]) else 1
        if len(desks[lighter]) == m:
            lighter = 1 - lighter
        desks[lighter].append(x)
    a, b = desks
    improved = True
    while improved:
        improved = False
        diff = sum(a) - sum(b)
        for i in range(m):
            for j in range(m):
                nd = diff - 2 * (a[i] - b[j])
                if abs(nd) < abs(diff):
                    a[i], b[j] = b[j], a[i]
                    diff = nd
                    improved = True
    return abs(sum(a) - sum(b))
''')
add('desks_count_upwards', 'ci-even-desks', 'counts updated upwards, so one trader is used twice', '''
def even_desks(skills):
    m = len(skills) // 2
    total = sum(skills)
    reach = [0] * (m + 1)
    reach[0] = 1
    for x in skills:
        for c in range(1, m + 1):
            reach[c] |= reach[c - 1] << x
    return min(abs(total - 2 * s) for s in range(total + 1) if reach[m] >> s & 1)
''')
add('desks_one_count_per_total', 'ci-even-desks', 'one table over totals keeping a single count per total (the count nearest m)', '''
def even_desks(skills):
    m = len(skills) // 2
    total = sum(skills)
    best = {0: 0}
    for x in skills:
        for s, c in list(best.items()):
            if s + x not in best or abs(best[s + x] - m) > abs(c + 1 - m):
                best[s + x] = c + 1
    return min(abs(total - 2 * s) for s, c in best.items() if c == m)
''')
add('desks_bool_table', 'ci-even-desks', 'the stated table as lists of booleans, one cell at a time (the target order of growth, no bit tricks)', '''
def even_desks(skills):
    m = len(skills) // 2
    total = sum(skills)
    can = [[False] * (total + 1) for _ in range(m + 1)]
    can[0][0] = True
    for x in skills:
        for c in range(m, 0, -1):
            row, fewer = can[c], can[c - 1]
            for s in range(total, x - 1, -1):
                if fewer[s - x]:
                    row[s] = True
    return min(abs(total - 2 * s) for s in range(total + 1) if can[m][s])
''')
add('desks_sets_OK', 'ci-even-desks', 'the stated table as a set of totals per count: right', '''
def even_desks(skills):
    m = len(skills) // 2
    total = sum(skills)
    reach = [set() for _ in range(m + 1)]
    reach[0].add(0)
    for s in skills:
        for c in range(m - 1, -1, -1):
            reach[c + 1] |= {t + s for t in reach[c]}
    return min(abs(total - 2 * t) for t in reach[m])
''')

# ------------------------------------------------------------ ci-merged-tape
add('merge_first_row_ones', 'ci-merged-tape', 'the row for no letters of a set to 1 without comparing b with the tape', '''
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    n, m = len(a), len(b)
    if n + m != len(tape):
        return 0
    w = [[0] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1):
        w[0][j] = 1
    for i in range(1, n + 1):
        w[i][0] = w[i - 1][0] if a[i - 1] == tape[i - 1] else 0
        for j in range(1, m + 1):
            ch = tape[i + j - 1]
            w[i][j] = ((w[i - 1][j] if a[i - 1] == ch else 0) + (w[i][j - 1] if b[j - 1] == ch else 0)) % MOD
    return w[n][m]
''')
add('merge_first_col_ones', 'ci-merged-tape', 'the column for no letters of b set to 1 without comparing a with the tape', '''
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    n, m = len(a), len(b)
    if n + m != len(tape):
        return 0
    w = [[0] * (m + 1) for _ in range(n + 1)]
    w[0][0] = 1
    for j in range(1, m + 1):
        w[0][j] = w[0][j - 1] if b[j - 1] == tape[j - 1] else 0
    for i in range(1, n + 1):
        w[i][0] = 1
        for j in range(1, m + 1):
            ch = tape[i + j - 1]
            w[i][j] = ((w[i - 1][j] if a[i - 1] == ch else 0) + (w[i][j - 1] if b[j - 1] == ch else 0)) % MOD
    return w[n][m]
''')
add('merge_either_not_both', 'ci-merged-tape', 'when both feeds match, only the first is followed (elif)', '''
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    n, m = len(a), len(b)
    if n + m != len(tape):
        return 0
    w = [[0] * (m + 1) for _ in range(n + 1)]
    w[0][0] = 1
    for i in range(n + 1):
        for j in range(m + 1):
            if i + j == 0:
                continue
            ch = tape[i + j - 1]
            if i and a[i - 1] == ch and w[i - 1][j]:
                w[i][j] = w[i - 1][j]
            elif j and b[j - 1] == ch:
                w[i][j] = w[i][j - 1]
    return w[n][m] % MOD
''')
add('merge_empty_is_zero', 'ci-merged-tape', 'an empty tape answered 0', '''
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    n, m = len(a), len(b)
    if n + m != len(tape) or not tape:
        return 0
    w = [[0] * (m + 1) for _ in range(n + 1)]
    w[0][0] = 1
    for i in range(n + 1):
        for j in range(m + 1):
            if i + j == 0:
                continue
            ch = tape[i + j - 1]
            w[i][j] = ((w[i - 1][j] if i and a[i - 1] == ch else 0) + (w[i][j - 1] if j and b[j - 1] == ch else 0)) % MOD
    return w[n][m]
''')
add('merge_symmetric_halved', 'ci-merged-tape', 'when the feeds are equal the count is halved (swapping the feeds taken as the same way)', '''
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    n, m = len(a), len(b)
    if n + m != len(tape):
        return 0
    w = [[0] * (m + 1) for _ in range(n + 1)]
    w[0][0] = 1
    for i in range(n + 1):
        for j in range(m + 1):
            if i + j == 0:
                continue
            ch = tape[i + j - 1]
            w[i][j] = (w[i - 1][j] if i and a[i - 1] == ch else 0) + (w[i][j - 1] if j and b[j - 1] == ch else 0)
    r = w[n][m]
    if a == b and a:
        r //= 2
    return r % MOD
''')
add('merge_memo_recursion', 'ci-merged-tape', 'the ruled-out recursion with lru_cache: right method, 600 frames deep at the default limit', '''
from functools import lru_cache
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
add('merge_binomial_shortcut', 'ci-merged-tape', 'the ruled-out recursion, with one-letter inputs answered by a binomial first', '''
from math import comb
MOD = 10 ** 9 + 7
def merge_ways(a, b, tape):
    if len(a) + len(b) != len(tape):
        return 0
    if len(set(a + b + tape)) <= 1:
        return comb(len(tape), len(a)) % MOD
    def ways(i, j):
        if i == len(a) and j == len(b):
            return 1
        total = 0
        if i < len(a) and a[i] == tape[i + j]:
            total += ways(i + 1, j)
        if j < len(b) and b[j] == tape[i + j]:
            total += ways(i, j + 1)
        return total
    return ways(0, 0) % MOD
''')

# ------------------------------------------------------------ ci-light-cargo
add('cargo_single_never', 'ci-light-cargo', 'value loop stops one short, so a parcel alone is never recorded', '''
def light_cargo(weights, values, cap):
    top = sum(values)
    lightest = [0] + [float('inf')] * top
    for w, v in zip(weights, values):
        for t in range(top, v, -1):
            lightest[t] = min(lightest[t], lightest[t - v] + w)
    return max(t for t in range(top + 1) if lightest[t] <= cap)
''')
add('cargo_greedy_best_of_three', 'ci-light-cargo', 'three greedy orders (density, value, lightness), the best taken', '''
def light_cargo(weights, values, cap):
    def g(key):
        load = total = 0
        for i in sorted(range(len(weights)), key=key):
            if load + weights[i] <= cap:
                load += weights[i]
                total += values[i]
        return total
    return max(g(lambda i: -values[i] / weights[i]), g(lambda i: -values[i]), g(lambda i: weights[i]))
''')
add('cargo_scaled_weights', 'ci-light-cargo', 'weight table after dividing weights and cap by a scale that keeps the table small (weights rounded down)', '''
def light_cargo(weights, values, cap):
    scale = max(1, cap // 20000)
    ws = [w // scale for w in weights]
    c = cap // scale
    best = [0] * (c + 1)
    for w, v in zip(ws, values):
        for t in range(c, w - 1, -1):
            if best[t - w] + v > best[t]:
                best[t] = best[t - w] + v
    return best[c]
''')
add('cargo_scaled_weights_up', 'ci-light-cargo', 'the same with weights rounded up', '''
def light_cargo(weights, values, cap):
    scale = max(1, cap // 20000)
    ws = [-(-w // scale) for w in weights]
    c = cap // scale
    best = [0] * (c + 1)
    for w, v in zip(ws, values):
        for t in range(c, w - 1, -1):
            if best[t - w] + v > best[t]:
                best[t] = best[t - w] + v
    return best[c]
''')
add('cargo_sparse_weight_dict', 'ci-light-cargo', 'the weight table kept as a dict of reachable weights, nothing dominated dropped', '''
def light_cargo(weights, values, cap):
    best = {0: 0}
    for w, v in zip(weights, values):
        for t, val in list(best.items()):
            if t + w <= cap and best.get(t + w, -1) < val + v:
                best[t + w] = val + v
    return max(best.values())
''')
add('cargo_memo_take_skip', 'ci-light-cargo', 'take-or-skip recursion remembered on (parcel, room left): the weight table by another name', '''
import sys
from functools import lru_cache
def light_cargo(weights, values, cap):
    sys.setrecursionlimit(10000)
    n = len(weights)
    @lru_cache(maxsize=None)
    def go(i, room):
        if i == n:
            return 0
        best = go(i + 1, room)
        if weights[i] <= room:
            best = max(best, values[i] + go(i + 1, room - weights[i]))
        return best
    return go(0, cap)
''')
add('cargo_branch_and_bound', 'ci-light-cargo', 'take-or-skip in density order with the fractional bound: exponential at worst, not the target', '''
import sys
def light_cargo(weights, values, cap):
    sys.setrecursionlimit(10000)
    order = sorted(range(len(weights)), key=lambda i: -values[i] / weights[i])
    w = [weights[i] for i in order]
    v = [values[i] for i in order]
    n = len(w)
    best = [0]
    def bound(i, room):
        b = 0.0
        while i < n and w[i] <= room:
            room -= w[i]
            b += v[i]
            i += 1
        if i < n:
            b += v[i] * room / w[i]
        return b
    def go(i, room, val):
        if val > best[0]:
            best[0] = val
        if i == n or val + bound(i, room) < best[0] + 1:
            return
        if w[i] <= room:
            go(i + 1, room - w[i], val + v[i])
        go(i + 1, room, val)
    go(0, cap, 0)
    return best[0]
''')

# ------------------------------------------------------------ ci-smooth-orderings
add('smooth_unsorted_copies', 'ci-smooth-orderings', 'the copy rule applied to neighbours in the list as given, not sorted', '''
def smooth_orderings(sizes, d):
    vals = list(sizes)
    n = len(vals)
    ways = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        if i == 0 or vals[i] != vals[i - 1]:
            ways[1 << i][i] = 1
    for sent in range(1 << n):
        for last in range(n):
            w = ways[sent][last]
            if not w:
                continue
            for j in range(n):
                if sent >> j & 1 or abs(vals[last] - vals[j]) > d:
                    continue
                if j and vals[j] == vals[j - 1] and not sent >> (j - 1) & 1:
                    continue
                ways[sent | 1 << j][j] += w
    return sum(ways[-1])
''')
add('smooth_shortcut_then_walk', 'ci-smooth-orderings', 'the ruled-out walk, with "every pair may sit together" answered by a formula first', '''
from collections import Counter
from math import factorial
def smooth_orderings(sizes, d):
    left = Counter(sizes)
    kinds = sorted(left)
    if kinds[-1] - kinds[0] <= d:
        r = factorial(len(sizes))
        for c in left.values():
            r //= factorial(c)
        return r
    def walk(last, placed):
        if placed == len(sizes):
            return 1
        total = 0
        for v in kinds:
            if left[v] and (last is None or abs(v - last) <= d):
                left[v] -= 1
                total += walk(v, placed + 1)
                left[v] += 1
        return total
    return walk(None, 0)
''')
add('smooth_divide_by_two', 'ci-smooth-orderings', 'labelled count divided by 2 for each repeated size, not by the factorial of its count', '''
from collections import Counter
def smooth_orderings(sizes, d):
    n = len(sizes)
    ways = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        ways[1 << i][i] = 1
    for sent in range(1 << n):
        for last in range(n):
            w = ways[sent][last]
            if w:
                for j in range(n):
                    if not sent >> j & 1 and abs(sizes[last] - sizes[j]) <= d:
                        ways[sent | 1 << j][j] += w
    r = sum(ways[-1])
    for c in Counter(sizes).values():
        if c > 1:
            r //= 2
    return r
''')
add('smooth_divide_by_count', 'ci-smooth-orderings', 'labelled count divided by the count of each size, not its factorial', '''
from collections import Counter
def smooth_orderings(sizes, d):
    n = len(sizes)
    ways = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        ways[1 << i][i] = 1
    for sent in range(1 << n):
        for last in range(n):
            w = ways[sent][last]
            if w:
                for j in range(n):
                    if not sent >> j & 1 and abs(sizes[last] - sizes[j]) <= d:
                        ways[sent | 1 << j][j] += w
    r = sum(ways[-1])
    for c in Counter(sizes).values():
        r //= c
    return r
''')
add('smooth_first_copy_only_start', 'ci-smooth-orderings', 'the copy rule on the start but not on later steps', '''
def smooth_orderings(sizes, d):
    vals = sorted(sizes)
    n = len(vals)
    ways = [[0] * n for _ in range(1 << n)]
    for i in range(n):
        if i == 0 or vals[i] != vals[i - 1]:
            ways[1 << i][i] = 1
    for sent in range(1 << n):
        for last in range(n):
            w = ways[sent][last]
            if not w:
                continue
            for j in range(n):
                if sent >> j & 1 or abs(vals[last] - vals[j]) > d:
                    continue
                ways[sent | 1 << j][j] += w
    return sum(ways[-1])
''')
add('smooth_set_of_permutations', 'ci-smooth-orderings', 'set(permutations) filtered: right, 11 factorial tuples', '''
from itertools import permutations
def smooth_orderings(sizes, d):
    return sum(1 for p in set(permutations(sizes)) if all(abs(x - y) <= d for x, y in zip(p, p[1:])))
''')
add('desks_random_restarts', 'ci-even-desks', 'no table: 300 random splits, each improved by swaps of one trader for one, the best kept', '''
import random
def even_desks(skills):
    m = len(skills) // 2
    total = sum(skills)
    rnd = random.Random(1)
    best = total
    xs = list(skills)
    for _ in range(300):
        rnd.shuffle(xs)
        a, b = xs[:m], xs[m:]
        diff = sum(a) - sum(b)
        improved = True
        while improved and diff:
            improved = False
            for i in range(m):
                for j in range(m):
                    nd = diff - 2 * (a[i] - b[j])
                    if abs(nd) < abs(diff):
                        a[i], b[j] = b[j], a[i]
                        diff = nd
                        improved = True
        best = min(best, abs(diff))
        if best <= total % 2:
            break
    return best
''')
add('trace_rows_cols_swapped', 'ci-trace-count', 'rows and columns swapped in the bounds check', '''
MOD = 10 ** 9 + 7
def trace_count(board, word):
    R, C = len(board[0]), len(board)
    ways = {(i, j): 1 for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == word[0]}
    for ch in word[1:]:
        nxt = {}
        for (i, j), w in ways.items():
            for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if 0 <= a < R and 0 <= b < C and a < len(board) and b < len(board[0]) and board[a][b] == ch:
                    nxt[(a, b)] = (nxt.get((a, b), 0) + w) % MOD
        ways = nxt
    return sum(ways.values()) % MOD
''')
add('smooth_memo_counts_OK', 'ci-smooth-orderings', 'the walk remembered on (copies left of each size, last size): right', '''
from collections import Counter
from functools import lru_cache
def smooth_orderings(sizes, d):
    items = sorted(Counter(sizes).items())
    vals = [v for v, _ in items]
    @lru_cache(maxsize=None)
    def go(left, last):
        if not any(left):
            return 1
        total = 0
        for i, c in enumerate(left):
            if c and (last < 0 or abs(vals[i] - vals[last]) <= d):
                total += go(left[:i] + (c - 1,) + left[i + 1:], i)
        return total
    return go(tuple(c for _, c in items), -1)
''')
