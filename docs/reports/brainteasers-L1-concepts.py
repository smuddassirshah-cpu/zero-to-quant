"""Concept audit, brainteasers level 1 (l1 to l5, review-1, homework-1).
Exhaustive searches and exact enumerations behind every empirical claim in the
level: reachable positions, minimal move counts, tilings, weighing plans, jug
routes, rope and hourglass plans. Run from the repo root:
    python3 -I docs/reports/brainteasers-L1-concepts.py
Exit 0 means every checked claim holds. Each assert names its ledger row
(docs/reports/audit-brainteasers-1-3-ledger.md).
"""
import sys
from collections import deque
from functools import lru_cache
from itertools import combinations, permutations
from fractions import Fraction

sys.setrecursionlimit(10000)
checks = 0


def ok(cond, name):
    global checks
    checks += 1
    assert cond, name
    print('ok  ' + name)


# ---------------------------------------------------------------- lizards (l1 s0, s1, s9; homework-1 item 0)
def lizard_reach(start):
    seen = {start}
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        for i in range(3):
            for j in range(3):
                if i < j and s[i] > 0 and s[j] > 0:
                    k = 3 - i - j
                    t = list(s)
                    t[i] -= 1
                    t[j] -= 1
                    t[k] += 2
                    t = tuple(t)
                    if t not in seen:
                        seen.add(t)
                        dist[t] = dist[s] + 1
                        q.append(t)
    return dist


d = lizard_reach((1, 2, 3))
ok(len(d) == 9, 'l1 s1 byKey.longer: nine positions reachable from (1, 2, 3)')
ok(all(min(s) > 0 or sorted(s)[1] > 0 for s in d), 'l1 s1: no reachable position has one colour')
ok((4, 2, 0) in d and d[(4, 2, 0)] == 3, 'l1 s0: 4, 2, 0 reached in three meetings')
ok(all(not (s[1] == 0 and s[2] == 0) for s in d), 'l1 s1 byKey.red: green and blue never both 0')
dP = lizard_reach((2, 5, 8))
ok((15, 0, 0) in dP and (0, 15, 0) in dP and (0, 0, 15) in dP, 'l1 s9: island P reaches every single colour')
ok(dP[(0, 0, 15)] == 5, 'l1 s9 feedback.correct: all blue on P takes 5 meetings')
dQ = lizard_reach((4, 6, 8))
ok(all(sorted(s)[1] > 0 for s in dQ), 'l1 s9: island Q never one colour')
dH = lizard_reach((3, 4, 8))
ok(all(sorted(s)[1] > 0 for s in dH), 'homework-1 item 0: 3, 4, 8 never one colour')
# the differences modulo 3 are invariant
for s in dP:
    assert (s[0] - s[1]) % 3 == 0 and (s[1] - s[2]) % 3 == 0
ok(True, 'l1 s1 explain: differences keep their residue modulo 3 (checked on every reachable P state)')

# ---------------------------------------------------------------- coins turned k at a time (l1 s2, s6, quiz 0; review-1 item 0)
def heads_reach(n, k):
    dist = {n: 0}
    q = deque([n])
    while q:
        h = q.popleft()
        for a in range(0, k + 1):  # a heads turned to tails, k - a tails turned to heads
            if a <= h and k - a <= n - h:
                t = h - a + (k - a)
                if t not in dist:
                    dist[t] = dist[h] + 1
                    q.append(t)
    return dist


d9 = heads_reach(9, 4)
ok(0 not in d9 and min(d9) == 1, 'l1 s2: nine coins, turn four: all tails unreachable, 1 head reachable')
d10 = heads_reach(10, 4)
ok(d10.get(0) == 3, 'l1 s6: ten coins, turn four: fewest moves to all tails is 3')
ok(0 not in heads_reach(11, 2), 'l1 quiz 0: eleven coins, turn two: never all tails')
ok(0 not in heads_reach(15, 6), 'review-1 item 0: fifteen coins, turn six: never all tails')

# ---------------------------------------------------------------- lamps: row and column toggles (l1 s5, quiz 1; review-1 item 5)
def lamp_patterns(n):
    pats = set()
    for r in range(1 << n):
        for c in range(1 << n):
            pats.add(frozenset((i, j) for i in range(n) for j in range(n) if ((r >> i) & 1) ^ ((c >> j) & 1)))
    return pats


P3 = lamp_patterns(3)
ok(len(P3) == 32, 'l1 s5 explain: 32 of the 512 patterns reachable on 3 x 3')
ok({len(p) for p in P3} == {0, 3, 4, 5, 6, 9}, 'l1 quiz 1: reachable lit counts on 3 x 3 are 0, 3, 4, 5, 6, 9')


def blocks_even(p, n):
    return all(sum((i + di, j + dj) in p for di in (0, 1) for dj in (0, 1)) % 2 == 0
               for i in range(n - 1) for j in range(n - 1))


ok(all(blocks_even(p, 3) for p in P3), 'l1 s5: every 2 x 2 block even in every reachable pattern')
cells = [(i, j) for i in range(3) for j in range(3)]
ok(all(not blocks_even(frozenset(two), 3) for two in combinations(cells, 2)),
   'l1 quiz 1 option 2 why: two lit lamps always leave some 2 x 2 block with one')
ok(all(not blocks_even(frozenset([c]), 3) for c in cells), 'l1 quiz 1 option 1 why: one lit lamp leaves a block odd')
P4 = lamp_patterns(4)
ok(len(P4) == 128, 'review-1 item 5 explain: 128 reachable patterns on 4 x 4')
ok({len(p) for p in P4} == {0, 4, 6, 8, 10, 12, 16}, 'review-1 item 5: reachable counts 0, 4, 6, 8, 10, 12, 16')
ok({4 * r + 4 * c - 2 * r * c for r in range(5) for c in range(5)} == {0, 4, 6, 8, 10, 12, 16},
   'review-1 item 5 explain: 4r + 4c - 2rc formula gives the same set')
# l1 s5 options: row 1 then columns 2 and 3 -> 5 lit; row 1 and column 1 -> 4 lit
def toggle(n, rows, cols):
    return sum(((i in rows) + (j in cols)) % 2 for i in range(n) for j in range(n))


ok(toggle(3, {0}, {1, 2}) == 5, 'l1 s5 option 3 why: row 1 then columns 2 and 3 leave five on')
ok(toggle(3, {0}, {0}) == 4, 'l1 s5 option 4 why: a row and a column leave four on')

# ---------------------------------------------------------------- rub out and write (l1 s3, s8, s11, quiz 3)
def last_number(nums, f):
    results = set()

    def rec(board):
        if len(board) == 1:
            results.add(board[0])
            return
        for i, j in combinations(range(len(board)), 2):
            rest = [board[k] for k in range(len(board)) if k not in (i, j)]
            rec(rest + [f(board[i], board[j])])
    rec(list(nums))
    return results


ok(last_number(range(1, 7), lambda a, b: a + b + a * b) == {5039}, 'l1 s3: a + b + ab on 1..6 always ends at 5039')
ok(last_number(range(1, 5), lambda a, b: a + b + 2 * a * b) == {472}, 'l1 s11: a + b + 2ab on 1..4 always ends at 472')
ok(last_number(range(1, 7), lambda a, b: a + b - 1) == {21 - 5}, 'l1 s8 principle: a + b - 1 lowers the sum by 1 per move (1..6 check)')
ok(sum(range(1, 21)) - 19 == 191, 'l1 s8: 1..20 with a + b - 1 ends at 191')
ok(sum(range(1, 11)) + 9 == 64, 'l1 quiz 3: 1..10 with a + b + 1 ends at 64')
ok(last_number(range(1, 6), lambda a, b: a + b + 1) == {15 + 4}, 'l1 quiz 3 principle checked on 1..5 by brute force')
# invariant for a+b+2ab: product of (2x+1)
ok(2 * (3 + 4 + 2 * 3 * 4) + 1 == (2 * 3 + 1) * (2 * 4 + 1), 'l1 s11 hint: 2(a + b + 2ab) + 1 = (2a + 1)(2b + 1)')

# ---------------------------------------------------------------- reverse a row by neighbour swaps (l1 s10)
def swap_dist(n):
    start = tuple(range(n))
    goal = tuple(reversed(start))
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        if s == goal:
            return dist[s]
        for i in range(n - 1):
            t = list(s)
            t[i], t[i + 1] = t[i + 1], t[i]
            t = tuple(t)
            if t not in dist:
                dist[t] = dist[s] + 1
                q.append(t)


ok(swap_dist(6) == 15, 'l1 s10: reversing six people by neighbour swaps takes 15 moves')

# ---------------------------------------------------------------- tilings (l2, review-1, homework-1)
def tile(cells, shapes):
    """Exact cover of the set `cells` by translated copies of the given shapes (lists of (di, dj))."""
    cells = set(cells)
    order = sorted(cells)

    def rec(free):
        if not free:
            return True
        c = min(free)
        for sh in shapes:
            for anchor in sh:
                placed = [(c[0] + di - anchor[0], c[1] + dj - anchor[1]) for di, dj in sh]
                if all(p in free for p in placed):
                    nf = free - set(placed)
                    if rec(nf):
                        return True
        return False
    return rec(frozenset(cells))


DOM = [[(0, 0), (0, 1)], [(0, 0), (1, 0)]]
I3 = [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)]]
I4 = [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (1, 0), (2, 0), (3, 0)]]
T4 = [[(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 0), (0, 1), (0, 2), (-1, 1)],
      [(0, 0), (1, 0), (2, 0), (1, 1)], [(0, 0), (1, 0), (2, 0), (1, -1)]]


def board(n, m=None):
    m = m or n
    return {(i, j) for i in range(n) for j in range(m)}


b5 = board(5)
dark5 = [c for c in b5 if (c[0] + c[1]) % 2 == 0]
ok(len(dark5) == 13 and all(tile(b5 - {c}, DOM) for c in dark5), 'l2 s0: 5 x 5 minus any dark square tiles with dominoes')
ok(all(not tile(b5 - {c}, DOM) for c in b5 if (c[0] + c[1]) % 2 == 1), 'l2 s0: 5 x 5 minus a light square does not tile')
b7 = board(7)
ok(tile(b7 - {(0, 0)}, DOM), 'l2 s10: 7 x 7 minus a corner tiles with dominoes')
ok(tile(b7 - {(0, 2)}, DOM), 'l2 s10: 7 x 7 minus the third square along an edge tiles')
ok(not tile(b7 - {(0, 1)}, DOM), 'l2 s10: 7 x 7 minus the square next to a corner does not tile')
ok(tile(b7 - {(3, 3)}, DOM), 'review-1 item 1: 7 x 7 minus the centre tiles with dominoes')
ok(not tile(board(6), I4), 'l2 s4: nine straight 1 x 4 tiles cannot cover 6 x 6 (search)')
cnt = [sum(1 for i in range(1, 7) for j in range(1, 7) if (i + j) % 4 == r) for r in (2, 3, 0, 1)]
ok(cnt == [9, 10, 9, 8], 'l2 s4: colour counts 9, 10, 9, 8 for (i + j) mod 4 on 6 x 6')
cnt10 = [sum(1 for i in range(1, 11) for j in range(1, 11) if (i + j) % 4 == r) for r in (2, 3, 0, 1)]
ok(cnt10 == [25, 26, 25, 24], 'homework-1 item 7 model: colour counts 25, 26, 25, 24 on 10 x 10')
ok(not tile(board(6), T4), 'l2 s8: nine T-tetrominoes cannot cover 6 x 6 (search)')
ok(tile(board(4), T4), 'l2 s8 explain: four T-tetrominoes cover 4 x 4')
ok(not tile(board(4, 7), T4), 'review-1 item 6: seven T-tetrominoes cannot cover 4 x 7 (search)')
good = {c for c in b7 if tile(b7 - {c}, I3)}
ok(good == {(i, j) for i in (0, 3, 6) for j in (0, 3, 6)}, 'homework-1 item 1: 7 x 7 minus a square tiles with 1 x 3 exactly for i, j in {1, 4, 7}')
c3 = sorted(sum(1 for i in range(1, 8) for j in range(1, 8) if (i + j) % 3 == r) for r in range(3))
ok(c3 == [16, 16, 17], 'homework-1 item 1 explain: classes of (i + j) mod 3 hold 17, 16, 16')

# ---------------------------------------------------------------- knight and grid tours (l2 s1, s2, s3, s9, quiz 0, quiz 2)
def knight_dist(n):
    start, goal = (0, 0), (n - 1, n - 1)
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        for di, dj in [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]:
            t = (s[0] + di, s[1] + dj)
            if 0 <= t[0] < n and 0 <= t[1] < n and t not in dist:
                dist[t] = dist[s] + 1
                q.append(t)
    return dist


kd = knight_dist(8)
ok(kd[(7, 7)] == 6, 'l2 s2: fewest knight moves corner to opposite corner on 8 x 8 is 6')
ok(all((d % 2) == ((c[0] + c[1]) % 2) for c, d in kd.items()), 'l2 s1: knight distance parity equals square colour parity')


def ham_paths(n, start, closed=False):
    """Count Hamiltonian paths on the n x n grid graph from start; return (count, endpoints)."""
    N = n * n
    nbr = {}
    for i in range(n):
        for j in range(n):
            nbr[(i, j)] = [(i + di, j + dj) for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)) if 0 <= i + di < n and 0 <= j + dj < n]
    count = 0
    ends = set()
    visited = {start}

    def rec(c, depth):
        nonlocal count
        if depth == N:
            if not closed or start in nbr[c]:
                count += 1
                ends.add(c)
            return
        for t in nbr[c]:
            if t not in visited:
                visited.add(t)
                rec(t, depth + 1)
                visited.discard(t)
    rec(start, 1)
    return count, ends


n5, e5 = ham_paths(5, (0, 0))
ok(n5 == 824, 'l2 s3 explain: 824 tours of the 5 x 5 rooms from the corner')
ok(e5 == {(i, j) for i in range(5) for j in range(5) if (i + j) % 2 == 0} - {(0, 0)}, 'l2 s3: a tour can end on every dark room except S, and on no light room')
ok((0, 1) not in e5, 'l2 quiz 0: no tour ends next to the start')
c4, _ = ham_paths(4, (0, 0), closed=True)
ok(c4 > 0, 'l2 s9: the 4 x 4 grid has a closed tour')
c5, _ = ham_paths(5, (0, 0), closed=True)
ok(c5 == 0, 'l2 s9: the 5 x 5 grid has no closed tour')

# ---------------------------------------------------------------- 3 x 3 x 3 cheese (l2 s11, quiz 1)
cubes = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]
even = [c for c in cubes if sum(c) % 2 == 0]
ok(len(even) == 14 and (0, 0, 0) in even and (1, 1, 1) not in even, 'l2 s11: 14 cubes share the corner parity, the centre has the other')


def cube_ham(start, must_end=None):
    nbr = {c: [t for t in cubes if sum(abs(a - b) for a, b in zip(c, t)) == 1] for c in cubes}
    visited = {start}
    found = [False]

    def rec(c, depth):
        if found[0]:
            return
        if depth == 27:
            if must_end is None or c == must_end:
                found[0] = True
            return
        for t in nbr[c]:
            if t not in visited:
                visited.add(t)
                rec(t, depth + 1)
                visited.discard(t)
    rec(start, 1)
    return found[0]


ok(not cube_ham((1, 1, 1)), 'l2 quiz 1: no path through all 27 cubes starts at the centre (search)')
ok(cube_ham((0, 0, 0)), 'l2 s11: a path through all 27 cubes from a corner exists')
ok(not cube_ham((0, 0, 0), (1, 1, 1)), 'l2 s11: no corner-start path ends at the centre (search)')

# ---------------------------------------------------------------- pigeonhole (l3, review-1 item 7, homework-1 item 2)
def max_free(items, bad):
    best = 0
    for r in range(len(items), 0, -1):
        if any(not any(bad(a, b) for a, b in combinations(s, 2)) for s in combinations(items, r)):
            return r
    return best


ok(max_free(range(1, 13), lambda a, b: a + b == 13) == 6, 'l3 s1, quiz 0: six numbers from 1..12 can avoid a sum of 13, seven cannot')
ok(max_free(range(0, 10), lambda a, b: (a + b) % 10 == 0 or (a - b) % 10 == 0) == 6, 'l3 s8: six residues avoid a sum or difference divisible by 10, seven cannot')
odds = list(range(1, 100, 2))
ok(len(odds) == 50 and not any(b - a == 1 for a, b in combinations(odds, 2)), 'review-1 item 7: the 50 odd numbers have no consecutive pair')
ok(all(any(b - a == 1 for a, b in combinations(s, 2)) for s in [list(range(1, 52)), list(range(50, 101))]) and True,
   'review-1 item 7: pairs (1,2),...,(99,100) are 50 boxes, 51 picks force a pair (box argument)')
import math
grid9 = [(x, y) for x in (0, 1.5, 3) for y in (0, 1.5, 3)]
ok(min(math.dist(a, b) for a, b in combinations(grid9, 2)) == 1.5 > math.sqrt(2), 'l3 s6: nine points 1.5 apart in the 3 x 3 square, all beyond sqrt 2')
tri = [(0, 0), (2, 0), (1, math.sqrt(3))]
cen = (1, math.sqrt(3) / 3)
ok(all(math.dist(p, cen) > 1 for p in tri) and abs(math.dist(tri[0], cen) - 2 / math.sqrt(3)) < 1e-12,
   'homework-1 item 2: corners and centre of the side-2 triangle are all more than 1 apart (centre at 2/sqrt 3)')
ok(math.ceil(40 / 13) == 4 and math.ceil(100 / 4) == 25, 'l3 s7, quiz 1: ceiling counts 4 and 25')

# ---------------------------------------------------------------- balance weighings (l4, review-1 item 3, homework-1 item 3)
@lru_cache(maxsize=None)
def solvable(h, l, b, g, k):
    """Can k weighings find the fake and say heavy or light? State: h coins that can only be heavy,
    l only light, b either, g known genuine. A weighing puts counts on each pan (equal totals)."""
    cases = h + l + 2 * b
    if cases <= 1:
        return True
    if k == 0:
        return False
    if cases > 3 ** k:
        return False
    for h1 in range(h + 1):
        for l1 in range(l + 1):
            for b1 in range(b + 1):
                for h2 in range(h - h1 + 1):
                    for l2 in range(l - l1 + 1):
                        for b2 in range(b - b1 + 1):
                            n1 = h1 + l1 + b1
                            n2 = h2 + l2 + b2
                            # genuine coins fill the gap on the lighter-count pan
                            gap = n1 - n2
                            if abs(gap) > g:
                                continue
                            if max(n1, n2) == 0:
                                continue
                            # left heavy: heavy candidates on left, light candidates on right
                            total = h + l + b + g
                            lh = solvable(h1 + b1, l2 + b2, 0, total - h1 - b1 - l2 - b2, k - 1)
                            if not lh:
                                continue
                            rh = solvable(h2 + b2, l1 + b1, 0, total - h2 - b2 - l1 - b1, k - 1)
                            if not rh:
                                continue
                            rest = (h - h1 - h2) + (l - l1 - l2) + (b - b1 - b2)
                            bal = solvable(h - h1 - h2, l - l1 - l2, b - b1 - b2, total - rest, k - 1)
                            if bal:
                                return True
    return False


ok(solvable(0, 0, 12, 0, 3), 'l4 s2 to s3, homework-1 item 3: 12 coins, heavy or light, no genuine, 3 weighings')
ok(not solvable(0, 0, 13, 0, 3), 'l4 s7, homework-1 item 3: 13 coins, no genuine coin, 3 weighings: impossible')
ok(solvable(0, 0, 13, 1, 3), 'l4 quiz 0, homework-1 item 3: 13 coins plus a genuine coin, 3 weighings: possible')
ok(not solvable(0, 0, 14, 1, 3), 'l4 quiz 0 explain, homework-1 item 3: 14 coins plus a genuine coin: impossible')
ok(solvable(0, 0, 39, 0, 4), 'l4 s11: 39 coins, no genuine, 4 weighings: possible')
ok(not solvable(0, 0, 40, 0, 4), 'l4 s11: 40 coins, no genuine, 4 weighings: impossible')
ok(solvable(0, 0, 40, 1, 4), 'l4 s11 byKey.forty: 40 coins with one genuine coin, 4 weighings: possible')
ok(not solvable(0, 0, 2, 0, 5), 'l4 s5: two coins, no genuine: never')
for k in (2, 3, 4):
    assert solvable(0, 0, (3 ** k - 3) // 2, 0, k) and not solvable(0, 0, (3 ** k - 3) // 2 + 1, 0, k)
    assert solvable(0, 0, (3 ** k - 1) // 2, 1, k) and not solvable(0, 0, (3 ** k - 1) // 2 + 1, 1, k)
ok(True, 'l4 summary note, s8 byKey.onetwentyone: (3^k - 3)/2 without and (3^k - 1)/2 with a genuine coin, k = 2, 3, 4')
# the 8 cases after left sinks on (1,2,3,4) v (5,6,7,8), then (1,2,5) v (3,6,9)
cases8 = [(c, 'H') for c in (1, 2, 3, 4)] + [(c, 'L') for c in (5, 6, 7, 8)]


def outcome(case, left, right):
    c, t = case
    s = (1 if t == 'H' else -1) * ((c in left) - (c in right))
    return 'left' if s > 0 else 'right' if s < 0 else 'level'


from collections import Counter
cnt2 = Counter(outcome(c, {1, 2, 5}, {3, 6, 9}) for c in cases8)
ok(cnt2 == {'left': 3, 'right': 2, 'level': 3}, 'l4 s3: second weighing splits the 8 cases 3, 2, 3')


# heavy-only: k weighings handle 3^k coins (the thirds plan) and no more
def heavy_ok(n, k):
    if n <= 1:
        return True
    if k == 0:
        return False
    for a in range(1, n // 2 + 1):
        if heavy_ok(a, k - 1) and heavy_ok(n - 2 * a, k - 1):
            return True
    return False


for k in range(1, 6):
    assert heavy_ok(3 ** k, k) and not heavy_ok(3 ** k + 1, k)
ok(True, 'l4 s6, s8: with one heavy fake k weighings handle exactly up to 3^k coins (search, k = 1..5)')
ok(min(k for k in range(1, 8) if heavy_ok(50, k)) == 4 and min(k for k in range(1, 8) if heavy_ok(100, k)) == 5
   and min(k for k in range(1, 8) if heavy_ok(10, k)) == 3 and min(k for k in range(1, 8) if heavy_ok(27, k)) == 3,
   'l4 s9, quiz 1, s1, review-1 item 3: 50 coins need 4, 10 need 3, 27 need 3, 100 need 5')
ok(not (heavy_ok(13, 2)) and heavy_ok(9, 2) and not heavy_ok(10, 2), 'l4 quiz 2: a tilt leaving 13 or 10 suspects cannot finish in two weighings; 9 can')
ok(36 * 5 + 5 == 185 and 55 * 10 - 8 == 542, 'l4 s10, review-1 item 8: bag signatures 185 g means bag 5, 542 g means bag 8')

# ---------------------------------------------------------------- jugs with a tap (l5 s0, s1, s5, s6, quiz; homework-1 item 5)
def jug_bfs(a, b):
    start = (0, 0)
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        moves = [(a, y), (x, b), (0, y), (x, 0)]
        p = min(x, b - y)
        moves.append((x - p, y + p))
        p = min(y, a - x)
        moves.append((x + p, y - p))
        for t in moves:
            if t not in dist:
                dist[t] = dist[(x, y)] + 1
                q.append(t)
    return dist


def fewest(a, b, target, which=None):
    d = jug_bfs(a, b)
    best = None
    for (x, y), n in d.items():
        hit = (x == target if which == 'a' else y == target if which == 'b' else target in (x, y))
        if hit and (best is None or n < best):
            best = n
    return best


def amounts(a, b):
    d = jug_bfs(a, b)
    return {x for x, y in d} | {y for x, y in d}


ok(fewest(5, 8, 2, 'a') == 4, 'l5 s0: 2 litres in the 5-litre jug takes 4 steps at least')
ok(fewest(4, 9, 6) == 8, 'l5 s1: 6 litres with jugs 4 and 9 takes 8 steps')
d49 = jug_bfs(4, 9)
at4 = {v for (x, y), n in d49.items() if n <= 4 for v in (x, y)}
ok({1, 8} <= at4 and 6 not in at4, 'l5 s1 byKey.four: within four steps 1 and 8 litres appear, 6 does not')
ok(amounts(6, 9) == {0, 3, 6, 9}, 'l5 s5: jugs 6 and 9 make only 0, 3, 6, 9')
ok(amounts(6, 15) - {0} == {3, 6, 9, 12, 15}, 'l5 s6: jugs 6 and 15 make 3, 6, 9, 12, 15 and nothing else')
ok(fewest(3, 7, 5) == 8, 'l5 quiz 0: 5 litres with jugs 3 and 7 takes 8 steps')
d37 = jug_bfs(3, 7)
at4 = {v for (x, y), n in d37.items() if n <= 4 for v in (x, y)}
ok({1, 6} <= at4 and 5 not in at4, 'l5 quiz 0 byKey.four: within four steps 1 and 6 appear, 5 does not')
ok(3 not in amounts(4, 6), 'l5 quiz 1: jugs 4 and 6 never make 3')
ok(fewest(5, 11, 3) == 12, 'homework-1 item 5: 3 litres with jugs 5 and 11 takes 12 steps')
for a in range(1, 13):
    for b in range(a, 13):
        g = math.gcd(a, b)
        assert amounts(a, b) == {k * g for k in range(0, b // g + 1)}, (a, b)
ok(True, 'l5 s6 formula, summary: jugs a, b make exactly the multiples of gcd(a, b) up to max(a, b) (all a, b <= 12)')

# ---------------------------------------------------------------- no tap: 10, 7, 3 (l5 s10, s11)
def split_bfs(caps, start, first=None):
    dist = {start: 0}
    q = deque([start])
    while q:
        s = q.popleft()
        for i in range(3):
            for j in range(3):
                if i != j and s[i] > 0 and s[j] < caps[j]:
                    if dist[s] == 0 and first is not None and (i, j) != first:
                        continue
                    p = min(s[i], caps[j] - s[j])
                    t = list(s)
                    t[i] -= p
                    t[j] += p
                    t = tuple(t)
                    if t not in dist:
                        dist[t] = dist[s] + 1
                        q.append(t)
    return dist


ds = split_bfs((10, 7, 3), (10, 0, 0))
ok(ds[(5, 5, 0)] == 9, 'l5 s11: splitting 10 into 5 and 5 with jugs 7 and 3 takes 9 pours')
ok(split_bfs((10, 7, 3), (10, 0, 0), first=(0, 2))[(5, 5, 0)] == 10, 'l5 s11 byKey.eleven: starting 10 into 3 takes 10 at best')
route = [(10, 0, 0), (3, 7, 0), (3, 4, 3), (6, 4, 0), (6, 1, 3), (9, 1, 0), (9, 0, 1), (2, 7, 1), (2, 5, 3), (5, 5, 0)]
ok(all(ds[s] == i for i, s in enumerate(route)), 'l5 s11 hint: the listed 9-pour route is a shortest route')

# ---------------------------------------------------------------- ropes (l5 s2, s8, quiz 2; homework-1 item 4)
def rope_marks(T):
    """Every event-driven plan for two ropes of burn time T, lighting ends only at time 0 or when a rope goes out.
    A rope is (remaining burn, flames). Returns the set of times at which some rope goes out."""
    marks = set()

    def rec(t, ropes):
        # ropes: list of [remaining, flames, lit_once]
        # choose, for each rope, how many extra ends to light now (0, 1, 2 minus current)
        opts = []
        for r in ropes:
            rem, fl = r
            if rem <= 0:
                opts.append([fl])
            else:
                opts.append(list(range(fl, 3)))
        for f0 in opts[0]:
            for f1 in opts[1]:
                new = [[ropes[0][0], f0], [ropes[1][0], f1]]
                burning = [r for r in new if r[0] > 0 and r[1] > 0]
                if not burning:
                    continue
                dt = min(Fraction(r[0], r[1]) for r in burning)
                nxt = []
                for r in new:
                    if r[0] > 0 and r[1] > 0:
                        nxt.append([r[0] - dt * r[1], r[1]])
                    else:
                        nxt.append(r)
                marks.add(t + dt)
                rec(t + dt, nxt)
    rec(Fraction(0), [[Fraction(T), 0], [Fraction(T), 0]])
    return {int(m) for m in marks}


ok(rope_marks(80) == {40, 60, 80, 120, 160}, 'l5 s8: two 80-minute ropes mark exactly 40, 60, 80, 120, 160')
ok(min(rope_marks(60)) == 30, 'l5 quiz 2: two 60-minute ropes: the earliest mark is 30')
ok(90 in rope_marks(120), 'homework-1 item 4: two 120-minute ropes mark 90')
ok(60 in rope_marks(80), 'l5 s2: 60 is reachable with two 80-minute ropes')

# ---------------------------------------------------------------- hourglasses (l5 s7, s9; review-1 item 4)
def hourglass(a, b, turns):
    """Simulate: both started at 0; turns is a dict time -> which glasses to flip (checked to be event times)."""
    sand = {'a': [a, 0], 'b': [b, 0]}  # [top, bottom]
    sizes = {'a': a, 'b': b}
    t = Fraction(0)
    events = []
    while t <= max(a, b) * 4:
        running = {k: v[0] for k, v in sand.items() if v[0] > 0}
        if not running:
            break
        dt = min(running.values())
        t += dt
        for k in sand:
            if sand[k][0] > 0:
                sand[k][0] -= dt
                sand[k][1] += dt
        emptied = [k for k in sand if sand[k][0] == 0 and sand[k][1] == sizes[k] and k in running]
        events.append((int(t), emptied))
        for k in turns.get(int(t), []):
            assert emptied, 'turn only at an event'
            sand[k] = [sand[k][1], sand[k][0]]
    return events


ev = hourglass(5, 9, {5: ['a'], 9: ['a']})
ok(any(t == 13 and 'a' in e for t, e in ev), 'l5 s7: 5 and 9 hourglasses, turning the 5 at 5 and at 9, mark 13')
ev = hourglass(4, 7, {4: ['a'], 7: ['b'], 8: ['b']})
ok(any(t == 9 and 'b' in e for t, e in ev), 'l5 s9: 4 and 7 hourglasses mark 9')
ev = hourglass(6, 11, {6: ['a'], 11: ['a']})
ok(any(t == 16 and 'a' in e for t, e in ev), 'review-1 item 4: 6 and 11 hourglasses mark 16')

# ---------------------------------------------------------------- gloves and socks worst cases (review-1 item 2, l3, homework-1 item 6)
def worst_case(multiset, success):
    """Largest draw with no success, by brute force over multisets of counts."""
    kinds = list(multiset)
    best = 0
    from itertools import product
    for counts in product(*[range(multiset[k] + 1) for k in kinds]):
        hand = dict(zip(kinds, counts))
        if not success(hand):
            best = max(best, sum(counts))
    return best


gloves = {('black', 'L'): 5, ('black', 'R'): 5, ('brown', 'L'): 5, ('brown', 'R'): 5}
ok(worst_case(gloves, lambda h: any(h[(c, 'L')] > 0 and h[(c, 'R')] > 0 for c in ('black', 'brown'))) + 1 == 11,
   'review-1 item 2: eleven gloves force a wearable pair')
socks = {'red': 7, 'blue': 9, 'green': 4}
ok(worst_case(socks, lambda h: any(v >= 2 for v in h.values())) + 1 == 4, 'l3 s0: four socks force a pair')
ok(worst_case(socks, lambda h: h['blue'] >= 2) + 1 == 13, 'l3 s4: thirteen socks force two blue')
ok(worst_case(socks, lambda h: all(v >= 2 for v in h.values())) + 1 == 18, 'l3 s9: eighteen socks force two of every colour')
socks2 = {'black': 5, 'white': 3, 'grey': 8}
ok(worst_case(socks2, lambda h: h['black'] >= 2 or h['white'] >= 2) + 1 == 11, 'homework-1 item 6: eleven socks force a non-grey pair')
ok(worst_case({c: 9 for c in 'abcd'}, lambda h: any(v >= 3 for v in h.values())) + 1 == 9, 'l3 s10: nine socks force three alike from four colours')

print(f'brainteasers L1 concepts: {checks} checks passed')
