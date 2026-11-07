"""brainteasers/homework-1 hw9-l-pieces-6x10: reader's own checks of every number
and claim in the model. A memoised first-empty-cell count of L tilings (reader's
route, column-major frontier), the colour split of every placement, the stripe and
chessboard counts, and the 4a - 30 step."""
from functools import lru_cache
from harness import item, check, finish

_, it = item('brainteasers', 'homework-1', 'hw9-l-pieces-6x10')

base = [(0, 0), (1, 0), (2, 0), (2, 1)]   # line of three down, extra at right angles to an end
def norm(cells):
    mr = min(r for r, c in cells); mc = min(c for r, c in cells)
    return tuple(sorted((r - mr, c - mc) for r, c in cells))
shapes = set()
cells = base
for flip in range(2):
    for _ in range(4):
        cells = [(c, -r) for r, c in cells]
        shapes.add(norm(cells))
    cells = [(r, -c) for r, c in cells]
check(len(shapes) == 8, f'the L has 8 orientations ({len(shapes)})')

def tilings(R, C):
    # cells in column-major order: index c * R + r
    anchored = []
    for s in shapes:
        first = min(s, key=lambda rc: (rc[1], rc[0]))
        anchored.append([(r - first[0], c - first[1]) for r, c in s])
    N = R * C
    @lru_cache(maxsize=None)
    def go(p, rest):
        # rest: filled bits from index p on; every cell before p is filled
        while p < N and rest & 1:
            p += 1; rest >>= 1
        if p == N:
            return 1
        r0, c0 = p % R, p // R
        total = 0
        for a in anchored:
            m = 0
            for dr, dc in a:
                r, c = r0 + dr, c0 + dc
                if not (0 <= r < R and 0 <= c < C):
                    break
                bit = 1 << (c * R + r - p)
                if rest & bit:
                    break
                m |= bit
            else:
                total += go(p, rest | m)
        return total
    return go(0, 0)

for (R, C), want in [((2, 4), 2), ((4, 4), None), ((3, 8), None), ((4, 6), None)]:
    n = tilings(R, C)
    check(n > 0 and (want is None or n == want), f'control {R} x {C}: {n} tilings')
check(tilings(6, 10) == 0, '6 x 10: no tiling by L pieces')
check(tilings(10, 6) == 0, '10 x 6: no tiling by L pieces')
check(tilings(5, 8) > 0, '5 x 8 (area 40, 10 pieces, even) can be tiled, so the parity is the point')

stripe = chess = 0
splits_s, splits_c = set(), set()
for s in shapes:
    for r0 in range(6):
        for c0 in range(10):
            pts = [(r0 + r, c0 + c) for r, c in s]
            if all(r < 6 and c < 10 for r, c in pts):
                splits_s.add(sorted([sum(c % 2 == 0 for r, c in pts), sum(c % 2 for r, c in pts)])[0])
                splits_c.add(sum((r + c) % 2 for r, c in pts))
                stripe += 1
check(splits_s == {1}, 'every placement covers 3 and 1 on column stripes')
check(splits_c == {2}, 'every placement covers 2 and 2 on the chessboard')
dark = sum(1 for r in range(6) for c in range(10) if c % 2 == 0)
check(dark == 30 and 6 * 10 == 15 * 4 == 60, 'stripes give 30 dark of 60; area 60 = 15 x 4')
vals = sorted({4 * a - 30 for a in range(16)}, key=abs)
check(0 not in vals and abs(vals[0]) == 2, f'4a - 30 for a = 0..15 never 0, nearest {vals[:2]}')
# An I piece (four in a line) meets column stripes 2 and 2 or 4 and 0: the prompt's
# "one more beside an end square" admits it, and the stripe step then fails (finding BZ1-1).
i_split = {sum(c % 2 for c in range(c0, c0 + 4)) for c0 in range(7)}
check(i_split == {2}, f'a horizontal I piece covers 2 and 2 on stripes ({i_split}), so the L must be pinned down')
finish()
