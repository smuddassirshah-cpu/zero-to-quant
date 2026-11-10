"""The delta reader's own solutions to the 22 drills the fix pass changed.
Written from each brief as it now stands, by a method other than the model's wherever one exists."""
import re
import heapq
from bisect import bisect_left
from fractions import Fraction
from collections import Counter, deque


def find_in_ring(ring, targets):
    # un-turn the ring with a linear scan for the smallest id, then bisect a plain sorted copy
    n = len(ring)
    if n == 0:
        return [-1] * len(targets)
    s = ring.index(min(ring))
    flat = ring[s:] + ring[:s]
    out = []
    for t in targets:
        a = bisect_left(flat, t)
        out.append((s + a) % n if a < n else -1)
    return out


def solve_tick_ranges(text):
    # offline: queries in rising order, one merge pass over the log; no bisect
    v = [int(x) for x in text.split()]
    n, q = v[0], v[1]
    ticks, qs = v[2:2 + n], v[2 + n:2 + n + q]
    ans = [None] * q
    i = j = 0
    last_t = None
    for k in sorted(range(q), key=lambda k: qs[k]):
        t = qs[k]
        while i < n and ticks[i] < t:
            i += 1
        if t != last_t:              # a repeated query reuses the run already measured
            j = i
            while j < n and ticks[j] == t:
                j += 1
            last_t = t
        ans[k] = '%d %d' % (i, j - 1) if j > i else '-1 %d' % i
    return '\n'.join(ans)


def board_words(board, words):
    # a set of every prefix; grow strings from each cell while they are still a prefix
    prefixes, whole = set(), set(words)
    for w in words:
        for i in range(1, len(w) + 1):
            prefixes.add(w[:i])
    R = len(board); C = len(board[0]) if R else 0
    found = set()
    used = [[False] * C for _ in range(R)]

    def go(r, c, s):
        s += board[r][c]
        if s not in prefixes:
            return
        if s in whole:
            found.add(s)
        used[r][c] = True
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            rr, cc = r + dr, c + dc
            if 0 <= rr < R and 0 <= cc < C and not used[rr][cc]:
                go(rr, cc, s)
        used[r][c] = False

    for r in range(R):
        for c in range(C):
            go(r, c, '')
    return sorted(found)


def solve_live_median(text):
    # offline: compress the sizes, keep live counts in a Fenwick tree, find the k-th by descent
    tok = text.split()
    q = int(tok[0]) if tok else 0
    ops = [(tok[1 + 2 * i], int(tok[2 + 2 * i])) for i in range(q)]
    vals = sorted({x for _, x in ops})
    idx = {x: i + 1 for i, x in enumerate(vals)}
    m = len(vals)
    tree = [0] * (m + 1)
    top = 1
    while top * 2 <= m:
        top *= 2
    live = 0
    out = []
    for op, x in ops:
        d = 1 if op == '+' else -1
        live += d
        i = idx[x]
        while i <= m:
            tree[i] += d
            i += i & -i
        if live == 0:
            out.append('-'); continue
        k = (live + 1) // 2
        pos, step = 0, top
        while step:
            nxt = pos + step
            if nxt <= m and tree[nxt] < k:
                pos = nxt; k -= tree[nxt]
            step >>= 1
        out.append(str(vals[pos]))
    return ' '.join(out)


def busiest_links(trips, k):
    c = Counter('-'.join(sorted(t)) for t in trips)
    return sorted(c, key=lambda name: (-c[name], name))[:k]


def formula_value(formula):
    # one flat token stack; a closing bracket folds back to the nearest name
    st = []
    for tok in re.findall(r'[A-Z]+|-?\d+|\)', formula):
        if tok == ')':
            j = len(st) - 1
            while not isinstance(st[j], str):
                j -= 1
            args = st[j + 1:]
            f = {'SUM': sum, 'MAX': max, 'MIN': min}[st[j]]
            del st[j:]
            st.append(f(args))
        elif tok[0].isalpha():
            st.append(tok)
        else:
            st.append(int(tok))
    return st[0]


def cheapest_pairs(a, b, k):
    # search the k-th cost by value, then list every trade below it and pad with the k-th cost
    if k == 0 or not a or not b:
        return []

    def at_most(v):
        cnt, j = 0, len(b)
        for x in a:
            while j and x + b[j - 1] > v:
                j -= 1
            if j == 0:
                break
            cnt += j
            if cnt >= k:
                break
        return cnt

    lo, hi = a[0] + b[0], a[-1] + b[-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    out = []
    for x in a:
        if x + b[0] >= lo:
            break
        for y in b:
            if x + y >= lo:
                break
            out.append(x + y)
    out.sort()
    return out + [lo] * (k - len(out))


def min_clear_rate(queues, minutes):
    lo, hi = 0, max(queues)          # lo fails (or is 0), hi works
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if sum(-(-q // mid) for q in queues) <= minutes:
            hi = mid
        else:
            lo = mid
    return hi


def count_sum_paths(parent, values, target):
    # path totals stored per node; a counter of the totals above, entered and left on one stack
    n = len(parent)
    kids = [[] for _ in range(n)]
    root = parent.index(-1)
    for i, p in enumerate(parent):
        if p >= 0:
            kids[p].append(i)
    tot = [0] * n
    seen = Counter({0: 1})
    count = 0
    st = [root]
    tot[root] = values[root]
    state = [0] * n
    while st:
        u = st[-1]
        if state[u] == 0:
            state[u] = 1
            count += seen[tot[u] - target]
            seen[tot[u]] += 1
            for c in kids[u]:
                tot[c] = tot[u] + values[c]
                st.append(c)
        else:
            st.pop()
            seen[tot[u]] -= 1
    return count


def first_misplaced(book):
    # by the definition: check each level, in preorder, against every level above it
    st = [(book, ())]
    while st:
        node, above = st.pop()
        if node is None:
            continue
        p, l, r = node
        for q, went_left in above:
            if (went_left and not p < q) or (not went_left and not p > q):
                return p
        st.append((r, above + ((p, False),)))
        st.append((l, above + ((p, True),)))
    return None


def funded_projects(capital, k, projects):
    ps = sorted(projects, key=lambda p: p[0])
    i, n = 0, len(ps)
    open_ = []
    for _ in range(k):
        while i < n and ps[i][0] <= capital:
            heapq.heappush(open_, -ps[i][1]); i += 1
        if not open_:
            return capital
        capital += -heapq.heappop(open_)
    return capital


def funded_projects_brute(capital, k, projects):
    # the brief read literally, for the small cases
    left = list(projects)
    for _ in range(k):
        best = -1
        for j, (need, profit) in enumerate(left):
            if need <= capital and (best < 0 or profit > left[best][1]):
                best = j
        if best < 0:
            break
        capital += left.pop(best)[1]
    return capital


def compact_log(log, k):
    chars, counts = [], []
    for ch in log:
        if chars and chars[-1] == ch:
            counts[-1] += 1
            if counts[-1] == k:
                chars.pop(); counts.pop()
        else:
            chars.append(ch); counts.append(1)
    return ''.join(c * m for c, m in zip(chars, counts))


def spread_shifts(shifts):
    # the brief's rule read literally: scan the 26 initials for each slot
    left = [0] * 26
    for ch in shifts:
        left[ord(ch) - 97] += 1
    prev, out = -1, []
    for _ in range(len(shifts)):
        best = -1
        for i in range(26):
            if i != prev and left[i] > 0 and (best < 0 or left[i] > left[best]):
                best = i
        if best < 0:
            return ''
        left[best] -= 1
        out.append(chr(97 + best)); prev = best
    return ''.join(out)


def widest_ramp(prices):
    # days sorted by price (earlier day first on a tie); widest = day minus the earliest day so far
    best, first = 0, None
    for i in sorted(range(len(prices)), key=lambda i: (prices[i], i)):
        if first is None or i < first:
            first = i
        else:
            best = max(best, i - first)
    return best


def earliest_ready_day(ready, k, m):
    if k * m > len(ready):
        return -1
    days = sorted(set(ready))

    def ok(day):
        cnt = run = 0
        for r in ready:
            run = run + 1 if r <= day else 0
            if run == k:
                cnt += 1; run = 0
        return cnt >= m

    lo, hi = 0, len(days) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(days[mid]):
            hi = mid
        else:
            lo = mid + 1
    return days[lo]


def rebuild(pre, ino):
    where = {v: i for i, v in enumerate(ino)}

    def build(p, i, size):   # the part whose ids are pre[p:p+size] and ino[i:i+size]
        if size == 0:
            return None
        root = pre[p]
        ls = where[root] - i
        return (root, build(p + 1, i, ls), build(p + 1 + ls, where[root] + 1, size - ls - 1))

    return build(0, 0, len(pre))


def min_longest_gap(relays, k):
    gaps = [b - a for a, b in zip(relays, relays[1:])]
    lo, hi = 0, max(gaps)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if sum(-(-g // mid) - 1 for g in gaps) <= k:
            hi = mid
        else:
            lo = mid
    return hi


def right_edge_view(tree):
    # depth-first, right side first: the first value met at each depth
    view = []
    st = [(tree, 0)]
    while st:
        node, d = st.pop()
        if node is None:
            continue
        if d == len(view):
            view.append(node[0])
        st.append((node[1], d + 1))
        st.append((node[2], d + 1))
    return view


def prefix_stock(events):
    # a dict of totals keyed by every prefix of every code
    total, stock, out = {}, {}, []
    for e in events:
        if e[0] == 'set':
            code, cnt = e[1], e[2]
            ch = cnt - stock.get(code, 0)
            stock[code] = cnt
            for i in range(len(code) + 1):
                total[code[:i]] = total.get(code[:i], 0) + ch
        else:
            out.append(total.get(e[1], 0))
    return out


def solve_tray_queue(text):
    # one plain queue gives the ids; a serve that finds the out-tray empty moves every waiting ticket
    lines = [ln.split() for ln in text.split('\n') if ln.strip()]
    n = int(lines[0][0]) if lines else 0
    queue, in_out, moves, served = deque(), 0, 0, []
    for ln in lines[1:1 + n]:
        if ln[0] == 'in':
            queue.append(ln[1])
        else:
            if in_out == 0:
                moves += len(queue)
                in_out = len(queue)
            if in_out:
                served.append(queue.popleft()); in_out -= 1
            else:
                served.append('0')
    return str(moves) + '\n' + ' '.join(served)


def count_convoys(target, position, speed):
    # exact arrival times as fractions; a van's real arrival is the later of its own and the one ahead
    count, ahead = 0, None
    for p, s in sorted(zip(position, speed), reverse=True):
        t = Fraction(target - p, s)
        if ahead is None or t > ahead:
            count += 1
            ahead = t
    return count


def visible_masts(heights):
    # west to east: a new mast is seen by every shorter mast it pops and by the taller one left
    seen = [0] * len(heights)
    st = []
    for j, h in enumerate(heights):
        while st and heights[st[-1]] < h:
            seen[st.pop()] += 1
        if st:
            seen[st[-1]] += 1
        st.append(j)
    return seen
