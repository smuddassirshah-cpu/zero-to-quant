"""Independent methods and prose-constraint checks for drill pack ci, pack 8, imported by drills-ci-8-check.py.
Each method is written apart from the drill's model solution: brute force on small inputs, a different
algorithm on large ones."""
import heapq, bisect
from collections import Counter, defaultdict, deque
from itertools import accumulate, combinations
from math import comb

# ======================= prose constraints, per drill (AssertionError names the broken rule) =======================

def v_grace(a):
    s, g = a["sessions"], a["grace"]
    assert all(0 <= x <= y <= 10**9 for x, y in s), "0 <= start <= end <= 1e9"
    assert 0 <= g <= 10**9

def v_rest(a):
    t, r = a["tasks"], a["rest"]
    assert all(isinstance(k, str) and k.isalpha() and k.islower() for k in r), "rest keys are names"
    assert all(isinstance(v, int) and 0 <= v <= 10**9 for v in r.values()), "rest 0 to 1e9"
    assert len(t) <= 100000

def v_robot(a):
    tok = a["text"].split()
    r, c = int(tok[0]), int(tok[1])
    assert 1 <= r <= 200 and 1 <= c <= 200, "r, c"
    rows = tok[2:2 + r]
    assert len(rows) == r and all(len(x) == c and set(x) <= set(".#R") for x in rows), "row shape"
    assert "".join(rows).count("R") == 1, "R once"
    cmds = tok[2 + r:]
    assert len(cmds) <= 10000, "commands"
    for k in cmds:
        assert k in ("L", "R") or (k[0] == "F" and k[1:].isdigit() and 1 <= int(k[1:]) <= 1000), f"command {k}"

def v_onebit(a):
    assert len(a["codes"]) <= 100000 and all(0 <= x < 2**30 for x in a["codes"])

def v_switch(a):
    sw, t = a["switches"], a["target"]
    assert len(sw) <= 14 and 1 <= len(t) <= 18
    assert all(len(s) == len(t) and set(s) <= set("01") for s in sw) and set(t) <= set("01"), "same length, 0 and 1"

VALID = {"ci-grace-sessions": v_grace, "ci-rest-days": v_rest, "ci-robot-floor": v_robot,
         "ci-one-bit-apart": v_onebit, "ci-switch-panel": v_switch}

# ======================= independent methods =======================

def merge_with_grace(sessions, grace):
    n = len(sessions)
    if n <= 300:
        # brute force: union every pair whose grace-widened spans meet, then read the groups
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for i in range(n):
            for j in range(n):
                (a, b), (c, d) = sessions[i], sessions[j]
                if a <= c <= b + grace:
                    parent[find(i)] = find(j)
        groups = defaultdict(list)
        for i in range(n):
            groups[find(i)].append(sessions[i])
        out = [[min(x for x, _ in g), max(y for _, y in g), len(g)] for g in groups.values()]
        return sorted(out)
    # large: cut the sorted starts where a start passes the running maximum end plus grace
    order = sorted(sessions)
    ends = list(accumulate((e for _, e in order), max))
    cuts = [0] + [i for i in range(1, n) if order[i][0] > ends[i - 1] + grace] + [n]
    return [[order[a][0], ends[b - 1], b - a] for a, b in zip(cuts, cuts[1:])]

def run_days(tasks, rest):
    if len(tasks) <= 200 and all(v <= 50 for v in rest.values()):
        # brute force: walk the calendar a day at a time
        last, out, day, k = {}, [], 0, 0
        while k < len(tasks):
            day += 1
            m = tasks[k]
            if m not in last or day - last[m] > rest.get(m, 0):
                last[m] = day
                out.append(day)
                k += 1
        return out
    last, out, day = {}, [], 0
    for m in tasks:
        day = day + 1 if m not in last else max(day + 1, last[m] + rest.get(m, 0) + 1)
        last[m] = day
        out.append(day)
    return out

def solve_robot_floor(text):
    # complex numbers for place and heading; each F jumps to the first blocked cell along the line
    tok = text.split()
    r, c = int(tok[0]), int(tok[1])
    rows = tok[2:2 + r]
    open_cells = {complex(i, j) for i in range(r) for j in range(c) if rows[i][j] != "#"}
    pos = next(complex(i, j) for i in range(r) for j in range(c) if rows[i][j] == "R")
    head = complex(-1, 0)
    seen = {pos}
    for k in tok[2 + r:]:
        if k == "L":
            head *= 1j
        elif k == "R":
            head *= -1j
        else:
            n = 0
            while n < int(k[1:]) and pos + head * (n + 1) in open_cells:
                n += 1
            for s in range(1, n + 1):
                seen.add(pos + head * s)
            pos += head * n
    face = {complex(-1, 0): "N", complex(0, 1): "E", complex(1, 0): "S", complex(0, -1): "W"}[head]
    return f"{int(pos.real)} {int(pos.imag)} {face} {len(seen)}"

def one_bit_pairs(codes):
    if len(codes) <= 3000:
        return sum(bin(codes[i] ^ codes[j]).count("1") == 1 for i in range(len(codes)) for j in range(i))
    # by bit: a pair differing only in bit b is (v without b, v with b)
    cnt = Counter(codes)
    return sum(k * cnt.get(v | (1 << b), 0) for b in range(30) for v, k in cnt.items() if not v >> b & 1)

def fewest_switches(switches, target):
    n, want = len(switches), int(target, 2)
    m = [int(s, 2) for s in switches]
    best = None
    for mask in range(1 << n):
        x = 0
        for i in range(n):
            if mask >> i & 1:
                x ^= m[i]
        if x == want:
            key = (bin(mask).count("1"), [i for i in range(n) if mask >> i & 1])
            if best is None or key < best:
                best = key
    return None if best is None else best[1]

INDEP = {"ci-grace-sessions": merge_with_grace, "ci-rest-days": run_days, "ci-robot-floor": solve_robot_floor,
         "ci-one-bit-apart": one_bit_pairs, "ci-switch-panel": fewest_switches}

SLOW_IDX = {"ci-rest-days": [2], "ci-one-bit-apart": [3]}

# ======================= numbers stated in the briefs, recomputed by the independent methods =======================
STATED = {
    "ci-grace-sessions": [(lambda: merge_with_grace([[30, 45], [0, 10], [12, 20], [50, 52], [44, 47]], 2), [[0, 20, 2], [30, 47, 2], [50, 52, 1]]),
                          (lambda: (12 - 10, 50 - 47), (2, 3))],
    "ci-rest-days": [(lambda: run_days(["kiln", "drum", "kiln", "kiln", "drum"], {"kiln": 2, "drum": 0}), [1, 2, 4, 7, 8])],
    "ci-robot-floor": [(lambda: solve_robot_floor("3 3\n...\n.#.\nR..\nF5 R F1 R F4\n"), "0 1 S 4")],
    "ci-one-bit-apart": [(lambda: one_bit_pairs([5, 4, 7, 5, 1]), 6), (lambda: (5 ^ 4, 5 ^ 7, 5 ^ 1), (1, 2, 4))],
    "ci-switch-panel": [(lambda: fewest_switches(["1000", "1100", "0011", "0111"], "1111"), [0, 3]),
                        (lambda: (int("1000", 2) ^ int("0111", 2), int("1100", 2) ^ int("0011", 2)), (15, 15)),
                        (lambda: [s for s in ["1000", "1100", "0011", "0111"] if int(s, 2) == 15], []),
                        (lambda: 0b0110 < 0b1001, True)],
}
