"""Wrong or too-slow solutions the authors did not plant, ci packs 3 and 4.

Four candidates turned out to be right and are kept as a record, marked in their comment:
handoff_distances__wrap, solve_level_totals__floor, spread_shifts__precheck, count_convoys__float.
rebuild__slices is right too, and inside the height cap it is fast enough.

A name `fn__tag` is one candidate for the drill whose function is `fn`.
Run: harness.py wrong.py app/content/drills   (PASS here is a finding)
"""
import bisect
import heapq
import re
import sys
from collections import Counter, deque


# ---------- pack 3 ----------

def formula_value__sentinel(formula):
    # folds MAX and MIN from a "large enough" start of minus or plus 10**9
    stack = []
    for tok in re.findall(r"[A-Z]+|-?\d+|\)", formula):
        if tok == ")":
            args = []
            while not isinstance(stack[-1], str):
                args.append(stack.pop())
            name = stack.pop()
            if name == "SUM":
                v = sum(args)
            elif name == "MAX":
                v = -10 ** 9
                for a in args:
                    v = max(v, a)
            else:
                v = 10 ** 9
                for a in args:
                    v = min(v, a)
            stack.append(v)
        elif tok[0].isalpha():
            stack.append(tok)
        else:
            stack.append(int(tok))
    return stack[0]


def formula_value__deeprec(formula):
    # the planted recursive parser, with the recursion limit raised
    sys.setrecursionlimit(1000000)
    s = formula.replace(" ", "")
    pos = 0

    def parse():
        nonlocal pos
        if s[pos].isalpha():
            j = s.index("(", pos)
            name = s[pos:j]
            pos = j + 1
            args = [parse()]
            while s[pos] == ",":
                pos += 1
                args.append(parse())
            pos += 1
            return sum(args) if name == "SUM" else max(args) if name == "MAX" else min(args)
        j = pos + 1
        while j < len(s) and s[j].isdigit():
            j += 1
        v = int(s[pos:j])
        pos = j
        return v

    return parse()


def min_clear_rate__plus_one(queues, minutes):
    # q // r + 1 for the ceiling: one too many when r divides q
    lo, hi = 1, max(queues)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(q // mid + 1 for q in queues) <= minutes:
            hi = mid
        else:
            lo = mid + 1
    return lo


def largest_free_block__noflush(rows):
    # the stack is never emptied at the end of a row
    if not rows:
        return 0
    c = len(rows[0])
    up = [0] * c
    best = 0
    for row in rows:
        stack = []
        for j in range(c):
            up[j] = up[j] + 1 if row[j] == "." else 0
            left = j
            while stack and stack[-1][1] >= up[j]:
                left, top = stack.pop()
                best = max(best, top * (j - left))
            stack.append((left, up[j]))
    return best


def largest_free_block__rowpairs(rows):
    # every pair of rows, O(r^2 c) in bits: AND the rows as integers and read the longest run
    best = 0
    masks = [int(r.replace(".", "1").replace("#", "0"), 2) for r in rows]
    for top in range(len(masks)):
        m = masks[top]
        for bottom in range(top, len(masks)):
            m &= masks[bottom]
            if not m:
                break
            run = max(map(len, bin(m)[2:].split("0")))
            best = max(best, run * (bottom - top + 1))
    return best


def kth_smallest_gap__from_one(positions, k):
    # searches gaps from 1 up, forgetting that two sensors can share a mark
    p = sorted(positions)
    lo, hi = 1, p[-1] - p[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(bisect.bisect_right(p, x + mid, i + 1) - i - 1 for i, x in enumerate(p)) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_smallest_gap__heap(positions, k):
    # merge the n sorted runs of gaps with a heap: O(k log n)
    p = sorted(positions)
    heap = [(p[i + 1] - p[i], i, i + 1) for i in range(len(p) - 1)]
    heapq.heapify(heap)
    for _ in range(k - 1):
        g, i, j = heapq.heappop(heap)
        if j + 1 < len(p):
            heapq.heappush(heap, (p[j + 1] - p[i], i, j + 1))
    return heap[0][0]


def compact_log__lastk(log, k):
    # compares the last k letters at every step, stopping at the first that differs
    stack = []
    for ch in log:
        stack.append(ch)
        n = len(stack)
        if n >= k:
            i = 2
            while i <= k and stack[n - i] == ch:
                i += 1
            if i > k:
                del stack[n - k:]
    return "".join(stack)


def compact_log__replace(log, k):
    # rescans the log after each round of deletions
    runs = [ch * k for ch in "abcdefghijklmnopqrstuvwxyz"]
    changed = True
    while changed:
        changed = False
        for r in runs:
            if r in log:
                log = log.replace(r, "")
                changed = True
    return log


def widest_ramp__late_tie(prices):
    # sorts by price, later day first on a tie, so equal prices never pair up
    best = 0
    first = len(prices)
    for i in sorted(range(len(prices)), key=lambda i: (prices[i], -i)):
        if i > first:
            best = max(best, i - first)
        first = min(first, i)
    return best


def widest_ramp__pruned_pairs(prices):
    # every pair, but only from days lower than all before, and only wider than the best
    n = len(prices)
    best = 0
    low = None
    for i, p in enumerate(prices):
        if low is not None and p >= low:
            continue
        low = p
        for j in range(n - 1, i + best, -1):
            if prices[j] >= p:
                best = j - i
                break
    return best


def earliest_ready_day__no_reset(ready, k, m):
    # a down server does not break the run
    if m * k > len(ready):
        return -1

    def blocks(day):
        count = run = 0
        for r in ready:
            if r <= day:
                run += 1
                if run == k:
                    count += 1
                    run = 0
        return count

    lo, hi = min(ready), max(ready)
    while lo < hi:
        mid = (lo + hi) // 2
        if blocks(mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo


def min_longest_gap__average(relays, k):
    # spreads the route evenly over all the pieces, ignoring where the old relays stand
    pieces = len(relays) - 1 + k
    total = relays[-1] - relays[0]
    return max(1, -(-total // pieces))


def min_longest_gap__heap(relays, k):
    # right answer one relay at a time: O(k log n)
    heap = [(-(b - a), b - a, 1) for a, b in zip(relays, relays[1:])]
    heapq.heapify(heap)
    for _ in range(k):
        piece, g, parts = heap[0]
        if piece == -1:
            break
        heapq.heapreplace(heap, (-(-(-g // (parts + 1))), g, parts + 1))
    return -heap[0][0]


def find_in_ring__index(ring, targets):
    out = []
    for t in targets:
        try:
            out.append(ring.index(t))
        except ValueError:
            out.append(-1)
    return out


def ring_waits__walk(load):
    # walks forward from every slot
    n = len(load)
    out = []
    for i in range(n):
        wait = -1
        for step in range(1, n):
            if load[(i + step) % n] > load[i]:
                wait = step
                break
        out.append(wait)
    return out


def ring_waits__top_once(load):
    # walks forward from every slot, but answers -1 at once for the top reading
    n = len(load)
    top = max(load) if n else 0
    out = []
    for i in range(n):
        if load[i] == top:
            out.append(-1)
            continue
        step = 1
        while load[(i + step) % n] <= load[i]:
            step += 1
        out.append(step)
    return out


def solve_tick_ranges__lines(text):
    # reads lines 0, 1 and 2 as the brief lists them, with no thought for blank lines
    lines = text.split("\n")
    n, q = map(int, lines[0].split())
    ticks = list(map(int, lines[1].split()))
    out = []
    for t in map(int, lines[2].split()):
        lo = bisect.bisect_left(ticks, t)
        hi = bisect.bisect_right(ticks, t)
        out.append("%d %d" % (lo, hi - 1) if lo < hi else "-1 -1")
    return "\n".join(out)


def solve_tick_ranges__index(text):
    v = text.split()
    n, q = int(v[0]), int(v[1])
    ticks = v[2:2 + n]
    out = []
    for t in v[2 + n:2 + n + q]:
        if t in ticks:
            lo = ticks.index(t)
            out.append("%d %d" % (lo, lo + ticks.count(t) - 1))
        else:
            out.append("-1 -1")
    return "\n".join(out)


def solve_tray_queue__refills(text):
    # counts refills, not tickets moved
    words = text.split()
    n = int(words[0]) if words else 0
    in_tray, out_tray, served, moves = [], [], [], 0
    i = 1
    for _ in range(n):
        if words[i] == "in":
            in_tray.append(words[i + 1])
            i += 2
            continue
        i += 1
        if not out_tray and in_tray:
            out_tray = in_tray[::-1]
            in_tray = []
            moves += 1
        served.append(out_tray.pop() if out_tray else "0")
    return str(moves) + "\n" + " ".join(served)


def count_convoys__whole_hours(target, position, speed):
    # arrival times in whole hours
    convoys = 0
    slowest = -1
    for p, s in sorted(zip(position, speed), reverse=True):
        t = (target - p) // s
        if t > slowest:
            convoys += 1
            slowest = t
    return convoys


def count_convoys__float(target, position, speed):
    # float times: not wrong inside the stated ranges, run to confirm the tests agree
    convoys = 0
    slowest = -1.0
    for p, s in sorted(zip(position, speed), reverse=True):
        t = (target - p) / s
        if t > slowest:
            convoys += 1
            slowest = t
    return convoys


def visible_masts__stack_size(heights):
    # counts everything left on the stack, not just the one taller mast
    seen = [0] * len(heights)
    stack = []
    for i in range(len(heights) - 1, -1, -1):
        count = 0
        while stack and stack[-1] < heights[i]:
            stack.pop()
            count += 1
        seen[i] = count + len(stack)
        stack.append(heights[i])
    return seen


def visible_masts__look_east(heights):
    # looks east from every mast, stopping at the first taller one
    n = len(heights)
    seen = [0] * n
    for i in range(n):
        tallest = 0
        for j in range(i + 1, n):
            if heights[j] > tallest:
                seen[i] += 1
                tallest = heights[j]
                if tallest > heights[i]:
                    break
    return seen


def largest_block_area__own_edge(widths, heights):
    # a bar keeps its own left edge instead of the one it inherits from the bars it pops
    best = 0
    stack = []
    x = 0
    for w, h in zip(widths + [0], heights + [0]):
        while stack and stack[-1][1] >= h:
            left, top = stack.pop()
            best = max(best, top * (x - left))
        stack.append((x, h))
        x += w
    return best


# ---------- pack 4 ----------

def _kids(parent):
    kids = [[] for _ in parent]
    root = 0
    for i, p in enumerate(parent):
        if p < 0:
            root = i
        else:
            kids[p].append(i)
    return root, kids


def best_route_value__two_sweeps(parent, values):
    # the diameter trick: furthest depot from any start, then furthest from that one
    root, kids = _kids(parent)
    n = len(parent)

    def sweep(start):
        best = [None] * n
        best[start] = values[start]
        todo = [start]
        top = start
        while todo:
            v = todo.pop()
            if best[v] > best[top]:
                top = v
            near = list(kids[v])
            if parent[v] >= 0:
                near.append(parent[v])
            for u in near:
                if best[u] is None:
                    best[u] = best[v] + values[u]
                    todo.append(u)
        return top, best[top]

    a, _ = sweep(root)
    _, total = sweep(a)
    return total


def best_route_value__deeprec(parent, values):
    # plain recursion with the limit raised
    sys.setrecursionlimit(1000000)
    root, kids = _kids(parent)
    best = [values[root]]

    def down(v):
        gains = sorted((max(0, down(c)) for c in kids[v]), reverse=True)[:2]
        best[0] = max(best[0], values[v] + sum(gains))
        return values[v] + (gains[0] if gains else 0)

    down(root)
    return best[0]


def board_words__per_word(board, words):
    # one search per word, the method the drill calls too slow, with the two usual
    # prunings: letter counts, and starting from the rarer end
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


def board_words__per_word_counts(board, words):
    # one search per word with the letter-count check only
    rows = len(board)
    cols = len(board[0]) if rows else 0
    have = Counter("".join(board))
    grid = [list(r) for r in board]

    def trace(word):
        if any(have[ch] < c for ch, c in Counter(word).items()):
            return False
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


def busiest_links__any_case(trips, k):
    # "alphabetical" read as a dictionary reads it, ignoring case
    counts = Counter()
    for a, b in trips:
        counts["-".join(sorted((a, b), key=str.lower))] += 1
    return sorted(counts, key=lambda name: (-counts[name], name.lower()))[:k]


def cheapest_pairs__distinct(a, b, k):
    # treats equal costs in a list as one leg
    a, b = sorted(set(a)), sorted(set(b))
    if not a or not b:
        return []
    heap = [(x + b[0], i, 0) for i, x in enumerate(a[:k])]
    heapq.heapify(heap)
    out = []
    while heap and len(out) < k:
        cost, i, j = heapq.heappop(heap)
        out.append(cost)
        if j + 1 < len(b):
            heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
    return out


def cheapest_pairs__square(a, b, k):
    # prices only the first k of each list, then sorts: O(k^2)
    return sorted(x + y for x in a[:k] for y in b[:k])[:k]


def count_sum_paths__set(parent, values, target):
    # remembers which totals are on the path, not how many times each
    root, kids = _kids(parent)
    seen = {0}
    count = 0
    stack = [(root, 0, False, False)]
    while stack:
        node, total, leaving, added = stack.pop()
        if leaving:
            if added:
                seen.discard(total)
            continue
        total += values[node]
        if total - target in seen:
            count += 1
        added = total not in seen
        seen.add(total)
        stack.append((node, total, True, added))
        for c in kids[node]:
            stack.append((c, total, False, False))
    return count


def first_misplaced__level_order(book):
    # right bounds, but read level by level instead of in preorder
    todo = deque([(book, None, None)])
    while todo:
        node, lo, hi = todo.popleft()
        if node is None:
            continue
        price, left, right = node
        if (lo is not None and price <= lo) or (hi is not None and price >= hi):
            return price
        todo.append((left, lo, price))
        todo.append((right, price, hi))
    return None


def funded_projects__one_a_round(capital, k, projects):
    # opens at most one newly affordable project before each choice
    order = sorted(projects)
    ready = []
    i = 0
    for _ in range(k):
        if i < len(order) and order[i][0] <= capital:
            heapq.heappush(ready, -order[i][1])
            i += 1
        if not ready:
            break
        capital -= heapq.heappop(ready)
    return capital


def funded_projects__reuse(capital, k, projects):
    # best affordable profit by a prefix maximum, never marking a project used
    order = sorted(projects)
    needs = [p[0] for p in order]
    top = []
    for _, profit in order:
        top.append(max(profit, top[-1]) if top else profit)
    for _ in range(k):
        i = bisect.bisect_right(needs, capital)
        if i == 0:
            break
        capital += top[i - 1]
    return capital


def handoff_distances__wrap(parent, queries):
    # jump tables keep -1 above the root, which Python reads as the last desk.
    # PASSES and is right after all: a jump past the root lands on a value that depends
    # only on the level and the depth, so two desks of equal depth still compare equal.
    n = len(parent)
    root, kids = _kids(parent)
    depth = [0] * n
    order = [root]
    for v in order:
        for c in kids[v]:
            depth[c] = depth[v] + 1
            order.append(c)
    up = [list(parent)]
    for _ in range(max(1, n.bit_length()) - 1):
        prev = up[-1]
        up.append([prev[prev[v]] for v in range(n)])
    out = []
    for a, b in queries:
        da, db = depth[a], depth[b]
        if da < db:
            a, b = b, a
        gap, k = abs(da - db), 0
        while gap:
            if gap & 1:
                a = up[k][a]
            gap >>= 1
            k += 1
        if a != b:
            for k in range(len(up) - 1, -1, -1):
                if up[k][a] != up[k][b]:
                    a, b = up[k][a], up[k][b]
            a = up[0][a]
        out.append(da + db - 2 * depth[a])
    return out


def handoff_distances__climb(parent, queries):
    # one line at a time, the obvious method, written tightly
    n = len(parent)
    root, kids = _kids(parent)
    depth = [0] * n
    order = [root]
    for v in order:
        for c in kids[v]:
            depth[c] = depth[v] + 1
            order.append(c)
    out = []
    for a, b in queries:
        steps = 0
        while a != b:
            if depth[a] < depth[b]:
                a, b = b, a
            a = parent[a]
            steps += 1
        out.append(steps)
    return out


def solve_level_totals__floor(text):
    # starts the best total at the lowest single balance, -10**9.
    # PASSES and is right after all: level 1 is one balance, so the best total is never below -10**9.
    nums = [int(t) for t in text.split()]
    n = nums[0]
    parent, balance = nums[1:1 + n], nums[1 + n:1 + 2 * n]
    root, kids = _kids(parent)
    best_level, best_total = 1, -10 ** 9
    level, row = 1, [root]
    while row:
        total = sum(balance[i] for i in row)
        if total > best_total:
            best_level, best_total = level, total
        row = [c for i in row for c in kids[i]]
        level += 1
    return "%d %d" % (best_level, best_total)


def solve_live_median__insort(text):
    # one sorted list, insort and del: the method the brief names as too slow
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


def solve_live_median__eager_heaps(text):
    # two heaps, but a cancel removes from the heap at once with list.remove and heapify
    tokens = text.split()
    q = int(tokens[0]) if tokens else 0
    low, high = [], []
    out = []
    for i in range(q):
        x = int(tokens[2 + 2 * i])
        if tokens[1 + 2 * i] == "+":
            if low and x <= -low[0]:
                heapq.heappush(low, -x)
            else:
                heapq.heappush(high, x)
        elif low and x <= -low[0]:
            low.remove(-x)
            heapq.heapify(low)
        else:
            high.remove(x)
            heapq.heapify(high)
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(low) < len(high):
            heapq.heappush(low, -heapq.heappop(high))
        out.append(str(-low[0]) if low else "-")
    return " ".join(out)


def spread_shifts__first_seen(shifts):
    # breaks a tie by who appears first in the bag, not by the alphabet
    left = Counter(shifts)
    names = list(left)
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


def spread_shifts__precheck(shifts):
    # decides "no rota" by the usual count test alone, then never checks again.
    # PASSES and is right: the count test is exact, and holding the last person back is the same rule.
    left = Counter(shifts)
    if left and max(left.values()) > (len(shifts) + 1) // 2:
        return ""
    heap = [(-c, ch) for ch, c in left.items()]
    heapq.heapify(heap)
    rota = []
    held = None
    while heap:
        c, ch = heapq.heappop(heap)
        rota.append(ch)
        if held:
            heapq.heappush(heap, held)
        held = (c + 1, ch) if c + 1 < 0 else None
    return "".join(rota)


def read_tree__digits(text):
    # tells a value from a mark with isdigit, which is false for a negative number
    tokens = text.split()
    pos = 0

    def build():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if not tok.isdigit():
            return None
        left = build()
        right = build()
        return (int(tok), left, right)

    return build()


def read_tree__pop_front(text):
    # takes each token off the front of the list: O(n^2) moves
    tokens = text.split()

    def build():
        tok = tokens.pop(0)
        if tok == "#":
            return None
        left = build()
        right = build()
        return (int(tok), left, right)

    return build()


def rebuild__global_split(pre, ino):
    # cuts `pre` by the root's place in the whole of `ino`, right only on the left spine
    where = {v: i for i, v in enumerate(ino)}

    def build(p_lo, p_hi, i_lo, i_hi):
        if p_lo >= p_hi:
            return None
        root = pre[p_lo]
        mid = where[root]
        return (root, build(p_lo + 1, mid + 1, i_lo, mid), build(mid + 1, p_hi, mid + 1, i_hi))

    return build(0, len(pre), 0, len(ino))


def rebuild__slices(pre, ino):
    # list.index and slices at every node: O(n h)
    if not pre:
        return None
    mid = ino.index(pre[0])
    return (pre[0], rebuild__slices(pre[1:mid + 1], ino[:mid]), rebuild__slices(pre[mid + 1:], ino[mid + 1:]))


def right_edge_view__last_write(tree):
    # depth-first with a stack, left pushed first, so the left node is written last
    view = {}
    stack = [(tree, 0)]
    while stack:
        node, d = stack.pop()
        if node is None:
            continue
        view[d] = node[0]
        stack.append((node[1], d + 1))
        stack.append((node[2], d + 1))
    return [view[d] for d in sorted(view)]


def prefix_stock__short_prefixes(events):
    # totals for every proper prefix, forgetting that a code starts with itself
    total = Counter()
    stock = {}
    out = []
    for e in events:
        if e[0] == "set":
            change = e[2] - stock.get(e[1], 0)
            stock[e[1]] = e[2]
            for cut in range(len(e[1])):
                total[e[1][:cut]] += change
        else:
            out.append(total[e[1]] if e[1] in total else 0)
    return out


def prefix_stock__sorted_scan(events):
    # codes in a sorted list; an ask bisects to the prefix and adds up every match
    codes = []
    stock = {}
    out = []
    for e in events:
        if e[0] == "set":
            if e[1] not in stock:
                bisect.insort(codes, e[1])
            stock[e[1]] = e[2]
        else:
            p = e[1]
            i = bisect.bisect_left(codes, p)
            total = 0
            while i < len(codes) and codes[i].startswith(p):
                total += stock[codes[i]]
                i += 1
            out.append(total)
    return out
