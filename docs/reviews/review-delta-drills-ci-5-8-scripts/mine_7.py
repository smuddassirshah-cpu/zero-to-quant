"""Delta reader's own solutions, pack 7. Written from the briefs, by a method other
than the model's wherever one exists. Used by run.py. Plain brute forces for the
small cases are in extra_7.py; top-down forms and their depths in depth_7.py."""
import heapq
from collections import Counter, deque

MOD = 1_000_000_007


# ci-drop-point-routes: one pass carrying two counts, routes that have met a P and routes that have not.
def drop_point_routes(grid):
    R, C = len(grid), len(grid[0])
    met = [[0] * C for _ in range(R)]
    not_met = [[0] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            ch = grid[r][c]
            if ch == '#':
                continue
            if r == 0 and c == 0:
                m, nm = 0, 1
            else:
                m = (met[r - 1][c] if r else 0) + (met[r][c - 1] if c else 0)
                nm = (not_met[r - 1][c] if r else 0) + (not_met[r][c - 1] if c else 0)
            if ch == 'P':
                m, nm = m + nm, 0
            met[r][c], not_met[r][c] = m % MOD, nm % MOD
    return met[R - 1][C - 1]


# ci-long-mirrors: every stretch, compared with its reverse.
def long_mirrors(tape, k):
    n = len(tape)
    tot = 0
    for i in range(n):
        for j in range(i + max(k, 1), n + 1):
            s = tape[i:j]
            if s == s[::-1]:
                tot += 1
    return tot


# ci-merged-tape: counts pushed forward letter by letter of the tape.
def merge_ways(a, b, tape):
    if len(a) + len(b) != len(tape):
        return 0
    cur = {0: 1}              # letters of a used -> ways
    for pos, ch in enumerate(tape):
        nxt = {}
        for i, w in cur.items():
            j = pos - i
            if i < len(a) and a[i] == ch:
                nxt[i + 1] = (nxt.get(i + 1, 0) + w) % MOD
            if j < len(b) and b[j] == ch:
                nxt[i] = (nxt.get(i, 0) + w) % MOD
        cur = nxt
        if not cur:
            return 0
    return cur.get(len(a), 0) % MOD


# ci-mirror-pieces: breadth-first search over cut positions.
def solve_mirror_pieces(text):
    tok = text.split()
    out = []
    for tape in tok[1:1 + int(tok[0])]:
        n = len(tape)
        dist = [-1] * (n + 1)
        dist[0] = 0
        q = deque([0])
        while q and dist[n] < 0:
            i = q.popleft()
            for j in range(n, i, -1):
                if dist[j] < 0:
                    s = tape[i:j]
                    if s == s[::-1]:
                        dist[j] = dist[i] + 1
                        q.append(j)
        out.append(str(dist[n]))
    return '\n'.join(out)


# ci-priced-edits: cheapest path on the grid of (letters of source used, letters of target made).
def solve_priced_edits(text):
    tok = text.split()
    ins, dele, rep = int(tok[0]), int(tok[1]), int(tok[2])
    q = int(tok[3])
    out = []
    for k in range(q):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]
        n, m = len(s), len(t)
        best = {(0, 0): 0}
        heap = [(0, 0, 0)]
        while heap:
            c, i, j = heapq.heappop(heap)
            if c > best[(i, j)]:
                continue
            if i == n and j == m:
                out.append(str(c))
                break
            moves = []
            if j < m:
                moves.append((c + ins, i, j + 1))
            if i < n:
                moves.append((c + dele, i + 1, j))
            if i < n and j < m:
                moves.append((c + (0 if s[i] == t[j] else rep), i + 1, j + 1))
            for nc, ni, nj in moves:
                if nc < best.get((ni, nj), 1 << 60):
                    best[(ni, nj)] = nc
                    heapq.heappush(heap, (nc, ni, nj))
    return '\n'.join(out)


# ci-tolerant-common: table from the far ends, every one of the three moves always tried.
def tolerant_common(a, b, tol):
    n, m = len(a), len(b)
    f = [[0] * (m + 2) for _ in range(n + 2)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            v = max(f[i + 1][j], f[i][j + 1])
            if abs(a[i] - b[j]) <= tol:
                v = max(v, 1 + f[i + 1][j + 1])
            f[i][j] = v
    return f[0][0]


# ci-three-feed-common: the same from the far ends, in three dimensions.
def three_feed_common(a, b, c):
    na, nb, nc = len(a), len(b), len(c)
    f = [[[0] * (nc + 2) for _ in range(nb + 2)] for _ in range(na + 2)]
    for i in range(na - 1, -1, -1):
        for j in range(nb - 1, -1, -1):
            for k in range(nc - 1, -1, -1):
                v = max(f[i + 1][j][k], f[i][j + 1][k], f[i][j][k + 1])
                if a[i] == b[j] == c[k]:
                    v = max(v, 1 + f[i + 1][j + 1][k + 1])
                f[i][j][k] = v
    return f[0][0][0]


# ci-smooth-orderings: remembered count over (how many of each size are left, last size).
def smooth_orderings(sizes, d):
    kinds = sorted(set(sizes))
    cnt = Counter(sizes)
    memo = {}

    def go(left, last):
        if not any(left):
            return 1
        key = (left, last)
        if key in memo:
            return memo[key]
        tot = 0
        for i, s in enumerate(kinds):
            if left[i] and (last is None or abs(s - last) <= d):
                tot += go(left[:i] + (left[i] - 1,) + left[i + 1:], s)
        memo[key] = tot
        return tot

    return go(tuple(cnt[s] for s in kinds), None)


# ci-hold-limit: best value for every (crates, tonnes) reached, pushed forward.
def hold_value(weights, values, cap, k):
    best = {(0, 0): 0}
    for w, v in zip(weights, values):
        nxt = dict(best)
        for (c, t), val in best.items():
            if c < k and t + w <= cap:
                key = (c + 1, t + w)
                if val + v > nxt.get(key, -1):
                    nxt[key] = val + v
        best = nxt
    return max(best.values())


# ci-trace-count: counts pushed from each square to its neighbours.
def trace_count(board, word):
    R, C = len(board), len(board[0])
    cur = {(r, c): 1 for r in range(R) for c in range(C) if board[r][c] == word[0]}
    for ch in word[1:]:
        nxt = {}
        for (r, c), w in cur.items():
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and board[nr][nc] == ch:
                    nxt[(nr, nc)] = (nxt.get((nr, nc), 0) + w) % MOD
        cur = nxt
    return sum(cur.values()) % MOD
