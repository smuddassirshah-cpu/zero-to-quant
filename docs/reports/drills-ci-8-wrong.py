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
