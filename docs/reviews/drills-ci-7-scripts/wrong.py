"""Wrong or too-slow solutions a real candidate writes, none of them planted by the
author. Run: harness.py wrong.py app/content/drills --limit 15
CANDIDATES = {label: (drill id, source, what is wrong)}. A label ending _OK is a
candidate that turned out to be right (kept so nobody re-tries it)."""
CANDIDATES = {}


def add(label, did, comment, src):
    CANDIDATES[label] = (did, src, comment)


# ------------------------------------------------------------ ci-drop-point-routes
add('drop_exactly_one', 'ci-drop-point-routes', 'counts routes through exactly one drop point', '''
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    R, C = len(grid), len(grid[0])
    z = [[0] * C for _ in range(R)]
    o = [[0] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            ch = grid[r][c]
            if ch == '#':
                continue
            if r == 0 and c == 0:
                a, b = 1, 0
            else:
                a = (z[r-1][c] if r else 0) + (z[r][c-1] if c else 0)
                b = (o[r-1][c] if r else 0) + (o[r][c-1] if c else 0)
            if ch == 'P':
                a, b = 0, a
            z[r][c], o[r][c] = a % MOD, b % MOD
    return o[-1][-1]
''')
add('drop_first_row_ones', 'ci-drop-point-routes', 'first row and column set to 1 without looking for shelves', '''
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    R, C = len(grid), len(grid[0])
    def count(avoid):
        w = [[0] * C for _ in range(R)]
        for r in range(R):
            for c in range(C):
                if grid[r][c] in avoid:
                    continue
                if r == 0 or c == 0:
                    w[r][c] = 1
                else:
                    w[r][c] = (w[r-1][c] + w[r][c-1]) % MOD
        return w[-1][-1]
    return (count('#') - count('#P')) % MOD
''')
add('drop_end_not_checked', 'ci-drop-point-routes', 'a drop point on the last cell is not seen (flag set when leaving a cell)', '''
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    R, C = len(grid), len(grid[0])
    no = [[0] * C for _ in range(R)]
    yes = [[0] * C for _ in range(R)]
    no[0][0] = 1
    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#':
                no[r][c] = yes[r][c] = 0
                continue
            a, b = no[r][c], yes[r][c]
            if grid[r][c] == 'P':
                a, b = 0, a + b
            for rr, cc in ((r + 1, c), (r, c + 1)):
                if rr < R and cc < C:
                    no[rr][cc] = (no[rr][cc] + a) % MOD
                    yes[rr][cc] = (yes[rr][cc] + b) % MOD
    return yes[-1][-1]
''')
add('drop_square_only', 'ci-drop-point-routes', 'rows and columns swapped (right only on a square floor)', '''
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    n = len(grid)
    m = len(grid[0])
    e = [[0] * n for _ in range(m)]
    k = [[0] * n for _ in range(m)]
    for i in range(min(n, m)):
        for j in range(min(n, m)):
            pass
    for i in range(n):
        for j in range(m):
            ch = grid[i][j]
            if ch == '#':
                continue
            if i == 0 and j == 0:
                a = c = 1
            else:
                a = (e[j][i-1] if i else 0) + (e[j-1][i] if j else 0)
                c = (k[j][i-1] if i else 0) + (k[j-1][i] if j else 0)
            e[j][i] = a % MOD
            k[j][i] = 0 if ch == 'P' else c % MOD
    return (e[n-1][m-1] - k[n-1][m-1]) % MOD
''')
add('drop_mod_of_difference_missing', 'ci-drop-point-routes', 'both counts reduced, the difference not (negative answers)', '''
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    rows, cols = len(grid), len(grid[0])
    every = [0] * cols
    clear = [0] * cols
    for i in range(rows):
        for j in range(cols):
            ch = grid[i][j]
            if ch == '#':
                every[j] = clear[j] = 0
                continue
            if i == 0 and j == 0:
                a = c = 1
            else:
                a = every[j] + (every[j - 1] if j else 0)
                c = clear[j] + (clear[j - 1] if j else 0)
            every[j] = a % MOD
            clear[j] = 0 if ch == 'P' else c % MOD
    d = every[-1] - clear[-1]
    return d if d >= 0 else -d
''')
add('drop_recursive_memo_OK', 'ci-drop-point-routes', 'memoised recursion from the end, 400 frames deep: right', '''
import sys
from functools import lru_cache
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    R, C = len(grid), len(grid[0])
    @lru_cache(maxsize=None)
    def go(r, c, seen):
        if r >= R or c >= C or grid[r][c] == '#':
            return 0
        seen = seen or grid[r][c] == 'P'
        if r == R - 1 and c == C - 1:
            return 1 if seen else 0
        return (go(r + 1, c, seen) + go(r, c + 1, seen)) % MOD
    return go(0, 0, False)
''')

# ------------------------------------------------------------ ci-spaced-picks
add('picks_with_empty', 'ci-spaced-picks', 'the empty choice listed', '''
def spaced_picks(values, gap):
    v = sorted(values)
    out = []
    def walk(i, pick):
        out.append(pick[:])
        for j in range(i, len(v)):
            if not pick or v[j] - pick[-1] >= gap:
                walk(j + 1, pick + [v[j]])
    walk(0, [])
    return out
''')
add('picks_not_copied', 'ci-spaced-picks', 'the pick stored without a copy, then popped', '''
def spaced_picks(values, gap):
    v = sorted(values)
    out, pick = [], []
    def walk(i):
        for j in range(i, len(v)):
            if pick and v[j] - pick[-1] < gap:
                continue
            pick.append(v[j])
            out.append(pick)
            walk(j + 1)
            pick.pop()
    walk(0)
    return out
''')
add('picks_take_skip_order', 'ci-spaced-picks', 'take-or-skip recursion, choices in the order the leaves come, not sorted', '''
def spaced_picks(values, gap):
    v = sorted(values)
    out = []
    def walk(i, pick):
        if i == len(v):
            if pick:
                out.append(pick)
            return
        if not pick or v[i] - pick[-1] >= gap:
            walk(i + 1, pick + [v[i]])
        walk(i + 1, pick)
    walk(0, [])
    return out
''')
add('picks_abs_sort', 'ci-spaced-picks', 'gap tested on absolute values (wrong with a negative strike)', '''
def spaced_picks(values, gap):
    v = sorted(values)
    out, pick = [], []
    def walk(i):
        for j in range(i, len(v)):
            if pick and abs(v[j]) - abs(pick[-1]) < gap:
                continue
            pick.append(v[j])
            out.append(pick[:])
            walk(j + 1)
            pick.pop()
    walk(0)
    return out
''')
add('picks_string_order', 'ci-spaced-picks', 'choices sorted as text', '''
from itertools import combinations
def spaced_picks(values, gap):
    v = sorted(values)
    out = []
    for size in range(1, len(v) + 1):
        for p in combinations(v, size):
            if all(b - a >= gap for a, b in zip(p, p[1:])):
                out.append(list(p))
    return sorted(out, key=str)
''')
add('picks_pairs_only_next', 'ci-spaced-picks', 'unsorted input, all pairs tested, each choice sorted but the list left in walk order', '''
def spaced_picks(values, gap):
    out, pick = [], []
    def walk(i):
        for j in range(i, len(values)):
            if any(abs(values[j] - p) < gap for p in pick):
                continue
            pick.append(values[j])
            out.append(sorted(pick))
            walk(j + 1)
            pick.pop()
    walk(0)
    return out
''')

# ------------------------------------------------------------ ci-long-mirrors
add('mirrors_exactly_k', 'ci-long-mirrors', 'counts length exactly k', '''
def long_mirrors(tape, k):
    n = len(tape)
    return sum(1 for i in range(n - k + 1) if tape[i:i + k] == tape[i:i + k][::-1])
''')
add('mirrors_radius_formula', 'ci-long-mirrors', 'longest stretch per centre, then (L - k + 1) of them, forgetting they shrink by two', '''
def long_mirrors(tape, k):
    n = len(tape)
    count = 0
    for centre in range(2 * n - 1):
        lo, hi = centre // 2, (centre + 1) // 2
        L = 0
        while lo >= 0 and hi < n and tape[lo] == tape[hi]:
            L = hi - lo + 1
            lo -= 1
            hi += 1
        if L >= k:
            count += L - k + 1
    return count
''')
add('mirrors_radius_formula_parity', 'ci-long-mirrors', 'longest per centre, then (L - k) // 2 + 1 with k rounded the wrong way', '''
def long_mirrors(tape, k):
    n = len(tape)
    count = 0
    for centre in range(2 * n - 1):
        lo, hi = centre // 2, (centre + 1) // 2
        L = 0
        while lo >= 0 and hi < n and tape[lo] == tape[hi]:
            L = hi - lo + 1
            lo -= 1
            hi += 1
        if L >= k:
            count += (L - k + 1) // 2 + 1
    return count
''')
add('mirrors_table_len2', 'ci-long-mirrors', 'table by length that never seeds length 2 (even lengths lost)', '''
def long_mirrors(tape, k):
    n = len(tape)
    pal = [[False] * n for _ in range(n)]
    count = 0
    for i in range(n):
        pal[i][i] = True
        if k <= 1:
            count += 1
    for L in range(3, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            if tape[i] == tape[j] and pal[i + 1][j - 1]:
                pal[i][j] = True
                if L >= k:
                    count += 1
    for i in range(n - 1):
        if tape[i] == tape[i + 1]:
            pal[i][i + 1] = True
            if k <= 2:
                count += 1
    return count
''')
add('mirrors_cubic_OK_slow', 'ci-long-mirrors', 'every stretch sliced and reversed: O(n^3), not ruled out at difficulty 2', '''
def long_mirrors(tape, k):
    n = len(tape)
    count = 0
    for i in range(n):
        for j in range(i + k, n + 1):
            piece = tape[i:j]
            if piece == piece[::-1]:
                count += 1
    return count
''')
add('mirrors_k_over_n_crash', 'ci-long-mirrors', 'table sized by k, fails when k is longer than the tape', '''
def long_mirrors(tape, k):
    n = len(tape)
    pal = [[False] * (n + 1) for _ in range(n + 1)]
    count = 0
    for L in range(1, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            pal[i][j] = tape[i] == tape[j] and (L < 3 or pal[i + 1][j - 1])
    start = [0] * n
    for i in range(n):
        if pal[i][i + k - 1]:
            pass
    for i in range(n):
        for j in range(i + k - 1, n):
            count += pal[i][j]
    return count
''')

# ------------------------------------------------------------ ci-tolerant-common
add('tol_contiguous', 'ci-tolerant-common', 'longest common run of neighbours (substring table)', '''
def tolerant_common(a, b, tol):
    best = 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if abs(x - y) <= tol else 0)
            best = max(best, cur[-1])
        prev = cur
    return best
''')
add('tol_one_sided', 'ci-tolerant-common', 'no abs: b may be above a by any amount', '''
def tolerant_common(a, b, tol):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            if x - y <= tol:
                cur.append(prev[j] + 1)
            else:
                cur.append(max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]
''')
add('tol_greedy_both_ways', 'ci-tolerant-common', 'the first-close-tick greedy from a and from b, the larger taken', '''
def tolerant_common(a, b, tol):
    def g(a, b):
        j = count = 0
        for x in a:
            k = j
            while k < len(b) and abs(x - b[k]) > tol:
                k += 1
            if k < len(b):
                count += 1
                j = k + 1
        return count
    return max(g(a, b), g(b, a))
''')
add('tol_greedy_from_each_start', 'ci-tolerant-common', 'the greedy restarted from every tick of a, the best taken', '''
def tolerant_common(a, b, tol):
    def g(a, b):
        j = count = 0
        for x in a:
            k = j
            while k < len(b) and abs(x - b[k]) > tol:
                k += 1
            if k < len(b):
                count += 1
                j = k + 1
        return count
    return max([g(a[i:], b) for i in range(len(a))] + [g(b[i:], a) for i in range(len(b))] + [0])
''')
add('tol_transitive', 'ci-tolerant-common', 'ticks bucketed by tol + 1 and the classic run on bucket numbers', '''
def tolerant_common(a, b, tol):
    a = [x // (tol + 1) for x in a]
    b = [x // (tol + 1) for x in b]
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]
''')
add('tol_increasing', 'ci-tolerant-common', 'a tick of b reused by several ticks of a (pairs kept non-crossing, not strict)', '''
def tolerant_common(a, b, tol):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            if abs(x - y) <= tol:
                cur.append(max(prev[j + 1], cur[j], prev[j]) + 1 if False else max(prev[j + 1] + 1, cur[j]))
            else:
                cur.append(max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]
''')

# ------------------------------------------------------------ ci-priced-edits
add('edits_borders_swapped', 'ci-priced-edits', 'first row priced as deletes and first column as inserts, inside right', '''
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        prev = [j * dele for j in range(len(t) + 1)]
        for i, x in enumerate(s, 1):
            cur = [i * ins]
            for j, y in enumerate(t, 1):
                cur.append(min(prev[j - 1] + (0 if x == y else sub), prev[j] + dele, cur[j - 1] + ins))
            prev = cur
        out.append(str(prev[-1]))
    return '\\n'.join(out)
''')
add('edits_unit_times_price', 'ci-priced-edits', 'unit-cost table, then each kind of edit priced on the way back', '''
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        n, m = len(s), len(t)
        d = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            d[i][0] = i
        for j in range(m + 1):
            d[0][j] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                d[i][j] = min(d[i-1][j-1] + (s[i-1] != t[j-1]), d[i-1][j] + 1, d[i][j-1] + 1)
        i, j, cost = n, m, 0
        while i or j:
            if i and j and d[i][j] == d[i-1][j-1] + (s[i-1] != t[j-1]):
                cost += sub if s[i-1] != t[j-1] else 0
                i, j = i - 1, j - 1
            elif i and d[i][j] == d[i-1][j] + 1:
                cost += dele
                i -= 1
            else:
                cost += ins
                j -= 1
        out.append(str(cost))
    return '\\n'.join(out)
''')
add('edits_sub_capped_unit', 'ci-priced-edits', 'length difference priced, then mismatches at min(replace, insert + delete), no alignment', '''
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        n, m = len(s), len(t)
        d = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            d[i][0] = i
        for j in range(m + 1):
            d[0][j] = j
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                d[i][j] = min(d[i-1][j-1] + (s[i-1] != t[j-1]), d[i-1][j] + 1, d[i][j-1] + 1)
        out.append(str(d[n][m] * min(ins, dele, sub)))
    return '\\n'.join(out)
''')
add('edits_equal_skips_min', 'ci-priced-edits', 'never replaces: only insert and delete, and a free match (replace priced as insert + delete)', '''
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        prev = [j * ins for j in range(len(t) + 1)]
        for i, x in enumerate(s, 1):
            cur = [i * dele]
            for j, y in enumerate(t, 1):
                if x == y:
                    cur.append(prev[j - 1])
                else:
                    cur.append(min(prev[j] + dele, cur[j - 1] + ins))
            prev = cur
        out.append(str(prev[-1]))
    return '\\n'.join(out)
''')
add('edits_always_replace_or_one', 'ci-priced-edits', 'a mismatch always priced at the replacement, insert and delete only for the length difference', '''
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        prev = [j * ins for j in range(len(t) + 1)]
        for i, x in enumerate(s, 1):
            cur = [i * dele]
            for j, y in enumerate(t, 1):
                if x == y:
                    cur.append(prev[j - 1])
                elif len(s) == len(t):
                    cur.append(min(prev[j - 1] + sub, prev[j] + dele + 0 * ins, cur[j - 1] + ins) if False else prev[j - 1] + sub)
                else:
                    cur.append(min(prev[j - 1] + sub, prev[j] + dele, cur[j - 1] + ins))
            prev = cur
        out.append(str(prev[-1]))
    return '\\n'.join(out)
''')
add('edits_trailing_newline', 'ci-priced-edits', 'a newline after the last answer', '''
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, sub = int(tok[0]), int(tok[1]), int(tok[2])
    out = ''
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        prev = [j * ins for j in range(len(t) + 1)]
        for i, x in enumerate(s, 1):
            cur = [i * dele]
            for j, y in enumerate(t, 1):
                cur.append(min(prev[j - 1] + (0 if x == y else sub), prev[j] + dele, cur[j - 1] + ins))
            prev = cur
        out += str(prev[-1]) + '\\n'
    return out
''')
add('edits_memo_recursion', 'ci-priced-edits', 'memoised recursion at the default limit: 600 frames deep on 300 letters', '''
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
            return min(go(i + 1, j + 1) + (0 if s[i] == t[j] else sub), go(i + 1, j) + dele, go(i, j + 1) + ins)
        out.append(str(go(0, 0)))
    return '\\n'.join(out)
''')

# ------------------------------------------------------------ ci-hold-limit
add('hold_exactly_k', 'ci-hold-limit', 'exactly k crates, not at most', '''
def hold_value(weights, values, cap, k):
    NEG = float('-inf')
    best = [[NEG] * (cap + 1) for _ in range(k + 1)]
    for t in range(cap + 1):
        best[0][t] = 0
    for w, v in zip(weights, values):
        for c in range(k, 0, -1):
            for t in range(cap, w - 1, -1):
                if best[c - 1][t - w] + v > best[c][t]:
                    best[c][t] = best[c - 1][t - w] + v
    return max(0, best[k][cap])
''')
add('hold_exact_weight_last_cell', 'ci-hold-limit', 'exact-weight table, answer read from the last cell only', '''
def hold_value(weights, values, cap, k):
    NEG = float('-inf')
    best = [[NEG] * (cap + 1) for _ in range(k + 1)]
    best[0][0] = 0
    for w, v in zip(weights, values):
        for c in range(k, 0, -1):
            for t in range(cap, w - 1, -1):
                if best[c - 1][t - w] + v > best[c][t]:
                    best[c][t] = best[c - 1][t - w] + v
    r = max(best[c][cap] for c in range(k + 1))
    return r if r > 0 else 0
''')
add('hold_weight_excl', 'ci-hold-limit', 'weights loop stops one short: a crate never fills the hold exactly', '''
def hold_value(weights, values, cap, k):
    best = [[0] * (cap + 1) for _ in range(k + 1)]
    for w, v in zip(weights, values):
        for c in range(k, 0, -1):
            for t in range(cap, w, -1):
                if best[c - 1][t - w] + v > best[c][t]:
                    best[c][t] = best[c - 1][t - w] + v
    return best[k][cap]
''')
add('hold_top_k_then_knapsack', 'ci-hold-limit', 'plain knapsack, then if it used too many crates, knapsack over the k most valuable', '''
def hold_value(weights, values, cap, k):
    def plain(ws, vs):
        best = [(0, 0)] * (cap + 1)
        for w, v in zip(ws, vs):
            for t in range(cap, w - 1, -1):
                cand = (best[t - w][0] + v, best[t - w][1] - 1)
                if cand > best[t]:
                    best[t] = cand
        return best[cap]
    val, used = plain(weights, values)
    if -used <= k:
        return val
    order = sorted(range(len(weights)), key=lambda i: -values[i])[:k]
    return plain([weights[i] for i in order], [values[i] for i in order])[0]
''')
add('hold_count_as_tiebreak', 'ci-hold-limit', 'one table over weight keeping (value, fewest crates); a state over k crates is dropped', '''
def hold_value(weights, values, cap, k):
    best = [(0, 0)] * (cap + 1)
    for w, v in zip(weights, values):
        for t in range(cap, w - 1, -1):
            val, used = best[t - w]
            if used < k and (val + v > best[t][0] or (val + v == best[t][0] and used + 1 < best[t][1])):
                best[t] = (val + v, used + 1)
    return best[cap][0]
''')
add('hold_k_minus', 'ci-hold-limit', 'k not clipped and the table read at row k - 1', '''
def hold_value(weights, values, cap, k):
    best = [[0] * (cap + 1) for _ in range(k + 1)]
    for w, v in zip(weights, values):
        for c in range(k - 1, 0, -1):
            for t in range(cap, w - 1, -1):
                best[c][t] = max(best[c][t], best[c - 1][t - w] + v)
    return max(b[cap] for b in best)
''')
