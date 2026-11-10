"""Second reader's own solutions to the 30 drills of ci packs 3 and 4.

Written from the brief and constraints alone, by a method other than the model's
wherever one exists. Run: harness.py mine.py app/content/drills
"""
import bisect
import heapq
import re
from collections import Counter, deque
from fractions import Fraction


# ---------- pack 3 ----------

def formula_value(formula):
    # flat token stack: names and numbers; a closing bracket folds back to its name
    stack = []
    for tok in re.findall(r"[A-Z]+|-?\d+|\)", formula):
        if tok == ")":
            args = []
            while not isinstance(stack[-1], str):
                args.append(stack.pop())
            name = stack.pop()
            stack.append({"SUM": sum, "MAX": max, "MIN": min}[name](args))
        elif tok[0].isalpha():
            stack.append(tok)
        else:
            stack.append(int(tok))
    return stack[0]


def min_clear_rate(queues, minutes):
    def need(r):
        return sum(-(-q // r) for q in queues)
    lo = max(1, -(-sum(queues) // minutes))  # no slower rate can do it
    hi = max(queues)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= minutes:
            hi = mid
        else:
            lo = mid + 1
    return lo


def largest_free_block(rows):
    # per row: height, and how far left and right that height can stretch (no stack)
    if not rows:
        return 0
    c = len(rows[0])
    height = [0] * c
    left = [0] * c
    right = [c] * c
    best = 0
    for row in rows:
        edge = 0
        for j in range(c):
            if row[j] == ".":
                height[j] += 1
                left[j] = max(left[j], edge)
            else:
                height[j] = 0
                left[j] = 0
                edge = j + 1
        edge = c
        for j in range(c - 1, -1, -1):
            if row[j] == ".":
                right[j] = min(right[j], edge)
                best = max(best, height[j] * (right[j] - left[j]))
            else:
                right[j] = c
                edge = j
    return best


def kth_smallest_gap(positions, k):
    p = sorted(positions)
    n = len(p)

    def within(d):
        return sum(bisect.bisect_right(p, x + d, i + 1) - i - 1 for i, x in enumerate(p))

    lo, hi = -1, p[-1] - p[0]  # within(lo) < k <= within(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if within(mid) >= k:
            hi = mid
        else:
            lo = mid
    return hi


def compact_log(log, k):
    letters, counts = [], []
    for ch in log:
        if letters and letters[-1] == ch:
            counts[-1] += 1
        else:
            letters.append(ch)
            counts.append(1)
        if counts[-1] == k:
            letters.pop()
            counts.pop()
    return "".join(ch * c for ch, c in zip(letters, counts))


def widest_ramp(prices):
    # visit days from the lowest price up (earlier day first on a tie); the earliest
    # day visited so far is the best start for each
    best = 0
    first = len(prices)
    for i in sorted(range(len(prices)), key=lambda i: (prices[i], i)):
        if i > first:
            best = max(best, i - first)
        first = min(first, i)
    return best


def earliest_ready_day(ready, k, m):
    days = sorted(set(ready))

    def blocks(day):
        total = run = 0
        for r in ready:
            if r <= day:
                run += 1
            else:
                total += run // k
                run = 0
        return total + run // k

    if blocks(days[-1]) < m:
        return -1
    lo, hi = 0, len(days) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if blocks(days[mid]) >= m:
            hi = mid
        else:
            lo = mid + 1
    return days[lo]


def min_longest_gap(relays, k):
    gaps = [relays[i + 1] - relays[i] for i in range(len(relays) - 1)]

    def extra(length):
        return sum(-(-g // length) - 1 for g in gaps)

    lo, hi = 0, max(gaps)  # extra(hi) = 0 <= k; lo is never feasible
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if extra(mid) <= k:
            hi = mid
        else:
            lo = mid
    return hi


def find_in_ring(ring, targets):
    # no search at all: one dict
    at = {v: i for i, v in enumerate(ring)}
    return [at.get(t, -1) for t in targets]


def ring_waits(load):
    n = len(load)
    if n == 0:
        return []
    top = max(load)
    m = load.index(top)
    waits = [-1] * n
    stack = []  # (unrolled position, reading), read backwards from the top slot
    for t in range(n - 1, -1, -1):  # arr = load[m+1:] + load[:m+1], top reading last
        i = (m + 1 + t) % n
        x = load[i]
        while stack and stack[-1][1] <= x:
            stack.pop()
        if x != top:
            waits[i] = stack[-1][0] - t
        stack.append((t, x))
    return waits


def solve_tick_ranges(text):
    v = text.split()
    n, q = int(v[0]), int(v[1])
    first, last = {}, {}
    for i, t in enumerate(v[2:2 + n]):
        t = int(t)
        first.setdefault(t, i)
        last[t] = i
    out = []
    for t in v[2 + n:2 + n + q]:
        t = int(t)
        out.append("%d %d" % (first[t], last[t]) if t in first else "-1 -1")
    return "\n".join(out)


def solve_tray_queue(text):
    lines = [ln.split() for ln in text.split("\n") if ln.strip()]
    n = int(lines[0][0]) if lines else 0
    queue = deque()
    in_size = out_size = moves = 0
    served = []
    for parts in lines[1:1 + n]:
        if parts[0] == "in":
            queue.append(parts[1])
            in_size += 1
        else:
            if out_size == 0:
                moves += in_size
                out_size, in_size = in_size, 0
            if out_size:
                served.append(queue.popleft())
                out_size -= 1
            else:
                served.append("0")
    return "%d\n%s" % (moves, " ".join(served))


def count_convoys(target, position, speed):
    convoys = 0
    slowest = Fraction(-1)
    for p, s in sorted(zip(position, speed), reverse=True):
        t = Fraction(target - p, s)
        if t > slowest:
            convoys += 1
            slowest = t
    return convoys


def visible_masts(heights):
    # west to east: a new mast is seen by every shorter mast it pops and by the taller one left
    seen = [0] * len(heights)
    stack = []
    for j, h in enumerate(heights):
        while stack and heights[stack[-1]] < h:
            seen[stack.pop()] += 1
        if stack:
            seen[stack[-1]] += 1
        stack.append(j)
    return seen


def largest_block_area(widths, heights):
    n = len(heights)
    edge = [0] * (n + 1)
    for i, w in enumerate(widths):
        edge[i + 1] = edge[i] + w
    lower_left = [-1] * n   # nearest bar to the left that is strictly lower
    for i in range(n):
        j = i - 1
        while j >= 0 and heights[j] >= heights[i]:
            j = lower_left[j]
        lower_left[i] = j
    lower_right = [n] * n
    for i in range(n - 1, -1, -1):
        j = i + 1
        while j < n and heights[j] >= heights[i]:
            j = lower_right[j]
        lower_right[i] = j
    best = 0
    for i in range(n):
        best = max(best, heights[i] * (edge[lower_right[i]] - edge[lower_left[i] + 1]))
    return best


# ---------- pack 4 ----------

def _depths(parent):
    n = len(parent)
    depth = [-1] * n
    for i in range(n):
        path = []
        v = i
        while v >= 0 and depth[v] < 0:
            path.append(v)
            v = parent[v]
        d = depth[v] if v >= 0 else -1
        for u in reversed(path):
            d += 1
            depth[u] = d
    return depth


def best_route_value(parent, values):
    # deepest nodes first, each pushing its best downward total up to its parent
    n = len(parent)
    depth = _depths(parent)
    one = [0] * n
    two = [0] * n
    best = max(values)
    for v in sorted(range(n), key=lambda v: -depth[v]):
        down = values[v] + one[v]
        best = max(best, values[v] + one[v] + two[v])
        p = parent[v]
        if p >= 0 and down > 0:
            if down > one[p]:
                one[p], two[p] = down, one[p]
            elif down > two[p]:
                two[p] = down
    return best


def board_words(board, words):
    # one search per word, with the usual two prunings: letter counts, and
    # starting from the rarer end of the word
    rows = len(board)
    cols = len(board[0]) if rows else 0
    have = Counter("".join(board))
    grid = [list(r) for r in board]

    def trace(word):
        need = Counter(word)
        if any(have[ch] < c for ch, c in need.items()):
            return False
        if have[word[0]] > have[word[-1]]:
            word = word[::-1]
        last = len(word) - 1

        def go(r, c, i):
            if grid[r][c] != word[i]:
                return False
            if i == last:
                return True
            grid[r][c] = "."
            ok = False
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and go(nr, nc, i + 1):
                    ok = True
                    break
            grid[r][c] = word[i]
            return ok

        return any(go(r, c, 0) for r in range(rows) for c in range(cols))

    return sorted(w for w in words if trace(w))


def busiest_links(trips, k):
    counts = Counter("-".join(sorted(t)) for t in trips)
    return sorted(counts, key=lambda name: (-counts[name], name))[:k]


def cheapest_pairs(a, b, k):
    # binary search the k-th cost, then list every trade below it and pad with it
    if k == 0 or not a or not b:
        return []

    def at_most(v):
        total = 0
        j = len(b)
        for x in a:
            while j and x + b[j - 1] > v:
                j -= 1
            if j == 0:
                break
            total += j
        return total

    lo, hi = a[0] + b[0] - 1, a[-1] + b[-1]
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if at_most(mid) >= k:
            hi = mid
        else:
            lo = mid
    out = []
    for x in a:
        if x + b[0] >= hi:
            break
        for y in b:
            if x + y >= hi:
                break
            out.append(x + y)
    out.sort()
    return out + [hi] * (k - len(out))


def count_sum_paths(parent, values, target):
    # preorder by index lists; keep the totals on the current root path in a list
    # and a Counter, and unwind both when the walk moves to another branch
    n = len(parent)
    kids = [[] for _ in range(n)]
    root = parent.index(-1)
    for i, p in enumerate(parent):
        if p >= 0:
            kids[p].append(i)
    depth = _depths(parent)
    seen = Counter({0: 1})
    path = [0]  # running totals; path[d + 1] is the total at the node of depth d
    count = 0
    todo = [root]
    while todo:
        v = todo.pop()
        while len(path) > depth[v] + 1:
            seen[path.pop()] -= 1
        total = path[-1] + values[v]
        count += seen[total - target]
        seen[total] += 1
        path.append(total)
        todo.extend(kids[v])
    return count


def first_misplaced(book):
    def walk(node, lo, hi):
        if node is None:
            return None
        price, left, right = node
        if not (lo < price < hi):
            return (price,)
        return walk(left, lo, price) or walk(right, price, hi)

    hit = walk(book, float("-inf"), float("inf"))
    return hit[0] if hit else None


def funded_projects(capital, k, projects):
    locked = [(need, profit) for need, profit in projects]
    heapq.heapify(locked)
    open_profits = []
    done = 0
    while done < k:
        while locked and locked[0][0] <= capital:
            heapq.heappush(open_profits, -heapq.heappop(locked)[1])
        if not open_profits:
            break
        capital += -heapq.heappop(open_profits)
        done += 1
    return capital


def handoff_distances(parent, queries):
    # Euler tour and a sparse table of the shallowest node between two first visits
    n = len(parent)
    kids = [[] for _ in range(n)]
    root = parent.index(-1)
    for i, p in enumerate(parent):
        if p >= 0:
            kids[p].append(i)
    depth = _depths(parent)
    first = [0] * n
    tour = []
    stack = [(root, 0)]
    while stack:
        v, i = stack.pop()
        if i == 0:
            first[v] = len(tour)
        tour.append(depth[v])
        if i < len(kids[v]):
            stack.append((v, i + 1))
            stack.append((kids[v][i], 0))
    table = [tour]
    span = 1
    while 2 * span <= len(tour):
        prev = table[-1]
        table.append([min(prev[i], prev[i + span]) for i in range(len(tour) - 2 * span + 1)])
        span *= 2
    out = []
    for a, b in queries:
        lo, hi = sorted((first[a], first[b]))
        j = (hi - lo + 1).bit_length() - 1
        low = min(table[j][lo], table[j][hi - (1 << j) + 1])
        out.append(depth[a] + depth[b] - 2 * low)
    return out


def solve_level_totals(text):
    nums = list(map(int, text.split()))
    n = nums[0]
    parent, balance = nums[1:1 + n], nums[1 + n:1 + 2 * n]
    depth = _depths(parent)
    totals = [0] * (max(depth) + 1)
    for d, bal in zip(depth, balance):
        totals[d] += bal
    top = max(totals)
    return "%d %d" % (totals.index(top) + 1, top)


def solve_live_median(text):
    # the method the drill says is too slow: one sorted list, insort and del
    tokens = text.split()
    q = int(tokens[0]) if tokens else 0
    live = []
    out = []
    for i in range(q):
        x = int(tokens[2 + 2 * i])
        if tokens[1 + 2 * i] == "+":
            bisect.insort(live, x)
        else:
            del live[bisect.bisect_left(live, x)]
        out.append(str(live[(len(live) + 1) // 2 - 1]) if live else "-")
    return " ".join(out)


def spread_shifts(shifts):
    # the rule as written, by scanning the letters for each slot
    left = Counter(shifts)
    names = sorted(left)
    rota = []
    prev = None
    for _ in range(len(shifts)):
        pick = None
        for ch in names:
            if ch != prev and left[ch] and (pick is None or left[ch] > left[pick]):
                pick = ch
        if pick is None:
            return ""
        rota.append(pick)
        left[pick] -= 1
        prev = pick
    return "".join(rota)


def read_tree(text):
    # read the tokens backwards: a value then finds its two parts on top of a stack
    stack = []
    for tok in reversed(text.split()):
        if tok == "#":
            stack.append(None)
        else:
            left = stack.pop()
            right = stack.pop()
            stack.append((int(tok), left, right))
    return stack[0]


def rebuild(pre, ino):
    # no dict: the left part ends where `ino` reaches the id that stops it
    n = len(pre)
    p = i = 0

    def build(stop):
        nonlocal p, i
        if i < n and ino[i] != stop:
            root = pre[p]
            p += 1
            left = build(root)
            i += 1
            right = build(stop)
            return (root, left, right)
        return None

    return build(object())


def right_edge_view(tree):
    view = []

    def walk(node, depth):
        if node is None:
            return
        if depth == len(view):
            view.append(node[0])
        walk(node[2], depth + 1)
        walk(node[1], depth + 1)

    walk(tree, 0)
    return view


def prefix_stock(events):
    total = Counter()
    stock = {}
    out = []
    for e in events:
        if e[0] == "set":
            code, count = e[1], e[2]
            change = count - stock.get(code, 0)
            stock[code] = count
            for cut in range(len(code) + 1):
                total[code[:cut]] += change
        else:
            out.append(total[e[1]] if e[1] in total else 0)
    return out
