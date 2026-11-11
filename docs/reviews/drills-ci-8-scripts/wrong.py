"""Second reader's candidates for pack 8: wrong or too-slow solutions a real
candidate writes that are neither planted nor in the author's drills-ci-8-wrong.py.
Run: harness.py wrong.py <drills dir> --limit 15
Every label says what the slip is. The harness prints the ones that pass every test."""
C = {}


def add(label, did, comment, code):
    C[label] = (did, code, comment)


# ------------------------------------------------------------ ci-grace-sessions
add('grace_set_dedupe', 'ci-grace-sessions', 'equal sessions dropped by a set before the count', '''
def merge_with_grace(sessions, grace):
    out = []
    for s, e in sorted(set(map(tuple, sessions))):
        if out and s <= out[-1][1] + grace:
            out[-1][1] = max(out[-1][1], e)
            out[-1][2] += 1
        else:
            out.append([s, e, 1])
    return out
''')
add('grace_empty_crash', 'ci-grace-sessions', 'first visit taken before the loop, so no sessions is an error', '''
def merge_with_grace(sessions, grace):
    ss = sorted(sessions)
    out = [[ss[0][0], ss[0][1], 1]]
    for s, e in ss[1:]:
        if s <= out[-1][1] + grace:
            out[-1][1] = max(out[-1][1], e)
            out[-1][2] += 1
        else:
            out.append([s, e, 1])
    return out
''')
add('grace_event_sweep_tie', 'ci-grace-sessions', 'sweep over events, an end plus grace taken before a start at the same minute', '''
def merge_with_grace(sessions, grace):
    ev = []
    for s, e in sessions:
        ev.append((s, 1, e))
        ev.append((e + grace, 0, e))
    ev.sort()
    out = []
    open_ = 0
    for t, kind, e in ev:
        if kind == 1:
            if open_ == 0:
                out.append([t, e, 0])
            open_ += 1
            out[-1][2] += 1
            out[-1][1] = max(out[-1][1], e)
        else:
            open_ -= 1
    return out
''')
add('grace_count_only_extending', 'ci-grace-sessions', 'a session inside the visit is not counted', '''
def merge_with_grace(sessions, grace):
    out = []
    for s, e in sorted(sessions):
        if out and s <= out[-1][1] + grace:
            if e > out[-1][1]:
                out[-1][1] = e
                out[-1][2] += 1
        else:
            out.append([s, e, 1])
    return out
''')
add('grace_gap_from_start_sorted_end_desc', 'ci-grace-sessions', 'equal starts sorted longest first, then the last session end kept (max forgotten only on ties)', '''
def merge_with_grace(sessions, grace):
    out = []
    for s, e in sorted(sessions, key=lambda x: (x[0], -x[1])):
        if out and s <= out[-1][1] + grace:
            if s != out[-1][0]:
                out[-1][1] = max(out[-1][1], e)
            out[-1][2] += 1
        else:
            out.append([s, e, 1])
    return out
''')

# ------------------------------------------------------------ ci-rest-days
add('rest_default_one', 'ci-rest-days', 'a machine missing from rest given one rest day', '''
def run_days(tasks, rest):
    ready, day, out = {}, 0, []
    for m in tasks:
        day = max(day + 1, ready.get(m, 0))
        ready[m] = day + rest.get(m, 1) + 1
        out.append(day)
    return out
''')
add('rest_only_back_to_back', 'ci-rest-days', 'rest applied only when the same machine has two jobs in a row', '''
def run_days(tasks, rest):
    day, out, prev = 0, [], None
    for m in tasks:
        day += 1
        if m == prev:
            day += rest.get(m, 0)
        out.append(day)
        prev = m
    return out
''')
add('rest_ready_from_previous_day', 'ci-rest-days', 'the ready day worked out from the day before the wait', '''
def run_days(tasks, rest):
    ready, day, out = {}, 0, []
    for m in tasks:
        nxt = day + 1
        ready_m = ready.get(m, 0)
        ready[m] = nxt + rest.get(m, 0) + 1
        day = max(nxt, ready_m)
        out.append(day)
    return out
''')
add('rest_gap_counts_other_jobs_only', 'ci-rest-days', 'rest measured in jobs done since, not in days', '''
def run_days(tasks, rest):
    last, day, out = {}, 0, []
    for i, m in enumerate(tasks):
        day += 1
        if m in last:
            done = i - last[m] - 1
            day += max(0, rest.get(m, 0) - done)
        last[m] = i
        out.append(day)
    return out
''')

# ------------------------------------------------------------ ci-robot-floor
ROBOT = '''
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
                    break
                r, c = a, b
                seen.add((r, c))
    return f"{r} {c} {'NESW'[facing]} {len(seen)}"
'''
add('robot_lines_not_stripped', 'ci-robot-floor', 'rows read as whole lines, spaces and all', '''
def solve_robot_floor(text):
    lines = text.split('\\n')
    rows, cols = map(int, lines[0].split())
    grid = lines[1:1 + rows]
    for i, row in enumerate(grid):
        if 'R' in row:
            r, c = i, row.index('R')
    steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    facing = 0
    seen = {(r, c)}
    for cmd in ' '.join(lines[1 + rows:]).split():
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
''')
add('robot_one_command_line', 'ci-robot-floor', 'commands read from one line only', '''
def solve_robot_floor(text):
    lines = [ln.strip() for ln in text.strip().split('\\n')]
    rows, cols = map(int, lines[0].split())
    grid = lines[1:1 + rows]
    for i, row in enumerate(grid):
        if 'R' in row:
            r, c = i, row.index('R')
    steps = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    facing = 0
    seen = {(r, c)}
    cmds = lines[1 + rows].split() if len(lines) > 1 + rows else []
    for cmd in cmds:
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
''')
add('robot_start_cell_is_wall', 'ci-robot-floor', 'only "." is floor, so the robot cannot cross its own start cell', ROBOT.replace("grid[a][b] == '#'", "grid[a][b] != '.'"))
add('robot_cells_at_stops_only', 'ci-robot-floor', 'cells counted where a command ends, not along the way', ROBOT.replace('''                r, c = a, b
                seen.add((r, c))''', '''                r, c = a, b
            seen.add((r, c))'''))
add('robot_blocked_ends_everything', 'ci-robot-floor', 'a blocked move ends the whole run, not the one command', '''
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
    stop = False
    for cmd in tokens[2 + rows:]:
        if stop:
            break
        if cmd == 'L':
            facing = (facing + 3) % 4
        elif cmd == 'R':
            facing = (facing + 1) % 4
        else:
            dr, dc = steps[facing]
            for _ in range(int(cmd[1:])):
                a, b = r + dr, c + dc
                if not (0 <= a < rows and 0 <= b < cols) or grid[a][b] == '#':
                    stop = True
                    break
                r, c = a, b
                seen.add((r, c))
    return f"{r} {c} {'NESW'[facing]} {len(seen)}"
''')
add('robot_rows_cols_swapped_in_bounds', 'ci-robot-floor', 'the edge test uses the column count for rows', ROBOT.replace('0 <= a < rows and 0 <= b < cols', '0 <= a < cols and 0 <= b < rows'))
add('robot_blocked_turns_round', 'ci-robot-floor', 'a blocked robot keeps trying, and a command "R" inside the grid block is counted as a row', ROBOT.replace("grid = tokens[2:2 + rows]", "grid = [t for t in tokens[2:] if set(t) <= set('.#R') and len(t) == cols][:rows]"))
add('robot_first_R_in_text', 'ci-robot-floor', 'start found with text.index, which is thrown by spaces before rows', '''
def solve_robot_floor(text):
    tokens = text.split()
    rows, cols = int(tokens[0]), int(tokens[1])
    grid = tokens[2:2 + rows]
    body = text.split('\\n', 1)[1]
    k = body.index('R')
    r, c = k // (cols + 1), k % (cols + 1)
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
''')

# ------------------------------------------------------------ ci-double-checks
CHECKS = '''
import bisect

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
'''
add('checks_start_minute_not_counted', 'ci-double-checks', 'a visit at the start minute of a job is not counted for it', CHECKS.replace('bisect.bisect_left(marks, start)', 'bisect.bisect_right(marks, start)'))
add('checks_by_need_desc', 'ci-double-checks', 'jobs taken by need, largest first', CHECKS.replace('key=lambda job: (job[1], -job[0])', 'key=lambda job: (-job[2], job[1])'))
add('checks_slow_count', 'ci-double-checks', 'slow: every visit scanned to count those inside a job', '''
def fewest_checks(jobs):
    marks = set()
    for start, end, need in sorted(jobs, key=lambda job: job[1]):
        have = sum(1 for m in marks if start <= m <= end)
        minute = end
        while have < need:
            if minute not in marks:
                marks.add(minute)
                have += 1
            minute -= 1
    return len(marks)
''')
add('checks_count_by_minutes', 'ci-double-checks', 'slow: every minute of the job walked to count its visits', '''
def fewest_checks(jobs):
    marks = set()
    for start, end, need in sorted(jobs, key=lambda job: job[1]):
        have = sum(1 for m in range(start, end + 1) if m in marks)
        minute = end
        while have < need:
            if minute not in marks:
                marks.add(minute)
                have += 1
            minute -= 1
    return len(marks)
''')
add('checks_by_end_then_need_cap', 'ci-double-checks', 'the two-point trick of the classic: only the last two visits remembered', '''
def fewest_checks(jobs):
    count = 0
    a = b = -1
    for start, end, need in sorted(jobs, key=lambda job: (job[1], -job[0])):
        have = (a >= start) + (b >= start)
        if need - have >= 2 or (need >= 2 and have == 0):
            count += max(need, 2) - have if need > 2 else 2
            a, b = end - 1, end
        elif need - have == 1:
            count += 1
            a, b = b, end
    return count
''')
add('checks_window_last_five', 'ci-double-checks', 'visits kept in a list, appended and never sorted, count taken from the last five', '''
def fewest_checks(jobs):
    marks = []
    used = set()
    for start, end, need in sorted(jobs, key=lambda job: (job[1], -job[0])):
        have = sum(1 for m in marks[-5:] if start <= m <= end)
        minute = end
        while have < need:
            if minute not in used:
                used.add(minute)
                marks.append(minute)
                have += 1
            minute -= 1
    return len(marks)
''')
add('checks_sorted_by_end_start_asc_place_from_have', 'ci-double-checks', 'missing visits placed at end, end - 1, ... counting from the number already held', '''
import bisect

def fewest_checks(jobs):
    marks = []
    for start, end, need in sorted(jobs, key=lambda job: job[1]):
        have = bisect.bisect_right(marks, end) - bisect.bisect_left(marks, start)
        for minute in range(end - (need - have) + 1, end + 1):
            i = bisect.bisect_left(marks, minute)
            if i == len(marks) or marks[i] != minute:
                marks.insert(i, minute)
    return len(marks)
''')

# ------------------------------------------------------------ ci-first-fit-slot
JOIN = '''
    merged = []
    for s, e in sorted(bookings + [[slot, slot + length]]):
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [slot, merged]
'''
add('fit_no_gap_before_first', 'ci-first-fit-slot', 'gaps between bookings only: the room before the first booking is never tried', '''
def first_fit(bookings, start, length):
    if not bookings:
        slot = start
    else:
        slot = None
        for i in range(len(bookings) - 1):
            a = max(start, bookings[i][1])
            if a + length <= bookings[i + 1][0]:
                slot = a
                break
        if slot is None:
            slot = max(start, bookings[-1][1])
''' + JOIN)
add('fit_gap_size_only', 'ci-first-fit-slot', 'a gap is taken when it is long enough as a whole, though start sits part way along it', '''
def first_fit(bookings, start, length):
    prev = 0
    slot = None
    for s, e in bookings:
        if s - prev >= length and s > start:
            slot = max(start, prev)
            break
        prev = e
    if slot is None:
        slot = max(start, prev)
''' + JOIN)
add('fit_past_end_forgets_start', 'ci-first-fit-slot', 'no gap found: the job goes at the last end, even when start is later', '''
def first_fit(bookings, start, length):
    slot = start
    found = False
    for s, e in bookings:
        if e <= slot:
            continue
        if s >= slot + length:
            found = True
            break
        slot = e
    if not found and bookings:
        slot = bookings[-1][1]
''' + JOIN)
add('fit_gap_must_begin_after_start', 'ci-first-fit-slot', 'only gaps that begin at or after start are tried, so a job cannot start part way along a gap', '''
def first_fit(bookings, start, length):
    prev = 0
    slot = None
    for s, e in bookings:
        if prev >= start and s - prev >= length:
            slot = prev
            break
        prev = e
    if slot is None:
        slot = max(start, prev)
''' + JOIN)
add('fit_bisect_then_walk', 'ci-first-fit-slot', 'binary search on the starts, stepping back one booking, then the first gap from there measured from that booking end', '''
import bisect

def first_fit(bookings, start, length):
    i = max(0, bisect.bisect_right([b[0] for b in bookings], start) - 1)
    slot = start
    for s, e in bookings[i:]:
        if s >= slot + length:
            break
        slot = max(slot, e)
''' + JOIN)
add('fit_merge_new_only_once', 'ci-first-fit-slot', 'the new booking joined to the one before it, or else the one after, never both; old touches joined first', '''
def first_fit(bookings, start, length):
    slot = start
    for s, e in bookings:
        if e <= slot:
            continue
        if s >= slot + length:
            break
        slot = e
    old = []
    for s, e in bookings:
        if old and old[-1][1] == s:
            old[-1][1] = e
        else:
            old.append([s, e])
    new = [slot, slot + length]
    for b in old:
        if b[1] == new[0]:
            b[1] = new[1]
            return [slot, old]
    for b in old:
        if b[0] == new[1]:
            b[0] = new[0]
            return [slot, old]
    return [slot, sorted(old + [new])]
''')

# ------------------------------------------------------------ ci-one-bit-apart
add('bit_no_shift', 'ci-one-bit-apart', 'the code XORed with 0 to 29, not with 1 << b', '''
from collections import Counter

def one_bit_pairs(codes):
    count = Counter(codes)
    total = 0
    for code, k in count.items():
        for b in range(30):
            other = code ^ b
            if other > code:
                total += k * count.get(other, 0)
    return total
''')
add('bit_range_1_to_30', 'ci-one-bit-apart', 'bits 1 to 30 flipped, never bit 0', '''
from collections import Counter

def one_bit_pairs(codes):
    count = Counter(codes)
    total = 0
    for code, k in count.items():
        for b in range(1, 31):
            other = code ^ (1 << b)
            if other > code:
                total += k * count.get(other, 0)
    return total
''')
add('bit_distinct_pairs_slow', 'ci-one-bit-apart', 'slow: every pair of distinct codes compared', '''
from collections import Counter

def one_bit_pairs(codes):
    count = Counter(codes)
    keys = list(count)
    total = 0
    for i in range(len(keys)):
        a = keys[i]
        for j in range(i):
            x = a ^ keys[j]
            if x & (x - 1) == 0:
                total += count[a] * count[keys[j]]
    return total
''')
add('bit_groups_by_cleared_bit', 'ci-one-bit-apart', 'codes grouped with one bit cleared; every pair in a group counted, equal codes included', '''
from collections import Counter

def one_bit_pairs(codes):
    total = 0
    for b in range(30):
        groups = Counter(c & ~(1 << b) for c in codes)
        total += sum(g * (g - 1) // 2 for g in groups.values())
    return total
''')
add('bit_set_bits_only', 'ci-one-bit-apart', 'only set bits cleared (each pair from its larger code), but found with bit_length of the code minus one', '''
from collections import Counter

def one_bit_pairs(codes):
    count = Counter(codes)
    total = 0
    for code, k in count.items():
        for b in range(code.bit_length() - 1):
            if code >> b & 1:
                total += k * count.get(code ^ (1 << b), 0)
    return total
''')

# ------------------------------------------------------------ ci-ring-turns
RINGS = '''
def turn_rings(grid, k):
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
'''
add('rings_two_wide_not_a_ring', 'ci-ring-turns', 'a ring two rows or two columns thick is left alone', RINGS.replace('rows - 2 * t >= 2 and cols - 2 * t >= 2', 'rows - 2 * t > 2 and cols - 2 * t > 2'))
add('rings_square_assumed', 'ci-ring-turns', 'the ring count taken from the rows alone', RINGS.replace('while rows - 2 * t >= 2 and cols - 2 * t >= 2:', 'while rows - 2 * t >= 2:\n        if cols - 2 * t < 1: break'))
add('rings_values_pulled_not_pushed', 'ci-ring-turns', 'each cell takes the tile k places ahead: the turn runs the other way', RINGS.replace('out[a][b] = grid[i][j]', 'out[i][j] = grid[a][b]'))
add('rings_shift_mod_missing_inner', 'ci-ring-turns', 'the anticlockwise shift is n - k with k not reduced first', RINGS.replace('-k % n', '(n - k) if k <= n else (n - k % n) % n').replace('cells[(idx + shift) % n]', 'cells[(idx + shift) % n if shift < n else idx]'))
add('rings_parity_from_k', 'ci-ring-turns', 'direction flips with the ring, but an odd ring turns k - 1 steps', RINGS.replace('-k % n', '-(k - 1) % n'))
add('rings_alias_rows', 'ci-ring-turns', 'the copy is shallow, so tiles are written into the caller rows and read back turned', RINGS.replace('out = [row[:] for row in grid]', 'out = grid[:]'))

# ------------------------------------------------------------ ci-switch-panel
add('switch_gauss', 'ci-switch-panel', 'elimination over GF(2): a working set, not a smallest one', '''
def fewest_switches(switches, target):
    want = int(target, 2)
    basis = []          # (reduced mask, set of switches as a mask)
    for i, s in enumerate(switches):
        v, who = int(s, 2), 1 << i
        for bv, bw in basis:
            if v ^ bv < v:
                v ^= bv
                who ^= bw
        if v:
            basis.append((v, who))
            basis.sort(reverse=True)
    who = 0
    for bv, bw in basis:
        if want ^ bv < want:
            want ^= bv
            who ^= bw
    if want:
        return None
    return [i for i in range(len(switches)) if who >> i & 1]
''')
add('switch_dp_first_kept', 'ci-switch-panel', 'a table of best sets per pattern, filled switch by switch; ties keep the set found first', '''
def fewest_switches(switches, target):
    best = {0: []}
    for i, s in enumerate(switches):
        m = int(s, 2)
        for state, pick in list(best.items()):
            new = state ^ m
            if new not in best or len(pick) + 1 < len(best[new]):
                best[new] = pick + [i]
    return best.get(int(target, 2))
''')
add('switch_sizes_from_one', 'ci-switch-panel', 'sizes from 1 up, with a zero target handled by returning None', '''
from itertools import combinations

def fewest_switches(switches, target):
    want = int(target, 2)
    masks = [int(s, 2) for s in switches]
    if want == 0 and not masks:
        return []
    for size in range(1, len(masks) + 1):
        for pick in combinations(range(len(masks)), size):
            lit = 0
            for i in pick:
                lit ^= masks[i]
            if lit == want:
                return list(pick)
    return None
''')
add('switch_or_not_xor', 'ci-switch-panel', 'lamps turned on by OR, so a second press never turns one off', '''
from itertools import combinations

def fewest_switches(switches, target):
    want = int(target, 2)
    masks = [int(s, 2) for s in switches]
    for size in range(len(masks) + 1):
        for pick in combinations(range(len(masks)), size):
            lit = 0
            for i in pick:
                lit |= masks[i]
            if lit == want:
                return list(pick)
    return None
''')
add('switch_bfs_set_order', 'ci-switch-panel', 'breadth-first search over patterns, the presses returned in the order pressed, not sorted', '''
from collections import deque

def fewest_switches(switches, target):
    want = int(target, 2)
    masks = [int(s, 2) for s in switches]
    seen = {0: []}
    q = deque([0])
    while q:
        s = q.popleft()
        if s == want:
            return seen[s]
        for i in range(len(masks) - 1, -1, -1):
            if i not in seen[s]:
                t = s ^ masks[i]
                if t not in seen:
                    seen[t] = seen[s] + [i]
                    q.append(t)
    return None
''')
add('switch_dedupe_equal', 'ci-switch-panel', 'equal switches dropped first, so the positions returned are those of the shortened list', '''
from itertools import combinations

def fewest_switches(switches, target):
    want = int(target, 2)
    uniq = list(dict.fromkeys(switches))
    masks = [int(s, 2) for s in uniq]
    for size in range(len(masks) + 1):
        for pick in combinations(range(len(masks)), size):
            lit = 0
            for i in pick:
                lit ^= masks[i]
            if lit == want:
                return list(pick)
    return None
''')

# ------------------------------------------------------------ ci-k-bit-count
KB = '''
from math import comb

def count_k_bits(queries):
    def upto(n, k):
        if n < 0:
            return 0
        count, used = 0, 0
        for b in range(n.bit_length() - 1, -1, -1):
            if n >> b & 1:
                if used <= k:
                    count += comb(b, k - used)
                used += 1
        if used == k:
            count += 1
        return count
    return [upto(hi, k) - upto(lo - 1, k) for lo, hi, k in queries]
'''
add('kbits_float_comb', 'ci-k-bit-count', 'binomials from factorials with true division', KB.replace('from math import comb', 'from math import factorial\n\ndef comb(n, r):\n    if r < 0 or r > n:\n        return 0\n    return int(factorial(n) / (factorial(r) * factorial(n - r)))'))
add('kbits_scipy_style_float', 'ci-k-bit-count', 'binomials built by a running float product', KB.replace('from math import comb', 'def comb(n, r):\n    if r < 0 or r > n:\n        return 0\n    x = 1.0\n    for i in range(r):\n        x = x * (n - i) / (i + 1)\n    return round(x)'))
add('kbits_bit0_skipped', 'ci-k-bit-count', 'the walk stops above bit 0', KB.replace('range(n.bit_length() - 1, -1, -1)', 'range(n.bit_length() - 1, 0, -1)'))
add('kbits_no_guard_below_zero', 'ci-k-bit-count', 'lo - 1 = -1 walked as if it were a number', KB.replace('        if n < 0:\n            return 0\n', ''))
add('kbits_table_60', 'ci-k-bit-count', "Pascal's triangle with 60 rows and columns, indexed without a check", '''
def count_k_bits(queries):
    C = [[0] * 60 for _ in range(60)]
    for i in range(60):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    def upto(n, k):
        if n < 0:
            return 0
        count, used = 0, 0
        for b in range(n.bit_length() - 1, -1, -1):
            if n >> b & 1:
                if used <= k:
                    count += C[b][k - used]
                used += 1
        if used == k:
            count += 1
        return count
    return [upto(hi, k) - upto(lo - 1, k) for lo, hi, k in queries]
''')
add('kbits_hi_only_when_lo_zero', 'ci-k-bit-count', 'lo = 0 special-cased as "no subtraction", every other lo subtracts the count up to lo', KB.replace('return [upto(hi, k) - upto(lo - 1, k) for lo, hi, k in queries]', 'return [upto(hi, k) - (upto(lo, k) if lo else 0) + (1 if lo and bin(lo).count("1") == k and lo.bit_length() < 40 else 0) for lo, hi, k in queries]'))
add('kbits_32_bits', 'ci-k-bit-count', 'the walk covers 32 bits only', KB.replace('range(n.bit_length() - 1, -1, -1)', 'range(31, -1, -1)'))
add('kbits_fixed_59_wrong_top', 'ci-k-bit-count', 'the walk covers bits 58 down to 0, missing the top bit of a 60-bit bound', KB.replace('range(n.bit_length() - 1, -1, -1)', 'range(58, -1, -1)'))

# ------------------------------------------------------------ ci-loop-starts
add('loop_zero_arrivals', 'ci-loop-starts', 'one start by the skip-ahead greedy, then every depot the van reaches with an empty battery', '''
def loop_starts(fuel, burn):
    n = len(fuel)
    g = [f - b for f, b in zip(fuel, burn)]
    if sum(g) < 0:
        return []
    start = tank = 0
    for i in range(n):
        tank += g[i]
        if tank < 0:
            start, tank = i + 1, 0
    out = [start % n]
    tank = 0
    for d in range(n - 1):
        tank += g[(start + d) % n]
        if tank == 0:
            out.append((start + d + 1) % n)
    return sorted(set(out))
''')
add('loop_slices_min', 'ci-loop-starts', 'slow: min over a slice of the prefixes for every depot', '''
def loop_starts(fuel, burn):
    n = len(fuel)
    pre = [0]
    for f, b in zip(fuel, burn):
        pre.append(pre[-1] + f - b)
    total = pre[n]
    if total < 0:
        return []
    return [s for s in range(n) if min(pre[s + 1:]) >= pre[s] and (s == 0 or min(pre[1:s + 1]) + total >= pre[s])]
''')
add('loop_nonneg_gain_and_total', 'ci-loop-starts', 'total at least 0 and every depot from which the minimum prefix lies behind it', '''
def loop_starts(fuel, burn):
    n = len(fuel)
    pre = [0]
    for f, b in zip(fuel, burn):
        pre.append(pre[-1] + f - b)
    if pre[n] < 0:
        return []
    low = min(pre[1:])
    last = max(i for i in range(1, n + 1) if pre[i] == low)
    return [s for s in range(n) if s >= last % n and min(pre[s + 1:] or [pre[s]]) >= pre[s]] if last % n else [s for s in range(n) if pre[s] <= min(pre[s + 1:])][:1]
''')
add('loop_suffix_min_only_total_zero_assumed', 'ci-loop-starts', 'the lap after depot 0 tested against the whole minimum prefix, not the earlier ones only', '''
def loop_starts(fuel, burn):
    n = len(fuel)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + fuel[i] - burn[i]
    total = pre[n]
    later = [0] * (n + 1)
    later[n] = pre[n]
    for i in range(n - 1, -1, -1):
        later[i] = min(pre[i], later[i + 1])
    low = min(pre[1:])
    return [s for s in range(n) if later[s + 1] >= pre[s] and low + total >= pre[s]]
''')

# ------------------------------------------------------------ ci-ring-bonuses
add('bonus_two_line_passes_wrap_once', 'ci-ring-bonuses', 'left pass from trader 0 round to trader 0 again, right pass the same, one lap each', '''
def ring_bonuses(scores):
    n = len(scores)
    t = [1] * n
    for i in range(1, n + 1):
        a, b = i % n, (i - 1) % n
        if scores[a] > scores[b] and t[a] <= t[b]:
            t[a] = t[b] + 1
    for i in range(n - 1, -2, -1):
        a, b = i % n, (i + 1) % n
        if scores[a] > scores[b] and t[a] <= t[b]:
            t[a] = t[b] + 1
    return sum(t)
''')
add('bonus_sorted_ties_get_more', 'ci-ring-bonuses', 'traders taken in score order, each one more than the larger neighbour already served', '''
def ring_bonuses(scores):
    n = len(scores)
    t = [0] * n
    for i in sorted(range(n), key=lambda i: scores[i]):
        t[i] = 1 + max(t[(i - 1) % n], t[(i + 1) % n]) if n > 1 else 1
    return sum(t)
''')
add('bonus_cut_at_last_lowest_no_far_end', 'ci-ring-bonuses', 'cut at a lowest score, the line passes run, the far end fixed against the cut by one comparison per sweep, two sweeps', '''
def ring_bonuses(scores):
    n = len(scores)
    low = scores.index(min(scores))
    line = scores[low:] + scores[:low]
    t = [1] * n
    for i in range(1, n):
        if line[i] > line[i - 1]:
            t[i] = t[i - 1] + 1
    if n > 1 and line[n - 1] > line[0]:
        t[n - 1] = max(t[n - 1], 2)
    for i in range(n - 2, -1, -1):
        if line[i] > line[i + 1]:
            t[i] = max(t[i], t[i + 1] + 1)
    return sum(t)
''')
add('bonus_peaks_valleys_formula', 'ci-ring-bonuses', 'run lengths between valleys and peaks summed as triangles, equal scores treated as a fall', '''
def ring_bonuses(scores):
    n = len(scores)
    if n == 1:
        return 1
    low = scores.index(min(scores))
    line = scores[low:] + scores[:low] + [scores[low]]
    total = 0
    up = down = peak = 0
    for i in range(1, n + 1):
        if line[i] > line[i - 1]:
            up += 1
            down = 0
            peak = up
            total += 1 + up
        elif line[i] == line[i - 1]:
            up = down = peak = 0
            total += 1
        else:
            up = 0
            down += 1
            total += 1 + down - (1 if peak >= down else 0)
    return total - 1 + 1 - 1 + (1 if False else 0) + 0
''')

# ------------------------------------------------------------ ci-room-numbers
add('rooms_dict_by_times', 'ci-room-numbers', 'rooms mapped back through a dict keyed by (start, end)', '''
import heapq

def room_numbers(meetings, clean):
    free, busy, opened, got = [], [], 0, {}
    for s, e in sorted(map(tuple, meetings), key=lambda m: m[0]):
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room, opened = opened, opened + 1
        got[(s, e)] = room
        heapq.heappush(busy, (e + clean, room))
    return [got[tuple(m)] for m in meetings]
''')
add('rooms_index_lookup', 'ci-room-numbers', 'each sorted meeting mapped back with meetings.index', '''
import heapq

def room_numbers(meetings, clean):
    free, busy, opened = [], [], 0
    rooms = [0] * len(meetings)
    for m in sorted(meetings, key=lambda m: m[0]):
        s, e = m
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room, opened = opened, opened + 1
        rooms[meetings.index(m)] = room
        heapq.heappush(busy, (e + clean, room))
    return rooms
''')
add('rooms_one_heap_lowest_of_earliest', 'ci-room-numbers', 'one heap of (free minute, room): the room on top is taken when free, which is the earliest freed, ties by number', '''
import heapq

def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: meetings[i][0])
    heap, opened = [], 0
    rooms = [0] * len(meetings)
    for i in order:
        s, e = meetings[i]
        if heap and heap[0][0] <= s:
            ready = []
            while heap and heap[0][0] <= s and len(ready) < 2:
                ready.append(heapq.heappop(heap))
            ready.sort(key=lambda x: x[1])
            room = ready[0][1]
            for r in ready[1:]:
                heapq.heappush(heap, r)
        else:
            room, opened = opened, opened + 1
        rooms[i] = room
        heapq.heappush(heap, (e + clean, room))
    return rooms
''')
add('rooms_clean_before_too', 'ci-room-numbers', 'a room must also be clean for `clean` minutes before the first meeting in it; rooms freed compare e + clean < s + 1 after rounding', '''
import heapq

def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: (meetings[i][0], i))
    free, busy, opened = [], [], 0
    rooms = [0] * len(meetings)
    for i in order:
        s, e = meetings[i]
        while busy and busy[0][0] + clean <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room, opened = opened, opened + 1
        rooms[i] = room
        heapq.heappush(busy, (e + (clean if clean < 1000 else 0), room))
    return rooms
''')
add('rooms_sort_whole_rows', 'ci-room-numbers', 'meetings sorted as [start, end, index] rows, so equal starts go shortest first', '''
import heapq

def room_numbers(meetings, clean):
    rows = sorted([s, e, i] for i, (s, e) in enumerate(meetings))
    free, busy, opened = [], [], 0
    rooms = [0] * len(meetings)
    for s, e, i in rows:
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room, opened = opened, opened + 1
        rooms[i] = room
        heapq.heappush(busy, (e + clean, room))
    return rooms
''')

# ------------------------------------------------------------ ci-spiral-cells
SP = '''
def spiral_cells(rows, cols, ks):
    def before(t):
        return rows * cols - (rows - 2 * t) * (cols - 2 * t)
    last = (min(rows, cols) - 1) // 2
    out = []
    for k in ks:
        lo, hi = 0, last
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if before(mid) < k:
                lo = mid
            else:
                hi = mid - 1
        t = lo
        p = k - before(t) - 1
        h, w = rows - 2 * t, cols - 2 * t
        if p < w:
            out.append([t, t + p])
        elif p < w + h - 1:
            out.append([t + p - w + 1, t + w - 1])
        elif p < 2 * w + h - 2:
            out.append([t + h - 1, t + w - 1 - (p - w - h + 2)])
        else:
            out.append([t + h - 1 - (p - 2 * w - h + 3), t])
    return out
'''
add('spiral_le_in_search', 'ci-spiral-cells', 'the search keeps a ring whose earlier plots number exactly k', SP.replace('if before(mid) < k:', 'if before(mid) <= k:'))
add('spiral_isqrt_floor', 'ci-spiral-cells', 'the ring from an integer square root, rounded the wrong way', '''
from math import isqrt

def spiral_cells(rows, cols, ks):
    def before(t):
        return rows * cols - (rows - 2 * t) * (cols - 2 * t)
    s = rows + cols
    out = []
    for k in ks:
        t = (s - isqrt(s * s - 4 * (k - 1))) // 4
        t = min(t, (min(rows, cols) - 1) // 2)
        p = k - before(t) - 1
        h, w = rows - 2 * t, cols - 2 * t
        if p < w:
            out.append([t, t + p])
        elif p < w + h - 1:
            out.append([t + p - w + 1, t + w - 1])
        elif p < 2 * w + h - 2:
            out.append([t + h - 1, t + w - 1 - (p - w - h + 2)])
        else:
            out.append([t + h - 1 - (p - 2 * w - h + 3), t])
    return out
''')
add('spiral_perimeter_ring_sizes', 'ci-spiral-cells', 'plots before a ring summed from perimeters 2(h + w) - 4, which is wrong for a last ring of one line only if used there, and the search bound is min // 2', SP.replace('last = (min(rows, cols) - 1) // 2', 'last = min(rows, cols) // 2'))
add('spiral_last_ring_line_backwards', 'ci-spiral-cells', 'a last ring of one column is swept from the bottom up', SP.replace('        if p < w:', '        if w == 1 and t > 0:\n            out.append([t + h - 1 - p, t])\n        elif p < w:'))
add('spiral_square_tmax', 'ci-spiral-cells', 'the last ring number taken from the rows alone', SP.replace('last = (min(rows, cols) - 1) // 2', 'last = (rows - 1) // 2'))
add('spiral_float_before', 'ci-spiral-cells', 'the ring found by a float bisection on the area formula', '''
def spiral_cells(rows, cols, ks):
    def before(t):
        return rows * cols - (rows - 2 * t) * (cols - 2 * t)
    out = []
    for k in ks:
        lo, hi = 0.0, (min(rows, cols) - 1) // 2 + 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if before(mid) < k:
                lo = mid
            else:
                hi = mid
        t = int(lo)
        p = k - before(t) - 1
        h, w = rows - 2 * t, cols - 2 * t
        if p < w:
            out.append([t, t + p])
        elif p < w + h - 1:
            out.append([t + p - w + 1, t + w - 1])
        elif p < 2 * w + h - 2:
            out.append([t + h - 1, t + w - 1 - (p - w - h + 2)])
        else:
            out.append([t + h - 1 - (p - 2 * w - h + 3), t])
    return out
''')

# ------------------------------------------------------------ ci-stone-hops
HOPS = '''
from collections import deque

def fewest_hops(stones, lo, hi):
    n = len(stones)
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])
    seen_to = 0
    while queue:
        i = queue.popleft()
        if i == n - 1:
            return dist[i]
        for j in range(max(i + lo, seen_to + 1), min(i + hi, n - 1) + 1):
            if stones[j] == '.':
                dist[j] = dist[i] + 1
                queue.append(j)
        seen_to = max(seen_to, i + hi)
    return -1
'''
add('hops_window_pushed_late', 'ci-stone-hops', 'sliding minimum that takes position j - lo in after using it', '''
from collections import deque

def fewest_hops(stones, lo, hi):
    n = len(stones)
    INF = float('inf')
    dp = [INF] * n
    dp[0] = 0
    dq = deque()
    for j in range(1, n):
        while dq and dq[0] < j - hi:
            dq.popleft()
        if stones[j] == '.' and dq:
            dp[j] = dp[dq[0]] + 1
        i = j - lo
        if i >= 0 and dp[i] < INF:
            while dq and dp[dq[-1]] >= dp[i]:
                dq.pop()
            dq.append(i)
    return -1 if dp[-1] == INF else dp[-1]
''')
add('hops_seen_to_rescan_one', 'ci-stone-hops', 'the scan starts at the furthest place looked at, not one past it', HOPS.replace('seen_to + 1', 'seen_to'))
add('hops_last_hop_ignores_lo', 'ci-stone-hops', 'the end counted as reached once it is within hi, whatever lo', HOPS.replace('''        if i == n - 1:
            return dist[i]''', '''        if i == n - 1:
            return dist[i]
        if i + hi >= n - 1:
            return dist[i] + 1'''))
add('hops_water_stops_scan', 'ci-stone-hops', 'water ends the scan from a stone, as if it could not be hopped over', HOPS.replace('''            if stones[j] == '.':
                dist[j] = dist[i] + 1
                queue.append(j)''', '''            if stones[j] != '.':
                break
            dist[j] = dist[i] + 1
            queue.append(j)'''))
add('hops_seen_to_skips_blocked_window', 'ci-stone-hops', 'the furthest mark is moved to i + hi even when i + lo lies beyond the old mark plus one, which is right; but the mark is clipped to i + lo - 1 when the window was empty', HOPS.replace('seen_to = max(seen_to, i + hi)', 'seen_to = max(seen_to, min(i + hi, n - 1))'))
add('hops_greedy_levels_with_lo', 'ci-stone-hops', 'levels kept as one stretch [a, b] of places, with lo and hi applied to its ends', '''
def fewest_hops(stones, lo, hi):
    n = len(stones)
    if n == 1:
        return 0
    a = b = 0
    hops = 0
    while True:
        na, nb = a + lo, min(b + hi, n - 1)
        if na > n - 1 or na > nb:
            return -1
        cand = [j for j in range(na, nb + 1) if stones[j] == '.']
        hops += 1
        if not cand:
            return -1
        if cand[-1] == n - 1:
            return hops
        if (cand[0], cand[-1]) == (a, b):
            return -1
        a, b = cand[0], cand[-1]
        if hops > n:
            return -1
''')
add('hops_dp_int_inf_small', 'ci-stone-hops', 'sliding minimum, with unreachable marked by n and water places still pushed', '''
from collections import deque

def fewest_hops(stones, lo, hi):
    n = len(stones)
    dp = [n] * n
    dp[0] = 0
    dq = deque()
    for j in range(1, n):
        i = j - lo
        if i >= 0:
            while dq and dp[dq[-1]] >= dp[i]:
                dq.pop()
            dq.append(i)
        while dq and dq[0] < j - hi:
            dq.popleft()
        if stones[j] == '.' and dq:
            dp[j] = min(n, dp[dq[0]] + 1)
    return -1 if dp[-1] >= n else dp[-1]
''')

# ------------------------------------------------------------ ci-stop-cascade
STOP = '''
import heapq

def solve_stop_cascade(text):
    tokens = text.split()
    n = int(tokens[0])
    asks, stops = [], []
    last, volume = None, 0
    out = []

    def buy(qty):
        nonlocal last, volume
        while qty > 0 and asks:
            best = asks[0]
            take = min(qty, best[2])
            qty -= take
            best[2] -= take
            volume += take
            last = best[0]
            if best[2] == 0:
                heapq.heappop(asks)

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
            pos += 3
        while stops and last is not None and stops[0][0] <= last:
            buy(heapq.heappop(stops)[2])
        out.append(f'{last} {volume}' if last is not None else '- 0')
    return '\\n'.join(out)
'''
add('stop_highest_price_ever', 'ci-stop-cascade', 'stops tested against the highest trade price so far, not the last', STOP.replace('    last, volume = None, 0', '    last, volume = None, 0\n    high = 0').replace('nonlocal last, volume', 'nonlocal last, volume, high').replace('            last = best[0]', '            last = best[0]\n            high = max(high, last)').replace('stops[0][0] <= last', 'stops[0][0] <= high'))
add('stop_partial_sell_dropped', 'ci-stop-cascade', 'a sell order is taken off the book when touched, even if part of it is left', STOP.replace('''            if best[2] == 0:
                heapq.heappop(asks)''', '''            heapq.heappop(asks)'''))
add('stop_split_single_space', 'ci-stop-cascade', "lines split on one space, so extra spaces break the parse", '''
import heapq

def solve_stop_cascade(text):
    lines = text.strip().split('\\n')
    n = int(lines[0])
    asks, stops = [], []
    last, volume = None, 0
    out = []
    for seq in range(1, n + 1):
        ev = lines[seq].split(' ')
        qty = 0
        if ev[0] == 'S':
            heapq.heappush(asks, [int(ev[1]), seq, int(ev[2])])
        elif ev[0] == 'T':
            heapq.heappush(stops, (int(ev[1]), seq, int(ev[2])))
        else:
            qty = int(ev[1])
        while True:
            while qty > 0 and asks:
                best = asks[0]
                take = min(qty, best[2])
                qty -= take
                best[2] -= take
                volume += take
                last = best[0]
                if best[2] == 0:
                    heapq.heappop(asks)
            if stops and last is not None and stops[0][0] <= last:
                qty = heapq.heappop(stops)[2]
            else:
                break
        out.append(f'{last} {volume}' if last is not None else '- 0')
    return '\\n'.join(out)
''')
add('stop_last_only_on_full_fill', 'ci-stop-cascade', 'the last price is set only when a sell order is used up', STOP.replace('''            last = best[0]
            if best[2] == 0:
                heapq.heappop(asks)''', '''            if best[2] == 0:
                last = best[0]
                heapq.heappop(asks)'''))
add('stop_fires_on_best_ask', 'ci-stop-cascade', 'a stop fires when the cheapest sell is at or above its price', STOP.replace('while stops and last is not None and stops[0][0] <= last:', 'while stops and ((last is not None and stops[0][0] <= last) or (asks and stops[0][0] <= asks[0][0])):'))
add('stop_merged_into_one_buy', 'ci-stop-cascade', 'every stop in reach added into one buy, once, with no second look after it trades', STOP.replace('''        while stops and last is not None and stops[0][0] <= last:
            buy(heapq.heappop(stops)[2])''', '''        for _ in range(2):
            q = 0
            while stops and last is not None and stops[0][0] <= last:
                q += heapq.heappop(stops)[2]
            if q:
                buy(q)'''))
add('stop_price_levels_stale', 'ci-stop-cascade', 'sells kept as a dict of price levels with a heap of prices; a level that empties is deleted but its price is pushed again only if new', '''
import heapq

def solve_stop_cascade(text):
    tokens = text.split()
    n = int(tokens[0])
    level, prices, stops = {}, [], []
    seen = set()
    last, volume = None, 0
    out = []

    def buy(qty):
        nonlocal last, volume
        while qty > 0 and prices:
            p = prices[0]
            if level.get(p, 0) == 0:
                heapq.heappop(prices)
                continue
            take = min(qty, level[p])
            qty -= take
            level[p] -= take
            volume += take
            last = p

    pos = 1
    for seq in range(n):
        kind = tokens[pos]
        if kind == 'B':
            buy(int(tokens[pos + 1]))
            pos += 2
        else:
            price, qty = int(tokens[pos + 1]), int(tokens[pos + 2])
            if kind == 'S':
                level[price] = level.get(price, 0) + qty
                if price not in seen:
                    seen.add(price)
                    heapq.heappush(prices, price)
            else:
                heapq.heappush(stops, (price, seq, qty))
            pos += 3
        while stops and last is not None and stops[0][0] <= last:
            buy(heapq.heappop(stops)[2])
        out.append(f'{last} {volume}' if last is not None else '- 0')
    return '\\n'.join(out)
''')
add('stop_lines_before_cascade', 'ci-stop-cascade', 'the line for an event is recorded before its stops fire', STOP.replace('''        while stops and last is not None and stops[0][0] <= last:
            buy(heapq.heappop(stops)[2])
        out.append(f'{last} {volume}' if last is not None else '- 0')''', '''        out.append(f'{last} {volume}' if last is not None else '- 0')
        while stops and last is not None and stops[0][0] <= last:
            buy(heapq.heappop(stops)[2])'''))

CANDIDATES = C

# ------------------------------------------------------------ second round
add('grace_both_sides', 'ci-grace-sessions', 'each session widened by the grace on both sides before a plain merge', '''
def merge_with_grace(sessions, grace):
    out = []
    for s, e in sorted(sessions):
        if out and s - grace <= out[-1][1] + grace:
            out[-1][1] = max(out[-1][1], e)
            out[-1][2] += 1
        else:
            out.append([s, e, 1])
    return out
''')
add('robot_blocked_keeps_trying', 'ci-robot-floor', 'right value, but a blocked move does not end its command (constraints[1] rules this out as too slow)', ROBOT.replace('''                if not (0 <= a < rows and 0 <= b < cols) or grid[a][b] == '#':
                    break''', '''                if not (0 <= a < rows and 0 <= b < cols) or grid[a][b] == '#':
                    continue'''))
add('rooms_lazy_release', 'ci-room-numbers', 'busy rooms are released only when no room is free, so a low room that has come free is passed over', '''
import heapq

def room_numbers(meetings, clean):
    order = sorted(range(len(meetings)), key=lambda i: (meetings[i][0], i))
    free, busy, opened = [], [], 0
    rooms = [0] * len(meetings)
    for i in order:
        s, e = meetings[i]
        if not free:
            while busy and busy[0][0] <= s:
                heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            room = heapq.heappop(free)
        else:
            room, opened = opened, opened + 1
        rooms[i] = room
        heapq.heappush(busy, (e + clean, room))
    return rooms
''')
add('stop_buy_remainder_rests', 'ci-stop-cascade', 'the unfilled part of a market buy waits and takes later sells', STOP.replace('    last, volume = None, 0', '    last, volume = None, 0\n    owed = 0').replace('''        if kind == 'B':
            buy(int(tokens[pos + 1]))
            pos += 2''', '''        if kind == 'B':
            before = volume
            want = int(tokens[pos + 1])
            buy(want)
            owed += want - (volume - before)
            pos += 2''').replace('''            if kind == 'S':
                heapq.heappush(asks, [price, seq, qty])''', '''            if kind == 'S':
                heapq.heappush(asks, [price, seq, qty])
                if owed:
                    before = volume
                    buy(owed)
                    owed -= volume - before'''))
add('stop_sell_at_stop_price_trades', 'ci-stop-cascade', 'a waiting stop also fires when a sell arrives at or below its price', STOP.replace('''            if kind == 'S':
                heapq.heappush(asks, [price, seq, qty])''', '''            if kind == 'S':
                heapq.heappush(asks, [price, seq, qty])
                if last is not None and stops and stops[0][0] <= price <= last:
                    buy(heapq.heappop(stops)[2])'''))
add('hops_levels_first_last_stone', 'ci-stone-hops', 'each level kept as its first and last stone only, the next level scanned from first + lo to last + hi', '''
def fewest_hops(stones, lo, hi):
    n = len(stones)
    a = b = 0
    hops = 0
    while b < n - 1:
        na = nb = -1
        for j in range(max(a + lo, b + 1), min(b + hi, n - 1) + 1):
            if stones[j] == '.':
                if na < 0:
                    na = j
                nb = j
        if na < 0:
            return -1
        a, b = na, nb
        hops += 1
    return hops
''')
add('fit_job_inside_gap_needs_whole_minutes_after_start', 'ci-first-fit-slot', 'the walk skips every booking that begins before start, so one running at start is missed unless it is the last such', '''
def first_fit(bookings, start, length):
    slot = start
    for s, e in bookings:
        if s < start and e <= start:
            continue
        if s <= slot < e or slot <= s < slot + length:
            slot = e
''' + JOIN)
add('checks_have_from_tail_run', 'ci-double-checks', 'visits counted from the back of the sorted list only while they are consecutive minutes', '''
import bisect

def fewest_checks(jobs):
    marks = []
    for start, end, need in sorted(jobs, key=lambda job: (job[1], -job[0])):
        have = 0
        i = len(marks) - 1
        while i >= 0 and marks[i] >= start and have < need:
            have += 1
            i -= 1
        minute = end
        while have < need:
            j = bisect.bisect_left(marks, minute)
            if j == len(marks) or marks[j] != minute:
                marks.insert(j, minute)
                have += 1
            minute -= 1
    return len(marks)
''')
add('bit_xor_power_of_two_incl_zero', 'ci-one-bit-apart', 'slow: every pair, with x & (x - 1) == 0 also true for equal codes', '''
def one_bit_pairs(codes):
    total = 0
    for i in range(len(codes)):
        for j in range(i):
            x = codes[i] ^ codes[j]
            if x & (x - 1) == 0:
                total += 1
    return total
''')
add('kbits_popcount_of_lo_added_wrongly', 'ci-k-bit-count', 'count up to hi minus count up to lo, with lo added back when it has k set bits, but tested with bit_count of lo - 1', KB.replace('return [upto(hi, k) - upto(lo - 1, k) for lo, hi, k in queries]', 'return [upto(hi, k) - upto(lo, k) + (1 if lo > 0 and bin(lo - 1).count("1") == k else (1 if lo == 0 and k == 0 else 0)) for lo, hi, k in queries]'))
add('loop_total_then_nonneg_prefix_from_s', 'ci-loop-starts', 'a start is taken when no later prefix dips below it, the lap past depot 0 trusted to the total', '''
def loop_starts(fuel, burn):
    n = len(fuel)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + fuel[i] - burn[i]
    if pre[n] < 0:
        return []
    out, low = [], pre[n]
    for s in range(n - 1, -1, -1):
        if pre[s] <= low:
            out.append(s)
        low = min(low, pre[s])
    return out[::-1]
''')

# these passed every hidden test and then agreed with the model on 6,000 random inputs each
# (verify_passers.py): they are right solutions in another style, not counted as wrong.
EQUIVALENT = ['grace_gap_from_start_sorted_end_desc', 'robot_blocked_turns_round', 'fit_bisect_then_walk',
              'rings_shift_mod_missing_inner', 'loop_suffix_min_only_total_zero_assumed',
              'bonus_cut_at_last_lowest_no_far_end', 'spiral_le_in_search', 'spiral_perimeter_ring_sizes',
              'spiral_square_tmax', 'hops_seen_to_skips_blocked_window', 'hops_dp_int_inf_small',
              'loop_nonneg_gain_and_total', 'stop_sell_at_stop_price_trades',
              'fit_job_inside_gap_needs_whole_minutes_after_start', 'checks_have_from_tail_run']
RIGHT_AFTER_ALL = {k: C.pop(k) for k in EQUIVALENT}
CANDIDATES = C
