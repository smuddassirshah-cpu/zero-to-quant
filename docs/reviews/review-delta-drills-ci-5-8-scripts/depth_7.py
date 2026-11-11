"""Pack 7: how deep does a natural remembered recursion go on each hidden test of the
six drills the fix pass resized? Usage (repo root): python3 depth_7.py

The first reader measured on the drill page: an `lru_cache` recursion passes 450 calls
deep and stops Python at 500; with a generator expression held in each call it passes
200 and fails at 250. This script cannot run the page. It counts calls on the stack
(my own top-down solutions, checked against every `expect`) and reports the deepest
test, so the sizes can be read against those two bands."""
import json
import sys
from functools import lru_cache

sys.setrecursionlimit(20000)
D = 'app/content/drills'
MOD = 1_000_000_007
depth = [0, 0]      # current, deepest


def counted(f):
    def g(*a):
        depth[0] += 1
        if depth[0] > depth[1]:
            depth[1] = depth[0]
        try:
            return f(*a)
        finally:
            depth[0] -= 1
    return g


def merge_ways(a, b, tape):
    if len(a) + len(b) != len(tape):
        return 0

    @lru_cache(None)
    @counted
    def go(i, j):
        if i == len(a) and j == len(b):
            return 1
        w = 0
        if i < len(a) and a[i] == tape[i + j]:
            w += go(i + 1, j)
        if j < len(b) and b[j] == tape[i + j]:
            w += go(i, j + 1)
        return w % MOD
    return go(0, 0)


def solve_mirror_pieces(text):
    tok = text.split()
    out = []
    for tape in tok[1:1 + int(tok[0])]:
        n = len(tape)

        @lru_cache(None)
        @counted
        def cut(s):
            if s == n:
                return 0
            return 1 + min(cut(e) for e in range(s + 1, n + 1) if tape[s:e] == tape[s:e][::-1])
        out.append(str(cut(0)))
    return '\n'.join(out)


def solve_priced_edits(text):
    tok = text.split()
    ins, dele, rep = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]

        @lru_cache(None)
        @counted
        def go(i, j):
            if i == len(s):
                return (len(t) - j) * ins
            if j == len(t):
                return (len(s) - i) * dele
            return min(dele + go(i + 1, j), ins + go(i, j + 1),
                       (0 if s[i] == t[j] else rep) + go(i + 1, j + 1))
        out.append(str(go(0, 0)))
    return '\n'.join(out)


def tolerant_common(a, b, tol):
    @lru_cache(None)
    @counted
    def go(i, j):
        if i == len(a) or j == len(b):
            return 0
        v = max(go(i + 1, j), go(i, j + 1))
        if abs(a[i] - b[j]) <= tol:
            v = max(v, 1 + go(i + 1, j + 1))
        return v
    return go(0, 0)


def long_mirrors(tape, k):
    @lru_cache(None)
    @counted
    def pal(i, j):
        return i >= j or (tape[i] == tape[j] and pal(i + 1, j - 1))
    return sum(1 for i in range(len(tape)) for j in range(i + k - 1, len(tape)) if pal(i, j))


def drop_point_routes(grid):
    R, C = len(grid), len(grid[0])

    @lru_cache(None)
    @counted
    def go(r, c, met):
        if r >= R or c >= C or grid[r][c] == '#':
            return 0
        met = met or grid[r][c] == 'P'
        if r == R - 1 and c == C - 1:
            return 1 if met else 0
        return sum(go(r + dr, c + dc, met) for dr, dc in ((0, 1), (1, 0))) % MOD
    return go(0, 0, False)


FORMS = {
    'ci-merged-tape': (merge_ways, 'plain calls'),
    'ci-mirror-pieces': (solve_mirror_pieces, 'a generator in each call'),
    'ci-priced-edits': (solve_priced_edits, 'plain calls'),
    'ci-tolerant-common': (tolerant_common, 'plain calls'),
    'ci-long-mirrors': (long_mirrors, 'plain calls'),
    'ci-drop-point-routes': (drop_point_routes, 'a generator in each call'),
}


def main():
    bad = 0
    for did, (fn, form) in FORMS.items():
        d = json.load(open(f'{D}/{did}.json'))
        deepest = (0, None)
        for kind in ('examples', 'tests'):
            for i, t in enumerate(d[kind]):
                depth[0] = depth[1] = 0
                got = eval(t['call'], {d['fn']: fn})
                if got != eval(t['expect']):
                    bad += 1
                    print('TOP-DOWN DISAGREES', did, kind, i, got, t['expect'])
                if depth[1] > deepest[0]:
                    deepest = (depth[1], f'{kind}[{i}]')
        band = 250 if 'generator' in form else 500
        safe = 200 if 'generator' in form else 450
        verdict = 'inside the band that passed' if deepest[0] <= safe else (
            'BETWEEN the passing and the failing depth' if deepest[0] < band else 'AT OR PAST the failing depth')
        print('%-22s deepest %4d calls at %-10s (%s; passed at %d, failed at %d): %s'
              % (did, deepest[0], deepest[1], form, safe, band, verdict))
    sys.exit(1 if bad else 0)


main()
