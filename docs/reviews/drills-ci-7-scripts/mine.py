"""Second reader's own solutions to pack 7, written from the candidate's view
(brief, constraints, hint, examples) before reading the model solutions.
Where a second method exists I used one that is not the hint's."""
import sys
from functools import lru_cache

MOD = 1_000_000_007


def drop_point_routes(grid):
    # one table with a flag: routes that have met no P, routes that have met one
    R, C = len(grid), len(grid[0])
    no = [[0] * C for _ in range(R)]
    yes = [[0] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            ch = grid[r][c]
            if ch == '#':
                continue
            if r == 0 and c == 0:
                a, b = 1, 0
            else:
                a = (no[r - 1][c] if r else 0) + (no[r][c - 1] if c else 0)
                b = (yes[r - 1][c] if r else 0) + (yes[r][c - 1] if c else 0)
            if ch == 'P':
                a, b = 0, a + b
            no[r][c], yes[r][c] = a % MOD, b % MOD
    return yes[R - 1][C - 1]


def spaced_picks(values, gap):
    v = sorted(values)
    n = len(v)
    out = []
    for mask in range(1, 1 << n):
        pick = [v[i] for i in range(n) if mask >> i & 1]
        if all(y - x >= gap for x, y in zip(pick, pick[1:])):
            out.append(pick)
    out.sort()
    return out


def long_mirrors(tape, k):
    # table by length: pal[i] for the current length, from the two shorter ones
    n = len(tape)
    if k > n:
        return 0
    prev2 = [True] * (n + 1)      # length 0
    prev1 = [True] * n            # length 1
    total = n if k <= 1 else 0
    for L in range(2, n + 1):
        cur = [tape[i] == tape[i + L - 1] and prev2[i + 1] for i in range(n - L + 1)]
        if L >= k:
            total += sum(cur)
        prev2, prev1 = prev1, cur
    return total


def tolerant_common(a, b, tol):
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        x = a[i - 1]
        for j in range(1, m + 1):
            best = prev[j] if prev[j] > cur[j - 1] else cur[j - 1]
            if abs(x - b[j - 1]) <= tol and prev[j - 1] + 1 > best:
                best = prev[j - 1] + 1
            cur[j] = best
        prev = cur
    return prev[m]


def solve_priced_edits(text):
    tok = text.split()
    ins, dele, rep = int(tok[0]), int(tok[1]), int(tok[2])
    q = int(tok[3])
    out = []
    for k in range(q):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        # rolling row over the target
        row = [j * ins for j in range(len(t) + 1)]
        for i in range(1, len(s) + 1):
            new = [i * dele] + [0] * len(t)
            for j in range(1, len(t) + 1):
                best = row[j - 1] + (0 if s[i - 1] == t[j - 1] else rep)
                if row[j] + dele < best:
                    best = row[j] + dele
                if new[j - 1] + ins < best:
                    best = new[j - 1] + ins
                new[j] = best
            row = new
        out.append(str(row[-1]))
    return '\n'.join(out)


def hold_value(weights, values, cap, k):
    # exactly c crates at exactly weight w, kept as dicts
    states = [dict() for _ in range(k + 1)]
    states[0][0] = 0
    for w, v in zip(weights, values):
        for c in range(k - 1, -1, -1):
            for tw, tv in list(states[c].items()):
                nw = tw + w
                if nw <= cap and states[c + 1].get(nw, -1) < tv + v:
                    states[c + 1][nw] = tv + v
    return max(max(s.values()) for s in states if s)


def queen_count(board, q):
    n = len(board)

    def go(r, left, cols, d1, d2):
        if left == 0:
            return 1
        if n - r < left:
            return 0
        total = go(r + 1, left, cols, d1, d2)
        for c in range(len(board[r])):
            if board[r][c] == '.' and not (cols >> c & 1) and not (d1 >> (r + c) & 1) and not (d2 >> (r - c + 8) & 1):
                total += go(r + 1, left - 1, cols | 1 << c, d1 | 1 << (r + c), d2 | 1 << (r - c + 8))
        return total
    return go(0, q, 0, 0, 0)


def invoice_matches(amounts, target, k):
    # by distinct amount and how many copies of it to use
    from collections import Counter
    cnt = sorted(Counter(amounts).items())
    out = []

    def go(i, left, room, cur):
        if left == 0:
            out.append(cur[:])
            return
        if i == len(cnt) or room == 0:
            return
        a, c = cnt[i]
        if a > left:
            return
        for use in range(0, min(c, room, left // a) + 1):
            go(i + 1, left - use * a, room - use, cur + [a] * use)
    go(0, target, k, [])
    out.sort()
    return out


def trace_count(board, word):
    R, C = len(board), len(board[0])
    cur = [[1 if board[r][c] == word[0] else 0 for c in range(C)] for r in range(R)]
    for ch in word[1:]:
        nxt = [[0] * C for _ in range(R)]
        for r in range(R):
            for c in range(C):
                if board[r][c] == ch:
                    s = 0
                    if r:
                        s += cur[r - 1][c]
                    if r + 1 < R:
                        s += cur[r + 1][c]
                    if c:
                        s += cur[r][c - 1]
                    if c + 1 < C:
                        s += cur[r][c + 1]
                    nxt[r][c] = s % MOD
        cur = nxt
    return sum(map(sum, cur)) % MOD


def solve_mirror_pieces(text):
    tok = text.split()
    q = int(tok[0])
    out = []
    for s in tok[1:1 + q]:
        n = len(s)
        # pal[i][j] table, then best over the last piece
        pal = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
        best = [0] * (n + 1)
        for j in range(1, n + 1):
            best[j] = min(best[i] + 1 for i in range(j) if pal[i][j - 1])
        out.append(str(best[n]))
    return '\n'.join(out)


def three_feed_common(a, b, c):
    sys.setrecursionlimit(10000)

    @lru_cache(maxsize=None)
    def go(i, j, k):
        if i == len(a) or j == len(b) or k == len(c):
            return 0
        if a[i] == b[j] == c[k]:
            return 1 + go(i + 1, j + 1, k + 1)
        return max(go(i + 1, j, k), go(i, j + 1, k), go(i, j, k + 1))
    return go(0, 0, 0)


def even_desks(skills):
    m = len(skills) // 2
    total = sum(skills)
    reach = [set() for _ in range(m + 1)]
    reach[0].add(0)
    for s in skills:
        for c in range(m - 1, -1, -1):
            reach[c + 1] |= {t + s for t in reach[c]}
    return min(abs(total - 2 * t) for t in reach[m])


def merge_ways(a, b, tape):
    if len(a) + len(b) != len(tape):
        return 0
    m = len(b)
    row = [0] * (m + 1)
    row[0] = 1
    for j in range(1, m + 1):
        row[j] = row[j - 1] if b[j - 1] == tape[j - 1] else 0
    for i in range(1, len(a) + 1):
        row[0] = row[0] if a[i - 1] == tape[i - 1] else 0
        for j in range(1, m + 1):
            t = tape[i + j - 1]
            v = 0
            if a[i - 1] == t:
                v += row[j]
            if b[j - 1] == t:
                v += row[j - 1]
            row[j] = v % MOD
    return row[m]


def light_cargo(weights, values, cap):
    # Pareto list of (weight, value): lighter and worth more, merged per parcel
    front = [(0, 0)]
    for w, v in zip(weights, values):
        add = [(fw + w, fv + v) for fw, fv in front if fw + w <= cap]
        merged = sorted(front + add, key=lambda p: (p[0], -p[1]))
        front = []
        best = -1
        for fw, fv in merged:
            if fv > best:
                front.append((fw, fv))
                best = fv
    return front[-1][1]


def smooth_orderings(sizes, d):
    # by how many of each distinct size are left, and the last size sent
    from collections import Counter
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
