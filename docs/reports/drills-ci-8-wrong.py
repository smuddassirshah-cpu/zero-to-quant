"""Wrong solutions a candidate would write, beyond each drill's `planted` ones (drills ci pack 8).
drills-ci-8-check.py runs each on the hidden tests and asserts it fails one (a wrong value, an exception,
or past 5 s for a slow one). WRONG[id] is a list of (code, what is wrong); a too-slow one says "slow" first."""

def _sub(code, *pairs):
    for a, b in pairs:
        assert a in code, a
        code = code.replace(a, b)
    return code

WRONG = {}

GRACE = """def merge_with_grace(sessions, grace):
    visits = []
    for start, end in sorted(sessions):
        if visits and start <= visits[-1][1] + grace:
            visit = visits[-1]
            visit[1] = max(visit[1], end)
            visit[2] += 1
        else:
            visits.append([start, end, 1])
    return visits
"""
WRONG["ci-grace-sessions"] = [
    (_sub(GRACE, ("sorted(sessions)", "sorted(sessions, key=lambda s: s[1])")), "sorted by end"),
    ("""def merge_with_grace(sessions, grace):
    visits, prev = [], None
    for start, end in sorted(sessions):
        if visits and start <= prev + grace:
            visits[-1][1] = max(visits[-1][1], end)
            visits[-1][2] += 1
        else:
            visits.append([start, end, 1])
        prev = end
    return visits
""", "join test against the last session's own end"),
    (_sub(GRACE, ("start <= visits[-1][1] + grace", "start <= visits[-1][0] + grace")), "grace counted from the visit's start"),
    (_sub(GRACE, ("visit[2] += 1", "visit[2] = 2")), "count set to two on a join"),
    (_sub(GRACE, ("visit[1] = max(visit[1], end)", "visit[1] = max(visit[1], end) if start <= visit[1] else visit[1]")), "a session joined by the grace does not extend the end"),
    ("""def merge_with_grace(sessions, grace):
    groups = [[s, e, 1] for s, e in sessions]
    changed = True
    while changed:
        changed = False
        for i in range(len(groups)):
            for j in range(len(groups)):
                if i != j and groups[i][0] <= groups[j][0] <= groups[i][1] + grace:
                    a, b = groups[i], groups[j]
                    groups[i] = [min(a[0], b[0]), max(a[1], b[1]), a[2] + b[2]]
                    del groups[j]
                    changed = True
                    break
            if changed:
                break
    return sorted(groups)
""", "slow: merge any two groups until nothing changes"),
]

REST = """def run_days(tasks, rest):
    ready = {}
    day = 0
    days = []
    for machine in tasks:
        day = max(day + 1, ready.get(machine, 0))
        ready[machine] = day + rest.get(machine, 0) + 1
        days.append(day)
    return days
"""
WRONG["ci-rest-days"] = [
    (_sub(REST, ("max(day + 1, ready.get(machine, 0))", "max(day, ready.get(machine, 1))")), "two jobs on one day"),
    (_sub(REST, ("day = 0\n", "day = -1\n")), "days counted from 0"),
    ("""def run_days(tasks, rest):
    days = []
    for k, machine in enumerate(tasks):
        day = days[-1] + 1 if days else 1
        last = None
        for j in range(k):
            if tasks[j] == machine:
                last = days[j]
        if last is not None:
            day = max(day, last + rest.get(machine, 0) + 1)
        days.append(day)
    return days
""", "slow: scans every earlier job for the machine's last day"),
    ("""def run_days(tasks, rest):
    pending = list(range(len(tasks)))
    days = [0] * len(tasks)
    ready, day = {}, 0
    while pending:
        day += 1
        for k in pending:
            if ready.get(tasks[k], 0) <= day:
                days[k] = day
                ready[tasks[k]] = day + rest.get(tasks[k], 0) + 1
                pending.remove(k)
                break
    return days
""", "a later job goes first while the next one waits"),
    ("""def run_days(tasks, rest):
    days, day, free = [], 0, 0
    for machine in tasks:
        day = max(day + 1, free)
        free = day + rest.get(machine, 0) + 1
        days.append(day)
    return days
""", "a rest stops the whole workshop"),
]

ROBOT = """def solve_robot_floor(text):
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
                    break
                r, c = a, b
                seen.add((r, c))
    return f"{r} {c} {'NESW'[facing]} {len(seen)}"
"""
WRONG["ci-robot-floor"] = [
    (_sub(ROBOT, ("(facing + 3) % 4", "(facing + 9) % 4"), ("(facing + 1) % 4", "(facing + 3) % 4"), ("(facing + 9) % 4", "(facing + 1) % 4")), "left and right swapped"),
    (_sub(ROBOT, ("seen = {(r, c)}", "seen = set()")), "start cell not counted"),
    (_sub(ROBOT, ("facing = 0\n", "facing = 1\n")), "starts facing east"),
    (_sub(ROBOT, ("if not (0 <= a < rows and 0 <= b < cols) or grid[a][b] == '#':", "if a >= rows or b >= cols or grid[a][b] == '#':")), "no check for the top and left edges"),
    (_sub(ROBOT, ("return f\"{r} {c}", "return f\"{c} {r}")), "column before row"),
    ("""def solve_robot_floor(text):
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
            k = int(cmd[1:])
            a, b = r + dr * k, c + dc * k
            if 0 <= a < rows and 0 <= b < cols and grid[a][b] != '#':
                for s in range(1, k + 1):
                    seen.add((r + dr * s, c + dc * s))
                r, c = a, b
    return f"{r} {c} {'NESW'[facing]} {len(seen)}"
""", "jumps the whole move or not at all"),
]

ONEBIT = """from collections import Counter

def one_bit_pairs(codes):
    count = Counter(codes)
    total = 0
    for code, k in count.items():
        for b in range(30):
            other = code ^ (1 << b)
            if other > code:
                total += k * count.get(other, 0)
    return total
"""
WRONG["ci-one-bit-apart"] = [
    (_sub(ONEBIT, ("    return total\n", "    return total + sum(k * (k - 1) // 2 for k in count.values())\n")), "equal codes counted as partners"),
    (_sub(ONEBIT, ("total += k * count.get(other, 0)", "total += other in count")), "one pair per pair of distinct codes"),
    (_sub(ONEBIT, ("range(30)", "range(29)")), "top bit never flipped"),
    (_sub(ONEBIT, ("total += k * count.get(other, 0)", "total += count.get(other, 0)")), "copies of the smaller code not multiplied in"),
    ("""def one_bit_pairs(codes):
    total = 0
    for i in range(len(codes)):
        for j in range(i + 1, len(codes)):
            x = codes[i] ^ codes[j]
            if x & (x - 1) == 0:
                total += 1
    return total
""", "slow: every pair, and 0 taken for a power of two"),
    ("""def one_bit_pairs(codes):
    s = sorted(codes)
    total = 0
    for i in range(len(s)):
        for j in range(i + 1, min(len(s), i + 64)):
            x = s[i] ^ s[j]
            if x and x & (x - 1) == 0:
                total += 1
    return total
""", "sorted, then only near neighbours compared"),
]

SWITCH = """from itertools import combinations

def fewest_switches(switches, target):
    want = int(target, 2)
    masks = [int(s, 2) for s in switches]
    for size in range(len(masks) + 1):
        for pick in combinations(range(len(masks)), size):
            lit = 0
            for i in pick:
                lit ^= masks[i]
            if lit == want:
                return list(pick)
    return None
"""
WRONG["ci-switch-panel"] = [
    (_sub(SWITCH, ("range(len(masks) + 1)", "range(1, len(masks) + 1)")), "pressing nothing never tried"),
    (_sub(SWITCH, ("combinations(range(len(masks)), size)", "reversed(list(combinations(range(len(masks)), size)))")), "the last smallest set instead of the first"),
    (_sub(SWITCH, ("return list(pick)", "return [i + 1 for i in pick]")), "switches numbered from 1"),
    (_sub(SWITCH, ("masks = [int(s, 2) for s in switches]", "masks = [int(s[::-1], 2) for s in switches]")), "switches read backwards but the target not"),
    ("""def fewest_switches(switches, target):
    want = int(target, 2)
    masks = [int(s, 2) for s in switches]
    for mask in range(1 << len(masks)):
        lit = 0
        for i in range(len(masks)):
            if mask >> i & 1:
                lit ^= masks[i]
        if lit == want:
            return [i for i in range(len(masks)) if mask >> i & 1]
    return None
""", "the first working mask, whatever its size"),
]

# ======================= drills six to ten =======================

RINGS = """def turn_rings(grid, k):
    rows, cols = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    t = 0
    while rows - 2 * t >= 2 and cols - 2 * t >= 2:
        top, left, bottom, right = t, t, rows - 1 - t, cols - 1 - t
        cells = [(top, j) for j in range(left, right)]
        cells += [(i, right) for i in range(top, bottom)]
        cells += [(bottom, j) for j in range(right, left, -1)]
        cells += [(i, left) for i in range(bottom, top, -1)]
        n = len(cells)
        shift = k % n if t % 2 == 0 else -k % n
        for idx, (i, j) in enumerate(cells):
            a, b = cells[(idx + shift) % n]
            out[a][b] = grid[i][j]
        t += 1
    return out
"""
WRONG["ci-ring-turns"] = [
    (_sub(RINGS, ("shift = k % n if t % 2 == 0 else -k % n", "shift = k % (2 * (bottom - top + right - left)) if t % 2 == 0 else -k % (2 * (bottom - top + right - left) + 4)")), "the ring length miscounted at the corners"),
    (_sub(RINGS, ("shift = k % n if t % 2 == 0 else -k % n", "shift = -k % n if t % 2 == 0 else k % n")), "the border turned anticlockwise"),
    (_sub(RINGS, ("t % 2 == 0", "(min(rows, cols) // 2 - 1 - t) % 2 == 0")), "directions counted from the innermost ring"),
    (_sub(RINGS, ("        n = len(cells)\n", "        n = 2 * (rows + cols) - 4\n")), "every ring reduced by the border's length"),
    (_sub(RINGS, ("    out = [row[:] for row in grid]\n", "    out = grid\n    grid = [row[:] for row in grid]\n"), ("    return out\n", "    return out\n")), "grid changed in place (the caller's list is overwritten)"),
    (_sub(RINGS, ("cells += [(i, left) for i in range(bottom, top, -1)]", "cells += [(i, left) for i in range(bottom, top - 1, -1)]")), "the top-left corner listed twice"),
]

CHECKS = """import bisect

def fewest_checks(jobs):
    marks = []
    for start, end, need in sorted(jobs, key=lambda job: (job[1], -job[0])):
        have = bisect.bisect_right(marks, end) - bisect.bisect_left(marks, start)
        minute = end
        while have < need:
            i = bisect.bisect_left(marks, minute)
            if i == len(marks) or marks[i] != minute:
                marks.insert(i, minute)
                have += 1
            minute -= 1
    return len(marks)
"""
WRONG["ci-double-checks"] = [
    (_sub(CHECKS, ("key=lambda job: (job[1], -job[0])", "key=lambda job: (job[0], job[1])")), "jobs taken by start"),
    (_sub(CHECKS, ("bisect.bisect_right(marks, end) - bisect.bisect_left(marks, start)", "bisect.bisect_left(marks, end) - bisect.bisect_right(marks, start)")), "visits at the end minutes not counted"),
    (_sub(CHECKS, ("        minute = end\n", "        minute = end\n        have = 0\n")), "visits already inside ignored, new ones still skip used minutes"),
    (_sub(CHECKS, ("key=lambda job: (job[1], -job[0])", "key=lambda job: (job[1] - job[0], job[1])")), "shortest jobs first"),
    ("""def fewest_checks(jobs):
    marks = set()
    for start, end, need in sorted(jobs, key=lambda job: job[1]):
        have = sum(start <= m <= end for m in marks)
        for minute in range(end - (need - have) + 1, end + 1):
            marks.add(minute)
    return len(marks)
""", "missing visits added at the last minutes even when some are used"),
    ("""def fewest_checks(jobs):
    marks = []
    for start, end, need in sorted(jobs, key=lambda job: (job[1], -job[0])):
        have = sum(start <= m <= end for m in marks)
        minute = end
        while have < need:
            if minute not in marks[-need:]:
                marks.append(minute)
                have += 1
            minute -= 1
    return len(marks)
""", "only the last few visits checked for a clash"),
]

FIT = """def first_fit(bookings, start, length):
    slot = start
    for s, e in bookings:
        if e <= slot:
            continue
        if s >= slot + length:
            break
        slot = e
    merged = []
    for s, e in sorted(bookings + [[slot, slot + length]]):
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [slot, merged]
"""
WRONG["ci-first-fit-slot"] = [
    (_sub(FIT, ("        if s >= slot + length:\n", "        if s > slot:\n")), "the first gap after the slot taken, however short"),
    (_sub(FIT, ("        if s >= slot + length:\n", "        if s > slot + length:\n")), "a booking starting at the job's end taken as a clash"),
    (_sub(FIT, ("if merged and s <= merged[-1][1]:", "if merged and s <= merged[-1][1] + 1:")), "bookings one minute apart joined"),
    (_sub(FIT, ("    slot = start\n", "    slot = 0\n"), ("    return [slot, merged]", "    return [max(slot, start), merged]")), "the search starts at minute 0"),
    (_sub(FIT, ("        slot = e\n", "        slot = e\n        break\n")), "the slot moved past one booking only"),
    ("""def first_fit(bookings, start, length):
    slot = start
    for s, e in bookings:
        if e <= slot:
            continue
        if s >= slot + length:
            break
        slot = e
    new = [slot, slot + length]
    merged = []
    for s, e in bookings:
        if e == new[0]:
            new[0] = s
        elif s == new[1]:
            new[1] = e
        else:
            merged.append([s, e])
    merged.append(new)
    return [slot, sorted(merged)]
""", "only bookings that touch the new one joined"),
]

ROOMS = """import heapq

def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: (meetings[i][0], i))
    free = []
    busy = []
    opened = 0
    rooms = [0] * len(meetings)
    for i in order:
        start, end = meetings[i]
        while busy and busy[0][0] <= start:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room = opened
            opened += 1
        rooms[i] = room
        heapq.heappush(busy, (end + clean, room))
    return rooms
"""
WRONG["ci-room-numbers"] = [
    (_sub(ROOMS, ("(end + clean, room)", "(end, room)")), "cleaning time ignored"),
    (_sub(ROOMS, ("key=lambda i: (meetings[i][0], i)", "key=lambda i: i")), "meetings placed in list order"),
    (_sub(ROOMS, ("heapq.heappush(free, heapq.heappop(busy)[1])", "free.append(heapq.heappop(busy)[1])"), ("room = heapq.heappop(free)", "room = free.pop()")), "the room freed last reused first"),
    (_sub(ROOMS, ("        while busy and busy[0][0] <= start:\n", "        if busy and busy[0][0] <= start:\n")), "one room released per meeting"),
    (_sub(ROOMS, ("key=lambda i: (meetings[i][0], i)", "key=lambda i: (meetings[i][0], -i)")), "ties in start taken last in the list first"),
    (_sub(ROOMS, ("heapq.heappush(free, heapq.heappop(busy)[1])", "free.append(heapq.heappop(busy)[1])"), ("room = heapq.heappop(free)", "room = free.pop(0)")), "free rooms handed out in the order they were freed"),
]

LOOP = """def loop_starts(fuel, burn):
    n = len(fuel)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + fuel[i] - burn[i]
    total = pre[n]
    later = [0] * (n + 1)
    later[n] = pre[n]
    for i in range(n - 1, -1, -1):
        later[i] = min(pre[i], later[i + 1])
    starts = []
    earlier = float('inf')
    for s in range(n):
        if s:
            earlier = min(earlier, pre[s])
        if later[s + 1] >= pre[s] and earlier + total >= pre[s]:
            starts.append(s)
    return starts
"""
WRONG["ci-loop-starts"] = [
    (_sub(LOOP, ("if later[s + 1] >= pre[s] and earlier + total >= pre[s]:", "if later[s + 1] >= pre[s]:")), "the stretch after passing depot 0 not checked"),
    (_sub(LOOP, ("if later[s + 1] >= pre[s] and earlier + total >= pre[s]:", "if total >= 0 and earlier + total >= pre[s]:")), "the stretch before depot 0 not checked"),
    (_sub(LOOP, ("        if s:\n            earlier = min(earlier, pre[s])\n", "        if s > 1:\n            earlier = min(earlier, pre[s - 1])\n")), "the earlier minimum stops one depot short"),
    ("""def loop_starts(fuel, burn):
    pre, run = [], 0
    for f, b in zip(fuel, burn):
        pre.append(run)
        run += f - b
    if run < 0:
        return []
    low = min(pre)
    return [s for s, p in enumerate(pre) if p == low]
""", "the depots at the lowest prefix, right only when the loop nets to zero"),
    ("""def loop_starts(fuel, burn):
    n = len(fuel)
    if sum(fuel) < sum(burn):
        return []
    starts, tank, start = [], 0, 0
    for k in range(2 * n):
        i = k % n
        tank += fuel[i] - burn[i]
        if tank < 0:
            tank, start = 0, k + 1
        elif k - start + 1 >= n and start < n and start not in starts:
            starts.append(start)
            start += 1
            tank -= fuel[start - 1] - burn[start - 1]
    return sorted(starts)
""", "a sliding start that drops the first depot's gain without re-checking"),
]
