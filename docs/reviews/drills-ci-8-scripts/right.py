"""Right solutions in other styles, to see that none is refused (harness.py right.py <drills dir>),
to time in Pyodide (pyo_time.py) and to probe for recursion depth (depth.py, page_probe.py).
My own solutions in mine.py are fifteen more (sliding minimum for loop starts and stone hops,
score order for ring bonuses)."""
C = {}


def add(label, did, comment, code):
    C[label] = (did, code, comment)


add('R_bonus_memo_recursion', 'ci-ring-bonuses', 'remembered recursion: one more than the largest lower neighbour', '''
import sys
from functools import lru_cache
sys.setrecursionlimit(1000000)

def ring_bonuses(scores):
    n = len(scores)

    @lru_cache(maxsize=None)
    def need(i):
        best = 1
        for j in ((i - 1) % n, (i + 1) % n):
            if scores[j] < scores[i]:
                best = max(best, need(j) + 1)
        return best
    return sum(need(i) for i in range(n))
''')
add('R_bonus_memo_dict_recursion', 'ci-ring-bonuses', 'the same with a dict, no lru_cache', '''
import sys
sys.setrecursionlimit(1000000)

def ring_bonuses(scores):
    n = len(scores)
    memo = {}

    def need(i):
        if i in memo:
            return memo[i]
        best = 1
        for j in ((i - 1) % n, (i + 1) % n):
            if scores[j] < scores[i]:
                best = max(best, need(j) + 1)
        memo[i] = best
        return best
    return sum(need(i) for i in range(n))
''')
add('R_bonus_sweeps_both_ways', 'ci-ring-bonuses', 'forward and backward sweeps round the table in turn until nothing changes', '''
def ring_bonuses(scores):
    n = len(scores)
    t = [1] * n
    changed = True
    while changed:
        changed = False
        for i in list(range(n)) + list(range(n - 1, -1, -1)):
            for j in ((i - 1) % n, (i + 1) % n):
                if scores[i] > scores[j] and t[i] <= t[j]:
                    t[i] = t[j] + 1
                    changed = True
    return sum(t)
''')
add('R_stop_recursive_fire', 'ci-stop-cascade', 'a buy fires the stops it sets off from inside itself', '''
import heapq

def solve_stop_cascade(text):
    tokens = text.split()
    n = int(tokens[0])
    asks, stops = [], []
    state = {'last': None, 'vol': 0}
    out = []

    def fire():
        if stops and state['last'] is not None and stops[0][0] <= state['last']:
            buy(heapq.heappop(stops)[2])

    def buy(qty):
        while qty > 0 and asks:
            best = asks[0]
            take = min(qty, best[2])
            qty -= take
            best[2] -= take
            state['vol'] += take
            state['last'] = best[0]
            if best[2] == 0:
                heapq.heappop(asks)
        fire()

    pos = 1
    for seq in range(n):
        kind = tokens[pos]
        if kind == 'B':
            buy(int(tokens[pos + 1]))
            pos += 2
        else:
            price, qty = int(tokens[pos + 1]), int(tokens[pos + 2])
            if kind == 'S':
                heapq.heappush(asks, [price, seq, qty])
            else:
                heapq.heappush(stops, (price, seq, qty))
                fire()
            pos += 3
        out.append('- 0' if state['last'] is None else '%d %d' % (state['last'], state['vol']))
    return '\\n'.join(out)
''')
add('R_stop_bisect_lists', 'ci-stop-cascade', 'book and stops as sorted lists kept with insort, taken from the front with pop(0)', '''
from bisect import insort

def solve_stop_cascade(text):
    lines = [ln.split() for ln in text.split('\\n') if ln.strip()]
    n = int(lines[0][0])
    asks, stops = [], []
    last, vol = None, 0
    out = []
    for seq in range(1, n + 1):
        ev = lines[seq]
        q = 0
        if ev[0] == 'S':
            insort(asks, [int(ev[1]), seq, int(ev[2])])
        elif ev[0] == 'T':
            insort(stops, (int(ev[1]), seq, int(ev[2])))
        else:
            q = int(ev[1])
        while True:
            while q and asks:
                a = asks[0]
                take = min(q, a[2])
                q -= take
                a[2] -= take
                vol += take
                last = a[0]
                if not a[2]:
                    asks.pop(0)
            if stops and last is not None and stops[0][0] <= last:
                q = stops.pop(0)[2]
            else:
                break
        out.append('- 0' if last is None else '%d %d' % (last, vol))
    return '\\n'.join(out)
''')
add('R_stop_bisect_falling', 'ci-stop-cascade', 'the same, the lists kept in falling order so the cheapest is popped from the end', '''
from bisect import insort

def solve_stop_cascade(text):
    lines = [ln.split() for ln in text.split('\\n') if ln.strip()]
    n = int(lines[0][0])
    asks, stops = [], []
    last, vol = None, 0
    out = []
    for seq in range(1, n + 1):
        ev = lines[seq]
        q = 0
        if ev[0] == 'S':
            insort(asks, [-int(ev[1]), seq, int(ev[2])])
        elif ev[0] == 'T':
            insort(stops, (-int(ev[1]), seq, int(ev[2])))
        else:
            q = int(ev[1])
        while True:
            while q and asks:
                a = asks[-1]
                take = min(q, a[2])
                q -= take
                a[2] -= take
                vol += take
                last = -a[0]
                if not a[2]:
                    asks.pop()
            if stops and last is not None and -stops[-1][0] <= last:
                q = stops.pop()[2]
            else:
                break
        out.append('- 0' if last is None else '%d %d' % (last, vol))
    return '\\n'.join(out)
''')
add('R_rooms_bisect_free', 'ci-room-numbers', 'busy rooms in a heap, free rooms in a sorted list kept with insort, pop(0)', '''
import heapq
from bisect import insort

def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: meetings[i][0])
    free, busy, opened = [], [], 0
    rooms = [0] * len(meetings)
    for i in order:
        s, e = meetings[i]
        while busy and busy[0][0] <= s:
            insort(free, heapq.heappop(busy)[1])
        if free:
            room = free.pop(0)
        else:
            room, opened = opened, opened + 1
        rooms[i] = room
        heapq.heappush(busy, (e + clean, room))
    return rooms
''')
add('R_rooms_bisect_both', 'ci-room-numbers', 'busy and free both sorted lists kept with insort, both taken with pop(0)', '''
from bisect import insort

def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: meetings[i][0])
    free, busy, opened = [], [], 0
    rooms = [0] * len(meetings)
    for i in order:
        s, e = meetings[i]
        while busy and busy[0][0] <= s:
            insort(free, busy.pop(0)[1])
        if free:
            room = free.pop(0)
        else:
            room, opened = opened, opened + 1
        rooms[i] = room
        insort(busy, (e + clean, room))
    return rooms
''')
add('R_rooms_sorted_each_time', 'ci-room-numbers', 'free rooms in a list, sorted again after each release', '''
import heapq

def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: meetings[i][0])
    free, busy, opened = [], [], 0
    rooms = [0] * len(meetings)
    for i in order:
        s, e = meetings[i]
        moved = False
        while busy and busy[0][0] <= s:
            free.append(heapq.heappop(busy)[1])
            moved = True
        if moved:
            free.sort(reverse=True)
        if free:
            room = free.pop()
        else:
            room, opened = opened, opened + 1
        rooms[i] = room
        heapq.heappush(busy, (e + clean, room))
    return rooms
''')
add('R_switch_bfs', 'ci-switch-panel', 'breadth-first search over lamp patterns, switches tried in number order, the set sorted', '''
from collections import deque

def fewest_switches(switches, target):
    want = int(target, 2)
    masks = [int(s, 2) for s in switches]
    seen = {0: ()}
    q = deque([0])
    while q:
        s = q.popleft()
        if s == want:
            return sorted(seen[s])
        for i, m in enumerate(masks):
            if i not in seen[s] and s ^ m not in seen:
                seen[s ^ m] = seen[s] + (i,)
                q.append(s ^ m)
    return None
''')
add('R_switch_recursive_subsets', 'ci-switch-panel', 'recursion that grows a set to a fixed size, sizes in turn', '''
def fewest_switches(switches, target):
    want = int(target, 2)
    masks = [int(s, 2) for s in switches]
    n = len(masks)

    def grow(first, left, lit, pick):
        if left == 0:
            return list(pick) if lit == want else None
        for i in range(first, n - left + 1):
            pick.append(i)
            got = grow(i + 1, left - 1, lit ^ masks[i], pick)
            if got is not None:
                return got
            pick.pop()
        return None
    for size in range(n + 1):
        got = grow(0, size, 0, [])
        if got is not None:
            return got
    return None
''')
add('R_kbits_digit_dp', 'ci-k-bit-count', 'digit recursion with lru_cache on (bit, set bits left, tight)', '''
from functools import lru_cache

def count_k_bits(queries):
    def upto(n, k):
        if n < 0:
            return 0

        @lru_cache(maxsize=None)
        def go(b, left, tight):
            if left < 0:
                return 0
            if b < 0:
                return 1 if left == 0 else 0
            top = (n >> b & 1) if tight else 1
            return sum(go(b - 1, left - d, tight and d == top) for d in range(top + 1))
        return go(59, k, True)
    return [upto(hi, k) - upto(lo - 1, k) for lo, hi, k in queries]
''')
add('R_hops_union_find', 'ci-stone-hops', 'breadth-first search with a next-unvisited pointer per place (union-find)', '''
from collections import deque

def fewest_hops(stones, lo, hi):
    n = len(stones)
    nxt = list(range(n + 1))

    def find(x):
        root = x
        while nxt[root] != root:
            root = nxt[root]
        while nxt[x] != root:
            nxt[x], x = root, nxt[x]
        return root
    dist = [-1] * n
    dist[0] = 0
    nxt[0] = 1
    q = deque([0])
    while q:
        i = q.popleft()
        if i == n - 1:
            return dist[i]
        j = find(min(i + lo, n))
        while j <= min(i + hi, n - 1):
            if stones[j] == '.':
                dist[j] = dist[i] + 1
                q.append(j)
            nxt[j] = j + 1
            j = find(j + 1)
    return -1
''')
add('R_hops_sorted_unvisited', 'ci-stone-hops', 'stones not yet reached in a sorted list; each window cut out with bisect and del', '''
from bisect import bisect_left, bisect_right
from collections import deque

def fewest_hops(stones, lo, hi):
    n = len(stones)
    left = [i for i in range(1, n) if stones[i] == '.']
    dist = {0: 0}
    q = deque([0])
    while q:
        i = q.popleft()
        if i == n - 1:
            return dist[i]
        a, b = bisect_left(left, i + lo), bisect_right(left, i + hi)
        for j in left[a:b]:
            dist[j] = dist[i] + 1
            q.append(j)
        del left[a:b]
    return -1
''')
add('R_checks_mirror', 'ci-double-checks', 'the mirror image: jobs by start, latest first, visits placed as early as possible', '''
from bisect import bisect_left, bisect_right, insort

def fewest_checks(jobs):
    marks = []
    used = set()
    for start, end, need in sorted(jobs, key=lambda j: -j[0]):
        have = bisect_right(marks, end) - bisect_left(marks, start)
        m = start
        while have < need:
            if m not in used:
                used.add(m)
                insort(marks, m)
                have += 1
            m += 1
    return len(marks)
''')
add('R_rings_deque_rotate', 'ci-ring-turns', 'each ring read into a deque and turned with rotate(k)', '''
from collections import deque

def turn_rings(grid, k):
    rows, cols = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for t in range(min(rows, cols) // 2):
        top, left, bottom, right = t, t, rows - 1 - t, cols - 1 - t
        cells = [(top, j) for j in range(left, right)] + [(i, right) for i in range(top, bottom)]
        cells += [(bottom, j) for j in range(right, left, -1)] + [(i, left) for i in range(bottom, top, -1)]
        d = deque(grid[i][j] for i, j in cells)
        d.rotate(k if t % 2 == 0 else -k)
        for (i, j), v in zip(cells, d):
            out[i][j] = v
    return out
''')
add('R_rings_recursive', 'ci-ring-turns', 'recursion on the ring number', '''
def turn_rings(grid, k):
    rows, cols = len(grid), len(grid[0])
    out = [row[:] for row in grid]

    def ring(t, sign):
        if rows - 2 * t < 2 or cols - 2 * t < 2:
            return
        top, left, bottom, right = t, t, rows - 1 - t, cols - 1 - t
        cells = [(top, j) for j in range(left, right)] + [(i, right) for i in range(top, bottom)]
        cells += [(bottom, j) for j in range(right, left, -1)] + [(i, left) for i in range(bottom, top, -1)]
        n = len(cells)
        for idx, (i, j) in enumerate(cells):
            a, b = cells[(idx + sign * k) % n]
            out[a][b] = grid[i][j]
        ring(t + 1, -sign)
    ring(0, 1)
    return out
''')
add('R_spiral_isqrt', 'ci-spiral-cells', 'the ring from an integer square root, then stepped to the right ring; sides without their last corner', '''
from math import isqrt

def spiral_cells(rows, cols, ks):
    def before(t):
        return rows * cols - (rows - 2 * t) * (cols - 2 * t)
    s = rows + cols
    last = (min(rows, cols) - 1) // 2
    out = []
    for k in ks:
        t = min(last, max(0, (s - isqrt(s * s - 4 * (k - 1))) // 4))
        while t > 0 and before(t) >= k:
            t -= 1
        while t < last and before(t + 1) < k:
            t += 1
        p = k - before(t) - 1
        h, w = rows - 2 * t, cols - 2 * t
        if h == 1:
            out.append([t, t + p])
        elif w == 1:
            out.append([t + p, t])
        elif p < w - 1:
            out.append([t, t + p])
        elif p < w + h - 2:
            out.append([t + p - (w - 1), t + w - 1])
        elif p < 2 * w + h - 3:
            out.append([t + h - 1, t + w - 1 - (p - (w + h - 2))])
        else:
            out.append([t + h - 1 - (p - (2 * w + h - 3)), t])
    return out
''')
add('R_robot_blocked_keeps_trying', 'ci-robot-floor', 'right value; a blocked move does not end its command, which constraints[1] calls not fine', '''
def solve_robot_floor(text):
    tokens = text.split()
    rows, cols = int(tokens[0]), int(tokens[1])
    grid = tokens[2:2 + rows]
    for i, row in enumerate(grid):
        if 'R' in row:
            r, c = i, row.index('R')
    steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    facing = 0
    seen = {(r, c)}
    for cmd in tokens[2 + rows:]:
        if cmd == 'L':
            facing = (facing + 3) % 4
        elif cmd == 'R':
            facing = (facing + 1) % 4
        else:
            dr, dc = steps[facing]
            for _ in range(int(cmd[1:])):
                a, b = r + dr, c + dc
                if not (0 <= a < rows and 0 <= b < cols) or grid[a][b] == '#':
                    continue
                r, c = a, b
                seen.add((r, c))
    return f"{r} {c} {'NESW'[facing]} {len(seen)}"
''')
add('R_one_bit_streaming', 'ci-one-bit-apart', 'one pass: each code counts the partners already seen', '''
def one_bit_pairs(codes):
    seen = {}
    total = 0
    for c in codes:
        for b in range(30):
            total += seen.get(c ^ (1 << b), 0)
        seen[c] = seen.get(c, 0) + 1
    return total
''')

CANDIDATES = C
