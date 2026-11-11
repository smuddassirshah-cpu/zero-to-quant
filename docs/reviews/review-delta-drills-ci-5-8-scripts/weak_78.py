"""Two wrong solutions that the tests caught before a fix pass and pass now.
Usage (repo root): python3 weak_78.py

1. ci-drop-point-routes (pack 7, resized 200 -> 80): the two counts reduced, the
   difference not. Old tests[11] and [13] had a negative difference; no test has now.
2. ci-first-fit-slot (pack 8, old tests[5] folded out): no gap found, so the job goes
   at the last booking's end, even when `start` is later.
For each: the candidate on every example and hidden test, then a small input inside the
constraints on which it is wrong, with the model's and my own answer."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mine_7  # noqa: E402
import mine_8  # noqa: E402

D = 'app/content/drills'

DROP = '''
MOD = 10 ** 9 + 7
def drop_point_routes(grid):
    rows, cols = len(grid), len(grid[0])
    every = [0] * cols
    clear = [0] * cols
    for i in range(rows):
        for j in range(cols):
            ch = grid[i][j]
            if ch == '#':
                every[j] = clear[j] = 0
                continue
            if i == 0 and j == 0:
                a = c = 1
            else:
                a = every[j] + (every[j - 1] if j else 0)
                c = clear[j] + (clear[j - 1] if j else 0)
            every[j] = a % MOD
            clear[j] = 0 if ch == 'P' else c % MOD
    return every[-1] - clear[-1]
'''

FIT = '''
def first_fit(bookings, start, length):
    slot = None
    prev = 0
    for s, e in bookings:
        lo = max(prev, start)
        if lo + length <= s:
            slot = lo
            break
        prev = e
    if slot is None:
        slot = bookings[-1][1] if bookings else start
    merged = []
    for s, e in sorted(bookings + [[slot, slot + length]]):
        if merged and merged[-1][1] >= s:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [slot, merged]
'''


def fails(code, d):
    env = {}
    exec(code, env)
    out = []
    for kind in ('examples', 'tests'):
        for i, t in enumerate(d[kind]):
            if eval(t['call'], env) != eval(t['expect']):
                out.append(f'{kind}[{i}]')
    return out, env[d['fn']]


def main():
    d = json.load(open(f'{D}/ci-drop-point-routes.json'))
    f, cand = fails(DROP, d)
    env = {}
    exec(d['solution'], env)
    model = env['drop_point_routes']
    print('drop-point-routes: candidate fails', f or 'nothing', 'of', len(d['examples']) + len(d['tests']))
    found = None
    for n in range(18, 41):
        for k in range(n):
            grid = ['.' * n] * k + ['.' * k + 'P' + '.' * (n - k - 1)] + ['.' * n] * (n - k - 1)
            if cand(grid) != model(grid):
                found = (n, k, grid)
                break
        if found:
            break
    n, k, grid = found
    call = "drop_point_routes(['.' * %d] * %d + ['.' * %d + 'P' + '.' * %d] + ['.' * %d] * %d)" % (n, k, k, n - k - 1, n, n - k - 1)
    print('  smallest square floor with one P on the diagonal that catches it:', call)
    print('  model', model(grid), '| mine', mine_7.drop_point_routes(grid), '| candidate', cand(grid))

    d = json.load(open(f'{D}/ci-first-fit-slot.json'))
    f, cand = fails(FIT, d)
    env = {}
    exec(d['solution'], env)
    model = env['first_fit']
    print('first-fit-slot: candidate fails', f or 'nothing', 'of', len(d['examples']) + len(d['tests']))
    for args in (([[0, 3], [3, 6], [10, 12]], 20, 4), ([[2, 4]], 9, 1)):
        import copy
        print('  first_fit%s: model %s | mine %s | candidate %s'
              % (args, model(*copy.deepcopy(args)), mine_8.first_fit(*copy.deepcopy(args)), cand(*copy.deepcopy(args))))


main()
