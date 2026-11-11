"""Pack 7 extras. Usage (repo root): python3 extra_7.py
Plain brute forces for the ten drills whose tests changed in the fix pass, on every
example and hidden test small enough, then against the model on random small inputs.
Also the arithmetic of the hold-limit example note (finding 1 of pack 7)."""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brute_lib import run_brutes  # noqa: E402

MOD = 1_000_000_007


def b_routes(grid):
    R, C = len(grid), len(grid[0])

    def go(r, c, met):
        if r >= R or c >= C or grid[r][c] == '#':
            return 0
        met = met or grid[r][c] == 'P'
        if (r, c) == (R - 1, C - 1):
            return int(met)
        return go(r + 1, c, met) + go(r, c + 1, met)
    return go(0, 0, False) % MOD


def b_mirrors(tape, k):
    return sum(1 for i in range(len(tape)) for j in range(i + 1, len(tape) + 1)
               if j - i >= k and tape[i:j] == tape[i:j][::-1])


def b_merge(a, b, tape):
    n = len(tape)
    tot = 0
    for pick in itertools.combinations(range(n), len(a)) if len(a) <= n else ():
        s = set(pick)
        if ''.join(tape[i] for i in pick) == a and ''.join(tape[i] for i in range(n) if i not in s) == b:
            tot += 1
    return tot % MOD


def b_pieces(text):
    tok = text.split()
    out = []
    for tape in tok[1:1 + int(tok[0])]:
        n = len(tape)
        best = n
        for cuts in range(1 << (n - 1)):
            parts, start = [], 0
            for i in range(n - 1):
                if cuts >> i & 1:
                    parts.append(tape[start:i + 1])
                    start = i + 1
            parts.append(tape[start:])
            if len(parts) < best and all(p == p[::-1] for p in parts):
                best = len(parts)
        out.append(str(best))
    return '\n'.join(out)


def b_edits(text):
    tok = text.split()
    ins, dele, rep = int(tok[0]), int(tok[1]), int(tok[2])
    out = []
    for k in range(int(tok[3])):
        s, t = tok[4 + 2 * k], tok[5 + 2 * k]

        def go(i, j):
            if i == len(s):
                return (len(t) - j) * ins
            if j == len(t):
                return (len(s) - i) * dele
            return min(dele + go(i + 1, j), ins + go(i, j + 1), (0 if s[i] == t[j] else rep) + go(i + 1, j + 1))
        out.append(str(go(0, 0)))
    return '\n'.join(out)


def b_tolerant(a, b, tol):
    best = 0
    for size in range(1, min(len(a), len(b)) + 1):
        ok = False
        for ia in itertools.combinations(range(len(a)), size):
            for ib in itertools.combinations(range(len(b)), size):
                if all(abs(a[x] - b[y]) <= tol for x, y in zip(ia, ib)):
                    ok = True
                    break
            if ok:
                break
        if not ok:
            break
        best = size
    return best


def _is_sub(s, t):
    it = iter(t)
    return all(ch in it for ch in s)


def b_three(a, b, c):
    for size in range(len(a), 0, -1):
        for idx in itertools.combinations(range(len(a)), size):
            s = ''.join(a[i] for i in idx)
            if _is_sub(s, b) and _is_sub(s, c):
                return size
    return 0


def b_smooth(sizes, d):
    return sum(1 for p in set(itertools.permutations(sizes)) if all(abs(x - y) <= d for x, y in zip(p, p[1:])))


def b_hold(weights, values, cap, k):
    best = 0
    n = len(weights)
    for mask in range(1 << n):
        if bin(mask).count('1') <= k and sum(weights[i] for i in range(n) if mask >> i & 1) <= cap:
            best = max(best, sum(values[i] for i in range(n) if mask >> i & 1))
    return best


def b_trace(board, word):
    R, C = len(board), len(board[0])

    def go(r, c, i):
        if board[r][c] != word[i]:
            return 0
        if i == len(word) - 1:
            return 1
        return sum(go(nr, nc, i + 1) for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
                   if 0 <= nr < R and 0 <= nc < C)
    return sum(go(r, c, 0) for r in range(R) for c in range(C)) % MOD


def _grid(r, alphabet, fix_corners=None):
    R, C = r.randint(1, 4), r.randint(1, 4)
    g = [[r.choice(alphabet) for _ in range(C)] for _ in range(R)]
    if fix_corners:
        for (y, x) in ((0, 0), (R - 1, C - 1)):
            if g[y][x] == '#':
                g[y][x] = '.'
    return [''.join(row) for row in g]


def _word(r, alphabet, lo, hi):
    return ''.join(r.choice(alphabet) for _ in range(r.randint(lo, hi)))


def _gen_merge(r):
    a, b = _word(r, 'ab', 0, 4), _word(r, 'ab', 0, 4)
    if r.random() < 0.7:
        pos = sorted(r.sample(range(len(a) + len(b)), len(a)))
        ia, ib = iter(a), iter(b)
        tape = ''.join(next(ia) if i in pos else next(ib) for i in range(len(a) + len(b)))
    else:
        tape = _word(r, 'ab', 0, 8)
    return a, b, tape


BRUTES = {
    'ci-drop-point-routes': (b_routes, lambda a: len(a[0]) * len(a[0][0]) <= 30,
                             lambda r: (_grid(r, '..P#', True),)),
    'ci-long-mirrors': (b_mirrors, lambda a: True, lambda r: (_word(r, 'ab', 1, 9), r.randint(1, 5))),
    'ci-merged-tape': (b_merge, lambda a: len(a[2]) <= 14, _gen_merge),
    'ci-mirror-pieces': (b_pieces, lambda a: all(len(t) <= 14 for t in a[0].split()[1:]),
                         lambda r: ('2\n' + _word(r, 'ab', 1, 9) + '\n' + _word(r, 'abc', 1, 9) + '\n',)),
    'ci-priced-edits': (b_edits, lambda a: all(len(t) <= 8 for t in a[0].split()[4:]),
                        lambda r: ('%d %d %d\n1\n%s %s\n' % (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9),
                                                           _word(r, 'ab', 1, 6), _word(r, 'ab', 1, 6)),)),
    'ci-tolerant-common': (b_tolerant, lambda a: len(a[0]) <= 7 and len(a[1]) <= 7,
                           lambda r: ([r.randint(0, 9) for _ in range(r.randint(0, 6))],
                                      [r.randint(0, 9) for _ in range(r.randint(0, 6))], r.randint(0, 3))),
    'ci-three-feed-common': (b_three, lambda a: len(a[0]) <= 12,
                             lambda r: (_word(r, 'abc', 0, 7), _word(r, 'abc', 0, 7), _word(r, 'abc', 0, 7))),
    'ci-smooth-orderings': (b_smooth, lambda a: len(a[0]) <= 8,
                            lambda r: ([r.randint(1, 6) for _ in range(r.randint(1, 7))], r.randint(0, 4)), 400),
    'ci-hold-limit': (b_hold, lambda a: len(a[0]) <= 16,
                      lambda r: (lambda n: ([r.randint(1, 9) for _ in range(n)], [r.randint(1, 20) for _ in range(n)],
                                            r.randint(1, 20), r.randint(1, n + 1)))(r.randint(1, 8))),
    'ci-trace-count': (b_trace, lambda a: len(a[0]) * len(a[0][0]) <= 9 and len(a[1]) <= 8,
                       lambda r: (_grid(r, 'ab'), _word(r, 'ab', 1, 6))),
}


def main():
    bad = run_brutes(BRUTES, 707)
    # ci-hold-limit examples[1]: which sets of the crates 4, 3, 6 fit within 9 tonnes
    w, v, cap = [4, 3, 6], [45, 20, 40], 9
    fits = [([w[i] for i in idx], sum(v[i] for i in idx))
            for size in (2, 3) for idx in itertools.combinations(range(3), size)
            if sum(w[i] for i in idx) <= cap]
    print('hold-limit examples[1]: sets of two or more crates within 9 tonnes (tonnes, pounds):', fits)
    sys.exit(1 if bad else 0)


main()
